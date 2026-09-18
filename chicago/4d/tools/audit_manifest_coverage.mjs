#!/usr/bin/env node
/**
 * audit_manifest_coverage.mjs — T-1282. A GATED WRITER BELONGS IN THE MANIFEST.
 *
 * `tools/derived_manifest.json` is what lets pr-lap.sh clear a merge conflict by
 * REBUILDING a generated file instead of picking a side. A tool that check.sh gates with
 * `--check`, and that can also WRITE, is by definition a tool whose output is derived —
 * so if it is not in the manifest, `rederive.mjs --run` never runs it, the lap leaves the
 * branch stale, and the gate goes red with no automated remedy.
 *
 * WHY THIS IS A GATE AND NOT A NOTE (owner, 2026-09-18: "add a note to things to say if
 * you add a writer it should be in that manifest, right?"). A note is what we already had,
 * in the manifest's own preamble, and it did not hold: on the night of 2026-09-17 FOUR
 * separate hand-fixes were needed on this one gap, every one of them a gated writer the
 * manifest had never heard of — derive_resident_roles.py (household cards, hit on four
 * merges), location_spend.py, profile_population_1835.py and model_town_1835.py. Each cost
 * a red PR, a diagnosis and a hand rebuild. The rule is only worth anything if adding a
 * writer and forgetting the manifest FAILS.
 *
 * NOT EVERY GATED WRITER MAY BE LISTED, which is why the answer is an exemption list and
 * not an auto-add. `_must_reproduce` in the manifest names the case: a tool can pass
 * `--check` and still not rebuild to itself, and listing it would let the lap overwrite
 * real content — crosswalk_census_1840_heads.py is the standing example, green on --check
 * while --build rewrote 137 lines. So a tool is either IN the manifest or in
 * `_not_derivable` below WITH A REASON somebody wrote.
 */
import { readFileSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const APP = path.resolve(HERE, '..');
const read = (p) => readFileSync(path.join(APP, p), 'utf8');

/**
 * Gated writers that must NOT be in the manifest, each with the reason. A line here is a
 * decision, not a silencer: it says somebody measured this tool and found that re-running
 * it does not reproduce its committed output, or that its inputs are not in the repository.
 */
const NOT_DERIVABLE = {
  'crosswalk_census_1840_heads.py':
    'Passes --check and still does not rebuild to itself: measured 2026-09-14, --build '
    + 'rewrote 137 lines of census_1840/crosswalk.json and resident_crosswalk.json on a tree '
    + 'the gate called clean. This is the standing example behind the manifest rule '
    + '`_must_reproduce`.',
  'read_newberry_index.py':
    'Needs OCR shards that live outside the repository. Invoked bare it prints its usage and '
    + 'exits 0, writing nothing — the failure mode `_must_actually_write` was written for.',
};

const check = read('tools/check.sh');
const manifest = read('tools/derived_manifest.json');

// A tool the gate runs with --check, paired with a mode that writes.
const gated = new Set([...check.matchAll(/python3 tools\/([a-z0-9_]+\.py) --check/g)].map((m) => m[1]));
const WRITE_MODE = /(?:^|\n)\s*(?:if\s+)?["']--(?:build|write)["']/;

const missing = [];
for (const tool of [...gated].sort()) {
  let src;
  try { src = read(`tools/${tool}`); } catch { continue; }
  if (!WRITE_MODE.test(src)) continue;                 // a checker with no write mode
  if (manifest.includes(`tools/${tool}`)) continue;     // listed
  if (NOT_DERIVABLE[tool]) continue;                    // exempted, in writing
  missing.push(tool);
}

if (missing.length) {
  console.error('manifest coverage: MISSING.\n');
  console.error(`${missing.length} tool(s) are gated by check.sh with --check and can WRITE,`);
  console.error('but are in neither tools/derived_manifest.json nor this file\'s exemption list:\n');
  for (const t of missing) console.error(`  tools/${t}`);
  console.error('\nA gated writer the manifest has never heard of is one `rederive.mjs --run`');
  console.error('never runs, so the lap leaves every open PR stale and its gate goes red with');
  console.error('no automated remedy. Add it to the manifest — measuring first that --build or');
  console.error('--write REPRODUCES the committed output on a clean tree, which is the rule');
  console.error('`_must_reproduce` — or, if it does not reproduce, add it to NOT_DERIVABLE in');
  console.error('this file with the measurement that says why.\n');
  process.exit(1);
}

console.log(`manifest coverage: OK — every gated writer is listed or exempted `
  + `(${gated.size} gated tool(s), ${Object.keys(NOT_DERIVABLE).length} exempted in writing)`);
