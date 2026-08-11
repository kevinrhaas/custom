# STATUS

Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-10 · **Phase:** S0, S1 (datum), S2-partial (terrain + river at the
forks), S4-partial (frame_tavern, log_dwelling, bridge_timber) and R1 (renderer) complete.
**Milestone 0 shipped; Milestone 1 (the forks) is in** — six structures placed from the
georeference, real ground, a traced river, and the liberties now readable inside the
walkthrough rather than only in the repository. **Seven structures now, and the seventh is
not a building**: the North Branch bridge is the first record built on the `bridge_timber`
archetype and the first in this dataset whose dimensions come from evidence rather than from
a placeholder. As of 2026-08-10 it stands on **two bents rather than fifteen invented cribs**
(§ 24) — the first time a reading of an archive has taken something *out* of this model.
**Eight structures now, and the eighth is the first BUILDING whose footprint is evidence**:
Hogan's store on Lake Street, where Chicago's post office opened in 1831, is recorded twice by
Andreas as twenty by forty-five feet (§ 25). It is also the first record here with nothing
conjectural in it, and the correction that came with it moved the post office's departure from
this building by twenty months.

---

## What exists and works

| thing | state |
|---|---|
| Repository scaffold | **done** — full tree per `docs/PLAN.md` |
| Schemas (structure, source, scene) | **done** — phases, tiers, rights gating, scene-owned dates |
| `tools/validate.py` | **done** — schema, referential, confidence contract, per-scene date gates, phase-overlap, epoch coverage, release blocking, license + rights gating, staleness, publish budget |
| `tools/test_validate.py` | **done** — 96 checks, all green, including a proof that an 1836 building is excluded from the 1835 scene, that a liberty naming a building does not cover an invention it never mentions, that an attribute the archetype never reads cannot pass without saying what the mesh does instead, and that rewriting a record's prose does not report its mesh as stale while changing a value the generator reads does, and that an attribute an archetype declares it consumes actually moves the parameters when its value changes, and that an exclusion carries a reason and a citation that resolves and stops being an exclusion at its own earliest scene |
| `tools/check.sh` | **done** — full gate runs in **0.4 s**, no Blender |
| Research dossiers | **done** — 8 reports, ~360 KB, committed verbatim in `docs/research/` |
| Source records | **25**, of which **14** carry a Wayback snapshot — the three added with the bridge all do, and so does the post-office page |
| Structure records | **8** — six buildings at the forks, the North Branch bridge, and Hogan's store on Lake Street |
| Terrain epochs | registry written; `e1834_harbor_cut` active, geometry layers **not yet built** |
| **Datum** | **VERIFIED** — Wright-derived, Hathaway- and OSM-checked, RMS 17.5 m, re-derivable from traces |
| **Generator pipeline** | **WORKS** — pinned Blender 4.5.3, `frame_tavern`, 496-tri Sauganash from the record alone |
| **`frame_dwelling`** | **BUILT 2026-08-11, NO RECORD USES IT YET** — the archetype that unblocks houses: 1/1.5/2 storeys, knee wall and gable-end attic window, rear ell read off the footprint polygon, stoop or small roofed porch, and `construction` finally moving vertices (stud module places the openings, clapboard butt joints land on stud lines, braced frames get the girt band a balloon frame has no line for). Golden params + `docs/RESEARCH/archetype-frame_dwelling.png`; 248-730 tris per house. `GROUND_CONTACT: perimeter` verified against the mesh — every edge of the footprint polygon carries a wall at z = 0, worst gap 0.0 mm, nothing below the base of the walls |
| **`outbuilding`** | **BUILT 2026-08-11, NO RECORD USES IT YET** — the highest-count-per-effort archetype in the plan, and the one that gives the town yards instead of eight isolated public houses. A FAMILY, not a shape: `construction` log/plank/light_frame drives three different wall routines, shed roofs are first-class rather than a fallback, `open_sides` turns any subset of elevations into posts-and-plate, and `door` is none/man/stable/wagon — a boolean is refused with a message saying why. `board_gap_m` alone is the whole difference between a stable and a corn crib. Five golden variants from a 1.25 m privy to a 13 m hotel stable, 272-2008 tris; `GROUND_CONTACT: perimeter` verified on ALL FIVE against ground-plane EDGES rather than vertices (the first check compared vertices and produced false failures on a 13 m wall that is one quad). Discharges the stable half of L10; **the yard half stays open** — a fence line with two gateways is an enclosure, and building it out of an outbuilding would be calling a fence a building, so L10 needs NARROWING rather than resolving |
| **Renderer** | **WALKABLE** — three.js r0.185.1 vendored, pointer-lock + touch, confidence view, provenance popup |
| **Smoke** | **128 of 129 green** at 390×780 and 1280×800, zero page errors. The one failure is `desktop 1280x800: walk intent moves the camera`, a frame-rate regression rather than a behaviour regression — mobile passes. See § Known weaknesses 0. |
| **Flora** | **the sward is in** (2026-08-10) — `renderers/web/js/flora.js` plants the graminoid matrix, forbs, emergents and low shrubs from `data/flora/`, at 8 draw calls and ~90 k triangles. July phenology is enforced in the renderer as well as in the data: no flowering culm is drawn for any species the record calls vegetative |
| **Liberties, in the app** | **done** — the Evidence panel lists all 26, derived from `docs/LIBERTIES.md` by `tools/compile_liberties.py` and re-derived by `check.sh`; the provenance popup shows the ones taken with the building you are inspecting; and the gate checks the document *for gaps* in both directions — refusing any conjectural value (footprint, position, or a stated form attribute) that no liberty admits to, and equally any attested value the archetype never reads and no liberty owns up to leaving out |
| **The lake shore** | **TRACED, NOT BUILT** — `shoreline.geojson`: the harbour reach, the 1834 cut, the old southward channel, the sand bar as an island and the mainland shore, E +314…+1570 off Wright 1834. Vectors only; no elevation, no mesh, nothing east of the box renders yet |
| **Published** | `site/chicago/4d/` (4.08 MB of a 25 MB budget) + a tile on the Chicago landing page |
| Exclusions | 14 date-guarded structures + a 4-item watch list — **in the walkthrough** since 2026-08-10 (Evidence panel, "What is not here"), citations joined, and now held to the same citation rule as a structure record (§ 26) |

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

- **Seven buildings** — six at the forks and Hogan's store a block east on Lake Street. Eight archetypes and ~40 researched structures are still unbuilt.
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
- **Placement is real but coarse.** All eight structures now carry surveyed coordinates rather
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

00. **The prairie loses a blind side-by-side against a July photograph, in under a second,
    and we now know exactly why.** A four-parcel sweep on 2026-08-10 put each piece of the
    vegetation through its own builder-and-critic loop against verified photographs of
    surviving Illinois tallgrass, with a blind A/B as the judgement. Three critics ran on one
    identical shot set. All three lost. Two of them, on different references and different
    framings, lost on the **same** feature. What follows is the measured state, recorded
    because it is more useful than the summary "needs work":

    - **The mid-field sheet is discarded at ~455 m.** Canopy rings from 2.5 m to 453 m sit at
      the sward top; from 511.8 m outward every ring drops to `y = 0.05` with `aMask = 0` and
      the shader discards it. The vegetated surface therefore ends where the fog is only
      27 %, and the 93 % haze `world.js` designs for at 1290 m is never rendered onto any
      vegetated pixel. **All three parcels have been converging on a colour no visible
      surface in the scene reaches.** This one fact produces the blind tell in both pairs,
      the missing aerial recession, the collapsed grain and the ring seam below.
    - **There is no aerial recession on flat ground and there structurally cannot be.** At a
      1.68 m eye with a 55° vertical field over 800 rows, a ground point at distance *d*
      lands `1290.9/d` px below the horizon — so the entire fog ramp from 10 % to 93 % lives
      between rows 402 and 406. Six pixels of atmosphere in an 800-pixel frame. Only vertical
      structure carried into the distance can buy recession here; exponential distance fog
      cannot.
    - **A ring seam draws a straight line across the frame.** `TUNE.mid.radius = 27.0 m`, and
      on flat ground a constant radius maps to a constant screen row — predicted 448.8,
      measured at row 450 in `prairie_south`, razor-straight across all 1280 columns.
    - **Grain collapses with depth where the photographs' is flat.** 5×5 high-pass RMS in
      bands down from the land/sky boundary: ours 13.8 / 14.6 / 21.2, both references
      18.8 / 31.4 / 39.3 and 39.3 / 41.7 / 41.3.
    - **The horizon timber is nearly absent.** Timber is detected in **31 %** of horizon
      columns overall and 3.6 % across the central two-thirds, against **100 %** of columns in
      every band of the reference including its faintest. The 2–4 px band *height* is honest
      arithmetic; the emptiness is not. A round that reported re-toning this band had in fact
      reduced its detection cover from 21.1 % to 0.9 %, and the target it was given
      (Weber 0.036–0.067) does not exist in the reference at any threshold — that error was
      the brief's, not the builder's.
    - **Crowns read as boulders.** Fine-detail ratio 0.23–0.34 against the photograph's
      0.61–0.64 — our crowns at 20–60 m carry the fine-scale texture of a photograph's
      kilometre-distant treeline. Shadows clip to literal `(0,0,0)` where the photograph's
      darkest decile is L 14–27, and sunlit crown tops are **blue** (G−B −19 to −26) where
      the photograph's are warm green (+13 to +24).
    - **The shot set has only one open-prairie view.** `prairie_south` stands 3.46 m from a
      trunk with 23.4 % open sky against `prairie_west`'s 95.4 %. That second angle exists
      precisely as the control that separates a tuned view from a fixed one, so
      `prairie_west` has been tuned against itself with no control.
    - **`river_bank` fails its own brief and the fault is the renderer, not the data.** Zone 1
      specifies cordgrass at 1.2–2.0 m and 40–55 % cover with `bare_soil_fraction: 0.0`; the
      frame shows ~25 cm sprigs on visible bare soil in near-rows.

    Two things came out of the sweep clean and should be said as plainly as the failures. The
    **July phenology is correct at source** — every warm-season grass vegetative with a null
    inflorescence, cattail fruiting and brown, ramp leafless, and a live guard that suppresses
    and reports any record that contradicts itself. And the **flora dataset is the one parcel
    a critic passed without reservation**. The renderer is what is failing it.

    Two methodological corrections worth keeping, both of which invalidate numbers this
    project has quoted:

    - **The primary reference was the wrong photograph.** `dupage_tallgrass_2018-07-24.jpg` is
      titled "*Restored* tallgrass prairie" and described as a "Prairie planting" on a former
      agricultural field — a seed mix on plowed ground, and restorations are bought for being
      forb-rich. The never-plowed Woodworth stand is the better analogue for unmanaged 1835
      prairie. Measured flower load: planting 12.91 %, virgin remnant 1.79–5.54 %. The honest
      target is **4–6 %, not 13.89 %**.
    - **Two rounds were judged at the wrong look-angle.** The shot harness set no pitch while
      the reference photographer had tilted down ~12°, so every "nearest quarter" number
      compared the photograph at 2 m against our render at 4 m — and near-field vegetation was
      exactly what those rounds were tuning. The harness is now pitch-matched and prints its
      pitch. Correcting it makes the gap *worse*: 0.07 % against a virgin remnant's 2.97 %.
    - A hue/saturation test cannot separate July from October here — the October negative
      control lands *between* the two July photographs. That metric should not be quoted by
      anyone, including this file.

0. **The walk assertion fails on the test machine, by one frame, and it is a shared cost.**
   `tools/smoke_renderer.mjs` holds W down for 2.2 seconds of wall clock and requires the
   walker to cover more than 0.30 m. The walker moves `dt × 1.45 m/s` with `dt` clamped at
   0.05 s, so the assertion is really "render at least five frames in 2.2 seconds" — a
   frame-rate assertion, measured on a machine with no GPU at all, where the whole scene is
   rasterised in software. Measured at the viewpoint the assertion runs from, on 2026-08-10:

   | tree state | ms/frame | frames in 2.2 s | walked |
   |---|---|---|---|
   | HEAD, before this round | 417 | 5.3 | 0.38 m — passes |
   | + terrain and sky work, no vegetation data | 520 | 4.2 | 0.30 m — on the line |
   | + flora and trees | ~610 | 3.6 | 0.29 m — fails |
   | + the vegetation sweep (2026-08-10, measured) | ~730 | 3.0 | **0.22 m — fails** |

   The last row is a **regression inside an already-failing assertion**, and it is recorded
   rather than absorbed: the sweep put 339 stemmed willow thickets where there had been 202
   unstemmed ones, drew limbs on every tree form instead of one, and gave the sward's flower
   heads real geometry per recorded shape. That is more triangles for a reason, but it is
   still 0.07 m further from the bar. Triangles are 494,667 against a 600 k budget and draw
   calls 21 against 80, so the budget gates do not catch it — this is fill and shading cost on
   a software rasteriser, not geometry count. **Mobile at 390×780 still passes.** Item 10 in
   ROADMAP § S6a next (adaptive budget) is the standing answer and has not been done.

   The **mobile** pass at 390×780 passes: the sward's low-spec field is a
   genuinely shallower one (a 4.6 m near ring against 7.6, the canopy taking
   over at 4.6 m instead of 10) rather than the desktop field scaled down, and
   at 124 k triangles the phone-sized viewport clears the bar. It is the
   1280×800 pass that misses.

   Three parcels landed in one round and together they crossed it. **No one of them can
   recover it**: deleting the vegetation entirely still leaves 520 ms, which is not five
   frames. Cutting the sward's density by a third moved the frame by 12 ms and visibly
   un-hid the ground, so that trade was taken back — the sward's own bar is that the ground
   is invisible at eye height, and it was not worth failing that to not-quite-pass this.
   **The assertion has not been weakened and must not be.** What it is telling us is true: the
   scene got a third slower this round. The choices are to make the frame cheaper (the ground
   shader is the largest single cost and it is now drawn behind a sward that hides most of it),
   or to decide deliberately that a wall-clock walk test cannot live on a software rasteriser
   and give it a frame-count form instead — a decision for a human, not for a parcel that
   would benefit from it.


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
    project has produced. **Repaired 2026-08-10, in one slice with its bake** (see 18 below).
    Miller's house was the same shape in miniature — its record says two chimneys and
    `log_dwelling` built one — and is **repaired 2026-08-10, in one slice with its bake**
    (see 19 below). What is still unenforced is what no record mentions at all —
    the Western's unmodelled stable yard is now claimed, but a liberty nobody noticed taking
    remains uncatchable by any mechanism.
13. **The document and the data had drifted, and writing the claim down found it.** L12 still
    read "position tagged `inferred`" for the Walker meeting house; the record was downgraded to
    `conjectural` on 2026-08-09 and nothing carried the change back. The keyword rule was
    indifferent to the disagreement — the entry says "placed", the value was conjectural, and the
    match held for a reason that had nothing to do with whether the two agreed. Declaring the
    claim forced the comparison. L12 now carries a Revised line saying so, and the stale sentence
    stays: the file is append-only, and a silently corrected admission is not one.
15. **FIXED — the staleness gate existed in the documentation and nowhere else.** `AGENTS.md`
    has said since the scaffold that "a stale committed GLB is a check failure, not a warning",
    and `assets/manifest.json` has carried an `inputs_sha256` per asset since the first bake.
    Nothing ever recomputed it. `run_stale_check` asked only whether each GLB appeared in the
    manifest, so a record could be edited into a different building and the town would keep
    rendering the old one with the gate green — the exact failure mode the S5 repairs are queued
    for, unguarded. The check now recomputes every committed asset's inputs and fails on
    disagreement, and the recipe lives with the generators (`generators/mesh_inputs.py`,
    `terrain_gen.terrain_inputs_sha`) so the side that writes the hash and the side that checks
    it cannot drift.
    **Switching it on required redefining the hash, because the old one was unusable.** It hashed
    the whole phase record plus every `.py` under `generators/`, which meant all six buildings
    read stale for reasons that cannot move a vertex: the `geometry:` declarations added on
    2026-08-10, and a `CONSUMED` constant added to one archetype's parameter module invalidating
    the others' buildings. A hash that cries stale over a rewritten note gets disbelieved, and a
    disbelieved gate is worse than none. It now hashes what the builder can see — the *resolved*
    parameters, the class's derived properties, the confidence floats, and the bytes of the
    builder, `common/`, `build.py` and the Blender pin. Parameter-module bytes are deliberately
    out: that module's whole effect on the mesh is the object it returns, and the object is
    hashed in more detail than its source would give.
    **The eight committed hashes were re-stamped without a bake, and that is a claim, so here is
    the proof.** Under the new recipe, every input to all six buildings is byte-identical to what
    it was at the last bake (`c3953d2`) — checked by running the new recipe inside a worktree of
    that commit and diffing the input documents, not by inspection. The single difference is
    `build.py`, whose only change in this slice is delegating the hash to the new module. Terrain
    re-stamped for the same reason: `terrain_gen.py` hashes its own bytes and gained an extracted
    function. No mesh was regenerated and none needed to be. `manifest.json` now records
    `inputs_scheme`, and the gate refuses a manifest stamped under a scheme it does not compute
    rather than comparing two hashes that mean different things.
    What this still does not catch is stated in `mesh_inputs.py`: it compares inputs, not output.
    Cycles AO is not bit-reproducible across hardware, which is why freshness is defined on inputs
    at all — a hand-edited GLB behind an untouched record passes, and nothing here can see it.
16. **The nightly bake pushes its branch and cannot open its PR.** `chicago-4d-bake.yml` ends
    by creating a pull request and that step has been failing on a repository setting —
    "GitHub Actions is not permitted to create or approve pull requests" — so every bake since
    the workflow was written has left its geometry on an orphan `steward/bake-*` branch that
    nothing merges. Eight such branches exist. This slice worked around it by fetching the bake
    branch and fast-forwarding onto it, which is fine for an agent that is watching, and no use
    at all for the nightly. The fix is one checkbox in the repository's Actions settings, or a
    PAT on that step; the workflow lives outside `chicago/4d/` and is therefore outside this
    lane's scope to edit, so it is recorded here rather than fixed.
17. **Frame rate figures are meaningless here.** 2–9 fps under headless SwiftShader is software
    rasterisation, not a GPU measurement. Draw calls (12) and triangles (1,006) are real.

18. **FIXED — the Wolf Point Tavern has its frame half and its wolf sign.** The defect the
    omission gate found on 2026-08-10 is repaired the same day, record and mesh in one commit:
    `frame_extension` → `frame_addition`, `signage` → `sign`, the two names `log_dwelling`
    actually reads. The building that named Wolf Point now has a board hanging outside it.
    **The rename was the smaller half.** `frame_addition: true` and nothing else would have let
    the archetype pick the bay's side, width, depth and storey count from its defaults — a
    two-storey frame block across the river front of a tavern the sources describe as low — so a
    documented feature would have arrived at an invented size with nothing admitting it, which is
    the same failure this repair exists to end, one level down. The record therefore states all
    four: side `end` and width 4 m of the 12 m frontage and depth 7 m all **conjectural**, storey
    count 1 **inferred** by the same argument the storey count above it uses. L24 admits the three
    conjectural ones; L20 moves to Resolved carrying both spellings that no longer resolve,
    because a silently corrected admission is not one.
    **What the sign is: a blank board.** The bracket, the arm, the board and its proportions are
    the archetype's invention, and the painted wolf is not drawn — no description of it survives,
    and a wolf painted from imagination would be the most conspicuous invention in the scene on
    the one object every visitor will walk up to. L25 says so.
    **Two limits worth stating.** The confidence tint on the bay follows what the bay IS
    (documented that it existed, inferred that it was low), not its unknown size — the rule set
    for the Sauganash, which means the tint alone will not tell a visitor the width is a guess and
    only the popup's liberty chip will. And the whole repair rests on a footprint that is itself a
    placeholder: 4 m of an invented 12 m is a fraction of a guess.

19. **FIXED — the chimney count is a number the archetypes read, and the third misspelling is now
    a test.** Every record states `chimneys`; neither archetype read the value. `frame_tavern`
    built two stacks whatever the record said and `log_dwelling` built one, so Samuel Miller's
    house — record two, model one — stood a stack short from its first bake. Both archetypes take
    the count now. The pair on a frame block keeps its exact positions (0.22 and 0.78 of the
    frontage, read off the Sauganash depictions) so that parameterising the number did not quietly
    move a building whose count was already right; a log building's second stack goes on the frame
    addition rather than the far gable, because *the record's own reason* for counting two is "a
    stack in each element", and honouring the number while contradicting its argument is not
    honouring it. L21 moves to Resolved and the six records drop the `geometry: 'simplified'`
    declaration that was true until this landed.
    **The `log_dwelling` half was the Wolf Point defect a third time.** The parameter was
    `chimney`, a boolean; no record in this dataset has ever contained that word, so `from_phase`
    took its default on every log building and nothing complained. Three occurrences of one
    failure is a pattern rather than bad luck, so it now has a check instead of another
    discoverer: `test_consumed_attributes_actually_reach_the_parameters` perturbs every stated
    value its archetype declares it CONSUMES and requires the resolved parameters to change — 55
    attributes exercised across the six records, with a `ParamError` counted as read, since
    refusing a value is the loudest possible proof of having seen it. The opposite direction (an
    attribute stated and *not* declared) was already the omission gate; this closes the direction
    where the declaration itself is the false one, which is the worse of the two, because an
    attribute inside CONSUMED is excused from admitting anything.
    **What it does not fix, and that is the more interesting half.** The count is `inferred` on
    every building and nothing else about a stack is recorded anywhere — not one source describes
    a chimney on any of these six. Position, girth, height above the ridge and material are all
    the archetype's, so the confidence chip a visitor reads on that row grades only *how many*.
    L26 is new and is the only place that distinction is legible.

20. **FIXED — Miller's frame range is dimensioned by the record, and fixing it found the storeys
    on the wrong half of the house.** The queued defect was L24's one building over:
    `frame_addition` is `documented` on `miller_house` — "a two-story house added to the cabin,
    fronting the river" — and the record stated no side, no width, no depth and no storey count,
    so `log_dwelling` supplied all four from its defaults. Repaired 2026-08-10, record and mesh in
    one commit. Two of the four turn out to be **attested**, which is the difference between this
    building and the Wolf Point bay: the side is `front` because the source says *fronting the
    river*, and the range is two storeys because the source says *a two-story house*. Only the
    width and depth are invented, and they are read off this record's own footprint polygon — the
    river-fronting limb is 9 × 6 m — rather than picked afresh, so the mesh agrees with the plan
    the record already draws. L27 admits them; they inherit the polygon's invention, which is
    total.
    **The storey count was the real defect and it was not on the queue.** `stories` was `2,
    documented`, with its own note saying in as many words that the two storeys described the
    river-fronting range and not the whole building — but `log_dwelling` reads `stories` as the
    LOG CORE's count. So the documented claim was spent on the cabin, the range fell back to a
    4.7 m default, and the model stood a two-storey log cabin **behind a shorter frame block**:
    the composition inverted, seen from the exact spot across the water where the 1833 description
    of it was written. That is the `frame_extension`/`signage`/`chimney` failure in its subtler
    form — not a name the archetype could not find, but a name it found and read as being about a
    different half of the building. No spelling check catches that, and neither does
    `test_consumed_attributes_actually_reach_the_parameters`, which proves only that a value moves
    *something*. The two-storey claim now sits on `frame_addition_stories`, the cabin's `stories`
    is 1 `inferred` (no source gives the log part a height; the 1833 view's "a two-story building
    and adjoining log cabin" only reads as a contrast if the cabin was lower), the 5.2 m moves to
    `frame_addition_height_m`, and `wall_height_m` becomes the cabin's 2.6 m — the number this
    record has named for it since it was written, sitting in a note rather than in a field.
    L13 moves to Resolved: neither composite building is a single extrusion any more.
    **What did not get better.** The archetype masses the footprint's bounding box, so the log
    core comes out the full 9 m wide rather than the polygon's 6 m and the 3 × 5 m re-entrant
    corner behind the range is filled in. Stating the range's own numbers is what makes that
    visible — the defaults produced an inverted-T matching neither the polygon nor the sources —
    and L27 records it. And the whole repair still rests on a placeholder: 9 × 6 of an invented
    9 × 11.

21. **The first bridge, and the first record whose size is not a placeholder.** The North Branch
    crossing at Kinzie Street — Chicago's first bridge, built 1832, replaced 1839 — is now a
    record, a bake and a published mesh, on the `bridge_timber` archetype that had been written
    and never used. Two of its numbers are evidence rather than invention, which is new here:
    **ten feet wide** is Charles Cleaver's, recalled in the *Chicago Tribune* of 29 Oct 1893 by a
    man who had driven a team across it, and the **71.83 m span** is measured between the two
    traced 1834 waterlines along the Kinzie alignment rather than chosen — it agrees with the
    reach's drafted mean width to about a metre, which is the check that it reads the map at this
    station instead of averaging it. Three source records were added, all three with Wayback
    snapshots.
    **What is invented is the middle of the bridge, and it is the most conspicuous thing in it.**
    Cleaver describes the ends — "the abutments were built of heavy logs in the shallow water near
    the banks" — and nobody describes what stood between them. Something had to carry 71.83 m of
    log stringer, so the archetype's default 4.5 m spacing puts **fifteen cribs in the river**, a
    regular colonnade a visitor will read as a fact about the bridge. It is a fact about the
    archetype. L29 admits it, and the confidence tint cannot: the tint grades what a crib *is*,
    not how many there were. The span it divides is itself the drawn waterline-to-waterline
    distance, and the abutments stood inside that line by an unrecorded amount.
    **Two sources contradict each other about the thing and both are kept.** Andreas has it
    "formed of stringers and only fitted for foot passengers" and "useless for teams" as late as
    the summer of 1833; Cleaver remembered driving across it, and on 18 Aug 1835 a procession of
    hundreds crossed it. It was rebuilt or widened in between and nothing reached says when or
    how. The record takes the 1835 reading — four stringers, a full-width deck — and says on its
    own face that an 1833 scene would want the other one.
    **A correction to this project's own dossier came out of writing it.**
    `docs/research/03-structures-north.md` §5 tags both "about 10 ft wide" and "clearing the water
    by about 6 ft" as documented. Only the width survives: the pages carrying the width, the
    abutments, the stringers, the 1832 date and the 1839 replacement say nothing about a height
    above the water, and a direct search of the same host for the phrasing returns nothing. The
    figure is kept, `clearance_m` is tagged `inferred`, and `bridge_timber_params.py`'s docstring
    is corrected so the constant's name stops asserting what it cannot show.
    **The contract's water-anchor rule is wired rather than written.** `docs/GLB-CONTRACT.md` has
    said since the archetype was drafted that a structure over water anchors `y = 0` at the design
    water surface and that the renderer must place it against the water plane; nothing implemented
    it, and nothing needed to until there was a bridge. The archetype declares `VERTICAL_ANCHOR`,
    `compile_scene.py` copies it to `placement.vertical_anchor`, and the renderer places `water`
    at a literal zero — that plane is zero by the definition of the vertical datum. The smoke
    asserts the **difference** between the two anchors, not `y === 0`: over dry land they agree,
    so a test that passed there would prove nothing.
    **Writing that assertion found two things the code was right about and the description was
    not.** First, sampling at the record's placement origin proves nothing either: that origin is
    the polygon's (0, 0), for this bridge the west end, which sits exactly on the traced waterline
    where the ground crosses zero — zero against zero, and the check passes whatever the renderer
    does. It samples the deck's midpoint now. Second, the failure mode is the opposite of the
    obvious one. `terrain.height()` does not report the channel bed over water; it reports a
    **wading barrier at +4 m**, put there to stop the walker strolling into the river. A bridge
    left on the terrain anchor therefore does not sink out of sight — it hangs four metres above
    the water, which is the harder failure to read, and it is what the smoke now pins.
    **You cannot walk across it, and that is stated rather than faked.** The walker follows the
    terrain, so the deck is scenery you pass under rather than a route; its footprint is excluded
    from the collision polygons, because treating a deck as a wall would put an invisible barrier
    across the river with nothing visible at head height to explain it. A walkable deck needs the
    walker to learn about surfaces above the ground, which is its own unit of work.

22. **The bridge arrives nowhere, and the gate that says so is new.** Three rules now ask
    whether a record is honest: the confidence model grades what a value claims, the liberties
    coverage check demands an admission for anything invented, and the geometry declarations
    demand one for anything stated and not built. None of them can see a structure that was
    built faithfully onto ground that is not underneath it, because **nothing in the record is
    wrong**. Every name resolves, every value reaches a vertex, every confidence chip is earned,
    and the North Branch bridge still stands 2.42 m clear of the terrain at both landings.
    `check_ground_contact` closes that direction. Each archetype declares where it touches the
    ground — `perimeter` for a building (the footprint outline, at the base of the walls) and
    `ends` for a crossing (the two end edges, at deck height) — and `validate.py` measures that
    outline against the committed heightfield through `tools/heightfield.py`. **The tolerance is
    not a new number: it is the walker's 0.35 m step-up rule**, because the question the gate
    asks is literally the walker's question, and a structure a visitor could not step onto has
    not met the ground.
    **What it found is the only thing it found, and that is worth stating too.** The six
    buildings land: their worst corner sits 0.16 m off (the Wolf Point Tavern, over the bank
    fall), well inside a step. The bridge does not, and cannot with the data as it stands — the
    deck sits at 2.22 m (Cleaver's inferred six-foot clearance plus the stringer and plank depth
    under it) and the highest land anywhere in the 640 m box is 1.31 m, so there is no ground in
    this epoch for it to arrive at. The record declares `ground_contact: approach_not_modelled`
    and L30 admits it; the popup shows the chip on the building being inspected, so the
    admission reaches a visitor and not only a reviewer.
    **The approach is not modelled because nothing describes one.** Andreas gives the stringers,
    Cleaver gives the width and the log abutments "in the shallow water near the banks", and no
    source reached says how a person or a team got from the bank onto the deck. An embankment
    would be a second invention stacked on the clearance figure — which is itself only
    `inferred` and unsourced in the dossier that supplied it — and unlike L29's fifteen cribs it
    is the invention a visitor would walk over rather than look at.
    **A smaller thing came out of writing it, and it is a warning about the staleness hash.**
    The contact height was first written as a `@property` on `BridgeTimberParams`, and
    `mesh_inputs.py` hashes every property a parameter class derives — so a number no builder
    reads immediately re-staled the bridge. That is exactly the false positive § 15 rewrote the
    hash to end, arriving from a new direction: the rule "a derived property is a mesh input" is
    right about constants and wrong about accessors. It is a module-level
    `ground_contact_z(params)` instead, and the docstring says why so the next one does not
    rediscover it.
    **What it still cannot see** is a structure standing on ground that exists and is wrong —
    the check compares a mesh against the heightfield, and both can agree on a surface no
    source supports.

23. **Four attributes of the bridge are now behind their evidence, and the evidence was a
    footnote under a paragraph this project has quoted for weeks.** The record's own memo listed
    four open threads on 2026-08-10; two were pulled the same day and one of them paid for
    everything. **Andreas prints, at the foot of pp. 631-632, a statement signed by four men who
    used the branch bridges** — J. D. Caton, John Bates, Charles Cleaver and John Noble, agreed
    at a meeting of old settlers late in the fall of 1883 and handed to the editors by Bates.
    It is the only description anybody wrote of how these crossings were put together:
    abutments of logs in the shallow water near the banks, **two "bents" of four heavy logs
    resting on the bottom in deeper water**, stringers of heavy logs from the abutments to the
    bents and between them, **puncheons or split logs for a floor**, about ten feet wide,
    **without railings for the first few years, after which guards or railings were added**, and
    **about six feet above the water, "so that teams passed under them on the ice freely."**
    Source record: `old_settlers_bridges_1883`, tier 2.
    **What it corrects, and none of it is corrected yet.** `pier_spacing_m` puts fifteen cribs in
    the river on the archetype's default; the letter says two bents. `pier_kind` is `crib`, and
    this record argued its way there by treating the Kinzie Street page's type-word "Bent" as
    modern editorial classification — it is the settlers' own word, and Cleaver, the eyewitness
    that argument leaned on, signed it. `clearance_m` was demoted to `inferred` here for want of
    a page; the page exists, and the dossier's `[DOC]` tag was right. The deck is the archetype's
    and the letter states it. **Every one of those is a mesh input**, so the record cannot move
    without the GLB moving with it, and this commit deliberately changes no value and no
    confidence tag: it lands the source, the memo, the liberties updates and the notes that say
    on each attribute's own face that it is behind its evidence. **The repair and its bake are
    one slice and it is the next one.** (It was, and it landed the same day — § 24.)
    **The work order**, so the next slice does not have to re-derive it: `bridge_timber` builds
    intermediate supports from a spacing, and the evidence is a count and a form, not a spacing —
    two bents at the thirds of a 71.83 m span is a different parameterisation, not a different
    number, so the archetype changes before the record does. `pier_kind` wants a `bent` value
    (four heavy logs standing on the bottom) beside `crib`. `clearance_m` moves to `documented`
    with this source. `railing` stays `false` and its note changes from an argument from silence
    to a reading of "the first few years". L29 moves to **Resolved** when the mesh shows two
    supports, and not before.
    **Two negative findings came with it, and they cost as much to establish as the positive
    one.** Neither 1834 sheet draws this bridge. Both were inspected at the crossing's own fitted
    pixel rather than by eye — invert each sheet's committed GCP affine at the record's deck line,
    fetch that IIIF region — and on both, the street stops at the waterline: a platted street is a
    dedication, not a structure. The thread the memo rated most promising, "the 1834/1835 Wabansia
    and Kinzie's Addition plat", turns out to be `hathaway_1834`, a sheet already in this dataset
    and already georeferenced, which is its own small lesson about open-thread lists. And on
    Hathaway a hatched, ladder-like mark sits in the channel within 35 m of the crossing and reads
    convincingly as a plank-and-stringer bridge symbol at moderate zoom; at full resolution it is
    the letter **H** of "BRANCH", lettered down the water. It is written down here so that it is
    found once rather than discovered twice.

24. **FIXED — two bents, not fifteen cribs, and the repair changed a parameter rather than a
    number.** § 23's work order landed the same day it was written, record and archetype and bake
    in one commit. `pier_spacing_m` is gone from `bridge_timber` and from the record;
    `pier_count: 2` (`documented`) replaces it, `pier_kind` is `bent`, `clearance_m` is promoted
    to `documented` on the 1883 statement, and the floor the archetype had been supplying in
    silence is stated as `deck_kind: puncheon`. The river carries three spans where it carried
    sixteen.
    **The parameter was the fault, not the value.** An archetype that divides a span by a spacing
    can only ever produce a colonnade, and a spacing is a builder's convenience that no witness
    would ever record. What a man who drove a team across a bridge remembers is *how many* stood
    in the water and *what they were made of* — so the input is now a count and a form, and the
    spacing survives only as `PIER_SPACING_FALLBACK_M`, the thing a bridge falls back to when
    nobody described its middle. Changing 4.5 to 23.94 would have fixed this bridge and left the
    next one to be found by the same accident.
    **What the confidence view now says, and it says more than it did.** `clearance_m` is one of
    the attributes that says what this structure WAS (a bridge's documented description *is*
    dimensional — see `bridge_timber_params`), so promoting it takes the deck and the stringers
    out of the half-dithered state the `inferred` tag put them in, and the bents come out solid
    because both their count and their form are attested. That is the first time in this dataset
    that evidence has made something *less* dithered.
    **And what it still cannot say is where they stood.** The letter locates the bents by depth —
    "resting on the bottom, in deeper water" — which is a locator this project cannot use: no
    source gives the channel's bed profile and nothing below the waterline is modelled. They are
    built at the third points because that is what a builder would do with three roughly equal
    runs. So the chip on `pier_count` grades how many and a visitor sees exactly where, which is
    the `chimneys` situation of § 19 arriving at a different structure. **L31** is where it is
    admitted, and it carries a second omission the repair created: three spans make each stringer
    run 23.9 m, longer than any timber anybody was moving, so those runs were spliced somewhere
    and nothing says where. The mesh shows one log per bay. **L29 moves to Resolved** — and only
    now, because the entry itself said it would stay until the mesh showed two supports.
    **One limit of the mesh is worth stating on its own**, because it is the most specific phrase
    in the source. *Resting on the bottom* is what distinguishes a bent from a driven pile bent,
    and above the waterline the two are the same picture; `_log_bent` differs from `_pile_bent` by
    four heavy logs against three light ones, which is what a visitor can actually see. The rest
    of the distinction lives in the record and in this file.

25. **The first building whose footprint is evidence, and a correction to our own dossier that
    changes what it is.** `hogan_store` — the log store at the west end of the Lake Street block
    in which the United States opened a post office at Chicago on 31 March 1831 — is the eighth
    structure and the first BUILDING here whose outline is not a placeholder. Andreas gives its
    size twice, in two independently written passages: "The building was twenty by forty-five feet
    in size, was partitioned off so as to serve as a post-office on one side, and as the store of
    Brewster, Hogan & Co., on the other", and "the store only occupied an area of forty-five by
    twenty feet". 45 × 20 ft is 13.716 × 6.096 m and the footprint is tagged `documented`, which
    no building footprint in this dataset has been before. **What is documented is the SIZE and
    not the plan**: which axis runs along the street is nobody's evidence, so that assignment sits
    on the facade bearing in the position note, where rotating the building is what changes it.
    **This is also the first record here with nothing conjectural in it**, which is not a boast —
    it means its gaps are gaps in the sources' precision rather than holes filled by invention.
    It does mean the popup's empty "What we made up here" state is finally exercised by real data,
    which § 11 recorded as unexercised.
    **The correction is the more useful half.** `docs/research/03-structures-north.md` § 4 dates
    the post office's move to the Franklin and South Water address from 2 November 1832, the day
    Hogan succeeded Bailey as postmaster, and calls that the 1835 office. Andreas says twice that
    the office was still at Lake and South Water through 1833 and moved **about July 1834**. The
    dossier's conclusion survives and its chronology does not: the 1832 date is the postmaster's,
    not the building's. The conflation is traceable to the Currey page the dossier used, which
    makes the appointment and the move one sentence — and which also supplies the "south west
    corner" that Andreas never gives. Source record `chicagology_first_post_office` says on its
    own face where it is followed and where it is not. **The consequence for the scene**: on
    1835-07-01 this building is a store that used to be the post office, and the town's actual
    post office is a different, unmodelled building about 100 m east, of which nothing survives
    but a street junction — it would be the most invented building in the dataset and it is
    written down rather than built (`docs/RESEARCH/hogan_store.md` § 4).
    **The weak point is survival, not geometry, and it is stated on the record.** The building is
    attested standing to about July 1834 and no source reached follows it past that; it is placed
    in a scene set eleven months later on the continuity argument, with the counter-argument —
    Lake and South Water was the corner most exposed to the 1835 boom — in the same note. If
    evidence turns up that it came down first, it belongs in `exclusions.json` and this record
    leaves the scene.
    **One smaller thing came out of the same page and is recorded rather than acted on.** Currey
    has Thompson's 1830 plat laying out streets "uniformly 66 feet wide"; every position in this
    dataset offsets by half of an **80 ft** street, from the widths annotated on Hathaway 1834.
    The difference is 2.1 m, an order of magnitude inside the georeference's own error, so nothing
    moves — but the two cannot both be right about the same street, and the reconciliation worth
    testing is that they are not about the same street. See `docs/RESEARCH/hogan_store.md` § 5.

26. **What was left out is readable in the walkthrough, and enforcing it found the one file
    where rule one was never checked.** `data/exclusions.json` — fourteen researched
    structures with the evidence that dates them, plus a four-item watch list — has existed
    since the scaffold and has been read by agents only. A visitor standing in an empty lot
    cannot distinguish three different statements: nobody researched this, the evidence
    dates it after the scene, or it had already come down. The first is a gap in the work
    and the other two are findings that cost research to establish. The Evidence panel now
    carries them under **What is not here**, derived per scene by `compile_scene.py` with
    the citations joined, below the liberties and in the same `<details>` entry, because
    they are the same kind of disclosure.
    **The chip is the record's field, never a phrase derived from an absence.** Ten entries
    carry `earliest_scene` and show "not until 1837"; `kinzie_house` and `ouilmette_cabin`
    were excluded because they were GONE, carry no such field, and get no chip — stamping
    one on them would be an invention on the panel that exists to admit inventions. The
    smoke asserts that discriminating pair rather than a count, and asserts that a building
    the visitor can walk up to is *not* on the list, which a section dumping the whole
    dataset would still have passed.
    **The list states what it is not**, and that sentence is a smoke assertion too: eight of
    roughly forty researched structures stand, so a fourteen-item list of absences with no
    such note reads as "this is what is missing", which would be the largest false claim the
    panel could make.
    **Two rules arrived with it, and the first is embarrassing in the useful way.** AGENTS.md
    rule 1 is that every `source_id` resolves in `data/sources/`; `exclusions.json` was the
    one file where nothing enforced it, because until now nothing read it — a citation there
    could have named a source that never existed and the gate would have stayed green.
    `check_exclusions` holds it to the same standard as a structure record: a slug id, a
    name, a stated reason (an exclusion without one is a deletion with a filename), and at
    least one citation that resolves. The committed file passes unchanged; the value is that
    the next entry cannot. The second is the date gate read backwards: an entry dating a
    building to 1837 is a correct exclusion from 1835 and a WRONG one from 1837, and no
    comparison against the records can catch it because an excluded structure has no record
    to compare with. In a year-parameterized project that is exactly the check worth having
    before the second scene exists rather than after.
    **The watch list is deliberately not shown.** Its four items are structures whose 1835
    status is uncertain rather than settled, and one of them (`western_hotel`) is standing in
    the scene — putting them under "what is not here" would be false about the one thing the
    section is for. Their uncertainty belongs on the records and in the provenance popup,
    which is a different slice and is not queued.
27. **The sidecars are re-derived by the gate now, which they were not.** `compile_scene.py`
    writes what the renderer reads and the outputs are committed so the site needs no build
    step — an arrangement that only holds if drift is a failure. Nothing recomputed them, so
    a record edited without a recompile shipped a walkthrough quoting the previous dataset
    with every citation still looking authoritative. `--check` re-derives to memory and
    compares; `check.sh` runs it, the same way it already re-derived `liberties.json`. The
    eight committed sidecars and the index were byte-identical on the first run, so this
    switched on with no repair behind it. What it does NOT check is the direction the
    staleness gate covers — that the GLB matches the record — and neither of them can see a
    record that is wrong about the town.

## Next

**S5 — more structure records**, which is now the binding constraint: seven structures stand
where the sources describe roughly forty, and one of the seven is a bridge. Note the coupling discovered on 2026-08-10, because it sets
the shape of the work: `tools/compile_scene.py` writes an `asset` path for every structure that
resolves into the scene, so a record committed without its GLB makes the renderer fetch a file
that is not there — a 404 the smoke correctly fails on. **A structure record and its bake are one
unit.** An agent without Blender can prepare the record and the research memo, but the pair has
to land together, so the bake workflow's PR is part of the same slice rather than a follow-up.
**That coupling is now enforced rather than remembered** (2026-08-10): editing a value a
generator reads makes the committed GLB stale and `check.sh` fails until the re-bake lands with
it. It was then exercised for real by the Wolf Point repair the same day — the rename turned the
tavern's asset stale on the spot and the branch could not go green until the bake landed on it,
which is the whole point of writing the check, and again the same day by Miller's second chimney,
and a third time by his frame range.
**The repair list refilled itself from the archive rather than from the gates, and emptied again
the same day** (2026-08-10, § 23 → § 24). Every previous entry on it was found by a check: a
misspelled attribute, a name read as being about the wrong half of a building. That one was found
by reading a page, and it is now **DONE** — the record, the archetype and the bake landed
together, `pier_count: 2` replaced `pier_spacing_m`, and the queue is empty again. What it leaves
behind is a shape worth reusing rather than a task: when evidence and an archetype disagree, check
whether the archetype is asking for the wrong *kind* of number before changing the number it has.
The older account of the queue, still true of everything before this entry: The last entry —
`miller_house` recording a `documented` frame range with no side, width, depth or storey count —
landed 2026-08-10 with its bake (§ 20), and it was the fourth and last of the faults the omission
gate opened. Three of the four were spelling; the fourth was a name read as being about the wrong
half of a two-part building, which no spelling check would have caught. Nothing new is queued
behind it, so **S5 is additions again**: eight archetypes and about forty researched structures
against the six that stand.

**S9 — streets, roads and paths**, queued behind S2e at Kevin's direction. Geometry generated from the Thompson module rather than traced; surface is unpaved earth with plank walks, NOT a graded roadway; elevations drape on the heightfield because nothing was graded until 1855-58. See ROADMAP § S9 for why each of those is a trap.

**S5a — Fort Dearborn**, the next building. Its position is settled (E +1152, N +221, cross-checked to 35 m) and the coastline gate Kevin named is cleared, but the FOOTPRINT has no source yet: Wright labels the reservation and draws no plan. Also unsettled, and needed before it is drawn: what the fort actually was on 1835-07-01.

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
