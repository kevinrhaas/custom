---
id: T-0405
title: Adding one signboard repaints every board alphabetically after it, and some lose a line
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

**Measured on T-0263's own diff, 2026-08-29.** One board was added to the town —
`frederick_thomas_shop`, on South Water Street east of Dearborn, because the
American settled its trade. `tools/generate_business_signboards.py` then rewrote
**eleven other boards** that have nothing to do with it, all over the town:

| board | mounting before → after | what the board says |
|---|---|---|
| `goss_cobb_saddlery` | wall → awning | loses `Lake & Canal Streets` |
| `h_jones_store` | awning → facade painted | unchanged |
| `hogan_store` | bracket → wall | **gains** `Merchants / Chicago—Illinois` |
| `madore_beaubien_house` | wall → awning | unchanged |
| `miller_house` | awning → facade painted | unchanged |
| `peck_store` | facade painted → bracket | loses `South Water Street` |
| `philo_carpenter_log_shop` | wall → awning | `Drugs and Medicines` → `Druggist` |
| `pruyne_kimball_drugstore` | wall → awning | loses `South Water Street` |
| `robert_kinzie_store` | awning → facade painted | unchanged |
| `sauganash_hotel` | awning → bracket | unchanged |
| `thomas_church_store` | facade painted → bracket | unchanged |

**The cause is a global cycle walked in a global order, not a local rule.** The
mountings are dealt from `MOUNTING_CYCLE` as the generator walks the selected
frontages, and the walk is in structure-id order. `frederick_thomas_shop` sorts
under `f`, so **every board from `g` onward advanced one position in its cycle**
— which is exactly the set above, and exactly nothing before it. The docstring's
stated intent is LOCAL: *"assigned so that no two boards within `NEIGHBOUR_M` of
each other share a mounting, a style or a ground colour"*. A rule that only has
to separate neighbours does not have to renumber the whole town to admit one
frontage in the middle of the alphabet.

**Why it matters beyond churn.** The mounting decides how many lines a board has
room for (`room < 3` drops the `place` line and swaps `trade` for
`trade_short`), so a reshuffle silently changes WHAT BOARDS SAY. Peck's board
stopped naming South Water Street, and Pruyne & Kimball's stopped naming it, for
no reason connected to Peck or to Pruyne. Carpenter's log shop stopped saying
`Drugs and Medicines` — the 1833 wording T-0130 chose for that specific shop to
distinguish it from his South Water store — and now says `Druggist`, which is the
other shop's line. Those are wording decisions the table argues case by case,
undone by an unrelated insertion.

It is also a review hazard: it puts ~190 lines of unrelated diff into every PR
that adds a storefront, which is where a real regression hides.

**Acceptance:**

- Adding one board to the middle of the set changes THAT board and any board
  whose `NEIGHBOUR_M` separation actually required a different deal — and no
  others. Demonstrate with the `frederick_thomas_shop` insertion re-run against
  its parent commit: the diff names the new board and, if any, the neighbours,
  with the separation that forced each one.
- The neighbour separation the docstring promises still holds afterwards, and is
  asserted rather than assumed.
- Any board whose wording changes as a consequence has that change argued in
  `SIGN_WORDING`'s own `why`, not produced by a shifted cycle.
- `tools/check.sh` re-derives the record byte for byte, as now.
