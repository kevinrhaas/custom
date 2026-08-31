import { createServer } from 'node:http';
import { mkdir, readFile, stat } from 'node:fs/promises';
import { dirname, extname, join, normalize } from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const projectRoot = dirname(fileURLToPath(import.meta.url));
const siteRoot = join(dirname(projectRoot), 'site', 'zion-bryce');
const artifactRoot = join(dirname(dirname(projectRoot)), 'qa');
const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
  '.svg': 'image/svg+xml'
};
const failures = [];
const expect = (condition, message) => { if (!condition) failures.push(message); };

await mkdir(artifactRoot, { recursive: true });

const server = createServer(async (request, response) => {
  try {
    const rawPath = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const relative = rawPath === '/' ? 'index.html' : rawPath.replace(/^\/+/, '');
    let file = normalize(join(siteRoot, relative));
    if (!file.startsWith(siteRoot)) throw new Error('Invalid path');
    if ((await stat(file)).isDirectory()) file = join(file, 'index.html');
    const body = await readFile(file);
    response.writeHead(200, { 'content-type': mime[extname(file)] || 'application/octet-stream', 'cache-control': 'no-cache' });
    response.end(body);
  } catch (error) {
    response.writeHead(404, { 'content-type': 'text/plain' });
    response.end('Not found');
  }
});

await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const { port } = server.address();
const baseUrl = `http://127.0.0.1:${port}/`;

let browser;
try {
  browser = await chromium.launch({ headless: true });

  const desktop = await browser.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true });
  const page = await desktop.newPage();
  const consoleErrors = [];
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('pageerror', (error) => consoleErrors.push(error.message));
  await page.goto(baseUrl, { waitUntil: 'networkidle' });
  await page.waitForSelector('#daysList .day-card');

  expect(await page.locator('#daysList .day-card').count() === 9, 'desktop: expected nine day cards');
  expect(await page.locator('#tripTitle').isVisible(), 'desktop: trip title is not visible');
  expect(await page.locator('.trip-ticket').isVisible(), 'desktop: trip summary ticket is not visible');
  await page.screenshot({ path: join(artifactRoot, 'zion-bryce-desktop.png'), fullPage: false });

  await page.getByRole('button', { name: 'Swap days' }).click();
  expect(await page.locator('[data-park-tab]').count() === 2, 'desktop: expected Zion and Bryce planning tabs');
  expect(await page.locator('#assignmentGrid select').count() === 3, 'desktop: expected three flexible-day assignments');
  expect(await page.locator('#weatherGrid .weather-card').count() === 3, 'desktop: expected three weather cards');
  await page.locator('#assign-2026-09-07').selectOption('narrows');
  await page.getByRole('button', { name: 'Plan' }).click();
  expect((await page.locator('.day-card[data-day="3"] h3').textContent()).includes('Narrows'), 'desktop: flexible assignment did not update plan');

  await page.getByRole('button', { name: 'Swap days' }).click();
  await page.locator('[data-park-tab="bryce"]').click();
  expect(await page.locator('#brycePlannerGrid select').count() === 3, 'desktop: expected three Bryce planning choices');
  await page.locator('#bryce-afternoon').selectOption('rim');
  await page.getByRole('button', { name: 'Plan' }).click();
  await page.locator('.day-card[data-day="7"] summary').click();
  expect((await page.locator('.day-card[data-day="7"]').innerText()).includes('Lodge reset + amphitheater overlooks'), 'desktop: Bryce choice did not update Day 7');

  await page.getByRole('button', { name: 'Pack' }).click();
  const firstCheck = page.locator('[data-check-id]').first();
  const firstCheckId = await firstCheck.getAttribute('data-check-id');
  // The native input is intentionally visually hidden; exercise the same
  // associated label a keyboard/touch user activates instead of force-clicking
  // through the presentation layer.
  await page.locator(`[data-check-row="${firstCheckId}"] .check-copy`).click();
  expect(await firstCheck.isChecked(), 'desktop: checklist label did not toggle its input');
  await page.reload({ waitUntil: 'networkidle' });
  expect(await page.locator(`[data-check-id="${firstCheckId}"]`).isChecked(), 'desktop: checklist state did not persist');

  await page.getByRole('button', { name: 'Notes' }).click();
  await page.locator('#stay-bryce-lodge').fill('local-only-test');
  await page.locator('#tripNotes').fill('Offline field note');
  await page.waitForTimeout(400);
  await page.reload({ waitUntil: 'networkidle' });
  expect(await page.locator('#stay-bryce-lodge').inputValue() === 'local-only-test', 'desktop: private stay field did not persist');
  expect(await page.locator('#tripNotes').inputValue() === 'Offline field note', 'desktop: notes did not persist');

  await page.getByRole('button', { name: 'Plan' }).click();
  const downloadPromise = page.waitForEvent('download');
  await page.locator('#calendarButton').click();
  const download = await downloadPromise;
  expect(download.suggestedFilename() === 'zion-bryce-2026.ics', 'desktop: calendar filename is incorrect');

  await desktop.setOffline(true);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#daysList .day-card');
  expect(await page.locator('#daysList .day-card').count() === 9, 'desktop: offline reload did not restore the plan');
  await desktop.setOffline(false);
  expect(consoleErrors.length === 0, `desktop: console errors: ${consoleErrors.join(' | ')}`);
  await desktop.close();

  const mobile = await browser.newContext({ viewport: { width: 390, height: 780 }, isMobile: true, hasTouch: true });
  const phone = await mobile.newPage();
  const mobileErrors = [];
  phone.on('console', (message) => { if (message.type() === 'error') mobileErrors.push(message.text()); });
  phone.on('pageerror', (error) => mobileErrors.push(error.message));
  await phone.goto(baseUrl, { waitUntil: 'networkidle' });
  await phone.waitForSelector('#daysList .day-card');
  const widthCheck = await phone.evaluate(() => ({ scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth }));
  expect(widthCheck.scroll <= widthCheck.client, `mobile: horizontal overflow (${widthCheck.scroll}px > ${widthCheck.client}px)`);
  const navBox = await phone.locator('.view-nav').boundingBox();
  expect(navBox && Math.round(navBox.y + navBox.height) <= 781, 'mobile: bottom navigation is outside the viewport');
  expect(await phone.locator('.view-tab').count() === 5, 'mobile: expected five bottom navigation tabs');
  await phone.screenshot({ path: join(artifactRoot, 'zion-bryce-mobile.png'), fullPage: false });

  await phone.getByRole('button', { name: 'Swap days' }).click();
  await phone.screenshot({ path: join(artifactRoot, 'zion-bryce-mobile-swap.png'), fullPage: false });
  expect(await phone.locator('#assignmentGrid select').count() === 3, 'mobile: assignment controls are missing');
  await phone.locator('[data-park-tab="bryce"]').click();
  expect(await phone.locator('#brycePlannerGrid select').count() === 3, 'mobile: Bryce planning controls are missing');
  expect(mobileErrors.length === 0, `mobile: console errors: ${mobileErrors.join(' | ')}`);
  await mobile.close();
} catch (error) {
  failures.push(`browser harness: ${error.stack || error.message}`);
} finally {
  await browser?.close();
  await new Promise((resolve) => server.close(resolve));
}

if (failures.length) {
  console.error(`Browser checks failed (${failures.length}):`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`Browser checks passed at 1440×1000 and 390×780. Screenshots: ${artifactRoot}`);
