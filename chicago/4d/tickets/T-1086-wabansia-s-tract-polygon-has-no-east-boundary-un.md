---
id: T-1086
title: Wabansia's tract polygon has no east boundary until the water-lot wedge is seated, and place_vocabulary still calls the tract undecided on ground the project now commits
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-12
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Wabansia's tract polygon has no east boundary until the water-lot wedge is seated, and place_vocabulary still calls the tract undecided on ground the project now commits.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

FOUND BY T-1070, 2026-09-12, seating Wabansia. Two loose ends the seating recorded rather
than closed, together because the same reading closes both.

**1. The tract has no outline.** T-1070 publishes
`data/traces/wabansia_seating.json` § `block_grid_polygon_local_enu_m` and deliberately
does NOT call it the tract's: Wabansia runs east of the block grid to the North Branch,
over the water-lot wedge — Kain's and Hight's subdivision — which T-1077 read as a lot
strip and said in its own words it did not seat. Until that wedge is on modern ground the
tract has no east boundary, and this project will not draw one it cannot derive. The same
file's `tract_polygon_local_enu_m` is `{"seated": false}` with that reason in it.

**2. `place_vocabulary.json` is now stale about this ground.** It resolves `Wabansia` as
UNDECIDED on basis **B4** — "a survey adjacent to the town that this project commits none
of (Kinzie's Addition, Wabansia — T-0789, T-0790)" — and names T-0790 as the ticket that
would settle it. That sentence is false of the ground as of this seating, and it is false
of Kinzie's Addition too: T-1060 committed its streets. A Democrat notice naming Wabansia
therefore still lands `undecided` on a rule whose stated reason has expired.

**Why it is not a one-line edit.** B4 is the owner's ruling and moving a place off it
changes what counts as a Chicago appearance, which re-scores the register's person counts.
`outside` is the likely answer for both tracts — they are adjacent to the platted town,
not in it — but "likely" is not how this file is written, and the B-rules are his.

**Acceptance:**

1. The water-lot wedge seated off the same datum, and Wabansia's tract polygon derived
   from the grid's west and north bounds, Kinzie Street, and the wedge's river edge.
2. `tract_polygon_local_enu_m` filled by the same gated tool, with the committed west bank
   cross-check stated — T-1070 measured T-1074's tier-4 block corner 66 m inside that bank
   and refused it; a tract boundary meets the same question.
3. `place_vocabulary.json` re-ruled for `Wabansia` AND `Kinzie's Addition` — by the owner,
   or blocked on him — with the register's before/after person counts in the PR.

**Links:** T-1070 · T-1077 · T-1074 · T-0790 · T-0789 · T-1060 ·
`data/research/newspapers/place_vocabulary.json` § B4
