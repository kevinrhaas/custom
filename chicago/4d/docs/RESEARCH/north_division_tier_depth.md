# How deep is the North Division's block tier? Read off the plat

**T-1457, 2026-09-20.** Every number here is recomputed from committed files by
`tools/measure_north_division_tier_depth.py`, which carries the assertions as
`--self-test` and which `tools/check.sh` runs. Its inputs are two committed files
and no image library: the pixel reading in
`data/traces/thompson_north_division_streets.json` and `data/streets/1835.json`.
`--reread` goes back to the 7 MB sheet and reproduces every committed pixel exactly.

## The ask

T-0451 read this sheet **across** — the six north–south corridors between Kinzie
Street and North Water Street, and the seven blocks they divide. It never read the
sheet **down**, so the tier had a width and no depth. T-1436 went to cut the lots
into those blocks and could not:

> The tier is bounded north by Kinzie Street and south by North Water Street.
> Kinzie is committed and `attested`. North Water is `reconstructed` and is CUT
> FROM THE RIVER BANK by `tools/derive_north_water.py`; `street_control.json` §
> `north_bank.not_in_the_corridor_layer` refuses it a corridor in as many words —
> *"offsetting that polyline by half a module would invent a rectangle no sheet
> draws"*. Taking the south face off North Water's committed centreline anyway
> gives block depths of 92 m at Franklin, 119 at Wells and 137–139 at La Salle,
> Clark and Dearborn, against the South Division's 93.9 m. **A tier the plat draws
> two lot rows deep does not run 92 m at one end and 139 m at the other; what
> varies is the bank, not the block.**

That last sentence is the thing this reading overturns. What varies **is** the
block. The plat draws the tier as a wedge, and it letters the figures that say so.

## What the sheet draws

Every block carries **four** horizontal lines, not two: the tier's north face, the
south edge of the upper lot row, the north edge of the lower lot row, and the
tier's south face. The two middle lines are an alley. Through the fit below:

| block | corridor pair | E | depth | upper row | alley | lower row |
|---|---|---|---|---|---|---|
| 5 | Franklin–Wells | 268.33 | 116.93 m | 178.6 ft | 20.4 ft | 184.6 ft |
| 4 | Wells–La Salle | 391.53 | 120.09 m | 191.9 ft | 20.4 ft | 181.7 ft |
| 3 | La Salle–Clark | 513.67 | 124.30 m | 207.0 ft | 21.8 ft | 179.1 ft |
| 2 | Clark–Dearborn | 636.87 | 128.32 m | 221.2 ft | 20.9 ft | 178.8 ft |
| 1 | Dearborn–Wolcott | 759.81 | 131.33 m | 232.7 ft | 21.1 ft | 177.1 ft |
| 7 | west of Market | 20.58 | 107.85 m | 149.2 ft | 22.9 ft | 181.7 ft |

**The lower row is constant and the upper row is the wedge.** The lower row runs
184.6, 181.7, 179.1, 178.8, 177.1 ft — mean 180.3 — and the sheet **letters that
row 180**, once in every block, down the west edge of lot 4, with the figure 80
across the same lot's head. The upper row runs 178.6 → 232.7 ft, growing
monotonically eastward and taking up the whole difference.

That is what a surveyor does when a straight section line runs above a river bank
that falls away from it: hold the river frontage at one depth, and let the back row
absorb the rest. Block 1's is the only upper-row figure lettered on the tier, which
is consistent — the upper row is a different depth in every block, so there is no
one figure to letter, and the surveyor lettered the row that **is** constant.

## The sheet's own chained figures close on it

Block 1's east line, against the Due North / True Meridian line, is lettered **260**
over **180**. The 260 is not the upper row alone, which is drawn 237 ft there: it is
the upper row **plus the alley**, drawn 258.9 ft. And 260 + 180 = 440 ft from the
section line to the tier's south face, against 436.2 drawn. The chain closes to 1 %
without anything being fitted to it.

## The fit, and the half of it that fails

Pixels become metres through a px-to-northing fit anchored on three South Division
corridors — Lake, Randolph and Washington — whose two edges are measured on this
same sheet (20 samples, `south_division_control_px`) and whose centrelines are
committed. It lands on **0.5345 m/px**. T-0451's independent px-to-easting fit, from
four *north–south* corridors, landed on **0.5345**. Two fits, two axes, seven
controls, no shared arithmetic, agreeing to **0.004 %**. Each control corridor comes
back an 80 ft street to within 1.1 m.

The tier, however, stands 400–700 px above that control band, and a
one-dimensional fit does not survive the extrapolation intact. Held **out** of the
fit, the committed Kinzie line is missed like this:

| block | E | read north face | committed Kinzie south kerb | residual |
|---|---|---|---|---|
| 5 | 268.33 | +262.99 | +246.23 | **+16.76 m** |
| 4 | 391.53 | +257.98 | +245.25 | +12.73 m |
| 3 | 513.67 | +252.88 | +244.28 | +8.61 m |
| 2 | 636.87 | +248.04 | +243.30 | +4.75 m |
| 1 | 759.81 | +242.68 | +242.32 | **+0.37 m** |

A miss that runs monotonically with **easting** is a shear in the sheet, not
scatter — and the sheet says so itself: its east–west lines do not share one lean
(South Division corridors +0.017 to +0.024, the tier's north face +0.041, its south
face +0.071, block 7's +0.088), which is why a row scan has to search lean per line
where T-0451's column scan could fit one lean per band.

**So this reading publishes depths and refuses northings.** A depth is a difference
taken at one easting, and the lettered 180 ft confirms it in the extrapolation zone
to 0.2 ft in the mean. An absolute northing from up here would launder the shear
into false precision. T-1458 seats the tier off committed Kinzie and cuts the blocks
to the depths above.

## What the sheet will not give

**Block 6** returns only two of its four lines — the north face and one middle line.
It is the block the plat draws its watercourse across, and the two freehand banks
cross the lot lines there (T-0452, `thompson_plat_sloughs.md`); the same block
already swallows a vertical stroke in T-0451's reading. Its depth is carried on the
tier line, not read.

**Block 7** returns all four and is reported, but held out of the straight-line south
face: its south face sits 3.2 px (1.74 m) off the line blocks 5–1 share and leans
+0.088 against their +0.071. Block 7 fronts the North Branch, not the main stem, and
there is no reason to expect it on the same line. Its lower row still comes back
181.7 ft, so the 180 ft rule holds there too.

Across blocks 5–1 the south face **is** one straight line, to half a metre: residuals
+0.18, −0.43, +0.16, +0.24, −0.16 m.

## What this does not settle

The tier's south face is the north line of **North Water Street** as the plat draws
it. This reading does not re-grade North Water, does not touch
`derive_north_water.py`, and does not give the corridor `street_control.json`
refuses it: it says where the *blocks* stop, which is a different statement from
where the *street* runs, and only the first is drawn.
