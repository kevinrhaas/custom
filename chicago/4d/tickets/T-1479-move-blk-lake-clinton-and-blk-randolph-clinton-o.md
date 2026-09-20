---
id: T-1479
title: Move blk_lake_clinton and blk_randolph_clinton onto the West Division grid: blocks 28 and 45 re-cut in the sheet's own arrangement, with the structures seated on their lots re-seated
state: open
epic: GROUND
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-20
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: null
---

Move blk_lake_clinton and blk_randolph_clinton onto the West Division grid: blocks 28 and 45 re-cut in the sheet's own arrangement, with the structures seated on their lots re-seated.

Found working T-1455, which cuts the West Division's own grid. Two cells stand in both
grids — `blk_lake_clinton` (plat block 28) and `blk_randolph_clinton` (block 45) — and
T-1455 left them on the Original Town's grid, carried in the West Division's omissions
with `already_derived_as` and the reason.

**Why they were left.** Both are on the SOUTH Division module: four lots to a face with
an east-west alley, which the sheet's own reading says is the wrong arrangement for
them. Re-cutting them moves ten lot lines each — and committed structure records are
seated against those lots by name (`recon_1835_blk_randolph_clinton_*`, and
`plat_occupancy.py` reports `recon_1835_west_018` lapping onto `blk_randolph_clinton`
lot 2). That is a re-seat and a bake, not a lot-layer change.

**And both print no dimension**, so under T-1455's own rule this grid would WITHHOLD
their lot lines rather than re-cut them — which would take lots away from structures
standing on them. The first question this ticket has to answer is what a structure
seated on a withdrawn lot is seated on.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)
