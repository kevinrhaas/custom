---
id: T-0852
title: tools/ticket.mjs inflight has a three-hour cold window, so a run that claims and then reads for four hours is invisible to the next run
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

tools/ticket.mjs inflight has a three-hour cold window, so a run that claims and then reads for four hours is invisible to the next run.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**The measurement.** Cohort 14 (T-0509) was read twice on 2026-09-05 by two runs that could not see
each other; the two ledgers disagreed on 36 of the 76 people and T-0816 had to rule every one of
them. The second run filed this defect itself and the filing died with its branch.

**The mechanism.** `inflight` reports a branch as in flight only if it was pushed within the last
three hours, and files everything older under "Cold — finished tickets, or branches older than a
run". A run that claims, pushes its claim commit, and then reads sources for four hours drops out
of the hot list at exactly the moment duplicating it is most expensive. The heading is also
literally wrong for that branch: it is neither finished nor litter.

**Acceptance:** a branch whose ticket is still `claimed` is reported as in flight however long ago
it was pushed, with its age shown, and the cold list keeps its current meaning for everything else.
A self-test covers a claim older than the window. The tool stays offline — no PR lookup.

**Links:** T-0816 (the reconciliation this cost) · T-0509 · `chicago/4d/tools/ticket.mjs` § inflight.
