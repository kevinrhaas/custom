---
id: T-0221
title: measure_street_frontage.layer_of reads a record's evidence layer off its filename, and misreads physicians_office
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-27
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

measure_street_frontage.layer_of reads a record's evidence layer off its filename, and misreads physicians_office.

`tools/measure_street_frontage.py`'s `layer_of` decides which of the three evidence layers a
record belongs to — research, inferred household, reconstruction — **by its id prefix**:
`recon_1835_*`, `inf_*`, and everything else is research. It is imported by
`tools/measure_corridor_intrusion.py`, whose census and whose absolute assertion
(*"no GENERATED roof laps a corridor"*) both rest on it.

**Measured 2026-08-27 across all 348 committed structure records** while writing the owner's
business-front clause: the prefix reading and the record's own contents agree on **347** and
disagree on **one**. `physicians_office` carries no prefix and reads as `research`, but it is a
product of the inferred-household programme and says so itself —
`reconstruction.status: "inferred_household"`, occupation physician. Every record either of the
programmes wrote carries the `reconstruction` block that programme writes; a researched record
does not.

**Why it matters more than one row of a table.** `measure_corridor_intrusion.py --gate` ratchets
the RESEARCH layer and asserts **zero** for the generated layers. A generated record that reads
as research is scored against the ratchet instead of against the absolute, so the gate that is
meant to be uncrossable can be crossed by a record whose filename happens not to start with
`inf_`. `physicians_office` does not lap a corridor today, so nothing is wrong in the tree — this
is the gate's reach, not a live fault.

`tools/plat_occupancy.py`'s `researched_ids()` already reads the record rather than the name, and
says why in its docstring. Two readings of one fact is this project's recurring defect; they
should be one.

**Acceptance:** `layer_of` answers from the record rather than from the id, or the two readings
are reconciled in one module both callers import; the `physicians_office` disagreement is gone;
`measure_corridor_intrusion.py`'s census and its zero assertion are re-derived and any movement
in the numbers is stated; and a self-test proves the absolute assertion still fires when a
generated roof is put in a corridor. Never by weakening a gate.

**Links:** T-0199 / T-0220 (where it was found) · `tools/plat_occupancy.py` `researched_ids` ·
ROADMAP K30.
