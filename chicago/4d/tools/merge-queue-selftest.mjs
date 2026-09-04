#!/usr/bin/env node
/**
 * The QUEUE.md merge driver's assertions, and proof they still fire when broken.
 *
 * Every case here is one that actually happened while landing a queue re-rank on
 * 2026-09-04 — four merges, four hand reconciliations. They are the reason the
 * driver exists, so they are the reason it is tested.
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const DRIVER = path.join(HERE, 'merge-queue.mjs');

let pass = 0; let fail = 0;
const ok = (cond, what) => { if (cond) { pass++; console.log(`  ok    ${what}`); } else { fail++; console.log(`  FAIL  ${what}`); } };

/** Run the driver over three versions; returns { code, text }. */
function run(base, ours, theirs) {
  const dir = mkdtempSync(path.join(tmpdir(), 'mq-'));
  const O = path.join(dir, 'base'); const A = path.join(dir, 'ours'); const B = path.join(dir, 'theirs');
  writeFileSync(O, base); writeFileSync(A, ours); writeFileSync(B, theirs);
  let code = 0;
  try {
    execFileSync('node', [DRIVER, O, A, B, 'QUEUE.md'], { stdio: ['ignore', 'ignore', 'ignore'] });
  } catch (e) { code = e.status ?? 1; }
  const text = readFileSync(A, 'utf8');
  rmSync(dir, { recursive: true, force: true });
  return { code, text };
}
const ids = (t) => t.split('\n').map((l) => /^(T-\d{4})\b/.exec(l)?.[1]).filter(Boolean);

const HEAD = '# QUEUE — top is next.\n# --- a band the owner wrote\n';

console.log('\n\x1b[1m== the QUEUE.md merge driver\x1b[0m');

// 1. The everyday case: they closed one, we did nothing to it.
{
  const base = HEAD + 'T-0001 — a\nT-0002 — b\nT-0003 — c\n';
  const ours = base;
  const theirs = HEAD + 'T-0001 — a\nT-0003 — c\n';
  const r = run(base, ours, theirs);
  ok(r.code === 0, 'a ticket they closed is dropped');
  ok(!ids(r.text).includes('T-0002'), '...and it is really gone');
  ok(ids(r.text).join() === 'T-0001,T-0003', '...leaving the rest in our order');
}

// 2. They filed a new one while we re-ranked.
{
  const base = HEAD + 'T-0001 — a\nT-0002 — b\n';
  const ours = HEAD + 'T-0002 — b\nT-0001 — a\n';           // we re-ranked
  const theirs = HEAD + 'T-0001 — a\nT-0002 — b\nT-0009 — new\n';
  const r = run(base, ours, theirs);
  ok(r.code === 0, 'a ticket they filed is appended');
  ok(ids(r.text).slice(0, 2).join() === 'T-0002,T-0001', "...and OUR re-rank survives it");
  ok(ids(r.text).includes('T-0009'), '...with theirs at the end');
  ok(/NOT YET PLACED/.test(r.text), '...under a band saying it is unranked');
}

// 3. THE CASE THAT MOTIVATED THE DRIVER: we re-rank the whole file, they close
//    two and file two. A text merge conflicts on every hunk; union doubles it.
{
  const base = HEAD + [1, 2, 3, 4, 5].map((n) => `T-000${n} — t${n}`).join('\n') + '\n';
  const ours = HEAD + '# --- a new band\n' + [5, 3, 1, 4, 2].map((n) => `T-000${n} — t${n}`).join('\n') + '\n';
  const theirs = HEAD + 'T-0001 — t1\nT-0003 — t3\nT-0005 — t5\nT-0008 — t8\nT-0009 — t9\n';
  const r = run(base, ours, theirs);
  ok(r.code === 0, 'a whole-file re-rank against closes and files resolves');
  ok(ids(r.text).slice(0, 3).join() === 'T-0005,T-0003,T-0001', "...our order kept for what survives");
  ok(!ids(r.text).includes('T-0002') && !ids(r.text).includes('T-0004'), '...their two closes applied');
  ok(ids(r.text).includes('T-0008') && ids(r.text).includes('T-0009'), '...their two new tickets carried');
  ok(new Set(ids(r.text)).size === ids(r.text).length, '...and nothing is duplicated');
}

// 4. Comments and bands are the owner's and must survive verbatim.
{
  const base = HEAD + 'T-0001 — a\n';
  const ours = HEAD + '# --- a band explaining why\nT-0001 — a\n';
  const theirs = HEAD + 'T-0001 — a\nT-0002 — b\n';
  const r = run(base, ours, theirs);
  ok(/a band explaining why/.test(r.text), "our band comment survives the merge");
  ok(/a band the owner wrote/.test(r.text), '...and so does the header');
}

// 5. Both sides file the SAME id — the collision this cannot paper over.
{
  const base = HEAD + 'T-0001 — a\n';
  const ours = HEAD + 'T-0001 — a\nT-0007 — ours\n';
  const theirs = HEAD + 'T-0001 — a\nT-0007 — theirs\n';
  const r = run(base, ours, theirs);
  ok(r.code === 0, 'the same id on both sides does not duplicate');
  ok(ids(r.text).filter((i) => i === 'T-0007').length === 1, '...it appears once');
  ok(/ours/.test(r.text), '...and ours is the copy kept');
}

// 6. …and its own assertions still fire when broken.
console.log('\n\x1b[1m== …and the refusal still fires\x1b[0m');
{
  // A base that already carries a duplicate forces the result to carry one too.
  const base = HEAD + 'T-0001 — a\n';
  const ours = HEAD + 'T-0001 — a\nT-0001 — a again\n';
  const theirs = HEAD + 'T-0001 — a\n';
  const r = run(base, ours, theirs);
  ok(r.code !== 0, 'a result that would carry an id twice is REFUSED, not written');
}
{
  const r = run('', '', '');
  ok(r.code === 0, 'three empty files are not an error');
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
