# What a Chicago chimney of 1835 was built of

**Opened by T-0008, which is R-W2a finding 1's other half.** The material sheet
(`docs/RESEARCH/materials.md`, wired as `generators/common/materials.py`) measured that
`frame_dwelling`, `frame_storefront` and `log_dwelling` built every chimney stack with the
**roof** material, so a stack came out painted whatever weathering condition its own roof
was dealt. R-W2c refused to fix that by picking a colour: *"it is not a palette fix, and
picking the placeholder's brick would be the wrong half of it"* — because the two stacks
this town has are two different objects, and the archetypes had already said so.

This file is the fabric question, answered at the tier the evidence carries. It does not
touch a stack's POSITION: `docs/LIBERTIES.md` **L26** has owned that since the archetypes
were written, and nothing here disturbs it.

## 1 · What this repository actually holds

**One coloured witness to any Chicago chimney, and it is retrospective.** Image 8 of the
owner's brief of 2026-08-18 (`data/sources/assets/owner_brief_2026_08_18/README.md`) is
the C. E. Petford watercolour of the Sauganash Hotel, and the brief's own reading of it
records **"brick chimneys"** on a two-storey clapboard block. The set's README says a
tier-5 retrospective view *may drive materials as `inferred` and may never drive a
coordinate*, which is exactly the weight taken here. T-0092 had already read that plate
onto the Sauganash's own stacks (`chimney_material: brick`); what was missing was any rule
for the other 142 buildings standing round it.

**Brick was being made in this town, and the date is documented.** `brickyard_north_side`
— Blodgett's brick-yard, Andreas vol. 1 p. 1161 — was established *"in the spring of 1833,
on the North Side, not far from the river bank, between Dearborn and Clark streets"*, and
the same sentence traces the town's first brick building to it. The record's own note adds
the corroboration: the Lake House, begun on the north bank in **1835**, is three storeys
and a basement of brick. So a brick stack in July 1835 needs no import and no invention: it
needs a mason and the yard two blocks away.

**Nothing states the fabric of any other stack, and three attributes could have.** Across
`data/structures/`, `chimneys` is a COUNT on every record that carries it; `chimney_material`
is stated on exactly one building; `construction` says what the walls are and never what
the flue is. There is no source in this repository describing a Chicago chimney catching
fire, being pulled down, or being built — the fire ordinances the town legislated
(`chicago_democrat_1833_11_26`, Ordinance 9 and its neighbours) are about goods in the
street, not about flues.

## 2 · The framed house: brick, INFERRED

A stack on a framed building in this dataset **rises inside the wall and breaks the roof at
the ridge**. That is not a new claim — `frame_dwelling._chimneys` has said it in as many
words since the archetype was written: *"the first stands at a GABLE END, rising inside the
wall and breaking the roof at the ridge. That is the eastern habit these settlers brought
with them, and it is the difference between a framed house and the log cabins next door."*
`frame_storefront` puts its stacks on the ridge line; `frame_tavern` puts them across the
frontage at the depth midline. All three are interior stacks.

An interior stack carries a fire up through a timber roof. It has to be masonry to do that,
and the masonry Chicago had in July 1835 was brick. Together with the one coloured witness
in §1, that is an **inferred** claim: reasoned from evidence about this town — a working
brick-yard, a brick hotel under construction, and a watercolour of one of these very
buildings — rather than stated of any particular house.

**The tone is not a new number.** It is `frame_tavern`'s committed `BRICK_RGBA`
(0.45/0.23/0.17 linear, roughness 0.85), wired to the Sauganash by T-0092 off the Petford
view, moved into the sheet so the town has ONE brick instead of an archetype-local copy per
archetype — the same move T-0007 made for the hewn log, and the complaint materials.md §2.3
files against exactly this shape of duplication. The Sauganash's own masters are byte-for-byte
unchanged by T-0008 as a result, which is the check that the value really did not move.

## 3 · The log cabin: stick-and-clay, RECONSTRUCTED

A stack on a log dwelling in this dataset stands **outside the gable**, and
`log_dwelling._stack` has always argued why: *"a stick-and-clay or fieldstone stack built
against the gable can be pulled away from the building when it catches fire, and it does
not eat floor space."* That sentence was committed years of parcels before this one, and it
is a claim about FABRIC that the renderer then ignored, painting the thing it describes in
the roof's colour.

So the fabric follows the disposition that was already argued: a **cat-and-clay** stack —
split sticks laid up in courses like a miniature crib and daubed inside and out with the
same clay the wall below it is chinked with. Fieldstone is the other half of the archetype's
own sentence and is **not** built: a stone stack is a different silhouette as well as a
different colour, and choosing between the two per building would need evidence this
project does not have. One treatment, declared.

**Nothing attests any Chicago log house's stack, so this is `reconstructed`** — the tier
AGENTS.md exists to license: *invented within bounds, because the scene needs it and nothing
states it.* The bounds are two values this repository already ships:

| bound | value | why it binds |
|---|---|---|
| not as pale as the CHINKING | 0.700 / 0.670 / 0.590 | the same clay, sitting sheltered under an eave, while a stack takes weather and smoke on every face |
| not as dark as the palest ROOF CONDITION | 0.424 / 0.384 / 0.345 (`weathered`) | below that it stops reading as masonry against the roof beside it, which is the whole defect T-0008 fixes |

Nothing states where between the two it sits, so it sits at the **midpoint**, to three
decimals: **0.562 / 0.527 / 0.468**. Roughness is the sheet's `earth` substrate (0.95),
because the surface is daub. `docs/LIBERTIES.md` **L168** records the invention.

## 4 · What is deliberately left alone

- **The fort.** `fort_structure` still builds its stacks with `M_ROOF`. Its buildings are
  the second Fort Dearborn of **1816** — seventeen years before Blodgett dug his first
  clay — on federal ground, with `construction` running log, brick, earth and stone across
  ten records. Neither answer above reaches it without inventing a third, so it is a ticket
  and not a guess: **T-0137**.
- ~~**The 90 inferred placeholders**~~ — **CONVERGED 2026-08-28, T-0138.** They shipped a
  `placeholder_chimney_brick` at `#89503F`, a different brick from the archetypes' and 20 %
  apart in linear red; R-W2a finding 4 is right that a town painted by two generators with no
  shared palette splits visibly in half. `inferred_placeholder.py` now asks
  `materials.chimney_finish("interior")` for its stack, so the placeholders and the archetypes
  read the same row — §2's brick, at `0.45 / 0.23 / 0.17`, roughness 0.85. **The literal lost
  because it had no witness**: nothing in this repository argues for `#89503F`, and §2's value
  is the Petford watercolour's, so this converges on the evidenced side rather than splitting
  the difference. **The byte change did not happen, because there is nothing left to change**:
  `generators/inferred_placeholder.py --check` reports *0 flagged placeholder GLBs; 230
  superseded by a canonical bake*, and no committed GLB carries the material name at all. K38's
  passthrough re-bank was not needed and no building repaints. What the parcel buys is that the
  split cannot walk back in the day a record outruns the bake and a placeholder is emitted again.
- **A log dwelling's placeholder stack is still brick, and that is the massing's fault, not the
  palette's.** `chimney_finish` is asked for `interior` unconditionally because the placeholder
  builds one kind of stack — a box inside the footprint depth, rising through the roof. §3's
  daub belongs to a stack standing OUTSIDE the gable, and painting it onto a stack drawn inside
  the roof would put the right fabric on the wrong silhouette. Left alone deliberately.
- **The covering of any roof**, which R-W2a finding 2 says nobody states and this parcel
  does not pretend to know. A stack that is no longer roof-coloured makes no claim about
  the roof it passes through.

## 5 · What would replace this

A source describing a Chicago chimney — an insurance survey, a builder's account, a
recollection naming brick or clay at a named house — turns §2 from `inferred` into
`attested` for that building and §3 from `reconstructed` into something better. Failing
that, an inventory of Blodgett's output would bound how much of the town could have been
brick at all; the record already says the yard's first working season was 1833 and says
nothing about how many thousand it burned.
