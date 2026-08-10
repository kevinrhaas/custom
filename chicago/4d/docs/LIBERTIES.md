# Liberties taken

**Append-only.** Every compression, simplification, and invention gets a row. Nothing is ever
removed from this file; if a liberty is later resolved by evidence, add a line saying so.

The standard, borrowed from the Joliet project in this repo:

> A visitor should be able to tell you which parts we made up.

The per-attribute confidence model in the data covers *attributes*. This file covers the
decisions that do not live in any single attribute — scope, scale, omission, and the choices a
reader would otherwise have to reverse-engineer.

## The `Covers:` field — what an entry claims to discharge

An entry that admits to a **drawn** invention says so in machine-readable form:

```
**Covers:** `sauganash_hotel.log_1829.footprint`, `wolf_point_tavern.footprint`
```

Each token is `structure_id[.phase_id].aspect`, with `aspect` one of `footprint` or `position`.
Naming the phase covers that phase; leaving it out covers whichever of the structure's phases
drew that aspect from nothing. The commit gate reads these claims in both directions: every
`conjectural` footprint or position in `data/structures/` must be claimed by some entry, and
every claim must land on a value that is actually invented. The prose stays the explanation and
the field is the assertion — the gate used to infer coverage from an entry's *wording*, which a
liberty could satisfy by mentioning a footprint while discussing something else.

An entry with no `Covers:` field claims nothing and is still a liberty: omissions,
simplifications, navigation rules and scope decisions have nothing drawn to point at. When
evidence settles a claimed invention, move the entry to **Resolved** — the gate exempts that
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
**Recorded:** 2026-08-09.

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
**Recorded:** 2026-08-09.

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

---

## Resolved

*(none yet — entries move here with the evidence that settled them, and stay in place above)*
