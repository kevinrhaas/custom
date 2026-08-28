---
id: T-0192
title: The cross streets' own frontages get the street edge
state: claimed
epic: TOWN
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-0127
opened: 2026-08-24
closed: null
pr: null
claimed_by: run 8/27/2026, 6:18:39 PM CT
blocked_on: null
needs_bake: false
---

The cross streets' own frontages get the street edge.

Piece 3 of 5 of **T-0127 — The rest of the town gets the street edge**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** the seven cross streets' platted block faces carry the street edge by the
same rule Lake, South Water and Randolph already do — laid from the plat grid, not
hand-placed — and a walker turning off Lake onto a cross street stays on the boards.
`full`, `balanced` and `light` each inside their ceiling at all five stands, at BOTH
viewports, measured on the published mirror. Gates green.

**THE CODE HALF IS DONE AND IT WAS THE HALF THE RECORD SAID WAS MISSING.** Until this
branch `_edge_faces` enumerated a block's NORTH and SOUTH faces only, so naming a cross
street anywhere would have laid nothing at all — `data/frontage/town_street_edge.json`'s
own boundary refusal said so in as many words. All four faces are enumerated now, on an
axis-aware ordering (`EDGE_FACES`, `EDGE_SIDES`), and every cross street generates: the
seven together are 34 platted faces and +3,562.9 m of walk, re-derived rather than
estimated.

**THE GEOMETRY HALF IS REFUSED ON THE FRAME BUDGET, AND HERE IS THE NUMBER.** `balanced`
stood **8,656 triangles** inside its 1,210,000 ceiling on `dev` at 2ab3065a — worst of
T-0135's five stands, the forks from Wolf Point, desktop 1280x800, read twice and
identical to the triangle. Re-derived per street, one at a time:

| cross street | faces | +walk m | +crossing m |
|---|---:|---:|---:|
| Market | 2 | 208.8 | 24.4 |
| State | 3 | 309.2 | 53.9 |
| Franklin | 5 | 551.5 | 117.3 |
| Dearborn | 6 | 577.2 | 117.3 |
| La Salle | 6 | 632.2 | 163.7 |
| Wells | 6 | 638.1 | 117.3 |
| Clark | 6 | 646.0 | 139.3 |

Market is the smallest of the seven and it was BUILT AND MEASURED rather than
estimated. Published, desktop, five stands:

| tier | ceiling | dev | with Market | delta |
|---|---:|---:|---:|---:|
| `full` | 1,400,000 | 1,369,931 | 1,338,875 | **−31,056** |
| `balanced` | 1,210,000 | 1,201,344 | **1,226,196 — OVER by 16,196** | **+24,852** |
| `light` | 785,000 | 746,060 | 759,942 | +13,882 |

So the smallest cross street in the town does not fit, and every other one is two to
three times its size. This ticket is not closed by shrinking further: half of Market is
not a rule, it is a hand-placed exception, and the acceptance above is what it is.

**AND THE DELTA IS NOT THE WALK.** 208.8 m of walk plus one crossing is about 10,400
triangles at this layer's own measured 42.8 a metre. `full` moved 31,056 the WRONG WAY
and `balanced` moved 24,852 — neither is the geometry added. `full` and `balanced` carry
identical settings apart from the ceiling number itself, so what separates them is the
flora census reading `BUDGET.triangles`, and a 10,400-triangle change is swinging it by
±40,000. That is filed as its own ticket and it is what has to be understood before this
one can be re-measured honestly.

**Links:** T-0127 (parent) · T-0191/T-0240 (Randolph) · T-0241 (Washington, refused on
the same rung by 58,926) · T-0193 (the West Division) · T-0223 · T-0146 · T-0209 ·
docs/LIBERTIES.md L160.
