#!/usr/bin/env node
/**
 * The ticket queue's one tool: create, claim, close, block, list, board, check.
 *
 * WHY THIS EXISTS. On 2026-08-17 the owner reported that his own requests were
 * untraceable — "i asked for a whole list of items … it's hard to find that
 * list anywhere in your files" — while the loop researched what it preferred.
 * The operational state ("what next, what's in flight, what's blocked on whom")
 * lived inside an 11,407-line ROADMAP.md and a 6,838-line STATUS.md, which no
 * owner can reorder and no agent can hold in context. Tickets pull the STATE
 * out; the prose stays where it is, as archive.
 *
 * DESIGN RULES, each bought by a documented failure in this repo:
 *  - One file per ticket. Two branches that edit one shared list corrupt it —
 *    the changelog's union-merge history is seven repairs long.
 *  - State lives ONLY in front matter. No state directories: a file's location
 *    and its `state:` field would be two copies of one fact, and this project's
 *    recurring fault is exactly two copies of one fact disagreeing.
 *  - BOARD.md and tickets.json are GENERATED. `check` refuses a stale board the
 *    same way check_published refuses a stale mirror (build.json, 2026-08-15).
 *  - IDs are assigned here, not guessed by authors — two branches that each
 *    guess "top + 1" both get it wrong (the v93/v98 collisions). A cross-branch
 *    collision is still possible at creation; `check` catches it at merge and
 *    `restamp` is the remedy.
 *  - QUEUE.md order belongs to the owner. This tool APPENDS on `new`, REMOVES
 *    on `done`/`block`/`withdraw`, and never reorders. `check` asserts the
 *    queue is exactly the workable-open set, so it cannot silently drift from
 *    the tickets, but the ORDER of its lines is never touched by machinery.
 *
 * The front-matter parser is deliberately not YAML: flat `key: value` lines
 * between two `---` fences, values read as string | null | true | false. What
 * tickets/README.md documents is exactly what parses; nothing else does.
 */
import { readFileSync, writeFileSync, readdirSync, existsSync, renameSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, '..');
const DIR = path.join(ROOT, 'tickets');
const QUEUE = path.join(DIR, 'QUEUE.md');
const BOARD = path.join(DIR, 'BOARD.md');
const JSON_OUT = path.join(DIR, 'tickets.json');

/**
 * THE PUBLISHED MIRROR OF tickets.json — T-0154, and it is here because the two
 * rules that govern a closing PR could not both be obeyed in the order AGENTS.md
 * states them.
 *
 *   1. do the work, run `tools/publish.sh` — "PUBLISH IN THE SAME COMMIT";
 *   2. push, open the PR — the PR NUMBER does not exist until this moment;
 *   3. `ticket.mjs done T-NNNN --pr N` — "close it in the merging PR";
 *   4. …which rewrites tickets.json, and `check_published.mjs` compares that file
 *      to this mirror byte for byte. The gate is now red, on every close.
 *
 * Step 3 needs a number that only step 2 can produce, so no ordering of the
 * documented steps ends green. What actually happened instead was a REMEMBERED
 * extra `publish.sh` after the close — the unwritten step that goes wrong at 3am,
 * and did on T-0153/PR #318.
 *
 * So the writer of the file maintains its mirror. Deliberately narrow:
 *  - it copies ONLY when this tool actually rewrote tickets.json. A mirror that
 *    somebody else made stale must still fail the gate — the acceptance clause
 *    says so in as many words — and a blanket refresh on every invocation would
 *    quietly launder exactly that.
 *  - it never creates the mirror directory. An unpublished checkout stays
 *    unpublished; `publish.sh` is what decides the mirror exists.
 *  - `check` pins the copy line in publish.sh, below, so the destination cannot
 *    drift into two disagreeing copies of one fact.
 */
const MIRROR = path.resolve(ROOT, '../../site/chicago/4d/tickets.json');
/** The line in publish.sh this mirror is the twin of. `check` asserts it survives. */
const PUBLISH_SH = path.join(ROOT, 'tools/publish.sh');
const PUBLISH_PIN = 'cp -f tickets/tickets.json "$SITE/tickets.json"';

const STATES = ['open', 'claimed', 'review', 'done', 'blocked-owner', 'blocked-tech',
  'withdrawn', 'split'];
/**
 * EFFORT IS MEASURED IN RUNS, NOT IN POINTS.
 *
 * The owner asked on 2026-08-17 whether tickets should carry work points and be
 * split past a threshold. Points are a proxy; the thing they proxy for here is
 * concrete and already binding — **can ONE run take this from claim to a merged,
 * gated, visibly-changed dev?** A run has hard edges in this project: a ~150-min
 * budget, a 10-minute per-command ceiling that the desktop smoke does not fit
 * inside, and the bake boundary (no Blender on the improve runner). So the unit
 * is the run, and the test is the acceptance clause: **if a ticket needs more
 * than one demonstration to be done, it is more than one ticket.**
 *
 * The evidence it was needed: on its first run under this queue the loop took
 * T-0001 (walkable bridges), shipped only the walker-deck half, titled the PR
 * "T-0001(1/2)" and left the ticket `claimed` — it had to invent a notation
 * because the system could not say "this is two runs".
 */
const EFFORT = {
  XS: 'part of a run',
  S: 'one run',
  M: 'one run, tight — or one run plus a bake',
  L: 'MORE THAN ONE RUN — must be split before it can be claimed',
};
// PAPERS: the newspaper-corpus epic — extraction from the 1833-1835 Democrat
// and American transcriptions, and the documented businesses/residents seeded
// from them. Registered 2026-08-28 with the epic's nine founding tickets
// (T-0256..T-0264), on the owner's instruction.
const EPICS = ['RENDERING', 'TOWN', 'GROUND', 'FLORA', 'PIPELINE', 'META', 'PAPERS', 'SOUTH_TIME'];
const BY = ['owner', 'loop', 'steward'];
// Workable = an agent may take it off the queue. `claimed`/`review` stay in the
// queue so a crashed run's ticket is still visible in priority order rather
// than vanishing into a state nobody lists.
const WORKABLE = ['open', 'claimed', 'review'];

/* ---------------------------------------------------------------- parsing */

function parseTicket(file) {
  const src = readFileSync(file, 'utf8');
  const m = /^---\n([\s\S]*?)\n---\n?/.exec(src);
  if (!m) return { file, error: 'no front-matter fence' };
  const t = { file, body: src.slice(m[0].length) };
  for (const line of m[1].split('\n')) {
    if (!line.trim()) continue;
    const kv = /^([a-z_]+):\s*(.*)$/.exec(line);
    if (!kv) return { file, error: `unparseable front-matter line: "${line}"` };
    const v = kv[2].trim();
    t[kv[1]] = v === 'null' ? null : v === 'true' ? true : v === 'false' ? false : v;
  }
  return t;
}

function loadAll() {
  if (!existsSync(DIR)) return [];
  return readdirSync(DIR)
    .filter((f) => /^T-\d{4}.*\.md$/.test(f))
    .map((f) => parseTicket(path.join(DIR, f)));
}

function writeTicket(t) {
  const keys = ['id', 'title', 'state', 'epic', 'requested_by', 'seen', 'effort',
    'legacy_id', 'parent', 'opened', 'closed', 'pr', 'claimed_by', 'blocked_on', 'needs_bake'];
  const fm = keys.map((k) => `${k}: ${t[k] ?? 'null'}`).join('\n');
  writeFileSync(t.file, `---\n${fm}\n---\n${t.body ?? ''}`);
}

function today() {
  // Central Time, the project's clock (AGENTS.md).
  return new Date().toLocaleDateString('en-CA', { timeZone: 'America/Chicago' });
}

function slugOf(title) {
  return title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48);
}

const git = (args) => execFileSync('git', args, {
  cwd: ROOT, encoding: 'utf8', timeout: 20_000, stdio: ['ignore', 'pipe', 'ignore'],
});

/** The branch this checkout is on, or '' when detached or there is no git. */
function currentBranch() {
  try { return git(['rev-parse', '--abbrev-ref', 'HEAD']).trim(); } catch { return ''; }
}

/**
 * Every branch head on the remote, read ONCE per process — `inflight` asks about
 * a hundred tickets and one `ls-remote` answers all of them. `main` and `dev` are
 * never work-in-progress, so they never appear.
 *
 * Failure returns [] on purpose: these callers stand between a run and its work,
 * and a network blip must never be able to stop one.
 */
let branchCache = null;
function remoteBranches() {
  if (branchCache) return branchCache;
  try {
    branchCache = git(['ls-remote', '--heads', 'origin'])
      .split('\n')
      .map((l) => {
        const [sha, ref] = l.split('\t');
        return { name: ref?.split('refs/heads/')[1]?.trim(), sha: sha?.trim() };
      })
      .filter((b) => b.name && b.name !== 'main' && b.name !== 'dev');
  } catch {
    branchCache = [];
  }
  return branchCache;
}

/**
 * THE HIGHEST TICKET NUMBER ANYWHERE — this tree, plus every ticket sitting on a
 * branch that has not merged yet.
 *
 * Ids used to be `max + 1` over the LOCAL tickets directory, which only ever holds
 * what has merged. Two branches opened the same afternoon therefore both computed
 * the same next number, and `check` refused the second one at the merge. That
 * happened THREE TIMES in two days (T-0084, T-0111, T-0116), and each time the
 * repair cost a rebase — and, until `restamp` was fixed alongside this, the
 * renumbered ticket also lost its place in the owner's queue.
 *
 * So look where the in-flight numbers actually are: the tickets directory of every
 * `steward/*` branch on the remote. One `ls-tree` per branch, no checkout, no
 * fetch of file contents — the FILENAMES carry the ids.
 *
 * Best-effort, like everything else here that touches the network: no git, no
 * remote, or a stale clone just means the old local-only answer, never a refusal
 * to create a ticket. It narrows the window; `check` still closes it.
 */
function remoteIdMax() {
  try {
    // Refresh the steward refs so a branch pushed minutes ago is visible. Cheap:
    // these branches are a few commits off dev and share nearly all their objects.
    try {
      git(['fetch', '--quiet', '--prune', 'origin', '+refs/heads/steward/*:refs/remotes/origin/steward/*']);
    } catch { /* offline, or no such refspec — fall through to whatever is cached */ }
    const refs = git(['for-each-ref', '--format=%(refname)', 'refs/remotes/origin/steward'])
      .split('\n').map((s) => s.trim()).filter(Boolean);
    // `<ref>:<path>` resolves against the CWD, not the top of the tree — from
    // `chicago/4d` a path of `chicago/4d/tickets` silently reads as
    // `chicago/4d/chicago/4d/tickets` and returns EMPTY WITH EXIT 0, which is how
    // this scan first shipped finding nothing at all and quietly handing back the
    // old local-only answer. So ask git where the top is and read from there.
    const top = git(['rev-parse', '--show-toplevel']).trim();
    const dir = `${git(['rev-parse', '--show-prefix']).trim()}tickets`;
    let max = 0;
    for (const ref of refs) {
      let names = '';
      try {
        names = execFileSync('git', ['ls-tree', '--name-only', `${ref}:${dir}`], {
          cwd: top, encoding: 'utf8', timeout: 20_000, stdio: ['ignore', 'pipe', 'ignore'],
        });
      } catch { continue; }        // a branch from before the queue existed
      for (const m of names.matchAll(/^T-(\d{4})-/gm)) max = Math.max(max, Number(m[1]));
    }
    return max;
  } catch {
    return 0;
  }
}

/** The next free id, counting merged tickets AND every branch still in flight. */
function nextIdNum(tickets) {
  const local = Math.max(0, ...tickets.map((t) => Number(/^T-(\d{4})$/.exec(t.id ?? '')?.[1] ?? 0)));
  return Math.max(local, remoteIdMax()) + 1;
}

const idOf = (n) => `T-${String(n).padStart(4, '0')}`;

/**
 * How many hours since this branch was last pushed to, or null if unknowable.
 *
 * NOT ancestry. Everything here squash-merges, so a merged branch's head is never
 * an ancestor of `dev` and `merge-base --is-ancestor` answers "unmerged" for every
 * branch that ever landed — a confidently wrong signal, which is worse than none.
 * Age is the honest one: a steward run lasts under two hours, so a branch whose tip
 * is a day old is not a run at work, whatever its ticket says.
 *
 * Reads the commit only if it is already in this clone (it is, for anything fetched);
 * no network, and null when the object is absent.
 */
function branchAgeHours(sha) {
  if (!sha) return null;
  try {
    const ts = Number(git(['log', '-1', '--format=%ct', sha]).trim());
    return Number.isFinite(ts) ? (Date.now() / 1000 - ts) / 3600 : null;
  } catch {
    return null;
  }
}

/** A run lasts ~1 hour; nothing older than this is one, whatever else is true. */
const RUN_HOURS = 3;

/**
 * Does this branch name carry this ticket's number?
 *
 * Branch names are not standardised — the same ticket has been worked on
 * `steward/t62-more-docks` and `steward/t-0062-more-docks` — so match the NUMBER
 * with its padding and its separator optional, and refuse to match a longer one
 * (T-0062 must not fire on `t-0620`).
 */
function branchCarries(branch, id) {
  const n = /^T-(\d+)$/.exec(id)?.[1];
  if (!n) return false;
  return new RegExp(`(?:^|[^0-9a-z])t-?0*${Number(n)}(?![0-9])`, 'i').test(branch);
}

/** Branches that look like somebody ELSE is already working this ticket. */
function remoteBranchesFor(id) {
  const here = currentBranch();
  return remoteBranches()
    .filter((b) => b.name !== here && branchCarries(b.name, id))
    .map((b) => {
      const age = branchAgeHours(b.sha);
      return age !== null && age > RUN_HOURS
        ? `${b.name}  (last pushed ${Math.round(age)}h ago — older than a run, likely litter)`
        : b.name;
    });
}

function find(tickets, id) {
  const t = tickets.find((x) => x.id === id);
  if (!t) { console.error(`no ticket ${id}`); process.exit(1); }
  return t;
}

function queueIds() {
  return queueLines().map(queueId).filter(Boolean);
}

function queueAppend(t) {
  const cur = existsSync(QUEUE) ? readFileSync(QUEUE, 'utf8').replace(/\n+$/, '\n') : queueHeader();
  writeFileSync(QUEUE, cur + `${t.id} — ${t.title}\n`);
}

function queueLines() {
  if (!existsSync(QUEUE)) return [];
  return readFileSync(QUEUE, 'utf8').split('\n');
}

/** The id a queue line carries, or null for a comment/blank/prose line. */
function queueId(line) {
  return /^(T-\d{4})\b/.exec(line.trim())?.[1] ?? null;
}

/**
 * The LABEL half of a queue line — everything after the id, which QUEUE.md's own
 * header calls "a label, not data" and which is regenerated from the ticket's
 * `title:`. It is also the only thing that tells two lines carrying the SAME id
 * apart, which is what `queueIndexOf` below needs it for.
 */
function queueLabel(line) {
  return /^T-\d{4}\s*[—-]\s*(.*)$/.exec(line.trim())?.[1]?.trim() ?? '';
}

/**
 * THE LINE THAT BELONGS TO ONE PARTICULAR TICKET — by id AND by label (T-0217).
 *
 * Matching on the id alone is right in every state `check` allows, and wrong in
 * the one state `restamp` exists to repair: a duplicate id puts TWO lines in the
 * queue carrying it, and `indexOf` returns whichever the owner happened to rank
 * higher — a coin toss. On 2026-08-27 it came up tails during T-0215's merge and
 * silently overwrote a queue line the owner had ordered with another ticket's
 * title, leaving a stale line behind for good measure. `check` was green
 * throughout; it was caught by reading `tail QUEUE.md`.
 *
 * The title is the discriminator because the line was WRITTEN from it. When it
 * cannot discriminate — a hand-edited label, or genuinely identical titles — this
 * falls back to the first line carrying the id, i.e. the old behaviour, and the
 * caller says out loud that it guessed. A repair tool that refused to run would
 * leave the duplicate in place, which is worse.
 */
function queueIndexOf(id, title) {
  const lines = queueLines();
  const carries = (l) => queueId(l) === id;
  const exact = lines.findIndex((l) => carries(l) && queueLabel(l) === title);
  return { i: exact >= 0 ? exact : lines.findIndex(carries), byLabel: exact >= 0 };
}

function queueReplaceAt(i, rows) {
  // Children take the PARENT'S EXACT PLACE in the order. Appending them to the
  // bottom would silently demote work the owner had deliberately ranked — the
  // one thing this file's ordering rule exists to prevent. A split is a
  // clarification of what the work is, never a re-prioritisation of it.
  const lines = queueLines();
  if (i < 0) lines.push(...rows); else lines.splice(i, 1, ...rows);
  writeFileSync(QUEUE, lines.join('\n').replace(/\n+$/, '\n'));
}

function queueReplace(id, rows, title) {
  queueReplaceAt(queueIndexOf(id, title).i, rows);
}

function queueRemove(id) {
  if (!existsSync(QUEUE)) return;
  const kept = readFileSync(QUEUE, 'utf8').split('\n')
    .filter((l) => !l.trim().startsWith(id)).join('\n');
  writeFileSync(QUEUE, kept.replace(/\n+$/, '\n'));
}

function queueHeader() {
  return `# QUEUE — top is next. THE OWNER ORDERS THIS FILE; agents only append and remove.\n`
    + `# Reorder by moving lines. Everything after the ticket id on a line is a label, not data.\n\n`;
}

/* ----------------------------------------------------------------- board */

function generateBoard(tickets) {
  const at = new Date().toLocaleString('en-US', { timeZone: 'America/Chicago',
    month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
  const order = queueIds();
  const rank = (t) => { const i = order.indexOf(t.id); return i < 0 ? 9999 : i; };
  const sec = (name, list, line) => list.length
    ? `## ${name} (${list.length})\n\n${list.map(line).join('\n')}\n\n` : '';
  const row = (t) => `- **${t.id}** ${t.title}`
    + `${t.requested_by === 'owner' ? ' · **OWNER**' : ''}`
    + `${t.seen === true ? ' · SEEN' : ''}${t.needs_bake === true ? ' · needs-bake' : ''}`
    + `${t.legacy_id ? ` · was ${t.legacy_id}` : ''}`
    + `${t.state === 'claimed' || t.state === 'review' ? ` · ${t.state}` : ''}`;
  const open = tickets.filter((t) => WORKABLE.includes(t.state)).sort((a, b) => rank(a) - rank(b));
  const owner = tickets.filter((t) => t.state === 'blocked-owner');
  const tech = tickets.filter((t) => t.state === 'blocked-tech');
  const split = tickets.filter((t) => t.state === 'split');
  const done = tickets.filter((t) => t.state === 'done')
    .sort((a, b) => String(b.closed).localeCompare(String(a.closed))).slice(0, 20);

  const md = `# BOARD — generated by \`tools/ticket.mjs board\`, ${at} CT. Do not edit.\n\n`
    + sec('In the queue, in the owner’s order', open, row)
    + sec('⏸ Waiting on an owner decision', owner, (t) => `${row(t)}\n  - **the question:** ${t.blocked_on}`)
    + sec('Blocked on tooling or another ticket', tech, (t) => `${row(t)} — ${t.blocked_on}`)
    + sec('Split into pieces (the pieces are in the queue)', split, (t) => `${row(t)}`
      + ` — ${tickets.filter((c) => c.parent === t.id).map((c) => c.id).join(', ')}`)
    + sec('Recently done', done, (t) => `${row(t)} · ${t.closed}${t.pr ? ` · PR #${t.pr}` : ''}`);
  // Idempotent on purpose: only touch the files when the CONTENT changed, so a
  // regenerated-but-identical board stays byte-stable and the published mirror
  // (check_published.mjs compares it verbatim) does not go stale merely because
  // `check` ran after `publish.sh`. The timestamp is excluded from the diff and
  // only rewritten alongside a real change.
  const settle = (file, next) => {
    const cur = existsSync(file) ? readFileSync(file, 'utf8') : '';
    const bare = (x) => x.replace(/generated_ct.*|generated by.*/g, '');
    if (bare(cur) === bare(next)) return false;
    writeFileSync(file, next);
    return true;
  };
  settle(BOARD, md);

  const strip = tickets.map(({ file, body, error, ...rest }) => ({
    ...rest, queue_rank: WORKABLE.includes(rest.state) ? rank(rest) : null,
  }));
  const wrote = settle(JSON_OUT, JSON.stringify({ project: 'chicago-4d',
    generated_ct: at, tickets: strip }, null, 2) + '\n');
  // T-0154: this tool is the WRITER of tickets.json, so it carries the file to
  // the one published path publish.sh copies it to. Only on a real rewrite —
  // see MIRROR's note on why a blanket refresh would weaken check_published.
  if (wrote) mirrorTickets();
}

/**
 * Carry tickets.json to `site/chicago/4d/tickets.json`, the verbatim copy
 * `tools/publish.sh` makes and `tools/check_published.mjs` compares byte for
 * byte. Returns true when it moved bytes, so the caller can say so.
 */
function mirrorTickets() {
  if (!existsSync(path.dirname(MIRROR))) return false;   // never published: leave it that way
  const src = readFileSync(JSON_OUT);
  if (existsSync(MIRROR) && readFileSync(MIRROR).equals(src)) return false;
  writeFileSync(MIRROR, src);
  console.log('   tickets.json mirrored to site/chicago/4d/ (T-0154)');
  return true;
}

/* ----------------------------------------------------------------- check */

function check(tickets) {
  const problems = [];
  const seen = new Map();
  for (const t of tickets) {
    const at = path.basename(t.file);
    if (t.error) { problems.push(`${at}: ${t.error}`); continue; }
    if (!/^T-\d{4}$/.test(t.id ?? '')) problems.push(`${at}: bad id "${t.id}"`);
    if (seen.has(t.id)) {
      problems.push(`${at}: DUPLICATE id ${t.id} (also ${seen.get(t.id)}) — two branches each `
        + 'assigned it. `node tools/ticket.mjs restamp <file>` renumbers the younger one');
    }
    seen.set(t.id, at);
    if (!STATES.includes(t.state)) problems.push(`${at}: state "${t.state}" is not one of ${STATES.join('/')}`);
    if (!EPICS.includes(t.epic)) problems.push(`${at}: epic "${t.epic}" is not one of ${EPICS.join('/')}`);
    if (!BY.includes(t.requested_by)) problems.push(`${at}: requested_by "${t.requested_by}"`);
    if (!t.title) problems.push(`${at}: no title`);
    if (t.state === 'done' && !t.pr) problems.push(`${at}: done without a pr — the closing PR is the receipt`);
    if (t.state === 'done' && !t.closed) problems.push(`${at}: done without a closed date`);
    if (t.state?.startsWith('blocked') && !t.blocked_on) {
      problems.push(`${at}: ${t.state} without blocked_on — a block with no stated question is an abandonment`);
    }
    if (!t.body?.trim()) problems.push(`${at}: empty body — a ticket with no ask or acceptance is a title`);
    if (!Object.keys(EFFORT).includes(t.effort)) {
      problems.push(`${at}: effort "${t.effort}" is not one of ${Object.keys(EFFORT).join('/')} `
        + `(measured in RUNS: ${Object.entries(EFFORT).map(([k, v]) => `${k} = ${v}`).join('; ')})`);
    }
    // An L in the queue is a ticket that CANNOT be finished by whoever takes it,
    // so it would produce a half-done ticket and a self-invented "(1/2)" title.
    // Sizing is the author's job, not the claimant's.
    if (t.effort === 'L' && WORKABLE.includes(t.state)) {
      problems.push(`${at}: effort L is in the queue — ${EFFORT.L}. `
        + `Run \`node tools/ticket.mjs split ${t.id} "first piece" "second piece"\`; `
        + 'the children keep its place in the order.');
    }
    if (t.state === 'split' && WORKABLE.includes(t.state)) {
      problems.push(`${at}: a split parent must not sit in the queue — its children carry the work`);
    }
    if (t.parent && !tickets.some((x) => x.id === t.parent)) {
      problems.push(`${at}: parent ${t.parent} does not exist`);
    }
  }
  // The queue must be EXACTLY the workable set: an open ticket missing from the
  // queue is invisible work, and a queued closed ticket sends an agent to a
  // ghost. Order is not checked — order is the owner's.
  const q = queueIds();
  const wantIds = tickets.filter((t) => WORKABLE.includes(t.state)).map((t) => t.id);
  const ledger = new Map(tickets.filter((t) => t.id).map((t) => [t.id, t]));
  for (const id of q) {
    // NOT IN THE LEDGER AT ALL is its own answer, and it is the one T-0217 asked
    // for: a queue line pointing at an id no ticket file carries is a line the
    // owner ranked that now sends whoever reads it to nothing. The old single
    // message called that "not an open ticket", which reads like a ticket that
    // closed — a repair (delete the line) rather than a corruption (find out
    // what was lost).
    if (!ledger.has(id)) {
      problems.push(`QUEUE.md lists ${id}, which is not in the ledger — no ticket file carries `
        + 'that id. A queue line pointing at nothing is a lost ranking, not a stale one: find '
        + 'what the line used to name before deleting it');
    } else if (!wantIds.includes(id)) {
      problems.push(`QUEUE.md lists ${id}, which is not an open ticket (state ${ledger.get(id).state})`);
    }
  }
  for (const id of wantIds) {
    if (!q.includes(id)) problems.push(`open ticket ${id} is missing from QUEUE.md — append it, do not reorder`);
  }
  const dupQ = q.filter((id, i) => q.indexOf(id) !== i);
  for (const id of new Set(dupQ)) problems.push(`QUEUE.md lists ${id} twice`);

  // THE LABEL HAS TO NAME THE TICKET (T-0217). Every gate above reads the id and
  // nothing else, so a line carrying one ticket's id and another's title passes
  // all of them: both ids are real, both are open, neither is duplicated. That is
  // exactly the residue `restamp`'s wrong-line bug left on 2026-08-27, and it is
  // what an agent reading QUEUE.md top-down goes and builds. The label is
  // regenerated from `title:`, so the ticket wins and the line is repairable by
  // hand in one edit — the message says which line and what it should read.
  queueLines().forEach((l, n) => {
    const id = queueId(l);
    const t = id && ledger.get(id);
    if (!t || !t.title) return;
    const label = queueLabel(l);
    if (label !== t.title) {
      problems.push(`QUEUE.md line ${n + 1} labels ${id} "${label || '(nothing)'}", but that `
        + `ticket is titled "${t.title}" — the ticket wins; rewrite the line as `
        + `\`${id} — ${t.title}\``);
    }
  });

  // The generated pair must be fresh — a stale board is the stale-build.json
  // fault (found on check_published's first run) wearing a new file name.
  const beforeB = existsSync(BOARD) ? readFileSync(BOARD, 'utf8') : '';
  const beforeJ = existsSync(JSON_OUT) ? readFileSync(JSON_OUT, 'utf8') : '';
  generateBoard(tickets);
  if (readFileSync(BOARD, 'utf8') !== beforeB || readFileSync(JSON_OUT, 'utf8') !== beforeJ) {
    problems.push('BOARD.md / tickets.json were stale — regenerated now; commit them '
      + '(run `node tools/ticket.mjs board` before every merge, like the changelog stamp)');
  }

  // THE MIRROR PIN (T-0154). `mirrorTickets` above hard-codes where publish.sh
  // puts this file, which is a second copy of one fact — the failure mode this
  // whole tool's design rules are written against. So the fact is pinned: if the
  // copy in publish.sh moves or goes away, this says so rather than letting the
  // two drift into silently mirroring different paths.
  if (existsSync(PUBLISH_SH) && !readFileSync(PUBLISH_SH, 'utf8').includes(PUBLISH_PIN)) {
    problems.push(`tools/publish.sh no longer contains \`${PUBLISH_PIN}\`, which is the copy `
      + 'this tool mirrors on its behalf (T-0154). Reconcile them: change MIRROR in '
      + 'tools/ticket.mjs to publish.sh\'s new destination, or drop the mirroring if '
      + 'publish.sh has stopped carrying tickets.json at all.');
  }
  return problems;
}

/* ------------------------------------------------------------------ main */

const [cmd, ...args] = process.argv.slice(2);
const flag = (name) => { const i = args.indexOf(`--${name}`); return i < 0 ? null : (args[i + 1] ?? true); };
const has = (name) => args.includes(`--${name}`);
const tickets = loadAll();

switch (cmd) {
  case 'new': {
    const title = args.filter((a) => !a.startsWith('--')
      && a !== flag('epic') && a !== flag('by') && a !== flag('effort') && a !== flag('legacy')).join(' ');
    if (!title) { console.error('usage: ticket.mjs new "title" [--epic E] [--by owner|loop|steward] [--seen] [--needs-bake] [--effort M] [--legacy OLD-ID]'); process.exit(1); }
    const id = idOf(nextIdNum(tickets));
    const t = {
      file: path.join(DIR, `${id}-${slugOf(title)}.md`),
      id, title, state: 'open',
      epic: (flag('epic') ?? 'META').toUpperCase(),
      requested_by: flag('by') ?? 'steward',
      seen: has('seen'), effort: flag('effort') ?? 'M',
      legacy_id: flag('legacy') ?? null,
      opened: today(), closed: null, pr: null, claimed_by: null, blocked_on: null,
      needs_bake: has('needs-bake'),
      body: `\n${title}.\n\n**Acceptance:** (state it before working — the definition of done, never weakened to pass)\n`,
    };
    writeTicket(t); queueAppend(t); generateBoard(loadAll());
    console.log(`${id} created → ${path.relative(ROOT, t.file)} (appended to QUEUE bottom — the owner orders it)`);
    break;
  }
  case 'claim': {
    const t = find(tickets, args[0]);
    if (!WORKABLE.includes(t.state)) { console.error(`${t.id} is ${t.state}, not claimable`); process.exit(1); }
    // An L ticket cannot be finished in the run that claims it, so claiming one
    // guarantees a half-done ticket and a PR that invents its own "(1/2)".
    if (t.effort === 'L') {
      console.error(`${t.id} is effort L — ${EFFORT.L}.\n`
        + `Split it first, and the pieces keep this ticket's place in the queue:\n`
        + `  node tools/ticket.mjs split ${t.id} "first piece" "second piece"`);
      process.exit(1);
    }
    // A claim only reaches `dev` when its PR merges, so a run that opens a PR and
    // does not merge it leaves the ticket reading `open` to the NEXT run, which
    // then does the same work twice. That happened to T-0062 on 2026-08-19: run
    // 943 opened PR #258 green and deferred the merge on a smoke it could not
    // finish; run 944 read the queue, saw T-0062 open at the top, and rebuilt it
    // from scratch on its own branch. Two runs, one ticket, one of them binned.
    //
    // The remote branch list is the one piece of shared state a run CAN see
    // before it starts, so look there. Best-effort by construction: no network,
    // no git, or a detached checkout just means no warning — never a false stop.
    const rival = remoteBranchesFor(t.id);
    if (rival.length && !has('force')) {
      console.error(`${t.id} looks like it is already being worked:\n`
        + rival.map((b) => `  ${b}`).join('\n')
        + `\nCheck whether that branch has an open PR before starting. If it is stale,\n`
        + `or that branch is yours, claim it anyway:\n`
        + `  node tools/ticket.mjs claim ${t.id} --force`);
      process.exit(1);
    }
    t.state = 'claimed';
    t.claimed_by = `${flag('by') ?? 'run'} ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })} CT`;
    writeTicket(t); generateBoard(loadAll());
    console.log(`${t.id} claimed`);
    break;
  }
  case 'done': {
    const t = find(tickets, args[0]);
    t.state = 'done'; t.closed = today(); t.pr = flag('pr');
    if (!t.pr) { console.error('done needs --pr N — the closing PR is the receipt'); process.exit(1); }
    writeTicket(t); queueRemove(t.id); generateBoard(loadAll());
    console.log(`${t.id} done (PR #${t.pr}) — removed from QUEUE`);
    break;
  }
  case 'block': {
    const t = find(tickets, args[0]);
    t.state = has('owner') ? 'blocked-owner' : 'blocked-tech';
    t.blocked_on = flag('on');
    if (!t.blocked_on) { console.error('block needs --on "the question or the missing thing"'); process.exit(1); }
    writeTicket(t); queueRemove(t.id); generateBoard(loadAll());
    console.log(`${t.id} → ${t.state}`);
    break;
  }
  case 'unblock': {
    const t = find(tickets, args[0]);
    t.state = 'open'; t.blocked_on = null;
    writeTicket(t); queueAppend(t); generateBoard(loadAll());
    console.log(`${t.id} → open (appended to QUEUE bottom; the owner may move it up)`);
    break;
  }
  case 'withdraw': {
    const t = find(tickets, args[0]);
    t.state = 'withdrawn'; t.closed = today(); t.blocked_on = flag('why') ?? t.blocked_on;
    writeTicket(t); queueRemove(t.id); generateBoard(loadAll());
    console.log(`${t.id} withdrawn`);
    break;
  }
  case 'restamp': {
    // The duplicate-id remedy. Renumber ONE ticket (the younger of a colliding
    // pair) to the next free id, renaming its file with it.
    //
    // Takes a path as readily as a bare filename or an id: with two files sharing
    // an id, `find` by id cannot tell them apart, so the FILE is the only way to
    // say which one moves — and the first thing anyone reaches for is the path
    // `check` just printed.
    const arg = args[0] ?? '';
    const t = tickets.find((x) => x.file === path.resolve(arg))
      ?? tickets.find((x) => path.basename(x.file) === path.basename(arg))
      ?? find(tickets, arg);
    const old = t.id;
    // KEEP ITS PLACE IN THE QUEUE. This used to remove the old line and append
    // the new one at the BOTTOM, so renumbering a ticket silently re-prioritised
    // it — and the owner orders that file. A restamp changes a ticket's NUMBER
    // and nothing else about it.
    //
    // AND KEEP THE OTHER TICKET'S. The comment above says the FILE is the only
    // way to name which of a colliding pair moves; the queue edit then went back
    // to matching on the shared id, so it rewrote whichever of the two lines the
    // owner had ranked higher (T-0217). `queueIndexOf` resolves the line by id
    // AND label, so the line that moves is the one written from THIS file.
    const { i: line, byLabel } = queueIndexOf(old, t.title);
    t.id = idOf(nextIdNum(tickets));
    const dest = path.join(DIR, `${t.id}-${slugOf(t.title)}.md`);
    writeTicket(t); renameSync(t.file, dest); t.file = dest;
    if (line >= 0) queueReplaceAt(line, [`${t.id} — ${t.title}`]);
    else if (WORKABLE.includes(t.state)) queueAppend(t);
    // Say so when the label could not name the line. With a duplicate id in the
    // queue that means the wrong line may just have moved — the exact fault this
    // repair is for — and the reader is the only one who can tell.
    if (line >= 0 && !byLabel && queueIds().filter((x) => x === old).length) {
      console.log(`   NOTE: no queue line carried this ticket's title, so line ${line + 1} `
        + `was picked by id alone and another ${old} line remains. Check QUEUE.md.`);
    }
    generateBoard(loadAll());
    console.log(`${old} → ${t.id}${line >= 0 ? ' (queue place kept)' : ''}`);
    break;
  }
  case 'split': {
    // The remedy for an L ticket, and for any ticket a run discovers is bigger
    // than one demonstration. The parent becomes the grouping record (state
    // `split`, out of the queue) and the children take its place in the order.
    const t = find(tickets, args[0]);
    const titles = args.slice(1).filter((a) => !a.startsWith('--'));
    if (titles.length < 2) {
      console.error(`usage: ticket.mjs split ${t.id} "first piece" "second piece" [...]`);
      process.exit(1);
    }
    let next = nextIdNum(tickets) - 1;
    const rows = [];
    titles.forEach((title, n) => {
      next += 1;
      const id = idOf(next);
      const child = {
        file: path.join(DIR, `${id}-${slugOf(title)}.md`),
        id, title, state: 'open', epic: t.epic, requested_by: t.requested_by,
        seen: t.seen, effort: 'S', legacy_id: t.legacy_id, parent: t.id,
        opened: today(), closed: null, pr: null, claimed_by: null, blocked_on: null,
        needs_bake: false,
        body: `\n${title}.\n\nPiece ${n + 1} of ${titles.length} of **${t.id} — ${t.title}**, `
          + `split because the parent needed more than one run's demonstration to be done. `
          + `The parent keeps the full ask and its links; this ticket owns one slice of it.\n\n`
          + `**Acceptance:** (state it before working — one demonstration, never weakened to pass)\n`,
      };
      writeTicket(child);
      rows.push(`${id} — ${title}`);
      console.log(`  ${id}  ${title}`);
    });
    queueReplace(t.id, rows, t.title);
    t.state = 'split'; t.closed = today();
    writeTicket(t); generateBoard(loadAll());
    console.log(`${t.id} → split into ${titles.length}; children hold its place in QUEUE`);
    break;
  }
  case 'list': {
    const want = flag('state');
    const shown = tickets.filter((t) => has('workable') ? WORKABLE.includes(t.state) : (!want || t.state === want));
    const order = queueIds();
    shown.sort((a, b) => (order.indexOf(a.id) + 1 || 9999) - (order.indexOf(b.id) + 1 || 9999));
    for (const t of shown) {
      console.log(`${t.id}  ${String(t.state).padEnd(13)} ${t.requested_by === 'owner' ? 'OWNER ' : '      '}${t.title}`);
    }
    break;
  }
  case 'board': generateBoard(tickets); console.log(`BOARD.md + tickets.json regenerated (${tickets.length} tickets)`); break;
  /**
   * WHAT IS BEING WORKED ON RIGHT NOW — the one question the files cannot answer.
   *
   * A ticket's state lives in its file, and the file only reaches `dev` when its PR
   * merges, so BOARD.md can show the queue and what has landed but never what is in
   * flight. The remote branch list can: a run pushes its branch in its first commit,
   * hours before anything merges. So read the branches and map them back to tickets.
   *
   * Three things fall out of that mapping, and each is worth seeing:
   *   - a branch on an OPEN ticket — that is the loop, working, right now;
   *   - a branch on a DONE ticket — a leftover, safe to delete;
   *   - a ticket the files call `claimed` with no branch — an abandoned claim.
   */
  case 'inflight': {
    const here = currentBranch();
    const branches = remoteBranches();
    const rows = [];
    for (const b of branches) {
      const t = tickets.find((x) => branchCarries(b.name, x.id));
      if (t) rows.push({ b: b.name, t, age: branchAgeHours(b.sha) });
    }
    // Live work first: a young branch on a ticket that is not finished.
    const isLive = (r) => !['done', 'withdrawn'].includes(r.t.state) && (r.age === null || r.age <= RUN_HOURS);
    rows.sort((a, b) => Number(isLive(b)) - Number(isLive(a)) || a.t.id.localeCompare(b.t.id));

    if (!branches.length) {
      console.log('no remote branches readable (no network, or no git) — nothing to report');
      break;
    }
    const live = rows.filter(isLive);
    const cold = rows.filter((r) => !isLive(r));
    const age = (r) => (r.age === null ? '' : r.age < 1 ? `${Math.round(r.age * 60)}m ago` : `${Math.round(r.age)}h ago`);

    if (!live.length) {
      console.log('IN FLIGHT — nothing. No fresh branch carries a ticket number.');
    } else {
      console.log(`IN FLIGHT — ${live.length} branch(es) pushed within ${RUN_HOURS}h on unfinished tickets:\n`);
      for (const r of live) {
        console.log(`  ${r.t.id}  ${String(r.t.state).padEnd(9)} ${r.t.requested_by === 'owner' ? 'OWNER ' : '      '}${r.t.title}`);
        console.log(`          ↳ ${r.b}${r.b === here ? '   ← you are here' : ''}   ${age(r)}\n`);
      }
    }
    console.log('Git cannot tell you whether a branch LANDED — everything here squash-merges,');
    console.log('so a merged branch never becomes an ancestor of dev. The PR list is the truth:');
    console.log('  https://github.com/kevinrhaas/custom/pulls\n');

    if (cold.length) {
      console.log(`Cold — finished tickets, or branches older than a run (${cold.length}):`);
      for (const r of cold) {
        console.log(`  ${r.b}  (${r.t.id}, ${r.t.state}${age(r) ? ', ' + age(r) : ''})`);
      }
      console.log('  Most are leftovers whose PR merged; delete with `git push origin --delete <branch>`.\n');
    }

    // A claim with no branch behind it is the shape of an abandoned run.
    const orphans = tickets.filter((t) => ['claimed', 'review'].includes(t.state)
      && !rows.some((r) => r.t.id === t.id));
    if (orphans.length) {
      console.log(`Claimed in the merged files, with no branch on the remote (${orphans.length}) —`);
      console.log('a run that claimed and never pushed, or a branch already deleted:');
      for (const t of orphans) console.log(`  ${t.id}  ${t.title}${t.claimed_by ? `  [${t.claimed_by}]` : ''}`);
      console.log('');
    }

    const unmatched = branches.length - rows.length;
    if (unmatched > 0) console.log(`${unmatched} other branch(es) carry no ticket number (bakes, chores) — not listed.`);
    break;
  }
  case 'check': {
    const problems = check(tickets);
    if (problems.length) {
      console.error('ticket queue FAILED:');
      for (const p of problems) console.error('  - ' + p);
      process.exit(1);
    }
    const open = tickets.filter((t) => WORKABLE.includes(t.state)).length;
    const blocked = tickets.filter((t) => t.state === 'blocked-owner').length;
    console.log(`ticket queue OK — ${tickets.length} tickets, ${open} in the queue, ${blocked} waiting on the owner`);
    break;
  }
  default:
    console.log('usage: ticket.mjs new|claim|done|block|unblock|withdraw|restamp|split|list|inflight|board|check');
    process.exit(cmd ? 1 : 0);
}
