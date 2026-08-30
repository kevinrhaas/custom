# The platted block and lot grid, generated from the module

**Record:** none — this is a memo about a *derivation*, not about a building ·
**Data:** `data/traces/vectors/thompson_lots.json` ·
**Inputs:** `data/traces/street_control.json`, `data/streets/1835.json`,
`data/sources/thompson_plat_1830.json` ·
**Gate:** `tools/generate_plat_lots.py --check`, in `tools/check.sh` ·
**Roadmap:** K7

---

## 1. Why this is generated and not traced

`data/sources/thompson_plat_1830.json` is a **parameter source**. No open high-resolution
archival scan of the 1830 plat has been located, the surviving artifact is a Canal
Commissioners' working copy dated to at least 1836, and the original burned in 1871. What the
record is good for is the module — the original town at roughly 0.375 sq mi, 80-ft streets,
18-ft alleys — and the source note has said since it was written that street and alley geometry
should be generated from those figures rather than traced from pixels.

The 1834 sheets would be the alternative, and § S9 of the roadmap already measured what tracing
them would cost. Both carry 3.7–4.5 % anisotropic paper stretch; the eleven corridors measured
off them read 75.7–92.8 ft with a median 3.7 ft above the adopted 80. That excess is stretch and
the placement of a pen line, not a wider street. A grid fitted to those readings would arrive in
the dataset with 4 % of paper distortion baked into every block face, and a street that is
straight because a surveyor made it straight would come out bent because we traced a folded
sheet.

So the grid here is arithmetic on two committed things: the street centrelines this project
already stands on, and the module width beside them.

## 2. The construction, in one paragraph

A block edge is a street centreline from `data/streets/1835.json` offset by half the platted
corridor (12.192 m); the four offsets are intersected to give the block. Lots divide the block's
north and south faces in the same proportion and join station to station, so a block with a
curved face (South Water follows the river) subdivides without anything having to be straight.
The alley is a centred 18-ft strip taken out of the middle. A block is emitted only where the
committed centrelines of all four bounding streets actually reach it — at most half a corridor
of extension is allowed, for a line drawn *to* a junction rather than *through* it — and a block
with a corner on water or beyond the modelled ground is refused outright.

**19 blocks, 152 lots, 5 refused.** Four to a block face throughout.

## 3. What each part is entitled to claim

| element | confidence | why |
|---|---|---|
| block boundary | `inferred` | arithmetic on inferred inputs: street lines whose own `geometry_confidence` is `inferred`, offset by a module width `street_control.json` also grades `inferred`. Arithmetic does not upgrade its inputs. |
| alley width (18 ft) | as attested as the street | the module figure, and the 1834 traverses read 17.1–18.7 ft on the same passes that settled the street |
| alley **position** | `conjectural` | nothing in `data/sources/` says which blocks were alleyed, or whether the alley ran with a block's long axis or across it |
| lot lines | `conjectural` | four to a face is a reading of **one** block (§ 4). Applying it to eighteen others is inference from a single instance |
| lot **numbers** | `conjectural`, inside a numbered block only | the scheme is block 18's, read once; the lines it numbers are the module's, drawn from no sheet. A number on a line nobody drew is conjectural whatever the number's provenance (§ 4a) |
| block **numbers** | `inferred`, six blocks only | two numerals on the crop, counted one block per step along their own tier. Everywhere else — the other two tiers, the West Division, where the run begins and ends — is refused in writing (§ 4a). Block ids still name the streets that bound them, which is a description that never goes wrong |

## 4. The single reading behind four lots to a face

`docs/RESEARCH/clark_reach_bulge_1834.md` § 8 records the owner's crop of Wright's sheet at the
Clark reach, read at 3×: block numbers 19 and 18, the lot numbers **4 3 2** along block 18's
north row and **5 6 7** along its south row, and the platted **80** written in each street.
That is four lots across a block face of about 320 ft, in two rows, which is exactly the
arrangement generated here — and it is one block. It is enough to choose the arrangement and not
enough to document it, which is what `conjectural` is for.

(This paragraph said "19, 18 and 17" and gave each row its fourth lot number until 2026-08-29.
The crop carries two blocks and three numerals a row; the rest was retelling. Corrected under
T-0358, and nothing built on it moves — see § 4a.)

### 4a. The block numbers, and the address that needed them

**Landed 2026-08-29, T-0358.** The same two numerals now put a number on six blocks.
`data/traces/thompson_block_numbering.json` is authored, `tools/generate_plat_lots.py` stamps it,
and `plat_block_number` / `plat_lot_number` appear in the generated grid.

19 west of 18 fixes the step at one and the direction as falling eastward, and fixes it *along
the tier* rather than down a column — two blocks side by side differing by one cannot be
column-major. The stream drawn in the street between them is the one § 4 of the bulge memo
traced at local E +462…+469, which is the east half of the La Salle corridor (centreline
E +451.3; Wells 122 m west, Clark 123 m east), so the two are the Wells–La Salle and La Salle–
Clark blocks. Counting the tier: **21 Market–Franklin, 20 Franklin–Wells, 19 Wells–La Salle,
18 La Salle–Clark, 17 Clark–Dearborn, 16 Dearborn–State.**

**Block 16 is the one that mattered**, and it is the one number here an independent source
agrees with. G. Spring's For-Sale notice — the only lot-and-block address in the newspaper
corpus — puts "LOT No. 7, in block No. 16 … on Lake street, one lot east of Haddock's Tavern".
Dearborn–State is bounded south by Lake; the lot scheme read off block 18 runs 5–8 west to east
along a south row, so lot 7 is the third from Dearborn and Haddock's the second; and the Mansion
House, which is Haddock's Tavern, was already argued onto the second lot from Dearborn from
Andreas and from Botsford's advertisements, before any of this existed. The count still stays
`inferred` — three agreeing statements are not a survey — but nothing independent contradicts it.

**Everything outside that tier is refused**, because two numerals in one row say nothing about
how the run passes to the next row, and three schemes that all reproduce 19 beside 18 give the
Lake–Randolph and Randolph–Washington tiers different numbers. Full reading, refusals and the
two consequences it exposes — the Mansion House standing one lot west of where the corpus puts
it, and the anonymous roof sitting on Spring's documented dwelling-house — in
`docs/RESEARCH/thompson_block_numbering.md`.

The same crop is the reason the alley is drawn east–west: two rows of lots facing opposite ways
require something between them.

## 5. What the grid corroborates, and where it disagrees

The block pitches here come from **modern street control** (OpenStreetMap junctions carried
through `street_control.json`), and the pitches in `street_corridors_1834.json` come from
**traverses across two 1834 sheets**. They are independent measurements of the same grid, so
they are worth putting side by side:

| | this grid | the 1834 traverses |
|---|---|---|
| N–S street pitch (E–W spacing) | 118.8, 122.0, 122.0, 123.4, 123.0, 128.0 m | 116.6–123.2 m |
| E–W street pitch, Randolph→Washington | 135.3 m | 134–136 m |
| E–W street pitch, Lake→Randolph | 142.8 m | — (outside the two spacings measured) |

Five of the six N–S pitches and the Randolph–Washington spacing land inside the traverse bands.
The Dearborn–State pitch of 128.0 m does not, and neither does Lake–Randolph at 142.8 m. Both are
recorded rather than averaged away, and neither is explained here: a modern alignment is a
nineteenth- and twentieth-century artefact as much as a survivor of the plat, and the traverses
read two E–W spacings on one sheet, which the roadmap already flags as too thin a base to
generate a grid from. Two independent methods agreeing on five readings and disagreeing on two
is a result to state, not to reconcile with a third number nobody measured.

**Derived lot depths, by row** — these are residuals of the block, not readings:

| row | block depth | lot depth |
|---|---|---|
| South Water → Lake | 93.9–98.5 m (308–323 ft) | 144–153 ft |
| Lake → Randolph | 118.4 m (388 ft) | 185 ft |
| Randolph → Washington | 110.9 m (364 ft) | 173 ft |

The north tier lands within a few feet of 150 ft either side of its alley, which is a figure a
reader may recognise from later Chicago plats. **This dataset does not cite it**, and a
coincidence is not a corroboration: no source in `data/sources/` gives a Thompson lot depth at
all, which is why the depths above are described as what is left over once the block is divided.
Finding a stated lot depth is the research errand that would move these lines off conjecture.

## 6. What the grid refuses to build, and what that tells us

Five candidate blocks are in `omitted` with their reason, and the reasons are the useful part:

- **Three** would have spanned 258 m between Canal and Market — the South Branch. The rule that
  refuses them (`max_pitch_m` 200) exists so a "block" can never be generated across the river.
- **`blk_south_water_market`** is refused because South Water's committed centreline stops 24 m
  short of it, and **`blk_south_water_clinton`** because it stops 878 m short (South Water is a
  South Division street and does not cross into the West Division at all).

That first one is a real gap rather than an artefact: the block between Market and Franklin, on
the river front, is one of the most built-up in the 1835 town, and the reason it cannot be
generated is that the street layer does not yet carry South Water west of E +100. It is the same
control § S9 records as owed, arriving from a different direction.

### 6.1 And the control it is owed cannot be fetched — measured 2026-08-27

T-0183 read the refusal as an errand: one control point at Market × South Water, the committed
set holds four and none of them is anywhere on South Water, go and derive it. The errand was run
and **the rule cannot make the point.** The reading reproduces with

    python3 tools/refetch_control.py --discover market_south_water

which now exits 1 rather than reporting a junction, and is filed with its node ids under
`refused_control` in `data/traces/street_control.json`.

Under `node_rule` a junction is the set of nodes shared by the two named modern surface roadways.
Market's successor is North Upper Wacker Drive and South Water's is West Upper Wacker Drive, and
they share **exactly two nodes — 28358888 and 28358944 — which are `lake_market`'s own committed
pair**, to the id, to the coordinate and to the 17.68 m spread. The way geometry says why: North
Upper Wacker's northernmost way ends at 28358944, West Upper Wacker's first way begins at it and
runs north-east, and its other carriageway comes back down to 28358888. The two arms are one
carriageway pair changing name through a **bend at the Lake Street junction**, not two streets
crossing at South Water.

**The failure mode worth carrying away is that the rule does not fail loudly.** It returns the
right node count, a plausible spread and a clean mean, and nothing in the output says "bend".
Committed, `market_south_water` would have stood at local (89.16, −110.42) — on Lake Street,
**110 m south of the corner it names** — and the block it was fetched to unlock would have been
generated with no depth at all. `--discover` now compares its result against the control already
in the file and refuses a set it recognises, which is the cheap guard against the next one.

The reason is not that the modern city lost the corner; it is that it lost the **street**. Wacker
Drive only reaches South Water's platted line (about local N +5 to +11) at Franklin, 120 m east of
Market, and west of Franklin it turns south-west onto the Lake and Market corner. That is also why
`data/streets/1835.json` already describes South Water's west approach as following *"the dry
south bank resolved by the committed heightfield"* rather than modern control: the modern control
was never there to follow.

So `blk_south_water_market` is no longer waiting on somebody fetching a junction. It is waiting on
a decision — close South Water's west end onto Market's corridor from the 1834 sheets and the
committed bank, on the same basis as the rest of that curve and graded for what it is; or return
its 27 roofs to the South balance the way T-0163 returned `blk_south_water_clinton`'s to the West.
That is the owner's call, because a corner closed without control widens what a block face is
allowed to stand on for every block after it.

**One thing the errand did find.** The same extract and the same rule read *West Upper Wacker
Drive × North Franklin Street* as a clean two-node crossing — 28358941 and 28358883, mean
E 447281.16, N 4637407.21, spread 15.28 m, local (208.46, +11.41). That is the corner the first
post office stood on from 2 Nov 1832 to 3 Mar 1837, and it would be this dataset's **first**
control point anywhere on South Water Street. It is recorded and deliberately not adopted here:
committing it re-derives placements, and it does nothing for this block, whose gap is at the west
end.

### 6.2 And it was closed — the owner's ruling, carried out 2026-08-30

Asked the one question § 6.1 left, the owner ruled: **close South Water Street's committed west end
onto Market's corridor from the 1834 sheets and the committed bank, on the same basis the rest of
that curve already stands on, and grade it for what it is.** T-0183 carried that out.

**The corner is (89.51, −71.02).** Market's platted centreline — the line through the data box at
N −400 and the committed control point `lake_market` — is carried north until the committed
heightfield `e1834_harbor_cut` turns wet, and the northernmost dry sample on it, bisected to 0.01 m
against the same water test `tools/generate_plat_lots.py` uses, is that point. Market's path gains
it as a vertex; the vertex is collinear with the control the line already stood on, so nothing
between Lake Street and the data box moved. South Water's path loses its old terminal vertex
(100, −101) — which ran 30 m down the South Branch's east bank, past Lake Street's own latitude, and
is Market Street's ground rather than this street's — and gains the corner plus one vertex at
(101, −71) that carries the line east along the point of land to the committed (120, −57). Every
0.5 m sample of both new segments is dry.

**The refusal was not softened, and that is the load-bearing half.** This corner still has no
derivable control. `python3 tools/refetch_control.py --discover market_south_water` still exits 1,
`refused_control.market_south_water` is unchanged except for an appended record of what the owner
ruled, and the end is graded `conjectural` in `south_water.west_end` in `data/streets/1835.json`,
where the position is — with the bend, the two nodes and the 110 m named in the record itself, so a
reader can tell this corner from one that has a control point. It is liberty **L214**.

**What the grid does with it.** `blk_south_water_market` builds: 8 lots, 4,957 m², 107.0 m of
frontage, a depth running 8.8 m at the Market end to 36.9 m at Franklin — the wedge the bank leaves
between the river and Lake Street, and the first platted block this grid has emitted west of
Franklin on the river front. Plat block **21**'s number is now stamped on a block rather than on an
omission. The grid goes from 19 blocks to 20 and from 34 cross-street platted faces to 36
(`tools/test_frontage_faces.py`). Its 27 roofs of headroom are schedulable and are deliberately
**not** dealt here: `tools/reconcile_665.py` schedules blocks, and dealing them is its own unit of
work. `tools/measure_block_gating.py` still passes — the block has left the `awaiting_control` list
because it no longer refuses, and `blk_south_water_clinton` stays `never_platted`, still measured
across the water.

## 7. The cross-check: where the town's buildings actually stand

`tools/generate_plat_lots.py --report` puts every placed structure in the 1835 scene against the
grid. As of 2026-08-13:

- **80** stand inside a generated block.
- **120** stand outside the grid altogether — the North Division, the fort, the West Division
  beyond Clinton, and the five refused blocks. The grid covers 19 blocks, not the town.
- **22 stand inside a platted street corridor.**

The 22 need reading with their depth, because a centre 0.5 m inside a corridor edge says nothing
at all against a georeference carrying ±20 m. Sorted by how far in they lie, **seven are 6.5 m
or deeper** — a building in the middle of the road rather than one whose centre rounds across a
kerb line:

| record | street | depth into corridor | position confidence |
|---|---|---|---|
| `inf_packer_dwelling` | Randolph | 12.1 m | conjectural |
| `inf_sawpit_shed` | South Water | 11.5 m | conjectural |
| `inf_cooperage_south` | South Water | 10.5 m | conjectural |
| `inf_cooperage_south_branch` | Randolph | 10.4 m | conjectural |
| `inf_harness_shop` | Randolph | 8.6 m | conjectural |
| `inf_gunsmith_shop` | Randolph | 7.9 m | conjectural |
| `newberry_dole_warehouse` | South Water | 7.0 m | conjectural |

Every one of them is a `conjectural` placement from the inferred-structure programme, and that
is the finding: the placement gate in `tools/generate_inferred_households.py` tests for overlap
with other buildings, for water and for modelled ground, and it has never tested for the street.
Nothing documented is in the road — which is the outcome that makes the seven above worth
fixing rather than explaining away.

**Nothing was moved in this slice, deliberately.** Repositioning a generated structure re-derives
the household programme and its ledger, and that belongs in the parcel that owns those files
(K1 phase three) rather than being smuggled into the slice that discovered it. The gate to add
there is a corridor test using this grid.

There is one historical case that the check must never be taught to "fix": the Sauganash's first
cabin was found, after the 1830 plat was laid out, to be standing *in the middle of a platted
street*, and Beaubien moved it. A building in the road is a thing that happened. What the check
catches is a building put there by us.

## 7a. The gate, the move, and the question the centre test was not asking

**Landed 2026-08-13, K1 phase three (a).** `tools/plat_corridors.py` now carries the corridor
geometry for both sides of this argument — the report above and the placement gate in
`tools/generate_inferred_households.py` — so the check and the generator that has to satisfy it
cannot answer differently. The gate refuses **any** generated footprint that reaches inside a
platted corridor, and the 38 recipe centres in
`data/reconstruction/1835_inferred_household_programme.json` were snapped clear of the roadway:
23 moved, by a median 12.0 m and at most 21.9 m. Centres in a corridor fell **22 → 10**, and not
one of the ten is a generated placement.

**The centre test was the wrong shape of question, and switching to footprints is what showed
it.** A centre is one point; a building is a rectangle up to 11 m across. Twenty-three recipe
buildings had a centre outside the corridor and up to 6.5 m of their own depth inside it, because
the recipe read the frontage bands as centre-lines to sit ON rather than as edges to sit BEHIND.
The row of Lake Street shops is the clearest case: every one of them was centred within a metre
of the corridor edge, so each stood with its front half in the street and its back half on the
lot. Nothing in the centre report could see that, and 22 in-corridor centres understated the
real count by more than half — the footprint pass finds **56** structures with some part inside a
corridor before this slice and **33** after it.

**Three of the moves had to go somewhere other than straight back.** `physicians_office` was
snapped into the First Presbyterian Church, `inf_packer_dwelling` into a reserved phase-2 slot
and `inf_cooperage_south` into the South Branch, so each was placed at the nearest position that
clears the corridor, every committed footprint by 3 m, the two uninstantiated phase-2 recipes,
and the heightfield's dry, covered, walkable ground. That is why the physician's office is 17.7 m
from where it was: the free ground nearest its Lake Street frontage is a lot back from it.

**What the 33 remaining footprints are, and why almost none of them is this slice's to move.**
Four are anonymous roofs from the two infill generators (worst 4.3 m, `recon_1835_south_a5_044`),
and they inherit the same gate when that parcel next runs — it is not added there in this slice
because moving an anonymous roof re-derives the occupancy ledger those generators own. The rest
are hand-placed records whose positions carry a frontage argument from a source, and **thirteen
of them are on South Water Street**, which turns out to be a finding rather than a queue:

> Walking north from South Water's committed centreline to the traced 1834 waterline, the
> distance to water is **10.75 m at E +180** — against a platted half-corridor of 12.19 m. The
> legal 80 ft street there reaches **1.4 m into the river**, and the spare falls under 3 m at
> four more of the eleven stations. On the river reach a building on the north side of South
> Water Street cannot be both outside the platted corridor and on dry land.

So the South Water group is not thirteen misplaced buildings. It is the plat module and the drawn
bank disagreeing on the reach where the town actually did business, and the resolution is a
reading of what the *travelled* way was there (L79 has it at 5.8–10.5 m of an 80 ft corridor
elsewhere) rather than a nudge to thirteen records. `slough_log_bridge` reaching 0.0 m into South
Water is the other reminder in this list that the corridor is not a keep-out zone: a bridge in
the roadway is a bridge doing its job.

## 7b. The last four, and the eight-building row that was aimed at the streets

**Landed 2026-08-13, K7 phase two (b).** The four anonymous roofs § 7a left in the roadway are
out of it, and the two infill generators now ask the same question the household generator does,
through the same `tools/plat_corridors.py`. All three read one module; none of them can put a
generated building in a platted street any more. **No generated placement anywhere in this
dataset stands in a corridor.** Footprints with some part inside one: **33 → 29**, and the 29 are
hand-placed records with a frontage argument, unchanged by this slice on purpose.

**The four were not four numbers. They were one row's spacing.** `data/reconstruction/`
`1835_phase1_south_mixed_blocks.json` carries eight ancillary buildings in two yard rows, and
their local E values were 314, 438, 560, 687, 810 and 315, 559, 809 — a **123 m pitch, which is
the block pitch**. That put exactly one yard building at the eastern edge of every block, a
building's width from the next platted street, five times over and then three times again. The
generator that wrote them tested nothing at all: not overlap, not water, not ground, not the
street.

**Half of them passed, and the reason they passed is the part worth keeping.** Measured from the
corridor edge before this slice:

| record | family | what it is | before | after |
|---|---|---|---|---|
| `recon_1835_south_a5_044` | A5 | small utility building | **−4.32 m** (Dearborn) | +14.68 m |
| `recon_1835_south_a1_046` | A1 | stable | **−3.24 m** (Wells) | +28.11 m |
| `recon_1835_south_a2_047` | A2 | barn or carriage shed | **−2.83 m** (Clark) | +23.17 m |
| `recon_1835_south_a4_042` | A4 | woodshed | **−1.03 m** (La Salle) | +18.97 m |
| `recon_1835_south_a3_041` | A3 | privy | +1.54 m (Wells) | +23.54 m |
| `recon_1835_south_a3_043` | A3 | privy | +1.38 m (Clark) | +19.38 m |
| `recon_1835_south_a4_048` | A4 | woodshed | +1.40 m (State) | +30.40 m |
| `recon_1835_south_a3_045` | A3 | privy | +2.06 m (State) | +19.06 m |

Negative is inside the roadway. The four that failed are the four largest ancillary footprints in
the parcel; the four that passed are three privies and a small shed, and they cleared the corridor
by **1.4–2.1 m against this dataset's own ±20 m georeference**. They were not placed clear of the
street — they were too small to reach it. A gate that had only ever been shown the four failures
would have read as four bad numbers in a good row.

**So all eight moved, by one rule rather than by four corrections.** Each yard building now
stands directly behind the easternmost principal roof of its own block — the same local E as that
roof, 24 m behind it for the lake-front rear yards and 21 m for the block-interior service yards.
That is not a new invention laid over an old one: a rear yard belongs to a lot, a lot belongs to a
house, and the rows are already named `rear_yards` and `deep_yards`. Moving a privy to the back of
a lot is the typology the row was written for, and standing one at the street line was the
accident. The moves are 17–32 m west.

**What did not change, and must not be read as having changed.** These positions were
`conjectural` before and are `conjectural` after. Clearing the roadway is not standing on a
recovered lot, and being behind a particular anonymous roof is not evidence that this yard served
that house — both buildings are count-units, and neither exists in any source. Nothing was
regraded, no confidence moved, and no occupancy changed: the household ledger keys on structure
id, not on position, so the 83 adopted roofs kept their households across the move. The
re-derivation gates in `tools/check.sh` re-run all three generators and the sidecar compile, so
the eight moved records are the recipe's output rather than eight hand edits.

**The North parcel is inside the rule without being bound by it.** `generate_north_infill.py`
carries the same gate, and it refuses nothing today: the grid covers 19 South and West Division
blocks and no North Division block, because the North's street control is what § S9 records as
owed. Wiring it now means that when that control lands, the 60 North roofs are already inside the
rule instead of waiting to be found in the road by a report — which is how these four were found.

## 8. What this is not

- **Not rendered.** The grid is a dataset layer; the walkthrough does not draw it and no visitor
  can see it, which is why this slice adds nothing to `docs/LIBERTIES.md` — a liberty is a
  record of something invented that a visitor is looking at. When the lot lines reach the screen
  (the confidence view would paint them dithered, as conjecture), that entry comes with them.
- **Not the whole plat.** The dossier table in `docs/research/02-flora.md` records the platted
  town as 58 blocks between Kinzie, Madison, State and Desplaines; 19 are generated here, bounded by
  the streets this project has committed. The North Division is absent on purpose — its street
  control is the work § S9 still records as owed, and a block generated between two lines that
  are not yet fixed would look exactly like one that is.
- **Not a cadastre.** No lot is owned and no lot is claimed to be the lot a particular building
  stood on. Forty lots carry a plat number since T-0358 (§ 4a) and every one of them is
  `conjectural`: it is a number put on a line the module drew, not a line a surveyor did.
