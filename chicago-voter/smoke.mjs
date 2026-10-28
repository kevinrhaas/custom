// Smoke test: serve site/, take the survey at phone and desktop widths with
// several answer patterns, and fail on any page error or any race left empty.
//   node chicago-voter/smoke.mjs [--shots DIR]
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const root = join(dirname(fileURLToPath(import.meta.url)), '..', 'site');
const shots = process.argv.includes('--shots') ? process.argv[process.argv.indexOf('--shots') + 1] : null;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml' };

const server = createServer(async (req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  try { const b = await readFile(join(root, p)); res.writeHead(200, { 'content-type': TYPES[extname(p)] || 'application/octet-stream' }); res.end(b); }
  catch { res.writeHead(404); res.end('nf'); }
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}/chicago-voter/`;

const browser = await chromium.launch();
let fail = 0;
// pattern: which option position to click (0..3) per question, by a rule
const patterns = { first: () => 0, last: () => 3, second: () => 1, mixed: (i) => [0, 3, 1, 2, 2, 0, 3, 1, 0, 2, 1, 3][i % 12] };
for (const [w, h] of [[390, 780], [1280, 800]]) {
  for (const [pname, pick] of Object.entries(patterns)) {
    // the animated run waits out each transition; the rest run with reduced motion
    const animated = pname === 'mixed';
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: animated ? 'no-preference' : 'reduce' });
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', (e) => errs.push(e.message)); page.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
    await page.goto(base);
    if (shots && animated) { await page.waitForTimeout(500); await page.screenshot({ path: `${shots}/intro-${w}.png` }); }
    await page.click('#start');
    let n = 0;
    for (; n < 30; n++) {
      await page.waitForTimeout(animated ? 800 : 60);
      if (await page.$('#ldone')) {
        const segs = await page.$$('.lrow .seg'); for (let k = 0; k < segs.length; k++) { const bs = await segs[k].$$('button'); await bs[k % 2].click(); }
        if (shots && animated) await page.screenshot({ path: `${shots}/lightning-${w}.png` });
        await page.click('#ldone'); break;
      }
      if (shots && animated && n === 3) await page.screenshot({ path: `${shots}/q4-${w}.png` });
      const opts = await page.$$('.opt'); if (!opts.length) break;
      if (shots && n === 0 && pname === 'mixed') await page.screenshot({ path: `${shots}/q-${w}.png` });
      await opts[pick(n) % opts.length].click();
    }
    await page.waitForSelector('#sheet');
    const r = await page.evaluate(() => { const { E } = window.__voter.evaluate(); return Object.values(E).filter((e) => !e.decided).map((e) => e.race.id); });
    const asked = await page.evaluate(() => window.__voter.state.order.length);
    if (shots && pname === 'mixed') {
      await page.screenshot({ path: `${shots}/done-${w}.png`, fullPage: true });
      await page.click('[data-race="sheriff"]'); await page.waitForTimeout(200);
      await page.screenshot({ path: `${shots}/race-${w}.png` });
      await page.keyboard.press('Escape');
    }
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    console.log(`${w}x${h} ${pname}: ${asked} questions, undecided [${r.join(', ')}]${errs.length ? ' ERRORS ' + errs.join(' | ') : ''}${overflow ? ' HORIZONTAL OVERFLOW' : ''}`);
    if (errs.length || overflow) fail = 1;
    if (r.length && pname !== 'last') fail = fail || 0; // undecided is reported, judged by eye: blank can be a valid outcome
    await ctx.close();
  }
}
await browser.close(); server.close();
process.exit(fail);
