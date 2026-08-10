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

**What it cannot do.** It cannot tell you the control is *right* — `lake_market` is unverifiable
against OpenStreetMap today (§ 4) and every coordinate here carries the georeference's ±20 m
regardless. It says the buildings stand where the dataset says it put them, and it says the
module is one number rather than five sentences. Those are both smaller claims than "the
buildings are in the right place", and neither of them was true before.

## 6. What this hands to S9

`docs/ROADMAP.md` § S9 wants street geometry **generated analytically from the plat module and
snapped to control** rather than traced. Both halves of that sentence are now committed data: the
module is `platted_street` and the control is the `control` table, with each street's axis and its
modern equivalent stated. What S9 still needs is the plat's block dimensions and extent, which are
not here — this file holds only what the placements already used.
