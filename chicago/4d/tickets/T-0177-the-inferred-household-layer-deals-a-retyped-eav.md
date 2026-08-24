---
id: T-0177
title: The inferred-household layer deals a retyped eave and pitch, not the family's bands
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

The inferred-household layer deals a retyped eave and pitch, not the family's bands.

Piece 4 of 5 of **T-0148 — The A1 stable cannot reach its ridge band at any pitch its family allows**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** the inferred-household layer's roofs draw their eave and their pitch from
`tools/family_bands.py` rather than from the constants retyped into
`tools/generate_inferred_households.py` (2.5 / 2.78 / 3.25 / 5.05 m walls, 32 / 33 / 35 / 38
deg pitches); records re-derive, changed GLBs rebaked in the same commit, gates green,
ratchet updated.

**Why.** Measured 2026-08-24 under T-0148: 12 of the 59 ridge-band offenders are this layer's.
It is the generator furthest from the bands — it does not import `family_bands` at all, so
neither its eave nor its pitch is drawn from the family's authored range, and twelve of its
records sit outside the ridge-feasible part of their eave band. Same shape as T-0175/T-0176.

**Care needed:** these records carry occupancy and household links, so re-deriving them touches
more than geometry. Read `tools/generate_inferred_households.py`'s own note first.
