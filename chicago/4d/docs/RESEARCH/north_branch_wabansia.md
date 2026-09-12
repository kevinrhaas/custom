# The North Branch north of the forks window — what was traced, and what was not

**Traced:** 2026-09-12 · **Ticket:** T-1072 (the north half of T-0794) · **Epoch:**
`e1834_harbor_cut` · **Tool:** `tools/trace_north_branch.py` · **Output:**
`data/terrain/epochs/e1834_harbor_cut/branches.geojson`

Re-derivable end to end:

```
python3 tools/trace_north_branch.py            # re-trace and write
python3 tools/trace_north_branch.py --check    # re-trace and diff against committed
python3 tools/trace_north_branch.py --debug    # + a PNG overlay of the trace
python3 tools/trace_north_branch.py --check-properties   # the offline half; check.sh runs it
```

---

## 1. What was missing

`tools/trace_river.py` traces the forks inside a 1120 px window of the BPL master scan of
J. S. Wright's 1834 survey. T-1071 carried the South Branch out of the bottom of that window
to the School Section's south line. The North Branch had the same hole at the other end: the
committed water stopped dead on the forks window's **north** edge, map row 1252, a little
north of Kinzie Street — and everything Wright draws above that row, the whole length of the
river through Wabansia, was not in the project at all.

That is the reach the town looks at. Wabansia's river-front water lots — Kain's and Hight's
subdivision, the lots numbered 6 to 19 on the sheet — front on this water, and until now they
fronted on nothing.

## 2. A fourth window, and where the splice is

Same argument as the third, mirrored. `trace_river.py` finds a 70 m channel in a town of
coloured ward washes by working at a LOCAL block percentile, so enlarging its window would
move every vertex the forks trace has already committed — and the terrain is carved from
those vertices. So this is a separate window whose **south edge is the forks window's north
edge**:

| | window (resource px of the BPL master, 4204 × 5166) |
|---|---|
| forks (`trace_river.py`) | x 868, y 1252, 1120 × 1120 |
| **North Branch (this trace)** | **x 640, y 0, 780 × 1252** |
| South Branch (`trace_south_branch.py`) | x 1150, y 2372, 800 × 2578 |

Row 1252 is a line both tools name, not a tolerance either of them hopes for.
`river.geojson` is neither read nor rewritten here, and `trace_north_branch.py` asserts
`trace_river.REGION[1] == 1252` before it segments a pixel, so moving the forks window breaks
this trace loudly instead of quietly unsticking the splice.

**How well the two polygons actually meet**, measured on the splice row against Wright's own
inked bank lines (at row 1251 the ink stands at x 1120–1122 and x 1234–1237):

| | west bank | east bank |
|---|---|---|
| committed forks polygon | x 1124 — **2.1 m** east of the ink | x 1247 — **8.2 m** east of the ink |
| this trace | x 1117 — **2.8 m** west of the ink | x 1188 — **33.8 m** west of the ink |
| the two polygons' disagreement | **4.9 m** | **60.1 m** |

The west side of the splice is as good as the sheet allows. The east side is not, and § 5
says what it is and what it is not.

## 3. The setting that had to change: green and grey, thirteen units apart

The forks settings carry north unchanged except one — `hue_tol`, 11 → 7.

`wash_mask` separates Wright's grey bank wash from his coloured ward washes by how far a
pixel's hue departs from the LOCAL paper's. On Wabansia's river front that separation is the
narrowest it is anywhere on this sheet. Medians over a 13-row band at map row 745, across the
west bank:

| | R−B | G−B |
|---|---|---|
| green wash on the river-front lots | 27 | **31** |
| grey bank wash beside it | 32 | **19** |
| paper of the channel between the banks | 40 | 26 |

One channel, thirteen units, and a tolerance of 11 swallows it. This is not a rounding error
in the result. At `hue_tol` 8 the traced west bank steps **131 px — 93 m — into the lots** at
map row 800, and the polygon published as river would have covered ground Wright drew as
platted lots with lot lines ruled across it. That is a categorical mistake, not a graded one:
a reader of `branches.geojson` cannot tell a bank the tool got 93 m wrong from a bank Wright
drew there.

Going the other way, at `hue_tol` 5 the upper reach's own bank wash starts leaving with the
colours and the trace breaks at row 764 — the channel comes out in two pieces and the seed
keeps only the southern one. **The whole usable band is `hue_tol` 6 and 7**, which is why the
value is argued from the pixels in the table above rather than tuned to a pretty picture. 7 is
taken because 6 sits one step from the break.

This is the third time the hue reference has been the thing that mattered and the second time
it decided a reach: T-1071 moved `hue_block`/`hue_pct` because the School Section's yellow
reservation wash was standing in for paper. There the reference was wrong; here the reference
is right and the tolerance around it was too loose. Both are the same fact about this sheet —
Wright's washes are close to his paper and to each other, and the segmentation is only ever as
good as the local statement of what paper is.

## 4. What is published, and at what grade

Three features, all `inferred`, all sourced to `wright_1834`:

| id | what |
|---|---|
| `north_branch_wabansia` | the water polygon — 64 ring vertices, **4.8 ha** |
| `north_branch_west_bank` | Wabansia's river front — **799 m**, 31 vertices |
| `north_branch_east_bank` | the unplatted ground east of the river — **782 m**, 30 vertices |

Drafted channel width at the seed: **62.6 m (205 ft)**, against the forks trace's own 72.9 m for this
reach inside its window, 69.7 m for the main stem and 57.3 m for the South Branch, and 49.7 m
for the South Branch up in the School Section. The branch narrows as it leaves the forks, which
is what the sheet draws; no gauging record is claimed for it.

**No bed depth is claimed here at all**, and `--check-properties` fails if one ever appears.
A cadastral plat gives planform and not soundings; the water surface is flat at the datum for
the same reason the forks are, because the pre-reversal river had a near-zero surface gradient
and stood at lake level through this reach. **No crest heights** either: north of the modelled
terrain box there is no heightfield for a crest to belong to.

## 5. The east bank, where it is short — stated, not smoothed

`hue_tol` 7 buys the west bank at a price on the east one. Measured per row against Wright's
inked east bank over all 932 rows of the reach, this trace's east boundary sits a median
**1.4 m** inside the ink, p90 **8.5 m** — and is short of it by more than 10 m on **81 rows**,
in exactly two places:

* **rows 728–779** (~37 m of the reach), where the east bank wash thins against the paper;
* **rows 1222–1251**, the last 30 rows — which is the splice, and is the 33.8 m in § 2.

At `hue_tol` 11 the east bank is better (median 0.7 m, 34 rows over 10 m) and the west bank is
93 m wrong. The trade was taken deliberately and in one direction: a bank that is short is a
bank drawn inside water that is really water, and a bank that has leaked is lots drawn as
river. Nothing here is graded up to cover it — the water polygon carries `uncertainty_m: 20`
like its neighbours, and the two short stretches exceed it. **Filed as T-1078** rather than left in a note,
because the fix is a reading of the east bank wash and not a parameter.

## 6. What the northern end is

Wright ruled a line across the top of his survey and washed the river up to it. The channel's
north end at map row 309 is therefore **where he stopped drawing, not where the river stopped
running**: the North Branch ran on north for miles, to the Skokie marshes, past anything on
this plat. The terminal stretch is dropped from both bank lines for exactly the reason
T-1071's southern one is — publishing it would assert a river end this sheet never drew — and
it cannot be told by the ink, because at this terminus there IS a line: the survey's own north
boundary, drawn across the channel. Six ring vertices come off, three on the splice row and
three on the survey limit, and the trace prints both counts on every run.

## 7. What this unblocks

* Wabansia's water lots (T-1069) get the water they front on. Until now the lot strip's river
  side was a boundary with nothing on the other side of it.
* The two branches now run from the sheet's north margin to the survey's south line in one
  connected chain of three polygons, which closes **T-0794** — both halves of it.
* `validate.py`'s waterline crossings already read every polygon in `branches.geojson`
  (T-1071), so a face that ends on the North Branch now meets a bank that exists.

## 8. What was NOT done

* **No terrain.** The heightfield box stops far south of here; this is planform only.
* **No bathymetry, no crests, no revetment**, and no claim about the bank's material.
* **Nothing east of the river.** The unplatted ground Wright washes salmon on that side is a
  tract question (T-0792), not a water one.
