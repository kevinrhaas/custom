---
id: T-0726
title: The published tree stands at exactly 32.00 MB of its 32 MB budget, so the next PR to add a changelog entry cannot pass the gate
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The published tree stands at exactly 32.00 MB of its 32 MB budget, so the next PR to add a changelog entry cannot pass the gate.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured 2026-09-05 on a clean worktree of `dev` at 3c814565, with nothing changed:**

```
site check: published tree 32.00 MB of 32 MB budget
PASS  0 error(s), 230 warning(s)
```

It passes with **zero** headroom. `check.sh` fails on `over the 32 MB budget`, so the
budget is inclusive at exactly 32.00 and one more kilobyte is a hard failure. T-0509
found this the way it will keep being found: its diff adds a changelog entry, which
`publish.sh` mirrors into `site/chicago/4d/js/changelog.js` AND
`site/chicago/4d/walk/js/changelog.js`, plus its rows in the `tickets.json` mirror —
about 6 KB in total — and the gate went red:

```
FAIL  site: published tree is 32.0 MB, over the 32 MB budget — GitHub Pages cannot
      serve Git LFS objects, so this has to stay lean
```

**This blocks every publishing PR from now on, not just that one.** Every 4D PR ships a
changelog entry by contract and every one of them runs `publish.sh`, so the next run to
reach its gate hits the same wall, and the one after that. It is not a slow drift any
more; it is a stop.

**Three candidates, cheapest first, and none of them is "raise the number":**

1. `site/chicago/4d/tickets.json` is a **660-ticket** mirror that the renderer never
   loads — `smoke_budget.mjs --for-diff` says so in as many words: *"the backlog mirror —
   the renderer never loads it"*. It is rewritten on every PR (342 lines of churn a time)
   and nothing served reads it. If the launcher or Manager needs it, ship a trimmed index
   of open tickets rather than the whole board.
2. The changelog is mirrored **twice** into the published tree, at `js/changelog.js` and
   `walk/js/changelog.js`, and both are 540-plus entries of prose. One of the two could
   be a redirect, or the published copy could carry the newest N entries with the archive
   fetched on demand.
3. Whatever the largest GLBs in the mirror actually are, measured rather than guessed.

Raising the budget is the one move to refuse without a reason: the number exists because
GitHub Pages cannot serve Git LFS objects, and that constraint has not changed.

**Links:** T-0509 (blocked by this; its PR is on `hold`) · `tools/check.sh` § site check
· `tools/publish.sh`.
