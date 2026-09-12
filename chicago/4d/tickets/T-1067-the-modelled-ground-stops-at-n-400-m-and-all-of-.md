---
id: T-1067
title: The modelled ground stops at n +400 m and all of Kinzie's Addition stands north of it — eleven committed streets and 54 blocks on ground the heightfield does not cover
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-12
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The modelled ground stops at n +400 m and all of Kinzie's Addition stands north of it — eleven committed streets and 54 blocks on ground the heightfield does not cover.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-1062**, which set out to put a viewpoint on the Kinzie Block and could not.

`data/terrain/epochs/e1834_harbor_cut/heightfield.json` boxes the modelled ground at
`n` +400 m. The Kinzie Block's SOUTH face — its nearest edge to the town — is at
+402.72, so the whole block misses the heightfield, by 2.7 m at the near corner and by
about 70 m at the far one. It is not a near miss for the Addition as a whole: T-1060
committed eleven streets whose paths run north to n ≈ +1029, which is 629 m past the
edge, and T-1061's 54 blocks all stand on the same ground.

This is the NORTH counterpart of T-0219, which finishes the heightfield south to Madison
Street. Two things are worth measuring before anything is built:

- What the renderer currently does north of +400. `data/streets/1835.json` already
  carries lines out there and `streets.js` drapes every vertex on
  `terrain.surfaceHeight()`; what that returns outside the box, and what a visitor
  therefore sees standing on Michigan Street looking north (the `kinzie_block`
  viewpoint T-1062 added), is unrecorded.
- What the box would have to become. `terrain_spec.json` § `box_derivation` argues each
  of its four numbers from evidence; `n_max` would need the same treatment, and
  Wright's sheet covers the Addition whole.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
