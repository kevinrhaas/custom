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
**Decision:** ambient wildlife is rendered sparsely, with many species present as audio or as
traces (tracks, feeding sign) rather than animated animals.
**Why:** two reasons, both evidential. July is the quietest wildlife date in the Chicago year —
no migration, silent leks, moulting waterfowl — and a summer scene populated with the spectacle
of *other* seasons would be wrong. And a boomtown of 3,265 people is not a wilderness; wild
animal density inside the platted grid was low.
**Recorded:** 2026-08-09.

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
**Covers:** `western_hotel.frame_1834.form.stables`.
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

---

## Resolved

Entries here were true when they were written and are kept verbatim, with a **Resolved:**
line saying what settled them. The gate exempts this section from the check that a claimed
value is still an invention, which is what lets an append-only document survive its own data
being corrected.

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

