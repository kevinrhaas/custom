---
id: T-0760
title: ticket.mjs inflight calls a 6-hour-old branch cold, so claim let a second run rebuild T-0509 on top of parked PR #831
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

ticket.mjs inflight calls a 6-hour-old branch cold, so claim let a second run rebuild T-0509 on top of parked PR #831.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**The finding.** `tools/ticket.mjs inflight` splits pushed branches into IN FLIGHT (pushed within
3h) and "Cold — finished tickets, **or branches older than a run**". `claim` reads the first list
only. A run that opens a PR and parks it leaves a branch that goes cold in three hours while its
ticket is still very much taken, and `claim` then waves the next run straight through.

That happened on 2026-09-05. Run A cut `steward/t-0509-cohort-14` at 02:58 UTC, did the whole
cohort, opened **PR #831** and labelled it `hold` — parked on a published-tree size budget it could
not pass. At 09:2x UTC run B ran `inflight`, saw no T-0509 row, claimed T-0509 unopposed, and
rebuilt the same 76-person cohort from scratch. It only found out at `git push`, which was rejected
non-fast-forward because the branch name was already taken. The second take is on
`steward/t-0509-cohort-14-rerun`.

The 3h window is the right heuristic for "is a run still alive"; it is the wrong one for "is this
ticket taken". A parked PR is the case that separates them, and it is a case this lane creates
deliberately every time a gate is red.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- `inflight` reports a branch whose ticket has an **open PR** regardless of the branch's age, and
  says the PR number and its labels — a `hold` PR is the loudest possible "taken".
- `claim` refuses a ticket that has an open PR without `--force`, with the PR's URL in the refusal.
- A branch older than 3h with **no** open PR keeps its current cold classification, so the corpse
  rule (AGENTS.md § THE QUEUE) is unaffected.
- A test covers the parked-PR case, since that is the one the current split gets wrong.

**Links:** PR #831 · `tools/ticket.mjs` (`inflight`, `claim`) · AGENTS.md § THE QUEUE.
