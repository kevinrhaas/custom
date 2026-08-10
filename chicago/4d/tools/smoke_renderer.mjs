/**
 * Smoke test for the three.js walkthrough.
 *
 *   PW_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
 *     node tools/smoke_renderer.mjs
 *
 * Drives the real page in a real browser at 390x780 AND 1280x800 and fails on
 * any page error. Mobile is a release gate, not a nice-to-have.
 *
 * What it asserts, and why each one is here:
 *
 *   scene reaches ready ......... the boot chain actually completed
 *   canvas renders non-black .... WebGL produced an image, not a cleared buffer
 *   confidence toggle ........... the deliverable measurably changes the render
 *   pick -> citation ............ the visual claim and the citable claim connect
 *   pick -> liberties ........... and what we made up about THAT building
 *   walk moves the camera ....... input intent reaches the walker
 *   liberties are readable ...... what we made up is in the panel, not only in the repo
 *   draw calls under budget ..... the batch strategy is doing its job
 *   zero page errors ............ everywhere, both widths
 *
 * On failure it prints the failing URL or text, never a bare status: a smoke
 * result you have to reproduce by hand has not saved you anything.
 */

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// Playwright is installed globally here, and ESM does not honour NODE_PATH, so
// resolve the global root and import by absolute path.
async function loadPlaywright() {
  let ns;
  try {
    ns = await import('playwright');
  } catch {
    const root = (process.env.NODE_PATH
      || execSync('npm root -g', { encoding: 'utf8' })).trim().split(path.delimiter)[0];
    ns = await import(path.join(root, 'playwright', 'index.js'));
  }
  // playwright is CommonJS; imported as ESM its exports land under .default
  return ns.chromium ? ns : ns.default;
}
const { chromium } = await loadPlaywright();

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.SMOKE_ROOT || path.resolve(HERE, '..');
const PORT = Number(process.env.SMOKE_PORT || 4187);
const YEAR = process.env.SMOKE_YEAR || '1835';
const KEEP = process.env.SMOKE_SHOTS || '';

const TYPES = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.glb': 'model/gltf-binary',
  '.bin': 'application/octet-stream', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.md': 'text/markdown',
};

const failures = [];
const passes = [];
function check(name, cond, detail = '') {
  if (cond) { passes.push(name); console.log(`  pass  ${name}`); }
  else { failures.push(name); console.log(`  FAIL  ${name}${detail ? ` — ${detail}` : ''}`); }
}

const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  let file = path.join(ROOT, url);
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!file.startsWith(ROOT) || !fs.existsSync(file)) {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end(`not found: ${url}`);
    return;
  }
  res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

await new Promise((r) => server.listen(PORT, r));
const base = `http://127.0.0.1:${PORT}/renderers/web/index.html?year=${YEAR}`;
console.log(`serving ${ROOT} on ${PORT}\n`);

const browser = await chromium.launch({
  executablePath: process.env.PW_EXECUTABLE || undefined,
  // SwiftShader is the only GPU here. Chromium finds it unaided, but say so
  // rather than leaving a headless run to chance.
  args: ['--enable-unsafe-swiftshader'],
});

/** How different are two pixel signatures, 0..255 per cell. */
function signatureDistance(a, b) {
  if (!a?.cells || !b?.cells || a.cells.length !== b.cells.length) return Infinity;
  let sum = 0;
  let worst = 0;
  for (let i = 0; i < a.cells.length; i++) {
    const d = Math.abs(a.cells[i] - b.cells[i]);
    sum += d;
    worst = Math.max(worst, d);
  }
  return { mean: sum / a.cells.length, worst };
}

for (const [label, viewport, touch] of [
  ['mobile 390x780', { width: 390, height: 780 }, true],
  ['desktop 1280x800', { width: 1280, height: 800 }, false],
]) {
  console.log(`${label}:`);
  const ctx = await browser.newContext({
    viewport,
    hasTouch: touch,
    isMobile: false,          // isMobile forces mobile emulation Chromium-side
    deviceScaleFactor: touch ? 2 : 1,
  });
  const page = await ctx.newPage();

  const errors = [];
  page.on('pageerror', (e) => errors.push(`pageerror: ${e.message || e}`));
  page.on('response', (r) => {
    if (r.status() >= 400) errors.push(`HTTP ${r.status()} ${r.url()}`);
  });
  page.on('requestfailed', (r) => {
    const why = r.failure()?.errorText || '';
    if (!/ERR_ABORTED/.test(why)) errors.push(`request failed (${why}) ${r.url()}`);
  });
  page.on('console', (m) => {
    const t = m.text();
    if (m.type() === 'error' && !t.startsWith('Failed to load resource')) {
      errors.push(`console.error: ${t}`);
    }
  });

  const res = await page.goto(base, { waitUntil: 'domcontentloaded' });
  check(`${label}: page serves`, res.status() === 200, `status ${res.status()} at ${base}`);

  // --- boot ---------------------------------------------------------------
  let ready = false;
  try {
    await page.waitForFunction(() => window.__chicago4d?.ready === true, { timeout: 30000 });
    ready = true;
  } catch {
    const state = await page.evaluate(() => ({
      error: window.__chicago4d?.error ?? null,
      problems: window.__chicago4d?.problems ?? [],
    })).catch(() => ({}));
    check(`${label}: scene reaches ready`, false,
      `${state.error ?? 'timed out'} | ${(state.problems || []).slice(0, 3).join(' | ')}`);
  }
  if (ready) check(`${label}: scene reaches ready`, true);

  if (ready) {
    const problems = await page.evaluate(() => window.__chicago4d.problems);
    // Provisional placement and placeholder-asset notes are expected findings,
    // not defects. Anything else in this list is a real integration problem.
    const hard = problems.filter((p) => !/provisional|PLACEHOLDER|placeholder/i.test(p));
    check(`${label}: no unexpected loader problems`, hard.length === 0, hard.slice(0, 3).join(' | '));

    const structures = await page.evaluate(() => window.__chicago4d.registry.size);
    check(`${label}: scene has structures`, structures > 0, `${structures} loaded`);

    // --- the scene actually draws ----------------------------------------
    await page.evaluate(() => window.__chicago4d.frame('sauganash_hotel', 26));
    await page.waitForTimeout(250);

    const off = await page.evaluate(() => window.__chicago4d.capture());
    check(`${label}: canvas renders non-black`,
      off.mean > 12 && off.litFraction > 0.5,
      `mean luminance ${off.mean?.toFixed(1)}, lit ${(off.litFraction * 100).toFixed(0)}%`);
    check(`${label}: drawing buffer matches the viewport`,
      off.width >= viewport.width && off.height >= viewport.height * 0.8,
      `${off.width}x${off.height} for a ${viewport.width}x${viewport.height} viewport`);

    // --- the confidence view ---------------------------------------------
    const modeBefore = await page.evaluate(() => window.__chicago4d.confidenceView);
    await page.evaluate(() => window.__chicago4d.setConfidenceView(true));
    const on = await page.evaluate(() => window.__chicago4d.capture());
    const modeAfter = await page.evaluate(() => window.__chicago4d.confidenceView);
    const d = signatureDistance(off, on);
    check(`${label}: confidence toggle flips state`, modeBefore === false && modeAfter === true,
      `before ${modeBefore}, after ${modeAfter}`);
    check(`${label}: confidence view changes the render`,
      d.worst >= 6 && d.mean >= 0.6,
      `cell delta mean ${d.mean?.toFixed(2)}, worst ${d.worst} (need worst>=6)`);

    await page.evaluate(() => window.__chicago4d.setConfidenceView(false));
    const back = await page.evaluate(() => window.__chicago4d.capture());
    const dBack = signatureDistance(off, back);
    check(`${label}: turning it off restores the render`, dBack.worst <= 3,
      `residual worst-cell delta ${dBack.worst}`);

    // --- pick -> provenance ----------------------------------------------
    const picked = await page.evaluate(() => {
      const hit = window.__chicago4d.pick('sauganash_hotel');
      const popup = document.getElementById('popup');
      return {
        ok: !!hit,
        visible: popup && !popup.hasAttribute('hidden'),
        text: popup?.textContent ?? '',
      };
    });
    check(`${label}: pick('sauganash_hotel') opens the popup`, picked.ok && picked.visible,
      `hit ${picked.ok}, visible ${picked.visible}`);
    check(`${label}: popup carries a real citation`,
      /Wau-Bun/.test(picked.text) && /Kinzie, Juliette/.test(picked.text),
      `popup text did not contain the Wau-Bun citation: ${picked.text.slice(0, 160)}`);
    check(`${label}: popup shows per-attribute confidence`,
      /documented/.test(picked.text) && /conjectural/.test(picked.text),
      picked.text.slice(0, 160));
    check(`${label}: popup links the research dossier`,
      /docs\/RESEARCH\/sauganash_hotel\.md/.test(picked.text), picked.text.slice(-200));

    // --- the liberties for THIS building, on the card ----------------------
    // The confidence chips answer "how sure are you of this value". They cannot
    // answer "what did you decide without evidence at all", which is what the
    // liberties record. Asserted per-building rather than as a count, because
    // the failure this guards against is the card showing all eighteen (or the
    // wrong four) instead of the ones the markdown attaches to this structure.
    const popLib = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const sec = document.querySelector('#popup .pop-liberties');
        return {
          present: !!sec,
          ids: [...document.querySelectorAll('#popup .pop-liberties .lib-id')]
            .map((n) => n.textContent.trim()),
          text: sec?.textContent ?? '',
        };
      };
      return { sauganash: read('sauganash_hotel'), greenTree: read('green_tree_tavern') };
    });
    check(`${label}: the popup carries the liberties taken with this building`,
      popLib.sauganash.present
      && ['L4', 'L4a', 'L5', 'L6'].every((id) => popLib.sauganash.ids.includes(id)),
      `got [${popLib.sauganash.ids.join(', ')}]`);
    check(`${label}: it shows the reasoning, not just the admission`,
      /invented/i.test(popLib.sauganash.text) && /Why/i.test(popLib.sauganash.text),
      popLib.sauganash.text.slice(0, 200));
    // The discriminating case: a different building, a different set. A popup
    // that dumped the whole list would pass every assertion above.
    check(`${label}: another building gets its own liberties, not the whole list`,
      popLib.greenTree.ids.includes('L9')
      && !popLib.greenTree.ids.some((id) => ['L4', 'L5', 'L6', 'L1'].includes(id)),
      `green tree got [${popLib.greenTree.ids.join(', ')}]`);
    check(`${label}: a scene-wide liberty is not attached to a building`,
      !popLib.sauganash.ids.includes('L1') && !popLib.sauganash.ids.includes('L14'),
      `sauganash got [${popLib.sauganash.ids.join(', ')}]`);

    // Collapsed by default here too — the card must stay skimmable, and a
    // building with four liberties would otherwise push the citations off it.
    const popLibOpen = await page.evaluate(() => {
      window.__chicago4d.pick('sauganash_hotel');
      const first = document.querySelector('#popup .pop-liberties details.lib');
      const body = first.querySelector('.lib-body');
      const before = body.checkVisibility();
      first.open = true;
      return { before, after: body.checkVisibility() };
    });
    check(`${label}: popup liberties start collapsed and open on demand`,
      popLibOpen.before === false && popLibOpen.after === true,
      `${popLibOpen.before} -> ${popLibOpen.after}`);

    await page.evaluate(() => window.__chicago4d.pick('sauganash_hotel'));

    // --- a raycast pick down the crosshair, not just by id ----------------
    const rayPick = await page.evaluate(() => {
      const hit = window.__chicago4d.pick();
      return hit ? hit.id : null;
    });
    check(`${label}: raycast down the crosshair resolves a structure_id`,
      rayPick === 'sauganash_hotel', `got ${rayPick}`);

    await page.evaluate(() => window.__chicago4d.popup.close());

    // --- walking ----------------------------------------------------------
    const before = await page.evaluate(() => ({ ...window.__chicago4d.player }));
    // Software rasterisation runs this scene at a handful of frames a second,
    // so give the walk a wall-clock window that survives it.
    await page.keyboard.down('KeyW');
    await page.waitForTimeout(2200);
    await page.keyboard.up('KeyW');
    const after = await page.evaluate(() => ({ ...window.__chicago4d.player }));
    const moved = Math.hypot(after.e - before.e, after.n - before.n);
    check(`${label}: walk intent moves the camera`, moved > 0.3,
      `moved ${moved.toFixed(2)} m in 2.2 s (backend `
      + `${await page.evaluate(() => window.__chicago4d.controlBackend)})`);

    // --- you cannot stand inside a building --------------------------------
    const pushed = await page.evaluate(() => {
      const a = window.__chicago4d;
      const fp = a.footprints.find((f) => f.id === 'sauganash_hotel');
      if (!fp) return { skipped: true };
      const cx = fp.pts.reduce((s, p) => s + p[0], 0) / fp.pts.length;
      const cn = fp.pts.reduce((s, p) => s + p[1], 0) / fp.pts.length;
      a.walker.teleport({ local_e: cx, local_n: cn });
      a.step();
      const { e, n } = a.player;
      // ray-cast point-in-polygon, same test the walker uses
      let hit = false;
      const pts = fp.pts;
      for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        const [xi, yi] = pts[i];
        const [xj, yj] = pts[j];
        if ((yi > n) !== (yj > n) && e < ((xj - xi) * (n - yi)) / (yj - yi) + xi) hit = !hit;
      }
      return { inside: hit, e, n, cx, cn };
    });
    check(`${label}: the walker is pushed out of a building footprint`,
      pushed.skipped || pushed.inside === false,
      `dropped at (${pushed.cx}, ${pushed.cn}), ended at (${pushed.e?.toFixed(2)}, ${pushed.n?.toFixed(2)})`);
    await page.evaluate(() => window.__chicago4d.frame('sauganash_hotel', 26));

    // --- the touch backend, on the mobile pass only ------------------------
    if (touch) {
      const stick = await page.evaluate(async () => {
        const api = window.__chicago4d;
        const c = document.getElementById('view');
        const r = c.getBoundingClientRect();
        const send = (type, x, y, id = 7) => c.dispatchEvent(new PointerEvent(type, {
          pointerId: id, pointerType: 'touch', isPrimary: true, bubbles: true, cancelable: true,
          clientX: r.left + x, clientY: r.top + y,
        }));
        // Left half: push the thumbstick forward.
        send('pointerdown', r.width * 0.25, r.height * 0.75);
        await new Promise((res) => requestAnimationFrame(res));
        send('pointermove', r.width * 0.25, r.height * 0.75 - 60);
        await new Promise((res) => setTimeout(res, 60));
        const forward = api.intent.forward;
        const backend = api.controlBackend;
        send('pointerup', r.width * 0.25, r.height * 0.75 - 60);
        return { forward, backend, stickVisible: !!document.getElementById('stick')?.classList.contains('on') };
      });
      check(`${label}: touch activates the touch backend`, stick.backend === 'touch', stick.backend);
      check(`${label}: thumbstick writes forward intent`, stick.forward > 0.5,
        `intent.forward = ${stick.forward}`);

      // Right-half drag must turn the view and nothing else.
      const look = await page.evaluate(async () => {
        const api = window.__chicago4d;
        const c = document.getElementById('view');
        const r = c.getBoundingClientRect();
        const b0 = api.player.bearingDeg;
        const send = (type, x, y, id = 9) => c.dispatchEvent(new PointerEvent(type, {
          pointerId: id, pointerType: 'touch', isPrimary: true, bubbles: true, cancelable: true,
          clientX: r.left + x, clientY: r.top + y,
        }));
        send('pointerdown', r.width * 0.75, r.height * 0.4);
        for (let i = 1; i <= 6; i++) {
          send('pointermove', r.width * 0.75 - i * 12, r.height * 0.4);
          await new Promise((res) => requestAnimationFrame(res));
        }
        send('pointerup', r.width * 0.75 - 72, r.height * 0.4);
        await new Promise((res) => setTimeout(res, 80));
        return { turned: Math.abs(((api.player.bearingDeg - b0 + 540) % 360) - 180) };
      });
      check(`${label}: right-half drag turns the view`, look.turned > 1,
        `turned ${(180 - look.turned).toFixed(1)}°`);
    }

    // --- budgets ------------------------------------------------------------
    const stats = await page.evaluate(() => window.__chicago4d.stats());
    check(`${label}: draw calls under budget`, stats.drawCalls <= stats.budget.drawCalls,
      `${stats.drawCalls} calls (budget ${stats.budget.drawCalls})`);
    check(`${label}: triangles under budget`, stats.triangles <= stats.budget.triangles,
      `${stats.triangles} tris (budget ${stats.budget.triangles})`);
    console.log(`        ${stats.drawCalls} draw calls · ${stats.triangles} tris · `
      + `${stats.batches} batch(es) · ${stats.structures} structure(s) · `
      + `${(stats.bytes / 1024).toFixed(0)} KB of GLB · ${stats.fps} fps`);

    // --- the gate and the chrome -------------------------------------------
    await page.click('#gate-btn');
    await page.waitForTimeout(150);
    // Entering the walkthrough grabs the pointer on desktop; release it, or
    // every later click lands on the locked canvas instead of the HUD.
    await page.evaluate(() => document.exitPointerLock?.());
    await page.waitForTimeout(120);
    const chrome = await page.evaluate(() => ({
      gateHidden: document.getElementById('gate').hasAttribute('hidden'),
      hudShown: !document.getElementById('hud').hasAttribute('hidden'),
      overflow: document.documentElement.scrollWidth <= window.innerWidth + 1,
    }));
    check(`${label}: tap-to-start reveals the walkthrough`,
      chrome.gateHidden && chrome.hudShown,
      `gate hidden ${chrome.gateHidden}, hud shown ${chrome.hudShown}`);
    check(`${label}: no horizontal overflow`, chrome.overflow);

    // The HUD toggle must drive the same view the harness does.
    await page.click('#btn-confidence');
    await page.waitForTimeout(100);
    const viaHud = await page.evaluate(() => window.__chicago4d.confidenceView);
    check(`${label}: the HUD toggle drives the confidence view`, viaHud === true, `${viaHud}`);
    await page.click('#btn-confidence');

    // --- what's new ---------------------------------------------------------
    // The changelog is authored inside the app and mirrored out by publish.sh.
    // That import is the part worth guarding: it resolves differently in the
    // dev tree than in the published build if anyone reintroduces a fetch, and
    // this is the assertion that would catch it before it 404s live.
    await page.evaluate(() => window.localStorage.removeItem('chicago4d.whatsnew.seen'));
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => window.__chicago4d?.ready === true, null, { timeout: 30000 });
    await page.click('#gate-btn');
    await page.waitForTimeout(150);
    await page.evaluate(() => document.exitPointerLock?.());

    const unread = await page.evaluate(() => ({
      chip: !document.getElementById('help-dot')?.hasAttribute('hidden'),
      tab: !document.getElementById('whatsnew-dot')?.hasAttribute('hidden'),
    }));
    check(`${label}: a first-time visitor is told there are unread notes`,
      unread.chip && unread.tab, `chip ${unread.chip}, tab ${unread.tab}`);

    await page.click('#btn-help');
    await page.click('.panel-tab[data-tab="whatsnew"]');
    await page.waitForTimeout(120);
    const wn = await page.evaluate(() => {
      const host = document.getElementById('whatsnew');
      return {
        entries: host.querySelectorAll('.wn-entry').length,
        items: host.querySelectorAll('.wn-items li').length,
        newest: host.querySelector('.wn-title')?.textContent || '',
        dated: /CT$/.test(host.querySelector('.wn-meta')?.textContent || ''),
        cleared: document.getElementById('help-dot')?.hasAttribute('hidden'),
        seen: window.localStorage.getItem('chicago4d.whatsnew.seen'),
      };
    });
    check(`${label}: the what's-new tab renders every release`,
      wn.entries >= 5 && wn.items >= wn.entries,
      `${wn.entries} entries, ${wn.items} items`);
    check(`${label}: entries carry a title and a stamped date`,
      wn.newest.length > 4 && wn.dated, `"${wn.newest}", dated ${wn.dated}`);
    check(`${label}: opening the tab clears the unread marker`,
      wn.cleared && Number(wn.seen) > 0, `cleared ${wn.cleared}, seen ${wn.seen}`);
    check(`${label}: a first visit flags nothing (no "last time" to differ from)`,
      await page.evaluate(() => document.querySelectorAll('#whatsnew .wn-entry.is-new').length) === 0);

    // A RETURNING visitor is the case the marker exists for: pin `seen` one
    // release back and exactly the newer entries should carry it.
    await page.evaluate(() => window.localStorage.setItem('chicago4d.whatsnew.seen', '3'));
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => window.__chicago4d?.ready === true, null, { timeout: 30000 });
    await page.click('#gate-btn');
    await page.waitForTimeout(150);
    await page.evaluate(() => document.exitPointerLock?.());
    await page.click('#btn-help');
    await page.click('.panel-tab[data-tab="whatsnew"]');
    await page.waitForTimeout(120);
    const ret = await page.evaluate(() => ({
      flagged: [...document.querySelectorAll('#whatsnew .wn-entry.is-new .wn-title')]
        .map((n) => n.textContent),
      total: document.querySelectorAll('#whatsnew .wn-entry').length,
    }));
    check(`${label}: a returning visitor sees only what shipped since last time`,
      ret.flagged.length === ret.total - 3 && ret.flagged.length > 0,
      `${ret.flagged.length} of ${ret.total} flagged: ${ret.flagged.join(' | ')}`);
    // --- the liberties, in the Evidence panel ------------------------------
    // The claim this project makes is that a visitor can tell which parts we
    // made up. The confidence view covers attributes; these are the decisions
    // that belong to no attribute, and they are only a disclosure if they are
    // reachable from the page rather than from the repository.
    const lib = await page.evaluate(() => {
      // The what's-new checks above leave the panel open on their tab, and a
      // toggle here would close it — open only if it is shut.
      if (document.getElementById('panel').hasAttribute('hidden')) {
        document.getElementById('btn-help').click();
      }
      const tab = [...document.querySelectorAll('.panel-tab')]
        .find((t) => t.dataset.tab === 'evidence');
      tab?.click();
      const mount = document.getElementById('liberties');
      return {
        counted: window.__chicago4d.liberties?.count ?? 0,
        error: window.__chicago4d.liberties?.error ?? 'no liberties on the handle',
        rendered: mount ? mount.querySelectorAll('details.lib').length : 0,
        busy: mount ? mount.hasAttribute('aria-busy') : true,
        text: mount ? mount.textContent : '',
        overflow: document.documentElement.scrollWidth <= window.innerWidth + 1,
      };
    });
    check(`${label}: the liberties list loads`, lib.counted >= 17 && !lib.busy,
      `${lib.counted} loaded (${lib.error})`);
    check(`${label}: every loaded liberty is rendered`, lib.rendered === lib.counted,
      `${lib.rendered} rendered of ${lib.counted}`);
    check(`${label}: the list names a scene-wide liberty`,
      /No people, anywhere/.test(lib.text) && /L1\b/.test(lib.text),
      lib.text.slice(0, 160));
    check(`${label}: the Evidence panel does not overflow`, lib.overflow);

    // The admissions themselves, on the page. `Covers:` is what the commit gate
    // reads to decide whether every invented footprint has been owned up to, and
    // a guarantee enforced in the repository but invisible in the walkthrough is
    // the same filed confession this panel exists to stop being. Asserted
    // discriminatingly: the entry that admits to the Sauganash's two invented
    // outlines shows footprint chips, and the scene-wide "no people" entry —
    // which invents nothing that gets drawn — claims nothing.
    const claims = await page.evaluate(() => {
      const read = (id) => {
        const el = [...document.querySelectorAll('#liberties details.lib')]
          .find((d) => d.querySelector('.lib-id')?.textContent.trim() === id);
        return [...(el?.querySelectorAll('.lib-covers') ?? [])].map((n) => n.textContent.trim());
      };
      return { l5: read('L5'), l8: read('L8'), l1: read('L1'), l4: read('L4') };
    });
    check(`${label}: an entry shows the inventions it admits to`,
      claims.l5.length > 0 && claims.l5.every((t) => /footprint/.test(t))
      && claims.l5.some((t) => /Sauganash/i.test(t)),
      `L5 claims [${claims.l5.join(' | ')}]`);
    check(`${label}: a claim over several buildings names each of them`,
      claims.l8.length === 3 && new Set(claims.l8).size === 3,
      `L8 claims [${claims.l8.join(' | ')}]`);
    check(`${label}: an entry that invented nothing drawn claims nothing`,
      claims.l1.length === 0 && claims.l4.length === 0,
      `L1 [${claims.l1.join(' | ')}] L4 [${claims.l4.join(' | ')}]`);

    // Collapsed by default, and opening one gives the reasoning — not just the
    // admission that a liberty was taken.
    // A closed <details> still lays its contents out — measuring the body's own
    // box reads the same number open or shut. checkVisibility() is the signal
    // that answers the question actually being asked, and the list's height
    // confirms the panel really grew around it.
    const opened = await page.evaluate(() => {
      const mount = document.getElementById('liberties');
      const first = mount.querySelector('details.lib');
      const body = first.querySelector('.lib-body');
      const snap = () => ({
        shown: body.checkVisibility(),
        list: mount.getBoundingClientRect().height,
      });
      const before = snap();
      first.open = true;
      return { before, after: snap(), text: first.textContent };
    });
    check(`${label}: expanding a liberty reveals its reasoning`,
      opened.before.shown === false && opened.after.shown === true
      && opened.after.list > opened.before.list + 40 && /Why/i.test(opened.text),
      `shown ${opened.before.shown} -> ${opened.after.shown}, `
      + `list ${opened.before.list.toFixed(0)} -> ${opened.after.list.toFixed(0)} px`);
    await page.click('#panel-close');

    // --- free-fly -----------------------------------------------------------
    // Three properties worth pinning, all of which would rot silently:
    // the aerial anchor arrives IN the air, the terrain is still a floor, and
    // landing puts you back on the ground rather than stranding the eye.
    const aerial = await page.evaluate(async () => {
      const a = window.__chicago4d;
      a.goTo('from_above');
      await new Promise((r) => setTimeout(r, 400));
      return { alt: a.player.altitude, flying: a.player.flying, pitch: a.player.pitchDeg };
    });
    check(`${label}: the aerial anchor arrives in the air, looking down`,
      aerial.flying === true && aerial.alt > 100 && aerial.pitch < -10,
      `flying ${aerial.flying}, ${aerial.alt?.toFixed(0)} m up, pitch ${aerial.pitch?.toFixed(0)}`);

    const aboveShot = await page.evaluate(() => window.__chicago4d.capture());
    check(`${label}: the view from above renders`,
      aboveShot.mean > 12 && aboveShot.litFraction > 0.5,
      `mean luminance ${aboveShot.mean?.toFixed(1)}`);

    // Terrain is a floor even in free-fly. Driven by pushing the eye under the
    // ground and stepping once, NOT by flying into it: tick() uses wall-clock
    // dt and this suite runs at a couple of frames a second under SwiftShader,
    // so a "hold forward and dive" test would cover four metres and prove
    // nothing. One frame against a violated invariant is the honest form.
    const floored = await page.evaluate(() => {
      const a = window.__chicago4d;
      a.walker.teleport({ local_e: 60, local_n: -200, yaw_deg: 0, altitude_m: 40, pitch_deg: -80 });
      a.walker.state.eyeY -= 200;             // straight through the world
      a.step();
      return { alt: a.player.altitude, flying: a.player.flying };
    });
    check(`${label}: free-fly cannot sink through the terrain`,
      floored.flying === true && floored.alt > 0.5 && floored.alt < 4,
      `${floored.alt?.toFixed(2)} m above ground`);

    // Landing snaps, so one frame settles it — see walker.setFlying() for why
    // the smoothed descent was rejected.
    const landed = await page.evaluate(() => {
      const a = window.__chicago4d;
      a.goTo('from_above');
      a.setFly(false);
      a.step();
      return { alt: a.player.altitude, flying: a.player.flying, y: a.player.y };
    });
    check(`${label}: leaving free-fly puts the visitor back on the ground`,
      landed.flying === false && Math.abs(landed.alt) < 0.2,
      `flying ${landed.flying}, ${landed.alt?.toFixed(2)} m off the ground`);

    // Space is mode-scoped: it ascends in the air and inspects on foot. If that
    // ever leaks, walking visitors levitate every time they try to inspect.
    await page.evaluate(() => {
      window.__chicago4d.goTo('sauganash');
      // Aim at the building, the same way the pick test does — Space inspects
      // down the crosshair, so a test that has not aimed is testing the prairie.
      window.__chicago4d.frame('sauganash_hotel', 26);
    });
    await page.evaluate(() => window.__chicago4d.popup.close());
    await page.keyboard.press('Space');
    await page.waitForTimeout(250);
    const spaceOnFoot = await page.evaluate(() => ({
      alt: window.__chicago4d.player.altitude,
      flying: window.__chicago4d.player.flying,
      inspected: !document.getElementById('popup').hasAttribute('hidden'),
    }));
    check(`${label}: Space inspects on foot instead of lifting off`,
      spaceOnFoot.flying === false && Math.abs(spaceOnFoot.alt) < 0.2 && spaceOnFoot.inspected,
      `flying ${spaceOnFoot.flying}, ${spaceOnFoot.alt?.toFixed(2)} m up, inspected ${spaceOnFoot.inspected}`);
    await page.evaluate(() => window.__chicago4d.popup.close());
    await page.evaluate(() => window.__chicago4d.frame('sauganash_hotel', 26));

    if (KEEP) {
      await page.screenshot({ path: path.join(KEEP, `walk-${viewport.width}x${viewport.height}.png`) });
    }
  }

  check(`${label}: zero page errors`, errors.length === 0,
    errors.slice(0, 4).join(' | '));
  await ctx.close();
  console.log('');
}

// The vendored meshopt decoder must be a working module, because the published
// web derivatives will need it and a broken vendor file would only surface then.
{
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  const meshopt = await page.evaluate(async () => {
    const m = await import('./vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js');
    await m.MeshoptDecoder.ready;
    return { supported: m.MeshoptDecoder.supported, decode: typeof m.MeshoptDecoder.decodeGltfBuffer };
  }).catch((e) => ({ error: String(e) }));
  check('vendor: meshopt decoder loads and reports supported',
    meshopt.supported === true && meshopt.decode === 'function',
    JSON.stringify(meshopt));
  check('vendor: meshopt import raises no page error', errors.length === 0, errors.join(' | '));
  await ctx.close();
}

await browser.close();
server.close();

console.log(`\n${passes.length} passed, ${failures.length} failed`);
if (failures.length) {
  console.log(`FAILURES:\n - ${failures.join('\n - ')}`);
  process.exit(1);
}
console.log('SMOKE PASS');
