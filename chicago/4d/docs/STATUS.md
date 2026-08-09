# STATUS

Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-09 · **Phase:** S0 scaffold complete, S1 (datum) not started

---

## What exists and works

| thing | state |
|---|---|
| Repository scaffold | **done** — full tree per `docs/PLAN.md` |
| Schemas (structure, source, scene) | **done** — phases, tiers, rights gating, scene-owned dates |
| `tools/validate.py` | **done** — schema, referential, confidence contract, per-scene date gates, phase-overlap, epoch coverage, release blocking, license + rights gating, staleness, publish budget |
| `tools/test_validate.py` | **done** — 15 checks, all green, including a proof that an 1836 building is excluded from the 1835 scene |
| `tools/check.sh` | **done** — full gate runs in **0.4 s**, no Blender |
| Research dossiers | **done** — 8 reports, ~360 KB, committed verbatim in `docs/research/` |
| Source records | 13 seeded, of which 4 carry real Wayback snapshots |
| Structure records | **1** (Sauganash, two phases) |
| Terrain epochs | registry written; `e1834_harbor_cut` active, geometry layers **not yet built** |
| Exclusions | 14 date-guarded structures + a 4-item watch list |

## What does not exist yet

Everything downstream of the datum, by design:

- **No geometry of any kind.** No generators, no archetypes, no bake, no GLBs.
- **No renderer.** `renderers/web/` is an empty directory.
- **No terrain layers.** The 30-zone heightfield spec exists in the research dossier but has not
  been turned into data.
- **No flora or fauna records.** The palettes and the placement table exist in the dossiers only.
- **No smoke test**, because there is nothing yet to smoke.
- **No published site tree.** Nothing under `site/chicago/4d/`.

## Blocking: the datum is unverified

`data/datum.json` carries `verified: false`, and the validator says so on every run. This is
deliberate and it is the project's critical path:

> The scene origin at the Wolf Point forks must be derived from the georeferenced Wright 1834
> and Hathaway 1834 rasters before any geometry is generated. Fixing the origin after geometry
> exists means regenerating everything.

Structure positions therefore carry `symbolic_location` ("south-east corner of Lake and Market")
with null coordinates. That is not a placeholder to be filled in casually — it is the honest
state until the georeferencing is done and its residuals recorded.

## Known weaknesses, stated plainly

1. **One structure record does not prove the schema.** The Sauganash exercises phases, a
   building move, and the full confidence range, but the model has not met a fort, a bridge, or
   a row of storefronts yet. Expect schema pressure at Milestone 1.
2. **`construction: balloon_frame` on the Sauganash is probably wrong** and is flagged as such
   in the record. Balloon framing postdates the 1831 building by a year. Left visible rather
   than silently swapped, because substituting one guess for another is not a fix.
3. **The Sauganash gallery reading was revised on day one**, from "gallery, conjectural" to
   "no gallery, inferred", after opening the two retrospective images the repo already held.
   Both show no veranda and both show the 1829 log cabin surviving as an attached wing. The
   images are not independent of each other, so this is inference, not documentation — and the
   `frame_tavern` archetype now has to support an attached log wing.
4. **Two sources have no web archive.** `drloih_hotels` has no Wayback snapshot and the
   validator warns about it on every run; the warning is correct and stands until someone
   archives the page. Wau-Bun's archived_url points at a scanned edition of the book rather
   than the transcription actually read during research — noted in the source record.
5. **Several research claims are snippet-derived.** `encyclopedia.chicagohistory.org` returned
   503 throughout the research session, and a few citations in the dossiers rest on search-index
   snippets rather than retrieved pages. They must be re-fetched before any of them is promoted
   to `documented`.
6. **The Conley/Stelzer rights question is open.** Marked `check_required`; no asset may be
   derived from it until a Stanford Copyright Renewal Database check is recorded.
7. **The 1835 lake stage is a guess.** 580 ± 1.5 ft ASL, tagged conjectural, and the entire
   vertical datum hangs off it.

## Next

**S1 — verify the datum.** Pull the BPL Wright 1834 GeoTIFF and the LOC Hathaway JP2, warp
against surviving PLSS section-line geometry (not against buildings), store the Allmaps
annotations in `data/traces/`, derive the origin, record the residuals, and flip
`verified: true`. Everything else is waiting on it.

Parallel work that does **not** need the datum: the renderer shell on synthetic geometry,
archetype generators against golden parameters, and further research dossiers.
