# Datum derivation memo — the Wolf Point origin

**Derived:** 2026-08-09 · **Status:** `data/datum.json` `verified: true` ·
**Re-derivable:** `python3 tools/rederive_datum.py --print` reproduces every number below from
the committed traces, and `tools/check.sh` fails if it ever stops matching.

## Result

| | |
|---|---|
| **Origin** | the centre of the Chicago River forks at Wolf Point, as drawn on Wright 1834 |
| **EPSG:26916** | E **447072.7**, N **4637395.8** |
| **WGS84** | 41.886721, -87.637951 |
| **Fit quality** | RMS 17.5 m over 8 control points (max 32.7 m) |
| **Cross-checks** | independently georeferenced Hathaway forks 57.9 m away; modern OSM river junction 39.4 m away |
| **Brief's placeholder** | (41.8885, -87.6385) — **203 m NNW of the derived point**, up the North Branch. The gate that refused to generate geometry until verification existed for exactly this case. |

## Method

1. **Master raster.** The BPL/Digital Commonwealth scan of Wright 1834
   (`commonwealth:js957744g`, 4204×5166 px, open rights) fetched at full resolution via IIIF.
   All pixel coordinates are in this resource space — the same space Allmaps uses, so the
   archived BPL annotation and this project's control are directly comparable.
2. **Why not just use the BPL georeference.** The published Allmaps annotation carries
   **three** control points with a first-order polynomial — the minimum possible, zero
   redundancy, no residuals computable. Evaluated against this project's independent control it
   shows RMS 25.9 m with a 56.8 m maximum. Archived verbatim in
   `data/traces/allmaps/wright_1834_allmaps_annotation.json` as provenance, superseded for use.
3. **Ground control.** Eight intersections were identified on the map from gridded crops at 3×
   zoom (picking precision ≈ ±4 px ≈ ±3 m) and matched to modern OpenStreetMap intersection
   nodes fetched from the Overpass API on 2026-08-09 (multi-node crossings averaged; max spread
   6.4 m). Control anchors on street centerlines that survive unchanged — including **State &
   Madison, the PLSS corner of sections 9/10/15/16 (T39N R14E)**, whose line the map itself
   draws continuing east as the reservation's south boundary. **No buildings were used as
   control**; the buildings are what the datum exists to locate.
4. **Fit.** Least-squares affine, pixel → EPSG:26916. Coefficients, per-point residuals, and
   sources in `data/traces/gcp/wright_1834_gcps.json`.
5. **Forks pixel.** The junction centre — where the North Branch, South Branch, and main-stem
   channel midlines meet — reads at **(1428, 1812)** ± ~15 px on the Wright scan.
6. **Cross-check.** The LOC scan of Hathaway 1834 (6536×9318; worked at 4000 px width) was
   independently georeferenced with five GCPs (RMS 17.7 m) — no Allmaps annotation existed for
   it, so `data/traces/gcp/hathaway_1834_gcps.json` is new georeferencing work. Its forks pixel
   (1445, 2010 in the working raster) lands **57.9 m NE** of the Wright-derived point.
7. **Third witness.** The modern OSM waterway junction node (12144667082) lies **39.4 m south**
   of the Wright point. The junction has not physically moved since 1834 — the banks were
   wharfed and regularized, but the Y stayed where it was.

## Findings worth keeping in mind

- **Both 1834 sheets are anisotropically stretched** — Wright 3.7% and Hathaway 4.5% difference
  between x and y scale, plus visible local warp (Wright's worst residual, 32.7 m, sits at
  Clark & Washington where the sheet is visibly distorted around the Public Square). This is
  physical paper behavior, not georeferencing error, and it means **a global affine cannot do
  better than tens of metres locally on these maps.**
- **Working uncertainty:** treat any position traced from the 1834 maps as ±~20 m until it is
  reconciled against a second source; the ~58 m cross-map disagreement is the honest ceiling.
- The Wright scan's E-W streets slope visibly relative to the sheet edge (~1.2° global rotation
  in the fit, more locally) — anyone tracing footprints should work from the fitted transform,
  never from "the map looks north-up."
- Hathaway carries **survey bearings and lot dimensions** ("N.51°E." along the main stem,
  "80"-ft streets, lot depths) — valuable for S2 street-geometry generation independent of any
  raster warp.

## Neither 1834 map shows buildings — verified 2026-08-09

Checked at native LOC resolution over the forks and the built-up South Water blocks 17-21:
**Hathaway 1834 is a pure cadastral lot plat** — block outlines, lots numbered 1-8, street
names, survey bearings, nothing else. Wright 1834 is the same. The widely repeated claim that
Hathaway's "small rectangles denote individual buildings", which reached this project's own
brief, is **false**.

Consequences, and they are not all bad:

- **No period map this project holds gives a building footprint for 1835 Chicago.** Footprints
  come from *textual* dimensions where they are attested — the Green Tree's 12 × 12 ft rooms,
  St Mary's 25 × 35 ft, First Presbyterian's 40 × 25 ft, the Western Hotel's 40 × 60 ft L — and
  are conjectural otherwise. That is a research task, not a tracing task.
- **Placement gets better, not worse.** The plats give exact street and lot geometry, so a
  building documented at a named corner can be put on that corner precisely. The residual error
  is the georeference's ±20 m, not an additional guess about where the corner was.
- The only sources that draw buildings at all are the 1933 Conley/Stelzer reconstruction
  (rights-flagged, pictorial) and the 1940 Nelson map (tier 6). Neither may drive geometry.

## Decisions

1. **Wright is the master; Hathaway is the check** — per the brief, and because Wright carries
   the denser verified control and open rights.
2. **The origin is the 1834-map-derived junction, not the modern junction node.** The project
   reconstructs the period geometry; the modern node corroborates it but does not define it.
3. Origin recorded to 0.1 m — far inside the real uncertainty, kept only so the re-derivation
   check has a stable target. Nothing downstream may treat sub-metre precision as meaningful.
4. `symbolic_location` fields on structures stay authoritative until footprints are traced with
   the fitted transforms; coordinates get filled in S2+, carrying the ±20 m caveat into each
   position note.

## Inputs and their permanence

| artifact | where |
|---|---|
| Wright scan (resource space) | IIIF `commonwealth:js957744g`; working-copy sha256 in the GCP file |
| BPL Allmaps annotation | `data/traces/allmaps/wright_1834_allmaps_annotation.json` (verbatim) |
| Wright GCPs + fit | `data/traces/gcp/wright_1834_gcps.json` |
| Hathaway working raster | LOC IIIF at `full/4000,`; sha256 in the GCP file; ×1.634 to native pixels |
| Hathaway GCPs + fit | `data/traces/gcp/hathaway_1834_gcps.json` |
| Modern control | OSM node ids recorded per GCP; © OpenStreetMap contributors, ODbL (`data/sources/osm_streets_2026.json`) |
| Re-derivation | `tools/rederive_datum.py`, run by `tools/check.sh` |

## What could move this origin later

Only better evidence should: a higher-quality warp (thin-plate spline against many more control
points), the corrected 1835 Wooley plat georeferenced, or a professional survey-grade
georeference of the originals. Any such change re-runs the derivation deliberately, updates
`datum.json` and this memo together, and regenerates all dependent geometry — which is why the
bake refuses to run against a datum that no longer matches its traces.
