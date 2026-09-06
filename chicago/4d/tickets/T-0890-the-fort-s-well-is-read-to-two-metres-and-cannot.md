---
id: T-0890
title: The fort's well is read to two metres and cannot be drawn: this project can build a walled roofed building or a fence, and a well is neither
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The fort's well is read to two metres and cannot be drawn: this project can build a walled roofed building or a fence, and a well is neither.

**Opened by T-0881**, which placed the two Out Buildings off the 1830 Harrison plan and
refused to draw the Well beside them. **L228** carries the refusal and the coordinate.

**The evidence is not the problem.** The plate draws a small open ring and letters it *Well*;
under the transform every Fort Dearborn record uses, its centre is **local E +1152.50,
N +139.53 — UTM 448225.20 E, 4637535.33 N**, 81.5 m south and 0.5 m east of the fort's centre.
Hubbard's *"was in the outer inclosure and near the south gate"* is satisfied twice over: the
ring is inside the enclosure and 50.3 m due north of the knot the same sheet letters *Gate*.
Two witnesses, agreeing, on a position this project can defend to a few metres.

**The tooling is the problem.** `outbuilding`, `log_dwelling`, `frame_*`, `institutional`,
`fort_structure` all build a walled, roofed building. `data/enclosures/` draws fences —
post-and-rail, pickets, boards — from a perimeter. A well curb is neither, and rendering it as
either would be the model saying something the sources do not.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. A way to stand a well head on committed ground that is not a building and not a fence —
   whichever of a new archetype, a new `kind` on the enclosures layer, or a new small-object
   layer costs least and claims least. Whatever it is, it is proposed rather than imposed if
   it touches `docs/GLB-CONTRACT.md`.
2. `fort_dearborn_well` placed at the coordinate above, `inferred` for position on two
   witnesses, and every element of its fabric — curb, cover, sweep, depth, diameter —
   graded `reconstructed` with a liberty that lists them item by item. The 14.5 px ring is a
   map symbol and must not be read as a diameter.
3. **L228 retired or restated**, because its whole content is that this could not be done.
4. Baked with `--only` where a bake is owed, published in the same commit, and
   `bash tools/check.sh` green.

**Links:** T-0881 · T-0758 · T-0592 · **L228** · **L216** · `docs/RESEARCH/wells.md` ·
`docs/RESEARCH/fort_dearborn.md` § 7 · `data/sources/harrison_1830_river_mouth.json`
