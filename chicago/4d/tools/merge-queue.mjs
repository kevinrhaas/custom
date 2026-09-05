#!/usr/bin/env node
/**
 * The git merge driver for tickets/QUEUE.md.
 *
 * WHY A DRIVER AND NOT `merge=union`. The changelog tried union and the repo's
 * own .gitattributes records what it cost: union is a LINE union, a changelog
 * entry is many lines, and the shared closing bracket survived once, so one
 * entry swallowed the next and produced valid JavaScript nobody noticed. Five
 * merges in one day, each repaired by hand.
 *
 * QUEUE.md is line-structured — one ticket is exactly one line — so union would
 * not corrupt it silently the way it corrupted the changelog, and `ticket.mjs
 * check` catches every union failure mode loudly (`lists X twice`, `is not an
 * open ticket`, `missing from QUEUE.md`). But loud is not the same as resolved:
 * on the case that actually hurts — one side re-ranks the file while the other
 * closes tickets — union concatenates BOTH orderings and hands back ~300 lines
 * with every ticket twice. That is a conflict wearing a merge's clothes.
 *
 * WHAT THIS DOES INSTEAD, and it is the reconciliation done by hand four times
 * on 2026-09-04 while landing one queue re-rank:
 *
 *   result = OURS,  minus every ticket THEIRS removed since the base,
 *                   plus  every ticket THEIRS added since the base.
 *
 * OURS keeps the ORDER, because order is the owner's and the branch being merged
 * into is the one holding his instruction. THEIRS contributes membership, because
 * a ticket dev closed is closed and a ticket dev filed is real. The two sides
 * change different things about this file almost every time — one re-ranks, the
 * other opens and closes — which is exactly why a set reconciliation works where
 * a text merge cannot.
 *
 * IT REFUSES RATHER THAN GUESSES. If the result would carry a duplicate id, the
 * driver exits non-zero and git leaves the normal conflict markers for a human.
 * A queue with a ticket in it twice is a ranking nobody can read.
 *
 * Registered by `tools/setup-merge-drivers.sh` (merge.queue.driver), declared in
 * the repo's .gitattributes. If the driver is NOT registered, git falls back to
 * the ordinary text merge and you get conflict markers — the old behaviour, never
 * something worse. `check.sh` says so when it notices.
 *
 * Usage (git calls this, you do not):  merge-queue.mjs %O %A %B %P
 *   %O base   %A ours (READ AND WRITTEN — the result goes here)   %B theirs   %P path
 */
import { readFileSync, writeFileSync } from 'node:fs';

const [base, ours, theirs, label = 'QUEUE.md'] = process.argv.slice(2);
if (!base || !ours || !theirs) {
  console.error('usage: merge-queue.mjs %O %A %B %P');
  process.exit(2);
}

const TICKET = /^(T-\d{4})\b/;
const read = (p) => {
  try { return readFileSync(p, 'utf8'); } catch { return ''; }
};
/** id -> the whole line, for every ticket line in a version of the file. */
const index = (text) => {
  const m = new Map();
  for (const line of text.split('\n')) {
    const hit = TICKET.exec(line);
    if (hit) m.set(hit[1], line.replace(/\s+$/, ''));
  }
  return m;
};

const baseText = read(base);
const oursText = read(ours);
const theirsText = read(theirs);

const B = index(baseText);
const O = index(oursText);
const T = index(theirsText);

const closedByThem = [...B.keys()].filter((id) => !T.has(id));
const addedByThem = [...T.keys()].filter((id) => !B.has(id));

/**
 * WHICH SIDE'S ORDER WINS, and this is the question the first version got wrong.
 *
 * It ordered on "OURS keeps the order", reasoning that the branch being merged into
 * is the one holding the owner's instruction. That is true when ours is the newer
 * work. It is FALSE, and destructively so, when a long-stale branch merges dev: then
 * "ours" is the branch that predates the owner's re-rank, its old order wins, and the
 * moment that branch merges the old order is carried back onto dev.
 *
 * That happened on 2026-09-04. Four PRs cut before a research-first re-rank each
 * merged dev; each kept its own stale order; and the owner's ranking was gone from
 * dev by the fourth — "the queue got massively reordered, we were working on all of
 * the research items first".
 *
 * The honest rule is not about which side is "ours". It is about WHICH SIDE ACTUALLY
 * RE-ORDERED. Compare the relative sequence of the ids all three versions share:
 *   - only ours moved them   -> ours ordered deliberately; keep ours.
 *   - only theirs moved them -> theirs ordered deliberately; keep theirs.
 *   - neither moved them     -> no disagreement; keep ours (identical anyway).
 *   - BOTH moved them        -> two deliberate rankings; REFUSE and let a human read.
 */
const seq = (m) => [...m.keys()].filter((id) => B.has(id) && T.has(id) && O.has(id));
const sameOrder = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
const baseSeq = seq(B); const oursSeq = seq(O); const theirsSeq = seq(T);
const oursReordered = !sameOrder(baseSeq, oursSeq);
const theirsReordered = !sameOrder(baseSeq, theirsSeq);
if (oursReordered && theirsReordered) {
  console.error(`merge-queue: ${label} — BOTH sides re-ranked the queue since the merge base. `
    + 'Two deliberate orderings cannot be merged mechanically; resolve by hand and keep the '
    + "one the owner asked for. (This refuses rather than silently picking a side — picking "
    + 'one is how a stale branch erased a re-rank on 2026-09-04.)');
  process.exit(1);
}
// The side that did the re-ranking supplies the file we walk; the other supplies membership.
const orderingText = theirsReordered ? theirsText : oursText;

// Walk the ordering side line by line so every comment, band header and blank line
// survives exactly where the owner put it. Only ticket lines are filtered.
const dropped = theirsReordered
  ? [...B.keys()].filter((id) => !O.has(id))     // what OURS closed
  : closedByThem;
const out = [];
for (const line of orderingText.split('\n')) {
  const hit = TICKET.exec(line);
  if (hit && dropped.includes(hit[1])) continue;
  out.push(line);
}

// Their new tickets land at the END, under a band that says where they came from
// and that nobody has ranked them yet — the same place `ticket.mjs new` puts one.
const present = new Set(out.map((l) => TICKET.exec(l)?.[1]).filter(Boolean));
const toAppend = [...new Set([...addedByThem, ...[...O.keys()].filter((id) => !B.has(id))])]
  .filter((id) => !present.has(id));
if (toAppend.length) {
  while (out.length && !out[out.length - 1].trim()) out.pop();
  out.push('');
  out.push('# --- MERGED IN, NOT YET PLACED. These arrived on the branch being merged and were');
  out.push('# --- appended here rather than guessed into a band. Rank them or leave them.');
  for (const id of toAppend.sort()) out.push(T.get(id) ?? O.get(id));
}
out.push('');

const merged = out.join('\n').replace(/\n{3,}$/, '\n');

// The one thing worth refusing over.
const ids = merged.split('\n').map((l) => TICKET.exec(l)?.[1]).filter(Boolean);
const dupes = [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))];
if (dupes.length) {
  console.error(`merge-queue: ${label} would carry ${dupes.join(', ')} twice — refusing, `
    + 'resolve by hand. A queue with a ticket in it twice is a ranking nobody can read.');
  process.exit(1);
}

writeFileSync(ours, merged);
const note = [];
if (closedByThem.length) note.push(`-${closedByThem.length} closed`);
if (toAppend.length) note.push(`+${toAppend.length} new`);
console.error(`merge-queue: ${label} reconciled — ${theirsReordered ? "theirs'" : "ours'"} order kept`
  + (note.length ? `, ${note.join(', ')}` : ', no membership change')
  + `, ${ids.length} queued.`);
process.exit(0);
