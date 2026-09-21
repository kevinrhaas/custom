#!/usr/bin/env node
/**
 * rederive.mjs — run the derived research layer's rebuild sequence, and answer
 * whether a given conflict may be cleared by doing so.
 *
 * WHY THIS EXISTS (owner, 2026-09-10). With PR #1058 the PR lap could merge for
 * the first time, and every open PR promptly came back LEFT ALONE for a REAL
 * CONFLICT. Every conflicting file was a tool output that two runs had each
 * re-derived — seven directory crosswalks on one PR, the land-sale crosswalk and
 * spend and identity_master on another, the scene sidecar and the audit workbook
 * on a third. Not one of them was a disagreement about the town.
 *
 * `.github/steward/pr-lap.sh` already draws exactly the right line for this:
 *
 *   "A conflict here is never resolved by hand: the merge takes either side to
 *    clear the marker and the tool then rewrites the file from source."
 *
 * It just drew it around five bookkeeping files. This widens it to the derived
 * research layer, and the widening is a LIST rather than a pattern, so what is
 * in scope can be read off `tools/derived_manifest.json` by anyone.
 *
 * THE SAFETY PROPERTY, and it is worth being exact about, because this is a tool
 * that resolves merges in research data:
 *
 *   1. A path not named in the manifest is refused, exactly as before.
 *   2. A path whose file declares `hand_authored: true` is refused even if named
 *      — `--check` fails if the manifest ever lists one.
 *   3. Resolving is only ever "take either side, then rebuild from the inputs".
 *      Nothing here merges two versions of anything.
 *   4. `tools/check.sh` is the proof, and it runs AFTER this. check.sh is what
 *      asserts each of these files re-derives; a wrong entry here makes the gate
 *      red, and the lap does not push a red tree. The worst case is a PR that
 *      stays open — the state it was already in — never a bad merge onto dev.
 *
 * THE ORDER IS LOAD-BEARING, and was learned on PR #1055: crosswalks before the
 * spends that read them, consolidate after all of them, and mint_civic_residents
 * AFTER consolidate, because consolidate moves the inputs mint reads. Built in
 * the wrong order mint still differed on two cards and only converged when re-run.
 *
 * AND ONE ORDER IS NOT ENOUGH (T-1363, measured on #1495). A step can READ a file
 * a LATER step rebuilds, and re-ordering cannot fix that when the later step
 * derives from the layer the earlier one writes into — it is a two-cycle, and
 * `steps` is a linear order. The arrival stage draws from
 * data/reconstruction/1835_town_model.json; model_town_1835.py rebuilds that model
 * out of the population the stage helped move; so any run that moved the town left
 * ~1,200 arrival draws a pass behind and the gate went red on them. A second whole
 * `--run` did not help — it moved the model again. So the manifest DECLARES the
 * short tail that converges it (`second_pass`), `--run` runs it, and the callers
 * — pr-lap.sh and pr-stuck.sh — get convergence without knowing any of this.
 *
 *   node tools/rederive.mjs --check                 the manifest is well-formed
 *   node tools/rederive.mjs --resolvable <paths…>   may these conflicts be cleared?
 *   node tools/rederive.mjs --run                   run the sequence, then the second pass
 *   node tools/rederive.mjs --second-pass           run ONLY the declared second pass
 *   node tools/rederive.mjs --prove                 does every step write what it claims?
 *   node tools/rederive.mjs --self-test
 */
import { readFileSync, existsSync, statSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const APP = path.resolve(HERE, '..');
const REPO = path.resolve(APP, '..', '..');
const MANIFEST = path.join(HERE, 'derived_manifest.json');

const argv = process.argv.slice(2);
const has = (n) => argv.includes(`--${n}`);
const rest = () => argv.filter((a) => !a.startsWith('--'));

const load = (file = MANIFEST) => JSON.parse(readFileSync(file, 'utf8'));

/**
 * Repo-relative, whatever the caller passed.
 *
 * REPO-RELATIVE IS TRIED FIRST, and that is not arbitrary: `git diff
 * --diff-filter=U` prints repo-relative paths and pr-lap.sh hands them straight
 * here, but the manifest's commands run with cwd = chicago/4d, so a bare
 * cwd-relative resolve turned `chicago/4d/data/…` into
 * `chicago/4d/chicago/4d/data/…` and every path fell through as "not in the
 * manifest". Refusing everything is the SAFE direction, which is exactly why it
 * would have gone unnoticed: the lap would have kept leaving PRs alone and this
 * file would have looked like it simply never matched.
 */
function normalise(p) {
  if (!p.startsWith('/') && existsSync(path.join(REPO, p))) {
    return path.relative(REPO, path.join(REPO, p)).split(path.sep).join('/');
  }
  const abs = path.resolve(p.startsWith('/') ? p : path.join(process.cwd(), p));
  return path.relative(REPO, abs).split(path.sep).join('/');
}

/** Does this file declare itself hand-authored? A judgement is not a derivation. */
function handAuthored(rel) {
  const abs = path.join(REPO, rel);
  if (!existsSync(abs) || !rel.endsWith('.json')) return false;
  try { return load(abs).hand_authored === true; } catch { return false; }
}

const allResolved = (m) => m.steps.flatMap((s) => s.resolves ?? []);
const cmdline = (cmd) => (cmd ?? []).join(' ');
const secondPass = (m) => m.second_pass ?? [];

/* ------------------------------------------------------------------- check */

function check(m = load()) {
  const problems = [];
  const seen = new Map();
  // THE INVARIANT THAT MAKES THE BACKSTOP REAL (see the manifest's own
  // `_only_gated_tools`). check.sh is what proves a rebuild was right; a tool
  // check.sh never asks `--check` of has no such proof, so re-running it can
  // destroy a committed file and leave the gate green.
  const gate = existsSync(path.join(APP, 'tools', 'check.sh'))
    ? readFileSync(path.join(APP, 'tools', 'check.sh'), 'utf8') : '';

  m.steps.forEach((s, i) => {
    const at = `step ${i + 1} (${(s.command ?? []).join(' ')})`;
    if (!Array.isArray(s.command) || s.command.length < 2) {
      problems.push(`${at}: command must be an argv array`);
      return;
    }
    const script = path.join(APP, s.command[1]);
    if (!existsSync(script)) problems.push(`${at}: ${s.command[1]} does not exist`);
    else if (gate && !new RegExp(`${s.command[1].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^\\n]*--check`).test(gate)) {
      problems.push(`${at}: tools/check.sh never runs ${s.command[1]} with --check, so nothing `
        + 'asserts its output re-derives. An ungated derivation may not resolve a conflict — '
        + 'gate the tool first, or leave the conflict for the run that owns the ticket.');
    }
    if (!Array.isArray(s.resolves)) problems.push(`${at}: resolves must be an array (use [] for a rebuild-only step)`);

    for (const rel of s.resolves ?? []) {
      if (rel !== normalise(path.join(REPO, rel))) problems.push(`${at}: ${rel} is not a clean repo-relative path`);
      // A path claimed by two steps means the later one silently wins, and which
      // one that is depends on the order — exactly the ambiguity this file exists
      // to remove.
      if (seen.has(rel)) problems.push(`${at}: ${rel} is also resolved by ${seen.get(rel)} — one owner per file`);
      seen.set(rel, at);
      if (!existsSync(path.join(REPO, rel))) problems.push(`${at}: ${rel} is listed but does not exist in the tree`);
      if (handAuthored(rel)) {
        problems.push(`${at}: ${rel} declares hand_authored — a judgement is not a derivation `
          + 'and a tool may not rewrite it. Remove it from the manifest.');
      }
    }
  });

  // THE SECOND PASS EARNS ITS PLACE OR IT IS REFUSED (T-1363). Two properties, and
  // both matter for a different reason:
  //
  //   Every entry's command must BE one of the steps. That is what keeps
  //   `_only_gated_tools` true here for free — the second pass can never reach a
  //   tool check.sh has not gated, because it can never reach a tool the sequence
  //   does not already run. It also means the pass resolves no conflicts of its
  //   own: resolution stays the steps' business.
  //
  //   Every entry must say what went stale UNDERNEATH it, and be right about it.
  //   `stale_on` names files a LATER step rebuilds; `stale_on_pass` names an
  //   earlier entry in this list whose outputs it reads. A `stale_on` path that is
  //   only ever rebuilt ABOVE the step has no lag to fix, and an entry with no
  //   reason at all is how a second pass turns into a superstition somebody
  //   lengthens whenever a gate goes red.
  const byCommand = new Map(m.steps.map((s, i) => [cmdline(s.command), i]));
  const resolvedAt = new Map();
  m.steps.forEach((s, i) => { for (const rel of s.resolves ?? []) resolvedAt.set(rel, i); });
  const passSeen = new Map();

  secondPass(m).forEach((e, k) => {
    const line = cmdline(e.command);
    const at = `second pass ${k + 1} (${line})`;
    if (!Array.isArray(e.command) || e.command.length < 2) {
      problems.push(`${at}: command must be an argv array`);
      return;
    }
    if (!byCommand.has(line)) {
      problems.push(`${at}: no step in the sequence runs this command. A second-pass entry `
        + 'must name a step verbatim — that is what keeps it to tools check.sh gates. '
        + 'Add the step first, or fix the argv to match it exactly.');
      return;
    }
    if (passSeen.has(line)) {
      problems.push(`${at}: already run by ${passSeen.get(line)} — one slot per command`);
      return;
    }
    const step = byCommand.get(line);
    for (const rel of e.stale_on ?? []) {
      if (!resolvedAt.has(rel)) {
        problems.push(`${at}: stale_on ${rel} is rebuilt by no step, so re-running cannot `
          + 'have been what moved it. Name a file the sequence writes, or drop the entry.');
      } else if (resolvedAt.get(rel) < step) {
        problems.push(`${at}: stale_on ${rel} is rebuilt at step ${resolvedAt.get(rel) + 1}, `
          + `ABOVE step ${step + 1} — the sequence already hands it over fresh and there is no `
          + 'lag here to fix. An entry that re-runs for no measured reason does not belong.');
      }
    }
    for (const ref of e.stale_on_pass ?? []) {
      if (!passSeen.has(ref)) {
        problems.push(`${at}: stale_on_pass names \`${ref}\`, which is not an EARLIER entry in `
          + 'this list. A pass runs top to bottom, so a dependency below it has not run yet.');
      }
    }
    if ((e.stale_on ?? []).length === 0 && (e.stale_on_pass ?? []).length === 0) {
      problems.push(`${at}: says nothing about what went stale underneath it. State it in `
        + 'stale_on (a file a later step rebuilds) or stale_on_pass (an earlier entry here).');
    }
    passSeen.set(line, at);
  });

  if (problems.length) {
    console.error('derived manifest FAILED:');
    for (const p of problems) console.error(`  - ${p}`);
    return 1;
  }
  console.log(`derived manifest OK — ${m.steps.length} step(s), ${allResolved(m).length} `
    + `resolvable file(s), none hand-authored; ${secondPass(m).length} step(s) declared `
    + 'for the second pass');
  return 0;
}

/* ------------------------------------------------------- resolvable? */

/**
 * The question pr-lap.sh asks. EVERY path must be covered, or the answer is no:
 * clearing some conflicts and leaving others would leave the merge half-done and
 * the markers in the tree.
 */
function resolvable(paths, m = load()) {
  const covered = new Set(allResolved(m));
  const unknown = [];
  const refused = [];
  for (const raw of paths) {
    const rel = normalise(raw);
    if (handAuthored(rel)) refused.push(`${rel} (declares hand_authored)`);
    else if (!covered.has(rel)) unknown.push(rel);
  }
  if (unknown.length === 0 && refused.length === 0) {
    console.log(`all ${paths.length} conflicting file(s) are rebuilt from source by the manifest`);
    return 0;
  }
  console.error('these conflicts are NOT the manifest\'s to clear:');
  for (const u of refused) console.error(`  - ${u}`);
  for (const u of unknown) console.error(`  - ${u} (not in tools/derived_manifest.json)`);
  console.error('\nThey want the run that owns the ticket. Add a file here only when a tool');
  console.error('rewrites it from its inputs and check.sh asserts that it does.');
  return 1;
}

/* -------------------------------------------------------------------- run */

/** Run one command from the manifest, reporting the tail of its output if it fails. */
function invoke(command, tag) {
  const line = cmdline(command);
  process.stdout.write(`  ${tag} ${line}\n`);
  try {
    execFileSync(command[0], command.slice(1), { cwd: APP, stdio: ['ignore', 'pipe', 'pipe'] });
    return true;
  } catch (e) {
    console.error(`  FAILED: ${line}`);
    console.error(`${e.stdout ?? ''}${e.stderr ?? ''}`.split('\n').slice(-8).map((l) => `    ${l}`).join('\n'));
    return false;
  }
}

/**
 * THE DECLARED SECOND PASS (T-1363). Short by construction — every entry has to
 * name a step and say what moved underneath it — and it runs in the order the
 * manifest lists, which is NOT the order those steps sit in `steps`.
 */
function runSecondPass(m = load()) {
  const pass = secondPass(m);
  if (!pass.length) return 0;
  console.log(`  — the declared second pass: ${pass.length} step(s) that read what the `
    + 'sequence rebuilt after them');
  for (const [k, e] of pass.entries()) {
    if (!invoke(e.command, `[2nd ${k + 1}/${pass.length}]`)) return 1;
  }
  return 0;
}

function run(m = load()) {
  for (const [i, s] of m.steps.entries()) {
    if (!invoke(s.command, `[${i + 1}/${m.steps.length}]`)) return 1;
  }
  if (runSecondPass(m) !== 0) return 1;
  console.log(`derived layer rebuilt — ${m.steps.length} step(s) in dependency order, then `
    + `${secondPass(m).length} declared second-pass step(s)`);
  return 0;
}

/* ------------------------------------------------------------------ prove */

/**
 * DOES EACH STEP ACTUALLY WRITE WHAT IT CLAIMS? The one thing `--check` cannot
 * see by reading the manifest, and the one that bit.
 *
 * read_newberry_index.py was listed here as the rebuild for leads.json. Invoked
 * bare it PRINTS ITS USAGE AND EXITS 0 — it writes nothing at all, because
 * rebuilding that file needs `--parse` over OCR shards kept outside the repo.
 * The entry passed `--check` (the tool is gated), passed an idempotency test
 * (nothing changed, because nothing ran) and passed a full-sequence run. It
 * failed only when a real merge needed it, hours later, as `leads.json does not
 * re-derive from its inputs`.
 *
 * The idempotency test that missed it ran the tool under `timeout 400` with its
 * output suppressed, so a tool killed at 400 seconds and a tool that did nothing
 * looked exactly alike. This asks the question that separates them: run the
 * command, and require every file it claims to resolve to have been WRITTEN.
 * mtime rather than content, because a correct rebuild of an unchanged tree
 * produces identical bytes — "the file did not change" is the expected result
 * and proves nothing either way.
 */
function prove(m = load()) {
  const stamp = (rel) => { try { return statSync(path.join(REPO, rel)).mtimeMs; } catch { return null; } };
  let bad = 0;
  for (const [i, s] of m.steps.entries()) {
    const label = s.command.join(' ');
    const before = new Map((s.resolves ?? []).map((r) => [r, stamp(r)]));
    try {
      execFileSync(s.command[0], s.command.slice(1), { cwd: APP, stdio: ['ignore', 'pipe', 'pipe'] });
    } catch (e) {
      console.error(`  [${i + 1}] FAILED to run: ${label}`);
      bad += 1;
      continue;
    }
    const untouched = [...before.keys()].filter((r) => stamp(r) === before.get(r));
    if (untouched.length) {
      console.error(`  [${i + 1}] ${label}`);
      console.error('        claims to rebuild file(s) it did not write:');
      for (const u of untouched) console.error(`          ${u}`);
      bad += 1;
    } else if ((s.resolves ?? []).length) {
      console.log(`  [${i + 1}] ok — ${label} wrote all ${s.resolves.length} of its file(s)`);
    } else {
      console.log(`  [${i + 1}] ok — ${label} (rebuild only, resolves nothing)`);
    }
  }
  if (bad) {
    console.error(`\nderived manifest: ${bad} step(s) do not write what they claim.`);
    console.error('A command that writes nothing leaves the lap taking `--ours` on a file it');
    console.error('then cannot rebuild, and the gate goes red where a plain refusal would');
    console.error('have been clearer. Remove the step, or give it the arguments that write.');
    return 1;
  }
  console.log(`\nderived manifest: all ${m.steps.length} step(s) write what they claim`);
  return 0;
}

/* -------------------------------------------------------------- self-test */

async function selfTest() {
  const { mkdtempSync, writeFileSync, rmSync, mkdirSync } = await import('node:fs');
  const { tmpdir } = await import('node:os');
  let failures = 0;
  const check_ = (what, ok, detail) => {
    console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${what}${detail ? ` — ${detail}` : ''}`);
    if (!ok) failures += 1;
  };

  const real = load();

  console.log('\n  the manifest that ships');
  check_('is well-formed, and check() passes it', check(real) === 0);
  check_('every step rebuilds at least one thing or says it rebuilds nothing',
    real.steps.every((s) => Array.isArray(s.resolves)));
  check_('the hand-authored file is NOT resolvable',
    resolvable(['chicago/4d/data/research/land_sales/resident_rulings.json'], real) === 1);
  check_('a file nobody derives is NOT resolvable',
    resolvable(['chicago/4d/data/residents/households/hh_taylor_c.json'], real) === 1);
  check_('a file the manifest owns IS resolvable',
    resolvable(['chicago/4d/data/research/land_sales/resident_crosswalk.json'], real) === 0);
  check_('a MIXED set is refused as a whole — half a merge is not a merge',
    resolvable([
      'chicago/4d/data/research/land_sales/resident_crosswalk.json',
      'chicago/4d/data/residents/households/hh_taylor_c.json',
    ], real) === 1);
  check_('mint_civic_residents resolves nothing, because its outputs are resident cards',
    real.steps.find((s) => s.command.join(' ').includes('mint_civic_residents'))?.resolves.length === 0);
  check_('the spends come after the crosswalks they read',
    real.steps.findIndex((s) => s.command.join(' ').includes('spend_land_sales'))
      > real.steps.findIndex((s) => s.command.join(' ').includes('read_land_sales')));
  check_('mint comes after consolidate, which moves the inputs it reads (PR #1055)',
    real.steps.findIndex((s) => s.command.join(' ').includes('mint_civic_residents'))
      > real.steps.findIndex((s) => s.command.join(' ').includes('consolidate_resident_evidence')));

  console.log('\n  the declared second pass (T-1363)');
  const pass = secondPass(real);
  check_('is declared at all — the sequence alone does not converge', pass.length > 0);
  check_('every entry names a step the sequence already runs, so it inherits the gating',
    pass.every((e) => real.steps.some((s) => s.command.join(' ') === e.command.join(' '))));
  check_('the arrival stage is in it — it is the reader in the measured cycle',
    pass.some((e) => e.command.join(' ').includes('attribute_fill_arrival')));
  check_('the arrival entry is stale on the town model, which a LATER step rebuilds',
    (() => {
      const e = pass.find((x) => x.command.join(' ').includes('attribute_fill_arrival'));
      const model = 'chicago/4d/data/reconstruction/1835_town_model.json';
      const writer = real.steps.findIndex((s) => (s.resolves ?? []).includes(model));
      const reader = real.steps.findIndex((s) => s.command.join(' ') === e?.command.join(' '));
      return e?.stale_on?.includes(model) && writer > reader && reader >= 0;
    })());
  check_('the tiers are counted before the profile that reads them — the hand order that converged',
    pass.findIndex((e) => e.command.join(' ').includes('migrate_attribute_tiers'))
      < pass.findIndex((e) => e.command.join(' ').includes('profile_population_1835')));
  check_('model_town is NOT re-run in it — that would put the arrival draws back a pass',
    !pass.some((e) => e.command.join(' ').includes('model_town_1835')));

  console.log('\n  check() refuses a manifest that would be unsafe');
  const tmp = mkdtempSync(path.join(tmpdir(), 'c4d-rederive-'));
  try {
    const bad = (steps, second_pass = []) => {
      const f = path.join(tmp, 'm.json');
      writeFileSync(f, JSON.stringify({ schema: 1, steps, second_pass }));
      return check(load(f));
    };
    check_('a step naming a script that does not exist',
      bad([{ command: ['python3', 'tools/no_such_tool.py'], resolves: [] }]) === 1);
    check_('the SAME file resolved by two steps — one owner per file',
      bad([
        { command: ['python3', 'tools/compile_scene.py'], resolves: ['chicago/4d/data/town_census.json'] },
        { command: ['python3', 'tools/town_census.py'], resolves: ['chicago/4d/data/town_census.json'] },
      ]) === 1);
    check_('a hand-authored file listed as resolvable',
      bad([{
        command: ['python3', 'tools/read_land_sales.py', '--build'],
        resolves: ['chicago/4d/data/research/land_sales/resident_rulings.json'],
      }]) === 1);
    check_('a listed path that is not in the tree',
      bad([{ command: ['python3', 'tools/compile_scene.py'], resolves: ['chicago/4d/data/nope.json'] }]) === 1);

    // AND THE SECOND PASS, which is the part that can quietly grow. Each of these
    // is a way an entry could be added that re-runs a tool for no measured reason.
    const scene = { command: ['python3', 'tools/compile_scene.py', '--all'], resolves: ['chicago/4d/data/town_census.json'] };
    const census = { command: ['python3', 'tools/town_census.py'], resolves: ['chicago/4d/data/residents/index.json'] };
    check_('a second-pass entry naming a command no step runs',
      bad([scene, census], [{ command: ['python3', 'tools/town_census.py', '--build'], stale_on: ['chicago/4d/data/town_census.json'] }]) === 1);
    check_('a second-pass entry stale on a file only an EARLIER step rebuilds',
      bad([scene, census], [{ command: census.command, stale_on: ['chicago/4d/data/town_census.json'] }]) === 1);
    check_('a second-pass entry stale on a file NO step rebuilds',
      bad([scene, census], [{ command: scene.command, stale_on: ['chicago/4d/data/nope.json'] }]) === 1);
    check_('a second-pass entry that says nothing about what went stale',
      bad([scene, census], [{ command: scene.command }]) === 1);
    check_('a second-pass entry depending on one BELOW it, which has not run yet',
      bad([scene, census], [
        { command: scene.command, stale_on_pass: ['python3 tools/town_census.py'] },
        { command: census.command, stale_on: ['chicago/4d/data/residents/index.json'] },
      ]) === 1);
    check_('the same command given two second-pass slots',
      bad([scene, census], [
        { command: scene.command, stale_on: ['chicago/4d/data/residents/index.json'] },
        { command: scene.command, stale_on: ['chicago/4d/data/residents/index.json'] },
      ]) === 1);
    check_('…and the shape all six of those are wrong against IS accepted',
      bad([scene, census], [{ command: scene.command, stale_on: ['chicago/4d/data/residents/index.json'] }]) === 0);
  } finally { rmSync(tmp, { recursive: true, force: true }); }

  console.log(`\n${failures === 0 ? 'rederive self-test: all pass' : `rederive self-test: ${failures} FAILURE(S)`}`);
  return failures === 0 ? 0 : 1;
}

/* ------------------------------------------------------------------- main */

if (has('self-test')) process.exit(await selfTest());
else if (has('resolvable')) process.exit(resolvable(rest()));
else if (has('prove')) process.exit(prove());
else if (has('second-pass')) process.exit(runSecondPass());
else if (has('run')) process.exit(run());
else process.exit(check());
