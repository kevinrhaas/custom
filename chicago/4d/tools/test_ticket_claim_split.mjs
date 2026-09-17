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
import { mkdtempSync, mkdirSync, rmSync, writeFileSync, readFileSync, cpSync } from 'node:fs';
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

/* ---------------------------------------------- prune: the queue drops finished work */

/**
 * A branch's QUEUE.md is a snapshot, and `dev` closes tickets under it while the PR is
 * open. `ticket.mjs check` refuses a queue line whose ticket is not workable, so the
 * branch goes red on work that is already done — #1387, #1389 and #1392 all did on
 * 2026-09-17. `prune` applies the gate's own rule, and it can only DELETE a line:
 * the owner's ranking and the band headers survive it untouched.
 */
{
  const { tmp, APP } = sandbox();
  try {
    console.log('\n  a queue carrying work that finished on dev');
    for (const [id, state] of [['T-2001', 'done'], ['T-2002', 'split'], ['T-2003', 'open']]) {
      writeFileSync(path.join(APP, 'tickets', `${id}-fixture.md`), ticketFile(id, `fixture ${id}`, state));
    }
    writeFileSync(path.join(APP, 'tickets', 'QUEUE.md'),
      '# QUEUE — top is next. THE OWNER ORDERS THIS FILE.\n# --- 1. A BAND\n'
      + 'T-2003 — fixture T-2003\nT-2001 — fixture T-2001\nT-2002 — fixture T-2002\n');

    const dry = run(APP, 'prune', '--dry-run');
    const queueAfterDry = readFileSync(path.join(APP, 'tickets', 'QUEUE.md'), 'utf8');
    check('5. --dry-run names what would go and writes nothing',
      /T-2001 \(done\)/.test(dry.out) && /T-2002 \(split\)/.test(dry.out)
      && queueAfterDry.includes('T-2001'),
      dry.out.trim());

    const r = run(APP, 'prune');
    const q = readFileSync(path.join(APP, 'tickets', 'QUEUE.md'), 'utf8');
    check('6. the finished and split lines go', r.status === 0
      && !q.includes('T-2001 —') && !q.includes('T-2002 —'), r.out.trim());
    check('   …the workable line stays, and so does the band the owner wrote',
      q.includes('T-2003 —') && q.includes('# --- 1. A BAND'));
    check('   …and a second prune is a no-op, never a second opinion',
      /nothing to drop/.test(run(APP, 'prune').out));
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

/* ------------------------------------- reconcile: the queue gets back what a merge lost */

/**
 * THE OTHER DIRECTION, AND THE ONE `prune` CANNOT REACH (T-1285). QUEUE.md is in
 * pr-lap.sh's GENERATED set, so a conflict there is cleared by taking a side and
 * letting a tool rewrite the file. For this file the "tool" is `board`, which builds
 * BOARD.md FROM the queue — it can only ever preserve what the side it took already
 * said. Take the branch's side and every line the base added is simply gone.
 *
 * Measured 2026-09-17 on the two PRs the lap had just pushed: #1400 missing 28 of
 * dev's lines, #1392 missing 27, both red on the single gate step `ticket queue` out
 * of 439 — and `prune` ran on both and could do nothing, correctly, because a prune
 * only deletes.
 *
 * The thing it must never do is invent an order: the queue is the OWNER's ranking.
 * So a restored line goes back after the SAME line it followed on the branch, and the
 * only case with no answer — a predecessor the base does not carry either — goes to
 * the foot, where `new` puts a line it cannot place.
 */
{
  const { tmp, APP } = sandbox();
  try {
    console.log('\n  a queue whose merge took the branch\'s side and dropped the base\'s lines');
    const T = (id) => writeFileSync(path.join(APP, 'tickets', `${id}-fixture.md`),
      ticketFile(id, `fixture ${id}`, 'open'));
    for (const id of ['T-3001', 'T-3002', 'T-3003', 'T-3004', 'T-3005']) T(id);

    const QUEUE = path.join(APP, 'tickets', 'QUEUE.md');
    const HEADER = '# QUEUE — top is next. THE OWNER ORDERS THIS FILE.\n# --- 1. A BAND\n';
    // The base: the owner's ranking, including two lines added while the PR was open.
    writeFileSync(QUEUE, HEADER
      + 'T-3001 — fixture T-3001\nT-3002 — fixture T-3002\nT-3003 — fixture T-3003\n');
    git(APP, 'add', '-A'); git(APP, 'commit', '-q', '-m', 'base queue');
    git(APP, 'branch', '-f', 'base');

    // The branch: it never saw T-3002 or T-3003, and it opened two of its own.
    writeFileSync(QUEUE, HEADER
      + 'T-3001 — fixture T-3001\nT-3004 — fixture T-3004\nT-3005 — fixture T-3005\n');

    const dry = run(APP, 'reconcile', '--base', 'base', '--dry-run');
    check('5. --dry-run reports and writes nothing',
      dry.status === 0 && /WOULD/.test(dry.out)
      && !readFileSync(QUEUE, 'utf8').includes('T-3002'),
      dry.out.trim().split('\n')[0]);

    const r = run(APP, 'reconcile', '--base', 'base');
    const q = readFileSync(QUEUE, 'utf8');
    const ids = q.split('\n').map((l) => /^(T-\d{4})/.exec(l)?.[1]).filter(Boolean);

    check('6. THE FAULT: the base\'s lost lines are back', r.status === 0
      && ids.includes('T-3002') && ids.includes('T-3003'), ids.join(' '));
    check('7. …in the base\'s own order, which is the owner\'s',
      ids.indexOf('T-3001') < ids.indexOf('T-3002')
      && ids.indexOf('T-3002') < ids.indexOf('T-3003'), ids.join(' '));
    check('8. the branch\'s own lines are not moved — its relative order is untouched',
      ids.indexOf('T-3001') < ids.indexOf('T-3004')
      && ids.indexOf('T-3004') < ids.indexOf('T-3005'), ids.join(' '));
    check('9. the band header survives — a reconcile is not a regeneration',
      q.includes('# --- 1. A BAND') && q.includes('THE OWNER ORDERS THIS FILE'));

    // THE REGRESSION THAT COST THE OWNER'S RULING. The first cut rebuilt on the BASE's
    // file, so every non-ticket line the branch had written was silently replaced by the
    // base's. On 2026-09-17 the owner renumbered the parked jaunts bands and wrote the
    // fall-through rule into the header; the lap ran `reconcile`, and #1413 merged with
    // neither, because the tool had quietly taken dev's headers back.
    writeFileSync(QUEUE, '# QUEUE — top is next. THE OWNER ORDERS THIS FILE.\n'
      + '# --- 1. A BAND RENAMED BY THIS BRANCH\n# Owner ruling this branch is here to make.\n'
      + 'T-3001 — fixture T-3001\n');
    run(APP, 'reconcile', '--base', 'base');
    const hq = readFileSync(QUEUE, 'utf8');
    check('9b. a header THIS BRANCH rewrote is kept, and the base\'s is not restored over it',
      hq.includes('A BAND RENAMED BY THIS BRANCH')
      && hq.includes('Owner ruling this branch is here to make.')
      && !hq.includes('# --- 1. A BAND\n'),
      hq.split('\n').filter((l) => l.startsWith('#')).join(' | '));
    check('9c. …and the base\'s missing ticket lines still came back',
      /T-3002/.test(hq) && /T-3003/.test(hq));
    writeFileSync(QUEUE, q);
    check('10. every line the base had is still there, and nothing is duplicated',
      new Set(ids).size === ids.length && ids.length === 5, ids.join(' '));

    // A branch line the base has never seen keeps the place the branch gave it, even at
    // the very top — the branch's ordering of its own work is not the tool's to move.
    T('T-3006');
    writeFileSync(QUEUE, HEADER + 'T-3006 — fixture T-3006\nT-3001 — fixture T-3001\n');
    run(APP, 'reconcile', '--base', 'base');
    const ids2 = readFileSync(QUEUE, 'utf8').split('\n')
      .map((l) => /^(T-\d{4})/.exec(l)?.[1]).filter(Boolean);
    check('11. a branch line the base lacks keeps its place, even leading the queue',
      ids2[0] === 'T-3006' && ids2.includes('T-3002') && ids2.includes('T-3003'),
      ids2.join(' '));

    const missing = run(APP, 'reconcile', '--base', 'no-such-ref');
    check('12. an unreadable base is refused loudly, never treated as an empty queue',
      missing.status !== 0 && /cannot read/.test(missing.out),
      missing.out.trim().split('\n')[0] || `status ${missing.status}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

console.log(failures
  ? `\n  ${failures} failure(s)\n`
  : '\n  a split keeps its lock, and the queue drops only finished work and regains what a merge lost\n');
process.exit(failures ? 1 : 0);
