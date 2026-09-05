---
id: T-0730
title: The published tree is 793 bytes under its 32 MB budget on dev, so the next changelog entry or new ticket fails check.sh for every run in the lane
state: withdrawn
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: 2026-09-05
pr: null
claimed_by: null
blocked_on: Answered by events, not by the owner: the published-tree budget was re-budgeted from 32 to 36 MB in #823 (with the reasoning written into validate.py), and #836 (T-0722) stopped publishing changelog.js twice. dev now measures 31.73 MB of 36 MB, so the bookkeeping bytes this ticket priced no longer fail check.sh and T-0581's PR is no longer parked on them.
needs_bake: false
closed_at: 2026-09-05T18:24:38.068Z
claimed_run: null
---

The published tree is 793 bytes under its 32 MB budget on dev, so the next changelog entry or new ticket fails check.sh for every run in the lane

**MEASURED ON dev AT 06a0a9ec, 2026-09-05.** `tools/validate.py` sums every file under
`site/chicago/4d/` and fails over `SITE_BUDGET_MB = 32` (validate.py:112, :5409). On clean dev
the tree measures **31.9992 MB — 793 bytes of headroom.** The check passes today and reports
`published tree 32.00 MB of 32 MB budget`, which reads like a rounding note and is in fact the
last warning anyone gets.

**IT IS ALREADY SPENT.** Anything the house rules require a PR to do now blows it:

| what a normal PR adds to the published tree | bytes |
|---|---|
| one changelog entry, mirrored to `js/changelog.js` | ~3,255 |
| the same entry, mirrored again to `walk/js/changelog.js` | ~3,255 |
| two new tickets, via `ticket.mjs`'s automatic `tickets.json` mirror | ~1,355 |

T-0581 measured these on its own diff and came out **6,923 bytes over**. A changelog entry is
required by the contract; the `tickets.json` mirror happens on `ticket.mjs claim` whether the run
wants it or not. **So every run in this lane now fails `check.sh` on a byte count that has nothing
to do with its work**, and T-0581's PR is parked on `hold` for exactly this and nothing else.

**WHY IT ARRIVED TODAY AND WILL NOT STOP.** Two published files grow monotonically with every
merge and never shrink:

- `changelog.js` is **1,345.7 KB and published TWICE** — `site/chicago/4d/js/changelog.js` (the
  contract path Manager and the launcher parse) and `site/chicago/4d/walk/js/changelog.js` (what
  the walkthrough's What's-new tab imports). 543 entries, ~6.5 KB of budget per merge across the
  pair.
- `tickets.json` is **356.1 KB**, 661 tickets, and grows on every claim and every new ticket.

That is roughly 8 KB per merge of pure bookkeeping, against 0 bytes remaining.

**THIS IS THE OWNER'S CALL AND THE TICKET IS BLOCKED ON IT**, because all three answers are
architecture rather than cleanup and the wrong one is easy to reach for. Raising
`SITE_BUDGET_MB` because a PR failed is the "weakened to pass" move the house rules exist to stop,
so it is not taken here.

The options, with what each costs:

1. **Raise the budget.** The constant's stated reason is that GitHub Pages cannot serve Git LFS
   objects, which is a reason to keep binaries out of the tree, not a reason for 32 specifically.
   Pages' own limit is 1 GB. Cheapest, and it defers rather than fixes: the two files still grow.
2. **Stop publishing the changelog twice.** 1.35 MB — about forty merges of headroom — is a
   verbatim duplicate. `site/chicago/4d/js/changelog.js` is a named contract path and must not
   move; the `walk/` copy could import the published one instead of receiving its own mirror.
   Needs a look at whether the walkthrough can reach up a directory, which is the reason the
   duplicate exists in the first place.
3. **Age the published changelog out.** Ship the newest N entries to the site and keep the whole
   literal in `renderers/web/js/changelog.js`. Touches the changelog contract, which is sacred, so
   this needs the owner's word before a line is written.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- The owner's decision recorded, and the change made under it.
- `./tools/check.sh` green on dev with **at least 200 KB of headroom**, so the next twenty merges
  do not re-open this.
- If the answer is option 2 or 3, the What's-new tab and Manager's ingest both demonstrated still
  reading their changelog after the change.
- A note in `docs/` saying what the budget is for and what to do when it is next approached, so
  the next run finds a procedure instead of a wall.
