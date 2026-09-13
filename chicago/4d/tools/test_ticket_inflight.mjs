#!/usr/bin/env node
/**
 * test_ticket_inflight.mjs — `ticket.mjs inflight` reports a claim that outlived the
 * three-hour window, and still refuses to call a finished branch work.
 *
 * WHY THIS EXISTS (T-0852). `inflight` read branch AGE and nothing else. A run claims,
 * pushes its claim commit, and then READS sources for four hours; at the three-hour
 * mark its branch fell out of the hot list and into one headed "finished tickets, or
 * branches older than a run" — both halves of which are false about it. It dropped out
 * at exactly the moment duplicating it was most expensive. Cohort 14 (T-0509) was read
 * twice on 2026-09-05 by two runs that could not see each other; the ledgers disagreed
 * on 36 of the 76 people and T-0816 had to adjudicate every one.
 *
 * WHY IT TAKES TWO WITNESSES AND NOT ONE. The obvious fix — trust the ticket file, and
 * call any `claimed` ticket's branch live however old — was written first and measured
 * against the real remote, where it reported SEVEN long-merged branches of T-0987 as in
 * flight. That ticket is worked one stretch per run and sits `claimed` on `dev`
 * permanently by design. So the file is necessary and not sufficient, and the second
 * witness is the CLAIM LOCK: `claim/t-nnnn` is taken in the same breath as the claim and
 * released by `ticket.mjs done`, so it lives exactly as long as the run does. Case 3
 * below is T-0987's shape and it is the reason the lock is in the rule.
 *
 * AND WHY `held` IS NOT `live`. T-0802's blind spot runs the other way: a run that dies
 * between its merge and `ticket.mjs done` leaves a ticket `claimed` behind a genuinely
 * cold branch. T-0429 sat that way for five days as the topmost queue line carrying no
 * PR — the exact shape of available work — and a run rebuilt 116 files onto records
 * already on `dev`. A third reading keeps both faults visible at once: `held` is printed
 * under IN FLIGHT with its age and a line saying a claim outliving a run is either a long
 * read or a dead one, and that the PR list decides which.
 *
 * WHY THE TEST IS A FIXTURE. The correct answer against the real remote changes by the
 * hour, so it cannot be the demonstration. `inflight --branches-json` reads a CONSTRUCTED
 * branch list ([{ name, age_hours }]) — the same device `landed --pr-json` uses, for the
 * same reason — and `--json` prints the reading each branch got. No network is reachable
 * from any case here, which is the point: this command stands between a run and its work
 * and must never be able to stop one.
 *
 * The sandbox is test_ticket_landed.mjs's: ticket.mjs resolves its paths from its own
 * location, so a temporary tree beside a copy of the tool is a whole world for it to be
 * wrong in, and the real queue is never touched.
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

/* ------------------------------------------------------------------ fixture */

const ticketFile = (id, title, state) => `---
id: ${id}
title: ${title}
state: ${state}
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-01
closed: ${state === 'done' ? '2026-09-02' : 'null'}
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

const TICKETS = [
  ['T-0509', 'The cohort a run claimed and then read for four hours', 'claimed'],
  ['T-0987', 'The recurring ticket that is claimed on dev permanently by design', 'claimed'],
  ['T-0429', 'The ticket whose run died between its merge and `done`', 'claimed'],
  ['T-1105', 'The ticket a run picked up eight minutes ago', 'open'],
  ['T-0042', 'The near miss a number match invites', 'claimed'],
  ['T-0055', 'The old branch on a ticket nobody ever claimed', 'open'],
  ['T-0100', 'The ticket that is finished', 'done'],
  ['T-0266', 'The ticket whose branch tip this clone does not hold', 'open'],
  ['T-0662', 'The ticket a run put up for review and is still on', 'review'],
];

// name, age_hours. `null` = the object is not in this clone and the age is unknowable.
const BRANCHES = [
  // 1. the base case: a run that pushed eight minutes ago.
  { name: 'steward/t-1105-tract-aware-generators', age_hours: 0.13 },
  // 2. THE FAULT. Five hours of reading, and the claim lock still stands.
  { name: 'steward/t-0509-cohort-14', age_hours: 5 },
  { name: 'claim/t-0509', age_hours: 5 },
  // 3. T-0987's shape: claimed on dev forever, lock long since released by `done`.
  { name: 'steward/t-0987-stretch-10-norris', age_hours: 40 },
  { name: 'steward/t-0987-stretch-11-hidden-surnames', age_hours: 12 },
  // 4. T-0429's shape: the run died after the merge, and `done` had let the lock go.
  { name: 'steward/t-0429-south-water-lasalle', age_hours: 120 },
  // 5. an old branch on a ticket nobody claimed — cold, exactly as before.
  { name: 'steward/t-0055-kinzie-view-plate-source', age_hours: 30 },
  // 6. a finished ticket is cold however young its branch, and however stray its lock.
  { name: 'steward/t-0100-the-finished-one', age_hours: 0.5 },
  { name: 'claim/t-0100', age_hours: 0.5 },
  // 7. the claim marker on its own, before the run's first push.
  { name: 'claim/t-0662', age_hours: 6 },
  { name: 'steward/t-0662-mint-labels', age_hours: 6 },
  // 8. a tip this clone does not hold: age unknowable.
  { name: 'steward/t-0266-phone-picket-moire', age_hours: null },
  // 11. the near miss: T-0042's lock must not travel to T-0429.
  { name: 'claim/t-0042', age_hours: 9 },
];

function sandbox() {
  const tmp = mkdtempSync(path.join(tmpdir(), 'c4d-inflight-'));
  const APP = path.join(tmp, 'chicago', '4d');
  mkdirSync(path.join(APP, 'tools'), { recursive: true });
  mkdirSync(path.join(APP, 'tickets'), { recursive: true });
  cpSync(path.join(REPO, 'tools', 'ticket.mjs'), path.join(APP, 'tools', 'ticket.mjs'));
  const queue = [];
  for (const [id, title, state] of TICKETS) {
    writeFileSync(path.join(APP, 'tickets', `${id}-fixture.md`), ticketFile(id, title, state));
    if (['open', 'claimed', 'review'].includes(state)) queue.push(`${id} — ${title}`);
  }
  writeFileSync(path.join(APP, 'tickets', 'QUEUE.md'),
    '# QUEUE — top is next. THE OWNER ORDERS THIS FILE.\n\n' + queue.join('\n') + '\n');
  writeFileSync(path.join(APP, 'branches.json'), JSON.stringify(BRANCHES, null, 2));
  return { tmp, APP };
}

function inflight(APP, file = 'branches.json', ...extra) {
  const r = spawnSync('node',
    [path.join(APP, 'tools', 'ticket.mjs'), 'inflight', '--branches-json', path.join(APP, file), ...extra],
    { cwd: APP, encoding: 'utf8' });
  return { status: r.status, out: `${r.stdout ?? ''}${r.stderr ?? ''}` };
}

/* ---------------------------------------------------- 1-11: the constructed list */

{
  const { tmp, APP } = sandbox();
  try {
    console.log('\n  a constructed branch list, no network, ticket.mjs inflight');
    const { status, out } = inflight(APP);
    const json = inflight(APP, 'branches.json', '--json');
    const rows = JSON.parse(/\[[\s\S]*\]\s*$/.exec(json.out)?.[0] ?? 'null') ?? [];
    const read = (branch) => rows.find((r) => r.branch === branch)?.reading;
    // The line a branch is printed on, so "reported in flight" is asserted against the
    // rendered report and not only against the JSON the report is built from.
    const lines = out.split('\n');
    const coldFrom = lines.findIndex((l) => /^Cold —/.test(l));
    const printedCold = (branch) => coldFrom >= 0 && lines.slice(coldFrom).some((l) => l.includes(branch));
    const printedInFlight = (branch) =>
      lines.slice(0, coldFrom < 0 ? lines.length : coldFrom).some((l) => l.includes(branch));

    check('1. a branch pushed minutes ago on an open ticket is live',
      read('steward/t-1105-tract-aware-generators') === 'live');

    check('2. THE FAULT: a 5h branch whose claim still stands is reported in flight',
      read('steward/t-0509-cohort-14') === 'held'
      && printedInFlight('steward/t-0509-cohort-14')
      && !printedCold('steward/t-0509-cohort-14'),
      read('steward/t-0509-cohort-14'));
    check('   …with its age shown, and named as a claim that outlived a run',
      /steward\/t-0509-cohort-14.*5h ago/.test(out) && /claim still stands on the remote/.test(out));
    check('   …and the run\'s own claim marker is in flight beside it',
      read('claim/t-0509') === 'held');

    check('3. T-0987: a ticket claimed on dev by design, whose lock was released, stays cold',
      read('steward/t-0987-stretch-10-norris') === 'cold'
      && read('steward/t-0987-stretch-11-hidden-surnames') === 'cold'
      && printedCold('steward/t-0987-stretch-10-norris'),
      read('steward/t-0987-stretch-10-norris'));

    check('4. T-0429: the run that died after its merge is cold, not resurrected as work',
      read('steward/t-0429-south-water-lasalle') === 'cold');

    check('5. an old branch on a ticket nobody claimed is cold, as it always was',
      read('steward/t-0055-kinzie-view-plate-source') === 'cold');

    check('6. a done ticket is cold however young the branch, and however stray the lock',
      read('steward/t-0100-the-finished-one') === 'cold' && read('claim/t-0100') === 'cold');

    check('7. `review` is held on the same footing as `claimed`',
      read('claim/t-0662') === 'held' && read('steward/t-0662-mint-labels') === 'held');

    check('8. an unknowable age is live, never cold — a blip may not invent litter',
      read('steward/t-0266-phone-picket-moire') === 'live');

    check('9. the cold heading no longer calls a held branch finished or litter',
      /^Cold — finished tickets, or unclaimed branches older than a run/m.test(out));

    check('10. the IN FLIGHT count is every live and held branch, and no cold one',
      new RegExp(`IN FLIGHT — ${rows.filter((r) => r.reading !== 'cold').length} branch`).test(out),
      out.split('\n')[0]);

    check('11. a near miss: T-0042\'s claim lock does not make T-0429 held',
      read('claim/t-0042') === 'held' && read('steward/t-0429-south-water-lasalle') === 'cold');

    check('12. it exits 0 and reports; it is a report, not a gate', status === 0, `status ${status}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

/* ------------------------------------------- 13: nothing readable is not a finding */

{
  const { tmp, APP } = sandbox();
  try {
    console.log('\n  an unreachable remote');
    writeFileSync(path.join(APP, 'empty.json'), '[]');
    const { status, out } = inflight(APP, 'empty.json');
    check('13. an empty branch list says so and accuses nobody',
      status === 0 && /nothing to report/.test(out) && !/IN FLIGHT — \d/.test(out), out.trim());
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

console.log(failures ? `\n  ${failures} failure(s)\n` : '\n  inflight reads a long claim as work and a merged branch as litter\n');
process.exit(failures ? 1 : 0);
