# Liberties taken

**Append-only.** Every compression, simplification, and invention gets a row. Nothing is ever
removed from this file; if a liberty is later resolved by evidence, add a line saying so.

The standard, borrowed from the Joliet project in this repo:

> A visitor should be able to tell you which parts we made up.

The per-attribute confidence model in the data covers *attributes*. This file covers the
decisions that do not live in any single attribute — scope, scale, omission, and the choices a
reader would otherwise have to reverse-engineer.

## The `Covers:` field — what an entry claims to discharge

An entry that admits to an invention says so in machine-readable form:

```
**Covers:** `sauganash_hotel.log_1829.footprint`, `sauganash_hotel.log_1829.form.roof_type`
```

Each token is `structure_id[.phase_id].aspect`. The aspect is either one of the record's fixed
blocks — `footprint`, `position`, `documented_range`, or the structure-level `function` and
`occupants` — or any attribute of the building's form, written with its prefix:
`form.roof_type`, `form.gallery`, `form.wall_height_m`. Naming the phase covers that phase;
leaving it out covers whichever of the structure's phases stated that aspect without evidence.

The commit gate reads these claims in both directions: every `conjectural` value in
`data/structures/` must be claimed by some entry, and every claim must land on a value that is
actually invented. The prose stays the explanation and the field is the assertion — the gate
used to infer coverage from an entry's *wording*, which a liberty could satisfy by mentioning a
footprint while discussing something else.

The requirement reaches past the drawn geometry on purpose. A conjectural `roof_type` is not a
gap in the model: a gable gets built and a visitor sees a gable. A conjectural `gallery: false`
is the same claim in the negative — the front of the building is rendered plain because nobody
found evidence either way. The confidence chip says *we do not know*; only the liberty says what
we did about not knowing.

The rule runs in the other direction too, and this is the half that took longest to find a
mechanism for. An invention is a value with no evidence behind it. An **omission** is the
opposite — evidence with no geometry in front of it — and it leaves no trace in a record that
looks any different from a well-attested one. So the claim comes from the generator rather than
from a reader's attention: each archetype declares the attributes it actually reads, and any
attribute outside that set must say on the record what the mesh does instead —

```
"stables": { "value": true, "confidence": "documented", "geometry": "absent", … }
```

`absent` means nothing of it is built; `simplified` means something stands in its place that
this value does not drive; `record_only` means it was never a build instruction — a rejected
reading or a negative finding, which owes nothing. The first two are admissions, and the gate
holds each of them to a `Covers:` token exactly as it holds an invention. That is what closes
the gap this document had against a `documented` chip sitting over something a visitor cannot
see.

An entry with no `Covers:` field claims nothing and is still a liberty: navigation rules and
scope decisions have nothing in the data to point at. When evidence settles a claimed invention,
or the model catches up with an omission, move the entry to **Resolved** — the gate exempts that
section, which is what lets an append-only document survive its data being corrected.

---

## Standing liberties

### L1 — No people, anywhere
**Decision:** version 1 ships with no human figures of any kind.
**Why:** the final removal of the Potawatomi from Chicago occurred in August 1835, inside the
target year. Depicting Native presence is not a research gap to be filled by inference; it
requires consultation (see `AGENTS.md`). Rather than depict some people and not others — which
would itself make a claim — the scene is uniformly unpopulated. An empty, accurate town is
honest; a populated, invented one is not.
**Consequence:** the town reads quieter than it was. Chicago in July 1835 held roughly 3,265
people and was booming. The absence is a deliberate statement of scope, not an estimate of
population.
**Recorded:** 2026-08-09.

### L2 — Fauna presented at low density, and often as sound only
**Decision:** ambient wildlife is rendered sparsely, with many species present as audio, as traces,
or as nothing at all rather than as animated animals.
**Why:** two reasons, both evidential. July is the quietest wildlife date in the Chicago year — no
migration, silent leks, moulting waterfowl — and a summer scene populated with the spectacle of
*other* seasons would be wrong. And a boomtown of 3,265 people is not a wilderness; wild animal
density inside the platted grid was low.
**What the dataset now says (2026-08-11):** `data/fauna/` holds **139 species records across 10
habitat zones**. **Forty of them are present and would not be seen** — 25 audible only, 9 present
and imperceptible on this date, 6 as trace alone — and 15 more are recorded as absent or
deliberately withheld. Only **10 of 61 bird records are in full song** on 1 July, and each of those
carries a written argument for why that species is an exception; 42 are call-only or silent. Every
duck is flightless in wing moult. The prairie-chicken's lek is silent, the spring frog chorus is
over, and the passenger pigeon crosses in tens.
**Consequence:** the town reads quieter and emptier of animals than an eye would have found it, in
one direction only — sound carries where sight does not, and the loudest things in the July scene
are insects, frogs and livestock rather than birds. The validator enforces each of these as schema
(`tools/validate.py`, `check_fauna_species`), so this liberty is a description of the data and not
a hope about it.
**Recorded:** 2026-08-09. **Revised:** 2026-08-11.

### L3 — Vertical exaggeration available but off by default
**Decision:** the renderer may offer a vertical-exaggeration toggle; it defaults to off.
**Why:** total natural relief across the entire modeled area is under fifteen feet. Flatness is
the single most important fact about this landscape and the reason the city later had to raise
itself out of the mud. Exaggeration aids legibility and falsifies the experience, so it is opt-in
and clearly labeled.
**Recorded:** 2026-08-09.

---

## Per-subject liberties

### L4 — Sauganash Hotel: the gallery question, and how it was decided
**Decision (revised same day):** **no** gallery, tagged `inferred`.
**Why:** no period source attests one either way. The first reading followed the secondary
literature, which describes the surviving retrospective images as disagreeing, and modelled a
gallery as `conjectural`. Examining the two images the project actually holds — the Braunhold
engraving in Andreas (1884) and Kurz & Allison panel 14 (1893) — showed both depicting the
building with **no** veranda. Since the Kurz & Allison composition is probably copied from
Andreas, that is one witness and a copy rather than two, so the finding is `inferred`, not
`documented`.
**Worth noting as a process point:** the correction came from looking at the pictures instead of
reading about the pictures. Both are in the repo and both were a minute's work to open.
**How to resolve further:** any pre-1860 depiction or a written description.
**Recorded:** 2026-08-09. **Revised:** 2026-08-09.

### L4a — Sauganash Hotel: the log wing is inferred from two derivative images
**Decision:** the 1829 log cabin is modelled as an attached single-story wing on the 1831
building, tagged `inferred`.
**Why:** both retrospective depictions draw it plainly, with log courses and corner notching,
and it matches the documentary account that the frame block was "built onto" the cabin. But the
two images are not independent, and neither is a period record.
**Consequence:** the `frame_tavern` archetype has to support an attached log wing — a Milestone 0
geometry requirement that came out of the evidence rather than the plan.
**Recorded:** 2026-08-09.

### L5 — Sauganash Hotel: both footprints are invented
**Decision:** placeholder rectangles (7×6 m log, 12×8 m frame), tagged `conjectural`.
**Why:** no dimensions are attested in any source reached. The rectangles are plausible for the
type and carry no evidence whatsoever.
**How to resolve:** Andreas vol. 1 p. 106 at page-image level; then the Hathaway 1834 building
rectangle once the datum is verified.
**Covers:** `sauganash_hotel.log_1829.footprint`, `sauganash_hotel.frame_1831.footprint`.
**Recorded:** 2026-08-09.

### L6 — Sauganash Hotel: the pre-1830 position is not represented
**Decision:** the `log_1829` phase is placed at the post-move Lake & Market site for its whole
span, although the cabin stood somewhere else until about 1830.
**Why:** the original site is described only as "near the forks, on the south side" and as
having fallen inside a platted street — not precisely enough to place. Splitting the phase would
require inventing the first position.
**Recorded:** 2026-08-09.

### L7 — Wolf Point: three buildings placed from bank geometry, not from a corner
**Decision:** `wolf_point_tavern`, `miller_house` and `walker_meeting_house` are positioned by
deriving a coordinate from the datum origin at the forks and from **modern** riverbank geometry
(OpenStreetMap water polygons), because **no surviving intersection locates any of them**. The
Sauganash method — half an 80 ft platted street off a documented corner — does not apply.
**Why:** the streets that once ran past them either never existed (the north-bank point was
platted in Kinzie's Addition in 1833–35 and largely unbuilt) or have been rebuilt out of
recognition. The relative positions *are* attested — the west-bank row runs James Kinzie's house,
the tavern, the meeting house from south to north; Miller's house is on the point between the
North Branch and the main stem — so the coordinates are constrained, not free.
**Consequence:** these three carry a larger and *differently shaped* uncertainty than the corner
buildings: roughly 40 m along the bank and 20 m across it, plus an unquantified allowance for the
modern bank not being the 1835 bank. Each record states its own figure in its position note. The
sidecar's flat `uncertainty_m: 20` understates them.
**Recorded:** 2026-08-09.

### L8 — Three footprints at Wolf Point are invented outright
**Decision:** the footprints of `wolf_point_tavern` (12 × 7 m), `miller_house` (a 9 × 11 m L) and
`walker_meeting_house` (7 × 7 m) are placeholders tagged `conjectural`, citing no sources.
**Why:** no period map shows building footprints (verified for both 1834 sheets), and no text
reached measures any of these three. What *is* attested in two cases is a **shape** rather than a
size — Miller's house as a two-storey range fronting the river with a log cabin behind, Walker's
as "a small square log building" — so the polygons carry an attested proportion at an invented
scale. That distinction is stated in each footprint note.
**How to resolve:** Andreas vol. 1, "Wharfs, Piers and Early Hotels", pp. 626–631, at page-image
level.
**Covers:** `wolf_point_tavern.footprint`, `miller_house.footprint`,
`walker_meeting_house.footprint`.
**Recorded:** 2026-08-09.

### L9 — Green Tree Tavern: the footprint is derived from a room, and the side additions are left off
**Decision:** the footprint (12.19 × 7.62 m ≈ 40 × 25 ft) is **derived** from the attested 12 ft
room module, the ~8 ft central hall and the two-rank depth, tagged `inferred`; the low one-storey
additions at each end are recorded on the record but **excluded from the geometry**.
**Why:** it is the only footprint in the parcel with a textual basis, but what is attested is the
module, not the count — a three-room side gives ~52 ft, so the length is good to about ±20%. The
side additions are attested by John Gray, landlord 1838–41, which is *after* the scene date, and
nothing dates them; modelling them would assert they existed in July 1835.
**How to resolve:** the c. 1859 photograph (CHM ICHi-040230), which shows the building at its
original corner and would settle dimensions, exterior finish and the gallery at once.
**Covers:** `green_tree_tavern.frame_1833.form.side_additions`.
**Recorded:** 2026-08-09.
**Revised:** 2026-08-10 — the omission is now claimed rather than described. The record carries
`side_additions: true` and the `frame_tavern` archetype has no parameter for it, so the attribute
reaches the mesh nowhere; the record says so with `geometry: "absent"` and this entry is what the
gate matches that declaration against.

### L10 — Western Hotel: the stable and wagon yard are attested and not modelled
**Decision:** only the hotel block is built. The "large stable and the yard into which the trains
were driven", with entrances from both streets, are recorded as `stables: true` and left out of
the geometry. The L's **arm widths** (7.0 m) are invented; only its 40 × 60 ft envelope is
attested.
**Why:** neither the stable nor the yard is dimensioned or located, and the `frame_tavern`
archetype builds a building, not a parcel.
**Consequence:** this understates the site more than any confidence tag can express — the yard
*is* the west-side teamsters' house as a visitor experienced it, and the model shows a hotel
standing in nothing. A parcel-level or yard archetype would fix it.
**Covers:** `western_hotel.frame_1834.form.stables`,
`western_hotel_stable.stable_1834.form.wagon_yard`.
**Revised:** 2026-08-11 — **narrowed, not resolved: the stable is now built and the yard still is
not.** `data/structures/western_hotel_stable.json` stands the large stable behind the hotel on the
attested relation — "In the rear was the large stable and the yard into which the trains were
driven" — so the half of this entry that said a hotel stands in nothing is no longer true of the
stable. THE YARD REMAINS OUT OF THE MODEL AND CANNOT BE PUT IN IT BY THIS ARCHETYPE. A yard is an
enclosure — a fence line, two gateways and the ground between them — and `outbuilding` builds a
building; using it here would mean calling a fence a building, which is a worse claim than the
omission. The two gateways, on Randolph and on Canal, are unbuilt for the same reason. The
admission has therefore MOVED AS WELL AS SHRUNK: it now sits on the stable's own record as
`form.wagon_yard: {value: true, confidence: "documented", geometry: "absent"}`, beside the building
it belonged to, while `western_hotel.frame_1834.form.stables` keeps its own `geometry: "absent"`
because the hotel's mesh still contains no stable. WHAT WOULD RESOLVE THIS ENTRY RATHER THAN
NARROW IT AGAIN: an enclosure archetype. The same missing archetype is why `estray_pen` is drawn as
a roofed shed, why Clybourn's stockyard is unmodelled, and why the pig pens the town code of
November 1833 implies have nowhere to go.
**Recorded:** 2026-08-09.
**Revised:** 2026-08-10 — claimed rather than merely described. `stables` is `documented`, which
is the strongest chip this project has, and it sits over a building with no stable within a
hundred metres of it; the record now declares `geometry: "absent"` and the gate holds that
declaration to this entry.

### L11 — Western Hotel: one completed phase on a disputed date, rather than a construction phase
**Decision:** modelled as complete and in operation on 1835-07-01, on the 1834 build date, with
no `construction_1835` phase.
**Why:** the date is disputed 1834 (the builder W. H. Stow's own word, with corroborating detail)
against 1835 (an undated line in a chronology that also mis-sizes the building). A construction
phase would have to invent a start month, a duration and a degree of completeness that no source
gives — and would silently adopt the weaker date in order to have something to model.
**How to resolve:** any account of the Western independent of Stow. If 1835 is confirmed, split
the phase then.
**Recorded:** 2026-08-09.

### L12 — Walker Meeting House: placed on one side of a disputed river
**Decision:** placed on the **west** bank, north of the Wolf Point Tavern, position tagged
`inferred`.
**Why:** two near-primary witnesses (Wau-Bun 1831; chicagology's transcribed recollection) put a
Walker-built log worship-and-school building on the west bank and give a *relative position* that
can be placed. The competing reading — the successor congregation's own history, "in 1834 the
growing congregation built a log cabin north of the Chicago River" — is modern, unfootnoted, and
gives a division rather than a location.
**Consequence:** **if the north-bank reading is right, this building is about 150 m from where it
is drawn, on the far side of the North Branch.** The likeliest reconciliation is that both are
true of *different* buildings — an 1831 school-house on the west bank and a purpose-built 1834
cabin on the north — in which case the model has the wrong one. Note also that
`data/exclusions.json` states in passing that the 1835 meeting house is on the north bank; that
file and this record disagree and neither was edited to match the other.
**How to resolve:** Andreas on the early Methodist society; the congregation's own archives; or
the reported 1835 painting showing Wolf Tavern, Miller's House and Walker's cabin in one view.
**Covers:** `walker_meeting_house.log_1831.position`.
**Recorded:** 2026-08-09. **Revised:** 2026-08-10 — the Decision line above still reads
`inferred`, which is what this entry claimed when it was written. The record was downgraded to
`conjectural` on 2026-08-09, on the reasoning in its own position note: choosing between two
readings 150 m apart across a river is a coin flip with an argument attached, not a derivation.
The `Covers:` claim is the binding statement of what this entry discharges; the stale word is
left standing because the file is append-only and a silently corrected admission is not one.

### L14 — Terrain: a conjectural micro-relief under every claim
**Decision:** the land surface carries ±0.10 ft (30 mm) of two-octave value noise everywhere,
and the `_CONFIDENCE` channel does **not** report it.
**Why:** no contour survey of the 1835 town site exists, so the terrain is a set of zone levels
from period narrative feet, and a zone level rendered literally is a dead-flat plane that reads
as a rendering error rather than as ground — and gives a walker no motion parallax to judge
distance by. The noise is a texture, not a claim: its amplitude is below the 0.25 ft the dossier
asks the heightmap to be *quantised* at, and far below the resolution of any statement in the
record. The confidence channel carries the zone's tag because the zone level is the claim being
made. Setting `micro_relief.amplitude_ft` to 0 in `terrain_spec.json` removes it entirely.
**Consequence:** the plain is measurably rougher at cell scale (2.8 ft per 300 ft) than the
dossier's flatness rule, while the *block* gradient the rule is actually about stays inside it
(0.47 ft per 300 ft). The generator prints both on every run.
**Recorded:** 2026-08-10.

### L15 — Terrain: the west-prairie swales are invented alignments
**Decision:** two shallow swales (0.75 and 0.6 ft deep) cross the West Division wet prairie,
tagged `conjectural` and rendered dithered-translucent in the confidence view.
**Why:** dossier zone 18 says the West Division carried "1–2 ft slough swales", so that swales
existed is inferred from a source. **Where they ran is attested nowhere**, and these two
alignments were drawn to make the wet prairie read as wet prairie rather than as a lawn. They
are the only piece of terrain geometry in this parcel invented outright.
**How to resolve:** the 1821 GLO township plat land-cover, or the ISGS "Illinois Landcover in
the Early 1800s" digitisation, both named in the dossier and neither reached.
**Recorded:** 2026-08-10.

### L16 — Terrain: the water is a wall to the walker
**Decision:** the heightfield carries the real channel bed (about −12 ft in the main stem), the
ground mesh draws it, and the walker cannot enter the water — `terrain.height()` reports a
barrier at the waterline instead of the bed.
**Why:** a walker whose eye is pinned to the bed walks into the river and looks at the town from
under the water, which reads as a bug rather than as a river. This is a navigation rule, not a
claim about the terrain: nothing about the modelled ground changes, and `groundHeight()` still
reports the truth. It is a liberty because a person in 1835 could in fact cross — by the ferry
at Wolf Point, or by boat — and the model currently offers neither.
**Known edge:** a walker *teleported* into the channel — by a camera anchor or by the test
harness, never by walking — stands on the barrier and appears to float. Every anchor in
`data/scenes/1835.json` is on land (the `forks` placeholder that was not has been moved), so it
is not reachable in normal use, but it is the shape of the compromise and it is written down
rather than discovered.
**How to resolve:** model the ferry and the bridges as structures, then let the walker use them.
**Recorded:** 2026-08-10.

### L17 — Terrain: the ground continues past the modelled box as a radial skirt
**Decision:** the heightfield covers a 640 m square around the forks. Beyond it the ground mesh
carries each boundary height radially outward to 1400 m, so the river widens into the fog rather
than ending at a cliff.
**Why:** the alternative — a hard edge at 320 m — is a worse lie than a smeared one, and the
scene's fog is total by 1500 m. Nothing outside the box is modelled, sampled, or claimed: the
heightfield's own sampler returns its fallback there, and the skirt is geometry for the horizon
only.
**Consequence:** the main stem appears to widen as it recedes east. Anyone extending the model
east to the harbour replaces the skirt with real terrain rather than editing it.
**Recorded:** 2026-08-10.

**Revised 2026-08-11 — two statements in the text above are now false, and the east half of this
entry is retired.** The box is no longer "a 640 m square": S2e extended it to **E −320 … +1700,
N −400 … +400**, 2 020 × 800 m. Modelled ground now reaches **300 m past where the old skirt itself
ended**, so nothing east of the town is skirt any more — the shore, the 1834 cut, the sand bar, the
old southward channel, Fort Dearborn's site and twenty-odd buildings all stood in it and now stand
on real terrain. In area, 0.966 km² of the old 7.43 km² skirt has become ground. **The stated
consequence is retired with it**: the main stem no longer "appears to widen as it recedes east",
because it runs to its actual mouth inside the box, and what recedes east is open lake.

**And the skirt is no longer radial**, which matters more than it sounds. Radial scaling on a
2 020 × 800 rectangle pushes the east edge out by a quarter of what it pushes the north — backwards,
since east is the direction with the most to hide. It is now a **rectangular apron of 1 500 m per
side**, which is also the first time the skirt actually reaches the distance this entry's own
argument leans on: the old radial construction reached only 1 080 m beyond the edge while the text
claimed 1400. So the apron is **larger in absolute area than the thing it replaced** — 17.46 km²
against 7.43 — and that is worth admitting in the same breath as the good news, because the part
that mattered is gone and the part that grew is prairie and lake nobody looks at.

What has NOT changed: nothing outside the box is modelled, sampled or claimed, the heightfield's own
sampler returns its fallback there, and the apron is geometry for the horizon only. It costs 2 256
vertices.

### L18 — Sauganash Hotel: the 1829 cabin's height and its roof are placeholders
**Decision:** the `log_1829` phase is built 2.4 m to the plate under a gable roof, both tagged
`conjectural`, both carrying the word PLACEHOLDER in their own notes.
**Why:** nothing attests either. 2.4 m is an ordinary single-storey hewn-log wall and a gable is
the near-universal roof for the type and the period — but the ordinary reading of a *type* is not
evidence about a *building*, and that is exactly where this project draws the line between
`inferred` and `conjectural`. The 1831 frame block's height and roof are `inferred` because the
reasoning is about that block: two storeys are documented and the form is described. The cabin
has neither, so its numbers were chosen rather than derived.
**Consequence:** the oldest thing standing in the scene — the attached wing of L4a, which a
visitor walks straight past — has an invented height and an invented roof. The dithered massing
says its size is unknown; it does not say that 2.4 m and a gable were picked because they are
usual.
**How to resolve:** any dimensioned description of the 1829 cabin. Failing that, the Braunhold
engraving at page-image level, where the wing's height can be measured against a block whose
storey count is documented.
**Covers:** `sauganash_hotel.log_1829.form.wall_height_m`, `sauganash_hotel.log_1829.form.roof_type`.
**Recorded:** 2026-08-10.

### L19 — Green Tree and Western: two galleries decided by default, not by evidence
**Decision:** `gallery: false` on both the Green Tree Tavern and the Western Hotel, tagged
`conjectural` on both. Both buildings render with a plain front.
**Why:** no source reached describes a porch, veranda or gallery on either building, and none
rules one out. False is what the archetype falls back to, not a finding. The Green Tree's
witnesses describe two entrances — the front on Canal and one "about the middle of the long side"
on Lake — without mentioning a porch, which is weak negative evidence at best: they were
correcting a drawing, not inventorying an elevation. The Western is more open still. A wagon
house with entrances to its yard from both streets is precisely the type that often carried a
porch over the door, and nothing here says it did not.
**Consequence:** this is an invention that does not look like one. A drawn footprint announces
itself — the visitor can see that a shape was chosen. A plain elevation reads as the finding,
and the confidence tint on an attribute whose value is `false` has nothing to dither. Recorded
here because the model shows two blank fronts that no source put there.
**How to resolve:** the c. 1859 photograph (CHM ICHi-040230) settles the Green Tree the moment
anyone opens it. For the Western, any depiction at all — the project holds none.
**Covers:** `green_tree_tavern.frame_1833.form.gallery`, `western_hotel.frame_1834.form.gallery`.
**Recorded:** 2026-08-10.

### L22 — Wall surfaces are the archetype's, not the record's
**Decision:** `cladding` on the four frame buildings and `paint` on the three log ones are
recorded and unread. Frame walls always get clapboard lap courses; log walls always get bare
hewn log. A record saying `cladding: board_and_batten` or `paint: white` on a log core would
change nothing on screen.
**Why:** each archetype was written for the buildings it had, and every one of them is
clapboarded or unpainted, so the fixed surface and the recorded value have never differed. The
`frame_paint` parameter drives a frame addition's colour; nothing drives the log core's.
**Consequence:** the dataset's weakest inferences are here — `cladding` and `paint` are
`inferred` on almost every record, several of them explicitly "not attested either way" — and a
visitor cannot tell that the surface they are looking at is the archetype's default rather than
the record's reading. Where evidence is thin, an unread attribute is a claim made twice.
**How to resolve:** wire both attributes through `from_phase` and re-bake. Note the ordering
this creates: the Sauganash's documented white paint IS read, so painted frame is already
data-driven; it is the surface *texture* that is not.
**Covers:** `green_tree_tavern.form.cladding`, `miller_house.form.cladding`,
`sauganash_hotel.form.cladding`, `western_hotel.form.cladding`, `miller_house.form.paint`,
`walker_meeting_house.form.paint`, `wolf_point_tavern.form.paint`.
**Recorded:** 2026-08-10.

### L23 — One window arrangement, on every frame building
**Decision:** `fenestration` is recorded on the three frame taverns and read by none of them.
The archetype builds the same elevation on all three: five bays above, four plus a centred door
below.
**Why:** the arrangement came from the two Sauganash depictions and was made the archetype's
default. The Green Tree's record says `small_paned_sash`, which describes the glazing and not
the layout, and the Western's says `regular_bays`, which describes the layout only loosely —
neither is a rhythm anyone could build from, so the default was never replaced.
**Consequence:** three buildings of different sizes wear one facade. The Western is 40 ft on its
front and the Sauganash's five-bay rhythm is spread across it unchanged, which reads as a
finding about how the town was built and is instead an artefact of one archetype.
**How to resolve:** a bay-count parameter derived from frontage, and records that state a rhythm
rather than a glazing type. Both, then a re-bake.
**Covers:** `green_tree_tavern.form.fenestration`, `sauganash_hotel.form.fenestration`,
`western_hotel.form.fenestration`.
**Recorded:** 2026-08-10.

### L24 — Wolf Point Tavern: the frame bay's side, width and depth are invented
**Decision:** the frame half of the "partly log and partly frame" tavern is built as a
one-storey bay 4 m wide and the full 7 m depth of the footprint, at the north end of the log
core. Its side, its width and its depth are tagged `conjectural`; that it existed at all is
`documented` and its single storey is `inferred`.
**Why:** the evidence is one clause — "This building was partly log and partly frame" — and it
gives no dimension, no position on the building and no date. Something had to be built or the
documented half of the fabric stays invisible, which is the failure L20 records. So the numbers
are chosen and declared rather than defaulted: 4 m of a 12 m frontage keeps the building reading
as a log house with a frame piece rather than the reverse, which is the distinction that decides
which archetype the record belongs to at all; the full depth avoids a notch at the back corner
that would read as a modelled fact about the plan; and `end` is the cheapest way to enlarge a log
pen, since the ridge simply runs on and no log wall is cut.
**Consequence:** a visitor sees one specific frame bay in one specific place. The confidence view
dithers it by what it IS — documented that it existed, inferred that it was low — and not by its
unknown size, following the rule set for the Sauganash: dimensional uncertainty belongs in the
sidecar, where the popup shows it, rather than ghosting a building whose character is attested.
So the tint alone will not tell a visitor that the width is a guess. This entry does.
**How to resolve:** Andreas vol. 1 pp. 626-631 at page-image level, or the Braunhold retrospective
view of Wolf Point at plate level — the same two unopened sources that would settle the footprint.
**Covers:** `wolf_point_tavern.log_frame_1828.form.frame_addition_side`,
`wolf_point_tavern.log_frame_1828.form.frame_addition_width_m`,
`wolf_point_tavern.log_frame_1828.form.frame_addition_depth_m`.
**Recorded:** 2026-08-10.

### L25 — Wolf Point Tavern: the wolf on the sign is not drawn
**Decision:** the tavern's sign is modelled as a plain weathered board hanging from a bracket.
The painted wolf that gave the point its name is not depicted, and the board carries no image at
all. The record's `sign` value names the subject — `painted_wolf_sign` — so the popup can say
what hung there while the mesh says only that something hung there.
**Why:** the sign is documented and the image is not. No description of the painting survives —
not its size, not the board's shape, not how the wolf was drawn, not whether it was a whole
animal or a head — and a wolf painted from imagination would be the most conspicuous invention in
the scene, on the one object every visitor will walk up to. The bracket, the arm length and the
board's proportions are invented too; they are archetype geometry rather than record values, in
the same way L22 covers wall surfaces.
**Consequence:** the most famous object at Wolf Point is present and blank. That is the honest
reading — a board hung there, and we do not know what was on it — but it is a deliberate absence
a visitor might otherwise take for an unfinished model.
**How to resolve:** any period description or depiction of the board. None is held.
**Recorded:** 2026-08-10.

### L26 — Every chimney stands where the archetype puts it
**Decision:** the records count the stacks and the archetypes place them. On a frame block
(`sauganash_hotel`, `green_tree_tavern`, `western_hotel`) they sit on the ridge line, spaced
evenly between 0.22 and 0.78 of the frontage. On a log building (`wolf_point_tavern`,
`miller_house`, `walker_meeting_house`) the first stands outside the log core's gable wall, and a
second — where a record counts two — stands against the outer gable of the frame addition. Every
stack is the same 0.96 m square shaft with a corbelled head, rising 0.55 m above the ridge it
passes.
**Why:** not one source in this dataset describes a chimney on any of these six buildings. What
the sources give is a count, and only for the Sauganash is even that drawn ("both depictions show
two"); everything else — position, size, material, whether the stack was inside the wall or
against it — is typological. Something has to be built, because a heated tavern with no stack is
a claim too, and a stated count with no geometry is the failure L21 records. So the arrangement
is argued rather than preferred: an exterior gable-end stack is the frontier pattern for a log
pen, a pair on the ridge is what a central-hall frame block carries, and the second stack on
Miller's house goes on the frame range because *the record's own reasoning for counting two* is
"a stack in each element" — building both on the log core would honour the number and contradict
the argument for it.
**Consequence:** the confidence tint on a stack is the count's — `inferred` on every building
here — and a visitor reasonably reads that as covering the thing they are looking at. It does
not. It covers *how many*, and nothing at all about *where*, *how big* or *made of what*. This
entry is the only place that distinction is legible.
**How to resolve:** any depiction at plate level. The two retrospective Sauganash images would
settle position and rough proportion for that building alone; nothing held would settle the
others.
**Recorded:** 2026-08-10.

### L27 — Miller House: the frame range's width and depth come from an invented plan
**Decision:** the two-storey range fronting the river is built 9 m wide and 6 m deep — the whole
frontage of the footprint and a little over half its depth — with the log cabin occupying the 5 m
behind it. Both numbers are tagged `conjectural`. That the range existed, that it stood on the
river front and that it was two storeys are all `documented`; only its size is invented.
**Why:** the sources give this building a composition and never a dimension. "A two-story house
added to the cabin, fronting the river" and the 1833 view's "a two-story building and adjoining
log cabin" say what the parts were and how they sat, and no source reached says how big either
one was. The width and depth are therefore read off this record's own footprint polygon, whose
river-fronting limb is 9 × 6 m, rather than picked afresh — which makes the mesh agree with the
plan the record already draws instead of taking the archetype's defaults of half the width and
half the depth, a 4.5 m block in the middle of a frontage the polygon draws full-width. That is a
smaller invention than a new number and it is still an invention, because the polygon is a
PLACEHOLDER: its own note says every number in it is made up. A fraction of a guess, exactly as
L24 says of the Wolf Point bay.
**Consequence:** two things a visitor cannot see from the confidence tint. The range is dithered
by what it IS — documented that it existed and was two storeys — and not by its unknown size,
which is the rule set for the Sauganash and repeated for Wolf Point in L24. And the record draws
an L while the archetype masses a rectangle: the log core is carved out of the footprint's
bounding box, so it comes out the full 9 m wide rather than the polygon's 6 m, and the 3 × 5 m
re-entrant corner behind the range is filled in. Stating the range's own numbers is what makes
that visible — before this slice the defaults left an inverted-T that matched neither the polygon
nor the sources.
**How to resolve:** Andreas vol. 1, "Wharfs, Piers and Early Hotels" pp. 626-631 at page-image
level — the same unopened source that would settle the footprint this inherits from.
**Covers:** `miller_house.log_frame_1827.form.frame_addition_width_m`,
`miller_house.log_frame_1827.form.frame_addition_depth_m`.
**Recorded:** 2026-08-10.

### L30 — The bridge lands on nothing, and no approach is modelled
**Decision:** the North Branch bridge's deck stops at the traced 1834 waterline at both ends,
2.42 m above the ground beneath it, and **no approach of any kind is built** — no embankment, no
ramp, no sloping run of deck. The crossing stands in the river and touches neither bank.
**Why:** the deck sits 2.22 m above the water (Cleaver's inferred six-foot clearance plus the
stringer and plank depth under it), and the modelled ground at both landings is Z = 0 by
construction, because the terrain surface crosses the datum exactly along the drawn waterline.
The highest land anywhere in the 640 m box is 1.31 m. So there is nothing for the deck to arrive
at, and nothing anybody wrote says what did. Andreas gives the stringers; Cleaver gives the
width and log abutments "in the shallow water near the banks"; no source reached describes how a
person or a team got from the bank up onto the deck. Building one would stack a second invention
on top of the clearance figure — which is itself only `inferred`, and unsourced in the dossier
that supplied it — and unlike the fifteen cribs of L29, it is the invention a visitor would walk
over rather than look at.
**Consequence:** the crossing reads as a bridge to nowhere. From the bank you cannot step onto
it, and the walkthrough cannot pretend otherwise: the walker follows the terrain, so the deck is
scenery you pass under. That is honest about the evidence and wrong about the town — a bridge
that carried a procession of hundreds in August 1835 plainly met its banks. Every part of that
gap is unrecorded, so it is stated rather than drawn.
**How to resolve:** a period depiction of the crossing or a levelled section. The 1834/1835
Wabansia and Kinzie's Addition plat, contemporaneous to within two weeks of the scene date, is
the best candidate; a sourced clearance figure would also narrow it, since a lower deck needs
less approach and the six feet is the weakest number in the record.
**Covers:** `north_branch_bridge.log_1832.ground_contact`.
**Recorded:** 2026-08-10.
**Evidence since:** both candidates named above were pulled on 2026-08-10 and **the gap is
unchanged, but two of the escape routes out of it are closed.** The Wabansia and Kinzie's
Addition plat is the sheet this project already holds as `hathaway_1834`; inspected at the
crossing's own georeferenced pixel it draws no bridge, and neither does Wright 1834 — both stop
their street lines at the waterline, because a platted street is a dedication and not a
structure. And the six feet is no longer "the weakest number in the record": Caton, Bates,
Cleaver and Noble state it in 1883, and state why — the bridges "were about six feet above the
water, so that teams passed under them on the ice freely" — so a lower deck is not available as
the cheap way to shorten an approach nobody described. The same sentence calls these **wagon**
bridges, which means a wagon reached the deck somehow. The approach is therefore better attested
as a fact and no better described than it was. See `docs/RESEARCH/north_branch_bridge.md` §6.
**Revised:** 2026-08-10.

### L31 — The two bents are where a builder would put them, not where anybody saw them
**Decision:** the North Branch bridge's two bents stand at the third points of its 71.83 m span,
23.94 m and 47.89 m from the west landing, each built as four heavy logs under a cap log. The
count and the form are `documented`; **the stations are the archetype's**, and so is everything
about a bent except how many logs stood in it.
**Why:** the 1883 old-settlers statement gives a count and a construction and no geometry —
"built on abutments and two 'bents'", the abutments "in the shallow water near the banks" and
the bents "resting on the bottom, in deeper water". That locates them by depth, which this
project cannot use: no source gives the channel's bed profile at the crossing and the
heightfield models nothing below the waterline, so "deeper water" cannot be turned into a
station. Even thirds are therefore what a builder would do with three roughly equal stringer
runs, and they are not a finding. The alternative — biasing the two toward the middle to match
"in deeper water" against a guessed channel section — would invent a riverbed in order to place
a pier, which is two inventions where this is one.
**Consequence:** three things a visitor cannot read off the confidence view, and this entry is
where they are legible. The chip on `pier_count` grades **how many**, and a visitor standing on
the bank sees exactly where they are. The girth of the logs, the cap, and the fact that the four
stand in a row across the deck rather than paired are the archetype's throughout. And the
letter's most specific phrase — *resting on the bottom*, which is what distinguishes a bent from
a driven pile bent — is invisible in the model, because nothing below half a metre under the
waterline is built at all.
**A fourth thing, and it is the honest cost of the repair.** Three spans instead of sixteen
makes each stringer run 23.9 m, and nobody was moving a 23.9 m timber. The letter says stringers
"stretched from the abutments to the bents, and between the bents" and never says they were
single sticks; they were spliced somewhere and no source says where. The mesh shows one log per
bay, so the splices are **omitted** rather than invented — the same choice L30 makes about the
approach, one order of magnitude smaller.
**How to resolve:** a survey, a section, or a repair account with dimensions. Andreas's main text
records that a committee was appointed in December 1833 "to see that they were properly
repaired" and that "in September the corporation paid $166.67 on account of repairing" — a
voucher or a council minute behind that payment is the most likely thing to describe the
structure member by member.
**Recorded:** 2026-08-10.

### L32 — The sward is drawn at a density that hides the ground, not at a stem count
**Decision:** the near field plants roughly **7.3 tufts per square metre**, each tuft a dozen
blades, and that number is a rendering constant in `renderers/web/js/flora.js` (`TUNE.near`).
It is not derived from any record.
**Why:** the flora records give **cover fractions** for the matrix grasses — cordgrass 40-55 %
of the ground in wet prairie, bluejoint 15-25 % — and no source anywhere gives shoots per
square metre for the 1835 lake plain. A real tallgrass sward carries hundreds of shoots to the
square metre; drawing that is not affordable in a browser, so a tuft instance stands for a
*bundle* of shoots rather than for a plant. The records therefore set the MIX — which species,
in what proportion, at what July height, in what greens, in flower or not — and this constant
sets how much geometry is spent realising it. It was tuned against the one thing a photograph
can settle: at standing eye height, in the reference images of surviving Illinois tallgrass in
mid-July, the ground is not visible at all.
**Consequence:** the count of plants on screen is not a measurement and must never be read as
one. A reader counting cordgrass clumps per square metre in this walkthrough is counting a
rendering budget. Cover fractions, heights and phenology *are* the record and can be read.
Two smaller companions to the same admission: only about one tuft in six of a flowering matrix
grass carries a spike, because a bundle of shoots is not a plant and a culm on every bundle
gave the wet prairie the look of a wheat field; and the dead-thatch tint is applied to 7 % of
tufts, a proportion nobody recorded, kept small because a straw-coloured sward is the October
negative control rather than July.
**How to resolve:** it does not resolve into evidence. It could be replaced by a stem-density
model if a modern remnant survey of a comparable community is adopted as a proxy and recorded
as such.
**Recorded:** 2026-08-10.

### L33 — Beyond about ten metres the prairie is a canopy surface, not plants
**Decision:** vegetation is drawn as individual geometry only within about 27 m of the
visitor. Beyond that the sward is a single sheet at the height of the community's own canopy —
coloured by the zone under it, holed where the records say water — carried out to the edge of
the modelled ground.
**Why:** from an eye height of 1.68 m, a sight line that reaches the soil 60 m away is 1.6
degrees below the horizon; everything from 45 m to the horizon occupies about two degrees of a
fifty-degree frame. Nothing drawn out there can be resolved as a plant, and everything drawn
out there is paid for across the whole plain. The sheet is not a claim that the far prairie is
smooth: it is the top of the sward, which is what a standing observer can actually see of it.
**Consequence:** the far field carries no species. It is coloured from the mean July foliage of
the zone's graminoids and stands at their mean height, so a community change shows as a change
of green and of level and never as a change of plant. The confidence view marks the whole sheet
`inferred`, which is the honest grade for a surface nobody surveyed, but it cannot grade the
species mix underneath it because it is not drawing one. There is also a visible seam in
principle where the sheet begins; it is ragged and it sits behind the drawn plants, but a
visitor who looks for it on flat ground will find it.
**How to resolve:** more geometry, or an impostor scheme that carries species identity into
the far field.
**Recorded:** 2026-08-10.

### L34 — The sky is corrected toward one photograph, and only near the horizon
**Decision:** the sky is Preetham's model as the vendored `Sky.js` implements it, with one
fitted correction applied inside its fragment shader (`HORIZON_RESTORE` in
`renderers/web/js/world.js`): red and green are attenuated as the sight line approaches the
horizon, blue is untouched, and the effect dies out above about 25°. The three constants that
shape it were solved by least squares against **one photograph** — the July reference in
`bar/`, sampled at ten elevations from 16° down to 0.5°.
**Why:** the model has a genuine defect at the horizon and it is not a matter of taste.
`Sky.js` builds its in-scatter with a `(1 - Fex)` extinction term, and along a horizon ray the
model's own optical path runs ~26× the zenith path at 1° up. `Fex` has gone to zero in all
three channels there, so `1 - Fex` is (1,1,1) and the only wavelength-dependent factor in the
in-scatter is gone. What remains is the ratio of the two phase functions, which is nearly
achromatic — 0.816 : 0.919 : 1.000 for this scene at 1°. The model therefore renders a **white**
horizon: sRGB (181,191,195) at saturation 0.072, where the photograph reads (136,163,192) at
0.288. The error is not a shortage of blue — our blue was 195 against its 191 — it is red +45
and green +28 that a real horizon does not carry. So the correction restores channel dependence
the saturated term threw away, rather than adding a colour the sky did not have.
**Consequence:** the sky above the horizon is no longer purely a physical model's output. It is
a physical model plus an empirical fit, and the fit's authority is the authority of a single
photograph taken on one afternoon at one place. Two specific limits follow. First, it is
**azimuth-blind**: the defect is the same in every direction but the model's horizon
*brightness* is not, and the reference photograph looks within 19° of the sun. Subtracting the
same fraction of red and green from the anti-sun sky leaves it bluer and darker than a
photograph would be — measured at 1° above the north horizon, (104,132,166): the hue is right
(B−R +62 against the bar's +55, where before the correction it was +17) but the luminance is
128 against 160. The render brackets the photograph rather than sitting on it, and it now
brackets from the blue side instead of the grey side. Second, between about 8° and 12° of
elevation the sky is still 15–20 units short of the reference in B−R; that residual is tone-map
compression in the blue channel and was deliberately left alone.
**How to resolve:** an azimuth term, which needs a second **verified** July photograph shot away
from the sun to fit against. There is not one in `bar/`, and deriving the anti-sun sky from the
solar one would be invention of exactly the kind this project refuses. Until then the honest
statement is the one above: correct toward the sun, bracketing away from it.
**Recorded:** 2026-08-10.

### L35 — The far timber is exempted from the air that hides everything else
**Decision:** the horizon timber band runs the scene's own haze law by hand against each
body's real distance, but caps it: `HAZE_MAX = 0.82` in `renderers/web/js/trees.js`. Every
other distant thing in the scene is hazed by the shared fog, which is deliberately total by
1500 m. The timber alone is not allowed to disappear.
**Why:** two commitments in this repo point opposite ways and one of them had to give. **L17**
leans on total extinction at 1500 m to hide a radial ground skirt that nothing is claimed
about — if the air did not close, the skirt's edge would be visible and would look like
landform. But the timber dossier § 1.6 is a table of real timber bodies at **three, four and
six miles**, explicitly headed "for distant LOD / horizon silhouettes", and total extinction at
1500 m erases every one of them. Deleting them to satisfy the fog would be erasing evidence to
protect a convenience. The cap keeps them visible at a contrast that never exceeds what the
scene's air already allows anything else at about 1.2 km, so it buys the dossier's timber back
without letting the band claim more clarity than the atmosphere elsewhere permits.
**Consequence:** distance in this scene is not governed by one law. Ground, water and sward
obey the fog; the timber band obeys the fog up to 82 % and then stops. A visitor cannot see
this. Three things follow, and the third is this entry correcting itself.

First, the further bodies are **compressed**: `hazeAt` reaches the cap at about 1.15 km, so
everything from there out to the furthest body at 9.7 km renders at one identical value. Their
relative distance is not readable, and the band is *evidence that timber stood out there*, not
a measurement of how far.

Second — **and this entry got this wrong once already, so the retraction is worth keeping.** An
earlier revision said the cap had become load-bearing tonally: that since the haze colour was
retargeted, a fully-hazed surface displayed *brighter* than the sky behind it (L 170.1 against
L 161.7), leaving this cap as the only thing keeping the band dark. That was a real measurement
of an unreal thing. In the vendored three r185 the fragment order is `opaque → tonemapping →
colorspace → fog`, and the fog colour is uploaded through `getUnlitUniformColorSpace()`, so the
scene's fog is a straight lerp toward the literal hex **in display space, after the tone
curve**. A fully-fogged surface therefore renders sRGB (136, 163, 192) — L **159.4**, four
levels *below* the horizon sky, which is exactly what airlight should do. The L 170.1 figure
came from `trees.js` running the haze colour through ACES a second time to derive its band
colour, which is the answer to a question the renderer never asks. There was no atmospheric
inconsistency. There was a colour-management error in one file, and this register briefly wrote
it up as physics.

What survives is smaller and still true: because `trees.js` aims its band at (152, 175, 195)
while the ground it stands on converges to (136, 163, 192), the two are **16 red and 12 green
apart** with the band `toneMapped: false, fog: false` so nothing downstream reconciles them.
The far timber and the far ground are lit by two different laws and meet at the horizon.

Third — **this entry asserted a visual outcome and the assertion was false.** It first said a
visitor "would have no reason to suspect it — the band simply reads as far-off woods." Measured
in the delivered frame, the band covers **0.9 %** of its own detection window at Weber **0.026**,
and only **31 % of horizon columns carry any timber at all** — 3.6 % across the central
two-thirds — against 100 % of columns in the reference photograph. It does not read as far-off
woods, and it does not read as a pale ridge either. It mostly does not read. Both sides of the
capping choice sit below the visibility threshold, so the liberty this entry exists to confess
is currently invisible, while the *absence* it was meant to prevent is what a viewer actually
sees. A liberties register that asserts what a visitor perceives must be checked against a
render, or it becomes a record of intent rather than of effect.
**How to resolve:** an atmosphere that is wavelength- and altitude-dependent rather than a
single exponential would haze a six-mile treeline and a 1400 m skirt differently on physics
instead of by exemption, and would let both L17 and § 1.6 hold at once. Failing that, replacing
the skirt with real terrain to the east removes L17's need for a closed horizon, and the cap can
then be argued on its own merits.
**Recorded:** 2026-08-10.

### L36 — The business street is built at an invented size, on purpose
**Decision:** the footprints of the South Water Street and Lake Street commercial buildings —
`peck_store`, `chicago_democrat_office`, `harmon_loomis_store`, `madore_beaubien_house`,
`bates_auction_room`, `jb_beaubien_homestead`, `dole_warehouse_south`,
`carpenter_south_water_store`, `chicago_american_office`, `frederick_thomas_shop`,
`old_bank_building` and `pruyne_kimball_drugstore` — are
invented polygons tagged `conjectural`, citing no source. Several of their **storey counts** are
invented too, and one of them, Frederick Thomas's shop, has an invented **position** and an
invented **function** as well.
**Why:** the honest alternative was to leave the business street empty, and that is the worse
lie. This town's trade was its whole reason to exist — a county seat of some three thousand
people, 250 vessel arrivals in 1835 — and until now the model held eight buildings of which not
one was a store. What the sources give for these buildings is a name, a trade and usually a
street corner: Andreas records that Peck kept a two-storey frame store at South Water and
LaSalle, and the *Chicago Democrat* of 26 November 1833 states its own address in its own
imprint. **None of them gives a dimension.** No period map in this project shows a building
footprint, which is verified for both 1834 sheets. So a footprint here is a guess by
construction, and the only question was whether to make it visibly or by omission.
One real constraint does apply and is used: **South Water lots are 55 ft wide**, which caps the
frontages rather than fixing them.
**Consequence:** the visitor walks a street whose buildings are the right buildings, in the
right places, at the wrong sizes. Turn the confidence view on and the whole row dithers, which
is the correct answer and an unusually honest picture of what this project knows about
commercial Chicago: **who** and **where**, almost never **how big**. Do not measure anything
off this street. The distance between two of these buildings is the distance between two
attested corners, which is real; the buildings spanning it are not.
**How to resolve:** a dimension for any single one of them upgrades that one and nothing else.
The most likely source is the *Chicago Democrat* itself — an advertiser describing his own
premises, or a to-let notice giving a size. The project holds one issue and more is expected.
**Covers:** `peck_store.footprint`, `chicago_democrat_office.footprint`,
`harmon_loomis_store.footprint`, `madore_beaubien_house.footprint`,
`bates_auction_room.footprint`, `jb_beaubien_homestead.footprint`,
`dole_warehouse_south.footprint`, `carpenter_south_water_store.footprint`,
`chicago_american_office.footprint`, `frederick_thomas_shop.footprint`,
`old_bank_building.footprint`, `old_bank_building.position`,
`pruyne_kimball_drugstore.footprint`, `pruyne_kimball_drugstore.position`,
`pruyne_kimball_drugstore.form.stories`,
`old_bank_building.form.stories`,
`chicago_american_office.form.stories`, `dole_warehouse_south.form.stories`,
`frederick_thomas_shop.form.stories`, `frederick_thomas_shop.position`,
`frederick_thomas_shop.function`.
**Recorded:** 2026-08-10.

### L37 — A shop placed by the phrase "two doors from"
**Decision:** `frederick_thomas_shop` stands on South Water Street with its position, its
function, its storey count and its footprint all tagged `conjectural`. It is the least-evidenced
building in the model.
**Why:** everything this project knows about it is an 1835 advertisement placing it "two doors
from the American office" — and the American office is itself only located "near the
draw-bridge". So the shop is positioned relative to a building that is positioned relative to a
bridge. Each step is attested and the compounded result is a guess: "two doors" assumes a lot
width and a continuous frontage, neither of which is recorded for that block. Its trade is not
stated either, so even what the building was *for* is inferred from the fact that a man
advertised from it.
**Consequence:** this record exists to make a point the empty-lot alternative cannot. The
business street was continuous — shops stood two doors from other shops — and a model that
draws only the buildings whose corners are documented shows a row of isolated structures with
gaps between them that never existed. That gap is a false statement too, and a less visible one.
**How to resolve:** an advertisement giving a block, or a lot number in a deed.
**Recorded:** 2026-08-10.

### L38 — The South Branch bridge lands on ground that is not there
**Decision:** `south_branch_raft_bridge` does not reach the terrain at either end.
**Why:** the same admission L30 already makes for the North Branch bridge, for the same reason
and with the same cause. The bridge is placed and dimensioned from the traced 1834 waterlines,
which is real evidence about where the water was; the ground it should land on is the terrain
heightfield, which is modelled from a zone table and does not carry a graded approach. Neither
is wrong on its own, and the model still shows a bridge arriving nowhere.
**Consequence:** a visitor who walks to either end steps off the deck. Because both branch
bridges now do this, it reads as a characteristic of the model rather than a defect in one
record, which is if anything worse — it makes the crossing look deliberate.
**How to resolve:** approach embankments, which are terrain work rather than structure work,
and which nothing in the sources describes for either bridge.
**Covers:** `south_branch_raft_bridge.log_1833.ground_contact`.
**Recorded:** 2026-08-10.

### L39 — Chicago's first movable bridge, with the moving part left out
**Decision:** `dearborn_street_drawbridge` is built as a fixed timber crossing. Its **draw span**
and its **gallows frames** are recorded on the record and declared `geometry: absent`; its
overall length is declared `simplified`; its width, its pier count and its pier kind are
`conjectural`; and like both branch bridges it does not reach the ground at either end.
**Why:** the draw is the entire historical point of this structure — it is the first movable
bridge in Chicago, built 1834, and what a contemporary would have told you about it is that it
opened. What the sources give is that it was "about 300 feet" long with a "**60 foot**" opening,
of "gallows pattern", with frames at either end, and hoisted. That is enough to know a draw
existed and roughly how wide; it is not enough to build the mechanism. Nothing describes how the
leaves were framed, what carried the hoist, where the windlass or capstan stood, or whether the
opening was one leaf or two. Modelling it would mean designing a machine and attributing it to
1834 Chicago.
**A correction is embedded here and worth stating**, because it is how the omission got its
shape: this project briefly held that the bridge was double-leaf and chain-hoisted. Neither is
attested. Both descriptions were lifted from the same web page's account of the **1890s–1963
bascule bridges** on the same street, sixty years later. The words "double-leaf" and "leaves"
occur on that page only there. Had the mechanism been modelled from that reading, the model
would have carried a late-Victorian bascule in an 1834 scene, which is exactly the failure mode
this file exists to catch.
**Consequence:** a visitor sees a long low timber bridge and no reason to think it was ever
anything else. The one fact that made this structure remarkable in its own town is the fact the
model does not show. The 60-foot gap in the deck is not drawn either, so the crossing reads as
continuous when it was not.
**Evidence since, 2026-08-11:** the frames are **built**. `bridge_timber` grew a draw — the
sixty-foot opening now clears four invented supports out of itself and stations two gallows
frames at its ends — on the argument that a dithered translucent frame says "this shape is ours"
in a way no footnote can, while an absent one tells a visitor the town's one piece of
engineering was a plain causeway. What is still missing is the *mechanism*: no leaf, no hinge,
no tackle. The draw is built **closed**, which is the only state agnostic between the three
arrangements the sources permit. `gallows_height_m` is conjectural and carries the whole frame's
confidence, so the most conspicuous object on the crossing is the one the confidence view
dithers hardest.
**How to resolve:** any description of the draw's framing or its hoist — a repair contract, a
council order, an engraving. The bridge was repaired in 1835, so a repair record is the most
likely thing to exist.
**Covers:** `dearborn_street_drawbridge.draw_1834.footprint`,
`dearborn_street_drawbridge.draw_1834.form.draw_lifting_gear`,
`dearborn_street_drawbridge.draw_1834.form.gallows_height_m`,
`dearborn_street_drawbridge.draw_1834.form.overall_length_m`,
`dearborn_street_drawbridge.draw_1834.form.pier_count`,
`dearborn_street_drawbridge.draw_1834.form.pier_kind`,
`dearborn_street_drawbridge.draw_1834.form.width_m`,
`dearborn_street_drawbridge.draw_1834.ground_contact`.
**Recorded:** 2026-08-10.

### L36a — Thomas Church's store: a building placed by a street and one sentence
**Decision:** `thomas_church_store` stands on Lake Street with its **position** and its
**footprint** tagged `conjectural`, and it is declared `outside_modelled_ground`.
**Why:** the entire evidence is one sentence in an uncredited editorial addendum on a
chicagology map-gallery page — *"The first store building on Lake Street, a two-story frame
structure, was built by Thomas Church."* That gives a **form** and a **street**, and no year,
block, lot, corner or dimension. The page's surrounding sentences run 1833, 1835, 1837, which
invites a date the sentence does not give; the project's own source record for that page grades
the addendum the weakest text in its set and says it must never outrank Andreas. So the storey
count and the material are documented and everything spatial is invention: the block, the side
of the street and the point along it were chosen to avoid the Lake Street buildings this dataset
knows the corners of and has not yet modelled — the Tremont House, the Mansion House, the
Exchange Coffee House, First Presbyterian, St Mary's. **Placing a record where there is room is
a rendering decision, not a finding**, and it is written on the record so a visitor can recover
it. The 55 ft lot cap that constrains the South Water frontages is a South Water figure and is
not evidence about Lake Street, so no cap is claimed here.
**Consequence:** the along-street uncertainty is the whole of Lake Street inside the town,
roughly 700 m, and the side of the street is a coin toss. The building is right; the lot is
ours. It also stands beyond the modelled terrain box, on the radial skirt of L17, for the same
reason as every record L40 covers.
**How to resolve:** Andreas at page-image level for any mention of Thomas Church, which would
outrank the addendum on this project's own grading; or a *Chicago Democrat* advertisement giving
Church's address. A date is the more urgent half — **if the store is 1835 work it may not have
stood on 1835-07-01, and the record then belongs in `data/exclusions.json` rather than in the
scene.**
**Covers:** `thomas_church_store.frame_1834.footprint`,
`thomas_church_store.frame_1834.position`.
**Evidence since, 2026-08-11:** the ground_contact token is withdrawn. This entry said the
store stood beyond the modelled box on L17's radial skirt; S2e has since built the ground
under it. The invented block, side of street and point along it are untouched.
**Recorded:** 2026-08-11.

### L47 — Fort Dearborn's stockade: the plan is evidence and the wall is not
**Decision:** the fort's picket line is built at an invented height, out of invented posts, with
an invented gate opening and invented corner works. Its **plan** — a square, two gates north and
south, bastions at the north-west and south-east angles, a block-house at the south-west — is
`documented` or `inferred` from three sources that agree; its **fabric** is entirely ours.
**Why:** the whole of the physical description this project could find is one adjective. Juliette
Kinzie, living inside it in 1831: *"The fort was inclosed by high pickets, with bastions at the
alternate angles. Large gates opened to the north and south."* Andreas adds "a square stockade"
and the two gates. The 1830 Harrison plan draws the outline. **Nobody wrote down how high the
pickets were, how wide they were, how close they stood, how wide the gates opened or how far the
bastions projected**, and Quaife — who wrote the standing monograph on this fort and had the War
Department files — gives no dimension of the 1816 work anywhere. So twelve feet, a ten-inch face,
a hand's gap, a twelve-foot gate and a seven-metre bastion are all this project's arithmetic
wearing plausible numbers.
**The one that matters most is the height.** A stockade's height is what a visitor reads the
building by: at three metres it is a compound, at four it is a fort. The confidence view dithers
it, which is exactly right and is the only thing standing between a viewer and a number we
invented from an adjective.
**Consequence:** the fort's silhouette — the thing anyone would photograph — is ours. So is the
gap between the posts, which decides whether you can see through the wall.
**How to resolve:** any quartermaster return, repair estimate or engineer's report for the post
between 1816 and 1836. A picket count or a quantity of timber would settle the height and the
spacing together.
**Covers:** `fort_dearborn_palisade.picket_1816.form.picket_height_m`,
`fort_dearborn_palisade.picket_1816.form.picket_width_m`,
`fort_dearborn_palisade.picket_1816.form.picket_spacing_m`,
`fort_dearborn_palisade.picket_1816.form.gate_width_m`,
`fort_dearborn_palisade.picket_1816.form.bastion_length_m`,
`fort_dearborn_palisade.picket_1816.form.bastion_projection_m`,
`fort_dearborn_palisade.picket_1816.form.posterns`.
**Recorded:** 2026-08-11.

### L42 — The fort's buildings stand at heights, under roofs and behind stacks nobody recorded
**Decision:** across the six modelled buildings inside Fort Dearborn, the **storey counts** of
the officers' quarters and the barracks, the **wall heights** of the block-house, the magazine,
the artillery house and the root house, every **roof form and pitch** that is not a plain gable
by type, the block-house's **jetty**, its **loopholes** and its **stack**, and the deliberate
**absence of galleries** on the two long ranges are all invention.
**Why:** two witnesses walked round the inside of this fort and wrote down what stood where —
Gurdon Hubbard in 1827 and the key to the 1855 photograph — and between them they give one
building's dimensions, one building's material twice, and nothing at all about height, roof or
chimney for anything. The 1830 plan is a plan: it has no third dimension. What fills the gap here
is building type, which is a real argument and not evidence: a magazine has no windows, a
block-house has a jettied upper storey and loopholes because that is what the word means, and a
barracks for two companies does not fit on one floor of a ninety-foot range.
**The galleries are the subtlest of these and they are a decision, not an omission.** Captain
Whistler's 1808 index for the FIRST fort says its barracks were *"two storeys high with shingled
Roofs and Galliaries fronting the parade"*. Nothing says the 1816 fort's ranges had them, and
John H. Kinzie says the two forts were "differently constructed". So the ranges are built with
plain fronts, which renders as a claim — a visitor sees flat elevations facing the parade — made
because the evidence for the alternative belongs to a building that burned in 1812.
**Consequence:** the fort's massing is ours. Roof heights set the skyline of the whole complex,
and a two-storey barracks against a one-storey one changes the scene from across the river.
**How to resolve:** the same records that would settle the stockade — returns, repair estimates,
the Chicago Democrat's building notices — or any measured elevation of the fort before 1856.
**Covers:** `fort_dearborn_officers_quarters.log_1816.form.stories`,
`fort_dearborn_officers_quarters.log_1816.form.gallery`,
`fort_dearborn_barracks.log_1816.form.stories`,
`fort_dearborn_barracks.log_1816.form.gallery`,
`fort_dearborn_blockhouse.log_1816.form.wall_height_m`,
`fort_dearborn_blockhouse.log_1816.form.upper_overhang_m`,
`fort_dearborn_blockhouse.log_1816.form.loopholes`,
`fort_dearborn_blockhouse.log_1816.form.roof_type`,
`fort_dearborn_blockhouse.log_1816.form.roof_pitch_deg`,
`fort_dearborn_blockhouse.log_1816.form.chimneys`,
`fort_dearborn_magazine.brick_1816.form.wall_height_m`,
`fort_dearborn_magazine.brick_1816.form.roof_type`,
`fort_dearborn_artillery_house.log_1816.form.construction`,
`fort_dearborn_artillery_house.log_1816.form.stories`,
`fort_dearborn_artillery_house.log_1816.form.wall_height_m`,
`fort_dearborn_artillery_house.log_1816.form.roof_type`,
`fort_dearborn_artillery_house.log_1816.form.roof_pitch_deg`,
`fort_dearborn_root_house.cellar_1816.form.wall_height_m`,
`fort_dearborn_root_house.cellar_1816.form.roof_type`.
**Recorded:** 2026-08-11.

### L43 — Three things inside and beside the fort are placed by a sentence, a side, or nothing
**Decision:** the **magazine's outline**, the **artillery house's outline and position**, and the
**root house's outline and position** are invented. All three are built anyway.
**Why:** they are three different grades of thin and it is worth separating them, because the
model shows all three the same way. The **magazine** has the best-attested position in the fort —
Hubbard, 1827: *"the magazine, of brick, was situated about half way between the west end of the
guard and block-houses"* — and the 1830 plan does not draw it, so its size is a powder magazine
for a two-company post and nothing more. The **artillery house** is named once, by Robert Fergus,
describing the fort in **1850**, on a side of the parade the 1830 plan has already filled with
the barracks; its position is the one part of that side the plan leaves empty and its size fits
the gap. The **root house** rests on one sentence of Juliette Kinzie's putting the garrison's
root-houses on the river bank west of the fort in 1831, with no number, no size and no point on
that bank — and her plural is not modelled either, because a count invented on top of a position
invented is two inventions.
**Consequence:** a visitor walking the fort sees three structures whose outlines are ours. The
artillery house is the one to distrust most: it is placed inside a documented enclosure on the
authority of a description written fifteen years after the army left.
**How to resolve:** an inventory, a plan of the fort later than 1830, or the Chicago Democrat's
notices. Any of the three would move at least one of these to `inferred`.
**Covers:** `fort_dearborn_magazine.brick_1816.footprint`,
`fort_dearborn_artillery_house.log_1816.footprint`,
`fort_dearborn_artillery_house.log_1816.position`,
`fort_dearborn_root_house.cellar_1816.footprint`,
`fort_dearborn_root_house.cellar_1816.position`.
**Recorded:** 2026-08-11.

### L44 — The 1832 lighthouse: one documented number and an invented tower
**Decision:** `chicago_lighthouse_1832` is built as a tapering twelve-sided masonry shaft with a
gallery and a lantern, standing about 65 m north-west of the fort. Its **height** is documented
and its **lantern** is documented; its **footprint**, its **position**, its **taper**, its cap
and its finish are ours.
**Why:** Andreas gives the whole of it in one sentence — *"Another tower, forty feet high, was
begun and completed by Mr. Jackson in 1832. It boasted of a fourteen-inch reflector."* — and the
lighthousefriends page adds four fourteen-inch reflectors in a bird-cage lantern room. **That is
all.** No diameter, no wall thickness, no plan, no material and no distance from the fort.
**A correction is embedded here, and it is the reason this entry exists.** This project's own
dossier reads the 1832 tower as *"forty feet high; conical stone/masonry"* and tags it
`[DOC]`, and `data/exclusions.json` calls it "the 1832 conical masonry tower" on Andreas's
authority. Neither "conical" nor "masonry" is in Andreas's sentence or on the lighthousefriends
page. The only fabric detail either source carries — *"The walls were three feet thick"* and a
height of fifty feet — belongs to the **first** tower, the one that collapsed unfinished on 30
October 1831. So the shape everybody repeats about this lighthouse is a description of a building
that fell down. The record grades the material `inferred` on a real argument (Samuel Jackson
built both towers under the same appropriation on the same site, and the first was masonry) and
the shape `conjectural`, and the taper this archetype builds is admitted here.
**Consequence:** the most distinctive small object at the river mouth is a shape we chose. Its
position is worse: adjacency to the fort is documented three ways and the offset is a bearing and
a distance we picked.
**How to resolve:** the Light-House Board's annual reports, a keeper's return, or any of the
several 1840s and 1850s views of the fort — the tower stands in the 1850 daguerreotype and the
1855 photograph, and a measured reading of either would settle the shape at once.
**Covers:** `chicago_lighthouse_1832.tower_1832.footprint`,
`chicago_lighthouse_1832.tower_1832.position`,
`chicago_lighthouse_1832.tower_1832.form.roof_type`,
`chicago_lighthouse_1832.tower_1832.form.paint`.
**Recorded:** 2026-08-11.

### L45 — The garrison garden: a fence read from a drawing convention, and a planting not drawn
**Decision:** `fort_dearborn_garrison_garden` is built as a worm rail fence round a square of
about 77 m. The fence's **height, its courses, its panel length and its zigzag** are invented,
and the **planting inside it is documented and not built at all**.
**Why:** the 1830 Harrison plan draws this plot and labels it "Garden for the Garrison", and it
draws two of its sides as a continuous zigzag. A zigzag boundary on a period American survey is
the convention for a worm — snake — rail fence, so that is what is built; but the convention is
the reading and the sheet never says "fence", which is why `wall_kind` is `inferred` and every
dimension of the fence is `conjectural`. The planting is the opposite case and the sharper one:
Juliette Kinzie says the company gardens were *"well filled with currant-bushes and young
fruit-trees"*, which is `documented`, and **nothing of it is modelled**, because currant bushes
and fruit trees are flora and `data/flora/` has no cultivated zone and no garden species. So the
record carries a documented chip over an empty rectangle of ground.
**A guard belongs here too.** The garden usually quoted in accounts of this fort — *"The ground
on the south side was enclosed and cultivated as a garden"* — is from a passage that ends *"Such
was the old Fort previous to 1812"*. It is the FIRST fort's garden and this record does not rest
on it.
**Consequence:** the reservation reads as fenced, empty ground. The single most evocative
detail anyone recorded about this place — fruit trees in a garrison garden on the Chicago
prairie — is in the data and invisible in the model.
**How to resolve:** a cultivated-ground zone in `data/flora/`, which is a flora parcel rather
than a structure one; the species are already named by the source.
**Covers:** `fort_dearborn_garrison_garden.fence_1816.form.fence_height_m`,
`fort_dearborn_garrison_garden.fence_1816.form.rail_courses`,
`fort_dearborn_garrison_garden.fence_1816.form.panel_length_m`,
`fort_dearborn_garrison_garden.fence_1816.form.panel_offset_m`,
`fort_dearborn_garrison_garden.fence_1816.form.planting`.
**Recorded:** 2026-08-11.

### L46 — The fort stands on a bank the model has no cut or fill for
**Decision:** the **stockade** and the **commandant's quarters** stand clear of the terrain on
their north sides — 1.40 m and 0.46 m at the worst point — and are declared
`approach_not_modelled`. No cut, fill, revetment, platform or foundation is modelled anywhere in
the complex.
**Why:** the fort sits on a plateau at about 3.33 m that falls away to the river between local
N +245 and N +270, which is what a fort on a river bank inside a bend should do. The north wall
of the stockade and the north face of the brick range cross the top of that fall, and the
archetypes build a level base at one elevation. The real work plainly had something under it —
a picket line is set in a trench and a brick range needs footings — and no source reached
describes either.
**Consequence:** walk round to the river side of the fort and the pickets stand up out of the
slope on nothing. It is the honest picture of two things at once: a fort correctly placed on a
bank, and a model with no earthworks in it.
**How to resolve:** a levelled section of the bank, which no source gives; or terrain work that
models the platform the fort stood on, which is a terrain parcel rather than a structure one.
**Covers:** `fort_dearborn_palisade.picket_1816.ground_contact`,
`fort_dearborn_commandants_quarters.brick_1816.ground_contact`.
**Recorded:** 2026-08-11.
**Revised:** 2026-08-11, hours after it was written, and the revision is the good kind. This
entry was originally titled *"The fort stands 832 m beyond the modelled ground, and nothing
could see it"* and covered the **ground contact of all fourteen** structures in this complex,
because the `e1834_harbor_cut` heightfield stopped at local E +320 and the fort is at E +1152.
**S2e parcel (b) landed while this parcel was being written** — the field now reaches E +1700 —
so twelve of the fourteen simply land, their declarations are gone from the records, and the two
that remain fail for a completely different and much more interesting reason, which is what the
entry above now describes. Two of the twelve had to move to get there: the **lighthouse** and
the **root house**, whose positions were always `conjectural`, had been put where no ground
existed to contradict them and turned out to be standing in the channel; both moved onto the
bank top and both notes say so.
**The half of the original entry that is NOT superseded, because it is about the machinery and
not about the ground.** `tools/heightfield.py` clamps outside the box, so while the fort was 832
m past the edge it sampled the clamped edge for its base AND for every point of its outline, the
two agreed to the millimetre, and the ground-contact gate — the gate this project wrote
specifically to catch a building standing on nothing — reported a **perfect landing**. Every
structure L40 covers was caught only because the clamped edge varies along a wall and produced a
gap; the fort was far enough out and square enough on to produce none. The gate could see
buildings that were nearly right and was blind to the one that was completely wrong.
`Heightfield.covers()`, the `outside_modelled_ground` state and the two-way check that a
declaration matches the measurement were written for that and stay whether or not any structure
currently needs them — and turning them on immediately flagged two structures in other parcels
that nothing had caught. See `docs/STATUS.md` § "Known weaknesses" 0a.

### L41 — The harbour piers are a measured line, an interpolated length and an invented width
**Decision:** `north_pier` and `south_pier` are drawn as timber crib lines 900 ft and 400 ft
long and **25 ft wide**. The bearing and the landward root of both are measured off Wright
1834; the length of both is an **interpolation between two year-end figures**, recorded
`inferred` on `form.length_m`; the width of both is **the archetype's own constant**, recorded
`conjectural`, and it carries the footprint down with it.
**Why:** the sheet that gives the line cannot give the width. Wright 1834 draws the harbour as
two red pier lines with HARBOR lettered between them, and read through this project's own
fitted affine the two run at 103.4 and 103.5 degrees from grid north and stand 64.2 m apart —
against a documented 200 ft entrance, which is 61.0 m, a four-per-cent agreement from evidence
that shares no input. That is a good measurement of a **line**. But the sheet is drawn at about
1:7,200, where a 25-ft crib is 0.13 mm of paper and about a fifth of the width of the pen that
drew the pier: the red bands are line weight and carry no thickness at all, so measuring one
would be measuring the draughtsman's nib. No text reached states a width either. 25 ft is this
archetype's number, kept as a single constant in `pier_crib_params.DEFAULT_WIDTH_M` so that
both piers inherit **one** invention a reader can find in one place rather than two that could
drift apart.
**The length is a different kind of not-knowing and is graded differently.** No source gives a
length for any date inside the 1835 season; what exist are year-end figures — north 700 ft
(end 1834) to 1,260 ft (end 1835), south 200 ft to 700 ft — and 1 July is placed between them
on a season-weighted rather than a calendar reading, at 900 ft and 400 ft, inside the bands
`docs/research/04-structures-south.md` §3 reaches independently. That is `inferred` with the
arithmetic written out, not `conjectural`, and it is not claimed here. What is claimed is the
**drawn shape**, which is graded by its weaker axis.
**A third invention rides along and is claimed here too:** the cribs are drawn as equal
30-ft modules (`pier_crib_params.CRIB_MODULE_FALLBACK_M`). Nobody recorded a crib length, and a
pier built out over several seasons in fact ends where a season ended, not on an even module.
**Consequence:** a visitor sees two piers of a definite length and a definite width, and only
their direction and their starting point are evidence. The confidence view renders both as
massing, which is right, and cannot say that one of the two axes is much better known than the
other — only this entry can. Nothing should be read off how far out they run.
**How to resolve:** the Chief Engineer's annual report for 1835 or the House Document series
would replace the interpolated length with a figure (`docs/research/01-terrain-hydrology.md`
already names them as the thing to find). For the width, J. D. Graham's 1857 and 1858
hydrographic surveys of the Chicago bar draw the piers in plan at a usable scale, or any
specification or voucher for the crib work.
**Covers:** `north_pier.crib_1835.footprint`, `north_pier.crib_1835.form.width_m`,
`south_pier.crib_1835.footprint`, `south_pier.crib_1835.form.width_m`.
**Recorded:** 2026-08-11.

### L51 — The north bank is drawn at invented sizes, and the confidence view cannot say so
**Decision:** the footprints of the seven north-bank and Wolf Point structures added on
2026-08-11 — `cobweb_castle`, `blacksmith_shop_state_st`, `miller_tannery`,
`north_side_school_1833`, `steamboat_hotel`, `council_house` and `robinson_caldwell_cabins` —
are invented polygons tagged `conjectural`, citing no source. The North Side school house's
**construction** is invented too.
**Why:** the same argument L36 makes for the business street, one bank north. What these sources
give is a name, a use, a year and usually a street: *Wau-Bun* describes Cobweb Castle's
composition and never its size; Andreas gives the tannery a direction, the school a side of
Clark Street, the smithy a proximity and the hotel a street, and **not one of them gives a
dimension**. No period map in this project draws a building footprint, which is verified for
both 1834 sheets. So a footprint here is a guess by construction and the only question was
whether to make it visibly or by omission. One polygon carries real evidence in its **shape**
and none in its size — Cobweb Castle's centre, two wings and two tails is *Wau-Bun*'s sentence
drawn — and that distinction is stated in its own footprint note.
The school's `construction` is a preference between two readings rather than a derivation: log
keeps it with the older north-bank fabric, and the nearest building anybody dated is frame — the
Methodist meeting house contracted for "a frame building twenty-six by thirty-eight feet" at
North Water and Clark on 30 June 1834, one block away and a year later. Choosing log also chose
the archetype, so if it is wrong the building is wrong in kind.
**Consequence, and it is worse here than on the business street.** `log_dwelling` computes its
wall massing's `_CONFIDENCE` from `stories` and `construction` only — **not from `footprint`** —
so a building whose every dimension is invented renders at the confidence of its storey count.
`miller_tannery` is the clean case: its footprint is a placeholder and the whole building shows
`0.5`, inferred. **Turning the confidence view on does not reveal an invented footprint on any
log building in this dataset.** The `_CONFIDENCE` worked example in docs/GLB-CONTRACT.md says
the footprint should drive it; the archetype does not. Until that is fixed and the town re-baked,
this entry is the only place a visitor can learn it.
**How to resolve:** a dimension for any one of them upgrades that one and nothing else. The
likeliest source is the *Chicago Democrat* and the *Chicago American* — Davis advertised the
Steamboat Hotel in the latter, and hotel advertisements of the period describe premises. The
archetype half is a one-line change plus a re-bake of every log building.
**Covers:** `cobweb_castle.log_1820.footprint`,
`blacksmith_shop_state_st.log_1823.footprint`,
`miller_tannery.log_1831.footprint`,
`north_side_school_1833.log_1833.footprint`,
`north_side_school_1833.log_1833.form.construction`,
`steamboat_hotel.frame_1835.footprint`,
`council_house.log_1834.footprint`,
`robinson_caldwell_cabins.log_1831.footprint`.
**Recorded:** 2026-08-11.

### L54 — Cobweb Castle: the one building anybody described, built as a box
**Decision:** the Indian Agency house is modelled as a plain rectangular log mass under a gable
roof. Its attested **plan** — "a centre, two wings, and, strictly speaking, two tails" — is
recorded as `plan_composition`, drawn in the footprint polygon, and declared
`geometry: "absent"`. Its attested **cladding**, "clapboarded part way up", is declared
`geometry: "simplified"`. Its `roof_type` is tagged `conjectural` although a gable is built.
**Why:** this is the best-described building on the north bank and the archetype can express
almost none of it. `log_dwelling` masses the footprint polygon's **bounding box**, so the cross
this record draws — a centre projecting one metre forward of two flanking wings, with two tails
running back from the rear — comes out as a 13 × 9 m rectangle with the re-entrant corners filled
in. The same limitation L27 records for Miller's L-shaped plan, on the building where it costs
most. The roof follows from it: *Wau-Bun* says the hours were passed "under its **odd-shaped
roof**", which is what a centre with two wings and two tails produces, and one gable is the
opposite of that — so the value is a substitution and is graded as one rather than passed off as
a reading. The clapboarding is a documented finish on a log wall that the archetype paints as
bare hewn log (L22's finding, on a record L22 does not name).
**Consequence:** the visitor walks past a box. Everything a reader would recognise this building
by — the wings, the tails, the comical adjuncts a platted street exposed, the boards taken part
way up the wall — is in the record and not in the model. The confidence view marks the mass
`1.0` because the roof is conjectural, which is right by accident: it is the plan that is
missing, and the tint cannot say which.
**How to resolve:** an archetype that extrudes the polygon rather than its bounding box would
build the plan this record already draws, from data already committed. That is a geometry change
and a re-bake, not a research problem.
**Covers:** `cobweb_castle.log_1820.form.plan_composition`,
`cobweb_castle.log_1820.form.cladding`,
`cobweb_castle.log_1820.form.roof_type`.
**Recorded:** 2026-08-11.

### L53 — The Steamboat Hotel: a documented hotel with an entirely invented fabric
**Decision:** `steamboat_hotel` is built as a two-storey braced-frame block, 15 × 8 m, unpainted,
gable-roofed, with no gallery — and **every one of those values is tagged `conjectural`**,
including the construction, which is also what chose the archetype.
**Why:** two sources give this house a street, a cross-street, a year and a keeper, and not one
word about its fabric, size, plan, storeys or finish. Andreas: "The Steamboat Hotel, on North
Water Street, near Kinzie, was kept in 1835 by John Davis." That is the whole of it. Frame was
chosen because every Chicago hotel this dataset can date to 1833 or later is frame — the Green
Tree of 1833, the Western of 1834, the Tremont of 1833 — while the log taverns at the forks all
belong to the 1828-31 generation. But this project's own line, set in L18, is that **the ordinary
reading of a type is not evidence about a building**, and nobody described this one. `paint` and
`gallery` are recorded rather than omitted for a reason worth keeping: the archetype's defaults
are white paint and no gallery, so leaving them out would have made both claims silently, and
white paint on an 1835 house is a claim *Wau-Bun* shows was worth remarking on in 1831.
**Consequence:** the whole building renders as dithered massing in the confidence view, which is
the correct answer and an unusually honest one — this is what the project knows about a hotel it
can name, date and staff. **Do not read anything off its elevation.** And note the compounding
risk: if the frame reading is wrong the building is wrong in kind, not in detail, because a log
reading would move it to a different archetype.
**A second admission belongs with it.** The date is inferred, not documented. Both sources say
1835 and neither gives a month; every dated anchor — the 8 June 1835 first issue of the paper
Davis advertised in, the 9 November 1835 change of management — falls **after** the scene date.
The record argues the case on `documented_range` and says that a dated advertisement putting the
opening after 1 July sends it to `data/exclusions.json`.
**How to resolve:** the *Chicago American* and the *Chicago Democrat*. An advertisement would
plausibly settle the fabric, the size and the opening date in one document.
**Covers:** `steamboat_hotel.frame_1835.form.construction`,
`steamboat_hotel.frame_1835.form.stories`,
`steamboat_hotel.frame_1835.form.wall_height_m`,
`steamboat_hotel.frame_1835.form.roof_type`,
`steamboat_hotel.frame_1835.form.paint`,
`steamboat_hotel.frame_1835.form.gallery`.
**Recorded:** 2026-08-11.

### L52 — Two buildings placed inside bands, and two or three cabins built as one
**Decision:** `council_house` and `robinson_caldwell_cabins` carry `conjectural` positions —
points chosen inside stretches a source bounds but does not narrow — and the cabins are built as
**one** cabin where the source counts "two or three".
**Why:** the council house is located by a single sentence in a 1910 newspaper recollection: "on
the north side of the river, **east of the present State street and west of the 'Lake House'**".
That is a 215 m stretch of riverbank, and no other source narrows it, so the along-bank position
is good to about **±110 m** — five times the georeference's own uncertainty and the largest
positional error in this dataset. The cabins are located by *Wau-Bun*'s row order alone — the
tavern, then "near him" the cabins, then "a little remote" the log meeting house — between two
neighbours that are themselves placed from bank geometry, one of which (`walker_meeting_house`)
may be on the wrong bank entirely. The count is the source's own hedge: "two or three log cabins
occupied by Robinson, the Pottowattamie chief, and some of his wife's connexions". Building two
or three would mean inventing the number *Wau-Bun* declined to give, plus their spacing and
arrangement, so the record keeps the words as the value, declares `geometry: "simplified"`, and
builds one.
**Consequence:** for both, the sidecar's flat `uncertainty_m: 20` is wrong by a large factor —
the same understatement L7 records for the Wolf Point three, worse. A visitor sees a council
house standing on a specific spot that no source puts it on, and sees one cabin where at least
two stood. Neither is visible in the confidence view: the tint grades a value, not a place, and
it cannot render a building that should have been two.
**Both records are flagged `review_required: true`** and that is not a liberty, it is the
standing constraint in `AGENTS.md`. The council house is where the assembly of 18 August 1835
formed; the cabins were the homes of Potawatomi people in the year of the removal. This project
models the built environment and asserts nothing about presence, occupancy or events, and the
flag holds the scene short of `released` until someone qualified has read the records.
**How to resolve:** for the council house, any source naming a street, a corner or a lot — the
*Chicago Democrat*'s notices of agency business, or the corrected 1835 Wabansia and Kinzie's
Addition plat. For the cabins, any source that follows them past 1831: the 1833 treaty's
schedules of improvements and claims are the likeliest.
**Covers:** `council_house.log_1834.position`,
`robinson_caldwell_cabins.log_1831.position`,
`robinson_caldwell_cabins.log_1831.form.cabin_count`.
**Recorded:** 2026-08-11.

### L55 — The town's three worship buildings wear a dwelling's facade
**Decision:** the First Presbyterian Church, St. Mary's and the Temple Building are all built
with the `frame_dwelling` archetype, which puts the door in the long eaves-front wall and sets
the openings out on a house's bay module. `plan` and `bays` are tagged `conjectural` on all
three.
**Why:** the schema offers an `institutional` archetype and there is no generator behind it, so
a record using it compiles a sidecar pointing at a GLB that does not exist and the building is
invisible. Of the archetypes that do build, `frame_tavern` carries a public house's gallery,
`frame_storefront` carries a shopfront, and `outbuilding` refuses a storey count — leaving
`frame_dwelling`, which is the only one that builds a plain single-range frame box with a gable
roof and nothing else. That is the right MASSING for all three buildings and the wrong FACADE
for all three.
**Consequence:** a visitor sees three plain frame boxes with a domestic front. `plan:
centre_passage` was chosen on each to force a centred door and a symmetrical elevation, which
is the nearest a house's grammar comes to a meeting house's; the archetype's own default,
`hall_parlour`, would have put the church door two thirds of the way along the wall. The bay
counts — five on the Presbyterian church, three on St. Mary's and the Temple Building — are
consequences of that choice and of the frontage, not findings. Nothing describes a window,
a door or an elevation on any of the three.
**A second cost, on St. Mary's only:** a 25 × 35 ft church almost certainly stood **gable-end
to the street**, and this archetype builds an eaves-front range only — the ridge always runs
parallel to the facade — so the 35 ft dimension becomes the Lake Street frontage by
construction. The building is turned ninety degrees from what its proportions imply. The
footprint note says so; the attribute is `inferred` rather than `conjectural` because both
dimensions are attested and only their assignment is not, so this entry claims the facade and
the footprint note carries the orientation.
**How to resolve:** an `institutional` (or `meeting_house`) archetype — a single-cell plan, a
gable-front option, a door in the gable end, a plain bench-lit side elevation — which would
serve all three buildings and any later church. Failing that, any depiction or description of
one of these elevations.
**Covers:** `first_presbyterian_church.frame_1834.form.plan`,
`first_presbyterian_church.frame_1834.form.bays`,
`st_marys_church.frame_1833.form.plan`,
`st_marys_church.frame_1833.form.bays`,
`temple_building.frame_1833.form.plan`,
`temple_building.frame_1833.form.bays`.
**Recorded:** 2026-08-11.

### L56 — Four documented interiors, and no interior is modelled
**Decision:** the pine-board benches seating about 200 and the plastered walls over bare
puncheon floors in the First Presbyterian Church, the rough benches and the table for an altar
in St. Mary's, and the division of Eliza Chappel's log house into a school-room and lodging
quarters are all recorded as `documented` and all declared `geometry: absent`.
**Why:** this project models exteriors. No structure in the dataset has an interior, and these
four are the first records whose best-attested facts are inside the building — which is the
situation the `geometry:` declaration exists for: without it the popup would show the strongest
confidence chip the project has over something a visitor cannot see.
**Consequence:** the three best sentences anybody wrote about these buildings are in the record
and not in the model. It matters more here than for a stable or a sign, because for a meeting
house the interior IS the building: what distinguishes the Presbyterian church from St. Mary's
is not their massing, which is within a few feet of identical, but that one was plastered with
benches for two hundred and the other was unplastered with rough benches and a table.
**One of the four does reach the mesh, indirectly, and that is worth saying:** the Chappel
house's attested division into two rooms is the reason its invented footprint is a two-room
size rather than a single pen. A number a human chose from a sentence is not the sentence
being built.
**How to resolve:** interiors, or a popup that renders the interior description alongside the
elevation. The second is much cheaper and would discharge most of what this entry admits.
**Covers:** `first_presbyterian_church.frame_1834.form.seating`,
`first_presbyterian_church.frame_1834.form.interior_finish`,
`st_marys_church.frame_1833.form.seating`,
`chappel_infant_school.log_1833.form.interior_division`.
**Recorded:** 2026-08-11.

### L57 — The Temple Building is sized by arithmetic on its own cost
**Decision:** the Temple Building's footprint is drawn at 30 × 25 ft, tagged `conjectural`,
and derived from the one quantitative fact anybody recorded about it — that it cost about $900.
**Why:** no source gives this building a dimension. It does give a cost, and this dataset now
holds two contemporary buildings whose cost AND area are both attested: the First Presbyterian
Church at $600 for 1,000 sq ft and St. Mary's at $400 for 875 sq ft, i.e. $0.60 and $0.46 per
square foot. Two storeys at the midpoint of that range buys about 1,600 sq ft of floor, so
about 800 per storey; 30 × 25 ft is 750, which at $0.55 gives $825 against the attested $900.
**Consequence:** a derivation with three numbers in it reads as a finding and is not one. Two
things are wrong with it in known directions and neither is corrected, because correcting a
guess with another guess is worse: the cost per square foot of a two-storey building is lower
than a single-storey one's — a second floor is cheap against a roof and a foundation — so the
real building was probably BIGGER than this; and both reference figures rest on the citation
problem set out in the Presbyterian church's research note, where the dossier's row cites
Wikipedia and Andreas together without saying which supplied the dimensions. The 25 ft depth is
additionally borrowed rather than derived: it is the depth of both churches and of the
rectangle four other records in this dataset already use.
**How to resolve:** any dimension at all, from a deed, an insurance entry, a subscription list
or Andreas at page-image level.
**Covers:** `temple_building.frame_1833.footprint`.
**Recorded:** 2026-08-11.

### L58 — Three buildings sized by what they were for
**Decision:** the log jail (20 × 15 ft), Eliza Chappel's log school house (24 × 18 ft) and the
Watkins house on Michigan Street (30 × 20 ft) are drawn at invented footprints, tagged
`conjectural`.
**Why:** no source reached gives any of the three a dimension, a plan or a room count. What
each does supply is a USE, and the sizes are read off that and nothing else: a jail described as
"something more metropolitan ... than the estray pen" and superseded within a few years is a
two-cell log lock-up; a log house "divided into school-room and lodging quarters" holds two
rooms, so it is bigger than a single pen and smaller than a public building; a house a
schoolmaster could take a class in one room of is an ordinary two-room dwelling.
**Consequence:** three buildings stand at three specific sizes that nobody recorded, and the
proportions are as invented as the areas. The repetition across the dataset is deliberate and is
the honest form of the admission — 24 × 18 and 30 × 20 recur here and elsewhere because they are
type sizes, not measurements, and a set of unrelated-looking numbers would hide that.
**How to resolve:** a county order or contract for the jail (which would carry a specification
as well as a size); the Kinzie's Addition plat and its early conveyances for the Watkins house;
Andreas at page-image level around scan pp. 305, 367 and 431 for all three.
**Covers:** `log_jail.log_1833.footprint`,
`chappel_infant_school.log_1833.footprint`,
`watkins_school_house.house_1833.footprint`.
**Recorded:** 2026-08-11.

### L59 — Two buildings placed in the middle of a block face
**Decision:** Eliza Chappel's log school house and the Watkins house on Michigan Street are
placed at the mid-point of the block face each is attested on, and their positions are tagged
`conjectural`.
**Why:** the evidence is a stretch of street and no more. Andreas puts the school house in "a
log house just outside the military reservation", which fixes it immediately west of State
Street — the reservation's western boundary on the south side until February 1835 — and this
project's dossier reads that as the two-block strip between South Water and Lake, tagging the
exact lot conjectural itself. Andreas puts the Watkins school "in a house on Michigan Street
between Cass and Rush", which is a block face about 110 m long. Neither source names a lot, a
corner or a side of a corner.
**Consequence:** each building stands at one specific point inside a run of frontage it could
have stood anywhere along. The error is not the georeference's ±20 m but the length of the
block: about ±60 m along State Street for the school house and about ±55 m along Michigan
Street for the Watkins house, and that is on top of the ±20 m and of an unknown setback from
the street line. A visitor sees two buildings sitting on specific lots. There are no lots.
**Why the midpoint rather than a corner:** a corner is a claim and the midpoint is the centre of
the distribution the evidence describes. It is still a point where the record has an interval.
**How to resolve:** the Kinzie's Addition plat and its conveyances for the Watkins house; any
1834–35 newspaper advertisement naming either address; Andreas at page-image level around scan
pp. 305 and 431, read for a street number or a neighbour rather than for the school.
**Covers:** `chappel_infant_school.log_1833.position`,
`watkins_school_house.house_1833.position`.
**Recorded:** 2026-08-11.

### L60 — The estray pen is a fence, and the model gives it a roof
**Decision:** Chicago's first public building — the estray pen on the south-west corner of the
public square — is built with the `outbuilding` archetype as a log-walled box 30 × 20 ft and
8 ft high, with a gate and **a shed roof at the shallowest pitch the generator will accept**.
Every one of those values is tagged `conjectural`.
**Why:** what the sources attest is a municipal FUNCTION, a corner and a month. A pound is an
enclosure; there is no reason to think this one was roofed and nothing mentions a roof. This
project has no generator that builds an enclosure — `palisade` is named in the schema and has no
module behind it — and `outbuilding`, the only archetype that will build a low walled rectangle,
cannot build a roofless structure. So the choice was a roofed box or no building at all, and the
working policy for this parcel is that an absent building is invisible while a conjectural one is
legible and correctable.
**Consequence:** the roof is the model's, not the record's, and it is the most conspicuous thing
about the structure. It is set to `shed` at 6 degrees — a 0.64 m rise over the pen's 6 m run, as
close to flat as the generator goes — which is a deliberate attempt to minimise a feature that
probably was not there rather than a finding about a roof that was. The material is invented too,
and the live alternative would look completely different: most frontier pounds were split-rail or
post-and-rail, which is open and horizontal and see-through, where this is a closed notched log
wall. The gate is a doorway in a wall where the real thing was probably a hung rail gate. What
survives of the evidence in the mesh is a rectangle of about the right size in about the right
place.
**How to resolve:** an enclosure archetype — post-and-rail or notched log, ROOFLESS, gated,
taking a perimeter rather than a footprint. It would serve this record, the fenced-or-unfenced
state of the public square itself, the garrison gardens and every yard in the town, and it is
the honest fix. A town or county order establishing the pound would settle the size and the
material at the same time.
**Covers:** `estray_pen.pen_1833.footprint`,
`estray_pen.pen_1833.form.construction`,
`estray_pen.pen_1833.form.roof_type`,
`estray_pen.pen_1833.form.roof_pitch_deg`,
`estray_pen.pen_1833.form.wall_height_m`,
`estray_pen.pen_1833.form.door`.
**Recorded:** 2026-08-11.

### L61 — The first court-house is built finished, on a date that may predate it
**Decision:** the first Cook County court-house is built on the public square as a completed
one-room wooden building 24 × 18 ft. Its position within the square and every attribute of its
form are tagged `conjectural`; only its existence, its year and its function are not.
**Why, and this is two admissions rather than one.**
**(1) The date.** `illinoiscourthistory` gives one sentence — "Cook County built their first
courthouse in 1835" — and a caption, "The first Cook County Courthouse, 1835–1853". **No source
fixes a month.** On 1835-07-01 the building may have been unbuilt, under construction, or newly
finished, which is exactly what `data/exclusions.json`'s watch_list already says about it. This
record models the third of those, which on a flat prior is about half likely. **Under
construction is a phase, not an omission**, and the honest alternative would be a second phase
carrying a frame-and-no-cladding state; it is not written because nothing dates the transition
and a construction phase with invented start and end dates would be two inventions where there
is now one.
**(2) The form, and the two descriptions that must never reach it.** The famous "about thirty by
sixty feet ... front ornamented with a four-column Doric portico of wood work" is Andreas on the
**1837** court-house. And in `illinoiscourthistory` itself, two lines under the 1835 sentence,
sits "constructed in the Greek Revival style, and built with stone ... designed by ... John M.
Van Osdel" — that is the **1853** building, and it is the easier of the two to lift by mistake;
Van Osdel did not reach Chicago until 1837. This project's own dossier compounds the problem at
`docs/research/04-structures-south.md` line 178, where the corner and the phrase "a small wooden
stockade-type building" are tagged `[DOC]` to a document that contains neither. Nothing in the
record cites them, so the size, the material, the wall height, the roof and the door are all
this project's invention.
**A sting in the tail worth recording:** the corner adopted — the north-east of the square — is
reasoned from the two documented structures occupying the west corners and from the reading in
circulation ("the southwest corner of Clark & Randolph", which is the block's north-east
corner). It is ALSO the siting Andreas documents for the 1837 building, so the one placement
claim this record makes is the one an 1837 description would have contaminated it with. It is
adopted anyway, with that stated, because the alternative is a placement with no argument at all.
**How to resolve:** the Cook County commissioners' records for 1834–35. A single dated order
would carry a contract, a cost, a specification and a completion date, and would move four
attributes and the date from conjectural to documented at once.
**Covers:** `cook_county_courthouse_1835.wood_1835.footprint`,
`cook_county_courthouse_1835.wood_1835.position`,
`cook_county_courthouse_1835.wood_1835.form.construction`,
`cook_county_courthouse_1835.wood_1835.form.wall_height_m`,
`cook_county_courthouse_1835.wood_1835.form.roof_type`,
`cook_county_courthouse_1835.wood_1835.form.roof_pitch_deg`,
`cook_county_courthouse_1835.wood_1835.form.door`.
**Recorded:** 2026-08-11.

### L62 — Watkins' school house: one unrecorded word decides the whole building
**Decision:** the house on Michigan Street that John Watkins used as his second school is built
as a story-and-a-half braced-frame dwelling on a hall-and-parlour plan. `stories`,
`construction` and `plan` are all tagged `conjectural`.
**Why:** Andreas says "a house". That is the entire description. Frame is adopted because the
building stood in Kinzie's Addition, platted and selling in 1833, where what was going up was
new building rather than the older log stock at the forks — which is an argument about a
neighbourhood, not evidence about a house. The storey count and the plan are the
`frame_dwelling` archetype's own defaults, kept deliberately rather than replaced with fresh
numbers, on the reasoning L29 states about the bridge's pier spacing: a new figure would look
like a finding and would not be one.
**Consequence, and it is larger than an attribute:** the material decides the ARCHETYPE, and the
archetype is not a graded value. If a source says log, this record moves to `log_dwelling` and
the walls, the corners, the openings and the roof all change — a different building, not a
different attribute. The confidence view cannot show that, because it grades values and this is
a choice made one level above them. This entry is where it is recorded.
**How to resolve:** the Kinzie's Addition plat and its early conveyances; the 1833–35 *Chicago
Democrat*, which carried school advertisements and would name the house or its owner; Andreas at
page-image level around scan p. 305.
**Covers:** `watkins_school_house.house_1833.form.stories`,
`watkins_school_house.house_1833.form.construction`,
`watkins_school_house.house_1833.form.plan`.
**Recorded:** 2026-08-11.

### L63 — The Wolf Point row gains two buildings whose footprints are invented outright
**Decision:** `james_kinzie_house` (8 × 6.5 m) and `robert_kinzie_store` (7 × 6 m) are added to the
west-bank row on the strength of one clause each, with footprints tagged `conjectural` that cite no
sources.
**Why:** the sources give these two an ORDER and a NEIGHBOUR and nothing else. chicagology puts James
Kinzie's residence south of Wentworth's tavern; Andreas's list of the town's Indian traders gives
"Robert A. Kinzie, near Wentworth's tavern" (scan p. 235). Neither is described, measured, dated or
given a material. Unlike Miller's house, where an attested composition carries the SHAPE while only
the size is invented, here neither shape nor size carries anything: the polygons are ordinary
single-pen plans at ordinary sizes, chosen to sit in a river-front row.
**Consequence:** the west bank at Wolf Point now carries five structures — James Kinzie's house,
Robert Kinzie's store, the tavern, the Robinson cabins and Walker's meeting house — across about
130 m of frontage, on four ordering statements and no measured distances. Every one of them hangs off
`wolf_point_tavern`, which is itself the weakest placement in the parcel (L7). If the tavern moves,
the row moves with it.
**How to resolve:** Andreas vol. 1 at page-image level around the Wolf Point material (index: pp. 111,
114, 174, 629–631); or the retrospective Wolf Point views — Blanchard & Shober 1867, and the
"Wolf Point in 1830" plate Andreas reproduces — examined at plate level for the row's massing.
**Covers:** `james_kinzie_house.dwelling_1830.footprint`, `robert_kinzie_store.store_1830.footprint`.
**Recorded:** 2026-08-11.

### L64 — Two Clybourne records stand about three kilometres from their own ground, and one cabin stands for two
**Decision:** `clybourn_slaughterhouse` and `clybourn_cabins` are placed at the northern edge of the
modelled terrain on the east bank of the North Branch, with `position` tagged `conjectural`. Their
attested ground is the Clybourne place several miles up the branch — "south of the Bloomingdale Road
and opposite the North Chicago Rolling Mills" (Andreas scan p. 1149), "several miles up the North
Branch, where now are the North Chicago rolling-mills" (scan p. 215) — roughly 3 km north-north-west
of the forks and some 2.8 km beyond the box's northern edge. `clybourn_cabins` draws ONE cabin where
the dossier says the family built two, and states the count as `cabin_count` with `geometry:
"simplified"`.
**Why:** the terrain epoch models 640 m square. Dropping the buildings would have made the town's
first industry invisible; placing them at their true coordinates would have put them on the radial
skirt outside every view. The project owner's instruction of 2026-08-11 was to place at the edge of
modelled ground and say so. The BANK is preserved in both cases and is the only part of the
coordinate that carries evidence. The second cabin is not drawn because a second polygon would need
an invented spacing, an invented orientation and an invented relation to the first — three inventions
to express one number that is itself second-hand.
**Consequence:** two buildings appear at the head of the modelled North Branch that in life stood
three kilometres further up it, and a visitor who paces the distance from Wolf Point to the
slaughter-house will get an answer that is wrong by kilometres rather than by metres. The 60 m
between the cabins and the slaughter-house is invented entirely. The stock yard later called Bull's
Head is not modelled at all, and the door side of the slaughter-house — river or landward — is a coin
flip.
**How to resolve:** extend the terrain epoch north up the North Branch, at which point both records
move to their attested reach and this entry moves to Resolved.
**Covers:** `clybourn_slaughterhouse.log_1827.position`, `clybourn_slaughterhouse.log_1827.footprint`,
`clybourn_slaughterhouse.log_1827.form.door_side`, `clybourn_cabins.log_1824.position`,
`clybourn_cabins.log_1824.footprint`, `clybourn_cabins.log_1824.form.cabin_count`.
**Recorded:** 2026-08-11.

### L65 — The town's industry is modelled as sheds, and the works inside them are not built
**Decision:** four industrial records — `brickyard_north_side`, `elston_soap_candle_manufactory`,
`pierce_blacksmith_shop` and `newberry_dole_slaughterhouse_south_branch` — are each built as a single
`outbuilding` at an invented size, with their plant recorded on the record and absent from the mesh:
the brickyard's clamp, hacks, clay pit and spoil (`yard_works`), Elston's rendering kettle, ash leach
and moulding floor (`plant`), and Pierce's forge, bellows and chimney (`forge`).
**Why:** this project has archetypes for buildings and none for a WORKS. A brickyard is an area of
ground with a burning clamp on it; a soap manufactory is a fire under a kettle; a smithy is a hearth
and a stack. The outbuilding archetype builds walls and a roof and has no chimney parameter at all,
so the one visible sign of every one of these trades — smoke — cannot be built. Rather than leave the
trades out of the town, each is modelled as the shed the trade worked under and the plant is declared.
**Consequence:** the most legible failure in this parcel. Blodgett's brickyard, which supplied the
brick for the Lake House going up on the same bank, reads as one open shed in a field. Elston's
manufactory has no fire. Pierce's smithy has no smoke. The confidence chips over these attributes say
"we are fairly sure this existed" and the visitor sees nothing. This is the same shortfall L10 records
against the Western Hotel's wagon yard, now repeated four times, and it is the strongest argument in
the dataset for a works or parcel archetype. Newberry & Dole's slaughter-house is additionally placed
on a reach and a bank of the South Branch that no source gives — Andreas says only "on the South
Branch of the river" (scan p. 1151), a corridor kilometres long — and its door side is a coin flip.
**How to resolve:** a `works` or `yard` archetype that can carry an enclosure, a fire and a stack. Any
description of any of these four premises would help the footprints; nothing found describes one.
**Covers:** `brickyard_north_side.yard_1833.footprint`,
`brickyard_north_side.yard_1833.form.yard_works`,
`elston_soap_candle_manufactory.works_1833.footprint`,
`elston_soap_candle_manufactory.works_1833.form.plant`,
`pierce_blacksmith_shop.shop_1833.footprint`, `pierce_blacksmith_shop.shop_1833.form.forge`,
`newberry_dole_slaughterhouse_south_branch.works_1834.footprint`,
`newberry_dole_slaughterhouse_south_branch.works_1834.position`,
`newberry_dole_slaughterhouse_south_branch.works_1834.form.door_side`.
**Recorded:** 2026-08-11.

### L66 — Two river warehouses stand on banks that are disputed or unattested, and neither has its dock
**Decision:** `newberry_dole_warehouse` is placed on the SOUTH bank of the main stem with its position
tagged `conjectural`, against an Andreas sentence that puts the firm's warehouse on the north side;
`kinzie_hunter_warehouse` is placed on the NORTH bank with its position AND its date range tagged
`conjectural`, on a plausibility the dossier itself tags `[CONJ]`. Both records state `dock: true`
with `geometry: "absent"`, and neither dock is built.
**Why (the bank):** this project's own dossiers disagree. docs/research/03-structures-north.md §3.10
reports a square frame "Newberry and Dole's Forwarding and Commission House" on South Water Street in
views of c. 1835; docs/research/04-structures-south.md quotes Andreas — "whose warehouse was on the
North Side, immediately east of where Rush-street bridge now stands" (scan p. 1139) — and instructs
"Do not put it on South Water Street." The south bank is adopted because Andreas's sentence sits
inside an account of a grain shipment made on the brig *Osceola* in **1839**, so the building it
locates is the firm's warehouse four years after the scene date. That is reasoning, not proof, and the
disagreement is recorded rather than resolved. Kinzie & Hunter's bank is not disputed but simply
absent: the dossier lists it as an open gap, "bank, date, size".
**Why (the dock):** "each had a warehouse with its dock along the river front" is the clause that
attests these buildings at all, and Andreas independently names "Newberry & Dole's wharf" as the place
the schooner *Illinois* was cheered on 12 July 1834 (scan p. 503). The project has a `pier_crib`
archetype for the harbour piers and nothing for a river wharf; a dock of invented length, height and
construction sitting in the water would be a larger invention than the buildings it served.
**Consequence:** the river trade — the reason the town existed in 1835 — is represented by two sheds
standing back from an empty bank. On `kinzie_hunter_warehouse` the `dock` attribute carries a
`documented` chip over nothing at all, which is precisely the failure the geometry declarations exist
to surface. And one of the two warehouses is probably on the wrong side of the river.
**How to resolve:** identify the c. 1835 view the north-side dossier describes and give it a source
record; or read further issues of the *Chicago Democrat*, whose advertising columns are where a
forwarding house states its street.
**Covers:** `newberry_dole_warehouse.frame_1833.position`, `newberry_dole_warehouse.frame_1833.footprint`,
`newberry_dole_warehouse.frame_1833.form.dock`, `kinzie_hunter_warehouse.warehouse_1834.position`,
`kinzie_hunter_warehouse.warehouse_1834.footprint`, `kinzie_hunter_warehouse.warehouse_1834.form.dock`,
`kinzie_hunter_warehouse.warehouse_1834.documented_range`.
**Recorded:** 2026-08-11.

### L67 — A trade advertised in November 1833 becomes a building standing in July 1835
**Decision:** `elston_soap_candle_manufactory` is built from a newspaper advertisement, with both its
`documented_range` and its `position` tagged `conjectural`.
**Why:** the *Chicago Democrat* of 26 November 1833 carries Daniel Elston & Co.'s soap and candle
manufactory, paying cash for tallow and house ashes, and Andreas's summary of the same columns repeats
it (scan p. 755). That fixes a TRADE in a month — and the source record for the paper states the limit
in as many words: an advertisement is "strong evidence of existence and address, weak evidence of
survival, and no evidence at all of form." The scene date is nineteen months later, in the town's
fastest-changing period. No address is given anywhere. The works are placed on the east bank of the
North Branch on two unevidenced arguments: that Elston is a North Branch figure (the road named for
him, and his later brickyard on that side — Andreas scan pp. 409, 1169, both decades after the scene),
and that rendering is a nuisance trade that sits at the edge of a town near its slaughtering. Every
other locatable advertiser in the same issue was on or near South Water Street, which is at least as
good an argument the other way and is written into the record's position note.
**Consequence:** a manufactory appears on the North Branch that may have stood on South Water Street,
or may not have been standing at all by July 1835. It is built because an absent building is invisible
to a visitor while a conjectural one is legible and correctable — the project owner's standing
instruction of 2026-08-11 — and because the tallow trade belongs beside the slaughtering this parcel
also models.
**How to resolve:** further issues of the *Chicago Democrat*. One line of an 1834 or 1835
advertisement carrying a street would settle the position and narrow the range at once.
**Covers:** `elston_soap_candle_manufactory.works_1833.documented_range`,
`elston_soap_candle_manufactory.works_1833.position`.
**Recorded:** 2026-08-11.

### L68 — The slough crossing is invented at every dimension except its material
**Decision:** `slough_log_bridge` is built at an invented 8 × 3 m deck with `clearance_m` 0.5 m tagged
`conjectural`, and it deliberately does NOT borrow the branch bridges' documented figures.
**Why:** the source gives one sentence — where Water Street crossed the slough, a log bridge was
needed until after 1840 — and one adjective, *log*. The span is sized off the STREAM rather than the
bridge: the hydrology dossier gives the slough a width of 15–40 ft (zone 14) and tags width and depth
conjectural while calling the route documented, so 8 m of deck crosses the narrow end of that range.
The clearance is the number that mattered most to get wrong quietly: the two branch bridges stood
"about six feet above the water, so that teams passed under them on the ice freely", which is
documented for THEM and absurd here — nothing passed under a slough crossing. 0.5 m is a reading of a
conjectural stream depth, not a measurement.
**Consequence:** a visitor sees a small timber deck whose every proportion is this project's. If the
slough ran 40 ft wide at the crossing, the span is half what it should be.
**How to resolve:** any period description of the crossing, or a surveyed width for the slough at the
foot of State Street.
**Covers:** `slough_log_bridge.log_1833.footprint`, `slough_log_bridge.log_1833.form.clearance_m`.
**Recorded:** 2026-08-11.

### L69 — Two structures stand at their documented sites beyond the modelled ground
**Decision:** `brickyard_north_side` and `slough_log_bridge` are placed at the sites their sources
give — the north bank between Clark and Dearborn, and the Water Street crossing at the foot of State
Street — which lie 300 m and 490 m east of the modelled terrain box. Both phases declare
`ground_contact: {state: "outside_modelled_ground"}`.
**Why:** the opposite choice was available and was taken for the Clybourne records (L64), which were
pulled to the modelled edge because their sites are kilometres away and only loosely fixed. These two
are different: the brickyard's site is attested to a 120 m span of street frontage (Andreas scan
p. 1161) and the bridge's to the meeting of a named street and a named stream mouth, so displacing
them would throw away the best evidence either record holds. What is missing here is terrain, not
evidence.
**Consequence:** neither structure meets any ground. `tools/heightfield.py` clamps at the box edge, so
without the declaration the gate would have reported both as landing perfectly on terrain that does
not exist. The slough bridge is worse off again: the South Division slough it crosses is not cut into
this terrain epoch at all — the only modelled watercourse besides the river is an unnamed slough on
the north side — so it stands over flat ground with no stream beneath it, and the `bridge_timber`
archetype anchors it to the river's water surface, which the hydrology dossier puts 0.15–0.45 m below
the slough's own.
**How to resolve:** extend the terrain epoch east over the South Division and the north bank as far as
Dearborn, and cut the slough's documented route into it. Then both declarations come off and this
entry moves to Resolved.
**Covers:** `slough_log_bridge.log_1833.ground_contact`.
**Evidence since, 2026-08-11:** the brickyard's token is withdrawn — S2e extended the
heightfield east and Blodgett's yard now lands on modelled ground. The slough crossing still
stands clear of it, but for the different reason recorded on that record: the South Division
slough it crosses is still not cut into this terrain epoch, so it spans nothing.
**Recorded:** 2026-08-11.

### L70 — The mosquitoes are rendered as nothing, and they were the defining July fact
**Decision:** mosquitoes, deer flies and horse flies are recorded as `abundant` and
`not_perceptible` in four zones, and nothing is drawn for any of them.
**Why:** the insects will not read at any render scale. Their visible signal is *human* — smudge
fires, mosquito bars over beds, covered arms, hands moving at faces — and L1 puts human depiction
out of scope for v1. So the single most intense sensory fact of a July Chicago, in a town "situated
in the midst of sloughs and marshes" with endemic ague and no window screens, is rendered as
absence.
**Consequence:** a visitor walks a July wetland town that feels comfortable. It was not. The only
sourced testimony for it sits on a page that returned HTTP 403 and has no source record, so even
the quotation is unverified; Andreas is not and never will be a source for it — searches for
*mosquito*, *mosquitoes* and *musquitoes* all return zero hits.
**How to resolve:** a retrievable period source, and either a smoke/smudge element in the
structures dataset or the lifting of L1.
**Recorded:** 2026-08-11.

### L71 — The horse herds at the town margin are attested and not depicted
**Decision:** `f01_wet_prairie/equus_caballus_indigenous_herds` records the herds with
`status: excluded_by_scope` and `presence: not_depicted`. Nothing is placed.
**Why:** Shirreff described the prairies around Chicago in 1833 as studded with tents and numerous
herds of horses browsing in all directions. Those herds are inseparable from the people who kept
them, and AGENTS.md and L1 put human depiction out of scope for v1 uniformly. The great assembly at
Chicago is 18 August 1835 — six and a half weeks *after* the scene date — so staging it would be
wrong twice over.
**Consequence:** the prairie margin is emptier than it was. This is a scope decision, not a finding
of absence, and the dataset distinguishes the two: `not_depicted` is a different value from
`absent` and the validator will not let one be written as the other.
**Note:** the Shirreff 1833 account has no source record in `data/sources/`; only the August 1835
date is cited, from `chicagology_lastwardance`, and nothing beyond that date is drawn from it.
**Recorded:** 2026-08-11.

### L72 — The town's outbuildings are placed and sized by eye, on the strength of the buildings in front of them
**Decision:** the three secondary buildings added behind the town's public houses —
`western_hotel_stable` (13 x 7 m), `wolf_point_tavern_stable` (9 x 6 m) and `beaubien_barn`
(6.10 x 4.88 m) — carry **invented footprints**, two carry **invented positions**, and two carry an
**invented door elevation**, all tagged `conjectural`, citing no sources.
**Why:** not one source reached by this project gives any outbuilding at the forks a dimension, a
plan or a bearing. What the sources give is existence and relation: a stable "in the rear" of the
Western Hotel, a county tariff that prices keeping a horse overnight at a house one of whose
keepers held the county's first tavern licence, and a cabin that "he used after this for a barn".
The sizes answer the attested TRADE rather than being chosen freely — the Western's stable is the
largest outbuilding in the dataset because its source calls it large and its teams "were as
numerous as were the guests"; the Wolf Point stable is smaller so the two are not one invented
building at two addresses; and the Beaubien barn is drawn at single-pen CABIN scale, 20 x 16 ft,
because the source describes a dwelling that stopped being one rather than a barn that was built.
**Consequence:** a visitor sees three buildings whose *presence* is evidenced and whose *shape and
exact place* are ours. The Beaubien barn additionally inherits its parent record's two open
questions — the corner Andreas contradicts himself about, some 45 m, and the fact that neither
street existed on the unplatted reservation in 1835.
**How to resolve:** Wright 1834 or Hathaway 1834 read at lot level for the Randolph-and-Canal
block; Andreas "Wharfs, Piers and Early Hotels", scan pp. 626-631, at page-image level for the Wolf
Point group; the 1839 land-sale plat of Block 5 with the lot numbers Andreas quotes.
**Covers:** `western_hotel_stable.stable_1834.footprint`,
`wolf_point_tavern_stable.stable_1831.footprint`,
`wolf_point_tavern_stable.stable_1831.position`,
`wolf_point_tavern_stable.stable_1831.form.door_side`,
`beaubien_barn.converted_1817.footprint`, `beaubien_barn.converted_1817.position`,
`beaubien_barn.converted_1817.form.door_side`.
**Recorded:** 2026-08-11.

### L73 — Every outbuilding in the town is detailed by the archetype, not by a source
**Decision:** the `outbuilding` archetype supplies, as fixed conventions applied to every record
that uses it and stated by no source anywhere: the **single small unglazed vent** it cuts in a
wall; the **post spacing** in an open bay; the **board rhythm** of a boarded wall; the **roof
covering** (laid boards — not shingles, not shakes, not thatch); and the **direction a shed roof
falls**, which the archetype derives from the open sides rather than reading from the record. The
size-aware defaults for wall height, roof form and pitch are conventions in the same sense.
**Why:** no source reached by this project describes the fabric, the covering, the openings or the
framing of ANY outbuilding at the forks — not one. The archetype's own module says so at the top
and grades an unstated attribute `conjectural` for exactly this reason, so the confidence channel
already paints these buildings honestly; what it cannot say is that the *detail a visitor is
looking at* was designed rather than found.
**Consequence:** two outbuildings in this scene that carry different evidence still share a vent, a
board rhythm and a roof texture, because those came from one Python module. Anyone reading a
boarded wall as a finding about 1835 Chicago carpentry is reading the generator.
**How to resolve:** any period description or depiction of a secondary building at Chicago before
1836 — none is currently known to this project. This entry has no `Covers:` field on purpose: it
claims nothing about any single record, because the invention is in the archetype and lands on
every one of them.
**Recorded:** 2026-08-11.

### L74 — Tremont House I: a hotel built two storeys tall because three rests on one modern sentence
**Decision:** the first Tremont House is built at the north-west corner of Lake and Dearborn as a
**two-storey** braced-frame block 50 × 30 ft, unpainted, gable-roofed and without a gallery. The
storey count, the wall height, the roof, the paint, the gallery and the footprint are all tagged
`conjectural`.
**Why, and the storey count is the whole entry.** What is documented about this building is
unusually good: the corner three times over, frame construction three times over, Alanson Sweet
as builder, Ira Couch as proprietor from 1834, and destruction by fire on 27 October 1839. What
is not documented is its height. `chicagology_prefire021` prints an uncredited modern "Building
Summary" — "a three-story wooden building" — beside two period texts that count no storeys at
all: the Chicago *Tribune* letter of 2 February 1874 ("an unpretending frame structure") and
*Chicago Illustrated* of January 1866 ("a wooden structure"). Andreas, who gives the building a
builder, a corner, a material, four proprietors and a death date, gives it no height. So the
three-storey Tremont has exactly one witness and it is a modern editor;
`docs/research/04-structures-south.md` line 155 weighs it twice by citing "chicagology and
Wikipedia". **Two is adopted and is still a guess**, on three arguments that are not evidence:
Chicago in 1833 held about 350 people and *Wau-Bun* found the Sauganash's TWO storeys remarkable
two years earlier; the *Chicago American*'s "Improvements in 1836", quoted by Andreas, counts
"about twenty large two to three-story wooden buildings" among that year's NEW work; and this
project already excludes the Saloon Building of 1836 partly as the town's first three-storey
structure.
**Consequence:** if the three-storey reading is right the building stands about 2.6 m taller than
the model shows, and it would be the tallest thing in the 1835 scene. Everything else here is the
usual: no source measures the house, describes its roof, names its finish or mentions a porch,
and the confidence view renders the whole block as massing. **One documented thing about this
building IS carried and is not built**: Ira Couch's "a mere shell, without any sidewalk around
it". This project builds no plank walks anywhere, so the record states `sidewalk: false` as
`record_only` — a negative finding about the ground, not an omission.
**How to resolve:** the *Daily American*'s account of the 27 October 1839 fire, which Andreas
quotes for the merchants' stock losses and which itemised insurance building by building; or any
*Chicago American* or *Chicago Democrat* advertisement of the house, which in the period counted
rooms.
**Covers:** `tremont_house_1.frame_1833.footprint`,
`tremont_house_1.frame_1833.form.stories`,
`tremont_house_1.frame_1833.form.wall_height_m`,
`tremont_house_1.frame_1833.form.roof_type`,
`tremont_house_1.frame_1833.form.paint`,
`tremont_house_1.frame_1833.form.gallery`.
**Recorded:** 2026-08-11.

### L75 — Mansion House: an attested frame front, built on invented arms
**Decision:** Dexter Graves's log tavern on Lake Street near Dearborn is built as a 12 × 9 m
one-storey log core with a one-storey frame block 12 m wide and 4 m deep across its front. The
footprint, the wing's width, its depth, its storey count and its finish are all tagged
`conjectural`.
**Why:** Andreas describes this building's growth in a sentence that is worth more than anything
else in the parcel — "As originally built, the Mansion House was situated some little distance
back from the street, but two years later Mr. Graves erected a frame addition in the front, which
came out to a line with the street" — and the sentence contains no numbers. So the *side* of the
addition is documented (the only one in this dataset that is; the Wolf Point Tavern's is
conjectural, L24), and its size is not. **The 4 m depth is the invention doing the most work: it
stands in for "some little distance back from the street", which is an unmeasured setback**, and
anything from a two-metre porch depth to a full second range is compatible with the sentence. The
12 m width is set to the full frontage so the new block presents one continuous face to Lake
Street, which is what the RESULT implies and not what the width does; a narrower block would
leave a notch at one end that no source describes and that would read as a modelled fact about
the plan. One storey for the addition is an argument from silence — a two-storey front on a
one-storey log tavern would have been the more remarkable thing and would probably have been
said.
**Consequence:** the building's south face stands exactly on the Lake Street building line, which
IS attested, and every metre behind that line is chosen. The overall 12 × 9 m rests on two weak
arguments — it later took two street numbers, 84 and 86 Lake Street, and it held a room the
Circuit Court sat in — and neither is a measurement. The unfinished loft, which the court sat in,
is `documented` and is built as a gable-end opening and nothing else, since a loft leaves no
other external trace.
**How to resolve:** *Chicago Democrat* or *Chicago American* advertisements of the house under
Haddock or Markle, which in the period counted rooms; or a Cook County deed on the lots that
became Nos. 84 and 86 Lake Street, which would give the frontage from a document rather than from
a street-number inference.
**Covers:** `mansion_house.log_frame_1833.footprint`,
`mansion_house.log_frame_1833.form.frame_addition_width_m`,
`mansion_house.log_frame_1833.form.frame_addition_depth_m`,
`mansion_house.log_frame_1833.form.frame_addition_stories`,
`mansion_house.log_frame_1833.form.frame_paint`.
**Recorded:** 2026-08-11.

### L76 — The Exchange Coffee House: five documented facts, and not one of them about the building
**Decision:** Mark Beaubien's second hotel is built at the north-west corner of Lake and Wells as
a two-storey braced-frame block 46 × 30 ft, unpainted, gable-roofed, without a gallery. The
construction, the storey count, the wall height, the roof, the paint, the gallery and the
footprint are all tagged `conjectural`.
**Why:** two independent passages of Andreas — the hotel chapter and the life of Mark Beaubien —
agree on the builder, the corner, the year, the keepers and the name, which is more agreement
than any other building in this parcel gets. Neither says what it was made of, how big it was,
how many storeys it had or what it looked like. **The consequential guess is `construction`,
because it also chose the ARCHETYPE**: a frame reading makes this a `frame_tavern` and a log
reading would make it a `log_dwelling`, so if it is wrong the building is wrong in kind and not
merely in detail — the same admission L62 makes for Watkins' school house. The argument for frame
is that every Chicago hotel this dataset can date to 1833 or later is frame while the log taverns
belong to 1828-31; the argument against treating that as evidence is L18, that the ordinary
reading of a TYPE is not evidence about a BUILDING — and the man who built this one had made his
last hotel by adding a frame block onto a log cabin.
**Consequence:** the confidence view renders the whole house as massing, correctly. The facade
bearing is a second unclaimed choice of the same kind: no source says which street the house
fronted, and a corner house called an *Exchange*, at which stage seats were later booked, could
as easily have turned its front to Wells. **A correction this record carries rather than
inherits:** `data/exclusions.json` and `docs/research/04-structures-south.md` both say stage
seats were taken here "in 1835-36". Andreas dates that advertisement to the *Chicago American* of
**6 August 1836**, thirteen months after the scene date, so the record does not claim a
stage-office function for 1835. The exclusion of a separate stage-office BUILDING is unaffected.
**How to resolve:** the *Chicago Democrat* and the *Chicago American*, in both of which this
house was a standing address; and the 1834-36 Cook County tavern licences, which would also
settle whether Abram A. Markle held this house and the Mansion House at the same time.
**Covers:** `exchange_coffee_house.frame_1834.footprint`,
`exchange_coffee_house.frame_1834.form.construction`,
`exchange_coffee_house.frame_1834.form.stories`,
`exchange_coffee_house.frame_1834.form.wall_height_m`,
`exchange_coffee_house.frame_1834.form.roof_type`,
`exchange_coffee_house.frame_1834.form.paint`,
`exchange_coffee_house.frame_1834.form.gallery`.
**Recorded:** 2026-08-11.

### L77 — The Lake House is a building site built with a fort's archetype, one storey up, on a corner nobody halved
**Decision:** the Lake House is modelled as a **construction site**: a roofless brick shell one
storey high on a 79 × 49 ft plan, at the corner of Rush and Michigan streets on the north bank,
built with the `fort_structure` archetype under `kind: "magazine"`. The position, the footprint,
the archetype `kind`, the storey count and the wall height are all tagged `conjectural`.
**Why, and it is three admissions.**
**(1) How far it had risen is unattested, and that is the interesting part.** Everything about
the FINISHED hotel is documented — brick, three storeys and a basement, nearly $100,000, five
named backers, opened in the autumn of 1836. Nothing says what stood on the ground on 1 July
1835; `chicagology_prefire112`'s own *what_it_does_not_supply* list says so in terms. One storey
comes from a schedule argument — ground broken somewhere in 1835, open by autumn 1836, so about
eighteen months for three storeys and a basement of brick, putting 1 July 1835 in the first
quarter of the work — and the honest range is **zero to two**. At three storeys this structure
would stand about 12 m and be the tallest thing in the scene, which is exactly what
`data/exclusions.json`'s `lake_house_finished` entry exists to prevent. The best anchor found is
J. D. Bonnell's letter to the *Chicago Times* of 15 March 1876, quoted by Andreas, seeing "the
Lake House in course of construction" on a date the letter gives as 25 August 1835 — eight weeks
after the scene date — though the same letter's "forty years ago" implies 1836 and Andreas's
lead-in says 1837. The 1837 reading is impossible on the letter's own content.
**(2) The archetype is off-label and `kind: "magazine"` is a selector, not a claim.** It does not
say the Lake House was a powder magazine. `fort_structure` is the ONLY archetype in this project
whose vocabulary admits `construction: brick` AND `roof_type: none`, and brick is the one
documented fact about this structure's fabric while rooflessness is the one important fact about
its state; `magazine` is the only one of its eleven builders that draws a plain masonry
rectangle with a single opening and no windows, where every other kind would cut a regular window
rhythm and render a building site as a finished hotel. `frame_tavern` would build a windowed,
roofed, five-bay house; `outbuilding` can build neither brick nor a roofless structure — the same
constraint L60 records for the estray pen, which had to take a roof it probably never had. The
archetype's own docstring already extends it past the fort once, to the 1832 lighthouse.
**(3) The corner is documented and the side of the street is not.** Andreas twice puts the house
at Kinzie, Rush and Michigan streets, fronting Michigan. A block between Kinzie and Michigan has
two faces on Rush about 110 m apart and nothing says which; the east side is adopted on a
neighbourhood argument. **Guard travelling with it:** north-side Michigan Street is today's East
Hubbard Street, one block north of Kinzie — NOT Michigan Avenue, which did not cross the river
until 1920. The gloss "near where the Wrigley Building stands today", on `chicagology_prefire112`
and repeated in `docs/research/03-structures-north.md` §3.8 (which also renders the street as
"Michigan (Water)"), moves the site about 150 m and across Kinzie.
**Consequence:** what a visitor sees is a low roofless brick rectangle, which is right in kind
and invented in every dimension. **What the model still cannot show is the excavation** — a
construction site is a hole in the ground before it is anything else, and nothing in this project
cuts a cellar into the terrain, so the shell sits ON the surface rather than in it. The footprint
also asserts a full rectangle walled to one height where a real site would be part cellar, part
first-course brickwork, part mortar-bed, scaffold and stacked material.
**How to resolve:** the *Chicago American* (first issue 8 June 1835) and the *Chicago Democrat*
for 1835-36 — a $100,000 hotel going up in a town of three thousand was news; and the Kinzie's
Addition conveyances, which would give the lots, the plan and the side of Rush Street at once.
**Covers:** `lake_house_construction.shell_1835.position`,
`lake_house_construction.shell_1835.footprint`,
`lake_house_construction.shell_1835.form.kind`,
`lake_house_construction.shell_1835.form.stories`,
`lake_house_construction.shell_1835.form.wall_height_m`.
**Recorded:** 2026-08-11.

### L78 — A saddler's corner survives nineteen months on nothing but a paid advertisement
**Decision:** `goss_cobb_saddlery` is built at the crossing of Lake and Canal from one newspaper
advertisement, with its `documented_range`, its `footprint` and its storey count tagged
`conjectural`.
**Why:** the *Chicago Democrat* of 26 November 1833 carries the firm's own notice — "they have
opened a shop in this village, on the conner of Lake and Canal-streets" — which is a **tier-1,
self-reported address**, better positional evidence than most records in this dataset hold,
because the advertiser's customers had to be able to find him. It fixes a trade and a junction in
one week of November 1833 and does nothing else. **The scene date is nineteen months later**, in
the town's fastest-changing period, and `data/sources/chicago_democrat_1833_11_26.json` states
the limit in as many words: an advertisement is "strong evidence of existence and address, weak
evidence of survival, and no evidence at all of form". Nothing reached follows this firm past
November 1833. The building stands anyway, on the project owner's standing instruction that an
absent building is invisible while a conjectural one is legible and correctable — the same
reasoning L67 gives for Elston's soap works, from the same issue of the same paper.
**Consequence:** a shop stands on Lake Street that may have been gone, moved or rebuilt by July
1835, at a size and a storey count nobody recorded. **Two positional admissions travel with it.**
The advertisement names a *junction*, not a corner, exactly as the Democrat's own imprint says
"on the corner of South Water and Clark-streets" and names none; the Green Tree Tavern holds the
north-east quadrant of this crossing, three remain, and this record picks the south-east — a
one-in-three choice worth about 40 m. And "Canal" at this crossing inherits the doubt already
recorded on the Green Tree: modern Canal Street lies a full block back from the west bank, where
the 1830s riverbank street was West Water, so if the advertisement means the bank street the shop
belongs about **145 m east**. That is the larger of the two and it is the same open question the
Green Tree's own record carries; settling one settles both. The `position` is nonetheless tagged
`inferred` rather than `conjectural`, because the junction itself is documented and it is only
the quadrant that is chosen — the doubt is written on the record rather than in the tag.
**How to resolve:** further issues of the *Chicago Democrat* and the *Chicago American*, one line
of which would settle survival and might name a side; and the lot geometry on Wright 1834 or
Hathaway 1834, which would settle Canal against West Water for this record and for the Green Tree
at once.
**Covers:** `goss_cobb_saddlery.shop_1833.documented_range`,
`goss_cobb_saddlery.shop_1833.footprint`,
`goss_cobb_saddlery.shop_1833.form.stories`.
**Recorded:** 2026-08-11.

---

## Resolved

Entries here were true when they were written and are kept verbatim, with a **Resolved:**
line saying what settled them. The gate exempts this section from the check that a claimed
value is still an invention, which is what lets an append-only document survive its own data
being corrected.


### L40 — Two thirds of the town stands on ground that has not been built
**Decision:** twenty of the thirty-three structures now in the dataset stand **outside the
modelled heightfield** and do not reach the terrain beneath them. Their records are correct and
their positions are derived through the same fitted transform as everything else; there is
simply no ground there yet.
**Why:** the heightfield covers **E −320 … +320, N −320 … +320** — a 640 m square around the
forks, built when the forks was the whole scene. The town is not that shape. South Water Street
runs from about **E +347** (`h_jones_store`) to **E +745** (`frederick_thomas_shop`); the
Dearborn Street bridge is at **+699**; Cobweb Castle, the north-bank agency house, is at
**+814**; the Beaubien homestead is at **+1090**. The entire business district — the reason the
town existed — sits east of the modelled world, along with the bridge that crossed to it.
This was not discovered by inspection. It surfaced the moment the project stopped building only
the best-evidenced structures and started building the town: the forks quadrant was sufficient
for eight buildings and is nowhere near sufficient for thirty-three.
**Consequence:** those twenty buildings currently float. A visitor who walks east finds the
ground end and the town continue. **This is worse than the buildings being absent**, because an
absent building makes no claim while a floating one makes a false one, and the confidence view
cannot mark it — the tint grades what a building WAS, not whether it stands anywhere. It is
recorded here as a liberty rather than left as a bug because it is a known, measured, deliberate
intermediate state: the records were built first on the argument that evidence is harder to come
by than geometry, and the geometry is now the thing holding.
**How to resolve:** ROADMAP § S2e — extend the heightfield east to about **E +1700**, a
~2.0 km × 0.7 km field, using the shore, the 1834 cut, the sand bar and the old southward
channel already traced in `data/traces/vectors/wright_1834_east.json` and
`shoreline.geojson`. That work is in progress. **When it lands, this entry moves to Resolved**
rather than being edited, and any structure still floating afterwards — the North Branch
industry sits well north of even the extended box — gets an entry of its own naming it.
**Covers:** `bates_auction_room.frame_1834.ground_contact`,
`carpenter_south_water_store.frame_1833.ground_contact`,
`chicago_american_office.frame_1835.ground_contact`,
`chicago_democrat_office.frame_1833.ground_contact`,
`dole_warehouse_south.frame_1832.ground_contact`,
`frederick_thomas_shop.frame_1835.ground_contact`,
`h_jones_store.frame_1833.ground_contact`,
`harmon_loomis_store.frame_1833.ground_contact`,
`jb_beaubien_homestead.factory_1817.ground_contact`,
`madore_beaubien_house.log_1831.ground_contact`,
`old_bank_building.frame_1834.ground_contact`,
`peck_store.frame_1833.ground_contact`,
`pruyne_kimball_drugstore.frame_1830s.ground_contact`,
`h_jones_store.frame_1833.footprint`, `h_jones_store.frame_1833.position`,
`h_jones_store.frame_1833.form.stories`,
`jh_kinzie_forwarding_store.frame_1830s.footprint`,
`jh_kinzie_forwarding_store.frame_1830s.position`,
`jh_kinzie_forwarding_store.frame_1830s.form.stories`,
`north_pier.crib_1835.ground_contact`, `south_pier.crib_1835.ground_contact`,
`cobweb_castle.log_1820.ground_contact`,
`blacksmith_shop_state_st.log_1823.ground_contact`,
`north_side_school_1833.log_1833.ground_contact`,
`steamboat_hotel.frame_1835.ground_contact`,
`council_house.log_1834.ground_contact`,
`first_presbyterian_church.frame_1834.ground_contact`,
`st_marys_church.frame_1833.ground_contact`,
`log_jail.log_1833.ground_contact`,
`estray_pen.pen_1833.ground_contact`,
`cook_county_courthouse_1835.wood_1835.ground_contact`,
`chappel_infant_school.log_1833.ground_contact`,
`watkins_school_house.house_1833.ground_contact`.
**Recorded:** 2026-08-10.

**Resolved:** 2026-08-11. The ground was built. ROADMAP § S2e extended the heightfield east from a
640 m square to **E −320 … +1700, N −400 … +400** — 809 × 321 samples at 2.5 m — and twenty-seven of
the structures this entry covers now land on real terrain. The declarations came off those records in
the same pass that moved this entry here.

Three things are worth keeping from it rather than deleting with it. **The finding was only visible
because the town got built**: eight well-evidenced buildings at the forks all sat comfortably inside
the old box, and it took building the business district to discover the business district had no
ground under it. **The gate could not see it either** — `tools/heightfield.py` clamped outside the
box, so a structure 832 m past the edge sampled the clamped edge for its base and for every contact
point, agreed to the millimetre, and was reported as landing perfectly. Fort Dearborn is what exposed
that, and the fix (`Heightfield.covers()`, plus a two-way check that a declaration matches the
measurement) immediately flagged two more structures nothing had caught. And **not everything came
back**: the Clybourne records still stand about three kilometres from their attested ground up the
North Branch, and the stockade's north wall and the commandant's quarters now cross the top of the
river bank because no cut, fill, revetment or foundation is modelled anywhere in this project. Those
are L64 and L46's business, not this entry's.

### L13 — Composite log-and-frame buildings are extruded to a single wall height
**Decision:** `miller_house` and `wolf_point_tavern` are each modelled at one wall height,
although both are attested as composites — Miller's as a two-storey frame range fronting the
river with a one-storey log cabin behind, the Wolf Point Tavern as "partly log and partly frame".
**Why:** the `log_dwelling` archetype does not yet build a mixed-height mass, and averaging the
two heights would produce a building matching neither description. The records carry the taller
element's height and flag the overstatement rather than hiding it.
**Consequence:** a geometry requirement for `log_dwelling`, discovered from the evidence in the
same way the Sauganash's attached log wing was (L4a). Until it lands, the log elements render
taller than they were.
**Recorded:** 2026-08-09.
**Revised:** 2026-08-10 — half of this is no longer true. The archetype does build a mixed-height
mass: a frame addition carries its own storey count and its own height, and the Wolf Point Tavern
now stands as a 2.6 m log core with a 2.55 m frame bay rather than one extrusion. Miller's house
is unchanged and still the case this entry describes — its record carries the taller element's
5.2 m and its log cabin is rendered two storeys high — because setting its frame range's height
without also settling how much of the footprint the range takes would swap one overstatement for
a different one. The entry stays here rather than moving to Resolved for exactly that reason.
**Resolved:** 2026-08-10 — the other half landed the same day, in the slice the Revised line
above asks for. Miller's range now carries its own width (9 m), depth (6 m), storey count (2,
`documented`) and height (5.2 m), so the 5.2 m came off `wall_height_m` and the log cabin stands
at the 2.6 m this record has named for it since it was written. Neither building is a single
extrusion any more, and the overstatement this entry existed to flag is gone rather than
described. Worth keeping the sentence "the records carry the taller element's height": for
Miller's house that had a sharper edge than it reads. `stories` was `2, documented`, and the
archetype reads `stories` as the LOG CORE's — so the documented claim was spent on the cabin,
the range fell back to a default height of 4.7 m, and the model stood the taller element behind
the shorter one. The invented dimensions that replaced the defaults are admitted in L27.

### L20 — Wolf Point Tavern: the frame half and the painted wolf sign are recorded and unbuilt
**Decision:** the record states `frame_extension: true` and `signage: painted_wolf_sign`, both
`documented`, and the mesh contains neither. What stands at Wolf Point is a plain hewn-log cabin
with no frame piece and no sign.
**Why:** not a judgement — an accident, and it is recorded as one rather than dressed up. The
`log_dwelling` archetype reads `frame_addition` and `sign`; this record spells the same two
things `frame_extension` and `signage`. Neither spelling is wrong and neither resolver ever
complained, because `from_phase` fills an absent attribute with a default: no frame addition, no
sign. The building was baked from those defaults and nothing anywhere said the two best-attested
features of the house had been dropped.
**Consequence:** this is the worst case the confidence model has, because the model is working
exactly as designed and still misleads. `documented` is the strongest claim the project makes.
A visitor who picks the tavern reads *signage · painted wolf sign · documented* on a building
with no sign on it, and *construction · partly log and partly frame* on a building that is
entirely log — and the one thing every source agrees the Wolf Point tavern was known by is the
painted wolf hung outside it. The chips were true about the evidence and false about the view.
**How to resolve:** rename the two attributes to the parameters the archetype reads and re-bake.
That is a data change plus geometry, and the two have to land in one slice, so it is queued in
`docs/ROADMAP.md` rather than half-done here. Until it lands the record admits the gap.
**Covers:** `wolf_point_tavern.log_frame_1828.form.frame_extension`,
`wolf_point_tavern.log_frame_1828.form.signage`.
**Recorded:** 2026-08-10.
**Resolved:** 2026-08-10 — the two attributes are spelled `frame_addition` and `sign`, the
names the archetype reads, and the tavern was re-baked in the same slice: a frame bay stands
at the north end of the log core and a board hangs from a bracket on the river front. The
record now carries the frame part's side, width, depth and storey count explicitly rather
than inheriting the archetype's defaults, and every invented one of those is admitted in
L24; what the board shows is admitted in L25. This entry stays exactly as written, including
the two spellings that no longer resolve, because a silently corrected admission is not one.


### L21 — Chimneys are counted in the records and fixed in the archetypes
**Decision:** every record states a chimney count and no archetype reads it. `frame_tavern`
builds two stacks at 0.22 and 0.78 of the frontage; `log_dwelling` builds one, at the gable end.
The records that say two get two only where the archetype already built two.
**Why:** the counts were written from the depictions ("both depictions show two") and the
archetypes were written from the same depictions, so they have never disagreed — which is
precisely why nothing caught that they were never connected. Samuel Miller's house is the case
that shows it: the record says two chimneys and the `log_dwelling` archetype builds one.
**Consequence:** a record could raise a chimney count on new evidence and the town would not
change. For Miller's house the model already shows one stack fewer than the record claims.
**How to resolve:** make the count a parameter in both archetypes and re-bake — a small change
on the data side, a geometry change on the other, so it lands as one slice.
**Covers:** `green_tree_tavern.form.chimneys`, `miller_house.form.chimneys`,
`sauganash_hotel.form.chimneys`, `walker_meeting_house.form.chimneys`,
`western_hotel.form.chimneys`, `wolf_point_tavern.form.chimneys`.
**Recorded:** 2026-08-10.
**Resolved:** 2026-08-10 — `chimneys` is a parameter of both archetypes and the number built is
the number recorded. Miller's house has its second stack, on the frame range, which is where the
record's own reasoning for counting two puts it. The `log_dwelling` half was not a missing
feature but a third misspelling of the kind L20 records: the parameter was `chimney`, a boolean,
and no record has ever contained that word — so `from_phase` took its default and built one stack
on every log building whatever the record said. That class of defect is now a test rather than a
discovery (`test_consumed_attributes_actually_reach_the_parameters`): an attribute an archetype
declares it consumes has to change the resolved parameters when its value changes. What this
entry admitted is discharged; what it did not admit — that a stack's position, size and material
are invented on every building — is now stated on its own, in L26.

### L29 — The North Branch bridge stands on fifteen piers nobody recorded
**Decision:** the bridge is built with cribs every 4.5 m, which over its 71.83 m span puts
**fifteen log cribs standing in the river** between the two abutments. The spacing is tagged
`conjectural` on the record.
**Why:** what survives about this bridge is its width, its material and its ends. Cleaver:
"The abutments were built of heavy logs in the shallow water near the banks. These bridges were
ten feet wide." Andreas: "formed of stringers." Nothing anybody wrote describes the middle of it.
Something had to hold up 71.83 m of log stringer, so intermediate supports are not the invention
— their number, their spacing and their form are. 4.5 m is the archetype's own default, kept
deliberately rather than replaced with a fresh guess, because a new number would look like a
finding and would not be one.
**Consequence:** this is the most conspicuous invention in the structure and it is invisible in
the confidence view, because the tint on the piers grades what a crib IS rather than how many of
them there were. A visitor walking the bank sees a regular colonnade marching across the water
and reads it as a fact about the bridge. It is a fact about the archetype. The span it divides is
itself the drawn waterline-to-waterline distance, and Cleaver's abutments stood *inside* that
line by an unrecorded amount, so the true bay count was smaller than fifteen by an unknown
margin.
**How to resolve:** a period depiction or a survey of the crossing. Two are worth trying: the
1834/1835 Wabansia and Kinzie's Addition plat, which is contemporaneous to within two weeks of
the scene date, and Andreas vol. 1 at page-image level, where the bridge prose transcribed here
sits.
**Covers:** `north_branch_bridge.log_1832.form.pier_spacing_m`.
**Recorded:** 2026-08-10.
**Evidence since:** the sentence above — "nothing anybody wrote describes the middle of it" — is
no longer true, and the entry stays here rather than moving to Resolved because the model still
shows fifteen cribs. Somebody did write it down: at the foot of Andreas pp. 631-632 is a
statement signed by J. D. Caton, John Bates, Charles Cleaver and John Noble, agreed at a meeting
of old settlers in the fall of 1883, saying that both branch bridges "were built on abutments and
two 'bents'", each bent "of four heavy logs, resting on the bottom, in deeper water". **Two
intermediate supports, not fifteen**, and bents rather than cribs. It was found by reading the
printed pages either side of the passage this project already quoted, rather than by searching
the index, which does not reach it. Until the record and its re-bake land together the river
still carries a colonnade that the evidence does not, and this admission stands exactly as
written. Source: `old_settlers_bridges_1883`; the finding is
`docs/RESEARCH/north_branch_bridge.md` §6 and the work order is `docs/STATUS.md` §23.
**Revised:** 2026-08-10.
**Resolved:** 2026-08-10 — the mesh shows two bents, so this entry moves here, and not before,
which is what the Revised line above said it was waiting for. `pier_spacing_m` is gone from the
record and from the archetype: `pier_count: 2, documented` replaces it, `pier_kind` is `bent`,
and `bridge_timber` builds four heavy logs under a cap at each of them. The parameter changed
rather than the number, because a spacing is a builder's convenience nobody would remember and a
count is what a user of a bridge does. **What this entry admitted is discharged and what it did
not is now L31**: the letter gives two bents and never says where along the span they stood, so
the positions are still the archetype's, and the tint still cannot say so. The sentence in
**Consequence** about the true bay count being "smaller than fifteen by an unknown margin" turned
out to be true in the wrong direction and by a factor of five.
