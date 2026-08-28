---
id: T-0265
title: The commandant's quarters now carries two bricks: the fort's wall brick and the sheet's chimney brick
state: open
epic: RENDERING
requested_by: loop
seen: false
effort: XS
legacy_id: null
parent: null
opened: 2026-08-27
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

T-0137 gave the fort's ten stacks the sheet's `CHIMNEY_BRICK` — 0.450/0.230/0.170 at roughness
0.85. `fort_structure.WALL_RGBA["brick"]` is 0.470/0.260/0.200, and it paints the walls of the
two brick buildings in the complex. So the commandant's quarters now rises a stack of one brick
out of a wall of another: 4 % apart in linear red, 13 % in green, 18 % in blue.

Neither value is wrong and neither is a new invention. They are the same latent split
`docs/RESEARCH/materials.md` finding 4 names and T-0138 is already open on for the placeholder
generator's `placeholder_chimney_brick` — a town painted by more than one palette with no shared
row. T-0137 deliberately did not converge it: moving a value in `generators/common/` stales every
master in the town, and moving `WALL_RGBA` stales this archetype's, so it is a change with a bake
attached and it belongs to whoever pays for it knowingly.

**Acceptance:** Chicago has ONE brick, held on the sheet and read by the fort's walls, the fort's
stacks and the placeholders alike — or the difference between a wall brick and a flue brick is
argued from something, in `docs/RESEARCH/chimneys.md` or `materials.md`, rather than left as an
accident of which module wrote the literal. The masters the change stales are rebaked in the same
commit. Best taken together with T-0138, which is the same defect on the other generator.

**Links:** T-0137 (which found it) · T-0138 (the same split, placeholder side) ·
`docs/RESEARCH/materials.md` finding 4 · `generators/archetypes/fort_structure.py::WALL_RGBA` ·
`generators/common/materials.py` § the chimney stack.
