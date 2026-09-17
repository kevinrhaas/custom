---
id: T-1243
title: The 1812 shoreline: shore_1812_pre_cut gets its own dated trace, its bounds and its sources, and the state gate accepts a supplied 1812 line instead of requiring an empty one
state: claimed
epic: SOUTH_TIME
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0468
opened: 2026-09-17
closed: null
pr: null
claimed_by: run 9/17/2026, 9:14:16 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35230630566
---

The 1812 shoreline: shore_1812_pre_cut gets its own dated trace, its bounds and its sources, and the state gate accepts a supplied 1812 line instead of requiring an empty one.

Piece 1 of 4 of **T-0468 — Create an e1812 natural terrain epoch for the Fort Dearborn battle landscape**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (stated before working, and not weakened to pass)

1. `shore_1812_pre_cut` carries geometry of its OWN — a trace measured off a sheet
   that draws the pre-cut mouth, with its source, its observed date and its grade —
   and it is not, at any point, an alias of `shore_1835_harbor_cut`.
2. The reading's distance from the address date is stated as a limit rather than
   left implicit, and the liberty of carrying it back is recorded in
   `docs/LIBERTIES.md`.
3. `tools/check_shoreline_states.py` stops requiring the 1812 state to be EMPTY and
   starts requiring what it was really guarding: that no dated shore adopts a line
   from outside its own terrain epoch — asserted of a supplied state as well as a
   planned one, with self-test cases that fire when each is broken.
4. Nothing dated after 1812 is published as 1812 shore.

**What landed.** `tools/trace_shoreline_1830.py` traces the Harrison 1830 harbour
survey — the one plan this project holds of the natural mouth — off the same raster
and the same committed transform T-0883 stated and T-0882 checked, asserting the
stockade's ink still falls where that transform says before it measures anything
(8.0 px off its committed centre, against a 12 px tolerance). Two shore runs come out:
`south_shore_pre_cut` (688.8 m) and `north_shore_pre_cut` (999.1 m), in
`data/terrain/epochs/e1830_natural/shoreline.geojson`, both graded `inferred`.
The 1828 soldiers' channel and the lake edge are cut out by declared cuts, each
carrying its reason in the file. Three residual defects are named in `known_defects`
rather than smoothed away — about 60 m of the 1828 channel's western entrance, two
building-glyph spurs, and up to 5.2 m of standoff on a tight convex bend.

**What this piece does NOT do:** no water polygon, no sand bar, no hydrology
(T-1247), no terrain spec (T-1248), no heightfield, meshes or scene selection
(T-1246). The state's status is `supplied`, not `active`, for exactly that reason.
