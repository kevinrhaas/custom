---
id: T-0802
title: A ticket whose PR merged can sit 'claimed' forever, because nothing compares ticket state against the PRs that landed
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

A ticket whose PR merged can sit `claimed` forever, because nothing compares ticket state
against the PRs that landed.

**The instance.** T-0429 shipped in PR #597, merged to `dev` 2026-09-01T00:40:50Z. The run
died before `ticket.mjs done`, so the ticket stayed `claimed` and stayed in
`list --workable`. Five days later it was still the topmost ticket in the queue carrying no
PR, which is exactly the shape of available work. One branch
(`steward/t-0429-south-water-lasalle`) rebuilt the whole block on the strength of that
reading — 116 files, 5,827 insertions, baked — and every record it produced already existed
on `dev` under the same id.

**Why the existing guards do not catch it.** `inflight` is the guard for this class, and it
is honest about its own blind spot: everything here squash-merges, so a merged branch never
becomes an ancestor of `dev` and `inflight` deliberately refuses to claim a branch landed. It
sorts on branch AGE instead, so T-0429's branch showed as *cold* — correctly — and cold reads
as litter, not as done. `ticket.mjs check` polices sizing and queue membership, not staleness.
Nobody is wrong; there is simply no check that asks the one question that settles it.

**The question that settles it, and it is cheap.** For each ticket not in a terminal state,
does a MERGED PR exist whose title carries its id? That is one REST call
(`/repos/kevinrhaas/custom/pulls?state=closed`), it is the same evidence a human uses, and it
is decisive in the direction that matters: a merged PR naming T-NNNN is strong evidence the
work landed, while its absence proves nothing and should stay silent. Report, never fail —
the id in a title is a convention, not a contract, and a gate that hard-fails on a naming
convention will block a run that did nothing wrong.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- A tool (`ticket.mjs` subcommand, or a check next to `inflight`) reports every non-terminal
  ticket for which a merged PR names its id, with the PR number and merge instant.
- Run against today's `dev` it reports **zero** — T-0429 was the only one, and this ticket's
  own PR closes it. The demonstration is therefore against a constructed case, not a live
  one: feed it a ticket id known to be `done` and show it would have fired.
- It REPORTS. It does not fail `check.sh`, and it says in its own output why not.
- No network, or a rate-limited call, degrades to silence — never to a false accusation.
  `inflight`'s best-effort construction is the precedent to follow.

**Links:** T-0429 · `tools/ticket.mjs` § `inflight` · `tickets/README.md` § *A claim is only
real once its PR merges*, which names this exact failure and costs it at ~70 minutes of loop
time per recurrence.
