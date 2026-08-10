# The lake shore, the harbour reach and the sand bar — how they were traced

**Traced:** 2026-08-10 · **Epoch:** `e1834_harbor_cut` · **Extent:** local E +314 … +1570,
N −589 … +505 · **Tool:** `tools/trace_shoreline.py` · **Output:**
`data/terrain/epochs/e1834_harbor_cut/shoreline.geojson`

This is ROADMAP **S2e parcel (a)** — the vectors the eastern terrain extension needs. It
carries no elevations and builds no ground; the terrain box still stops at local E +320.
What it settles is the question that had to be settled first: **where the 1835 water ended.**

## Why the shore could not simply be drawn

Everything east of roughly Michigan Avenue is later landfill, much of it fire debris after
1871. The modern coast is about a kilometre east of the 1835 one at the river mouth, so
tracing today's shoreline into an 1835 dataset would have been the single largest false claim
in it — and it would have looked like diligence. The shore has to come off the same 1834
sheet as everything else, through the same affine, carrying the same ±20 m.

## What was traced, and how

Same sheet, same transform, same wash convention as the forks: Wright draws water as a grey
wash band on the water side of a black bank line. Two things differ, and both are recorded in
the tool because they are the reason it is a second tool rather than a wider window.

1. **The background statistic.** The forks trace measures "darker than paper" against a local
   64-px block, which is what lets it find a 70 m channel inside a town of coloured ward
   washes. Lake Michigan is washed as a band a couple of hundred metres wide, and against a
   local background a band that wide *is* its own paper — the interior reads as unshaded and
   only the two edges survive. This trace measures against the whole window instead. That is
   the right answer here and the wrong answer at the forks.
2. **The sand bar is a hole.** The water body is one connected thing — main stem, the 1834
   cut, the old southward channel, the lake margin — and the bar is the island it runs round.
   So the bar comes out of the segmentation as a hole in the water, which is exactly what it
   is on the map, and it is carried as the water polygon's interior ring.

Six numbers are hand-placed on the scan and nothing else is: three seeds that pick the water,
and two anchors that claim a boundary run for a name. A run no anchor claims within 60 px is
not written.

## What came out

| feature | form | extent (local m) | confidence |
|---|---|---|---|
| `harbor_reach_water` | polygon + 1 interior ring | E 314…1574, N −589…503 | `inferred` |
| `sand_bar_1834` | polygon, 44 vertices, 1.5 km perimeter | E 1305…1498, N −436…225 | `inferred` |
| `south_shore_harbor_reach` | line, 102 vertices, 2 466 m | E 314…1257 | `inferred` |
| `north_shore_harbor_reach` | line, 57 vertices, 1 568 m | E 314…1464 | `inferred` |

`inferred`, not `documented`, for the same reason the forks river polygon is: a cadastral plat
is not a hydrographic survey, and the georeference is good to tens of metres, not to the metre.

## The cross-check that came free

The two traces overlap by 80 m — this window's west edge is at local E +314 and the forks
window's east edge is at E +398 — and they were produced by different segmentation settings in
different windows. In the overlap they agree to **0.1–5.7 m on the south bank and 0.5–1.3 m on
the north**, against a ±20 m georeference uncertainty. That is not proof the line is where the
river was; it is proof the segmentation is measuring the draughtsman's line rather than its own
parameters, which is the part that was worth checking.

## What is deliberately not in the file

- **The lake east of the traced shore.** Two boundary runs were found, reported and dropped:
  the outer edge of the lake wash in the north-east (272 m) and a second in the south-east
  behind the bar (823 m). Neither is a shore — they are where the draughtsman stopped washing.
  Nothing in this file describes the lake beyond the traced edge, and the water polygon's
  eastern boundary is the window, not a coast.
- **Any elevation for the bar.** A sand bar is a surface that a couple of feet of lake stage
  moves, no source gives its height, and inventing one to make it render would be exactly the
  kind of quiet gap-filling `AGENTS.md` forbids. Elevations are argued for in
  `terrain_spec.json` or not at all.
- **The piers.** Wright draws the 1834 cut as a straight channel between two pier lines, and
  between them the traced boundary is the pier's inner face as drafted — not a natural shore.
  The feature says so in its own `note`. Piers are structures with phases (`docs/EPOCHS.md`),
  so their alignment is not a terrain claim and they are not modelled here.
- **South of about N −580.** The trace leaves the window there. The old southward channel and
  the shore continue; they are not traced, and the geometry stops rather than being extended
  by eye.

## What this settles for the terrain extension

Measured, rather than estimated:

| | local E |
|---|---|
| current terrain box east edge | +320 |
| mainland shore, at its most eastward (the fort reservation) | **+1257** |
| sand bar, east edge | **+1497** |
| traced window east limit | +1570 |

So ROADMAP S2e's proposed **E +1500** box is confirmed as the right order of magnitude but is
about 3 m from clipping the bar. **+1560** is the number to use — it takes the whole bar and
stops inside the traced evidence rather than past it.

Two consequences for parcel (b), the heightfield:

- The bar is **land inside the water**, so the "distance from the waterline" rule that builds
  the forks terrain needs a signed distance that understands islands, not just banks.
- The extension roughly triples the modelled area. At the current 2.5 m cell that is ~213k
  samples (~425 KB int16); the evidence east of the built blocks does not support 2.5 m detail,
  so a coarser cell out there is worth considering — but that is a resolution decision, not a
  provenance one, and it belongs with the terrain spec.

## Re-running it

```
pip install numpy scipy pillow pyproj
python3 tools/trace_shoreline.py            # rewrites the GeoJSON
python3 tools/trace_shoreline.py --check    # re-traces and diffs against what is committed
python3 tools/trace_shoreline.py --debug    # + a PNG overlay of water, island and runs
```

Like the forks trace and the datum re-derivation, it is **not** in `tools/check.sh`: it needs
the network and three libraries the gate deliberately does not require. The IIIF region's
sha256 is recorded in the output, so the input is pinned even though the fetch is not.
