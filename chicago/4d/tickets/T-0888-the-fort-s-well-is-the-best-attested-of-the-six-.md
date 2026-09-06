---
id: T-0888
title: The fort's well is the best-attested of the six things on the plate and this project has no class that can draw one
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0881
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The fort's well is the best-attested of the six things on the plate and this project has no class that can draw one.

Piece 2 of 2 of **T-0881 — The fort's well and the Out Buildings: the class T-0592 refused the town, and a plural label the plate draws once**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**WHY IT IS SEPARATED FROM THE OUT BUILDINGS.** T-0887 places two buildings with an archetype
this project already has. The well has none, and that is the whole ticket: `generators/
archetypes/` holds nine classes and every one of them is a building, a wall or a crib. A well
is a hole with a curb round it, and it needs a class of its own — `pier_crib.py` (112 lines
plus a 306-line params module) is the honest measure of what a small new archetype costs here,
on top of the schema, the material sheet, `mesh_inputs` hashing and `docs/GLB-CONTRACT.md`.
That is a demonstration; it is not the same demonstration as placing two blocks.

**WHAT IS ALREADY SETTLED, so the run that takes this does not re-derive it.**
`docs/RESEARCH/wells.md` § 2 grades the fort's well **position `inferred`, on two witnesses**:
the plate letters `Well` with a drawn ring, and Hubbard puts it *"in the outer inclosure and
near the south gate"* (leaves 75-76, printed pp. 37-38). It is the best-attested of the six
things T-0758 named. **The pixel is measured and it is here**: the ring's ink runs x 1440-1453,
y 880-894 on the rotated leaf, centre **(1446.5, 887.0)** — 1.5 px east and 243.0 px south of
the committed fort centre at (1445, 644), which is **0.50 m east and 81.5 m south** of it, or
UTM 448225.20 E, 4637535.32 N. The ring is about 14.5 px across, which is 4.9 m: that is a map
symbol's size and NOT the well's, and any record must say so.

**Acceptance:**

1. A `well` archetype, or a written refusal of one that says what the model does instead —
   and if it is a refusal it must answer `wells.md` § 4.4, which sent this question here
   precisely because the town-wide refusal did not settle it.
2. If placed: position `inferred` on the two witnesses, the symbol's size never mistaken for
   the well's, the pre-1835 witness problem argued from the garrison's continuity to
   29 December 1836 the way every Fort Dearborn record here argues it, and every invented
   element a liberty.
3. `bash tools/check.sh` green, baked with `--only` and published in the same commit.
