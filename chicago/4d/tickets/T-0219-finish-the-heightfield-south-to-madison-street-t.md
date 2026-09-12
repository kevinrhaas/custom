---
id: T-0219
title: Finish the heightfield SOUTH to Madison Street, the plat's last tier
state: open
epic: GROUND
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

Finish the heightfield SOUTH to Madison Street, the plat's last tier. The mirror of
T-0010 / ROADMAP T-E3's eastern extension, and **the only route to any of the South's
120 remaining roofs.**

**Why, measured (T-0026, `tools/measure_southern_ground.py`).** The modelled box ends at
local **N -400 m**, and that line falls *inside* Washington Street's own 80 ft platted
corridor — 0.33 ha of that street's south half, over 899 m of its length, is already off
the field. South of the corridor the field holds **0.0819 ha** of land above the water
surface and **0.0000 ha** of it is in the South Division: every cell is west of local
E -10, the West Division bank across the South Branch. Madison Street — the 1830 plat's
south boundary, resolved from the PLSS section corner at State & Madison — is **125.2 m**
further south again, so the plat's last tier of blocks (**6 blocks, 48 lots, 6.28 ha**,
Market to State) has **0 of 24** block-boundary points on modelled ground.

**What it needs from the traces, and it is narrow.** The box's `n_min` is capped by
evidence rather than by cost, and the evidence is about ONE river: the spec says a box
reaching further south *"would show open prairie where the river actually continues"*, and
that river is the South Branch, whose traced water ends at **N -405.2** (west bank) /
**-404.3** (east bank). Everything else already reaches past Madison — the harbour-reach
shoreline to **N -589.2**, the sand bar to **N -436**. So the work is the South Branch's
two banks carried from N -405 to about **N -531 (126 m per bank)** off a sheet this project
already holds, then `n_min` moved in `terrain_spec.json`, then a bake. The tier itself is
dry ground: at N -400 the branch occupies local E -8 to +35 and the tier runs E +88
(Market) to +826 (State).

**Street control is NOT the blocker and must not be carried first.** Every north-south
column of the south plat has its committed centreline cut at exactly N -400, the field's
own south edge; the modern control that would carry them further is already committed
(`G1` is an OpenStreetMap node with an id and a 13.9 m residual). Carry the lines without
the ground and `tools/generate_plat_lots.py` emits six blocks whose every placement
`tools/generate_block_infill.py` refuses for standing outside the modelled terrain —
`tools/measure_southern_ground.py --gate` now fails at the commit if that happens.

Ground **east of State** is not part of this and is not coming at any date: it is the
United States Reservation (T-E2, `data/reconstruction/1835_no_build_ground.json`).

**Acceptance:** the committed heightfield covers the plat's Washington–Madison tier;
`tools/measure_southern_ground.py` reports the tier's block-boundary points on modelled
ground and the figure is no longer zero; `tools/reconcile_665.py` re-derives and the South
balance's `waiting_on` moves off terrain of its own accord; `tools/check.sh` green. The
South Branch's extended banks are traced and sourced like every other trace — **or** the
reason they cannot be is recorded and this ticket closes with it, in which case the South's
120 roofs are gated permanently and the programme should say so.

**Prior attempt: PR [#432](https://github.com/kevinrhaas/custom/pull/432), closed unmerged 2026-09-05 under T-0803.**
Opened 2026-08-28; by the time it was read it stood **672 commits behind `dev`** with 54
changed files, re-tracing the river and rebuilding the heightfield and the terrain/water
GLBs on top of a `dev` that has since moved the South Branch's east bank (T-0686, #882)
and re-derived north_water twice (T-0780, #889). **Read its PR body before starting** — it
is the reasoning archive for this ticket and it is not thrown away. In particular it
records four faults the extension exposed and fixed, each of which will recur: the raster
cache ignored `REGION`; `upsample` measured the block grid against the image rather than
the block size; a sheet stain read as riverbank and fused a 190 m false lobe across four
platted blocks; and `open_lake` would have built 465 m of invented coastline where no
traced water reaches the guard. It also filed **T-0253** for a 5.1 m regression on
`blk_south_water_franklin`'s north face.

Its branch could NOT be deleted from the session that closed it — this environment's proxy refuses a ref delete over both git and the REST API (HTTP 403) — so `ticket.mjs claim` **will see it as a rival branch and refuse**. That refusal is a false stop: the PR is closed and the branch is abandoned. `claim T-0219 --force` is correct here. `ticket.mjs inflight` reads it as COLD, which is the honest signal.

## FINDING, 2026-09-12: this is an L, and the blast radius is the NORTH bank

Attempted on `steward/t-0219-heightfield-madison`, parked on `hold`. The SOUTH half of
this ticket is done and measured; what it cannot carry inside one run is a cascade nobody
had costed, and the cascade is at the other end of the box.

**What is finished and green.** The window is 280 px taller, both South Branch banks come
south with it, `n_min` is Madison's line at N -530, the heightfield is 809 x 373 and the
terrain and water GLBs are baked from it (ground mesh vs heightfield max 3 mm, rms 0.2 mm
over 33,750 rays). Every acceptance clause about the south is met:
`measure_southern_ground.py` reports **24 of 24** tier boundary points on modelled ground
against the 0 of 24 this ticket was filed for, Washington's corridor is wholly on the
field, and `reconcile_665.py` moved the South balance's `waiting_on` off TERRAIN to
STREET CONTROL of its own accord. `tools/validate.py --all` is **green, 0 errors**.

**Why it is an L.** The window cannot be widened without also fixing how the local paper
background is measured (`upsample` read the block grid against the image height, so the
background under every pixel depended on how tall the window happened to be). That fix is
not optional and it is not local: it moves the WHOLE trace by up to 2.20 m — measured, by
the `--check-north` this attempt implemented because the comment claiming it had named a
flag that never existed. The north bank moves with everything else, and a great deal of
the town is placed against the north bank. Re-deriving what follows is the real cost:

  * done here — the four dooryard/planted-row/yard-goods/river-wharf derivations, the
    frontage works, the Kinzie Block reading, the planting-reach baseline, the north-bank
    frontage baseline, `compile_scene`, and North Water Street itself, which needed a real
    repair: its derivation targets the bank's offset curve and lets the fit sit below it,
    so at the exempt terminus the fitted vertex landed inside the 5.0 m end floor that
    `clearance_gate` enforces AFTER the fact. The floor is now held where the vertex is
    chosen. Only the terminus — the crossing's approaches are anchored to the deck by
    design and the gate never probes the deck span.
  * NOT done, and this is the second run's work — `measure_west_division_streets` and
    `measure_north_division_streets` fail their self-tests: west_water's committed path is
    supposed to BE the derived bank offset to the centimetre, and the five North Division
    streets are supposed to meet North Water Street within 0.05 m. Both moved. **Neither
    tool has a writer** — those paths are hand-committed and asserted against a rule, so
    six street records have to be re-derived by hand and re-argued. Two structures drift
    with them (`steamboat_hotel` -0.09 m off its declared 5.00 m frontage,
    `north_bank_shed_dearborn_e3` -0.284 m off its on_rule figure), and re-seating a
    building against a moved street is a provenance judgement, not arithmetic — two
    attempts at it in this run were 15 and 16 m out because the front face is the
    max-v edge and the measurement is validate's frame, not the raw centreline.

**So the split is not south-then-north; it is terrain-then-north-bank-fabric, and the two
cannot merge separately** — `tools/check.sh` is one gate and the terrain change is what
makes the north-bank records stale. Whoever takes this needs one run that carries BOTH,
or the owner's ruling that the north-bank street fabric may be re-derived in a preparatory
run of its own while the field still ends at N -400.

**Pre-existing red, not caused by this work:** the Chappel shore gate. Clean `origin/dev`
fails `tools/check.sh` on exactly that step and nothing else, which is T-1083's point.
