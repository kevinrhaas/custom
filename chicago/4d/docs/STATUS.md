# STATUS

Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-10 · **Phase:** S0, S1 (datum), S2-partial (terrain + river at the
forks), S4-partial (frame_tavern, log_dwelling, bridge_timber) and R1 (renderer) complete.
**Milestone 0 shipped; Milestone 1 (the forks) is in** — six structures placed from the
georeference, real ground, a traced river, and the liberties now readable inside the
walkthrough rather than only in the repository.

---

## What exists and works

| thing | state |
|---|---|
| Repository scaffold | **done** — full tree per `docs/PLAN.md` |
| Schemas (structure, source, scene) | **done** — phases, tiers, rights gating, scene-owned dates |
| `tools/validate.py` | **done** — schema, referential, confidence contract, per-scene date gates, phase-overlap, epoch coverage, release blocking, license + rights gating, staleness, publish budget |
| `tools/test_validate.py` | **done** — 63 checks, all green, including a proof that an 1836 building is excluded from the 1835 scene, that a liberty naming a building does not cover an invention it never mentions, and that an attribute the archetype never reads cannot pass without saying what the mesh does instead |
| `tools/check.sh` | **done** — full gate runs in **0.4 s**, no Blender |
| Research dossiers | **done** — 8 reports, ~360 KB, committed verbatim in `docs/research/` |
| Source records | 13 seeded, of which 4 carry real Wayback snapshots |
| Structure records | **1** (Sauganash, two phases) |
| Terrain epochs | registry written; `e1834_harbor_cut` active, geometry layers **not yet built** |
| **Datum** | **VERIFIED** — Wright-derived, Hathaway- and OSM-checked, RMS 17.5 m, re-derivable from traces |
| **Generator pipeline** | **WORKS** — pinned Blender 4.5.3, `frame_tavern`, 496-tri Sauganash from the record alone |
| **Renderer** | **WALKABLE** — three.js r0.185.1 vendored, pointer-lock + touch, confidence view, provenance popup |
| **Smoke** | 109 checks green at 390×780 and 1280×800, zero page errors |
| **Liberties, in the app** | **done** — the Evidence panel lists all 24, derived from `docs/LIBERTIES.md` by `tools/compile_liberties.py` and re-derived by `check.sh`; the provenance popup shows the ones taken with the building you are inspecting; and the gate checks the document *for gaps* in both directions — refusing any conjectural value (footprint, position, or a stated form attribute) that no liberty admits to, and equally any attested value the archetype never reads and no liberty owns up to leaving out |
| **The lake shore** | **TRACED, NOT BUILT** — `shoreline.geojson`: the harbour reach, the 1834 cut, the old southward channel, the sand bar as an island and the mainland shore, E +314…+1570 off Wright 1834. Vectors only; no elevation, no mesh, nothing east of the box renders yet |
| **Published** | `site/chicago/4d/` (3.7 MB of a 25 MB budget) + a tile on the Chicago landing page |
| Exclusions | 14 date-guarded structures + a 4-item watch list |

## Corrections made after the first live look

Kevin opened the deployed build on real hardware and found two things headless testing had
missed. Both are fixed; both are the kind of thing only a real viewer catches.

- **The building rendered pure black on a real GPU.** The confidence shader computed
  `weight = f(vConfidence) * uConfMode` even when the view was switched OFF — and `NaN * 0.0`
  is still `NaN`, which poisoned `diffuseColor` through the mix. A geometry reaching a batch
  without `_CONFIDENCE` leaves the attribute unbound, and an unbound attribute is not reliably
  zero on real hardware the way it is under a software rasteriser. The channel is now
  sanitised at the vertex stage and the off path is guarded before it reads anything.
- **A well-documented building was rendered as near-total guesswork.** `wall_height_m` and
  `roof_type` were tagged `conjectural` while their own notes gave typological reasoning —
  "two full stories at typical period floor height", "gable is the near-universal form for the
  type and period". That is the brief's definition of `inferred`, not of `conjectural`. Worse,
  the massing rule took the worst confidence across the footprint too, so an unknown SIZE
  dithered the entire building into ghost massing. Size and character are different kinds of
  not-knowing: Wau-Bun documents a two-storey white frame building with bright-blue shutters,
  and no source gives a dimension. The massing now follows the attributes that say what the
  building was; dimensional uncertainty is carried in the sidecar, where the popup shows it.
  Understating what we know is as much a misrepresentation as overstating it.

## What does not exist yet

- **Six buildings** at the forks. Eight archetypes and ~40 researched structures are still unbuilt.
- **No terrain.** The scene stands on a flat plane; the 30-zone heightfield spec exists in the
  research dossier but has not been turned into data. This is the next stage.
- **No flora or fauna records.** The palettes and the placement table exist in the dossiers only.
- **Terrain and the river now exist**, traced from Wright 1834 through the same affine that
  fixed the datum. Total land relief across the whole 640 m box is **4.30 ft** — that is not a
  simplification, it is the site. The dossier's suggested 4–8x vertical exaggeration was
  refused because it contradicts `docs/EPOCHS.md` and LIBERTIES L3.
- **The bank profile is the largest unsourced assumption in the build.** No zone in the terrain
  dossier gives a bank *profile* at all; the 6 m face and its ease-out shape were chosen partly
  because a flat toe leaves the Z=0 contour — which IS the drawn waterline — ill-conditioned
  against the grid.
- **`chicagoarchitecturehistory.com` cites nothing** for the two best elevation figures in the
  dossier, which is why no land elevation in this build is tagged `documented`.
- **Placement is real but coarse.** All six structures now carry surveyed coordinates rather
  than nulls, at about ±20 m — the georeference's error, not an additional guess. Three of them
  (Wolf Point Tavern, Miller House, Walker's meeting house) have no surviving intersection and
  are derived from the confluence and the modern bank, with a larger and differently shaped
  uncertainty stated on each.
- **Walker's meeting house may be the wrong building.** The west-bank testimony describes 1831
  and the north-bank claim is dated 1834, which is what you would see if the sources describe
  two different buildings about 150 m apart across a river. Position is tagged `conjectural`
  and the record says so in the first line.

## The datum is verified

`data/datum.json` now carries `verified: true`: **E 447072.7, N 4637395.8 (EPSG:26916) =
41.886721, -87.637951** — the forks junction as drawn on Wright 1834, fitted against eight
modern control points (RMS 17.5 m), cross-checked against an independently georeferenced
Hathaway (57.9 m agreement) and the modern OSM river junction (39.4 m). The brief's placeholder
was **203 m off**. Full memo: `docs/RESEARCH/datum_derivation.md`; the derivation re-runs from
committed traces via `tools/rederive_datum.py`, which `check.sh` enforces.

Structure positions still carry `symbolic_location` with null coordinates — they get filled as
footprints are traced through the fitted transforms in S2+, each carrying the ±20 m working
uncertainty of the 1834 sheets in its note.

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
8. **FIXED — the white paint now reads as white.** The earlier diagnosis in this file (a weak
   sky contribution at a grazing sun angle) was wrong, and wrong in a way worth recording: the
   tan wall was a STALE PUBLISHED ASSET, an older bake that still carried the over-dark AO
   texture. Two separate causes then turned up behind it. `publish.sh` shipped from
   `assets/web/`, which only `bake.sh` refreshes, so running the generator directly republished
   the previous mesh silently — now guarded, and it says so when it copies a master through.
   And the sky-derived PMREM environment was overriding albedo outright: measured, a brown log
   wall rendered at an R/B ratio of 1.08 against the 1.75 its own base colour specifies, with
   every surface converging on the sky colour whatever it was made of. For a project whose
   claim is that a documented white wall reads as white, that is a data-integrity bug wearing
   an aesthetics costume. The environment is gone; a hemisphere fill with a warm ground bounce
   plus the sun now carry the lighting, and hue is preserved (log R/B 1.30). Revisit with a
   properly exposed HDRI rather than a PMREM of an analytic sky.
9. **AO is baked but switched off, deliberately.** The bake path works end to end and is wired
   as a real glTF occlusion texture, but the archetype's clapboard courses and window reveals
   sit a centimetre off the wall and occlude each other: a measured bake comes out at mean 0.265
   with 69% of texels below half, and the building renders brown. Shortening the AO distance
   only reaches 0.38. It needs a low-poly AO cage, not a tuning tweak. `--ao` keeps the path
   exercised and `assets/manifest.json` records honestly that the shipped asset has none.
10. **`gltf-transform` did not run**, so `assets/web/` currently holds copies of the
    uncompressed masters rather than meshopt/KTX2 derivatives. Harmless at 44 KB; it must work
    before the town scales.
11. **FIXED — the liberties are now attached to their buildings.** The provenance popup reads
    `subjects` and shows the liberties taken with the building being inspected: the Sauganash's
    four, L9 on the Green Tree, L7/L8 on the three Wolf Point placements. Both views render from
    one derived record through one entry renderer, so the panel and the card cannot describe the
    same liberty differently, and the smoke asserts the discriminating case — a second building
    gets its own set, not the whole list, and a scene-wide liberty is not pinned to any building.
    **Completeness is now enforced for one class of invention, and only one.** `validate.py`
    runs the inverse check: every phase whose `footprint` or `position` is `conjectural` must be
    claimed by a liberty's `Covers:` field — `structure_id[.phase_id].aspect`, declared by the
    document rather than inferred from its wording. Six such inventions exist in the committed
    data (five footprints, plus Walker's position); six declarations cover them. The self-test
    asserts the discriminating case, and that case got stricter: an entry whose prose is *about*
    footprints and placement, and which names the building, no longer covers anything at all.
    The claims are checked the other way too — a token naming no such structure, no such phase,
    or an attribute that is not conjectural fails the gate, so an over-claim is as loud as a gap.
    Entries under **Resolved** are exempt from that last rule, which is what lets an append-only
    document survive its own data being corrected. **The rule now covers stated form as well as
    drawn geometry** (2026-08-10): the aspect vocabulary is every attested value in a record —
    `footprint`, `position`, `documented_range`, the structure-level `function`/`occupants`, and
    `form.<attr>` enumerated from the data rather than from a list, so a new archetype attribute
    is inside the rule the day it appears. Widening it found four inventions with no admission —
    the Sauganash 1829 cabin's wall height and roof type, both PLACEHOLDER in their own notes,
    and `gallery: false` on the Green Tree and the Western, where false is the archetype's
    default rather than a finding. Ten conjectural values, ten declarations. **What is still
    unenforced is omissions and simplifications**, and that is the hard half: an invention has a
    record to point at and an omission does not, so the Western's unmodelled stable yard (L10)
    and the Green Tree's side additions (L9) are covered by prose alone. No mechanism can catch a
    liberty taken that nobody noticed taking. Six of six structures carry at least one liberty,
    so the popup's empty state remains unexercised by real data.
12. **The omission half is enforced now too, and switching it on found a documented feature
    that was never built.** The invention rule reads a `conjectural` tag and demands an
    admission. An omission leaves no tag: evidence with no geometry in front of it looks exactly
    like evidence with geometry in front of it, which is why prose was the only thing holding it
    until now. The claim therefore comes from the generator — each `*_params.py` declares the
    form attributes its `from_phase` actually reads (`CONSUMED`), and every attribute outside
    that set must say on the record what the mesh does instead: `absent`, `simplified`, or
    `record_only` for something that was never a build instruction. The first two owe
    `docs/LIBERTIES.md` a `Covers:` token exactly as an invention does, and the popup marks
    those rows so a visitor sees it and not only the repository. **Twenty-one attributes across
    six buildings turned out to reach no vertex.** Most are benign-but-real simplifications — a
    chimney count no archetype reads, one window rhythm on all three frame taverns, wall surfaces
    fixed by the archetype rather than the record. One is not. **The Wolf Point Tavern's frame
    extension and its painted wolf sign are both `documented` and both absent from the model**:
    the record spells them `frame_extension` and `signage`, the `log_dwelling` archetype reads
    `frame_addition` and `sign`, and `from_phase` fills an absent attribute with a default, so
    the two best-attested features of the house were dropped in silence and the popup showed the
    project's strongest confidence chip over both. That is the confidence model working as
    designed and still misleading, which makes it the sharpest argument for this rule that the
    project has produced. The fix is a rename plus a re-bake — record and geometry in one slice
    — and it is queued in ROADMAP § S5, not half-done here. L20 admits to it meanwhile.
    Miller's house is the same shape in miniature: its record says two chimneys and
    `log_dwelling` builds one. What is still unenforced is what no record mentions at all —
    the Western's unmodelled stable yard is now claimed, but a liberty nobody noticed taking
    remains uncatchable by any mechanism.
13. **The document and the data had drifted, and writing the claim down found it.** L12 still
    read "position tagged `inferred`" for the Walker meeting house; the record was downgraded to
    `conjectural` on 2026-08-09 and nothing carried the change back. The keyword rule was
    indifferent to the disagreement — the entry says "placed", the value was conjectural, and the
    match held for a reason that had nothing to do with whether the two agreed. Declaring the
    claim forced the comparison. L12 now carries a Revised line saying so, and the stale sentence
    stays: the file is append-only, and a silently corrected admission is not one.
14. **Frame rate figures are meaningless here.** 2–9 fps under headless SwiftShader is software
    rasterisation, not a GPU measurement. Draw calls (12) and triangles (1,006) are real.

## Next

**S5 — more structure records**, which is now the binding constraint: six buildings stand where
the sources describe roughly forty. Note the coupling discovered on 2026-08-10, because it sets
the shape of the work: `tools/compile_scene.py` writes an `asset` path for every structure that
resolves into the scene, so a record committed without its GLB makes the renderer fetch a file
that is not there — a 404 the smoke correctly fails on. **A structure record and its bake are one
unit.** An agent without Blender can prepare the record and the research memo, but the pair has
to land together, so the bake workflow's PR is part of the same slice rather than a follow-up.

**S2e — extend the ground east to the lake.** Raised to the top of the terrain work on
2026-08-10 at Kevin's direction, after free-fly made it visible from the air: the modelled
box stops at local E +320, while the Fort Dearborn site is at E +1127 and the 1835 shore is
about a kilometre further still. Fort Dearborn and the harbour works cannot be placed until
the ground under them exists. The shoreline itself is a provenance problem before it is a
modelling one — everything east of roughly Michigan Avenue is later landfill, so the edge
must come off Wright 1834, not off a modern coast. See ROADMAP § S2e.

**Parcel (a) is done and parcel (b) is the next slice.** The shore is now traced
(`tools/trace_shoreline.py` → `shoreline.geojson`, memo
`docs/RESEARCH/shoreline_harbor_1834.md`) and it moved two numbers off estimate and onto
measurement: the mainland shore reaches local **E +1257** and the sand bar's east edge
**E +1497**, so the roadmap's proposed +1500 box would have clipped the bar by 3 m and the
box should be **+1560**. Two independent segmentations of the same sheet, in different windows
with different background statistics, agree in their 80 m overlap to **0.1–5.7 m** on the south
bank and **0.5–1.3 m** on the north — worth stating because it is evidence that the trace reads
the draughtsman's line and not its own thresholds. What is still absent: **no elevation exists
anywhere east of E +320**, the bar included. A bar is a surface a couple of feet of lake stage
moves and no source gives its height, so the number will have to be argued in the terrain spec
rather than picked. Until the heightfield and its bake land together, nothing east of the
current box renders and the aerial view's edge is unchanged.

**S2 remainder** — Frog Pond, the Wells Street marsh, and the rest of the hydrology beyond
the single traced slough centreline.

**S6 — flora and fauna records**, which is also what would retire liberty L2's promise: the
palettes and placement tables exist in the dossiers and nothing has been turned into data.

New findings for S2 from the datum work: Hathaway carries survey bearings and lot dimensions
("N.51°E." along the main stem, 80-ft streets annotated); both 1834 sheets are anisotropically
stretched (3.7% / 4.5%), so street geometry should be generated analytically from the plat
dimensions and snapped to the fitted control, never traced raw from pixels.
