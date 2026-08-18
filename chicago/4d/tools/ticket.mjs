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
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, '..');
const DIR = path.join(ROOT, 'tickets');
const QUEUE = path.join(DIR, 'QUEUE.md');
const BOARD = path.join(DIR, 'BOARD.md');
const JSON_OUT = path.join(DIR, 'tickets.json');

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
const EPICS = ['RENDERING', 'TOWN', 'GROUND', 'FLORA', 'PIPELINE', 'META'];
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

function find(tickets, id) {
  const t = tickets.find((x) => x.id === id);
  if (!t) { console.error(`no ticket ${id}`); process.exit(1); }
  return t;
}

function queueIds() {
  if (!existsSync(QUEUE)) return [];
  return readFileSync(QUEUE, 'utf8').split('\n')
    .map((l) => /^(T-\d{4})\b/.exec(l.trim())?.[1]).filter(Boolean);
}

function queueAppend(t) {
  const cur = existsSync(QUEUE) ? readFileSync(QUEUE, 'utf8').replace(/\n+$/, '\n') : queueHeader();
  writeFileSync(QUEUE, cur + `${t.id} — ${t.title}\n`);
}

function queueReplace(id, rows) {
  // Children take the PARENT'S EXACT PLACE in the order. Appending them to the
  // bottom would silently demote work the owner had deliberately ranked — the
  // one thing this file's ordering rule exists to prevent. A split is a
  // clarification of what the work is, never a re-prioritisation of it.
  const lines = existsSync(QUEUE) ? readFileSync(QUEUE, 'utf8').split('\n') : [];
  const i = lines.findIndex((l) => l.trim().startsWith(id));
  if (i < 0) lines.push(...rows); else lines.splice(i, 1, ...rows);
  writeFileSync(QUEUE, lines.join('\n').replace(/\n+$/, '\n'));
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
    if (bare(cur) !== bare(next)) writeFileSync(file, next);
  };
  settle(BOARD, md);

  const strip = tickets.map(({ file, body, error, ...rest }) => ({
    ...rest, queue_rank: WORKABLE.includes(rest.state) ? rank(rest) : null,
  }));
  settle(JSON_OUT, JSON.stringify({ project: 'chicago-4d',
    generated_ct: at, tickets: strip }, null, 2) + '\n');
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
  for (const id of q) {
    if (!wantIds.includes(id)) problems.push(`QUEUE.md lists ${id}, which is not an open ticket`);
  }
  for (const id of wantIds) {
    if (!q.includes(id)) problems.push(`open ticket ${id} is missing from QUEUE.md — append it, do not reorder`);
  }
  const dupQ = q.filter((id, i) => q.indexOf(id) !== i);
  for (const id of new Set(dupQ)) problems.push(`QUEUE.md lists ${id} twice`);

  // The generated pair must be fresh — a stale board is the stale-build.json
  // fault (found on check_published's first run) wearing a new file name.
  const beforeB = existsSync(BOARD) ? readFileSync(BOARD, 'utf8') : '';
  const beforeJ = existsSync(JSON_OUT) ? readFileSync(JSON_OUT, 'utf8') : '';
  generateBoard(tickets);
  if (readFileSync(BOARD, 'utf8') !== beforeB || readFileSync(JSON_OUT, 'utf8') !== beforeJ) {
    problems.push('BOARD.md / tickets.json were stale — regenerated now; commit them '
      + '(run `node tools/ticket.mjs board` before every merge, like the changelog stamp)');
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
    const max = Math.max(0, ...tickets.map((t) => Number(/^T-(\d{4})$/.exec(t.id ?? '')?.[1] ?? 0)));
    const id = `T-${String(max + 1).padStart(4, '0')}`;
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
    const t = tickets.find((x) => path.basename(x.file) === args[0]) ?? find(tickets, args[0]);
    const max = Math.max(0, ...tickets.map((x) => Number(/^T-(\d{4})$/.exec(x.id ?? '')?.[1] ?? 0)));
    const old = t.id; queueRemove(old);
    t.id = `T-${String(max + 1).padStart(4, '0')}`;
    const dest = path.join(DIR, `${t.id}-${slugOf(t.title)}.md`);
    writeTicket(t); renameSync(t.file, dest); t.file = dest;
    if (WORKABLE.includes(t.state)) queueAppend(t);
    generateBoard(loadAll());
    console.log(`${old} → ${t.id}`);
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
    let max = Math.max(0, ...tickets.map((x) => Number(/^T-(\d{4})$/.exec(x.id ?? '')?.[1] ?? 0)));
    const rows = [];
    titles.forEach((title, n) => {
      max += 1;
      const id = `T-${String(max).padStart(4, '0')}`;
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
    queueReplace(t.id, rows);
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
    console.log('usage: ticket.mjs new|claim|done|block|unblock|withdraw|restamp|list|board|check');
    process.exit(cmd ? 1 : 0);
}
