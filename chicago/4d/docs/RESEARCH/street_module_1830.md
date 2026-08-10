# The platted street module, and the control every placement stands on

**Record:** none — this is a memo about a *method*, not about a building ·
**Data:** `data/traces/street_control.json` · **Gate:** `check_position_derivations`
in `tools/validate.py`

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

**Why it is `inferred` and not `documented`.** The annotation has not been read street by street.
This dataset applies one town-wide figure to Lake, Market, Canal, Randolph and Kinzie, and a
town-wide figure taken from an annotation is a reading rather than a measurement of each of those
five streets. That is exactly the shape `inferred` is for, and the note in
`street_control.json` states the reasoning as the confidence model requires.

**The reconciliation worth testing**, carried forward from `hogan_store.md` § 5: the two figures
may not be about the same streets — 66 ft general, with the riverfront and market streets platted
wider. Reading the widths off Hathaway 1834 at Lake, South Water and Market specifically settles
it. That is a slice of research, and it is now a slice with a single edit at the end of it.

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
