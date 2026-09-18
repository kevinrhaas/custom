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
 * T-1302. THE INVENTORY REPLACED THE PATTERN, BECAUSE NO PATTERN WAS RIGHT.
 *
 * This audit used to answer "can this tool write?" by matching its SOURCE. Every version
 * of that test is wrong, and each was measured on 2026-09-18 against the real tree:
 *
 *   anchored to a line start (as shipped)  found  0 unlisted writers
 *   widened bluntly                        found 59 — but EIGHT of those declare no write
 *                                                mode at all and matched the string
 *                                                `--build` inside their own prose;
 *                                                carry_stage_blocks.py has only --check
 *   matching a DECLARED flag only          found 52 — and misses read_fergus_1839.py,
 *                                                which has no --build, and WRITES BY
 *                                                DEFAULT when the argument is neither
 *                                                --check nor --self-test
 *
 * A tool's write mode is sometimes its default branch, so no reading of the source can
 * answer the question. Behaviour can: run it on a clean tree and ask git what moved. That
 * is far too slow for a per-commit gate — and it does not need to run per commit, because
 * the answer only changes when a TOOL changes. So the measurement is committed, with a
 * date beside every row, in tools/writer_inventory.json, and this gate holds the tree to
 * it: a gated tool with no measured row fails here. That is what stops a new writer
 * arriving unmeasured, which is the hole the ticket was filed for.
 */
const check = read('tools/check.sh');
const manifest = read('tools/derived_manifest.json');
const inventory = JSON.parse(read('tools/writer_inventory.json'));
const INV = inventory.tools;

// A tool is LISTED when a step RUNS it, not when a note MENTIONS it. The substring test
// this replaces read `tools/read_newberry_index.py` out of another step's prose and
// called it listed — the one tool the old exemption list existed to keep out.
const manifestTools = new Set(
  JSON.parse(manifest).steps.flatMap((step) => step.command
    .filter((a) => /^tools\/[a-z0-9_]+\.py$/.test(a))
    .map((a) => a.replace(/^tools\//, ''))));

const gated = new Set([...check.matchAll(/python3 tools\/([a-z0-9_]+\.py) --check/g)].map((m) => m[1]));

const unmeasured = [];
const disagree = [];
for (const tool of [...gated].sort()) {
  const row = INV[tool];
  if (!row) { unmeasured.push(tool); continue; }
  const listed = manifestTools.has(tool);
  if (row.placement === 'manifest' && !listed) {
    disagree.push(`${tool} — the inventory says 'manifest'; the manifest does not run it`);
  } else if (row.placement !== 'manifest' && listed) {
    disagree.push(`${tool} — the manifest runs it; the inventory says '${row.placement}'`);
  }
}

if (unmeasured.length || disagree.length) {
  console.error('manifest coverage: MISSING.\n');
  if (unmeasured.length) {
    console.error(`${unmeasured.length} tool(s) are gated with --check and have NO measured row`);
    console.error('in tools/writer_inventory.json:\n');
    for (const t of unmeasured) console.error(`  tools/${t}`);
    console.error('\nMEASURE IT; DO NOT READ ITS SOURCE — the note above says why that cannot');
    console.error('work. Run its write mode on a clean tree, or run it BARE if it declares no');
    console.error('flag, and record what git says moved:');
    console.error('  wrote its own outputs and changed no committed byte  -> reproduces');
    console.error('  changed a committed byte                             -> not_derivable, WITH THE NUMBER');
    console.error('  wrote nothing, and it HAS a write flag               -> perturb it before deciding');
    console.error('  wrote nothing, run bare                              -> not_a_writer\n');
  }
  if (disagree.length) {
    console.error('The inventory and the manifest disagree:\n');
    for (const d of disagree) console.error(`  ${d}`);
    console.error('');
  }
  process.exit(1);
}

const by = (p) => Object.values(INV).filter((r) => r.placement === p).length;
console.log(`manifest coverage: OK — ${gated.size} gated tool(s), every one measured.`);
console.log(`  ${by('manifest')} in the manifest · ${by('pending')} measured to reproduce and not yet placed`);
console.log(`  ${by('not_derivable')} cannot rebuild, each with its number · ${by('not_a_writer')} write nothing`);
if (by('pending')) {
  console.log('  The pending ones are recorded, not hidden. Ordering is its own measured pass:');
  console.log('  on #1452 three reconstruction stages OSCILLATED until they sat in the right');
  console.log('  slot, so these cannot be appended to the manifest blind (T-1302 batch 2).');
}
