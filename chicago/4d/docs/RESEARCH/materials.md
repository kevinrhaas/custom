# The material sheet — what the town's surfaces are made of

**Parcel R-W2a** (ROADMAP · RENDERING §4 W2) · written 2026-08-16 · **a document, not a change**

This is the input `R-W2b` wires in and the bake half draws its atlases from. It commits no
code, no parameter and no record. Its job is to answer four questions for every surface in
the town, in one place, so that a builder and a critic read the same sheet:

1. **which surfaces exist** — not which ones we imagine, the ones actually in the shipped GLBs;
2. **what each one is**, with the evidence this repository holds and the confidence that
   evidence supports;
3. **its roughness**, and — the part §4 W2 asks for explicitly and R-G1 scored worst — *why*;
4. **its tiling rate**, derived from a dimension the generators already commit rather than
   chosen to look right.

Everything in §1 is **measured out of `assets/gltf/**/*.glb`**, not read off the source. The
source and the shipped bytes have disagreed in this project before (B-BUG2), and a sheet that
inventories intentions is worth nothing to a bake.

---

## 0. Headline

`assets/gltf/` holds **334 assets carrying 1,353 material slots**, and they resolve to **32
distinct material names, 41 distinct base colours and 18 distinct roughness values**. Nothing
in the town carries a texture of any kind (§1 item 9). Two independent generators paint it:
the nine Blender **archetypes** (244 assets) and the pure-Python **inferred placeholder**
(90 assets), and their palettes were written separately and have never been reconciled.

**The five findings are worth more than the sheet.** They are in §4, and two of them —
**the chimney is not a material in this project**, and **no record anywhere states a roof
covering** — are the reason the town's roofs and stacks cannot be textured today even with a
finished atlas. They are recorded as findings and **not patched here**: this parcel ships a
document.

---

## 1. The surface census, measured from the shipped GLBs

Counts are material slots, across all 334 assets. Base colours are the `baseColorFactor`
actually in the file. Every material in the town is `metallicFactor: 0`, unlit by any map,
double-sided and opaque (R-W5a proved this exhaustively when it merged 47 batches into 16).

| material | slots | shipped base colour (as written) | roughness | emitted by |
|---|---|---|---|---|
| `roof` | 234 | `0.34, 0.30, 0.27` | **0.90** (156) / **0.93** (76) / 0.88 (2) | every archetype |
| `wall` | 114 | `0.52, 0.44, 0.34` unpainted (94) · `0.88, 0.87, 0.83` whitewash (11) · `0.55, 0.16, 0.13` red (8) · `0.90, 0.89, 0.85` white (1) | 0.75 (79) / 0.85 (35) | `frame_dwelling`, `frame_storefront`, `frame_tavern` |
| `dark` | 114 | `0.07, 0.08, 0.09` | 0.35 (69) / 0.40 (45) | frame + log + fort + palisade |
| `trim` | 104 | derived from the wall paint | 0.85 (69) / 0.80 (35) | `frame_dwelling`, `frame_storefront` |
| `placeholder_opening_dark` | 90 | `0.176, 0.239, 0.200` | 0.70 | `inferred_placeholder` |
| `placeholder_chimney_brick` | 90 | `0.537, 0.314, 0.247` | 0.88 | `inferred_placeholder` |
| `board` | 76 | `0.335, 0.310, 0.268` (69) + painted variants | 0.94 | `outbuilding` |
| `interior` | 76 | `0.072, 0.068, 0.060` | 0.60 | `outbuilding` |
| `timber` | 76 | `0.208, 0.172, 0.128` | 0.90 | `outbuilding` |
| `log` | 53 | `0.340, 0.266, 0.188` (52) · `0.42, 0.33, 0.24` (**1**) | 0.92 (44) / 0.93 (8) / 0.90 (1) | log + fort + palisade + bridge + crib + tavern |
| `chinking` | 50 | `0.700, 0.670, 0.590` | 0.95 | log + fort + outbuilding |
| `glass` | 45 | `0.09, 0.11, 0.13` | 0.25 | `frame_storefront`, `frame_tavern` |
| `placeholder_wall_*` | 90 | six finishes, §1.1 | **0.86**, all six | `inferred_placeholder` |
| `placeholder_roof_*` | 90 | four conditions, §1.1 | **0.90**, all four | `inferred_placeholder` |
| `frame` | 31 | `0.52, 0.44, 0.34` | 0.75 | `log_dwelling` (frame addition) |
| `fill` | 6 | `0.300, 0.295, 0.270` | 0.98 | `bridge_timber`, `pier_crib` |
| `deck` | 4 | `0.47, 0.41, 0.32` | 0.95 | `bridge_timber` |
| `brick` | 3 | `0.47, 0.26, 0.20` | 0.92 | `fort_structure` |
| `earth` | 2 | `0.34, 0.30, 0.22` | 0.92 | `fort_structure` |
| `stone` | 1 | `0.58, 0.56, 0.51` | 0.92 | `fort_structure` |
| `shutter` | 1 | `0.14, 0.32, 0.62` | 0.75 | `frame_dwelling`, `frame_tavern` |
| `sign` | 1 | `0.60, 0.54, 0.44` | 0.85 | `log_dwelling`, `frame_storefront` |
| `terrain_ground` | 1 | `0.36, 0.35, 0.22` | 1.00 | terrain GLB |
| `terrain_water` | 1 | `0.18, 0.24, 0.24` | 0.15 | terrain GLB |

Three readings that fall straight out of the table and are not obvious from the source:

- **`shutter` ships once.** Exactly one record in the dataset states shutters — the
  Sauganash's documented bright blue (`Wau-Bun`) — and the archetypes build shutters only
  where a record attests them. The `green` and `black` entries in `SHUTTER_RGBA` have never
  been used, and the unreferenced slot is dropped at export rather than shipped. The palette
  is not carrying dead weight into the scene.
- **`timber` has two definitions in the source and one in the town.** `outbuilding.py` and
  `frame_storefront.py` each define a `TIMBER_RGBA`, and they are **3.2× apart in linear
  red** — `0.208, 0.172, 0.128` against `0.66, 0.56, 0.40`. Only the outbuilding's ships:
  no storefront in the dataset turns `framing_exposed` on, so the storefront's paler value
  has never been rendered. Two different materials are sharing one name (§4, finding 3).
- **One log wall in Chicago is a different timber from the other 52.** `frame_tavern` alone
  imports `LOG_RGBA` (`0.42, 0.33, 0.24`, roughness 0.90); every other log surface uses
  `logwork.HEWN_RGBA` (`0.340, 0.266, 0.188`, roughness 0.92–0.93). `logwork.py`'s own
  comment says the darker value was chosen deliberately *against* `LOG_RGBA`. The one asset
  affected is the Sauganash's log wing (§4, finding 2).

### 1.1 The placeholder palette — 90 buildings, its own vocabulary

`generators/inferred_placeholder.py` paints the anonymous inferred-infill town. It is **27 %
of the assets** and it shares no colour and no roughness with the archetypes.

| finish (`finish_key`) | hex in source | shipped `baseColorFactor` |
|---|---|---|
| `fresh_timber` (37) | `#C3A478` | `0.765, 0.643, 0.471` |
| `weathered_timber` (19) | `#817D72` | `0.506, 0.490, 0.447` |
| `whitewash` (16) | `#D8D1BC` | `0.847, 0.820, 0.737` |
| `ochre` (7) | `#A98B52` | `0.663, 0.545, 0.322` |
| `mixed_patch` (6) | `#BFAE8E` | `0.749, 0.682, 0.557` |
| `red_oxide` (5) | `#7A4437` | `0.478, 0.267, 0.216` |

| condition (`roof_condition`) | hex | shipped |
|---|---|---|
| `darkened` (26) | `#4B4037` | `0.294, 0.251, 0.216` |
| `patched` (24) | `#3C3732` | `0.235, 0.216, 0.196` |
| `weathered` (22) | `#6C6258` | `0.424, 0.384, 0.345` |
| `fresh` (18) | `#5E4938` | `0.369, 0.286, 0.220` |

**These are the only per-building finish and roof-condition vocabularies the project has**,
they are driven by real record attributes (`finish_key`, `roof_condition` — the latter stated
on 218 records), and **no archetype reads either of them.** A weathered roof and a fresh one
are the same colour on all 244 archetype buildings and different colours on all 90
placeholders. Whichever way W2 goes, this vocabulary is the one to converge on, because it is
the one the *data* already speaks (§4, finding 4).

### 1.2 What is deliberately not in this sheet

The ground, the roads and the water are the only textured surfaces in the scene and they are
**runtime canvases**, not assets: `terrain.js` builds the prairie tile and one more, `streets.js`
builds the street wear, and the water normal drifts. They belong to the terrain program and to
W5, they carry no license question, and W2's atlas must not absorb them — three parcels have
already been burned by treating the ground as a building surface.

---

## 2. The sheet

One row per surface the atlas has to carry. **`selected by`** is the parameter R-W2b makes
name it. **Confidence follows `docs/PROVENANCE.md`'s function, not its spelling**: *attested*
= a source record says so; *inferred* = reasoned from specific committed evidence, with the
reasoning stated; *conjectural* = invented to fill a need, and owed a `docs/LIBERTIES.md` line.

### 2.1 Wall surfaces

| surface | what it is | evidence | confidence | roughness | tile | selected by |
|---|---|---|---|---|---|---|
| **`clapboard`** | riven or sawn horizontal siding, 0.14 m exposed face, butt joints landing on stud lines and staggered course to course | the commonest wall in the town: the Sauganash is "a two-story clapboard block" in the Braunhold engraving and the Kurz & Allison panel (`kurz_allison_1893`); `andreas_1884_v1` has the agency house "clapboarded part way up"; the Green Tree plate in the owner's 2026-08-11 reference set is "two full storeys of pale clapboard" | **attested** for the form, **inferred** for the 0.14 m (a period exposure, already committed as `CLAPBOARD_COURSE_M` in three archetypes) | **0.86 ± variation** — riven oak weathering silver; the variation matters more than the constant (§3) | **4.48 m square, 1024² → 228.6 px/m**; 32 courses of 0.14 m exactly | `cladding: clapboard` (`frame_storefront`; today read by that archetype only) |
| **`board_and_batten`** | vertical boards with a batten over each joint, 0.356 m set-out | `BATTEN_SPACING_M`, already committed as "14 in, the usual set-out" — a typological value, not a reading of any Chicago building | **conjectural** — no source in this repository puts board-and-batten on any named Chicago building in 1835 | 0.88 ± variation | **4.272 m square, 1024² → 239.7 px/m**; 12 battens of 0.356 m | `cladding: board_and_batten` |
| **`vertical_board`** | plain vertical sawn boards, no batten | one record: `recon_1835_south_f2_039`, and its own note says **"INVENTED, NOT DERIVED"**, bounded by `owner_chicago_1835_reconstruction_spec_2026` | **conjectural**, and the record says so | 0.90 ± variation | **4.58 m square, 1024² → 223.6 px/m**; 20 boards of 0.229 m (`SHEATHING_BOARD_M`) | `cladding: vertical_board` |
| **`hewn_log`** | squared log courses, 0.34 m on the course, chinking 0.055 m proud between them | the log town is the best-attested fabric here: `cobweb_castle`, `blacksmith_shop_state_st`, `fort_dearborn_*`, and `docs/research/03-structures-north.md`'s survey | **attested** for the fabric; **inferred** for `COURSE_M = 0.34` (`logwork.py` argues it from a squared log, and states the reasoning) | 0.92 ± variation — weathered oak, coarse | **4.08 m square, 1024² → 251.0 px/m**; 12 courses of 0.34 m exactly | `construction: log` / `hewn_log` |
| **`chinking`** | clay-and-lime between the log courses; **stands proud** and is separate geometry | `logwork.py`'s note; the fabric is universal in the sources | **inferred** — the material is ordinary and unremarked, which is why nothing says it | 0.95, near-uniform — dried lime scatters and does not vary the way timber does | **2.04 m square, 512² → 251.0 px/m** — matches the log's texel density exactly, which is what keeps a wall from reading as two resolutions | emitted with `hewn_log`; not separately selectable |
| **`sawn_board`** | plain sawn stock, random widths 0.18–0.40 m, gappy | `outbuilding.py`'s `BOARD_W_M`; the archetype's docstring argues the gaps | **inferred** | 0.94 ± variation | **4.00 m square, 1024² → 256.0 px/m** — widths are geometry, so the sheet carries grain only | `outbuilding`, board kinds |
| **`whitewash`** | lime wash over any of the above; **it does not replace the substrate, it coats it** | the Green Tree dossier settles the hard case: Gale's "walls, ceilings, and board partitions had evidently received a coat of whitewash" is **interior**, and the record carries `paint: unpainted` and says why | **attested** where a record attests it (9 `wall` slots + 16 placeholders); never a default | 0.90 — chalky, flat, and **the least glossy surface in the town** | **overlay, not a tile** — a whitewash sheet is a value/roughness modifier over the substrate's own rhythm, so the clapboard courses stay visible through it, which is what a limewashed wall actually looks like | `paint: whitewash` |
| **`white_paint`** | lead paint, a remarkable expense here | the Sauganash: "a pretentious white two-story building" (`Wau-Bun`), and the dossier's own reading — *a painted white frame building was remarkable precisely because its neighbours were not* | **attested**, for exactly one building | 0.60 — the only smooth wall in Chicago, and that is the point | overlay, as whitewash | `paint: white` |
| **`red_paint` / `red_oxide`** | iron-oxide paint | 6 archetype slots + 5 placeholders; no named Chicago building in this repository is attested red | **conjectural** at the building level, **inferred** as a period finish | 0.85 ± variation | overlay | `paint: red` / `finish_key: red_oxide` |
| **`brick`** | fired brick, laid in courses | `fort_dearborn_commandants_quarters` (`construction: brick`, inferred bare) and `lake_house_construction` | **attested** that these two are brick; **no source in this repository gives a brick or a course dimension** | 0.90 | **rate unresolvable — see §3.2.** The tile cannot be set until a source gives a brick size | `construction: brick`, and every chimney (§4, finding 1) |
| **`stone`** | rubble or dressed masonry | `chicago_lighthouse_1832`; its own note says bare masonry is **unattested** and whitewash is the commoner Great Lakes finish | **conjectural**, and the record says so | 0.93 | rate unresolvable, as brick | `construction: stone` |
| **`earth`** | trodden ground and turf | `fort_dearborn_parade`, `fort_dearborn_root_house`; both notes say plainly *"No source describes it"* | **inferred**, minimally | 0.95 | 4.00 m noise tile — no rhythm to be integral with | `construction: earth` |

### 2.2 Roof surfaces

**This is the sheet's weakest section and the weakness is in the data, not here.** See §4,
finding 1: no record in the dataset states a roof covering, so nothing below can be *selected*
until an attribute exists to select it.

| surface | what it is | evidence | confidence | roughness | tile |
|---|---|---|---|---|---|
| **`shingle`** | riven shingles over board sheeting | **the one direct attestation in the repository**: the North Side school of 1833 is "a frame building twenty-six by thirty-eight feet; twelve-foot posts; **sheeted and shingled roof**" (`docs/RESEARCH/north_side_school_1833.md`) | **attested** for that one building; **inferred** as the ordinary covering of a framed building here | 0.90 ± strong variation — a shingle field is the most legible weathering surface on a building | **exposure is unattested.** At 1024²: tile = 32 × exposure, which holds 228.6 px/m at a 0.14 m exposure. Pick the exposure from a source or record a liberty — do not pick it to make the arithmetic land |
| **`roof_board`** | plain boards weighted or nailed, no shingle field | `outbuilding.py` argues it explicitly: *"a shingle field on an outbuilding would be claiming a finish"* | **inferred**, and well argued | 0.94 | as `sawn_board`, 4.00 m |
| **`bark` / `puncheon`** | — | **not modelled and not evidenced.** Named here only so the next reader knows it was looked for and not found | — | — | — |

Today all three are one material at one colour: `roof`, `0.34, 0.30, 0.27`. The board roof is
separated from the shingle roof by **0.03 of roughness and nothing else** — same colour, same
name, in the shipped bytes.

### 2.3 Everything else

| surface | roughness | notes |
|---|---|---|
| `glass` | 0.25 | the only sub-0.5 surface on a building. Muntins, sash and reveal are geometry and belong to **R-W3c**, not to this atlas |
| `dark` (openings, interiors seen through) | 0.35 / 0.40 / 0.60 / 0.70 | **four different values for one idea across four generators.** Not a texture; a convergence job for R-W2b |
| `trim`, `sign` | 0.80–0.85 | trim is derived from the wall paint and needs no sheet of its own; `sign` is one board and L25 governs what may be on it |
| `deck`, `fill` | 0.95 / 0.98 | bridge and crib; `fill` is river stone and gravel and is the roughest surface in the town |
| `terrain_ground`, `terrain_water` | 1.00 / 0.15 | out of scope, §1.2 |

---

## 3. Roughness, texel density, and where the pixels come from

### 3.1 The roughness reading, corrected

**R-G1's scored note — "there is no roughness variation anywhere" — is right about the thing
that matters and wrong as literally written, and the difference decides what W2 builds.**

Between surfaces there is already a great deal of variation: **18 distinct roughness values**
ship, spanning 0.15 to 1.00, and they are argued in the source rather than guessed. What does
not exist anywhere in the town is variation **within** a surface — every square metre of every
wall has exactly one roughness. That is what makes nothing read as painted, weathered or wet,
because weathering is by definition uneven.

**So the deliverable is a roughness *map*, not a better roughness constant**, and R-W2b should
not spend a round re-tuning the 18 numbers. The `± variation` in §2 is the map's job: the
constant is the mean, and the sheet's per-surface amplitude is what the atlas paints.

Every roughness number in §2 is **reasoned, not sourced**. No source this project holds
measures the gloss of anything, and none ever will. They are `conjectural` in the strict sense
and the sheet says so here once rather than repeating it in every row — but the *substrate*
each one belongs to is often attested, and that is the part provenance is protecting.

### 3.2 Texel density

§4 W2 sets **128–256 px/m**, inspection distance arm's length. Every tile in §2 is sized so
that it (a) lands inside that band and (b) is a **whole number of the surface's own committed
module** — 32 clapboard courses, 12 log courses, 20 sheathing boards. That second condition is
what stops the seam being visible, and it is why the tile sizes are odd numbers of metres
rather than round ones.

Two surfaces cannot be sized: **brick and stone**. Their rhythm is a brick dimension, this
repository holds no source that gives one for Chicago in 1835, and choosing one to make the
arithmetic land would be exactly the invention `docs/LIBERTIES.md` exists to catch. Leave them
untiled or record the liberty; do not quietly pick a modern brick.

### 3.3 Where the pixels come from — the licensing answer, decided here

**Generate them; do not photograph them.** AGENTS rule 6 and `assets/LICENSES.md` gate this
hard, and the arithmetic is not close:

- **38 of this project's 65 sources are `rights_status: check_required`** and may be cited in
  text but must not have an asset derived from them. Every `chicagology_*` record is in that
  set, and that is most of the visual material.
- The one photograph committed at full resolution — `saari_2018_dupage_tallgrass` — is CC
  BY-SA 4.0, cleared for **verbatim redistribution and measurement and explicitly not for any
  derived asset**. `assets/LICENSES.md` spells out that a tile built from it is an adaptation
  carrying ShareAlike. It is also a prairie, not a wall.
- **The one set that could inform materials is rights-gated for exactly this.**
  `data/sources/assets/prefire_views_kevin_2026_08/` — twelve retrospective views supplied by
  the owner as the accuracy bar — states in its own README that it "may drive massing, roof
  form, fenestration rhythm, **materials** and setting as `inferred`". It is also mostly
  `chicagology_*`, which `assets/LICENSES.md` gates `check_required`: **cite it, read it, do
  not derive a tile from it.** That is not a loophole to route around; it is the distinction
  between evidence and pixels, and this sheet is on the evidence side of it.
- No source in `data/sources/` is a photograph of an 1830s Chicago building surface. There is
  no such photograph; the town burned in 1871 and photography arrived after these buildings.

So the atlas should be **procedurally generated from the dimensional constants in §2**, which
the generators already commit and which are themselves sourced or argued. That route needs no
new `assets/LICENSES.md` clearance beyond a row saying the tiles are generated output covered
by the project's own license — and it has the property this project actually cares about: a
visitor can be told exactly which numbers the wall was drawn from.

### 3.4 State the colour space on every value — this sheet's one process rule

The two generator paths express colour differently and **neither module states which space it
is in**. `logwork.py` says its values are linear; `inferred_placeholder.py` writes hex strings
straight into `baseColorFactor`, which glTF defines as linear, and hex notation conventionally
means sRGB.

**This sheet does not claim a bug, because the evidence points the other way.** The one finish
both paths name is whitewash: the archetype's linear `0.88, 0.87, 0.83` against the
placeholder's shipped `0.847, 0.820, 0.737` — a 12.6 % gap in blue. Read the placeholder hexes
as sRGB instead and they would ship at `0.687, 0.638, 0.503`, a 40 % gap. The hexes were
evidently chosen as linear values, and the town is consistent.

But it is consistent by luck of authorship and not by anything written down, and an atlas is
where that stops being survivable: a PNG *is* sRGB-encoded by convention, so the sheet and the
factor it multiplies will be in two different spaces unless someone says so. **Every colour
value W2 produces states its space, in the file that holds it.**

---

## 4. Findings

Five things found while inventorying, none of them patched here.

**1 — The chimney is not a material in this project.** `frame_dwelling`, `frame_storefront`
and `log_dwelling` all build their stacks with `M_ROOF`: **219 chimney stacks on 199
buildings are painted with the roof's colour**, `0.34, 0.30, 0.27` at roughness 0.90. The 90
placeholder buildings, meanwhile, ship a real `placeholder_chimney_brick` at `0.537, 0.314,
0.247`. So the town has a brick chimney material, and the 199 buildings built from archetypes
do not use it. It is worse than a palette slip: `log_dwelling`'s own docstring argues at
length that a frontier stack is *stick-and-clay or fieldstone* built outside the gable so it
can be pulled down when it catches fire — a materially different object from a framed house's
brick stack — and the two render identically, as roof. Opened as **R-W2c**.

**2 — One log wall in Chicago is a different timber from the other 52.** `frame_tavern` alone
imports `LOG_RGBA` (`0.42, 0.33, 0.24`, roughness 0.90); everything else uses `HEWN_RGBA`
(`0.340, 0.266, 0.188`, roughness 0.92–0.93), which `logwork.py` says it made ~20 % darker on
purpose, having measured that a first pass at 0.295 "put the log dwellings visibly in a
different town from the Sauganash's wing". The reconciliation went one way and the Sauganash
did not follow. One asset is affected — the Sauganash's log wing, the single most-looked-at
building in the scene, and the station `sauganash` stands in front of it.

**3 — `timber` is one name over two materials 3.2× apart.** `outbuilding.py`'s
`0.208, 0.172, 0.128` ("heavy timber holds moisture, weathers darker") and
`frame_storefront.py`'s `0.66, 0.56, 0.40` ("fresh sawn lumber, paler than a wall") are both
defensible and are not the same thing. Only the outbuilding's ships — no record turns
`framing_exposed` on — so this is latent rather than visible, and it will surface the first
time a storefront exposes its framing beside a shed. R-W2b should give them two names.

**4 — The data speaks a finish vocabulary that no archetype reads.**
`roof_condition` is stated on **218 records** and `finish_key` drives six wall finishes, and
both are read only by `inferred_placeholder`. On all 244 archetype buildings a weathered roof
and a fresh one are the same pixel. Separately, `cladding` is stated on **27** records and
read on **22** — `frame_storefront`'s. The three taverns and two log dwellings that state a
cladding state it into nothing, and one of those five is the sharpest material attestation in
the dataset: `cobweb_castle` carries `cladding: clapboard_part_way_up`, **`attested`**, sourced
to `andreas_1884_v1` — *"the agency-house being afterward clapboarded part way up"*, David
McKee's recollection. **A documented fact about a real building's surface is committed, correct,
and rendered by nothing**, and the value is not even in `CLADDINGS`. That single record is the
best argument in the repository for why W2 is worth doing.

**5 — 27 % of the town is painted by a generator with no shared palette.** The 90 inferred
placeholders share not one colour and not one roughness with the 244 archetype assets: their
walls are all roughness 0.86, a value that appears nowhere else; their roofs are 0.90 at four
colours the archetypes do not have. Any atlas that textures the archetypes and not the
placeholders will split the town visibly in half, and the placeholders are the anonymous
background buildings — the ones that *make* the town read as a town. Whatever W2 builds must
cover both paths, and §1.1's vocabulary is the one to converge on because the records already
carry it.

---

## 5. What this sheet does not settle

- **The shingle exposure**, and therefore the roof tile — §2.2. It needs a source or a liberty.
- **Brick and stone course dimensions** — §3.2. Same.
- **Which way finding 1 should go**: give the archetypes the placeholder's brick, or model the
  stick-and-clay stack `log_dwelling` argues for. That is a research question about frontier
  chimneys, not a palette question, and R-W2c should open with it.
- **Whether `roof_covering` is a new attribute or a widening of `cladding`.** It is a schema
  change either way and it touches 315 records, so it is a parcel, not a footnote.

Nothing above was derived from a source this repository does not hold, and no confidence was
raised to make a row look finished.
