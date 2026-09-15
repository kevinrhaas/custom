# STATUS

## Shipped 2026-09-15 â€” T-1143: every research reading has an accountable outcome

The old research-spend measure is preserved at **21,419 read / 7,769 ruled / 13,650
unspent**; changing that baseline would have hidden the backlog instead of closing it. A new
generated ledger now accounts for **23,699 reading units across all twelve committed research
domains**, including the previously unregistered Genealogy Trails, newspapers and resident
research passes. Every row is exactly one of asserted, later-only, outside Chicago,
aggregate-only, refused or unresolved, and zero rows are unclassified.

This does **not** claim the backlog is all on resident cards. The exact structured-target test
finds 170 asserted units. Another 19,304 are durably dispositioned without pretending they are
1835 assertions, and **4,225 remain unresolved** under open T-1145, T-1146 or T-1147. The older
second hop remains independently green at **1,643 reached / 1,643 on a card / 0 unwritten / 0
source-less**. The ledger gate now fails on an unregistered domain, an unmatched reading pattern,
an unclassified or duplicate unit, a dead source or target, a closed unresolved owner, or an
attested/inferred assertion that survives only as prose. Its mutation self-test breaks each of
those contracts in memory.

No resident, structure, business or visible scene output changes in this ticket. It establishes
the accounting surface that T-1137 and the queued research-completion work must preserve and
spend. The generated dated review is `docs/RESEARCH/research-spend-ledger-2026-09-15.md`.

## Shipped 2026-09-13 â€” T-1106: the far band is a wall, and it had been dealt as a floor

**T-0280 put both sides of the far band's grass-or-flower split into the same unit, and picked
the wrong one.** That ticket was right that a cover cannot be divided by a lattice probability,
and its ground-cover reading stands as the honest mix for GROUND. The far band is not ground.
Its nearest card stands 34 m from the visitor and its furthest 95 m; at fifty metres a 1.7 m eye
looks 1.9 degrees below horizontal, so the sward is seen **edge-on, as a wall**, and the plant
that fills a pixel is the first element the ray meets. What governs that is projected area per
element times elements per mÂ² of ground â€” **silhouette-area density** â€” and the depth of the
wall cancels out of a ratio between two strata standing in it.

**The module already held that model, one field over.** `tools/measure_far_bloom.mjs` Â§1 has
priced the BLOOM share on exactly this `n Ã— a` bridge since T-0209, stating the same edge-on
argument. Between T-0280 and this ticket the far band was reading one wall in two different
units.

**What changed.** `silhouetteOf(sp)` = `stems Ã— w Ã— h`, beside `coverOf`'s `stems Ã— Ï€Â·clumpÂ²`;
`subsetOn()` sums it as `sil` beside `cover`; `farSplitOf` decides the boundary **once per
community per side of the waterline** instead of per lattice slot, and `rebuildFar` now reads a
constant rather than computing a ratio. The matrix side is the record's own `matrix_fraction`
**converted** by the graminoid stratum's own measured aspect `sil / cover`, not replaced by the
species rows' raw sum â€” T-0280 chose the authored figure deliberately and this keeps that
choice. `matrixSil` is exported beside it so the two can be checked against each other. No
constant enters the split that is not summed off `data/flora`.

**The liberty, stated: L236.** The silhouette of a clump is its **bounding rectangle** `w Ã— h`,
with no shape factor. It is explicitly NOT the far card's own quad â€” that card's width is the
aggregate `band.wide` L137 gives it, not this plant's. A shape factor cancels out of the ratio
wherever the two strata share a growth form, the project has no measured profile for either to
make it not cancel, and applying one to a single side would be a thumb on the scale. L235 is
revised in the same pass: the fallback width it covers is now one factor of `w Ã— h` rather than
the radius of a disc, and is otherwise untouched.

**It moves both ways, which is the test that it is a measurement.**
`tools/measure_far_split.mjs --source` now prints all three units side by side. The forb's share
of the far cards, per community:

| community | T-0209 lattice | T-0280 cover | T-1106 silhouette | move | aspect gram / forb |
|---|---|---|---|---|---|
| z10_settled_town | 68.97 %* | 46.75 % | **72.72 %** | 1.556Ã— | 0.67 / 2.04 |
| z06_dense_forest | 74.07 %* | 72.10 % | **78.48 %** | 1.088Ã— | 1.91 / 2.70 |
| z04_marsh | 57.14 %* | 38.02 % | **38.01 %** | 1.000Ã— | 3.98 / 3.98 |
| z03_sedge_meadow | 54.05 %* | 11.51 % | **8.25 %** | **0.717Ã—** | 3.47 / 2.40 |
| z05_riverbank_timber | 68.97 %* | 5.26 % | **10.39 %** | 1.974Ã— | 2.12 / 4.43 |
| z02_mesic_prairie | 51.28 %* | 2.74 % | **3.73 %** | 1.364Ã— | 2.63 / 3.62 |
| z01_wet_prairie | 50.00 %* | 2.95 % | **3.62 %** | 1.228Ã— | 3.22 / 3.98 |
| z08_lakeshore | 74.07 %* | 6.33 % | **6.50 %** | 1.026Ã— | 2.18 / 2.24 |
| z09_sand_prairie | 35.45 % | 0.16 % | **0.30 %** | 1.938Ã— | 2.05 / 3.98 |
| z07_bur_oak_savanna | 0.00 % | 0.00 % | 0.00 % | â€” | â€” |

`*` was sitting on the forb ring's 1.000 ceiling. `aspect` is each stratum's own `sil / cover`,
the square metres of wall one square metre of its floor stands up, and the move is the ratio of
the two â€” arithmetic, not a tuning. **`z03_sedge_meadow` goes DOWN**, because its sedges are the
taller narrower stratum; `z04_marsh` moves by one hundredth of a percentage point, because its
two strata happen to share an aspect of 3.98. A change that could only add flowers would not be
a measurement.

**At the three gate stands**, the annulus weighted by the ground it lands on:

| stand | T-0209 | T-0280 | T-1106 | far cards |
|---|---|---|---|---|
| prairie_west (z02_mesic_prairie) | 51.40 % | 4.72 % | **6.62 %** | 226 |
| prairie_south (z05_riverbank_timber) | 52.04 % | 7.33 % | **8.97 %** | 241 |
| river_bank (z04_marsh) | 42.07 % | 19.93 % | **24.41 %** | 28 |

**The drawn bloom, both readings measured on this same tree in this run**
(`tools/measure_far_bloom.mjs --source`, desktop):

| stand | heads before â†’ after | furthest | > 24 m | > 40 m |
|---|---|---|---|---|
| prairie_west | 1993 â†’ **1997** | 26.4 â†’ **47.5 m** | 102 â†’ **106** | 0 â†’ **4** |
| prairie_south | 1225 â†’ **1238** | 78.7 â†’ 76.5 m | 149 â†’ **162** | 19 â†’ **32** |
| river_bank | 43 â†’ 43 | 14.0 â†’ 14.0 m | 0 â†’ 0 | 0 â†’ 0 |

`prairie_west` regains the far tail T-0280 cost it â€” nothing past 40 m before, four heads now,
and the furthest head almost doubles. **It does not go back to 135.7 m, and it must not**: that
figure was bought by a clamped constant, and T-0280's refusal of it is not reopened here.
`prairie_south`'s furthest ticks down 2.2 m while its counts past 24 m and past 40 m both rise â€”
the tail is a re-deal of the same lottery and the single furthest head is its noisiest statistic;
the bin counts are the figure to read.

**What did not move.** Card count, instance count, draw calls, triangles, and where any card
stands: 226 / 241 / 28 far cards at the three stands before and after. This decides what a card
is a picture of, exactly as T-0209 left it. Zero sward records convert to no silhouette â€”
`silUnknown` is exported so that stays checkable.

## Shipped 2026-09-13 â€” T-0280: the far band's grass-or-flower split was reading a lattice ceiling, and now reads the ground

**Eight of the ten communities were splitting on the number 1.000.**

`rebuildFar` decides whether a far card stands for a grass or for a flowering plant with

    split = matrixShare Ã— (1 âˆ’ forbside / (matrixShare + forbside))

so the forb's share of the cards the band occupies is exactly `forbside / (matrixShare +
forbside)`, and the whole of this ticket is about which number `forbside` is. It was
`forbShare` â€” the **forb ring's** lattice occupancy, `min(1, density Ã— cellÂ² / perCell)` at one
plant per 2.89 mÂ² slot. Nine of the ten populated forb layers sit on that clamp (T-0019,
`tools/forb_clamp_baseline.json`), so for nine communities the far band's species mix was
decided by a ceiling and not by anything their records say. `z06_dense_forest` asks 66.381
plants per mÂ² and `z01_wet_prairie` asks 0.407, and the band split both as though they had
asked for the same thing.

**And it was the wrong kind of number even unclamped.** `matrixShare` is
`cover.matrix_fraction`, a fraction of GROUND COVERED; `forbShare` is a slot-occupancy chance
derived from stem density. Dividing one by the sum of both adds an area to a probability â€”
K49(a)'s unit error, one stratum further out â€” so raising the clamp would have swapped a wrong
constant for a wrong quantity. At 66.381 plants per mÂ² the unclamped share is ~1 and every far
card in the dense forest would have been a flower.

**Both sides are now the same quantity: the ground the stratum covers.** `subsetOn().cover`
sums `stems Ã— Ï€Â·clumpÂ²` over the subset that may stand on this side of the waterline, which for
a cover-recorded species hands back its own `cover_fraction` intact. The matrix side stays the
record's own `matrix_fraction` â€” that same quantity, already written down.

**The clump is the drawn one, and it has to be (L235).** Fifty sward records state no
`width_m`: every forb of the wet prairie, the mesic prairie and the sand prairie, and both
marsh forbs. A sum over recorded widths alone returns **0.0000** for the sand prairie and
**0.0000** for the marsh, and the band would deal both as pure grass on the strength of a
missing field. `coverOf` falls back to `clumpRadiusOf` â€” the footprint `crowdsTheWalker` has
given those plants all along â€” and `flora.communities()` exports `forbCoverFallbacks` so the
provenance of every figure below is visible rather than assumed.

**The instrument.** `tools/measure_far_split.mjs`. BEFORE and AFTER are not two runs compared
by hand: `communities()` exports `forbShare` beside `forbCover`, so both are arithmetic on the
same compiled communities in one pass. Â§2 samples the far band's annulus (16â€“175 m) with the
placer's own `zoneAt` and a new `flora.isWaterAt` â€” `shoreDistance` cannot say which SIDE of
the waterline a sample is on â€” and weights each sample by `farBand.coverAt(d)`.

| community | matrix | forbShare | forbCover | before | after | w-less |
|---|---|---|---|---|---|---|
| `z06_dense_forest` | 0.350 | 1.000\* | 0.9045 | 74.07 % | **72.10 %** | 1 |
| `z10_settled_town` | 0.450 | 1.000\* | 0.3950 | 68.97 % | **46.75 %** | 0 |
| `z04_marsh` | 0.750 | 1.000\* | 0.4600 | 57.14 % | **38.02 %** | 2 |
| `z03_sedge_meadow` | 0.850 | 1.000\* | 0.1106 | 54.05 % | **11.51 %** | 1 |
| `z08_lakeshore` | 0.350 | 1.000\* | 0.0237 | 74.07 % | **6.33 %** | 3 |
| `z05_riverbank_timber` | 0.450 | 1.000\* | 0.0250 | 68.97 % | **5.26 %** | 0 |
| `z01_wet_prairie` | 1.000 | 1.000\* | 0.0304 | 50.00 % | **2.95 %** | 11 |
| `z02_mesic_prairie` | 0.950 | 1.000\* | 0.0267 | 51.28 % | **2.74 %** | 9 |
| `z09_sand_prairie` | 0.600 | 0.329 | 0.0009 | 35.45 % | **0.16 %** | 5 |
| `z07_bur_oak_savanna` | 0.900 | 0.000 | 0.0000 | 0.00 % | 0.00 % | 0 |

\* on the clamp. Read the `before` column down: it is 50â€“74 % everywhere, and it is 50â€“74 %
everywhere **because it is `matrixShare` divided by `matrixShare + 1`**. The `after` column
spans 0.16 % to 72 %, and it is ordered the way the records are: a prairie is a grass matrix
with scattered forbs, a closed forest floor is a herb layer under a canopy. Nothing about the
mix was a reading before; all of it is now.

At the stands, the annulus weighted by the ground it lands on: `prairie_west` **51.40 % â†’
4.72 %**, `prairie_south` **52.04 % â†’ 7.33 %**, `river_bank` **42.07 % â†’ 19.93 %**. The card
count does not move at any of them â€” 226, 241 and 28 far cards before and after â€” because this
decides what a card STANDS FOR, exactly as T-0209 left it.

**What a visitor loses, stated plainly** (`tools/measure_far_bloom.mjs --source`, desktop). At
`prairie_west` the drawn heads go **2,522 â†’ 1,993** and the furthest **135.7 m â†’ 26.4 m**; at
`prairie_south`, 1,602 â†’ 1,225 and 167.1 m â†’ 78.7 m; `river_bank` is unchanged at 43 and 14.0 m
(its band is mostly water and timber). **The distant bloom was bought by the clamp.** T-0209's
acceptance â€” *bloom past twenty-four metres at `prairie_west`* â€” still holds on 102 heads, and
nothing past 40 m survives. That is the honest consequence of taking a constant out of a ratio,
not a regression to repair by putting it back: if the far sward should read as more flowered
than its ground cover, the argument for that is a SILHOUETTE reading (a tall forb is more
visible per square metre of ground than the grass it stands in), which is a different
measurement and is filed as its own ticket.

**Files:** `renderers/web/js/flora.js` (`clumpRadiusOf`, `coverOf`, `subsetOn().cover`,
`rebuildFar`, `communities()`, `isWaterAt`) Â· `tools/measure_far_split.mjs` (new) Â·
`docs/LIBERTIES.md` L235.

## Shipped 2026-09-13 â€” T-0277: what a density handover would cost the sward's far edge, re-measured against the corrected ruler

**The ramp stays, and this time the reason is a reading rather than an inherited one.**

`TUNE.mid.band` and `TUNE.forb.band` are the last two coverage ramps in the sward. Every
other boundary â€” the near ring's outer edge, the mid ring's inner one, both far bands â€”
hands its ground over by DENSITY (T-0093, T-0086): each slot carries its own boundary drawn
from a world-anchored rank, and a plant is drawn whole or not at all. These two still ramp,
so at `full` the last few metres of grass and flowers are resolved through the 4x4 screen
door â€” a band of dots per pixel.

**Why it had to be re-asked.** T-0187 priced the change and kept the ramp, and its
arithmetic was never in dispute. Its RULER was. Every figure it compared against was read at
`flora.fadeAt(...) > 0.02`, a coverage the screen door renders as nothing whatever for two
instance phases in three (T-0225), so a coverage ramp was being credited with reach no
visitor could see. The gate reads the boundary at 1/16 now â€” the screen door's own quantum â€”
and carries the `band x 1/16` inset that costs. The comparison a spread has to win is
therefore a different one, and this is the re-run.

**The instrument.** `tools/simulate_outer_spread.mjs` stands where the gate's part 7 and
`tools/measure_sward_reach.mjs` stand, bins the same 16 bearings over the same +/-30 degree
cone, and for every placed mid and forb instance reports the drawn boundary under both
representations â€” today's ramp read at 1/16, and `slotRing`'s own arithmetic on this slot's
own `aChiRing` with the rank asked of the placer through a new `flora.handoverAt` (the rule
`fringeAt` set: ask the placer, do not re-derive the noise in the tool). It reproduces
`measure_sward_reach.mjs`'s reading of the unmodified tree to the centimetre at both
viewports, which is what makes its other column worth believing. Partial spreads are priced
too, so the choice is read off a curve.

| ring, tune | today, at 1/16 | fully spread | bars, spread |
|---|---|---|---|
| mid, `full` | 25.00 min / 26.61 mean (bars 21.76 / 24.46) | 22.58 / 25.36 | 22.20 / 24.90 â€” **clears** by 0.38 / 0.46 m |
| mid, `light` | 10.32 / 11.96 (bars 9.50 / 11.50) | 8.56 / 11.23 | 9.60 / 11.60 â€” **over** by 1.04 / 0.37 m |
| forb, `full` | 23.52 / 24.74 (bars 20.89 / 23.59) | 16.41 / 21.73 | 21.20 / 23.90 â€” **over**, from a quarter of the band upwards |

At `light` three quarters of the band is over as well (11.57 mean); half clears at 11.75.
The forb ring at `light` is over under every representation including the unmodified one â€”
11 or 12 bins of 16 and a 4.47 m minimum â€” which is the sampling the instrument already
declines to read a boundary off, not a defect this introduces.

**Why it loses, in two parts, and the second is a better reason than T-0187 gave.**

1. *The bar rises when the band is spread.* `ringsFor` replaces a spread layer's `band` with
   `HARD`, so the `band/16` a reading at the quantum sits inside the placed boundary â€” 0.44 m
   at `full`, 0.10 m at `light` â€” vanishes. A spread must clear a HIGHER bar with a SHORTER
   reach. Printing it against the ramp's own bars would have flattered it by 0.44 m, which is
   most of the margin it has.
2. *A handover's boundary is a SAMPLE, and its expectation falls with the slots in the bin.*
   The desktop cone holds 642 mid slots, forty to a 3.75-degree bin, and one of forty draws a
   rank low enough to stand near the boundary. The `light` cone holds 132, about eight to a
   bin, and eight draws do not reach it. At `light` the mid ring is as sparse as the forb ring
   is at `full` â€” exactly the case `measure_sward_reach.mjs` refuses to read a boundary off.

**And it cannot be taken one edge at a time.** `full` would carry a mid spread; it will not
carry a forb one. But the forb ring ends within a metre of the mid ring deliberately, so the
two boundaries land on the same screen row â€” spreading only the grass would leave the flowers
dithering along the line the grass had just stopped drawing, drawn by half as many plants and
against a step. A split decision is worse than either whole one.

**Nothing moved.** No plant, no ring, no byte of geometry: the only renderer change is the
additive `flora.handoverAt` accessor the tool reads through, and the TUNE commentary now
carries these figures instead of the superseded ones. Reopening this means changing what is
measured, not the bar â€” a sward dense enough at `light` for eight plants a bin to become
forty, or a forb layer that does not have to share the mid ring's boundary.

Verified: `tools/check.sh`; `node tools/measure_sward_reach.mjs --source` at both viewports
(unchanged from dev); `node tools/simulate_outer_spread.mjs --source` at both viewports;
the smoke parts `tools/smoke_budget.mjs --for-diff` prices for this diff.

## Shipped 2026-09-13 â€” T-0334: the line the Trustees walked round the built-up town

Section 22 of the by-laws passed 5 August 1835 forbids stacking hay inside a boundary the
ordinance walks street by street â€” Washington Street at the U.S. Reservation, west to Canal,
north to Kinzie, east to Wolcott, north to Illinois, and out to Lake Michigan â€” at $25 a
stack. **It is the only documented statement this project holds about where the built-up
town ended in the scene year.** Every other judgement here about density comes from the
plat, the land sales and measured frontage.

`tools/derive_hay_limits.py` derives it into `data/reconstruction/1835_hay_limits.json` and
`check.sh` re-derives it on every commit. All six of the ordinance's vertices are
intersections of committed `path_local_enu_m` centrelines; five are true crossings, and the
sixth carries the Illinois Street line 100.78 m past its committed east end to the traced
1834 shore (recorded, gated at 150 m). The start â€” *"on Washington street, at the United
States Reservation"* â€” is where Washington's line meets the committed reservation ring's
west side, and it lands there to the centimetre.

**What is decided rather than derived, and graded `inferred` with its reasoning:** the
ordinance walks an OPEN line and ends at the lake, so closing it needs the two sides it
names but does not draw. The ring closes down the traced lake shore, across the harbour
entrance in one straight segment (water between two piers â€” a closure, not a claim about
ground), west along the reservation's own traced waterline and south down its west side.
The reading this rests on â€” that a walk *commencing at* the reservation is bounded by it,
so the garrison was not subject to the town's hay rule â€” is recorded with its alternative
and what that alternative would cost (the 23 fort structures would come inside; nothing
else would move).

**Measured:** 199 acres, 4,715.9 m round, 30 vertices. Of 383 committed structure
positions, 302 inside and 81 outside â€” 23 on the reservation, 36 west of Canal, 20 north of
the Kinzie/Illinois line, 1 south of Washington (Heacock on Monroe), 1 in the harbour (the
South Pier).

**The disagreement with the block-infill programme, named.** 18 of 21 scheduled blocks are
inside and the schedule places no NEW roof outside. The three outside are the Clintonâ€“Canal
tier, which the boundary leaves out because it turns north AT Canal. Two are `at_capacity`
and hold 21 standing roofs between them (11 and 10 of 31); the third is already
`not_a_block`. So the reconstruction's built town reaches one tier further west than the
town's own fire line did. Either the roofs were there and the line was drawn short, or the
tier is a block too far west. Stated, not settled.

**Nothing is drawn in the scene,** and `docs/LIBERTIES.md` carries no new admission: a legal
limit is not a fence, and nobody in 1835 could see this one. It reaches a visitor on the
card â€” `renderers/web/js/ordinances.js`, a new *"Was it inside the town's fire limit?"*
section with the verdict, the acreage, the section's own words and the citation. 383 cards
gain the row.

The ordinance is 35 days after the scene date. Carried as evidence ABOUT 1835; nothing is
placed, moved or dated because of it, and `date_standing` in the file says so.


## T-0385 â€” the New York Clothing Store stands against the Tremont House

Tuthill King's card â€” American 1835-06-08 c014, 1835-06-20 c007, 1835-07-04 c003,
one dateline of 8 June 1835 â€” places the shop *three doors north of the Tremont
House, in Dearborn Street*. The register read it as `street_only` on `dearborn`
because the gazetteer mints a house's live placement from its EARLIEST printing,
and the earliest of these three falls inside an 8,024-character blob with the
hotel's name cut away. The second impression loses "of the" and the name and keeps
only "House". Only the third prints "[the T]remont House".

The `match_landmarks` blocker the ticket names is no longer one: `tremont_house_1`
carries the plain aka `Tremont House` and `{tremont, house}` resolves to it today.
The live blocker was the second one the ticket's prior attempt found, and it is
what this ships.

**The rule.** A reading that declares its own anchor UNREAD does not hold a house's
placement against a reading of the same advertisement that names it. It is stated
in `compile_gazetteer.py` beside the T-0440 pass, in prose and not only in code.
`anchor_unread` is an authored field on the placement â€” the pass that could not read
the word is the one that says so â€” and `claim_problems` now refuses an anchor whose
prose says it was unread and whose field does not. Six placements in the corpus
carry the flag.

**The bounds, and they are what stop it becoming a judgement it may not make.**
Same class; same street where the unread reading names one; ONE dateline at or
before the scene date, which is what makes the impressions one card â€” and it has to
be the dateline rather than T-0440's issue-date bound, because the legible
impression of King's card is 3 July and the scene date is 1 July. That impression
is not an address first printed after the scene date: the address ran on 06-08 and
06-20 and all that is gained on 07-04 is the ability to read it. Two datelines are
refused and left to `anchor_changes`. The pass never reorders two anchors both of
which were read.

**What moved.** One business. `business_new_york_clothing_store` resolves to
`structure tremont_house_1` and its register row goes `street_only` â†’ `new_building`
(`street_only` 60 â†’ 59, `new_building` 28 â†’ 29). It leaves the street-face adoption
deal (40 â†’ 39 adopted), so `recon_1835_blk_randolph_clark_d6_04` passes to Fullerton
& Botsford and three other Dearborn roofs re-allocate. The two remaining unread
anchors â€” `business_hubbard_co`, `business_s_b_cobb_saddle_harness_and_trunk_manufactory`
â€” keep theirs: neither has a second impression to be read against.

**What is NOT shipped.** No geometry. `new_building` is a finding and no tool in this
project builds from one; all 29 rows are in that position. A roof three doors north
of the Tremont House is owed and does not stand, and T-0306's remaining pieces carry
it. The ticket was filed `needs_bake: true` and needed no bake: nothing staled
(`validate.py --stale`: 380 assets match their inputs, 0 stale).

**Verified.** `tools/check.sh` green, 304 steps, none red; gazetteer self-test 132
cases (9 new, each proved by disabling the pass and watching it fail). Renderer smoke
per `smoke_budget.mjs --for-diff`, recorded in the PR.

## T-0983 â€” continuation FS closes at 125 over twenty-seven households

Image 58 is now recorded in `pages/33SQ-GYYJ-FS.json`, with every visible
continuation block inspected. The contact-sheet inventory had counted 28 occupied
rows and read the family footing as 152. Native-resolution row crops show 27
occupied rows and three blank ruled positions; the apparent last row was the
footing below the closing rule. Its glyphs read 1, 2, 5, not 1, 5, 2.

The 27 family totals were read before addition and sum independently to 125.
Manufactures and trades closes at 12, inland navigation at 1, and learned
professions at 1. The other four industry columns, slaves, pensioners, and
disability columns are blank in body and footing. A horizontal mark straddling a
school-column rule remains unresolved, its school footings are blank, and the
literacy column at the bound edge remains unread.

Neither published pairing key contains a 27-household or 125-person left sheet.
Printed 240 does have 27 names, but four unread cells leave it without a population
key, so it cannot pass both tests. FS remains unpaired and contributes no name,
occupation, resident, or 1835 placement. Group 3 now has six continuations read
line by line and nine images inventoried only. T-0984 retains the remaining eight
filled leaves and blank BH, one leaf per run. PR #1044 carries this completion.

## T-0981 â€” continuation BS: twenty-nine households, unpaired

Image 56 is recorded in `pages/33SQ-GYYJ-BS.json`, with all 29 occupied TOTAL
entries and every continuation block inspected. Twenty-six family totals are
readable and sum to 102. Lines 4, 10 and 12 remain null with alternatives 4 or
11; the resulting conditional totals are 114, 121, 128 and 135, none equal to
the written footing 131. The discrepancy stays recorded and no glyph is chosen
from the arithmetic.

All seven written occupation and school footings close independently: agriculture
2, commerce 7, manufactures and trades 5, inland navigation 1, learned professions
1, one primary/common school and 115 scholars. Mining and ocean navigation are
blank in the body and footing. The slave, pensioner, and disability blocks are
blank; the literacy column at the bound edge remains unread.

The only available left-sheet key with 29 occupied households is printed 226,
with population 184. The only population key of 131 is printed 208, with 30
households. Neither passes both keys, so the sheet remains unpaired and sequence
evidence is not used. No household identity, resident, occupation, or school fact
is projected into 1835. Group 3 now has five continuations read line by line and
ten images still inventoried only. T-0982 retains the remaining nine filled leaves
and blank BH, one leaf per run. PR #1043 carries this completion.

## T-0979 â€” continuation 9ZK: twenty-three households, unpaired

Image 53 is recorded in `pages/33SQ-GYYJ-9ZK.json`, with all 23 occupied TOTAL
entries and seven industry columns inspected. Nineteen totals are read and sum
to 95; lines 3, 4, 18 and 21 remain null with alternatives. Their one conditional
completion to the written footing 119 is recorded without filling any cell.
The inventory's old strip sum of 118 is not promoted to a reading.

Agriculture closes at 2 + 1 + 1 = 4. Eleven manufacturing entries close at 21,
including the independently read 7 on line 20. Inland navigation has one body
entry and no written footing. A horizontal professions mark, a crossed mark
beside a disability-column rule, and an upright mark near the school binding
remain unresolved. The literacy column is unread. Geometry records the measured
bands, individual crop boxes and the instrument's spurious component groups.

The sole committed left sheet with 23 households is printed 225 (9HY), whose
115-person footing agrees with its own cells. It fails this sheet's 119-person
key. No household identity or 1835 occupation is assigned. Group 3 now has four
continuations read line by line and eleven images still inventoried only.
T-0978 split in place: T-0979 owns this leaf, T-0980 retains ten filled leaves
and blank BH. PR #1042 carries this completion.


## T-0977 â€” continuation 9SQ: thirty entries, four unresolved totals

Image 52 is read in `pages/33SQ-GYYJ-9SQ.json`: 30 occupied TOTAL entries,
all seven industry columns, and the other visible blocks. Four totals remain null
(lines 5, 7, 13, 16), with visual alternatives. The 26 readable totals sum to 149.
Only one combination of those alternatives reaches the written 175, but arithmetic
is not a reading; none is filled. Agriculture 1, commerce 4, inland navigation 1
and professions 6 close independently. Four clear manufacturing entries also sum
to its footing 4, but a fifth short upright mark stays unresolved. A small loop
beside a slave-column rule is unresolved; the obscured school/literacy edge is unread.

Printed 224 (JM) shares 30 households and 175 people, but only 2 of the 26
readable right-hand totals match its independently committed household sequence.
That coincidental two-key match is refused. Printed 216 (DD) has 175 people but
31 households and fails the count. The sheet stays unpaired and assigns no names
or occupations to 1835 residents. Measured column bands, crop boxes and the
instrument's truncated-body limitation are recorded on the page.

Group 3 now has three continuations read line by line and twelve inventoried-only
images. T-0975 was split in place: T-0977 owns this leaf; T-0978 retains eleven
filled leaves and blank BH, one leaf per run. PR #1041 carries this completion.


## T-0976 â€” seven open PRs reconciled

PR #1040 integrates the PW recapitulation and BP/P5 named census sheets, preserves four competing page readings with their original commit hashes, and repairs the Loyd abbreviation and courtesy-title identity defects. The garden comparison is available without changing its rule. The full disposition and validation requirement are in [the reconciliation record](RESEARCH/open-pr-reconciliation-2026-09-08.md).

## Completed reading â€” T-0974: 31 census lines, three occupation footings closed

All 31 entries on image 51 are recorded in `pages/33SQ-GYYJ-9J5.json`, including
six unresolved family totals. The 25 readable totals sum to 150; that is a partial
sum, not the sheet population. The enumerator writes **179** at the foot. Four
assignments of the recorded alternatives would reach 179, so arithmetic alone
cannot settle which separated-stroke cell is 11 rather than 4. No assignment is
selected. Three occupation columns close independently: commerce **6**,
manufactures and trades **8**, learned professions and engineers **2**. The other
four industry columns have no written entries.

The slave and pensioner blocks are blank. The disability block has one unresolved
short vertical mark in the white-blind column on line 30; its 8 by 28 px box and
reason for withholding a value are recorded. The seven school columns are blank;
the narrow illiteracy column is obscured at the binding and remains unread.

The page stays **unpaired**: no available printed population key for a 31-entry
left sheet equals 179. Sixteen equal-line-count candidates are listed, with
unread population keys distinguished from mismatches. No name, serial, 1835
resident, occupation or grade is derived from the unpaired continuation.

T-0973 was split under the queue's one-leaf-per-run rule. T-0974 owns this reading;
T-0975 preserves the remaining twelve filled continuations and the blank leaf in
the parent's queue position. The continuation coverage count includes inspected
lines with unresolved cells; it is not a claim that every glyph was deciphered.


## Shipped 2026-09-11 â€” T-0432: blk_south_water_dearborn's second deal, and the last block with room in it

**What shipped.** Three roofs on `blk_south_water_dearborn`, the FOURTH and last of the South
Water blocks T-0009's ruling unblocked (T-0420 piece 4 of 4):

- `recon_1835_blk_south_water_dearborn_d3_08` â€” a **D3 one-room frame cottage**, 5.047 m wide,
  standing ON the committed South Water block face at the plat module's 1.5 m margin, its
  **east wall the west wall of `frederick_thomas_shop`** on a shared party line.
- `recon_1835_blk_south_water_dearborn_d5_07` â€” a **D5 deep-plan frame cottage**, 6.835 m wide,
  the same party line read from the other side: its west wall is the shop's east wall.
- `recon_1835_blk_south_water_dearborn_a1_09` â€” the A1 stable in the same lot's yard, at the
  alley end.

The three and the shop make **21.2 m of continuous street wall** â€” 28.547 m to 49.742 m along
the face. Lot 7, the Lake-and-State corner, stays open. The block moves `open` â†’
**`at_capacity`**, free lots 2 â†’ 1, headroom 4 â†’ 0, standing roofs 11 â†’ 14; the town's standing
count goes 367 â†’ 370 of 667.

**The count of two is measured twice, in different units, and the two agree.** Lot 2 projects
onto the north face between 25.93 m and 52.86 m; less the plat module's 1.5 m margin each side
that is 23.93 m buildable, of which the shop holds 33.594 m to 42.907 m. West gap 6.164 m, east
gap 8.453 m â€” and the west gap is really 5.932 m, because `john_holbrook_store` ends at
24.662 m on the lot next door and the three-metre separation rule admits no party wall this run
did not declare. One roof each; neither gap takes two. Separately, T-0079 allows
`ROW_UNITS_PER_LOT` = 3 row units to a lot of this grid and the shop is one of them, so two more
reach that ceiling exactly. The metres also chose the western FAMILY: the generator sizes a D4
at 6.072 m, which will not go in 5.932 m, so the west unit is the D3 and the D4 returns to the
south district's balance.

**Every platted block the plat module reaches is now `at_capacity`.** That is the statement
T-0028 asked whichever of the four runs went last to make: the anonymous-block programme has run
out of committed ground. The 297 roofs still owed are all behind named gates â€”
`blk_south_water_market` (South Water's centreline stops 24 m short of control, 27 roofs) and
the four coverage gates west, south, north and at Wolf Point (270 between them). Fifteen of the
eighteen built-out blocks still hold one lot open on purpose; three have none, from earlier
parcels.

### The gate that had to be taught something: two deals may meet on one lot

`tools/generate_block_infill.py` accounted for a block's lots in four classes â€” built on by this
parcel, built on by another deal on this block, already carrying a roof, named open â€” and held
them **pairwise disjoint**. That made "built on by another deal" a PROHIBITION as well as an
account: a lot the first deal's run stood over could never be dealt again. It had never bitten,
because `blk_south_water_clark`'s two deals took lots 4 and 2 and never met. Here the block's
whole remaining headroom stands on lot 2, so the old ceiling of one principal roof per lot â€”
retired by T-0079 in August â€” would have gone on enforcing itself through an accounting rule.

Three changes, and each is bounded:

1. **The overlap is admitted.** "Built on by another deal" is now that set LESS the lots this
   deal builds on; the other three pairs stay disjoint and every lot is still accounted for.
2. **It is bounded by the density standard's own ceiling, counted across deals.** A lot may
   carry `ROW_UNITS_PER_LOT` row units; the units already standing are read off the committed
   ground, and a yard building is not one of them (a privy behind the row does not pack a
   frontage). A record this programme did not write carries no inventory class and is counted â€”
   Frederick Thomas's shop stands in this row whoever built it.
3. **The occupancy question is asked of the whole parcel, not of one entry.** `mine_ids` is one
   recipe entry's records, which on a block dealt once is every anonymous roof on it â€” so the
   question had always been asked of ground the parcel itself had not touched. Read with only
   its own records excluded, the first deal's `--check` saw the second deal's cottages as a
   stranger's houses, and the owner's business-front clause switched off under the shared lot the
   moment a third claimant stood on it. Every `recon_1835_blk_<block>_*` record is excluded
   instead. Nothing physical relaxes: lot margin, corridor, three-metre separation and the run's
   own strip all refuse what they always refused.

### T-0441's ceiling is not a wall here

PR #599, the closed prior attempt at this ticket, failed on the `balanced` tier's triangle
ceiling â€” `dev` at 1,208,434 of 1,210,000 and the branch at 1,210,608. The ceilings were raised
on the owner's ruling afterwards (#765). Measured on this branch by
`node tools/measure_detail_ceilings.mjs`: full **1,359,838 of 1,460,000** (PASS by 100,162),
balanced **1,200,848 of 1,280,000** (PASS by 79,152), light **773,942 of 825,000** (PASS by
51,058). The three roofs cost 1,704 triangles at the master.

### Derived layers that moved with the roofs

The siding stock is dealt over the whole town at once (T-0112), so three new clapboard walls
re-dealt `chicago_american_office`'s exposure and its GLB was re-baked in the same commit.
Re-derived and committed: the lot-line fences, dooryard plantings, planted rows, lot building
material, the town census, the land-tract join, the scene-date register, the street-face
adoptions, the Newberry leads (the fingerprint gate forces a re-parse of all four volumes) and
the frontage works. `tools/measure_generator_half.py`'s stated asset counts go 380 â†’ 383 and
378 â†’ 381.

## Shipped 2026-09-07 â€” T-0788: Wright's block numbers, read off the sheet instead of counted

**What shipped.** The Original Town's block numbers, **read**. `data/traces/thompson_block_numbering.json`
carried six numbers derived from two numerals on a 639 Ã— 719 px crop; it now carries
**twenty-four blocks, twenty-two of them numerals read off the georeferenced sheet**. All
nineteen generated blocks in `data/traces/vectors/thompson_lots.json` take a number where six did,
and **144 lots** are numbered where 40 were.

**The method is the finding.** This project is fitted to the BPL copy of Wright 1834 (RMS 17.5 m,
eight ground control points). So a block's four bounding street centrelines give a box in local
ENU, `tools/wright_px.py` maps it into the scan's pixel space, and IIIF returns that rectangle at
6Ã—. **The block fills the frame**, which takes "which block carries this numeral" away from the
reader and gives it to the fit. Every entry cites the region it was read on.

| tier | west â†’ east |
|---|---|
| South Water â€“ Lake | 21 20 19 18 17 16 â€” *falls* eastward |
| Lake â€“ Randolph | *28 29* Â· river Â· 31 32 33 34 35 36 â€” **rises** eastward |
| Randolph â€“ Washington | *45 44 43* 42 41 40 Â· **Public Square** Â· 38 37 â€” *falls* eastward |

*(italic: West Division, west of the South Branch)*

- **The run reverses tier by tier.** The old file refused to carry the count from one tier to the
  next and named a boustrophedon as one thing it could not rule out. That is what the sheet draws.
  A count carried straight down would have numbered the Lake tier backwards.
- **All four previously counted numbers are confirmed** â€” 21, 20, 17 and 16. Nothing moves; they
  stop being arithmetic. **Block 16 is G. Spring's** *"LOT No. 7, in block No. 16 â€¦ on Lake
  street"*, and that address now rests on a numeral in the block's own frame.
- **The Public Square is block 39, and Wright does not write it.** He washes the block pink, rules
  it into eight lots and letters *Public Square* where the number would go. 39 is the one number
  in the file still counted â€” across a single block, bracketed by 40 read west and 38 read east â€”
  and it carries `numeral_on_sheet: false`. It is written onto
  `data/reconstruction/1835_reserved_ground.json`, where the block's identity is argued.
- **The lot scheme is read on four blocks now**, not one: 20, 18, 16 and 40 each print 4 3 2 1
  across the north row west to east and 5 6 7 8 across the south. Block 40 sits in a tier whose
  BLOCK numbering runs the other way, so the lot run belongs to the block. **The grade does not
  move** â€” the lines it numbers are still the module's, and a number on a line nobody drew is
  conjectural whatever its own provenance.
- **Not every block carries eight lots.** The West Division block west of block 28 prints
  `1 4 5 8 9` â€” ten lots in two rows of five. No West Division block is generated today, so
  nothing is mis-numbered; it is recorded so the day one is, this is found first.

**What is refused, and it is most of the plat.** Twenty-four blocks of fifty-eight. The
Washingtonâ€“Madison tier, the North Division and the West Division beyond Clinton are refused
because the method is *cut the crop from committed street lines* and the street grid does not
reach them; a numeral found by eye on paper that stretches 3.7% is a numeral placed by the reader.
**Block 30** is refused separately â€” the Lake tier reads 29 on the west bank and 31 east of the
branch and the ground between is water, so 30 is somewhere not yet read. And one grid cell,
`blk_randolph_canal`, is **two** plat blocks with the river between them (44 and 43), so it takes
no number at all and both readings wait in `blocks_not_in_the_grid`.

**Nothing was promoted.** Every number stays `inferred`, not `documented`: the numeral is read,
but WHICH BLOCK carries it is an identification made through a Â±20 m fit against a 97 m block, and
the grade is the weaker of the two steps, as it was before.

**Verification.** `tools/check.sh` green, including `generate_plat_lots.py --check`, which
re-derives the whole grid byte for byte offline.

**Files.** `data/traces/thompson_block_numbering.json` (authored) Â·
`data/traces/vectors/thompson_lots.json` (generated) Â·
`data/reconstruction/1835_reserved_ground.json` Â· `tools/generate_plat_lots.py` (prose only) Â·
`docs/RESEARCH/thompson_block_numbering.md` Â§ 0 Â· `docs/RESEARCH/thompson_plat_grid.md` Â§ 4b Â·
`docs/RESEARCH/clark_reach_bulge_1834.md` Â§ 9.

## Shipped 2026-09-06 â€” T-0843: the mints ask the identity master before they write a card

**What shipped.** The prevention half of T-0839. #929 folded 42 duplicate cards under
written rulings and gated that every candidate cluster carries one â€” that is *ruling
coverage over the duplicates that exist*, and it stops nothing from writing the next one.

**The cause.** Three of the four minting passes test "does the town already carry this
person?" by SURNAME, and the proxy is partial by design: each skips the households minted
by itself and by the passes below it, so a card one of those wrote is invisible to it.
A man his sources spell six ways goes straight through the gap.

**The instrument.** `tools/identity_master_guard.py` â€” new â€” hands a candidate name to
`consolidate_resident_evidence.cluster()`, the identity master's OWN function, inside its
own surname bucket, with every identity of that surname standing as an anchor whether it
holds a committed card or not. It refuses only where the master merges (M1/M2/M3); where
the master refuses to choose between rivals (R2/R3/R4) so does this, and the candidate is
minted. Wired into the documented, placed and letter-list passes as refusal 9, each
consulted BLIND to exactly the households its own surname test skips, so no pass reads
back its own answer and all three stay re-derivable beside each other. `mint_civic_
residents.py` already consulted the master (its refusal 2) and is unchanged.

### The rules are not re-implemented, and the first draft is why

Written out by hand from `MERGE_RULES`, the resolver reported **19** committed cards as
duplicates of each other where the master itself reports **2**. A hand copy of M2 cannot
see the rivals that HOLD a merge apart: `C. S. Hunt` looks like the one Charles Hunt on a
card until you notice the bucket also prints `Cha Hunt`, which is R3 and not a merge. The
resolver defers to `cluster()` for that reason, and the case is a self-test.

### What it costs the town today: nothing

| pass | accepted | newly refused |
|---|---|---|
| documented | 39 | **0** |
| placed | 5 | **0** |
| letter_list | 658 | **0** |

`identity_master_guard.py --report` is the measurement: 1,356 of 6,697 identities stand on
a committed card, 2 stand on more than one, and reading all 1,362 person records back as if
they were being minted today resolves exactly those 4 onto a different card. Both pairs are
`brown_rufus`/`brown_mrs_rufus` and `norton_n_r`/`norton_nelson_r`, deferred to **T-0723**
by name in `data/residents/card_merge_rulings.json`. It is a lock, not a repair.

### The gate

`consolidate_resident_evidence.py --check` now fails when any identity stands on more than
one town card. The only way past is a DEFERRAL in `card_merge_rulings.json` naming the cards,
the ticket that owns them and the reason â€” a deferral without a ticket or without a reason
fails too. Four self-test cases assert it fires. `check.sh` gains the guard's own self-test.

### The gate caught one within the hour, and it is filed rather than decided

Merging `dev` brought T-0724 (#931), which taught the splitter that a compound surname is
one surname â€” and `Bogart, Dr. Henry Van der` and `H. Vanderbogart` fell into one bucket
for the first time, where M2 attached the initial. Two town cards, one identity, and dev's
own `consolidate_town_cards.py --check` was green on it because the cluster carried an
`undecided` row, which is the ticket's whole argument about ruling coverage in one example.

It is **T-0950**, deferred by name in `card_merge_rulings.json`. It is not decided here:
the death notices put the doctor's death at 8 April 1835 and the letter this card was
minted from ran on 20 May 1835 â€” ordinary for an uncalled-for letter, and still something
somebody has to weigh. T-0843 owns the lock on the door, not the adjudication behind it.

### One derived row moved, and it is the right one

`docs/RESEARCH/letter-list-surname-collisions.md` counted `Norton N. R.` as a candidate only
the corrected surname reading refuses. It is now refused under BOTH readings, because the
master resolves those initials onto the committed Nelson R. Norton whichever token the old
rule took for a surname. Collisions **9 â†’ 8**. Nothing was retired to make that happen; the
report says so in its own prose.

## Shipped 2026-09-06 â€” T-0828: a fence run id names the side of the lot, not just the lot

**What shipped.** `tools/generate_lot_line_fences.py` mints `side_<lot>_<e|w|n|s>`
where it minted `side_<lot>`, and the three lot-line fence records rebuilt from it.
Seventeen ids that were each carried twice are now thirty-four ids carried once:

| file | runs | ids carried twice, before | after |
|---|---|---|---|
| `data/enclosures/town_lot_line_pickets.json` | 61 | 4 | 0 |
| `data/enclosures/town_lot_line_rails.json` | 147 | 8 | 0 |
| `data/enclosures/town_lot_line_boards.json` | 83 | 5 | 0 |

**No fence moved.** The diff over the three records is 336 lines, and every one of
them is an `id` or the `note` that now says which side the run is on. Not one
`path_local_enu_m`, `belongs_to`, kind, opening or count changed â€” the collision was
never in the geometry, and the geometry is the same geometry it was.

### Why the id collided, and why both entries were always real

A run was named after the LOT it belongs to, and a lot has two side lines. The two
runs called `side_blk_lake_dearborn_lot1` in the rails file sit at easting 709.8 and
735.7 â€” one lot's width apart, the east and the west line of that lot, each with its
own path. Both are real fence. The name identified the lot and then stopped, which is
under-specification rather than duplication, and it is why the check could not simply
assert there: asserting would have refused correct data.

### The discriminator is the geometry that already told them apart

The side line's midpoint lies to one side of the lot's centre, and the two sides of a
lot lie on opposite sides of it, so the dominant component of that offset â€” east,
west, north or south â€” always separates them. It is measured off the WHOLE committed
line rather than off the piece, so trimming a run around a building that stands on it
cannot rename the side the run is on; and it is measured from the FIRST lot named in
the id, which is the id's own sorted order, so a party line between two lots reads as
the side of the earlier-named one. That is a statement about a real line and not a
tie-break: the east side of lot 1 IS the west side of lot 2, and the id names both.
The note on every side run now says the side in words as well.

### The exception came out of `check_unique_ids.py`, which is the point of it

`EXCEPTIONS` held these three entries and nothing else. It is now empty, and the
check covers `runs[]` like every other keyed list â€” 67 of 68 kinds of list before,
68 of 68 today. The table stays, empty, with the story of the entry that left it:
an exception here is a named, ticketed gap and never a silent skip, and the check
refuses one the day it stops being needed, which is exactly how this one came out â€”
it reported the entries as unnecessary and asked for the deletion.

Three self-test cases had to move with it. They asserted the machinery â€” an
exception honoured, an exception reported when its list comes good, an exception
whose file is simply absent â€” by pinning to the real `town_lot_line_rails.json`
entry, so the day the entry went it took its own proof with it and they failed. They
now install a synthetic exception for their own duration, which keeps the machinery
proven for whoever needs the next one; and a new case asserts the three fence files
are held by the rule like any other list.

### Visible-progress rule

**Not visible**, and it is not pretended to be. Nothing on the walk changed: the
fences stand where they stood, and a run id is not drawn. What changed is that
anything indexing these runs by id â€” a scene compile keying a mesh, an audit joining
a run to its lot, a diff asking whether a run moved â€” can no longer silently keep one
side of a lot and lose the other.

## Shipped 2026-09-06 â€” T-0860: the three kin ties #947 read and the survey could not see

**What shipped.** Kin rows on both people for three ties `dev` did not hold, each
under a written ruling:

| tie | on dev before |
|---|---|
| Mark Beaubien â€” brother of Jean Baptiste | `hh_beaubien_mark` carried **no kin at all** |
| Charles Loomis Harmon â€” son of Elijah Dewey Harmon | `hh_harmon_brothers` carried **no kin at all** |
| Isaac Dewey Harmon â€” son of Elijah Dewey Harmon | same |

**The Miller ruling is untouched.** #947 and #949 disagree on it â€” #949 landed it
at `inferred`, #947 refused it because "Samuel, the landlord" is a surname the
dataset carries five times. The owner's call, in session: land the three, leave
Miller as `dev` has it. That disagreement is not reopened.

### Why the survey could not see them, and it was mechanical

**#947 adds no tools.** It is data-only, so its three findings were readings a
person made rather than anything the survey derives. Two separate gaps:

1. `"Andreas's life of **his brother** Jean Baptiste"` â€” the pattern reads
   `<relation> of <Name>`, and English puts no "of" after "his brother".
2. `"lists his five surviving children: 'Charles Loomis Harmon, Isaac Dewey
   Harmon, â€¦'"` â€” one subject and five others, which no `<relation> <Name>`
   pattern reaches.

### One gap closed by generalising, the other deliberately not

**`PROSE_POSSESSIVE`** reads `his|her <relation> <Name>`, bounded exactly as
`PROSE` is. Measured before switching it on: **10 matches** across the committed
prose, and the existing "must resolve to exactly one town person" step refuses
`his mother Potawatomi` and the rest on its own. **The net is wider; the sieve is
unchanged.**

That exposed a second thing. The documented ellipsis rule â€” a quoted source that
elides the surname is re-read with the SUBJECT'S â€” was implemented as *exactly one
token*, a fair reading of `Samuel` and a wrong one of `Jean Baptiste`. It now
covers a compound forename, and applies **only after the printed name has failed
to resolve on its own**, so a name that stands alone is never rewritten and a
re-read can fail to find somebody but cannot find the wrong somebody.

**The Harmon gap gets no pattern, on purpose** â€” a regex fitted to that sentence
would be fitted to that sentence. `data/residents/kin_readings.json` is an
authored seam: a kinship a person read where no pattern reaches, recorded as a
statement so it becomes a proposal and is ruled like any other. It earns the right
to be **asked** and nothing about the answer.

What stops it being a back door: **every entry names the path its quote stands on,
and `--check` refuses an entry whose quote is not actually there.** Three
self-test cases hold it â€” a quote that is nowhere, a card not in the tree, and the
committed readings really standing on their cards.

### Widening the net surfaced a new question, and it is answered

`"his sons Charles Henry"` became landable. **Refused**, on #947's own reading:
Andreas names the son in full, `hh_beaubien_charles_h` carries initials, and
deciding they are one man is a crosswalk ruling rather than a kinship â€” the
father's own record already says that of the two sons named, one has a household
here.

Rulings **13 â†’ 17** (13 landed, 4 refused). Kin gate green, self-test green,
`validate.py` PASS with 0 errors â€” the reciprocity check reads all four new rows.

## Shipped 2026-09-06 â€” T-0855: the Hubbard fold rests on the man his own transcription names

**What shipped.** `hubbard_g` folds onto `hubbard_henry_g`, not `hubbard_gurdon`.
Its only press evidence is transcribed **`Hubbard, [Henry] G.`** and cites
`person_hubbard_henry_g`; `hh_hubbard_henry_g.json` is a separate **attested** card
in the same tree. T-0839 (#929) had put one man's record on another man.

### It needed a new rule, not a bent one

`C2` â€” an initial onto its one full forename â€” **refuses** a cluster with two rivals,
on principle, and a bare `G.` has two here: Gurdon and Henry G. What settles it is not
a name-matching inference at all: somebody read the page and wrote `[Henry]`.

> **C5 â€” THE TRANSCRIBER NAMED HIM, IN BRACKETS.** A bracketed forename is an
> editorial expansion by whoever transcribed the source. It is evidence about
> IDENTITY where an initial is only evidence about spelling, so it outranks the
> initial and settles a cluster C2 would refuse.

The old ruling's `against` read *"No second Hubbard household is on any card, and no
source reached names one."* Both halves were false. It now says so.

**`chicago_democrat_1833_1835` stays on Gurdon** â€” three of the four cards still
folded onto him cite it too, so it is his by other routes. Only the single wrong
`press_evidence` entry came off, and that was checked before anything was removed.

### Two defects found while fixing it, and both were hiding it

1. **`--apply` could not correct a mis-fold.** Its already-folded branch only *read*
   the stub, so rewriting the ruling and re-running changed nothing â€” the stub and the
   redirect table went on naming Gurdon. It now re-points a corrected fold and records
   `repointed_from`.
2. **`--check` passed the whole time the ruling said Henry and the data said Gurdon.**
   It verified a redirect points at *a* real person, never at the person the **ruling**
   names. Two copies of one fact disagreeing â€” this project's oldest failure shape â€”
   and it made a corrected ruling silently inert.

Both are asserted now, and both were proved to fire by putting the redirect back and
watching them catch it.

### The gate the ticket asked for

`bracket_conflict()`, pure and self-tested: a folded card whose reading brackets a
forename absent from its survivor is refused. Five cases, including **the false
positive it would otherwise have shipped** â€” a bracketed RANK (`Allen, [Lieut] James`)
is not a forename and must not trip it.

Measured over all 42 folded records: **one** tripped it, this one. The other 41 stand,
so #929's consolidation is sound and this was an isolated ruling error.

### Where it came from

Draining the open-PR backlog. **#932** was the losing rival to #929 and superseded on
coverage (36 clusters ruled against 31, 42 folds against 34) â€” but it was **right about
this card**, and closing it on the numbers would have buried the finding. Reading a
losing rival before closing it is what turned this up.

### Visible-progress rule

**Visible**, and it settles the commitment made two entries ago: a man's card now
carries the reading that names him, and another man's stops carrying a record that was
never his.

## Shipped 2026-09-05 â€” T-0817: the owner's queue ranking stops going backwards

**What shipped.** Two halves, because the fault has two.

1. **`tools/merge-queue.mjs` â€” the band-stripping bug.** A new ticket is now placed
   where its own side placed it, carrying the comment band that introduced it,
   instead of being dumped at the end under "MERGED IN, NOT YET PLACED". And a band
   that genuinely cannot be anchored now **refuses the merge and names the line**
   rather than dropping it.
2. **`tools/check_queue_order.mjs` â€” a gate, wired into `check.sh`.** Every re-rank
   the base records must still be present on the branch.

### Why the driver alone was never going to be enough

T-0817 found the thing that matters and it is worth quoting: *"It never reaches a
squash-merge on GitHub, because GitHub does not run this repository's merge
drivers. So the driver protects branch merges and cannot protect the thing that
actually lands."*

That is exactly what happened with **PR #801** â€” the driver **refused**, correctly,
and the ranking was lost anyway, because the refusal lives on a developer's machine
and the merge happened on the server. `check.sh` is the required `gate` on dev's
ruleset, so a gate refuses the merge **button**, which is the only door the
regression actually comes through.

### The driver's bug was not where the ordering rule is

The ordering rule ("the side that actually re-ordered wins") is sound. The bug was
below it: only the **ordering side's** text is walked, so any band the *other* side
wrote was discarded outright â€” and because `seq()` compares only ids present in all
three versions, six brand-new tickets under a new band do not register as a re-order
at all. `theirsReordered` stays false, ours becomes the ordering side, and the
owner's ranking is dropped without the "both sides re-ranked" refusal ever being
reached. #909 measured the result: *"stripped THREE times â€¦ six tickets the owner put
at the top came to be sitting at line 416."*

### What the gate asserts, and what it deliberately does not

**Set inclusion of the RE-RANK LEDGER's entries, not a date comparison.** Two
re-ranks happened on 2026-09-05 alone, so "is our newest date â‰¥ theirs" would have
passed a branch that dropped one of them. It never judges whether an order is good â€”
only whether a decision the base already recorded has gone missing, which is
decidable without reading a single ranking.

It **skips rather than fails** when there is no base to read (no `origin/dev`, a
detached checkout, an offline runner). A gate that fails for want of a network is a
gate people learn to bypass.

### Tested against the real regression, not a fixture

The real `tickets/QUEUE.md` with yesterday's two re-ranks removed is **refused**, and
both are named in the owner's own words. 37 assertions on the driver (11 new, on the
band-stripping case and its refusal) and 13 on the gate â€” including the #801 scenario
end to end in a real git repo, and the same-day case a date check would wave through.

### Visible-progress rule

The previous entry committed that the next run must be visible, and this one is not.
**Exemption 1 â€” an owner-reported bug â€” which AGENTS.md says "always outranks this
rule".** The owner asked for this fix directly, after that commitment was made. The
commitment carries to the run after this one.

## Shipped 2026-09-05 â€” T-0431: blk_south_water_clark's second deal, on the drug store's party wall

**What shipped.** Two roofs on `blk_south_water_clark`, the third of the four South Water
blocks T-0009's ruling unblocked (T-0420 piece 3 of 4):

- `recon_1835_blk_south_water_clark_c2_06` â€” a **C2 store-residence**, 5.751 m Ã— 10.760 m,
  1.5 levels, standing ON the committed South Water block face at the plat module's 1.5 m
  margin, its **east wall the west wall of `pruyne_kimball_drugstore`** on a shared party
  line. First time this project has stood an invented roof shoulder to shoulder with a
  *documented* one.
- `recon_1835_blk_south_water_clark_a3_07` â€” the A3 privy in the same lot's yard, at the
  alley end.

Lot 1, the Lake-and-Clark corner, stays open. The block moves `open` â†’ **`at_capacity`**,
free lots 2 â†’ 1, headroom 4 â†’ 0, standing roofs 10 â†’ 12.

**The face is this block's own record, not the town's.** South Water carries four documented
records on this block (Harmon & Loomis, Pruyne & Kimball, Bates's auction room, Madore
Beaubien) against Lake's one, and three of the four are commercial; T-0024's second clause
then puts a commercial roof ON the street line. The town-wide count does not decide it and
the recipe says so.

**The end rule is read, not asserted.** `measure_end_rule.py blk_south_water_clark --list`
puts lot 2 at **84.44 m walked** from the Dearborn drawbridge against lot 1's **231.87 m**.
This face grades only on the walked criterion (6.07 m unit step); the straight line reads
4.81 m and is BELOW THE FLOOR â€” the same shape T-0317 found on `blk_randolph_market`.

### The finding: two sizings of the same ground, in different units

`reconcile_665.py` sizes principal room as `ROW_UNITS_PER_LOT * (free_lots - 1)` â€” party-line
units of 6.072 m counted against LOTS â€” and dealt this block 3 principal roofs.
`generate_block_infill.py`'s T-0105 ceiling is one principal roof per lot, and a frontage run
may carry no more roofs than the lots it was dealt; this run was dealt one lot, so one is the
ceiling. **It is not the metres that refuse the other two here.** Measured on the committed
face: lot 2 projects 24.643â€“49.751 m, 22.108 m buildable after the 1.5 m side margins; the
drug store holds 39.108â€“46.825 m; 12.965 m clear west and 1.426 m east; the store takes
33.356â€“39.107 m and leaves **7.213 m still clear**, which is width enough for a D3 at its
4.88 m band minimum. The two dealt cottages (D3, D4) are therefore NOT deferred â€” this
generator's deferral list is for families it refuses by name â€” so the recipe claims 2 of the
4 in its own `drawn_from_schedule` numbers and the other two return to the south district's
balance. Filed as the successor ticket T-0431 owes under T-0028's programme rule.

### The correction that made the ground reachable

The first deal (2026-08-15) was declared on frontage lots `[2, 4]` and stands **entirely on
lot 4** (60.439â€“72.893 m along the face, where lot 4 runs 49.286â€“74.393 m): it packs west
from the east end and ran out of roofs 10.7 m short of lot 2. Lot 2 stayed declared as its
ground, and the two halves of the programme then read it two ways â€” `reconcile_665.py`
counted it FREE, `generate_block_infill.py`'s T-0105 lot accounting counted it built on and
refused it to any later deal. Narrowing the declaration to `[4]` moves no coordinate (the
east anchor reads `along_max`, which lot 4 sets either way) and both units re-derive
byte-identical. The amendment is written into that entry's own `runs` field.

### Side effect worth having

`adopt_street_faces.py` seats one more documented trader on the street: **J. Curtiss,
attorney and counsellor at law** â€” 38 adoptions â†’ 39, refusals 22 â†’ 21.

### Also here

- Baked: `c2_06`, `a3_07`, and `d5_01` â€” whose siding stock was re-dealt (6 in â†’ 4.5 in) by
  the new neighbours within 60 m, which `validate.py --stale` caught.
- Re-derived: the 665 programme, `town_census.json`, `street_face_adoptions.json`,
  `register_1835.json`, `land_sales/ground.json`, all sidecars, and the publish mirror.

## Shipped 2026-09-05 â€” T-0832 (of T-0813): the five files that conflict on every merge stop conflicting

**What shipped.** Two merge drivers and the `.gitattributes` to reach them:
`tools/merge-generated.mjs` (the five build products â€” keep ours, print the
rebuild command, never conflict) and `tools/merge-smoke-state.mjs` (the smoke
ledger â€” union of whole readings, never of lines). Registered by
`setup-merge-drivers.sh` beside the existing two; twenty assertions in
`tools/merge-generated-selftest.mjs`, wired into `check.sh`.

### The measurement, which is a log rather than an argument

PR #906 was open about seventy minutes. `dev` moved **five times** under it â€”
#904, #907, #908, #905, #858 â€” and every one of the five merges conflicted,
**always in generated files and never once in the substantive diff**:

| lap | dev landed | conflicted |
|---|---|---|
| 1 | #904 | BOARD.md, tickets.json Ã—2, build.json, walk/index.html |
| 2 | #907 | the same five, plus STATUS.md (a real conflict, hand-merged) |
| 3 | â€” | the same five, measured with `merge-tree` before the lap |
| 4 | #905 | the same five |
| 5 | #858 | BOARD.md, tickets.json Ã—2 |

`check.sh`, `QUEUE.md`, `changelog.js` and every ticket source auto-merged every
time, because those carry a driver or are hand-authored. Two other PRs report it
independently: **#894** â€” *"each one collides on the same four generated files"*,
four rebases paid and the fifth is where that run's clock ran out; **#850** â€”
*"Every conflict so far has been in a generated fileâ€¦ The substantive diff has
merged cleanly every time"*, rebased twice, the gate run three times on three
bases, then parked. #850 prices a lap at ~19 minutes of honest verification,
during which dev took three more merges.

### Why keeping ours is safe on those five, and only those

Each is **already refused by the gate when stale** â€” read out of `check.sh`, not
assumed: BOARD.md and tickets.json by `ticket.mjs check`; the site tickets.json by
`test_ticket_mirror.mjs`, which asserts a mirror somebody else made stale still
fails; build.json and walk/index.html by `check_published.mjs`. **So the conflict
was never what protected these files â€” the gate was, and the conflict was pure
cost.** That is the same reasoning `chicago/4d/.gitattributes` already sets out
for the liberty register.

### The file that looks like one of them and is not

`tools/dev-smoke-state.json` sits in exactly the same conflict set. Measured
before writing any rule: it is an **append-only** register of smoke readings
(T-0216), 62 of them; its rows carry **no `id`**, so T-0820's uniqueness check
cannot see it; and **no step of `check.sh` reads it at all**. Nothing regenerates
it and nothing would notice a merge throwing half of it away. #905 resolved one
lap by taking dev's side and said so â€” right for one lap, wrong as a standing
rule, because a reading is evidence that a gate was run on a tree, and evidence
is not regenerable.

**Treating all six alike would have destroyed data silently.** The ledger gets a
union of whole readings instead, deduplicated on a canonical form that sorts keys
at every depth â€” not `JSON.stringify(r, keys.sort())`, whose replacer array is
applied at every level and would flatten two readings that differ only inside a
nested object, dropping one. In a driver whose single promise is that no reading
is ever lost, that was the bug that mattered, and it is its own test case.

### The last test is a real merge, on purpose

Nineteen cases test the scripts. The twentieth builds a git repo, writes the
`.gitattributes`, registers the drivers and performs an actual conflicting merge.
`.gitattributes` naming a driver, the driver being registered, and git reaching it
are three separate things, and only the third is what a branch experiences â€” **a
driver that works perfectly and is never invoked looks exactly like no driver at
all**, which is the state this repo was in for all five laps of #906.

### Visible-progress rule â€” stated against me, not around me

**This is the second consecutive invisible run I have shipped**, after T-0820, and
the four-entry window already carries two or three invisible entries. The hard
trigger in AGENTS.md (three consecutive entries opening "Nothing you can see") is
not met â€” v596 does not â€” but the one-in-four ratio is stretched and pretending
otherwise would be the gaming the rule warns about.

What justifies it is exemption 3's substance rather than its letter: it is not a
gate, it is the thing parking gates' worth of finished work. The parcels are
nameable, which the exemption requires â€” **#850** (T-0559, two readings settled
against the sheets), **#856** (T-0497, the Dalton index), **#841** (T-0581, Moses
and Kirkland vol. 1) are all sitting with green work behind this exact conflict,
and #894 ran out of clock on it outright.

**The next run must be visible, and this entry is the commitment.**

### A correction, because it was my own duplicate

This work was first filed as **T-0831** and it should not have been: **T-0813**
already asked for exactly it, on the owner's request, and was ranked at the top of
the drain band. T-0813's measurement is also better than the one above â€” it counted
**21 of 21 open PRs** conflicting on the same six files, and observed that the two
files which already had drivers conflicted on **0 of 21** and **3 of 21**
respectively. That is the real evidence; my five laps are a second sample of it.

T-0813 is now split â€” **T-0832** (this, the merge treatment) and **T-0833**
(`tools/drain.mjs`, its untouched second half) â€” and the children hold its queue
place. T-0831 is withdrawn.

**Two deliberate deviations from what T-0813 specified**, recorded in T-0832 rather
than left to be found:

1. It asked for a driver that *re-runs the tool that owns the file*. A merge driver
   runs during the merge on a HALF-MERGED tree, once per conflicting file, and the
   owning tools here are `ticket.mjs board` and `publish.sh` â€” the second reads the
   whole tree and takes a minute or two. Regenerating from a state that never
   existed is worse than keeping a stale copy. So it keeps ours and PRINTS the
   command, and the gate's existing staleness checks are what make that safe.
2. It asked to union the ledger *by (tree hash, viewport, stage), newest wins on a
   tie*. Newest-wins **discards a reading**, and two runs of one stage on one tree
   are not redundant â€” they are the evidence it was run twice. This unions on full
   identity and drops nothing; pruning, if ever wanted, is a deliberate pass and not
   a merge driver's silent side effect.

## Shipped 2026-09-05 â€” T-0820: an id used twice is refused on the branch, not on dev

**What shipped.** `tools/check_unique_ids.py`, wired into `tools/check.sh` beside the
conflict-marker check it is a sibling of. It walks every committed JSON under `data/`,
`tools/` and `tickets/` â€” 2,835 files, 0.6 s â€” and refuses any list of objects that
carries the same `id` twice, naming the file, the key, the id, and whether the two
bodies are identical (a merge that kept both) or different (an id that names two
things). Fourteen self-test cases prove it fires.

**Why it is on the branch's gate and not a nightly.** `dev` went red twice on
2026-09-05 on this exact fault â€” T-0739 minted by two branches (#863), then a second
byte-identical `west_water` in `data/streets/1835.json` from a branch cut before the
first landed (#889) â€” and a third came that evening from an agent staging a `UU`
conflict with `git add -A`. None was caught on the branch that wrote it. All three were
caught by `check.sh` against `dev` AFTER the merge, which is the expensive place: the
dev gate is the base every open PR inherits, so one duplicate parked nineteen PRs
behind a red they had not caused. `dev` now carries a ruleset requiring `gate`, so a
red dev no longer discourages merging â€” it forbids it.

### The rule is discovered, not listed

A hand-maintained table of "lists to check" goes stale the first time somebody adds a
list, and the list they add is the one that breaks. So the check applies wherever the
SHAPE appears: a dict value that is a list of two or more objects, every one carrying
an `id`. Measured over the tree before it was switched on: **68 kinds of list, 67
already clean.** The rule is what the data already obeyed, written down.

### What it found, and the cause was not the one expected

One real fault: `fulton` in `data/streets/1835.json` cited `thompson_plat_1830`
**twice**. It is not a merge artefact. `abacee6e4` â€” the T-0713 sweep that attested the
platted streets â€” appended the plat to every street's `sources`, and Fulton's list
already contained it. T-0713's own STATUS entry above says so in as many words: "and
`fulton`, which already cited the plat". The sweep knew and appended anyway. Fixed
here, one element removed; every other street in the file cites the plat once.

That matters beyond the one line: **the fault the check was built for arrived by a
route nobody predicted.** Three duplicates from merges, and the fourth from a
single-branch sweep that read the value and added it again. A check written to catch
merges would have missed it; a check written against the shape caught it.

### The one exception, named rather than skipped â€” T-0828, and since closed

`runs[]` in the three `data/enclosures/town_lot_line_*.json` files repeated ids, and
those were NOT duplicates. Two runs called `side_blk_lake_dearborn_lot1` sat at easting
709.8 and 735.7 â€” one lot's width apart, the east and the west line of that lot. Both
are real fence; the generator named a run after the LOT and a lot has two sides, so the
id under-specified. Asserting there would have refused correct data. **T-0828 fixed the
generator** (see the entry at the head of this file, 2026-09-06): the id now names the
side, all three files rebuilt clean, and `EXCEPTIONS` is empty. The check refuses an
exception the day it stops being needed, so it cannot outlive its ticket â€” and that is
how this one came out, on its own report rather than because somebody remembered.

### Not covered, and measured rather than assumed â€” T-0829

T-0820's acceptance also named `data/research/*/coverage.json` â†’
`declarations[].items[]`. It is **not** covered: those are lists of strings and the
declarations carry no `id`. All ten files are clean today, but nothing holds them.
The obvious extension was measured and refused: 222 kinds of string list, 28,331 lists,
14 with a repeat â€” and most of those repeats are **correct**, because the lists are
multisets (`by_ward` has one entry per person, and two people share a ward). A blanket
rule would refuse honest data, the same mistake `raised[]` forced this check to avoid.
Three `mentions` lists in `gazetteer.json` are genuinely suspect and are written up in
T-0829 for adjudication against the clippings, not silently deduplicated â€” the same
clipping id twice is either a double count or a clipping-level id doing a
mention-level job, and which one it is decides whether the fix is a deletion or a
rename.

### Visible-progress rule

This is an invisible run under **exemption 3** â€” a gate blocking visible parcels. It is
not speculative: with `dev`'s ruleset active, the next duplicate id stops every merge
on the lane, and the parcels it stopped on 2026-09-05 were the nineteen PRs held behind
#889. The last three merged entries (v588â€“v590) are all visible, so the one-in-four cap
is not in play.

## Shipped 2026-09-05 â€” T-0823, T-0824: a speed slider per pace, and a framed arrival

The owner, in session: three speed sliders "like you have for walk speed", ceilings "like
walk at 20 mph and horse gallop at some high number like 60 mph", gait names as the slider
moves; and "for any travel, when you land it should be a nice complete view of the structure
â€¦ center the structure entirely in frame" with the card open.

**Sliders.** The walking slider moved from Settings to Travel (ids kept) and gained two
siblings: walk 0.5â€“8.94 m/s, wagon 0.5â€“13.41, horse 0.5â€“26.82, each stored under its own key
(`speed`, `wagonSpeed`, `horseSpeed`) and composed into `WALK` by `travel.applyPace()`; Shift
multiplies by 2.28 / 1 / 1.7, capped at the ceiling. `GAITS` in travel.js names the speed
("trot Â· 8.1 mph"); the top names â€” "faster than any man", "runaway", "beyond any horse" â€”
say what the ceilings are. Interface, not claims about 1835; no LIBERTIES entry.

**Framing.** `main.js framing(id)`: the front bearing from the router (nearest street track,
else south-west), the distance that fits the footprint's half-diagonal across the 76Â°
horizontal field of view and the height (wall Ã— 1.55) within the live vertical one, aimed at
the building's middle, clamped 10â€“90 m. `frame()`, the ride's destination and the flight's
landing all take it, so the three arrivals cannot disagree.

**Smoke restated, not weakened:** the pace assertion compares WALK to each pace's stored
slider value instead of to the old constants; the three arrival distances (`<= 14 m`,
`<= 40 m`) became "within 2.5 m of the framing distance for that building AND its four
extreme ground points and ridge inside the frame" â€” a stronger claim than the fixed radius.
Unverified until the gate runs.

## Shipped 2026-09-05 â€” T-0713: the platted streets are attested, and the line grades the ribbon

**What shipped.** Seventeen streets in `data/streets/1835.json` move from
`geometry_confidence: inferred` to `attested` and each now cites
`thompson_plat_1830`: the sixteen the owner named â€” `south_water`, `lake`, `randolph`,
`washington`, `market`, `franklin`, `wells`, `lasalle`, `clark`, `dearborn`, `state`,
`canal`, `clinton`, `kinzie`, `wolcott`, `michigan_north` â€” and `fulton`, which already
cited the plat and is the best-held line in the file at RMS 0.35 m across four surviving
intersections. `surface_confidence` and `wear_confidence` are untouched everywhere: the
plat attests where a street ran, and carries nothing about what it was paved with or how
it was worn. `north_water`, `fort_road` and `fort_bank_track` stay `reconstructed` â€” a
line derived from the committed bank and two fort tracks the plat does not draw â€” and
`carroll` stays `inferred`, because it is the one West Division tier that does not survive
inside the plat and its line is interpolated between Kinzie and Fulton.

### The distinction each upgraded note now states

The 17.5 m RMS in `data/datum.json` `derivation.residual_m` is COORDINATE UNCERTAINTY â€”
how well the 1834 sheet warped onto modern ground â€” and it bounds how precisely a line is
PLACED, not whether the street was there. Confusing the two is what held these sixteen at
`inferred`: a metric bracket on a position was being read as a doubt about existence. Every
upgraded note says so in its own words, and each was re-read for
`tools/audit_confidence.py`'s SILENCE vocabulary. One hit, in `fulton`: "no source gives
Fulton a crossing" is a sentence about a BRIDGE and not about the line, and it is reworded
so an attested field is not hedged in its own note.

### The composition decision, which is what makes it visible

`streets.js` graded a ribbon by `Math.max()` of geometry, surface and wear (T-0100), and
every record in the file carries `wear_confidence: reconstructed` â€” so upgrading the lines
alone would have moved no pixel and the whole platted town would have gone on dithering as
invention. T-0713 splits the one grade into the two claims it had flattened:

- **the LINE decides whether the ribbon STANDS** â€” presence, dither, and which level hides
  it. That is the claim "a street ran here", and it is the only one of the three the
  visitor's own footing depends on. It is carried on `_confidence`, the contract's channel,
  and it is the channel the confidence view reads.
- **SURFACE and WEAR decide only the TRACK painted on it.** They are carried on a second
  attribute, `_trackConfidence`, read nowhere but the street material's own fragment block,
  which fades the worn texture toward the bare corridor in proportion to how invented it is
  â€” and only while the confidence view is on (`vTrackConfidence * uConfMode`), so the
  ordinary daylight frame is the frame that shipped before this.

T-0100's guard is kept rather than traded away, and `tools/test_street_confidence.mjs` is
restated to prove it: an invented line under an attested surface still dithers out, and a
record with no geometry grade still falls to `reconstructed` rather than reading as
attested. What the split adds is the converse the `max()` could not express â€” an attested
line under an invented wear no longer dithers away, because "we do not know how worn it was"
is not a reason to tell a visitor the street was not there. The test now extracts BOTH
expressions from the source and refuses to pass if the ribbon's one reads `surface_` or
`wear_confidence` again, if the track's one has dropped either of them, or if
`_trackConfidence` reaches the shader and is never spent.

**Measured on the shipped index:** 21 street records â€” 17 ribbons attested, 1 inferred
(`carroll`), 3 reconstructed. Hiding `inferred` drops Carroll and leaves the platted town
standing; hiding `reconstructed` drops the two fort tracks and the north bank line.

### Not decided here

`INVENTED_TRACK_ALPHA` is 0.45, chosen to sit clear of the 0.34 the confidence view already
uses to dither invented massing â€” a track we made up should read fainter than one we did
not, and still plainly fainter than the road it is painted on is solid. It is a legibility
constant and no measurement fixed it; if the fade reads wrong against the amber tint at a
distance, that number is the thing to move, not the split.

### Carried, not caused

`python3 tools/compile_scene.py --all` was run and five sidecars â€”
`clybourn_slaughterhouse`, `elston_soap_candle_manufactory`, `green_tree_tavern`,
`pruyne_kimball_drugstore` and `residents_sources.json` â€” recompiled with land-sale evidence
that had landed on `dev` without a recompile. That drift was on `dev` before this branch
existed (verified against a clean tree) and `check.sh` fails on it either way, so the
recompile is carried here rather than left for the next run to trip over.

## Shipped 2026-09-05 â€” T-0637: 302 runs of fence stop belonging to nobody

**What shipped.** `tools/enclosure_owners.py`, a derivation, and the two generators that now
call it. Every run on the enclosure layer carries a `belongs_to` naming the lot it bounds, the
committed buildings standing on that lot, and the households `data/residents/index.json` puts
in those buildings â€” `lives_at` as a home, `works_at` as a workplace, which is this dataset's
join to a business because a business here IS a structure with a trade on its `function`.
Where one line divides two lots it belongs to both and each entry gives the compass bearing
from the run's midpoint to that owner's ground, so the side is a measurement off the committed
plat rather than a word. `data/enclosures/town_lot_line_{boards,pickets,rails}.json` and
`town_dooryard_pickets.json` are regenerated; a new record-level `belongs_to_rule` block on
each states the rule, its sources and its counts.

**The numbers, on 306 runs.** 51 joined to a household; 24 households now have a fence round
their ground; 117 lots named. The other 251 name the structures whose ground they bound and
carry `refused: no_household_names_this_ground`, with the reason stated once per record: 20 of
this town's 1,380 households hold a real `lives_at` and 50 a real `works_at`, all at named
landmarks. **That is a gap in the address work (T-0514), not in the join** â€” a re-generation
picks up whatever the placement sweep lands without a line of the rule changing.

**What was refused.** A structure's `occupants` block is prose, and 72 of the buildings this
layer fences name a household id in it â€” 59 ids, of which **53 belong to households the
2026-09-02 synthesis removed** and the index no longer holds (T-0516's finding, counted here).
Worse, a mention is not an occupancy: `philo_carpenter_log_shop` names `hh_chappel_eliza_mir`
in a sentence whose own `value` says no occupant is attested there at the scene date. Joining
on that prose would have handed ground to the wrong household while looking like evidence, so
the count is filed as a finding in each record and the join stays on the two committed links.
It is also why the dooryard record joins **1 of its 13** plots: clause 4 of that generator's
own rule admits a lot on the strength of the same prose, and only Elijah Harmon's household is
on a lot this record reaches with a real address behind it.

**Nothing hand-authored was overwritten.** `tools/check_enclosure_owners.py` (new, wired into
`tools/check.sh`) re-derives the authored yards anyway and prints the comparison: it agrees
`sauganash_yard` is the Sauganash's and reports that `philo_carpenter_log_shop` stands on the
same lot â€” a second building on the ground, not a second owner of the yard. The Western's
wagon yard and the estray pen stand on ground the plat never divided into lots, so the
derivation has nothing to compare and says so. The gate also fails a run that names an owner
this repository does not hold, and a generated run with no `belongs_to` and no refusal.

**Nothing in the scene moved.** No coordinate, no fence, no bake: this ticket adds a relation.

## Shipped 2026-09-04 â€” T-0701â€¦T-0712: the drawer, Go to, Travel, People, the Evidence hub, the card

**Every screen a visitor sees changed; the PR names the twelve tickets.** The owner's asks:
the menu "is so small" (a sixth tab did not fit); Go to with "reconstructed roofs hidden by
default" and "filters like taverns, shops, etc."; travel "instantly, by walking, by wagon
(fast), by horse (faster)", "go as fast as a horse through the city", "maybe a gallop
up-and-down view", "open the card on landing" or "fly â€¦ and open the card"; the card should
not lead with "what we made up"; "the citizens should show there"; Evidence "is entirely
unwieldy". Ruled in session: one PR into `dev`; menu and card **share one right-hand slot**;
the card's top half uses **quiet coloured grade dots**.

### Decisions
- **One slot**: opening the drawer tucks the card (`#popup[data-tucked]`, never `hidden`);
  closing untucks; a Go-to arrival closes the drawer and opens the card.
- **Hidden roofs** follow the presence grade, `documented_range.confidence ||
  placement.position_confidence || 'reconstructed'` â€” 276 of 358 hidden until the toggle.
  Privies, stables and sheds file under Homes & yards.
- **Default travel mode `instantly`**, so first-run behaviour and every arrival assertion stand.
- **Router**: grid A* on 2 m cells, streets cheap, footprints and undecked water blocked; a
  null route falls back to instant travel and says so.
- **Paces are interface choices, not claims about 1835** â€” 3.6 m/s says nothing about any
  1835 wagon â€” so **no LIBERTIES entry**; the Travel note says so instead.
- **`people.json`** is a compiled sidecar (`compile_people()`, drift-checked under `--check`);
  `residents.js` still reads the manifest and household files.

### Smoke restatements â€” restated, never weakened (unverified until the gate runs)
- Tab order â†’ exactly `goto,travel,people,evidence,settings,controls,whatsnew` (same exactness).
- "Five tabs fit one row" â†’ every rail item unsqueezed, one column desktop / one row mobile (same fit test).
- "Every loaded structure" â†’ default `=== count(presenceGrade â‰  reconstructed)`, toggle `=== registry.size` (full count kept, behind the owner's toggle).
- Position grade per row â†’ chip `=== presenceGrade` and `data-jump-position ===` position grade (both grades read).
- Chip colours distinct and `â‰  .jump-name` â†’ same, reconstructed read after the toggle.
- `.jump-result span` â†’ `.jump-result .jump-name` (the same element, by its own class).
- Intersection arrival â†’ precondition `api.setTravelMode('instantly')` stated (the default it already relied on).
- `checkVisibility` in card panes â†’ activate the pane's `[data-pop-tab]` first (a collapsed read passing would be dishonest).
- `.pop-account` â†’ `#popup .pop-lead.pop-account`, plus a composed lead without `change_note` (stricter).
- `.pop-meta [data-note]` â†’ `#popup .pop-where [data-note]`; chip coverage adds `.fact-dot â‰¥ 3`, `.pop-facts .conf === 0` (additions).
- Card not collateral when the panel opens â†’ unchanged; tucking keeps `hidden` off `#popup`.

**Verified 2026-09-05 on the integrated tree** (`tools/check.sh` CHECK PASS; smoke to files,
zero page errors in every leg): desktop parts 12, 3 and 13 and mobile 10-13 and 3-6 all
pass â€” 66, 80, 110, 203 and 123 checks. The mobile 3-6 leg found one real defect on the way
and it is fixed in the same PR: the new pace chip had pushed the confidence chip group to the
left of a 390 px top bar, and its 280 px level menu, hung off the group's right edge, opened
70 px past the screen; on a phone the menu now anchors to the viewport's own edges. One plan
clause was corrected rather than the code: the Go to list starts with no row active, as a
combobox does, so two ArrowDowns reach the SECOND row, and the gate asserts that.

New assertions live in T-0701â€¦T-0712's acceptance clauses. T-0713 (street lines attested from
the Thompson plat) is written for the loop and stays in the queue.

## Shipped 2026-09-04 â€” T-0542: the third town election was Friday 10 July 1835, and the 85-name poll list is not its poll book

**Nothing a visitor can see changed, and this is the exemption named in the PR: the finding
was blocking T-0514, T-0515 and T-0634, all three of which mint or regrade people whose cards
a visitor opens.** T-0493 read the four voter lists of 1833-1835 and was asked to date the
1835 poll. It could not: the list prints no date, and Andreas dates the third town election
twice, two hundred pages apart and not in agreement â€” *"The third election was held in July,
1835"* in the town chapter, *"the third election of town oHicers, which occurred .Au- gust 5,
1S35"* in the police chapter. The scene date is 1835-07-01, so eighty-five men's presence at
the moment this town is drawn rested on which reading was right.

### The town's own paper answers it, in two issues a week apart

Nobody had asked the *Chicago Democrat*. It is in the deposit, seventy-three issues of it,
and it settles the question three times over â€” `data/research/civic/claims/town_election_1835_democrat.json`:

| issue | what it says | id |
|---|---|---|
| 10 Jun 1835 | the election is ordered by a new act, no copy of the act can be had in Chicago, and the poll is *"postponed, or adjourned, some how or other, from time to time"* | d001 |
| 8 Jul 1835 | *"the election of Trustees under a new Charter takes place Friday of this week"* â€” a Wednesday paper, so **Friday 10 July 1835** | d002 |
| 15 Jul 1835 | *"Chicago Charter Election.â€”This election took place on Friday last"*, with the return | d003 |
| 15 Jul 1835 | the charter itself, Sec. 4: the annual town election moves to **the first Monday in June** | d005 |
| 26 Aug 1835 | the new board's ordinance code, *"Passed the [5]th day of August, 183[5]. H. HUGUNIN, Pres't"* | d004 |

The identification rests on the names, not on the dates alone: the men the return puts on the
two tickets are Andreas's eight â€” Hugunin, Loyd, Jackson, King, Kimball, Williams, Sherman,
Dole â€” which is what makes his passage and this return one event. **The third town election
was Friday 10 July 1835, nine days AFTER the scene date.** Andreas's town chapter is right;
his police chapter's 5 August 1835 is the day the elected board sat and passed its code. On
either reading of that sentence â€” a conflation, or "election of town officers" meaning the
board choosing the officers the charter gives it â€” the popular poll does not move off 10 July.
d005 also kills the circumstantial argument that had been carried for the August reading: the
1833 and 1834 polls fell in the second week of August under a law that the 1835 act superseded.

### And the answer to the question asked was "neither"

The 85-name list is **not the poll book of that election** (`town_findings_voter_lists.json`
v003). Kimball and Dole polled 142 votes each and Hugunin 124; eighty-five men cannot cast a
hundred and twenty-four votes for one candidate. That alone leaves *different poll* or *short
printing*, and the membership decides between them: six of the ten men who stood â€” Kimball,
Loyd, Jackson, Dole, Kinzie, Davis â€” are absent, while the list runs unbroken from Adams to
Wright, so no lost page or dropped column accounts for them. **Which poll it is stays open.**
The nearest candidate is the county and state general election of Monday 3 August 1835, at
which Cook County chose a Recorder and at which Peter Pruyne, who stands on this list, was the
caucus candidate; that is named as a candidate and asserted as nothing. What it means for the
work downstream is that a name on this list evidences presence in Chicago in 1835 and **not**
presence on any stated day â€” a sharper constraint than T-0514 and T-0515 were given, not a
looser one.

### What was NOT settled, and what was read to fail to settle it

The 1833 discrepancy stands (v004). Andreas says twenty-eight men voted on 10 August 1833;
the list prints thirty. **No count outside Andreas exists in anything this project holds**:
the *Democrat*'s first number is 26 November 1833, so the poll has no contemporary report, and
its whole run to August 1835 carries no retrospective one; the board's own ordinances printed
31 December 1833 name no judges or clerks of that election. The nearest thing in the corpus is
a notice in the paper's first issue, over the name of a Judge of Election, for the choice of
one Constable for the Chicago **Magistrates District** â€” a district office, not a town one,
and it is recorded because it is near, not because it bears. The one thing sayable without a
new source is source criticism and is offered as that: Andreas's sentence is prefaced *"It is
believed"*, it counts the town's legal voters rather than the enrolments in a poll book, and
it was written in 1884. The judges-and-clerks hypothesis is the weaker of the two the ticket
offered â€” judges and clerks of an Illinois poll were themselves electors and voted, so their
names belong in a poll book. Neither count is repaired.

### Reading is only half of it, and the meter said so

Seven new units read is seven more units the civic domain had read and not ruled on, and
`measure_research_spend.py --gate` failed on exactly that: 20 unspent against a ceiling of 13.
**The ceiling was not raised.** The rulings were written instead, one per unit, each naming
its unit by id â€” `data/research/civic/town_election_1835_crosswalk.json` â€” and every one of
them is a refusal to carry, because T-0542 was forbidden to mint or regrade and says so. civic
is back to 13 unspent, 499 read against 486 ruled on. **Nobody was added to the town, nobody
was removed, and no grade moved.**


## Shipped 2026-09-03 â€” T-0423: the corpus's one lot-and-block address is seated, and stops carding as vacant

**The dwelling-house on lot 7 of block 16 is named on the card a visitor opens, instead of
"A vacant one-room frame cottage".** G. Spring's For-Sale notice ran in the *Chicago
Democrat* six times between 1834-06-18 and 1834-11-19 â€” *"LOT No. 7, in block No. 16, one
lot east of Haddock's Tavern, on Lake street â€¦ There is on said lot a large Dwelling-House
and fine well"* â€” and a lot and a block is the plat's own language, which makes it the most
precise placement statement in the whole newspaper corpus. **This is the visible half of
T-0358**, which committed the Thompson block numbering so the sentence could reach ground.
It reached a polygon and stopped: the roof standing on that polygon went on titling itself
with a claim of absence made over the top of a source saying a house was there.

### The third grammar, and it needed its own policy

A paper of 1834 places a building three ways, and they are three different claims:

| the paper says | it constrains | the policy |
|---|---|---|
| a platted street and nothing narrower | a face | `docs/STREET-FACE-ADOPTION.md`, L212 |
| a count of doors off a named corner | a position, and no lot | `docs/CORNER-ORDINAL.md`, L215 |
| **a lot and a block** | **the plat's own unit** | **`docs/LOT-ADDRESS.md`, L216** |

`data/research/newspapers/lot_addresses.json` authors the address and nothing else â€” the
printed words, the printings, what the notice says stood on the lot, and who the advertiser
was. Every step from there is derived by `tools/lot_addresses.py`: block number â†’ block
through the committed numbering (which the ledger may not contradict), lot number â†’ polygon
through the committed lot grid, polygon â†’ **exactly one** roof by footprint centroid, or the
address is refused. Both directions are gated in `check.sh`, and nine ways the seating could
lie are in its `--self-test`.

### The grade does not move, and the chain is why

The words are read. The block number is `inferred` â€” and since 2026-09-06 (T-0788) it is a
numeral READ on block 16's own ground rather than three blocks counted east of another one.
The lot number is still `conjectural` twice over: four lots to a face is now a reading of
four blocks rather than one, but the lines the scheme numbers are drawn from no sheet, so a
number put on them is conjectural whatever its own provenance. So the seating is graded at the
**bottom tier**, `confidence` is `const: "reconstructed"` in the schema, and the gate re-reads
the phase and fails if a documented address has quietly promoted a reconstructed roof.

The seating writes **one block** and nothing else â€” no coordinate, no footprint, no form
value, and not even the record's `function`, which the dooryard, fence, planting and
signboard generators read to decide what stands in a yard. No mesh changed and nothing was
re-baked. The town gained an address, not a building.

### Three things it refuses, and two it records rather than draws

It is **not** "G. Spring's house": he is who to apply to for terms, `is_the_occupant` and
`is_the_owner` are `false` in the ledger and refused if they are not, and the same G. Spring
is the attorney the papers put near Franklin and South Water. T-0412 is that trap read from
the other side. It may not seat two addresses on a roof, or one address on two roofs.

Recorded rather than drawn: the notice calls the house **LARGE** and the fabric under the
address is a 5.36 Ã— 6.38 m D3 count-unit dealt long before the address resolved (**T-0593**);
and the **fine well** is not drawn, because this town has no well of any kind and the first
one would stand on the single lot whose address happens to resolve (**T-0592**). Both are on
the record in the notice's own words. A documented feature that is absent is stated, not
omitted.

## Shipped 2026-09-03 â€” T-0450: three caps, and the one a leg's margin is taken against

**`docs/SMOKE-BUDGET.md` opened by telling three tickets that the 30-minute cap their
margins are taken against "is not this machine's". It was wrong, and it has ranked those
tickets against the wrong bound since 2026-08-30.** The page compared a **per-leg**
timeout with a **whole-body** reading. They do not bound each other:

| cap | what it bounds | where it is written |
|---|---|---|
| 600 s | ONE foreground command in a steward run | the harness |
| 30 min | ONE LEG of the nightly gate â€” one viewport, one stage range, eight legs in parallel | `chicago-4d-bake.yml` Â§ `smoke` |
| 90 min | the WHOLE body in one process, no per-leg cap at all | `chicago-4d-smoke.yml` Â§ `smoke` |

The 55 m 10 s figure offered as proof is a reading of the third row and sits comfortably
inside its own cap. **T-0170, T-0173 and T-0181 were reasoning about the leg cap
correctly**, and the page now says so.

**The same-machine half is settled from committed files rather than from a timing.** The
nightly gate's legs, the full-body run, the dev gate and the steward improve runner are
all `runs-on: ubuntu-latest`; the two smoke workflows install the same `playwright@1.56.1`
and chromium alone; `smoke_renderer.mjs` passes `--enable-unsafe-swiftshader` wherever it
runs. T-0450's own pair of readings â€” 4 m 40 s on the gate runner, 4 m 44 s on the improve
runner, four seconds apart â€” is recorded with its provenance, **and with its unverified
half named**: the ticket gives `dev` at `415909cf` for both, while run 33290607360's head
commit is `fc10c83d`, so "the same bytes" is not a checked fact and is not claimed as one.

**The leg table is a tool, not prose, because four re-cuts in 2026 rotted every prose copy
of it.** `node tools/smoke_budget.mjs --legs` reads the stage ranges and the cap out of the
workflow and prices each leg from `tools/dev-smoke-state.json`. Today: the worst fully
measured margin is **desktop `10-13` at 12 m 09 s**, and a leg whose only readings straddle
its boundary is priced with the neighbour included and says so â€” cost an upper bound, margin
a lower one. `--self-test`, which `check.sh` runs, now fails if the ranges ever stop tiling
parts 1..13 exactly once; the workflow's own comment has asserted that since T-0171 and
nothing held it.

**Nothing a visitor can see changed, and T-0181 is not closed by this.** Its acceptance â€”
the worst desktop leg measured on three separate runs, the spread recorded, the cap or the
cut set from the spread â€” stands unchanged, because the 17 m 51 s above is summed from
per-part readings that each paid their own boot, which is the very prediction-from-parts
move that ticket was opened to object to. What is removed is only the claim that it was
arguing against the wrong bound. The re-read is written into T-0181 itself.

## Shipped 2026-09-01 â€” T-0462: the next 75 real names receive deep research

**Resident identity research now covers 150 of 848 eligible real named people
(17.7%), with no reconstructed person admitted.** The second fixed, non-overlapping
cohort contributes 27 corroborated enrichments, 23 explicitly unmerged candidates and
25 documented no-find outcomes. Cumulatively the public layer carries 31 corroborated
findings, 30 candidates and 89 no-finds.

The pass used six parallel research streams and 47 newly registered sources across
contemporary statutes, a Supreme Court report, an 1843 directory, institutional
biographies and finding aids, edited papers, county and church histories and local
archives. Exact queries, source limits and conflicts are retained. Surname form was a
search lead only; it produced no heritage, lineage, immigration, kinship or occupation
claim.

The most important correction is methodological: **a waiting letter demonstrates
postal reachability, not bodily presence in Chicago**. Strong matches place Ezra
Galusha at Warrenville, George R. Makepeace near Joliet, Paul Burdick at Milwaukee,
Thomas R. Covell at Salt Creek and Chester House at House's Grove. Each remains a
candidate rather than being rewritten as a town resident.

The likely Eliza Chappel duplicate remains merge-pending-scan, as do Aaron
Parcel/Aron Parcell and Alonzo Murray/Murry spelling pairs. Ebenezer Ford gains a
strong Fort Dearborn/church candidate and an identified missing May return, but no
household was silently edited. `docs/RESEARCH/resident_identity_pass_02_75.md` records
the full assessment and continuation priorities.

## Shipped 2026-08-30 â€” T-0384: an ordinal off a corner places a store, and claims no lot

**John Holbrook's clothing store stands on South Water Street, one door east of Dearborn**,
between the Chicago American's office at the corner and Frederick Thomas's shop. Two papers
print the address â€” Democrat 1835-06-10 c010 (*"on South-Water st. one door from Dearborn
street"*) and American 1835-06-13 c012 â€” and the reading that let him be placed is the
owner's ruling of 2026-08-30: **a count of doors off a named corner is an ordinal off the
corner, not a reach of the street**. `docs/CORNER-ORDINAL.md` is the policy.

### What was in the way, and it was not the question the ticket named

T-0384 was written believing the blocker was *"may a business-front lot carry two documented
storefronts standing at the street?"* â€” PR #514's question, parked on `hold`. It was not. Under
the register as committed the advertisement read as `street_only`, so `docs/STREET-FACE-ADOPTION.md`
owed Holbrook a standing South Water roof and **there is not one free**: nineteen front the
street, five are a named household's dwelling, five are yard buildings, nine are already
adopted. He was one of seven South Water advertisements short purely on supply.

### The limit, and it is enforced in fields rather than in prose

An ordinal is **not a lot**. The record carries `lot_claim` â€” `claims_lot: false`, `lot: null`,
`placement_rule: corner_ordinal` â€” the schema permits no other value for either of the first
two, and `tools/plat_occupancy.no_lot_claim_ids` reads it: such a record is not a HOLDER of the
lot for the owner's business-front clause of 2026-08-27, so it neither entitles the lot it
stands on nor exhausts it. That is exactly what PR #514 lacked â€” standing Holbrook beside the
American's office switched the clause off, `len(holders) != 1`, and `generate_block_infill.py`
was refused a roof it had been dealt. Nothing physical is relaxed: separation, lot margins and
corridor intrusion all still bind, and `occupied_lots` still counts the roof against its
block's headroom.

The transparency runs **one way on purpose**. A lot held only by no-lot-claim records reads as
taken and the run is not dealt it â€” the conservative answer, costing nothing today because no
such lot exists. Freeing it would be a second ruling, about ground rather than evidence.

### The vocabulary is derived, which is why it does not have to be re-decided

A reading pass writes what it always wrote â€” `class: relative`, an anchor naming the cross
street, an `offset_normalized` carrying the phrase â€” and `compile_register.ordinal_off_a_corner`
reads the ordinal out of it. Three tests, each refusing a phrase the corpus actually prints:
the offset must count doors in a word translatable to a number (*"a few doors below"* is
refused), the reference must resolve to exactly one platted street, and the business's own
street must be a different one. An ordinal off a BUILDING is untouched â€” it resolves earlier,
as a landmark hop.

### The sweep, and what it found that is not this ticket's

`tools/measure_corner_ordinals.py` reports it on every run: over 86 extraction files, **28**
claims count doors, 5 name a corner of two streets and resolve as one, 20 are landmark hops or
name no platted street, and **3 are readable as an ordinal off a corner**. Those three are
Holbrook's Democrat printing and Clark, Filer & Co.'s warehouse *"five [doors east] of the
corner [of Randolph st.]"*, printed twice. Holbrook's other printing is NOT readable: the
American's transcription cuts the cross street to *"De[arborn]"* and a bracketed supply is not
a street name â€” so the Democrat's printing is what carries the placement, and it also
corroborates the street word the American's column lost.

**Clark, Filer & Co. is a finding and it is not fixed here.** Three of its printings carry the
anchor and the gazetteer's LIVE placement for the house is `class: none` with a null street, so
`resolve_anchor` is handed nothing and the row reads `unplaceable`. That is a gazetteer fault,
not this policy's; **T-0440** carries it, including the count of other houses in the same
position, which nobody has taken.

### What is unverified, stated plainly

- **Which side of Dearborn is a reading, not a source.** East is taken because the three
  addresses this block face's own papers print describe a continuous row when read eastward and
  nothing that closes when read westward. The position is graded `inferred` for that reason.
- **The metres are a convention.** L215's door-gap rule â€” a neighbouring front stands 3.048 m
  (10 ft) clear of the wall it neighbours â€” has two reasons and no source. A second ordinal
  placement anywhere in the corpus turns it from a convention used once into a rule that has to
  be argued.
- **Every dimension of the building is borrowed** from `chicago_american_office` and
  `frederick_thomas_shop` on the same face. Nothing about the premises is attested.
- **PR #514 is superseded, not merged.** It built the same store against a reading the owner has
  since ratified, but it claimed the lot and went red on the platted-parcels step; its branch is
  closed rather than left parked.

## Shipped 2026-08-31 â€” T-0442: 75 real named residents receive identity reviews

**Seventy-five of 848 eligible attested or inferred named people (8.8%) now have a
dated, reproducible identity-research outcome.** The fixed sample spans five established
profiles, every one of the twenty richer unplaced newspaper records, and fifty of the
post-office-only names split evenly between present and uncertain. No reconstructed
person is eligible.

The result is deliberately less flattering than 75 new biographies: **4 corroborated
findings, 7 candidate identities and 64 searches with no safe match**. Candidates are
published on the resident card with their supporting source, conflict and an explicit
â€œnot mergedâ€ warning. A no-find says what it is too: the reviewed search did not find a
safe bridge, not that the person did not exist.

The useful near-matches include Augustus Garrett, James Curtiss, Buckner Stith Morris
and David Brookins. Jesse W. Fell is explicitly rejected as the automatic expansion of
J. W. Fell because institutional chronologies put Jesse in Vandalia and Clinton in
1835. J. H. Collins is the strongest resolution: profession and his distinctive Caton
partnership connect the abbreviation to James H. Collins by more than the name.

No household, marriage, kinship, immigration or heritage field was invented. The
source hierarchy explicitly forbids surname-based heritage claims. The cohort,
outcomes, source resolutions and public payload re-derive in the gate; browser checks
hold both candidate and negative-result warnings on mobile and desktop.

## Shipped 2026-08-30 â€” T-0170: the last part of the gate that could not be run is halved

**Nothing a visitor sees.** `SMOKE_STAGE` has THIRTEEN parts; part 10 is halved and old parts
11-12 are 12-13. This is the last piece of T-0121 and the third re-cut of the day, after T-0346
and T-0173.

**The part was never inside the ceiling.** Profiled at 1280x800 with `SMOKE_TIMING=1` on an
**idle** runner â€” load average 0.27-1.48, zero other Chromium processes, the friendliest reading
this suite can be given â€” it was **killed at 9 m 20 s** with the street readouts and the Settings
units still to run. Third and fourth kill of the same part. T-0167's 7 m 43 s is the outlier in
the record, not the number to size a cut from.

**It had been skipped twice for want of a boundary.** This part carried no `// --- section ---`
headers at all; that is the stated reason T-0167 cut part 8 instead. Eight seams are named now,
so the next cut here is a choice from a list rather than a fresh profile.

**The first cut was measured and rejected, and it is in the record.** Cutting above R-BUG7's
flower-head census gave **5 m 05 s / 6 m 24 s** â€” a 3 m 36 s margin, and this project's own rule
(ROADMAP Â§ THE RUN BUDGET) is that a margin that thin is not a margin. Moving that one section up
into the head balances it.

| part | desktop | margin | staged | verdict |
|---|---|---|---|---|
| 10 | **5 m 59 s** | 4 m 01 s | 23 | 1 failed â€” T-0279's flower heads, 2,693 of 18,893 |
| 11 | **4 m 41 s** | 5 m 19 s | 13 | SMOKE PASS |

23 + 13 = **36**, the count the single part took. The red is inherited:
`tools/dev-smoke-state.json` records the same check red on dev at 2,526 of 18,911 on 2026-08-29,
and it does not fire at mobile at all.

**Nothing dropped, measured as an equality.** At mobile on the same tree, the pre-cut
`smoke_renderer.mjs` at the single part gives **45 passed / 0 failed / 36 staged / 9 always-on in
5 m 59 s**; the pair gives **45 / 0 / 36 / 9 in 6 m 01 s**. A pair still boots once, so the mobile
recipe does not grow a command.

**One binding crosses and it is the one that already crossed the stage split.** `streetLayer`, so
`anyStage(7, 10)` becomes `anyStage(7, 10, 11)`. The other six names the scan found below the
line (`headSupport`, `horizon`, `over`, `planted`, `popIn`, `sward`) are prose or strings in every
occurrence. The second half's prologue is `enterTown()` and `setFly(false)`.

**The readings are of THIS tree.** The cut was first measured at parts 9 and 10, before T-0173
merged and shifted the whole tail by one; every figure above was re-taken after the re-derivation
onto T-0173's numbering and agrees with the first pass to within six seconds (5 m 58 s / 4 m 38 s
then, 5 m 59 s / 4 m 41 s now). All three are filed in `tools/dev-smoke-state.json`.

**Read the margins as readings of an idle machine.** T-0215's factor of twenty is not repealed by
a cut: 4 m 01 s is a margin against the box that measured it.

## Shipped 2026-08-30 â€” T-0333: eighteen inches of stack, and the town was already inside it

**The Town of Chicago's by-law of 5 August 1835, section 18, is the first documented
DIMENSIONAL constraint this project holds on anything above a roof line**, and it is now
measured and gated. `chicago_democrat_1835_08_19#c005`, page 1 column 2, prints it line by
line: *"every stove pipe or chimney passing through the roof of any building shall extend
and be carried at least eighteen inches above the roof, and no stove pipe shall be passed
through the side or end of any building"*, under five dollars for each and every offence,
with a fire warden in every house, store and shop once a month from September to May.

### The census, and it is the whole finding

`tools/measure_stack_ordinance.py`, read off the committed masters' glTF accessor bounds
rather than off the generators that wrote them â€” the same discipline `measure_stack_fabric.py`
(T-0137) uses, and for the same reason: the generator is the thing under test.

| archetype | buildings | above its own roof |
|---|---|---|
| `frame_dwelling` | 116 | 0.780 m â€” 30.7 in |
| `log_dwelling` | 44 | 0.720 m â€” 28.3 in |
| `frame_storefront` | 36 | 0.710 m â€” 28.0 in |
| `frame_tavern` | 11 | 0.550 m â€” **21.7 in**, the tightest in the town |
| `fort_structure` | 6 | 0.780 m â€” 30.7 in |
| **town** | **213 buildings, 234 stacks** | **least 0.550 m, 3.7 in of margin** |

**Nothing was raised, moved or rebuilt, and no master was rebaked.** The ticket anticipated
this outcome in its own words â€” *"the answer may already be compliant, in which case this
ticket closes as a GATE and a provenance note rather than as geometry"* â€” and it is what the
measurement says. `docs/LIBERTIES.md` is untouched: a documented constraint the model already
satisfies is not an invention.

### What is unverified, and what is deliberately not decided

- **The clearance is measured to the RIDGE**, which is the top of the `roof` material. A
  stack standing off the ridge â€” `frame_tavern` across the frontage, `frame_storefront` on
  a shed roof â€” breaks a roof plane lower than that, so its true projection is larger than
  the figure above. The figures are a floor, not an estimate.
- **A building carrying stacks on two roofs reports its tallest.** That the ell's or the
  frame addition's stack clears its own ridge by the same margin is the ARCHETYPE's
  guarantee â€” every archetype builds each stack with one helper, relative to the ridge it
  is handed â€” and not this measurement's. Stated rather than assumed.
- **The corporation limits are not drawn and this gate makes no ruling about them.**
  Section 18 binds *"within the limits of the Corporation"*; section 22 of the same sitting
  walks those limits street by street and is **T-0334**, unbuilt. Nothing is conformed to a
  rule that may not bind it, because nothing has to move: every stack clears eighteen inches
  on both sides of a line nobody has drawn. If a record ever legitimately stands a shorter
  stack outside the limits, T-0334's boundary is what scopes this gate, and the gate's own
  failure message says so instead of inviting the next run to weaken a documented figure.
- **The by-law postdates the scene date by five weeks and is not applied retrospectively.**
  It is used as a bound the drawn town is measured against, not as a rule the 1 July town
  was held to.
- **There is no stove pipe anywhere in this model.** Every stack drawn is masonry, so
  section 18's second clause â€” no pipe out through a side or end wall â€” binds nothing that
  is drawn. That answers the ticket's second question: the archetypes do not distinguish a
  pipe from a chimney because they have only chimneys.

`docs/RESEARCH/chimneys.md` Â§ 7 holds the reading. `tools/check.sh` runs the gate and its
four self-test cases.
## Shipped 2026-08-30 â€” T-0173: the desktop gate's part 7 is halved, and both halves fit

**Not a thing a visitor sees.** It is the thing that lets a run PROVE what a visitor sees. A
steward run's single foreground command is capped at ten minutes, and part 7 stopped fitting
inside it: profiled on the steward runner with `SMOKE_TIMING=1` at load 0.81-2.86, it was killed
at **9 m 25 s** with its last two assertions unrun and `the suite body ran to completion` reporting
a FAIL that looks like a product red and is not one. That is the third desktop part to go this
way (T-0121's four, T-0167's part 8, T-0346's part 4 the same morning), and the cause is the same
one every time: the town grows and the part grows with it.

- **The cut is measured, and the measurement says where.** The profile puts **7 m 04 s of a
  9 m 25 s part in ONE block** â€” the three road-legibility stations, each of which teleports to
  its own viewpoint and reads `page.screenshot` frames through five distance bands. Around it:
  20 s of boot, 33 s of navigation and the street-layer checks, 1 m 04 s of the R-A1 aid, and the
  batch merge under that.
- **So the boundary could not be one of the file's own `// --- ` section headers**, which is what
  T-0170 had already found and left for whoever cut it: the best of them leaves **7 m 37 s against
  1 m 30 s**, which is not a cut, it is a rename. The cut falls at the STATION instead â€” the grain
  the block is actually made of. Each station teleports to its own viewpoint, takes its own frames
  and answers its own `check`, and none of them reads anything a sibling left standing.
- **Nothing crosses it.** `roadRuns` is local to the block. The movement report built from it is
  printed and never gated, and it has always compared only what the invocation measured â€” that is
  what lets `SMOKE_VIEWPORT=mobile` run without retiring desktop's half of the bank â€” so a part
  reporting on its own stations is the existing rule, not a new one. `--update-road-bands` merges
  per band and leaves untouched bands alone. R-A1's three assertions are taken STANDING AT
  `lake_market`, so that station goes into the new part with them, in the same order, unchanged.
- **Measured after the cut, at desktop, same runner and same hour:** part 7 â€” **5 m 05 s, 12
  staged, SMOKE PASS**; part 8 â€” **5 m 06 s, 8 staged, SMOKE PASS**. 12 + 8 = **20**, exactly the
  count the old part 7 was taking, which is how "never dropping a check" is demonstrated rather
  than asserted. Both halves clear the ceiling by **4 m 55 s**, against the 35 s the old part 7 was
  over it by.
- **Which of the two carries the shared street reading matters, and it is part 7.** `anyStage(7, 9)`
  becomes `anyStage(7, 10)`; `streetLayer` â€” the most expensive single evaluate in the file â€” is
  referenced in parts 7 and 10 and nowhere else, checked statically and then run. Part 8's own
  profile is the proof it does not pay for it: boot at 0 m 17 s, first station at 3 m 17 s, no gap
  where that reading would sit.
- **Parts 8-11 are renumbered 9-12**, because this cut is mid-body and T-0167's append could not be
  repeated (T-0346 hit the same wall the same day). The pairing rule survives in content and moves
  in spelling: `1+2, 3+4+5+6, 7+8, 9+10+11` becomes `1+2, 3+4+5+6, 7+8+9, 10+11+12`, ranges
  `1-2 3-6 7-9 10-12`. `chicago-4d-bake.yml`'s smoke matrix is edited in this commit, as its own
  comment demands of any renumbering; the ranges still tile 1..12 once each with no gap or overlap.
- **The renumbered legs were run, not reasoned about.** Mobile `SMOKE_STAGE=7-9` is **43 passed,
  0 failed, 34 staged** in 7 m 33 s â€” the same 43 the old `7-8` leg reported on 2026-08-30, so the
  leg carries exactly what it carried. Mobile `SMOKE_STAGE=10-12` is **168 passed, 0 failed, 159
  staged** in 9 m 33 s, which fires all three renumbered tail parts.
- **`tools/dev-smoke-state.mjs` mirrors `PARTS` and had to move with it** (11 â†’ 12), and
  `CHANGELOG_PARTS` with it (What's-new is part 11 now, not 10).

**What this does NOT close.** T-0173's acceptance names three parts and this is one of them: the
old part 4 was T-0346's, and the old part 7 â€” **now part 10** â€” is T-0170's, which is still open
and still measured over the ceiling on three separate runners. T-0173's own instruction was "do
not cut part 7 twice", and cutting a part that another ticket owns while eight slices of this lane
run at once is exactly the way to do it twice. So T-0173 closes on what it uniquely owned and
T-0170 keeps its own part, with the numbers in it re-labelled for this cut.

**Re-taken after a rebase, because dev had gained a geometry change under it.** T-0333 put a stove
pipe on every roof in the town while this branch was being measured, so the desktop pair was run
again on the rebased tree: part 7 **5 m 03 s / 12 staged** and part 8 **5 m 06 s / 8 staged**,
both SMOKE PASS, within three seconds of the first pair. `./tools/check.sh` PASS on the same tree,
and `node tools/smoke_budget.mjs --self-test` â€” T-0235's map, merged into dev the same hour â€” is
green on the new numbering.

**A caveat on every figure above, and the ROADMAP already states the rule.** These readings were
taken at load average 0.81-2.86 on a 4-core runner. T-0215 measured a factor of twenty between a
quiet box and a loaded one, so 4 m 55 s of margin is a floor on what these parts cost, not a
description of it.

## Shipped 2026-08-30 â€” T-0305: the four readings the American contradicts itself on

**What a visitor sees:** S. B. Cobb's saddlery â€” the corner shop on Lake Street in the West
Division â€” now carries an **open question** on the provenance card you get by walking up to it,
and the Evidence panel's open-questions list goes from four to five. It is the second building in
the scene whose card asks a live question rather than only grading a claim.

**The ticket was filed with a title that asserted its own answer** â€” *"need the page images"* â€”
and an empty acceptance clause. The acceptance was written first, and written so that it could
refute the title: name the four, test each against the whole 86-issue corpus rather than against
the American alone, and only then put what survives to the owner. Nothing survived the corpus
test. The title was right, and it is right for a stated reason now instead of by assertion.

**The four, and the shape of each.** `tools/measure_american_contradictions.py --gate` re-derives
them; `docs/RESEARCH/american_self_contradictions.md` quotes every printing.

| # | question | printings | the corpus |
|---|---|---|---|
| 1 | Edward Burton's tailoring shop â€” Franklin or Lake street | one card, one copy date, four settings: Franklin, Franklin, unresolved, **Lake** | `Burton` is not in the Democrat at all |
| 2 | Wm. Sabine â€” North or South Water Street | North 06-13 and 06-20, **South** 07-04 | one post-office letter-list line |
| 3 | John Dave[s] â€” the card set below Sabine's | the same two dates, the same two readings | three letter-list lines |
| 4 | S. B. Cobb's saddlery â€” which cross street | Lake legible in all three 1835 cards, the cross street lost in all three | the Democrat's 1833 *"Lake and Canal streets"* |

**Three things the run found that the ticket did not know.**

- **2 and 3 are one event, not two.** Both houses read North in both June settings and South in
  the July one. Two firms do not cross a river together between issues; a compositor resets a
  column. That does not say which reading is right â€” it does mean **one page image settles both**,
  and it is why the ask is six columns for four questions rather than eight.
- **The contradicting printing is invisible to the register.** On 1835-07-04 the three forwarding
  cards were extracted as ONE claim, filed under the third firm's name (Newberry & Dole), so
  `business_wm_sabine_storage_forwarding_and_commission_merchant` reads "North Water Street" flat
  with no disagreement recorded on it. The South reading survives only on John Davis's entity and
  in that claim's own note. **Not re-cut here**, deliberately: re-cutting a claim is a reading of
  the page, and the page is the thing that is missing.
- **Question 4 is the weakest of the four, and that is worth knowing before anyone spends a
  scan on it.** The 1833 corner is one of the few addresses in this project read off the page
  images themselves â€” `chicago_democrat_1833_11_26` carries `verified: true` â€” so the American's
  silence is not doubt about 1833. What it leaves open is the twenty months after it: whether the
  shop Cobb *"will continue the above business at"* in June 1835 is the same corner, which is
  exactly the identification the record grades `inferred`.

**A sentence that was counting, and had already gone wrong.** The Evidence panel's own account of
the open questions ended *"one of them is standing in front of you"*. That was true of four
entries and stopped being true on 2026-08-29, when the New York House became the second standing
one â€” a day before this run added a fifth. It is the same failure the hand-typed paraphrase before
it made, and the same failure the panel's own changelog entry says it fixed. It counts nothing now:
each entry carries its own `standing` flag and the chip beside it says which.

**What is left is the owner's, and it is six columns**, all in the American â€” 1835-06-13 p3 c5,
1835-07-04 p4 c4, 1835-06-27 p3 c5, 1835-08-15 p3 c6, 1835-06-08 p3 c5, 1835-07-11 p3 c6. Two of
them serve two questions each. Nothing smaller will do it: every reading above is already the best
the transcription can give, and three of the four subjects appear nowhere else in eighty-six
issues except a list of letters waiting at the post office. The ticket is `blocked-owner` on
exactly that ask.

**Held by a gate, not by memory.** Every reading is declared with the page and column it sits in
and re-derived on every `check.sh`, along with the negative half over all seventy-three Democrat
issues. Eight assertions, each proved to fire under `--self-test`. The day one of these four is
answered â€” by an image, or by an extraction pass reaching a card nobody has read â€” the build says
so.

## Shipped 2026-08-30 â€” T-0346: the desktop gate's costliest part is cut into three

**Nothing you can see changed.** This is exemption 3 of the visible-progress rule: a gate that is
blocking visible parcels. `tools/smoke_renderer.mjs` part 4 was being killed at the ten-minute
foreground ceiling a steward run's single command has, so no run could take the desktop half of its
own gate â€” and part 4 is where the draw-call and triangle ceilings are gated at the town's worst
frame, which is exactly the check a NEW BUILDING breaks. T-0385 (the New York Clothing Store in
Dearborn Street) and T-0375 (five documented tradesmen on South Water Street) both stand roofs and
both have to clear that ceiling; until today neither could demonstrate it on the runner that ships
them.

**The cost was one section of ten, and it was measured rather than guessed.** `SMOKE_TIMING=1`
under this lane's own eight-way contention, 2026-08-30, against `--published`:

| section of part 4 | reached at | left at |
|---|---|---|
| raycast pick â†’ walking â†’ bridge deck â†’ budgets â†’ life size â†’ nothing hovers | 0:18 | 1:10 |
| **the scene-detail ladder** | 1:10 | **7:27** |
| the gate and the chrome | 7:27 | 8:42 |
| the confidence menu's own clicks | 8:42 | killed at 9:20 |

Six minutes and seventeen seconds of a ten-minute part sat in ONE section. That section walks every
stand in `STANDS` at every detail tier and cannot be halved without walking the set twice â€” the
single-walk saving is what T-0135 built it around â€” so it is a part on its own rather than a
boundary nudged along.

**The cut, and what crossed it.** Two named section boundaries, both re-verified for crossing
bindings the way T-0121 and T-0167 verified theirs. Exactly one binding crossed: part 4's `stats`,
read only for `stats.budget.drawCalls`. Part 5 now reads that ceiling itself, out of `stats.budget`
rather than written into the test, so the bar still follows its definition site in `main.js` and a
scene that outgrew its budget still cannot be made green by editing this file. The ladder takes no
pose from what ran before it â€” `order` teleports to each stand itself and finishes at the reference
frame â€” so no `enterTown()` or re-framing was needed at the boundary.

- **Parts 4, 5 and 6, measured under the same load:** 1 m 09 s (17 staged checks), 6 m 46 s (16),
  3 m 13 s (6). All three SMOKE PASS at desktop against `--published`.
- **Nothing was dropped, and it is checked rather than claimed.** At mobile, where the old part 4
  still fitted the ceiling, `origin/dev`'s part 4 and this branch's parts 4-6 report the SAME
  numbers on the same tree: **51 passed, 0 failed, 42 staged-section checks, 9 always-on** â€” 6 m 17 s
  against 6 m 15 s. That is the arithmetic the audit line exists for, run as an equality.
- **Parts 5-9 are renumbered 7-11**, because these two sections sit in the MIDDLE of the body and
  T-0167's append could not be repeated. `anyStage(5, 7)` â€” the shared street reading â€” becomes
  `anyStage(7, 9)`; `streetLayer` is referenced in parts 7 and 9 and nowhere else, checked
  statically and then run: `SMOKE_VIEWPORT=mobile SMOKE_STAGE=7-8` is **43 passed, 0 failed** in
  7 m 31 s.
- **The pairing rule survives in content and moves in spelling.** `1+2, 3+4, 5+6, 7+8+9` becomes
  `1+2, 3+4+5+6, 7+8, 9+10+11` â€” the same four mobile commands carrying the same parts, ranges
  `1-2 3-6 7-8 9-11`. `chicago-4d-bake.yml`'s smoke matrix is edited in this commit, as its own
  comment demands of any renumbering; the ranges still tile 1..11 once each with no gap or overlap.
- **`tools/dev-smoke-state.mjs` mirrors `PARTS` and had to move with it** (9 â†’ 11), and
  `CHANGELOG_PARTS` with it (What's-new is part 10 now, not 8).

**One thing this leaves behind, stated rather than hidden.** Every reading already in
`tools/dev-smoke-state.json` is filed under the OLD numbering, so a reading labelled `stage: "5"`
is the part that is now 7. Nothing reads them as a bar and every one of them carries a `treeHash`
that no longer matches any tree with this file in it, so `ask` will say it was not taken on your
tree â€” but the numbering is now dated and the record's note says so.

**What this does NOT do.** It does not re-profile the whole desktop recipe under load, and it does
not resize the parts T-0346's second measurement put over the ceiling for reasons that were later
shown to be contention rather than cost (old stages 5 and 7, now 7 and 9). That is a second
demonstration and therefore a second ticket: T-0346 was split rather than shipped as a self-invented
half.
## Shipped 2026-08-30 â€” T-0369: desktop stage 8's verdict stops depending on which stages ran in front of it

**Nothing you can see changed.** This is a gate repair, taken under AGENTS.md's third
visible-progress exemption: the stage split exists so a branch can verify a subset, and a subset
that is red only because of its own composition costs every visible parcel an argument about whose
failure it is. T-0316's run re-ran `dev` twice to establish that its own change was innocent.

**The measurement, reproduced on this runner on an unmodified `dev` (published mirror):**

| command | verdict |
|---|---|
| `SMOKE_VIEWPORT=desktop SMOKE_STAGE=8` | 37 passed, 0 failed |
| `SMOKE_VIEWPORT=desktop SMOKE_STAGE=1,8` | 75 passed, **1 failed** â€” `clickChrome: .panel-tab[data-tab="settings"] is covered at its own centre by <h2>` |

- **The `<h2>` is the inspect card's, and the card is part 1's.** `clickChrome` named the tag and
  not the thing it belongs to, so the first act of this ticket was to make it walk up to the
  nearest ancestor carrying an id. The failure then reads `covered at its own centre by <h2>
  inside #popup`, which is the whole diagnosis in one line. Part 1's last page interaction is
  `boardPick` â€” twenty-five `pick()` calls proving that aiming at the Tremont House's signboard
  opens the business behind it â€” and a `pick()` that lands on a structure OPENS the card. Part 1
  never closed it. `#popup` is `position: fixed; z-index: 30; top: 58px; right: 12px`, 392 px
  wide; the HUD panel is 380 px wide at the same corner, so on 1280Ã—800 the card sits squarely on
  the panel's tab strip. Part 8's first statement clicks a tab.
- **Why it survived the split's whole existence.** Nothing between part 1 and part 7 reads panel
  chrome â€” parts 2â€“7 read the scene graph or take their own captures, and part 4 happens to close
  the card mid-part for its own reasons. Part 8 is *nothing but* panel chrome, and it is the only
  part that inherits the leak with something to lose.
- **Repaired at both ends, and only the second end makes the verdict order-independent.** Part 1
  closes the card it opened and now ASSERTS the teardown â€” `part 1 hands the page on with nothing
  standing over the chrome`, over `#popup` and `#control-help` â€” so the next part that walks away
  leaving an overlay up is named at the boundary where it happened rather than four parts later
  under another gate's name. Part 8 also clears the card in the same preamble that already
  re-opens the panel, so it no longer depends on *every* predecessor being well-behaved. Nothing
  was weakened: the added check is new, and no existing assertion moved.
- **It is NOT the same fault as T-0349, and that hypothesis is now refuted rather than open.**
  T-0369 was filed as the second instance of T-0349's shape and suggested both be answered by one
  repair. They cannot be. T-0349's own third reading names its cause exactly â€” the signboard
  gate's seventh clause counts `frontage.meshes === 62` and a run with stage 1 behind it carries
  five extra `frontage-far-merge` meshes the desktop camera's history caused. That is a census
  clause reading a distance-merge artefact; this is an overlay left standing over a control. Two
  different faults that share only the phrase "red after stage 1". T-0349 is untouched here.

**Verification.** `./tools/check.sh` PASS. `tools/smoke_renderer.mjs --published`: desktop
`SMOKE_STAGE=1,8` **105 passed / 0 failed** (was 75/1), desktop `SMOKE_STAGE=8` alone **37 passed
/ 0 failed** â€” the same verdict both ways, which is the acceptance. Mobile `SMOKE_STAGE=1,8`
**105 passed / 0 failed**. Both viewports carry the new part-1 check.

## Shipped 2026-08-29 â€” T-0358: the plat gets its block numbers, and the corpus's only address resolves

**Nothing you can see changed.** This is a dependency: the corpus's one lot-and-block address â€”
G. Spring's *"LOT No. 7, in block No. 16, one lot east of Haddock's Tavern, on Lake street"*,
printed six times in the *Chicago Democrat* â€” resolved to nothing, because
`data/traces/vectors/thompson_lots.json` keys its nineteen blocks on their bounding streets and no
committed source numbered one. Three separate readings had recorded that this was the most
placeable statement the corpus makes and that placing it was somebody else's job.

**The evidence turned out to be two numerals, not three.** `clark_reach_bulge_1834.md` Â§ 8 and
`thompson_plat_grid.md` Â§ 4 both said the owner's crop of Wright's 1834 sheet reads *"block numbers
19, 18 and 17"*. Re-read at full resolution â€” the file is 639 Ã— 719 px â€” it carries **19 and 18**,
and the map region ends at block 18's east edge; the asset's own README, written when it was
supplied, describes two. The third arrived in the retelling. Both memos are corrected, and nothing
built on them moves: two consecutive numerals fix the step and the direction as well as three would.
What changes is that a later reader can now see how far the base can be pushed, which matters
because this ticket pushes it three blocks.

- **Six blocks are numbered and everything else is refused in writing.** 19 west of 18 fixes the
  step at one, falling eastward, and fixes it *along the tier* â€” two blocks side by side differing
  by one cannot be column-major. The watercourse drawn in the street between them is the one
  already traced at local E +462â€¦+469, the east half of the La Salle corridor (centreline E +451.3;
  Wells 122 m west, Clark 123 m east), so they are Wellsâ€“La Salle and La Salleâ€“Clark. Counting:
  **21 Marketâ€“Franklin, 20 Franklinâ€“Wells, 19, 18, 17 Clarkâ€“Dearborn, 16 Dearbornâ€“State.** The other
  two tiers, the West Division, the North Division and where the run begins and ends are all refused,
  each with its reason: two numerals in one row say nothing about how the run passes to the next.
- **Block 16 is the one counted number an independent source agrees with.** Dearbornâ€“State is
  bounded south by Lake Street, and the lot scheme the same crop shows runs 5 6 7 8 west to east
  along a south row â€” so lot 7 is the third lot east of Dearborn and Haddock's Tavern, one lot west,
  is the second. That is where T-0324 had already argued the Mansion House stood, from Andreas's
  "on Lake near Dearborn" and Botsford's corner advertisements, before any of this existed. Three
  statements, three sources, one block face. **The count stays `inferred`** â€” agreement is not a
  survey â€” and 17, 20 and 21 have no such check and say so on each record.
- **Nothing was promoted and no confidence moved.** `data/traces/thompson_block_numbering.json` is
  authored and carries the reading, the identification and the refusals;
  `tools/generate_plat_lots.py` only stamps it, and re-derives the grid byte for byte as before.
  Every `plat_lot_number` is `conjectural` *including block 18's own*: a number put on a line the
  module drew is conjectural whatever the number's provenance. No modern plat reprint was consulted
  and the record says so in terms.
- **Two consequences are now measurable and neither is acted on here.** The Mansion House stands on
  lot 5, the corner lot, and the corpus puts it on lot 6 â€” a gap of **24.2 m, one lot east**, which
  is inside the along-street allowance that record already declares, so the coordinate is unchanged
  and the note now carries the number instead of the sentence. And lot 7, which carried "a large
  Dwelling-House and fine well", holds an anonymous reconstructed count-unit roof. Standing Spring's
  documented house there is the visible follow-up, filed as **T-0423**.
- **No mesh went stale and this cost no bake.** `generators/mesh_inputs.py` hashes archetype, phase
  and resolved params; a block number moves no vertex.

## Blocked 2026-08-29 â€” T-0384: Holbrook's blocker was answered by a ruling nobody carried back to the ticket

**Nothing was built and that is the finding.** T-0384 sat at row 2 of the queue, `state: open`
and `blocked_on: null`, over a body that said in prose it was blocked behind an owner ruling â€”
*may a platted business-front lot carry TWO documented storefronts standing at the street?* â€” the
question PR #514 asked and is still parked on `hold` carrying. Every run that took row 2 had to
re-derive the same conclusion before it could put the ticket down. **The question in the ticket is
now the wrong one, and answering it would not have placed the store.**

- **The register re-read the advertisement.** `business_john_holbrook` today reads `action:
  street_only`, `anchor.kind: street`, over *"[on South] Water st., one door from Dearborn
  street"*, noting *"the anchor is a reach of dearborn and names nothing narrower"*. PR #514 read
  the same printed line as an ordinal off the corner and raised a 30 Ã— 25 ft shop 3.048 m east of
  the American's office. One line, two readings, and the register's is the committed one.
- **The owner ruled the same day what a `street_only` business gets** (T-0354, L212): it adopts a
  standing roof, nothing is built for it, and every adoption declares `lot: null` and
  `claims_lot: false`. Under that ruling Holbrook never seats on a platted lot, so the lot clause
  is **moot for him**. `street_face_adoptions.json` refuses him for supply instead â€” one of seven
  South Water advertisements against nineteen fronting roofs of which five are homes, five are yard
  buildings and nine are already taken.
- **The old clause was measured rather than assumed stale.** Through `tools/plat_occupancy.py`, no
  figure authored: 19 business-front lots dealt town-wide, 5 carry a documented building, the
  2026-08-27 clause is live on 2 and already off on 3 â€” and **0 register businesses anchor on any of
  those five**. The red PR #514 reported still reproduces (a second documented holder makes
  `len(holders) != 1` in `shared_business_fronts`, the run loses its lot, the platted-parcels step
  goes red), but widening the clause today would unblock nothing at all, Holbrook included.
- **The cheaper exit needs no ruling.** `adopt_street_faces.py` re-derives on every commit, so the
  first South Water roof **T-0375** frees seats Holbrook automatically. The ticket now carries that,
  and the one-line question it is actually waiting on, in `blocked_on` where `ticket.mjs board`
  shows it to the owner.

## Shipped 2026-08-29 â€” T-0417: the street-face adoptions reach the buildings, and nine come out of the yard

**The allocation is now SPENT.** T-0354 paired 24 documented businesses with reconstructed roofs
on the streets their advertisements name, and stopped there: the pairing lived in
`data/research/newspapers/street_face_adoptions.json`, the buildings still opened as anonymous
count-units, and the policy's own file said so â€” *"Nothing here writes a card"*. Nineteen roofs on
South Water Street, Lake Street and Randolph Street now carry an `occupants` block naming the
business, its trade, the street the paper puts it on and every claim the reading rests on. It is
derived, not authored: `tools/inferred_occupancy.py` â€” the ledger the inferred-household programme
already used for exactly this â€” hands the block to whichever generator owns the roof, so
`generate_block_infill.py --check` re-derives all nineteen byte for byte.

**Twenty-four became nineteen, and that is the finding.** Nine of T-0354's adoptions had been
seated in ANCILLARY roofs â€” the privies, stables and woodsheds the anonymous parcels deal behind a
lot. **Peter Cohen, clothier, grocer and liquor dealer and the best-attested shopkeeper in the
whole corpus at eight printings, was in `recon_1835_blk_south_water_clark_a3_05`, a privy.** The
rule against it was not new and was not weakly held: `tools/generate_block_infill.py` has refused
to hang an occupant on an ancillary roof since the inferred-household programme, on the ground that
*"a yard building serves the lot it stands behind, and an adoption is a claim about who lived or
worked in a building"*. The allocation simply could not see which roofs were sheds, and nothing
noticed for a day because nothing consumed the table. **An allocation nothing spends is an
allocation nothing checks** â€” that is the transferable lesson here.

- `tools/adopt_street_faces.py` gained refusal 6, *the roof is a yard building*, and its supply
  count now reports fronting roofs less homes less yards. Four of the nine took a principal roof
  instead â€” Harmon, Loomis & Co. moved from a shed into a narrow two-storey store â€” and five had
  none left on their street, so `every roof on the face is spoken for` goes 3 â†’ 8 and the waiting
  pile 36 â†’ 41 against the register this branch was cut from. Re-derived once more on the rebase
  onto T-0400, which merged firm groups and moved `street_only` 60 â†’ 59: **19 adopted, 40 waiting,
  7 of them short purely of supply.** All of it re-derived; none of it authored, which is the point
  of deriving the allocation rather than listing it.
- **Fifteen assertions fire when broken**, up from eight: nine in `adopt_street_faces --self-test`
  (including a business seated in a yard building) and six in `inferred_occupancy --self-test`
  (an adoption that claims a lot, an order that has become a claim, nothing to cite, a roof outside
  the anonymous layer, two businesses on one roof, a claim id naming no corpus source). The ledger
  also raises if the household programme and an adoption claim one roof, which nothing upstream
  prevents.
- **No geometry moved and no mesh went stale.** `generators/mesh_inputs.py` hashes archetype,
  phase and resolved params; an `occupants` block moves no vertex, so this cost no bake.
- **L212 is revised** with the new counts and the yard refusal; `docs/STREET-FACE-ADOPTION.md`
  carries refusal 6 and a re-measured table. The derived table's `_doc` had been citing L207 for
  its own liberty and now cites L212.
- Still not written here: a SIGNBOARD. `tools/generate_business_signboards.py` refuses a `recon_*`
  record by name, so a board on one of these roofs is a change to the signage rule and needs its
  own argument rather than a quiet exception.
- **T-0416** carries the rest of T-0387 â€” Wm. Sabine, John Dave and the Dearborn Street wine store,
  all three refused for want of a roof whose lot fronts North Water or Dearborn. That is an owner
  question (is a corner side a face?) before it is a placement.

## Shipped 2026-08-29 â€” T-0354: what a business does when the paper names a street and nothing narrower

**The register could place 58 of 203 documented businesses; 24 more now stand on the street faces
their advertisements name.** (T-0354's title says 24 of 190 with 49 `street_only`. It was filed that
morning; T-0380, T-0383, T-0355, T-0399 and T-0356 all landed on `dev` before this branch merged and
the `street_only` pile went 47 â†’ 45 â†’ 60 while it was being written. Every figure here is this
branch's own re-derivation against the register as merged, and none of it is authored â€”
`tools/adopt_street_faces.py --report` reprints all of it. **The policy did not move with the
counts**, which is the argument for deriving the allocation instead of listing it.) The owner ruled on 2026-08-29, choosing between the three options the
ticket set out, that a `street_only` business *adopts a reconstructed roof already standing on that
street face*. `docs/STREET-FACE-ADOPTION.md` is that ruling written so a later run applies it
without re-deciding it, `tools/adopt_street_faces.py` derives the allocation,
`data/research/newspapers/street_face_adoptions.json` is the derived table, **L212** is the liberty,
and `tools/check.sh` re-derives all of it on every commit.

**The four limits are assertions, not promises.** No adoption claims a lot (`lot: null`,
`claims_lot: false`, and the gate refuses a record that grows a lot field of any name); the adopted
roof stays `reconstructed`, re-read from the structure's own phase on every commit; which roof on a
face is an allocation by deterministic rule and says so in every record; and order within a face is
not a claim. Each of those four is a way the ruling could be breached silently by a later run, which
is why each is a check rather than a paragraph.

**What it moves, and where the rest wait.** 60 `street_only` in the register: **24 adopted, 36
waiting.** Twenty-four name Dearborn, La Salle, Canal or North Water, where no reconstructed roof's
platted lot faces the street â€” Dearborn has eighteen roofs showing it a corner side and none showing
it a front. Nine are a second heading of a house already seated on that face. Three are short purely
of supply. South Water took 14 of its 19 fronting roofs (5 are households' dwellings); Lake took 9;
Randolph took 1.

**What is unverified or deliberately left, stated plainly.**

- **Only `lot front` is adopted, and that is a decision with a cost.** `tools/fronting_street.py`
  also answers `corner side` and `centreline band`; both are refused here, because an
  advertisement's street is where the door is and a gable end reaching a street is not a doorway.
  **Widening the reading would reach 24 more**, and `--report` prints both readings side by side so
  the number an owner ruling would change is one number, not a rewrite.
- **Two Lake Street roofs are probably one house, and the corpus cannot say so.** Wm. G. Branchaud,
  W. G. Blanchard, G. Blanshard and F. G. Blanshard advertised one trade at one door within five
  months under four transcribed spellings; T-0413 joined the two Blanshards and **T-0408** read the
  whole run behind the other two and joined them, so the group takes two roofs now instead of four.
  'Branchaud' turned out to be a supply made from the only two columns of that card the
  transcription flags as Tesseract fallbacks â€” the impressions of 1834-07-16 and 1834-09-17, whose
  columns are independent Vision readings, set BLANCHARD â€” so the reading was repaired and an
  `identity.json` firm merge joined 'Wm. G. Blanchard' to 'W. G. Blanchard'. The LAST join is
  refused and the refusal is declared: 'W. G. Blanchard' and 'G. Blanshard' stand in the same
  doorway opposite Dr. Temple's, in consecutive cards that never ran in the same weeks, and **no
  printing in the corpus sets both spellings** â€” so `refused_firm_merges` holds them apart as
  `not_joined` and says what would settle it. Very probably one man; the papers do not say it.
- **The 84 `unplaceable` are untouched and T-0354's second half stays open.** The ruling does not
  reach them and this policy does not extend it; some are outside the plat entirely.
- **Nothing is spent yet.** This is the policy and the allocation. No card, signboard or frontage
  reads it â€” that is T-0263's and the seeding tickets'. No geometry moved and no triangle was added,
  so no bake was required.
- **The renderer smoke was not run and did not need to be.** This branch touches
  `data/research/`, `docs/`, `tools/` and the changelog only; no scene, structure, terrain or
  renderer file changes, and `data/research/` is not published. `tools/check.sh` â€” the dev gate â€”
  is green in full, including its own new step.

---
## Shipped 2026-08-29 â€” T-0380: the New York House stands on Lake Street near Wells

**A building this project had wrongly ruled out now stands in the town.** The New York House sat
on the EXCLUDE list of the first structures dossier on the grounds that "build date not attested in
Andreas". Andreas I p. 635 attests it plainly â€” *"built in 1834 and opened to the public the
following year by Lathrop Johnson and George Stevens, who conducted it until the fall of 1839"* â€”
and that was found on 2026-08-11, when `data/exclusions.json`'s entry was rewritten to say the
exclusion was FALSIFIED and would stay "only until a structure record replaces it". It waited
eighteen days. `data/structures/new_york_house.json` is that record, and the entry has moved from
`excluded` to the watch list, which is the category it has actually belonged to since.

**The opening month is answered from the other side.** Andreas gives no month, so on Andreas alone
whether the house was open on the scene date was an argument. The Chicago American of 13 June 1835
carries two men advertising offices AT the house â€” Dr J. B. Barnard, physician, "at the New York
House, Lake street" (p. 3 col. 3), and J. C. Bradley, a travelling dentist, "his office at the New
York House, where he will remain until after the Land Sale" (p. 3 col. 2, repeated 1835-06-20).
Both are carried on the record's `occupants` with their claims, and both readings are
transcription-mediated under the owner's ruling of 2026-08-28.

**What this unblocks.** "The New York House" is an anchor in the American's advertising, and
`tools/compile_register.py` refused two placeable businesses with the same sentence â€” *"The anchor
'the New York House' names nothing the committed town holds."* Rebuilt against the committed town
it resolves both: Bradley matches the house's occupants, and Barnard's placement now names
`new_york_house` as its landmark. That is why T-0306 was split; the remaining pieces are T-0381
and T-0382.

**What is unverified, stated plainly.**

- **The side of Wells is not evidence.** Andreas says "near Wells" and Wells has two sides. The
  house stands on the free Wells-end lot of `blk_south_water_franklin`, west of Wells, because
  that lot is empty while the eastern block's Lake face already carries three dealt roofs â€” a
  reason about this dataset, recorded at **L209** and carried as the watch-list entry's own
  question. The corner is refused in writing: the source says *near*, not *at the corner of*.
- **The form beyond two storeys and eaves-to-the-street is the type talking**, claimed at **L208**:
  the 40 Ã— 25 ft plan is the dataset's stock period rectangle, and the paint, pitch, bays, gallery
  and two stacks are the archetype's.
- **The desktop viewport of the renderer smoke was NOT run.** `docs/PIPELINE.md`'s dev gate is
  `tools/check.sh` and this suite is dispatch-plus-one-path; desktop part 4 alone exceeded the
  ten-minute ceiling on a single foreground command on a loaded runner, and the run had no room
  for the ~25-minute crawl. **Mobile was run in full, all nine parts, against the published
  mirror, and is green** â€” mobile is the release gate. Desktop part 4 also carries a standing red
  on `dev` from before this branch (`tools/dev-smoke-state.json`, 2026-08-28: the light tier's
  80-call floor at Lake and Market).
- **`tools/check.sh` is green except for the seven failures `origin/dev` already carries** â€” the
  cross-street faces, `blk_washington_clark` standing off the modelled ground, the southern
  coverage reading and three far-timber census lines. Measured on an unmodified `origin/dev`
  worktree in this run: the same seven, and no others on either side.

**Three census lines in the suite moved with the data and were updated in the same commit**, which
is what each of their own comments asks of a run that moves them: the frontage layer's post count
(15 â†’ 16), the hitching posts (14 â†’ 15, twelve at the street edge â†’ thirteen â€” a documented public
house qualifies for a post under T-0194's rule), and the Evidence panel's open questions (3 â†’ 4,
with the card's in-scene set going from one beside the Western Hotel to two).

---
## Shipped 2026-08-29 â€” T-0383: the saddlery at Lake and Canal is S. B. Cobb's alone

**The board on that shop lettered a partnership the same corpus says was dissolved four and a half
months before the scene date.** `goss_cobb_saddlery` was built in August 2026 from one advertisement
â€” the *Chicago Democrat* of 26 November 1833, "they have opened a shop in this village, on the
conner of Lake and Canal-streets" â€” and its own `documented_range` note closed by naming what would
move it: *"further issues of the Chicago Democrat or the Chicago American. One line of an 1834 or
1835 advertisement would settle the survival and might settle the corner."* T-0261 read the
American's thirteen issues on 2026-08-28. It answers one half of that sentence and refuses the
other.

| what the American prints | claim |
|---|---|
| the dissolution, dated *Chicago, Feb. 18, 1835*, one signature unread | `chicago_american_1835_06_08#c006` |
| the same notice with **OLIVER GOS[S]** now legible | `chicago_american_1835_06_13#c015` |
| *"[S]A[D]DLE, HARNESS & TRUNK M[anufa]c[tor]y. S[. ]B[. ]COB[B] [w]il[l] [c]o[nt]in[ue] the [above business] at his shop"* | `chicago_american_1835_06_13#c016` |
| the same card again, ten days AFTER the scene date | `chicago_american_1835_07_11#c008` |

**Survival is settled and the corner is not.** `documented_range` moves `reconstructed` â†’
`inferred`: four printed dates now bridge the nineteen months the old range carried forward on
nothing, the last of them past 1 July 1835. The cross street is lost in all three 1835 printings â€”
*"Lake anc Amor. streets"*, then no street names at all, then *"corner of Lake and THE Balle"* â€” so
**the building has not moved a metre**, the quadrant guard and the Canal-versus-West-Water doubt
stand exactly as written, and that question stays T-0305's, on the page images.

**What a visitor sees.** The board reads `S. B. COBB / Saddle, Harness & Trunk Manufactory / Lake &
Canal Streets` (2.30 m wide against 2.29, which is the only geometry that moved anywhere in this
change), and the card behind it is headed for Cobb instead of the firm. `occupants` is `attested`
over `chicago_american_1835`; the firm survives in `aka` and in the record's own prose, because the
1833 advertisement is the better-attested of the two facts and deleting it to record the later one
would be a loss.

**`docs/LIBERTIES.md` L78 is REVISED rather than resolved.** It covered three admissions â€” the
range, the footprint and the storey count â€” and exactly one of them has been discharged, so its
`Covers:` line drops `documented_range` and keeps the other two. Moving it to Resolved would have
exempted two live inventions from the gate that checks them.

**Not verified here, and stated.** `dev`'s own gate was red at three steps before this branch
existed â€” the dooryard plantings, the planted poplar rows and the yard goods have all drifted from
their rules since T-0307 moved North Water Street, which is **T-0377**. This diff is red at those
same three steps and no others; none of the three files names this record, this phase or this trade
anywhere in them.

## Shipped 2026-08-29 â€” T-0244: the gate could not see twelve of the fourteen hitching posts

**The geometry was right the whole time and the instrument was blind.** The frontage layer's post
probe in `tools/smoke_renderer.mjs` read `mesh?.geometry` â€” the layer's single shared `frontage`
mesh â€” with a comment saying "the posts live in the shared mesh". That was true on 2026-08-19 and
stopped being true on 2026-08-21, when T-0194 put twelve hitching posts at the town's trading
frontages. A post that names a street is STANDING timber and lands in that street's
`<record>__<street>__standing` chunk, published as a `frontage-chunk` mesh so it culls and casts
with the fences beside it and costs no draw call of its own (T-0069, T-0194). The shared mesh never
holds one. So all twelve reported a max and a min over an EMPTY vertex set â€” `-Infinity` for a
height, `Infinity` for a foot â€” and the Sauganash's two, which its own record stands and which do
fall back to the shared mesh, went on measuring correctly.

**The repair is the resolution rule, not the count.** A post is now found by WHERE IT STANDS,
across every mesh the layer draws, because which mesh a post is folded into is a draw-call decision
that may change again without the post moving â€” the same lesson T-0243's batched wood taught the
tree census two days earlier. Read at both viewports on the published mirror:

| | posts | reading |
|---|---:|---|
| the Sauganash's own record (no `street`) | 2 | 1.300 m against a recorded 1.30, foot 0.000 |
| the street edge (`street` named) | 12 | 1.300 m against a recorded 1.30, foot 0.000 |

Each box holds exactly the 72 vertices of one post's shaft and cap, with one exception stated in
the code: at the Mansion House the board crossing over Lake Street brings its near edge 0.13 m from
the post and lays 15 more vertices in the box. They move neither reading â€” a crossing deck stands
0.06 m over its ground, under the foot the min is looking for and a metre and a quarter under the
head the max is â€” and the 0.4 m box is left alone rather than tightened onto the 0.22 m cap, which
would leave 0.02 m of margin against that same crossing.

**`found` is asserted separately from the heights**, because an empty vertex set fails the height
test too and reads as a post of the wrong height rather than as a post the gate cannot see. That
distinction is what cost this defect two days.

**A second stale number in the same part, and it is the ledger rather than an assertion weakened.**
"the frontage layer lays all five records' walks" expected **83** refusals and `dev` has **84**:
T-0028 opened `blk_lake_franklin`, whose dealt warehouse stands 1.50 m off that lot's frontage line
â€” inside the 3.0 m a street fence needs, so the building IS the street wall and the fence is
refused with a written reason. Nothing else in that line moves: 5 records, 51 walks, 39 crossings,
15 posts, 35 fence runs, 899,148 vertices, no problems. The count carries its reason beside T-0241's,
T-0196's, T-0024's, T-0228's and T-0246's, as each of those did.

**Why both reached `dev`.** `docs/PIPELINE.md`: the dev gate is `check.sh` and nothing else, and
`check.sh` asks whether a record re-derives from its own rule, never whether the renderer draws it.
The renderer smoke is dispatch-plus-one-path on purpose, so a check that only Playwright runs can go
red on `dev` without blocking a merge â€” the same gap T-0242 and T-0243 record for two other layers.

**The visible parcel this unblocks (AGENTS.md Â§ VISIBLE-PROGRESS exemption 3): T-0192**, at the top
of QUEUE.md â€” the cross streets' own frontages get the street edge. It lands in this exact layer and
its demonstration is desktop part 2, which could not be read while two of that part's frontage
assertions were standing red for reasons of their own.

**Gates.** `./tools/check.sh` **PASS**. `node tools/smoke_renderer.mjs --published` stage **2** at
**both** viewports â€” desktop 1280Ã—800 and mobile 390Ã—780 â€” **82/0 each, zero page errors**. The
other standing reds on `dev` are untouched and are their own tickets: T-0243 (the tree stations),
T-0279 (flower heads over open ground), T-0247/T-0249 (the light tier's draw calls), T-0271/T-0223
(`balanced` at the forks).

**Nothing you can see changed.** No renderer, no data record and no geometry was touched â€” only the
harness that reads the geometry back.

## Shipped 2026-08-29 â€” T-0316: the large river warehouse leaves the plat

`tools/reconcile_665.py` dealt **F3, the large river warehouse**, to platted blocks. T-0028 found
it on 2026-08-28 by opening `blk_lake_franklin` and being unable to build the F3 it had been dealt:
sampled against the committed heightfield the nearest water to that block's boundary is **134 m**,
its cargo doors would open onto a residential street and its landing apron would cross a public
one. The stopgap put F3 in `tools/generate_block_infill.py`'s `REFUSED_FAMILIES`, so the recipe
DEFERS the slot with a stated reason (L203) instead of reaching for a shape â€” which keeps the roof
on the books and treats a fault in the DEAL as a fault at the block. Every future platted block
dealt an F3 would have deferred it too.

**The repair is upstream, in T-0213's shape.** A family whose own crosswalk record makes water
access a precondition of the FORM is never dealt to a platted block â€” **at any distance**, because
the constraint is the generator's and not the ground's: `generate_block_infill.py` authors no metre
outside a committed lot polygon inside four platted STREETS, and the wharf and landing ground of
the main stem is placed by `generate_river_wharves.py` against the committed bank, outside that
grid entirely.

**Which families, read off the records rather than asserted.** Two readings of the crosswalk have
to agree or the derive refuses: a keyword scan of `required_variant` and the `variants` line says
which families are even in question (**F1, F3, W5**), and `WATERSIDE_JUDGEMENT` says which of those
the record REQUIRES water for, **quoting that record's own `assumption_note` verbatim**.

| family | requires water | the record's own sentence |
|---|---|---|
| **F3** Large river warehouse | yes | "Landing apron and cargo-door arrangement must follow site access and cannot extend into water or duplicate a counted pier." |
| **W5** Sawmill, boat-repair or riverside shop | yes | "river access requires validated dry-bank terrain contact." |
| F1 Freight or storage shed | no | "Stored goods and dock relationship are not known for anonymous slots; skids belong only where terrain and route access support them." |

T-0316 asked for F1, F2 and F4 to be checked while the run was here. **F2** ("Hoist beam presence
varies; cargo type and operator are not inferred") and **F4** ("Board-stack quantity and open-side
pattern are visual variation, not inventory facts") name no water at all and are not candidates â€”
so the ticket's own guess that F4 "carries the same site logic" is **refuted by F4's record**.
Edit any of those notes, or add a family that names a wharf, and the re-derive fails by name rather
than silently re-classifying it.

**It is a permutation, and that is asserted rather than trusted.** One waterside roof on a platted
block is exchanged for a dry PRINCIPAL roof of the same trade-ness on that district's own unbounded
balance. The re-derive moves exactly one roof today:

```
waterside (T-0316): F3, W5 require water â€” F3 blk_south_water_market -> south_plat_beyond_committed_control for C2
```

No total moves: not the 662, not a district, not a family, not any unit's roof count, and not its
principal/ancillary split â€” each of those is checked in the tool. `blk_lake_franklin`'s own
deferral stands as the record of what happened; the block generator's refusal stays where T-0028
put it, now as a belt rather than the only brace.

**Gates.** `tools/check.sh` green (the full dev gate, including the `reconcile_665.py --check`
re-derive and the changelog contract). `python3 tools/measure_family_deal.py` green â€” 0 refusals,
31 off-band claims, every one already named in `tools/family_deal_baseline.json`, nothing new and
nothing grown. No renderer file, no geometry, no coordinate, no mesh, no bake: the programme
document is not loaded by the walkthrough and is not published.

## Shipped 2026-08-29 â€” T-0243: the two timber gates read a batched mesh, and one of them could never fail

**T-0243.** `tools/smoke_renderer.mjs` stage 7 held two checks on the near-field wood, and
both traversed for `/^timber__/` â€” the four merged quadrant meshes `timber__q0â€¦q3`. T-0223
replaced them on 2026-08-27 with a single `THREE.BatchedMesh` named **`timber`**, and from
that merge the regex matched nothing:

- **`every tree drawn stands at its own station`** went red on its own liveness clause
  (`meshes > 0`), on an **unmodified `dev`**. Every branch cut from dev inherited it and had
  to argue "not mine" â€” measured three times in two days.
- **`no timber is drawn out in the channel`** asserts `offshore === 0`, and an empty
  traversal yields zero offshore vertices. **It passed, green, for a fortnight, having
  asserted nothing at all about the timber.** That is the worse half, and it is the reason
  this ticket was sized as a repair rather than a rename.

**Why a rename would have been the wrong fix.** A `BatchedMesh` holds every chunk in one pair
of buffers with a per-instance transform the batch owns, so
`geometry.getAttribute('position')` read through `matrixWorld` is not a chunk's world
position. `tools/drawn_timber_census.mjs` (new) walks each instance's own geometry range
under its own matrix, through `_instanceInfo` / `_geometryInfo` / `_matricesTexture` â€” the two
structures `getBoundingBoxAt()` and `getMatrixAt()` read, walked in the page so the census
needs no THREE there. It is the same arrangement `drawn_placement_census.mjs` uses for the
building batches, deliberately: the gate and the instrument run ONE census, not two readings
of the same idea.

**It still reads a plain `timber__*` mesh.** Unwinding the batching cannot silently empty the
gate the way landing it did.

**The bars did not move, and the liveness clauses grew.** 24 m is the widest crown's reach
plus its lean; 12 m is a bank willow leaning over the channel; both were argued in T-0110's
box and neither was touched. Both now come back FROM the census (`strayBarM`, `offshoreBarM`)
rather than being written a second time in the gate. And `chunks > 0 && verts > 1000 &&
unreadable === 0` guards **both** checks now â€” the offshore half had no liveness clause at
all, which is precisely how it passed on nothing.

**And it is demonstrated to fail.** `tools/measure_drawn_timber.mjs --refute` displaces two
chunks of the live scene â€” one mirrored across the datum's east-west line (R-BUG5b's own
fault, applied to the chunk standing furthest from that line, because a chunk on the line is
its own mirror), one translated to a point the terrain mask calls water more than 16 m from
any bank â€” and requires the census to report each. Clean run, source tree, 1280Ã—800:
**152,792 vertices across 70 chunks in 1 batch against 881 stations, 0 stray (worst
measurable 15.4 m), 242 over water at all and 0 offshore.** Broken: **3,140 stray** (3,118
beyond the station hash) and **1,099 offshore**, worst 24 m. A gate this shape is believed
because it can be made to fail, not because it is green.

**What this does not do.** It repairs neither T-0244 (the twelve hitching posts draw no
vertices the gate can find) nor T-0265 (the sward census at a phone). Those are the other two
standing reds and they are their own tickets. *(T-0244 closed 2026-08-29 â€” the top section of
this file; the posts were drawn all along and the probe read one mesh of the layer's several.)*

**Nothing you can see changed.** No renderer, no data record and no geometry was touched â€”
only the harness that reads the geometry back.

## Recorded 2026-08-29 â€” T-0328's tail: the reading gets its dossier, and coverage.json stops saying 56

**T-0328 shipped in PR #510** â€” D. Weaver's building is on **Lot 2**, block 1, North Water
street, on four printings against one. The notice turned out to be a standing advertisement
running in five consecutive numbers; three of them (1834-11-26 c010, 1834-12-03 c025,
1834-12-10 c012) had never been claimed by any reading pass, and all three set Lot 2. No
transcription was amended to reach it, which is the rule T-0294 was keeping when it claimed
both disagreeing printings and edited neither.

**This entry is what that merge left behind**, and both halves are record hygiene rather than
new reading:

- **`coverage.json` was asserting a count that had stopped being true.** The December 1834
  range said *"Four issues, read through, 56 claims"* and *"none of the 56 claims is counted
  unresolved"*. The month holds **60**. Counted per commit rather than re-asserted: 56 at
  `103168a0` (T-0294), 57 at `26f03456` (T-0339), 58 at `c49d8fa5` (T-0330), 60 at `5c638546`
  (T-0328). The range now says so, and says the later four are machine-checked on `dev` like
  the original 56. The November range records its own addition and â€” the part worth keeping â€”
  **why the read missed it**: the notice stands in the alternating pair of physical columns,
  surviving as every other line, which is the shape that month's reads found hardest. That is
  a fact about the instrument and it belongs where the next reader of the month will see it.
- **`docs/RESEARCH/weaver_building_north_water_block_1.md` is new.** AGENTS.md Â§ Honesty
  rules requires a dossier where sources disagree; the reading was made and defended in the
  claim notes, which is where a reader of that claim finds it and nowhere else.

**The dossier also states what the ticket's own premise got wrong.** T-0328 rested on "2 and
9 are not a confusable pair in clean type". True, and the conclusion followed â€” but this type
is not clean: the same advertisement's copy dateline is set **12, 12, 13 and 19** across the
five weeks. The reading stands on the count of independent settings, not on any one column
being trustworthy. **T-0350** carries the dateline.

**Still `transcription_mediated`.** The acceptance asked for the digit off a page image; the
deposit holds transcriptions only, and no scan has been read. Written down rather than
passed over.

**Nothing you can see changed**, and no claim, quote, gazetteer entry or geometry was
touched â€” only the two records that describe what was read.

## Shipped 2026-08-29 â€” T-0262: the scene-date register, and what the papers can actually do to the town

**`tools/compile_register.py` turns the gazetteer into a work list.** The gazetteer is an index of
what was PRINTED â€” 1,094 claims out of 82 issues, 221 businesses, 2,201 people. It says nothing
about what the model should build. The register does: for every business an ACTION against the
committed town, for every person whether the town already holds them. It is derived, wholly, and
`check.sh` re-derives it and refuses a committed copy a rebuild would not produce â€” the same
contract `gazetteer.json` is under, for the same reason.

**Ruling 3 gains the word BEFORE.** `built_at_scene_date` in the gazetteer is `not contradicted_by`,
whatever the contradiction is dated, which struck a firm out of a July town on the strength of an
August dissolution notice. Here the veto is a contradiction dated ON OR BEFORE 1835-07-01. A later
one is recorded â€” `dissolved_after_scene_date`, one business â€” and disobeyed.

**The ticket's second exclusion was a proxy, and T-0356 replaced it with the field.** T-0262 asked
to exclude entries whose only 1835 evidence `announces_opening` after 1 July. There was no
`announces_opening` in the claim vocabulary â€” except as a bare `true` on twenty claims that no tool
read â€” so the register used the derivable proxy `first_evidence_after_scene_date`: a business whose
FIRST issue postdates the scene date evidences nothing about 1 July. Thirty-eight businesses by the
time the corpus was fully read.

**The re-read settled it, and the proxy was excluding houses the papers put in the town.** The
claim now carries `{verbatim, dating, iso, note}` and the DATING decides: a `stated` future opening
after the scene date excludes; an `effected` one is dated by the advertisement's own dateline and
bounds the opening from ABOVE, so it never excludes; an `undated` one decides nothing. Four of the
thirty-eight genuinely announce a later opening and stay out â€” Cromelien's wine branch (14 Aug),
Everts' high school for young gentlemen (10 Aug), Hunt's for young ladies (17 Aug), Lyon's
wholesale grocery (1 Sep). **Thirty-four are restored**, and five of those are printed standing in
the July town: Wm. H. Taylor's boot store over a dateline of 8 JULY 1834, Wm. H. Kennicott saying he
had practised dentistry here "for the past year", Samuel Lewis's music-school copy dated 22 June,
S. Abell's 24 June and John Holbrook's 10 June. The register's placeable count moves from 66 to 78
and its street-only count from 47 to 63.

**What replaced the proxy is not nothing.** A business first printed in August that announces no
opening now stands under ruling 3, and that is a liberty: `backdating_liberty_required`, the
forward twin of `survival_liberty_required` â€” documented only after the scene date, present on it
by assumption. Thirty-three businesses carry it, computed and never asserted. `docs/LIBERTIES.md`
carries neither class yet (T-0357 is the survival half, T-0404 the backdating half).

### The counts, which are the epic's yield measured

| businesses | 221 |
|---|---|
| present at the scene date | 190 |
| excluded â€” contradicted before 1835-07-01 | 14 |
| excluded â€” first evidence after 1835-07-01 (the proxy T-0356 retired) | 17 |
| `enrich_existing` (a committed building already carries it) | 39 |
| `new_building` (placeable against the committed town) | 24 |
| `street_only` (a street face and no closer) | 49 |
| `unplaceable` (no street the model holds) | 109 |
| standing on a survival liberty (last evidence pre-1835) | 129 |

| persons | 2,201 |
|---|---|
| `enrich` â€” already in `data/residents/` | 117 |
| `replace_invented` â€” a documented person of an invented household's trade | 113 |
| `new_resident` â€” ruling 1 | 1,971 |
| â€¦of those, known only from the letter lists | 1,555 |
| **invented households the register can retire** | **28 of 117** |

Those are the figures the epic landed on, and they are kept as landed. **Re-measured on
2026-08-29, after the whole corpus was read and after T-0356 replaced the proxy exclusion
with the field**, the same register reads:

| businesses | 242 |
|---|---|
| present at the scene date | 224 |
| excluded â€” contradicted before 1835-07-01 | 14 |
| excluded â€” opening announced after 1835-07-01 | 4 |
| `enrich_existing` | 38 |
| `new_building` | 30 |
| `street_only` | 63 |
| `unplaceable` | 111 |
| standing on a survival liberty (last evidence pre-1835) | 126 |
| standing on a backdating liberty (first evidence post-scene-date) | 33 |

| persons | 2,628 |
|---|---|
| `enrich` | 184 |
| `replace_invented` | 119 |
| `new_resident` | 2,325 |
| **invented households the register can retire** | **27** |

The retirement figure is a count of HOUSEHOLDS and it is capped per trade by construction: three
documented tailors retire at most the tailors the town invented. Reporting the matched persons
instead would report 113 people retiring 117 households, which is a number about nothing. The 28
are 4 blacksmiths, 4 grocers, 4 tavern keepers, 3 shoemakers, 2 joiners, 2 tailors and one each of
baker, butcher, cooper, dentist, harness maker, hotel keeper, merchant, painter and physician.

### Matching a firm to a building is a different question from matching a firm to a firm

The first cut of `enrich_existing` claimed 58 buildings and a good many of them were wrong, in four
distinct ways. Each is now a guard with a self-test on the case that forced it.

1. **A `proprietors` entry is routinely a whole firm style** â€” `Clark, Filer & Co.`, `H. Doty & Co.`,
   `Kinzie & Hall` â€” and taking its last word for a surname reads those three firms as `co`, `co`
   and `hall`. Two of them then matched Daniel Elston's soap works, whose occupants line ends
   `& Co.`. The partners now come from the gazetteer's own firm policy (`firm_surnames`, T-0304).
2. **A surname is not a person.** The Kinzie brothers are one surname and three businesses; matching
   on `kinzie` put R. A. Kinzie's store inside J. H. Kinzie's. Where the RECORD prints a forename
   and the PAPER prints one, they must now agree â€” and two spelled-out forenames must agree whole,
   not by initial, because `John S. Kinzie` and the James Kinzie House share a `j`. The test is
   asked of the whole record, not of the field the surname was found in, or a disagreement simply
   routes round the guard by dropping to the next tier.
3. **An `aka` is where a record keeps its loosest descriptions.** `Taylor's tavern` is a real second
   name of the Wolf Point Tavern and W. H. Taylor's boot and shoe store is a different Taylor, so
   an aka match now also requires the trades to agree. And an aka that locates a building by
   ANOTHER building â€” `the cabins near Wentworth's tavern` â€” is cut at its locative word, which is
   what stopped Elijah Wentworth's tavern on Flag Creek matching a row of log cabins at Wolf Point.
4. **An anonymous reconstructed roof cannot ALREADY carry a documented business.** `recon_*` and
   `inf_*` are excluded outright. Putting a documented firm into an invented roof is a decision
   T-0263 makes deliberately, with the adoption written down; making it by string match is how an
   invention gets laundered into the documented layer. `Kinzie Hall` had matched
   `recon_1835_north_i2_015` on the word "hall".

5. **A word in the record is not a surname in the record** (T-1042). The pools these guards back
   are word SETS, so any capitalised word in a building's prose could satisfy a required surname:
   `S. Dewey`, a joiner, matched Dr Elijah **Dewey** Harmon's log cabin on a middle name. Where the
   paper prints a forename for the surname, the record must now print that surname AS a surname.
   The same reading had been losing a match the other way â€” a generational tag reads as a
   capitalised word, so `John Bates Jr.` left `bates` in no surname position at all and `J. Bates,
   jr.` read as a man whose forename was Jr. Both of the auction-store notices now reach
   `bates_auction_room`.

Every surviving `enrich_existing` carries the tier it matched on and the exact text it matched
against, so T-0263 can argue with a proposal without re-running anything.

**The reading itself has ONE home** (T-1042). `compile_gazetteer.surname_words()` answers "which
words of this proprietor string are surnames", and `firm_surnames()`, `adopt_street_faces.surnames()`
and `replace_invented_residents.street_face_stands()` all read it instead of each taking a string's
last word. The two outside this file used to invent a man â€” `H. Doty & Co.` and the five printings
of `J. L. Wilson & Co.` each yielded `co`, and the street-face table stood somebody called Co on
three streets â€” and to lose one, since `Clark, Filer & Co.` yielded `clark` alone. Eighteen of the
198 register businesses read differently for it; no adoption moved, and the table now carries its
own `surnames` rather than leaving the household pass to guess at them a third time.

### A name is not always one building, and the anchor path used to pretend it was

`resolve_anchor` reads the landmark a paper prints â€” "David Carver's Old Stand", "west of J.
Wright's" â€” against the committed town, and until 2026-08-29 `match_landmark` ended
`return sorted(hits)[0] if hits else None`. Where two committed records answered to one name it
took whichever id sorted first and the register wrote *"The landmark is the committed structure
X"* over it. Nothing in the file said a second record had answered to the same name; an
alphabetical tie-break came out looking like a reading.

**Thirty-five identity-word sets in the committed town are held by more than one record**, and the
figure is derived on every build â€” `compiled_from.structures_sharing_a_name` in the register, and
`tools/check.sh` prints it. Twenty-eight are anonymous count-units, where the collision is a
consequence of naming a roof "Reconstructed 2-room frame cottage 02" and no advertisement will
ever print it. **Seven are named landmarks a paper could name, and would:**

| the name | the records it answers to |
|---|---|
| `pier`, `harbour pier works` | `north_pier`, `south_pier` |
| `branch bridge`, `branch bridge first over` | `north_branch_bridge`, `south_branch_raft_bridge` |
| `house school watkins` | `north_side_school_1833`, `watkins_school_house` |
| `crossing slough water` | `north_water_slough_crossing`, `slough_log_bridge` |
| `building john let wright` | `wright_building_to_let_a`, `wright_building_to_let_b` |

The Wright pair is the case T-0386 is blocked behind and the clearest of the seven: one
advertisement, two buildings to let, one proprietor's name, and the only thing separating the two
records is the *(east)* / *(west)* this project added â€” which `words()` drops as a stop word, so
the two are one name to every reading pass that will ever run. `north` and `south` are stop words
for the same reason, which is why the piers and the branch bridges collide too.

So the anchor now has a **sixth kind, `ambiguous`**: the name was recognised, the town holds it
more than once, and the register refuses rather than picks â€” naming every rival in the note. It
never places; a business whose anchor is ambiguous falls to `street_only` or `unplaceable` on the
street the paper printed, exactly as an unresolved one does. The same refusal guards the one-hop
business match below it, because the corpus prints one house under more than one heading.

**No placement in the register moves today**, and that is the honest measure of this change: zero
of the 209 businesses print an anchor that lands on one of the thirty-five. It is a guard against a
fabrication rather than the repair of one â€” and the thing it guards is live, because the moment a
reading pass widens enough to see past a project-added disambiguator, "J. Wright's" resolves onto
two records and the old code would have picked the east one.

### The T-0257 fixtures, as the acceptance requires

`business_j_s_c_hogan` â†’ `enrich_existing`, target `hogan_store`, matched on the record's own name.
`business_peter_cohen` â†’ `street_only`, target `south_water`: the paper's anchor is "the east end of
South Water-street", which the register resolves as a REACH of a platted street â€” a real resolution
and not a placement, so it reads as its own anchor kind rather than as a failure.

### What is honestly not settled

- **One reading pass is still open.** T-0297 (August 1835, the four issues AFTER the scene date) was
  in flight in a sibling run when this was built. The register is deterministic and re-derived by
  the gate, so `--build` after that merges refreshes it; the counts above are as of the gazetteer on
  `dev` at 2026-08-29.
- **`wolf_point_tavern_stable` still takes Elijah Wentworth's Flag Creek tavern**, on an occupants
  line that reads "Elijah Wentworth in 1831, William Walters on the scene date". The match is on a
  HISTORICAL occupant of a building whose scene-date occupant the same sentence names. T-0355.
- **78 businesses stand at the scene date and are placeable nowhere.** That is the size of the
  problem the seeding tickets do not solve, and it is a fact about the papers, not about the tool.

Filed with the register in hand: **T-0354** (the `street_only` and `unplaceable` policy â€” 49 and
78), **T-0355** (the historical-occupant match), **T-0356** (`announces_opening` as a real claim
field rather than a proxy) and **T-0357** (the 129 survival liberties `docs/LIBERTIES.md` does not
yet carry). All PAPERS, all appended to the bottom of QUEUE.md â€” the owner orders it.

## Shipped 2026-08-29 â€” T-0283: the North's freight row is repaired, and the fault was a split fault

**The row allowed the North Division ONE freight roof and seven stand there.** T-0211 found the
breach on 2026-08-28, declared it as a ratchet so it could not grow, and deliberately did not repair
it: repairing it is a decision about the authored target, and the cells sum to their division's
target AND to their group's total, so no cell moves alone.

**The decision, and it is narrower than the ticket feared.** The town-wide freight total is
contradicted by nothing â€” twenty are authored, twelve stand. What is wrong is WHERE the programme
put them. So the repair is a split repair, four cells wide:

| group | division | was | now |
|---|---|---|---|
| `warehouses_freight` | north | 1 | **7** |
| `warehouses_freight` | south | 17 | **11** |
| `ordinary_dwellings` | north | 90 | **84** |
| `ordinary_dwellings` | south | 170 | **176** |

Both row totals stand (335 and 20), all four district targets stand (365 / 135 / 152 / 10),
`family_targets` is untouched and `roof_total` is untouched. Nothing that stands moves; no mesh
changes; the 662 roofs are the same 662 roofs, re-typed.

**Why the South pays and no one else.** Six of the North's seven freight roofs are documented
pre-existing records â€” Kinzie & Hunter's warehouse, the four north-bank sheds at the Dearborn reach,
the north-side brickyard â€” and the seventh, `recon_1835_north_f1_022`, was dealt by a parcel that ran
before anything measured this. Against them the South's freight cell holds seventeen authored slots
of which five stand: twelve are unbuilt and unnamed. **An authored slot yields to a documented
record** â€” the principle T-0032 established when it held the institutional row to the named census â€”
and the South's cell is the only one that can pay without moving a group total or a division target.
The compensating `ordinary_dwellings` swap is what keeps each division's own column on its target.

**What it costs, stated rather than clamped.** The South is scheduled six fewer warehouses (freight
remainder 12 â†’ 6) and six more ordinary dwellings (72 â†’ 78), and its business-front re-deal now moves
7 trade roofs where it moved 9. The North's remainder does not move by a single roof â€” but it stops
being scheduled seven houses short for a reason nothing anywhere stated:
`reconcile_665.py`'s clamp shed **7** slots from north `ordinary_dwellings` before this and sheds
**1** after. That last one is L93's anonymous school, which is not an authoring fault at all â€” it is
`measure_group_district_rows.py` and `measure_institutional_claims.py` reading one liberty
differently â€” and it moves when the liberty is retired, not before.

**The gate lost its declaration and gained a case.** `("north", "warehouses_freight")` is RETIRED
from `DECLARED_OVERSHOOT`, not lowered, and a new self-test case asserts both halves of that â€” the
row is not over AND it carries no declaration â€” because either half alone passes vacuously. The
three ratchet cases used to drive the freight declaration; a declaration of size 1 cannot fall
without disappearing, so `overshoot_findings` now takes the table it reads and the self-test hands it
a synthetic one. `--self-test` is nine cases green. The argument lives at
`district_group_matrix_note` in `data/reconstruction/1835_building_inventory.json`, beside the
`roof_total_note` that records the only other time a count in that file moved.

## Shipped 2026-08-28 â€” T-0028: `blk_lake_franklin` opens, and the warehouse it was dealt is refused rather than massed

**The first NEW platted block this programme has opened since 2026-08-23**, when T-0028 re-derived
the schedule with `tools/reconcile_665.py` and found there was nothing left to open: eleven blocks
`at_capacity`, six `open` but only on lots that already stand (T-0143's core density, a different
ticket), one `reserved`, and two `gated` on street control. That run filed T-0163, which landed on
2026-08-24, split the two refusals apart and measured them â€” and did NOT open a block. It found
`blk_south_water_clinton` was never a block at all (`never_platted`, 328 m away with 20 of 66
samples wet â€” opposite banks) and escalated `blk_south_water_market` to T-0183, where it still sits
`blocked-owner`.

**What reopened the programme was the DEAL, not control.** `blk_lake_franklin` â€” Lake, Wells,
Randolph, Franklin â€” has stood `open` with two free lots throughout. T-0188 read it on 2026-08-27
and recorded that it *"cannot carry a three-unit run as dealt"*, because the schedule dealt it
**I3**, which `generate_block_infill.py` refuses by name, alongside **F3**. T-0213 weighted the
trade families onto the business front on 2026-08-26; the I3 went with it. Re-derived today the
deal is A1, D1, D5 and F3 â€” three of four buildable â€” so the block opens.

**The arrangement is measured on both rules, and they agree.** `tools/measure_street_frontage.py`
counts 16 documented records and 8 inferred households within 25 m of Lake Street's committed
centreline against Randolph's 7 and 7 (the reconstruction column is this programme's own output and
does not vote), so Lake is the business face. `tools/measure_end_rule.py` puts lot 4 at 441.12 m
from the foot of the Dearborn Street drawbridge against lot 7's 473.20 m straight, 550.45 m against
668.96 m walked. So the free Lake lot takes the row, the free Randolph lot is left open, and inside
the run the better roof stands at the east end nearest the crossing: a deep-plan frame cottage
anchored 1.5 m off the lot's east margin, an older log dwelling abutting west of it on one party
wall, and the stable in the same lot's yard at the alley end.

**The street line was not adopted â€” it agreed, and that is worth recording.** This face carried no
frontage-declaring record before the run, so there was no built line to adopt under T-0104 and the
floor is the plat module's own 1.5 m lot margin. `temple_lake_st_building`, a documented record
placed by an entirely different parcel that declares no frontage, stands 1.492 m off the same face
at 75.73â€“82.52 m along. The run stands at 1.499 m and stops 3.90 m short of it. Seven millimetres,
by coincidence of the data rather than by anything this parcel chose. `tools/measure_street_line.py`
now reports nine block faces and every one of them is one street line.

**THE FOURTH ROOF IS REFUSED, AND THE REFUSAL IS THE FINDING.** F3 is the "Large river warehouse".
Its crosswalk entry makes water access a precondition of the FORM â€” required variant
`warehouse_river_large`, variants *"multiple cargo doors; landing apron; sparse glazing"*,
assumption note *"Landing apron and cargo-door arrangement must follow site access and cannot
extend into water or duplicate a counted pier."* This generator authors no coordinates: every metre
comes from a committed lot polygon inside a block bounded by four platted STREETS. Sampled against
the committed heightfield `e1834_harbor_cut`, the nearest water to this block's boundary is
**134 m**. So F3 joins I1, I2 and I3 in `REFUSED_FAMILIES` â€” for the opposite reason to theirs, and
the module comment now says which is which: the institutional families are refused for what an
anonymous one would CLAIM, F3 for the GROUND. The slot is deferred in the recipe with its reason
and the roof stays on the books.

**That is a stopgap and it is filed as one.** Treating a fault in the DEAL at the block means every
future platted block dealt an F3 will defer it, and three warehouse roofs will pile up as deferrals
nobody is scheduled to build. **T-0316** asks the deal to stop sending them inland, in the same
shape as T-0213 â€” and notes that F3 is absent from the generator's `FUNCTIONS` table and from the
`block` arm of `measure_family_deal.py` too, so the deal was reaching for a family the parcel shape
has never been able to name.

**Numbers.** 3 roofs (2 principal, 1 ancillary) of the block's 4 of headroom; 341 buildings standing
of 662; the block goes to 14 standing, 1 of headroom, 1 free lot. No roof is added to the town â€” the
three come out of `south_plat_beyond_committed_control`. Baked with `bake.sh --only` per structure;
`tools/check.sh` and `tools/smoke_renderer.mjs` green. Liberty **L203**. T-0028 closes on this one block
with its successor **T-0317** filed, which is what its own sizing note asks of every run: one run,
one demonstration, one successor.

## Shipped 2026-08-28 â€” T-0246: the log jail comes onto the plat, and Randolph's walk reaches its corner

**The fault is the modern-kerb read, for the fourth time.** `log_jail` was placed on 2026-08-11
from Andreas's *"northwest corner of the court-house square"*, and the square's four inside corners
were computed for that parcel from **modern OpenStreetMap intersection centres** stepped 12.2 m into
the block. That is the same derivation T-0127 found under the eleven South Water records and T-0196
found under Lake Street's four. Measured against this project's own committed line â€” the
`data/streets/1835.json` centreline offset by half the committed 80 ft corridor, which is what
`tools/generate_plat_lots.py` builds every block edge from â€” the jail's north wall stood **3.48 m
out past `blk_randolph_lasalle`'s Randolph frontage**, with its centroid inside the corridor.

**What it cost, and the second half was not obvious.** `tools/generate_frontage_works.py`'s march
refused the two steps of the square's own Randolph walk that the jail covered, 0.0 to 10.4 m along
the face. A walk refused short of its corner then takes the corner **crossing** with it â€” the rule
lays a crossing only where both walks reach the corner â€” so the LaSalle Street crossing at Randolph
was refused in turn, *"the two walks stop 34.8 m apart"*. One misplaced building was costing 10.4 m
of boards **and two board crossings**.

**The repair is this record's own method run against this project's own line.** The footprint is
translated **4.981 m** along the face's inward normal â€” dE âˆ’0.040, dN âˆ’4.981 in local ENU, so
UTM E 447538.25 N 4637126.21 becomes **E 447538.21 N 4637121.23** â€” which leaves its north wall
**1.50 m** back from the committed frontage line. The square is not subdivided, so there is no lot
line to stand off: 1.50 m is `plat_occupancy.LOT_MARGIN_M`, the plat module's own margin off a
boundary, and it is the same figure every reconciled South Water and Lake record took.

**Nothing along the street moved and no grade changed.** The along-face position, the block, the
corner and the side are untouched; the confidence stays `inferred`, because re-deriving a coordinate
from better geometry is not new evidence. The record's own 20 m working uncertainty from the
georeference is unchanged and is four times this move â€” so this reconciles two of this project's own
lines and does **not** claim to have located the jail better. The facade bearing stays 0 while the
face runs at 0.46Â°, which leaves the front wall between 1.50 and 1.55 m back across its width;
rotating a documented record is a second claim and this is a repair.

**Measured, before â†’ after.**

| | before | after |
|---|---:|---:|
| `log_jail` lap of the Randolph corridor | 3.48 m | none |
| placed phases lapping a platted corridor | 20 of 349 | **19 of 349** |
| in the DEEP mode (â‰¥ 3.48 m) | 6 | **5** |
| records lapping Randolph | 2 | **1** |
| `blk_randolph_lasalle` north walk | 10.4 â†’ 99.0 m of the face | **0.0 â†’ 99.0 m** |
| its walking decks | 6 | **7** |
| street edge, walk/crossing runs | 88 | **90** |
| street edge, walk laid | 3,160.3 m | **3,170.7 m** |
| street edge, crossings | 34 (811.0 m) | **36 (857.5 m)** |
| street edge, refusals stated | 84 | **83** |

The two new crossings are `blk_randolph_wells_north_crossing_blk_randolph_lasalle_north` (over
LaSalle Street) and `blk_lake_lasalle_south_crossing_over_randolph` (over Randolph). No refusal was
added, and no run was lost.

**What is left on Randolph, and it is not this fault.** One record still laps it:
`newberry_dole_slaughterhouse_south_branch`, 11.45 m in at the far west end, whose body is drawn
toward the street from its own anchor (K30(b)). Nothing here touches it.

**One earlier reading is now stale by five metres.** T-0224 fixed the `public_square` critic stand
by bisecting the estray pen and the log jail, and quotes the jail at **131.2 m off at 319.9Â°**. With
the jail reconciled it is **127.2 m at 320.2Â°** from the same stand. The bisector moves by 0.15Â°,
which is far inside the frame, and the stand was **not** re-derived here â€” the number is recorded as
moved rather than silently left reading as though it had not.

**The smoke's frontage census moved, and it is the ledger rather than an assertion weakened.**
`tools/smoke_renderer.mjs`'s "the frontage layer lays all five records' walks" carries a running
count with the reason for each move. Crossings 37 â†’ **39** and refusals 84 â†’ **83**; walks, posts
and fence runs do not move, because the returned steps EXTEND an existing run rather than opening
a new one. The comment says so, as T-0241, T-0196, T-0024 and T-0228 each did before it.

**Gates, and one of them is red â€” inherited, and one number is mine.** `tools/check.sh` **PASS**
(after `generate_yard_goods.py`, `compile_scene.py --all` and
`measure_corridor_intrusion.py --write-baseline`, which is the ratchet's own way to bank a repair).
`node tools/smoke_renderer.mjs --published`, run in staged legs at **both** viewports â€” mobile
390Ã—780 (1-2, 3-4, 5-6, 7-9) and desktop 1280Ã—800 (1â€¦9) â€” **zero page errors** anywhere. Every red
is on `dev` before this branch, each named to an open ticket:

| leg | red | whose |
|---|---|---|
| mobile 1-2, desktop 2 | twelve street-edge hitching posts measure `-Infinity` | **T-0244** â€” byte-identical to `dev`'s own standing record (`dev-smoke-state`, 2026-08-28T10:27) |
| mobile 7-9, desktop 7 | the tree-station assertion reads 0 of 0 vertices | **T-0243** â€” byte-identical to `dev`'s standing record |
| desktop 7 | 2,526 of 18,911 flower heads over open ground | **T-0279**, to its own figure |
| desktop 4 | the `light` tier draws 85 calls against its 80-call floor | **T-0247/T-0249** â€” **85 on a clean `origin/dev` worktree too**, so not this branch (`dev`'s stored 83 is a stale tree) |
| desktop 4 | `balanced` over its ceiling at the forks | **T-0271/T-0223** â€” and **1,160 triangles of it are mine** |

**The one number this branch moves on a red gate, stated rather than buried.** Measured on a clean
`origin/dev` worktree and on this branch, same stand (the forks, from Wolf Point), same command
(`SMOKE_VIEWPORT=desktop SMOKE_STAGE=4 node tools/smoke_renderer.mjs --published`). Re-taken after
this branch merged `origin/dev` at **`363d920b`**, so the comparison is against the base it lands
on and not the one it left; both readings were identical before and after those five commits:

| | clean `origin/dev` | this branch | delta |
|---|---:|---:|---:|
| `balanced` at the forks | 1,214,417 | **1,215,577** | **+1,160** |
| over the 1,210,000 ceiling by | 4,417 | **5,577** | +1,160 |

That is 10.4 m of plank walk, two board crossings and one more walking deck, at the street edge's
measured 42.8 triangles a metre. **The ceiling was already breached and it is not breached by this**
â€” but T-0223's complaint is precisely that content lands while the budget is over, so the increment
is recorded here rather than left for the next reading to discover. It was merged anyway on three
grounds: the dev gate is `check.sh` and nothing else (`docs/PIPELINE.md`), the breach is
owner-acknowledged and carried by four open tickets, and the alternative is leaving a documented
building drawn standing in a platted street. Nothing was weakened to pass.

**No bake.** The position lives in the sidecar the renderer reads, not in the mesh, and
`validate.py --stale` stayed green across the move.

**One side effect, and the rule is right.** `data/yard/town_trade_goods.json` re-derives with one
fewer wagon: `town_wagon_lasalle_2` stood on the verge the new LaSalle crossing now occupies, and
the yard rule refuses it â€” *"A footway is a floor and a wagon parked across it is the town's own
Ordinance 9 complaint, drawn."* 64 wagons to 63, and the refusal states itself.
## Shipped 2026-08-28 â€” T-0254: the North Water Street slough crossing, and the street west of it

**T-0226 left the North Division's river front with no roadway west of E +240 and said so.** It had
re-derived North Water Street from the committed north bank after finding 477.4 m of the old line
inside the water mask, and it stopped the derived line on the east shoulder of the attested
north-side slough because `renderers/web/js/streets.js` may not paint a ford â€” R-BUG4. The reach
west of that, to the North Branch, waited on a crossing record. This is it.

**The crossing.** `north_water_slough_crossing`, `bridge_timber`, a 12 m deck 3 m wide laid square
at local **E +183 .. +195, N +156 .. +159**. Reconstructed throughout; nothing records it. Measured
by `tools/measure_slough_crossing.py`, which now reads all three of the town's crossings:

| | open water under the deck | dry seats | walk | clearance |
|---|---|---|---|---|
| Slough Log Bridge, Water St | 3.30 m of 8.00 | 2.35 / 2.35 m | 0.83 m | 0.50 m |
| La Salle Slough Crossing | 5.55 m of 12.0 | 3.10 / 3.35 m | 0.84 m | 0.50 m |
| **North Water St Crossing** | **6.65 m of 12.0 (55 %)** | **2.60 / 2.75 m** | **0.68 m** | **0.35 m** |

**The clearance is read off the abutments, not borrowed.** The committed heightfield stands at
+0.63 m where the deck's west end lands and +0.73 m where its east end does, over a 0.00 m water
surface, so a walk surface at 0.68 m lies within 0.05 m of both banks. That is why this crossing
needs neither the graded cut its eldest sibling needed nor the fill the La Salle one did: no
approach entry was added to `terrain_spec.json` and none is wanted. Its two siblings' 0.50 m came
from the hydrology dossier's conjectural thalweg; this one's came from ground that can be measured.

**Where the deck goes, and why not on the old street line.** This slough is a **68.5 m funnel**
where it meets the main stem, narrowing to 32.4 m at N +130 and 16.2 m at N +140, with a **2.5 m
sill 0.18 m deep** at N +147.5â€“150 and a steady **5â€“7 m channel** above it. A crossing on a straight
river-front line would span 20 m of water 1.54 m deep â€” a river bridge, and the town built two of
those and remembered both by name. So the street goes round the head of the bay, as a bank road
does, and crosses where the stream is six metres wide.

**The street.** `tools/derive_north_water.py` now derives TWO reaches with the structure between
them â€” east from the deck at E +195 to E +830, west from E +183 to the North Branch at E âˆ’30 â€” and
each reach's smoothing window is clamped inside itself, because at E +190 the slough and the funnel
are one water run reaching N +165 and a window that saw it would push the street 20 m up the slough
instead of over it. **One bend stands in the water on purpose**, at the deck's midpoint [189, 157.5]:
R-BUG4 drops a panel whose centreline endpoint is wet, so the two panels the deck replaces are
dropped and the crossing carries the street. Dry bends at each shoulder would have painted a 6.65 m
ford in silence â€” the fault T-0254 was filed to avoid. `--gate` now asserts exactly one wet bend and
that it is the deck's.

**What the west reach costs, and it is not hidden.** The tool measures it:

    clearance from the waterline, northward:      12.05 m .. 41.95 m
    clearance from the waterline, perpendicular:  12.00 m .. 41.50 m

against a 12.192 m setback. The 41.5 m is **one 15 m stretch at the base of Wolf Point**, where the
bank falls 45 m of northing in 35 m of easting and the derivation's running maximum â€” which holds
the street north of every bank point within 15 m of it â€” lags the turn. The rule is doing what it
says. `SMOOTH_M` is shared with the committed east reach, so tuning it here would re-derive 590 m of
street nobody asked to move: filed as **T-0307** with three routes and an acceptance clause, not
tuned in this PR.

**What this is worth in the scene.** 250 m of roadway that has never been drawn, on the one division
whose whole waterfront street was missing, plus a third crossing beside the two that stand.
**What a reader should doubt first**, and the record says so in its own words: whether North Water
Street reached west of the slough in 1835 at all. Nothing places a building on that side of it and
the North Division's initial parcel puts its roofs north of N +105. If that street did not run, this
crossing did not stand. Recorded as **L202**.
## Shipped 2026-08-28 â€” T-0156: the flicker instrument stops overstating what it found

**A column called INTERIOR was quoted for six days as *the layer fighting itself*, and it never
meant that.** `tools/measure_tie_class.mjs` partitions a 2 mm-nudge flicker by which layer owns
each moving pixel, then splits each layer's share into its outline against the rest of the scene
and the pixels its own footprint surrounds on all eight sides. The second number was read as a
depth tie â€” the defect R-BUG6 was opened to find â€” and printed under the sentence *"the pixels
where a layer fights ITSELF"*.

`interiorOf` cannot support that reading. It knows one layer's outline against everything else and
is blind to the boundary between two surfaces OF that layer, so one crown behind another and a
chimney against its own roof both land inside it. T-0013 measured the size of the error on
2026-08-23 with a depth pass and found **94â€“98 % of the count sitting on a depth BREAK** â€” a
silhouette by any honest reading â€” and **0 % a depth reorder or a shading resample**. It changed
nothing in the instrument, deliberately: closing a ticket by rewriting the tool that measured it is
the one move this project does not allow.

**Five days later the instrument was still printing the refuted sentence**, so anybody reading the
tool rather than ROADMAP Â§ R-BUG6(c2) read the wrong claim. This ships the repair, by ADDING a
measurement rather than loosening one:

- `tools/depth_field.mjs` â€” T-0013's discriminator extracted whole (the packed-depth swap, the
  linearisation, the second-difference break test), imported by both instruments so they cannot
  answer the same question differently. The trade table in `generate_frontage_works.py` and the
  face arithmetic in `block_faces` are the same move for the same reason.
- `measure_tie_class.mjs` prints the split beside the count, names the column `SURROUNDED` â€” which
  is what it measures â€” and ends on the only total that ever meant what "interior" was taken to
  mean. Its `--out` masks now paint an internal edge and a self-fight different colours; before,
  one colour asserted the reading the depth pass refutes.

**The demonstration, both tools run the same afternoon on the same published mirror**, `from_above`,
1280Ã—800, 2 mm nudge, shadow map off, control 0 px and return 0 px: `structures` 421 surrounded â†’
**402 internal edge / 0 reorder / 0 same-surface / 19 no-depth**, and `trees` 231 â†’ **218 / 0 / 0 /
13** â€” agreeing pixel for pixel with `diagnose_interior_flicker.mjs`'s independent run. `ground`
reads 66 here against 77 there, and the gap is the tools' own layer lists rather than the
discriminator: `measure_tie_class` also carries `streets`, `flora` and `water`, which claim eleven
pixels first. **Self-fight across all six layers: 0 of 731.**

The surrounded counts are byte-identical to the run taken immediately before the change, so the
split is an addition and not a re-measurement. Against 2026-08-23 the counts moved (structures 370
â†’ 421, trees 257 â†’ 231) and the shares did not (95 / 94 / 98 % against 94 / 98 / 96 %) â€” five days
of content under a claim that survives it.

## Shipped 2026-08-28 â€” T-0224: a critic baseline standing on the public square

**T-0027 replanted a whole city block and nothing in this project could show it in a picture.** The
public square â€” the block bounded by Randolph, Clark, Washington and LaSalle, the one block
`data/reconstruction/1835_reserved_ground.json` holds was never private building ground â€” went from
wet prairie to sedge meadow on 2026-08-23, and it was verified by a zone lookup and a zero-pageerror
pass. `tools/critic_shots.mjs` had no stand on it or facing it, so the sward over the town's only
reserved block, and the county buildings standing on it, had no reading of any kind.

**The stand.** `public_square`, a pose station rather than an anchor: local `(550, -370)`, ground
0.885 m, bearing **292Â°**, pitch 0. It stands inside the block's south-east corner and looks across
its long diagonal, which is the longest run of reserved sward in the town.

**The bearing is derived, not chosen by eye.** It is the bisector of the two county buildings that
stand on 1 July 1835 â€” the estray pen at the south-west corner, **81.8 m off at 264.9Â°**, and the
log jail at the north-west corner, **131.2 m off at 319.9Â°**. They are 55.1Â° apart, so each sits
27.5Â° off centre. Both were projected through the renderer's own camera before the pose was fixed,
which is what settles the composition question the frame itself cannot: at 1280Ã—800 the camera
reports fov 55 and aspect 1.6 â€” half-FOV 39.8Â° â€” and puts them at **x = 246 and x = 1047 of 1280**;
at 390Ã—780 it reports fov 94 and aspect 0.5 â€” half-FOV 28.2Â° â€” which leaves **0.7Â° of margin** and
puts them at the extreme edges. **So the desktop row reads the ground and the two buildings, and
the mobile row reads the ground.** No stand on this block does better: its corners are 108 m apart
and the buildings sit on two of them.

**The third county building is not in the frame, and a frame that showed it would be the bug.** The
ticket names three; only two of them exist on the scene date. The first Cook County court-house was
erected on the north-east corner in the **fall** of 1835 â€” `documented_range.from` is `1835-10-01`
in `data/structures/cook_county_courthouse_1835.json`, on three independent Andreas passages â€” so it
is dated out of a 1 July scene and is absent from the registry, which the probe confirmed
(`inRegistry: false`, against `true` for the other two).

**The rows.** Shot against the committed tree, `--metrics`, source tree, full detail.

| viewport | timber all | timber centre | â€¦town's share of breaks | crown fine | crown Gâˆ’B | decile L | literal black px | RMS far/mid/near | flower load | BLOOM share of ground | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop 1280Ã—800 | 0.689 | 0.748 | 0.123 | 0.759 | 16.91 | 10.3 | 0 | 14.4 / 24.0 / 26.0 | 0.0034 | 0.0048 | 162 / 1,016,672 |
| mobile 390Ã—780 | 0.844 | 0.808 | 0.051 | 0.629 | 15.49 | 9.34 | 0 | 22.0 / 27.7 / 20.5 | 0.0007 | 0.0037 | 158 / 954,133 |

`sha256` `b08cedcd3653â€¦` desktop, `875e290b2dd1â€¦` mobile. Land/sky boundary row 401 of 800 and 391
of 780 â€” the horizon sits within a percent of the frame's own middle at both viewports, which is
what a level pitch on flat ground should give and is the cheapest available check that the pose
landed.

**What the rows say, and the one figure worth arguing with.**

- **This is the third station where flower load means anything.** Harness note 3 in *The critic
  baseline â€” 2026-08-14* holds that the flower denominator is only vegetation at the open-prairie
  stands; the near band here is reserved sward with no street, wall or roof in it, so `public_square`
  joins `prairie_south` and `prairie_west`. Desktop reads **0.0034**, which sits between those two
  (0.0031 and 0.0012 on 2026-08-14) and two orders under the 4â€“6 % brief. The block was replanted;
  it was not repopulated.
- **Mobile reads 0.0007 against desktop's 0.0034 â€” a factor of five at one stand, on one build.**
  The portrait frame is narrower and closer to the ground plane, and 103 flower-hued pixels of
  151,309 is a small numerator. Do not read the two viewports against each other here.
- **No literal black at either viewport**, against 12,063 pixels at `river_bank` and 11,015 at
  `first_post_office` in the 2026-08-14 table. The darkest decile is L 9.34â€“10.3, still under the Â§5
  floor of L â‰¥ 14, and R-W1 still owns it.
- **The town is 12.3 % of what breaks this skyline on desktop and 5.1 % on mobile.** The rest is
  timber. That is the R-W4a subtraction doing its job at a stand where the horizon is mostly the
  north and west sides of the block and the town beyond them.

**The repeat, and it is a stronger reading than the one that was planned.** `--stability` did not
finish inside the run's ten-minute-per-command ceiling, so the harness's own repeat contract was not
exercised. What replaced it is better evidence for the same question: the pair of frames was shot
TWICE, in two separate browser processes, **half an hour and five sibling merges apart** â€” the
second round after this branch was replayed onto a `dev` carrying T-0227's AO work â€” and all four
frames are **byte-identical**, `b08cedcd3653â€¦` desktop and `875e290b2dd1â€¦` mobile both times, with
every metric repeating exactly. So 2/2 at both viewports across processes, which is what the
2026-08-14 table reports for its eleven, and the run's own churn is the control. It does not assert
the â‰¤ 1 % metric-drift half of the contract by the harness's own instrument; that is the part still
owed.

**The rig now stands at fourteen stations** â€” ten scene anchors and four poses â€” against the eleven
the 2026-08-14 table records.

**Verified.** `tools/check.sh` (PASS) â€” which is the dev gate in full, per `docs/PIPELINE.md`.
`node tools/critic_shots.mjs --stations public_square --metrics` at both viewports on the source
tree, and `--published --stations public_square` at both viewports on the mirror this PR writes:
the station resolves, the declared pitch is met and `page_errors` is empty in all four. The
unfiltered `tools/smoke_renderer.mjs` was NOT run â€” it takes about 55 minutes on this runner
(T-0235) against a run ceiling of ten minutes per command, and it was started and killed at that
ceiling rather than quietly skipped. Nothing under `renderers/`, `generators/`, `data/` or
`assets/` is touched by this change; the diff is one tool, this file, the changelog and the
publish mirror's copy of it.

## Shipped 2026-08-28 â€” T-0227: the AO bake is too dark, and now something has actually looked at it

**Nothing in the town moved.** This run answers a question the project has been holding an opinion
about for months without ever having read a rendered frame that carried the thing it was judging.

**The question, and why it was open.** `bake_ao()` has said since it was written that AO on these
archetypes is a geometry problem, and quoted "mean 0.265 with 69 % of texels below half" plus "0.38
at a 0.25 m AO distance". T-0158 voided both â€” read off an sRGB-tagged buffer, and averaged over a
512Â² atlas **68.9 % of which is empty UV space**, so the 69 % was very nearly the empty fraction
itself. Worse than either fault: **until T-0158 the export shipped a uniformly black texture**, so
no AO judgement this project holds was ever made on a file that carried occlusion at all.

**What was done.** `sauganash_hotel` rebaked with `--ao` (baked mean 0.1665 â†’ exported 0.1665, 0.0 %
drift), swapped into the source tree, and shot at both Sauganash anchors and both viewports through
`tools/critic_shots.mjs --metrics` against the same tree without it. The new
`tools/measure_ao_frame.mjs` reads the building's **own visible pixels** out of those frames â€” the
structures mask (`full` vs the `__bare` capture) intersected with the pixels that moved between the
two conditions â€” so the reading is of the walls, not of the frame and not of the atlas.

| station | viewport | pixels read | mean L\* without â†’ with | L\* < 20 | literal black px |
|---|---|---|---|---|---|
| `sauganash` | desktop | 87,893 | **33.8 â†’ 11.1** | 31.1 % â†’ **88.9 %** | 0 â†’ **6,532** |
| `sauganash` | mobile | 20,010 | 33.4 â†’ 11.1 | 31.8 % â†’ 89.5 % | 0 â†’ 1,289 |
| `sauganash_wing` | desktop | 99,681 | 39.1 â†’ 17.9 | 15.4 % â†’ 64.9 % | 0 â†’ 3,781 |
| `sauganash_wing` | mobile | 17,511 | 41.9 â†’ 20.6 | 4.9 % â†’ 56.5 % | 0 â†’ 340 |

**The answer is yes, and the atlas statistic understated it.** A documented white-painted wall loses
two thirds of its lightness and puts thousands of pixels at literal 0,0,0 â€” a hole in the render,
not a shaded wall. The whole-frame critic table agrees from the other side (`literal black px`
0 â†’ 6,841, `shadow darkest decile L` 4.67 â†’ 2.00 at `sauganash` desktop), with triangles unchanged.
**"Mean 0.5358 over written texels" reads as about-half-occluded and sounds survivable; the frame
says the building goes out.** The mechanism is that glTF occlusion scales the INDIRECT term only,
and at the scene's 70.5Â° sun the street elevations a walker sees are carried by little else (Â§1
items 9â€“11) â€” occlusion near 1 there removes essentially all their light. So R-W3a keeps its cage
and loses its target: **acceptance is now a `measure_ao_frame.mjs` reading, not an atlas mean.**

**Two costs the cage parcel inherits, measured on the same asset.** The atlas is **31.1 % occupied**
(81,458 of 262,144 texels; the master 94,420 â†’ 202,292 bytes, +114 %), so two thirds of a ~107 KB
occlusion PNG is blank â€” **T-0286**. And `aoMap` is part of `materialKey` in `buildings.js`, so an
AO'd asset cannot batch with an un-AO'd one: **+2 draw calls at every station and both viewports for
one building**, against ceilings already breached â€” **T-0285**.

**What did NOT ship: the AO itself.** The bake stays off and `assets/manifest.json` keeps saying so.
Shipping an occlusion map that extinguishes a documented white wall would be a data-integrity bug in
an aesthetics costume, and the affordability questions above are R-W3a's to answer.

## Shipped 2026-08-28 â€” T-0211: the other nine group rows are cross-checked against something now

**The hole T-0032 left behind.** `data/reconstruction/1835_building_inventory.json` carries the same
662-roof aggregate three ways â€” 35 `family_targets`, a 10-group Ã— 4-division `district_group_matrix`,
and four `districts` totals â€” and the ledger asserted that all three sum to `roof_total` and that each
group's families sum to that group's row. **Nothing asserted anything about a group's split BY
DIVISION**, and the two views were authored independently. T-0032 (PR #388) found what that permits
in the `institutional_public` row and corrected that one row; the ticket it filed asks the same
question of the other nine.

**The answer is not "they are fine".** `tools/measure_group_district_rows.py` prints the full
ten-row Ã— four-division audit with the signed gap in every cell. Thirty-eight of the forty cells hold
roofs they have room for. Two do not, and both are in the North Division:

| group | division | row says | stands | over by |
|---|---|---|---|---|
| `warehouses_freight` | north | 1 | 7 | **6** |
| `institutional_public` | north | 3 | 4 | **1** |

Six of the seven North freight roofs are **documented pre-existing records** â€” Kinzie & Hunter's
warehouse, the four north-bank sheds at the Dearborn reach, the north-side brickyard â€” so the breach
is not an invention that can be removed. It is a row authored without the north bank's river-freight
fabric in view. The seventh is `recon_1835_north_f1_022`, dealt by a parcel that ran before anything
measured this. The institutional cell is a narrower thing: T-0032 set that row to the NAMED census and
`measure_institutional_claims.py` holds it there, while this counts every roof that stands â€” so the
two gates disagree by exactly `recon_1835_north_i2_015`, the one anonymous school **L93** records as a
liberty taken rather than deleted. Both readings are right for their own question.

**What the breach was costing, which nothing anywhere stated.** `reconcile_665.py` clamps the negative
away with `max(0, matrix[g][district] - built[(district, g)])`, so a row wrong by six roofs read
exactly like a row that is right. The clamp does not merely hide it â€” it re-spends it. The division's
ten clamped heads then sum to **more** than its own remainder, by exactly the overshoot, and an
unnamed loop sheds the difference from whichever group has the most head. Measured: the North
Division's **seven** overshooting roofs are paid for, in full, out of its **ordinary dwellings**. The
programme document now says so, in `remaining.district_group_rows_overshot` and
`remaining.district_group_slots_shed`.

**What is asserted, and why it is the weaker claim.** The I3 repair does not generalise. An
institutional row can be held to a census because Chicago's public buildings are enumerable; dwellings,
stores and barns are not, so "the row equals what stands" is the WRONG assertion for the other nine â€”
a row 74 roofs above what stands is the programme working as intended. The gate asserts the two things
that are true regardless:

1. **the matrix adds up in BOTH directions** â€” each row's four cells to its own `total`, and each
   division's ten cells to its own `target`. Neither was asserted anywhere before this, and the second
   is what makes the shed an identity rather than a coincidence;
2. **every division over one of its group rows declares it**, at a declared size â€” a ratchet in the
   shape `measure_band_claims.py` uses. It may fall, it may not rise, a new breach fails, and a
   declaration that outlives its breach fails too.

Neither cell is repairable by editing one number: the cells sum to their division's target *and* to
their group's total, so moving one moves four others and the 662-roof programme with them. That is a
decision about the authored target and it is filed as its own ticket. This run's job was to stop the
breach being invisible while it waits.

Verified: `tools/check.sh` (green, with the two new steps), `python3
tools/measure_group_district_rows.py --self-test` (8 cases, including the north half of the
apportionment T-0032 corrected, a grown breach, a healed one and a stale declaration). No renderer
file changed, so the frame is byte-identical.

## Shipped 2026-08-28 â€” T-0282: the shrub stratum joins the ceiling declaration, and a visitor can read it

**T-0019 declared the forb lattice's ceiling this morning and the declaration could not see half of
what it was declaring.** `flora.js` deals FOUR (stratum, side) lotteries through the same `shareOf`
against the same 0.34602 plants/mÂ² ceiling â€” forb dry, forb wet, shrub dry, shrub wet â€” and the
baseline listed forb layers only. `z06_dense_forest`'s shrub records ask **0.403 clumps per mÂ²**
against that ceiling and have been over it since **K54** named that community as the one whose shrub
density reaches the clamp. `shrubShareWet` and `shrubDensityWet` were not exported from `flora.js`
at all, so a quarter of the lattice was unreadable from outside it.

**The gate that exists to stop a layer joining the clamp in silence was itself silent about a
stratum.** It is ten layers of eighteen now, not nine of ten, and the identity of a declared line is
`(community, stratum, side)`. The gate was verified reading RED on the real tree before the
re-declare â€” `z06_dense_forest.shrub.dry is on the lattice ceiling and is NOT declared` â€” and green
after it. A declaration written before this carries no `stratum` and is read as `forb`, so the file
migrates on the next `--declare` instead of failing every line at once.

| layer | asks | draws | share of its own evidence |
|---|---|---|---|
| `z06_dense_forest` forb | 66.381 /mÂ² | 0.346 /mÂ² | **0.5 %** |
| `z04_marsh` forb, dry and wet | 22.000 /mÂ² | 0.346 /mÂ² | **1.6 %** |
| `z10_settled_town` forb | 11.866 /mÂ² | 0.346 /mÂ² | **2.9 %** |
| `z05_riverbank_timber` forb | 3.851 /mÂ² | 0.346 /mÂ² | **9.0 %** |
| `z03_sedge_meadow` forb | 1.812 /mÂ² | 0.346 /mÂ² | **19.1 %** |
| `z08_lakeshore` forb | 0.630 /mÂ² | 0.346 /mÂ² | **54.9 %** |
| `z02_mesic_prairie` forb | 0.408 /mÂ² | 0.346 /mÂ² | **84.8 %** |
| `z01_wet_prairie` forb | 0.407 /mÂ² | 0.346 /mÂ² | **85.0 %** |
| **`z06_dense_forest` shrub** | **0.403 /mÂ²** | **0.346 /mÂ²** | **85.8 %** |

**The second half is the one a visitor gets, and it is why this was worth a run rather than a
follow-up line.** T-0019 put the debt in `tools/forb_clamp_baseline.json` and in this file â€” where a
reviewer reads, and nowhere a visitor does. T-0281, filed by that run, says it plainly: *a visitor
standing in the dense forest is looking at half a per cent of the flowers the research put there and
has no way to find that out.* **`docs/LIBERTIES.md` L201** now carries the table above, what is ours
in it (the number of slots) and what is not (every density in it, straight from `data/flora`), and
it compiles into `data/liberties.json` â€” so it stands in the Evidence panel's liberties list beside
the other two hundred. That is not T-0281's full "What grows here" section and does not close it;
it is the clamp reaching the register this project already ships to visitors.

**Nothing was raised and no plant moved.** K58's other two routes buy their plants in exactly the
two communities that carry the most geometry, and the scene-detail ceiling is breached at Lake and
Canal at both viewports today (T-0203, T-0218). The frame is identical.

Verified: `tools/check.sh`, `node tools/measure_sward_draw.mjs --gate` (both assertions PASS, and
the clamp assertion shown RED first), `node tools/smoke_renderer.mjs --published` across both
viewports.

## Shipped 2026-08-28 â€” T-0225: the sward's drawn reach is read at a coverage the screen door can hold

**The defect.** `tools/smoke_renderer.mjs` part 7 reports the sward's outer boundary by binning the
view into 16 bearings and taking, in each, "the furthest plant in this bearing that is actually
DRAWN". Drawn was `flora.fadeAt(...) > 0.02`. `fadeAt` is COVERAGE since T-0035 â€” the alpha the
fragment program resolves through an ordered 4x4 Bayer matrix â€” so the reading called a plant drawn
at two per cent of a screen door that has sixteen levels in it.

**What two per cent actually renders as.** `chiBayer4` returns `(v + 0.5)/16` over `v = 0..15` and
`vChiDither` slides that whole set of sixteen thresholds by a per-instance phase, so the pixels
surviving in a 4x4 tile number `floor(16F)` or `ceil(16F)` and nothing between. Below `F = 1/16`
that is 0 or 1, and **which of the two is decided by the instance's dither phase â€” a number no
reader this side of the GPU has.** At `F = 0.02` one phase in three keeps a single pixel of the
tile and the other two keep nothing at all. The boundary the gate reported was therefore very
nearly the radius at which the placer stopped placing, which the lattice inset already guarantees.

**Measured, with the new `tools/measure_sward_reach.mjs`** â€” the same station the gate finds, the
same 16 bins, a sweep of thresholds. The gap between the PLACED boundary and the 2 % reading is
**0.54 m at `full` (27.35 â†’ 26.81 m mean) and 0.56 m at `light` (12.52 â†’ 11.96 m)**. That is the
size of the thing the statistic was measuring.

**The threshold, and why it is not a taste.** `1/16` is the smallest value at which "drawn" stops
being a property of the instance's dither phase and becomes a property of its coverage: at or above
it every instance keeps at least one pixel in every 4x4 tile it covers, whatever phase it drew. It
is the screen door's own quantum.

**The bars are re-derived, not slackened.** They are stated against the PLACED boundary (`nominal`
Â± the slot's own `fringe`) while the statistic now reads the DRAWN one. The ramp is linear
(`flora.fadeOf`: `clamp01((outer - d) / band)`), so a slot reaches coverage `F` at `outer - F Ã—
band` and the two boundaries differ by exactly `band Ã— seen` â€” 0.44 m on the desktop's 7.0 m ramp,
0.10 m on the phone's 1.6 m one. That term is a property of the statistic, so it belongs in the
bar; leaving it out would fail a sward for being read more honestly. Nothing else about the bars
moved.

**What each viewport lands at, and both readings are printed by the check itself** (T-0187's `show`
flag exists for this):

| viewport | tune | nominal Â± fringe | reach at 6.25 % | at the old 2 % | bars (min / mean) |
|---|---|---|---|---|---|
| desktop 1280Ã—800 | `full` | 26.40 Â± 3.00 m | 25.00â€“28.00, mean **26.61** | 25.00â€“28.41, mean 26.81 | 21.76 / 24.46 |
| mobile 390Ã—780 | `light` | 12.40 Â± 1.60 m | 10.32â€“13.22, mean **11.96** | 10.32â€“13.22, mean 11.96 | 9.50 / 11.50 |

Both viewports clear both bars â€” the phone by 0.82 m on the minimum and 0.46 m on the mean, the
desktop by 3.24 m and 2.15 m. **No finding about the sward falls out of this**; had one, it would
have been its own ticket rather than a wider bar. On the phone the two readings are identical to
the centimetre, which is what a 1.6 m ramp and a 6.8 cm shell between the thresholds predicts.

**What it unblocks, and that is why an invisible run was taken.** T-0187 priced spreading the mid
and forb rings' OUTER edges by density â€” the repair T-0093 made at the near/mid boundary and T-0086
at the far band's â€” and took a different route because the boundary check preferred the dither: a
spread took the mean drawn reach to 9.64 m at `light` against a bar of 11.60 m with 0.29 m unspent.
Every figure in that argument was read at 0.02. The bar is off the scale now; whether a spread can
actually clear it is unknown and unmeasured, and **T-0277** is that work. The stale half of the
`TUNE` comment in `flora.js` says so rather than continuing to assert a price taken with a broken
instrument.

**Verification.** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile SMOKE_STAGE=7` green on both
boundary checks, on one inherited red (`every tree drawn stands at its own station`, 0 of 0
vertices across 0 merged meshes â€” T-0243, standing on `dev` since 2026-08-28T00:55 by
`tools/dev-smoke-state.mjs`). Desktop part 7 was **not** taken to completion: it overran the
ten-minute foreground ceiling on a runner at load 3.6 of 4 CPU, and `dev-smoke-state` records no
desktop part-7 pass on this runner on any tree. The desktop figures above are from
`measure_sward_reach.mjs` at the gate's own station with the gate's own arithmetic, which is what
the tool was written for.

## Shipped 2026-08-28 â€” T-0019 (K58): the forb lattice's ceiling is declared, and it binds NINE layers, not six

**The clamp, stated plainly.** `forbShareOf` in `renderers/web/js/flora.js` is
`min(1, density Ã— cellÂ² / perCell)`, and that `min` is a lattice ceiling of **one plant per slot**.
`TUNE.forb` is a 3.4 m cell dealt 4 times, so a slot stands for **2.89 mÂ²** and the lattice cannot
draw more than **0.346 flowering plants per mÂ²** whatever a community's records say. K58 opened on
that, and its acceptance offered two ways out: each clamped layer either FITS or its shortfall is
declared in the census gate. Fitting is not available â€” see the last section â€” so this run declares.

**K58's own count is superseded: it is nine of the ten populated forb layers, not six, and the
figures are bigger than the ones on record.** K58 counted six at the midpoints of the recorded
ranges. T-0034 moved the forb stratum onto the TOP of every range (L182), so the asked densities
are the upper bounds now, and the two prairies and the lakeshore joined the clamp:

| community | side | records ask | lattice offers | draws |
|---|---|---:|---:|---:|
| `z06_dense_forest` | dry | 66.381 /mÂ² | 0.346 | **0.5 %** |
| `z04_marsh` | dry | 22.000 | 0.346 | 1.6 % |
| `z04_marsh` | **wet** | 22.000 | 0.346 | 1.6 % |
| `z10_settled_town` | dry | 11.866 | 0.346 | 2.9 % |
| `z05_riverbank_timber` | dry | 3.851 | 0.346 | 9.0 % |
| `z03_sedge_meadow` | dry | 1.812 | 0.346 | 19.1 % |
| `z08_lakeshore` | dry | 0.630 | 0.346 | 54.9 % |
| `z02_mesic_prairie` | dry | 0.408 | 0.346 | 84.8 % |
| `z01_wet_prairie` | dry | 0.407 | 0.346 | 85.0 % |
| `z09_sand_prairie` | dry | 0.114 | 0.114 | **100 % â€” the only one that fits** |

K58's midpoint figures for the same layers were 44.545 (`z06`), 14.5 (`z04`) and 7.760 (`z08`,
`z10`). **The marsh's WET side appears here for the first time**: `forbShareWet` is clamped exactly
as `forbShare` is, and the density behind it was not exported from `flora.js` until this run
(`communities().forbDensityWet`).

**Why nobody saw the drift.** A share reading `1.000` is one plant per slot whatever the slot is,
so a layer sitting ON the ceiling printed identically to one tuned below it, and the size of the
debt could only be recovered by re-deriving it from the records. Both movements happened under a
green tree: **K55 took the clamped count from four to six** by fixing a cover-fraction/count unit
error, and **T-0034 took it from six to nine** by dealing off the upper bound. Neither showed up
anywhere.

**The declaration and its gate.** `tools/forb_clamp_baseline.json` is the ledger: every
(community, side) the ceiling binds, the density its records ask for, and the share of that density
the lattice can carry. `node tools/measure_sward_draw.mjs --gate` now prints the whole table and
FAILS when the measured set stops matching the declaration â€” a layer joining the clamp, a layer
leaving it, the lattice ceiling moving, or an asked density moving more than half a per cent.
`--declare` rewrites the file from the measurement, so the figure is never re-typed off a console.

**The gate was shown reading red three ways before it was trusted**, which is this project's own
bar: with an empty declaration it named all nine undeclared layers; with `z04_marsh.wet` declared
at 18.0 against a measured 22.0 it called the declaration stale; with `z09_sand_prairie` declared
clamped when it is not it asked for the line to be withdrawn. Green with the committed file:
`9 clamped, 0 problem(s)`.

**What was NOT done, and it is a decision rather than an omission.** No ceiling constant moved.
`TUNE.forb.cell` and `TUNE.forb.perCell` are what they were. K58's routes out â€” a per-stratum cell,
more than one plant per slot where the record asks for it â€” all buy plants with geometry, and they
buy the most of it in `z06_dense_forest` and `z10_settled_town`, which are the two layers already
carrying the most. The `full` and `balanced` scene-detail ceilings are breached on `dev` as this is
written (T-0223, T-0229), so this is not the run to spend triangles on. The routes stay open and
they now have a number written against each of them.

## Shipped 2026-08-28 â€” T-0024: the face rule ranks dwellings, and the store steps onto the street line

**The question, and it has been open since 2026-08-15.** The face rule orders the DWELLINGS a
block parcel is dealt â€” the best take the better street, the meanest take the back one. T-A15 was
dealt the first STORE any block parcel had ever had to place, found the rule said nothing about
one, and EXTENDED the ranking to cover it: commerce above the better dwelling, on the reasoning
that a store-residence's claim on the better frontage is *"functional rather than social, the only
one of the six roofs whose purpose requires that a stranger can find it"*. It put the C2 on
Randolph, sent a D6 to the back street, and flagged its own extension as ROADMAP K32 for the next
block dealt a commercial family to follow or refute â€” the schedule still holds C1â€¦C4, F1â€¦F4, H3,
T1 and W1â€¦W5 for blocks not yet built, and a warehouse's claim on frontage is plainly not a
store's.

**Settled on reading 2 of the three the ROADMAP offered: the face rule ranks dwellings only, and a
non-dwelling is placed by its own function.** Reading 1 was to keep the ranking, reading 3 to
refuse the question and leave it to each parcel's arrangement note. Reading 2 is taken because it
is the only one of the three that can be READ OFF THE COMMITTED RECORD instead of argued.

**The reading.** Over the 48 documented buildings this project's own reconciliation credits a
non-dwelling family, by the traffic class `data/streets/1835.json` authors for the street each
stands nearest:

| letter | n | principal | ordinary | light |
|---|---|---|---|---|
| C stores | 15 | 10 | 5 | **0** |
| F warehouses | 9 | 9 | 0 | **0** |
| W workshops | 7 | 2 | 5 | **0** |
| T lodging | 8 | 3 | 4 | 1 |
| I institutions | 9 | 1 | 4 | 4 |

Not one documented store, warehouse or workshop stands on a light street â€” a zero across **31
buildings**, on the three letters a block parcel may actually be dealt. Lodging's one is the
Steamboat Hotel, 287 m from the State Street centreline, which does not front it; the institutional
families are refused to a block parcel BY NAME (L93) and no frontage rule reaches them. The second
reading is the setback: **every documented store standing on a platted street stands on its line**,
thirteen of the fifteen inside the measured street-line band, the two outside it being Robert
Kinzie's store at Wolf Point and the Miller house, both off the platted grid.

**The two clauses, authored in the recipe and refused at the generator.** (1) A non-dwelling takes
the block's better face by the committed street hierarchy, and a store, warehouse or workshop may
never take a light one. (2) A commercial roof stands ON the street line, at the closest line the
plat module's own margin allows â€” the same line the party-line runs on South Water and Lake already
stand on, rather than a second convention.

**What moved: ONE roof, and that is the finding rather than a convenience.** On `blk_randolph_clark`
reading 1 and reading 2 put the store on the same face, so the ranking could be refused without
re-dealing a block that already stands: no roof added or removed, no id, family, footprint or form
value changed, no household re-homed, no bake. What changed is the SETBACK â€” the C2 came forward
from 4.5 m to **1.50 m**, out of the 4.0â€“7.5 m band of house fronts it had been standing in. A
building whose whole argument was that a stranger must be able to find it had been placed as though
it were a cottage. One consequence follows it: the street-lining yard fence looks for a lot standing
back from its own frontage, a shop front is not one, and **24.6 m of fence comes off** that face.

**The 4.26 mm that was in the way, and it is named as what it is.** The per-lot margin gate compared
the distance from a footprint CORNER to the nearest point of the lot RING against the plat module's
1.5 m margin, while the setback a recipe authors is measured along the face normal. On a lot whose
side lines are not exactly square to its face the two differ by millimetres, so a roof authored to
stand exactly ON the margin read 1.4957 m and failed. It now carries the same 5 mm derivation
tolerance the party-line frontage gate two hundred lines above it already uses, for the same reason.
The margin is unchanged: 1.5 m is still the floor and a roof a centimetre inside it still fails.

**The gates.** `tools/generate_block_infill.py` refuses a slot that breaks either clause â€” a
light-street frontage, a face that is not the block's better one, or a commercial roof authored
behind the line â€” and `tools/measure_face_rule.py` holds the reading the clauses are taken from,
with two absolute assertions over the roofs the block parcels place and a `--self-test` that breaks
both in memory. Both run in `tools/check.sh`.

**What is reported and NOT asserted on.** The North, West and phase-one parcels ran before any of
this and place another 23 non-dwelling roofs. Seven are assigned to State Street at 150 to 550 m of
setback, which is not a frontage â€” it is the nearest committed centreline in a division with almost
no street control, and gating on those would be gating on the absence of a street. The real residual
is printed rather than fixed in passing: **two invented warehouses stand nearest Randolph at 12.9
and 14.5 m, against a documented F record that is 9 of 9 on principal streets.** Moving them is a
parcel's work on ground that is already built out, not a line in this one.

**Liberty L200.** Ticket **T-0024**, ROADMAP **K32**.

## Shipped 2026-08-28 â€” T-0025: the census that said three records were silent had read one field of a record that argues in four

**K35, opened by K34, asked what to do about three structures carrying AGENTS.md's standing
constraint with "no text anywhere in the record" saying what for. Two of the three were not
silent.** Read at K34's own commit (`23bb280b`), over the whole record rather than
`research_note`: `beaubien_barn` said it in `research_note`, `clybourn_slaughterhouse` said it in
`function.note` â€” *"flagged for review with the rest of this record's Indigenous content rather
than paraphrased away"*, in the same field that names Archibald Clybourne "the Government butcher
for the Pottawatomies" â€” and `council_house`, which K34 never named as a gap, said it in
`function.note` too. **Eight of the nine kept the convention, not six.** Only
`robert_kinzie_store` was bare.

This is not a scolding of K34; it is the reason the gate now reads what it reads. A building's
reasoning here is spread across `function.note`, `position.note`, the per-attribute notes and
`research_note`, and a policy sentence can honestly live in any of them.

**The one real gap is closed from the record's own attested business.** Andreas lists the store's
keeper among the town's Indian traders (scan p. 235) and among those licensed to sell goods (scan
p. 249); chicagology has it dealing in "groceries and Indian goods"; the record's `aka` carries
the source's own "R. A. Kinzie, Indian trader". The trade that names the building is the trade
the 1833 treaty ended, and the removal it ended in was under way six weeks after the scene date.
The paragraph states that and stops â€” no confidence moved, no source added, no liberty owed, and
the flag not lifted (lifting it is the claim that the consultation has happened, which assertion
5 already refuses).

**`tools/measure_review_constraint.py` gains assertion 6**, absolute, at every layer: a flagged
record must refer to the flag in one of the phrasings this dataset uses AND name the subject the
constraint is about, both in its own prose. Record-level, not sentence-level â€” `cobweb_castle`
opens "THE RECORD IS FLAGGED review_required BECAUSE OF WHAT THIS BUILDING WAS" and answers
itself over the next two sentences. **K35's objection to this route â€” "says something" is not
"says why" â€” stands, and the answer is that the census now PRINTS the sentence it matched under
every flagged id**, so what the gate cannot judge is at least in front of a reader. Both halves
were broken in memory against the real dataset and both fire; the restored tree passes.

**What is NOT claimed.** No visitor sees anything new: a building held under the constraint still
says so nowhere on its card, and the flag reaches the browser only as a `scene-loader.js` console
line. That is **T-0268**, filed by this unit rather than folded into it. `tools/check.sh` green
(the full gate, including `--stale`, the sidecar recompile check and the changelog contract);
`SMOKE_VIEWPORT=mobile` and the desktop smoke as recorded in the PR. No renderer file, no
geometry, no coordinate, no bake.

## Shipped 2026-08-28 â€” T-0162: the sward census stands at a phone, and its first honest phone reading is red

`tools/measure_sward_draw.mjs` has carried a `SWARD_VIEWPORT=mobile` flag since T-0018, and its own
header said why it had to exist: *"the viewport decides the ring sizes and therefore how many slots a
station deals, so the census has to be answerable at both."* It was not answerable at both. The two
runs came back **identical, row for row** â€” T-0018 measured 7,844 slots either way â€” and nobody could
see why, because both numbers were real numbers taken from a real page.

**THE WINDOW IS NOT THE DEVICE, AND THE RING SIZES ARE CUT FROM THE DEVICE.** `flora.js` sizes every
ring off `mergeTune(lowSpec && detail === 'full' ? 'light' : detail)`, and `lowSpec` is
`controls/touch.js` `prefersTouch()` â€” `(pointer: coarse)`, or a touch point under a 900 px window.
`browser.newPage({ viewport })` sets the window and nothing else: Chromium then reports
`navigator.maxTouchPoints === 0` and a fine pointer, so a 390-px page resolved `full` exactly as the
1280-px one did. The flag reached the CSS and never reached the tune.

**What it stands at now**, copied from `tools/smoke_renderer.mjs`'s own mobile context rather than
invented here (`hasTouch`, `deviceScaleFactor: 2`, and `isMobile: false` with the comment that goes
with it), so the census and the gate stand in the same place:

```
  stand: desktop 1280x800, 0 touch point(s), pointer fine   â€” detail full,  sward tune full
         ring reach: near 7 m, mid 26.4 m, forb 25.4 m
  stand: MOBILE  390x780,  1 touch point(s), pointer COARSE â€” detail light, sward tune light
         ring reach: near 4 m, mid 12.4 m, forb 12.4 m
```

**And the two censuses now differ, which is the demonstration.** Same 29 station-rows, same published
mirror, one command apart:

| | desktop 1280Ã—800 | mobile 390Ã—780 |
|---|---:|---:|
| slots dealt | **7,973** | **2,672** |
| drawn | 6,090 | 2,152 |
| refused by the two filters | 23.6 % | 19.5 % |
| pooled B/Bnull | 0.64 | 1.08 |

**THE STAND IS PRINTED AND IT IS ASSERTED.** The acceptance clause was *"no measurement is left
claiming a viewport it did not stand at"*, so the run states the stand it reached â€” window, touch
points, pointer, detail level, tune, and every layer's ring reach â€” before its first figure, and
EXITS 2 rather than print a census under a heading it did not earn. The desktop stand is asserted the
same way and for the same reason: a runner that reported a coarse pointer would deal this tool a
phone's census while its header said 1280Ã—800.

**THE FIRST HONEST PHONE READING IS RED, ON ITS FIRST RUN.** `--gate` â€” the assertion that no list
may owe a species a whole slot and draw it nowhere in the scene â€” **passes at desktop (0 pairs over
7,153 slots) and FAILS at mobile (1 pair over 2,763 slots)**:
`z10_settled_town.forb.xanthium_strumarium`, common cocklebur, owed 1.49 of a slot by the settled
town's own cover records and drawn nowhere at a phone's ring sizes. That is not a regression this
branch caused â€” it is the reading nobody had ever taken â€” and it is **T-0266**, not a fix made in
passing.

**Filed by this run:** T-0266 (the phone census's own gate is red).
## Shipped 2026-08-28 â€” T-0138: the town's two brick chimneys become one

`generators/inferred_placeholder.py` painted its stacks `placeholder_chimney_brick` at
`#89503F` â€” `0.537, 0.314, 0.247` linear, roughness 0.88 â€” a literal written in that file and
read nowhere else. T-0008 gave the 112 brick stacks on the archetype buildings the sheet's
`CHIMNEY_BRICK` at `0.45, 0.23, 0.17`, roughness 0.85. **About 20 % apart in linear red, on
buildings standing on the same streets** â€” `docs/RESEARCH/materials.md` finding 5's complaint
(a generator with no shared palette) surviving the parcel meant to end it, and named as
deliberately left alone in `chimneys.md` Â§4.

**The literal loses, and not by a coin toss.** Nothing in this repository argues for `#89503F`:
no source record, no note, no tier. `CHIMNEY_BRICK` is `frame_tavern`'s committed `BRICK_RGBA`,
read off the Petford watercolour of the Sauganash (T-0092, **L154**) â€” the one coloured witness
to any Chicago chimney â€” generalised to the town's other framed stacks on Blodgett's North Side
brick-yard, spring 1833. An `inferred` value carrying a source beats an undocumented literal, so
the literal goes and **no new number enters the sheet**. `CHIMNEY_BRICK`'s own argument is
untouched.

**The generator asks the selector, not the row.** It now calls
`materials.chimney_finish("interior")`, which is what it actually builds: a box inside the
footprint depth rising through the roof, the framed house's masonry flue. Asked the question
rather than told the answer, a placeholder cannot drift from the archetypes again.

**A log dwelling's placeholder still gets brick, and that is the massing's fault.** Â§3's
stick-and-clay daub belongs to a stack standing OUTSIDE the gable; the placeholder puts every
stack inside the roof, so the daub would be the right fabric on the wrong silhouette. Left alone
with the reason written down rather than half-fixed.

### THE HALF OF THE TICKET THAT NO LONGER EXISTS, AND SAYING SO IS MOST OF THIS ENTRY

T-0138 was written on 2026-08-22 against **"90 committed masters"**, and asked for them, their
compressed derivatives and the banked passthrough set to be regenerated in the same commit
(K38, `--write-baseline`). That was the whole reason T-0008 did not smuggle the convergence in.
Re-measured on `dev` before anything was edited:

| measurement | reading |
|---|---|
| `python3 generators/inferred_placeholder.py --check` | `0 flagged placeholder GLBs; 230 superseded by a canonical bake` |
| manifest entries with `kind: placeholder` | **0** of 349 |
| committed GLBs under `assets/` containing `placeholder_chimney_brick` | **0** |

So no master moved, no derivative moved, the passthrough baseline did not need re-banking, and
**no building repaints â€” there is no before/after frame to take, because nothing renders this
material.** The acceptance asked for one and the honest answer is that the subject of the
photograph has been baked out from under the ticket. This is T-0126's shape exactly (materials.md
Â§7): the divergence is closed at the source so it cannot walk back in the day a record outruns
the bake and a placeholder is emitted again.

**What a visitor sees, and it is one sentence.** L168's Evidence card said *"the 90 inferred
placeholders keep their own `#89503F` brick"*. That sentence was false and it is on a card
anybody can open, so it now says what happened instead. Nothing in the 3-D scene changed.

**An invisible run, declared as one.** AGENTS.md's rule is that a run changes something a visitor
can see; this one changes a card and a generator. It is the eighth of eight parallel slices on
this queue and the seven above it are on visible parcels, so the one-in-four cap is not touched â€”
but the entry says "nothing you can see" rather than dressing it up, which is the other half of
that rule.

**Gates.** `tools/check.sh` green, including `inferred_placeholder.py --check` and
`compile_liberties.py --check`. Changelog contract green at v314.

## Shipped 2026-08-28 â€” T-0099: the bank track from the fort's north gate reaches the water

`p4_0` â€” the fort from the north bank, the stand this project shoots it from â€” draws a track
climbing the bank from the water's edge to Fort Dearborn's NORTH gate, the way to the ferry the
1830 Harrison plan names among the ground round the fort. The town has never drawn it, and the
refusal was written down rather than forgotten: **L140**, the fort road's own liberty, says *"the
bank it descends is the flat plateau T-0004 exists to grade and a ramp down an ungraded bank
would be two inventions stacked."* T-0004 graded that reach on 2026-08-20. One invention is gone;
this ships the other, labelled.

**`fort_bank_track` â€” one straight chord, 23.91 m long, 3.60 m wide.**

| | value | where it comes from |
|---|---|---|
| start | `[1156.63, 253.92]` | the north gate's own centre (26.5 m along a 53 m wall â€” the midpoint `measure_fort_gates.py` reads the shipped leaves at), carried out along the wall's outward normal by **6.740 m**, the standoff `fort_road` already keeps from the SOUTH gate |
| end | `[1133.40, 259.61]` | the committed heightfield's Z = 0 waterline on the easting of the **west end of the commandant's quarters** â€” the 1855 Hesler key's ferry landing, *"under the west chimney of the Commandant's quarters"* |
| width | 3.60 m | the palisade's committed `gate_width_m` â€” the gate it comes out of |
| corridor | 12.0 m | `fort_road`'s, the only other reconstructed corridor on this reservation |
| grade | `reconstructed` geometry, `inferred` surface, `reconstructed` wear | L199 |

**Why it slants, and the number is what decides it.** Straight north out of the gate the graded
bank falls 3.599 m in under 10 m â€” **1 in 2.7**, a scramble rather than a way to a boat. Swung
west onto the landing the same fall spreads over 23.91 m: **1 in 6.65 mean, 1 in 3.65 at its
steepest metre**, at `[1140.0, 257.99]` on the committed heightfield. That worst metre is gentler
than ground this project already draws roadway on â€” `south_water` reaches **1 in 3.0** at the
river bank, `randolph` and `washington` 1 in 4.1. One chord and not several, so no joint opens a
wedge of prairie at a bend (L178, L194).

**READ THE DATE ON THE LANDING.** `wentworth_1881_fort_dearborn` warns on its own face that the
Hesler key is 1855 and describes the compound after the garrison marched out. It is read here as
an inference that a landing fixed by the shape of a bank stood where it stood twenty years
earlier, never as a measurement of 1835, and it does not lift the record off `reconstructed`.

**What it looks like, measured rather than asserted.** From `p4_0`'s own stand â€” the nearest dry
ground on its sightline, local `1145, 308`, yaw 170 â€” the two frames differ in **37,887 pixels**,
and the difference is the track and the street readout naming it, and nothing else:
`docs/evidence/t-0099-before.png`, `t-0099-after.png`, and the bank zoomed in
`t-0099-bank-crop.png`. The ground it lies on is already the apron's bare trodden earth (L174), so
the track reads as *wear* on bare ground rather than as a new colour â€” which is what the plate
draws too. Standing at the top of it, the street readout says **ON STREET â€” The bank track**
(`t-0099-gate-after.png`).

**One consequence nobody would have predicted, and it is committed rather than suppressed.**
`tools/generate_dooryard_plantings.py` seats a house's stems *away from the nearest street*, and
it reads every street in the dataset with no limit on reach or on which bank it is. For
`recon_1835_north_d4_039`, a dwelling on the NORTH bank at `~[1139, 321]`, the new track is
**61.6 m** away against `michigan_north`'s **68.3 m** â€” so a track on the south bank, across the
river, became that house's nearest street and turned its yard. Two cottonwoods move about 6 m.
The rule was re-derived and the result committed; whether a street should be able to reach a
house across open water is **T-0255**.

**Filed by this run:** T-0255 (the dooryard rule's unbounded street reach).
## Shipped 2026-08-28 â€” T-0245: South Water Street gets its first control point, at Franklin

`data/traces/street_control.json` held four control points â€” `lake_canal`, `lake_market`,
`randolph_canal`, `kinzie_canal` â€” and **none of them was anywhere on South Water Street**, the
riverfront street the whole south bank is measured along. There are five now.
`control.south_water_franklin` is committed at E 447281.16, N 4637407.21 (41.8868373 N,
-87.6354394 W; local ENU **208.46, +11.41**), the mean of OSM nodes `28358883` and `28358941` â€”
North Franklin Street's two crossings of West Upper Wacker Drive's carriageways, 15.28 m apart on
the same easting to 0.08 m.

**It is a crossing, and it is shown to be one rather than asserted.** `node_rule`'s third failure
mode â€” the one T-0183 found at Market one block west â€” is that two named surface roadways share
nodes wherever one CHANGES NAME INTO the other at a bend, which reads identically in the output.
The discriminator recorded on this entry is that **both named ways continue through the shared
set on both sides**: North Franklin Street arrives on way `452188414` from local (208.2, -12.3),
passes `28358941`, runs on to `28358883` on way `253745133` and carries north; West Upper Wacker
crosses east-west on a different carriageway at each node (`319358165` â†’ `931237159` through the
first, `319358163` â†’ `1136945346` through the second). At Market neither holds: North Upper
Wacker *ends* at its node and West Upper Wacker *begins* there.

Reproduced twice on the day, from the committed record, against the live map:

```
  tools/refetch_control.py --discover south_water_franklin
      2 shared node(s), mean E 447281.16 N 4637407.21, spread 15.28 m, drift 0.00 m
  tools/refetch_control.py                    (the default verify pass, all five)
      south_water_franklin ok  2 node(s), drift 0.00 m (tolerance 1.00)
      lake_market 0.04 Â· kinzie_canal 0.01 Â· lake_canal 0.00 Â· randolph_canal 0.00
```

**AND NOTHING MOVED â€” these are the numbers.** The point's value is that it makes two committed
lines checkable for the first time, which is a different thing from correcting them.

| measured against `control.south_water_franklin` | |
|---|---:|
| committed South Water Ã— Franklin corner (intersection of the two centrelines) | local (208.49, +2.83) |
| the control | local (208.46, +11.41) |
| separation | **8.58 m** (Î”E âˆ’0.03, Î”N +8.58) |
| perpendicular standoff from South Water's own line (it runs 15.4Â° N of E here) | **8.28 m** |
| that, against the 12.192 m half of the 80 ft platted module | **68 %**, 3.91 m to spare |
| Franklin's committed easting at the junction's northing | **0.03 m** |

So the whole disagreement is *across* South Water and none of it is *along* it. The 8.28 m south
is the standoff `data/streets/1835.json` has described since it was written as *"shifted into the
dry half of the platted riverfront corridor"* â€” a reconstruction decision about dry ground, not
an error in an offset â€” and that sentence now carries the measurement. Re-deriving the street
onto the modern centreline would *undo* it, so nothing is re-derived and no placement names this
control. Franklin's 0.03 m is a **reproduction, not an independent confirmation**: `franklin`
already lists `osm_streets_2026` among its sources, so what it establishes is that the line can be
re-derived from the source it names, which until today it could not be.

**It does not unlock `blk_south_water_market`.** That block's gap is at its WEST corner and South
Water already reaches Franklin; the 27 roofs still wait on the owner decision `refused_control.
market_south_water` states. T-0028 therefore stays where it is â€” see below.

**The corner has a document.** The first post office stood at the south-west corner of Franklin
and South Water from 2 Nov 1832 to 3 Mar 1837 (`docs/research/03-structures-north.md`), so it is
a corner on the scene date and not only a modern junction.

**AND IT IS VISIBLE, in the one place a control point can be.** The Go-to menu's survey
junctions are compiled into the sidecar index from `street_control.json` on every check, so the
menu now offers five where it offered four â€” `South Water Street & Franklin Street`, at local
(208.46, +11.41). **The gate guarding that menu was measuring a constant:** it asserted
`jumps.all.intersections === 4`, in as many words, so the first correct fifth control point this
project ever committed turned a working menu red on mobile PART 8. That is the same fault the
menu was built to avoid, one level up â€” changelog v54 states that no intersection coordinate is
copied into the interface *precisely* so that correcting the control changes the menu on the next
compile. The assertion now reads the compiled list: `main.js` exposes `api.intersections` beside
the `scene.anchors` the very next assertion already reads, and the check compares the menu's
count to it (`> 3` keeps the floor).

Files: `data/traces/street_control.json` (the control point, plus `streets.franklin` named and
`streets.south_water`'s "no committed control point anywhere on it" retired),
`data/streets/1835.json` (`south_water` and `franklin` notes), `renderers/web/js/main.js`
(`api.intersections`), `tools/smoke_renderer.mjs` (the literal `4` retired), recompiled sidecar
index, published mirror, changelog v310.
## Settled 2026-08-28 â€” T-0134: the south bank at the Dearborn reach has no ground the plate's warehouses could stand on, and the reason it was refused was wrong

Image 3 of the owner's brief of 2026-08-18 draws low warehouses on **both** banks of the reach
below the Dearborn draw. T-0133 built the north side â€” four freight sheds standing back from
North Water Street â€” and left the south side empty on one sentence, repeated in all four
records: *"the platted South Water Street corridor reaches to within about 1.7 m of the traced
1834 waterline at the Dearborn reach, so there is no ground there."* That was **one spot
reading taken by hand at one station**, and the whole bank of the reach was refused on it.

`tools/measure_south_bank_ground.py` is that refusal as a command. It walks the south bank from
the Dearborn crossing (local E 699.2, the bridge's own committed position) east to the United
States Reservation's west line (E 842.0, the line `measure_no_build_ground.py` already resolves
from the State & Madison section corner) and asks whether the **smallest footprint family F1
allows** â€” 18 Ã— 32 ft, the freight shed of the plate â€” can be put down at **any bearing** on
ground that is dry in the committed heightfield, outside every platted corridor and off refused
ground. Every bound is the permissive one, and the relief clause is reported four ways so the
answer can be seen not to rest on it.

```
  124 of 143 stations carry ANY dry ground outside a platted corridor
  widest such strip   26.50 m at E 813.2 (1.30 m of relief)
  positions the smallest F1 footprint stands at, at any bearing:
     relief <= 0.30 m   0        relief <= 1.00 m    6
     relief <= 0.35 m   0        no relief clause   26
  BESIDE THE PLATTED STREET (west of South Water's own east end, E 805.0):
     widest free strip  8.00 m at E 804.2
     relief <= 0.30 m   0        relief <= 1.00 m    3
     relief <= 0.35 m   0        no relief clause    3
```

**The refusal holds, and it holds much harder than 1.7 m did â€” but "there is no ground" was
false.** 124 of 143 stations do carry dry ground outside a corridor, and beside the platted
street the free strip widens eastward to 8.00 m. What defeats a building is the **slope**, not
the width: that strip is the river bank itself, and the three positions on it that accept a
footprint at all span 0.96â€“0.98 m of relief, more than three times the 0.30 m walker step
tolerance three infill generators hold themselves to. The 26.50 m strip at E 813.2 is **east of
South Water Street's platted end** â€” the slough's east bank, under `slough_log_bridge` â€” and
answers a different question, which is why the tool reports the two apart.

**What is now open is a decision, not a number.** The platted 80 ft corridor occupies this bank
down to the water, and L79 records the travelled tracks running 5.8â€“10.5 m inside an 80 ft
corridor; South Water's committed track is 10.5 m, so about 7 m of legal corridor stands between
the wheel line and the corridor's north edge, on ground flat to 0.05 m. So the question is
whether an invented building may stand on the **river margin of a platted street corridor**,
where this town's warehouses and landings in fact stood. It would be the first record placed
knowingly inside a corridor â€” the 29 that lap one today are documented records the plat was
fitted around â€” and `measure_corridor_intrusion.py --gate` refuses a new lap by construction.
Filed as its own ticket rather than decided here. The live alternative is that what the plate
draws on the south bank is wharfed out over the water (T-0059), not standing on it.

**What shipped.** `tools/measure_south_bank_ground.py` + its baseline, gated in `check.sh` so
a fit **appearing** fails â€” that is the question re-opening, not a number to bank; the finding
at `docs/RESEARCH/south_bank_dearborn_ground.md`; a `data/exclusions.json` entry, so the
visitor standing in the empty south bank can read why it is empty in the walkthrough's *What is
not here*; and the superseded sentence corrected in all four north-bank shed records.

**Nothing in the town moved.** No geometry changed and no bake was needed.
## Shipped 2026-08-28 â€” T-0221: one reading of which evidence layer a record belongs to

**Three tools asked the question and one of them answered it from a filename.**
`tools/measure_street_frontage.layer_of` decided whether a structure record was
`research`, `inferred_household` or `reconstruction` **by its id prefix** â€” `recon_1835_*`,
`inf_*`, everything else research â€” and `tools/measure_frontage_fabric.py` and
`tools/measure_corridor_intrusion.py` both import it. `tools/plat_occupancy.researched_ids`
already read the RECORD instead, and said in its docstring why. Two readings of one fact is
this project's recurring defect; there is now one, in
`plat_occupancy.layer_of_record`, and it reads the record.

**The record already carries the answer, as a rule rather than a convention.**
`data/structures.schema.json` states it â€” *"Named/documented structures do not carry this
block"* â€” and its `reconstruction.status` enum names which programme wrote the ones that do:
`inferred_anonymous` is a count-unit of the 665-roof programme, `inferred_household` a roof
raised because an argued household needed somewhere to be. So the layer is read off that
block, and `layer_of` is a lookup into it rather than a second opinion. An id carrying no
committed record is now REFUSED rather than guessed at from its shape; the one caller that
built a record in memory (`measure_frontage_fabric._synthetic`) builds it with the
`reconstruction` block its layer follows from, so its fixture is read the same way the tree is.

**Across all 349 committed records the two readings disagree exactly once**, and the run's
self-test measures that rather than quoting it. `physicians_office` carries neither prefix and
is a product of the inferred-household programme, which its own
`reconstruction.status: "inferred_household"` says. Its record was never wrong; the reading of
it was.

**Why one row of a census was worth a ticket.** `measure_corridor_intrusion.py --gate` holds
two different kinds of assertion. The 20 documented laps are a RATCHET â€” a depth may not grow,
and a repair is banked with `--write-baseline`. The generated layers are an ABSOLUTE â€” **zero**,
because every generator already refuses a roof in a roadway through the same module. A generated
record reading as `research` is scored against the ratchet instead of the absolute, so the
clause that cannot be crossed could have been crossed by a record whose filename happens not to
start with `inf_`. Nothing in the tree was ever mis-scored: `physicians_office` laps no corridor,
and the gate reports the same 20 phases and the same zero before and after.

**The gate now proves that itself.** `tools/measure_corridor_intrusion.py --self-test`, in
`check.sh`, translates a roof onto the Lake Street centreline in memory â€” position point and
world polygon together, with the depth computed by `measure()` rather than typed in â€” and checks
which assertion fires. An anonymous `recon_1835_*` roof is caught by the absolute (the control,
which the old reading also caught). `physicians_office` in the same roadway is caught by the
absolute now, and under the id-prefix reading â€” kept in the module, refuted, so it stays refuted â€”
is caught only by the ratchet. That is the difference the ticket bought, demonstrated rather than
argued.

**What moved in the numbers**, re-derived and stated because a census is not a place to be quiet:

```
  measure_corridor_intrusion --gate   20 of 349 lapping, 0 generated   unchanged
  measure_frontage_fabric --gate      3 principal streets, no failure  unchanged
  measure_street_frontage             lake   research 17 -> 16, household 7 -> 8
                                      clark  research  6 ->  5, household 1 -> 2
```

`physicians_office` stands within 25 m of both centrelines, so it moves column on both â€” one
building leaving the documented count of the street the face rule is usually asked about. Lake is
still the better face by a wide margin and no parcel's conclusion turns on it; the count is
simply now the count of what the records say.

## Shipped 2026-08-27 â€” T-0196: three Lake Street buildings come onto the plat, and the fourth is refused with the number that refused it

The Lake Street half of the repair T-0198 and T-0199 made on South Water. Four documented
records stood out past their own frontage line, in the platted roadway, because their
cross-street coordinate was taken off a **modern OpenStreetMap kerb line** rather than off this
project's committed 1835 centreline. `tools/generate_frontage_works.py`'s march refuses every
step a wall stands on, which is why Lake Street's north side came out in stumps.

**The four, measured on the march rather than estimated.** Each repair is the record's own
method run against this project's own line: translate along the block face's inward normal
until the street wall stands `LOT_MARGIN_M` (1.50 m) back from the committed frontage line.
No `local_e` moved â€” the along-street coordinate is the axis the sources argue.

| record | face | out past the line | moved | steps of walk it refused |
|---|---|---:|---:|---:|
| `old_bank_building` | `blk_lake_lasalle` north | 1.62 m | **3.124 m** | 4 |
| `dole_warehouse_south` | `blk_lake_dearborn` north | 1.28 m | **2.784 m** | 3 |
| `st_marys_church` | `blk_lake_dearborn` north | 3.03 m | **4.532 m** | 2 |
| `first_presbyterian_church` | `blk_lake_lasalle` north | 1.90 m | **refused** | 2 |

**What it did to the town's street edge**, re-derived and read off the record:

```
  walk        2,468.3 m in 33 runs  ->  2,499.5 m in 34 runs
  crossings   25 (596.2 m)          ->  29 (689.1 m)
  decks       140                   ->  142
  refusals    68                    ->  66
  wall-refused march steps in the town   13 -> 4
```

Two new corner crossings on Lake Street's north side (`blk_lake_clark Ã— blk_lake_dearborn`,
`blk_lake_wells Ã— blk_lake_lasalle`) and two more on the South Water faces those walks now
reach the corner of. `blk_lake_dearborn` north goes from 36.3 m to 51.8 m in one run;
`blk_lake_lasalle` north from 57.3 m to 72.9 m in two, the break being its own ground and not a
wall. `tools/measure_corridor_intrusion.py` banks two records cleared outright (22 lapping
phases to 20); `st_marys_church` stays in the census on **State** Street, which is a cross-street
lap and a different ticket.

**THE FOURTH IS REFUSED, AND THE NUMBERS ARE WHY.** `first_presbyterian_church` needs 3.395 m.
`physicians_office` stands 3.15 m behind it on the lot it would come onto:

| move along the inward normal | gap to `physicians_office` |
|---:|---:|
| 0.0 m (as committed) | 3.15 m |
| 0.2 m | 2.95 m â€” inside the 3.0 m separation gate |
| 3.2 m | 0 â€” the footprints overlap |

There is no translation along this normal that both clears the walk and leaves the pair apart.
**The owner's 2026-08-27 business-front clause does not reach it**, and that was measured rather
than assumed: the clause is bounded to a lot named in its block's own `frontage` run, and
`blk_lake_lasalle` has no frontage run at all â€” its roofs came from the pre-plat South Division
parcel. So nothing committed says what happens when a **documented** building's correct position
is held by an **inferred** one. Filed as **T-0251**, `blocked-owner`, with the three options and
the figures. The record's own `position.note` carries the refusal, so a visitor opening the card
reads it.

**Nothing else moved.** The three reconciled records keep their confidence grade â€” re-deriving a
coordinate from better geometry is not new evidence â€” their block, their corner, their side and
every uncertainty they state. No gate was weakened, no threshold moved, and no roof left the
town: all three seat on lots that already carry anonymous roofs, and the nearest of those stands
6.99, 7.11 and 8.14 m away, clear of the 3.0 m the separation gate asks.

**Also found, and filed rather than folded in:** T-0196's own count of "eleven refused steps,
all on Lake Street" was read before T-0240 laid Randolph. Re-read after it, the town carried
thirteen â€” the other two are `log_jail` on `blk_randolph_lasalle`'s north face, 3.48 m into the
Randolph corridor with its centroid inside. **T-0246.**

**The smoke's pinned frontage census moved with the walk**: walks 42â†’43, crossings 28â†’32,
refusals 74â†’72, meshes 53â†’54 (one culling chunk per run of sidewalk). Shape, not threshold â€”
nothing here is a gate being loosened.

**Verified in the foreground on the branch.** `./tools/check.sh` **PASS** â€” which is the dev gate
(`docs/PIPELINE.md`: "the dev gate is `check.sh` and nothing else"). Smoke against the published
mirror, **mobile 390Ã—780, all nine parts**: `1-2` 147/**1**, `3-4` 114/0, `5-6` 43/0, `7-9`
151/**1**. Smoke **desktop 1280Ã—800**: `1` 76/0, `2` 80/**1** â€” and every assertion this branch
touched is green in it, including *Lake Street's walk is continuous and walkable end to end* and
*a board crossing carries the walker over the road at the corner*. Zero page errors at both
viewports.

**The three failures are two, and both are `dev`'s with tickets already filed.** The Sauganash
hitching-post check is **T-0244** (T-0194's twelve street-edge posts resolve to an empty vertex
set; the two Sauganash posts still measure correctly, and this branch moves no post â€” the
census still reads 15 posts, 12 of them hitching). The tree-station check is **T-0243** (T-0223's
`BatchedMesh` renamed `timber__q0â€¦q3` to `timber`, so the gate's regex matches nothing; no tree
moved). Neither is touched here.

**The desktop ceiling sweep was taken with `tools/measure_detail_ceilings.mjs`** rather than
desktop stage 4, which does not fit the ten-minute foreground command ceiling on this runner and
which `tools/dev-smoke-state.json` records as FAIL on `dev` itself at `2026-08-27T20:16` (the
T-0210/T-0215 loaded-box failure). Every tier is inside its ceiling with the new boards laid:

| tier | ceiling | worst stand | clear by |
|---|---:|---|---:|
| `full` | 1,400,000 | 1,372,635 â€” the forks, from Wolf Point | 27,365 |
| `balanced` | 1,210,000 | 1,204,048 â€” the forks, from Wolf Point | 5,952 |
| `light` | 785,000 | 746,028 â€” Lake Street at Canal | 38,972 |

Mobile's own ceiling sweep is inside stage `3-4`, which passed 114/0. **No ceiling was moved for
this**, and the balanced margin of 5,952 is worth reading beside T-0241: Washington Street still
does not fit, and 31 m of Lake Street walk did not make it fit.

**RE-VERIFIED AFTER MERGING `dev`** (#417 T-0195, #419 T-0213, #420 T-0182 â€” the last of which
moves two Lake-face buildings 8 cm, so the re-take is not a formality). `./tools/check.sh` PASS.
Desktop stage `2` 80/**1** â€” the same inherited T-0244 and every touched assertion green. Both
ceiling sweeps re-taken on the merged mirror and unchanged to the triangle: desktop
1,372,635 / 1,204,048 / 746,028 against 1,400,000 / 1,210,000 / 785,000; mobile
1,274,689 / 1,150,060 / 695,154 against the same three. The frontage census the smoke pins
re-derives identically on the merged tree â€” walks 43, crossings 32, refusals 72, meshes 54 â€” so
`dev`'s geometry did not move this layer.

**And once more after #421 (T-0193) landed on `dev`**, which is the last thing to merge under
this branch: `./tools/check.sh` PASS, desktop stage `2` 80/**1** (the same inherited T-0244),
desktop ceilings 1,372,635 / 1,204,048 / 746,028 â€” identical to the reading above, because that
ticket refused its block rather than laying it. The frontage census re-derives at walks 43,
crossings 32, refusals 72, meshes 54 for the third time.

**AND ONCE MORE AFTER #423 (T-0241, Washington Street) landed on `dev`** â€” a whole street of
boards arriving under this branch, so the street edge was **re-derived** on the merged data
rather than hand-resolved, and every figure re-taken. The deltas are additive and the pins now
carry both: walks 49â†’**50**, crossings 33â†’**37**, refusals 83â†’**81**, meshes 61â†’**62**; fences
(35) and posts (15) do not move, because a wall 1.50 m back from the frontage line is still
inside the 3.0 m a street fence needs. Town street edge on the merged tree: **3,160.3 m of walk
in 41 runs, 34 crossings, 35 fence runs, 249 walking decks, 36 block faces.**

`./tools/check.sh` PASS. Desktop stage `2` 80/**1** â€” the inherited T-0244, every touched
assertion green. Mobile stage `3-4` **116/0**, which is the ceiling sweep AND the draw-call
budget at the worst frame. Desktop ceilings with both streets laid:

| tier | ceiling | worst stand | clear by |
|---|---:|---|---:|
| `full` | 1,400,000 | 1,388,091 â€” the forks, from Wolf Point | 11,909 |
| `balanced` | 1,210,000 | 1,197,398 â€” the forks, from Wolf Point | 12,602 |
| `light` | 785,000 | 761,528 â€” Lake Street at Canal | 23,472 |

**No ceiling was moved, by either ticket.** Worth recording beside T-0247, which is `dev`'s:
`light` reads **85** draw calls at Lake and Market on the desktop sweep against the 80-call
floor T-0147 restored. That ticket measured 83 on an unmodified `dev` before Washington; the
sweep above is the first reading with both streets on it. The mobile gate that actually asserts
the budget is green (116/0), and this branch adds **one** culling chunk â€” the forty-first run of
sidewalk â€” to a street edge that grew by eight under #423.

## Shipped 2026-08-27 â€” T-0213: the trade families are weighted onto the business front

The surviving half of ROADMAP **K29**. T-0022 refuted the other half â€” the schedule may deal log
cabins to commercial frontage, and the fault there was an arrangement rule, not the programme â€”
and it left this one standing: the 662-roof schedule apportions families **by district** and has
no notion of a street, so a block dealt a South Water face was no likelier to be dealt a store, a
warehouse or a workshop than a block two streets back.

**The measurement, and it is the reason this is a term rather than a preference.** The share of
DOCUMENTED buildings carrying a trade family (`C` stores, `F` warehouses, `W` workshops) is
**monotone in the committed street hierarchy** â€” the `traffic` field on `data/streets/1835.json`,
sourced there to Andreas by way of `chicagology_prefire233`. 68 records, joined to the committed
`likely_family` reconciliation and assigned to the street each footprint stands nearest by the
same census `tools/measure_frontage_fabric.py` already ran for T-0022:

| street class | documented buildings | trade | share |
|---|---:|---:|---:|
| `principal` | 27 | 21 | **0.7778** |
| `ordinary` | 22 | 10 | **0.4545** |
| `light` | 19 | 0 | **0.0000** |

The ordering survives the obvious sensitivity: add the lodging families and it reads 0.8889 /
0.6364 / 0.0526. Nobody had ever asked the street list this question; `--trade` prints both
tables so the choice of letters can be checked rather than taken on trust.

**Research layer ONLY**, which is what makes it a measurement instead of a ratchet. Weighting the
schedule by what the schedule invented would be the programme grading its own homework, and the
share would climb with every block built.

**What shipped.** A block's weight is the mean of its own four faces' class shares, so
`blk_south_water_franklin` reads 0.6162 and `blk_randolph_market` reads 0.4217 without anybody
typing a number for either â€” and re-classing a street on `data/streets/1835.json` re-weights every
block on it in the same commit. `tools/reconcile_665.py` then re-deals each district's principal
families across its platted blocks at those weights, by Hamilton, clipped to the principal slots
each block actually has.

**It is a PERMUTATION, and that is asserted rather than trusted.** Three checks run on every
`--check`: the multiset of families over a district's blocks is identical before and after, every
block keeps the exact principal roof count the district deal gave it, and no roof is left unplaced.
So no total moves â€” not the 662, not a district, not a family, not any block's roof count or its
ancillary mix. It changes only *which* block gets *which*.

**Seven of the south's platted blocks changed deal.** `blk_south_water_franklin` and
`blk_south_water_lasalle` held twelve of the business front's roofs between them and not one
store, warehouse or workshop; each now takes one. `blk_south_water_market` â€” three principal
faces of four, the highest weight on the grid at 0.6970 â€” goes from four trade roofs to five.

**Nothing you can see changed today**, and the visible-progress rule is answered by naming what
this precedes rather than by dressing it up: every future block build reads this schedule, and a
block once built is a committed record. T-0028's next anonymous block and the four open South
Water and Lake units are the parcels it stands in front of.

**Verified in the foreground on the branch.** `./tools/check.sh` PASS â€” *which is the dev gate*
(`docs/PIPELINE.md`: "the dev gate is `check.sh` and nothing else"), and it re-runs
`reconcile_665.py --check`, so the permutation assertions above are gate-carried. Smoke, published
mirror: **mobile 390Ã—780 stage 7-9** 151 passed / 1 failed, **desktop 1280Ã—800 stage 8** 37 passed
/ 0 failed (the stage that reads the changelog â€” the only renderer-facing file this branch
touches). The one mobile red is **T-0243**, inherited: reproduced identically in a clean
`origin/dev` worktree in this same run, 151/1 with the same single failure. No structure record,
no GLB, no renderer module and no scene data moved, so no bake.

## Shipped 2026-08-27 â€” T-0147: the `light` ceiling comes back DOWN, 1,050,000 â†’ 785,000

The third and last piece of **T-0149**, and the one the other two existed to make possible.
T-0135's five-stand re-basing on 2026-08-22 lifted all three ceilings at once and left `light`
carrying **1,050,000** â€” more than `full` had promised the day before â€” so the tier a weak
machine boots into was not a floor anybody could be promised. T-0150 (furniture distance-culled
at `light`, 350 m), T-0146 (far chunks merged back into single draws) and T-0223's timber cull
each trimmed the axial view without touching the picture. **A ceiling that comes back down after
a trim is the strongest evidence the trim worked**, and this is that.

**Measured before it was moved**, which is why T-0147 was a separate ticket from the trims.
`tools/measure_detail_ceilings.mjs`, published mirror, T-0135's five stands, **both** release
viewports, `dev` @ `f7aca445` (after T-0194's hitching posts merged):

| tier | ceiling before | desktop 1280Ã—800 | mobile 390Ã—780 | ceiling now |
|---|---:|---:|---:|---:|
| `full` | 1,425,000 | 1,252,879 | 1,145,313 | untouched here â€” T-0229 restored it to 1,400,000 |
| `balanced` | 1,260,000 | 1,084,292 | 1,020,684 | untouched here â€” T-0229 restored it to 1,210,000 |
| `light` | 1,050,000 | **703,610** | **649,296** | **785,000** |

Worst `light` draw calls: **76** desktop (Lake and Market), **69** mobile.

**Where 785,000 comes from**, so it is a principle rather than "enough for today": it gives
`light` the same proportional headroom over its own measured worst stand that `full` carries
over its â€” 1,400,000/1,252,879 is 11.7 %, and 785,000/703,610 is 11.6 %. It is a worst-stand
number, not a reference-stand one. And it is **21.5 % below the 1,000,000 `full` promised before
2026-08-22**, which is the sentence T-0149 was opened to answer.

**The draw-call promise comes back as a COUNT.** `tools/smoke_renderer.mjs`' check that held
`light` inside **80** calls was weakened to a ratio on 2026-08-22, and its own comment asked
T-0147 to turn it back: *"a count is what a promise to a person looks like."* It is 80 again â€”
the number chosen before any of the 2026-08 content landed, not one fitted around today's 76, so
there are **four** calls of room. Thin on purpose and thin in fact: this branch read **75**
before T-0194's hitching posts merged into `dev` and **76** after, so one ordinary visible parcel
spent a quarter of the margin between two readings an hour apart. That is the bar working. When
it goes red the answer is a trim or an argued re-budget at `DETAIL` â€” never a weakening of the
assertion, which is the move T-0223 forbade by name. The ratio check is **kept underneath** rather than replaced: the
count is the promise, the ratio is the claim that the scene-detail control is not decoration.

**What this deliberately does NOT do.** `full` and `balanced` are untouched â€” taking T-0229's
raise back out was that ticket's own change with its own reading, and it merged from a parallel
slice while this was being gated â€” this one does not reach across it. Nothing in the renderer moves: no geometry, no reach, no shadow tier, no cull. The
only edits are one constant, one gate assertion, their reasoning, and the changelog.

**Verified in the foreground on the branch.** `./tools/check.sh` PASS â€” *which is the dev gate*
(`docs/PIPELINE.md`: "the dev gate is `check.sh` and nothing else"). Smoke at **mobile 390Ã—780,
all nine parts**: `1-2` PASS (148/0), `3-4` PASS (114/0, printing `light 434366/785000`), `5-6`
PASS (43/0), `7-9` 151 passed / **1 failed**. Smoke at **desktop 1280Ã—800** stage `6` PASS (23/0)
â€” boot, canvas, **zero page errors**, vendor.

**NOT verified, and stated rather than glossed:** desktop smoke stage 4 â€” the stage that holds the
ceiling sweep â€” **could not be taken on this runner.** It exceeds the ten-minute foreground command
ceiling, and `tools/dev-smoke-state.json` records `dev`'s own desktop stage 4 as FAIL at
`2026-08-27T20:16` (`page.click: Target page â€¦ has been closed`, the T-0210/T-0215 loaded-box
failure). The desktop half of the sweep is covered instead by `tools/measure_detail_ceilings.mjs`,
which is documented and verified to reproduce that gate's figures to the triangle and to the draw
call â€” a substitute for the instrument, not for the stage.

**One red, proven inherited, filed as T-0243.** `mobile: every tree drawn stands at its own
station` fails â€” and fails identically on a clean `origin/dev` worktree. `smoke_renderer.mjs`
traverses `/^timber__/`; T-0223 replaced `timber__q0â€¦q3` with one `THREE.BatchedMesh` named
`timber`, so the regex matches nothing and the check fails its own `meshes > 0` liveness clause.
No tree moved. Its sibling â€” `no timber is drawn out in the channel` â€” is *passing on the same
empty traversal*, which is the worse half. `dev`'s standing record reads PASS for mobile 7-9,
taken five minutes before T-0223 merged.

## Shipped 2026-08-27 â€” T-0216: dev has a standing smoke result, and a red can be attributed without re-running it

**Four runs in one day re-derived the same two reds by hand.** `chicago-4d-check.yml` runs
`check.sh` and nothing else, and `chicago-4d-smoke.yml` is dispatch-plus-one-path, so the smoke
state of `dev` was whatever the last agent happened to run in a worktree. The question every
branch asks â€” *"is this red mine, or did I inherit it?"* â€” cost a clean `origin/dev` worktree and
a ten-minute stage, every time it was asked. On 2026-08-27 three runs paid it on the What's-new
stage and a fourth on the desktop triangle ceiling, and the first of those turned out to belong to
neither branch nor `dev`: it was the machine (T-0215's frame timings â€” 0.46â€“1.10 s per frame on a
quiet box, 17â€“27 s on a loaded one).

**`tools/dev-smoke-state.json` is the record; `tools/dev-smoke-state.mjs` writes and reads it.**
`ask --viewport desktop --stage 8` answers the question from the file, running nothing.

**It is fed by the two routes a run already has, and that is a constraint, not a preference.**
`.github/workflows/` is outside a steward run's scope (`AGENTS.md` Â§ How work ships) â€” the exact
reason T-0215 could not build this in its own PR â€” so the record is not a new scheduled job. A
local smoke log and a `chicago-4d-smoke.yml` run's log go through **one parser**: `record <log>`
and `ci <run id>`. If the owner later schedules that workflow on `dev`, `ci` is what folds its
result in and nothing in the tool changes.

**A verdict without its conditions is what sent three runs chasing a machine, so every reading
carries them** â€” host kind, CPU count, load average, wall clock, and any animation-frame cost the
smoke printed after a timeout. A CI pass on a quiet runner *dates* a steward-runner red; it does
not overrule it.

**And every reading carries a hash of what the smoke actually exercises**, so it can be attributed
rather than merely dated. `renderers/`, `data/`, `assets/`, `tools/smoke_renderer.mjs` and the
published mirror, from the git index. Match it and the reading is a reading *of your tree*: the red
is inherited, provably, with nothing re-run. Three files every branch changes **by construction**
would otherwise have made the hash differ before any real work was done, and each is handled for a
different reason â€” `tickets.json` is dropped (`ticket.mjs claim` mirrors it in the first commit,
and nothing in the renderer reads it); the changelog is hashed **apart** and reported against
part 8 alone, which is the only part that reads it; and `publish.sh`'s build stamp is **normalised
out** of the gate page rather than the page being dropped. **Verified, not asserted:** this branch
and `origin/dev` hash identically â€” `sha256:0d99bf7ecdf56cd1` â€” with a changelog entry, a claimed
ticket and a fresh publish stamp between them.

**Seeded with what this run measured, on a quiet box, and it says so.** Four `--published` runs,
all green, on a 4-CPU runner at load 3.7â€“6.1: mobile 1â€“2 in 4 m 17 s, mobile 7â€“9 in 8 m 19 s,
desktop 8 in 2 m 34 s, desktop 9 in 3 m 52 s. Seven of the eighteen viewport-parts.

**Two of those four are readings somebody wanted.** Desktop part 8 is the stage T-0215 watched die
on its FIRST click at 90 s â€” it passes here in 2 m 34 s on the same tree, which is the factor-of-
twenty story in two lines of the record rather than a day of re-derivation. And desktop part 9 is
T-0210's *"stage 9 times out clicking the panel close, on an unmodified tree"*: it did not time out,
it passed in 3 m 52 s at load 3.7. That does not refute T-0210 â€” it dates it and gives it the
counter-reading it never had, which is a fact for whoever takes that ticket rather than a verdict
from this one.

**All three verdicts are exercised, not just the happy one.** `pass`, `fail` and `killed` were each
driven through the parser before merge. `killed` is deliberately NOT reported as inherited even when
the hash matches: a kill is a statement about the machine the browser starved on, and collapsing it
into "the red is yours/not yours" would rebuild the exact wrong answer three runs already gave.

**What is NOT in it yet, stated rather than implied.** The CI half is unread: `ci 32689397335`
would fold in the last unfiltered `chicago-4d-smoke.yml` pass on `dev`
(2026-08-24T04:16Z, `97ac4c8563cb`, success, both viewports) and GitHub rate-limited this account
twice while trying. The code path is exercised â€” `ci` with no argument lists the four runs â€” and
the tool now exits 3 with one sentence instead of a stack trace when the limit is hit. Fold it in
on the next quiet run. The eleven viewport-parts nobody measured today report
*"no reading â€” nobody has recorded this one"*, which is the honest answer and not a gap being
hidden.

**It is a record, never a bar.** Nothing here fails a gate, refuses a merge or excuses a red â€” the
shape `tools/road_band_baseline.json` is kept in (T-0016).

## Shipped â€” T-0058: a wharf deck is a floor, and there are steps up onto it

**Seven docks stood in this town as scenery.** `terrain.walkHeight()` puts a wading barrier at
4.0 m over open water and no wharf deck overrode it, so a visitor could see a wharf, aim at it,
open the warehouse it serves â€” and never set foot on it. The bridges have been standable since
T-0001 by a route a wharf cannot take: `placement.walk_surface_m` lives on a sidecar, and a wharf
carries no structure record at all.

**So the LAYER publishes what it drew.** `createWharves` returns `decks` in `decksFrom()`'s own
`{ id, y, pts }` shape at the `deck_top_m` each slab was built at, and `main.js` pushes them into
the array `createWalker` holds by reference â€” after `planting` is taken, so the planters are not
handed the same rectangle twice. Inventing a record to carry a height would have been a SECOND
opinion about a number `wharves.js` already knows, which is the fault T-0001 found 1.8 m over the
North Branch planks.

**Publishing the deck is the half that is easy to declare done.** Measured at load on this
terrain: deck tops **0.90 m at all seven** â€” the record's freeboard floor, because every bank is
under it â€” over heels at **0.117â€“0.575 m**. That is a **0.325â€“0.783 m** riser against the walker's
0.35 m step-up rule, and **six of the seven decks were unboardable** at the moment they became
walkable. A dock a visitor can walk ALONG and cannot get ONTO reads as a broken model.

**The answer is a boarding stair, and not a regrade.** The other honest reading is that the banks
were filled to deck level, and that is a claim about the LAND â€” it moves the terrain record and
needs a bake. The stair invents only timber this layer already draws: 2.4 m across, 0.75 m of
going, dividing whatever rise the ground leaves it into equal treads under the record's 0.30 m
ceiling. How many treads is the terrain's answer at load and is authored nowhere â€” **one** at
Kinzie & Hunter's and at Robert Kinzie's, **two** at the five South Water landings, twelve in all.
`data/wharves/river_landings.json` gained `boarding_stair_width_m`, `_tread_m` and `_rise_m` and no
stair height; **L195** records the invention and what bounds each figure.

**One thing found on the way, filed rather than fixed (T-0228).** Carpenter's and Jones's decks tie
their heels back into bank the riverside plank walk already runs along: about 2,700 frontage
vertices lie inside those two deck outlines and 270 inside their stairs. None of that geometry
moved â€” but the deck is a registered floor now, so the walk meets a 0.50 m riser at the deck's edge
and the way up is the boarding stair, which at those two rises off the plank walk itself. Truthful,
and nobody chose it. `tools/smoke_renderer.mjs` excludes wharf decks from the frontage layer's
tie-into-the-ground probe for that reason â€” a board under a dock is not a board riding one â€” which
is right for that check and is not an answer to the question.

**Verification.** `tools/check.sh` **CHECK PASS**. `tools/smoke_renderer.mjs --published`, the full
staged gate at both viewports: desktop parts 1â€“9 and mobile 1-2, 3-4, 5-6, 7-9. Three new checks in
the wharf section â€” the layer publishes every plank it drew at the height it drew it (19 surfaces:
7 decks, 12 treads); no tread rises past the record's ceiling or the step-up rule; and **the walk
itself, all seven docks, 0 blocked strides, worst stride 0.205 m**, each ending on the planks over
open water with the barrier 3.1 m above its head.

**One failure, and it is dev's, not this branch's.** Desktop part 4's `full` and `balanced`
scene-detail ceilings are breached at Lake Street at Canal. Measured on this runner in this session
against `origin/dev`'s own published mirror: dev **1,410,456** tris of 1,400,000, this branch
**1,410,744** â€” the twelve treads are **+288 triangles on a frame already 10,456 over**. (`balanced`
came in *lower* here than on dev, 1,225,457 against 1,251,361, which is the vegetation deal's own
spread and not a saving.) The queue already owns it: **T-0089**, **T-0146**, **T-0147**.

## Shipped 2026-08-24 â€” T-0112: the anonymous roofs get their own siding stocks, dealt in their recipes

**The state before, counted rather than asserted.** T-0049 dealt 24 named frame buildings a
`siding_exposure_m` from four period mill stocks and could reach no further: the other 131
clapboard frame roofs in the scene re-derive byte-for-byte from `tools/generate_block_infill.py`
and its four kin, so a value written into those records by a second tool is drift on the next
run. All 131 wore the archetypes' 0.14 m, and **every one of the 186 anonymous pairs standing
within 60 m of each other wore the same board â€” 186 of 186, 100 %.** No anonymous roof, of 131,
differed from its nearest neighbour.

**The refutation that decided the rule, and it is the third time this dataset has hit it.** The
obvious move was to run L148's own key inside the recipes: base stock from the phase's
construction season, `(year + quarter) % 4`. Measured on the records: **all 131 anonymous roofs
carry `documented_range.from = 1835-01-01`** â€” the programme's count-unit convention, not a
construction season, the same literal on every one of them. That key deals all 131 ONE stock. It
is the archetypes' single course put back one step over, a range collapsed to a point â€” T-V1's
sixty identical North roofs and T-0142's one-pitch-per-family, a third time. So the base is
DRAWN from the four-stock list on the record's own stable key (slot 11; 1-10 are spoken for),
exactly as `tools/family_bands.py` draws a footprint, an eave and a pitch from the crosswalk's
authored ranges, and then advanced by the same 60 m rule L148 already uses.

**Where the deal lives.** `tools/siding_stock.py` â€” the set, the separation distance, the advance
and the recipe post-pass, in one module, imported by all five generators AND by
`tools/deal_siding_stock.py`, so the two populations cannot drift apart on what a board is.
Each recipe calls `deal_records()` at the END of `records_from_inputs()` (after
`place_on_frontage()` in the South parcel, which moves buildings), because the stock is the one
form value that depends on where a roof's neighbours stand.

**Scope: 131 dealt, 4 left as neighbours, and the reason is a liberty and not an oversight.** A
recipe deals a roof only when the record carries a `reconstruction` block â€” the anonymous
`recon_*` count-units and the `inf_*`/`physicians_office` roofs raised for reconstructed
households, all of which docs/LIBERTIES.md L91 admits as inventions whole. The inferred-household
programme also regenerates four DOCUMENTED frame buildings (`heacock_house_monroe`,
`temple_lake_st_building`, `wright_building_to_let_a`, `wright_building_to_let_b`); those are
attested buildings, their liberty tokens are enumerated one by one, and inventing a board width
for a real building outside the entry that owns it is not this parcel's to do. They stay on
0.140 m and the deal counts them as the fixed neighbours they are.

**The trade that was measured, not assumed.** A recipe deals its OWN parcel. It could read the
other parcels' committed records and deal the town in one order â€” measured with the shipped rule,
that reaches **9 of 186** anonymous pairs sharing instead of 16, and moves 25 of the 131 roofs.
It was refused: it makes moving one North roof re-deal the platted blocks and restale their
meshes, so every future building costs a town-wide rebake. Seven pairs is not worth that
coupling, and the residual is written down rather than rounded off. Some sharing is unavoidable
in any case â€” four stocks cannot separate a roof with nine neighbours, and the densest stands
here have nine.

**The result.**

| | before | after |
|---|---|---|
| clapboard pairs within 60 m sharing a stock, whole town | 192 / 266 (72.2 %) | **21 / 266 (7.9 %)** |
| the same, anonymous roofs only | 186 / 186 (100 %) | **16 / 186 (8.6 %)** |
| anonymous roofs whose NEAREST neighbour hangs a different course | 0 / 131 | **120 / 131** |
| stock distribution (0.114 / 0.127 / 0.140 / 0.152 m) | 8 / 6 / 135 / 10 | **33 / 44 / 39 / 43** |

**What re-derived and what moved.** All five recipe `--check`s are green, so every one of the 131
values re-derives from its recipe. 146 structure records changed and **118 of the 159 clapboard
walls moved their stock; 41 did not** â€” 28 anonymous roofs were dealt the 0.140 m they already
wore and 13 named ones were unaffected. 15 of the 24 named records were re-dealt, because
`tools/deal_siding_stock.py` now reads what the recipes dealt each derived neighbour instead of
assuming 0.140 m for all of them (and no longer counts a vertical-board wall as a neighbour at
all â€” it exposes no course). **The bake ran here: 342 assets rebuilt, 118 GLBs changed, 224 came
out byte-identical**, derivatives and sidecars regenerated, published; the staleness gate is back
to 344 fresh, 0 stale.

**The new gate, and it was landed red first.** `tools/deal_siding_stock.py --check` was never in
`tools/check.sh` at all, so the named half's 24 values were ungated. It is a step now, and it
grew a second half: every invented clapboard frame roof in the town must carry a stock from the
set. The recipes' own `--check`s hold each value byte for byte but would not notice a recipe that
stopped dealing ALTOGETHER â€” a record with no `siding_exposure_m` is a perfectly well-formed
record; it just puts 131 walls back on one course, invisibly. Run against the tree before the
recipes were wired, the new step names all 131 by id and exits 1.

docs/LIBERTIES.md **L196** owns the invention and supersedes L148's sentence saying derived
records stay on the default.
## Shipped 2026-08-27 â€” T-0158: one line in the wrong order was extinguishing the AO, and the number the AO parcel aims at was wrong too

**Nothing in the town changed, and this run is exempt under AGENTS.md exemption 2** â€” the second
half of a split whose first half was a measurement. T-0015 measured the failure on 2026-08-23,
wrote the guard, demonstrated it firing, and then deliberately reverted it because T-0139 made any
edit to `build.py` unhealable. T-0139 is closed; this is the fix half, and it lands the guard.

**The fault, in one line.** `bake_ao()` set `img.colorspace_settings.name = "Non-Color"` *after*
`bpy.ops.object.bake(type="AO")`. Setting a colorspace on a GENERATED image that has no file
behind it and is not packed **frees the image buffer**, which then regenerates from
`generated_color` â€” black â€” and **clears `is_dirty`**, which is the flag Blender's own exporter
tests in `make_temp_image_copy()` before it will bother to carry unsaved pixels across. So one
statement destroyed the data *and* switched off the exporter's only rescue path. Moving it above
the bake is the whole repair.

**Measured on the bytes, not read off the code** â€” `sauganash_hotel`, 512Ã—512, 48 samples,
Blender 4.5.3, four bakes of the same asset, occlusion PNG extracted from the GLB and decoded
with a reader written for this and self-tested against all five PNG filter types:

| when the image is tagged `Non-Color` | in Blender's buffer after the bake | in the exported GLB | drift |
|---|---|---|---|
| **after the bake â€” as shipped** | min 0.000 max 1.000 mean **0.2158** | min **0** max **0** mean **0.0000**, all 262,144 texels | **100 %** |
| **before the bake â€” the fix** | min 0.000 max 1.000 mean **0.1665** | min 0.0000 max 1.0000 mean **0.1665** | **0.0 %** |
| bake, `pack()`, then Non-Color | mean 0.2158 | mean 0.2158 | 0.0 % |
| no colorspace change at all (sRGB) | mean 0.2158 | mean 0.2158 | 0.0 % |

The last two rows survive the export but are the wrong number, and that is the second finding.

**`Image.pixels` on an 8-bit buffer is RAW â€” measured, both directions.** Setting 0.1665 and
reading it back gives 0.1647 whether the image is tagged `sRGB` or `Non-Color`, and the saved PNG
byte is 42 either way (an sRGB *encode* would be 113). So the tag does not change how the buffer
is read; it changes what the **bake writes into it**. Under `sRGB` the bake stores the
sRGB-ENCODED occlusion; glTF samples an occlusion texture as `byte / 255` **with no transfer
decode**, so the pre-2026-08-27 path was shipping a map ~30 % too bright *before* it went black.

**Which means the AO parcel has been aiming at a number that is wrong twice over.** `bake_ao()`'s
docstring and ROADMAP R-W3a both quote **"mean 0.265, 69 % of texels below half"** (and 0.38 for a
shortened AO distance) as the reading that makes the Sauganash render brown when its white paint
is documented. Two faults:

1. **the gamma above** â€” those are sRGB-encoded readings, not occlusion;
2. **the population** â€” they are taken over the whole 512Ã—512 atlas, and **68.9 % of that atlas is
   empty UV space**. The famous "69 % below half" is very nearly the empty fraction itself. Most
   of what that figure counted was blank, not dark.

Re-measured from the exported file: atlas-wide raw mean **0.1665**, and over the **81,458** texels
the unwrap actually writes, **mean 0.5358 with 58.7 % below half**. The 0.38 figure carries both
faults and has not been re-measured at all. The *shape* of the concern survives â€” more than half
the written surface is below half occlusion â€” but the numbers behind every AO decision this
project has taken are void, and **none of them was ever read off a file that carried the occlusion
in the first place**. Corrected in place in `bake_ao()` and R-W3a; **T-0227** filed to answer the
question properly, from a rendered frame, before R-W3a builds a cage to improve a figure nobody
has measured correctly. T-0227 also carries the unwrap: an atlas two-thirds empty is two-thirds
of every occlusion map's bytes spent on nothing.

**What was NOT done, deliberately: `--ao` stays off.** It is opt-in and nothing passes it â€” not
`tools/bake.sh`, not `chicago-4d-bake.yml` (T-0015 established this). This ticket's job was the
mechanism; whether the result is *good enough to ship* is a different question, it is now
answerable for the first time, and it is T-0227. Turning the flag on in the same run that made it
work would be deciding that question by momentum.

**A cost figure R-W3a now has to answer first.** With the export working, `sauganash_hotel`'s
master goes **94,420 â†’ 202,292 bytes, +114 %**: a 512Â² occlusion PNG carrying real variation costs
~107 KB where the black one compressed to 3,620 â€” so T-0015's "+4.4 % file size" was measuring the
size of the *bug*, and is void. `assets/gltf/` is 27 MB; a 512Â² map on each of 348 masters adds
~37 MB. Textures do not meshopt, so the derivatives carry the same PNGs, and the published tree is
**23.53 MB against a 25 MB `SITE_BUDGET_MB`**. Texture size and how many assets get a map at all
are now the cage parcel's first questions, not its last.

**What fails when it recurs** â€” the ticket asked for this specifically, because it is the second
fault of this shape here and the first repair left only a comment behind.

- `generators/ao_export.py` reads the **exported bytes**: a pure-stdlib PNG decoder and GLB reader
  (no Blender; CI installs `jsonschema pyproj openpyxl pypdf numpy scipy Pillow` â€” the
  last three since T-1083, because without them thirteen raster steps skipped in silence).
- `generators/build.py` calls `assert_ao_survived_export()` the moment each GLB is written, and
  the manifest entry is written **only if it passes** â€” so `baked_ao: true` cannot outlive the
  occlusion again. It refuses a missing `occlusionTexture`, a uniform texture (whichever value it
  is uniform on â€” a white map is a bake that did not arrive just as much as a black one), and a
  mean more than 2 % from the bake's own reading, which is the arm that would catch the sRGB
  curve at ~30 %.
- `generators/ao_export.py --gate` runs in `check.sh` on every commit over all 348 committed
  masters in 0.27 s, and cross-checks the manifest **in both directions**: `baked_ao: true` with
  no texture, and a texture under `baked_ao: false`.
- `--self-test` breaks every arm in memory â€” 17 assertions, including the five PNG filter types
  round-tripping and a gradient of known mean reading back exactly.
- Proved on the real artefacts rather than only synthetically: the guard **refuses** the actual
  broken GLB (uniform 0.0000 over 262,144 texels) and **passes the fixed one on merit**.

**Gates: `tools/check.sh` PASS. The Playwright smoke was NOT run to completion, and that is
stated rather than glossed.** The only renderer file this change touches is `changelog.js` (one
entry), but three attempts at `SMOKE_STAGE=8` mobile against the published mirror gave two
timeouts and one browser kill, at 9â€“13 minutes for a stage that should not take that long â€” the
box was running ten agents at **load 48 with 105 concurrent Chromium processes on 4 cores**, and a
control run on unmodified `origin/dev` failed the same way. A loaded box makes the suite flap in
both directions, so nothing was concluded from it and no assertion was touched. What *was* proved,
with generous timeouts: an isolated probe of the exact What's-New assertions passed all eight â€”
273 entries render, the new entry appears with all six items, the unread marker clears, a
returning visitor is flagged only the newer entries, zero page errors. **CI's nine-stage run at
both viewports is the authority here.**

**The rebake, and what it cost.** `generators/mesh_inputs.py` hashes `build.py`'s bytes into every
asset's `inputs_sha256`, so this one-line reorder restaled all 346 structure masters. The full
rebake took **1 m 23 s** and every one of the 346 GLBs came back **byte-identical** â€” the only
change in `assets/` is 346 hash strings in `manifest.json`. Worth recording, because T-0015 could
not run that rebake at all (T-0139) and reverted a working guard rather than monkey-patch around
it: the healing route now works, and it is cheap.
## Shipped 2026-08-27 â€” T-0184: the ribbon's bends are mitred, and both joints the ticket named were wrong

**23.47 m2 of prairie inside the roadway, closed to 0.000, for 22 triangles.** `streets.js` built
every panel square to ITS OWN chord, so at a bend the row at a shared centreline point was emitted
twice â€” once perpendicular to the incoming chord, once to the outgoing one. The two rows crossed at
the centreline and splayed apart towards the edges: a triangle of unpainted ground on the outside of
the turn, `half * tan(turn/2)` long at the ribbon's edge, and a matching double-blended overlap on
the inside. Both are gone: the two panels now share one corner on the bisector of their chord
normals, `1 / cos(turn/2)` long, so neither a gap nor an overlap is arithmetically possible.

### The instrument, and its control runs on every build

`tools/measure_road_joints.mjs` (probe in `tools/road_joint_probe.mjs`, shared with the smoke the way
`drawn_placement_census.mjs` is): a **2 cm plan lattice** over every authored bend, each point
classified twice â€” inside the nominal ribbon, and inside any drawn street triangle in plan. Coverage
is asked of EVERY street, because a crossing street's roadway is roadway.

The control is not a `--refute` flag somebody has to remember: the same lattice is probed against a
**reference ribbon built here from the committed centrelines under the old square-joint rule**, with
the same 2.25 m sampling, the same waterline trim and the same sliver drop. So `square` is the wedge
and `drawn` is what is left, on every run, and a build where the reference reads zero is a build
where the tool says it has stopped being an instrument.

| | uncovered | drawn triangles |
|---|---|---|
| before | **23.472 m2** over 21 live bends | 22,596 |
| after | **0.000 m2** | 22,618 |

Each bend's reading agrees with the closed form `half^2 * turn / 2` to three decimals â€” 4.292 against
4.289 at South Water's worst â€” which is what says the lattice reads geometry rather than noise.

### Both joints the ticket named were wrong, in opposite directions

1. **South Water's west approach turns 17.8 deg at [120, -57], not at [140, -35].** The angle and the
   4.3 m2 were right and the coordinate named the next vertex along, which turns 7.4 deg for 1.77 m2.
2. **Dearborn's corner left 0.00 m2 uncovered, not L178's 0.30.** South Water Street's own 10.5 m
   roadway covers the WHOLE 0.61 m2 sector there, not half of it: the sector reaches at most 3.50 m
   from [698.93, 7] and South Water's ribbon spans N 1.8 to N 12.3. **The one joint the ledger chose
   to admit to was the one joint in the town that never showed** â€” while the five on South Water's
   own bends, named in the same breath and not measured, were 4.29, 4.25, 3.58, 1.77 and 1.77.
   L178 is revised in place with the correction rather than rewritten.

### The two costs, and why the mitre is capped rather than run out

**22 triangles**, town-wide, and the whole breakdown is: **23 of the 30 authored bends are mitred at
ZERO cost** â€” a mitre moves vertices, it does not add any â€” and 7 are too sharp for one mitre and pay
3 triangles each except the fort road's 39.3-degree turn, which pays 4. south_water [120, -57],
[180, -5], [220, 6]; north_water [827, 116], [920, 190]; fort_road [1115, 55], [1140, 78]. Read back
off the shipped scene rather than argued: 22,596 street triangles before, 22,618 after. No straight
street pays anything, so this is +22 at the worst stand in the town and +22 at the best.

**Against the ceilings, stated because they are already breached on `dev`** by other work (`full`
1,412,120 of 1,400,000 and `balanced` 1,252,802 of 1,210,000 at Lake Street at Canal, owned
elsewhere): 22 triangles is 0.0018 % of the `balanced` ceiling and 0.05 % of the 42,802 that
breach already stands at. It does not cause the breach and it does not materially deepen it.

**A mitred corner stands `half * (sec(turn/2) - 1)` past its bend by construction** â€” 0.17 m at the
fort road's 39.3-degree turn â€” and `drawn_placement_census.mjs` holds every drawn road vertex within
**0.05 m** of its own street's half-width. That census is what catches a mirrored ribbon, so it was
not touched; the geometry was designed to respect it. The cap is spent by CUTTING the turn rather than
truncating the corner: a joint too sharp for one mitre is closed by `k` sub-mitres whose outer corners
are the intersections of `k + 1` lines each tangent to the half-width circle. That polygon still
contains every point the round buffer does â€” a truncated corner would not â€” and the worst corner in
town now stands **0.029 m** out. Recorded as **L194**.

**And the concave side is never cut.** There the two offset strips already overlap and the nominal
ribbon reaches the full mitre point, so subdividing that side would pull the ribbon inside its own
recorded width and open a gap on the inside of the turn to close one on the outside. The asymmetry is
forced by the geometry, not chosen.

### Found and filed rather than fixed: T-0226 â€” and CLOSED 2026-08-28

Three of North Water Street's six bends carried no joint question at all, because its committed
centreline ran **inside the water mask** and no ribbon may be drawn there â€” the first reading of this
instrument reported them as 33.8 m2 of uncovered ground apiece and it was the tool that was wrong, not
the town. The nominal ribbon is now defined as ground the module is ALLOWED to paint, and those bends
are counted separately so they cannot hide.

**T-0226 settled it, and the street was the record that was wrong.** 477.4 m of its 843.3 m stood in
the river. The bank is a Wright 1834 trace with a stated Â±20 m; the street line was a hand-drawn
schematic that said so in its own note, graded `reconstructed`, standing on no control, and missing
the bank by up to 86 m â€” 4.3Ã— that uncertainty. The North Division placement recipe had already ruled
in writing that *"proximity to North Water Street never overrides the authoritative water mask"*, and
not one building in the town was placed against the old line. So the bank was left alone and the
street was re-derived FROM it by `tools/derive_north_water.py`, gated in `check.sh`: the platted
corridor's south line on the bank, the centreline 12.192 m north of it. Six bends,
`[240, 136.5] [560, 106.2] [780, 110.2] [830, 108.5] [920, 190] [970, 270]`, 807.3 m of centreline
with none of it wet, and the probe reads **0 bends refused for water** where it read 3. The full
reasoning is `docs/RESEARCH/north_water_street_and_the_bank.md`. The bend list above is the reading
taken before that, and north_water's sharp bend is now 44.1 degrees at `[830, 108.5]`.

Two consequences, both carried in the same change. The four `north_bank_shed_dearborn_*` records
derive their coordinate from this street's north edge, and left where they were they would have had
the corrected roadway drawn through them â€” 0.12 to 2.73 m from the new centreline against a 3.0 m
half-width â€” so they were re-derived by their own unchanged rule and stand 2.00 m back from the
track's north edge again. And the street's west terminus is now the east shoulder of the attested
north-side slough rather than a point 85.8 m out in the river: a ribbon may not paint a watercourse
and this town's other two slough crossings are modelled structures, so **T-0254** carries the reach
west of it.

### The picture

`docs/evidence/t-0184-before.png` and `-after.png`, one stand and one camera, on South Water
Street's west approach 15 m short of the [120, -57] bend, lifted 12 m and pitched 35 degrees down
so the ribbon's own edge is in frame. Before: a triangle of prairie cut into the road's left edge at
the turn. After: the roadway runs whole through it. Nothing else in either frame differs.

### Gates, and the one that was NOT run

**Run, on the published mirror:** `tools/check.sh` CHECK PASS Â· `measure_drawn_placement.mjs --gate
--refute` 0 strays of 28,265 drawn vertices, worst 0.00 m, negative control fires Â·
`measure_road_joints.mjs --gate` 0.000 m2 with its square-joint control at 23.472 m2.

**The full Playwright smoke was NOT run to completion, and CI is the authority for it.** The runner
was at load 48 with 105 concurrent Chromium processes from ten parallel agents; three agents had
already reported browsers killed mid-run and timeouts on unmodified `origin/dev` controls, so a local
smoke result would have been worthless in both directions. What was obtained before the run was
stopped is reported as a partial: mobile 390x780, stage 5, published mirror â€” **all five street-layer
checks passed**, including the new one, and the run's only failure is the "suite body ran to
completion" line caused by killing it.

The smoke gains nine stations inside the sector at every authored bend, at three angles and three
radii, which is the part of the lattice a release can afford. **It was verified RED on the pre-fix
build before it was believed** â€” mobile stage 5, naming South Water [120, -57] at all three radii â€”
which is the reading that says it is an assertion rather than decoration.
## Shipped â€” T-0187: the phone's sward stops thinning five metres ahead of the walker, and the obvious fix is priced and refused

**T-0187, the residue T-0093 banked rather than closed.** The near/mid run converted two boundaries
from coverage ramps to density handovers and wrote down what it had not touched: *"the mid and forb
rings' own OUTER coverage ramps are still screen-door ramps, and at `light` detail they reach in as
far as 5.4 m and 7.4 m â€” inside the verge on a phone."* This is that run, and it does not close it
the way that sentence expects.

**What a visitor sees.** Stand in open prairie on a phone. The ground from about five metres out to
the middle distance was drawn through a regular mesh of holes â€” every clump in that band carved by
an ordered 4Ã—4 screen door, at its most legible around eight to ten metres where the ramp is near
half coverage. It is written solid now, and the sward no longer opens up ahead of the walker: the
band the ramp used to thin is full ground cover. Flowers at the ring's edge last a little longer
with it, out to 11.8 m where they stopped at 10.0 m.

**The cause is one number that was never carried down.** `LOW` and `MID` in `renderers/web/js/
flora.js` cut the ring radii â€” 27 m to 13 m â€” and scaled the fringe with them, *"about an eighth of
the radius at every setting"*, its own comment. They left `band`, the width the outer edge fades
over, at the full-detail 7.0 m and 5.0 m. A ramp sized for 18â€“27 m therefore sat on a 13 m ring and
came out across the middle of the phone's field. `balanced` had it too, unnoticed: its mid ramp
began at **8.2 m**, also inside the verge. Nothing about the phone was special.

**THE OBVIOUS FIX WAS PRICED AND REFUSED, and the number is the whole of the reason.** Handing these
edges over by density â€” `spreadOuter`, T-0093's own answer, and what the ticket points at â€” was
simulated slot by slot on the published mirror, against every mid instance's own `aChiRing` and the
gate's own sixteen bearing bins, before a parameter was touched:

| detail | mean drawn reach now | with the band handed over by density | the bar |
|---|---|---|---|
| `full`, desktop | 26.81 m | 25.42 m | 24.90 m â€” survives |
| `light`, mobile | 11.89 m | 9.64 m | **11.60 m â€” red** |

Even a **one-metre** spread lands at 11.48 m at `light`. The loss is not a tuning artefact: the
drawn edge of a stochastic thinning is the depth at which the thinning still leaves a plant standing
in a given bearing, and the mid lattice deals about one slot per metre per bin at 12 m against two
and a third at 26 m. No representation that draws a plant whole or not at all can reach as far as
one that draws every plant faintly.

**And the bar it fails is resting on plants nobody can see.** The smoke reads the boundary off *"the
furthest plant in this bearing that is actually DRAWN"*, and drawn means `fadeAt > 0.02` â€” two per
cent coverage, one pixel in fifty through the Bayer matrix. On a coverage ramp that admits every
placed slot, so the statistic reports where the placer stopped placing, which the placement guard
already guarantees, rather than where the field ends. **The bars were left exactly where they
stood** and the instrument's defect is filed as T-0209 rather than fixed in passing here.

**So the ramp is cut to the ring instead.** The rule, written where the numbers live: an outer band
may not BEGIN inside the verge â€” `radius âˆ’ step âˆ’ fringe âˆ’ 9.0`, the nine metres
`tools/measure_near_verge.mjs` calls the ground a walker looks at. `light` takes **1.6 m** on both
rings (the clearance binds at 1.8; it lands equal to the fringe, so the sward's edge thins over no
more ground than it is ragged by). `balanced` takes the proportionate **4.7 m** and **3.4 m**, which
already clear it. `full` is unchanged at 7.0 m and 5.0 m, clearing by 16.4 m and 17.4 m.

**What it costs.** Nothing in the lattice: the ramp never paid for geometry â€” the placement guard
and the lattice do â€” so the grass slots, the species deal and the drawn census are identical plant
for plant. Two things do move. Fill, because the ground the ramp used to thin is now written solid
and the fragment shader's discard sits before the lighting rather than after it. And the flower
heads, because `headRingOf` hangs the head ring off the band: at `light` the forb heads run to
11.8 m where they stopped at 10.0 m, which is more head instances against the same 240 cap.

**Verification, and the reach it was refused for went UP.** `tools/check.sh` CHECK PASS.
`tools/smoke_renderer.mjs --published` part 7 at 390Ã—780: **45 passed, 0 failed**, both boundary
checks green at their existing bars, and the figures printed on the passing line as well as the
failing one (a `show` flag on `check`, added because a change to the boundary has to be able to
quote what it was before):

| | before | after | bar |
|---|---|---|---|
| min drawn reach | 10.32 m | 10.32 m | â‰¥ 9.60 |
| mean drawn reach | 11.89 m | **11.96 m** | â‰¥ 11.60 |
| max drawn reach | 12.76 m | **13.22 m** | â€” |
| boundary rows spread | 17.4 px | **19.8 px** | â‰¥ 4 |

The gain is arithmetic rather than luck: the smoke culls a plant below `fadeAt <= 0.02`, which on a
7 m band is 0.14 m of reach and on a 1.6 m band is 0.03 m. Narrowing the ramp hands most of that
back â€” which is the mirror image of why the density handover could not: it does not draw the
outermost plants at all. `full` detail is untouched by this change (only `LOW` and `MID` moved), so
the desktop boundary readings cannot shift.

**What this run did NOT do.** The outer edges are still coverage ramps and still dither, in the last
1.6 m of the phone's ring and the last 7 m of the desktop's â€” outside the verge at every setting,
which is the claim the fragment shader's own comment makes and could not make before. Making them
density handovers waits on T-0209.

## Shipped â€” T-0031: the South Water timber belt is derived from the street, not authored beside it

**The owner's ruling, and route 1 was buildable.** R-BUG5 measured `FAR_TIMBER.main_stem_belt_east`
standing in the main stem â€” **39 of 39 samples over water, 3.347 m under the surface** â€” and the
renderer has refused to draw it since 2026-08-16. The residual, R-BUG5(b), was not a pick without
the owner because where the belt's near edge ran is a placement claim Andreas does not settle. He
ruled on 2026-08-17: derive it from the committed `south_water` centreline, assert the side of the
street, record the assertion as a liberty, re-bank the gates.

**What shipped.** `tools/derive_timber_belt.py` builds the path out of `data/streets/1835.json` â€”
the committed `south_water` centreline, mitred-offset **12.192 m** (half the platted 24.384 m
corridor) to the SOUTH, clipped east at the **mean easting of the committed `wells` centreline,
E +329.3**, which is byte for byte the number `timberEastLimits()` already hands the near-field
planter for the same limit. The path stays a literal in `trees.js`, because
`tools/measure_far_timber.py` reads the renderer's own table and must keep being able to, and
`tools/check.sh` re-derives it on every commit. **Move South Water Street and the gate fails until
the belt moves with it.**

| | the stub | the derived belt |
|---|---|---|
| samples over water | **39 of 39** | **0 of 136** |
| worst depth | 3.347 m | â€” |
| length | 73.4 m | 265.0 m |
| east end | E +396 â€” **66.7 m east of Wells** | E +329.4, on the committed `wells` easting |
| distance to the water's edge | in the channel | 24â€“49 m |

**The stub was east of the street it was named for**, because it was authored against the old 640 m
box with Wells guessed at E +400. That is the same class of error K45(b2) found in
`z05_riverbank_timber`'s note (440 m out) and it is half of why the line ended up in the channel:
the other half is that it was offset north instead of south.

**The placement was checked against something it was not fitted to.** Every 2 m sample of the
derived line stands **24â€“49 m from the water's edge**, inside the 30â€“74 m gallery `communityAt()`
deals from the same bank distance â€” so the far body stands on ground the near planter's own
classifier independently calls ZONE 5 gallery. The browser census agrees with the Python one body
for body and sample for sample.

**What a visitor sees, measured through `horizonCensus()`.** The band drew nothing for eleven days.
It now wins **19 bearings from the Green Tree anchor** (73â€“80Â°, crowns to 36.6 px at 1280Ã—800),
**36 from Randolph and Canal** (47â€“61Â°, 37.3 px â€” the stand R-BUG5 reproduced the owner's
screenshot from) and **15 from the forks** (84â€“89Â°, 46.9 px). From the `south_water` anchor itself
it draws nothing, which is correct: standing on the belt puts it inside `MIN_FAR_M`. Frames:
`docs/evidence/t-0031-{before,after}.png`, crop `t-0031-green-tree-crop.png` â€” the pair differs by a
small eye-height settle between the two runs, so read the crop rather than differencing the frames.

**One thing the ticket did not ask.** Since K45(b2) the near planter sweeps the whole field and
ends the South Division timber at the same Wells Street, so **70 stems already stand in this
reach**. The far body is not a duplicate of them â€” it is the relationship `north_division_timber`
has had with the ZONE 6 wood since the sweep widened: stems near, silhouette far, one east limit
read from one street record. But the belt was never wholly absent from the scene, only from the
skyline, and that is worth knowing before anyone quotes "the belt draws nothing".

**The one assertion is `docs/LIBERTIES.md` L182** â€” which side of the street. South, on the
dossier's own reading (relict trees *"8â€“25 /ha in the north/riverside blocks (South Waterâ€“Lake,
west of Wells)"*) and on a measurement: the strip between the street centreline and the water is
**11.5 m at its narrowest and 36.0 m at Wells**, and on this date it is the working waterfront.

**Gates.** `tools/check.sh` green, including the census, its five-case self-test, the three ratchet
directions and the new re-derivation step. **The Playwright smoke was NOT run**: the shared runner
was at load 48 with 105 concurrent Chromium processes and browsers were being killed mid-run, so a
local result would have been worthless in both directions. CI is the authority. The browser figures
quoted above were taken before that instruction, on the same loaded box, and are reported with that
caveat â€” they are counts out of the scene graph rather than timings, which is why they are quoted
at all.
## Shipped 2026-08-24 â€” T-0027: the public square has no wet fraction to read, and the sward was the thing that was wrong

**The ticket asked how much of the public square was wet, and the answer is that the question has no
fraction in it.** `tools/measure_public_square.py` (new, and a `check.sh` gate) samples the committed
platted block `blk_randolph_lasalle` at 0.5 m â€” 43,885 samples over 10,976 mÂ² â€” against the committed
heightfield:

| | |
|---|---|
| ground | **+2.84 to +2.96 ft** above the summer-1835 water surface (mean +2.90) |
| relief across the whole block | **1.49 in** |
| **wet fraction** | **0.0 %** â€” 0 of 43,885 samples at or below the water |
| the dossier's bed for zone 15 | +1.0 to +2.0 ft, which the ground stands **0.84 to 1.96 ft above** |
| the square's drain, `state_slough_course` | heads **34.4 m** off the block's east kerb, outside it |

### The zero is a reading of the model, and the relief row is what says so

An inch and a half across a city block is *inside* the terrain spec's own declared micro-relief â€”
two octaves of value noise at Â±0.10 ft, seed 18350701, which `micro_relief.note` calls **"a texture,
not a claim"**. The square carries no landform at all; it is the South Division's plain profile plus
noise, which is exactly what `not_modelled_in_this_box` says dossier zone 15 is. **A wet fraction
read off this ground would be a read of the noise seed.** That is why the gate asserts the relief
beside the water: assertion 1 is a statement about the model only while assertion 2 holds.

### So the honest answer is a depth, and it is a question nobody had asked

The dossier's row 15 puts the pond's bed at +1.0 to +2.0 ft; the committed ground stands 0.84 to
1.96 ft above it. **The pond cannot be laid on this block â€” it has to be dug**, one to two feet deep
over 10,976 mÂ², out of the one land elevation in this box that rests on a documentary sentence, under
the block carrying Chicago's first public building, with no source stating a depth. T-E5(a) had the
date and the extent as one question; they sit inside a third, and `geometry conjectural` was carrying
it. Zone 15 stays deferred and `not_established`. **No confidence moved and no ground moved.**

### What was actually wrong, and it needed no bake

The **sward**. `docs/research/02-flora.md` heads its ZONE 3 *"SLOUGH & SEDGE MEADOW (**Public
Square** â†’ Tremont House site â†’ river at State St)"* and Â§ 1.2 calls that slough the single most
important vegetation feature INSIDE the platted grid. `z03_sedge_meadow`'s extent is an **elevation
band** of +0.6 to +2.2 ft â€” which can never reach a block the terrain draws at +2.9 ft, *because zone
15 is deferred*. So the one block three sources describe as water was planted by the same rule as
anonymous prairie 800 m west, and the pond quotation reached the flora layer nowhere. It is the
mirror of what T-E5(a) found in the fauna, where `z04_marsh` "has never reached the square" either.

**Shipped:** `include_polygons` on the flora extent matcher â€” the exact mirror of `exclude_polygons`,
for a community whose evidence is a PLACE and whose rule is a HEIGHT â€” in
`renderers/web/js/flora.js`, mirrored in `tools/validate.py`'s evaluator and registered in
`tools/measure_layer_reads.py`; the square's ring on `z03_sedge_meadow`, taken **vertex for vertex
from the committed plat** and held there by the gate, so nothing is fitted and in particular nothing
is shaped around the estray pen, the log jail and the court-house, which stand ON the sward;
`docs/LIBERTIES.md` **L188** for the one invention, that the wet ground stopped at the surveyor's
line; the correction of `data/reconstruction/1835_reserved_ground.json`'s now-false *"the square
renders as dry prairie"*; `docs/RESEARCH/public_square_pond.md` Â§ 6; ROADMAP T-E5(b) closed.

**Unverified / stated rather than measured:** the sward's *appearance* on the block is asserted from
the zone record and the smoke's zero-pageerror pass, not from a shipped screenshot diff â€” no critic
baseline stands on the public square, which is itself worth a ticket.
## Refuted 2026-08-24 â€” T-0026: there is no southern buildable ground, and the schedule was naming the wrong blocker

**T-E4 was opened on "south is where the room is" and told the next run to widen the eligible ground
southward.** Measured against the committed heightfield, there is nothing there to widen onto. The
modelled box ends at **local N -400 m**, and that line falls **inside Washington Street's own 80 ft
platted corridor** â€” so the town's southernmost committed street is the last thing on the field.

| | measured by `tools/measure_southern_ground.py` |
|---|---|
| land above the water surface south of Washington's platted corridor | **0.0819 ha** (131 cells of 135) |
| ...of it in the South Division | **0.0000 ha** â€” every cell lies west of local E -10, on the West Division bank across the South Branch |
| Washington's own corridor lying off the field | **0.33 ha**, over **899 m** of its length, up to **7.29 m** deep |
| Madison Street below the field's south edge | **125.2 m** at State, **119.2 m** at Market |
| the plat's last tier â€” Washington to Madison, Market to State | **6 blocks, 48 lots, 6.28 ha, 0 of 24 boundary points on modelled ground** |

**The finding that matters is not the acreage, it is what the programme was telling the next run to
do.** `south_plat_beyond_committed_control` holds **120 roofs**, the largest of the three gated
balances, and it said they were waiting on **street control**: *"no block east of State or south of
Washington has four committed centrelines (ROADMAP S9)"*. That is true and it is downstream. Every
north-south column of the south plat â€” Market, Franklin, Wells, LaSalle, Clark, Dearborn, State â€”
has its committed centreline cut at **exactly N -400**, the field's own south edge, not at a street.
Street control stops where the ground does, and the modern control that would carry it further is
already committed: `G1`, the PLSS corner at State & Madison, is an OpenStreetMap node with an id and
a 13.9 m residual. A run that had believed the stated blocker would have carried the lines south,
emitted six blocks, and watched `tools/generate_block_infill.py` refuse every placement on them for
*standing outside the modelled terrain*. **Ground east of State was never available either â€” T-E2
settled that it is the United States Reservation.**

**What the terrain parcel actually needs, measured so it is not re-argued.** The box's south cap is
evidence-bound rather than a cost decision, and the evidence is about **one river**: the spec says a
box reaching further south *"would show open prairie where the river actually continues"*, and the
river in question is the South Branch, whose traced water ends at **N -405.2**. Everything else is
already in hand â€” the harbour-reach shoreline reaches **N -589.2** and the sand bar **N -436**, both
south of Madison. So the extension needs the South Branch's two banks carried from N -405 to about
**N -531, 126 m per bank**, off a sheet this project holds, and then a bake. The tier itself is dry:
at N -400 the branch occupies local E -8 to +35 and the tier runs E +88 to +826. Filed as **T-0219**.

**What shipped, and what did not.** `tools/measure_southern_ground.py` is new â€” the report, two
assertions and a self-test, wired into `tools/check.sh`. The first assertion is absolute and is the
one worth having: **no committed platted block stands off the modelled ground** (19 of 19 today), so
the day a centreline is carried south without the terrain following, the failure arrives at the
commit naming the block instead of inside a parcel run as a cryptic per-placement refusal. The
second holds the programme's stated southern coverage to the measured one. `tools/reconcile_665.py`
now **composes** the South balance's `waiting_on` from that measurement rather than authoring it,
and carries the figures in `coverage.southern_ground`. `tools/compile_scene.py` puts the measured
southern edge on the ground card. **No structure record moved, no roof was added or removed, the 665
total is unchanged, and nothing was baked.**
## Shipped 2026-08-27 â€” T-0199 / T-0220: the owner changed the density standard, and South Water's walk closed up

**THE STANDARD MOVED. This is not a bug being fixed, and it must not read as one later.** Until
2026-08-27 this project held one principal roof to a platted lot. It no longer does on the town's
business front: **a platted business-front lot may carry a documented store at the street AND an
anonymous dwelling behind it.** Kevin ruled it, in those terms, on 2026-08-27.

**How the question arose, which is why it was his to answer.** T-0127 sent eleven documented South
Water buildings back onto the committed plat â€” their setback had come from `osm_streets_2026`, a
2026 kerb line, and stood them up to 8.17 m out in the platted roadway, which is why T-0069's
plank walk came out of that street in stumps. T-0198 (PR #373) moved six. It refused the other
five **in writing, per store**, because on the plat each of them SEATS on a lot the 665-roof
schedule had already dealt to that street's anonymous frontage run. Nothing overlapped â€” all
eleven were checked against every committed footprint in the town and the worst overlap is
**zero**. What refused the repair was the RULE, and the finding under the finding was worse than
the repair: **the block programme had dealt those roofs onto lots documented buildings actually
stand on, and passed its own occupancy gate only because those buildings were drawn out in the
road.**

**The fork, as put to him, and his answer.** (a) The lot rule holds and the town gives the roofs
back: **eight roofs leave** (338 â†’ 330), four block recipes are re-authored, two households are
re-homed or leave with their roof. (b) The business-front lot carries both. **He chose (b)**, on
the reasoning the ticket recommended â€” the geometry already permits it, and (a) pays eight roofs
and two households for a rule the corrected data has itself called into question. It is the same
argument T-0143 and T-0188 are about, the core density standard T-0079 raised, and settling it by
side effect inside a sidewalk ticket would have been the wrong way to decide it.

**Where the ruling is recorded**, because a standard that lives in one commit message is a
standard nobody can find: `tools/plat_occupancy.py`'s module docstring (the ruling, the fork and
the clause's three tests), `docs/ROADMAP.md` K30(d), the four affected blocks' own
`arrangement_note`s in `data/reconstruction/1835_platted_block_parcels.json`, and tickets T-0199
and T-0220.

**What the clause admits, and what it still refuses.** `plat_occupancy` now answers two questions
with two maps instead of conflating them: `occupied_lots` â€” *what stands on this lot* â€” unchanged
and still truthful, because a documented store on a shared front still stands there and its roof
still counts against its block's headroom; and `exclusive_lots` â€” *what BARS another roof* â€”
which is the first less this clause. `generate_block_infill.py` and `reconcile_665.py` both read
the second, so the generator and the schedule cannot drift apart on it (T-A6, T-A7). Three tests,
all of which must hold: **the lot is named in its block's own `frontage` run** in the committed
parcel recipes (an interior lot, a side lot and any block with no frontage run are untouched);
**the standing building is researched**, not one this project's reconstruction programmes wrote
(two anonymous roofs on one lot is still one too many); and **it stands AT the street**, its
street wall no further back from the committed frontage line than the run's own units plus one
lot margin, both read from the block's own recipe. A fourth falls out of the third: the store has
to be the lot's only occupant, which is what keeps the schedule from offering a block room it is
already building on â€” and it is also why one function serves both halves, since the generator
asks it with its own records excluded and the schedule asks it with nothing excluded.

**Nothing physical was relaxed, and NO second rule was needed.** No overlap, the 1.5 m lot
margin, the platted corridor and the three-metre separation between roofs all still bind,
untouched. One pair did fail the separation gate on the way â€” the run's westernmost unit at
**2.40 m** from `carpenter_south_water_store`, side by side along the face with their fronts
level â€” and the honest fix was in the recipe rather than in the gate. That break is AUTHORED:
`blk_south_water_wells`'s westernmost frontage slot stands `clear_west_of` the store by a
stated `clear_m`, and
`place_frontage`'s own note says where the number comes from â€” *"the three-metre separation
rule â€” not this recipe â€” is what fixes the size of the break"*. **2.40 m was authored while the
store stood 6.62 m out in the roadway**, when the along-face break was not the real gap at all;
on the plat their fronts are level and it is. So the authored break moved to the gate: 2.4 â†’
3.0 m, one anonymous roof 0.6 m further west, `clear_why` written beside it. **No threshold was
lowered anywhere in this work.**

**Which of the eleven still needed moving, re-measured rather than inherited.** The figures the
parked branch carried were taken before #373 merged and were stale by six records. After #373:
three of the eleven (`jh_kinzie_forwarding_store`, `temple_building`, `chicago_democrat_office`)
were on the plat and clear of every corridor; three more (`harmon_loomis_store`,
`madore_beaubien_house`, `peck_store`) were on the plat with a 0.16â€“0.21 m residual on a CROSS
street, which is T-0195 and which this ruling does not touch; and **five still stood in the
roadway â€” exactly the five #373 refused.** They moved 9.67 (`h_jones_store`), 8.41
(`chicago_american_office`), 8.12 (`carpenter_south_water_store`), 7.75
(`frederick_thomas_shop`) and 7.05 m (`pruyne_kimball_drugstore`) along their block face's inward
normal, each leaving its street wall 1.50 m back from the committed frontage line. **That is
#373's method, not the parked branch's** â€” the branch had put the wall ON the lot line, and one
rule across the eleven is worth more than the 1.5 m. `local_e` moves only by the face's own skew,
0.07â€“0.24 m; the along-street position the sources argue is untouched, and no confidence grade
moved.

**What a visitor sees**, measured against `dev` after #373:

| | before | after |
|---|---|---|
| town street edge | 1,214.5 m of walk in **20** runs | **1,297.3 m** in **18** |
| corner crossings | 9 (212.5 m) | **11** (266.5 m) |
| walking decks | 89 | **96** |
| `blk_south_water_wells` north face | 20.6 m + 41.1 m | **one 97.6 m run** |
| `blk_south_water_dearborn` north face | 15.6 m + 20.8 m | **one 67.6 m run** |
| phases lapping a platted corridor | 26 | **21** |
| standing roofs | 338 | **338** |

**The march refuses ZERO steps for a wall anywhere on South Water Street**, read off `_march`
itself step by step rather than inferred from the run lengths. Every remaining South Water
refusal is that street's own ground â€” 0.07â€“0.13 m of roll under one walking deck, one step at
+0.02 m at or under the water. The **eleven** wall-refused steps left in the town are all on Lake
Street: `old_bank_building` 4, `dole_warehouse_south` 3, `first_presbyterian_church` 2,
`st_marys_church` 2. That is **T-0196**, and the ruling deliberately does not reach it â€” measured,
not assumed: neither `blk_lake_lasalle` nor `blk_lake_dearborn` has a frontage run in the parcel
recipes for the clause to sit on, and all four would land on lots that already carry anonymous
roofs.

**The smoke ran all nine stages at both viewports** â€” mobile **449 checks, 1 failed**;
desktop **454 checks, 2 failed**; and mobile was re-run whole after the second dev merge,
**450 checks, 1 failed**. Every failure is one assertion at one stand.

**ONE GATE IS RED AND IT IS NOT WAVED THROUGH.** `scene detail 'balanced' stays inside its own
ceiling at the WORST stand` fails at Lake Street at Canal, the long axial view. Measured as an
A/B â€” the same tree read twice, once with `dev`'s `town_street_edge.json` in the published mirror
and once with this one â€” the frontage layer costs **5,350 triangles** at that stand, to the
triangle, at every tier and both viewports:

| tier Â· viewport | ceiling | dev | here |
|---|---:|---:|---:|
| `balanced` Â· mobile | 1,210,000 | 1,208,033 â€” **1,967 to spare (0.16 %)** | **1,213,383** over |
| `balanced` Â· desktop | 1,210,000 | 1,253,630 â€” **already over by 43,630** | 1,258,980 |
| `full` Â· desktop | 1,400,000 | 1,413,266 â€” **already over by 13,266** | 1,418,616 |
| `full` Â· mobile | 1,400,000 | 1,366,289 | 1,371,639 (28,361 to spare) |
| `light` Â· mobile / desktop | 1,050,000 | passes | 807,943 / 859,229 |

Desktop's two failures are `dev`'s and predate this branch entirely. Mobile's is this branch's,
and it was 3,383 triangles over a ceiling `dev` was 1,967 triangles from failing â€” **762
triangles over, 0.06 %, once dev's #384/#387/#394 were merged in and gave most of it back**. **A tier with
0.16 % of headroom is not a budget, it is a coincidence** â€” T-0135 set these on 2026-08-22 with
*"about 6 % of headroom over the measured worst"* and five days of content ate it. **No ceiling
was moved here**, deliberately: raising a number to make a red go away inside a ticket about a
sidewalk is the exact defect T-0135 was opened to end, and its own text says the choice between a
conscious re-budget and the trim T-0149/T-0146 are open for is the owner's â€” *"This is the
measure. The move is his."* What HAS changed since he last looked is that `light`, the objection
he was given last time, now sits 18â€“23 % UNDER its ceiling rather than 65 % over. Filed with every
figure as **T-0218**.

**One measurement made on the way, worth its own ticket.** `measure_street_frontage.layer_of`
names the three evidence layers by ID PREFIX, and across the committed 348 records it disagrees
with the record's own contents exactly once: `physicians_office` carries no `inf_` prefix and is
nonetheless a product of the inferred-household programme, which its own
`reconstruction.status` says. The new clause reads the record rather than the filename for
precisely that reason â€” a rule about documented buildings must not let an invented one through on
the strength of its name. Filed as **T-0221**.
## Shipped â€” T-0215: the What's-new stage was not failing on What's-new, and nothing was broken

**Three agents in one day read the same log as a broken panel.** `SMOKE_VIEWPORT=desktop
SMOKE_STAGE=8` died on a single `page.click` timeout; one branch re-ran it in a clean `origin/dev`
worktree at `29eebdef` to prove it was not its own change, and it was not. **Read the summary line
and the diagnosis is already half done: `0 staged-section check(s)`.** The eight passes were the
boot, page-error and vendor checks every invocation takes. Part 8 was dying on the **Settings tab,
its first action**, before one of its 28 assertions had run â€” including all the ones that have
nothing to do with What's-new. The part is *named* for its last section, and three readers took
the name for the subject.

**The panel was driven by hand while the gate was dying, on the same tree and the same machine.**
Gate dismissed, panel open, `elementFromPoint` at the tab's own centre returning the tab itself, no
pointer lock, and the feed painting **272 entries and 1,569 items**, newest *"Two evidence cards
were showing their own merge scars"*, its meta line `Fixed Â· Aug 26, 2026, 11:18 PM CT`, the unread
chip cleared and `chicago4d.whatsnew.seen` at 272. Every assertion the stage makes about that panel
would have passed.

**What had actually moved was the cost of a frame.** Ten consecutive frames on the loaded runner:
**17,036 Â· 29 Â· 333 Â· 21,451 Â· 20,211 Â· 119 Â· 4,420 Â· 22,280 Â· 12,242 Â· 26,580 ms**, against the
**0.46-1.10 s** measured on 2026-08-13 that the 90-second action budget was written around. The
29 ms and 119 ms frames in that same sample are what settles it: the renderer draws this town fast
when it is given the CPU, and for tens of seconds at a stretch it was not. Load average was
**38.7-51.7 with 71-115 concurrent Chromium processes** (a dozen agents on one box); two runs ended
`Target page, context or browser has been closed`, `pgrep -c chrome` went 115 â†’ 0 in one interval,
and a `page.goto` against a **local static file server** timed out at 30 s.

**It is flaky, not broken, and the tidy explanation is refuted.** The identical click landed in
**10.9 s** cold from a fresh boot through part 8's own prologue, **28.4 s** on a settled page,
**20.6 s** for the What's-new tab and **53.8 s** for `#gate-btn` after a reload â€” and then blew
90 s in the gate. The obvious mechanism (a filtered run clicks during the expensive first frames
where an unfiltered run has seven parts of walking in between) predicts the COLD click is the slow
one; it was the fastest of the five. There is no trigger, only a distribution with a tail across
the budget.

**No commit is guilty, and that is shown rather than asserted.** T-0167 measured desktop part 8
green at 6 m 10 s twice on 2026-08-24. Since then nothing the panel is made of has changed â€”
`renderers/web/index.html`, `js/hud.js`, `js/whatsnew.js` and `css/walk.css` were last touched at
`d7e09dcb` (T-0076), well before that reading. What has changed under `renderers/web/` since
2026-08-23 is `flora.js`, `frontage.js`, `trees.js`, `streets.js`, `main.js` and `changelog.js`:
six contributions to the cost of a frame and not one panel.

**The budget is NOT raised a second time.** This file predicted the recurrence in as many words on
2026-08-13 â€” *"a standing hazard, not a fixed one: the same starvation will return as the town
grows, and the next symptom will again look like a UI bug rather than a budget"* â€” and 90 â†’ 180
would buy one town-sized month and spend it against a ten-minute per-command ceiling this gate has
already been re-cut for twice. **`clickChrome()`** replaces part 8's fourteen panel-chrome clicks:
in ONE page round trip it asserts everything `page.click` asserts across many frame-bound ones â€”
the element exists, is enabled, has a real box, and is **the topmost thing at its own centre** â€”
then clicks it. Nothing is skipped. The `elementFromPoint` test IS T-0108's assertion: a control
the HUD's `pointer-events: none` swallows returns the canvas and fails here exactly as it fails a
visitor's mouse, now in one round trip naming what covered it instead of in ninety seconds with a
call log that reads like a broken control. The four clicks where the trusted event is the *subject*
rather than the means â€” part 4's confidence menu â€” stay `page.click` and now say why.

**And the smoke now prints what a frame costs whenever an action times out**, so the next reader
gets in the same log the answer this cost three agents a day to establish. It is a report and never
a bar: the failure still fails.

**The helper's own first run got one thing wrong, and it is the lesson worth keeping.** It took
part 8 from 0 staged checks to 19 of 28 and then failed two â€” *"G opens the Go to tab"* reading
`{"open":false,"tab":"goto"}` and the row after it reading `has no box (0x0)`. One fault:
**a real mouse press focuses a focusable control and an untrusted `.click()` does not.** Part 8
closes the panel and then presses `g`, and `g` only reaches the window shortcut once focus has
left the Go-to search box, because `isTyping(e.target)` swallows it otherwise â€” which is precisely
what that guard exists for. So the panel stayed shut and the row beneath it had no box.
`clickChrome` focuses before it clicks now. That is the exact hazard in swapping a trusted event
for an untrusted one, and anyone extending this past part 8 should look for it first. Note also
which instrument found it: one line naming the fault, where the old path spent ninety seconds and
printed a call log about a button it had itself found visible, enabled and stable.

**The controlled A/B, which settles it.** The box drained around 06:00 CT â€” every agent's browser
was killed at once â€” and that bought the reading this needed: **`origin/dev`'s own unmodified
`smoke_renderer.mjs`, on this same tree, at a quiet load.**

| run | harness | load / Chromium | outcome | wall |
|---|---|---|---|---|
| desktop 8 | dev's, unmodified | 38.7 â†’ 51.7 / 71-115 | **1 failed Â· 0 staged checks** | 4 m 23 s |
| desktop 8 | dev's, unmodified | **10.4 â†’ 13.7 / 20-24** | **37 passed, 0 failed Â· 28 staged Â· PASS** | **14 m 33 s** |
| desktop 8 | after | 15.8 â†’ 21.2 / 21-35 | **37 passed, 0 failed Â· 28 staged Â· PASS** | **6 m 10 s** |
| mobile 8 | after | 14.4 â†’ 12.0 / 20-27 | **37 passed, 0 failed Â· 28 staged Â· PASS** | 2 m 52 s |
| desktop 8 | after, on the **final merged tree** | 12.4 â†’ 13.5 / 30 | **37 passed, 0 failed Â· 28 staged Â· PASS** | 4 m 49 s |

**Row two is the verdict: the harness that failed three agents is green on a quieter machine, same
tree, same commit, every one of the 28 assertions reached and passed.** Stage 8 was never broken.

**Row two is also the argument for changing anything at all.** It passed in **14 m 33 s** â€” four
and a half minutes past the ten-minute per-command ceiling a steward run is killed at, so on this
box the old part 8 does not fit even when it does not flake. `clickChrome` runs the same 28 checks
at a comparable load in **6 m 10 s**, which is T-0167's 2026-08-24 figure to the second. It buys
back **8 m 23 s of margin** on the ceiling this gate has already been re-cut for twice, and it
does it by not paying for frames rather than by checking less. **Desktop-only, and the mechanism
is the obvious one**: at 390Ã—780 a frame covers a quarter the pixels and the same part costs
2 m 52 s against 6 m 10 s.

Every green row was taken as the box drained, so **none proves the fix survives load 50 and
nothing measurable here could**. They prove the assertions exist, pass, are reached, and now fit
the ceiling; the claim about load rests on row two and the frame timings.

**The same fault one part along is already filed by someone else** â€” **T-0210**, *"the desktop
smoke's stage 9 times out clicking the panel close, on an unmodified tree"*. `clickChrome` is the
ready-made answer for it, and part 9 is deliberately left alone here: it is that ticket's, and a
helper with exactly one part's worth of surprises behind it should be extended by someone who has
read the focus-fidelity paragraph above first.

**What is NOT fixed, and it is the part that matters.** `chicago-4d-check.yml` runs `check.sh` and
nothing else, and the full smoke is dispatch-only, so **dev has no standing smoke result of its
own**. "Is this red mine or dev's?" costs a fresh worktree and a re-run every single time, which is
exactly what three agents paid today. A nightly dispatch of `chicago-4d-smoke.yml` on `dev` would
make it a lookup â€” filed as T-0216, and left unbuilt here because it edits a workflow file, which
AGENTS.md Â§ How work ships puts outside a steward run's scope.

**And a second defect, found by merging this.** dev handed out `T-0211` to another branch while
this one was carrying it, which is exactly what `ticket.mjs restamp` exists for â€” and restamp
renumbered the right FILE while rewriting the WRONG QUEUE LINE, clobbering the other ticket's
entry and leaving a phantom line for an id that no longer existed. `indexOf`/`queueReplace` key on
the id, and with a duplicate id there are two lines carrying it. `ticket.mjs check` refused
neither state; it was caught by reading `tail QUEUE.md` and repaired by hand. **T-0217**, with the
one-line cause and the self-test that would prove a fix.

## Shipped 2026-08-27 â€” T-0022: the South Water row is log and frame, and the rule that made it frame-only was a preference

**The ticket asked whether the schedule may deal log cabins to the town's commercial frontage. It
may, and the interesting part is that nothing was stopping it.** L99 and L100 both recorded the
opposite worry in the same words â€” the 665-roof programme apportions families by DISTRICT and "has
no notion of what a street was for", so "it will keep dealing cabins to commercial frontage every
time this lane reaches one" â€” and ROADMAP K29 proposed the remedy that follows from believing it: a
schedule term weighting the meanest dwelling families off the business front. **Measured, the fault
runs the other way, and the schedule was never the fault.**

**The number.** Before this run, **15 invented buildings stood on South Water Street's line and not
one of them was log.** Thirteen of the fifteen were the party-line river row itself. The documented
record for the same line is 8 buildings, one of them log â€” Hogan's store. Every log dwelling the
schedule HAD dealt those five blocks, all five of them, stood on the Lake face, put there by a rule
the block recipes state in their own prose: *"the two best dwellings the schedule deals take its two
free lots â€¦ and the two meanest take Lake."* **Lake Street is the other principal thoroughfare**, so
the rule was moving cabins from one commercial frontage to another and reading as care.

**The evidence is three witnesses and none of them is taste.** The committed record already stands
log TRADE buildings on the principal-street line â€” `hogan_store` (a store, South Water),
`philo_carpenter_log_shop` (a drug shop, Lake), `madore_beaubien_house` (dwelling and store, South
Water), `mansion_house` (a tavern, Lake) â€” and one street back `james_kinzie_house` is a documented
log RESIDENCE on Lake. The only picture of this row, image 11 of the owner's brief of 2026-08-18
(*"South Water Street in 1834"*), draws it as *"roughly ten one-storey log and frame buildings
shoulder to shoulder facing the river, two two-storey frame stores anchoring the east end"* â€” and
that is the **same plate T-0078 already cites as the warrant for the party-line treatment itself.**
This project took the half of that sentence about shape and left the half about fabric. And the
owner's ruling of 2026-08-27 on PR #371's fork, option (b), settles the general point: a
business-front lot may carry a documented store at the street and an anonymous dwelling behind it,
so the business front is not a district a dwelling is kept out of.

**What shipped: ten records changed places, and that is the whole of it.** Five log dwellings came
off the Lake lots into the South Water run â€” one per block, at its west end â€” and the five frame
cottages they displaced took the Lake lots the cabins held, at the cabins' own setbacks and offsets.
**No roof was added or removed. No record changed id, family, footprint or any form value.** The
slots keep their positions in the recipe list precisely so the ids do not shift, because a record
renamed is a record re-dimensioned and that would have been a bake for a change that moves no
vertex; `validate.py` confirms it â€” 0 errors, no staleness. The run's line, length, anchors and unit
count are unchanged, the schedule re-derives untouched (338 standing, 327 remaining), and the
closest any moved record comes to anything that is not its own party wall is **3.14 m** â€” Wells's
cabin to Carpenter's South Water store, against a 3 m separation gate.

**K29's re-apportionment is refused rather than deferred.** A schedule term built to keep cabins off
the business front would have been a term built on a refuted premise. **Its other half survives and
is filed as T-0208**: weighting the trade families C, F and W ONTO the business front is not
refuted â€” the same census reads South Water's documented line at 80 % trade â€” but it is a genuine
schedule change, it is invisible until a block is built, and it does not belong in this run.

**Held by `tools/measure_frontage_fabric.py`**, wired into `check.sh` with its own self-test. One
assertion, absolute, no ratchet and no threshold: *a principal street's invented frontage may not be
more uniform in construction than the documented record of the same street.* A floor of one log
building where the record puts one, not a share â€” the plate gives no ratio, so a share would be a
number somebody chose. It runs over the anonymous layers together rather than per layer, because
splitting them would have carved an exemption for the household row on Lake, and an exemption
written to make a new gate pass is a gate that arrives disbelieved. **It is red at the commit before
this one and green at this one.** The principal streets come from the committed street hierarchy
(`data/streets/1835.json`, `traffic: principal`), not from a list in the tool; the street-line band
is the measured empty gap in the setback distribution (last building on the line 1.61 m, next
building anywhere 3.81 m), printed by `--setbacks`.

**What DID move, because a cabin is not the shape of a cottage.** Four derived layers read a lot's
building and re-derived around the swap, and the numbers are stated rather than swept up: dooryard
garden plots **15 â†’ 14**, dooryard stems **130 â†’ 128** across **63 â†’ 62** dwellings, town wagons
**68 â†’ 67** (one farm box, off a street verge). The lot-line fences kept their count exactly (111
fenced lots of 121 improved, 277 runs) and moved geometry only, and the street edge kept every metre
of its 1,214.5 m of walk â€” two of its refusal notes now name a different building. All four are the
rules doing what they are for; none was touched.

**What a visitor sees.** Standing on South Water Street looking at the river row, five of the
thirteen units are now log-walled, interleaved with the frame ones â€” a working frontier row rather
than a uniform frame terrace. **What is still invented is unchanged and L182 says so**: that any of
these buildings stood at all, which of them was of logs, and that they stood shoulder to shoulder.
The plate supports the treatment; it cannot say which building was which.
## Shipped â€” T-0179: the shed a family cannot carry is refused once, and the refusal is on the card

**The premise held for two of three, was refuted for the third, and missed a fourth.** T-0179
reported that C1, F1 and F4 are offered a shed by their crosswalk roof line that their own `ridge_ft`
band cannot carry. Swept against what the archetypes actually build â€” `tools/roof_form.py`, gated by
`tools/measure_ridge_reach.py`:

| family | ticket said | measured | why |
|---|---|---|---|
| C1 small shop | 231 of 441 | **231 of 441** | `frame_storefront._shed_roof` falls back-to-front, so the run is the 20-30 ft depth |
| F1 freight shed | 399 of 441 | **399 of 441** | `outbuilding`, no open side, so the fall is down 32-50 ft |
| F4 lumber shed | 441 of 441 | **0 of 441** | its own entry says `1/open`, "open posts", "part-open sides" â€” an open long side turns `shed_axis` and the fall goes across the 24-36 ft width |
| W5 riverside shop | not named | **84 of 441** | the sweep bails on a family with no pitch band before testing any FORM, so W5's shed had never been measured |

So the answer is **C1, F1 and W5**, not C1, F1 and F4, and the instrument that produced the original
list could not see one of its own cases. Both corrections are in `docs/LIBERTIES.md` L182.

**A second fault, found on the way and larger.** *Which* families get a shed was decided **five
times**, once as a literal inside each anonymous parcel, and the five had already drifted:
north/west/households name D2, A3, A4, A5; block/inferred_infill name D2, A3, A4. One roof stands on
the difference â€” `recon_1835_south_a5_044` is a gable where the other three A5s are sheds. The rule
now lives in `tools/roof_form.py` alone and all five parcels read it.

**A third, in the model rather than the data.** `tools/ridge_model.py` turned a shed's span with
`gable_front`, the way it turns a gable's. All three archetypes that build a shed
(`frame_dwelling`, `frame_storefront`, `log_dwelling`) use a private `_shed_roof` that falls from
the back wall to the facade and never reads the orientation at all, and `frame_tavern` has no shed
branch. Nothing caught it because no committed GLB is a storefront shed, so `measure_ridge_band.py`
had no roof to compare the model against. Corrected; the 261 modelled roofs and the 58-roof residual
are unchanged, because the correction only touches a form nothing is built with yet.

**What a visitor sees.** Thirteen cards â€” nine C1 shops, two F1 freight sheds, two W5 workshops â€”
carry a new paragraph on `roof_type` naming the form the specification offers, the span a shed would
climb, the ridge band it would miss and how many of the family's own footprints miss it, with this
building's own plan called out either way. Prose is not hashed into `mesh_inputs`' staleness recipe,
so **no geometry moved and no bake is owed by this run.**

**The gate, and it fails five ways.** `measure_ridge_reach.py` now joins the sweep to the deal: a
family dealt a shed its band cannot carry, a refused family's record that does not carry the
refusal, a parcel that grows its own copy of the shed set, the open-sided table drifting from the
crosswalk's own words, and a second parcel opting out of the rule. `--self-test` breaks each in
memory and is a step in `check.sh`. The sweep's grid and reach test are `roof_form`'s, so the gate
and the generators cannot be answering different questions.

**What is NOT done, named:** `recon_1835_south_a5_044` still stands on a gable. Giving it the shared
answer moves committed geometry, so it is held in `roof_form.AWAITING_BAKE`, banked by the gate at
exactly one entry that may shrink and may not grow, and filed as **T-0212**. And the underlying
question is still the owner's: the crosswalk's `ridge_ft` column is written for a gable's half-span,
and three families' shed reading cannot live inside it. Recording the refusal is not the same as
retiring it.
## Shipped â€” T-0034: the bloom had no target, but it had a CEILING, and the records were already over it

**The ticket was "raise the bloom", and R-W4c(b1) had already taken away the bar.** The 4â€“6 %
flower-load target is unsourced on one half and does not reproduce on the other; do not quote it.
The owner ruled on the ticket rather than picking one of (b1)'s three routes: *"I think you can
adjust that without source"* â€” the bloom may be tuned as a **reconstructed** value, bounded,
declared, never promoted. So this run did not re-derive a target. It asked the other question the
ticket's own title contains: **raising a number is only a raise if something downstream can carry
it.**

**The bar that governs the bloom is the lattice, and it is 0.346 forbs per square metre.**
`forbShareOf` in `renderers/web/js/flora.js` is `min(1, density Ã— cellÂ² / perCell)` â€” four slots to
a 3.4 m cell, one plant per slot, and not one plant more whatever a record says. On the build
before this change, **six of ten forb layers already sat on that clamp** (ROADMAP K58, still open):
for those, `density_per_ha` is a number the renderer cannot spend. K55 had already been bitten by
exactly this â€” it multiplied `z10_settled_town`'s forb density and drew the same 146 plants.

**And then nothing had to be invented, because the records already asked for more bloom than the
lattice can draw.** Every abundance in `data/flora` is a *range* â€” 400â€“900 yellow coneflowers to the
hectare â€” and the renderer had been reading its **midpoint**, a figure no source states, chosen
silently, planting every hectare of the town as the average hectare. The forb stratum's slot count
is now dealt off the **top** of each species' own recorded range instead (`stemsHigh` â†’
`subsetOn().densityHigh` â†’ `forbShare`):

| community | midpoint sum | recorded top | share was | share now | raise |
|---|---|---|---|---|---|
| `z02_mesic_prairie` | 0.2800 /mÂ² | **0.4080** | 0.809 | **1.000** | 1.236Ã— |
| `z01_wet_prairie` | 0.2760 | **0.4070** | 0.798 | **1.000** | 1.254Ã— |
| `z09_sand_prairie` | 0.0725 | **0.1140** | 0.210 | 0.329 | 1.572Ã— |
| the other seven | â€” | â€” | 1.000 / 0 | 1.000 / 0 | **none** |

The mesic prairie's records sum to **0.408** where the lattice carries **0.346**, so **18 % of what
the evidence asks for is clipped by a rendering constant**. No record changed and none was
overwritten; the species lottery still runs on the midpoints, so the *mix* of the sward is
identical and only the number of slots filled moved. It is `docs/LIBERTIES.md` **L182**,
reconstructed tier, bounded by the records themselves: no species is planted denser than its own
record's larger figure. The shrub stratum is deliberately excluded â€” a denser shrub layer is more
bushes, not more bloom.

**What a visitor sees.** At `prairie_west`, **206 forbs and 1,617 flower heads â†’ 256 and 1,968**,
for 8,191 more sward triangles; at `prairie_south`, 125 and 949 â†’ 155 and 1,122. **And it is the
last raise either prairie can be given** â€” both now read a share of 1.000 with no headroom left, so
the next flower on that ground needs a different lattice and not a different number.

**The instrument, and two readings that had to be wired for it.** `tools/measure_bloom_headroom.mjs`
is new, committed and carries `--assert`. It drives the placer through its own entry points â€”
`flora.update` with a synthetic camera, then `flora.stats` and `flora.communities()` â€” and asks the
three ceilings between `density_per_ha` and a flower on the screen which of them binds. It needed
`flora.stats.caps` (the ceiling beside each set's count) and `flora.forbLattice` (the lattice
geometry the clamp is against), because both were inside the module and unreadable from outside:
**a share sitting on its clamp had looked exactly like a share that was simply small.** It is not
in `tools/check.sh` â€” it drives a browser â€” and is a measurement to be re-run and quoted, in the
shape of `tools/measure_sward_draw.mjs`.

**Two findings this run did not cause, both filed rather than fixed.**

- **T-0208** â€” `flora-head-spike` in the settled town and `flora-head-dome` in the wet woods stand
  at **820 of 820** and truncate silently: `maybeHead` stops pushing mid-plant when a set is full,
  and nothing reports it. Measured across every community at four bearings, **on the build before
  this raise as well as after**. The nine head sets share nine separate ceilings of 820 and the
  aggregate is barely a fifth spent at the worst stand, so it is an allocation, not a budget.
- **T-0209** â€” the head ring reaches **23.65 m** while the sward is carried to **175 m** as
  aggregate cards that carry no head at all, so **bloom covers 1.8 % of the ground the sward
  covers**. That is the real answer to "raise the bloom" and it is a DISTANCE, not a density: this
  parcel spent the whole of the lattice's remaining 24 % and the frame past twenty-four metres did
  not change by a pixel.

**What was NOT done, deliberately.** No ceiling constant was raised. `TUNE.forb.cell`,
`TUNE.forb.perCell` and `TUNE.cap.head` are exactly what they were â€” the room this run spent was
room that already existed inside the records, and where it ran out the run says so and files the
parcel rather than moving the number that was in the way. R-W4c(b1)'s route 3 â€” retiring the 4â€“6 %
figure from the three documents that still quote it â€” is also not done here; it is a documentation
sweep and this parcel is a prairie.
## Shipped â€” T-0032: the town held 662 roofs, because three of the six civic slots counted nothing

**The open half of T-I3, closed on the owner's delegated pick.** He ruled on 2026-08-17: *"close it
at 665 or 662 â€” either is close."* It is **662**. T-I3(a) had already enumerated the town's public
buildings and found three roofs â€” the log jail, the council house and the lighthouse, all three
committed named records â€” against a family target of six. Route 2, re-typing the three spare slots
into ordinary families, was refused for the reason T-I3(a) established: they were a count of
nothing, not miscategorised real roofs, so re-typing would have invented three buildings on the
strength of an arithmetic artifact.

**Every candidate is settled against the dataset, not against the dossier.**
`tools/measure_institutional_claims.py` now carries the civic ledger and re-derives it on every run
of the gate: three **stood** (each an I3 entry in the physical-roof reconciliation crediting a
roof); four came **later** â€” the court-house (fall 1835; a committed record the reconciliation
credits none), the engine house (contracted 30 December 1835), the market house (1837), the custom
house (Chicago was not a port of entry until 1846); two were **functions with no building of their
own** â€” the United States Land Office, working four weeks before the scene date out of a room on
Lake Street, and a town hall the corporation never built; and the estray pen **stood and was
roofless**. The gate fails if the I3 target is not the number that stood â€” above it is a slot that
counts nothing, below it is a documented roof with nothing to count against â€” and nine self-test
cases break each assertion in memory to prove it fires.

**The correction found a second fault in the same row, and this is the part worth keeping.** The
inventory apportioned twelve institutional roofs as **south 10 / west 1 / north 1** while the named
records stand **south 5 / west 1 / north 3**. Two authored views of the same aggregate â€” a family
schedule and a districtÃ—group matrix â€” were never cross-referenced, so the schedule kept finding
institutional headroom in the South Division that no evidence supports and none in the North where
three of these buildings are. That is the T-I3(a) shape again: not a document disagreeing with the
data, but the data disagreeing with itself in two files nothing read together. The row is now the
census, and the gate holds it there.

**What moved.** `roof_total` **665 â†’ 662**; `principal_functional` **511 â†’ 508** (all three phantom
roofs were principal, so `ancillary` stays 154 and the programme's ratio becomes 154:508 â€” the block
ceiling is unchanged at either ratio, checked rather than assumed); `family_targets.I3` **6 â†’ 3**;
`institutional_public` **12 â†’ 9**, south 10 â†’ 5 and north 1 â†’ 3; the **south district target 370 â†’
365** and the **north 150 â†’ 152**. Downstream, `reconcile_665.py` re-derives 338 standing and **324
remaining** (was 327), with **296** gated on coverage (was 299). **Every I3 slot has left the
schedule** â€” one at `blk_lake_franklin`, one at `blk_south_water_market`, three in the South balance
â€” so no block is short a roof because the schedule dealt it a family every generator refuses.

**What a visitor sees.** The gate screen reads **338 buildings standing, of the 662 the town held**.
Nothing in the scene moved: no building was added, removed, re-typed or re-dated, and the standing
count is 338 exactly as it was.

**What was deliberately not done.** The filename `1835_665_roof_programme.json` and the tool name
`reconcile_665.py` **stay**, each carrying a line saying the number in the name is history; renaming
them is churn the ruling does not require, and the live total is always `remaining.of_target`.

## Shipped â€” T-0023 + T-0189: the Randolphâ€“Washington row stops inheriting South Water's rules

**Two things the row was given by a street it does not stand on, at two layers of the same
records: the criterion that decides which roof is better, and the sentence that tells a visitor
what row they are standing in.** Both were written for T-0078's party-line run on South Water
Street, where both were true. Both were then applied verbatim to every frontage run since.

**T-0023 / K31 â€” the end rule's criterion is now the WALK.** The rule keeps its claim, unchanged
since T-A8 and invented since T-A8: the better roof stands nearer the Dearborn Street drawbridge,
the only crossing of the main stem in July 1835. What changes is the distance â€” **walked along the
committed street centrelines** from the roof's own frontage, not T-A11's straight line. It lives in
`data/reconstruction/1835_platted_block_parcels.json` â†’ `placement_rule.end_rule`, and
**`tools/measure_end_rule.py`** prints it so the next parcel quotes rather than re-argues. Full
admission in `docs/LIBERTIES.md` **L182**; the resolution is written into ROADMAP Â§ K31.

**Four measurements decided it, taken on all 36 faces of the platted grid.**

1. **The two criteria name the same nearest lot on 36 of 36 faces.** K31 warned the successor must
   not be chosen where it agrees with the old rule. They agree everywhere, so **no block could have
   discriminated between them, and the choice was never about which roof goes where.** Nothing was
   re-graded and nothing was retro-fitted; L102 onward stand verbatim.
2. **The straight line measures how far away the BLOCK is, not where a roof stands on it.** Its
   worst step between two neighbouring party-line units runs from **6.06 m** on the far blocks to
   **0.52 m** at `blk_randolph_clark` â€” it goes blind as a block approaches the bridge, weakest
   exactly where the bridge matters most. **It is below the floor on 12 of the 36 faces**, the back
   face of `blk_south_water_clark` â€” the block T-A11 wrote the rule on â€” among them. The exhaustion
   was never a fact about this row; the row reached it first.
3. **The floor is the recipe's own admitted invention.** It deals its 48 principal slots setbacks of
   **4.0 m to 7.5 m** and grades them "a period typology and not a measurement of this lot". A
   setback moves a roof along the outward normal, broadly the axis the rule reads, so **3.50 m** is
   noise the records already declare on the same line. The rule now records the within-face order as
   **arbitrary** where its step falls at or under it â€” K31's third candidate, kept as a bound rather
   than adopted as the answer. Under the walk no committed face is in that position.
4. **T-0079 changed what the rule ranks and nobody noticed.** Before the core density standard a
   block carried one roof per lot, so the rule ordered LOTS ~24.6 m apart; a party-line run now
   stands three units on ONE lot ~6 m apart, so **the rule has been ranking the front doors of what
   the plat calls a single property.** That, more than the bridge's bearing, is why it ran out of
   room. Under the walk the step is the unit's own 6.072 m on every face.

**A reproduction, and it found a real discrepancy.** T-A11's eight figures re-derive within
**1.7 m** (ratio 2.908 against 2.86) â€” it read the frontage. T-A15's read **26.4 m nearer**, which
is a lot's frontage-to-middle distance; L106 names the point in passing ("the 49.3 m between the lot
2 and lot 6 **centroids**"). **The criterion had been read at two points 26.5 m apart on two blocks
and neither parcel said which.** T-A15's finding is unaffected â€” its spread reproduces at **7.86 m**
against 7.5 m.

**T-0189 â€” and the sentence describing all this was wrong on 9 of 23 cards.** The bold location line
and the position note beside it are the first two things a visitor reads on a party-line unit.
Three houses on **Washington Street**, 400 m from the water, were told they were "one unit of the
party-line **river** row", standing on "the town's **river business front**", looking at "Washington
Street **and the river beyond it, as every documented store on this face does**" â€” on a face whose
entire documented 1835 frontage is the estray pen, the town's pound for stray animals. Three more
stand on Randolph, three on Lake; the other 14 are on South Water and were always right. All three
phrases now name the face the building actually stands on, and the note says in terms that a row on
any other face is **borrowing** the treatment from the 1834 South Water view rather than being drawn
by it. Recorded as **L183**.

**Not one coordinate moved.** All 23 records and their sidecars re-derive from the same recipe and
the same committed block boundaries; the phrases describe the placement, they do not decide it.

**What is NOT done and is filed rather than dodged.** The frontage note still says "its east wall is
fixed by the west end of the run's own frontage" on a west-anchored run â€” the generator's internal
convention leaking into visitor prose. It is confusing rather than false, it is not about 1835, and
it is its own ticket.
## Shipped â€” T-0054: 23 standing liberties compiled as settled, because Resolved was the last section

**The count, measured rather than assumed.** The ticket said "every liberty appended since L111",
seventeen of them. It is **23**, and they are not a range: of the **71** entries numbered L111 and
above, **24** sit under `## Resolved` and one of those (L116, the sycamore drawn as an elm) genuinely
belongs there. The other 47 were placed by hand in the right section by whoever wrote them. So the
fault is intermittent â€” it catches whoever appends at the end of the file, which is what this
document tells you to do â€” and it had reached **L181**, written three days ago. `data/liberties.json`
compiled **34** entries `section: "resolved"`; **11** carry a `**Resolved:**` line saying what
settled them.

**Why it is not cosmetic.** `validate.py` exempts the Resolved section from the check that a claimed
invention is *still* an invention â€” the exemption is what lets an append-only document survive its
own data being corrected. **12 of the 65 exempted claim tokens were exempt by accident**: the four
Lake-and-Clark roofs' footprints and positions (L144) and the four State Street and La Salle slough
claims (L149, L150). Put back under the check, **all twelve pass** â€” every one is still an invention,
which is exactly what makes the label a lie rather than a nuisance. On screen it was worse than the
gate: ten building cards carried a scope chip reading *resolved* on a liberty that still stands,
including the Western Hotel's wagon-yard fence (L127), which is standing in the town.

**Fixed by moving the trap, not by patching around it.** `## Resolved` now sits **above** the
per-subject register instead of below it, so appending at the end of the file â€” the operation the
document mandates â€” lands where a new liberty belongs. No liberty text is edited and none is
removed: the 23 stay exactly where they were written and the 11 settled entries move up. The
compiled sections are now 3 standing / 167 per-subject / 11 resolved.

**And the guard, because a reshaped file can be reshaped back.** `compile_liberties.py` now decides
`resolved` from **two independent statements that must agree** â€” the section an entry sits under,
and whether its own text carries the `**Resolved:**` line the section's preamble has always asked
for. Either half alone is reported by id and fails `check.sh`; a misfiled entry compiles as
`per_subject`, which is the reading that keeps its obligations. This is the T-0207 lesson used the
other way round: *that* fault was invisible because two derivations of one source agreed, so the
repair here is a second statement that is not derived from the first.

**One deliberate change to what a visitor sees beyond the chips.** The derived file is now emitted
grouped standing â†’ per-subject â†’ resolved, stable within each group, so the Evidence panel's order
is a decision in the compiler rather than a side effect of where a section sits in a 7,800-line
markdown file. The order on screen is the same order as before the reshuffle.
## Shipped 2026-08-24 â€” T-0157: a phone multisamples the town, and the obvious number said not to

**The ask.** `main.js` had read `antialias: !coarse` since Milestone 0 â€” the renderer's first
commit, 2026-08-09, before there was a town to look at â€” so every touch device drew the whole
reconstruction with no multisampling. T-0013 had established that every one of the 627
interior-flickering pixels at `from_above` is an edge and that **only sample density touches
them** (supersampling healed 83â€“93 %; a shading change that moved 164,572 px healed none), but
every reading it took was at 1280Ã—800 on the DESKTOP boot, where MSAA was already absorbing most
of it. The ticket asked for the phone to be measured first, and for the flag to be shipped only
with a frame cost in hand.

**The instrument, and the gap it had to close first.** `tools/measure_phone_aa.mjs`. Before it
could read anything, one thing had to be fixed: `measure_tie_class.mjs`'s `TIE_VIEWPORT=mobile`
opens a plain `newPage({ viewport })`, and `prefersTouch()` is `(pointer: coarse)` or
`maxTouchPoints > 0 && innerWidth < 900` â€” **a viewport satisfies neither**, so the existing
"mobile" reading was the DESKTOP renderer in a narrow window: `antialias: true`, `detail: full`,
the pointer-lock backend. This is the same class of finding T-0018 filed against
`SWARD_VIEWPORT=mobile` ("changes the browser page size but not `lowSpec`"), now measured on a
second instrument. Every figure below comes from a context with `hasTouch: true` and
`deviceScaleFactor: 2` â€” what `smoke_renderer.mjs` uses for the release gate â€” and the run prints
the three readings that prove the coarse path took: `pointer: coarse true`, `detail "light"`,
`pixelRatio 1.5`.

`antialias` is a context-creation attribute with no runtime handle, so the control is an init
script that rewrites the one attribute inside `HTMLCanvasElement.prototype.getContext` before
three.js sees it â€” and it is **proven live**, not asserted: the run reads
`getContextAttributes().antialias` AND `gl.getParameter(gl.SAMPLES)` off the live context and
aborts unless they are `false`/0 or `true`/4. R-A1's frozen readback and R-BUG6(a)'s inert
`--no-sun-shadow` are why that is written down.

**THE MEASUREMENT REFUTES ITS OWN HEADLINE NUMBER, AND THIS IS THE FINDING.** At 390Ã—780 on the
published mirror, 2 mm nudge, shadow map off by R-BUG6(a)'s repaired control, control 0 px and
return-to-pose 0 px on every run:

| station | flicker px | HARD FLIPS (â‰¥ 64 of 255) | worst Î” | mean Î” |
|---|---|---|---|---|
| `from_above` off â†’ on | 1,056 â†’ **2,482** | 25 â†’ **0** | 105 â†’ 28 | 15.6 â†’ 6.8 |
| `lake_market` off â†’ on | 4,843 â†’ **7,310** | 124 â†’ **0** | 140 â†’ 37 | 14.8 â†’ 6.4 |

**The flicker COUNT â€” the figure T-0013 and three boxes of ROADMAP quote â€” goes UP by 135 %
aerial and 51 % at eye height when MSAA is switched on.** A run that measured only the count
would have refused this change on its own evidence. The count rises because a partial resample
touches more pixels than a whole flip does; what collapses is the SEVERITY. Every one of the 149
pixels that were swapping surface outright stops doing it â€” not fewer, none â€” and the worst
single pixel moves about a quarter of what it did. That is exactly the difference between an
edge that crawls and an edge that is resolved, and no pixel count on its own can see it.

The mobile interior/silhouette split the ticket asked for, at `from_above`, antialias off as
shipped: structures 346 interior / 74 silhouette, trees 188 / 134, ground 125 / 54, water 20 /
49, streets 0 / 9, flora 0 / 2. Quoted with T-0013's correction attached â€” `interiorOf` knows a
layer's outline against the rest of the scene and cannot see the boundary between two surfaces
OF that layer, so 94â€“98 % of an "interior" count is internal silhouette.

**The whole table reproduced digit for digit on a second independent run** â€” 1,056 / 25, 4,843 /
124, 2,482 / 0, 7,310 / 0, every per-layer row identical.

**And a finding about the ownership test at EYE HEIGHT, recorded rather than smoothed over.**
`measure_tie_class.mjs`'s footprint partition had only ever been run aerially, and its own header
warns that *"a large overlap between two layers is a bug in this tool rather than a finding"*. At
`from_above` the overlaps are small â€” 0, 5, 9, 0, 63, 310 of 1,056 â€” and the partition is sound.
At `lake_market` the ground's footprint overlaps the streets' on **2,436 of its 2,607** flickering
pixels, because the street layer is a skin on the heightfield and hiding either one moves the same
pixels. Every pixel is still counted exactly once, but which of those two layers gets the credit
is decided by the LAYERS list order rather than by çÝ¶ó†òµë(š+myÒF†RÖ6²†6öÖ×Væ—G”B‚–&VgW6W2FW'&–âæ—5vFW&÷WG&–v‡BÂæBF†P§ÆçF–ærÆö÷FW7G2F†RW†7B7FVÒö–çB&Vf÷&R—B6·2ç’V6öÆöv–6ÂVW7F–öâ’âF†R76R—2&–v‡@®(	BWfW'—F†–æröâF†BF‚—2TåRF‡&÷Vv†÷WBâF†RÖ6²æBF†RG&vâvFW"Fòæ÷BF—6w&VR†W&Rà¤æ÷F†–ær7G&V×27BÆ6VÖVçBvFRâ¢¥F†RfVÇBv2–â÷VÆF–öâæö&öG’†BÆ—7FVB2§7W7V7B¢¢ÂæBF†B—2F†Rf–æF–ærv÷'F‚¶VW–æs¢F†R6æF–FFRÆ—7Bv2w&—GFVâg&öÒF†P¦æV"Öf–VÆBÆçFW"Â&V6W6RF†B—2v†W&R6V&6‚f÷"'v†BÆçG2F†–æw2"ÆVG2ÂæBF†RF†–æp§F†BG&WrF†W6RG&VW2FöW2æ÷BÆçBç—F†–ærà ¢222v†B6†—V@ ¦6öÇfT†÷&—¦öâ‚–æ÷r6·2FW'&–âæ—5vFW"‡RÂâ–BWfW'’VÖ—GFVB6×ÆRæB6¶—2—B(	B6×ÆV@¦BF†RVÖ—GFVBö–çB&F†W"F†âB&öG’w2fW'F–6W2Â&V6W6R&VÇB6â7&÷726†ææVÂ&WGvVVà§GvòG'’VæG2Âv†–6‚—2v†BF†Ræ÷'F‚'&æ6‚&VÇBFöW2â÷WG6–FRF†RÖöFVÆÆVB†V–v‡Ff–VÆBF†RÖ6°§&WGW&ç2—G2fÆÆ&6²æBç7vW'2&G'’"ÂæBF†B—2F†R†öæW7Bç7vW"F†W&S¢F†—2&ö¦V7B†2æð§7W'fW’öbF†Bw&÷VæBà ¥Gvò&VFW'2ÂæBF†W’&Ræ÷B&VGVæFçBâFööÇ2öÖV7W&Uöf%÷F–Ö&W"ç–6Vç7W6W0¦†V–v‡Ff–VÆBæ&–æ–âFFööâWfW'’6öÖÖ—C²G&VW2æf%F–Ö&W%vFW"‚–6Vç7W6W2F†RÖ6²F†R'&÷w6W ¦ÆöFVBöfbF†RV&Æ—6†VBÖ—'&÷"ÂæB6Öö¶U÷&VæFW&W"æÖ§676W'G2F†RGvòw&VRv–ç7BF†R&æ¶V@¦çVÖ&W'2â¢¥F†W’w&VR6×ÆRf÷"6×ÆRæBFòF†RÖ–ÆÆ–ÖWG&RöâÆÂf—fR&öF–W2¢¢(	BF†P¥"Ô%Ts62Ö6Æ7277V×F–öâ76W'FVB&F†W"F†â77VÖVBf÷"F†Rf—'7BF–ÖRöâF†—2Æ–W"âF†R6Öö¶P¦Ç6ò76W'G2†÷&—¦öåvWE6¶—VBâg&öÒ7FæBv†W&RF†R&VÇB6ÆV'2Ô”åôd%ôÖ¢¢¦g&öÒF†P§7vâö–çBF†R&VÇB—23#’ã"Òv’v–ç7B33Ò7WBÖöfb¢¢Âã‚Ò–ç6–FR—BÂ6òvFRF†@§6öÇfVBöæÇ’B7vâv÷VÆB†fRW†W&6—6VBæ÷F†–ærâÖV7W&VBöâF†R6†—VB'V–ÆBg&öÒF†B7FæBÀ¢¢£r6×ÆW26Æ—VB¢¢à ¢222v†B—2äõBf—†VBÂæB—B—27FFVB&F†W"F†âW&VB÷fW  ¢¢¦Ö–å÷7FVÕö&VÇEöV7Fæ÷rG&w2æ÷F†–ærÂ&V6W6RæöæRöb—Bv2öâÆæBâ¢¢&W—&–ær—BÖVç0¦6†ö÷6–ærv†W&RF†R&VÇBw2æV"VFvR7GVÆÇ’&âÂæBæò6÷W&6RF†—2&W÷6—F÷'’†öÆG26WGFÆW2F†B(	@§F†Ræ÷FRF†B&öGV6VBF†RfVÇB—2—G6VÆbF†R&ö¦V7Bw2&W7B7W'&VçB&VF–æröbæG&V2‚'F†R6÷WF€¥6–FRF–Ö&W"W‡FVæE¶VEÒV7B2f"2vVÆÇ27G&VWB"’â6†ö÷6–æræWrÆ–æRFòÖ¶RF†R6Vç7W2w&VVà§v÷VÆB&R–çfVçF–ærF†RF†–ærF†RÖV7W&VÖVçB§W7B6†÷vVBæö&öG’¶æ÷w2âF†RGvòöffVæFW'2&R&æ¶V@¦'’æÖR–âFööÇ2öf%÷F–Ö&W%ö&6VÆ–æRæ§6öæ¢F†RfVÇBÖ’6‡&–æ²æBÖ’æ÷Bw&÷rÂæWröffVæFW ¦f–Ç2ÂæB&W—"F†Bf÷&vWG2Fò&RÖ&æ²f–Ç2FöòâF†R&VæFW&W"†ÆbæVVG2æò&6VÆ–æRæB†0¦æöæRâ¢¥"Ô%TsR†"’w&—FW2WF‡&VR&÷WFW2f÷"F†R÷væW"æB—2æ÷B–6²v—F†÷WB†–Òâ¢  ¢22f—†VB##bÓ‚Ób(	BF†R6—‚ÖVF÷rÆçG2&R7FæF–ærÂæBF†R67&VVç6†÷BF†R&6VÂ6¶VBf÷"fWFöVB†Æb—G2÷vâ&W—  ¢¢¤³C’†"’¢¢ÂF†Rf—‚†Æböb³C’†’âf—6—F÷"6â6VR—C¢¢§&—&–RFö6²—27FæF–ær–âF†RvW@§&—&–R¢¢ÂGvòÖWG&W2öb66R÷fW"ÖWG&R×v–FR&÷6WGFRÂv†W&R—G2÷vâ&V6—R÷vVB2ã#2öbF†VÐ¦æBæöæR7FööBâvFW"†VÖÆö6²—2&W6–FR—BÂvööBæWGFÆR—2öâF†Rf÷&W7BfÆö÷"Âæ–æV&&²æBv–Æ@¦v&Æ–2&RöâF†R&—fW&&æ²ÂF†R6ö×72ÆçB—2öâF†RÖW6–2&—&–Rà ¢¢¤ÖV7W&VBÂFööÇ2öÖV7W&U÷7v&EöG&ræÖ§6öâF†RV&Æ—6†VBÖ—'&÷"ÂÆÂV–v‡B6öÖ×Væ—F–W3 £bÃsƒ6Æ÷G2(i"bÃs“RÂæBb7V6–W2÷vVBv†öÆRÆçBæBG&vâæ÷v†W&R(i"â¢¢F†R6WGFÆVBF÷vâ(	@§F†RöæR6öÖ×Væ—G’F†R&VÆV6R6Öö¶Rw2÷vâ7FF–öâ7FæG2–â(	B7F–ÆÂ&W÷'G2'6VçBÂ6òF†P§&W—"F–Bæ÷BÖ÷fRF†RfVÇBFòF†RöæÇ’Æ6RF†RvFR6â6VRà ¥F†R6öç7G'V7F–öâ—2F†RöæR³C’†’&W67&–&VC¢&æ²ÓÆGF–6Rg&2†<+|ë²,+|ë"²¼+|ë2²6†–gB–öà§F†R6Æ÷Bw2÷vâ¢§v÷&ÆB¢¢6ö÷&F–æFW2…#2vVæW&F÷'2’ÂvÆ¶VBv–ç7BF†R4Db–6²‚–Ç&VG§vÆ·2â7FFVÆW72Â6ò&RÖ6VçG&–ærF†RÆGF–6RWG2F†R6ÖRÆçB&6²æBæ÷F†–ær6†ævW27V6–W0¦2–÷RvÆ²WFò—Bâ³C‚w266÷VçBÖ¶VW–ær–6¶W"v2æ÷B÷'FVBà ¢¢¥F‡&VRf–æF–æw2ÂæBF†R6V6öæB—2F†RG&ç6fW&&ÆRöæRâ¢  £â¢¥F†RF†–ææ–ær†2Fò&R'BöbF†R6ÖRG&râ¢¢6²&FöW2ÆçB7FæB†W&R"æB'v†–6€¢7V6–W2"öbGvò–æFWVæFVçBçVÖ&W'2æBF†R7W'f—f÷'2&R§&æFöÒ7V'6×ÆR¢öb¢Æ÷rÖF—67&Wæ7’6WB(	Bv†–6‚—2ö—76öâv–â–â—G2F–ÂÂ’æRâF†RfVÇB&V–ær&W—&VBà¢FVÇB‚–6·2&÷F‚öböæRG&s¢RÂ6†&V6'&–W2F†RÆçBÂæBVw2÷6—F–öâ–ç6–FP¢³Â6†&R–vÆ·2F†R4Dbâ6ÖRÖ&v–æÇ2ÂöæR7G&F–f–VBG&rà£"â¢¥D„RDTå4RÄ”U%24ääõBD´R•BÂäBD„R4Tå5U2tõTÄB„dRÔU$tTB•Bâ¢¢Æ–VBFòF†RæV ¢æBÖ–BGVgG22vVÆÂÂF†R6ÖR6öç7G'V7F–öâw&WrF†RvW7B&—&–R¢¦–âf—6–&ÆR&÷w2v—F‚&&P¢w&÷VæB&WGvVVâF†VÒ¢¢(	BÆGF–6R&æB—2fÖ–Ç’öbæV"ÖF–vöæÂÆ–æW2Â–çf—6–&ÆRBGvð¢ÆçFVB6Æ÷G2–â‡VæG&VBæBVæÖ—76&ÆRB6—‡G’âF†R6Vç7W26ÆÆVBF†BfW'6–öâà¢–×&÷fVÖVçB‡v÷'7B6†÷'FfÆÂ3ãCr(i""ãƒr’æBWfW'’çVÖ&W"v2w&VVã²Gvò7&—F–5÷6†÷G6 ¢g&ÖW2B&—&–U÷vW7FÂ&Vf÷&RæBgFW"Â&VgW6VB—B–âöæRÆöö²âF†RÖG&—‚Æ—7G2vW&P¢Æ÷6–ær¢¦æò¢¢7V6–W2FòF†RF–ÂÂ6òF†R6÷7Bv2ÆÂf—6–&ÆRæBF†R&VæVf—BÆÂ–â6öÇVÖà¢F†BÇ&VG’&VB¦W&òâ¢¥F†Rf÷&"Æ–W"¶VW2F†R7G&F–f–VBG&s²æV"æBÖ–B&P¢VçF÷V6†VBÂæBF†V—"v÷'7B6†÷'FfÆÂ7F—23ãCrâ¢¢F†R7V66W76÷"—2¢¤³C’†B’¢¢à£2â¢¥F†R&Æö6²6—¦R—26WB'’ÆçFVB6Æ÷G2Âæ÷B'’6VÆÇ2â¢¢F†R7&æÆWž(	5GFW'6öâ&÷FF–öâF†@¢'&V·2F†RÆGF–6Rw2F–vöæÇ2—2¶W–VBöâv÷&ÆB&Æö6³²BL9sB6VÆÇ2F†Rf÷&"Æ–W"ÆçG0¢öæR÷"GvòW"&Æö6²Â6òF†R&÷FF–öâv2ÆÂF†B7W'f—fVBæB¢§F‡&VR¢¢7V6–W27F–ÆÂ7Föö@¢æ÷v†W&RâBl9sb‡ãÃ#B6Æ÷G2ÂãSBÒÂ&÷WBF†Rf÷&"&–ærw2÷vâv–GF‚’æöæRF–Bà ¢¢¤æ÷B6Æ–ÖVC¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BF†—2'VææW"w2ÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–ær’âFööÇ2ö6†V6²ç6†ÂF†RÖö&–ÆR6Öö¶RöâF†RV&Æ—6†VBÖ—'&÷"ÂF†R6Vç7W2æ@¦&÷F‚7&—F–5÷6†÷G6g&ÖW2&Rw&VVââæòFFö6†ævRÂæò&¶Rà ¢22f÷VæB##bÓ‚Ób(	B6—‚ÆçG2F†RÖVF÷r&V6—W2÷vRÆ6RFò7FæBæ÷v†W&RÂæBF†RvFRw2÷vâ7FF–öâ6ææ÷B6VRç’öbF†VÐ ¢¢¤³C’†’¢¢ÂF†RÖV7W&VÖVçB†Æböb³C’âæ÷F†–ærf—6—F÷"6â6VR6†ævVC²F†Rf—†W2&P¢¢¤³C’†"’¢¢†æò&W6V&6‚æVVFVBÂ7FæG26—‚ÆçG2W’æB¢¤³C’†2’¢¢Â&÷F‚4TTâà ¤³C‚Æ÷7BF†RÖW&–6â7–6Ö÷&R&V6W6R6ÖÆÂvV–v‡FVB6×ÆRÆ÷6W2—G2&&RVæBÂæB³C’6¶V@§v†WF†W"F†R6ÖR—2G'VRöbF†R7v&B(	B¢£‚öbF†RSBÆçB&V6÷&G2¢¢Âv–ç7BG&VW2æ§6w23bÀ¦æBæWfW"öæ6R6÷VçFVBâ—B—2G'VRâÖV7W&VB'’FööÇ2öÖV7W&U÷7v&EöG&ræÖ§6öâF†RV&Æ—6†V@¦Ö—'&÷"Â7FæF–ærF†RÆ6W"–âWfW'’6öÖ×Væ—G’–âGW&â(	B¢£‚6öÖ×Væ—F–W2Âb÷VÆFVBÆ—7G2À£bÃsƒ6Æ÷G2FVÇBÂv÷'7B6†÷'FfÆÂ3ãCr6Æ÷G3¢¢  §Â7V6–W2Â÷vVBÂÆ—7BÂ&V6÷&FVB2À§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â¢§&—&–RFö6²¢¢6–Ç†—VÕ÷FW&V&–çF†–æ6WVÖÂ¢£2ã#2¢¢Â£÷vWE÷&—&–Ræf÷&&ÂFVç6—G•÷W%ö†À§ÂvFW"†VÖÆö6²6–7WFöÖ7VÆFÂ"ãc"Â£÷vWE÷&—&–Ræf÷&&ÂFVç6—G•÷W%ö†À§ÂvööBæWGFÆRÆ÷'FVö6æFVç6—6ÂãsBÂ£eöFVç6Uöf÷&W7Bæf÷&&Â6÷fW%ög&7F–öæÀ§Âæ–æV&&²‡—6ö6'W5ö÷VÆ–föÆ—W6ÂãCRÂ£U÷&—fW&&æµ÷F–Ö&W"æf÷&&Â6÷fW%ög&7F–öæÀ§Â6ö×72ÆçB6–Ç†—VÕöÆ6–æ–GVÖÂãBÂ£%öÖW6–5÷&—&–Ræf÷&&ÂFVç6—G•÷W%ö†À§Âv–ÆBv&Æ–2ÆÆ—VÕö6æFVç6VÂã"Â£U÷&—fW&&æµ÷F–Ö&W"æf÷&&Â6÷fW%ög&7F–öæÀ ¥&—&–RFö6²—2.(	32ÒÆçB÷fW"&÷6WGFRãn(	3ãÒ7&÷73¢F†RvWB&—&–R—2÷vVBF‡&VRö`§F†VÒæB7FæG2æöæRà ¢¢¤æBF†R†&æW726÷VÆBæ÷B6VR—BÂv†–6‚—2F†Rf–æF–ærF†B—2æ÷B&÷WBfÆ÷&â¢¢F†R&VÆV6P§6Öö¶R&VG2F†R6ÖR6Vç7W2ÂBv†FWfW"7FF–öâF†RvFR—27FæF–ær–â(	BF†R6WGFÆVBF÷vâÂ¢£c€§6Æ÷G2ÂöæR6öÖ×Væ—G’öbFVâ¢¢(	BæBg&öÒF†W&RF†Rç7vW"—2#'6VçB"âf—'7BG&gBöbF†—0¦VçG'’V÷FVBW†7FÇ’F†BæB6ÆÆVBF†R7v&Bw2F–Â6ÆVââ—Bv2F†R6×ÆRF†Bv26ÆVâà¤WfW'’W"Ög&ÖRf–wW&RF†R6Öö¶R&–çG2†2F†—26†RÂæBF†R&W—"v2FòÖ÷fRF†R–ç7G'VÖVçBÀ¦æ÷BFò6†ævRv†B—B6÷VçG2à ¢¢¤6V6öæBfVÇB6—G2VæFW&æVF‚ÂöæRÆ–æRV&Æ–W"â¢¢–6²‚–FVÇ24ÄõE2ÂæB6Æ÷B—2öæRG&và§ÆçBâ7FV×5÷W%öÓ&æBFVç6—G•÷W%ö†&R6÷VçG2öbÆçG3²6÷fW%ög&7F–öæ—2â&Vö`¦w&÷VæBâ'V–ÆE7V6–W6æ÷&ÖÆ—6W2ÆÂF‡&VR–çFòöæR6†&RÂ6ò¢&6÷fW'2#RRöbF†Rw&÷VæB"¢—0§&VB2¢#ã#RÆçG2W"7V&RÖWG&R"¢(	BF†R6ÖR6VçFVæ6R&÷WBGvòÖÖWG&RFöwvööBæB&÷W@¦v–ÆBv&Æ–2à ¢¢¥6—‚öbGvVçG’Æ—7G2Ö—‚F†RGvòÂFF6WB×v–FR¢¢‡6òF†Rf–wW&RFöW2æ÷BÖ÷fRv—F‚F†R6ÖW&“ ¦£eöFVç6Uöf÷&W7Bæf÷&&¢£“bãRR¢¢öb6Æ÷G2FVÇBöfb6÷VçG2v–ç7B7V6–W2&V6÷&FVB26÷fW"À¦£…öÆ¶W6†÷&RæÖG&—†BãRÂ£5÷6VFvUöÖVF÷ræf÷&&ã"RÂ£5÷6VFvUöÖVF÷ræÖG&—†2ã‚RÀ¦£•÷6æE÷&—&–RæÖG&—†ãrRÂ£÷6WGFÆVE÷F÷vâæf÷&&ãbRâF†Rf÷&W7BVæFW'7F÷'’—2F†P¦W‡G&VÖS¢&×2B"ãR7FV×2öÜ+"F¶R“bRöbF†BÆ—7Bv–ç7Bæ–æR6‡'V'2à ¢¢¥F†R&W—"—2&Æö6¶VBöâFFÂæBF†B—2v‡’F†—2—2†’â¢¢6öçfW'6–öâæVVG2F†RÆçBw2÷và¦fö÷G&–çBÂæB¢£#R&V6÷&G2v—fR6÷fW"g&7F–öâv—F‚æòv–GF…öÖ¢¢(	Bö÷&FVç6—6Âv†–6‚—0£cRöbF†RF÷vâw2ÆvâÂæBÆÂF‡&VR6÷fW"×&V6÷&FVBf÷&'2öbF†R6VFvRÖVF÷rÖöærF†VÒâF†P§Æ6W"w2W†—7F–ærfÆÆ&6²—2vÆ¶W"Ö6ÆV&æ6R&F—W2ÂæB—Bv÷VÆBFöÖ–æFRF†Rç7vW# ¦ÖV7W&VBöffÆ–æRÂ—BÖ÷fW2ö÷&FVç6—6g&öÒãc6†&RFòã“’v†–ÆR&V6÷&FVBv–GF‚Ö÷fW0¦G&–föÆ—VÕ÷&WVç6g&öÒãbFòã2âvF†R&—F†ÖWF–2GW&ç2öâ—2&V6÷&FVBÂæ÷Bf–ÆÆVBà ¢¢¥&W÷'FVBæBæ÷BvFVB¢¢ÂöâF†R"ÔÓ7Æ—B(	B&"FöF’v÷VÆBV—F†W"f–ÂF†R'V–ÆB÷fW §Vç&W6V&6†VBFF÷"&RÖWBv—F‚â–çfVçF–öââv†B•2vFVB—2F†BF†R–ç7G'VÖVçBv÷&·3¢WfW'§6Æ÷BFVÇB—2GG&–'WFVBFò7V6–W2Â÷fW"÷VÆFVB7v&Bà ¢¢¥v‡’F†RF–Âv2æ÷B&W—&VB–âF†R6ÖR'Vââ¢¢³C‚w2–6¶W"¶VW2'Vææ–ær66÷VçG2Âv†–6‚—0¦f–æRf÷"vööBFVÇBöæ6RBÆöBæBw&öærf÷"7v&B&RÖFVÇBg&öÒv÷&ÆBÖæ6†÷&VBÆGF–6Röà¦WfW'’&RÖ6VçG&S¢7FFRÖ¶W26Æ÷Bw27V6–W2FWVæBöâF†R÷&FW"6Æ÷G2vW&Rf—6—FVB–âÂ6òF†P§ÆçBB–÷W"fVWBv÷VÆB6†ævR7V6–W22–÷RvÆ¶VBWFò—BâF†R7v&BæVVG27FFVÆW70¦WV—fÆVçB(	BÆ÷rÖF—67&Wæ7’76–væÖVçB¶W–VBöâF†R6Æ÷Bw2÷vâ6ö÷&F–æFW2(	BæBF†B—2§Æ6VÖVçB6†ævRv†÷6Rf–ÇW&RÖöFR—2F–vöæÂ7G&—–ær'’7V6–W2Âv†–6‚†2Fò&RÆöö¶VB@§&F†W"F†â6÷VçFVBâ³C’†"’6'&–W2F†Rf÷&ÒæBF†R6†V6²à ¢¢¥VçfW&–f–VBÂæB7FFVB&F†W"F†â6¶—VC¢¢¢F†RFW6·F÷†Æböb6Öö¶U÷&VæFW&W"æÖ§6v2æ÷@§'Vâ(	Bã2Ö–çWFW2v–ç7BF†—2'VææW"w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâFööÇ2ö6†V6²ç6†ÂF†P¦Öö&–ÆR6Öö¶Rv–ç7BF†RV&Æ—6†VBÖ—'&÷"æBFööÇ2öÖV7W&U÷7v&EöG&ræÖ§6&Rv†BF†—2&W7G0¦öââF†RGvòVF—Bf–wW&W2&RFF6WB×v–FRæBf–Ww÷'BÖ–æFWVæFVçC²F†R6Öö¶Rw2F–Âf–wW&R—0§F†Rg&ÖRF†RvFR7FööB–âÂæB—G2æ÷FRæ÷r6—26ò–â2Öç’v÷&G2à ¢22f—†VB##bÓ‚Ób(	BF†R7–6Ö÷&R—27FæF–ærÂæBF†RFVç6—G’—Bv27W÷6VFÇ’7F'fVBöbv2æWfW"F†RfVÇ@ ¢¢¤³C‚¢¢ÂæB—B&VgWFVBF†R&VÖ—6R—Bv2÷VæVBöââF†R&6VÂ6–BWfW'’7V6–W2—2ÆçFVB@¦F†—&BFòGvòF†—&G2öbF†RFVç6—G’—G2÷vâ&V6÷&B6'&–W2â¢¤&÷F‚&W—'2—BæÖVB&P§Væ'V–ÆF&ÆRÂæBF†R&—F†ÖWF–2—2–âF†R&V6÷&B&F†W"F†â–ââ÷–æ–öã¢¢  ¢Ò¢¥&W66Æ–ærF†RvV–v‡G26òWfW'’&VÆ—6VBFVç6—G’ÆæG2–ç6–FR—G2&V6÷&FVB&æB—2à¢Vç6öÇf&ÆR7—7FVÒ–âGvòöbF†Rf÷W"6öÖ×Væ—F–W2â¢¢&VÆ—6VBFVç6—F–W27VÒFòF†R7FæBFVç6—G’À¢6òF†R&V6÷&FVBfÆö÷'2†fRFòf—BVæFW"F†R7FæB6V–Æ–ærâ¢¦vWE÷vööG6¢fÆö÷'27VÒFòö†¢v–ç7B6V–Æ–æröbƒBâvÆÆW'–¢sRv–ç7Bc"¢¢–âF†R6÷WF‚F—f—6–öâ&VÇBâæò76–væÖVçBö`¢vV–v‡G2W†—7G2à¢Ò¢¤FW&—f–ærW$†g&öÒF†RÖ—‚7VÒ6öçG&F–7G2F†RF÷76–W"&÷rF†RvV–v‡G2&R&VB÷WBöb¢¢(	@¢vÆÆW'’B¢£bG&VW2ö†¢¢v–ç7B*r¤ôäRRw2¢&6æ÷’3(	3ƒG&VW2ö†"¢ÂvWE÷vööG6B¢£S2¢ ¢v–ç7B*r¤ôäRbw2¢&÷fW&ÆÂ6æ÷’F&vWBS(	3G&VW2ö†"¢à ¢¢¥6òF†R&V6÷&Bw2FVç6—G’6öÇVÖâ—2æ÷B7FæBFVç6—G’¢¢Âv†–6‚¤ôäRb7FFW2–â—G2÷vâv÷&G0¦æBv†–6‚F†RÖ—‚6öÖÖVçB–âG&VW2æ§6†26–BÆÂÆöærâF†Rf–ÆRv2&–v‡BæBF†R&6VÂF†@¦F÷V'FVB—Bv2w&öærâæ÷F†–ær&÷WBvV–v‡BÂ&æBÂFVç6—G’÷"FW'GW&R6†ævVBà ¢¢¥v†Bv27GVÆÇ’'&ö¶Vâ—2F†RE$râ¢¢WfW'’7FVÒv2â–æFWVæFVçBG&röâ—G26öÖ×Væ—G’w0§6†&W2ÂæBâ–æFWVæFVçBG&rÆ÷6W2F†R&&RVæBöbF—7G&–'WF–öâ(	BF†R7–6Ö÷&R—2ã“€¦W‡V7FVB÷fW"RvÆÆW'’7FV×2æBF†R6VVFVB6‡VffÆRFVÇBæöæRÂW&ÖæVçFÇ’Â&V6W6RF†R66VæP¦—26VVFVBâF†RG&r—2æ÷r6÷'&V7FVBv–ç7Bv†B—B÷vW3¢&÷÷'F–öæÂFò6†&R9rG&vâ(‰ §Æ6VFÂæB7V6–W2Ç&VG’÷vVBv†öÆR7FVÒF¶W2F†RæW‡BöæR÷WG&–v‡Bâæ÷F†–ær÷fW'6†ö÷G0¦'’7FVÒæBæ÷F†–ær÷vVB7FVÒvWG2æöæRÂ&÷F‚'’6öç7G'V7F–öã²7G&W72×FW7FVB÷fW"¢£3RÃƒƒ¢ ¢†Ö—‚Â7FæB6—¦RÂ6VVB’66W2(	Bv÷'7B÷fW'6†ö÷Bã“’Âv÷'7B6†÷'FfÆÂã#Â¦W&òÆ÷76W2à ¢¢¤ÖV7W&VBöâF†RV&Æ—6†VBÖ—'&÷"Â–FVçF–6ÂB3“9ssƒæB#ƒ9sƒâ¢¢7–6Ö÷&W27FæF–æp¢¢£(i""¢¢âvV–v‡FVBVçG&–W27FæF–æræ÷v†W&R¢£(i"¢¢Â÷WBöb#bâv÷'7B÷fW'6†ö÷BãS7FV×2À§v÷'7B6†÷'FfÆÂãƒbâ7FV×2c2(i"s‚æBF†–6¶WB7FööÇ2#B(i"#3¢FEG&VVG&w2G&VRw2÷và§6†Rg&öÒF†R6ÖR7G&VÒæBF¶W2F–ffW&VçBçVÖ&W"öbG&w2W"7V6–W2Â6òF†Rv†öÆRvööB—0§&RÖFVÇBâæ÷F†–ærF†B6WG2†÷rÖç’7FV×2†V7F&R†öÆG2Ö÷fVBà ¢¢¤æBF†R6Vç7W2³Cr6–Bv2Ö—76–æræ÷rW†—7G2â¢¢ÖV7W&U÷ÆçF–æu÷&V6‚ç–&÷fW2&V6÷&B6à¦&R¦6†÷6Vâ£²7FG2æG&w6æBGvò6Öö¶R76W'F–öç2&÷fR—B—2¦G&vâ¢â&VæFW&W"F†BvVçB&6°§FòF†R–æFWVæFVçBG&rf–Ç2&÷F‚à ¢¢¥VçfW&–f–VBÂæB7FFVB&F†W"F†â6¶—VC¢¢¢F†RFW6·F÷†Æböb6Öö¶U÷&VæFW&W"æÖ§6v2æ÷@§'Vâ(	Bã2Ö–çWFW2v–ç7BF†—2'VææW"w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâFööÇ2ö6†V6²ç6†æBF†P¦Öö&–ÆR6Öö¶Rv–ç7BF†RV&Æ—6†VBÖ—'&÷"&Rv†BF†—2&W7G2öâÂÇW2F—&V7B&÷F‚×f–Ww÷'@¦6Vç7W2&ö&RöbF†RV&Æ—6†VB'V–ÆBÂv†–6‚—2v†W&RF†RFW6·F÷çVÖ&W'2&÷fR6öÖRg&öÒà ¢22f÷VæB##bÓ‚Ób(	BF†RÖW&–6â7–6Ö÷&R—2æ÷B–âF†—2F÷vâÂæBF†R&&²—Bv2v—fVâ&÷fW2—@ ¢¢¤³Crâ¢¢F†R&6VÂv26Æ–ÖVB4TTâæBFVÆ—fW&VBTå4TTâÂæBF†R–çfW'6–öâ—2F†Rf–æF–ærâF†P¦&6†WG—R—2'V–ÇB(	B5T4”U2çÆFçW5öö66–FVçFÆ—6Â—G2÷vâ&öÆRÂFW"ÂF–ÖWFW"&æBÂVf`¦6÷VçBÂæBGvò×FöæR&&²v†÷6RÆRWW"Æ–Ö'2&RF†RöæRF†–ær£U÷&—fW&&æµ÷F–Ö&W&6–ævÆW0§F†R7V6–W2÷WBf÷"â67&VVç6†÷Bg&öÒç’7FæB–âF†—2F÷vâ—2Væ6†ævVBÂ&V6W6R¢¦æò7–6Ö÷&P¦—2ÆçFVBç—v†W&R–âF†R66VæRâ¢  ¢¢¤ÖV7W&VB–âF†RV&Æ—6†VB'V–ÆBB#ƒ9sƒ¢¢Â÷WBöb’çG&VW2ç7FG2ç7V6–W6¢¢£c2vööG§7FV×2ÂRöbF†VÒ–âF†RvÆÆW'’Â7–6Ö÷&W2â¢¢F†RÖ—‚vV–v‡B—2"öbF†RvÆÆW'’w2bÂ6òã“€§vW&RW‡V7FVBæBF†R6VVFVBG&r&WGW&æVBæöæR(	B2ãRRÆ–¶VÇ’öâ–æFWVæFVçBG&w2âF‡&VR÷F†W §7V6–W27FæB2öæR7FVÒV6‚Â6òF†—2—2F†RF–ÂöbF—7G&–'WF–öâæBæ÷B7V6–Â66S¢£RÖG&r6×ÆR6ææ÷B6''’#bÖVçG'’V6öÆöw’à ¢¢¥F†R'VÆRVæFW&æVF‚—BÂæBæòvFR†2WfW"Æöö¶VBB—Bâ¢¢F†RvÆÆW'’Ö—‚7V×2Fò¢£b¢ ¦v–ç7B7FæBFVç6—G’öb¢¥³3BÂc%Òö†¢¢6÷WF‚öbF†R&—fW"æB¢¥³SÂs…Òö†¢¢æ÷'F‚Â6òWfW'¦Æ—FW&Â—2vÆ¶VB2§6†&R£¢¢¦V6‚7V6–W2—2ÆçFVBB#ž(	3crRöbF†RFVç6—G’w&—GFVâ&W6–FP¦—Bâ¢¢³CbÖFRF†RÆ—FW&ÂF†RçVÖ&W"F†BÆçG2F†R7FVÒæBF†R&V6÷&Bw2&æBF†R6öç7G&–çBöà§F†BÆ—FW&Â(	BæBF†RÆ—FW&Â—2æ÷BF†RFVç6—G’âF†R7–6Ö÷&Rw2"6—G2BF†RÖ–Gö–çBöb—G0§&V6÷&FVB³Â5Òö†æB76W3²F†R66VæRÆçG2—BB¢£ãSž(	3ã3Bö†¢¢âF†B—2$ôDÔ¢¤³C‚¢¢À¦g&ÖR×v–FRÂ÷VæVB&F†W"F†â7F'FVBà ¢¢¥v†BF†—26÷'&V7G2â¢¢³CR†#’æB6†ævVÆör¢§c3’¢¢&÷F‚6’†æFgVÂöb7FV×2ÆöærF†R&—fW ¦&Ræ÷r7–6Ö÷&W2âF†W’&Ræ÷BâF†R7V6–W2&V6ÖR§6VÆV7F&ÆR¢(	Bv†–6‚—2v†BF†B&6VÂw2vFP¦ÖV7W&W2Â6÷'&V7FÇ’(	BæB6VÆV7F&ÆR—2æ÷BG&vââFööÇ2öÖV7W&U÷ÆçF–æu÷&V6‚ç–&æ·2v†WF†W ¦&V6÷&B6â&R¢¦6†÷6Vâ¢£²æ÷F†–ær&æ·2v†WF†W"—B—2¢¦G&vâ¢¢ÂæBF†RG&vâ6Vç7W2Æ—fW2öæÇ¦–ç6–FR'Vææ–ær&VæFW&W"â³C‚w26†V†Æb—2F†B6Vç7W226Öö¶R76W'F–öã²—Bf–Ç2&VBöà§F†R7–6Ö÷&RFöF’à ¢¢¥v†BF–B6†—â¢¢Fö72ôÄ”$U%D”U2æÖF¢¤Ãb¢¢—2&W6öÇfVB(	Bæò7V6–W2–âF†—266VæRvV'0¦æ÷F†W"w2&6†WG—Ræ÷r(	BæBF†RGvò–çfVçFVB&&²FöæW2&R¢¤Ã‚¢¢v—F‚F†V—"&÷VæG27FFVBà¦G&VW2æ§6v–æVBöæR÷F–öæÂf–VÆBÂ&&µWW&ÂöâF†RWW"&öÆRæBF†RÆ–Ö'3²WfW'’÷F†W §7V6–W2öÖ—G2—BæB—2'—FRÖ–FVçF–6ÂâF†RGvò×FöæR&&²v2¢§&÷fVBFòG&r¢¢v—F‚F†RvV–v‡@§FV×÷&&–Ç’BC‡ÆRG'Væ·2VæÖ—7F¶&ÆRBsÒv–ç7BF†RæV"Ö&Æ6²&öÆW2&W6–FRF†VÒ’À¦æBF†BW‡W&–ÖVçBv2&WfW'FVB&Vf÷&RF†R6öÖÖ—Bà ¢¢¥VçfW&–f–VBÂæB7FFVB&F†W"F†â6¶—VC¢¢¢F†RFW6·F÷†Æböb6Öö¶U÷&VæFW&W"æÖ§6v2æ÷@§'Vâ(	Bã2Ö–çWFW2v–ç7BF†—2'VææW"w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâFööÇ2ö6†V6²ç6†ÂF†RvFRw0¦÷vâ6VÆb×FW7BæBF†RÖö&–ÆR6Öö¶Rv–ç7BF†RV&Æ—6†VBÖ—'&÷"&Rv†BF†—2&W7G2öâà ¢22f—†VB##bÓ‚Ób(	BF†Rw&—GFVâvV–v‡BÆçG2F†R7FVÒÂæBF†RF–G’ÇFW&æF—fRv2&VgWFVB'’F†R6†RöbF†RFF6W@ ¢¢¤³Cb¢¢ÂF†RVW7F–öâ³CR†#’ÖV7W&VBæB&VgW6VBFòç7vW"âF†RÆ—FW&Â–â4ôÔÕTä•D”U6—2æ÷p§F†RçVÖ&W"–6²‚–vÆ·3²F†R&V6÷&Bw2&æB—2F†R4ôå5E$”åBöâ—BâröbF†R#bÖ—‚VçG&–W0¦6†ævRfÇVRæBÆÂ#b6†ævR7FæF–ærà ¢¢¥&÷WFR26ææ÷B&R'V–ÇBÂæBF†B—2F†Rf–æF–ærâ¢¢³CbæÖVBF‡&VR&÷WFW2æB6ÆÆVB&÷WFR2(	@¦¶W’FVç6—G–'’‡¦öæRÂ7V6–W2’ÂV6‚6öÖ×Væ—G’&VF–ærF†R&æBg&öÒF†R¦öæR—G2÷vâF÷76–W& ¦6—FW2(	B'F†RöæRF†B6—2v†BF†Rf–ÆRw26öÖÖVçB6Æ–×2"âvWE÷vööG66—FW2¢¥¤ôäRf¢¢æ@¦ÖW6–5÷ö6¶WF6—FW2¢¥¤ôäRf"¢¢æB¢¦&÷F‚&W6öÇfRFòF†R6–ævÆR&V6÷&B£eöFVç6Uöf÷&W7F¢¢À§v†÷6RVÆÒ&æB³CÂƒÖ—2F†R7v×F†–6¶WBw2&VF–ærâ¦öæRÖ¶W–VBÂF†RVÆÒ—2c–â&÷F€¦6öÖ×Væ—F–W2æBF†R¢£"¢¢F†BÖ¶W2—B–æ6–FVçFÂ–âF†Rf—&R×&÷FV7FVBö6¶WB†2æ÷v†W&R–à¦FFöFòÆ—fR(	B&÷WFR2FW7G&÷—2F†RW†7B&VF–ær—Bv2&÷÷6VBFò&W7F÷&Râ&÷WFRF—66&G0¦—B'’—G2÷vâFÖ—76–öââ&÷WFR"—2F†W&Vf÷&Ræ÷B&VfW&Væ6R&WGvVVâGvòV6öÆöv–W3²—B—2F†P¦öæÇ’öæRöbF†RF‡&VRF†B6âW‡&W72F†Rf–ÆRÂæBF†R&V6öâ—2F†RFF6WBw26†Rà ¢¢¥F†RÖV7W&VÖVçBF†BÖFR—B6fS¢#2–ç6–FRÂ2&VÆ÷rÂ&÷fRâ¢¢WfW'’Æ—FW&Âv266÷&V@¦v–ç7BF†R&æBöbF†R¦öæR—G2÷vâ6öÖ×Væ—G’6—FW2â¢¤æ÷BöæR†æBvV–v‡B—2â–æfÆF–öâ¢¢(	@§v†W&RF†Rf–ÆRFW'G2g&öÒ&V6÷&B—BF†–ç27V6–W2ÂæWfW"6Æ–×2Ö÷&RöböæRF†âF†RWf–FVæ6P¦6'&–W2âF†B—2v†BÆ–6Vç6VB†æF–ærF†R†æBvV–v‡G2F†R66VæRÂæB—B—2çVÖ&W"æö&öG’†@§F¶Vã¢³CR†#’6ö×&VBF†RÆ—FW&Âv–ç7BF†Rf–wW&RF†B÷fW'&öFR—BÂæWfW"v–ç7BF†R&æ@¦—G2÷vâ6öÖ×Væ—G’6—FW2à ¢¢¥v†BÖ÷fVB–âF†Rg&ÖRÂæBv†BF–Bæ÷Bâ¢¢W$†(	BF†R7FæBFVç6—G’F†B6WG2†÷rÖç§7FV×2vööB6'&–W2(	Bv2æWfW"÷fW'&–FFVâæB—2VçF÷V6†VBÂ6ò¢¦æò7FVÒ6÷VçB6†ævVB¢£¢æòG&VP¦V&VBÂfæ—6†VB÷"Ö÷fVBw&÷VæBâ7V6–W26†&R6†ævVB–âF‡&VRöbF†Rf÷W"6öÖ×Væ—F–W2âF†P§6–ÇfW"ÖÆRfÆÇ2g&öÒ¢£#’ãBRFòã’R¢¢öbF†RvFW"w2VFvRæBF†R&Æ6²v–ÆÆ÷r&—6W2g&öÐ¢¢£SãRFòc"ãrR¢¢Âv†–6‚—2F†RVFvRÖ—‚w2÷vâæ÷FR‚¢&vöW2Fòv–ÆÆ÷r"¢’f–æÆÇ’7W'f—f–ærF†P¦ÆöBâF†RVÆÒ&—6W2g&öÒ¢£#RãbRFò3’ã"R¢¢öbF†R7v×F†–6¶WBæBfÆÇ2g&öÒ¢£#"ãBRFð£"ã"R¢¢öbF†RÖW6–2ö6¶WB(	BGvò&VF–æw2öbF†RF÷76–W"v†W&RF†W&R†B&VVâöæRà ¢¢¥F†RF‡&VRFW'GW&W2&RFV6Æ&VBÂæ÷B'6÷&&VBâ¢¢vÆÆW'’æÖ—‚ç6Æ—…ö×–vFÆö–FW6ƒ‚v–ç7@§£R³Â#UÖ’ÂvÆÆW'’æVFvTÖ—‚æ6W%÷666†&–çVÖƒ‚v–ç7B³RÂ3UÖ’æ@¦ÖW6–5÷ö6¶WBæÖ—‚çVÆ×W5öÖW&–6æƒ"v–ç7B£b³CÂƒÖ’6—B÷WG6–FRF†V—"6—FVB&æG2Â&P¦V6‚w&—GFVâF÷vâ–âF†V—"6öÖ×Væ—G’w2æWrFW'GW&W6f–VÆBv—F‚F†R&V6öâÂæB&P¦Fö72ôÄ”$U%D”U2æÖF¢¤Ãr¢¢âF†R&VæFW&W"&VgW6W2FòÆöBâVæFV6Æ&VBöæR(	BæB&VgW6W2¢¢§7FÆR¢¢öæRFöó¢FW'GW&R&W—&VBv—F†÷WBG&÷–ær—G2æ÷FRf–Ç2Â&V6W6RFV6Æ&F–öâF†@¦÷WFÆ—fW2—G2fVÇB—2†÷rvFR7F÷2ÖVæ–ærç—F†–ærà ¢¢¥Gvò÷VâVW7F–öç26Æ÷6VBv—F†÷WB&V–ærç7vW&VBâ¢¢³CR†#’w2&W6–GVR(	Bg&†–çW5öæ–w&B@¦v–ç7BÖ–Gö–çBöbR(	BæVVFVBæòW‡ÆæF–öâöæ6RF†R'VÆR7F÷VB&V–ær'F†RÖ–Gö–çB#¢F†@§v2&VwVÆ&—G’‚öb#RVçG&–W2†VæVBFòföÆÆ÷rÂæBB—2–ç6–FR£bw2³Â#Öâæ@¦&–FvUöö¶w2ÖW&vVB¢¥¤ôäRf2²¤ôäRr¢¢Âv†–6‚³CR†#’W66ÆFVBFòF†R÷væW"ÂFöW2æ÷BæVV@¦FV6–F–æs¢v—F‚F†R&V6÷&B6öç7G&–çB&F†W"F†â6÷W&6RF†RVW7F–öâ—2æ÷B§v†–6‚&æB¢'W@¢¦—2F†RvV–v‡BFÖ—76–&ÆR–âöæRöbF†VÒ¢ÂæBÆÂf÷W"ö²vV–v‡G2&Rà ¢¢¥F†Rg&ÖRv2ÖV7W&VB&Vf÷&RæBgFW"öâF†R6ÖRF‡&VR7FF–öç2¢¢ÂæBF†R6öçG&öÂ—2F†P¦f–æF–æs¢&—&–U÷vW7F(	BF†Rw&÷VæBæG&V26ÆÇ2¢&â÷Vâ&—&–RÂVçF—&VÇ’g&VRg&öÒF–Ö&W""¢(	@¦FöW2æ÷BÖ÷fR††–v‚×72$Õ2f"#ãs’(i"#ãs‚ÂæV"’ãc(i"’ãc’Âv†–ÆR&—fW%ö&æ¶Â7FæF–æp¦–âF†R6öÖ×Væ—G’F†B6†ævVBÖ÷7BÂÖ÷fW2†&FW7BæB–âF†RF—&V7F–öâF†RvV–v‡G2&VF–7B†f £#ãƒR(i"bãsBÂæV"Rã“‚(i"bãcB’â5$•D”24„õE2ô¶&Vf÷&RæBgFW"ÂæBF†RgFW"×6WB&W&öGV6V@¦7&÷72Gvò&ö6W76W2Â6òF†RFVÇF2&RF†R6†ævR&F†W"F†âF†R&7FW&—6W"âöæR7v–ær—2ÆVg@§VæW‡Æ–æVBæB—2&V6÷&FVB–âF†R$ôDÔ&÷‚&F†W"F†â'W&–VC¢&—&–U÷vW7Fw2†÷&—¦öâ×F–Ö&W ¦g&7F–öâfÆÇ2ãs#b(i"ãS3‚öâFW6·F÷v†–ÆR&&VÇ’Ö÷f–æröâÖö&–ÆRà ¢¢¥VçfW&–f–VBÂæB7FFVB&F†W"F†â6¶—VC¢¢¢F†RFW6·F÷†Æböb6Öö¶U÷&VæFW&W"æÖ§6v2æ÷@§'Vâ(	Bã2Ö–çWFW2v–ç7BF†—2'VææW"w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâFööÇ2ö6†V6²ç6†ÂF†P¦Öö&–ÆR6Öö¶Rv–ç7BF†RV&Æ—6†VBÖ—'&÷"ÂF†RvFRw2÷vâ6VÆb×FW7BæBF†R7&—F–26†÷G2&RF†P§fW&–f–6F–öâF†Bv2FöæRà ¢22f—†VB##bÓ‚Ób(	BF†R7–6Ö÷&R—2ÆçFVBÂæBF†RvV–v‡Bw&—GFVâ&W6–FRWfW'’7V6–W2–âF†RG&VRÖ—†W2—2æ÷BF†RvV–v‡BF†BÆçG2—@ ¢¢¤³CR†#’¢¢ÂF†R6W&&ÆRF†—&Böb³CR†"’â²wÆFçW5öö66–FVçFÆ—2rÂ%Ö—2–âF†RvÆÆW'’Ö—‚À§6òFööÇ2öÖV7W&U÷ÆçF–æu÷&V6‚ç–w2&÷WFVBÖ&6†WG—VBÖæB×6VÆV7FVBÖ'’Öæ÷F†–ær&æ²—2¢£ö`£#¢¢v†W&R—Bv2ÂæBF†RfÆööGÆ–âvööB†öÆG2F†RFVâ7V6–W2—G2÷vâ&V6÷&B†öÆG2âF†P¤ÖW&–6â7–6Ö÷&R(	B¢'&&RÂB—G2æ÷'F†W&âVFvS²v†—FRÖ÷GFÆVB&&²fÆ6†–æröâF†RWW"Æ–Ö'2" ®(	B—2–âF†Rg&ÖRf÷"F†Rf—'7BF–ÖRÂBÆ—GFÆRVæFW""RöbF†B6öÖ×Væ—G’w27FV×2à ¢¢¥F†R&W67&–&VBvV–v‡Bv2w&öærGv–6RÂæBF†R6V6öæBöæR—2F†Rf–æF–ærâ¢¢³CR†"’æ@¦Fö72ôÄ”$U%D”U2æÖFÃB&÷F‚w&÷FRF†RVçG'’÷WB2²wÆFçW5öö66–FVçFÆ—2rÂÖâ¢£—2F†P¦&÷GFöÒöbF†R&V6÷&FVB³Â5Ò&æBæBF†Rf–ÆRw2'VÆR—2—G2Ö–Gö–çB¢¢(	B‚öbF†R#R7FæF–æp¦VçG&–W26—BW†7FÇ’öâF†V—"&æBw2Ö–Gö–çB÷"—G2fÆö÷"(	B6òF†RçVÖ&W"—2¢£"¢¢âæB—Bv÷VÆ@¦æ÷B†fRÖGFW&VBv†Bv2w&—GFVâÂ&V6W6R¢§F†RÆ—FW&Â&W6–FR7V6–W2–B—2fÆÆ&6²¢£ ¦Ö—†W6—2&V'V–ÇBBÆöB2&V6÷&G2æFVç6—G•¶–EÒóòfÆÆ&6¶ÂæB&V6÷&G2æFVç6—G–—2F†P¦Ö–Gö–çBöbF†R&æB–âF†Rd•%5BD”Ô$U%õ¤ôäU6VçG'’æÖ–ærF†R7V6–W2â¢£röbF†R#bVçG&–W0¦&Rw&—GFVâFòöæRçVÖ&W"æBÆ6R7FV×2Bæ÷F†W"â¢  ¢¢¥F‡&VRöbF†R6WfVçFVVâv÷VÆB&R&VB2âW'&÷"g&öÒF†Rg&ÖRâ¢¢VÆ×W5öÖW&–6æ—2w&—GFVà¢¢£c¢¢–âF†R7v×F†–6¶WBæB¢£"¢¢–âF†RÖW6–2ö6¶WB(	BGvòF–ffW&VçB&VF–æw2öbF†RF÷76–W ®(	BæB—2ÆçFVBB¢£#R¢¢–â&÷F‚Â£Rw2&æB&V–ærF†Rf—'7BöæRF†RÆöFW"ÖVWG2à¦6W%÷666†&–çVÖ—27WBFò¢£‚¢¢BF†RvFW"w2VFvRÂv†W&RF†Rf–ÆR6—2–â2Öç’v÷&G2F†@§F†RÖ—‚¢&vöW2Fòv–ÆÆ÷r"¢ÂæB—2ÆçFVBF†W&RB¢£#R¢£¢æV&Ç’F†—&BöbF†RVFvR–ç7FVBö`¦æ–çF‚öb—BâÆÂf—fR7V6–W2w&—GFVâ–çFòÖ÷&RF†âöæRÆ—7BF¶R£Rw2&æBWfW'—v†W&R(	BF†P¦f—'7B×¦öæR×v–ç2'VÆR³CR†’f÷VæBFV6–F–ærF†R7V2ÂöæRf–VÆBÆöærà ¢¢¤æ÷F†–ærv26÷'&V7FVBÂFVÆ–&W&FVÇ’â¢¢v†–6‚çVÖ&W"÷Vv‡BFòv–â—26Æ–Ò&÷WBF†RV6öÆöw’À¦æBç7vW&–ær—BÖ÷fW27FV×2–âF‡&VRöbF†Rf÷W"6öÖ×Væ—F–W2Böæ6RâF†B—2¢¤³Cb¢¢Âv—F‚F†P§F‡&VR&÷WFW2w&—GFVâ÷WBæBF†Rg&ÖR—B†2Fò&÷fR—G6VÆb–ââv†B6†ævVBFöF’—2F†BF†P¦F—fW&vVæ6R—2&æ¶VB–â—'2(	BÆ—FW&ÂÂ'Vææ–ærÂæBF†R¦öæRF†R'Vææ–æröæR6ÖRg&öÒÂW†7@¦&÷F‚v—2(	BæBF†RFW&—fF–öâ—266ææVB÷WBöbF†R&VæFW&W"Â6òG&VW2æ§6F†B7F÷0¦÷fW'&–F–ærF†RÆ—FW&Â¢§&—6W2¢¢&F†W"F†â6ö×&–ærçVÖ&W"v—F‚—G6VÆbâÖ—‚VçG'’vV–v‡FV@¢¢£¢¢æ÷rf–Ç2Föó¢—Bv÷VÆBÆöö²ÆçFVBÂ&RVç–6¶&ÆRÂæB&R–çf—6–&ÆRFòF†R76W'F–öâF†@¦6÷VçG27V6–W2æòÖ—‚†öÆG2à ¢¢¤æBF†R7–6Ö÷&R—2G&vâ2âVÆÒg&öÒF†R&&²÷WGv&G2â¢¢—B—2F†R¢¦öæÇ’¢¢Æ6VB7V6–W0§v—F‚æò5T4”U6&6†WG—Röb—G2÷vâÂ6ò5T4”U5·7æ–EÒóò5T4”U2çVÆ×W5öÖW&–6æv—fW2—@§F†RVÆÒw2&öÆRÂFW"ÂVfb6÷VçBæB¢¦&&²6öÆ÷W"¢¢v†–ÆR—G2†V–v‡BÂ7&÷vâæBföÆ–vR6öÖP¦g&öÒ—G2&V6÷&BâF†RöæRF†–ærF†B&V6÷&B6–ævÆW2F†R7V6–W2÷WBf÷"—2¢'v†—FRÖ÷GFÆVB&&°¦fÆ6†–æröâF†RWW"Æ–Ö'2"¢(	B6òF†RG&VR—2–âF†R66VæRæB6ææ÷B&R–FVçF–f–VB–â—Bâæð¦fÆ÷&&V6÷&B6'&–W2&&²6öÆ÷W"BÆÂÂ6ò†W‚v÷VÆB†fR&VVâ6öç7–7V÷W2–çfVçF–öâöà¦æö&öG’w2WF†÷&—G’â&V6÷&FVB2Fö72ôÄ”$U%D”U2æÖF¢¤Ãb¢¢æB&æ¶VBW†7FÇ’Â&÷F‚v—3¢§6V6öæB7V6–W2fÆÆ–ær–çFòF†R6ÖR†öÆRf–Ç2F†RvFRÂæBv—f–ærF†R7–6Ö÷&R—G2÷và¦&6†WG—R†2FòVâÖ&æ²—B–âF†R6ÖR6öÖÖ—Bà ¢¢¥v†B—2VçfW&–f–VBÂ7FFVBÆ–æÇ’â¢¢FööÇ2ö6†V6²ç6†—2w&VVâæB4Ôô´Uõd”Uuõ%CÖÖö&–ÆRæöFP§FööÇ2÷6Öö¶U÷&VæFW&W"æÖ§2Ò×V&Æ—6†VF—2w&VVã²¢§F†RFW6·F÷†Æbv2æ÷B'Vâ¢¢(	Bã2Ö–çWFW0¦v–ç7BF†—2'VææW"w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâF†R7–6Ö÷&R†2æ÷B&VVâÆöö¶VBB–â§&VæFW&VBg&ÖS¢—B—2VæFW""RöböæR6öÖ×Væ—G’w27FV×2æBæò7FF–öâv26†÷6VâFò7FæBæV ¦öæRà ¢22f—†VB##bÓ‚Ób(	BF†R&77vööB—2–âfÆ÷vW"ÂæBF†R&W—"&W67&–&VBf÷"—BG&w2f÷W"—†VÇ0 ¢¢¤³CR†2’¢¢ÂæB—B—2F†R6V6öæBöbÃ2w2F‡&VR&W—'2âG&VW2æ§6†2†VBF‚æ÷s¢F†P¢¢¤ÖW&–6â&77vööB–â&ÆööÒ¢¢æBF†R¢¦—&öçvööB–âg'V—B¢¢&RG&vâg&öÒF†V—"÷vâ&V6÷&G2(	@¦6öÆ÷W"Â6—¦RæB†V–v‡BöâF†RÆçBÆÂ2w&—GFVâ(	BæBFööÇ2öÖV7W&UöfÆ÷&÷&V6‚ç–&æ·0¢¢¦öæR¢¢†VFÆW72fÆ÷vW"v†W&R—B&æ¶VBF‡&VRâF†R&VÖ–æ–æröæR—2F†Rw&RÂv†÷6Rf–æUöG&V ¦f÷&Òæò&VFW"–×ÆVÖVçG3²—Bv2æWfW"F†—2&W—"w2à ¢¢¥F†R&W67&–&VB&W—"—2öæR7FW6†÷'BÂæBF†R&—F†ÖWF–26—26ò&F†W"F†â§VFvVÖVçBâ¢ ¤†æF–ærG&VW2æ§6fÆ÷&æ§6w2„TEôôeõ4„VfW&&F–ÒG&w26ÇW7FW%÷FW&Ö–æÆw2¢£FòB¢ ¦†VG2(	B6÷VçB6Æ–'&FVBf÷"f÷&"Âv†W&RF†Rv†öÆRÆçB•2öæRfÆ÷vW&–ær66RâF†R&V6÷&Bw0¦÷vâ6—¦UöÖ—2ãn(	3ã"Òf÷"ôäR–æfÆ÷&W66Væ6S²BF†R#2Ò6ÆçB&ævRöbæV–v†&÷W&–ær7&÷và¢ƒÒWÂ#Ò÷WB’ã’Ò7V'FVæG2ã3’&BÂv†–6‚—2¢£2ã2‚¢¢BF†—2f–ÆRw2ƒ32‚÷&BâF†P¦7&÷vâ6''––ær—B—2(	3bÒ7&÷72Â÷"¢£Sƒ‚¢¢BF†R6ÖR&ævRâf÷W"2×‚7V6·2öâSƒ×€¦7&÷vâv÷VÆB†fR&æ¶VBfÇ6R72öâ³CBw2÷vâ76W'F–öâRâ6ò6—¦RÂ6öÆ÷W"æB†V–v‡Eög&6 ¦6öÖRg&öÒF†R&V6÷&BW†7FÇ’æBÕTÅD•Ä”4•E’—2¶W–VBFòF†R&V6÷&FVB7&÷vâv–GF‚(	BãbW"ÖWG&RÀ¦6Æ×VBn(	3#bÂ¢£#¢¢öâ&77vööBæB¢£’¢¢öââ—&öçvööB(	B&V6÷&FVB2Fö72ôÄ”$U%D”U2æÖF ¢¢¤ÃR¢¢ÂFVÆ–&W&FVÇ’W'&–ærÆ÷rà ¢¢¥F†RvööG’Æ–W"†2§VÇ’vFRf÷"F†Rf—'7BF–ÖRâ¢¢³CBÖV7W&VBF†B§VÇ’ç†VæöÆöw–v2&V@¦'’fÆ÷&æ§6ÆöæS²4ôåE$5BæÖB*sRãB'VÆRæ÷r'Vç2öâ&÷F‚&VFW'2ÂæB&V6÷&BF†B—0¦fVvWFF—fV÷"'VFF–ævæB7F–ÆÂ6'&–W2â–æfÆ÷&W66Væ6R—2&W÷'FVB&F†W"F†âG&vâà¦§VÇ’ç†VæöÆöw–&V6†W2¢£C‚öbSB¢¢&V6÷&G2v†W&R—B&V6†VB‚ÂæBF†Rv†öÆRVç&V6†V@§÷VÆF–öâfÆÇ2¢£33’(i"3¢¢öbÃƒƒ—'2à ¢¢¥F†RvFRv276W'F–æröæRöb—G2÷vâf7G2–ç7FVBöbÖV7W&–ær—Bâ¢¢E$TU5ô¥6w26†W6æ@¦G&w5ö†VG6vW&RF†RÆ—FW&Ç26WB‚–æBfÇ6V(	BF†RöæR—"öb&÷WF–ærf7G2–à¦ÖV7W&UöfÆ÷&÷&V6‚ç–æ÷B66ææVB÷WBöbF†R&VFW"â†VBF‚FFVBFòG&VW2æ§6v÷VÆB†fP¦vöæRöâ&V–ær&W÷'FVB2'6VçBf÷"2Æöær2æö&öG’VF—FVBF†Bf–ÆRÂæB&V6W6R76W'F–öâR—0¦W†7B–â&÷F‚F—&V7F–öç2—Bv÷VÆB†fR¢§76VBv†–ÆR6––ærF†R÷÷6—FRöbv†BF†R&VæFW&W ¦FöW2¢¢â&÷F‚&R66ææVBæ÷s²F&ÆRv—F‚æòVÖ—GFW"Â÷"âVÖ—GFW"v—F‚æòF&ÆRÂ&—6W3²æBÆÀ¦öb—B—2W†W&6—6VB'’Ò×6VÆb×FW7Fà ¢¢¥F†R†öæW7BÆ–Ö—BÂæB—B—2F†Rf–æF–ær67&VVç6†÷Bv÷VÆB÷F†W'v—6R&öGV6Râ¢¢&÷F‚fÆ÷vW&–æp§7V6–W2&R–âÖW6–5÷ö6¶WFÂv†–6‚—2¢£#öbS’7FV×2¢¢ÂæBÆÂ¢£B¢¢fÆ÷vW&–ær7FV×27Fæ@¦æ÷'F‚öbâ³sBÒâF†RæV&W7B6öÖÖ—GFVB66VæRæ6†÷"—2¢£#c’ãRÒ¢¢v’†6÷WF…÷vFW&’ÂBv†–6€¦öæR–æfÆ÷&W66Væ6R—2¢£ã#‚‚¢£²F†Rf'F†W7B—2g&öÕö&÷fVBSCrãRÒæBãB‚âf—6—F÷ §v†òvÆ·2æ÷'F‚ÖV7B7FæG2VæFW"fÆ÷vW&–ær&77vööC²f—6—F÷"v†ò7F—2v†W&RF†—2&ö¦V7@§÷6W2F†VÒæWfW"6VW2öæRâF†B—2v†W&RF†RÖW6–2ö6¶WBfÆÇ2öâF†RÖöFVÆÆVBw&÷VæBÂæ÷BfVÇ@¦–âF†R†VBF‚âFööÇ2öÖV7W&Uö†VE÷&V6‚æÖ§6&R×'Vç2F†RF&ÆRà ¢¢¤6÷7C¢¢¢¢£ƒr†VG2öâB7FV×2¢¢ÂÃC“böbF†RF–Ö&W"Æ–W"w22Ãƒ“G&–ævÆW2ÂæB¢¦æòæWp¦G&r6ÆÂ¢¢(	BF†R†VG2ÖW&vR–çFòF†R6ÖRf÷W"6‡Væ²'VffW'2BF†R6ÖRÖFW&–Âà ¢¢¥v†B—2VçfW&–f–VBÂ7FFVBÆ–æÇ’â¢¢FööÇ2ö6†V6²ç6†—2w&VVâæ@¦4Ôô´Uõd”Uuõ%CÖÖö&–ÆRæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§2Ò×V&Æ—6†VF—2w&VVâB¢£#’76VBò ¦f–ÆVBÂ¦W&òvRW'&÷'2¢£²¢§F†RFW6·F÷†Æbv2æ÷B'Vâ¢¢(	Bã2Ö–çWFW2v–ç7BF†—2'VææW"w0£ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâFööÇ2öÖV7W&Uö†VE÷&V6‚æÖ§6—2ÖV7W&VÖVçBæB—2FVÆ–&W&FVÇ¤äõB–âFööÇ2ö6†V6²ç6†¢—BG&—fW2'&÷w6W"æB6÷7G2ãC2v–ç7BvFRF†B†öÆG2—G6VÆbFð§ã“2–âF÷FÂâF†RfÆ÷vW"†2æ÷B&VVâÆöö¶VBB–â&VæFW&VBg&ÖRBF†R&ævRf—6—F÷"v÷VÆ@§6VR—Bg&öÒÂ&V6W6Ræò7FF–öâ7FæG2v—F†–â#c’ÒöböæRà ¢22ÖV7W&VB##bÓ‚Ób(	BF†R&W—"–W7FW&F’w2&6VÂ&W67&–&VBG&w2æ÷F†–ærÂæB&W6V&6†VBG&VR†2æWfW"&VVâ–âF†R66VæP ¢¢¤³CR†’¢¢ÂæB—BÖ÷fW2æò&V6÷&BÂæò&ÖWFW"æBæò&VæFW&W"f–ÆRâ³CBf÷VæBf÷W"&W6V&6†V@¦Æ¶W6†÷&RG&VW2†æFVBFòæò&VFW"æBw&÷FRF†R&W—"F÷vâ–âGvòÆ6W3¢¢&FB£…öÆ¶W6†÷&V §FòD”Ô$U%õ¤ôäU6"¢âÖV7W&VB&Vf÷&R7VæF–ær6Öö¶Röâ—BÂF†B&W—"G&w2¢§¦W&ò¢¢7FV×2à ¢¢¦D”Ô$U%õ¤ôäU6—27V6–W2F&ÆRÂæ÷BÆ6VÖVçBÆ—7Bâ¢¢G&VW2æ§6÷Vç2F†÷6R¦öæRf–ÆW2f÷ ¦†V–v‡BÂ7&÷vâv–GF‚Â§VÇ’föÆ–vRÂFVç6—G’æB6öæf–FVæ6RÂF†VâÆ6W2g&öÒ†æB×w&—GFVà¦4ôÔÕTä•D”U6Ö—ƒ²¦öæRw2W‡FVçF—2&VB'’fÆ÷&æ§6æBæWfW"'’G&VW2æ§6âF†R6öçG&öÂ—0¦Ç&VG’6öÖÖ—GFVB(	B¢¦£uö'W%ööµ÷6fææw2FV6Æ&VBW‡FVçB&÷‚—2BãB¶Ò÷WG6–FRF†RÖöFVÆÆV@¦f–VÆBæB—G2ö·2&RG&vâç—v’â¢¢öbF†RÆ¶W6†÷&Rw2f÷W"vööG’&V6÷&G2ÂGvòÇ&VG’F¶P§F†V—"7V2g&öÒ£U÷&—fW&&æµ÷F–Ö&W&†f—'7B¦öæRv–ç2’æBF†R÷F†W"Gvò&R–âæòÖ—‚Â6ð¦–6²‚–6âæWfW"&WGW&âF†VÒà ¢¢¤æBF†R†öÆRv2Ç&VG’ö67W–VBâ¢¢F†R¢¤ÖW&–6â7–6Ö÷&R¢¢(	B&÷WFVB'¦£U÷&—fW&&æµ÷F–Ö&W&Âf÷&ÒG&VUövÆÆW'–v—F‚â&6†WG—RÂFVç6—G•÷W%ö†³Â5ÒÂ—G2v†—FP¦Ö÷GFÆVB&&²w&—GFVâF÷vâ(	B—2–âæöæRöbF†Rf÷W"Ö—†W2æB†2æWfW"7FööB–âF†—266VæRâ—B—0§F†RöæÇ’öæRöbF†R#&÷WFVBÂ&6†WG—VBvööG’7V6–W2–âF†B÷6—F–öâÂæB¢¤³CB6÷VçFVB—B0§&V6†VB¢¢Â6÷'&V7FÇ’'’—G2÷vâFVf–æ—F–öâà ¢¢¥F†RF–Ö&W"Æ–W"†2æWfW"f—6—FVBF‡&VRV'FW'2öbF†RÖöFVÆÆVBw&÷VæBâ¢¢F†RvööG’ÆçF–æp¦Æö÷7vVW2f—†VB7V&RÂRôâ(‰#3bââ³3bÓ²F†R†V–v‡Ff–VÆB'Vç2R(‰#3#ââ³sÂâ(‰#Cââ³Câö`¢¢£“"ÃƒCB¢¢æöFW2&÷fRF†RÆçFW"w2÷vâG'’fÆö÷"Â¢£S"Ãc2ƒ#rãRR’&R–ç6–FR—BæBCÃcƒ¦&R÷WG6–FR(	Bƒrã’†¢¢âfÆ÷&æ§6w2ÆGF–6R—26VçG&VBöâF†R6ÖW&æBföÆÆ÷w2F†Rf—6—F÷"÷fW ¦ÆÂöb—Bâ£…öÆ¶W6†÷&Vw2&÷‚&Vv–ç2¢£ÃƒBÒ¢¢V7BöbF†RÆçFW"w2VFvRà ¢¢¥v†B—2VçfW&–f–VBÂ7FFVBÆ–æÇ’â¢¢F†RÆæB6Vç7W2—2â¢§WW"&÷VæB¢¢öâw&÷VæBF†RÆö÷ ¦6÷VÆBf—6—BÂæ÷B6÷VçBöb7FV×3¢F†RG&6VBvFW"Ö6²ÂF†R'V–ÆF–æw2ÂF†R6öÖ×Væ—G’6Æ76–f–W ¦æBF†RW"Ö†V7F&R&öÆÂÆÂ&VÖ÷fRÖ÷&RâFööÇ2ö6†V6²ç6†—2w&VVâv—F‚F†RGvòæWr7FW2æ@¦4Ôô´Uõd”Uuõ%CÖÖö&–ÆRæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§2Ò×V&Æ—6†VF—2w&VVã²¢§F†RFW6·F÷†Æbv0¦æ÷B'Vâ¢¢(	Bã2Ö–çWFW2v–ç7BF†—2'VææW"w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâ&÷F‚÷VÆF–öç2&P¦&æ¶VB'’FööÇ2öÖV7W&U÷ÆçF–æu÷&V6‚ç–²Fö72ôÄ”$U%D”U2æÖF¢¤Ã2¢¢6'&–W26÷'&V7F–öâæ@¢¢¤ÃB¢¢&V6÷&G2F†RGvòöÖ—76–öç2âF†R&W—"—2¢¤³CR†"’¢£¢GVæR6öÖ×Væ—G’v—F‚Æ6VÖVç@§'VÆRÂæBF†RÆçFW"w27V&R6'&–VBV7BâæV—F†W"—2öæRÆ–æRà ¢22ÖV7W&VB##bÓ‚Ób(	Bf–wW&R6â&R&VBæB7F–ÆÂ&V6‚æ÷F†–æs¢33’öbÃƒƒ‡&V6÷&BÂf–wW&R’—'2ÂæB6—‚&W6V&6†VBÆçG2&R†æFVBFòæò&VæFW&W"BÆÀ ¢¢¤³CB¢¢ÂæB—BÖ÷fW2æò&V6÷&BæBæò&VæFW&W"f–ÆRâ³C"6¶VBv†WF†W"d”uU$R—2&VBâWfW'§&VFW"†W&RF¶W2¢¦6ö†÷'B¢¢ÂæBæò&VFW"&V6V—fW2WfW'’&V6÷&C¢fÆ÷&æ§6G&w2f—fRöbF†P¦Öæ–fW7Bw26WfVâ&öÆW2æBf–gFVVâöb—G2f÷&×2÷fW"ÆÂFVâ¦öæW3²G&VW2æ§6G&w2F†R÷F†W"Gvð§&öÆW2Âf—fRf÷&×2ÂæB¢¦f÷W"öbF†RFVâ¦öæW2¢¢â×VÇF—Ç’F†R&VB×6WB'’F†B&÷WF–æræB¢£33¦öbF†RÃƒƒ‡&V6÷&BÂf–wW&R’—'2—B6ÆÇ2&VB&V6‚æ÷F†–ær¢¢(	B‚RÂ7&÷72röbF†R€¦FV6Æ&VB7V6–W2&VG2(	BæBF†RÖ&W÷'G2¦W&òöb—Bà ¢¢¥6—‚&V6÷&G2&V6‚æò&VFW"BÆÂâ¢¢f÷W"&R£…öÆ¶W6†÷&Vw2vööG’67'V"(	B¢¦6÷GFöçvööBÀ§V¶–ær7VâÂ&Ç6Ò÷Æ"Â6æF&"v–ÆÆ÷r¢¢ÂF‡&VRöbF†VÒGFW7FVF(	BÖ—76–ærg&öÒ¦D”Ô$U%õ¤ôäU6Æ—7B–âG&VW2æ§6F†BæÖW2f÷W"¦öæW2æBW‡Æ–ç2æöæRöbF†R6—‚—BÆVfW0¦÷WBâF†R¦öæRw2÷vâ&VG5ö6&öÖ—6W2¢&67'V"öb6æB6†W''’æBÆVæ–ær6÷GFöçvööB"£¢F†P§6æB6†W''’—2G&vâæBF†R6÷GFöçvööB—2æ÷Bâ¢¥F†—2—2–æFWVæFVçBöbF†Rw&÷VæBVW7F–öâ¢¢(	@§v†FWfW"³C"w2f–æF–ærF"æBBÔS26WGFÆR&÷WBF†RV7FW&âW‡FVçG2ÂF†W6Rf÷W"&R7F–ÆÂ†æFV@§Fòæ÷F†–ærâF†R÷F†W"Gvò&RF†R&—fW&&æ²w2f–æW2Âv†÷6Rf÷&ÒF†RÖæ–fW7B—G6VÆbV&Æ—6†W20§Væ–×ÆVÖVçFVBà ¢¢¤³C"w2g'V—B6VçFVæ6R—2&VgWFVBÂæB—B—2F†RöæR³C2v2÷VæVBFòw&—FRÆ–&W'G’&÷WBâ¢ ¢¢£#’öbF†R3¢¢&V6÷&G26''––ær§VÇ’g'V—B&RG&vâÂ–âF†Rg'V—Bw2÷vâ&V6÷&FVB6öÆ÷W"À§6†RÂ6—¦RæB†V–v‡B(	Bg'V—F–ær†VB6öÖW2öfb§VÇ’æ–æfÆ÷&W66Væ6VW†7FÇ’2fÆ÷vW&–æröæP¦FöW2âv†Bæ÷F†–ær&VG2—2F†R¢¦&ööÆVâ¢¢Âv†–6‚F†RfÆ–FF÷"&WV—&W2v†VæWfW"†VæöÆöw–—0¦g'V—F–ævâ¢¥F†RfÆ÷vW"F†B&VÆÇ’—2Ö—76–ær—2F†RÖW&–6â&77vööB–â&ÆööÒ¢¢Â&V6W6P¦G&VW2æ§6†2æò†VB&6†WG—RBÆÃ²F†R—&öçvööBw2g'V—BæBF†Rw&Rw2vòF†R6ÖRv’à ¢¢¥GvòÖ÷&Rf—6–&ÆRVFvW2öbF†R6ÖR&÷WF–ærâ¢¢6öÖÖöææB§VÇ’æV&æ6V&R&VB'¦G&VW2æ§6ÆöæR(	B¢£3öbSB¢¢ÆçB&V6÷&G26â&RæÖVBFòf—6—F÷"æB¢£#B6ææ÷B¢¢(	Bæ@¦§VÇ’ç†VæöÆöw–—2&VB'’fÆ÷&æ§6ÆöæRÂ6òF†RvööG’Æ–W"†2¢¦æò§VÇ’vFR¢¢à ¢¢¥v†B6†—VC¢¢¢FööÇ2öÖV7W&UöfÆ÷&÷&V6‚ç–æBFööÇ2öfÆ÷&÷&V6…ö&6VÆ–æRæ§6öæÂ&æ¶–æp¦ÆÂF‡&VR÷VÆF–öç2'’æÖRÂv—F‚f—fR76W'F–öç2‡F†RÖæ–fW7Bw2f÷&Òfö6'VÆ&–W2v–ç7BF†P§&VFW'2rF—7F6‚F&ÆW3²F†R6ö†÷'G2F—6¦ö–çBæBF÷FÃ²F†RVç&÷WFVB&V6÷&G3²WfW'’'FÇ§&V6†VB&VBv—F‚—G26÷VçG3²F†RfÆ÷vW'2F†BG&ræò†VB’ÂÆÂW†W&6—6VB'’Ò×6VÆb×FW7F–à¦FööÇ2ö6†V6²ç6†âWfW'’6ö†÷'B—266ææVB÷WBöbF†R&VæFW&W"æB66ææW"F†B6ææ÷Bf–æB—G0¦FV6Æ&F–öâ&—6W2&F†W"F†â&÷WF–ærF†RF÷vâFòæ÷F†–ærâFö72ôÄ”$U%D”U2æÖF¢¤Ã2¢¢&V6÷&G0§F†RöÖ—76–öâæBF†RF‡&VR&W—'2F†Bv÷VÆB&W6öÇfR—C²¢¤³CR¢¢—2F†R&6VÂà ¢¢¥F†RÆ–Ö—B—27FFVBÂæ÷BF—66÷fW&VBÆFW#¢¢¢F†—2ÖV7W&W2&÷WF–æröæÇ’âv†WF†W"&÷WFV@§&V6÷&B†2ÖöFVÆÆVBw&÷VæBVæFW"—B—2³C"w2f–æF–ærF"æB—2æ÷B6¶VB†W&Rà ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BÖÖ–çWFRW"Ö6öÖÖæ@¦6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&Rw&VVâà ¢22ÖV7W&VB##bÓ‚Ób(	BS‚öbF†RfÆ÷&æBfVæÆ–W'2rf–wW&W2&V6‚æ÷F†–ærÂæBöæRöbF†RGvòÆ–W'2†2æò&VFW"BÆÀ ¢¢¤³C"¢¢ÂæB—BÖ÷fW2æò&V6÷&BâF†R'V–ÆF–æw2æBF†Rw&÷VæBV6‚FV6Æ&Rv†–6‚öbF†V— ¦f–wW&W2&V6†W2fW'FWƒ²FFöfÆ÷&æBFFöfVæ(	B#“2&V6÷&G2&WGvVVâF†VÒ(	BæWfW ¦†BâF†W’Fòæ÷s¢¢£f–wW&W27&÷72f—fR&V6÷&B¶–æG2¢¢ÂgFW"–FVçF—G’Âf–ÆR&÷WF–ærÀ§&÷fVææ6RæB&÷6R&R7G&—VBF†Rv’F†Rw&÷VæB6–FR7G&—2F†VÒâ¢£3‚&V6‚fW'FW‚÷ ¦—†VÂ¢¢Â"&R6†÷vâ2FW‡BÂ"&R&VBöæÇ’'’F–væ÷7F–2ÂæB¢£S‚&V6‚æ÷F†–ær¢¢à ¢¢¥F†RÆ&vW7Bf–æF–ær—2v†öÆRÆ–W"â¢¢FFöfVæ—2¢£3’7V6–W2&V6÷&G27&÷72FVà¦†&—FB¦öæW2æB¦W&ò&VG2¢¢(	BæBF†R6†V6²F†B6—26ò—2F—&V7F÷'’66âÂæ÷Bf–VÆ@¦öæS¢¢¦æòf–ÆRVæFW"&VæFW&W'2öæÖW2F†RÆ–W"¢¢ÂæBFööÇ2÷V&Æ—6‚ç6†FöW2æ÷B6÷’—BÀ§6ò6—FRö6†–6vòóFBöFFö6öçF–ç2æòfVæöæB'&÷w6W"†2æWfW"&VVâöffW&VB—Bà¥F‡&VRFö7VÖVçG2–×Æ–VB÷F†W'v—6R(	BFF÷66VæW2óƒ3Ræ§6öæÆ—7G2fVæ–â—G2Æ–W'6À¦Fö72ôÄ”$U%D”U2æÖFÃ"FW67&–&W2F†R6÷VæG66R26†—VBÂæBFööÇ2÷fÆ–FFRç–FVÖæFV@¦V–v‡Bfö6'VÆ'’&Æö6·2&V6W6R¢&&VæFW&W"&VG2F†—2&Æö6²"¢â¢¥F†—2—2æ÷B66Rf÷ ¦FVÆWF–ærç—F†–ær¢£¢tTåE2æÖB6—2F†RFF6WB—2F†RGW&&ÆR'FVf7BæB&VæFW&W'2&P¦F—7÷6&ÆRâF†RfVÇB—2F†Bæ÷F†–ær6–B6òà ¢¢¤–âF†RfÆ÷&Âf÷W"Vç&VBF†–æw2æBöæRfÇ6R6VçFVæ6Râ¢¢FFöfÆ÷&ö–æFW‚æ§6öæw2öFö6 §6–B—G2w&÷VæEò¦æB&&U÷6ö–Åög&7F–öæ6÷–W2vW&RF†W&R¢'6òF†Rw&÷VæB6†FW"6âv÷&°¦g&öÒöæRfWF6‚"¢(	B¢¦FW'&–âæ§6æWfW"÷Vç2FFöfÆ÷&¢¢ÂæBF†B6VçFVæ6R—2æ÷r&Ww&—GFVà§Fòv†B—2G'VRâÆçF&ÆUö–å÷66VæV—2&VB'’æ÷F†–ærâF†Ræ–æRÆWGFW26''’¢£‚¢¢Vç&V@¦f–wW&W2&WGvVVâF†VÒ‡v–æBÂÄôBÂ–ç7Fæ6R'VFvWG2Âw&÷VæB6öÆ÷W'2’&V6W6RfÆ÷&æ§6W6W2—G0¦÷vâETäV6öç7FçG2æB&VG2w&VVç6æBG'•ö66VçFöæÇ’âæB¢£3fÆ÷vW&–ær7V6–W2&V6÷&@¦§VÇ’g'V—Fæ÷F†–ærG&w2¢¢à ¢¢¤³Cw2&W6–GVÂ—2ç7vW&VBÂæBF†RÆçG2&RöâF†Rv÷'6R6–FRöb—Bâ¢¢ÆÂ¢£#"¢ §Vç&W6öÇfVB×6÷W&6R6—FF–öç2–âFFöfÆ÷&6—Böâ&V6÷&BæöFRv—F‚BÆV7BöæRf–wW&RF†@§&V6†W2fW'FWƒ²ÆÂ¢£3¢¢–âFFöfVæ6—BöâÆ–W"æ÷F†–ærG&w2âF†R&VF–ærF†@¦FV6–FW2v†WF†W"F†B—2fVÇB—27F–ÆÂF†R÷væW"w2(	B6ÖRF‡&VR&÷WFW22³Cà ¢¢¥v†B6†—VC¢¢¢FööÇ2öÖV7W&UöÆ–W%÷&VG2ç–Â—G2S‚ÖVçG'’&æ²Âf—fR76W'F–öç2†WfW'¦f–wW&R6Æ76–f–VC²WfW'’&VBFV6Æ&F–öâ7F–ÆÂ&VÂ&VC²F†R'6öÇWFRÆ–W"'VÆR–â&÷F€¦F—&V7F–öç2ÇW2W"Öf–wW&R&WfW'6R66ã²æòæWrVç&VBf–wW&S²æòv†÷7B–âF†R&æ²’ÂÆÀ¦W†W&6—6VB'’Ò×6VÆb×FW7F–âFööÇ2ö6†V6²ç6†â¢¥F†RÆ–Ö—B—27FFVBÂæ÷BF—66÷fW&VBÆFW#¢¢ £"VçG&–W2v†÷6RÆVbæÖR—2&VBVæFW"æ÷F†W"&V6÷&B¶–æB&RW†V×Bg&öÒF†RW"Öf–VÆB66à¦æB&–çFVB27FFVB&F†W"F†â&÷fVâà ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BÖÖ–çWFRW"Ö6öÖÖæ@¦6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&Rw&VVââ¢¤æò&V6÷&BÂ76W@¦÷"&ÖWFW"6†ævVB¢¢ÂæBF†RöæÇ’&VæFW&W"VF—B—26†ævVÆörVçG'’à ¢22ÖV7W&VB##bÓ‚Ób(	BF†R&–v‡G2'VÆR6÷VÆBöæÇ’WfW"f—&Röâf–öÆF–öâ6öÖV&öG’†BÇ&VG’w&—GFVâF÷vâÂæBC’vVöÖWG'’Ö&V&–ærGG&–'WFW2&R'V–ÇBg&öÒ6÷W&6W2æö&öG’†26†V6¶V@ ¢¢¤³C¢¢ÂæB—BÖ÷fW2æò&V6÷&BâtTåE2æÖB'VÆRbæBFö72õ$õdTää4RæÖF6’¦6†V6µ÷&WV—&VF6÷W&6R¢&Ö’&R6—FVB–âFW‡B'WB×W7Bæ÷B†fR76WG2FW&—fVBg&öÒ—B"¢Âæ@¥$õdTää4RæÖB6–B¢¢'F†RfÆ–FF÷"Væf÷&6W2F†—2â"¢¢F†RVæf÷&6VÖVçB6ö×&W2Gvòf–VÆG2ö`§F†R¢§6ÖR6÷W&6R&V6÷&B¢¢(	B&–v‡G5÷7FGW6v–ç7BF†R6÷W&6Rw2÷vâ76WE÷W6VÆ&VÂ(	B6ò—@¦f—&W2öæÇ’v†VââWF†÷"†2&V6÷&FVBF†Rf–öÆF–öââ¢¥F†R—"†2æWfW"W†—7FVB†W&S¢3‚ö`£cB6÷W&6W2†fRVç&W6öÇfVB&–v‡G2æBWfW'’öæRFV6Æ&W27&÷75ö6†V6¶÷"FW‡EööæÇ–¢¢Âv†–ÆP§F†RF‡&VRF†BFV6Æ&RvVöÖWG'–&R7W'fW’æBGvòÖ2ÂÆÂ6ÆV"âF†RÆ&VÇ2&R†öæW7C°§F†R'VÆR—2&÷WBFW&—fF–öâæBF†RÖV6†æ—6Ò—2&÷WBFV6Æ&F–öâà ¢¢¤6¶VBöbF†RF÷vâ–ç7FVB¢¢ÂW6–ærF†R&VB×6WG2F†RvVæW&F÷'2Ç&VG’FV6Æ&P¢†4ôå5TÔTF–âV6‚¥÷&×2ç–ÂF†R6ÖRFVf–æ—F–öâ6†V6µövVöÖWG'•öFV6Æ&F–öç6W6W2ÂÇW0§F†Rfö÷G&–çBöÇ–vöâg&öÕ÷†6V&VG2“¢¢£C’vVöÖWG'’Ö&V&–ærGG&–'WFW2öâ#&V6÷&G26—FP¦âVç&W6öÇfVB6÷W&6R¢¢(	BC2öâ'V–ÆF–æw2ÂböâF†RFW'&–â7V2(	BæB¢£’öbF†R#'V–ÆF–æw0¦†fR&¶VBÖ7FW"–âF†RG&VR¢¢â¢£3RöbF†RC’7FæBöâVç&W6öÇfVB7W÷'BÆöæR¢¢æB¢£`¦öbF†÷6R&Rw&FVBGFW7FVF¢£¢F†R6Vvæ6‚†÷FVÂw27F÷&W—2æB6öç7G'V7F–öâÂF†RvöÆ`¥ö–çBFfW&âw2g&ÖRFF—F–öâæB–çFVB6–vâÂF†Rw&VVâG&VRFfW&âw2fö÷G&–çBÂ&ööbæ@§–çBÂ7BÖ'’w26‡W&6‚w2fö÷G&–çBÂF†RvW7FW&â†÷FVÂÂÖ–ÆÆW"†÷W6RÂæBF†RvW7BæB6÷WF€¦F—f—6–öâÆWfVÇ2öâF†Rw&÷VæBà ¢¢¥v†BF†—2&6VÂ&VgW6W2FòFV6–FRâ¢¢v†WF†W"F–ÖVç6–öâ&VB÷WBöb6÷—&–v‡FVBvR—0¦â&76WBFW&—fVBg&öÒ—B"—2&–v‡G2&VF–ærÂæBF†—2&ö¦V7Bw2÷vâFö7VÖVçG2F—6w&VR(	@¦Fö72õÄâæÖF&VG2—Bæ'&÷vÇ’†–ÖvW2Â¢&&Vf÷&Rç’FW&—fF—fRFW‡GW&R"¢’ÂtTåE2æÖBæ@¥$õdTää4RæÖB'&öFÇ’âF†RGvò&VF–æw2v—fR÷÷6—FRç7vW'2f÷"ÆÂC’Â6òF†RvFR†öÆG2F†P§÷VÆF–öâv†W&R—B—2æBF†R&VF–ærvöW2FòF†R÷væW#²F‡&VR&÷WFW2&Rw&—GFVâW–à¥$ôDÔ³Cà ¢¢¥v†B6†—VC¢¢¢FööÇ2öÖV7W&U÷&–v‡G5öFW&—fF–öâç–æB—G2C’ÖVçG'’&æ²Âf÷W"76W'F–öç0¢‡F†RöÆBÆ&VÂFW7B¶WBÂÇW2æWrÖfVÇBÂæòÖv†÷7BæBæò×v÷'6Væ–æröâF†R&æ²’ÂÆÂf—fP¦f–ÇW&RÖöFW2W†W&6—6VB'’Ò×6VÆb×FW7F–âFööÇ2ö6†V6²ç6†â¢¥F†R&W6–GVÂ—2æÖVBæ@¦6÷VçFVBöâWfW'’'Vã¢¢¢FFöfÆ÷&6'&–W2¢£#"¢¢6—FF–öç2öbâVç&W6öÇfVB6÷W&6Ræ@¦FFöfVæ¢£3¢¢Â&÷F‚&VæFW&VBÂæV—F†W"v—F‚FV6Æ&VB&VB×6WB(	B³C"à ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BÖÖ–çWFRW"Ö6öÖÖæ@¦6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&Rw&VVââ¢¤æò&V6÷&BÂ76WBÀ§&ÖWFW"÷"&VæFW&W"f–ÆR6†ævVBâ¢  ¢22ÖV7W&VB##bÓ‚Ób(	B—B—2ƒ’Âæ÷B“S²F†—2'VææW"&W&öGV6W2F†Ræ–v‡FÇ’w2'—FW2öâWfW'’öæRöbF†VÓ²æBF†R&Ww&—FR—2æ÷B66†VGVÆVBÂ—B—2÷Và ¢¢¤³C¢¢ÂæB—BÖ÷fW2æò76WBâ³3’6÷VÆBæ÷BfW&–g’—G2÷vâ&V6÷&BF†Rö'f–÷W2v’(	B'§&VvVæW&F–ærFW&—fF—fRæB6ö×&–ær'—FW2(	B&V6W6RFööÇ2÷vV%öFW&—fF—fW2ç6†F–Bæ÷@§&öGV6RF†R'—FW2öâF†R6—FRâ—B&W÷'FVB¢¦Æ÷vW"&÷VæBöb“R¢¢g&öÒfW'FW‚6–væGW&P¦æBæÖVBF†RW†7B6÷VçBÂF†R&–6RæBF†RFV6—6–öâ2F†—2&6VÂâÆÂf÷W"VW7F–öç2&P¦ç7vW&VBg&öÒ6öçG&öÂF†B'Vç2F†R7FW—G6VÆb÷fW"ÆÂ33BÖ7FW'2Â6‡Væ¶VB–çFòf÷W £2Ö–â#276W2Fòf—BF†R†&æW72w2FVâÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærâF†BÆö÷—2æ÷p¦FööÇ2öÖV7W&U÷vV%÷&W&öGV7F–öâç–&F†W"F†â6öÖWF†–ærWfW'’&6VÂ&V–çfVçG2ÂæB—@§&VgW6W2Fòw&—FR–çFò76WG2öVæFW"ç’fÆrà ¢¢¥F†RW†7B6÷VçC¢C"öb33B&W&öGV6Râ¢¢F†R“"f–ÇW&W2FV6ö×÷6Rv—F‚æ÷F†–ærÆVgB÷fW ®(	B¢£ƒ’6öÖR&6²'—FRÖf÷"Ö'—FRVæFW"$´UõÄUEDSÓ¢¢‡F†RÆWGFRÖW&6WB’æB¢§F‡&VP§vW&RÇ&VG’÷væVB'’æÖR¢£¢³3rw2GvòÆ6V†öÆFW'2F†B6ö×&W726ÖÆÆW"Âæ@¦FW'&–åõöSƒ3Eö†&&÷%ö7WBævÆ&BB&—G2v–ç7BbÖ&—B6²Âv†–6‚—2"Õsb†"’à ¢¢¤æBF†R6VçFVæ6RF†RæòÔ&ÆVæFW"7G&FVw’&W7G2öâ—2G'VRgFW"ÆÂâ¢¢&¶R"¢¢3sR¢ ¢ƒs£3BUD2’&Ww&—FW2¢£#ƒ¢¢FW&—fF—fW2æB†öÆG2ÆÂ“#²öâF†Rƒ’F†Ræ–v‡FÇ’w2'—FW0¦æBF†—2'VææW"w2&R¢¦ÖCRÖ–FVçF–6ÂÂƒ’öbƒ’¢¢âF†R&¶Rw2#ƒFV6ö×÷6RW†7FÇ’(	Bƒ§ÆWGFRÖW&²“Æ6V†öÆFW"Ö7FW'2Ww&FVBFò6æöæ–6Â&6†WG—R&¶W2²FW'&–â@£b&—G2(	B6ò&–æ'’F–fbæö&öG’6÷VÆB&Wf–Wræ÷r†2â&—F†ÖWF–2âv†Bv2w&öærv0¦æWfW"F†RW‡G&7F–öã¢¢¤³3b†"’6'&–VB7FW6†ævRF‡&÷Vv‚3‚f–ÆW2æBæ÷B33Bâ¢  ¢¢¤³3’w2fW'FW‚6–væGW&R—2&VgWFVB2â–FVçF–f–W"¢¢Â–â&÷F‚F—&V7F–öç3¢ƒ’6†&VBÂ¢§6—€§vVÆFVBf–ÆW2FöF’w27FW&W&öGV6W2W†7FÇ’¢¢†÷F–Ö—¦VFVGW2v—F†÷WBF†RÆWGFR72¦æBF‡&VRf–ÇW&W2v—F‚æòvVÆBâ“R—2çVÖ&W"Fò7F÷V÷F–ærÂæBæòvFR—2'V–ÇBöâ—Bà ¢¢¥F†R&–6R¢¢Âf÷"F†R&V6÷&C¢³C‚Ãƒ3b'—FW2÷fW"F†Rƒ’†ÖVâ³#S‚ÂÆÂƒ’w&÷r’Â³C‚Ã3#€¦æWB7&÷72F†RG&VR(	B¢£ã‚RöbF†R#RÔ"'VFvWB¢¢â³3’w26×ÆR6–B³“ræB3P§&W&öGV7F–öã²F†RG'WF‚—2³#S‚æBC"ãRRà ¢¢¥GvòFV6—6–öç2â¢¢¥v†òÖ÷fW2F†Rƒ’£¢æö&öG’†W&R(	Bâ÷Vâ"Ç&VG’†öÆG2F†÷6RW†7@¦'—FW2ÂæBF†—2&6VÂæV—F†W"&VvVæW&FW2F†VÒæ÷"ÖW&vW2F†B"â¢¢3sRæB3cB6''’æð§7FGW26†V6·2BÆÂ¢¢&V6W6R&÷BÖ÷VæVB"FöW2æ÷BG&–vvW"F†RFWbvFS²'Vææ–ær—@¦v–ç7BF†VÒ—2F†R¦æ—F÷"w2¦ö"æBF†R÷væW"w26ÆÂâ¥6†÷VÆBF†R&V6÷&BæÖRF†R5DU£ ¢¢¦æòâ¢¢fÆr7G&–ær—2&÷6RæB6â&RVF—FVBFòGW&âvFRw&VVã²67&—B†6‚v÷VÆ@¦†fR–çfÆ–FFVBÆÂ33BVçG&–W2öâV6‚öbF†Rf÷W"6öÖÖ—G2F†B†fR6†ævVBF†R7FWÀ¢¢§Gv–6Röâ6öÖÖ—BF†BÖ÷fVBæò'—FR¢¢ƒ3‚Â2ÂÂ’âv†BF†Rf–ÇW&RæVVFVBv2'VÆRÀ¦æB—B—2–âF†R7FWw2†VFW#¢¢¦6†ævRF†BÖ÷fW2ç’FW&—fF—fRw2'—FW2&VvVæW&FW2ÆÀ£33BÂæ÷BF†RöæW2F†Bf—6–&Ç’'&ö¶Râ¢  ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&Rw&VVââ¢¤æð¦76WBÂ&V6÷&BÂ&ÖWFW"÷"&VæFW&W"f–ÆR6†ævVBâ¢  ¢22f—†VB##bÓ‚Ób(	BF†R6†—VBÖöFVÂæ÷r&V6÷&G2F†RÖöFVÂ—Bv2ÖFRg&öÓ²æB“RöbF†VÒvW&RÖFR'’7FWF†—2&W÷6—F÷'’æòÆöævW"†0 ¢¢¤³3’â¢¢³3‚w2&W6–GVÂv2F†B7FÆVæW72v27F–ÆÂ¢§F–ÖW7F×¢£¢FööÇ2÷V&Æ—6‚ç6† ¦6ö×&VB×F–ÖW2ÂæBöâg&W6‚6ÆöæRv—B6†V6¶÷WFw2w&—FR÷&FW"Ö¶W2¢£33Böb33B¢ ¦Ö7FW'2öÆFW"F†âF†V—"FW&—fF—fW2Â6òF†R66âv26–ÆVçBöâW†7FÇ’F†RG&VR'Và§7F'G2g&öÒâÖ7FW"&V'V–ÇBv—F‚F†R6ÖRvVöÖWG'’æBF–ffW&VçBô4ôäd”DTä4VfÇVW2(	@§F†R66RF†R67&—Bw2÷vâ6öÖÖVçBv2w&—GFVâ&÷WB(	B76VBF†B66âæBÆÂV–v‡@¦6öçFVçB76W'F–öç2Æ–¶Rà ¢¢¥v†BÖ÷fVBâ¢¢FööÇ2÷vV%öFW&—fF—fW2ç6†&V6÷&G2æÖR(i"6†#Sb†Ö7FW"–2—B&öGV6W0¦V6‚FW&—fF—fRÂ–çFò¢¦76WG2öÖæ–fW7BçvV"æ§6öæ¢¢Â&W6–FR76WG2öÖæ–fW7Bæ§6öæ¢F†P¦Öæ–fW7B&V6÷&G2FF(i"Ö7FW"æB—2w&—GFVâ'’F†R&ÆVæFW"'V–ÆBÂF†—2&V6÷&G2Ö7FW"(i ¦FW&—fF—fRæB—2w&—GFVâ'’F†R7FWgFW"—Bâ¢¤76W'F–öâ’¢¢6ö×&W2F†R&V6÷&FVB†6€§FòF†RÖ7FW"–âF†RG&VRÂ'6öÇWFR–â&÷F‚F—&V7F–öç2(	BÖ÷fVBÖ7FW"f–Ç2Âà§Vç&V6÷&FVBFW&—fF—fRf–Ç2ÂâVçG'’v—F‚æòf–ÆRf–Ç2âW†W&6—6VBöâF†R&VÂG&VRÂæ÷@¦öæÇ’–âÖVÖ÷'“¢öæR'—FRVæFVBFòÖ7FW"Ö¶W2F†RvFRf–Â'’æÖRæ@¦FööÇ2÷V&Æ—6‚ç6†&VgW6R&Vf÷&Rw&—F–ærç—F†–ærâV&Æ—6‚ç6†æòÆöævW"66ç2×F–ÖW2@¦ÆÃ²—B'Vç2F†RvFRâ¢¥F†W&R—2FVÆ–&W&FVÇ’æòfÆrç—v†W&RF†B&Ww&—FW2F†R&V6÷&@§v—F†÷WB&VvVæW&F–ærF†R'—FW2¢¢(	BF†R&VÖVG’—2Çv—2ÒÖöæÇ’ÆæÖSæà ¢¢¥F†R6÷WÆ–ærv2F†R&VÂVW7F–öâæB—B—2FV6–FVC¢F†R5DUw&—FW2—BÂWfW'’'VâÂæ@¦&¶R6'&–W2F†RF–fbâ¢¢F†R&V6÷&Bw2Æ–fV7–6ÆR—2F†RFW&—fF—fRw2(	B6ÖR&öGV6W"Â6ÖP§'VâÂ6ÖR6öÖÖ—B(	B6òæ–v‡FÇ’&Ww&—FW2—B–âF†R6ÖR'&VF‚æB6ææ÷BÆVfRF†RFW`¦vFR&VBf÷"WfW'–öæRVÇ6Râ—B—2FVÆ–&W&FVÇ’¢¦æ÷B¢¢–à¦FööÇ2÷vV%öFW&—fF—fUö&6VÆ–æRæ§6öæÂv†–6‚—2&V6÷&BöbfVÇG2W'6öâ&æ·2'’†æBà ¢¢¤äBD„R4ôåE$ôÂD„Bt25Uõ4TBDòdU$”e’•BDôU2äõBU„•5Bâ¢ ¦FööÇ2÷vV%öFW&—fF—fW2ç6†6—2—B¢'&W&öGV6W233öb33B"¢âÖV7W&VC¢¢£böb#¢¢–â§7&VB6×ÆRÂæB¢¦ÆÂBF†Bf–ÆVB6öÖR&6²'—FRÖf÷"Ö'—FRVæFW"$´UõÄUEDSÓ¢¢à¦÷F–Ö—¦Vw2ÆWGFR72v2¢§vVÆF–ær¢¢Â³3b†"’GW&æVBF†R72öfbf÷"G&rÖ6ÆÂ&V6öç0§F†B7FæBÂæB—B&VvVæW&FVBöæÇ’F†R3‚76WG2v†÷6RÖFW&–Â–FVçF—G’†B'&ö¶Vââ'§fW'FW‚6–væGW&R(	Bæòç†æVVFVB(	B¢£“RöbF†R#C6ö×&W76VBFW&—fF—fW26''’fWvW §fW'F–6W2F†âF†V—"Ö7FW'2¢¢ÂÃS2fW'F–6W2–âF÷FÂÂæBF†B—2Æ÷vW"&÷VæBà ¢¢¤æ÷F†–æröâF†R6—FR—2w&öær¢£¢vVÆB—2Æ÷76ÆW72ÂG&–ævÆW2&RWVÂÂæB76W'F–öç0£(	3’&Rw&VVâöâÆÂ“Râv†B—2fÇ6R—2F†R6Æ–ÒF†BF†—2'VææW"6â&VvVæW&FRv†@§F†Ræ–v‡FÇ’6†—2(	BG'VRf÷"Cböb#C(	BæBF†R6öç6WVVæ6R—266†VGVÆVC¢¢§F†RæW‡B&¶P§&Ww&—FW2ÆÂ“R2VçvVÆFVBf–ÆW2¢¢Â“RÖf–ÆR&–æ'’F–fbv—F‚æòçVÖ&W"GF6†VBFò—Bà¢¢¤³C¢¢÷vç2F†R6÷VçBÂF†R&–6RæBF†RFV6—6–öâÂæBF†RgW'F†W"VW7F–öâ³3’FV6Æ–æVC §v†WF†W"F†R&V6÷&B6†÷VÆBæÖRF†R5DU2vVÆÂ2F†RÖ7FW"à ¢¢¥7FFVBÂæ÷BF–F–VC¢¢¢F†R&V6÷&Bv2¢§6VVFVB¢¢–âF†—26öÖÖ—BÂæ÷B&öGV6VB'’gVÆÀ§'VâÂ&V6W6RgVÆÂ'Vâv÷VÆBÖ÷fRF†÷6R“Rf–ÆW2âöæRVçG'’v2w&—GFVâ'’F†R7FW†—G0¦FW&—fF—fR6ÖR&6²ÖCRÖ–FVçF–6Â“²F†R÷F†W"332&W7Böâ76W'F–öç2(	3‚æBöâF†R“0§77F‡&÷Vv‡2r'—FR–FVçF—G’v—F‚F†V—"Ö7FW'2â—BFöW2æ÷B6Æ–ÒF†R6†—VB'—FW26ÖP¦g&öÒFöF’w27FWà ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BF†—2†&æW72w0£ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&P¦w&VVââæò6öÖÖ—GFVB76WB6†ævVB'—FRà ¢22f—†VB##bÓ‚Ób(	BV&Æ—6‚7FW6÷VÆBWBã"Ô"öbVæ6ö×&W76VBÖöFVÇ2–çFòF†R–ÆöBæBF†Rv†öÆRvFR6–B4„T4²50 ¢¢¤³3‚â¢¢³3ræ÷F–6VBF†—&Bw&—FW"öb76WG2÷vV"öæBFV6Æ–æVBFò6†6R—C ¦FööÇ2÷V&Æ—6‚ç6†6÷–VBç’Ö7FW"F‡&÷Vv‚v†VæWfW"—Bv2æWvW"'’×F–ÖRâ6†6VBÂ—B—0§v÷'6RF†âF†Ræ÷FRà ¢¢¤—B—2&V6†&ÆR–âöæR6öÖÖæBÂæBæ÷F†–ær6VW2—Bâ¢¢Gvò6ö×&W76VBÖ7FW'2F÷V6†VB(	@§F†R7FFRF†RG&VR&V6†W2v†VæWfW"vVæW&F÷'2ö'V–ÆBç–—2'Vâöâ—G2÷vâÂv†–6‚—2F†P¦66RF†R67&—Bw2÷vâ6öÖÖVçB6—2F†R6÷’W†—7G2f÷"(	BF†VâFööÇ2÷V&Æ—6‚ç6† ¦f÷'EöFV&&÷&å÷Æ—6FV¢£BÃsc‚(i"ƒCÃƒ3b'—FW2¢¢æBFV&&÷&å÷7G&VWEöG&v'&–FvV ¢¢£sÃSB(i"SSrÃ“b¢¢â¢¢³Ã#"Ãsc'—FW2¢¢–çFòF†R–ÆöBÂw&—GFVâ–çFòF†R§G&6¶VB §6÷W&6RG&VRæBÖ—'&÷&VBFò6—FRöâöâF†BG&VRF†RFW&—fF—fRvFRW†—FVBÀ¦6†V6µ÷V&Æ—6†VBæÖ§6W†—FVBÂæBF†RgVÆÂFööÇ2ö6†V6²ç6†&–çFVB¢¤4„T4²52¢¢à ¢¢¤æB—B6÷VÆBæ÷B†fR&VVâ÷F†W'v—6Râ¢¢Ö7FW"6÷–VB÷fW"—G2÷vâFW&—fF—fR†2F†@¦Ö7FW"w2G&–ævÆW2ÂæöFR–FVçF—G’Â6öçG&7BGG&–'WFW2Â&÷VæF–ær&÷‚‡¦W&ò'Væw2’æ@¦ÖFW&–ÂF&ÆRÂæB'—FR6÷VçBF†B—2WVÂ&F†W"F†âÆ&vW"â³3b†’w2V–v‡B76W'F–öç0§vF6‚F†R§G&ç6f÷&ÖF–öâ¢76WG2övÇFbò(i"76WG2÷vV"ö²F†W’6ææ÷B6VRf–ÆRF†B6¶—V@¦—Bâ¢¤vFRw&—GFVâv–ç7BG&ç6f÷&ÖF–öâ—2æ÷BvFRöâ—G2÷WGWBF—&V7F÷'’â¢  ¢¢¤—B—2æ÷BF‡&VRw&—FW'2(	B—B—2F‡&VR67&—G2æBf÷W"77F‡&÷Vv‚'&æ6†W2¢¢ÂF‡&VRö`§F†VÒ6–ÆVçC¢F†R6—¦R'VÆR³3rFV6–FVBƒ“276WG2’Â÷F–Ö—¦Vw2f–ÇW&RfÆÆ&6²À¦vÇFb×G&ç6f÷&Ö×Væf–Æ&ÆR6÷––ær¢¦ÆÂ33B¢¢‡–ÆöBBãSB(i"#ã“bÔ"ÂBãl9rv–ç7B£#RÔ"'VFvWB’ÂæBV&Æ—6‚ç6†w2×F–ÖR6÷’â¢¤æB×F–ÖRæWfW"6ö×&VB'—FS¢¢¢öâg&W6€¦6ÆöæR¢£33Böb33BÖ7FW'2&RöÆFW"F†âF†V—"FW&—fF—fW2¢¢Â'’v—B6†V6¶÷WFw2–æFW€¦÷&FW"Â6òF†R'VÆRf—&W2öâç’&V'V–ÆBæB—2&Æ–æBöâF†RG&VR'Vâ7F'G2g&öÒà ¢¢¥v†BÖ÷fVC¢¢¢æò76WBÂæò&V6÷&Bâ¢¤76W'F–öâ‚¢¢Â'6öÇWFR–â&÷F‚F—&V7F–öç2v–ç7BF†P£“277F‡&÷Vv‡2&æ¶VB'’æÖR(	B“GF‚f–Ç2v†–6†WfW"w&—FW"ÖFR—BÂæB&æ¶VBöæRF†@§&WGW&ç26ö×&W76VBf–Ç2æB6—2Fò&RÖ&æ²â&÷F‚Ò×6VÆb×FW7F×WFF–öç2f—&Rà¢¢¦FööÇ2÷V&Æ—6‚ç6†—2æòÆöævW"w&—FW"öb76WG2÷vV"ö¢£¢—B¶VW2F†R66âÂÖ÷fW2—@¦&÷fRF†Rf—'7Bw&—FRæB&VgW6W2ÂæÖ–ærV6‚f–ÆRæBF†RFööÇ2÷vV%öFW&—fF—fW2ç6‚ÒÖöæÇ– §F†B&W—'2—BâfW&–f–VBVæBFòVæB(	BF†R6ÖRGvòF÷V6†W2æ÷r7F÷—BBW†—Bv—F‚F†P§v÷&¶–ærG&VR6ÆVâà ¢¢¥7FFVBÂæ÷BF–F–VC¢¢¢æWrÆ6V†öÆFW"æ÷ræVVG2Ò×w&—FRÖ&6VÆ–æV–âF†R6öÖÖ—BF†BFG0¦—BÂ&V6W6R'F†RvVæW&F÷"FFVBöæR"æB'6öÖWF†–ær6÷–VBÖ7FW"F‡&÷Vv‚"&RF†R6ÖP¦'—FW2æBöæRöbF†VÒ—2FV6—6–öââæB&VgW6–æröâ×F–ÖR—27F–ÆÂ×F–ÖR(	BÖ7FW"&V'V–Ç@§v—F‚F†R6ÖRvVöÖWG'’æBF–ffW&VçBô4ôäd”DTä4VfÇVW276W2&÷F‚F†R66âæB76W'F–öç0£.(	3râ¢¤³3’¢¢—2F†B&W6–GVÃ¢F†R7FW¶æ÷w2v†–6‚Ö7FW"—B6ö×&W76VBæBw&—FW2—BF÷và¦æ÷v†W&Rà ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BF†—2†&æW72w0£ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&P¦w&VVââæò6öÖÖ—GFVB76WB6†ævVB'—FR–âF†—2&6VÂà ¢22f—†VB##bÓ‚Ób(	BF†Ræ–æWG’Vç7VVW¦VBf–ÆW2vW&R&–v‡BÂæBF‡&VR7VVW¦VBöæW2vW&R6†—–ær&–vvW"F†âF†RÖöFVÇ2F†W’6ÖRg&öÐ ¢¢¤³3râ¢¢³3b†’&W÷'FVB“FW&—fF—fW22'—FRÖ–FVçF–6ÂÖ7FW"6÷–W2æB³3b†"’w26öçG&öÀ¦f÷VæBF†BF†R—VÆ–æRw2÷vâ7FWFöW2æ÷B&W&öGV6RF†VÒâ'Vâ÷fW"ÆÂ“ÂF†R7FWF¶W2F†VÐ¢¢£S#Ãs(i"c#‚Ã#‚'—FW2Â³rÃ3#‚‚³#ãbR’¢¢Âv—F‚¢£ƒ‚öbF†R“w&÷v–ær¢£¢ÖW6†÷Fw&—FW0¦6ö×&W76–öâ†VFW"Â'VffW"×f–WrF&ÆRæBâ–æFW‚'VffW"ÂæBöân(	3c×G&–ævÆR6†VBF†÷6P¦6÷7BÖ÷&RF†âF†R6ö×&W76–öâ6fW2â¢¥F†R77F‡&÷Vv‚v2F†R&–v‡Bç7vW#²—Bv2§W7Bæö&öG’w0¦FV6—6–öâ¢¢(	B—BfVÆÂ÷WBöbvVæW&F÷'2ö–æfW'&VE÷Æ6V†öÆFW"ç–w&—F–ærF†R6ÖR'—FW2–çFò&÷F€§G&VW2à ¢¢¤æBF†R6Æ72&VF–6FR—2w&öær–â&÷F‚F—&V7F–öç2â¢¢¶–æC¢Æ6V†öÆFW&Ö2öçFð¢'Væ6ö×&W76VB"“öb“FöF’ÂæBF†B—26ö–æ6–FVæ6Röbw&—FR÷&FW"âF‡&VR76WG2F†B†fP¦&VVâF‡&÷Vv‚F†—27FWöâWfW'’&¶R6–æ6R—Bv2w&—GFVâ6†—¢¦Æ&vW"¢¢F†âF†V—"Ö7FW'2(	@¦f÷'EöFV&&÷&å÷&ö÷Eö†÷W6V³3#BÂÆ¶Uö†÷W6Uö6öç7G'V7F–öæ³#CÂf÷'EöFV&&÷&åöÖv¦–æV³##B(	@§v†–ÆRf÷'EöFV&&÷&å÷&FVÂRÃSB'—FW2æB3G&–ævÆW2Â6ö×&W76W2(‰##BãRRÂæBGvòöbF†P¦æ–æWG’Æ6V†öÆFW'26ö×&W72(‰#’ã2Râ'—FR6—¦RFöW2æ÷B&VF–7BF†R6–vâV—F†W"â6òF†R'VÆR—0¢¢¦¶VWv†–6†WfW"f–ÆR—26ÖÆÆW"ÂÖV7W&VBW"76WB¢¢ÂæB—BÆ—fW2–à¦FööÇ2÷vV%öFW&—fF—fW2ç6†&F†W"F†â–âÆ—7BöbæÖW2à ¢¢¥v†BÖ÷fVC¢¢¢F‡&VRFW&—fF—fW2Â&WÆ6VB'’F†V—"Ö7FW'2(	B¢®(‰#sƒ‚'—FW2¢¢ÂæBF†W’æ÷r6''¦W†7BfÆöB÷6—F–öç2&F†W"F†âVçF—6VBÆGF–6RâF†R“&RVçF÷V6†VBâ¢¥F†RvFS¢¢ ¦ÖV7W&U÷vV%öFW&—fF—fW2ç–76W'F–öâbÂ'6öÇWFRÂ¢¦&÷VæB¦W&ò¢¢Âv—F‚Ò×6VÆb×FW7FF†@¦w&÷w2FW&—fF—fR'’öæR'—FRæB6öæf—&×2—Bf—&W2¦æB¢w&÷w2âWö6‚ÖW6‚'’öæR'—FRæ@¦6öæf—&×2—BFöW2æ÷Bà ¢¢¥F†RöæRW†6ÇW6–öâÂ'’æÖS¢¢¢vFW%õöSƒ3Eö†&&÷%ö7WBævÆ&—2³sCB'—FW2‚³SRãR’VæFW"F†P§'VÆRæB—2¢¦æ÷B¢¢76VBF‡&÷Vv‚âF†RWö6‚ÖW6†W2r&—BFWF‚—2vVöÖWG&–2FV6—6–öâ…"Õsb’À§F†Rw&÷VæBæBvFW&Æ–æR&Rv†B"Ô%Ts62Â"Ô%TsBæB"ÔÓÖV7W&Rv–ç7BÂæB¢¥"Õsb†"’†öÆG0¦&÷F‚f–ÆW2¢¢VæF–ærF†R÷væW"w2v÷&Böâ&VvVæW&F–ærvVöÖWG'’÷WG6–FR&¶Rà ¢¢¤ÆVgB÷VâÂ7FFVC¢¢¢F†RGvòÆ6V†öÆFW'2F†B6ö×&W726ÖÆÆW"7F’Ö7FW"6÷–W2(	@¦–æfW'&VE÷Æ6V†öÆFW"ç–&Ww&—FW2WfW'’Æ6V†öÆFW"–çFò&÷F‚G&VW2öâV6‚'VâæBv÷VÆBVæFð§F†VÒâ¢£Ãc#B'—FW2â¢¢æBFööÇ2÷V&Æ—6‚ç6†—2¢§F†—&B¢¢w&—FW"öb76WG2÷vV"ö¢—B6÷–W2¦Ö7FW"F‡&÷Vv‚v†VæWfW"—B—2æWvW"'’×F–ÖRÂv†–6‚—277F‡&÷Vv‚æ÷F†–ærFV6–FVBæBv†–6€§F†—2vFR6ææ÷B6VRâv÷'F‚&6VÂà ¢¢¥F†RvFRw2÷vâ6VÆb×FW7B†B&VVâ&VB6–æ6R³3b†"’¢¢(	B&V&æ¶–ærF†RÖFW&–Â&F6†WBV×G¦ÆVgBöæR×WFF–öâv—F‚æ÷F†–ærFò×WFFRÂæB—B&–çFVBÔ•54TBÂ6òÒ×6VÆb×FW7F&W÷'FV@¥4TÄbÕDU5Bd”Âöâ6ÆVâG&VRâæ÷F†–æræ÷F–6VB&V6W6R6†V6²ç6†&âÒÖvFVæBæWfW ¦Ò×6VÆb×FW7Fââ–æÆ–6&ÆR×WFF–öâæ÷r&–çG26¶—VFÂæB6†V6²ç6†'Vç2F†R6VÆb×FW7@¦2—G2÷vâ7FWà ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BF†—2†&æW72w2ÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&Rw&VVââæ÷F†–æp¦†W&RÖ÷fW2fW'FW‚ÂÖFW&–Â÷"÷6Rà ¢22f—†VB##bÓ‚Ób(	BF†R6ö×&W76–öâfÆrF†B†–B3‚'V–ÆF–æw2rÖFW&–ÂæÖW2v2Ç6ò7VæF–ærF†RF÷vâw2G&rÖ6ÆÂ'VFvWBÂæB†ÆbF†Ræ6†÷'2vW&R÷fW"—@ ¢¢¤³3b†"’â¢¢³3b†’&V6÷&FVBF†RÆWGFR722fVÇB&÷WBäÔU3¢vÇFb×G&ç6f÷&Ò÷F–Ö—¦V ¦föÆG2F†RæÖVBÖFW&–Ç2öbç’f–ÆR6''––ærf—fR÷"Ö÷&RöbF†VÒ–çFòöæRÆWGFTÖFW&–Æ §ÇW2vVæW&FVBäw2Â6ò3‚6†—VB76WG2Æ÷7BÆövÂ6†–æ¶–ævÂ&ö&FÂ&ööfÂF&¶À¦–çFW&–÷&öâF†Rv’FòF†R'&÷w6W"âF†R72w2÷vâ§W7F–f–6F–öâ—2F†BÖW&v–ærÖFW&–Ç0§6fW2G&r6ÆÇ2Â6òF†R&VF–ærv2F†BæÖW2†B&VVâG&FVBf÷"7VVBâ¢¤æV—F†W"v2G'VRà¤—B6÷7B&÷F‚â¢  ¢¢¤d”äD”är(	BvVæW&FVBÖÖ¶W2â76WBVæ&F6†&ÆRâ¢¢ÖFW&–Ä¶W’‚––à¦&VæFW&W'2÷vV"ö§2ö'V–ÆF–æw2æ§6–æ6ÇVFW2ÒæÖòçWV–FÂæBtÅDdÆöFW"Ö–çG2g&W6‚WV–BW ¦ÆöFVBFW‡GW&RÂ6òÆWGFR76WB6ææ÷B¦ö–âç’&F6‚(	Bæ÷BF†RF÷vâw2ÂæBæ÷Bæ÷F†W §ÆWGFR76WBw2âF†R3‚6†—VB2¢£C6–ævÆRÖ'V–ÆF–ær&F6†W2¢¢ƒCÂæ÷B3ƒ¢6Vvæ6…ö†÷FVÆ ¦6ÖR÷WBv—F‚F‡&VRÆWGFTÖFW&–Æ2Â—G2vÆ72æB6‡WGFW'2&VgW6–ærF†RÖW&vR’öâF÷öbF†P§F÷vâw2bâ¢¥F†RV&Æ—6†VBF÷vâG&WrSb&F6†W2â"ÕsVw26öÖÖ—GFVBf–wW&R—2bâ¢¢v—F‚F†R70¦öfc¢Sb(i"bÂFW‡GW&W2–âÖVÖ÷'’SR(i"CÂ6†FW"&öw&×2R(i""à ¢¢¤d”äD”är"(	B"ÕsVw2çVÖ&W'2vW&RF¶VâöâF†R6÷W&6RG&VRâ¢¢—G2¢&æòÖöbç’¶–æB"¢v0§G'VRöbv†BF†—2&W÷6—F÷'’&¶W2æBæWfW"G'VRöbv†BF†R6—FR6W'fW2(	BF†R–FVçF–6ÂW'&÷ ¤³3b†’f÷VæB–â"Õs&w2ÖFW&–Â6†VWBÂg&öÒF–ffW&VçB&6VÂÂF‡&VRF—2'Bâ"ÕsVw0§&W7VÇB7FæG2ƒCr(i"b—2&VÂÂæB—2v†BF†RCæ÷rföÆB&6²–çFò“²—G2#b&F6†W2"v0¦æWfW"7FFVÖVçB&÷WBF†R6—FRâFööÇ2öÖV7W&U÷6†—VEö&F6†W2æÖ§6&VG2F†R¢¦Ö—'&÷"¢¢'¦FVfVÇBæB&–çG2v†–6‚G&VR—B&VBÂ6òF†W&R—2æòF†—&BF–ÖRFò†fRà ¢¢¤d”äD”är2(	Bf÷W"öbF†RV–v‡B66VæRæ6†÷'2vW&R÷fW"F†RƒÖ6ÆÂ'VFvWBöâF†R6—FRâ¢¢¦&F6‚†öÆF–æröæR'V–ÆF–ær—27VÆÆVBv—F‚F†B'V–ÆF–ærÂ6òF†—2—2–BW"÷6RæB—2v÷'7@§v†W&RF†RF÷vâ—2FVç6W7BâB#ƒ9sƒÂF‡&÷Vv‚F†R&VæFW&W"w2÷vâvõFö  §ÂÂw&VVå÷G&VRÂf÷&·2Âg&öÕö&÷fRÂ6÷WF…÷vFW"ÂÆ¶UöÖ&¶WBÂ2væ6…÷v–ærÂe÷÷7Eööff–6RÂ6Vvæ6‚À§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â&Vf÷&RÂ¢£"¢¢Â¢£“b¢¢Â¢£ƒB¢¢Â¢£ƒ"¢¢ÂsÂc‚ÂcbÂc"À§ÂgFW"ÂsÂc‚Âc2Âc’Âc2ÂcÂcÂS’À ¤æ÷F†–ær†BÖV7W&VB—C¢F†R6Öö¶R&VG2F†R6÷VçFW"Bv†FWfW"÷6R—B—27FæF–ær–âÂæ@¦7&—F–5÷6†÷G2æÖ§6&W÷'G2G&r6ÆÇ2W"7FF–öâv—F†÷WB76W'F–æröâF†VÒà ¢¢¥F†R6÷7B—2ƒrÃ3“"'—FW2¢¢(	BF†R3‚vò3‚ÃSC(i"SRÃ“3"‚³S‚ã‚R’Â&V6W6R“ræÖV@¦ÖFW&–Ç2F¶RÖ÷&R&ööÒF†âsRvVæW&FVBäw2âF†B—2³BãRöâBãRÔ"G&VRv–ç7B£#RÔ"'VFvWBâÖFW&–Â–FVçF—G“¢33Böb33FÂæB³3b†’w2&F6†WB—2&V&æ¶VBV×G’à ¢¢¦FööÇ2÷vV%öFW&—fF—fW2ç6†—2F†R7G'V7GW&Â†Æbâ¢¢F†RvV"ÖFW&—fF—fR7FW—2Æ–gFVB÷WBö`¦FööÇ2ö&¶Rç6†v†öÆRÂ6ò&ÆVæFW"Ög&VR'VææW"6â&VvVæW&FRFW&—fF—fW2g&öÒF†R6öÖÖ—GFV@¦Ö7FW'2æBÖV7W&RF†VÒ(	BÆ–æ²"6÷VÆB&R¦f÷VæB¢'&ö¶Vâ'’³3b†’æBæ÷B§&W—&VB¢v—F†÷WB¦æ–v‡FÇ’âF†R6öçG&öÂF†BÖ¶W2F†—2GG&–'WF&ÆS¢VæFW"$´UõÄUEDSÓ—B&W&öGV6W2¢£#C2ö`£33BFW&—fF—fW2'—FRÖf÷"Ö'—FR¢¢Â–æ6ÇVF–ærÆÂ3‚à ¢¢¥F†R÷F†W"“&RGvòf–æF–æw2F†—2&6VÂF–Bæ÷Bf—‚æBF–Bæ÷B†–FRâ¢¢¢¤³3r¢¢(	B“ ¦FW&—fF—fW2&R'—FRÖ–FVçF–6ÂÖ7FW"6÷–W2ÂæBF†R—VÆ–æRw2÷vâ7FWFöW2æ÷B&W&öGV6P§F†VÓ¢—BÖ¶W2F†VÒã#R¦&–vvW"¢ƒBÃ“c‚(i"bÃöâF†R6×ÆR’âæ÷F†–ær7FFW2v†–6€¦&V†f–÷W"—2–çFVæFVBâ¢¢„³3r—2DôäR##bÓ‚Ób(	BF†R77F‡&÷Vv‚—26÷'&V7BÂÖV7W&VB÷fW"ÆÀ£“B³#ãbRÂæBF†R6×ÆRvVæW&Æ—6VC²6VRF†R6V7F–öâ&÷fRâ’¢¢¢¥"Õsb†"’¢¢(	BF†R6†—V@§FW'&–â—27F–ÆÂ¢£BÖ&—B¢£¢&VvVæW&F–ærF†P¦6öÖÖ—GFVBÖ7FW"BB&—G2&W&öGV6W276WG2÷vV"÷FW'&–åõöSƒ3Eö†&&÷%ö7WBævÆ&ÖCRf÷"ÖCRÀ¦æBF†RÃbÖ'—FRvFòF†RbÖ&—Bf–ÆR—2W†7FÇ’"Õsbw2÷vâV÷FVB6÷7Bâ¢¥"Õsbw2f—‚—2–à§F†R67&—BæBæ÷B–âF†Rf–ÆRf—6—F÷"F÷væÆöG2¢¢Â6òF†Rw&÷VæB—27F–ÆÂöâF†R3bÖÐ¦ÆGF–6R"Ô%Ts62f÷VæB'W&–W2F†R&öBâ&÷F‚&R÷Vâ&6VÇ2–âFö72õ$ôDÔæÖFà ¢¢¤æ÷BfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbF†R6Öö¶R‡ã2Ö–âv–ç7BF†—2†&æW72w2ÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–ær’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbÒ×V&Æ—6†VF&Rw&VVâÂæBF†P¦FW6·F÷G&rÖ6ÆÂçVÖ&W'2&÷fR&RÖV7W&VBB#ƒ9sƒ'’F†RæWrFööÂà ¢22æWr##bÓ‚Ó#‚(	BF†R&W6–FVçG26Vç7W2ÂæB2W'6öâ&÷w2&VF–ær¶ö&¦V7Bö&¦V7EÖ  ¢¢¥BÓ#ò$ôDÔ³S"†"’â¢¢³S"vfRFF÷&W6–FVçG2ö6V6öæB&VFW"öâ##bÓ‚Óræ@¤³C"w276W'F–öâ6F–Bæ÷Bf—&RÂ&V6W6RF†R76W'F–öâ6âöæÇ’f–Âf÷"Æ–W ¦FööÇ2öÖV7W&UöÆ–W%÷&VG2ç–vÆ·2æB—G2Æ–W"Æ—7Bv2GvòæÖW2ÆöærâF†B—2F†R†öÆP§F†—26Æ÷6W2ÂæBF†R6Vç7W2—BÖFR÷76–&ÆR—2v†Bf÷VæBF†RfVÇB&VÆ÷rà §ÂÆ–W"Âf–wW&W2ÂÖW6‚Â6†÷vâÂVç&VBÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â&W6–FVçG2ö†÷W6V†öÆFÂCBÂÂC"Â"À§Â&W6–FVçG2öÖæ–fW7FÂ#RÂÂ#"Â2À§Â¢§F†RÆ–W"¢¢Â¢£c’¢¢Â¢£¢¢Â¢£cB¢¢Â¢£R¢¢À ¢¢¤æ÷F†–ær†W&R—2ÖW6†æBæ÷F†–ærWfW"v–ÆÂ&Râ¢¢ÃæBtTåE2æÖBw27FæF–ær6öç7G&–ç@¦†öÆC¢cG&w2æò‡VÖâf–wW&W2Â6òæòf–wW&RöbW'6öâÖ÷fW2fW'FW‚–âF†—266VæRà¦6†÷væ—2F†Rv†öÆRöbF†R&VB6–FRà ¢222F†RfVÇC¢f–wW&R6â&R6†—VBÂfWF6†VBÂ&VæFW&VBæB7F–ÆÂæ÷B&V@ ¦vUööå÷66VæUöFFVÂ&—'F…÷–V&æBæÖUö&6—6&Rw&FVB6Æ–Ò&Æö6·2(	@¦·fÇVRÂ6öæf–FVæ6RÂæ÷FRÂ6÷W&6W7ÖÂW†7FÇ’Æ–¶RF†R†÷W6V†öÆBw2÷vâ6Æ–×2(	Bæ@¦W'6öä‡FÖÆ76VBÆÂF‡&VRv†öÆRFògVæ7F–öâF†BW66W2v†B—B—2v—fVâà ¢Ò¢£2öb#’W'6öâ&÷w2¢¢&VB†÷rF†—2W'6öâ—2æÖVB(	B¶ö&¦V7Bö&¦V7EÖà¢Ò¢£’öbF†VÒ¢¢&VB—BGv–6RÖ÷&RÂf÷"F†RvRæBF†R&—'F‚–V"à¢Ò¢¤WfW'’7FvRÓ’76W'F–öâ76VBF‡&÷Vv†÷WBâ¢¢F†R7V—FR6¶VBv†WF†W"F†R6V7F–öâÆöG2À¢6÷VçG2ÂÖ&·2—G2röfbÖ6&B†÷W6V†öÆG2ÂV÷FW2—G26÷W&6W2æB7F'G26öÆÆ6VBâ6&@¢F†B&VæFW'2F†Ru$ôär7G&–ær&VæFW'27G&–ærÂæBæöæRöbF†÷6RVW7F–öç26â6VR—Bà ¥v†Bv2Æ÷7B—2æ÷BFV6÷&F–öââæÖUö&6—2çfÇVV—2F†RööÂâ–çfVçFVBæÖRv2G&và¦g&öÒÂæB2öbF†—2F÷vâw2V÷ÆR6''’æÖW2F†—2&ö¦V7B–çfVçFVBâf—†VB'’&÷WF–ærF†P§F‡&VRF‡&÷Vv‚6Æ–Õ&÷vÂv†–6‚—2v†BWfW'’÷F†W"w&FVB6Æ–ÒöâF†R6&BÇ&VG’W6VBà ¢¢¥F‡&VRæWr6Öö¶R6†V6·2ÂV6‚fW&–f–VBFòf–Âv–ç7BF†RöÆB&VæFW"F‚&Vf÷&R—Bv0¦¶WB¢¢(	BÖV7W&VBÂæ÷B76W'FVC¢æòf–wW&R&V6†W2W'6öâw2&÷r2¶ö&¦V7Bö&¦V7EÖ²à¦–çfVçFVBæÖR6—2v†–6‚ööÂ—B6ÖRg&öÓ²FFVBW'6öâ6'&–W2âvRæB&—'F‚–V"À¦&÷F‚w&FVBâf÷W'F‚v2w&—GFVâæB¢¦F—66&FVB¢£¢â76W'F–öâöâF†R6VçFVæ6R¢%D„RäÔP¤•2”ådTåDTB"¢76W2öâF†R'&ö¶Vâ'V–ÆBÂ&V6W6RF†B6VçFVæ6R—2–âF†RW'6öâw2æ÷FVæ@§F†Ræ÷FR&V6†VBF†R6&BF‡&÷Vv†÷WBâ6†V6²F†B6ææ÷Bf–Â—2æ÷B6†V6²à ¢222Gvò6ÖÆÆW"†öÆW2Âv—&VB–âF†R6ÖR6öÖÖ—@ ¦6÷VçG2æ'•öw&FV&V6†VBæ÷F†–ær&V†–æB¢&WfW'’öæRöbF†VÒw&FVB"¢(	BG'VRÂæB—BFVÆÇ2§&VFW"æ÷F†–ærâF†Ræ÷FRv—fW2F†RFÆÇ’æ÷s¢¢£sbGFW7FVBÂ#–æfW'&VBÂ2&V6öç7G'V7FVB¢¢à¤æBfö6'VÆ'’ç6W†W6v2F†RöæR6Æ÷6VB6WBF†RæVÂv—F††VÆBv†–ÆR6†÷v–ærW'6öç5µÒç6W† ¦öâWfW'’W'6öâw2&÷rà ¢222F†Rf—fR&VgW6Ç2Â–âw&—F–æræB–âF†R&æ° ¦FööÇ2öÆ–W%÷&VG5ö&6VÆ–æRæ§6öæv–æVB&VgW6VEö&V6W6Vf–VÆBâ6÷VçG2æ†÷W6V†öÆG6À¦†÷W6V†öÆG5µÒç&W6VçEööå÷66VæUöFFVæBF†R†÷W6V†öÆB&V6÷&Bw2÷vâF—f—6–öæ&P¦FVæ÷&ÖÆ—6VB6÷–W2öbF†–æw2Ç&VG’6†÷vâ(	BF†RÖæ–fW7Bw2fÆB6÷’öbw&FVB6Æ–Ð¦6'&–W2æV—F†W"—G26öæf–FVæ6RÂ—G2&V6öæ–æræ÷"—G26÷W&6W2Â6ò6†÷v–ær—Bv÷VÆB&R6†÷v–æp¦ÆW72â†VFÂ–â&÷F‚6÷–W2Â—2f÷&V–vâ¶W’–çFòW'6öç5µÒæ–F²F†Rf7B—B7FFW2Ç&VG§&V6†W2F†Rf—6—F÷"2F†BW'6öâw2&VÆF–öç6†—â¢¤&VgW6Â—2æ÷BW&Ö—76–öâ¢¢(	BF†P¦VçG&–W27F’&æ¶VBÂ76W'F–öâB7F–ÆÂf–Ç2öâæWrVç&VBf–wW&RæB76W'F–öâR7F–ÆÀ¦f–Ç2–böæRöbF†W6RÆVfW2F†RFFà ¢222v†B—2äõBfW&–f–V@ ¥F†R6Vç7W2—2¢§FW‡B66â¢¢÷fW"&VæFW&W'2÷vV"ö§2ò¢æ§6v—F‚6öÖÖVçG27G&—VBÂæBöâF†—0¦Æ–W"F†RÆVbæÖW2&RF†R&VæFW&W"w2÷vâfö6'VÆ'’(	BfÇVVÂæ÷FVÂæÖVÂ†VFâf—fP¦öbF†RVç&VBVçG&–W2&RF†W&Vf÷&R¢§7FFVB¢¢&F†W"F†â&÷fVâÂÆ—7FVB27V6‚'’F†RFööÀ¦æBæÖVB–â5DDTEõ4„$TFv—F‚v†BV6‚6öÆÆ–FW2v—F‚âfW&–f–6F–öâv27FvW2‚æB’@¦&÷F‚f–Ww÷'G2Âf÷W"ÆVw2Âf–ÆVBÂvRW'&÷'3²F†R÷F†W"6WfVâ7FvW2vW&Ræ÷B&R×'VâÀ¦æBæ÷F†–ær÷WG6–FRF†RWf–FVæ6RæVÂv2F÷V6†VBà ¢22æWr##bÓ‚Ób(	BF†RF÷vâöâF†R6—FR†2sRFW‡GW&W2ÂæBF†R&W÷6—F÷'’†2æöæP ¢¢¤³3b†’â¢¢F†RvVöÖWG'’f—6—F÷"F÷væÆöG2&V6†W2F†VÒÆöærf÷W"Æ–æ·2(	@¦FFö(i"76WG2övÇFbö‡F†RÖ7FW'2’(i"76WG2÷vV"ö‡F†R6†—VBFW&—fF—fW2’(i ¦6—FRö6†–6vòóFBö‡F†RV&Æ—6†VBÖ—'&÷"’âÆ–æ²—2vFVB'’F†R7FÆVæW726†V6²ÂÆ–æ²2'¦6†V6µ÷V&Æ—6†VBæÖ§6ÂæB¢¦Æ–æ²"v2vFVB'’æ÷F†–ærBÆÂ¢£¢æò†6‚Âæò6÷VçBÂæð¦76W'F–öâF–VB6†—VBFW&—fF—fRFòF†RÖ7FW"—Bv26ö×&W76VBg&öÒâ—B—2Ç6òF†RÆ–æ°§v—F‚F†RÖ÷f–ær'G2(	BGvòvÇFb×G&ç6f÷&Ö76W2(	BæBFööÇ2ö&¶Rç6†w2÷vâ6öÖÖVçG2&V6÷&@§v†B†2Ç&VG’6öÖR÷WBöbF†VÓ¢¢&'VrF†B6öÆÆ6VBWfW'’'V–ÆF–ærFòGvòÖÖWG&R&÷€§6†—VB7BgVÆÇ’w&VVâvFR(	BGv–6R"¢ÂæBÒ×FW‡GW&RÖ6ö×&W72·Gƒ&fÆrF†B¢'6–ÆVçFÇ§GW&æVBWfW'’FW&—fF—fR–çFòâVæ6ö×&W76VB6÷’öb—G2Ö7FW"Â–âWfW'’Vçf—&öæÖVçBÂ6–æ6P§F†—27FWv2w&—GFVâ"¢â&÷F‚vW&Rf÷VæB'’W'6öâ&VF–ærF†R67&—Bà ¢¢¤d”äD”är(	BF†R6†—VBF÷vâ—2FW‡GW&VBæBF†R&¶VBF÷vâ—2æ÷Bâ¢¢÷F–Ö—¦Vw2ÆWGFP§72föÆG2F†RæÖVBÖFW&–Ç2öb¢£3‚öbF†R33B76WG2¢¢–çFò6–ævÆRÆWGFTÖFW&–Ã ¦6''––ærvVæW&FVBäw3¢¢£sRFW‡GW&W2W†—7BöâF†R6—FRF†BW†—7B–âæòÖ7FW"¢¢ÂæBF†P¦æÖW2F†W’&WÆ6R(	BÆövÂ6†–æ¶–ævÂ&ö&FÂ&ööfÂF&¶Â–çFW&–÷&(	B&RvöæRg&öÒF†P¦f–ÆR'&÷w6W"ÆöG2âÖöærF†VÒF†R6Vvæ6‚†÷FVÂÂF†RvöÆbö–çBFfW&âæB—G27F&ÆRÂF†P¦Æör¦–ÂÂF†RW7G&’VâÂ6ö'vV"67FÆRÂF†R6÷Væ6–Â†÷W6RæBVÆWfVâ&V6öåò¦&V6öç7G'V7F–öç2à ¢¢¥F†R7Æ—B—24õTåBÂæB—B—2W†7Bâ¢¢WfW'’76WBv†÷6RÖ7FW"6'&–W2¢¦f—fR÷"6—‚¢ ¦ÖFW&–Ç2—2fVÇFVB(	B3öbF†VÒÆöuöGvVÆÆ–ævÂb÷WF'V–ÆF–ævÂg&ÖU÷FfW&æ(	BæBWfW'¦76WB6''––ær¢¦f÷W"÷"fWvW"¢¢—26ÆVâÂÆÂ#“böbF†VÒÂv—F‚æòW†6WF–öâ–âV—F†W ¦F—&V7F–öââF†B—2F†RÆWGFR72w2÷vâF‡&W6†öÆB&F†W"F†âç—F†–ær&÷WBÆöw2‡F†RFööÀ¦æÖW2—G2÷WGWBÆWGFTÖFW&–ÃæB—G2Fö7VÖVçFVBÖ–æ–×VÒ—2f—fRÖFW&–Ç2’â6ò¢§F†P¦fVÇBw&÷w2v—F‚F†RF÷vâöâ&÷VæF'’#sR76WG2&R6—GF–ærW†7FÇ’öæRÖFW&–Â6†÷'Böb¢£ ¦â&6†WG—RF†Bv–ç2f–gF‚7W&f6R(	Bv†–6‚—2&V6—6VÇ’v†B"Õs&"—2f÷"(	BÖ÷fW2WfW'¦76WB—B–çG27&÷72F†RÆ–æRâF†R&F6†WB—2v†BÖ¶W2F†B'&—fÂÆ÷VBà ¢¢¤d”äD”är"(	B"Õs&w2ÖFW&–Â6†VWB—26†VWBöbF†RÖ7FW'2ÂæB—B6—26ò–âF†Rw&öæp§v÷&G2â¢¢Fö72õ$U4T$4‚öÖFW&–Ç2æÖF÷Vç2'’&V6öæ–ærF†B¢'F†R6÷W&6RæBF†R6†—VB'—FW0¦†fRF—6w&VVB–âF†—2&ö¦V7B&Vf÷&R(
b6†VWBF†B–çfVçF÷&–W2–çFVçF–öç2—2v÷'F‚æ÷F†–ærFð¦&¶R"¢ÂæBF†VâÖV7W&W276WG2övÇFbò¢¢ò¢ævÆ&VæFW"F†R†VF–ær¢'F†R7W&f6R6Vç7W2À¦ÖV7W&VBg&öÒF†R6†—VBtÄ'2"¢âF†÷6R&RF†RÖ7FW'2â—G2¢¢&æ÷F†–ær–âF†RF÷vâ6'&–W2§FW‡GW&Röbç’¶–æB"¢¢—2G'VRöbv†BF†—2&W÷6—F÷'’&¶W2æBfÇ6Röbv†BF†R6—FR6W'fW2À¦æB¢¥"Õs&"(	BF†RæW‡B–6²–âF†BÆæR(	BÆç2Fòv—&RâFÆ2öçFòF†RÖFW&–ÂæÖW2F†@§F†RV&Æ—6‚F‚FVÆWFW2öâ3‚76WG2â¢¢F†R6†VWB—26÷'&V7FVB–âÆ6S²æöæRöb—G2f—fP¦f–æF–æw2Ö÷fW2à ¢¢¤d”äD”är2(	B“76WG26†—Væ6ö×&W76VBæBæ÷F†–ær6—26òâ¢¢F†W’&RW†7FÇ’F†R“ §W&RÕ—F†öâÆ6V†öÆFW"tÄ'2Âv†–6‚vVæW&F÷'2ö–æfW'&VE÷Æ6V†öÆFW"ç–w&—FW2'—FRÖ–FVçF–6ÆÇ¦–çFò&÷F‚G&VW3²F†R#CB&ÆVæFW"Ö&¶VB76WG26ö×&W72Rã#œ9râ—B—2S‚´"ÂãBRöbF†P§–ÆöBÂæBæ÷B&ö&ÆVÒFöF’(	BF†Rö–çB—2F†BF†R&¶R&W÷'G2fÆÆ&6²6÷’2§v&æ–ærÆ–æR–âÆöræö&öG’&VG2ÂæBF†RöæÇ’6öÖÖ—GFVB–ç7G'VÖVçBF†B6÷VÆBæ÷F–6R—2£#RÔ"F÷FÂ×6—¦R'VFvWBF†RG&VR—2æ÷v†W&RæV"à ¢¢¥t„BDôU2äõBÔõdRÂÔT5U$TBâ¢¢G&–ævÆR6÷VçG2&R–FVçF–6ÂöâÆÂ33B—'2Â6ð¦Ò×6–×Æ–g’fÇ6V†2†VÆC²æöFRæÖW2Â7G'V7GW&Uö–Fö†6Uö–FW‡G&2æBÖW6‚æÖW2ÆÀ§7W'f—fS²ô4ôäd”DTä4V(	B†÷rf—6—F÷"—2FöÆBv†–6‚'G2vRÖFRW(	B&V6†W2F†R6—FRöà¦WfW'’76WBF†B6'&–W2—BâF†Rv÷&ÆB&÷VæF–ær&÷‚w&VW2FòBv÷'7B¢£"ãc2'Væw2¢¢öbà¦76WBw2÷vâW‡FVçBƒãrÖÒöâ"ãrÒ6†VB’ÂæBF†RFW'&–âw2ƒ"ã‚ÖÒ—2¢£ã‚'Væw2¢¢ö`¦—G2RÃ#Ò&÷‚Â6öç6—7FVçBv—F‚F†RsbãbÖÒÆGF–6R"Õsb6öÖÖ—GFVBâ¢¤6÷'&V7FVB##bÓ‚Ób'¤³3b†"“¢''Vær"F†W&R—2W‡FVçBòcSS3V'’F†RvFRw2÷vâFVf–æ—F–öâÂæ÷BF†Rf–ÆRw27GVÀ¦ÆGF–6RÂæBF†R6†—VBFW'&–â—2BÖ&—B(	B6òƒ"ã‚ÖÒ—26öç6—7FVçBv—F‚3bÖÒÆGF–6RFöòÀ¦æBF†B—2F†RöæRf—6—F÷"—27FæF–æröââ6VR"Õsb†"’â¢  ¢¢¥F†RvFR—2FööÇ2öÖV7W&U÷vV%öFW&—fF—fW2ç’ÒÖvFVÂ–â6†V6²ç6†ÂBã"2æBv—F‚æð¦FV6öFW"¢¢(	BWfW'’6Æ–Ò&÷fR—2ç7vW&&ÆRg&öÒF†RvÅDb¥4ôâ6‡Væ²âf—fR'6öÇWFR76W'F–öç0¢†&–¦V7F–öâÂG&–ævÆW2Â–FVçF—G’Â6öçG&7BGG&–'WFW2Â&÷VæF–ær&÷‚’æBöæR&F6†W@¢†FööÇ2÷vV%öFW&—fF—fUö&6VÆ–æRæ§6öæÂF†R3‚’âÆÂV–v‡Bf–ÇW&RÖöFW2vW&R'&ö¶VâFVÆ–&W&FVÇ¦–âÒ×6VÆb×FW7FæBV6‚f—&W2â¢¥F†R&W—"—2³3b†"’¢¢(	B—B&VvVæW&FW233B&–æ'’f–ÆW2Â6ð¦—B—26W&FR&6VÂæB—BFöW2æ÷BæVVB&ÆVæFW"â¢¤DôäR##bÓ‚ÓbÂæB—BGW&æVB÷WBFò&P¦&÷WBG&r6ÆÇ2&F†W"F†âæÖW2(	B6VRF†RF÷öbF†—2f–ÆRâ¢  ¢22æWr##bÓ‚Ób(	BF†R6öç7G&–çBF†—2&ö¦V7BWG2&÷fRF†Rv÷&²v2¶WB'’F†R'V–ÆF–æw2æBæ÷B'’F†RV÷ÆP ¢¢¤³3Bâ¢¢tTåE2æÖBw27FæF–ær6öç7G&–çB—2F†RöæR6VçFVæ6R–âF†—2&W÷6—F÷'’F†B÷WG&æ·0§F†R&W7Böb—C¢F†Rf–æÂ&VÖ÷fÂöbF†R÷FvFöÖ’g&öÒ6†–6vò—2¢¤VwW7Bƒ3R¢¢Â–ç6–FRF†P¦f—'7BF&vWB–V"ÂæB—B—2¢&æ÷B&W6V&6‚vFò&Rf–ÆÆVB'’–æfW&Væ6R"¢â—B—2v—fVà¦W†7FÇ’öæRÖV6†æ—6Ò(	B¢¦&Wf–Wu÷&WV—&VC¢G'VVöâç’&V6÷&B&Æö6·266VæRg&öÒ&V–ærÖ&¶V@¦&VÆV6VF¢¢(	BæBæ÷F†–ær†BWfW"ÖV7W&VBv†BF†B6VçFVæ6R6÷fW'2à §ÂÆ–W"Â6'&–W2F†RfÆrÂF–B—B&Æö6²&VÆV6SòÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×À§ÂFF÷7G'V7GW&W2öÂ¢£’¢¢öb33"Â–W2À§ÂFF÷&W6–FVçG2ö†÷W6V†öÆG2Â¢£r¢¢öbs2Â¢¦æò¢¢À§ÂFF÷&W6–FVçG2öW'6öç2Âöb#’Â¢¦æò(	BF†RÆ–W"v2æWfW"&VB¢¢À ¢¢¤d”äD”ärÂäB•B•2ôäR$T4õ$Bâ¢¢†…ö6ÆGvVÆÅö&–ÆÇ–(	B&–ÆÇ’6ÆGvVÆÂÂ6Vvæ6‚ÂF†P¦vVæ7’w2–çFW'&WFW"æBF†RæÖW6¶RöbF†RF÷vâw2&W7BÖ¶æ÷vâFfW&â(	B6'&–W2F†—26VçFVæ6P¦–â—G2&W6V&6…öæ÷FVÂ–âF†R6ÖRv÷&G2†…÷&ö&–ç6öåöÆW†æFW&W6W3¢¢$—B6'&–W0§&Wf–Wu÷&WV—&VB6òF†Bæò66VæR6öçF–æ–ær—B6â&RÖ&¶VB&VÆV6VB&Vf÷&RF†R6öç7VÇFF–öà§F†R&ö¦V7B†26öÖÖ—GFVBFòâ"¢¢¥F†Rf–VÆBv2fÇ6VÂæBv—BÆörÕ6f–æG2æò6öÖÖ—B–à§v†–6‚—Bv2WfW"ç—F†–ærVÇ6Râ¢¢F†R&V6÷&B†2&VVâ&öÖ—6–ærF†RfÆr6–æ6R—Bv2w&—GFVâà¦F÷V6†W5÷&VÖ÷fÂ(y"&Wf–Wu÷&WV—&VF(	BF†RöæR'VÆRF†RfÆ–FF÷"F–B†öÆBöâF†—2Æ–W"(	B6÷VÆ@¦æ÷B6VR—BÂ&V6W6RF÷V6†W5÷&VÖ÷fÆv2fÇ6VFöòà ¤&÷F‚&RG'VVæ÷rÂ¢¦öâF†R&V6÷&Bw2÷vâ6öÖÖ—GFVBFW‡BæBöâæ÷F†–æræWr¢£¢F†R6ÖRæ÷FP¦Ç&VG’V÷FW2æG&V2WGF–ærF†—2ÖâBF†R†VBöbF†RÖ&6‚FòF†RÖ—76÷W&’âæ÷F†–ærVÇ6P¦&÷WBF†R&V6÷&BÖ÷fVBÂæBF†Ræ÷FRæ÷r6—2F†RfÆw2vW&RfÇ6RæBF†BF†R&w&‚&÷fP§F†VÒ6–B÷F†W'v—6Rà ¢¢¤d”äD”är"(	BF†R6WfVâ†÷W6V†öÆG2vW&R6fR'’6ö–æ6–FVæ6Râ¢¢fÆ–FFRç–w266VæRvFR'V–Ç@¦—G2&Æö6¶VBÆ—7B÷WBöbFF÷7G'V7GW&W2öÆöæRÂv†–ÆRF†RW'&÷"—B&–çG2öâF†R¦†÷W6V†öÆB §6–FR6—2ç’&V6÷&BF÷V6†–ærF†R&VÖ÷fÂ¢&&Æö6·266VæRg&öÒ&V–ærÖ&¶VB&VÆV6VB"¢âF†@¦6öç6WVVæ6RF–Bæ÷BföÆÆ÷râF†R†÷W6V†öÆG2vW&R6÷fW&VBç—v’&V6W6R¢¦ÆÂöbF†V— ¦Æ—fW5öFöv÷&·5öFÆ–æ·2ÆæBöâ7G'V7GW&RF†B—2fÆvvVBFöò¢¢(	Bf7Bæ÷F†–ær&WV—&VBÀ¦æ÷F†–ærÖV7W&VBÂæBæ÷F†–ærv÷VÆB†fRæ÷F–6VBF†RÆ÷72öbâfÆvvVB†÷W6V†öÆBv—F‚çVÆÀ¦Æ—fW5öFæBâVæfÆvvVBv÷&·Æ6R76VB6ÆVã²F†B66VæR—2æ÷r6öÖÖ—GFVB6VÆb×FW7Bà ¢¢¤d”äD”är2(	BF†R6ÖR6VçFVæ6RÂ&VBF†R÷F†W"v’Â—2FVÆ–&W&FRäòæBæ÷BFVfV7Bâ¢ ¦6†VÅö–æfçE÷66†ööÆÂvÆ¶W%öÖVWF–æuö†÷W6VæBvF¶–ç5÷66†ööÅö†÷W6VV6‚6¢¢'&Wf–Wu÷&WV—&VB—26WBfÇ6R(
b'WBF†R6ÆÂ—2v÷'F‚6V6öæB÷–æ–öâ"¢ÂæBV6‚—2fÇ6Rà¥6òF†RvFRFW7G2¢¦&÷F‚F—&V7F–öç2¢¢&F†W"F†â'&÷6RÖVçF–öç2F†R&VÖ÷fÂ(y"6WBF†RfÆr"à¤vFRF†B6÷VÆBæ÷BFVÆÂf–æF–ærg&öÒf–æF–ær2v÷VÆB†fR&VVââ–ç7G'VÖVçB&wV–ærf÷ ¦—G2÷vâ6öæ6ÇW6–öââv†B—BÆVfW2÷Vâ—2¢¤³3R¢£¢F‡&VRöbF†Ræ–æRfÆvvVB7G'V7GW&W27FFP¦æò&V6öâç—v†W&RÂæBF†R'V–ÆF–ær6–FR†2æòf–VÆB&V6öâ6÷VÆBÆ—fR–âà ¢¢¤dõU"%4ôÅUDR54U%D”ôå2äBäò$D4„UB¢¢ÂFVÆ–&W&FVÇ’(	B&F6†WB—2F†R&–v‡B–ç7G'VÖVç@¦f÷"fVÇB&V–ær–BF÷vâÂæBF†—2—26öÖÖ—FÖVçBâ&÷6RÖF6†W2f–VÆC²F÷V6†W5÷&VÖ÷fÆ ¦–×Æ–W2&Wf–Wu÷&WV—&VFB†÷W6V†öÆBäBW'6öâÆWfVÃ²F†RfÆr&V6†W2F†R'V–ÆF–æp¢ƒöb“²æB(	B&V†f–÷W&ÂÂv–ç7BF†R&VÂFF6WB(	B66VæRv—F‚&VÆV6VFf÷&6VBG'VP¦—2&VgW6VBf÷"¢¦W†7FÇ’¢¢F†RVæ–öâöbfÆvvVB–G27&÷72WfW'’Æ–W"Â6òvFRF†B&W7FFV@§F†R'VÆR6ææ÷B72v†–ÆRF†RfÆ–FF÷"F—6w&VW2v—F‚—BâFööÇ2÷&Wf–Wuö6öç7G&–çEö&6VÆ–æRæ§6öæ ¦Ö¶W2F†R7–ÖÖWG'’W‡Æ–6—C¢¢¦FF–ærfÆr—2g&VRÂ6ÆV&–æröæRf–Ç2¢¢æBæÖW2v†@¦6ÆV&–ær—Bv÷VÆBÖVâà ¢¢¥F†RvFRv2fW&–f–VBFòf–ÂÂöâf÷W"6W&FR–æ¦V7F–öç2¢¢(	BF†R6ÆGvVÆÂfÆr6ÆV&V@¦v–âÂ6ö'vV%ö67FÆVVæfÆvvVBVæFW"F‡&VR†÷W6V†öÆG2ÂW'6öâv—fVâF÷V6†W5÷&VÖ÷fÆ §v—F†÷WB&Wf–Wu÷&WV—&VFÂæBF†RfÆ–FF÷"&WfW'FVBFò7G'V7GW&W2ÖöæÇ’âV6‚W†—G2v—F‚F†P¦F—fW&vVæ6RæÖVBÂæBF†R&W7F÷&VBG&VR76W2à ¢¢¥fW&–f–VC¢¢¢FööÇ2ö6†V6²ç6†w&VVââ4Ôô´Uõd”Uuõ%CÖÖö&–ÆRæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6 ¦w&VVâv–ç7BF†RV&Æ—6†VBÖ—'&÷"â¢¥F†RFW6·F÷†Æbv2äõB'VâæB—2æ÷B6Æ–ÖVB0§76VB¢¢(	B—BæVVG2ã2Ö–çWFW2v–ç7BF†—2†&æW72w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærÂv†–6‚F†P¥$ôDÔw2'VâÖ'VFvWB&÷‚&V6÷&G2âF†—2&6VÂ6†ævW2æò&VæFW&W"f–ÆRÂæòvVöÖWG'’æBæð¦6ö÷&F–æFRà ¢¢¥v†B—BF–BäõBFó¢¢¢—BÖ÷fVBæò'V–ÆF–ærÂ†÷W6V†öÆB÷"6ö÷&F–æFRÂ–çfVçFVBæ÷F†–æræ@§&Vw&FVBæ÷F†–ærâæòÆ–&W'G’—2÷vVB(	BFö72ôÄ”$U%D”U2æÖF&V6÷&G2–çfVçF–öç2ÂæBF†W&R—2æð¦–çfVçF–öâ†W&Râ—BF–Bæ÷BFV6–FRv†WF†W"F†RF‡&VRVæW‡Æ–æVB7G'V7GW&RfÆw2æVVB&V6öà¦f–VÆC²F†B—2³3RæB—B—2â÷væW"w26†ö–6RÂæ÷BvFRw2à ¢22æWr##bÓ‚Ób(	BF†W&R—2'&–FvR–âF†—266VæR÷fW"vFW&6÷W'6RF†R66VæRFöW2æ÷B6öçF–à ¢¢¥BÔSR†’â¢¢F†RFW'&–â7V2FVfW'2f÷W"–â×F÷vâvFW"fVGW&W2VæFW"öæR6†&VB‡&6R(	@¢¢&W†—7FVæ6RFö7VÖVçFVBÂvVöÖWG'’6öæ¦V7GW&Â"¢âW†—7FVæ6R—26Æ–Ò&÷WB¢§Æ6R¢£²66VæR—0¦¢¦FFR¢¢âæö&öG’†B6¶VBF†R6V6öæBVW7F–öâöbç’öbF†Rf÷W"ÂæBF†W’Fòæ÷Bç7vW"—@¦Æ–¶Rà §ÂF÷76–W"¦öæRÂfVGW&RÂBƒ3RÓrÓÂv†BFFW2—BÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§ÂBÂF†R6Æ÷Vv‚Â¢§&W6VçB¢¢†–æfW'&VB’Â7G'V7GW&RF†—2&ö¦V7BÇ&VG’7FæG2–âF†R66VæRÀ§ÂRÂ¢¥F†RV&Æ–2×7V&RöæB¢¢Â¢¦æ÷BW7F&Æ—6†VB¢¢†–æfW'&VB’Âæ÷F†–ær(	BæBöæRFö7VÖVçB&wVW2&÷F‚v—2À§ÂbÂF†Rg&öröæBÂÆ¶RbÆ6ÆÆRÂ&W6VçB†–æfW'&VB’ÂæWw7W"ÂöæR–V"ÆFRFòF†RF’À§ÂrÂF†RvVÆÇ27G&VWBÖ'6‚Â&W6VçB†–æfW'&VB’ÂF†R6VçFVæ6RF†Bv—fW2F†R6Æ÷Vv‚v—fW2v†B—BG&–ç2À ¢¢¥D„R4„%U5Bd”äD”är•2äõBD„RôäBâ¢¢6Æ÷Vv…öÆöuö'&–FvV(	B¥F†R6Æ÷Vv‚Æör'&–FvRÂvFW ¥7G&VWB¢(	B—26öÖÖ—GFVB7G'V7GW&R7FæF–æröâƒ3RÓrÓÂæB—G2÷vâFö7VÖVçFVE÷&ævVæ÷FP§V÷FW2F†R6÷W&6R'Vææ–ærF†B7&÷76–ær¢'VçF–ÂgFW"ƒC"¢â¦öæRBÂF†R6Æ÷Vv‚—B7&÷76W2Â—0¦FVfW'&VBæBVæG&vââ¢¤f—6—F÷"vÆ·2öçFòF–Ö&W"7&÷76–ærÆ–B÷fW"÷Vâ&—&–R¢¢ÂæB†0¦&VVâ&ÆRFò6–æ6RF†R'&–FvRÆæFVBâF†B—2æ÷Bâ&wVÖVçBf÷"7WGF–ær6öæ¦V7GW&Â6†ææVÂ(	@§F†RFWF‚æBv–GF‚&R7F–ÆÂVç6÷W&6VBæB&6VÂ†2’7F–ÆÂ÷vç2F†VÒâ—B—2F†R&ööbF†BF†P¦f÷W"vW&RæWfW"öâöæRfö÷F–ærÂv†–6‚öæR6†&VB‡&6R–×Æ–VBF†W’vW&Rà ¢¢¤öâF†RöæBF†Rç7vW"—2æ÷EöW7F&Æ—6†VFÂæBFVÆ–&W&FVÇ’äõB&—Bv2æ÷BF†W&R"â¢¢öæP¦Fö7VÖVçBÂ6†–6vöÆöw•÷&Vf—&S#s6Â6'&–W2&÷F‚6–FW2ÂæBæö&öG’†Bæ÷F–6VBF†B—BFöW2à¢¢¤dõ#¢¢¢—G26Æ÷Vv‚6VçFVæ6R†2F†R7G&VÒG&–æ–ær¢'F†RöæBæBF†RÖ'6‚W‡FVæF–ærWvVÆÇ0¥7G&VWB"¢2Æ—fRfVGW&RöbG&–ævR7—7FVÒv†÷6R'&–FvR÷WFÆ—fW2F†R66VæR'’f—fR–V'2à¢¢¤t”å5B¢¢ÂæBF†RFVfW'&ÂvV–v†VBæöæRöbF†W6RF‡&VS  £â¢¥F†RV÷FF–öâFFW2æ÷F†–ær¢¢(	B¢'v2F†VâöæB"¢Â7BFVç6Rv–ç7Bâ¢£ƒSr¢¢&W6VçBÀ¢–âFö7VÖVçBF†—2&ö¦V7Bw2÷vâ6÷W&6R&V6÷&B–FVçF–f–W22'V–ÇBöâ¢¤‡V&&&Bw26†–6vò2†P¢f÷VæB—B–âƒ‚¢¢æB¢¤Ff—2w2ƒ3"¢¢G&v–ærà£"â¢¥F†RF÷76–W"w2÷vâ&÷r6—2F†Rw&öær6V6öâ¢¢(	B&÷rR&VG2¢'6V6öæÂ(
bvFW"ã^(	3"gBFVW ¢¢¦–â7&–ær¢¢"¢ÂæBF†R66VæRFFR—2¢£§VÇ’¢¢âF†R&÷r7FFVB6V6öã²F†RFVfW'&Â&VB¢66VæRà£2â¢¥Gvò6÷VçG’'V–ÆF–æw2Ç&VG’7FæBöâF†B&Æö6²Â&Vf÷&RF†R66VæRFFR¢¢(	BF†R¢¦W7G&¢Vâ¢¢Â6†–6vòw2f—'7BV&Æ–2'V–ÆF–ærÂöâF†R6÷WF‚×vW7B6÷&æW"g&öÒ¢¤Ö&6‚ƒ3"¢¢ÂæBF†P¢¢¦Æör¦–Â¢¢öâF†Ræ÷'F‚×vW7B6÷&æW"g&öÒF†R¢¦fÆÂöbƒ32¢¢â÷VæB—2æ÷B'V–ÇB–âöæBà ¢¢¥F†R'V–ÆF–æw2Fòæ÷B&VgWFRöæB(	BF†W’$õTäBöæRÂæBF†B—2F†Rv†öÆR&W7VÇBâ¢¢§v†öÆRÖ&Æö6²öæB—2&VgW6VB'’F†—2&ö¦V7Bw2÷vâ6öÖÖ—GFVB&V6÷&G3²'F–ÂöæR—2VçF÷V6†VB'§F†VÒæB—2W†7FÇ’F†RFVÆ—fW&&ÆRBÔSRw2F†—&BVW7F–öâ6¶VBf÷"Âv†–6‚æò6÷W&6R&V6†VB6à§7WÇ’â6òF†RFFRæBF†RW‡FVçB&R¢¦öæRVW7F–öâ¢¢æBæV—F†W"—26WGFÆVBâW†—7FVæ6P¦Fö7VÖVçFVBÂvVöÖWG'’6öæ¦V7GW&Æv2G'VRöbÆ6RæBv2&V–ær&VB2F†÷Vv‚—BvW&RG'VRö`§F†R66VæRÂæBF†RvVöÖWG'’—B6ÆÆVB6öæ¦V7GW&Â—2æ÷BFWF–ÂFòf–ÆÂ–âÆFW"(	B—BFV6–FW0§v†WF†W"vFW"7FæG2VæFW"6†–6vòw2f—'7BV&Æ–2'V–ÆF–ærà ¢¢¥BÔSRw2fÆÆ&6²—2F—66†&vVBæBäòÄ”$U%E’•2õtTBâ¢¢—G2–ç7G'V7F–öâv2Fòw&—FR¦Fö72ôÄ”$U%D”U2æÖFVçG'’6––ærF†R7V&R—2G&vâG'’–b—B6÷VÆBæ÷B&R6WGFÆVB†öæW7FÇ’à¤æ÷F†–ærv2–çfVçFVBÂæò6öæf–FVæ6RÖ÷fVBÂæBF†R7V&Rv2¢¦Ç&VG’¢¢G&vâG'’æBÇ&VG§&V6÷&FVB27V6‚–âFW‡Bf—6—F÷"&VG2âv†Bv2Ö—76–ærv2F†R&V6öâÂæBF†R&V6öâ—2æ÷r–à§F†B6ÖRf—6—F÷"Öf6–ærFW‡B(	BF†Rf÷W"v‡–7G&–æw2w&÷VæBæ§6&VæFW'2â&÷6R–âF†R7V2—0§7G&—VBg&öÒF†RFW'&–âw27FÆVæW72†6‚Â6ò—B6÷7Bæò&¶Rà ¢¢¤äB•B4õ5B4ôÔUD„”ärDõtå5E$TÒäô$ôE’tõTÄB„dRtôäRÄôô´”ärdõ"â¢ ¦FFöfVæ÷¦öæW2öcEöÖ'6‚æ§6öæ&W7FVB¢§F‡&VR6Æ–×2¢¢öâF†RöæBV÷FF–öâ2–â×66VæP¦Wf–FVæ6R(	B×W6·&B&W6Væ6VæBÖÆÆ&B&W6Væ6VvW&RGFW7FVFöâ¢§F†BV÷FF–öâÆöæR¢¢À§F†R×W6·&Bw2æ÷FR&VF–ær¢&F—&V7BWf–FVæ6Röbæ–ÖÇ2&W6VçB–âçVÖ&W'2BæÖVBÆö6F–öà¦–ç6–FRF†R66VæR&÷‚"¢â—B—2æ÷C¢—B—2Wf–FVæ6R&÷WBÆ6RBâVæ¶æ÷vâF–ÖRâ¢¤æòw&FP¦Ö÷fVB¢¢ÂæBF†B—2ÖV7W&VB&F†W"F†â6öçfVæ–VçB(	Bv†B6'&–W2GFW7FVF—2æG&V2w2¢&GV6·0¦æB×W6·&G2–âF†RÖ'6†W2"¢ÂæBF†RÖ'6†W2†RæÖW2¢¦&R¢¢F†R†&—FBF†—2¦öæRÆçG0¢†£EöÖ'6†w2W‡FVçB—2'VffW"öbF†RÖVBvFW"ÂF†R&—fW"×6†÷&R7G&—ÂæB†2æWfW"&V6†V@§F†R7V&R’âF†Ræ–ÖÂ—2GFW7FVB–âF†R†&—FBF†R66VæRG&w2æB—2æòÆöævW"GFW7FVBB¦æÖVB&Æö6²F†R66VæRG&w2G'“²F†Ræ÷FW2æ÷r6’v†–6‚öbF†RGvòF†W’ÖVâà ¢¢¥F†RvFRv2fW&–f–VBFòf–ÂÂöâf÷W"6W&FR–æ¦V7F–öç2â¢¢âVæFFVBFVfW'&ÂÂâ–æfW'&VF ¦w&FRv—F‚—G2&V6öæ–ær&Ææ¶VBÂ¦öæRçVÖ&W"æ÷F†–ærFVfW'2ÂæB6÷W&6RF†BFöW2æ÷B&W6öÇfP®(	BV6‚W†—G2v—F‚F†RF—fW&vVæ6RæÖVBÂæBF†R&W7F÷&VBf–ÆR76W2â—B†öÆG2F†R6÷'&W7öæFVæ6P¦–â¢¦&÷F‚¢¢F—&V7F–öç2Â6òf–gF‚–â×F÷vâvFW"fVGW&R6ææ÷B&RFVfW'&VBVæFFVBæBFF–æp¦VçG'’6ææ÷B÷WFÆ—fRF†RFVfW'&Â—Bw&FW2âv†–6‚¦öæW2—B6÷fW'2—2¢¦FV6Æ&VB¢¢Âæ÷B6æ–ffV@¦÷WBöbF†R&÷6Rv‡–¢&VvW‚÷fW"&÷6R&VG2Æ–¶R'VÆRVçF–ÂæÖR6†ævW2VæFW"—BÂv†–6€¦—2v†B"ÕsFv2æBv†BF†R6Öö¶Rw2÷vâ÷FW'&–çÇvFW"ö–f–ÇFW"v2à ¢¢¥fW&–f–VC¢¢¢FööÇ2ö6†V6²ç6†w&VVââ4Ôô´Uõd”Uuõ%CÖÖö&–ÆRæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6w&VVà¦v–ç7BF†RV&Æ—6†VBÖ—'&÷"â¢¥F†RFW6·F÷†Æbv2äõB'VâæBF†—2—2æ÷B6Æ–ÖVB276VB¢¢(	@¦—BæVVG2ã2Ö–çWFW2v–ç7BF†—2†&æW72w2ÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ærÂv†–6‚F†R$ôDÔw2'Và¦'VFvWB6V7F–öâ&V6÷&G2âF†—2&6VÂ6†ævW2æò&VæFW&W"f–ÆRÂæòvVöÖWG'’æBæò6ö÷&F–æFS²v†@¦—B6†ævW2F†B'&÷w6W"ÆöG2BÆÂ—2f÷W"v‡–7G&–æw2–â6–FV6"æBöæR6†ævVÆörVçG'’à ¢¢¥v†B—BF–BäõBFó¢¢¢—BÖöFVÆÆVBÂÖ÷fVBæB6—¦VBæ÷F†–ær(	BÆÂf÷W"fVGW&W2&VÖ–âFVfW'&VBà¤—BVF—FVBæò&W6V&6‚F÷76–W"‡F†÷6R&R6öÖÖ—GFVBfW&&F–ÒÂv†–6‚—2v‡’F†RF—6w&VVÖVçBÆ—fW2–à¦Fö72õ$U4T$4‚÷V&Æ–5÷7V&U÷öæBæÖF’âæB—BF–Bæ÷Bç7vW"¢¦†÷r×V6‚¢¢öbF†R7V&Rv2vWBÀ§v†–6‚—2¢¥BÔSR†"’¢¢æBæVVG2&¶Rà ¢22æWr##bÓ‚Ób(	BF†RF÷F–öâ'VÆRæ–æR&Æö6²&6VÇ27WÆ–VB'’†æB—26öFRæ÷rÂæB—B6†ævW2æ÷F†–æp ¢¢¤³#‚—2FöæR¢¢ÂæBF†R†öæW7B†VFÆ–æR—2F†B¢¦æ÷BöæR†÷W6V†öÆBÂ&ööb÷"6ö÷&F–æFRÖ÷fVB¢¢à¥6–æ6RBÔ’öâ##bÓ‚ÓRÂæ–æR&Æö6²&6VÇ2†fR&VgW6VBG&FR6V6öæB&ööbæBWfW'’öæRö`§F†VÒw&÷FRF†R&VgW6ÂF÷vâ2¦6†ö–6R&F†W"F†â'VÆR¢Â&V6W6RÖWF†öB'VÆRbv26–ÆVçBöà§F‡&VRF†–æw2Böæ6RâÆÂF‡&VR&RFV6–FVBæBGvòöbF†VÒ&Ræ÷rvFW2à ¢¢¥F†R6WGFÆVÖVçB—2W&Ö—76—fRöâF†RF&ÆRæB7G&–7BöâF†R&FR¢¢ÂFVÆ–&W&FVÇ’(	B6WGFÆ–ærÆÀ§F‡&VR6öç6W'fF—fVÇ’v÷VÆB†fR&VVâ6WF–öâG&W76VB2ÖWF†öC  ¢Ò¢¢†’’FW7G2"æB2&VBGvò$ô¤T5D”ôå2öbF†R†÷W6–ærF&ÆRÂæ÷B6WBöb—'2â¢¢F†P¢7G&–7FW"—"&VF–ær—2¢§&VgW6VB¢¢Âöâ'VÆRbw2÷vâ7FæF&B&F†W"F†âöâF7FS¢&WV—&–æp¢F†R—"&VgW6W2F†R¢¦f÷W'FVVçF‚Æ&÷W&–ær†÷W6V†öÆB¢¢…BÔBw2CvW7BöbF†R&—fW"Â&wVVB–à¢W†7FÇ’F†R&ö¦V7FVBf÷&Ò’Âv†–6‚'VÆRbæÖW22öæRöbF†R¢¦f÷W"FV6—6–öç2—G2F†—&BFW7@¢&V6÷fW'2¢¢(	BæBF†R6ÖR&w&‚6—2FW7BF†B†2Fò&RFöÆBF†Rç7vW'2—2&VfW&Væ6Rà¢v†BF†R&ö¦V7F–öç2FÖ—B—2ÖV7W&VBÂæ÷BvfVBC¢¢£#†fÖ–Ç’ÂF—f—6–öâ’—'27&÷72€¢G&FW2¢¢F†BF†—2Æ–W"†÷W6W2æöæRöbà¢Ò¢¢†–’’F†W&R•26(	BöæRF÷F–öâW"G&FRW"&Æö6²&6VÂâ¢¢&Æö6²—2â'FVf7BöbF†P¢G&v–ær&F†W"F†âVæ—BöbF†RF÷vâÂv†–6‚—2F†R&V6öâf÷"F†R6æBæ÷Bâö&¦V7F–öâFð¢—C¢v—F†÷WBöæRÂF†Rw&çVÆ&—G’öbF†RÆB6WG2F†R&FRBv†–6‚F†—26Vç7W2w&÷w2â—B—0¢Ç6òv†BÖ¶W2†’’6fR(	BF†R&ö¦V7F–öç2v–FVâ§v†–6‚¢&öög2&RVÆ–v–&ÆRÂF†R6&÷VæG2¦†÷p¢f7B¢ç’öbF†VÒÖ’Ö÷fR6÷VçBà¢Ò¢¢†––’’FW7BÖVç2F†RG&FRw2õtâ6öÖÖ—GFVBFW‡BÂæ÷BÖWF†öB'VÆR2w2Æ—7BöbVæ&÷VæFV@¢G&FW2â¢¢&V–ærVæ&÷VæFVB6—2v†W&RçVÖ&W"6ÖRg&öÓ²FW7B6·2v†WF†W"F†RçVÖ&W"—2Föð¢Æ÷râöæÇ’F†R¢¦6'VçFW'2æBÆ&÷W&W'2¢¢7FFR—BÂ6òF†RÆVæG&W76W2rC"æBF†RFV×7FW'2p¢CB&R&VgW6VB(	B¢§v—F‚F†R&VÖVG’æÖVB¢£¢&wVRF†RfÆö÷"–âF†BG&FRw2÷vâ&wVÖVçBÂg&öÐ¢F†RF÷vâÂæBF†R&öög2föÆÆ÷rà ¢¢¤&÷F‚vFW2vW&R&÷fVâFò&—FR&Vf÷&RÖW&vR¢¢Âv–ç7B×WFFVB6÷–W2öbF†R&öw&ÖÖR&F†W §F†â'’–ç7V7F–öã¢6V6öæB6'VçFW"öâ&Æµ÷6÷WF…÷vFW%÷vVÆÇ6w2CBæBÆVæG&W72öà¦&Æµ÷&æFöÇ…ög&æ¶Æ–æw2C"(	BF†RGvò&öög2æ–æR&6VÇ2&VgW6VB'’†æB(	BV6‚f–Âv—F‚F†P¦6ÆW6RæÖVBâF†RfÆö÷"&VF–6FR—2¢¦–×÷'FVB¢¢g&öÒFööÇ2öÖV7W&UöF÷F–öå÷FW7G2ç––çFòF†P¦vFR&F†W"F†â&W7FFVBÂ6òF†R&W÷'BæBF†RvFR6ææ÷BG&–gB'B&÷WBv†BfÆö÷"—2à¥F†BFööÂÇ6òæòÆöævW"FVÆÇ2—G2&VFW"F†RVW7F–öâ—2÷VâÂv†–6‚—BF–B–âf÷W"Æ6W2à ¢¢¤ÆÂ#7FæF–ær&Æö6²F÷F–öç2Ç&VG’ö&W–VBF†R6¢¢Âv†–6‚—2v‡’æ÷F†–ærÖ÷fVBâF†RfÇVP¦—2F†BF†RFVçF‚&Æö6²6ææ÷BG&–gBà ¢¢¥v†Bv2æBv2äõB'Vââ¢¢â÷FööÇ2ö6†V6²ç6†(	BF†RFWbvFR(	B—2¢¦w&VVâ¢¢à¦æöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2'VâB¢¦Öö&–ÆRƒ3“ƒsƒ’öæÇ’¢£²F†RFW6·F÷†Æb¢§v2æ÷@§'Vâ¢¢Â&V6W6R6–ævÆRf÷&Vw&÷VæB6öÖÖæBöâF†—2'VææW"—26VBBFVâÖ–çWFW2æBF†RFW6·F÷ ¦†ÆbF¶W2&÷WBF†—'FVVâ„³#ÂÖV7W&VB’âF†—2&6VÂ6†ævW2öæRWF†÷&VB¥4ôâw2ÖWF†öF&÷6P¦æBGvòFööÇ3¢¢¦æò&VæFW&W"f–ÆRÂæò&V6÷&BÂæòvVöÖWG'’Âæò6ö÷&F–æFRÂæòÖFW&–Â¢¢â6’6ð§&F†W"F†â–×Ç––ær&÷F‚†ÇfW2&âà ¢22æWr##bÓ‚Ób(	BöæRæWr†÷W6V†öÆB&VæÖVBs2öb2–çfVçFVB&W6–FVçG2Âæ÷BF†RrÓ#RVÆWfVâ&6VÇ2&W÷'FV@ ¢¢¤³#—2FöæRâ¢¢FööÇ2övVæW&FUö–æfW'&VEöæÖW2ç–FVÇBV6‚†6öÖ×Væ—G’Â6W‚–ööÂ&÷VæB¢¦'¦–æFW‚¢¢Â6òâ–çfVçFVBæÖRv2gVæ7F–öâöb†÷rÖç’V÷ÆR6÷'FVB†VBöb–÷RâVÆWfVâ&6VÇ0¦ÖV7W&VBF†R&W7VÇF–ær6‡W&â–â76–æræB&W÷'FVBr×FòÓs#²WfW'’öæRöbF†VÒv26–ævÆP§6×ÆRB6–ævÆR&&—G&'’ö–çB–â†6‚÷&FW"âFööÇ2öÖV7W&UöæÖUö6‡W&âç–—2F†P¦–ç7G'VÖVçB(	B—B–ç6W'G27–çF†WF–2†÷W6V†öÆB¢¦–âÖVÖ÷'’¢¢Â&R×'Vç2F†RÆÆö6F÷"æB6÷VçG2v†ð¦vWG2&VæÖVB(	BæB÷fW"¢£#C–ç6W'F–öç27&÷72ÆÂ6—‚G&FW2¢¢F†RF—7G&–'WF–öâ—2æ÷B6VçG&V@¦æV"f–gF‚öbF†RÆ–W#¢ÖVâ¢£CãB¢¢f÷"6'VçFW"Â¢§v÷'7Bs2öb2¢¢ÂæBöæÇ’¢£öbC¢ ¦6'VçFW"&ö&W2&VæÖVBæö&öG’à ¢¢¥F†RÆÆö6F÷"—2æ÷r–ç6W'F–öâÖÆö6Ã¢v÷'7Böb2öâF†R6ÖR#C&ö&W2ÂÖVâBãbâ¢¢V6€§W'6öâ†2F†V—"÷vâFWFW&Ö–æ—7F–2÷&FW&–æröbF†RööÂæB6Æ–×2F†RÆV7B×W6VBæÖRF†W’&P§W&Ö—GFVBÂ6òæÖRFWVæG2öâv†ò–÷R6öÆÆ–FRv—F‚&F†W"F†âöâ†÷rÖç’V÷ÆR&V6VFR–÷Rà¤F†—&BöbF†R–×&÷fVÖVçB6öÖW2g&öÒ¢§VçvVÆF–ærF†Rv—fVâæÖRg&öÒF†R7W&æÖR¢£¢&WVFV@¦v—fVâæÖR—2v†BF÷vâÆöö·2Æ–¶RæB6Æ–×2æ÷F†–ærÂ6ò—B—2æ÷rV6‚W'6öâw2f—'7@§&VfW&Væ6Rv—F‚æòÆVFvW"BÆÂÂv†–ÆR7W&æÖR(	Bv†–6‚&VG22¶–ç6†—(	B¶VW2F†RÆVFvW"æ@§F†RfÆö÷"'VÆRà ¢¢¥F†R&W6–GVÂ—2F†RôôÂÂæBF†R&W÷'B&÷fW2F†B&F†W"F†â76W'F–ær—Bâ¢¢V6‚&ö&P§&–çG2—G2'V6¶WBw2&W77W&RâB¢£ãG‚¢¢‡ööÂv—F‚&ööÒ’â–ç6W'F–öâ&VæÖW2¢¦BÖ÷7BöæR¢ §W'6öâ(	BÆ—FW&ÆÇ’³#w266WFæ6R7&—FW&–öââB¢£"ã7‚¢¢ƒ3b7W&æÖW2FVÇBFòs2ÖVâ’—@§&VæÖW2WFòFVâÂ&V6W6RF†W&R—2æò7&RæÖRBF†RfÆö÷"â¢¥FVâ&VæÖW2B"ã7‚—2ööÀ§F†B—2Föò6ÖÆÃ²FVâBãG‚v÷VÆB&RâÆÆö6F÷"F†B—27F–ÆÂæ÷BÆö6Ââ¢¢v–FVæ–ærF†P§ööÇ2—2Wf–FVæ6Rv÷&²(	BÖ÷&RæÖVBƒ3R6†–6vöç2÷WBöbæG&V2æBF†R&öÆÇ2(	Bæ÷BGVæ–æp¦¶æö"ÂæBB7‚&W77W&RF†R&W6–GVÂv–ÆÂ6Æ–Ö"v–âà ¢¢¤'VrF†Rf—‚W‡÷6VC¢¢¢VçvVÆF–ærF†RGvò†ÇfW2ÆWBGvòV÷ÆRG&rF†R6ÖR—"ÂæBF†P¦f—'7B'Vâ6†—VB¢§GvòÇf‚†7F–æw2¢¢âF†B—2&VgW6VB÷WG&–v‡Bæ÷ræBÆÂ2gVÆÂæÖW2&P¦F—7F–æ7B(	BG'VR'’66–FVçB&Vf÷&RÂG'VR'’76W'F–öâæ÷rà ¢¢¥F†RöæR×F–ÖR6÷7B—2F†Rv†öÆRÆ–W"¢£¢¢£2öb2&VæÖVB7&÷72†÷W6V†öÆBf–ÆW2¢¢À§&V6÷&FVB2¢¤Ã¢¢â—B–çfVçG2æ÷F†–æræWr(	B6ÖRööÇ2Â6ÖRw&FW2Â6ÖRæÖUö&6—6 ¦6—FF–öç2æBæ÷FW3²F–ffW&VçB–çfVçFVBæÖR—2F†R6ÖR6Æ–Ò&÷WBF†R6ÖRæö&öG’à ¢¢¥v†Bv2æBv2äõB'VâÂ7FFVB&F†W"F†â–×Æ–VBâ¢¢â÷FööÇ2ö6†V6²ç6†(	BF†RFWbvFR(	B—0¢¢¦w&VVâ¢¢Â–æ6ÇVF–ærF†RæWr7FW†ÖV7W&UöæÖUö6‡W&âç’ÒÖvFVÂã"2’æB6ö×–ÆU÷66VæRç¢ÒÖÆÂÒÖ6†V6¶÷fW"F†R33&VvVæW&FVB6–FV6'2âæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2'Vâ@¢¢¦Öö&–ÆRƒ3“ƒsƒ’öæÇ’Â#B76VBòf–ÆVB¢£²F†RFW6·F÷†Æb¢§v2æ÷B'Vâ¢¢Â&V6W6R§6–ævÆRf÷&Vw&÷VæB6öÖÖæBöâF†—2'VææW"—26VBBFVâÖ–çWFW2æBF†RFW6·F÷†ÆbF¶W0¦&÷WBF†—'FVVâ„³#ÂÖV7W&VB’âæ÷F†–ærf—7VÂ6†ævVB†W&R(	BF†RF–fb—2æÖR7G&–æw2–à§&V6÷&G2æB6–FV6'2Âæò&VæFW&W"f–ÆRÂæòvVöÖWG'’ÂæòÖFW&–ÂÂæò6ö÷&F–æFR(	B6òF†R&—6²F†P¦FW6·F÷†Æb6÷fW'2—2æ÷BF†R&—6²F†—2&6VÂ6'&–W2â6’6ò&F†W"F†â–×Ç––ær&÷F‚†ÇfW0§&âà ¢22æWr##bÓ‚Ób(	BF†RF÷vâ†2æò6†–ÖæW’ÖFW&–ÂÂæBæò&V6÷&Bç—v†W&R6—2v†B&ööb—2ÖFRö` ¢¢¥"Õs&¢¢ÂF†RÖFW&–Â6†VWBÂ—2w&—GFVã¢Fö72õ$U4T$4‚öÖFW&–Ç2æÖFâ—B—2ÖV7W&VB÷WBö`§F†R6†—VBtÄ'2&F†W"F†â&VBöfbF†RvVæW&F÷'2Â&V6W6RF†R6÷W&6RæBF†R'—FW2†fP¦F—6w&VVB†W&R&Vf÷&Râ¢£33B76WG26''’Ã3S2ÖFW&–Â6Æ÷G2Â&W6öÇf–ærFò3"æÖW2ÂC&6P¦6öÆ÷W'2æB‚&÷Vv†æW72fÇVW2â¢¢WfW'’öæR—2ÖWFÆÆ–4f7F÷"ÂF÷V&ÆU6–FVFÂõTVÀ¦æB6'&–W2æòÖöbç’¶–æB(	B*s—FVÒ’w2'¦W&òFW‡GW&W2ç—v†W&R"—26öæf—&ÖVBBF†R'—FP¦ÆWfVÂÂæ÷BV÷FVBà ¢¢¥Gvòf–æF–æw2&Æö6²FW‡GW&–ær÷WG&–v‡BÂæBæV—F†W"—2&VæFW&–ær&ö&ÆVÒâ¢  ¢Ò¢¥F†R6†–ÖæW’—2æ÷BÖFW&–Â–âF†—2&ö¦V7Bâ¢¢g&ÖUöGvVÆÆ–ævÂg&ÖU÷7F÷&Vg&öçFæ@¢ÆöuöGvVÆÆ–ævÆÂ'V–ÆBF†V—"7F6·2v—F‚Õõ$ôôfÂ6ò¢£#’6†–ÖæW’7F6·2öâ“’'V–ÆF–æw0¢&R–çFVBv—F‚F†R&ööbw26öÆ÷W"¢¢Âã3BÂã3Âã#vB&÷Vv†æW72ã“âF†R“–æfW'&V@¢Æ6V†öÆFW'2ÂÖVçv†–ÆRÂ6†—&VÂÆ6V†öÆFW%ö6†–ÖæW•ö'&–6¶âF†RF÷vâ†2'&–6°¢6†–ÖæW’ÖFW&–ÂæBF†R&6†WG—R'V–ÆF–æw2Fòæ÷BW6R—B(	BæBÆöuöGvVÆÆ–ævw2÷và¢Fö77G&–ær&wVW2F†Bg&öçF–W"7F6²—27F–6²ÖæBÖ6Æ’÷"f–VÆG7FöæRÂF–ffW&VçBö&¦V7@¢g&öÒg&ÖVB†÷W6Rw2'&–6²7F6²Âv†–6‚&VæFW'2–FVçF–6ÆÇ’Fò—Bâ÷VæVB2¢¥"Õs&2¢¢Âæ@¢—B÷Vç2v—F‚&W6V&6‚VW7F–öâ&F†W"F†âÆWGFRà¢Ò¢¤æò&V6÷&B7FFW2&ööb6÷fW&–ærâ¢¢3R&V6÷&G27FFR&ööb§G—R¢æB3’—F6ƒ°¢¢§¦W&ò¢¢6’v†BF†R&ööb—2ÖFRöbâF†R&ö&B&ööb÷WF'V–ÆF–æv&wVW2f÷"—26W&FV@¢g&öÒ6†–ævÆRf–VÆB'’¢£ã2öb&÷Vv†æW72æBæ÷F†–ærVÇ6R¢¢(	B–FVçF–6Â6öÆ÷W"Â–FVçF–6À¢æÖRÂ–âF†R6†—VB'—FW2âF†R&W÷6—F÷'’w2öæRF—&V7BGFW7FF–öâÂF†Ræ÷'F‚6–FR66†ööÂw0¢'6†VWFVBæB6†–ævÆVB&ööb"Â—2&VB'’æ÷F†–ærâ&öög26ææ÷B&RFW‡GW&VBVçF–ÂâGG&–'WFP¢W†—7G2Fò6VÆV7BF†R6÷fW&–ærÂæBF†B—266†VÖ6†ævR7&÷723R&V6÷&G2à ¢¢¤æBöæRFö7VÖVçFVBf7B—26öÖÖ—GFVBÂ6÷'&V7BÂæB&VæFW&VB'’æ÷F†–ærâ¢¢6ö'vV%ö67FÆV ¦6'&–W26ÆFF–æs¢6Æ&ö&E÷'E÷v•÷WÂ¢¦GFW7FVF¢¢Â6÷W&6VBFòæG&V5óƒƒE÷c(	@¤Ff–BÖ4¶VRw2'F†RvVæ7’Ö†÷W6R&V–ærgFW'v&B6Æ&ö&FVB'Bv’W"â—B—2¦ÆöuöGvVÆÆ–ævÂv†–6‚FöW2æ÷B&VB6ÆFF–ævBÆÂÂæBF†RfÇVR—2æ÷BWfVâ–à¦4ÄDD”äu6â6ÆFF–æv—27FFVBöâ#r&V6÷&G2æB&VBöâ#"à ¢¢¥"Ôsw2'F†W&R—2æò&÷Vv†æW72f&–F–öâç—v†W&R"—26÷'&V7FVBÂæBF†R6÷'&V7F–öâ6†ævW0§v†Bs"'V–ÆG2â¢¢&WGvVVâ7W&f6W2F†W&R&RÇ&VG’‚&wVVBfÇVW27ææ–ærãRFòãà¥v†BFöW2æ÷BW†—7B—2f&–F–öâ§v—F†–â¢7W&f6S¢WfW'’7V&RÖWG&RöbWfW'’vÆÂ†2öæP§&÷Vv†æW72Âv†–6‚—2v‡’æ÷F†–ær&VG22–çFVBÂvVF†W&VB÷"vWBâ¢¥F†RFVÆ—fW&&ÆR—2§&÷Vv†æW72ÖÂæ÷B&WGFW"6öç7FçG2¢¢(	BFòæ÷B7VæB&÷VæB&R×GVæ–ærF†R‚çVÖ&W'2à ¢¢¥v†Bv2äõB'VâÂ7FFVB&F†W"F†â–×Æ–VBâ¢¢F†—2&6VÂ6†ævVBæò6öFRÂæò&ÖWFW ¦æBæò&V6÷&BÂ6òæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2¢¦æ÷B¢¢'VâBV—F†W"f–Ww÷'Bæ@¦FööÇ2÷V&Æ—6‚ç6†&öGV6VBæòÖ—'&÷"6†ævR&W–öæBF†R6†ævVÆörââ÷FööÇ2ö6†V6²ç6†76V@¦w&VVâÂæB—B—2F†RFWbvFRâæ÷F†–ær†W&R†2&VVâ&VæFW&VBÂ&V6W6RF†W&R—2æ÷F†–ær†W&P§Fò&VæFW"à ¢22æWr##bÓ‚Ób(	B'V–ÆF–ær†2&VVâF¶Vâ÷WBöbF†RF÷vâÂæBF†RF÷vâw2V&Æ–2'V–ÆF–æw2&RF‡&VP ¢¢¥BÔ“2†’â¢¢F†R&öw&ÖÖR66†VGVÆW26—‚6—f–2÷"V&Æ–2×6W'f–6R&öög2æBWfW'’vVæW&F÷"†0§&VgW6VBFòÖ72öæR6–æ6RÃ“2ÂöâF†Rw&÷VæBF†BF†R&6†WG—R&V†–æBF†RfÖ–Ç’7V·2öæÇ¦v'&—6öâv÷&G2âF†R&VgW6Â—2æ÷rF†R&W6V&6‚–ç7FVBâ¢¤öâƒ3RÓrÓF†RF÷vâw2V&Æ–0¦'V–ÆF–æw2v—F‚&ööb&RF‡&VR(	BÆöuö¦–ÆÂ6÷Væ6–Åö†÷W6VÂ6†–6võöÆ–v‡F†÷W6Uóƒ3&(	Bæ@§F†—2&ö¦V7BÇ&VG’†BÆÂF‡&VRâ¢¢W7G&•÷Væ—2V&Æ–2æB&ööfÆW72âF†RVçVÖW&F–öâ—0¦Fö72õ$U4T$4‚ö6—f–5÷V&Æ–5ö'V–ÆF–æw5óƒ3RæÖFÂæBWfW'’6—FF–öâ–â—B—2æG&V3¢¢¦æòæWp§6÷W&6Rv2æVVFVBæBæöæRv2–çfVçFVBâ¢  ¢¢¥F†Rf–æF–ær—2F†Rf÷W'F‚'V–ÆF–ærâF†R6÷W'BÖ†÷W6Rv2æ÷B'V–ÇB–WBâ¢¢33"7G'V7GW&W2&W6öÇfV@¦–çFòF†Rƒ3R66VæRæB33Fó²6ööµö6÷VçG•ö6÷W'F†÷W6Uóƒ3V—2&RÖFFVBFòF†RfÆÂæB&W6öÇfW0¦–çFòƒ3b–ç7FVBâ—G2&V6÷&B6–BÂBÆVæwF‚æB†öæW7FÇ’ÂF†Bæ÷F†–ær—B†B&V6†VBf—†VB¦ÖöçF‚ÂæB&V6öæVBg&öÒfÆB&–÷"÷fW"GvVÇfRÖÖöçF‚v–æF÷rF†BF†R'V–ÆF–ærv2&÷WB†Æ`¦Æ–¶VÇ’Fò&R7FæF–ærâ¢¥F†Rv–æF÷rv2æWfW"GvVÇfRÖöçF‡2â¢¢æG&V2w2F÷vâ×W&–öBæ'&F—fS ¢¢$GW&–ærF†RfÆÂöbF†R–V"ƒƒ3RÂ’öæR×7F÷'’æB&6VÖVçB'&–6²6÷W'BÖ†÷W6Rv2W&V7FVBöà§F†Ræ÷'F†V7B6÷&æW"öbF†R7V&RÂöâ6Æ&²æB&æFöÇ‚7G&VWG2"¢‡66ââ3c’’â†—26‡&öæöÆöw¦Æ—7G2—BVæFW"ƒ3RB¢¤æ÷fVÖ&W"¢¢‡66ââ3r’âæBF†R6÷VçG’&V6÷&FW"¢'&VÖ÷fVB†—2öff–6P§F÷v&BF†RVæBöbö7Fö&W"FòF†RæWr'V–ÆF–ær&V6VçFÇ’W&V7FVB'’F†R6÷VçG’öâF†RV&Æ–0§7V&R"¢‡66ââ3R’âF‡&VR7FFVÖVçG2(	Bæ'&F—fRÂâ–æFW‚æB&–öw&‡’(	BæBæ÷BöæR—0¦V&Æ–W"F†âF†RfÆÂà ¢¢¥F†RFF6WB†BÇ&VG’6–B6òÂ–âæ÷F†W"f–ÆRÂf÷"f÷W"F—2â¢¢F†R‡—6–6Â×&ööb&V6öæ6–Æ–F–öâv—fW2F†—2&V6÷&B&ööeö6÷VçC¢v—F‚F†R&V6öæ–ær¢%&öGV7F–öâ6‡&öæöÆöw’Æ6W26öç7G'V7F–öâ–âfÆÂƒ3S²æò6÷W'F†÷W6R&ööb6†÷VÆB7FæBöâ§VÇ’"¢(	B6öÖÖ—GFVB##bÓ‚Ó"ÂöæRF’gFW"F†R7G'V7GW&R&V6÷&BF†B7FööBF†R'V–ÆF–æröâF†R7V&Râ6òg&öÒ"VwW7BöæRFö7VÖVçB–âF†—2FF6WB†VÆBF†R6÷W'BÖ†÷W6RVæ'V–ÇBv†–ÆRæ÷F†W"G&Wr—BÂæBæ÷F†–ær&VBF†RGvòFövWF†W#²F†RvÆ·F‡&÷Vv‚w2÷vâ&VÆV6Ræ÷FW2WfVâ6'&–VBF†R&V6öæ6–Æ–F–öâw2&VF–ær÷WBFòf—6—F÷'2(	B¢&6÷W'F†÷W6RF†Bv2æ÷B'V–ÇBVçF–ÂF†RWGVÖâ"¢(	Bv†–ÆRF†RvÆ·F‡&÷Vv‚G&Wr—Bâ¢¥F†RöæRF†Bv2&–v‡B—2F†RöæRv—F‚æò6—FF–öâBÆÂâ¢¢F†R&V6öæ6–Æ–F–öâw2'&öGV7F–öâ6‡&öæöÆöw’"6—FW2æ÷F†–æs²F†R&V6÷&B6—FW2æG&V2æB6—2F†R÷÷6—FRÂ&V6W6Rv†B—B6—FVBv26F–öâà ¢¢¥F†R6—FF–öâF†R&V6÷&B†Bv2–7GW&Râ¢¢—B6—FVB¢&6V7F–öâ†VFVBuD„Rd•%5@¤4õU%BÔ„õU4RârB66ââ3s2"¢â66ââ3s2—2ÄDS²F†÷6Rv÷&G2&RâVæw&f–ærw26F–öâÀ§&–çFVBVæFW"¢$6÷—&–v‡B6V7W&VB'’âBâæG&V2ÂƒƒBâ"¢F†R&w&‚F†B6'&–W2F†RFFR—0¦f÷W"66âvW2V&Æ–W"âF†—2—2F†R6V6öæBF–ÖR–âF†—2&ö¦V7B6—FF–öâ†2&W6öÇfVBFò¦†VF–ær&F†W"F†âFò6VçFVæ6RÂæB—B—2F†Rv†öÆR6W6S¢WfW'’vFR†W&R6·2v†WF†W"¦'V–ÆF–ær—2–ç6–FR—G2Æ÷BÂ6ÆV"öbF†R&öGv’ÂöâW&Ö—GFVBw&÷VæBæB6ÆV"öb—G2æV–v†&÷W'2à¥F†RvFRF†B6·2v†WF†W"—BW†—7FVB–WB—2F†RFFRvFRÂæB&ævRWF†÷&VBg&öÒ6F–öà§76W2—BW&fV7FÇ’à ¢¢¥GvòöbF†R&V6÷&Bw2÷vâ†VFvW2&R6WGFÆVBæB&÷F‚6’—Bv2&WGFW"F†â—B¶æWrâ¢¢—Bv&æV@§F†BæG&V2w2æ÷'F‚ÖV7B6—F–ær&—2F†Rƒ3r%T”ÄD”är"æBÖ–v‡B&R6öçFÖ–æF–ærâƒ3R&V6÷&@®(	BæG&V2v—fW2F†B6÷&æW"FòF†—2öæRÂ–âF†R6VçFVæ6RF†BFFW2—Bâ—B'VÆVB÷WB'&–6²&V6W6P¢'F†Rf—'7B'&–6²'V–ÆF–ær–â6†–6vò—2ƒ3r"(	BF†B—2F†Rf—'7B'&–6²„õU4RÂæBæG&V26ÆÇ0§F†—26÷W'BÖ†÷W6R'&–6²â¢¤æV—F†W"—2Æ–VBâ&÷F‚æVVBF†R&¶R¢¢Â&V6W6R6†ævVBf÷&ÒfÇVP§7FÆW2F†RÖW6ƒ²F†W’&R&V6÷&FVBöâF†R&V6÷&B2ÖVæFÖVçG2à ¢¢¤æòæöç–Ö÷W2&ööbÖ’6Æ–ÒFò&RV&Æ–2'V–ÆF–ærÂæBF†B—2æ÷r76W'FVBâ¢ ¦FööÇ2öÖV7W&Uö–ç7F—GWF–öæÅö6Æ–×2ç–'Vç2–â6†V6²ç6†v–ç7BWfW'’6öÖÖ—GFVB&V6÷&B&F†W §F†âöæÇ’F†RöæW2vVæW&F÷"—2&÷WBFòw&—FR(	B¢¦'6öÇWFR¦W&ò¢¢f÷"F†Rv÷'6†—æB6—f–0¦fÖ–Æ–W2Â&V6W6RF†W’&RVçVÖW&&ÆRÂæB¢§&F6†WBBöæR¢¢f÷"F†R66†ööÇ2ÂæÖ–ærF†R6–ævÆP¦æöç–Ö÷W2æ÷'F‚F—f—6–öâ66†ööÂÃ“2&V6÷&G2&F†W"F†âFVÆWFW2âÆÂF‡&VR†ÇfW2vW&R'&ö¶Và¦FVÆ–&W&FVÇ’&Vf÷&RF†RvFRv2G'W7FVBà ¢¢¥v†B6Æ÷Bv÷VÆB†fR&VVâ7VçBöâ—2æ÷B'V–ÆF–ærâ¢¢F†R7&÷77vÆ²6—2F†RfÖ–Ç’7ç0¢¢&¦–Âö&Æö6¶†÷W6S²Væv–æR÷6W'f–6S²FFVBöff–6W2"¢ÂæBWfW'’FFVBöff–6R–â6†–6vòF†@§7VÖÖW"v2&ööÒ–â6öÖV&öG’w2&—fFR&VÖ—6W2âF†RVæ—FVB7FFW2ÆæBöff–6Rv2÷Vâg&öÒÖ£ƒ3RæBG&ç67F–ær&VV&–Vâw2&RÖV×F–öâf÷W"vVV·2&Vf÷&RF†R66VæRFFR(	BæB—Bv2&öö×2öà§F†RV7B6–FRöbÆ¶R7G&VWBÂv—F‚æG&V2æ÷F–ærF†BF†R&Vv—7FW"æB&V6V—fW"¢'vW&RW7VÆÇ’@§F†V—"&—fFRöff–6W2"¢âF†R÷7Böff–6Rv26÷VçFW"–â†övâw27F÷&RâF†R6÷VçG’w2÷vâöff–6W'0§vW&R&—fFRVçF–ÂÆFRö7Fö&W"âF‡&VRwV&G2FFVBFòFFöW†6ÇW6–öç2æ§6öæÂæ@¦f—'7Eöf—&UöVæv–æUö†÷W6VÖVæFVB&V6W6R—BFFVBF†RTät”äRv†–ÆRF†R„õU4R—2ÆFW"7F–ÆÂà ¢¢¥v†B—2äõBFöæRÂæB—B—2F†RçVÖ&W"â¢¢F‡&VRöbF†R6—‚“26Æ÷G2&R6÷VçBöbæ÷F†–ærÂæ@§F†RF&vWB7F–ÆÂ6—26—‚âF†R–çfVçF÷'’w2&—F†ÖWF–2—26Æ÷6VB(	BfÖ–Ç’F&vWG27VÒ–çFð¦F—7G&–7BÖw&÷W&÷w2Â&÷w2–çFòF—7G&–7BF&vWG2ÂF—7G&–7G2–çFò&ööe÷F÷FÃ¢ccVÂæ@¦&V6öæ6–ÆUóccRç–76W'G2ÆÂF‡&VR(	B6òF†RF‡&VR6ææ÷B6–×Ç’&R&VÖ÷fVBâF†RGvòW†—G2&P§GvòF–ffW&VçB6Æ–×2&÷WBF†RF÷vâƒcc"&öög2Â÷"F‡&VR&öög2F†BvW&Ræ÷B6—f–2’ÂF†R&W6V&6€§6WGFÆW2æV—F†W"ÂæB6†ö÷6–æröæRv÷VÆB–çfVçBW†7FÇ’F†R¶–æBöbvw&VvFRF†—2&6VÂ§W7@§&VÖ÷fVBâ¢¥BÔ“2†"’Â&Æö6¶VBöâF†R÷væW"â¢¢¢‚¢¤4Äõ4TB##bÓ‚Ó#r2F–6¶WBBÓ3"Â&÷WFR(	@§F†RF÷FÂ—2cc"â&VBF†BVçG'’BF†RF÷öbF†—2f–ÆR&Vf÷&RV÷F–ærç’çVÖ&W"–âF†—0§&w&‚â¢¢’¢Ç6òVæÖ÷fVC¢W7G&•÷Væw2†6R–B7F–ÆÂ&VG0¦Våóƒ36gFW"—G2–V"v26÷'&V7FVBFòƒ3"Â&V6W6R†6R–B—2†Æböb&¶VB76WBw0¦f–ÆVæÖRà ¢22##bÓ‚Ób(	BF†R'V–ÆF–æw2–âF†R7G&VWG2&RG&vâw&öærÂæ÷BÆ6VBw&öærÂæBF†RF÷vâw2vV÷&VfW&Væ6R—2W†öæW&FV@ ¢¢¤³3†"’¢¢ÂF†RGG&–'WF–ær†ÆbÂæB—BÖ÷fVBæ÷F†–ærâ³3†’ÖV7W&VB#’'V–ÆF–æw2Æ–æp¦ÆGFVB6÷'&–F÷"æBÆVgBF†RFVW6ÇW7FW"v—F†÷WB6W6RâF†R6W6R—2æ÷r6öÖÖæBÀ¦FööÇ2öÖV7W&Uö6÷'&–F÷%ö–çG'W6–öâç’Ò×&VfÆV7Fà ¢¢¥F†R7W7V7BF†—2&ö¦V7BæÖVB—2&VgWFVBÂ'’&—F†ÖWF–2â¢¢6÷WF‚vFW"—2vV÷&VfW&Væ6V@§F‡&÷Vv‚ÖöFW&âv6¶W"G&—fRÂv†–6‚v2'V–ÇBöâÖFRw&÷VæBÂ6òF—7Æ6VB6VçG&VÆ–æRv÷VÆ@¦F—7Æ6RWfW'’&V6÷&BöâF†B7G&VWBÆ–¶Râ—BFöW2æ÷C¢F†R2FVW6÷WF‚vFW"æ6†÷'0§7FæB¢£ãcN(	3Rã3Ò¢¢g&öÒF†R6öÖÖ—GFVB6VçG&VÆ–æRv–ç7BÆGFVB†Æb×v–GF‚ö`¢¢£"ã“"Ò¢¢âF†R6÷'&–F÷"æBF†RÆ6VÖVçG2w&VRFò&÷WBÖWG&RÂF†RF—6w&VVÖVçB†0¢¢¦&÷F‚6–vç2¢¢ÂæBF—7Æ6VÖVçBF†BW‡Æ–æVBBãS(	3‚ãrÒ–çG'W6–öâv÷VÆB†fRFò&P£BãS(	3‚ãrÒà ¢¢¥F†R6W6R—2Gvò6öçfVçF–öç2F†BvW&RæWfW"&V6öæ6–ÆVBâ¢¢F†RFW&—fF–öâ6öçfVçF–öâWG0¦&V6÷&Bw2ö–çBöâ—G2e$ôåDtR(	BF†R÷6—F–öâæ÷FW26’¢&öfg6WB"ã"ÒÂ†Æbâƒg@§ÆGFVB7G&VWB"¢âF†RG&v–ær6öçfVçF–öâWG2Æö6ÂƒÂ–BF†RöÇ–vöâw2Ö–æ–×VÒ6÷&æW"À§6òF†R&öG’w&÷w2æ÷'F‚æBV7Bg&öÒF†Bö–çC²¢£33öbF†R3326öÖÖ—GFVBfö÷G&–çG2Fð¦—Bâ¢¢6÷WF‚×6–FR'V–ÆF–ærv—F‚—G2ö–çBöâF†R6÷WF‚¶W&"—2F†W&Vf÷&RG&vâ–çFòF†P§&öGv’¢¦'’—G2÷vâgVÆÂFWF‚¢¢âÆÂ2FVW6÷WF‚vFW"&V6÷&G2FV6Æ&RF†R6÷WF‚6–FRæ@¦ÆÂ2&RG&vâæ÷'F‡v&Bg&öÒF†R¶W&#²7&÷72F†Rv†öÆRF&ÆRÂ¢¦ÆÂrFVW&V6÷&G2†fP§F†V—"&öG’G&vâF÷v&BF†R7G&VWBg&öÒF†V—"÷vâæ6†÷"¢¢â&VfÆV7F–ærV6‚&öG’&÷WB—G0¦÷vâö–çBF¶W2¢£"öbF†RrVæFW"Ò¢¢Âf—fRöbF†VÒFòW†7FÇ’¦W&òâ³3†’w2&V6VçG&–æp§v2F†Rw&öær÷W&F–öâöâF†R&–v‡B7W7V7B(	B—BÖ÷fW2&öG’†Æb—G2FWF‚ÂæB6ææ÷@¦6ÆV"fVÇBv†÷6R6—¦R¦—2¢—G2FWF‚à ¢¢¥F†R6†ÆÆ÷rF–Â—2ç7vW&VBæB—2æ÷BFò&Rf—†VBâ¢¢öæ6R&öG’—2G&vâöâF†R6÷'&V7@§6–FRöb—G2÷vâö–çBÂv†B—2ÆVgB–âF†R&öGv’¢¦—2†÷rf"F†Bö–çB7FæG2–ç6–FRF†P¦6÷'&–F÷"¢¢(	BFòv—F†–â¢£ãÒ¢¢÷fW"F†R6—‚&V6÷&G2F†RÆr6÷fW'2â6òF†RGvòFW&×2&P§6W&&ÆRæBVæWVÃ¢F†RG&v–ærFW&Ò—2'V–ÆF–ærw2FWF‚ÂBãS(	3‚ãrÓ²F†Rö–çBFW&Ò—0¢¢£ã3^(	3ãc’Ò¢¢Âv†–6‚—2v†BFW&—fVB6÷'&–F÷"æB†æB×G&6VB6VçG&VÆ–æRF—6w&VR'’à¦G&VÖöçEö†÷W6UóÂW†6†ævUö6öffVUö†÷W6VæBvW7FW&åö†÷FVÆ&RF†V—"ö–çBw2VæWG&F–öà¦æBæ÷F†–ærVÇ6RÂæBF†V—"&öF–W2&R¢¦Ç&VG’G&vâ6÷'&V7FÇ’¢¢(	B&VfÆV7F–ærF†VÒ6VæG0§F†VÒ"Ò–çFòF†R&öBÂv†–6‚—2F†R6†V6²F†BF†RÆr—2&÷WBF†Rö–çBâGvVÇfRçVFvV@¦'V–ÆF–æw2v÷VÆB†fR&÷Vv‡Bæ÷F†–ærà ¢¢¤'&–FvR–â7G&VWB—2æ÷B'V–ÆF–ær–â7G&VWBâ¢¢6Æ÷Vv…öÆöuö'&–FvV—2æ÷p¦6FVv÷&—6VB27G&VWBgW&æ—GW&R(	BFW&—fVBg&öÒ—G2÷vâ&6†WG—R¦æB¢gVæ7F–öâÂæWfW"g&öÐ¦Æ—7Böb–G2(	BæB—G2&÷r7F—2–âF†RF&ÆRÂ–âF†R&6VÆ–æRæBVæFW"F†R&F6†WBâF†P¦W†V×F–öâw2ö'f–÷W2'W6R—2Fò&VÆ&VÂ7F÷&R2'&–FvRÂ6òF†RvFR&VgW6W2ç’6FVv÷'¦6†ævS²V6µ÷7F÷&Vv2F—6wV—6VB2'&–FvU÷F–Ö&W&7&÷76–ær&Vf÷&RF†R'VÆRv2G'W7FV@¦æBF†RvFR6Vv‡B—Bà ¢¢¥v†B—2äõBFöæRâ¢¢æ÷F†–ærv2&VG&vââF†R&W—"6†ævW2fö÷G&–çG2Â6ò—B6†ævW2WfW'¦ffV7FVBÖW6‚æBæVVG2&¶RF†R–×&÷fR'VææW"6ææ÷BFò(	BF†B—2¢¤³3†2’¢¢âF‡&VRFVW §&V6÷&G2&Ræ÷BF†Rg&öçFvRfVÇBæB&RæÖVB&F†W"F†âfW&vVB–ã ¦æWv&W''•öFöÆU÷v&V†÷W6VÂv†÷6Rö–çB—2rãÒ–ç6–FRF†R6÷'&–F÷"æBv†÷6R÷vâæ÷FR6—0¦—G2&æ²—2F—7WFVC²†övå÷7F÷&VÂFW&—fVBFòF†RÆ¶RôÖ&¶WB§Væ7F–öâBF†RvVFvS²æ@¦FV×ÆUö'V–ÆF–ævÂv†–6‚–×&÷fW2'WBFöW2æ÷B6ÆV"â¢¤æò6ö÷&F–æFRÂF–ÖVç6–öâÂfö÷G&–çB÷ ¦6öæf–FVæ6RÖ÷fVBÂæBæ÷F†–ærv2–çfVçFVBâ¢  ¢22##bÓ‚Ób(	B#’'V–ÆF–æw2&RG&vâ7FæF–ær–âF†RF÷vâw2÷vâ7G&VWG2ÂæBWfW'’öæRöbF†VÒv2Æ6VB'’†æ@ ¢¢¤³3†’¢¢ÂF†RÖV7W&–ær†ÆbâBÔ’f÷VæBF‡&VRFö7VÖVçFVB7F÷&W2–ç6–FRF†R6÷WF‚vFW ¥7G&VWB6÷'&–F÷"æBBÔ"f÷VæBGvòÖ÷&RÂæBF†RVçG'’F†B6öÆÆV7FVBF†VÒ6¶VBf÷"F†P¦F—7G&–'WF–öâ&F†W"F†âF†RæV6F÷FW2â—B—26öÖÖæBæ÷r(	@¦FööÇ2öÖV7W&Uö6÷'&–F÷%ö–çG'W6–öâç–(	BæBFööÇ2ö6†V6²ç6†'Vç2—Bà ¢¢£#’öbF†RF÷vâw233"Æ6VB†6W2ÆöæRöbF†R2ÆGFVB6÷'&–F÷'2â¢¢b†fRF†V— ¦6VçG&ö–B–âöæRÂv†–6‚—2BÔrw2FW7C²’†fRF†V—"WF†÷&VB÷6—F–öâö–çB–âöæRâ6÷WF€¥vFW"6'&–W2BöbF†R#’æBF†RFVWW7BB¢£"ãÒ¢¢Â'WBF†R6WB7ç2¢¦V–v‡B¢ §7G&VWG2(	B&æFöÇ‚Â6Æ&²Â7FFRÂÆ¶RÂFV&&÷&âÂvVÆÇ2æB6æÂ2vVÆÂ(	B6ð¢&ÆÂöbF†VÒ&Röâ6÷WF‚vFW""FöW2æ÷B7W'f—fRF†RgVÆÂÖV7W&VÖVçBà ¢¢¤WfW'’öæRöbF†R#’—2&W6V&6†ÖÆ–W"&V6÷&Bâ¢¢¦W&òöbF†Ræöç–Ö÷W2&V6öç7G'V7F–öà§&öög2æB¦W&òöbF†R–æfW'&VBÖ†÷W6V†öÆB&öög2Æç’6÷'&–F÷"âWfW'’vVæW&F÷"†26¶V@¦ÆEö6÷'&–F÷'2æ–çG'W6–öâ‚–&Vf÷&RÆ6–ærç—F†–ær6–æ6R³rÂæBF†—2&6VÂ6öÖÖ—G2F†@¦2â¢¦'6öÇWFR¢¢76W'F–öâ&F†W"F†â&F6†WC¢vVæW&FVB&ööb–â&öGv’—2§&Vw&W76–öââ&÷F‚†ÇfW2öbF†RvFRvW&R'&ö¶VâFVÆ–&W&FVÇ’&Vf÷&R&V–ærG'W7FVBà ¢¢¥F†RFWF‡2&R&–ÖöFÂÂæBF†Rv—2F†Rf–æF–ærâ¢¢æ÷F†–ærBÆÂ6—G2&WGvVVâã“‚Ð¦æB2ãC‚Ó¢r&V6÷&G2FVWÂ"6†ÆÆ÷râ¢£2öbF†RrFVW&R6÷WF‚vFW"â¢¢F†R6†ÆÆ÷p§F–Â—27&VB÷fW"6—‚7G&VWG2B(šBã“‚ÒÂv†–6‚—2v†BFW&—fVB6÷'&–F÷"æBG&6V@¦6VçG&VÆ–æR6â†öæW7FÇ’F—6w&VR'’(	BBÔrw2&ÖWG&R÷"Gvò&÷VBöb—G2÷vâg&öçFvR"âF†P¦FVW6ÇW7FW"—2æ÷BF†BÂæB—B†2æòGG&–'WFVB6W6R–WBâ¢„³3†"’ÂF†RVçG'’&÷fRÀ¦GG&–'WFVB—BF†R6ÖRF“¢F†R6W6R—2F†RG&v–ær6öçfVçF–öâÂæBF†R6†ÆÆ÷rF–Âw0¢&ÖWG&R÷"Gvò"—2æ÷rÖV7W&VBBã3^(	3ãc’Ò&F†W"F†âFW67&–&VBâ’  ¢¢¥GvòçVÖ&W'2F†BvW&RV÷FVBæBFòæ÷B&W&öGV6Râ¢¢BÔrw2¦f÷W'FVVâ¢&V6÷&G2v—F‚F†V— ¦6VçG&ö–B–â&öGv’—2¢£b¢¢(	BÖV7W&VBBS#cC3CfÂF†R6öÖÖ—BF†B7FFW2—BÂ2vVÆÀ¦2FöF’ÂæB—B—2F†R6ÖRb&÷F‚F–ÖW2Â6òF†RÆ–W"†2æ÷Bw&÷vââæBGvòöbF†Rf÷W ¦'V–ÆF–æw2BÔræÖW2&R&–çFVBv–ç7BF†Rw&öær7G&VWBÂ&V6W6R6VçG&ö–BBà¦–çFW'6V7F–öâ—2–ç6–FR¢§Gvò¢¢6÷'&–F÷'2æBæ÷F†–ær6–Bv†–6‚Fò&W÷'Bà ¢¢¥F†RöæR7—7FVÖF–26W6RF†B6÷VÆB&RFW7FVB†W&Rv2FW7FVBæB—2&VgWFVBâ¢¢F†P§÷6—F–öâ6—G2BF†Rfö÷G&–çBöÇ–vöâw2÷&–v–âÂv†–6‚—2fW'FW‚öâ33"öb332&V6÷&G2Â6ð¦'V–ÆF–ærFW&—fVBFò7G&VWB6÷&æW"—2G&vâv—F‚6÷&æW"öâF†Bö–çB(	BvööBVæ÷Vv€¦ÖV6†æ—6ÒF†B#öbF†R#’æ6†÷'27FæBöâÆVvÂw&÷VæBv†–ÆRF†R&öG’&V6†W2–çFòF†P§7G&VWBâ6VçG&–ærWfW'’fö÷G&–çBöâ—G2÷vâæ6†÷"6ÆV'2RÂ–×&÷fW2BæBÖ¶W2¢£ §v÷'6R¢¢ÂF†RG&VÖöçB†÷W6R'’rãS’ÒâÒ×&V6VçG&V¶VW2F†R&VgWFF–öâ'Vææ&ÆRà ¢¢¥v†B—2VçfW&–f–VC¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6Âf÷"F†RW7VÂ&V6öà®(	BF†R†&æW72w2FVâÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ær…$ôDÔÂ'F†R'Vâ'VFvWB"’âFööÇ2ö6†V6²ç6† §76VBæBF†RÖö&–ÆR†Æb76VBv–ç7BF†RV&Æ—6†VBÖ—'&÷"âF†—2&6VÂ6†—2æòFFÀ§&VæFW&W"÷"66VæR6†ævRÂ6òF†W&R—2æ÷F†–ær–â—B'&÷w6W"6÷VÆBÆöBF–ffW&VçFÇ“¢¢¦æð§&V6÷&BÂ6ö÷&F–æFRÂF–ÖVç6–öâ÷"6öæf–FVæ6RÖ÷fVB¢¢ÂæBæò'V–ÆF–ærv2F÷V6†VBà ¢22æWr##bÓ‚Ób(	BWfW'’6&Bw2F÷76–W"Æ–æ²v2CBöâF†RFWÆ÷–VB6—FRÂæB3öbF†VÒ6†÷VÆBæWfW"†fR&VVâÆ–æ·0 ¢¢¤³#bâ¢¢V6‚'V–ÆF–ær6&BVæG2v—F‚Æ–æ²FòF†R&W6V&6‚w&—FR×W&V†–æBF†R'V–ÆF–ærÂæ@¦÷Wæ§66ö×÷6VB—B2F‚&VÆF—fRFòF†RvÆ·F‡&÷Vv‚âFööÇ2÷V&Æ—6‚ç6†ÆVfW2Fö72ö ¦÷WBöbF†R–ÆöB'’FW6–vâÂ6ò¢¦ÆÂ33"Æ–æ·2CBvBöâF†RFWÆ÷–VB6—FR¢¢(	BÖV7W&VBÂæ÷@§&V6öæVB&÷WC¢(
fv—F‡V"æ–òö7W7FöÒö6†–6vòóFBöFö72õ$U4T$4‚÷6Vvæ6…ö†÷FVÂæÖF&WGW&ç2CBæ@§F†R6ÖRF÷76–W"öâv—D‡V"&WGW&ç2#âF†RÆ–æ²&W6öÇfVB–âF†R6÷W&6RG&VRÂv†–6‚—2F†RöæP§Æ6R—Bv2WfW"6Æ–6¶VBà ¢¢¥F†RÆ–æ²—2æ÷r'6öÇWFRæBvöW2Fòv—D‡V"¢¢Âv†–6‚&VæFW'2Ö&¶F÷vã²Ö–æ&F†W"F†âFWfÀ¦&V6W6RF†B—2F†R'&æ6‚f—6—F÷"w26÷’v2&öÖ÷FVBg&öÒƒöbF†RSRF—7F–æ7BF÷76–W"F‡0¦7W'&VçFÇ’Æ–æ¶VB&RFWbÖöæÇ’Â6òF†RÆr—2æ–ÂFöF’’à ¢¢¥F†R3&RF†Rf–æF–ærF†R&6VÂF–Bæ÷B&VF–7Bâ¢¢F†R6ö×–ÆW"76W'FV@¦Fö72õ$U4T$4‚óÆ–CâæÖF'’6öçfVçF–öâæBæWfW"6¶VBv†WF†W"F†Rf–ÆRW†—7FVB(	B&–v‡B&÷WB3 §&V6÷&G2Âw&öær&÷WB3ÂWfW'’öæR¦Fö7VÖVçFVB¢'V–ÆF–ærv†÷6Rw&—FR×W†2æ÷B&VVâFöæR‡F†P¦6÷W'F†÷W6RÂF†RÆör¦–ÂÂF†RW7G&’VâÂ7BÖ'’w2ÂF†RFV×ÆR'V–ÆF–ærÂF†R&W6'—FW&–â6‡W&6‚À¤¶–ç¦–Rb‡VçFW"w2v&V†÷W6R’âF†÷6R6&G2æ÷r6’¦æòF÷76–W"w&—GFVâf÷"F†—2'V–ÆF–ær–WB¢æ@¦öffW"æòæ6†÷"âF†R3&VÖ–â&W6V&6‚FV'BæBFööÇ2ö6†V6µöF÷76–W%öÆ–æ·2ç–æÖW2F†VÒWfW'§'Vâà ¢¢¥v‡’—B7W'f—fVC¢¢¢F†R6Öö¶R76W'FVBF†R6&Bw2DU…B6öçF–æVBF†RF‚Âv†–6‚v2G'VRöâWfW'§'Vâv†–ÆRWfW'’Æ–æ²v2'&ö¶Vââ—Bæ÷r&VG2F†R‡&VfæB76W'G2—BÆVfW2F†—2÷&–v–âÂv—F€¦FV×ÆUö'V–ÆF–æv2F†RF—67&–Ö–æF–æræòÖÆ–æ²66RâfÆ–FFRç–†BvFVBF†R¦÷VâVW7F–öâ ¦F÷76–W"ö–çFW"w2W†—7FVæ6R6–æ6R—Bv2w&—GFVã²F†R'V–ÆF–ær6&Bw2ö–çFW"æWfW"†B—Bà ¢¢¥v†B—2VçfW&–f–VC¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6Âf÷"F†RW7VÂ&V6öâ(	BF†P¦†&æW72w2FVâÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ær…$ôDÔÂ'F†R'Vâ'VFvWB"’âFööÇ2ö6†V6²ç6†76VBæ@§F†RÖö&–ÆR†Æb76VBv–ç7BF†RV&Æ—6†VBÖ—'&÷"Â¢£#’76VBòf–ÆVB¢¢âF†RGvòæWp¦76W'F–öç2vW&RFF—F–öæÆÇ’'VâB#ƒ9sƒv–ç7BF†R6ÖRÖ—'&÷"'’âBÖ†ö267&—B(	B&÷F€¦w&VVâÂ¦W&òvRW'&÷'2Â–ârãR2(	B6òv†B—2VçfW&–f–VBBFW6·F÷—2F†R&W7BöbF†R7V—FRÂæ÷@§F†—2&6VÂw2÷vâ6Æ–×2âF†BçVÖ&W"—2v÷'F‚æ÷F–æröâ—G2÷vã¢&ö÷F–ærF†RV&Æ—6†VBvÆ²Ð§F‡&÷Vv‚æB&VF–ærGvò6&G2BFW6·F÷6÷7G26V6öæG2ÂæBF†RFW6·F÷†Æbw2F†—'FVVâÖ–çWFW0¦&R—G2&öBÖ6öçG&7BæB†÷&—¦öâ6GW&W2âFW7BÖæÖRf–ÇFW"v÷VÆBÆWB—B'Vâ2Gvò6öÖÖæG0§F†BV6‚f—Bà ¢¢¤æòvVöÖWG'’ÂF–ÖVç6–öâÂ6ö÷&F–æFR÷"6öæf–FVæ6RÖ÷fVB¢£¢36–FV6'2Æ÷6RF‚F†Bö–çFV@¦Bæ÷F†–ærÂæBF†R&W7B&RVçF÷V6†VBà ¢22æWr##bÓ‚Ób(	BF†Rw&÷VæB7F–ÆÂ7FæG2÷fW"F†R&öB—B6'&–W2ÂæBF†Rf—‚6÷7G2Ãb'—FW0 ¢¢¥"Õsb¢¢Âv†–6‚W‡V7FVBFò&÷fRF†R†÷&—¦öçFÂ'FVf7B–çf—6–&ÆRæB–ç7FVBÖV7W&VB—Böà¥6÷WF‚vFW"7G&VWBâ"Ô%Ts62&W—&VBF†R3bÖÒdU%D”4ÂÆGF–6R'’&VF–ær†V–v‡G2&6²öfbF†P¦†V–v‡Ff–VÆBBÆöC²F†R6ÖRVçF—6W"Ö÷fW2RæBâÂæ÷F†–ær6÷'&V7G2F†BÂæBfW'FW€¦6öæf÷&ÖVBBF—7Æ6VB÷6—F–öâ†öÆG2F†Rf–VÆBw2†V–v‡Bf÷"F†Rw&öærÆ6Rà ¢¢¤ÖV7W&VBBÆÂ#S’Ãcƒ’öbF†Rf–VÆBw2÷vâ6×ÆRö–çG2ÂgFW"6öæf÷&Ôw&÷VæEFôf–VÆB‚–Â'¦–çFW'öÆF–ærF†R6öçF–æ–ærG&–ævÆR–âÆâ¢¢(	BFööÇ2öÖV7W&U÷FW'&–åö†÷&—¦öçFÂæÖ§6Âv—F‚F†P£BÖ&—B&V'V–ÆB6öÖ–ær&6²¢¦'—FRÖf÷"Ö'—FR–FVçF–6ÂFòF†Rf–ÆR–â76WG2÷vV"ö¢¢Â6òF†P¦çVÖ&W'2&RF†R6†—–æröæW3  §ÂVæ6öF–ærÂ´"ÂÆGF–6RÂÆâF—7Æ6VÖVçBÂG&vâ7W&f6Rg2f–VÆB‡&×2ò“’òÖ‚’Â7BF†R#"ÖÒ&öBÆ–gBÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§ÂÖ7FW"Âc#“bÂfÆöBÂ(	BÂã2ò2ã‚ò¢£rãrÖÒ¢¢Â(	BÀ§Â¢§6†—VBÂBÖ&—B¢¢ÂcsÂ3bãBÖÒÂ¢£#s2ãÖÒ¢¢Â"ãòrã’ò¢£Cbã2ÖÒ¢¢Â¢£ƒr¢¢ƒCBG'’’À§Â¢£bÖ&—B(	BF¶Vâ¢¢Âcs"ÂsbãbÖÒÂS"ãÖÒÂãBò2ã‚ò¢£"ã’ÖÒ¢¢Â¢£¢¢À§ÂVæ6ö×&W76VBÂc#“bÂfÆöBÂãÖÒÂã2ò2ã‚ò¢£rãrÖÒ¢¢ÂÀ ¢¢¥F†R6Æ÷6W7B÷fW"Ö'VFvWB6×ÆR7FæG2ã’Òg&öÒ6÷WF‚vFW"7G&VWBw26VçG&VÆ–æR¢¢(	B–ç6–FR£ãRÒG&fVÆÆVBG&6²(	B¢£3ã"ÖÒ&÷fRF†Rf–VÆBÂ6''––ær&öBÆ–gFVB#"ÖÒâ¢¢F†B—0¥"Ô%Ts62w2f–ÇW&RÖöFR7W'f—f–ær—G2÷vâf—‚ÂöâF†R7G&VWBF†R÷væW"&W÷'FVB—Bg&öÒÂBóP§F†R×Æ—GVFRæBöâã2RöbF†RF÷vââF†RÖV6†æ—6Ò—26Æ÷RÂæ÷B6—¦S¢F†Rƒr6×ÆW26—B@¦ÖVF–â6Æ÷Röb¢£‚R¢¢ÂæBfÆBÆGFVB&—&–R6ææ÷B6†÷rF†—2Bç’&—BFWF‚à ¢¢¥F†RFV6—6–öâÂÖFR'’ÖV7W&VÖVçB&F†W"F†â&VfW&Væ6Râ¢¢F†RFW'&–â¶VW26†—–æp§VçF—6VB(	BF†RVæ6ö×&W76VBf–ÆR'W—2"ã’ÖÒ(i"rãrÖÒf÷"Rã‚Ô"ÂæBrãrÖÒ—2DT4”ÔD”ôà¦WfW'’&÷r6'&–W2(	BB¢£b&—G2öâF†RWö6‚ÖW6†W2öæÇ’¢£¢³Ãb'—FW2Âv–ç7B³Rãr´ ¢‚³"ãBR’ÖV7W&VBf÷"&—6–ærF†Rv†öÆR–ÆöBFò'W’æ÷F†–ærÖV7W&&ÆRÂ&V6W6R&V6—6–öâ—0§W"ÖÖW6‚æBWfW'’76WBF†B—2æ÷BF†RFW'&–â÷"F†RvFW"Ç&VG’ÆæG2–ç6–FRBã‚ÖÐ¢†ÖVF–âãRÖÒ’âGvò6÷'&V7F–öç2&–FRv—F‚—C¢"Ô%Ts62w2¢$RæBâÖ÷fR'’WFòS2ÖÒ"¢v0¦&—F†ÖWF–2æBF†RÖV7W&VBf–wW&R—2¢£#s2ãÖÒ¢¢–âÆã²æBR&—G2—2¦&–vvW"¢F†âbà ¢¢¥v†B—2VçfW&–f–VC¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6(	BF†RFVâÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–ærâF†RÖö&–ÆR†Æbv2'Vâv–ç7BV&Æ—6†VBÖ—'&÷"6''––ærF†RbÖ&—@¦w&÷VæC¢¢£#‚76VBÂf–ÆVB¢¢â¢¤æòtÄ"6†—2v—F‚F†—2&6VÂ¢£¢76WG2÷vV"ö&VÆöæw2FòF†P¦æ–v‡FÇ’&¶RÂ6òF†Rw&÷VæBf—6—F÷"ÆöG27F—2BÖ&—BVçF–Â6†–6vòÓFBÖ&¶Rç–ÖÆæW‡B'Vç2à ¢22æWr##bÓ‚ÓR(	Bc#2–çfVçFVBFWF–Ç26—FVB&æBF†R7V6–f–6F–öâæWfW"w&÷FRÂæBC"öbF†VÒvW&RVæf–æF&ÆP ¢¢¤³32¢¢ÂF†R÷F†W"†Æböb³#Rw27V&¦V7BÂæB—B—2v÷'6R–â¶–æC¢æ÷BfÇVR÷WG6–FR—G2&æB'W@¦fÇVRv—F‚¢¦æò&æBFò&R–ç6–FR¢¢â³#R†’÷VæVB—BBSƒg&öÒF†R&÷6R6Vç7W2âF†RÖV7W&V@¦f–wW&R—2¢£c#2fÇVW2öâ##röb#C’&V6÷&G2¢¢(	B–çF##Â6†–ÖæW—6“2Â&ö&EövöÖc’À¦ÆæCbÂFö÷&öFö÷%÷6–FV3rV6‚Â&—63RÂ÷&6†#2ÂvööG5öFö÷&övööG5öFö÷%÷6–FV‚V6‚À¦vÆÆW'–BÂ6†÷g&öçF(	B¢¦æB&ööe÷—F6…öFVvC"â¢  ¢¢¥F†RC"&RF†Rf–æF–ærÂæBF†R&V6öâF†W’vW&RÖ—76VB—27G'V7GW&Ââ¢¢f—fRfÖ–Æ–W2(	B2ÂBÀ¤RÂsBÂsR(	Bw&—FRF†V—"&ööb2¢&v&ÆR÷"6†VB"£¢f÷&Òv—F‚æò6Æ÷R–â—BâWfW'’öæRöbF†V— §&V6÷&G27F–ÆÂ6'&–VBæ÷FR6––ærF†R—F6‚v2G—RÖÆWfVÂ6†ö–6Rv—F†–âF†RfÖ–Ç’&æBà¤³#R†’w2&æFVB†Æb6÷VÆBæ÷B6VRF†VÒ&V6W6R¢¦fÇVRv—F‚æò&æB—2æWfW"FW7FVBv–ç7@¦öæR¢¢Â6òF†RFööÂvÆ¶VB7BW†7FÇ’F†R&V6÷&G2v†W&RF†RfVÇB—2F÷FÂ&F†W"F†â'F–Âà¥F†RvVæW&÷W2¶W—v÷&Bv2fÆö÷"öâF†R&÷6R6Vç7W3²F†R¦6Æ76–f–6F–öâ¢v26V6öæBfÆö÷ ¦æö&öG’†BæÖVBà ¢¢¥&÷WFR"‡7Æ—BF†Ræ÷FR’v26†÷6VâÂæB&÷WFR2v2ÖV7W&VB2Væf–Æ&ÆRâ¢¢w&F–ærF†W6R¦ÆWfVÂÆ÷vW"v÷VÆB7FÆR#C’6öÖÖ—GFVBtÄ'2(	BvVæW&F÷'2öÖW6…ö–çWG2ç–†6†W2F†R6öæf–FVæ6P¤dÄôE2–çFòF†RÖW6‚–çWB&V6—RÂv†–6‚—2F†R6ÖRvÆÂBÕc†"’æB³#R†"’6—B&V†–æBâ¢¥&÷6R—0¦æ÷B†6†VB¢¢Â6òF†R†öæW7B&W—"æBF†Rff÷&F&ÆRöæR&RF†R6ÖR&W—"†W&RâF†B—2¦6ö–æ6–FVæ6RæB—2w&—GFVâW2öæRÂ&V6W6RæW‡BF–ÖR—Bv–ÆÂæ÷B&Rà ¢¢¥F†Ræ÷FRæVvFW2F†RÆVFR&F†W"F†âG&÷–ær6—FF–öââ¢¢WfW'’ffV7FVBfÇVR—2&Vf—†VB'¦vVæW&F÷"&w&‚&VF–ær¢'F†R7V2—26—FVB&V6W6RF†R–çfVçF–öâ—2&÷VæFVB'’—B"¢(	BF†P¦W†7BVçG'VR6Æ–Ò(	B6ò6–ÆVçB&VÖ÷fÂv÷VÆB†fRÆVgBF†RfÇ6R–×&W76–öâ7FæF–ærâF†P§&WÆ6VÖVçB÷Vç2äõB$õTäDTB%’D„R5T4”d”4D”ôâÂæBF†R6VçFVæ6R&÷fR&÷WBF†R–çfVçF–öà¦&V–ær&÷VæFVBFöW2æ÷B†öÆBf÷"F†—2fÇVVÂæÖW2F†RfÖ–Ç’æBF†Rf–VÆBÂæB6—2F†RfÇVR—0§F†R&V6öç7G'V7F–öâvVæW&F÷"w2G—RFVfVÇBâV6‚&6VÂw2÷vâ6Æ÷6–ær6ÆW6R—2¶WBfW&&F–Òà ¢¢¦FööÇ2ö&æEöæ÷FW2ç–—2F†R6–ævÆR&VF–6FR¢¢Â–×÷'FVB'’ÆÂf—fRvVæW&F÷'2F†BWF†÷"F†P§6VçFVæ6RæB'’FööÇ2öÖV7W&Uö&æEö6Æ–×2ç–F†BVF—G2—B(	BfÖ–Ç•ö&æG2ç–w2ÆW76öâÂÆ–V@¦&Vf÷&R—B6÷VÆB&—FRv–ââF†R76W'F–öâ'Vç2–âÒÖvFVæBÒ×7G&–7FæB—2¢¦'6öÇWFS¢æð¦&6VÆ–æRÂæòÆÆ÷væ6R¢¢ÂFVÆ–&W&FVÇ’VæÆ–¶RF†R³#R&F6†WB&W6–FR—BÂ&V6W6R&÷6R&W— ¦6÷7G2æò&¶RæB6â&Æö6²æ÷F†–ærâ¢¥&÷fVB–âF‡&VRF—&V7F–öç2&Vf÷&R&V–ærG'W7FVC¢¢¢c#2&V@¦v–ç7BF†R&R×&W—"FFÂgFW"ÂæB†æB×ÆçFVBg&W6‚öffVæFW"6Vv‡BââVæ6Æ76–f–V@¦f–VÆB6''––ær6—FF–öâÇ6òf–Ç2Â6òF†RæW‡B–çfVçFVBf—GF–ær6ææ÷B–æ†W&—BöæR'’FVfVÇBà ¢¢¥&W6–GVÂÂ7FFVB&F†W"F†âF–F–VC¢¢¢6÷W&6W6öâF†W6Rc#2fÇVW27F–ÆÂÆ—7G2F†R7V2v†–ÆP§F†Ræ÷FRæ÷r6—2F†R7V2FöW2æ÷B&÷VæBF†VÒâF†R7V2•2F†R6÷W&6RöbF†RfÖ–Ç’76–væÖVç@¦&V†–æBF†R&6†WG—RFVfVÇBÂ6ò—B—2æ÷B6–×Ç’w&öær(	B'WBF†RGvòf–VÆG2æòÆöævW"w&VRÂæ@§F†BvçG2FV6—6–öâ&F†W"F†â7vVWâ¢¤æòfÇVRÖ÷fVBæBæòvVöÖWG'’Ö÷fVC¢¢¢c#2æ÷FP§7G&–æw2ÂöæRæWrFööÂÂf—fRvVæW&F÷"6ÆÂ6—FW2ÂöæRvFR76W'F–öâà ¢¢¥v†B—2VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2æ÷B'Vâ(	BF†P¦†&æW72626–ævÆR6öÖÖæBBFVâÖ–çWFW2æBF†RFW6·F÷†ÆbæVVG2&÷WBF†—'FVVâ…$ôDÔÀ¢'F†R'Vâ'VFvWB"’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†Æb&÷F‚76VBâF†—2&6VÂ6†ævW2¢¦æð¦vVöÖWG'’ÂæòF–ÖVç6–öâæBæò&VæFW&W"6öFR¢¢(	BöæÇ’æ÷FR&÷6RÂv†–6‚—27G&—VBg&öÒWfW'’ÖW6€¦–çWB†6‚–âF†—2&ö¦V7Bà ¢22æWr##bÓ‚ÓR(	B—B—2“‚fÇVW2Âæ÷BSBÂæB#B6W6W2Âæ÷B“‚(	BæB&ööb—F6‚†BæWfW"&VVâÖV7W&V@ ¢¢¤³#R†’¢¢ÂF†RÖV7W&VÖVçB†ÆbâF†R&6VÂv266÷VBg&öÒâVfR6÷VçBF¶Vâöâ“2&V6÷&G2à¤6¶VB&÷W&Ç’(	BWfW'’&V6öç7G'V7FVB&V6÷&B–âF†RFF6WBæBWfW'’f÷&ÒfÇVRF†R7&÷77vÆ°¦WF†÷'2FW7F&ÆR&æBf÷"(	B¢£3RfÇVW2vW&RFW7FVBv–ç7B&æBæB“‚&R÷WG6–FR—BÂöà£ƒöb#C’&V6÷&G2¢£¢¢£SBVfW2Â3‚&ööb—F6†W2ÂB7F÷&W’6÷VçG2Â"fö÷G&–çG2Â&ööbf÷&×2â¢ ¥F†RVfRf–wW&RöbSB7W'f—fVBF†Rv–FVæ–ær'’6ö–æ6–FVæ6RÂæBBÕc†’w2C—2—G2æöç–Ö÷W2†Æbà¢¢¥&ööb—F6‚†BæWfW"&VVâÖV7W&VB'’ç—F†–ær–âF†—2&ö¦V7B¢¢ÂæB—B—2F†R6V6öæBÖÆ&vW7@¦fVÇB–âF†RFF6WBw2&÷fVææ6Rà ¢¢¥F†R“‚&R#B6W6W2â¢¢F†—'FVVâ†fÖ–Ç’ÂfÇVR’—'2†öÆBÆÂSBVfW2æB¢§6—‚FVw&VP¦6öç7FçG2†öÆBÆÂ3‚—F6†W2¢£¢"ãs‚Òv–ç7BC2w2Ž(	3’gBöâ#&V6÷&G2Â"ãRÒv–ç7BC"w0£~(	3‚gBöâæBv–ç7B¢¥sBw2ž(	3‚gBöâ2¢¢‡F†Rv÷'7BÂ³"ã#rgB’Â‚ã+v–ç7BC"w2C£"fÆö÷ ¦öâ#â¢¥6WfVâÖWG&RfÇVW266÷VçBf÷"ÆÂSBVfW2¢¢(	B"ãRÂ"ãsRÂ"ãs‚Â2ã#RÂRãRÂRã#ÂRã3R(	@§v†–6‚—2F†R&6†WG—RF&ÆRÂæ÷BÖV7W&VÖVçBöbç—F†–ærâF†RvVæW&F÷"–6·2F†RfÇVRg&öÒF†P¢¢¦&6†WG—R¢¢æBF†Ræ÷FR6—FW2F†R¢¦fÖ–Ç’¢¢à ¢¢¥—F6‚—2Væ—BÖ—6ÖF6‚æBæ÷F†–ærVÇ6Râ¢¢F†R7&÷77vÆ²WF†÷'2&—6S§'Vã²F†RvVæW&F÷"WF†÷'0§v†öÆRFVw&VW2âC£"—2‚ãC3\+æBF†R6†VB6öç7FçB—2‚ã+Â6ò#C"6†VG26—B¢£ãöb£ §7FW¢¢VæFW"fÆö÷"F†W’v÷VÆB†fR6ÆV&VB†BF†RfÇVR&VVâWF†÷&VB–âF†R&æBw2÷vâVæ—G2à¤ÆÂ3‚&Rv—F†–âöæR7FWà ¢¢¥F†R7V"ÓÖgBVW7F–öâ³#RÆVgB÷Vâ—2FV6–FVC¢F†W’&Rf–ÇW&W2â¢¢CböbSBVfW2&Rv—F†–â¦fö÷BæBæV&æW72—2W†7FÇ’v†B&WG—VB6öç7FçBÆöö·2Æ–¶RâF†RöæÇ’6Æ6²–âF†RFööÂ—0£ãRÖÒf÷"F†RÖWG&R&÷VæB×G&—à ¢¢¤6V6öæBfVÇBÂ&W÷'FVBæBæ÷BvFVBâ¢¢F†R6ÖR6VçFVæ6R—2öâfÇVW2F†R7V6–f–6F–öâFöW0¦æ÷B&÷VæBBÆÂ(	B¢¦–çFöâ##r&V6÷&G2Â##v–ç7BfÖ–Ç’F†BæWfW"ÖVçF–öç2–çC°¦&ö&EövöÖöâ“’v–ç7B7V6–f–6F–öâF†BæÖW2æò&ö&Bvç—v†W&S²6†–ÖæW—6öâSÀ£“26–ÆVçBâ¢¢F†W&R—2æò&æBFò&R–ç6–FRâF†R–ç7G'VÖVçB—2¶W—v÷&BæBF†W&Vf÷&RfÆö÷"Â6ð¦—B&–çG2&F†W"F†âf–Ç2ÂæB—B—2÷VæVB2¢¤³32¢¢v—F‚F†RFV6—6–öâ—BæVVG27FFVBà ¢¢¦FööÇ2öÖV7W&Uö&æEö6Æ–×2ç’ÒÖvFV'Vç2öâWfW'’6†V6²ç6†Â2&F6†WBâ¢¢F†R7G&–7@¦76W'F–öâ¢¦f–Ç2FöF’æB—2ÖVçBFò¢¢†Ò×7G&–7FÂW†—BÂ“‚f–æF–æw2“²v†BvFW2—2F†P¦6öÖÖ—GFVB6Vç7W2–âFööÇ2ö&æEö6Æ–×5ö&6VÆ–æRæ§6öæ(	BæWröffVæFW"Â÷"6öÖÖ—GFVBöæRv†÷6P§fÇVRÖ÷fVBÂf–Ç2â¢¤&÷F‚†ÇfW2vW&R'&ö¶VâöâW'÷6RæB&÷fVBFòf–Â¢¢&Vf÷&R&V–ærG'W7FVC ¦ÆçFVBBã’ÒCvÆÂ—26Vv‡B2äUrÂæB&W—&–ær&V6öåóƒ3Uöæ÷'F…öC5ó&v—F†÷WB&Ww&—F–æp§F†R&6VÆ–æR—26Vv‡B2âVç&V6÷&FVB&W—"âF†RfVÇBÖ’6‡&–æ²æBÖ’æ÷Bw&÷rà ¢¢¤³#R†"’—2&Æö6¶VBW†7FÇ’v†W&RBÕc†"’—2&Æö6¶VB¢¢(	BWfW'’öffVæFW"—2öâ6æöæ–6ÆÇ’&¶V@§&6VÂÂæBF†R&W—"6ææ÷B72F†RvFR—B×W7B72Fò&V6‚F†R'&æ6‚F†R&¶R&VG2â¢¤æð¦F–ÖVç6–öâÖ÷fVB†W&Râ¢  ¢¢¥v†B—2VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2æ÷B'Vâ(	BF†P¦†&æW72626–ævÆR6öÖÖæBBFVâÖ–çWFW2æBF†RFW6·F÷†ÆbæVVG2&÷WBF†—'FVVâ…$ôDÔÀ¢'F†R'Vâ'VFvWB"’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†Æb&÷F‚76VBâF†—2&6VÂ6†ævW2¢¦æòFFÀ¦æòvVöÖWG'’æBæò&VæFW&W"6öFR¢£¢v†B6†—2—2öæRæWrFööÂÂ—G26öÖÖ—GFVB6Vç7W2ÂöæRvFR7FW ¦æBFö7VÖVçFF–öâà ¢22æWr##bÓ‚ÓR(	BF†RGv–ç2&RÆÂ–âöæR&6VÂÂæBCæ÷FW2&Rw&öær&÷WBF†V—"÷vâ6÷W&6P ¢¢¥BÕc†’¢¢ÂF†RÖV7W&VÖVçB†Æbâ"Ôs&ÆÖVB6÷WF…÷vFW&f÷"†÷&—¦öâöböæRv&ÆR&WVFVBÀ¦æBF†B&÷r†BÇ&VG’&VVâf—†VBGv–6R&Vf÷&RF†—2&6VÂv26Æ–ÖVC¢F†R†6RÖöæR6÷WF€§&6VÂ6×ÆW2—G2fö÷G&–çG2ÂæBÆÂGvVÇfR†6S6ÆGFVBÖ&Æö6²&6VÇ26×ÆRfö÷G&–çBæ@¦VfRâÖV7W&VB7&÷72ÆÂ¢£#‚¢¢æöç–Ö÷W2&öög2Â¢¦WfW'’Gv–â–âF†RF÷vâ—2–âöæR&6VÂ¢¢(	@¦†6S%öæ÷'F…öF—f—6–öåö–æ—F–ÆÂw&—GFVâ&Vf÷&RF†R6×Æ–ær'VÆRW†—7FVBâ6—‡G’&öög2ÂGvVçG’×F‡&VP¦fÖ–Æ–W2Â¢£#BF—7F–æ7BÖ76–æw3²3böbF†Rc6†&Rfö÷G&–çBäBâVfRv—F‚æ÷F†W"&ööbö`§F†V—"÷vâfÖ–Ç’¢¢à ¢¢¥D„R4Tå5U2dõTäB4ôÔUD„”är$”ttU"D„âD„REt”å2â¢¢WfW'’–çfVçFVBF–ÖVç6–öâ6'&–W2F†Ræ÷FP¢¢%G—RÖÆWfVÂ6†ö–6Rv—F†–âF†RfÇC¶fÖ–Ç’fwC²&æB"¢ÂæBF†B6VçFVæ6R—2F†RVçF—&RFVfVæ6Rf÷"F†P¦–çfVçF–öââ¢£CöbF†R#‚VfW2&R÷WG6–FRF†R&æBF†V—"÷vâæ÷FR6—FW2¢¢(	B‚–â†6S÷6÷WF†À£r–â†6S%öæ÷'F†ÂR–â†6S%÷vW7FâF†R†6RÖöæR&6VÂ—2F†R6†'66S¢—B6×ÆW2—G0¤dôõE$”åBæB6'&–W2F†R6VçFVæ6R6––ær6òÂv†–ÆR—G2VfR—27F–ÆÂöæR6öç7FçBW"fÖ–Ç’â6ò§&V6÷&B6â†öÆBG'VR6VçFVæ6R&÷WB—G2ÆâæBfÇ6RöæR&÷WB—G2vÆÂÂ–âF†R6ÖRæ÷FP§7G–ÆRÂæBæ÷F†–ærF—7F–æwV—6†VBF†VÒâF†—2—2$ôDÔ¢¤³#R¢¢w2fVÇBÖV7W&VBöâ6V6öæBÆ–W#°¢¢¦æöæRöbF†RC—2f—†VB†W&Râ¢  ¢¢¦FööÇ2öÖV7W&UöÖ76–æu÷f&–WG’ç’ÒÖvFV'Vç2öâWfW'’6†V6²ç6†â¢¢—G27V&¦V7B—26VçFVæ6P§F†RFF—G6VÆbÖ¶W3¢F†R3‚&V6÷&G2F†B6’6×ÆVBFWFW&Ö–æ—7F–6ÆÇ–&R†VÆBFò—B(	B–ç6–FP§F†R&æBÂVæ—VRv—F†–âfÖ–Ç’æB&6VÂâ¢¤&÷F‚6ÆW6W2vW&R'&ö¶VâöâW'÷6RæB&÷fVBFð¦f–Â¢¢&Vf÷&R&V–ærG'W7FVBâWfW'—F†–ærVÇ6R—B&W÷'G2æBFöW2æ÷Bf–ÂÂæBF†RFööÂw2Fö77G&–æp§6—2v‡’–â2Öç’v÷&G3¢¦Fòæ÷B&VB72†W&R2'F†RF÷vâ—2F—7G&–'WF–öâ"¢à ¢¢¤öæR&VÂ'VrÂf—†VBâ¢¢F†RVfRfÆö÷"F†B¶VW2â–çfVçFVB÷WF'V–ÆF–ærFÆÂVæ÷Vv‚Fò6''’—G0¦÷vâFö÷"v2Dôõ%ô„TE$ôôÕôÒÒ"ãV(	B¢¦Öâ¢¢Fö÷"(	BÆ–VBFòWfW'’Fö÷"Ö6''––ærfÖ–Ç’À¦–æ6ÇVF–ærF†RvvöâFö÷'2öâsÂs"ÂsRÂcæB"âvvöâFö÷"—22ãÒ–âF†R6ÆV"â—BæWfW ¦&—B&V6W6RF†÷6RfÖ–Æ–W27FööBB&WG—VB2ãC"Ó²F†RÖöÖVçBF†Ræ÷'F‚&6VÂ6×ÆVB—G2&æBÀ¦&V6öåóƒ3Uöæ÷'F…÷sò¦f–ÆVB'’æÖRB"ãƒ#Òv—F‚æò†VFW"âVfUöfÆö÷"†fÖ–Ç’ÂFö÷"–æ÷p¦6·2÷WF'V–ÆF–æu÷&×2äDôõ%õ4•¤UôÖ–ç7FVBöb6''––ær†æBÖ6÷–VB6öç7FçB(	BF†R6ÖRfVÇ@§F†—2&6VÂ—2&÷WBÂ–âÖ–æ–GW&RâF†R“&Æö6²&V6÷&G2&R¢¦'—FRÖ–FVçF–6Â¢¢7&÷72F†R6†ævRà¥F†R6×Æ–ær'VÆR—G6VÆbÖ÷fVBFòFööÇ2öfÖ–Ç•ö&æG2ç–Âv†–6‚&÷F‚vVæW&F÷'2æ÷r–×÷'Bà ¢¢¥BÕc†"’•2u$•EDTâÂÔT5U$TBäB4ääõBÄäB„U$R(	B&VB—G2$ôDÔ&÷‚&Vf÷&RF÷V6†–ærç¦F–ÖVç6–öâöâ&¶VB&V6÷&Bâ¢¢v—&–ærF†Ræ÷'F‚vVæW&F÷"FòfÖ–Ç•ö&æG6v2–×ÆVÖVçFVBæB'Vã ¦WfW'’Æ6VÖVçBvFR76VB†æò6öÆÆ—6–öâÂæò6÷'&–F÷"–çG'W6–öâÂæ÷F†–æröfbF†RFW'&–âÂæ÷F†–æp¦÷fW"F†Rã3RÒ&VÆ–Vb6öçG&7B’ÂæB—BF¶W2¢£3bGv–ç2FòÂ#BF—7F–æ7BÖ76–æw2FòcÂæBp¦÷WBÖöbÖ&æBVfW2Fò¢¢â—Bv2&WfW'FVB&V6W6RF†R6—‡G’æ÷'F‚tÄ'2&R6æöæ–6Â&ÆVæFW"&¶W3 ¦6†æv–ærF–ÖVç6–öâ7FÆW2ÆÂ6—‡G’ÂfÆ–FFRç’ÒÖÆÆ—2F†RFWbvFRÂF†W&R—2æò&ÆVæFW"öà§F†—2'VææW"ÂæB6†–6vòÓFBÖ&¶Rç–ÖÆ&¶W2¢¦g&öÒFWf¢¢(	B6òF†Rf—‚6ææ÷B72F†RvFR—B×W7@§72Fò&V6‚F†R'&æ6‚F†R&¶R&VG2â¢¥F†B6—&6ÆR7FæG2–âg&öçBöb³#R†"’æBWfW'’&6VÀ§F†Bv÷VÆBÖ÷fRF–ÖVç6–öâöâF†R#‚6æöæ–6ÆÇ’Ö&¶VB&öög2â¢¢F‡&VR&÷WFW2&Rw&—GFVâWf÷ §F†R÷væW#²6†ö÷6–æröæR—2öÆ–7’VW7F–öâæBâ÷fW&æ–v‡B'VâF–Bæ÷BÖ¶R—Bà ¢¢¥v†B—2VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2æ÷B'Vâ(	BF†R†&æW70¦626–ævÆR6öÖÖæBBFVâÖ–çWFW2æBF†RFW6·F÷†ÆbæVVG2&÷WBF†—'FVVâ…$ôDÔÂ'F†R'Và¦'VFvWB"’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†Æb&÷F‚76VBâ¢¥F†—2&6VÂ6†ævW2æòFFÂæð¦vVöÖWG'’æBæò&VæFW&W"6öFR¢£¢v†B6†—2—2GvòæWrFööÇ2ÂöæRvFR7FWÂâ–×÷'B–âF†R&Æö6°¦vVæW&F÷"v†÷6R“&V6÷&G2&R'—FRÖ–FVçF–6ÂÂæBFö7VÖVçFF–öâà ¢22æWr##bÓ‚ÓR(	B6—‡FVVâ&VgW6Ç2vW&RÖFRv–ç7B6æF–F6–W2F†—2Æ–W"æWfW"7GVÆÇ’†@ ¢¢¥BÔ6‚¢¢ÂF†R&6¶f–ÆÂöb&Æµ÷&æFöÇ…öFV&&÷&æ(	BF†RöæR&Æö6²F†BÆæFVB&Vf÷&R'VÆRb†B—G0§F†—&BFW7BÂæB6òF†RöæR&Æö6²æWfW"6¶VBv†òÆ—fVBöâ—BâF†RF÷F–öç2&RF†RGvòF†R&6VÀ§&VF–7FVC¢F†R¢¤C2¢¢öâÆ÷BFòGvVçF–WF‚6'VçFW"w2†÷W6V†öÆBÂF†R¢¤C¢¢öâÆ÷B2Fò§GvVçG’×F†—&BÆ&÷W&–æröæRâ–æfW'&VB†÷W6V†öÆG2¢£“’(i"¢¢ÂW'6öç2¢£(i"2¢¢ÂF÷FV@¦æöç–Ö÷W2&öög2¢£"(i"B¢¢ÂæB¢§7FæF–ær&öög2Væ6†ævVBB3#"¢¢(	Bæ÷F†–ærv2'V–ÇBÂÖ÷fVB÷ §&Vw&FVBâ&V6÷&FVB–â¢¤Ã’¢¢à ¢¢¥D„Rd”äD”är•2$õUBD„R$ôôe2•B$TeU4TBâ¢¢F†R&Æö6²Ç6òFVÇ2¢¤CB¢¢æB¢¤C"¢¢ÂæB&÷F€§&–çBDõD$ÄR(	BF†R6'VçFW'2r'6V6öæB&ööb"æBF†RÆ&÷W&W'2rÂW†7FÇ’2BV–v‡B&Æö6·0¦&Vf÷&R—Bâæö&öG’†B6¶VBv†BF†÷6RfW&F–7G2&RÖFRöbâF†—2Æ–W"†÷W6W2¢¦öæR¢¢6'VçFW"–à¦CBæBF†B†÷W6V†öÆB7FæG2–âF†R¢¤æ÷'F‚¢¢F—f—6–öã²—B†÷W6W2¢¦f÷W"¢¢Æ&÷W&W'2–âC"æ@¦ÆÂf÷W"7FæB–âF†R¢¤æ÷'F‚¢¢÷"F†R¢¥vW7B¢¢âWfW'’6'VçFW"æBWfW'’Æ&÷W&W"—B†÷W6W2–âF†P¢¢¥6÷WF‚¢¢F—f—6–öâÆ—fW2–âC2÷"Câ¢¤æV—F†W"6V6öæB&ööb—2†fÖ–Ç’ÂF—f—6–öâ’—"F†—0¦Æ–W"†2WfW"†÷W6VBâ¢  ¢¢¤—B76W2&V6W6R'VÆRb6—2—G2F‡&VRFW7G2&R–æFWVæFVçBÂ–â2Öç’v÷&G2â¢¢FW7B"&VG0§F†R6WBöbfÖ–Æ–W2æBFW7B2F†R6WBöbF—f—6–öç2Â6ò&ööb—2FÖ—GFVBöâfÖ–Ç’F¶Vâ÷WBö`¦öæRF—f—6–öâæBF—f—6–öâF¶Vâ÷WBöbæ÷F†W"fÖ–Ç’âFööÇ2öÖV7W&UöF÷F–öå÷FW7G2ç’Ò×—'6À¦FFVB†W&RÂ&–çG2F†R6÷7C¢¢£#—'27&÷72‚G&FW2&RFÖ—GFVB'’F†R&ö¦V7F–öç2æB†÷W6VB'¦æ÷F†–ær¢¢ÂæBFW7BÆVfW2W†7FÇ’¢§Gvò¢¢öbF†VÒF÷F&ÆR(	BF†R6'VçFW'2rCB÷6÷WF‚æBF†P¦Æ&÷W&W'2rC"÷6÷WF‚Âv†–6‚&R&V6—6VÇ’F†RGvò&öög2WfW'’6V6öæB×&ööb&VgW6Â†2&VVâ&÷WBà¥6—‡FVVâ&VgW6Ç27&÷72æ–æR&Æö6·2vW&R&VgW6Ç2öb6æF–F7’76VÖ&ÆVBg&öÒWf–FVæ6RF†B—0¦æWfW"&÷WBF†R6ÖR&ööbGv–6Rà ¢¢¥D„R5E$”5DU"$TD”är•2äõBD´TâÂäBD„R$T4ôâ•24ôÔÔ•EDTB$D„U"D„â54U%DTBâ¢¢&WV—&–æp§F†R—"v÷VÆB&VgW6RF†R¢¦f÷W'FVVçF‚Æ&÷W&–ær†÷W6V†öÆB¢¢(	BBÔBw2C–âF†RvW7BF—f—6–öâÀ¦F÷FVBv†VâF†—2Æ–W"†÷W6VBÆ&÷W&W'2vW7BöbF†R&—fW"öæÇ’–âC"6†çF–W2ÂæB&wVVB–à¦W†7FÇ’F†R&ö¦V7FVBf÷&Òâ'VÆRbæÖW2F†BF÷F–öâ2öæRöbF†Rf÷W"—G2F†—&BFW7B§&V6÷fW'2¢À§6ò—"&VF–ær'&V·2F†R6Æ–'&F–öâF†R'VÆR&W7G2öââF†RFööÂ&W÷'G2—"†÷W6VF6öÇVÖà¦æBvFW2æ÷F†–æs²¢¥$ôDÔ³#‚æ÷r†2F‡&VRF†–æw2Fò6WGFÆR&F†W"F†âGvò¢¢ÂæBF†R6 §VW7F–öâ—Bv2÷VæVBf÷"Ö’&RVW7F–öâ&÷WBâV×G’6WBà ¢¢¥v†B—2VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6v2æ÷B'Vâ(	BF†P¦†&æW72626–ævÆR6öÖÖæBBFVâÖ–çWFW2æBF†RFW6·F÷†ÆbæVVG2&÷WBF†—'FVVâ…$ôDÔÀ¢'F†R'Vâ'VFvWB"’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†Æb&÷F‚76VBâF†—2&6VÂ6†ævW2æò&VæFW&W ¦6öFRæBæòvVöÖWG'“²v†B'&÷w6W"ÆöG2F†B—2æWr—2Gvòö67WçG6&Æö6·2æBF†RæÖW2öà£cr–çfVçFVBW'6öç2à ¢22f—†VB##bÓ‚ÓR(	BV'FW"öbF†RÖöFVÆÆVBÆæBv2æWfW"÷VâFò'V–ÆFW"ÂæBæ÷F†–ær6–B6ð ¢¢¥BÔS"¢¢ÂÆæR2w2f—'7B&6VÂgFW"BÔS&Vv—7FW&VBF†Rƒ36†VWBâGvòw&÷VæG2÷WG6–FRF†RÆ@¦&Ræ÷r&VgW6VC¢F†R¢¥Væ—FVB7FFW2&W6W'fF–öâ¢¢V7Böb7FFR7G&VWBæBF†R¢§6æB&"7&÷70§F†R&—fW"Ö÷WF‚¢¢à ¢¢¥F†RçVÖ&W"—2F†R&wVÖVçBâ¢¢öbF†R¢£#ã‚†¢¢öbÖöFVÆÆVBÆæB7FæF–ær&÷fRF†RvFW §7W&f6R–âF†—266VæRÂ¢£3"ã†(	B#bãRR¢¢—2öæR÷"F†R÷F†W#¢F†R&W6W'fF–öâ#"ãSr†ÂF†R& £’ãS2†âWfW'’vFRF†—2&ö¦V7B†B6¶VBv†WF†W"Æ6VÖVçB6ÆV&VB—G2æV–v†&÷W'2Â—G2Æ÷@¦Æ–æW2ÂF†RÆGFVB&öGv’ÂF†RÖöFVÆÆVBFW'&–âæBF†R&VÆ–VbâæöæRöbF†VÒ6¶VBv†WF†W"F†P¦w&÷VæBv2WfW"f÷"6ÆRâÃrf÷VæBF†B†öÆR–ç6–FRF†RÆBf—fRF—2rv÷&²vòæB6Æ÷6VB—@¦f÷"&Æö6·3²F†—2—2F†R6ÖR†öÆRv†W&R—B—2f÷W"F–ÖW2&–vvW"à ¢¢¤æ÷F†–ærÖ÷fVBÂ&V6W6Ræ÷F†–ærv2F†W&R–WB(	BæBF†B—2ÇV6²Âæ÷B'VÆRâ¢¢6WfVçFVVà§7G'V7GW&R&V6÷&G27FæBöâF†RGvòw&÷VæG2æBÆÂ6WfVçFVVâ¶VWF†V—"Æ6W3¢F†Rf÷'Bw27Fö6¶FRÀ§&FRæBVÆWfVâ'V–ÆF–æw2ÂF†Rv'&—6öâv&FVâÂF†Rƒ3"Æ–v‡F†÷W6RÂ&VV&–Vâw2†öÖW7FVBæ@¦&&âÂæBF†R6÷WF‚–W"Âv†–6‚F÷V6†W2&÷F‚â¢¥¦W&òæöç–Ö÷W2&öög2â¢¢WfW'’&V6—R6òf"†2&VVà¦¶W–VBFòÆGFVB&Æö6²ÂæBF†R&W6W'fF–öâv2æWfW"ÆGFVBÂ6òF†Rw&÷VæBv27&VB'’F†P¦÷&FW"F†Rv÷&²†VæVB–ââF†RvFRÆæG2w&VVâöâF†RF’—B—2w&—GFVâÂæB&÷F‚öb—G0¦76W'F–öç2vW&R&÷fVBFòf–Â&Vf÷&R—Bv2G'W7FVC¢&VÖ÷f–æröæRW&Ö—76–öâf–Ç2—B'’æÖRÂæ@§6‡&–æ¶–ærF†R&"öÇ–vöâFò6Æ—fW"f–Ç2F†RVæFW"Ö6÷fW&vR6÷VçBv—F‚Ã6VÆÇ2à ¢¢¥D„R$TeU4Â•2Dô5TÔTåDTC²D„R$õTäD%’•2”ädU%$TBÂDU$•dTBÂäB„ôäU5DÅ’4„õ%Bâ¢¢æG&V2v—fW0§F†R&W6W'fF–öâ2sRãc’7&W2ÂF†R6÷WF‡vW7Bg&7F–öæÂV'FW"öb6V7F–öâ(	BVçÆGFVBÂ÷WG6–FP§F†RF÷vâw2÷vâV7FW&â&÷VæF'’ÂæBVæFW"&VV&–Vâw2f—fR×vVV²ÖöÆB&RÖV×F–öâ6Æ–ÒöâF†R66VæP¦FFRâæ÷BöæRfW'FW‚öbF†RöÇ–vöâ—2WF†÷&VC¢—G2vW7BæB6÷WF‚6–FW2&RF†RV'FW"w2Gvð§7W'fW’Æ–æW2&W6öÇfVBg&öÒF†R6–ævÆR6öçG&öÂö–çBw&–v‡Eóƒ3Eöv72æ§6öæ¢¤s¢¢Âv†÷6R÷vâæ÷FP¦†26–B6–æ6RF†RFGVÒv÷&²F†BÖF—6öâw2Æ–æR6öçF–çVW2V7B2F†R&W6W'fF–öâw26÷WF€¦&÷VæF'“²—G2F†—&B6–FR—2F†R6öÖÖ—GFVBvFW&Æ–æRF†RG&6RÇ&VG’6ÆÇ2F†R&W6W'fF–öâw2Æ¶P§6†÷&Râ¢¥F†RFW&—fVBöÇ–vöâ6öÖW2FòcRãs7&W2v–ç7BF†RFö7VÖVçFVBsRãc’(	B2ã"R6†÷'B(	Bæ@¦—B—2æ÷BGVæVBFò6Æ÷6RF†Rvâ¢¢F†R6æF–FFW2†ÖVæFW"Æ–æRV7BöbF†Rƒ3BvFW&Æ–æRÂF†P§G&6Rw2÷vâ²òÓ#ÒÂ6†÷&RG&6RF†BÆVfW2—G2v–æF÷r6÷WF‚öbÖF—6öâ’&RæÖVBæBæöæR—0¦ÖV7W&VBà ¢¢¥6òF†RöÇ–vöâ—2fÆö÷"ÂæBF†RfÆö÷"—26†V6¶VB&F†W"F†âG'W7FVBâ¢¢F†RvFR&RÖ6÷VçG2Âöà¦WfW'’6†V6²ç6†ÂF†R6VÆÇ2öbÖöFVÆÆVBÆæB&÷fRF†RvFW"7W&f6RF†B7FæBV7BöbF†RvW7@¦Æ–æRÂæ÷'F‚öbÖF—6öâÂ6÷WF‚öbF†RÖ–â7FVÒæB–ç6–FRæV—F†W"öÇ–vöââFöF’F†B6÷VçB—0¢¢§¦W&ò¢¢(	BF†RöÇ–vöç2&V6‚WfW'’7V&RÖWG&Röbw&÷VæBF†RFW'&–âÖöFVÇ2F†W&Râ¢¥BÔS2W‡FVæG0§F†RFW'&–âV7BæB6÷WF‚ÂæBF†B—2F†R&6VÂF†—276W'F–öâW†—7G2Fò6F6‚â¢  ¢¢¥7F–ÆÂ÷VâÂæB†öæW7FÇ’÷Vã¢¢¢f÷W"7G'V7GW&W2F†Rƒ3ÆFRG&w2(	BÖ&²&VV&–Vâw2À¤VÆ–¦‚vVçGv÷'F‚w26&–âÂÆg&Ö&ö—6Rw26&–âæB7F÷&RÂ÷'FW"w2Æör6&–â(	B†fRæò&V6÷&BÂæð¦W†6ÇW6–öâæBæòFW7FVB7W'f—fÂFòƒ3RÓrÓâBÔS"Æ—7G2F†VÒ2÷VâVW7F–öç2&F†W"F†à¦–çfVçF–ærF—7÷6—F–öç2Â–âF†RæWrF—7÷6—F–öâF&ÆRBF†Rfö÷Bö`¦Fö72õ$U4T$4‚ö6†–6võóƒ3ö6Æ–×2æÖFâ¢¤Ö&²&VV&–Vâw2—2F†RöæR–ç6–FRF†RÖöFVÆÆVB&Vâ¢ ¥F†R&W6W'fF–öâw2÷vâ&W6–GVR—2&V6÷&FVBFöó¢F†RSc"6VÆÇ2F†Rf—'7B72fÆvvVB0§Væ6Æ76–f–VBGW&æVB÷WBFò&RVçF—&VÇ’F†RvFW&Æ–æRFöÆW&æ6R&æBÂWfW'’öæRöbF†VÒ&WGvVVà¢ÓãÒæBãÒÂæBæöæRöbF†VÒw&÷VæBà ¢22æWr##bÓ‚ÓR(	BF†RF÷vâw2V&Æ–27V&Rv2&V–æröffW&VBFò–çfVçFVB†÷W6W2ÂæBGvòFö7VÖVçFVBöæW2vW&RÇ&VG’7FæF–æröâ—@ ¢¢¥BÔbâ¢¢&Æµ÷&æFöÇ…öÆ6ÆÆV(	B&æFöÇ‚Â6Æ&²Âv6†–æwFöâÂÆ6ÆÆR(	Bv26Æ–ÖVB2F†RÆ7@¦÷Vâ&Æö6²VçG'’öâ—G2&÷ræB¢§v2æ÷B'V–ÇB¢¢â—B—2¢§F†RV&Æ–27V&R¢£¢æG&V26ÆÇ2—@¢§F†R7V&R¢æB§F†R6÷W'BÖ†÷W6R7V&R¢ÂF†—2&ö¦V7Bw2÷vâw&÷VæB6öçG&öÂæÖW2—G26÷&æW'0¢¤årò4R6÷&æW"öbF†RV&Æ–27V&R&Æö6²¢ÂæB—B6'&–W2F†RW7G&’Vâ†—G26÷WF‚×vW7B6÷&æW"À¤Ö&6‚ƒ32Â6†–6vòw2f—'7BV&Æ–2'V–ÆF–ær’ÂF†RÆör¦–Â†æ÷'F‚×vW7BÂfÆÂƒ32’æBF†Rf—'7@¤6öö²6÷VçG’6÷W'BÖ†÷W6Rƒƒ3R’âF†RccR×&ööb&öw&ÖÖRv2FVÆ–ær—Bf÷W"–çfVçFVB&—fFR&öög2(	@¦âÂC6ÂCFæBCVâF†R&Æö6²—2æ÷r¢§&W6W'fVB¢£¢æòÆ÷G2Âæò&öög2Â&VgW6Â–à§F†R&Æö6²vVæW&F÷"ÂæBvFR–â6†V6²ç6†â¢¥7FæF–ær&öög2Væ6†ævVBB3##²&VÖ–æ–ær3C2Â¦öbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v2R(	BF†R7V&R†VÆBf÷W"öbF†Rf—fR’âF†RÆBw&–BG&÷2g&öÐ£S"Æ÷G2Fò¢£CB¢¢â&V6÷&FVB–â¢¤Ãr¢¢à ¢¢¤UdU%’Ä4TÔTåBtDRD„•2$ô¤T5B„254TBD„REtò%T”ÄD”äu2D„BtU$R5DäD”ärôâ•BÂäBD„@¤•2D„R„TDÄ”äRâ¢¢w&–v‡Eö'V–ÆF–æu÷FõöÆWEöæBö&Â¦ö†âw&–v‡Bw2GvòFö7VÖVçFVB6÷GFvW2Fð¦ÆWBÂvW&RÆ6VB–â¢'F†R6÷WF‚F—f—6–öâ&æBF†R&V6—W2W6Rf÷"÷&F–æ'’GvVÆÆ–æw2"¢æBF†B&æ@§&â7&÷72F†R7V&RâF†V—"Æ6VÖVçBv2FW7FVBf÷"6ÆV&æ6Rg&öÒ÷F†W"'V–ÆF–æw2Âf÷"—G2÷và¦Æ÷BÆ–æW2Âf÷"F†RÆGFVB&öGv’æBf÷"'V–ÆF&ÆRw&÷VæB(	BWfW'’VW7F–öâF†—2&ö¦V7B¶æWr†÷p§Fò6²&÷WB÷6—F–öâÂæB¢¦æ÷BöæRöbF†VÒv2v†WF†W"F†Rw&÷VæBv2f÷"6ÆR¢¢âF†W’†fR&VVà¦Ö÷fVC¢V6‚F¶W2F†RæV&W7Bg&VRÆGFVBÆ÷Bæò6öÖÖ—GFVB&Æö6²&V6—R†2Ç&VG’7ö¶Vâf÷"Âƒ2Ð¦æBc’ÒÂöçFòF†R&æFöÇ‚g&öçFvRöbF†RGvò&Æö6·2f6–ærF†R7V&RâF†R—"—27Æ—BÂæBF†P§7Æ—B—27FFVB(	BF†RöæÇ’w&÷VæBF†B¶WBF†VÒöâöæR&Æö6²v2#ÒgW'F†W"öfbæBf6VBGvð¦F–ffW&VçB7G&VWG2ÂæBöæRGfW'F—6VÖVçBöffW&–ærGvò'V–ÆF–æw2æWfW"6–BF†W’6†&VB†öÆF–ærà ¢¢¥F†RFVfV7B—2W7G&VÒöbF†R66†VGVÆRâ¢¢FööÇ2övVæW&FU÷ÆEöÆ÷G2ç–7V&F—f–FW2WfW'’&Æö6²—@¦6â'V–ÆBÂ&V6W6RF†B—2v†BF†RF†ö×6öâÖöGVÆR6—2&Æö6²—3²—B†2æòv’Fò6²v†WF†W"¦&Æö6²v2WfW"öffW&VB–âÆ÷G2â6òF†R&W6W'fF–öâv—F†G&w2F†R¢¦Æ÷BÆ–æW2¢¢æBæ÷BÖW&VÇ’F†P§66†VGVÆRw2W&Ö—76–öâFòW6RF†VÒÂæBÆ÷G5÷W%öf6U÷v—F††VÆF&V6÷&G2v†BF†RÖöGVÆRv÷VÆB†fP¦G&vâ6òF†Rv—F†G&vÂ—2f—6–&ÆR&F†W"F†âÆöö¶–ærÆ–¶RvVæW&F÷"f–ÇW&Rà ¢¢¥D„R$U4U%dD”ôâ•2–æfW'&VFäB•2äõB$ôÔõDTBâ¢¢æò6÷W&6RF†—2&ö¦V7B†öÆG27FFW2F†BF†P§7V&Rv2&W6W'fVBg&öÒ6ÆRâv†B—B†öÆG2—2F†R&Æö6²w2æÖRÂF†R6÷VçG’w2F‡&VR'V–ÆF–æw2öà¦—BÂF†RF÷76–W"w2÷vâ&VF–æröbF†R&W7Böb—B(	B¢&÷VâÂVæ–×&÷fVBÂfVæ6VB÷"VæfVæ6VB&—&–P¦&Æö6²"¢(	BæBöæRW&–öBFW67&—F–öâöbF†Rw&÷VæB—G6VÆc¢¢$÷W"V&Æ–27V&Rv2F†VâöæBÀ§v†W&RF†R–æF–ç2†BG&VBF†R×W6·&BÂæBv†W&RF†Rf—'7B6WGFÆW'2‡VçFVBGV6·2â"¢F†Rw&FP§7F—2v†W&RF†RWf–FVæ6RWG2—BÂæBFööÇ2öÖV7W&U÷&W6W'fVEöw&÷VæBç–&–çG2v†B&VgWFF–öà§v÷VÆB6†ævRà ¢¢¥D„RôäB•2Dô5TÔTåDTBäB•2äõBÔôDTÄÄTB(	BBÔSRâ¢¢F†RFW'&–â6'&–W2æò7FæF–ærvFW"öâF†—0¦&Æö6²æBF†RÖ'6‚fÆ÷&¦öæR—2'VffW"öbF†RÖVBvFW"Â6òF†R7V&R&VæFW'22G'’&—&–P§v—F‚F‡&VRV&Æ–2'V–ÆF–æw2öâ—BâF†B—26V6öæBfÇ6R7FFVÖVçB&÷WBF†R6ÖRw&÷VæBâ—B—0¦÷VæVB&F†W"F†â6Æ÷6VB†W&RÂv—F‚F†RF‡&VRVW7F–öç2F†B†fRFò&R6WGFÆVB&Vf÷&Rç’w&÷Væ@¦Ö÷fW2à ¢¢¥F†RVÆWfVçF‚³#ÖV7W&VÖVçB—2öb¢¢6'&–VBÖ÷fW"–çfVçFVBW'6öç2&VæÖVBÂv–ç7B"ÖöbÓ ¦BBÔRæB&ævRöbr^(	3s"R÷fW"F†Ræ–æR&Vf÷&R—Bâ¦W&òf÷"7G'V7GW&Â&V6öã¢¢§F†—2&6VÀ¦–ç6W'G2æB&VÖ÷fW2æòW'6öâ¢¢Â6òF†RÆÆö6F÷"†2æ÷F†–ærFò6†–gBâF†B—2F†Rf—'7BWf–FVæ6R–à¦æ–æRÖV7W&VÖVçG2&÷WB§v†B¢W'GW&'2—Bà ¢¢¥VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6(	BF†—2&6VÂ6†ævW2FFÂFööÇ0¦æBFö72öæÇ’ÂæBF†RFW6·F÷†ÆbFöW2æ÷Bf—BF†R'VææW"w2FVâÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ær‡6VP¥$ôDÔ*rD„R%Tâ%TDtUB’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbF†R6Öö¶RvW&R&÷F‚'Vâw&VVà¦v–ç7BF†RV&Æ—6†VBÖ—'&÷"à ¢22æWr##bÓ‚ÓR(	BF†R&Æö6²÷÷6—FRF†R6÷W'F†÷W6RÂæBGvòöb–W7FW&F’w2F‡&VRF÷F–öâ6æF–F6–W2Fòæ÷B&W&öGV6P ¢¢¥BÔRâ¢¢&Æµ÷&æFöÇ…ö6Æ&¶(	B&æFöÇ‚ÂFV&&÷&âÂv6†–æwFöâÂ6Æ&²(	Bæ÷r6'&–W2¢¦V–v‡@¦æöç–Ö÷W2&öög2¢£¢7F÷&R×&W6–FVæ6RÂf—fRGvVÆÆ–æw2ÂvööG6†VBæB&—g’Âöâ6—‚öb—G26WfVà¦g&VRÆ÷G2Âv—F‚Æ÷BÆVgB÷VâæBÆ÷B†VÆB'’F†R–æfW'&VBwVç6Ö—F‚w26†÷â¢¥7FæF–ær&öög0£3B(i"3##²&VÖ–æ–ær3S(i"3C2ÂRöbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v22’â–æfW'&VB†÷W6V†öÆG2“‚(i"“’À¦–æfW'&VBW'6öç2(i"â&V6÷&FVB–â¢¤Ãb¢¢â¢¥F†R&V6—R6ÆV&VBWfW'’Æ6VÖVçBvFRöâ—G0¦f—'7B'Vâ¢¢(	BF†RV–v‡F‚&Æö6²–â&÷râF†R&Æö6²7FæG27&÷726Æ&²7G&VWBg&öÒF†RV&Æ–27V&P¢†6÷VçG’6÷W'F†÷W6RÂ&÷F‚w&–v‡B'V–ÆF–æw2FòÆWBÂF†RW7G&’Vâ’v—F‚FV&&÷&â7G&VWBÂF†R'&–FvP§7G&VWBÂf÷"—G2V7Bf6S²—B—2F†Rf—'7B&Æö6²&6VÂFVÇB¢¦&÷F‚¢¢Æ&vW"†÷W6RfÖ–Æ–W2Böæ6P¦æBF†Rf—'7BFò7FæB¢¦3&7F÷&R×&W6–FVæ6R¢¢âöæRF÷F–öã¢F†RCÆör6&–âöâÆ÷B2&V6öÖW0§F†RGvVçG’×6V6öæB–æfW'&VBÆ&÷W&–ær†÷W6V†öÆBà ¢¢¥EtòôbBÔBw2D…$TRDõD”ôâ4äD”D4”U2DòäõB$U$ôET4RÂäBD„•2•2D„R„TDÄ”äRâ¢¢F†RVçG'¦F—&V7FÇ’&VÆ÷r&V6÷&G2F†B—G2C&76W2ÆÂF‡&VRöbÖWF†öB'VÆRbw2FW7G2f÷"F†P¢¢¦ÆVæG&W76W2¢¢æB—G2CFf÷"F†R¢§FV×7FW'2¢¢âFW7G2"æB2†öÆBf÷"&÷F‚â¢¥FW7BFöW0¦æ÷B¢£¢'VÆRb6·2v†WF†W"F†RG&FRw2¦÷vâ&wVÖVçB¢7FFW2–â—G26öÖÖ—GFVBFW‡BF†B—G26÷VçB—0¦fÆö÷"&F†W"F†â&÷VæBÂæBæV—F†W"öbF†÷6R&wVÖVçG26öçF–ç2ç’7V6‚7FFVÖVçB(	BF†RöæÇ¦ö67W'&Væ6RöbF†Rv÷&B–âF†RÆVæG&W72&wVÖVçB—2æG&V2w2¢'v—F‚F†RfÆö÷"6÷fW&VB&W6–FW2"¢Â§Ææ²fÆö÷"–â&ö&F–ær†÷W6RâöæÇ’F†R¢¦6'VçFW'2¢¢æBF†R¢¦Æ&÷W&W'2¢¢7FFR—Bà¦FööÇ2öÖV7W&UöF÷F–öå÷FW7G2ç–—26öÖÖ—GFVB6òF†RæW‡B&6VÂ¢§'Vç2¢¢'VÆRb&F†W"F†à§&V6ÆÆ–ær—BÂæB&–çG2F†R6VçFVæ6RV6‚fW&F–7B&W7G2öââF†RBÔBVçG'’&VÆ÷ræBÃR&RÆVg@§7FæF–ærfW&&F–Ó²v†B—26÷'&V7FVB—2F†RÖWF†öBâ¢¤³#‚w2VW7F–öâæ'&÷w2¢£¢æ÷B&Ö’G&FP§F†B†2æ÷B6¶VBf÷"&ööb&Rv—fVâöæR"'WB&FöW2FW7BÖVâF†RG&FRw2÷vâFW‡BÂ÷"ÖWF†ö@§'VÆR2w2Æ—7BöbVæ&÷VæFVBG&FW2"(	BGvò&VF–æw2F†BF—6w&VRf÷"W†7FÇ’GvòG&FW2â'VâöâF†—0¦&Æö6²w2C&ÂW†7FÇ’öæRG&FR76W3¢F†RÆ&÷W&W'2ÂF¶–ær6V6öæB&ööbÂ&VgW6VBf÷"F†RV–v‡F€§F–ÖRöâF†R6ÖR6öç6W'fF—fR&VF–ærà ¢¢¥F†Rf6R'VÆR&W&öGV6VBW†7FÇ’(	BF†Rf—'7BF–ÖRF†B6â&R6–Bâ¢¢FööÇ2ð¦ÖV7W&U÷7G&VWEög&öçFvRç’&æFöÇ‚v6†–æwFöæ&WGW&ç2&æFöÇ‚r&W6V&6‚òr–æfW'&VBÖ†÷W6V†öÆ@¦v–ç7Bv6†–æwFöâòÂF†R6ÖRBv–ç7BBÔBÖV7W&VBöâF†R6ÖR—"Âg&öÒ6öÖÖæ@§&F†W"F†âg&öÒÖVÖ÷'’âF†RF†—&BÆ–W"&VB‚æB"æB—2W†6ÇVFVBÂæ÷BÖW&vVBà ¢¢¥F†Rf6R'VÆR&æ·2GvVÆÆ–æw2ÂæBF†—2&Æö6²†B7F÷&RÂ6òF†R'VÆRv2U…DTäDTB(	B6VR³3"â¢ ¤7F÷&R×&W6–FVæ6Rw26Æ–ÒöâF†R&WGFW"g&öçFvRv2F¶VâFò&RgVæ7F–öæÂ&F†W"F†â6ö6–ÂÂ6ð§F†R3&Föö²&æFöÇ‚w2F†—&Bg&VRÆ÷BæBF†RCfF†Bv÷VÆB†fR†B—BvVçBFòF†R†VBöbF†P¦&6²7G&VWBâF†B—2â–çfVçF–öâ&÷WBƒ3R6öÖÖW&6RÖFR'’âvVçC²—B—2fÆvvVB&F†W"F†à¦ÆVgBFò&WVBÂæB¢¤³#’—26—&6Æ–ærF†R6ÖRVW7F–öâg&öÒF†R÷F†W"6–FR¢¢à ¢¢¥D„RTäB%TÄR•2U„„U5DTBôâD„•2$õr(	B6VR³3â¢¢F—7Fæ6RFòF†RFV&&÷&â7G&VWBG&v'&–FvR'Vç0¢¢£3‚ã2ò3#ãò3#Rã‚Ò¢¢7&÷72F†R&æFöÇ‚g&öçFvRæB3sbãB(i"3ƒ‚ã"Ò&V†–æBâf"öæV"öâF†P¦g&öçBf6R—2¢£ã,9r¢¢v–ç7BBÔBw2ãÂBÔ2w2ã2æBBÔ"w2"ã“2ÂæBF†R'6öÇWFR7&V@¦—2¢£rãRÒ¢¢(	BVæFW"F†—&BöböæRÆ÷Bw2#BãbÒg&öçFvRâF†R6W6R—2vVöÖWG&–3¢F†R'&–FvR&V'0¢¢£ãL+V7Böbæ÷'F‚¢¢g&öÒF†R&Æö6²6VçG&Rv†–ÆRF†Rf6R'Vç2V7N(	7vW7BÂ6òF†R7&—FW&–öâ6VW0¦öæÇ’¢£‚R¢¢öbç’Æöær×7G&VWBF—7Æ6VÖVçBâ—Bv2föÆÆ÷vVBç—v’öâBÔ2w2&V6öæ–ærÂæBöà§F†—2&Æö6²7G&öævW"7&—FW&–öâw&VW2v—F‚—B†Æ÷Bb—2F†R6÷&æW"öâFV&&÷&âÂF†R'&–FvR7G&VWB’À§v†–6‚—2W†7FÇ’v†B³3×W7Bæ÷B77VÖR†öÆG2VÇ6Wv†W&Râ¢¤Fòæ÷BV÷FRF†RVæB'VÆR2–b—@¦÷&FW&VBç—F†–æröâF†R&æFöÇŽ(	5v6†–æwFöâ&÷rv—F†÷WB&RÖÖV7W&–ær—Bâ¢  ¢¢¥VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6(	BF†—2&6VÂ6†ævW2FFæ@¦Fö72öæÇ’ÂæBF†RFW6·F÷†ÆbFöW2æ÷Bf—BF†R'VææW"w2FVâÖÖ–çWFRW"Ö6öÖÖæB6V–Æ–ær‡6VP¥$ôDÔ*rD„R%Tâ%TDtUB’âFööÇ2ö6†V6²ç6†æBF†RÖö&–ÆR†ÆböbF†R6Öö¶RvW&R&÷F‚'Vâw&VVà¦v–ç7BF†RV&Æ—6†VBÖ—'&÷"à ¢22æWr##bÓ‚ÓR(	B&Æö6²v—F‚æòg&öçBÂæBF†Rf6R'VÆRw2f—'7BÖV7W&VÖVçBFöW2æ÷B&W&öGV6P ¢¢¥BÔBâ¢¢&Æµ÷&æFöÇ…ög&æ¶Æ–æ(	B&æFöÇ‚ÂvVÆÇ2Âv6†–æwFöâÂg&æ¶Æ–â(	Bæ÷r6'&–W2¢¦V–v‡@¦æöç–Ö÷W2&öög2¢¢Â6—‚&–æ6—ÂÂ7F&ÆRæB&—g’Âöâ6—‚öb—G26WfVâg&VRÆ÷G2Âv—F‚Æ÷B¦ÆVgB÷VâæBÆ÷B"†VÆB'’†&Ööâw2Æör6&–ââ¢¥7FæF–ær&öög23b(i"3C²&VÖ–æ–ær3S’(i"3SÂ0¦öbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v2#’â–æfW'&VB†÷W6V†öÆG2“b(i"“‚Â–æfW'&VBW'6öç2‚(i"à¥&V6÷&FVB–âÃRâ¢¥F†R&V6—R6ÆV&VBWfW'’Æ6VÖVçBvFRöâ—G2f—'7B'Vâ¢¢(	BF†R6WfVçF‚&Æö6²–à¦&÷r(	BæB—B—2F†Rf—'7B&Æö6²&6VÂöbF†—26†RFò6öÖÖ—BFööÂÂf÷"F†R&V6öâ&VÆ÷râ—B—0§F†Rf—'7B&Æö6²öâF†R&÷r¢§Gvò7G&VWG2&6²¢¢ÂæBF†Rf—'7B¢¦æV—F†W"öbv†÷6Rf6W2F†RF÷vâw0§&V6÷&B6ÆÇ2g&öçB¢¢à ¢¢¥BÔ2u2d4RÕ%TÄRÔT5U$TÔTåBDôU2äõB$U$ôET4RÂäBD„•2•2D„R„TDÄ”äRâ¢¢F†RVçG'’F—&V7FÇ¦&VÆ÷r&W÷'G2¢¤Æ¶R"Â&æFöÇ‚"Â6÷WF‚vFW"’¢¢f÷"&WfW'’Fö7VÖVçFVB÷"–æfW'&VB7G'V7GW&P§v†÷6Rfö÷G&–çB6VçG&ö–B7FæG2v—F†–â#RÒöb7G&VWBw26öÖÖ—GFVB6VçG&VÆ–æR"âæòf–ÇFW §&V6÷fW&&ÆRg&öÒF†—2&W÷6—F÷'’&öGV6W2F†÷6RçVÖ&W'2(	BF†R7FFVBöæRv—fW2¢¤Æ¶Rrò&æFöÇ‚p¢ò6÷WF‚vFW"B¢¢öâF†R&W6V&6‚Æ–W"ÆöæR(	BæBF†Rf–ÇFW"7GVÆÇ’W6VBv2æWfW"w&—GFVâF÷vâà¥F†R§VFvVÖVçB—B7W÷'FVB7W'f—fW2WfW'’f–ÇFW"G&–VB„Æ¶R—2F†R&WGFW"f6R'’v–FRÖ&v–â“°§v†Bf–ÆVB—2¢§&W&öGV6–&–Æ—G’¢¢Âv†–6‚öâ&ö¦V7Bv†÷6R&öGV7B—2&÷fVææ6R—2F†RÖ÷&P§6W&–÷W2öbF†RGvòâFööÇ2öÖV7W&U÷7G&VWEög&öçFvRç–—26öÖÖ—GFVB6òF†RæW‡B&6VÂ'Vç2F†P¦ÖV7W&VÖVçB&F†W"F†â&VÖVÖ&W&–ær—Bâ¢¥F†RBÔ2VçG'’&VÆ÷r—2ÆVgB7FæF–ærfW&&F–Ò¢¢ÂæB6ð¦—2ÃC¢Ä”$U%D”U2æÖB—2VæBÖöæÇ’æBv†B—26÷'&V7FVB—2F†RÖWF†öBà ¢¢¥F†R6÷VçB&W÷'G2—G2F‡&VRWf–FVæ6RÆ–W'26W&FVÇ’æBæWfW"7V×2F†VÒâ¢¢F†Ræöç–Ö÷W2&öög0§F†R&Æö6²&6VÇ2F†V×6VÇfW2Æ6R7FööBB¢£Röâ&æFöÇ‚æB’öâv6†–æwFöâ¢¢v†VâF†—0¦'&ævVÖVçBv26†÷6VâæB&VB¢£‚æB"¢¢F†RÖöÖVçBF†R&6VÂ'V–ÇB(	Bf6R'VÆR6÷VçF–ærF†@¦Æ–W"&VG2F†R&öw&ÖÖRw2÷vâ÷WGWB&6²2Wf–FVæ6RâW†6ÇVFVBÂF†—2&Æö6²w2ç7vW"—2¢£@¦v–ç7B¢£¢&æFöÇ‚6'&–W2r&W6V&6‚ÖÆ–W"&V6÷&G2æBr–æfW'&VBÖ†÷W6V†öÆB'V–ÆF–æw2Âæ@¢¢¥v6†–æwFöâ7G&VWBw2VçF—&RFö7VÖVçFVBƒ3Rg&öçFvR—2F†RW7G&’Vâ¢¢ÂF†RF÷vâw2÷VæBf÷"7G&¦æ–ÖÇ2à ¢¢¥F†RVæB'VÆRw27&VB†2F†–ææVBf÷"6V6öæB&Æö6²'Vææ–ærâ¢¢F—7Fæ6RFòF†RFV&&÷&â7G&VW@¦G&v'&–FvR'Vç2¢£S#rã‚Ò¢¢BÆ÷BbFò¢£SƒBãÒ¢¢BÆ÷BöâF†R&æFöÇ‚g&öçFvRæB¢£Sc‚ãRÒ¢ ¦BÆ÷BrFò¢£c#ãÒ¢¢BÆ÷B&V†–æBâF†Rf"VæBöbF†Rg&öçBf6R7FæG2¢£ã9r¢¢2f"g&öÐ§F†R'&–FvR2F†RæV"VæBÂv–ç7BBÔ2w2ã2æBBÔ"w2"ã“2ÂæBF†Rg&öçBf6Rw2'6öÇWFP§7&VB—2¢£Sbã"Ò¢¢v–ç7BBÔ2w2c‚ã"ÒâföÆÆ÷vVBç—v’öâBÔ2w2&V6öæ–ærÂæB&V6÷&FVB0¦6Æ÷6W"Fò&&—G&'’F†â÷&FW&VBà ¢¢¥F†R'6V6öæB&ööb"VW7F–öâ†2&VVâF†Rw&öærVW7F–öâf÷"6—‚&Æö6·2â¢¢F†RCBæBC"F†BWfW'¦&Æö6²6–æ6RBÔ’†2&VgW6VB2§6V6öæB¢&öög2f÷"F†R6'VçFW'2æBÆ&÷W&W'2&RÇ6òF†P¢¢¦f—'7B¢¢&öög2öbF†R¢§FV×7FW'2¢¢æBF†R¢¦ÆVæG&W76W2¢¢(	BF†R÷F†W"GvòöbÖWF†öB'VÆR"w2f÷W §Væ&÷VæFVBG&FW2ÂV6‚†÷W6VB–âF†BöæRfÖ–Ç’æBæò÷F†W"ÂV6‚Ç&VG’–âF†R6÷WF‚F—f—6–öâÀ¦V6‚76–ærÆÂF‡&VRöb'VÆRbw2FW7G2öâF†÷6R&öög2â¢¥6—‡FVVâæöç–Ö÷W2C"æBCB&öög27FæB–à§F†R6÷WF‚F—f—6–öâVæFW"W†7FÇ’F†BFW67&—F–öââ¢¢³#‚—26WGFÆ–ærÆ&vW"VW7F–öâF†â—Bv0¦÷VæVBöã¢æ÷Bv†WF†W"G&FRÖ’F¶R6V6öæB&ööbÂ'WBv†WF†W"'VÆRbÖ’†æB&ööbFòG&FP§F†BæWfW"6¶VBf÷"öæRà ¢¢¥F†Ræ–çF‚³#ÖV7W&VÖVçB—2cöb‚¢¢6'&–VBÖ÷fW"–çfVçFVBW'6öç2&VæÖVBÂv–ç7BcrÖöbÓ`¦BBÔ2æBrÖöbÓ"BBÔâ6WfVâÖV7W&VÖVçG27ârRFòs"Rv—F‚æ÷F†–ærf—†VB÷"'&ö¶Và¦&WGvVVâF†VÒâ³#7F–ÆÂ÷vç2F†Rf—‚à ¢¢¥VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†Æböb6Öö¶U÷&VæFW&W"æÖ§6FöW2æ÷Bf—BF†—2'VææW"w2FVâÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–æræBv2æ÷B'Vã²F†RÖö&–ÆR†Æbv2ÂæBFööÇ2ö6†V6²ç6†(	Bv†–6‚—2F†RFW`¦vFR(	B76VBâ6VRF†R'VâÖ'VFvWB&÷‚–â$ôDÔà ¢22æWr##bÓ‚ÓR(	BF†Rf—'7B&Æö6²öfbF†R'W6–æW72g&öçBÂæBF†R'VÆRF†B'&ævVBF†R&÷r7F÷2ÖVæ–ærç—F†–æröâ—@ ¢¢¥BÔ2â¢¢&ÆµöÆ¶UöÖ&¶WF(	BÆ¶RÂg&æ¶Æ–âÂ&æFöÇ‚ÂÖ&¶WB(	Bæ÷r6'&–W2¢§6WfVâæöç–Ö÷W0§&öög2¢¢Âf—fR&–æ6—ÂÂ7F&ÆRæB&—g’Âöâf—fRöb—G26—‚g&VRÆ÷G2Âv—F‚Æ÷B2ÆVgB÷Vâæ@¦Æ÷G2æB†VÆB'’F†R6Vvæ6‚†÷FVÂv—F‚†–Æò6'VçFW"w2ÆörG'Vr7F÷&RÂæB'’F†R6¶W"w0¦GvVÆÆ–ærâ¢¥7FæF–ær&öög2#“’(i"3c²&VÖ–æ–ær3cb(i"3S’Â#öbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v2#‚’à¤–æfW'&VB†÷W6V†öÆG2“B(i"“bÂ–æfW'&VBW'6öç2b(i"‚â&V6÷&FVB–âÃBâ¢¥F†R&V6—R6ÆV&VBWfW'§Æ6VÖVçBvFRöâ—G2f—'7B'VâæBæòFööÂ6†ævVB¢¢(	BF†R6—‡F‚&Æö6²–â&÷râ—B—2F†R¢¦f—'7@¦&Æö6²öbF†—2&6VÂ6†RF†B—2æ÷Böâ6÷WF‚vFW"7G&VWB¢£²WfW'’÷VâVçG'’ÆVgB–âF†R66†VGVÆP¦—2öâ&æFöÇ‚à ¢¢¥F†Rf6R'VÆRv276W'FVBf—fRF–ÖW2æB—2ÖV7W&VB†W&RÂ&V6W6RæV—F†W"öbF†—2&Æö6²w2f6W0¦—26÷WF‚vFW"â¢¢f—fR&6VÇ26VçBF†V—"&WGFW"GvVÆÆ–æw2Fò'F†R'W6–æW72g&öçB"æBæÖVBF†@¦g&öçB'’F†R7G&VWBw2Fö7VÖVçFVBW6R(	Bv†–6‚6—2æ÷F†–ær&÷WB&Æö6²&÷VæFVB'’Æ¶RæB&æFöÇ‚à¤6÷VçF–ærWfW'’Fö7VÖVçFVB÷"–æfW'&VB7G'V7GW&Rv†÷6Rfö÷G&–çB6VçG&ö–B7FæG2v—F†–â¢£#RÒ¢¢öb§7G&VWBw26öÖÖ—GFVB6VçG&VÆ–æS¢¢¤Æ¶R"Â&æFöÇ‚"Â6÷WF‚vFW"’â¢¢Æ¶Rw2GvVÇfR&RF†P¥6Vvæ6‚ÂF†Rw&VVâG&VRÂF†RW†6†ævR6öffVR†÷W6RÂF†RG&VÖöçBÂF†RÖç6–öâ†÷W6RÂ&÷F‚6‡W&6†W2À¤†övâw27F÷&RÂv÷72b6ö&"w26FFÆW'’Â–W&6Rw2&Æ6·6Ö—F‚6†÷ÂFöÆRw26÷WF‚v&V†÷W6Ræ@¤6'VçFW"w2Æör6†÷²&æFöÇ‚w2Gvò&RF†RÆör¦–ÂæBF†RvW7FW&â†÷FVÂâF†R'VÆRæ÷r&W7G2öâ¦ÖV7W&VÖVçB&F†W"F†â†&—BÂ¢¦æB—B—27F–ÆÂâ–çfVçF–öâ¢£¢æò6÷W&6R6—2&WGFW"GvVÆÆ–æp§7FööBöâF†R&WGFW"7G&VWBà ¢¢¥F†RVæB'VÆRw2÷&FW"7W'f—fW2æB—G2ÖVæ–ærFöW2æ÷BÂæBF†B—2F†Rf–æF–ærâ¢¢BÔw0¦7&—FW&–öâ(	BF—7Fæ6RFòF†RFV&&÷&â7G&VWBG&v'&–FvR(	B'Vç2¢£S3"ã"Ò¢¢BÆ÷BbFò¢£cãBÒ¢¢@¦Æ÷BöâF†RÆ¶Rg&öçFvRæB¢£Ssbã2Ò¢¢BÆ÷BrFò¢£cCãÒ¢¢BÆ÷B&V†–æBÂ÷&FW&–ærF†RÆ÷G0¦W†7FÇ’2—B†2öâWfW'’&Æö6²öbF†R&÷râv†B6†ævVB—2F†R6—¦RöbF†RF–ffW&Væ6RâöâBÔ"w0¦&Æö6²F†Rf"VæB7FööB¢£"ã“<9r¢¢2f"g&öÒF†R'&–FvR2F†RæV"VæC²†W&RÂ¢£ã<9r¢¢âF†P¦'6öÇWFR7&VBöbF†Rg&öçBf6R—2¢£c‚ã"Ò¢¢v–ç7BBÔ"w2sã"Ò(	BF†R6ÖR&Æö6²ÂÖ÷fVB†Æb¦¶–ÆöÖWG&Râ¢¥F†R7&—FW&–öâ—2æ÷r6W&F–ærGvòÆ÷G2&W6–FVçBv÷VÆB†fR6ÆÆVBF†R6ÖRF—7Fæ6P¦g&öÒF†R'&–FvRâ¢¢—Bv2föÆÆ÷vVBç—v’Â&V6W6R6†æv–ær7&—FW&–öâF†R&Æö6²v†W&RF†Rf—'7@§7F÷2fÆGFW&–ærF†Rç7vW"—2†÷râ–çfVçF–öâ7F'G2FòÆöö²Æ–¶Rf–æF–ær(	B'WBF†R'&ævVÖVç@¦öâF†—2&Æö6²—26Æ÷6W"Fò&&—G&'’F†âöâç’&Æö6²öbF†R&÷rÂæBÃB6—26òà ¢¢¤³3vWG2—G2f—'7B6öçG&öÂÖV7W&VÖVçBÂæB—B—2f7F÷"öbGvVçG’Fòf÷'G’â¢¢³3†2f—fP¦Fö7VÖVçFVB'V–ÆF–æw27FæF–ærBã^(	3‚ã"Ò–ç6–FRF†RÆGFVB6÷WF‚vFW"6÷'&–F÷"æB6·2v†WF†W §F†B—2öæR&B7G&WF6‚öb7G&VWB÷"Væ–f÷&Òw&–B&–2âF†Rf—'7BGvòFö7VÖVçFVB&öög2ÖV7W&V@¦v–ç7B¢¦F–ffW&VçB¢¢6÷'&–F÷"&RöâF†—2&Æö6³¢F†R¢¥6Vvæ6‚†÷FVÂ–çG'VFW2ã’Ò¢¢–çFòF†P¤Æ¶R6÷'&–F÷"æB¢¥†–Æò6'VçFW"w2ÆörG'Vr7F÷&Rã#"Ò¢¢(	B–ç6–FRF†RÆBw2÷vâ&V6—6–öâö`§7FæF–æröâF†R¶W&"Æ–æRâGvò66W2&Ræ÷B7W'fW“²F†W’&RF†R6öçG&öÂ³3F–Bæ÷B†fRÂæ@§F†W’ö–çBv’g&öÒVæ–f÷&Ò&–2âæ÷F†–ærv2Ö÷fVBà ¢¢¥GvòFö7VÖVçFVB&öög26†&RÆ÷BæBF†RFW&—fVBö67Wæ7’F&ÆRæÖW2F†R6ÖÆÆW"öæRâ¢¢F†P¥6Vvæ6‚WG2“Bã32Ü+"öb—G2“bãÜ+"öâF†RÆ÷BæBF†RÆör6†÷#‚ãS‚Ü+"öb—G2#’ãrÜ+#²F†P§6÷W&6R6—2F†R6†÷7FööBv–ç7BF†R6Vvæ6‚w2V&Æ–2&"æBF†Rfö÷G&–çG2F÷V6‚BãÒÂ6ð§F†R&V6÷&Bw&VW2v—F‚—G6VÆbâÆEöö67Wæ7–æÖW2F†Rf—'7B†öÆFW"'’–B(	BF†RÆör6†÷(	B6ð¢¢§F†RF÷vâw2Ö÷7BÖFö7VÖVçFVB'V–ÆF–ær—2æ÷BF†RöæRF†BF&ÆR7&VF—G2v—F‚—G2÷vâ6÷&æW"â¢¢—@¦6÷7BF†—2&6VÂæ÷F†–æræB—Bv–ÆÂÖ—6ÆVBç–öæR&VF–ærF†BF&ÆRf÷"v†B7FæG2v†W&Rà ¢¢¥VçfW&–f–VB†W&S¢¢¢F†RFW6·F÷†Æböb6Öö¶U÷&VæFW&W"æÖ§6FöW2æ÷Bf—BF†—2'VææW"w2FVâÖÖ–çWFP§W"Ö6öÖÖæB6V–Æ–æræBv2æ÷B'Vã²F†RÖö&–ÆR†Æbv2ÂæBFööÇ2ö6†V6²ç6†(	Bv†–6‚—2F†RFW`¦vFR(	B76VBâ6VRF†R'VâÖ'VFvWB&÷‚–â$ôDÔà ¢22æWr##bÓ‚ÓR(	BF†R'W6–æW72g&öçB—2'V–ÇBVæBFòVæBÂæBF†R'VÆRF†Bf–ÆÆVB—Bö–çG2F†R÷F†W"v’öâ—G2Æ7B&Æö6° ¢¢¥BÔ"â¢¢&Æµ÷6÷WF…÷vFW%öFV&&÷&æ(	B6÷WF‚vFW"Â7FFRÂÆ¶RÂFV&&÷&â(	Bæ÷r6'&–W2¢§6—€¦æöç–Ö÷W2&öög2¢¢Âf—fR&–æ6—ÂæBöæR&—g’Âöâf—fRöb—G26—‚g&VRÆ÷G2Âv—F‚Æ÷Br‡F†P¤Æ¶RÖæBÕ7FFR6÷&æW"’ÆVgB÷VâæBÆ÷G2æBb†VÆB'’F†RÖç6–öâ†÷W6RæBF†R6†VÂ–æfç@§66†ööÂâ¢¥7FæF–ær&öög2#“2(i"#““²&VÖ–æ–ær3s"(i"3cbÂ#‚öbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v23B’à¤–æfW'&VB†÷W6V†öÆG2“"(i"“BÂ–æfW'&VBW'6öç2B(i"bâ&V6÷&FVB–âÃ2â¢¥F†R&V6—R6ÆV&V@¦WfW'’Æ6VÖVçBvFRöâ—G2f—'7B'VâæBæòFööÂ6†ævVB¢¢(	BF†Rf–gF‚&Æö6²–â&÷râ7FFR7G&VW@¦—2F†RÆGFVBF÷vâw2V7FW&âÆ–Ö—BÂ6ò¢§F†R6÷WF‚vFW"&÷r—26Æ÷6VB¢£¢WfW'’&Æö6²öbF†P¦'W6–æW72g&öçB—2æ÷r'V–ÇBÂæBWfW'’÷VâVçG'’ÆVgB–âF†R66†VGVÆR—2öæR7G&VWB&6²÷ ¦gW'F†W"à ¢¢¥F†R'VÆRF†B'&ævVBÆÂf—fR&Æö6·2&WfW'6W2F—&V7F–öâöâF†RÆ7BöæRÂæBF†B—2F†P¦f–æF–ærâ¢¢f÷W"&6VÇ2WBF†V—"&WGFW"&öög2&æV&W"F†RF÷vâÖ6VçG&RVæB#²BÔ7F÷VB76W'F–æp§F†B26ö×72F—&V7F–öâæBÖV7W&VB—B(	BF†RF—7Fæ6RFòF†R¢¤FV&&÷&â7G&VWBG&v'&–FvR¢¢À§F†RöæÇ’7&÷76–æröbF†RÖ–â7FVÒ–â§VÇ’ƒ3RâöâF†Rf÷W"&Æö6·2&Vf÷&RF†—2öæRF†R'&–FvRÆ¦V7BÂ6òF†R6ö×72æBF†R7&—FW&–öâw&VVBæBæ÷F†–ær6W&FVBF†VÒâF†—2&Æö6²w2'&–FvRVæB—0¦—G2¢§vW7B¢¢VæC¢Æ÷Bw2g&öçFvR—2¢£3bãBÒ¢¢g&öÒ—BÂÆ÷G2"æBB&R¢£SrãrÒ¢¢æB¢£ƒãrÒ¢¢À¦Æ÷Bb—2¢£bãbÒ¢¢ÂæBF†R&6²7G&VWB'Vç2¢£#bãBÒ¢¢BÆ÷BFò¢£cãÒ¢¢BÆ÷BrâF†P§&6VÂföÆÆ÷w2F†R6öÖÖ—GFVB7&—FW&–öâ&F†W"F†âF†R6ö×72Âv†–6‚—2F†Rv†öÆRö–çBöb†f–æp§&WÆ6VBöæRv—F‚F†R÷F†W"(	BæBF†RÆ÷BÆVgB÷Vâ—2v–âF†Rf'F†W7BöbF†RV–v‡Bg&öÒF†RöæÇ¦'&–FvR–âF÷vâà ¢¢¤F†—&B7&—FW&–öâv2G&–VBæB—2&V6÷&FVB2TäDT4”D$ÄRÂv†–6‚—2v÷'F‚Ö÷&RF†âF†—&@¦çVÖ&W"â¢¢6–ævÆRÆæFÖ&²—2F†–â&6—2Â6òF†R&6VÂ6¶VBv†W&RF†R¦Ö72¢öbFö7VÖVçFV@¦'V–ÆF–ær—2âF†Rfö÷G&–çB×vV–v‡FVB6VçG&ö–BöbÆÂ¢£ƒ2Fö7VÖVçFVB&öög2ƒ’ÃCRÜ+"’¢¢ÆæG2@¦Æö6Â¢¤R“3’Ââ#2¢¢ÂV7BöbF†—2&Æö6²ÂÖ¶–ærÆ÷BbæV&W7BB¢£ƒ’ã’Ò¢¢v–ç7BÆ÷Bw0¢¢£#Sã‚Ò¢¢âW†6ÇVF–ærF†Rf÷'BFV&&÷&â&W6W'fF–öâ(	B2&öög2Â¢£ÃCcÜ+"¢¢(	BÖ÷fW2—BFð¢¢¤Rs3rÂâƒ‚¢¢æB&WfW'6W2F†Rç7vW#¢¢£“RãÒ¢¢BÆ÷Bv–ç7B¢£Rã’Ò¢¢BÆ÷BbâF†P¦7&—FW&–öâF†W&Vf÷&RGW&ç2VçF—&VÇ’öâv†WF†W"Ö–Æ—F'’&W6W'fF–öâ6÷VçG22'BöbF†RF÷vâÀ§v†–6‚—2§VFvÖVçBæBæ÷BÖV7W&VÖVçBÂæB—G2v†öÆR7&VB7&÷72F†Ræ÷'F‚F–W"v—F†÷WBF†P¦f÷'B—2¢£#ã’Ò¢¢v–ç7BF†R'&–FvRw2¢£sã"Ò¢¢à ¢¢¤³3—2æ÷r†ÆbÖÖV7W&VBæBÆÂf—fRöb—G266W2&RöâöæR7G&VWBâ¢¢&÷F‚öbF†—2&Æö6²w0¦Fö7VÖVçFVB6÷WF‚vFW"'V–ÆF–æw27FæB–âF†RÆGFVB&öGv’(	BF†R¢¤6†–6vòÖW&–6âöff–6R¢ ¢¢£bã“Ò¢¢–âæB¢¤g&VFW&–6²F†öÖ2w26†÷bã#RÒ¢¢Â¢£C‚ãbÜ+"¢¢öbFö7VÖVçFVB&ööböâw&÷VæBF†P§ÆB6ÆÇ27G&VWBâv—F‚BÔ’w2F‡&VRƒBãRÒÂbãbÒÂ‚ã"Ò’F†B—2f—fRFö7VÖVçFVB'V–ÆF–æw2ÂÆÂöà¥6÷WF‚vFW"ÂÆÂ&WGvVVâBãRæB‚ã"Ò–ââF†B—2F†R6†Röb6VçG&VÆ–æR÷"v–GF‚W'&÷"öâöæP§7G&WF6‚Âæ÷BöbVæ–f÷&Ò&–27&÷72F†Rw&–B(	Bv†–6‚—2F†RF—7G&–'WF–öâ³3v2÷VæVBFòf–æBà¤æ÷F†–ærv2Ö÷fVC¢÷6—F–öâv—F‚6÷W&6R÷WG&æ·26÷'&–F÷"F†—2&ö¦V7BFW&—fVBà ¢¢¥GvògW'F†W"6öæf—&ÖF–öç2Â&÷F‚öbF†–æw2V&Æ–W"&6VÇ2†BFò&wVRâ¢¢BÔrw2Æ66R†2¢¢¦f–gF‚¢¢–ç7Fæ6RæB—B—2F†RÆ&vW7BF†B6÷7G2Æ÷Bæ÷F†–ær(	BF†RÖW&–6âöff–6RÆ2Æ÷B'¢¢£ãsBÜ+"¢¢v—F‚¢£ãÜ+"¢¢–ç6–FRF†R'V–ÆF&ÆR–ç6WBâæBBÔw2&VgW6ÂöbF†RÆFW&Âöfg6W@¦—26öæf—&ÖVB–æFWVæFVçFÇ’æBÖ÷&R6ÆVæÇ“¢g&öÒF†R6öÖÖ—GFVBÆ6VÖVçBÂãRÒgW'F†W"vW7B'W—0¢¢£ãÒ¢¢öb6ÆV&æ6Rf÷"ãsbÒöbÆ÷BÖÆ–æRÖ&v–âæB2ãÒ'W—2¢£ã#"Ò¢¢f÷""ã#bÒÂv†W&P¦†ÆbÖWG&RöbW‡G&6WF&6²'W—2¢£ãSÒ¢¢æB6÷7G2æV—F†W"âF†R&6VÂw26Æ÷6W7B&ö6‚—0¢¢£rãÒ¢¢v–ç7B2ÒvFRà ¢¢¥F†R&÷r6Æ÷6W2v—F‚³#‚÷VâÂæBF†R6÷VçB—2f÷W"&Æö6·2öbf—fRâ¢¢F†RCBæBF†RC"F†—2&Æö6°§v2FVÇBV6‚72'VÆRbw2F‡&VRFW7G2&VBÆ—FW&ÆÇ’æB&÷F‚&R&VgW6VBöâF†R6ÖP¦6öç6W'fF—fR&VF–ærâöæR&Æö6²öbF†R&÷rFVÇBæV—F†W"fÆö÷"G&FR6V6öæB&ööbÂöæRFVÇB—BFð§F†R6'VçFW'2ÆöæRÂæBF‡&VRFVÇB—BFò&÷F‚â¢¥F†R6WfVçF‚³#ÖV7W&VÖVçB—2S’öbB¢¢À¦v–ç7BrÖöbÓ"Âs"ÖöbÓÂ’ÖöbÓ“‚æB3"ÖöbÓ“b(	Bf—fR&VF–æw27ææ–ærrRFòs"Rv—F‚æ÷F†–æp¦f—†VB÷"'&ö¶Vâ&WGvVVâF†VÒà ¢22æWr##bÓ‚ÓR(	BF†Rf÷W'F‚'W6–æW72Ög&öçB&Æö6²ÂæBF†Rf—'7BF–ÖRF†R&÷rw2&&WGFW"VæB"—2ÖV7W&VÖVç@ ¢¢¥BÔâ¢¢&Æµ÷6÷WF…÷vFW%ö6Æ&¶(	B6÷WF‚vFW"ÂFV&&÷&âÂÆ¶RÂ6Æ&²(	Bæ÷r6'&–W2¢¦f—fP¦æöç–Ö÷W2&öög2¢¢Âf÷W"&–æ6—ÂæBöæR&—g’Âöâf÷W"öb—G2f—fRg&VRÆ÷G2Âv—F‚Æ÷B‡F†P¤Æ¶RÖæBÔ6Æ&²6÷&æW"’ÆVgB÷VâæBÆ÷G2ÂbæBr†VÆB'’†&ÖöâbÆööÖ—2w27F÷&RÂ¦ö†â&FW0¤§"âw2V7F–öâ&ööÒæBF†Rf—'7BG&VÖöçB†÷W6Râ¢¥7FæF–ær&öög2#ƒ‚(i"#“3²&VÖ–æ–ær3sr(i"3s"À£3BöbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v23’’â–æfW'&VB†÷W6V†öÆG2“(i"“"Â–æfW'&VBW'6öç2"(i"Bà¥&V6÷&FVB–âÃ"â¢¥F†R&V6—R6ÆV&VBWfW'’Æ6VÖVçBvFRöâ—G2f—'7B'VâæBæòFööÂ6†ævVB¢ ®(	BF†Rf÷W'F‚&Æö6²–â&÷rà ¢¢¥D„R$õr„2UB•E2$UEDU"$ôôe2$äT$U"D„RDõtâÔ4TåE$RTäB"D…$TRD”ÔU2äBäUdU"4”Bt„Bt0¤BD„BTäBâ¢¢F†—2&Æö6²w2V7BVæB—2FV&&÷&â7G&VWBÂæBF†R¢¤FV&&÷&â7G&VWBG&v'&–FvR¢¢(	@§F†RöæÇ’7&÷76–æröbF†RÖ–â7FVÒ–â§VÇ’ƒ3RÂÇ&VG’6öÖÖ—GFVB7G'V7GW&R&V6÷&BÂ—G26÷WF€¦'WFÖVçBBF†Rfö÷BöbFV&&÷&âöâ6÷WF‚vFW"(	BÖV7W&W2F†R6Æ–Ó¢¢£3RãbÒ¢¢g&öÒÆ÷Bbw0¦g&öçFvRÂSRãRÒg&öÒÆ÷BBw2Âs‚ãÒg&öÒÆ÷B"w2Â¢£ãrÒ¢¢g&öÒÆ÷Bw2ÂæBöâF†R&6°§7G&VWB#bã2ÒBÆ÷Br÷WBFò¢£S‚ã"ÒBÆ÷B¢¢Âv†–6‚—2F†RÆ÷BÆVgB÷Vââæò6÷W&6R6—2¦&WGFW"†÷W6R7FööBæV&W"F†R'&–FvRÂ6òF†R'&ævVÖVçB—22–çfVçFVB2—Bv3²v†B6†ævVB—0§F†B—B—2–çfVçFVBv–ç7B&RÖFW&—f&ÆRçVÖ&W"–ç7FVBöb6ö×72F—&V7F–öâà ¢¢¤äBD„Rd4R„ÄbôbD„R4ÔR%TÄRÔTUE2•E2d•%5B4õTåDU"ÔU„ÕÄRâ¢¢F‡&VR&6VÇ2†fR6ÆÆV@¥6÷WF‚vFW"F†RfÇV&ÆRg&öçFvRæBÆ¶RF†R&6²7G&VWBâF†RÆ&vW7BFö7VÖVçFVBfö÷G&–çBöà§F†—2&Æö6²—2öâÆ¶S¢F†Rf—'7B¢¥G&VÖöçB†÷W6RB3’ã2Ü+"¢¢Âv–ç7B“"ã’Ü+"f÷"F†RV7F–öà§&ööÒÂ“"ã’Ü+"f÷"†&ÖöâbÆööÖ—2w27F÷&RæBCbãRÜ+"f÷"'W–æRb¶–Ö&ÆÂw2G'Vr7F÷&RâF†R'VÆP¦—2¶WB(	B—B—2G—öÆöw’f÷"v†W&Ræöç–Ö÷W2GvVÆÆ–æw2öbF–ffW&VçBF–W'2vò(	B'WB—B—2æ÷p§&V6÷&FVB2¦æ÷B¢6Æ–Ò&÷WBv†–6‚7G&VWBv2v÷'F‚Ö÷&RÂ&Vf÷&Rf÷W"&Æö6·2öb&WWF—F–öà§GW&æVB—B–çFòöæRà ¢¢¥BÔrw2Æ66R†2f÷W'F‚–ç7Fæ6RæB—B—2F†Rf—'7BF†B6÷7G2Æ÷Bæ÷F†–ærBÆÂâ¢¢F†P¦G'Vr7F÷&RÆ2Æ÷B"'’¢£BãcbÜ+"¢¢ÂæB¢£ãÜ+"öb—B—2–ç6–FRF†R'V–ÆF&ÆR–ç6WB¢£¢F†P§v†öÆRÆÆ–W2–âF†RãRÒÖ&v–â7G&—âGvòöbF†R7F÷&Rw26÷&æW'2&RãsÒæBãcRÒ–ç6–FP§F†RÆGFVBÆ÷BÆ–æRæBF†R÷F†W"Gvò&RRãBÒ÷WB–âF†R&öBÂ¢£RãSRÒ¢¢–çG'W6–öâ–çFòF†P¥6÷WF‚vFW"6÷'&–F÷"âv—F‚Ãw2#"ãÜ+"öb'V–ÆF&ÆRÆÂ¶–ç¦–Rw2’ãrÜ+"æ@¦&V6öåóƒ3U÷vW7Eó†w2ã’Ü+"ÂF†R66Ræ÷r7ç2—G2v†öÆR&ævRà ¢¢¥D„Rôde4UBD„Bå5tU$TBD„RÄ5B$Äô4²u2ÄDôU2ÄÔõ5BäõD„”är„U$RÂäBD„RÔT5U$TÔTåB4•0¥t…’â¢¢BÔÖ÷fVB6†çG’vW7BFò6ÆV"6‡W&6‚w27F÷&RâöâÆ÷B"F†R6ÖRÖ÷fR'W—2¢£ã2Ò@£ãRÒöböfg6WBæBã32ÒB2ãÒ¢¢(	BF†R2ÒfW'6–öâ6÷7F–ærã#bÒöbÆ÷BÖÆ–æRÖ&v–â(	Bv†W&P¦†ÆbÖWG&RöbW‡G&6WF&6²'W—2¢£ãSÒ¢¢'’—G6VÆbâ6‡W&6‚w27F÷&R7FööBFVW–ç6–FR—G2Æ÷C°§F†—2öæR7FæG2–âF†R&öGv’Â6òöæÇ’F†R6WF&6²6†ævW2F†RF—7Fæ6RâF†R6÷GFvR—26WB&6°£rãRÒæB6ÆV'2—B'’¢£bãƒ2Ò¢¢v–ç7B2ÒvFRÂF†R6Æ÷6W7B&ö6‚–âF†R&6VÂâF†P¦ÆFW&Âöfg6WG2ÆVgB–âF†R&V6—R&R¦—GFW"æB&RÆ&VÆÆVB¦—GFW"à ¢¢¤d•dR4õUD‚D•d•4”ôâ„õU4T„ôÄE2Ä•dR”âCRÂD…$TR$Äô4µ2%Tää”är„dR$TTâDTÅBôäRÂäBäð¥$4TÂ„BUdU"$T4õ$DTBt…’äôäRôbD„TÒD´U2•Bâ¢¢'VÆRbw2fÖ–Ç’æBF—f—6–öâFW7G272öà§F†—2&Æö6²w2CRf÷"F†R&¶W"ÂF†R'WF6†W"ÂF†R&Æ6·6Ö—F‚æB&÷F‚6ÆW&·2âÆÂf—fRf–ÂFW7BöæP®(	BF†V—"6öÖÖ—GFVB&wVÖVçG2Fòæ÷B6ÆÂF†V—"6÷VçG2fÆö÷'2ÂæBGvòöbF†VÒ6F†V×6VÇfW0¦÷WG&–v‡B‚&öæÇ’öæRÂ&V6W6R&¶V†÷W6R6W'fW2w&VBÖç’V÷ÆRæBæ÷F†–ærGFW7G26V6öæB"’à¤&VgW6Âæö&öG’w&—FW2F÷vâ—2–æF—7F–æwV—6†&ÆRg&öÒ'VÆRæö&öG’Æ–VBÂ6ò—B—2w&—GFVâF÷và¦æ÷rà ¢¢¤³#‚tUE2D„•$B$T4TDTåB”å5DTBôb4T4ôäBâ¢¢F†RCBöâÆ÷B"76W2ÆÂF‡&VRFW7G2f÷"F†P¦6'VçFW'2W†7FÇ’2BÔ’w2æBBÔw2F–BÂæBv2&VgW6VBv–âöâF†R6öç6W'fF—fR&VF–ærà¥F‡&VRf÷"F‡&VR—2F†R÷&F–æ'’6†Röb6÷WF‚F—f—6–öâ&Æö6²Âæ÷B&V7W'&–ærVFvR(	BF†P§VW7F–öâ6†÷VÆB&R6WGFÆVB&F†W"F†â6öÆÆV7Bf÷W'F‚âF†RÆ&÷W&W'2vW&RFVÇBæòC"†W&RÂF†P¦f—'7B&Æö6²6–æ6RBÔ‚v†W&RF†V—"6V6öæB×&ööbVW7F–öâF–Bæ÷B&—6Rà ¢¢¥D„R4•…D‚³#ÔT5U$TÔTåB•2D„R4ÔÄÄU5BUdU"$T4õ$DTC¢röb"¢¢6'&–VBÖ÷fW"–çfVçFVBW'6öç0§&VæÖVBÂv–ç7Bs"ÖöbÓBBÔÂ’ÖöbÓ“‚BBÔ’Â3"ÖöbÓ“bBBÔ‚æB#RÖöbÓ“BBBÔ&‚à¤æ÷F†–ærv2f—†VB–â&WGvVVââ—B—2F†R†6‚×÷6—F–öâÖV6†æ—6ÒÃ–FVçF–f–VBÂ6öæf—&ÖVBg&öÒF†P¦÷F†W"VæBöb—G2&ævRÂæB—B—2æ÷BWf–FVæ6RF†BF†R6‡W&â—2VæFW"6öçG&öÂâ³#7F–ÆÂ÷vç2F†P¦f—‚à ¢22æWr##bÓ‚ÓR(	BF†RF†—&B'W6–æW72Ög&öçB&Æö6²ÂæBF†RæÖR6‡W&â—2F‡&VRF–ÖW2v÷'6RF†â&W÷'FV@ ¢¢¥BÔâ¢¢&Æµ÷6÷WF…÷vFW%öÆ6ÆÆV(	B6÷WF‚vFW"Â6Æ&²ÂÆ¶RÂÆ6ÆÆR(	Bæ÷r6'&–W2¢§6WfVà¦æöç–Ö÷W2&öög2¢¢Âf—fR&–æ6—ÂæBGvò–&B'V–ÆF–æw2Âöâf—fRöb—G26—‚g&VRÆ÷G2Âv—F‚Æ÷B¢‡F†RÆ¶RÖæBÔÆ6ÆÆR6÷&æW"’ÆVgB÷VâÂÆ÷Bb†VÆB'’F†R6†–6vòFVÖö7&Bw2öff–6RæBÆ÷BR'¥F†öÖ26‡W&6‚w27F÷&Râ¢¥7FæF–ær&öög2#ƒ(i"#ƒƒ²&VÖ–æ–ær3ƒB(i"3srÂ3’öbF†VÒöâ6÷fW&V@¦w&÷VæB¢¢‡v2Cb’â–æfW'&VB†÷W6V†öÆG2ƒ‚(i"“Â–æfW'&VBW'6öç2(i""â&V6÷&FVB–âÃâ¢¥F†P§&V6—R6ÆV&VBWfW'’Æ6VÖVçBvFRöâ—G2f—'7B'VâæBæòFööÂ6†ævVB¢¢(	BF†RF†—&B&Æö6²–â§&÷rà ¢¢¥D„Rd•%5B$Äô4²ôbD„R$õrD„B%$•dTBt•D‚Dô5TÔTåDTB$ôôbôâ$õD‚d4U2â¢¢F†Rg&öçFvP¦&wVÖVçBBÔ‚÷VæVBæBBÔ’FW7FVB(	B&W7BGvVÆÆ–æw2Fò6÷WF‚vFW"ÂÖVæW7BFòÆ¶R(	B†26òf ¦&VVâg&VRFòÇ’Â&V6W6RF†R&6²7G&VWBv2V×G’öâ&÷F‚V&Æ–W"&Æö6·2â6‡W&6‚w27F÷&R7FæG0¦öâF†—2öæRw2Æ¶Rg&öçFvRâF†R'&ævVÖVçBv2Æ–VBç—v’Â6òÆör6&–âæBÆæ²6†çG¦æ÷r7FæBöâg&öçFvRF†BÇ&VG’6'&–W2Fö7VÖVçFVB7F÷&Râ6ÖR–çfVçF–öâÂÆW72&ööÓ²Ã§6—26ò&F†W"F†âÆWGF–ærF†RGFW&â&VB2WFöÖF–2à ¢¢¥BÔrw2vW7Eó†66R†2F†—&BæB×V6‚Æ&vW"–ç7Fæ6RÂÖV7W&VB†W&Râ¢¢6‡W&6‚w27F÷&R—0§6VFVBöâÆ÷BR'’FW7BöæR(	B¢£S’ã2Ü+"öb“"ã’Ü+"F†W&Rv–ç7B32ãbÜ+"öâÆ÷B2¢¢(	B'WB¢£#"ãÜ+ ¦öbF†RÆ÷B2Æ—2–ç6–FRÆ÷B2w2'V–ÆF&ÆR–ç6WB¢¢Â6òÆ÷BF†R66†VGVÆR&VG22g&VR6'&–W2¦Fö7VÖVçFVB'V–ÆF–ær7&÷72—G2g&öçFvR6÷&æW"âv–ç7B’ãrÜ+"„¶–ç¦–RÂæöæRöb—B'V–ÆF&ÆR’æ@£ã’Ü+"†&V6öåóƒ3U÷vW7Eó†’ÂF†—2—2F†R&–vvW7B–WBÂæBVæÆ–¶R¶–ç¦–Rw2—B—2¦–ç6–FR¢F†P¦'V–ÆF&ÆR'Bâ—B—2"ãBRöbF†RÆ÷Bw2'V–ÆF&ÆR&VÂ6òF†RÆ÷B7F–ÆÂFöö²&ööc¢F†R6†çG’—0¦öfg6WBvW7BÂv’g&öÒF†R7F÷&RÂæB6ÆV'2—B'’¢£rãSbÒ¢¢v–ç7B2ÒvFR(	BF†R6Æ÷6W7@¦&ö6‚ç—v†W&R–âF†—2&6VÂâæò'VÆR6†ævVBæBæ÷F†–ærv2Ö÷fVC²F†RçVÖ&W"—2&V6÷&FVB6ð§F†RæW‡B&6VÂFòÖVWBF†R66R†2F‡&VRFFö–çG2–ç7FVBöbGvòà ¢¢¤³#‚•2äòÄôätU"ôäRÔôdbÂt„”4‚•2D„R$uTÔTåBdõ"4UEDÄ”är•Bâ¢¢BÔ’f÷VæB'VÆRb6–ÆVçBöà¦†÷rÖç’&öög2öböæR&Æö6²G&FRÖ’F¶RæB&W÷'FVB—B266Ræò&Æö6²†BöffW&VB&Vf÷&Rà¥F†—2&Æö6²öffW&VBF†R–FVçF–6Â66S¢f÷W"öb—G2f—fRGvVÆÆ–æw272ÆÂF‡&VRFW7G2f÷"öæRG&FP¦÷"F†R÷F†W"ÂF†RC2¦æB¢F†RCBf÷"6'VçFW'2ÂF†RC¦æB¢F†RC"f÷"Æ&÷W&W'2âGvò6öç6V7WF—fP¦&Æö6·2†fRæ÷rFVÇB&÷F‚fÆö÷"G&FW2&÷F‚öbF†RfÖ–Æ–W2F†W’&R†÷W6VB–âÂ6òF†—2—2v†B¦f—fRÖ÷"×6—‚ÖGvVÆÆ–ær&Æö6²–âF†R6÷WF‚F—f—6–öâÆöö·2Æ–¶R&F†W"F†â6ö–æ6–FVæ6RâöæRF÷F–öà§W"G&FRv2F¶Vâv–âÂöâBÔ’w2&VF–æræB&V6÷&FVB26†ö–6Rà ¢¢¤äBD„R³#‚”B•2U4TBEt”4R”âD„•2$Uõ4•Dõ%’â¢¢$ôDÔ³#†—2F†R'VÆRÓbVW7F–öâ&÷fS°§F†RV&Æ—6†VBÖÖ—'&÷"vFRF†BÆæFVB2"3CrÇ6ò6†—VBVæFW"F†RæÖR³#‚æB†2æò$ôDÔ ¦VçG'’öb—G2÷vââ&÷F‚&R&VÂv÷&²æBæV—F†W"—2w&öær(	BF†R6öÆÆ—6–öâ—2–âF†RÆ&VÂâ¦F—6Ö&–wVF–öâÆ–æR—2FFVBBF†R$ôDÔ†VF–ær6òWfW'’W†—7F–ær6—FF–öâ&W6öÇfW3²&VçVÖ&W&–æp¦ÆæFVBv÷&²—2æ÷B&Æö6²&6VÂw26ÆÂâF†—2—2F†R6ÖRFVfV7BBÔ’f÷VæB–âÃ“’w2ö–çFW"Â–âF†P¦÷÷6—FRF—&V7F–öâà ¢¢¥D„Rd”eD‚³#ÔT5U$TÔTåB•2D„RôäRD„B%$Tµ2D„R$d”eD‚ôbD„RÄ”U""DU45$•D”ôââ¢ ¤–ç6W'F–ærGvò†÷W6V†öÆG2&VæÖVB¢£s"öbF†R6'&–VBÖ÷fW"–çfVçFVBW'6öç2¢¢Âv–ç7B’ÖöbÓ“€¢…BÔ’’Â3"ÖöbÓ“b…BÔ‚’Â#RÖöbÓ“B…BÔ&‚’æBrÖöbÓ32×F÷V6†VB…BÔR’âæòw&FRÖ÷fVBÂWfW'¦æÖUö&6—6¶WB—G2ööÂ6—FF–öâÂæB6†V6²ç6†&RÖFW&—fW2ÆÂ"(	BF†—2—26‡W&âÂæ÷B§&÷fVææ6Rf–ÇW&RâF†RÖV6†æ—6Ò—2æ÷B&æFöÓ¢FööÇ2övVæW&FUö–æfW'&VEöæÖW2ç–FVÇ2æÖW0§&÷VæB×&ö&–âF‡&÷Vv‚V6‚6öÖ×Væ—G’ÖæB×6W‚ööÂ–â7F&ÆR†6‚÷&FW"öbW'6öâ–BÂ6òöæRæWp§W'6öâÆæF–ærV&Ç’–âÆ&vR'V6¶WB&VæÖW2WfW'—F†–ærgFW"—BâF†R7&VBg&öÒ’Fòs"—0§W&VÇ’v†W&RF†RæWr–G2†6†VBâ³#w2f—‚7F–ÆÂ&VÆöæw2–â—G2÷vâ&6VÃ²F†—2—2F†Rf–gF‚&Æö6°§Fò&–FRÆöæröâ—BÂæBF†Rf—'7Bv†W&RF†R6–FRVffV7B—2Æ&vW"F†âF†R&6VÂà ¢22f—†VB##bÓ‚ÓR(	BF†RvVæW&Â66R&V†–æB"Ô%Ts62Ö#¢æ÷F†–ær6†V6¶VBv†B7GVÆÇ’6†—0 ¢¢¤³#‚â¢¢3CRf—†VBF†RFW'&–âVçF—6W"æBVæFVBöâöæRÆ–æS¢¦Fòæ÷BÖV7W&RF†Rf–ÆR–÷R'V–ÇBÀ¦ÖV7W&RF†Rf–ÆR–÷R6†—â¢—BÇ6ò6–BÆ–æÇ’v†B—B†Bæ÷BFöæR(	B$æ÷F†–ærVÇ6R–âF†—0§&ö¦V7BÖV7W&W2V&Æ—6†VB'FVf7Bv–ç7B—G2÷vâ6÷W&6RÂæBæö&öG’†2Æöö¶VBf÷"F†RæW‡@¦–ç7Fæ6Röb—Bâ"F†—2—2F†BvFRà ¢¢¥F†R–çf&–çB—2F÷FÂÂv†–6‚—2v†BÖ¶W2—B6†Vâ¢¢FööÇ2÷V&Æ—6‚ç6†—2ÆÖ÷7BVçF—&VÇ¦7¢F†RÖ—'&÷"—2ÖVçBFò&RF†R&W÷6—F÷'’Â&V'&ævVBâ6ò¢¦WfW'’V&Æ—6†VBf–ÆR×W7B&P¦'—FRÖ–FVçF–6ÂFò—G26÷W&6R¢¢ÂVæÆW72—B—2öâFV6Æ&VBÆ—7B(	BæBV6‚VçG'’öâF†BÆ—7B†2Fð§6’v†BG&ç6f÷&×2F†R'—FW2æB¢¦æÖRF†RvFRF†BÖV7W&W2F†R4„•TBf÷&Ò¢¢âF†B6V6öæ@¦6öÇVÖâ—2F†Rv†öÆRö–çC¢—B—2F†RVW7F–öâæö&öG’6¶VB&÷WBF†RFW'&–âÂæ÷rw&—GFVâF÷và¦&W6–FRWfW'’Æ6R—BÆ–W2à ¤7W'&VçB7FFS¢¢£S#f–ÆW2'—FRÖ–FVçF–6ÂÂ#“bG&ç6f÷&ÖVBVæFW"BFV6Æ&VB'VÆW2ÂVæÖVBâ¢  ¢¢¤—Bf÷VæBGvòVæ6†V6¶VBf–ÆW2öâ—G2f—'7B'Vâ¢¢Âv†–6‚—2F†R&wVÖVçBf÷"—Bà ¢Ò¢¦'V–ÆBæ§6öæv2GvòF—27FÆRâ¢¢—B6Æ–ÖVBfW'6–öâƒ““33&'V–ÇB##bÓ‚Ó5C“£ƒ£U¦ ¢v†–ÆRF†RÖ—'&÷"&W6–FR—Bv2g&öÒFöF’BF–ffW&VçB6öÖÖ—Bâæ÷F†–ær–âV&Æ—6‚ç6†WfW ¢&Ww&÷FR—B(	B—B†B&VVâw&—GFVâöæ6RÂ'’†æBâFööÇ2÷FW7EöFWe÷&Wf–WræÖ§6æBFö72õ•TÄ”äRæÖF ¢&÷F‚&VB—BÂ6ò&÷F‚vW&R&VF–ær7FÆR6Æ–Ò&÷WBv†B6†—VBâV&Æ—6‚ç6†æ÷r&VvVæW&FW0¢—BWfW'’'Vâg&öÒF†R6ÖRGvòf&–&ÆW2F†Rf—6–&ÆR'V–ÆB7F×W6W2Â6òF†RÖ6†–æR×&VF&ÆP¢Gv–âæBF†R‡VÖâ×&VF&ÆRöæR6ææ÷BF—6w&VRà¢Ò¢¥F†RÖ—'&÷"w2–æFW‚æ‡FÖÆ¢¢—2w&—GFVâöæ6Rg&öÒ†W&VFö2æBG&6VBFòæ÷F†–ærâ—B—2¢&VF—&V7B7GV"v—F‚æò6Æ–Ò–â—BÂ6ò—BæVVG2æòvFR(	B'WBF†B—2æ÷r&V6÷&FVBÂ6ò–b—BWfW ¢w&÷w26Æ–ÒF†R'6Væ6R—2f—6–&ÆRà ¢¢¥F†RvFRv2fW&–f–VBFòf–Ââ¢¢6–ævÆRG&–Æ–æræWvÆ–æRVæFVBFòF†RV&Æ—6†V@¦FFöFGVÒæ§6öæf–Ç2—Bv—F‚F†RF—fW&vVæ6RæÖVBæBF†R6÷W&6RF‚V÷FVC²&W7F÷&–ærF†Rf–ÆP§76W2â6†V6²F†B†2æWfW"f–ÆVB—2æ÷B6†V6²(	BF†R6ÖR7FæF&B³#rv2†VÆBFòV&Æ–W §FöF’à ¢¢¥v†BF†—2FöW2äõBFòÂ7FFVB6ò—B—2æ÷B77VÖVBâ¢¢—B6ö×&W2%•DU2f÷"6÷–W2â—BFöW2æ÷@§fW&–g’F†BFV6Æ&VB§G&ç6f÷&Ò¢&W6W'fW2v†BF†RG&ç6f÷&Ò—27W÷6VBFò&W6W'fR(	BF†B—0§W"×G&ç6f÷&Òv÷&²ÂæB—B—2W†7FÇ’v†B3CR†BFòFò'’†æBf÷"F†RFW'&–ââF†R#“2tÄ ¦FW&—fF—fW2&RFV6Æ&VBÂæ÷B6†V6¶VC²¢¥"Õsb¢¢Ç&VG’6·2v†WF†W"F†R6ÖRVçF—6W"Ö÷fW2Ræ@¤â'’WFòS2ÖÒæBv†WF†W"F†RFW'&–â6†÷VÆB6†—VçF—6VBBÆÂÂæBæö&öG’†2Æöö¶VBà ¢22d•„TB##bÓ‚ÓR(	BF†Rw&÷VæB–÷R6VR•2F†Rw&÷VæBF†RF÷vâ—2æ6†÷&VBFòæ÷rÂæBæV—F†W"7W&f6R†BÖ÷fV@ ¢¢¥"Ô%Ts62Ö"¢¢ÂF†R†Æb†’&VgW6VBFòwVW72BâF†R’ãn(	32ã6ÒF—6w&VVÖVçB†’ÖV7W&VB—2&VÂÀ¦æB¢¦æV—F†W"F†RG&vâÖW6‚æ÷"F†R6×ÆW"v2w&öær¢¢âF†Rv—2–çG&öGV6VB¦&WGvVVâ¢F†VÒÂ'§F†RV&Æ—6‚7FWÂgFW"F†RöæÇ’vFRF†BÖV7W&W2—Bà ¦vVæW&F÷'2÷FW'&–åövVâç–&’Ö67G2—G2FV6–ÖFVBw&÷VæBv–ç7BF†R†V–v‡Ff–VÆBæB&VgW6W2Fð¦W‡÷'B7B¢£3ÖÒ¢¢â—G2Ö7FW"†öæ÷W'2F†BFò¢£"ãRÖÒ¢¢(	B2W†7B2F†Rf–VÆB—B—2'V–Ç@¦g&öÒâF†Rf–ÆR'&÷w6W"ÆöG2—2F†RFW&—fF—fRvÇFb×G&ç6f÷&Ò÷F–Ö—¦Vw&—FW2gFW'v&G2–à¦FööÇ2ö&¶Rç6†ÂæBF†BVçF—6W2õ4•D”ôâFò¢£B&—G2VæFW"öæRVæ–f÷&ÒæöFR66ÆR¢¢âF†R66ÆP¦—26WB'’F†Rv–FW7B†—3²F†—2ÖW6‚—2¢£RÃ#Òv–FR¢¢†"Ã#Ò&÷‚ÇW2ãR¶Òöb6¶—'BV6€§6–FR’æB¢£‚ãbÒFÆÂ¢¢Â6òF†RfW'F–6Â'Væw2&R¢£3bÖÒ¢¢'BâÖV7W&VBöâF†R6†—VB'—FW3 ¢¢§&×2ƒRÖÒÂÖ‚##‚ÖÒ¢¢à ¢¢¤æò6WGF–ærf—†W2—BÂæBF†Bv2ÖV7W&VB&F†W"F†â77VÖVBâ¢¢b&—G2(	BF†RÖ†–×VÒF†Rf÷&Ö@¦öffW'2(	B7F–ÆÂÆæG2öâsbãbÖÒÆGF–6RâöæÇ’GW&æ–ær6ö×&W76–öâöfbÖVWG2F†RFöÆW&æ6RÂ@¢¢£bãCRÔ"v–ç7Bcƒ‚´"¢¢à ¢¢¥F†Rf—‚—2æ÷BgVFvRæBFVÆ–&W&FVÇ’æ÷BÄ”eEôÖâ¢¢F†R&VæFW&W"&VG2F†Rw&÷VæBw2†V–v‡G0¦&6²öfbF†R†V–v‡Ff–VÆB2—BÆöG2†6öæf÷&Ôw&÷VæEFôf–VÆB‚–’Â6òF†R7W&f6Rf—6—F÷"6VW2æ@§F†R7W&f6RWfW'—F†–ær—2Æ6VBöâ&RF†R6ÖR7W&f6R'’6öç7G'V7F–öââÆÂ¢£#BÃC¢¢fW'F–6W0¦Ö÷fRÂ'’WFò¢£##rãbÖÒ¢£²F†R&W6–GVÂ—2¢£ã#B+VÒ¢¢Âv†–6‚—2fÆöC3"7F÷&vRà ¢¢¥F‡&VRvFW2Ö—76VBF†—2æBÆÂF‡&VRÖ—76VB—BF†R6ÖRv“¢F†W’6ö×&RF†R&VæFW"Fòæ÷F†W §&VæFW"â¢¢VçF—6VBw&÷VæBÆöö·2W&fV7FÇ’6÷'&V7BâGvòvFW2æ÷r†öÆBÖV7W&VÖVçB–ç7FVB(	@¦6†V6²ç6†76W'G2F†R6öÖÖ—GFVBÖ7FW"æB&W÷'G2F†RFW&—fF—fRÂæBF†R6Öö¶R76W'G2F†P§7W&f6R7GVÆÇ’E$tâv–ç7BF†R6×ÆW"Âw&VVâB&÷F‚f–Ww÷'G2à ¢¢¥VæfÆGFW&–ærÂæBv÷'F‚¶VW–ær–âf–Wrâ¢¢F†—2—2F†RF†—&B&6VÂöâöæR÷væW"&W÷'Bâ"Ô%Ts0¦f—†VB&VÂ6öçG&7BfVÇBæBFV6Æ&VBF†R'Vr6Æ÷6VC²F†R÷væW"&W&öGV6VB—BF†R6ÖRF’à¥"Ô%Ts62ÖÖV7W&VBF†R6W6RæBf—†VBæ÷F†–ærÂv†–6‚—2F†RöæÇ’&V6öâF†—2f—‚—2F†R&–v‡BöæP§&F†W"F†âçVFvRFòÄ”eEôÖF†Bv÷VÆB†fRÆVgB'V–ÆF–æw2Â6öÆÆ—6–öâæBfÆ÷&7F–ÆÂw&öærâF†P¦ÆW76öâ—2öæRÆ–æS¢¢¦Fòæ÷BÖV7W&RF†Rf–ÆR–÷R'V–ÇBÂÖV7W&RF†Rf–ÆR–÷R6†—â¢¢æ÷F†–ærVÇ6P¦–âF†—2&ö¦V7BÖV7W&W2V&Æ—6†VB'FVf7Bv–ç7B—G2÷vâ6÷W&6RÂæBæö&öG’†2Æöö¶VBf÷"F†P¦æW‡B–ç7Fæ6Röb—Bà ¢¢¥7F–ÆÂ÷VâÂæB†öæW7FÇ’÷Vã¢¢¢F†R6ÖRVçF—6W"Ö÷fW2RæBâ'’WFò¢£S2ÖÒ¢¢æBæ÷F†–æp¦6÷'&V7G2F†Bâ—B—2–çf—6–&ÆRöâFV6–ÖFVB&—&–R2f"2ç–öæR†26†V6¶VB(	BæBæö&öG’†0¦7GVÆÇ’6†V6¶VBâF†B—2¢¥"Õsb¢¢ÂÆöærv—F‚v†WF†W"F†RFW'&–â6†÷VÆB6†—VçF—6VBBÆÂà¢22ÔT5U$TB##bÓ‚ÓR(	BF†RG&vâFW'&–âæBF†R†V–v‡Ff–VÆB&RD”ddU$TåBDDÂæ÷BFV6–ÖF–öà ¢¢¥"Ô%Ts62Ö"â¢¢"Ô%Ts62Öf÷VæBF†RG&vâw&÷VæB6—GF–ær’ãn(	32ã6Ò&÷fRFW'&–âç7W&f6T†V–v‡B‚– ¦BF†R÷væW"w2÷6RâF†—26·2v†–6‚öbF†RGvòÖ÷fVBÂ'’FW7F–ærF†RG&vâÖW6‚w2¢¦÷vâfW'F–6W2¢ ¦v–ç7BF†R6×ÆW"(	BRÃ“c"fW'F–6W27&÷723FW'&–âÖW6†W2ÂvFW"W†6ÇVFVBà ¥F‡&VR÷WF6öÖW2vW&R÷76–&ÆRæBF†W’&R×WGVÆÇ’W†6ÇW6—fRâæV"×¦W&òWfW'—v†W&Rv÷VÆBÖVâF†P¦ÖW6‚•2F†R†V–v‡Ff–VÆBÂFV6–ÖFVBÂæBF†R'W&–Â—2â–çFW'öÆF–öâ'FVf7Böb6ö'6RG&–ævÆW2à¤6öç7FçBöfg6WBv÷VÆBÖVâFGVÒ6†–gBâ&æFöÒv÷VÆBÖVâF–ffW&VçBFFà §ÂÂÀ§ÂÒÒ×ÂÒÒ×À§ÂÖ–âòÖ‚Â¢®(‰#2ãsrÒò³"ãsCBÒ¢¢À§ÂWF‚ò“WF‚W&6VçF–ÆRÂ(‰#"ãCcRò³ãS’À§ÂÖVF–âÂ³ã#bÀ§ÂÖVâ+6BÂ³ãƒr+¢£ã3b¢¢À§ÂfW'F–6W2v—F†–âRÖÒÂ¢£ƒ"öbRÃ“c"ƒ2ãR’¢¢À ¢¢¤—B—2F†RF†—&B÷WF6öÖRâ¢¢F†R7&VB—2ÔUE$U2Âæ÷B6VçF–ÖWG&W2Â6òF†—2—2æ÷B6ö'6R×G&–ævÆP¦–çFW'öÆF–öã²æBF†R7FæF&BFWf–F–öâ—2ãBÒv–ç7BÖVâöbã’ÒÂ6ò—B—2æ÷BFGVÐ§6†–gBV—F†W"â¢¥F†R&¶VBFW'&–âtÄ"æB†V–v‡Ff–VÆBæ&–æ&RF–ffW&VçB7W&f6W2¢¢Â&÷Vv†Ç¦6òÖÆö6FVB(	BF†RÖVF–â—2#bÖÒ(	BæBÆö6ÆÇ’F—6w&VV–ær'’WFòF‡&VRÖWG&W2à ¢¢¥F†R26ÒBF†R÷væW"w2÷6Rv2F†RÆö6ÂfÇVRöb×V6‚Æ&vW"F—6w&VVÖVçBâ¢¢WfW'—F†–æp¦æ6†÷&VBFòF†R6×ÆW"(	B&öG2ÂfÆ÷&Â'V–ÆF–æw2Â6öÆÆ—6–öâ(	B—2Æ6VBv–ç7B7W&f6RF†@¦F–ffW'2g&öÒF†RG&vâöæR'’WFò2Ò6öÖWv†W&R–âF†R66VæRà ¢¢¥7F–ÆÂæ÷BW7F&Æ—6†VBÂæBF†—2—2æ÷rF†Rv†öÆRVW7F–öã¢v†–6‚öæR—2WF†÷&—FF—fRâ¢¢öæRö`§F†W6Rv2vVæW&FVBg&öÒFW'&–â7V2F†R÷F†W"æòÆöævW"ÖF6†W2Â÷"öæR—27FÆRâVçF–ÂF†B—0§6WGFÆVBæ÷F†–ær6†÷VÆB&RÖ÷fVC¢&—6–ærÄ”eEôÖÂ&RÖ&¶–ærÂ÷"&VvVæW&F–ærF†R†V–v‡Ff–VÆB6÷VÆ@¦V6‚&RF†R6†ævRF†BFW7G&÷—2F†R6÷'&V7B7W&f6RâF†RæW‡B7FW—2Fò&RÖFW&—fR&÷F‚g&öÒF†P¦6öÖÖ—GFVBFW'&–â7V2æB6VRv†–6‚&W&öGV6W2à ¢22æWr##bÓ‚ÓR(	BF†R6V6öæB'W6–æW72Ög&öçB&Æö6²ÂæBF†R6V6öæB&ööbV6‚G&FRv2&VgW6V@ ¢¢¥BÔ’â¢¢&Æµ÷6÷WF…÷vFW%÷vVÆÇ6(	B6÷WF‚vFW"ÂÆ6ÆÆRÂÆ¶RÂvVÆÇ2(	Bæ÷r6'&–W2¢¦V–v‡@¦æöç–Ö÷W2&öög2¢¢Â6—‚&–æ6—ÂæBGvò–&B'V–ÆF–æw2Âöâ6—‚öb—G26WfVâg&VRÆ÷G2Âv—F‚Æ÷B¢‡F†RÆ¶RÖæBÕvVÆÇ26÷&æW"’ÆVgB÷VâæBÆ÷Bb†VÆB'’'VgW2'&÷vâw2&ö&F–ær†÷W6Râ¢¥7FæF–æp§&öög2#s2(i"#ƒ²&VÖ–æ–ær3“"(i"3ƒBÂCböbF†VÒöâ6÷fW&VBw&÷VæB¢¢‡v2SB’â–æfW'&VB†÷W6V†öÆG0£ƒb(i"ƒ‚Â–æfW'&VBW'6öç2“‚(i"â&V6÷&FVB–âÃâ¢¥F†R&V6—R6ÆV&VBWfW'’Æ6VÖVçBvFRöà¦—G2f—'7B'VâæBæòFööÂ6†ævVB¢¢(	BF†R6V6öæB&Æö6²–â&÷rFòFò6òÂv†–6‚—2v†BBÔ‚6–B¦&Æö6²&6VÂ6†÷VÆBæ÷rÆöö²Æ–¶Rà ¢¢¥D„Rd”äD”är•2D„B%TÄRbDôU2äõB4’t„B•Bt255TÔTBDò4’ÂäB•B•2õTäTB2³#‚â¢ ¥&VBÆ—FW&ÆÇ’Â¢¦f÷W"¢¢öbF†—2&Æö6²w26—‚GvVÆÆ–æw272ÆÂF‡&VRF÷F–öâFW7G2f÷"öæRG&FP¦÷"F†R÷F†W"(	BF†RC2¦æBF†RCB¢f÷"6'VçFW'2†öæR6'VçFW"†÷W6V†öÆB7FæG2–âCBÂ–âF†P¤æ÷'F‚F—f—6–öâ’ÂF†RC¦æBF†RC"¢f÷"Æ&÷W&W'2†f÷W"7FæB–âC'2’âF†R'VÆR—26–ÆVçBöâ†÷p¦Öç’&öög2öböæR&Æö6²6–ævÆRG&FRÖ’F¶RÂ&V6W6Ræò&Æö6²&Vf÷&RF†—2öæRFVÇBG&FRGvð¦öb—G2fÖ–Æ–W2âöæRF÷F–öâW"G&FRv2F¶VâæBF†R÷F†W"Gvò&VgW6VBÂöâF†R&VF–ærF†@§'VÆRbw2÷vâ÷Væ–ær6VçFVæ6R(	BF†RÖ—‚—26Æ–Ò&÷WBF†RF÷vâÂæ÷B&÷WBv†B†2&VVâG&vâ(	@¦f÷&&–G2öæR&Æö6²w2FVÂg&öÒ&—6–ærG&FRw26÷VçBGv–6Râ¢¥F†B—26†ö–6RæB—2&V6÷&FVB0¦öæR¢¢Â–â&÷F‚6Vç7W2&wVÖVçG2æB–âÃÂ6òF†RæW‡B&6VÂÖVWG2â&wVÖVçB—B6âF—6w&VP§v—F‚&F†W"F†â&V6VFVçB—B†2FòwVW72Bâ³#‚—2&—6VBFòÖ¶R—B6öFRà ¢¢¥F‡&VRFö7VÖVçFVB7F÷&W2öâF†—2&Æö6²7FæB”å4”DRF†RÆGFVB6÷WF‚vFW"6÷'&–F÷"¢¢(	B¦öæW2w0¦w&ö6W'’'’¢£BãRÒ¢¢Â†–Æò6'VçFW"w27F÷&R'’¢£bãbÒ¢¢ÂV6²w27F÷&R'’¢£‚ã"Ò¢£²GvòöbF†P§F‡&VRÆæòÆ÷BöbF†R&Æö6²BÆÂâBÔrW7F&Æ—6†VBF†B&R×ÆB&V6÷&G26â7FæB&ÖWG&R÷ §Gvò&÷VB"öbF†V—"g&öçFvRæBÖV7W&VBv†BF†BFöW2Fòö67Wæ7“²F†R–çG'W6–öâ—G6VÆb†@¦æWfW"&VVâÖV7W&VBâ—B6÷7BF†—2&6VÂæ÷F†–ær(	BF†RæV&W7B–çfVçFVB&ööbFòç’öbF†RF‡&VR—0¢¢£rã“’Ò¢¢v–ç7B2ÒvFR(	B6ò—B—2÷VæVB2¢¤³3¢¢&F†W"F†âF÷V6†VB–ç6–FR&Æö6°§&6VÂâF‡&VRæÖVB'V–ÆF–æw2&RG&vâ7FæF–ær–â7G&VWBÂæBV—F†W"F†R7G&VWBÂF†R÷6—F–öç0¦÷"ƒ3R6÷WF‚vFW"7G&VWB—2v†B—2w&öærà ¢¢¤Ã“’w26öÖÖW&6–ÂÖg&öçFvR&6VÂF–Bæ÷BW†—7Bâ¢¢F†BVçG'’6—2F†RVW7F–öâv2÷VæVB2¥$ôDÔ&6VÃ²F†R”B—BæÖW2v2Ç&VG’6''––ærF†R6öæf–FVæ6RÖ&æB&6VÂÂ6òF†W&R†2&VVà¦Æ–&W'G’v—F‚æòv÷&²—FVÒ&V†–æB—Bâ—B—2÷VæVB&÷W&Ç’2¢¤³#’¢¢ÂæBF†—2&Æö6²—2—G0§6V6öæB–ç7Fæ6S¢F†R&öw&ÖÖRFVÇBÆör6&–âæBÆæ²6†çG’FòF†RF÷vâw2'W6–W7@¦6öÖÖW&6–Âg&öçFvRf÷"F†R6V6öæBF–ÖR'Vææ–ærÂæBF‡&VR6÷WF‚vFW"&Æö6·2&R7F–ÆÂ÷Vâà ¢¢¤f÷W'F‚ÖV7W&VÖVçBöb³#¢¢¢–ç6W'F–ærGvò†÷W6V†öÆG2&VæÖVB¢£’öbF†R“‚6'&–VBÖ÷fW ¦–çfVçFVBW'6öç2¢¢Âv–ç7B3"ÖöbÓ“bBBÔ‚Â#RÖöbÓ“BBBÔ&‚æBrÖöbÓ32×F÷V6†VBBBÔRâæð¦w&FRÖ÷fVBæBWfW'’æÖUö&6—6¶WB—G2ööÂ6—FF–öâÂ6òF†—2—26‡W&â&F†W"F†â§&÷fVææ6Rf–ÇW&R(	Bf÷"F†Rf÷W'F‚&Æö6²–â&÷rà ¢22f—†VB##bÓ‚ÓR(	BF†R6†ævVÆörw2ÖW&vRG&—fW"v26÷''WF–ærF†Rf–ÆRÂ6–ÆVçFÇ’ÂWfW'’F–ÖP ¢¢¤³#râ¢¢æv—FGG&–'WFW6ÖW&vVB§2ö6†ævVÆöræ§6v—F‚ÖW&vS×Væ–öæ6òF†BGvò'&æ6†W2V6€§6†—–ærâVçG'’v÷VÆBæ÷B6öæfÆ–7BâF†R7FFVB†¦&Bv2'Gvò'&æ6†W2VF—F–ærF†R6ÖRW†—7F–æp¦VçG'’"Â6ÆÆVB&&S²F†RWfW'–F’&WVæBv26ÆÆVB6fRâ¢¥F†B—2&6·v&G2â¢  ¥Væ–öâ—2Ä”äRVæ–öâæB6†ævVÆörVçG'’—2æ÷BÆ–æRâv†Vâ&÷F‚6–FW2&WVæBÂF†R6†&V@¦6Æ÷6–ærÒÒÆ—26öÖÖöâ6öçFW‡BæB7W'f—fW2¢¦öæ6R¢¢(	B6òF†Rf—'7BVçG'’7vÆÆ÷w2F†R6V6öæ@¦æBF†RÆ—FW&Â—2ÆVgBv—F‚âVæ6Æ÷6VB'&6¶WBâF†R&W7VÇB—27F–ÆÂfÆ–B¦f67&—BÂ6ð¦æöFRÒÖ6†V6¶76W2—BæBæ÷F†–ærF÷vç7G&VÒæ÷F–6W2à ¢¢¤ÖV7W&VC¢f—fR6öç6V7WF—fRÖW&vW2–âöæRF’¢¢‚3#bÂ33"Â33bÂ33’æB"Ô%TsB’V6‚&öGV6V@¦W†7FÇ’F†—26÷''WF–öâæBV6‚æVVFVBF†R6ÖRÖçVÂ&W—"(	B&V'V–ÆBg&öÒF†R&6R6÷’æ@§&R×7F×âVæ–öâF–Bæ÷B&WfVçB6–ævÆR6öæfÆ–7Bâ—B6öçfW'FVBf—fRÆ÷VB6öæfÆ–7G2–çFòf—fR6–ÆVç@¦6÷''WF–öç2F†B†BFò&R&W—&VB'’†æB&Vv&FÆW72à ¥F†R6†ævVÆörÖW&vW2æ÷&ÖÆÇ’æ÷râGvò'&æ6†W2F†B&÷F‚6†—âVçG'’6öæfÆ–7BÂÆ÷VFÇ’ÂBF†P¦ÖW&vRÂæBF†R&W6öÇWF–öâ—2F†Rö'f–÷W2öæS¢¶VW&÷F‚ÂæWvW7Bf—'7BÂ&R×'Và¦FööÇ2÷7F×Ö6†ævVÆöræÖ§6à ¢¢¤æB6Æ–Ò–âF†B6öÖÖVçBæVVFVB6÷'&V7F–ærÂF†÷Vv‚æ÷BF†Rv’’f—'7Bw&÷FR—Bâ¢¢F†R6öÖÖVç@§6–B'F†R6öçG&7B6†V6²6F6†W2F†B(	BfW'6–öç2×W7B&R7G&–7FÇ’FV7&V6–ær"â’&V6÷&FVBF†B0¦æWfW"w&—GFVââ¢¥F†Bv2w&öæs¢F†R'VÆRW†—7G2–â6†V6²Ö6†ævVÆöræÖ§6æBÇv—2†2â¢¢v†B—@¦6ææ÷BFò—2&W÷'B(	B—B6—G2gFW"F†RÖöGVÆRÆöBÂæBF†R6†RvÆ²&÷fR—BW†—G2F†RÖöÖVçB¦'&6¶WB—2Væ&Ææ6VBâF†RÖW&vRF†BGWÆ–6FW2fW'6–öâ—2F†R6ÖRÖW&vRF†B'&V·2F†R6†RÀ§6òWfW'’'VâF–VBöâF†R6†Rf—'7BæBF†RGWÆ–6FRv2æWfW"æÖVC²F†R†æB&W—"F†Vâ&V'V–Ç@§F†Rf–ÆRg&öÒ&6R6÷’æBFöö²F†RGWÆ–6FRv—F‚—Bâ6÷'&V7B6†V6²ÂVç&V6†&ÆR–â&V6—6VÇ§F†R66R—Bv2w&—GFVâf÷"à ¥F†RfW'6–öâ'VÆR—2æ÷rVæf÷&6VB–âF†R¢§FW‡B66â¢¢2vVÆÂÂv†–6‚'Vç2&Vf÷&RF†BW†—BÂ6ò¦GWÆ–6FR—2æÖVBWfVâv†VâF†RÆ—FW&Âv–ÆÂæ÷BÆöB(	BæBv2–âF†RçVÖ&W&–ær&R&W÷'FVBFöòÀ¦&V6W6RvÖVç2âVçG'’v2G&÷VB–âÖW&vRâfW&–f–VBFòf–Âöââ–æ¦V7FVBGWÆ–6FP¦&Vf÷&R&V–ær6öÖÖ—GFVBà ¢¢¥F†R6ÖRÖW&vS×Væ–öæÆ–æRæBF†R6ÖRW‡÷7W&RW†—7B–âF†R÷F†W"fÆVWB2¢¢‡öÆV6B×ÆFf÷&Ð¦Fö72õ4„TÄÂÔ’æÖB*rF†RfÆVWB6†ævVÆör6öçG&7B’âF†—2&Wò—2f—†VC²F†RfÆVWB—2æ÷Bà ¢22ÔT5U$TB##bÓ‚ÓR(	BF†Rw&÷VæB–÷R6VR—2æ÷BF†Rw&÷VæBF†RF÷vâ—2æ6†÷&VBFð ¢¢¥"Ô%Ts62Öâ¢¢F†R÷væW"&W&öGV6VBF†R–çf—6–&ÆRæV"Öf–VÆB&öBv—F‚F†R"Ô%Ts2f—‚–ââF†R6W6P¦—2æ÷rÖV7W&VBÂæB—B—2æ÷BF†R7G&VWG2BÆÂà ¤BF†R&W÷'FVB÷6RÂF†RE$tâw&÷VæB6—G2¢£’ãbFò2ã6Ò&÷fRFW'&–âç7W&f6T†V–v‡B‚–¢¢ÂF†P§6×ÆW"F†B&öG2ÂÆçG2Â'V–ÆF–æw2æB6öÆÆ—6–öâ&RÆÂÆ6VBv—F‚(	B÷fW"F†Rv†öÆR‡VæG&V@¦ÖWG&W2Âæ÷B§W7BæV"F†R6ÖW&âÄ”eEôÖÂF†R&öBw2Æ–gB&÷fRF†B6×ÆW"Â—2¢£#"ÖÒ¢¢âF†P§&öGv’—2VæFW"F†Rf—6–&ÆRw&÷VæBÆöær—G2VçF—&RÆVæwF‚†W&RÂæB6ò—2ç—F†–ærVÇ6R&ö÷FVB'§F†R6ÖR6×ÆW"Âv†–6‚—2v‡’F†Rw&72GVgG2F—6V"v—F‚—Bà ¢¢¥v‡’F†R&öB7F–ÆÂ6†÷w2&W–öæB&÷WB6WfVâÖWG&W3¢¢¢F†RöÇ–vöâöfg6WBv–ç2B&ævRæBÆ÷6W0§W6Æ÷6RÂ&V6W6RFWF‚Ö'VffW"&W6öÇWF–öâ—2f–æW7BæV"F†R6ÖW&âF†R7&÷76÷fW"—2gVæ7F–öâö`¦F—7Fæ6RÆöæR(	Bv†–6‚—2v‡’F†R&÷VæF'’—26ÆVâ†÷&—¦öçFÂÆ–æRB6öç7FçB&F—W2ÂF†RöæP¦fVGW&RöbF†R÷væW"w267&VVç6†÷G2F†Bæò÷F†W"W‡ÆæF–öâ66÷VçFVBf÷"à ¢¢¤f—6—F÷"7FæG226Ò7Væ²–çFòF†RFW'&–âF†W’6â6VRâ¢¢W–RB"ãCSR÷fW"6×ÆW"&VF–æp£ãssR—2F†R&V6÷&FVBãc‚ÒöbW–R†V–v‡C²F†RG&vâw&÷VæBVæFW"F†B6ÖRö–çB—2ã“bà ¢¢¥v†B—2äõBW7F&Æ—6†VC¢v†–6‚öbF†RGvò—2w&öærâ¢¢F†RG&vâ7W&f6R—2&¶VBtÄ"ÂF†P§6×ÆW"&VG2†V–v‡Ff–VÆBæ&–æÂ&÷F‚FW66VæBg&öÒF†R6ÖRFW'&–â7V2ÂæBF†—2ÖV7W&VÖVçB6—0¦öæÇ’F†BF†W’F—6w&VRâ&—6–ærÄ”eEôÖv÷VÆB†–FRFGVÒF—6w&VVÖVçB&V†–æBgVFvRæBÆVfP¦'V–ÆF–æw2æB6öÆÆ—6–öâw&öærâÆæFVB2ÖV7W&VÖVçBÂ&VBÂv—F‚æòf—‚(	Bv†–6‚—2v†BF†R&6VÀ¦6¶VBf÷"æBv†B6fVB"Ô%Ts"g&öÒf—‚F†Bv÷VÆB†fRÖFRF†–æw2v÷'6Rà ¢22æWr##bÓ‚ÓR(	Bf—fR–çfVçFVB†÷W6W2öâF†RF÷vâw2'W6–æW72g&öçBÂæBF†R6†&RÖ÷WBF†BWBF†VÒF†W&P ¢¢¥BÔ‚¢¢ÂæB—B—2F†Rf—'7B&Æö6²&6VÂ6–æ6RBÔRF†B7GVÆÇ’'V–ÇB&Æö6³¢BÔbæBBÔp¦V6‚6WB÷WBFòf–ÆÂöæR–âæBf–æ—6†VBW&W—&–ærF†R&—F†ÖWF–2F†BFV6–FW2v†B&Æö6²Ö¦&RFVÇBâ&Æµ÷6÷WF…÷vFW%ög&æ¶Æ–æ(	B6÷WF‚vFW"ÂvVÆÇ2ÂÆ¶RÂg&æ¶Æ–â(	Bæ÷r6'&–W2¢§6WfVà¦æöç–Ö÷W2&öög2¢¢Âf—fR&–æ6—ÂæBGvò–&B'V–ÆF–æw2Âöâf—fRöb—G26—‚g&VRÆ÷G2Âv—F‚Æ÷B¢‡F†RÆ¶RÖæBÔg&æ¶Æ–â6÷&æW"’ÆVgB÷Vââ¢¥7FæF–ær&öög2#cb(i"#s3²&VÖ–æ–ær3“’(i"3“"ÂSBö`§F†VÒöâ6÷fW&VBw&÷VæB¢¢‡v2c’â–æfW'&VB†÷W6V†öÆG2ƒB(i"ƒbÂ–æfW'&VBW'6öç2“b(i"“ƒ²F÷FÇ0£S‚†÷W6V†öÆG2æB“BV÷ÆRâ&V6÷&FVB–âÃ“’à ¢¢¥F†R&V6—R6ÆV&VBWfW'’Æ6VÖVçBvFRöâ—G2f—'7B'VâæBæòFööÂ6†ævVB¢¢Âv†–6‚—2F†P§6†RBÔ"&VF–7FVBF†W6Rv÷VÆB6WGFÆR–çFòæBv†–6‚BÔbæBBÔr&÷F‚–çFW''WFVBà ¢¢¥D„Rd”äD”är•2$õUBD„R4„$RÔõUBÂäõB$õUBD„•2$Äô4²ÂäB•B•2õTäTB2³#Râ¢¢F†—2—2F†P¦f—'7B&Æö6²F†—2ÆæR†2f–ÆÆVBöâ6÷WF‚vFW"7G&VWB(	BF†RF÷vâw2'W6–æW72g&öçBÂv†W&RWfW'¦Fö7VÖVçFVB&ööböâ÷"&W6–FRF†R&Æö6²—26öÖÖW&6–Ã¢F†RFV×ÆR'V–ÆF–ærÂF†RW†6†ævR6öffVP¤†÷W6RÂ¢â‚â¶–ç¦–Rw2f÷'v&F–ær7F÷&RÂæWv&W''’bFöÆRw2v&V†÷W6RvW7BæB‚â¦öæW2w27F÷&RV7Bà¥F†RccR×&ööb&öw&ÖÖRFVÇB—B¢¦f—fR÷&F–æ'’GvVÆÆ–æw2ÂöæRöbF†VÒC"Ææ²6†çG’¢¢Â&V6W6P¦FööÇ2÷&V6öæ6–ÆUóccRç–÷'F–öç2fÖ–Æ–W2'’D•5E$”5BæB†2æòæ÷F–öâöbv†B7G&VWBv0¦f÷"âF†R&Æö6²v2'V–ÇB2FVÇB(	BF†R÷'F–öæÖVçB—2F†R&öw&ÖÖRw26Æ–ÒæB÷fW'&–F–ær—B'¦†æBöâF†RF’—B&öGV6W2âv·v&B&W7VÇB—2†÷r&V6öç7G'V7F–öâ&V6öÖW2–7GW&R6öÖV&öG¦Æ–¶VB(	B'WBF†RFVfV7B—2æ÷rw&—GFVâF÷vâ–âF‡&VRÆ6W2&F†W"F†â'6÷&&VB6–ÆVçFÇ’ÂæB—@§v–ÆÂ&V7W"öâ&Æµ÷6÷WF…÷vFW%÷vVÆÇ6Â&Æµ÷6÷WF…÷vFW%öÆ6ÆÆVÂ&Æµ÷6÷WF…÷vFW%ö6Æ&¶À¦&Æµ÷6÷WF…÷vFW%öFV&&÷&ææB&ÆµöÆ¶UöÖ&¶WF¢¢§6—‚öbF†RFVâ÷Vâ&Æö6·2g&öçB6öÖÖW&6–À§7G&VWBâ¢  ¢¢¥BÔrw26V6öæBFW7B—2f–æF–6FVB'’ÖV7W&VÖVçBÂv†–6‚—2v†BF†—2&Æö6²v2–â÷6—F–öâFð¦Fòâ¢¢BÔrÆVgBÆ÷B"66†VGVÆ&ÆR&V6W6R¶–ç¦–Rw27F÷&RÆ2—BöæÇ’–ç6–FRF†RãRÒÖ&v–à§7G&—â–bF†B†B&VVâFöòvVæW&÷W2ÂF†—2&6VÂ—2v†W&R—Bv÷VÆB†fRf–ÆVBâ—BF–Bæ÷C¢F†P¦Æ÷B"&ööb7FæG2¢£rã2Ò¢¢g&öÒ¶–ç¦–Rw27F÷&Rv–ç7B2ãÒ6W&F–öâvFRÂæBWfW'’÷F†W §&ööbF†—2&6VÂÆ6W2—2gW'F†W"g&öÒ—G2÷vâæV&W7BæV–v†&÷W"F†âF†Bà ¢¢¤&÷F‚F÷F&ÆRG&FW276VB'VÆRböâöæR&Æö6²Âf÷"F†Rf—'7BF–ÖR6–æ6RF†R'VÆRFöö²—G0§F†—&BFW7Bâ¢¢W†7FÇ’GvòG&FW2r6öÖÖ—GFVB&wVÖVçG26ÆÂF†V—"÷vâ6÷VçG2fÆö÷"(	B6'VçFW"æ@¦Æ&÷W&W"(	BæBF†—2&Æö6²v2FVÇBC2æBC–âF†R6÷WF‚F—f—6–öâÂv†–6‚—2&V6—6VÇ’F†P¦fÖ–Ç’V6‚—2Ç&VG’†÷W6VB–âF†W&Râ&÷F‚vW&RF÷FVBƒ7F‚6'VçFW"ÂWF‚Æ&÷W&W"’âF÷F–æp¦öæÇ’öæRÂ2WfW'’&6VÂ&Vf÷&RF†—2F–BÂv÷VÆB†fR&VVâ&VfW&Væ6R&F†W"F†âF†R'VÆP¦6†ö÷6–ærà ¢¢¤³#ÖV7W&VBF†—&BF–ÖRÂæB—B—2F†Rv÷'7B&VF–ær–WBâ¢¢–ç6W'F–ærGvò†÷W6V†öÆG2&VæÖV@¢¢£#‚öbF†RƒB6'&–VBÖ÷fW"–æfW'&VB†÷W6V†öÆG2æB3"öbF†R“b6'&–VBÖ÷fW"–çfVçFVBW'6öç2¢¢(	@¦F†—&BöbF†RÆ–W"(	Bv–ç7B#RÖöbÓ“BBBÔ&‚æBrÖöbÓ32×F÷V6†VBBBÔRâæòw&FRÖ÷fVBÂæð¦æÖUö&6—6Æ÷7B—G2ööÂ6—FF–öâÂæB6†V6²ç6†&RÖFW&—fW2ÆÂ“‚Â6òF†—2—26‡W&â&F†W"F†à¦&÷fVææ6Rf–ÇW&Râ³#w2÷vâFW‡B6—2F†Rf—‚&VÆöæw2–â—G2÷vâ&6VÃ²—B†2æ÷r&–FFVà¦Æöærv—F‚&Æö6²F‡&VRF–ÖW2ÂæB—B—2F†R&V6öâF†—2"w2F–fb—2Crf–ÆW2v–FRf÷"6†ævP§v†÷6R&VÂ6öçFVçB—26WfVâ'V–ÆF–æw2à ¢¢¤äB•BDôU2äõB4„•âD„RDU4µDõE$rÔ4ÄÂ%TDtUB•2U„4TTDTBäBD„•2$4TÂ•2t„BU„4TTDT@¤•Bâ¢¢FööÇ2ö6†V6²ç6†—2w&VVââF†RÖö&–ÆRf–Ww÷'B—2w&VVâ(	BC’76W'F–öç2Â¦W&òvRW'&÷'2à¥F†RFW6·F÷f–Ww÷'Bf–Ç2f÷W"76W'F–öç2f÷"öæR&V6öââÖV7W&VBöâF†RV&Æ—6†VBÖ—'&÷"@£#ƒ9sƒÂ&÷F‚'Vç2gVÆÂæB–âF†Rf÷&Vw&÷VæC  §ÂÂG&r6ÆÇ2Â'VFvWBÂfW&F–7BÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§ÂFWdS#cC3F†&6VÆ–æR’Â¢£sR¢¢ÂƒÂ72À§ÂF†—2'&æ6‚Â³r&öög2Â¢£ƒB¢¢ÂƒÂ¢¦f–Â¢¢ÂæBF†RF‡&VRW"×F–W"FWF–Â6V–Æ–æw2v—F‚—BÀ ¢¢¥6WfVâ&öög26÷7Bæ–æRG&r6ÆÇ2â¢¢"Ôs&ö¦V7FVB³W"’&V6÷&G3²F†Rö'6W'fVB&FR†W&R—0§7FVWW"ÂæB—Bv27VçBv–ç7Bf—fR6ÆÇ2öb†VG&ööÒâF†—2—2¢¥"ÕsV¢¢Â'&—f–ærV&Æ–W"F†à¦—G2÷vâ7G&–v‡BÆ–æR&VF–7FVBÂæBF†R÷W&F–öæÂ6öç6WVVæ6R—2&ÇVçC¢¢¦ÆæR"6ææ÷BÆæ@¦æ÷F†W"&Æö6²VçF–Â"ÕsVÆæG2â¢¢æ–æR÷Vâ&Æö6·2&VÖ–âæBæ÷BöæRöbF†VÒ—26ÖÆÆW"F†âF†P¦öæRF†B'&ö¶R—Bà ¢¢¥F‡&VRF†–æw2vW&RäõBFöæRFòÖ¶R—Bw&VVâ¢¢ÂÆ—7FVB&V6W6RV6‚—2FV×F–ær6†÷'F7WBâF†P¦'VFvWBv2æ÷B&—6VB(	Bâ76W'F–öâÖ÷fVBFòFÖ—Bv†B—Bv2ÖV7W&–ær—2æ÷BvFRâ&öög2vW&P¦æ÷BG&÷VB(	BF†R66†VGVÆRFVÇ26WfVâÂæB'V–ÆF–ærf—fRFò6F—6g’g&ÖR&FR—2f—GF–ærF†P§F÷vâFòF†R&VæFW&W"â"ÕsVv2æ÷Bf—†VB–âF†—2'Vâ(	B—B—2ÆæR&6VÂv—F‚ÆæR ¦Ç&VG’–âfÆ–v‡BÂæB&F6†–ærF†R66VæR—2Væ—Böb—G2÷vâà ¢¢¤öæR&VæFW&W"ÖF¦6VçBf—‚•2–âF†—2'&æ6‚Â&V6W6RF†R&6VÂ6÷VÆBæ÷B&RF–væ÷6VBv—F†÷W@¦—Bâ¢¢FööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6f–ÇFW&VBFW'&–â&ö&ÆV×2v—F‚÷FW'&–çÇvFW"ö–v–ç7BF†P§v†öÆRÖW76vRÂ6ò&Æµ÷6÷WF…÷vFW%ög&æ¶Æ–æ(	BF†Rf—'7B&Æö6²v†÷6R–B6öçF–ç2F†Rv÷&B(	BGW&æV@§Gvò÷&F–æ'’Æ6V†öÆFW"Ö76WBæ÷FW2–çFò&W÷'FVBFW'&–âÆöBf–ÇW&Râæ6†÷&VBFð¦õåÇ2¢‡FW'&–çÇvFW"•Æ"ö–Âv†–6‚—2v†BF†R6öFRw2÷vâ6öÖÖVçBÇv—26Æ–ÖVBÂæBfW&–f–V@¦v–ç7B&VÂFW'&–âÆWö6ƒã¢(
fæBvFW#¢(
fÖW76vW2–â&÷F‚F—&V7F–öç2âf—fRöbF†RFVâ÷Và¦&Æö6·2&R&Æµ÷6÷WF…÷vFW%ò¦à ¢¢¥v†BF†—2&6VÂF–BäõBFòâ¢¢—BF–Bæ÷B&RÖ÷'F–öâF†R66†VGVÆR„³#R’Â—BF–Bæ÷Bf—‚F†P¦æÖRÆÆö6F÷"„³#’Â—BF–Bæ÷Bf—‚F†RG&rÖ6ÆÂ'VFvWB…"ÕsV’ÂæB—BF–Bæ÷Bç7vW"v†WF†W ¦öæR÷VâÆ÷BW"&Æö6²—2F†R&–v‡Bf6æ7’(	BF†RVW7F–öâBÔbÆVgB7FæF–æræBæ÷F†–ær†W&P§F÷V6†W2à¢22f—†VB##bÓ‚ÓR(	BvWB6÷&æW"v2FVÆWF–ærv†öÆRæVÇ2öb&öBÂG'’†Æb–æ6ÇVFV@ ¢¢¥"Ô%TsB¢¢Â÷væW"×&W÷'FVBg&öÒ6÷WF‚vFW"7G&VWB26ÆVâÖVFvVBw&VVâVG&–ÆFW&ÂVæ6†V@§F‡&÷Vv‚F†R&öGv’â7G&VWG2æ§6G&÷VBæVÂ÷WG&–v‡Bv†VâF†R6VçG&VÆ–æR¢¦÷"ç’öb—G2f÷W ¦6÷&æW'2¢¢fVÆÂöâvFW"âF†R6öÖÖVçB6–BF†RVFvRFW7B¶WB&æ²&öBg&öÒ–çF–ær÷fW"vFW §v†W&R—G2ÆVvÂ6÷'&–F÷"&V6†VB—B(	BF†R&–v‡B–ÒæBF†Rw&öær–ç7G'VÖVçBÂ&V6W6RFVÆWF–ærF†P§æVÂF¶W2F†RG'’†Æbv—F‚—Bà ¤—B6Æ—2BF†RvFW&Æ–æRæ÷rÂV6‚VæBG&–ÖÖVBöâV6‚6–FR–æFWVæFVçFÇ’'’&—6V7F–öâ÷WBg&öÐ§F†RG'’6VçG&VÆ–æRâ7–ÖÖWG&–2öâW'÷6S¢&æ²&öB—2vWBöâöæR6–FRöæÇ’ÂæB6‡&–æ¶–ær—@§7–ÖÖWG&–6ÆÇ’v÷VÆBF‡&÷rF†RG'’fW&vRv’2vVÆÂâF†R6VçG&VÆ–æRFW7B—2Væ6†ævVB(	B&ö@§v†÷6R6VçG&R—2–âF†R&—fW"—27&÷76–ærÂæB7&÷76–ær—2'&–FvRw2¦ö"à ¢¢¤ÖV7W&VBöâF†R'V–ÇBvVöÖWG'“¢¢¢BÃƒC2æVÇ2†fRG'’6VçG&VÆ–æRÂ¢¦ÆÂBÃƒC2æ÷r&V6‚F†P§&–&&öâ¢¢Â#‚6Æ—VBBF†RvFW&Æ–æRÂG&÷VB27V"ÖÖWG&R6Æ—fW'2Â¢£c"ãrÒöb&öGv§&V6÷fW&VB¢¢âF†R2VG2òã3Öf—'7B&V6÷&FVBf÷"F†—2'Vrv2&VBöfbG'Væ6FVB&ö&P¦Æ—7F–æræBv2¢¦†ÆbF†RG'VRf–wW&R¢£²6÷'FVBF&ÆR&VBg&öÒ—G2F–Â—2æ÷BF÷FÂÂæBF†P¦çVÖ&W"–âF†R&öFÖæB6†ævVÆör—2æ÷rF†RÖV7W&VBöæRà ¥F†RvFR76W'G2F†R–çf&–çB&F†W"F†âF†RçVÖ&W"(	BWfW'’æVÂv—F‚G'’6VçG&VÆ–æR&V6†W0§F†R&–&&öâÂF†RöæÇ’W&Ö—GFVB'6Væ6W2&V–ær7V"ÖÖWG&R6Æ—fW'2Âv†–6‚&R6÷VçFVBæB&–çFVB(	@¦æB—B76W'G2F†B6Æ—–ær7GVÆÇ’†Vç2Â6òÆFW"6–×Æ–f–6F–öâ&6²FòFVÆWF–ærF†RæVÀ¦f–Ç2–â4’&F†W"F†â–â67&VVç6†÷Bà ¢22$TõTäTB##bÓ‚ÓR(	BF†R÷væW"&W&öGV6VBF†R–çf—6–&ÆR&öBt•D‚F†Rf—‚–âÂæB—B—2æ÷BF†R7G&VWG0 ¥&W÷'FVBv–âF†R6ÖRWfVæ–ærÂÖö&–ÆRÂÆ¶R7G&VWB&ö6†–ærg&æ¶Æ–â(	BgFW"F†RVçG'’&VÆ÷p¦FV6Æ&VB—B6öÇfVBâ&W&öGV6VBBF†BW†7B÷6Râ¢¤f÷&6VBgVÆÇ’÷VRÂFWF‚×w&—F–ærÂBF†P¦Ö&¶W"72w2÷vâöÇ–vöâöfg6WBÂF†R&–&&öâ7F–ÆÂ&V6†W2öæÇ’&÷r“3röbSc¢F†R&÷GFöÒCP¦öbF†Rg&ÖR†öÆG2æò&öGv’Bç’÷6—G’â¢¢æB—B—2æ÷B7G&VWG2fVÇB(	BW"×&÷rFWF–À¦VæW&w’fÆÇ2g&öÒãÓ"ãB&÷fR&÷rFòã"&VÆ÷r&÷r#Â6òF†R&öBÂF†Rw&72GVgG2æ@§F†Rw&÷VæBFW‡GW&RÆÂfæ—6‚FövWF†W"BöæR&F—W2âF†RvVöÖWG'’—2&W6VçBƒ3"7G&VWBfW'F–6W0§v—F†–âÒ“²6öÖWF†–ær—2'W'––ær—Bâ&V6÷&FVB2¢¥"Ô%Ts62¢¢ÂF÷öbF†R&VæFW&–ærVWVRÂv—F€§F†RVçFW7FVB‡—÷F†W6—2æÖVBæBF†R–ç7G'V7F–öâFòÖV7W&RF†RG&vâFW'&–âv–ç7@¦FW'&–âç7W&f6T†V–v‡B‚–&Vf÷&R6†æv–ærç—F†–ærà ¢¢¥F†RvFRvVçBw&VVâ&V6W6R—G2æWr7FF–öâ7FæG2B7&÷76–ær¢¢(	BöæRöbF†RfWrÆ6W2F†P¦æV"w&÷VæB—2–çF7B(	BæBF†R÷væW"v2s"gB6†÷'BöböæRâF†—&BF–ÖRöâF†—2'VrF†BF†P¦ç7vW"v2v†W&RF†RvFRv2ö–çFVBÂæBF†R&6VÂF†Bw&÷FRF†BÆW76öâF÷vâ&WVFVB—Bà ¤6V6öæBÂ6W&FRfVÇB6ÖR÷WBöbF†R6ÖR&W÷'G2‚¢¥"Ô%TsB¢¢“¢FE&V6÷&FG&÷2v†öÆR&ö@§VBv†Vâå’öb—G2f÷W"6÷&æW'2—2vFW"ÂG'’†Æb–æ6ÇVFVBâ¢£2VG2òã3Òöb&öGv¦FVÆWFVBv†–ÆRF†R6VçG&VÆ–æR—2G'’ÆæB¢£²¶–ç¦–RÆ÷6W2Bã"Röb—G6VÆbâ6Æ—BF†RvFW&Æ–æRÀ¦Fòæ÷BF—66&Bà ¢22æWr##bÓ‚ÓR(	BF†R†÷&—¦öâ×F–Ö&W"f–wW&Rv266÷&–ærF†RF÷vâw2&öög2ÂæBF†Rf—‚f÷"—B—27V'G&7F–öâ&F†W"F†â6öÆ÷W"FW7@ ¢¢¥"ÕsFâ¢¢$TäDU$”är*rR6·2f÷"¢®(šR“R¢¢†÷&—¦öâ×F–Ö&W"6öÇVÖâ6÷fW&vRâF†RçVÖ&W"ç7vW&–æp§F†BVW7F–öâ6÷VçFVB¢¦ç’¢¢'&V²–âF†R6·–Æ–æR&÷fRF†RÆæB÷6·’Æ–æRÂæBv&ÆRVæB'&V·0¦6·–Æ–æR27W&VÇ’2âö²(	B"Ôs6Vv‡B&—&–U÷6÷WF†Ö÷f–ærã3cB(i"ãC3böâæ–æWFVVâæWp§&öög2v—F‚æò&VæFW&W"6†ævRâ¢¤6÷'&V7FVBÂ&—&–U÷6÷WF†&VG2ã#“RFW6·F÷v†W&R—B&V@£ãc3"ÂæBc"Röbv†Bv26÷VçFVB2F–Ö&W"F†W&Rv2F†RF÷vâ¢¢ƒC’öbS2ÖV7W&VB6öÇVÖç0¦'&ö¶Röâ&ööbæBöâæ÷F†–ærVÇ6R’â7&÷72F†R#"7FF–öâ×f–Ww÷'G2F†RÖVâfÆÇ2¢£ãcs"(i £ãSƒ"¢¢ÂæBF†RçVÖ&W"ÖVWF–ærF†RF&vWBfÆÇ2¢£(i"¢¢âgVÆÂF&ÆR–âFö72õ$ôDÔæÖF ¬*r"ÕsFà ¢¢¥F†RF—67&–Ö–æF÷"F†—2&ö¦V7B†Bw&—GFVâF÷vâFöW2æ÷Bv÷&²ÂæBF†Bv2ÖV7W&VB&F†W §F†â&wVVBâ¢¢"Ôs&÷÷6VBF†R7&÷vâÖ‡VR6†ææVÂ(	B&v†—FWv6†VBv&ÆR—2æ÷Bw&VVâ"âBF†P¦f—'7B†—B—†VÂöbWfW'’'&ö¶Vâ6öÇVÖâÂFW6·F÷¢w&W’v&ÆW2B&—&–U÷6÷WF†6—BBéD~(‰$ ¢¢¢³#"ãB¢¢Â†¦VBF–Ö&W"B&—&–U÷vW7F&ævW2¢¢³ãFò³rãR¢¢âF†RGvò÷VÆF–öç2÷fW&Æ ¦6ö×ÆWFVÇ’Â&V6W6RF†R†÷&—¦öâ6·’—27G&öævÇ’&ÇVRÖFöÖ–æçBæBWfW'’æöâ×6·’—†VÂ6ÆV'2³0¤~(‰$"FW7B(	BF†R6†ææVÂv2æ÷B×6·’FWFV7F÷"Â6òF†RöÆBf–wW&Rv2FW7F–ærF†R6ÖR6öæF—F–öà§Gv–6Râ¢¤æò6öÆ÷W"FW7B6â6W&FRF†VÒ–â&–æ6—ÆR†W&R¢£¢ÃrÖ¶W2W‡F–æ7F–öâF÷FÂ'£SÒÂ6òF—7FçBF–Ö&W"æBF—7FçBvÆÂ&÷F‚6öçfW&vRöâF†Rför6öÆ÷W"à ¢¢¥v†B&WÆ6VB—BF¶W2F†RF÷vâv’–ç7FVBöbwVW76–ærâ¢¢F†R†&æW72†÷Föw&‡2V6€§7FF–öâGv–6Rg&öÒF†R–FVçF–6Â÷6R(	Böæ6R2F†Rf—6—F÷"6VW2—BÂöæ6Rv—F‚F†R7G'V7GW&W6 ¦w&÷W†–FFVâ(	BæBÖV7W&W2F†R†÷&—¦öâ–âF†R6V6öæBg&ÖRâF–Ö&W"'’6öç7G'V7F–öã¢æð§F‡&W6†öÆBÂæò‡VRÂæ÷F†–ærFòGVæRÂæB¢§F†Rf–wW&R6ææ÷BÖ÷fRv†Vâ&Æö6²ÆæG2¢¢âF†RöÆ@¦çVÖ&W"—2¶WBB—G2öÆBfÇVRVæFW"æÖRF†B6—2v†B—B6÷VçG2‡6·–Æ–æR'&V·2’Â6ð£##bÓ‚ÓBw2&6VÆ–æR—27F–ÆÂ6ö×&&ÆRæBæò7Bf–wW&Rv26–ÆVçFÇ’&VFVf–æVBà ¢¢¥Gvò&÷W'F–W2öbF†RæWrf–wW&RF†B×W7B&RV÷FVBv—F‚—Bâ¢¢—B&—6W2B6—‚öbF†P£#"7FF–öâ×f–Ww÷'G2Â&V6W6R'V–ÆF–ær6â7FæB–âg&öçBöbF–Ö&W"æB†–FR—B(	B—Bç7vW'0¢¦—2F†R†÷&—¦öâF–Ö&W&VB¢Âæ÷B¦6âF†Rf—6—F÷"6VRF–Ö&W"7BF†RF÷vâ¢Âv†–6‚—2F†R&–v‡@§VW7F–öâf÷"F&vWBFW&—fVBg&öÒ†÷Föw&‡2öbG&VVÆ–æRâæBg&öÕö&÷fV—2âW&–Â÷6P§v†÷6R&æB—2æ÷B†÷&—¦öâBÆÂƒã#"òãSbÂF÷vâ6†&RR“¢Fòæ÷BfW&vR—B–âv—F†÷W@§6––ær6òà ¢¢¥VçfW&–f–VBòæ÷B6Æ–ÖVC¢¢¢æ÷F†–ær&÷WBF†R&VæFW&W"6†ævVBÂ6òæò66VæR6Æ–ÒÖ÷fW2v—F€§F†—2âF†R6÷7BöbF†R6V6öæB6GW&R—2ÖV7W&VBƒ2Ö–â"2f÷"F†RgVÆÂ&÷F‚×f–Ww÷'B'VâÀ¦v–ç7Bã"Ö–âv—F†÷WB—B’æBÒÖæòÖÖ6¶÷G2÷WBâWGF–ærF†RF÷vâ&6²v26†V6¶VB&F†W §F†â77VÖVC¢RÂ’æBSF–ffW&–ær—†VÇ2öbÃ#BÃ7&÷72F†R6†ævRÂ–ç6–FRF†R†&æW72w0¦÷vâ7&÷72×&ö6W72&W6–GVÂÂv—F‚F†RÒ×7F&–Æ—G–6öçG&7B76–ær'—FRÖ–FVçF–6Âà ¢22'FÇ’f—†VB##bÓ‚ÓR(	BF†R&öBB7&÷76–ærÂF†RGvò7FF–öç2F†BæWfW"7FööBöâöæRÂæBvFRF†B'7F–æVBW†7FÇ’v†Vâ—B6†÷VÆB†fR6†÷WFV@ ¢22æWr##bÓ‚ÓR(	BF†R&öBvFR6âæ÷r6VR6öçG&7B2vVÆÂ2Æ–v‡FæW72ÂæBF†R†÷Föw&‚—Bv2FöÆBFò6Æ–'&FRv–ç7B†2æò&öB–â—@ ¢¢¥"ÔÓâ¢¢F†R÷væW"'VÆVBöâ##bÓ‚ÓBF†BF†R&öBvFR6†÷VÆB66÷&RW‡÷7W&RÖ–çf&–ç@¢¢¦6öçG&7B¢¢æB¶VWâ'6öÇWFR¢¦fÆö÷"¢¢(	B&÷F‚&'2Âæ÷B&WÆ6VÖVçB(	BgFW""Õs¦ÆVv—F–ÖFVÇ’6†ævVBF†R66VæRw2W‡÷7W&RÂ&W6W'fVBF†R&öBöw&÷VæB&F–òFòv—F†–âãBRÂæ@¦Æ÷7BvFR—B†Bæ÷B&Vw&W76VBâ&÷F‚çVÖ&W'2&Ræ÷rÖV7W&VBBWfW'’&öB&æBÂB&÷F€§f–Ww÷'G2â¢¤æV—F†W"—2vFVB¢¢ÂæBF†B7Æ—B—2FVÆ–&W&FS¢F†R&6VÂw2÷vâ66WFæ6RæÖW0§F‡&VR'V–ÆG2Fò6Öö¶RæBF†RÆæRÆÆ÷w2&6VÂGvòÂ6ò—Bv27Æ—B–çFò¦ÆæBF†P¦ÖV7W&VÖVçB¢æB§6WBF†R&'2¢&Vf÷&R—Bv26Æ–ÖVBâvFRF†BÖ÷fW2BF†R6ÖRÖöÖVçB0¦—G2÷vâ&6VÆ–æR†2æò&6VÆ–æRà ¢¢¥F†RÖV7W&VÖVçB—2fW&–f–VBv–ç7BçVÖ&W"F†—2&ö¦V7B6öÖÖ—GFVB&Vf÷&RF†R6öFRFò6ö×WFP¦—BW†—7FVBâ¢¢"Õsw2&¶VBv÷&¶–ær&V6÷&FVBvV&W"¢£ã#r¢¢Bg&öÕö&÷fVÂFW6·F÷À£(	3#SÒÂF¶Vâ'’†æBBF†Rö–çBöbW6RöâFWdCsc&–âvV&W$6öçG&7B‚–&VG2¢£ã#p¦Bâ¢¢v–ç7B"Õsw2ãÓÂVÆWfVâ6öÖÖ—G2ÆFW"âF†R#S(	3cÒ&æBÖ÷fVBã“C(i"ã““¢‚³bã2R’v—F‚éDÅÂ¢"ã3b(i""ãB–â7FWÂv†–6‚—2"Ô%Ts2w2Ç†ÖæBÖ÷VRv÷&²&V6†–ær&æ@¥"Ô%Ts2&VF–7FVB—Bv÷VÆBÆVfRVçF÷V6†VB(	B6ÖÆÂÂ&VÂÂæB"ÔÓ"w2FòW‡Æ–âà ¢¢¥F†Rf–æF–ærF†BÖGFW'2Ö÷&RF†âF†R&6VÆ–æS¢vV&W"†2æò6V–Æ–ær2—G2&6¶w&÷VæBvöW0¦F&²ÂæBöæR&æBÇ&VG’FVÖöç7G&FW2—Bâ¢¢Æ¶UöÖ&¶WFÂFW6·F÷Â(	3#SÒ&VG0¢¢¦vV&W"‚ãƒ#6÷fW"w&÷VæBöbÂ¢2ã¢¢Âv†W&RF†R6ÖR&æBöâÖö&–ÆR&VG2ã33’÷fW ¤ÅÂ¢S2ãRâæ÷F†–ær—2w&öærv—F‚F†R&öBF†W&R(	BéDÅÂ¢—2‚ãBRW&6WF–&ÆRâF†R&öBw0§&ö¦V7FVB&ö&W2öâF†Bf–Ww÷'B6–×Ç’ÆæBv–ç7B6öÖWF†–ærÆÖ÷7B&Æ6²ÂæB&F–òv†÷6P¦FVæöÖ–æF÷"—2F†RÆ–v‡B–âF†R&6¶w&÷VæB—2Væ&÷VæFVBv†VâF†R&6¶w&÷VæB†2æöæRâ¢¤ÖVF–à¥vV&W"÷fW"&æB6âF†W&Vf÷&R&R6WB'’—G2F&¶W7B&ö&W2&F†W"F†â'’—G2&öG2â¢¢F†B—0§F†R&V6—6Rf–ÇW&RF†R÷væW"w2'VÆ–ærçF–6—FVB'’—&–ærF†R&F–òv—F‚fÆö÷"–ç7FVBö`§7v–æröæR&"f÷"F†R÷F†W"ÂæB—B—2F†RçVÖ&W"F†R&'2v÷VÆB†fR&VVâf—GFVBv–ç7B†@§F†W’&VVâ6WB–âF†R6ÖR6†ævR2F†R&6VÆ–æRà ¢¢¤æB"ÔÓw2F‡&W6†öÆB6÷W&6RFöW2æ÷BW†—7Bâ¢¢F†R&6VÂ6—2FòFW&—fRF†R&'2'’ÖV7W&–æp¢'v†B6öçG&7B&VÂF—'BG&6²†öÆG2v–ç7B&VÂ&—&–R"–âF†R"Õ$Tc†÷Föw&‚à¢¢¥F†W&R—2æòF—'BG&6²–âF†B†÷Föw&‚â¢¢FööÇ2öÖV7W&U÷&VfW&Væ6Rç–æ÷r7W'fW—2F†RÆæ@§&Vv–öâæB&–çG2—C¢F†Rv–FW7B6öçF–wV÷W2&&RÖV'F‚'Vâç—v†W&R&VÆ÷rF†R†÷&—¦öâ—0¢¢£33"‚Ò‚ã"RöbF†Rg&ÖRv–GF‚ÂB(‰#3‚ã,+¢¢(	BF†R&÷GFöÒVFvRöbF†Rg&ÖRÂBF†P§†÷Föw&†W"w2÷vâfVWBÂæB—B—2G'’7FV×2æBÆ—GFW"&WGvVVâÆçG2&F†W"F†â7W&f6RâF†P§v–FW7B'Vâv—F‚æòw&VVâW†6W72BÆÂ—2ãRB(‰#ãL+Âv†–6‚—2F†R†¦VBG&VVÆ–æRæB—2æ÷@¦w&÷VæBâF†R6ö–ÂÖÆ–¶R¦g&7F–öâ¢—22R÷fW"F†Rv†öÆRÆæB&Vv–öâæB&—6W2Fò‚ãRR–âF†P¦&÷GFöÒ\+Âv†–6‚—2W†7FÇ’v‡’g&7F–öâ6ææ÷BFV6–FRF†—2æB'VâÆVæwF‚6ã¢G&6°¦7&÷76–ærF†Bg&ÖRv÷VÆB&R6öçF–wV÷W27&÷72Æ&vR'Böb—G2v–GF‚B6öÖRVÆWfF–öâÂæ@¦æ÷F†–ær–â—B—2à ¥F†—2—2F†R6V6öæBF–ÖRF†—2&ö¦V7B†2&VVâ†æFVBF&vWBF†B—G2÷vâ&VfW&Væ6R6ææ÷@§7WÇ’âF†Rf—'7B—2&V6÷&FVB&÷fRVæFW"F†R##bÓ‚Ó&—&–R7vVW(	B†÷&—¦öâ×F–Ö&W"'&–V`§7V6–g––ær%vV&W"ã3n(	3ãcr"Âöbv†–6‚5DEU26—2—B¢&FöW2æ÷BW†—7B–âF†R&VfW&Væ6RBç§F‡&W6†öÆB(	BF†BW'&÷"v2F†R'&–Vbw2Âæ÷BF†R'V–ÆFW"w2â"¢æ÷F†–ær"Õ$Tc7GVÆÇ’ÆæFVB—0§vV¶VæVB'’F†—3¢ÆÂf÷W"6·’&VF–æw2ÂF†R†÷&—¦öâ&æBæBF†R6æ÷’6öçG&7B7F–ÆÀ§&W&öGV6RÂæBF†W’&Rv†Bv÷&ÆBæ§6æBG&VW2æ§6V÷FRâ¢¥"ÔÓ"—2F†W&Vf÷&R&Æö6¶VBöâ§F‡&W6†öÆB6÷W&6RÂæ÷BöâVff÷'B¢¢ÂæBF†RF‡&VR†öæW7B÷F–öç2(	B6V6öæB6—FVB†÷Föw&‚F†@¦FöW26†÷rG&6²Â6—FVBV&Æ—6†VBFWFV7F–öâF‡&W6†öÆBÆ&VÆÆVB26Æ–Ò&÷WBW–W2&F†W §F†â&öG2Â÷""ÔÓw2÷vâ&6VÆ–æRg&÷¦VâæBÆ&VÆÆVB&÷f—6–öæÂ(	B&Rw&—GFVâ÷WB–à¦Fö72õ$ôDÔæÖF*r"ÔÓ"f÷"F†R÷væW"Fò6†ö÷6R&WGvVVââFòæ÷B–6²çVÖ&W"æB6ÆÂ—@¦FW&—fVBà ¢22f—†VB##bÓ‚ÓR(	BF†RF÷vâv2––ærG&r6ÆÂW"6öÆ÷W"öb–çBÂæBF†RæW‡B3“’&öög2æ÷r6÷7BæöæP ¢¢¥"ÕsVâ¢¢F†RG&rÖ6ÆÂ'VFvWBv2F†RöæRF†–ær&÷F‚÷fW&æ–v‡BÆæW2vW&Rv—F–æröã¢"Ôs¦ÖV7W&VB¢¢³G&r6ÆÇ2f÷"’æWr&öög2¢¢Â7G&–v‡BÖÆ–æ–ærFò&÷WB¢¢³#Cv–ç7B'VFvWBö`£ƒ¢¢÷fW"F†R3“’&öög27F–ÆÂFò6öÖRÂæB—B†BÇ&VG’&¶VB&Æö6²öb†÷W6W2…BÔ‚Â"33"’à¤—B—2æ÷Bw&÷wF‚&ö&ÆVÒç’Ö÷&Râ—B—2¢§¦W&ò¢¢à ¢¢¥F†R6W6RÂæB—Bv2†–F–ær–âÆ–â6–v‡Bâ¢¢'V–ÆF–æw2æ§66÷'G2F†RF÷vâ–çFòöæP¦&F6†VDÖW6†W"F—7F–æ7BÖFW&–ÂÂæBF†R¶W’–æ6ÇVFVBF†R&6R6öÆ÷W"âWfW'’öæRöbF†RCp¦&F6†W2v2F†R6ÖRÖW6…7FæF&DÖFW&–Æ–âWfW'’&W7V7B&VæFW&W"F—7F–æwV—6†W2(	BÖWFÆæW70£Â¢¦æòÖöbç’¶–æB¢¢ÂF÷V&ÆU6–FVÂ÷VRÂÇ†FW7FÂ6Öö÷F‚×6†FVBâF†RöæÇ’f–VÆG2F†@¦F–ffW&VBvW&R6öÆ÷&Âv—F‚¢£3’F—7F–æ7BfÇVW27&÷72Cr&F6†W2¢¢ÂæB&÷Vv†æW76Âv—F‚bâF†P§F÷vâv27VæF–ærf÷'G’×6WfVâG&r6ÆÇ2Fò&VæFW"GvòçVÖ&W'2ÂæB'W––æræ÷F†W"öæRWfW'’F–ÖR¦&Æö6²ÆæFVB6''––ær–çBæ÷F†–ærVÇ6R–âF÷vâW6VBâ¢¥"Ôsw2"³"v2æWrÖFW&–À¤u$õU2Âæ÷Bö&¦V7G2¢¢(	Bv†–6‚—2&V6—6VÇ’v‡’—Bv2Væ–f÷&ÒB&V&–æw2S+'C¢F†R6÷7@¦6÷VçG2–çG2–âg&ÖRÂæ÷B'V–ÆF–æw2à ¢¢¥F†Rf—‚6'&–W26öÆ÷W"W"fW'FW‚æB—2&—F†ÖWF–6ÆÇ’–FVçF–6ÂÂv†–6‚—2F†RöæÇ’&V6öâ—B—0¦ÆÆ÷vVB†W&Râ¢¢ÖFW&–Âæ6öÆ÷&—2Ç&VG’–âF†R&VæFW&W"w2Æ–æV"v÷&¶–ær76S²F‡&VRw0¦Æ6öÆ÷%ög&vÖVçCæ×VÇF—Æ–W2F–fgW6T6öÆ÷"ç&v&'’F†R6öÆ÷&GG&–'WFRv—F‚æò6öÆ÷W"×76P¦6öçfW'6–öâöb—G2÷vã²æBF†R6öæf–FVæ6Rf–Wrw2F–çBv2Ç&VG’Æ–VB¦gFW"¢F†B6‡Væ²â6ð§F†R6†FW"FöW2F†R6ÖR&öGV7B–âF–ffW&VçB÷&FW"ÂæBFö7VÖVçFVBv†—FRvÆÂ7F–ÆÂ&VæFW'2@§F†RfÇVR—G2&V6÷&B6Æ–×2ÂFòF†R&—Bâ&÷Vv†æW72—2FF—F–öæÆÇ’6ö×&VBBF‡&VRFV6–ÖÇ2À§v†–6‚ÖW&vW2F†R&W7ö¶RÖ7FW'2rfÆöC3"ãƒ““““““scSƒC#v—F‚F†RvVæW&FVB–æf–ÆÂw2ã–à ¢¢¦FööÇ2ö7&—F–5÷6†÷G2æÖ§6Â6÷W&6RG&VRÂ&÷F‚f–Ww÷'G2Â&Vf÷&RæBgFW"öâF†R6ÖRFWf¢¢  §ÂG&r6ÆÇ2Â6Vvæ6†Â2væ6…÷v–ævÂÆ¶UöÖ&¶WFÂe÷÷7Eööff–6VÂf÷&·6Âw&VVå÷G&VVÂ6÷WF…÷vFW&Âg&öÕö&÷fVÂ&—&–U÷6÷WF†Â&—&–U÷vW7FÂ&—fW%ö&æ¶À§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§ÂFW6·F÷&Vf÷&RÂsRÂs‚Â“ÂcbÂ“‚Â2Â“bÂs"Â“RÂ¢£’¢¢ÂSbÀ§ÂFW6·F÷gFW"ÂSbÂS‚ÂcÂSrÂc‚ÂsÂcbÂS’Âc"Â¢£sR¢¢ÂS"À§ÂÖö&–ÆR&Vf÷&RÂs"ÂsBÂs‚ÂcÂƒ"Â“’Â“BÂs"Â“2Â¢£b¢¢ÂC’À§ÂÖö&–ÆRgFW"ÂSBÂSRÂS‚ÂSÂcBÂc‚ÂcBÂS’ÂcÂ¢£s2¢¢ÂCrÀ ¢¢¤&F6†W2Cr(i"c²7FF–öâ×f–Ww÷'G2÷fW"F†R(šBƒ'VFvWBöb#"(i"öb#"â¢¢æWr&ööböbç¦6öÆ÷W"æ÷r¦ö–ç2âW†—7F–ær&F6‚Â6òBÔ‚æBF†R3“’&öög2&V†–æB—B6÷7Bæ÷F†–ærà ¢¢¥v†B—B6÷7BÂ7FFVB–âçVÖ&W'2&F†W"F†â&V77W&æ6Râ¢¢G&–ævÆW2&R¢¦–FVçF–6ÂFòF†P§G&–ævÆRBÆÂ#"7FF–öâ×f–Ww÷'G2¢¢(	Bæ÷F†–ærv2G&÷VBFò'W’F†R6ÆÇ2âF†Rg&ÖW2&R¦æ÷B ¦'—FRÖ–FVçF–6Ã¢"öb#"†6‚F†R6ÖRÂæBF†R&W7BF–ffW"öâ¢£ã2Röb—†VÇ2¢¢Â–â~(	3“P§66GFW&VB6ö×öæVçG2v†÷6RÆ&vW7B—2Sb‚ÂÆÂöâ'V–ÆF–ær6–Æ†÷VWGFW2(	BFWF‚F–W2B6ö–æ6–FVç@§7W&f6W2&W6öÇf–ærF†R÷F†W"v’VæFW"6†ævVBG&r÷&FW"âv÷'7B6–ævÆR—†VÂ“2ó#SS°¢¢§v†öÆRÖg&ÖRÖVâÌéGÂã>(	3ãRöböæR‚Ö&—B6÷VçB¢¢âæò7W&f6Rç—v†W&R—2&W–çFVBà ¢¢¥v†B—BFöW2æ÷BFòâ¢¢—BFöW2æ÷BF÷V6‚F†RvFW"7W&f6RÂ÷7B×&ö6W76–ær÷"G–æÖ–2&W6öÇWF–öà¢…"ÕsV"Â7F–ÆÂ÷VâÂ7F–ÆÂ6''––ær"Ô%Tsw2&—fW"fÆ–6¶W"’ÂæB—BÆVfW2b&F6†W2v†W&R—0§&V6†&ÆR(	BF†R&÷Vv†æW72†ÆbæVVG26†FW"F6‚æB—2w&—GFVâW2¢¥"ÕsV"¢¢v—F‚—G0¦çVÖ&W'2Ç&VG’ÖV7W&VBâF†R'VFvWB—2ÖWBv—F‚R6ÆÇ2öb†VG&ööÒBF†Rv÷'7B7FF–öâæBF†P¦w&÷wF‚FW&Ò—2¦W&òÂ6òF†B†Æb'W—2Ö&v–âÂæ÷Bf—‚à ¢22f—†VB##bÓ‚ÓR(	BF†R&öBB–÷W"fVWBÂF†RGvò7FF–öç2F†BæWfW"7FööBöâöæRÂæBvFRF†B'7F–æVBW†7FÇ’v†Vâ—B6†÷VÆB†fR6†÷WFV@ ¢¢¥"Ô%Ts2Â÷væW"×&W÷'FVBöâÖö&–ÆRÂöâF†RFWb&Wf–Wrv—F‚"Ô%Ts"w2f—‚Ç&VG’–ã¢¢¢7FæF–æröà¤g&æ¶Æ–â7G&VWB&ö6†–ær&æFöÇ‚ÂF†Rv†VVÂ'WG2&VB–âF†RÖ–BÖF—7Fæ6RæB¢&—B6†÷VÆBæ÷@¦&R–çf—6–&ÆRv†Vâ’Ò7FæF–æröâ—Bâ"¢G'VRâF†RæV"&æBæ÷r66÷&W2¢£2ãÅÂ¢v—F‚ƒRö`§&ö&W2W&6WF–&ÆR¢¢öâÖö&–ÆRæB2ã"òcRöâFW6·F÷Âv–ç7B¢£ãRò3R¢¢&Vf÷&RÂÖV7W&V@¦öâF†RV&Æ—6†VBÖ—'&÷"âWfW'’&æB7BCÒ—2VçF÷V6†VB'’F†RæV"Öf–VÆBf—‚à ¢¢¥F†R&6VÂw2f—'7BÖ÷fRÖV7W&VBæ÷F†–ærÂæBF†B—2F†Rf–æF–ærâ¢¢—B6–C¢FB³"ÂCÖ ¦&æBÂW‡V7B—BFòf–ÂÂæBF†Bf–ÇW&R—2F†R66WFæ6RâFFVBÂæBF†R&æB6öÆÆV7FVB¢¦öæP§&ö&R¢¢B6÷WF…÷vFW&æB¢¦æöæR¢¢Bg&öÕö&÷fV(	B&V6W6R¢¦æV—F†W"vFVB7FF–öâ7FæG2öà¦&öB¢¢â6÷WF…÷vFW&—2¢£Òg&öÒF†R6VçG&VÆ–æR—B—2æÖVBgFW"¢¢‡F†B—2BÕc"Âæ÷p¦ÖV7W&VB&F†W"F†â7W7V7FVB’æBrÒg&öÒF†RæV&W7BöæS²g&öÕö&÷fV—2sRÒWâF†Rv–æF÷p§v2w&öær–âGvòF–ÖVç6–öç2ÂF—7Fæ6RæB÷6RÂæBF†Rf–Æ–ærvFR6÷VÆBöæÇ’6†÷röæRöbF†VÒà¥F†W&R—2æ÷rF†—&B7FF–öã¢Æ¶UöÖ&¶WFÂ&V6†VBF†Rv’f—6—F÷"&V6†W2—B(	B'’6Æ–6¶–ær§fW&–f–VB7G&VWBÖ6öçG&öÂ–çFW'6V7F–öâ–âF†RvòFòF"(	Bv†–6‚F†VâGW&ç2FòÆöö²ÆöærF†P¦6VçG&VÆ–æRVæFW&fö÷BÂ&V&–ær&VBöfbF†R6öÖÖ—GFVBF‚âF†R'&—fÂ÷6RÆöæRv2æ÷BVæ÷Vv€¦V—F†W#¢F†R6†—VB§V×f6W2f—†VB&V&–ærÂv†–6‚B7&÷76–ærö–çG2F–vöæÆÇ’–çFòF†P¦&Æö6²æBWB¢§¦W&ò¢¢&öB&ö&W2–ç6–FRÒà ¢¢¥F†R&–ÖR7W7V7B—2&VgWFVBÂæBæòw&72v26ÆV&VBâ¢¢F†R&6VÂæÖVBæV"Öf–VÆB7v&@¦ö66ÇW6–öâ2Ö÷7BÆ–¶VÇ’Âv—F‚âW‡Æ–6—BæöâÖÆ–6Væ6Rv–ç7Bv–FVæ–ær6ÆV&–ær6÷'&–F÷"Fòv–à¦66÷&RâF†R†&æW72æ÷r&R×6†ö÷G2—G2&öBÖ&¶W'2v—F‚F†R7v&BæBF†RG&VW2†–FFVâÂ6òà¦ö66ÇVFVB&ö&R—2F—7F–æwV—6†&ÆRg&öÒâ'6VçBöæR(	BæB–âF†RæV"&æB¢¦ÆÂFVâ&ö&W2&P¦Ö&¶VBV—F†W"v’¢¢âæ÷F†–ær—2†–F–ærF†R&öBâfÆ÷&æ§6—2VçF÷V6†VBÂæò&V6÷&FVBw&÷VæB6÷fW ¦Ö÷fVBÂæBF†RæöâÖÆ–6Væ6RæWfW"†BFò&RFW7FVBâWfW'’&æBæ÷r&W÷'G2F†RF—67&–Ö–æF–öà¢†6VVââöbÒ&ö¦V7FVBÂ²6ÆV"öbfÆ÷&’Â&V6W6RFVÆÆ–ærö66ÇW6–öâg&öÒfÆFæW72—2F†P¦F—7F–æ7F–öâF‡&VRvFW2–â&÷rf–ÆVBFòG&rà ¢¢¥F†RfVÇBÂ7FFVBÖ÷&R&V6—6VÇ’F†â'F†RÇ†—2FöòÆ÷r"â¢¢âÇ††W&R—2¢¦6÷fW&vP¦g&7F–öâ¢¢(	Bv†B6†&RöbF†Rw&÷VæB—2&&RV'F‚&F†W"F†âw&72(	BæBF†B—2F†R&–v‡@§–7GW&RöbÖ—‡GW&RöæÇ’v†W&RöæR—†VÂ7ç2Öç’F6†W2öb—BâBvÆ¶W"w2fVWBöæR—†VÀ§7ç2öæRF6‚Âv†–6‚–âÆ–fR—2V—F†W"V'F‚÷"w&72ÂæBF†R&ÆVæB–çG2Væ–f÷&Òv6‚ö`¦w&72×v—F‚ÖÖ†–çBÖöbÖF—'B–ç7FVBâF†R†&æW72ÖV7W&W2&÷F‚VæG2öb—C¢F†R6ÖRæV"&ö&W2v—F€§F†R&–&&öâf÷&6VB¢¦gVÆÇ’÷VR¢¢66÷&R¢£2ãBÅÂ¢¢¢Â6òF†R6öçG&7Bv26—GF–ær–âF†R&–&&öâw0¦÷vâ6öÆ÷W"æBF†R6†—VBÇ†v27VæF–ærVæFW"†Æböb—BâF†RæV"f–VÆBÇ6ò†2ÆW72Fò7VæB(	BF†P¦w&÷VæBVæFW&fö÷B—2vVçV–æVÇ’F&¶W"F†âB&ævRÂ¢¤ÅÂ¢Sãv–ç7BS"ã~(	3Sbã2¢¢âF†Rf—‚66ÆW0¦Ç†'’"ãB–ç6–FRRÒÂfF–ærFòæ÷F†–ær'’CÒâ&V6÷&FVB2¢¤Ã“‚¢¢à ¢¢¥F†RGW&&ÆR†Æb—2F†RvF–ær'VÆRâ¢¢&æBvFVBöâ¦†÷rÖç’&ö&W2vW&R4TTâ¢vFW2—G6VÆ`¦÷WBB&V6—6VÇ’F†RÖöÖVçBF†RF†–ær—BÖV7W&W2vöW2w&öæs¢&öBæö&öG’6â6VR&W÷'G2ãÓÀ§v†–6‚—2–æF—7F–æwV—6†&ÆRg&öÒ7G&WF6‚v—F‚æò&öB–â—BÂæBF†R6†V6²76W2'’'7FVçF–öâà¤&æG2&Ræ÷rvFVBöâ†÷rÖç’&ö&W2vW&R¢¥$ô¤T5DTB¢¢(	Böâ67&VVâÂæBF†W&Vf÷&R÷vVB§–7GW&RâF†—2—2F†RF†—&BF–ÖRF†—2öæR'Vr†2&VVâVW7F–öâöbv†BF†RvFRv2ö–çFVBBÀ¦æBF†Rf—'7Bf—‚F†BÖ¶W2F†RvFRf–ÂÆ÷VFÇ’&F†W"F†âV–WFÇ’FV6Æ–æRFòç7vW"à ¢¢¤6V6öæBfVÇBÂf÷VæB'’F†RæWr7FF–öâæBf—†VBv—F‚—Bâ¢¢BFW6·F÷Â(	3#SÒg&öÒF†P¦7&÷76–ærÂF†R&–&&öâ66÷&VB¢£ãÅÂ¢¢¢v†–ÆRF†RÖ&¶W"72v2g&öçFÖ÷7B(	B"Ô%Ts"w2fVÇB¦v–âÂ—G2öÇ–vöâöfg6WB†f–ær&VVâGVæVBVçF–ÂF†R&æG2¦BF†RGvò7FF–öç2F†VâvFVB §76VBâFVWVæVBFòF†RÖ&¶W"72w2÷vâfÇVW2ÂF†B&æB&VG2¢£‚ãÅÂ¢BP§W&6WF–&ÆR¢¢âæBF†R÷VRF–væ÷7F–2†BFò&Rf—†VB&Vf÷&R—B6÷VÆB&R&VÆ–WfVC¢—G2f—'7@¦f÷&ÒÆWBF†RFW'&–â–çB&6²÷fW"F†R&–&&öâæB&W÷'FVBã6V–Æ–ærVæFW"†VÇF‡’&öBà¤—Bw&—FW2FWF‚æ÷rÂ2F†RÖ&¶W"72Çv—2F–BâF–væ÷7F–2F†BÆ–W2V–WFÇ’—2v÷'6RF†à¦æòF–væ÷7F–2ÂæBF†—2öæRÆ–VB–âF†RF—&V7F–öâöb¦æ÷F†–ærFò6VR†W&R¢(	BF†R6ÖRF—&V7F–öâ0¦WfW'’÷F†W"–ç7G'VÖVçB–âF†—2'Vrw2†—7F÷'’à ¢¢¥v†B—2æ÷Bf—†VBâ¢¢F†RæV"&æB†2F†RÆV7B†VG&ööÒöbç’&æBvÆ¶W"7GVÆÇ’7FæG0¦–ã¢—G26V–Æ–ærgVÆÇ’÷VR—2¢£2ãBÅÂ¢öâÖö&–ÆRæBBã2öâFW6·F÷¢¢Âv–ç7BRãž(	3bã’BF†P§6ÖR7FF–öâw2C(	3ÒæBB&÷F‚W&–Â&æG2(	BæB¢£#RöbæV"&ö&W2öâÖö&–ÆRÂCRöà¦FW6·F÷Â6ææ÷B6ÆV"F†RW&6WF–&–Æ—G’F‡&W6†öÆBWfVâBgVÆÂ÷6—G’¢¢â„æ÷B'F†RÆ÷vW7Böbç¦&æB"Âv†–6‚âV&Æ–W"G&gBöbF†—26–C¢BF†B7FF–öâF†Rc(	3CÒ&æB—2Æ÷vW"7F–ÆÂÂæ@§F†B—2&öBB¶–ÆöÖWG&R&F†W"F†âöæRVæFW&fö÷Bâ’÷6—G’†2æV&Ç’'Vâ÷WB2à¦–ç7G'VÖVçB†W&RâÃ“‚æÖW2F†R†öæW7@§7V66W76÷#¢FW‡GW&VB6÷fW&vRÂV'F‚æBw&72&W6öÇfVB2F6†W2BF†R66ÆRæV"—†VÂ6à§6†÷rÂ6òF†RW–R–çFVw&FW2F†R&V6÷&FVBg&7F–öâ&F†W"F†âF†R&ÆVæFW"&RÖÖ—†–ær—BâF†@¦&VÆöæw2Fò¢¥"Õs"¢¢Âv†W&RF†RãBFW‡GW&R66÷&RÇ&VG’Æ—fW2à¢22æWr##bÓ‚ÓR(	B&VgW6Âæö&öG’6÷VÆBFVÆÂ'Bg&öÒâVæç7vW&VBVW7F–öà ¢¢¤³#â¢¢'VÆRböbF†R†÷W6V†öÆB&öw&ÖÖRÆWG2&Æö6²&ööb&RF÷FVB'’â&wVVB†÷W6V†öÆ@¦öæÇ’–bF‡&VRFW7G272ÂæBF†R6V6öæB6·2v†WF†W"F†R&ööbw2fÖ–Ç’—2öæRF†—2Æ–W"Ç&VG¦†÷W6W2F†BG&FR–ââ¢¤f÷"f÷W"G&FW2F†BVW7F–öâ†Bæòç7vW"BÆÂâ¢¢'&–6¶Ö¶W&À¦6¶W&Â6w–W&æBv†VVÇw&–v‡FÆ—fRW†6ÇW6—fVÇ’öâF†R3&öög2F†—2Æ–W"§&—6W2¢&F†W §F†âF÷G2ÂæBF†÷6R&V6÷&G2æÖVBæòfÖ–Ç’–âç’f–VÆBvFR6÷VÆB&VB(	BV–v‡BgW'F†W §G&FW2vW&R'FÇ’–âF†R6ÖR÷6—F–öâÂr†÷W6V†öÆG2–âF÷FÂâBÔR&VgW6VBF†R6w–W"F÷F–öà¦öâF†B6–ÆVæ6RæB6–BBF†RF–ÖRF†B—B6÷VÆBæ÷BFVÆÂF†R&VgW6Âg&öÒâVæç7vW&V@§VW7F–öâà ¢¢¥F†Rç7vW"v2G&ç67&—F–öâÂæ÷BFV6—6–öââ¢¢WfW'’öæRöbF†R3'V–ÆF–æw2v2FVÇB¦7&÷77vÆ²fÖ–Ç’'’F†R&öw&ÖÖRÂæBWfW'’öæR†2Çv—2§6–B¢6ò–â&÷6R(	BF†Rfö÷G&–çBæ÷FP§&VG2&b‚#"gB&V7FævÆRg&öÒF†R¢¤C2¢¢fÖ–Ç’&æB"ÂæBV6‚f÷&ÒfÇVR6—FW2F†R6ÖP¦&æBâF†R&æBv26öÖÖ—GFVB–âGvòÆ6W2æB&VF&ÆR–âæV—F†W"âw&—F–ær—B–çFð¦&V6öç7G'V7F–öâæfÖ–Ç–F†W&Vf÷&R¢¦–çfVçG2æ÷F†–æræB÷vW2Fö72ôÄ”$U%D”U2æÖFæ÷F†–ær¢£²'VÆR`¦v–ç2æòf÷W'F‚6ÆW6RÂæBæòG&FR—2w&çFVB72(	BG&FRv†÷6RfÖ–Æ–W2&R&VF&ÆR6à§7F–ÆÂf–ÂF†RFW7Bà §ÂÂ&Vf÷&RÂgFW"À§ÂÒÒ×ÂÒÒÓ§ÂÒÒÓ§À§Â6Vç7W2G&FW2&W6öÇf–ær'VÆRbw2fÖ–Ç’FW7BÂ#Röb#’Âf÷W"öbF†VÒæ÷BBÆÂÂ¢£#’öb#’¢¢À§ÂG&FRÖfÖ–Ç’—'2F†RFW7B6â6ö×&Rv–ç7BÂ(	BÂ¢£CB¢¢À§Â†÷W6V†öÆG27FæF–æröâ&ööbF†BæÖW2æòfÖ–Ç’ÂrÂ¢£¢¢À ¢¢¥F†RGW&&ÆR†Æb—2F†RvFRâ¢¢FööÇ2övVæW&FUö–æfW'&VEö†÷W6V†öÆG2ç–f–Ç2–bç’&ööb¦†÷W6V†öÆB¦Æ—fW2÷"v÷&·2–â¢æÖW2æòfÖ–Ç’–âF†R7&÷77vÆ²(	B÷fW"&÷F‚Æ–æ·2Â&V6W6R6†÷w0¦fÖ–Ç’—22×V6‚6Æ–Ò&÷WBF†RF÷vâ26÷GFvRw2âF†RFW7B6ææ÷Bvò6–ÆVçBv–âv—F†÷WB¦vFR6––ær6òà ¢¢¥F†R&6VÂw2÷vâ7W7–6–öâv2&VgWFVBâ¢¢—BfÆvvVB–æe÷6w–W%öGvVÆÆ–æuö&Ö76–ær2à¦÷WF'V–ÆF–ævv†–ÆRöÖ76W22g&ÖUöGvVÆÆ–ævâF†W’F–ffW"&V6W6R¢§F†W’vW&RFVÇ@¦F–ffW&VçBfÖ–Æ–W2¢¢ÂC2æBC"ÂæBV6‚&W6öÇfW2F‡&÷Vv‚—G2÷vâfÖ–Ç’w26öÖÖ—GFVB&6†WG—R(	@§F†R&V6÷&Bw2W†—7FVæ6Ræ÷FR6—26ò–â2Öç’v÷&G2âF†R&VÂ7Æ—B—2f—fRsB6†÷2Ö76VBGvð§v—2ÂÆÂöbF†VÒöæR×7F÷&W’Âv†–6‚sBw2÷vâÆ–6Væ6RFöW2æ÷BW‡Æ–âà ¢¢¤æBVæFW&æVF‚F†BÂF†Rf–æF–ærv÷'F‚Ö÷&RF†âF†R&6VÂâ¢¢&VF–ærV6‚6öÖÖ—GFVBf÷&ÒfÇVP¦v–ç7B—G2fÖ–Ç’w2&æB6†÷w2¢£SBöb“2&V6öç7G'V7FVB&öög26—B÷WG6–FRF†R&æBF†V—"÷vâæ÷FP¦6—FW2¢¢(	B3’öbc"æöç–Ö÷W2ÂRöb3&W7ö¶RÂv÷'7B–æeöÆVæG'•öæ÷'F†B#ƒ7gBv–ç7Bà¤R&æBöbCŽ(	3“"âF†R6W6R—2F†BF†Rf÷&ÒvVæW&F÷'26†ö÷6RfÇVW2'’¢¦&6†WG—R¢¢æBGF6€¦æ÷FR6—F–ærF†R¢¦fÖ–Ç’¢¢âæ÷FRF†B6—FW2&æB—2F†RFVfVæ6Rf÷"F†R–çfVçF–öã²v†W&RF†P§fÇVR—2÷WG6–FR—BF†Ræ÷FR—2w&öær&÷WB—G2÷vâ6÷W&6RâF†B—2¢¤³#R¢¢Â7Æ—B6òF†P¦ÖV7W&VÖVçBÆæG2&Vf÷&Rç—F†–ærÖ÷fW2à ¢¢¥GvòvFW26Vv‡Bv†B&VF–ærv÷VÆBæ÷B†fRâ¢¢&V6öæ6–ÆUóccRç–6Æ76–f–VB&öög2'’v†WF†W"§&V6öç7G'V7F–öâ&Æö6²v2§&W6VçB¢Â6òÆÂ36–ÆVçFÇ’Ö÷fVBg&öÒ–æfW'&VEö†÷W6V†öÆE÷&öw&ÖÖVFð¦vVæW&FVF(	BF÷FÇ2Væ6†ævVBÂGG&–'WF–öâw&öærâæB6ö×–ÆU÷66VæRç–6VçBWfW'§&V6öç7G'V7F–öâÖ&Æö6²&V6÷&BFòF†Ræöç–Ö÷W2Ö–æf–ÆÂF÷76–W#²F†R†÷W6V†öÆBÆ–W"†2—G2÷vâæBæ÷p§ö–çG2B—Bâv†–6‚7W&f6VB¢¤³#b¢£¢V&Æ—6‚ç6†FVÆ–&W&FVÇ’¶VW2Fö72ö÷WBöbF†R–ÆöBÂ6ð¦öâF†RFWÆ÷–VB6—FR¢¦ÆÂ#sb'V–ÆF–ær6&G2Æ–æ²FòCB¢¢à ¢22æWr##bÓ‚ÓR(	BF†R†÷Föw&‚F†R6·’—26Æ–'&FVBv–ç7B—2æ÷r–âF†R&W÷6—F÷'’ÂæB—B6†V6·2÷W@ ¢¢¥"Õ$Tcâ¢¢&VæFW&W'2÷vV"ö§2÷v÷&ÆBæ§6FW&—fW2—G26·’W‡÷7W&RÂF†Rv†öÆRöb—G0¦†÷&—¦öâ×&W7F÷&Rf—BæBF†R6öÆ÷W"F—7Fæ6R6öçfW&vW2öâg&öÒ&VF–æw2F¶VâöfböæP§†÷Föw&‚ÂV÷FVB–âF†R6öÖÖVçG22&"öGWvU÷FÆÆw&75ó#‚ÓrÓ#Bæ§vâ¢¥F†Bf–ÆRv0¦–âæò6†V6¶÷WBâ¢¢v—BÇ2Öf–ÆW6&WGW&æVBæ÷F†–ærf÷"—Böâ##bÓ‚ÓBÂv†–6‚ÖFRWfW'’6·¦çVÖ&W"–âF†R&VæFW&W"V÷FF–öâF†B6÷VÆB&R&VBæBæ÷B6†V6¶VB(	BæB—Bv2&Æö6¶–æp§Gvò&6VÇ2Â"Õs‡v†÷6RF&vWG2*sR6·2Fò&R&RÖæ6†÷&VB'’ÖV7W&–ær&VfW&Væ6RF‡&÷Vv€§F†—26öFR’æB"ÔÓ‡v†÷6R&öBÖ6öçG&7BF‡&W6†öÆG2&R7W÷6VBFò&RFW&—fVBg&öÒv†B§&VÂF—'BG&6²†öÆG2v–ç7B&VÂ&—&–RÂ&F†W"F†â–6¶VBFòf—BFöF’w2'V–ÆB’à ¢¢¤—B—26öÖÖ—GFVBÂæB—B—2F†R&–v‡Bf–ÆRâ¢¢676’6&’Â¥&W7F÷&VBFÆÆw&72&—&–R–à¤GUvR6÷VçG’Â–ÆÆ–æö—2¢Â#B§VÇ’#‚Âv–¶–ÖVF–6öÖÖöç2Â@¦FF÷6÷W&6W2ö76WG2÷6&•ó#…öGWvU÷FÆÆw&72öGWvU÷FÆÆw&75ó#‚ÓrÓ#Bæ§vv—F‚6÷W&6P§&V6÷&B6&•ó#…öGWvU÷FÆÆw&76â–FVçF–f–6F–öâF–Bæ÷B&W7BöâF†Rf–ÆVæÖS¢F†P¤6öÖÖöç2FW67&—F–öâ—2¢%&—&–RÆçF–æröâf÷&ÖW"w&–7VÇGW&Âf–VÆB–âGUvR6÷VçG’"¢(	@§F†R6ÖR&W7F÷&F–öâÖæ÷B×&VÖæçBf–æF–ærF†R##bÓ‚Ó7vVWÖFR&÷WBF†—2†÷Föw&‚(	@¦æBF†Rf–ÆRw2÷vâU„”b6—26×7Vær4ÒÔs“3bÂ¢£#‚ÓrÓ#B“£3#£#R¢¢Â#bÖÒWV—fÆVçBÀ¦÷&–VçFF–öâW&–v‡Bà ¢¢¥F†R&ööb—2F†BF†RçVÖ&W'26öÖR&6²÷WBöb—Bâ¢¢—F†öã2FööÇ2öÖV7W&U÷&VfW&Væ6Rç–À¦æWrv—F‚F†—2&6VÂÂ&RÖÖV7W&W2F†R&VF–æw2v÷&ÆBæ§6V÷FW3  §Â&VF–ærÂV÷FVB–âv÷&ÆBæ§6Â&RÖÖV7W&VB##bÓ‚ÓRÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â"‚&÷fRF†R6·’öÆæB7FW‡F†R„õ$•¤ôåõ$U5Dõ$Vf—BF&vWBæBF†R†¦R6öÆ÷W"’Âƒ3bÃc2Ã“"’Â¢¢ƒ3rÃc"Ãƒr’¢¢À§Â6·’BãBãL+&÷fRF†R†÷&—¦öâÂƒÃS2Ã#’’Â¢¢ƒ“rÃSÃ#‚’¢¢À§Â6·’BŒ+Âƒ#RÃcRÃ#R’Â¢¢ƒ’Ãc2Ã#b’¢¢À§Â6·’BL+Âƒ3rÃcbÃ#’Â¢¢ƒ32ÃcbÃ#’¢¢À ¤æ÷F†–ær–âF†R&VæFW&W"v2F÷V6†VBFòÖ¶RF†W6Rw&VRÂæBF†R&W6–GVÂ(	BfWrVæ—G2–à§&VBæB&ÇVR(	B—2F†RöæRF†R6öFR&VF–7G3¢F†RFööÂfW&vW2F†RgVÆÂg&ÖRv–GF‚ÂF†P¦÷&–v–æÂ&VF–æw2vW&RF¶VâBF†R6†÷Bw2÷vâf–Wr¦–×WF‚ÂæBv÷&ÆBæ§6&V6÷&G2F†BF†P¦ÖöFVÂw2†÷&—¦öâ¦'&–v‡FæW72¢—2¦–×WF‚ÖFWVæFVçBWfVâv†W&R—G2‡VR—2æ÷Bà ¢¢¤6V6öæB6öæf—&ÖF–öâ'&—fVBVæ6¶VBâ¢¢F†R#bÖÒWV—fÆVçBv—fW2Srã‚öFVrfW'F–6ÆÇ¦æBF†R6·’öÆæB7FW6—G2B&÷rƒ#öb3#BÂv†–6‚WG2F†R6ÖW&—F6‚B¢®(‰#"ã+¢¢âF†P£##bÓ‚Ó&—&–R7vVW†BÇ&VG’W7F&Æ—6†VBÂg&öÒâVçF—&VÇ’F–ffW&VçBF—&V7F–öâÂF†@¢'F†R&VfW&Væ6R†÷Föw&†W"†BF–ÇFVBF÷vâã,+"(	B6÷'&V7F–öâF†B–çfÆ–FFVBGvò&÷VæG0¦öbGVæ–ærBF†RF–ÖRâGvòFW&—fF–öç2öbF†R6ÖRçVÖ&W"F†BæWfW"6rV6‚÷F†W"âF†P§W6VgVÂf÷&Òöb—B—2F†BF†Rg&ÖR—2æ÷r¢§6öÇfVB¢£¢VÆWfF–öâ‡&÷r’Òƒƒ#(‰"&÷r’òSrã ¦FVw&VW2Â&V6†–ærBãL+&÷fRF†R†÷&—¦öâæB3‚ã|+&VÆ÷râç’&VF–ærF¶Vâg&öÒF†—0§†÷Föw&‚6âæ÷r7FFRF†RVÆWfF–öâ—Bv2F¶VâBÂv†–6‚—2v†B&÷F‚öbF†—2&ö¦V7Bw0§&VfW&Væ6RF—6w&VVÖVçG2GW&æVB÷WBFò&R&÷WBà ¢¢¥F†R&–v‡G2&R&V6÷&FVB&F†W"F†â77VÖVBÂæBF†W’&Ræ÷BW&Ö—76—fRâ¢¢42%’Õ4BãÀ¦GG&–'WF–öâ&WV—&VBâF†Rf–ÆR—26öÖÖ—GFVB¢¦'—FRÖf÷"Ö'—FRVæÖöF–f–VB¢¢(	B4„Ó¦Fcs†Sss“#F3S3cFCs†cv6#fC3““&VÂ6†V6¶VBv–ç7BF†R4„ÓF†R6öÖÖöç2’&W÷'G0¦f÷"F†Rf–ÆRvR(	B6òv†BF†—2&W÷6—F÷'’&VF—7G&–'WFW2—2F†RÆ–6Vç6VBv÷&²æBæ÷Bà¦FFF–öâÂæB6†&TÆ–¶R—2æ÷BG&–vvW&VB'’—G2&W6Væ6Râ¢¤FW&—f–ærg&öÒ—Bv÷VÆBG&–vvW ¦—B¢£¢7&÷Â&W6×ÆRÂFW‡GW&R÷"ÅUB—2âFFF–öâF†B42%’Õ4Bã&WV—&W2&P§&VÆV6VBVæFW"42%’Õ4BãâF†R&ö¦V7BFW&—fW2æ÷F†–ærg&öÒ—B†—B—2ÖV7W&VBÂæWfW §6×ÆVB’ÂFööÇ2÷V&Æ—6‚ç6†FöW2æ÷B6÷’FF÷6÷W&6W2öÂæB76WG2ôÄ”4Tå4U2æÖFæ÷p¦6'&–W2F†R6ÆV&æ6R2âW‡Æ–6—BÂ&V6öæVBW†6WF–öâFò—G243ô42Ô%’ÖöæÇ’FVfVÇBà ¢¢¤öæRf–wW&RF–Bæ÷B&W&öGV6RÂæB—2ÆVgB7FæF–ær2VW7F–öâ&F†W"F†â6Æ÷6VBâ¢ ¦v÷&ÆBæ§6v—fW2F†R&"w2Ö÷7BF—7FçBÆæB2ƒ‚ÃCbÃCR“²F†R"‚–ÖÖVF–FVÇ’&VÆ÷rF†P§7FWÖV7W&RƒbÃ3ÃC’Â&V6W6Ræ—fR&æBöâF†B&÷rÆæG2'FÇ’öâF†Rf"G&VVÆ–æP§&F†W"F†âöâ÷Vâ7v&BâF†R÷&–v–æÂ&VF–ær7FFW2æò&V6—RÂ6òF†—2—2&V6—P¦Ö—6ÖF6‚Âæ÷B6öçG&F–7F–öâ(	Bv†öWfW"æVVG2F†BçVÖ&W"æW‡B6†÷VÆBFVf–æRv†W&R—B6öÖW0¦g&öÒ&Vf÷&RV÷F–ær—Bà ¢¢¥v†BF†—2&6VÂF–BäõBFó¢¢¢6†ævR6–ævÆR&VæFW&VB—†VÂâæò&VæFW&W"f–ÆRv2F÷V6†VBÀ¦æòF‡&W6†öÆBÖ÷fVBÂæòF&vWB&RÖæ6†÷&VBâ"ÕsæB"ÔÓ÷vâF†÷6RÂæB&÷F‚&Ræ÷rVæ&Æö6¶VBà ¢22æWr##bÓ‚ÓR(	BÆ÷Bv26ÆÆVBg&VR&V6W6R'V–ÆF–ærw26VçG&ö–Bv2–âF†R&ö@ ¢¢¥BÔrâ¢¢BÔb†&VÆ÷r’ÖFR&Æö6²w2&ööÒgVæ7F–öâöb—G2g&VRÆ÷G2âF†—2—2&÷WB†÷rÆ÷@§v2¶æ÷vâFò&Rg&VS¢¦æò6öÖÖ—GFVBfö÷G&–çB†2—G26VçG&ö–B–ç6–FR—B¢âF†R6VçG&ö–B—2§&÷‡’f÷"F†R'V–ÆF–ærÂæB—Bf–Ç2öâW†7FÇ’F†R&V6÷&G2F†RÆBw&–Bv2'V–ÇBFò6÷'&V7B(	@¦'V–ÆF–ærÆ6VBg&öÒG—VB6ö÷&F–æFW2&Vf÷&RF†RÆBÖöGVÆRW†—7FVB6â7FæBÖWG&R÷"Gvð§&÷VBöb—G2÷vâ7G&VWBg&öçFvRÂv†–6‚WG2—G26VçG&ö–B–âF†R$ôEt’æBF†W&Vf÷&R–âæòÆ÷@¦öbç’&Æö6²â¢¤f÷W'FVVâ6öÖÖ—GFVB&V6÷&G2vW&R–âF†B÷6—F–öââ¢¢ÖV7W&VBBFWd“c†S3ƒ–  §ÂF†R'V–ÆF–ærÂ&Æö6²ÂÆ÷BÂöb—G6VÆböâF†BÆ÷BÂ–âF†R'V–ÆF&ÆR'BÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â¢¥FV×ÆR'V–ÆF–ær¢¢Â&Æµ÷6÷WF…÷vFW%ög&æ¶Æ–æÂÂ‚ãbÜ+"Â#rRÂBã"Ü+"À§Â¢¤†&ÖöâbÆööÖ—2w27F÷&R¢¢Â&Æµ÷6÷WF…÷vFW%ö6Æ&¶ÂÂ#’ã"Ü+"Â3RÂ’ãRÜ+"À§Â¢¤6†–6vòFVÖö7&Böff–6R¢¢Â&Æµ÷6÷WF…÷vFW%öÆ6ÆÆVÂbÂ3ã"Ü+"Â3BRÂãBÜ+"À§Â¢¤6öö²6÷VçG’6÷W'F†÷W6R¢¢Â&Æµ÷&æFöÇ…öÆ6ÆÆVÂbÂRãÜ+"Â2RÂãBÜ+"À§Â&V6öåóƒ3U÷6÷WF…öCUó3FÂ&ÆµöÆ¶UöFV&&÷&æÂ2Â#RãRÜ+"Â3bRÂRãÜ+"À ¤f÷W"öbF†Rf—fR&RæÖVBÂFö7VÖVçFVB'V–ÆF–æw2ÂæBF†R66†VGVÆRv2öffW&–ærF†V—"Æ÷G2Fð¦æöç–Ö÷W2–çfVçFVB&öög2â¢¥F†R6Æ–ÖVB&Æö6²—2F†R6†'W7B66R¢£¢&Æµ÷6÷WF…÷vFW%ög&æ¶Æ–æ §v2FVÇB6—‚&–æ6—Â&öög2f÷"v†B—B6ÆÆVB6WfVâg&VRÆ÷G2ÂæBF†RFV×ÆR'V–ÆF–ær—2öà¦öæRöbF†VÒà ¢¢¥F†R'VÆRæ÷r†2GvòFW7G2ÂæBV6‚ç7vW'2F–ffW&VçBv’öb&V–ærw&öærâ¢¢F†W’Æ—fR–à¦FööÇ2÷ÆEöö67Wæ7’ç–Âv†–6‚—2F†RôäÅ’–×ÆVÖVçFF–öâ(	BFööÇ2÷&V6öæ6–ÆUóccRç–æ@¦FööÇ2övVæW&FUö&Æö6µö–æf–ÆÂç–&÷F‚–×÷'B—BÂv†W&RBÔb†BÆVgBF†VÒv—F‚6÷’V6‚à £â¢¤'V–ÆF–ær7FæG2öâF†RÆ÷BÖ÷7Böb—B—2öâ¢¢Â'’ÖV7W&VB&VâF†R6ÖR6Æ–ÒF†P¢6VçG&ö–BÖFRÂÖFR&÷WBF†R'V–ÆF–ær–ç7FVBöb&÷WBö–çB–ç6–FR—BâöâF†R6öÖÖ—GFV@¢FF6WB—B—2W&VÇ’FF—F—fS¢¢¦æò&V6÷&B6†ævW2Æ÷B¢¢Âö67W–VBÆ÷G2vòs’(i"ƒBÂæ@¢æ÷F†–ærF†B&VBF¶Vâ&V6ÖRg&VRà£"â¢¤—Bö67W–W2F†BÆ÷BöæÇ’v†W&R—B&V6†W2F†RÆ÷Bw2'V–ÆF&ÆR'B¢¢(	BF†RÆ÷B–ç6WB'¢F†RãRÒWfW'’æWr&ööb×W7B¶VWg&öÒ—G2÷vâÆ÷BÆ–æW2â¢¤¢â‚â¶–ç¦–Rw27F÷&RV&ç2F†—0¢FW7B¢£¢’ãrÜ+"öb—BÆ–W2öâ&Æµ÷6÷WF…÷vFW%ög&æ¶Æ–æÆ÷B"æB¦æöæR¢–ç6–FRF†R'V–ÆF&ÆP¢–ç6WBÂ6ò&ööb7F–ÆÂf—G2F†W&R6ÆV"öb—BæBF†R66†VGVÆRÖ’7F–ÆÂFVÂöæRâv—F†÷W@¢FW7BGvòF†RF÷vâv÷VÆBÆ÷6R&öög2—B6â†öæW7FÇ’†fRà ¢¢¥F†RÆVFvW"†BF†R6ÖRFVfV7Bg&öÒF†R÷F†W"6–FRâ¢¢&ööbv2GG&–'WFVBFò&Æö6²'’—G0§÷6—F–öâô”åBÂ6òF‡&VR'V–ÆF–æw2v†÷6Rö–çB—2–âF†R&öGv’vW&R6÷VçFVB27FæF–ær–âæð¦&Æö6²BÆÃ¢F†R¢¤W†6†ævR6öffVR†÷W6R¢¢‡v†–6‚†öÆG2æ–æRFVçF‡2öbÆ÷BöbF†R6Æ–ÖV@¦&Æö6²’Â¢¤†&ÖöâbÆööÖ—2w27F÷&R¢¢æBF†R¢¥G&VÖöçB†÷W6R¢¢âF†V—"&öög2vW&RæWfW"7V'G&7FV@¦g&öÒF†R†VG&ööÒöbF†R&Æö6²F†W’‡—6–6ÆÇ’7FæB–ââ&ööb7FæF–æröâ&Æö6²w2Æ÷B7FæG0¦–âF†B&Æö6²à ¢¢¥v†B—B6÷7Bâ¢¢66†VGVÆ&ÆRÖöâÖ6÷fW&VBÖw&÷VæB¢£cb(i"c¢£²vFVBöâ6÷fW&vR¢£332(i"33‚¢¢à¥7FæF–ær&öög2&RVæ6†ævVBB#cbÂ&VÖ–æ–ærB3“’(	Bæ÷F†–ærv2'V–ÇB÷"&VÖ÷fVBâf÷W"&Æö6·0¦Æ÷6Rg&VRÆ÷BV6‚æB&Æµ÷6÷WF…÷vFW%ö6Æ&¶Ç6òv–ç2Gvò7FæF–ær&öög2Â6ò—G2FVÂG&÷0¦g&öÒrFòRà ¢¢¥v†B—BÖV7W&VBæBFVÆ–&W&FVÇ’F–Bæ÷B6ÆÂö67Wæ7’â¢¢&V6öåóƒ3U÷vW7Eó†Æ2ã’Ü+ ¦öçFò&Æµ÷&æFöÇ…ö6Æ–çFöæÆ÷B"Âv†W&RBÔB7FæG2&–æ6—Â&ööbâFW7BöæR6VG2—BöâÆ÷BBÀ§v†W&Rƒ"Röb—B—2Â6òF†BÆ6VÖVçB7FæG2â'VÆRF†B6ÆÆVBWfW'’Æâö67WF–öâv÷VÆ@¦†fR6öæFVÖæVB6öÖÖ—GFVBÂvFVBÆ6VÖVçB÷fW"6÷&æW"öb'V–ÆF–ærÂæBv†WF†W"Gvò&öög0¦Ö’7FæBF‡&VRÖWG&W2'B7&÷726öæ¦V7GW&Â6–FRÆ÷BÆ–æR—2F†R6W&F–öâvFRw2VW7F–öà®(	Bv†–6‚—B76VBâ&V6÷&FVB†W&R6òF†R6–ÆVæ6R—2æ÷BÖ—7F¶Vâf÷"æö&öG’†f–ærÆöö¶VBà ¢¢¥v†BF†—2&6VÂF–BäõBFó¢¢¢'V–ÆB&Æö6²âBÔr6Æ–ÖVB&Æµ÷6÷WF…÷vFW%ög&æ¶Æ–ææBf÷Væ@¦—B6÷VÆBæ÷B&R'V–ÇB†öæW7FÇ“²—B&WGW&ç2FòF†RVWVRv—F‚6÷'&V7FVBFVÂ(	Br&öög2ÂP§&–æ6—ÂæB"æ6–ÆÆ'’Âöâ6—‚g&VRÆ÷G2à ¢22æWr##bÓ‚ÓR(	B†ÆbF†R÷Vâ&Æö6·2vW&R66†VGVÆVB&öög2F†V—"÷vâÆ÷G26÷VÆBæ÷B†öÆ@ ¢¢¥BÔbâ¢¢F†RccR×&ööb66†VGVÆR6÷VçFVB&Æö6²w2&ööÒ–â$ôôe2æBæWfW"–âÄõE2ÂæB&–æ6—À§&ööbæVVG2g&VRÆ÷BâÖV7W&VB7&÷72F†RFVâ÷Vâ&Æö6·2BFWdcfc&&6&Âv–ç7BF†RÆ6VÖVç@¦vFW2–âFööÇ2övVæW&FUö&Æö6µö–æf–ÆÂç–F†Bv÷VÆB†fR&VgW6VBF†VÓ  §Â&Æö6²ÂÆ÷G2Âg&VRÂFVÇB&–æ6—ÂÂv†BF†R&V6—Rv÷VÆB†fR†—BÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â&Æµ÷6÷WF…÷vFW%ö6Æ&¶Â‚ÂbÂ¢£r¢¢Â¢§Vçw&—F&ÆR¢¢(	Bæò6WfVçF‚g&VRÆ÷BW†—7G2À§Â&ÆµöÆ¶UöÖ&¶WFÂ‚ÂbÂ¢£r¢¢Â¢§Vçw&—F&ÆR¢¢(	Bæò6WfVçF‚g&VRÆ÷BW†—7G2À§Â&Æµ÷6÷WF…÷vFW%÷vVÆÇ6Â‚ÂrÂrÂf–ÆÇ2F†R&Æö6³²æòÆ÷BÆVgB÷VâÀ§Â&Æµ÷&æFöÇ…ög&æ¶Æ–æÂ‚ÂrÂrÂf–ÆÇ2F†R&Æö6³²æòÆ÷BÆVgB÷VâÀ§Â&Æµ÷&æFöÇ…ö6Æ&¶Â‚ÂrÂrÂf–ÆÇ2F†R&Æö6³²æòÆ÷BÆVgB÷VâÀ§Â&Æµ÷&æFöÇ…öFV&&÷&æÂ‚Â2Â¢£¢¢†öæRæ6–ÆÆ'’’Â¢§Vçw&—F&ÆR¢¢(	B–&B'V–ÆF–ær&V†–æBæò&ööbÀ ¢¢¤f—fRöbF†RFVâÂæBF‡&VRF—7F–æ7Bf–ÇW&W2Âæ÷BöæRâ¢¢Gvò&Æö6·2vW&RFVÇBÖ÷&R&–æ6—À§&öög2F†âF†W’†BÆ÷G2Âv†–6‚æò&V6—R6÷VÆB†fRw&—GFVâF÷vâBÆÂâF‡&VRvW&RFVÇBW†7FÇ¦2Öç’2F†W’†Bg&VRÂv†–6‚—2w&—F&ÆRæB§v÷'6R£¢—B6–ÆVçFÇ’7VæG2F†Rf6æ7’F†R&6VÀ§&V6—Rw2÷vâÆ6VÖVçB'VÆR&öÖ—6W2(	B¢&&Æö6²B66—G’—26Æ–Ò&÷WBƒ3RF†BF†P¦Wf–FVæ6RFöW2æ÷B7W÷'C²F†R66†VGVÆRw266—G’—26V–Æ–ær"¢(	B6òF†Rf—'7B&6VÂFòF¶RöæP§v÷VÆB†fRf–ÆÆVB&Æö6²Fò66—G’v†–ÆR76–ærWfW'’vFRâæB&Æµ÷&æFöÇ…öFV&&÷&æÂF†P¥BÔ6‚&6¶f–ÆÂÂv2FVÇB6–ævÆR–&B'V–ÆF–æræBæò&–æ6—Â&ööbFò7FæB—B&V†–æC¢F†R6ÖP¦&Æ–æFæW726VVâg&öÒF†R÷F†W"VæBÂ&V6W6Râæ6–ÆÆ'’&ööbw2vFR—2F†B—B6W'fW2&–æ6—À§&ööbF†R6ÖR&6VÂ'V–ÇBà ¢¢¥v‡’—Bv2–çf—6–&ÆRâ¢¢ö67Wæ7’v26÷VçFVB–â&öög2(	B7FæF–æu÷&öög6(	B6òGvò&öög2öâöæP¦Æ÷BæBGvò&öög2öâGvòÆ÷G27V'G&7FVBF†R6ÖRÖ÷VçBöb†VG&ööÒâF†R&Æö6²vVæW&F÷"†0¦FW&—fVBG'VRÆ÷Bö67Wæ7’6–æ6RBÔBæBF†R66†VGVÆRæWfW"F–BÂ6òF†RGvò†ÇfW2öbF†R6ÖP§VW7F–öâvW&R&V–ærç7vW&VB'’F–ffW&VçB&—F†ÖWF–2âæ÷F†–ær6†—VBw&öæs¢F†RvFW2F†Bv÷VÆ@¦†fR6Vv‡BV6‚öbF†W6R&R&VÂæBv÷VÆB†fRf—&VBâ¢¥F†RFVfV7Bv2F†BF†W’f—&RBF†P¤TäBöb&6VÂ¢¢(	BgFW"'Vâ†26Æ–ÖVB&Æö6²Â&VBF†R66†VGVÆRæBw&—GFVâ&V6—Rà ¢¢¥F†Rf—‚—2F†BF†RFVÂæ÷r¶æ÷w2v†BÆ÷B—2â¢¢FööÇ2÷&V6öæ6–ÆUóccRç–FW&—fW2Æ÷@¦ö67Wæ7’'’F†R§6ÖR'VÆRF†RvVæW&F÷"W6W2¢(	Bfö÷G&–çB6VçG&ö–Bv–ç7BF†R6öÖÖ—GFVBÆ÷@§öÇ–vöâ(	BæB&Æö6²w2&ööÒ&V6öÖW2&–æ6—ÂÒÖ–â†g&VRÆ÷G2(‰"Â&ööb†VG&ööÒ–v—F€¦æ6–ÆÆ'–&÷VæFVB'’&÷F‚F†RSC£S&F–òæBF†R&–æ6—Ç2F†V×6VÇfW2âF†RFVÂöffW'2§Fö¶VâVæ—B6ææ÷BF¶RFòF†RæW‡BVæ—B–ç7FVBöbG&÷–ær—BÂ6òWfW'’Ö&v–æÂ7F–ÆÂ6Æ÷6W2À¦æBæWr76W'F–öâf–Ç2F†R'V–ÆB–bç’Væ—B—2WfW"FVÇB7B—G2&ööÒà ¢¢¥v†B—B6÷7BÂæBF†RçVÖ&W"—2F†Rö–çBâ¢¢66†VGVÆ&ÆRÖöâÖ6÷fW&VBÖw&÷VæB¢£s(i"cb¢£²vFVBöà¦6÷fW&vR¢£3#‚(i"332¢¢âf—fR&öög2Ö÷fVBg&öÒ&'V–ÆF&ÆRæ÷r"Fò'v—F–æröâ6÷fW&vR"&V6W6P§F†W’æWfW"†Bç—v†W&RFò7FæBâ¢¤ÆÂFVâ÷Vâ&Æö6·2&Ræ÷r'V–ÆF&ÆRæBWfW'’öæRöbF†VÐ¦¶VW2Æ÷B÷Vâ¢¢Âv†–6‚—2F†R7FFRBÔröçv&B6â&R'Vâg&öÒv—F†÷WB&RÖFW&—f–ærF†—2à ¢¢¥v†BF†—2&6VÂF–BäõBFó¢¢¢'V–ÆB&Æö6²âBÔb6Æ–ÖVB&Æµ÷&æFöÇ…ög&æ¶Æ–ææBf÷VæB—@§v2öæRöbF†RF‡&VRF†B6÷VÆBæ÷B&R'V–ÇB†öæW7FÇ“²F†R&Æö6²—2&VÆV6VB&6²FòF†RVWVRv—F€¦6÷'&V7FVBÖ—‚ƒb&–æ6—Â²"æ6–ÆÆ'’ÂöæRÆ÷B÷Vâ’f÷"F†RæW‡B'VâFòF¶Rà ¢22æWr##bÓ‚ÓR(	BF†R6&BFG2—G2÷vâ6Æ–×2WÂæB#Böb#s’'V–ÆF–æw2†fRæ÷F†–ærGFW7FVB&÷WBF†VÐ ¢¢¤³#6"¢¢ÂF†R7V'7FçF—fR†ÆböbF†R÷væW"w2&W÷'BæBF†R6WVVÂFò³#6&VÆ÷râWfW'§&÷fVææ6R6&Bæ÷r÷Vç2v—F‚¢¦v†BF–BvR–æ6ÇVFRÂæBv†W&RF–B—B6öÖRg&öÓö¢¢(	BF‡&VP§&÷w2ÂöæRW"ÆWfVÂÂæÖ–ærF†R6Æ–×2F†B7FæBBV6‚æB6––ærv†W&RF†W’6ÖRg&öÒà ¢¢¤—B—2'F—F–öâÂv†–6‚—2F†Rv†öÆRöbv‡’—B6â&RvFVBâ¢¢WfW'’w&FVB6Æ–ÒF†R6&@§&VæFW'2ÆæG2–âW†7FÇ’öæR&÷rÂ6òF†R&VÆV6R6†V6²—2$T4õTåB&F†W"F†âÆöö³¢–6°¦WfW'’'V–ÆF–ærB&÷F‚f–Ww÷'G2ÂFÆÇ’F†R6öæf–FVæ6R6†—2öfbF†R$TäDU$TB6&BÂæB&WV—&P§F†R6V7F–öâw2F‡&VRçVÖ&W'2Fò&RF†÷6RçVÖ&W'2â¢£#sböb#sbÆöFVB'V–ÆF–æw2w&VRâ¢¢F†P§&V6÷VçB&WW6W2F†RöÆFW"6†—Ö6÷fW&vRvFRw2÷vâ6VÆV7F÷"öâW'÷6R(	BGvòFVf–æ—F–öç2öb&¦6Æ–ÒöâF†—26&B"—2†÷r7VÖÖ'’v÷VÆB6öÖRFòF—6w&VRv—F‚F†R6&Bv†–ÆR&÷F‚vFW0§7F–VBw&VVâà ¢¢¥F†RFF6WBÂ6÷VçFVBf÷"F†Rf—'7BF–ÖRF†—2v’â¢¢#s’&V6÷&G26''’¢£2ÃcsRw&FVB6Æ–×2(	@£“’GFW7FVFÂS’–æfW'&VFÂ"Ã“cr&V6öç7G'V7FVFâ¢¢¢£#BöbF†R#s’†fRæòGFW7FVB6Æ–Ð¦BÆÂ¢¢Â6ò&÷rF†B&VæFW&VBöæÇ’v†Vâ—B†B6öÖWF†–ærv÷VÆBvò6–ÆVçBöâF‡&VRV'FW'2ö`§F†RF÷vâBF†RW†7BÖöÖVçBf—6—F÷"æVVG2FVÆÆ–ærâ—B6—2¢$æ÷F†–ær&÷WBF†—2'V–ÆF–ær—0¦GFW7FVB'’6÷W&6Râ"¢–ç7FVBà ¢¢¤6—FF–öâÖVç2F–ffW&VçBF†–ærBV6‚ÆWfVÂâ¢¢g&öÖöââGFW7FVB6Æ–Ó²&÷VæFVB'– ¦öââ–çfVçFVBöæR(	B“2æöç–Ö÷W2&öög26—FRF†R&V6öç7G'V7F–öâ7V2æBæG&V2öâWfW'¦GG&–'WFRÂæBöæR6÷W&6W3¦Æ&VÂ÷fW"ÆÂF‡&VR&÷w2v÷VÆB†fR&–çFVBæ–æWFVVçF‚Ö6VçGW'¦†—7F÷'’2GG&–'WF–öâf÷"'V–ÆF–æræö&öG’6Æ–×27FööBF†W&Rà ¢¢¥Gvòf–æF–æw2F†B&Ræ÷BF†R6V7F–öââ¢  ¢Ò¢£c’'V–ÆF–æw2†fR–çfVçF–öç2F†Bæ÷F†–ær—2&V6÷&FVB2&÷VæF–ærâ¢¢öbF†R#s&V6÷&G2v—F€¢BÆV7BöæR&V6öç7G'V7FVF6Æ–ÒÂc’6—FRæ÷F†–æröâç’öbF†VÒÂ6òF†V—"&÷VæFVB'–Æ–æP¢&VG2¢$æ÷F†–ær—26—FVB2&÷VæF–ærF†W6Râ"¢F†R&÷GFöÒF–W"&WV—&W2æ÷FRæBæ÷B6÷W&6P¢(	BFVÆ–&W&FVÇ’(	B'WBæö&öG’†BWfW"6÷VçFVBF†R6öç6WVVæ6RâF†R6Vvæ6‚†÷FVÂ—2öæRöbF†P¢c’âf—6–&ÆRæ÷r&F†W"F†âf—†VC²v†WF†W"F†÷6R6†÷VÆB7V—&R&÷VæB—2&W6V&6‚à¢Ò¢¤GFW7FVB—2æ÷B'V–ÇBÂöâB&V6÷&G2â¢¢F†RvW7FW&â†÷FVÂw27F&ÆW2&RGFW7FVB'’¢&RÖf—&R66÷VçBæBF†W&R—2æ÷F†–æröbF†VÒ–âF†RÖöFVÂâ7VÖÖ'’öbv†Bv2¦–æ6ÇVFVB ¢F†B6÷VçFVBF†VÒVæFW"&GFW7FVB"æB7F÷VBv÷VÆBæÖR6öÖWF†–ærF†B—2æ÷BF†W&RÂ6òF†P¢&÷r&WVG2F†RÖ&²F†RF&ÆR&VÆ÷rÇ&VG’6'&–W3¢¤æ÷B–âF†RÖöFVÃ¢7F&ÆW2¢à ¢22æWr##bÓ‚ÓR(	B“2'V–ÆF–æw2vW&RæÖVBw&FR&WGFW"F†âF†V—"÷vâ&V6÷&BÂæBF†R&VÆV6RvFRv2†öÆF–ær—B–âÆ6P ¢¢¤³#6¢¢Â÷væW"×&W÷'FVBg&öÒ6&BöâF†RFWb&Wf–WrâF†R†VF–ær&VB¢¢$–æfW'&VB7F&ÆP¢3r"¢¢æBWfW'’6†—&VæVF‚—B&VB¢¥$T4ôå5E%T5DTB¢¢âF†R†VF–ærv2F†Rw&öæröæRÂöà¢¢£“27G'V7GW&R&V6÷&G2¢¢(	BWfW'’æöç–Ö÷W2&ööbF†—2&ö¦V7B†2WfW"vVæW&FVBà ¢¢¤—B—2F†R&W6–GVRöbf—‚F†Bv÷&¶VBâ¢¢F†RcsbÖW&vRöb##bÓ‚Ó2Ö÷fVB’ÃsbfÇVW2öçFð¦GFW7FVBò–æfW'&VBò&V6öç7G'V7FVFæB&RÖw&FVBÃc“BF†B†B6Æ–ÖVBFò&R&V6öæ–ærv†Và§F†W’vW&R–çfVçF–öââ—BÖ÷fVBF†RDDâF†R$õ4R—2†&F6öFVB–âF†RvVæW&F÷'2ÂæB—BF–Bæ÷@¦Ö÷fR(	B6ò–æfW'&VFvVçBg&öÒ&V–ærF†R$õEDôÒF–W"‡v†W&R$–æfW'&VB7F&ÆR"v2†öæW7B’Fð§F†RÔ”DDÄRöæRÂ§&V6öæVBg&öÒWf–FVæ6R&÷WBF†—2'F–7VÆ"F†–ær¢Âv†–6‚âæöç–Ö÷W0¦6÷VçB×Væ—B—2&V6—6VÇ’æ÷Bâ¢¤æ÷F†–ær&÷WBç’'V–ÆF–ær6†ævVB†W&R¢£¢æ÷B÷6—F–öâÂ¦F–ÖVç6–öâÂ6÷W&6R÷"w&FRâöæÇ’v†BF†R6&B6ÆÇ2F†VÒà ¢¢¥66ÆRÂW†7FÇ’Â6òÆFW"7vVW6âFVÆÂG&–gBg&öÒg&W6‚fVÇBâ¢¢“2æÖW3²c ¦7–Ö&öÆ–5öÆö6F–öæ7G&–æw3²“2&W6V&6…öæ÷FV÷VæW'2'F—F–öæ–ær6ÆVæÇ’–çFòC ¦$T4ôÔÔTäDTBòtTäU$DTFÂ3”ädU%$TB%T”ÄD”ävæB#”ädU%$TBòtTäU$DTF²WfW'¦6†ævUöæ÷FVöââæöç–Ö÷W2&ööc²F†R6&Bw2÷vâ&V6öç7G'V7F–öâfÆs²æBF†R†÷W6V†öÆBæ@§W'6öâÆ&VÇ2öbF†R³Æ–W"â¢¦&V6öÖÖVæFVF—2F†Rv÷&BF†—2&ö¦V7B&VæÖVBv’g&öÒ%’äÔP¦öâ##bÓ‚Ó2¢¢æBF†Vâ&–çFVBöâC"6&G2f÷"f÷'Fæ–v‡Bà ¢¢¤f—fRvVæW&F÷'2Âæ÷BF†RGvòF†R&6VÂÆ—7FVB(	BæB6—‡F‚7FvRF†B—2æ÷BvVæW&F÷"â¢ ¦vVæW&FUö–æfW'&VEöæÖW2ç–'Vç2eDU"F†R†÷W6V†öÆB&öw&ÖÖRæB&Ww&—FW2F†R†÷W6V†öÆBw2÷và¦Æ&VÂâ&VvVæW&F–ær†÷W6V†öÆG2v—F†÷WB—BFVÆWFW2WfW'’–çfVçFVB&W6–FVçBw2æÖRæ@¦æÖUö&6—6(	BF†Rv†öÆRöb³‚(	BæB¢§F†R†÷W6V†öÆB&öw&ÖÖRw2ÒÖ6†V6¶6ææ÷B6VRF†—2¢¢À¦&V6W6R—B÷fW&Æ—2F†RæÖ–ær72&Vf÷&R6ö×&–ærâÒÖ6†V6¶—2w&VVâV—F†W"v’âF†R÷&FW"—0¦vVæW&FUö–æfW'&VEö†÷W6V†öÆG2ç–F†VâvVæW&FUö–æfW'&VEöæÖW2ç–ÂæB—B—2æ÷rw&—GFVâ–çFð¥$ôDÔ³#6v†W&RF†RæW‡BW'6öâv–ÆÂÆöö²à ¢¢¥F†RvFRv2Væf÷&6–ærF†RfVÇBâ¢¢6Öö¶U÷&VæFW&W"æÖ§676W'FVBF†R†÷W6V†öÆBÆ&VÂÖF6†V@¦ö–æfW'&VBöâ6òF†RF†–ærF†B6†÷VÆB†fR6Vv‡BF†—2v2&WV—&–ær—BâF†B76W'F–öâ—0§–ææVBFòF†R†VBw2÷vâw&FVæ÷rÂæBæWrv†öÆR×&Vv—7G'’6†V6²f–Ç2F†R&VÆV6Röâç¦æÖR÷Væ–ærv—F‚w&FR—G2&V6÷&BFöW2æ÷B6''’Â÷"v—F‚ç’öbF†RF‡&VR&WF—&VBv÷&G2(	@§v—F‚F†RfVÇBÆçFVB–âF†R6ÖR72Â6òvFR66ææ–ær6ÆVâG&VR6ææ÷B&RÖ—7F¶Vâf÷ ¦vFR66ææ–æræ÷F†–ærà ¢¢¥GvòF†–æw2÷WG6–FRF†RvW&Rv÷'6RF†âF†R6&G2â¢¢Fö72õ$õdTää4RæÖF(	BF†RvR–÷P§6VæB6öÖVöæRFòv†VâF†W’6²v†BF†Rw&FW2ÖVâ(	B7F–ÆÂFVf–æVBFö7VÖVçFVBò–æfW'&VBð¦6öæ¦V7GW&ÆÂ6ò&V6÷&Bw&—GFVâ'’föÆÆ÷v–ær—B¢¦f–Ç2F†R'V–ÆB¢¢âæBfÆ–FFRç–w2÷và¦W'&÷'2æÖVBF†Rw&öærF–W#¢6÷W&6VÆW72GFW7FVFfÇVR&W÷'FVB¢&Fö7VÖVçFVB&WV—&W2@¦ÆV7BöæR6÷W&6Uö–B"¢â&÷F‚6÷'&V7FVC²$ôDÔ³bÂv†–6‚&÷÷6VBF†—&Bfö6'VÆ'’F†BæWfW §6†—VBÂ—2¢¤4Äõ4TB27WW'6VFVB¢¢à ¢¢¥7F–ÆÂ÷VâÂæB—B—2F†R†ÆbF†R÷væW"6&VBÖ÷7B&÷WBâ¢¢³#6"(	B§6’v†Bv2”ä4ÅTDTB@¦V6‚ÆWfVÂæBv†W&R—B6ÖRg&öÒ¢(	B—2VçF÷V6†VBâF†RæÖW2&RæòÆöævW"w&öæs²F†R6&G27F–ÆÀ¦Fòæ÷BFVÆÂf—6—F÷"F†B'V–ÆF–ærw2fö÷G&–çBÂ†V–v‡BÂ&ööbf÷&ÒæB÷6—F–öâvW&RÆÀ¦–çfVçFVBæBöæÇ’—G2&Æö6²v2&V6öæVBà ¢22æWr##bÓ‚ÓB(	BF†R&Æö6²v†W&RGvòÆ–W'2öbF†—2&V6öç7G'V7F–öâÖWBöâF†R6ÖRw&÷VæBÂæBF†RF÷F–öâ'VÆRw&WrF†—&BFW7@ ¢¢¥BÔRâ¢¢&Æµ÷&æFöÇ…öÖ&¶WF(	B&æFöÇ‚Âg&æ¶Æ–âÂv6†–æwFöâÂÖ&¶WB(	B—2F†Rf—'7B6÷WF€¤F—f—6–öâ&Æö6²öbF†R&æFöÇ‚&÷ræBæ÷r6'&–W2¢¦V–v‡Bæöç–Ö÷W2&öög2¢£¢f÷W"GvVÆÆ–æw2ÂöæP§W"Æ÷Böâf÷W"öbF†R6—‚g&VRÆ÷G2ÂæBf÷W"–&B'V–ÆF–æw2öfbF†R&Æö6²ÆÆW’â¢¥7FæF–ær&öög0£#S‚(i"#cc²&VÖ–æ–ærCr(i"3“’ÂsöbF†VÒöâw&÷VæBF†R&ö¦V7B†26÷fW&vRf÷"â¢¢†÷W6V†öÆG0¢¢£SR(i"Sb¢¢ÂW'6öç2¢£“(i"“"¢¢â&V6÷&FVB–â¢¤Ã“r¢¢âF†R&6VÂWF†÷'2æò6ö÷&F–æFW3¢WfW'¦ÖWG&R—2&VBöfbF†R6öÖÖ—GFVB³rÆ÷BöÇ–vöç2Âv†–6‚—2v†B†2ÖFRWfW'’&Æö6²6–æ6RBÔ"§&V6—RVçG'’&F†W"F†âvVöÖWG'’&wVÖVçBâF†R&V6—R6ÆV&VBWfW'’öæRöbF†RvVæW&F÷"w0§Æ6VÖVçBvFW2öâ—G2f—'7B'Vâ(	BæòÆ÷BÖÆ–æRÂ6W&F–öâÂ6÷'&–F÷"Â&VÆ–Vb÷"ö67Wæ7’f–ÇW&P§Fò—FW&FRv–ç7B(	Bv†–6‚—2v†BF†R67V×VÆFVBvFW2öbBÔ"F‡&÷Vv‚BÔBvW&Rf÷"à ¢¢¥F†R&Æö6²v2Ç&VG’'V–ÇBöâ'’D„•2&ö¦V7Bw2÷F†W"†Æbâ¢¢Ã“R&V6÷&FVBF†Rf—'7@§'FÇ’Ö'V–ÇB&Æö6²æBF†R&öög2–â—G2v’6ÖRg&öÒF†R&R×ÆBvW7BF—f—6–öâFVç6—G’&V6—Rà¤†W&RF†RGvò7FæF–ær&öög2&R–æe÷6w–W%öGvVÆÆ–æuöæBö&(	BF†RGvVÆÆ–æw2öbF†Rö67WF–öà¦6Vç7W2w2÷vâGvò6w–W"†÷W6V†öÆG2ÂÆ6VBg&öÒG—VBÆö6ÂÔTåR6ö÷&F–æFW2&Vf÷&RF†RÆBÖöGVÆP¦W†—7FVBâF†RÆ–W"F†B&wVW2v†òF†RF÷vâ†VÆBæBF†RÆ–W"F†Bf–ÆÇ2—G2&Æö6·2†fRæ÷p¦6öÆÆ–FVBÂæBF†RBÔBÖ6†–æW'’'6÷&&VB—Bv—F†÷WB6†ævS¢ö67Wæ7’FW&—fVBg&öÒF†R6öÖÖ—GFV@¦fö÷G&–çG2ÂÆ÷G2BæBb&VgW6VB6V6öæB&–æ6—Â&ööbÂ†VG&ööÒ7VçBöâF†R6—‚g&VRÆ÷G2à ¢¢¥v†W&RF†Rf6æ7’fÆÇ2v2FV6–FVB'’&—F†ÖWF–2ÂæBF†R&6VÂ6—26ò&F†W"F†âG&W76–ær—@§Wâ¢¢&÷F‚7FæF–ær&öög26—BöâF†R&æFöÇ‚f6RÂ6òF†RGvòÆ÷G2g&VRF†W&R&RW†7FÇ’F†RGvð§F†Rg&öçFvR×fÇVRG—öÆöw’vçG2f÷"F†R&WGFW"6÷GFvW2ÂæBF†R&öw&ÖÖRw2ÇFW&æF–ærf6æ7¦†2æ÷v†W&RFòfÆÂ'WBv6†–æwFöââ†BF†R66†VGVÆRFVÇBöæR&ööbfWvW"F†RGFW&âv÷VÆB†fP§&VB2FVÆ–&W&FRâ'&ævVÖVçEöæ÷FVæBÃ“r&÷F‚7FFR—Bà ¢222F†RF†—&BF÷F–öâFW7B(	BF†RVW7F–öâBÔBÆVgB÷VâÂ6WGFÆV@ ¥BÔ&‚w2'VÆRb†B¢§Gvò¢¢FW7G3¢F†RG&FRw26öÖÖ—GFVB&wVÖVçB×W7B6ÆÂ—G26÷VçBfÆö÷"Âæ@§F†R&ööbw2fÖ–Ç’×W7B&RöæRF†—2Æ–W"Ç&VG’†÷W6W2F†BG&FR–ââBÔBÖWB66RæV—F†W ¦6÷fW&VB(	BC26'VçFW"&ööböâF†Rf—'7BvW7BF—f—6–öâ&Æö6²Âv†VâÆÂVÆWfVâ6'VçFW ¦†÷W6V†öÆG27FööBæ÷'F‚÷"6÷WF‚(	BæB&VgW6VB—B¢¦'’†æB¢¢ÂÆVf–ærF†RVW7F–öâFòBÔRà ¢¢¥'VÆRbæ÷r†2F‡&VRFW7G2¢¢ÂF†RF†—&B&V–ærF†R&ööbw2¢¦F—f—6–öâ¢¢â—B—2F†RfÖ–Ç’FW7BÖFP¦&÷WBF†R÷F†W"†—2öbF†R6ÖRF&ÆS¢v†W&RG&FRÆ—fVB—22×V6‚6Æ–Ò&÷WBF†RF÷vâ0§v†B—BÆ—fVB–ââ¢¤—Bv26†V6¶VBv–ç7BWfW'’F÷F–öâFV6—6–öâF¶Vâ&Vf÷&R—BæB&V6÷fW'2ÆÀ¦f÷W"¢¢(	BBÔ&‚w26'VçFW"F÷FVBÂBÔ&‚w2Æ&÷W&W"F÷FVBÂBÔBw2Æ&÷W&W"F÷FVBÂBÔBw0¦6'VçFW"&VgW6VBâFW7BF†B†BFò&RFöÆBF†÷6Rç7vW'2v÷VÆB&R&VfW&Væ6S²öæRF†@§&V6÷fW'2F†VÒ—2'VÆRâF†—2&Æö6²w2C2öâÆ÷Br76W2ÆÂF‡&VRÂ6òGvVÆgF‚6'VçFW"†÷W6V†öÆ@¦—2–æfW'&VB†6'VçFW"(i""’æBF†R÷F†W"6WfVâ&öög27F’æöç–Ö÷W26÷VçB×Væ—G2à ¢222v†BF†RFW7B6ææ÷Bç7vW"ÂæB—B—2æ÷B&÷WBF†RG&FW2(	B¢¤³#¢  ¥F†R6w–W'2v†÷6RGvò&öög27FæBöâF†—2fW'’&Æö6²¢§72FW7B¢¢(	BF†V—"&wVÖVçB&VG2'Gvð§6w–W"†÷W6V†öÆG2&R–æfW'&VBÂ¢§F†R6ÖÆÆW7BçVÖ&W"F†Bç7vW'2F†RFVÖæB¢¢"(	BæBf–ÂFW7B ¦f÷"&V6öâF†B†2æ÷F†–ærFòFòv—F‚6w–W'3¢F†V—"GvVÆÆ–æw2&R&W7ö¶P¦–æe÷6w–W%öGvVÆÆ–æuò¦&V6÷&G26''––æræò&V6öç7G'V7F–öâæfÖ–Ç–BÆÂÂ6òF†RVW7F–öâ'v†–6€¦fÖ–Ç’FöW2F†—2Æ–W"†÷W6RF†BG&FR–â"†2æ÷F†–ærFò&VBâ¢¤f÷W"G&FW2öbGvVçG’Öæ–æR&P¦†÷W6VBF†Bv’æBöæÇ’F†Bv’¢¢(	B'&–6¶Ö¶W"Â6¶W"Â6w–W"Âv†VVÇw&–v‡B(	BæBV–v‡BÖ÷&R&P§'FÇ’6òâf÷"F†÷6Rf÷W"F†R6V6öæBFW7B—2¢§6–ÆVçBÂæ÷BæVvF—fR¢¢ÂæB6–ÆVæ6R—27W'&VçFÇ¦&V–ær&VB2&VgW6ÂâF†B—2F†R6öç6W'fF—fRF—&V7F–öâæB—B—2æ÷BF†R6ÖRF†–ærâ÷VæVB0¥$ôDÔ³#à ¢222³#ÖV7W&VBv–âÂg&öÒöæRÖ†÷W6V†öÆB–ç6W'F–öà ¤–ç6W'F–ær6–ævÆR†÷W6V†öÆB&VæÖVB¢£röbF†R32¢¢6'&–VBÖ÷fW"–çfVçFVBW'6öç2–âF†RF÷V6†V@¦†÷W6V†öÆBf–ÆW2Â&V6W6RF†RæÖRÆÆö6F÷"FVÇ2'’–æFW‚âBÔ&‚w2Gvò×W'6öâ–ç6W'F–öâ&VæÖV@£#Röb“C²F†—2—2F†R6ÖRFVfV7BBF†R6ÖR&FRæB—B—27F–ÆÂ÷Vââæ÷F†–ær&÷WBç–&öG’w0¦&wVVB†—7F÷'’6†ævVB(	BöæÇ’F†R–çfVçFVBæÖRGF6†VBFò—BâF†R6‡W&â—2v‡’F†—2&6VÂw2F–f`§F÷V6†W2#B†÷W6V†öÆBf–ÆW2f÷"öæRFF—F–öâà ¢22f—†VB##bÓ‚ÓB(	BF†R&öG2vW&R–çf—6–&ÆRÂWfW'’7G&VWB6†V6²v2w&VVâÂæBF†R&–ÖR7W7V7Bv2–ææö6Vç@ ¥"Ô%Ts"Â÷væW"×&W÷'FVC¢¢'F†RF÷vâ&öG26VVÒFòF—6V"–âÆ6W2æBv†Vâ–÷RfÇ’÷fW"F†VÐ§–÷RÆ÷6RF†VÒâ"¢G'VRB&÷F‚f–Ww÷'G2â¢¥Gvò–æFWVæFVçBfVÇG2¢¢ÂæBF†RÖV6†æ—6ÒF†R&6VÀ¦æÖVB2Ö÷7BÆ–¶VÇ’GW&æVB÷WBFò&RF†RöæRF†–ærF†Bv2†VÇ–ærà ¢¢¥F†RvFR6÷VÆBæ÷B6VRç’öb—BÂæBF†B—2F†Rf—'7BF†–ærF†Bv2w&öærâ¢ ¦FööÇ2÷6Öö¶U÷&VæFW&W"æÖ§676W'FVB6WfVçFVVâ7G&VWB&V6÷&G2ÂãfW'F–6W2ÂG&RW'&÷"VæFW £RÓRÒÂæòfW'FW‚÷fW"vFW"(	BÆÂG'VRÂÆÂw&VVâÂÆÂ&W6–FRF†Rö–çBâ¢¤G&VB—2æ÷B6VVââ¢ ¤æ÷F†–ær–âF†—2&W÷6—F÷'’6¶VBv†WF†W"&öB&V6†VBF†R67&VVâà ¢¢¥v†BF†RæWr6†V6²FöW2â¢¢&öD6öçG&7B‚–†öÆG2F†R66VæRBGvòæ6†÷'2f—6—F÷"—2öffW&VB(	@¦6÷WF…÷vFW&BW–R†V–v‡BF÷vââ÷Vâ7G&VWBÂg&öÕö&÷fVBF†RW&–Âæ6†÷"(	BæBF¶W0§F‡&VRg&ÖW3¢F†R&VÂ&VæFW"¢¥"¢¢ÂF†R6ÖRvVöÖWG'’G&vâ2â÷VRÖ&¶W"v—F‚¦FVÆ–&W&FVÇ’FVWW"öÇ–vöâöfg6WB¢¤Ò¢¢ÂæBF†R66VæRv—F‚F†R7G&VWG2†–FFVâ¢¤ò¢¢â&ö&Röâ¦6öÖÖ—GFVB6VçG&VÆ–æR6÷VçG2öæÇ’v†W&R¢¤Ò¢¢&V6†VBF†R67&VVâÂ6ò&öG2vVçV–æVÇ’†–FFVâ&V†–æB¦'V–ÆF–ærÂG&VR÷"&—6RÆVfRF†R6×ÆR&F†W"F†â66÷&–ær2fVÇG2Âv†–ÆR&öBÆ÷6–ærF†P¦FWF‚f–v‡BFòF†RFW'&–â7F—2–â—BâF†R66÷&R—2ÄÂ¢…"’(‰"Â¢„ò—ÆöâF†R7&—F–2†&æW72w2÷và¦Æ$Æâ&'3¢ÖVF–â¢¬éDÅÂ¢(šRã‚¢¢æB¢®(šRSRR¢¢öb&ö&W2BéDÅÂ¢(šR"W"&æBÂvFVBFòcÒà ¢¢¤ÖV7W&VBv—F‚F†RfVÇB–â(	B&÷F‚&'2f–ÂÂv†–6‚—2F†R66WFæ6S¢¢¢6÷WF…÷vFW&#S(	3cÐ¢¢£ã2ÅÂ¢ÂBRW&6WF–&ÆR¢£²g&öÕö&÷fV(	3#SÒ¢£ãÅÂ¢ÂRöbVÆWfVâ&ö&W2¢¢âv—F‚F†P¦f—‚ÂFW6·F÷¢6÷WF…÷vFW&¢£Bã"ò2ã’òBã¢¢7&÷72C(	3Â(	3#SÂ#S(	3cÒBsòƒ’ò“"RÀ¦g&öÕö&÷fV¢£"ã’ò"ãB¢¢B“òc2Rà ¢¢¤fVÇB(	BF†RFWF‚f–v‡BÂæB—B—2F†R&W÷'FVB&–âÆ6W2"â¢¢&öB—2V'F‚–çFVBfÆBöà§F†RFW'&–âBF†R6ÖR†V–v‡BÂ†VÆB–âg&öçB'’öæRVæ—BöböÇ–vöâöfg6WBâFWF‚&V6—6–öà¦FVw&FW2v—F‚F—7Fæ6RÂ6ò7Bã#SÒF†RFW'&–âvöâ–âF6†W2â(‰#Bò(‰#†ÆöæRFöö²F†Rf–Æ–æp¦&æBFò¢£2ã2ÅÂ¢òsR¢¢âæòfW'FW‚Ö÷fVC²v÷'7DG&V7F–ÆÂvFW2BRÓRÒà ¢¢¤fVÇB"(	BF†R&öBv2BR÷VRÂæB—B—2F†R&W÷'FVBÆ÷72g&öÒF†R—"â¢¢BF†RW&–À¦æ6†÷"F†R&–&&öâ—2v–FRÂVæö66ÇVFVBæBv–ç2FWF‚ÂæB—B7F–ÆÂ66÷&VBãòR(	B¦æV—F†W"¢F†P¦öfg6WB¦æ÷"¢F†RF†–â×&–&&öâ'VÆRÖ÷fVBF†B&æBBÆÂâÆ–v‡FÇ’v÷&âG&6²w2Ç†v0¦ã‚²'WG2£ãSB(‰"7&÷vâ£ãF¢‚RV'F‚÷fW"“"R&—&–Rv’g&öÒF†R'WG2ÂBRBF†R7&÷vâà¤&6VÆ–æW2&—6VBFò¢£ãSBòã3‚òã#‚¢¢ÂÖöGVÆF–öâ6†RæB6Æ72÷&FW&–ærVçF÷V6†VBÂ&V6÷&FV@¦2¢¤Ã“b¢¢ÖVæF–ærÃs’(	Bv†–6‚Ç&VG’&V6÷&FVBF†W6RçVÖ&W'22–çfVçF–öâ&F†W"F†âÖV7W&VÖVçBà ¢¢¥&VgWFVB(	BÖ—ÖfW&vVBÇ†fÆÆ–ærVæFW"Ç†FW7Fâ¢¢F†R&6VÂw2&–ÖR7W7V7BÂæBF†P§6†RöbF†RcsBG&VVÆ–æR'VrâGW&æ–ærÖ—Ö2öfbÖFR¢¦WfW'’¢¢&æBv÷'6R†6÷WF…÷vFW& £#S(	3cÓ¢#"Röb&ö&W2&V6†–ærF†R67&VVâv—F‚Ö—2Â¢£bR¢¢v—F†÷WB’âF†RÖ—6†–â—2†öÆF–æp¦7V"×—†VÂ&–&&öâFövWF†W"Âæ÷BW&6–ær—BâÖ–äf–ÇFW&—2Væ6†ævVBÂæBF†R–ç7G'V7F–öâFð¦ÖV7W&R&Vf÷&R6†ö÷6–ær—2v†B7F÷VB&f—‚"F†Bv÷VÆB†fRÖFRF†—2v÷'6Rà ¢¢¤æ÷B7FVBöã¢¢¢G&ç7&VçC¢G'VVv—F‚Ç†FW7FFöW26÷'BF÷vâ×v–FRÖW6‚öâÖVæ–ævÆW70¦&÷VæF–ær×7†W&R6VçG&RÂæBF†R÷VRVWVRÖV7W&VB6Æ–v‡FÇ’&WGFW"(	B'WBâVæ&ÆVæFV@¦Ç†×FW7FVBg&vÖVçBG&w2BgVÆÂ7G&VæwF‚Âv†–6‚v÷VÆBÖ¶RWfW'’&öB6öÆ–BæBFVÆWFRF†P¦w&FVB÷v÷&âöÆ–v‡BF—7F–æ7F–öâF†RFF6WB6'&–W2â–bF†R6÷'BWfW"&—FW2ÂF†Rç7vW"—0§W"×&V6÷&B&VæFW$÷&FW&Âæ÷B÷6—G’à ¢¢¥v†BF†—26÷7BF†RvFRFòÆV&ã¢¢¢g&öÕö&÷fV—2âW&–Âæ6†÷"ÂæBÆVf–ærF†R6ÖW&§F†W&R'&ö¶RF†R†÷&—¦öâ×F–Ö&W"6†V6²F÷vç7G&VÒ(	B—B&VG2F†R&æBF†RG&VR6öÇfW"'V–ÆG2&÷Væ@§F†R6ÖW&æB&W÷'FVBæ÷Vv‡Böbæ÷Vv‡B6÷fW&VB&V&–æw2âÖV7W&VÖVçBF†BÖ÷fW2F†R6ÖW&÷vW0§F†RæW‡BöæR—G2÷6R&6²à ¢22æWr##bÓ‚ÓB(	BF†Rf—'7B&Æö6²7&÷72F†R&—fW"Âöâw&÷VæBF†Bv2Ç&VG’'FÇ’'V–Ç@ ¢¢¥BÔBâ¢¢&Æµ÷&æFöÇ…ö6Æ–çFöæ(	B&æFöÇ‚Â6æÂÂv6†–æwFöâÂ6Æ–çFöâ(	B—2F†Rf—'7BvW7@¤F—f—6–öâ&Æö6²F†RÆBÖöGVÆR&V6†W2æBæ÷r6'&–W2¢§6WfVâæöç–Ö÷W2&öög2¢£¢f÷W"GvVÆÆ–æw2öà¦f÷W"Æ÷G2ÂF‡&VR–&B'V–ÆF–æw2öfbF†RÆÆW’âF†RF÷vâ7FæG2B¢£#S‚&öög2öbccR¢£²Cr&VÖ–à¦æB¢£s’öbF†÷6R†fRÖöFVÆÆVBw&÷VæB¢¢âöæRÆ÷B—2ÆVgB&&RöâW'÷6RâF†RvVöÖWG'’†Æbv2§&V6—RVçG'’æBæ÷F†–ærVÇ6RÂW†7FÇ’2BÔ"&VF–7FVBf÷"F†RF†—&BF–ÖR'Vææ–ær(	Bv†BF†—0¦&Æö6²6÷7Bv2–âF†RvFW2ÂæB—B—2F†Rf—'7BöæRF†B6÷VÆB†fRf÷VæBF†—2à ¢¢¥F‡&VR&öög2vW&RÇ&VG’7FæF–æröâ—BÂæBæ÷F†–ær6÷VÆB6VRF†VÒâ¢¢WfW'’&Æö6²&6VÂ6òf ¦'&—fVBBV×G’w&÷VæBÂ6òG&VF–ærÆÂV–v‡BÆ÷G22g&VRv26÷'&V7BGv–6RæBv÷VÆB†fR&VVà§w&öær†W&S¢&V6öåóƒ3U÷vW7Eó†Âó–æBó#6—B–ç6–FRF†—2&Æö6²ÂÆ6VBg&öÒG—V@¦6ö÷&F–æFW2ÖöçF‡2&Vf÷&RF†RÆBÖöGVÆRW†—7FVBÂæB¢¦æò&V6÷&BöbF†V—'2æÖW2Æ÷B¢¢&V6W6P§F†W&RvW&RæòÆ÷G2FòæÖRâF†RöæR×&–æ6—Â×W"ÖÆ÷B6†V6²&VG2öæÇ’F†R&V6÷&G2F†R&6VÀ¦'V–ÆG2Â6òâö67W–VBÆ÷BæBg&VRöæRvW&RF†R6ÖRF†–ærFò—BÂæB¢§F†R6W&F–öâvFRFöW0¦æ÷B6Æ÷6RF†RF–ffW&Væ6S¢Gvò&–æ6—Â&öög2GvVÇfRÖWG&W2'BöâöæRGvVçG’Öf—fRÖÖWG&RÆ÷B70¦WfW'’FW7B–âF†Rf–ÆRâ¢¢6V6öæB†÷W6Röâ6öÖV&öG’w2Æ÷Bv÷VÆBæ÷B†fRÆöö¶VBÆ–¶RFVfV7Bg&öÐ¦ç’F—&V7F–öâ(	BF†RF÷vâv÷VÆB6–×Ç’†fR&VVâ6Æ–v‡FÇ’FVç6W"F†âF†Rw&÷VæB—B7FæG2öâà ¢¢¥F†Rf—‚FW&—fW2F†Rç7vW"&F†W"F†â6¶–ærf÷"—Bâ¢¢v†–6‚Æ÷G2&RF¶Vâ—2&VBöfbF†P¦6öÖÖ—GFVBfö÷G&–çG2öbF†R&V6÷&G2F†B7FæBF†W&S²&V6—RF†B†BFò&RFöÆBv÷VÆB&R§6V6öæB÷–æ–öâ&÷WBF†R6ÖRw&÷VæBÂv†–6‚—2F†RFVfV7BF†RÆBÖöGVÆRv2'V–ÇBFò&WF—&RâGvð¦vFW2&–FRv—F‚—Bâ–&B'V–ÆF–ær×W7B7FæBöâÆ÷BF†—2&6VÂvfR&–æ6—Â&ööbÂ&V6W6P¦–&B'V–ÆF–ær&V†–æB6öÖV&öG’VÇ6Rw2†÷W6R—26Æ–Ò&÷WBF†V—"†÷W6V†öÆBâæB¢¦WfW'’Æ÷Bö`§F†R&Æö6²×W7Bæ÷r&R'V–ÇBöâÂÇ&VG’ö67W–VBÂ÷"æÖVB÷Vâv—F‚—G2&V6öæ–ær¢¢(	BF†÷6RF‡&VP§vW&R6÷VçFVB–âF‡&VRÆ6W2æBæ÷F†–ærÖFRF†VÒÖVWBÂ6òÆ÷B6÷VÆB†fR&VVâ6ÆÆVB÷Vâ–à§F†R&V6—Rv—F‚†÷W6R7FæF–æröâ—BÂv†–6‚—2fÇ6R7FFVÖVçB&÷WBF†RF÷vâ–âF†Rf–ÆRF†@¦Fö7VÖVçG2F†RF÷vââÆÂf—fR&VgW6Ç2vW&RfW&–f–VB'’6öÖÖ—GF–ærV6‚öæRFVÆ–&W&FVÇ’à ¢¢¥GvòF†–æw2F†—2&Æö6²W‡÷6VB'’æ÷B&V–ær6÷WF‚â¢¢F†Rf—6—F÷"Öf6–ærÆö6F–öâÆ–æRöâWfW'¦vVæW&FVB&V6÷&B&VB¢%6÷WF‚F—f—6–öâ"¢2Æ—FW&Â(	BG'VRöbWfW'’&V6÷&BF†B†BWfW"W†—7FV@¦æBw&öæröâÆÂ6WfVâöbF†W6RÂv†–6‚—2F†R6†RöbFVfV7BöæÇ’f—'7B66Rf–æG2âæBF†P£ccR×&ööbÆVFvW"GG&–'WFVB¢¦WfW'’æöç–Ö÷W2&ööb–âF†RvW7BF—f—6–öâFòF†RvöÆbö–çB&V6—R¢¢À¦&V6W6RVçF–ÂFöF’F†Bv2F†R6ÖR6WC¢—B&VBF†R6WfVâæWr&öög226WfVâöbF†B&V6—Rw0¦÷vâÆ6VÖVçG2VÖ—GFVB÷WBöb÷&FW"æB&VgW6VBFòFW&—fRBÆÂâ—B6÷VçG2'’F†R&öw&ÖÖR†6P¦V6‚&V6÷&BæÖW2æ÷rÂæBF†RvW7B&V6—Rw2&VÖ–æFW"†öÆG2B¢£3R¢¢ÂVæ6†ævVBÂv—F‚6WfVâvW7@§&öög27FæF–ær&W6–FR—Bà ¢¢¤öæR†÷W6V†öÆBF÷FVBÂöæR&VgW6VBÂæBF†R&VgW6Â—2&÷WBF†R'VÆR&F†W"F†âF†R&ööbâ¢¢F†P¦&Æö6²FVÇ2CæBC2(	BF†RGvòfÖ–Æ–W2BÔ&‚w2'VÆRFÖ—G2âF†RCÆör6&–â—2F÷FVC¢F†P¦Æ&÷W&W"w26÷VçB—2fÆö÷"'’—G2÷vâ6öÖÖ—GFVBFW‡BÂC—2F†RfÖ–Ç’F†—2Æ–W"†÷W6W2æ–æRö`¦—G2VÆWfVâ†÷W6VBÆ&÷W&W'2–âÂæBF†—2Æ–W"¢¦Ç&VG’Æ6W2GvòÆ&÷W&–ær†÷W6V†öÆG2–âF†P¥vW7BF—f—6–öâ¢¢Â6òæ÷F†–ær7&÷76W2F—f—6–öâÆ–æRF†R&öw&ÖÖR†Bæ÷BÇ&VG’&wVVBà¤†÷W6V†öÆG2¢£SB(i"SR¢¢ÂW'6öç2¢£“(i"“¢¢âF†RC26'VçFW"—2&VgW6VC¢'VÆRbw2GvòFW7G0¦&R6–ÆVçBöâF—f—6–öâæBÆÂVÆWfVâ6'VçFW"†÷W6V†öÆG27FæBæ÷'F‚÷"6÷WF‚Â6òGvVÆgF‚vW7@¦öbF†R&—fW"v÷VÆB&RæWr6Æ–Ò&÷WBv†W&RF†RF÷vâw26'VçFW'2Æ—fVBÂ'&—f–ær26–FP¦VffV7Böb&Æö6²&6VÂ(	BF†RW†7Bf–ÇW&RÖöFR'VÆRbW†—7G2Fò&WfVçBâ¢¥v†WF†W"F†R'VÆP§F¶W2F—f—6–öâFW7B—2æ÷r$ôDÔBÔRw2Fò6WGFÆR¢¢Âöæ6RÂ&F†W"F†âV6‚&6VÂw2FòFV6–FP¦v–ââæò‡VÖâf–wW&R—2G&vâ„Ã’ÂVæ6†ævVBà ¢22æWr##bÓ‚ÓB(	BF†R&6VÆ–æR66÷&VC¢¢£Bã‚öb¢¢ÂæBGvòöbF†RF‡&VR†VFÆ–æRçVÖ&W'2vW&RÖV7W&–ærF†Rw&öærF†–æp ¢¢¥"Ôsâ¢¢F†R66÷&VB†Æböbsã"—2–âÂæBF†R&"—Bv2ÖV7W&VBv–ç7B—2F†RöæR*s6—0¦6â7GVÆÇ’&R†VÆC¢V–v‡B†W2Â(	3Âf—fRæÖVB7FF–öç2Âw&—GFVâ§W7F–f–6F–öâÂ7V6–f–0¦f—‚f÷"WfW'’†—2VæFW"‚Âv–ç7BF†—2&ö¦V7Bw2÷vâ&VfW&Væ6R6WB(	BF†RGvVÇfR&RÖf—&P§–7F÷&–ÂÆFW2æBF†RfW&–f–VBFÆÆw&72†÷Föw&‡2(	BæBæWfW"v–ç7B6öÖÖW&6–ÂvÖP¦g&ÖRâ72—2¢¦ÖVâ(šR‚ãv—F‚æò†—2&VÆ÷rr¢¢âF†R&6VÆ–æR—2¢£Bã‚¢¢ÂæB¢¦WfW'’öæRö`§F†RV–v‡B†W2—2&VÆ÷rr¢¢âF†B—2F†RçVÖ&W"ÆFW"†6W2†fRFò&VBÂæB—B—2&V6÷&FV@¦&Vf÷&RsF÷V6†W2F†R&VæFW&W"&V6—6VÇ’6òF†BF†W&R—26öÖWF†–ærFò&VBà ¢¢¥F†R&÷Fö6öÂw2–æFWVæFVæ6R6öæF—F–öâ—26F—6f–VBæBv÷'F‚7FF–ærâ¢¢F†—2&6VÂw&÷FRæð¦6öFRBÆÂ(	Bv—BF–fbÒ×7FFf÷"—B—2F‡&VRFö7VÖVçG2æB6†ævVÆörVçG'’(	BæBF†R'Và§F†B'V–ÇBFööÇ2ö7&—F–5÷6†÷G2æÖ§6æBFööÇ2ö7&—F–5öÖWG&–72æÖ§6v2F–ffW&VçBöæRâF†P§66÷&W"&VBF†Rg&ÖW2à ¢222F†R66÷&W0 §Â7FF–öâÂÆ–v‡BÂÖFW&–ÂÂFW‡GW&RÂvVöÖWG'’ÂFÖ÷7†W&RÂ÷7BÂ6ö×÷6—F–öâÂ†—7F÷'’ÂÖVâÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â6Vvæ6†Â2Â2ÂÂRÂBÂBÂbÂrÂ¢£Bã2¢¢À§Âf—'7E÷÷7Eööff–6VÂ2ÂBÂÂbÂBÂBÂrÂ‚Â¢£Bãc2¢¢À§Â6÷WF…÷vFW&Â2Â2ÂÂ2ÂBÂBÂBÂRÂ¢£2ã3‚¢¢À§Â&—&–U÷vW7FÂRÂRÂ"ÂRÂBÂBÂbÂrÂ¢£BãsR¢¢À§Â&—fW%ö&æ¶Â"Â2Â"ÂBÂRÂ2ÂbÂrÂ¢£Bã¢¢À§Â¢¦†—2ÖVâ¢¢Â¢£2ã"¢¢Â¢£2ãb¢¢Â¢£ãB¢¢Â¢£Bãb¢¢Â¢£Bã"¢¢Â¢£2ã‚¢¢Â¢£Rã‚¢¢Â¢£bã‚¢¢Â¢£Bã‚¢¢À ¤FW6·F÷#ƒ9sƒâF†RÖö&–ÆR6WBv26GW&VBæBÖV7W&VB–âF†R6ÖR'VâæB—2¢¦æ÷@§66÷&VB¢¢(	BF†R'V'&–2—2&VF–æröbg&ÖW2æBf—fR7FF–öç2BöæRf–Ww÷'B—2v†BF†P§&÷Fö6öÂ6·2f÷#²6V6öæBf–Ww÷'Bv÷VÆBF÷V&ÆRF†R&VF–ærv—F†÷WB6†æv–ærv†–6‚†6R÷vç0¦ç—F†–ærâ6—‚7FF–öç2†6Vvæ6…÷v–ævÂÆ¶UöÖ&¶WFÂf÷&·6Âw&VVå÷G&VVÂg&öÕö&÷fVÀ¦&—&–U÷6÷WF†’vW&R&VBf÷"6öçFW‡BæBFVÆ–&W&FVÇ’æ÷B66÷&VBà ¢¢¥FW‡GW&RBãB—2F†RfÆö÷"öbF†Rv†öÆRW†W&6—6RæB—B—2æ÷B7W'&—6R¢¢(	B*s—FVÒ’6—0§F†W&R&R¦W&òFW‡GW&RÖ2öâ#CB76WG2ÂæBF†Rg&ÖW26†÷r—C¢6Æ&ö&B—2¦vVöÖWG'’¢Â§&ööb—2öæRfÆBfÇVRÂ6†–æ¶–ær—26V6öæBfÆBfÇVRÂæBF†RöæÇ’FW‡GW&R–âF÷vâg&ÖR—0§F†Rw&÷VæBâ¢¤†—7F÷&–6Â67W&7’Bbã‚—2F†R6V–Æ–ær¢¢ÂæB—B—2F†R†—2F†—2&ö¦V7B—0¦7GVÆÇ’vööBC¢Bf—'7E÷÷7Eööff–6VF†Rfö÷G&–çB—2æG&V2Gv–6R÷fW"ÂF†R÷6—F–öâ—0§7W'fW–VBÂæBF†RVç&W6öÇfVB&VG2&R6'&–VBöâF†R&V6÷&B–ç7FVBöb&V–ær&W6öÇfVB–çFòF†P¦vVöÖWG'’âF†Rv&WGvVVâãBæBbã‚—2F†R6†RöbF†—2&ö¦V7B(	BF†R&W6V&6‚—2†VBö`§F†R&VæFW&–ær'’f—fRö–çG2öâFVâ×ö–çB66ÆRà ¢222v‡’V6‚†—266÷&VBv†B—BF–BÂæBF†RöæRf—‚F†BÖ÷fW2—@ ¤WfW'’†—2—2&VÆ÷r‚Â6òWfW'’†—26'&–W2f—‚æB†6RâF†Rf—†W2&Rw&—GFVâ–çFð¦Fö72õ$ôDÔæÖFv–ç7BF†R&6VÂF†B÷vç2F†VÒà ¢¢¤Æ–v‡F–ærb6†F÷r(	B2ã"(i"sâ¢¢F†RöæÇ’67B6†F÷rÆVv–&ÆR–âF†Rf—fRg&ÖW2—2V6€¦6†–ÖæW’w2ÂöâF†R&ööb&W6–FR—BâF†RF—&V7F–öæÂÆ–v‡B67G2æBF†Rw&÷VæB&V6V—fW2Â6òF†P§6†F÷rÖ—2æ÷B7v—F6†VBöfb(	B—B—2vVöÖWG'“¢B#£3öâ§VÇ’@£Cãƒœ+âF†R7Vâ7FæG2¢£sã\+¢¢WæB6†F÷r—2¢£ã3SB9r¢¢F†R†V–v‡Böbv†BF‡&÷w2—BÂ6ð¦†÷W6Rw26†F÷rÆ–W2VæFW"—G2÷vâVfW2æBvÆ¶W"w2g&ÖR6'&–W2ÆÖ÷7Bæò6†F÷p¦–æf÷&ÖF–öââF†R66VæRæ÷FR6†÷6RF†B†÷W"FVÆ–&W&FVÇ’ÂFòÆ–v‡BF†R6÷WF‚VÆWfF–öâF†P§&V6÷&G26ÆÂv†—FRÂæBF†RG&FR—26÷VæB(	B'WB—G26÷7B†2æWfW"&VVâw&—GFVâF÷vâÂæB—B—0§F†—3¢¢¦f÷&Ò†2Fò&R6'&–VB'’6öÖWF†–ær÷F†W"F†â6†F÷rÂæBF†RGvò6æF–FFW2&R&÷F€§7v—F6†VBöfb¢¢„ò—2&¶VEöó¢fÇ6VöâÆÂ#CB76WG2Â*s—FVÒ²Vçf—&öæÖVçBÆ–v‡F–ær—0¦'V–ÇBæBæ÷B–ç7FÆÆVBÂ*s—FVÒ’âv–ç7BF†BÂ†VÖ—7†W&TÆ–v‡FB¢£"ãB¢¢VæFW"¦F—&V7F–öæÄÆ–v‡FB¢£2ã¢¢—2ãCBf–ÆÂ&F–òÂv†–6‚fÆGFVç2v†BÆ—GFÆRÖöFVÆÆ–ærF†P¦ævÆRÆVfW2â¤f—ƒ¢s–ç7FÆÇ2F†RW‡÷6VB„E$’ÂæBF†R†VÖ—7†W&RæB&÷Væ6R6öÖRDõtâ–âF†P§6ÖR6†ævR(	BF†RG&Ç&VG’w&—GFVâöâF†R&6VÂâæ÷F†–ær†W&R&wVW2f÷"Ö÷f–ærF†R†÷W"â  ¢¢¤ÖFW&–Â&VÆ—6Ò(	B2ãb(i"s"†æòÔ&ÆVæFW"†Æb’â¢¢WfW'’7W&f6R—2öæRfÆB6öÆ÷W"â&ööbÂ§v†—FWv6†VB6Æ&ö&BvÆÂÂ†WvâÆöræB—G26†–æ¶–ærÂæB6†–ÖæW’F–ffW"öæÇ’–â‡VR(	@§F†W&R—2æò&÷Vv†æW72f&–F–öâç—v†W&R–âF†RF÷vâÂ6òæ÷F†–ær&VG22–çFVBÂvVF†W&VB÷ §vWBâF†RvRÔ'Vâ&ÇVR6‡WGFW'2B6Vvæ6†6—BBF†R6ÖRfÇVR2F†RvÆ¦–ær&W6–FRF†VÒà¢¤f—ƒ¢F†RÖFW&–Â6†VWBs"w2æòÔ&ÆVæFW"†Æb—2Ç&VG’66÷VBFòw&—FR(	Bv†–6‚7W&f6W2W†—7BÀ§v†BV6‚—2ÖFRöbÂæBv†–6‚&6†WG—R&ÖWFW"6VÆV7G2—Bâ  ¢¢¥FW‡GW&RFWF–ÂbF–Æ–ær(	BãB(i"s"â¢¢¦W&òFW‡GW&RÖ2öâ#CB76WG3²F†Rw&÷VæB—2F†RöæÇ§FW‡GW&VB7W&f6R–âF÷vâg&ÖRæB—G2æV"f–VÆB—2w&¦–ærÖævÆR6ÖV"âF†R†—26ææ÷@§&—6RVçF–Âs"w2&¶R†ÆbÆæG2â¤f—ƒ¢s"Â&÷F‚†ÇfW3²æ÷F†–ærVÇ6RÖ÷fW2F†—2â  ¢¢¤vVöÖWG&–2FWF–Âb6–Æ†÷VWGFR(	BBãb(i"s"õs2ÂæBöæR—FVÒf÷"ÆæR"â¢¢Ö76–ær—2vööB(	BF†P¦6Vvæ6†VÆÂæB¶æVRvÆÂÂf—'7E÷÷7Eööff–6Vw2VfR÷fW&†æræBÆörVæG2Â&—fW%ö&æ¶w0¦6÷&Fw&72(	BæB÷Væ–æw2&Rv†W&RF†R6–Æ†÷VWGFRf–Ç3¢æò&WfVÂÂæò6–ÆÂÂæò66‚Âæò×VçF–à¦ç—v†W&R–âF†R6WBÂ6òF†RbÖ÷fW"Ób&‡—F†ÒF†Rw&VVâG&VRÆFRFö7VÖVçG2FöW2æ÷BW†—7BâF†P§v÷'6Rf–ÇW&R—2B6÷WF…÷vFW&ÂæB—B—2¢¦FF¢¢f–ÇW&R&F†W"F†â&VæFW&–æröæS¢F†P¦†÷&—¦öâ&÷röbF†R'W6–æW727G&VWB—2öæRv&ÆR7F×VBF÷¦VâF–ÖW2BWfVâ76–ærÂv†W&RF†P§&W6V&6‚¶æ÷w27F÷&RÂâV7F–öâ&ööÒÂGvòæWw7W"öff–6W2æBv&V†÷W6Râ¤f—ƒ¢÷Væ–æw2Fð¥s2w26vRv÷&²æBs"w2&×3²F†R&WVFVB7F×FòÆæR"(	BF†Ræöç–Ö÷W2Æ6V†öÆFW"Ö76–æp¦æVVG2W"×&V6÷&Bf&–F–öâ–âv–GF‚Â—F6‚æBVfR†V–v‡BG&vâg&öÒF†RfÖ–Ç’&æB—BÇ&VG¦6'&–W2â  ¢¢¤FÖ÷7†W&R(	BBã"(i"sBâ¢¢F†R6·’—26Æ÷VFÆW72w&F–VçBBWfW'’7FF–öâÂæBF†R#(	3SÐ¦&æB†öÆG2æ÷F†–ærf÷"F†R†¦RFò7BöâÂ6òF†Rf"G&VVÆ–æRÖVWG2—G26·’v—F‚æò6W&F–öà¦Bf÷W"öbF†Rf—fRâF†RöæRÆ6R—Bv÷&·2—2&—fW%ö&æ¶Âv†W&RF†Rf"6†÷&RvVçV–æVÇ§&V6VFW2(	BF†R##bÓ‚Ó2f"×F–Ö&W"f—‚—2f—6–&ÆR–âF†Rg&ÖRâ¤f—ƒ¢sBÂ—FV×2(	3bÂÇW26·§F†B—2æ÷B6–ævÆRw&F–VçBâ  ¢¢¥÷7B×&ö6W76–ær(	B2ã‚(i"sRâ¢¢FöæRÖ–æræBæ÷F†–ærVÇ6Râf—6–&ÆR7F—"×7FW–æröâF†P¦6Vvæ6†&–FvRæBÆöærF†RvFW"÷fVvWFF–öâ&÷VæF'’B&—fW%ö&æ¶Âv†W&RF†RvFW"ÆæP¦Ç6ò6†÷w2&V7FæwVÆ"7FW–ærv–ç7BF†RVÖW&vVçB7FæBâ¤f—ƒ¢sRw24Ô72ÂæB"Ô%Ts—0¦–âF†R6ÖRg&ÖRâ  ¢¢¤6ö×÷6—F–öâ(	BRã‚(i"F†Ræ6†÷'2Âæ÷B†6Râ¢¢f÷W"öbF†Rf—fR7FF–öç2g&ÖRF†V—"7V&¦V7@¦†öæW7FÇ’â6÷WF…÷vFW&FöW2æ÷C¢cRöb—G2g&ÖR—2f÷&Vw&÷VæBw&72æBF†R'W6–æW727G&VW@¦—B—2æÖVBf÷"—2C×—†VÂ&æBöâF†R†÷&—¦öâââæ6†÷"f—6—F÷"—2öffW&VB6†÷VÆB6†÷rF†P§F†–ær—B—2æÖVBgFW"â¤f—ƒ¢6÷WF…÷vFW&w2æ6†÷"–âFF÷66VæW2óƒ3Ræ§6öævçG2÷6—F–öà¦öâF†R7G&VWB&F†W"F†â–âF†Rf–VÆB6÷WF‚öb—B(	BöæR&V6÷&BÂæò6öFRÂæB—B—2F†R6†VW7@§ö–çBöâF†—2v†öÆRF&ÆRâ  ¢¢¤†—7F÷&–6Â67W&7’(	Bbã‚(i"Ö÷7FÇ’V&æVBÂöæR&VÂFVGV7F–öââ¢¢f—'7E÷÷7Eööff–6V66÷&W2ƒ ¦Wf–FVæ6Rfö÷G&–çBÂ7W'fW–VB÷6—F–öâÂVç&W6öÇfVB&VG26'&–VBöâF†R&V6÷&BâF†RFVGV7F–öâ—0¦B6÷WF…÷vFW&ƒR’f÷"F†R6ÖR&WVFVB7F×(	BVæ–f÷&Ö—G’F†Bæò6÷W&6R6Æ–×2ÂVæFW'7FF–æp§v†BF†R&W6V&6‚¶æ÷w2(	BæBB&—&–U÷vW7Fƒr’f÷"F†RfÆ÷vW"ÆöBâ¢¤4õ%$T5DTB##bÓ‚ÓP¦'’"ÕsF2†“¢F†R'Gvò÷&FW'2öbÖvæ—GVFR"F†—2&w&‚W6VBFò6Æ–Òv2ÖV7W&VÖVçBW'&÷"À¦æB—Bv2Œ9rFöò&–râ¢¢ã&—2v†BF†RfÆ÷vW"ÖÆöB&V6—R&W÷'G2ÂæBF†B&V6—RÖ—76W0£“BãRRöbF†R&ÆööÒBF†—27FF–öâ(	B—G2‡VR7WBBS+WG2–VÆÆ÷r6öæVfÆ÷vW"–âv—F‚F†P¦w&72âÖV7W&VB'’†–F–ærF†RfÆ÷vW"†VG2æB7V'G&7F–ærÂF†R&VæFW"w2G'VR&ÆööÒ†W&R—0¢¢£"ã’R¢¢öb‡VVBw&÷VæBâv–ç7BF†RN(	3bRF&vWBF†B—2f7F÷"öbGvòFòF‡&VRÂv†–6‚—0§7F–ÆÂ&VÂFVGV7F–öâæB7F–ÆÂæ÷Bf—†VBâ&VB$ôDÔ"ÕsF2†’&Vf÷&RV÷F–ærV—F†W"çVÖ&W"(	@¦–â'F–7VÆ"ÂF†RN(	3bRF&vWBv2—G6VÆbFW&—fVBv—F‚F†R&Æ–æB&V6—RæB—2¢¦æ÷B–WBöâF†P§6ÖR66ÆR¢¢2F†R"ã’Râ¤f—ƒ¢"ÕsF2†"’f÷"F†RfÆ÷vW"ÆöBÂv†–6‚×W7B&RÖFW&—fRF†RF&vW@¦f—'7C²ÆæR"f÷"F†R7F×â  ¢222F†RF‡&VRf–æF–æw2F†B&Ræ÷B66÷&W0 ¢¢£âGvòöbF†RF‡&VRçVÖ&W'2*s—FVÒr&W7G2öâ&RÖV7W&–ærF†R6æ÷’Âæ÷B6†F÷râ¢¢F†P¦&6VÆ–æR&V6÷&FVB'6†F÷w27F–ÆÂ6Æ—FòÆ—FW&Â&Æ6²(	B"Ãc2W&RƒÃÃ–—†VÇ2@¦&—fW%ö&æ¶ÂÃRBf—'7E÷÷7Eööff–6V"æBF&¶W7Bw&÷VæBFV6–ÆR2Æ÷r2¢¤Âã“2¢¢à¤&÷F‚&R&VÂÖV7W&VÖVçG2æB&÷F‚&RGG&–'WFVBFòF†Rw&öær7W&f6Râ6öææV7FVB6ö×öæVçG2ö`§F†RÆ—FW&ÂÖ&Æ6²Ö6²Âv—F‚F†V—"&÷VæF–ær&÷†W3  §Â7FF–öâÂÆ—FW&Â&Æ6²Â6ö×öæVçG2Âöb—B–â6ö×öæVçG2Ç––ær¢¦VçF—&VÇ’&÷fR¢¢F†RÖVF–âÆæB÷6·’&÷rÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Âf—'7E÷÷7Eööff–6VÂÃRÂ’Â¢£R¢¢†Æ&vW7B‚Ã3sb‚Âƒ“S~(	3CB“C.(	3r(	BF†R7&÷vâBF÷&–v‡B’À§Â&—fW%ö&æ¶Â"Ãc2ÂBÂ¢£“BR¢¢‡6—‚7&÷vâ6ÇW7FW'2ÂÆÂ’(šB#3Â&÷VæF'’&÷r3c’’À§Â&—&–U÷6÷WF†Â"Ã3RÂÂ¢£“’ãrR¢¢†ÆÂ’(šB#cÂ&÷VæF'’&÷r3“R’À§Â6Vvæ6…÷v–ævÂcÂÂ¢£R¢¢†öæR7&÷vâVFvR’À ¤æ÷BöæRÆ—FW&ÂÖ&Æ6²—†VÂ–âF†RFW6·F÷6WB—2öâ6†FVBw&÷VæBâF†W’&RF†R6†FVB6–FRö`§F†RæV"×G&VR6æ÷’(	BF†RF–Ö&W&ÖW6…7FæF&DÖFW&–ÆÂfW'FW‚Ö6öÆ÷W&VBÂVçF—6–ærFò¦W&ð§v†W&RÆVbf6W2v’g&öÒsã\+7VââF†RF&¶W7BÖFV6–ÆRf–wW&R—2F†R6ÖR7W&f6R&V6†V@¦6V6öæBv“¢F†RÖWG&–2f–æG2&w&÷VæB"2WfW'—F†–ær&VÆ÷rF†RW"Ö6öÇVÖâÆæB÷6·’Æ–æRÂæB–à¦6öÇVÖâ6''––ærG&VRF†BÆ–æR—2F†R§F÷öbF†R7&÷vâ¢Â6òF†R7&÷vâ6÷VçG22w&÷VæBà¤ÖV7W&VBB&—fW%ö&æ¶¢¢£c2Ãs—†VÇ2BÂÂ"Âöbv†–6‚“RãrRÆ–R&÷fRF†RÖVF–âÆæB÷6·§&÷r¢£²F†RFV6–ÆRööÂ—2ãSRÃÂ6òF†RÂã“2&VF–ær—26æ÷’ÖV7W&VÖVçBVæBFòVæBà¦6÷WF…÷vFW&“"ãrRÂf—'7E÷÷7Eööff–6Vƒ‚ãbRâ¢¦6Vvæ6…÷v–ævæBÆ¶UöÖ&¶WF&RF†P¦W†6WF–öç2¢¢(	BF†V—"æV"Ö&Æ6²—2“(	3“BR¦&VÆ÷r¢F†B&÷ræB—2F–ffW&VçB÷VÆF–öâÂæ÷@¦F–væ÷6VB†W&Rà ¤6öç6WVVæ6RÂæB—B6†ævW2v†BsFöW3¢¢§&—6–ærF†R6†F÷rfÆö÷"v–ÆÂæ÷BÖ÷fRV—F†W ¦çVÖ&W"â¢¢v†BÆ–v‡G2ÆVbf6–ærv’g&öÒF†R7Vâ—2F†RVçf—&öæÖVçBFW&ÒsW†—7G2Fð¦–ç7FÆÂÂ÷"fÆö÷"öâF†R7&÷vâw2F&¶W7BÆ&VFòâF†Rf—‚7F—2–âs²F†RÖV6†æ—6ÒæÖVB–à¬*s—FVÒrFöW2æ÷B7W'f—fRà ¢¢£"âF†R†÷&—¦öâ×F–Ö&W"ÖWG&–26ææ÷BFVÆÂG&VVÆ–æRg&öÒF÷vç66RÂæBF†RF÷vâ§W7BÖ÷fV@¦—Bâ¢¢F†R&V6—R6÷VçG2†÷&—¦öâ6öÇVÖâ2F–Ö&W&VB–bç’—†VÂ–âF†R&æB&÷fRF†RÆæB÷6·¦Æ–æRfÆÇ22ÇVÖ&VÆ÷rÂ÷"2~(‰$"&÷fRÂF†R6·’W‡G&öÆFVBg&öÒF†R#&÷w2÷fW"—Bâv&ÆP¦VæB'&V¶–ærF†R6·–Æ–æR6F—6f–W2F†B27W&VÇ’2âö²â&R×'Vææ–ærF†R†&æW72öâFöF’w0¦FWf(	Bv—F‚¢¦æò&VæFW&W"6†ævR6–æ6RF†R&6VÆ–æR¢¢†v—BF–fbÒ×7FB#ƒ&FC–âä„TBÒÐ§&VæFW&W'2ö—26†ævVÆöræ§6ÂCÆ–æW2ÂæBæ÷F†–ærVÇ6R’(	Bæ–æR7FF–öç2&W&öGV6RF†V—"F–Ö&W ¦f–wW&W2æB¢¦&—&–U÷6÷WF†Ö÷fW2g&öÒã3cBFòãC3bÆÂòã3CFòãCC6VçG&R¢¢Â#P¦v–ââv†B6†ævVB&WGvVVâF†RGvò'Vç2—2’æöç–Ö÷W2&öög2…BÔ"æBBÔ2’ÂæBF†Rg&ÖP§6†÷w2F†VÓ¢F†RÆVgBF†—&Böb&—&–U÷6÷WF†w26·–Æ–æR—2w&W’v&ÆRVæG2â¢¥F†R*rRF&vWBö`®(šR“R†÷&—¦öâF–Ö&W"6÷fW&vR6âF†W&Vf÷&R&R6F—6f–VB'’'V–ÆF–ærF†RF÷vâ¢¢Âv†–6‚—2æ÷@§v†B—FVÒRv2WfW"&÷WBâ"ÕsB÷vç2F†RF&vWC²—BæVVG2F—67&–Ö–æF÷"Â÷"6V6öæBÖWG&–0§F†BÖV7W&W2öæÇ’6öÇVÖç2v—F‚æò7G'V7GW&R–âF†VÒÂ&Vf÷&R—G266WFæ6RçVÖ&W"ÖVç0¦ç—F†–ærà ¢¢£2âÆæR"—27VæF–ærF†RG&rÖ6ÆÂ'VFvWBf7FW"F†âÆæR6â&V6÷fW"—Bâ¢¢¢¥$U4ôÅdT@£##bÓ‚ÓR'’"ÕsV(	B6VRF†RF÷öbF†—2f–ÆRâ¢¢F†R³v2æWrÖFW&–Âu$õU2ÂF†Rw&÷wF€§FW&Ò—2æ÷r¦W&òÂæBæò7FF–öâ—2÷fW"'VFvWBBV—F†W"f–Ww÷'BâF†R&VF–ær&VÆ÷r—2¶WB0§F†RÖV7W&VÖVçBF†Bf÷VæB—Bâ6ÖRGvò'Vç2À§6ÖR&VæFW&W"Â³’7G'V7GW&R&V6÷&G2ƒ#C"(i"#cÂ³rã’R“  §ÂÂ6Vvæ6†Â2væ6…÷v–ævÂÆ¶UöÖ&¶WFÂe÷÷7Eööff–6VÂf÷&·6Âw&VVå÷G&VVÂ6÷WF…÷vFW&Âg&öÕö&÷fVÂ&—&–U÷6÷WF†Â&—&–U÷vW7FÂ&—fW%ö&æ¶À§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§ÂFW6·F÷&6VÆ–æRÂcRÂcbÂs‚ÂcbÂƒrÂ“ÂƒRÂcrÂs2Â“rÂSbÀ§ÂFW6·F÷FöF’ÂcRÂsrÂƒ’ÂcbÂ“‚Â"Â“bÂcrÂƒBÂ‚ÂSbÀ§ÂÖö&–ÆR&6VÆ–æRÂc"Âc2ÂcbÂcÂƒ"Âƒ‚Âƒ2ÂcÂsÂ“BÂC’À§ÂÖö&–ÆRFöF’Âc"Âs"ÂsrÂcÂƒ"Â“’Â“BÂcÂƒ"ÂRÂC’À ¢¢¤W†7FÇ’³FW6·F÷B6WfVâöbVÆWfVâ7FF–öç2æBW†7FÇ’BF†R÷F†W"f÷W"¢¢(	Bæ@§G&–ævÆW2&÷6R'’öæÇ’#CN(	3Sc"Â6òF†—2—2W"Öö&¦V7B6÷7BÂæ÷BvVöÖWG'’â7FF–öç2÷fW"F†P¢¢®(šBƒ¢¢'VFvWBvò¢£B(i"b¢¢öâFW6·F÷æB¢£B(i"R¢¢öâÖö&–ÆS²F†Rv÷'7BvöW2“r(i"‚âF†P§Væ–f÷&Ö—G’—2F†R'Bæö&öG’†2W‡Æ–æVC¢³B&V&–æw2S+'BÂæB³Bg&öÕö&÷fVÀ§v†–6‚6VW2F†Rv†öÆRF÷vââ¢¥7G&–v‡BÖÆ–æRW‡G&öÆF–öâöâF†R&VÖ–æ–ærCB&öög2—2&÷W@¢³#CG&r6ÆÇ2¢¢v–ç7B'VFvWBöbƒâF†B—2æ÷B&V6öâFò6Æ÷rÆæR"F÷vâ(	BF†R&öög0¦&RF†R&öGV7B(	B'WBF†R'VFvWB6ææ÷B&RÖWB'’GVæ–ærgFW"F†Rf7BÂæB"ÕsR6†÷VÆBG&V@¦&F6†–ær2—G2f—'7BVW7F–öâ&F†W"F†â—G2Æ7BâF†Rg&öÕö&÷fV¦W&ò—2ÆVC¢6öÖWF†–æp¦Ç&VG’G&÷2F†W6Rö&¦V7G2BF—7Fæ6Rà ¢222v†BF†—2FöW2æ÷BFð ¤—B6†ævW2æò6öFRÂÖ÷fW2æò'V–ÆF–æræB&RÖÖV7W&W2æò&VfW&Væ6R†÷Föw&‚âF†R*sRF&vWG0§F†BvW&R6WBg&öÒF†RVæ6öÖÖ—GFVB##bÓ‚Ó7vVW7F–ÆÂæVVB&RÖæ6†÷&–ær'’ÖV7W&–ær§&VfW&Væ6RÆFRF‡&÷Vv‚FööÇ2ö7&—F–5öÖWG&–72æÖ§6Âv†–6‚—27F–ÆÂöæRÖÆ–æR¦ö"æB—27F–ÆÀ¦æ÷BFöæRâæB'V'&–266÷&R—2öæR&VFW"w2§VFvVÖVçBv—F‚—G2&V6öæ–ærGF6†VB(	BF†Rf—†W0¦&VÆ÷r&RF†RGW&&ÆR†ÆbÂæ÷BF†RçVÖ&W"à ¢22æWr##bÓ‚ÓB(	BGvò&öög2öbFVâv—fVââö67WçBÂæBF†R'VÆRF†B&VgW6VBF†R÷F†W"V–v‡@ ¢¢¥BÔ&‚â¢¢F†R&6VÂv2W‡V7FVBFò&wVR&÷WBF†RF÷vâw2G&FRÖ—‚âv†B—Bf÷VæB—2F†B¦&Æö6²&6VÂWG2FVâGvVÆÆ–æw2öâF†RÆBf7FW"F†âç’7V6‚&wVÖVçB6âÖ÷fRÂ6òF†P§VW7F–öâF†BÖGFW&VBv2¢§v†ò—2ÆÆ÷vVBFò7F'BöæR¢¢âF†Rö67WF–öâ6Vç7W2—26Æ–Ò&÷W@¤6†–6vò(	B2Ã#cRV÷ÆR–â3“‚GvVÆÆ–æw2Â6Æ–'&FVBv–ç7BæG&V2w2ƒ32&÷7FW"(	BæB6Vç7W0§F†Bw&÷w2WfW'’F–ÖR6öÖV&öG’G&w26÷GFvR—26Vç7W2f—GFVBFòF†RÖöFVÂâGvòö`¦&Æµ÷&æFöÇ…÷vVÆÇ6w2FVâ&öög2&RF÷FVB–çFòF†R–æfW'&VBÖ†÷W6V†öÆBÆ–W#²F†R÷F†W"V–v‡@§7F’æöç–Ö÷W26÷VçB×Væ—G2Âv†–6‚—2v†BF†W’Ç&VG’vW&Rà ¢¢¥F†R'VÆRæ÷rÆ—fW2–âF†R†÷W6V†öÆB&öw&ÖÖRw2÷vâÖWF†öFÆ—7B¢¢Âv†W&RF†RæW‡B&6VÂv–ÆÀ§&VB—Bâ&Æö6²&ööbÖ’&RF÷FVBöæÇ’v†W&R$õD‚FW7G273¢F†RG&FRw26öÖÖ—GFVB&wVÖVç@§7FFW2–â—G2÷vâFW‡BF†B—G26÷VçB—2¢¦fÆö÷"&F†W"F†â&÷VæB¢¢ÂæBF†R&ööbw2fÖ–Ç’—0¦öæRF†—2Æ–W"¢¦Ç&VG’†÷W6W2F†BG&FR–â¢¢à ¢Ò¢¥GvòöbGvVçG’Öæ–æRG&FW272F†Rf—'7BFW7B¢¢(	BF†R6'VçFW"‚¢'F†R6†÷6÷VçB—2fÆö÷ ¢VæFW"F†RG&FRÂæ÷BÖV7W&Röb—B"¢’æBF†RÆ&÷W&W"‚¢'7F–ÆÂ6ÖÆÂg&7F–öâöbv†B2Ã#cP¢V÷ÆR–×Æ–W2"¢’âWfW'—F†–ærVÇ6R7FFW26V–Æ–ær(	BF†RÆ7FW&W"w2æBF†RG&÷fW"w26’¢&æ@¢æòÖ÷&R"¢÷WG&–v‡B(	B÷"—2&÷VæFVB'’v÷&·6†÷÷"7F÷&RfÖ–Ç’w2&ööbF&vWBâGvò&Vç@¢gW'F†W"ÖF6†W2&RfÇ6R÷6—F—fRv÷'F‚æÖ–æs¢¦fÆö÷"¢V'2–âF†RÆVæG&W72æ@¢&ö&F–ærÖ†÷W6RÖ¶VWW"VçG&–W2öæÇ’–ç6–FRF†RæG&V2V÷FF–öâ¢'v—F‚F†RfÆö÷"6÷fW&V@¢&W6–FW2"¢à¢Ò¢¥F†R6V6öæBFW7BÂÖV7W&VBv–ç7BF†RÆ–W"2—B7FæG2Â–6·2F†R6ÖRGvòfÖ–Æ–W2â¢¢ÆÂ€¢öbF†RÆ–W"w2F÷FVBÆ&÷W&–ær†÷W6V†öÆG2Æ—fR–âCæB’öb—G26'VçFW'2–âC2(	@¢æBCÆör6&–âæBC2öæR×&ööÒ6÷GFvR&RGvòöbF†R6WfVâGvVÆÆ–æw2F†—2&Æö6²FVÇ2à¢F†RFW7G2vW&RFW&—fVB–æFWVæFVçFÇ’æBw&VVBöâF†Rf—'7B&Æö6²F†W’vW&RÆ–VBFòÂv†–6€¢—2F†RöæÇ’&V6öâFòG'W7BV—F†W"öbF†VÒà¢Ò¢¤†÷W6V†öÆG2S"(i"SBÂW'6öç2ƒ‚(i"“ÂF÷FVBæöç–Ö÷W2&öög2ƒ2(i"ƒRÂ7FæF–ær&öög0¢Væ6†ævVBB#Sâ¢¢F†—2&6VÂ'V–ÇBæ÷F†–ærÂÖ÷fVBæ÷F†–æræB&Vw&FVBæ÷F†–ærâF†RGvð¢&öög2r&W6Væ6RÂ÷6—F–öâæBfö÷G&–çB&RW†7FÇ’2–çfVçFVBgFW"F†RF÷F–öâ2&Vf÷&R—C°¢v†BF†W’v–â—2â&wVVBö67WçB–ç7FVBöb&Ææ²â&V6÷&FVB2¢¤Ã“B¢¢à¢Ò¢¥F†RƒæBƒ"†÷W6W2&RF†R&VgW6Âv÷'F‚¶VW–ærâ¢¢F†R66†VGVÆRÆÆ÷w2‚Æ&vW"†÷W6W2æ@¢BÖW&6†çB÷"&öfW76–öæÂ†÷W6W2–âF†Rv†öÆRF÷vâÂæBF†V—"ö67WçG2&RF†RÖ÷7BÆ–¶VÇ¢V÷ÆR–âF†—2FF6WBFò&RæÖV&ÆRâ–çfVçF–ærâæöç–Ö÷W2ÖW&6†çB–çFòöæRv÷VÆB'&V²F†P¢&öw&ÖÖRw2÷vâ'VÆRæWfW"Fò–æfW"W'6öâv†W&RFö7VÖVçFVBöæR—2f–Æ&ÆRâF†÷6RGvòvç@¢BÔ“2w2G&VFÖVçB(	B&VF–æröbF†R&V6÷&B(	BæBæ÷BG&rg&öÒ6Vç7W2à¢Ò¢¥F†RF÷F–öâ—2WF†÷&VBöæ6RæBvFVB–â&÷F‚F—&V7F–öç2â¢¢FööÇ2övVæW&FUö&Æö6µö–æf–ÆÂç– ¢æ÷r&VG2F†R†÷W6V†öÆBÆVFvW"F‡&÷Vv‚FööÇ2ö–æfW'&VEöö67Wæ7’ç–ÂW†7FÇ’2F†RF‡&VP¢V&Æ–W"æöç–Ö÷W2&6VÇ2FòÂ6òæòvVæW&FVB&V6÷&B—2†æBÖVF—FVBæBF†RG&–gB6†V6²F†@¢Ö¶W2F†W6R&6VÇ2G'W7Gv÷'F‡’7F–ÆÂ&–æG2â†÷W6V†öÆBö–çFVBBâæ6–ÆÆ'’&ööbf–Ç2'¢æÖR(	B–&B'V–ÆF–ær6W'fW2F†RÆ÷B—B7FæG2&V†–æBÂæBæö&öG’Æ—fW2–â&—g’(	BæB&öö`¢F†RÆVFvW"æÖW2F†Bæò&V6—R'V–ÆG2f–Ç2'’æÖRâ¢¥fW&–f–VB'’Fö–ærV6‚â¢ ¢Ò¢¥v†B—B6‡W&æVBæBF–Bæ÷Bf—‚Â&V6÷&FVB2$ôDÔ³#â¢¢FF–ærGvòV÷ÆR&VæÖVB¢£#Rö`¢F†R“B¢¢&V6öç7G'V7FVB&W6–FVçG2âF†R–çfVçFVBÖæÖRÆÆö6F÷"FVÇ2æÖW2&÷VæBV6‚ööÂ'¢–æFW‚v—F†–â'V6¶WBÂ6òâ–ç6W'F–öâ6†–gG2WfW'–öæRgFW"—Bâæòw&FRÖ÷fVBæBWfW'’æÖP¢&RÖFW&—fW2VæFW"ÒÖ6†V6¶Â'WBF†RvVæW&F÷"w2÷vâFö77G&–ær6—2F†R76–væÖVçB—2gVæ7F–öà¢öbW'6öâw2–Bv†Vâ—B—2gVæ7F–öâöbF†Rv†öÆR÷VÆF–öâ(	BæBWfW'’gWGW&R&Æö6²&6VÀ¢v–ÆÂ&Ww&—FRV'FW"öbF†RF÷vâw2–çfVçFVBæÖW226–FRVffV7BVçF–ÂF†B—2f—†VBà ¢¢¤vFW3¢¢¢FööÇ2ö6†V6²ç6†w&VVã²æöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6w&VVâB3“9ssƒæB#ƒ9sƒÀ§¦W&òvRW'&÷'2Â'Vâv–ç7BF†R6÷W&6RG&VRæBv–âv—F‚Ò×V&Æ—6†VFà ¢22æWr##bÓ‚ÓB(	B&Æö6²f–ÆÆVB–âÂæBF†RF&ÆRæ÷F†–ær†BWfW"&V@ ¢¢¥BÔ"â¢¢&Æµ÷&æFöÇ…÷vVÆÇ6(	B&æFöÇ‚ÂÆ6ÆÆRÂv6†–æwFöâÂvVÆÇ2(	B7FööBV×G’æBæ÷p¦6'&–W2¢§FVâæöç–Ö÷W2&öög2¢£¢6WfVâ&–æ6—Â'V–ÆF–æw2öâ6WfVâöb—G2V–v‡BÆ÷G2ÂF‡&VR–&@¦'V–ÆF–æw2öfbF†RÆÆW’ÂFòF†RfÖ–Ç’Ö—‚F†RccR×&ööb66†VGVÆR÷'F–öæVB—BâF†RF÷vâ7FæG0¦B¢£#C"&öög2öbccR¢£²C#2&VÖ–âæB¢£“RöbF†÷6R†fRÖöFVÆÆVBw&÷VæB¢¢âöæRÆ÷B—2ÆVg@¦&&RöâW'÷6RÂæBv†–6‚Æ÷B—2&&—G&'’(	B&V6÷&FVB27V6‚–â¢¤Ã“"¢¢Âv—F‚F†Rg&öçFvP¦&wVÖVçB†Æ&vW"†÷W6W2Fò&æFöÇ‚Â&÷Vv†W"GvVÆÆ–æw2Fòv6†–æwFöâ’w&—GFVâF÷vâ6ò—B6â&P¦F—6w&VVBv—F‚à ¢¢¥F†R&6VÂWF†÷'2æò6ö÷&F–æFW2ÂæBF†B—2F†RGW&&ÆR†Æbâ¢¢F†RF‡&VRV&Æ–W"–æf–ÆÀ§&6VÇ2V6‚†æB×w&÷FRF†V—"÷vâV7F–æw2æBæ÷'F†–æw2Â&V6W6RF†RÆBÖöGVÆRF–Bæ÷BW†—7@§v†VâF†W’vW&Rw&—GFVââFööÇ2övVæW&FUö&Æö6µö–æf–ÆÂç–&VG2WfW'’ÖWG&RöfbF†R6öÖÖ—GFVBÆ÷@§öÇ–vöç2öbF†R³rw&–C¢F†R&V6—R6—2v†–6‚fÖ–Ç’7FæG2öâv†–6‚Æ÷BÂv†WF†W"—Bg&öçG2F†P§7G&VWB÷"F†RÆÆW’ÂæB†÷rf"&6²âF†RFVfV7B6Æ72³rW‡÷6VB(	B6WfVâ'V–ÆF–æw27FæF–ær–à§F†RÖ–FFÆRöbF†R&öBÂWBF†W&R'’&V6—RF†B†BæWfW"6¶VBv†W&RF†R&öBv2(	B—2æ÷p§&WF—&VB'’6öç7G'V7F–öâ&F†W"F†â'’vFR6F6†–ær—BgFW'v&G2âF†RvFR7F–ÆÂ'Vç3¢F†P¦vVæW&F÷"FW7G2WfW'’fö÷G&–çBv–ç7B—G2÷vâÆ÷BÆ–æW2ÂF†RÆGFVB6÷'&–F÷'2ÂWfW'’÷F†W ¦fö÷G&–çB–âF†RFF6WBÂF†R†V–v‡Ff–VÆBæBF†R&6†WG—RÂ&Vf÷&R—Bw&—FW2f–ÆRà ¢¢¤F&ÆRF†—2&ö¦V7B†B&VVâ6''––æræBæWfW"&VF–ærâ¢¢fÖ–Ç•ö&æG5ögF–âF†R'V–ÆF–æp¦–çfVçF÷'’†2&æG2f÷"#öbF†R&öw&ÖÖRw23RfÖ–Æ–W2âF†R÷F†W"B(	B¢¤ƒÂƒ"Âƒ2Â3BÀ¥CÕC2ÂsRÂc2ÂcBÂ“Ô“2ÂÓ¢¢(	B†BæöæRÂ6òF†RV&Æ–W"vVæW&F÷'26÷VÆBöæÇ’'V–ÆBF†P¦fÖ–Æ–W26öÖV&öG’†B6W&FVÇ’&WG—VB–çFò—F†öâÂv†–ÆRF†R66†VGVÆRvVçBöâ÷'F–öæ–ærƒ¦æBƒ"Fò&Æö6·2âƒ3UöfÖ–Ç•ö&6†WG—Uö7&÷77vÆ²æ§6öæ†2†VÆBF†Rfö÷G&–çB&æBÂ7F÷&W¦6÷VçBÂVfR†V–v‡BæBÆ6V†öÆFW"&6†WG—Rf÷"¢¦ÆÂ3R¢¢F†Rv†öÆRF–ÖRÂæBw&VW2v—F€¦fÖ–Ç•ö&æG5ögFöâWfW'’öæRöbF†R#F†W’6†&RâF†RvVæW&F÷"&VG2F†R7&÷77vÆ²â¢¤ƒæ@¤ƒ"7FæBf÷"F†Rf—'7BF–ÖR¢¢ÂæBæò&æB—2&WG—VBç—v†W&Rà ¢¢¤öæRçVÖ&W"v2Ö÷fVBFòf—Bâ&6†WG—RÂæB—B—2w&—GFVâF÷vââ¢¢F†R2&—g’w2WF†÷&V@¦VfR&æB'Vç2bÓrgBæB—G2&÷GFöÒ—2&VÆ÷rv†BF†R÷WF'V–ÆF–ær&6†WG—RæVVG2Fò6''’—G0¦÷vâFö÷"ÇW2†VFW"(	B&VgW6VB'’æÖRBãƒ“ÒâF†R6×ÆR—2æ÷rG&vâg&öÒF†R'BöbF†P¦WF†÷&VB&æBF†R&6†WG—R6â'V–ÆBƒ"ãrÒÂ&W6–FR†6RöæRw2&—f–W2B"ãR’ÂæBfÖ–Ç§v†÷6Rv†öÆR&æB6—G2VæFW"F†BfÆö÷"f–Ç2Æ÷VFÇ’&F†W"F†â&V–ærV–WFÇ’&—6VB÷WBöb—G0§G—öÆöw’à ¢¢¤æB6öÖÖæBF†BV–WFÇ’FW7G&÷–VBæ–v‡Bw2&ÆVæFW"v÷&²Âf÷VæB'’'Vææ–ær—Bâ¢ ¦vVæW&F÷'2ö–æfW'&VE÷Æ6V†öÆFW"ç–'V–ÆG2F†RfÆvvVBÆ6V†öÆFW"Ö76–ærf÷"æWræöç–Ö÷W0§&V6÷&Bâ—G2ÒÖ6†V6¶F‚†27FööB6–FR6–æ6R##bÓ‚Ó2f÷"ç’76WBF†R6æöæ–6Â&¶R†0§7WW'6VFVB(	B¶–æC¢vVæW&FVF–âF†RÖæ–fW7B(	Bf÷"F†R7FFVB&V6öâF†BFVÖæF–ærF†P§Æ6V†öÆFW"'—FW2&6²v÷VÆBf÷&&–BF†RWw&FRF†R&¶RW†—7G2FòW&f÷&Òâ¢¤—G2%T”ÄBF‚F–@¦æ÷Bâ¢¢'Vâöæ6Rf÷"FVâæWr&V6÷&G2Â—BÇ6ò&Ww&÷FRF†R#‚Ç&VG’Ö&¶VBöæW3¢2´"ö`¦6æöæ–6Â&6†WG—RvVöÖWG'’F÷vâFòBã’´"fÆvvVB&÷‚V6‚Âv—F‚F†V—"Öæ–fW7BVçG&–W0§7F×VB&6²Fò¶–æC¢Æ6V†öÆFW&6òæ÷F†–ærF÷vç7G&VÒ6÷VÆBFVÆÂF†RF–ffW&Væ6Râ—B&W&öGV6W0¦öâ6ÆVâFWf6†V6¶÷WBÂ6ò—B—2æ÷BÆö6Â66–FVçBà ¢¢¤WfW'’vFR7F–VBw&VVâF‡&÷Vv‚—B¢¢Âv†–6‚—2F†R'Bv÷'F‚¶VW–ærâÆ6V†öÆFW"F†@¦ÖF6†W2—G2&V6÷&B—2&V6—6VÇ’v†BF†RvFW26†V6²f÷"Â6ò#‚'V–ÆF–æw26öÆÆ6–ærFò&÷†W2—0¦7FFRF†Rv†öÆR7V—FR&Vv&G226÷'&V7B(	BæBF†RV&Æ—6†VB6Öö¶R76VBv–ç7B—BÂ#Bæ@£#76W'F–öç2Â&Vf÷&Rç–öæRæ÷F–6VBâv†B6Vv‡B—Bv2&VF–ærv—B7FGW6F†B†BCc¦f–ÆW2–â—Bv†VâF†R&6VÂF÷V6†VBFVââF†R'V–ÆBF‚æ÷r6·2F†R6ÖRVW7F–öâF†R6†V6²F€¦6·2æB&W÷'G2'V–ÇB(
b#‚7WW'6VFVB'’6æöæ–6Â&¶V²F†R7–ÖÖWG'’&WGvVVâ6†V6°¦æBF†R'V–ÆB—B6†V6·2v2F†Rv†öÆRFVfV7BâF†Rf÷W"vFR'Vç2&÷fRvW&RF†Vâ&R×'Vâg&öÐ§67&F6‚v–ç7BF†R&W7F÷&VB&¶Rà ¢¢¥v†BF–BäõB6†—Â7FFVBÆ–æÇ“¢F†R†÷W6V†öÆG2â¢¢BÔ"2w&—GFVâÇ6ò6ÆÆVBf÷"†÷W6V†öÆ@§&V6÷&G2âF÷F–ærF†W6RFVâ&öög2ÖVç2&W7FF–ærF†Rö67WF–öâ6Vç7W2(	BF†R†÷W6V†öÆBvVæW&F÷ ¦vFW2F†R6Vç7W2æBF†R†÷W6V†öÆG2v–ç7BV6‚÷F†W"–â&÷F‚F—&V7F–öç2(	BæBF†B6Vç7W2—0§F†R÷VÆF–öâÆ–W"w2vV¶W7B¦ö–çBÂFW&—fVBg&öÒf—fR–âÖFF6WB6Æ–'&F–öç2&F†W"F†à¦6—FVBâ&RÖ&wV–ær—B26–FRVffV7Böb&Æö6²&6VÂv÷VÆB&RW†7FÇ’F†R¶–æBöb6–ÆVç@§&RÖFV6—6–öâF†—2&ö¦V7B&VgW6W2â¢¥F†RFVâ&öög2&RVæö67W–VB¢¢Âæò†÷W6V†öÆBæÖW2F†VÒÂæ@§F†Rv÷&²—2VWVVB2¢¥$ôDÔBÔ&‚¢¢âæò‡VÖâf–wW&R—2G&vâ„Ã’ÂVæ6†ævVBà ¢22æWr##bÓ‚ÓB(	B#3"&öög27FæBöbccRÂæBöæÇ’RöbF†R&W7B†fRç—v†W&RFòvð ¢¢¥BÔâ¢¢F†RccR×&ööb&öw&ÖÖR†2&VVâ7V'G&7FVBg&öÒf÷"F†Rf—'7BF–ÖRâF†RF&vWBv0¦WF†÷&VB–âFF÷&V6öç7G'V7F–öâóƒ3Uö'V–ÆF–æuö–çfVçF÷'’æ§6öæöâ##bÓ‚ÓæBæWfW"Ö÷fV@¦v–ç7Bv†Bv2'V–ÇC²F†RfÖ–Ç’7&÷77vÆ²7F–ÆÂ6ÆÆVB¢£cr&öög2&VÖ–æ–ær¢¢v†–ÆP¢¢£#3"¢¢vW&R7FæF–ærÂf–wW&Rw&öær'’Ö÷&RF†âF†—&BöbF†R&öw&ÖÖRÂæBF†RæW‡@¦&Æö6²&6VÂv2vö–ærFò66†VGVÆRv–ç7B—BâF†R&VÖ–æFW"—2æ÷rDU$•dTB(	@¦FööÇ2÷&V6öæ6–ÆUóccRç–(i"FF÷&V6öç7G'V7F–öâóƒ3UóccU÷&ööe÷&öw&ÖÖRæ§6öæÂ&RÖFW&—fVB'¦FööÇ2ö6†V6²ç6†Æ–¶RF†RÆBw&–BæBF†RÆ–&W'F–W2âÆVFvW"&÷WBF÷vâF†Bw&÷w2Ö÷7@¦æ–v‡G26ææ÷B&RçVÖ&W"6öÖV&öG’G—VBà ¢¢£#C"&V6÷&G2&R#3"‡—6–6Â&öög2â¢¢GvVÇfR&V6÷&G2&RG&v'&–FvRÂF‡&VR'&–FvW2ÂGvð§–W'2ÂÆ—6FRÂ&FRw&÷VæBÂv'&—6öâv&FVâÂâ÷VâÆ—fW7Fö6²÷VæBÂ6÷W'F†÷W6P§F†R&öGV7F–öâ6‡&öæöÆöw’WG2–âF†RWGVÖâæB†÷FVÂ7F–ÆÂ6öç7G'V7F–öâ6†VÆÂ(	BF†P§‡—6–6Â×&öö`§&V6öæ6–Æ–F–öâ7&VF—G2F†VÒv—F‚æò&ööbÂv†–6‚—2v†B—B—2f÷"âöæR&V6÷&B—2Gvò6&–ç0¦æBF†RÆVFvW"6÷VçG2F†RÆ÷r&VF–ærâ'’F—7G&–7C¢¢¥6÷WF‚ÂvW7BCÂæ÷'F‚ƒÂf÷'B¢ ¦v–ç7BF&vWG2öb3sò3RòSòâ¢£C32&VÖ–ââ¢  ¢¢¥F†RçVÖ&W"F†B6†ævW2v†BÆæR"FöW2—2Râ¢¢F†RÆBÖöGVÆR&V6†W2’&Æö6·0¦†öÆF–ærS"Æ÷G2âBF†R&Wf–WvVB†6RÓ&6VÂw2÷vâFVç6—G’(	BöæR&–æ6—Â&ööbW"Æ÷BÀ¦æ6–ÆÆ'’BF†R&öw&ÖÖRw2÷vâSC£S(	BF†÷6R&Æö6·2†fR¢£R&öög2öb†VG&ööÒ¢¢Âæ@§6WfVâöbF†VÒÂF†Rv†öÆRÆ¶R7G&VWB&VÇBÂ&RÇ&VG’B÷"÷fW"—BâF†R÷F†W"¢£3#‚&öög0¦†fRæòÖöFVÆÆVBw&÷VæBFò7FæBöâ¢£¢#–â&Æµ÷6÷WF…÷vFW%öÖ&¶WFæ@¦&Æµ÷6÷WF…÷vFW%ö6Æ–çFöæÂv†–6‚F†RÆBÖöGVÆR&VgW6W2&V6W6R6÷WF‚vFW"w26öÖÖ—GFV@¦6VçG&VÆ–æR7F÷2#BÒæBƒs‚Ò6†÷'BöbF†VÓ²3R†VÆB'’F†RvW7B&V6—Rw2÷vâvFRBÆö6À¤R(‰#sÓ²æB#s2–âw&÷VæBv—F‚æò6öÖÖ—GFVB7G&VWB6öçG&öÂBÆÂ(	BV7Böb7FFRÂ6÷WF‚ö`¥v6†–æwFöâÂvW7Böb6Æ–çFöâÂæBF†RVçF—&Ræ÷'F‚F—f—6–öâÂv†–6‚F†Rw&–B6÷fW'2'’æ÷B§6–ævÆR&Æö6²â¢¥F†RccR×&ööb&öw&ÖÖR—26÷fW&vRÖ&÷VæBÂæ÷B&V6—RÖ&÷VæBâ¢¢ÆæR"†0§&÷Vv†Ç’FVâ&Æö6²&6VÇ2–â—B&Vf÷&R*r3’7G&VWB6öçG&öÂæBF†RFW'&–âW‡FVç6–öç2&RF†P¦öæÇ’F†–ærÆVgBFòFòà ¢¢¥6—‚fÖ–Ç’F&vWG2&RÇ&VG’W†6VVFVBÂ'’æ–æR&öög2ÂæBF†B—2&W÷'FVB&F†W"F†à¦†–FFVââ¢¢37F÷&W2Â“"æBC"ÂsÂsBæBsRÆÂ6''’Ö÷&R&öög2F†âF†R##bÓ‚ÓF&vW@¦ÆÆ÷w2ÂWfW'’öæRöbF†VÒWf–FVæ6RF†R&W6V&6‚Æ6VBgFW"F†RF&vWBv2w&—GFVââ¦Fö7VÖVçFVB&ööb—2æ÷B&VÖ÷f&ÆRÂ6òF†Ræ–æR6öÖR÷WBöbF†R–çfVçFVBfÖ–Ç’v—F‚F†RÖ÷7@§6Æ6²„CB’âF†R6ÖR'VÆR'Vç2–ç6–FRV6‚F—7G&–7Bv–ç7BF†Rw&÷WÖG&—‚(	Bæ÷'F‚†öÆG0§F‡&VR–ç7F—GWF–öæÂ&öög2æBGvòv&V†÷W6W2Ö÷&RF†â—G26†&RÂÆÂöbF†VÒGFW7FVBà ¢¢¥v†BF†—2FöW2æ÷BFòâ¢¢—B'V–ÆG2æ÷F†–æræBÖ÷fW2æ÷F†–æs¢WfW'’6÷VçB†W&R—2¦gVæ7F–öâöb&V6÷&G2F†BvW&RÇ&VG’6öÖÖ—GFVBâF†RW"Ö&Æö6²fÖ–Ç’Ö—‚—2à¦÷'F–öæÖVçBöbF†RF—7G&–7Bw2&VÖ–æFW"Âæ÷B6Æ–ÒF†Bç’&Æö6²†VÆBF†÷6RfÖ–Æ–W2(	@¦—BW†—7G26òF†R66†VGVÆRFG2WÂæBF†R&Æö6²&6VÇ2F†B6öç7VÖR—Bw&FRWfW'’fÇVP§F†W’VÖ—BBF†R–çfVçFVBF–W"2F†W’Çv—2†fRâGvòWF†÷&VBf–ÆW2vW&R6÷'&V7FVBv†W&P§F†W’7FFVB6öÖWF†–ærVçG'VR&÷WBv†B†2&VVâ'V–ÇC¢F†RvW7B&6VÂw27FGW0¢†&Wf–WvVE÷&V6—Uöæ÷E÷&VæFW&VFÂv†Vâ#öb—G2SR&öög27FæB’ÂF†R&ööb&V6öæ6–Æ–F–öâw0§7FGW2†ÆææVFÂv†Vâ—B—2FöæRæBF†—2ÆVFvW"&VG2—B’ÂF†Ræ÷'F‚&V6—Rw2'&VÖ–æ–æp£“&öög2"ƒc’gFW"&V6öæ6–Æ–F–öâ’ÂæBF†R7&÷77vÆ²w27WW'6VFVBcrà ¢22F†R&VæFW&–ær&öw&Ò—2Æ—fRÂæB÷fW&æ–v‡Bv÷&²æòÆöævW"6†—2Fò&öGV7F–öà ¢¢£##bÓ‚ÓBâ¢¢GvòF†–æw26†ævVBöâF†R÷væW"w2–ç7G'V7F–öâÂæBFövWF†W"F†W’6WBv†@§Föæ–v‡Bw2Æö÷FöW2à ¦Fö72õ$TäDU$”äræÖF—2¢¤5D•dR¢¢‡&Wf–WvVBæBÖW&vVBÂ"3b’âF†RrG&6²æBF†Rs ¦7&—F–2†&æW72&R'V–ÆF&ÆRæ÷s²F†R‚†vÆ²Ö†F’æBâ†æF—fRVæv–æR’G&6·2æBWfW'§&VÖ–æ–ærõtäU"DT4•4”ôæ7F’vFVBW†7FÇ’2w&—GFVââF†R&÷fVBµE‚Õ6ögGv&R–ç7FÆÀ¦ÆæFVBöâF†R&¶R'VææW"Âv†–6‚Væ&Æö6·2s"w2FW‡GW&W2(	Bæ÷FRv†B—Bf—†W3¢&¶Rç6†6·0¦f÷"Ò×FW‡GW&RÖ6ö×&W72·Gƒ&öæÇ’v†VâF†R·G†&–æ'’—2&W6VçBÂ&V6W6RvÇFb×G&ç6f÷&Ð¦&÷'G2F†R§v†öÆR¢÷F–Ö—¦Rv†Vâ—B—2'6VçBÂÖW6†÷B–æ6ÇVFVBà ¥F†—2—2æ÷röâ¢§Gvò×F–W"FWf(i"Ö–æ—VÆ–æR¢¢†Fö72õ•TÄ”äRæÖF’ÂF†RGvò×F–W ¦f÷&ÒöbF†RfÆVWB–Æ÷B–â¶Wf–ç&†2ö¦ö'G&6¶W"çöÆV6BæÆ—fVâ7FWv&B&6VÇ2æBF†P¦æ–v‡FÇ’&¶R'&æ6‚öfbFWfæB"–çFòFWf²ÖW&v–ærF†W&RV&Æ—6†W2öæÇ’F†R–çFVw&F–öà§&Wf–WrB¢¦ö7W7FöÒö6†–6vòóFBöFWb÷vÆ²ó÷–V#Óƒ3V¢¢(	Bæö–æFW‚Â&ææW"ÖÖ&¶VBÀ¦'V–ÆBæ§6öæ&W÷'F–ærF–W#¢FWfâ¢¥&öGV7F–öâÖ÷fW2öæÇ’v†VâF†R÷væW"F—7F6†W0¦6†–6vòÓFB×&öÖ÷FR×Fò×&öBç–ÖÆâ¢¢&öÖ÷F–öâ—2vFVC²FWÆ÷’—2æ÷BÂæBæWfW"v–ÆÂ&Rà ¥GvòFVfV7G2&R&V6÷&FVB&F†W"F†âf—†VBÂ&÷F‚–ææVB'’vFW26òF†W’6ææ÷Bw&÷s ¢¢£s’öbsC"ÃSƒFW'&–âfW'F–6W2f6RF÷vçv&B¢¢ƒãRÂ—6öÆFVBÂæòf—6–&ÆR'FVf7B(	@¥$ôDÔBÔ%Ts"ÂF—7F–æ7Bg&öÒF†R&Æ6²vVFvRF†Bv2f—†VBFöF’’ÂæB¢§F†R&—fW"VFvP¦fÆ–6¶W'2v†VâfÇ––ær¢¢…$ôDÔ"Ô%TsÂÆÖ÷7B6W'F–æÇ’FWF‚Ö'VffW"f–v‡F–ær&WGvVVâF†P§vFW"ÆæRæBF†Rw&÷VæB7&÷76–ær—BÂ÷væVB'’F†R"ÕsR&6VÂ’â¥"Ô%Tsv26Æ÷6V@£##bÓ‚Ób(	BF†RwVW72–âF†B6VçFVæ6Rv2&–v‡B&÷WBF†Rf–v‡BæBw&öær&÷WBF†R÷væW# ¦—Bv2F†R6ÖW&w2æV"ÆæRÂæ÷BF†RvFW"ÖFW&–Ââ6VRF†RF÷öbF†—2f–ÆRâ  ¢22F†R6V6öæB&Æö6²&WVFVBF†R6†RÂæB&VgW6VBöæRöb—G2&öög0 ¢¢£##bÓ‚ÓBâ¢¢&Æµ÷&æFöÇ…öFV&&÷&æ(	BF†RV7FW&æÖ÷7B&Æö6²F†RÆBÖöGVÆR&V6†W2öâF†P¥&æFöÇ‚F–W"(	B6'&–W2¢¦æ–æRöbF†RFVâ&öög2F†R66†VGVÆRFVÇB—B¢¢â7FæF–ær&öög0¢¢£#C"(i"#S¢¢Â&VÖ–æ–ær¢£C#2(i"CB¢¢ÂƒböbF†VÒöâw&÷VæBF†R&ö¦V7B†26÷fW&vRf÷"âF†P¦vVöÖWG'’†ÆböbBÔ2v2&V6—RVçG'’æBæ÷F†–ærVÇ6RÂv†–6‚—2W†7FÇ’v†BBÔ"6–B—@§v÷VÆB&RâF†RGvòF†–æw2v÷'F‚&VF–ær&Rv†BF†R&WVBW‡÷6VBà ¢¢¥F†RFVçF‚&ööbv26—f–2ÂæB—B—2FVfW'&VB&F†W"F†â'V–ÇBâ¢¢“2&W6öÇfW2F‡&÷Vv‚F†P¦f÷'E÷7G'V7GW&VÆ6V†öÆFW"ÂæBWfW'’'V–ÆF–ær¶–æBF†B&6†WG—RöffW'2—2v'&—6öâv÷&B(	@§V'FW'2Â&'&6·2Â&Æö6¶†÷W6RÂÖv¦–æRÂwV&BÂ7WFÆW"Â'F–ÆÆW'’âÖ76–ærâæöç–Ö÷W2F÷và¦6—f–2'V–ÆF–ærF‡&÷Vv‚—Bv÷VÆB†fR7FööBv'&—6öâ'V–ÆF–ærsSÒg&öÒF†Rf÷'BâF†R7&÷77vÆ°¦†BÇ&VG’w&—GFVâF†R6öæF—F–öâöâ—G2÷vâVçG'“¢F†RfÖ–Ç’¢'7ç2VæÆ–¶RgVæ7F–öç3²F†W’×W7@§&V6öæ6–ÆRFòæÖVBV&Æ–2&V6÷&G2&Vf÷&R6VÆV7F–ær6öç7G'V7F–öâ"¢â6òF†RvVæW&F÷"æ÷r&VgW6W0¤“Â“"æB“2¢¦'’æÖR¢¢ÂV÷F–ærF†R6öÖÖ—GFVB6VçFVæ6RV6‚&VgW6ÂVæf÷&6W2ÂæB&ööbF†P§66†VGVÆRFVÇB'WBF†R&6VÂF–Bæ÷B'V–ÆB×W7B&RæÖVB–âF†R&V6—Rv—F‚—G2&V6öæ–ær(	B¦vFRF†B&—FW2–â&÷F‚F—&V7F–öç2Â6òfÖ–Ç’6ææ÷B&RV–WFÇ’G&÷VBæBFVfW'&Â6ææ÷@¦&RW6VBFò†–FRöæRâF†RF—7F–æ7F–öâ&V–ærG&vã¢âæöç–Ö÷W2¦GvVÆÆ–ær¢—26÷VçB×Væ—BF÷v&@¦Fö7VÖVçFVBvw&VvFS²âæöç–Ö÷W2§V&Æ–2'V–ÆF–ær¢76W'G2F†Bâ–ç7F—GWF–öâ7FööB†W&Ræ@¦ÆVgBæò&V6÷&BÂæBF†—2F÷vâw2V&Æ–2'V–ÆF–æw2&RfWrVæ÷Vv‚Fò&RÆ—7FVBâ¢¤öæRæöç–Ö÷W2“ §7F–ÆÂ7FæG2–âF†Ræ÷'F‚F—f—6–öâ¢¢g&öÒ&6VÂw&—GFVâ&Vf÷&Rç’öbF†—2ÂÖ76VB2vVæW&–0¦g&ÖR&Æö6³²—B—2&V6÷&FVB–âÃ“2&F†W"F†â&VÖ÷fVBÂæB—B—2æ÷B&V6VFVçBF†BW‡FVæG2à¥$ôDÔ¢¥BÔ“2¢¢æ÷r÷vç2F†R&W6V&6‚F†R&VgW6Â—2v—F–æröâà ¢¢¤ÆFVçBFVfV7Bg&öÒF†Rf—'7B&Æö6²Â6Vv‡B'’F†R6V6öæBÂöâGvòÖ6VçF–ÖWG&RÖ&v–ââ¢ ¦Æ÷Eög&ÖR‚–6†÷6RÆ÷Bw2ÆÆW’VFvR2F†RVFvRæV&W7BF†RÆÆW’w24TåE$ô”B(	Bv†–6‚6—G2@§F†R&Æö6²w26VçG&RÂ6òöââTäBÆ÷BF†R6–FRÆ÷BÆ–æR'Vææ–ær&6²F÷v&B—B—2æV&Ç’26Æ÷6P¦2F†RÆÆW’VFvRâÖV7W&VBöâF†—2&Æö6³¢¢£3‚ã“2Òv–ç7B3‚ã“RÒ¢¢ÂæBGvòöb—G2f÷W"Væ@¦Æ÷G2–6¶VBF†R6–FRÆ–æRÂg&Ö–ær'V–ÆF–ær'&öG6–FRFò—G2÷vâ7G&VWBæB÷fW"F†P¦æV–v†&÷W&–ærÆ÷Bâ¢¥v†B&W÷'FVB—Bv2F†RÆ÷BÖÖ&v–âvFRBãCBÒv–ç7BãRÒ&÷VæB¢¢(	@¦Ö–ÆÆ–ÖWG&R×66ÆR6ö×Æ–çB&÷WBæ–æWG’ÖFVw&VRW'&÷"Âv†–6‚—2F†R'BFò&VÖVÖ&W"âÖV7W&–æp§FòF†RÆÆW’7G&—6W&FW2F†R6ÖRGvòVFvW2'’ã"ÒæB#bã2ÒÂæB7G'V7GW&Â6†V6²æ÷p§&–FW2v—F‚—B†g&öçBæB&V"&RF†R6ÖRÆVæwF‚Fòv—F†–âF†RÆBw26¶Ws²#RF—6w&VVÖVç@¦ÖVç2öæR—26–FRÆ–æR’â¢¦&Æµ÷&æFöÇ…÷vVÆÇ66ÆV&VBF†RöÆBF–R'’ã2Ò–â3rÂ6òæ÷F†–æp¥BÔ"6öÖÖ—GFVBÖ÷fW2¢¢(	B—Bv2öæR&Æö6²w2&÷÷'F–öç2v’g&öÒF†R6ÖRf–ÇW&RÂæB—B†@¦&VVâw&VVâà ¥Föæ–v‡Bw2Æö÷—2W‡V7FVBFò&öGV6R¢¦öæR&6VÂW"'Vâg&öÒGvòÆæW2F†B6ææ÷@¦6öÆÆ–FR¢¢†Fö72õ$ôDÔæÖF(i"%D„RõdU$ä”t…BÄäU2"“¢ÆæR$TäDU$”ärF÷V6†W2&VæFW&W"æ@§FööÂf–ÆW2ÂÆæR"Dõtâ4ôÕÄUD”ôâF÷V6†W2FFöæÇ’â¢¥"Ôs¢¢‡F†R7&—F–2†&æW72’Â¢¥BÔ¢ ¢‡F†RccR×&ööb&V6öæ6–Æ–F–öâ’æBF†Rf—'7BGvò&Æö6·2öfbF†R&V6öæ6–ÆVB66†VGVÆR‚¢¥BÔ"¢¢À¢¢¥BÔ2¢¢’&RÆÂ–âÂ6òF†RäU…BU–6·2&R¢¥"Õs¢¢†Æ–v‡B’æB¢¥"ÕsB¢¢†FÖ÷7†W&R’–à¦ÆæR²¢¥BÔN(
b¢¢†öæR÷Vâ&Æö6²W"'VâÂæ÷rF÷F–ær–âF†R6ÖR'Vâ’æB¢¥BÔ“2¢¢‡F†P¦6—f–2&öög2BÔ2&VgW6VB(	B&W6V&6‚Âæ÷BÖ76–ær’–âÆæR"â¢¥BÔ&‚¢¢—2–âFöòâFöF’w0¦6÷VçB—2¢£#c7G'V7GW&R&V6÷&G2(	B#S‡—6–6Â&öög2öbccRF&vWB(	BSB†÷W6V†öÆG2Â“ §W'6öç2¢¢âWfW'—F†–ær'&—fW22"–çFòFWfæBv—G2F†W&Rà ¤†öæW7B7FFRöbF†R&ö¦V7BâF†–æw2F†B&RVçfW&–f–VB7F’Æ&VÆVBVçfW&–f–VC²vFRF†@§v26¶—VB—2&V6÷&FVB26¶—VBâWFFVB–âF†R6ÖR6öÖÖ—B2F†Rv÷&²—BFW67&–&W2à ¢¢¤Æ7BWFFVC¢¢¢##bÓ‚ÓB+r¢¥†6S¢¢¢3Â3†FGVÒ’Â3"×'F–Â‡FW'&–â²&—fW"BF†P¦f÷&·2’Â3B×'F–Â†g&ÖU÷FfW&âÂÆöuöGvVÆÆ–ærÂ'&–FvU÷F–Ö&W"’Â3’×'F–Â†FFVBf—6–&ÆP§7G&VWBÆ–W"’Â3×'F–ÂƒccR×&ööbÆVFvW"²‚æöç–Ö÷W2&öög2’æB#‡&VæFW&W"¦6ö×ÆWFRâ¢¤³†–æfW'&VB&W6–FVçG2’6ö×ÆWFRF‡&÷Vv‚†6RGvó²³r‡F†RÆGFVB&Æö6²æBÆ÷@¦w&–B’6ö×ÆWFRF‡&÷Vv‚†6RöæRÂæB†6RGvòw2Æ6VÖVçBvFR—26Æ÷6VB(	BWfW'’vVæW&FV@§Æ6VÖVçB–âF†RFF6WB—2÷WBöbF†RÆGFVB&öGv’æBÆÂF‡&VRvVæW&F÷'2Væf÷&6R—C°¤³’†æf–vF–öâT’’6ö×ÆWFRâ¢  ¢¢¤7W'&VçBW‡ç6–öã¢¢¢F†Rƒ3R66VæR&W6öÇfW2¢£##"7G'V7GW&R&V6÷&G2¢¢ÂæB¢£S"†÷W6V†öÆG2ð£ƒ‚W'6öç2¢¢7FæB&V†–æBF†VÒƒsbFö7VÖVçFVBÂ#FW&—fVBÂ“"–æfW'&VB’â‚&V6÷&G2&RFvvV@¦–æfW'&VEöæöç–Ö÷W6æBF—7Æ’2fÆvvVB&Wf–WrÖ76–æw3²¢£ƒ2öbF†÷6Ræ÷r†fRâ&wVV@¦ö67WçB¢¢&F†W"F†â&V–æræöç–Ö÷W26÷VçB×Væ—G2ÂæBc"7G'V7GW&W2æÖR†÷W6V†öÆBöâF†P¦'V–ÆF–ær6&BâF†W’&Vv–î(	G&F†W"F†â6ö×ÆWF^(	GF†R÷væW"7V6–f–6F–öâw2ccR×&ööbF&vWBâW†7@¦æöç–Ö÷W2&W6Væ6RÂfö÷G&–çBæBÆ÷B÷6—F–öâ&VÖ–â6öæ¦V7GW&ÂÂæBF†RF÷F–öâ6†ævW2æöæP¦öbF†C¢v†B—BFG2—2&V6öâf÷"F†R&ööbÂæ÷BWf–FVæ6Rf÷"—Bâ¢¤æò–æfW'&VBW'6öâ†2¦æÖRÂæBæöæR6†÷VÆB¢£²æòf–wW&R—2G&vâ„Ã’âF†R&VÖ–æ–æræ÷'F‚W‡ç6–öâ—27F–ÆÂvFV@¦&V†–æBVæ–f–VBFW'&–âæB‡–G&öÆöw’6÷fW&vRà ¢¢¥F†RvV¶W7B¦ö–çB–âF†R÷VÆF–öâÆ–W"Â7FFVBÆ–æÇ“¢¢¢æòW&–öBG&FRF&ÆRf÷"¦6ö×&&ÆRvW7FW&âF÷vâW†—7G2–âFF÷6÷W&6W2öâWfW'’ö67WF–öâ&F–ò—2F†W&Vf÷&RFW&—fV@¦g&öÒf—fR–âÖFF6WB6Æ–'&F–öç2&F†W"F†â6—FVBÂæBF†R&—F†ÖWF–2—2w&—GFVâ÷WBW"G&FP¦–âFö72õ$U4T$4‚÷&W6–FVçG5óƒ3Uö–æfW'&VBæÖFâF†B—2&VÂvÂæ÷B&÷VæF–ærW'&÷"à ¢¢¥vFW"fVvWFF–öâ6÷'&V7F–öã¢¢¢VÖW&vVçBÆçG2æ÷rW6RG'VRF—7Fæ6RFò6†÷&VÆ–æRæB&P¦Æ–Ö—FVBFòF†R6†ÆÆ÷rV–v‡BÖÖWG&RÖ'6‚VFvRâæöâÖVÖW&vVçBfÆ÷&æBWfW'’vööG’Æ6VÖVçB&P§&V¦V7FVB÷fW"F†RG&6VBvFW"Ö6²ÂæB6–æ6R##bÓ‚Ó2F†RÖ—'&÷"öbF†B'VÆR†öÆG2Föó¢§7V6–W2v†÷6R&V6÷&FVB7V'7G&FV—2÷Vå÷vFW&(	BBF†BfÆöG2(	B—2&VgW6VBWfW'’7FF–öà¦öâG'’w&÷VæBâf—'7B×'Vâæf–vF–öâwV–FR6â&RF—6Ö—76VBæB&V÷VæV@¦g&öÒ6WGF–æw2à ¢¢¥&ÆÆVÂ†6R×GvòÆææ–æs¢¢¢F‡&VRæöâ×&VæFW&VB&6VÂ&V6—W2æ÷r6÷fW"ƒBFF—F–öæÂ6÷WF€¤F—f—6–öâ&öög2ƒcb&–æ6—ÂÂ‚æ6–ÆÆ'’’ÂSRvW7BF—f—6–öâ&öög2ƒCB&–æ6—ÂÂæ6–ÆÆ'’¦æBcæ÷'F‚F—f—6–öâ&öög2ƒCR&–æ6—ÂÂRæ6–ÆÆ'’’âFövWF†W"v—F‚F†R–×ÆVÖVçFVBC‚F†W§&W6W'fR#Cr6Æ÷G2v—F†÷WBW†6VVF–ærç’ccR×&ööbfÖ–Ç’6âF†W’&VÖ–âÆç2Âæ÷B66VæR6Æ–×3 §F†R6÷WF‚6WBv—G2f÷"‡—6–6Â×&ööb&V6öæ6–Æ–F–öã²3RvW7B&öög2Ç6òv—Bf÷"Væ–f–V@§vW7Gv&BÖ÷FW'&–âW‡FVç6–öâFòRÓsÒÂæBF†R÷WFW"æ÷'F‚72v—G2f÷"â³scÒ6÷fW&vRà¢¢¤Ö–ÆW7FöæR6†—VC²Ö–ÆW7FöæR‡F†Rf÷&·2’—2–â¢¢(	B6—‚7G'V7GW&W2Æ6VBg&öÒF†P¦vV÷&VfW&Væ6RÂ&VÂw&÷VæBÂG&6VB&—fW"ÂæBF†RÆ–&W'F–W2æ÷r&VF&ÆR–ç6–FRF†P§vÆ·F‡&÷Vv‚&F†W"F†âöæÇ’–âF†R&W÷6—F÷'’â¢¥6WfVâ7G'V7GW&W2æ÷rÂæBF†R6WfVçF‚—0¦æ÷B'V–ÆF–ær¢£¢F†Ræ÷'F‚'&æ6‚'&–FvR—2F†Rf—'7B&V6÷&B'V–ÇBöâF†R'&–FvU÷F–Ö&W& ¦&6†WG—RæBF†Rf—'7B–âF†—2FF6WBv†÷6RF–ÖVç6–öç26öÖRg&öÒWf–FVæ6R&F†W"F†âg&öÐ¦Æ6V†öÆFW"â2öb##bÓ‚Ó—B7FæG2öâ¢§Gvò&VçG2&F†W"F†âf–gFVVâ–çfVçFVB7&–'2¢ ¢Œ*r#B’(	BF†Rf—'7BF–ÖR&VF–æröbâ&6†—fR†2F¶Vâ6öÖWF†–ær¦÷WB¢öbF†—2ÖöFVÂà¢¢¤V–v‡B7G'V7GW&W2æ÷rÂæBF†RV–v‡F‚—2F†Rf—'7B%T”ÄD”ärv†÷6Rfö÷G&–çB—2Wf–FVæ6R¢£ ¤†övâw27F÷&RöâÆ¶R7G&VWBÂv†W&R6†–6vòw2÷7Böff–6R÷VæVB–âƒ3Â—2&V6÷&FVBGv–6R'¤æG&V22GvVçG’'’f÷'G’Öf—fRfVWBŒ*r#R’â—B—2Ç6òF†Rf—'7B&V6÷&B†W&Rv—F‚æ÷F†–æp¦6öæ¦V7GW&Â–â—BÂæBF†R6÷'&V7F–öâF†B6ÖRv—F‚—BÖ÷fVBF†R÷7Böff–6Rw2FW'GW&Rg&öÐ§F†—2'V–ÆF–ær'’GvVçG’ÖöçF‡2à ¢ÒÒÐ ¢22F†R7&—F–2&6VÆ–æR(	B##bÓ‚Ó@ ¢¢¥$TäDU$”ärsã—2–âæBsã"w2çVÖW&–2†Æbv—F‚—Bâ¢¢FööÇ2ö7&—F–5÷6†÷G2æÖ§67FæG2@¦VÆWfVâf—†VB7FF–öç2(	BF†RV–v‡B66VæRæ6†÷'2g&öÒFF÷66VæW2óƒ3Ræ§6öæÂG&—fVâ'’F†P§vÆ·F‡&÷Vv‚w2÷vâvõFö6òF†R&–r6ææ÷BG&–gBg&öÒF†Rf–Wwö–çG2f—6—F÷"—2öffW&VBÀ§ÇW2F‡&VR&RÖW7F&Æ—6†VB&—&–R×7vVW7FæG2(	BB&÷F‚&VÆV6Rf–Ww÷'G2Âv—F‚F†Ræ–ÖF–öà¦6Æö6²†VÆBg&öÒ&Vf÷&RF†R&VæFW"Æö÷w26V6öæBF–6²æBF†RDôÒ6‡&öÖR†–FFVâà¦FööÇ2ö7&—F–5öÖWG&–72æÖ§6&VG2F†Räw2v—F‚æòFWVæFVæ6–W2BÆÂÂv†–6‚ÖVç2F†R6ÖP¦6öFR6âÖV7W&R&VfW&Væ6R†÷Föw&‚æBöæRöb÷W"g&ÖW2â¢¥F†B†2æWfW"&VVâG'VP¦†W&R&Vf÷&R¢¢ÂæB—B—2F†R&V6öâF†RçVÖ&W'2&VÆ÷r&Rv÷'F‚&V6÷&F–ærà ¢¢¥&VBF†W6R2&6VÆ–æRÂæ÷B266÷&V&ö&Bâ¢¢f÷W"F†–æw2†fRFò&R6–B&Vf÷&RF†P§F&ÆW2Â÷"F†W’v–ÆÂ&RV÷FVBw&öævÇ“  £â¢¥F†W’&Ræ÷B6ö×&&ÆRFòF†R##bÓ‚Ó&—&–R7vVWw2f–wW&W2â¢¢F†B†&æW72v0¢æWfW"6öÖÖ—GFVBæBæV—F†W"vW&R—G27FF–öâ6ö÷&F–æFW2Â6ò&÷F‚F†R6öFRæBF†R6ÖW&¢÷6—F–öç2&RæWrâv†W&R*sRF&vWBv26WBg&öÒF†R7vVWw2–×ÆVÖVçFF–öâÂF†RF&vW@¢æVVG2&RÖæ6†÷&–ær'’ÖV7W&–ær&VfW&Væ6R†÷Föw&‚F‡&÷Vv‚D„•26öFR(	Bv†–6‚—2æ÷r¢öæRÖÆ–æR¦ö"æB—2æ÷B–WBFöæRà£"â¢¥F†RÖV7W&VÖVçB6öçfVçF–öç2&RF†R†&æW72w2÷vâ¢¢æB&R7FFVB–âF†R†VBö`¢FööÇ2ö7&—F–5öÖWG&–72æÖ§6¢v†B6÷VçG226·’Â†÷rF†RÆæB÷6·’Æ–æR—2f÷VæBÂF†R&æ@¢F†R†÷&—¦öâF–Ö&W"—2Æöö¶VBf÷"–âÂæB†÷r7&÷vâ—†VÂ—2–FVçF–f–VBâF†W’&Rf—†VB6ð¢F†BGvò&÷VæG2&R6ö×&&ÆS²F†W’&Ræ÷B6Æ–×2&÷WBƒ3Rà£2â¢¤fÆ÷vW"ÆöB—2öæÇ’ÖVæ–ævgVÂBF†R÷Vâ×&—&–R7FF–öç2â¢¢–âg&ÖRv—F‚7G&VWG2À¢vÆÇ2æB&öög2–â—BF†RFVæöÖ–æF÷"—2æ÷BfVvWFF–öâà£Bâ¢¥F†R7&÷vâÖWG&–72æVVB7&÷vââ¢¢g&öÕö&÷fV&W÷'G2F†VÒ&V6W6RF†R†&æW72&W÷'G0¢WfW'—F†–ærÂ'WBÃC"7&÷vâ—†VÇ2–ââW&–Âg&ÖR—2æ÷B6æ÷’ÖV7W&VÖVçBà ¤&÷F‚&6VÆ–æR'Vç2vW&R¢£ó'—FRÖ–FVçF–6Â&WGvVVâGvò6W&FR'&÷w6W"&ö6W76W2¢¢@¦&÷F‚f–Ww÷'G2ÂæBWfW'’7FF–öâw2—F6‚ÖF6†VB—G2FV6Æ&F–öâà ¢¢¦FW6·F÷#ƒ9sƒ¢  §Â7FF–öâÂF–Ö&W"ÆÂÂF–Ö&W"6VçG&RÂ7&÷vâf–æRÂ7&÷vâ~(‰$"ÂFV6–ÆRÂÂÆ—FW&Â&Æ6²‚Â$Õ2f"öÖ–BöæV"ÂfÆ÷vW"ÆöBÂG&w2òG&–ævÆW2À§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â6Vvæ6†Âãc3rÂãccbÂãSs’ÂCBã’ÂRãsbÂÂãBòrãRòã‚Âã3ÂcRò33"ÃCSRÀ§Â6Vvæ6…÷v–ævÂãC“2ÂãCsRÂãScbÂrãBÂãs2ÂcÂã‚òrãòã’Âã3ƒ2Âcbò3sbÃSc2À§ÂÆ¶UöÖ&¶WFÂãS‚ÂãSƒ‚ÂãSSÂ#BãbÂ2ÂÂ"ãòRã‚òãÂã3#rÂs‚òCƒBÃSSBÀ§Âf—'7E÷÷7Eööff–6VÂãƒCrÂã“3rÂãSS"Â"ã"ÂRã3RÂRÂ’ãrò‚ã‚ò’ã’ÂãBÂcbò3“2Ãc“‚À§Âf÷&·6Âãs3’ÂãsƒBÂãs#RÂ3RãÂ#RãS‚ÂÂãòrãòãBÂã2ÂƒròS“bÃc‚À§Âw&VVå÷G&VVÂãs3Âãs3RÂãcsÂ#ã2Â3ãƒ‚ÂÂ"ã’òRã2òã’ÂãrÂ“òSS2ÃC“‚À§Â6÷WF…÷vFW&¢®(
¢¢Âãƒƒ’Âã“2ÂãBÂ#rãBÂ"ã“RÂÂrãò#bãrò3ãÂãSsRÂƒRòSsÃs‚À§Âg&öÕö&÷fVÂã#"ÂãƒÂãƒ3Âã"Â#‚ã#BÂÂ2ã‚òbãrò’ãrÂã’ÂcròC32Ã“À§Â&—&–U÷6÷WF†Âã3cBÂã3CÂãcƒ"Â#rã‚Â2ã#rÂ#3RÂBã‚òRãò‚ãrÂã3Âs2òS"Ã‚À§Â&—&–U÷vW7FÂãƒ3"ÂãƒSÂãc#’Â#BãÂ2ãcrÂÂBãBò#ã‚ò#rãrÂã"Â“ròc‚ÃcƒbÀ§Â&—fW%ö&æ¶ÂãcCÂãs’ÂãsCÂCrã’Âã“2Â#c2Â2ã"ò#2ã’ò#’ã’Âã#"ÂSbò3sÃc“À ¢¢¦Öö&–ÆR3“9ssƒ¢  §Â7FF–öâÂF–Ö&W"ÆÂÂF–Ö&W"6VçG&RÂ7&÷vâf–æRÂ7&÷vâ~(‰$"ÂFV6–ÆRÂÂÆ—FW&Â&Æ6²‚Â$Õ2f"öÖ–BöæV"ÂfÆ÷vW"ÆöBÂG&w2òG&–ævÆW2À§ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â6Vvæ6†ÂãsSbÂãƒ#2ÂãSs"Â#bã2Â’ãC’ÂÂ2ãRòãbòã2ÂãC"Âc"ò33Ã#ƒ2À§Â6Vvæ6…÷v–ævÂãccrÂãS“"Âãc#RÂ#"ãRÂ‚ãs‚ÂÂ2ãBòãbòãBÂã“"Âc2ò3#2Ã“CbÀ§ÂÆ¶UöÖ&¶WFÂãc“rÂãs’ÂãS“rÂRã’ÂRã#ÂÂ2ã2ò"ãòãBÂãsrÂcbò3srÃ"À§Âf—'7E÷÷7Eööff–6VÂã“’Âã“ƒ’ÂãSCÂ#ãÂRã#bÂsc2ÂBãrò’ãBòãBÂãÂcò3ƒbÃS3bÀ§Âf÷&·6ÂãsC’Âãs3Âã33rÂ3rãRÂ#2ãC"ÂÂãbòã‚òãbÂÂƒ"òSs2ÃƒCÀ§Âw&VVå÷G&VVÂãscrÂãsCbÂãsCÂ#2ãbÂ3’ãCbÂÂbã"òã"òãRÂã"Âƒ‚òS3rÃcS’À§Â6÷WF…÷vFW&¢®(
¢¢Âãƒ3bÂãƒÂãsSRÂ3Rã’ÂrãSBÂÂ#Bãò32ã’ò#RãÂã#‚Âƒ2òSSÃcRÀ§Âg&öÕö&÷fVÂãSbÂã“"ÂãssBÂBã"Â#Rã32ÂÂbã2òã’òãRÂã"Âcò3srÃ#À§Â&—&–U÷6÷WF†ÂãCcrÂãC“"Âãc"Â3ã‚Â2ãsbÂ#crÂã2ò"ã’ò‚ãÂã‚ÂsòCsbÃsBÀ§Â&—&–U÷vW7FÂãcs’Âãc“bÂãss"Â#BãÂãcRÂÂ#ãò3ã‚ò’ãbÂã2Â“BòcRÃ3cbÀ§Â&—fW%ö&æ¶Âãs2Âãss2ÂãƒBÂCã2Â"ãsrÂ#SBÂ#ã’ò32ã"òbãÂãBÂC’ò3cRÃ3S2À ¢¢®(
6÷WF…÷vFW&†W&R—2F†R$UD•$TB7FæB(	BÆö6Âƒ#cÂÓ“R–Â%6÷WF‚vFW"7G&VWBÂÆöö¶–æp¦V7B"Âv†–6‚7FööBÒ6÷WF‚öbF†R6VçG&VÆ–æRöbF†R7G&VWB—B—2æÖVBf÷"æBg&ÖVBf–VÆBâ¢ ¥BÕc"‚33R’Ö÷fVBF†Ræ6†÷"öâ##bÓ‚ÓRFòƒ3#’ã‚Ârã–ÂF†RvVÆÇ27G&VWB6÷&æW"ÂæBWfW'¦6÷WF…÷vFW&f–wW&R6†÷Bg&öÒ##bÓ‚Óböçv&G2ÖV7W&W2F†B7FæB–ç7FVBâ¢¥F†RGvò&Ræ÷@¦6ö×&&ÆRæBæV—F†W"—26÷'&V7F–öâöbF†R÷F†W"(	BF†W’&RGvòÆ6W2â¢¢&÷F‚7FæG2vW&P§&R×6†÷BöâöæR'V–ÆBöâ##bÓ‚Ó#26òF†RÖ÷fR6â&R&VB6W&FVÇ’g&öÒF†RF÷vâw2w&÷wFƒ²6VP¢¥&R×6†÷B##bÓ‚Ó#2(	BF†R6÷WF…÷vFW&&6VÆ–æR&÷rÖV7W&W27FæBF†BæòÆöævW"W†—7G2¢BF†P§F÷öbF†—2f–ÆRâæò÷F†W"7FF–öâ–âF†W6RF&ÆW2Ö÷fVC²æWv&W''•öFöÆU÷v†&f…BÓC’æ@¦æ÷'F…ö'&æ6…ö'&–FvUöFV6¶…BÓ’vW&RFFVBFòF†R66VæRgFW'v&G2æB†fRæò&÷r†W&RBÆÂÀ§6òF†R&–ræ÷r7FæG2B¢¦f÷W'FVVâ¢¢7FF–öç2v–ç7BF†—2F&ÆRw2VÆWfVâ(	BF†Rf÷W'FVVçF‚—0¦V&Æ–5÷7V&V…BÓ##BÂ##bÓ‚Ó#‚’Â÷6RöâF†R&W6W'fVB&Æö6²Âv†÷6RGvò&÷w2&RBF†RF÷ö`§F†—2f–ÆRà ¢¢¥v†BF†R&6VÆ–æR6—2Âv–ç7BF†R$TäDU$”är*sRF&vWG2â¢  ¢Ò¢¤†÷&—¦öâF–Ö&W"6÷fW&vR—26†÷'Böb“RæV&Ç’WfW'—v†W&R¢¢(	Bã#Fòãƒ’FW6·F÷Â&W7@¢Bf—'7E÷÷7Eööff–6VƒãƒCr’æBv÷'7BÆöö¶–ærF÷vâBF†RF÷vâg&öÒF†R—"â*r—FVÒP¢7FæG2ÂæB"ÕsB÷vç2—Bà¢Ò¢¥6†F÷w27F–ÆÂ6Æ—FòÆ—FW&Â&Æ6²â¢¢"Ãc2W&RƒÃÃ–—†VÇ2B&—fW%ö&æ¶À¢ÃRBf—'7E÷÷7Eööff–6VÂ"Ã3RB&—&–U÷6÷WF†öâFW6·F÷ÂæBF†RF&¶W7BFV6–ÆP¢'Vç22Æ÷r2¢¤Âã“2¢¢v–ç7BF†R*rRfÆö÷"öb¢¤Â(šRB¢¢â*r—FVÒr7FæG2ÂæB"Õs¢÷vç2—Bà¢Ò¢¥7VæÆ—B7&÷vç2&RæòÆöævW"&ÇVRâ¢¢~(‰$"—2÷6—F—fRBWfW'’7FF–öâ‚³ã"Fò³Crã’’ÂvVÆÀ¢6ÆV"öbF†R(šR³F&vWBBæ–æRöbVÆWfVâÂv†W&RF†R7vVWÖV7W&VB(‰#’Fò(‰##bâF†R6öÆ÷W ¢'Vw2f—†VBöâ##bÓ‚Ó&RF†R&V6öã²F†—2—2F†Rf—'7BÖV7W&VÖVçBF†B6—26òà¢Ò¢¤w&–â7F–ÆÂ6öÆÆ6W2v—F‚FWF‚Â'WBæ÷BVæ–f÷&ÖÇ’¢¢(	B6Vvæ6†&VG2ãBòrãRòã€¢f"öÖ–BöæV"öâFW6·F÷Â&—fW%ö&æ¶2ã"ò#2ã’ò#’ã’âF†R7FF–öç2F†BÆöö²F÷vâ¢7G&VWB÷"7&÷72vFW"†öÆBF†V—"w&–ã²F†RöæW2Æöö¶–ær÷fW"÷Vâ7v&BÆ÷6R—Bâ*r—FVÐ¢B7FæG2à¢Ò¢¤fÆ÷vW"ÆöBBF†R&—&–R7FF–öç2—2ã3æBã"¢¢v–ç7BF†R†öæW7BN(	3bP¢F&vWBâçåGvò÷&FW'2öbÖvæ—GVFR6†÷'Gçâ(	B¢§F†Rv—2Œ9r6ÖÆÆW"F†âF†BÂæBF†—0¢'VÆÆWBv2w&öær…"ÕsF2†’Â##bÓ‚ÓR’â¢¢F†÷6R&RF†R§&V6—Rw2¢f–wW&W2æBF†R&V6—P¢Ö—76W2“BãRRöbF†R&ÆööÒB&—&–U÷vW7FÂ6÷VçF–ærc’ãrRöbF†R—†VÇ2fÆ÷vW"–çFV@¢2F†RÆçB—B—2&V–ær6ö×&VBv–ç7BâÖV7W&VB'’7V'G&7F–öâÂF†R&ÆööÒ—2¢£ã#’ð¢ãƒròãsb¢¢B&—&–U÷vW7Fò&—&–U÷6÷WF†ò&—fW%ö&æ¶âF†R&V6—Rf–wW&W2&P¢¶WB&V6W6RF†R##bÓ‚ÓB&6VÆ–æR—2öâF†VÒà¢Ò¢¤G&r6ÆÇ2W†6VVBF†R(šBƒ'VFvWBBf÷W"7FF–öç2¢¢(	B&—&–U÷vW7F“rFW6·F÷ò“@¢Öö&–ÆRÂw&VVå÷G&VV“óƒ‚Âf÷&·6ƒróƒ"Â6÷WF…÷vFW&ƒRóƒ2â¢¥F†—2—2æWr–æf÷&ÖF–öâÀ¢æ÷BæWrfVÇB¢£¢F†R'VFvWB†2öæÇ’WfW"&VVâÖV7W&VBBF†R7vâ7FF–öâÂv†W&R—@¢76W2BcRóc"Â6òæö&öG’†B7FööBç—v†W&RVÇ6Rv—F‚F†R6÷VçFW"'Vææ–ærâ&V6÷&FVB–à¢$ôDÔv–ç7B"ÕsRÂv†–6‚÷vç2F†RG&rÖ6ÆÂv÷&²à ¢¢¥v†B—2äõB–âF†—2&6VÆ–æRÂ7FFVBÆ–æÇ’â¢¢F†R‚Ö†—2'V'&–266÷&Rsã"Ç6ò6·2f÷"—0¢¢¦æ÷B'Vâ¢¢âF†R&÷Fö6öÂ&WV—&W27&—F–2F†BF–Bæ÷Bw&—FRF†R6öFRVæFW"&Wf–WrÂæBF†P§'VâF†B'V–ÇBF†R†&æW726ææ÷B&RF†B7&—F–2v—F†÷WBÖ¶–ærF†R66÷&RÖVæ–ævÆW72â—B—0§&6VÆÆVB2$ôDÔ¢¥"Ôs¢¢æBF†R&6VÆ–æR—2–æ6ö×ÆWFRVçF–Â—BÆæG2à ¢ÒÒÐ ¢22v†BW†—7G2æBv÷&·0 §ÂF†–ærÂ7FFRÀ§ÂÒÒ×ÂÒÒ×À§Â&W÷6—F÷'’66fföÆBÂ¢¦FöæR¢¢(	BgVÆÂG&VRW"Fö72õÄâæÖFÀ§Â66†VÖ2‡7G'V7GW&RÂ6÷W&6RÂ66VæR’Â¢¦FöæR¢¢(	B†6W2ÂF–W'2Â&–v‡G2vF–ærÂ66VæRÖ÷væVBFFW2À§ÂFööÇ2÷fÆ–FFRç–Â¢¦FöæR¢¢(	B66†VÖÂ&VfW&VçF–ÂÂ6öæf–FVæ6R6öçG&7BÂW"×66VæRFFRvFW2Â†6RÖ÷fW&ÆÂWö6‚6÷fW&vRÂ&VÆV6R&Æö6¶–ærÂÆ–6Vç6R²&–v‡G2vF–ærÂ7FÆVæW72ÂV&Æ—6‚'VFvWBÀ§ÂFööÇ2÷FW7E÷fÆ–FFRç–Â¢¦FöæR¢¢(	B“b6†V6·2ÂÆÂw&VVâÂ–æ6ÇVF–ær&ööbF†Bâƒ3b'V–ÆF–ær—2W†6ÇVFVBg&öÒF†Rƒ3R66VæRÂF†BÆ–&W'G’æÖ–ær'V–ÆF–ærFöW2æ÷B6÷fW"â–çfVçF–öâ—BæWfW"ÖVçF–öç2ÂF†BâGG&–'WFRF†R&6†WG—RæWfW"&VG26ææ÷B72v—F†÷WB6––ærv†BF†RÖW6‚FöW2–ç7FVBÂæBF†B&Ww&—F–ær&V6÷&Bw2&÷6RFöW2æ÷B&W÷'B—G2ÖW6‚27FÆRv†–ÆR6†æv–ærfÇVRF†RvVæW&F÷"&VG2FöW2ÂæBF†BâGG&–'WFRâ&6†WG—RFV6Æ&W2—B6öç7VÖW27GVÆÇ’Ö÷fW2F†R&ÖWFW'2v†Vâ—G2fÇVR6†ævW2ÂæBF†BâW†6ÇW6–öâ6'&–W2&V6öâæB6—FF–öâF†B&W6öÇfW2æB7F÷2&V–ærâW†6ÇW6–öâB—G2÷vâV&Æ–W7B66VæRÀ§ÂFööÇ2ö6†V6²ç6†Â¢¦FöæR¢¢(	BgVÆÂvFR'Vç2–â¢£ãB2¢¢Âæò&ÆVæFW"À§Â&W6V&6‚F÷76–W'2Â¢¦FöæR¢¢(	B‚&W÷'G2Âã3c´"Â6öÖÖ—GFVBfW&&F–Ò–âFö72÷&W6V&6‚öÀ§Â6÷W&6R&V6÷&G2Â¢£#R¢¢Âöbv†–6‚¢£B¢¢6''’v–&6²6æ6†÷B(	BF†RF‡&VRFFVBv—F‚F†R'&–FvRÆÂFòÂæB6òFöW2F†R÷7BÖöff–6RvRÀ§Â7G'V7GW&R&V6÷&G2Â¢£ƒB–âF†Rƒ3R66VæR¢¢(	Bsb&RÖW†—7F–ærWf–FVæ6R&V6÷&G2ÇW2‚f—6–&Ç’FvvVBæöç–Ö÷W2&V6öÖÖVæFVB–æf–ÆÂ&V6÷&G3²&V6÷&B6÷VçBæB‡—6–6Â×&ööb6÷VçB&R6W&FVÇ’&V6öæ6–ÆVBÀ§ÂFW'&–âWö6‡2Â&Vv—7G'’w&—GFVã²Sƒ3Eö†&&÷%ö7WF7F—fRÂvVöÖWG'’Æ–W'2¢¦æ÷B–WB'V–ÇB¢¢À§Â¢¤FGVÒ¢¢Â¢¥dU$”d”TB¢¢(	Bw&–v‡BÖFW&—fVBÂ†F†v’ÒæBõ4ÒÖ6†V6¶VBÂ$Õ2rãRÒÂ&RÖFW&—f&ÆRg&öÒG&6W2À§Â¢¤vVæW&F÷"—VÆ–æR¢¢Â¢¥tõ$µ2¢¢(	B–ææVB&ÆVæFW"BãRã2Âg&ÖU÷FfW&æÂC“b×G&’6Vvæ6‚g&öÒF†R&V6÷&BÆöæRÀ§Â¢¦g&ÖUöGvVÆÆ–æv¢¢Â¢¤%T”ÅB##bÓ‚ÓÂäò$T4õ$BU4U2•B”UB¢¢(	BF†R&6†WG—RF†BVæ&Æö6·2†÷W6W3¢óãRó"7F÷&W—2Â¶æVRvÆÂæBv&ÆRÖVæBGF–2v–æF÷rÂ&V"VÆÂ&VBöfbF†Rfö÷G&–çBöÇ–vöâÂ7Fö÷÷"6ÖÆÂ&ööfVB÷&6‚ÂæB6öç7G'V7F–öæf–æÆÇ’Ö÷f–ærfW'F–6W2‡7GVBÖöGVÆRÆ6W2F†R÷Væ–æw2Â6Æ&ö&B'WGB¦ö–çG2ÆæBöâ7GVBÆ–æW2Â'&6VBg&ÖW2vWBF†Rv—'B&æB&ÆÆööâg&ÖR†2æòÆ–æRf÷"’âvöÆFVâ&×2²Fö72õ$U4T$4‚ö&6†WG—RÖg&ÖUöGvVÆÆ–ærçæv²#C‚Ós3G&—2W"†÷W6Râu$õTäEô4ôåD5C¢W&–ÖWFW&fW&–f–VBv–ç7BF†RÖW6‚(	BWfW'’VFvRöbF†Rfö÷G&–çBöÇ–vöâ6'&–W2vÆÂB¢ÒÂv÷'7BvãÖÒÂæ÷F†–ær&VÆ÷rF†R&6RöbF†RvÆÇ2À§Â¢¦÷WF'V–ÆF–æv¢¢Â¢¤%T”ÅB##bÓ‚ÓÂäò$T4õ$BU4U2•B”UB¢¢(	BF†R†–v†W7BÖ6÷VçB×W"ÖVff÷'B&6†WG—R–âF†RÆâÂæBF†RöæRF†Bv—fW2F†RF÷vâ–&G2–ç7FVBöbV–v‡B—6öÆFVBV&Æ–2†÷W6W2âdÔ”Å’Âæ÷B6†S¢6öç7G'V7F–öæÆör÷Ææ²öÆ–v‡Eög&ÖRG&—fW2F‡&VRF–ffW&VçBvÆÂ&÷WF–æW2Â6†VB&öög2&Rf—'7BÖ6Æ72&F†W"F†âfÆÆ&6²Â÷Vå÷6–FW6GW&ç2ç’7V'6WBöbVÆWfF–öç2–çFò÷7G2ÖæB×ÆFRÂæBFö÷&—2æöæRöÖâ÷7F&ÆR÷vvöâ(	B&ööÆVâ—2&VgW6VBv—F‚ÖW76vR6––ærv‡’â&ö&EövöÖÆöæR—2F†Rv†öÆRF–ffW&Væ6R&WGvVVâ7F&ÆRæB6÷&â7&–"âf—fRvöÆFVâf&–çG2g&öÒã#RÒ&—g’Fò2Ò†÷FVÂ7F&ÆRÂ#s"Ó#‚G&—3²u$õTäEô4ôåD5C¢W&–ÖWFW&fW&–f–VBöâÄÂd•dRv–ç7Bw&÷VæB×ÆæRTDtU2&F†W"F†âfW'F–6W2‡F†Rf—'7B6†V6²6ö×&VBfW'F–6W2æB&öGV6VBfÇ6Rf–ÇW&W2öâ2ÒvÆÂF†B—2öæRVB’âF—66†&vW2F†R7F&ÆR†ÆböbÃ²¢§F†R–&B†Æb7F—2÷Vâ¢¢(	BfVæ6RÆ–æRv—F‚GvòvFWv—2—2âVæ6Æ÷7W&RÂæB'V–ÆF–ær—B÷WBöbâ÷WF'V–ÆF–ærv÷VÆB&R6ÆÆ–ærfVæ6R'V–ÆF–ærÂ6òÃæVVG2ä%$õt”är&F†W"F†â&W6öÇf–ærÀ§Â¢¥6÷WF‚vFW"7G&VWB¢¢Â¢¤%T”ÅB##bÓ‚Ó¢¢(	B6—‡FVVâ6öÖÖW&6–Â&V6÷&G2ÆæBF†RF÷vâw2'W6–æW727G&VWBÂv†–6‚F†RÖöFVÂ†VÆBæöæRöc¢V6²w27F÷&RÂ&÷F‚æWw7W"öff–6W2Â†&ÖöâbÆööÖ—2ÂÖF÷&R&VV&–Vâw2Æör†÷W6RÂ&FW2w2V7F–öâ&ööÒÂF†R&VV&–Vâ†öÖW7FVBÂFöÆRw2v&V†÷W6RÂ&÷F‚6'VçFW"6†÷2Âg&VFW&–6²F†öÖ2ÂF†RöÆB&æ²'V–ÆF–ærÂ'W–æRb¶–Ö&ÆÂÂ¢â‚â¶–ç¦–RÂ¦öæW2ÂæBF†öÖ26‡W&6‚öâÆ¶RâöæRfö÷G&–çB—2Wf–FVæ6R„6'VçFW"w2b‚#gBÆör6†÷(	BF†RFF6WBw24T4ôäB&VÂfö÷G&–çB“²f–gFVVâ&R–çfVçFVB–ç6–FRF†RFö7VÖVçFVBSRgB6÷WF‚vFW"Æ÷B6â¢¥v†BF†—27G&VWB¶æ÷w2—2§v†ò¢æB§v†W&R¢ÂæBÆÖ÷7BæWfW"¦†÷r&–r¢â¢¢Gvò&V6÷&G26''’&Wf–Wu÷&WV—&VF‡F†R&VV&–Vç2Âv†÷6R†—7F÷'’'Vç27G&–v‡B–çFòF†RVwW7Bƒ3R&VÖ÷fÂæBF†R&W6W'fF–öâ&RÖV×F–öâ’(	Bv†–6‚&Æö6·2F†Rƒ3R66VæRg&öÒ&VÆV6VFVçF–Â6öç7VÇFF–öâ†Vç2âGvòVç&W6öÇfVB&VG2&RfÆvvVBöâF†R&V6÷&G2F†V×6VÇfW3¢v†WF†W"†&ÖöâbÆööÖ—2w2'V–ÆF–ær•2F†R¤6†–6vòFVÖö7&B¢w2'V–ÆF–ær‡F†W’6—B3rÒ'BæBæG&V2v—fW2æò6–FR’ÂæBv†WF†W"†–Æò6'VçFW"w2Æ¶R7G&VWBÆör6†÷7F–ÆÂ7FööBgFW"†R'V–ÇBöâ6÷WF‚vFW"–âƒ32À§Â¢¥&VæFW&W"¢¢Â¢¥tÄ´$ÄRäBäd”t$ÄR¢¢(	BF‡&VRæ§2#ãƒRãfVæF÷&VBÂö–çFW"ÖÆö6²²F÷V6‚Â6öæf–FVæ6Rf–WrÂ&÷fVææ6R÷WÂÆ—fR6ö×72æBæ÷'F‚×W÷fW'f–WrFW&—fVBg&öÒF†RÆöFVB†V–v‡Ff–VÆBæB7G'V7GW&Rfö÷G&–çG2À§Â¢¤æf–vF–öâ–æFW‚¢¢Â¢¤4ôÕÄUDRdõ"4ôÔÔ•EDTBDD¢¢(	B6WGF–æw26V&6†W2ÆÂsb66VæR7G'V7GW&W2æBÆÂf÷W"fW&–f–VB–çFW'6V7F–öç2Âv—F‚Æ–6W2æB&V6÷&FVBÆö6F–öâFW‡C²–çFW'6V7F–öâ÷6—F–öç2&R6ö×–ÆVBg&öÒFF÷G&6W2÷7G&VWEö6öçG&öÂæ§6öæ&F†W"F†â6÷–VB–çFò&VæFW&W"6öFRâ6ö×72Â÷fW'f–WrÖæBF†RÆ—fRƒ3Rö7W'&VçB7G&VWBÖæÖR&VF÷WB&R–æFWVæFVçFÇ’W'6—7FVçBFövvÆW2âf÷W'F‚W'6—7FVçB6WGF–ær7v—F6†W2WfW'’f—6—F÷"Öf6–æræf–vF–öâÖV7W&VÖVçB&WGvVVâ–×W&–Â‡F†RFVfVÇC¢gBÂÖ’Â×‚’æBÖWG&–2†ÒÂ¶ÒÂ¶Òö‚’v—F†÷WB6†æv–ærF†RÖWG&–266VæRFFâF†R&VF÷WB&W÷'G2F†R6÷'&–F÷"VæFW&fö÷BÂâ–çFW'6V7F–öâv†VâGvò6VçG&VÆ–æW2&RæV"ÂæBF†RæW‡B7&÷727G&VWBWFòsÒò#3gB†VBâÀ§Â¢¥6Öö¶R¢¢Â¢¥52##bÓ‚ÓB¢¢(	BFööÇ2ö6†V6²ç6†w&VVâÂæBæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6w&VVâB&÷F‚&VÆV6Rf–Ww÷'G2–âÆÂf÷W"6öÖ&–æF–öç2F†RvFR6·2f÷#¢6÷W&6RG&VR¢£#BÖö&–ÆRò#FW6·F÷¢¢ÂV&Æ—6†VBÖ—'&÷"¢£#Bò#¢¢Â¦W&òvRW'&÷'2F‡&÷Vv†÷WBÂv—F‚F†RF÷vâB#c&V6÷&G2â'Vâ2f÷W"6W&FRf÷&Vw&÷VæB6öÖÖæG2&V6W6RgVÆÂ72W†6VVG2FVâÖ–çWFW2âF†R†—7F÷'’&VÆ÷r—2F†R&V6÷&Böb†÷rF†÷6R76W'F–öç2vW&RV&æVBâ¢¥52##bÓ‚Ó2ÂæBf÷"F†Rf—'7BF–ÖRv–ç7BF†Rf–ÆW2F†B7GVÆÇ’6†—â¢¢FööÇ2ö6†V6²ç6†—2w&VVâÂæBæöFRFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§676W2¢£3c76W'F–öç2¢¢B&÷F‚&VÆV6Rf–Ww÷'G2ƒ3“ƒsƒæB#ƒƒƒ’v—F‚¦W&òvRW'&÷'2(	B'VâGv–6RÂöæ6Rv–ç7BF†R6÷W&6RG&VRæBöæ6Rv—F‚Ò×V&Æ—6†VFv–ç7BF†RÖ—'&÷"â¢¥F†R6V6öæB'Vâ—2F†RöæRF†BÖGFW'2æB—BF–Bæ÷BW†—7BVçF–Âæ÷râ¢¢6–FV6"w2vÇFbóÆæÖSâævÆ&&W6öÇfW2FòF†RTä4ôÕ$U54TBÖ7FW'2–âF†R6÷W&6RG&VRæBFòF†RÖW6†÷B²VçF—6VBFW&—fF—fW2öâF†R6—FRÂ6òæ÷F†–ærF†B&â†BWfW"ÆöFVB6ö×&W76VB76WB(	BæB&VæFW&W"'VrF†BöæÇ’W†—7G2–âF†RVçF—6VBF‚6öÆÆ6VBÆÂ#C"7G'V7GW&W2Fò"Ò&÷†W2öâF†RÆ—fR6—FRf÷"6WfW&ÂF—2ÂF‡&÷Vv‚GvòGFV×FVBf—†W2Âv—F‚F†RvFRgVÆÇ’w&VVâF†Rv†öÆRF–ÖRâF†R6—¦R76W'F–öâv2Ç6òÖV7W&–ærF†RDÄÄU5B'V–ÆF–ær–âF†R66VæRÂv†–6‚76W2v—F‚öæR6÷'&V7B'V–ÆF–æræB#C'&ö¶VâöæW3²—Bæ÷rÖV7W&W2WfW'’7G'V7GW&Rv–ç7B—G2÷vâ&V6÷&BÂ–æ6ÇVF–ær—G2Fö7VÖVçFVBvÆÂ†V–v‡Bâ&V–çG&öGV6–ærF†RfVÇBf–Ç2F†RæWr6†V6·2'’æÖRöâÆÂ#C"âFööÇ2ö&¶Rç6†'Vç2F†RV&Æ—6†VB6Öö¶RgFW"V&Æ—6‚âG&r6ÆÇ2æBG&–ævÆW2BF†R7vâ7FF–öã¢¢£S’ò33"ÃCSR¢¢FW6·F÷Â–ç6–FRF†RƒòÃÃgVÆÂÖFWF–Â'VFvWBâF†RGvò†ÇfW27F–ÆÂ'Vâ26W&FRf÷&Vw&÷VæB6öÖÖæG2Â&V6W6RgVÆÂ72W†6VVG2FVâÖ–çWFW2âÀ§Â¢¤fÆ÷&¢¢Â¢§F†R7v&B—2–ã²F†RfÇ6Rf"Öf–VÆB7W&f6R—2÷WB¢¢ƒ##bÓ‚Ó’(	B&VæFW&W'2÷vV"ö§2öfÆ÷&æ§6ÆçG2F†Rw&Ö–æö–BÖG&—‚Âf÷&'2ÂVÖW&vVçG2æBÆ÷r6‡'V'2g&öÒFFöfÆ÷&öâ§VÇ’†VæöÆöw’&VÖ–ç2Væf÷&6VB–â&VæFW&W"æBFFâæV"öÖ–FFÆRÆçG2&ö÷BöâF†RW†7BFW'&–â7W&f6RæBvFW"VÖW&vVçG2öâF†RvFW"7W&f6RâF†Rf÷&ÖW"6öÆ–B6æ÷’BÆçB×F÷†V–v‡Bv2F†R&VçB6V6öæBw&÷VæB6VVâöâ&VÂFWf–6W3²—B—2&VÖ÷fVBÂæBVç&W6öÇfVBF—7FçB&—&–R6öÆ÷W"æ÷r7F—2öâF†R6öÆRFW'&–â7W&f6R„Ãƒ’â¢¥6–æ6R##bÓ‚Ó2V6‚6öÖ×Væ—G’—2ÆçFVBB—G2÷vâ&V6÷&FVB6÷fW"æÖG&—…ög&7F–öæ¢¢(	Bf–VÆBF†R&V6÷&G26'&–VBÂF†RfÆ–FF÷"vFVBæBF†R&VæFW&W"†BæWfW"6¶VBf÷"(	BæBV6‚—27Æ—B'’F†RV&Æ—6†VB7V'7G&FVöb—G27V6–W2Â6òfÆöF–ærÖÆVfVBVF–2—2ÆçFVB÷fW"vFW"æBæWfW"öâF†R&æ²—Bv27FæF–æröââÀ§Â¢¥F†Rw&÷VæBw26Æ–×2Â–âF†R¢¢Â¢¦FöæR¢¢ƒ##bÓ‚Ó’(	BF†RWf–FVæ6RæVÂw2¥F†Rw&÷VæB–÷R&R7FæF–æröâ¢&VG2w&FVB6Æ–×2öfbFW'&–å÷7V2æ§6öæÂFW&—fVBW"66VæR'’6ö×–ÆU÷66VæRç–æB&RÖFW&—fVB'’6†V6²ç6†²F†R6ÖR6Æ–6RFFVB&V6öæ–æræBvVöÖWG'’×7FFR6†V6·26òF†÷6R&÷w2&RæòÆöævW"6–ÆVçB&öÖ—6W2âÀ§Â¢¥v†B6÷W&6R—2Â–âF†R¢¢Â¢¦FöæR¢¢ƒ##bÓ‚Ó’(	B6—FF–öç2æ÷r6''’F†RFö7VÖVçBÖöFW&âvR&W&–çG2†G&ç67&–&W6’÷"F†R&VF–ærF†B—B&W&–çG2æöæRÂÇW2V6‚6÷W&6Rw2÷vâv†Eö—E÷7WÆ–W6òv†Eö—EöFöW5öæ÷E÷7WÇ–Â6òF†RÆFFW"f—6—F÷"6VW2–æ6ÇVFW2F†R&V6öâ—B—2F†RÆFFW"âÀ§Â¢¤Æ–&W'F–W2Â–âF†R¢¢Â¢¦FöæR¢¢(	BF†RWf–FVæ6RæVÂÆ—7G2F†RÆ–&W'F–W2FW&—fVBg&öÒFö72ôÄ”$U%D”U2æÖF'’FööÇ2ö6ö×–ÆUöÆ–&W'F–W2ç–æB&RÖFW&—fVB'’6†V6²ç6†²F†R&÷fVææ6R÷W6†÷w2F†RöæW2F¶Vâv—F‚F†R'V–ÆF–ær–÷R&R–ç7V7F–æs²æBF†RvFR6†V6·2F†RFö7VÖVçB¦f÷"v2¢–â&÷F‚F—&V7F–öç2(	B&VgW6–ærç’6öæ¦V7GW&ÂfÇVR†fö÷G&–çBÂ÷6—F–öâÂFW'&–â6Æ–ÒÂ÷"7FFVBf÷&ÒGG&–'WFR’F†BæòÆ–&W'G’FÖ—G2FòÂæBWVÆÇ’ç’GFW7FVBfÇVRF†R&6†WG—R÷"FW'&–âvVæW&F÷"æWfW"&VG2æBæòÆ–&W'G’÷vç2WFòÆVf–ær÷WBÀ§Â¢¥F†RÆGFVB7G&VWBÖöGVÆR¢¢Â¢¤ÔT5U$TBäBd•4”$ÄR¢¢(	B7G&VWB6÷'&–F÷'2æBv–GF‡2&VÖ–â6öÖÖ—GFVB–âFF÷G&6W2÷fV7F÷'2÷7G&VWEö6÷'&–F÷'5óƒ3Bæ§6öæÂv—F‚Æ¶RæB&æFöÇ‚æÖVBg&öÒ6öÖÖ—GFVB6öçG&öÂæB&RÖFW&—fVBöffÆ–æR'’6†V6µ÷7G&VWEöÖöGVÆVâFF÷7G&VWG2óƒ3Ræ§6öææ÷rFG26WfVçFVVâFFVBF‡2æB¶VW2F†RƒgBÆVvÂ6÷'&–F÷"6W&FRg&öÒÃs’w2Rã‚ÓãRÒf—6–&ÆRG&fVÆÆVB7G&—2â6ö×–ÆU÷66VæRç–¦ö–ç2F†V—"6—FF–öç2–çFòF†R6–FV6"–æFWƒ²F†R&VæFW&W"G&W2F†VÒöâF†Rw&÷VæBÂ6Æ—2F†VÒBvFW"æB6ÆV'2fVvWFF–öâöæÇ’g&öÒF†RG&6²â6÷WF‚vFW"æBÆ¶R&VB2&–æ6—Âw&FVBV'F‚Â÷&F–æ'’7G&VWG22v÷&âæF—fRV'F‚ÂæBæòw&fVÂÂÆæ²&öGv’÷"†&Bf–ær—26†÷vââæ÷'F‚vFW"w27W'fRæBWfW'’'WB÷G&6²v–GF‚&VÖ–âW‡Æ–6—FÇ’6öæ¦V7GW&ÂâÀ§Â¢¥F†RÆ¶R6†÷&R¢¢Â¢¥E$4TBÂäõB%T”ÅB¢¢(	B6†÷&VÆ–æRævVö§6öæ¢F†R†&&÷W"&V6‚ÂF†Rƒ3B7WBÂF†RöÆB6÷WF‡v&B6†ææVÂÂF†R6æB&"2â—6ÆæBæBF†RÖ–æÆæB6†÷&RÂR³3N(
b³Ssöfbw&–v‡Bƒ3BâfV7F÷'2öæÇ“²æòVÆWfF–öâÂæòÖW6‚Âæ÷F†–ærV7BöbF†R&÷‚&VæFW'2–WBÀ§Â¢¥V&Æ—6†VB¢¢Â6—FRö6†–6vòóFBöƒBã3Ô"öb#RÔ"'VFvWB’²F–ÆRöâF†R6†–6vòÆæF–ærvRÀ§ÂW†6ÇW6–öç2ÂBFFRÖwV&FVB7G'V7GW&W2²BÖ—FVÒvF6‚Æ—7B(	B¢¦–âF†RvÆ·F‡&÷Vv‚¢¢6–æ6R##bÓ‚Ó„Wf–FVæ6RæVÂÂ%v†B—2æ÷B†W&R"’Â6—FF–öç2¦ö–æVBÂæBæ÷r†VÆBFòF†R6ÖR6—FF–öâ'VÆR27G'V7GW&R&V6÷&BŒ*r#b’À ¢226÷'&V7F–öç2ÖFRgFW"F†Rf—'7BÆ—fRÆöö° ¤¶Wf–â÷VæVBF†RFWÆ÷–VB'V–ÆBöâ&VÂ†&Gv&RæBf÷VæBGvòF†–æw2†VFÆW72FW7F–ær†@¦Ö—76VBâ&÷F‚&Rf—†VC²&÷F‚&RF†R¶–æBöbF†–æröæÇ’&VÂf–WvW"6F6†W2à ¢Ò¢¥F†R'V–ÆF–ær&VæFW&VBW&R&Æ6²öâ&VÂuRâ¢¢F†R6öæf–FVæ6R6†FW"6ö×WFV@¢vV–v‡BÒb‡d6öæf–FVæ6R’¢T6öædÖöFVWfVâv†VâF†Rf–Wrv27v—F6†VBôdb(	BæBæâ¢ã ¢—27F–ÆÂææÂv†–6‚ö—6öæVBF–fgW6T6öÆ÷&F‡&÷Vv‚F†RÖ—‚âvVöÖWG'’&V6†–ær&F6€¢v—F†÷WBô4ôäd”DTä4VÆVfW2F†RGG&–'WFRVæ&÷VæBÂæBâVæ&÷VæBGG&–'WFR—2æ÷B&VÆ–&Ç¢¦W&òöâ&VÂ†&Gv&RF†Rv’—B—2VæFW"6ögGv&R&7FW&—6W"âF†R6†ææVÂ—2æ÷p¢6æ—F—6VBBF†RfW'FW‚7FvRæBF†RöfbF‚—2wV&FVB&Vf÷&R—B&VG2ç—F†–ærà¢Ò¢¤vVÆÂÖFö7VÖVçFVB'V–ÆF–ærv2&VæFW&VB2æV"×F÷FÂwVW77v÷&²â¢¢vÆÅö†V–v‡EöÖæ@¢&ööe÷G—VvW&RFvvVB6öæ¦V7GW&Æv†–ÆRF†V—"÷vâæ÷FW2vfRG—öÆöv–6Â&V6öæ–ær(	@¢'GvògVÆÂ7F÷&–W2BG—–6ÂW&–öBfÆö÷"†V–v‡B"Â&v&ÆR—2F†RæV"×Væ—fW'6Âf÷&Òf÷"F†P¢G—RæBW&–öB"âF†B—2F†R'&–Vbw2FVf–æ—F–öâöb–æfW'&VFÂæ÷Böb6öæ¦V7GW&Æâv÷'6RÀ¢F†RÖ76–ær'VÆRFöö²F†Rv÷'7B6öæf–FVæ6R7&÷72F†Rfö÷G&–çBFöòÂ6òâVæ¶æ÷vâ4•¤P¢F—F†W&VBF†RVçF—&R'V–ÆF–ær–çFòv†÷7BÖ76–ærâ6—¦RæB6†&7FW"&RF–ffW&VçB¶–æG2ö`¢æ÷BÖ¶æ÷v–æs¢vRÔ'VâFö7VÖVçG2Gvò×7F÷&W’v†—FRg&ÖR'V–ÆF–ærv—F‚'&–v‡BÖ&ÇVR6‡WGFW'2À¢æBæò6÷W&6Rv—fW2F–ÖVç6–öââF†RÖ76–æræ÷rföÆÆ÷w2F†RGG&–'WFW2F†B6’v†BF†P¢'V–ÆF–ærv3²F–ÖVç6–öæÂVæ6W'F–çG’—26'&–VB–âF†R6–FV6"Âv†W&RF†R÷W6†÷w2—Bà¢VæFW'7FF–ærv†BvR¶æ÷r—22×V6‚Ö—7&W&W6VçFF–öâ2÷fW'7FF–ær—Bà¢Ò¢¥F†R&—&–RV&VBFò&R6V6öæBFW'&–âÆ–W"â¢¢F†Rf"fVvWFF–öâ6–×Æ–f–6F–öâv0¢6öÆ–B†÷&—¦öçFÂ6†VWBBÆçB×F÷†V–v‡Bâöâ&VÂ†&Gv&R—B†–B'V–ÆF–ærf÷VæFF–öç0¢æBÆçB&ö÷G2v†–ÆRF†RvÆ¶W"&VÖ–æVB6÷'&V7FÇ’öâF†R7GVÂ†V–v‡Ff–VÆB&VÆ÷r(	BÖ÷7@¢6ÆV&Ç’BF†R&—fW"&æ²æBW†6†ævR6öffVR†÷W6RâF†R6†VWB—2&VÖ÷fVBÂæ÷B&öÖ÷FVBFð¢FW'&–ââvÆ¶W"Â'V–ÆF–æw2Â7G&VWG2ÂG&VW2æBFWF–ÆVBfÆ÷&æ÷r6†&RöæRW‡Æ–6—B7W&f6P¢6×ÆW#²VÖW&vVçB&ö÷G2W6RF†RvFW"7W&f6RâF†Rf"f–VÆB—2FW'&–âFW‡GW&RVçF–Â¢÷&÷W2ÂFW'&–â×&ö÷FVB&WÆ6VÖVçB6â&R'V–ÇB„Ãƒ’à ¢22v†BFöW2æ÷BW†—7B–W@ ¢Ò¢¥F†RgVÆÂccR×&ööb–çfVçF÷'’—2æ÷B'V–ÇBâ¢¢6÷WF‚C‚ÇW2æ÷'F‚cæöç–Ö÷W26Æ÷G2&Rf—6–&ÆS²&VÖ–æ–ær&6VÇ2Â6ö÷&F–æFVBv÷&ÆBW‡FVç6–öç2æBF†R3RÖfÖ–Ç’6æöæ–6Â&6†WG—RÆ–'&'’&R7F–ÆÂ÷VââF†R&V6öæ6–Æ–F–öâæBfÖ–Ç’7&÷77vÆ²&R6öÖÖ—GFVB†æFöfb6öçG&öÇ2à¢Ò¢¤æòFW'&–ââ¢¢F†R66VæR7FæG2öâfÆBÆæS²F†R3×¦öæR†V–v‡Ff–VÆB7V2W†—7G2–âF†P¢&W6V&6‚F÷76–W"'WB†2æ÷B&VVâGW&æVB–çFòFFâF†—2—2F†RæW‡B7FvRà¢Ò¢¤æòfÆ÷&÷"fVæ&V6÷&G2â¢¢F†RÆWGFW2æBF†RÆ6VÖVçBF&ÆRW†—7B–âF†RF÷76–W'2öæÇ’à¢Ò¢¥FW'&–âæBF†R&—fW"æ÷rW†—7B¢¢ÂG&6VBg&öÒw&–v‡Bƒ3BF‡&÷Vv‚F†R6ÖRff–æRF†@¢f—†VBF†RFGVÒâF÷FÂÆæB&VÆ–Vb7&÷72F†Rv†öÆRcCÒ&÷‚—2¢£Bã3gB¢¢(	BF†B—2æ÷B¢6–×Æ–f–6F–öâÂ—B—2F†R6—FRâF†RF÷76–W"w27VvvW7FVBN(	3‡‚fW'F–6ÂW†vvW&F–öâv0¢&VgW6VB&V6W6R—B6öçG&F–7G2Fö72ôUô4…2æÖFæBÄ”$U%D”U2Ã2à¢Ò¢¥F†R&æ²&öf–ÆR—2F†RÆ&vW7BVç6÷W&6VB77V×F–öâ–âF†R'V–ÆBâ¢¢æò¦öæR–âF†RFW'&–à¢F÷76–W"v—fW2&æ²§&öf–ÆR¢BÆÃ²F†RbÒf6RæB—G2V6RÖ÷WB6†RvW&R6†÷6Vâ'FÇ¢&V6W6RfÆBFöRÆVfW2F†R£Ó6öçF÷W"(	Bv†–6‚•2F†RG&vâvFW&Æ–æR(	B–ÆÂÖ6öæF—F–öæV@¢v–ç7BF†Rw&–Bà¢Ò¢¦6†–6vö&6†—FV7GW&V†—7F÷'’æ6öÖ6—FW2æ÷F†–ær¢¢f÷"F†RGvò&W7BVÆWfF–öâf–wW&W2–âF†P¢F÷76–W"Âv†–6‚—2v‡’æòÆæBVÆWfF–öâ–âF†—2'V–ÆB—2FvvVBFö7VÖVçFVFà¢Ò¢¥Æ6VÖVçB—2&VÂ'WB6ö'6Râ¢¢ÆÂV–v‡B7G'V7GW&W2æ÷r6''’7W'fW–VB6ö÷&F–æFW2&F†W ¢F†âçVÆÇ2ÂB&÷WB+#Ò(	BF†RvV÷&VfW&Væ6Rw2W'&÷"Âæ÷BâFF—F–öæÂwVW72âF‡&VRöbF†VÐ¢…vöÆbö–çBFfW&âÂÖ–ÆÆW"†÷W6RÂvÆ¶W"w2ÖVWF–ær†÷W6R’†fRæò7W'f—f–ær–çFW'6V7F–öâæ@¢&RFW&—fVBg&öÒF†R6öæfÇVVæ6RæBF†RÖöFW&â&æ²Âv—F‚Æ&vW"æBF–ffW&VçFÇ’6†V@¢Væ6W'F–çG’7FFVBöâV6‚à¢Ò¢¥vÆ¶W"w2ÖVWF–ær†÷W6RÖ’&RF†Rw&öær'V–ÆF–ærâ¢¢F†RvW7BÖ&æ²FW7F–Ööç’FW67&–&W2ƒ3¢æBF†Ræ÷'F‚Ö&æ²6Æ–Ò—2FFVBƒ3BÂv†–6‚—2v†B–÷Rv÷VÆB6VR–bF†R6÷W&6W2FW67&–&P¢GvòF–ffW&VçB'V–ÆF–æw2&÷WBSÒ'B7&÷72&—fW"â÷6—F–öâ—2FvvVB6öæ¦V7GW&Æ ¢æBF†R&V6÷&B6—26ò–âF†Rf—'7BÆ–æRà ¢22F†RFGVÒ—2fW&–f–V@ ¦FFöFGVÒæ§6öææ÷r6'&–W2fW&–f–VC¢G'VV¢¢¤RCCss"ãrÂâCc3s3“Rã‚„U4s£#c“b’Ð£Cãƒƒcs#ÂÓƒrãc3s“S¢¢(	BF†Rf÷&·2§Væ7F–öâ2G&vâöâw&–v‡Bƒ3BÂf—GFVBv–ç7BV–v‡@¦ÖöFW&â6öçG&öÂö–çG2…$Õ2rãRÒ’Â7&÷72Ö6†V6¶VBv–ç7Bâ–æFWVæFVçFÇ’vV÷&VfW&Væ6V@¤†F†v’ƒSrã’Òw&VVÖVçB’æBF†RÖöFW&âõ4Ò&—fW"§Væ7F–öâƒ3’ãBÒ’âF†R'&–Vbw2Æ6V†öÆFW §v2¢£#2Òöfb¢¢âgVÆÂÖVÖó¢Fö72õ$U4T$4‚öFGVÕöFW&—fF–öâæÖF²F†RFW&—fF–öâ&R×'Vç2g&öÐ¦6öÖÖ—GFVBG&6W2f–FööÇ2÷&VFW&—fUöFGVÒç–Âv†–6‚6†V6²ç6†Væf÷&6W2à ¥7G'V7GW&R÷6—F–öç27F–ÆÂ6''’7–Ö&öÆ–5öÆö6F–öæv—F‚çVÆÂ6ö÷&F–æFW2(	BF†W’vWBf–ÆÆVB0¦fö÷G&–çG2&RG&6VBF‡&÷Vv‚F†Rf—GFVBG&ç6f÷&×2–â3"²ÂV6‚6''––ærF†R+#Òv÷&¶–æp§Væ6W'F–çG’öbF†Rƒ3B6†VWG2–â—G2æ÷FRà ¢22f—†VB##bÓ‚Ó2(	BF†R6†ævVÆörv2'&ö¶Vâ%’ÔU$tRÂæB&÷F‚&VçG2vW&Rw&VVà ¢¢¦&VæFW&W'2÷vV"ö§2ö6†ævVÆöræ§6F–Bæ÷B'6RöâÖ–æÂæBæV—F†W"F–B—G2V&Æ—6†V@¦Ö—'&÷"â¢¢F†Rv†Bw2ÖæWrF"–×÷'G2—BÂ6òF†RF"v2FVBöâF†RFWÆ÷–VB6—FS²ÖævW"æ@§F†RöÆV6BæÆ—fRÆVæ6†W"'6RF†RÖ—'&÷"Â6òF†—2&ö¦V7B&W÷'FVBæò&VÆV6W2BÆÂâc@¦VçG&–W2Â&6²FòF†Rf—'7B'V–ÆF–ærÂvW&R–âF†Rf–ÆRæB&V6†–æræö&öG’à ¢¢¤W†7FÇ’öæRÒÒÆv2Ö—76–ær¢¢(	BF†RFW&Ö–æF÷"öbccB¢%GvVçG’×F‡&VR'V–ÆF–æw2vW&R7FæF–æp¦–âF†R7G&VWB"¢âWfW'’VçG'’&VÆ÷r—Bv2æW7FVB–ç6–FRF†BVçG'’w2—FV×6'&’Âv†–6‚—2v‡¦æöFR&W÷'FVBF†R7–çF‚W'&÷"BÆ–æRScRÂF†RVæBöbF†Rf–ÆRÂSCÆ–æW2g&öÒF†RFÖvRâ§6V6öæBVçG'’&öFRÆöærv—F‚GWÆ–6FRc¢cF¢Gvò'&æ6†W2f–æ—6†VB32Ö–çWFW2'BÂV6€§7F×VB—G2VçG'’öâ—G2÷vâ'&æ6‚ÂæBæV—F†W"¶æWrF†RçVÖ&W"v2F¶Vâà ¢¢¥F†RÖV6†æ—6Ò—2F†R'Bv÷'F‚¶VW–ærÂ&V6W6RæòW†—7F–ærvFR6÷VÆB†fR6Vv‡B—Bâ¢ ¦æv—FGG&–'WFW6ÖW&vW2F†—2f–ÆRv—F‚ÖW&vS×Væ–öæ(	BFVÆ–&W&FRÂFö7VÖVçFVB6†ö–6RÂ&V6W6P§Gvò'&æ6†W2V6‚&WVæF–ærâVçG'’6öÆÆ–FRWfW'’F–ÖRæBVæ–öâ¶VW2&÷F‚–ç7FVBö`¦6öæfÆ–7F–ærâ'WBF†RVæ–öâG&—fW"'Vç2EU$”ärD„RÔU$tRâÖW&vRcV3†FS†2Gvò&VçG2À¦6&SC“F6æBcs†C²¢¦&÷F‚'6RÂæBF†RÖW&vRöbF†VÒFöW2æ÷Bâ¢¢WfW'’vFR–âF†—0§&ö¦V7B'Vç2öâ6öÖÖ—B6öÖV&öG’w&÷FRâæ÷F†–ær&âöâF†R6öÖÖ—Bv—Bw&÷FRà ¢Ò¢¥F†R&W—"â¢¢F†RFW&Ö–æF÷"—2&W7F÷&VBâF†RGWÆ–6FVBVçG'’—2æ÷r¢§ccr¢¢æB6—G2BF†P¢F÷Âv†W&R—G2÷vâG6ƒ#£#bUD2ÂF†RæWvW7B–âF†Rf–ÆR’6—2—B&VÆöæw2âæòVçG'’ç–öæR†0¢&VBv2&VçVÖ&W&VB(	Bv†–ÆRF†Rf–ÆRv2'&ö¶VâÂæòVçG'’v2&VF&ÆRBÆÂà¢Ò¢¦FööÇ2ö6†V6²ç6†æ÷r'Vç2F†R6†ævVÆör6öçG&7B¢¢Â27FWÆ–¶Rç’÷F†W"âtTåE2æÖB†0¢Çv—2–ç7G'V7FVBâvVçBFò'Vâ6†V6²Ö6†ævVÆöræÖ§6'’†æB&Vf÷&RÖW&v–æs²†æB×'Vâ6†V6°¢—2W†7FÇ’F†RF†–ærÖW&vR×F–ÖR6÷''WF–öâWfFW2ÂæBF†Rf–ÆRF†BvFW2WfW'’6öÖÖ—BF–@¢æ÷BvFRF†—2öæRâF†RvVæW&–2§&VæFW&W"ÖöGVÆW2'6R¢7FWF–B6F6‚—B(	B2'6RW'&÷# ¢&VæFW&W'2÷vV"ö§2ö6†ævVÆöræ§6Âv†–6‚æÖW2f–ÆRæBæ÷BFVfV7Bà¢Ò¢¥F†R6öçG&7B6†V6²&VG2F†RÆ—FW&Âw24„R2FW‡B&Vf÷&RW†V7WF–ær—B¢¢Â&V6W6RW†V7WF–æp¢—B—2F†RvV¶W"FW7B–âGvòv—2â7vÆÆ÷vVBVçG'’—27F–ÆÂfÆ–Bö&¦V7BÆ—FW&ÂÂ6ò—BæVV@¢æ÷B&—6R7–çF‚W'&÷"BÆÂ(	B—B6â6–×Ç’fæ—6‚g&öÒF†R'&’v—F‚F†Rf–ÆRÆöF–æp¢6ÆVæÇ’âæBÖævW"æBF†RÆVæ6†W"æWfW"W†V7WFRF†—2f–ÆS²F†W’vÆ²—B'&6¶WBÖv&RÂ6ð¢F†R6†R•2F†R6öçG&7BâWfW'’VçG'’×W7B÷VâB'&6¶WBFWF‚²öæRF†B÷Vç2FVWW"v÷@¢7vÆÆ÷vVBÂæBF†RVçG'’&÷fR—B—2F†RöæRF†BÆ÷7B—G2FW&Ö–æF÷"âfW&–f–VBv–ç7BF†R&VÀ¢6÷''WFVBf–ÆRg&öÒÖ–æ¢¢&Æ–æR#S¢VçG'’ccB÷Vç2B'&6¶WBFWF‚2Âæ÷B(	B—B—2æW7FV@¢–ç6–FRVçG'’ccB†Æ–æR‚’Âv†–6‚—2Ö—76–ær—G2ÒÒÆ"¢âF†R†VFW"6÷VçBg&öÒF†RFW‡BvÆ°¢—2Ç6ò6ö×&VBv–ç7B4„ätTÄôræÆVæwF†Âv†–6‚—2v†B6F6†W2F†R6–ÆVçB†Æbà¢Ò¢¥v†BF†—27F–ÆÂFöW2æ÷B6÷fW"â¢¢F†R6†V6²æ÷r'Vç2&Vf÷&RWfW'’6öÖÖ—BæB&Vf÷&RWfW'¢ÖW&vRâvVçBW&f÷&×2Â'WBæ÷F†–ær–âF†—27V'G&VR'Vç2öâÖW&vR6öÖÖ—B—G6VÆb(	BF†P¢&W÷6—F÷'’w24’—2÷WG6–FR6†–6vòóFFæB÷WG6–FRF†—2ÆæRw266÷Râ‡VÖâÖW&vRöâv—D‡V ¢6â7F–ÆÂV&Æ—6‚Væ–öâÖ6÷''WFVB6†ævVÆörâF†Ræ'&÷rfW'6–öâöbF†B†¦&B—2æ÷rÆ÷V@¢F†RÖöÖVçBç–öæR'Vç2F†RvFS²F†RvVæW&ÂfW'6–öâ—2&V6÷&FVB–â$ôDÔ*r³"à ¢22f—†VB##bÓ‚Ó2(	BF†R†÷&—¦öâF–Ö&W"v2&V–ærFVÆWFVB'’—G2÷vâFW‡GW&P ¢¢¥3f—FVÒRÂ&÷F‚ÖV6†æ—6×2F†R—FVÒæÖW2â¢¢F†Rf"×F–Ö&W"&æBG&w2F†RF÷76–W"w2&öF–W0¦öbvööG2BF‡&VRÂf÷W"æB6—‚Ö–ÆW226–Æ†÷VWGFRöâ&–ærÂ'&ö¶VâW7&÷vâ'’7&÷vâv—F€§6·’÷VæVBF‡&÷Vv‚F†R7FæB(	B¶'Vç2F÷vâFò&÷WBã"–âvâBf÷W"‡VæG&VBÖWG&W2À§v†W&RF†R&æB—2f÷'G’—†VÇ2FÆÂÂF†B—2FW‡GW&Râöâ6—‚ÖÖ–ÆR&öG’v†÷6RVçF—&R6–Æ†÷VWGFP¦—2öæR÷"Gvò—†VÇ2—B—2¢¦FVÆWF–öâ¢¢ÂæBF†R&æBv26''––ær&÷F‚f–ÇW&W2Böæ6Rà ¢Ò¢¤ÖV7W&VBBF†R7vâ7FF–öâÂv—F‚F†R—†VÂfÆö÷"&VÖ÷fVBæBF†Vâ–âÆ6Râ¢¢#ƒöb“ ¢&V&–æw26''’F–Ö&W"&öG’âv—F†÷WBF†RfÆö÷"F†RÖöGVÆF–öâG&Wr¢£#Söb#ƒ¢¢&W6öÇf&ÆP¢&V&–æw2B—†VÂ÷"Ö÷&RöâF†R†öæRæB¢£#cröb#ƒ¢¢öâF†RFW6·F÷(	Bv÷'7B6–Æ†÷VWGFP¢¢£ã‚‚¢¢æB¢£ã3‚¢¢ÂvVöÖWG'’6öÇfVBæBw&—GFVâ–çFòF†R'VffW"æBFöòF†–âFòÆæ@¢ç—v†W&Râv—F‚—C¢¢£#ƒó#ƒæB#ƒó#ƒ¢¢Âv÷'7B¢£ã‚¢¢âF†R&æBw2G&–ævÆR6÷VçB—0¢¢£Sc"ÂVæ6†ævVB¢¢(	BF†RfÆö÷"Ö÷fW2fW'F–6W2æBæWfW"F†V—"çVÖ&W"à¢Ò¢¥F†RfÆö÷"—2öâF†R$U5TÅBÂæ÷B6öâ¶¢¢Â6ò—B&–æG2öæÇ’v†W&R—†VÇ2&R66&6S¢¢CÒG&VVÆ–æR—2C‚FÆÂæB¶VW2—G2v2FòF†RÆ7BW"6VçBâv†W&R&öG’w2&p¢6–Æ†÷VWGFR—2—G6VÆb7V"×—†VÂF†RÖöGVÆF–öâ—27W&W76VB÷WG&–v‡BÂ&V6W6RFW‡GW&RF†@¢6ææ÷B&RG&vâ6âöæÇ’7V'G&7Bà¢Ò¢¥F†R&æB—2F†W&Vf÷&Ræ÷r6öÇfVBv–ç7BF†RÆ—fRf–Ww÷'Bâ¢¢Ö–âæ§676W0¢—†VÇ5W%&F–æöfbF†R&VæFW&W"6—¦RæBF†R6ÖW&w2÷vâf–VÆB(	BCsR‚÷&Böâ†öæR@¢—G2“L+6Æ×v–ç7Bƒ32‚÷&BöâFW6·F÷BS\+Âf7F÷"öbãsRF†RöÆBf—†VBf–VÆBv÷@¢w&öær–âF†RF—&V7F–öâF†B÷fW"Ö7WG2†öæRâf–Ww÷'B6†ævR&R×6öÇfW2F†R&æBW†7FÇ’0¢vÆ¶–ærFöW2à¢Ò¢¥F†R6öÆ÷W"v2öæRÆ–æRöb&—F†ÖWF–2ç7vW&–ærVW7F–öâF†R&VæFW&W"æWfW"6·2â¢ ¢†¦TF—7Æ”Æ–æV"‚–&âF†R†¦R6öÆ÷W"F‡&÷Vv‚4U2Fò&V6‚F†R&æBw2F—7Æ’fÇVRâF†P¢&æB—2FöæTÖVC¢fÇ6RÂfös¢fÇ6V(	B—G2g&vÖVçB—2÷VR(i"6öÆ÷'76VÂ6òÆ–æV ¢fW'FW‚6öÆ÷W"F—7Æ—22F†R†W‚—BFV6öFW2g&öÒ(	Bv†–ÆRF†RfövvVBw&÷VæB—0¢÷VR(i"FöæVÖ–ær(i"6öÆ÷'76R(i"fövv—F‚föt6öÆ÷&WÆöFVB–âF†RõUEUB6öÆ÷W"76RÀ¢6öçfW&v–æröâF†B6ÖRÆ—FW&Â†W‚âöæRFV6öFRV6‚âF†RFöæR7W'fRv2Æ–VBFòöæRVæ@¢æBFòæ÷F†–ær—B†BFòÖF6ƒ¢¢£b&VBæB"w&VVâ¢¢öfbF†Rw&÷VæB—BF÷V6†W2Âc’–â&ÇVP¢B&—&–U÷vW7Fâ&÷F‚VæG2&W÷'B¢¢3ƒ†63¢¢æ÷râæBF†RöÆBfÇVRv2¢¤Âsv–ç7B¢†÷&—¦öâ6·’öbÂc"¢¢(	B&æB§ÆW"¢F†â—G2÷vâ6·’Âv†–6‚—2v†BF—7FçBG&VVÆ–æP¢æWfW"—3²—B—2ÂS’æ÷rÂF‡&VR&VÆ÷rà¢Ò¢¥F†RvFR—2WfW'’&W6öÇf&ÆR&V&–ærÂæ÷BW&6VçFvRâ¢¢“R&"v÷VÆB†fR76VBF†P¢FW6·F÷†ÆböbF†RFVfV7Bƒ#cró#ƒ—2“RR’âF‡&VRæWr76W'F–öç2B&÷F‚f–Ww÷'G3¢F†R&æ@¢æB66VæRæföræ6öÆ÷&&RöæR6öÆ÷W"Âæò&W6öÇf&ÆR&V&–ær—2G&vâVæFW"F†RfÆö÷"ÂæBF†P¢&æBv26öÇfVBv–ç7BD„•2f–Ww÷'B(	BfÆö÷"ÖV7W&VB–â—†VÇ2—2ÖVæ–ævÆW72v–ç7B¢†&BÖ6öFVBf–VÆBâfW&–f–VBF†W’&—FR'’&VÖ÷f–ærF†RfÆö÷#¢&÷F‚f–Ww÷'G2f–ÂÂv—F‚F†P¢6÷VçG2æBF†Rv÷'7B—†VÂæÖVBà¢Ò¢¥v†BF†—2FöW2äõB6Æ–Òâ¢¢F†Rf–æF–ær&V†–æB—FVÒR—2†÷Föw&†–2(	B£3Röb†÷&—¦öà¢6öÇVÖç26''’ç’F–Ö&W"Â2ãbR7&÷72F†R6VçG&ÂGvò×F†—&G2¢(	BæB—Bv2F¶Vâv—F‚6†÷@¢†&æW72F†B—2æ÷B–âF†R&VÆV6RvFRâ¢¤—B†2æ÷B&VVâ&RÖÖV7W&VB¢¢Â6òæò6öÇVÖâf–wW&P¢—2V÷FVB†W&Râv†B—2ÖV7W&VB—2F†BF†RvVöÖWG'’—Bv2ÖV7W&–ær—2æòÆöævW"&V–æp¢F‡&÷vâv’ÂæBF†BF†R&æB—2F&¶W"F†â—G26·’&F†W"F†âÆW"âFö72ôÄ”$U%D”U2æÖF ¢Ã3R—2&Wf—6VB–â&÷F‚F—&V7F–öç3²F†Rãƒ"†¦R6—BW†—7G2Fò6öæfW72—2VçF÷V6†VBÂæ@¢F†RF—7Fæ6R6ö×&W76–öâ—B'W—2—2Væ6†ævVBà ¢22f—†VB##bÓ‚Ó2(	BF†R7v&BVæFVBöâ7G&–v‡BÆ–æRÂæBF†RÆ–æRv2&—F†ÖWF–0 ¢¢¤&–ær—26—&6ÆR&÷WBF†RvÆ¶W"Â6ò—G2÷WFW"VFvR—26öç7FçB67&VVâ&÷râ¢¢F†P§F‡&VRÖ7&—F–2&—&–R7vVWÖV7W&VB—BæBæÖVBF†R&÷s¢ETäRæÖ–Bç&F—W2Ò#rã&VF–7FVB&÷p£CC‚ã‚æBF†Rg&ÖR6†÷vVBöæRBCSÂ7G&–v‡B7&÷72ÆÂ#ƒ6öÇVÖç2âF†B—2$ôDÔ*r3f¦—FVÒ2ÂæBF†R&V6öâ—B—2&—F†ÖWF–2&F†W"F†â&VæFW&–ær'FVf7B—2F†R6—FS¢Bã3gBö`§&VÆ–Vb7&÷72F†Rv†öÆRcCÒ&÷‚Â6òf—†VBF—7Fæ6R&VÆÇ’FöW2ÆæBöâf—†VB&÷râF†RvFP¦æ÷rÖV7W&W2—BF†Rv’F†Rf–æF–ærv27FFVB(	B&–âF†Rf–Wr'’&V&–ærÂ6²V6‚&–â†÷rf ¦—G2÷vâ7v&B&V6†W2Â6öçfW'BF†RF—7Fæ6RFòF†R&÷r—BÆæG2öââ¢¤öâF†R&–ær2—B7Föö@§F†÷6R&÷w27ææVBãB‚â¢  ¤WfW'’ÆGF–6R6Æ÷Bæ÷r6'&–W2—G2÷vâ÷WFW"&F—W3¢F†RÆ–W"w2æöÖ–æÂöæRÇW2§v÷&ÆBÖæ6†÷&VBöfg6WBöbWFò¢¬+2Ò¢¢BgVÆÂFWF–ÂŒ+ãbÒöâ†öæRÂ&÷WBâV–v‡F‚öbF†P§&–ærBWfW'’FWF–Â6WGF–ær’Âg&öÒ6Öö÷F‚BÒfÇVRÖæö—6RÆö&W2v—F‚W"×6Æ÷BF—F†W"÷fW §F†VÒâÖV7W&VBgFW#¢¢£Rã’‚¢¢öb7&VBB#ƒ9sƒæB¢£rãB‚¢¢B3“9ssƒÂF†R7v&@§&V6†–ær#Rã(	3#‚ãBÒ&÷WBæöÖ–æÂ#bãBà ¢Ò¢¥v–FVæ–ærF†RfFRv÷VÆBæ÷B†fRv÷&¶VBÂæBF†R&V6öâ—2v÷'F‚¶VW–ærâ¢¢F†R&æB—0¢Ç&VG’rÒÂv†–6‚—2‚‚öbg&ÖRBF†BF—7Fæ6RâF†RÆ–æR—2æ÷BF†R&×(	B—B—2v†W&P¢F†R&×&V6†W2¦W&òÂæBv–FW"&×7F–ÆÂ&V6†W2¦W&òWfW'—v†W&RBöæ6Râv†B&VÖ÷fW2¢Æ–æR—2&÷VæF'’F†B—2–âF–ffW&VçBÆ6R–âV6‚F—&V7F–öâà¢Ò¢¤—B—2æV&Ç’g&VRÂ'’6öç7G'V7F–öâ&F†W"F†â'’ÇV6²â¢¢G&–ævÆW2&R–Bf÷"'’F†P¢ÄED”4RÂæ÷B'’F†RfFRÂ6ò6Æ÷BF†Rg&–ævRW6†W2&W–öæB&V6‚—2G&÷VBB&V'V–Æ@¢–ç7FVBöbG&vâB¦W&ò†V–v‡BÂæBF†RÆGF–6Rw&Wr'’F†R×Æ—GVFRFò6''’F†RöæW2—@¢W6†W2–â(	Bv—F‚7–ÖÖWG&–2öfg6WBF†RÖVâ6÷7B—2&F—W<+"²f&–æ6VÂæ÷@¢‡&F—W2²×Æ—GVFRœ+&âÖV7W&VBô"B#ƒ9sƒBF‡&VRf—†VB7FF–öç3¢÷Vâ&—&–P¢¢£sB3c2(i"sbcSb¢¢G&–ævÆW2‚³ã2RÂ2sC"(i"2ƒSfÆ÷&–ç7Fæ6W2’Â6WGFÆVBF÷và¢¢£3ƒ’3c’(i"3ƒ’#S2¢¢Ž(‰#ã2R’Â&—fW"&æ²¢£3S’(i"3SR¢¢Ž(‰#B’âG&r6ÆÇ2Væ6†ævV@¢B3ròcbòs"âF†R6÷7BÆæG2v†W&RF†R7v&B—2FVç6RæBæ÷v†W&RVÇ6RÂv†–6‚—2F†R&–v‡@¢6†Rf÷"—Bà¢Ò¢¥v÷&ÆB÷6—F–öâÂæ÷B6ÖW&F—7Fæ6Râ¢¢F†Röfg6WB—2gVæ7F–öâöbF†Rw&÷VæBÆöæRÂ6òF†P¢&vvVBVFvRFöW2æ÷B7v–Ò2F†RvÆ¶W"Ö÷fW2æB—2F†R6ÖRVFvRv†–6†WfW"v’F†W’f6R(	@¢F†R÷Ö–âFVfV7BöæR&–ærgW'F†W"÷WBÂfö–FVB&F†W"F†âG&FVBf÷"âF†RvFR6·2F†P¢Æ6W"†fÆ÷&æg&–ævTF’–ç7FVBöb&RÖFW&—f–ærF†Ræö—6RÂæB&WV—&W2æ–æRö–çG2Fòç7vW ¢–FVçF–6ÆÇ’g&öÒGvò6ÖW&2CÒ'Bà¢Ò¢¥F†RfÆ÷vW'2†BFò6öÖRv—F‚F†Rw&72â¢¢F†Rf÷&"&–ærVæG2v—F†–âÖWG&RöbF†RÖ–B&–ærÀ¢6òg&–ævRöâF†RÖG&—‚ÆöæRv÷VÆB†fRÆVgBF†R'&–v‡FW7Bö&¦V7G2–âF†Rf–VÆBG&v–ærF†P¢Æ–æRF†Rw&72æòÆöævW"FöW2â—B—2vFVBöâ—G2$”äu2&F†W"F†âöâ—G2G&vâVFvS¢@¢2ãBÒ6VÆÇ22ãs\+&–â†öÆG2öæR÷"Gvòf÷&'2Â6ò'F†RgW'F†W7BöæRG&vâ"—26×Æ–æp¢7FF—7F–2ÂæBÖV7W&VBF†Bv’—B&W÷'FVBæ–æRÖÖWG&R†öÆR–âw&÷VæBF†B†2æöæRà¢Ò¢¥F†R÷Ö–âvFR†BFò&RÖFR–ç7Fæ6RÖv&RFò7F’†öæW7Bâ¢¢—B6¶VBF†RÆ–W"w2æöÖ–æÀ¢&–ær†÷rfFVBâ'&—f–ærÆçBv2ÂæBæöÖ–æÂ&–ærç7vW'2§¦W&ò¢(	Bg&VR72(	Bf÷ ¢W†7FÇ’F†RÆçG2F†Rg&–ævRW6†W2gW'F†W7B÷WBâ—B&VG2V6‚–ç7Fæ6Rw2÷vâ6†•&–æv ¢æ÷râ6ÖR&÷VæBÂ6ÖRÖV7W&VBãR'&—fÂ†V–v‡Bà¢Ò¢¥fW&–f–VBF†RvFR&—FW2¢¢Â'’WGF–ærF†Rg&–ævR&6²Fò¦W&ó¢F†R&÷VæF'’7&VBfÆÇ2Fð¢¢£ãB‚¢¢v–ç7B&"öbBÂF†Rf÷&"&–æw27âãÒÂæBF†Rv÷&ÆBÖæ6†÷&–ær6†V6°¢&W÷'G2æòf&–F–öâBÆÂâF‡&VRf–ÇW&W2ÂöâF†R6öFRF†B6†—VB–W7FW&F’à¢Ò¢¥v†BF†—2FöW2æ÷BFòâ¢¢—BFöW2æ÷BW‡FVæBF†R7v&BâÃƒ7F–ÆÂ÷vç2F†R6ö×&W76–öâ(	BF†P¢FW'&–âw2÷vâ6öÆ÷W"6'&–W2WfW'—F†–ær7BF†R&–ær(	BæBF†RÖ–BÖf–VÆBF&vWG2–â3f—FV×0¢Â"æBN(	3r&RVçF÷V6†VBâF†—2&VÖ÷fW2Æ–æRF†RW–R&VG22âö&¦V7B–âF†Rv÷&ÆC²—@¢FöW2æ÷BWBfVvWFF–öâv†W&RF†W&R—2æöæRà ¢22f—†VB##bÓ‚Ó2(	BfFRgVæ7F–öâF†Bv2&öGV6–ær7FW  ¢¢¥F†RG&ç6—F–öâF†R÷væW"6¶VBf÷"†B&VVâF†W&RÆÂÆöærÂ6×ÆVBöæ6RW"7G&–FRâ¢ ¢$w&72æBfÆ÷vW'2V"÷WBöbF†Rw&÷VæB2–÷RvÆ²F÷v&G2F†VÒ"„³2’&VBÆ–¶RÖ—76–æp¦fVGW&RÂæBfÆ÷&æ§6†266ÆVBWfW'’ÆçBF÷vâ÷fW"F†R÷WFW"&æBöb—G2&–ær6–æ6RF†P¦Æ–W"v2w&—GFVââF†RFVfV7B—2F†R$DRÂæ÷BF†R'6Væ6S¢F†R&×v2WfÇVFVBöâF†R5R@¦ÆGF–6R×&V'V–ÆBF–ÖRæB&¶VB–çFòF†R–ç7Fæ6Rw2†V–v‡BÂæBF†RÆGF–6R&V'V–ÆG2öæÇ’WfW'¦ETäRç7FWææV&ÖWG&W2vÆ¶VBâã"Òöb7FWv–ç7BF†RæV"&–ærw2"ã"Ò&æBÖVç2Æç@§vVçBg&öÒæ÷F†–ærFò¢£SRRöbgVÆÂ†V–v‡B–â6–ævÆRg&ÖR¢¢Âöæ6RW"7G&–FRÂf÷&WfW"âfFP§F†BöæÇ’WFFW2v†VâF†RF†–ær—B—2fF–ær—2&V'V–ÇB—27FWgVæ7F–öâvV&–ær&×w2æÖRÀ¦æB—B—2–çf—6–&ÆR–â&Wf–Wr&V6—6VÇ’&V6W6RF†R&×&VG26÷'&V7FÇ’öâF†RvRà ¥F†R&×æ÷r'Vç2W"g&ÖR–âF†RfW'FW‚6†FW"v–ç7B6ÖW&÷6—F–öæâv†BF†B6÷7BÂæ@§v†B—B&÷Vv‡BÂ—2–â$ôDÔ*r³3²F‡&VRF†–æw2&VÆöær†W&Rà ¢Ò¢¤fÆ÷vW"†VB6ææ÷B§W7B6‡&–æ²(	B—B†2Fò6öÖRF÷vââ¢¢—G2÷&–v–â—2'Gv’W7FVÒÂ6ð¢66Æ–ær–âÆ6RÆVfW2—B–âF†R—"÷fW"ÆçBF†B—2æòÆöævW"VæFW"—Bâ6†•&—6VæB¢v÷&ÆB×76RFW66VçBÆ–VBgFW"F†R–ç7Fæ6RG&ç6f÷&Ò‡F†R–ç7Fæ6RÖG&—‚6'&–W2&VÀ¢&÷FF–öâf÷"F–ÇFVB†VG2Â6ò—B6ææ÷B&RföÆFVB–çFòF†RÆö6Âöfg6WB’à¢Ò¢¥F†RfFRÂã3V†VBvFRv2—G6VÆbF†Rv÷'7B÷–âF†Rf–VÆB¢¢Â&V–ær7FW–âF†P¢Ö–FFÆRöb&×öâF†R'&–v‡FW7Bö&¦V7B–âF†Rg&ÖRâ†VG2†fRF†V—"÷vâ–ç6WB&–æræ÷rÂæ@¢F†R6ÖR†VG2&RG&vã¢F†R&–ær&V6†W2¦W&òW†7FÇ’v†W&RF†RÆçBw2&×76W2ã3Rà¢Ò¢¥F†RwV&çFVR—2vVöÖWG&–2Âæ÷BV×—&–6Ââ¢¢F†RÆGF–6R—2–ç6WBg&öÒF†RfFR&–ær'’F†P¢&V'V–ÆB7FWÂ6òÆçB—2Çv—2Æ6VBÂB¦W&ò†V–v‡BÂ&Vf÷&R—B—2æV"Væ÷Vv‚Fò&Rv÷'F€¢ç’âF†R&W6–GVÂ—2öæRg&ÖRöb÷fW'6†ö÷B(	BF†R&V'V–ÆBf—&W2öâF†Rg&ÖRF†B6'&–W2F†P¢vÆ¶W"7BF†R7FW(	Bv†–6‚—2ã#BÒBcg2Â&÷WBRöbÆçBw2†V–v‡BÂæB—B—0¢w&—GFVâF÷vâ&F†W"F†â&÷VæFVBv’âF†RæV"&–ærw2f—6–&ÆR&F—W2—2ãbÒ6†÷'FW"F†â—@¢v2Âv†–6‚—2F†R&–6RöbF†R–ç6WBæB—2ÆVgB26÷fW&vRVW7F–öâ–â³2à¢Ò¢¥F†RvFRæ÷rvÆ·2â¢¢GvVçG’ãRÒ6W2B3“9ssƒæB#ƒ9sƒÂ6†V6¶–ærWfW'’ÆçBF†@¢V'2–âg&öçBöbF†RvÆ¶W#¢ÖV7W&VBv÷'7B'&—fÂ¢£ãR¢¢öbgVÆÂ†V–v‡Bv–ç7BP¢&"ÂÇW26†V6²öâF†R&–ærvVöÖWG'’6òF†RÖ&v–â6ææ÷B&RGVæVBv’ÆFW"âG&–ævÆW0¢ScBƒ#FW6·F÷v–ç7BScBcƒ&Vf÷&R(	B&÷VæF–ærW'&÷"ÂæBæòæWr76WBà ¢¢¤æBF†RvFRv2ÖV7W&–ærF†RvVF†W"â¢¢'Vææ–ærF†R&6VÆ–æR&Vf÷&RF÷V6†–ærç—F†–ærGW&æV@§WâVç&VÆFVB&VC¢¢'GW&æ–ær—Böfb&W7F÷&W2F†R&VæFW""¢f–ÆVB&÷WB¢§Gvò'Vç2–âF‡&VRöà¦Ö–â¢¢ÂB3“9ssƒÂv—F‚v÷'7BÖ6VÆÂFVÇFöb’v–ç7B&"öb‚âF†R76W'F–öâ6ö×&W2Gvð¦6GW&W2öbF†R6ÖR66VæRFòFV6–FRv†WF†W"7v—F6†–ærF†R6öæf–FVæ6Rf–WröfbÆVfW2ç—F†–æp¦&V†–æB(	BæBF†Rv–æB&Æ÷w2&WGvVVâF†VÒÂB(	32g2VæFW"F†R6ögGv&R&7FW&—6W"Â6òÖ÷7Bö`§F†R&W6–GVÂ—Bv2ÖV7W&–ærv27v––ærw&72âF†RFöÆW&æ6R†BÇ&VG’&VVâv–FVæVBöæ6Rf÷ ¦W†7FÇ’F†B&V6öâÂv†–6‚—2F†RFVÆÃ¢vFRv†÷6R&"—26WB'’—G2÷vâæö—6R—2vFRF†@§v–ÆÂ&Rv–FVæVBv–ââÖ–âæ§6v–ç2†&æW72ÖöæÇ’6WDæ–ÖF–öä†öÆF(	B¶VWG&v–ærÂGfæ6P¦æ÷F†–ær(	BæBF†RF‡&VR6GW&W2&RF¶VâVæFW"—BâF†R&W6–GVÂ—2&VF&6²æö—6Ræ÷rÂ6òF†P¦&"¢§F–v‡FVæVB¢¢g&öÒÖVâãRòv÷'7B‚FòÖVâãòv÷'7B2ÂæBF†R76W'F–öâ&÷fR—@¢‚¦6öæf–FVæ6Rf–Wr6†ævW2F†R&VæFW"¢’v÷B7G&–7FÇ’†&FW"Â&V6W6R7v’6âæòÆöævW"7WÇ’ç¦öbF†RF–ffW&Væ6R—B†2Fòf–æBâGvò6öç6V7WF—fRgVÆÂ'Vç2w&VVâB&÷F‚f–Ww÷'G2à ¥F†B6Æ÷6W2F†RFV'BF†R&¶RÖvFRVçG'’&VÆ÷r&V6÷&G22÷vVC¢F†RfÆ÷&6Æö6²—2g&÷¦VâGW&–æp¦6GW&RÂæBF†R&÷VæBv2F–v‡FVæVB&F†W"F†âv–FVæVBà ¢22f—†VB##bÓ‚Ó2(	BF†Ræ–v‡FÇ’&¶R†B&VVâ&VBf÷"F—2ÂæBæö&öG’6÷VÆB6VR—@ ¢¢¥F†RÆ6V†öÆFW"vFRf÷&&FRF†RWw&FRF†R&¶RW†—7G2FòW&f÷&Òâ¢¢vVæW&F÷'2ö'V–ÆBç– §w&—FW276WG2övÇFbóÆ–CåõóÇ†6SâævÆ&f÷"ç’&V6÷&Bv†÷6R&6†WG—R†2vVæW&F÷"ÂæBWfW'¦&V6öåò¦&V6÷&B†2öæR(	B6òF†R6æöæ–6Â&ÆVæFW"&¶RÆæG2öâW†7FÇ’F†Rf–ÆVæÖP¦vVæW&F÷'2ö–æfW'&VE÷Æ6V†öÆFW"ç–6Æ–×2ÂæBF†RvFRF†Vâ&V¦V7FVBF†R&VÂ&¶Rf÷"æ÷@¦&V–ærF†RW&RÕ—F†öâÆ6V†öÆFW"—Bv2'V–ÇBFò&WÆ6Râ6V6öæB6öæfÆ–7B&öFRÆöæs ¦FööÇ2ö&¶Rç6†'Vç2vÇFb×G&ç6f÷&Ò÷fW"76WG2÷vV"öÂ6òFVÖæF–ær'—FRÖWVÆ—G’v—F‚F†P¦Ö7FW"76W'FVBF†B6ö×&W76–öâæWfW"†Vç2â¢¥v†BÖFR—B–çf—6–&ÆR—2F†R6†Rv÷'F€§&VÖVÖ&W&–ær¢¢(	BF†RvFR76VBöâWfW'’FWfVÆ÷W"Ö6†–æRæBf–ÆVBöâWfW'’4’'VææW"Â&V6W6P§F†RF–ffW&Væ6Rv2v†WF†W"ç†6÷VÆB&V6‚F†RæWGv÷&²âw&VVâÆö6ÂvFRv2&W÷'F–æröâ§—VÆ–æR—Bv2æ÷B'Vææ–ærâF†RvFRæ÷r6ö×&W2öæÇ’F†RÖ7FW"v–ç7BF†R&V6÷&BÂ&WV—&W0§F†RFW&—fF—fRÖW&VÇ’FòW†—7BÂæB7FæG26–FRf÷"ç’76WBv†÷6RÖæ–fW7BVçG'’6—0¦¶–æC¢vVæW&FVFÂÆVf–ærF†BFòF†R÷&F–æ'’7FÆVæW726†V6²à ¢¢¦FööÇ2÷V&Æ—6‚ç6†v2â67V×VÆF÷"Âæ÷BÖ—'&÷"â¢¢—B6÷–VBf–ÆW2–âæBæWfW"Föö²ç¦÷WBÂ6ò&WF—&VB76WB6†—VBf÷&WfW#¢‚õ÷&V6öÖÖVæFVEóƒ3RævÆ&Æ6V†öÆFW'2Â÷'†æVBv†Và§F†R&öw&ÖÖRv2&VæÖVBÂvW&R7F–ÆÂ&V–ær6W'fVBFòf—6—F÷'2ÆöærgFW"æ÷F†–ær&VfW&Væ6V@§F†VÒâFVÆWF–ærf–ÆRg&öÒF†R6÷W&6RG&VRv2æ÷BF†–ærF†RV&Æ—6†VB6—FR6÷VÆBW‡&W72à¤f—†VB'’6ÆV&–ærF†RV&Æ—6†VBFFövÇFf&Vf÷&R6÷––æs²–ÆöB’ãb(i"‚ãSRÔ"BF†RF–ÖRà ¢¢¤¶æ÷vâfÆ·’vFRÂFVÆ–&W&FVÇ’æ÷B6–ÆVæ6VBâ¢¢Öö&–ÆR3“ƒsƒ¢GW&æ–ær—Böfb&W7F÷&W2F†P§&VæFW&6ö×&W2g&ÖR6GW&VB&Vf÷&RF†R6öæf–FVæ6RFövvÆRv—F‚öæR6GW&VBgFW"Âv†–ÆRF†P¦fÆ÷&—27F–ÆÂ7v––ærâö'6W'fVBf–Æ–ærGv–6RBv÷'7BÖ6VÆÂFVÇFv–ç7B&÷VæBöb‚æ@§76–æröâF†RF†—&B'Vâv—F‚æò6öFR6†ævRâF†R&÷VæB†2äõB&VVâv–FVæVB(	B&VÆV6RvFP¦Æö÷6VæVBVçF–Â—B7F÷26ö×Æ–æ–ær—2æ÷BvFRâF†Rf—‚—2Fòg&VW¦RF†RfÆ÷&6Æö6²GW&–æp¦6GW&RÂæB—B—2÷vVBâ¢¥–B##bÓ‚Ó2¢¢(	B6VRF†RfÆ÷&ÖfFRVçG'’&÷fS¢6GW&W2æ÷r'Và§VæFW"6WDæ–ÖF–öä†öÆFæBF†R&÷VæBF–v‡FVæVBFòv÷'7B6VÆÂöb2à ¢22f—†VB##bÓ‚Ó2(	BGvòFVfV7G2F†R÷væW"†÷Föw&†VBÂæBv†BF†W’FVv‡@ ¢¢¥F†R6Æ&²7G&VWB†VFÆæBv2F†RÖw2÷vâÆWGFW&–ærâ¢¢f—†VB##bÓ‚Ó2âv†BÖ¶W2—@§v÷'F‚&V6÷&F–ær—2F†BF†RG&6R†B&VVâ¦&VÆ–WfVB¢v–ç7BÖV7W&VÖVçBF†BF—6w&VV@§v—F‚—C¢F†R6÷WF‚vFW"vV÷&VfW&Væ6Ræ÷FR&V6÷&FVBs’ãbÒöb&W6–GVÂB6Æ&²v–ç7@£‚ãrÒBFV&&÷&âæBGG&–'WFVBF†R7v–ærFòW"7G&WF6‚â&÷F‚çVÖ&W'2vW&R&–v‡BæBF†P¦W‡ÆæF–öâv2w&öærâcÒÆö6ÂF—6w&VVÖVçB&WGvVVâGvò–æFWVæFVçBÖWF†öG2—2FVfV7@§&W÷'BÂæ÷BâW'&÷"&"à ¢¢¦vVæW&F÷'2÷FW'&–åövVâç’ÒÖvÆ&†B&VVâVç'Vææ&ÆR6–æ6RFW'&–åö–çWG6v0¦W‡G&7FVBâ¢¢FW'&–åö–çWG5÷6†‚–—26ÆÆVB&Vf÷&RÖ–â‚––ç6W'FVBvVæW&F÷'2ööà¦7—2çF†²'Vâ2—F†öã2vVæW&F÷'2÷FW'&–åövVâç–F†BF‚—27—2çF…³Ö'’66–FVçBÀ§'VâVæFW"&ÆVæFW"Ò×—F†öæ—B—2æ÷BÂæBF†RtÄ"†ÆbF–VBöâÖöGVÆTæ÷Df÷VæDW'&÷&âF†P¦–ç6W'BÖ÷fVBFò–×÷'BF–ÖRâæ÷F†–ær6Vv‡B—B&V6W6RFööÇ2ö&¶Rç6†FöW2æ÷B'V–ÆBFW'&–à¦æBF†RFW'&–âtÄ"—2&&RÂFVÆ–&W&FR–çfö6F–öââ¢¥F†R†V–v‡Ff–VÆBæBF†RtÄ"&Ræ÷p¦&6²–â7FW¢£²F†R6öÖÖ—GFVBtÄ"&Vf÷&RF†—2'Vâv2&¶VBBÒÖFV6–ÖFRÖFVrãFæBF†P¦öæRgFW"Bã6‡6VR³B’à ¢¢¥F†RG&VR×Æ6VÖVçBvFRæBF†R&—fW"Ö6²&RGvòF–ffW&VçBVW7F–öç2â¢¢—5vFW&6·0¢&—2F†—2F†R&—fW""æB—G2F‡&W6†öÆB—2ÖÒVæFW"F†RFGVÒÂv†–6‚—26÷'&V7Bf÷"F†@§VW7F–öâæBv26–ÆVçFÇ’w&öærf÷"&Ö’7FVÒ7FæB†W&R"âF†R&VÆV6RvFR†Bw&VVà¦6†V6²öâF†Rf—'7BVW7F–öâv†–ÆRF†R÷væW"†B†÷Föw&‚öbF†R6V6öæBf–Æ–ærâ&÷F€¦6†V6·2&Ræ÷r&W6VçBà ¢22æWr##bÓ‚Ó2(	BF†RÆGFVBw&–BW†—7G2ÂæB—Bf÷VæB6WfVâ'V–ÆF–æw2–âF†R&ö@ ¢¢¤³r†6RöæRâ¢¢F†R&Æö6²æBÆ÷Bw&–B—2vVæW&FVB&F†W"F†âG&6VC ¦FööÇ2övVæW&FU÷ÆEöÆ÷G2ç–öfg6WG2F†—2&ö¦V7Bw26öÖÖ—GFVB7G&VWB6VçG&VÆ–æW2'’†ÆbF†P§ÆGFVB6÷'&–F÷"Â–çFW'6V7G2F†VÒÂæBF—f–FW2F†R&W7VÇB–çFòÆ÷G2(	B’&Æö6·2ÂS"Æ÷G2À§&RÖFW&—fVB'—FRf÷"'—FR'’FööÇ2ö6†V6²ç6†âG&6–ærF†Rƒ3B6†VWG2–ç7FVBv÷VÆB†fR&¶V@§F†V—"2ã~(	3BãRRW"7G&WF6‚–çFòWfW'’&Æö6²f6RâF†R&Æö6·2&R–æfW'&VF&V6W6RF†V— ¦–çWG2&S²F†RÆ÷BÆ–æW2æBF†RÆÆW’÷6—F–öâ&R6öæ¦V7GW&ÆæB7F’F†Bv’Â&V6W6P¦f÷W"Æ÷G2Fòf6R—2&VF–æröbôäR&Æö6²†&Æö6²‚öâF†R÷væW"w26Æ&²×&V6‚7&÷’âæòÆ÷@¦æBæò&Æö6²—2çVÖ&W&VB(	BF†—2&ö¦V7B†2æWfW"&VBF†ö×6öâw2çVÖ&W&–æröfb6†VWBà ¢¢¥F†Rw&–B–ÖÖVF–FVÇ’–Bf÷"—G6VÆb26†V6²â¢¢öb##"Æ6VB7G'V7GW&W2Âƒ7FæB–ç6–FR¦vVæW&FVB&Æö6²Â#7FæB÷WG6–FRF†R’&Æö6·2—B6÷fW'2ÂæB#"7FæB–ç6–FRÆGFVB7G&VW@¦6÷'&–F÷"âÖ÷7BöbF†÷6R#"&Rv—F†–âÖWG&R÷"Gvòöb6÷'&–F÷"VFvRÂv†–6‚6—2æ÷F†–æp¦v–ç7B+#ÒvV÷&VfW&Væ6R(	B'WB¢§6WfVâ6—BbãRFò"ãÒ–âÂv†–6‚—2F†RÖ–FFÆRöbF†P§&öB¢¢ÂæBWfW'’öæRöbF†VÒ—26öæ¦V7GW&ÆÆ6VÖVçBg&öÒF†R–æfW'&VB×7G'V7GW&P§&öw&ÖÖRâF†RÆ6VÖVçBvFRF†BWBF†VÒF†W&RFW7G2f÷"÷fW&Æv—F‚÷F†W"'V–ÆF–æw2Âf÷ §vFW"ÂæBf÷"ÖöFVÆÆVBw&÷VæC²—B†2æWfW"FW7FVBf÷"F†R7G&VWBâæ÷F†–ærFö7VÖVçFVB—2–âF†P§&öBà ¢¢¤æ÷F†–ærv2Ö÷fVB–âF†—26Æ–6RÂöâW'÷6Râ¢¢&W÷6—F–öæ–ærvVæW&FVB7G'V7GW&W2&RÖFW&—fW0§F†R†÷W6V†öÆBÆVFvW"Â6ò—B&VÆöæw2FòF†R&6VÂF†B÷vç2F†÷6Rf–ÆW2…$ôDÔ³†6RF‡&VR§&F†W"F†âFòF†R6Æ–6RF†BF—66÷fW&VBF†R&ö&ÆVÒâF†Rf–æF–ær—2&V6÷&FVBv—F‚F†R6WfVà§&V6÷&G2æÖVBÂ–âFö72õ$U4T$4‚÷F†ö×6öå÷ÆEöw&–BæÖF*rræB$ôDÔ³rà ¢¢¥v†BF†Rw&–B—2†öæW7B&÷WBæ÷B&V–ær¢£¢’&Æö6·2öbF†RÆBw2S‚Âæòæ÷'F‚F—f—6–öâ†—G0§7G&VWB6öçG&öÂ—2v†B*r3’&V6÷&G22÷vVB’ÂæòÆ÷BFWF‚g&öÒç’6÷W&6R(	BF†RFWF‡2&P§&W6–GVÇ2öbF†R&Æö6²(	BæBæ÷F†–ær&VæFW&VBâ&Æµ÷6÷WF…÷vFW%öÖ&¶WFÂöæRöbF†RÖ÷7B'V–ÇB×W ¦&Æö6·2–âF†RF÷vâÂ—2&VgW6VB÷WG&–v‡B&V6W6RF†R7G&VWBÆ–W"FöW2æ÷B6''’6÷WF‚vFW"vW7@¦öbR³âF†B&VgW6Â—2F†R7G&VWB6öçG&öÂ÷vVBÂ'&—f–ærg&öÒF–ffW&VçBF—&V7F–öâà ¢22æWr##bÓ‚Ó2(	BGvVçG’×F‡&VR'V–ÆF–æw2÷WBöbF†R&öBÂæBF†Rö–çBFW7BF†B6÷VÆBæ÷B6VRF†VÐ ¢¢¤³†6RF‡&VR†’ò³r†6RGvò†’â¢¢F†Rw&–Bf÷VæB6WfVâ7G'V7GW&W27FæF–ærbã^(	3"ãÐ¦–ç6–FRÆGFVB7G&VWB6÷'&–F÷"æBÆVgBF†VÒF†W&RöâW'÷6RÂ&V6W6RÖ÷f–ærvVæW&FV@¦'V–ÆF–ær&RÖFW&—fW2F†R†÷W6V†öÆBÆVFvW"âF†—26Æ–6RÖ÷fW2F†VÒæB6‡WG2F†R†öÆRF†W’6ÖP§F‡&÷Vvƒ¢FööÇ2÷ÆEö6÷'&–F÷'2ç–†öÆG2F†R6÷'&–F÷"vVöÖWG'’f÷"$õD‚F†R&W÷'BF†Bf÷VæBF†P§&ö&ÆVÒæBF†RÆ6VÖVçBvFRF†B†2Fò6F—6g’—BÂ6òF†RGvò6ææ÷Bç7vW"F–ffW&VçFÇ’(	BF†P§6ÖR&wVÖVçBvVæW&F÷'2öÖW6…ö–çWG2ç–6WGFÆW2f÷"F†R7FÆVæW72†6‚âF†RvFR&VgW6W2ç¦vVæW&FVBfö÷G&–çBF†B&V6†W2–ç6–FR6÷'&–F÷"â¢£#2öbF†R3‚&V6—R6VçG&W2Ö÷fVB¢¢†ÖVF–à£"ãÒÂv÷'7B#ã’Ò“²–âÖ6÷'&–F÷"6VçG&W27&÷72F†R66VæRfVÆÂ¢£#"(i"¢¢ÂæBæöæRöbF†RFVà¦—2vVæW&FVBÆ6VÖVçBà ¢¢¥F†R6WfVâvW&RF†RÆ÷VBVæBöbGvVçG’×F‡&VRÂæBF†Rö–çBFW7B—2v‡’æö&öG’¶æWrâ¢¢6VçG&P¦—2öæRö–çBæB'V–ÆF–ær—2&V7FævÆRWFòÒ7&÷72Â6ò'V–ÆF–ær6âg&öçB7G&VW@§v—F‚—G26VçG&R6ÆV"öbF†R6÷'&–F÷"æB†Æb—G2FWF‚–ç6–FR—BâF†B—2W†7FÇ’v†BF†P§&V6—R†B'V–ÇC¢—B&VBF†RƒgBg&öçFvR&æG226VçG&RÖÆ–æW2Fò6—Bôâ&F†W"F†â2VFvW0§Fò6—B$T„”äBÂæBF†Rv†öÆRÆ¶R7G&VWB6†÷&÷r7FööBv—F‚—G2g&öçB†Æb–âF†R7G&VWBæB—G0¦6VçG&Rv—F†–âÖWG&RöbF†R¶W&"Æ–æRâ6÷VçF–ærfö÷G&–çG2–ç7FVBöb6VçG&W2f–æG2¢£Sb¢ §7G'V7GW&W2v—F‚6öÖR'B–â6÷'&–F÷"&Vf÷&RF†—26Æ–6RæB¢£32¢¢gFW"—Bà ¢¢¥F‡&VRöbF†RÖ÷fW26÷VÆBæ÷B6–×Ç’7FW&6²â¢¢‡—6–6–ç5ööff–6V6æVB–çFòF†Rf—'7@¥&W6'—FW&–â6‡W&6‚Â–æe÷6¶W%öGvVÆÆ–æv–çFò&W6W'fVB†6RÓ"6Æ÷BÂ–æeö6ö÷W&vU÷6÷WF† ¦–çFòF†R6÷WF‚'&æ6‚(	B6òV6‚vVçBFòF†RæV&W7B÷6—F–öâ6ÆV&–ærF†R6÷'&–F÷"ÂWfW'¦6öÖÖ—GFVBfö÷G&–çB'’2ÒÂF†RGvòVæ–ç7FçF–FVB†6RÓ"&V6—W2æBF†R†V–v‡Ff–VÆBw2G'¦6÷fW&VBw&÷VæBâF†R‡—6–6–âw2öff–6R—2rãrÒg&öÒv†W&R—Bv2&V6W6RF†RæV&W7Bg&VP¦w&÷VæBFò—G2Æ¶R7G&VWBg&öçFvR—2Æ÷B&6²g&öÒ—Bâ¢¤æ÷F†–ærv2&Vw&FVBâ¢¢F†W6P§÷6—F–öç2vW&R6öæ¦V7GW&Æ&Vf÷&RæB&R6öæ¦V7GW&ÆgFW#²6ÆV&–ærF†R&öGv’—2æ÷@§7FæF–æröâ&V6÷fW&VBÆ÷BÂæBF†R&V6—R6—26òv†W&R—BW6VBFò6’F†R6VçG&W2vW&R&æ@¦76–væÖVçG2ÆöæRà ¢¢¥v†B—2ÆVgB–âF†R&öB—2Ö÷7FÇ’æ÷BFVfV7BÂæBöæR'Böb—B—2ÖV7W&VÖVçBâ¢¢f÷W ¦æöç–Ö÷W2&öög2g&öÒF†R–æf–ÆÂvVæW&F÷'2–æ†W&—BF†—2vFRv†VâF†B&6VÂæW‡B'Vç2âF†P¦÷F†W"#’&R†æB×Æ6VB&V6÷&G2v—F‚g&öçFvR&wVÖVçB&V†–æBF†VÒÂæB¢§F†—'FVVâ&Röà¥6÷WF‚vFW"7G&VWB¢¢(	Bv†W&RÂvÆ¶–æræ÷'F‚g&öÒF†R6öÖÖ—GFVB6VçG&VÆ–æRÂF†RG&6VBƒ3@§vFW&Æ–æR—2¢£ãsRÒv’BR³ƒv–ç7B"ã’Ò†ÆbÖ6÷'&–F÷"¢¢âF†RÆGFVBƒgB7G&VW@§F†W&R'Vç2ãBÒ–çFòF†R&—fW"ÂæBF†R7&R—2VæFW"2ÒBf÷W"Ö÷&RöbVÆWfVâ7FF–öç2âöà§F†B&V6‚'V–ÆF–æröâF†Ræ÷'F‚6–FRöb6÷WF‚vFW"6ææ÷B&R&÷F‚÷WG6–FRF†RÆVvÂ6÷'&–F÷ ¦æBöâG'’ÆæB(	B6òF†RF—6w&VVÖVçB—2&WGvVVâF†RÆBÖöGVÆRæBF†RG&vâ&æ²ÂæB—BvçG0¦&VF–æröbF†RG&fVÆÆVBv’&F†W"F†âF†—'FVVâçVFvVB&V6÷&G2à ¢22æWr##bÓ‚Ó2(	BF†RÆ7Bf÷W"÷WBöbF†R&öBÂæBF†R&÷rF†Bv2–ÖVBBF†R7G&VWG0 ¢¢¤³r†6RGvò†"’â¢¢F†Rf÷W"æöç–Ö÷W2&öög2F†R&Wf–÷W26Æ–6RFVÆ–&W&FVÇ’ÆVgB–âÆGFV@¦6÷'&–F÷"&R÷WBöb—BÂæB&÷F‚–æf–ÆÂvVæW&F÷'2æ÷r6²F†R6÷'&–F÷"VW7F–öâF‡&÷Vv‚F†R6ÖP¦FööÇ2÷ÆEö6÷'&–F÷'2ç–F†R†÷W6V†öÆBvVæW&F÷"æBF†Rw&–B&W÷'B&VBâ¢¤æòvVæW&FV@§Æ6VÖVçBç—v†W&R–âF†—2FF6WB7FæG2–âÆGFVB7G&VWB6÷'&–F÷"â¢¢fö÷G&–çG2v—F‚6öÖP§'B–ç6–FRöæS¢¢£32(i"#’¢£²F†R#’&R†æB×Æ6VB&V6÷&G2v—F‚g&öçFvR&wVÖVçBæB&Ræ÷@§F†—26Æ–6Rw2FòÖ÷fRâfW&–f–VBF†RvFR&—FW2'’WGF–æröæR&V6÷&B&6²v†W&R—Bv3¢—Bf–Ç0§v—F‚F†R&V6÷&BæÖVBæBF†RFWF‚ÖV7W&VBà ¢¢¥F†Rf÷W"vW&RöæR&÷rw276–ærâ¢¢F†R&6VÂw2V–v‡Bæ6–ÆÆ'’'V–ÆF–æw2†BÆö6ÂRfÇVW2ö`£3BÂC3‚ÂScÂcƒrÂƒæB3RÂSS’Âƒ’(	B¢£#2Ò—F6‚Âv†–6‚—2F†R&Æö6²—F6‚¢¢(	B6òöæP§–&B'V–ÆF–ær7FööBBF†RV7FW&âVFvRöbWfW'’&Æö6²Â'V–ÆF–ærw2v–GF‚g&öÒF†RæW‡B7G&VWBÀ¦V–v‡BF–ÖW2÷fW"âF†RvVæW&F÷"F†Bw&÷FRF†VÒFW7FVBæ÷F†–æs¢æ÷B÷fW&ÆÂæ÷BvFW"Âæ÷@¦w&÷VæBÂæ÷BF†R7G&VWBà ¢¢¤†ÆböbF†VÒ76VBÂæBv‡’F†W’76VB—2F†R'Bv÷'F‚¶VW–ærâ¢¢F†Rf÷W"F†B–çG'VFV@¢Ž(‰#ã2Fò(‰#Bã3"Ò–ç6–FRF†R&öGv’’&RF†Rf÷W"Æ&vW7Bæ6–ÆÆ'’fö÷G&–çG2–âF†R&6VÃ²F†P¦f÷W"F†B6ÆV&VB—B&RF‡&VR&—f–W2æB6ÖÆÂ6†VBÂ6ÆV"'’¢£ãN(	3"ãÒv–ç7BF†—0¦FF6WBw2÷vâ+#ÒvV÷&VfW&Væ6R¢¢âF†W’vW&Ræ÷BÆ6VB6ÆV"öbF†R7G&VWBÂF†W’vW&RFöò6ÖÆÀ§Fò&V6‚—B(	B6òf—‚–ÖVBöæÇ’BF†Rf÷W"f–ÇW&W2v÷VÆB†fR6÷'&V7FVBf÷W"çVÖ&W'2æBÆVg@§F†R'VÆRF†B&öGV6VBF†VÒâÆÂV–v‡BÖ÷fVB–ç7FVBÂ'’öæR&wVÖVçC¢V6‚æ÷r7FæG2F—&V7FÇ¦&V†–æBF†RV7FW&æÖ÷7B&–æ6—Â&ööböb—G2÷vâ&Æö6²Â#BÒ&6²f÷"F†R&V"–&G2æB#Òf÷ §F†R6W'f–6R–&G2Â&V6W6R&V"–&B&VÆöæw2FòÆ÷BæBÆ÷B&VÆöæw2Fò†÷W6Râ~(	33"Òö`¦Ö÷fVÖVçBà ¢¢¤æ÷F†–ærv2&Vw&FVBæBæ÷F†–ærv2F÷FVBâ¢¢F†W6R÷6—F–öç2vW&R6öæ¦V7GW&Æ&Vf÷&Ræ@¦&R6öæ¦V7GW&ÆgFW#²6ÆV&–ærF†R&öGv’—2æ÷B7FæF–æröâ&V6÷fW&VBÆ÷BÂæB7FæF–æp¦&V†–æBâæöç–Ö÷W2&ööb—2æ÷BWf–FVæ6Röb6W'f–ær—BâF†R†÷W6V†öÆBÆVFvW"¶W—2öâ7G'V7GW&R–@§&F†W"F†âöâ÷6—F–öâÂ6òF†Rƒ2F÷FVB&öög2¶WBF†V—"†÷W6V†öÆG27&÷72F†RÖ÷fR(	Bv†–6‚—0§v†BÖFRF†R6÷WÆ–ærF†R&Wf–÷W26Æ–6R6—FVB&RÖFW&—fF–öâ&F†W"F†â&RÖ&wVÖVçBâF†P¤æ÷'F‚&6VÂ6'&–W2F†R6ÖRvFRæB—B&–æG2æ÷F†–ærFöF“¢F†Rw&–B6÷fW'2æòæ÷'F‚F—f—6–öà¦&Æö6²Â&V6W6RF†B7G&VWB6öçG&öÂ—2v†B*r3’7F–ÆÂ&V6÷&G22÷vVBâFWF–Ã ¦Fö72õ$U4T$4‚÷F†ö×6öå÷ÆEöw&–BæÖF*rv"à ¢22æWr##bÓ‚Ó2(	BöæRv’Fòvò6öÖWv†W&RÂw&FVC²æBF†R†ÆböbF†RvFRF†Bv2æ÷B'Vææ–æp ¢¢¤³’â¢¢f–Wwö–çG2æBF†RÆ6R6V&6‚vW&RGvòÆ—7G2öbF†R6ÖRw&÷VæB–ç6–FR6WGF–æw2à¥F†W’&Ræ÷röæRvòFöF"Â6V6öæB–âF†R7G&—gFW"6öçG&öÇ2Â÷VæVB'’Æ¶&CäsÂö¶&Cã¢€¦WF†÷&VBf–Wwö–çG2ÂBfW&–f–VB§Væ7F–öç2Â##"7G'V7GW&W2Â'V–ÇBg&öÒF†R66VæRÂF†R–æFW‚æ@§F†R&Vv—7G'’&F†W"F†âg&öÒÖVçR6öÖV&öG’Ö–çF–ç2â6'FâÖ†VÇ—2†Ö'W&vW"à ¢¢¥F†R&6VÂ6¶VBf÷"Fö7VÖVçFVBVçG&–W2öæÇ’ÂæBF†BGW&æVB÷WBFò&RF†Rw&öærÆ—7Bâ¢ ¤æò7G'V7GW&R÷6—F–öâ–âF†—2FF6WB—2w&FVBFö7VÖVçFVF(	B¢£SB&R–æfW'&VFæBc€¦6öæ¦V7GW&Æ¢¢(	B6òFö7VÖVçFVBÖöæÇ’v÷VÆB†fR6†—VBf÷W"§Væ7F–öç2âWfW'’7G'V7GW&R&W7VÇ@¦–ç7FVB6'&–W2—G2÷vâÆ6VÖVçBç÷6—F–öåö6öæf–FVæ6VÂ–âF†R6ÖRF‡&VRv÷&G2æBF‡&VP¦6öÆ÷W'2F†R'V–ÆF–ær6&BW6W2ÂæBF†RF"w27VÖÖ'’Æ–æR6÷VçG2F†Rw&FW2g&öÒF†RÆ—7B—@§–çG2âv†B7W'f—fW2&÷WB'V–ÆF–ær—2W7VÆÇ’7G&VWBæB6–FRöb—BÂ6òvVÆÂÖFö7VÖVçFV@§FfW&âv—F‚6öæ¦V7GW&Â÷6—F–öâ—2F†Ræ÷&ÖÂ66R†W&R&F†W"F†âf–ÇW&R(	BæBF†RÖVçP¦æ÷r6—2v†–6‚—2v†–6‚BF†RÖöÖVçBF†Rf—6—F÷"6†ö÷6W2v†W&RFòvòâF†RvFR6ö×&W2WfW'¦6†—v–ç7BF†R&V6÷&B—B§V×2Fó²ÖVçRF†Bw&FVB÷6—F–öâÖ÷&R¶–æFÇ’F†âF†R&V6÷&@¦FöW2v÷VÆB&RF†—2&ö¦V7Bw2v÷'7B¶–æBöb'Vrà ¢¢¥GvòFVfV7G2F†RæWr76W'F–öç26Vv‡B–âF†V—"÷vâ6Æ–6Râ¢¢F†Rf—fR×F"7G&—f—GFVB3c€¦öæÇ’'’fÆW‚×6‡&–æ¶–ærÆ&VÇ2÷WB7BF†V—"÷vâ'WGFöç2(	BöæRF–G’&÷rÂÖV7W&VBÂæBÖW72Fð¦Æöö²C²F†RFW6·F÷æVÂ—23ƒ‚æ÷rÂF"FF–ær—2b‚æBÖö&–ÆRG—RãR‚ÂÆVf–æp¦&÷WB#‚öb6Æ6²B&÷F‚f–Ww÷'G2ÂæBF†RvFRÖV7W&W2&÷w2Â÷fW&fÆ÷ræB7VVW¦RB&÷F‚à¤6—‡F‚F"FöW2æ÷Bf—BæBv–ÆÂf–ÂF†W&RâF†R6öæf–FVæ6R6†—2Ç6ò&VæFW&VB–FVçF–6ÆÇ¦w&W’Â&V6W6RÆ–âæ§V××&W7VÇB6ÖÆÆ'VÆR÷WG&æ·2æ6öæbÖ–æfW'&VFöâ7V6–f–6—G“²F†P¦vFRæ÷r&WV—&W2F†Rw&FW2FòF–ffW"'’6öÆ÷W"2vVÆÂ2'’v÷&Bà ¢¢¥F†RFW6·F÷†ÆböbFööÇ2÷6Öö¶U÷&VæFW&W"æÖ§6†Bæ÷B&VVâ'Vææ–ærÂæB—B—2æ÷B6ÆV"f÷ ¦†÷rÆöærâ¢¢—B&÷'FVBWfW'’'VâBF†Rf—'7B6Æ–6²öâF†RÖVçR'WGFöâ(	BöâÖ–æ2vVÆÂ2öà§F†—2'&æ6‚Â&W&öGV6–&Ç’(	BæBWfW'’FW6·F÷76W'F–öâgFW"F†Bö–çBÂ&÷Vv†Ç’F†—&BöbF†P§7V—FRÂ6–×Ç’æWfW"W†V7WFVBv†–ÆRF†R'Vâ&W÷'FVBf–ÇW&RF†B&VBÆ–¶R'&ö¶Vâ6öçG&öÂà¤æ÷F†–ærv26÷fW&–ærF†R'WGFöã¢VÆVÖVçDg&öÕö–çF&WGW&æVBF†R'WGFöâ—G6VÆbB—G2÷vâ6VçG&RÀ§v—F‚æòö–çFW"Æö6²ÂF†RvRf—6–&ÆRæBfö7W6VBâF†R6W6R—2F†R66VæRw2÷vâvV–v‡Bâ@£S32G&–ævÆW2öâ6ögGv&R&VæFW&W"öæRæ–ÖF–öâg&ÖRF¶W2¢£ãCn(	3ã2†ÖV7W&VB’¢¢À¦æBÆ—w&–v‡Bw26Æ–6²v—G2f÷"F†RVÆVÖVçBFò†öÆB7F–ÆÂ7&÷72g&ÖW2&Vf÷&R—Bv–ÆÂ†—B×FW7@¦—BÂ6ò32öbFVfVÇB7F–öâ'VFvWBv2&V–ær7VçBöâg&ÖW2&F†W"F†âöâF†RvRâF†P¦'VFvWB—2æ÷r“2(	B&ööÒf÷"6Æ÷rÖ6†–æRÂæ÷BW&Ö—76–öâf÷"'&ö¶Vâ6öçG&öÂÂ6–æ6R6Æ–6°§F†BæWfW"ÆæG27F–ÆÂf–Ç2â¢¥F†—2—27FæF–ær†¦&BÂæ÷Bf—†VBöæR¢£¢F†R6ÖR7F'fF–öà§v–ÆÂ&WGW&â2F†RF÷vâw&÷w2…$ôDÔ³BÇ&VG’&V6÷&G2bRöbG&–ævÆR†VG&ööÒ’ÂæBF†P¦æW‡B7–×FöÒv–ÆÂv–âÆöö²Æ–¶RT’'Vr&F†W"F†â'VFvWBâgVÆÂGvò×f–Ww÷'B72æ÷p§F¶W2Wv&G2öbFVâÖ–çWFW2†W&S²4Ôô´Uõd”Uuõ%CÖÖö&–ÆWÆFW6·F÷'Vç2öæR†Æbv†–ÆP¦—FW&F–æræB&–çG2F†B—B—2æ÷BF†RvFRà ¢22æWr##bÓ‚Ó2(	BçVÖ&W"F†Bv2w&—GFVâÂfÆ–FFVBÂ6†—VBæBæWfW"&V@ ¢¢¤³2Â6÷fW&vRâ¢¢WfW'’fÆ÷&¦öæR&V6÷&BWF†÷'26÷fW"æÖG&—…ög&7F–öæ(	B†÷r×V6‚öbF†P¦w&÷VæBF†B6öÖ×Væ—G’w2ÖG&—‚6÷fW'2(	Bv—F‚&&U÷6ö–Åög&7F–öæ&W6–FR—BâFööÇ2÷fÆ–FFRç– ¦†2vFVB&÷F‚6–æ6RF†R&V6÷&G2vW&Rw&—GFVâÂæB–æFW‚æ§6öæFVæ÷&ÖÆ—6W2F†R&&R×6ö–Âf–wW&P§7V6–f–6ÆÇ’6òF†Rw&÷VæB6†FW"6âfWF6‚—Böæ6Râ¢¦&VæFW&W'2÷vV"ö§2öfÆ÷&æ§6†BæWfW"6¶V@¦f÷"V—F†W"â¢¢ÆÂFVâ6öÖ×Væ—F–W2vW&RÆçFVBBF†R6–ævÆRÆGF–6RFVç6—G’Ã3"GVæVBöâ6Æ÷6V@§vWB&—&–RÂ6ò6WGFÆVBF÷vâv†÷6R÷vâ&V6÷&B6—2¢£CRRöb—G2w&÷VæB—2&&R¢¢v2G&vâv—F€§F†Rw&÷VæB6Æ÷6VBÂæB6òvW&RF†R6†FVB&—fW&&æ²VæFW'7F÷'’ƒãCR’ÂF†Rf÷&W7BfÆö÷"ƒã3R’æ@§F†RÆ¶W6†÷&R6æBƒã3R’à ¥F†Rg&7F–öâ—2æ÷rF†R&ö&&–Æ—G’F†BÖG&—‚ÆGF–6R6Æ÷B6'&–W2ÆçB(	BæV"GVgG2æ@¦Ö–B6&G2Æ–¶RÂ&V6W6RF†–ææ–æröæRæBæ÷BF†R÷F†W"v÷VÆBWB6VÒW†7FÇ’BF†R7&÷76÷fW §v†W&RF†R6†ævRöb&W&W6VçFF–öâ—2ÖVçBFò&R–çf—6–&ÆRâ—B—2F†R6ÖR'VÆRF†Rf÷&"Æ–W ¦†2Çv—2Æ–VBFò—G2÷vâ&V6÷&FVBFVç6—F–W2ÂöâF†Rf–VÆBF†RÖG&—‚Æ–W"–væ÷&VBà ¢Ò¢¥vWB&—&–R—2VçF÷V6†VB¢¢Â&V6W6R—B&V6÷&G2ãæBã—2F†Ræ6†÷"âæ÷F†–ærF†P¢F‡&VRÖ7&—F–2&—&–R7vVWGVæVB†2Ö÷fVBÂæBF†R6†ævR6âöæÇ’WfW"§&VÖ÷fR¢–ç7Fæ6W2à¢ÖV7W&VBB#ƒ9sƒv–ç7BÖ–æBF‡&VRf—†VB7FF–öç3¢vWB&—&–R¢£3c“s’G&—2v–ç7@¢3cƒc2¢¢‚³ã2RÂv†–6‚—2F†R&W6‡VffÆVB&æFöÒG&rÂæ÷BæWrvVöÖWG'’’Â6WGFÆVBF÷và¢¢£C#’#ƒv–ç7BCCcƒ2¢¢Ž(‰#"ã‚RÂ2#s‚fÆ÷&–ç7Fæ6W2v–ç7B2ƒC"’ÂÖ'6‚VFvP¢¢£#“’cv–ç7B3‚#3R¢¢Ž(‰#"ã’R’âF†R66VæRvWG2Æ–v‡FW"W†7FÇ’v†W&R&V6÷&B6—2F†P¢w&÷VæB—2&&Rà¢Ò¢¤ÖV7W&VBÂ7&÷72F†RV–v‡B6öÖ×Væ—F–W2F†B†fR6ÆVâ6×Æ–ær7FF–öâ¢£¢ÆçFVBFVç6—G¢æ÷r7ç2¢£"ã#(	3bã“GVgG2W"Ü+"¢¢v†W&R—Bv2öæRf–wW&RWfW'—v†W&RÂæBF†R–×Æ–V@¢gVÆÂÖ6÷fW"FVç6—G’w&VW2B¢£bã3(	3‚ãR¢¢v–ç7BÆGF–6R6''––ærrã3à¢Ò¢¥F†RvFR6·2&÷F‚†ÇfW2¢¢Â&V6W6Rç7vW&–æröæÇ’F†Rf—'7B—2†÷rF†—2vVçBVææ÷F–6VC ¢F†BV6‚6öÖ×Væ—G’w2WF†÷&VBçVÖ&W"&V6†W2F†R&VæFW&W"‡&RÖfWF6†VBg&öÒF†R&V6÷&G2Âæ÷@¢6ö×&VBv–ç7B6÷’öbF†R&VæFW&W"’ÂæBF†BF†R7v&BöâF†Rw&÷VæBföÆÆ÷w2—BâF†P¢6V6öæB76W'F–öâf–Ç2–âF†R÷F†W"F—&V7F–öâFöò(	B–bWfW'’6öÖ×Væ—G’vVçB&6²FòöæP¢FVç6—G’ÂF†RW"ÖÜ+"7&VBv÷VÆB6öÆÆ6RF÷v&BæBF†R–×Æ–VBf–wW&W2v÷VÆBfâ÷W@¢7&÷72F†Rã3^(	3ãF†R&V6÷&G2v—fRà¢Ò¢¤öæRçF’×f7V—G’wV&BÖ÷fVBæBF†RFöÆW&æ6RF–Bæ÷Bâ¢¢¢&FWF–ÆVBfÆ÷&&ö÷G26†&RF†P¢FW'&–âæBvFW"7W&f6W2"¢&WV—&W2Ö–æ–×VÒ6×ÆR6òF†BÆçF–æræ÷F†–ær6ææ÷B&W÷'B¢W&fV7Bv÷'7BW'&÷#²—G27FF–öâ7FæG2–âF†R6WGFÆVBF÷vâÂæBF†RÖö&–ÆR6öæRF†W&Ræ÷r†öÆG0¢cr&ö÷FVBÆçG2v–ç7B&÷WBS&Vf÷&RâF†RwV&B—2S²F†RRÓRÒ&ö÷BFöÆW&æ6R—0¢VçF÷V6†VBâF†BçVÖ&W"—2&÷W'G’öbF†RFF6WBæ÷r&F†W"F†âöbF†R&VæFW&W"à ¢¢¥Gvòf–æF–æw2ÖV7W&VBöâF†Rv’ÂæBæ÷Bf—†VBF†Vââ&÷F‚f—†VB##bÓ‚Ó2(	B6VR&VÆ÷râ¢¢3f¦—FVÒ’&VG2F†R&—fW%ö&æ¶6†÷Bv–ç7B¦öæRw26÷&Fw&72(	B'WBw&÷VæBv—F†–âV–v‡BÖWG&W2ö`§vFW"—2F†RÔ%4‚¦öæR'’W‡FVçBÂæBF†R6†÷Bw27v&B—2VçF—&VÇ’£Fö£v—F‚æò£–à¦—BBÆÂâæBF†R'ã#R6Ò7&–w2"&R&WGFW"W‡Æ–æVB'’7V6–W2F†â'’FVç6—G“ ¦çW†%öGfVææBç–×†VööF÷&F&RfÆöF–ærÖÆVfVBVF–72&V6÷&FVBBã(	3ãÒv†÷6P¦÷vâV&æ6VFW‡B6—2F†W’fÆöB–â÷VâvFW"ÂæBF†W’vW&R¢£bãRRöbF†RGVgG27FæF–æp¦öâF†BG'’&æ²¢¢Â&V6W6R&öÆS¢VÖW&vVçFv2ÆÂF†R&VæFW&W"6÷VÆB6VRâf—†–ærF†B—2FF¦f–VÆB–âF†RV&Æ—6†VBfö6'VÆ'’&Vf÷&R—B—2Æ–æR–âF†R&VæFW&W"(	B&VæFW&W"F†BFV6–FV@§v†–6‚ÆçG2fÆöB'’&VF–ærF†V—"†V–v‡G2v÷VÆB&RwVW76–ærBW†7FÇ’F†Rö–çBF†—2&ö¦V7@§&VgW6W2Fòà ¢22æWr##bÓ‚Ó2(	BF†RG2vW&R7FæF–æröâ6ö–ÂÂæB&÷6Rv2F†RöæÇ’F†–ærF†B6–B6ð ¢¢¤³2ÂF†R6V6öæBf–æF–ærâ¢¢vFW"Æ–Ç’æB6GF–ÂvW&RF†R6ÖR&V6÷&BFòF†RÆ6W#¢&÷F€¦&öÆS¢VÖW&vVçFÂæBF†R&öÆR—2v†B7FF–öâ‚–&VBâ6òF†RÖ'6‚6öÖ×Væ—G’v2ÆçFV@¦–FVçF–6ÆÇ’öâ&÷F‚6–FW2öb—G2÷vâvFW&Æ–æRÂæBçW†%öGfVææBç–×†VööF÷&F(	@£ã(	3ãÒÂf÷&Ó¢ÖE÷&÷7G&FVÂV&æ6V&fÆöF–ærG2–â÷VâvFW""(	B7FööB2æ¶ÆRÐ¦†–v‚ÖG2&ö÷FVB–âF†R6ö–ÂöbF†RG'’&æ²â¢¥F†RWf–FVæ6Rv2–âF†R&V6÷&BæBVç&VF&ÆR'¦ç—F†–ær'WBW'6öââ¢  ¦FFöfÆ÷&ö–æFW‚æ§6öææ÷rV&Æ—6†W27V'7G&FW6fö6'VÆ'’æBWfW'’&öÆS¢VÖW&vVçF&V6÷&@§7FFW2öæS  §ÂfÇVRÂ†&—BÂÖ’&RÆçFVBÀ§ÂÒÒ×ÂÒÒ×ÂÒÒ×À§Â6ö–ÆÂ&ö÷FVBw&÷VæB&÷fRF†RvFW#²F†RFVfVÇBv†VâF†Rf–VÆB—2'6VçBÂG'’w&÷VæBöæÇ’À§Â6GW&FVE÷6ö–ÆÂF†RVÖW&vVçB†&—B(	BvWBw&÷VæBõ"7FæF–ærvFW"ÂföÆ–vR&÷fRF†R7W&f6RÂ&÷F‚6–FW2À§Â÷Vå÷vFW&Â&ö÷FVB&VÆ÷rF†R7W&f6RÂÆVfW2fÆöF–ærôâ—BÂ÷fW"vFW"öæÇ’À ¢Ò¢¥F†RfÆ–FF÷"&VgW6W2F†RVçÆçF&ÆR&V6÷&B¢¢Âæ÷B§W7BF†RVæ¶æ÷vâv÷&C¢â÷Vå÷vFW& ¢7V6–W2–â¦öæRv†÷6RW‡FVçBæWfW"&V6†W2vFW"(	B÷"'VffW"F†B7F'G2BF†R&æ²&F†W ¢F†âBF†RvFW&Æ–æR(	B—2âW'&÷"Â&V6W6R&V6÷&BF†B6âæWfW"&RG&vâ—26Æ–ÒF†P¢vÆ·F‡&÷Vv‚FöW2æ÷BÖ¶Râ6—‚æWr6VÆb×FW7G2–âFööÇ2÷FW7E÷fÆ–FFRç–à¢Ò¢¥F†R6öÖ×Væ—G’—27Æ—BÂæ÷BF†R6Æ÷BG&÷VBâ¢¢fÆ÷&æ§6–6·2g&öÒF†R7V'6WBÆVvÂöâF†P¢6–FRöbF†RvFW&Æ–æR—B—2ÆçF–ærÂv—F‚F†RvV–v‡G2&Væ÷&ÖÆ—6VB÷fW"F†B7V'6WBâ&VgW6–æp¢F†R6Æ÷BgFW"F†R–6²v÷VÆB†fR&VVâöæRÆ–æR6†÷'FW"æBv÷VÆB†fRF†–ææVBF†RG'’Ö'6€¢VFvR'’F†RÆ–Æ–W2rbãRR6†&S²ÖG&—…ög&7F–öæãsRFöW2æ÷B7F÷ÖVæ–ærãsR&V6W6RGvð¢öbF†B6öÖ×Væ—G’w27V6–W2fÆöBà¢Ò¢¤ÖV7W&VBÂB#ƒ9sƒâ¢¢â‚Ò7vVWöbF†RÖöFVÆÆVB&÷ƒ¢¢£#“’G'’Ö'6‚ÖVFvR7FF–öç2¢ ¢ƒ#ƒ’ÆçF&ÆRBÆÂ’æB¢£#ƒb÷fW"vFW"¢¢â&÷F‚Æ–Æ–W2vW&RÆVvÂBÆÂ#ƒ’G'’7FF–öç0¢æB&Ræ÷rÆVvÂBæöæS²F†R6GF–Â—2Væ6†ævVBB#ƒ’G'’ò#s2vWBâBF†RÖ'6‚ÖVFvP¢7FF–öâæV&W7BF†Rf÷&·2F†R7v&B†öÆG2—G2FVç6—G’(	B¢£"Cƒ2(i""Cƒ&ö÷FVB–ç7Fæ6W2À¢CrSS(i"CrC3RG&–ævÆW2¢¢(	BæBF†RGvò†VE÷&–†VG2F†B7FööBöâF†BG'’&æ²Âv†–6€¢&RF†RÆ–Ç’&Æöö×2Â&RvöæRâvWB×&—&–R6öçG&öÂ7FF–öâ—2–FVçF–6Âà¢Ò¢¥F†RvFR6·2F†RÆ6W"Âæ÷B6÷’öb—G2'VÆW2â¢¢fÆ÷&ç7FF–öäöb†RÂâÂ7V6–W4–B–'Vç0¢F†R6ÖR7FF–öâ‚–F†R66GFW"'Vç3²F†R6Öö¶R7vVW2F†R&÷‚v—F‚—BB&÷F‚f–Ww÷'G2æ@¢76W'G2æòfÆöF–ærÖÆVfVBVF–2†2G'’7FF–öâÂF†BF†RÆ–Æ–W27F–ÆÂ†fRvWBöæW2Âæ@¢F†BF†R6GF–Â7F–ÆÂ7FæG2öâ&÷F‚6–FW2(	BF†BÆ7BöæR&V6W6RÆ6W"F†B†B&VgW6V@¢¦WfW'—F†–ær¢öâF†B&æ²v÷VÆB÷F†W'v—6R&VB272à¢Ò¢¥v†BF†—2FöW2æ÷B6Æ–Òâ¢¢F†BF†RÆ–Æ–W2&RBF†Rf÷&·2BÆÂ—27F–ÆÂ–æfW'&VFg&öÒ¢&Vv–öæÂfÆ÷&†7v–æµ÷v–Æ†VÆÕó““F’ÂBFö¶VâFVç6—G’ÂæBv†W&RF†RG26—Bv—F†–âF†P¢V–v‡BÖÖWG&RÖ'6‚VFvR—2F†R66GFW"w2Âæ÷B6÷W&6Rw2âF†R6†ævRÖ÷fW27V6–W2g&öÒw&÷Væ@¢—B6ææ÷Bö67W’Fòw&÷VæB—B6ã²—B—2æ÷BæWrWf–FVæ6RF†B—Bv2F†W&Rà ¢22¶æ÷vâvV¶æW76W2Â7FFVBÆ–æÇ £â¢¥F†RvFRF†BW†—7G2Fò6F6‚'V–ÆF–ær7FæF–æröâæ÷F†–ær&W÷'FVBW&fV7@¢ÆæF–ærf÷"f÷'Bƒ3"Ò7BF†RVFvRöbF†Rv÷&ÆBâ¢¢f÷W'FVVâ7G'V7GW&W2vVçB–âöâ##bÓ‚Ó@¢Æö6ÂR³3(
b³ƒ²F†RSƒ3Eö†&&÷%ö7WF†V–v‡Ff–VÆB7F÷2BR³3#âF†B×V6‚—2ÃCw0¢&ö&ÆVÒBf÷W"F–ÖW2F†RF—7Fæ6RæB—B—2†öæW7FÇ’FV6Æ&VBöâWfW'’&V6÷&Bâ¢¥F†R'@¢F†B—2FVfV7B–âF†RÖ6†–æW'’&F†W"F†â–âF†RFF¢£¢FööÇ2ö†V–v‡Ff–VÆBç–6Æ×0¢÷WG6–FRF†R&÷‚Â6òF†Rw&÷VæBÖ6öçF7B6†V6²6×ÆVBF†R6Æ×VBVFvRf÷"F†R7G'V7GW&Rw0¢&6RäBf÷"WfW'’ö–çBöb—G2÷WFÆ–æRÂv÷BF†R6ÖRçVÖ&W"Gv–6RÂæB6öæ6ÇVFVBF†BF†P¢f÷'BÖVWG2F†Rw&÷VæBâWfW'’7G'V7GW&RÃC6÷fW'2v26Vv‡BöæÇ’&V6W6RF†R6Æ×VBVFvP¢f&–W2ÆöærvÆÂæB&öGV6VBv²F†Rf÷'Bv2f"Væ÷Vv‚÷WBæB7V&RVæ÷Vv‚öâFð¢&öGV6RæöæRâF†RvFR6÷VÆB6VR'V–ÆF–æw2F†BvW&RæV&Ç’&–v‡BæBv2&Æ–æBFòöæRF†@¢v26ö×ÆWFVÇ’w&öærâ†V–v‡Ff–VÆBæ6÷fW'2‚–æ÷r6·2v†WF†W"F†W&R—2ç’w&÷VæBF†W&R@¢ÆÂ&Vf÷&R6¶–ær†÷r†–v‚—B—2ÂF†R66†VÖ6'&–W2â÷WG6–FUöÖöFVÆÆVEöw&÷VæF7FFP¢&W6–FR&ö6…öæ÷EöÖöFVÆÆVFÂæBF†RFV6Æ&F–öâ—26†V6¶VBv–ç7BF†RÖV7W&VÖVçB–à¢&÷F‚F—&V7F–öç2âGW&æ–ær—Böâ–ÖÖVF–FVÇ’fÆvvVBGvò7G'V7GW&W2–â÷F†W"&6VÇ2F†@¢æ÷F†–ær†B6Vv‡Bâ¢¥3&R&6VÂ†"’F†VâÆæFVBF†R6ÖRF’¢¢æBF†Rf–VÆBæ÷r&V6†W2R³sÂ6òGvVÇfRö`¢F†Rf÷W'FVVâf÷'B7G'V7GW&W2ÆæBæBF†V—"FV6Æ&F–öç2&RvöæRâGvòFòæ÷BÂf÷"¢F–ffW&VçBæB&WGFW"&V6öã¢F†Rf÷'B6—G2öâÆFVRF†BfÆÇ2FòF†R&—fW"&WGvVVà¢â³#CRæBâ³#sÂæBF†R7Fö6¶FRw2æ÷'F‚vÆÂæBF†R6öÖÖæFçBw2V'FW'27&÷72F†P¢F÷öbF†BfÆÂ'’ãCÒæBãCbÒâ¢¤æò7WBÂf–ÆÂÂ&WfWFÖVçB÷"f÷VæFF–öâ—2ÖöFVÆÆV@¢ç—v†W&R–âF†—2&ö¦V7B¢¢ÂæBF†R&VÂv÷&²Æ–æÇ’†BöæRâÃCbv2&Ww&—GFVâF†R6ÖP¢F’Fò6’6òâF†R&Æ–æFæW72F†Rf÷'BW‡÷6VB—2f—†VB&Vv&FÆW72öbv†WF†W"ç—F†–æp¢7W'&VçFÇ’æVVG2F†RæWr7FFRà £â¢¥F†R&—&–RÆ÷6W2&Æ–æB6–FRÖ'’×6–FRv–ç7B§VÇ’†÷Föw&‚Â–âVæFW"6V6öæBÀ¢æBvRæ÷r¶æ÷rW†7FÇ’v‡’â¢¢f÷W"×&6VÂ7vVWöâ##bÓ‚ÓWBV6‚–V6RöbF†P¢fVvWFF–öâF‡&÷Vv‚—G2÷vâ'V–ÆFW"ÖæBÖ7&—F–2Æö÷v–ç7BfW&–f–VB†÷Föw&‡2ö`¢7W'f—f–ær–ÆÆ–æö—2FÆÆw&72Âv—F‚&Æ–æBô"2F†R§VFvVÖVçBâF‡&VR7&—F–72&âöâöæP¢–FVçF–6Â6†÷B6WBâÆÂF‡&VRÆ÷7BâGvòöbF†VÒÂöâF–ffW&VçB&VfW&Væ6W2æBF–ffW&Vç@¢g&Ö–æw2ÂÆ÷7BöâF†R¢§6ÖR¢¢fVGW&Râv†BföÆÆ÷w2—2F†RÖV7W&VB7FFRÂ&V6÷&FV@¢&V6W6R—B—2Ö÷&RW6VgVÂF†âF†R7VÖÖ'’&æVVG2v÷&²#  ¢Ò¢¥F†RÖ–BÖf–VÆB6†VWB—2F—66&FVBBãCSRÒâ¢¢6æ÷’&–æw2g&öÒ"ãRÒFòCS2Ò6—B@¢F†R7v&BF÷²g&öÒSã‚Ò÷WGv&BWfW'’&–ærG&÷2Fò’ÒãVv—F‚Ö6²Òæ@¢F†R6†FW"F—66&G2—BâF†RfVvWFFVB7W&f6RF†W&Vf÷&RVæG2v†W&RF†Rför—2öæÇ¢#rRÂæBF†R“2R†¦Rv÷&ÆBæ§6FW6–vç2f÷"B#“Ò—2æWfW"&VæFW&VBöçFòç¢fVvWFFVB—†VÂâ¢¤ÆÂF‡&VR&6VÇ2†fR&VVâ6öçfW&v–æröâ6öÆ÷W"æòf—6–&ÆP¢7W&f6R–âF†R66VæR&V6†W2â¢¢F†—2öæRf7B&öGV6W2F†R&Æ–æBFVÆÂ–â&÷F‚—'2À¢F†RÖ—76–ærW&–Â&V6W76–öâÂF†R6öÆÆ6VBw&–âæBF†R&–ær6VÒ&VÆ÷rà¢Ò¢¥F†W&R—2æòW&–Â&V6W76–öâöâfÆBw&÷VæBæBF†W&R7G'V7GW&ÆÇ’6ææ÷B&Râ¢¢B¢ãc‚ÒW–Rv—F‚S\+fW'F–6Âf–VÆB÷fW"ƒ&÷w2Âw&÷VæBö–çBBF—7Fæ6R¦B ¢ÆæG2#“ã’öF‚&VÆ÷rF†R†÷&—¦öâ(	B6òF†RVçF—&Rför&×g&öÒRFò“2RÆ—fW0¢&WGvVVâ&÷w2C"æBCbâ6—‚—†VÇ2öbFÖ÷7†W&R–ââƒ×—†VÂg&ÖRâöæÇ’fW'F–6À¢7G'V7GW&R6'&–VB–çFòF†RF—7Fæ6R6â'W’&V6W76–öâ†W&S²W‡öæVçF–ÂF—7Fæ6Rföp¢6ææ÷Bà¢Ò¢¤&–ær6VÒG&w27G&–v‡BÆ–æR7&÷72F†Rg&ÖRâ¢¢ETäRæÖ–Bç&F—W2Ò#rãÖÂæ@¢öâfÆBw&÷VæB6öç7FçB&F—W2Ö2Fò6öç7FçB67&VVâ&÷r(	B&VF–7FVBCC‚ã‚À¢ÖV7W&VBB&÷rCS–â&—&–U÷6÷WF†Â&¦÷"×7G&–v‡B7&÷72ÆÂ#ƒ6öÇVÖç2à¢Ò¢¤w&–â6öÆÆ6W2v—F‚FWF‚v†W&RF†R†÷Föw&‡2r—2fÆBâ¢¢\9sR†–v‚×72$Õ2–à¢&æG2F÷vâg&öÒF†RÆæB÷6·’&÷VæF'“¢÷W'22ã‚òBãbò#ã"Â&÷F‚&VfW&Væ6W0¢‚ã‚ò3ãBò3’ã2æB3’ã2òCãròCã2à¢Ò¢¥F†R†÷&—¦öâF–Ö&W"—2æV&Ç’'6VçBâ¢¢F–Ö&W"—2FWFV7FVB–â¢£3R¢¢öb†÷&—¦öà¢6öÇVÖç2÷fW&ÆÂæB2ãbR7&÷72F†R6VçG&ÂGvò×F†—&G2Âv–ç7B¢£R¢¢öb6öÇVÖç2–à¢WfW'’&æBöbF†R&VfW&Væ6R–æ6ÇVF–ær—G2f–çFW7BâF†R.(	3B‚&æB¦†V–v‡B¢—2†öæW7@¢&—F†ÖWF–3²F†RV×F–æW72—2æ÷Bâ&÷VæBF†B&W÷'FVB&R×Föæ–ærF†—2&æB†B–âf7@¢&VGV6VB—G2FWFV7F–öâ6÷fW"g&öÒ#ãRFòã’RÂæBF†RF&vWB—Bv2v—fVà¢…vV&W"ã3n(	3ãcr’FöW2æ÷BW†—7B–âF†R&VfW&Væ6RBç’F‡&W6†öÆB(	BF†BW'&÷"v0¢F†R'&–Vbw2Âæ÷BF†R'V–ÆFW"w2à¢Ò¢¤7&÷vç2&VB2&÷VÆFW'2â¢¢f–æRÖFWF–Â&F–òã#>(	3ã3Bv–ç7BF†R†÷Föw&‚w0¢ãc(	3ãcB(	B÷W"7&÷vç2B#(	3cÒ6''’F†Rf–æR×66ÆRFW‡GW&Röb†÷Föw&‚w0¢¶–ÆöÖWG&RÖF—7FçBG&VVÆ–æRâ6†F÷w26Æ—FòÆ—FW&ÂƒÃÃ–v†W&RF†R†÷Föw&‚w0¢F&¶W7BFV6–ÆR—2ÂN(	3#rÂæB7VæÆ—B7&÷vâF÷2&R¢¦&ÇVR¢¢„~(‰$"(‰#’Fò(‰##b’v†W&P¢F†R†÷Föw&‚w2&Rv&Òw&VVâ‚³2Fò³#B’à¢Ò¢¥F†R6†÷B6WB†2öæÇ’öæR÷Vâ×&—&–Rf–Wrâ¢¢&—&–U÷6÷WF†7FæG22ãCbÒg&öÒ¢G'Væ²v—F‚#2ãBR÷Vâ6·’v–ç7B&—&–U÷vW7Fw2“RãBRâF†B6V6öæBævÆRW†—7G0¢&V6—6VÇ’2F†R6öçG&öÂF†B6W&FW2GVæVBf–Wrg&öÒf—†VBöæRÂ6ð¢&—&–U÷vW7F†2&VVâGVæVBv–ç7B—G6VÆbv—F‚æò6öçG&öÂà¢Ò¢¦&—fW%ö&æ¶f–Ç2—G2÷vâ'&–VbæBF†RfVÇB—2F†R&VæFW&W"Âæ÷BF†RFFâ¢¢¦öæR¢7V6–f–W26÷&Fw&72Bã.(	3"ãÒæBC(	3SRR6÷fW"v—F‚&&U÷6ö–Åög&7F–öã¢ã²F†P¢g&ÖR6†÷w2ã#R6Ò7&–w2öâf—6–&ÆR&&R6ö–Â–âæV"×&÷w2à ¢GvòF†–æw26ÖR÷WBöbF†R7vVW6ÆVâæB6†÷VÆB&R6–B2Æ–æÇ’2F†Rf–ÇW&W2âF†P¢¢¤§VÇ’†VæöÆöw’—26÷'&V7BB6÷W&6R¢¢(	BWfW'’v&Ò×6V6öâw&72fVvWFF—fRv—F‚çVÆÀ¢–æfÆ÷&W66Væ6RÂ6GF–Âg'V—F–æræB'&÷vâÂ&×ÆVfÆW72ÂæBÆ—fRwV&BF†B7W&W76W0¢æB&W÷'G2ç’&V6÷&BF†B6öçG&F–7G2—G6VÆbâæBF†R¢¦fÆ÷&FF6WB—2F†RöæR&6VÀ¢7&—F–276VBv—F†÷WB&W6W'fF–öâ¢¢âF†R&VæFW&W"—2v†B—2f–Æ–ær—Bà ¢GvòÖWF†öFöÆöv–6Â6÷'&V7F–öç2v÷'F‚¶VW–ærÂ&÷F‚öbv†–6‚–çfÆ–FFRçVÖ&W'2F†—0¢&ö¦V7B†2V÷FVC  ¢Ò¢¥F†R&–Ö'’&VfW&Væ6Rv2F†Rw&öær†÷Föw&‚â¢¢GWvU÷FÆÆw&75ó#‚ÓrÓ#Bæ§v—0¢F—FÆVB"¥&W7F÷&VB¢FÆÆw&72&—&–R"æBFW67&–&VB2%&—&–RÆçF–ær"öâf÷&ÖW ¢w&–7VÇGW&Âf–VÆB(	B6VVBÖ—‚öâÆ÷vVBw&÷VæBÂæB&W7F÷&F–öç2&R&÷Vv‡Bf÷"&V–æp¢f÷&"×&–6‚âF†RæWfW"×Æ÷vVBvööGv÷'F‚7FæB—2F†R&WGFW"æÆöwVRf÷"VæÖævVBƒ3P¢&—&–RâçäÖV7W&VBfÆ÷vW"ÆöC¢ÆçF–ær"ã“RÂf—&v–â&VÖæçBãsž(	3RãSBRâF†R†öæW7@¢F&vWB—2¢£N(	3bRÂæ÷B2ãƒ’R¢¢ççâ¢¥D„R4õ%$T5D”ôât2$”t…BäB•E2åTÔ$U%2$P¢t•D„E$tâÂ##bÓ‚ÓR'’"ÕsF2†#’â¢¢æV—F†W"6ÆW6R7W'f—fW26†V6¶–ærâ¢¤æòæWfW"×Æ÷vV@¢&VÖæçB†÷Föw&‚—26öÖÖ—GFVBFòF†—2&W÷6—F÷'’æBæò6÷W&6R&V6÷&BFW67&–&W2öæR¢¢(	@¢F†R‡&6Rö67W'2öæ6R–âFF÷6÷W&6W2öÂ–ç6–FRF†R&V6÷&BöbF†RÆçF–ærÂ6—F–æp¢æ÷F†–ær(	B6òF†Rãsž(	3RãSBR†Æb—2Vç6÷W&6VBâæB"ã“RFöW2æ÷B&W&öGV6S¢F†P¢6öÖÖ—GFVB&V6—R&VG2¢£RãSBR¢¢öâF†Bg&ÖRÂrã"Röâ—G2æV&W7BV'FW"æB#Rãƒ"P¢v—F‚—G2GvòFW7G2&V÷&FW&VBâ¢¥F†W&R—2F†W&Vf÷&RæòN(	3bRF&vWB¢¢ÂæBF†—2f–ÆR×W7@¢æ÷B&R&VB26WGF–æröæRâæöFRFööÇ2öÖV7W&Uö&ÆööÕ÷F&vWBæÖ§6&–çG2ÆÂöb—C°¢$ôDÔ*r"ÕsF2†#’6'&–W2F†R&V6öæ–æræBF†RF‡&VR&÷WFW2÷WBà¢Ò¢¥Gvò&÷VæG2vW&R§VFvVBBF†Rw&öærÆöö²ÖævÆRâ¢¢F†R6†÷B†&æW726WBæò—F6‚v†–ÆP¢F†R&VfW&Væ6R†÷Föw&†W"†BF–ÇFVBF÷vâã,+Â6òWfW'’&æV&W7BV'FW""çVÖ&W ¢6ö×&VBF†R†÷Föw&‚B"Òv–ç7B÷W"&VæFW"BBÒ(	BæBæV"Öf–VÆBfVvWFF–öâv0¢W†7FÇ’v†BF†÷6R&÷VæG2vW&RGVæ–ærâF†R†&æW72—2æ÷r—F6‚ÖÖF6†VBæB&–çG2—G0¢—F6‚â6÷'&V7F–ær—BÖ¶W2F†Rv§v÷'6R£¢ãrRv–ç7Bf—&v–â&VÖæçBw2"ã“rRà¢Ò‡VR÷6GW&F–öâFW7B6ææ÷B6W&FR§VÇ’g&öÒö7Fö&W"†W&R(	BF†Rö7Fö&W"æVvF—fP¢6öçG&öÂÆæG2¦&WGvVVâ¢F†RGvò§VÇ’†÷Föw&‡2âF†BÖWG&–26†÷VÆBæ÷B&RV÷FVB'¢ç–öæRÂ–æ6ÇVF–ærF†—2f–ÆRà £â¢¥F†Rf÷&ÖW"6Æ÷r×&VæFW&W"vÆ¶–ærf–ÇW&R—2&W6öÇfVBv—F†÷WBvV¶Væ–ær—G2F—7Fæ6R&"â¢ ¢Ö÷fVÖVçBæ÷r6öç7VÖW2WFòV'FW"×6V6öæBöb&VÂg&ÖRF–ÖR–âFW'&–âÖæBÖ6öÆÆ—6–öà¢7V'7FW2æòÆ&vW"F†âãR2â6ögGv&R&VæFW&W"G&v–æröæÇ’Gvòg&ÖW2W"6V6öæBæð¢ÆöævW"GW&ç2ãCRÒ÷2vÆ²–çFò7&vÂÂv†–ÆRF†R6†÷'B7V'7FW2&WF–â&æ²æB'V–ÆF–æp¢6öÆÆ—6–öâ67W&7’âF†Rf÷&Vw&÷VæB6Öö¶R'Vâ76W2F†R6ÖRvÆ²ÖF—7Fæ6R76W'F–öâ@¢&÷F‚3“9ssƒæB#ƒ9sƒâ7W'&VçBgVÆÂ×66VæR'VFvWG2&RC’òS2G&r6ÆÇ2æB3s‚ÃcCrð¢C“’Ã3C2G&–ævÆW2&W7V7F—fVÇ“²F†RFW6·F÷&VæFW&W"&VÖ–ç26Æ÷rB"g2VæFW"7v–gE6†FW"À¢'WBVÆ6VB×F–ÖRvÆ¶–ær—2æòÆöævW"6÷WÆVBFòF†Bg&ÖR6÷VçBà £â¢¤öæR7G'V7GW&R&V6÷&BFöW2æ÷B&÷fRF†R66†VÖâ¢¢F†R6Vvæ6‚W†W&6—6W2†6W2Â¢'V–ÆF–ærÖ÷fRÂæBF†RgVÆÂ6öæf–FVæ6R&ævRÂ'WBF†RÖöFVÂ†2æ÷BÖWBf÷'BÂ'&–FvRÂ÷ ¢&÷röb7F÷&Vg&öçG2–WBâW‡V7B66†VÖ&W77W&RBÖ–ÆW7FöæRà£"â¢¦6öç7G'V7F–öã¢&ÆÆööåög&ÖVöâF†R6Vvæ6‚—2&ö&&Ç’w&öær¢¢æB—2fÆvvVB27V6€¢–âF†R&V6÷&Bâ&ÆÆööâg&Ö–ær÷7FFFW2F†Rƒ3'V–ÆF–ær'’–V"âÆVgBf—6–&ÆR&F†W ¢F†â6–ÆVçFÇ’7vVBÂ&V6W6R7V'7F—GWF–æröæRwVW72f÷"æ÷F†W"—2æ÷Bf—‚à£2â¢¥F†R6Vvæ6‚vÆÆW'’&VF–ærv2&Wf—6VBöâF’öæR¢¢Âg&öÒ&vÆÆW'’Â6öæ¦V7GW&Â"Fð¢&æòvÆÆW'’Â–æfW'&VB"ÂgFW"÷Væ–ærF†RGvò&WG&÷7V7F—fR–ÖvW2F†R&WòÇ&VG’†VÆBà¢&÷F‚6†÷ræòfW&æFæB&÷F‚6†÷rF†Rƒ#’Æör6&–â7W'f—f–ær2âGF6†VBv–ærâF†P¢–ÖvW2&Ræ÷B–æFWVæFVçBöbV6‚÷F†W"Â6òF†—2—2–æfW&Væ6RÂæ÷BFö7VÖVçFF–öâ(	BæBF†P¢g&ÖU÷FfW&æ&6†WG—Ræ÷r†2Fò7W÷'BâGF6†VBÆörv–ærà£Bâ¢¥Gvò6÷W&6W2†fRæòvV"&6†—fRâ¢¢G&Æö–…ö†÷FVÇ6†2æòv–&6²6æ6†÷BæBF†P¢fÆ–FF÷"v&ç2&÷WB—BöâWfW'’'Vã²F†Rv&æ–ær—26÷'&V7BæB7FæG2VçF–Â6öÖVöæP¢&6†—fW2F†RvRâvRÔ'Vâw2&6†—fVE÷W&Âö–çG2B66ææVBVF—F–öâöbF†R&öö²&F†W ¢F†âF†RG&ç67&—F–öâ7GVÆÇ’&VBGW&–ær&W6V&6‚(	Bæ÷FVB–âF†R6÷W&6R&V6÷&Bà£Râ¢¥6WfW&Â&W6V&6‚6Æ–×2&R6æ—WBÖFW&—fVBâ¢¢Væ7–6Æ÷VF–æ6†–6vö†—7F÷'’æ÷&v&WGW&æV@¢S2F‡&÷Vv†÷WBF†R&W6V&6‚6W76–öâÂæBfWr6—FF–öç2–âF†RF÷76–W'2&W7Böâ6V&6‚Ö–æFW€¢6æ—WG2&F†W"F†â&WG&–WfVBvW2âF†W’×W7B&R&RÖfWF6†VB&Vf÷&Rç’öbF†VÒ—2&öÖ÷FV@¢FòFö7VÖVçFVFà£bâ¢¥F†R6öæÆW’õ7FVÇ¦W"&–v‡G2VW7F–öâ—2÷Vââ¢¢Ö&¶VB6†V6µ÷&WV—&VF²æò76WBÖ’&P¢FW&—fVBg&öÒ—BVçF–Â7Fæf÷&B6÷—&–v‡B&VæWvÂFF&6R6†V6²—2&V6÷&FVBà£râ¢¥F†Rƒ3RÆ¶R7FvR—2wVW72â¢¢Sƒ+ãRgB4ÂÂFvvVB6öæ¦V7GW&ÂÂæBF†RVçF—&P¢fW'F–6ÂFGVÒ†æw2öfb—Bà£‚â¢¤d•„TB(	BF†Rv†—FR–çBæ÷r&VG22v†—FRâ¢¢F†RV&Æ–W"F–væ÷6—2–âF†—2f–ÆR†vV°¢6·’6öçG&–'WF–öâBw&¦–ær7VâævÆR’v2w&öærÂæBw&öær–âv’v÷'F‚&V6÷&F–æs¢F†P¢FâvÆÂv25DÄRT$Ä•4„TB54UBÂâöÆFW"&¶RF†B7F–ÆÂ6'&–VBF†R÷fW"ÖF&²ð¢FW‡GW&RâGvò6W&FR6W6W2F†VâGW&æVBW&V†–æB—BâV&Æ—6‚ç6†6†—VBg&öÐ¢76WG2÷vV"öÂv†–6‚öæÇ’&¶Rç6†&Vg&W6†W2Â6ò'Vææ–ærF†RvVæW&F÷"F—&V7FÇ’&WV&Æ—6†V@¢F†R&Wf–÷W2ÖW6‚6–ÆVçFÇ’(	Bæ÷rwV&FVBÂæB—B6—26òv†Vâ—B6÷–W2Ö7FW"F‡&÷Vv‚à¢æBF†R6·’ÖFW&—fVBÕ$TÒVçf—&öæÖVçBv2÷fW'&–F–ærÆ&VFò÷WG&–v‡C¢ÖV7W&VBÂ'&÷vâÆöp¢vÆÂ&VæFW&VBBâ"ô"&F–òöbã‚v–ç7BF†RãsR—G2÷vâ&6R6öÆ÷W"7V6–f–W2Âv—F€¢WfW'’7W&f6R6öçfW&v–æröâF†R6·’6öÆ÷W"v†FWfW"—Bv2ÖFRöbâf÷"&ö¦V7Bv†÷6P¢6Æ–Ò—2F†BFö7VÖVçFVBv†—FRvÆÂ&VG22v†—FRÂF†B—2FFÖ–çFVw&—G’'VrvV&–æp¢âW7F†WF–726÷7GVÖRâF†RVçf—&öæÖVçB—2vöæS²†VÖ—7†W&Rf–ÆÂv—F‚v&Òw&÷VæB&÷Væ6P¢ÇW2F†R7Vâæ÷r6''’F†RÆ–v‡F–ærÂæB‡VR—2&W6W'fVB†Æör"ô"ã3’â&Wf—6—Bv—F‚¢&÷W&Ç’W‡÷6VB„E$’&F†W"F†âÕ$TÒöbâæÇ—F–26·’à£’â¢¤ò—2&¶VB'WB7v—F6†VBöfbÂFVÆ–&W&FVÇ’â¢¢F†R&¶RF‚v÷&·2VæBFòVæBæB—2v—&V@¢2&VÂvÅDbö66ÇW6–öâFW‡GW&RÂ'WBF†R&6†WG—Rw26Æ&ö&B6÷W'6W2æBv–æF÷r&WfVÇ0¢6—B6VçF–ÖWG&RöfbF†RvÆÂæBö66ÇVFRV6‚÷F†W#¢ÖV7W&VB&¶R6öÖW2÷WBBÖVâã#cP¢v—F‚c’RöbFW†VÇ2&VÆ÷r†ÆbÂæBF†R'V–ÆF–ær&VæFW'2'&÷vââ6†÷'FVæ–ærF†RòF—7Fæ6P¢öæÇ’&V6†W2ã3‚â—BæVVG2Æ÷r×öÇ’ò6vRÂæ÷BGVæ–ærGvV²â¢¥´&÷F‚f–wW&W2dô”B(	@¢BÓS‚Â##bÓ‚Ó#s²æBF†RW‡÷'Bv26†—–ær&Æ6²FW‡GW&Rv†VâF†—2v2w&—GFVâÂ6ð¢'&VæFW'2'&÷vâ"v2æ÷B&VF–æröbòâF†R6öæ6ÇW6–öâ7W'f—fW2öâ&VæFW&VBg&ÖS ¢BÓ##rÂ##bÓ‚Ó#‚ÂBF†RF÷öbF†—2f–ÆRåÒ¢¢ÒÖö¶VW2F†RF€¢W†W&6—6VBæB76WG2öÖæ–fW7Bæ§6öæ&V6÷&G2†öæW7FÇ’F†BF†R6†—VB76WB†2æöæRà£â¢¦vÇFb×G&ç6f÷&ÖF–Bæ÷B'Vâ¢¢Â6ò76WG2÷vV"ö7W'&VçFÇ’†öÆG26÷–W2öbF†P¢Væ6ö×&W76VBÖ7FW'2&F†W"F†âÖW6†÷BôµEƒ"FW&—fF—fW2â†&ÖÆW72BCB´#²—B×W7Bv÷&°¢&Vf÷&RF†RF÷vâ66ÆW2à£â¢¤d•„TB(	BF†RÆ–&W'F–W2&Ræ÷rGF6†VBFòF†V—"'V–ÆF–æw2â¢¢F†R&÷fVææ6R÷W&VG0¢7V&¦V7G6æB6†÷w2F†RÆ–&W'F–W2F¶Vâv—F‚F†R'V–ÆF–ær&V–ær–ç7V7FVC¢F†R6Vvæ6‚w0¢f÷W"ÂÃ’öâF†Rw&VVâG&VRÂÃrôÃ‚öâF†RF‡&VRvöÆbö–çBÆ6VÖVçG2â&÷F‚f–Ww2&VæFW"g&öÐ¢öæRFW&—fVB&V6÷&BF‡&÷Vv‚öæRVçG'’&VæFW&W"Â6òF†RæVÂæBF†R6&B6ææ÷BFW67&–&RF†P¢6ÖRÆ–&W'G’F–ffW&VçFÇ’ÂæBF†R6Öö¶R76W'G2F†RF—67&–Ö–æF–ær66R(	B6V6öæB'V–ÆF–æp¢vWG2—G2÷vâ6WBÂæ÷BF†Rv†öÆRÆ—7BÂæB66VæR×v–FRÆ–&W'G’—2æ÷B–ææVBFòç’'V–ÆF–ærà¢¢¤6ö×ÆWFVæW72—2æ÷rVæf÷&6VBf÷"öæR6Æ72öb–çfVçF–öâÂæBöæÇ’öæRâ¢¢fÆ–FFRç– ¢'Vç2F†R–çfW'6R6†V6³¢WfW'’†6Rv†÷6Rfö÷G&–çF÷"÷6—F–öæ—26öæ¦V7GW&Æ×W7B&P¢6Æ–ÖVB'’Æ–&W'G’w26÷fW'3¦f–VÆB(	B7G'V7GW&Uö–E²ç†6Uö–EÒæ7V7FÂFV6Æ&VB'’F†P¢Fö7VÖVçB&F†W"F†â–æfW'&VBg&öÒ—G2v÷&F–ærâ6—‚7V6‚–çfVçF–öç2W†—7B–âF†R6öÖÖ—GFV@¢FF†f—fRfö÷G&–çG2ÂÇW2vÆ¶W"w2÷6—F–öâ“²6—‚FV6Æ&F–öç26÷fW"F†VÒâF†R6VÆb×FW7@¢76W'G2F†RF—67&–Ö–æF–ær66RÂæBF†B66Rv÷B7G&–7FW#¢âVçG'’v†÷6R&÷6R—2¦&÷WB ¢fö÷G&–çG2æBÆ6VÖVçBÂæBv†–6‚æÖW2F†R'V–ÆF–ærÂæòÆöævW"6÷fW'2ç—F†–ærBÆÂà¢F†R6Æ–×2&R6†V6¶VBF†R÷F†W"v’Föò(	BFö¶VâæÖ–æræò7V6‚7G'V7GW&RÂæò7V6‚†6RÀ¢÷"âGG&–'WFRF†B—2æ÷B6öæ¦V7GW&Âf–Ç2F†RvFRÂ6òâ÷fW"Ö6Æ–Ò—22Æ÷VB2và¢VçG&–W2VæFW"¢¥&W6öÇfVB¢¢&RW†V×Bg&öÒF†BÆ7B'VÆRÂv†–6‚—2v†BÆWG2âVæBÖöæÇ¢Fö7VÖVçB7W'f—fR—G2÷vâFF&V–ær6÷'&V7FVBâ¢¥F†R'VÆRæ÷r6÷fW'27FFVBf÷&Ò2vVÆÂ0¢G&vâvVöÖWG'’¢¢ƒ##bÓ‚Ó“¢F†R7V7Bfö6'VÆ'’—2WfW'’GFW7FVBfÇVR–â&V6÷&B(	@¢fö÷G&–çFÂ÷6—F–öæÂFö7VÖVçFVE÷&ævVÂF†R7G'V7GW&RÖÆWfVÂgVæ7F–öæöö67WçG6Âæ@¢f÷&ÒãÆGG#æVçVÖW&FVBg&öÒF†RFF&F†W"F†âg&öÒÆ—7BÂ6òæWr&6†WG—RGG&–'WFP¢—2–ç6–FRF†R'VÆRF†RF’—BV'2âv–FVæ–ær—Bf÷VæBf÷W"–çfVçF–öç2v—F‚æòFÖ—76–öâ(	@¢F†R6Vvæ6‚ƒ#’6&–âw2vÆÂ†V–v‡BæB&ööbG—RÂ&÷F‚Ä4T„ôÄDU"–âF†V—"÷vâæ÷FW2À¢æBvÆÆW'“¢fÇ6VöâF†Rw&VVâG&VRæBF†RvW7FW&âÂv†W&RfÇ6R—2F†R&6†WG—Rw0¢FVfVÇB&F†W"F†âf–æF–ærâFVâ6öæ¦V7GW&ÂfÇVW2ÂFVâFV6Æ&F–öç2â¢¥v†B—27F–ÆÀ¢VæVæf÷&6VB—2öÖ—76–öç2æB6–×Æ–f–6F–öç2¢¢ÂæBF†B—2F†R†&B†Æc¢â–çfVçF–öâ†2¢&V6÷&BFòö–çBBæBâöÖ—76–öâFöW2æ÷BÂ6òF†RvW7FW&âw2VæÖöFVÆÆVB7F&ÆR–&B„Ã¢æBF†Rw&VVâG&VRw26–FRFF—F–öç2„Ã’’&R6÷fW&VB'’&÷6RÆöæRâæòÖV6†æ—6Ò6â6F6‚¢Æ–&W'G’F¶VâF†Bæö&öG’æ÷F–6VBF¶–ærâ6—‚öb6—‚7G'V7GW&W26''’BÆV7BöæRÆ–&W'G’À¢6òF†R÷Ww2V×G’7FFR&VÖ–ç2VæW†W&6—6VB'’&VÂFFà£"â¢¥F†RöÖ—76–öâ†Æb—2Væf÷&6VBæ÷rFöòÂæB7v—F6†–ær—Böâf÷VæBFö7VÖVçFVBfVGW&P¢F†Bv2æWfW"'V–ÇBâ¢¢F†R–çfVçF–öâ'VÆR&VG26öæ¦V7GW&ÆFræBFVÖæG2à¢FÖ—76–öâââöÖ—76–öâÆVfW2æòFs¢Wf–FVæ6Rv—F‚æòvVöÖWG'’–âg&öçBöb—BÆöö·2W†7FÇ¢Æ–¶RWf–FVæ6Rv—F‚vVöÖWG'’–âg&öçBöb—BÂv†–6‚—2v‡’&÷6Rv2F†RöæÇ’F†–ær†öÆF–ær—@¢VçF–Âæ÷râF†R6Æ–ÒF†W&Vf÷&R6öÖW2g&öÒF†RvVæW&F÷"(	BV6‚¥÷&×2ç–FV6Æ&W2F†P¢f÷&ÒGG&–'WFW2—G2g&öÕ÷†6V7GVÆÇ’&VG2†4ôå5TÔTF’ÂæBWfW'’GG&–'WFR÷WG6–FP¢F†B6WB×W7B6’öâF†R&V6÷&Bv†BF†RÖW6‚FöW2–ç7FVC¢'6VçFÂ6–×Æ–f–VFÂ÷ ¢&V6÷&EööæÇ–f÷"6öÖWF†–ærF†Bv2æWfW"'V–ÆB–ç7G'V7F–öââF†Rf—'7BGvò÷vP¢Fö72ôÄ”$U%D”U2æÖF6÷fW'3¦Fö¶VâW†7FÇ’2â–çfVçF–öâFöW2ÂæBF†R÷WÖ&·0¢F†÷6R&÷w26òf—6—F÷"6VW2—BæBæ÷BöæÇ’F†R&W÷6—F÷'’â¢¥GvVçG’ÖöæRGG&–'WFW27&÷70¢6—‚'V–ÆF–æw2GW&æVB÷WBFò&V6‚æòfW'FW‚â¢¢Ö÷7B&R&Væ–vâÖ'WB×&VÂ6–×Æ–f–6F–öç2(	B¢6†–ÖæW’6÷VçBæò&6†WG—R&VG2ÂöæRv–æF÷r&‡—F†ÒöâÆÂF‡&VRg&ÖRFfW&ç2ÂvÆÂ7W&f6W0¢f—†VB'’F†R&6†WG—R&F†W"F†âF†R&V6÷&BâöæR—2æ÷Bâ¢¥F†RvöÆbö–çBFfW&âw2g&ÖP¢W‡FVç6–öâæB—G2–çFVBvöÆb6–vâ&R&÷F‚Fö7VÖVçFVFæB&÷F‚'6VçBg&öÒF†RÖöFVÂ¢£ ¢F†R&V6÷&B7VÆÇ2F†VÒg&ÖUöW‡FVç6–öææB6–vævVÂF†RÆöuöGvVÆÆ–æv&6†WG—R&VG0¢g&ÖUöFF—F–öææB6–væÂæBg&öÕ÷†6Vf–ÆÇ2â'6VçBGG&–'WFRv—F‚FVfVÇBÂ6ð¢F†RGvò&W7BÖGFW7FVBfVGW&W2öbF†R†÷W6RvW&RG&÷VB–â6–ÆVæ6RæBF†R÷W6†÷vVBF†P¢&ö¦V7Bw27G&öævW7B6öæf–FVæ6R6†—÷fW"&÷F‚âF†B—2F†R6öæf–FVæ6RÖöFVÂv÷&¶–ær0¢FW6–væVBæB7F–ÆÂÖ—6ÆVF–ærÂv†–6‚Ö¶W2—BF†R6†'W7B&wVÖVçBf÷"F†—2'VÆRF†BF†P¢&ö¦V7B†2&öGV6VBâ¢¥&W—&VB##bÓ‚ÓÂ–âöæR6Æ–6Rv—F‚—G2&¶R¢¢‡6VR‚&VÆ÷r’à¢Ö–ÆÆW"w2†÷W6Rv2F†R6ÖR6†R–âÖ–æ–GW&R(	B—G2&V6÷&B6—2Gvò6†–ÖæW—2æ@¢ÆöuöGvVÆÆ–æv'V–ÇBöæR(	BæB—2¢§&W—&VB##bÓ‚ÓÂ–âöæR6Æ–6Rv—F‚—G2&¶R¢ ¢‡6VR’&VÆ÷r’âv†B—27F–ÆÂVæVæf÷&6VB—2v†Bæò&V6÷&BÖVçF–öç2BÆÂ(	@¢F†RvW7FW&âw2VæÖöFVÆÆVB7F&ÆR–&B—2æ÷r6Æ–ÖVBÂ'WBÆ–&W'G’æö&öG’æ÷F–6VBF¶–æp¢&VÖ–ç2Væ6F6†&ÆR'’ç’ÖV6†æ—6Òà£2â¢¥F†RFö7VÖVçBæBF†RFF†BG&–gFVBÂæBw&—F–ærF†R6Æ–ÒF÷vâf÷VæB—Bâ¢¢Ã"7F–ÆÀ¢&VB'÷6—F–öâFvvVB–æfW'&VF"f÷"F†RvÆ¶W"ÖVWF–ær†÷W6S²F†R&V6÷&Bv2F÷væw&FVBFð¢6öæ¦V7GW&Æöâ##bÓ‚Ó’æBæ÷F†–ær6'&–VBF†R6†ævR&6²âF†R¶W—v÷&B'VÆRv0¢–æF–ffW&VçBFòF†RF—6w&VVÖVçB(	BF†RVçG'’6—2'Æ6VB"ÂF†RfÇVRv26öæ¦V7GW&ÂÂæBF†P¢ÖF6‚†VÆBf÷"&V6öâF†B†Bæ÷F†–ærFòFòv—F‚v†WF†W"F†RGvòw&VVBâFV6Æ&–ærF†P¢6Æ–Òf÷&6VBF†R6ö×&—6öââÃ"æ÷r6'&–W2&Wf—6VBÆ–æR6––ær6òÂæBF†R7FÆR6VçFVæ6P¢7F—3¢F†Rf–ÆR—2VæBÖöæÇ’ÂæB6–ÆVçFÇ’6÷'&V7FVBFÖ—76–öâ—2æ÷BöæRà£Râ¢¤d•„TB(	BF†R7FÆVæW72vFRW†—7FVB–âF†RFö7VÖVçFF–öâæBæ÷v†W&RVÇ6Râ¢¢tTåE2æÖF ¢†26–B6–æ6RF†R66fföÆBF†B&7FÆR6öÖÖ—GFVBtÄ"—26†V6²f–ÇW&RÂæ÷Bv&æ–ær"À¢æB76WG2öÖæ–fW7Bæ§6öæ†26'&–VBâ–çWG5÷6†#SfW"76WB6–æ6RF†Rf—'7B&¶Rà¢æ÷F†–ærWfW"&V6ö×WFVB—Bâ'Vå÷7FÆUö6†V6¶6¶VBöæÇ’v†WF†W"V6‚tÄ"V&VB–âF†P¢Öæ–fW7BÂ6ò&V6÷&B6÷VÆB&RVF—FVB–çFòF–ffW&VçB'V–ÆF–æræBF†RF÷vâv÷VÆB¶VW ¢&VæFW&–ærF†RöÆBöæRv—F‚F†RvFRw&VVâ(	BF†RW†7Bf–ÇW&RÖöFRF†R3R&W—'2&RVWVV@¢f÷"ÂVæwV&FVBâF†R6†V6²æ÷r&V6ö×WFW2WfW'’6öÖÖ—GFVB76WBw2–çWG2æBf–Ç2öà¢F—6w&VVÖVçBÂæBF†R&V6—RÆ—fW2v—F‚F†RvVæW&F÷'2†vVæW&F÷'2öÖW6…ö–çWG2ç–À¢FW'&–åövVâçFW'&–åö–çWG5÷6†’6òF†R6–FRF†Bw&—FW2F†R†6‚æBF†R6–FRF†B6†V6·0¢—B6ææ÷BG&–gBà¢¢¥7v—F6†–ær—Böâ&WV—&VB&VFVf–æ–ærF†R†6‚Â&V6W6RF†RöÆBöæRv2VçW6&ÆRâ¢¢—B†6†V@¢F†Rv†öÆR†6R&V6÷&BÇW2WfW'’ç–VæFW"vVæW&F÷'2öÂv†–6‚ÖVçBÆÂ6—‚'V–ÆF–æw0¢&VB7FÆRf÷"&V6öç2F†B6ææ÷BÖ÷fRfW'FWƒ¢F†RvVöÖWG'“¦FV6Æ&F–öç2FFVBöà¢##bÓ‚ÓÂæB4ôå5TÔTF6öç7FçBFFVBFòöæR&6†WG—Rw2&ÖWFW"ÖöGVÆR–çfÆ–FF–æp¢F†R÷F†W'2r'V–ÆF–æw2â†6‚F†B7&–W27FÆR÷fW"&Ww&—GFVâæ÷FRvWG2F—6&VÆ–WfVBÂæB¢F—6&VÆ–WfVBvFR—2v÷'6RF†âæöæRâ—Bæ÷r†6†W2v†BF†R'V–ÆFW"6â6VR(	BF†R§&W6öÇfVB ¢&ÖWFW'2ÂF†R6Æ72w2FW&—fVB&÷W'F–W2ÂF†R6öæf–FVæ6RfÆöG2ÂæBF†R'—FW2öbF†P¢'V–ÆFW"Â6öÖÖöâöÂ'V–ÆBç–æBF†R&ÆVæFW"–ââ&ÖWFW"ÖÖöGVÆR'—FW2&RFVÆ–&W&FVÇ¢÷WC¢F†BÖöGVÆRw2v†öÆRVffV7BöâF†RÖW6‚—2F†Rö&¦V7B—B&WGW&ç2ÂæBF†Rö&¦V7B—0¢†6†VB–âÖ÷&RFWF–ÂF†â—G26÷W&6Rv÷VÆBv—fRà¢¢¥F†RV–v‡B6öÖÖ—GFVB†6†W2vW&R&R×7F×VBv—F†÷WB&¶RÂæBF†B—26Æ–ÒÂ6ò†W&R—0¢F†R&ööbâ¢¢VæFW"F†RæWr&V6—RÂWfW'’–çWBFòÆÂ6—‚'V–ÆF–æw2—2'—FRÖ–FVçF–6ÂFòv†@¢—Bv2BF†RÆ7B&¶R†33“S6C&’(	B6†V6¶VB'’'Vææ–ærF†RæWr&V6—R–ç6–FRv÷&·G&VRö`¢F†B6öÖÖ—BæBF–ff–ærF†R–çWBFö7VÖVçG2Âæ÷B'’–ç7V7F–öââF†R6–ævÆRF–ffW&Væ6R—0¢'V–ÆBç–Âv†÷6RöæÇ’6†ævR–âF†—26Æ–6R—2FVÆVvF–ærF†R†6‚FòF†RæWrÖöGVÆRâFW'&–à¢&R×7F×VBf÷"F†R6ÖR&V6öã¢FW'&–åövVâç–†6†W2—G2÷vâ'—FW2æBv–æVBâW‡G&7FV@¢gVæ7F–öââæòÖW6‚v2&VvVæW&FVBæBæöæRæVVFVBFò&RâÖæ–fW7Bæ§6öææ÷r&V6÷&G0¢–çWG5÷66†VÖVÂæBF†RvFR&VgW6W2Öæ–fW7B7F×VBVæFW"66†VÖR—BFöW2æ÷B6ö×WFP¢&F†W"F†â6ö×&–ærGvò†6†W2F†BÖVâF–ffW&VçBF†–æw2à¢v†BF†—27F–ÆÂFöW2æ÷B6F6‚—27FFVB–âÖW6…ö–çWG2ç–¢—B6ö×&W2–çWG2Âæ÷B÷WGWBà¢7–6ÆW2ò—2æ÷B&—B×&W&öGV6–&ÆR7&÷72†&Gv&RÂv†–6‚—2v‡’g&W6†æW72—2FVf–æVBöâ–çWG0¢BÆÂ(	B†æBÖVF—FVBtÄ"&V†–æBâVçF÷V6†VB&V6÷&B76W2ÂæBæ÷F†–ær†W&R6â6VR—Bà£bâ¢¥F†Ræ–v‡FÇ’&¶RW6†W2—G2'&æ6‚æB6ææ÷B÷Vâ—G2"â¢¢6†–6vòÓFBÖ&¶Rç–ÖÆVæG0¢'’7&VF–ærVÆÂ&WVW7BæBF†B7FW†2&VVâf–Æ–æröâ&W÷6—F÷'’6WGF–ær(	@¢$v—D‡V"7F–öç2—2æ÷BW&Ö—GFVBFò7&VFR÷"&÷fRVÆÂ&WVW7G2"(	B6òWfW'’&¶R6–æ6P¢F†Rv÷&¶fÆ÷rv2w&—GFVâ†2ÆVgB—G2vVöÖWG'’öââ÷'†â7FWv&Bö&¶RÒ¦'&æ6‚F†@¢æ÷F†–ærÖW&vW2âV–v‡B7V6‚'&æ6†W2W†—7BâF†—26Æ–6Rv÷&¶VB&÷VæB—B'’fWF6†–ærF†R&¶P¢'&æ6‚æBf7BÖf÷'v&F–æröçFò—BÂv†–6‚—2f–æRf÷"âvVçBF†B—2vF6†–ærÂæBæòW6P¢BÆÂf÷"F†Ræ–v‡FÇ’âF†Rf—‚—2öæR6†V6¶&÷‚–âF†R&W÷6—F÷'’w27F–öç26WGF–æw2Â÷"¢BöâF†B7FW²F†Rv÷&¶fÆ÷rÆ—fW2÷WG6–FR6†–6vòóFBöæB—2F†W&Vf÷&R÷WG6–FRF†—0¢ÆæRw266÷RFòVF—BÂ6ò—B—2&V6÷&FVB†W&R&F†W"F†âf—†VBà£râ¢¤g&ÖR&FRf–wW&W2&RÖVæ–ævÆW72†W&Râ¢¢.(	3’g2VæFW"†VFÆW727v–gE6†FW"—26ögGv&P¢&7FW&—6F–öâÂæ÷BuRÖV7W&VÖVçBâG&r6ÆÇ2ƒ"’æBG&–ævÆW2ƒÃb’&R&VÂà £‚â¢¤d•„TB(	BF†RvöÆbö–çBFfW&â†2—G2g&ÖR†ÆbæB—G2vöÆb6–vââ¢¢F†RFVfV7BF†P¢öÖ—76–öâvFRf÷VæBöâ##bÓ‚Ó—2&W—&VBF†R6ÖRF’Â&V6÷&BæBÖW6‚–âöæR6öÖÖ—C ¢g&ÖUöW‡FVç6–öæ(i"g&ÖUöFF—F–öæÂ6–vævV(i"6–væÂF†RGvòæÖW2ÆöuöGvVÆÆ–æv ¢7GVÆÇ’&VG2âF†R'V–ÆF–ærF†BæÖVBvöÆbö–çBæ÷r†2&ö&B†æv–ær÷WG6–FR—Bà¢¢¥F†R&VæÖRv2F†R6ÖÆÆW"†Æbâ¢¢g&ÖUöFF—F–öã¢G'VVæBæ÷F†–ærVÇ6Rv÷VÆB†fRÆW@¢F†R&6†WG—R–6²F†R&’w26–FRÂv–GF‚ÂFWF‚æB7F÷&W’6÷VçBg&öÒ—G2FVfVÇG2(	B¢Gvò×7F÷&W’g&ÖR&Æö6²7&÷72F†R&—fW"g&öçBöbFfW&âF†R6÷W&6W2FW67&–&R2Æ÷r(	B6ò¢Fö7VÖVçFVBfVGW&Rv÷VÆB†fR'&—fVBBâ–çfVçFVB6—¦Rv—F‚æ÷F†–ærFÖ—GF–ær—BÂv†–6‚—0¢F†R6ÖRf–ÇW&RF†—2&W—"W†—7G2FòVæBÂöæRÆWfVÂF÷vââF†R&V6÷&BF†W&Vf÷&R7FFW2ÆÀ¢f÷W#¢6–FRVæFæBv–GF‚BÒöbF†R"Òg&öçFvRæBFWF‚rÒÆÂ¢¦6öæ¦V7GW&Â¢¢Â7F÷&W¢6÷VçB¢¦–æfW'&VB¢¢'’F†R6ÖR&wVÖVçBF†R7F÷&W’6÷VçB&÷fR—BW6W2âÃ#BFÖ—G2F†RF‡&VP¢6öæ¦V7GW&ÂöæW3²Ã#Ö÷fW2Fò&W6öÇfVB6''––ær&÷F‚7VÆÆ–æw2F†BæòÆöævW"&W6öÇfRÀ¢&V6W6R6–ÆVçFÇ’6÷'&V7FVBFÖ—76–öâ—2æ÷BöæRà¢¢¥v†BF†R6–vâ—3¢&Ææ²&ö&Bâ¢¢F†R'&6¶WBÂF†R&ÒÂF†R&ö&BæB—G2&÷÷'F–öç2&P¢F†R&6†WG—Rw2–çfVçF–öâÂæBF†R–çFVBvöÆb—2æ÷BG&vâ(	BæòFW67&—F–öâöb—B7W'f—fW2À¢æBvöÆb–çFVBg&öÒ–Öv–æF–öâv÷VÆB&RF†RÖ÷7B6öç7–7V÷W2–çfVçF–öâ–âF†R66VæRöà¢F†RöæRö&¦V7BWfW'’f—6—F÷"v–ÆÂvÆ²WFòâÃ#R6—26òà¢¢¥GvòÆ–Ö—G2v÷'F‚7FF–ærâ¢¢F†R6öæf–FVæ6RF–çBöâF†R&’föÆÆ÷w2v†BF†R&’•0¢†Fö7VÖVçFVBF†B—BW†—7FVBÂ–æfW'&VBF†B—Bv2Æ÷r’Âæ÷B—G2Væ¶æ÷vâ6—¦R(	BF†R'VÆR6W@¢f÷"F†R6Vvæ6‚Âv†–6‚ÖVç2F†RF–çBÆöæRv–ÆÂæ÷BFVÆÂf—6—F÷"F†Rv–GF‚—2wVW72æ@¢öæÇ’F†R÷Ww2Æ–&W'G’6†—v–ÆÂâæBF†Rv†öÆR&W—"&W7G2öâfö÷G&–çBF†B—2—G6VÆb¢Æ6V†öÆFW#¢BÒöbâ–çfVçFVB"Ò—2g&7F–öâöbwVW72à £’â¢¤d•„TB(	BF†R6†–ÖæW’6÷VçB—2çVÖ&W"F†R&6†WG—W2&VBÂæBF†RF†—&BÖ—77VÆÆ–ær—2æ÷p¢FW7Bâ¢¢WfW'’&V6÷&B7FFW26†–ÖæW—6²æV—F†W"&6†WG—R&VBF†RfÇVRâg&ÖU÷FfW&æ ¢'V–ÇBGvò7F6·2v†FWfW"F†R&V6÷&B6–BæBÆöuöGvVÆÆ–æv'V–ÇBöæRÂ6ò6×VVÂÖ–ÆÆW"w0¢†÷W6R(	B&V6÷&BGvòÂÖöFVÂöæR(	B7FööB7F6²6†÷'Bg&öÒ—G2f—'7B&¶Râ&÷F‚&6†WG—W2F¶P¢F†R6÷VçBæ÷râF†R—"öâg&ÖR&Æö6²¶VW2—G2W†7B÷6—F–öç2ƒã#"æBãs‚öbF†P¢g&öçFvRÂ&VBöfbF†R6Vvæ6‚FW–7F–öç2’6òF†B&ÖWFW&—6–ærF†RçVÖ&W"F–Bæ÷BV–WFÇ¢Ö÷fR'V–ÆF–ærv†÷6R6÷VçBv2Ç&VG’&–v‡C²Æör'V–ÆF–ærw26V6öæB7F6²vöW2öâF†Rg&ÖP¢FF—F–öâ&F†W"F†âF†Rf"v&ÆRÂ&V6W6R§F†R&V6÷&Bw2÷vâ&V6öâ¢f÷"6÷VçF–ærGvò—2&¢7F6²–âV6‚VÆVÖVçB"ÂæB†öæ÷W&–ærF†RçVÖ&W"v†–ÆR6öçG&F–7F–ær—G2&wVÖVçB—2æ÷@¢†öæ÷W&–ær—BâÃ#Ö÷fW2Fò&W6öÇfVBæBF†R6—‚&V6÷&G2G&÷F†RvVöÖWG'“¢w6–×Æ–f–VBv ¢FV6Æ&F–öâF†Bv2G'VRVçF–ÂF†—2ÆæFVBà¢¢¥F†RÆöuöGvVÆÆ–æv†Æbv2F†RvöÆbö–çBFVfV7BF†—&BF–ÖRâ¢¢F†R&ÖWFW"v0¢6†–ÖæW–Â&ööÆVã²æò&V6÷&B–âF†—2FF6WB†2WfW"6öçF–æVBF†Bv÷&BÂ6òg&öÕ÷†6V ¢Föö²—G2FVfVÇBöâWfW'’Æör'V–ÆF–æræBæ÷F†–ær6ö×Æ–æVBâF‡&VRö67W'&Væ6W2öböæP¢f–ÇW&R—2GFW&â&F†W"F†â&BÇV6²Â6ò—Bæ÷r†26†V6²–ç7FVBöbæ÷F†W ¢F—66÷fW&W#¢FW7Eö6öç7VÖVEöGG&–'WFW5ö7GVÆÇ•÷&V6…÷F†U÷&ÖWFW'6W'GW&'2WfW'’7FFV@¢fÇVR—G2&6†WG—RFV6Æ&W2—B4ôå5TÔU2æB&WV—&W2F†R&W6öÇfVB&ÖWFW'2Fò6†ævR(	BSP¢GG&–'WFW2W†W&6—6VB7&÷72F†R6—‚&V6÷&G2Âv—F‚&ÔW'&÷&6÷VçFVB2&VBÂ6–æ6P¢&VgW6–ærfÇVR—2F†RÆ÷VFW7B÷76–&ÆR&ööböb†f–ær6VVâ—BâF†R÷÷6—FRF—&V7F–öâ†à¢GG&–'WFR7FFVBæB¦æ÷B¢FV6Æ&VB’v2Ç&VG’F†RöÖ—76–öâvFS²F†—26Æ÷6W2F†RF—&V7F–öà¢v†W&RF†RFV6Æ&F–öâ—G6VÆb—2F†RfÇ6RöæRÂv†–6‚—2F†Rv÷'6RöbF†RGvòÂ&V6W6Rà¢GG&–'WFR–ç6–FR4ôå5TÔTB—2W†7W6VBg&öÒFÖ—GF–ærç—F†–ærà¢¢¥v†B—BFöW2æ÷Bf—‚ÂæBF†B—2F†RÖ÷&R–çFW&W7F–ær†Æbâ¢¢F†R6÷VçB—2–æfW'&VFöà¢WfW'’'V–ÆF–æræBæ÷F†–ærVÇ6R&÷WB7F6²—2&V6÷&FVBç—v†W&R(	Bæ÷BöæR6÷W&6RFW67&–&W0¢6†–ÖæW’öâç’öbF†W6R6—‚â÷6—F–öâÂv—'F‚Â†V–v‡B&÷fRF†R&–FvRæBÖFW&–Â&RÆÀ¢F†R&6†WG—Rw2Â6òF†R6öæf–FVæ6R6†—f—6—F÷"&VG2öâF†B&÷rw&FW2öæÇ’¦†÷rÖç’¢à¢Ã#b—2æWræB—2F†RöæÇ’Æ6RF†BF—7F–æ7F–öâ—2ÆVv–&ÆRà £#â¢¤d•„TB(	BÖ–ÆÆW"w2g&ÖR&ævR—2F–ÖVç6–öæVB'’F†R&V6÷&BÂæBf—†–ær—Bf÷VæBF†R7F÷&W—0¢öâF†Rw&öær†ÆböbF†R†÷W6Râ¢¢F†RVWVVBFVfV7Bv2Ã#Bw2öæR'V–ÆF–ær÷fW# ¢g&ÖUöFF—F–öæ—2Fö7VÖVçFVFöâÖ–ÆÆW%ö†÷W6V(	B&Gvò×7F÷'’†÷W6RFFVBFòF†R6&–âÀ¢g&öçF–ærF†R&—fW""(	BæBF†R&V6÷&B7FFVBæò6–FRÂæòv–GF‚ÂæòFWF‚æBæò7F÷&W’6÷VçBÀ¢6òÆöuöGvVÆÆ–æv7WÆ–VBÆÂf÷W"g&öÒ—G2FVfVÇG2â&W—&VB##bÓ‚ÓÂ&V6÷&BæBÖW6‚–à¢öæR6öÖÖ—BâGvòöbF†Rf÷W"GW&â÷WBFò&R¢¦GFW7FVB¢¢Âv†–6‚—2F†RF–ffW&Væ6R&WGvVVâF†—0¢'V–ÆF–æræBF†RvöÆbö–çB&“¢F†R6–FR—2g&öçF&V6W6RF†R6÷W&6R6—2¦g&öçF–ærF†P¢&—fW"¢ÂæBF†R&ævR—2Gvò7F÷&W—2&V6W6RF†R6÷W&6R6—2¦Gvò×7F÷'’†÷W6R¢âöæÇ’F†P¢v–GF‚æBFWF‚&R–çfVçFVBÂæBF†W’&R&VBöfbF†—2&V6÷&Bw2÷vâfö÷G&–çBöÇ–vöâ(	BF†P¢&—fW"Ög&öçF–ærÆ–Ö"—2’9rbÒ(	B&F†W"F†â–6¶VBg&W6‚Â6òF†RÖW6‚w&VW2v—F‚F†RÆà¢F†R&V6÷&BÇ&VG’G&w2âÃ#rFÖ—G2F†VÓ²F†W’–æ†W&—BF†RöÇ–vöâw2–çfVçF–öâÂv†–6‚—0¢F÷FÂà¢¢¥F†R7F÷&W’6÷VçBv2F†R&VÂFVfV7BæB—Bv2æ÷BöâF†RVWVRâ¢¢7F÷&–W6v2"À¢Fö7VÖVçFVFÂv—F‚—G2÷vâæ÷FR6––ær–â2Öç’v÷&G2F†BF†RGvò7F÷&W—2FW67&–&VBF†P¢&—fW"Ög&öçF–ær&ævRæBæ÷BF†Rv†öÆR'V–ÆF–ær(	B'WBÆöuöGvVÆÆ–æv&VG27F÷&–W62F†P¢Äôr4õ$Rw26÷VçBâ6òF†RFö7VÖVçFVB6Æ–Òv27VçBöâF†R6&–âÂF†R&ævRfVÆÂ&6²Fò¢BãrÒFVfVÇBÂæBF†RÖöFVÂ7FööBGvò×7F÷&W’Æör6&–â¢¦&V†–æB6†÷'FW"g&ÖR&Æö6²¢£ ¢F†R6ö×÷6—F–öâ–çfW'FVBÂ6VVâg&öÒF†RW†7B7÷B7&÷72F†RvFW"v†W&RF†Rƒ32FW67&—F–öà¢öb—Bv2w&—GFVââF†B—2F†Rg&ÖUöW‡FVç6–öæö6–vævVö6†–ÖæW–f–ÇW&R–â—G27V'FÆW ¢f÷&Ò(	Bæ÷BæÖRF†R&6†WG—R6÷VÆBæ÷Bf–æBÂ'WBæÖR—Bf÷VæBæB&VB2&V–ær&÷WB¢F–ffW&VçB†ÆböbF†R'V–ÆF–ærâæò7VÆÆ–ær6†V6²6F6†W2F†BÂæBæV—F†W"FöW0¢FW7Eö6öç7VÖVEöGG&–'WFW5ö7GVÆÇ•÷&V6…÷F†U÷&ÖWFW'6Âv†–6‚&÷fW2öæÇ’F†BfÇVRÖ÷fW0¢§6öÖWF†–ær¢âF†RGvò×7F÷&W’6Æ–Òæ÷r6—G2öâg&ÖUöFF—F–öå÷7F÷&–W6ÂF†R6&–âw27F÷&–W6 ¢—2–æfW'&VF†æò6÷W&6Rv—fW2F†RÆör'B†V–v‡C²F†Rƒ32f–Wrw2&Gvò×7F÷'’'V–ÆF–æp¢æBF¦ö–æ–ærÆör6&–â"öæÇ’&VG226öçG&7B–bF†R6&–âv2Æ÷vW"’ÂF†RRã"ÒÖ÷fW2Fð¢g&ÖUöFF—F–öåö†V–v‡EöÖÂæBvÆÅö†V–v‡EöÖ&V6öÖW2F†R6&–âw2"ãbÒ(	BF†RçVÖ&W"F†—0¢&V6÷&B†2æÖVBf÷"—B6–æ6R—Bv2w&—GFVâÂ6—GF–ær–âæ÷FR&F†W"F†â–âf–VÆBà¢Ã2Ö÷fW2Fò&W6öÇfVC¢æV—F†W"6ö×÷6—FR'V–ÆF–ær—26–ævÆRW‡G'W6–öâç’Ö÷&Rà¢¢¥v†BF–Bæ÷BvWB&WGFW"â¢¢F†R&6†WG—RÖ76W2F†Rfö÷G&–çBw2&÷VæF–ær&÷‚Â6òF†RÆöp¢6÷&R6öÖW2÷WBF†RgVÆÂ’Òv–FR&F†W"F†âF†RöÇ–vöâw2bÒæBF†R29rRÒ&RÖVçG&ç@¢6÷&æW"&V†–æBF†R&ævR—2f–ÆÆVB–ââ7FF–ærF†R&ævRw2÷vâçVÖ&W'2—2v†BÖ¶W2F†@¢f—6–&ÆR(	BF†RFVfVÇG2&öGV6VBâ–çfW'FVBÕBÖF6†–æræV—F†W"F†RöÇ–vöâæ÷"F†R6÷W&6W2(	@¢æBÃ#r&V6÷&G2—BâæBF†Rv†öÆR&W—"7F–ÆÂ&W7G2öâÆ6V†öÆFW#¢’9rböbâ–çfVçFV@¢’9rà £#â¢¥F†Rf—'7B'&–FvRÂæBF†Rf—'7B&V6÷&Bv†÷6R6—¦R—2æ÷BÆ6V†öÆFW"â¢¢F†Ræ÷'F‚'&æ6€¢7&÷76–ærB¶–ç¦–R7G&VWB(	B6†–6vòw2f—'7B'&–FvRÂ'V–ÇBƒ3"Â&WÆ6VBƒ3’(	B—2æ÷r¢&V6÷&BÂ&¶RæBV&Æ—6†VBÖW6‚ÂöâF†R'&–FvU÷F–Ö&W&&6†WG—RF†B†B&VVâw&—GFVà¢æBæWfW"W6VBâGvòöb—G2çVÖ&W'2&RWf–FVæ6R&F†W"F†â–çfVçF–öâÂv†–6‚—2æWr†W&S ¢¢§FVâfVWBv–FR¢¢—26†&ÆW26ÆVfW"w2Â&V6ÆÆVB–âF†R¤6†–6vòG&–'VæR¢öb#’ö7Bƒ“2'’¢Öâv†ò†BG&—fVâFVÒ7&÷72—BÂæBF†R¢£sãƒ2Ò7â¢¢—2ÖV7W&VB&WGvVVâF†RGvð¢G&6VBƒ3BvFW&Æ–æW2ÆöærF†R¶–ç¦–RÆ–væÖVçB&F†W"F†â6†÷6Vâ(	B—Bw&VW2v—F‚F†P¢&V6‚w2G&gFVBÖVâv–GF‚Fò&÷WBÖWG&RÂv†–6‚—2F†R6†V6²F†B—B&VG2F†RÖBF†—0¢7FF–öâ–ç7FVBöbfW&v–ær—BâF‡&VR6÷W&6R&V6÷&G2vW&RFFVBÂÆÂF‡&VRv—F‚v–&6°¢6æ6†÷G2à¢¢¥v†B—2–çfVçFVB—2F†RÖ–FFÆRöbF†R'&–FvRÂæB—B—2F†RÖ÷7B6öç7–7V÷W2F†–ær–â—Bâ¢ ¢6ÆVfW"FW67&–&W2F†RVæG2(	B'F†R'WFÖVçG2vW&R'V–ÇBöb†Vg’Æöw2–âF†R6†ÆÆ÷rvFW"æV ¢F†R&æ·2"(	BæBæö&öG’FW67&–&W2v†B7FööB&WGvVVâF†VÒâ6öÖWF†–ær†BFò6''’sãƒ2Òö`¢Æör7G&–ævW"Â6òF†R&6†WG—Rw2FVfVÇBBãRÒ76–ærWG2¢¦f–gFVVâ7&–'2–âF†R&—fW"¢¢Â¢&VwVÆ"6öÆöææFRf—6—F÷"v–ÆÂ&VB2f7B&÷WBF†R'&–FvRâ—B—2f7B&÷WBF†P¢&6†WG—RâÃ#’FÖ—G2—BÂæBF†R6öæf–FVæ6RF–çB6ææ÷C¢F†RF–çBw&FW2v†B7&–"¦—2¢À¢æ÷B†÷rÖç’F†W&RvW&RâF†R7â—BF—f–FW2—2—G6VÆbF†RG&vâvFW&Æ–æR×Fò×vFW&Æ–æP¢F—7Fæ6RÂæBF†R'WFÖVçG27FööB–ç6–FRF†BÆ–æR'’âVç&V6÷&FVBÖ÷VçBà¢¢¥Gvò6÷W&6W26öçG&F–7BV6‚÷F†W"&÷WBF†RF†–æræB&÷F‚&R¶WBâ¢¢æG&V2†2—@¢&f÷&ÖVBöb7G&–ævW'2æBöæÇ’f—GFVBf÷"fö÷B76VævW'2"æB'W6VÆW72f÷"FV×2"2ÆFR0¢F†R7VÖÖW"öbƒ33²6ÆVfW"&VÖVÖ&W&VBG&—f–ær7&÷72—BÂæBöâ‚Vrƒ3R&ö6W76–öâö`¢‡VæG&VG27&÷76VB—Bâ—Bv2&V'V–ÇB÷"v–FVæVB–â&WGvVVâæBæ÷F†–ær&V6†VB6—2v†Vâ÷ ¢†÷râF†R&V6÷&BF¶W2F†Rƒ3R&VF–ær(	Bf÷W"7G&–ævW'2ÂgVÆÂ×v–GF‚FV6²(	BæB6—2öâ—G0¢÷vâf6RF†Bâƒ3266VæRv÷VÆBvçBF†R÷F†W"öæRà¢¢¤6÷'&V7F–öâFòF†—2&ö¦V7Bw2÷vâF÷76–W"6ÖR÷WBöbw&—F–ær—Bâ¢ ¢Fö72÷&W6V&6‚ó2×7G'V7GW&W2Öæ÷'F‚æÖF*sRFw2&÷F‚&&÷WBgBv–FR"æB&6ÆV&–ærF†RvFW ¢'’&÷WBbgB"2Fö7VÖVçFVBâöæÇ’F†Rv–GF‚7W'f—fW3¢F†RvW26''––ærF†Rv–GF‚ÂF†P¢'WFÖVçG2ÂF†R7G&–ævW'2ÂF†Rƒ3"FFRæBF†Rƒ3’&WÆ6VÖVçB6’æ÷F†–ær&÷WB†V–v‡@¢&÷fRF†RvFW"ÂæBF—&V7B6V&6‚öbF†R6ÖR†÷7Bf÷"F†R‡&6–ær&WGW&ç2æ÷F†–ærâF†P¢f–wW&R—2¶WBÂ6ÆV&æ6UöÖ—2FvvVB–æfW'&VFÂæB'&–FvU÷F–Ö&W%÷&×2ç–w2Fö77G&–æp¢—26÷'&V7FVB6òF†R6öç7FçBw2æÖR7F÷276W'F–ærv†B—B6ææ÷B6†÷rà¢¢¥F†R6öçG&7Bw2vFW"Öæ6†÷"'VÆR—2v—&VB&F†W"F†âw&—GFVââ¢¢Fö72ôtÄ"Ô4ôåE$5BæÖF†0¢6–B6–æ6RF†R&6†WG—Rv2G&gFVBF†B7G'V7GW&R÷fW"vFW"æ6†÷'2’ÒBF†RFW6–và¢vFW"7W&f6RæBF†BF†R&VæFW&W"×W7BÆ6R—Bv–ç7BF†RvFW"ÆæS²æ÷F†–ær–×ÆVÖVçFV@¢—BÂæBæ÷F†–æræVVFVBFòVçF–ÂF†W&Rv2'&–FvRâF†R&6†WG—RFV6Æ&W2dU%D”4Åôä4„õ&À¢6ö×–ÆU÷66VæRç–6÷–W2—BFòÆ6VÖVçBçfW'F–6Åöæ6†÷&ÂæBF†R&VæFW&W"Æ6W2vFW& ¢BÆ—FW&Â¦W&ò(	BF†BÆæR—2¦W&ò'’F†RFVf–æ—F–öâöbF†RfW'F–6ÂFGVÒâF†R6Öö¶P¢76W'G2F†R¢¦F–ffW&Væ6R¢¢&WGvVVâF†RGvòæ6†÷'2Âæ÷B’ÓÓÒ¢÷fW"G'’ÆæBF†W’w&VRÀ¢6òFW7BF†B76VBF†W&Rv÷VÆB&÷fRæ÷F†–ærà¢¢¥w&—F–ærF†B76W'F–öâf÷VæBGvòF†–æw2F†R6öFRv2&–v‡B&÷WBæBF†RFW67&—F–öâv0¢æ÷Bâ¢¢f—'7BÂ6×Æ–ærBF†R&V6÷&Bw2Æ6VÖVçB÷&–v–â&÷fW2æ÷F†–ærV—F†W#¢F†B÷&–v–â—0¢F†RöÇ–vöâw2ƒÂ’Âf÷"F†—2'&–FvRF†RvW7BVæBÂv†–6‚6—G2W†7FÇ’öâF†RG&6VBvFW&Æ–æP¢v†W&RF†Rw&÷VæB7&÷76W2¦W&ò(	B¦W&òv–ç7B¦W&òÂæBF†R6†V6²76W2v†FWfW"F†R&VæFW&W ¢FöW2â—B6×ÆW2F†RFV6²w2Ö–Gö–çBæ÷râ6V6öæBÂF†Rf–ÇW&RÖöFR—2F†R÷÷6—FRöbF†P¢ö'f–÷W2öæRâFW'&–âæ†V–v‡B‚–FöW2æ÷B&W÷'BF†R6†ææVÂ&VB÷fW"vFW#²—B&W÷'G2¢¢§vF–ær&'&–W"B³BÒ¢¢ÂWBF†W&RFò7F÷F†RvÆ¶W"7G&öÆÆ–ær–çFòF†R&—fW"â'&–FvP¢ÆVgBöâF†RFW'&–âæ6†÷"F†W&Vf÷&RFöW2æ÷B6–æ²÷WBöb6–v‡B(	B—B†æw2f÷W"ÖWG&W2&÷fP¢F†RvFW"Âv†–6‚—2F†R†&FW"f–ÇW&RFò&VBÂæB—B—2v†BF†R6Öö¶Ræ÷r–ç2à¢¢¥–÷R6ææ÷BvÆ²7&÷72—BÂæBF†B—27FFVB&F†W"F†âf¶VBâ¢¢F†RvÆ¶W"föÆÆ÷w2F†P¢FW'&–âÂ6òF†RFV6²—266VæW'’–÷R72VæFW"&F†W"F†â&÷WFS²—G2fö÷G&–çB—2W†6ÇVFV@¢g&öÒF†R6öÆÆ—6–öâöÇ–vöç2Â&V6W6RG&VF–ærFV6²2vÆÂv÷VÆBWBâ–çf—6–&ÆR&'&–W ¢7&÷72F†R&—fW"v—F‚æ÷F†–ærf—6–&ÆRB†VB†V–v‡BFòW‡Æ–â—BâvÆ¶&ÆRFV6²æVVG2F†P¢vÆ¶W"FòÆV&â&÷WB7W&f6W2&÷fRF†Rw&÷VæBÂv†–6‚—2—G2÷vâVæ—Böbv÷&²à £#"â¢¥F†R'&–FvR'&—fW2æ÷v†W&RÂæBF†RvFRF†B6—26ò—2æWrâ¢¢F‡&VR'VÆW2æ÷r6°¢v†WF†W"&V6÷&B—2†öæW7C¢F†R6öæf–FVæ6RÖöFVÂw&FW2v†BfÇVR6Æ–×2ÂF†RÆ–&W'F–W0¢6÷fW&vR6†V6²FVÖæG2âFÖ—76–öâf÷"ç—F†–ær–çfVçFVBÂæBF†RvVöÖWG'’FV6Æ&F–öç0¢FVÖæBöæRf÷"ç—F†–ær7FFVBæBæ÷B'V–ÇBâæöæRöbF†VÒ6â6VR7G'V7GW&RF†Bv0¢'V–ÇBf—F†gVÆÇ’öçFòw&÷VæBF†B—2æ÷BVæFW&æVF‚—BÂ&V6W6R¢¦æ÷F†–ær–âF†R&V6÷&B—0¢w&öær¢¢âWfW'’æÖR&W6öÇfW2ÂWfW'’fÇVR&V6†W2fW'FW‚ÂWfW'’6öæf–FVæ6R6†——2V&æVBÀ¢æBF†Ræ÷'F‚'&æ6‚'&–FvR7F–ÆÂ7FæG2"ãC"Ò6ÆV"öbF†RFW'&–âB&÷F‚ÆæF–æw2à¢6†V6µöw&÷VæEö6öçF7F6Æ÷6W2F†BF—&V7F–öââV6‚&6†WG—RFV6Æ&W2v†W&R—BF÷V6†W2F†P¢w&÷VæB(	BW&–ÖWFW&f÷"'V–ÆF–ær‡F†Rfö÷G&–çB÷WFÆ–æRÂBF†R&6RöbF†RvÆÇ2’æ@¢VæG6f÷"7&÷76–ær‡F†RGvòVæBVFvW2ÂBFV6²†V–v‡B’(	BæBfÆ–FFRç–ÖV7W&W2F†@¢÷WFÆ–æRv–ç7BF†R6öÖÖ—GFVB†V–v‡Ff–VÆBF‡&÷Vv‚FööÇ2ö†V–v‡Ff–VÆBç–â¢¥F†RFöÆW&æ6R—0¢æ÷BæWrçVÖ&W#¢—B—2F†RvÆ¶W"w2ã3RÒ7FW×W'VÆR¢¢Â&V6W6RF†RVW7F–öâF†RvFP¢6·2—2Æ—FW&ÆÇ’F†RvÆ¶W"w2VW7F–öâÂæB7G'V7GW&Rf—6—F÷"6÷VÆBæ÷B7FWöçFò†0¢æ÷BÖWBF†Rw&÷VæBà¢¢¥v†B—Bf÷VæB—2F†RöæÇ’F†–ær—Bf÷VæBÂæBF†B—2v÷'F‚7FF–ærFöòâ¢¢F†R6—€¢'V–ÆF–æw2ÆæC¢F†V—"v÷'7B6÷&æW"6—G2ãbÒöfb‡F†RvöÆbö–çBFfW&âÂ÷fW"F†R&æ°¢fÆÂ’ÂvVÆÂ–ç6–FR7FWâF†R'&–FvRFöW2æ÷BÂæB6ææ÷Bv—F‚F†RFF2—B7FæG2(	BF†P¢FV6²6—G2B"ã#"Ò„6ÆVfW"w2–æfW'&VB6—‚Öfö÷B6ÆV&æ6RÇW2F†R7G&–ævW"æBÆæ²FWF€¢VæFW"—B’æBF†R†–v†W7BÆæBç—v†W&R–âF†RcCÒ&÷‚—2ã3ÒÂ6òF†W&R—2æòw&÷VæB–à¢F†—2Wö6‚f÷"—BFò'&—fRBâF†R&V6÷&BFV6Æ&W2w&÷VæEö6öçF7C¢&ö6…öæ÷EöÖöFVÆÆVF ¢æBÃ3FÖ—G2—C²F†R÷W6†÷w2F†R6†—öâF†R'V–ÆF–ær&V–ær–ç7V7FVBÂ6òF†P¢FÖ—76–öâ&V6†W2f—6—F÷"æBæ÷BöæÇ’&Wf–WvW"à¢¢¥F†R&ö6‚—2æ÷BÖöFVÆÆVB&V6W6Ræ÷F†–ærFW67&–&W2öæRâ¢¢æG&V2v—fW2F†R7G&–ævW'2À¢6ÆVfW"v—fW2F†Rv–GF‚æBF†RÆör'WFÖVçG2&–âF†R6†ÆÆ÷rvFW"æV"F†R&æ·2"ÂæBæð¢6÷W&6R&V6†VB6—2†÷rW'6öâ÷"FVÒv÷Bg&öÒF†R&æ²öçFòF†RFV6²ââVÖ&æ¶ÖVç@¢v÷VÆB&R6V6öæB–çfVçF–öâ7F6¶VBöâF†R6ÆV&æ6Rf–wW&R(	Bv†–6‚—2—G6VÆböæÇ¢–æfW'&VFæBVç6÷W&6VB–âF†RF÷76–W"F†B7WÆ–VB—B(	BæBVæÆ–¶RÃ#’w2f–gFVVâ7&–'2—@¢—2F†R–çfVçF–öâf—6—F÷"v÷VÆBvÆ²÷fW"&F†W"F†âÆöö²Bà¢¢¤6ÖÆÆW"F†–ær6ÖR÷WBöbw&—F–ær—BÂæB—B—2v&æ–ær&÷WBF†R7FÆVæW72†6‚â¢ ¢F†R6öçF7B†V–v‡Bv2f—'7Bw&—GFVâ2&÷W'G–öâ'&–FvUF–Ö&W%&×6Âæ@¢ÖW6…ö–çWG2ç–†6†W2WfW'’&÷W'G’&ÖWFW"6Æ72FW&—fW2(	B6òçVÖ&W"æò'V–ÆFW ¢&VG2–ÖÖVF–FVÇ’&R×7FÆVBF†R'&–FvRâF†B—2W†7FÇ’F†RfÇ6R÷6—F—fR*rR&Ww&÷FRF†P¢†6‚FòVæBÂ'&—f–ærg&öÒæWrF—&V7F–öã¢F†R'VÆR&FW&—fVB&÷W'G’—2ÖW6‚–çWB"—0¢&–v‡B&÷WB6öç7FçG2æBw&öær&÷WB66W76÷'2â—B—2ÖöGVÆRÖÆWfVÀ¢w&÷VæEö6öçF7E÷¢‡&×2––ç7FVBÂæBF†RFö77G&–ær6—2v‡’6òF†RæW‡BöæRFöW2æ÷@¢&VF—66÷fW"—Bà¢¢¥v†B—B7F–ÆÂ6ææ÷B6VR¢¢—27G'V7GW&R7FæF–æröâw&÷VæBF†BW†—7G2æB—2w&öær(	@¢F†R6†V6²6ö×&W2ÖW6‚v–ç7BF†R†V–v‡Ff–VÆBÂæB&÷F‚6âw&VRöâ7W&f6Ræð¢6÷W&6R7W÷'G2à £#2â¢¤f÷W"GG&–'WFW2öbF†R'&–FvR&Ræ÷r&V†–æBF†V—"Wf–FVæ6RÂæBF†RWf–FVæ6Rv2¢fö÷Fæ÷FRVæFW"&w&‚F†—2&ö¦V7B†2V÷FVBf÷"vVV·2â¢¢F†R&V6÷&Bw2÷vâÖVÖòÆ—7FV@¢f÷W"÷VâF‡&VG2öâ##bÓ‚Ó²GvòvW&RVÆÆVBF†R6ÖRF’æBöæRöbF†VÒ–Bf÷ ¢WfW'—F†–ærâ¢¤æG&V2&–çG2ÂBF†Rfö÷Böbâc3Óc3"Â7FFVÖVçB6–væVB'’f÷W"ÖVâv†ð¢W6VBF†R'&æ6‚'&–FvW2¢¢(	B¢âBâ6FöâÂ¦ö†â&FW2Â6†&ÆW26ÆVfW"æB¦ö†âæö&ÆRÂw&VV@¢BÖVWF–æröböÆB6WGFÆW'2ÆFR–âF†RfÆÂöbƒƒ2æB†æFVBFòF†RVF—F÷'2'’&FW2à¢—B—2F†RöæÇ’FW67&—F–öâç–&öG’w&÷FRöb†÷rF†W6R7&÷76–æw2vW&RWBFövWF†W# ¢'WFÖVçG2öbÆöw2–âF†R6†ÆÆ÷rvFW"æV"F†R&æ·2Â¢§Gvò&&VçG2"öbf÷W"†Vg’Æöw0¢&W7F–æröâF†R&÷GFöÒ–âFVWW"vFW"¢¢Â7G&–ævW'2öb†Vg’Æöw2g&öÒF†R'WFÖVçG2FòF†P¢&VçG2æB&WGvVVâF†VÒÂ¢§Væ6†Vöç2÷"7Æ—BÆöw2f÷"fÆö÷"¢¢Â&÷WBFVâfVWBv–FRÀ¢¢§v—F†÷WB&–Æ–æw2f÷"F†Rf—'7BfWr–V'2ÂgFW"v†–6‚wV&G2÷"&–Æ–æw2vW&RFFVB¢¢Âæ@¢¢¦&÷WB6—‚fVWB&÷fRF†RvFW"Â'6òF†BFV×276VBVæFW"F†VÒöâF†R–6Rg&VVÇ’â"¢ ¢6÷W&6R&V6÷&C¢öÆE÷6WGFÆW'5ö'&–FvW5óƒƒ6ÂF–W""à¢¢¥v†B—B6÷'&V7G2ÂæBæöæRöb—B—26÷'&V7FVB–WBâ¢¢–W%÷76–æuöÖWG2f–gFVVâ7&–'2–à¢F†R&—fW"öâF†R&6†WG—Rw2FVfVÇC²F†RÆWGFW"6—2Gvò&VçG2â–W%ö¶–æF—27&–&Âæ@¢F†—2&V6÷&B&wVVB—G2v’F†W&R'’G&VF–ærF†R¶–ç¦–R7G&VWBvRw2G—R×v÷&B$&VçB"0¢ÖöFW&âVF—F÷&–Â6Æ76–f–6F–öâ(	B—B—2F†R6WGFÆW'2r÷vâv÷&BÂæB6ÆVfW"ÂF†RW–Wv—FæW70¢F†B&wVÖVçBÆVæVBöâÂ6–væVB—Bâ6ÆV&æ6UöÖv2FVÖ÷FVBFò–æfW'&VF†W&Rf÷"vçBö`¢vS²F†RvRW†—7G2ÂæBF†RF÷76–W"w2´Dô5ÖFrv2&–v‡BâF†RFV6²—2F†R&6†WG—Rw0¢æBF†RÆWGFW"7FFW2—Bâ¢¤WfW'’öæRöbF†÷6R—2ÖW6‚–çWB¢¢Â6òF†R&V6÷&B6ææ÷BÖ÷fP¢v—F†÷WBF†RtÄ"Ö÷f–ærv—F‚—BÂæBF†—26öÖÖ—BFVÆ–&W&FVÇ’6†ævW2æòfÇVRæBæð¢6öæf–FVæ6RFs¢—BÆæG2F†R6÷W&6RÂF†RÖVÖòÂF†RÆ–&W'F–W2WFFW2æBF†Ræ÷FW2F†B6¢öâV6‚GG&–'WFRw2÷vâf6RF†B—B—2&V†–æB—G2Wf–FVæ6Râ¢¥F†R&W—"æB—G2&¶R&P¢öæR6Æ–6RæB—B—2F†RæW‡BöæRâ¢¢„—Bv2ÂæB—BÆæFVBF†R6ÖRF’(	B*r#Bâ¢¢¥F†Rv÷&²÷&FW"¢¢Â6òF†RæW‡B6Æ–6RFöW2æ÷B†fRFò&RÖFW&—fR—C¢'&–FvU÷F–Ö&W&'V–ÆG0¢–çFW&ÖVF–FR7W÷'G2g&öÒ76–ærÂæBF†RWf–FVæ6R—26÷VçBæBf÷&ÒÂæ÷B76–ær(	@¢Gvò&VçG2BF†RF†—&G2öbsãƒ2Ò7â—2F–ffW&VçB&ÖWFW&—6F–öâÂæ÷BF–ffW&Vç@¢çVÖ&W"Â6òF†R&6†WG—R6†ævW2&Vf÷&RF†R&V6÷&BFöW2â–W%ö¶–æFvçG2&VçFfÇVP¢†f÷W"†Vg’Æöw27FæF–æröâF†R&÷GFöÒ’&W6–FR7&–&â6ÆV&æ6UöÖÖ÷fW2FòFö7VÖVçFVF ¢v—F‚F†—26÷W&6Râ&–Æ–æv7F—2fÇ6VæB—G2æ÷FR6†ævW2g&öÒâ&wVÖVçBg&öÒ6–ÆVæ6P¢Fò&VF–æröb'F†Rf—'7BfWr–V'2"âÃ#’Ö÷fW2Fò¢¥&W6öÇfVB¢¢v†VâF†RÖW6‚6†÷w2Gvð¢7W÷'G2ÂæBæ÷B&Vf÷&Rà¢¢¥GvòæVvF—fRf–æF–æw26ÖRv—F‚—BÂæBF†W’6÷7B2×V6‚FòW7F&Æ—6‚2F†R÷6—F—fP¢öæRâ¢¢æV—F†W"ƒ3B6†VWBG&w2F†—2'&–FvRâ&÷F‚vW&R–ç7V7FVBBF†R7&÷76–ærw2÷vâf—GFV@¢—†VÂ&F†W"F†â'’W–R(	B–çfW'BV6‚6†VWBw26öÖÖ—GFVBt5ff–æRBF†R&V6÷&Bw2FV6²Æ–æRÀ¢fWF6‚F†B”””b&Vv–öâ(	BæBöâ&÷F‚ÂF†R7G&VWB7F÷2BF†RvFW&Æ–æS¢ÆGFVB7G&VWB—2¢FVF–6F–öâÂæ÷B7G'V7GW&RâF†RF‡&VBF†RÖVÖò&FVBÖ÷7B&öÖ—6–ærÂ'F†Rƒ3Bóƒ3Rv&ç6–¢æB¶–ç¦–Rw2FF—F–öâÆB"ÂGW&ç2÷WBFò&R†F†v•óƒ3FÂ6†VWBÇ&VG’–âF†—2FF6W@¢æBÇ&VG’vV÷&VfW&Væ6VBÂv†–6‚—2—G2÷vâ6ÖÆÂÆW76öâ&÷WB÷Vâ×F‡&VBÆ—7G2âæBöà¢†F†v’†F6†VBÂÆFFW"ÖÆ–¶RÖ&²6—G2–âF†R6†ææVÂv—F†–â3RÒöbF†R7&÷76–æræB&VG0¢6öçf–æ6–ævÇ’2Ææ²ÖæB×7G&–ævW"'&–FvR7–Ö&öÂBÖöFW&FR¦ööÓ²BgVÆÂ&W6öÇWF–öâ—B—0¢F†RÆWGFW"¢¤‚¢¢öb$%$ä4‚"ÂÆWGFW&VBF÷vâF†RvFW"â—B—2w&—GFVâF÷vâ†W&R6òF†B—B—0¢f÷VæBöæ6R&F†W"F†âF—66÷fW&VBGv–6Rà £#Bâ¢¤d•„TB(	BGvò&VçG2Âæ÷Bf–gFVVâ7&–'2ÂæBF†R&W—"6†ævVB&ÖWFW"&F†W"F†â¢çVÖ&W"â¢¢*r#2w2v÷&²÷&FW"ÆæFVBF†R6ÖRF’—Bv2w&—GFVâÂ&V6÷&BæB&6†WG—RæB&¶P¢–âöæR6öÖÖ—Bâ–W%÷76–æuöÖ—2vöæRg&öÒ'&–FvU÷F–Ö&W&æBg&öÒF†R&V6÷&C°¢–W%ö6÷VçC¢&†Fö7VÖVçFVF’&WÆ6W2—BÂ–W%ö¶–æF—2&VçFÂ6ÆV&æ6UöÖ—2&öÖ÷FV@¢FòFö7VÖVçFVFöâF†Rƒƒ27FFVÖVçBÂæBF†RfÆö÷"F†R&6†WG—R†B&VVâ7WÇ––ær–à¢6–ÆVæ6R—27FFVB2FV6µö¶–æC¢Væ6†VöæâF†R&—fW"6'&–W2F‡&VR7ç2v†W&R—B6'&–V@¢6—‡FVVâà¢¢¥F†R&ÖWFW"v2F†RfVÇBÂæ÷BF†RfÇVRâ¢¢â&6†WG—RF†BF—f–FW27â'’76–æp¢6âöæÇ’WfW"&öGV6R6öÆöææFRÂæB76–ær—2'V–ÆFW"w26öçfVæ–Væ6RF†Bæòv—FæW70¢v÷VÆBWfW"&V6÷&Bâv†BÖâv†òG&÷fRFVÒ7&÷72'&–FvR&VÖVÖ&W'2—2¦†÷rÖç’¢7Föö@¢–âF†RvFW"æB§v†BF†W’vW&RÖFRöb¢(	B6òF†R–çWB—2æ÷r6÷VçBæBf÷&ÒÂæBF†P¢76–ær7W'f—fW2öæÇ’2”U%õ54”äuôdÄÄ$4µôÖÂF†RF†–ær'&–FvRfÆÇ2&6²Fòv†Và¢æö&öG’FW67&–&VB—G2Ö–FFÆRâ6†æv–ærBãRFò#2ã“Bv÷VÆB†fRf—†VBF†—2'&–FvRæBÆVgBF†P¢æW‡BöæRFò&Rf÷VæB'’F†R6ÖR66–FVçBà¢¢¥v†BF†R6öæf–FVæ6Rf–Wræ÷r6—2ÂæB—B6—2Ö÷&RF†â—BF–Bâ¢¢6ÆV&æ6UöÖ—2öæRö`¢F†RGG&–'WFW2F†B6—2v†BF†—27G'V7GW&Rt2†'&–FvRw2Fö7VÖVçFVBFW67&—F–öâ¦—2 ¢F–ÖVç6–öæÂ(	B6VR'&–FvU÷F–Ö&W%÷&×6’Â6ò&öÖ÷F–ær—BF¶W2F†RFV6²æBF†R7G&–ævW'0¢÷WBöbF†R†ÆbÖF—F†W&VB7FFRF†R–æfW'&VFFrWBF†VÒ–âÂæBF†R&VçG26öÖR÷WB6öÆ–@¢&V6W6R&÷F‚F†V—"6÷VçBæBF†V—"f÷&Ò&RGFW7FVBâF†B—2F†Rf—'7BF–ÖR–âF†—2FF6W@¢F†BWf–FVæ6R†2ÖFR6öÖWF†–ær¦ÆW72¢F—F†W&VBà¢¢¤æBv†B—B7F–ÆÂ6ææ÷B6’—2v†W&RF†W’7FööBâ¢¢F†RÆWGFW"Æö6FW2F†R&VçG2'’FWF‚(	@¢'&W7F–æröâF†R&÷GFöÒÂ–âFVWW"vFW""(	Bv†–6‚—2Æö6F÷"F†—2&ö¦V7B6ææ÷BW6S¢æð¢6÷W&6Rv—fW2F†R6†ææVÂw2&VB&öf–ÆRæBæ÷F†–ær&VÆ÷rF†RvFW&Æ–æR—2ÖöFVÆÆVBâF†W’&P¢'V–ÇBBF†RF†—&Bö–çG2&V6W6RF†B—2v†B'V–ÆFW"v÷VÆBFòv—F‚F‡&VR&÷Vv†Ç’WVÀ¢'Vç2â6òF†R6†—öâ–W%ö6÷VçFw&FW2†÷rÖç’æBf—6—F÷"6VW2W†7FÇ’v†W&RÂv†–6‚—0¢F†R6†–ÖæW—66—GVF–öâöb*r’'&—f–ærBF–ffW&VçB7G'V7GW&Râ¢¤Ã3¢¢—2v†W&R—B—0¢FÖ—GFVBÂæB—B6'&–W26V6öæBöÖ—76–öâF†R&W—"7&VFVC¢F‡&VR7ç2Ö¶RV6‚7G&–ævW ¢'Vâ#2ã’ÒÂÆöævW"F†âç’F–Ö&W"ç–&öG’v2Ö÷f–ærÂ6òF†÷6R'Vç2vW&R7Æ–6VB6öÖWv†W&P¢æBæ÷F†–ær6—2v†W&RâF†RÖW6‚6†÷w2öæRÆörW"&’â¢¤Ã#’Ö÷fW2Fò&W6öÇfVB¢¢(	BæBöæÇ¢æ÷rÂ&V6W6RF†RVçG'’—G6VÆb6–B—Bv÷VÆB7F’VçF–ÂF†RÖW6‚6†÷vVBGvò7W÷'G2à¢¢¤öæRÆ–Ö—BöbF†RÖW6‚—2v÷'F‚7FF–æröâ—G2÷vâ¢¢Â&V6W6R—B—2F†RÖ÷7B7V6–f–2‡&6P¢–âF†R6÷W&6Râ¥&W7F–æröâF†R&÷GFöÒ¢—2v†BF—7F–æwV—6†W2&VçBg&öÒG&—fVâ–ÆR&VçBÀ¢æB&÷fRF†RvFW&Æ–æRF†RGvò&RF†R6ÖR–7GW&S²öÆöuö&VçFF–ffW'2g&öÒ÷–ÆUö&VçF'¢f÷W"†Vg’Æöw2v–ç7BF‡&VRÆ–v‡BöæW2Âv†–6‚—2v†Bf—6—F÷"6â7GVÆÇ’6VRâF†R&W7@¢öbF†RF—7F–æ7F–öâÆ—fW2–âF†R&V6÷&BæB–âF†—2f–ÆRà £#Râ¢¥F†Rf—'7B'V–ÆF–ærv†÷6Rfö÷G&–çB—2Wf–FVæ6RÂæB6÷'&V7F–öâFò÷W"÷vâF÷76–W"F†@¢6†ævW2v†B—B—2â¢¢†övå÷7F÷&V(	BF†RÆör7F÷&RBF†RvW7BVæBöbF†RÆ¶R7G&VWB&Æö6°¢–âv†–6‚F†RVæ—FVB7FFW2÷VæVB÷7Böff–6RB6†–6vòöâ3Ö&6‚ƒ3(	B—2F†RV–v‡F€¢7G'V7GW&RæBF†Rf—'7B%T”ÄD”är†W&Rv†÷6R÷WFÆ–æR—2æ÷BÆ6V†öÆFW"âæG&V2v—fW2—G0¢6—¦RGv–6RÂ–âGvò–æFWVæFVçFÇ’w&—GFVâ76vW3¢%F†R'V–ÆF–ærv2GvVçG’'’f÷'G’Öf—fRfVW@¢–â6—¦RÂv2'F—F–öæVBöfb6ò2Fò6W'fR2÷7BÖöff–6RöâöæR6–FRÂæB2F†R7F÷&Rö`¢'&Ww7FW"Â†övâb6òâÂöâF†R÷F†W""ÂæB'F†R7F÷&RöæÇ’ö67W–VBâ&Vöbf÷'G’Öf—fR'¢GvVçG’fVWB"âCR9r#gB—22ãsb9rbã“bÒæBF†Rfö÷G&–çB—2FvvVBFö7VÖVçFVFÂv†–6€¢æò'V–ÆF–ærfö÷G&–çB–âF†—2FF6WB†2&VVâ&Vf÷&Râ¢¥v†B—2Fö7VÖVçFVB—2F†R4•¤Ræ@¢æ÷BF†RÆâ¢£¢v†–6‚†—2'Vç2ÆöærF†R7G&VWB—2æö&öG’w2Wf–FVæ6RÂ6òF†B76–væÖVçB6—G0¢öâF†Rf6FR&V&–ær–âF†R÷6—F–öâæ÷FRÂv†W&R&÷FF–ærF†R'V–ÆF–ær—2v†B6†ævW2—Bà¢¢¥F†—2—2Ç6òF†Rf—'7B&V6÷&B†W&Rv—F‚æ÷F†–ær6öæ¦V7GW&Â–â—B¢¢Âv†–6‚—2æ÷B&ö7B(	@¢—BÖVç2—G2v2&Rv2–âF†R6÷W&6W2r&V6—6–öâ&F†W"F†â†öÆW2f–ÆÆVB'’–çfVçF–öâà¢—BFöW2ÖVâF†R÷Ww2V×G’%v†BvRÖFRW†W&R"7FFR—2f–æÆÇ’W†W&6—6VB'’&VÂFFÀ¢v†–6‚*r&V6÷&FVB2VæW†W&6—6VBà¢¢¥F†R6÷'&V7F–öâ—2F†RÖ÷&RW6VgVÂ†Æbâ¢¢Fö72÷&W6V&6‚ó2×7G'V7GW&W2Öæ÷'F‚æÖF*rBFFW0¢F†R÷7Böff–6Rw2Ö÷fRFòF†Rg&æ¶Æ–âæB6÷WF‚vFW"FG&W72g&öÒ"æ÷fVÖ&W"ƒ3"ÂF†RF¢†övâ7V66VVFVB&–ÆW’2÷7FÖ7FW"ÂæB6ÆÇ2F†BF†Rƒ3Röff–6RâæG&V26—2Gv–6RF†@¢F†Röff–6Rv27F–ÆÂBÆ¶RæB6÷WF‚vFW"F‡&÷Vv‚ƒ32æBÖ÷fVB¢¦&÷WB§VÇ’ƒ3B¢¢âF†P¢F÷76–W"w26öæ6ÇW6–öâ7W'f—fW2æB—G26‡&öæöÆöw’FöW2æ÷C¢F†Rƒ3"FFR—2F†R÷7FÖ7FW"w2À¢æ÷BF†R'V–ÆF–ærw2âF†R6öæfÆF–öâ—2G&6V&ÆRFòF†R7W'&W’vRF†RF÷76–W"W6VBÂv†–6€¢Ö¶W2F†Rö–çFÖVçBæBF†RÖ÷fRöæR6VçFVæ6R(	BæBv†–6‚Ç6ò7WÆ–W2F†R'6÷WF‚vW7@¢6÷&æW""F†BæG&V2æWfW"v—fW2â6÷W&6R&V6÷&B6†–6vöÆöw•öf—'7E÷÷7Eööff–6V6—2öâ—G0¢÷vâf6Rv†W&R—B—2föÆÆ÷vVBæBv†W&R—B—2æ÷Bâ¢¥F†R6öç6WVVæ6Rf÷"F†R66VæR¢£¢öà¢ƒ3RÓrÓF†—2'V–ÆF–ær—27F÷&RF†BW6VBFò&RF†R÷7Böff–6RÂæBF†RF÷vâw27GVÀ¢÷7Böff–6R—2F–ffW&VçBÂVæÖöFVÆÆVB'V–ÆF–ær&÷WBÒV7BÂöbv†–6‚æ÷F†–ær7W'f—fW0¢'WB7G&VWB§Væ7F–öâ(	B—Bv÷VÆB&RF†RÖ÷7B–çfVçFVB'V–ÆF–ær–âF†RFF6WBæB—B—0¢w&—GFVâF÷vâ&F†W"F†â'V–ÇB†Fö72õ$U4T$4‚ö†övå÷7F÷&RæÖF*rB’à¢¢¥F†RvV²ö–çB—27W'f—fÂÂæ÷BvVöÖWG'’ÂæB—B—27FFVBöâF†R&V6÷&Bâ¢¢F†R'V–ÆF–ær—0¢GFW7FVB7FæF–ærFò&÷WB§VÇ’ƒ3BæBæò6÷W&6R&V6†VBföÆÆ÷w2—B7BF†C²—B—2Æ6V@¢–â66VæR6WBVÆWfVâÖöçF‡2ÆFW"öâF†R6öçF–çV—G’&wVÖVçBÂv—F‚F†R6÷VçFW"Ö&wVÖVçB(	@¢Æ¶RæB6÷WF‚vFW"v2F†R6÷&æW"Ö÷7BW‡÷6VBFòF†Rƒ3R&ööÒ(	B–âF†R6ÖRæ÷FRâ–`¢Wf–FVæ6RGW&ç2WF†B—B6ÖRF÷vâf—'7BÂ—B&VÆöæw2–âW†6ÇW6–öç2æ§6öææBF†—2&V6÷&@¢ÆVfW2F†R66VæRà¢¢¤öæR6ÖÆÆW"F†–ær6ÖR÷WBöbF†R6ÖRvRæB—2&V6÷&FVB&F†W"F†â7FVBöââ¢¢7W'&W¢†2F†ö×6öâw2ƒ3ÆBÆ––ær÷WB7G&VWG2'Væ–f÷&ÖÇ’cbfVWBv–FR#²WfW'’÷6—F–öâ–âF†—0¢FF6WBöfg6WG2'’†Æböbâ¢£ƒgB¢¢7G&VWBÂg&öÒF†Rv–GF‡2ææ÷FFVBöâ†F†v’ƒ3Bà¢F†RF–ffW&Væ6R—2"ãÒÂâ÷&FW"öbÖvæ—GVFR–ç6–FRF†RvV÷&VfW&Væ6Rw2÷vâW'&÷"Â6òæ÷F†–æp¢Ö÷fW2(	B'WBF†RGvò6ææ÷B&÷F‚&R&–v‡B&÷WBF†R6ÖR7G&VWBÂæBF†R&V6öæ6–Æ–F–öâv÷'F€¢FW7F–ær—2F†BF†W’&Ræ÷B&÷WBF†R6ÖR7G&VWBâ6VRFö72õ$U4T$4‚ö†övå÷7F÷&RæÖF*rRà £#bâ¢¥v†Bv2ÆVgB÷WB—2&VF&ÆR–âF†RvÆ·F‡&÷Vv‚ÂæBVæf÷&6–ær—Bf÷VæBF†RöæRf–ÆP¢v†W&R'VÆRöæRv2æWfW"6†V6¶VBâ¢¢FFöW†6ÇW6–öç2æ§6öæ(	Bf÷W'FVVâ&W6V&6†V@¢7G'V7GW&W2v—F‚F†RWf–FVæ6RF†BFFW2F†VÒÂÇW2f÷W"Ö—FVÒvF6‚Æ—7B(	B†2W†—7FV@¢6–æ6RF†R66fföÆBæB†2&VVâ&VB'’vVçG2öæÇ’âf—6—F÷"7FæF–ær–ââV×G’Æ÷@¢6ææ÷BF—7F–æwV—6‚F‡&VRF–ffW&VçB7FFVÖVçG3¢æö&öG’&W6V&6†VBF†—2ÂF†RWf–FVæ6P¢FFW2—BgFW"F†R66VæRÂ÷"—B†BÇ&VG’6öÖRF÷vââF†Rf—'7B—2v–âF†Rv÷&°¢æBF†R÷F†W"Gvò&Rf–æF–æw2F†B6÷7B&W6V&6‚FòW7F&Æ—6‚âF†RWf–FVæ6RæVÂæ÷p¢6'&–W2F†VÒVæFW"¢¥v†B—2æ÷B†W&R¢¢ÂFW&—fVBW"66VæR'’6ö×–ÆU÷66VæRç–v—F€¢F†R6—FF–öç2¦ö–æVBÂ&VÆ÷rF†RÆ–&W'F–W2æB–âF†R6ÖRÆFWF–Ç3æVçG'’Â&V6W6P¢F†W’&RF†R6ÖR¶–æBöbF—66Æ÷7W&Rà¢¢¥F†R6†——2F†R&V6÷&Bw2f–VÆBÂæWfW"‡&6RFW&—fVBg&öÒâ'6Væ6Râ¢¢FVâVçG&–W0¢6''’V&Æ–W7E÷66VæVæB6†÷r&æ÷BVçF–Âƒ3r#²¶–ç¦–Uö†÷W6VæB÷V–ÆÖWGFUö6&–æ ¢vW&RW†6ÇVFVB&V6W6RF†W’vW&RtôäRÂ6''’æò7V6‚f–VÆBÂæBvWBæò6†—(	B7F×–æp¢öæRöâF†VÒv÷VÆB&Râ–çfVçF–öâöâF†RæVÂF†BW†—7G2FòFÖ—B–çfVçF–öç2âF†P¢6Öö¶R76W'G2F†BF—67&–Ö–æF–ær—"&F†W"F†â6÷VçBÂæB76W'G2F†B'V–ÆF–æp¢F†Rf—6—F÷"6âvÆ²WFò—2¦æ÷B¢öâF†RÆ—7BÂv†–6‚6V7F–öâGV×–ærF†Rv†öÆP¢FF6WBv÷VÆB7F–ÆÂ†fR76VBà¢¢¥F†RÆ—7B7FFW2v†B—B—2æ÷B¢¢ÂæBF†B6VçFVæ6R—26Öö¶R76W'F–öâFöó¢V–v‡Bö`¢&÷Vv†Ç’f÷'G’&W6V&6†VB7G'V7GW&W27FæBÂ6òf÷W'FVVâÖ—FVÒÆ—7Böb'6Væ6W2v—F‚æð¢7V6‚æ÷FR&VG22'F†—2—2v†B—2Ö—76–ær"Âv†–6‚v÷VÆB&RF†RÆ&vW7BfÇ6R6Æ–ÒF†P¢æVÂ6÷VÆBÖ¶Rà¢¢¥Gvò'VÆW2'&—fVBv—F‚—BÂæBF†Rf—'7B—2VÖ&'&76–ær–âF†RW6VgVÂv’â¢¢tTåE2æÖ@¢'VÆR—2F†BWfW'’6÷W&6Uö–F&W6öÇfW2–âFF÷6÷W&6W2ö²W†6ÇW6–öç2æ§6öæv2F†P¢öæRf–ÆRv†W&Ræ÷F†–ærVæf÷&6VB—BÂ&V6W6RVçF–Âæ÷ræ÷F†–ær&VB—B(	B6—FF–öâF†W&P¢6÷VÆB†fRæÖVB6÷W&6RF†BæWfW"W†—7FVBæBF†RvFRv÷VÆB†fR7F–VBw&VVâà¢6†V6µöW†6ÇW6–öç6†öÆG2—BFòF†R6ÖR7FæF&B27G'V7GW&R&V6÷&C¢6ÇVr–BÂ¢æÖRÂ7FFVB&V6öâ†âW†6ÇW6–öâv—F†÷WBöæR—2FVÆWF–öâv—F‚f–ÆVæÖR’ÂæB@¢ÆV7BöæR6—FF–öâF†B&W6öÇfW2âF†R6öÖÖ—GFVBf–ÆR76W2Væ6†ævVC²F†RfÇVR—2F†@¢F†RæW‡BVçG'’6ææ÷BâF†R6V6öæB—2F†RFFRvFR&VB&6·v&G3¢âVçG'’FF–ær¢'V–ÆF–ærFòƒ3r—26÷'&V7BW†6ÇW6–öâg&öÒƒ3RæBu$ôäröæRg&öÒƒ3rÂæBæð¢6ö×&—6öâv–ç7BF†R&V6÷&G26â6F6‚—B&V6W6RâW†6ÇVFVB7G'V7GW&R†2æò&V6÷&@¢Fò6ö×&Rv—F‚â–â–V"×&ÖWFW&—¦VB&ö¦V7BF†B—2W†7FÇ’F†R6†V6²v÷'F‚†f–æp¢&Vf÷&RF†R6V6öæB66VæRW†—7G2&F†W"F†âgFW"à¢¢¥F†RvF6‚Æ—7B—2FVÆ–&W&FVÇ’æ÷B6†÷vââ¢¢—G2f÷W"—FV×2&R7G'V7GW&W2v†÷6Rƒ3P¢7FGW2—2Væ6W'F–â&F†W"F†â6WGFÆVBÂæBöæRöbF†VÒ†vW7FW&åö†÷FVÆ’—27FæF–ær–à¢F†R66VæR(	BWGF–ærF†VÒVæFW"'v†B—2æ÷B†W&R"v÷VÆB&RfÇ6R&÷WBF†RöæRF†–ærF†P¢6V7F–öâ—2f÷"âF†V—"Væ6W'F–çG’&VÆöæw2öâF†R&V6÷&G2æB–âF†R&÷fVææ6R÷WÀ¢v†–6‚—2F–ffW&VçB6Æ–6RæB—2æ÷BVWVVBà£#râ¢¥F†R6–FV6'2&R&RÖFW&—fVB'’F†RvFRæ÷rÂv†–6‚F†W’vW&Ræ÷Bâ¢¢6ö×–ÆU÷66VæRç– ¢w&—FW2v†BF†R&VæFW&W"&VG2æBF†R÷WGWG2&R6öÖÖ—GFVB6òF†R6—FRæVVG2æò'V–Æ@¢7FW(	Bâ'&ævVÖVçBF†BöæÇ’†öÆG2–bG&–gB—2f–ÇW&Râæ÷F†–ær&V6ö×WFVBF†VÒÂ6ð¢&V6÷&BVF—FVBv—F†÷WB&V6ö×–ÆR6†—VBvÆ·F‡&÷Vv‚V÷F–ærF†R&Wf–÷W2FF6W@¢v—F‚WfW'’6—FF–öâ7F–ÆÂÆöö¶–ærWF†÷&—FF—fRâÒÖ6†V6¶&RÖFW&—fW2FòÖVÖ÷'’æ@¢6ö×&W3²6†V6²ç6†'Vç2—BÂF†R6ÖRv’—BÇ&VG’&RÖFW&—fVBÆ–&W'F–W2æ§6öæâF†P¢V–v‡B6öÖÖ—GFVB6–FV6'2æBF†R–æFW‚vW&R'—FRÖ–FVçF–6ÂöâF†Rf—'7B'VâÂ6òF†—0¢7v—F6†VBöâv—F‚æò&W—"&V†–æB—Bâv†B—BFöW2äõB6†V6²—2F†RF—&V7F–öâF†P¢7FÆVæW72vFR6÷fW'2(	BF†BF†RtÄ"ÖF6†W2F†R&V6÷&B(	BæBæV—F†W"öbF†VÒ6â6VR¢&V6÷&BF†B—2w&öær&÷WBF†RF÷vâà ¢22æW‡@ ¢¢¥3R(	BÖ÷&R7G'V7GW&R&V6÷&G2¢¢Âv†–6‚—2æ÷rF†R&–æF–ær6öç7G&–çC¢6WfVâ7G'V7GW&W27Fæ@§v†W&RF†R6÷W&6W2FW67&–&R&÷Vv†Ç’f÷'G’ÂæBöæRöbF†R6WfVâ—2'&–FvRâæ÷FRF†R6÷WÆ–ærF—66÷fW&VBöâ##bÓ‚ÓÂ&V6W6R—B6WG0§F†R6†RöbF†Rv÷&³¢FööÇ2ö6ö×–ÆU÷66VæRç–w&—FW2â76WFF‚f÷"WfW'’7G'V7GW&RF†@§&W6öÇfW2–çFòF†R66VæRÂ6ò&V6÷&B6öÖÖ—GFVBv—F†÷WB—G2tÄ"Ö¶W2F†R&VæFW&W"fWF6‚f–ÆP§F†B—2æ÷BF†W&R(	BCBF†R6Öö¶R6÷'&V7FÇ’f–Ç2öââ¢¤7G'V7GW&R&V6÷&BæB—G2&¶R&RöæP§Væ—Bâ¢¢âvVçBv—F†÷WB&ÆVæFW"6â&W&RF†R&V6÷&BæBF†R&W6V&6‚ÖVÖòÂ'WBF†R—"†0§FòÆæBFövWF†W"Â6òF†R&¶Rv÷&¶fÆ÷rw2"—2'BöbF†R6ÖR6Æ–6R&F†W"F†âföÆÆ÷r×Wà¢¢¥F†B6÷WÆ–ær—2æ÷rVæf÷&6VB&F†W"F†â&VÖVÖ&W&VB¢¢ƒ##bÓ‚Ó“¢VF—F–ærfÇVR¦vVæW&F÷"&VG2Ö¶W2F†R6öÖÖ—GFVBtÄ"7FÆRæB6†V6²ç6†f–Ç2VçF–ÂF†R&RÖ&¶RÆæG2v—F€¦—Bâ—Bv2F†VâW†W&6—6VBf÷"&VÂ'’F†RvöÆbö–çB&W—"F†R6ÖRF’(	BF†R&VæÖRGW&æVBF†P§FfW&âw276WB7FÆRöâF†R7÷BæBF†R'&æ6‚6÷VÆBæ÷Bvòw&VVâVçF–ÂF†R&¶RÆæFVBöâ—BÀ§v†–6‚—2F†Rv†öÆRö–çBöbw&—F–ærF†R6†V6²ÂæBv–âF†R6ÖRF’'’Ö–ÆÆW"w26V6öæB6†–ÖæW’À¦æBF†—&BF–ÖR'’†—2g&ÖR&ævRà¢¢¥F†R&W—"Æ—7B&Vf–ÆÆVB—G6VÆbg&öÒF†R&6†—fR&F†W"F†âg&öÒF†RvFW2ÂæBV×F–VBv–à§F†R6ÖRF’¢¢ƒ##bÓ‚ÓÂ*r#2(i"*r#B’âWfW'’&Wf–÷W2VçG'’öâ—Bv2f÷VæB'’6†V6³¢¦Ö—77VÆÆVBGG&–'WFRÂæÖR&VB2&V–ær&÷WBF†Rw&öær†Æböb'V–ÆF–ærâF†BöæRv2f÷Væ@¦'’&VF–ærvRÂæB—B—2æ÷r¢¤DôäR¢¢(	BF†R&V6÷&BÂF†R&6†WG—RæBF†R&¶RÆæFV@§FövWF†W"Â–W%ö6÷VçC¢&&WÆ6VB–W%÷76–æuöÖÂæBF†RVWVR—2V×G’v–ââv†B—BÆVfW0¦&V†–æB—26†Rv÷'F‚&WW6–ær&F†W"F†âF6³¢v†VâWf–FVæ6RæBâ&6†WG—RF—6w&VRÂ6†V6°§v†WF†W"F†R&6†WG—R—26¶–ærf÷"F†Rw&öær¦¶–æB¢öbçVÖ&W"&Vf÷&R6†æv–ærF†RçVÖ&W"—B†2à¥F†RöÆFW"66÷VçBöbF†RVWVRÂ7F–ÆÂG'VRöbWfW'—F†–ær&Vf÷&RF†—2VçG'“¢F†RÆ7BVçG'’(	@¦Ö–ÆÆW%ö†÷W6V&V6÷&F–ærFö7VÖVçFVFg&ÖR&ævRv—F‚æò6–FRÂv–GF‚ÂFWF‚÷"7F÷&W’6÷VçB(	@¦ÆæFVB##bÓ‚Óv—F‚—G2&¶RŒ*r#’ÂæB—Bv2F†Rf÷W'F‚æBÆ7BöbF†RfVÇG2F†RöÖ—76–öà¦vFR÷VæVBâF‡&VRöbF†Rf÷W"vW&R7VÆÆ–æs²F†Rf÷W'F‚v2æÖR&VB2&V–ær&÷WBF†Rw&öæp¦†ÆböbGvò×'B'V–ÆF–ærÂv†–6‚æò7VÆÆ–ær6†V6²v÷VÆB†fR6Vv‡Bâæ÷F†–æræWr—2VWVV@¦&V†–æB—BÂ6ò¢¥3R—2FF—F–öç2v–â¢£¢V–v‡B&6†WG—W2æB&÷WBf÷'G’&W6V&6†VB7G'V7GW&W0¦v–ç7BF†R6—‚F†B7FæBà ¢¢¥3’(	B7G&VWG2Â&öG2æBF‡2¢¢Â¢¤d•%5Bd•4”$ÄR4Ä”4RDôäR##bÓ‚Óâ¢¢6WfVçFVVâFFV@¦V'F‚G&fVÇv—2&R6ö×–ÆVBg&öÒFF÷7G&VWG2óƒ3Ræ§6öæÂG&VB&F†W"F†âfÆGFVæVBÂæ@¦–FVçF–f–VBÆ—fRv—F‚F†V—"ƒ3RæB##bæÖW2âF†RV&Æ–W"6VçFVæ6R†W&R6––ær&æ÷F†–ærv0¦w&FVBVçF–ÂƒSRÓS‚"6öægW6VBF†RÆFW"&—6–æröb6†–6vòv—F‚V&Ç’7G&VWBv÷&²æBv0§w&öæs¢6÷WF‚vFW"v2÷&FW&VB—F6†VB'’&–Âƒ3BæBw&FVBf÷"G&–ævRF†B§VÇ“²6÷WF€¥vFW"æBÆ¶RvW&RF†RGvòV&Ç’&–æ6—Â–×&÷fVB&÷WFW2âv†B&VÖ–ç2—2F†Ræ÷'F‚×6–FP¦6öçG&öÂöW‡FVçB&W6V&6‚Âç’6W&FVÇ’GFW7FVBÆæ²fö÷GvÆ·2ÂæBWf–FVæ6RF†B6÷VÆB&WÆ6P§F†R6öæ¦V7GW&ÂG&fVÆÆVBv–GF‡2æB'WBGFW&ç2&V6÷&FVB–âÃs’â6VR$ôDÔ*r3’à ¢¢¥3V(	Bf÷'BFV&&÷&â¢¢(	B¢¤DôäR##bÓ‚Ó¢¢Â&÷F‚vFW26ÆV&VB&Vf÷&Rç’vVöÖWG'’à¢¢¥F†Rfö÷G&–çB†26÷W&6Râ¢¢bâ†'&—6öâ§"âw27W'fW’öbF†RÖ÷WF‚öbF†R6†–6vò&—fW"f÷ §F†R†&&÷W"v÷&·2Â#BfV''V'’ƒ3Â&÷fVB'’v–ÆÆ–Ò†÷v&BÂRå2â6—f–ÂVæv–æVW"Â&W&öGV6V@¦–âæG&V2föÂââ2æBÆ—7FVB–âF†BföÇVÖRw2÷vâF&ÆRöbÖ22$f÷'BFV&&÷&â–à£ƒ3Ó3""â—BG&w2F†Rf÷'B”âÄâ(	B7V&RVæ6Æ÷7W&RÂv÷&·2BF‡&VRævÆW2Âf÷W"&ævW2ÂGvð¦vFW2ÂGvò'V–ÆF–æw2fÆæ¶–ærF†R6÷WF‚vFR(	BæB—G2'&ævVÖVçB—26÷'&ö&÷&FVB'V–ÆF–ær'¦'V–ÆF–ær'’wW&Föâ‡V&&&Bw2ƒ#rvÆ²&÷VæBF†R–ç6–FR„æG&V2â#cB’â&V6÷&FVB0¦†'&—6öåóƒ3÷&—fW%öÖ÷WF†â¢¥F†RÆFR†2æò66ÆR&"¢¢Â6òF†R66ÆR—2FW&—fVBg&öÒF†RöæP§7FFVBF–ÖVç6–öâ–âF†Rv†öÆR6ö×ÆW‚(	BF†R6öÖÖæFçBw2V'FW'2B&&÷WB#R‚SgB"–âF†P£ƒSR†÷Föw&‚¶W’(	Bv—f–ærãgB÷‚æB7Fö6¶FR&÷WBS2ÒƒsBgB’7V&RB¢¬+#R¢¢à¥Gvò6†V6·2öâF†R6ÖRÆFRw&VRFòRRæBRâ¢¥F†Rv'&—6öâ—26WGFÆVB¢£¢†VÆ@¦6öçF–çV÷W6Ç’g&öÒ§VæRƒ3"Fò#’FV6VÖ&W"ƒ3bÂÖ¢â¦ö†âw&VVæRWF‚–æfçG'’Ö÷7BÆ–¶VÇ¦6öÖÖæF–æröâF†R66VæRFFRÂ7G&VæwF‚gFW"ƒ32VæGFW7FVBâf÷W'FVVâ&V6÷&G2ÂGvòæWp¦&6†WG—W2†Æ—6FVÂf÷'E÷7G'V7GW&V’Âf÷W'FVVâ&¶W2ÂãrÃG&–ævÆW2âf—fRW†6ÇW6–öç0§vVçB–âv—F‚—BÂf÷W"öbF†VÒw&öærÖf÷'Bf–æF–æw2â6VRFö72õ$U4T$4‚öf÷'EöFV&&÷&âæÖFà¢¢¥v†B—BF–BäõB6WGFÆRæBv†B—2æ÷rF†R&–æF–ær6öç7G&–çC¢F†W&R—2æòw&÷VæBVæFW"—Bâ¢  ¢¢¥3&R(	BW‡FVæBF†Rw&÷VæBV7BFòF†RÆ¶Râ¢¢&—6VBFòF†RF÷öbF†RFW'&–âv÷&²öà£##bÓ‚ÓB¶Wf–âw2F—&V7F–öâÂgFW"g&VRÖfÇ’ÖFR—Bf—6–&ÆRg&öÒF†R—#¢F†RÖöFVÆÆV@¦&÷‚7F÷2BÆö6ÂR³3#Âv†–ÆRF†Rf÷'BFV&&÷&â6—FR—2BR³#ræBF†Rƒ3R6†÷&R—0¦&÷WB¶–ÆöÖWG&RgW'F†W"7F–ÆÂâf÷'BFV&&÷&âæBF†R†&&÷W"v÷&·26ææ÷B&RÆ6VBVçF–À§F†Rw&÷VæBVæFW"F†VÒW†—7G2âF†R6†÷&VÆ–æR—G6VÆb—2&÷fVææ6R&ö&ÆVÒ&Vf÷&R—B—2¦ÖöFVÆÆ–æröæR(	BWfW'—F†–ærV7Böb&÷Vv†Ç’Ö–6†–vâfVçVR—2ÆFW"ÆæFf–ÆÂÂ6òF†RVFvP¦×W7B6öÖRöfbw&–v‡Bƒ3BÂæ÷BöfbÖöFW&â6ö7Bâ6VR$ôDÔ*r3&Rà ¢¢¥&6VÂ†’—2FöæRæB&6VÂ†"’—2F†RæW‡B6Æ–6Râ¢¢F†R6†÷&R—2æ÷rG&6V@¢†FööÇ2÷G&6U÷6†÷&VÆ–æRç–(i"6†÷&VÆ–æRævVö§6öæÂÖVÖð¦Fö72õ$U4T$4‚÷6†÷&VÆ–æUö†&&÷%óƒ3BæÖF’æB—BÖ÷fVBGvòçVÖ&W'2öfbW7F–ÖFRæBöçFð¦ÖV7W&VÖVçC¢F†RÖ–æÆæB6†÷&R&V6†W2Æö6Â¢¤R³#Sr¢¢æBF†R6æB&"w2V7BVFvP¢¢¤R³C“r¢¢Â6òF†R&öFÖw2&÷÷6VB³S&÷‚v÷VÆB†fR6Æ—VBF†R&"'’2ÒæBF†P¦&÷‚6†÷VÆB&R¢¢³Sc¢¢âGvò–æFWVæFVçB6VvÖVçFF–öç2öbF†R6ÖR6†VWBÂ–âF–ffW&VçBv–æF÷w0§v—F‚F–ffW&VçB&6¶w&÷VæB7FF—7F–72Âw&VR–âF†V—"ƒÒ÷fW&ÆFò¢£ã(	3RãrÒ¢¢öâF†R6÷WF€¦&æ²æB¢£ã^(	3ã2Ò¢¢öâF†Ræ÷'F‚(	Bv÷'F‚7FF–ær&V6W6R—B—2Wf–FVæ6RF†BF†RG&6R&VG0§F†RG&Vv‡G6Öâw2Æ–æRæBæ÷B—G2÷vâF‡&W6†öÆG2âv†B—27F–ÆÂ'6VçC¢¢¦æòVÆWfF–öâW†—7G0¦ç—v†W&RV7BöbR³3#¢¢ÂF†R&"–æ6ÇVFVBâ&"—27W&f6R6÷WÆRöbfVWBöbÆ¶R7FvP¦Ö÷fW2æBæò6÷W&6Rv—fW2—G2†V–v‡BÂ6òF†RçVÖ&W"v–ÆÂ†fRFò&R&wVVB–âF†RFW'&–â7V0§&F†W"F†â–6¶VBâVçF–ÂF†R†V–v‡Ff–VÆBæB—G2&¶RÆæBFövWF†W"Âæ÷F†–ærV7BöbF†P¦7W'&VçB&÷‚&VæFW'2æBF†RW&–Âf–Wrw2VFvR—2Væ6†ævVBà ¢¢¥3"&VÖ–æFW"¢¢(	Bg&öröæBÂF†RvVÆÇ27G&VWBÖ'6‚ÂæBF†R&W7BöbF†R‡–G&öÆöw’&W–öæ@§F†R6–ævÆRG&6VB6Æ÷Vv‚6VçG&VÆ–æRà ¢¢¥3b(	BfÆ÷&æBfVæ&V6÷&G2¢¢Âv†–6‚—2Ç6òv†Bv÷VÆB&WF—&RÆ–&W'G’Ã"w2&öÖ—6S¢F†P§ÆWGFW2æBÆ6VÖVçBF&ÆW2W†—7B–âF†RF÷76–W'2æBæ÷F†–ær†2&VVâGW&æVB–çFòFFà ¤æWrf–æF–æw2f÷"3"g&öÒF†RFGVÒv÷&³¢†F†v’6'&–W27W'fW’&V&–æw2æBÆ÷BF–ÖVç6–öç0¢‚$âãS+Râ"ÆöærF†RÖ–â7FVÒÂƒÖgB7G&VWG2ææ÷FFVB“²&÷F‚ƒ3B6†VWG2&Ræ—6÷G&÷–6ÆÇ§7G&WF6†VBƒ2ãrRòBãRR’Â6ò7G&VWBvVöÖWG'’6†÷VÆB&RvVæW&FVBæÇ—F–6ÆÇ’g&öÒF†RÆ@¦F–ÖVç6–öç2æB6æVBFòF†Rf—GFVB6öçG&öÂÂæWfW"G&6VB&rg&öÒ—†VÇ2à 