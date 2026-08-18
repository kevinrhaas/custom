---
id: T-0089
title: The 'light' scene-detail ceiling is breached, and it was breached before this run's geometry
state: open
epic: META
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
needs_bake: false
---

The `light` scene-detail level draws more triangles than its own ceiling allows, and it
did so before this run added a metre of plank walk.

**Measured 2026-08-18**, `tools/smoke_renderer.mjs --published`, desktop 1280 x 800, on the
T-0090 branch: `scene detail 'light' stays inside its own ceiling` FAILS at **604 950 tris of
600 000**, 48 draw calls. `full` and `balanced` both pass, and `turning scene detail down
actually draws less` passes — the levels still mean something, the tightest one is just over.
The mobile half does not fail it: at 390 x 780 the frustum is narrower and the count stays under.

**It is not this branch's.** T-0090's whole addition to the scene is the Sauganash's frontage,
and it was measured in the browser at **3 684 triangles** (the frontage layer draws 7 308 in
total: 3 624 the Green Tree's, 3 684 the Sauganash's, separated by a bounding box — the two inns
are 250 m apart). Take the most generous assumption for this branch, that every one of those
3 684 was inside the frustum at the station the ceiling is measured from, and `dev` still stood
at **601 266 of 600 000**. The branch made a breach worse; it did not open it.

**Why nobody had seen it.** The desktop half of the smoke has never finished inside this runner's
ten-minute per-command ceiling (**T-0060**), and this row sits at assertion 151 of it — far enough
in that the runs which do reach it are the ones that get lucky on timing. T-0052 measured the same
budget at **565 206 / 600 000** and **T-0056** is the open ticket for the layer that eats most of
it; the ~36 000 triangles of headroom that ticket bought have since been spent by the layers
shipped on top (the docks, the goods, the boards, the yard, the wagon shed and two frontages).

**Acceptance:** `scene detail 'light' stays inside its own ceiling` is green at 1280 x 800 on the
published mirror, with the saving stated against the 604 950 measured here, and **without thinning
what any layer claims to be** — T-0056's rule holds: a picket drawn as a rail is a
misrepresentation, not a saving. The likely first move is T-0056 itself (the enclosure layer is
detail-blind), and this ticket is where the number lives until it is.

**Update 2026-08-18 (T-0086, the far sward).** The far band adds a worst case of **2 660
triangles** at `light` — 190 cards of a 7-column archetype — measured in the browser at
**+1 962** at the South Water stand at detail `full`. It makes this breach 0.4 % worse and does
not open it; the saving this ticket asks for is unchanged and still sits in T-0056.

**Links:** T-0056 (the layer that pays full cost at every level) · T-0060 (why the row goes unseen)
· `docs/ROADMAP.md` § THE RUN BUDGET · PR for T-0090 (where it was measured).
