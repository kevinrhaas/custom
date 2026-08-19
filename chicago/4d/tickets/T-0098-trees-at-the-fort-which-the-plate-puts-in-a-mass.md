---
id: T-0098
title: Trees at the fort, which the plate puts in a mass east of the walls
state: open
epic: TOWN
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Trees at the fort, which the plate puts in a mass east of the walls.

Found by T-0044's image-accuracy pass. `p4_0` draws a substantial tree mass immediately east of the
stockade, around the two-storey frame house outside the walls; `p4_1` shows trees round the buildings
on both banks. The render has none at the fort. The placed-planting record kind that T-0091 built for
the Sauganash's yard (`data/flora/plantings/`) is exactly the mechanism, and it needs no bake.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

A planting record stands trees where the plate puts them, each stem inside its species' recorded
height band with the renderer refusing any that is not, the liberty is recorded, and a before/after
from `p4_0`'s stand is committed.
