// smoke-test.mjs — the ship gate for the Porchfest Planner.
//
// Serves custom/porchfest/, opens the marketing page and the app in Chromium
// AND WebKit at mobile (390x780) and desktop (1440x900), and fails on any
// pageerror, any console error, or any key surface that never renders.
// WebKit is iOS Safari's engine and catches iOS-only breakage Chromium
// tolerates. Mobile is a release gate, not an afterthought.
//
//   node build/smoke-test.mjs
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, dirname } from 'node:path';
import { chromium, webkit } from 'playwright';

const ROOT = join(dirname(new URL(import.meta.url).pathname), '..', 'site', 'porchfest');
const PORT = 4191;
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml' };

const server = http.createServer(async (req, res) => {
  try {
    let p = normalize(decodeURIComponent(req.url.split('?')[0])).replace(/^(\.\.[/\\])+/, '');
    if (p.endsWith('/')) p += 'index.html';
    const body = await readFile(join(ROOT, p));
    res.writeHead(200, { 'Content-Type': MIME[extname(p)] || 'application/octet-stream' });
    res.end(body);
  } catch { res.writeHead(404); res.end('nope'); }
});
await new Promise(r => server.listen(PORT, r));
const at = (p) => `http://localhost:${PORT}${p}`;

let failures = 0;
const fail = (m) => { failures++; console.log(`   ✗ ${m}`); };
const ok = (m) => console.log(`   ✓ ${m}`);

function watch(page, label) {
  const errs = [];
  page.on('pageerror', e => errs.push(`pageerror: ${e.message}`));
  page.on('console', m => { if (m.type() === 'error') errs.push(`console.error: ${m.text()}`); });
  page.on('requestfailed', r => {
    // The app must make zero network requests; band photos are the one
    // deliberate exception and are allowed to fail (offline / hotlink).
    if (!/porchfest-band-photos|drive\.google/.test(r.url())) errs.push(`requestfailed: ${r.url()}`);
  });
  return () => { errs.forEach(e => fail(`${label} — ${e}`)); return errs.length === 0; };
}

const skipped = [];
for (const [name, browserType] of [['chromium', chromium], ['webkit', webkit]]) {
  let browser;
  try {
    browser = await browserType.launch();
  } catch (e) {
    // CI installs both engines. Locally one may be missing — say so loudly
    // rather than passing silently on half the matrix.
    skipped.push(name);
    console.log(`\n! ${name} unavailable — NOT VERIFIED (${String(e.message).split('\n')[0]})`);
    continue;
  }
  for (const [vp, size] of [['mobile', { width: 390, height: 780 }], ['desktop', { width: 1440, height: 900 }]]) {
    const ctx = await browser.newContext({ viewport: size, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const tag = `${name}/${vp}`;
    console.log(`\n${tag}`);

    // ---- marketing page ----
    let done = watch(page, tag);
    await page.goto(at('/index.html'), { waitUntil: 'networkidle' });
    const h1 = await page.textContent('h1').catch(() => '');
    if (!h1 || !/porches/i.test(h1)) fail(`${tag} — marketing h1 missing (got "${h1}")`);
    else ok('marketing page renders');
    const appLink = await page.getAttribute('a[href*="app/"]', 'href').catch(() => null);
    if (!appLink) fail(`${tag} — marketing page has no link to the app`); else ok('marketing links to app');
    done();

    // ---- the app ----
    done = watch(page, tag);
    await page.goto(at('/app/'), { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);

    const bandCount = await page.evaluate(() => JSON.parse(document.getElementById('payload').textContent).bands.length);
    if (bandCount !== 91) fail(`${tag} — expected 91 bands, payload has ${bandCount}`); else ok(`payload: ${bandCount} bands`);

    // controls populated
    const nTaste = await page.locator('#taste .taste').count();
    if (nTaste !== 10) fail(`${tag} — expected 10 taste sliders, found ${nTaste}`); else ok('10 taste dimensions');
    const nGenre = await page.locator('#genres .chip').count();
    if (nGenre < 20) fail(`${tag} — only ${nGenre} genre chips`); else ok(`${nGenre} genre chips`);

    // A route must exist on load, with nothing clicked.
    const t0 = Date.now();
    await page.waitForFunction(() => document.querySelectorAll('#stops .stop').length > 0, null, { timeout: 25000 })
      .catch(() => fail(`${tag} — no route on load`));
    const ms = Date.now() - t0;
    ok('routes on load without a click');
    if (vp === 'mobile') await page.locator('[data-go="tune"]:visible').first().click();

    // Moving a dial must re-plan on its own.
    const before = await page.textContent('#stops');
    await page.evaluate(() => {
      const s = document.querySelector('.taste[data-dim="loudness"] input');
      s.value = '-2'; s.dispatchEvent(new Event('input', { bubbles: true }));
    });
    await page.waitForTimeout(1400);
    const after = await page.textContent('#stops');
    if (before === after) fail(`${tag} — turning a dial did not change the schedule`);
    else ok('dial change re-plans live');
    await page.evaluate(() => {
      const s = document.querySelector('.taste[data-dim="loudness"] input');
      s.value = '0'; s.dispatchEvent(new Event('input', { bubbles: true }));
    });
    await page.waitForTimeout(1400);

    // Band-count constraints: exactly N, then a range.
    const setCount = async (min, max) => {
      await page.selectOption('#minB', String(min));
      await page.selectOption('#maxB', String(max));
      await page.waitForTimeout(1500);
      return page.locator('#stops .stop').count();
    };
    const exact6 = await setCount(6, 6);
    if (exact6 !== 6) fail(`${tag} — asked for exactly 6 bands, got ${exact6}`);
    else ok('exactly 6 bands honoured');
    const ranged = await setCount(3, 5);
    if (ranged < 3 || ranged > 5) fail(`${tag} — asked for 3-5 bands, got ${ranged}`);
    else ok(`3-5 band range honoured (${ranged})`);
    const capped = await setCount(0, 4);
    if (capped > 4) fail(`${tag} — "at most 4" produced ${capped}`); else ok(`"at most 4" honoured (${capped})`);
    await setCount(0, 0);

    // Avoiding a genre must take it out of the route, live.
    const countryTag = async () => page.evaluate(() =>
      [...document.querySelectorAll('#stops .stop .tg')].map(t => t.textContent).includes('country'));
    await page.evaluate(() => {   // seek country first, so it's definitely present
      const c = document.querySelector('[data-tag="country"]');
      c.click();
    });
    await page.waitForTimeout(1500);
    const hadCountry = await countryTag();
    await page.evaluate(() => document.querySelector('[data-tag="country"]').click()); // -> avoid
    await page.waitForTimeout(1500);
    const stillCountry = await countryTag();
    if (stillCountry) fail(`${tag} — avoided "country" but it is still in the route`);
    else ok(`avoiding a genre drops it live${hadCountry ? ' (was present when sought)' : ''}`);
    await page.evaluate(() => document.querySelector('[data-tag="country"]').click()); // -> neutral
    await page.waitForTimeout(1200);

    // ---- draw ("big names") ----
    // The slider must actually move the planner: asking for big names has to
    // raise the mean draw of the routed acts, and asking for hidden gems has
    // to lower it. Comparing means rather than asserting specific bands keeps
    // this robust against the planner's randomised restarts.
    const meanDraw = () => page.evaluate(() => {
      const D = JSON.parse(document.getElementById('payload').textContent);
      const by = new Map(D.bands.map(b => [b.n, b.dw]));
      const names = [...document.querySelectorAll('#stops .stop h3')].map(h => h.textContent.trim());
      const vals = names.map(n => by.get(n)).filter(v => typeof v === 'number');
      return vals.length ? vals.reduce((a, c) => a + c, 0) / vals.length : null;
    });
    const setPop = async (v) => {
      await page.evaluate((val) => {
        const s = document.querySelector('#popR');
        s.value = String(val); s.dispatchEvent(new Event('input', { bubbles: true }));
      }, v);
      await page.waitForTimeout(1600);
    };
    const hasDraw = await page.evaluate(() =>
      JSON.parse(document.getElementById('payload').textContent).bands.every(b => typeof b.dw === 'number'));
    if (!hasDraw) fail(`${tag} — payload bands are missing draw scores`); else ok('every band carries a draw score');
    if (await page.locator('#popR').count() !== 1) fail(`${tag} — no draw slider`); else ok('draw slider present');

    const drawNeutral = await meanDraw();
    await setPop(2);
    const drawBig = await meanDraw();
    await setPop(-2);
    const drawGems = await meanDraw();
    await setPop(0);
    if (drawBig === null || drawNeutral === null || drawGems === null) {
      fail(`${tag} — draw slider emptied the route`);
    } else {
      if (drawBig <= drawNeutral)
        fail(`${tag} — "big names" did not raise mean draw (${drawNeutral.toFixed(1)} -> ${drawBig.toFixed(1)})`);
      else ok(`"big names" raises mean draw (${drawNeutral.toFixed(1)} -> ${drawBig.toFixed(1)})`);
      if (drawGems >= drawNeutral)
        fail(`${tag} — "hidden gems" did not lower mean draw (${drawNeutral.toFixed(1)} -> ${drawGems.toFixed(1)})`);
      else ok(`"hidden gems" lowers mean draw (${drawNeutral.toFixed(1)} -> ${drawGems.toFixed(1)})`);
    }

    // The preset is the one-tap version of the same thing.
    await page.evaluate(() => [...document.querySelectorAll('[data-preset]')]
      .find(b => b.dataset.preset === 'Big names').click());
    await page.waitForTimeout(1600);
    const presetPop = await page.evaluate(() => +document.querySelector('#popR').value);
    if (presetPop !== 2) fail(`${tag} — "Big names" preset left the slider at ${presetPop}`);
    else ok('"Big names" preset drives the slider');
    await page.evaluate(() => [...document.querySelectorAll('[data-preset]')]
      .find(b => b.dataset.preset === '__clear').click());
    await page.waitForTimeout(1600);
    const clearedPop = await page.evaluate(() => +document.querySelector('#popR').value);
    if (clearedPop !== 0) fail(`${tag} — Reset left the draw slider at ${clearedPop}`);
    else ok('Reset clears the draw preference');

    // ---- who's walking (the crew presets) ----
    const crewNames = await page.evaluate(() =>
      [...document.querySelectorAll('#crew [data-preset]')].map(b => b.dataset.preset));
    if (crewNames.length !== 4) fail(`${tag} — expected 4 group presets, found ${crewNames.length}`);
    else ok(`group presets: ${crewNames.join(', ')}`);

    const clickPreset = async (name) => {
      await page.evaluate((n) => [...document.querySelectorAll('[data-preset]')]
        .find(b => b.dataset.preset === n).click(), name);
      await page.waitForTimeout(1800);
    };
    // "Easy does it" is the one that also eases the walking, so it is the one
    // worth asserting: a preset that only moved taste would quietly under-serve
    // someone whose limit is the distance, not the volume.
    await clickPreset('Easy does it');
    const easy = await page.evaluate(() => ({
      pace: +document.querySelector('#pace').value,
      max: +document.querySelector('#maxB').value,
      tags: [...document.querySelectorAll('#genres .chip[data-s="1"]')].map(c => c.dataset.tag),
      stops: document.querySelectorAll('#stops .stop').length,
      on: !!document.querySelector('#crew button.on'),
    }));
    if (easy.pace !== 3) fail(`${tag} — "Easy does it" left pace at ${easy.pace}, expected 3`);
    else ok(`"Easy does it" eases the pace (${easy.pace} km/h)`);
    if (easy.max !== 4 || easy.stops > 4) fail(`${tag} — "Easy does it" gave ${easy.stops} stops (cap ${easy.max})`);
    else ok(`"Easy does it" caps the walk (${easy.stops} stops)`);
    if (!easy.tags.length) fail(`${tag} — "Easy does it" set no genres`);
    else ok(`"Easy does it" seeks genres (${easy.tags.join(', ')})`);
    if (!easy.on) fail(`${tag} — no group preset shows as selected`); else ok('selected group preset is marked');

    // Reset has to undo the logistics too, or the slow pace outlives the preset.
    await clickPreset('__clear');
    const afterReset = await page.evaluate(() => ({
      pace: +document.querySelector('#pace').value,
      max: +document.querySelector('#maxB').value,
      tags: document.querySelectorAll('#genres .chip[data-s="1"]').length,
    }));
    if (afterReset.pace !== 4.5 || afterReset.max !== 0 || afterReset.tags !== 0)
      fail(`${tag} — Reset left pace ${afterReset.pace}, cap ${afterReset.max}, ${afterReset.tags} genres`);
    else ok('Reset restores pace, band cap and genres');

    const stops = await page.locator('#stops .stop').count();
    if (stops > 0) ok(`planned ${stops} stops in ${ms} ms`);
    if (ms > 8000) fail(`${tag} — planner took ${ms} ms (>8s)`);

    // summary populated
    const sBands = await page.textContent('#sBands');
    if (String(stops) !== sBands) fail(`${tag} — summary says ${sBands} bands, list shows ${stops}`);
    else ok(`summary agrees (${sBands} bands, ${await page.textContent('#sWalk')} walking)`);

    // every stop must sit inside that band's advertised set window
    const outside = await page.evaluate(() => {
      const to24 = (s) => { const m = s.match(/(\d+):(\d+)\s*(AM|PM)/); return ((+m[1] % 12) + (m[3] === 'PM' ? 12 : 0)) * 60 + +m[2]; };
      const bad = [];
      for (const row of document.querySelectorAll('#stops .stop')) {
        const begin = to24(row.querySelector('.when b').textContent);
        const m = row.querySelector('.meta').textContent.match(/set (\d+:\d+ [AP]M)–(\d+:\d+ [AP]M)/);
        if (!m) { bad.push('unparsable meta'); continue; }
        const [s, e] = [to24(m[1]), to24(m[2])];
        if (begin < s - 0.5 || begin >= e) bad.push(`${row.querySelector('h3').textContent}: arrive ${begin}, window ${s}-${e}`);
      }
      return bad;
    });
    if (outside.length) outside.forEach(b => fail(`${tag} — stop outside its set window: ${b}`));
    else ok('every stop is inside its set window');

    const chrono = await page.evaluate(() => {
      const rows = [...document.querySelectorAll('#stops .stop .when b')].map(e => e.textContent);
      const to24 = (s) => { const m = s.match(/(\d+):(\d+) (AM|PM)/); return ((+m[1] % 12) + (m[3] === 'PM' ? 12 : 0)) * 60 + +m[2]; };
      const t = rows.map(to24);
      return t.every((v, i) => i === 0 || v >= t[i - 1]);
    });
    if (!chrono) fail(`${tag} — schedule is not in chronological order`); else ok('schedule is chronological');

    // map drew a route
    const routePaths = await page.evaluate(() =>
      [...document.querySelectorAll('#map path')].filter(p => (p.getAttribute('stroke') || '').includes('brand')).length);
    if (routePaths < 1) fail(`${tag} — no route drawn on the map`); else ok('map drew the route');
    // Pins merge when they'd overlap, so read the stops each pin covers from
    // data-stops rather than from the (deliberately abbreviated) label.
    const pinned = await page.evaluate(() =>
      [...document.querySelectorAll('#map rect[data-stops]')].flatMap(r => r.getAttribute('data-stops').split(',')));
    const missingPins = Array.from({ length: stops }, (_, i) => String(i + 1)).filter(n => !pinned.includes(n));
    if (missingPins.length) fail(`${tag} — stops missing a map pin: ${missingPins.join(', ')}`);
    else ok(`all ${stops} stops pinned on the map`);

    // No pin may sit on top of another — overlaps must cluster, not stack.
    const collide = await page.evaluate(() => {
      const pins = [...document.querySelectorAll('#map rect[rx="9"]')].map(r => ({
        x: +r.getAttribute('x'), y: +r.getAttribute('y'),
        w: +r.getAttribute('width'), h: +r.getAttribute('height'),
      }));
      const hits = [];
      for (let i = 0; i < pins.length; i++) for (let j = i + 1; j < pins.length; j++) {
        const a = pins[i], b = pins[j];
        if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h)
          hits.push(`(${a.x.toFixed(0)},${a.y.toFixed(0)})×(${b.x.toFixed(0)},${b.y.toFixed(0)})`);
      }
      return hits;
    });
    if (collide.length) fail(`${tag} — ${collide.length} overlapping map pin(s): ${collide.slice(0, 3).join(' ')}`);
    else ok('no pins overlap');

    // share link round-trip
    const url = await page.evaluate(() => location.hash);
    if (!/^#s=/.test(url)) fail(`${tag} — no share hash written`);
    else {
      const p2 = await ctx.newPage();
      const done2 = watch(p2, `${tag}/shared`);
      await p2.goto(at('/app/') + url, { waitUntil: 'networkidle' });
      await p2.waitForTimeout(400);
      const stops2 = await p2.locator('#stops .stop').count();
      if (stops2 !== stops) fail(`${tag} — shared link rebuilt ${stops2} stops, expected ${stops}`);
      else ok(`share link round-trips (${stops2} stops)`);
      done2();
      await p2.close();

      // A shared plan must carry the draw preference, and a link cut before
      // the slider existed must still open (no draw preference, old behaviour).
      await setPop(2);
      const url2 = await page.evaluate(() => location.hash);
      const p3 = await ctx.newPage();
      const done3 = watch(p3, `${tag}/shared-draw`);
      await p3.goto(at('/app/') + url2, { waitUntil: 'networkidle' });
      await p3.waitForTimeout(500);
      const pop3 = await p3.evaluate(() => +document.querySelector('#popR').value);
      if (pop3 !== 2) fail(`${tag} — shared link lost the draw preference (got ${pop3})`);
      else ok('share link round-trips the draw preference');
      const legacy = await p3.evaluate(() => {
        // The hash is `#s=<state>&v=<view>` now; take just the state.
        const s = location.hash.replace(/^#s=/, '').split('&')[0];
        const o = JSON.parse(decodeURIComponent(escape(atob(
          s.replace(/-/g, '+').replace(/_/g, '/')))));
        delete o.pw;                                  // a link from before the slider
        return btoa(unescape(encodeURIComponent(JSON.stringify(o))))
          .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
      });
      done3();
      await p3.close();

      // Fresh page, not a hash swap — changing only the fragment does not
      // reload the document, so the old state would survive and prove nothing.
      const p4 = await ctx.newPage();
      const done4 = watch(p4, `${tag}/shared-legacy`);
      await p4.goto(at('/app/') + '#s=' + legacy, { waitUntil: 'networkidle' });
      await p4.waitForTimeout(500);
      const popLegacy = await p4.evaluate(() => +document.querySelector('#popR').value);
      const legacyStops = await p4.locator('#stops .stop').count();
      if (popLegacy !== 0 || legacyStops === 0)
        fail(`${tag} — pre-draw share link broke (pop ${popLegacy}, ${legacyStops} stops)`);
      else ok('pre-draw share links still open');
      done4();
      await p4.close();
      await setPop(0);
    }

    // A stop must be able to open that band's full card, or the schedule is a
    // dead end when you want to know who you're about to go and see.
    // On mobile the schedule lives behind its own tab, so get there first.
    if (vp === 'mobile') await page.locator('[data-go="route"]:visible').first().click();
    await page.waitForTimeout(250);
    const viewBeforeJump = await page.evaluate(() => document.body.dataset.view);
    const firstStopBand = await page.textContent('#stops .stop h3');
    await page.locator('#stops .stop .morebtn').first().click();
    await page.waitForTimeout(600);
    const jumped = await page.evaluate(() => {
      const f = document.querySelector('#bgrid .card.focus');
      return { view: document.body.dataset.view, name: f ? f.querySelector('h3').textContent.trim() : null,
               full: f ? !!f.querySelector('p') : false };
    });
    const wantName = (firstStopBand || '').replace(/★$/, '').trim();
    if (jumped.view !== 'bands') fail(`${tag} — "Full profile" left the view on ${jumped.view}`);
    else if (jumped.name !== wantName) fail(`${tag} — jumped to "${jumped.name}", expected "${wantName}"`);
    else if (!jumped.full) fail(`${tag} — focused card has no full profile text`);
    else ok(`"Full profile" opens the band card (${jumped.name})`);

    // The flow that will actually happen: read the schedule, tap through to a
    // band, then Back to carry on down the list. Desktop shows the schedule
    // without switching tabs, so assert it returns where it came FROM rather
    // than to a hardcoded view.
    await page.goBack();
    await page.waitForTimeout(700);
    const cameBack = await page.evaluate(() => document.body.dataset.view);
    if (cameBack !== viewBeforeJump)
      fail(`${tag} — Back from a band card landed on ${cameBack}, came from ${viewBeforeJump}`);
    else ok(`Back from a band card returns to ${cameBack}`);

    // ---- browser Back / Forward ----
    // Views are the app's navigation, so they must be history entries. On
    // Android Back is a system gesture; leaving the app on a tab change is
    // the bug this guards against.
    const view = () => page.evaluate(() => document.body.dataset.view);
    const goView = async (v) => {
      await page.locator(`[data-go="${v}"]:visible`).first().click();
      await page.waitForTimeout(350);
    };
    await goView('tune');
    await goView('route');
    await goView('map');
    const beforeBack = await view();
    await page.goBack(); await page.waitForTimeout(700);
    const back1 = await view();
    if (back1 !== 'route') fail(`${tag} — Back from ${beforeBack} landed on ${back1}, expected route`);
    else ok('Back returns to the previous view');
    await page.goBack(); await page.waitForTimeout(700);
    const back2 = await view();
    if (back2 !== 'tune') fail(`${tag} — second Back landed on ${back2}, expected tune`);
    else ok('Back steps back through views');
    await page.goForward(); await page.waitForTimeout(700);
    const fwd = await view();
    if (fwd !== 'route') fail(`${tag} — Forward landed on ${fwd}, expected route`);
    else ok('Forward re-enters the view');

    // A route must survive the trip, not come back empty or re-randomised.
    const afterNav = await page.locator('#stops .stop').count();
    if (afterNav === 0) fail(`${tag} — the route was lost navigating history`);
    else ok(`route survives Back/Forward (${afterNav} stops)`);

    // Tuning must NOT push entries, or Back becomes useless: an afternoon of
    // dial-turning would bury the view you actually wanted to return to.
    await goView('tune');
    const depth0 = await page.evaluate(() => history.length);
    await page.evaluate(() => {
      const s = document.querySelector('.taste[data-dim="energy"] input');
      for (const v of ['1', '2', '-1', '0']) { s.value = v; s.dispatchEvent(new Event('input', { bubbles: true })); }
    });
    await page.waitForTimeout(1800);
    const depth1 = await page.evaluate(() => history.length);
    if (depth1 !== depth0) fail(`${tag} — tuning pushed ${depth1 - depth0} history entries, expected 0`);
    else ok('tuning replaces rather than pushing history');

    // bands browser
    await page.locator('[data-go="bands"]:visible').first().click();
    await page.waitForTimeout(250);
    const cards = await page.locator('#bgrid .card').count();
    if (cards !== 91) fail(`${tag} — bands view shows ${cards} cards`); else ok('bands browser lists all 91');
    await page.fill('#bq', 'jazz');
    await page.waitForTimeout(200);
    const filtered = await page.locator('#bgrid .card').count();
    if (filtered === 0 || filtered >= 91) fail(`${tag} — genre search returned ${filtered}`); else ok(`search filters (jazz -> ${filtered})`);
    await page.fill('#bq', '');
    await page.waitForTimeout(200);

    // Sorting by biggest names must actually order by draw, descending, and
    // the badge must land on the acts that earned it — with its evidence.
    await page.selectOption('#bsort', 'draw');
    await page.waitForTimeout(250);
    const sorted = await page.evaluate(() => {
      const D = JSON.parse(document.getElementById('payload').textContent);
      const by = new Map(D.bands.map(b => [b.n, b.dw]));
      return [...document.querySelectorAll('#bgrid .card h3')].map(h => by.get(h.textContent.trim()));
    });
    const descending = sorted.every((v, i) => i === 0 || v <= sorted[i - 1]);
    if (!descending) fail(`${tag} — "biggest names" sort is not descending by draw`);
    else ok(`sorts by draw (top: ${sorted[0]}, bottom: ${sorted[sorted.length - 1]})`);

    const badges = await page.evaluate(() => {
      const D = JSON.parse(document.getElementById('payload').textContent);
      const expect = D.bands.filter(b => b.dw >= 42).length;
      const els = [...document.querySelectorAll('#bgrid .drawbadge')];
      return { expect, got: els.length, titled: els.filter(e => (e.getAttribute('title') || '').trim()).length };
    });
    if (badges.got !== badges.expect)
      fail(`${tag} — ${badges.got} draw badges rendered, expected ${badges.expect}`);
    else ok(`${badges.got} bands badged as notable`);
    if (badges.titled !== badges.got)
      fail(`${tag} — ${badges.got - badges.titled} badge(s) claim notability with no evidence`);
    else ok('every badge carries its evidence');
    await page.selectOption('#bsort', 'time');
    await page.waitForTimeout(200);

    // theme
    await page.click('#themeBtn');
    await page.waitForTimeout(150);
    const theme = await page.getAttribute('html', 'data-theme');
    if (theme !== 'light') fail(`${tag} — theme toggle did not switch (${theme})`); else ok('theme toggles');

    // Mobile chrome geometry: a toast stretched between top and bottom, or a
    // primary action hidden under the fixed tab bar, are both cascade bugs
    // that only show up at this width.
    if (vp === 'mobile') {
      await page.locator('[data-go="tune"]:visible').first().click();
      await page.waitForTimeout(150);
      const geo = await page.evaluate(() => {
        const t = document.getElementById('toast');
        t.textContent = 'measuring the toast'; t.classList.add('show');
        const tr = t.getBoundingClientRect();
        const go = document.getElementById('go').getBoundingClientRect();
        const tabs = document.querySelector('.mobtabs').getBoundingClientRect();
        t.classList.remove('show');
        return { toastH: tr.height, goBottom: go.bottom, tabsTop: tabs.top, vh: innerHeight };
      });
      if (geo.toastH > 120) fail(`${tag} — toast is ${geo.toastH.toFixed(0)}px tall (stretched)`);
      else ok(`toast sized correctly (${geo.toastH.toFixed(0)}px)`);
      if (geo.goBottom > geo.tabsTop + 1) fail(`${tag} — CTA bottom ${geo.goBottom.toFixed(0)} is under the tab bar at ${geo.tabsTop.toFixed(0)}`);
      else ok('primary action clears the tab bar');
    }

    // no horizontal overflow on mobile
    if (vp === 'mobile') {
      await page.locator('[data-go="route"]:visible').first().click();
      await page.waitForTimeout(200);
      const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (over > 2) fail(`${tag} — ${over}px horizontal overflow`); else ok('no horizontal overflow');
    }

    done();
    await ctx.close();
  }
  await browser.close();
}

server.close();
if (skipped.length) console.log(`\n! engines not verified here: ${skipped.join(', ')}`);
console.log(failures ? `\n✗ ${failures} failure(s)\n` : '\n✓ all smoke checks passed\n');
// CI must run the full matrix; a missing engine there is a failure.
if (skipped.length && process.env.CI) { console.log('CI requires every engine'); process.exit(1); }
process.exit(failures ? 1 : 0);
