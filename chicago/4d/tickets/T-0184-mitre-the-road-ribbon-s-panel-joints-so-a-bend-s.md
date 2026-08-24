---
id: T-0184
title: Mitre the road ribbon's panel joints, so a bend stops opening a wedge of prairie
state: open
epic: TOWN
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Mitre the road ribbon's panel joints, so a bend stops opening a wedge of prairie.

`renderers/web/js/streets.js` `addRecord()` builds every panel square to ITS OWN chord: the
row at a shared centreline point is drawn twice, once perpendicular to the incoming chord and
once perpendicular to the outgoing one. Where a street bends, those two rows cross at the
centreline and diverge towards the edges, so the outside of every turn carries a triangular
wedge of unpainted ground — apex on the centreline, `half_width * tan(turn/2)` wide at the
ribbon's edge — and the inside carries a matching overlap.

**Measured on the shipped build (T-0111, 2 cm plan probe of drawn triangles inside the nominal
ribbon).** Dearborn's new 5.7-degree joint at the South Water corner: a 0.61 m2 sector, of which
South Water's own roadway covers half, leaving 0.30 m2 uncovered — small enough to ship, and
recorded in docs/LIBERTIES.md L178 as an admitted artefact. **South Water Street's own west
approach is the real prize:** its authored line turns 17.9 degrees at [140, -35] on a 10.5 m
track, which is a sector of about 4.3 m2 at a single joint, and it has been there since the
street layer shipped. Lake, North Water and the fort road each have bends of their own.

The fix is a mitre: compute one normal per centreline POINT — the bisector of the incoming and
outgoing chord normals, scaled by `1 / cos(turn / 2)` and capped so a sharp turn cannot spike —
and let both panels share it. Adjacent panels then emit identical corner positions and neither a
gap nor an overlap is possible. `dryReach`, the `MIN_PANEL_W_M` drop and `refinedPanel`'s drape
refinement all take the normal as an argument already.

**Why it was not done inside T-0111:** it moves ribbon geometry on every bent street in the town,
and T-0111's parcel was 2.7 m of Dearborn. It needs its own before/after measurement, its own
smoke leg and a check that no road-contrast band moves against its baseline.

**Acceptance:** the 2 cm plan probe finds ZERO uncovered ground inside the nominal ribbon at every
authored bend in `data/streets/1835.json` (Dearborn's corner and South Water's west approach named
explicitly, before and after); no street's ribbon leaves its own `track_width_m` half-width, so
`tools/measure_drawn_placement.mjs --gate` still reads 0 strays and its `--refute` control still
fails a mirrored build; the smoke's panel accounting, drape and approach-coverage checks stay green
at both viewports; and a screenshot from the South Water west approach shows the join closed.

**Links:** T-0111 (which measured this and admitted it) - docs/LIBERTIES.md L178 -
`renderers/web/js/streets.js` (`addRecord`, `refinedPanel`) - T-0110 (the drape refinement that
shares this code path).
