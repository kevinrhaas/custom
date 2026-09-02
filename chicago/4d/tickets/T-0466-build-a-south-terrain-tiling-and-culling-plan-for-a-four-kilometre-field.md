---
id: T-0466
title: Build a south-terrain tiling and culling plan for a four-kilometre field
state: open
epic: SOUTH_TIME
requested_by: owner
seen: false
effort: S
legacy_id: null
opened: 2026-09-01
closed: null
pr: null
claimed_by: null
blocked_on: T-0464
needs_bake: false
---

The renderer's 12 x 3 ground tiling was tuned for the present roughly 2,020 x 800 m terrain. A Madison-to-Cermak field is several times deeper north-south and must not simply multiply visible triangles and draw calls without measurement.

Measure the expanded field at the existing smoke camera stands plus new south stands. Replace fixed assumptions with a documented tiling/culling strategy that scales with terrain aspect ratio while preserving the `light` tier as the floor. Raise full/balanced budgets only when the measured parcel requires it, per AGENTS.md.

Acceptance: the expanded field has an explicit tile grid or dynamic rule; downtown and south-scene stands have measured triangle/draw-call results; no terrain seam appears; `light` remains within its ceiling; and the result unblocks the south geometry rather than only documenting a performance risk.