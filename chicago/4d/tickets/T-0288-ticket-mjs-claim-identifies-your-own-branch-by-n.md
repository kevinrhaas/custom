---
id: T-0288
title: ticket.mjs claim identifies your own branch by NAME, so it never warns about the rival branch that matters most
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

ticket.mjs claim identifies your own branch by NAME, so it never warns about the rival branch that matters most.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`node tools/ticket.mjs claim T-0096` was run at 11:56 on 2026-08-28 with
`steward/t-0096-fort-flagstaff` **already on the remote, carrying an open PR (#447) with four
hours of finished work on it**. The claim was granted without a word, and the whole ticket was
then built a second time, independently, before the collision surfaced at `git push`.

**The guard is `remoteBranchesFor()` in `tools/ticket.mjs`:**

```js
const here = currentBranch();
return remoteBranches()
  .filter((b) => b.name !== here && branchCarries(b.name, id))
```

`b.name !== here` is meant to stop a run warning about its own pushed branch. But **a branch name
here is a function of the ticket** — `steward/t-<id>-<short topic>` — so two runs working T-0096
land on the same name far more often than not. The exclusion therefore fires exactly when the
rival is real: the guard disables itself in the one case it exists for. Both runs had already
branched before claiming, which is what the tool's own instructions ask for ("claim in your first
commit").

**`inflight` did not cover the gap either.** The rival branch was pushed 4 h earlier, past
`RUN_HOURS`, so it was filed under *"Cold — finished tickets, or branches older than a run"* and
labelled *"likely litter"*. It was not litter; it was an open PR parked on `hold`. Age is a poor
proxy for abandoned when a PR can sit parked for review — and the tool already prints *"The PR
list is the truth"* without ever consulting it.

**Cost:** one full run duplicated. Both runs found the same source (Andreas vol. 1 p. 128), took
the same reading and refused the same two positions, which is a pleasing corroboration and an
expensive way to buy one.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`claim` refuses — or at minimum warns loudly — when a remote branch carries this ticket's number
and that branch is not one this run pushed. Identify "mine" by something that actually is mine:
the local branch's own commits, or the branch's absence from the remote at process start. Not by a
name the ticket id generates. Ship a test that fires when the guard is removed, in `tools/test_*`,
the way this repo's other guards carry one.

Consider also: `inflight` asking the PR list about any branch it is about to call cold, since the
open/closed state of a PR is the signal that age is standing in for.

**Links:** T-0238 (two parallel slices took the same ticket — different cause, same cost) ·
PR #447 (the parked run) · the PR that found this.
