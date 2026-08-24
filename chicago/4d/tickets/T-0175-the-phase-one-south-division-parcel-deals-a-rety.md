---
id: T-0175
title: The phase-one South Division parcel deals a retyped eave and pitch, not the family's bands
state: open
epic: TOWN
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0148
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The phase-one South Division parcel deals a retyped eave and pitch, not the family's bands.

Piece 2 of 5 of **T-0148 — The A1 stable cannot reach its ridge band at any pitch its family allows**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** the phase-one South Division parcel's 48 roofs draw their eave and their
pitch from `tools/family_bands.py` — the sampler the block and North parcels already use —
instead of the constants retyped into `tools/generate_inferred_infill.py`; the records
re-derive, the changed GLBs are rebaked in the same commit, every gate is green and the
ridge ratchet records whatever the repair heals.

**Why.** Measured 2026-08-24 under T-0148: 28 of the 59 roofs outside their family ridge band
are this parcel's, and they are outside it because nothing chose their eave or their pitch —
every D3 stands at a retyped 2.78 m eave (9.12 ft, outside the family's authored 8-9 ft) and
a retyped 38 deg. T-0144 and T-0145 moved footprint, eave and pitch onto the authored bands
for two of the five reconstruction generators; this is one of the three they never reached.
Same shape as T-0176 and T-0177, different parcel.
