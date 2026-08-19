---
id: T-0095
title: The fort's corner works and its two documented gates, as the plate draws them
state: open
epic: TOWN
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

The fort's corner works and its two documented gates, as the plate draws them.

Found by T-0044's image-accuracy pass. `p4_0` draws the corner works RISING ABOVE the curtain with
their own pyramidal roofs and small lanterns, and a log-faced work over the gate in the middle of the
wall. The model builds the bastions as shallow projections at curtain height and draws no gate at all,
though `gate_sides` (n and s) and `gate_width_m` are already in the record and `bastion_corners` (nw
and se) is attested three ways. **The guard in the record binds here**: the two blockhouses at the
south-east and north-west angles belong to the FIRST fort and may not be borrowed, so this ticket is
about drawing what the second fort's own record already states, at the height and roof the plate
supports as inferred.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

The gates in both documented walls are drawn, the corner works and the south-west blockhouse read
above the curtain, every new form value carries its own confidence and note, and a before/after from
`p4_0`'s stand is committed. Geometry — needs the nightly bake.
