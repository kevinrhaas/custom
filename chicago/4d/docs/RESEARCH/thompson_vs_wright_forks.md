# Thompson 1830 against Wright 1834 at the forks

**T-0685, 2026-09-05.** The river banks this reconstruction stands on are traced from the
Wright 1834 survey. The owner reads the Thompson 1830 plat differently at Wolf Point, and
T-0453 asked for the difference to be *measured* rather than characterised. This is the
measurement. **Nothing moved**: the terrain's planform is unchanged, and this page and the
two files it rests on exist so that the decision about whether it should move can be made
against numbers.

## What had to be built first

`data/sources/thompson_plat_1830.json` calls the sheet a **parameter source** — "read for
its stated figures, never traced for geometry" — and there were no Thompson ground control
points in `data/traces/gcp/`. Two drawings in two frames cannot be compared, so the plat had
to be fitted to the frame the datum was fitted in before anything could be said at all.

**`data/traces/gcp/thompson_1830_gcps.json` — 23 control points, RMS 4.2 m, worst 9.4 m.**
Every point is a street crossing *inside* the plat, never on its boundary: the sheet's south
and east edges are the "Due East and West Line" and the "Due North Line", which are section
lines rather than street centrelines, and reading Madison or State Street off them would bake
a 12 m half-street of assumption into the control. Nineteen junctions were read from
OpenStreetMap on 2026-09-05 under the rule already written down in
`data/traces/street_control.json` `node_rule`; four are re-used from control this project had
already committed, so the Thompson fit and the Wright fit stand on the same ground where they
overlap.

**That 4.2 m is a fact about the drawing, not about the ground.** Wright fits at RMS 17.5 m
and Hathaway at 17.7 m because they are lithographs of a landscape on paper that stretched.
Thompson is a fair copy of a *survey*: its streets are ruled and its module is arithmetic, so
a ruled grid reproduces the ruled grid it laid out. **The river is the one feature on the
sheet the ruling does not govern**, which is exactly why the fit being this tight matters —
a 20-50 m disagreement about the river cannot be blamed on the georeference.

Three junctions were looked for and refused, and the refusals are recorded in the file rather
than left as absences: two on the Fulton Street row where the reading locked onto a lot line
(both then missed modern Fulton Street by 35-38 m in the same direction, which is what gave
them away), and Lake & Des Plaines, which reads cleanly on the plat and was not re-fetched on
the modern side after the residuals were already known.

## What was traced

`data/traces/vectors/thompson_1830_forks.json`, written by `tools/thompson_forks.py --trace`,
holds the plat's three shores over the bounding box of the three Wright bank lines, so neither
reading is compared against nothing. Thompson draws each bank as **one freehand ink line on
bare paper** — no wash, no fill, nothing to threshold between — so the reading is a ridge
follower rather than the region-growing that `tools/trace_river.py` needs on Wright's washed
sheet. The banks are the only freehand curves on an otherwise entirely ruled sheet, which is
what makes that safe here.

Two traces stop short of Wright's, and both stops are recorded in the file:

- the **north bank of the main stem** ends at the mouth of the slough. T-0452 read this sheet
  for its watercourses and found it draws exactly one besides the river, running north out of
  the main stem across North Division block 6 — and on the sheet the slough's west bank and
  the river's north bank are *one continuous line*, so a follower turns up it. The last 240 m
  of Wright's north bank therefore has no Thompson counterpart here, and the table below says
  so rather than hiding it;
- the **west bank of the North Branch** ends where the sheet's drawn bank ends, about 130 m
  short of Wright's north end, because above that the paper carries the Commissioners'
  certificate and a follower looking for the darkest line finds the handwriting.

## The disagreement, in metres

29 paired samples at named eastings and northings, chosen before the measurement was run.
Negative means Thompson is **west of** (or **south of**) Wright.

| reach | samples | delta range | reading |
|---|---|---|---|
| East bank of the North Branch | 5 | −16.9 to −36.7 m | Thompson well west |
| West bank of the North Branch | 8 | −26.2 to −55.7 m | Thompson much further west |
| West bank of the South Branch | 5 | −20.7 to −30.7 m | Thompson west |
| East bank of the South Branch | 4 | −1.0 to −9.4 m | **the two agree** |
| South bank of the main stem | 6 | −5.0 to −22.3 m | Thompson slightly south |
| North bank of the main stem | 1 | +7.4 m | (one sample; see the stop above) |

Over all 29: mean |delta| **23.7 m**, median 22.6 m, max 55.7 m, min 1.0 m; **signed mean
−23.2 m**. Eleven of the 29 fall inside the ±20 m `data/sources/thompson_plat_1830.json`
already declares for this dataset.

**The disagreement is not scatter and it is not a rotation.** Every sample but one has the
same sign, and the two sheets part company by a nearly constant amount along each bank. Put
as channel widths it becomes one sentence:

| | Thompson | Wright (`drafted_width_m`) | Thompson wider by |
|---|---|---|---|
| North Branch | 89-93 m | 72.9 m | ~20 m |
| South Branch | 67-75 m | 57.3 m | ~20 m |

**Thompson draws a river about 20 m wider than Wright does, in both branches, and sets it
about 20-30 m further west.** The east bank of the South Branch is where the two nearly touch
(1-9 m apart); the west bank of the North Branch is where they are furthest (up to 55.7 m).
Wolf Point's own tip lands 23.0 m apart — Thompson's 22.5 m west of Wright's and 4.8 m north.

## What this does and does not license

**It does not show that either sheet is wrong about the water.** Both are cadastral plats,
and `data/terrain/epochs/e1834_harbor_cut/river.geojson` already says so of Wright's:
"planform is as drafted on a cadastral plat, not a hydrographic survey". A cadastral river
line is the boundary the *lots* are surveyed to, and a survey that stops at the top of the
bank slope draws a wider channel than the water occupies. A systematic ~20 m of extra width
on both branches is the shape that explanation predicts, and neither sheet carries a sounding
to settle it.

**It is smaller than a disagreement this project has already recorded.** The same GeoJSON's
provenance note says "the two 1834 sheets disagree about the forks by 58 m" — Wright against
Hathaway, in the same reach, in the same frame. Thompson against Wright is 23.7 m in the mean
and 55.7 m at its worst. **The new sheet does not widen the spread of evidence about the
forks; it sits inside it.**

**What it does establish** is that the ±20 m the source record declares is not enough to
absorb this one: 18 of 29 samples exceed it, and on the west bank of the North Branch the two
readings do not overlap at ±20 m each. So "there was nothing to fix" is *not* the answer here,
and which planform is of record is the owner's call. The options, with the measurement in
front of them:

1. **Keep Wright.** Nothing moves. The Thompson line stays committed beside it as the second
   reading, and the ±20 m in the source record is restated as ±30 m at the forks so it
   honestly covers the spread the project can now see.
2. **Adopt Thompson at Wolf Point.** The west bank of the North Branch moves up to 55 m west
   and both branches widen by ~20 m. That re-derives every waterline test in the project and
   is its own unit of work — T-0453 acceptance 5 says so, and this page does not do it.
3. **Split the difference under a stated rule** — e.g. take the east banks from Wright, where
   the two nearly agree, and widen the channel to the mean. This is the option that invents a
   planform neither surveyor drew, and it is listed so it can be refused on purpose rather
   than by omission.

## Reproducing it

```
python3 tools/thompson_forks.py --check     # offline: re-derives the fit and every utm vertex
python3 tools/thompson_forks.py --fit       # re-solves the affine from the 23 control points
python3 tools/thompson_forks.py --trace     # re-reads the sheet (needs numpy + Pillow)
python3 tools/thompson_forks.py --measure   # prints the full table this page summarises
```

`--check` needs nothing installed: the fit is a pure-Python normal-equation solve, and every
`utm` vertex in the vectors file is re-derived from its committed `px` and compared. The
georeference is the part a reader most needs to be able to reproduce, so it is the part with
no dependencies.
