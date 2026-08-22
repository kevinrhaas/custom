---
id: T-0010
title: Finish the heightfield east
state: open
epic: GROUND
requested_by: loop
seen: true
effort: M
legacy_id: T-E3
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

Finish the heightfield east (= S2e's remaining band): ground a visitor can walk onto that
is not there today. Deep history: § T-E3 (~7347). NEEDS THE BAKE.

**Acceptance:** the eastern band walks; shoreline per the 1834 map ruling already recorded.

---
**MEASURED 2026-08-22 by the T-0105 run, which passed over this ticket and owes the reason.
It reads as ALREADY DELIVERED, by S2e parcel (b) on 2026-08-11 — three months of tickets after
the ROADMAP box that became this card was written, and the box (§ T-E3, authored 2026-08-14)
never caught up.** The next run should verify and close it rather than build it again.

* `data/terrain/epochs/e1834_harbor_cut/heightfield.json` carries
  `box_local_enu_m {"e": [-320.0, 1700.0], "n": [-400.0, 400.0]}` — S2e's own requirement was
  "the box must reach about E +1700", and `terrain_spec.json § box_derivation.e_max` argues that
  number off the north pier's 1835 head rather than rounding to it.
* The eastern band is modelled ground, not a flat fill: E +800..+1200 is **90.6 % dry** with
  relief from -5.30 m to +3.75 m, E +1200..+1700 is 36.0 % dry as the shore and the bar take over.
* It carries buildings: the fort complex stands 832 m east of where the field used to stop, and
  STATUS records that twelve of its fourteen structures land on it.
* The shoreline half of the acceptance is in force too — `terrain_spec.json § shore_runs` takes
  `south_shore_harbor_reach` and `north_shore_harbor_reach` from `shoreline.geojson`, which is the
  Wright 1834 trace this ticket names.

