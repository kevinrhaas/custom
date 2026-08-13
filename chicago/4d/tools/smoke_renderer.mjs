/**
 * Smoke test for the three.js walkthrough.
 *
 *   PW_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
 *     node tools/smoke_renderer.mjs
 *
 * Drives the real page in a real browser at 390x780 AND 1280x800 and fails on
 * any page error. Mobile is a release gate, not a nice-to-have.
 *
 * `SMOKE_VIEWPORT=mobile` (or `desktop`) runs one of the two while iterating.
 * That is not the gate and the run says so on its first line.
 *
 * What it asserts, and why each one is here:
 *
 *   scene reaches ready ......... the boot chain actually completed
 *   canvas renders non-black .... WebGL produced an image, not a cleared buffer
 *   confidence toggle ........... the deliverable measurably changes the render
 *   pick -> citation ............ the visual claim and the citable claim connect
 *   citation -> its document .... why a modern page is on the rung it is on, and
 *                                 what the source itself says it cannot supply
 *   pick -> liberties ........... and what we made up about THAT building
 *   the bridge floats ........... a water-anchored structure is placed on the
 *                                 water plane, not on the river bed under it
 *   walk moves the camera ....... input intent reaches the walker
 *   one terrain surface ......... walker, structures and flora share the rendered land
 *   streets drape + identify .... earth tracks share the heightfield and dated names
 *   navigation aids ............. compass, moving overview marker, settings toggles
 *   complete jump search ........ every viewpoint, verified junction and loaded
 *                                 structure, in one Go to tab, each structure
 *                                 graded with its own record's position grade
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

const launchBrowser = () => chromium.launch({
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

// The gate is both viewports and nothing less. SMOKE_VIEWPORT exists because a
// full pass takes upwards of ten minutes on a software renderer and an agent
// iterating on one half should not have to spend the other half to see it — it
// says so out loud when it is used, so a filtered run cannot be mistaken for the
// gate in a log somebody reads later.
const ONLY = process.env.SMOKE_VIEWPORT || '';
if (ONLY) console.log(`NOT THE FULL GATE — viewports filtered to "${ONLY}"\n`);

for (const [label, viewport, touch] of [
  ['mobile 390x780', { width: 390, height: 780 }, true],
  ['desktop 1280x800', { width: 1280, height: 800 }, false],
].filter(([label]) => !ONLY || label.includes(ONLY))) {
  console.log(`${label}:`);
  // Give each release viewport a fresh renderer process. Reusing one process
  // makes a software-only run measure the previous viewport's accumulated GPU
  // state and can starve the second walk test down to a single frame.
  const browser = await launchBrowser();
  const ctx = await browser.newContext({
    viewport,
    hasTouch: touch,
    isMobile: false,          // isMobile forces mobile emulation Chromium-side
    deviceScaleFactor: touch ? 2 : 1,
  });
  const page = await ctx.newPage();
  // Playwright's default 30 s action timeout is not an assertion, and on this
  // scene it had quietly become one. A click waits for the element to be stable
  // across animation frames and then hit-tests it, and every one of those steps
  // queues behind the render loop — which on a software renderer drawing 533 000
  // triangles takes 0.5–1.1 s per frame (measured, both viewports). So opening
  // the menu was timing out on a button that `elementFromPoint` returned as the
  // topmost element at its own centre, with no pointer lock, the page visible
  // and focused: nothing was wrong with the page and everything was wrong with
  // the budget. The desktop half of the gate had stopped running entirely
  // because of it. Ninety seconds is room for a slow machine, not permission
  // for a broken control: a click that never lands still fails, three times
  // slower.
  page.setDefaultTimeout(90_000);

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
    // not defects. `review_required` is also a deliberate release blocker, but
    // pin its exact records before excluding it so a new blocker cannot hide in
    // the general integration-problem list.
    const reviews = problems.filter((p) => /review_required is set/.test(p));
    const expectedReviews = await page.evaluate(() => [...window.__chicago4d.registry.values()]
      .filter((r) => r.sidecar?.review_required)
      .map((r) => r.sidecar.id)
      .sort());
    const reportedReviews = reviews.map((p) => p.split(':', 1)[0]).sort();
    check(`${label}: the scene declares its exact consultation blockers`,
      expectedReviews.length > 0
      && JSON.stringify(reportedReviews) === JSON.stringify(expectedReviews),
      `reported ${JSON.stringify(reportedReviews)}, expected ${JSON.stringify(expectedReviews)}`);
    const hard = problems.filter((p) => !/provisional|PLACEHOLDER|placeholder|review_required is set/i.test(p));
    check(`${label}: no unexpected loader problems`, hard.length === 0, hard.slice(0, 3).join(' | '));

    const structures = await page.evaluate(() => window.__chicago4d.registry.size);
    check(`${label}: scene has structures`, structures > 0, `${structures} loaded`);

    // --- water anchoring (docs/GLB-CONTRACT.md) ---------------------------
    // A bridge's local y = 0 is the design water surface, not the ground, so
    // the renderer must NOT sample the heightfield for it. Mid-channel the
    // ground surface is the river BED, so a regression here sinks the bridge
    // out of sight and reads as a missing asset. The assertion is written as
    // the DIFFERENCE between the two anchors rather than "y === 0", because
    // over dry land the two agree and a test that passed there would prove
    // nothing.
    //
    // The bed is sampled at the deck's MIDPOINT, not at the placement origin.
    // That origin is the polygon's (0, 0) — for this bridge the west end, which
    // by construction sits exactly on the traced waterline where the ground
    // surface crosses zero. Sampling there compares zero against zero and the
    // check passes whatever the renderer does. Found by this assertion failing
    // on its first run, which is the argument for writing it as a difference.
    const anchored = await page.evaluate(() => {
      const api = window.__chicago4d;
      const rec = api.registry.get('north_branch_bridge');
      const p = rec?.sidecar?.placement;
      const poly = rec?.sidecar?.footprint?.polygon;
      if (!p || !poly?.length) return { missing: true };
      const world = api.buildings.positionOf('north_branch_bridge');
      // Footprint bbox centre, rotated by the facade bearing exactly as
      // walker.js's footprintsFrom does, then offset to world ENU.
      const us = poly.map(([u]) => u);
      const vs = poly.map(([, v]) => v);
      const u = (Math.min(...us) + Math.max(...us)) / 2;
      const v = (Math.min(...vs) + Math.max(...vs)) / 2;
      const th = (p.rotation_deg ?? 0) * Math.PI / 180;
      const midE = (p.local_e ?? 0) + u * Math.cos(th) + v * Math.sin(th);
      const midN = (p.local_n ?? 0) - u * Math.sin(th) + v * Math.cos(th);
      return {
        anchor: p.vertical_anchor,
        y: world ? world.y : null,
        // The real channel bed, and what the terrain anchor would have
        // returned here — which is NOT the bed: height() reports a wading
        // barrier over water, so the regression this catches lifts the bridge
        // metres into the air rather than sinking it.
        bed: api.terrain.groundHeight(midE, midN),
        terrainAnchor: api.terrain.height(midE, midN),
      };
    });
    check(`${label}: the bridge declares a water anchor`,
      anchored.anchor === 'water', `${anchored.anchor ?? 'record missing'}`);
    check(`${label}: the bridge sits on the water plane, not on the terrain`,
      anchored.y !== null && Math.abs(anchored.y) < 0.01
      && anchored.bed < -0.5 && Math.abs(anchored.terrainAnchor - anchored.y) > 1,
      `placed y ${anchored.y?.toFixed(2)}, bed ${anchored.bed?.toFixed(2)} m, `
      + `terrain anchor would give ${anchored.terrainAnchor?.toFixed(2)} m`);

    // --- the scene actually draws ----------------------------------------
    await page.evaluate(() => window.__chicago4d.frame('sauganash_hotel', 26));
    await page.waitForTimeout(250);

    // Hold the visual clock across the three captures below. They ask what the
    // confidence view does to a frame, and the wind blows between them: without
    // the hold the residual is mostly swaying grass, which made the restore
    // check fail about two runs in three. Holding removes the variable rather
    // than widening the tolerance around it, and it makes the "changes the
    // render" assertion strictly harder, since sway can no longer supply any of
    // the difference it needs to find.
    await page.evaluate(() => window.__chicago4d.setAnimationHold(true));
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
    await page.evaluate(() => window.__chicago4d.setAnimationHold(false));
    // With the clock held these are two captures of one unchanged scene, so the
    // restored frame should be the SAME frame. The residual left is readback
    // noise, not weather; a confidence tint left enabled changes the mean
    // broadly (the assertion immediately above pins that at >= 0.6).
    check(`${label}: turning it off restores the render`,
      dBack.mean <= 0.1 && dBack.worst <= 3,
      `residual mean ${dBack.mean?.toFixed(2)}, worst-cell delta ${dBack.worst}`);

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

    // --- and what KIND of source each citation is ---------------------------
    // The card has printed a bare `tier 4` beside a citation since it was
    // written, at a visitor with no table to look it up in, while the panel
    // around it argues that a person can judge the evidence for themselves. The
    // words come off `data/source.schema.json` through the compiled sidecar.
    // Asserted as a pair on ONE card, each label matched to its own citation: the
    // Sauganash cites a period survey, a near-primary recollection and a modern
    // retrospective, so a card stamping one rung on every line — or the right
    // words on the wrong citation — fails where a presence check would pass.
    // `.cites > li` and not `.cites li`: a citation's stated limits are a nested
    // list, and counting their items as citations is how this assertion first
    // reported a card with no rung on it.
    const rungs = await page.evaluate(() => {
      window.__chicago4d.pick('sauganash_hotel');
      return [...document.querySelectorAll('#popup .cites > li')].map((li) => ({
        cite: li.querySelector('.cite-text')?.textContent.trim() ?? '',
        tier: li.querySelector('.tier')?.textContent.trim() ?? '',
      }));
    });
    const rungOf = (re) => rungs.find((r) => re.test(r.cite))?.tier ?? '(no such citation)';
    check(`${label}: every citation says what rung it is on`,
      rungs.length > 0 && rungs.every((r) => /^tier \d+ · \S/.test(r.tier)),
      JSON.stringify(rungs.map((r) => r.tier)));
    check(`${label}: the rung belongs to its own citation`,
      /^tier 2 · near-primary recollection$/.test(rungOf(/Wau-Bun/))
      && /^tier 1 · period\/eyewitness$/.test(rungOf(/Wright/))
      && /^tier 5 · modern retrospective/.test(rungOf(/Kurz/)),
      `Wau-Bun "${rungOf(/Wau-Bun/)}" · Wright "${rungOf(/Wright/)}" · Kurz "${rungOf(/Kurz/)}"`);
    // --- and WHY a citation is on that rung, and what it cannot be used for --
    // A rung is a judgement about a document, and on ten of these records the
    // document is not the page: a visitor following `chicagology_prefire273`
    // arrived at a modern blog stamped "tier 2 · near-primary recollection"
    // with nothing saying it reprints the Chicago Magazine of 15 May 1857. The
    // Sauganash's card carries the discriminating triple, which is why it is
    // asserted here rather than by presence: one citation that reprints a
    // document, one that IS one and reprints nothing (Wright's survey sheet,
    // which instead states what it does not supply), and one that has neither.
    // A card stamping the line on every citation fails on the second; a card
    // showing none fails on the first.
    const evidence = await page.evaluate(() => {
      window.__chicago4d.pick('sauganash_hotel');
      return [...document.querySelectorAll('#popup .cites > li')].map((li) => ({
        cite: li.querySelector('.cite-text')?.textContent.trim() ?? '',
        reprints: [...li.querySelectorAll('.cite-reprints')].map((p) => p.textContent.trim()),
        limits: [...li.querySelectorAll('.cite-lim li')].map((x) => x.textContent.trim()),
      }));
    });
    const ev = (re) => evidence.find((r) => re.test(r.cite)) ?? { reprints: [], limits: [] };
    check(`${label}: a citation says what document it reprints`,
      ev(/Chicagology/).reprints.length === 1
      && /reprints\s+Chicago Magazine/.test(ev(/Chicagology/).reprints[0])
      && /1857-05-15/.test(ev(/Chicagology/).reprints[0]),
      JSON.stringify(ev(/Chicagology/).reprints));
    check(`${label}: a source that IS its document reprints nothing`,
      ev(/Wright/).reprints.length === 0 && ev(/Wau-Bun/).reprints.length === 0,
      `Wright ${JSON.stringify(ev(/Wright/).reprints)} · `
      + `Wau-Bun ${JSON.stringify(ev(/Wau-Bun/).reprints)}`);
    // The limit that reached this project's own brief before anyone opened the
    // scan, and then stayed in the repository: a survey of streets and blocks
    // does not give you a building.
    check(`${label}: a source states what it does not supply`,
      ev(/Wright/).limits.includes('building footprints')
      && ev(/Wau-Bun/).limits.length === 0,
      `Wright ${JSON.stringify(ev(/Wright/).limits)} · `
      + `Wau-Bun ${JSON.stringify(ev(/Wau-Bun/).limits)}`);
    check(`${label}: popup links the research dossier`,
      /docs\/RESEARCH\/sauganash_hotel\.md/.test(picked.text), picked.text.slice(-200));

    // --- what the chip cannot say: whether you are looking at it -----------
    // A confidence chip grades the evidence. It says nothing about whether the
    // value reached the mesh, and the two come apart in the worst direction — the
    // Wolf Point sign was `documented` on a building that had no sign until the
    // rename and re-bake of 2026-08-10 (LIBERTIES L20). Asserted
    // per-attribute rather than by presence, because a card that marked every row
    // — or the wrong rows — would pass a count.
    const geom = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const rows = {};
        for (const tr of document.querySelectorAll('#popup table.attrs tr')) {
          const mark = tr.querySelector('.geom');
          rows[tr.querySelector('th')?.textContent.trim() ?? '?'] =
            mark ? mark.textContent.trim() : null;
        }
        return rows;
      };
      return { western: read('western_hotel'), wolf: read('wolf_point_tavern'),
               greenTree: read('green_tree_tavern') };
    });
    check(`${label}: an attested feature the model omits says so on its row`,
      geom.western.stables === 'not built',
      `stables ${geom.western.stables}`);
    // The case this whole marker exists for, now from the other side. The Wolf
    // Point sign was `documented` on a building with no sign for a day, because
    // the record spelled it `signage` and the archetype reads `sign`. It is built
    // now, so its row must carry NO marker — an assertion that fails both if the
    // rename is reverted and if the marker is ever applied to a built attribute.
    check(`${label}: the documented wolf sign is built and its row is unmarked`,
      geom.wolf.sign === null && geom.wolf['frame addition'] === null,
      `sign ${geom.wolf.sign}, frame addition ${geom.wolf['frame addition']}`);
    check(`${label}: a value a fixed default stands in for is marked differently`,
      geom.western.cladding === 'not modelled from this',
      `cladding ${geom.western.cladding}`);
    // Chimneys were the other half of that marker until 2026-08-10: every record
    // counted its stacks and neither archetype read the number, so Miller's house
    // showed one stack over a record claiming two. The count is a parameter now, so
    // the row carries no marker — on the log building that gained a stack and on the
    // frame building whose pair was already right, which are different reasons to
    // pass and both have to hold.
    check(`${label}: the recorded chimney count is built, so its row is unmarked`,
      geom.wolf.chimneys === null && geom.western.chimneys === null,
      `wolf ${geom.wolf.chimneys}, western ${geom.western.chimneys}`);
    // The discriminating cases. An attribute the archetype builds must carry no
    // marker at all, or the card teaches a visitor to distrust the whole model;
    // and a rejected reading is not a thing missing from the view.
    check(`${label}: an attribute the generator builds carries no marker`,
      geom.western.stories === null && geom.western['roof type'] === null,
      `stories ${geom.western.stories}, roof type ${geom.western['roof type']}`);
    check(`${label}: a reading recorded but never a build instruction is not marked`,
      geom.greenTree['log core'] === null && geom.greenTree.side_additions === undefined
      && geom.greenTree['side additions'] === 'not built',
      `log core ${geom.greenTree['log core']}, side additions ${geom.greenTree['side additions']}`);

    // --- the liberties for THIS building, on the card ----------------------
    // The confidence chips answer "how sure are you of this value". They cannot
    // answer "what did you decide without evidence at all", which is what the
    // liberties record. Asserted per-building rather than as a count, because
    // the failure this guards against is the card showing the whole list (or the
    // wrong subset) instead of the ones the markdown attaches to this structure.
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
      && ['L4', 'L4a', 'L5', 'L6', 'L18'].every((id) => popLib.sauganash.ids.includes(id)),
      `got [${popLib.sauganash.ids.join(', ')}]`);
    check(`${label}: it shows the reasoning, not just the admission`,
      /invented/i.test(popLib.sauganash.text) && /Why/i.test(popLib.sauganash.text),
      popLib.sauganash.text.slice(0, 200));
    // The discriminating case: a different building, a different set. A popup
    // that dumped the whole list would pass every assertion above.
    check(`${label}: another building gets its own liberties, not the whole list`,
      popLib.greenTree.ids.includes('L9') && popLib.greenTree.ids.includes('L19')
      && !popLib.greenTree.ids.some((id) => ['L4', 'L5', 'L6', 'L1', 'L18'].includes(id)),
      `green tree got [${popLib.greenTree.ids.join(', ')}]`);
    check(`${label}: a scene-wide liberty is not attached to a building`,
      !popLib.sauganash.ids.includes('L1') && !popLib.sauganash.ids.includes('L14'),
      `sauganash got [${popLib.sauganash.ids.join(', ')}]`);

    // Collapsed by default here too — the card must stay skimmable, and a
    // building carrying several liberties would otherwise push the citations off it.
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

    // --- was it here at all? ----------------------------------------------
    // The claim the whole scene rests on, and the last one to reach the card.
    // `popup.js` read `documented_range` from the moment it was written and
    // `compile_scene.py` never emitted it, so the line rendered as nothing on
    // every building, silently, with every gate green — which is why the
    // assertion is written against the RENDERED card rather than the sidecar.
    //
    // Asserted per building and on the discriminating pair, because a card that
    // stamped one confidence on every presence claim would pass a check for
    // "there is a chip". The Sauganash's frame phase is `documented` — Wau-Bun
    // watched it go up and it burned on a recorded date in 1851. Hogan's store is
    // `inferred` and is the weakest presence claim in the dataset: attested to
    // about July 1834 and placed in a scene eleven months later on a continuity
    // argument. Those two must not read the same.
    const presence = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const sec = [...document.querySelectorAll('#popup .pop-sec')]
          .find((s) => /Was it here/i.test(s.querySelector('h3')?.textContent ?? ''));
        if (!sec) return null;
        const row = sec.querySelector('table.attrs tr');
        const note = row?.querySelector('[data-note]');
        return {
          span: row?.querySelector('.val')?.textContent.trim() ?? '',
          conf: row?.querySelector('.conf')?.textContent.trim() ?? '',
          account: sec.querySelector('.pop-account')?.textContent.trim() ?? '',
          noteText: note?.textContent.trim() ?? '',
          noteHidden: note ? note.hasAttribute('hidden') : null,
        };
      };
      return { hogan: read('hogan_store'), saug: read('sauganash_hotel') };
    });
    check(`${label}: the card says whether the building was here on the scene date`,
      presence.hogan?.span === '1831-03-31 → 1835-12-31',
      `span "${presence.hogan?.span}"`);
    check(`${label}: the presence claim is graded per building, not stamped`,
      presence.hogan?.conf === 'inferred' && presence.saug?.conf === 'documented',
      `hogan ${presence.hogan?.conf}, sauganash ${presence.saug?.conf}`);
    // The reasoning is the point: a span with a chip and no argument is what the
    // card already had everywhere else. Hogan's is the one that matters — the end
    // of that range is a continuity argument, not a source.
    check(`${label}: the presence claim carries its reasoning, folded away`,
      presence.hogan?.noteHidden === true
      && /NO SOURCE REACHED FOLLOWS THE BUILDING PAST IT/.test(presence.hogan?.noteText ?? ''),
      `hidden ${presence.hogan?.noteHidden}, note "${(presence.hogan?.noteText ?? '').slice(0, 120)}"`);
    // What no chip can express: this building held the post office for three
    // years and is not the post office on the day you are standing in.
    check(`${label}: the phase's own account of itself reaches the card`,
      /post office/i.test(presence.hogan?.account ?? '')
      && presence.saug?.account !== presence.hogan?.account,
      `account "${(presence.hogan?.account ?? '').slice(0, 120)}"`);

    // The position's argument, on the line that shows the position. Three of the
    // eight placements are derived from bank geometry because no corner survives;
    // the card showed the conclusion and hid the reasoning behind nothing.
    const posWhy = await page.evaluate(() => {
      window.__chicago4d.pick('walker_meeting_house');
      const meta = document.querySelector('#popup .pop-meta [data-note]');
      const btn = document.querySelector('#popup .pop-meta [data-toggle-note]');
      const before = meta?.hasAttribute('hidden');
      btn?.click();
      return { before, after: meta?.hasAttribute('hidden'), text: meta?.textContent ?? '' };
    });
    check(`${label}: the position's reasoning opens on demand`,
      posWhy.before === true && posWhy.after === false && posWhy.text.length > 200,
      `${posWhy.before} -> ${posWhy.after}, ${posWhy.text.length} chars`);

    // --- was it this shape? -----------------------------------------------
    // The footprint is the largest claim a visitor is standing in front of and
    // the card said nothing about it at all: `compile_scene.py` carried its
    // confidence and dropped its sources and its argument. Six of the eight
    // outlines here open with the word PLACEHOLDER and two are the opposite, and
    // none of that reached anybody.
    //
    // Asserted on the discriminating pair, as everywhere else on this card, and
    // the pair is the strongest one in the dataset: Hogan's store is the only
    // BUILDING footprint that is evidence — Andreas gives twenty by forty-five
    // feet twice — and the Sauganash's is the placeholder its own note calls the
    // central unresolved question of the record. A card stamping one grade on all
    // eight outlines would pass any check for "there is a chip".
    const shape = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const sec = [...document.querySelectorAll('#popup .pop-sec')]
          .find((s) => /Was it this shape/i.test(s.querySelector('h3')?.textContent ?? ''));
        const row = sec?.querySelector('table.attrs tr');
        return {
          present: !!sec,
          conf: row?.querySelector('.conf')?.textContent.trim() ?? '',
          shown: row?.querySelector('[data-note]')?.textContent ?? '',
          recorded: window.__chicago4d.registry.get(id)?.sidecar?.footprint?.note ?? '',
        };
      };
      const pair = { hogan: read('hogan_store'), saug: read('sauganash_hotel') };
      // Every building, because the omission below is a rule and not a property
      // of the two buildings the pair happens to name.
      let valued = [];
      for (const id of window.__chicago4d.registry.keys()) {
        window.__chicago4d.pick(id);
        if (document.querySelector('#popup .pop-shape .val')) valued.push(id);
      }
      return { ...pair, valued };
    });
    check(`${label}: the card says how much of the shape is evidence`,
      shape.hogan.present && shape.saug.present
      && shape.hogan.conf === 'documented' && shape.saug.conf === 'conjectural',
      `hogan ${shape.hogan.conf}, sauganash ${shape.saug.conf}`);
    check(`${label}: the footprint's reasoning is the record's, verbatim`,
      shape.saug.shown === shape.saug.recorded && shape.saug.recorded.length > 300
      && /PLACEHOLDER/.test(shape.saug.shown)
      && shape.hogan.shown === shape.hogan.recorded
      && shape.hogan.shown !== shape.saug.shown,
      `${shape.saug.shown.length} shown of ${shape.saug.recorded.length} recorded`);
    // A deliberate omission, pinned so that a later slice cannot fill it by
    // accident. The only printable value is the polygon and the only way to print
    // a polygon in a table is to reduce it — a bounding box over Miller's L-plan
    // would be a measurement the record does not make, on the card that exists to
    // admit inventions. The shape is already in front of the visitor at full size.
    check(`${label}: and prints no dimension it would have had to invent`,
      shape.valued.length === 0,
      shape.valued.length ? `value printed on ${shape.valued.join(', ')}` : 'no value cell on any building');

    // The mechanism, rather than a third instance of the same discovery. Both
    // `documented_range` and the footprint were graded in the sidecar and silent
    // on the card, and each was found by somebody reading a file. A claim that
    // carries a confidence and reaches no chip is exactly what a program can see:
    // count the graded claims in the record and count the chips on the claim
    // tables, for every building, and require them to agree. Scoped to the claim
    // tables and the location line — the liberties carry their own chips and are
    // not claims about a recorded value.
    const chipCover = await page.evaluate(() => {
      const out = [];
      for (const id of window.__chicago4d.registry.keys()) {
        const s = window.__chicago4d.registry.get(id)?.sidecar;
        if (!s) continue;
        window.__chicago4d.pick(id);
        let graded = Object.keys(s.attributes ?? {}).length;
        if (s.documented_range?.confidence) graded += 1;
        if (s.placement?.position_confidence) graded += 1;
        if (s.footprint?.confidence) graded += 1;
        const chips = document.querySelectorAll(
          '#popup .pop-meta .conf, #popup .pop-sec table.attrs .conf').length;
        out.push({ id, graded, chips });
      }
      return out;
    });
    const uncovered = chipCover.filter((r) => r.graded !== r.chips);
    check(`${label}: every graded claim in a record reaches the card as a chip`,
      chipCover.length >= 8 && uncovered.length === 0,
      uncovered.length
        ? uncovered.map((r) => `${r.id} ${r.graded} graded / ${r.chips} shown`).join('; ')
        : `${chipCover.length} building(s), ${chipCover.reduce((a, r) => a + r.graded, 0)} claims`);

    // Is the shape a bake from the record, or a stand-in?  The established
    // Sauganash asset must remain a real bake while the anonymous phase-one
    // roofs must say both that their mesh is provisional and that their
    // per-parcel placement is a recommended reconstruction.
    const placeholder = await page.evaluate(() => {
      window.__chicago4d.pick('sauganash_hotel');
      const realFlags = [...document.querySelectorAll('#popup .pop-flag')]
        .map((f) => f.textContent);
      window.__chicago4d.pick('recon_1835_south_d3_001');
      const recommendedFlags = [...document.querySelectorAll('#popup .pop-flag')]
        .map((f) => f.textContent);
      return {
        real: window.__chicago4d.registry.get('sauganash_hotel')?.assetIsPlaceholder,
        realFlag: realFlags.some((t) => /placeholder massing/i.test(t)),
        recommended: window.__chicago4d.registry.get('recon_1835_south_d3_001')
          ?.assetIsPlaceholder,
        placeholderFlag: recommendedFlags.some((t) => /placeholder massing/i.test(t)),
        // The dataset's word for these roofs is `inferred_anonymous` since the
        // merge of 2026-08-13; the card was still testing for `recommended` and
        // so rendered no flag at all. Same assertion, current vocabulary — the
        // flag must still be on the card, which is what this has always asked.
        reconstructionFlag: recommendedFlags.some((t) => /inferred reconstruction/i.test(t)),
      };
    });
    check(`${label}: established assets remain identified as real bakes`,
      placeholder.real === false && placeholder.realFlag === false,
      JSON.stringify(placeholder));
    check(`${label}: anonymous infill is visibly flagged as placeholder reconstruction`,
      placeholder.recommended === true && placeholder.placeholderFlag
      && placeholder.reconstructionFlag,
      JSON.stringify(placeholder));

    // --- the record's own account -----------------------------------------
    // `research_note` is on every record and in every compiled sidecar, and the
    // sidecar-contract gate reported it as compiled-and-never-read: an unshipped
    // claim rather than dead weight. It is the paragraph that says which of two
    // sources was believed, or that the likeliest reading of the evidence is that
    // the record models the wrong building. Nothing was broken — the field simply
    // had no surface — so unlike the two faults before it, this is asserted
    // against what a visitor reads for the first time here.
    //
    // The assertion that matters is VERBATIM, and it is deliberately an exact
    // string comparison against the sidecar rather than a substring match. A note
    // about the limit of the evidence is the last text on this card that should be
    // trimmed or summarised, and a renderer that showed a first sentence and an
    // ellipsis would pass every looser check written here.
    const account = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const sec = [...document.querySelectorAll('#popup .pop-sec')]
          .find((s) => /own account/i.test(s.querySelector('h3')?.textContent ?? ''));
        const body = sec?.querySelector('.research-body');
        return {
          present: !!sec,
          shown: body?.textContent ?? '',
          recorded: window.__chicago4d.registry.get(id)?.sidecar?.research_note ?? '',
        };
      };
      return { hogan: read('hogan_store'), saug: read('sauganash_hotel') };
    });
    check(`${label}: the record's own account reaches the card`,
      account.hogan.present && /THE BUILDING WHERE CHICAGO'S MAIL BEGAN/.test(account.hogan.shown),
      `present ${account.hogan.present}, "${account.hogan.shown.slice(0, 90)}"`);
    check(`${label}: it is the record's words, unabridged`,
      account.hogan.shown === account.hogan.recorded && account.hogan.recorded.length > 500,
      `${account.hogan.shown.length} chars shown of ${account.hogan.recorded.length} recorded`);
    // The discriminating case, as everywhere else on this card: a second building
    // gets its own account. A section rendering one fixed block of prose — or the
    // scene's, or the previous pick's — would pass both checks above.
    check(`${label}: another building gets its own account, not this one's`,
      account.saug.shown === account.saug.recorded
      && account.saug.shown !== account.hogan.shown
      && /MILESTONE 0 REFERENCE RECORD/.test(account.saug.shown),
      `sauganash "${account.saug.shown.slice(0, 90)}"`);

    // --- who was here -------------------------------------------------------
    // `data/residents/` draws nobody by design, so the ONLY place a visitor can
    // meet the town's people is this card. Before it existed the layer stopped at
    // the repo — the failure mode that looks identical, from the street, to the
    // work never having been done. The discriminating half is the third check: a
    // building the programme RAISED for a hypothesised household has to say so,
    // or the card reads as evidence that somebody lived here.
    const who = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const sec = [...document.querySelectorAll('#popup .pop-sec')]
          .find((x) => /who was here/i.test(x.querySelector('h3')?.textContent ?? ''));
        return {
          present: !!sec,
          text: sec?.textContent ?? '',
          grades: [...(sec?.querySelectorAll('.grade') ?? [])].map((g) => g.className),
          basis: sec?.querySelector('.res-basis')?.textContent ?? '',
          recorded: window.__chicago4d.registry.get(id)?.sidecar?.residents ?? [],
        };
      };
      return {
        brown: read('brown_boarding_house'),
        inferred: read('inf_cooperage_south'),
        none: read('log_jail'),
      };
    });
    check(`${label}: a building names the household the sources put in it`,
      who.brown.present && /Mrs Rufus Brown/.test(who.brown.text)
      && who.brown.grades.some((c) => c.includes('grade-documented')),
      `present ${who.brown.present}, grades ${who.brown.grades.join('|')}`);
    check(`${label}: a person's grade is shown, and it is not a confidence chip`,
      who.brown.grades.some((c) => c.includes('grade-derived'))
      && !who.brown.grades.some((c) => c.includes('conf-')),
      who.brown.grades.join('|'));
    check(`${label}: a building raised for an inferred household says so`,
      who.inferred.present
      && who.inferred.grades.every((c) => c.includes('grade-inferred'))
      && /BECAUSE OF THIS HOUSEHOLD/.test(who.inferred.basis),
      `basis "${who.inferred.basis.slice(0, 80)}"`);
    check(`${label}: a building with no household gets no section at all`,
      !who.none.present && who.none.recorded.length === 0,
      `present ${who.none.present}`);

    // Collapsed by default, for the same reason the liberties are: these run to
    // several hundred words, and on a phone the panel is 62vh — an open account
    // would push the citations off the card entirely.
    const accountOpen = await page.evaluate(() => {
      window.__chicago4d.pick('hogan_store');
      const d = document.querySelector('#popup .pop-research details.research');
      const body = d.querySelector('.research-body');
      const before = body.checkVisibility();
      d.open = true;
      return { before, after: body.checkVisibility() };
    });
    check(`${label}: the account starts collapsed and opens on demand`,
      accountOpen.before === false && accountOpen.after === true,
      `${accountOpen.before} -> ${accountOpen.after}`);

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

    // Walking used to ease the eye toward the sampled ground. On a bank that
    // put the camera below the visible mesh uphill and left it floating
    // downhill, even though both are driven by the same heightfield. Disturb
    // the eye deliberately, then traverse the resolved slope in both directions:
    // every update must restore exact standing clearance, not approach it.
    const terrainLock = await page.evaluate(() => {
      const a = window.__chicago4d;
      const run = (n, bearing) => {
        a.walker.teleport({ local_e: 140, local_n: n, yaw_deg: bearing });
        a.walker.state.eyeY += 0.9;
        let worst = 0;
        let minGround = Infinity;
        let maxGround = -Infinity;
        a.intent.forward = 1;
        for (let i = 0; i < 520; i++) {
          a.walker.update(0.05, a.intent);
          const s = a.walker.state;
          const ground = a.terrain.walkHeight(s.e, s.n);
          minGround = Math.min(minGround, ground);
          maxGround = Math.max(maxGround, ground);
          worst = Math.max(worst, Math.abs(s.eyeY - ground - a.walkBudget.eyeHeight));
        }
        a.intent.forward = 0;
        return { worst, relief: maxGround - minGround };
      };
      return { uphill: run(-20, 180), downhill: run(-58, 0) };
    });
    check(`${label}: walking stays exactly on the terrain through rises and falls`,
      terrainLock.uphill.worst < 1e-6 && terrainLock.downhill.worst < 1e-6
      && terrainLock.uphill.relief > 0.25 && terrainLock.downhill.relief > 0.25,
      JSON.stringify(terrainLock));

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
      controlHelpShown: !document.getElementById('control-help').hasAttribute('hidden'),
      desktopHelpShown: getComputedStyle(document.getElementById('control-help-desktop')).display !== 'none',
      touchHelpShown: getComputedStyle(document.getElementById('control-help-touch')).display !== 'none',
      overflow: document.documentElement.scrollWidth <= window.innerWidth + 1,
    }));
    check(`${label}: tap-to-start reveals the walkthrough`,
      chrome.gateHidden && chrome.hudShown,
      `gate hidden ${chrome.gateHidden}, hud shown ${chrome.hudShown}`);
    check(`${label}: first entry shows the navigation guide for the active input mode`,
      chrome.controlHelpShown
      && (touch ? chrome.touchHelpShown && !chrome.desktopHelpShown
        : chrome.desktopHelpShown && !chrome.touchHelpShown),
      JSON.stringify(chrome));
    check(`${label}: no horizontal overflow`, chrome.overflow);
    await page.click('#control-help-gotit');
    const controlHelpDismissed = await page.evaluate(() => ({
      hidden: document.getElementById('control-help').hasAttribute('hidden'),
      stored: localStorage.getItem('chicago4d.controlHelpDismissed'),
    }));
    check(`${label}: the navigation guide dismisses and remembers the choice`,
      controlHelpDismissed.hidden && controlHelpDismissed.stored === '1',
      JSON.stringify(controlHelpDismissed));

    // --- navigation --------------------------------------------------------
    // Both readouts are derived from the live walker.  The overview's signature
    // is sampled from its own 2D canvas before and after a teleport so this
    // checks the visible marker, not merely an object property updated beside it.
    const nav = await page.evaluate(() => {
      const api = window.__chicago4d;
      const mapCanvas = document.getElementById('overview-map-canvas');
      const signature = () => {
        const p = mapCanvas.getContext('2d').getImageData(0, 0, mapCanvas.width, mapCanvas.height).data;
        let hash = 2166136261;
        for (let i = 0; i < p.length; i += 37) hash = Math.imul(hash ^ p[i], 16777619) >>> 0;
        return hash;
      };
      api.walker.teleport({ local_e: 20, local_n: -40, yaw_deg: 90 });
      api.step();
      const first = signature();
      const east = {
        direction: document.getElementById('compass-direction')?.textContent,
        bearing: document.getElementById('compass-bearing')?.textContent,
        snapshot: api.navigation.snapshot(),
      };
      api.walker.teleport({ local_e: 180, local_n: 90, yaw_deg: 225 });
      api.step();
      return {
        compassShown: !document.getElementById('compass')?.hasAttribute('hidden'),
        mapShown: !document.getElementById('overview-map')?.hasAttribute('hidden'),
        mapCaption: document.querySelector('.overview-caption')?.textContent?.trim(),
        mapAria: document.getElementById('overview-map')?.getAttribute('aria-label'),
        speedLabel: document.getElementById('v-speed')?.textContent?.trim(),
        units: document.getElementById('s-units')?.value,
        mapSize: [mapCanvas.width, mapCanvas.height],
        east,
        first,
        second: signature(),
        moved: api.navigation.snapshot(),
      };
    });
    check(`${label}: compass shows the live heading`,
      nav.compassShown && nav.east.direction === 'E' && nav.east.bearing === '090°',
      `${nav.east.direction} ${nav.east.bearing}`);
    check(`${label}: overview map renders the whole heightfield`,
      nav.mapShown && nav.mapSize[0] >= 188 && nav.mapSize[1] >= 76
      && nav.east.snapshot.bounds.eMax - nav.east.snapshot.bounds.eMin > 1900
      && nav.mapCaption === 'map' && nav.units === 'imperial'
      && /feet|ft/.test(nav.mapAria ?? ''),
      `${nav.mapSize.join('x')}, caption ${nav.mapCaption}, aria ${nav.mapAria}, `
      + `E ${nav.east.snapshot.bounds.eMin}…${nav.east.snapshot.bounds.eMax}`);
    check(`${label}: walking speed is presented in miles per hour`,
      /^\d+(?:\.\d)? mph$/.test(nav.speedLabel ?? '') && !/m\/s/.test(nav.speedLabel ?? ''),
      `speed label ${nav.speedLabel}`);
    check(`${label}: overview marker follows position and bearing`,
      nav.first !== nav.second && Math.abs(nav.moved.e - 180) < 0.1
      && Math.abs(nav.moved.n - 90) < 0.1 && Math.abs(nav.moved.bearingDeg - 225) < 0.1,
      `canvas ${nav.first} -> ${nav.second}; ${JSON.stringify(nav.moved)}`);

    const streetLayer = await page.evaluate(() => {
      const a = window.__chicago4d;
      // Sample the dynamic flora from a known dry South Division viewpoint.
      // The preceding overview check deliberately teleports over the river;
      // after the deep-channel vegetation fix an empty sward there is correct.
      a.walker.teleport({ local_e: 107, local_n: -103, yaw_deg: 180 });
      a.step();
      let vertices = 0;
      let worstDrape = 0;
      let wetVertices = 0;
      a.streets.group.traverse((o) => {
        const pos = o.geometry?.getAttribute?.('position');
        if (!pos) return;
        vertices += pos.count;
        const step = Math.max(1, Math.floor(pos.count / 900));
        for (let i = 0; i < pos.count; i += step) {
          const e = pos.getX(i);
          const n = -pos.getZ(i);
          worstDrape = Math.max(worstDrape,
            Math.abs(pos.getY(i) - a.terrain.surfaceHeight(e, n) - 0.022));
          if (a.terrain.isWater(e, n)) wetVertices++;
        }
      });

      // The former far-field canopy was a solid horizontal mesh at plant-top
      // height. It looked like a second terrain layer, hid the bases of the
      // buildings and let the visitor walk underneath it. The actual flora is
      // instanced geometry whose matrices must begin on the same terrain
      // sampler the buildings and streets use (or at the water surface for
      // emergent plants). There must be no replacement canopy slab.
      const canopyPresent = !!a.flora.group.getObjectByName('flora-canopy');
      const waterY = a.terrain.heightfield?.meta?.water_surface_m ?? 0;
      let rootedPlants = 0;
      let worstPlantRoot = 0;
      let waterPlants = 0;
      let deepWaterPlants = 0;
      for (const name of ['flora-near', 'flora-mid', 'flora-forb', 'flora-rosette']) {
        const mesh = a.flora.group.getObjectByName(name);
        const matrix = mesh?.instanceMatrix?.array;
        if (!matrix) continue;
        for (let i = 0; i < mesh.count; i++) {
          const o = i * 16;
          const e = matrix[o + 12];
          const y = matrix[o + 13];
          const n = -matrix[o + 14];
          const expected = a.terrain.isWater(e, n)
            ? waterY : a.terrain.surfaceHeight(e, n);
          worstPlantRoot = Math.max(worstPlantRoot, Math.abs(y - expected));
          if (a.terrain.isWater(e, n)) {
            waterPlants++;
            if (a.flora.shoreDistance(e, n) > 8.01) deepWaterPlants++;
          }
          rootedPlants++;
        }
      }
      const treeStations = a.trees.group.userData.stations ?? [];
      const wetTreeStations = treeStations.filter(({ e, n }) => a.terrain.isWater(e, n));
      // ...and the stronger question the river mask does not answer. `isWater`
      // asks whether the heightfield is below SHORE_Y, 100 mm UNDER the water
      // plane, so a stem rooted in that band passes the mask and still renders
      // standing in the river. Every station carries the ground height the
      // renderer built it at; the water surface comes from the epoch record.
      const drownedTreeStations = treeStations.filter(({ e, n, y }) => (
        (typeof y === 'number' ? y : a.terrain.surfaceHeight(e, n)) < waterY
      ));
      const lowestTreeStation = treeStations.reduce(
        (lo, { e, n, y }) => Math.min(lo, typeof y === 'number' ? y : a.terrain.surfaceHeight(e, n)),
        Infinity,
      );

      let anchoredBuildings = 0;
      let worstBuildingAnchor = 0;
      let exchangeAnchor = null;
      for (const [id, record] of a.registry.entries()) {
        const p = record.sidecar?.placement;
        const at = a.buildings.positionOf(id);
        if (!p || !at) continue;
        const expected = p.vertical_anchor === 'water'
          ? waterY : a.terrain.surfaceHeight(p.local_e ?? 0, p.local_n ?? 0);
        const error = Math.abs(at.y - expected);
        worstBuildingAnchor = Math.max(worstBuildingAnchor, error);
        anchoredBuildings++;
        if (id === 'exchange_coffee_house') {
          exchangeAnchor = { y: at.y, expected, error };
        }
      }

      // Dry land has one value no matter which compatibility entry point an
      // older caller uses. The walk-specific sampler differs only over water,
      // where it deliberately supplies the navigation barrier.
      let worstDrySurfaceAlias = 0;
      for (const [e, n] of [[319.12, -90.66], [140, -35], [89.2, -110.4]]) {
        if (!a.terrain.isWater(e, n)) {
          worstDrySurfaceAlias = Math.max(worstDrySurfaceAlias,
            Math.abs(a.terrain.surfaceHeight(e, n) - a.terrain.walkHeight(e, n)));
        }
      }
      a.walker.teleport({ local_e: 452.5, local_n: -110.4, yaw_deg: 0 });
      a.step();
      const crossing = {
        state: a.navigation.streetState,
        historic: document.getElementById('street-historic')?.textContent,
        modern: document.getElementById('street-modern')?.textContent,
        shown: !document.getElementById('street-readout')?.hasAttribute('hidden'),
      };
      a.walker.teleport({ local_e: 89.2, local_n: -180, yaw_deg: 0 });
      a.step();
      const approaching = {
        state: a.navigation.streetState,
        historic: document.getElementById('street-historic')?.textContent,
        modern: document.getElementById('street-modern')?.textContent,
        ahead: document.getElementById('street-approach')?.textContent,
      };
      return {
        records: a.streets.records.length, vertices, worstDrape, wetVertices,
        canopyPresent, rootedPlants, worstPlantRoot, waterPlants, deepWaterPlants,
        treeStations: treeStations.length, wetTreeStations: wetTreeStations.length,
        drownedTreeStations: drownedTreeStations.length,
        lowestTreeStation, waterY,
        treeRejectedBelowWaterline: a.trees.stats?.rejectedBelowWaterline ?? null,
        anchoredBuildings, worstBuildingAnchor, exchangeAnchor, worstDrySurfaceAlias,
        clearsLake: a.streets.blocksGrowth(452.5, -110.4),
        keepsBlockGreen: !a.streets.blocksGrowth(510, -180),
        crossing, approaching,
      };
    });
    check(`${label}: earth streets are populated and draped on the rendered ground`,
      streetLayer.records >= 17 && streetLayer.vertices > 1000
      && streetLayer.worstDrape < 1e-5 && streetLayer.wetVertices === 0,
      `${streetLayer.records} streets, ${streetLayer.vertices} vertices, `
      + `drape ${streetLayer.worstDrape}, wet ${streetLayer.wetVertices}`);
    check(`${label}: no elevated flora sheet can masquerade as a second terrain layer`,
      streetLayer.canopyPresent === false,
      `flora-canopy present ${streetLayer.canopyPresent}`);
    check(`${label}: detailed flora roots share the terrain and water surfaces`,
      streetLayer.rootedPlants > 100 && streetLayer.worstPlantRoot < 1e-5,
      `${streetLayer.rootedPlants} roots, worst error ${streetLayer.worstPlantRoot}`);
    check(`${label}: emergent flora stays within eight metres of a riverbank`,
      streetLayer.deepWaterPlants === 0,
      `${streetLayer.waterPlants} water plants, ${streetLayer.deepWaterPlants} in deep water`);
    check(`${label}: woody vegetation never occupies the river mask`,
      streetLayer.treeStations > 10 && streetLayer.wetTreeStations === 0,
      `${streetLayer.treeStations} trees, ${streetLayer.wetTreeStations} wet stations`);
    // The owner photographed a row of gallery trees standing mid-channel while
    // the mask check above was green: the mask's SHORE_Y sits 100 mm below the
    // water plane, so a stem could root under the water and still pass. This
    // asks the question the picture asks — is any stem's foot below the water
    // surface — and it must never be relaxed into the mask test again.
    check(`${label}: no tree stands below the waterline`,
      streetLayer.treeStations > 10 && streetLayer.drownedTreeStations === 0,
      `${streetLayer.drownedTreeStations} of ${streetLayer.treeStations} stations below `
      + `z=${streetLayer.waterY}; lowest station ${streetLayer.lowestTreeStation?.toFixed?.(3)} m, `
      + `${streetLayer.treeRejectedBelowWaterline} candidates rejected at placement`);

    // The owner: "grass and flowers appear out of the ground as you walk towards
    // them". The lattice is rebuilt every `step` metres walked and the fade ramp
    // is evaluated per frame, so the ramp has to be inset from the lattice by at
    // least the step — otherwise a plant that was outside the lattice at one
    // rebuild is already well inside the ramp by the next and arrives at a real
    // fraction of its height in a single frame. Two checks: the geometry of the
    // rings, and then an actual walk, which is the one that would have caught it.
    const popIn = await page.evaluate(() => {
      const a = window.__chicago4d;
      const SETS = ['flora-near', 'flora-mid', 'flora-forb', 'flora-rosette'];
      const rings = a.flora.rings;
      const inset = Object.entries(rings.layers).map(([id, r]) => ({
        id,
        outer: r.lattice.outer - (r.fade[0] + rings.step),
        // Only the mid ring HAS an inner ramp; where there is none there is
        // nothing for a plant to grow across on its way past the walker.
        inner: r.fade[3] > 0 ? r.fade[2] - (r.lattice.inner + rings.step) : 0,
      }));

      a.walker.teleport({ local_e: 107, local_n: -103, yaw_deg: 180 });
      a.step();
      const snap = () => {
        const p = a.camera.position;
        const f = p.clone();
        a.camera.getWorldDirection(f);
        const fl = Math.hypot(f.x, f.z) || 1;
        const seen = new Map();
        for (const name of SETS) {
          const mesh = a.flora.group.getObjectByName(name);
          const m = mesh?.instanceMatrix?.array;
          if (!m) continue;
          for (let i = 0; i < mesh.count; i++) {
            const o = i * 16;
            const e = m[o + 12];
            const n = -m[o + 14];
            seen.set(`${name}|${e.toFixed(3)}|${n.toFixed(3)}`, { name, e, n });
          }
        }
        return { seen, e: p.x, n: -p.z, fe: f.x / fl, fn: -f.z / fl };
      };

      // Short paces, so the lattice is rebuilt several times inside the walk and
      // never by more than one pace beyond the step it is triggered on.
      const PACE = 0.15;
      const AHEAD = Math.cos(30 * Math.PI / 180);
      let prev = snap();
      let arrivals = 0;
      let worst = 0;
      let worstAt = null;
      for (let k = 0; k < 20; k++) {
        a.walker.teleport({ local_e: prev.e + prev.fe * PACE, local_n: prev.n + prev.fn * PACE });
        a.step();
        const now = snap();
        for (const [key, plant] of now.seen) {
          if (prev.seen.has(key)) continue;
          const d = Math.hypot(plant.e - now.e, plant.n - now.n) || 1e-6;
          // Only what is in front of the walker. A plant may also arrive across
          // the view-cone edge, which is 62 degrees wide against a frame that is
          // never more than 40 — off-screen, and not what the owner saw.
          if (((plant.e - now.e) * now.fe + (plant.n - now.n) * now.fn) / d < AHEAD) continue;
          const fade = a.flora.fadeAt(plant.name, d);
          arrivals++;
          if (fade > worst) { worst = fade; worstAt = { set: plant.name, d, fade }; }
        }
        prev = now;
      }
      return { inset, arrivals, worst, worstAt, pace: PACE, step: rings.step };
    });
    check(`${label}: every flora fade ring is inset inside its own lattice`,
      popIn.inset.length === 3
      && popIn.inset.every((r) => r.outer >= -1e-9 && r.inner >= -1e-9),
      popIn.inset.map((r) => `${r.id} outer +${r.outer.toFixed(2)} inner +${r.inner.toFixed(2)}`)
        .join(', ') + ` against a ${popIn.step} m rebuild step`);
    // The bound is one pace, not zero: the rebuild fires on the frame that
    // carries the walker past the step, so it can overshoot by however far that
    // one frame moved. 0.15 m of a 2.2 m near band is 7%.
    check(`${label}: a plant in front of the walker never arrives already grown`,
      popIn.arrivals >= 20 && popIn.worst <= 0.10,
      `${popIn.arrivals} arrivals over ${(20 * popIn.pace).toFixed(2)} m; worst height `
      + `${(popIn.worst * 100).toFixed(1)}% of full`
      + (popIn.worstAt ? ` (${popIn.worstAt.set} at ${popIn.worstAt.d.toFixed(2)} m)` : ''));
    check(`${label}: every structure, including Exchange Coffee House, shares the terrain surface`,
      streetLayer.anchoredBuildings > 20
      && streetLayer.worstBuildingAnchor < 1e-6
      && streetLayer.exchangeAnchor?.error < 1e-6
      && streetLayer.worstDrySurfaceAlias < 1e-6,
      `${streetLayer.anchoredBuildings} structures, worst ${streetLayer.worstBuildingAnchor}, `
      + `Exchange ${JSON.stringify(streetLayer.exchangeAnchor)}, `
      + `dry alias ${streetLayer.worstDrySurfaceAlias}`);
    check(`${label}: street clearing removes travel-track plants but preserves the block`,
      streetLayer.clearsLake && streetLayer.keepsBlockGreen, JSON.stringify(streetLayer));
    check(`${label}: the readout shows both 1835 and current names at an intersection`,
      streetLayer.crossing.shown
      && streetLayer.crossing.state?.mode === 'intersection'
      && /Lake Street/.test(streetLayer.crossing.historic)
      && /La Salle Street/.test(streetLayer.crossing.historic)
      && /W Lake Street/.test(streetLayer.crossing.modern)
      && /LaSalle/.test(streetLayer.crossing.modern),
      JSON.stringify(streetLayer.crossing));
    check(`${label}: the street readout announces the next cross street ahead`,
      streetLayer.approaching.state?.mode === 'on'
      && streetLayer.approaching.historic === 'Market Street'
      && /N Wacker Drive/.test(streetLayer.approaching.modern)
      && /Lake Street/.test(streetLayer.approaching.ahead)
      && /\d+ ft/.test(streetLayer.approaching.ahead)
      && !/\d+ m(?:\s|$)/.test(streetLayer.approaching.ahead),
      JSON.stringify(streetLayer.approaching));

    // The menu is built from the two runtime collections, not from a sampled
    // shortlist.  With an empty query every loaded structure and every compiled
    // control junction must have a button; a real search must narrow both kinds.
    await page.click('#btn-help');
    await page.click('.panel-tab[data-tab="settings"]');
    await page.click('#s-show-control-help');
    const reopenedGuide = await page.evaluate(() => ({
      shown: !document.getElementById('control-help').hasAttribute('hidden'),
      panelHidden: document.getElementById('panel').hasAttribute('hidden'),
    }));
    check(`${label}: Settings can reopen the dismissed navigation guide`,
      reopenedGuide.shown && reopenedGuide.panelHidden,
      JSON.stringify(reopenedGuide));
    await page.click('#control-help-close');
    await page.click('#btn-help');
    await page.click('.panel-tab[data-tab="settings"]');
    const unitChoice = await page.evaluate(async () => {
      const api = window.__chicago4d;
      const select = document.getElementById('s-units');
      const choose = (value) => {
        select.value = value;
        select.dispatchEvent(new Event('change', { bubbles: true }));
        api.walker.teleport({ local_e: 89.2, local_n: -180, yaw_deg: 0 });
        api.step();
        api.hud.setFly(true, { announce: false });
        api.hud.setAltitude(100);
        const result = {
          value: select.value,
          navigation: api.navigation.units,
          speed: document.getElementById('v-speed')?.textContent?.trim(),
          altitude: document.getElementById('badge-alt')?.textContent?.trim(),
          map: document.getElementById('overview-map')?.getAttribute('aria-label'),
          street: document.getElementById('street-approach')?.textContent?.trim(),
        };
        api.hud.setFly(false, { announce: false });
        return result;
      };
      const metric = choose('metric');
      const imperial = choose('imperial');
      const { formatDistance } = await import('/renderers/web/js/units.js');
      return {
        metric, imperial,
        mile: formatDistance(1609.344, 'imperial'),
        kilometre: formatDistance(1000, 'metric'),
        stored: JSON.parse(localStorage.getItem('chicago4d.settings') || '{}').units,
      };
    });
    check(`${label}: Settings switches every navigation measurement as one unit system`,
      unitChoice.metric.value === 'metric' && unitChoice.metric.navigation === 'metric'
      && /km\/h$/.test(unitChoice.metric.speed ?? '')
      && unitChoice.metric.altitude === '100 m up'
      && /\d+ m/.test(unitChoice.metric.map ?? '')
      && /\d+ m$/.test(unitChoice.metric.street ?? '')
      && unitChoice.imperial.value === 'imperial'
      && unitChoice.imperial.navigation === 'imperial'
      && /mph$/.test(unitChoice.imperial.speed ?? '')
      && unitChoice.imperial.altitude === '328 ft up'
      && /\d+ ft/.test(unitChoice.imperial.map ?? '')
      && /\d+ ft$/.test(unitChoice.imperial.street ?? '')
      && unitChoice.mile === '1.0 mi' && unitChoice.kilometre === '1.0 km'
      && unitChoice.stored === 'imperial',
      JSON.stringify(unitChoice));
    // --- the Go to tab ------------------------------------------------------
    //
    // Going somewhere is not a setting, and it used to be two settings: a
    // "Named viewpoints" row of chips with, underneath it, a search containing
    // the same ground and more of it. Both are now one list in one tab, second
    // after Controls. These assertions are what would notice the duplicate
    // coming back, or the tab quietly moving to the end of the strip where
    // nobody opens it.
    const tabStrip = await page.evaluate(() => {
      const bar = document.querySelector('.panel-tabs');
      const items = [...bar.querySelectorAll('.panel-tab')];
      return {
        order: items.map((el) => el.dataset.tab),
        // A strip that has silently become two rows tall is the failure mode
        // this panel has already had once, so measure rows rather than trust
        // white-space: nowrap to hold. The tabs only: the close button is
        // shorter than they are and `align-items: center` gives it an offsetTop
        // of its own, which is not a second row.
        rows: new Set(items.map((el) => Math.round(el.offsetTop))).size,
        overflow: Math.round(bar.scrollWidth - bar.clientWidth),
        // The tabs are allowed to shrink, so "one row, no overflow" can also be
        // reached by squeezing a label out past its own button. Count that too.
        squeezed: items.filter((el) => el.scrollWidth > el.clientWidth + 1)
          .map((el) => el.dataset.tab),
        strayViewpointList: document.querySelectorAll(
          '[data-panel="settings"] .anchor-btn, #anchors').length,
      };
    });
    check(`${label}: Go to is a tab of its own, immediately after Controls`,
      tabStrip.order.join(',') === 'controls,goto,settings,evidence,whatsnew',
      tabStrip.order.join(','));
    check(`${label}: five tabs still fit the panel on one row, unsqueezed`,
      tabStrip.rows === 1 && tabStrip.overflow <= 1 && !tabStrip.squeezed.length,
      `${tabStrip.rows} row(s), ${tabStrip.overflow}px of horizontal overflow, `
      + `squeezed [${tabStrip.squeezed.join(', ')}]`);
    check(`${label}: Settings no longer carries a second list of viewpoints`,
      tabStrip.strayViewpointList === 0, `${tabStrip.strayViewpointList} stray node(s)`);

    // G, from the walk, with the panel shut.
    await page.click('#panel-close');
    await page.keyboard.press('g');
    await page.waitForTimeout(60);
    const viaKey = await page.evaluate(() => ({
      open: !document.getElementById('panel').hasAttribute('hidden'),
      tab: document.querySelector('.panel-tab.is-on')?.dataset.tab,
      focused: document.activeElement?.id,
    }));
    check(`${label}: G opens the Go to tab`,
      viaKey.open && viaKey.tab === 'goto'
      // The search takes focus for a visitor who arrived by keyboard, and must
      // not on a phone: focusing it there raises the on-screen keyboard over
      // the list the tap was for.
      && (touch ? viaKey.focused !== 'jump-search' : viaKey.focused === 'jump-search'),
      JSON.stringify(viaKey));

    const jumps = await page.evaluate(() => {
      const input = document.getElementById('jump-search');
      const registry = window.__chicago4d.registry;
      const rows = [...document.querySelectorAll('#jump-results .jump-result')];
      // The chip on a result and the grade on the record it jumps to are the
      // same claim shown twice. Compare every one of them, the way the popup's
      // own confidence assertions do — a menu that graded a position more
      // kindly than the record does would be this project's worst kind of bug.
      const mismatched = [];
      let graded = 0;
      for (const row of rows) {
        if (row.dataset.jumpKind !== 'structure') continue;
        const want = registry.get(row.dataset.jumpId)?.sidecar?.placement?.position_confidence
          || 'conjectural';
        const chip = row.querySelector('.conf');
        const shown = chip?.textContent?.trim();
        if (shown === want && chip.classList.contains(`conf-${want}`)) graded++;
        else mismatched.push({ id: row.dataset.jumpId, want, shown: shown ?? null });
      }
      // And the colour has to carry the distinction, which is exactly what a
      // bare `.jump-result small` rule took away from it once: it outranks
      // `.conf-inferred` on specificity and painted all three grades the same
      // dim grey — a legend that lies, in a project whose whole product is the
      // grading.
      const colourOf = (grade) => {
        const chip = document.querySelector(`.jump-result .conf-${grade}`);
        return chip ? getComputedStyle(chip).color : null;
      };
      const all = {
        anchors: document.querySelectorAll('[data-jump-kind="anchor"]').length,
        structures: document.querySelectorAll('[data-jump-kind="structure"]').length,
        intersections: document.querySelectorAll('[data-jump-kind="intersection"]').length,
        loaded: registry.size,
        sceneAnchors: window.__chicago4d.scene?.anchors?.length ?? 0,
        chippedNonStructures: rows.filter((r) => r.dataset.jumpKind !== 'structure'
          && r.querySelector('.conf')).length,
      };
      const note = document.getElementById('jump-note')?.textContent ?? '';
      const tally = { documented: 0, inferred: 0, conjectural: 0 };
      for (const [, record] of registry) {
        const grade = record?.sidecar?.placement?.position_confidence || 'conjectural';
        if (grade in tally) tally[grade]++;
      }
      const colours = {
        inferred: colourOf('inferred'),
        conjectural: colourOf('conjectural'),
        plain: getComputedStyle(document.querySelector('.jump-result span')).color,
      };
      input.value = 'Randolph Canal';
      input.dispatchEvent(new Event('input', { bubbles: true }));
      const filtered = [...document.querySelectorAll('#jump-results .jump-result')]
        .map((b) => ({ id: b.dataset.jumpId, kind: b.dataset.jumpKind, text: b.textContent }));
      return { all, filtered, graded, mismatched, note, tally, colours };
    });
    check(`${label}: jump menu includes every loaded structure`,
      jumps.all.structures === jumps.all.loaded && jumps.all.loaded > 70,
      `${jumps.all.structures} listed of ${jumps.all.loaded} loaded`);
    check(`${label}: jump menu includes every verified intersection`,
      jumps.all.intersections === 4, `${jumps.all.intersections} listed`);
    check(`${label}: jump menu includes every viewpoint the scene names`,
      jumps.all.anchors === jumps.all.sceneAnchors && jumps.all.anchors > 3,
      `${jumps.all.anchors} listed of ${jumps.all.sceneAnchors} in the scene`);
    check(`${label}: every structure result carries its record's position grade`,
      jumps.graded === jumps.all.structures && !jumps.mismatched.length,
      `${jumps.graded} graded of ${jumps.all.structures}, `
      + `mismatched ${JSON.stringify(jumps.mismatched.slice(0, 3))}`);
    check(`${label}: a viewpoint and a survey junction are not graded like a building`,
      jumps.all.chippedNonStructures === 0,
      `${jumps.all.chippedNonStructures} non-structure result(s) carry a confidence chip`);
    check(`${label}: the grades are told apart by colour, not only by their words`,
      jumps.colours.inferred && jumps.colours.conjectural
      && jumps.colours.inferred !== jumps.colours.conjectural
      && jumps.colours.inferred !== jumps.colours.plain,
      JSON.stringify(jumps.colours));
    check(`${label}: the tab counts its own list rather than quoting a written total`,
      jumps.note.includes(`${jumps.all.structures} structures`)
      && jumps.note.includes(`${jumps.tally.documented} are `)
      && jumps.note.includes(`${jumps.tally.inferred} inferred`)
      && jumps.note.includes(`${jumps.tally.conjectural} conjectural`),
      `${jumps.note} / ${JSON.stringify(jumps.tally)}`);
    check(`${label}: jump search finds an intersection by both street names`,
      jumps.filtered.some((r) => r.id === 'randolph_canal' && r.kind === 'intersection'),
      JSON.stringify(jumps.filtered));
    await page.click('[data-jump-id="randolph_canal"]');
    await page.waitForTimeout(80);
    const arrived = await page.evaluate(() => ({ ...window.__chicago4d.player }));
    check(`${label}: an intersection result moves the visitor there`,
      Math.abs(arrived.e + 155.24) < 0.2 && Math.abs(arrived.n + 251.19) < 0.2,
      `arrived (${arrived.e?.toFixed(2)}, ${arrived.n?.toFixed(2)})`);

    await page.click('#btn-help');
    await page.click('.panel-tab[data-tab="settings"]');
    const toggles = await page.evaluate(() => {
      const compass = document.getElementById('s-compass');
      const map = document.getElementById('s-overview-map');
      const street = document.getElementById('s-street-names');
      compass.click(); map.click(); street.click();
      const hidden = {
        compass: document.getElementById('compass').hasAttribute('hidden'),
        map: document.getElementById('overview-map').hasAttribute('hidden'),
        street: document.getElementById('street-readout').hasAttribute('hidden'),
      };
      compass.click(); map.click(); street.click();
      return {
        hidden,
        restored: !document.getElementById('compass').hasAttribute('hidden')
          && !document.getElementById('overview-map').hasAttribute('hidden')
          && !document.getElementById('street-readout').hasAttribute('hidden'),
      };
    });
    check(`${label}: settings toggle all three navigation aids`,
      toggles.hidden.compass && toggles.hidden.map && toggles.hidden.street && toggles.restored,
      JSON.stringify(toggles));
    await page.click('#panel-close');

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

    // The document's own account of what this list is. It is compiled out of
    // `docs/LIBERTIES.md` and was rendered nowhere, while the panel opened with a
    // hand-written paraphrase of it — a restatement with nothing holding it to
    // the half it restates. Verbatim, and against the fetched document rather
    // than a phrase copied in here, because the failure this pins is a sentence
    // in the repository disagreeing with the sentence on the screen.
    const libNote = await page.evaluate(() => {
      const el = document.getElementById('liberties-note');
      const panel = document.querySelector('[data-panel="evidence"]');
      const recorded = window.__chicago4d.liberties?.note ?? '';
      const text = (panel?.textContent ?? '').replace(/\s+/g, ' ');
      return {
        shown: el?.textContent ?? '',
        recorded,
        busy: el ? el.hasAttribute('aria-busy') : true,
        // Once, not twice: the paraphrase is gone rather than joined.
        occurrences: recorded
          ? text.split(recorded.replace(/\s+/g, ' ')).length - 1 : 0,
      };
    });
    check(`${label}: the liberties list says what it is, in the document's words`,
      libNote.shown === libNote.recorded && libNote.recorded.length > 80 && !libNote.busy,
      `shown "${libNote.shown.slice(0, 80)}" of ${libNote.recorded.length} recorded`);
    check(`${label}: the panel states it once — the hand-written paraphrase is gone`,
      libNote.occurrences === 1, `${libNote.occurrences} occurrence(s)`);

    // The admissions themselves, on the page. `Covers:` is what the commit gate
    // reads to decide whether every invented footprint has been owned up to, and
    // a guarantee enforced in the repository but invisible in the walkthrough is
    // the same filed confession this panel exists to stop being. Asserted
    // discriminatingly: the entry that admits to the Sauganash's two invented
    // outlines shows footprint chips, and the scene-wide "no people" entry —
    // which invents nothing that gets drawn — claims nothing.
    const claims = await page.evaluate(() => {
      const entry = (id) => [...document.querySelectorAll('#liberties details.lib')]
        .find((d) => d.querySelector('.lib-id')?.textContent.trim() === id);
      const read = (id) => [...(entry(id)?.querySelectorAll('.lib-covers') ?? [])]
        .map((n) => n.textContent.trim());
      const tokens = (id) => [...(entry(id)?.querySelectorAll('.lib-covers') ?? [])]
        .map((n) => n.getAttribute('title') ?? '');
      return {
        l5: read('L5'), l8: read('L8'), l1: read('L1'), l4: read('L4'),
        l18: read('L18'), l19: read('L19'),
        bank: read('L31a'), slough: read('L31c'), bankTokens: tokens('L31a'),
      };
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

    // The admissions are not only about drawn geometry. A roof chosen because it
    // was usual and a porch left off because nobody found one are inventions a
    // visitor cannot see being made, so they get chips of their own — and the
    // chip reads as an attribute, not as the `form.` token the gate matches on.
    check(`${label}: an invented roof and height are admitted like an outline`,
      claims.l18.length === 2 && claims.l18.every((t) => /Sauganash/i.test(t))
      && claims.l18.some((t) => /roof type/.test(t))
      && claims.l18.some((t) => /wall height/.test(t))
      && !claims.l18.some((t) => /form\./.test(t)),
      `L18 claims [${claims.l18.join(' | ')}]`);
    check(`${label}: a decision made by default is admitted in two buildings`,
      claims.l19.length === 2 && new Set(claims.l19).size === 2
      && claims.l19.every((t) => /gallery/.test(t)),
      `L19 claims [${claims.l19.join(' | ')}]`);

    // The ground admits to its inventions on the same terms, and the chip has to
    // say which half of the dataset it lands in: a 6 m bank face nobody recorded
    // is the piece of ground every visitor walks down to the water on, and until
    // the coverage gate could read the terrain spec it was owned up to only
    // because somebody noticed. Asserted discriminatingly — a building's
    // admission must NOT read as the ground's, which a chip that simply printed
    // the token's first segment would have failed.
    check(`${label}: the ground admits to what it invented, and says it is the ground`,
      claims.bank.length === 1 && /the ground/.test(claims.bank[0])
      && /bank/.test(claims.bank[0]) && !claims.l5.some((t) => /the ground/.test(t)),
      `L31a claims [${claims.bank.join(' | ')}]`);
    check(`${label}: the chip carries the epoch the admission is about`,
      claims.bankTokens.length === 1
      && /^admitted for terrain\.[a-z0-9_]+\.bank$/.test(claims.bankTokens[0]),
      `L31a tokens [${claims.bankTokens.join(' | ')}]`);
    // The one ground invention nobody had written down until the gate demanded
    // it. A visitor reading "north side slough" here is reading a depth that no
    // source gives, on a watercourse whose course is Wright's.
    check(`${label}: the invention the gate found is on the page, not only in the repo`,
      claims.slough.length === 1 && /north side slough/.test(claims.slough[0]),
      `L31c claims [${claims.slough.join(' | ')}]`);

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

    // --- what is not here, in the same panel --------------------------------
    // The liberties answer "which parts did you make up". They cannot answer
    // "which parts did you find and leave out", and an empty street looks the
    // same whether a building is missing because nobody researched it or because
    // the evidence puts it two years later. The second is a finding with a
    // citation, and it shipped nowhere a visitor could read it until now.
    const excl = await page.evaluate(() => {
      const mount = document.getElementById('exclusions');
      const entries = [...mount.querySelectorAll('details.excl')];
      const byName = (re) => entries.find((d) => re.test(d.querySelector('.lib-title')?.textContent ?? ''));
      const saloon = byName(/Saloon Building/);
      const kinzie = byName(/Kinzie House/);
      return {
        counted: window.__chicago4d.exclusions?.count ?? 0,
        error: window.__chicago4d.exclusions?.error ?? 'no exclusions on the handle',
        rendered: entries.length,
        busy: mount.hasAttribute('aria-busy'),
        text: mount.textContent,
        titles: entries.map((d) => d.querySelector('.lib-title')?.textContent.trim() ?? ''),
        saloonWhen: saloon?.querySelector('.lib-scope')?.textContent.trim() ?? '',
        saloonReason: saloon?.querySelector('.lib-body dd')?.textContent.trim() ?? '',
        saloonCite: saloon?.querySelector('.cites .cite-text')?.textContent.trim() ?? '',
        saloonLinks: [...(saloon?.querySelectorAll('.cites a') ?? [])].map((a) => a.href),
        reprints: mount.querySelectorAll('.cite-reprints').length,
        kinzieWhen: kinzie?.querySelector('.lib-scope')?.textContent.trim() ?? '',
        kinzieReason: kinzie?.querySelector('.lib-body dd')?.textContent.trim() ?? '',
        // Collapsed: the standing note wraps across source lines, so a raw
        // textContent match would be asserting the HTML's line breaks.
        heading: (document.querySelector('[data-panel="evidence"]')?.textContent ?? '')
          .replace(/\s+/g, ' '),
        // The list's own account of itself, compiled into the derived document
        // and — until this landed — read into a return value and rendered by
        // nobody, while the markup carried a paraphrase of it.
        noteShown: document.getElementById('exclusions-note')?.textContent ?? '',
        noteRecorded: window.__chicago4d.exclusions?.standard ?? '',
        noteBusy: document.getElementById('exclusions-note')?.hasAttribute('aria-busy') ?? true,
        overflow: document.documentElement.scrollWidth <= window.innerWidth + 1,
      };
    });
    check(`${label}: the researched exclusions load`,
      excl.counted >= 14 && !excl.busy && excl.rendered === excl.counted,
      `${excl.rendered} rendered of ${excl.counted} (${excl.error})`);
    check(`${label}: an exclusion gives its reason and the source it rests on`,
      /1836/.test(excl.saloonReason) && /Andreas/.test(excl.saloonCite)
      && excl.saloonLinks.length > 0,
      `"${excl.saloonReason}" — ${excl.saloonCite} [${excl.saloonLinks.length} link(s)]`);
    // The chip is the record's own `earliest_scene`, never a phrase derived from
    // its absence: the Kinzie house is not here because it was GONE, and stamping
    // it "not until 1836" would be an invention on a panel about inventions.
    check(`${label}: a later building says when, and a vanished one says why instead`,
      /not until 1837/.test(excl.saloonWhen) && excl.kinzieWhen === ''
      && /GONE/i.test(excl.kinzieReason),
      `saloon "${excl.saloonWhen}" · kinzie "${excl.kinzieWhen}" / "${excl.kinzieReason.slice(0, 40)}"`);
    // The discriminating case: this is the list of things NOT in the scene, so a
    // building the visitor can walk up to must not appear on it. A section that
    // dumped the whole dataset would still have passed every check above.
    check(`${label}: a building standing in the scene is not on the not-here list`,
      !excl.titles.some((t) => /Sauganash|Green Tree|Wolf Point Tavern|Western Hotel/.test(t)),
      excl.titles.join(' | '));
    // Which is WHY this section withholds what a citation reprints, and the
    // rule above is the reason rather than a preference: the Inter Ocean piece
    // behind two of these entries is headed "The Old Western Hotel", and the
    // Western Hotel is standing 200 m away. Pinned so the option cannot quietly
    // flip back on — the card carries the line and this list does not.
    check(`${label}: the not-here list withholds what its sources reprint`,
      excl.reprints === 0, `${excl.reprints} reprints line(s) under the exclusions`);
    // …and it says so itself. A list of fourteen absences with no such sentence
    // reads as "this is what is missing", which would be the largest false claim
    // the panel could make — the town is short about thirty more buildings.
    check(`${label}: the list says it is not everything missing`,
      /What is not here/.test(excl.heading)
      && /not a list of everything missing/i.test(excl.heading),
      excl.heading.slice(-200));
    // …and it says it in the DERIVED document's words. Asserted verbatim against
    // the compiled value rather than a phrase copied in here, because the failure
    // this pins is the sentence in the repository disagreeing with the sentence
    // on the screen — the same assertion the liberties note and the ground's
    // scope already carry.
    check(`${label}: the not-here list says what it is, in the compiled document's words`,
      excl.noteShown === excl.noteRecorded && excl.noteRecorded.length > 80
      && !excl.noteBusy,
      `shown "${excl.noteShown.slice(0, 80)}" of ${excl.noteRecorded.length} recorded`);
    // Once, not twice: the hand-written paraphrase beside it is gone rather than
    // joined by the compiled sentence.
    check(`${label}: the panel states it once — the paraphrase is gone`,
      excl.noteRecorded
        ? excl.heading.split(excl.noteRecorded.replace(/\s+/g, ' ')).length - 1 === 1
        : false,
      `${excl.noteRecorded
        ? excl.heading.split(excl.noteRecorded.replace(/\s+/g, ' ')).length - 1
        : 'no'} occurrence(s)`);
    check(`${label}: the Evidence panel still does not overflow`, excl.overflow);

    // --- and the third category: researched, and still open -----------------
    // The exclusions answer "what did you find and leave out". They cannot hold
    // a structure whose 1835 status nobody could settle — and one of those four
    // is STANDING in the scene, so putting it on the not-here list would make
    // that list false. It gets its own section and its own chip.
    const open = await page.evaluate(() => {
      const mount = document.getElementById('uncertain');
      const entries = [...mount.querySelectorAll('details.uncertain')];
      const byName = (re) => entries.find((d) => re.test(d.querySelector('.lib-title')?.textContent ?? ''));
      const read = (d) => ({
        chip: d?.querySelector('.lib-scope')?.textContent.trim() ?? '',
        body: d?.querySelector('.lib-body')?.textContent.replace(/\s+/g, ' ').trim() ?? '',
        text: d?.textContent.replace(/\s+/g, ' ') ?? '',
        cites: [...(d?.querySelectorAll('.cites .cite-text') ?? [])].map((c) => c.textContent.trim()),
      });
      return {
        counted: window.__chicago4d.exclusions?.uncertainCount ?? 0,
        rendered: entries.length,
        busy: mount.hasAttribute('aria-busy'),
        western: read(byName(/Western Hotel/)),
        court: read(byName(/court-house/)),
        caldwell: read(byName(/Caldwell/)),
        heading: (document.querySelector('[data-panel="evidence"]')?.textContent ?? '')
          .replace(/\s+/g, ' '),
        // The same repair on the same fetch: this section's own account of the
        // third category, compiled and until now rendered nowhere. Its paraphrase
        // was the worse of the two — it had drifted into a hand-typed COUNT of
        // the open questions, wrong the day a fifth is recorded.
        noteShown: document.getElementById('uncertain-note')?.textContent ?? '',
        noteRecorded: window.__chicago4d.exclusions?.uncertainStandard ?? '',
        noteBusy: document.getElementById('uncertain-note')?.hasAttribute('aria-busy') ?? true,
        overflow: document.documentElement.scrollWidth <= window.innerWidth + 1,
      };
    });
    check(`${label}: the open questions load`,
      open.counted === 4 && !open.busy && open.rendered === open.counted,
      `${open.rendered} rendered of ${open.counted}`);
    // The discriminating pair, and it is the whole argument for the section: one
    // of these four is a building the visitor can walk up to and three are empty
    // ground. A section that stamped one chip on all four would have passed any
    // check for "there is a chip" — and would be lying about the Western Hotel.
    check(`${label}: the standing one says it is standing and the unbuilt ones do not`,
      /standing here/.test(open.western.chip) && /inferred/.test(open.western.chip)
      && open.court.chip === 'not built' && open.caldwell.chip === 'not built',
      `western "${open.western.chip}" · court "${open.court.chip}"`);
    // …and the doubt is not restated here in this section's own words. It names
    // the claim on the record that carries it, which is the same claim the
    // provenance card shows, so the two cannot drift.
    check(`${label}: the standing one names the claim on its record that carries the doubt`,
      /frame_1834\.documented_range/.test(open.western.text)
      && /provenance card/i.test(open.western.body),
      open.western.body.slice(0, 200));
    // An entry resting on no source record says so in a sentence. An empty list
    // of citations would read as an oversight rather than the finding it is —
    // the dossier does not say which source calls the story unverified, and
    // naming one here would be inventing it.
    check(`${label}: an uncited open question says why it is uncited`,
      /No source record/i.test(open.caldwell.text)
      && open.caldwell.cites.length === 0 && open.court.cites.length > 0,
      `caldwell ${open.caldwell.cites.length} cite(s) · court ${open.court.cites.length}`);
    check(`${label}: the panel says what the third category is`,
      /still an open question/i.test(open.heading)
      && /standing in front of you/i.test(open.heading),
      open.heading.slice(-240));
    // …in the compiled document's words, verbatim, and once. The paraphrase this
    // replaces counted the entries — "three of these … and the fourth" — which no
    // gate could have held to a list that grows.
    check(`${label}: the open questions say what they are, in the compiled document's words`,
      open.noteShown === open.noteRecorded && open.noteRecorded.length > 80
      && !open.noteBusy,
      `shown "${open.noteShown.slice(0, 80)}" of ${open.noteRecorded.length} recorded`);
    check(`${label}: the panel states that once too — and counts nothing by hand`,
      (open.noteRecorded
        ? open.heading.split(open.noteRecorded.replace(/\s+/g, ' ')).length - 1 === 1
        : false)
      && !/Three of these/i.test(open.heading),
      `${open.noteRecorded
        ? open.heading.split(open.noteRecorded.replace(/\s+/g, ' ')).length - 1
        : 'no'} occurrence(s)`);
    check(`${label}: the Evidence panel still does not overflow with it`, open.overflow);

    // …and the same entry on the building it is about. The section above tells a
    // visitor that "the provenance card shows it", and until now the card showed
    // the CLAIM — a dated span with an `inferred` chip — and never that the claim
    // is a tracked open question with a live dispute behind it. The doubt reached
    // whoever opened a panel about the scene, not whoever walked up to the house.
    //
    // Asserted against the rendered card, per building, on the discriminating
    // pair — as everywhere else on this card, and for the reason `documented_range`
    // taught: reading the derived list would prove only that the list is fine.
    const openCard = await page.evaluate(() => {
      const read = (id) => {
        window.__chicago4d.pick(id);
        const sec = document.querySelector('#popup .pop-question');
        const entry = sec?.querySelector('details.uncertain');
        const body = entry?.querySelector('.lib-body');
        const presence = [...document.querySelectorAll('#popup .pop-sec')]
          .find((s) => /Was it here/i.test(s.querySelector('h3')?.textContent ?? ''));
        return {
          present: !!sec,
          chip: entry?.querySelector('.lib-scope')?.textContent.trim() ?? '',
          text: (sec?.textContent ?? '').replace(/\s+/g, ' ').trim(),
          collapsed: body ? body.checkVisibility() === false : null,
          presenceChip: presence?.querySelector('.conf')?.textContent.trim() ?? '',
        };
      };
      const western = read('western_hotel');
      // Every other building in the scene, because "no section" is the rule and
      // not a property of whichever second building this pair happens to name.
      const others = [...window.__chicago4d.registry.keys()]
        .filter((id) => id !== 'western_hotel')
        .filter((id) => read(id).present);
      return { western, others };
    });
    check(`${label}: the open question reaches the building it is about`,
      openCard.western.present
      && /W\. H\. Stow/.test(openCard.western.text)
      && /hotel chronology/i.test(openCard.western.text)
      && /frame_1834\.documented_range/.test(openCard.western.text),
      openCard.western.text.slice(0, 220));
    // What no chip can say: what settling it would change. The grade tells a
    // visitor we are unsure; only this says the dispute is between the builder's
    // own statement and a chronology, and that the answer decides whether the
    // house was new or still going up on the day they are standing in.
    check(`${label}: it says what settling it would change`,
      /What it would change/i.test(openCard.western.text)
      && /STANDING in the scene/i.test(openCard.western.text),
      openCard.western.text.slice(-260));
    // One uncertainty, two surfaces, one grade. The card's own presence chip and
    // the open question's chip are read from the same record field, so a card that
    // qualified the two differently is exactly the drift the shared renderer and
    // the `carried_by` gate exist to stop.
    check(`${label}: the card grades the doubt the same way the claim above it is graded`,
      openCard.western.chip === 'inferred'
      && openCard.western.presenceChip === 'inferred',
      `question "${openCard.western.chip}" · presence "${openCard.western.presenceChip}"`);
    check(`${label}: it starts collapsed like every other disclosure on the card`,
      openCard.western.collapsed === true, `collapsed ${openCard.western.collapsed}`);
    // The discriminating case, and it is a deliberate silence rather than a
    // missing empty state. The current watch list has exactly two structures in
    // the scene: the Western Hotel and Cobweb Castle. Every other building must
    // stay silent; a card dumping the whole list would fail this exact set.
    check(`${label}: only tracked in-scene buildings carry open questions`,
      openCard.others.length === 1 && openCard.others[0] === 'cobweb_castle',
      `beside western_hotel: ${openCard.others.join(', ') || 'none'}`);
    // Reading every card leaves one open over the panel, which the panel's own
    // close button then cannot be clicked through.
    await page.evaluate(() => window.__chicago4d.popup.close());

    // --- what the ground claims, in the same panel ---------------------------
    // Every building can say what it asserts and how sure of it we are. The
    // surface all of them stand on is graded just as carefully in
    // `terrain_spec.json` and said none of it to a visitor — while dithering
    // under the confidence view, which shows that a grade exists and nothing
    // about what was graded.
    const ground = await page.evaluate(() => {
      const mount = document.getElementById('ground');
      const entries = [...mount.querySelectorAll('details.ground')];
      const read = (d) => ({
        label: d.querySelector('.lib-title')?.textContent.trim() ?? '',
        group: d.querySelector('.lib-scope')?.textContent.trim() ?? '',
        conf: d.querySelector('summary .conf')?.textContent.trim() ?? '',
        body: d.querySelector('.lib-body')?.textContent.replace(/\s+/g, ' ').trim() ?? '',
        cites: [...d.querySelectorAll('.cites > li')].map((li) => li.textContent.trim()),
        // Which of this claim's figures say they are not in front of you, by the
        // figure's own name — a count would pass against a panel that marked the
        // wrong row.
        marks: [...d.querySelectorAll('.lib-body dd .geom')].map((g) => ({
          field: g.closest('dd')?.previousElementSibling?.textContent.trim() ?? '',
          text: g.textContent.trim(),
        })),
      });
      const all = entries.map(read);
      const find = (labelRe, groupRe) => all.find(
        (e) => labelRe.test(e.label) && (!groupRe || groupRe.test(e.group))) ?? null;
      return {
        counted: window.__chicago4d.ground?.count ?? 0,
        error: window.__chicago4d.ground?.error ?? 'no ground on the handle',
        rendered: entries.length,
        busy: mount.hasAttribute('aria-busy'),
        water: find(/^water$/, /water surface/),
        bank: find(/^bank$/, /the bank/),
        south: find(/South Division/, /divisions/),
        material: find(/^north division$/, /made of/),
        southMaterialWest: find(/^south division west of State St$/, /made of/),
        southMaterialEast: find(/^south division east of State St$/, /made of/),
        marshMaterial: find(/^south division marsh$/, /made of/),
        // The compiled claim, so the assertion below compares the panel with the
        // repository rather than with a phrase typed into this file.
        recordedNotes: Object.fromEntries(
          (window.__chicago4d.ground?.claims ?? []).map(
            (c) => [c.id, (c.notes ?? []).map((n) => n.replace(/\s+/g, ' ').trim())])),
        // Land vertices: the divisions, the bank, the marsh, the swales and the
        // micro-relief. Their grades are what the caveat is about.
        landGrades: all.filter((e) => /divisions|the bank|marshy|swales|texture/.test(e.group))
          .map((e) => e.conf),
        inferredWithoutReason: all.filter(
          (e) => e.conf === 'inferred' && /No reasoning is recorded/.test(e.body))
          .map((e) => `${e.group}/${e.label}`),
        scopeShown: mount.querySelector('.ground-scope')?.textContent
          .replace(/^\s*What these claims cover\s*—\s*/, '') ?? '',
        scopeRecorded: window.__chicago4d.ground?.scope ?? '',
        text: mount.textContent.replace(/\s+/g, ' '),
        overflow: document.documentElement.scrollWidth <= window.innerWidth + 1,
      };
    });
    check(`${label}: the ground's claims load`,
      ground.counted >= 19 && !ground.busy && ground.rendered === ground.counted,
      `${ground.rendered} rendered of ${ground.counted} (${ground.error})`);
    // THE discriminating pair, and the reason this section is worth having: the
    // water plane is documented and the bank face — the largest unsourced
    // assumption in the build — is conjectural. A section that stamped one grade
    // on the whole terrain would pass any check for "there is a chip".
    check(`${label}: the ground is graded per claim, not stamped`,
      ground.water?.conf === 'documented' && ground.bank?.conf === 'conjectural',
      `water "${ground.water?.conf}" · bank "${ground.bank?.conf}"`);
    // The spec's own caveat, asserted where a visitor reads it rather than in the
    // file: no land elevation in this scene is better than inferred.
    check(`${label}: no land elevation claims to be documented`,
      ground.landGrades.length >= 6 && !ground.landGrades.includes('documented'),
      `${ground.landGrades.length} land claim(s): ${[...new Set(ground.landGrades)].join(', ')}`);
    // WHICH ground these twenty claims are about. The spec has stated its own
    // extent since it was written, `compile_scene.py` has compiled it into every
    // terrain sidecar, and no renderer ever asked for it — so a visitor who flew
    // up, saw the ground end, and came to this section to find out what it covers
    // was told everything except that. Verbatim against the compiled value, for
    // the same reason as the record's own account above.
    check(`${label}: the ground says which ground these claims are about`,
      ground.scopeShown === ground.scopeRecorded && (ground.scopeRecorded ?? '').length > 40
      && /forks.*harbour/i.test(ground.scopeShown ?? ''),
      `shown "${(ground.scopeShown ?? '').slice(0, 90)}" of `
      + `${(ground.scopeRecorded ?? '').length} recorded`);
    check(`${label}: the panel quotes the spec's caveat that no survey exists`,
      /No contour survey of the 1835 town site exists/.test(ground.text)
      && /no land elevation in this spec is better than/i.test(ground.text),
      ground.text.slice(0, 120));
    // A claim carries the spec's own figures and the source it rests on.
    check(`${label}: a land claim shows its figures and its citation`,
      /far \(m\)/.test(ground.south?.body ?? '') && /300/.test(ground.south?.body ?? '')
      && (ground.south?.cites ?? []).some((c) => /chicagoarchitecturehistory|architecture/i.test(c)),
      `${(ground.south?.body ?? '').slice(0, 80)} | ${(ground.south?.cites ?? [])[0] ?? 'no cite'}`);
    // Until 2026-08-10 this asserted the opposite: three surface materials were
    // graded `inferred` with no reasoning at all, and the panel said so because
    // the empty state was the finding. The three notes are written now — what
    // held them back was the staleness hash, not the research — so what is worth
    // pinning is the gate's rule (`check_terrain_claims`) asserted where a
    // visitor reads it: nothing that calls itself an INFERENCE may show the
    // disclaimer. Scoped to inferred on purpose — a documented claim owes
    // evidence, not an argument, so an assertion over the whole panel would have
    // read the two documented soil claims as gaps. One of those two has since
    // grown a note for a different reason; see the next assertion.
    check(`${label}: every claim that calls itself an inference records its reasoning`,
      !ground.inferredWithoutReason.length
      && /north-side section measured on its own/i.test(ground.material?.body ?? ''),
      `${ground.inferredWithoutReason.join(', ') || 'none'} | material `
      + `"${(ground.material?.body ?? '').slice(0, 80)}"`);
    // A grade this project has decided is too high, said where the grade is read.
    // `surface_materials.south_division` is `documented` on a 2022 essay that was
    // opened on 2026-08-11 and prints no citation for anything; the value is to
    // become `inferred` and cannot move until a Blender bake lands, because a
    // confidence is an input to the ground mesh. So the correction ships as prose
    // — which the terrain hash strips — and a visitor reads it under a chip that
    // is still the old one.
    //
    // Verbatim against the compiled claim rather than a phrase copied here: the
    // failure being pinned is the sentence in the repository disagreeing with the
    // sentence on the screen. And the pair is discriminating rather than a
    // presence check — the OTHER documented soil claim (the marsh, on
    // `chicagology_prefire273`) is correctly graded and carries no such
    // correction, so a panel that stamped this disclosure on every documented
    // claim would fail here.
    const southNotes = ground.recordedNotes?.['surface_materials.south_division west of State St'] ?? [];
    const marshNotes = ground.recordedNotes?.['surface_materials.south_division_marsh'] ?? [];
    const overGraded = southNotes.find((n) => /over-graded/.test(n)) ?? '';
    check(`${label}: the soil claim that is graded too high says so where it is graded`,
      ground.southMaterialWest?.conf === 'documented'
      && overGraded.length > 200
      && (ground.southMaterialWest?.body ?? '').replace(/\s+/g, ' ').includes(overGraded)
      && ground.southMaterialEast?.conf === 'documented'
      && ground.marshMaterial?.conf === 'documented'
      && !marshNotes.some((n) => /over-graded/.test(n))
      && !/over-graded/.test(ground.marshMaterial?.body ?? ''),
      `south-west "${ground.southMaterialWest?.conf}" carries ${overGraded.length} chars · `
      + `south-east "${ground.southMaterialEast?.conf}" · `
      + `marsh "${ground.marshMaterial?.conf}" carries ${marshNotes.length} note(s)`);
    // The empty state stays: it is a guard now rather than a finding, and the
    // committed data no longer exercises the half that matters — a claim that
    // OWES a reason and gives none. That is exercised directly: the renderer must
    // still say so for a claim with no reasoning, and must not say it for one that
    // has some — the discriminating pair, one level down from the panel.
    const emptyState = await page.evaluate(async () => {
      const { groundClaimHtml } = await import('/renderers/web/js/ground.js');
      const claim = { id: 'x', group: 'g', label: 'l', confidence: 'inferred',
        fields: [], sources: [], citations: [], notes: [] };
      return {
        without: groundClaimHtml(claim),
        with: groundClaimHtml({ ...claim, notes: ['because the sources say so'] }),
      };
    });
    check(`${label}: a claim with no reasoning would still say so`,
      /No reasoning is recorded/.test(emptyState.without)
      && !/No reasoning is recorded/.test(emptyState.with)
      && /because the sources say so/.test(emptyState.with),
      emptyState.without.slice(0, 120));
    // The ground's version of the Wolf Point wolf sign, and the reason this slice
    // exists: the surface materials are graded — two of them `documented`, the
    // strongest grade this project awards — and NOTHING in the model is made of
    // any of them. The assertion is the discriminating pair rather than "a mark
    // exists": the material row is marked and the dossier-zone row beside it is
    // not, and the bank, whose face_m is what shapes every bank in the box,
    // carries no mark at all.
    check(`${label}: a soil the ground is not made of says so, and the figures that are do not`,
      (ground.material?.marks ?? []).some(
        (m) => /material/.test(m.field) && m.text === 'not modelled from this')
      && !(ground.material?.marks ?? []).some((m) => /dossier/.test(m.field))
      && !(ground.bank?.marks ?? []).length,
      `material marks ${JSON.stringify(ground.material?.marks ?? [])} · `
      + `bank marks ${JSON.stringify(ground.bank?.marks ?? [])}`);
    // And the mark is exercised at the renderer, so it survives the data being
    // repaired: the day S6 colours the ground by zone, the declaration comes off
    // the spec and the committed panel stops carrying this case.
    const marking = await page.evaluate(async () => {
      const { groundClaimHtml } = await import('/renderers/web/js/ground.js');
      const claim = { id: 'x', group: 'g', label: 'l', confidence: 'documented',
        sources: [], citations: [], notes: ['because'] };
      const html = (mesh) => groundClaimHtml({ ...claim,
        fields: [{ key: 'material', value: 'loam', ...(mesh ? { mesh } : {}) }] });
      return { unbuilt: html('simplified'), built: html(null),
        restated: html('restated_in_code') };
    });
    check(`${label}: the mark is the declaration's, not the row's`,
      /not modelled from this/.test(marking.unbuilt)
      && !/not modelled from this/.test(marking.built)
      && !/geom/.test(marking.restated),
      marking.unbuilt.slice(0, 140));
    check(`${label}: the Evidence panel still does not overflow with the ground on it`,
      ground.overflow);
    await page.click('#panel-close');

    // --- free-fly -----------------------------------------------------------
    // Three properties worth pinning, all of which would rot silently:
    // the aerial anchor arrives IN the air, the terrain is still a floor, and
    // landing puts you back on the ground rather than stranding the eye.
    const aerial = await page.evaluate(async () => {
      const a = window.__chicago4d;
      a.goTo('from_above');
      await new Promise((r) => setTimeout(r, 400));
      return {
        alt: a.player.altitude, flying: a.player.flying, pitch: a.player.pitchDeg,
        label: document.getElementById('badge-alt')?.textContent?.trim(),
      };
    });
    check(`${label}: the aerial anchor arrives in the air, looking down`,
      aerial.flying === true && aerial.alt > 100 && aerial.pitch < -10
      && /^\d+ ft up$/.test(aerial.label ?? '') && !/\d+ m up/.test(aerial.label ?? ''),
      `flying ${aerial.flying}, internal ${aerial.alt?.toFixed(0)} m, `
      + `HUD ${aerial.label}, pitch ${aerial.pitch?.toFixed(0)}`);

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
  await browser.close();
  console.log('');
}

// The vendored meshopt decoder must be a working module, because the published
// web derivatives will need it and a broken vendor file would only surface then.
{
  const browser = await launchBrowser();
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
  await browser.close();
}
server.close();

console.log(`\n${passes.length} passed, ${failures.length} failed`);
if (failures.length) {
  console.log(`FAILURES:\n - ${failures.join('\n - ')}`);
  process.exit(1);
}
console.log('SMOKE PASS');
