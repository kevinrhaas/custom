---
id: T-0179
title: Three families offer a shed roof their own ridge band cannot carry: C1, F1 and F4
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Three families offer a shed roof their own ridge band cannot carry: C1, F1 and F4.

Found by T-0148's sweep, `tools/measure_ridge_reach.py`, which asks of every family and every
roof form its `roof` column names whether the authored `ridge_ft` band is reachable from some
eave in the eave band at some pitch in the pitch band, at every footprint in the footprint band.
Every family passes on the gable reading. Three fail on the shed one, because a shed's roof
climbs the WHOLE span rather than half of it and the ridge band was written for the gable:

* **C1** "front gable or shed", ridge 15-20 ft — 231 of 441 footprints unreachable, first at
  14x25 ft.
* **F1** "gable or shed", ridge 18-24 ft — 399 of 441, first at 18x33.8 ft.
* **F4** "gable or shed", ridge 17-24 ft — 441 of 441. No footprint in F4's own band can be
  roofed as a shed inside its own ridge band.

**Nothing is broken today and that is why this is a ticket and not a gate failure.** No
generator deals a shed to C1, F1 or F4: `_roof_kind` in both sampling parcels reserves the shed
for D2, A3, A4 and A5. So the gate passes a family when ANY form it names is reachable, and
prints these three as NOTE lines. The day a parcel deals one of them a shed — which the
crosswalk plainly permits — it will be built outside its own ridge band and the ridge gate will
bank it.

**Acceptance:** either the three families' shed reading is retired in the crosswalk (an owner
call about the specification, so `block --owner` if that is the answer), or the generators state
in one place that these families are gable-only and why, and `tools/measure_ridge_reach.py`
gates that statement against what the generators actually deal so the two cannot drift.

**Links:** T-0148 (opened this) · L176 · `tools/measure_ridge_reach.py` ·
`data/reconstruction/1835_family_archetype_crosswalk.json`.
