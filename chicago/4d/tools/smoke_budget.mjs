#!/usr/bin/env node
/**
 * T-0235 — what the renderer gate COSTS on this machine, and which parts of it
 * cover the change you actually made.
 *
 *   node tools/smoke_budget.mjs                    # the measured cost of the whole gate
 *   node tools/smoke_budget.mjs --for <path>…      # the parts that cover those files
 *   node tools/smoke_budget.mjs --for-diff [ref]   # the same, off `git diff --name-only`
 *   node tools/smoke_budget.mjs --self-test        # the map has not rotted (check.sh)
 *
 * WHY THIS EXISTS. Three tickets — T-0170, T-0173, T-0181 — reason about the
 * desktop legs' margin against a **30-minute** cap. On the steward runner the
 * whole gate was measured at 55 m 10 s on 2026-08-27, so that cap describes
 * some other machine and those three margins are margins against a number that
 * was never taken here. And a steward run's single foreground command is capped
 * at 600 s, so no run can take the gate whole: it takes the parts that cover
 * what it touched, and until now nothing said which those are. A run therefore
 * either ran all fifteen commands — more than its whole budget — or picked by
 * feel.
 *
 * THE FIGURES ARE READ, NEVER ASSERTED. Every second printed here comes out of
 * `tools/dev-smoke-state.json`, the standing record T-0216 built, filtered to
 * readings taken ON THIS CLASS OF MACHINE (`host.kind: steward-runner`) against
 * the published mirror. Nothing here is a bar, a gate or a promise — it is the
 * record, summarised, with the parts it has no reading for named as such. When
 * the town grows and the parts get re-cut again, the numbers move on their own.
 *
 * THE MAP CAN ONLY EVER ADD PARTS. A path the map does not know maps to THE
 * WHOLE GATE, not to nothing — so a file nobody thought about makes the recipe
 * bigger rather than quietly making it smaller. `--self-test` holds that, holds
 * the part count against `smoke_renderer.mjs`'s own `PARTS`, and holds every
 * pattern in the map against the committed tree, so a renamed module shows up
 * here rather than as a part that silently stopped being recommended.
 *
 * THE NUMBERING CHANGED ON 2026-08-30 (T-0346): old part 4 became 4 + 5 + 6 and
 * old parts 5-9 became 7-11. Readings filed before that merge are labelled in
 * the old numbering, and this tool RENUMBERS them rather than discarding them —
 * the content of old part 5 is the content of new part 7, so the reading is a
 * reading of new part 7. Old part 4 is the one that cannot be renumbered to a
 * single part: it is a reading of 4+5+6 together, and it is reported that way.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');                 // chicago/4d
const REPO = path.resolve(APP, '..', '..');           // the monorepo root
const STATE = path.join(HERE, 'dev-smoke-state.json');
const SMOKE = path.join(HERE, 'smoke_renderer.mjs');

/** Parts of the smoke body. Mirrors `PARTS` in tools/smoke_renderer.mjs, and
 *  `--self-test` fails if the two ever disagree. */
const PARTS = 11;

/** A steward run's single foreground command is capped at 600 s (ROADMAP § THE
 *  RUN BUDGET). Recipes are packed to a lower figure so a part that has grown
 *  since its last reading does not put the command over on its own. */
const CEILING_S = 600;
const PACK_TO_S = 480;

/** The T-0346 merge, after which a reading's stage numbers are the current
 *  ones. Before it, old part 4 is new 4+5+6 and old 5-9 are new 7-11. */
const RENUMBERED_AT = Date.parse('2026-08-30T03:35:16Z');

/** Which parts cover which change.
 *
 *  Each entry is a path prefix or a `*`-glob against the repo-relative path
 *  inside `chicago/4d/`, and the parts of the smoke body that read what it
 *  produces. The justification for each row is the part's own section headings
 *  in `smoke_renderer.mjs` — see docs/SMOKE-BUDGET.md, which lists them.
 *
 *  `ALL` means every part: the file feeds the whole scene, so no part can be
 *  ruled out. That is also what an UNKNOWN path maps to. */
const ALL = Array.from({ length: PARTS }, (_, i) => i + 1);
/** NONE is not a gap. It is the map SAYING that no part of the smoke body reads
 *  this path, which is a different statement from "nobody wrote a row for it" —
 *  the second maps to the whole gate. A NONE-only change still runs one cheap
 *  staged pass per viewport, because boot, the page-error check and the vendor
 *  checks are taken in EVERY invocation whichever stage is asked for. */
const NONE = [];
const COVERAGE = [
  // --- read by no part of the scene: the gate's own tooling, the backlog, the
  // --- prose. check.sh is what covers these, not the renderer.
  ['tools/', NONE, 'the gate\'s own tooling — not served to the browser'],
  ['generators/', NONE, 'the bake\'s generators — their output is the data rows below'],
  ['patches/', NONE, 'vendored patches applied at build time, not at run time'],
  ['tickets/', NONE, 'the backlog'],
  ['docs/', NONE, 'prose — except docs/LIBERTIES.md, which compiles into the scene'],
  ['README.md', NONE, 'prose'],
  ['AGENTS.md', NONE, 'prose'],
  ['tools/smoke_renderer.mjs', ALL, 'the gate itself'],

  // --- the whole scene: geometry, the scene graph, the boot chain, the mirror
  ['assets/', ALL, 'meshes and the material sheet — every part draws them'],
  ['data/structures/', ALL, 'the records the whole town is built from'],
  ['data/scenes/', ALL, 'what the scene loads at all'],
  ['data/datum.json', ALL, 'the projection every metre in the scene is in'],
  ['data/exclusions.json', ALL, 'what the scene declares it is NOT drawing'],
  ['renderers/web/js/main.js', ALL, 'the boot chain'],
  ['renderers/web/js/scene-loader.js', ALL, 'the boot chain'],
  ['renderers/web/js/world.js', ALL, 'the world the parts all measure against'],
  ['renderers/web/js/geometry.js', ALL, 'shared geometry the parts all read'],
  ['renderers/web/index.html', ALL, 'the page itself'],
  ['renderers/web/css/', ALL, 'the chrome every panel check clicks'],
  ['data/reconstruction/', ALL, 'the infill programme the records are expanded from'],
  ['site/chicago/4d/', ALL, 'the published mirror, which is the --published target'],
  ['site/chicago/4d/js/changelog.js', [10], "the mirrored entries What's-new reads"],
  ['site/chicago/4d/walk/js/changelog.js', [10], "the mirrored entries What's-new reads"],
  ['site/chicago/4d/tickets.json', NONE, 'the backlog mirror — the renderer never loads it'],

  // --- PART 1: the enclosure layer, the plantings inside it, and the signs
  ['renderers/web/js/enclosures.js', [1], 'the enclosure layer (T-0038)'],
  ['renderers/web/js/yards.js', [1], "the town's lot-line yard fences (T-0068)"],
  ['renderers/web/js/signage.js', [1], 'the business signs (T-0039, T-0066)'],
  ['data/enclosures/', [1], 'fences, the pound, the dooryard pickets'],
  ['data/signage/', [1], 'what the signs say'],

  // --- PART 2: the trading frontages, the river's edge and what floats on it
  ['renderers/web/js/frontage.js', [2], 'the frontage layer (T-0082, T-0090)'],
  ['renderers/web/js/yard.js', [2], 'the yard goods at the trading frontages (T-0040)'],
  ['renderers/web/js/wharves.js', [2], 'the river wharves (T-0041) and walking one (T-0058)'],
  ['renderers/web/js/boats.js', [2], 'the boats on the river (T-0063)'],
  ['renderers/web/js/confidence.js', [2, 3, 6], 'the confidence view, its card and its menu'],
  ['data/frontage/', [2], 'the frontage records'],
  ['data/wharves/', [2], 'the wharf records'],
  ['data/boats/', [2], 'the boat records'],
  ['data/yard/', [2], 'the yard goods'],

  // --- PART 3: the ground you stand on, and the card that says why
  ['renderers/web/js/ground.js', [3], 'the ground faces the sky (R-BUG3c)'],
  ['renderers/web/js/terrain.js', [3], 'the ground the town stands on'],
  ['renderers/web/js/citations.js', [3], 'pick -> provenance, and what kind of source'],
  ['renderers/web/js/liberties.js', [3, 11], 'the liberties on the card, and in the panel'],
  ['renderers/web/js/residents.js', [3, 11], 'who was here, and the people in the panel'],
  ['renderers/web/js/display-name.js', [3], 'the prose may not name a level the record is not'],
  ['renderers/web/js/popup.js', [3], 'the card a visitor opens'],
  ['renderers/web/js/census.js', [3, 9], 'the population on the card and in the census'],
  ['data/terrain/', [3], 'the heightfield'],
  ['data/liberties.json', [3, 11], 'what we made up about THAT building'],
  ['docs/LIBERTIES.md', [3, 11], 'the source the liberties are compiled from'],
  ['data/residents/', [3, 11], 'the invented residents have names now (K18)'],
  ['data/sources/', [3], 'the citation -> its document'],
  ['data/sidecars/', [3], 'the record\'s own account, on the card'],

  // --- PARTS 4-6: standing, walking, the detail ladder and the chrome
  ['renderers/web/js/walker.js', [4, 5, 6], 'walking, standing, and the ladder they are measured on'],
  ['renderers/web/js/controls/', [4, 5, 6, 10], 'the pick, the touch backend and the settings'],
  ['renderers/web/js/far-merge.js', [5, 7], 'the detail ladder and the batch merge'],

  // --- PART 7: navigation, the roads and the merge the reach stands on
  ['renderers/web/js/navigation.js', [7], 'navigation and its readouts'],
  ['renderers/web/js/hud.js', [7], 'the readouts a visitor navigates by'],

  // --- PART 8: what the light does to the town
  ['renderers/web/js/facades.js', [8], 'T-0002, the facade tones'],
  ['renderers/web/js/buildings.js', [8], 'the facades and the shadow reach they carry'],

  // --- PART 9: what grows, what moves, and the streets a visitor reads
  ['renderers/web/js/flora.js', [9], 'the flora census'],
  ['renderers/web/js/plants.js', [9], 'the sward'],
  ['renderers/web/js/trees.js', [9], 'the horizon timber'],
  ['renderers/web/js/shrub-grain.js', [9], 'the sward\'s grain'],
  ['renderers/web/js/fauna.js', [9, 11], 'the wildlife, drawn and in the panel'],
  ['renderers/web/js/streets.js', [2, 7, 9], 'the street edge, the road aid and the street names'],
  ['data/flora/', [9, 11], 'what grows here'],
  ['data/fauna/', [9, 11], 'the wildlife'],
  ['data/streets/', [2, 7, 9], 'the street records'],
  ['data/traces/', [2, 7, 9], 'the traced lines the streets and the bank are built from'],
  ['data/town_census.json', [9], 'the drawn population'],

  // --- PART 10: the settings, the Go-to tab and What's-new
  ['renderers/web/js/whatsnew.js', [10], "what's new"],
  ['renderers/web/js/changelog.js', [10], "the entries What's-new reads"],
  ['renderers/web/js/units.js', [10], 'the settings that change what the readouts say'],

  // --- PART 11: the Evidence panel and the air above the town
  ['data/research/', [11], 'researched, and still open — the third category'],
];

// ---------------------------------------------------------------------------

const fmt = (s) => (s == null ? '     —' : `${Math.floor(s / 60)}m ${String(Math.round(s % 60)).padStart(2, '0')}s`);
const key = (parts) => parts.join(',');

/** The current parts a reading covers, renumbering it if it predates T-0346. */
function currentParts(reading) {
  const taken = Date.parse(reading.takenAt);
  const parts = reading.parts || [];
  if (!parts.length) return null;
  if (Number.isFinite(taken) && taken >= RENUMBERED_AT) return parts.slice().sort((a, b) => a - b);
  const out = new Set();
  for (const p of parts) {
    if (p <= 3) out.add(p);
    else if (p === 4) { out.add(4); out.add(5); out.add(6); }
    else out.add(p + 2);
  }
  return [...out].sort((a, b) => a - b);
}

/** Every measured group, per viewport: a set of current parts -> median seconds. */
function measured() {
  const state = JSON.parse(fs.readFileSync(STATE, 'utf8'));
  const groups = new Map();                     // "viewport|1,2" -> {viewport, parts, secs[]}
  for (const r of state.readings || []) {
    if (!r.wallSeconds) continue;               // a killed run reports none
    if ((r.host && r.host.kind) !== 'steward-runner') continue;
    if (r.target !== 'published') continue;     // the --published run is the one that matters
    const parts = currentParts(r);
    if (!parts) continue;
    const k = `${r.viewport}|${key(parts)}`;
    if (!groups.has(k)) groups.set(k, { viewport: r.viewport, parts, secs: [], renumbered: false });
    const g = groups.get(k);
    g.secs.push(r.wallSeconds);
    if (Date.parse(r.takenAt) < RENUMBERED_AT) g.renumbered = true;
  }
  for (const g of groups.values()) {
    const s = g.secs.slice().sort((a, b) => a - b);
    g.median = s[Math.floor(s.length / 2)];
    g.n = s.length;
  }
  return [...groups.values()];
}

/** Cover `want` with disjoint measured groups, cheapest-and-narrowest first.
 *  Returns the chosen groups and the parts nothing has a reading for. */
function cover(groups, viewport, want) {
  // Coverage first, cost second: a reading of parts 3-6 together is worth more
  // to this report than a cheaper reading of part 3 alone that leaves 4, 5 and
  // 6 with no figure at all.
  const pool = groups.filter((g) => g.viewport === viewport);
  const taken = new Set();
  const chosen = [];
  for (const p of want) {
    if (taken.has(p)) continue;
    const usable = pool.filter((c) => c.parts.includes(p) && !c.parts.some((q) => taken.has(q)));
    if (!usable.length) continue;
    usable.sort((a, b) => b.parts.length - a.parts.length || a.median - b.median);
    const g = usable[0];
    chosen.push(g);
    for (const q of g.parts) taken.add(q);
  }
  return { chosen, missing: want.filter((p) => !taken.has(p)) };
}

/** Pack `want` into commands that each stay under the pack budget. */
function recipe(groups, viewport, want) {
  const cost = new Map();
  for (const g of groups.filter((x) => x.viewport === viewport)) {
    if (g.parts.length === 1) cost.set(g.parts[0], g.median);
  }
  // A part with no reading of its own is priced at the mean of the ones that
  // have one — an estimate, printed as such, never a claim.
  const known = [...cost.values()];
  const fallback = known.length ? Math.round(known.reduce((a, b) => a + b, 0) / known.length) : null;
  const cmds = [];
  let cur = [];
  let curCost = 0;
  for (const p of want) {
    const c = cost.get(p) ?? fallback ?? 0;
    if (cur.length && curCost + c > PACK_TO_S) { cmds.push({ parts: cur, secs: curCost }); cur = []; curCost = 0; }
    cur.push(p);
    curCost += c;
  }
  if (cur.length) cmds.push({ parts: cur, secs: curCost });
  return { cmds, estimated: want.filter((p) => !cost.has(p)) };
}

/** `1,2,3,5` -> `1-3,5`, the form SMOKE_STAGE takes. */
function stageArg(parts) {
  const out = [];
  let i = 0;
  while (i < parts.length) {
    let j = i;
    while (j + 1 < parts.length && parts[j + 1] === parts[j] + 1) j++;
    out.push(i === j ? `${parts[i]}` : `${parts[i]}-${parts[j]}`);
    i = j + 1;
  }
  return out.join(',');
}

/** The part of `viewport` with the smallest measured reading of its own. */
function cheapestPart(groups, viewport) {
  const singles = groups.filter((g) => g.viewport === viewport && g.parts.length === 1)
    .sort((a, b) => a.median - b.median);
  return singles.length ? singles[0].parts[0] : 1;
}

function partsFor(paths) {
  const hits = [];
  const want = new Set();
  let unknown = 0;
  for (const raw of paths) {
    // Accept a repo-root path (chicago/4d/…) or an app-relative one.
    const p = raw.replace(/^chicago\/4d\//, '');
    // Specificity, so a general prefix cannot drown a row written about one
    // file: an exact-path row beats every prefix row, and the longest prefix
    // beats the shorter ones it sits inside.
    const exact = COVERAGE.filter(([pat]) => !pat.endsWith('/') && p === pat);
    let rows = exact;
    if (!rows.length) {
      const pre = COVERAGE.filter(([pat]) => pat.endsWith('/') && p.startsWith(pat));
      const longest = Math.max(0, ...pre.map(([pat]) => pat.length));
      rows = pre.filter(([pat]) => pat.length === longest);
    }
    if (!rows.length) {
      unknown++;
      hits.push({ path: p, parts: ALL, why: 'NOT IN THE MAP — the whole gate, because nothing here can rule a part out' });
      for (const n of ALL) want.add(n);
      continue;
    }
    const ps = [...new Set(rows.flatMap(([, parts]) => parts))].sort((a, b) => a - b);
    hits.push({ path: p, parts: ps, why: rows.map(([, , why]) => why).join('; '), none: ps.length === 0 });
    for (const n of ps) want.add(n);
  }
  return { hits, want: [...want].sort((a, b) => a - b), unknown };
}

// --- the reports -----------------------------------------------------------

function reportCost(groups) {
  console.log('THE GATE, AS MEASURED ON THE STEWARD RUNNER');
  console.log('Read from tools/dev-smoke-state.json — steward-runner readings against');
  console.log(`the published mirror. A record, not a bar. Foreground ceiling ${CEILING_S} s.\n`);
  for (const viewport of ['desktop', 'mobile']) {
    const { chosen, missing } = cover(groups, viewport, ALL);
    const total = chosen.reduce((a, g) => a + g.median, 0);
    console.log(`  ${viewport}`);
    for (const g of chosen.sort((a, b) => a.parts[0] - b.parts[0])) {
      const flag = g.parts.length > 1 ? '  (one reading of the group, not of each part)' : '';
      const era = g.renumbered ? ' †' : '';
      console.log(`    part ${stageArg(g.parts).padEnd(5)} ${fmt(g.median).padStart(8)}   n=${g.n}${era}${flag}`);
    }
    if (missing.length) console.log(`    no reading at all for part(s) ${stageArg(missing)}`);
    console.log(`    ${'measured total'.padEnd(11)} ${fmt(total).padStart(8)}   over ${chosen.length} command(s)`
      + (missing.length ? `, and ${missing.length} part(s) unmeasured` : ''));
    console.log('');
  }
  const both = ['desktop', 'mobile'].reduce((a, v) => a + cover(groups, v, ALL).chosen.reduce((x, g) => x + g.median, 0), 0);
  console.log(`  BOTH VIEWPORTS, EVERY PART: ${fmt(both)}`);
  console.log('  † renumbered from a reading filed before the T-0346 cut (2026-08-30).');
  console.log('');
  console.log('  THE 30-MINUTE CAP T-0170, T-0173 AND T-0181 REASON AGAINST IS NOT THIS');
  console.log(`  MACHINE'S. The gate here costs ${fmt(both)}, and no single command may exceed`);
  console.log(`  ${CEILING_S} s, so a run takes the parts that cover its change: --for <path>…`);
}

function reportFor(paths) {
  const groups = measured();
  const { hits, want, unknown } = partsFor(paths);
  console.log('WHAT YOU CHANGED, AND THE PARTS THAT COVER IT\n');
  for (const h of hits) {
    console.log(`  ${h.path}\n      ${h.none ? 'NO PART' : `parts ${stageArg(h.parts)}`} — ${h.why}`);
  }
  if (!want.length) {
    // Every path was a NONE row. The scene did not change, so no part of the
    // body has anything to say about it — but boot, the page-error check and
    // the vendor checks are taken in every invocation, so one cheap staged
    // pass per viewport still proves the page comes up clean.
    console.log('\n  NO PART OF THE SMOKE BODY READS ANY OF THIS. check.sh is the gate that');
    console.log('  covers it. Take the always-on scaffolding anyway — boot, the page-error');
    console.log('  check and the vendor checks run in EVERY invocation:\n');
    const groups = measured();
    for (const viewport of ['mobile', 'desktop']) {
      const { cmds } = recipe(groups, viewport, [cheapestPart(groups, viewport)]);
      const c = cmds[0];
      console.log(`    SMOKE_VIEWPORT=${viewport} SMOKE_STAGE=${stageArg(c.parts)} node tools/smoke_renderer.mjs --published`
        + `\n        ≈ ${fmt(c.secs)} measured, the cheapest part of that viewport`);
    }
    console.log('');
    console.log('  A staged run is NOT the gate and says so on its first line.');
    return;
  }
  console.log(`\n  parts to run: ${stageArg(want)}`
    + (unknown ? `  (${unknown} path(s) not in the map, so the whole gate)` : ''));
  console.log('\n  RUN, from chicago/4d/ (each command packed under the foreground ceiling):\n');
  for (const viewport of ['mobile', 'desktop']) {
    const { cmds, estimated } = recipe(groups, viewport, want);
    for (const c of cmds) {
      console.log(`    SMOKE_VIEWPORT=${viewport} SMOKE_STAGE=${stageArg(c.parts)} node tools/smoke_renderer.mjs --published`
        + `\n        ≈ ${fmt(c.secs)} measured, ${fmt(CEILING_S - c.secs)} of margin`);
    }
    if (estimated.length) {
      console.log(`    (part ${stageArg(estimated.filter((p) => want.includes(p)))} has no reading of its own; `
        + 'priced at the mean of those that do)');
    }
  }
  console.log('\n  A staged run is NOT the gate and says so on its first line. The gate is');
  console.log('  both viewports, every part — see the cost of that with no arguments.');
  console.log('  File what you ran: node tools/dev-smoke-state.mjs record <log>');
  console.log('  And redirect to a FILE, not a pipe: node block-buffers stdout to a pipe,');
  console.log('  so a piped smoke log stays at zero bytes until the process exits — which');
  console.log('  is how a run at 41 minutes was killed one minute from its finish (T-0235).');
}

function selfTest() {
  const fails = [];
  const smoke = fs.readFileSync(SMOKE, 'utf8');
  const m = /^const PARTS = (\d+);$/m.exec(smoke);
  if (!m) fails.push('cannot find `const PARTS = N;` in tools/smoke_renderer.mjs');
  else if (Number(m[1]) !== PARTS) fails.push(`smoke_renderer.mjs has PARTS=${m[1]}, this map is built for ${PARTS}`);

  const seen = new Set();
  for (const [pat, parts, why] of COVERAGE) {
    // An empty row is deliberate — NONE — and must say why in the same breath.
    if (!parts.length && !why) fails.push(`${pat}: maps to no part and gives no reason`);
    for (const p of parts) {
      if (!Number.isInteger(p) || p < 1 || p > PARTS) fails.push(`${pat}: part ${p} is not 1..${PARTS}`);
      seen.add(p);
    }
    if (!why) fails.push(`${pat}: no reason given`);
    // `site/chicago/4d/` is the published mirror and lives at the repo root;
    // every other pattern is relative to chicago/4d/.
    const target = pat.startsWith('site/') ? path.join(REPO, pat) : path.join(APP, pat);
    if (!fs.existsSync(target)) fails.push(`${pat}: no such path in the tree — the map has rotted`);
  }
  for (const p of ALL) if (!seen.has(p)) fails.push(`part ${p} is covered by no row of the map`);

  // The map may only ever ADD parts: an unknown path is the whole gate.
  const unknown = partsFor(['renderers/web/js/no-such-module-at-all.js']);
  if (unknown.want.length !== PARTS) fails.push('an unknown path must map to the whole gate, not to a subset');

  // The renumbering is the one piece of arithmetic here, so assert it directly.
  const old = (parts, when) => currentParts({ parts, takenAt: when });
  const before = '2026-08-29T12:00:00Z';
  const after = '2026-08-30T12:00:00Z';
  const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  if (!eq(old([3], before), [3])) fails.push('old part 3 must renumber to 3');
  if (!eq(old([4], before), [4, 5, 6])) fails.push('old part 4 must renumber to 4,5,6');
  if (!eq(old([5], before), [7])) fails.push('old part 5 must renumber to 7');
  if (!eq(old([7, 8, 9], before), [9, 10, 11])) fails.push('old parts 7-9 must renumber to 9-11');
  if (!eq(old([4], after), [4])) fails.push('a reading filed after the cut must not be renumbered');

  if (!eq(stageArg([1, 2, 3, 5, 7, 8]), '1-3,5,7-8')) fails.push('stageArg does not fold contiguous runs');

  // Every group in the record must renumber into current parts.
  for (const g of measured()) {
    if (g.parts.some((p) => p < 1 || p > PARTS)) fails.push(`a reading renumbers outside 1..${PARTS}: ${key(g.parts)}`);
  }

  if (fails.length) {
    for (const f of fails) console.error(`  FAIL ${f}`);
    console.error(`smoke budget self-test: ${fails.length} failure(s)`);
    process.exit(1);
  }
  console.log(`smoke budget self-test: the map covers all ${PARTS} parts, `
    + `${COVERAGE.length} patterns all exist, the renumbering holds`);
}

const argv = process.argv.slice(2);
if (argv[0] === '--self-test') selfTest();
else if (argv[0] === '--for') reportFor(argv.slice(1));
else if (argv[0] === '--for-diff') {
  const ref = argv[1] || 'origin/dev';
  const out = execFileSync('git', ['diff', '--name-only', `${ref}...HEAD`], { cwd: APP, encoding: 'utf8' });
  const paths = out.split('\n').map((s) => s.trim()).filter((s) => s.startsWith('chicago/4d/') || s.startsWith('site/chicago/4d/'));
  if (!paths.length) console.log(`nothing under chicago/4d/ changed against ${ref}`);
  else reportFor(paths.map((p) => p.replace(/^chicago\/4d\//, '')));
} else if (argv.length && argv[0].startsWith('-')) {
  console.error('usage: smoke_budget.mjs [--for <path>… | --for-diff [ref] | --self-test]');
  process.exit(2);
} else reportCost(measured());
