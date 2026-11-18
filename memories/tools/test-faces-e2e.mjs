// Run with the site's local HTTP server. FACE_TEST_IMAGE can point to a real
// portrait to additionally verify detection/name confirmation. No file uploads.
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const root = fileURLToPath(new URL('../../', import.meta.url));
const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
const fixture = process.env.FACE_TEST_IMAGE || path.join(root, 'site/memories/photos/sample/walter-uniform-1943.jpg');
const filename = path.basename(fixture);
const browser = await chromium.launch({headless: true, executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox', '--enable-unsafe-swiftshader']});
try {
  const page = await browser.newPage({viewport: {width: 390, height: 780}});
  const requests = [], errors = [];
  page.on('request', request => requests.push({url:request.url(), method:request.method()}));
  page.on('pageerror', error => errors.push(error.message));
  const url = new URL('/memories/admin/face-test.html', base).href;
  await page.route(url, route => route.fulfill({contentType:'text/html', body:'<!doctype html><html><head><meta name="viewport" content="width=device-width"><link rel="stylesheet" href="../css/skins.css"><link rel="stylesheet" href="admin.css"><link rel="stylesheet" href="faces.css"></head><body class="adm"><main class="adm-wrap" id="faces"></main></body></html>'}));
  await page.goto(url);
  await page.evaluate(async ({filename}) => {
    const {mountFaceTool} = await import('./faces.js');
    window.faceApprovals = [];
    window.faceTool = mountFaceTool(document.querySelector('#faces'), {photos:[{id:'fixture', title:'Test portrait', filename}], onApprove:names=>window.faceApprovals.push(names)});
  }, {filename});
  await page.locator('input[type=file]').setInputFiles(fixture);
  assert.equal(await page.locator('.face-mapping select').inputValue(), 'fixture');
  await page.getByRole('button', {name:'Find faces on this device',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.face-status').textContent.startsWith('Found '), null, {timeout:180000});
  const status = await page.locator('.face-status').innerText();
  const count = await page.locator('.face-card').count();
  if (process.env.FACE_TEST_IMAGE) assert.ok(count > 0, 'real fixture should produce a face');
  if (count) {
    await page.getByLabel('Name for this group', {exact:true}).first().fill('June');
    await page.getByRole('button', {name:'Add checked names to photo review'}).click();
    assert.deepEqual(await page.evaluate(()=>window.faceApprovals), [{fixture:{people:['June']}}]);
  } else {
    assert.match(await page.locator('.face-errors').innerText(), /no faces found/);
  }
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth), false, 'mobile layout should fit');
  assert.deepEqual(errors, []);
  assert.deepEqual(requests.filter(request=>request.method!=='GET'), [], 'no photo uploads');
  assert.deepEqual(requests.filter(request=>!request.url.startsWith(new URL(base).origin+'/')&&!request.url.startsWith('blob:')&&!request.url.startsWith('data:')), [], 'no external services');
  await page.getByRole('button',{name:'Clear face results from this page'}).click();
  assert.equal(await page.locator('.face-card').count(), 0);
  await page.evaluate(()=>window.faceTool.destroy());
  assert.equal(await page.locator('.face-tool').count(),0);
  console.log(`Face browser checks passed: ${status} No uploads, no external requests, no page errors, mobile layout fits.`);
} finally { await browser.close(); }
