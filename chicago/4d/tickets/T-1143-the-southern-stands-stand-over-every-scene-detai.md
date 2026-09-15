---
id: T-1143
title: The southern stands stand over every scene-detail ceiling, and no ground tiling moves it
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-15
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The southern stands stand over every scene-detail ceiling, and no ground tiling moves it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured while T-0466 was choosing the ground's culling grid, at four poses down the new
southern field — 700 m, 1,800 m and 3,200 m south of the datum, and one aerial over it —
with `tools/measure_ground_tiling.mjs`. The readings are committed in
`data/render/ground_tiling_budget.json`.

**At the `light` tier — the FLOOR, ceiling 825,000 triangles — the worst southern stand
reads 1,387,934.** At `full`, ceiling 1,460,000, it reads 2,147,081. The stand that does
it is `mid_field_looking_north`: 1.8 km south of the town, on open ground, looking back
at it. From there the WHOLE town is in one frustum at once, and no stand this project
owns has ever been outside it looking in — `tools/smoke_renderer.mjs` STANDS are all
inside the town or above it.

**This is not the ground and it is not the tiling.** T-0466 tiled the ground better and
took triangles OFF every one of these readings; the remainder is the buildings, the
flora and the shadow pass, seen whole. Nor is it a number that any tiling can move: a
tile is culled when it is out of frustum, and from out there nothing is.

**What this ticket is not, either:** a re-budget. The instrument that took these figures
is not calibrated against the gate — its four DOWNTOWN readings also sit above what
`tools/measure_detail_ceilings.mjs` reports for the same stands, which is stated in the
reading's own `what_this_is_not`. So the first piece of work is to read the southern
stands on the GATE's instrument and find out what the real figure is. Only then is there
a question about ceilings, distance culling or a southern LOD, and it should be asked
with T-0467 (which puts real anchors down there) rather than before it.

**Acceptance:** the southern field has stand readings taken on the same instrument the
ceilings are held with; whatever they say is written down beside the downtown ones; and
if they are over, the answer is argued — a trim, a distance rule, or an argued
re-budget — rather than the ceiling being moved to fit.
