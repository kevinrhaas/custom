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
rising bank, seen from the north bank at about the height of a person standing. Pale
pointed pickets; two works rising above the wall with pyramidal roofs and small lanterns;
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
| 3 | Pickets are flat-topped and dark; the plate's are pointed and pale. | geometry — needs the nightly bake |
| 4 | The corner works do not rise above the curtain with roofs and lanterns as the plate draws them. | geometry — needs the bake |
| 5 | No gate is drawn in either documented wall; the plate shows a log-faced work over the gate. | geometry — needs the bake |
| 6 | **A flagstaff and flag over the fort** — the most conspicuous single feature of `p4_0`. | **NOT a bake question, and NOT to be built on this plate alone** — see below |
| 7 | The ground round the walls is full prairie sward; both plates show it bare and trodden. | **closed 2026-08-23 by T-0097** — a 12 m band of trodden earth outside the palisade, derived from the stockade's own committed footprint (`data/enclosures/fort_dearborn_apron.json`, L174); before/after at `docs/evidence/t-0097-{before,after}.png` |
| 8 | No trees at the fort; `p4_0` puts a tree mass east of the walls and `p4_1` trees round the buildings on both banks. | no bake |

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
