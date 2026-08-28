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

## 4 · The fort: brick, INFERRED — and the reason it looked unreachable

**This section used to say the fort was deliberately left alone.** It read: *"its buildings
are the second Fort Dearborn of 1816 — seventeen years before Blodgett dug his first clay —
on federal ground … neither answer above reaches it without inventing a third."* That was
written from §1's town evidence and **never checked against the fort's own records**, and
those records refute it. T-0137 is the ticket that made someone look.

**Brick stood inside this stockade in 1816, and this repository attests it twice over.**

| record | `construction` | confidence | what says so |
|---|---|---|---|
| `fort_dearborn_commandants_quarters` | `brick` | **attested** | Hubbard, standing in the fort in 1827: *"the brick building, just within the north stockade previously occupied by the commanding officers"*. The 1855 photograph key, twenty-eight years later and independent: *"the Commandant's Quarters, A (brick, about 25×50 ft.)"*. |
| `fort_dearborn_magazine` | `brick` | **attested** | Hubbard again: *"the magazine, of brick"*. |

Blodgett's yard bounds when the **town** could build in brick. It says nothing about what
the Army had already put up inside the stockade seventeen years earlier, and it was never
evidence about the fort — §1's sentence is *"a brick stack in July 1835 needs no import and
no invention"*, about a townsman's house. A garrison post is exactly where masonry appears
first: it is federal work, provisioned by the Quartermaster rather than by whatever a
settlement of a few hundred could fire for itself, and this one demonstrably had brick for
its powder and for its commanding officer.

**The disposition decides, here as everywhere else on the sheet.** `fort_structure._chimneys`
stands every stack at the midline of the building's depth and rises it from the ground
through the ridge — §2's interior stack, not §3's. An interior stack carries a fire up
through a timber roof and has to be masonry to do it. So the fort takes **`CHIMNEY_BRICK`**,
the row §2 already argues, at **`inferred`**: reasoned from evidence about this ground and
this date rather than stated of any flue. No third row, and no new invention to record —
`docs/LIBERTIES.md` **L26** still owns where every stack stands, and **L168** still owns only
the cat-and-clay fabric it was written for.

**Cat-and-clay is refused, and this is the refusal.** §3's argument is not "log walls, so a
clay stack" — it is a stack standing OUTSIDE the gable, which can be pulled away from the
building when it catches fire and does not eat floor space. Five of the fort's six chimneyed
buildings are log, and not one of their stacks stands outside a gable. Applying §3 on the
strength of the wall material alone would take the colour and drop the sentence that earns
it. If the fort's stacks are ever re-dispositioned to the gable, this ruling goes with them.

**What it covers:** ten stacks on six buildings — the barracks (3), the commandant's
quarters (2), the officers' quarters (2), the blockhouse, the guard house and the sutler's
store. Two of the ten stand on a building whose own walls are attested brick, which is as
direct as this dataset gets. The other four fort buildings, the parade, the root house and
the lighthouse count no stack and are untouched: the material is appended only where a record
counts one, so their masters keep the four-material list they shipped with.

**What would replace this:** a source describing any flue at this post — a Quartermaster
return, a repair estimate, an inspection report — turns `inferred` into `attested` for the
building it names, or refutes it. A source putting the fort's stacks outside the gable moves
them to §3 instead. Neither exists in this repository today.

## 4b · What is still deliberately left alone

- **The 90 inferred placeholders**, which already ship a `placeholder_chimney_brick` at
  `#89503F` — a different brick from the archetypes', 20 % apart in linear red. R-W2a
  finding 4 is right that a town painted by two generators with no shared palette splits
  visibly in half, and converging that value is a byte change to 90 committed masters and
  their banked passthrough set (K38). Ticketed as **T-0138**, not smuggled in here.
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
