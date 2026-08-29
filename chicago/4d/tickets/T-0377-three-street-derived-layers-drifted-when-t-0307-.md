---
id: T-0377
title: Three street-derived layers drifted when T-0307 moved North Water Street, and dev's gate is red on all three
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---
PR #530 (T-0307) changed `data/streets/1835.json` and nothing else. Three committed
layers are DERIVED from the street lines and were not regenerated with it, so
`tools/check.sh` on an unmodified `origin/dev` fails three steps:

```
the dooryard plantings re-derive from the rule that dealt their stems     FAIL
the planted poplar rows re-derive from the rule that chose their greens   FAIL
the yard goods re-derive from the rule that chose their frontages         FAIL
```

Found on 2026-08-29 by T-0376's branch, which is byte-identical to `dev` on
`data/flora/**`, `data/yard/**` and `data/streets/**` — so the drift is a function of
dev's tree alone. Not fixed there, because a PR is one revertible unit and moving
plantings is a visible change that owes its own entry.

**Acceptance:** (never weakened to pass)

- The three generators are re-run and their outputs committed, so `check.sh` is green on
  an unmodified `dev`.
- The move is stated: how many stems, rows and goods changed position, and by how much.
- Whether the three should be re-derived by the same gate that catches them, or whether a
  street edit should be refused until they are, is answered in the PR rather than left.
- A changelog entry if anything a visitor can see moves; none if nothing does, said plainly.
