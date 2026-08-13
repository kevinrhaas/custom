# STATUS

Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-13 · **Phase:** S0, S1 (datum), S2-partial (terrain + river at the
forks), S4-partial (frame_tavern, log_dwelling, bridge_timber), S9-partial (dated visible
street layer), S10-partial (665-roof ledger + 108 anonymous roofs) and R1 (renderer)
complete. **K1 (inferred residents) complete through phase two; K7 (the platted block and lot
grid) complete through phase one, and phase two's placement gate is closed — every generated
placement in the dataset is out of the platted roadway and all three generators enforce it;
K9 (navigation UI) complete.**

**Current expansion:** the 1835 scene resolves **222 structure records**, and **152 households /
188 persons** stand behind them (76 documented, 20 derived, 92 inferred). 108 records are tagged
`inferred_anonymous` and display as flagged review massings; **83 of those now have an argued
occupant** rather than being anonymous count-units, and 162 structures name a household on the
building card. They begin—rather than complete—the owner specification's 665-roof target. Exact
anonymous presence, footprint and lot position remain conjectural, and the adoption changes none
of that: what it adds is a reason for the roof, not evidence for it. **No inferred person has a
name, and none should**; no figure is drawn (L1). The remaining North expansion is still gated
behind unified terrain and hydrology coverage.

**The weakest joint in the population layer, stated plainly:** no period trade table for a
comparable western town exists in `data/sources/`. Every occupation ratio is therefore derived
from five in-dataset calibrations rather than cited, and the arithmetic is written out per trade
in `docs/RESEARCH/residents_1835_inferred.md`. That is a real gap, not a rounding error.

**Water vegetation correction:** emergent plants now use true distance to shoreline and are
limited to the shallow eight-metre marsh edge. Non-emergent flora and every woody placement are
rejected over the traced water mask, and since 2026-08-13 the mirror of that rule holds too: a
species whose recorded `substrate` is `open_water` — a pad that floats — is refused every station
on dry ground. A first-run navigation guide can be dismissed and reopened
from Settings.

**Parallel phase-two planning:** three non-rendered parcel recipes now cover 84 additional South
Division roofs (66 principal, 18 ancillary), 55 West Division roofs (44 principal, 11 ancillary)
and 60 North Division roofs (45 principal, 15 ancillary). Together with the implemented 48 they
reserve 247 slots without exceeding any 665-roof family cap. They remain plans, not scene claims:
the South set waits for physical-roof reconciliation; 35 West roofs also wait for a unified
westward map/terrain extension to E -700 m, and the outer North pass waits for N +760 m coverage.
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
| Structure records | **184 in the 1835 scene** — 76 pre-existing evidence records plus 108 visibly tagged anonymous recommended infill records; record count and physical-roof count are separately reconciled |
| Terrain epochs | registry written; `e1834_harbor_cut` active, geometry layers **not yet built** |
| **Datum** | **VERIFIED** — Wright-derived, Hathaway- and OSM-checked, RMS 17.5 m, re-derivable from traces |
| **Generator pipeline** | **WORKS** — pinned Blender 4.5.3, `frame_tavern`, 496-tri Sauganash from the record alone |
| **`frame_dwelling`** | **BUILT 2026-08-11, NO RECORD USES IT YET** — the archetype that unblocks houses: 1/1.5/2 storeys, knee wall and gable-end attic window, rear ell read off the footprint polygon, stoop or small roofed porch, and `construction` finally moving vertices (stud module places the openings, clapboard butt joints land on stud lines, braced frames get the girt band a balloon frame has no line for). Golden params + `docs/RESEARCH/archetype-frame_dwelling.png`; 248-730 tris per house. `GROUND_CONTACT: perimeter` verified against the mesh — every edge of the footprint polygon carries a wall at z = 0, worst gap 0.0 mm, nothing below the base of the walls |
| **`outbuilding`** | **BUILT 2026-08-11, NO RECORD USES IT YET** — the highest-count-per-effort archetype in the plan, and the one that gives the town yards instead of eight isolated public houses. A FAMILY, not a shape: `construction` log/plank/light_frame drives three different wall routines, shed roofs are first-class rather than a fallback, `open_sides` turns any subset of elevations into posts-and-plate, and `door` is none/man/stable/wagon — a boolean is refused with a message saying why. `board_gap_m` alone is the whole difference between a stable and a corn crib. Five golden variants from a 1.25 m privy to a 13 m hotel stable, 272-2008 tris; `GROUND_CONTACT: perimeter` verified on ALL FIVE against ground-plane EDGES rather than vertices (the first check compared vertices and produced false failures on a 13 m wall that is one quad). Discharges the stable half of L10; **the yard half stays open** — a fence line with two gateways is an enclosure, and building it out of an outbuilding would be calling a fence a building, so L10 needs NARROWING rather than resolving |
| **South Water Street** | **BUILT 2026-08-11** — sixteen commercial records land the town's business street, which the model held none of: Peck's store, both newspaper offices, Harmon & Loomis, Madore Beaubien's log house, Bates's auction room, the Beaubien homestead, Dole's warehouse, both Carpenter shops, Frederick Thomas, the old bank building, Pruyne & Kimball, J. H. Kinzie, Jones, and Thomas Church on Lake. One footprint is evidence (Carpenter's 16 x 20 ft log shop — the dataset's SECOND real footprint); fifteen are invented inside the documented 55 ft South Water lot cap. **What this street knows is *who* and *where*, and almost never *how big*.** Two records carry `review_required` (the Beaubiens, whose history runs straight into the August 1835 removal and the reservation pre-emption) — which blocks the 1835 scene from `released` until consultation happens. Two unresolved reads are flagged on the records themselves: whether Harmon & Loomis's building IS the *Chicago Democrat*'s building (they sit 37 m apart and Andreas gives no side), and whether Philo Carpenter's Lake Street log shop still stood after he built on South Water in 1833 |
| **Renderer** | **WALKABLE AND NAVIGABLE** — three.js r0.185.1 vendored, pointer-lock + touch, confidence view, provenance popup, live compass and a north-up overview derived from the loaded heightfield and structure footprints |
| **Navigation index** | **COMPLETE FOR COMMITTED DATA** — Settings searches all 76 scene structures and all four verified intersections, with aliases and recorded location text; intersection positions are compiled from `data/traces/street_control.json` rather than copied into renderer code. Compass, overview map and the live 1835/current street-name readout are independently persistent toggles. A fourth persistent setting switches every visitor-facing navigation measurement between Imperial (the default: ft, mi, mph) and Metric (m, km, km/h) without changing the metric scene data. The readout reports the corridor underfoot, an intersection when two centrelines are near, and the next cross street up to 70 m / 230 ft ahead. |
| **Smoke** | **PASS 2026-08-13.** `tools/check.sh` (which now runs the changelog contract check as a step) and `node tools/smoke_renderer.mjs` both pass in the foreground: **359 assertions** (181 mobile + 178 desktop), zero page errors, at both release viewports (390×780 and 1280×800) — the two halves run as separate foreground commands, because a full pass now exceeds the ten minutes a single one gets here. Draw calls and triangles at the spawn station: **62 / 330,283** mobile and **65 / 332,455** desktop, both inside the 80 / 1,000,000 budget for Full detail; the horizon band is 562 triangles at both. The suite rejects a second flora surface, compares every detailed plant root and every structure anchor — including Exchange Coffee House — to the authoritative terrain/water sampler, asks the flora placer itself where each species may stand, and exercises both unit systems. Mobile: 61 draw calls / 287,857 triangles / 3 fps; desktop: 71 / 425,560 / 1 fps, both under the 80 / 600,000 release budgets. |
| **Flora** | **the sward is in; the false far-field surface is out** (2026-08-11) — `renderers/web/js/flora.js` plants the graminoid matrix, forbs, emergents and low shrubs from `data/flora/`. July phenology remains enforced in renderer and data. Near/middle plants root on the exact terrain surface and water emergents on the water surface. The former solid canopy at plant-top height was the apparent second ground seen on real devices; it is removed, and unresolved distant prairie colour now stays on the sole terrain surface (L80). **Since 2026-08-13 each community is planted at its own recorded `cover.matrix_fraction`** — a field the records carried, the validator gated and the renderer had never asked for — and each is split by the published `substrate` of its species, so a floating-leaved aquatic is planted over water and never on the bank it was standing on. |
| **The ground's claims, in the app** | **done** (2026-08-10) — the Evidence panel's *The ground you are standing on* reads graded claims off `terrain_spec.json`, derived per scene by `compile_scene.py` and re-derived by `check.sh`; the same slice added reasoning and geometry-state checks so those rows are no longer silent promises. |
| **What a source is, in the app** | **done** (2026-08-11) — citations now carry the document a modern page reprints (`transcribes`) or the reading that it reprints none, plus each source's own `what_it_supplies` / `what_it_does_not_supply`, so the ladder a visitor sees includes the reason it is the ladder. |
| **Liberties, in the app** | **done** — the Evidence panel lists the liberties derived from `docs/LIBERTIES.md` by `tools/compile_liberties.py` and re-derived by `check.sh`; the provenance popup shows the ones taken with the building you are inspecting; and the gate checks the document *for gaps* in both directions — refusing any conjectural value (footprint, position, a terrain claim, or a stated form attribute) that no liberty admits to, and equally any attested value the archetype or terrain generator never reads and no liberty owns up to leaving out |
| **The platted street module** | **MEASURED AND VISIBLE** — street corridors and widths remain committed in `data/traces/vectors/street_corridors_1834.json`, with Lake and Randolph named from committed control and re-derived offline by `check_street_module`. `data/streets/1835.json` now adds seventeen dated paths and keeps the 80 ft legal corridor separate from L79's 5.8-10.5 m visible travelled strips. `compile_scene.py` joins their citations into the sidecar index; the renderer drapes them on the ground, clips them at water and clears vegetation only from the track. South Water and Lake read as principal graded earth, ordinary streets as worn native earth, and no gravel, plank roadway or hard paving is shown. North Water's curve and every rut/track width remain explicitly conjectural. |
| **The lake shore** | **TRACED, NOT BUILT** — `shoreline.geojson`: the harbour reach, the 1834 cut, the old southward channel, the sand bar as an island and the mainland shore, E +314…+1570 off Wright 1834. Vectors only; no elevation, no mesh, nothing east of the box renders yet |
| **Published** | `site/chicago/4d/` (14.31 MB of a 25 MB budget) + a tile on the Chicago landing page |
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
- **The prairie appeared to be a second terrain layer.** The far vegetation simplification was
  a solid horizontal sheet at plant-top height. On real hardware it hid building foundations
  and plant roots while the walker remained correctly on the actual heightfield below — most
  clearly at the river bank and Exchange Coffee House. The sheet is removed, not promoted to
  terrain. Walker, buildings, streets, trees and detailed flora now share one explicit surface
  sampler; emergent roots use the water surface. The far field is terrain texture until a
  porous, terrain-rooted replacement can be built (L80).

## What does not exist yet

- **The full 665-roof inventory is not built.** South 48 plus North 60 anonymous slots are visible; remaining parcels, coordinated world extensions and the 35-family canonical archetype library are still open. The reconciliation and family crosswalk are committed handoff controls.
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

## Fixed 2026-08-13 (second occurrence) — the changelog was union-corrupted by a merge again

**The hazard K12 says is still open is not theoretical, and it recurred within the day.** `main`
carried an unparseable `renderers/web/js/changelog.js` from the merge that landed K16: the v72
entry *"The grass stopped in a straight line across the prairie"* had lost its `] },` and swallowed
everything below it, and the K16 entry rode in with a duplicate `v: 72`. Same mechanism as the
first occurrence — `.gitattributes` merges this path `merge=union`, the union driver runs DURING
the merge, and **nothing in this subtree runs on a commit git wrote**. Both parents were green.

Repaired inside the facade-weathering PR, which is the merge that found it: the terminator is
restored, the K16 entry is renumbered **v74** and moved above v73 where its own `ts` (16:44,
against v73's 16:03) says it belongs, and this slice's entry is **v75**. No entry anybody has read
was renumbered — while the file was broken on `main`, none of them was readable.

**What caught it was the standing instruction, working exactly as written**: `tools/check.sh` runs
the contract check as a step, and running the gate AFTER the merge rather than only before it is
what turned a silently broken `main` into a named failure (*"line 27: entry v72 opens at bracket
depth 3, not 1"*). What did NOT catch it is unchanged and is still ROADMAP § K12: no gate runs on
the merge commit itself. Two occurrences in two days is the argument for taking one of K12's two
candidate fixes — the subtree's gate on pushes to `main`, or a merge driver that understands the
literal — rather than continuing to rely on the next agent to merge running the check by hand.

## New 2026-08-13 — the town was the colour of new lumber, and its own records said otherwise

**K4, first half.** `paint` is authored on **174 of the scene's 243 phases** — 142 `unpainted`, 14
whitewash, 12 red, 5 masonry, 1 white; graded 163 `derived`, 9 `inferred`, 2 `documented` — `tools/validate.py` has gated it since the schema was
written, and the dossiers say what it looked like: the fort *"serviceable, weathered,
whitewashed/unpainted log-and-brick"*, the Dearborn Street bridge *"weathered, patched, sagging"*,
and `docs/RESEARCH/green_tree_tavern.md` § 4 on the reading that makes it matter — the Sauganash's
white paint is remarkable in the sources *precisely because its neighbours were not*, which only
holds if the town around it is not white either. **`generators/common/mesh.py` resolves all 142
through one warm fresh-sawn tan.** The owner's finding — *the buildings read as freshly painted and
identical* — is those two facts, and neither of them is a bug.

`renderers/web/js/facade.js` now moves each building toward its own greyscale by an amount derived
from its own stated finish and its own `documented_range.from`, and gives it a per-building
lightness offset of up to ±7.5 % keyed on the structure id. Memo:
`docs/RESEARCH/facade_weathering_1835.md`; admission: `docs/LIBERTIES.md` **L91**.

- **It reads no material names, and that is a pipeline finding rather than a preference.**
  `tools/bake.sh` runs gltf-transform over `assets/web/`, whose palette pass MERGES materials and
  renames the survivors `PaletteMaterial001…`: the Sauganash master carries
  `wall / roof / log / shutter / glass` and the file a visitor downloads carries three paletted
  materials with the colours in a texture. **38 of the published building assets are in that
  state.** `tools/smoke_renderer.mjs` loads the masters from `assets/gltf/` and the live site loads
  the derivatives from `data/gltf/`, so a name-keyed treatment would have been gated on one
  pipeline and shipped on another — which is the shape of the nightly-bake failure recorded below.
  Weathering here is therefore the REMOVAL of colour: each fragment is mixed toward its own
  luminance, so a tan board greys and a near-neutral window void barely moves. The surfaces that
  would have needed protecting protect themselves, arithmetically, in both pipelines. **Any future
  per-surface facade treatment is blocked until the derivative carries surface identity** — a
  change to `tools/bake.sh` and to `docs/GLB-CONTRACT.md`, and so a proposal, not a slice.
- **The gate could not see it, and the first version of the assertion failed against a working
  shader.** `readbackSignature()` reduced a frame to a grid of LUMINANCES, and mixing toward
  luminance is very nearly luminance-preserving by construction: on a frame of the Green Tree the
  luminance grid moved **0.09 mean / 1 worst** while chroma moved **0.97 / 11.9**. It now carries a
  chroma grid beside the luminance one and the smoke compares that.
- **Measured across the 242 committed sidecars.** 141 unpainted, undocumented phases silver
  **0.462–0.800**; 167 structures carry a non-zero silvering; 5 masonry and 68 finish-less
  structures carry none. Tone spread **0.1406**, peak **0.0715** against the ±0.075 bound. The 128
  generated roofs — the ids that would betray a weak hash, sharing 22 leading characters — take
  **127 distinct tones**. Draw calls unchanged: **35 building batches for 242 structures**, because
  the channel is two floats per vertex inside the existing batches.
- **The two documented finishes are untouched, and the frame is checked for it.** The Sauganash's
  white and St Mary's get neither the silvering nor the tone offset, and an assertion frames the
  Sauganash and requires it not to move when the treatment is switched off — without which "the
  treatment reaches the pixels" would be equally happy with a shader that weathered everything.
  This leaves St Mary's, whose documented finish is `unpainted`, as the one unweathered unpainted
  building in the town; accepted rather than special-cased.
- **What it does NOT claim.** That any particular building was this colour. `paint` is `derived`
  on 163 of the 174 phases that state one and `inferred` on 9, and no grade moved; the treatment draws the finish the
  record already claimed instead of overriding it with a default. Nothing here is a new reading of
  a source. Board tone and board width WITHIN a wall, hewn versus round logs, and weathering by
  elevation are the archetypes' half of K4 and all still open — they need a bake.

## Fixed 2026-08-13 — the changelog was broken BY A MERGE, and both parents were green

**`renderers/web/js/changelog.js` did not parse on `main`, and neither did its published
mirror.** The What's-new tab imports it, so the tab was dead on the deployed site; Manager and
the polecat.live launcher parse the mirror, so this project reported no releases at all. 64
entries, back to the first building, were in the file and reaching nobody.

**Exactly one `] },` was missing** — the terminator of v64 *"Twenty-three buildings were standing
in the street"*. Every entry below it was nested inside that entry's `items` array, which is why
node reported the syntax error at line 565, the end of the file, 540 lines from the damage. A
second entry rode along with a duplicate `v: 64`: two branches finished 33 minutes apart, each
stamped its entry on its own branch, and neither knew the number was taken.

**The mechanism is the part worth keeping, because no existing gate could have caught it.**
`.gitattributes` merges this file with `merge=union` — a deliberate, documented choice, because
two branches each prepending an entry collide every time and union keeps both instead of
conflicting. But the union driver runs DURING THE MERGE. Merge `65c8de1` has two parents,
`cbe494c` and `60a78d0`; **both parse, and the merge of them does not.** Every gate in this
project runs on a commit somebody wrote. Nothing ran on the commit git wrote.

- **The repair.** The terminator is restored. The duplicated entry is now **v67** and sits at the
  top, where its own `ts` (12:26 UTC, the newest in the file) says it belongs. No entry anyone has
  read was renumbered — while the file was broken, no entry was readable at all.
- **`tools/check.sh` now runs the changelog contract**, as a step like any other. AGENTS.md has
  always instructed an agent to run `check-changelog.mjs` by hand before merging; a hand-run check
  is exactly the thing a merge-time corruption evades, and the file that gates every commit did
  not gate this one. The generic *renderer modules parse* step did catch it — as `parse error:
  renderers/web/js/changelog.js`, which names a file and not a defect.
- **The contract check reads the literal's SHAPE as text before executing it**, because executing
  it is the weaker test in two ways. A swallowed entry is still a valid object literal, so it need
  not raise a syntax error at all — it can simply vanish from the array with the file loading
  cleanly. And Manager and the launcher never execute this file; they walk it bracket-aware, so
  the shape IS the contract. Every entry must open at bracket depth 1; one that opens deeper got
  swallowed, and the entry above it is the one that lost its terminator. Verified against the real
  corrupted file from `main`: *"line 25: entry v64 opens at bracket depth 3, not 1 — it is nested
  inside entry v64 (line 18), which is missing its `] },`"*. The header count from the text walk
  is also compared against `CHANGELOG.length`, which is what catches the silent half.
- **What this still does not cover.** The check now runs before every commit and before every
  merge an agent performs, but nothing in this subtree runs on a merge commit itself — the
  repository's CI is outside `chicago/4d` and outside this lane's scope. A human merge on GitHub
  can still publish a union-corrupted changelog. The narrow version of that hazard is now loud
  the moment anyone runs the gate; the general version is recorded in ROADMAP § K12.

## Fixed 2026-08-13 — the horizon timber was being deleted by its own texture

**S6a item 5, both mechanisms the item names.** The far-timber band draws the dossier's bodies
of woods at three, four and six miles as a silhouette on a ring, broken up crown by crown with
sky opened through the stand — `k` runs down to about 0.02 in a gap. At four hundred metres,
where the band is forty pixels tall, that is texture. On a six-mile body whose entire silhouette
is one or two pixels it is a **deletion**, and the band was carrying both failures at once.

- **Measured at the spawn station, with the pixel floor removed and then in place.** 281 of 900
  bearings carry a timber body. Without the floor the modulation drew **251 of 280** resolvable
  bearings at a pixel or more on the phone and **267 of 281** on the desktop — worst silhouette
  **0.18 px** and **0.31 px**, geometry solved and written into the buffer and too thin to land
  anywhere. With it: **280/280 and 281/281**, worst **1.00 px**. The band's triangle count is
  **562, unchanged** — the floor moves vertices and never their number.
- **The floor is on the RESULT, not a cap on `k`**, so it binds only where pixels are scarce: a
  400 m treeline is 40 px tall and keeps its gaps to the last per cent. Where a body's raw
  silhouette is itself sub-pixel the modulation is suppressed outright, because a texture that
  cannot be drawn can only subtract.
- **The band is therefore now solved against the live viewport.** `main.js` passes
  `pixelsPerRadian` off the renderer size and the camera's own field — 475 px/rad on a phone at
  its 94° clamp against 833 px/rad on a desktop at 55°, a factor of 1.75 the old fixed field got
  wrong in the direction that over-cuts a phone. A viewport change re-solves the band exactly as
  walking does.
- **The colour was one line of arithmetic answering a question the renderer never asks.**
  `hazeDisplayLinear()` ran the haze colour through ACES to reach the band's display value. The
  band is `toneMapped: false, fog: false` — its fragment is `opaque → colorspace`, so a linear
  vertex colour displays as the hex it decodes from — while the fogged ground is
  `opaque → tonemapping → colorspace → fog` with `fogColor` uploaded in the OUTPUT colour space,
  converging on that same literal hex. One decode each. The tone curve was applied to one end
  and to nothing it had to match: **16 red and 12 green** off the ground it touches, 69 in blue
  at `prairie_west`. Both ends report **#88a3c0** now. And the old value was **L 170 against a
  horizon sky of L 162** — a band *paler* than its own sky, which is what a distant treeline
  never is; it is L 159 now, three below.
- **The gate is every resolvable bearing, not a percentage.** A 90 % bar would have passed the
  desktop half of the defect (267/281 is 95 %). Three new assertions at both viewports: the band
  and `scene.fog.color` are one colour, no resolvable bearing is drawn under the floor, and the
  band was solved against THIS viewport — a floor measured in pixels is meaningless against a
  hard-coded field. Verified they bite by removing the floor: both viewports fail, with the
  counts and the worst pixel named.
- **What this does NOT claim.** The finding behind item 5 is photographic — *31 % of horizon
  columns carry any timber, 3.6 % across the central two-thirds* — and it was taken with a shot
  harness that is not in the release gate. **It has not been re-measured**, so no column figure
  is quoted here. What is measured is that the geometry it was measuring is no longer being
  thrown away, and that the band is darker than its sky rather than paler. `docs/LIBERTIES.md`
  L35 is revised in both directions; the 0.82 haze cap it exists to confess is untouched, and
  the distance compression it buys is unchanged.

## Fixed 2026-08-13 — the sward ended on a straight line, and the line was arithmetic

**A ring is a circle about the walker, so its outer edge is a constant screen row.** The
three-critic prairie sweep measured it and named the row: `TUNE.mid.radius = 27.0` predicted row
448.8 and the frame showed one at 450, straight across all 1280 columns. That is ROADMAP § S6a
item 3, and the reason it is arithmetic rather than a rendering artefact is the site: 4.30 ft of
relief across the whole 640 m box, so a fixed distance really does land on a fixed row. The gate
now measures it the way the finding was stated — bin the view by bearing, ask each bin how far
its own sward reaches, convert the distance to the row it lands on. **On the ring as it stood
those rows spanned 1.4 px.**

Every lattice slot now carries its own outer radius: the layer's nominal one plus a
world-anchored offset of up to **±3 m** at full detail (±1.6 m on a phone, about an eighth of the
ring at every detail setting), from smooth 4 m value-noise lobes with a per-slot dither over
them. Measured after: **5.9 px** of spread at 1280×800 and **17.4 px** at 390×780, the sward
reaching 25.0–28.4 m about a nominal 26.4.

- **Widening the fade would not have worked, and the reason is worth keeping.** The band is
  already 7 m, which is 18 px of frame at that distance. The line is not the ramp — it is where
  the ramp reaches zero, and a wider ramp still reaches zero everywhere at once. What removes a
  line is a boundary that is in a different place in each direction.
- **It is nearly free, by construction rather than by luck.** Triangles are paid for by the
  LATTICE, not by the fade, so a slot the fringe pushes beyond reach is dropped at rebuild
  instead of drawn at zero height, and the lattice grew by the amplitude to carry the ones it
  pushes in — with a symmetric offset the mean cost is `radius² + variance`, not
  `(radius + amplitude)²`. Measured A/B at 1280×800 at three fixed stations: open prairie
  **174 363 → 176 656** triangles (+1.3 %, 3 742 → 3 850 flora instances), settled town
  **389 369 → 389 253** (−0.03 %), river bank **350 109 → 350 105** (−4). Draw calls unchanged
  at 37 / 66 / 72. The cost lands where the sward is dense and nowhere else, which is the right
  shape for it.
- **World position, not camera distance.** The offset is a function of the ground alone, so the
  ragged edge does not swim as the walker moves and is the same edge whichever way they face —
  the pop-in defect one ring further out, avoided rather than traded for. The gate asks the
  placer (`flora.fringeAt`) instead of re-deriving the noise, and requires nine points to answer
  identically from two cameras 40 m apart.
- **The flowers had to come with the grass.** The forb ring ends within a metre of the mid ring,
  so a fringe on the matrix alone would have left the brightest objects in the field drawing the
  line the grass no longer does. It is gated on its RINGS rather than on its drawn edge: at
  3.4 m cells a 3.75° bin holds one or two forbs, so "the furthest one drawn" is a sampling
  statistic, and measured that way it reported a nine-metre hole in ground that has none.
- **The pop-in gate had to be made instance-aware to stay honest.** It asked the layer's nominal
  ring how faded an arriving plant was, and a nominal ring answers *zero* — a free pass — for
  exactly the plants the fringe pushes furthest out. It reads each instance's own `aChiRing`
  now. Same bound, same measured 0.0 % arrival height.
- **Verified the gate bites**, by putting the fringe back to zero: the boundary spread falls to
  **1.4 px** against a bar of 4, the forb rings span 0.00 m, and the world-anchoring check
  reports no variation at all. Three failures, on the code that shipped yesterday.
- **What this does not do.** It does not extend the sward. L80 still owns the compression — the
  terrain's own colour carries everything past the ring — and the mid-field targets in S6a items
  1, 2 and 4–7 are untouched. This removes a line the eye reads as an object in the world; it
  does not put vegetation where there is none.

## Fixed 2026-08-13 — a fade function that was producing a step

**The transition the owner asked for had been there all along, sampled once per stride.**
"Grass and flowers appear out of the ground as you walk towards them" (K3) read like a missing
feature, and `flora.js` has scaled every plant down over the outer band of its ring since the
layer was written. The defect is the RATE, not the absence: the ramp was evaluated on the CPU at
lattice-rebuild time and baked into the instance's height, and the lattice rebuilds only every
`TUNE.step.near` metres walked. 1.2 m of step against the near ring's 2.2 m band means a plant
went from nothing to **55 % of full height in a single frame**, once per stride, forever. A fade
that only updates when the thing it is fading is rebuilt is a step function wearing a ramp's name,
and it is invisible in review precisely because the ramp reads correctly on the page.

The ramp now runs per frame in the vertex shader against `cameraPosition`. What that cost, and
what it bought, is in ROADMAP § K3; three things belong here.

- **A flower head cannot just shrink — it has to come down.** Its origin is partway up a stem, so
  scaling in place leaves it in the air over a plant that is no longer under it. `aChiRise` and a
  world-space descent applied after the instance transform (the instance matrix carries a real
  rotation for tilted heads, so it cannot be folded into the local offset).
- **The `fade < 0.35` head gate was itself the worst pop in the field**, being a step in the
  middle of a ramp on the brightest object in the frame. Heads have their own inset ring now, and
  the same heads are drawn: the ring reaches zero exactly where the plant's ramp passes 0.35.
- **The guarantee is geometric, not empirical.** The lattice is inset from the fade ring by the
  rebuild step, so a plant is always placed, at zero height, before it is near enough to be worth
  any. The residual is one frame of overshoot — the rebuild fires on the frame that carries the
  walker past the step — which is 0.024 m at 60 fps, about 1 % of a plant's height, and it is
  written down rather than rounded away. The near ring's visible radius is 0.6 m shorter than it
  was, which is the price of the inset and is left as a coverage question in K3.
- **The gate now walks.** Twenty 0.15 m paces at 390×780 and 1280×800, checking every plant that
  appears in front of the walker: measured worst arrival **0.0 %** of full height against a 10 %
  bar, plus a check on the ring geometry so the margin cannot be tuned away later. Triangles
  564 821 desktop against 564 681 before — a rounding error, and no new asset.

**And the gate was measuring the weather.** Running the baseline before touching anything turned
up an unrelated red: *"turning it off restores the render"* failed about **two runs in three on
main**, at 390×780, with a worst-cell delta of 9 against a bar of 8. The assertion compares two
captures of the same scene to decide whether switching the confidence view off leaves anything
behind — and the wind blows between them, at 1–3 fps under the software rasteriser, so most of
the residual it was measuring was swaying grass. The tolerance had already been widened once for
exactly that reason, which is the tell: a gate whose bar is set by its own noise is a gate that
will be widened again. `main.js` gains a harness-only `setAnimationHold` — keep drawing, advance
nothing — and the three captures are taken under it. The residual is readback noise now, so the
bar **tightened** from mean 0.5 / worst 8 to mean 0.1 / worst 3, and the assertion above it
(*confidence view changes the render*) got strictly harder, because sway can no longer supply any
of the difference it has to find. Two consecutive full runs green at both viewports.

That closes the debt the bake-gate entry below records as owed: the flora clock is frozen during
capture, and the bound was tightened rather than widened.

## Fixed 2026-08-13 — the nightly bake had been red for days, and nobody could see it

**The placeholder gate forbade the upgrade the bake exists to perform.** `generators/build.py`
writes `assets/gltf/<id>__<phase>.glb` for any record whose archetype has a generator, and every
`recon_*` record has one — so the canonical Blender bake lands on exactly the filename
`generators/inferred_placeholder.py` claims, and the gate then rejected the real bake for not
being the pure-Python placeholder it was built to replace. A second conflict rode along:
`tools/bake.sh` runs gltf-transform over `assets/web/`, so demanding byte-equality with the
master asserted that compression never happens. **What made it invisible is the shape worth
remembering** — the gate passed on every developer machine and failed on every CI runner, because
the difference was whether `npx` could reach the network. A green local gate was reporting on a
pipeline it was not running. The gate now compares only the master against the record, requires
the derivative merely to exist, and stands aside for any asset whose manifest entry says
`kind: generated`, leaving that to the ordinary staleness check.

**`tools/publish.sh` was an accumulator, not a mirror.** It copied files in and never took any
out, so a retired asset shipped forever: 108 `__recommended_1835.glb` placeholders, orphaned when
the programme was renamed, were still being served to visitors long after nothing referenced
them. Deleting a file from the source tree was not a thing the published site could express.
Fixed by clearing the published `data/gltf` before copying; payload 19.16 → 18.55 MB at the time.

**Known flaky gate, deliberately not silenced.** `mobile 390x780: turning it off restores the
render` compares a frame captured before the confidence toggle with one captured after, while the
flora is still swaying. Observed failing twice at worst-cell delta 11 against a bound of 8 and
passing on the third run with no code change. The bound has NOT been widened — a release gate
loosened until it stops complaining is not a gate. The fix is to freeze the flora clock during
capture, and it is owed. **Paid 2026-08-13** — see the flora-fade entry above: captures now run
under `setAnimationHold` and the bound tightened to a worst cell of 3.

## Fixed 2026-08-13 — two defects the owner photographed, and what they taught

**The Clark Street headland was the map's own lettering.** Fixed 2026-08-13. What makes it
worth recording is that the trace had been *believed* against a measurement that disagreed
with it: the South Water georeference note recorded 79.6 m of residual at Clark against
18.7 m at Dearborn and attributed the swing to paper stretch. Both numbers were right and the
explanation was wrong. A 60 m local disagreement between two independent methods is a defect
report, not an error bar.

**`generators/terrain_gen.py --glb` had been unrunnable since `terrain_inputs` was
extracted.** `terrain_inputs_sha()` is called before `main()` inserted `generators/` on
`sys.path`; run as `python3 generators/terrain_gen.py` that path is `sys.path[0]` by accident,
run under `blender --python` it is not, and the GLB half died on `ModuleNotFoundError`. The
insert moved to import time. Nothing caught it because `tools/bake.sh` does not build terrain
and the terrain GLB is a rare, deliberate invocation. **The heightfield and the GLB are now
back in step**; the committed GLB before this run was baked at `--decimate-deg 0.04` and the
one after at `0.03` (see K14).

**The tree-placement gate and the river mask are two different questions.** `isWater` asks
"is this the river" and its threshold is 100 mm under the datum, which is correct for that
question and was silently wrong for "may a stem stand here". The release gate had a green
check on the first question while the owner had a photograph of the second failing. Both
checks are now present.

## New 2026-08-13 — the platted grid exists, and it found seven buildings in the road

**K7 phase one.** The block and lot grid is generated rather than traced:
`tools/generate_plat_lots.py` offsets this project's committed street centrelines by half the
platted corridor, intersects them, and divides the result into lots — 19 blocks, 152 lots,
re-derived byte for byte by `tools/check.sh`. Tracing the 1834 sheets instead would have baked
their 3.7–4.5 % paper stretch into every block face. The blocks are `inferred` because their
inputs are; the lot lines and the alley position are `conjectural` and stay that way, because
four lots to a face is a reading of ONE block (block 18 on the owner's Clark-reach crop). No lot
and no block is numbered — this project has never read Thompson's numbering off a sheet.

**The grid immediately paid for itself as a check.** Of 222 placed structures, 80 stand inside a
generated block, 120 stand outside the 19 blocks it covers, and 22 stand inside a platted street
corridor. Most of those 22 are within a metre or two of a corridor edge, which says nothing
against a ±20 m georeference — but **seven sit 6.5 to 12.1 m in, which is the middle of the
road**, and every one of them is a `conjectural` placement from the inferred-structure
programme. The placement gate that put them there tests for overlap with other buildings, for
water, and for modelled ground; it has never tested for the street. Nothing documented is in the
road.

**Nothing was moved in this slice, on purpose.** Repositioning generated structures re-derives
the household ledger, so it belongs to the parcel that owns those files (ROADMAP K1 phase three)
rather than to the slice that discovered the problem. The finding is recorded with the seven
records named, in `docs/RESEARCH/thompson_plat_grid.md` § 7 and ROADMAP K7.

**What the grid is honest about not being**: 19 blocks of the plat's 58, no North Division (its
street control is what § S9 records as owed), no lot depth from any source — the depths are
residuals of the block — and nothing rendered. `blk_south_water_market`, one of the most built-up
blocks in the town, is refused outright because the street layer does not carry South Water west
of E +100. That refusal is the street control owed, arriving from a different direction.

## New 2026-08-13 — twenty-three buildings out of the road, and the point test that could not see them

**K1 phase three (a) / K7 phase two (a).** The grid found seven structures standing 6.5–12.1 m
inside a platted street corridor and left them there on purpose, because moving a generated
building re-derives the household ledger. This slice moves them and shuts the hole they came
through: `tools/plat_corridors.py` holds the corridor geometry for BOTH the report that found the
problem and the placement gate that has to satisfy it, so the two cannot answer differently — the
same argument `generators/mesh_inputs.py` settles for the staleness hash. The gate refuses any
generated footprint that reaches inside a corridor. **23 of the 38 recipe centres moved** (median
12.0 m, worst 21.9 m); in-corridor centres across the scene fell **22 → 10**, and none of the ten
is a generated placement.

**The seven were the loud end of twenty-three, and the point test is why nobody knew.** A centre
is one point and a building is a rectangle up to 11 m across, so a building can front a street
with its centre clear of the corridor and half its depth inside it. That is exactly what the
recipe had built: it read the 80 ft frontage bands as centre-lines to sit ON rather than as edges
to sit BEHIND, and the whole Lake Street shop row stood with its front half in the street and its
centre within a metre of the kerb line. Counting footprints instead of centres finds **56**
structures with some part in a corridor before this slice and **33** after it.

**Three of the moves could not simply step back.** `physicians_office` snapped into the First
Presbyterian Church, `inf_packer_dwelling` into a reserved phase-2 slot, `inf_cooperage_south`
into the South Branch — so each went to the nearest position clearing the corridor, every
committed footprint by 3 m, the two uninstantiated phase-2 recipes and the heightfield's dry
covered ground. The physician's office is 17.7 m from where it was because the nearest free
ground to its Lake Street frontage is a lot back from it. **Nothing was regraded.** These
positions were `conjectural` before and are `conjectural` after; clearing the roadway is not
standing on a recovered lot, and the recipe says so where it used to say the centres were band
assignments alone.

**What is left in the road is mostly not a defect, and one part of it is a measurement.** Four
anonymous roofs from the infill generators inherit this gate when that parcel next runs. The
other 29 are hand-placed records with a frontage argument behind them, and **thirteen are on
South Water Street** — where, walking north from the committed centreline, the traced 1834
waterline is **10.75 m away at E +180 against a 12.19 m half-corridor**. The platted 80 ft street
there runs 1.4 m into the river, and the spare is under 3 m at four more of eleven stations. On
that reach a building on the north side of South Water cannot be both outside the legal corridor
and on dry land — so the disagreement is between the plat module and the drawn bank, and it wants
a reading of the travelled way rather than thirteen nudged records.

## New 2026-08-13 — the last four out of the road, and the row that was aimed at the streets

**K7 phase two (b).** The four anonymous roofs the previous slice deliberately left in a platted
corridor are out of it, and both infill generators now ask the corridor question through the same
`tools/plat_corridors.py` the household generator and the grid report read. **No generated
placement anywhere in this dataset stands in a platted street corridor.** Footprints with some
part inside one: **33 → 29**; the 29 are hand-placed records with a frontage argument and are not
this slice's to move. Verified the gate bites by putting one record back where it was: it fails
with the record named and the depth measured.

**The four were one row's spacing.** The parcel's eight ancillary buildings had local E values of
314, 438, 560, 687, 810 and 315, 559, 809 — a **123 m pitch, which is the block pitch** — so one
yard building stood at the eastern edge of every block, a building's width from the next street,
eight times over. The generator that wrote them tested nothing: not overlap, not water, not
ground, not the street.

**Half of them passed, and why they passed is the part worth keeping.** The four that intruded
(−1.03 to −4.32 m inside the roadway) are the four largest ancillary footprints in the parcel; the
four that cleared it are three privies and a small shed, clear by **1.4–2.1 m against this
dataset's own ±20 m georeference**. They were not placed clear of the street, they were too small
to reach it — so a fix aimed only at the four failures would have corrected four numbers and left
the rule that produced them. All eight moved instead, by one argument: each now stands directly
behind the easternmost principal roof of its own block, 24 m back for the rear yards and 21 m for
the service yards, because a rear yard belongs to a lot and a lot belongs to a house. 17–32 m of
movement.

**Nothing was regraded and nothing was adopted.** These positions were `conjectural` before and
are `conjectural` after; clearing the roadway is not standing on a recovered lot, and standing
behind an anonymous roof is not evidence of serving it. The household ledger keys on structure id
rather than on position, so the 83 adopted roofs kept their households across the move — which is
what made the coupling the previous slice cited a re-derivation rather than a re-argument. The
North parcel carries the same gate and it binds nothing today: the grid covers no North Division
block, because that street control is what § S9 still records as owed. Detail:
`docs/RESEARCH/thompson_plat_grid.md` § 7b.

## New 2026-08-13 — one way to go somewhere, graded; and the half of the gate that was not running

**K9.** Viewpoints and the place search were two lists of the same ground inside Settings.
They are now one `Go to` tab, second in the strip after Controls, opened by <kbd>G</kbd>: 8
authored viewpoints, 4 verified junctions, 222 structures, built from the scene, the index and
the registry rather than from a menu somebody maintains. `#btn-help` is a hamburger.

**The parcel asked for documented entries only, and that turned out to be the wrong list.**
No structure position in this dataset is graded `documented` — **54 are `inferred` and 168
`conjectural`** — so documented-only would have shipped four junctions. Every structure result
instead carries its own `placement.position_confidence`, in the same three words and three
colours the building card uses, and the tab's summary line counts the grades from the list it
paints. What survives about a building is usually a street and a side of it, so a well-documented
tavern with a conjectural position is the normal case here rather than a failure — and the menu
now says which is which at the moment the visitor chooses where to go. The gate compares every
chip against the record it jumps to; a menu that graded a position more kindly than the record
does would be this project's worst kind of bug.

**Two defects the new assertions caught in their own slice.** The five-tab strip fitted 360 px
only by flex-shrinking labels out past their own buttons — one tidy row, measured, and a mess to
look at; the desktop panel is 380 px now, tab padding is 6 px and mobile type 11.5 px, leaving
about 20 px of slack at both viewports, and the gate measures rows, overflow and squeeze at both.
A sixth tab does not fit and will fail there. The confidence chips also rendered identically
grey, because a plain `.jump-result small` rule outranks `.conf-inferred` on specificity; the
gate now requires the grades to differ by colour as well as by word.

**The desktop half of `tools/smoke_renderer.mjs` had not been running, and it is not clear for
how long.** It aborted every run at the first click on the menu button — on `main` as well as on
this branch, reproducibly — and every desktop assertion after that point, roughly a third of the
suite, simply never executed while the run reported a failure that read like a broken control.
Nothing was covering the button: `elementFromPoint` returned the button itself at its own centre,
with no pointer lock, the page visible and focused. The cause is the scene's own weight. At
533 000 triangles on a software renderer one animation frame takes **0.46–1.10 s (measured)**,
and Playwright's click waits for the element to hold still across frames before it will hit-test
it, so 30 s of default action budget was being spent on frames rather than on the page. The
budget is now 90 s — room for a slow machine, not permission for a broken control, since a click
that never lands still fails. **This is a standing hazard, not a fixed one**: the same starvation
will return as the town grows (ROADMAP K14 already records 6 % of triangle headroom), and the
next symptom will again look like a UI bug rather than a budget. A full two-viewport pass now
takes upwards of ten minutes here; `SMOKE_VIEWPORT=mobile|desktop` runs one half while
iterating and prints that it is not the gate.

## New 2026-08-13 — a number that was written, validated, shipped and never read

**K3, coverage.** Every flora zone record authors `cover.matrix_fraction` — how much of the
ground that community's matrix covers — with a `bare_soil_fraction` beside it. `tools/validate.py`
has gated both since the records were written, and `index.json` denormalises the bare-soil figure
specifically so the ground shader can fetch it once. **`renderers/web/js/flora.js` had never asked
for either.** All ten communities were planted at the single lattice density L32 tuned on closed
wet prairie, so a settled town whose own record says **45 % of its ground is bare** was drawn with
the ground closed, and so were the shaded riverbank understory (0.45), the forest floor (0.35) and
the lakeshore sand (0.35).

The fraction is now the probability that a matrix lattice slot carries a plant — near tufts and
mid cards alike, because thinning one and not the other would put a seam exactly at the crossover
where the change of representation is meant to be invisible. It is the same rule the forb layer
has always applied to its own recorded densities, on the field the matrix layer ignored.

- **Wet prairie is untouched**, because it records 1.00 and 1.00 is the anchor. Nothing the
  three-critic prairie sweep tuned has moved, and the change can only ever *remove* instances.
  Measured at 1280×800 against `main` at three fixed stations: wet prairie **360 979 tris against
  360 863** (+0.03 %, which is the reshuffled random draw, not new geometry), settled town
  **429 281 against 441 683** (−2.8 %, 3 278 flora instances against 3 842), marsh edge
  **299 161 against 308 235** (−2.9 %). The scene gets lighter exactly where a record says the
  ground is bare.
- **Measured, across the eight communities that have a clean sampling station**: planted density
  now spans **2.21–6.90 tufts per m²** where it was one figure everywhere, and the implied
  full-cover density agrees at **6.31–8.15** against a lattice carrying 7.30.
- **The gate asks both halves**, because answering only the first is how this went unnoticed:
  that each community's authored number reaches the renderer (re-fetched from the records, not
  compared against a copy of the renderer), and that the sward on the ground follows it. The
  second assertion fails in the other direction too — if every community went back to one
  density, the per-m² spread would collapse toward 1 and the implied figures would fan out
  across the 0.35–1.00 the records give.
- **One anti-vacuity guard moved and the tolerance did not.** *"detailed flora roots share the
  terrain and water surfaces"* requires a minimum sample so that planting nothing cannot report a
  perfect worst error; its station stands in the settled town, and the mobile cone there now holds
  67 rooted plants against about 150 before. The guard is 50; the 1e-5 m root tolerance is
  untouched. That number is a property of the dataset now rather than of the renderer.

**Two findings measured on the way, and not fixed then. Both fixed 2026-08-13 — see below.** S6a
item 9 reads the `river_bank` shot against zone 1's cordgrass — but ground within eight metres of
water is the MARSH zone by extent, and the shot's sward is entirely `z04`/`z10` with no `z01` in
it at all. And the "~25 cm sprigs" are better explained by species than by density:
`nuphar_advena` and `nymphaea_odorata` are floating-leaved aquatics recorded at 0.01–0.10 m whose
own `appearance` text says they float in open water, and they were **6.5 % of the tufts standing
on that dry bank**, because `role: emergent` was all the renderer could see. Fixing that is a data
field in the published vocabulary before it is a line in the renderer — a renderer that decided
which plants float by reading their heights would be guessing at exactly the point this project
refuses to.

## New 2026-08-13 — the pads were standing on soil, and prose was the only thing that said so

**K3, the second finding.** A water lily and a cattail were the same record to the placer: both
`role: emergent`, and the role is what `station()` read. So the marsh community was planted
identically on both sides of its own waterline, and `nuphar_advena` and `nymphaea_odorata` —
0.01–0.10 m, `form: mat_prostrate`, `appearance` "floating pads in open water" — stood as ankle-
high mats rooted in the soil of the dry bank. **The evidence was in the record and unreadable by
anything but a person.**

`data/flora/index.json` now publishes a `substrates` vocabulary and every `role: emergent` record
states one:

| value | habit | may be planted |
|---|---|---|
| `soil` | rooted ground above the water; the default when the field is absent | dry ground only |
| `saturated_soil` | the emergent habit — wet ground OR standing water, foliage above the surface | both sides |
| `open_water` | rooted below the surface, leaves floating ON it | over water only |

- **The validator refuses the unplantable record**, not just the unknown word: an `open_water`
  species in a zone whose extent never reaches water — or a buffer that starts at the bank rather
  than at the waterline — is an error, because a record that can never be drawn is a claim the
  walkthrough does not make. Six new self-tests in `tools/test_validate.py`.
- **The community is split, not the slot dropped.** `flora.js` picks from the subset legal on the
  side of the waterline it is planting, with the weights renormalised over that subset. Refusing
  the slot after the pick would have been one line shorter and would have thinned the dry marsh
  edge by the lilies' 6.5 % share; `matrix_fraction` 0.75 does not stop meaning 0.75 because two
  of that community's species float.
- **Measured, at 1280×800.** An 8 m sweep of the modelled box: **299 dry marsh-edge stations**
  (289 plantable at all) and **286 over water**. Both lilies were legal at all 289 dry stations
  and are now legal at none; the cattail is unchanged at 289 dry / 273 wet. At the marsh-edge
  station nearest the forks the sward holds its density — **2 483 → 2 481 rooted instances,
  47 551 → 47 435 triangles** — and the two `head_ray` heads that stood on that dry bank, which
  are the lily blooms, are gone. A wet-prairie control station is identical.
- **The gate asks the placer, not a copy of its rules.** `flora.stationOf(e, n, speciesId)` runs
  the same `station()` the scatter runs; the smoke sweeps the box with it at both viewports and
  asserts no floating-leaved aquatic has a dry station, that the lilies still have wet ones, and
  that the cattail still stands on both sides — that last one because a placer that had refused
  *everything* on that bank would otherwise read as a pass.
- **What this does not claim.** That the lilies are at the forks at all is still `inferred` from a
  regional flora (`swink_wilhelm_1994`), at a token density, and where the pads sit within the
  eight-metre marsh edge is the scatter's, not a source's. The change moves a species from ground
  it cannot occupy to ground it can; it is not new evidence that it was there.

## Known weaknesses, stated plainly

0a. **The gate that exists to catch a building standing on nothing reported a perfect
    landing for a fort 832 m past the edge of the world.** Fourteen structures went in on 2026-08-11 at
    local E +1130…+1180; the `e1834_harbor_cut` heightfield stops at E +320. That much is L40's
    problem at four times the distance and it is honestly declared on every record. **The part
    that is a defect in the machinery rather than in the data**: `tools/heightfield.py` clamps
    outside the box, so the ground-contact check sampled the clamped edge for the structure's
    base AND for every point of its outline, got the same number twice, and concluded that the
    fort meets the ground. Every structure L40 covers was caught only because the clamped edge
    varies along a wall and produced a gap; the fort was far enough out and square enough on to
    produce none. The gate could see buildings that were nearly right and was blind to one that
    was completely wrong. `Heightfield.covers()` now asks whether there is any ground there at
    all before asking how high it is, the schema carries an `outside_modelled_ground` state
    beside `approach_not_modelled`, and the declaration is checked against the measurement in
    both directions. Turning it on immediately flagged two structures in other parcels that
    nothing had caught. **S2e parcel (b) then landed the same day** and the field now reaches E +1700, so twelve of
    the fourteen fort structures land and their declarations are gone. Two do not, for a
    different and better reason: the fort sits on a plateau that falls to the river between
    N +245 and N +270, and the stockade's north wall and the commandant's quarters cross the
    top of that fall by 1.40 m and 0.46 m. **No cut, fill, revetment or foundation is modelled
    anywhere in this project**, and the real work plainly had one. L46 was rewritten the same
    day to say so. The blindness the fort exposed is fixed regardless of whether anything
    currently needs the new state.

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

0. **The former slow-renderer walking failure is resolved without weakening its distance bar.**
   Movement now consumes up to a quarter-second of real frame time in terrain-and-collision
   substeps no larger than 0.05 s. A software renderer drawing only two frames per second no
   longer turns a 1.45 m/s walk into a crawl, while the short substeps retain bank and building
   collision accuracy. The foreground smoke run passes the same walk-distance assertion at
   both 390×780 and 1280×800. Current full-scene budgets are 49 / 53 draw calls and 378,647 /
   499,343 triangles respectively; the desktop renderer remains slow at 2 fps under SwiftShader,
   but elapsed-time walking is no longer coupled to that frame count.


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

**S9 — streets, roads and paths**, **FIRST VISIBLE SLICE DONE 2026-08-11.** Seventeen dated
earth travelways are compiled from `data/streets/1835.json`, draped rather than flattened, and
identified live with their 1835 and 2026 names. The earlier sentence here saying "nothing was
graded until 1855-58" confused the later Raising of Chicago with early street work and was
wrong: South Water was ordered pitched by April 1834 and graded for drainage that July; South
Water and Lake were the two early principal improved routes. What remains is the north-side
control/extent research, any separately attested plank footwalks, and evidence that could replace
the conjectural travelled widths and rut patterns recorded in L79. See ROADMAP § S9.

**S5a — Fort Dearborn** — **DONE 2026-08-11**, both gates cleared before any geometry.
**The footprint has a source.** F. Harrison Jr.'s survey of the mouth of the Chicago River for
the harbour works, 24 February 1830, approved by William Howard, U.S. Civil Engineer, reproduced
in Andreas vol. 1 p. 113 and listed in that volume's own table of maps as "Fort Dearborn in
1830-32". It draws the fort IN PLAN — square enclosure, works at three angles, four ranges, two
gates, two buildings flanking the south gate — and its arrangement is corroborated building by
building by Gurdon Hubbard's 1827 walk round the inside (Andreas p. 264). Recorded as
`harrison_1830_river_mouth`. **The plate has no scale bar**, so the scale is derived from the one
stated dimension in the whole complex — the commandant's quarters at "about 25 x 50 ft" in the
1855 photograph key — giving 1.10 ft/px and a stockade about 53 m (174 ft) square at **±20 %**.
Two checks on the same plate agree to 5 % and 11 %. **The garrison is settled**: held
continuously from June 1832 to 29 December 1836, Maj. John Greene 5th Infantry most likely
commanding on the scene date, strength after 1833 unattested. Fourteen records, two new
archetypes (`palisade`, `fort_structure`), fourteen bakes, ~17,000 triangles. Five exclusions
went in with it, four of them wrong-fort findings. See `docs/RESEARCH/fort_dearborn.md`.
**What it did NOT settle and what is now the binding constraint: there is no ground under it.**

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
