#!/usr/bin/env node
/**
 * T-0100 — a street's geometry confidence reaches the picture.
 *
 * `streets.js` grades a ribbon by the WEAKEST grade on anything that decides
 * what it is or where it runs. Until T-0100 it read only `surface_confidence`
 * and `wear_confidence`, and never `geometry_confidence` — the field that says
 * whether the LINE was traced, inferred or invented. A street whose route was
 * invented but whose surface and wear were attested would have drawn at full
 * confidence, and turning `reconstructed` off would have left the invention
 * standing.
 *
 * WHY THIS TEST SLICES THE SOURCE INSTEAD OF IMPORTING IT. `addRecord` is not
 * exported and `streets.js` pulls in three, which will not load headless. The
 * alternative — copying the expression into the test — would let the shipped
 * one drift away from the tested one silently, which is the failure mode this
 * ticket is about in the first place. So the expression is EXTRACTED from
 * `renderers/web/js/streets.js` and evaluated, the same way
 * `tools/measure_rank_bias.mjs` takes its primitives out of `flora.js`. Every
 * extraction is guarded: if the shape moves, this file fails loudly rather than
 * testing a stale copy of itself.
 *
 *   node tools/test_street_confidence.mjs
 *
 * Exit 0 on pass, 1 on any failed check, 2 if the source could not be read the
 * way this test needs to read it (drift).
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'renderers/web/js/streets.js');
const INDEX = join(ROOT, 'data/sidecars/1835/index.json');

const src = readFileSync(SRC, 'utf8');

function drift(msg) {
  console.error(`DRIFT — ${msg}`);
  console.error(`  ${SRC} no longer has the shape this test reads it with.`);
  console.error('  Fix the test against the source; do NOT weaken the checks.');
  process.exit(2);
}

/* ---- the shipped LEVEL map -------------------------------------------- */

const levelMatch = /^const LEVEL = (\{[^}]*\});/m.exec(src);
if (!levelMatch) drift('cannot find `const LEVEL = { ... };`');
let LEVEL;
try {
  LEVEL = Function(`"use strict"; return (${levelMatch[1]});`)();
} catch (e) {
  drift(`the LEVEL literal did not evaluate: ${e.message}`);
}
for (const k of ['attested', 'inferred', 'reconstructed']) {
  if (typeof LEVEL[k] !== 'number') drift(`LEVEL is missing the grade \`${k}\``);
}

/* ---- the shipped confidence expression --------------------------------- */

// Deliberately anchored on `const confidence = Math.max(` inside addRecord and
// closed on the first `);` — the expression is a single call and nothing else
// in this file opens one that way.
const confMatch = /const confidence = Math\.max\(\s*([\s\S]*?)\s*\);/.exec(src);
if (!confMatch) drift('cannot find `const confidence = Math.max( ... );`');

const terms = confMatch[1]
  .split('\n')
  .map((s) => s.trim().replace(/,$/, ''))
  .filter(Boolean);
if (!terms.length) drift('the confidence expression has no terms');

// The point of the ticket: the expression must actually consult the line's own
// grade. Without this guard the test would happily pass on the old two-term
// version and report the bug fixed.
if (!confMatch[1].includes('geometry_confidence')) {
  drift('the confidence expression does not read `geometry_confidence` — T-0100 is not fixed');
}

function evalTerms(termList, record) {
  return Math.max(
    ...termList.map((t) =>
      Function('LEVEL', 'record', `"use strict"; return (${t});`)(LEVEL, record),
    ),
  );
}

const shipped = (record) => evalTerms(terms, record);

// The pre-T-0100 expression, rebuilt from the shipped terms by dropping the
// geometry one. This is the positive control: every case below is also run
// through it, and the case the ticket describes MUST come out differently.
const oldTerms = terms.filter((t) => !t.includes('geometry_confidence'));
if (oldTerms.length !== terms.length - 1) {
  drift(`expected exactly one geometry term, found ${terms.length - oldTerms.length}`);
}
const before = (record) => evalTerms(oldTerms, record);

/* ---- the checks -------------------------------------------------------- */

let failed = 0;
const ok = (cond, label) => {
  console.log(`  ${cond ? 'ok  ' : 'FAIL'}  ${label}`);
  if (!cond) failed++;
};

const rec = (geometry, surface, wear) => ({
  geometry_confidence: geometry,
  surface_confidence: surface,
  wear_confidence: wear,
});

const INVENTED = LEVEL.reconstructed;
const ATTESTED = LEVEL.attested;

console.log('\n[1m== a street\'s geometry confidence reaches the picture (T-0100)[0m');

// The ticket's case, stated as the ticket states it.
const inventedLine = rec('reconstructed', 'attested', 'attested');
ok(shipped(inventedLine) === INVENTED,
  `an invented LINE under an attested surface dithers out — ${shipped(inventedLine)} of ${INVENTED}`);
ok(before(inventedLine) === ATTESTED,
  `  ...and drew at FULL confidence before T-0100 — the bug, reproduced — ${before(inventedLine)}`);
ok(shipped(inventedLine) !== before(inventedLine),
  '  ...so this test distinguishes the fix from the fault');

// An inferred line grades as inferred, not rounded to either end.
const inferredLine = rec('inferred', 'attested', 'attested');
ok(shipped(inferredLine) === LEVEL.inferred,
  `an inferred line grades inferred, not attested — ${shipped(inferredLine)}`);

// Fully attested stays fully attested: the new term must not darken a street
// that earned its confidence.
ok(shipped(rec('attested', 'attested', 'attested')) === ATTESTED,
  'a wholly attested street still draws at full confidence');

// The weakest grade wins wherever it sits, which is the rule the layer states.
ok(shipped(rec('attested', 'attested', 'reconstructed')) === INVENTED,
  'an invented WEAR still dominates an attested line — the old behaviour is kept');
ok(shipped(rec('reconstructed', 'reconstructed', 'reconstructed')) === INVENTED,
  'all three invented is invented');

// A record with no geometry grade must fall to the conservative end rather than
// silently reading as attested.
ok(shipped({ surface_confidence: 'attested', wear_confidence: 'attested' }) === INVENTED,
  'a record with NO geometry grade is treated as invented, not as attested');

/* ---- and the shipped town does not move -------------------------------- */

// The comment in streets.js claims this change moves no pixel today. That is a
// claim about the data, so it is measured here rather than asserted, and it
// will start failing the day the data makes it false — which is the day the
// fix begins to matter.
const index = JSON.parse(readFileSync(INDEX, 'utf8'));
const streets = index.streets ?? [];
ok(streets.length > 0, `the shipped index carries street records — ${streets.length}`);

const missing = streets.filter((r) => !('geometry_confidence' in r));
ok(missing.length === 0,
  `every shipped street record carries a geometry grade — ${streets.length - missing.length} of ${streets.length}`);

const moved = streets.filter((r) => shipped(r) !== before(r));
ok(moved.length === 0,
  `no shipped street changes grade under the fix — ${moved.length} moved of ${streets.length}`
  + (moved.length ? ` (${moved.slice(0, 3).map((r) => r.id).join(', ')})` : ''));
if (moved.length) {
  // This one is a TRIPWIRE, not a regression. It fires the day a street's
  // surface and wear are graded better than its line — which is the day T-0100
  // stops being theoretical and starts changing the picture. Nothing here is
  // broken: the claim in streets.js that this term "moves no pixel today" has
  // simply expired, and the right repair is to update that comment in the same
  // commit as the data, the way a banked baseline is dropped by the commit that
  // repaired it. Do not revert the geometry term to silence this.
  console.log('  note  this is the tripwire, not a regression — the fix has begun to matter.');
  console.log('        Update the "degenerate in the present dataset" note in streets.js');
  console.log('        in the same commit as the data change, then re-run.');
  for (const r of moved) {
    console.log(`        ${r.id}: geometry ${r.geometry_confidence}, surface ${r.surface_confidence},`
      + ` wear ${r.wear_confidence} — ${before(r)} → ${shipped(r)}`);
  }
}

const pinned = streets.filter((r) => before(r) === INVENTED).length;
console.log(`  note  ${pinned} of ${streets.length} are already pinned at ${INVENTED} by surface or wear,`);
console.log('        which is WHY nothing moves — a coincidence of the data, not of the layer.');

console.log(failed ? `\n[31mSTREET CONFIDENCE FAIL[0m — ${failed} check(s)` : '\n[32mSTREET CONFIDENCE PASS[0m');
process.exit(failed ? 1 : 0);
