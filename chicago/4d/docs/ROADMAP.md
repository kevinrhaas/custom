# ROADMAP

The build order and the work parcels. `docs/PLAN.md` carries the full reasoning; this is the
operational view — what to pick up next, and what it depends on.

```
S0 scaffold ─┬─► S1 georeference + datum ──► S2 terrain e1834 ──► S3 M0 Sauganash walkable
   [DONE]     │        [DONE]
              ├─► R1 renderer shell (synthetic geometry) ────────┘
              ├─► P1 research dossiers (read-only) ──► S5 structure records ──► S8 M1
              └─► S4 archetype generators (golden params) ──────► S5 bakes
S2 ──► S6 flora + fauna ──► S7 polish, audio, perf ──► release sweep
```

**Critical path: S1 → S2 → S3.** The datum gates every coordinate in the project. Work that does
not need coordinates is deliberately structured to proceed in parallel.

---

## S1 — Georeference and verify the datum · **DONE 2026-08-09**

Origin: E 447072.7, N 4637395.8 (EPSG:26916) = 41.886721, -87.637951 — the Wright-drawn forks,
eight-GCP fit RMS 17.5 m, cross-checked against an independent Hathaway georeference (57.9 m)
and the modern OSM junction (39.4 m). The published Allmaps 3-point transform was measured
(RMS 25.9 m against independent control) and superseded; no annotation existed for the LOC
Hathaway, so that georeference is new work. Memo: `docs/RESEARCH/datum_derivation.md`;
enforcement: `tools/rederive_datum.py` in `check.sh`. Carry-forward: ±20 m working uncertainty
for anything traced from the 1834 sheets; generate street geometry analytically from plat
dimensions (Hathaway annotates them) and snap to control rather than tracing pixels.

## S2 — Terrain, epoch `e1834_harbor_cut`

### S2e — extend the ground EAST to the lake · **IN PROGRESS — parcel (a) DONE 2026-08-10**

Promoted above the rest of S2 because the free-fly camera made the gap impossible to
miss from the air: **the modelled ground stops 800 m short of Fort Dearborn and about a
kilometre short of Lake Michigan.**

The numbers, measured against `data/datum.json` rather than estimated:

| | local E | inside the box? |
|---|---|---|
| current terrain box | −320 … **+320** | — |
| Lake St & State St | +842 | no |
| **Fort Dearborn site** (Michigan Ave bridge) | **+1127** | no, 3.5× beyond the edge |
| modern lakefront at the river mouth | +2155 | no |

(Landmark positions are modern-successor scoping figures, not dataset claims — they say
how far the box falls short, nothing about 1835.)

**The shoreline is the interesting part, and it is a provenance problem, not a modelling
one.** The 1835 lake edge is nowhere near the modern one: everything east of roughly
Michigan Avenue is landfill, much of it fire debris after 1871. Drawing today's coast
would be the single largest false claim in the dataset. The shore has to come off Wright
1834 — which also carries the 1834 harbour cut, the two piers, the sand tongue and the
decaying old southward channel — with the same ±20 m carried forward as everything else
traced from those sheets. This is precisely the case the year-parameterized architecture
exists for: `docs/EPOCHS.md` treats terrain as versioned per epoch, so a later year gets
its own shoreline rather than editing this one.

Scope, roughly: extend to about E +1500, giving a ~1.9 km × 0.7 km field. At the current
2.5 m cell that is ~213k samples (~425 KB int16) against today's 66k (132 KB) — well
inside the 25 MB publish budget, but worth considering a coarser cell east of the built
blocks, where the evidence does not support 2.5 m detail anyway.

Unblocks the **Fort Dearborn** and **Harbor works** parcels in S5, which cannot be placed
onto ground that does not exist. It also retires the aerial view's worst artefact: from
150 m up you currently see the ground simply end.

Parcels (parallel once S1 lands):

- **(a) Shoreline + river vectors** — **DONE 2026-08-10.** `tools/trace_shoreline.py` →
  `data/terrain/epochs/e1834_harbor_cut/shoreline.geojson`: the main stem from the box edge
  east, the 1834 cut between its piers, the old southward channel, the **sand bar as an
  island** (the water polygon's interior ring), and the mainland lake shore — 2 466 m of south
  shore, 1 568 m of north shore, a 1.5 km bar perimeter, all off the same Wright 1834 sheet
  through the same affine, ±20 m. Memo: `docs/RESEARCH/shoreline_harbor_1834.md`. Two boundary
  runs were found and dropped on purpose: the outer edge of the lake wash is where the
  draughtsman stopped washing, not a coast. **Measured, which changes the box:** the mainland
  shore reaches E +1257 and the bar's east edge E +1497, so the proposed +1500 clips the bar by
  3 m — **use E +1560**, inside the traced window's +1570. The two windows overlap by 80 m and
  agree there to 0.1–5.7 m, which is the check that the segmentation is reading the map rather
  than its own parameters. Not yet consumed by `terrain_gen.py`; it is the evidence, not the
  ground.
- **(b) Heightfield** — the 30-zone table in `docs/research/01-terrain-hydrology.md`, quantized ≤0.25 ft at 5–10 ft cells. Z=0 at the 1835 lake surface. **Next slice**, and it needs a bake for the ground GLB, so record + mesh land together. Two things parcel (a) hands it: the bar is *land inside water*, so the signed-distance rule that builds the forks ground has to understand islands, not only banks; and no elevation for the bar exists in any source, so its height is a spec argument to be made in the open, not a number to pick.
- **(c) Hydrology** — the slough (public-square pond → past Lake & Dearborn → river at the foot of State), Frog Pond at Lake & LaSalle, the Wells Street marsh, the marshy river-shore strip.
- **(d) `terrain_gen.py`** — spec + vectors → terrain mesh + `heightfield.bin` for collision.

Reminder: piers and bridges are **structures with phases**, not terrain (see `docs/EPOCHS.md`).

## R1 — Renderer shell · *can start now, needs no datum*

Parcels: (a) shell + input-intent layer + walker; (b) confidence shader + provenance popup
against a hand-written test sidecar; (c) `tools/smoke.mjs`.

Build against synthetic geometry and flat ground. Contract in `docs/PLAN.md`. Mobile
(390×780) is a release gate from the first walkable commit — retrofitting touch into a 3D
walkthrough later is the expensive way to do it.

## S3 — Milestone 0: the Sauganash, end to end

Definition of done in `docs/PLAN.md`. The record, the sources, and the dossier are already
written; what remains is the `frame_tavern` archetype, the first bake, and the walkable page
with a working confidence toggle.

Success is not "a building appears". Success is that a viewer can toggle the confidence view
and see exactly which parts of the Sauganash we can defend — the white two-story block and the
blue shutters solid, the invented footprint and the disputed gallery dithered.

## S4 — Archetype generators

One parcel per archetype, each with a golden-parameter GLB and a reference shot:

`frame_tavern` · `frame_storefront` · `frame_dwelling` · `log_dwelling` · `institutional` ·
`fort_structure` · `outbuilding` · `plank_walk` · `bridge_timber` · `pier_crib` · `palisade`

Balloon-frame logic (stud spacing, sheathing, proportions) is a first-class requirement, not a
detail: 1833–35 Chicago is where balloon framing was invented, and it is the first thing a
knowledgeable viewer checks.

## S5 — Structure records

**Queued first, and it is a repair, not an addition: three attributes that are recorded and
unbuilt.** Found by the omission gate on 2026-08-10 and admitted meanwhile by L20 and L21.

| record | attribute | what the archetype reads | effect |
|---|---|---|---|
| ~~`wolf_point_tavern`~~ | ~~`frame_extension`~~ | `frame_addition` | **DONE 2026-08-10** — renamed, dimensioned and re-baked in one slice |
| ~~`wolf_point_tavern`~~ | ~~`signage`~~ | `sign` | **DONE 2026-08-10** — the board hangs on the river front; the wolf is not drawn (L25) |
| ~~`miller_house`~~ | ~~`chimneys: 2`~~ | `chimney` (a boolean) | **DONE 2026-08-10** — the count is a parameter of both archetypes; the second stack stands on the frame range |

**The one repair found by reading rather than by a gate is DONE** (2026-08-10, STATUS § 23 → § 24):

| record | attribute | what the evidence says | effect |
|---|---|---|---|
| ~~`north_branch_bridge`~~ | ~~`pier_spacing_m`~~ (15 cribs at the archetype default) | **two "bents" of four heavy logs resting on the bottom** | **DONE** — `pier_count: 2` replaces the spacing in record and archetype; L29 resolved, L31 new |
| ~~`north_branch_bridge`~~ | ~~`pier_kind: crib`~~ | the settlers' own word is **bents** — and Cleaver signed it | **DONE** — `bent` beside `crib` and `pile`; four heavy logs under a cap |
| ~~`north_branch_bridge`~~ | ~~`clearance_m`~~ (`inferred`, page not found) | **"about six feet above the water, so that teams passed under them on the ice freely"** | **DONE** — `documented` on `old_settlers_bridges_1883`; the deck and stringers come out of dithering |
| ~~`north_branch_bridge`~~ | ~~deck~~ (archetype's, unstated) | **"puncheons or split logs were laid for a floor"** | **DONE** — `deck_kind: puncheon`, a value the generator reads |

All four were mesh inputs, so the record, the archetype change and the bake landed as one slice —
the same coupling the note below describes, arriving from a new direction. The evidence is a
signed 1883 statement by four men who used the bridge, printed as a footnote at Andreas
pp. 631-632 and missed by the full-text index; see `docs/RESEARCH/north_branch_bridge.md` § 6.

**The lesson is about the parameter, not the number.** `bridge_timber` divided a span by a
spacing, so it could only ever produce a colonnade; no source will ever state a spacing, and what
a witness remembers is a count and a form. Setting 4.5 m to 23.94 m would have fixed this bridge
and left the next one to be found by the same accident. Worth asking of any archetype whose
defaults are about to be overridden: is it asking for the kind of number a source could contain?
What the repair could not settle is where along the span the two bents stood — the letter locates
them by depth, in a river whose bed this project does not model — so they sit at the third points
and **L31** admits it, together with the splices in three 23.9 m stringer runs that no source
places.

Each of the earlier repairs was a small data edit plus a re-bake, so **record and geometry landed in one slice** — the
same coupling the note below describes. All three are done.

**The list refills itself, which is the point of the gate.** Making the chimney count real
required placing Miller's second stack, and placing it exposed the next repair of exactly the
same kind:

| record | attribute | what the archetype does | effect |
|---|---|---|---|
| ~~`miller_house`~~ | ~~`frame_addition` (documented, undimensioned)~~ | picks side, width, depth and storey count from its defaults | **DONE 2026-08-10** — the record states all five, the two invented ones are L27, re-baked in the slice |

That was L24's defect one building over, and it came with a second one underneath it that was
not on any list. **`stories: 2, documented` was the frame range's and `log_dwelling` reads it as
the log core's**, so the documented claim was spent on the cabin, the range took a 4.7 m default,
and the model stood a two-storey log cabin behind a shorter frame block — the composition
inverted. The record now separates them: `frame_addition_stories: 2` documented, `stories: 1`
inferred for the cabin, `frame_addition_height_m: 5.2` and `wall_height_m: 2.6`. Two of the four
queued attributes turned out to be attested rather than invented — the side, because the source
says *fronting the river*, and the storey count — and only the width and depth are guesses, taken
off the record's own footprint limb (9 × 6 m) rather than picked afresh. L13 moves to Resolved,
L27 is new. **The repair queue is empty and nothing refilled it: S5 is additions again.**

The lesson worth carrying past this table: the omission gate found three misspellings and the
fourth fault was not one. `stories` was a name the archetype *found* and read as being about the
other half of a two-part building — which is invisible to a spelling check and to
`test_consumed_attributes_actually_reach_the_parameters`, since the value does move geometry,
just the wrong geometry. Any archetype attribute that means different things to different
elements of a composite building is the same trap; `wall_height_m` was the second one in this
record.

**The Wolf Point pair landed together, which is the shape** (2026-08-10). Both renames, the four
attributes the frame bay needed, the re-bake, the publish and the liberties moved in one PR. Two
things are worth carrying forward. First, a rename is never only a rename: `frame_addition: true`
alone would have let the archetype choose the bay's side, width, depth and storey count from its
defaults, so a documented feature would have arrived at an invented size with nothing admitting
it — the record now states all four and L24 admits the three that are conjectural. Second, the
staleness gate did exactly what it was written for: the record edit turned the tavern's GLB STALE
on the spot and the commit could not go green until the bake landed with it.

**And the count of a thing is not the thing** (2026-08-10). `chimneys` was stated by every record
and read by neither archetype: `frame_tavern` built two stacks and `log_dwelling` built one,
whatever the number said. Both take the count now, and the frame pair keeps its exact positions so
that parameterising a number did not move a building whose count was already right. The
`log_dwelling` half was the `frame_extension`/`signage` failure a third time — the parameter was
`chimney` and no record has ever contained that word — so the class has a check now rather than
another discoverer: `test_consumed_attributes_actually_reach_the_parameters` perturbs every stated
value an archetype declares it consumes and requires the resolved parameters to change. What the
count still does not carry is where a stack stood, how big it was or what it was made of; nothing
in the dataset records that for any building, and L26 is where it is admitted.

**You cannot land half of one any more** (2026-08-10). `check.sh` recomputes each committed GLB's
inputs and fails when the record and the mesh disagree. The working shape: prepare the record on
a branch, let the bake workflow run against that branch (it triggers on any push under
`chicago/4d/data/**` or `generators/**`), take its baked assets onto the same branch, and merge
one PR carrying both. See `generators/mesh_inputs.py` for what counts as an input and what
deliberately does not.

**The first bridge landed 2026-08-10, and it is the first record whose size is evidence.** The
North Branch crossing at Kinzie Street — Chicago's first bridge, 1832-1839 — is a record, a bake
and a published mesh on the `bridge_timber` archetype, which had been written and never used.
Three things worth carrying into the rest of S5:

- **A crossing can be measured where a building cannot.** Its 71.83 m span is the distance
  between the two traced 1834 waterlines along the Kinzie alignment, read off `river.geojson`,
  and its 3.048 m width is Cleaver's "ten feet wide" — so the footprint is derived rather than a
  placeholder. Anything that meets the traced water (the piers, the wharves, the raft bridge) can
  be dimensioned the same way. Anything that does not still gets a placeholder.
- **The invention moved from the outline to the interior.** A building's placeholder is its
  footprint; this bridge's is the fifteen cribs the archetype puts under a span nobody described
  the middle of (L29). Same class of fault, different place to look for it.
- **The contract's water anchor is implemented now** — `VERTICAL_ANCHOR` on the archetype,
  `placement.vertical_anchor` in the sidecar, a literal `y = 0` in the renderer, and a smoke
  assertion written as the difference between the two anchors. The next structure over water
  needs no renderer work. **What is still missing is walking on it**: the walker follows the
  terrain, so the deck is scenery. That is its own unit and it is recorded in STATUS, not faked.

**The first building whose footprint is evidence landed 2026-08-10**, and it is an ADDITION
rather than a repair — the first since the queue emptied. `hogan_store`, the log store at the
west end of the Lake Street block where the United States opened a post office at Chicago on
31 March 1831, carries a `documented` footprint: Andreas states its size twice, twenty by
forty-five feet, both times as an aside about how little room the town's mail needed. Three
things worth carrying into the rest of S5:

- **A building can be measured after all, when the source is describing something else.** The
  bridge's numbers came from a witness describing the bridge. This one's came from a writer
  making a point about the *post office's* cramped quarters. Dimensions in this literature hide
  inside arguments about something other than the building, so search the prose around an
  institution rather than the entry for a structure.
- **Reading a page corrected the dossier's chronology by twenty months.** `docs/research/`
  § 4 dated the post office's move to Franklin and South Water from the day Hogan became
  postmaster (2 Nov 1832); Andreas says twice it moved about July 1834. The dossier's summary
  tables are finding aids, and a table row is not the page. See `docs/RESEARCH/hogan_store.md`
  § 3.
- **The first record with nothing conjectural in it.** Its gaps are gaps in the sources'
  precision rather than filled holes, so it needs no liberty — which finally exercises the
  provenance popup's empty "What we made up here" state that STATUS § 11 recorded as unexercised
  by real data. Its weak point is instead its **survival**: attested to about July 1834 and
  placed in a scene eleven months later on a continuity argument, stated as such on the record.

Per-cluster parcels, each one file per structure so parallel agents never collide:

| parcel | contents |
|---|---|
| Wolf Point west bank | Wolf Tavern (painted wolf sign), Green Tree, Western Hotel, James Kinzie house, R. A. Kinzie store |
| North bank | Miller House, Miller tannery, Cobweb Castle, Walker's meeting house, Steamboat Hotel, Lake House (under construction) |
| South Water blocks A–G | the block-by-block sketch in `docs/research/04-structures-south.md` is the work order. ~~Hogan's store / the first post office, Lake at South Water~~ **DONE 2026-08-10**. Next on this block: Philo Carpenter's log drug store, "immediately adjacent to the Sauganash's public bar", which has no dimensions at all; and the **Franklin Street post office**, the building actually holding the mail on the scene date, of which nothing but a street junction is attested — see `docs/RESEARCH/hogan_store.md` § 4 before building it |
| Lake Street | Tremont House I, Mansion House, Exchange Coffee House, St. Mary's, First Presbyterian, Thomas Church store |
| Civic square | estray pen, log jail, courthouse (under construction, month unfixed) |
| Fort Dearborn | palisade, blockhouse, bastion, magazine, quarters, barracks, sutler, hospital, parade, gardens |
| Harbor works | north pier, south pier, the cut, the lighthouse, wharves |
| Crossings | ~~North Branch bridge~~ **DONE 2026-08-10** · South Branch raft bridge (floating — needs its own archetype, see `bridge_timber_params`) · Dearborn Street drawbridge (200 ft with a 60-ft draw, a different animal and outside the current terrain box) |

## S6 — Flora and fauna

Per-zone parcels from the dossiers: 10 flora zones, 7 fauna zones. Honor the July phenology
rules — big bluestem is vegetative in July, cordgrass is the tall flowering element, ramps are
leafless scapes. Negative findings (no ring-billed gulls, no beaver, no periodical cicadas) go
into the data as `absent` entries with citations, so nobody re-adds them later.

## S7 — Polish

Performance against the budgets, licensed ambience audio, provenance-popup UX, `LIBERTIES.md`
completeness pass, mobile release gate.

**Done 2026-08-10 — free-fly, and the town seen whole.** `F` (or the ▲ chip) lifts the visitor
off the prairie; `Space`/`Q` and a touch pad rise and descend; the `from_above` anchor arrives
already in the air. Forward follows the look direction and strafe stays level; horizontal speed
scales with altitude, capped, because at 300 m a walking pace reads as not moving. Terrain
remains a floor — the step-up rule and the footprint capsule are deliberately *not* applied,
since they are exactly what you asked to leave. Leaving free-fly snaps to the ground rather
than descending: the walk path's ground-smoothing is exponential at 14/s, which from 175 m is a
150 m/s plummet followed by a crawl.

Worth knowing for whoever takes the next slice: **the aerial view is the most honest picture of
how little is built.** Six structures across a 640 m box, and the edge of the modelled ground is
visible from about 150 m up. That is L17 working as intended, not a bug to hide — but it makes
S5 (more structures) the obvious next unit, and it argues for an eventual haze/extent treatment
rather than a bigger skirt.

**Done 2026-08-10 — the liberties are in the walkthrough.** `docs/LIBERTIES.md` stays the
append-only source of truth; `tools/compile_liberties.py` derives `data/liberties.json`,
`check.sh` re-derives it and fails on drift, and the Evidence panel lists all eighteen with
their reasoning.

**Done 2026-08-10 — and attached to their buildings.** The provenance popup reads `subjects`
and shows the liberties taken with the building being inspected, under "What we made up here",
between the attribute table and the citations. Panel and card share one entry renderer
(`libertyEntryHtml`) so they cannot drift; the smoke asserts per-building filtering rather than
a count, which is the assertion a popup dumping all eighteen would still have passed.

**Done 2026-08-10 — the document is checked for gaps.** The inverse check runs in
`validate.py` (`check_liberties_coverage`) and therefore in `check.sh`: every phase whose
`footprint` or `position` is `conjectural` must be named by a liberty that is *about that
aspect*, matched against the entry's own prose. Naming the building is deliberately not
sufficient, and the self-test asserts exactly that case. Six inventions in the committed data,
six covered. The Evidence panel states the guarantee, because a promise a visitor cannot read
is not one.

**Done 2026-08-10 — coverage is now asserted, not inferred.** Entries carry a `**Covers:**`
field of `structure_id[.phase_id].aspect` tokens; `compile_liberties.py` parses it, and
`check_liberties_coverage` matches the claims against the records **in both directions** — an
invention with no admission fails, and so does an admission whose value is not conjectural
(exempt under **Resolved**, so evidence is allowed to arrive without breaking the gate). The
keyword match over prose is gone, and the self-test's discriminating case is now an entry that
talks about footprints and placement while claiming nothing. Writing the claims down immediately
found a drift the heuristic was indifferent to: L12 described the Walker meeting house position
as `inferred` months after the record was downgraded to `conjectural`. The chips are in the
Evidence panel and on the provenance card, because a guarantee enforced only in the repository
is the filed confession this whole line of work exists to stop being.

**Done 2026-08-10 — the rule now covers what a building *is*, not only where it stands.** The
`Covers:` vocabulary was `footprint`/`position`; it is now every attested value in a record —
those two, `documented_range`, the structure-level `function` and `occupants`, and `form.<attr>`
for anything under a phase's form, enumerated from the data rather than from a list so a new
archetype attribute is inside the rule the day it appears. The argument is that a conjectural
`roof_type` is not an absence in the model: a gable gets built and the visitor sees a gable, and
a conjectural `gallery: false` is the same claim in the negative — a plain front rendered because
nobody found evidence either way, which reads as the finding. Four inventions were owed an
admission and had none: the Sauganash's 1829 cabin height and roof (L18) and the Green Tree's and
the Western's galleries (L19). Ten conjectural values, ten declarations. The chips read as
attributes — "Sauganash Hotel roof type" — while the token the gate matches keeps its `form.`
prefix.

**Done 2026-08-10 — the hard half: omissions and simplifications are enforced.** The missing
claim turned out to belong to the *generator*, not to the record or the document. Each
`generators/archetypes/*_params.py` now declares `CONSUMED`, the form attributes its `from_phase`
actually reads, and `validate.py` holds every attribute outside that set to a `geometry:`
declaration on the record — `absent` (nothing of it is built), `simplified` (a fixed default
stands in its place) or `record_only` (a rejected reading, which owes nothing). `absent` and
`simplified` need a `Covers:` token exactly as an invention does, checked both ways, and the
popup marks those rows *not built* / *not modelled from this* so the admission reaches a visitor
and not only a reviewer. Twenty-one attributes across six buildings reach no vertex; L9 and L10
now claim theirs, and L20–L23 are new.

Switching it on found a real defect, which is the argument for the rule in one line: **the Wolf
Point Tavern's frame extension and its painted wolf sign are both `documented` and neither is
modelled.** The record spells them `frame_extension` and `signage`; `log_dwelling` reads
`frame_addition` and `sign`; the absent attributes resolved to defaults and nothing complained.
Both were fixed the same day, in one slice with the re-bake — see S5. The standing limit is
unchanged and worth repeating: nothing can catch a liberty taken that nobody noticed taking — but
an attribute recorded and never built is no longer in that category.

**Done 2026-08-10 — and the defect it found is repaired: the wolf sign hangs.** The rule's whole
argument was one building, so here is that building finished. The record's `frame_extension` and
`signage` are now `frame_addition` and `sign`, the names `log_dwelling` reads; the frame bay and
the signboard are baked, published and visible; and the popup's `documented` chips over both now
describe something a visitor can walk up to. The rename alone would have been the smaller half of
the fix. A frame addition with no dimensions recorded takes the archetype's defaults — a two-storey
block across the river front, on a tavern the sources describe as low — so the record states the
bay's side, width, depth and storey count, and L24 admits the three of those that are invented.
The board is deliberately blank: the sign is documented and the painting on it is not (L25).

**Done 2026-08-10 — what is not here, and the file that said so reaching a visitor.** Every
gate above asks whether what we *built* is honest. None of them could reach the structures
this project researched and deliberately did not build: `data/exclusions.json` has held
fourteen of them, with the evidence that dates each one, since the scaffold — and it shipped
nowhere a visitor could read it. The Evidence panel now carries them under **What is not
here**, derived per scene by `compile_scene.py` with citations joined, in the same entry the
liberties use. The panel states, and the smoke asserts, that this is **not** a list of
everything missing: eight of roughly forty researched structures stand, and the aerial view
remains the honest picture of the rest.

Switching it on found the one file where rule 1 was never enforced. Every `source_id` in this
project must resolve in `data/sources/`; nothing read the exclusions file's, so a citation
there could have named a source that never existed. `check_exclusions` now requires a slug id,
a name, a stated reason and a citation that resolves — the committed file passes unchanged,
and the next entry cannot skip it. The date gate also runs backwards now: an entry dating a
building to 1837 is a correct exclusion from 1835 and a wrong one from 1837, which no
comparison against the records can catch, because an excluded structure has no record.

And the sidecars are re-derived on every commit (`compile_scene.py --all --check`, in
`check.sh`). They are committed so the site needs no build step, which only keeps the
walkthrough and the archive together if a record edited without a recompile is a gate failure
rather than a discovery on the deployed site. All eight were byte-identical on the first run.

**Done 2026-08-10 — the staleness gate is a check now, not a sentence.** Every rule above
assumes the shipped mesh is the one the record describes, and nothing was testing that: the
manifest had carried an `inputs_sha256` per asset since the first bake and no code ever
recomputed it. It does now, for buildings and terrain alike, with the recipe living beside the
generators so the writer and the checker cannot drift.

Turning it on meant rewriting what the hash is over, because the old one reported all six
buildings stale for reasons that cannot move a vertex — record prose, and a constant added to a
sibling archetype's parameter module. It now hashes the *resolved* parameters, the derived
properties, the confidence floats and the builder's bytes; parameter-module source is out,
because its entire effect on the mesh is the object it returns. The eight committed hashes were
re-stamped without a bake and the re-stamp is proved rather than asserted: run the new recipe
inside a worktree of the last bake commit and the input documents come out identical, `build.py`
excepted, whose only change is delegating the hash. See STATUS § 15 for the full account and the
limit — this compares inputs, not output, so a hand-edited GLB still passes.

**Done 2026-08-10 — a structure has to reach the ground, and one does not.** The third
honesty gate in the family that began with liberties coverage. The confidence model grades what
a value claims and the geometry declarations grade whether it was built; neither can see a
structure assembled faithfully onto ground that is not under it, because every name resolves and
every value reaches a vertex. Each archetype now declares where it touches the terrain —
`perimeter` at the base of the walls, `ends` at deck height for a crossing — and `validate.py`
measures that outline against the committed heightfield. The tolerance is the walker's 0.35 m
step-up rule rather than a fresh number, because the gate is asking the walker's question.

The six buildings land, worst corner 0.16 m. **The North Branch bridge stands 2.42 m clear of
the ground at both landings and no land in the 640 m box rises to its deck**, so the crossing
touches neither bank. The record declares `ground_contact: approach_not_modelled`, L30 admits
it, and the chip reaches the visitor through the provenance popup. Two follow-ons this leaves
on the table, both real and both bigger than a slice:

- **The approach itself is unattested.** Nothing describes how a person got from the bank onto
  the deck, so the fix is research before it is geometry — the 1834/1835 Wabansia and Kinzie's
  Addition plat is the best candidate, and a sourced clearance would narrow it too, since a
  lower deck needs less approach.
- **Walking the deck** (STATUS § 21) is now measurably blocked rather than merely unbuilt: even
  with surfaces-above-the-ground in the walker, there is nothing to step from. The two are one
  piece of work, in that order.

## S8 — Milestone 1

Wolf Point cluster + South Water block D (LaSalle–Clark). The first test of whether the
archetype approach actually pays for itself.

## Later — the 4D proof

A second scene (1833 or 1830) exercising the epoch machinery, the `pre_fire_v1` crosswalk, and
a Manager row with the changelog cadence running.

---

## Working notes

- `tools/check.sh` before every commit. It takes under a second.
- One coherent unit of work per run.
- Writing subagents each get their own git worktree.
- Update `STATUS.md` in the same commit as the work, and keep it unflattering.
- No model identifiers in repo artifacts.
