---
id: T-1429
title: The nearest-street reading crosses the river: a bank test for nearest_frontage, so a roof is not credited with a corridor on the far side of the water
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-20
closed: null
pr: null
claimed_by: run 9/21/2026, 6:07:19 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35591950221
---

The nearest-street reading crosses the river: a bank test for nearest_frontage, so a roof is not credited with a corridor on the far side of the water.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-1191 on 2026-09-20, and written up in full in that ticket's own file under
*Finding, 2026-09-20: the river is not in the reading*.

`measure_frontage_fabric.nearest_frontage()` takes the smallest straight-line distance
from a footprint to every committed corridor. That was harmless while only the south and
west grid had corridors, because everything the north bank could be measured against was
already across the water and the readings were recorded as outliers with authored reasons
saying so. T-1191 put the north bank's own corridors in the reading, and now the crossing
happens in both directions and can produce a FALSE conformance rather than a stated
outlier: `fort_dearborn_out_building_a` and `_b` stand inside the unplatted military
reservation on the south bank and read 198.31 m and 195.52 m off Kinzie Street on the
north bank, which is an ordinary street, so the ancillary clause's "avoids a principal
street" stops firing and `placement_policy_1835` reads both as conforming.

**What this asks for:** a bank test in `nearest_frontage` — a corridor separated from the
footprint by the main stem or a branch is not that footprint's frontage. The water this
would test against is already committed (`data/traces`, the terrain water mask).

**Why it is its own unit:** it moves every setback reading in the tree at once —
`measure_frontage_fabric`, `measure_face_rule`, `placement_policy_1835`, the frontage
baselines and the outlier reasons that quote distances — and each of those carries a gate
and a self-test that would have to be re-read against the new numbers.

**Acceptance:** the two reservation out-buildings are outliers again, with their reasons
restored; every reading whose street changes is stated with its before and after; no
confidence and no coordinate moves.
