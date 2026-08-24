---
id: T-0190
title: The South Water placements stand out past the committed plat, and the walk breaks on them
state: blocked-owner
epic: TOWN
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-0127
opened: 2026-08-24
closed: null
pr: null
claimed_by: run 8/24/2026, 11:26:34 AM CT
blocked_on: Does a South Water business-front lot carry a documented store at the street AND an anonymous dwelling behind it (b), or does the lot rule hold and the town give back six principal roofs and two yard buildings (a)? See the ticket's fork; the whole plat repair is derived and waiting on the answer.
needs_bake: false
---

The South Water placements stand out past the committed plat, and the walk breaks on them.

Piece 1 of 5 of **T-0127 — The rest of the town gets the street edge**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

Ten documented buildings on the south side of South Water Street were placed against the
MODERN kerb, read off OpenStreetMap, rather than against this project's own committed plat,
and stand up to 6.9 m out past the platted lot line — inside the 80 ft corridor, nearly to
the travelled track. `tools/measure_corridor_intrusion.py` names them and measures the depth:
`h_jones_store` 8.17, `chicago_american_office` 6.91, `jh_kinzie_forwarding_store` 6.87,
`carpenter_south_water_store` 6.62, `frederick_thomas_shop` 6.25, `madore_beaubien_house`
5.98, `pruyne_kimball_drugstore` 5.55, `harmon_loomis_store` 5.31, `chicago_democrat_office`
5.11, `peck_store` 4.51.

That is why T-0069's walk on South Water comes out in pieces — 15.6 m and 20.8 m runs of a
97 m face — while Lake Street's runs whole: the march refuses every step a wall stands on,
and on this street the walls stand on the walk.

**What the sources actually fix, and what they do not.** Every one of these records cites a
street and a landmark — "on Water Street, near the draw-bridge", "at Clark", "on South Water"
— so the ALONG-STREET position is argued from a source and is not this ticket's business.
The SETBACK is not in any source: it came from `osm_streets_2026`, a 2026 kerb line, and this
project's answer to "where is the lot line" is its own committed plat
(`data/traces/vectors/thompson_lots.json`, re-derived by `tools/generate_plat_lots.py`).
Reconciling the setback with the plat is therefore not moving a building to make a number
smaller — the number it is measured against is the one the record should have used.

**Acceptance:** each of the ten either stands with its street-facing wall at or behind the
committed South Water frontage line — moved along the street's own normal only, its
along-street coordinate untouched, with the derivation and the metres recorded in its
`position.note` — or is refused in writing, per store; `measure_corridor_intrusion.py`
reports none of the ten lapping South Water's corridor and its baseline is rewritten to
record the repair; `tools/generate_frontage_works.py` re-derives and South Water's walk runs
unbroken along each face except where its own ground refuses it; `tools/check.sh` and
`tools/smoke_renderer.mjs` pass. Never by weakening a gate.

**Not in this ticket:** more streets (T-0191, T-0192, T-0193), hitching posts (T-0194), and
the shadow lever T-0115's ledger names — that is T-0192's to spend, since it is the piece
whose metres need it.

---
## 2026-08-24 — THE REPAIR IS DONE AND DERIVED. It collides with the block programme, and that collision is the owner's fork.

**What is on the branch `steward/t-0127-south-water-plat`, measured rather than described.**

Eleven records moved — the ten this ticket names, plus `temple_building`, which the walk found:
with the ten back on the plat it was the ONE remaining wall standing on a plank walk anywhere
on South Water, refusing the first 10.2 m of `blk_south_water_franklin`'s north face, and its
fault is the ten's fault exactly (an `osm_streets_2026` setback). Each was moved SOUTH along
South Water's own normal by the smallest translation, to the centimetre, that puts every
sampled point of its footprint outside the corridor `tools/plat_corridors.corridors()` builds
from the committed centreline and the committed 12.192 m platted half-width. No `local_e`
moved. Every metre is recorded in the record's own `position.note`.

| record | was inside the corridor | moved south |
|---|---|---|
| `h_jones_store` | 8.17 m | 8.18 m |
| `chicago_american_office` | 6.91 m | 6.92 m |
| `jh_kinzie_forwarding_store` | 6.87 m | 6.88 m |
| `carpenter_south_water_store` | 6.62 m | 6.62 m |
| `frederick_thomas_shop` | 6.25 m | 6.25 m |
| `madore_beaubien_house` | 5.98 m | 5.99 m |
| `pruyne_kimball_drugstore` | 5.55 m | 5.55 m |
| `temple_building` | 5.49 m | 5.68 m |
| `chicago_democrat_office` | 5.11 m | 5.12 m |
| `harmon_loomis_store` | 5.31 m | 5.31 m |
| `peck_store` | 4.51 m | 4.51 m |

**What it bought, which is the acceptance's own test.** `tools/generate_frontage_works.py`
re-derives and the town's street edge goes from **1,147.7 m of plank walk in 21 runs** to
**1,297.3 m in 18 runs**, with **9 corner crossings becoming 11** and 86 walking decks
becoming 96 — fewer, longer, joined-up walks. On South Water's own five faces the walk goes
from 237.2 m in nine broken pieces (46–71 m of a 97 m face) to 376.5 m in six runs plus two
new corner crossings, and three faces now run whole. **The march refuses ZERO steps for a
wall anywhere on South Water.** Every remaining refusal on that street is its own ground —
0.07–0.13 m of roll under one walking deck, and one step at +0.02 m, at or under the water —
which is what the acceptance asked for in those words.

`tools/measure_corridor_intrusion.py`: **29 lapping phases become 21**, eight cleared outright
and three left shallow. `tools/check.sh` passes every step it failed on the way here — the
staleness gate (placement is not in the mesh hash, so this costs no bake), the 665 programme,
the census, the intrusion ratchet with its baseline rewritten to bank the repair.

## THE COLLISION, and why this ticket stops here

`tools/generate_block_infill.py --check` fails, and it is right to.

A lot is occupied by whatever footprint reaches inside its 1.5 m buildable inset
(`plat_occupancy.occupied_lots`, T-A7). While these eleven stood out in the roadway, six of
them reached only the margin strip of their own lots — `blk_south_water_franklin`'s
arrangement note says so in as many words, measuring J. H. Kinzie's lap at *"9.7 m², all of
it in the 1.5 m margin strip"*. **Put them back on the plat and they seat.** Six lots that
read free now read taken:

| block | lot | now seats | which the block parcel had dealt to |
|---|---|---|---|
| `blk_south_water_franklin` | 2 | `jh_kinzie_forwarding_store` | a frontage roof |
| `blk_south_water_wells` | 0 | `h_jones_store` | a frontage roof **and** a yard building |
| `blk_south_water_wells` | 2 | `carpenter_south_water_store` | a frontage roof |
| `blk_south_water_clark` | 2 | `pruyne_kimball_drugstore` | a frontage roof |
| `blk_south_water_dearborn` | 0 | `chicago_american_office` | a frontage roof **and** a yard building |
| `blk_south_water_dearborn` | 2 | `frederick_thomas_shop` | a frontage roof |

Six anonymous principal roofs and two yard buildings, across four blocks. **Nothing overlaps
anything** — every one of the eleven was checked against every committed footprint in the
town and the worst overlap is zero. The store stands at the street and the cottage stands
behind it, and they fit. What fails is a RULE: one principal roof to a lot.

**So the finding underneath the finding is this.** The block programme dealt six principal
roofs onto lots that documented buildings actually stand on, and it passed its own occupancy
gate only because those buildings were drawn out in the road. The plat reconciliation did not
create that; it made it visible.

## THE FORK — and it is not a number that can be derived

**(a) The lot rule holds, and the town gives the roofs back.** Each affected block's South
Water face has only two free even lots left, so the frontage runs shrink: franklin 3→2, clark
2→1, wells 3→1, dearborn 3→1. Eight roofs leave the town (338 standing → 330), four block
recipes and their arrangement notes are re-authored, and the households whose `lives_at`
names a removed roof have to be re-homed or leave with it — `..._franklin_d3_03` and
`..._dearborn_d3_03` are dealt to the lots in question and both carry households. Honest,
and it costs the business front its density.

**(b) A business-front lot may carry a documented store at the street and an anonymous
dwelling behind it.** Nothing physical objects — the footprints already fit. The occupancy
rule is relaxed for `stands_on: frontage` where the standing building is documented, the
block parcels keep every roof, and no household moves. Cheaper, more urban, and it is a
statement about what a South Water lot WAS.

**This is the owner's, not the loop's.** It is the same argument T-0143 and T-0188 are about —
the core density standard — and it decides whether the town's business front is one roof to a
lot. Deriving it either way inside a sidewalk ticket would be settling a density question by
side effect. **Recommendation, if the owner wants one: (b)**, because the geometry already
permits it and (a) pays eight roofs and two households for a rule the corrected data has just
called into question.

**The branch is left OPEN with `hold`**, carrying the whole repair, so whichever way this
goes the eleven records do not have to be re-derived. `tools/publish.sh` was deliberately NOT
run: nothing here is shipping yet.

**Also filed on the way:** **T-0195** (three of the eleven still lap the CROSS street's
corridor by 0.10–0.31 m at their corners — moving south cannot reach that and moving along
the street would move the axis the sources argue) and **T-0196** (four buildings still stand
on LAKE Street's walk, the same OSM-kerb fault, and downstream of this same fork).

## Verification actually run, in the foreground

- `./tools/check.sh` — every step green **except** `generate_block_infill.py --check` (the fork
  above) and `check_published.mjs` (only because `publish.sh` was deliberately not run — the
  failure names exactly the eleven sidecars and the frontage record, and nothing else).
- `tools/smoke_renderer.mjs` at **390x780, all nine stages: 208 + 80 + 152 = 440 checks, 0 failed.**
  The frontage layer's pinned census in the smoke moved with the walk and was updated with it —
  walks 29→26, crossings 12→14, fence runs 12→11, meshes 38→35 (the town street edge's culling
  chunks are one per run of sidewalk, so twenty-one became eighteen). Those are the layer's shape,
  not a threshold, and no gate was loosened.
- `tools/smoke_renderer.mjs` at **1280x800, stages 1-3: 208 checks, 0 failed**; **stage 4: one
  failure, and it is not this branch's.** `scene detail 'balanced' stays inside its own ceiling at
  the WORST stand` reports 1,235,088 tris of 1,210,000 at Lake Street at Canal — and `origin/dev`
  with these eleven records unmoved reports **the identical figure, to the triangle**. The stand it
  fails at is at the far west end of the town and the walk this ticket lengthened is on South Water
  in the east, so the layer contributes nothing there. Pre-existing, and T-0089 / T-0147's to carry.
- Desktop stages 5-9 not run: each leg costs about seven minutes against a ten-minute per-command
  ceiling, and with the branch already red on the block-parcel gate there is nothing for them to
  clear. They run before this merges.
