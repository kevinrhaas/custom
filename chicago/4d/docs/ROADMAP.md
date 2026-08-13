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

## K — Kevin's punch list of 2026-08-13 · **THE PRIORITY QUEUE — steward, work these first**

Thirteen directions from the project owner, written up as parcels an agent can pick up cold.
Each names its files, its evidence, its gate and its trap. Standing policy for all of them:
**build liberally, grade honestly** — `conjectural` is a legitimate answer and the confidence
view paints it; the two absolute rules (never invent a source, never silently fill a gap) do
not relax. *Avoid circling on historical perfection: do the reasonable best, mark the rest,
move on.* One parcel per run; leave the others for the next tick or for interactive sessions —
check `git log` first so you do not duplicate a parcel already landed.

### K1 — The inferred-residents programme *(the big one; multi-session; carve into districts)*
Chicago went from ~350 people (1833) to ~3,265 (late 1835). Build the POPULATION as a dataset,
then build the buildings it implies. New directory `data/residents/`: one file per HOUSEHOLD,
grouping persons, with per-person fields — name, arrival date (month if knowable), party size,
origin, why they came, period-correct occupation, where they lived, where they worked — and an
accuracy grade using EXACTLY this vocabulary: **`documented`** (named in a source: Andreas is
dense with them — officials, ministers, traders, tavern keepers, the *Democrat*'s advertisers),
**`derived`** (a real person whose details are partly reconstructed), **`inferred`** (a
hypothesised resident filling the town's demonstrable needs — the first barber, the second
blacksmith, the cooper the packing trade requires). NEVER "recommended" — the words are
**inferred residents** and **inferred structures**. Natives who remained belong in the
population where sourced; depiction of people stays out of scope (L1) — this is a DATASET layer
feeding structures. Cross-reference each household to `data/structures/` ids (`lives_at`,
`works_at`); businesses cluster toward the river/streets, residences spread outward as the town
crowds (use the Thompson plat lots, K7). Extend `tools/validate.py` so a resident's source_ids
must resolve and grades are enforced. **The primary goal is buildings**: every inferred
household that needs a dwelling gets an `inferred structure` record on the plat, archetyped,
baked, confidence-graded — this is how the town reaches its true 1835 density. Start with
DOCUMENTED people (mayors-to-be, Ogden, Hubbard, the clergy, every advertiser already in
`chicago_democrat_1833_11_26`), then derive, then infer to fill the count by occupation census.

### K2 — Image-accuracy loops on the landmark buildings
Reference set: `data/sources/assets/prefire_views_kevin_2026_08/` (12 plates; READ ITS README —
the Doric-portico courthouse plate is the 1837+ building and is a NEGATIVE reference). Also
https://chicagology.com/prefire/prefire275/ (source record exists). Loop per building:
render the model's building from the plate's viewpoint, compare, improve, repeat until massing,
roof, fenestration rhythm, chimneys and signboard match. Tier-5 pictorial rule holds: views
drive FORM as `inferred`, never a coordinate or footprint. **Green Tree first** (plate 11 —
two-storey clapboard, end chimneys both gables, even 6/6 bays, hanging corner SIGNBOARD, rear
ell), then the fort group (whitewashed palisade on rising ground), then Sauganash/Wolf Point.

### K3 — Flora pop-in and coverage *(user-visible defect)*
Grass and flowers "appear out of the ground as you walk towards them." `flora.js`: the near
instanced ring materialises with no transition. Fix: grow/fade-in over distance (scale or alpha
ramp on spawn), widen the ring or add hysteresis so churn is invisible, and profile — mobile
390×780 stays a release gate. Also RAISE COVERAGE where it is thin: `river_bank`'s underfill is
already measured (zone says cordgrass 40–55 % cover, `bare_soil_fraction: 0.0`; render shows
bare soil), and the mid-field targets from the prairie sweep stand in § S6a.

### K4 — Facades: weathered wood, not painted clones
The buildings read as freshly painted and identical. Research first, then implement: most 1835
Chicago frame buildings were UNPAINTED weatherboard or whitewashed — paint was expensive; keep
the documented exceptions exactly as documented (Wau-Bun's white Sauganash with bright-blue
shutters). Add material variation per building — board tone jitter, weathering by age of the
phase, board-width irregularity — so no two share a face (extends L22/L23 rather than
repeating them). Log buildings: hewn vs round logs per record. Cite what you can; grade the
rest `inferred` with the economics argument in the note.

### K5 — The town's furniture: fences, yards, wagons, signs, porches, docks
The scene is buildings on bare ground; a working town has STUFF. In order: (a) the
**`enclosure` archetype** — fence line, gateway count, gate width, fence type (picket/rail/
worm) — already the single biggest structural gap: it discharges the estray pen (currently a
roofed shed, wrongly), the Western Hotel wagon yard (L10), Clybourn's stockyard, garden fences
(the Kinzie-view plate shows picket-fenced garden plots and Lombardy poplars — reference for
TREATMENT, the house itself stays excluded); (b) **signboards** on businesses — attested
(the Green Tree plate's hanging sign; the wolf sign documented) — parameter exists in
`frame_storefront`, switch it on per record, lettering stays undrawn (L25); (c) **yard
objects**: wagons/drays (documented mired on Lake St), woodpiles and lumber stacks (Ordinance 9
documents timber, stone, brick, boxes, barrels IN the streets), crates and barrels at the
stores, kitchen gardens (fort garden documented; dooryard gardens inferred), stove pipes on
every frame building (Ordinance 6 — documented, none modelled); (d) **porches** ONLY where
attested or typologically argued — the Kinzie piazza is the attested exemplar; do not blanket
the town; (e) **docks/wharves** at the forwarding houses (attested "with its dock along the
river front"; needs a river-wharf mode of `pier_crib`). Everything invented gets its liberty.

### K6 — The river bulge at Clark Street
The owner reports a bulge in the river at Clark that contradicts the record. Re-examine the
traced 1834 waterline through the central blocks against the Thompson plat block lines and
Wright; the South Water georeference note already shows the Clark end sitting ~78–80 m off
where Dearborn sits 15–19 — likely a tracing artifact from local paper stretch. Re-trace that
reach, regenerate the heightfield (land outside the reach must stay bit-identical — prove it
the way S2e did), re-run the gradient audit.

### K7 — Thompson plat lot lines
Generate block/lot geometry analytically from the plat module (80-ft streets, documented lot
widths), snapped to the datum — the S1 carry-forward note already prescribes exactly this.
Commit as `data/traces/vectors/thompson_lots.json`. It becomes the placement grid for K1's
inferred structures and the check on every "corner of X and Y" position in the dataset.

### K8 — River bank heights *(research first, then terrain)*
The owner: banks look too low against the fort views (10–20 ft with graduated slopes). The
dossier gives +2–4 ft banks at the forks (documented) but the FORT stood on distinctly rising
ground — "the flattened mound", the 1830 Harrison plan's bank, Swearingen's 18-ft pool at the
fort bend. Parcel: re-read `01-terrain-hydrology.md` and the primary accounts; raise and
GRADUATE the fort-reach south bank as the evidence supports; record the disagreement between
the tier-5 lithographs and the dossier rather than averaging it; keep the forks banks at their
documented height. Gradient audit re-run; exemption itemised like the others.

### K9 — Navigation and settings UI
(a) A **"Go to" tab** — buildings and street intersections, DOCUMENTED entries only for now
(inferred locations join later once K1 lands); it replaces the overlapping Viewpoints list and
sits as its own tab after Controls. (b) The panel opener becomes a **hamburger menu** (it is
more than settings); reassess the "?" icon. Mobile 390×780 gate; smoke tests updated with the
UI, never weakened.

### K10 — Bridge approaches
"How would a wagon cross that?" Every bridge currently floats over its banks
(`approach_not_modelled`). Build abutment earthworks/ramps that meet the deck at grade on both
ends — evidence: the 1883 settlers' statement (log abutments IN the shallow water near the
banks), deck heights already documented. Walkable end to end, wagon-plausible gradients;
regrade `ground_contact` as each bridge actually lands; move the relevant liberty text.

### K11 — Trees standing in the river
Placement bug: trees render mid-channel. `trees.js` placement must reject any position whose
ground sample is below the water surface (and the thicket screens must sit ON the point bars,
not in the water). Add the check to the smoke suite — "no tree below the waterline" — so it
cannot regress. Bank-edge willows stay; the fort views show timber ALONG the river, never in it.

### K12 — Loop hygiene *(standing instruction to every steward run)*
Every run that adds anything user-visible writes its changelog entry (v: null, ts: '') IN THE
SAME RUN — the overnight push of 2026-08-11 landed ~50 buildings with no changelog entry and
the owner noticed before we did. Publish (`tools/publish.sh`) and merge to main so the deploy
actually ships; main is the only branch Pages publishes.

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

**The 1835 lake edge is nowhere near the modern one** — everything east of roughly Michigan
Avenue is later landfill, much of it fire debris after 1871 — so drawing today's coast
would be the single largest false claim in the dataset. It comes off Wright 1834. This is
precisely the case the year-parameterized architecture exists for: `docs/EPOCHS.md` treats
terrain as versioned per epoch, so a later year gets its own shoreline rather than editing
this one.

**Which source drives which element** (set 2026-08-10 by Kevin, who is right that the
earlier reading of these sources was over-cautious — see `docs/PROVENANCE.md` § tier 5):

| element | source | confidence it supports |
|---|---|---|
| lake shore, harbour cut, piers, sand tongue, the old southward channel | **Wright 1834** — a survey, and the master warping raster | `inferred`, ±20 m; a fair estimate is expected rather than avoided |
| the river through the central blocks; street and block geometry | **Thompson plat 1830** — 80-ft streets, 18-ft alleys, generated analytically from the module, not traced | `documented` for the module, `inferred` for the fit |
| the streams coming in, and where each one terminates | **Conley/Stelzer 1833** as primary guide, Wright as the check | `inferred`, named in the note |
| **bridge positions** | **Conley/Stelzer 1833** — it draws them in place | `inferred` |
| general cross-check on all of the above | an 1836 map — **not yet in `data/sources/`; find and record one first** | — |

The standing rule still holds where it earns its keep: nothing traced from a pictorial
sheet becomes an *outline*. A reconstruction tells you a bridge was here; it does not tell
you its plan. Position `inferred` with a note, geometry from the archetype.

**Do not let ±20 m stop the work.** The uncertainty is recorded per structure and shown in
the popup; that is the mechanism for handling it. Leaving the east half of the town empty
because the shore cannot be fixed to the metre is the more misleading of the two options.

**Scope, now measured off the sheet rather than guessed.** First readings are committed in
`data/traces/vectors/wright_1834_east.json`, derived by `tools/wright_px.py` from the same
fitted affine the datum is checked against:

| feature, from Wright 1834 | local E | local N |
|---|---|---|
| Fort Dearborn (label centre) | **+1152** | +221 |
| river mouth, south bank | +1180 | +272 |
| lake shore north of the harbour | **+1331 … +1365** | +330 … +735 |
| north pier, outer end | **+1544** | +178 |

So the box must reach about **E +1700**, not the +1500 I first estimated — the harbour
works run further out than the shore does. That gives a ~2.0 km × 0.7 km field; at the
current 2.5 m cell, ~224k samples (~450 KB int16) against today's 66k (132 KB). Well inside
the 25 MB publish budget, but worth a coarser cell east of the built blocks, where the
evidence does not support 2.5 m detail anyway.

Two things the first pass settled, and one it did not:

- **The Fort Dearborn position is cross-checked.** Wright puts it at E +1152, N +221; the
  modern successor landmark (Michigan Avenue bridge) independently gives E +1127, N +195.
  35 m apart, from methods sharing no input. That is what licenses `inferred`.
- **Wright labels the reservation, not the fort.** There is no palisade plan on this sheet,
  so the footprint has to come from elsewhere — Andreas, or the fort's own published plans.
  Do not trace an outline off the banner.
- **The sand bar and the old southward channel are now read** (second pass, same day). Three
  ink lines, nested west to east: the mainland bank of the decaying old channel, the bar's
  channel side, and the bar's lake-facing side. Checked for coherence rather than eyeballed
  — at every sampled northing the three nest in order and the bar comes out 71–171 m wide,
  narrowing to its southern hook, which is what a littoral spit should do. Uncertainty is
  recorded at 30 m rather than the shore's 25: these are ink lines over a wash, and the
  southern hook is the least certain shape in this quadrant.

**The coastline gate is therefore cleared.** Shore, harbour piers, sand bar and old channel
are all in `data/traces/vectors/wright_1834_east.json` in local ENU. What S2e still needs is
the *heightfield* work — extending the zone table east over ~2.0 km × 0.7 km, with the bar
as sand and the old channel as water — not more tracing.

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

## S9 — Streets, roads and paths · **queued next after S2e (Kevin, 2026-08-10)**

Asked for as "streets, roads, paths in accurate surface and elevations". Both halves of
that have a specific answer here, and the second one is a trap.

**Geometry comes from the Thompson module, generated, not traced.** The 1830 plat gives
80-ft streets and 18-ft alleys over the original 0.375 sq mi; Wright 1834 shows the same
grid extended, and both sheets carry ±20 m of georeferencing slop that tracing would bake
in as wobble. Generate the grid analytically from the module and snap it to control. A
street that is straight because the surveyor made it straight should not arrive bent
because we traced a folded sheet.

**"Accurate surface" in 1835 means mud.** This is the trap: the instinct is to model a
crowned, kerbed, gravelled roadway, and every part of that is wrong for the date. Chicago's
streets were unpaved earth — notoriously, memorably so — with **plank sidewalks** where
anyone had bothered to lay them. The first plank roadway is over a decade later. So the
street surface is a material and a wear pattern on the prairie, not a built structure, and
the plank walks are the only raised element. Both need their own sources before they are
drawn; do not let the archetype supply them silently, which is the mistake the bridge
already made once (see v21).

**"Accurate elevations" means the streets follow the ground, because nothing had been
graded yet.** The great raising of Chicago is 1855–58, twenty years later. So there is no
cut, no fill, no crown and no camber: the roadway is the prairie surface with the sod worn
off it. Drape the grid on the heightfield and resist the urge to smooth it — the existing
gradient audit already puts the whole quadrant under 0.5 ft per 300 ft, so flat is the
finding, not a shortcut. Where a street crosses the slough or the marshy shore strip, that
is a real crossing problem the sources may describe; treat it as content, not as a
rendering artefact to be flattened away.

## S5a — Fort Dearborn · **DONE 2026-08-11**

Kevin's call, and the dependency he named is satisfied: the coastline, the sand bar and the
harbour works are read, so there is ground to put it on once S2e builds the heightfield.

- **Position is settled and cross-checked**: local E +1152, N +221, two independent methods
  35 m apart (see S2e).
- **The footprint is not.** Wright *labels* the reservation and draws no plan, so the
  palisade, blockhouses, barracks, magazine and parade have to come from elsewhere —
  Andreas 1884 carries fort plans, and the fort's own published drawings exist. Find and
  record that source before modelling; do not infer a stockade outline from a banner.
- It is a **complex, not a building**: S5's Fort Dearborn parcel already itemises palisade,
  blockhouse, bastion, magazine, quarters, barracks, sutler, hospital, parade and gardens.
  Expect several records and several bakes, not one.
- **Settle what it *was* on 1835-07-01 before drawing it.** This is the second fort, rebuilt
  1816. The garrison's comings and goings in the mid-1830s are exactly the kind of detail
  this project gets wrong by assuming — an occupied fort and an empty one are different
  scenes. Research it and cite it; `data/exclusions.json` is the place for whatever turns
  out not to be there.

**How both gates were cleared, and what it cost.**

- **The plan source exists and it is a survey.** *Map of the Mouth of Chicago River*, F. Harrison
  Jr., Ass't U.S. Civil Engineer, for the proposed harbour improvements, approved by William
  Howard 24 February 1830 — reproduced in **Andreas vol. 1 p. 113** and listed in that volume's
  own table of maps as "Fort Dearborn in 1830-32". It draws the fort in plan and names the ground
  round it (Garden for the Garrison, Cultivated Field, Big Barn with Cupola, Wash house, Well,
  Shop, Fort Cemetery, the Ferry). Recorded as `harrison_1830_river_mouth`, `asset_use: geometry`,
  tier 2 — because the plate says on its face that it carries "additions and changes … suggested
  by the Memory of Early Settlers", so it is a period survey plus fifty-year-old recollection
  mixed on one plate. **Nothing taken from it is graded `documented`.**
- **The plate has no scale bar, and that is the whole difficulty.** The scale is derived by
  setting the drawn north range equal to the commandant's quarters at "about 25 x 50 ft" from the
  1855 photograph key — 1.10 ft/px — and checked twice on the same plate (drawn aspect 1.9:1
  against a stated 2.0:1; parade width 71 ft against a stated 80 ft). **±20 %** on every derived
  dimension, on top of the datum's ±20 m. The stockade comes out about **53 m (174 ft) square**.
  **No dimension of the 1816 fort exists in the literature**: Quaife's monograph prints
  Whistler's measured 1808 draught of the FIRST fort and states none for the second anywhere.
- **The arrangement is much better evidence than the scale**, and it is what licenses `inferred`
  rather than `conjectural` for the positions: an 1830 engineer's plan and Gurdon Hubbard's 1827
  walk round the inside agree building by building, on the same sides of the same two gates.
- **The garrison is settled.** Held continuously **June 1832 → 29 December 1836**; Andreas
  brackets the scene date and the drloihjournal chronology fills the bracket with **Maj. John
  Greene, 5th Infantry**. Two companies in 1833; **no strength figure for mid-1835 was found and
  none is claimed**. The fort is modelled maintained, with its gates shut.
- **Fourteen records, two new archetypes, fourteen bakes, ~17,000 triangles.** `palisade`
  (picket stockade with named gates and corner works; worm rail fence for the garden) and
  `fort_structure` (eleven kinds — quarters, barracks, blockhouse, magazine, store, guard,
  sutler, artillery, parade, root house, tower). The lighthouse of 1832 came with them.
- **Five exclusions, four of them wrong-fort findings**: the first fort itself, the sally-port,
  the three artillery pieces and the fifty invalids, the 1850s board fence and turnstile — plus
  **there is no hospital building**, only the fort *becoming* a general hospital in the 1832
  cholera. Three corrections to `docs/research/04-structures-south.md` are recorded in
  `docs/RESEARCH/fort_dearborn.md` § 6, and one to § 2 in
  `docs/RESEARCH/chicago_lighthouse_1832.md`.
- **It stood on nothing for about four hours.** The complex is 832 m east of where the
  heightfield used to stop, and while it was there it exposed a real blind spot in the
  ground-contact gate — the clamped edge made a fort in the void report a perfect landing. See
  STATUS § "Known weaknesses" 0a. **S2e parcel (b) then landed the same day**: the field reaches
  E +1700, twelve of the fourteen structures land, and the lighthouse and the root house — both
  `conjectural` in position — moved off the channel and onto the bank top now that there is a
  surface to be wrong about. The two that remain off the ground are the stockade and the
  commandant's quarters, whose north sides cross the top of the river bank by 1.40 m and 0.46 m,
  because **no cut, fill, revetment or foundation is modelled anywhere in this project**. L46.

**Still open in this quadrant, in the order the evidence supports:** the named ground on the 1830
plan that is drawn as a symbol and a label and nothing else (Big Barn with Cupola, Wash house,
Well, Shop, Out Buildings, U.S. Factor's House, Cultivated Field, the Ferry — the Fort Cemetery
deliberately left alone); the drill ground south of the pickets, which Kinzie attests and does not
measure; the garden's planting, which is documented and needs a **cultivated flora zone** rather
than a structure; and a keeper's dwelling beside the lighthouse, which is plausible and
unattested.


## S4 — Archetype generators

One parcel per archetype, each with a golden-parameter GLB and a reference shot:

`frame_tavern` · `frame_storefront` · `frame_dwelling` · `log_dwelling` · `institutional` ·
`fort_structure` · `outbuilding` · `plank_walk` · `bridge_timber` · `pier_crib` · `palisade`

Balloon-frame logic (stud spacing, sheathing, proportions) is a first-class requirement, not a
detail: 1833–35 Chicago is where balloon framing was invented, and it is the first thing a
knowledgeable viewer checks.

**`frame_dwelling` DONE 2026-08-11** — and it is the one that unblocks houses. Until it existed
every frame record had to be a two-storey public house or a log cabin, so the dataset held
taverns, stores and a bridge and not one dwelling. It takes `stories` 1, 1.5 or 2 (default the
story-and-a-half, knee wall and gable-end attic window, which is the form of these years); reads
the rear **ell off the footprint polygon** rather than off invented dimensions, so an L-shaped
plan is built as an L and `GROUND_CONTACT: perimeter` is literally true of the mesh; builds a
stoop or a small roofed porch, never the tavern's gallery; and makes `construction` the first
attribute in this project that MOVES A VERTEX rather than sitting unread in the sidecar — the
stud module (16 in balloon, 24 in braced) places every opening, the clapboard butt joints fall on
stud lines, and a braced frame gets the girt band at its upper floor that a balloon frame has no
line for. `plan` + `bays` are **L23's own stated resolution** — a bay count derived from frontage
and a rhythm that comes from the room arrangement — so the default front is asymmetric and
unevenly spaced rather than the Sauganash's five bays worn by every building.

Still open on it, and worth a record's attention before the first house lands: no dormer (the
half storey is lit only from the gable ends), no foundation or cellar, no muntins in the sash,
and the stoop projects outside the recorded footprint. All four are in the report attached to
the parcel and belong in docs/LIBERTIES.md the day a `frame_dwelling` record does.

**`outbuilding` DONE 2026-08-11** — stables, sheds, cribs, smokehouses, privies. Built as a
FAMILY rather than a shape, because a single set of proportions that flatters the middle of the
range breaks both ends: five golden variants span a 1.25 m privy to a 13 m hotel stable, and
`GROUND_CONTACT: perimeter` is verified on all five rather than on one. Deliberate absences carry
as much of the design as the parameters — `stories` is NOT consumed, because two storeys of wall on
a secondary building is a claim and `wall_height_m` is the honest way to make it; `construction`
names log/plank/light_frame rather than balloon/braced, because nothing behind the boards of a shed
is visible at this LOD and no source describes the framing of any outbuilding here, so the
vocabulary names only what a viewer can see.

Two things it hands upward. **L10 should be NARROWED, not resolved**: this archetype can build the
Western Hotel's stable but not its wagon yard, and a yard is an enclosure — a fence line, two
gateways, trodden ground — so building it out of an outbuilding would be calling a fence a
building. The same gap swallows the estray pen and Clybourn's stockyard, and an `enclosure`
archetype is now a named want. And **registering any archetype restales every committed GLB**:
`mesh_inputs._code_shas` hashes `build.py`'s bytes for every archetype, and `build.py` carries the
`ARCHETYPES` registration table, so adding a row to it changes the hash of buildings it never
touched. Two parcels hit this independently and both verified the re-bake is byte-identical. The
fix is to split the export path out of `build.py` so the registration table stops being a mesh
input; until then one batched re-bake clears it.

**`frame_storefront` DONE 2026-08-11** — 23 consumed attributes, all 13 live storefront records
resolving with no `geometry:` declaration owed. It is the archetype where `construction` finally
separates from `frame_tavern`: balloon frame gets a thin 4 in corner board, no girt and a 16 in
module; braced frame gets a 6 in corner post and a girt line at the second floor. `cladding` is
read rather than ignored, which is the L22 defect not repeated. And the unfinished state is
buildable — open studwork over 9 in board sheathing on the loading gable, attested in kind by
Andreas for the *Chicago Democrat*'s own building at South Water and Clark, "unfinished at the
time" in November 1833. Never a default.

### Three bugs it found in neighbouring code — NOT fixed, and the third is a gate hole

1. **`MeshBuilder.add_gable_roof` fills each gable end with a solid triangle 0.25 m OUTBOARD of
   the wall.** So anything drawn on a gable at the wall plane is *inside* the roof and invisible.
   `log_dwelling._loft_opening` does exactly this: its loft openings are not in the committed
   reference image and never were. A generator that silently swallows its own output is the worst
   kind of bug here, because the reference render is what a reviewer checks.
2. **`log_dwelling`'s baked GLB has `y_min = -0.065`** while declaring `GROUND_CONTACT:
   perimeter` — an opening surround below grade. The same bug was found and clamped inside
   `frame_storefront`; this one is live in the committed asset, so a record is making a false
   ground-contact claim right now.
3. **`frame_tavern` declares `construction` and `gallery` in CONSUMED and builds neither** —
   and `test_consumed_attributes_actually_reach_the_parameters` PASSES, because it only requires
   the resolved *parameters* to move, not the geometry. Today every record says `gallery: false`,
   so the falsy rule hides it; **the first record that says `true` gets excused from a
   `geometry:` declaration for a gallery that is never built.** That is the exact failure the
   CONSUMED contract exists to prevent, sitting inside the test that is supposed to enforce it.
   Fixing it means the test has to compare vertices, not parameters.

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

### S6a — the eye-height sward · **ROUND 1 IN 2026-08-10**

`renderers/web/js/flora.js` draws the graminoid matrix, the forb layer, the emergents and the
low shrubs from `data/flora/`, mounted in `main.js` beside `trees.js`. Three layers: blade
geometry within about 7.6 m, camera-facing clump cards to 27 m, and one canopy surface at the
sward's own height from 10 m to the edge of the modelled ground. Placement is a deterministic
world lattice re-centred on the walker and culled to a 62° cone, so nothing swims underfoot and
nothing is paid for behind your head. Heights, greens, cover, phenology and per-plant confidence
all come from the records; the tuft density and the far-field surface are liberties (L32, L33).

**Judged against `WORK/bar`** — two verified photographs of surviving Illinois tallgrass in
mid-July (a Chicago-region remnant, 29 July 2021; a DuPage restoration, 24 July 2018) and an
October negative control. Where round 1 stands, measured on the primary shot rather than
asserted:

| tell | reference | round 1 |
|---|---|---|
| the ground is hidden at eye height | invisible | hidden past ~3 m, patchy in the nearest 2 m |
| several heights, several greens | 4-5 layers | 5 species heights, two greens each, per record |
| July hue (green, not tawny) | R/G 0.76-0.93 | **0.73-0.80** |
| local contrast (p90 − p10 luminance) | **141-212** | **101 near, 83 mid, 46 far** |
| no flowering bluestem/Indian grass/switchgrass | none | none, structurally |

### S6a next — the open work, in the order it is worth doing

**Reordered 2026-08-10 after a three-critic blind round on one identical shot set.** Every item
below carries a measured target and the definition it is measured with, because two rounds of
this work were spent chasing numbers that either did not reproduce or did not exist in the
reference. See STATUS.md § "Known weaknesses" 00 for the full measurements. The old list's
items 1–3 were not wrong; they were aimed at the near field, and the blind test is being lost
in the **mid** field.

1. **Draw vegetation past 455 m.** *The single biggest gap, and it is one bug behind four
   symptoms.* Canopy rings from 511.8 m outward drop to `y = 0.05` with `aMask = 0` and are
   discarded, so the vegetated surface ends where fog is 27 % and no visible surface ever
   reaches the haze all three parcels converge on. Fixing this alone should move the blind
   tell, the aerial recession, the grain collapse and the horizon step. Whatever stands beyond
   the modelled zone polygons has to be *drawn* — even a nominal community, graded honestly.
2. **Give the far sheet grain at fragment scale.** Its noise is two octaves over 88 × 36
   vertices, so its finest feature is metres across near and ~100 m across far. Target:
   5×5 high-pass RMS in the +30..70 band from **14.6 → ≥ 30** (references 31.4 and 41.7).
3. **Kill the ring seam.** `TUNE.mid.radius = 27.0` maps to a constant screen row on flat
   ground — measured as a razor edge at row 450 across all 1280 columns. Widen `ringFade`
   substantially or make the boundary irregular in world space.
4. **Crown surface.** Fine-detail ratio **0.23–0.34 → ≥ 0.55** (references 0.61–0.64); crown
   total sd **46–55 → ≤ 36** scale-matched; darkest decile **L ≥ 12, never (0,0,0)**;
   brightest decile **G−B ≥ +10** (currently −19 to −26 — sunlit crown tops are blue where the
   photograph's are warm green). Cheapest route: high-frequency shading at leaf-clump scale
   plus stochastic alpha cutout at the silhouette, a bounded indirect floor, and rebalancing
   sun against hemisphere on upward-facing normals.
5. **Horizon continuity.** Columns carrying timber **31 % → ≥ 90 %** (reference 100 % in every
   band). Band *height* stays 1–4 px — that arithmetic is honest. Two mechanisms: drop
   `hazeDisplayLinear()`'s ACES step so the band stops being aimed 16 R / 12 G past the ground
   it touches, and suppress the crown/gap modulation `k` whenever a crown subtends under ~2 px,
   where it deletes the silhouette rather than texturing it.
6. **Close the near field.** Detail-free area (5×5 luminance sigma < 2/255, below-horizon,
   resampled to 1280 wide) **13.7 % → < 2.0 %** in the nearest quarter (references 0.3–1.5 %).
   `TUNE.mat.inner = 10.0` leaves only ~66 blades/m² between the eye and raw terrain where a
   closed sward needs 270–400. Headroom is already paid for: 456 tufts placed against a 2,400
   cap. Add a **broad-leaf** element — in both references the visual mass at every distance is
   dicot leaf, not grass blade — and deepen the shade without dimming the flecks (near-band
   green p50 **121 → 75–95**).
7. **Flower load, against the corrected bar.** Whole-sward chroma flower **1.49 % → 4–6 %**
   (*not* 13.89 %: that figure came from a restoration planting on a former cornfield, not from
   prairie). Nearest quarter **0.07 % → 3.0 %**, which *is* right — it is what a never-plowed
   remnant shows at a matched look-angle. Colour variety: effN-after-median at equal N
   **144 → ≥ 300**, green hue IQR **5.6° → ≥ 8.5°**, green chroma p25 **32.3 → ≤ 26** (what is
   missing is the grey-green and glaucous foliage, not the saturated flowers).
8. **Fix the shot set before trusting any of the above.** `prairie_south` sits inside the
   gallery timber (23.4 % open sky), so there is exactly one open-prairie view and
   `prairie_west` has been tuned against itself with no control. Move it, and add a shot
   standing in **z02 mesic prairie** — the camera at `prairie_west` stands 5 cm below the z02
   elevation threshold, which is why wild bergamot, yellow coneflower, rattlesnake master and
   pale purple coneflower render zero pixels in every frame. That threshold is admittedly ours
   (the zone's own note: "a reading of the terrain, not evidence"). **Do not move species
   between zones to satisfy a camera.**
9. **`river_bank` is not honouring its own dataset.** Zone 1 specifies cordgrass at 1.2–2.0 m
   and 40–55 % cover with `bare_soil_fraction: 0.0`; the frame shows ~25 cm sprigs on bare
   soil in near-rows. The data is right; the renderer is not reading it.
10. **Adaptive budget.** Thin the sward automatically when measured frame time exceeds a
    threshold, so a slow device degrades instead of stuttering. Mobile is a release gate and
    the low-spec field is currently a fixed, hand-tuned reduction.
11. **Wind.** One travelling wave and a gust; the references show combing at several scales.

Deferred, with the reason: an **understory below 3 m** would fix a real and measured inversion
(our treeline base is *brighter* than its crowns — base/crown 1.84 against the photograph's
0.74, worth ~60 L) but it is invisible until the crowns stop reading as boulders. Fixing it
first puts a dark skirt under a pile of slate.

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
