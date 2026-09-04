---
id: T-0690
title: dev is red at mobile part 8: the road-legibility aid moves the frame by 3 cells where the gate wants 4
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

dev is red at mobile part 8: the road-legibility aid moves the frame by 3 cells where the gate wants 4.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-0446's run on 2026-09-04, and **proved inherited before it was filed**.

`tools/smoke_renderer.mjs` part 8 asserts that turning the road-legibility aid
full on moves the rendered frame:

    FAIL  mobile 390x780: raising the road-legibility aid reaches the render
          — set to 1, reads back 1: cell delta mean 0.36, worst 3
            (need worst>=4, mean>=0.15)

The mean clears its floor comfortably. It is the **worst-cell** half of the
requirement that misses, by one cell.

**It is dev's, not any branch's.** Run on a clean `origin/dev` worktree at
`a6d8909d`, `SMOKE_VIEWPORT=mobile SMOKE_STAGE=8`, the same assertion fails with
`mean 0.35, worst 3` — the same worst cell, one hundredth apart in the mean. The
T-0446 branch, which adds two streets, reads `0.36 / 3`: it moved the number the
RIGHT way and did not move the verdict.

Worth noting beside it, from the same log and not yet accounted for: the road-band
report in part 7 says **9 bands moved against the bank**, four of them `rose` by
1.3 to 4.4 ΔL* and six of them `ungated` — "was gated when banked and is not gated
now — either the probes stopped projecting or the station moved". A town whose
roads have become markedly more legible on their own is exactly the state in which
an aid that adds legibility would have less left to add, so the two readings may
be one fault. That is a hypothesis and this ticket does not assert it.

Desktop is not measured here — only mobile part 8 was read.

**Acceptance:** either the aid moves the frame by the four cells the gate asks
for, or the gate's worst-cell floor is re-derived from what the aid can actually
do at 390x780 and the reasoning is written down. Whichever it is, `origin/dev`
comes back green at mobile part 8, and the nine moved road bands are explained or
re-banked.
