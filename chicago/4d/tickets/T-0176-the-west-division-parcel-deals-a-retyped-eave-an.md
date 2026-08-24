---
id: T-0176
title: The West Division parcel deals a retyped eave and pitch, not the family's bands
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

The West Division parcel deals a retyped eave and pitch, not the family's bands.

Piece 3 of 5 of **T-0148 — The A1 stable cannot reach its ridge band at any pitch its family allows**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** the West Division approaches parcel's 20 roofs draw their eave and their
pitch from `tools/family_bands.py` rather than from constants retyped into
`tools/generate_west_infill.py`; records re-derive, changed GLBs rebaked in the same commit,
gates green, ratchet updated.

**Why.** Measured 2026-08-24 under T-0148: 11 of the 59 ridge-band offenders are this parcel's,
on the same cause as T-0175 — a retyped eave and a retyped pitch, several of them outside the
very bands the record's own note cites. Six of its records sit outside the ridge-feasible part
of their eave band.
