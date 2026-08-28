---
id: T-0185
title: The plate draws the fort's pickets three times coarser than the model builds them
state: claimed
epic: TOWN
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: run 8/27/2026, 11:33:13 PM CT
blocked_on: null
needs_bake: true
---

The plate draws the fort's pickets three times coarser than the model builds them.

Found by T-0094, which measured `data/sources/assets/prefire_views_kevin_2026_08/p4_0.png` to
refute a different claim about the same wall and turned this up on the way. It is the one thing
about the pickets the plate DOES say, and nothing has acted on it.

Measured (`tools/measure_picket_plate.py`, no `--gate`): the curtain's column profile
autocorrelates at **+0.70 at a 10 px lag** on the east reach and **+0.60 at the same lag** on the
west, so the draughtsman drew separate posts at a 10 px rhythm; the curtain stands **43 px** tall
there. That is about **0.23 of the wall's height per post**. The model builds `picket_spacing_m`
0.30 on a `picket_height_m` of 3.7 — **0.081**, nearly three times finer.

**Neither number is evidence about 1816.** Both `picket_width_m` (0.24) and `picket_spacing_m`
(0.30) are `reconstructed` and their notes say so; the plate is tier 5 and admissible for materials
and form as `inferred` at best, and 0.23 of a 3.7 m wall is a 0.85 m post, which is not a picket
anybody split. So the question is NOT "adopt the plate's proportion". It is whether a rhythm this
fine is the right reconstruction when the only picture anyone has drawn a stockade three times
coarser, and whether the wall reads as posts or as a slab at the distances a visitor actually
stands.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Either `picket_width_m` and `picket_spacing_m` move together, at the tier the reasoning earns, with
what bounds the new figures written in their notes and the liberty updated — or they are kept, with
the plate's disagreement recorded against them so the next run does not re-open it. Whichever way,
a before/after from `p4_0`'s own stand and from the north wall, and the picket count and triangle
cost stated. Geometry — needs the nightly bake.
