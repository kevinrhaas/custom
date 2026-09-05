# The Thompson plat georeferenced, and its water measured against Wright's

**Investigated:** 2026-09-05 · **Ticket:** T-0685 (piece 2 of 2 of T-0453) ·
**Epoch:** `e1834_harbor_cut` · **Record:** none — this is a memo about a *measurement* ·
**Source:** `thompson_plat_1830`, through the copy of the sheet held in this repository at
`chicago/pre_fire_v1/maps/images/1830_thompson_plat.png` (2728 × 1944) ·
**Data written:** `data/traces/gcp/thompson_1830_gcps.json`,
`data/traces/vectors/thompson_1830_forks_banks.json` ·
**Data read, not written:** `data/terrain/epochs/e1834_harbor_cut/river.geojson` ·
**Generator:** `tools/trace_thompson_forks.py` (`--check` re-derives, `--measure` reprints
every figure below) · **Gate:** `tools/check.sh`

---

## 1. The question, and why it needed a run of its own

T-0453 recorded a source conflict rather than an error: every bank in the model is traced
from **Wright 1834**, the owner read the **1830 Thompson plat** and saw the river borders
drawn differently at Wolf Point, and the file itself declares a drafting tolerance of about
±20 m. Two committed-quality sources disagreeing inside a declared tolerance is not a defect;
it is a measurement nobody had taken.

It could not be taken, because the plat had never been fitted to the frame the datum was
fitted in. `data/traces/gcp/` held Wright 1834 and Hathaway 1834 and nothing for Thompson, and
`data/sources/thompson_plat_1830.json` has carried a standing instruction since it was written:
*read for its stated figures, never traced for geometry*. **That rule is not revoked here.**
What is added is a transform, so that the plat's drawn banks can be *compared* in metres. The
output of this ticket is a number, not a planform; `data/terrain/` is untouched.

## 2. The georeference — 22 control points, RMS 4.5 m

`tools/trace_thompson_forks.py` fits an affine pixel → EPSG:26916 from twenty-two street
junctions the plat draws and the modern city kept: Franklin, Wells, La Salle, Clark and
Dearborn against Lake, Randolph and Washington in the South Division, and Clinton and Canal
against Fulton, Lake, Randolph and Washington in the West Division. Each modern junction is an
OpenStreetMap node set, surface roadways only, multi-node crossings averaged, **node ids
recorded so every coordinate is re-fetchable** — the rule `osm_streets_2026.json` states and
`tools/refetch_control.py` enforces for the placement control.

| | |
|---|---|
| control points | 22, spanning x 567–2436 and y 828–1624 of the sheet |
| **RMS residual** | **4.48 m** |
| worst point | 10.14 m (Washington & Canal) |
| best point | 0.94 m (Washington & Clark) |
| scale | 0.5253 m/px in x, 0.5286 m/px in y |
| rotation | 0.927° |
| axis-scale difference | 0.63 % |

**The pixels are not picked by eye, and that is the part worth explaining.** A street corridor
on this sheet is 80 ft and so is a lot, so along either axis the block faces and the lot lines
form one uniform comb and no spacing rule can tell them apart. What separates them is that the
lines running the *other* way **stop at a street and cross a lot line**. So a block face is
followed across the sheet by a local peak-tracker, a run of failed ink is a street crossing,
its centre is the corridor centre, and the perpendicular corridor's centre is the mean of the
two faces that bound it *evaluated at that crossing* — which carries the sheet's rotation and
local stretch instead of averaging them away.

**One free check fell out of it.** The Lake & Canal junction the tool discovers is OSM node
258020603, which is exactly the node `data/traces/street_control.json` commits as
`lake_canal`, to 0.00 m. The junction rule used here is the project's own.

### 2a. This sheet fits better than either 1834 sheet, and that is not a compliment to it

Wright 1834 fits at RMS 17.5 m with a 32.7 m worst point and 3.7 % anisotropy; Hathaway 1834
at RMS 17.7 m. Thompson fits at 4.5 m with 0.63 % anisotropy. **That is a statement about
draughting, not about survey.** A plat is a ruled grid, and a ruled grid matched to the modern
grid it became will close tightly wherever the modern street kept the platted line. It says
nothing at all about the freehand water inked on the same sheet — which is why every figure in
§ 4 is reported with the fit's residual standing beside it.

It does dispose of one worry. The sheet has a visible centre fold, and § 3 of
`thompson_plat_sloughs.md` fitted only the east–west axis and warned that anything read across
the fold was worth less than its residuals. A 4.5 m two-axis fit over both divisions says the
fold is not moving the grid by anything that matters at this scale.

## 3. What the plat draws at the forks, and one line that is not a bank

Six lines were followed from the ink and are committed in
`data/traces/vectors/thompson_1830_forks_banks.json`, in sheet pixels *and* EPSG:26916 *and*
local ENU — the pixels because they are the evidence, the metres because they are the
derivation.

| line | what it is |
|---|---|
| `north_branch_east_bank` | freehand. The plat draws **one** line up this reach; it says nothing about the North Branch's west bank here. |
| `main_stem_north_bank` | freehand, from the point of land at the forks to the corner where the bank turns east under the North Division blocks. The trace stops at that corner. |
| `south_branch_west_bank` | freehand. *West Water Street* is lettered in the corridor between this line and the block faces west of it, so the line is the street's east side, which is the bank. |
| `main_stem_south_bank` | freehand. |
| `south_branch_east_bank` | freehand. |
| **`wolf_point_nw_shore`** | **not a bank.** North-west of the forks the plat gives the water's edge as a **ruled straight line lettered with its own bearing** — the sheet reads *North 51° West* — which is simultaneously the north-east boundary of West Division blocks 22 and 29, drawn cut by the river. |

That last row is the reading this memo would most like the next reader to keep. A ruled
boundary and a drawn bank are different kinds of statement: one is where the surveyor put the
line, the other is where he thought the water was. Comparing the ruled line against a traced
bank is comparing two different claims, and its numbers in § 4 are reported with that said
rather than folded into an average.

## 4. The measurement (T-0453 acceptance 2, T-0685 acceptance 3)

Local ENU metres, origin `data/datum.json`. A bank running east–west is read at named
**eastings**; a bank running north–south at named **northings**. A positive delta means the
plat's line is further north (E cuts) or further east (N cuts). `nearest` is the distance from
that plat point to the nearest point on the Wright shore, which is the axis-free statistic.
Reproduce with `python3 tools/trace_thompson_forks.py --measure`.

**Main stem, north bank** — the plat is north of Wright, by less each step east:

| E | plat N | Wright N | delta | nearest |
|---:|---:|---:|---:|---:|
| +25 | 5.6 | −11.4 | **+17.0** | 15.9 |
| +50 | 15.9 | 3.4 | +12.5 | 10.3 |
| +75 | 27.9 | 20.4 | +7.5 | 6.2 |
| +100 | 45.7 | 37.4 | +8.2 | 6.8 |
| +125 | 61.1 | 56.6 | +4.5 | 3.3 |

**Main stem, south bank** — the plat is south of Wright:

| E | plat N | Wright N | delta | nearest |
|---:|---:|---:|---:|---:|
| +100 | −85.6 | −66.7 | −18.9 | 15.3 |
| +125 | −56.9 | −31.5 | **−25.3** | 15.6 |
| +150 | −34.2 | −11.5 | −22.7 | 18.3 |
| +175 | −14.3 | 4.1 | −18.4 | 17.0 |
| +200 | 2.8 | 13.5 | −10.6 | 9.9 |
| +225 | 16.0 | 22.8 | −6.8 | 6.4 |

**North Branch, east bank** — the plat is *west* of Wright, which gives the North Division
**more** ground, not less:

| N | plat E | Wright E | delta | nearest |
|---:|---:|---:|---:|---:|
| +150 | −65.5 | −31.0 | **−34.6** | 34.6 |
| +200 | −62.5 | −37.4 | −25.1 | 24.9 |
| +250 | −59.3 | −44.2 | −15.1 | 14.9 |

**South Branch, west bank — Wolf Point.** The largest disagreement on the sheet, and it grows
southward:

| N | plat E | Wright E | delta | nearest |
|---:|---:|---:|---:|---:|
| −200 | −16.3 | 3.6 | −19.9 | 19.7 |
| −250 | −21.0 | 2.9 | −23.9 | 23.9 |
| −300 | −28.5 | −0.7 | −27.9 | 27.8 |
| −350 | −35.5 | −3.9 | **−31.5** | 31.5 |

**South Branch, east bank** — the two sheets are the same line:

| N | plat E | Wright E | delta | nearest |
|---:|---:|---:|---:|---:|
| −150 | 71.9 | 72.0 | −0.2 | 0.1 |
| −200 | 58.4 | 58.2 | +0.2 | 0.1 |
| −250 | 48.2 | 49.6 | −1.3 | 1.3 |
| −300 | 38.8 | 46.6 | −7.9 | 7.8 |
| −350 | 31.7 | 41.5 | −9.8 | 9.7 |

**The forks' north-west shore** — the ruled *North 51° West* line of § 3, against Wright's
West Division shore. Reported, not averaged with the rest:

| E | plat N | Wright N | delta | nearest |
|---:|---:|---:|---:|---:|
| −75 | −64.6 | −30.3 | −34.3 | 18.6 |
| −50 | −83.6 | −63.3 | −20.3 | 15.2 |
| −25 | −97.4 | −81.2 | −16.2 | 13.8 |

Whole-line, every traced vertex to the nearest point on the matching Wright shore:

| reach | min | median | max | vertices |
|---|---:|---:|---:|---:|
| South Branch, east bank | 0.1 | **2.2** | 9.9 | 108 |
| main stem, north bank | 0.2 | **6.6** | 16.3 | 77 |
| main stem, south bank | 0.3 | **12.9** | 18.8 | 78 |
| the forks, NW shore (ruled) | 12.8 | **20.2** | 25.7 | 80 |
| North Branch, east bank | 3.3 | **24.8** | 35.3 | 102 |
| South Branch, west bank | 19.4 | **26.1** | 38.7 | 82 |

## 5. What the numbers say, and the two things they do not

**Three reaches are inside the ±20 m the file declares, and three are outside.** The South
Branch's east bank is not a disagreement at all — 2.2 m median across 108 vertices is two
independent readings of the same line, four years and two draughtsmen apart, and it is the
strongest corroboration this project has that either georeference is sound. The main stem's
north bank (6.6 m) is inside. The main stem's south bank (12.9 m median, −25.3 m worst) sits on
the line. Wolf Point's west bank (26.1 m), the North Branch's east bank (24.8 m) and the ruled
north-west shore (20.2 m) are outside it.

**The owner's reading is confirmed in fact and reversed in direction at one place.** The
disagreement *is* at Wolf Point and the forks, exactly where it was reported. But at the North
Branch the plat gives the North Division **more** dry ground than the model does, not less: at
N +150 the plat's bank stands at E −65.5 where Wright's stands at E −31.0. `north_water`'s west
end is at E −30, which under Wright sits on the bank and under Thompson sits 35 m inland.
**This memo does not settle T-0447** — that ticket asks about a street, and a street has its own
sources — but T-0447's premise, that the plat does not give North Water Street its ground, is
not what the plat measures out to say at this latitude, and it should be re-read before it is
worked.

**Two things these numbers do not establish.**

1. **They are not larger than Wright's own georeference error.** The committed banks were fitted
   at RMS 17.5 m with a 32.7 m worst point. A 20–30 m disagreement is between one and two
   residuals of the transform the committed line was carried through. It is real, it is
   systematic, and it is not, on this evidence alone, outside what the Wright fit can produce
   by itself. The Thompson fit's own 4.5 m is the smaller half of that budget.
2. **They do not say which sheet is right.** Wright 1834 is four years later and is a survey of
   what was there; Thompson 1830 is the town as laid out, and at Wolf Point the thing it lays
   out is a *lot boundary against the water*, which a surveyor may well have ruled to the
   convenient line rather than to the wet one. The § 3 finding — that the north-west shore is a
   ruled bearing and not a drawn bank — cuts directly against reading the plat as the better
   witness there.

## 6. What this reading refuses

- **Nothing moves.** `data/terrain/epochs/e1834_harbor_cut/` is read and not written. T-0453
  acceptance 4 and T-0685 acceptance 5 both say so, and moving a bank re-derives every
  waterline test in the project.
- **No geometry is committed from the plat into the model.** The traced lines live in
  `data/traces/vectors/` with `asset_use: measurement`, and `thompson_plat_1830` keeps
  `asset_use: inventory` and its standing rule.
- **No grade moves and no confidence is upgraded.** The committed banks stay `inferred` on
  `wright_1834`.
- **It does not rule on the planform of record.** That is T-0685 acceptance 4 and it is the
  owner's, with § 4 in front of it.
