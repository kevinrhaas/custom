// Local regression checks of invite gating and the admin invite tools.
// Start the local site server, then run node memories/tools/test-gate-e2e.mjs.
// A fresh key pair is created in memory for each run and injected into local
// browser responses. Production settings and invite keys are never changed.
// Screenshots land in memories/tools/shots/ (ignored by Git).
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { webcrypto as crypto } from 'node:crypto';
import assert from 'node:assert/strict';
import { installConfigFixture, sampleSettingsDocument } from './settings-test-fixture.mjs';
const { chromium } = createRequire(import.meta.url)('playwright');

const BASE = (process.env.BASE || process.env.ALBUM_TEST_URL || 'http://127.0.0.1:8765/memories/').replace(/\/?$/, '/');
if (!['localhost', '127.0.0.1'].includes(new URL(BASE).hostname)) throw new Error('Run fixture-key tests against a local preview only.');
const SHOTS = new URL('./shots/', import.meta.url).pathname;
mkdirSync(SHOTS, { recursive: true });
const pair = await crypto.subtle.generateKey({ name: 'ECDSA', namedCurve: 'P-256' }, true, ['sign', 'verify']);
const PUBLIC_KEY = Buffer.from(await crypto.subtle.exportKey('spki', pair.publicKey)).toString('base64');
const ADMIN_KEY = Buffer.from(await crypto.subtle.exportKey('pkcs8', pair.privateKey)).toString('base64');

// ---- mint exactly like access.js mintInvite --------------------------------
const b64 = (buf) => Buffer.from(buf).toString('base64');
const b64url = (s) => s.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
async function mint({ label = '', days = 0, iat = Date.now(), exp } = {}) {
  const priv = await crypto.subtle.importKey('pkcs8', Buffer.from(ADMIN_KEY, 'base64'),
    { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']);
  const body = { v: 1, label, iat, exp: exp ?? (days > 0 ? iat + days * 86400000 : 0), jti: Math.random().toString(36).slice(2, 10) };
  const p = b64url(b64(new TextEncoder().encode(JSON.stringify(body))));
  const sig = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, priv, new TextEncoder().encode(p));
  const code = `${p}.${b64url(b64(sig))}`; // WebCrypto ECDSA = raw r||s, what access.js verifies
  return { code, link: `${BASE}?invite=${encodeURIComponent(code)}` };
}

const HARNESS = `<!doctype html><html lang="en" data-skin="heirloom" data-mode="auto"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>(function(){var d=document.documentElement;d.dataset.scheme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}())</script>
<link rel="stylesheet" href="vendor/polecat-shell/fonts.css"><link rel="stylesheet" href="css/skins.css">
<link rel="stylesheet" href="css/app.css"><link rel="stylesheet" href="css/gate.css"></head>
<body><main id="main"></main><script type="module">
import { CONFIG } from './js/config.js';
import { runGate } from './js/gate.js';
const r = await runGate(CONFIG, document.getElementById('main'));
window.__gate = { granted: r.granted, label: r.label, isAdmin: r.isAdmin };
const welcome = document.createElement('p'); welcome.id = 'welcome';
welcome.textContent = 'Welcome' + (r.label ? ', ' + r.label : '');
document.getElementById('main').append(welcome);
</script></body></html>`;
const GATE_URL = `${BASE}__gate-test.html`;

const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] });
let checks = 0;
const ok = (cond, msg) => { assert.ok(cond, msg); checks++; console.log('  ✓', msg); };

async function ctx(colorScheme = 'light') {
  const c = await browser.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 1, colorScheme, reducedMotion: 'reduce', serviceWorkers: 'block' });
  c.setDefaultTimeout(15000);
  await installConfigFixture(c, PUBLIC_KEY, sampleSettingsDocument);
  await c.route(/__gate-test\.html/, (route) => route.fulfill({ contentType: 'text/html', body: HARNESS }));
  return c;
}
const errors = [];
const watch = (page) => page.on('pageerror', (e) => errors.push(String(e)));

try {
// 1. No token → gate shows; paste link → granted with label; reload stays in.
{
  const c = await ctx();
  const page = await c.newPage(); watch(page);
  await page.goto(GATE_URL);
  await page.waitForSelector('.gate-card');
  ok(await page.isVisible('text=This album is just for family.'), 'no token: gate shows');
  ok(await page.isVisible('text=Ask Lauren for your own link'), 'gate names the keeper');
  await page.screenshot({ path: `${SHOTS}gate-light.png`, animations: 'disabled' });

  await page.fill('#gate-code', 'abc.def');
  await page.click('.gate-btn');
  await page.waitForSelector('.gate-error:not(:empty)');
  ok((await page.textContent('.gate-error')) === "That link didn't work. Ask Lauren to send it again.", 'bad code: friendly error');
  await page.screenshot({ path: `${SHOTS}gate-error-light.png`, animations: 'disabled' });

  const expired = await mint({ label: 'Old', iat: Date.now() - 40 * 86400000, exp: Date.now() - 86400000 });
  await page.fill('#gate-code', expired.link);
  await page.click('.gate-btn');
  await page.waitForFunction(() => /expired/.test(document.querySelector('.gate-error').textContent));
  ok((await page.textContent('.gate-error')) === 'This link has expired. Ask Lauren for a fresh one.', 'expired link: friendly error');

  const amber = await mint({ label: 'Amber' });
  await page.fill('#gate-code', `Hi Amber, here's your link to the family album. Just tap it and it opens: ${amber.link}`);
  await page.click('.gate-btn');
  await page.waitForSelector('#welcome');
  ok((await page.evaluate(() => window.__gate)).label === 'Amber', 'pasted whole message: granted, label Amber');
  ok(!(await page.$('.gate')), 'gate removed after success (no reload)');
  await page.reload();
  await page.waitForSelector('#welcome');
  ok(!(await page.$('.gate')), 'reload: still granted on this device');
  await c.close();
}

// 2. Raw code paste works; ?invite=bad shows the error on arrival; ?invite=good walks right in.
{
  const c = await ctx('dark');
  const page = await c.newPage(); watch(page);
  await page.goto(`${GATE_URL}?invite=nope.nope`);
  await page.waitForSelector('.gate-error:not(:empty)');
  ok(/didn't work/.test(await page.textContent('.gate-error')), 'bad ?invite= in URL: error on arrival');
  ok(!page.url().includes('invite='), 'invite param cleaned from the address');
  await page.screenshot({ path: `${SHOTS}gate-error-dark.png`, animations: 'disabled' });
  await page.fill('#gate-code', '');
  await page.screenshot({ path: `${SHOTS}gate-dark.png`, animations: 'disabled' });
  const raw = await mint({ label: 'Grandpa Joe' });
  await page.fill('#gate-code', raw.code);
  await page.press('#gate-code', 'Enter');
  await page.waitForSelector('#welcome');
  ok((await page.textContent('#welcome')) === 'Welcome, Grandpa Joe', 'raw code + Enter: granted');
  await c.close();

  const c2 = await ctx();
  const p2 = await c2.newPage(); watch(p2);
  const tok = await mint({ label: 'Peggy', days: 30 });
  await p2.goto(tok.link.replace(BASE, GATE_URL));
  await p2.waitForSelector('#welcome');
  ok(!(await p2.$('.gate')), 'good ?invite= link: straight in, no gate');
  await c2.close();
}

// 3. Admin page: unlock with the key, make a link, the gate accepts it.
let adminLink = '';
for (const scheme of ['light', 'dark']) {
  const c = await ctx(scheme);
  const page = await c.newPage(); watch(page);
  await page.goto(`${BASE}admin/`);
  await page.waitForSelector('#unlockBtn');
  await page.screenshot({ path: `${SHOTS}admin-locked-${scheme}.png`, animations: 'disabled' });
  await page.fill('#adminKey', 'not-a-key');
  await page.click('#unlockBtn');
  await page.waitForSelector('#unlockError:not(:empty)');
  ok(/doesn't fit/.test(await page.textContent('#unlockError')), `admin (${scheme}): wrong key rejected kindly`);
  await page.fill('#adminKey', ADMIN_KEY);
  await page.click('#unlockBtn');
  await page.waitForSelector('#makeCard:not([hidden])');
  ok(await page.isVisible('text=This device can make links, edit album settings, and review photo tags.'), `admin (${scheme}): unlocked`);
  ok((await page.inputValue('#adminKey')) === '', `admin (${scheme}): key field cleared`);
  await page.fill('#who', 'Amber');
  await page.check('input[name=days][value="30"]');
  await page.click('#makeForm button[type=submit]');
  await page.waitForSelector('#result:not([hidden]) svg');
  adminLink = await page.inputValue('#resultLink');
  ok(adminLink.startsWith(`${BASE}?invite=`), `admin (${scheme}): link points at the album root`);
  ok((await page.textContent('#resultTitle')) === "Amber's link is ready", `admin (${scheme}): result titled`);
  const mail = await page.getAttribute('[data-act="mail"]', 'href');
  ok(decodeURIComponent(mail).includes("Hi Amber, here's your link to the family album"), `admin (${scheme}): warm email prewritten`);
  ok((await page.getAttribute('[data-act="sms"]', 'href')).startsWith('sms:?&body='), `admin (${scheme}): sms link`);
  ok((await page.$$('#made .adm-item')).length === 1, `admin (${scheme}): listed under links you've made`);
  await page.click('#result [data-act="copy"]').catch(() => {});
  await page.waitForTimeout(150);
  await page.evaluate(() => { document.getElementById('toast').hidden = true; });
  await page.locator('#result').scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${SHOTS}admin-link-${scheme}.png`, animations: 'disabled' });
  await page.locator('#makeCard').scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${SHOTS}admin-unlocked-${scheme}.png`, animations: 'disabled' });

  // Turn off on this device → status + the "send Kevin its ID" note.
  page.once('dialog', (d) => d.accept());
  await page.click('#made [data-do="off"]');
  await page.waitForSelector('.adm-item-tell');
  ok(/send Kevin its ID: \w+/.test(await page.textContent('.adm-item-tell')), `admin (${scheme}): turn-off explains permanent revocation`);
  await page.locator('#madeCard').scrollIntoViewIfNeeded();
  await page.evaluate(() => { document.getElementById('toast').hidden = true; });
  await page.screenshot({ path: `${SHOTS}admin-list-${scheme}.png`, animations: 'disabled' });

  // Shared settings and Drive verification are covered by test-settings-e2e.mjs.
  await c.close();
}

// 4. A link made on the admin page opens the album on a fresh device.
{
  const c = await ctx();
  const page = await c.newPage(); watch(page);
  await page.goto(adminLink.replace(BASE, GATE_URL));
  await page.waitForSelector('#welcome');
  ok((await page.evaluate(() => window.__gate)).label === 'Amber', 'admin-made link accepted by the gate');
  await c.close();
}

// 5. The keeper can also paste the admin key into the album gate.
{
  const c = await ctx();
  const page = await c.newPage(); watch(page);
  await page.goto(GATE_URL);
  await page.fill('#gate-code', ADMIN_KEY);
  await page.click('.gate-btn');
  await page.waitForSelector('#welcome');
  ok((await page.evaluate(() => window.__gate)).isAdmin === true, 'keeper admin key accepted by the album gate');
  await c.close();
}
} finally {
  await browser.close();
}

assert.deepEqual(errors, [], `page errors: ${errors.join('\n')}`);
console.log(`ok — ${checks} checks passed, no page errors`);
