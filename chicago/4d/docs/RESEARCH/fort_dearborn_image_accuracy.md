# Fort Dearborn, against its two plates — the image-accuracy pass (T-0044)

**Run 2026-08-19.** The third and last piece of T-0006, the owner's K2 ask: *render each
landmark from its reference plate's viewpoint, compare, improve.* The Green Tree (T-0042)
and the Sauganash (T-0043) were the first two. The next two UNticketed plates in the
committed reference set are the **two Fort Dearborn views** in
`data/sources/assets/prefire_views_kevin_2026_08/` — `p4_0.png` and `p4_1.png` — and this
is their pass.

Both are **tier 5 pictorial**, retrospective, and bound by that directory's README in full:
they may drive massing, roof form, fenestration, materials, furniture and setting as
`inferred`, and they may never drive a coordinate or a footprint outline.

## The plates

**`p4_0.png` — the fort from across the river, coloured, plate "1."** The stockade on its
rising bank, seen from the north bank at about the height of a person standing. A picket
curtain under a ruled FLAT cap, drawn pale on the reach east of the gate work and brown on
the reach west of it — **this line said "Pale pointed pickets" until 2026-08-24 and was
wrong on both counts; see § "Row 3 was wrong"**; two works rising above the wall with
pyramidal roofs and small lanterns;
a log-faced blockhouse over the gate; ranges inside with dormers, chimneys and even bays;
**a flagstaff over the fort with the national flag flying**; **a track climbing the bank
from the water's edge to the gate**; a boat with rowers on the river; a two-storey frame
house among trees to the right, outside the walls.

**`p4_1.png` — the fort from the lake, the wider view.** The compound as a pale mass on
the low bank with the river running behind it; a small house group on the far bank; a long
fence line running east along the bank; scattered houses on the rise to the left; poplars
and trees around the buildings to the right. **It also depicts Native people, tipis and
canoes: the standing constraint (AGENTS.md § 1835 and Indigenous history, L1) applies —
they are reference for the SETTING only and nothing of them is drawn.**

## The render, before this pass

`docs/RESEARCH/fort_from_the_north_bank_2026-08-19.png` — shot at local `1145, 300`, yaw
180°, which is `p4_0`'s own stand. The fort reads: stockade, ranges, chimneys, the
lighthouse beyond. What is missing against the two plates, in the order a visitor would
notice it:

| # | the gap | can this runner close it |
|---|---|---|
| 1 | **No road anywhere on the reservation.** Both plates show a travelled way at the fort; the render has trackless prairie between the town and the gate. | **yes — this pass ships it** |
| 2 | The track descending the bank from the north gate to the water (`p4_0`). | no while the bank is ungraded — T-0004 owns the bank |
| 3 | ~~Pickets are flat-topped and dark; the plate's are pointed and pale.~~ **This row was wrong in both halves — see below. Refuted and closed 2026-08-24 by T-0094.** | nothing to bake |
| 4 | ~~The corner works do not rise above the curtain with roofs and lanterns as the plate draws them.~~ **`p4_0` draws no work at either angle it shows. Refuted and closed 2026-08-24 by T-0095 — see below.** | nothing to bake |
| 5 | ~~No gate is drawn in either documented wall;~~ **a gate has been drawn in both since the archetype was written — but both stood a QUARTER OPEN, and that is now fixed. Closed 2026-08-24 by T-0095 — see below.** The plate's log-faced work over the gate is not built, and § "Row 4" says why. | **closed — one asset rebaked** |
| 6 | **A flagstaff and flag over the fort** — the most conspicuous single feature of `p4_0`. | **NOT a bake question, and NOT to be built on this plate alone** — see below |
| 7 | The ground round the walls is full prairie sward; both plates show it bare and trodden. | **closed 2026-08-23 by T-0097** — a 12 m band of trodden earth outside the palisade, derived from the stockade's own committed footprint (`data/enclosures/fort_dearborn_apron.json`, L174); before/after at `docs/evidence/t-0097-{before,after}.png` |
| 8 | No trees at the fort; `p4_0` puts a tree mass east of the walls and `p4_1` trees round the buildings on both banks. | no bake |

## Row 3 was wrong, and the correction is the interesting part (T-0094, 2026-08-24)

This pass wrote *"Pale pointed pickets"* of `p4_0` in its own description of the plate, and then
*"Pickets are flat-topped and dark; the plate's are pointed and pale"* in the table. **It read the
plate by eye and it read the model by eye, and it got both wrong.** T-0094 was filed off this row
and closed refuted; `tools/measure_picket_plate.py` now holds the finding and prints it.

**The model was never flat-topped.** `generators/archetypes/palisade.py::_picket` has built every
post as a shaft plus a four-triangle sharpened head since the archetype was written, sized by
`PalisadeParams.picket_point_m`. The committed master says so independently:
`assets/gltf/fort_dearborn_palisade__picket_1816.glb` puts the picket surface's 21,504 positions on
exactly three heights — 6,144 feet at 0.000 m, 12,288 shoulders at 3.388 m, **3,072 apexes at
3.700 m**, four per post over 768 posts. That is **0.312 m of head, 8.4 % of the picket**, and the
sawtooth reads plainly at the wall and still reads from `p4_0`'s own stand across the river.
`docs/evidence/t-0094-plate-vs-model.png` is the three views side by side.

**And the plate draws a ruled flat cap.** Measured on the east reach of the north curtain, over the
195 px between the gate work and the east corner: the cap resolves in 138 columns and is straight
to **0.45 px rms**, peak-to-peak 2.0 px, stable across three detector thresholds. The same plate
**resolves individual pickets** — the curtain's column profile autocorrelates at **+0.70 at a 10 px
lag**, +0.60 on the west reach — and stands the curtain **43 px** tall, so a head of the model's own
proportion would have serrated that line by **3.6 px**, eight times the residual. `p4_1` rules the
same flat cap. The draughtsman had the resolution and drew no point.

That does not make the model's head wrong — a lithographer rules the top of a distant stockade, and
these are tier-5 retrospective plates. It makes the head **unattested and ours**, which is now
recorded in the record's own `construction` note and in **L179**, where it had never been written
down at all.

**"Pale" is a reading of half of one wall.** The plate paints this single continuous curtain across
a **1.85× range of tone** in one view — median sRGB (200, 191, 158), luminance 191, east of the gate
work; (117, 102, 76), luminance 103, west of it — against the fort's own frame range at 183, bare
bank earth at 115 and the paper at 218. The picket surface this project ships, `hewn_log`, is sRGB
(158, 141, 120), **luminance 143: inside the range the plate paints the same wall across.** A source
that draws half a stockade darker than the model and half paler cannot warrant moving it either
way. The whitewash trap the ticket named is separate and stands: Fergus's white-washed board fence
is the enclosure of 1850, after the pickets came down.

**What the render's darkness at this stand actually is.** From `p4_0`'s stand a visitor looks south
at the fort's NORTH face, which on 1 July is the shaded one; the log ranges behind the wall read
(52, 55, 57) and the brick range (59, 44, 46) in the same frame. The wall is not painted black, it
is lit from behind — and the plate, being a picture, lit it anyway.

**What the plate does say about the pickets, and nobody has acted on:** it draws them at a 10 px
pitch on a 43 px wall — about **0.23 of the wall's height per post**, where the model builds 0.30 m
centres on a 3.7 m picket, **0.081**. The plate's rhythm is nearly three times as coarse. Filed as
its own ticket rather than acted on here: it is a `picket_width_m`/`picket_spacing_m` question, both
`reconstructed`, and moving either needs the bake.

## The flagstaff is a documented trap, and this pass refuses it

`p4_0` plainly draws a flagstaff. **`data/exclusions.json` already excludes one**: the
flagstaff in the parade belongs to Captain Whistler's 1808 FIRST fort, in the passage that
ends *"Such was the old Fort previous to 1812"*, and the entry closes *"none of it may be
borrowed for the second fort's records"*. Retrospective plates conflate the two forts —
that is why the courthouse plate in the same directory is filed as a negative reference —
so a tier-5 view is exactly the evidence that cannot settle this one. Raising it on this
plate alone would be the commonest error in the popular literature, committed on purpose.

It is a real question with a real answer somewhere: a garrison return, a quartermaster's
account, Andreas on the 1816 fort, or an identification of this plate against chicagology's
numbering. Filed as a ticket rather than built or forgotten.

## What this pass shipped

**The fort road** — `data/streets/1835.json`, id `fort_road`. Before and after from the
same stand, at local `1000, 30`, yaw 70°:
`fort_road_before_2026-08-19.png` → `fort_road_after_2026-08-19.png`.

`fort_road_published_2026-08-19.png` is the same stand on the PUBLISHED mirror, which is the
run that matters here — the source tree loads uncompressed masters and the site loads the
derivatives, and this project has shipped bugs in that gap twice. Zero page errors either way.

It leaves the east end of South Water Street, crosses the reservation east of the garrison
garden and past the Beaubien buildings, and arrives at the fort's south gate. The reasoning,
and the line between what is documented and what is invented, is in the record's own note and
in **L140**. In one sentence: the gates are attested three times over, the 1830 Harrison plan
puts the garrison garden *west of a road*, and the western reach — the connection to the town
— is this project's reconstruction, because South Water Street stops at the United States
Reservation by the 1833 order and nothing reached draws what carried on.

## What was filed instead of built

Rows 2–8 above became tickets at the bottom of `tickets/QUEUE.md`, where the owner can rank
them. Rows 3–5 are one bake apart; rows 6–8 are not.

## Rows 4 and 5 were wrong too, and the gate was open (T-0095, 2026-08-24)

The full working is in **`docs/RESEARCH/fort_dearborn_gate_and_corner_works.md`**; this is the
part that belongs to this table. Measured by `tools/measure_fort_works_plate.py` and
`tools/measure_fort_gates.py`, both of which run in `tools/check.sh`.

**Row 4 — `p4_0` raises no work at either angle it draws.** The plate raises exactly two
roofed, lanterned, log-faced works and **both stand over the middle of the wall**, at
**0.435 and 0.521** of the drawn run — over the gate, which is where row 5 already put one
of them. A corner work stands at 0.000 or 1.000. The one angle the plate shows unoccluded is
the north-east, and it is drawn **plain**: the picket crest is the skyline from column 319,
rising 0.04 curtain heights over its first twenty columns — which is what the record says of
that angle. The north-west angle, the one the record does put a work at, is behind the tree
outside the walls: the crest is last legible at column 1181 and the material past it is green
by 12.1 against 8.0 over the fort. **The plate has nothing to say about it, and no height was
read out of leaves.**

This row and row 3 are the same mistake made twice on the same sheet, one day apart: the plate
read by eye, and a feature of the record joined to a feature of the drawing that was somewhere
else.

**Row 5 — the gate was drawn, and it was open.** `palisade.py::_gate` has built a gateway in
both documented walls since the archetype was written — jamb posts, a lintel, two leaves —
and it was in the committed GLB when this table was written. What was wrong is something this
table did not claim: **one leaf of each pair was placed from a midpoint that collapsed onto
its own jamb**, so 0.90 m of the 3.6 m gateway stood open with daylight straight through the
wall, and 0.90 m of leaf lay across the pickets outside the frame. Both gates. In the bytes a
visitor downloaded. Fixed and rebaked; before and after from this plate's own stand at
`docs/evidence/t-0095-{before,after}.png`, with the gate itself at 5x in
`t-0095-close-{before,after}.png`.

**And the log-faced work over the gate is still not built.** Not because the plate is unclear
— it is perfectly clear — but because of § "The flagstaff is a documented trap" above,
applied consistently. This sheet already carries one feature `data/exclusions.json` assigns to
the FIRST fort, and two roofed lanterned log towers is that fort's own signature in everything
but position. A tier-5 view that conflates the two forts cannot add a tower to the second one
at an angle **or** over a gate.
