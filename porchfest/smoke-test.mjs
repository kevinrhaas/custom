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
  '.json': 'application/json', '.svg': 'image/svg+xml',
  // Band photos are local files now, so they have to be served as images —
  // octet-stream would leave every card showing its fallback initials.
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };

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

// The app must make zero network requests; band photos are the one deliberate
// exception and are allowed to fail (offline / hotlink).
const PHOTO = /porchfest-band-photos|drive\.google/;

function watch(page, label) {
  const errs = [];
  page.on('pageerror', e => errs.push(`pageerror: ${e.message}`));
  page.on('console', m => {
    if (m.type() !== 'error') return;
    // A failing image reports through BOTH requestfailed and console, so the
    // photo exception has to cover both channels — matched on the resource
    // URL, never on the message, so real console errors still fail the run.
    // (This only surfaced once a later test waited long enough for the lazy
    // photos to time out inside a watch window; before that the suite was
    // passing on timing rather than on being clean.)
    if (PHOTO.test((m.location() || {}).url || '')) return;
    errs.push(`console.error: ${m.text()}`);
  });
  page.on('requestfailed', r => {
    if (!PHOTO.test(r.url())) errs.push(`requestfailed: ${r.url()}`);
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
    // Band photos hotlink an S3 bucket this environment cannot reach, so they
    // HANG rather than fail. Re-rendering the 91-card grid re-issues all of
    // them, and enough pending sockets eventually take the renderer down mid
    // run. Failing them immediately is the same outcome the app is built for
    // (it degrades to initials) and keeps the suite deterministic.
    await ctx.route(/porchfest-band-photos|drive\.google/, r => r.abort());
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

    // ---- times must be real clock times ----
    // Arrival times are fractional (distance / pace). Rounding the minutes
    // apart from the hour let them carry to 60 without the hour following, so
    // the app printed "2:60 PM". It hit ~0.8% of times, which is exactly rare
    // enough for a single sampled plan to miss — so sweep the formatter
    // directly rather than trusting whatever the current route happens to be.
    const clockSweep = await page.evaluate(() => {
      const bad = [];
      for (let m = 0; m < 1440; m += 0.05) {
        const s = hhmm(m);
        const mt = s.match(/^(\d{1,2}):(\d{2}) (AM|PM)$/);
        if (!mt) { if (bad.length < 5) bad.push(`${m.toFixed(2)} -> "${s}" (unparsable)`); continue; }
        const hh = +mt[1], mm = +mt[2];
        if (hh < 1 || hh > 12 || mm > 59) if (bad.length < 5) bad.push(`${m.toFixed(2)} -> "${s}"`);
      }
      return bad;
    });
    if (clockSweep.length) fail(`${tag} — impossible times from hhmm: ${clockSweep.join(', ')}`);
    else ok('every minute of the day formats as a real clock time');

    // And nothing rendered on screen may be an impossible time either.
    const badRendered = await page.evaluate(() => {
      const out = [];
      for (const m of document.body.innerText.matchAll(/\b(\d{1,2}):(\d{2})\s*(AM|PM)\b/g)) {
        if (+m[1] < 1 || +m[1] > 12 || +m[2] > 59) out.push(m[0]);
      }
      return [...new Set(out)];
    });
    if (badRendered.length) fail(`${tag} — impossible time on screen: ${badRendered.join(', ')}`);
    else ok('no impossible time rendered');

    // every stop must sit inside that band's advertised set window
    const outside = await page.evaluate(() => {
      // Rejects an impossible minute rather than quietly accepting it — this
      // parser tolerating "2:60" is why the window check never caught it.
      const to24 = (s) => {
        const m = s.match(/(\d+):(\d+)\s*(AM|PM)/);
        if (!m || +m[2] > 59 || +m[1] < 1 || +m[1] > 12) throw new Error(`bad time "${s}"`);
        return ((+m[1] % 12) + (m[3] === 'PM' ? 12 : 0)) * 60 + +m[2];
      };
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
      const to24 = (s) => {
        const m = s.match(/(\d+):(\d+) (AM|PM)/);
        if (!m || +m[2] > 59 || +m[1] < 1 || +m[1] > 12) throw new Error(`bad time "${s}"`);
        return ((+m[1] % 12) + (m[3] === 'PM' ? 12 : 0)) * 60 + +m[2];
      };
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

    // ---- the notable-act star ----
    // Ask for big names so the route is guaranteed to contain starred acts.
    await setPop(2);
    if (vp === 'mobile') await page.locator('[data-go="route"]:visible').first().click();
    await page.waitForTimeout(400);
    const starred = await page.evaluate(() => {
      const D = JSON.parse(document.getElementById('payload').textContent);
      const by = new Map(D.bands.map(b => [b.n, b.dw]));
      return [...document.querySelectorAll('#stops .stop')].map(s => {
        const h3 = s.querySelector('h3');
        const btn = h3.querySelector('.tierdot');
        return {
          name: h3.childNodes[0].textContent.trim(),
          mark: btn ? btn.textContent.trim() : '',
          big: btn ? btn.classList.contains('big') : false,
          dw: by.get(h3.childNodes[0].textContent.trim()),
        };
      });
    });
    // Tier must be carried by SHAPE, not hue alone — two orange shades at 10px
    // are indistinguishable, and identical under red-green colour blindness.
    const wrongMark = starred.filter(s => typeof s.dw === 'number' &&
      s.mark !== (s.dw >= 60 ? '★★' : s.dw >= 42 ? '★' : ''));
    if (wrongMark.length)
      fail(`${tag} — wrong star for ${wrongMark.map(s => `${s.name}(${s.dw})="${s.mark}"`).join(', ')}`);
    else ok(`star shape matches tier (${starred.filter(s => s.mark).length} starred in route)`);
    if (!starred.some(s => s.mark)) fail(`${tag} — "big names" route contains no starred act to test`);

    // Tapping it must explain itself — the tooltip it replaces never showed on
    // a phone, which is how this went unexplained in the first place.
    const starIdx = starred.findIndex(s => s.mark);
    if (starIdx >= 0) {
      const viewBeforeStar = await page.evaluate(() => document.body.dataset.view);
      await page.locator('#stops .stop .tierdot').first().click();
      await page.waitForTimeout(300);
      const t = await page.evaluate(() => {
        const el = document.getElementById('toast');
        const r = el.getBoundingClientRect();
        return { shown: el.classList.contains('show'), text: el.textContent,
                 h: r.height, right: r.right, left: r.left, vw: innerWidth };
      });
      if (!t.shown || !/Big draw|Known name/.test(t.text))
        fail(`${tag} — tapping the star showed "${t.text}" (shown=${t.shown})`);
      else ok(`tapping the star explains it ("${t.text}")`);
      if (t.h > 120 || t.left < 0 || t.right > t.vw + 1)
        fail(`${tag} — star toast is ${t.h.toFixed(0)}px tall, ${t.left.toFixed(0)}-${t.right.toFixed(0)} in ${t.vw}px`);
      else ok('star toast fits the screen');
      // It must not also fire the row's own actions.
      const viewAfterStar = await page.evaluate(() => document.body.dataset.view);
      if (viewAfterStar !== viewBeforeStar)
        fail(`${tag} — tapping the star navigated to ${viewAfterStar}`);
      else ok('tapping the star does not trigger the row');
    }

    // Worst case: the longest explanation any band can produce must still fit.
    const worst = await page.evaluate(() => {
      const D = JSON.parse(document.getElementById('payload').textContent);
      const MARK = { big: '★★', known: '★' }, LABEL = { big: 'Big draw', known: 'Known name' };
      let longest = '';
      for (const b of D.bands) {
        const tier = b.dw >= 60 ? 'big' : b.dw >= 42 ? 'known' : '';
        if (!tier) continue;
        const why = (b.wy || []).slice(0, 2).join(', ');
        const msg = `${MARK[tier]} ${LABEL[tier]}${why ? ' — ' + why : ''}`;
        if (msg.length > longest.length) longest = msg;
      }
      const el = document.getElementById('toast');
      el.textContent = longest; el.classList.add('show');
      const r = el.getBoundingClientRect();
      el.classList.remove('show');
      return { longest, h: r.height, left: r.left, right: r.right, vw: innerWidth };
    });
    if (worst.h > 120 || worst.left < 0 || worst.right > worst.vw + 1)
      fail(`${tag} — longest star toast "${worst.longest}" is ${worst.h.toFixed(0)}px tall / overflows`);
    else ok(`longest star toast fits (${worst.h.toFixed(0)}px)`);
    await setPop(0);

    // ---- shuffle ----
    // It has to produce a DIFFERENT afternoon. The search is randomised but
    // the objective is not, so restarts all converge on one optimum — the
    // button re-derived the same winner and looked broken. It now penalises
    // repeating the current route, so this checks variety AND that the
    // variety does not cost too much match quality.
    if (vp === 'mobile') await page.locator('[data-go="tune"]:visible').first().click();
    await page.waitForTimeout(250);
    await page.evaluate(() => [...document.querySelectorAll('[data-preset]')]
      .find(b => b.dataset.preset === 'Loud & fast').click());
    await page.waitForTimeout(1800);
    const routeNow = () => page.evaluate(() => ({
      names: [...document.querySelectorAll('#stops .stop h3')].map(h => h.childNodes[0].textContent.trim()),
      fit: +document.getElementById('sFit').textContent.replace('%', ''),
    }));
    const first = await routeNow();
    const seenRoutes = new Set([first.names.join('|')]);
    let worstFit = first.fit, everChanged = 0;
    for (let i = 0; i < 4; i++) {
      const before = await routeNow();
      // Shuffling jumps to the schedule on mobile, which hides the button that
      // lives in the plan pane — so come back before pressing it again.
      if (vp === 'mobile') {
        await page.locator('[data-go="tune"]:visible').first().click();
        await page.waitForTimeout(250);
      }
      await page.locator('#go').click();
      await page.waitForTimeout(1500);
      const afterShuffle = await routeNow();
      seenRoutes.add(afterShuffle.names.join('|'));
      worstFit = Math.min(worstFit, afterShuffle.fit);
      everChanged += afterShuffle.names.filter(n => !before.names.includes(n)).length;
    }
    if (seenRoutes.size < 3)
      fail(`${tag} — 4 shuffles produced only ${seenRoutes.size} distinct route(s)`);
    else ok(`shuffle varies the route (${seenRoutes.size} distinct across 5)`);
    if (!everChanged) fail(`${tag} — shuffle never swapped a single band`);
    // Variety is worthless if it hands you a bad afternoon.
    if (first.fit - worstFit > 15)
      fail(`${tag} — shuffle cost ${first.fit - worstFit} match points (${first.fit}% -> ${worstFit}%)`);
    else ok(`shuffle keeps quality (${first.fit}% -> worst ${worstFit}%)`);
    await page.evaluate(() => [...document.querySelectorAll('[data-preset]')]
      .find(b => b.dataset.preset === '__clear').click());
    await page.waitForTimeout(1600);

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

    // ---- genre filters in the browser ----
    const shown = () => page.locator('#bgrid .card').count();
    const chipN = await page.locator('#bgenres .chip').count();
    if (chipN < 20) fail(`${tag} — only ${chipN} genre filter chips`); else ok(`${chipN} genre filters`);

    // A chip must narrow to exactly the bands carrying that tag.
    const punkExpected = await page.evaluate(() =>
      JSON.parse(document.getElementById('payload').textContent).bands.filter(b => b.tg.includes('punk')).length);
    await page.locator('[data-bf="punk"]').click();
    await page.waitForTimeout(300);
    const punkShown = await shown();
    if (punkShown !== punkExpected) fail(`${tag} — punk filter showed ${punkShown}, expected ${punkExpected}`);
    else ok(`genre filter narrows (punk -> ${punkShown})`);

    // Two genres must be a union, not an intersection: picking punk and folk
    // should widen the view, not demand a band that is somehow both.
    await page.locator('[data-bf="folk"]').click();
    await page.waitForTimeout(300);
    const bothShown = await shown();
    const unionExpected = await page.evaluate(() =>
      JSON.parse(document.getElementById('payload').textContent).bands
        .filter(b => b.tg.includes('punk') || b.tg.includes('folk')).length);
    if (bothShown !== unionExpected)
      fail(`${tag} — punk+folk showed ${bothShown}, expected the union ${unionExpected}`);
    else ok(`two genres union rather than intersect (${bothShown})`);

    // Filters and the search box must compose.
    await page.fill('#bq', 'women');
    await page.waitForTimeout(300);
    const composed = await shown();
    if (composed >= bothShown) fail(`${tag} — search did not narrow the filtered set (${composed})`);
    else ok(`filters compose with search (${composed})`);

    // An impossible combination explains itself instead of showing a blank grid.
    await page.fill('#bq', 'zzzznope');
    await page.waitForTimeout(300);
    const emptyMsg = await page.locator('#bgrid .empty').count();
    if (!emptyMsg) fail(`${tag} — no empty state when nothing matches`);
    else ok('empty state when nothing matches');

    await page.fill('#bq', '');
    await page.locator('#bfClear').click();
    await page.waitForTimeout(300);
    const cleared = await shown();
    if (cleared !== 91) fail(`${tag} — clearing filters left ${cleared} of 91`);
    else ok('clearing filters restores all 91');

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

    // ---- desktop panel layout ----
    if (vp === 'desktop') {
      // The bands view hides .wrap entirely, so get back to the panels first
      // or every measurement below is taken against a display:none element.
      await page.locator('[data-go="tune"]:visible').first().click();
      await page.waitForTimeout(300);
      const cols = () => page.evaluate(() =>
        getComputedStyle(document.querySelector('.wrap')).gridTemplateColumns
          .split(' ').map(v => Math.round(parseFloat(v))));

      // Nothing in the map's header may sit under the zoom cluster.
      const clash = await page.evaluate(() => {
        const a = document.querySelector('#resetLayout')?.getBoundingClientRect();
        const b = document.querySelector('.mapctl')?.getBoundingClientRect();
        if (!a || !b) return 'missing';
        return (a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom)
          ? `reset ${a.left.toFixed(0)}-${a.right.toFixed(0)} vs zoom ${b.left.toFixed(0)}-${b.right.toFixed(0)}` : '';
      });
      if (clash) fail(`${tag} — map header overlaps the zoom controls: ${clash}`);
      else ok('map header clears the zoom controls');

      // Dragging a divider must actually resize, and persist.
      const before = await cols();
      const g = await page.locator('.gutter').first().boundingBox();
      await page.mouse.move(g.x + g.width / 2, g.y + 200);
      await page.mouse.down();
      await page.mouse.move(g.x + g.width / 2 + 120, g.y + 200, { steps: 10 });
      await page.mouse.up();
      await page.waitForTimeout(400);
      const after = await cols();
      if (after[0] <= before[0]) fail(`${tag} — dragging the divider did not widen: ${before[0]} -> ${after[0]}`);
      else ok(`divider resizes the panel (${before[0]}px -> ${after[0]}px)`);

      // A FRESH PAGE rather than a reload. It shares localStorage, so this
      // still proves boot restores the stored width — and it proves it on a
      // renderer that has not just been through 250 automated operations.
      // (Reloading this page crashed headless WebKit at the tail of a full
      // run; the heap is flat across the same work, so that is the harness
      // wearing out, not a leak. Chromium never does it.)
      const fresh = await ctx.newPage();
      const doneFresh = watch(fresh, `${tag}/fresh`);
      await fresh.goto(at('/app/'), { waitUntil: 'domcontentloaded' });
      await fresh.waitForFunction(() => document.querySelectorAll('#stops .stop').length > 0,
        null, { timeout: 25000 }).catch(() => {});
      await fresh.waitForTimeout(300);
      const restored = await fresh.evaluate(() =>
        getComputedStyle(document.querySelector('.wrap')).gridTemplateColumns
          .split(' ').map(v => Math.round(parseFloat(v))));
      if (restored[0] !== after[0]) fail(`${tag} — panel width did not persist: ${after[0]} -> ${restored[0]}`);
      else ok(`panel width persists into a new session (${restored[0]}px)`);
      doneFresh();
      await fresh.close();

      // Collapse to zero, then the divider brings it back.
      await page.locator('[data-collapse="tune"]').click();
      await page.waitForTimeout(400);
      const collapsed = await cols();
      if (collapsed[0] !== 0) fail(`${tag} — collapse left the panel at ${collapsed[0]}px`);
      else ok('a panel collapses to nothing');
      const stillThere = await page.locator('.gutter').first().isVisible();
      if (!stillThere) fail(`${tag} — the divider vanished with the collapsed panel, no way back`);
      else ok('the divider survives so the panel can be recovered');
      await page.locator('.gutter').first().click();
      await page.waitForTimeout(400);
      const back = await cols();
      if (back[0] === 0) fail(`${tag} — clicking the divider did not restore the panel`);
      else ok(`clicking the divider restores it (${back[0]}px)`);

      // Reset puts it back to the shipped defaults.
      await page.locator('#resetLayout').click();
      await page.waitForTimeout(400);
      const reset = await cols();
      if (reset[0] !== 344 || reset[2] !== 400)
        fail(`${tag} — reset gave ${reset[0]}/${reset[2]}, expected 344/400`);
      else ok('reset restores the default layout');

      // Panels must never push the page sideways at any width.
      for (const w of [1100, 1280, 1512, 1920]) {
        await page.setViewportSize({ width: w, height: 900 });
        await page.waitForTimeout(250);
        const over = await page.evaluate(() =>
          document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (over > 0) fail(`${tag} — ${over}px horizontal overflow at ${w}px wide`);
      }
      ok('no horizontal overflow at any desktop width');
      await page.setViewportSize(size);
      await page.waitForTimeout(250);
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
