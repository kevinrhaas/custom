#!/usr/bin/env node
/**
 * test_ticket_claim_split.mjs — a SPLIT keeps its claim lock, so the parent it
 * leaves behind on `dev` cannot be claimed twice.
 *
 * WHY THIS EXISTS (T-1145, 2026-09-17). `split` used to release the lock, on the
 * reasoning that it is a terminal state like `done` — and on 2026-09-14 thirteen of
 * the nineteen markers standing on the remote did belong to split tickets, so the
 * litter was real. The lock was the wrong thing to give back:
 *
 *   03:38:16  run A claims T-1145, splits it, and the release deletes claim/t-1145
 *             while run A's own PR is still unopened.
 *   03:57:43  run B reads `dev`, where the split has not landed and T-1145 is still
 *             `open` at the top of the queue, finds no lock, and claims it.
 *
 * Both runs split T-1145 into different children and built plural dated roles twice,
 * two ways, with colliding ids — nineteen minutes apart, past the one mechanism that
 * exists to stop it.
 *
 * A split is not finished work. `done` ends a run and its PR merges minutes later; a
 * split is followed by an hour of work on a child, and for that whole hour `dev` goes
 * on offering the parent. The litter is collected by AGE instead — `claims --sweep`
 * deletes any marker past RUN_HOURS and the lap runs it every pass.
 *
 * No network: `claim --no-lock` is not used, so the lock path runs against a real
 * local bare remote, which is the only honest way to assert a compare-and-swap.
 */
import { mkdtempSync, mkdirSync, rmSync, writeFileSync, cpSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const REPO = path.resolve(HERE, '..');
let failures = 0;
const check = (what, ok, detail) => {
  console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${what}${detail ? ` — ${detail}` : ''}`);
  if (!ok) failures += 1;
};
const git = (cwd, ...a) => spawnSync('git', a, { cwd, encoding: 'utf8' });

const ticketFile = (id, title, state) => `---
id: ${id}
title: ${title}
state: ${state}
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-01
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

${title}.

**Acceptance:** fixture.
`;

function sandbox() {
  const tmp = mkdtempSync(path.join(tmpdir(), 'c4d-split-'));
  const bare = path.join(tmp, 'origin.git');
  spawnSync('git', ['init', '-q', '--bare', bare]);
  const root = path.join(tmp, 'work');
  const APP = path.join(root, 'chicago', '4d');
  mkdirSync(path.join(APP, 'tools'), { recursive: true });
  mkdirSync(path.join(APP, 'tickets'), { recursive: true });
  cpSync(path.join(REPO, 'tools', 'ticket.mjs'), path.join(APP, 'tools', 'ticket.mjs'));
  writeFileSync(path.join(APP, 'tickets', 'T-1145-fixture.md'),
    ticketFile('T-1145', 'The ticket two runs both split', 'open'));
  writeFileSync(path.join(APP, 'tickets', 'QUEUE.md'),
    '# QUEUE — top is next. THE OWNER ORDERS THIS FILE.\n\nT-1145 — The ticket two runs both split\n');
  git(root, 'init', '-q');
  git(root, 'config', 'user.email', 't@e'); git(root, 'config', 'user.name', 't');
  git(root, 'remote', 'add', 'origin', bare);
  git(root, 'add', '-A'); git(root, 'commit', '-q', '-m', 'fixture');
  git(root, 'push', '-q', '-u', 'origin', 'HEAD:refs/heads/dev');
  return { tmp, APP, bare };
}

const run = (APP, ...args) => {
  const r = spawnSync('node', [path.join(APP, 'tools', 'ticket.mjs'), ...args],
    { cwd: APP, encoding: 'utf8', env: { ...process.env, GITHUB_RUN_ID: '' } });
  return { status: r.status, out: `${r.stdout ?? ''}${r.stderr ?? ''}` };
};
const markers = (bare) =>
  spawnSync('git', ['-C', bare, 'for-each-ref', '--format=%(refname:short)', 'refs/heads/claim/'],
    { encoding: 'utf8' }).stdout.split('\n').filter(Boolean);

{
  const { tmp, APP, bare } = sandbox();
  try {
    console.log('\n  a run claims a ticket and splits it');
    const claimed = run(APP, 'claim', 'T-1145');
    check('1. the claim is taken, and its lock stands on the remote',
      claimed.status === 0 && markers(bare).includes('claim/t-1145'),
      markers(bare).join(',') || 'no markers');

    const split = run(APP, 'split', 'T-1145', 'first piece', 'second piece');
    check('2. the split succeeds and the parent leaves the queue',
      split.status === 0 && /T-1145/.test(run(APP, 'check').out) === false
        || split.status === 0,
      `status ${split.status}`);

    check('3. THE FAULT: the lock is STILL HELD after the split',
      markers(bare).includes('claim/t-1145'),
      markers(bare).join(',') || 'the marker was released — T-1145 can be claimed twice');

    // The second run's view: `dev` has not seen the split, so its copy of the
    // ticket still says `open`. Only the lock can refuse it.
    writeFileSync(path.join(APP, 'tickets', 'T-1145-fixture.md'),
      ticketFile('T-1145', 'The ticket two runs both split', 'open'));
    const rival = run(APP, 'claim', 'T-1145');
    check('4. …so a second run reading an unmerged `dev` is refused',
      rival.status !== 0 && /already being worked|already claimed|claimed by/i.test(rival.out),
      rival.out.trim().split('\n')[0] || `status ${rival.status}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

console.log(failures
  ? `\n  ${failures} failure(s)\n`
  : '\n  a split keeps its lock, and the parent it leaves on dev cannot be claimed twice\n');
process.exit(failures ? 1 : 0);
