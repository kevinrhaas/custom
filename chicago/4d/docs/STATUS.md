# STATUS

Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-11 (the half of the street reading that was measured and thrown away
a fortnight ago is committed, because a candidate is now asked what it does along its own
length rather than a fourth thing about its width: Lake and Randolph are measured, ten strips
of Wright lots are not, and the control point's untested coordinate turns out to be right to
3.4 m, § 52) ·
**Phase:** S0, S1 (datum), S2-partial (terrain + river at the
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
this building by twenty months. **And the card now answers the question the whole scene rests
on** — *was this building here on 1 July 1835* — which it never had, because the renderer read a
sidecar field the compiler had never written (§ 28). **That fault has a gate now rather than a
discoverer, and switching it on found the second one the same day** (§ 29): the card had also
been asking the sidecar whether the shape in front of you is a placeholder massing — a question
the compiler has never answered and, reading only `data/`, cannot. **And the gate's other
direction — what is compiled and never read — is now empty of unshipped claims** (§ 30): every
record's `research_note`, written for a reader and displayed nowhere for the life of the project,
is on the card verbatim. **And the next building's blocking question is answered without a single
vertex being moved** (§ 31): on 1 July 1835 Fort Dearborn was an occupied Army post under a named
commander, which is a different scene from the empty stockade the popular accounts imply — while
its footprint stays honestly unsourced, with the search narrowed from "find a plan" to one named
1839 plat. **And the surface every one of those buildings stands on can finally answer the same
questions they can** (§ 32): the terrain graded itself as carefully as any record, dithered under
the confidence view like any building, and had never once told a visitor what it was grading.
**And what the ground makes up is demanded by a check now rather than owed to somebody's
attention** (§ 33): the liberties coverage gate reads the terrain spec, and the first thing it
found was an invented depth on a watercourse no entry in the document had ever mentioned.
**And the last rule the ground could not be held to is enforced, because the thing holding it
back was a gate and not the research** (§ 34): writing a sentence of reasoning into the terrain
spec used to re-stale the ground and demand a Blender bake, so three claims said *no reasoning
is recorded* on the panel for a fortnight; the hash strips prose now, the three notes are
written, and an unreasoned ground claim stops the commit exactly as it does on a building.
**And the other half of the ground's honesty — what it states and does not build — is a gate
now, which it never was** (§ 35): five surface materials, two of them `documented`, describe a
soil no surface in this model is made of, and the panel showed them under the project's
strongest chip with nothing saying so.
**And the one declaration in that vocabulary that promises an agreement rather than admitting an
absence is a check now instead of a sentence** (§ 36): four figures said *the mesh contains
exactly this and does not read it from here*, three more restated a build instruction while
declaring a state that asks nothing, and the only thing holding any pair together was the hand
that wrote them.
**And the category between a building and an exclusion — researched, and still open — is data
now rather than four sentences, with its own promise enforced and its own section in the
walkthrough** (§ 37): the watch list said it existed so that nobody would promote these to
`documented` without new evidence, one of the four is a committed record, and nothing had ever
checked that sentence.
**And the largest claim a visitor stands in front of — the outline of the building — says how much
of itself is evidence** (§ 40): six of the eight footprints here open with the word PLACEHOLDER,
the compiler carried their confidence and dropped their reasoning, and the tint had been narrowed
to stop showing dimensional uncertainty on the stated understanding that the card would show it
instead. It never did. Second claim found graded-and-silent by somebody reading a file, so it is a
chip count now: run against the previous commit it reports all eight buildings one chip short.
**And the one building in this scene whose date is a live argument says so where a visitor meets it,
after a fortnight of the panel promising it on the card's behalf** (§ 41): the Western Hotel's card
showed the dated claim graded `inferred`, and the Evidence panel's entry for it ended with the words
*and the provenance card shows it* — true of the claim and false of the doubt, so the dispute
between the builder's own statement and the hotel chronology reached whoever opened a panel about
the town and not whoever walked up to the house. Nothing was broken, again, and the promise about
the other surface is a gate now instead of a sentence.

---

## What exists and works

| thing | state |
|---|---|
| Repository scaffold | **done** — full tree per `docs/PLAN.md` |
| Schemas (structure, source, scene) | **done** — phases, tiers, rights gating, scene-owned dates |
| `tools/validate.py` | **done** — schema, referential, confidence contract, per-scene date gates, phase-overlap, epoch coverage, release blocking, license + rights gating, staleness, publish budget |
| `tools/test_validate.py` | **done** — 205 checks, all green, including a proof that rewriting every note, caveat and citation in the terrain spec leaves the ground's staleness hash where it was while moving the bank face by a metre does not, and that no generator reads a key that hash strips, and a proof that a liberty admitting to an invention in one epoch's ground does not discharge the same invention in another's, that a ground admission and a building's are separate obligations neither of which covers the other, and that an 1836 building is excluded from the 1835 scene, that a liberty naming a building does not cover an invention it never mentions, that an attribute the archetype never reads cannot pass without saying what the mesh does instead, and that rewriting a record's prose does not report its mesh as stale while changing a value the generator reads does, and that an attribute an archetype declares it consumes actually moves the parameters when its value changes, and that an exclusion carries a reason and a citation that resolves and stops being an exclusion at its own earliest scene, and that a field the provenance card reads off a sidecar is actually in the sidecar, and that every field any renderer module reads off a sidecar is one the compiler writes, and that a ground figure declaring the mesh agrees with it is held to the half it restates — the heightfield the bake wrote, the build instruction it duplicates, or the generator line it describes — with a phrase that exists only inside a comment satisfying nothing, and that a watch-list entry naming a committed record fails the moment that record's claim is promoted to `documented` |
| `tools/check.sh` | **done** — full gate runs in **0.4 s**, no Blender |
| Research dossiers | **done** — 8 reports, ~360 KB, committed verbatim in `docs/research/` |
| Source records | **28**, of which **15** carry a Wayback snapshot — the three added with the bridge all do, and so do the post-office page and the Fort Dearborn page. **Four now derive their rung from the document they transcribe** rather than asserting it (§ 44): three chicagology pages read in full on 2026-08-10 and regraded 4 → 2 on the 1883 *Inter Ocean* interviews and the 1857 *Chicago Magazine* they carry, plus the Kinzie bridge page's long-standing Andreas sentence made checkable. **Six do now, after the three § 44 flagged were opened on 2026-08-11** (§ 45): `prefire062` reprints Andreas rather than the newspaper it named (4 → 3), `prefire276` reprints the 1857 *Chicago Magazine* (4 → 2), and `wikipedia_chicago_river` reprints nothing at all — the first record to declare `carries_no_document`. Six pages at tier 4 or weaker still date their own retrieval and declare nothing; the validator counts all three states every run |
| Structure records | **8** — six buildings at the forks, the North Branch bridge, and Hogan's store on Lake Street |
| Terrain epochs | registry written; `e1834_harbor_cut` active, geometry layers **not yet built** |
| **Datum** | **VERIFIED** — Wright-derived, Hathaway- and OSM-checked, RMS 17.5 m, re-derivable from traces |
| **Generator pipeline** | **WORKS** — pinned Blender 4.5.3, `frame_tavern`, 496-tri Sauganash from the record alone |
| **Renderer** | **WALKABLE** — three.js r0.185.1 vendored, pointer-lock + touch, confidence view, provenance popup |
| **Smoke** | 233 checks green at 390×780 and 1280×800, zero page errors |
| **The ground's claims, in the app** | **done** (2026-08-10) — the Evidence panel's *The ground you are standing on*: 20 graded claims off `terrain_spec.json` with their figures, reasoning and citations, derived per scene by `compile_scene.py` and re-derived by `check.sh`; `check_terrain_claims` holds the same claims to the record's citation rule (§ 32) and, since § 34, to its reasoning rule — every `inferred` ground claim states why, and none of them is a warning any more |
| **What a source is, in the app** | **done** (2026-08-11, § 48) — every citation carries the document it reprints (`transcribes`) or the finding that it reprints none, and the source's own `what_it_supplies` / `what_it_does_not_supply` behind a `<details>`. `check_source_surface` partitions all 22 properties of `data/source.schema.json` into visitor-facing and internal and fails on a property in neither, on a visitor field no compiled citation carries, and on one `citations.js` never reads. Withheld in exactly one place — the not-here list, where a source's account of what it carries names a standing building — and the smoke pins that too |
| **Liberties, in the app** | **done** — the Evidence panel lists all 34, derived from `docs/LIBERTIES.md` by `tools/compile_liberties.py` and re-derived by `check.sh`; the provenance popup shows the ones taken with the building you are inspecting; and the gate checks the document *for gaps* in both directions — refusing any conjectural value (footprint, position, or a stated form attribute) that no liberty admits to, and equally any attested value the archetype never reads and no liberty owns up to leaving out. **The ground is inside the same rule since 2026-08-10** (§ 33) via a `terrain.<epoch>.<claim>` namespace, matched against the claims the Evidence panel renders |
| **The platted street module** | **MEASURED on both sheets** — 11 corridors in `data/traces/vectors/street_corridors_1834.json`, median 83.7 ft, 66 ft excluded; 8 N-S streets (§ 42) and, since § 52, three E-W ones on Wright, of which Lake (79.4 ft) and Randolph (81.5 ft) are named by their committed modern junctions to 0.9 m. `check_street_module` re-derives every metre and every name offline on every commit. Evidence only: no street geometry is generated yet (S9) |
| **The lake shore** | **TRACED, NOT BUILT** — `shoreline.geojson`: the harbour reach, the 1834 cut, the old southward channel, the sand bar as an island and the mainland shore, E +314…+1570 off Wright 1834. Vectors only; no elevation, no mesh, nothing east of the box renders yet |
| **Published** | `site/chicago/4d/` (4.08 MB of a 25 MB budget) + a tile on the Chicago landing page |
| **What the ground does NOT build** | **done** (2026-08-10) — `terrain_inputs.CONSUMED` declares the spec figures `terrain_gen.build_field` reads; `check_ground_geometry` holds every other figure the Evidence panel shows to a `mesh:` declaration (`absent` / `simplified` / `record_only` / `restated_in_code`), both directions, and the first two owe `docs/LIBERTIES.md` a `Covers:` token. 36 figures declared, 5 owed an admission (§ 35). **The fourth state is checked as well as declared since § 36**: `terrain_inputs.RESTATES` names the half each restatement agrees with — the heightfield the bake wrote, another figure in the block, or a named line of the generator — and 7 figures are held to it |
| Exclusions | 14 date-guarded structures — **in the walkthrough** since 2026-08-10 (Evidence panel, "What is not here"), citations joined, and now held to the same citation rule as a structure record (§ 26) |
| Watch list | **4 open questions**, structured data since 2026-08-10 (§ 37) — the category between a building and an exclusion. Each carries what is open, what settling it would change, a dossier pointer that has to resolve, and either citations that resolve or a sentence saying why there are none. `check_watch_list` enforces the file's own promise: the one entry that IS a committed record names the claim carrying the doubt, that claim may not be `documented`, and — since § 41 — it must be a claim the provenance card actually renders, read off `popup.js` itself. In the walkthrough under "What is still an open question", with the standing one chipped as standing, **and on that building's own card since § 41** |

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
  dossier, which is why no land elevation in this build is tagged `documented`. **Established
  from the page rather than inferred from a quotation, 2026-08-11** (§ 51): the article cites
  nothing for anything — no footnote, no endnote, no reference anywhere in it.
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

28. **The claim the whole scene rests on had never rendered, and no gate could have seen it.**
    `popup.js` has read `sidecar.documented_range` since the card was written, and
    `compile_scene.py` has never emitted the field. So the one line that answers *was this
    building here on 1 July 1835* evaluated to an empty string on every building, on every
    load, for the life of the project — while `roof_pitch_deg` carried a chip, its sources and
    its reasoning. **Nothing in this repository could have caught it.** The compiler was
    consistent with itself and `--check` (§ 27) only proves that; the record was complete and
    validated clean; the renderer's markup was correct. Two halves each perfectly right about
    their own side of an interface neither of them states.
    **What ships is the phase's claim about itself**, in the attribute shape so the card
    renders it with the attribute renderer rather than a second one that would drift:
    `documented_range` (span, confidence, sources, note), the phase's `change_note`, and
    `position_note` / `position_sources` beside the position chip that was already there. The
    dates print as recorded — `1835-12-31`, not "December 1835" — because seven of the eight
    ranges end on 31 December of some year, which is a BOUND and not a day anybody recorded (the
    exception is the Sauganash, which burned on 4 March 1851). Prettifying a bound would dress
    it up as a date somebody wrote down.
    **The spread across the eight is the argument for showing it.** The Sauganash's frame phase
    is `documented` (Wau-Bun watched it built, it burned on a recorded date); Hogan's store is
    `inferred` and its note is the least comfortable paragraph on any card here — attested to
    about July 1834, placed eleven months later on continuity, on the corner most exposed to the
    1835 boom (§ 25). A card that stamped one grade on all eight would have looked like a
    feature, so **the smoke asserts that discriminating pair** rather than the presence of a
    chip, and asserts against the rendered card rather than the sidecar, because reading the
    sidecar is exactly the check that would have passed all along.
    **One gate came with it.** Every other `documented` value in this dataset owes a resolving
    source; `documented_range` was outside that rule for no reason but the order the checks were
    written in. It is inside it now — which matters more today than yesterday, because the claim
    is something a visitor reads rather than something only a reviewer could find.
    **What is still not on the card is the footprint's reasoning.** Its confidence drives the
    tint and its note stays in the record, because the footprint has no display value that is
    not itself a derivation — a bounding box over Miller's L-plan would be a new invention on
    the panel that exists to admit them. It is a gap, and it is stated rather than filled.

29. **The interface neither half stated, and the second field that fell through it.** § 28 ends
    with a sentence rather than a mechanism — *any other sidecar field the renderer reads is in
    the same category* — and one of them was already broken while that sentence was being
    written. `popup.js` asks the sidecar `asset_is_placeholder`; `compile_scene.py` has never
    written it and **could not**, because it compiles from `data/` and never opens a mesh. So the
    flag that tells a visitor *this shape is a stand-in, not a bake from the record* has never
    once rendered, on any building, for the life of the project. Second instance of § 28's
    failure class, found the same day, by a check rather than by somebody reading the file.
    **The gate derives the interface from both halves instead of asking either to declare it.**
    What the compiler writes is read off the committed sidecars — `compile_scene.py --check`
    already proves those are exactly what the dataset compiles to, so the artifact the renderer
    actually fetches is the definition of what is emitted, and no second list can drift from it.
    What the renderer reads is scanned out of the renderer: `check_sidecar_contract` follows
    `record.sidecar` and the names bound to it (`const s = record.sidecar`, `const p =
    s.placement ?? {}`) and resolves each dotted path against the sidecar shape. 27 reads across
    six modules; one of them resolved to nothing.
    **The fix moves the fact rather than inventing a field.** Whether a mesh is a placeholder is
    a statement the GLB makes about itself, in `asset.extras.placeholder` — which `scene-loader`
    has read at load time all along, to raise it as a problem. It now also puts it on the
    registry entry, and the card reads `record.assetIsPlaceholder`. Making the compiler emit it
    would have meant teaching a pure-data compiler to open binaries so that a record could
    restate something the mesh already says.
    **The flag is wired and still unexercised, which is stated rather than glossed.** All ten
    committed assets are real bakes, so `false` is the only value this dataset produces and no
    visitor will see the banner until a placeholder ships. The smoke therefore asserts the
    distinction the old field could not make — the value is `false` and not `undefined`, "we
    checked, it is a bake" rather than "nobody answered" — and that a real bake shows no banner.
    A test for truthiness would have passed against the broken field all along.
    **Where the scan stops is worth stating, because it is most of the interface.** It sees a
    read that names a field *while the sidecar is in hand*. A value passed to a function is read
    through that function's parameter, so `claimRow(label, span, range)` puts `range.confidence`
    out of reach — the fields under `documented_range` are checked as a block and not one by one.
    That is the direction the fault came from twice, though: the field name is chosen where the
    sidecar is in hand. It also errs loudly rather than quietly — reuse a bound name for an
    unrelated object and it will report that object's fields as missing — which is the right way
    round for a gate whose whole purpose is to end a silence.
    **The first thing it reported was a false positive, and the false positive was itself.** The
    comment written to explain why the card no longer reads `asset_is_placeholder` names the
    field, and a regex does not know prose from code. Comments are stripped now, block comments
    collapsing to their own newlines so a reported line number still points at the right line.
    **The reverse direction is reported and not enforced**, because the same interprocedural
    limit would make it lie: four top-level fields are compiled and never read — `archetype`,
    `scene`, `target_date`, and **`research_note`**. The last one is a finding rather than dead
    weight. Every record carries a research note written for a reader, it is compiled into every
    sidecar, and no surface in the walkthrough shows it. That is an unshipped claim, it is not
    fixed here, and it is not queued: it belongs to whoever next works on the card.

30. **The last compiled field that reached nobody is on the card, and it was never broken.**
    § 29 ends with a finding it declined to fix: `research_note` is on every structure record,
    compiled into every sidecar, and shown by no surface in the walkthrough. It is not the
    failure class of § 28 and § 29 — nothing asked for a field nobody wrote, every gate was
    right, and the two halves agreed. **The field simply had no surface**, which is the quieter
    way for a claim to go unshipped and the harder one to notice, because there is no fault to
    find. The card carries it now, under *the record's own account*, below the liberties and
    above the citations.
    **It is shown verbatim, and the smoke asserts that with an exact string comparison** against
    the sidecar rather than a substring match. These notes are the record talking about the limit
    of its own evidence — Walker's opens by stating what it actually asserts and closes by saying
    the likeliest reading of the sources is that this record models the wrong building; the Green
    Tree's names an 1859 photograph nobody has opened as the highest-value lead in the parcel.
    A renderer that showed a first sentence and an ellipsis would pass every looser assertion
    that could have been written here, and it would be editing a source. The discriminating case
    is asserted too: a second building gets its own account, so a section rendering one fixed
    block of prose — or the previous pick's — fails.
    **Collapsed, for the reason the liberties are.** Several hundred words open by default pushes
    the citations off a 62vh panel on a phone.
    **What this leaves.** The empty state — a record with no note — is unexercised by real data:
    all eight carry one. It renders nothing at all rather than a sentence explaining the absence,
    which is deliberate (there is no finding in a note that was never written) and therefore
    untested. And the sidecar-contract note now reports three unread top-level fields rather than
    four; `archetype`, `scene` and `target_date` are machinery the card has no reason to show, so
    that list is finally empty of unshipped claims.

31. **The next building's two blocking questions, one answered and one narrowed — and no geometry
    in this slice, deliberately.** ROADMAP § S5a has said since the coastline gate cleared that
    Fort Dearborn could not be drawn until two things were settled: what the fort actually *was* on
    1835-07-01, and where an outline could come from. This slice is the research half and it lands
    nothing a visitor can see, which is the honest shape for it — the fort site is at local E +1152
    and the modelled ground stops at E +320, so there is no terrain to stand it on, and a record
    without its bake is a 404 the smoke correctly fails on.
    **What it was: an occupied Army post under Major John Greene.** Greene took command on
    18 December 1833 and held it until 16 September 1835. Three separately written accounts have the
    fort garrisoned through 1835 — Andreas' officer roll, Wentworth's fuller one, and an 1857
    magazine account written while the buildings were being pulled down — and the post surgeon's
    prescription book carries an entry for a named sergeant dated 15 March 1835, which is a piece of
    paper rather than a recollection. The assumption worth naming as dead: this is not a ruin, not a
    caretaker's compound, and not the "abandoned by 1836" of the encyclopaedia entries.
    **Andreas contradicts himself three ways about the end and the contradiction dissolves.** p. 84
    prints the order withdrawing the troops on 29 December 1836; p. 162 says "in 1836"; the military
    chapter says "final evacuation, May 10, 1837" and flattens the 1831-32 gap its own p. 84 states
    in detail. Wentworth p. 35 reconciles them: the *soldiers* went on 29 December 1836 and the
    *post* was held by Brevet-Major Plympton until June or July 1837. A writer describing a garrison
    and a writer describing a post give different dates for the same event, honestly.
    **The footprint is still unsourced and that is stated rather than filled.** No dimension of the
    1816 stockade survives in anything read. What changed is that the search stopped being "look for
    a plan somewhere": the War Department's agent, reporting in 1840, names the platted lots of the
    Fort-Dearborn Addition withheld from sale because they covered "the fortress of Fort Dearborn
    *within the pickets*" — a surveyed envelope, three years after the troops left, on a plat whose
    streets survive in the modern grid. Two weaker candidates and four ruled-out ones are in the
    memo, so the next agent does not re-run them.
    **Three enclosures get confused in this literature and only one is the fort.** The 1816 stockade;
    the post-army compound of 1850, whose "say 400 feet" is quoted in the same sentence as "the
    pickets having been removed at an earlier date"; and the 53¼-acre reservation, which is what
    Wright labels. Anyone reaching for the 400 ft as a palisade length would have been wrong by a
    whole category, and it is the most citable number in the literature.
    **The best single document is a complaint about a picture.** Gurdon S. Hubbard, writing to
    Wentworth in 1881 to say that *Wau-Bun*'s cut of the fort is wrong, gives in passing what no
    view gives: the enclosure ran "nearly north and south, east and west"; the north picket line
    stood nowhere more than 80 ft from the water and 50-60 ft opposite the north gate; the north and
    south gates were on one sight line; and **the ground at the fort was "not over eight feet above
    the River at its lowest stage"**. That last one is a finding about the terrain, not the fort:
    the total land relief across the whole modelled box is 4.30 ft, so an 8 ft platform is taller
    than anything currently in the ground, and it belongs to S2e parcel (b). `kinzie_waubun_1856` is
    a source of this project and its fort illustration is now known to be wrong in four particulars.
    What this does not do is give a single coordinate, a single dimension, or a single record. It
    gives the next slice a source list instead of a search.

32. **The ground makes claims too, and it had never made one to a visitor.** Every gate and every
    panel above is about a building. `terrain_spec.json` grades itself as carefully as any
    structure record — a `documented` water plane, three `inferred` division levels argued out of
    period narrative feet, a `conjectural` 6 m bank face, a channel cross-section whose own note
    says it carries no evidence at all — and none of it reached a surface a visitor could read.
    The terrain even DITHERS under the confidence view, because the ground mesh carries the same
    `_CONFIDENCE` channel a building does. So the walkthrough has been showing that a grade exists
    while saying nothing about what was graded, which is the least useful half of the claim.
    The Evidence panel now carries **The ground you are standing on**: twenty claims, each with
    the spec's own figures under the spec's own key names, its reasoning verbatim, and its
    citations joined — derived by `compile_scene.py` into `sidecars/<scene>/terrain.json` and
    re-derived by `check.sh` like every other sidecar.
    **This is not the failure class of § 28 and § 29 and not the one of § 30 either.** Nothing
    asked for a field nobody wrote, and the field did not merely lack a surface: the whole
    DOCUMENT lacked one. `terrain_spec.json` was read by the generator and by nobody else, which
    is also why nothing checked it.
    **Switching that on found the second file where rule one was never enforced**, exactly as
    § 26 found the first. Every `source_id` in this project must resolve in `data/sources/`;
    `check_terrain_claims` now holds the ground to that, and to the two other rules a record
    answers to — a `documented` claim owes a resolving source, and no land elevation may be
    `documented` at all, which is the spec's own caveat enforced rather than merely written. The
    claims are enumerated by the same function that puts them on the panel, so the checked set
    cannot stop being the displayed set. The committed spec passes; the value is that the next
    zone cannot skip it.
    **One rule is a warning rather than an error, and the reason is a defect one level down.**
    `inferred` owes stated reasoning — an error on a record — and three surface-material claims
    (the north and west divisions' soils, and the channel's) have none. The fix is a sentence in
    `terrain_spec.json`, and that file's BYTES are the terrain's staleness hash, so writing a note
    that cannot move a vertex re-stales the ground and needs a Blender bake. That is precisely the
    false positive § 15 rewrote the BUILDING hash to end, still standing on the terrain side:
    `terrain_inputs_sha` hashes whole files. So the warning stands the way the un-archived-source
    warnings do, and the walkthrough says *no reasoning is recorded for this claim* where a
    reviewer would say the same thing — the gap reaches a visitor rather than waiting for the
    repair. **Closed by § 34**, which paid the defect one level down instead of paying the bake:
    the terrain hash strips prose now, the three notes are written, and the rule is an error.
    **Two liberties were owed and had never been written.** The 6 m bank face (L32) and the
    underwater channel profile (L33) are `conjectural` in the data and were admitted nowhere: the
    coverage gate reads `data/structures/` and cannot see the terrain spec, so nothing demanded
    them. That limit is the honest headline of this slice — the ground's inventions are inside the
    *panel* now and still outside the *gate*. **Closed the same day by § 33**, which found a
    third one that neither L32 nor L33 had noticed.
    **What it still cannot say.** The claims are block-level, so a grade covers a whole zone: the
    north-side slough is `conjectural` as a block while its existence and course are Wright's and
    only its depth is invented, and its note is the only thing that says so. And a claim can be
    perfectly graded, perfectly cited and wrong about the town.

33. **The ground is inside the coverage gate now, and switching it on found the invention nobody
    had noticed.** § 32 ends by naming its own limit: the terrain's inventions had reached the
    *panel* and were still outside the *gate*, because `check_liberties_coverage` reads
    `data/structures/` and can see nothing else. So L32 and L33 existed because somebody noticed
    and wrote them, which is exactly the arrangement this family of checks was built to replace —
    a coverage rule that depends on attention is the filed confession, one level up.
    The `Covers:` vocabulary now has a second namespace, `terrain.<epoch>.<claim>`, matched in
    both directions against the same enumeration the Evidence panel renders from.
    **Six conjectural ground claims, and only five had prose behind them.** The bank face (L32),
    the channel cross-section (L33), the micro-relief (L14) and the two west-prairie swales (L15)
    were all admitted somewhere in the document and none of them was *claimed*; adding the field
    to each was bookkeeping. The sixth was not. **The north-side slough's depth is invented and
    appeared on no list at all** — its existence and course are Wright 1834's, drawn on the sheet
    this whole terrain is fitted to, and its one-foot bed and 1.2 m e-fold are in the model
    because a shallower channel stops reading as water, which is a rendering argument wearing a
    terrain claim's clothes. **L34** is new and says so. That is the second time a check of this
    family has found something on its first run (§ 26 and § 29 were the others), and the argument
    for writing them is the same each time: the entries that were already there prove the author
    was diligent, and the one that was not is what the mechanism is for.
    **Two design decisions are load-bearing and are asserted rather than assumed.** The epoch is
    part of the token because `docs/EPOCHS.md` versions the ground — a later scene brings a second
    shoreline with second inventions, and an admission about this one must not silently discharge
    that one; the self-test asserts that a claim against `e1830_pre_cut` leaves `e1834_harbor_cut`
    failing. And the terrain is **not** squeezed into the structures' grammar as a record named
    `terrain`: the two domains are separate obligations that neither discharges for the other,
    which the self-test also pins, and the claim carries its `domain` rather than leaving a reader
    to infer it from a token's shape. This is the document whose subject is calling things what
    they are; § 20 is what it costs when a name is read as being about the wrong thing.
    **What it still cannot see.** The rule fires on a `conjectural` tag, so the ground's
    *omissions* are outside it exactly as a building's were before the geometry declarations —
    there is no terrain equivalent of `CONSUMED`, and a zone the spec describes and the generator
    ignores would leave no trace. The grades are also block-level: the slough is `conjectural` as
    a whole while only its depth is invented, so L34 admits more than the data does and the note
    is the only place the distinction is legible. And a ground claim can be perfectly graded,
    perfectly cited, perfectly admitted to, and wrong about the town.

34. **The gate that was charging a bake for a sentence, and the three claims that had been
    waiting on it.** § 32 ended with a rule it could not enforce: an `inferred` ground claim
    owes stated reasoning, three surface-material claims had none, and the check had to warn
    rather than fail — not because the research was missing but because the only place to write
    the reasoning is `terrain_spec.json`, whose BYTES were the terrain's staleness hash. A
    sentence that cannot move a vertex re-staled the ground and demanded a Blender bake this
    runner does not have. So the finding reached a visitor as *no reasoning is recorded for this
    claim* and stayed there.
    **The repair is § 15's, arriving on the ground.** `mesh_inputs.py` was written because a hash
    over "the files that were involved" cried stale over rewritten prose, and "a disbelieved gate
    is worse than none" is its own sentence. The terrain was still on exactly that hash.
    `generators/terrain_inputs.py` hashes a *document* instead: the spec, the two traced vector
    files and the datum with their prose removed, plus the bytes of the code that turns a spec
    into vertices. The stripped set — `note`, `*_note`, `_doc`, `label`, `scope`,
    `critical_caveat`, `why`, `sources` — is a DENYLIST, so a zone, a reach or a watercourse
    added to the spec tomorrow is a mesh input the day it appears; an allowlist of the keys the
    generator reads today would quietly stop asking about the newest one, which is the failure
    this family of checks exists to prevent. `name` is deliberately kept: in a GeoJSON it also
    names the CRS, and dropping `crs.properties.name` would take the coordinate reference system
    out of the hash to save a feature title.
    **The denylist is a claim about the generator, so it is checked against the generator.**
    `test_terrain_prose_is_not_read_by_the_generator` scans `terrain_gen.py` and `common/` for a
    subscript or a `.get()` of any stripped key — and asserts that the scan can see a real read
    at all, because a regex that matches nothing passes every test ever written against it.
    **The eight-word version of the other test**: rewrite every note, caveat and citation in the
    spec and in a traced bank line — the hash does not move; move the bank face by a metre, or
    append a swale, and it does.
    **The re-stamp, and the proof, because a re-stamp is a claim.** Under the new recipe the
    ground's input document at the last bake and at this commit differ in exactly one entry:
    the bytes of `terrain_gen.py`, whose only change in this slice is deleting the old
    `inputs_hash` and delegating. Checked by diffing the two documents in a worktree of the
    previous commit, not by inspection. No mesh was regenerated and none needed to be.
    `assets/manifest.json` now carries `terrain_inputs_scheme` beside `inputs_scheme`: the two
    halves were redefined on different days for the same reason, and one number would have made
    the second redefinition look like the first — or worse, re-stamped every building to describe
    a change on the other side of the manifest.
    **What the three notes say, and none of it flatters the dataset.** The north and west
    divisions' soil profile is `chicago_architecture_history_115`'s measurement *of the business
    district*; the dossier's surface-material table groups zones 8, 9, 18 and 19 under it, and
    carrying it across the river is that grouping rather than a second observation — with the
    same report describing the North Division as timbered, better-drained sandy ground and the
    West Division as wet prairie, neither of which is quite what the profile it lends them
    describes. The channel's `cahokia_alluvium_silt` is worse: nobody here has seen the bed, no
    source record in this project describes it, and the name is what modern geological mapping
    puts along this region's rivers generally — a formation carried onto this reach, not an
    observation of it. All three are on the panel, next to the claim.
    **What it costs, and a correction the smoke made to this entry while it was being written.**
    The first version of the assertion said *no claim on the panel shows the disclaimer* and
    failed on the committed data: two surface-material claims are `documented`, cite a source and
    carry no note, so they show it too. That is the right reading rather than a gap — a
    documented claim owes evidence, not an argument — and the assertion is scoped to `inferred`,
    where the obligation is. The case that matters is therefore no longer in the data, which is
    exactly how a disclaimer rots, so the smoke exercises `groundClaimHtml` directly on a claim
    with no notes and on one with them and keeps the discriminating pair.
    **The residual is the one the buildings have.** `terrain_gen.py` is hashed whole, so a
    docstring edit in the generator still re-stales the ground — identical to `build.py` on the
    structure side, one file rather than the file every ground claim has to be written in, and
    written down in `terrain_inputs.py` rather than left to be rediscovered. And, as ever, this
    compares inputs and not output: a hand-edited GLB behind an untouched spec passes.

35. **The ground says what it is made of and nothing is made of it, and the gate that found
    that is the omission rule arriving on the terrain.** § 33 ends by naming its own limit: the
    coverage rule fires on a `conjectural` tag, so the ground's *omissions* were outside it
    exactly as a building's were before the geometry declarations, and there was no terrain
    equivalent of `CONSUMED`. There is one now, and the first thing it reported is the sharpest
    case of a confidence chip answering the wrong question that this dataset has produced.
    **`terrain_spec.json` grades five surface materials and no surface in this model is made of
    any of them.** The South Division's black loam over quicksand over blue clay is
    `documented` — the strongest grade this project awards — and the marsh strip's peat and
    muck is too, and the ground mesh carries one earth colour from one edge of the box to the
    other. `terrain_gen.py` builds elevation and nothing else. A visitor reading that row is
    being told how sure we are of a fact about the site, not what is under their feet, and
    until today the panel could not tell them apart. **L35** admits it; the rows are marked
    *not modelled from this*, in the provenance card's words, from the provenance card's module.
    **The declaration is per figure and the admission is per claim**, which is a mismatch and is
    stated rather than smoothed: `terrain.<epoch>.<claim>` is the vocabulary the document
    already writes in, a soil profile is not separably admittable from the block that states it,
    and the block-level grading § 32 and § 33 both flagged is the same limit one level down. The
    note is where a reader learns which figure is the unbuilt one.
    **Two new categories came out of writing it, and the second is a warning rather than an
    admission.** `record_only` is the structure side's, unchanged — `dossier_zone` is a pointer
    into the research table, `range_ft` is the dossier's span from which the built `near_ft` and
    `far_ft` were picked, `bank_crest_ft` restates the crest the ramp already arrives at.
    `restated_in_code` is new and exists only here: the water surface is `0.0` in the spec and a
    literal zero in the generator, and the bank's ease-out is written out as a formula in the
    spec and separately written in Python. **Those values are true about the mesh and the mesh
    does not read them.** Calling that `absent` would be a lie in the visitor's direction and
    `simplified` one in the reviewer's, and it gets no marker on the panel, because a visitor IS
    looking at the thing it describes. What it owes is a warning to whoever edits the generator,
    and nothing checks that the two halves still agree — same for `bank_crest_ft` against
    `near_ft`, which carry the same number today by hand.
    **Where the declaration lives is the interesting half, and it is § 15's fault arriving for
    the third time.** An archetype declares `CONSUMED` beside the code that reads it, and that
    works because a params module's bytes are out of the building hash. The terrain's reader is
    `terrain_gen.py`, whose bytes go into the ground's hash WHOLE — so writing the map where it
    belongs immediately re-staled the ground and demanded a Blender bake for a constant that
    cannot move a vertex. That is exactly what § 34 paid off one level up, one week's worth of
    the same lesson: it is in `generators/terrain_inputs.py` instead, beside the denylist, which
    is the same kind of statement about the same generator. What co-location would have bought
    is bought by `test_declared_terrain_reads_are_real_reads`, which scans the generator for a
    read of every declared key — one step weaker than the structure side's perturbation test,
    which needs numpy the gate deliberately does not have.
    **And the key is called `mesh`, not `geometry`, because a test refused the obvious name.**
    `geometry` is what a record calls this declaration, and in a GeoJSON it is the feature's
    coordinates: adding it to the hash's denylist stripped every traced bank line, river ring
    and slough centreline out of the ground's staleness hash, so a bank could have been redrawn
    and the committed mesh would still have read fresh.
    `test_terrain_prose_is_not_read_by_the_generator` — written for a different purpose in § 34
    — caught it on the first run. The scheme is `resolved-spec-v2` and the manifest was
    re-stamped without a bake; the proof is the same one § 34 gives, run rather than asserted:
    the ground's input document at the previous commit and at this one are identical apart from
    the scheme label.
    **What it still cannot see.** A figure declared `simplified` when it is really `absent`, or
    the reverse — the states are the author's reading of what the mesh does, and only the
    CONSUMED half is checked against code. A zone the spec describes and the generator ignores
    ENTIRELY is caught only if it grades itself, since an ungraded block makes no claim and
    reaches no panel. And `restated_in_code` is the one state that asserts an agreement nothing
    enforces, which is a smaller version of the fault this whole family of checks exists to end.

36. **The declaration that was a promise, and the three figures that were making it under a state
    that asks nothing.** § 35 ends by naming its own residual in one sentence: *`restated_in_code`
    is the one state that asserts an agreement nothing enforces, which is a smaller version of the
    fault this whole family of checks exists to end.* The other three `mesh:` states say the ground
    does NOT contain a figure, and a reader who doubts one of them can go and look at the ground.
    This one says the opposite — the mesh contains exactly what this figure says and gets it from
    somewhere else — which is a claim about two documents at once, and neither of them knew about
    the other.
    **`terrain_inputs.RESTATES` names the second half, and the gate compares them.** Three kinds,
    in descending order of what the check buys, and saying so is part of the declaration rather
    than a caveat to be inferred. An **artifact** claim is held against the heightfield the bake
    wrote: `water.surface_ft` is 0.0 ft and `heightfield.json` records `water_surface_m` 0.0, so
    editing the spec's zero now fails instead of telling a visitor the river stands somewhere the
    ground does not — the strong one, because the thing being agreed with is the ground and not a
    description of it. A **figure** claim is held against the build instruction it restates. A
    **code** claim is prose describing an algorithm, which cannot be compared to Python at all, so
    it is held only to the presence of the generator line it names.
    **The three that were hiding were declared `record_only`, and that was the finding.** Each
    division's `bank_crest_ft` restates the crest the bank ramp arrives at, which is `near_ft` —
    the ramp multiplies the division level and reaches 1.0 at the top of the face. Every one of
    the three `mesh_note`s said so, and the south division's said, in as many words, *the two carry
    the same number and nothing checks that they still will*. `record_only` means a figure that was
    never a build instruction and owes nothing; a value that restates a build instruction is not
    that, and the wrong state is what kept the sentence a sentence. They are `restated_in_code` now
    and the gate holds each crest to its level. **All seven agree today**, which is the honest
    result: this check found a misdeclaration rather than a wrong number, and its value is that the
    next edit to `near_ft` cannot leave the panel showing the old crest.
    **The comment trap is pinned, because this project has walked into it before.**
    `check_sidecar_contract` reported ITSELF on its first run — the comment written to explain why
    a field is no longer read names that field, and a regex does not know prose from code. So the
    generator scan strips comments with `tokenize` rather than a regex (a `#` inside a string
    literal is not a comment), and the test proves the stripping by requiring a phrase that exists
    in `terrain_gen.py` only inside the comment arguing for the ease-out to satisfy nothing.
    **Where the map lives is § 15's lesson for the fourth time.** It is in
    `generators/terrain_inputs.py` beside `CONSUMED` and the denylist, not in `terrain_spec.json`:
    a `restates:` key in the spec outside the stripped `mesh` block would be a mesh input, and
    writing down a declaration that cannot move a vertex would have cost a Blender bake. Nothing
    was re-baked in this slice and nothing needed to be — the terrain hash strips `mesh` and
    `*_note`, so re-declaring three figures and rewriting five notes left the ground fresh.
    **What it still cannot see, and the weak kind is the whole of it.** A `code` claim proves that
    a line is present, not that the line does what the sentence says: rewrite the ease-out into a
    smoothstep under the same expression and the gate is content. Its realistic failure mode is a
    false positive on a reformat, which is the right way round — the sentence in the spec and the
    line in the code are supposed to move together, and a gate that fires when only one of them
    does is the warning § 35 says this state owes to whoever edits the generator. The strong kind
    is available wherever the restated figure is a NUMBER; the three prose ones are prose because
    an algorithm has no number to compare. And `bank_crest_dossier_zone` is deliberately left
    `record_only` even though it duplicates `bank.dossier_zone`: a pointer into a research table
    restates a document, not a mesh, and widening the state to cover that would make it mean two
    things.

37. **The category between a building and an exclusion, and the promise it had been making to
    nobody.** § 26 gave a visitor the difference between three statements an empty lot cannot
    make — nobody researched this, the evidence dates it later, it had already come down — and
    said in its own last paragraph that a fourth was deliberately left out: the **watch list**,
    four structures whose 1835 status is genuinely open rather than settled. It has been four
    free-text sentences in `data/exclusions.json` since the scaffold, read by agents only, and
    it opens by stating its own purpose: these are listed *"so nobody promotes them to
    documented without new evidence"*. **One of the four is a committed record**, so that
    sentence was checkable from the day the record landed, and nothing checked it. A promise
    with no mechanism is this project's own recurring fault, and this is its plainest instance:
    the file that exists to stop a promotion could not have noticed one.
    **It is data now, and `check_watch_list` holds it to the record's rules.** Each entry
    carries what is open, what settling it would change, a dossier pointer that must resolve to
    a committed file AND to a line inside it, and either citations that resolve in
    `data/sources/` or a sentence saying why there are none. The dataset half runs in both
    directions: an entry naming a committed record must say which claim carries the doubt
    (`carried_by`), that claim must exist on the named phase, and it **may not be
    `documented`** — the day the evidence arrives, the gate fails and the entry has to be argued
    off the list rather than quietly outgrown. The reverse is the L12 drift (§ 13) with a check
    in front of it: an entry still calling a structure unbuilt after its record lands fails too.
    **What it did not find is worth stating as plainly as a find would be.** No entry was wrong.
    The committed four pass unchanged apart from being restructured, and the value here is the
    next entry rather than a repair — which makes this the second check in this family (with
    § 27) to switch on with nothing behind it. The one thing writing it did surface is a
    drift-shaped near miss: `western_hotel`'s line still reads as though the 1834-against-1835
    question were open on the record, and the record settled it on 2026-08-09, adopting the
    builder's own statement and deliberately declining the phase mechanism. The entry stays —
    the range is `inferred` and stopping its promotion is the list's whole job — and a
    **Revised** line says so, because the original line is kept verbatim in `original` and a
    silently corrected note is not one.
    **And the third category reaches a visitor**, under *What is still an open question*,
    derived per scene by `compile_scene.py` beside the exclusions and re-derived by `check.sh`.
    § 26 refused to put these under "What is not here" and was right: **one of the four is
    standing in front of you**. The chip is derived from the scene rather than read off the
    entry — whether a structure resolves into 1 July 1835 is a fact about the dataset and the
    date — so the Western Hotel reads *standing here — inferred* while the courthouse, the
    Agency house and Caldwell's house read *not built*, and the smoke asserts that pair rather
    than the presence of a chip, since a section stamping one label on all four would have
    passed any looser check and would have been lying about the one building a visitor can walk
    up to. The standing entry does not restate its doubt in this section's words: it names
    `frame_1834.documented_range`, the same claim the provenance card renders, so the two
    surfaces cannot describe one uncertainty differently.
    **The uncited entry is the one worth reading.** Billy Caldwell's house at State and Chicago
    Avenue rests on a dossier line saying at least one source calls the story unverified — and
    not saying which. There is no page to cite, so the entry carries no citation and a sentence
    explaining that, and the panel prints the sentence where the citations would go. An empty
    list would have read as an oversight; naming a source to fill the field would have been
    rule one broken to satisfy a gate. It also sits inside AGENTS.md's standing constraint on
    1835 and Indigenous history, which the entry says on its own face.
    **What it still cannot see.** Whether the list is COMPLETE — an open question nobody
    noticed is exactly as invisible here as a liberty nobody noticed taking, and this list has
    four entries against roughly forty researched structures. And an entry can be well-formed,
    correctly cited, honestly graded, and asking the wrong question about the town.

38. **The sum five buildings stand on was done by hand, five times, and written in prose.**
    Every gate in §§ 26-37 asks whether a claim is honest. This one asks something duller and
    more load-bearing: whether the arithmetic under a coordinate was ever redone. Five of the
    eight placed structures are the same construction — read a modern intersection centre off
    OpenStreetMap, step **half an 80 ft platted street** to the kerb, stand a named face on it —
    and that construction lived as a sentence repeated once per record. The number 12.2 appeared
    in five paragraphs and in no file.
    **The sums are all correct**, which is the least interesting thing here: the eight
    constraints now recomputed reproduce to within 0.02 m, the rounding. Nothing was *making*
    them correct, and the next placement was going to be done the same way.
    **What the prose actually cost is that the module could not be changed.** `hogan_store.md`
    § 5 records a live disagreement — 80 ft annotated on Hathaway 1834 against Currey's 66 ft —
    and ends by saying nothing moves on account of it. That was true and it was also the only
    available answer, because settling it meant editing five paragraphs and redoing five sums by
    hand. `data/traces/street_control.json` now holds the module once, graded `inferred` with its
    reasoning and its dissent recorded beside it, and `check_position_derivations` rebuilds every
    placement from it. The disagreement is now one edit and a list of which buildings moved:
    2.13 m each, five of them.
    **The check is asked of the placed shape, not of the coordinate**, and that is the whole
    design. A record's coordinate is the footprint polygon's own origin, so at a facade bearing
    of 270 it is not the corner the claim is about — the Green Tree's recorded easting sits
    24.4 m from the intersection where the claim says 12.2. Comparing coordinates to kerbs would
    have passed a building standing correctly and passed one rotated out of its lot with equal
    confidence. The self-test's discriminating case is therefore one building appearing twice,
    with only the rotation and the origin differing.
    **Writing the control down found the thing prose was hiding: two coordinates for one
    junction.** Canal and Kinzie was averaged over five shared OSM nodes on 2026-08-09 for the
    georeference and over three on 2026-08-10 for the North Branch bridge, giving points 3.8 m
    apart. Not a disagreement about where the junction is — two subsets of one crossing, chosen
    by two pieces of work, neither recording that a choice was being made. **The bridge is not
    moved**, deliberately: its span is the distance between the traced 1834 banks along its
    centreline, that distance is a mesh parameter, and re-deriving it stales the committed GLB
    and asks for a Blender bake. So the record declares the 2.93 m variance and the gate checks
    that the declared number is the real one. An undeclared 2.93 m stays invisible; a declared
    one is a queued correction with its cost written down.
    **Three of the nine placements are declared unrecomputable, with reasons**, because the
    alternative is a check that certifies guesses: no surviving street here (Miller House), a
    position stacked on another inferred position (Walker's meeting house), an interpolation plus
    a free 40 m north of a crossing (Wolf Point Tavern).
    **What it does not claim, stated exactly.** It verifies the dataset against **its own stated
    control**, not against OpenStreetMap. Two of the four control points — Lake × Market and
    Randolph × Canal — were read for placements in 2026-08-09 and their node ids were never
    recorded, against `osm_streets_2026.json`'s own promise that they always are. The file
    declares both gaps and the gate requires the declaration, but the coordinates cannot be
    re-fetched from them. An attempt to re-fetch during this slice failed (Overpass 504 and empty
    name queries), so the gap is recorded, not closed, and it is the first thing owed here.
    **CLOSED the same day — § 39, and closing it moved a building.** Every
    coordinate also still carries the georeference's ±20 m, which no amount of internal
    consistency touches. See `docs/RESEARCH/street_module_1830.md`.

39. **The first thing owed was paid, and it moved a building.** § 38 ended by saying that two of
    the four control points could not be re-fetched from the source they cite, that an attempt had
    failed on Overpass, and that closing it was the first thing owed here. It is closed. The
    OpenStreetMap API answers where Overpass would not, and it answers two different questions,
    both of which were needed: `/map?bbox=` re-derives *which nodes a junction is*, and
    `/nodes.json` re-fetches *where those nodes are now*. `tools/refetch_control.py` does both. It
    is not in `tools/check.sh` and will not be — a commit gate that needs the network fails
    offline for reasons that have nothing to do with the commit.
    **Closing it required writing down a rule nobody had written down**, and that turned out to be
    the whole finding. A junction is the nodes shared by the two named **surface roadways**,
    averaged. What was never stated is what does not count: a way still under construction, a
    differently-named street stacked underneath — Market Street's modern successor is three
    streets here, Upper Wacker over Lower Wacker over a service drive — and **bikeways and
    footways**, which are mapped a few metres off the roadway they follow.
    **One junction reproduced, one did not.** Lake × Market comes back as two nodes 17.68 m apart,
    Lake Street crossing both carriageways of Wacker's bend, and their midpoint is the committed
    coordinate to 0.04 m: the 2026-08-09 reading is confirmed, and the Sauganash and Hogan's store
    do not move. Randolph × Canal is a single crossing node, and it is **4.44 m** from the
    committed coordinate. **The Western Hotel moved 2.14 m west and 3.89 m south.**
    **What the old number was made of is inferred, and the inference is not a coincidence.** The
    committed value is reproduced, to 0.04 m, by averaging the roadway crossing together with the
    three crossings the Canal Street and Randolph Street *bikeways* make. Four other four-node
    subsets nearby also average to within 0.12 m — arithmetic coincidences are cheap when enough
    nodes are in reach — so what lifts this one above them is stated rather than assumed: it is the
    only semantically coherent set, **the identical inclusion is visible in `kinzie_canal`**, and a
    name query written as a substring match ('Canal Street' matching 'Canal Street Bikeway')
    produces exactly this at both junctions and nothing extra at the other two, where no bikeway is
    mapped. One habit, two wrong coordinates, invisible because the ids were never written down.
    **It also settled § 38's other open question, the one that had no method behind it.** The two
    coordinates for Kinzie × Canal were described as two subsets of one crossing chosen by two
    pieces of work, neither recording a choice. They are not equivalent readings: two of the five
    committed nodes are Kinzie Street **Bikeway** × Canal, and the other three average to the
    bridge's 2026-08-10 reading to a centimetre. One applied the rule; one did not. The five-node
    mean is kept anyway and the correction stays queued with its cost written down — it is
    georeferencing GCP HB, so re-deriving it re-runs the Hathaway cross-check, and it is the
    bridge's control, so moving it re-derives the span from the traced banks and asks for a bake.
    **The gate now asks for the names, not only the ids.** Ids are re-fetchability: they say where
    those nodes are today, and they say nothing about whether they are the right nodes, which is
    the fault that actually occurred. A control point recording ids must now also record the two
    modern street names that make the junction and its lat/lon. Two new self-tests hold it, and the
    discriminating one is a control point whose ids re-fetch perfectly and whose *set* nobody can
    check.
    **What it still cannot claim.** That the control is right. This compares the dataset to a 2026
    street map; the ±20 m the georeference carries onto the 1834 sheets is untouched by any of it,
    and the correction here is an order of magnitude inside that. Two of the four control points
    are still single-node crossings, where "the mean" has nothing to average and the junction
    centre is wherever one mapper put one node.

40. **The largest claim a visitor stands in front of, and the card had no words for it — plus the
    second time this exact silence has been found by somebody reading a file.** Every honesty
    surface in §§ 26-39 grades something. None of them graded the **outline**: `compile_scene.py`
    carried `footprint.confidence` into the sidecar and dropped `footprint.sources` and
    `footprint.note` on the floor, so the biggest single claim in front of a visitor — the shape of
    the building — reached the card with no chip, no source and no reasoning, while `roof_pitch_deg`
    carried all three. **Six of the eight outlines open with the word PLACEHOLDER** and say in their
    own first line that no dimension is attested in anything reached; two are the opposite (Hogan's
    store's twenty by forty-five feet, twice in Andreas; the bridge's ten feet over a measured span)
    and two are in between (the Green Tree reasoned out of a room module, the Western's L-envelope
    attested with the limb assignment not). A visitor could read none of it.
    **The gap has a history, and it is the sharpest part of this.** The massing rule once took the
    worst confidence across the footprint, so an unknown SIZE dithered a well-documented building
    into ghost massing — fixed after the first live look by narrowing the tint to the attributes that
    say what a building WAS. That fix is recorded in this file, and it ends with the sentence
    *dimensional uncertainty is carried in the sidecar, where the popup shows it*. The sidecar
    carried it. **The popup was never given it.** So the one claim deliberately removed from the view
    is the one that had no surface anywhere, and the compensating disclosure was a sentence in a
    status file rather than a thing that was built.
    **No dimension is printed, and that is the decision rather than the omission.** § 28 refused to
    put the footprint on the card for exactly this reason — the only printable value is the polygon
    and printing a polygon means reducing it, so a bounding box over Miller's L-plan would be a
    measurement the record does not make, on the card that exists to admit inventions. What that
    argument settles is the VALUE, not the claim: the shape is already in front of the visitor at
    full size, and what was missing is how much of it is evidence. `claimRow` renders no value cell
    at all for a `null` value — which is not `—`, and is the same rule as an attribute with no note
    showing no note — and the smoke pins the absence across all eight buildings so a later slice
    cannot fill it by accident.
    **The mechanism, because this is the second instance and the first was found the same way.**
    `documented_range` (§ 28) and the footprint were both graded in the record and silent on the
    card, and both were found by a person reading a file. That is now countable: the smoke reads
    every record's graded claims — the date span, the position, the footprint, every form attribute —
    and requires the claim tables and the location line to carry exactly that many chips, for every
    building. **Run against the previous commit it reports all eight buildings one chip short**,
    which is the discriminating proof and was run rather than asserted.
    **What it still cannot see** is a claim that reaches a chip and says the wrong thing, and a chip
    count says nothing about whether the reasoning underneath it is any good. It also cannot see a
    field the compiler never writes at all: `check_sidecar_contract`'s unread-field report is
    top-level only, so `footprint.confidence` sat compiled-and-never-read for the life of the project
    inside a key the renderer *does* read for collision. Widening that report to leaf paths was considered
    and refused — the scan cannot follow a value into a function, so `documented_range.note` and
    every field `evidence()` reads generically would come back as false findings, and a noisy gate
    gets disbelieved, which § 15 already paid for once.

41. **The doubt was in the panel, the promise about the card was in the panel too, and the building
    the argument is about said nothing.** § 26 ended by saying the watch list's uncertainty "belongs
    on the records and in the provenance popup, which is a different slice and is not queued";
    § 37 shipped the panel half and its entry for the one STANDING structure ends, in the rendered
    text a visitor reads, with *and the provenance card shows it*. The card showed the **claim** —
    `1834-01-01 → 1840-12-31`, `inferred`, with the record's own note behind a `why`. It never showed
    that the claim is a tracked open question: not that the dispute is the builder's own statement
    (chicagology, W. H. Stow, "it was built in 1834") against an undated line in a hotel chronology,
    not that the later date would make the house brand new or unfinished on the scene date, and not
    that the grade is being **held down deliberately** so the evidence has to arrive before it moves.
    So the dispute reached whoever opened a panel about the whole town and not whoever walked up to
    the house it is about — which is precisely the gap the liberties had before § 11 attached them to
    their buildings.
    **The section is the panel's own entry, rendered by the panel's own code.** `uncertaintyEntryHtml`
    takes an `onCard` flag and `openQuestionsFor` is `libertiesFor` for the other list; two renderers
    would have let one uncertainty be described two ways, which is the drift the shared liberty
    entry exists to prevent. Two things change on the card and nothing else does: the chip drops
    "standing here" (the visitor's own position, not news) and carries the grade of the claim the
    doubt sits on, and the line that points at the card stops pointing at the card it is printed on.
    Nothing was added to `data/`, no sidecar moved, and no mesh is stale — the derived list the panel
    already fetches is the list the card filters.
    **A building with nothing open renders nothing, which is a decision and not a missing empty
    state.** "No open questions are recorded about this building" would read as *this building is
    settled*, and § 37 states exactly why that cannot be promised: four entries against roughly forty
    researched structures, and an open question nobody noticed is as invisible as a liberty nobody
    noticed taking. The smoke asserts the silence across the other seven buildings, because a card
    dumping the whole list would have passed every assertion about the Western Hotel.
    **And the promise about the other surface is a gate.** This is the third time a sentence in this
    project has described a surface it could not see — `documented_range` (§ 28) and
    `asset_is_placeholder` (§ 29) were both read by a card the compiler never fed, and both were
    found by a person reading a file. `carried_by` could have named any graded block on the phase,
    including one the card renders no section for, and the panel would have gone on promising it.
    `check_watch_list` now maps the record's claim to the sidecar path the card reads and holds that
    path to being one `renderers/web/js/popup.js` really reads, scanned by § 29's own machinery — so
    deleting a section from the card fails here rather than leaving a false sentence on the panel.
    The self-test's discriminating case is a well-formed, correctly graded claim (`demolition`) that
    the card has no words for. A smaller hole closed with it: a doubt may only sit on a claim that
    carries a confidence, which `form` — a dict of graded attributes, graded nowhere itself — did not.
    **What it still cannot see.** Whether the list is complete, which is § 37's limit and untouched
    by any of this. Whether the question is the right question about the town. And the map from a
    record's claim to a card section is authored: the check proves the card reads the path, not that
    the section a visitor sees is the one the entry meant.

42. **The number five buildings are placed from was an annotation nobody had checked, and
    checking it found the control point standing in the middle of a block.** Every platted
    placement here steps half a street from a surviving modern junction, and that half-street is
    one figure: 12.192 m, half of 80 ft. § 34 made it one figure in one file so it could be
    argued with, and then recorded the argument and left it: 80 ft is annotated on Hathaway 1834,
    Currey says the 1830 plat used 66, and the memo's own § 2 said settling it meant reading the
    widths off the sheet street by street. Nobody had.
    **It is read now, and 66 is out.** `tools/measure_street_widths.py` runs one traverse per
    1834 sheet along the block row south of Lake Street and measures every corridor it crosses,
    block boundary line centre to block boundary line centre: eight corridors — Desplaines,
    Jefferson, Clinton, Canal on each sheet — between **75.7 and 92.8 ft**, none within 9 ft of
    66. The reconciliation § 2 wanted tested dies on the same reading: those four ARE the general
    streets of the west division, which is exactly where a 66 ft general width would have to
    show. The check that this is reading the map rather than its own thresholds is the pitch:
    seven consecutive corridor spacings between 116.6 and 123.2 m, which is the 300 ft block plus
    one street the plat describes, and nothing asked them to be.
    **What it does not settle is in the file too.** The median is **84.8 ft**, five feet wide of
    the figure the dataset uses, and that is recorded rather than rounded away: what was measured
    is the corridor two draughtsmen drew on paper that has stretched 3.7-4.5%, and what
    `platted_street` claims is what Thompson platted in 1830. So the grade stays `inferred` for a
    NEW reason, stated in the file, and nothing in the dataset moves. The alleys read 17.1-18.7
    ft, consistent with 18 and not conclusive against 16 — two feet is inside this method's
    error, and a reading that cannot separate two figures does not get to pick one.
    **The traverse starts at a control pixel, and that is where the real finding came from.**
    Hathaway's HA and Wright's G5 both claim to be *Canal St & Lake St*. HA sits **52.4 m** west
    of the Canal corridor centreline and G5 **20.2 m** west, both inside block 28 — and the
    sheets say so themselves, because the block number *28* is printed straddling each recorded
    pixel and a block number is never printed in a street. Both appear to have taken block 28's
    mid-block alley for the street. **G5 is one of the eight points the datum is fitted from**:
    refitting with it on the centreline moves the origin **15.0 m** and leaves the RMS at 17.5 m.
    That is 40% of the ±20 m this project declares, and it is a candidate account of a good part
    of the 57.9 m cross-map disagreement the datum memo has carried as its honest ceiling with no
    explanation.
    **Queued, not adopted, and pinned so it cannot rot.** Moving the origin re-derives every
    coordinate and stales every mesh — a bake and a whole-dataset review, not a slice. So the
    figure is committed with `status: "queued, not adopted"`, and `check_street_module` holds both
    the offset and the exposure to the GCP pixels they were computed from: the day either
    correction is adopted, the gate fails until the sheets are read again. A finding whose inputs
    have moved is not a finding.
    **The gate is the offline half of the measurement.** The tool needs the network, and a commit
    gate that needs the network fails for reasons that have nothing to do with the commit. So
    `check_street_module` re-derives every committed metre from its committed pixels through the
    sheet's own affine, re-derives the summary from the readings, and requires the adopted module
    to be the candidate those readings support — the discriminating self-test is a file in which
    nothing is malformed, every metre checks out, and the figure five buildings stand on is the
    one its own readings exclude.
    **What it cannot do, and the half of the reading thrown away.** A second traverse, N-S along
    Canal, would have measured Lake and Randolph. It is not committed: on the Wright sheet it
    reads lot lines, and every test that separates a lot line from a street on Hathaway fails
    there — Wright's lot depths are 20-26 m, which is a platted street's width; a lot line runs as
    far as a block face does, because the line at the same depth continues across the alley; and
    two of its spacings land inside the module band by coincidence. Rather than tune a filter
    until the answer looked right, that half was dropped and said so. So the E-W streets are still
    unmeasured, which is also what S9 needs, and it needs a method that identifies a corridor by
    something other than its width. Ten of the thirteen control points on the two sheets have not
    been checked against their corridors either.

43. **The ladder every one of these gates stands on was enforced by nothing, and switching it
    on found four `documented` values resting on a source whose own record forbids exactly
    that.** Every honesty check in this project asks a question that presumes an answer to an
    earlier one. Is the value graded? Does the grade owe a source? Does the source resolve? Was
    the invention admitted? Did the attribute reach a vertex? Is the mesh the one the record
    describes? None of them ever asked **how good the source is** — the word `tier` did not
    occur anywhere in `tools/validate.py`. `docs/PROVENANCE.md` ranks the evidence on six rungs
    and attaches two rules to the ranking; `data/source.schema.json` writes the same ladder into
    the field description; and a `documented` attribute could have rested on a decorative 1940
    pictorial map without a single check complaining.
    **The ladder is read from one place now.** `tools/tiers.py` parses the rungs out of the
    schema's own `tier` description, and both halves of the project consume that one parse:
    `check_evidence_ladder` holds the dataset to it, and `tools/compile_scene.py` compiles the
    words into each joined citation so the provenance card can print them. A rung the schema
    validates but does not spell out raises rather than returning a shorter ladder — a silently
    empty ladder passes everything, which is the failure mode this family of checks exists to
    stop. Three rules are errors and pass on the committed data today: a `documented` value
    needs one source at tier 4 or better, a `footprint` graded above `conjectural` may not cite
    a tier 5-6 retrospective, and no tier 5-6 source may declare `asset_use: geometry`. The
    self-tests carry the discriminating cases, including the two the rule must NOT fire on: a
    period survey cross-checked against a 1933 pictorial map, and that same map carrying a
    *position* to `inferred`, which is what the 2026-08-10 revision of the tier rule exists to
    permit.
    **Where the document disagreed with itself, the disagreement is recorded and a reading is
    picked.** `docs/PROVENANCE.md` states the tier-5 rule twice and not identically — the table
    says never the *sole* evidence, the revision says "never reaches it, alone or in company".
    The table's reading is enforced, because forbidding a documented value from *citing* a
    retrospective beside a period survey would punish corroboration, which is the opposite of
    what the revision was written for.
    **The fourth rule is a warning and it has 21 findings in it.** A `documented` value with no
    source at tier 3 or better rests on later scholarship alone — no period document, no
    eyewitness recollection, no compilation from pioneer testimony. Five values on the Green
    Tree, four on Miller House, four on the Western, three on the Wolf Point Tavern, two on the
    Sauganash and three ground claims. **Four of the twenty-one are sharper than the count
    says**, and they were found by reading the source records rather than by the gate:
    `sauganash_hotel` `form.stories` and `form.construction`, `miller_house`
    `form.frame_addition_stories`, and `wolf_point_tavern` `form.sign` are supported by nothing
    but `drloih_hotels` or `drloih_wolf_point` — two unfootnoted blog compilations whose OWN
    records in `data/sources/` say, in their own words, *use only to generate leads and to
    corroborate; never as sole evidence*. The dataset is making exactly the use its own source
    records forbid, and the wolf sign is one of them: the `documented` chip that justified a
    whole slice of modelling work rests on a page that says do not rest on it.
    **Priced and queued rather than taken, for the reason § 42's datum exposure was.** Failing
    these would force a regrade, a confidence is a mesh input, and a regrade therefore arrives
    with a Blender bake attached. It is also not a rename: a page transcribing an 1833 newspaper
    is tier 2 whatever site hosts it, and this dataset already grades `chicagology_prefire252`
    that way, so each of the 21 is either an over-graded value or an under-tiered source and
    only reading the page settles which. The queue is in `docs/ROADMAP.md` § S5, and the machine
    -readable half of it — a `never_sole_evidence` flag on a source record, which would turn
    those four into errors — is queued behind the regrade rather than added now, because a gate
    that fails the committed dataset the day it lands is a gate that gets switched off.
    **And the number the card printed at a visitor said nothing.** `tier 4` has been on the
    citation line since it was written, beside a citation, in a panel whose entire argument is
    that a person can judge the evidence for themselves — with no table anywhere in the
    walkthrough to look a rung up in. It reads `tier 4 · later scholarship` now, out of the same
    ladder the gate enforces. The smoke asserts it as a pair on one card, each label matched to
    its own citation: the Sauganash cites Wright 1834, Wau-Bun and a Kurz & Allison
    chromolithograph, so a card stamping one rung on every line, or the right words against the
    wrong citation, fails where a presence check would pass. Run against the previous commit it
    reports every citation on the card one label short.
    **What it still cannot see.** A tier is a judgement about a source made once, in the source
    record, and nothing re-examines it — the ladder checks that a claim rests on a rung, not
    that the rung is the right one. `chicagology` pages are graded per page, which is correct
    and is also why the 21 exist; the two `drloih` pages are graded 4 and their own notes argue
    they are weaker than that. And `asset_use` cannot be used as a rule: `cross_check` is the
    schema's default and 22 of 28 sources wear it, including both tier-1 survey sheets, so it
    means "nobody set it" and not "corroboration only". Do not build a gate on that field
    without setting it deliberately first.

44. **The rung was a judgement about a website, and reading three of them moved fifteen values
    without touching one.** § 43 ends with an ambiguity it could not resolve: 21 `documented`
    values rest on later scholarship alone, and *either the values are over-graded or the
    sources are under-tiered*. The two halves cost very different things — regrading a value is
    a mesh input and arrives with a Blender bake, regrading a source is reading — so the cheap
    half went first. The three chicagology pages carrying fifteen of the twenty-one were
    fetched, read in full and identified from their own printed attributions. **All three are
    transcriptions of near-primary recollection and all three were graded 4.** They are 2 now,
    and the count in `check.sh` reads **six**. Memo:
    `docs/RESEARCH/evidence_tiers_chicagology.md`.
    **What each one turned out to be.** `prefire127` is the *Inter Ocean* of 1 July 1883 — a
    sketch of the Green Tree carried to people who had slept in it, printing their corrections
    in their own words, with Edwin Gale's 1902 *Reminiscences* under it and nine city
    directories 1839-1885 around it. `prefire273` is the *Chicago Magazine* of 15 May 1857,
    written from George Davis's 1832 drawing and from Gurdon S. Hubbard's account given to the
    writer directly. `prefire278` is the *Inter Ocean* of 22 July 1883, the same series a
    fortnight later.
    **Two of the three source records were wrong about their own page, and the second one is
    the finding.** `prefire273`'s citation said the page compiles Andreas and the Fergus
    series; the body is the 1857 magazine, and Andreas is a separate section nothing here reads
    through this page. Worse: **every value citing `prefire278` is about the Western Hotel, and
    the record described only the town code of 7 November 1833.** The material four claims rest
    on — "The Old Western Hotel: First Frame House on the West Side", the interviews giving the
    farmers' house, Stow, the two storeys and the stable yard — was not mentioned in the record
    at all. A source record that does not name the half the dataset uses is a citation nobody
    can check, and it passed every gate this project has, because every one of them asks whether
    a `source_id` resolves and none asked what is inside it.
    **So the judgement is a declaration now.** A record that dates its own RETRIEVAL rather
    than a document — `date` reading "accessed 2026-08-10" — and claims a rung at or above
    testimony must declare `transcribes`: the documents it carries, each with its date, its own
    rung, and a note saying which of this project's claims it carries. **The record's tier is
    then the best rung declared** — derived, not typed beside it, the same argument as a
    changelog version. `check_transcription_declarations` holds it in both directions, and the
    discriminating self-test is a record in which every field is well formed and the number is
    the one its own declarations exclude.
    **It has one finding on the committed data and it is a sentence being made checkable.**
    `chicagology_kinzie_bridge` has said since it was written *"Tier 3 for the Andreas
    transcription; the surrounding apparatus is a finding aid"* — true, and readable by nobody.
    Fourth instance in this project of a true sentence describing something no check could see;
    the Andreas passage is declared and the tabulated bridge chronology is explicitly not.
    **Apparatus is deliberately excluded from the declaration, and that is a rule with a
    reason.** `prefire127` carries nine period city directories, which are rung-1 documents; no
    claim here rests on them, and declaring them would drag the record's rung onto evidence this
    dataset does not stand on. They stay in the note. The cost is that under-declaration is
    possible and no check can see it — stated rather than papered over.
    **What did NOT clear, which is the part worth keeping in view.** Six remain and four of
    them are § 43's sharp ones, unchanged and unclearable this way: `sauganash_hotel`
    `form.stories` and `form.construction`, `miller_house` `form.frame_addition_stories` and
    `wolf_point_tavern` `form.sign` still rest on the two `drloih` blog compilations alone, and
    those pages' own records say *never as sole evidence*. That is a regrade of a value, so it
    is a bake, and it stays queued.
    **And one cleared warning is thinner than the others, said here rather than left to be
    found.** `miller_house.form.frame_addition` is `documented`, and what the 1857 magazine
    attests is *"a log structure partly sided"* — that a frame element existed. The words the
    record quotes, *"a two-story house added to the cabin, fronting the river"*, are drloih's.
    The record's split turns out to be exactly right, because the storey count is carried
    separately and is one of the four that did not clear — but the general point is a limit of
    the gate: **the ladder check is per-value and a source lends its rung to every attribute
    that lists it**, so a cleared warning is not by itself better evidence. The memo walks all
    fifteen one at a time for that reason.
    **What it still cannot see.** Whether a rung is the right rung: the declaration makes the
    judgement re-derivable, not correct. Whether a declared document says what its note claims —
    a human read put it there and a human read is what would overturn it. And nine pages at
    tier 4 or weaker date their own retrieval and declare nothing; three of them
    (`prefire062` quoting the *Chicago American* of 9 July 1835, `prefire276` transcribing the
    same 1857 magazine as `prefire273`, `wikipedia_chicago_river` quoting Swearingen's 1803
    account) look like exactly this case, and none was opened. Looking like the case is what
    this slice exists to stop being sufficient. The validator counts them every run.

45. **Two of the three pages were the case, the third reprints nothing, and the third is where
    the water surface's strongest chip comes from.** § 44 ends by naming three pages that *look*
    like modern hosts carrying old documents — `chicagology_prefire062`, `chicagology_prefire276`
    and `wikipedia_chicago_river` — and by saying that looking like the case is what that slice
    exists to stop being sufficient. All three are opened now. Memo:
    `docs/RESEARCH/evidence_tiers_round_two.md`.
    **`prefire062` is Andreas, not the newspaper, and the rung follows the document that is
    actually there.** The record said *"Quoting the Chicago American, 9 July 1836"*; the page's
    body is set under its own heading, *History of Chicago, Volume I, A. T. Andreas, 1884*, and
    it is Andreas who quotes the American mid-paragraph in a chapter on street grading. **Third
    source record in this dataset found wrong about its own page** (`prefire273` and `prefire278`
    were the first two), and the same class of fault: a citation nobody can check passing every
    gate, because every gate asks whether a `source_id` resolves and none asks what is inside it.
    Tier 4 → **3**, on Andreas — deliberately not the 1 the newspaper would carry, because the
    *Chicago American* of 9 July 1836 has never been opened here and promoting the page to 1
    would let a future value stand on a period document laundered through a compilation. § 44's
    own account of this page is also wrong by a year: the item is **1836**, not 1835.
    **`prefire276` is the 1857 magazine, tier 4 → 2 — and what is NOT declared is the more useful
    half.** It carries the same *Chicago Magazine* of 15 May 1857 that took `prefire273` to rung
    2, written from what the oldest residents told the writer, and it is the independent
    corroboration that the fort was occupied "till the removal of the Indians in 1836". A
    *Chicago Tribune* notice of 27 March 1856 is printed below it and would derive this record to
    rung **1**; nothing here rests on it and nothing will, so it stays apparatus under the rule
    § 44 wrote. The same goes for the dimensioned Hesler woodcut caption — and **that undeclared
    caption is now a mechanism rather than a warning in capitals**: the record has said since it
    was written that its three fort dimensions are unattributed and must not promote anything,
    and leaving the caption out of the declaration is what enforces it.
    **`wikipedia_chicago_river` was not the case at all, and saying so needed a word that did not
    exist.** It reprints nothing: the Swearingen material is one sentence of encyclopedia prose
    with a footnote — *Journal of Lieutenant James Strode Swearingen reproduced in Quaife 1913,
    pp. 373-377* — and **a citation is not a transcription**. A page nobody has opened and a page
    opened and found to carry no document declare exactly the same thing, so the validator's note
    would have gone on calling this one unread: a true sentence describing something no check can
    see, arriving inside the gate written to end that. `carries_no_document` is the third state —
    the reading itself, not a flag — mutually exclusive with `transcribes`, and a record
    declaring it may not be graded at or above the testimony rung, because there is no document
    on the page for the rung to be a judgement about. The counter reads three states now: **6
    declare their document, 1 was read and reprints none, 6 remain undeclared** (from nine).
    **And the footnote is worth more than the regrade would have been.** This record has asked
    since it was written that somebody *chase Swearingen to a primary printing*. It is named,
    dated and paginated now — Quaife, *Chicago and the Old Northwest, 1673-1835* (1913),
    pp. 373-377 — five pages, and the 1803 soundings stop resting on an encyclopedia.
    **The consequence, and it is the first of the six warnings to be settled the other way.**
    `terrain_spec.json` grades ground `water` **`documented`** on this record alone. Swearingen
    gives a width, a depth and two bank heights, no gradient, all measured at the fort 1.2 miles
    downstream — so the flat surface does not rest on him. What supports it is Wikipedia's own
    unfootnoted sentence that the river "flowed sluggishly into Lake Michigan from Chicago's flat
    plain", in a section about the 1900 reversal. § 43 asked whether each warning is an
    over-graded value or an under-tiered source; five are still open and **this one is the
    value**. `documented` → `inferred` is queued rather than taken, at the stated price: a
    confidence is a mesh input, so it stales the ground and lands with a Blender bake this runner
    does not have. `docs/ROADMAP.md` § S5.
    **What this does not settle.** Whether a rung is the right rung — unchanged. And
    **under-declaration is still invisible**: both chicagology pages here carry documents
    deliberately left out on the apparatus rule, and no check can tell that from having missed
    them. The mitigation is prose — the memo tabulates the undeclared documents beside the
    declared one, so the choice can be argued with rather than only trusted.

46. **The footnote was chased, and the paraphrase lost a figure it never had.** § 45 ended by
    saying that `wikipedia_chicago_river` reprints nothing but names something better: *Journal
    of Lieutenant James Strode Swearingen reproduced in Quaife 1913, pp. 373-377*. Those pages
    are fetched, read in full and recorded. Memo: `docs/RESEARCH/swearingen_1803.md`; source:
    **`quaife_1913_swearingen`, tier 1** — the first written eyewitness document in this
    dataset (the three tier-1 records before it are two survey sheets and a drawing).
    **Read from two scans, which is the standard and not a formality.** Internet Archive items
    `chicagooldnorthw00quaiuoft` and `chicagooldnorthw00quai` agree on the Chicago passage
    character for character once whitespace is normalised — the same two-scan discipline
    `old_settlers_bridges_1883` was read under. Two internal checks came free: the entry heads
    itself Wednesday 17 August 1803 and that date **was** a Wednesday, and the volume's own
    index points independently at p. 377.
    **The '6 ft on the north' is not in Swearingen.** The encyclopedia prints *"the riverbanks
    were 8 ft high on the south side and 6 ft on the north"*, two measurements side by side.
    What the journal says is that the fort bank is about 8 feet and *"the opposite bank is not
    so high, not being a difference, of more than two feet, by appearances"* — a **bounded**
    difference, explicitly estimated **by eye**. Six is 8 minus the maximum, computed by a later
    writer and then set beside a sounding as though it were one. The honest reading is 6-8 ft,
    visually estimated. **Fourth citation in this dataset found misdescribing its own page**
    (`prefire273`, `prefire278`, `prefire062` were the first three) and the first found by
    opening the *document* rather than the host.
    **What the paraphrase dropped is worth more than what it garbled.** Two sentences went
    missing. *"Dead water, owing to its being stopped up at the mouth, by the washing of sand,
    from the lakes"* — the pre-cut regime in the witness's own words. And *"The banks above are
    quite low"*, which is **the only sentence in the whole passage about the reach this project
    actually models**. Every figure the encyclopedia kept is taken at the fort, 1.2 miles
    downstream, and this record's own note has warned since it was written not to carry them
    upstream. So the paraphrase preserved the numbers that do not reach the forks and lost the
    observation that does. It is attached now to the spec's `bank` block, which cited **nothing
    at all** before today, and it does not move that block's `conjectural` grade: "quite low"
    carries no number, and the 6 m profile and the 2-4 ft rise are still ours.
    **It does not rescue the water plane, and the reason is in the witness's own clause.** The
    obvious move on finding a tier-1 source saying the river stood dead is to cite it under the
    flat surface and keep the `documented`. It is refused. Swearingen attributes the stillness,
    in the same sentence, to the mouth being stopped up by sand — the `e1830_natural` condition
    that the 1833-34 cut removed, and the 1835 scene is `e1834_harbor_cut` because of it. He
    also gives no gradient at all. Citing him there would be a tier-1 source attached to a claim
    it does not make, which is worse than the tier 4 it replaced because nobody would look at it
    twice. The `documented` → `inferred` regrade stays queued at its stated price of one bake,
    better argued than it was; the water block's note now says all of this where a visitor reads
    it, and it is the block's note rather than a private file because that is what
    `terrain_inputs.py` made affordable.
    **A price the roadmap over-quoted, corrected in passing.** § S5 said citing this source from
    `terrain_spec.json` would cost a bake because source ids are inside the terrain's staleness
    hash. They are not — `resolved-spec-v2` strips `sources` with the prose, for the stated
    reason that a citation cannot move a vertex. So the citation, the two corrected notes and
    the new one were all free, and the slice that was priced as read-only shipped the attachment
    too. A confidence is still an input, which is why the regrade is still queued.
    **What this does not settle.** The manuscript itself: Quaife could not get at the original
    either — it was privately held in Dallas in 1913 — so his text is a 1903 typescript made by
    a descendant, a two-hop chain he states himself and this record repeats. Whether the 1834
    trace agrees with the half mile is left as a consistency and not a measurement (§ 7 of the
    memo): walking the traced south shore south from the fort gives at least 1 366 m against
    Swearingen's 805, across thirty-one years of a spit that grows downdrift, and nothing in the
    dataset was changed on it. And Hubbard's "not over eight feet above the River" beside
    Swearingen's eight feet is one line of arithmetic left for the fort parcel.

47. **The four pages that could still be opened were opened, and one of them had a paragraph
    that is not in the article it was credited to.** The validator has counted the same sentence
    every run since 2026-08-10 — *six pages at tier 4 or weaker date their own retrieval and
    declare nothing*. Four of the six could be read; the two `drloih` blog compilations cannot be
    saved this way and stay behind the bake their four values need. All four were fetched on
    2026-08-11 — three from their committed Wayback snapshots, the church page live — and read
    end to end. Memo: `docs/RESEARCH/evidence_tiers_round_three.md`. **The count reads two, no
    value moved, and no mesh went stale.**
    **`chicagology_lastwardance`: 4 → 2, and the record was under-reading its own page.** It said
    *"a later compilation of recollections, unfootnoted"*. The page prints one attribution line —
    **Chicago Tribune, 14 August 1910** — and the article names its witness in its own last
    paragraph: the description *"was left for coming generations by one who saw it in his youth
    and who in old age wrote it out"*, by **Judge John Dean Caton**, who reached Chicago in 1833.
    So the bridge route this dataset stands on is one identified eyewitness's own words, not a
    digest of other people's. **Rung 2 and deliberately not rung 1**: the Tribune neither dates
    nor documents the writing, and *"(which stood where the railroad bridge stands now)"* is the
    1910 newspaper locating the crossing, not Caton — a gloss no placement here uses, now written
    into `what_it_does_not_supply`. **Fifth source record found wrong about its own page**, and
    the second wrong in the under-reading direction.
    **`chicagology_prefire274`: 4 → 2, on the topography and on nothing else.** It is *"Fort
    Dearborn I"*, transcribing **Chicago Magazine, March 1857** — the installment before the one
    `prefire276` carries, in the serial that took `prefire273` to rung 2. This is **the first
    source here that had to be graded by which part of it you are standing on**: rung 2 for the
    flattened mound, the sand hills and the old southward channel, which is ground the writer
    could still walk and a channel filled inside his readers' memory, and no better than rung 3
    for its declared subject, the fort of 1803-1812, which nobody in 1857 remembered and which
    nothing here cites. One inference is declared rather than hidden — the serial's
    oldest-inhabitants method is printed in the May issue and not in this one, so March is graded
    by continuity of the serial.
    **And that page disagrees with an epoch boundary, which is recorded rather than smoothed.**
    It dates the cut through the bar to *"the Engineers of the government in 1838"*;
    `data/terrain/epochs.json` opens `e1834_harbor_cut` on 1833-07-01 with the February 1834
    storm scouring it, on Andreas. **Andreas is followed** — nearer the works, and the pier
    chronology is already his — with 1838 read as most plausibly the harbour's completion rather
    than the cut. The magazine is not made to agree. Neither date is cited by anything and the
    boundary was set before the page was read.
    **`chicagology_first_post_office`: rung CONFIRMED at 4, and it is the first of these read and
    left where it stood.** Currey's 1922 article names its authorities inline wherever it has
    them and names none for the post-office facts: later scholarship, outranked by Andreas at 3
    exactly as the record already said. `docs/ROADMAP.md` § S5 called these six *"unread rather
    than wrong"*; one of them was simply unread.
    **The finding on that page is a paragraph that is not Currey's.** The 66 ft street module —
    the rival to the 80 ft every platted placement here is offset from — is printed between his
    1832 and 1837 sentences, and it cannot be read off the page as his: it interrupts a
    chronology that is otherwise strict, its subject is a survey in an article about buildings,
    and it is the one paragraph naming no authority while writing *"downstate Randolph County"*
    and glossing a surveyor's chain for a modern reader. It is left **undeclared** — unattributed
    website prose is off the ladder altogether rather than at the rung of the article it was set
    beside, the apparatus rule running in the opposite direction from `prefire276`, where it
    withheld a rung the project had not earned. **No number moves**: the figure was excluded by
    measurement on 2026-08-10, eight corridors at 75.7-92.8 ft, none within 9 ft of 66. What
    moves is what is being disagreed with. `data/traces/street_control.json` said *"Currey
    states"*, which reads as a named historian against a survey annotation and invites reopening;
    it is a sourceless website sentence against a survey annotation and a measurement. Corrected
    there, and the 66 ft stays recorded in all three files — a dissent that vanishes is a dissent
    that gets rediscovered.
    **`chicago_temple_history`: read, and it reprints nothing.** Looked for what the
    west-bank/north-bank disagreement actually needs — a trustees' minute, a circuit rider's
    journal, a conference record, any dated quotation from one. The page is 500 words of modern
    congregational narrative, unfootnoted end to end, no bibliography, no archive named on the
    site; its one quoted document is a 1922 sermon about building the skyscraper. `carries_no_document`
    declared, and the rung cannot rise because there is no document for a rung to be about. The
    full read also shows the paragraph inconsistent with itself before it ever meets this
    project's witnesses — founded 1831, cabin 1834, floated across *"four years later"*, brick
    church on the same corner 1845 — with nothing tied to a document, which is why the west-bank
    reading rests on the two near-primary witnesses instead.
    **And that citation is re-readable now.** On 2026-08-09 no snapshot existed and Save Page Now
    produced none, so `archived_url` was deliberately left absent rather than fabricated. A
    snapshot dated **2026-06-05** was found on 2026-08-11 and verified to carry both quotations
    the record depends on, character for character. One standing validator warning gone; the
    verbatim quotations stay in the note, because an archive is a second copy and not a reason to
    stop keeping the first.
    **The pattern across three rounds and ten pages, worth stating as a rule.** The error is
    almost never the tier — it is the sentence naming what the page carries: six records now
    found describing their own page wrongly, four over-reading and two under-reading. And a page
    is not one document: five of the ten carry a transcription plus apparatus, and on three of
    those the apparatus is the more tempting half.

48. **Ten rounds of grading a source, and the sentence that justifies the rung had never left the
    repository — a third kind of unshipped claim, and the first one no existing gate could have
    seen.** The four slices above (§ 44-47) spent themselves establishing WHY a page sits on the
    rung it sits on. All of that work landed in `data/sources/*.json`, and the card printed the
    number with none of it: a visitor following `chicagology_lastwardance` reached a present-day
    blog stamped **tier 2 · near-primary recollection** with nothing saying it reprints the
    *Chicago Tribune* of 14 August 1910 carrying John Dean Caton's own recollection. That reads
    as an over-grade — the exact failure the ladder was built to prevent, produced by the one
    field that would have explained it. **Thirteen of twenty-nine source records carry at least
    one of four such fields**, and nine of the ten committed sidecars cite at least one of the
    thirteen, so this was on nearly every card in the walkthrough.
    **The fault is a new one and that is the point.** § 28 was a field READ and never emitted;
    § 30 was a field EMITTED and never read. This is a field that **never entered the interface
    at all** — `transcribes`, `carries_no_document`, `what_it_supplies` and
    `what_it_does_not_supply` are in `data/source.schema.json`, three of them with descriptions
    that address a reader in as many words ("so an agent reaching for it sees the limit before
    the citation"), and `cite()` never carried one of them into a sidecar. Neither direction of
    `check_sidecar_contract` can see it: its shape is unioned over what IS emitted, and a shape
    built from what was offered cannot report what was never offered. Nothing was broken. Every
    half was right about its own side, again.
    **So the gate is over the schema, because the schema is the one bounded set here.**
    `compile_scene.SOURCE_FIELD_SURFACE` partitions all 22 properties into visitor-facing and
    internal, each with the one-line reason, and `check_source_surface` holds it three ways: a
    property in neither half fails; a visitor-facing field that some record carries and no
    compiled citation does fails (which is exactly the state the dataset was in this morning);
    and a visitor-facing field `renderers/web/js/citations.js` never reads fails. Adding a field
    to a source record now costs one sentence saying whether a visitor sees it, written by
    whoever knows the answer. Switching it on reported the four immediately, which is the fifth
    check in this family to find something on its first run.
    **What is shown and what is not, and the line is argued rather than convenient.** The card
    gets the document (`reprints <work> <date>`, never collapsed — it is one line and it is what
    makes the rung beside it legible), the finding that a page reprints none, and the two limit
    lists behind a `<details>`. It does NOT get the prose inside those fields: the `note` on a
    `transcribes` entry and the reading in `carries_no_document` quote rung numbers, name files
    in `data/` and record HTTP statuses and fetch dates — they are addressed to whoever
    re-grades the source, and the source record is one click from the card for anyone who wants
    them. That is a partition inside a field and it is stated here rather than left looking like
    an oversight.
    **The smoke found the one place this must not appear, and it found it as a failure rather
    than as a reviewer's opinion.** `citations.js` is deliberately one renderer for every context
    that shows a source, so the reprints line arrived under "What is not here" too — and
    `chicagology_prefire278`, behind two of those entries, is headed *"The Old Western Hotel:
    First Frame House on the West Side"*. The Western Hotel is standing in this scene 200 m away.
    The assertion that a building a visitor can walk up to may not appear on the not-here list
    (§ 26) failed on the spot. Under that heading a source's account of what it carries reads as
    a claim about the town, so the list keeps the plain citation and `evidence: false` says so
    at the call site — pinned by its own assertion, so the option cannot quietly flip back.
    **Two smaller things worth carrying.** A nested `<ul>` inside a citation broke two unrelated
    assertions that enumerate `.cites li`, which is the second time markup added inside a list
    item has made a counting selector wrong; they are `.cites > li` now. And the honest limit of
    the third direction: it is a name scan of one module, not dataflow — which is why the smoke
    asserts the rendered card and not the scan.

49. **The gate that found the last three faults says in its own docstring that it does not cover
    three documents, and both of the sentences it was not watching had never reached anybody.**
    `sidecar_shape` has read that way since § 29: the set is taken from each scene's `index.json`
    "because the other derived documents — `exclusions.json`, `terrain.json` — have their own
    readers and their own shapes". True, and for a fortnight it also meant that the interface
    where § 28, § 29 and § 30 each found a fault was guarded for one document out of four.
    `check_derived_contract` covers the other three — the per-scene `terrain.json` and
    `exclusions.json` and the repository-level `liberties.json` — in both directions, and it
    reported two on its first run. **Fifth check in this family to find something immediately.**
    **`terrain.json` states its own extent and the panel never asked.** *"The forks quadrant: the
    Chicago River main stem, North Branch and South Branch meeting at the datum origin at Wolf
    Point, and the three divisions of land they separate."* The Evidence panel's twenty ground
    claims describe a 640 m box and say nothing about the town east of it — which is precisely
    the question a visitor has after § S7's free-fly, having watched the ground end from 150 m
    up. Compiled into every terrain sidecar, read by no renderer, for the life of the project.
    It is the first line of that section now, before the caveat, because it is the frame every
    claim under it is read inside.
    **`liberties.json` carries its own account of what a liberty is, and the panel typed a
    paraphrase of it instead.** The derived `note` — *"The confidence model covers attributes.
    These are the decisions that live above any single attribute: scope, omission,
    simplification, and the choices a visitor would otherwise have to reverse-engineer"* — was
    compiled and rendered nowhere, while `index.html` opened the section with *"The chips above
    cover attributes. These are the decisions that belong to no single attribute…"*, hand-written
    and held to the document by nothing. That is § 36's fault one surface over: a restatement
    with no mechanism holding it to the half it restates, and the two are free to drift the day
    `docs/LIBERTIES.md` is edited. The paraphrase is deleted and the document's sentence renders
    in its place; the smoke pins it **verbatim against the fetched document** and asserts the
    panel states it **once**, so the typed copy cannot come back beside it.
    **The design decision worth carrying is that the binding is DECLARED.** A per-structure
    sidecar names itself — `record.sidecar` is an anchor a regex can follow, which is what
    § 29's scanner does. These three are fetched into a local `doc` and then handed entry by
    entry to a renderer, so the field name is chosen against a function parameter with nothing
    left to anchor on — the very limit § 29 stated and refused to widen. `DERIVED_DOCUMENTS`
    therefore writes the binding down (`claim` is an element of `claims`, `ex` of `excluded`)
    and the gate holds the module to it in both directions: a declared root reading a field no
    committed copy carries fails, and a root bound where the document has nothing fails too,
    because a claim about a module that cannot be checked is the state this family exists to end.
    **The `internal` half is § 48's partition arriving at a second family.** The bounded set
    there was the source schema; here it is what the compiler emits, which `--check` already
    proves is what the dataset derives to. Twelve fields are declared internal with their
    one-line reason — the scene id a file was fetched by, `claims.sources` before `cite()` joins
    it, `not_modelled.dossier_zone`, the liberties file's do-not-hand-edit banner — and the
    declaration is checked the other way as well: a field declared internal that the module does
    read fails, and so does a declaration outliving the field it describes.
    **Citation leaves are deliberately deferred to `check_source_surface`.** One compiled
    citation shape reaches all three documents, and giving a field two owners is giving it two
    answers the day they disagree.
    **The honest limit, and it is the same one § 28 was written about: this proves a module
    NAMES the field, not that the field reaches a pixel.** `exclusions.json`'s `standard` and
    `uncertain_standard` are read into `mountExclusions`'s return value and rendered by nobody,
    while `index.html` carries hand-written restatements of both — exactly the fault repaired
    above for the liberties, still standing two sections down, and the scan is satisfied because
    the name appears. That is why the smoke asserts the rendered text for the two claims this
    slice ships, and it is queued rather than quietly left: the same repair, the same shape.
    **Data and meshes untouched; nothing was re-baked.** No record value moved, no confidence
    changed, no sidecar changed — `scope` and `note` were already being compiled.

50. **The two the gate above named as its own limit are repaired, and one of the paraphrases had
    already started counting.** § 49 ends by naming `exclusions.json`'s `standard` and
    `uncertain_standard` as the standing example of a read that is a name rather than a render —
    compiled since those sections shipped, taken into `mountExclusions`'s return value, rendered
    by nobody, and restated by hand in `index.html` two sections below the identical repair the
    same slice had just made for the liberties. Both are mounted now: `standardMount` and
    `uncertainStandardMount`, the compiled sentence verbatim and first, the typed paraphrases
    deleted.
    **The open-questions paraphrase is the one worth recording, because it was not merely a
    restatement — it was arithmetic.** *"Three of these are empty ground … and the fourth is
    standing in front of you"* is true of the four entries committed today and false the day a
    fifth watch-list question is written, which is the same class of failure as any hand-typed
    number in this project and has no gate that could hold it: `check_watch_list` enforces what
    an entry must carry and nothing anywhere reads a sentence in `index.html` for a count. The
    compiled sentence — *"They are the third category, and one of them is standing in front of
    you"* — counts nothing, and the smoke now asserts that the phrase "Three of these" is not on
    the panel, so the arithmetic cannot come back.
    **What was kept beside each is only what the derived document does not say**, which is the
    line this repair had to draw and did not have to draw for the liberties. The not-here
    section keeps how to read its two kinds of entry — a *not until* chip is a building dated
    after the scene, no chip at all is one already gone — because that is a fact about the
    RENDERING (`exclusionEntryHtml` decides it) rather than about the dataset, and putting it in
    the compiler would be authoring renderer prose into `compile_scene.py`. The open-questions
    section keeps why a standing building is filed here rather than above. Everything that
    restated the compiled claim is gone.
    **Verbatim, once, and not busy — the same three assertions § 49 wrote for the liberties
    note**, against `window.__chicago4d.exclusions.standard` / `.uncertainStandard` rather than
    a phrase copied into the test, because the failure being pinned is the sentence in the
    repository disagreeing with the sentence on the screen. The two older assertions on this
    panel (*"not a list of everything missing"*, *"standing in front of you"*) kept passing
    through the swap without being touched, which is worth stating: both phrases are in the
    compiled sentences too, so they were never the thing holding the paraphrases in place.
    **What did NOT change is the gate.** `check_derived_contract` still cannot tell a read from
    a render and no widening was attempted — the scan cannot follow a value into a function, the
    limit § 29 stated and refused to widen, and § 49 restated. Its comment in `validate.py` said
    these two fields were the live example; it now says they were, and that the limit is
    unmoved. The next such field will be found by a person reading a module, exactly as this one
    was.
    **Data and meshes untouched; nothing was re-baked.** No record, no confidence, no sidecar
    and no GLB moved — both sentences were already being compiled. Smoke 233 checks green at
    390×780 and 1280×800.

51. **The sixth warning's page had never been opened, and the page has no citations in it at
    all.** The evidence ladder has counted six `documented` values resting on later scholarship
    alone since 2026-08-10. Five were read across § 43-47. The sixth — ground
    `surface_materials.south_division`, the soil profile of the South Division, `documented` on
    `chicago_architecture_history_115` alone — was the one `docs/ROADMAP.md` § S5 kept saying
    *has not been opened*, and the record itself said so in as many words: *"Not re-fetched at
    its locator by this parcel."* Everything this project knew about that page came from a
    quotation inside its own dossier. Memo: `docs/RESEARCH/surface_materials_south_division.md`.
    **The page is correctly tiered and the VALUE is over-graded** — the same verdict § 46
    reached on ground `water`, and now the verdict on all six. It is a 2022 essay by an
    architect-historian, so it IS its own document and the transcription rule does not reach it
    (`date` is the article's publication date, not a retrieval); tier 4 is right and nothing
    lifts it. What the reading adds is a limit that had been an inference: the old note said the
    page *"gives no citation for the two-to-three-feet figure"*, read off the dossier and true of
    one figure. **The article carries no footnote, endnote or numbered reference anywhere** —
    zero `<sup>`, one outbound link in the body and it is the author's own email — and its entire
    apparatus is a closing *Further reading* line naming Andreas. Established from the page, in
    two copies: the live URL and the Internet Archive capture of 2025-12-06, agreeing on every
    quoted passage and on the same absent apparatus.
    **The one document on the page is quoted and not named, and it settles a third of the
    claim.** Three paragraphs on, the author stops summarising and block-quotes **John Mills Van
    Osdel**, named there as Chicago's first architect, on the ground he built in: sand that
    *"could not pass downward into the clay, nor laterally"*, and *"a majority of the earlier
    frame buildings rested on posts sunk through the quicksand to the clay"*. That is a witness,
    and the dossier does not mention him — the one document on the page is the one thing the
    research did not carry off it. He attests the ORDER of the strata and the drainage failure.
    **He gives no black loam and not one thickness**, so the three figures in
    `black_loam_over_quicksand_over_blue_clay` — a foot, three to four feet, eight to twelve feet
    — are the 2022 author's alone. And the quotation carries no publication, no date and no page,
    which is exactly why the record declares no `transcribes`: that field's rung is a judgement
    about a named, dated document, and the page names none. Running the Van Osdel original down
    would buy a rung; the memo says where to start and admits the starting point is a guess.
    **The regrade is queued, not taken, and the reason is mechanical.** `documented` → `inferred`
    is right and cannot land here: `generators/terrain_inputs.py` deliberately does not strip
    `confidence`, so the word re-stales the committed ground GLB and `check.sh` fails until a
    Blender bake lands with it — and there is no Blender on the improve runner. It joins ground
    `water` and the four `drloih` values in the one bake slice. The validator still counts six,
    which is the enforcement; nothing in this slice can satisfy it.
    **What ships instead is the finding where the grade is read.** `note` IS stripped from the
    terrain hash — the whole point of § 34 — so the block now carries the partition above in the
    Evidence panel's *The ground you are standing on*, under a chip that is still stronger than
    the sentence beneath it. That is uncomfortable and it is the honest intermediate state; the
    alternative is a visitor reading `documented` with nothing beside it until the bake. The
    smoke pins it verbatim against the compiled claim rather than a phrase copied into the test,
    and pins the discriminating pair: the OTHER `documented` soil claim — the marsh, on
    `chicagology_prefire273` — is correctly graded and carries no such correction, so a panel
    stamping this disclosure on every documented claim fails.
    **Two smaller repairs, and the first is a hole in this project's own standard.**
    `archived_url` was a Wayback **wildcard search URL** (`/web/20240416000000*/`), which resolves
    to a calendar of captures rather than to a capture — not a citation that can be re-read,
    which is the standard the field exists to enforce. Nothing checks what an `archived_url`
    resolves TO, so it passed every run since it was written; it was the only one of its kind in
    `data/sources/`, and it is a dated capture now. And `verified` was `false` and is `true`.
    **Third dossier correction found by opening a page rather than by a check.**
    `docs/research/01-terrain-hydrology.md`'s surface-material table tags the profile
    **documented (§1.15)**, and that row is the direct ancestor of the grade in the spec — made
    without opening the page. `north_branch_bridge` § 6 and `hogan_store` § 3 were the first two,
    and the lesson has been the same each time: a table row is a finding aid and a finding aid is
    not the page. The dossiers are committed verbatim and are not edited, so the correction lives
    in the memo and the operative half of it in the spec's own note.
    **Data untouched below the prose, and no mesh is stale.** No confidence moved, no figure
    moved, no GLB was re-baked; the terrain sidecar changed because a note and a source record
    changed. Smoke green at 390×780 and 1280×800.

52. **The E-W streets are measured, and the thing that could read them is a test the tool did
    not have.** § 42 measured eight platted corridors off the two 1834 sheets and settled the
    module, and it threw half of the reading away: a N-S traverse along Canal reads *lot lines*
    on the Wright sheet, and every test that separates a lot line from a street on Hathaway
    passes them there. Lot depths are 20-26 m, which is a platted street's width; the bounding
    lines run as far as a block face does; two spacings land in the module band by coincidence.
    The memo said what the next attempt would need — a method that identifies a corridor by
    something other than its width — and this is it. **All three failed tests are readings taken
    ACROSS a candidate at one place.** The new one turns ninety degrees: a street corridor is
    open ground from one cross street to the next, because the block faces bounding it stop at
    the kerb, and a strip of lots is crossed by a lot line every few metres and ends at the
    block face. `clear_run` follows a candidate's own centreline 350 m each way and reports the
    longest unbroken run of paper.
    **The threshold is derived rather than chosen**, which is the whole difference between this
    and tuning a filter until the answer looks right: the shortest block face the module band
    allows is its loosest pitch less its widest street, 95 − 30 = 65 m. Move the band and it
    moves. **The separation is not marginal** — the three corridors kept run 213-287 m clear,
    the ten rejected 42-61 m, no overlap and a factor of 3.5 — **and it costs nothing on the
    readings already committed**, rejecting none of the eight N-S corridors, which run 201-677 m.
    **Three E-W corridors, all on Wright: Lake at 79.4 ft, Randolph at 81.5 ft, and one a block
    further south at 86.5 ft.** Eleven corridors now, median 83.7 ft, and the module no longer
    rests on one axis of the grid.
    **The names are measured too.** A corridor takes a street's name only when that street's
    committed modern junction(s), projected onto the traverse through the sheet's own affine,
    land within half the module's loosest pitch of its centreline. Lake and Randolph come in at
    0.9 m each. The third corridor is Washington Street by the plat's order and stays UNNAMED in
    the data, because no junction for it is committed — the inference is in the memo where a
    reader can see it. `check_street_module` re-derives every identification offline on every
    commit, and the first thing that gate did was catch this tool projecting offsets in pixels
    scaled by an average on sheets that are anisotropically stretched; the ground figure and the
    pixel figure disagreed by 1-2 m and the tool was wrong, not the gate.
    **And it answers the question § 42's control-point finding said it could not.** That finding
    priced a correction *across* Canal Street and recorded, as a limit, that whether G5 sits at
    the right northing was untouched. The traverse that crosses Lake can see exactly that:
    **G5 lies 3.4 m south of the Lake Street corridor's centreline**, so the 20.2 m correction
    really is one coordinate and not two. That was an assumption and is now a reading.
    **What it does not settle, which is the interesting half.** Hathaway's N-S traverse commits
    nothing — no two of its candidates are a block pitch apart — so the E-W widths rest on ONE
    sheet and are not cross-checked. Fixing that exposed a real fault: with a single surviving
    candidate the chain search used to keep it for having been found first, and a chain of one
    is not a chain. Hathaway's Canal corridor also stops being nameable, at 50.1 m against a
    47.5 m tolerance — not a second opinion about the control point but the same 52 m from the
    other side. The E-W spacings are 134-136 m against 117-123 m between the N-S streets, so the
    blocks are not square and a 300 ft block plus a street does not describe them; that is a
    finding for S9's block dimensions and is deliberately not turned into a figure off two
    spacings on one sheet. South Water and Market are still unmeasured.
    **Data and meshes untouched; nothing was re-baked.** No structure record, no confidence, no
    sidecar and no GLB moved — the corridors are traced evidence, like the shoreline, and the
    ground does not read them. Six new checks in `tools/test_validate.py`. Smoke green at
    390×780 and 1280×800.


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

**The evidence-ladder queue, as it stands after § 51, and the READING half of it is finished.**
Six `documented` values still rest on later scholarship alone and the validator counts them every
run — but every one of the six has now been read, and the verdict on all six is the same: the
sources are tiered correctly and the values are graded too high. Ground `water` (§ 46) and ground
`surface_materials.south_division` (§ 51) are both settled as over-graded VALUES waiting only on
the Blender bake a confidence change costs; the other four are the `drloih` values that
re-tiering cannot save and that land with the same bake. **All six are one slice on a runner with
Blender**, and none of it is research any more.
**The undeclared-page queue is down to those same two `drloih` pages** (§ 47): every
other page that dates its own retrieval now declares either the document it carries or the
reading that established it carries none. So what is left of this thread is not research any
more — it is one regrade slice on a runner that has Blender, taking five values down together
with the bake they stale. None of it blocks S5 additions.

**S9 — streets, roads and paths**, queued behind S2e at Kevin's direction. Geometry generated from the Thompson module rather than traced; surface is unpaved earth with plank walks, NOT a graded roadway; elevations drape on the heightfield because nothing was graded until 1855-58. See ROADMAP § S9 for why each of those is a trap. **The method problem it named is solved** (§ 52): the E-W streets can be read now, and Lake and Randolph are. What that parcel still wants from the sheets is the plat's **block dimensions and extent** — and the first measurement of the N-S spacing, 134-136 m against 117-123 m the other way, says the blocks are not square and that the 300 ft block the N-S streets fit does not describe them.

**S5a — Fort Dearborn**, the next building. Its position is settled (E +1152, N +221, cross-checked to 35 m) and the coastline gate Kevin named is cleared. **What the fort was on 1835-07-01 is settled too, 2026-08-10** — an occupied Army post under Major John Greene (§ 31, `docs/RESEARCH/fort_dearborn.md`). **The FOOTPRINT still has no source**: neither 1834 sheet draws a plan, and no dimension of the 1816 stockade survives in anything read. The next move on this parcel is not modelling and not more reading around it — it is one document, the **Fort-Dearborn Addition plat of 1839**, whose withheld lots are the surveyed envelope of the ground "within the pickets". Behind that, the ground itself: the fort site is 800 m beyond the modelled terrain box, so S2e comes first either way.

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
