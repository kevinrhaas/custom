# The platted street module, and the control every placement stands on

**Record:** none — this is a memo about a *method*, not about a building ·
**Data:** `data/traces/street_control.json`, `data/traces/vectors/street_corridors_1834.json` ·
**Gates:** `check_position_derivations` and `check_street_module` in `tools/validate.py` ·
**Tools:** `tools/refetch_control.py`, `tools/measure_street_widths.py`

---

## 1. What was wrong with the way this worked

Five of the eight placed structures in this dataset are the same construction, and until
2026-08-10 it existed only as a sentence repeated once per building:

> the modern intersection centre was read from OpenStreetMap (EPSG:26916 E …, N …) and the
> footprint offset 12.2 m east and 12.2 m north of it, **half an 80 ft platted street** in each
> direction, so that the building's west face sits on the … frontage

Five paragraphs, five hand-done sums, one number — 12.2 — that no file contained. Two things
follow, and the second is the reason this slice exists rather than the first.

**A slip would have been invisible.** Nothing recomputed any of those sums. They happen to be
right; every one of the eight constraints now checked reproduces to within 0.02 m, which is the
rounding. But nothing was *making* them right, and the next placement was going to be done the
same way.

**The module could not be changed.** § 2 records a live disagreement about the platted street
width whose consequence is 2.13 m on every offset in the dataset. Settling it against five
paragraphs means five sums redone by hand and a reviewer with a calculator. Settling it against
one figure in one file, with a check that recomputes every placement from it, means editing one
number and reading which buildings moved. That is the difference between a disagreement that can
be resolved and one that gets recorded and left alone — which is what happened to this one on
2026-08-10 (see `docs/RESEARCH/hogan_store.md` § 5).

## 2. The width: 80 ft adopted, 66 ft recorded, neither averaged

| reading | figure | source | status |
|---|---|---|---|
| adopted | streets **80 ft**, alleys 18 ft | annotated on **Hathaway 1834** and read off the sheet during the datum work; the same figures are carried in `data/sources/thompson_plat_1830.json` | `inferred` |
| dissent | streets **66 ft** ("the length of a surveyor's chain"), alleys 16 ft | Currey, via `chicagology_first_post_office`, describing Thompson's 1830 plat | recorded, not adopted |

**Why 80 ft is adopted.** An annotation on a cadastral survey sheet is a measurement of the
streets it is drawn on; a sentence in a narrative history is a summary of the town. Where those
two disagree about the same object, this project follows the survey. Hathaway 1834 is also the
sheet this dataset already trusts for block and lot subdivision — it is what makes a building
documented at a named corner placeable *on* that corner — so adopting a different street width
from a different source would leave the geometry and the module reading two sheets.

**Why it is `inferred` and not `documented`** — as of 2026-08-09, superseded by § 8. The
annotation has not been read street by street.
This dataset applies one town-wide figure to Lake, Market, Canal, Randolph and Kinzie, and a
town-wide figure taken from an annotation is a reading rather than a measurement of each of those
five streets. That is exactly the shape `inferred` is for, and the note in
`street_control.json` states the reasoning as the confidence model requires.

**The reconciliation worth testing**, carried forward from `hogan_store.md` § 5: the two figures
may not be about the same streets — 66 ft general, with the riverfront and market streets platted
wider. Reading the widths off Hathaway 1834 at named streets settles it. That is a slice of
research, and it is now a slice with a single edit at the end of it.

**Both were settled on 2026-08-10 — see § 8, which is the measurement.** The corridors were read
off both 1834 sheets, 66 ft is excluded, the reconciliation dies with it, and the single edit
turned out not to be needed. What § 8 changes here is the *reason* the grade is `inferred`, not
the figure. And § 9 is what the same traverse found about the control point it started from.

**What being wrong would cost**, stated because it is computable rather than arguable: every
offset drops from 12.192 m to 10.058 m and five buildings move 2.13 m — an order of magnitude
inside the ±20 m the georeference already carries, so nothing here is misleading a visitor. The
point is not the distance. It is that the dataset can now be told to move.

## 3. The finding: two coordinates for Canal and Kinzie

Writing the control down as data put two numbers for the same street junction next to each other
for the first time.

| when | how | EPSG:26916 | used by |
|---|---|---|---|
| 2026-08-09 | mean of the **five** shared OpenStreetMap nodes at the crossing | E 446889.29, N 4637660.73 | the Hathaway georeference (GCP **HB**) |
| 2026-08-10 | mean of **three** shared nodes at the same crossing | E 446891.70, N 4637657.80 | the North Branch bridge's deck centreline |

**3.8 m apart, and it is not a disagreement about where Kinzie and Canal is.** It is two different
subsets of one many-noded crossing, averaged by two different pieces of work, neither of which
recorded that a choice was being made. The georeference's is the better-recorded of the two — its
node ids are committed — so `street_control.json` carries that one.

**Which subset was right is no longer an open question, 2026-08-10 (§ 7).** Two of the five
committed nodes are not Kinzie × Canal at all: `11851144367` and `11851144368` are where the
**Kinzie Street Bikeway** crosses Canal Street, about 6 m north of the roadway. The other three are
the road crossings, and their mean — E 446891.71, N 4637657.80 — is the bridge's 2026-08-10
reading to a centimetre. One reading applied a rule; the other included a cycle path.

**The bridge is not moved, and that is a deliberate decision rather than an omission.** Its deck
centreline northing is the 2026-08-10 reading. Moving it 2.93 m north onto the recorded control
would re-derive where the deck meets the traced 1834 banks, and that distance *is* the span —
71.83 m, a mesh parameter of the `bridge_timber` archetype and the one footprint dimension in
this dataset that is measured rather than assumed. Changing it stales the committed GLB and asks
for a Blender bake, which is a different slice from this one. So the record **declares the
variance** (`centreline.control_variance_m: 2.93`) and the gate checks that the declared number
is the real one. An undeclared 2.93 m would have stayed invisible; a declared one is a queued
correction with its cost written down.

## 4. The control points, and the promise that was kept for two of four

`data/sources/osm_streets_2026.json` states: *node ids are recorded per control point so every
coordinate is re-fetchable.* That was kept for the georeferencing GCPs and not for the two
intersections read later, for placements.

| control | streets | node ids | provenance |
|---|---|---|---|
| `lake_canal` | Lake × Canal | ✔ 258020603 | GCP G5 / HA |
| `kinzie_canal` | Kinzie × Canal | ✔ five ids | GCP HB |
| `lake_market` | Lake × Market (N Wacker Dr) | **none recorded** | read 2026-08-09 for the Sauganash, re-used for Hogan's store |
| `randolph_canal` | Randolph × Canal | **none recorded** | read 2026-08-09 for the Western Hotel |

The two gaps are declared in the file rather than quietly filled, and the gate requires that: a
control point with no node ids and no stated `gap` is an error. What the check can therefore
claim is precise and worth stating exactly — it verifies **the dataset against its own stated
control**, and for two of the four it cannot re-derive that control from OpenStreetMap. Owed:
re-fetch both junctions, record the ids, and reconcile any difference as a dated correction.

An attempt to re-fetch them during this slice failed — the Overpass endpoint returned 504 and
empty results for the name queries tried — so the gap is recorded rather than closed. It is not
blocking: the placements are built from these coordinates, so the check is asking the right
question of the data that exists.

**Both gaps are closed as of 2026-08-10 — see § 7, which is what the re-fetch found.**

## 5. What the check does, and what it cannot

`check_position_derivations` rebuilds every placement it can and holds the rest to a declaration.

- **`platted_corner`** — the named face of the placed footprint must stand on the named kerb of
  the named street, half a platted module from the control, plus any declared offset. Asked of
  the **rotated, placed polygon**, not of the recorded coordinate: at a facade bearing of 270 the
  recorded point is not the corner the claim is about, and the self-test's discriminating case is
  one building appearing twice, rotated onto its lot and rotated out of it.
- **`traced_waterline`** — a crossing instead of a corner. The deck's centreline comes from the
  control; its two ends must meet the traced 1834 waterline at that northing, which is what makes
  the span measured. Tolerance 0.5 m rather than 0.05, because a traced bank is a polyline and
  where it crosses a given northing depends on which vertex pair you sample.
- **`not_derivable`** — three of the nine phases, each owing a reason. No surviving street here
  (Miller House); a position stacked on another inferred position (Walker's meeting house); an
  interpolation plus a free 40 m (Wolf Point Tavern). Recording those as derivations would be the
  check certifying a guess.

**What it cannot do.** It cannot tell you the control is *right*. Since 2026-08-10 every control
point can at least be re-fetched from OpenStreetMap and re-derived from the street names (§ 7),
which is a check on the reading rather than on the town; every coordinate here still carries the
georeference's ±20 m regardless. It says the buildings stand where the dataset says it put them, and it says the
module is one number rather than five sentences. Those are both smaller claims than "the
buildings are in the right place", and neither of them was true before.

## 6. What this hands to S9

`docs/ROADMAP.md` § S9 wants street geometry **generated analytically from the plat module and
snapped to control** rather than traced. Both halves of that sentence are now committed data: the
module is `platted_street` and the control is the `control` table, with each street's axis and its
modern equivalent stated. What S9 still needs is the plat's block dimensions and extent, which are
not here — this file holds only what the placements already used.

## 7. Closing the gap, and the fault it exposed

The re-fetch that failed on Overpass succeeded against the OpenStreetMap API itself
(`api.openstreetmap.org/api/0.6`), which answers two different questions and both were needed:
`/map?bbox=` re-derives *which nodes a junction is*, and `/nodes.json?nodes=` re-fetches *where
those nodes are now*. `tools/refetch_control.py` does both — `--discover` for the first, the
default pass for the second — and it is deliberately not in `tools/check.sh`, because a commit
gate that needs the network fails offline for reasons that have nothing to do with the commit.

**The rule had to be written down before either junction could be read**, and writing it down is
most of this slice. A junction is the nodes shared by the two named **surface roadways**,
averaged — the georeference's own "multi-node crossings averaged", because a crossing of two dual
carriageways is several nodes and its centre is their mean. What was never stated is what does
*not* count: a way still under construction, a differently-named street stacked underneath (Market
Street's successor is three streets here — North Upper Wacker Drive, North Lower Wacker Drive and
a service drive below that, and only the top one is the plat's), and **bikeways and footways**,
which are mapped a few metres off the roadway they follow.

| control | re-derived | committed | drift | outcome |
|---|---|---|---|---|
| `lake_canal` | 1 node | E 446913.03, N 4637287.42 | **0.00 m** | unchanged, already recorded |
| `lake_market` | 2 nodes, 17.68 m apart | E 447161.90, N 4637285.40 | **0.04 m** | ids recorded, **nothing moves** |
| `randolph_canal` | 1 node | E 446919.60, N 4637148.50 | **4.44 m** | ids recorded, **corrected** |
| `kinzie_canal` | 3 nodes (5 committed) | E 446889.29, N 4637660.73 | **3.80 m** | correction queued, § 3 |

**`lake_market` reproduces.** Lake Street crosses both carriageways of Wacker Drive's bend, and
the midpoint of those two nodes is the committed coordinate rounded to 0.1 m. So the 2026-08-09
reading is confirmed rather than corrected, the Sauganash and Hogan's store do not move, and the
committed value keeps its rounding — adopting the two-decimal mean would shift two buildings 4 cm
for no evidential gain.

**`randolph_canal` does not, and the Western Hotel moves 4.44 m.** Randolph and Canal is a single
crossing of the two centrelines, at E 446917.46, N 4637144.61. The committed coordinate is 2.14 m
east and 3.89 m north of it, and the two streets alone cannot produce it. What produces it, to
0.04 m, is the mean of **four** nodes: the roadway crossing plus the three crossings the Canal
Street and Randolph Street bikeways make with each other and with the roadways.

That reconstruction is `inferred`, and the honest statement of the evidence is that four other
four-node subsets in the vicinity also average to within 0.12 m of the committed number — with
enough nearby nodes, arithmetic coincidences are cheap. What lifts one of them above coincidence
is that it is the only semantically coherent set (every member is a Randolph × Canal crossing of
some kind), that **the identical inclusion is visible at `kinzie_canal`**, and that a name query
written as a substring match — `Canal Street` matching `Canal Street Bikeway`, `Kinzie Street`
matching `Kinzie Street Bikeway` — reproduces exactly this at both junctions and adds nothing at
the other two, where no bikeway is mapped. One habit, two wrong coordinates, and it stayed
invisible because the ids were never written down.

The road-only reading is adopted and the Western Hotel is moved with it: 2.14 m west, 3.89 m
south, an order of magnitude inside the ±20 m the georeference already declares. Nothing about
the corner, the lot or the frontages changes. The node was last edited in May 2024, so this is a
correction to our reading, not a change in the city — a distinction the tool can now make for
every control point, because it prints each node's OSM version and edit date.

**And the gate now asks for the names, not only the ids.** A list of node ids is
*re-fetchability*: it tells you where those nodes are today. It does not tell you whether they are
the right nodes, which is the fault that actually occurred. So a control point that records ids
must also record the two modern street names in `osm_ways` — enough to re-derive the *set* — and
its lat/lon. Two new self-tests hold the rule, and the discriminating one is the second: a control point
whose ids re-fetch perfectly and whose set nobody can check is now an error.

## 8. The corridors are measured, and the 66 ft reading is out

§ 2 ended by naming the slice that would settle the width — *reading the widths off Hathaway
1834 at named streets* — and called it "a slice of research, and it is now a slice with a
single edit at the end of it." This is that slice. It ran on **both** 1834 sheets, and it
needed no edit at the end: the module stands at 80 ft.

**What was measured, and what it is a measurement of.** Not the annotation again. The
*drawn corridor* — the space between the two block boundary lines that face each other
across a street, taken centre of line to centre of line, because the platted boundary is
the line the draughtsman drew and a centroid does not care how heavily he inked it. One
traverse per sheet, starting at that sheet's own *Canal St & Lake St* control pixel and
running east–west along the block row south of Lake Street, reporting every boundary line
it crossed. `tools/measure_street_widths.py`; readings in
`data/traces/vectors/street_corridors_1834.json`.

| corridor, west to east | Hathaway 1834 | Wright 1834 |
|---|---|---|
| Desplaines | 26.49 m = **86.9 ft** | 25.83 m = **84.7 ft** |
| Jefferson | 25.50 m = **83.7 ft** | 26.34 m = **86.4 ft** |
| Clinton | 24.14 m = **79.2 ft** | 24.44 m = **80.2 ft** |
| Canal | 23.06 m = **75.7 ft** | 28.28 m = **92.8 ft** |
| centre-to-centre pitch | 116.6, 117.4, 118.8 m | 117.6, 120.5, 123.2 m |

**66 ft is excluded, and by the streets it would have had to be about.** Eight corridors,
none within 9 ft of 66, on two independently drawn sheets. And the reconciliation § 2 asked
to test — that 66 ft is the general width with the riverfront and market streets platted
wider — dies on the same reading: these four *are* the general streets of the west
division, which is precisely where a 66 ft general width would have to appear. It does not.
The dissent stays in `street_control.json` with its status changed from *worth testing* to
*excluded*, because a source is not deleted for turning out to be wrong.

**The pitch is the check that the tool is reading the map and not itself.** A street belongs
to a grid: 300 ft blocks plus one street width is 380 ft, or 116 m. Seven consecutive
spacings came out between 116.6 and 123.2 m without anything asking them to, and that is
what licenses reading the eight gaps between them as streets. It is also the only
classifier here with any force — see the limits below.

**What it does NOT settle, stated because the number is uncomfortable.** The median of the
eight is **84.8 ft**, about 5 ft *wider* than the figure this project adopts. That is not
rounded away and it is not a reason to move the module: what has been measured is the
corridor two draughtsmen drew on warped paper in 1834, and what `platted_street` claims is
what Thompson platted in 1830. The sheets' own anisotropic stretch is 3.7-4.5%, which is
3.0-3.6 ft of it; a pen line placed on the outside rather than the middle of a boundary
accounts for more. So the reading decides *which candidate* and leaves the platted figure to
the foot alone, and the grade stays `inferred` — for a different reason than before, which
the note in `street_control.json` now states.

**Alleys: consistent with 18 ft, and not settled.** Three alley gaps came out 5.21, 5.31 and
5.70 m — 17.1, 17.4 and 18.7 ft. The dissent's 16 ft is 4.88 m. The nearest reading is 0.33 m
above it, and this method's error is larger than that, so the alley figure is *not* decided
here. Nothing in the dataset uses it.

**What this cannot do, and the half of the reading that was thrown away.** A second traverse
ran north–south along Canal to measure the E-W streets, and it is not committed. On the
Wright sheet it reads **lot lines**, and every test that separates a lot line from a street
on the Hathaway sheet fails there: Wright's lot depths are 20-26 m, which is a platted
street's width; a lot line runs as far as a block face does, because the line at the same
depth continues in the column across the alley; and two of its spacings land inside the
module band by arithmetic coincidence. Rather than tune a filter until the answer looked
right, that traverse was dropped and the module rests on the N-S streets. So this file still
has no measurement of Lake, Randolph, South Water or Market — which is also what S9 wants
next, and it will need a method that identifies a corridor by something other than its
width.

Two smaller things worth carrying, both of which cost a run of the tool to learn: a traverse
may not run down the street it is measuring (block faces stop at the kerb, so a pass along a
corridor crosses nothing but the street's own name), and it may not run down the mid-block
alley either (an alley is a blank corridor whose crossing lot lines stop at its kerbs and
whose mouths break the faces at both ends — a traverse in one reads two hundred metres of
paper and no streets). The tool offsets a quarter of the measured block pitch for that
reason, and the reason is in its docstring so the next reader does not rediscover it.

## 9. And the control point it was standing on is inside a block

The traverse starts at the sheet's own *Canal St & Lake St* ground-control pixel, and the
first thing it printed is that this pixel is not on Canal Street.

| sheet | GCP | recorded pixel | on the Canal centreline | apart |
|---|---|---|---|---|
| Hathaway 1834 | HA | 1122, 2218 (working) | 1204, 2219 | **52.4 m** |
| Wright 1834 | G5 | 1197, 1955 (resource) | 1226, 1956 | **20.2 m** |

**Both sit inside block 28**, west of the corridor, and the sheets say so themselves: the
block number *28* is printed straddling each of them, and a block number is never printed in
a street. The corridor 52 m east of HA is the one Hathaway letters `Canal.`; the one 20 m
east of G5 is the gap between blocks 28 and 29, with `West` — West Water Street — a further
block beyond it. Both readings appear to have taken **block 28's mid-block alley** for the
street: the alley pair on the Hathaway traverse measures 5.2 m and sits 6 m from HA.

**What this is not.** It is not a claim that Canal and Lake is somewhere else. The modern
junction is a well-recorded coordinate with its node ids committed (§ 7). It is a claim about
where that junction was *pointed at* on two 1834 sheets, which is a different kind of
mistake and the kind a georeference is made of.

**What it costs, computed rather than argued.** Wright's G5 is one of the eight points
`data/datum.json` is fitted from. Refitting the Wright control with G5 moved onto the
corridor centreline — and nothing else changed — moves the datum origin **15.0 m** (dE −15.0,
dN +0.2) and leaves the fit RMS at 17.5 m. That is the whole exposure, and it is inside the
±20 m the project already declares as its working uncertainty.

**It is queued and not adopted, deliberately.** Moving the origin re-derives every coordinate
in the dataset and stales every committed mesh, which is a Blender bake and a whole-dataset
review, not a slice. `datum_exposure` in the corridor file carries the figure with
`status: "queued, not adopted"`, and `check_street_module` pins both the offset and the
exposure to the GCP pixels they were computed from — so the day either correction is adopted
the gate fails until the sheets are read again. A finding whose inputs have moved is not a
finding.

**Two limits on the finding itself.** The correction measured is *across* Canal Street only:
whether HA and G5 sit at the right northing — whether the row they are in is Lake Street — is
a separate reading and is untouched here. And three of the five Hathaway points and seven of
the eight Wright points have not been checked this way at all. HC (State & Madison) was
looked at by eye and appears to be in its corridor; the rest are unexamined, and the same
method would examine them.

## 10. The E-W streets, and the test that could read them

§ 8 ended by naming what the other half of this reading would need: *a method that identifies
a corridor by something other than its width*. This is that method, and the three tests it
replaces are worth restating, because all three are readings taken **across** a candidate at
one place — its width, the length of the two lines bounding it, and whether its neighbours
are a block pitch away. On the Wright sheet a strip of lots passes all three: the depths are
20–26 m, which is a platted street's width; the bounding lines run as far as a block face
does; and two spacings land inside the module band by arithmetic coincidence.

**So the new test turns ninety degrees and asks what a candidate does along its own length.**
A platted street corridor is open ground from one cross street to the next — the block faces
bounding it stop at the kerb, so for a whole block nothing is drawn across it. A strip of lots
is the opposite: the lots inside a block are divided from each other by lines that cross the
strip every few metres, and the strip ends at the block face. `clear_run` follows a
candidate's own centreline 350 m each way, over a band 35% of its width (inside both boundary
lines), and reports the longest unbroken run of paper. **The threshold is derived, not
chosen**: the shortest block face the module band allows is its loosest pitch less its widest
street, 95 − 30 = **65 m**. Move the module band and the threshold moves with it. It is
deliberately the loosest such figure, because the test is there to exclude what cannot be a
street rather than to select what looks like one.

**The separation is not marginal.** On the Wright N-S traverse:

| | longest clear run |
|---|---|
| the three corridors kept | 213.5, 244.8, 287.4 m |
| the ten candidates rejected | 42.3 – 60.5 m |

No overlap, and a factor of 3.5 between the groups. The rejected ten break at about 45 m,
which is half a block — the lot line the strips are chopped by. **And the test costs nothing
on the readings already committed**: run against the four settled N-S corridors on each sheet
it rejects none of them, with clear runs of 201–677 m. A filter that had quietly killed the
existing measurement would have been the wrong filter.

**What came out.** Three E-W corridors, all on Wright:

| corridor | width | clear run | named by |
|---|---|---|---|
| **Lake Street** | 24.20 m = **79.4 ft** | 287.4 m | `lake_canal` + `lake_market`, 0.9 m away |
| **Randolph Street** | 24.85 m = **81.5 ft** | 244.8 m | `randolph_canal`, 0.9 m away |
| unnamed, one block further south | 26.37 m = **86.5 ft** | 213.5 m | — no committed junction |

**The names are measured too, not counted.** A corridor takes a street's name only if that
street's committed modern junction(s), projected onto the traverse through the sheet's own
affine, land within half the module's loosest pitch (47.5 m) of its centreline — the distance
at which the next corridor along would be the better match. Lake and Randolph come in at 0.9 m
each. The third corridor is Washington Street by the plat's own order, and it stays **unnamed
in the data** because this project has no committed junction for it: the inference is in this
paragraph, where a reader can see it, and not in a file where it would read as a reading.
`check_street_module` re-derives every identification offline on every commit from the
corridor's committed centre pixel, the traverse's ground axis and `street_control.json`.

**And it answers the question § 9 said it could not.** That section closed by recording a
limit: the correction it priced is *across* Canal Street only, and whether G5 sits at the
right northing — whether the row it is in is Lake Street — was untouched. The N-S traverse
crosses Lake, so it can see exactly that, and its t is measured from the recorded pixel's own
position along that axis. **G5 lies 3.4 m south of the Lake Street corridor's centreline.**
So the 20.2 m correction the file prices really is one coordinate and not two, which was an
assumption and is now a reading.

**Four things this does not settle, stated because they are the interesting half.**

1. **Hathaway reads nothing here.** Its N-S traverse finds two candidates and no two of them
   are a block pitch apart, so the module test demonstrates nothing and the traverse commits
   nothing. (Fixing this exposed a real fault in the tool: with a single candidate the chain
   search kept it for having been found first. A chain of one is not a chain, and it is now
   rejected like any other unsupported candidate.) **The E-W widths therefore rest on one
   sheet** and are not cross-checked the way the N-S four are.
2. **Hathaway's Canal corridor now fails to be named**, at 50.1 m against the 47.5 m
   tolerance. This is not a second opinion about § 9 — it is the same 52 m seen from the other
   side. The GCP and the modern junction agree with each other and disagree with the drawn
   corridor, so no independent naming supports the corridor Hathaway letters `Canal.`; on that
   sheet the four N-S corridors keep the names the *sheet* gives them and nothing more.
3. **The blocks are not square, and the arithmetic that fits the N-S streets does not fit
   these.** The two E-W spacings measure 134.4 and 135.6 m against 116.6–123.2 m between the
   N-S streets; the modern junctions put Lake to Randolph at Canal 142.9 m apart, 5% more,
   which is this sheet's stretch. A 300 ft block plus an 80 ft street is 116 m, so 135 m is a
   block of about 363 ft in the N-S direction. That is a finding for S9's block dimensions and
   it is **not** turned into a figure here: one traverse's two spacings on one sheet is not a
   plat.
4. **South Water and Market are still unmeasured.** Market's junction projects 227.7 m from
   the nearest corridor either traverse measured on Wright and 192.0 m on Hathaway, so it
   lies outside what these passes read. North of Lake, where South Water belongs, the
   traverse crosses three candidates and all three are rejected for the same reason — one of
   the two lines bounding them stops after 24–32 m, well short of a block face. Both streets
   need a traverse placed for them, not a looser filter.
