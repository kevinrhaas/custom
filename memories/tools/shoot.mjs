// shoot.mjs — screenshot + smoke the album. Usage:
//   node memories/tools/shoot.mjs [outDir] [skins=heirloom] [adminKeyFile]
// Serves site/ itself, mints an invite with the admin key (kept OUTSIDE the
// repo), and visits every view at 390×780 and 1280×800, failing on pageerrors.
import { chromium } from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { webcrypto as crypto } from 'node:crypto';

const ROOT = path.resolve(process.env.SITE_ROOT || new URL('../../site', import.meta.url).pathname);
const out = path.resolve(process.argv[2] || '/tmp/shots');
const skins = (process.argv[3] || 'heirloom').split(',');
const keyFile = process.argv[4] || '/home/claude/secrets/memories-ADMIN-KEY.txt';
fs.mkdirSync(out, { recursive: true });

const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json', '.mjs': 'text/javascript' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end('nf'); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0);
const port = server.address().port;
const base = `http://localhost:${port}/memories/`;

const b64url = (buf) => Buffer.from(buf).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
async function mint(label) {
  const priv = await crypto.subtle.importKey('pkcs8', Buffer.from(fs.readFileSync(keyFile, 'utf8').trim(), 'base64'), { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']);
  const body = { v: 1, label, iat: Date.now(), exp: 0, jti: 'shoot' + Math.random().toString(36).slice(2, 5) };
  const p = b64url(Buffer.from(JSON.stringify(body)));
  const sig = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, priv, new TextEncoder().encode(p));
  return `${p}.${b64url(sig)}`;
}

const errors = [];
const browser = await chromium.launch();
const code = await mint('Amber');
for (const [vw, vh, tag] of [[390, 780, 'm'], [1280, 800, 'd']]) {
  for (const scheme of ['light', 'dark']) {
    for (const skin of skins) {
      const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, colorScheme: scheme, deviceScaleFactor: tag === 'm' ? 2 : 1 });
      const page = await ctx.newPage();
      page.on('pageerror', (e) => errors.push(`${tag}/${scheme}/${skin}: ${e.message}`));
      page.on('console', (m) => { if (m.type() === 'error' && !/favicon|ERR_NAME|Failed to load resource/.test(m.text())) errors.push(`${tag}/${scheme}/${skin} console: ${m.text()}`); });
      await page.addInitScript((s) => { localStorage.setItem('memories.prefs', JSON.stringify({ skin: s, mode: 'auto', text: 'regular' })); }, skin);
      const snap = async (name, full = true) => { await page.waitForTimeout(700); await page.screenshot({ path: `${out}/${tag}-${scheme}-${skin}-${name}.png`, fullPage: full }); };
      if (skin === skins[0] && scheme === 'light') { await page.goto(base); await page.waitForTimeout(600); await snap('gate', false); }
      await page.goto(`${base}?invite=${code}`);
      await page.waitForSelector('.hero', { timeout: 10000 });
      await snap('home');
      await page.goto(`${base}#/chapter/growing`); await page.waitForSelector('.tile'); await snap('chapter');
      await page.locator('.tile').nth(2).click(); await page.waitForSelector('#viewer:not([hidden])'); await snap('viewer', false);
      await page.keyboard.press('Escape');
      await page.goto(`${base}#/years/1960`); await snap('years', false);
      await page.goto(`${base}#/search?q=horse`); await page.waitForTimeout(400); await snap('search');
      if (skin === skins[0] && scheme === 'light') {
        await page.goto(`${base}#/`); await page.waitForSelector('.hero');
        await page.locator(tag === 'm' ? '[data-look]' : '#lookButton').click(); await snap('look', false);
        await page.keyboard.press('Escape');
        await page.locator('[data-play="all"]').click(); await page.waitForTimeout(1800); await snap('show', false);
      }
      await ctx.close();
    }
  }
}
await browser.close(); server.close();
console.log(errors.length ? `ERRORS (${errors.length}):\n` + [...new Set(errors)].join('\n') : 'zero pageerrors');
process.exit(errors.length ? 1 : 0);
