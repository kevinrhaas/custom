---
id: T-0881
title: The Wash house and the Shop: the two buildings the 1830 plan draws standing on the fort's ground east of the pickets
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0758
opened: 2026-09-06
closed: null
pr: null
claimed_by: run 9/6/2026, 6:33:06 AM CT
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34030277570
---

The Wash house and the Shop: the two buildings the 1830 plan draws standing on the fort's ground east of the pickets.

Piece 1 of 3 of **T-0758 — The Harrison plan names six things on the fort's ground that this model has never drawn: Well, Wash house, Big Barn with Cupola, Shop, Out Buildings and the Fort Cemetery**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Both buildings are placed off `harrison_1830_river_mouth` by the transform section 3
  of `docs/RESEARCH/fort_dearborn.md` already states — 0.335 m/px of the archive.org page
  image, sheet rotated to its own north arrow, hung on the fort centre at local E +1152,
  N +221 — and the pixel reading is WRITTEN DOWN this time, so the next slice does not
  re-derive it from nothing.
- Nothing is graded `documented`: the plate carries "additions and changes suggested by
  the Memory of Early Settlers" on its own face, and the source record says so.
- The plan carries NO SCALE BAR and is used for arrangement and proportion rather than
  absolute size; every dimension taken here says which of the two it is.
- Both are 1830 witnesses standing at a 1835 scene date, and each record argues its
  standing on 1 July 1835 from the garrison's continuity to the evacuation of
  29 December 1836 rather than assuming it.
- Hubbard's independent "rude wash-houses ... on the low sandy beach" is read against the
  plan's single drawn Wash house and the disagreement is stated, not averaged away.
- `./tools/bake.sh --only` per structure and `tools/publish.sh` in the same commit;
  `bash tools/check.sh` green.
