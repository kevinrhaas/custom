# STATUS

## Shipped 2026-08-24 — T-0109: the slough crossing spans water, and its card finally says so

**The acceptance, stated before working, because the ticket carried none.** *Standing at the Water
Street crossing, the log bridge spans open water: the watercourse is cut under the deck, its
abutments land on dry bank, the channel runs unbroken from the deck to the river, nothing else is
rooted in the cut, and the crossing's own record — the card a visitor opens — says what it spans in
figures read off the committed heightfield rather than saying the stream is not modelled.* Not
weakened at any point; the fifth clause is the one that was still open.

**The first four clauses were already true, and this run did not make them true.** Measured on the
committed heightfield before anything was edited: along the deck's own 8.00 m span the ground falls
below the 1835 water surface for **3.30 m** (41 %), deepest **−0.53 m**, leaving **2.35 m** of dry
abutment seat at each end; **277 of 277** samples down `state_slough_mouth` from the deck to the
river stand below the water surface; the nearest other structure is **45.8 m** away and no walk,
board fence or street centreline in the scene is rooted on ground below the water surface anywhere
in the crossing's reach — the only thing over the water is the river walk's crossing footway, which
declares `rides: slough_log_bridge`. **T-0005 carved dossier zone 14 on 2026-08-20 (changelog v204)
and T-0118 straightened its last reach square under this deck the same day (v210)**, both filed
after T-0109 and neither aimed at it. The ticket had been describing a state the tree had left —
the T-0151 shape, and the second time this queue has produced one.

**What was actually still wrong is what a visitor reads.** `data/structures/slough_log_bridge.json`
told the card, in three places, that the slough "IS NOT MODELLED IN THIS TERRAIN EPOCH", that "this
bridge crosses nothing a visitor can see", and that "a visitor sees a bridge over nothing" — the
`research_note` verbatim on the card, the `position_note` behind its *why*. `docs/LIBERTIES.md` L69
said the same in the Evidence panel. One of them also pointed at a `ground_contact` block T-0046 had
already removed. All three passages now carry the measurement, plus the one prediction that did NOT
come true: L69 expected the archetype to anchor the deck to a river surface 0.15–0.45 m below the
slough's own, and the drain as built backs into the river as one pool at one surface. The footprint
note's counterfactual — *"if the slough ran 40 ft wide here the span is half what it should be"* —
is replaced by the check it invited: the built carve is **6.0 m** across the top, the span was not
resized, and it clears the carve by about a metre at each end.

**And the joint nobody was watching.** `tools/measure_slough_crossing.py` joins the bridge's
placement to the ground beneath it: it reads span, width, bearing, walk surface, stringer, plank and
clearance out of the committed record, samples the heightfield along the deck's own axis at 0.05 m,
and gates five things — open water under the deck, dry abutment seats, an unbroken reach to the
river, the record's clearance against its own deck build-up, and nothing rooted in the cut that does
not declare it rides the crossing. Wired into `tools/check.sh`. **Proved firing, four ways**: deck
moved 12 m west → *"the deck spans SOLID GROUND"*; deck shifted 1.7 m → *"the deck's west end keeps
0.25 m of dry seat"*; `clearance_m` hand-set to the branch bridges' 6 ft → *"its own deck stands
0.500 m over the water"*; the drain's last vertex walked onto the dry bank → *"320 of 377 samples
… stand above the water surface"*; and a probe fence in the channel → named by id. Tree restored
clean after each. Upstream is deliberately **not** asserted: the record reads the July drain above
its pool as a damp swale standing above the water, so a dry reading there is the claim.

**Nothing in the scene moved, and the changelog says so.** No terrain change was available in any
case — swale geometry is inside the terrain hash, so it costs a Blender bake this runner does not
have; the notes added to `state_slough_mouth` are prose and are stripped from that hash, so they
cost nothing.

**Verification.** `tools/check.sh` **CHECK PASS**. Smoke on the published mirror, mobile 390×780,
**`SMOKE_STAGE=2`** — chosen because that is the stage the crossing is in, not stage 5–6: the river
plank walk's block (T-0119) sits inside `stageOn(2)`, and it is the only place in the suite that
asserts this crossing. **75 passed / 0 failed, zero page errors, 5 m 13 s**, including *"the walker
stands on the planks over the water at the mouth"* (`isWater(809.4, 14.2)` mid-deck), *"the crossing
reads as planks underfoot, and walks off onto the bank"*, and *"the river walk publishes its floor
and registers its crossing deck"*.

## Shipped 2026-08-24 — T-0107: a landing on the west bank at Wolf Point, and a face that has to be afloat

**The gap, and it was a scope gap rather than a finding.** T-0062 shipped five reconstructed docks
on the owner's *"you can add more docks!"* and stated them on **South Water merchants**. That
phrasing is the whole reason the west bank had no landing: the rule was never asked of it. The
North Division shore carried a wharf only because Kinzie & Hunter's dock happens to be attested,
and the west bank at Wolf Point — five buildings, all of them fronting the water — carried none.
Neither T-0062 nor the branch it superseded (#258) had measured that shore and refused it.

**What shipped.** Robert A. Kinzie's storehouse now STATES a dock at `confidence: reconstructed,
geometry: simplified`, and the wharf layer draws it: a **13.0 m** deck on a timber crib, heel
2 m into the traced 1834 west bank, face 6 m out, abreast the store's own east-facing river wall.
**Five landings now stand where four did.** The trade test is written into the rule rather than
into four hand edits, and it is now asked of every river frontage in the town: on the west bank it
selects exactly one record and refuses the other four by their own trades — Wentworth's tavern,
James Kinzie's residence, the Robinson and Caldwell cabins and Father Walker's meeting house state
no dock and get none, which is the Temple Building's exclusion carried across the river. The
invention is claimed at LIBERTIES **L180**.

**What the sources actually carry, and where they stop.** The trade is attested twice —
chicagology's "storehouse dealing in groceries and Indian goods" and Andreas's *"Indian Traders —
Robert A. Kinzie, near Wentworth's tavern"* (scan p. 235). **NO SOURCE STATES A DOCK, WHARF OR
LANDING ANYWHERE AT WOLF POINT**, which is why the statement is `reconstructed` and not `inferred`.
What made this the strong candidate is that the record argued the case itself before any wharf
layer existed: its committed position note of 2026-08-11 reads *"a storehouse trading goods off
canoes has a positive reason to face the landing"* and set the facade due east on that reading. The
placement's own uncertainty is unchanged and inherited whole — about **40 m along the bank** from
the tavern (L7) and about 20 m across it from the georeference — so the landing is as well located
as the store, and no better. The West Water / Canal ambiguity that puts the Green Tree and the
saddlery within ~145 m of doubt does not reach this row: these five records are set by setback from
the modern west-bank line, not off a named street corner.

**The measurement that let it be drawn at all.** The traced 1834 bank runs **11.17 m** off the
store's river wall; a standard-form deck at that foot stands in **1.06 m** of water for the whole
13.0 m of its face on the committed heightfield, heel about 0.5 m clear on dry bank, clearance to
the wall **7.81 m**. The boat layer independently floats a schooner in this same reach abreast this
store (L146 / T-0140), so the modelled bed already carries a hull here.

**A new refusal clause, and it is measured rather than asserted.** The deck outline is a rectangle
set on the bank's own tangent — one standard form, so the dimensions are invented once (L132)
rather than once per site — and **the bank bends at Wolf Point**. A rectangle run against a curve
can put the far end of its face behind the bank, on dry ground: PR #258 measured exactly that at
Hogan's store, whose face runs from 1.10 m of water at one end to **−0.34 m** at the other, and
refused it rather than invent a bespoke outline for one frontage. That refusal is now **clause 6**:
the face is sampled at ~1 m and a deck whose face would stand on dry ground is refused with the
measured rise on the record, the way the trace-reach refusals already carry theirs. The record also
now reports `least_depth_at_face_m` and `face_stations`, so the margin a drawn landing passes by is
on the record rather than in the generator's head.

**THE CLAUSE REFUSES NOTHING IN THE TOWN AS IT STANDS, AND IT IS PROVED ANYWAY.** Every drawn face
is afloat by more than a metre (the least is Robert Kinzie's 1.06 m), so on the committed data the
clause is indistinguishable from no clause. `--selftest` fires the whole clause table on constructed
frontages — a straight bank, a flat bed, one thing wrong at a time — and it runs inside `--check`,
which `tools/check.sh` already invokes, so no new gate step was added. **Negative control run:**
with `if least <= 0.0` replaced by `if False`, the self-test goes red on 2 cases and exits 1. One of
the two cases is a dry patch that falls BETWEEN the three points the record reports, which is why
the run is sampled at 1 m instead of at the reported ends and middle.

**The staleness half.** `log_dwelling_params.from_phase` now excludes `dock` from its confidence
sweep, the same exclusion `frame_storefront_params` made for T-0062. Verified rather than assumed:
`structure_inputs_sha(robert_kinzie_store)` is `e15168f3…` **before and after** the dock statement,
while an unexcluded attribute added as a control does move it. Without this the statement would have
marked the store's committed GLB stale on a runner with no Blender, when not one of its vertices can
move.

**Verification.** `tools/check.sh` **CHECK PASS** (validator, wharf re-derivation + the clause
self-test, liberties compile, changelog contract, published mirror).
`tools/smoke_renderer.mjs --published` — the west-bank leg, mobile 390×780; the wharf census
assertion moved 4 → 5 drawn / 5 keep-outs / 3 refused with it, and `stands.length` with it.

## Shipped 2026-08-24 — T-0093: the verge stops fading through a screen of dots, and the ticket's own two stands say it was only half the near ring's doing

**T-0093, the residue T-0086 wrote down and left.** The far-sward run closed the OUTER edge of the
meadow by replacing a coverage ramp with a density handover, and said in the same STATUS entry that
it had not touched *"the near ring's own outer dither at 5–7.6 m, which is still a screen-door ramp
and is still what a close look at the verge shows"*. This is that run.

**What a visitor sees.** Stand anywhere in open prairie on a phone and the grass from about two
paces out to about four was drawn as a mesh of dots — every tuft in the middle of the frame carved
into dotted vertical columns by an ordered 4×4 screen door. It is written solid now. On a desktop
the same band sits at 4.8–7.0 m and the effect is subtler but present; it is gone there too.

**The measurement, and the instrument, because there was none.** `tools/measure_near_verge.mjs`
reads every flora instance's own `aChiRing` back off the buffer that went to the GPU and applies the
vertex program's own expression, so a plant is classed exactly as the shader classes it: `whole`
(coverage 1, written solid, the fragment guard skips the Bayer branch), `partial` (0 < coverage < 1,
every fragment thresholded — *these and only these are the dots*), `absent`. It then projects each
drawn plant's own recorded height and spread to screen and sums the footprints, because a hundred
plants at forty metres are four pixels and the complaint is about SCREEN. Mobile runs at
`deviceScaleFactor: 1.5` rather than the smoke's 2, so one measured pixel is one drawing-buffer
pixel — the screen door is locked to `gl_FragCoord` and a 4/3 resample smears the grain being
measured.

Screen-doored share of the frame inside 9 m, published mirror, before → after. The bracketed
figure is the same union less the footprints of the solid plants standing in front of it, so the
pair is a ceiling and a floor on the same thing:

| stand | mobile `light` | desktop `full` |
|---|---|---|
| South Water approaching Wells | 0.000 → 0.000 % (0.000 → 0.000) | 0.000 → 0.000 % (0.000 → 0.000) |
| the same, from the verge | 20.788 → **2.081** % (5.073 → **0.058**) | 11.973 → **0.000** % (0.398 → **0.000**) |
| Wells approaching Lake | 1.729 → 1.729 % (0.937 → 0.937) | 14.843 → **0.000** % (5.178 → **0.000**) |
| open prairie | 53.654 → **15.395** % (6.198 → **0.136**) | 45.173 → **0.000** % (0.264 → **0.000**) |

**`flora-near` carries no partially-covered instance at any of the eight readings**, against 198 and
174 at the open-prairie stand alone before; and **no plant at any stand is caught mid-ramp on either
converted boundary** — 0 of 0, which is the gate. At `full` the verge is clean everywhere. What is
left on a phone is the mid and forb rings' own OUTER ramps, which at `light` reach in to 5.4 m and
7.4 m — see *What this run did NOT do*. At **Wells approaching Lake on a phone the reading does not
move at all, to the pixel**: at `light` there is no near ring in frame there and the mid ring's
inner ramp had only four cards in it, so everything screen-doored at that stand is the outer ramp
this run does not touch. That is the honest reading and it is banked as such.

**And the sward is exactly as thick as it was.** Counting green-dominant pixels in the same frame
before and after, open prairie at 390×780: the middle band (rows 50–72 %) **54.17 % → 54.52 %**, the
foreground (rows 72–100 %) **79.61 % → 79.99 %**. Half a plant drawn everywhere and a whole plant
drawn half the time come to the same cover, which is the arithmetic in `slotRing` read back off the
picture.

**THE PRIME SUSPECT IS ONLY HALF THE AUTHOR, and at the ticket's own two stands it is none of it.**
T-0086's two stands are both in a roadway, and `station()` clears every plant off the travel track —
10.5 m wide on South Water, 7 m on Wells. So at *South Water approaching Wells* the near ring places
**0 tufts at `light` and 1 at `full`**: there is no near ring there to dither. At *Wells approaching
Lake* on a phone the near set is empty again and **every screen-doored pixel of the verge is written
by the mid ring's inner ramp fading IN across 4.5–7.5 m** — the other side of the same handover,
which the ticket names as existing and does not name as an author. Only in open prairie and on the
verge proper does the near ring dominate (5.90 % against the mid ring's 3.65 % exposed, mobile).
So the fix takes **both** sides: the near ring's outer edge and the mid ring's inner edge.

**And the band is not where the ticket says.** `ringsFor` insets every fade ring inside its own
lattice by the 0.6 m rebuild step, so the near ring's ramp runs **4.80–7.00 m** at `full`, not
5.4–7.6 — measured, as the `d` range of the partial instances. At `light` the ring is 4.6 m and the
ramp is **1.80–4.00 m**, which is under the walker's feet rather than ahead of them, and is why the
phone frame is the dramatic one.

**The fix is T-0086's own answer, applied to a ring that still has an edge in it.** Two flags in
`TUNE` — `near.spreadOuter` and `mid.spreadInner` — move the band out of the ring the shader ramps
and into a per-slot SPREAD of the boundary itself: a slot's own outer radius is
`fade[0] − band × handoverRank(e, n)`, world-anchored and quantised to ⅛ m exactly as `farRank` is,
and the ring the shader reads is a step (`HARD = 1e-4`). The fraction of slots drawn at distance `d`
is then `clamp((fade[0] − d) / band)` — *the same number the alpha ramp used to write* — so the
expected ground cover across the band is unchanged to the arithmetic and every tuning figure still
means what it meant. What is gone is the stipple: a plant is drawn whole or not at all, and a
stochastic density ramp has no edge in it to dither.

**What did NOT change, and it is most of the file.** Placement is untouched — every lattice slot is
still dealt a species and still counted by the drawn census, so no community's population or cover
figure moves. The mid ring's *outer* fringe, which is what keeps the sward's boundary off a constant
screen row (§ S6a item 3), is untouched. Heights are untouched (T-0035: the ramp has never been a
height since). The near ring pays *less* fill than before, not more: a plant outside its own ring
collapses to a point in the vertex program instead of rasterising and discarding half its fragments.

**The gate, and it fires.** `--gate` asserts one thing strictly: **no plant is caught mid-ramp on
either converted boundary**, zero rather than small, because a boundary handed over by density
cannot produce a coverage strictly between 0 and 1. Proved red by putting the pre-T-0093
`flora.js` back into the published mirror and re-running: *"253 plant(s) caught mid-ramp on the
near/mid handover, covering 53.277 % of the frame"* — 198 near tufts on the outer ramp and 55 mid
cards on the inner one — plus the banked-residue check, *"screen-doored verge grew 15.395 % →
53.654 %"*. Republished, the same command prints **GATE PASS** and reproduces 105 373 px to the
pixel. The residue that T-0093 does not close is banked in `tools/near_verge_baseline.json` and
held against regression rather than against a constant.

**`HARD` is a micron, and that is a measured figure.** The step the shader is left holding has to
be narrower than the old 1e-4 floor in `fadeOf` and in the GLSL: simulated over 40 000 slots, a
0.1 mm band still catches one to three of them mid-ramp — a plant whose own boundary happens to
fall within a tenth of a millimetre of the camera as it passes. Invisible, but not zero, and zero
is the assertion worth being able to make. So the division floor moved to 1e-6, where world
positions are float32 at 800 m and already spaced ~60 microns apart, so the difference the shader
computes cannot land inside it at all. `FAR_RING` keeps its own 1e-4 — an outer radius of 1e9 is
never within a millimetre of anything.

**Two things follow that are worth stating.** The flower heads ride their PLANT's ring now rather
than the layer's — on a spread boundary the layer's ring answers for no particular tuft, and a head
hung on it would be drawn out to 7 m over a plant whose own handover had already taken it away at
five, which is R-BUG7 rebuilt from the other end. And `flora.fadeAt`/`heightAt` take the whole
four-number ring now, not just the outer radius: with the mid ring's inner boundary spread per slot,
a reader carrying only the outer one would be told every mid card past 4.5 m is drawn. The pop-in
gate and the boundary gate in `tools/smoke_renderer.mjs` were updated to pass all four, which makes
them read the drawing more exactly, not less.

**What this run did NOT do.** The mid and forb rings' own OUTER coverage ramps are still screen-door
ramps, and at `light` detail they reach in as far as **5.4 m** and **7.4 m** — inside the verge on a
phone. That is a different edge from the one T-0093 names (it is the mid→far handover, which T-0086
answered by standing the far band over it rather than by converting it) and it is the residue this
run's gate holds against regression rather than closes. It is filed as its own ticket.
## Shipped 2026-08-24 — T-0094: the fort's pickets were never flat-topped, and the plate never drew them pointed

**Nothing in the scene moved, and that is the finding.** T-0094 said *"the fort's pickets are
flat-topped and dark, where the plate draws them pointed and pale."* It came off row 3 of
`docs/RESEARCH/fort_dearborn_image_accuracy.md`, which read the plate by eye and the model by eye.
**Both halves are wrong, and `tools/measure_picket_plate.py` now holds the numbers.**

- **The model.** `generators/archetypes/palisade.py::_picket` has built a four-triangle sharpened
  head on every post since the archetype was written. The committed master agrees without being
  asked: 21,504 picket positions on three heights — 6,144 feet at 0.000 m, 12,288 shoulders at
  3.388 m, **3,072 apexes at 3.700 m**, four per post over 768 posts. **0.312 m of head, 8.4 % of
  the picket.** It reads at the wall and it still reads from `p4_0`'s own stand.
- **The plate.** `p4_0` rules the curtain's top **flat** — 0.45 px rms over 138 resolved columns,
  peak-to-peak 2.0 — while resolving individual pickets at a **10 px pitch** on a **43 px** wall, so
  a head of the model's proportion would have serrated it by 3.6 px, eight times the residual.
  `p4_1` rules the same cap. The draughtsman had the resolution and drew none.
- **The tone.** The plate paints this one continuous wall across **1.85×** of tone in a single
  view — lum 191 east of the gate work, 103 west of it — and `hewn_log`, the surface shipped, is
  **lum 143, between them**. A plate that draws half a stockade darker than the model and half
  paler warrants moving it in neither direction. The whitewash stays refused: Fergus's board fence
  is the enclosure of 1850.

**What the run changed, honestly:** the card. A visitor who opens the stockade now reads that the
point on every picket is ours, what the plate does and does not show, and why the tone was not taken
from it — none of which the record said before. **L179** records the head as the invention it is;
L47 had covered "the fabric" in general and never named the most conspicuous part of it.

**Held so it cannot be re-filed off a screenshot:** `tools/measure_picket_plate.py --gate` in
`check.sh` refuses a stockade whose apexes have gone flat, been capped, worn under 4 % of the
picket, or been stacked on top of a full-height post. Proved red end to end against a real GLB with
its 3,072 apexes rewritten to the shoulder. The plate half of the same file **reports and does not
gate** — a tier-5 retrospective lithograph may refute a claim made about itself and may not hold a
build red.

**Not done, and stated rather than skipped.** The acceptance also asked the record to carry the head
as a **form value**. It cannot without a bake: `generators/mesh_inputs.py` hashes the resolved
parameters, and any new key under `form` restales the GLB — verified, not assumed — and there is no
Blender on this runner. The head is therefore declared in prose, in the liberty and in the gate, and
the form attribute is left for the run that has a bake. What the plate DOES say about the pickets —
its rhythm is nearly three times coarser than the model's — is **T-0185**.

Evidence: `docs/evidence/t-0094-plate-vs-model.png`, `docs/evidence/t-0094-p4_0-stand.png`.
## Shipped 2026-08-24 — T-0111: Dearborn's worn track reaches the causeway, on a second line

**The defect, measured before anything was changed.** `renderers/web/js/streets.js` draws its ribbon
from `path_local_enu_m`, and Dearborn's ends at `[699, 18]` — on the crest of the `dearborn_south`
approach fill, **2.70 m south of the deck**. Probed on the shipped build at 0.5 m stations up the
street's own centreline: **covered through n 18.0, uncovered from n 18.5**, with the ground dry and
above 1.97 m the whole way. The ribbon was not being clipped, refused or under-refined — T-0110 had
already fixed all three. It ended where the record ended, and the visitor climbing from South Water
crossed a band of bare crest to reach the bridge.

**THE ONE-LINE FIX IS THE WRONG FIX, AND IT WAS RUN RATHER THAN ARGUED.** With `[697.65, 20.7]`
appended to `path_local_enu_m`:

| gate | committed | with the bend appended |
|---|---|---|
| `generate_plat_lots.py --check` | 19 blocks, 144 lots verified | **PLAT GRID DRIFT** — `thompson_lots.json` no longer what the module re-derives |
| `measure_corridor_intrusion.py --gate` | 29 laps (29 committed) | **30** — `dearborn_street_drawbridge:draw_1834` newly laps dearborn by **0.66 m** |

Both re-verified green after the revert. T-0110's PR had reported the same thing; this run
re-measured it rather than inheriting it.

**The fix: a second line, and only the renderer reads it.** `drawn_track_local_enu_m` is optional,
per street, and carries the worn wheel line; `path_local_enu_m` stays the plat and stays what
`generate_plat_lots.py`, `plat_corridors`, the lot schedule, `hitsAt`/`status` (the street readout)
and `blocksGrowth` (the flora clearing) read. `prepare()` in `streets.js` exposes both as `path` and
`drawn` — `drawn` IS `path` for the seventeen streets that author no track — and only `addRecord()`
prefers `drawn`. `bounds` covers both, since a box that excluded the drawn line would answer "not
near this street" for ground the street is drawn on.

**Dearborn's track:** `[[696.4, -400], [698.932, 7.0], [697.65, 20.7]]`. It leaves the platted line
where South Water crosses it and runs one straight 13.76 m chord to the deck. The end point is the
south edge midpoint of the drawbridge's committed footprint AND `line[0]` of the `dearborn_south`
approach — two existing records that already agree where the boards begin. **Why swing at all,
measured:** held on the platted line the track's east edge stands 4.87 m off the fill's axis, 0.87 m
outside the 4.0 m half-width the earthwork is level across; swung onto the axis, all 7 m of width
ends on the level crest. Recorded as **L178**.

**The artefact it admits to, and the number.** Ribbon panels are drawn square to their own chord and
are not mitred, so a turn opens a wedge on its outside. A 2 cm plan probe of drawn triangles inside
the nominal ribbon: **0.30 m² uncovered** at the one joint (a 0.61 m² sector, half of it painted over
by South Water's own 10.5 m roadway), 0.17 m at its widest, inside the 0.84 m the road texture's edge
already fades across. **An eight-chord easement was measured first and was seven times worse
(2.18 m²)** — eight joints turn eight times — which is why the swing is one chord. Mitred joints are
filed as **T-0184**, which also names South Water's own 17.9-degree bend at `[140, -35]` (a ~4.3 m²
sector on a 10.5 m track, standing since the street layer shipped).

**Bounded rather than trusted.** `compile_scene.py` refuses a drawn track that leaves its own platted
corridor, that overhangs the platted line's ends by more than `DRAWN_TRACK_OVERHANG_MAX_M` (4.0 m;
Dearborn uses 2.69), or that carries no `drawn_track_note`. **All three proved red** by breaking them
one at a time and restoring.

**Two instruments were taught the second line, and neither was weakened.** The smoke's panel
accounting re-derives the module's arithmetic, and `drawn_placement_census.mjs` asserts every drawn
vertex owes a committed centreline within its own half-width; both now read `drawn ?? path`. Measuring
a ribbon against a line it was never drawn from would report a stray for authored data and miss the
mirroring the census exists to catch. The smoke's T-0110 approach stations now run **n 8 → 20.5 at
0.5 m** (was 8 → 17.5 at 1 m) on the drawn line — the comment that used to say the last 2.7 m were
outside what the gate could see is gone with the gap.
## Shipped 2026-08-24 — T-0143: the corner clause, demonstrated at Washington and Dearborn

**The succession T-0105 owes.** T-0079 raised the core density standard and demonstrated it on
`blk_lake_clark`; T-0105 carried it to `blk_randolph_dearborn` lot 4 and wrote in as many words
that the back face was the successor's to deal. This is that successor, and it takes the block's
last **four roofs of headroom**: three principal roofs in a party-line run on lot 1 and the barn
that belongs to the lot they stand on. `blk_randolph_dearborn` now stands at 17 roofs and one free
lot, and it stays `open` in the schedule.

**THE CORNER CLAUSE IS THE POINT, and this is the first parcel able to demonstrate it.** The
standard has three clauses; T-0105 could apply two and recorded that lot 4 was an interior lot, so
*a corner lot builds to the corner* had nothing to bind on. Lot 1 is this block's one free corner
lot. The run is anchored `corner: west` — packed EAST from the Washington-and-Dearborn corner,
1.5 m clear of the side line, that margin being the plat module's own and not a measurement — so
it occupies 19.30 m of the lot's 22.90 m of buildable frontage and the spare metres are at the far
end, away from the corner. An east-anchored run would have left the corner itself empty, which is
the shape of frontage the standard exists to reach.

**Clause one does not bind here, and the parcel says so rather than pretending.** `tools/
measure_street_frontage.py randolph washington dearborn state` reads, on the committed dataset:
Randolph 7 documented / 7 inferred, **Washington 1 / 0**, **Dearborn 6 / 1**, State 3 / 0. Randolph
is this block's business face and the first two deals took every free lot on it. So the ground this
row is built to is not valuable for the street it fronts; it is valuable for the street it stands
at the end of — Dearborn, the only crossing of the main stem in July 1835 — and the row is graded
on T-A11's end rule the same way T-0105 read it: the largest roof nearest the crossing (H1), a
one-room frame cottage next (D3), an older log cabin closing the run at the east end (D1).

**H1 is the first H-family roof this generator has ever stood.** T-0105 was dealt two H slots and
had to refuse both — H1 at this generator's flat 44.0 deg pitch stands outside the 8:12–11:12 its
own crosswalk entry cites — and T-0142 made the H families buildable at every size the schedule may
deal them. This is that repair carrying its first building.

**A REAL PLACEMENT FAULT, FOUND BY BUILDING ON A FACE THAT IS NOT THE NORTH ONE.**
`place_frontage` walked back from a unit's east wall by placing the footprint's (0, 0) corner at
`east - width`. That is right exactly when the footprint's own +u axis runs WITH the face's
`along` — true on a north or west face, false on a south or east one, because `rotation_deg` is the
facade bearing and the u axis is the outward normal turned a quarter turn. Every frontage run this
project has ever built stood on a north face, so the arithmetic was right on all twenty committed
units and wrong the first time it met a south face: each unit landed a **full width** west of the
party wall it declared. `check_frontage` refused it —
*"recon_1835_blk_randolph_dearborn_d3_15 stands 5.202 m from the party line it shares with
recon_1835_blk_randolph_dearborn_h1_14"* — which is the assertion earning its keep, because it
measures the geometry rather than reading back the recipe that produced it. The fix derives the
sign from the bearing and the face, and refuses a bearing that does not lie along the face at all.
**No committed record moves:** `u_along` is +1 on every north face, so `along_0` is `east - width`
exactly as before, and the twenty South Water and Randolph units re-derive byte-identical.

**Lot 1 leaves the two earlier entries' `open_lots`.** The lot-accounting gate refuses a lot that
is both *named open in the recipe* and *built on by another deal on this block*, and lot 1 is now
the second. Their stated reason for leaving it open — a civic roof the first deal deferred, and a
back face the second deal was not dealing — is answered rather than overturned, and it is quoted in
the third entry's `arrangement_note`. **Lot 5 stays open:** capacity is a ceiling and not a target.

**The 665 total does not move.** The four roofs come out of `south_plat_beyond_committed_control`;
`tools/reconcile_665.py` re-derives 338 standing / 327 remaining and every marginal still sums to
665. The town census reads 338 buildings standing, 142 people housed.

**Before and after, from one stand** — `tools/shoot.mjs . /renderers/web/ --at 700,-400,40`, in
Washington Street looking north-east at the corner:
`docs/RESEARCH/washington_dearborn_corner_before_2026-08-24.png` (empty grass to the block's
interior) and `…_after_2026-08-24.png` (the three-unit row built to the corner, its barn behind).

**Derivations regenerated in the same commit:** the four records and their Blender bakes, the web
derivatives, the sidecars (`compile_scene.py --all`), the dooryard pickets, the lot-line yard
fences, the dooryard plantings, the business signboards, the yard goods, the lot building material,
the frontage works, the 665 programme, the town census, and the published mirror.

**What is unverified is everything that matters:** that any building stood on this ground, that
there were three of them, that they stood shoulder to shoulder, and that the largest took the
corner are all inventions of this programme. The side lot lines the row crosses between its own
units are conjectural; the block face it stands on is committed geometry derived from the street
centrelines, which is the unit the standard counts in.

## Shipped 2026-08-24 — T-0103: seventy-eight roofs stop fronting the middle of their own block

`docs/GLB-CONTRACT.md` pins `rotation_deg` as **the facade bearing, 0 = facing north** — the way
the front looks. `tools/generate_block_infill.py`'s `place()` derived it from `inward`, the vector
running from the lot's street edge INTO the lot, so every roof it stood was exactly 180 degrees out
and presented its blank rear wall to the street. **78 records across all fourteen platted blocks**,
every one of them since the first block was dealt.

```
-    bearing = math.degrees(math.atan2(inward[0], inward[1])) % 360.0
+    bearing = math.degrees(math.atan2(-inward[0], -inward[1])) % 360.0
```

**Nothing moved.** `place()` derives the footprint's (0, 0) anchor from the same bearing, so a flip
rotates the rectangle about its own centre: measured across all 98 block records, the largest
centroid shift is **1.4 mm**, which is the millimetre rounding on `utm_e`/`utm_n` and nothing else.
The corridor-intrusion, reserved-ground, refused-ground, separation and occupancy gates are all
green unmoved, because none of them measures which way a building looks. The 20 frontage-row
records are untouched: `place_frontage` has always taken `face["bearing"]` off `tools/block_faces.py`,
which reads the block face's OUTWARD normal — which is exactly why the fault could stand beside the
South Water row (L142) for a week without looking wrong.

**What it looks like.** `tools/shoot.mjs ../../site/chicago/4d /walk/ --at 390,-255,180` — standing
in Randolph Street looking south at the north tier of `blk_randolph_wells` — before: two blank
clapboard walls with the openings of the far tier showing past them. After: four and five bays of
door and window across both street walls, and both chimneys moved to the front slope.

**The gate that should have caught it now exists.** Every gate this generator carries measured
WHERE a building stands; none measured which way it looks. `check_block` now holds every record
against `face_frame(grid, <the face it fronts>)["bearing"]` — a derivation from the block boundary,
independent of the lot polygon `place()` reads — with the alley cases held against that bearing
plus 180. The tolerance is 5 degrees, which covers the committed plat's own skew (up to 2.6 degrees
on the West Division blocks) and cannot admit a flip. **Proved red:** restoring the old line makes
`generate_block_infill.py --check` fail on `recon_1835_blk_randolph_wells_h2_01`, *"179.9deg off the
0.47deg its face looks"*.

**Derivations regenerated in the same commit:** sidecars (`compile_scene.py --all`), the dooryard
pickets, the lot-line yard fences and the dooryard plantings — each of which reads the sidecars.
The signboards, yard goods, frontage works, building-material and placeholder-GLB derivations
re-verified unchanged; `validate.py --stale` is green, so **no bake is owed** — a 180-degree turn is
placement, not mesh.

## Shipped 2026-08-24 — T-0165: the bake's smoke is its own job, and the nightly fits its ceiling again

**Run #261 was cancelled at 43m51s of a 45-minute job, inside the desktop half of the published
smoke.** It was the first bake since 2026-08-22 to get past `check.sh` — and getting there is what
exposed the fault, because `tools/bake.sh` runs the full two-viewport smoke, **unstaged**, as its
last step. ~12 minutes of generate-and-bake plus ~13 a viewport is ~38 before setup, against 45, on
a shared runner. It fitted only when nothing else contended.

| run | bake step | reached | outcome |
|---|---|---|---|
| #258 | 11m41s | `check.sh` | FAILED — `estray_pen` (T-0161) |
| #261 | **43m51s** | **desktop smoke** | **CANCELLED — the ceiling** |

**Nobody had seen it because two earlier faults never let a run get that far.** K38 (T-0160) and
`estray_pen` (T-0161) each killed the bake before the smoke. *"The bake is broken"* was **three
faults wearing one symptom**, and this was the last.

### What shipped: three jobs where there was one

```
bake     generate, derive, publish, gate     SKIP_SMOKE=1   ~15 min
smoke    the published mirror, per viewport  matrix         ~15 min each, PARALLEL
open-pr  the PR — only once smoke is green
```

**The gate is still both viewports and nothing less**, which is `smoke_renderer.mjs`'s own rule.
Each matrix leg prints *"NOT THE FULL GATE"* because alone it is not one; the two legs together are,
and `needs: smoke` fails if either fails. **The workflow reconstitutes the gate the suite refuses to
let a single filtered run claim.**

### The two cheap fixes were refused, and the ticket said so before the work started

Raising `timeout-minutes` or setting `SKIP_SMOKE=1` for good would have made the nightly green
tonight and stopped it testing the bytes it publishes — the exact property `bake.sh`'s own comment
was written to protect, after a bug that collapsed every building to a two-metre box shipped past a
fully green gate **twice**. `SKIP_SMOKE=1` IS set in CI now, so **`bake.sh`'s comment is corrected in
the same commit** to say where the property went, rather than leaving the next reader to conclude
the nightly stopped testing itself.

### Three details that are the difference between this working and looking like it works

- **The mirror travels as an artifact.** The smoke job serves the bytes THIS bake published, not
  whatever is committed on dev. Without it, any run that produced changes would silently smoke the
  wrong bytes — the one property the split must not lose.
- **The committed mirror is deleted before the artifact is unpacked.** `checkout` restores it as
  committed and `download-artifact` *overlays* rather than replaces, so a file the bake deleted
  would survive and the smoke would test a tree that never existed.
- **The branch is pushed before the smoke, the PR opened after.** A red smoke costs a review, not
  twenty minutes of Blender output — the salvage argument from polecat-platform #140 — while a bake
  whose mirror fails is never advertised as ready to merge.

**And one liability removed rather than added:** the first draft pinned `NODE_PATH` to
`/usr/local/lib/node_modules` in the smoke job. `smoke_renderer.mjs::loadPlaywright()` already falls
back to `npm root -g`, so the pin bought nothing and would break the day the runner image moved it.

**Demonstrated before pushing:** the suite driven against a detached copy of the mirror at
`SMOKE_ROOT`, exactly as the job will — *"serving …/mirror — PUBLISHED mirror (compressed assets,
visitor layout)"*, **141 passed, 0 failed**. That is the artifact hand-off proven, not assumed.
Playwright is also dropped from the `bake` job, which no longer launches a browser.

## Refuted 2026-08-23 — T-0018: a spatial filter cannot bias the sward's rank deal, and the standing instruction that said it could is struck

**K49(d) left a sentence in `flora.js` that has been telling every later parcel what not to
do.** In `stratum`'s doc block, on the two census rows that got worse:

> Rank is a deterministic function of position inside the block, so a filter that runs AFTER the
> deal on a spatial rule of its own — `station()` refusing a building footprint or the far side
> of a waterline — selects a **BIASED** set of ranks … That is the leading explanation and it is
> not proven; K49(e) measures it. **Do not reach for `stratum` in a heavily filtered layer until
> it has.**

K49(f) refuted the settled-town half the same day by fixing something else entirely — the fixed
grid — and left the riverbank's residual as all K49(e) had to explain. **The mechanism itself was
never tested, and the prohibition has stood for a week on an unproven sentence.** That is the part
worth settling: the number is one row of a census that has moved many times since, and the sentence
is an instruction.

### The mechanism is refuted, and it could not have been true

`tools/measure_rank_bias.mjs` — new, 0.4 s, no browser. Position → rank is
`feistel(idx, half, blockHash)`, and **`blockHash` is `hash3(bc, br, salt ^ STRAT_SALT)` — re-keyed
in every block.** A spatial rule does not know that key, so the ranks it accepts are an arbitrary
subset, independently re-drawn block by block. Pooled over blocks they are uniform. Bias would
require the filter to correlate with a hash of the block's own coordinates.

Measured over **400 independent layer keys**, χ² on 15 df against uniform:

| arm | slots kept | rank χ² | mix dev /100 | p95 |
|---|---|---|---|---|
| `none` | 100.0 % | 0.0 | 0.83 | 1.25 |
| `halfplane` — a waterline | 61.6 % | **2.0** | 3.33 | 6.76 |
| `disc` — a building footprint | 58.8 % | **4.1** | 5.01 | 8.69 |
| `stripe` — a street corridor | 72.1 % | **2.3** | 3.22 | 5.91 |
| `blind` — rank-blind control, same rate | 64.9 % | 4.7 | 4.54 | 7.78 |
| **`rank_low` — a filter that READS the rank** | 56.3 % | **100,800** | 60.46 | 80.42 |
| `independent` — the pre-K49(d) draw | 100.0 % | 0.0 | 5.83 | 9.90 |

The critical value at p = 0.001 is **37.7**. The three real shapes sit at 2.0, 4.1 and 2.3 —
indistinguishable from the rank-blind control. **The instrument goes red by four orders of
magnitude when there is something to catch**, which is what makes the green readings a measurement
rather than a gate that cannot fail.

### The alternative, named: a filter costs precision, not accuracy

The stratification's whole benefit is that a block's `u` are equally spaced, so a CDF band takes its
exact count rather than a Poisson one. **A filter keeping m of n slots keeps an arbitrary m-subset,
which is not equally spaced** — so the deal slides back towards an independent draw at about the
rate it thins. Unfiltered **0.83** per 100 planted slots; thinned to ~60 %, **3.2–5.0**; an
independent draw, **5.83**.

**So the rule is the opposite of the one that was written.** Reach for `stratum` in a filtered
layer — filtered, it still beats an independent draw. Expect precision to degrade with filtering;
do not expect a lean. The doc block in `flora.js` now says that, with these numbers.

### And the row that opened the ticket is a draw, not a fault

`z05_riverbank_timber` reading the wet prairie draws **44 slots** today and deviates **5.24**. Asked
what a deviation that size looks like when nothing is wrong — one block thinned to about that
count, over 400 keys:

| filter | slots drawn | mean deviation | p95 |
|---|---|---|---|
| `halfplane` | ~40 | **7.17** slots | 27.57 |
| `disc` | ~38 | **6.10** slots | 11.81 |
| `blind` | ~42 | **5.89** slots | 10.26 |

**5.24 is below the mean of all three.** The riverbank row is not merely explicable — at that sample
size it is better than an unbiased, correctly-working filtered deal typically manages. There is
nothing left to explain, and K49(e)'s residual is closed rather than carried.

### It measures the shipped code, and refuses to measure a copy of it

Every primitive — `hash3`, `frac`, `feistel`, `stratum`, `blockPhase`, `morton`, `spread16`, `vdc`,
`stratumHalf`, `pick`, `dealt` — is **extracted from `renderers/web/js/flora.js` at run time by
slicing its source**, not retyped in the tool. `scatter`'s index arithmetic is inline and cannot be
sliced by name, so the six expressions the tool reproduces are asserted to appear verbatim before
anything is dealt. **Both guards were demonstrated firing, `rc=2` and named:** renaming `stratum`
gives *"function stratum … is not a top-level declaration any more"*, and changing `nSlots`'
expression gives *"scatter's deal has changed and this tool still reproduces the old one"*. The
tree restores to `rc=0`. What the second guard does **not** catch is a new step *added* between
those lines; that is written down in the tool rather than left to be found.

**The self-test is now in `tools/check.sh`** — the control pair runs on every gate, so the day
someone makes the deal rank-correlated the claim stops being refuted there, not in a census six
weeks later. The first version of `sliceFunction` looked for `}` in the first column and was wrong
on the first file it read: `frac` is a one-liner, so the slice ran on for 112 lines and swallowed
`const STRAT_SALT`. It failed loudly as a duplicate declaration rather than quietly; it now balances
braces, skipping strings and comments.

**Nothing in the renderer's behaviour changed** — the only edit to `flora.js` is the doc block, and
renderer files are outside `mesh_inputs.py`'s staleness hash, so no asset is stale and no bake is
owed. No threshold moved, no data record changed.

**Gates.** `tools/check.sh` green, now carrying the new self-test. Published smoke, all four stages
at both viewports: **888 passed, 3 failed** — the same road-contrast bands R-W1, R-W2 and R-M1c own,
and **the same 888 / 3, digit for digit, as the run on the commit before this one.** That identity
is the control: a doc-block edit to a renderer file should move nothing, and it moved nothing.
Desktop stage 4 first came back as a harness error rather than a result — the 800 s per-command
`timeout` killed it while four stages ran back to back on a contended runner — and passes 152 / 0
when run alone. Recorded because a killed run and a failed run print differently and only one of
them is a smoke result.

## Corroborated 2026-08-23 — T-0018 in the REAL scene: the placer's own filters, measured where they run

**Read the entry above first: it is the refutation, and this is the second half of its evidence.**
The two runs took T-0018 in parallel and neither's `inflight` check could see the other. The entry
above settles the mechanism *in principle* — 400 synthetic layer keys, three modelled filter shapes,
χ² against uniform, and a rank-reading arm that goes red by four orders of magnitude. This one asks
the same question of the real thing: not a `halfplane` standing for a waterline but `station()`
itself, over the actual town, the actual river and the actual building footprints, at ten stations.
**Two instruments, two constructions, one answer** — and the second closes the one gap a synthetic
model leaves, which is whether the filters the placer really runs behave like the shapes that stand
for them.

**They do, and the answer is no — the other way round.** Over **7,844 slots dealt in 29 rows, of which
the two filters refuse 23.4 %**, the survivors are spread across their species lists **more** evenly
than a rank-blind subsample of the same size: pooled 0.65 of the rank-blind figure, median row 0.65,
worst row in the scene 1.11. And the riverbank row the parcel was left on refuses **0.0 %** of its
slots — 44 dealt, 44 drawn — so no filter can be carrying any part of its residual. That residual is
the deal's own discrepancy at a 44-slot population, which is the alternative the parcel was required
to name.

### The instrument, which is a decomposition rather than a correlation

The box asked for a correlation column: reject fraction against the change in deviation, across
sixteen rows. `deviation` is a functional of the survivors' ranks alone, so it can be put exactly
instead. `flora.js` now counts each species' slots at the moment of the deal as well as after the
filters — the same census one step earlier — and the tool reports

* `dealtDev` — the discrepancy the deal has **before** any filter;
* `B = Σ|drawn_i − q·dealt_i|` — how far the survivors are from the filter having taken the same
  fraction `q` of every species, which is zero for a perfectly even filter;
* `Bnull` — what `B` reads when the mechanism is absent, the hypergeometric mean absolute deviation
  of a rank-blind filter of that size.

`B/Bnull ≈ 1` refutes the mechanism for a row; `≫ 1` proves it. Nothing in the scene is above 1.11.

**It was shown red before it was believed.** Two controls run on the real dealt vectors, 200 trials
each: a genuinely uniform subsample of the same size reads **0.96–1.03**, so `Bnull` is calibrated;
one that rejects wide clumps preferentially — `crowdsTheWalker()`'s own rule — reads **3.92–5.00**.
The instrument can see the mechanism. It is not there.

**Why the reading is below 1, stated as reasoning and not as measurement.** `station()` refuses
ground in contiguous patches, and a contiguous patch is close to whole blocks. A whole block is a
complete stratum — one slot of every rank — so removing complete strata leaves the remainder exactly
stratified. The permutation K49(d) finding 3 called the danger is what makes the filtering safe.

**What this licenses.** `stratum` may be used in a heavily filtered layer. Filtering costs a layer
its SIZE, and a smaller population has a larger per-slot discrepancy for that reason alone
(`z09_sand_prairie` reading the mesic list: 51.8 % refused, `dev/100` 1.08 → 2.63, still below what
rank-blind filtering of that size predicts). It does not cost the layer its stratification. A census
row that got worse behind a filter should be blamed on the deal or on the row's size, and the tool
now prints both columns to say which.

**And the row that opened the ticket is not a draw either — nothing is filtered there at all.**
The entry above shows 5.24 sitting below the mean deviation of three simulated filters at that
sample size. In the scene the row deals **44 slots and draws 44**, refusing none: `dev/100` is 11.91
before the filters and 11.91 after. There is no filter to explain, at any strength.

**Nothing a visitor can see changed**, and the parcel carries K49(e)'s written exemption: a
gate-shaped measurement blocking a named parcel — every future use of `stratum` in a filtered layer.

**Verification.** `tools/check.sh` green · `node tools/measure_sward_draw.mjs` on the source tree and
on the published mirror, both viewports · `tools/smoke_renderer.mjs` staged over both viewports. One
finding filed on the way: `SWARD_VIEWPORT=mobile` changes the browser page size but not `lowSpec`,
so the two viewports deal identical censuses where the tool's own header says the viewport decides
the ring sizes.

## Shipped 2026-08-23 — T-0020: the shrub's last 4.4 points of shell, bought for three per cent of a frame

**ROADMAP K59**, opened by K57 on 2026-08-17 and deliberately left unclaimable: *"Take this parcel
only with a frame-time measurement in hand, in the wet woods where 167 of them stand; without one it
is a preference wearing a table, which is exactly what K57 refused."* K57 had shipped 48 leaf sprays
a shrub at the knee of a coverage curve and banked 64 as measured and unspent — 104 → 136 triangles
for cover **46.9 % → 51.3 %** — justifying the stop on a triangle count and a draw-call count, and
saying in as many words that neither is a frame.

**The shrub batch does not split.** One instanced set, one draw call, at either grain, K56 and K57
both — so the cost of a finer grain is fill and vertex work, and no frame-time figure had ever been
taken anywhere in this archetype's history.

### The instrument, and the two ways it was wrong first

`tools/measure_shrub_frame_cost.mjs` stands the walker in `z06_dense_forest` — 158 shrubs drawn in
one ring, the densest of the ten communities — sweeps eight bearings and fixes the camera at the
most expensive of them (1,343,341 triangles at 135°), holds the clock so the wind cannot blow
between two readings, drives frames one at a time rather than letting the browser pace them, and
fences each frame with a one-pixel readback. The candidate grain is injected by rewriting one
integer of `shrub-grain.js` as the tool's own static server hands it over, and the page is asked to
read `SHRUB_GRAIN.fill` back before anything is timed.

**`gl.finish()` is not a fence here, and it produced a confident wrong answer.** The first cut timed
`step()` + `gl.finish()` and reported **2.90 ms** a frame while the process spent about **four
seconds** of wall clock on each. ANGLE's SwiftShader backend rasterises in another process, so the
finish synchronises nothing the caller can observe; what was timed was how fast three.js can talk,
which is the one quantity that does not move when a shrub grows 32 triangles. Its verdict was
**+31 %**, and +31 % would have refused this parcel.

**And a Playwright route handler is not free.** Injecting the grain with `page.route` turned network
interception on for every request in the context — several hundred GLB and JSON files — and took one
page load from about eight seconds to over four minutes.

### The reading

| | 48 sprays | 64 sprays | |
|---|---|---|---|
| desktop 1280×800 | 4282.30 ms | 4410.30 ms | **+3.0 %** |
| mobile 390×780 | 2739.60 ms | 2795.80 ms | **+2.1 %** |
| desktop, the shipped grain measured AGAIN | **4292.90 ms** | | **+0.2 %** — the control |

The third row is the A/B/A: the identical scene, measured after the candidate. The runner's own
drift between two readings is two tenths of a point, so the candidate's three points are fifteen
times it rather than inside it.

**These milliseconds are a headless software rasteriser on a shared CI machine and nobody's phone.**
The tool prints the renderer string with every reading for that reason. The ratio is the answer, and
it argues in the safe direction: a software rasteriser is the most fill-sensitive renderer there is,
so it is the harshest available witness for the one risk in this parcel — 33 % more transparent
plate over the same silhouette, overdraw **1.33 → 1.56**.

### What shipped

| | before | after |
|---|---|---|
| leaf sprays per shrub | 48 | **64** |
| foliage cover of the bush's outline | 46.9 % | **51.3 %** |
| worst bearing of 24 | 43.0 % | **47.3 %** |
| stem cover — dark wood with foliage in front of it | 51.3 % | **54.2 %** |
| reach, against the recorded half-width | 0.998 | **0.997** |
| plate long side on a 2.25 m hazel | 35.0 cm | **34.6 cm**, 3.5× a 10 cm leaf |
| triangles per shrub | 104 | **136** — 17,368 → 22,712 in the ring, of 1,000,000 |

`node tools/measure_spray_grain.mjs --gate` — **GATE: PASS** on the new grain, unchanged bars (reach
≥ 0.95, a spray ≥ 2× a leaf, cover above 40 % at every bearing). The census is identical plant for
plant: no shrub moved, appeared or vanished. Recorded as **L175**.

### Skipped, with the reason, because the queue's rule asks for one

**T-0018** (K49(e), the spatial-filter question) and **T-0019** (K58, six forb layers over the
lattice ceiling) sit above this in QUEUE.md and were both passed over. T-0018 is a measurement whose
own ROADMAP box says *"re-scope it before claiming it"* — K49(f) refuted the explanation it was
opened on and halved the population it has to explain. T-0019's `fits` branch was checked before it
was skipped rather than after: measured today, the six communities ask the forb lattice for **1.25 to
44.5 plants/m² against its ceiling of 0.346**, so nothing tuning can do makes any of them fit and the
ticket resolves as a declared shortfall. Both outcomes are invisible runs, and AGENTS.md's cap — at
most one invisible run in any four — was already at two of the last four (v251, v248). Neither
ticket was reordered in QUEUE.md.

## Re-shot 2026-08-23 — T-0017: the `south_water` baseline row measures a stand that no longer exists

**T-V2 (#135) moved the `south_water` anchor on 2026-08-15**, from local `(260, -95)` — 101 m south
of the centreline of the street it is named for, framing a field — to `(329.8, 7.0)`, the Wells
Street corner. The 2026-08-14 critic baseline was shot the day before. Its `south_water` row has sat
in the table under one name ever since, next to ten rows that still measure the place they were
shot, and nothing said so. Both tables now carry a **†** on that row and a footnote naming the
retired coordinates.

### The re-shoot, and why it is three rows and not two

The obvious reading of this ticket — re-shoot the station and replace the row — is wrong, and the
run measured why rather than asserting it. **The stand is not the only thing that moved.** Holding
the retired coordinates fixed and shooting them on today's `dev` with today's harness gives a third
row, and it does not reproduce the 2026-08-14 numbers either:

**desktop 1280×800, `tools/critic_shots.mjs --stations south_water --metrics`, source tree**

| `south_water` | timber all | timber centre | crown fine | crown G−B | decile L | black px | RMS far/mid/near | flower load | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|
| **2026-08-14** baseline, retired stand | 0.889 | 0.903 | 1.004 | 27.4 | **2.95** | 0 | 17.0 / 26.7 / 30.1 | 0.0575 | 85 / 570,718 |
| **2026-08-23**, retired stand `(260, -95)` | 0.8742 | 0.8571 | 1.176 | 28.55 | **8.87** | 0 | 19.83 / 32.38 / 29.43 | 0.0037 | 208 / 1,441,196 |
| **2026-08-23**, current stand `(329.8, 7.0)` | 0.7000 | 0.6979 | 0.777 | **80.74** | **26.15** | 0 | 11.26 / 2.74 / 0.98 | 0.0020 | 185 / 1,308,796 |

**mobile 390×780**

| `south_water` | timber all | timber centre | crown fine | crown G−B | decile L | black px | RMS far/mid/near | flower load | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|
| **2026-08-14** baseline, retired stand | 0.836 | 0.811 | 0.755 | 35.9 | **7.54** | 0 | 24.1 / 33.9 / 25.1 | 0.0128 | 83 / 550,065 |
| **2026-08-23**, retired stand `(260, -95)` | 0.8872 | 0.9077 | 1.527 | 23.05 | **7.64** | 0 | 29.91 / 31.0 / 20.54 | 0.0078 | 196 / 1,402,486 |
| **2026-08-23**, current stand `(329.8, 7.0)` | 0.8897 | 0.8692 | 0.868 | **73.11** | **37.14** | 0 | 7.24 / 1.57 / 0.43 | 0.0018 | 170 / 1,247,467 |

Rows two and three are one build, one harness, one frozen clock, minutes apart — so **everything
between them is the stand**, and everything between rows one and two is nine days of town. Both
gaps are large. `flower load` at the retired stand fell **0.0575 → 0.0037** without the camera
moving a metre; draw calls at that same stand went **85 → 208** and triangles **570,718 →
1,441,196**, 2.5×. The dataset says the same thing from the other side: **242 placed structures on
the baseline commit, 343 today**, and within 200 m of the retired stand **39 → 64**. A stand in a
field in August is a stand among buildings now.

**So the 2026-08-14 row is not recoverable, only labelled.** It cannot be reproduced by returning
the camera, and it should not be overwritten with a number from a different town. It is kept, marked
as the retired stand, and the re-shoot is recorded here beside it.

### What the move did to the picture, and it is mostly a repair

- **The stand came out of the shade.** Darkest-decile L **8.87 → 26.15** desktop and **7.64 → 37.14**
  mobile. RENDERING § 5 sets the floor at **L ≥ 14**: the retired stand failed it at both viewports
  on today's build, the current stand clears it at both. Sunlit crown G−B **28.55 → 80.74** desktop,
  **23.05 → 73.11** mobile, the same cause read on crowns instead of shadows — the field stand sat
  under near-field timber and the street stand does not.
- **Grain collapses, and the street is why.** RMS far/mid/near **19.83 / 32.38 / 29.43 → 11.26 /
  2.74 / 0.98** desktop. Mid and near at the current stand are graded earth roadway, which carries
  almost no high-frequency texture; at the retired stand they were sward. This is a reading about
  what a road surface looks like, not a regression — the same surface T-0016's band report measures.
- **Flower load falls again on the move**, 0.0037 → 0.0020 desktop, for the same reason: less
  vegetation in frame. Bloom share of ground 0.0307 → 0.0013. § 5's flower target is only meaningful
  at the open-prairie stations, and `south_water` was never one; standing it in a street makes that
  plainer, it does not make it worse.
- **Horizon coverage splits by viewport** — desktop 0.8742 → 0.7000, because the roadway runs to the
  horizon and opens a gap in the skyline; mobile 0.8872 → 0.8897, unchanged, because the narrower
  frame is filled by the buildings flanking the street.
- **The move is cheaper than the stand it replaced** on today's town: 185 draws against 208 desktop,
  170 against 196 mobile. Both are far over the ≤ 80 budget — that is the town's growth, not the
  move, and it is true of every station now.

Frames from the two 2026-08-23 stands, desktop, same build:
`docs/evidence/t-0017-{retired,current}-stand.png`.

### Three things this found that the ticket did not ask for, stated rather than fixed

1. **The 2026-08-14 tables' `timber all` / `timber centre` columns are today's `skyline breaks`,
   not today's `horizon TIMBER`.** R-W4a (#140, 2026-08-15) showed that measurement was counting
   the town's roofs as timber and split it in two, keeping `coverageAll` as the skyline figure and
   adding `timberOnly` beside it. The values in those columns are still comparable to today's
   `skyline breaks` — the computation did not change — but the heading is the old, disproven name.
   Left as shot, because rewriting the heading of a banked baseline is a different act from
   annotating a row.
2. **The rig now stands at thirteen stations and the baseline table has eleven.**
   `newberry_dole_wharf` (T-0041) and `north_branch_bridge_deck` (T-0001) were added to
   `data/scenes/1835.json` after the baseline and have never had a row.
3. **The § 5 draw-call bullet under those tables is stale for every station, not just this one** —
   it names four stations over the ≤ 80 budget at 83–97, and `south_water` alone reads 170–185
   today. Owned by R-W5, which owns the draw-call work; not restated here on one station's evidence.

**No threshold moved, no station was dropped, no gate changed.** `data/scenes/1835.json` was patched
to the retired coordinates to shoot row two and restored byte-for-byte in the same command; the
committed scene is untouched, which `tools/check.sh` re-derives.

**Gates.** `tools/check.sh` green. Published smoke, all four stages at both viewports: **888 passed,
3 failed** — `the roads reach the screen from the walker's eye, down an open street` at both
viewports and `…from the air, at the aerial anchor` at mobile. All three are the bands R-W1, R-W2
and R-M1c already own and STATUS already records as knowingly red, and this parcel cannot have
caused them: **nothing the renderer loads changed.** The whole diff against `dev` under `site/` is
`tickets.json`, and under `chicago/4d/` it is `docs/`, `tickets/` and two PNGs — zero renderer, data
or asset files. Naming the count rather than the shape of the failure, because "pre-existing" is a
claim and the diff is the evidence for it.

## Shipped 2026-08-23 — T-0097: the ground outside the fort's walls is bare and trodden

**Visible run**, and the pick needs saying. The topmost workable ticket, T-0015, had a rival branch
pushed twenty minutes earlier (`steward/t-0015-ao-nightly`), so `claim` would have refused it. Of
what is left above this one: T-0017, T-0018, T-0021, T-0024 and T-0025 are measurement parcels or
questions; T-0019's own ROADMAP box (K58) names the measurement as the thing to land first and calls
the visible route *"not a free tune"*; T-0026, T-0027 and T-0028 need a bake this run did not have
room for beside a demonstration; and **T-0058 — the one visible ticket above this — was written with
its acceptance clause left blank**, so it cannot be run without inventing the definition of done,
which is the one thing this project's own rule says never to do. T-0097 is the topmost ticket that
both puts something in the town and states what done means. **QUEUE.md was not reordered.**

**The ask.** T-0044's image-accuracy pass read the render against the two committed Fort Dearborn
plates and listed eight gaps. Number 7: *"The ground round the walls is full prairie sward; both
plates show it bare and trodden."* In `p4_0.png` — the fort from the north bank, the stand this
project shoots it from — bare, pale, trodden earth runs from the foot of the pickets past a walking
figure to the crest of the bank, with the track from the gate crossing it, and the prairie only
resumes beyond. In the render, bluestem grew to the pickets.

**What shipped.** `data/enclosures/fort_dearborn_apron.json` — a band **12.0 m wide immediately
outside the palisade, on all four sides** — suppresses the sward there and lays the yard layer's
`trodden_earth` treatment in its place. Before and after from `p4_0`'s own stand
(`1145, 300`, yaw 180°) are committed at `docs/evidence/t-0097-before.png` and `-after.png`.

**It is a rule, which is what the acceptance clause asked for.** Not one coordinate is authored:
`tools/generate_fort_apron.py` derives every ring from `fort_dearborn_palisade`'s committed
`footprint.polygon` and `placement` in the frame `docs/GLB-CONTRACT.md` fixes, so the ground follows
the fort if the fort is ever re-placed, and `tools/check.sh` re-derives the file byte for byte.
**Four assertions run with it and fail the gate rather than a reviewer's attention:** the four bands
tile the annulus with no overlap and no gap (3,120 m² derived, 3,120 m² expected); no band covers
the parade inside the walls; `fort_road`'s last traced point stands ON the apron, so no collar of
untouched prairie is left between the track and the wall; and no other enclosure record already
treats this ground.

**Two small changes to shared code, both additive.** `ground.interior_local_enu_m` may now carry an
ARRAY OF RINGS as well as one ring — the apron is the band OUTSIDE the walls, which is a frame of
four bands and not a disc, and a record that could state only one ring would have had to claim the
parade as well to say it. And `ground.fringe_ring_local_enu_m` names the ONE ring the trampled-grass
fringe is measured from: band by band the fringe would have drawn a grassy seam along the wall and
along every internal join, which is the opposite of what the plate shows. Records written before
this read exactly as they did. `enclosures.js` also stops filing a problem for a record with no runs
at all — the enclosure here is the palisade, a committed structure with a baked GLB, so this record
carries `runs: []` and the ground alone.

**No new draw call and no new surface.** The apron rides the estray pen's existing `trodden_earth`
buffer and material.

**What is invented, and it is the width.** Twelve metres, one number for all four sides, no source
for a foot of it. Bounded by the plates — tier-5 pictorial, which may drive setting as `inferred`
and may never drive a coordinate — where the bare ground scaled against the fort's own 53 m side runs
to the order of ten to twenty metres, and by the fort road's own `corridor_width_m`, the only other
reconstructed distance this project has stated on this reservation. `docs/LIBERTIES.md` L174 claims
it. **What this deliberately does NOT claim:** the ground inside the walls, which no committed plate
shows; and it does not clip the fort road, whose last seven metres of track lie on the apron — both
are bare-earth drapes, both `reconstructed`, and a travelled way crossing a trodden apron is what the
plate draws.

**A GATE TURNED RED AND WAS REPLACED RATHER THAN RAISED, and which act that is matters.** T-0067's
confinement check — *"the sward is suppressed inside the fences and essentially nowhere else"* — held
the suppressed ground under **0.2 % of the modelled dry ground**, a constant fitted to the four fenced
records that existed when it was written. The apron is 3,120 m² the dataset DECLARES, which took the
figure to 0.368 %. Raising the constant to 0.005 would have bought the same red the next time the town
encloses anything, so the assertion now compares the SAMPLED suppression against the shoelace area of
the interiors the layer actually built: **4,764 m² declared across 22 interiors in 5 records, 4,592 m²
recovered by the 4 m sampler — 3.6 % apart**, gated at 20 %, with the absolute ceiling kept at a
fiftieth of the dry ground as the blow-up guard. That is strictly sharper than what it replaced: the
old bar could not tell 3,120 m² of apron from 3,120 m² of prairie taken off by a ring that lost a
coordinate, and the new one fails on the second while passing the first.

**The two road-legibility reds in stage 3 are `dev`'s, not this branch's.** T-0114. Measured both
ways: `origin/dev` in a clean worktree and this branch print **byte-identical band tables** at both
viewports — 2-40 m through 600-4000 m, every ΔL*, every perceptible percentage, every sample count.
This PR moves that gate by zero.

**What is still short, stated rather than left to be noticed.** The band stops square, where trodden
ground fans out from a gate; the gate side is worn no harder than the other three; and the palisade's
own footprint is only `inferred`, off the 1830 Harrison plan and Andreas, so this band can never be
better evidenced than the wall it is measured from.

## Shipped 2026-08-23 — T-0057: Ordinance 9's other half, on the one lot this town can say was building

**Visible run.** The three tickets above this one in the queue — T-0015, T-0016, T-0017 — are all
measurement parcels, and the last four merged entries run visible / invisible / invisible / visible.
AGENTS.md's visible-progress rule says that when the top of the queue is all invisible, the run's
job is to pull a visible parcel up and say in the PR why it was buried. T-0057 is the topmost
ticket that puts something in the town, and QUEUE.md was not reordered.

**The ask.** Ordinance 9 of 7 November 1833 names *timber, stone, brick, boxes and barrels* stacked
in the streets. T-0040 shipped the boxes and barrels (L131, `data/yard/town_trade_goods.json`) and
refused the other three in writing, because building material belongs to a lot that is GOING UP and
the goods record has no way to say which lot was.

**The census, which is the parcel.** 343 structures stand on the scene date: 256 anonymous infill,
87 named. **Exactly one carries a construction state in its own attributes** —
`lake_house_construction`, `function: hotel_under_construction`, graded **attested** off Andreas,
with `roof_type: none` for the same reason and J. D. Bonnell walking past 'the Lake House in course
of construction' on 25 August 1835. So `tools/generate_lot_building_material.py` writes nine piles
on one lot: 4 stacks of brick on the frontage, 3 piles of squared timber down the east flank, 2
heaps of footing stone at the rear. `tools/check.sh` re-derives the file byte for byte.

**The clause that is NOT in the rule, and refusing to write it is the finding.** No date test.
`documented_range.from` inside 1835 is a FIRST-ATTESTATION date for the named records — a
newspaper's first issue on 8 June 1835, a directory line, a deed — and a PROGRAMME date for the
anonymous ones (L126). Fourteen named records carry an 1835 opening and every one is refused by
name with that reason in the record's `refused` block, including the north and south piers, which
really were under documented extension that summer and are refused anyway: harbour works in the
lake are not a lot in the corporation whose ordinance is the whole evidence.

**Which materials is dealt from the record, not from the ordinance's list in order.** Brick because
`construction` is brick and attested; stone because the same sentence gives the building a
basement; timber because a three-storey brick house is floored, joisted and roofed in it and laid
from timber scaffolding. Brick is the town's own `CHIMNEY_BRICK`, taken as the material sheet's
linear triple; stone is the one new colour and is bounded between the layer's timber and the
chinking clay. `docs/LIBERTIES.md` **L173**.

**Not drawn, and said so.** No individual brick and no course — the material sheet records that no
source here gives a brick or a course dimension. And nothing in the street, which is the nuisance
the ordinance actually legislated against: this site's own position note carries ~20 m of working
uncertainty and the traced centreline of Michigan Street runs some 30 m north of where the same
georeference puts the frontage.

**Verification.** `./tools/check.sh` green. `tools/smoke_renderer.mjs --published`, both release
viewports, all four stages: mobile 141/112/40/152, desktop 141/109/41/152, **zero page errors**,
draw calls 42 of 215 and 618k triangles of 1.4 M at the site. Two new checks measure the piles in
their own frame — furthest vertex 1.90 m from its own anchor, **0 vertices inside the building's
own footprint**, which is the fault the generator actually made on its first run when it turned the
outward normal the wrong way. The two `roads reach the screen` reds in stage 3 are **T-0114 and
pre-existing**: a clean `origin/dev` worktree fails the identical checks with the identical counts.

## Shipped 2026-08-23 — T-0013: the interior flicker is the town's own edges, and none of it is a fight

**Nothing a visitor can see changed, and that is the third such run in four.** It is recorded
here rather than smoothed over: the visible-progress rule's cap is one invisible run in four,
the queue's topmost ticket asked for a diagnosis as its first demonstration, and the diagnosis
came back saying there is nothing to repair. The next run must land something visible.

T-0013 was re-aimed by the owner on 2026-08-23 at the **interior** share of the 2 mm-nudge
flicker — 370 px on `structures`, 257 on `trees` — where a layer was believed to be fighting
ITSELF, as opposed to its silhouette against the rest of the scene. It asked for the mechanism
to be NAMED per layer with evidence before anything was repaired.

`tools/diagnose_interior_flicker.mjs` names it, and it is the same mechanism for both layers:
**those pixels sit on edges internal to the layer, and an edge is not a defect.** Photographing
a packed-depth pass at both poses classifies every one of them — 349 of 370 on structures and
252 of 257 on trees sit on a depth BREAK inside the layer's own footprint; **0 are a depth
reorder and 0 are shading**. Supersampling heals 83–93 % of them, which is what a coverage-bound
edge does; going matte across 18 materials changes 164,572 px of the picture and heals none.
The handful that read no depth at all are the same finding again — a packed depth blended by
MSAA cannot be decoded, and only a pixel with more than one surface in it gets blended.

**What is now known to be unverified**: the discriminator's name. `interiorOf` knows a layer's
outline against everything else and cannot see the boundary between two surfaces OF that layer,
so 94–98 % of what it reports as "interior" is silhouette by any honest reading. The instrument
was not changed in this run — closing a ticket by rewriting the instrument that measured it is
the one move this project does not allow — so the number stands and its correction is a ticket.

Measured at `from_above`, 1280×800, published mirror, shadow map off by R-BUG6(a)'s repaired
control, with the run's own control and return-to-pose both 0 px. Deep box: ROADMAP § R-BUG6(c2).

## Shipped 2026-08-23 — T-0154: closing a ticket stops leaving the published mirror stale

**The ask.** `site/chicago/4d/tickets.json` is a verbatim copy of `tickets/tickets.json` and
`tools/check_published.mjs` compares the two byte for byte — the gate that generalises #145, where a
published artefact quietly differing from its source hid the terrain quantiser for three parcels.
`tools/ticket.mjs done` rewrites the source. So the order AGENTS.md states could not be obeyed:

1. do the work, run `tools/publish.sh` — "PUBLISH IN THE SAME COMMIT";
2. push, open the PR — **the PR number does not exist until this moment**;
3. `ticket.mjs done T-NNNN --pr N` — "close it in the merging PR";
4. the mirror is now stale and the gate fails on the next push.

Step 3 needs a number only step 2 can produce, so no ordering of the documented steps ends green. It
went red on T-0153/PR #318 at 05:11Z. What actually held it together was a REMEMBERED extra
`publish.sh` after the close — the unwritten step that goes wrong at 3am.

**What was built.** The writer of the file maintains its mirror: `ticket.mjs`'s `generateBoard`
carries `tickets.json` to the one published path `publish.sh` copies it to. Deliberately narrow, and
the narrowness is the whole design:

- **only on a real rewrite.** The acceptance clause forbids fixing this by making the gate weaker,
  and a blanket refresh on every invocation would do exactly that — a mirror somebody else made
  stale (a hand edit, a half-run publish, a bad merge) would be silently laundered by the next
  `ticket.mjs check`, and the gate would be reporting on the tool's own last act instead of on what
  the site ships. `settle()` now returns whether it wrote; the mirror moves only then.
- **it never creates the mirror directory.** An unpublished checkout stays unpublished; `publish.sh`
  is what decides the mirror exists.
- **the copy is pinned.** `ticket.mjs` hard-codes where `publish.sh` puts the file, which is two
  copies of one fact — this project's recurring fault. `ticket.mjs check` (which `check.sh` runs)
  asserts publish.sh still contains that exact `cp` line, and names the reconciliation if it does not.

**Demonstrated, both halves, in `tools/test_ticket_mirror.mjs`** — a new `check.sh` step. It builds a
sandbox of the shape the tools expect (`<tmp>/chicago/4d/…` beside `<tmp>/site/chicago/4d/`), copies
the three tools and the real ticket files in, and asserts: a freshly published sandbox is green; a
`done` with a PR number leaves it green **with no second publish**; the mirror really is the closed
board; a hand-staled mirror **still fails**; a no-op regeneration **does not launder it**; and moving
publish.sh's copy line is refused by `ticket.mjs check`. Nothing outside the sandbox is written — an
earlier draft mutated the real `tickets.json` and restored it, which is a working tree nobody can
explain if it crashes halfway.

**What is NOT fixed, and it is filed rather than folded in.** `renderers/web/js/changelog.js` is
mirrored to two published paths and `tools/stamp-changelog.mjs` rewrites it, so a run that stamps
after publishing hits the identical trap. It has not bitten because nothing forces that order —
unlike the close, which cannot be ordered correctly at all. **T-0155**, XS.

## Shipped 2026-08-23 — T-0152: the drawn ground stands exactly where the field says, because the quantiser's rung now divides the grid

**The ask.** The drawn ground stood **77.1 mm** off the field on the east slopes, with **56** of the
field's 259,689 sample points past the 22 mm road lift — one of them 0.1 m from the centreline of
North Water Street, 25.0 mm BELOW the ground it carries. Acceptance: zero samples past the lift, on
the bytes that ship.

**The mechanism, and it was never the bit depth.** `renderers/web/js/terrain.js` reads every ground
height back off `heightfield.bin` at load, so Y is exact to the micron. It reads that height at the
vertex's SHIPPED (E, N) — and `tools/web_derivatives.sh` moves those. `gltf-transform` quantises
POSITION under one uniform node scale set by the mesh's widest axis, which is the 2 020 m box plus
two skirt margins, so the rung was `5 020 / 2 / 32767` = **76.6 mm** and 2.5 m of terrain grid was
**32.64** of them. Vertices therefore landed between rungs, up to 51.9 mm out in plan, and a vertex
conformed at a displaced position holds the field's answer for the wrong place. The cost is
(slope × displacement) and nothing else, which is why R-W6 could write "flat platted prairie cannot
show this artefact at any bit depth" and be right, and why the east extension — bank faces at a
median 62 % slope, worst 87 % — made it visible without this step changing at all.

**Neither easy answer existed.** 16 bits is the format's maximum, and it already ships at 16.
Passing the master through uncompressed is +5.8 MB against a 22.32 MB payload and a 25 MB budget.

**What was built — the third answer, and it abolishes the displacement rather than shrinking it.**
The quantiser was measured rather than argued about: on the bytes that shipped, scale = half the
widest extent, translation = the mesh's own centre, rung = scale / 32767, and **378,581 of 378,582
axis values reproduce `round((p − centre) / rung)` to the bit** (the one exception is a half-rung
tie). So it is a ladder, and the only question is whether the generator's vertices stand on its
rungs. `generators/terrain_gen.py` now DERIVES the skirt margin so that they do:

    rung   = (e_span + 2 · margin) / 2 / 32767
    margin = 32767 · cell / k − e_span / 2          for rung = cell / k

taking the largest power-of-two `k` whose apron still reaches the haze distance — **k = 32, rung
78.125 mm, margin 1 549.921875 m**. A power of two on purpose: `gltf-transform` stores a bit depth
in the container above it, so asking for fewer bits multiplies the rung by a power of two and
leaves it commensurate. The generator and the shell script are not coupled through a number.

**Measured on the bytes that ship, before → after:**

| | before | after |
|---|---|---|
| plan movement, master → shipped | 51.9 mm max | **0.0 mm** |
| drawn surface vs the field, after conforming | 1.5 rms / 3.9 p99 / **77.1 max** | 1.3 / 3.7 / **6.7** |
| samples past the 22 mm road lift | **56** (20 on dry ground) | **0** |
| shipped derivative | 704,004 B | 699,096 B |

6.7 mm IS the master's own decimation error, to the tenth of a millimetre: the compressor now
contributes nothing at all to the surface a visitor stands on.

**Two gates, on both sides of the bake.** The generator REFUSES to export a ground whose vertices
do not stand on the rung, and `tools/measure_terrain_horizontal.mjs --gate` — new, in
`tools/check.sh`, 0.8 s — asserts the same thing on the shipped BYTES, plus the consequence: no
sample point past the road lift. It was demonstrated firing on the old committed derivative
("the publish step displaced the ground in plan by 51.9 mm", exit 1) before it was wired in. That
file had reported for a week without asserting anything, because until now no setting made the
number pass and a gate on it would only have said that a compressor is a compressor.

**No contract amendment was needed after all.** T-0152 anticipated one, because the fix R-W6 left on
the table was the SKIRT SPLIT — put the apron in its own mesh so the ground's own box sets the scale
— and that changes what a terrain GLB contains, which is bilateral. It also only buys a factor of
2.49 (the ground's box is still 2 020 m wide), which lands at about 31 mm and would have failed the
acceptance clause. The derived margin needs no structural change: one mesh, one primitive, same
node, same everything the renderer reads. `docs/GLB-CONTRACT.md` gains a paragraph recording the
invariant, and gives nothing up.

**What a visitor sees.** On flat ground, nothing — the conforming pass has hidden this since
R-BUG3c. On the east bank faces and at the North Water Street reach, the roadway, the grass tufts
and the rooted plants now sit on the ground rather than in it. L17 is revised: the apron is
1 549.921875 m per side and 18.35 km², up from 1 500 m and 17.46, and still 2 256 vertices.

## Shipped 2026-08-23 — T-0151: the shipped ground's bit depth is asserted, and its ticket was describing a state the tree had left

**The ask.** T-0012, at number two in the queue: *"the 16-bit ground exists in the bake script and
not in the file a visitor loads — the committed derivative still quantises POSITION to 14 bits."*

**Its first sentence was no longer true.** Measured with R-W6's own control — regenerate the
committed master and compare md5s — `terrain__e1834_harbor_cut.glb` at **16** bits reproduces the
committed derivative exactly (`5b8446876a425fceace5c7dd7c59688a`, 704,004 bytes) and at 14 bits
does not (`4b9fb0765a9b5669dd547b32ef156825`, 702,896). The 16-bit ground reached the site in a
nightly bake that rebuilt the terrain. The water mesh reproduces at both depths
(`61b38d4bc36964db450b59ac7b646b77`) — R-W6 predicted that in writing: four vertices at y = 0 land
on the lattice at every depth.

**So the fault was never only "the file is 14-bit". It was that nothing could tell you which it
was**, in either direction. R-W6(b) diagnosed the mechanism and the diagnosis was right the whole
time: the derivative gate compares master to derivative on material identity, triangle count, node
identity and a bounding box within four rungs, and **a bit-depth change moves none of them**.
`tools/measure_terrain_fit.mjs` printed the lattice in a report column and asserted nothing. So a
14-bit ground shipped for days with every gate green, then a 16-bit one arrived and every gate was
equally green, and a ticket sat near the top of the queue for a week asking for something that had
already happened.

**What was built.** `tools/measure_terrain_fit.mjs` recovers the shipped POSITION bit depth from
the mesh's own bytes — `gltf-transform` quantises under one uniform node scale set by the widest
axis, so the rung is `extent / (2**bits − 1)` and inverting it gives the depth as an integer — and
`--gate` FAILS when it is coarser than `tools/web_derivatives.sh` asks for. The ask is read out of
the shell rather than restated here, so there is one copy of the number. Demonstrated firing on the
14-bit file this ticket was written about: *"the shipped ground carries 14-bit POSITION where
tools/web_derivatives.sh asks for 16"*, exit 1. `tools/check_published.mjs`'s derivative entry says
so too — it used to say the derivative was only reported.

**What is NOT closed, and it is the honest half of this run — T-0152.** The bit depth is right and
the surface is worse than R-W6 measured it. On the ground that ships today,
`tools/measure_terrain_horizontal.mjs` reports the drawn surface, after conforming, at **1.5 rms /
3.9 p99 / 77.1 max mm** with **56** of the field's 259,689 samples past the 22 mm road lift, 20 of
them on dry ground. R-W6's 16-bit row was 1.4 / 3.8 / **12.9** and **0** past the lift. The depth
did not move; **the ground did** — extended east to the harbour mouth, into bank faces at a median
**62 %** slope (worst sample 87 %), and R-W6 named that mechanism itself: the cost is
(slope × displacement), and flat platted prairie cannot show the artefact at any bit depth. 16 bits
is the format's maximum and the uncompressed master is +5.8 MB against a 22.32 MB payload and a
25 MB budget, so neither of the two easy answers is available. R-W6 wrote down the third and named
its trigger — *"reopen [the skirt split] if a future epoch's box grows"* — and the box grew. That
is a generator change, a `docs/GLB-CONTRACT.md` proposal and a terrain bake: its own ticket, at
T-0012's own place in the queue rather than at the bottom.

**Nothing a visitor can see changed.** The ground under the town is unmoved — the renderer has read
its heights back off the heightfield since R-BUG3c, so the lattice never reached the eye in the
first place. What changed is that the town can now tell what it shipped.

## Shipped 2026-08-22 — T-0105: three roofs on one lot at Randolph and State, and the first block dealt twice

**The ask.** The succession T-0079 owes: carry the core density standard to the next core block
standing below the bar. T-0079 raised the ceiling from one principal roof per platted lot to
**three party-line units per lot** — measured at the smallest committed lot, 23.56 m of frontage
less the plat module's two 1.5 m margins, against the eighteen committed party-line units' mean
6.072 m — and demonstrated it once, on `blk_lake_clark`.

**What was in the way, and it is the recipe's shape rather than the ground.** Every block that
carries a free lot on its measured business face had already been dealt once, and
`data/reconstruction/1835_platted_block_parcels.json` assumed a block is dealt once, built once
and finished: one entry per block, records numbered from one. Rewriting `blk_randolph_dearborn`'s
August entry to cover both deals would restate an August schedule under numbers that were not
true in August. **So a block may now be dealt twice, as a second entry with its own `seq_start`**
— the record id carries the sequence, and two entries numbering from one would collide on the
first slot that shared a family. The lot accounting learned one new class with it, *built on by
another deal on this block*, which it needs in both directions: before the second deal's records
exist the lot reads as one nobody accounted for, and after they exist calling it "already
carrying a roof" would say a stranger built it. Nothing else had to move — occupancy, separation
and the roadway are all measured against the committed dataset rather than against one entry's
own slots.

**Which block, and it is a fact about the schedule rather than a preference.** Seven platted
blocks stand `open`. Four of them (`blk_south_water_franklin`, `_lasalle`, `_clark`, `_dearborn`)
front the reach whose committed street line is the open question in **T-0009**, `blocked-owner`
since this morning and worth 4.3–8.8 m — standing a tightened row against a line that may move is
the mistake T-0009 refused to make. `blk_lake_franklin` has the town's strongest business face and
a deal it cannot carry: D3, A1, an **F3** large *river* warehouse on a block that touches no water,
and an **I3** the generator refuses by name. `blk_randolph_market`'s two free lots are both on its
back face. **`blk_randolph_dearborn` is what is left**, and it is one of the two blocks with the
most headroom in the schedule: 9 roofs standing, 8 of headroom, three free lots — 1 and 5 on
Washington, **4 on Randolph**.

**The face rule is a command now (T-A14) and this parcel quotes it rather than remembering it:**
`tools/measure_street_frontage.py randolph washington market franklin` reports Randolph carrying
**7 documented records and 7 inferred households against Washington's 1 and 0**. Randolph is this
block's business face by the town's own record, so its one free lot on that face takes the row and
both free lots on Washington stay open. **The end rule is T-A11's:** this is the easternmost block
the plat module reaches on the Randolph tier, so the town-centre end of the frontage is the WEST
one, toward Dearborn Street and the only crossing of the main stem in July 1835 — and the row is
graded that way.

**What stands.** Three principal roofs on lot 4, on one line, at one 1.5 m setback, on two shared
party walls: `recon_1835_blk_randolph_dearborn_d6_10`, a one-and-a-half-storey cottage anchored
1.5 m off the lot's west side line, then `_d3_11`, a one-room frame cottage, then `_d1_12`, an
older log cabin. The run occupies **17.23 m of the lot's 23.00 m of buildable frontage**, and the
metres left over are at the east end where the run stops. The fourth roof is the standard's second
clause — an improved lot carries its outbuildings — so `_a4_13`, a woodshed, stands in lot 4's own
yard at the alley. Before and after from the same stand in Randolph Street, at local E 797,
N −257, looking WSW: `docs/RESEARCH/randolph_dearborn_row_{before,after}_2026-08-22.png`.

**The parcel took four of the block's eight roofs and says so.** Nothing is deferred: the other
four are not refused, they are the next run's, and the two free lots on Washington are the ground
they will stand on. The block stays `open` in the schedule, which is where **T-0143**, the
successor, reads it. No roof was added to the town — the four come out of
`south_plat_beyond_committed_control` and the programme still reconciles at 334 standing, 331
remaining, 665.

**Two roofs the schedule dealt this block could not be built, and the gates said so rather than
this parcel deciding it.** H2, the merchant's house, asks at this sequence for a two-storey wall of
**6.234 m** and `frame_dwelling` refuses anything over **6.2 m**, because the one attested ceiling
height in this dataset is the Green Tree's seven and a half feet. H1 is dealt the generator's flat
**44.0 deg** pitch for a storey and a half, which is inside D6's cited 9:12–12:12 and outside H1's
own 8:12–11:12; `measure_band_claims.py --gate` refuses it by name. Three families are dealt a
pitch their own crosswalk entry forbids (H1, H2, H3) and nine records of them already stand, so
the repair moves committed geometry and needs their bake: **T-0142**, filed rather than dodged by
re-ordering slots until the sampler dealt a shorter house.

**That a log cabin may stand on a commercial frontage is still open (T-0022)** and this parcel does
not settle it; what stands behind the deal is what T-0079 recorded, the owner's own reference for a
party-line row drawing log and frame buildings shoulder to shoulder, and this is one more recorded
instance rather than a ruling.

**Gates.** `./tools/check.sh` green in the foreground after `./tools/publish.sh`;
`node tools/smoke_renderer.mjs` — see the PR for which halves ran inside the ten-minute command
ceiling (T-0060/T-0121, unchanged) and how *zero page errors* was answered at both viewports.

## Shipped 2026-08-22 — T-0140: masts at Wolf Point, and the half of the plate that cannot be drawn

**Four craft join the boat layer at the forks** — `data/boats/era_boats.json` goes from nine hulls
to thirteen. Two two-masted lake schooners: one in the branch reach above Wolf Point at local
E −77.0, N +14.0, one in the South Branch reach below the forks at E −9.0, N −68.0 abreast Robert
A. Kinzie's store. A skiff afloat off the west bank at E −86.0, N +4.0 and one hauled out on the
bank below the Wolf Point cabins at E −83.0, N −20.0. Every hull `reconstructed`, unmanned,
unnamed; L146 extended rather than a new liberty opened, because it is the same invention at a
second address.

**The berths are derived, not chosen, and that is the only part of a boat's position this project
can defend.** Each afloat hull lies at close to the westernmost line on its own reach where the
committed heightfield gives it its draft plus the layer's 0.3 m under the keel along the whole
keel — 2.07 m of water under the upper schooner, 1.81 m under the lower one against the 1.80 m the
layer demands, 1.23 m under the skiff. The reach's own shoaling decides how near the bank a hull
may lie; nothing was nudged, and `boats.js` would have refused any of them outright.

**Why the forks needed them.** Plate "11" of the 2026-08-11 reference set
(`prefire_views_kevin_2026_08/p6_0.png`) and the Braunhold/Trowbridge views of the same quarter
hang ship masts over the Wolf Point roofs. Until today the only masted vessels in the scene were
the three moored 900 m east below the Dearborn drawbridge, and the forks — the busiest water in
the town — held nothing.

**T-0122 was split, because half its acceptance is not the loop's to meet.** It asked for a mast
reading above the GREEN TREE's own roofline from that inn's visitor stand. It cannot: the
`green_tree` anchor stands 24 m west of the inn, whose ridge subtends about 10°, and a 14.5 m mast
subtends 10° only inside ~83 m — while the nearest water on that bearing is ~157 m out. The cause
is the placement question the record already carries in its own `position_note`: DRLOIH gives the
corner as "Lake and West Water", West Water ran along the bank, and *"if the tavern actually stood
on the riverbank street rather than on Canal, it belongs about 145 m east of where this record
puts it."* Moving a documented building is the owner's call. **T-0140** is this shipped piece;
**T-0141** carries the arithmetic and the question, blocked on him.

**Verified:** `tools/check.sh` green · `node tools/smoke_renderer.mjs` green at 390×780 and
1280×800, zero pageerrors · `node tools/shoot.mjs site/chicago/4d /walk/` at the `forks` and
`green_tree` anchors, 114 draw calls of a 140 budget at the shoot's own stand, no page errors, and
the schooner's masts standing over the west-bank roofs in the frame.

## Shipped 2026-08-22 — T-0009: the deep corridor cluster is the street moving, not the buildings

**THE TICKET'S PREMISE IS REFUTED AND NOTHING WAS MOVED.** T-0009 (= ROADMAP K30(c)) asked for the
repair K30(b) had prescribed: redraw the bodies of the buildings drawn standing in the roadway onto
the correct side of their own frontage. Running it would have moved **twelve documented buildings a
full footprint depth behind the frontages their own committed control was offset to**. The
refutation is arithmetic, it is a command, and it is banked as **K30(d)**.

**The flag K30(b) read cannot tell two opposite drawings apart.** `body_toward_street` is true
both when the anchor sits on the KERB and the body grows across the frontage into the road, and
when the anchor sits at the BACK corner — set back by the footprint's own depth — so that the body
grows forward and its street-facing FACE lands on the frontage. The first is a fault; the second is
correct.

**`tools/measure_corridor_intrusion.py --anchors` separates them,** by measuring which of the
footprint's two faces the anchor coincides with along the street normal. **It is the back corner on
all 17 records in the deep mode and the kerb face on none of them.** The only three records whose
point IS the kerb face are `tremont_house_1`, `exchange_coffee_house` and `western_hotel` — exactly
the three K30(b) finding 3 named as already drawn correctly and ruined by reflection. Both
conventions are in the dataset; K30(b) had them the wrong way round.

**The dataset already said so where it is machine-checked.** `position.derivation` constrains a
FACE to a kerb, never the anchor — `sauganash_hotel`'s block reads *"the depth is in the polygon,
so the constraint is on the face"* — and `check_position_derivations` recomputes five placements
from `data/traces/street_control.json` on every commit. The twelve records' prose sums reproduce to
the centimetre: `peck_store`'s origin is its intersection centre less 12.2 m less its own width and
depth, and its north face lands on the derived kerb exactly; the four whose notes only quote the
kerb line have their face on the interpolated kerb to **0.01 m**; `log_jail`'s north face IS the
public square's NW inside corner.

**What is actually in the road is the road.** `data/streets/1835.json` says of `south_water` that
east of Franklin the line *"is shifted into the dry half of the platted riverfront corridor"* —
`plat_corridors` offsets that drawn line to make the legal corridor, so shifting the line re-plats
the street. Measured against the intersection centres the placements were derived from, the
committed line stands **4.3–8.8 m south** of them (Franklin −8.56, Wells −8.80, LaSalle −4.30,
Clark −4.90, Dearborn −6.20), which is the whole of the 4.51–8.17 m the ten South Water records lap.
And the shift is not a mistake either: `chicago_american_office`'s own note records the traced 1834
south bank running 18.7 m north of its north face, so a corridor centred on the modern control puts
its northern half in the river.

**T-0009 is `blocked-owner`,** because all three ways out change something with a source behind it:
move the ten buildings south with the street; derive the platted corridor from the survey control
rather than from the drawn line; or accept that this reach of South Water had water where its north
half is drawn. No structure record, coordinate, footprint, confidence or baseline was touched and
`docs/LIBERTIES.md` gains no entry.

## Shipped 2026-08-22 — T-0008: the chimney stops being painted the colour of the roof

**The defect, opened by R-W2a's own measurement of the shipped GLBs (finding 1) and carried as
ROADMAP R-W2c since 2026-08-16.** `frame_dwelling`, `frame_storefront` and `log_dwelling` built
every chimney stack with the ROOF material, so a stack came out wearing whatever weathering
condition its own roof was dealt — a chimney that disappears into the roof it passes through, from
the footway, on most of the town.

**It was not a palette fix, and R-W2c said so before this run started.** The two stacks this town
has are two different objects, and both archetypes had already argued which in committed prose:
`frame_dwelling._chimneys` says its stack rises *inside* the wall and breaks the roof at the ridge;
`log_dwelling._stack` says its stack is built *against* the gable so it can be pulled away when it
catches fire. Two dispositions, two materials, and the renderer was painting both of them roof.

**What shipped.** `docs/RESEARCH/chimneys.md` — the fabric question answered from what this
repository holds — plus two rows on the material sheet and a conditional `M_CHIMNEY` in four
archetypes. **157 stacks on 143 buildings** now carry a masonry material of their own:

- **Brick on the 112 framed buildings**, `inferred`. The one coloured witness here to any Chicago
  chimney is the Petford watercolour of the Sauganash, and the owner's brief reads **"brick
  chimneys"** off it. Blodgett's brick-yard opened on the North Side in the spring of 1833
  (`brickyard_north_side`, Andreas p. 1161); the Lake House went up in brick in 1835. And an
  interior flue through a timber roof has to be masonry. The VALUE is `frame_tavern`'s committed
  `BRICK_RGBA`, wired to the Sauganash by T-0092, moved into `common/materials.py` verbatim — the
  same convergence T-0007 made for the hewn log — so the Sauganash's own masters come out
  byte-for-byte unchanged.
- **Cat-and-clay on the 31 log cabins**, `reconstructed` and bounded rather than picked: no paler
  than the CHINKING it is daubed with (0.700/0.670/0.590), no darker than the palest ROOF
  CONDITION (0.424/0.384/0.345) or it stops reading as masonry, and at the midpoint of the two to
  three decimals — **0.562/0.527/0.468** — because nothing states where between them it sits.
  Fieldstone is the other half of `log_dwelling`'s own sentence and is deliberately not built.
  **docs/LIBERTIES.md L168** records the invention; L26 keeps every stack's position, untouched.

**It cost no draw call, and that is a fact worth keeping.** `buildings.js::materialKey` batches on
type, emissive, metalness, the four maps, side, transparency and flat-shading — never on base
colour and never on roughness, both of which have ridden per vertex since R-W5a2. So two new
colours merge into buckets that already exist: **113 draw calls before and 113 after**, measured at
`south_water`, 1280×800. Adding a COLOUR to this town is free; adding a MAP would not be.

**Where R-W2a's count does not reproduce, stated rather than quietly restated.** R-W2c says *219
stacks on 199 buildings*. The resolved parameters of the committed masters give **157 on 143**
(frame_dwelling 71/69, frame_storefront 33/33, log_dwelling 34/31, frame_tavern 19/10). The
2026-08-16 figure is not re-derivable from anything committed and is left as written; this run's
number is the one measured here, on this tree.

**What is NOT fixed, in writing.** The fort's ten garrison buildings keep roof-coloured stacks —
1816, seventeen years before the brick-yard, federal ground, and `construction` running log, brick,
earth and stone across the records, so neither answer above reaches them without inventing a third
(**T-0137**). The 90 inferred placeholders keep their own `#89503F` brick, about 20 % apart in
linear red from the archetypes' (**T-0138**); converging it rewrites 90 masters and the banked
passthrough set. Nothing here says what any roof was COVERED with — R-W2a finding 2 stands.
And a trap surfaced on the way: `generators/build.py` cannot build
`cook_county_courthouse_1835` at all, because its only phase runs October to December 1835 and the
only scene targets 1 July — so every `generators/common/` edit stales a committed asset that the
bake has no committed route to heal (**T-0139**). This run got past it with a throwaway
script; that is the thing the ticket exists to stop needing.

**Verification.** 245 generated masters rebuilt on the runner's own Blender, web derivatives
regenerated, `tools/publish.sh` in the same commit. `tools/check.sh` green, including the
staleness gate that is the whole reason the bake had to come with the change.
`node tools/smoke_renderer.mjs` green at 390×780 and 1280×800 with zero page errors. Before/after
at `south_water`: `docs/evidence/t-0008-{before,after}.png`.

## Shipped 2026-08-22 — T-0076: buildings are named for their people, not their spec codes

**The ask (owner, 2026-08-18), verbatim:** *"this name is not great Reconstructed D3 one-room frame
cottage #03, i would like when you put people in the houses to give it the name of their house or
call it a vacant one room frame cottage or use a term like for let or current for the era that it
is available. you should have the marker that it is reconstructed so that should be sufficient.
give the locations useful names not technical D3 #03 names, you can have that somewhere on the card
for reference identity purposes but dont make it the title."*

**What shipped.** `renderers/web/js/display-name.js` composes the title for the 222 anonymous
reconstructed roofs, from data the record and the residents layer already carry: **"The Pratt
house"** where a household lives there (104 roofs are adopted by the inferred-household programme),
**"The Dufresne boarding house"** where the household lives in the premises it keeps, **"Newell's
stable"** where one only works there, **"A privy"** for an outbuilding, **"A vacant one-room frame
cottage"** where nobody is placed, and **"A narrow two-story store, to let"** for premises a town
would have advertised. The card, the Go-to list and the liberties panel all take the same title
from the same function, so the three surfaces cannot drift.

**The production identity is kept, which was the other half of the ask.** `sidecar.name` is
untouched — it is what the parcel recipes re-derive byte for byte, what the GLBs are named for, and
what the release gate's own naming assertion reads — and it is printed under the title as a small
reference line. The Go-to search takes both, plus the household name: "D3 #017" and "Pratt" find
the same roof.

**What is honest about "vacant", and L167 is the entry.** No source says any of these roofs stood
empty. The residents layer places the households this town's trades demand and reaches 104 of the
222; the other 118 are **unmodelled, not attested empty**. The title says the building plainly, as
the owner asked, and the card carries that qualification directly under it in the same block as the
RECONSTRUCTED flag. Nothing in `data/` moved: this is a display layer over records that are
unchanged to the byte.

**Verification.** `tools/check.sh` green. `tools/smoke_renderer.mjs --published` green on mobile
390×780 stages 1, 2 and 4 and desktop 1280×800 stages 1 and 2, with four new gates in stage 2 — no
building titles itself by its part number (222 anonymous roofs scanned, and the rule re-run against
planted records so a scan of nothing cannot pass), the card shows that title with the reference
line under it, and search still answers to both names. **One knowingly red and two knowingly
unrun:** mobile stage 3 carries the two road-legibility failures of **T-0114**, unchanged by this
parcel to the decimal (walker 100–250 m ΔL* 1.8 of 3.2, weber 0.0795; aerial 250–600 m ΔL* 2.0 of
4.6, weber 0.0922), and desktop stages 3 and 4 do not fit the ten-minute foreground ceiling on this
runner (**T-0121**, open).

**What was deliberately not done.** A workplace title names the household and not the trade —
"McCarthy's shop", not "McCarthy's blacksmith shop" — because the trade words in the descriptions
are hedged ("carpenter or joiner shop", "small shop or office") and collapsing them would invent a
specificity the record does not carry. The trade is on the card, in the residents section, and in
the reference line.

## Shipped 2026-08-22 — T-0065: the goods say what is in them

**The ask (owner, 2026-08-18), verbatim:** *"you can add period correct names and brands and labels
to things."* It is the third of that day's overrides of the same restraint — the wagons (T-0064) and
the signboards (T-0066) were the other two — and this one lands on the layer that had the restraint
written into its own file header: *"It draws no mark, brand, stencil or label. Not on any barrel or
case, ever."*

**What shipped.** All 148 objects on `data/yard/town_trade_goods.json` — 102 casks and 46 packing
cases at 26 named trading frontages — carry a mark, dealt by `tools/generate_yard_goods.py` and
re-derived byte for byte by `check.sh`. A standing cask is stencilled with a commodity word across
three staves of its BILGE, which is the face a visitor reads from the footway; every third one
carries the house's own brand there instead. An empty laid on its side is marked on its HEAD, which
is the only face of a lying cask that reads the right way up. A case carries a shipping mark — the
consignee over CHICAGO, and the forwarding houses' cases add FROM BUFFALO. Seventy distinct marks,
in three invented letterforms, on one canvas atlas.

**What bounds it, and L166 is the entry.** Three things may go on a barrel: the house's own name
(already in the dataset, already on the board over its door), a commodity word out of the trade's
own attested advertisement (Peck's *"dry goods, hardware and groceries"*, Jones's *"grocery and
provision store"*), and a destination with the one port this project has in writing (Buffalo, from
the schooner arrivals in the dossier). Nothing else — no trademark, no price, no date, no maker this
town is not recorded as dealing with. Everything is `reconstructed`, on every vertex, so hiding that
tier still takes the whole layer away, marks and all. L131's "no marks" clause is superseded and
keeps its reasoning verbatim.

**It costs nothing.** The marks are a texture atlas on the layer's existing single material, so the
town has the same triangles, the same materials and the same draw calls it had before. Everything
unmarked samples a white cell, which multiplies to the timber it already was.

**Verification.** `tools/check.sh` green. `tools/smoke_renderer.mjs --published` green on mobile
390×780 stages 1, 2 and 4 and on desktop 1280×800 stages 1 and 2, with two new gates in the yard
section — every cask and case marked, and every uv on the sheet. **Two knowingly unrun and one
knowingly red:** desktop stages 3 and 4 do not fit the ten-minute foreground ceiling on this runner
(**T-0121**, open), and mobile stage 3 carries the two road-legibility failures of **T-0114**, whose
numbers are unchanged by this parcel to the decimal (walker 100–250 m ΔL* 1.8 of 3.2, weber 0.0795;
aerial 250–600 m ΔL* 2.0 of 4.6, weber 0.0922). The marks were also read off the render at the
Tremont House and Peck's store frontages — which is how the first build was caught writing every
case in the town mirrored.
## Shipped 2026-08-22 — T-0130: the signs read as the trade wrote them

**The ask (owner, 2026-08-21), of the Philo Carpenter board T-0066 had shipped:** *"philo would
not have referred to his own place as log drug store, it would be philo carpenter, drugs and
medicines, or druggist or whatever he would have referred to himself as on the sign, that may be
different than the name of the building for us, the sign may read differently historically."* Of
the next one: *"same with hogan's store."* Widened the same day: *"i guess do a pass on all those
signs and make sure they feel right for the era."* He then supplied **seven pages of 1833-35
Chicago newspaper advertising** in which the town's businesses write their own copy.

**The defect, in one sentence.** `_sign_text()` painted the structure record's own `name` and its
docstring defended that — *"the card a visitor opens by tapping the board has to say what the
board says"* — which collapsed two different objects. A record's `name` is OUR label for a
BUILDING; a signboard carries what the TRADE lettered. Thirty-three boards were carrying museum
captions.

**What shipped.** The wording is now its own field and may differ from the `name`. All 33 boards
are re-lettered from `SIGN_WORDING` in `tools/generate_business_signboards.py`, in the
advertisements' own register — proprietor or firm first and largest, the trade beneath, the place
last and smallest — carried per line with a role (`sign_lines`) and lettered in that hierarchy by
`renderers/web/js/signage.js`. **14 are `inferred`** on a firm's own advertised line, **19 are
`reconstructed`** from the trade vocabulary those pages evidence, and **0 are `attested`**. The
identity correction the owner named is made: "Hogan's Store" reads **BREWSTER, HOGAN & CO. /
Forwarding & Commission**, which the building's own `aka` already knew.

**Nothing is `attested`, and that is the owner's own ruling rather than caution.** The seven pages
were supplied as images in conversation and are **not committed** to `data/sources/assets/`; a
transcription is not a citation. His instruction, verbatim: *"I will give you all those data
sources later in a more comprehensive form proceed where you can and label reconstruction or
inferred with a note as you like."* So every newspaper-derived note quotes its advertisement, names
its date, says where the transcription came from, and says the value is to be **upgraded to
`attested`** when the pages land. **The four-step upgrade recipe is written into the T-0130
ticket** so it survives the run that wrote it. Goss & Cobb's page is committed already and is the
first to revisit.

**The golden mortar.** Carpenter's 1835 notice heads itself *"AT THE SIGN OF THE GOLDEN MORTAR"* —
a Chicago signboard described in print by the man who owned it, in the scene year — so a gilt
mortar and pestle is **painted** on his South Water board rather than the phrase being lettered.
**L25 is untouched**: it withholds an image nobody described, which is the opposite case. The
device does not generalise — one belongs to a shop only where its own advertisement names one —
and the smoke pins the count at exactly one rather than bounding it below.

**The check is CORRECTED, not relaxed.** T-0066 asserted string equality between board and card at
one board, which was the wrong invariant once the two fields separated. What replaces it is
`sign_identity` — the proprietor, firm or house, which must appear in both — asserted at the
Tremont's own board, over every sign in the town, and beside two new absolute assertions: no board
carries the word "log", and every board letters a trade as well as a proprietor. The generator
refuses to build if any of them fails.

**Cost: zero.** Measured on the published mirror, the signage layer draws **1,106 triangles in one
mesh before and after**, on the same 4096 × 1536 atlas — the lettering lives in the atlas every
triangle already samples, and the painted device is canvas too. Recorded in T-0115's ledger.

**Findings raised rather than buried**, in the record's own `findings` array: J. S. C. Hogan's
separate South Water dry-goods store, which the pages distinguish and the model does not carry;
Pierce & Abbott against this project's Asahel Pierce; P. Pryne & Co. against Pruyne & Kimball;
three advertisements that locate themselves by a neighbour and can be checked against this model's
placements; and a list of firms the pages name that the town lacks — none of which has been given
an invented building.

**Verification.** `tools/check.sh` green; smoke green at 390×780 (stages 1-4) and 1280×800 (stages
1-2), zero page errors, with only the known pre-existing T-0114 road-legibility reds in stage 3.
`docs/LIBERTIES.md` **L166**.

## Shipped 2026-08-21 — T-0072: the Wolf Tavern's sign flies from a pole, and the wolf is on it

**The ask (owner, 2026-08-18), of the sign close-up in image 4 of his brief:** *"its almost like a
flag, you should be able to get documentation of what this sign/flag was and put it at the tavern
correctly."* The ticket's own instruction was to do the documentation first.

**The documentation, and it was already in the dataset.** `chicagology_prefire273` — a source this
project has cited for the tavern's fabric since 2026-08-09 — carries, in a note at the foot of the
page: *"Wentworth was ambitious, and wanted a sign to attract wayfarers. Lieutenant Allen made one
for him out of a piece of a box. He painted a picture of a wolf on it. The fort blacksmith made
hinges, and the wolf sign was hung on a sapling. The tavern was the first institution to have a sign
board in Chicago."* Four things there are geometry, and the model had one of them: a board. A
**sapling** is a standing trunk, not the wall bracket the archetype had been building; the
**hinges** are ironwork nobody had drawn; and a **picture of a wolf** was on a board this project
had deliberately left blank. The owner's engraving draws exactly that arrangement from outside — a
mast-tall pole, a cross-arm, the board flying from it.

**What shipped.** Two new form attributes on the archetype. `sign_mount` = `sapling_pole`
(**inferred**), which builds a set pole clearing the ridge by 2.55 m, a lashed cross-arm, two iron
hinge straps and the board flying from them; and `sign_device` = `wolf` (**reconstructed**), a flat
dark silhouette painted on both faces. Both default off, so no other board in the town moved. The
tavern's mesh went 470 → 784 triangles and the town's frame is unchanged within its budget.

**The grading is the careful part, and it runs lower than the find suggests.** The sapling sentence
is in the page's editorial NOTE, not in the 1857 Chicago Magazine body that earned that source its
tier 2, and the note names no author and cites nothing. The cross-arm comes only from the
engraving, which is tier-5 pictorial and may drive form as `inferred` and never a coordinate. So
`sign_mount` takes the weaker half of its own value and reads `inferred`; the source record now
says where the passage sits and why.

**L25 is superseded, and that is the entry worth reading.** For eleven months this project held that
the board must stay blank because a wolf painted from imagination would be its most conspicuous
fabrication. The risk was real and the conclusion was wrong: a source says a picture of a wolf was
on that board, so an empty one asserts the opposite of the evidence in the one place every visitor
walks up to. What is lost is the draughtsmanship, not the subject. **L165** claims the outline, the
pole's every dimension and the pigment, and L25 keeps its reasoning verbatim with a pointer to it.

**Verification.** `tools/check.sh` green; `tools/smoke_renderer.mjs` green at 390×780 and 1280×800,
zero page errors, against the published mirror. All 43 `log_dwelling` masters rebaked in the same
commit — the parameter class gained two fields, so every building of that archetype re-hashed — with
their web derivatives, sidecars and `tools/publish.sh` mirror.

## Shipped 2026-08-21 — T-0133: four freight sheds on the north bank at the Dearborn crossing

**The ask.** Image 3 of the owner's brief of 2026-08-18 is an engraving of the reach below the
Dearborn drawbridge: masts crowding the water, a light structure near the mouth, **low warehouses on
the banks**. T-0133 is the second half of T-0071 (the first half, T-0132, built the bridge itself)
and its acceptance is that bank structures the plates attest stand at the Dearborn approaches, each
at its honest tier with a liberty for what was invented.

**What shipped.** Four `outbuilding` records on the **north** bank — `north_bank_shed_dearborn_w`
west of the bridge line and `_e1`, `_e2`, `_e3` downstream of it — low, unpainted, wagon door to the
river street. Three are vertical-boarded gables (27°, 30°, 33°) and one is a hewn-log shed roof at
23°; footprints are 20×32, 24×36, 18×34 and 28×44 ft, every one inside family **F1**'s own band
(18×32 to 28×50 ft). **Every value on all four is `reconstructed`**, including the fact that a
building stood there at all, and `docs/LIBERTIES.md` **L164** claims all 44 invented tokens.

**Where they stand, and it is a rule rather than a hand.** A tier-5 pictorial may drive massing,
form, materials and setting and may never drive a coordinate, so the plate decides only THAT sheds
stood here. The front wall is set 2.00 m back from the north edge of North Water Street's committed
track at each station, squared to the street's own bearing there, and every corner has to stand on
modelled ground above the water with ≤ 0.35 m of relief across the rectangle — the clause the infill
generators hold themselves to. All four clear the platted corridors, the committed footprints and
each other.

**Two limits stated in the open.** (1) They stand 4.5–10.5 m back from the traced 1834 waterline
with the river street between, not on the bank edge where the plate reads them: the modelled bank
climbs from water to plateau in three to four metres, and a building on that slope fails the relief
clause. T-0004 (raise and graduate the banks) is what would change the answer. (2) **The south bank
is empty for a measured reason.** At the Dearborn reach the platted South Water Street corridor
reaches to within about **1.7 m** of the traced waterline, so no building fits there that is not
standing in the platted street, and the corridor ratchet refuses a new one by construction. That
measurement is now its own ticket rather than something worked around.

**What it costs the count.** The inventory's district matrix allows the north division ONE
warehouse-or-freight roof and the Kinzie & Hunter forwarding store already holds it, so all four are
recorded in `1835_existing_roof_reconciliation.json` as substituting **zero** anonymous slots —
additions above the district's estimate, not substitutions inside it. `reconcile_665.py`
regenerated: 330 roofs standing, 335 remaining, and the north district's remainder falls 69 → 65.

**Verification.** `tools/check.sh` green; `tools/smoke_renderer.mjs` green at 390×780 and 1280×800,
zero page errors; all four masters, their web derivatives and their sidecars regenerated in the same
commit, and `tools/publish.sh` mirrored the result.

## Shipped 2026-08-21 — T-0070: the jail made accurate to its engraving

**The ask (owner, 2026-08-18):** the jail *"should be made more accurate"* to the engraving of the
first Cook County jail, image 1 of the 2026-08-18 brief. That plate draws a low log strongbox —
squared timber, a near-flat roof, minimal openings — with the fences and plank walks beside it that
T-0069 has already built.

**What was wrong.** `log_jail` carried a 32° gable, and 32° is not a finding: it is
`outbuilding_params.default_roof_pitch_deg`, the archetype's own default, kept deliberately on
2026-08-11 because nothing attested a pitch. The record said so in its own note. With a picture of
this particular building now in the dataset, a convention loses to it.

**What changed, and it is two attributes.** `roof_pitch_deg` 32.0 → **12.0**, still `inferred`,
with the plate as the reasoning: 0.486 m of rise over the 2.286 m half-span, ridge at **3.146 m**
where it stood at **4.089 m**. And `construction`'s note stopped calling hewn-versus-round
unattested — the plate draws squared logs laid horizontally, which is what
`common/logwork.hewn_log_wall` has been building all along, so the wall is evidence now rather than
a convention standing where evidence should be. The value's own grade (`attested`, Andreas) is
unchanged.

**What deliberately did not change.** The footprint (20 × 15 ft, `reconstructed`, invented), the
position, the bearing, and `wall_height_m` (2.66 m). A tier-5 pictorial may drive form, materials
and massing as `inferred` and **never a coordinate or a footprint outline** — the brief's own README
says so — and 2.66 m under a near-flat roof is already the low, squat building the plate shows.
Moving a dimension to match an impression would be inventing a measurement.

**`roof_type` stays `gable`, and that is a stated limit rather than an oversight.** The plate is
held here as the brief's WRITTEN record — the image binaries were supplied in-session and are not
committed; T-0075 owns identifying them against the Andreas plate numbering and creating the source
records — and "near-flat" does not distinguish one slope from two. A single-slope reading is a
legitimate rival that nothing this project holds can settle, and the record now says that in the
open. When T-0075 lands the plate as a source record, that is the attribute to revisit.

**Verification.** `tools/check.sh` green; `tools/smoke_renderer.mjs` green at 390×780 and 1280×800,
zero page errors; `tools/bake.sh --only log_jail` regenerated the master, the web derivative and the
sidecar in the same commit, so nothing is stale.

## Shipped 2026-08-21 — T-0066: the signboards say what they are

**The ask, verbatim (owner, 2026-08-18).** *"you can and should put the name of the location on
the sign board. the sign boards should have variation in color and style and signage font and
color, some signs may hang from an awning and others may be on the building or painted on the face
of the building. you need to add more signage and be period correct and it is fine if they are
reconstructions."*

**What it overrules, and it is this project's own writing.** T-0039 built the signage layer with
every board BLANK, and L130 argued the blankness was *"the second half of the honesty"*. That
argument was sound and the person it was written for has overruled it. **L25 is untouched**: its
subject is an IMAGE nobody described — the Wolf Point wolf — and no board in this town carries a
picture or a trade device. A NAME is a different object; the dataset already holds it and the card
already shows it.

**How a name gets onto a plank, in a project with no build step and no font pipeline.** The same
technique T-0082 used for the Green Tree's post board — a canvas drawn at load — scaled to a whole
town. Thirty-three signs in ten colourways cannot be thirty-three textures on a layer that is ONE
draw call, so the layer paints **one atlas** (a grid of 512×256 cells plus one cell of plain
weathered timber) and every triangle it emits carries a `uv` into it. A bracket arm samples the
timber cell; a board's two faces sample its own painted cell, mirrored on the back so the name
does not read backwards. **The lettering therefore costs zero triangles**, and the layer is still
one mesh with one material — the invariant the smoke has held since T-0039.

**What the record now decides, all of it re-derived byte for byte by `tools/check.sh`.**
`sign_text` (the record's own `name`, less a trailing parenthetical — so board and card agree by
construction); `mounting`, one of five; `style`, one of ten colourways × four letterforms; the
board's own width and height, derived from the length of its name inside the range its mounting
allows and inside the frontage it stands on; and `reach_m`, the furthest that mounting may put a
vertex from its own anchor, which is what the smoke holds each sign to.

**The variation is a rule, not a list.** A stable hash of the structure id sets a style preference
order and the first style is taken that no sign within 40 m already uses — neither its id nor its
ground colour. Mountings come from a per-trade-class cycle, advanced past anything a neighbour
within 40 m already hangs. Measured over the whole town: **0 of the 14 sign pairs within 40 m share a
style or a ground colour**, and the South Water row alone carries 10 signs on 4 mountings in 7
ground colours.

**More signage: 23 signs → 33.** The trade rule gains a WORKS AND WAREHOUSE class — three smiths'
shops (one refused, see below), three warehouses, two packing houses, a tannery, a soap and candle
manufactory, a brickyard — which paints its firm's name on its front and hangs nothing over a
footway nobody walked. That class carries one extra clause: the record's name must contain a
PROPRIETOR (a possessive or an ampersand), which refuses *"The Old Bank Building"* and *"Government
Blacksmith Shop"* in writing rather than painting a modern nickname on an 1835 wall.

**The mountings built:** `bracket_board` 6 (the wolf sign's own geometry, unchanged),
`awning_board` 7, `wall_board` 6, `post_board` 1, `facade_painted` 13. The post is the one mounting
that stands in the STREET rather than on the building, so it is refused — in writing, and the cycle
advances — wherever the fronting street's travelled track comes within a metre of where it would
stand, or where the frontage layer already lays a plank walk outside that wall. The Green Tree's
own post board (T-0082, L135) is the exemplar the shape is copied from and is untouched. A painted
band stands with its foot 2.30 m up rather than at the height a BOARD hangs at: measured on the
render, a band at board height lands across the doorway of every frontage that has one, behind any
surround standing proud of the wall. It drops back under the eave only where the wall has not the
height for both.

**Cheaper, not dearer.** The layer draws **1,106 triangles** where it drew 1,380 (−274), and
because the boards are the one piece of furniture still casting at `light` (T-0115 kept them
casting by measurement, and the smoke now asserts it) the measured frame falls by twice that.
Per mounting: a painted name is 2 triangles, a wall board 24, a bracket board 60, an awning 72, a
post 72. Recorded in T-0115's ledger.

**What is NOT claimed.** No source in this repository gives the wording, the colour, the letterform
or the mounting of a single sign in this town. Every part of all four is `reconstructed` on every
vertex, so hiding that tier takes all thirty-three down at once and leaves the town mute with one
wolf sign at the forks. `docs/LIBERTIES.md` **L158** is the claim and states the overrule of L130
explicitly rather than quietly editing it.

**Not verified.** The generator half (a baked town carrying its own boards) is still owed —
ROADMAP K5 (b) — and this is the renderer-side layer as before. The letterforms are browser font
stacks approximating the period's four working faces, not period type; legibility from a walker's
distance was the test that was actually applied, and it is a rendering choice rather than a claim.

## Shipped 2026-08-21 — T-0007: the material sheet reaches the town

**The ask.** R-W2a measured the town's surfaces and wrote `docs/RESEARCH/materials.md` — 1,353
material slots, 32 names, 41 colours, 18 roughness values, zero textures — and the document
reached nothing. Every colour in this project was a literal in whichever module happened to
paint that surface. Texture scored **1.4** on R-G1's table, the worst axis on the board.

**What now decides a surface.** `generators/common/materials.py` is the sheet as code, and it
splits a surface the way §2.1 already did: a **substrate** owns the roughness, the tile and the
module the tile is a whole number of; a **finish** owns the colour, and the three coatings own a
roughness that overrides the substrate's. `resolve(substrate, finish)` is what the exporter
gets. The tile rates ride along unused, so the bake half draws its atlas from the same numbers
rather than a second set.

**The wiring, which is the parcel.** `from_phase(phase, record)` now takes the record as well as
the phase, because the finish the 665-roof programme dealt a building is not a form attribute —
it sits in `reconstruction`, one level up, which is exactly why no archetype could read it.
`mesh_inputs.resolve_params` passes the same pair, so the staleness hash still sees precisely
what the builder sees. **222 records carry `finish_key` and 218 carry `roof_condition`**, and
until this parcel both were read by `generators/inferred_placeholder.py` alone.

**What moved in the shipped bytes.** 207 of 243 committed GLBs. Wall colour on every archetype
building now comes from the record's dealt finish unless a record states a coating, which still
wins — the Sauganash's attested white among them, at the sheet's 0.60, the only smooth wall in
Chicago. Roof colour comes from the weathering condition, so 234 roof slots that were one colour
now carry four. Wall roughness moves onto the sheet's per-substrate values (clapboard 0.86, hewn
log 0.92, sawn board 0.94, brick 0.90, rubble stone 0.93, trodden earth 0.95). Finding 2 is
discharged: `LOG_RGBA` is deleted and the Sauganash's log wing is built from the town's log
rather than from the paler value nothing else used. Finding 5 is discharged: three whitewashes
became one and two reds became one, and both generators read the same table — the placeholder
GLBs are byte-identical, because the convergence went onto the vocabulary the RECORDS speak.

**Triangle-neutral, and material-count-neutral, by measurement.** Diffed against `HEAD` over all
207 changed GLBs: triangle delta **0**, and **not one asset changed its material count**. The
second is not incidental — K36(a) put the palette-fold threshold at five materials and 275
assets sit at four, so a sixth surface would tip all of them at once. This parcel varies values,
never slot counts. Recorded against **T-0115**, whose ceiling is breached.

**What stayed honest.** **R-W2a finding 2 stands.** No source in this repository states what any
Chicago roof of 1835 was covered with, so the sheet has no `shingle` row and no `roof_board`
row: it has one `roof_plane` substrate whose note says the covering is unstated, and four
weathering conditions the records actually carry. Every archetype's roof ROUGHNESS is left as
its own committed literal, because §2.2 separates a board roof from a shingle field by 0.03 of
roughness and moving that number either way would be choosing a covering nobody wrote down.
`docs/LIBERTIES.md` **L155** owns the three interpretive choices: that a dealt finish outranks a
`paint` the archetypes themselves defaulted into the record (the 44 records carrying both AGREE,
so it is not a tie-break), that roof colour follows weathering, and that the roughnesses are
reasoned rather than sourced.

**The frames.** Critic stations re-shot on the published mirror at the identical stands
(`tools/critic_shots.mjs --published --viewport desktop`). At `south_water` and `from_above` the
change is small and honestly so — those stands look at NAMED buildings, which carry no
`reconstruction` block and therefore keep exactly the colours they had. At `lake_market` the
Sauganash's log wing visibly changes timber (finding 2). The repaint itself is photographed
where it lives, in the reconstructed south blocks, against a mirror rebuilt from `HEAD`'s own
web derivatives at the same stand: **8.20 % of the frame moves, mean |Δ| 62 of 255 over the
differing pixels.** Pairs: `docs/evidence/t-0007-{before,after}.png` (south_water),
`t-0007-sauganash-{before,after}.png`, `t-0007-south-blocks-{before,after}.png`.

**Split out, not half-done.** §2.3's four values for one dark opening and finding 3's one
`timber` name over two materials are the openings-and-glazing family, not the wall-and-roof
family this parcel wired; they are **T-0126**. The atlas, the roughness MAP §3.1 asks
for, and the shingle exposure remain the bake half's and are unresolvable from what this project
holds. Finding 1, the chimney, is T-0008's and opens with a research question rather than a
palette.

## Shipped 2026-08-20 — T-0110: the road ribbon follows the ground it claims to lie on

**The ask.** The owner, an hour after T-0046's earthworks landed, walking Kinzie onto the North
Branch bridge: the track "gets pixely and you can see grass triangles and it ends with a black
line and more grass, prob make it dirt road all the way."

**The mechanism was not the one the ticket suspected.** Replayed against the committed
heightfield, the water trims hold FULL width up both ramps — no sawtooth, no early stop from
`MIN_PANEL_W_M`. The fault: a street panel was one planar quad, 2.25 m long and two vertices
wide, and an embankment is not planar. Between the corners the fill's crest rose through the
ribbon by up to **1.49 m** (Kinzie west approach; 1.41 m east, 1.09 m where North Water crosses
the Dearborn approach fill), the opaque terrain won the depth test, and the road was simply not
drawn there — the owner's wedges and his road "ending" short of the deck. The smoke's
`worstDrape < 1e-5` gate stayed green throughout because it samples vertices, and every vertex
was perfectly draped.

**What shipped.** `streets.js` refines a panel — halving both axes, to at most 8×8 — while its
draped grid misses the field between its own vertices by more than `DRAPE_TOL_M` (0.03 m).
Every new vertex samples `terrain.surfaceHeight()` at its own stored float32 position; interior
rows re-run the same `dryReach` trims; a level is refused if any new row centre or vertex lands
on water (the R-BUG4 clip rule binds interiors too), and panels touching off-grid ground stay at
level 0 rather than refine against the fallback constant. A level-0 panel emits byte-identical
geometry to the old code, so the flat town — 4,784 of 5,055 panels — is arithmetically
untouched. Cost: 271 refined panels, ~+9k triangles town-wide (~1.5 % of the 'light' ceiling;
mobile frame measured 538,986 of 600,000). `terrain.js` gains `inBounds()` /
`Heightfield.contains()`. Two new permanent smoke gates: the ground never rises through a panel
between its vertices (bar 0.35 m, measured worst 0.22 m at two waterline nose tips under the
deck ends, failure class 0.9–1.5 m), and centreline stations up both North Branch approaches and
the Dearborn fill must land on drawn roadway. Evidence pair at the owner's stand:
`docs/evidence/t-0110-{before,after}.png`.

**Scoped out, measured, ticketed.** Dearborn's record ends at n 18, 2.7 m short of its causeway
deck end. The one-line fix — bending `path_local_enu_m` onto the fill — was built and REVERTED:
`generate_plat_lots.py --check` re-derives every block face by offsetting the whole street
polyline, so a 3 m track bend moves platted lot lines, and the extended corridor makes the
drawbridge's draw a new corridor intrusion (0.61 m). The plat line and the worn wheel line are
different claims sharing one field; **T-0111** filed with the diagnosis and the acceptance.

**Verification.** `tools/check.sh` **CHECK PASS**. Smoke halves on the published mirror, cut at
565 s per the T-0060 posture: mobile **223 passed / 3 failed** — the same three ungated
road-contrast rows the last several merges shipped under, all on level-0 (unchanged) streets;
desktop **156 passed / 0 failed** at the cut, which lands before the street section. A targeted
standalone desktop run on the published mirror therefore probed EVERY street vertex and
triangle: drape 1.2e-7, wet 0, worst interior sink 0.220 m, zero approach-station gaps, zero
page errors.

## Shipped 2026-08-19 — T-0046: bridge approach earthworks meet the deck at grade

**The ask.** The second half of T-0001's "how would a wagon cross that?" — the walker-deck half
(#231) made every deck a floor, and nothing let you reach one: each deck ends on the traced 1834
waterline, where the bank ramp puts the ground at exactly zero, 2.2 m below the planks.

**What shipped.** An `approaches` block in `terrain_spec.json` — eight graded road corridors,
every entry `reconstructed`, applied by `terrain_gen.py` after the bank ramp as max()/min()
against the assembled surface so each dies out where natural ground takes over. Six FILLS at
1 in 12 carry Kinzie Street onto both ends of the North Branch bridge, the South Branch bridge
onto its banks, and Dearborn Street onto the drawbridge, each crest run 3 m past the deck end
into the shallows as the fill the attested log abutment cribs retain; two CUTS grade the banks
DOWN to the slough crossing's low deck, which sat 0.35–0.49 m below its own ends. Crests pack
`APPROACH_SEAT_FT` (0.06 ft) under the plank line — physically the fill packs under the boards,
numerically it keeps a 5 mm-quantised crest from floating a float's width above the deck and
stealing the walker's floor. All four bridges now land: `ground_contact` declarations dropped,
L30/L38/L69 moved to Resolved, the invention recorded as **L147** with per-approach terrain
Covers tokens. Ground rebaked at the committed 0.03° decimation (250,030 tris, +2.5k on the
committed ground; fit 3 mm max). The 16-bit web derivative regenerated because the master moved
— the shipped lattice goes 306 mm → 77 mm, which is T-0012's subject but NOT its ≤ 13 mm
acceptance; that ticket stays open. Planting-reach baseline re-banked (+38 nodes the fills
raised out of the water margin). **T-0109 filed**: the slough crossing still spans solid ground
mid-deck — the watercourse under it is not cut into this epoch (L69's old point, now a ticket).

**Verification.** `tools/check.sh` **CHECK PASS** (validator, staleness, liberties compile,
changelog contract v199, publish sync). Smoke halves on the published mirror, cut at 565 s each
per the T-0060 posture (unchanged, same condition T-0062/T-0063/T-0108 merged under): mobile
**232 passed / 3 failed** — all three are the `(reported only)` road-contrast rows; two are the
long-tracked pair, and the third (`lake_market`, "standing on the crossing itself") is **newly
reporting** — that stand is 67 m from the south-branch fill and the raised ground plausibly
moved its band statistics; the row is ungated by design and is left to the road-contrast
programme's re-baseline rather than adjusted here. Desktop **156 passed / 0 failed** at the cut.
All five bridge assertions green at BOTH viewports inside the cuts, including the new permanent
one: **a walker on the bank climbs the approach onto the deck** (no teleport, terrain only). A
targeted standalone run (both viewports, published mirror) walked bank → approach → 72 m span →
off the far bank with **zero page errors** end to end — the tail assertion the ceiling keeps
cutting from the full smoke.

## Shipped 2026-08-19 — T-0063: boats correct for the era, on the water

**The ask.** The owner, 2026-08-18, verbatim: *"you can add boats correct for the era! they
would exist"* — and, of the drawbridge engravings, *"also note the boats there."* Under the
standing ruling to be liberal with reconstructed items and label them as such.

**What shipped.** A new derived layer — `data/boats/` + `renderers/web/js/boats.js` — puts
nine watercraft on the river: three two-masted lake schooners moored in the reach of the main
stem below the Dearborn Street drawbridge (the stretch images 2-3 of the 2026-08-18 brief
crowd with masts), two rowboats on the water off the South Water bank and two drawn up at its
edge (image 11), and two bark canoes hauled out on the bank below Fort Dearborn (the committed
2026-08-11 fort plates). Every hull is unmanned, unnamed, and graded `reconstructed` at every
vertex — the whole flotilla disappears when a visitor hides `reconstructed`. Aiming at a boat
opens its own card (type, size, state, and what bounded each invention) — the first pickable
thing in the scene that belongs to no structure record. The invention is claimed at LIBERTIES
**L146**. The schooner Illinois is deliberately NOT drawn or named: a named vessel at a berth
on a date is a claim no source makes.

**The layer refuses rather than adjusts.** An afloat hull is drawn only with its full draft
plus 0.3 m of water under the whole keel (checked against the committed heightfield at load);
a beached hull only on bank ground at the water's edge; and nothing within 30 m of the
drawbridge's crossing line, so the navigation span stays clear for T-0071. Zero refusals in
the shipped record — every position was chosen against the heightfield first.

**L1 and the standing constraint.** The canoes are trade watercraft drawn unmanned from the
plates that show them at this reach; no figures, no encampment, no staging. The record's own
`standing_constraint_note` says so, and any depiction of the Potawatomi themselves remains
out of scope pending consultation.

**Verification.** `tools/check.sh` green (validator, liberties compile, published-mirror
trace — `data/boats/` added to `check_published.mjs` COPIES — changelog contract).
`tools/smoke_renderer.mjs --published` run as its two halves in the foreground: mobile
**338 passed / 3 failed** — a COMPLETE mobile pass for the first time in days, including
`zero page errors` green; the three failures are dev's own, all pre-existing and tracked
(the two `roads reach the screen` rows already recorded in this file, and the Evidence-panel
`counts nothing by hand` row, which is open ticket **T-0037** and was simply never reached by
the runs the ten-minute ceiling cut earlier). Desktop **185 passed / 2 failed** (the same two
road rows, reported-only) before the ten-minute ceiling cut it at the shadow-reach captures
(**T-0060**, unchanged). All eight new boat assertions green at BOTH viewports, including the
schooners-reach-the-screen capture from the south bank and the boat's own card answering a
pick. Scene-detail note: `light` measured **597,894 of 600,000** at 1280×800 on this branch —
inside its ceiling with the boats mounted (T-0089 updated with the figure).

## Shipped 2026-08-19 — T-0062: more docks — the working waterfront, as far as the trace reaches

**The ask.** The owner, 2026-08-18, verbatim: *"you can add more docks!"*, under the standing
ruling to be liberal with reconstructed items and label them as such. T-0041 had drawn the only
two docks any source states and refused the rest of the river by rule; the override is the rule
now.

**What shipped.** Five South Water merchant records — J. H. Kinzie's forwarding store, Jones's
grocery and provision store, Harmon & Loomis's, Peck's, and Carpenter's South Water store — now
STATE a dock at `confidence: reconstructed`, each with its bound in its own note (the trade that
takes goods off the water; the mast-crowded reach of the 2026-08-18 brief, image 3; the south
bank's wharfing-out practice). The wharf generator accepts the reconstructed grade (the grade
clause T-0041 shipped is overridden, and the rule's selection still lives in the data — a record
with no dock statement still gets nothing; the Temple Building on the same frontage stays bare).
**Two of the five landings are drawn** — Kinzie's and Jones's, timber decks on cribs off the
traced bank, pickable to the store each serves — so four docks now stand where two did. The
invention is claimed at LIBERTIES **L145**.

**What is NOT drawn, and why that is the honest reading.** The traced 1834 bank polylines end at
local **E 390**, and Carpenter's, Peck's and Harmon & Loomis's frontages lie east of that. Before
this run the generator snapped all three to the trace's terminal vertex — three decks stacked on
one point, silently. It now refuses a deck any metre of which would stand off untraced bank
(clause 4b), with the reason on the record; **T-0106** owns extending the trace to the drawbridge
reach, and the three refused landings draw themselves when it lands. The staleness gate also
stopped sweeping `dock` into the frame_storefront mesh hash — a statement the builder never reads
was marking five stores stale when not one of their vertices could move.

**Verification.** `tools/check.sh` green (validator, wharf re-derivation, liberties compile,
changelog contract). `tools/smoke_renderer.mjs --published` run as its two halves, both cut by
the runner's ten-minute ceiling (**T-0060**, unchanged): mobile **223 passed / 2 failed**,
desktop **147 passed / 0 failed**, zero page errors on either — the two mobile failures are
`the roads reach the screen from the walker's eye` and `…from the air`, already recorded in
this file as dev's own and untouched by this branch. All eight wharf assertions green at BOTH
viewports, including the updated census pinning 4 drawn + 3 refused.

## Shipped 2026-08-19 — T-0079: the core density standard, and three roofs on one lot

**The ask.** Piece 3 of 3 of T-0073, the owner's flagged-important ask of 2026-08-18: *"there
should be more and denser buildings. this is important."* T-0077 put four roofs on the Lake Street
line at Dearborn and T-0078/T-0102 built the South Water row; both moved roofs that already
existed onto a frontage. This piece is the one that had to raise the BAR, because the rest of the
core cannot be tightened by rearranging what stands there.

**What was actually in the way, and it was arithmetic.** A platted block's ceiling was
`lots + round(lots × 154/511)` — one principal roof per lot, ten roofs on an eight-lot block — and
a party-line run carried exactly one roof per lot it was dealt. So "a row is denser than the lot
grid" was a sentence with no arithmetic behind it, and **every remaining core block read
`at_capacity` with 11 to 14 roofs standing against a ceiling of 10**. Five of the twelve core
blocks the plat module reaches were already ABOVE the rule, put there by the reviewed phase-one
parcel and the documented record. A ceiling the town passed by two fifths before it was written is
not bounding anything; it was only refusing the next roof, which is the one the owner asked for.

**And it was counted in the conjectural unit.** The side lot lines are conjectural — every record
this project writes says so in its own position note — while the block FACE is committed geometry
derived from the street centrelines. The old rule counted a block's capacity in the unit the grid
grades lowest. `tools/reconcile_665.py` said so itself and declined: *"a denser core would be a
decision about lot subdivision, and four lots to a face is a reading of ONE block that the grid
itself grades `conjectural`, so that decision is not taken here."* **It is not lot subdivision.** A
run does not divide the lot; it stands across the face, and the side lines it crosses were never
claimed.

**The standard, and its number is measured rather than chosen.** Three party-line units per platted
lot, taken at the WORST case so it holds for every lot on the grid: the smallest committed lot
carries **23.56 m** of frontage, the plat module keeps **1.5 m** clear of a side line at each end of
a run, and the **eighteen** party-line units already committed average **6.072 m** wide — so
(23.56 − 3.00) / 6.072 = **3.39**, three fit on the meanest lot in the town and the fourth does not.
A run across adjoining lots pays the two end margins once rather than per lot, so 3 × lots is
conservative there too. The standard is recorded in
`data/reconstruction/1835_platted_block_parcels.json` § `placement_rule.density_standard`, which is
where T-0028's block-building successors will read it, and its three clauses are: a commercial
frontage tightens toward party-line spacing; an improved lot carries its outbuildings; **a corner
lot builds to the corner**.

**The third clause needed a generator change.** An east-anchored run packs back toward the block
corner and stops wherever its roofs run out, so the corner was the one piece of frontage a row
could never reach. `place_frontage` now takes `corner: "west"` and `abut_east_of` — the same party
line read from the other side — and `check_frontage`'s party-wall assertion takes the smaller of
the two readings rather than branching on the recipe's key, so it stays a measurement of the
geometry and cannot be satisfied by relabelling an anchor.

**What shipped, and where you can stand to see it.** `blk_lake_clark` — bounded by Lake, Dearborn,
Randolph and Clark, and one of the five blocks that refuted the old ceiling with twelve roofs
against ten. Six of its eight lots arrive taken, all six seated by `tools/plat_occupancy.py`; the
free two are lot 0, the Lake-and-Clark corner, and lot 5 on Randolph. The face rule is T-A13's,
re-measured here: counting every committed structure that is not an anonymous count-unit and
stands within 25 m of a street's committed centreline, **Lake carries 21 and Randolph 13** — 15
against 6 counting documented records only — so Lake is this block's business face. The end rule
is T-A11's, unchanged: lot 0's frontage midpoint stands **177.9 m** from the foot of the Dearborn
Street drawbridge and lot 5's **215.8 m**, so lot 5 is the open one, as the farther lot has been on
every block of this row.

**Three principal roofs stand on lot 0 where the old gate allowed one** — a log dwelling on the
corner, a one-room cottage, a deep-plan cottage — occupying **16.86 m** of the lot's **21.75 m** of
buildable frontage, on one line, at one 1.5 m setback, on two shared party walls. The run is
west-anchored, so the log dwelling's west wall stands **1.50 m** from the Clark side line and the
4.89 m that remains is at the east end where the run stops, **10.58 m** short of the bakery on the
next lot. The fourth roof is the standard's second clause: the privy stands in lot 0's own yard at
the alley end. No coordinate is authored — the line, its bearing and the end the run packs away
from are read from the committed block boundary.

**No roof was added to the town.** The four come out of `south_plat_beyond_committed_control`, the
south district's balance waiting on street control past State and Washington, which fell from
**175 roofs to 120** when the ceiling rose. Every marginal still closes: the units sum to their
districts and the districts to 665. That redistribution is the ticket's own count-honesty clause —
budget moves inward before any liberty grows a total — and no liberty about the total was needed.

**What is unverified, and it is everything that matters.** That any building stood on this ground,
that there were three, that they stood shoulder to shoulder, and that the corner one was of logs
are all inventions, recorded in **L144**. Whether the schedule may deal a log dwelling to a
commercial frontage is **T-0022** and is still open; what decided it here is that the owner's own
reference for a party-line row draws it as *log and frame buildings shoulder to shoulder*, so the
question stays open for the schedule and this parcel is one recorded instance.

**One defect found and filed rather than normalised away.** T-0077's row on this same Lake face
stands 0.80 m off the face line and this generator's floor is the plat module's 1.5 m lot margin,
so **one block face now carries two street lines 0.70 m apart**. They are 10.58 m apart along the
face and no wall steps between them, but that is luck rather than design: **T-0104**.

**Gates.** `./tools/check.sh` — the dev gate — **green**, run in the foreground after
`./tools/publish.sh`. `node tools/smoke_renderer.mjs` — see the PR for exactly which halves ran
inside the runner's ten-minute command ceiling (**T-0060**, unchanged) and how `zero page errors`
was answered at both viewports. Before/after frames from the same stand in Lake Street at
`docs/RESEARCH/lake_clark_corner_{before,after}_2026-08-19.png`.

## Shipped 2026-08-19 — T-0102: the two-storey stores that anchor the South Water row

**The ask.** Piece 2 of 2 of T-0078. T-0101 stood the fourteen South Water roofs on the frontage
line and could not build the one thing the owner's reference for the reach also shows: **two
two-storey frame stores anchoring the east end of the row** (image 11 of
`data/sources/assets/owner_brief_2026_08_18/README.md`, *"South Water Street in 1834"*).

**Why it could not be built then.** `check_block` holds a parcel to the family mix it claims, and
all five South Water blocks were dealt D-family dwellings — no C3, no C4, no D7. So the town's
business front was a terrace of one-storey cottages by construction, and the ticket named the two
routes out: re-deal the schedule, or grow the 665-roof total under a liberty.

**The choice, which was the work.** The total does not move, and it did not need to. The
programme carries **seventeen C3 narrow two-storey stores and eight of them stand**, so nine were
already unbuilt and apportioned to the districts rather than to any block — the programme file
says so in its own words: *"a per-unit family mix is an apportionment of that district's
remainder, not a claim about any block."* Two of those nine stand here. The D5 deep-plan cottage
and the D4 two-room cottage they displace go back into the south district's remainder, which held
34 of each before this run and holds 35 after it. **Growing 665 to buy roofs the programme
already owned would have been inventing headroom the town does not need**, so it was refused and
the refusal is recorded in L143 rather than left as a road not taken.

**What shipped.** `blk_south_water_dearborn` — the last block of the row, where State Street is
the platted town's eastern limit, so its east corner IS the row's east end — is re-dealt from
`{A3, D1, D2, D3, D4, D5}` to `{A3, C3×2, D1, D2, D3}`. Six roofs, five principal and one
ancillary, against the same headroom of six. The run is re-chained so the two stores take the
block's east corner and the surviving D3 stands west of them: **6.24 m and 5.74 m wide, 13.3 m
and 13.0 m deep, 5.94 m to the eaves against the 2.47 m of the cottage beside them**, on the same
line, the same 1.5 m setback and the same shared party walls. No coordinate is authored — the
line, its bearing and the corner the run packs back from are read from the committed block
boundary, exactly as T-0101 left them.

**No mesh was hand-authored and no bake was needed.** Both stores resolve through the
`frame_storefront` placeholder, which `generators/inferred_placeholder.py` builds in pure Python
from the committed record; the two records that went were placeholders too, so no night's Blender
work was overwritten. Their web derivatives compress LARGER than their masters, so both are
banked as decided passthroughs in `tools/web_derivative_baseline.json` (K38) rather than left to
look like an accident.

**What is unverified.** Nothing about the stores is evidence: that a store stood on this corner,
that there were two, and that they were two storeys are all inventions bounded by the C3 band and
the 1834 view's treatment, recorded in L143. The surviving D3 keeps its id and the household the
inferred-household layer housed in it; L142's Covers field is corrected in place — with the
correction stated in the entry rather than made silently — because two of the ids it claimed no
longer name a building.

**Gates.** `./tools/check.sh` — the dev gate — **green**. `node tools/smoke_renderer.mjs
--published` **ran to completion in BOTH viewports for the first time in weeks** (55 minutes on
this runner, blocked on in the foreground): **654 passed, 7 failed**, and `zero page errors`
PASSED at 390×780 and at 1280×800 — the assertion T-0060 warns is the one that goes unrun.

**All seven failures are `dev`'s own and every one is already recorded in this file above:**
`the roads reach the screen from the walker's eye` and `…from the air` at both viewports (four),
`the panel states that once too — and counts nothing by hand` at both viewports (**T-0037**, two),
and `scene detail 'light' stays inside its own ceiling` at desktop (**T-0056**, one — 604 950 of
600 000 tris when last measured). **The last one was checked against this branch rather than
assumed**: the two placeholder meshes this parcel removed carry 36 triangles each and the two it
adds carry 42, so the whole change is **+12 triangles** against a ceiling already over by 4 950,
and the draw-call count cannot move because the object count does not.

## Shipped 2026-08-19 — T-0078: the South Water river row

**The ask.** Piece 2 of 3 of T-0073, the owner's flagged-important ask of 2026-08-18. His
reference for this reach is image 11 of `data/sources/assets/owner_brief_2026_08_18/README.md`
— *"South Water Street in 1834 — now Wacker Drive"* — which shows the south bank of the Main
Branch as a **continuous working row**: roughly ten one-storey log and frame buildings shoulder
to shoulder facing the river, the street between them and the grassy bank.

**What was actually wrong.** The five platted blocks between Franklin and State carry fourteen
anonymous roofs on their South Water faces, and the platted-block generator had one way to place
a roof: centred on its own lot, at a period setback, with a lateral nudge. So the town's business
front read as **6 m of building, then 14 to 20 m of grass**, every unit 6-8 m behind the
frontage the documented stores stand on — and, because the placement rule takes its bearing from
the way INTO the lot, every one of them **facing the middle of its block with its back to the
river**.

**What shipped.** A **frontage run** in `tools/generate_block_infill.py`: a slot may declare
`stands_on: "frontage"` instead of a lot, and it then takes the line, its bearing and the end it
packs back from out of the committed block boundary in
`data/traces/vectors/thompson_lots.json`. The recipe authors no coordinate. Anchors chain — the
unit at the east end off the end of the run's own frontage, each unit west of it off the wall of
the one before — and a third anchor, `clear_west_of`, lets a run break around a documented
building that stands proud of the platted line. The face arithmetic itself moved to
`tools/block_faces.py`, imported by this generator and by the one T-0077 wrote it in, because a
second copy of it would be a second opinion about the same ground.

Applied to the fourteen: **six runs — three at Franklin (77.6-95.0 m along the face), two plus
one at Wells, three at LaSalle, two at Clark, three at Dearborn — 85.6 m of continuous built
frontage on one line, at a uniform 1.5 m setback, every front on the face's own bearing.** The
2.4 m break in the Wells run is the smallest the three-metre separation rule allows against
Carpenter's store, which stands in the corridor on coordinates typed before the plat module
existed.

**Nothing was added and nothing was renamed.** The five parcels deal the same roofs; the
665-roof programme's totals do not move; every id, family band, dimension and baked placeholder
mesh is the one it was. Only fourteen `position` blocks changed.

**Three gates had to learn what a row is.** A run holds no lot per unit, so the one-roof-per-lot
ledger now counts the run against the lots the recipe names for it and refuses a run that
carries more roofs than lots. Containment moved from the single lot to the run's own strip: the
**outer** side lines, the street line and the rear line keep the full 1.5 m margin, and only the
**conjectural interior side lines** are crossed. And the three-metre separation rule takes the
same narrow exemption L141 gave it — a record that NAMES its neighbour in
`reconstruction.frontage.abuts`, gated at both ends to be a shared wall rather than a near miss.

**Two honest consequences, both recorded in L142.** A run of three packed roofs occupies about
19 m where three lots span 75, so the 665-roof re-derivation now reports **three** roofs
schedulable on committed ground where it reported one — density frees platted lots, and a later
parcel that builds on them is making its own claim. And the row's 180° turn is a *correction*:
`docs/GLB-CONTRACT.md` pins `rotation_deg` as the facade bearing and every documented South
Water store carries 0, while this generator's other placements — Lake-facing and alley-facing
roofs across twelve blocks — still face away from their streets. That is filed as its own ticket
rather than swept into this one.

**What this ticket did NOT do**, and why T-0078 was split rather than stretched: the view's
**two-storey stores at the east end** cannot be built from what these blocks were dealt. Their
schedule mix is all D-family dwellings — no C3, C4 or D7 — so a two-storey store anchor needs
either a schedule change or a documented liberty growing the total, which is one more
demonstration and therefore one more ticket (T-0095).

**Verification.** `./tools/check.sh` — the dev gate — green. `tools/smoke_renderer.mjs` run as
its two halves, both killed by the runner's ten-minute ceiling (**T-0060**, unchanged): mobile
**222 passed / 2 failed**, desktop **147 passed / 0 failed**, and the two mobile failures are
`the roads reach the screen from the walker's eye` and `…from the air`, already recorded in this
file as `dev`'s own and neither touched by this branch. Because `zero page errors` is the last
line of each viewport and neither tail ran, that question was answered separately and in the
foreground: a scratch harness booted the **published mirror** at 390x780 and 1280x800 and found
**zero page errors at both**. Before/after frames from the same pose on South Water at
`docs/RESEARCH/south_water_row_{before,after}_2026-08-19.png`.

## Shipped 2026-08-19 — T-0077: the Lake Street row at Dearborn

**The ask.** Piece 1 of 3 of T-0073, the owner's flagged-important ask of 2026-08-18: *"there
should be more and denser buildings. this is important."* He sent the Tremont House street scene
(`data/sources/assets/owner_brief_2026_08_18/README.md`, image 5) — a continuous two-storey
storefront row on shared party lines, which he reads as looking south-west from Lake and Dearborn
— beside a screenshot of that same corner in the render, where the Tremont stands alone on grass.

**What was actually wrong, and it was not a missing building.** The Clark–Dearborn block already
carried twelve anonymous roofs. Four of them sat on the phase-one parcel's `lake_front` row, which
is a shared northing and a list of eastings with a metre of jitter on each — **17 to 24 m behind
the Lake Street frontage**, and no two of them on one line. That is the right shape for the
interior of a block and the wrong shape for a street. The frontage itself held two buildings, the
inferred bakery and butcher's market, 34 m apart.

**What shipped.** A **party-line frontage** mode in `tools/generate_inferred_infill.py`: a
placement may declare that it stands on a block FACE instead of at the row's northing, and it then
takes the line, its bearing and the corner it packs back from out of the committed block boundary
in `data/traces/vectors/thompson_lots.json`. The recipe authors no coordinate. Anchors chain — the
corner unit off the block's own Dearborn corner, each unit west of it off the wall of the one
before, and a run may butt onto a building this parcel did not write. The jitter is suppressed,
because a shared party wall is one wall and cannot wander.

Applied to the four: **`_c3_015` (the two-storey store) on the Dearborn corner, then `_d5_016` and
`_d4_014` west of it — 19.4 m of continuous front — a 3.6 m gangway, then `_d3_013` butted onto
the west wall of `inf_butcher_market`.** 34.0 m of the block's 98.6 m Lake face is now built
frontage where 11.0 m was, and the corner run stands 1.0 m clear of the platted Dearborn corridor.

**Nothing was added and nothing was renamed.** The parcel still deals 40 principal and 8 ancillary
roofs; the 665-roof programme's totals do not move; every id, family band, dimension and baked mesh
is the one it was. Only four `position` blocks changed. That was a design constraint, not an
accident — the recipe's eastings still fix the sequence, and the sequence is what names a unit and
deals it a footprint.

**Two gates had to learn what a party line is.** The three-metre separation rule in
`tools/generate_inferred_households.py` refused `_d3_013` for touching the butcher's market, which
is correct for every other case it has ever seen and wrong for this one. The exemption is exactly
as wide as the claim that earns it: a record that NAMES its neighbour in
`reconstruction.frontage.abuts`. `check_frontage` in the infill generator gates the other end —
one line to the millimetre, and a declared party line that is really a gap is a failure. A building
that merely happens to be close still fails.

**What it costs, stated.** The row crosses the conjectural side line between lots 4 and 6 and puts
three roofs on one 24.6 m lot, which is defensible only because those side lines are the plat
module's own inventions and because 80 ft business frontage is exactly the ground that got
subdivided. One dooryard garden derived away when its lot stopped holding a single dwelling.
Recorded as **L141**.

**Not claimed.** This is one corner, not the downtown. T-0078 (the South Water river row) and
T-0079 (the remaining core blocks) are the rest of T-0073 and are untouched. The plate's
signboards, awnings and plank walks below the fronts are T-0066 and T-0069 and none of them is
built here.

## Shipped 2026-08-19 — T-0044: the fort road, and the two Fort Dearborn plates read against the render

**The ask.** T-0006's third and last piece: *render each landmark from its reference plate's
viewpoint, compare, improve* — on the next two UNticketed plates. Every plate of the owner's
2026-08-18 brief already has a ticket, so the next two are the **two Fort Dearborn views** in
`data/sources/assets/prefire_views_kevin_2026_08/` (`p4_0.png`, `p4_1.png`), which have never had
a pass. The written comparison, plate by plate and gap by gap, is
`docs/RESEARCH/fort_dearborn_image_accuracy.md`, with the before shot from `p4_0`'s own stand.

**What shipped: the road.** `fort_road` in `data/streets/1835.json` — eleven vertices from the
east end of South Water Street, across the United States Reservation east of the garrison garden
and past the Beaubien buildings, to the fort's south gate. A 5.5 m worn-earth track inside a 12 m
corridor, drawn by the existing street layer, no bake. Before and after from the same stand:
`docs/RESEARCH/fort_road_before_2026-08-19.png` → `fort_road_after_2026-08-19.png`.

**Where the line comes from, and where it stops coming from.** The gates are attested three times
(Kinzie inside the fort in 1831, Andreas, and a break in each of exactly those two walls on the
1830 Harrison plan). The 1830 plan also draws a road: the garrison garden's own position note has
read that plate since it was written and places the plot *"west of the road"*. So a road east of
that garden arriving at that gate is bounded. **The western reach is not**: South Water Street
stops at the reservation by the 1833 order and nothing reached draws what carried on, so the
connection to the town is this project's reconstruction — `geometry_confidence: reconstructed`,
`wear_confidence: reconstructed`, so the whole road dithers out with the rest of the invented town
when a visitor turns `reconstructed` off. Recorded as **L140**. The 1835 name is descriptive;
nobody names this road.

**What the pass found and did NOT build.** The fort's own fabric is where the plates and the model
part company — flat-topped dark pickets against pale pointed ones, corner works that do not rise
above the curtain with roofs and lanterns, no gate drawn in either documented wall. All three are
archetype geometry and **need the nightly bake, which this runner cannot run**; they are tickets
now, not claims. So are the bare trodden ground round the walls, the trees `p4_0` puts east of it,
and the bank track down to the water (which waits on T-0004 grading the bank).

**The flagstaff is refused, on purpose.** `p4_0` draws one, and `data/exclusions.json` already
excludes a flagstaff as belonging to Whistler's 1808 FIRST fort — *"none of it may be borrowed for
the second fort's records"*. Retrospective plates conflate the two forts; that is why the
courthouse plate in the same set is filed as a negative reference. A tier-5 view cannot settle it.
Filed as its own ticket, with the documentary evidence that would.

**Not claimed.** `p4_1` depicts Native people, tipis and canoes. The standing constraint holds in
full: nothing of it is drawn, and the plate is reference for the setting only.

## Shipped 2026-08-19 — T-0091: the Sauganash's yard fence, and the trees behind it

**The ask.** Piece 2 of 3 of T-0043, the image-accuracy pass on the Sauganash. The YARD side of
the owner's three views, which all three agree on and none of which had been built: a
**vertical-board fence** running off to the right of the hotel and enclosing the rear yard (images
8, 9, 10 of `data/sources/assets/owner_brief_2026_08_18/README.md`), described as **tall** in image
10, with **trees standing behind it** in image 8. L136 took the FRONT of this building from the same
three plates the night before and left this half standing in the brief.

**What changed, and it is two layers.** `data/enclosures/sauganash_yard.json` is a new enclosure
record and `renderers/web/js/enclosures.js` gains a third fence type, `board`: the picket branch's
construction — posts, stringers behind, vertical stock across — at the record's own board width
(0.254 m) and a butted 6 mm gap, 1.83 m tall, on 0.14 m posts at 2.44 m centres, with one 3.66 m
gateway centred in its Market Street run. It is the first fence in this town you cannot see through,
and that is the claim: pales say garden, three rails say wagon yard, butted boards say private.

**Every coordinate is derived and one is invented.** The line leaves the hotel's own south-west
corner (101.40 / −130.60), runs south on its west wall line, turns east along a rear line and comes
back north on the east wall line of Philo Carpenter's log shop to that shop's south-east corner —
the two buildings, which stand shoulder to shoulder along the whole Lake Street frontage, closing
the fourth side themselves. **The rear line is the one invented coordinate and it is a rule**: the
segment joining the midpoints of the committed platted lot's two side lines
(`data/traces/vectors/thompson_lots.json`, `blk_lake_market` lot 0), so the yard is the front half
of the lot and the back half is left unclaimed — because Carpenter's shop stands on the same lot and
the whole of it demonstrably was not the hotel's.

**And the first placed trees in this scene.** Every other stem in the town is dealt by
`trees.js`'s planter from the land — bank distance, division, relief, the community's recorded
density — which is the right answer for a wood and cannot put a tree behind a particular fence. So
`data/flora/plantings/sauganash_yard.json` is a new record kind: a stem states its species, its
position and its height, and the renderer draws it with the same archetype the wood uses. Three
stems here — two American elms at 17.0 and 16.5 m and a cottonwood at 18.5 m — and the ECOLOGY is
not invented: species, height bands, July foliage colour and crown widths are
`data/flora/zones/z10_settled_town.json`'s three relict survivors, and the renderer **refuses any
stem whose stated height falls outside its own species' recorded band** rather than drawing it. The
pass runs after the sweep so it redeals none of the wood, and every refusal the sweep makes — river
mask, dry floor, a committed footprint — it makes here too and REPORTS rather than skips.

**What this unblocks and what it does not.** T-0074 (trees and bushes kept around the houses) is the
same question asked town-wide and should read this record's shape rather than inventing a second
one. The ground inside the fence is untreated — still the prairie sward, where image 12 shows fenced
ground reading as garden and dooryard green — and that is T-0067's, stated in the record rather than
quietly done. The fence is not a collision surface: you walk through it, as through every enclosure
in this layer.

**The gate learned the third path.** `tools/measure_planting_reach.py` banks how many `addTree` call
sites `trees.js` has, precisely so a new selection path cannot draw a species the gate would
otherwise call unselectable. There are three now, and the third selects out of a RECORD, so the gate
reads the planting files through the manifest (never by globbing) and banks what they place —
`placed` in `tools/planting_reach_baseline.json` — with an assertion exact in both directions: a
stem arriving in or leaving a yard is a line in a diff.

**Evidence.** `docs/evidence/t-0091-{before,after}.png` — Market Street at the Lake corner,
E 88 / N −114, bearing 158°, 1280×800, detail `full`: open grass behind the hotel before, a board
fence with its gateway and three crowns over it after. `docs/evidence/t-0091-close-{before,after}.png`
— the same yard from six metres, detail `light`, which is where the cost was measured.

**Cost, measured in the browser** by publishing the mirror with and without the two records:
**636 987 → 644 639 triangles**, **+7 652**, 45 draw calls unchanged (the enclosure layer is still
one call and the trees merge into the timber chunks). That is the whole layer with the entire yard
in frame.

**What this run did NOT do.** `scene detail 'light' stays inside its own ceiling` is **T-0089**,
open and pre-existing on `dev`, and it fails at **613 500 tris of 600 000** on this branch. Taking
the most generous assumption — that every one of this unit's 7 652 triangles was inside the frustum
at the station that row is measured from — `dev` still stood at **605 848**, so the branch makes a
standing breach worse and did not open it. The two mobile road-contrast rows are `dev`'s own.
**T-0060 stands:** neither half of the smoke finishes inside this runner's ten-minute per-command
ceiling, so the tail of each viewport — including `zero page errors` — went unrun here; the page was
driven separately for errors instead and reported none.

**Recorded as a liberty.** **L139** — the fence's every dimension, the gateway nobody drew, the
depth rule, and that there are three trees, where each stands and how tall it is. Tier
`reconstructed` throughout, so turning `reconstructed` off in the confidence view empties the yard.

**Skipped above it, and this is the statement `tickets/README.md` asks for.** T-0046, T-0049,
T-0004, T-0005 and T-0083 all stand above T-0091 in `QUEUE.md` and all five carry
`needs_bake: true`; this runner has no Blender and may not install one. T-0091 is the topmost
workable ticket.

## Shipped 2026-08-18 — T-0087: the wagon box rests on its running gear

**The owner's report, and the half of it T-0084 did not answer.** From the Green Tree's yard:
*"it looks like that bar is supposed to be below the carriage of the wagon holding the wheels
together but not sure. all the wagons seem off."* The bar was the tongue and T-0084 made it a pole
— but the instinct behind the sentence was a second, independent defect. `buildWagon` drew a box, two
0.05 m axle sticks and four wheels and **nothing in between**: the floor at 0.95 m, the rear axle at
0.685 m, the front at 0.535 m, so the box hovered **0.27 m over one axle and 0.42 m over the other**
and the two axles were joined to each other by nothing at all. The eye reads a missing member, goes
looking for it, and finds the tongue lying in the grass.

**What changed.** Six timbers per wagon, on all four: a **bolster** over each axle (the box rests on
these), a **reach** on the centreline tying the rear axle forward to the front gear, **two hounds**
bracketing that reach and running on past the front axle to the tongue's root, and a **kingbolt**
through bolster, hounds and axle with its nut showing below.

**Only the sections are chosen; every position is derived.** Both bolsters are the same depth,
because a bolster's job is to bring two different axle heights up to one level floor — so the larger
**rear** wheel sets that level and the front bolster reaches down to the same line, and what is left
underneath is exactly the space the hounds and the reach occupy. The reach sits on the top of the
front axle and passes under the rear one because the two recorded wheel diameters put it there.
Change `wagon_body_m` or either wheel and the gear follows. **No recorded value moved**: the wheels
(1.37 m / 1.07 m), the body (3.05 × 1.07 × 0.55 m) and the bed height (0.95 m) are L131's own
numbers, untouched — the gap was closed by drawing the members that belong in it, not by dropping
the box or shrinking the wheels.

**Cost, measured in the browser at the owner's stand.** 636 410 → **636 986 triangles**, 45 draw
calls unchanged, one draw call for the whole layer as before. Six boxes per wagon is 72 triangles of
geometry each; the frame counter reads it twice because the layer is drawn in the shadow pass too.

**Evidence.** `docs/evidence/t-0087-{before,after}.png` — the owner's stand, E −132.78 / N −99.5,
bearing 000°, 1280×800, detail full. `docs/evidence/t-0087-close-{before,after}.png` — broadside at
3.2 m from the same wagon, which is where the daylight was: before, the grass and the next wagon are
visible straight through the gap under the box; after, there is gear there.

**Recorded as a liberty.** **L138** — every one of the six timbers is invented, and the entry states
what bounds each: the six sections are free numbers, every position is arithmetic on the recorded
wheels and body. Tier `reconstructed`, so turning `reconstructed` off in the confidence view takes
the gear with the rest of the wagon.

**What this run did NOT do.** `scene detail 'light' stays inside its own ceiling` is **T-0089**, open
and pre-existing on `dev`; this branch adds 576 triangles to a breach that stood at ~605 000 of
600 000 before it, and did not open it. The mobile road-contrast rows are `dev`'s own, below.

## Shipped 2026-08-18 — T-0084: the wagon tongue is a pole at its own section

**An owner report, confirmed twice.** The ticket was opened from the code while T-0081 shipped —
`renderers/web/js/yard.js` drew the tongue as ONE horizontal box spanning the drop from the front
axle to the ground, `halfH = (rootY - tipY) / 2` ≈ 0.24 m, so a 2.75 m stick 0.055 m thick was
rendered **0.48 m deep** — and the owner reported the same object from the Green Tree's yard the
same day: *"a note about the wagons to fix, it looks like that bar is supposed to be below the
carriage of the wagon holding the wheels together but not sure. all the wagons seem off."*

**What changed.** The tongue is drawn with `pushBoxV` at its recorded section along its own
inclination, on all four wagons: a 0.055 × 0.055 m pole running from the front axle's centre down
to the grass at **10.6°**, its far end resting ON the ground rather than sunk into it (the tip's
centre sits at half the pole's vertical section, `halfT / cos θ`, one pass of the fixed point).
The recorded 2.75 m is now read as the pole's LENGTH rather than its horizontal run, which is what
the number means: the tip lands **2.70 m** ahead of the body instead of 2.75 m, inside the 4.6 m
radius the smoke measures a wagon by. The old comment's reasoning — a stick's exact inclination is
not a claim this record makes — was right about the ANGLE and was answered by the wrong geometry;
the box only had to be that deep because it was axis-aligned.

**Cost: none.** `pushBox` and `pushBoxV` are both 12 triangles, so the layer is unchanged at
636 410 triangles / 45 draw calls, and the wagon's own numbers (body, wheels, bed, tongue length)
are untouched.

**Evidence.** `docs/evidence/t-0084-{before,after}.png` — the Green Tree's yard from E −132.78 /
N −99.5, bearing 000°, 1280×800, detail full. Before: a slab in the grass that reads as a second
box come adrift. After: a pole.

**Recorded as a liberty.** L131's **Revised: 2026-08-18 (T-0084)** — the inclination is now a
claim rather than something hidden inside a slab, and what bounds it is the two ends (the recorded
front-wheel radius at the root, the ground at the tip). No new invented value.

**What this run did NOT do.** The wagon box still floats over its axles with no bolsters, reach or
hounds — the second, independent defect behind the owner's sentence, which is **T-0087** and its
own demonstration. Fixing it here would have bundled two tickets into one PR.

## Shipped 2026-08-18 — the far sward: the meadow recedes instead of ending at a radius

**T-0086, an owner report.** On the T-0035 fix he wrote: *"the plant rendering is much better! but
in certain scenes it does not look right and you can see them fade in when in long distance view
like this, would be nice if you could see them in the distance blurred faintly further out."* Two
stands, three screenshots: **South Water approaching Wells, heading 084°** and **Wells approaching
Lake, heading 185°**. Two symptoms, one cause — the flora field is a set of rings about the walker
and nothing at all was drawn past the outermost one (HIGH 27 m, LOW **13 m**).

**What a visitor sees.** A new layer, `flora-far`, draws aggregate clump cards from the detailed
rings out to **175 m** (balanced 150, light 120). At the Wells stand the grass now runs to the
houses and to the horizon where it used to stop at a line 25 m out with bare green ground beyond
it; before/after pairs from both stands are on the PR.

**Two bands, because one lattice cannot do this.** A spacing that is right at 25 m is a thousand
cards at 150 m, and one that is right at 150 m leaves a hole where the detailed rings hand over.
So a fine lattice of small clumps (16–62 m, cell 3.4 m) and a coarse lattice of wide ones
(44–175 m, cell 9.5 m), overlapping across 44–62 m where each is thinning into the other.

**IT IS NOT THE SHEET THAT WAS REVERTED.** A solid far-field vegetation mesh shipped here once and
was taken out because it hid foundations and plant roots while the visitor walked on the real
heightfield below it. Every far card is a rooted instance standing on `terrain.surfaceHeight` at a
station `station()` allows — the same building footprints, the same travelled track, the same
waterline — so there is no second land surface to walk under, and no card stands on a road, in a
building or in the river. At the South Water stand, which looks straight down a street, the band
places **131** cards and the roadway keeps none of them.

**AND IT FADES BY DENSITY, NOT BY THE DITHER — that is the second half of the report.** The
existing rings resolve their coverage ramp with a 4×4 Bayer screen door, which is invisible at
arm's length and a band of dots at fifty metres down a shallow view, because distance compresses
the whole ramp into a few screen rows (at 60 m the mid ring's 7 m band is nine pixels tall). A far
card is drawn whole or not at all; what changes with distance is HOW MANY, against a world-anchored
per-slot rank (`farRank`) and a ramp that is zero at both ends (`farKeepAt`). A stochastic density
ramp has no edge in it to dither. The inner ramp is the handover: the band thins back to nothing as
the walker closes on it, so a 3 m aggregate card is never met at arm's length.

**What it costs, measured in the browser at the South Water stand, 1280×800, detail full.** Draw
calls **44 → 45** of 80 (the band shares the mid ring's material, so no new shader program).
Triangles **634 448 → 636 410**, +1 962. Caps: 420 cards at full, 300 balanced, **190 at light**,
where the card is a 7-column archetype (14 triangles) rather than the desktop's 9 (18) — so the
light level's worst case is **+2 660 triangles**, which makes **T-0089**'s known breach of the
600 000 light ceiling worse by 0.4 % and does not open it. That number belongs on T-0089 and is
recorded there.

**What is invented, and it is recorded.** **L137**: a far card stands for GROUND, not for a plant,
and its height is drawn from the upper half of the species' recorded range and lifted 1.14×/1.20×,
because what an aggregate shows against the sky is the tallest plants in the patch and not the mean
of them. The species, the colour and the height range are the community's own compiled records,
dealt by the same call the mid ring uses. The band is deliberately **excluded from the drawn
census** — a card is not a stem, and counting one as a stem would inflate every community's matrix
count by the area of an annulus four times the size of the ring the census is about.

**What this run did NOT do.** It did not touch the near ring's own outer dither at 5–7.6 m, which
is still a screen-door ramp and is still what a close look at the verge shows; the far band stands
over the mid and forb rings' outer edges at 16–62 m, which is where the owner's screenshots show
the band, and the near ring's is a separate and smaller question. If it is still visible to him it
is a ticket, not a weakening of this one.

## Shipped 2026-08-18 — the Sauganash's frontage: plank walks on both fronts, a crossing, and two hitching posts

**T-0090, the first of the three pieces T-0043 was split into.** (Filed as T-0086/87/88 and **renumbered on the merge**: #245 landed on `dev` first and had taken 0086 and 0087 for two findings of its own, which is the collision `tickets/README.md` § IDs describes. The three kept their exact QUEUE positions — renumbering is not reordering — so the branch's own commit messages name the old numbers.) T-0043 asked for the building
corrected AND its ground present in ONE demonstration, and the building half moves the
`frame_1831` phase fields `generators/mesh_inputs.py` hashes into the committed GLB — it needs the
nightly bake, which this runner has no Blender for. So the ticket became three: this one (the
street side), **T-0091** (the board fence and the rear-yard trees) and **T-0092** (the fabric,
`needs_bake`). Both of the others hold T-0043's place in QUEUE.

**What a visitor sees.** A 1.83 m plank walk along the hotel's Lake Street front AND its Market
Street side — *"plank walks on both frontages"*, which is image 9's phrase; a 1.22 m crossing of
four boards running 15.87 m from that walk across Lake Street and 0.6 m past the far edge of the
travelled track; and **two hitching posts**, 1.30 m tall and 0.16 m square under a 0.22 m capped
head, standing 2.93 m out from the front wall at 0.28 and 0.72 of its length. All of it is
pickable and all of it opens the hotel's card. The warrant is three of the owner's reference
views, written up at `data/sources/assets/owner_brief_2026_08_18/README.md`: image 8 (Petford
1831) gives *"plank sidewalk with a board crossing over the road; two posts (hitching/corner
posts) at the road edge"*, image 9 (Braunhold) gives *"plank walks on both frontages, hitching
posts"*, image 10 (Trowbridge) ties a saddled horse to one of them.

**The horse is not drawn, and the reason is narrower than L1.** L1 is about people. Nothing in
this project models an animal at all, and a horse invented at the one post with a plate behind it
would be the most conspicuous reconstruction in the town. Stated in **L136** so it is not read as
the same rule.

**NOTHING HERE IS LETTERED, and that is a reading.** L135 letters the Green Tree's board because
image 7 states the wording. None of this hotel's three views shows a name board at all — its
posts are hitching posts — so the Sauganash keeps the blank wall board
`tools/generate_business_signboards.py` hangs on it by rule (L130), the frontage layer draws no
board here, and clause 6 of that generator is deliberately NOT extended to this building. The
record carries the argument on its own face as a `board_on_a_post` block.

**THE SECOND BUILDING FOUND A HOLE IN THE RULE, which is the best reason to run one through it.**
The walk rule asked only that a street lie OUTWARD of a wall. The Sauganash's east wall is a flank
in the middle of its block, and Lake Street's centreline — which crosses the far END of it — stood
**0.13 m outward out of 16.00 m**, enough to pass: the rule laid a plank walk down a blank flank
and called it a frontage. The rule now also asks that the street lie IN FRONT of the wall rather
than beside it — at least half the distance to it standing outward, a 60-degree cone. Every real
frontage at both buildings clears that at **0.998 or better**; the flank measured **0.008**. Two
of the Sauganash's four walls are now refused in writing, each saying which test refused it.
**The Green Tree's walks, crossing, post and refusals are unchanged to the byte** — only its
record's own description of the rule changed, because the rule did.

**One generator, a table of buildings.** T-0082 wrote "the second and the twentieth cost nothing
but a line here"; this run spent that line. What is per-building in
`tools/generate_frontage_works.py` is now the prose — which plate says what — plus two switches
the plates decide: `sign` (a named board on a post: the Green Tree yes, the Sauganash no) and
`hitching` (posts at the road edge: the Sauganash yes, the Green Tree no). Every dimension,
clearance and refusal is one shared rule. `data/frontage/index.json` is generated with the records
now instead of kept by hand — a record written and never listed is a record nobody draws, and
`--check` would have called that green.

**What the gate holds.** `tools/check.sh` re-derives both records AND the manifest byte for byte.
Three new assertions in `tools/smoke_renderer.mjs`, none relaxed, and the layer's census assertion
widened to both records: the two hitching posts measured against their own terrain samples (top
within 0.05 m of the recorded 1.30 m, foot within 0.02 m of grade, no text on either) with the
layer's lettered count still exactly one; the frontage reaching the screen from Lake Street on the
same worst≥6 / mean≥0.3 bar the Green Tree's is held to; and a pick on the layer opening
`sauganash_hotel`.

**The gate as measured, in full.** `tools/check.sh` PASSES. `node tools/smoke_renderer.mjs
--published` on the published mirror: the **mobile half ran to completion — 325 passed, 3 failed,
and `zero page errors` PASSED**; the desktop half was killed by the runner's ten-minute ceiling
(**T-0060**) at 157 passed / 3 failed, having already taken all four of this parcel's assertions.
**None of the failures is this parcel's, and each was measured rather than assumed:**

- `the roads reach the screen from the walker's eye` and `…from the air` — both already recorded
  in this file as `dev`'s own, at both viewports.
- `the panel states that once too — and counts nothing by hand` — **T-0037**, whose own body
  records the same failure on `origin/dev` at `3114e061`. Its `occurrences: 1` half is correct;
  what fires is the guard scanning the whole Evidence panel and finding K53's liberty saying
  *"Three of these records…"*.
- `scene detail 'light' stays inside its own ceiling` — **604 950 tris of 600 000**, desktop only,
  and **new to this file**: it sits at assertion 151 of a desktop half that has not finished in
  weeks. It is NOT this branch's. This parcel's entire addition to the scene was measured in the
  browser at **3 684 triangles** (the frontage layer draws 7 308: 3 624 the Green Tree's, 3 684
  the Sauganash's, separated by a bounding box — the two inns are 250 m apart), so on the most
  generous assumption for this branch — every one of them inside the frustum at that station —
  `dev` already stood at **601 266 of 600 000**. Filed as **T-0089** with the arithmetic, linked
  to **T-0056** (the detail-blind enclosure layer that eats most of the budget) and **T-0060**.
  The branch made a standing breach 0.6 % worse; it did not open it.

**Known and not fixed here, and it is the same one T-0085 filed at the Green Tree:** the flora
layer does not know a walk exists, so the sward stands up through these planks too.

## Shipped 2026-08-18 — the Green Tree's frontage: plank walks, a board crossing, a named board on a post

**T-0082, the third of the four pieces T-0042 was split into.** T-0080 shipped the yard and
T-0081 the wagon shed; this is the STREET side of the same building. **T-0083** (the building's
own fabric, `needs_bake`) is still open and holds its place in QUEUE.

**What a visitor sees.** A 1.83 m plank walk along both of the inn's street walls, its deck
0.11 m out of the mud on 55 mm boards; a 1.22 m crossing of four boards running from that walk
across Canal Street and 0.6 m past the far edge of the travelled track; and a 3.60 m post at the
Lake-and-Canal corner carrying a 1.30 × 0.55 m board, hung from a 1.55 m cross-arm, **lettered
GREEN TREE**. All of it is pickable and all of it opens the inn's card. The warrant is two of the
owner's reference views, written up at `data/sources/assets/owner_brief_2026_08_18/README.md`:
image 6 (Braunhold 1838) gives *"post-mounted hanging signboard at the corner; plank sidewalks
with board crossings"*, image 7 (Trowbridge) gives *"the hanging 'GREEN TREE' sign on its post"*.

**THE LETTERING is the one decision that was argued rather than derived**, and it is the first
lettering this renderer has ever drawn. L25 leaves the town's one documented board blank and L130
leaves twenty-four more blank, for a reason that does not reach this one: L25's subject is an
IMAGE nobody described, and this board's subject is a NAME the plate states in as many words and
`data/structures/green_tree_tavern.json` already carries. So the WORDING is graded `inferred`
against the plate and drawn; the LETTERFORM — face, size, spacing, paint colour, absence of wear
— is invented and claimed at **L135**. No other board in the town is lettered.

**The wall board is withdrawn, in writing.** `tools/generate_business_signboards.py` grew a
clause 6: a frontage that carries a named board on a post at its corner does not also get a blank
board hung on its wall by rule. The refusal and its reason are in
`data/signage/town_business_signboards.json`; the blank-board count falls from 24 to 23.

**WHERE is derived from a building AND a street**, which no layer here had done before. A wall
gets a walk only if a street centreline lies OUTWARD of it within 22 m and the walk's outer edge
still clears that street's own travelled track; the crossing runs until it is past the far edge
of that track; the post stands 2.93 m out from each of the two walls that make the corner. Two of
the inn's four walls are refused for want of a street, in writing. Every dimension is invented —
nothing in this project measures a Chicago sidewalk of 1835.

**What the gate now holds.** Seven new assertions in `tools/smoke_renderer.mjs`, none relaxed:
the census, every vertex graded `reconstructed`, the decks tying into the ground they cross
(measured: 0.012 m below grade at worst, 0.112 m of deck above it), the post standing on its own
terrain sample with the board's underside 2.78 m up, the painted name matching the record's own
wording and grade, the layer reaching the screen from Canal Street, and a pick on the layer
opening the inn. `tools/check.sh` re-derives `data/frontage/green_tree_frontage.json` byte for
byte.

**Known and not fixed here: the sward grows through the deck.** The flora layer does not know the
walk exists, so grass and forbs stand up through the planks. It is filed as its own ticket rather
than patched in this parcel.

## Shipped 2026-08-18 — the Green Tree's wagon shed, and the covered wagon under it

**T-0081, the second of the four pieces T-0042 was split into.** T-0080 shipped the yard; this
is the shed the same plate shows. **T-0082** (frontage: sign, walks, verges) and **T-0083** (the
building's own fabric, `needs_bake`) are still open and hold their place in QUEUE.

**What a visitor sees.** An open-sided wagon shed standing against the north side of the inn —
three posts, a plate, a lean-to roof falling away from the wall — with a canvas-topped farm wagon
in the bay and its tongue down on the grass outside. It is pickable and it opens the inn's card,
the same contract the wagons, the bench and the signboards keep. The warrant is the Trowbridge
drawing (`data/sources/assets/owner_brief_2026_08_18/README.md`, image 7), which shows an
open-sided wagon shed attached at the left of the house with a covered wagon under it. Neither a
shed nor a tilt existed anywhere in this renderer before.

**WHICH WALL is derived, and it is the one judgement in the parcel.** The plate's word is "left",
which describes a viewpoint rather than a building. Three committed facts pick the wall and not
one of them is the plate: the placement record puts the front on Canal and the long side on Lake,
T-0080's two wagons already stand off the rear wall, and that leaves the north side wall — the
only one of the four that is neither a street frontage nor occupied. A wagon shed is entered off
a yard rather than off a corporation street, which is the same answer a third way.

**WHAT IS NOT HONOURED, said out loud.** The plate puts the shed at a GABLE. `frame_tavern` lays
this building's ridge along its longer axis (12.19 m against 7.62 m), which puts its gables on
the front and the rear and makes the north wall an eaves wall — so this stands at the left END of
the elevation and not at a gable. Correcting the fabric to the three views is bake-gated and is
**T-0083's**; this parcel does not pre-empt it, and the shed moves if that work moves the gables.

**HOW BIG is arithmetic on numbers already in the record**: the bay is the wagon's own 3.05 m
body with 0.50 m of air at each end by the 3.20 m of ground `WAGON_CLEAR_M` gives a parked wagon;
the open eave stands 2.95 m up, 0.35 m over the 2.60 m tilt it has to cover; the plate meets the
wall 3.63 m up at 12 degrees. The lean-to's head is checked against the building's own recorded
5.0 m wall height and a shed that would stand through the clapboard is refused in writing. All of
it is `reconstructed` and claimed at **L134**, which also records what this is NOT: John Gray's
low one-storey additions at each end of the house are attributes of the BUILDING, dated three to
six years after the scene and deliberately excluded from its footprint. This does not date them.

**The layer is still one draw call.** A tilt is canvas and must not read as timber, so the yard
layer's colour moved onto the geometry — one material, `vertexColors`, two tones — rather than
growing a second mesh for one arch. The confidence view still tints it: `confidence.patch()`
inserts after `<color_fragment>`, which is where the vertex colour is multiplied in.

**The rule re-derives.** `tools/generate_yard_goods.py` grew `_green_tree_wagon_shed()` and
`tools/check.sh` re-derives `data/yard/town_trade_goods.json` byte for byte.

**Verified.** `./tools/check.sh` CHECK PASS. `node tools/check-changelog.mjs` OK, 184 entries,
latest v184. Three new smoke assertions, all green at 1280×800 on the published mirror: the shed
is a lean-to whose eave clears its tilt; nothing standing in its bay reaches through the inn's
wall (deepest −1.60 m against a −1.65 m bound), out past its eaves or up through its own roof;
and the layer carries exactly two vertex tones across exactly one mesh.

**What is NOT verified, and it is T-0060.** The full smoke did not finish either viewport inside
this runner's ten-minute command ceiling — the desktop half reached 148 passed / 1 failed (the
known `the roads reach the screen` gate, dev's own) and was killed in the road-contrast section,
which sits AFTER the yard block and BEFORE the `zero page errors` line. So the gate's own
page-error assertion did not run. It was taken separately instead, on the published mirror at
**390×780 and 1280×800**, booting to `ready`, dismissing both overlays and standing in the yard:
**zero page errors, zero failed requests, zero console errors, no yard problems**, census 4
wagons / 1 bench / 1 shed / 1 mesh at both widths. That is the assertion, taken by hand, and it
is stated here rather than implied.

## Shipped 2026-08-18 — wagons in the Green Tree's yard, and a bench at its door

**T-0080, the first of four pieces T-0042 was split into.** The parent ticket asked for an
image-accuracy pass on the Green Tree Tavern against three views, and its acceptance clause —
"the building corrected to the views AND its surroundings (sign, walks, shed, yard, verges)
present" — is more than one demonstration, so it was split rather than shipped as a
self-invented "(1/4)". The children hold its exact place in QUEUE: **T-0080** the yard (this),
**T-0081** the wagon shed, **T-0082** the frontage (sign, walks, verges), **T-0083** the
building's own fabric. T-0083 is marked `needs_bake` because every item in it moves
`green_tree_tavern__frame_1833.glb`'s inputs and the improve runner has no Blender.

**What a visitor sees.** Two farm wagons standing in the yard behind the inn and a plank bench
against its front wall, all four pickable and all four opening the inn's card. The warrant is
the Trowbridge drawing of this building (`data/sources/assets/owner_brief_2026_08_18/README.md`,
image 7), which shows exactly that.

**What is derived and what is invented, stated separately.** WHERE is derived from the committed
footprint: the wagons stand square to the rear wall, 1.00 m off it, spaced at the 3.20 m of
ground `WAGON_CLEAR_M` gives a parked wagon, laid in from the far end of that wall; the bench
stands against the front wall 0.50 m in from the +u end, which is the end the barrels do not pile
at and the end the signboard's own rule leaves at ground level. WHAT is invented is the yard's
depth (taken as the building's own front width, 7.62 m — nothing measures it), the count (two,
because that width holds two), and the bench's size. All of it is `reconstructed` and claimed at
**L133**, which also records that it contradicts L131's own sentence about what could put a
second wagon in this town — that bar counted texts and not pictures, and it was too high.

**The people are missing on purpose.** The plate's bench is a bench of *sitters*. AGENTS.md's
standing constraint is not relaxed by a picture and v1 ships no human figures at all, so the
bench is drawn and nobody is on it.

**The rule re-derives.** `tools/generate_yard_goods.py` grew a `build_green_tree_yard()` and
`tools/check.sh` re-derives `data/yard/town_trade_goods.json` byte for byte, so "which yard gets
a wagon" stays auditable. A stand that came out inside another committed wall would be refused in
writing rather than nudged; none did here (nearest wall 27.8 m).

**Not done, and it belongs to the siblings**: the open-sided wagon shed with its covered wagon
(T-0081), the named signboard on its post, the plank walks, the verges and the fence-line brush
(T-0082), and the building's own bays, chimneys and low left wing (T-0083, needs the bake).

**A finding about the queue, recorded rather than acted on.** T-0005 (the three Main Branch
sloughs) carries `needs_bake: false` and cannot in fact go green on a Blender-free runner: any
new centreline in `data/terrain/epochs/<e>/hydrology.geojson` changes
`generators/terrain_inputs.py`'s prose-stripped input document, which is
`assets/manifest.json`'s `inputs_sha256` for `terrain__e1834_harbor_cut.glb`, so the staleness
gate refuses the commit until the ground is rebuilt. Its front matter is corrected in this PR.
T-0046, T-0049 and T-0004 above it in QUEUE were already marked `needs_bake`. QUEUE's order is
untouched.

## Shipped 2026-08-18 — plants fade in instead of growing out of the ground

**T-0035, an owner report of 2026-08-17:** *"the flowers still seem like they grow out of the ground
as you approach them, they do not fade in as you walk towards, they grow up."* **"Still" is the
finding.** This is his second report on the same ring; the first was answered by making the ramp
smoother rather than by taking it off the geometry, and a smooth growth is still a growth.

**The ring ramp is coverage now, not height.** `renderers/web/js/flora.js` hands it to the fragment
shader and resolves it with the ordered 4x4 Bayer screen-door dither the confidence view already
uses on an unevidenced wall — so a plant stands at the height its record gives it from the first
frame it is drawn at all, and what changes with distance is how much of it is written. Outside the
ring it collapses to a point rather than rasterising a full-size plant to discard every fragment,
and each plant offsets its dither threshold by a hash of its own world position so sixteen dither
levels against a ramp in distance do not read as sixteen rings about the walker.

**What is measured, on the published mirror at 390x780:**

| reading | before | after |
|---|---|---|
| shortest drawn plant over a 3 m walk | 0.02 % of its own height | **100.0 %** |
| height gained by a plant already on screen, per 0.15 m pace | up to the ramp's own slope | **0.0 %** |
| arrivals over the same walk / worst arrival coverage | — | 53 / **0.0 %** |
| draw calls · triangles | 41 · 611,823 | **41 · 611,823** |

**What is NOT measured, and it is the honest limit of this.** The gate reads the instance buffers
and the module's own statement of what the vertex program does with them (`flora.js` § `heightOf`),
not the pixels. That is the same footing every other flora gate in this suite stands on — `fadeAt`
has been the shared mirror since the ring was built — and it is load-bearing here rather than
decorative: `tools/measure_head_support.mjs` and the smoke's R-BUG7 gate scale a plant's top and a
stalk's foot by the same mirror, so a height ramp reintroduced without changing it breaks them.
**What no gate here can tell you is whether the stipple LOOKS like a fade**, which is an owner
check from spawn.

**R-BUG7 survives simpler.** The world-space head descent — a flower head sliding down its own stalk
to stay on a shrinking plant — is deleted with the scale it existed to chase. `maybeHead`'s clamp
gives `foot <= plantH` and nothing scales either side of it now; the smoke's every-drawn-head gate
is unchanged in what it asserts and green.

## Shipped 2026-08-18 — the front screen counts the town

**T-0036, an owner ask of 2026-08-17:** *"on the front (gate) screen, show the number of buildings
in the city and the population — people living in their buildings"*, and the population *"should
get to the correct Chicago 1835 population number as the buildings all complete."*

**Both numbers already existed; nothing here is an invention.** The gate now shows **322 buildings
standing of the 665 the town held** and **142 people housed of roughly 3,265**, counted at page
load out of `data/town_census.json` — a new derived record written by `tools/town_census.py` and
re-derived by `tools/check.sh`.

* **Buildings** is the 665-roof programme's own standing count
  (`data/reconstruction/1835_665_roof_programme.json` → `standing.physical_roofs.min`), so it is
  ROOFS and not records: a bridge, a pier, the fort palisade and the parade ground are structure
  records that are not buildings, and where one record reads as two or three cabins the ledger's
  low reading is taken here too. The two figures cannot disagree because there is only one of them.
* **People** is `data/residents/` joined through `lives_at`: a person counts when the building they
  live in resolves into the scene (`data/sidecars/1835/index.json`, which is what the renderer
  actually loads). 121 of the layer's 173 households live in a building that stands; the other 52
  have no dwelling record yet and are the headroom the ask is about. So the number grows as the
  town builds out, **by construction** — which is exactly what *"should get to the correct number
  as the buildings all complete"* asks for, and it is not a progress bar somebody animates.

**Both denominators are on the card, because neither figure is a total.** 322 alone reads as a
town; it is a progress report on one still being built.

**What the second number is NOT, and the card says the softer half of this out loud.** `housed`
counts PERSON ENTRIES, and three of the entries it counts stand for a group a source counts
without naming — *"the rest of the Beaubien household, unnamed"*, *"Heacock's wife and children"*,
*"the rest of the Robinson household"*. Each is at least one person and probably several, so the
figure is a **floor** on the people this dataset houses and never a population estimate;
`group_entries: 3` in the census carries the seam. The town's own total is quoted as the town's:
3,265 people in 398 dwellings is the census of **November** 1835 (Andreas vol. 1, printed p. 180),
four months after the scene date, which is why the card says *"roughly"* — the honesty note in the
ticket, honoured rather than rounded off.

**Why a derived file rather than a constant in the page.** The `build.json` lesson, on the most
visible surface there is: a number written once by hand goes stale silently. `tools/check.sh` now
re-derives the census, so a run that builds ten roofs and does not regenerate it fails at the
commit instead of shipping a town that says it is smaller than it is. The same step refuses a
household whose `lives_at` names a structure the scene does not carry, which would otherwise drop
people out of the count without a word.

**Files.** `tools/town_census.py` (new, derived + `--check`) · `data/town_census.json` (new,
derived) · `renderers/web/js/census.js` (new — every figure AND every denominator read from the
census, fail-soft to a hidden row) · `renderers/web/index.html` (an empty container, so there is
no numeral in the markup to go stale) · `renderers/web/css/walk.css` · `renderers/web/js/main.js`
(fetched beside the scene load, awaited before `ready`, exposed as `api.census`) ·
`tools/check.sh` · `tools/publish.sh` + `tools/check_published.mjs` COPIES row ·
`tools/smoke_renderer.mjs` (three assertions).

**The gate, measured.** `tools/check.sh` — the dev gate — **passes**, including the new
re-derivation step (it caught the missing mirror row on its first run, which is what that gate is
for). `node tools/smoke_renderer.mjs --published` was run on the **published mirror at both
release viewports**, and **all three new assertions pass at 390×780 AND 1280×800** — they read the
numerals back out of the rendered DOM and compare them to the JSON the page fetched, so a stale
gate screen fails rather than merely looking plausible. Neither half ran to completion: this
runner's **ten-minute per-command ceiling** (ROADMAP § THE RUN BUDGET) killed the mobile half at
**208 passed / 2 failed** and the desktop half at **143 passed / 0 failed**. The two mobile
failures are `the roads reach the screen from the walker's eye` and `…from the air`, **both
already recorded in this file as `dev`'s own** and neither touched by this branch. Because the
smoke's zero-page-errors assertion is the last line of each viewport and neither tail ran, that
question was answered separately and in the foreground: a scratch harness booted the published
gate at both viewports, asserted the rendered numerals against `data/town_census.json`, and
collected every page error, console error and HTTP ≥ 400 — **both viewports PASS, zero page
errors**. The scratch file is not committed; the durable assertions are the three in the smoke.

## Shipped 2026-08-18 — the two river warehouses have their docks

**T-0041 (piece 4 of 4 of T-0003, legacy K5 (e)).** `docs/ROADMAP.md` K5 (e) asks for
*"docks/wharves at the forwarding houses (attested 'with its dock along the river front')"*. It is
the last clause of that box and the one that had been owed longest:

* **Two records state a dock and both state it in the same sentence.**
  docs/research/03-structures-north.md §3.10 — *"Kinzie & Hunter and Dole & Newberry each had a
  warehouse WITH ITS DOCK ALONG THE RIVER FRONT"* — which is the clause that attests the Kinzie &
  Hunter building at all; and Andreas independently names *"Newberry & Dole's wharf"* as the place
  the schooner *Illinois*, the first vessel through the new cut, was cheered on 12 July 1834
  (scan p. 503).
* **Both carried `geometry: "absent"` over it**, so the strongest confidence chip in the dataset
  stood in front of a bare bank. `docs/LIBERTIES.md` **L66** recorded that as owed in 2026-08-11 and
  named the reason it had not been paid: *"this project has a `pier_crib` archetype for the harbour
  piers and nothing for a river wharf"*. That reason is a BAKE reason, and AGENTS.md
  § RECONSTRUCTED IS A TIER is the answer to it — the renderer-side half needs no Blender, which is
  the same argument that already carries the fences, the boards and the goods.

**What shipped.** `data/wharves/` (manifest + one generated record),
`renderers/web/js/wharves.js` (one draw call, its own program cache key, every vertex graded
`reconstructed`, pickable to the warehouse behind it), `tools/generate_river_wharves.py`, a
`tools/check.sh` step that re-derives the record byte for byte, a `tools/publish.sh` copy rule and
its `check_published.mjs` COPIES row, and a `newberry_dole_wharf` viewpoint in the Go-to tab.
**Two wharves, 26 crib bents, 1,224 vertices.** Both `dock` attributes move from
`geometry: "absent"` to `geometry: "simplified"`, which is the exact claim: a reconstructed wharf
of standard form stands in the place of the attribute, and the attribute's own value — *true* — is
all of it that comes from evidence.

**THE RULE, which is the answer to "why these two".** A sidecar standing on the scene date whose
own `dock` attribute is true and graded `attested` or `inferred` — the last clause refusing a wharf
drawn on a *reconstructed* dock, which would be an invention resting on an invention. Run over the
whole town it selects exactly two records and refuses every other river frontage in the dataset:
the South Water stores, the lumber landing, the ferry. Nothing else here says it had a dock.

**WHAT IS DERIVED AND WHAT IS INVENTED**, because the split is the point of the layer:

* **Derived, with no free numbers at all.** The wall each wharf serves is the committed footprint's
  own max-`v` edge through `docs/GLB-CONTRACT.md`'s frame (the same three lines
  `generate_business_signboards.py` composes). Where it stands is the traced 1834 bank line, nearest
  point to the middle of that wall, and the deck runs along the BANK's own tangent — which differs
  from square-to-the-building by about 20° at both sites. The clearance to the wall it serves
  (5.93 m and 6.33 m) and the depth at its face are measured, not assumed.
* **Invented, every one of them in `form` with its bound stated and claimed at L132.** The face
  6.0 m beyond the traced line, the heel 2.0 m back into the bank, the 3.0 m apron past the
  building each way, the 0.14 m plank, the 0.90 m freeboard floor, the 1.20 m crib and the three
  snubbing posts.
* **The deck's HEIGHT is neither.** It is the ground's own height along the landward edge, sampled
  from the terrain at load — T-0001's finding about the bridge deck, where a height authored beside
  the mesh instead of taken from it put a walker 1.8 m over the planks. At both of these sites the
  bank is lower than the freeboard floor, so both decks hold **0.90 m** over the water plane.

**Measured.** Depth at the face, off the committed heightfield: **1.28–1.32 m** at Newberry &
Dole's, **1.14–1.29 m** at Kinzie & Hunter's. That is water for a lighter or a scow and not for a
loaded lake schooner, and the record carries it as `depth_at_face_m` so what the invented reach
implies is on the record rather than in somebody's head. Layer **1,224 vertices in one draw call**.
Every deck's heel corners stand on dry ground and every face corner over water, asserted in the
smoke against the terrain the browser loaded rather than the heightfield the generator read.

**Not claimed.** That either dock was this size, this shape or this construction — the confidence
view takes both wharves down and leaves the bare banks the sources leave. **Neither deck is a walk
surface**: `walkHeight()` keeps its wading barrier over the water, so a visitor sees a wharf from
the bank and cannot walk out along one, which is filed as its own ticket rather than half-built
here. **No vessel, cargo, crane, gangway or name is drawn** — nothing this project holds describes
any vessel in Chicago at the scene date, and a hull would be a larger invention than the deck it
would lie at. **The bank each warehouse stands on is still disputed or unattested** (L66, open):
if either building is on the wrong side of the river, its wharf is on the wrong side with it.
Nothing here is baked, and the generator half — a river-wharf mode of `pier_crib`, so a baked town
carries its own docks — is still owed.

**The gate, measured.** `tools/check.sh` — the dev gate — passes, including the new step that
re-derives the record byte for byte. `node tools/smoke_renderer.mjs --published` was run on the
**published mirror at both release viewports**, and **all eight new assertions pass at 390×780 AND
1280×800**. The mobile half ran to completion: **304 passed, 3 failed, zero page errors**. **All
three failures are `dev`'s own and none is this parcel's**: `the roads reach the screen from the
walker's eye, down an open street` and `…from the air, at the aerial anchor`, both recorded as
dev's own failures in this file already; and `the panel states that once too — and counts nothing
by hand`, which is **T-0037** — an open ticket whose own body records that T-0001's run measured
the same failure on `origin/dev` before merging, because the guard scans the whole Evidence panel
and a liberty containing the words *"Three of these"* trips it. That liberty predates this branch
(`git diff docs/LIBERTIES.md` contains no such phrase). The desktop half runs past this runner's
ten-minute per-command ceiling (ROADMAP § THE RUN BUDGET), so its tail did not run in this unit:
it reached **140 passed, 2 failed** — the same two road gates — and everything this parcel adds is
inside what it did run.

## Shipped 2026-08-18 — barrels and cases at twenty-six doors, and the town's one wagon

**T-0040 (piece 3 of 4 of T-0003, legacy K5 (c)).** `docs/ROADMAP.md` K5 (c) asks for *"yard
objects: wagons/drays (documented mired on Lake St), woodpiles and lumber stacks (Ordinance 9
documents timber, stone, brick, boxes, barrels IN the streets), crates and barrels at the
stores"*. **Unlike the signboards one layer over, this clause does not start from silence** —
which is the whole reason it was worth taking:

* **The evidence is an ORDINANCE.** `data/sources/chicago_democrat_1833_11_26.json` (tier 1,
  verified from the scan) carries the village ordinances of 7 November 1833 complete, and
  **Ordinance 9 is about timber, stone, brick, boxes and barrels stacked in the streets**. A
  corporation does not legislate against a thing nobody does. That is a contemporary statement,
  by the people who had to walk round them, that this town's streets had goods standing in them.
* **What it does not give is a single address**, and it is twenty months before the scene date.
  So the FACT is well founded and WHICH DOOR is a rule — the shape T-0052 and T-0039 already use.
* **The roadmap's own wagon citation does not resolve.** K5 (c) offers *"wagons/drays (documented
  mired on Lake St)"* and **this project holds no source record for it**. It is struck from the
  argument rather than repeated, and refused in writing on the record.

**What shipped.** `data/yard/` (manifest + one generated record), `renderers/web/js/yard.js`
(one draw call, own program cache key, every vertex graded `reconstructed`, pickable to the
business behind it), `tools/generate_yard_goods.py`, a `tools/check.sh` step that re-derives the
record byte for byte, a `tools/publish.sh` copy rule and its `check_published.mjs` COPIES row.
**149 objects on 26 frontages** — 102 upright casks, 46 packing cases, and one empty laid on its
side outside each public house with the wall for it — plus **one wagon**. **3 frontages are
refused in writing**: the fort's provision store and the sutler's store (federal ground inside a
palisade, no corporation street in front of the door) and the reconstructed west-side grocery (an
anonymous slot).

**THE ONE WAGON.** No source here puts a wagon at any place in Chicago on any day; one place is
NAMED for them, `chicagology_prefire278`'s *"the yard into which the trains were driven"* — the
attestation behind `data/enclosures/western_hotel_wagon_yard.json` (L127). The wagon stands in
that yard and nowhere else, at a point **searched rather than chosen**: a 0.25 m lattice over the
yard's own bounding box, keeping the stand whose least clearance to every committed wall and
every fence line is greatest, **8.39 m** here.

**What is invented** — `docs/LIBERTIES.md` **L131**: the fact of goods at those particular doors
on that particular day, the count at each, and the objects' own sizes. **No barrel carries a
brand, a merchant's name, a stencil or a mark, and no case is labelled** (L25 generalised again).

**Measured.** Layer **7,160 triangles**, of which the wagon is 896 — **1.1 %** of the 627,811 the
scene draws and 0.72 % of the 1,000,000 ceiling — in **one** draw call (40 of a budget of 80 on
mobile, 41 on desktop). Worst vertex **0.64 m** from its own object's anchor; deepest **0.36 m**
back from an anchor, so **0.19 m clear of the facade plane** everywhere. Zero page errors at both
release viewports.

**Not claimed.** That any of these particular buildings had anything outside its door — the
confidence view takes all 149 down. **Ordinance 9's timber, stone and brick are not drawn at
all**: they are building material on a lot under construction rather than a merchant's stock on
his own frontage, and this record cannot say which lot. **Nothing stands in a roadway**, though
the roadway is what the ordinance is about — the restrained reading was chosen deliberately,
because a cask in the travelled way is a claim about the width of the road as well as about the
goods. Nothing here is baked. And **the full smoke does not fit this runner's ten-minute
per-command ceiling** (ROADMAP § THE RUN BUDGET): both halves were run on the published mirror
and every one of the nine new assertions passed at **both** 390x780 and 1280x800, but each half
was killed by the ceiling after 214 (mobile) and 132 (desktop) passes, so the tails of both
halves did not run in this unit.

## Shipped 2026-08-18 — two dozen shop signs, in a town that documents one

**T-0039 (piece 2 of 4 of T-0003, legacy K5 (b)).** `docs/ROADMAP.md` K5 (b) asked for
*"signboards on businesses — attested (the Green Tree plate's hanging sign; the wolf sign
documented) — parameter exists in `frame_storefront`, switch it on per record, lettering stays
undrawn (L25)"*. Worked strictly, that clause was already finished, and this is the finding the
ticket turned up:

* **Exactly ONE structure record in this dataset attests a sign** — `wolf_point_tavern`
  `form.sign`, the painted wolf, and it has hung in that building's GLB since the archetype grew
  a `sign` parameter. Nothing else in 332 records carries the attribute.
* **The Green Tree plate is NOT SEEN.** `data/sources/chm_green_tree_1859.json` says so itself:
  the image could not be retrieved, the identification comes from aggregator metadata rather than
  the holding institution, and `verified` is false. The hanging sign K5 (b) cites it for is not
  evidence this project holds. It is struck from the argument rather than repeated, and the
  roadmap box now says so.
* **The archetype route needs a bake.** `frame_storefront`'s `sign` parameter is Blender's, and
  there is no Blender on the improve runner. So switching it on per record would have shipped
  nothing visible.

So the boards are a `reconstructed` layer instead, on the enclosure layer's own argument: a
signboard is a plank on a bracket hanging off a wall this project has already drawn, its position
is arithmetic on the committed footprint and placement, and it therefore needs no bake.

**What shipped.** `data/signage/` (manifest + one generated record),
`renderers/web/js/signage.js` (one draw call, own program cache key, every vertex graded
`reconstructed`, pickable to the business behind it), `tools/generate_business_signboards.py`,
and a `tools/check.sh` step that re-derives the record byte for byte. **24 boards**, chosen by a
rule and not a list: a named record, a PUBLIC TRADE whose customer arrived on foot off the street,
that trade `attested` or `inferred` rather than `reconstructed`, standing on the scene date, and
no sign on the record already. **4 frontages are refused in writing** — Frederick Thomas's shop
(its own record says no source reached says what he sold), the reconstructed grocery and the
reconstructed physician's office (anonymous slots), and the Wolf Point Tavern (it already has the
only real board in the town).

**What is invented, and it is one thing.** The FACT of a board on those 24 frontages —
`docs/LIBERTIES.md` **L130**. The board's geometry is not new invention: arm, board and hangers
are `generators/archetypes/log_dwelling.py::_sign`'s own numbers, so the town has one convention
for hanging a board rather than two. **No board carries lettering, an image or a trade device**,
which is L25 generalised: no source gives the wording, device or colour of a single Chicago sign
of these years, the wolf's included.

**Not claimed.** That any of these particular buildings hung a board — the confidence view takes
all 24 down. That the trade list is the only defensible one: warehouses, packing houses, smithies,
cooperages, tanneries, brickyards, manufactories and stables are excluded on a judgement about
whose custom arrived on foot, and that judgement is recorded in the generator and in L130 rather
than derived from a source. And nothing here is baked, so a scene wanting these boards as solid
timber still needs the generator half of K5 (b).


## Shipped 2026-08-18 — fenced gardens behind eighteen of the town's houses

**T-0052 (piece 3 of 3 of T-0038, legacy K5).** The Kinzie-view plate shows *"picket-fenced garden
plots and Lombardy poplars"*, and `docs/ROADMAP.md` K5 (a) cites it in exactly those terms while
excluding the house itself from the 1835 scene. So the evidence here is a TREATMENT and not a
location — the ticket says so in its own body, and calls that "the whole difficulty". This run
answered it with a rule instead of a list.

**What shipped.** `data/enclosures/town_dooryard_pickets.json` — 18 picket-fenced garden plots on
platted house lots, generated by `tools/generate_dooryard_pickets.py` and re-derived byte for byte
by `tools/check.sh`. The fence is 1.22 m high, pales 0.089 m wide with a 0.089 m gap on two
stringers, 0.10 m posts at 2.44 m, with a 1.07 m gap in the side that faces the house. The plots are
up to 8.53 × 6.10 m, set 3.05 m or more behind the house's own back face and 0.91 m inside the lot
lines. `renderers/web/js/enclosures.js` learned the `picket` fence type: the same posts and
stringers, closed with vertical pales at the record's own pale width and gap.

**The rule, which is the answer to "why this lot".** A platted lot in
`data/traces/vectors/thompson_lots.json`, holding exactly ONE committed building, that building a
dwelling by both archetype and function, with a household recorded as living in it, and room at the
back for a plot that hits no other footprint. Every clause refuses something real: the Mansion
House, Eliza Chappel's infant school and the Temple Building each sit alone on a platted lot and are
not house lots; John Wright's two buildings to let are refused because their own records say *"the
honest reading of 'to let' is a building whose tenant this project cannot name"*; and five lots are
refused **in the record itself**, with the reason, because the committed house already stands at the
rear of its lot — one of them 7.40 m past its own rear line.

**Nothing here is hand-placed.** Every corner of every perimeter comes from the committed lot polygon
and the committed footprint, which is what makes 18 garden fences auditable rather than 18 numbers
somebody typed.

**What is NOT done, stated plainly.**

1. **The ground inside the fences is not drawn.** A kitchen garden is beds and bare earth; it is
   prairie sward here, because nothing states what was grown on any lot in this town. Same residual
   as the wagon yard and the pound.
2. **The plate is not held as a source record.** It reaches this repository only as an owner-supplied
   reference image with a README, so `existence.sources` on the record is deliberately EMPTY and the
   citation is a committed path. Filed as **T-0055**.
3. **The layer is not detail-aware.** A paled fence is thousands of very small boxes and this layer
   draws them at every scene-detail level, so the `light` ceiling — the tightest of the three — pays
   the full cost. Measured on the published mirror at 1280 × 800: `light` **565 206 / 600 000** after
   this change against **597 486** at the first cut, which is why a pale skips its buried underside
   and the plot is capped at 28 × 20 ft. Filed as **T-0056**.
4. **The fences are invented end to end** and claimed at **L129** — the treatment, the height, the
   pale rhythm, the plot size, its position and the gateway. Turn `reconstructed` off and all
   eighteen disappear.
5. **Only the platted grid can carry this.** The town's house lots in the West Division approaches,
   on the reservation and in the North Division have no lot geometry to derive a plot from, because
   the plat grid covers 19 of the plat's 58 blocks (§ S9 still records the North Division street
   control as owed).

## Shipped 2026-08-18 — the estray pen is a fence, and its roof is retired

**T-0051 (piece 2 of 3 of T-0038, legacy K5).** Chicago's first public building is a pound, and
Andreas says what it was in one clause: *"the 'pen' was a small wooden enclosure and quite
roofless."* From 2026-08-11 to today the model drew it as a log box with a shed roof, because
`outbuilding` — the only archetype that would build a low walled rectangle — cannot build a roofless
one. **L60** admitted exactly that and named the fix. T-0050 built the layer; this run moved the pen
onto it.

**What shipped.** `data/enclosures/estray_pen.json` — the structure record's own 9.144 × 6.096 m
rectangle re-expressed as a closed perimeter, drawn as a post-and-rail fence 1.83 m high, five
courses, 0.18 m posts at 2.44 m, with a 1.35 m gateway centred in the north side and no leaf hung in
it. Not one coordinate is new: the outline is the committed footprint, and the gateway keeps the
retired mesh's own clear width and its north-side convention so that this run changes the ROOF and
not a set of numbers restated in passing.

**What "retired rather than re-graded" meant in practice.** The five form values that made the box —
`construction`, `roof_type`, `roof_pitch_deg`, `wall_height_m`, `door` — are gone from
`data/structures/estray_pen.json`, and `assets/gltf/estray_pen__pen_1833.glb` and its two manifest
entries are deleted with them. The record stays: it is still the evidence record, still the card a
visitor opens, still the permit on the reserved ground of the public square.

**The mechanism, because a record with no mesh needed one.** A phase may now declare
`drawn_by: { layer, record, note }`. `tools/validate.py` gains `check_drawn_by()`, which asserts the
named record exists, names the structure back, is listed in the layer's own manifest, has **no GLB
and no manifest entry left behind it**, and that the phase's `form` is empty — a retired invention
left sitting in a record would keep showing on the card with a confidence chip and nothing behind
it. `tools/compile_scene.py` writes `asset: null` and carries `drawn_by` into the sidecar;
`scene-loader.js` loads the record without fetching a GLB; `walker.js` takes no obstruction from its
footprint, so the retired box leaves no invisible wall on the square.

**And the card is still reachable.** Picking used to come free with a roof to click on. `main.js`
now resolves a pick against the enclosure layer too, and `enclosures.js` banks each record's triangle
range so a hit resolves back to `structure_id`; `frame('estray_pen')` uses the perimeter's own centre
and height instead of a corner and an assumed 5 m wall. An enclosure with no structure behind it —
the wagon yard — answers nothing and the aim falls through, as before.

**What is NOT done, stated plainly.**

1. **The ground inside the pound is still prairie sward.** A pound's yard was not sward; nothing
   states what it was, so it is left rather than guessed. Same residual as the wagon yard.
2. **No gate leaf is hung**, because nothing describes one. The gateway is a gap.
3. **The generator half of L60 is still open.** `palisade` still builds no enclosure form, so the pen
   is drawn at load and is not baked with the rest of the town.
4. **The fence is invented end to end** — material, height, courses, posts, gateway — and is claimed
   at **L128**. L60 moves to **Resolved** and keeps covering the footprint, which is as invented as
   it ever was.

**Gates.** `./tools/check.sh` CHECK PASS. `node tools/smoke_renderer.mjs --published` gained four
assertions for this — the pen draws on the enclosure layer and bakes no mesh, the retired box leaves
no invisible wall, the pen reaches the screen from inside the pen, and aiming at the fence still
opens the pen's card — and all four pass at **390 × 780** and at **1280 × 800**. Each viewport pass
was cut short by this runner's 10-minute per-command ceiling (mobile reached 196 assertions, desktop
114); the only failures in either span are the two pre-existing road-legibility rows, both marked
*(reported only)* and not gated.

**Found on the way, filed rather than fixed:** every liberty appended to `docs/LIBERTIES.md` since
**L111** has landed physically below the `## Resolved` heading, so seventeen standing liberties —
including L127, written yesterday — compile as `resolved` and are exempt from the coverage gate.
L128 was placed in the per-subject section deliberately. Filed as its own ticket.

## Shipped 2026-08-18 — the Western Hotel's wagon yard, and the first enclosure this project can draw

**T-0038 (piece 1 of 4 of T-0003, legacy K5).** `docs/LIBERTIES.md` **L10** and **L60** have been
waiting on the same missing thing since 2026-08-09 and 2026-08-11, and both name it in the same
words: *"an enclosure archetype — post-and-rail or notched log, ROOFLESS, gated, taking a perimeter
rather than a footprint."* Without it the Western Hotel's yard — the thing the west-side teamsters'
house actually WAS to anybody who used it — was left out of the model entirely, and Chicago's first
public building, a pound, is drawn as a roofed shed because the only archetype that would take a low
walled rectangle cannot build a roofless one.

**What shipped is the renderer half of that archetype, and it needs no bake.** An enclosure carries
a polyline, a fence type, a height and its gateways, so `renderers/web/js/enclosures.js` builds it
at load from `data/enclosures/` the way `streets.js` builds a wagon track — no GLB, no `assets/`,
nothing for the nightly. The whole layer is **one draw call**; the fence drapes on
`terrain.surfaceHeight()` at every post and refuses a post whose foot is in the river mask; every
vertex carries `_confidence`, so hiding `reconstructed` removes the fence and leaves the ground the
sources leave.

**The population is one record and it is the attested one.** `western_hotel_wagon_yard` — 23 posts,
two runs, two gateways — off one clause: *"In the rear was the large stable and the yard into which
the trains were driven. There were entrances to the yard from both streets."*

**Three things this run had to be honest about.**

1. **The outline is mostly derived and the fence is entirely invented, and those are different
   grades.** The west line is the hotel's own west wall carried south, the south line is the
   stable's north face, both off committed sidecar coordinates; the east line is the single free
   coordinate and is set by the Randolph gateway rather than picked, because the hotel stands on the
   corner and a yard behind it can reach Randolph only by a neck past its east gable. The fence
   type, height, courses, post rhythm and section are invented outright and are claimed in **L127**.
2. **The ground inside the yard is not drawn, and is the larger residual.** A yard that took wagon
   trains daily was not prairie sward and it is still prairie sward here, because nothing states
   whether it was worn earth, gravel, plank or mud. Left standing rather than guessed.
3. **A latent renderer trap was found by walking into it, and it cost most of the run.** The first
   build drew a perfectly correct fence in SOLID BLACK at both viewports, in full sun, with no page
   error and no shader warning. three caches a compiled program under a key ending in
   `material.customProgramCacheKey()`, whose default is `onBeforeCompile.toString()` — the hook's
   SOURCE TEXT, not the closure. Every material `confidence.patch()` touches therefore reports the
   same key, so a plain patched `MeshStandardMaterial` is parameter-for-parameter the twin of a
   mapless building material out of `buildings.js` and was handed that layer's program, which reads
   per-vertex `_roughness` and facade-tone attributes this geometry never bound. Unpatching the
   material lit it perfectly, which is exactly what made the cause hard to see. Fixed here with the
   layer's own cache key; **the general trap is not fixed and is filed as its own ticket** — any
   future layer that patches a plain lit material walks into the same collision.

**What this does NOT do.** `western_hotel_stable.stable_1834.form.wagon_yard` still declares
`geometry: "absent"` and still belongs to L10: that declaration is about the outbuilding archetype's
mesh, which contains no yard and never will. The estray pen is still a roofed box, Clybourn's
stockyard is still unbuilt, and the pig pens the November 1833 town code implies still have nowhere
to go. All three are now buildable on this layer and none is built here.

**Verification.** `tools/check.sh` green. `tools/smoke_renderer.mjs` gained five assertions for the
layer — it draws its records, it is one draw call, every vertex is graded, no member stands outside
its own authored run, and the fence CHANGES THE FRAME from inside the yard — and all five pass at
390×780 and at 1280×800.

## Shipped 2026-08-17 — no two buildings in the town are drawn the same colour

**T-0048 (the tone half of T-0002, legacy K4).** The owner's report was that the buildings "read as
freshly painted and identical", and the second half of that was exact rather than
impressionistic: a wall took its colour from its ARCHETYPE, so two neighbours built to the
same pattern were the same brown to the last decimal. Measured on the shipped mirror before
the change: of 321 nearest-neighbour pairs within 60 m, **10 were drawn identically to the
bit**. None are now, and the town draws **331 distinct facade tones across 331 structures**.

**What it is, in this project's own vocabulary: reconstructed.** No source this repository
holds states the colour of any wall in 1835 Chicago, and the dataset agrees — `paint` is
`reconstructed` on 236 of 335 records, `inferred` on 15, **`attested` on exactly two**. So
`renderers/web/js/facades.js` invents within a stated bound and `docs/LIBERTIES.md` **L126**
records the bound: silvering that grows with the record's own age (at most 0.35 toward the
surface's own luminance and 0.10 of darkening, reached at 12 years, half-rate on whitewash,
none on masonry) and a per-building jitter of ±16 % of value and ±7 % of warmth, dealt from a
hash of the record's id. The jitter's ceiling is the only bound taken from something already
committed: the archetypes themselves put ~30 % of value between an unpainted wall and an
outbuilding's board, so no building is tinted to a shade the generators could not have baked.

**The two records a source speaks for are untouched, and that is asserted rather than
intended.** The Sauganash's documented white and St Mary's attested unpainted are handed the
identity tone; the smoke winds the tone off and asserts their drawn colour does not move by a
bit. 45 structures are old enough to silver; the fort's, at 19 years, is the greyest thing in
the scene.

**Three things this run had to be honest about.**

1. **The age input is not an age for most of the town.** `documented_range.from` is a
   construction date for the well-attested buildings and a SCENE-PROGRAMME date for the 262
   anonymous infill records, so those compute an age near zero and are drawn unsilvered. That
   is the absence of a claim, not a claim that they are new, and inventing ages for them would
   be a second reconstruction stacked on the first.
2. **The first shipped magnitude was too small to see, and the frames said so.** At ±10 % of
   value the before/after photographs at `lake_market` and `from_above` were hard to tell
   apart while every instrument read green — 331 tones, no two neighbours alike. The
   acceptance clause is written about what a visitor sees, so the bound was raised to ±16 %
   and re-measured rather than declared.
3. **The acceptance clause's own station stands in front of a building the rule exempts.**
   `lake_market` looks at the Sauganash, which is one of the two attested-paint records, so
   that frame moves least of all — the variation is behind it. Stated here rather than
   averaged away.

**Verification.** `tools/check.sh` green; `tools/measure_facade_variety.mjs` on the published
mirror (the numbers above); the mobile half of `tools/smoke_renderer.mjs --published` green,
with four new assertions — the census, the no-identical-neighbours invariant, the inertness of
the attested pair, and the liveness pair (winding the tone off moves the worst 48² cell by 10
and restores to a residual of 0). The desktop half does not fit this runner's ten-minute
per-command ceiling and was not run; see ROADMAP § THE RUN BUDGET.

**Not shipped:** board-width irregularity and lap rhythm, which are geometry and need the
nightly bake. Under the sizing rule that landed on `dev` the same day, T-0002 is **split**: this
run's half is **T-0048** (done) and the board half is **T-0049** (`needs_bake`). The measured
tail — a tenth of neighbour pairs still differ by only ~2.4 % of value, because the deal is blind
to position — is **T-0047**.

**T-0047 closed that tail on 2026-08-22, and the bound did not move.** The deal is no longer
blind: `facades.js` now deals the whole town at once, offering every building **32** candidates
out of the interval L126 already fences and taking the one that stands furthest clear of the
neighbours already dealt — a floor of 0.14 of applied value for two buildings on one spot,
falling linearly to nothing at 60 m. Candidate 0 is the plain `id|phase` hash, so a building with
nothing inside 60 m keeps the exact tone it had, and 158 of 339 structures take a different deal.
Measured on the published mirror with the same instrument: the tenth percentile of applied value
between nearest neighbours goes **2.4 % → 7.7 %** and the median **10.3 % → 13.3 %**, so the tail
now reaches **0.58** of the middle where the acceptance asks for 0.5. 338 distinct tones across
338 structures, **0 identical pairs**, the two attested-paint records untouched and bit-exact.
**The rejected alternative is recorded because it measured worse:** a two-sided cost, one that
also pulled a well-separated pair back toward the target, collapsed the median to 4.9 % and the
ratio to 0.31 — repulsion only pushes, and that is why it is the right shape.



## Changed 2026-08-17 — the backlog is a ticket queue the owner can reorder

**On the owner's direct request.** His words: tracking "what i have asked for and what you
and the loop are working on" had become impossible — his own K-series requests sat below
line 9,300 of an 11,400-line ROADMAP with no status tags (K10, "walkable bridges", was
asked for in August and never entered any queue), and reordering priorities meant editing
prose. The operational state now lives in **`tickets/`**: one markdown file per ticket,
`QUEUE.md` as the single priority order (owner-ordered; agents append and remove only),
`BOARD.md`/`tickets.json` generated, `tools/ticket.mjs check` gating it in check.sh, and
the board mirrored to the site for Manager. **34 tickets seeded**: every open ROADMAP
parcel (with `legacy_id`), the owner's six recovered K-asks at the top of the queue, and
the four standing owner decisions as `blocked-owner` tickets with their options inline.
ROADMAP's NEXT UP table is frozen with a tombstone; the deep boxes remain the reasoning
archive. AGENTS.md § THE QUEUE is the new contract.


## Shipped 2026-08-17 — the bridge is a surface now, and you still cannot get onto it from the bank

**T-0001, half one of two.** The owner's ask was one sentence — *"How would a wagon cross
that?"* — and the walkthrough's answer was that nothing could, not even a person on foot.
The walker was a capsule sliding on the heightfield, and `terrain.walkHeight()` reports a
**4.0 m wading barrier** over open water so a visitor stops at the river's edge instead of
walking into the channel bed. The barrier sits ABOVE every deck in the dataset, so a
visitor set down on the North Branch bridge hovered 1.8 m over its planks — the float
`docs/LIBERTIES.md` L9 recorded as unreachable, which stopped being true the moment a
crossing was somewhere a visitor could be sent.

**What the deck's height is, and why it is not measured off the mesh.** `deck_height_m` is
already resolved by `generators/archetypes/bridge_timber_params.py` — the attested 1.83 m
clearance plus the stringer and plank depths, 2.22 m for the three river crossings and
0.83 m for the slough culvert. `tools/compile_scene.py` now carries that number into every
sidecar as `placement.walk_surface_m`, by the same route and for the same stated reason it
already carries `vertical_anchor`: two definitions of one number agree until the day one of
them matters. The parameter modules import without Blender, so this costs the compile
nothing and needs no bake. `null` on the other 327 structures, which keeps the sidecar one
shape everywhere. `docs/GLB-CONTRACT.md` carries it as an additive row.

Reading the deck's top face off the GLB was the other candidate and was rejected on the
contract: the deck IS its own primitive, findable by its material being named `deck`, but
material names are pinned nowhere in GLB-CONTRACT.md, and the drawbridge's gallows frames
stand five metres above its deck so the bounding box answers a different question.

**The renderer half is one function.** `walker.js` grew `surfaceAt()`, and every path that
ever asked how high the floor is — walking, the step-up test, teleporting, landing out of
free-fly, resettling after an eye-height change — goes through it. That was the point of
routing all of them rather than the walk loop alone: a walker that agreed with itself on
some paths is how you stand on a bridge and fall through it when you stop moving. Its two
rules are asymmetric on purpose. **Over water the deck wins outright**, because the barrier
is a navigation rule about a river you have no boat for and a bridge is the thing that
answers it. **Over land the higher surface wins**, because the slough this fourth bridge
crosses is not modelled in this terrain epoch and its deck therefore lies about 0.4 m
INSIDE the prairie — letting the deck win there would sink a visitor into a hill to walk a
bridge over a stream that is not drawn.

**A visitor can reach it.** `data/scenes/1835.json` gains *On the North Branch bridge,
mid-span*, a standing viewpoint at the deck's own centre looking east down it. Without it
the feature was reachable only by flying out over the channel and dropping, which is not
how anybody would find it.

### What the gate says

Four new assertions, all green at both viewports: the crossing has a walkable deck; the
walker crosses it **end to end** with the deck under the boot for every sample and the
standing clearance exact to better than 1e-9 m; the **deck and not the barrier** is what
holds them up (the barrier reads 4.0 m at mid-span, the deck 2.22 m); and they walk off the
far end down onto the bank. The height assertion is an exact equality rather than a
tolerance, which is the whole point of sourcing the number from the params: a tolerance
would pass a renderer that had quietly grown a second definition.

### Not claimed — and this is the owner's actual question

**You still cannot step ONTO a deck from the bank, and nothing here pretends otherwise.**
Both branch decks land exactly on the traced 1834 waterline, where the ground crosses zero
by construction; the deck top is 2.22 m. The 0.35 m step-up rule refuses a 2.2 m riser the
way it refuses a wall, and it should. Half two of T-0001 — log abutments in the shallows
(the 1883 old-settlers statement puts them there) and wagon-plausible approach gradients
meeting the deck at grade — is TERRAIN, and `generators/terrain_gen.py` needs Blender for
the ground GLB. The improve runner has none, so it belongs to the nightly bake. **No ramp
was faked and no threshold was widened to make this run look finished.** The ticket stays
open, at the top of the queue where the owner put it, with `claimed_by` cleared.

Three assertions fail, and **all three are `origin/dev`'s own at `3114e061`**, measured on
this runner rather than assumed. The two road-contrast stations are the pair STATUS has
carried since #135 and #201. The third — `the panel states that once too — and counts
nothing by hand` — is newly *observed* rather than newly broken: it has been red since K53
(#221) shipped a liberty whose reasoning opens "Three of these records describe
multi-stemmed plants", and the guard scans the whole Evidence panel instead of the heading
it means. The desktop half of the smoke has never fitted this runner's ten-minute
per-command ceiling, which is why nobody had seen it. Measured directly against a clean
`origin/dev` worktree with a one-assertion probe: FAIL there too, same `occurrences: 1`,
same liberty. Filed as **T-0037**.

Runs: `tools/check.sh` PASS. `SMOKE_VIEWPORT=desktop` on the source tree, 263 passed /
3 failed. `SMOKE_VIEWPORT=mobile --published`, 266 passed / 3 failed. 39 draw calls
against a budget of 80, unchanged.

## Shipped 2026-08-17 — the parcel asked for a finer grain at the same plate area, and the plates are what carries the recorded width

**ROADMAP K57**, opened by K56 six hours earlier: *at the same total plate area, is the shrub's shell
better read as 32 masses of 0.4 m or 64 of 0.2 m?* **The question cannot be asked at a fixed plate
area, and that is the finding.** The plates are what carries the clump's **recorded half-width** — the
one horizontal number in this archetype the research owns — so a finer grain paid for out of the plate
size pulls the whole bush in. 48 sprays ship, at the plate size K56 shipped.

### Finding — holding the area spends a researched number on a rendering one

Measured over 24 bearings by the new `tools/measure_spray_grain.mjs`, orthographic, on the archetype
the scene draws:

| candidate | plate area | foliage cover | worst bearing | stem cover | reach ÷ recorded half-width | plate on a 2.25 m hazel | triangles |
|---|---|---|---|---|---|---|---|
| 32 @ 1.000 — K56, shipped | 2.698 | 36.9 % | 33.0 % | 40.9 % | **0.990** | 37.3 cm | 72 |
| 48 @ 0.816 — area held | 2.604 | 43.3 % | 39.3 % | 46.8 % | **0.930** | 29.3 cm | 104 |
| 64 @ 0.707 — area held | 2.624 | 45.4 % | 41.5 % | 48.3 % | **0.890** | 25.8 cm | 136 |
| 48 @ 1.000 — **SHIPPED** | 3.812 | **46.9 %** | **43.0 %** | **51.3 %** | **0.998** | 35.0 cm | **104** |
| 64 @ 1.000 | 4.986 | 51.3 % | 47.3 % | 54.2 % | 0.997 | 34.6 cm | 136 |

So the parcel's own candidate — 64 sprays at the shipped total area — buys 8.5 points of cover and
pays **0.990 → 0.890** of the recorded half-width for them, taking the plate from 37 cm to 26 cm and
within 2.6× of the 10 cm leaf that K56's whole diagnosis says two triangles cannot draw. **The grain
trades against triangles, not against area**, and at the shipped plate size the count alone gives
32 → 48 → 64 a cover of 36.9 % → 46.9 % → 51.3 %. Ten of the fourteen available points arrive with
the first 32 triangles and four with the second, so **48 is where the return halves**. The remaining
4.4 points are measured and deliberately unspent; a run that wants them can read what they cost.

### Finding — K56's shell-fill figures were taken by a script nobody committed

17.7 % → 30.9 % cannot be reproduced or re-pointed at a candidate, because the numbers only ever
existed inside a function that imports three.js. Two things fix that, and the second is the reusable
one:

- `renderers/web/js/shrub-grain.js` — the archetype's stems, bands, spray plan and every corner, in a
  module that **imports nothing**, so node reads the same arithmetic the browser draws. The extraction
  was proved neutral before a number moved: **1,296 floats over 144 vertices, 0 differing, worst delta
  exactly 0** against the original loop.
- `tools/measure_spray_grain.mjs` — the instrument, ~7 s and no browser. Its `32 @ 1.000` row
  reproduces K56's committed plate area of **2.698 to the digit**, which is the check that it measures
  the town rather than a port of it. (Its `16 @ 1.000` row reads 1.387 against K56's 1.399 because the
  pre-K56 bush had two spray bands and this table has three — the row is the count alone, and is
  labelled that way.)

**`--gate` runs in `tools/check.sh`** and asserts the two numbers the research owns rather than the
one this run chose: reach ≥ 0.95 of the recorded half-width, and a spray ≥ 2× a 10 cm leaf so the
"leaf mass" abstraction cannot quietly become a claim to draw a leaf. The third assertion is a ratchet
— cover ≥ 40 % at **every** bearing, above K56's worst-bearing 33.0 % and below today's 43.0 %.

### What a visitor sees

`docs/evidence/k57-{before,after}.png`, the wet woods at E −54 / N +314 bearing 135°, 1280×800 on the
published mirror — the same station K54 and K56 used. **38.8 % of the frame's pixels change.** The
bushes cover 47 % of their own outline where they covered 37, and the dark stems under them are 51 %
hidden where they were 41.

**No census moved**, which is the assertion that this is a geometry change and nothing else:
`tools/measure_sward_draw.mjs --gate` reads back every banked figure to the digit — 7,069 slots,
deviation matrix **154.19** · forb **86.16** · shrub **18.84**, shrub instances **181** over eight
stations, forb **923**, `z03_sedge_meadow` forb **84**, 0 of 98 pairs drawn nowhere.

**Cost:** 72 triangles a shrub becomes 104. The census counts **167** shrubs standing in
`z06_dense_forest` — not the 156 K54 and K56 quote, which K55 moved — so the wet woods' ring is
**17,368 triangles, 1.7 %** of the scene's million. The spawn frame reads **541,701 → 541,733**, and
that +32 is exactly one shrub: `tools/shoot.mjs` dumps its stats before it teleports, so its figure is
the anchor's and never the station's. Worth knowing before quoting it as a scene total.

### What is NOT verified

**Neither half of `tools/smoke_renderer.mjs`, for the fifth parcel running.** See the note below; the
blocker is unchanged and this run did not fix it. What ran green in the foreground instead:

- `./tools/check.sh` — **CHECK PASS** in 22 s, which is this repo's actual dev gate
  (`chicago-4d-check.yml` runs it and nothing else), including the new grain step.
- `node tools/measure_spray_grain.mjs --gate` — **GATE: PASS**.
- `node tools/measure_sward_draw.mjs --gate` on the published mirror — **GATE: PASS**, every figure
  identical to the banked table.
- `node tools/shoot.mjs` at the K56 station on the published mirror, before and after — **zero page
  errors** both times, 35 draw calls of 80, within budget.

**Unverified consequences, stated plainly:** no frame-time figure was taken, so "104 triangles is
affordable" rests on the triangle count and the draw-call count and not on a measured frame; the
`balanced` (800,000) and `light` (600,000) ceilings were not read back, though `full` sits at 54 % of
its own and both lower levels draw strictly less; and the mobile viewport was not rendered at all, so
the +32 triangles a shrub are unmeasured at 390×780.

## Shipped 2026-08-17 — the same fault ran BOTH WAYS, and for the herbs it under-planted the riverbank 96×

**ROADMAP K55**, opened by K54 with its arithmetic banked and taken as the last list dealt off the
wrong sum. `SLOT_BASIS` is now one object naming which sum each stratum's slot count comes off, read
by both `flora.js` and `tools/measure_sward_draw.mjs`, and both lattice strata read `stems`.

| forb layer | density before | after | ratio | `forbShare` before → after |
|---|---|---|---|---|
| `z05_riverbank_timber` | 0.025 /m² | **2.407** | **96×** | 0.072 → **1.0, clamped** |
| `z10_settled_town` | 0.395 | **7.760** | 19.6× | 1.0 → **1.0, no slot moves** |
| `z03_sedge_meadow` | 0.123 | **1.254** | 10.2× | 0.354 → **1.0, clamped** |
| `z06_dense_forest` | 40.615 | **44.545** | 1.10× | 1.0 → 1.0 |
| the other six | unchanged to the digit | | 1× | unchanged |

Drawn, `node tools/measure_sward_draw.mjs --gate` on the published mirror: **forb slots 781 → 923**
over the census's eight stations, `z03_sedge_meadow`'s own layer **31 → 84** (cover 1.0 % → 2.8 % of
a recorded 11.0 %), `z05_riverbank_timber`'s **1 → 16** at its own station and **4 → 50** standing in
the wet woods, plus a `z05` row at `z03` that did not exist (**0 → 14**). Forb deviation per 100
slots **10.40 → 9.33**. **Matrix 154.19 and shrub 18.84 are K54's banked figures to the second
decimal**, and `0 of 98` pairs are drawn nowhere — which is the assertion that nothing but the forb
slot count moved.

### Finding 1 — the sign of this fault is decided by the plant's own size, and the queue inherited the wrong one

`stems = cover ÷ π(width/2)²`. A 2.25 m dogwood clump covers about 4 m², so reading its cover
fraction as a count OVER-states it — K54's 8.8×. A 10 cm forb covers about 0.008 m², so the same
reading UNDER-states it by about 125×. The fault was banked as over-planting because that is the
case measured first, and K55's own statement inherited the direction along with the diagnosis:
it predicted `z05`'s understory was "8.8× too thick" when its herb layer was 96× too thin.

### Finding 2 — three of the six named rows were never faults; the column printed a default argument

The parcel suspected the matrix half was a refusal, and it is. `matrixShare` is
`cover.matrix_fraction` read off the record, so `subsetOn`'s `density` was **computed for the matrix
and read by nobody** — and `auditAbundance` reported `basis: list === 'shrub' ? 'stems' : 'recorded'`,
which is `subsetOn`'s default parameter rather than anything the renderer does. `z03.matrix`,
`z08.matrix` and `z09.matrix` were named as K55 work on that basis. Both sides now read `SLOT_BASIS`,
whose matrix entry is `null`, so the report prints *"slot count off cover.matrix_fraction, not this
sum (lottery only)"* and there is no number left to misread.

### Finding 3 — it is SEEN, and only just: the count moved a fifth and the frame moved 0.15 %

`docs/evidence/k55-{before,after}.png` — `z05_riverbank_timber`, E −300 / N +398, bearing 090°,
1280×800 on the published mirror, before shot with `HEAD`'s `flora.js` swapped into the same mirror
so nothing else differs: **1,586 changed pixels of 1,024,000 (0.15 %)**, a scatter of white flower
heads through the near grass. The `z03_sedge_meadow` station changes **24 pixels at bearing 135° and
nothing visible at 315°**, because the added plants are small and stand under a dense matrix layer.
**And the parcel's predicted visible half is refused outright**: `z10_settled_town`'s share was over
the lattice ceiling before and after, so the one community a visitor spends the walk in does not
move a plant. Quote the counts for this parcel, not a screenshot.

Opened by this parcel: **K58** — the clamp above is now load-bearing in six communities of ten, so
those layers are drawn at a density `TUNE.forb` chose rather than one any record states.
`flora.communities()` gained `forbShare`, `forbShareWet`, `shrubShare` and both densities in this
change precisely so K58 can read them; before it, a share sitting on its clamp and one tuned there
were indistinguishable from outside the module.

### Verified, and the mobile half got further than the last four parcels did

`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published`, foreground, killed by a 555 s
`timeout` before printing its verdict — the trailing `page.click: Target page … has been closed` is
that kill. What it logged before then: **178 assertions passed and exactly 2 failed**, and the two
are `south_water` and `from_above` road contrast, **still red exactly as R-W1 and T-V2 recorded
them** (see the R-BUG7 section below for the same pair). No other failure.

**The parcel's own layer is inside the part that ran**, which is why this is a verification and not
a shrug — at 390×780, on the published mirror:

- `pass  every slot the sward deals is counted against a species`
- `pass  every species the stand owes a stem to stands in it`
- `pass  detailed flora roots share the terrain and water surfaces`
- `pass  emergent flora stays within eight metres of a riverbank`
- `pass  no elevated flora sheet can masquerade as a second terrain layer`
- `note  sward tail — 0 species owed a whole slot and drawn nowhere`
- `note  sward abundance — 6 of 27 lists mix an area with a count`, the same six, unchanged: a
  mixed list is a fact about the dataset and no longer a defect.

**Not claimed: the desktop half**, ~13 minutes against this runner's ten-minute per-command
ceiling, and not the verdict line at either viewport.

What else ran in the foreground and passed:

- `./tools/check.sh` — **CHECK PASS**, which is this repo's dev gate (`chicago-4d-check.yml`).
- `node tools/measure_sward_draw.mjs --gate` on the published mirror — **GATE: PASS**, 7,069 slots
  in 22 lists, 0 of 98 pairs drawn nowhere.
- `node tools/shoot.mjs` at four station/bearing pairs on the published mirror — **zero page
  errors**, 35 draw calls of 80, 541,701 triangles of 1,000,000.

**Unverified consequences, stated plainly:** no frame-time figure was taken anywhere, and the
desktop half never ran; the two newly clamped communities are asserted from `flora.communities()`
rather than from a drawn count, because a clamped share draws the same slots however far past 1.0 it
is — which is K58's whole point.

## Shipped 2026-08-17 — a shrub's leaf spray is a MASS of leaves, and sixteen of them covered 17.7 % of the bush

**ROADMAP K56**, opened by K54 six hours earlier on the observation that the shrub archetype was
designed and photographed at fourteen instances in the whole scene and the wet woods now carries
**158 in one ring**. The parcel asked the right question in the right order — *what does a spray
STAND FOR, before any number changes* — and the answer decides which number moves.

**A spray stands for a season's leaves on one shoot.** That is the same abstraction the tree
canopy's plates and the near tuft's bundle of shoots already use here, and it is the only one two
triangles can carry: a hazel leaf is about 10 cm and no scaling off the clump width produces one.
So **the 0.4 m spray is not the fault, and shrinking it would have bought a smaller plate with more
sky around it.** Recorded as **L124** before the geometry was touched.

### Finding — the fault is the COUNT, and it is 17.7 % of a shell

Summed over the archetype's own loop, the sixteen sprays' plates cover **17.7 %** of the shell they
are spread over. A visitor sees straight through every clump, and an isolated plate with sky on both
sides of it reads as one enormous leaf precisely BECAUSE nothing overlaps it — which is why the size
looked like the culprit.

| | before | after |
|---|---|---|
| leaf sprays per shrub | 16 | **32** |
| spray bands | 2 | **3, the lowest arching DOWN** |
| plate area, archetype units² | 1.399 | **2.698** |
| shell fill | **17.7 %** | **30.9 %** |
| triangles per shrub | 40 | **72** — +5,056 in the wet woods' ring, of a 1,000,000 ceiling |
| spray length on a 2.25 m clump | 0.26–0.44 m | **0.26–0.44 m, unchanged** |
| drawn reach ÷ recorded half-width | 0.91 | **0.98** |

### Finding — nothing in the first cut hung below its own attachment

All sixteen sprays rose, so the shell stayed open exactly where the four stems are most exposed —
and `k0 = shade(0.16)` makes a stem a black stick wherever foliage does not cover it, which the
archetype's own comment feared in the abstract and `docs/evidence/k56-before.png` shows happening.
The lowest of the three bands now arches down over them, bounded so no tip is pushed below the
plant's own base.

`docs/evidence/k56-{before,after}.png`, the same station K54 used (E −54 / N +314, bearing 135°) at
1280×800 on the published mirror. **No census moved:** same species in the same places, plant for
plant; `spread`, `height` and the lattice are untouched, so `tools/measure_sward_draw.mjs` reads
back what it read yesterday — which the parcel predicted, because no count moves.

Opened by this parcel and **not** answered: **K57**, the spray's GRAIN — at the same total plate
area, is the shell better read as 32 masses of 0.4 m or 64 of 0.2 m? That trades triangles against
grain and needs a measured budget in the wet woods rather than a preference.

### What is NOT verified

**Neither half of `tools/smoke_renderer.mjs`.** `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` was started in the foreground and killed at 570 s without reaching a verdict, so the
run has the same gap K45(b4), K53, K54 and K52 all recorded: the suite has outgrown this runner's
ten-minute per-command ceiling at BOTH viewports, and the honest thing is to say so rather than
background it. **This is now a four-parcel-old blocker on the lane, not an incident.**

What ran in the foreground instead, and passed:

- `./tools/check.sh` — **CHECK PASS**, which is this repo's dev gate (`chicago-4d-check.yml`).
- `node tools/measure_sward_draw.mjs --gate` on the published mirror — **GATE: PASS**, and every
  figure is identical to K54's banked table to the digit: shrub instances 181 over 8 stations,
  156 in `z06_dense_forest` at 40.1 % of a recorded 94.9 %, `z05_riverbank_timber` 20.1 % of 19.5 %,
  deviation `shrub 10.41 over 181`. That identity IS the assertion that no count moved.
- `node tools/shoot.mjs site/chicago/4d /walk/` over all seven visitor anchors on the published
  mirror — **zero page errors**, 35 draw calls of 80, **541,701 triangles of 1,000,000** at `full`
  detail (541,668 before, measured at the spawn anchor where one shrub stands).

**Unverified consequences, stated plainly:** the triangle ceilings at `balanced` (800,000) and
`light` (600,000) were not read back, though `full` sits at 54 % of its own and both lower levels
draw strictly less; the mobile viewport (390×780) was not rendered at all, so the +32 triangles a
shrub were never measured at the detail level a phone gets; and no assertion about the wet woods'
frame time was taken, which is the half **K57** says a grain change needs before it moves.


`tools/shoot.mjs` gained a `--at e,n,yaw[,name]` flag, because an archetype before/after pair needs
one arbitrary station and the tool only had the visitor anchors, none of which stands in a plant
community. Its positional arguments are now read with flags removed, which also fixes `--at`
before the output directory silently becoming the output directory.

## Shipped 2026-08-17 — seventeen households were in the dataset and on no page, and the layer's one reader is why

**ROADMAP K52.** `data/residents/` was the layer that already had a reader, which is why K51's
successor named it the *harder* question: `tools/compile_scene.py`'s `compile_residents()`
attaches a household to a building sidecar and `popup.js` names it on the building card, so
"the browser has it" read as "somebody looks at it". The join reaches a building through
`lives_at` or `works_at`.

| | households | person entries |
|---|---|---|
| in `data/residents/` | 173 | 209 |
| reachable through a building card | 156 | 189 |
| **reachable nowhere** | **17** | **20** |

**The seventeen are the ones whose residence and workplace are both unattested at the scene
date** — so the layer was dropping records for being poorly evidenced, which is the opposite
of what this project's confidence model is for. The Mark Beaubien household is one of them:
he had left the Sauganash by 1834 and the Exchange by August 1834, where he slept on
1 July 1835 is not in the record, `lives_at` is `null`, and the join drops the most famous
household in the town.

### Finding 1 — a reader is not a read map

The join copies id, name, division, the relation and its note, and a person's name,
relationship, grade and occupation word. `arrival`, `origin`, `reason_for_coming`,
`party_size_on_arrival`, `present_on_scene_date`, `touches_removal`, a person's `sex`,
`age_on_scene_date`, `birth_year`, `name_basis` and their own `sources`, the occupation's
grade and reasoning, and the ten `researched_not_resident` findings all stopped at the
repository. The last of those is the sharpest: its own manifest doc calls it *"as load-bearing
as the households"*, and it includes a person this project believes was here and cannot cite,
*"recorded so that the gap is visible rather than quietly filled"*.

### Finding 2 — K42's assertion 3a did not fire, and that is a hole

`tools/measure_layer_reads.py` scans `flora` and `fauna` by name, so `residents` gaining a
reader tripped nothing. The fauna parcel was caught by its own instrument; this one was
caught by reading the join by hand. Extending the census to this layer is **K52(b)** and is
not done — the tool's kinds, baseline and negative control are all written around the other
two layers.

### What shipped, and what it does not do

The Evidence panel's people section: the manifest in one fetch, all 173 households with their
division, people and grade tallies, the 17 marked on their own rows, and the full record
fetched the first time a row is opened. Every graded claim carries its value, its confidence,
its reasoning and its joined citations (11 sources, joined by
`compile_residents_sources()`). **Nothing is drawn** — L1 stands, no human figure is in the
scene, and nothing went into `docs/LIBERTIES.md` because nothing was invented.

### What is NOT verified

The desktop half of `smoke_renderer.mjs` does not fit the runner's ten-minute per-command
ceiling and did not run. The mobile half ran on the published mirror: **263 passed, 2 failed**,
both failures the road-contrast bands `dev` already carries red (§ *Landed with two bands red*,
below) and neither this parcel's — it changes no 3-D rendering at all.

## Shipped 2026-08-17 — the shrub layer is a stratum and now has its own lattice: 4 bushes standing become 181

**ROADMAP K54**, route 2, opened by K53 six hours earlier with its arithmetic banked. The forb
lattice carries **one plant per 2.89 m² of ground**, so where the herb layer's own recorded density
saturates it the deal becomes a count-proportional SUBSAMPLE — and a subsample by head count thins
the shrubs by the whole saturation ratio, which in the wet woods is **117**. The two strata are not
competing for that ground in the first place: a hazel clump stands OVER the leeks, and the records
say so separately (nine `shrub_low` records in `z06_dense_forest` summing to 94.9 % cover, above a
herb layer recorded at 40 plants/m²). So the shrubs are dealt from **their own lattice pass over the
same ring**, at their own recorded clump density, and nothing is taken from the herb layer to pay
for them.

| `tools/measure_sward_draw.mjs`, published mirror, 8 communities stood in | before | after |
|---|---|---|
| shrub instances standing, summed over the 8 stations | **4** | **181** |
| shrubs drawn standing in `z06_dense_forest` | 2 | **156** |
| drawn shrub cover there, against a recorded 94.9 % | ~0 | **40.1 %** |
| drawn shrub cover, `z05_riverbank_timber`, recorded 19.5 % | 2.0 % *(whole forb list)* | **20.1 %** |
| deviation per 100 slots — matrix | 2.58 over 5,965 | **2.58 over 5,965** |
| deviation per 100 slots — forb | 10.56 over 844 | **10.40 over 781** |
| deviation per 100 slots — shrub | — | **10.41 over 181** |
| (list, species) pairs owed a whole slot and drawn nowhere | 0 of 98 | **0 of 98** |

**K49(c2)'s gain is kept and the raw sums cannot show it**, which is why the tool now prints the
per-100-slot figure: the deviation is an absolute sum over slots and this parcel split one list into
two, so `forb 89.11` became `forb 81.22 + shrub 18.84` at unchanged per-slot fidelity. The matrix
layer is untouched to the second decimal.

### Finding 1 — the slot count still mixed units, and it planted the riverbank understory 8.8× too thickly

K49(c2) moved the LOTTERY onto `stems` and said in as many words that the slot count was left on
the recorded sum. That sum adds cover fractions to plants per m², and sixteen of the twenty-one
shrub records state an area: `z05_riverbank_timber`'s forb share was **0.636 where its herb records
give 0.072**, and `z07_bur_oak_savanna`'s hazel was planted at **4×** its own recorded clump
density. Dealing the shrub stratum off `stems` fixes it for that stratum. **Four herb lists still
carry it — `z03`, `z05`, `z06`, `z10` — and the tool now names them; opened as K55.**

### Finding 2 — the census tool's headline label had been wrong since K49(c2), and K54's own box quoted it

`expected` is `share × slots` and `share` is the species' share of the LOTTERY, so
"deviation from the recorded cover" measures the lattice's disagreement with its own target
distribution, not with any record. K54's box cited that line as the instrument for judging which
quantity the sample reproduces; it cannot answer that question. The tool prints a real **cover**
column now — drawn ground cover against recorded ground cover, per community — and its first
denominator was wrong in R-M1c's exact way: dividing a community's plants by the whole ring reported
17.9 % where the community holds a fifth of the ring. It divides by the community's own **measured
plantable ground** inside the ring.

### Finding 3 — what the pair of screenshots shows, and it is not only more plants

`docs/evidence/k54-{before,after}.png`, same station (E −54 / N +314, bearing 135°), published
mirror at 1280×800: **before** is an open field with a log building 15 m away and one shrub in the
corner; **after** is a thicket the building shows through. Flora triangles at that station
**46,904 → 58,868**, and the herb layer is untouched — forb 194 → 195, rosette 35 → 31 — which is the
arithmetic proof that nothing was taken to pay for the shrubs. It is also the first look anyone has
had at this archetype REPEATED: it was designed and photographed at fourteen instances in the whole
scene and there are 158 in one ring, where its ~0.4 m leaf sprays are a community's near-field
texture. Opened as **K56**, which asks what a spray stands for before it changes a number.

### What is NOT verified

Neither half of `tools/smoke_renderer.mjs` — the desktop half has never fitted this runner's
ten-minute per-command ceiling and the mobile half has outgrown it too (K45(b4), K53). Its flora
gates read the sets by NAME and `flora-shrub` is already inside all of them (K53), and no set, ring
or archetype was added here — only the pass that fills one. **Unverified consequences, stated:** the
scene was not measured at `full` detail, where the shrub lattice offers ~1,113 slots against the
set's 900-instance cap, so a saturated community may cap there — the forb set has the identical
lattice and cap and sits just under it today. What ran in the foreground: `tools/check.sh` (CHECK
PASS, the dev gate), `tools/measure_sward_draw.mjs --gate` (PASS, both columns above), zero page
errors in every run.


## Shipped 2026-08-17 — the shrub layer was drawn with the forb archetype, and the clamp that made that survivable was hiding the recorded width

**ROADMAP K53**, from K45(b4)'s *"still not planted"* note. Twenty-one records across eight zones
carry `form: 'shrub_low'` and `FORB_FORMS` contains that string, so hazel, elder, buttonbush,
dogwood, ninebark, hawthorn, sumac, wild plum, brambles, meadowsweet, currant, sand cherry, dune
willow, juniper and the black-oak grubs were all drawn as **one herbaceous stalk with four broad
leaves**, scaled to the record's height — and their recorded clump width was clamped to 0.40 m,
because `placeForb`'s leaf archetype cannot survive a two-metre width.

`shrubGeometry()` is four woody stems from one root under sixteen leaf sprays, 40 triangles against
the forb's 12, on its own set `flora-shrub` dealt from the same forb lattice.

| measured at 8 anchors × 4 bearings, published mirror, 1280×800 | before | after |
|---|---|---|
| plants drawn with the shrub archetype | **0** | **14** |
| clump width | 0.40 m (the forb clamp) | **1.80 m median** |
| forb-layer plants, all archetypes | 2,201 | **2,201** (2,187 + 14) |
| flora triangles, worst view | 41,754 | 41,772 |

**Nothing was redealt.** Per zone as well as in total — `z08_lakeshore` 131 → 122 + 9,
`z05_riverbank_timber` 61 → 57 + 4, `z06_dense_forest` 222 → 221 + 1 — so the sward census reads the
same 6,809 slots and the same 154.19 / 89.11 deviations K49(c2) banked.

### Finding — only fourteen of them stand, and the reason is the lottery rather than the archetype

The forb layer deals ~220 slots over its ring and species compete for them on `stems`, plants per
m². The conversion for a cover-recorded species is `cover / (π · (width/2)²)`, so a hazel covering
7 m² of ground is **0.088 plants/m²** against `allium_tricoccum`'s **40**. Shrub share of each
zone's forb list: `z10_settled_town` **0.1 %**, `z06_dense_forest` **1.0 %**, `z08_lakeshore` 2.6 %,
`z05_riverbank_timber` 3.0 %, `z09_sand_prairie` 7.6 %. **`corylus_americana` is `attested` at
20–50 % ground cover and is drawn as 1 plant of 221.**

The count is not wrong — one hazel is one plant — but a ~220-slot sample dealt by head count
reproduces the population's head count and none of its ground cover. K49(c2) moved this lottery onto
counts deliberately, so moving it is a decision and not a repair: banked with its arithmetic and
opened as **K54**.

### What is NOT verified

Neither half of `tools/smoke_renderer.mjs` ran: the desktop half has never fitted this runner's
ten-minute per-command ceiling and K45(b4) recorded the mobile half outgrowing it too. The three
smoke gates that read the flora sets by NAME — rooted-plant anchoring, the pop-in walk, head
support — plus `tools/measure_head_support.mjs` were extended to `flora-shrub` in the same commit,
so the new set is inside them rather than invisible to them, **and that extension is unexecuted
here.** What did run, in the foreground: `tools/check.sh` (CHECK PASS, the dev gate),
`tools/measure_sward_draw.mjs --gate` (PASS), and the instance read-back above, with zero page
errors in every run.


## Measured 2026-08-17 — the flicker left after the shadow fix is NOT co-planar ties, and two tests say so

R-BUG6(a) fixed the shadow crawl and left 1,108 pixels at `from_above` it could not explain,
attributing them to "co-planar depth ties" — a phrase this file, the ROADMAP row and R-BUG1's
successor note all repeated, on no measurement. **R-BUG6(b) ran the two tests that can settle it
and the attribution is refuted.**

| test | what it can see | result |
|---|---|---|
| depth function `LessEqual` → `Less`, all 11 materials | changes a pixel **only** where two surfaces sit at exactly the same depth | 36,187 px of the frame move; **13 of them are flickering pixels — 1.2 %** |
| near plane 7 m → 35 m (5× the depth precision) | heals any tie decided by rounding | **604 of 607 survive**; whole frame 1,108 → 1,115 |

What is left is the town's own geometric edges being resampled by a camera that moved. That is
antialiasing, it is in every correct renderer, and R-BUG1's altitude-dependent near plane had
already taken the real defect.

### Finding 1 — an exact tie is STABLE; it is the near tie that flickers

3.5 % of this frame is exactly co-planar and none of it shimmers, which had looked like luck and
is arithmetic: two surfaces at the *same* depth quantise identically from every camera position,
so the winner is fixed by draw order and draw order does not move when the visitor does. A gap
*smaller than one quantum* is the one the camera re-rolls. The two are indistinguishable in a
still frame and opposite in motion, and this project had been reasoning about the first while
measuring the second.

### Finding 2 — a layer's footprint is the set of pixels that change when you hide it

`tools/measure_tie_class.mjs`. Exact ownership, decided by occlusion the way the depth buffer
decides it: structures 556 of the 1,108, trees 491, ground 35, water 22, streets 4, flora 0,
**unattributed 0**, control 0 px and return-to-pose 0 px. Buildings and trees own **94.5 % of the
flicker on 7.7 % of the frame** — the shape of edges, not of surfaces.

### Finding 3 — and the trap in that instrument's own second column

Its `interior` column was meant to separate ties from edges: a pixel surrounded by its owner's
footprint has nothing else drawn there. **It is not sound.** A roof against its own wall, a
chimney against its own roof and one building in front of another are all interior to the
`structures` footprint and all ordinary silhouettes — which is why 604 of 607 "interior ties"
survived 5× precision. A footprint says WHO owns a pixel and cannot say WHY it moved. The column
is kept with the caveat printed beside it, because the ownership half is exact.

### Finding 4 — the river-edge gate counts the sky as water

`measure_river_edge.mjs` calls a pixel wet when `b > r + 6 && g > r`, and a July sky passes:
measured on the same frame, **rows 0–200 are 1,280 of 1,280 "waterish"**. So its `bank_px` =
33,328 is mostly the horizon plus every roof and canopy silhouette against it. The gate is a
share and both halves inflate together, so it has not passed anything it should have failed —
but its pixel counts are not counts of the river and must not be quoted as such.

### What is NOT verified

The desktop half of `smoke_renderer.mjs` does not fit the runner's ten-minute per-command
ceiling and did not run. No renderer file was changed by this parcel, so there was nothing for
it to regress. R-BUG6(c) — whether the 36,187 co-planar pixels show the surface their record
intends — needs a bake and is not answered here.


## Fixed 2026-08-17 — the shadow grid slid a fraction of a texel under every step

**ROADMAP R-BUG6(a).** The sun has one orthographic shadow box and it follows the visitor. It was
re-centred on their exact position every frame, and a shadow map is a **raster**: its samples are a
lattice fixed to that box, so sliding the box by a fraction of a texel re-quantises every shadow
edge in the scene at once. Nothing in the world moves and every boundary is redrawn slightly
differently — the crawl along an eave line, and it got worse the day the reach went to ±240 m,
because shadow edges now cover the whole town instead of 60 m of it.

The centre is rounded onto a **world-anchored lattice of the box's own texel size**, in the light's
own plane. The offset is at most half a texel (5.9 cm desktop, 11.7 cm phone) and it is only ever
across the map, never along the sun — so the reach, the map size, the 11.7 / 23.4 cm texel and the
`bias` and `normalBias` calibrated to that texel are all untouched.

**Measured with the camera held perfectly still and the box slid half a texel — the only honest way
to isolate it (finding 3):**

| station | changed pixels, box slid ½ texel |
|---|---|
| `from_above`, 175 m | **2,023 → 0** |
| `descend_main_stem`, 90 m | **5,650 → 0** |

Under R-BUG1's own 2 mm nudge, on the published mirror at 1280×800: whole-frame flicker
**1,284 → 1,184** and **2,383 → 2,195**, and the gated bank share **2.9 % → 2.6 %** and
**3.4 % → 3.1 %**.

### Finding 1 — the control that "cleared the shadow map" was inert, and now it moves 5,439 pixels

`measure_river_edge.mjs --no-sun-shadow` dropped `sun.castShadow` after boot and changed **0
pixels**, which R-BUG6 recorded as a flag that never reached the render. The mechanism is
compilation: `castShadow` is read when a material's program is built, so flipping it afterwards
leaves every shader in the scene still sampling `directionalShadowMap[0]`, and the map itself is
still hanging in the texture unit from the last frame that had one. The scene keeps its shadows and
the flag reports success. The handle is now `renderer.shadowMap.enabled` **plus a `needsUpdate` on
every material in the scene**, which rebuilds each program against the new
`NUM_DIR_LIGHT_SHADOWS`. Putting the shadow back changes **5,439** pixels of the first station's
frame, which is the liveness number this diagnostic never had.

**Carry this forward: a renderer flag read at compile time is not a runtime handle.** Three of this
project's diagnostics flip one.

### Finding 2 — the town's flicker is mostly NOT the sun, and now there is a number

With the repaired control, taking the shadow map out of the frame entirely on `dev` moves the
whole-frame flicker from **1,284 → 1,108** at `from_above` and **2,383 → 2,008** at
`descend_main_stem`. So **the shadow map carries 14–16 %** of what R-BUG6 was opened to explain,
and the snap banks about half of that. The remaining ~84 % is co-planar depth ties — R-W5a2's
class, reached from the other direction — and is opened as **R-BUG6(b)** with those numbers as its
baseline. The parcel's title asked why the town flickers; the answer is "a seventh of it is this",
and saying so is the point.

### Finding 3 — a sub-pixel nudge cannot measure the shadow box, and scaling it up fails

2 mm slides the lattice by 1.7 % of a texel. A visitor walking at 1.4 m/s slides it twelve texels a
second, so the nudge understates the defect by about sixty times. The obvious repair — nudge by a
half texel instead — **does not work, and the measurement is kept because it is the interesting
part**: at `from_above` a 58.6 mm nudge changes **29,138** pixels with the snap on and **28,784**
with it off. The camera move resamples the whole frame, swamps the box, and even reverses the sign.

**A sub-pixel nudge is an instrument for depth ties only.** To measure the box, move the box:
`--box-drift` freezes `follow`, places the box twice half a texel apart, and photographs one
identical pose. Every pixel of that difference is the shadow map re-quantising, which is the
2,023 → 0 in the table above.

### Finding 4 — the instrument could not run on this runner, and the reason was a wait

Every capture timed out. `elementHandle.screenshot()` waits for the element to be *stable* — two
consecutive animation frames with an unchanged bounding box — and one frame of this scene under
SwiftShader takes about ten seconds, so two of them do not fit Playwright's 30 s action timeout.
Measured on the published mirror: element capture fails at 12 s where `page.screenshot()` returns
in **10.2 s** from the same page. The tool photographs the page now, with an assertion that the
canvas fills the viewport at the origin so the substitution is proven rather than assumed. **A
stability wait is the wrong wait in a harness that holds the clock on purpose**, and it is worth
checking the other Playwright tools here for the same idiom.

### The gate, and the assertion that failed a correct rig

Three assertions, and the middle one is R-A1's liveness clause. The box holds still across a
sub-texel step (**2.4 × 10⁻¹⁵ m** across the map, which is float noise); with
`world.setShadowSnap(false)` the same millimetre moves it **0.994 mm**; and a 1 m walk moves it
**5 times on the phone's 23.4 cm texel and 11 on the desktop's 11.7 cm, every jump exactly 1.000
texel** — the lattice pitch measured from outside, without the light's basis.

**The first version of the first assertion demanded the box hold still absolutely, and failed a
correct rig at 0.107 mm.** The centre keeps the walker's own component along the sun's direction,
because quantising that would move the box in depth for no benefit. An orthographic camera
translated along its own view axis rasterises every world point to the identical texel, and the
depth it writes and the depth it compares against shift together — so the invariant is *across the
map*, and the assertion projects onto `world.direction` to say so. **An invariant asserted one axis
too widely fails the code that satisfies it.**

## Shipped 2026-08-17 — the shadows reach ±240 m, because the whole town became one draw call

**ROADMAP R-W5a2 + R-W3b(a2)**, taken as one parcel: the batch merge is the enabler and the reach
is the payoff, and R-W3b(a) — six hours earlier — had already measured the reach as **draw-call-
bound** and named this merge as what unbinds it.

`buildings.js` grouped the town into one `BatchedMesh` per distinct material, and after R-W5a took
base colour out of that key the only field left splitting it was **roughness**: 16 batches for 16
finishes. Roughness is now carried per vertex the way colour is (`_roughness` plus a substitution
of three's `<roughnessmap_fragment>`), and the town is **one batch** — one call in the colour pass
and one in the shadow pass.

| anchor | dev: ±120 m, 16 batches | shipped: ±240 m, 1 batch |
|---|---|---|
| `green_tree` | **74** of 80 calls | **50** |
| `forks` | 73 | 47 |
| `south_water` | 69 | 41 |
| `from_above` | 69 | 44 |

**The reach doubled at the SAME texel size** — 4096² desktop / 2048² phone over a 480 m box is
11.7 cm and 23.4 cm, the figures this rig has resolved since R-W3b(a). Counted off the data:
`green_tree` **27 → 49** of 331 structures and **0 → 70** of 730 stems; `south_water` **26 → 91**
and **54 → 239**; `forks` **16 → 46** and **17 → 151**. Evidence pair at `green_tree` in
`docs/evidence/r-w5a2-{before,after}.png`.

### The finding: a batch merge is not pixel-identical, and a frame MEAN cannot see why

R-W5a's acceptance — whole-frame mean |Δ| under 0.01 of an 8-bit count — passes here four times
over, at **0.0024**. It is the wrong statistic for this operation. Shot at seven poses, 1280×800:
**942 pixels of 7,168,000 changed, the worst by 90 counts.** They are scattered singletons at roof
and wall junctions, and the cause is that merging sixteen batches into one **reorders the
submission of co-planar triangles that were tying in the depth buffer**. That is **R-BUG6's** own
class of defect reached from a direction it did not consider: a batching change can move a tie
without touching a material, a bias or a near plane. A merge parcel owes a changed-pixel COUNT and
a worst-pixel figure beside the mean.

The other 6,999,058 pixels are identical to the byte, which is the proof that the per-vertex
substitution is exact: had it silently failed, the whole town would have rendered at one roughness
and millions of pixels would have moved.

### What is NOT verified

The **desktop half of `tools/smoke_renderer.mjs` does not fit the improve runner's ten-minute
per-command ceiling** and did not run (ROADMAP § THE RUN BUDGET). `SMOKE_VIEWPORT=mobile` on the
published mirror is **250 passed, 2 failed** against `origin/dev`'s **246 passed, 2 failed**,
measured on the same runner with the same command: the same two road assertions `dev` already
carries, and the +4 is exactly this parcel's four new gates. `tools/check.sh` is **CHECK PASS**.
Every desktop figure above comes from `tools/measure_shadow_reach.mjs` and
`tools/measure_shipped_batches.mjs` at 1280×800 on the published mirror, not from the gate.

**4096² is asserted, not profiled.** Nothing here measures shadow-map memory or fill on real
hardware; the frame-time readings are swiftshader's and moved by under 2 %, consistent with
R-W3b(a)'s finding that the pass is geometry-bound. A phone that cannot allocate 2048² is not
something this runner can observe.


## Fixed 2026-08-17 — the sun threw a shadow within 60 m of the visitor and nowhere else

**ROADMAP R-W3b(a)**, the reach half of the cascaded-shadows parcel. The sun has one orthographic
shadow camera that follows the visitor, and everything outside it is clipped out of the depth map
before it is drawn. Counted off the DATA — each structure's `placement.local_e/local_n`, each
planted stem's own station, tested against the shadow camera's own matrices, on the published
mirror:

| anchor | structures inside, ±60 m | at ±120 m | stems, ±60 m | at ±120 m |
|---|---|---|---|---|
| `south_water` | **8** of 331 | **26** | **12** of 730 | **54** |
| `green_tree` | 8 | 27 | 0 | 0 |
| `sauganash` | 5 | 16 | 34 | 76 |
| `lake_market` | 5 | 13 | 33 | 73 |
| `from_above` | **1** | 8 | 41 | 55 |

Shipped at **±120 m with the map doubled to match** — 2048² on desktop, 1024² on a phone — so the
texel size is unchanged at 11.7 cm and 23.4 cm. Nothing in the near field got softer to buy the
distance, which is what the evidence pair at `green_tree` is shot to show.

### The finding: the reach is draw-call-bound, not fill-bound

Every batch entering the box is another draw call in the shadow pass. At `green_tree`, the worst
anchor: **70 calls at ±60 m, 74 at ±120, 78 at ±150 and exactly 80 at ±180** — and 80 is the
budget the smoke asserts, reached with two thirds of the town still outside the box. So the route
past ±120 m is **R-W5a2** (fewer batches) or **R-W3b(b)** (true cascades), not a bigger constant.

### What is NOT verified

The desktop half of `tools/smoke_renderer.mjs` does not fit the improve runner's ten-minute
per-command ceiling, so it did not run here. `SMOKE_VIEWPORT=mobile` ran green, `tools/check.sh`
ran green, and the desktop draw-call figures above come from
`tools/measure_shadow_reach.mjs --frames 4` at 1280×800 at all eight anchors rather than from the
gate itself.

## Shipped 2026-08-17 — the visitor can choose the light, and the switch shipped yesterday was reporting its position from memory

**ROADMAP K24**, owner-requested 2026-08-14: *"Can you make this an option in settings?"*, asked
on being told that R-W1's calibrated sky makes the scene 16 % dimmer and that holding the old
brightness would collapse albedo retention to 62 %. A **Brightness** slider in Settings, default
**0 stops** — the calibrated grade — opening the tone-mapping exposure by up to **one photographic
stop** (0.95 → 1.90).

### It dissolves the trade-off rather than picking a side, and the ceiling is a unit rather than a taste

"Correct and dim" against "bright and wrong" is a false choice when the visitor can be handed the
dial. What makes it safe is that the dial moves **one scalar on the tone mapper** and nothing else:
no light intensity, no material, no sky uniform, no fog, nothing in `data/`. There is no position
of it under which a wall is a different colour than the record says it is — which is the difference
between an accommodation and a second reconstruction, and it is why this could ship while R-W1
itself is still parked on PR #125.

**The ceiling is one stop because a stop is the unit, not because one stop looked right.** It is
what a camera's own exposure compensation is calibrated in; it is the largest correction that still
reads as the same photograph; and past it ACES rolls the sunlit roofs and the sky together into a
flat highlight, so the scene stops getting easier to see and starts losing the surfaces this
project documents.

**The design question K24 left open is decided: a slider, not a two-way toggle**, following the
eye-height precedent — and the readout names the calibrated position (`Calibrated — the light as
measured`) rather than showing a bare zero, for exactly the eye-height reason. A named default
makes moving off it a visible choice instead of a silent drift. `world.js` was touched in **two
places** (`BASE_EXPOSURE`, and a `setBrightness` on the returned world) rather than rewritten, so
PR #125's lighting rewrite conflicts with a constant and a method instead of a rewritten file — the
sequencing note in K24's box said "after #125", and this is why it did not have to be.

### The K24 constraint, asserted four ways — and the fourth is the finding

| assertion | mobile 390×780, published mirror |
|---|---|
| off with no stored preference | `brightness` **0** stops, `exposure` **0.95** |
| raising it reaches the render | cell delta mean **49.40**, worst **51** at 12² |
| the ceiling holds | `setBrightness(9)` clamps to **1**, `exposure` **1.90** |
| dropping it back restores the calibrated frame | residual mean **0.00**, worst **0** |

The instrument needed no measuring for once: exposure regrades every pixel, so the 12² whole-frame
signature that was too coarse for R-A1's roadway gives **49.40** here against R-A1's **0.29** at
the same grid. Floors are set at roughly a third of the measured figures.

**THE FINDING IS THE THIRD ROW, AND IT IS ABOUT R-A1 RATHER THAN ABOUT LIGHT.** `exposure` is the
first reading on the test harness whose expected value **moves**, and the first thing it reported
was `0.95` on a frame that had just changed by 45 counts. The cause is in `main.js` and its own
comment had already named it: `Object.assign` **invokes a getter and copies the value**, so any
`get x()` written inside the big `Object.assign(api, {…})` literal is frozen at its boot-time
answer. `get roadAid()` shipped inside that literal with R-A1 yesterday and has been **a constant
0 ever since**.

**Both of R-A1's readback assertions expect 0** — off at boot, and back to 0 when dropped — so a
frozen 0 passed both of them, and the third assertion reads a frame signature and never touched
the getter. **The road aid itself was always live**; the thing that was wired to nothing was the
report of its position. That is R-A1's own finding one level in: *an assertion that can only ever
see one value is not an assertion*, and the way to catch it is a reading whose right answer
changes. `roadAid`, `brightness` and `exposure` are all defined in the `Object.defineProperties`
block now, the smoke asserts the road aid **reads back 1** when it is raised, and the rule is
written where the mistake was made: anything whose answer changes after boot is defined there, and
a getter in the literal is a frozen snapshot.

### Not claimed

- **The desktop half of the smoke was not run** — ~13 min against this runner's 10-minute
  per-command ceiling (ROADMAP § THE RUN BUDGET). Mobile 390×780 on the published mirror is
  **232 passed, 2 failed**, and **both failures are `dev`'s own**: `the roads reach the screen
  from the air, at the aerial anchor` (the gate R-BUG5b / #201 merged with and wrote up) and
  `…from the walker's eye, down an open street` (the gate T-V2 / #135 merged with and wrote up).
  Measured rather than assumed — `origin/dev` at `51655e65`, same runner, same command:
  **229 passed, 2 failed**, the same two assertions. The +3 is exactly this parcel's three new
  gates: it adds no failure, and it weakens no threshold, band or station. The road-aid gate got
  **stricter**.
- **No accessibility standard is claimed to be met.** This is a viewing aid, not a conformance
  statement, and nothing here measures it against WCAG or any other bar.
- **No liberty was taken and no confidence moved.** `docs/LIBERTIES.md` is untouched: the default
  rendering is unchanged, and the aid makes no claim about 1835.
- **It does not discharge R-W1 or R-M1b.** PR #125's road-gate failure occurs at the *default*
  setting, and a preference control does not change it — K24's box said so on 2026-08-14 and it is
  still true.

## Measured 2026-08-17 — the two layers nobody had ever read back are not mirrored, and neither half of R-BUG5b's instrument transferred

**ROADMAP K50**, opened by R-BUG5b. Nothing a visitor can see changed today; this is the gate that
tells the next parcel whether it moved a building where it meant to. It carries the visible-progress
rule's third exemption, and the parcel it unblocks is named below rather than implied.

### The answer

| layer | population read back | anchors outside their own drawn footprint | nearer to their MIRROR |
|---|---|---|---|
| `buildings.js` | 331 structures unioned from 1,310 instances · **533,346 vertices** | **0**, worst **0.00 m** | **0** |
| `streets.js` | **19,372 vertices** · 3 meshes · 17 centrelines | **0** off every centreline, worst **0.00 m** | not a discriminator — see below |

Measured on the PUBLISHED mirror at 1280×800, through the instance matrices the renderer hands the
GPU, and compared against the DATA — a structure's `placement.local_e/local_n` in its sidecar, a
street's `path_local_enu_m` — never against another number the renderer computed. The ground half
was already answered twice (the drawn surface against `heightfield.bin` at every field sample, and
`tools/measure_terrain_horizontal.mjs` on its two horizontal axes) and `flora.js` was measured clean
by R-BUG5b itself. **All four layers R-BUG5b named are now answered.**

### Three findings, and two of them are about the instrument

**1. A per-INSTANCE box is not a building, and the first reading of this census reported 279 of
1,310 bodies misplaced.** A structure joins one batch per material it uses, so any one instance is
walls, or roof, or trim. Judging a building by one of its materials gave a **21 % false-positive
rate on a town that is entirely correct**, worst 24.45 m on `fort_dearborn_palisade`. `buildings.js`
`instanceBounds()` warns about precisely this in its own comment, for precisely the reason a size
gate once passed a town of collapsed boxes. **Any new gate on this layer that does not union per
structure id is measuring a material, not a building.**

**2. The mirror test does not discriminate on a street grid.** Asked whether a drawn road vertex is
nearer to a street at its mirrored northing, it answered *yes* for **3,975 of 19,372** vertices on a
build where every vertex is inside its own track. Reflect a point across an east-west line in a grid
town and it lands on another east-west street; and a vertex at the EDGE of its own track scores
worse than a mirror landing mid-track, by construction. So the streets gate is the **half-width test
alone** — which a mirrored ribbon cannot pass, because a reflected road runs where no centreline is
recorded — and the mirror figure is printed as a diagnostic that gates nothing. R-BUG5b's question
transferred; its instrument did not.

**3. The gate was proved RED before it was believed.** `--refute` injects R-BUG5b's exact fault into
the live scene — the sign of each instance matrix's z translation, the sign of every drawn road
vertex's z — and re-runs the same census code:

| | clean | fault injected |
|---|---|---|
| buildings outside their footprint | 0 of 331 | **329 of 331**, worst **1,238.89 m** |
| buildings nearer their mirror | 0 | **324** |
| road vertices off every centreline | 0 of 19,372 | **15,397**, worst 222.30 m, **5,010** off the grid altogether |

The two buildings that survive the mirror are the two standing on the datum's own east-west line,
which is arithmetic rather than a hole in the gate. This is R-A1's finding one parcel on: *an
assertion that can only ever see one value is not an assertion.*

### What it unblocks

**`K30(c)`**, the queue's #1 SEEN pick — *29 buildings on eight streets are drawn standing in the
roadway; redraw the bodies onto the correct side of their own frontage.* It changes where 331 bodies
are drawn relative to their records, and **until today no gate in this project read the buildings
layer's geometry back at all**. Its before-picture is here: worst anchor-outside-footprint
**0.00 m**, worst anchor-to-nearest-corner **47.11 m**.

`tools/drawn_placement_census.mjs` holds the census; `tools/measure_drawn_placement.mjs` runs it as
an instrument in about a minute at one viewport; `tools/smoke_renderer.mjs` runs the same function
as two release gates at both viewports. One module, because a gate that paraphrases its instrument
can pass a build the instrument fails.

## Fixed 2026-08-17 — scene detail did nothing to the wood, and the only thing it did do was halve the willow screen

**ROADMAP K45(b3)**, opened by K45(b2) finding 2. The Settings panel's scene-detail control offers
`full` / `balanced` / `light`, and a phone starts at `light`. K45(b2) had already worked out that
the control could not be moving the timber — the acceptance roll is `perHa · step² / 10000`, so a
coarser grid visits proportionally fewer cells and accepts proportionally more at each, and the
`STEMS` caps that were the only other difference had never bound. This parcel measured it, and
found a second fault nobody had asked about.

### What the three levels actually planted, measured on `dev` before a line changed

`tools/measure_timber_detail.mjs`, new here, walks the visitor's own `setDetail` through all three
levels on the PUBLISHED mirror and asks two questions of each — how many stems, and **how far north
do they reach and in what shape**. The second question is the one a stem count cannot answer: a
truncated wood and a thinned wood can plant the same number of trees.

| level | trees | stools | stems | timber tris | scene tris |
|---|---|---|---|---|---|
| `full` | 472 | 258 | 730 | 186,442 | 511,919 |
| `balanced` | 470 | 190 | 660 | 161,674 | 466,814 |
| `light` | 437 | 133 | 570 | 136,382 | 416,222 |

**472 / 470 / 437 is one wood planted three times** — the spread is a near-Poisson draw's, 1.6 σ,
not a control's. And **258 / 190 / 133**: the sandbar-willow point-bar screen was losing 52 % of its
stools at `light`. That branch rolls a *fixed* per-cell chance, so unlike the tree roll it is not
count-neutral in the sampling step. The screen is the one population in this file that must not be
thinned, and its own comment says so four lines above the roll doing the thinning: *"a screen needs
its clumps to touch … thinning these to half was what left them standing as separate cushions on
open sand."* **A comment that states an invariant is not a gate.**

### The repair, and what it costs

`keep` is a fraction on the tree acceptance roll — **1 / 0.80 / 0.60**, which is the levels' own
triangle ceilings in `main.js` (1,000,000 / 800,000 / 600,000) read as a ratio. That ratio is an
invention and is recorded as **L121**, with the alternative named and rejected in writing: the
pre-K45(b2) caps' ratio (1 / 0.634 / 0.366) is not used because those caps *never bound*, so they
are an intent nothing ever executed. The thicket roll now scales with the cell it is offered
(`min(1, 0.84 · cellArea / 16)`) and deliberately does **not** take `keep`.

| level | trees | stools | stems | timber tris | scene tris | northernmost stem |
|---|---|---|---|---|---|---|
| `full` | 472 (=) | 258 (=) | 730 (=) | 186,442 (=) | 511,919 (=) | N +397.7 m |
| `balanced` | **373** | **232** | 605 | 156,358 | 453,026 | N +396.4 m |
| `light` | **257** | **182** | 439 | 115,234 | **370,738** | N +391.8 m |

`full` is unchanged to the stem — every banked figure in this repository is `full`'s. `light` sheds
45,484 scene triangles (−10.9 %) and keeps the north end of the wood.

### Unverified, and stated

- **The screen does not fully recover at a coarse step, and is not tuned to.** A probability cannot
  exceed 1, so both coarser steps clamp: `light` reaches 182 of `full`'s 258 stools (70.5 %) and
  stops, because a 6–9 m point bar sampled on a 5.6 m grid has fewer points than the screen wants
  stools. Closing the rest needs sub-cell sampling on the bar and is not this parcel's.
- **The 1 / 0.8 / 0.6 ratio is borrowed, not measured.** No frame-time measurement on a real phone
  exists here. The ceilings are the honest stand-in and L121 says how to replace them.
- **No claim is made about `light` looking *right*.** What is asserted is that it is the same wood
  at a lower density rather than three quarters of one, and the gate asserts that as reach and
  distribution rather than as an opinion about a screenshot.

### Verified

`./tools/check.sh` PASS (21 s). `node tools/measure_timber_detail.mjs --gate` — **17 assertions, 0
failures**, on the published mirror. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` at 390×780 — the release gate at the viewport this parcel is SEEN on. **Not claimed:
the desktop half**, ~13 minutes against this runner's ten-minute per-command ceiling; the
measurement table above was taken at 1280×800, which is the viewport the parcel does not change
(`full` is unchanged to the stem).

## Fixed 2026-08-17 — the owner's floating flowers, and four repairs that computed the right number and had it thrown away

**R-BUG7, owner-reported 2026-08-16 with a photograph.** Yellow flower heads hanging above the
horizon over South Water Street on stalks that stop in mid-air. It was the **fifth** time this
symptom had been repaired in `renderers/web/js/flora.js` and the first time anything asserted it.

### What was wrong

`maybeHead` computes `tiltAz` so a head's stalk leans back to its own stem, and then passes a
**random `yaw`** into the same `push` call. `push` composes the instance rotation as a `YXZ` Euler,
so that yaw is an `Ry` applied *outside* the tilt — it spins the leaning head, and its azimuth with
it, to a uniformly random bearing. **`push`'s own docstring says to pass `yaw` 0 alongside a tilt.**
The yaw was not even needed there: the vertex program already spins a head about its own axis off
`aFlora.w`, so it was being applied twice and the second application was the fault.

That is why four prior repairs each closed a real mechanism and none closed this. Every one of them
computed a bearing that a later line discarded. **The two live suspects the parcel had queued are
both refuted**: the ring fade is monotone — the head ring reaches zero exactly where the plant's
ramp passes 0.35, so head fade ≤ plant fade at every distance — and the fault reproduces looking
down a dry street, not only across water.

### The numbers, landed red on the unmodified `dev` build first

`tools/measure_head_support.mjs`, published mirror, desktop, eight scene anchors × four bearings.
It reads the instance buffers back and asks whether each drawn head's stalk foot lands inside a
drawn plant's body, under its drawn top.

| | before | after |
|---|---|---|
| drawn heads with nothing under them | **38 of 11,752** | **0 of 11,735** |
| poses carrying a fault | 8 of 32 | 0 |
| stalk foot → nearest stem, median / p99 / worst | **21 / 234 / 582 mm** | **0 / 0 / 0** |

All 38 are `corymb` — the one architecture with both a wide tilt band and up to twenty heads per
plant, so its half-metre offset cap is large enough for a random bearing to miss the whole plant.

### The repair is a change of anchor, not a fifth aim

Head archetypes are now built with their origin at the **foot of their own stalk**, the instance is
pushed **on the stem** at the height its branch leaves it, and the tilt swings the head out about
that point. The offset from the stem is therefore *generated by* the stalk rather than being a
second number that has to agree with it — `r`, `spread` and a `0.94` fudge are gone from
`maybeHead`. And because `foot ≤ plantH` and the shader scales both by the same ramp, the stalk's
foot is under its plant's top **at every fade**: an invariant, not a number measured at one pose.
That second, quieter detachment — the lateral offset not shrinking with the fade — is what the
first cut of the repair left behind at 1 of 11,735, and it is gone.

### Verified

`./tools/check.sh` PASS. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` — the new
assertion *every drawn flower head has a plant under its own stalk* passes at 390×780, with the two
road-contrast bands still red exactly as R-W1 and T-V2 recorded them and no other failure.
**Not claimed: the desktop half**, which is ~13 minutes against this runner's ten-minute
per-command ceiling. The measurement above was taken at 1280×800, which is the harder viewport.

## Shipped 2026-08-17 — there are trees on the lakeshore sand, and the sward decided where

**ROADMAP K45(b4)**, the last of K45(b)'s three changes. `z08_lakeshore` records three trees for
the open dune — the eastern cottonwood in its dune form at 3–15/ha, the quaking aspen and the
balsam poplar at 2–8 each, all `attested` off the MNFI open-dune survey and Cowles 1901 — and no
community mix could choose any of them, so the beach carried no woody stem. **88 poplars now stand
on 4.30 ha of dry lakeshore**: 42 cottonwood, 23 aspen, 23 balsam poplar, against 41.7 / 23.2 /
23.2 expected from the weights.

**The stand density is derived, which is a first here.** ZONE 8 gives no canopy figure, because a
dune has no canopy — so `perHa` is **[7, 31]**, the sum of the three recorded bands, and each mix
weight is its own record's midpoint. At the middle of that range the draw plants 9 + 5 + 5 per
hectare, which is each record's own midpoint reproduced exactly.

**Where they stand is `flora.js`'s answer, not `trees.js`'s.** Every other woody community here is
selected from the heightfield, and a dune cannot be: what makes it a dune is the substrate. The
sward already resolves ten overlapping zone extents by priority to decide which grass a visitor is
standing in, so the timber asks it. The wood stands on the sand that is DRAWN, and moving the zone
moves both together. `trees.js` still reads no extent of its own.

| | before | after |
|---|---|---|
| stems on the lakeshore | **0** | **88** on 4.30 ha |
| trees in the near field | 373 | **472** |
| flora records reaching no reader | 6 | **2** |
| unreached (record, figure) pairs | 301 | **261** |
| placed species drawn as another species | — | **0** |
| timber triangles / draw calls | 167,830 / 4 | **186,442 / 5** |

### Three findings, and the first one shrinks the parcel that follows it

**1. The 40.2 ha banked as swept-and-refused was never 40.2 ha of woody omission.** Broken down
through the sward's own classifier: **4.30 ha is lakeshore and 33.6 ha is `z09_sand_prairie`**,
whose record carries no tree at all — its only woody entry is the bur-oak grub, a `shrub_low` no
woody reader takes. Five sixths of the refused ground is refused by the dataset, not the renderer.

**2. `SPECIES` is keyed by species id, and that breaks the first time a species is recorded twice.**
`populus_deltoides` is the gallery's 22–30 m emergent AND the dune's 5–15 m half-buried leaner. The
loader took the first zone to name a species, so the beach was one line from being planted with
twenty-five-metre floodplain cottonwoods — read, routed, banded, gated, and drawn as another zone's
tree. `ARCHETYPE_BY_ZONE` + a community's `specsFrom` fixes it for the lakeshore only; the general
form would redeal every community's specs and is its own parcel.

**3. A gate that scans one table reports a false finding when a second table appears.**
`measure_planting_reach.py` convicted both new poplars of being drawn with the elm's bark while
their own archetypes sat committed three hundred lines above. It reads the second table now, per
community, and the bank is 0. Separately, `measure_flora_reach.py` had a self-test case that named
`z08_lakeshore` as its example of an unrouted zone — a control whose fixture was the defect, so
repairing the defect turned it red. That is the third of that shape in four days.

**Still not planted, stated rather than left to be found:** ZONE 8c's willow scrub — `salix_cordata`
at 15–50 clumps/ha, red-osier, juniper, sand cherry — is `shrub_low`, a role no woody reader has a
cohort for. And the river's point-bar branch is now refused on the dune outright, because ZONE 8a
says the active beach is 85–98 % bare sand, *"do not vegetate this"*; measured, it caught 0 of the
dune's 2,687 dry nodes today and the nearest miss is 0.66 m.

### Verified

`./tools/check.sh` — **CHECK PASS**, before and after merging `dev`, with every moved bank
re-banked in the same commit: `planting_reach_baseline.json` (0 unselectable species, 5 timber
zones, 29 mix entries) and `flora_reach_baseline.json` (2 records, 14 figures). All three woody
gates' self-tests fire. It is the dev gate, and it passed in CI on the PR as well.

`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` — **237 passed / 2 failed** on
this parcel's own tree, and **237 / 2 with the same two road-contrast checks and the same numbers**
on a clean `origin/dev` worktree run the same way. The failures are the queue's, not this parcel's.

**Not claimed, and the second half of this is new:** the desktop half of the smoke (~13 min against
a 10-minute per-command ceiling) — and, after merging `dev` and its R-W1 lighting, **the mobile half
too**: the post-merge run was killed by the ceiling at 230 passes, same two failures, no page error,
with seven interaction and vendor checks unreached that all passed pre-merge.
## Landed on `dev` 2026-08-16 — the town was lit by a sky that does not exist, and the honest sky costs the roads

> **⛔ NOT FOR PROMOTION.** `dev` may carry this; `main` may not, until the owner has walked the
> `/dev/` preview and approved the look, or **R-W2** has bought the road contrast back. The next
> promotion reads ROADMAP § R-W1's release-condition box first and reverts this parcel rather than
> shipping it unreviewed. One number is why: **`south_water` 250–600 m, 71 % → 16 %.**

**Built 2026-08-14, parked three days on one smoke assertion, rebased onto `dev` at 836fa84 and
re-measured tonight.** `world.js` and `flora.js` auto-merged with everything that landed in between,
and `main.js` is untouched, so R-BUG1's altitude near-plane is intact.

### The finding stands, and it is worse than "one assertion short"

The sky over this reconstruction and the light falling on it were two different skies. Measured on
an upward-facing white Lambertian card, sun excluded, on the rebased branch:

| fill | luminance | R/B retention, white card facing north |
|---|---|---|
| the old `HemisphereLight` rig | **1.4047** | 85 % |
| this sky's own PMREM | **0.7484** | 78 % |

**1.9× the luminance and about 2.9× the red of its own sky.** Every calibration this project has
made — the sward's density, the wall colours, the crown contrast — was taken under a fill that
contradicted its own backdrop. Scaling the sky up to hold the old total was built and measured
before being rejected: it takes retention to **62 %**, which is the documented failure reached from
the other side.

### What it buys

Literal black pixels reach **zero at all three metric stations** — `river_bank` 12,063 → 0,
`first_post_office` 11,015 → 0, `prairie_south` 2,315 → 0 — and the decile L\* rises everywhere,
nearly doubling at `river_bank` (0.93 → 1.78). §1 item 11 retired, item 7's "no literal (0,0,0)"
half with it.

### What it costs, in the place that is already sore

The scene is ~16 % dimmer, so road contrast falls almost everywhere. Mobile, published mirror,
honest denominator (R-M1c):

| station · band | `dev` | R-W1 | |
|---|---|---|---|
| `south_water` 40–100 m | 87 % | 80 % | −7 |
| `south_water` 100–250 m | 52 % ✗ | 33 % ✗ | −19 |
| **`south_water` 250–600 m** | **71 % ✓** | **16 % ✗** | **−55** |
| `from_above` 100–250 m | 85 % | 78 % | −7 |
| `from_above` 250–600 m | 53 % ✗ | 50 % ✗ | −3 |
| `lake_market` 40–100 m | 100 % | 93 % | −7 |

### The third instrument finding of the evening, and the suite handed it over silently

**229 passed / 2 failed before. 229 passed / 2 failed after.** Identical, because `south_water` was
already red on its *100–250 m* band, so a band collapsing from 71 % to 16 % **crossed no bar and
appears nowhere in the summary**. A reader comparing tallies would have concluded this parcel cost
nothing. The gate is per station; the measurement is per band. Opened as **R-M1d**.

That is three in one evening — R-M1c (an occluder could raise a score), R-M1d (a band can collapse
in silence), and R-BUG7's finding that four repairs to a drawing have never been asserted at all.

### The conclusion, stated rather than deferred

**R-W1 is correct and premature.** It belongs with or after **R-W2**'s textured coverage, which is
what buys the contrast back. Landing it ahead of R-W2 trades a documented, owner-reported defect —
the far road down a street — for a less-visible correctness win. It is on `dev` and out of
production so that trade is visible to the person entitled to make it, rather than sitting a fourth
day on a branch nobody can look at.

### Desktop, measured — the assertion this was parked on in the first place

`desktop 1280×800`, published mirror: **226 passed, 2 failed**, and it is the same two stations.
`from_above` 250–600 m reads **54 %** — the assertion that parked this parcel on 2026-08-14 is
still the one that fails.

| desktop · band | R-W1 |
|---|---|
| `south_water` 2–40 m | 70 % ✓ |
| `south_water` 40–100 m | 67 % ✓ |
| `south_water` 100–250 m | 52 % ✗ |
| `south_water` 250–600 m | 37 % ✗ |
| `from_above` 100–250 m | 81 % ✓ |
| `from_above` 250–600 m | **54 % ✗** |
| `lake_market` (all five) | 70 / 87 / 95 / 100 / 100 ✓ |

**The desktop DELTA is not claimed.** `dev`'s own desktop baseline was not taken, so these are
R-W1's absolute figures and not a before/after. Only the mobile comparison above is a delta.

**Not claimed:** the mobile critic set, the other eight stations, and the `--published` critic run.
`docs/RESEARCH` still has no committed reference photograph for RENDERING §5 note 1, so these
numbers are internally consistent and not anchored to a photograph.

**The finding.** `renderers/web/js/world.js` calibrates its sky twice over — an exposure and
a horizon fit, both least-squared against a verified July photograph of Illinois prairie —
and then lit the town with something else entirely: a `HemisphereLight(0xa8c4e0, 0x7a6b4e,
2.4)` plus a second at 0.20, colours and intensities nobody had ever checked against the sky
they stood for. Measured with the new instrument, on an upward-facing white Lambertian card,
sun excluded:

| fill | R | G | B | luminance |
|---|---|---|---|---|
| the old hemisphere rig | 1.0440 | 1.4565 | 1.9535 | **1.4047** |
| this sky's own PMREM | 0.3663 | 0.7916 | 1.5492 | **0.7558** |

**1.86x the luminance and 2.85x the red of its own sky.** Not a tuning error — a fill and a
backdrop that had never been in the same measurement.

**The instrument.** `tools/light_probe.mjs` (new, ~9 s) borrows the live page's renderer and
lights, renders white and documented-colour Lambertian cards on six axes into a LINEAR float
target with tone mapping off, and reports irradiance and albedo retention. It measures the
RIG, upstream of ACES, the sRGB encode and the sky — a frame cannot tell you whether a wall
is pale because the light is blue or because the wall is. This is the white-card harness
RENDERING §4 W1 asks for, and it restores the page's renderer state and asserts that it did.

**What the environment fixed, desktop, at the three worst stations.**

| station | literal black px | decile L\* | crown G−B |
|---|---|---|---|
| `river_bank` | 12,063 → **0** | 0.93 → 1.78 | 47.8 → 33.7 |
| `first_post_office` | 11,015 → **0** | 5.35 → 6.20 | 12.2 → 15.7 |
| `prairie_south` | 2,315 → **0** | 7.09 → 7.97 | 19.9 → 10.7 |

RENDERING §1 **item 11 is retired** and **item 7's "no literal (0,0,0)" half with it**; item 8
holds at every station. Downward-facing fill is up 30 %, because the ground half of the
environment is derived from the light actually falling on the ground rather than being a
colour with an intensity beside it.

**What it cost, stated rather than discovered later: the scene is 16 % dimmer.** Holding the
old total illuminance was built and measured before being rejected — it needs the sky scaled
1.858x, and a real sky is blue (the calibrated zenith is B/R 4.2), so scaling it until it
carries a warm lamp's luminance collapses albedo retention:

| rig | log wall R/B retained against a white card in the same light |
|---|---|
| the old hemisphere fill | 85 % |
| this environment, own magnitude | 76 % |
| this environment, scaled to hold illuminance | **62 %** |

62 % is the 2026-08 failure arrived at from the other direction, so the environment is
installed at its own magnitude and there is no invented scalar anywhere in the fill.

**What did not clear, and it is not the light.** The decile target of L\* ≥ 14 is out of
reach of any rig. `CROWN_SHADE_FLOOR = 0.060` in `trees.js` folds a crown's self-shadowing
into its own vertex colour, so an interior leaf's albedo is the record's foliage green times
0.06 — **0.24 % reflectance**. At a floor of 1.0, meaning no self-shadowing at all, that
surface still reaches only L\* ≈ 12 here. R-G1 established the metric reads canopy rather
than shadow; this adds that the canopy is dark in the ALBEDO, where light cannot reach it.
The lever is `CROWN_SHADE_FLOOR`, and it is a separate calibration: that constant's committed
check is the Weber contrast the reference photograph's tree mass holds, 0.625 against 0.655
here.

**Why it is parked.** `tools/smoke_renderer.mjs` reports **403 passed, 4 failed**. Three were
an unstamped changelog and are stamped. The fourth is real and is named in ROADMAP R-W1:
**`the roads reach the screen from the air, at the aerial anchor`**, R-BUG2's own gate from
yesterday. `south_water` still passes. The gate was not weakened and will not be.

**Also on the branch.** `tools/critic_shots.mjs` takes `--stations a,b,c` so a phase can see
a number in three minutes instead of twelve; unknown ids fail loudly, and the baseline runs
pass no filter. `flora.js` now reads the sky fill from `scene.userData.chiSkyFill` rather
than by sniffing the light list — three applies `scene.environment` to physical materials
only, so the Lambert sward would otherwise have been left lit by a fill the town no longer
has, which is the same class of error flora.js already traverses for the sun to avoid.

**Not attempted, and not measured:** the mobile viewport's critic set, and the eight other
critic stations. Only the three named above were re-shot. The published `--published` critic
run was not taken either. Nothing here should be quoted as a whole-scene result.


## Shipped 2026-08-17 — the town's animals were researched, graded, cited, and read by nothing

**ROADMAP K51**, from K42 finding 2. `data/fauna/` holds **139 animal records across ten habitat
zones**, every one stated for 1 July 1835 rather than for the year, every graded claim carrying its
reasoning and its sources. No file under `renderers/` named the directory. `tools/publish.sh` did
not copy it. **A browser had never been offered the layer**, while `data/scenes/1835.json` listed
`fauna` among the scene's layers and `docs/LIBERTIES.md` L2 described how sparsely that wildlife
was *rendered*.

It is now the Evidence panel's **What was living here** section, and nothing about the 3-D scene
changed: no animal is drawn, no animal geometry is proposed, and the standing constraint on
depicting people is untouched. The section says so in words, and the smoke asserts the sentence.

### What a visitor gets

Ten habitats in the manifest's own order; inside each, its `reads_as` sentence, what the dawn
chorus does there on this date, whether its ground is drawn in this scene at all, and every species
grouped in the manifest's class order. Each animal opens to its July status, whether it would be
seen, heard or found only as sign, how many, what it would be doing, what it would look like, its
voice in July, the sign it leaves — and the reasoning and citations behind the three graded claims,
rendered by the same `citations.js` the building card uses.

| | before | after |
|---|---|---|
| fauna figures reaching a visitor | **0 of 30** | **30 of 30** |
| the whole flora+fauna dataset, unread | **58 of 100** | **28 of 100** |
| `data/fauna`'s share of the unread bank | **30** | **0** |
| habitats on the card / in the layer | — | **10 / 10** |
| species on the card / in the layer | — | **139 / 139** |
| citations rendered on the section | — | **54** |

### Three findings, and none of them is about animals

**1. K42's gate fired exactly as designed.** Its assertion 3a fails the moment a layer with no
declared reads gains a reader, *"because the whole of this layer's unread bank rests on nobody
opening it"*. Opening the directory turned the whole dev gate red on the first commit, and the
thirty figures had to be classified in the same commit rather than riding on a sentence that had
expired. A gate written against an absence has to name the event that ends the absence.

**2. Two of that gate's own controls were written against the repository's state.** The self-test
asserted `not layer_is_opened(src, "fauna")` and built its 3a case by setting `opened["fauna"]`.
The first became a second copy of the measurement; the second could no longer be constructed and
printed **SILENT** rather than failing — the quieter of the two ways a control dies. Both are
synthetic strings now. That is the sixth green reading on this project taken from an instrument
pointed at nothing, and the first where the instrument was a self-test.

**3. L2 said "ambient wildlife is rendered sparsely" and nothing was rendered.** Not sparsely:
none. Its 2026-08-11 revision added a paragraph of measured detail about a dataset no renderer had
ever opened. L2 now states what the renderer does and keeps the decision as standing intent.

### Verified

`./tools/check.sh` — **CHECK PASS**, with the publish-sync gate carrying a new `COPIES` rule for
`data/fauna/` (it caught the eleven published files that traced to no source, which is the rule
working). `tools/measure_layer_reads.py --gate` and `--self-test` green.
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` — see the PR for the count.

**Not claimed:** the desktop half of the smoke, ~13 min against this runner's 10-minute
per-command ceiling. The section was photographed at 1280×800 by hand and reads correctly.
## Fixed 2026-08-16 — the woody planter sweeps the modelled field, and the timber has the east end its own source gives it

**K45(b2)**, the second of K45(b)'s two changes. The planting loop's fixed square —
`const half = 320 - step`, E/N −316..+316, left over from the 640 m heightfield this scene began
as — is replaced by the heightfield's own extent inset by one planting step. **Reach goes from
52,163 to 189,700 of the field's 192,844 dry nodes: 27.05 % → 98.37 %**, and the 87.9 ha the timber
layer had never offered a stem to is **2.0 ha of one-step rim**. **147 stems stand east of the old
edge where one did**; 377 stems became 640.

**Ground the loop reaches is not ground a wood may stand on, and the classifier had no eastern
answer at all.** `communityAt` asks distance-to-water, so on the beach the lake is water and the
gallery mix — silver maple and elm — would have been planted on open sand. Andreas ends both
divisions in the sentence `z05_riverbank_timber` is already built from: the South Side belt runs
*"east as far as Wells Street"*, the North Side's timber excepts *"the sandy hills near the lake"*.
There is now one east limit per division, **read at load from `data/streets/1835.json`** — Wells at
**E +329.3**, State Street at **E +825.8**, the break-of-slope where `z09_sand_prairie` starts the
relict beach ridges. **64,385 nodes, 40.2 ha, are swept and refused**: a stated omission where an
unstated one stood. The dune community that belongs there is K45(b) change one and is not built.

**`z05_riverbank_timber`'s own note put Wells Street 440 m east of where it is.** The committed
centreline runs E +328.1 to +330.5 — **nine metres** east of the 640 m box's edge, not 440. The
conclusion the note drew survived, on nine metres of margin rather than four hundred, and a belt
read as running 440 m past the box would have licensed a gallery over the beach ridges the moment
the planter widened. Corrected in the record and in the manifest. Three other flora zone notes
state distances of the same shape and none has been checked.

**The timber's detail control has never done anything, and widening the sweep turned that from
harmless into a defect.** `step` is count-neutral by construction, so the `STEMS` caps are the whole
of the control — and at 163 trees they had never bound. Widened, `light` plants **387 trees and the
cap bound at exactly 300**. That is not a thinning: the loop runs south to north, so a bound cap
deletes the north end of the wood and leaves a straight edge, on phones, which start at `light`.
Caps raised by 3.70× (the ratio of ground now swept) and **a bound cap is now a `problems` entry**,
which the release smoke reads as a failure. The real repair — a keep fraction rather than a cap —
is ROADMAP **K45(b3)**.

**Cost, measured at 1280×800 rather than estimated:** load **1.98 s → 2.13 s**, timber triangles
**108,804 → 175,136**, whole scene **~393k → 459k** against a 1,000,000 budget, **draw calls
unchanged at 59** against ≤ 80. The four quadrant buffers are now 2 km wide, so culling is coarse —
free at 175k triangles, the wrong shape at 500k, and a tiled chunker trades draw calls for it.

**Not tuned to look better:** no mix, weight, density, confidence or archetype moved. But the wood
is dealt from one seeded stream in sweep order, so a wider sweep **redeals every stem in town** —
same rules, same expected counts, different individuals.

**Verified:** `tools/check.sh` green; `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs
--published` green. **The desktop half of the smoke was not run and is not claimed** — ~13 minutes
against this runner's 10-minute per-command ceiling.

## Measured 2026-08-16 — the road check could be passed by planting a tree in front of the road

**ROADMAP R-M1c.** **Nothing a visitor can see changed today**, and the exemption claimed is the
third one: this is a gate on nothing less than every road-contrast percentage this project has
quoted, and it is the parcel that unblocked a queue of four.

### What was wrong

`roadContrast()` scored `perceptible` as `ds.filter(d >= 2).length / ds.length`, where `ds` runs
over the probes the marker pass could see **through** the vegetation. A stretch of road standing
behind a tree left the sample instead of failing in it, so **anything that occluded a faint road
raised the score.**

### The proof is the stability, not any one number

One band, three builds, the same evening, the same runner, mobile, published mirror. The only
difference between the columns is what the near-field wood is doing:

| aerial anchor, 250–600 m | wood mirrored (`dev` 3ea4e00) | repaired (R-BUG5b) | widened (K45(b2)) |
|---|---|---|---|
| probes **seen** | 157 | 177 | 163 |
| probes **bare** | **182** | **182** | **182** |
| readable stretches | ~97 | ~96 | ~96 |
| score over `seen` — the old one | **62 %** passes | **54 %** fails | **59 %** passes |
| score over `nBare` — this parcel | **53.3 %** | **52.7 %** | **52.7 %** |

**The old score swung eight points three times while the number of readable stretches never moved
off ninety-six.** The build carrying a bug that drew the entire wood on the wrong side of the river
scored **highest of the three**, and K45(b2) — parked on `hold` since 2026-08-16 for *costing* this
band two points — would have gone **green by planting more timber in front of the same road.**

### The instrument was already built, already printing, and already carried the diagnosis

The `shotMF` pass photographs the same probes with the sward and the trees hidden. Its own comment,
written two parcels ago, states this finding in full: *"A probe marked here but not in `shotM` is a
road that is ON SCREEN and COVERED BY VEGETATION, **which the marked-only denominator drops instead
of failing**."* It was built as a diagnostic, `nBare` has been printed in every band line since, and
**nothing ever divided by it.**

### Why `nBare` and not `nProjected`

They are different claims about what a visitor is owed. A road behind a store is a road a visitor
legitimately cannot see, and scoring on `nProjected` would demand X-ray vision through the town's
own buildings. Vegetation is ours, it moves when we change it, and it must not be able to launder a
faint road out of the sample. `seen ⊆ bare` always, so this can only ever **lower** a score — it is
not a route through a bar, and it did not become one.

### What moved, measured at every station

**Exactly two figures in the whole suite**, and only one of them is gated:

| | before | after |
|---|---|---|
| `from_above` 250–600 m (**gated**) | 54 % of 177 seen | **53 % of 182 bare** |
| `from_above` 600–4000 m (reported only) | 96 % of 111 seen | 71 % of 151 bare |

Everywhere else `nBare == seen`, so nothing changed: `south_water` still reads 90 / 87 / 52 / 71 and
`lake_market` still reads 60 / 100 / 100 / 98. **The suite is 229 passed / 2 failed — the same two
failures, and the same verdict, as `dev`.** This parcel flips nothing. It makes one number honest
and takes away the way to bribe it.

**`ROAD_MIN_PERCEPTIBLE` was not moved**, and the aerial band is still under it — which is the real
state of that stretch of road and always was. Its fix is **R-W2**'s textured coverage; its ceiling
is 4.8 L\* opaque, so the contrast is there to be spent.

**Not claimed:** the desktop half of the smoke (~13 min against the 10-minute per-command ceiling).
Every road-contrast percentage quoted in this repository before today was taken on the old
denominator and is not comparable with one taken after it.

## Shipped 2026-08-16 — the South Water viewpoint stands in South Water Street, and the far-band collapse it was parked for does not reproduce

**ROADMAP T-V2**, built on 2026-08-15 and parked on `hold` PR #135 for two days. The anchor a
visitor is offered under the name **South Water Street** — the business street of 1835 Chicago —
stood at **(260, −95)**: 101 m south of the committed centreline of the street it is named for, in
a field, with that street a band of roofs on the horizon and about 60 % of the frame grass. It now
stands at **(329.8, 7.0)**, in the street at the Wells corner, looking east.

**Neither half of the coordinate is new evidence.** The easting is the Wells junction the sixteen
South Water records are themselves offset from, quoted verbatim in their own position notes; the
northing is `data/streets/1835.json`'s South Water centreline at that easting. A camera is not a
placement: no building moved, no dimension changed, no confidence tier changed anywhere.

### The parcel was parked on a measurement that has since stopped being true

The `hold` said the far band **collapsed to 0.5 L\* and 30 % perceptible** when the camera moved
into the street, and asked whether a threshold set against an oblique view should be asserting
250–600 m of road seen down its own length. **Re-measured on today's `dev` (c701833), that band
reads 2.1 L\* and 71 %.** R-BUG3's near lift, R-BUG5b's wood and R-A1 all landed in between. The
question the parcel was held for was answered by other work while it waited.

### What the move is actually worth, and it is the R-M1c fault again

Mobile 390×780, published mirror, same runner. `nProjected` is how much of that band's road is in
the frame at all; `n` is how much of it the marker pass can see:

| `south_water` band | old stand, in the field | new stand, in the street |
|---|---|---|
| 2–40 m | **not gated** — 1 probe projects | ΔL\* 4.1, **90 %**, n 10 of 10 |
| 40–100 m | ΔL\* 4.1, 100 %, n 28 of 34 | ΔL\* 3.5, 87 %, n 15 of 15 |
| 100–250 m | ΔL\* 3.7, 100 %, n 25 of **96** | ΔL\* 2.2, **52 %**, n 42 of **67** |
| 250–600 m | ΔL\* 15.8, 100 %, n **6 of 510** | ΔL\* 2.1, 71 %, n 100 of **423** |
| **gated probes PERCEPTIBLE** | **31** | **93** |

**The old stand scored 100 % on six probes of five hundred and ten.** The new stand shows
**seventy-one** perceptible stretches of that same band and scores 71 %. Across both gated bands the
street view puts **three times as much readable road** in front of a visitor — 93 stretches against
31 — and the gate records it as a regression, because `perceptible` divides by probes **SEEN** and
the field stand could not see 98.8 % of the band it was scoring. Scored on `nProjected`, the honest
denominator: **5.1 % → 19.0 %.**

This is the second independent demonstration of **R-M1c** in one evening, from a different station
and a different cause. R-BUG5b found it by removing an occluder; this finds it by pointing the
instrument at road it can actually reach.

### Landed with two bands red, neither of them this parcel's to fix

`the roads reach the screen from the walker's eye, down an open street` fails on **100–250 m at
52 %** against the 55 % bar — three points, on a station where the honest denominator says the move
*improved* both gated bands. `the roads reach the screen from the air, at the aerial anchor` also
fails and is **inherited from `dev` unchanged** (85 % / 54 %, identical to the digit) — R-BUG5b's
knowingly-red band, not this parcel's. **No threshold moved, no band widened, no station dropped.**
The bar belongs to R-W2 (coverage) and R-M1c (the denominator); **T-V2b is folded into R-M1c**,
because "a threshold set against an oblique view" turns out to be the same fault seen from the
other end.

**Not claimed:** the desktop half of the smoke, and the critic-shots baseline re-shoot the parcel's
own box asks for — `south_water` is a baseline station, so its row in the STATUS baseline table is
now measured from a different place and must be restated rather than compared. That is carried as
T-V2c rather than silently left as two incomparable numbers under one name.

## Fixed 2026-08-16 — the whole near-field wood was drawn mirrored, and that is why the trees were in the river

**ROADMAP R-BUG5b**, the owner's report reopened after #196 shipped a fix that did not change what
he could see. A visitor can see this one: from the south bank west of the forks, 4 ft up, ENE 076°,
the line of crowns across the main stem is gone, the North Side is wooded and the south bank of the
main stem opens out.

### What was wrong

`renderers/web/js/trees.js` asks every placement question in local ENU metres — `isWater(e, n)`,
`communityAt(e, n)`, `surfaceHeight(e, n)`, `cellAt(e, n)`, `blocked(e, n)`, `noteStation(e, n, y)`
— and then handed its ENU north straight to `addTree`, whose fifth argument is a three **world z**.
`terrain.js`'s `enuToWorld` is `(e, y, -n)`. **Every tree was tested at `(px, pz)` and drawn at
`(px, -pz)`: the entire near-field woodland mirrored about the datum's east–west line.** The repair
is a named `worldZ(n) => -n` at the two `addTree` call sites. No density, weight, band, seed or
waterline rule moved.

### The numbers, measured on the build in the owner's screenshot

**391** stations, **0** of them wet where the planter TESTED, **64** of the same 391 wet where it
DREW. **12,285 of 77,688** drawn vertices over the water mask, **10,734** of them more than 4 m
from dry ground, the worst **48 m** out — the middle of the channel. The proof of the mirror is a
pair of readings: the nearest station to a vertex read as ENU `n = -z` is **infinite**, and read as
`n = +z` is **13.1 m**, one crown radius.

### The finding, and it is not the sign

**Three gates agreed with each other and all three measured the same wrong thing.**
`wetTreeStations`, `drownedTreeStations` and `tools/measure_far_timber.py` all walk `stations` —
where the planter DECIDED to plant. That list is correct and always was. **Nothing had ever read
the drawn geometry back.** A gate on a placement is not a gate on a picture, and this is the sixth
time a green gate here has disagreed with the owner's window. `flora.js` had it right all along.
Two new smoke gates close it: *every tree drawn stands at its own station* (structural — it cannot
pass under a mirror) and *no timber is drawn out in the channel* (the report in its own terms).
**Both were demonstrated RED against the unfixed published mirror before the fix went in.** K50
opens the same question against `streets.js`, `buildings.js` and `ground.js`.

### The one red gate, and why the hold it was raised under does not survive being measured

`tools/check.sh` and the changelog contract are green, the two new gates went red on the unfixed
mirror and green on the fixed one, and the mobile smoke is **230 passed / 1 failed**. The one
failure is `the roads reach the screen from the air, at the aerial anchor` — the FLYING station.
**On foot both road stations are green**, so nothing a walker sees regressed. No street vertex
moved and every street gate is green.

This parcel was first parked on `hold` asking the owner to accept the red. **That question was
withdrawn on 2026-08-16 evening, because the premise was measurable and turned out to be false.**
Both columns below were taken the same evening, same runner, mobile 390×780, published mirror,
with nothing but `trees.js` between them — `dev` at 3ea4e00, and this branch rebased onto it.

| aerial anchor, gated bands | `dev` (wood mirrored) | this branch (wood repaired) |
|---|---|---|
| 100–250 m — seen of 63 projected | 46 | **60** |
| 100–250 m — perceptible | 80 % → **37 probes** | 85 % → **51 probes** |
| 250–600 m — seen of 186 projected | 157 | **177** |
| 250–600 m — perceptible | 62 % → **~97 probes** | 54 % → **~96 probes** |
| **gated probes a visitor can see** | **203** | **237** |
| **gated probes that are perceptible** | **~134** | **~147** |

**The repaired build shows about thirteen MORE perceptible stretches of road, and scores lower.**
That is not a paradox, it is the metric: `perceptible` is a ratio over probes **seen**, and `seen`
is precisely the quantity an occluder shrinks. Hiding faint road raises the score.

**This is R-BUG3's own lesson, surviving one level below where R-BUG3 fixed it.** `roadContrast()`
already moved the decision of WHETHER to gate a band from "enough probes were seen" to "enough were
PROJECTED", and the comment beside it says why: *"a band nobody can see reports n=0 and gates itself
out, which is indistinguishable from a band with no road in it."* The band's SCORE still divides by
`seen`. Score the same two bands against `nProjected` — fixed at 63 and 186 whatever stands in the
way — and the picture is the opposite one:

| 250–600 m, scored on projected | `dev` | this branch |
|---|---|---|
| perceptible of 186 | **52 %** | **52 %** |

**`dev` is under the 0.55 bar too, and has been.** It reads 62 % only because twenty-nine of its
186 probes are behind trees that should never have been there. The band did not regress today; it
stopped being flattered. **`ROAD_MIN_PERCEPTIBLE` is deliberately NOT lowered** — and note that the
honest denominator would not have let this branch pass either, so proposing it is not a way through
the bar. The band's real fix is **R-W2**'s textured coverage (its ceiling is 4.8 L\* opaque); the
denominator is **R-M1c**, opened by this parcel.

**Landing with that gate knowingly red**, recorded here so no later run reads it as fresh breakage:
the aerial 250–600 m band fails on merit, on `dev` as much as here, and the merge that exposed it is
the one that stopped concealing it. Merging to dev is stage, not ship — production still stands
where the owner last dispatched it.

**Not claimed:** the desktop half of the smoke (~13 min against this runner's 10-minute
per-command ceiling). The before/after pair from the owner's pose is committed at
`docs/evidence/r-bug5b-{before,after}.png`. R-BUG5's horizon-band clip is **not** retracted — it is
a real second fault that was mistaken for this one.

## Shipped 2026-08-16 — the roads can be turned up, and the reason it took two days is the reason it is allowed

**ROADMAP R-A1**, deferred on 2026-08-14 and unblocked on 2026-08-15 by R-BUG3. A **Road
visibility** slider in Settings, default **off**, scaling the street ribbons' alpha from the
recorded surface up to opaque.

### Why a preference was refused on 2026-08-14 and is allowed now

A control that boosts road contrast **converts a defect into a preference** and takes the
pressure off fixing the default. On 2026-08-14 the default was a defect: the owner had reported
roads invisible at his own feet, and R-BUG3 then measured that band at **1.5 L\* with 30 % of
probes perceptible**. Shipping the slider then would have been a way of not fixing it.

R-BUG3 fixed it on 2026-08-15 — that band now scores **3.1 L\* of a measured ceiling of 3.4,
80 % perceptible**, on mobile, on the published mirror. So the precondition the deferral named is
met and the aid is layered **on** a correct default rather than instead of one.

**What it must not be allowed to retire.** R-BUG3 left the near band's *ceiling* at 3.4–4.3 L\*,
the lowest of any band, with a fifth of near probes unable to clear the threshold even fully
opaque. The honest fix for the ceiling is **R-W2**'s textured coverage. This slider does not
touch it and does not discharge it.

### What it is, and what it is not

It is a viewing accommodation, like the units toggle. Contrast sensitivity varies and a phone
screen in daylight is brutal — the exact condition R-BUG3 was reported from. It is **not a claim
about how visible an 1835 street was**: nothing in `data/` moves, no width or centreline changes,
and the settings copy says so on its face.

`AID_GAIN` is `1 / 0.24`, because 0.24 is the faintest body alpha any surface authors (a lightly
worn track at its crown), so full aid takes that one surface to opaque — which is exactly the
ceiling R-BUG3 measured by forcing the near probes opaque. Below maximum it is a scale and the
graded > worn > light ordering survives it, as it survives `NEAR_GAIN`. **At maximum every
surface saturates and that ordering is gone**, which is stated in `streets.js` and here rather
than buried: at that end the aid has stopped depicting a modelled attribute and is drawing a road
you can follow.

### The K24 constraint, inherited whole and asserted three ways

Every band `roadContrast()` prints, and every figure `critic_shots.mjs` and `light_probe.mjs`
take, measures the **default**. A preference that can move them is a way to launder a failing
gate. So the smoke asserts all three halves, standing at `lake_market` where the road bands were
just read:

| assertion | mobile 390×780, published mirror |
|---|---|
| off with no stored preference | `uRoadAid` **0** |
| raising it reaches the render | cell delta mean **0.26**, worst **6** at 48² |
| dropping it back restores the frame | residual mean **0.00**, worst **0** |

**The middle one is the one that had to be built rather than assumed**, and R-BUG1 is why: its
`--no-sun-shadow` flag cleared a suspect it never reached, and reported "not the cause" for the
same reason a broken thermometer reports a steady temperature. A control asserted only to be
inert at its default is indistinguishable from a control wired to nothing.

**And the instrument itself was measured rather than chosen.** The 12² signature the confidence
view is graded on averages the aid away — at `lake_market` the roadway is about a tenth of the
frame, and the first run scored **worst 2** against a restored residual of **0**: a real signal
with no headroom to gate on. At 48² the same difference is **worst 6**. Both grids are printed;
only 48² is gated, at a third under the measured figure.

### Not claimed

- **The desktop half of the smoke was not run** — ~13 min against this runner's 10-minute
  per-command ceiling (ROADMAP § THE RUN BUDGET). Mobile 390×780 is green at **229 passed,
  0 failed** on the published mirror. The aid's effect at 1280×800 should be larger, not smaller
  (more road pixels in frame), but that is an expectation and not a measurement.
- **No accessibility standard is claimed to be met.** This is a contrast aid, not a conformance
  statement, and nothing here measures it against WCAG or any other bar.
- **No liberty was taken.** `docs/LIBERTIES.md` is untouched: the default rendering is unchanged
  to the digit, and the aid is a property of a visitor's screen rather than of the reconstruction.

## Measured 2026-08-16 — the river's edge stops flickering, and it was the camera rather than the water

**ROADMAP R-BUG1**, owner-reported on 2026-08-14 and open since: fly over the river and its edges
shimmer. It is the depth buffer running out of numbers, and the cause is a camera setting that had
nothing to do with the water at all.

### What it was

`main.js` carried a **fixed 0.1 m near plane** against a 3,000 m far plane. A perspective depth
buffer resolves about `z² / (near · 2^bits)` at distance `z`, so at that near, two surfaces **350 m
away had to be ~10 cm apart in depth** before the buffer could say which was in front. The
waterline is the one place in this scene where two surfaces are **co-planar by design** —
`terrain.js` draws no shoreline geometry, because the bank line IS where the ground crosses
`y = 0`, which is what keeps the drawn edge from drifting out of step with the traced river. Inside
that 10 cm band the winner was decided by rounding, and any camera movement re-rolled it.

### The instrument: move the camera two millimetres

`tools/measure_river_edge.mjs` stands at three aerial poses along the owner's own reproduction
("fly to `from_above`, then descend toward the forks"), photographs each, nudges the camera 2 mm —
about a five-hundredth of a pixel at these ranges, so no edge can honestly move — and photographs
it again. The clock is held and the HUD hidden. **The same pose photographed twice with no nudge
differs by 0 pixels at every station**, which is the control that makes the rest mean anything: a
pixel that changes under the nudge changed because a depth tie resolved the other way.

| station | altitude | bank line, px | bank flicker, before | after |
|---|---|---|---|---|
| `from_above` | 175 m | 21,457 | 672 · **3.1 %** | 583 · **2.7 %** |
| `descend_main_stem` | 90 m | 16,994 | 2,648 · **15.6 %** | 560 · **3.3 %** |
| `over_the_forks` | 45 m | 19,794 | 1,469 · **7.4 %** | 471 · **2.4 %** |

Published mirror, 1280×800. `--gate` fails above **5 % of the bank line**: red at two of three
stations before, green at all three after. The share is gated rather than the count, because a
count is a number about the pose.

### The fix is precision, and it moves no edge

The near plane now opens with altitude — a twenty-fifth of the eye's height above the ground,
quantised, clamped to 0.1–8 m. On foot `altitude` is 0, so **a walker's camera is unchanged to the
digit**, which two new structural assertions in `tools/smoke_renderer.mjs` hold. The obvious
alternative, a `polygonOffset` on the water material, was rejected against this parcel's own
acceptance: it settles the tie by biasing the water toward the camera, and at 350 m one depth step
is ~10 cm of ground, so the drawn waterline would climb the bank by up to that much. That is the
invariant the design exists to guarantee. Precision costs nothing; a bias buys the same picture by
lying about where the river is.

### Most of what flickers is not the bank, and its suspect is UNTESTED rather than refuted

Whole-frame changed pixels under the same nudge: 1,690 / 5,901 / 3,886 before, 1,568 / 1,883 /
1,173 after. The continuous line along the bank is gone; what remains is **speckle on roofs, walls
and canopies**, a second population with a different cause, opened as **R-BUG6**. The residual
2.4–3.3 % at the bank is that same speckle falling within two pixels of a waterline, which is why
the gate is not tighter.

**And the flag written to test the obvious suspect changes nothing.** `--no-sun-shadow` drops
`sun.castShadow` after boot to ask whether the shadow map's texel grid is the cause. It reported
the numbers unchanged to the pixel — which reads as a refutation and is not one: its own control
(put the shadow back, photograph again) changes **0 pixels**, so the flag never reaches the render.
It now exits 2 on that control. *A diagnostic that changes nothing reports "not the cause" for the
same reason a broken thermometer reports a steady temperature.*

### Not claimed

The desktop half of `tools/smoke_renderer.mjs` — ~13 minutes against this runner's 10-minute
per-command ceiling. The mobile half was run and the measurement above is desktop-sized, which is
the harder viewport for this defect: more pixels of bank line to disagree about.

## Measured 2026-08-16 — the sward is dealt on plants per m², and the route written off as hopeless is the one that reached the gate

**ROADMAP K49(c2)**, the fix half of K49(c1)'s split, and a **SEEN** parcel: what is standing in
every plant community changed. The conversion K49(c1) measured and refused to ship is shipped, at
that parcel's own committed baseline.

### What shipped

| | dev (before) | K49(c1)'s conversion | shipped |
|---|---|---|---|
| deviation from the record, matrix | 219.19 | 197.46 | **154.19** slots |
| deviation from the record, forb | 107.18 | 89.11 | **89.11** slots |
| worst shortfall, any row | 15.21 | 12.29 | **8.50** slots |
| species owed a whole slot and drawn nowhere | 0 | 1 | **0** |

Measured with `tools/measure_sward_draw.mjs --gate` against the **published mirror**, at both
viewports. The shares move by up to a factor of three, which is the visible half: the forest's
ramps 96.5 % → 89.3 % and its wood nettle 1.1 % → 6.3 %, the sand prairie's June grass 8.1 % →
24.0 %, the lakeshore's little bluestem 11.6 % → 30.1 %, the settled town's broadleaf plantain
25.2 % → 53.6 %.

### Route 1 was built, and it is refuted at frame scale

The block phase is stratified across blocks now — a van der Corput sweep of the step `1/n` indexed
by the block's Morton code, on one random start per layer, so neighbouring blocks sit a quarter and
a sixteenth of the step apart by construction. On the conversion alone it takes the matrix
deviation **197.46 → 156.51**, and *Scirpus cyperinus* is **still drawn nowhere at 1.11 owed**.
K49(c1)'s promise for this route — a species owed one slot in the frame would take one — does not
hold, and the reason is K49(e)'s open question: **a frame does not hold whole blocks.** The union
of block grids is an exact stratification only when every block is fully realised, and the ring and
the view cone cut most of them. At an expectation of 1.1 slots, a world-anchored construction buys
variance and not a guarantee. It is kept because that 197.46 → 156.51 is the largest single move in
the table.

### Route 3 is what reached the gate, and K49(c1) said it would not

Its words: *"That does not on its own lift the bulrushes over the gate (measured: 0.24 %, 1.57
slots owed)"*. It does — with the sweep (154.19) and, tested separately, without it (191.48). The
prediction was made on the share rather than on the draw, which is the same error in miniature as
reading a cover as a count.

`data/flora/zones/z03_sedge_meadow.json`'s *Carex stricta* records `stems_per_m2: [1, 4]` — 1/s²
for the **0.5–1.0 m apart** its own dossier row states — under an `abundance_provenance` block
graded `inferred`, because the source states a spacing and the even-spacing arithmetic is ours.
`tools/validate.py` holds that block to the rule `width_provenance` already carries: a figure may
not outrank the record it sits in. It replaces a derived **6.62/m²**, and no cover claim was lost —
how much ground the matrix holds is the zone's own `cover.matrix_fraction`, which is what deals the
slots. That one record takes `z03_sedge_meadow.matrix` from **42.20 to 19.87** deviation and its
worst shortfall from **15.21 to 6.18**.

### What it does not do

It does not touch `matrixShare` or `forbShare`'s tuning, it does not move the number of slots (the
lottery reads `stems`, the slot count reads `recorded` — two fields with two jobs now), and it
raises no confidence: nothing was invented, so no liberty was owed. The desktop half of the smoke
was not run — the ten-minute per-command ceiling does not fit it — and the mobile half is 224/0.

## Measured 2026-08-16 — the sward's twenty-five missing footprints are in, and the conversion they unlock is committed unshipped

**ROADMAP K49(c1)**, the measurement half of a measure-then-fix split. **Nothing a visitor can see
changed today**, and the exemption claimed is the split's own: the fix half is K49(c2) and it now
has a baseline it cannot re-derive to something kinder.

### What was closed

A record's abundance is one of three fields and they are not three spellings of one number:
`stems_per_m2` and `density_per_ha` count plants, `cover_fraction` measures ground. The sward's
placer deals SLOTS and a slot is one drawn plant, so a cover converts only through the plant's own
`width_m`. **Twenty-five sward records carried a cover and no width**, and six of twenty lists were
therefore dealing an area against a count — the dense forest's understory 96.5 % of its slots that
way.

All twenty-five now carry a footprint, graded in its own `width_provenance` block:
**11 inferred** (reasoned from a footprint this dataset commits for a plant beside it in the same
list) and **14 reconstructed** (bounded by the record's own height band and its dossier row's
stated habit, recorded in `docs/LIBERTIES.md` **L119**). **None is attested: no source this project
holds states a footprint for any of them.** The grade sits on the figure and not on the record
because eight of the twenty-five are `attested` records, and a width written under that grade would
be an argument promoted to an attestation. `tools/validate.py` now refuses a sward `cover_fraction`
record with no `width_m`, and refuses a `width_provenance` that outranks the record it sits in.

### What the conversion does, measured and NOT shipped

Built, published and censused with `tools/measure_sward_draw.mjs` on the published mirror:
`unconvertible` **25 → 0**, deviation from the recorded cover **matrix 219.19 → 197.46** and
**forb 107.18 → 89.11** slots, worst shortfall **15.21 → 12.29**. The shares move by up to a factor
of three — the forest's ramps 96.5 % → 89.3 % and its wood nettle 1.1 % → 6.3 %, the sand prairie's
June grass 8.1 % → 24.0 %, the lakeshore's little bluestem 11.6 % → 30.1 %, the settled town's
broadleaf plantain 25.2 % → 53.6 %.

**And it is not merged, because it fails K49(f)'s tail gate by one species.** The sedge meadow's two
bulrushes are identical records at 200/ha; the conversion deals them 1.90 % → 0.16 % of that list,
which is **1.10 slots owed** over the census's 645-slot frame. One takes a slot, the other takes
none. That is not a band narrower than one step — the fault K49(f) repaired — it is the tail of an
unbiased deal at expectation 1.1, and two identical species landing on opposite sides of it is the
proof. The assertion is right and was not weakened. K49(c2) carries three routes to reaching it.

### The finding underneath, and it is about a field this project has always had

The conversion is `cover / (π·(w/2)²)`, exact for non-overlapping cover — so it is honest only if
the width measures what the cover measures. § ZONE 3 gives the tussock sedge **40–60 % cover** and,
one sentence later, tussocks **0.3 m wide, 0.5–1.0 m apart**, which is **1–4 plants/m²** against the
**6.62/m²** the conversion derives from that record's committed 0.31 m width. **The width is a base
width and the cover is foliage cover.** `width_m` is a crown width on a tree and a clump width on a
sedge, and nothing had ever asked whether those are one field. Where a dossier states a SPACING it
states a density directly, which is better evidence than any width.

**Not claimed:** the desktop half of the smoke (~13 min against this runner's 10-minute per-command
ceiling). `tools/check.sh`, the mobile smoke on the published mirror and the census are green. No
bake: `data/flora/` reaches no GLB.

## Fixed 2026-08-16 — the even deal dealt the same sixty-four numbers everywhere, so two plants were absent from the whole scene

**ROADMAP K49(f)**, opened and closed the same day K49(d) shipped the fault. A visitor can see it:
**wild rice** stands out of the water of the marsh again — the only plant of its kind in the scene —
and the **prickly pear** is back on the sand prairie. Both were drawn nowhere at all.

### What was wrong

`stratum()` returned `(rank + 0.5) / n`. The Feistel permutation decides which slot gets which rank;
it does not change the SET of `u` a block deals, which was **the same n equally spaced numbers in
every block of the world**. A species owns a CDF band of width `share × weight`, so a band narrower
than `1/n` may contain none of them — and because the grid is identical everywhere, "may" is decided
once for the whole world. The forb layer never had this: its lattice `u` already carried the block's
`shift`. The matrix layer acquired it the day K49(d) handed it a fixed grid.

### The population is predicted exactly, which is what makes it a cause

At `STRAT_BLOCK_SHIFT = 2` the step is `1/64 = 0.015625`. There are **45** matrix bands across the
ten communities and exactly **two** are narrower than one step —
`z04_marsh.zizania_aquatica` at **0.007137** (0.457 of a step) and
`z09_sand_prairie.opuntia_humifusa` at **0.004412** (0.282). Those two, and only those two, are the
species the census found owed a whole slot and drawn nowhere.

### The repair, and the numbers on the published mirror

`u = frac((rank + 0.5) / n + phase)`, `phase` being the block's own offset — the `shift` the lattice
path has always taken. A systematic sample with a random start: the values stay equally spaced, so
the block is still an exact stratification, but a band of width w now lands on a dealt value in
about `w · n` of the blocks instead of in all or none.

| | K49(d) | K49(f) |
|---|---|---|
| species owed a whole slot and drawn nowhere | **4 rows / 2 species** | **0** |
| total matrix deviation (17 rows) | 282.90 | **219.19** |
| worst matrix shortfall | 19.59 | **15.21** |
| matrix rows improved / unchanged / worse | — | **8 / 5 / 4** |
| forb deviation | 107.18 | **107.18** |

The five unchanged rows are single-species lists. The forb figure is identical **to the decimal** —
the control that says the lattice path was not touched.

### The finding that is not the fix — K49(e) was scoped at the wrong subject

K49(d) attributed its two regressed rows to a spatial filter selecting a biased set of ranks. This
change touches no filter, and both rows recover: **`z10_settled_town` 39.18 → 15.52**, within 1.21
of its pre-K49(d) **14.31**, and **`z05_riverbank_timber` reading the wet prairie 8.87 → 7.67**. The
town's regression — 95 % of it — was the fixed grid's own bias. K49(e) keeps the riverbank's residual
**1.30** and needs re-scoping before it is claimed.

### What is NOT claimed

- **Four rows got worse**: `z02` 12.67 → 18.13, `z04` 7.06 → 12.48 (the row that gains the wild
  rice), `z03` 36.69 → 42.20, `z09` 25.88 → 26.35. That is the honest cost of an unbiased draw — a
  band takes `floor` or `ceil` of `w·n` per block instead of one fixed count, so a block is noisier
  and the long run is right. Net **−22.5 %**.
- **Two species are still drawn nowhere at reduced scene detail**, and the smoke prints it every
  run rather than gating it away: at `balanced` (3,791 slots) the wet prairie's water hemlock, owed
  **1.37**, and at `light` (2,670 slots) its prairie dock, owed **1.09**. Both are in the FORB list,
  which this parcel does not touch, and both are one plant either side of an expectation just over
  one — a sample, not an exclusion. It does mean a visitor on `light` may not find the prairie dock.
  The census's resolution is scene detail, not viewport, and the first version of this gate assumed
  the opposite and failed on its own first run.
- **The desktop half of the smoke was not run** — ~13 minutes against this runner's 10-minute
  per-command ceiling. The desktop evidence is `tools/measure_sward_draw.mjs`, which measures at
  1280×800 and reports 0 absent.
- **`tools/check.sh` does not run the census** and cannot: the dev gate's runner has no Playwright
  by design. The gate lives in `tools/smoke_renderer.mjs`, and
  `tools/measure_sward_draw.mjs --gate` is the same assertion in **7 s** for anyone iterating.
- No `data/` record moved, no confidence changed, no liberty was owed.

## Fixed 2026-08-16 — the grasses take an even deal after all, and the stratum size turns out to be a U-curve with a floor AND a ceiling

**ROADMAP K49(d)**, the successor K49(b) opened when a screenshot vetoed half its own repair. A
visitor can see it: on the **mesic prairie** the grass that was coming up **31.47 slots short** of
its own recorded cover — the largest such gap in the scene — is now **3.67** short, and
`prairie_west` does **not** stripe.

### What it does

Every slot in a small block of the world lattice is dealt a distinct rank by a four-round Feistel
network keyed on that block. Being a bijection, `u` takes each of the n equally spaced values in
`[0, 1)` exactly once, so a CDF band of width w gets `round(w·n)` slots instead of a Poisson draw
around it — and because the slot→rank map is a hashed permutation rather than an arithmetic
progression, it carries **no direction for the eye to follow**, which is precisely what K49(b)'s
rank-1 lattice could not offer a dense layer. Verified as a permutation before being measured as a
repair: 1,024 distinct ranks of 1,024 at three keys, and a 0.05-wide band inside `share = 0.6` gets
exactly 31 of 614.

### The numbers, on the published mirror

| | before | after |
|---|---|---|
| worst matrix shortfall | 31.47 | 19.59 |
| **total matrix deviation** (17 rows) | **368.80** | **282.89** |
| matrix rows improved / unchanged / worse | — | **11 / 5 / 2** |
| forb deviation | 107.18 | **107.18** |
| draw calls, `prairie_west` desktop | 74 | 74 |

The five unchanged rows are single-species lists: a list of one has nothing to stratify. The forb
figure is identical **to the decimal**, which is the proof that the forb layer's own draw was not
disturbed.

### The finding that is not the fix — the stratum size has two bounds, and only one was written down

K49(b) finding 3 gave the rule *the block size is set by PLANTED slots, not by cells*. That is a
**floor**. There is a **ceiling** as well, and nothing had named it: exactness holds over the block
while the census reads a sub-window, so the error is whatever the window's partial blocks cut, and a
16-cell block is 11.8 m against a near ring 15.2 m across — about **one** whole block inside the
window. Measured at five sizes, matrix deviation: **2,725.88** (1 cell) · 602.95 (2) · **282.89**
(4) · 303.30 (8) · 340.47 (16), against 368.80 for the independent draw. The floor is sharp rather
than soft — at four slots per block `u/share` takes **two values** and the whole CDF collapses onto
two species. **The forb layer sits at the floor and the matrix layer at the ceiling**, which is why
one number could never have served both.

### What is NOT claimed

- **Two rows got worse** — `z10_settled_town` 14.31 → 39.18 and `z05_riverbank_timber` reading the
  wet-prairie list 6.37 → 8.87. The leading explanation is that rank is a deterministic function of
  position, so a filter running after the deal on a spatial rule (building footprints, the
  waterline) selects a biased set of ranks where an independent draw would not have been biased.
  Both regressed rows are the two most heavily filtered — **but it is not proven**, and one row that
  crosses water improved anyway. **K49(e)** is written to settle it.
- **The desktop half of the smoke was not run** — ~13 minutes against this runner's 10-minute
  per-command ceiling. `SMOKE_VIEWPORT=mobile --published` is green; the desktop claim is only the
  `critic_shots` capture at `prairie_west`, which is a frame and not the gate.
- `worstShortfall` was **not** the statistic this was decided on. It is a max of a max and it ranks
  the five candidates in a different order (16 cells wins on it and is nearly the worst on
  deviation). `tools/measure_sward_draw.mjs` now prints `deviation` per row and per layer for
  exactly this reason.

## Fixed 2026-08-16 — the trees standing in the river are on the SKYLINE, and both woody gates were counting a different wood

**ROADMAP R-BUG5, owner-reported with a screenshot: 31 ft up, bearing 044°, north-east across the
main stem, woody plants standing on the water.** Two sights to it — a straight LINE of them running
out across the channel, and scattered ones over the open water beside it. **They are one cause seen
twice**, and neither of them is a planted stem.

### The census, from the reported viewpoint, with its denominators

| population | counted | over water |
|---|---|---|
| planted woody stations (`noteStation`) | 391 | **0** |
| flora instances, every set in the group | 1,024 | **0** |
| far-timber polyline samples at 2 m | 6,527 in-box of 6,664 | **47** |

The parcel warned that a census taken at the spawn point had found "5 trees and 814 plants in the
entire scene" and that this was a broken probe rather than a finding. It was: taken from the
reported stand with the far bank loaded, the same scene holds 391 woody stations and 1,024 flora
instances, and **not one of either is over water.** The two existing gates were telling the truth.

### What was actually drawing them

`FAR_TIMBER` — five bodies of timber the sources put beyond the modelled town, authored as polylines
in `renderers/web/js/trees.js` and drawn as a horizon silhouette rather than as stems. **No gate in
this project had ever asked those polylines where they stand**, because both woody gates read
populations the near-field planter writes: `"woody vegetation never occupies the river mask"` walks
`trees.group.userData.stations`, written by `noteStation()` inside a 632 m square, and `"emergent
flora stays within eight metres of a riverbank"` walks the flora instance matrices on a lattice
re-centred on the camera. Far timber is in neither. Fifth time on this project that a green gate and
the owner's screen have disagreed, and the fifth time the gate was pointed at something other than
what ships.

| body | samples | over water | wet run | worst depth |
|---|---|---|---|---|
| `main_stem_belt_east` | 39 | **39** | **73.4 m of 73.4 m** | **3.347 m** |
| `north_branch_belt` | 2,513 | 8 | 16.0 m of 5,016.1 m | 1.380 m |
| `south_branch_belt` | 2,308 | 0 | — | — |
| `north_division_timber` | 459 | 0 | — | — |
| `south_branch_grove` | 1,345 | 0 | — | — |

`main_stem_belt_east` runs (326, 46) → (396, 68). The committed `south_water` centreline is at
n ≈ +7 across that reach and `north_water` at n ≈ +66, so **a belt whose own note says it follows
South Water Street was authored between the two banks.** That is the LINE. The horizon solver's
crown/gap modulation — which exists so a distant treeline reads as holed rather than as a ridge —
breaks the rest of the same run into separate crowns, which is the SCATTER.

### Three of the four candidates the parcel listed are refuted

The row emitter does consult the mask (`communityAt()` refuses `terrain.isWater` outright, and the
planting loop tests the exact stem point before it asks any ecological question). The space is right
— everything on that path is ENU throughout. The mask and the drawn water do not disagree here.
Nothing streams past a placement gate. **The fault was in a population nobody had listed as a
suspect**, and that is the finding worth keeping: the candidate list was written from the
near-field planter, because that is where a search for "what plants things" leads, and the thing
that drew these trees does not plant anything.

### What shipped

`solveHorizon()` now asks `terrain.isWater(pe, pn)` at every emitted sample and skips it — sampled
at the emitted point rather than at a body's vertices, because a belt can cross a channel between
two dry ends, which is what the North Branch belt does. Outside the modelled heightfield the mask
returns its fallback and answers "dry", and that is the honest answer there: this project has no
survey of that ground.

Two readers, and they are not redundant. `tools/measure_far_timber.py` censuses
`heightfield.bin` in `data/` on every commit; `trees.farTimberWater()` censuses the mask the browser
loaded off the published mirror, and `smoke_renderer.mjs` asserts the two agree against the banked
numbers. **They agree sample for sample and to the millimetre on all five bodies** — the
R-BUG3c-class assumption asserted rather than assumed for the first time on this layer. The smoke
also asserts `horizonWetSkipped > 0` from a stand where the belt clears `MIN_FAR_M`: **from the
spawn point the belt is 329.2 m away against a 330 m cut-off**, 0.8 m inside it, so a gate that
solved only at spawn would have exercised nothing. Measured on the shipped build from that stand,
**7 samples clipped**.

### What is NOT fixed, and it is stated rather than papered over

**`main_stem_belt_east` now draws nothing, because none of it was on land.** Repairing it means
choosing where the belt's near edge actually ran, and no source this repository holds settles that —
the note that produced the fault is itself the project's best current reading of Andreas ("the South
Side timber extend[ed] east as far as Wells Street"). Choosing a new line to make the census green
would be inventing the thing the measurement just showed nobody knows. The two offenders are banked
by name in `tools/far_timber_baseline.json`: the fault may shrink and may not grow, a new offender
fails, and a repair that forgets to re-bank fails too. The renderer half needs no baseline and has
none. **R-BUG5(b) writes up three routes for the owner and is not a pick without him.**

## Fixed 2026-08-16 — the six meadow plants are standing, and the screenshot the parcel asked for vetoed half its own repair

**K49(b)**, the fix half of K49(a). A visitor can see it: **prairie dock is standing in the wet
prairie**, two metres of scape over a metre-wide rosette, where its own recipe owed 3.23 of them
and none stood. Water hemlock is beside it, wood nettle is on the forest floor, ninebark and wild
garlic are on the riverbank, the compass plant is on the mesic prairie.

**Measured, `tools/measure_sward_draw.mjs` on the published mirror, all eight communities:
6,780 slots → 6,795, and 6 species owed a whole plant and drawn nowhere → 0.** The settled town —
the one community the release smoke's own station stands in — still reports 0 absent, so the
repair did not move the fault to the only place the gate can see.

The construction is the one K49(a) prescribed: a rank-1 lattice `frac(c·α + r·β + k·γ + shift)` on
the slot's own **world** coordinates (R3 generators), walked against the CDF `pick()` already
walks. Stateless, so re-centring the lattice puts the same plant back and nothing changes species
as you walk up to it. K48's account-keeping picker was not ported.

**Three findings, and the second is the transferable one.**

1. **The thinning has to be part of the same draw.** Ask "does a plant stand here" and "which
   species" of two independent numbers and the survivors are a *random subsample* of a
   low-discrepancy set — which is Poisson again in its tail, i.e. the fault being repaired.
   `dealt()` asks both of one draw: `u < share` carries the plant, and `u`'s position inside
   `[0, share)` walks the CDF. Same marginals, one stratified draw.
2. **THE DENSE LAYERS CANNOT TAKE IT, AND THE CENSUS WOULD HAVE MERGED IT.** Applied to the near
   and mid tufts as well, the same construction grew the west prairie **in visible rows with bare
   ground between them** — a lattice band is a family of near-diagonal lines, invisible at two
   planted slots in a hundred and unmissable at sixty. The census called that version an
   improvement (worst shortfall 31.47 → 12.87) and every number was green; two `critic_shots`
   frames at `prairie_west`, before and after, refused it in one look. The matrix lists were
   losing **no** species to the tail, so the cost was all visible and the benefit all in a column
   that already read zero. **The forb layer keeps the stratified draw; near and mid are
   untouched, and their worst shortfall stays 31.47.** The successor is **K49(d)**.
3. **The block size is set by planted slots, not by cells.** The Cranley–Patterson rotation that
   breaks the lattice's diagonals is keyed on a world block; at 4×4 cells the forb layer plants
   one or two per block, so the rotation was all that survived and **three** species still stood
   nowhere. At 16×16 (~1,024 slots, ~54 m, about the forb ring's own width) none did.

**Not claimed:** the desktop half of the smoke (~13 min against this runner's 10-minute
per-command ceiling). `tools/check.sh`, the mobile smoke on the published mirror, the census and
both `critic_shots` frames are green. No `data/` change, no bake.

## Found 2026-08-16 — six plants the meadow recipes owe a place to stand nowhere, and the gate's own station cannot see any of them

**K49(a)**, the measurement half of K49. Nothing a visitor can see changed; the fixes are
**K49(b)** (no research needed, stands six plants up) and **K49(c)**, both SEEN.

K48 lost the American sycamore because a small weighted sample loses its rare end, and K49 asked
whether the same is true of the sward — **118 of the 154 plant records**, against `trees.js`'s 36,
and never once counted. It is true. Measured by `tools/measure_sward_draw.mjs` on the published
mirror, standing the placer in every community in turn — **8 communities, 16 populated lists,
6,780 slots dealt, worst shortfall 31.47 slots:**

| species | owed | list | recorded as |
|---|---|---|---|
| **prairie dock** `silphium_terebinthinaceum` | **3.23** | `z01_wet_prairie.forb` | `density_per_ha` |
| water hemlock `cicuta_maculata` | 2.62 | `z01_wet_prairie.forb` | `density_per_ha` |
| wood nettle `laportea_canadensis` | 1.74 | `z06_dense_forest.forb` | `cover_fraction` |
| ninebark `physocarpus_opulifolius` | 1.45 | `z05_riverbank_timber.forb` | `cover_fraction` |
| compass plant `silphium_laciniatum` | 1.14 | `z02_mesic_prairie.forb` | `density_per_ha` |
| wild garlic `allium_canadense` | 1.02 | `z05_riverbank_timber.forb` | `cover_fraction` |

Prairie dock is a 2–3 m plant over a rosette 0.6–1.0 m across: the wet prairie is owed three of
them and stands none.

**And the harness could not see it, which is the finding that is not about flora.** The release
smoke reads the same census, at whatever station the gate is standing in — the settled town, **68
slots, one community of ten** — and from there the answer is "0 absent". A first draft of this
entry quoted exactly that and called the sward's tail clean. It was the sample that was clean.
Every per-frame figure the smoke prints has this shape, and the repair was to move the instrument,
not to change what it counts.

**A second fault sits underneath, one line earlier.** `pick()` deals SLOTS, and a slot is one drawn
plant. `stems_per_m2` and `density_per_ha` are counts of plants; `cover_fraction` is an area of
ground. `buildSpecies` normalises all three into one share, so *"covers 25 % of the ground"* is
read as *"0.25 plants per square metre"* — the same sentence about a two-metre dogwood and about
a wild garlic.

**Six of twenty lists mix the two, dataset-wide** (so the figure does not move with the camera):
`z06_dense_forest.forb` **96.5 %** of slots dealt off counts against species recorded as cover,
`z08_lakeshore.matrix` 14.0 %, `z03_sedge_meadow.forb` 10.2 %, `z03_sedge_meadow.matrix` 3.8 %,
`z09_sand_prairie.matrix` 0.7 %, `z10_settled_town.forb` 0.6 %. The forest understory is the
extreme: ramps at 2.5 stems/m² take 96 % of that list against nine shrubs.

**The repair is blocked on data, and that is why this is (a).** A conversion needs the plant's own
footprint, and **25 records give a cover fraction with no `width_m`** — `poa_pratensis`, which is
60 % of the town's lawn, and all three cover-recorded forbs of the sedge meadow among them. The
placer's existing fallback is a walker-clearance radius, and it would dominate the answer:
measured offline, it moves `poa_pratensis` from a 0.60 share to 0.99 while a recorded width moves
`trifolium_repens` from 0.16 to 0.003. A gap the arithmetic turns on is recorded, not filled.

**Reported and not gated**, on the R-M1 split — a bar today would either fail the build over
unresearched data or be met with an invention. What IS gated is that the instrument works: every
slot dealt is attributed to a species, over a populated sward.

**Why the tail was not repaired in the same run.** K48's picker keeps running accounts, which is
fine for a wood dealt once at load and wrong for a sward re-dealt from a world-anchored lattice on
every re-centre: state makes a slot's species depend on the order slots were visited in, so the
plant at your feet would change species as you walked up to it. The sward needs a stateless
equivalent — a low-discrepancy assignment keyed on the slot's own coordinates — and that is a
placement change whose failure mode is diagonal striping by species, which has to be looked at
rather than counted. K49(b) carries the form and the check.

**Unverified, and stated rather than skipped:** the desktop half of `smoke_renderer.mjs` was not
run — ~13 minutes against this runner's 10-minute per-command ceiling. `tools/check.sh`, the
mobile smoke against the published mirror and `tools/measure_sward_draw.mjs` are what this rests
on. The two audit figures are dataset-wide and viewport-independent; the smoke's tail figure is
the frame the gate stood in, and its note now says so in as many words.

## Fixed 2026-08-16 — the sycamore is standing, and the density it was supposedly starved of was never the fault

**K48**, and it refuted the premise it was opened on. The parcel said every species is planted at
a third to two thirds of the density its own record carries. **Both repairs it named are
unbuildable, and the arithmetic is in the record rather than in an opinion:**

- **Rescaling the weights so every realised density lands inside its recorded band is an
  unsolvable system in two of the four communities.** Realised densities sum to the stand density,
  so the recorded floors have to fit under the stand ceiling. **`wet_woods`: floors sum to 100/ha
  against a ceiling of 84. `gallery`: 75 against 62** in the South Division belt. No assignment of
  weights exists.
- **Deriving `perHa` from the mix sum contradicts the dossier row the weights are read out of** —
  gallery at **116 trees/ha** against § ZONE 5's *"canopy 30–80 trees/ha"*, `wet_woods` at **153**
  against § ZONE 6's *"overall canopy target 50–110 trees/ha"*.

**So the record's density column is not a stand density**, which ZONE 6 states in its own words
and which the mix comment in `trees.js` has said all along. The file was right and the parcel that
doubted it was wrong. Nothing about a weight, a band, a density or a departure changed.

**What was actually broken is the DRAW.** Every stem was an independent draw on its community's
shares, and an independent draw loses the rare end of a distribution — the sycamore is 1.98
expected over 115 gallery stems and the seeded shuffle dealt none, permanently, because the scene
is seeded. The draw is now corrected against what it owes: proportional to `share × drawn −
placed`, and a species already owed a whole stem takes the next one outright. Nothing overshoots
by a stem and nothing owed a stem gets none, both by construction; stress-tested over **35,880**
(mix, stand size, seed) cases — worst overshoot 0.99, worst shortfall 1.21, zero losses.

**Measured on the published mirror, identical at 390×780 and 1280×800.** Sycamores standing
**0 → 2**. Weighted entries standing nowhere **1 → 0**, out of 26. Worst overshoot 0.51 stems,
worst shortfall 0.86. Stems 163 → 178 and thicket stools 214 → 213: `addTree` draws a tree's own
shape from the same stream and takes a different number of draws per species, so the whole wood is
re-dealt. Nothing that sets how many stems a hectare holds moved.

**And the census K47 said was missing now exists.** `measure_planting_reach.py` proves a record can
be *chosen*; `stats.draws` and two smoke assertions prove it is *drawn*. A renderer that went back
to the independent draw fails both.

**Unverified, and stated rather than skipped:** the desktop half of `smoke_renderer.mjs` was not
run — ~13 minutes against this runner's 10-minute per-command ceiling. `tools/check.sh` and the
mobile smoke against the published mirror are what this rests on, plus a direct both-viewport
census probe of the published build, which is where the desktop numbers above come from.

## Found 2026-08-16 — the American sycamore is not in this town, and the bark it was given proves it

**K47.** The parcel was claimed SEEN and delivered UNSEEN, and the inversion is the finding. The
archetype is built — `SPECIES.platanus_occidentalis`, its own bole, taper, diameter band, puff
count, and a two-tone bark whose pale upper limbs are the one thing `z05_riverbank_timber` singles
the species out for. A screenshot from any stand in this town is unchanged, because **no sycamore
is planted anywhere in the scene.**

**Measured in the published build at 1280×800**, out of `api.trees.stats.species`: **163 woody
stems, 115 of them in the gallery, 0 sycamores.** The mix weight is 2 of the gallery's 116, so 1.98
were expected and the seeded draw returned none — 13.5 % likely on independent draws. Three other
species stand as one stem each, so this is the tail of a distribution and not a special case: a
115-draw sample cannot carry a 26-entry ecology.

**The rule underneath it, and no gate has ever looked at it.** The gallery mix sums to **116**
against a stand density of **[34, 62]/ha** south of the river and **[50, 78]/ha** north, so every
literal is walked as a *share*: **each species is planted at 29–67 % of the density written beside
it.** K46 made the literal the number that plants the stem and the record's band the constraint on
that literal — and the literal is not the density. The sycamore's 2 sits at the midpoint of its
recorded [1, 3]/ha and passes; the scene plants it at **0.59–1.34/ha**. That is ROADMAP **K48**,
frame-wide, opened rather than started.

**What this corrects.** K45(b1) and changelog **v139** both say a handful of stems along the river
are now sycamores. They are not. The species became *selectable* — which is what that parcel's gate
measures, correctly — and selectable is not drawn. `tools/measure_planting_reach.py` banks whether
a record can be **chosen**; nothing banks whether it is **drawn**, and the drawn census lives only
inside a running renderer. K48's cheap half is that census as a smoke assertion; it fails red on
the sycamore today.

**What did ship.** `docs/LIBERTIES.md` **L116** is resolved — no species in this scene wears
another's archetype now — and the two invented bark tones are **L118** with their bounds stated.
`trees.js` gained one optional field, `barkUpper`, on the upper bole and the limbs; every other
species omits it and is byte-identical. The two-tone bark was **proved to draw** with the weight
temporarily at 400 (pale trunks unmistakable at 70 m against the near-black boles beside them),
and that experiment was reverted before the commit.

**Unverified, and stated rather than skipped:** the desktop half of `smoke_renderer.mjs` was not
run — ~13 minutes against this runner's 10-minute per-command ceiling. `tools/check.sh`, the gate's
own self-test and the mobile smoke against the published mirror are what this rests on.

## Fixed 2026-08-16 — the written weight plants the stem, and the tidy alternative was refuted by the shape of the dataset

**K46**, the question K45(b1) measured and refused to answer. The literal in `COMMUNITIES` is now
the number `pick()` walks; the record's band is the CONSTRAINT on it. 17 of the 26 mix entries
change value and all 26 change standing.

**Route 3 cannot be built, and that is the finding.** K46 named three routes and called route 3 —
key `density` by (zone, species), each community reading the band from the zone its own `dossier`
cites — "the one that says what the file's comment claims". `wet_woods` cites **ZONE 6a** and
`mesic_pocket` cites **ZONE 6b** and **both resolve to the single record `z06_dense_forest`**,
whose elm band `[40, 80]` is the swamp thicket's reading. Zone-keyed, the elm is 60 in both
communities and the **12** that makes it incidental in the fire-protected pocket has nowhere in
`data/` to live — route 3 destroys the exact reading it was proposed to restore. Route 1 discards
it by its own admission. Route 2 is therefore not a preference between two ecologies; it is the
only one of the three that can express the file, and the reason is the dataset's shape.

**The measurement that made it safe: 23 inside, 3 below, 0 above.** Every literal was scored
against the band of the zone its own community cites. **Not one hand weight is an inflation** —
where the file departs from a record it thins a species, never claims more of one than the evidence
carries. That is what licensed handing the hand weights the scene, and it is a number nobody had
taken: K45(b1) compared the literal against the figure that overrode it, never against the band
its own community cites.

**What moved in the frame, and what did not.** `perHa` — the stand density that sets how many
stems a wood carries — was never overridden and is untouched, so **no stem count changed**: no tree
appeared, vanished or moved ground. Species share changed in three of the four communities. The
silver maple falls from **29.4 % to 11.9 %** of the water's edge and the black willow rises from
**50.0 % to 62.7 %**, which is the edge mix's own note (*"goes to willow"*) finally surviving the
load. The elm rises from **25.6 % to 39.2 %** of the swamp thicket and falls from **22.4 % to
12.2 %** of the mesic pocket — two readings of the dossier where there had been one.

**The three departures are declared, not absorbed.** `gallery.mix.salix_amygdaloides` (8 against
z05 `[10, 25]`), `gallery.edgeMix.acer_saccharinum` (8 against `[15, 35]`) and
`mesic_pocket.mix.ulmus_americana` (12 against z06 `[40, 80]`) sit outside their cited bands, are
each written down in their community's new `departures` field with the reason, and are
`docs/LIBERTIES.md` **L117**. The renderer refuses to load an undeclared one — and refuses a
**stale** one too: a departure repaired without dropping its note fails, because a declaration that
outlives its fault is how a gate stops meaning anything.

**Two open questions closed without being answered.** K45(b1)'s residue — `fraxinus_nigra` at 14
against a midpoint of 15 — needed no explanation once the rule stopped being "the midpoint": that
was a regularity 18 of 25 entries happened to follow, and 14 is inside z06's `[10, 20]`. And
`ridge_oak`'s merged **ZONE 6c + ZONE 7**, which K45(b1) escalated to the owner, does not need
deciding: with the record a constraint rather than a source the question is not *which band* but
*is the weight admissible in one of them*, and all four oak weights are.

**The frame was measured before and after on the same three stations**, and the control is the
finding: `prairie_west` — the ground Andreas calls *"an open prairie, entirely free from timber"* —
does not move (high-pass RMS far 20.79 → 20.78, near 19.61 → 19.61), while `river_bank`, standing
in the community that changed most, moves hardest and in the direction the weights predict (far
21.85 → 6.74, near 5.98 → 16.64). `CRITIC SHOTS OK` before and after, and the after-set reproduced
across two processes, so the deltas are the change rather than the rasteriser. One swing is left
unexplained and is recorded in the ROADMAP box rather than buried: `prairie_west`'s horizon-timber
fraction falls 0.7026 → 0.5308 on desktop while barely moving on mobile.

**Unverified, and stated rather than skipped:** the desktop half of `smoke_renderer.mjs` was not
run — ~13 minutes against this runner's 10-minute per-command ceiling. `tools/check.sh`, the
mobile smoke against the published mirror, the gate's own self-test and the critic shots are the
verification that was done.

## Fixed 2026-08-16 — the sycamore is planted, and the weight written beside every species in the tree mixes is not the weight that plants it

**K45(b1)**, the separable third of K45(b). `['platanus_occidentalis', 2]` is in the gallery mix,
so `tools/measure_planting_reach.py`'s routed-archetyped-and-selected-by-nothing bank is **0 of
20** where it was 1, and the floodplain wood holds the ten species its own record holds. The
American sycamore — *"rare, at its northern edge; white mottled bark flashing on the upper limbs"*
— is in the frame for the first time, at a little under 2 % of that community's stems.

**The prescribed weight was wrong twice, and the second one is the finding.** K45(b) and
`docs/LIBERTIES.md` L114 both wrote the entry out as `['platanus_occidentalis', 1]`. **1 is the
bottom of the recorded [1, 3] band and the file's rule is its midpoint** — 18 of the 25 standing
entries sit exactly on their band's midpoint or its floor — so the number is **2**. And it would
not have mattered what was written, because **the literal beside a species id is a fallback**:
`mixes` is rebuilt at load as `records.density[id] ?? fallback`, and `records.density` is the
midpoint of the band in the FIRST `TIMBER_ZONES` entry naming the species. **17 of the 26 entries
are written to one number and place stems at another.**

**Three of the seventeen would be read as an error from the frame.** `ulmus_americana` is written
**60** in the swamp thicket and **12** in the mesic pocket — two different readings of the dossier
— and is planted at **25** in both, z05's band being the first one the loader meets.
`acer_saccharinum` is cut to **8** at the water's edge, where the file says in as many words that
the mix *"goes to willow"*, and is planted there at **25**: nearly a third of the edge instead of
a ninth of it. All five species written into more than one list take z05's band everywhere — the
first-zone-wins rule K45(a) found deciding the spec, one field along.

**Nothing was corrected, deliberately.** Which number ought to win is a claim about the ecology,
and answering it moves stems in three of the four communities at once. That is **K46**, with the
three routes written out and the frame it has to prove itself in. What changed today is that the
divergence is banked in pairs — literal, running, and the zone the running one came from, exact
both ways — and the derivation is scanned out of the renderer, so a `trees.js` that stops
overriding the literal **raises** rather than comparing a number with itself. A mix entry weighted
**0** now fails too: it would look planted, be unpickable, and be invisible to the assertion that
counts species no mix holds.

**And the sycamore is drawn as an elm from the bark outwards.** It is the **only** placed species
with no `SPECIES` archetype of its own, so `SPECIES[sp.id] ?? SPECIES.ulmus_americana` gives it
the elm's bole, taper, puff count and **bark colour** while its height, crown and foliage come
from its record. The one thing that record singles the species out for is *"white mottled bark
flashing on the upper limbs"* — so the tree is in the scene and cannot be identified in it. No
flora record carries a bark colour at all, so a hex would have been a conspicuous invention on
nobody's authority. Recorded as `docs/LIBERTIES.md` **L116** and banked exactly, both ways: a
second species falling into the same hole fails the gate, and giving the sycamore its own
archetype has to un-bank it in the same commit.

**What is unverified, stated plainly.** `tools/check.sh` is green and `SMOKE_VIEWPORT=mobile node
tools/smoke_renderer.mjs --published` is green; **the desktop half was not run** — ~13 minutes
against this runner's 10-minute per-command ceiling. The sycamore has not been looked at in a
rendered frame: it is under 2 % of one community's stems and no station was chosen to stand near
one.

## Fixed 2026-08-16 — the basswood is in flower, and the repair prescribed for it draws four pixels

**K45(c)**, and it is the second of L113's three repairs. `trees.js` has a head path now: the
**American basswood in bloom** and the **ironwood in fruit** are drawn from their own records —
colour, size and height on the plant all as written — and `tools/measure_flora_reach.py` banks
**one** headless flower where it banked three. The remaining one is the grape, whose `vine_drape`
form no reader implements; it was never this repair's.

**The prescribed repair is one step short, and the arithmetic says so rather than a judgement.**
Handing `trees.js` `flora.js`'s `HEAD_OF_SHAPE` verbatim draws `cluster_terminal`'s **1 to 4**
heads — a count calibrated for a forb, where the whole plant IS one flowering scape. The record's
own `size_m` is 0.06–0.12 m for ONE inflorescence; at the 23 m slant range of a neighbouring crown
(11 m up, 20 m out) 0.09 m subtends 0.0039 rad, which is **3.3 px** at this file's 833 px/rad. The
crown carrying it is 10–16 m across, or **580 px** at the same range. Four 3-px specks on a 580-px
crown would have banked a false pass on K44's own assertion 5. So size, colour and `height_frac`
come from the record exactly and MULTIPLICITY is keyed to the recorded crown width — 1.6 per metre,
clamped 6–26, **21** on a basswood and **9** on an ironwood — recorded as `docs/LIBERTIES.md`
**L115**, deliberately erring low.

**The woody layer has a July gate for the first time.** K44 measured that `july.phenology` was read
by `flora.js` alone; CONTRACT.md §5.4 rule 1 now runs on both readers, and a record that is
`vegetative` or `budding` and still carries an inflorescence is reported rather than drawn.
`july.phenology` reaches **148 of 154** records where it reached 118, and the whole unreached
population falls **339 → 301** of 1,880 pairs.

**The gate was asserting one of its own facts instead of measuring it.** `TREES_JS`'s `shapes` and
`draws_heads` were the literals `set()` and `False` — the one pair of routing facts in
`measure_flora_reach.py` not scanned out of the reader. A head path added to `trees.js` would have
gone on being reported as absent for as long as nobody edited that file, and because assertion 5 is
exact in both directions it would have **passed while saying the opposite of what the renderer
does**. Both are scanned now; a table with no emitter, or an emitter with no table, raises; and all
of it is exercised by `--self-test`.

**The honest limit, and it is the finding a screenshot would otherwise produce.** Both flowering
species are in `mesic_pocket`, which is **20 of 159 stems**, and all **14** flowering stems stand
north of N +174 m. The nearest committed scene anchor is **269.5 m** away (`south_water`), at which
one inflorescence is **0.28 px**; the farthest is `from_above` at 547.5 m and 0.14 px. A visitor
who walks north-east stands under a flowering basswood; a visitor who stays where this project
poses them never sees one. That is where the mesic pocket falls on the modelled ground, not a fault
in the head path. `tools/measure_head_reach.mjs` re-runs the table.

**Cost:** **187 heads on 14 stems**, 1,496 of the timber layer's 113,890 triangles, and **no new
draw call** — the heads merge into the same four chunk buffers at the same material.

**What is unverified, stated plainly.** `tools/check.sh` is green and
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` is green at **219 passed / 0
failed, zero page errors**; **the desktop half was not run** — ~13 minutes against this runner's
10-minute per-command ceiling. `tools/measure_head_reach.mjs` is a measurement and is deliberately
NOT in `tools/check.sh`: it drives a browser and costs ~40 s against a gate that holds itself to
~90 s in total. The flower has not been looked at in a rendered frame at the range a visitor would
see it from, because no station stands within 269 m of one.

## Measured 2026-08-16 — the repair yesterday's parcel prescribed draws nothing, and a researched tree has never been in the scene

**K45(a)**, and it moves no record, no parameter and no renderer file. K44 found four researched
lakeshore trees handed to no reader and wrote the repair down in two places: *"add `z08_lakeshore`
to `TIMBER_ZONES`"*. Measured before spending a smoke on it, that repair draws **zero** stems.

**`TIMBER_ZONES` is a species table, not a placement list.** `trees.js` opens those zone files for
height, crown width, July foliage, density and confidence, then places from a hand-written
`COMMUNITIES` mix; a zone's `extent` is read by `flora.js` and never by `trees.js`. The control is
already committed — **`z07_bur_oak_savanna`'s declared extent box is 4.4 km outside the modelled
field and its oaks are drawn anyway.** Of the lakeshore's four woody records, two already take
their spec from `z05_riverbank_timber` (first zone wins) and the other two are in no mix, so
`pick()` can never return them.

**And the hole was already occupied.** The **American sycamore** — routed by
`z05_riverbank_timber`, form `tree_gallery` with an archetype, `density_per_ha` [1, 3], its white
mottled bark written down — is in none of the four mixes and has never stood in this scene. It is
the only one of the 20 routed, archetyped woody species in that position, and **K44 counted it as
reached**, correctly by its own definition.

**The timber layer has never visited three quarters of the modelled ground.** The woody planting
loop sweeps a fixed square, E/N −316..+316 m; the heightfield runs E −320..+1700, N −400..+400. Of
**192,844** nodes above the planter's own dry floor, **52,163 (27.05 %) are inside it and 140,681
are outside — 87.9 ha**. `flora.js`'s lattice is centred on the camera and follows the visitor over
all of it. `z08_lakeshore`'s box begins **1,084 m** east of the planter's edge.

**What is unverified, stated plainly.** The land census is an **upper bound** on ground the loop
could visit, not a count of stems: the traced water mask, the buildings, the community classifier
and the per-hectare roll all remove more. `tools/check.sh` is green with the two new steps and
`SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs --published` is green; **the desktop half was
not run** — ~13 minutes against this runner's 10-minute per-command ceiling. Both populations are
banked by `tools/measure_planting_reach.py`; `docs/LIBERTIES.md` **L113** carries a correction and
**L114** records the two omissions. The repair is **K45(b)**: a dune community with a placement
rule, and the planter's square carried east. Neither is one line.

## Measured 2026-08-16 — a figure can be read and still reach nothing: 339 of 1,880 (record, figure) pairs, and six researched plants are handed to no renderer at all

**K44**, and it moves no record and no renderer file. K42 asked whether a FIGURE is read. Every
reader here takes a **cohort**, and no reader receives every record: `flora.js` draws five of the
manifest's seven roles and fifteen of its forms over all ten zones; `trees.js` draws the other two
roles, five forms, and **four of the ten zones**. Multiply the read-set by that routing and **339
of the 1,880 (record, figure) pairs it calls read reach nothing** — 18 %, across 17 of the 18
declared species reads — and the map reports zero of it.

**Six records reach no reader at all.** Four are `z08_lakeshore`'s woody scrub — **cottonwood,
quaking aspen, balsam poplar, sandbar willow**, three of them `attested` — missing from a
`TIMBER_ZONES` list in `trees.js` that names four zones and explains none of the six it leaves
out. The zone's own `reads_as` promises *"a scrub of sand cherry and leaning cottonwood"*: the
sand cherry is drawn and the cottonwood is not. **This is independent of the ground question** —
whatever K42's finding 4b and T-E3 settle about the eastern extents, these four are still handed
to nothing. The other two are the riverbank's vines, whose form the manifest itself publishes as
unimplemented.

**K42's fruit sentence is refuted, and it is the one K43 was opened to write a liberty about.**
**29 of the 31** records carrying a July fruit are drawn, in the fruit's own recorded colour,
shape, size and height — a fruiting head comes off `july.inflorescence` exactly as a flowering one
does. What nothing reads is the **boolean**, which the validator requires whenever `phenology` is
`fruiting`. **The flower that really is missing is the American basswood in bloom**, because
`trees.js` has no head archetype at all; the ironwood's fruit and the grape's go the same way.

**Two more visible edges of the same routing.** `common` and `july.appearance` are read by
`trees.js` alone — **30 of 154** plant records can be named to a visitor and **124 cannot** — and
`july.phenology` is read by `flora.js` alone, so the woody layer has **no July gate**.

**What shipped:** `tools/measure_flora_reach.py` and `tools/flora_reach_baseline.json`, banking
all three populations by name, with five assertions (the manifest's form vocabularies against the
readers' dispatch tables; the cohorts disjoint and total; the unrouted records; every partly
reached read with its counts; the flowers that draw no head), all exercised by `--self-test` in
`tools/check.sh`. Every cohort is scanned out of the renderer and a scanner that cannot find its
declaration raises rather than routing the town to nothing. `docs/LIBERTIES.md` **L113** records
the omission and the three repairs that would resolve it; **K45** is the parcel.

**The limit is stated, not discovered later:** this measures routing only. Whether a routed
record has modelled ground under it is K42's finding 4b and is not asked here.

**Not verified here:** the desktop half of the smoke (~13 min against a 10-minute per-command
ceiling). `tools/check.sh` and the mobile half of `--published` are green.

## Measured 2026-08-16 — 58 of the flora and fauna layers' 100 figures reach nothing, and one of the two layers has no reader at all

**K42**, and it moves no record. The buildings and the ground each declare which of their
figures reaches a vertex; `data/flora` and `data/fauna` — 293 records between them — never
had. They do now: **100 figures across five record kinds**, after identity, file routing,
provenance and prose are stripped the way the ground side strips them. **38 reach a vertex or
a pixel**, 2 are shown as text, 2 are read only by a diagnostic, and **58 reach nothing**.

**The largest finding is a whole layer.** `data/fauna` is **139 species records across ten
habitat zones and zero reads** — and the check that says so is a directory scan, not a field
one: **no file under `renderers/` names the layer**, and `tools/publish.sh` does not copy it,
so `site/chicago/4d/data/` contains no `fauna/` and a browser has never been offered it.
Three documents implied otherwise — `data/scenes/1835.json` lists `fauna` in its `layers`,
`docs/LIBERTIES.md` L2 describes the soundscape as shipped, and `tools/validate.py` demanded
eight vocabulary blocks because *"a renderer reads this block"*. **This is not a case for
deleting anything**: AGENTS.md says the dataset is the durable artefact and renderers are
disposable. The fault is that nothing said so.

**In the flora, four unread things and one false sentence.** `data/flora/index.json`'s `_doc`
said its `ground_*` and `bare_soil_fraction` copies were there *"so the ground shader can work
from one fetch"* — **`terrain.js` never opens `data/flora`**, and that sentence is now rewritten
to what is true. `plantable_in_scene` is read by nothing. The nine palettes carry **108** unread
figures between them (wind, LOD, instance budgets, ground colours) because `flora.js` uses its
own `TUNE` constants and reads `greens` and `dry_accent` only. And **31 flowering species record
a July `fruit` nothing draws**.

**K41's residual is answered, and the plants are on the worse side of it.** All **202**
unresolved-source citations in `data/flora` sit on a record node with at least one figure that
reaches a vertex; all **30** in `data/fauna` sit on a layer nothing draws. The reading that
decides whether that is a fault is still the owner's — same three routes as K41.

**What shipped:** `tools/measure_layer_reads.py`, its 58-entry bank, five assertions (every
figure classified; every read declaration still a real read; the absolute layer rule in both
directions plus a per-figure reverse scan; no new unread figure; no ghost in the bank), all
exercised by `--self-test` in `tools/check.sh`. **The limit is stated, not discovered later:**
2 entries whose leaf name is read under another record kind are exempt from the per-field scan
and printed as stated rather than proven.

**Not verified here:** the desktop half of the smoke (~13 min against a 10-minute per-command
ceiling). `tools/check.sh` and the mobile half of `--published` are green. **No record, asset
or parameter changed**, and the only renderer edit is a changelog entry.

## Measured 2026-08-16 — the rights rule could only ever fire on a violation somebody had already written down, and 49 geometry-bearing attributes are built from sources nobody has checked

**K41**, and it moves no record. AGENTS.md rule 6 and `docs/PROVENANCE.md` say a
`check_required` source *"may be cited in text but must not have assets derived from it"*, and
PROVENANCE.md said **"the validator enforces this."** The enforcement compares two fields of
the **same source record** — `rights_status` against the source's own `asset_use` label — so it
fires only when an author has recorded the violation. **The pair has never existed here: 38 of
64 sources have unresolved rights and every one declares `cross_check` or `text_only`**, while
the three that declare `geometry` are a survey and two maps, all clear. The labels are honest;
the rule is about a derivation and the mechanism is about a declaration.

**Asked of the town instead**, using the read-sets the generators already declare
(`CONSUMED` in each `*_params.py`, the same definition `check_geometry_declarations` uses, plus
the footprint polygon `from_phase` reads): **49 geometry-bearing attributes on 21 records cite
an unresolved source** — 43 on buildings, 6 on the terrain spec — and **19 of the 20 buildings
have a baked master in the tree**. **35 of the 49 stand on unresolved support alone** and **16
of those are graded `attested`**: the Sauganash Hotel's storeys and construction, the Wolf
Point Tavern's frame addition and painted sign, the Green Tree Tavern's footprint, roof and
paint, St Mary's Church's footprint, the Western Hotel, Miller House, and the west and south
division levels on the ground.

**What this parcel refuses to decide.** Whether a dimension read out of a copyrighted page is
an "asset derived from it" is a rights reading, and this project's own documents disagree —
`docs/PLAN.md` reads it narrowly (images, *"before any derivative texture"*), AGENTS.md and
PROVENANCE.md broadly. The two readings give opposite answers for all 49, so the gate holds the
population where it is and the reading goes to the owner; three routes are written up in
ROADMAP K41.

**What shipped:** `tools/measure_rights_derivation.py` and its 49-entry bank, four assertions
(the old label test kept, plus new-fault, no-ghost and no-worsening on the bank), all five
failure modes exercised by `--self-test` in `tools/check.sh`. **The residual is named and
counted on every run:** `data/flora` carries **202** citations of an unresolved source and
`data/fauna` **30**, both rendered, neither with a declared read-set — K42.

**Not verified here:** the desktop half of the smoke (~13 min against a 10-minute per-command
ceiling). `tools/check.sh` and the mobile half of `--published` are green. **No record, asset,
parameter or renderer file changed.**

## Measured 2026-08-16 — it is 189, not 195; this runner reproduces the nightly's bytes on every one of them; and the rewrite is not scheduled, it is open

**K40**, and it moves no asset. K39 could not verify its own record the obvious way — by
regenerating a derivative and comparing bytes — because `tools/web_derivatives.sh` did not
produce the bytes on the site. It reported a **lower bound of 195** from a vertex signature
and named the exact count, the price and the decision as this parcel. All four questions are
answered from a control that runs the step itself over all 334 masters, chunked into four
3 min 21 s passes to fit the harness's ten-minute per-command ceiling. That loop is now
`tools/measure_web_reproduction.py` rather than something every parcel reinvents, and it
refuses to write into `assets/` under any flag.

**The exact count: 142 of 334 reproduce.** The 192 failures decompose with nothing left over
— **189 come back byte-for-byte under `BAKE_PALETTE=1`** (the palette-era set) and **three
were already owned by name**: K37's two placeholders that compress smaller, and
`terrain__e1834_harbor_cut.glb` at 14 bits against a 16-bit ask, which is R-W6(b).

**And the sentence the no-Blender strategy rests on is true after all.** Bake PR **#175**
(07:34 UTC) rewrites **280** derivatives and holds all 192; on the 189 the nightly's bytes
and this runner's are **md5-identical, 189 of 189**. The bake's 280 decompose exactly — 189
palette-era + 90 placeholder masters upgraded to canonical archetype bakes + 1 terrain at
16 bits — so a binary diff nobody could review now has an arithmetic. What was wrong was
never the extraction: **K36(b) carried a step change through 38 files and not 334.**

**K39's vertex signature is refuted as an identifier**, in both directions: 189 shared, **six
welded files today's step reproduces exactly** (`optimize` dedups without the palette pass)
and three failures with no weld. 195 is a number to stop quoting, and no gate is built on it.

**The price**, for the record: +48,836 bytes over the 189 (mean +258, all 189 grow), +48,328
net across the tree — **0.18 % of the 25 MB budget**. K39's sample said +197 and 30 %
reproduction; the truth is +258 and 42.5 %.

**Two decisions.** *Who moves the 189*: nobody here — an open PR already holds those exact
bytes, and this parcel neither regenerates them nor merges that PR. **#175 and #164 carry no
status checks at all** because a bot-opened PR does not trigger the dev gate; running it
against them is the janitor's job and the owner's call. *Should the record name the STEP*:
**no.** A flag string is prose and can be edited to turn a gate green; a script hash would
have invalidated all 334 entries on each of the four commits that have changed the step,
**twice on a commit that moved no byte** (38, 3, 0, 0). What the failure needed was a rule,
and it is in the step's header: **a change that moves any derivative's bytes regenerates all
334, not the ones that visibly broke.**

**Not verified here:** the desktop half of the smoke (~13 min against a 10-minute
per-command ceiling). `tools/check.sh` and the mobile half of `--published` are green. **No
asset, record, parameter or renderer file changed.**

## Fixed 2026-08-16 — the shipped model now records the model it was made from; and 195 of them were made by a step this repository no longer has

**K39.** K38's residual was that staleness was still a **timestamp**: `tools/publish.sh`
compared mtimes, and on a fresh clone `git checkout`'s write order makes **334 of 334**
masters older than their derivatives, so the scan was silent on exactly the tree a run
starts from. A master rebuilt with the same geometry and different `_CONFIDENCE` values —
the case the script's own comment was written about — passed that scan and all eight
content assertions alike.

**What moved.** `tools/web_derivatives.sh` records `name → sha256(master)` as it produces
each derivative, into **`assets/manifest.web.json`**, beside `assets/manifest.json`: the
manifest records data → master and is written by the Blender build, this records master →
derivative and is written by the step after it. **Assertion 9** compares the recorded hash
to the master in the tree, absolute in both directions — a moved master fails, an
unrecorded derivative fails, an entry with no file fails. Exercised on the real tree, not
only in memory: one byte appended to a master makes the gate fail by name and
`tools/publish.sh` refuse before writing anything. `publish.sh` no longer scans mtimes at
all; it runs the gate. **There is deliberately no flag anywhere that rewrites the record
without regenerating the bytes** — the remedy is always `--only <name>`.

**The coupling was the real question and it is decided: the STEP writes it, every run, and
a bake carries the diff.** The record's lifecycle is the derivative's — same producer, same
run, same commit — so a nightly rewrites it in the same breath and cannot leave the dev
gate red for everyone else. It is deliberately **not** in
`tools/web_derivative_baseline.json`, which is a record of faults a person banks by hand.

**AND THE CONTROL THAT WAS SUPPOSED TO VERIFY IT DOES NOT EXIST.**
`tools/web_derivatives.sh` says it *"reproduces 331 of 334"*. Measured: **6 of 20** in a
spread sample, and **all 14 that failed come back byte-for-byte under `BAKE_PALETTE=1`**.
`optimize`'s palette pass was **welding**, K36(b) turned the pass off for draw-call reasons
that stand, and it regenerated only the 38 assets whose material identity had broken. By
vertex signature — no `npx` needed — **195 of the 241 compressed derivatives carry fewer
vertices than their masters**, 10,513 vertices in total, and that is a lower bound.

**Nothing on the site is wrong**: a weld is lossless, triangles are equal, and assertions
1–9 are green on all 195. What is false is the claim that this runner can regenerate what
the nightly ships — true for 46 of 241 — and the consequence is scheduled: **the next bake
rewrites all 195 as unwelded files**, a 195-file binary diff with no number attached to it.
**K40** owns the count, the price and the decision, and the further question K39 declined:
whether the record should name the STEP as well as the master.

**Stated, not tidied:** the record was **seeded** in this commit, not produced by a full
run, because a full run would move those 195 files. One entry was written by the step (its
derivative came back md5-identical); the other 333 rest on assertions 1–8 and on the 93
passthroughs' byte identity with their masters. It does not claim the shipped bytes came
from today's step.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's
10-minute per-command ceiling). `tools/check.sh` and the mobile half of `--published` are
green. No committed asset changed a byte.

## Fixed 2026-08-16 — a publish step could put 1.2 MB of uncompressed models into the payload and the whole gate said CHECK PASS

**K38.** K37 noticed a third writer of `assets/web/` and declined to chase it:
`tools/publish.sh` copied any master through whenever it was newer by mtime. Chased, it is
worse than the note.

**It is reachable in one command, and nothing sees it.** Two compressed masters `touch`ed —
the state the tree reaches whenever `generators/build.py` is run on its own, which is the
case the script's own comment says the copy exists for — then `tools/publish.sh`:
`fort_dearborn_palisade` **114,768 → 841,836 bytes** and `dearborn_street_drawbridge`
**71,504 → 557,196**. **+1,212,760 bytes** into the payload, written into the *tracked*
source tree and mirrored to `site/`. On that tree the derivative gate exited 0,
`check_published.mjs` exited 0, and the full `tools/check.sh` printed **CHECK PASS**.

**And it could not have been otherwise.** A master copied over its own derivative has that
master's triangles, node identity, contract attributes, bounding box (zero rungs) and
material table, and a byte count that is equal rather than larger. K36(a)'s eight assertions
watch the *transformation* `assets/gltf/ → assets/web/`; they cannot see a file that skipped
it. **A gate written against a transformation is not a gate on its output directory.**

**It is not three writers — it is three scripts and four passthrough branches**, three of
them silent: the size rule K37 decided (93 assets), `optimize`'s failure fallback,
`gltf-transform`-unavailable copying **all 334** (payload 4.54 → 20.96 MB, 4.6× against a
25 MB budget), and `publish.sh`'s mtime copy. **And mtime never compared a byte:** on a fresh
clone **334 of 334 masters are older than their derivatives**, by `git checkout`'s index
order, so the rule fires on any rebuild and is blind on the tree a run starts from.

**What moved:** no asset, no record. **Assertion 8**, absolute in both directions against the
93 passthroughs banked by name — a 94th fails whichever writer made it, and a banked one that
returns compressed fails and says to re-bank. Both `--self-test` mutations fire.
**`tools/publish.sh` is no longer a writer of `assets/web/`**: it keeps the scan, moves it
above the first write and refuses, naming each file and the `tools/web_derivatives.sh --only`
that repairs it. Verified end to end — the same two `touch`es now stop it at exit 1 with the
working tree clean.

**Stated, not tidied:** a new placeholder now needs `--write-baseline` in the commit that adds
it, because "the generator added one" and "something copied a master through" are the same
bytes and one of them is a decision. And refusing on mtime is still mtime — a master rebuilt
with the same geometry and different `_CONFIDENCE` values passes both the scan and assertions
2–7. **K39** is that residual: the step knows which master it compressed and writes it down
nowhere.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's
10-minute per-command ceiling). `tools/check.sh` and the mobile half of `--published` are
green. No committed asset changed a byte in this parcel.

## Fixed 2026-08-16 — the ninety unsqueezed files were right, and three squeezed ones were shipping bigger than the models they came from

**K37.** K36(a) reported 90 derivatives as byte-identical master copies and K36(b)'s control
found that the pipeline's own step does not reproduce them. Run over all 90, the step takes them
**520,700 → 628,028 bytes, +107,328 (+20.6 %)**, with **88 of the 90 growing**: `meshopt` writes
a compression header, a buffer-view table and an index buffer, and on a 16–60-triangle shed those
cost more than the compression saves. **The passthrough was the right answer; it was just nobody's
decision** — it fell out of `generators/inferred_placeholder.py` writing the same bytes into both
trees.

**And the class predicate is wrong in both directions.** `kind: placeholder` maps onto
"uncompressed" 90 of 90 today, and that is a coincidence of write order. Three assets that have
been through this step on every bake since it was written ship **larger** than their masters —
`fort_dearborn_root_house` +324, `lake_house_construction` +240, `fort_dearborn_magazine` +224 —
while `fort_dearborn_parade`, 5,504 bytes and 30 triangles, compresses −24.5 %, and two of the
ninety placeholders compress −9.3 %. Byte size does not predict the sign either. So the rule is
**keep whichever file is smaller, measured per asset**, and it lives in
`tools/web_derivatives.sh` rather than in a list of names.

**What moved:** three derivatives, replaced by their masters — **−788 bytes**, and they now carry
exact float positions rather than a quantised lattice. The 90 are untouched. **The gate:**
`measure_web_derivatives.py` assertion 6, absolute, **bound zero**, with a `--self-test` that
grows a derivative by one byte and confirms it fires *and* grows an epoch mesh by one byte and
confirms it does not.

**The one exclusion, by name:** `water__e1834_harbor_cut.glb` is +744 bytes (+55.0 %) under the
rule and is **not** passed through. The epoch meshes' bit depth is a geometric decision (R-W6),
the ground and waterline are what R-BUG3c, R-BUG4 and R-M1a measure against, and **R-W6(b) holds
both files** pending the owner's word on regenerating geometry outside a bake.

**Left open, stated:** the two placeholders that compress smaller stay master copies —
`inferred_placeholder.py` rewrites every placeholder into both trees on each run and would undo
them. **1,624 bytes.** And `tools/publish.sh` is a **third** writer of `assets/web/`: it copies a
master through whenever it is newer by mtime, which is a passthrough nothing decided and which
this gate cannot see. Worth a parcel.

**The gate's own self-test had been red since K36(b)** — rebanking the material ratchet empty
left one mutation with nothing to mutate, and it printed MISSED, so `--self-test` reported
SELF-TEST FAIL on a clean tree. Nothing noticed because `check.sh` ran `--gate` and never
`--self-test`. An inapplicable mutation now prints `skipped`, and `check.sh` runs the self-test
as its own step.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's 10-minute
per-command ceiling). `tools/check.sh` and the mobile half of `--published` are green. Nothing
here moves a vertex, a material or a pose.

## Fixed 2026-08-16 — the compression flag that hid 38 buildings' material names was also spending the town's draw-call budget, and half the anchors were over it

**K36(b).** K36(a) recorded the palette pass as a fault about NAMES: `gltf-transform optimize`
folds the named materials of any file carrying five or more of them into one `PaletteMaterial`
plus generated PNGs, so 38 shipped assets lost `log`, `chinking`, `board`, `roof`, `dark`,
`interior` on the way to the browser. The pass's own justification is that merging materials
saves draw calls, so the reading was that names had been traded for speed. **Neither was true.
It cost both.**

**FINDING 1 — a generated map makes an asset unbatchable.** `materialKey()` in
`renderers/web/js/buildings.js` includes `m.map?.uuid`, and a GLTFLoader mints a fresh uuid per
loaded texture, so a palette asset cannot join any batch — not the town's, and not another
palette asset's. The 38 shipped as **40 single-building batches** (40, not 38: `sauganash_hotel`
came out with three `PaletteMaterial`s, its glass and shutters refusing the merge) on top of the
town's 16. **The published town drew 56 batches. R-W5a's committed figure is 16.** With the pass
off: 56 → 16, textures in memory 55 → 41, shader programs 15 → 12.

**FINDING 2 — R-W5a's numbers were taken on the source tree.** Its *"no map of any kind"* was
true of what this repository bakes and never true of what the site serves — the identical error
K36(a) found in R-W2a's material sheet, from a different parcel, three days apart. R-W5a's
result stands (47 → 16 is real, and is what the 40 now fold back into); its "16 batches" was
never a statement about the site. `tools/measure_shipped_batches.mjs` reads the **mirror** by
default and prints which tree it read, so there is no third time to have.

**FINDING 3 — four of the eight scene anchors were over the 80-call budget on the site.** A
batch holding one building is culled with that building, so this is paid per pose and is worst
where the town is densest. At 1280×800, through the renderer's own `goTo`:

| | green_tree | forks | from_above | south_water | lake_market | s'nash_wing | f_post_office | sauganash |
|---|---|---|---|---|---|---|---|---|
| before | **102** | **96** | **84** | **82** | 71 | 68 | 66 | 62 |
| after | 70 | 68 | 63 | 69 | 63 | 61 | 60 | 59 |

Nothing had measured it: the smoke reads the counter at whatever pose it is standing in, and
`critic_shots.mjs` reports draw calls per station without asserting on them.

**The cost is 187,392 bytes** — the 38 go 318,540 → 505,932 (+58.8 %), because 197 named
materials take more room than 75 generated PNGs. That is +4.1 % on a 4.5 MB tree against a
25 MB budget. `material identity: 334 of 334`, and K36(a)'s ratchet is rebanked empty.

**`tools/web_derivatives.sh` is the structural half.** The web-derivative step is lifted out of
`tools/bake.sh` whole, so a Blender-free runner can regenerate derivatives from the committed
masters and measure them — link 2 could be *found* broken by K36(a) and not *repaired* without a
nightly. The control that makes this attributable: under `BAKE_PALETTE=1` it reproduces **243 of
334 derivatives byte-for-byte**, including all 38.

**The other 91 are two findings this parcel did not fix and did not hide.** **K37** — 90
derivatives are byte-identical master copies, and the pipeline's own step does not reproduce
them: it makes them ~21 % *bigger* (4,968 → 6,000 on the sample). Nothing states which
behaviour is intended. **(K37 is DONE 2026-08-16 — the passthrough is correct, measured over all
90 at +20.6 %, and the sample generalised; see the section above.)** **R-W6(b)** — the shipped
terrain is still **14-bit**: regenerating the
committed master at 14 bits reproduces `assets/web/terrain__e1834_harbor_cut.glb` md5 for md5,
and the 1,116-byte gap to the 16-bit file is exactly R-W6's own quoted cost. **R-W6's fix is in
the script and not in the file a visitor downloads**, so the ground is still on the 306 mm
lattice R-BUG3c found buries the road. Both are open parcels in `docs/ROADMAP.md`.

**Not verified here:** the desktop half of the smoke (~13 min against this harness's 10-minute
per-command ceiling). `tools/check.sh` and the mobile half of `--published` are green, and the
desktop draw-call numbers above are measured at 1280×800 by the new tool.

## New 2026-08-16 — the town on the site has 75 textures, and the repository has none

**K36(a).** The geometry a visitor downloads reaches them along four links —
`data/` → `assets/gltf/` (the masters) → `assets/web/` (the shipped derivatives) →
`site/chicago/4d/` (the published mirror). Link 1 is gated by the staleness check, link 3 by
`check_published.mjs`, and **link 2 was gated by nothing at all**: no hash, no count, no
assertion tied a shipped derivative to the master it was compressed from. It is also the link
with the moving parts — two `gltf-transform` passes — and `tools/bake.sh`'s own comments record
what has already come out of them: *"a bug that collapsed every building to a two-metre box
shipped past a fully green gate — twice"*, and a `--texture-compress ktx2` flag that *"silently
turned every derivative into an uncompressed copy of its master, in every environment, since
this step was written"*. Both were found by a person reading the script.

**FINDING 1 — the shipped town is textured and the baked town is not.** `optimize`'s palette
pass folds the named materials of **38 of the 334 assets** into a single `PaletteMaterial001`
carrying generated PNGs: **75 textures exist on the site that exist in no master**, and the
names they replace — `log`, `chinking`, `board`, `roof`, `dark`, `interior` — are gone from the
file a browser loads. Among them the Sauganash Hotel, the Wolf Point Tavern and its stable, the
log jail, the estray pen, Cobweb Castle, the council house and eleven `recon_*` reconstructions.

**The split is a COUNT, and it is exact.** Every asset whose master carries **five or six**
materials is faulted — 31 of them `log_dwelling`, 6 `outbuilding`, 1 `frame_tavern` — and every
asset carrying **four or fewer** is clean, all 296 of them, with no exception in either
direction. That is the palette pass's own threshold rather than anything about logs (the tool
names its output `PaletteMaterial001` and its documented minimum is five materials). So **the
fault grows with the town on a boundary 275 assets are sitting exactly one material short of**:
an archetype that gains a fifth surface — which is precisely what R-W2b is for — moves every
asset it paints across the line. The ratchet is what makes that arrival loud.

**FINDING 2 — R-W2a's material sheet is a sheet of the masters, and it says so in the wrong
words.** `docs/RESEARCH/materials.md` opens by reasoning that *"the source and the shipped bytes
have disagreed in this project before … a sheet that inventories intentions is worth nothing to
a bake"*, and then measures `assets/gltf/**/*.glb` under the heading *"the surface census,
measured from the shipped GLBs"*. Those are the masters. Its **"nothing in the town carries a
texture of any kind"** is true of what this repository bakes and false of what the site serves,
and **R-W2b — the next pick in that lane — plans to wire an atlas onto the material names that
the publish path deletes on 38 assets.** The sheet is corrected in place; none of its five
findings moves.

**FINDING 3 — 90 assets ship uncompressed and nothing says so.** They are exactly the 90
pure-Python placeholder GLBs, which `generators/inferred_placeholder.py` writes byte-identically
into both trees; the 244 Blender-baked assets compress 5.29×. It is 508 KB, 11.4 % of the
payload, and not a problem today — the point is that the bake reports a fallback copy as a
warning line in a log nobody reads, and the only committed instrument that could notice is a
25 MB total-size budget the tree is nowhere near.

**WHAT DOES NOT MOVE, MEASURED.** Triangle counts are identical on all 334 pairs, so
`--simplify false` has held; node names, `structure_id`/`phase_id` extras and mesh names all
survive; `_CONFIDENCE` — how a visitor is told which parts we made up — reaches the site on
every asset that carries it. The world bounding box agrees to at worst **2.63 rungs** of an
asset's own extent (0.107 mm on a 2.7 m shed), and the terrain's 82.8 mm is **1.08 rungs** of
its 5,020 m box, consistent with the 76.6 mm lattice R-W6 committed. **Corrected 2026-08-16 by
K36(b): a "rung" there is `extent / 65535` by the gate's own definition, not the file's actual
lattice, and the shipped terrain is 14-bit — so 82.8 mm is consistent with a 306 mm lattice too,
and that is the one a visitor is standing on. See R-W6(b).**

**The gate is `tools/measure_web_derivatives.py --gate`, in `check.sh`, at 0.2 s and with no
decoder** — every claim above is answerable from the glTF JSON chunk. Five absolute assertions
(bijection, triangles, identity, contract attributes, bounding box) and one ratchet
(`tools/web_derivative_baseline.json`, the 38). All eight failure modes were broken deliberately
in `--self-test` and each fires. **The repair is K36(b)** — it regenerates 334 binary files, so
it is a separate parcel and it does not need Blender. **DONE 2026-08-16, and it turned out to be
about draw calls rather than names — see the top of this file.**

## New 2026-08-16 — the constraint this project puts above the work was kept by the buildings and not by the people

**K34.** AGENTS.md's standing constraint is the one sentence in this repository that outranks
the rest of it: the final removal of the Potawatomi from Chicago is **August 1835**, inside the
first target year, and it is *"not a research gap to be filled by inference"*. It is given
exactly one mechanism — **`review_required: true` on any record blocks a scene from being marked
`released`** — and nothing had ever measured what that sentence covers.

| layer | carries the flag | did it block a release? |
|---|---|---|
| `data/structures/` | **9** of 332 | yes |
| `data/residents/` households | **7** of 173 | **no** |
| `data/residents/` persons | 0 of 209 | **no — the layer was never read** |

**FINDING 1, AND IT IS ONE RECORD.** `hh_caldwell_billy` — Billy Caldwell, Sauganash, the
agency's interpreter and the namesake of the town's best-known tavern — carries this sentence
in its `research_note`, in the same words `hh_robinson_alexander` uses: *"It carries
review_required so that no scene containing it can be marked released before the consultation
the project has committed to."* **The field was `false`, and `git log -S` finds no commit in
which it was ever anything else.** The record has been promising the flag since it was written.
`touches_removal ⇒ review_required` — the one rule the validator did hold on this layer — could
not see it, because `touches_removal` was `false` too.

Both are `true` now, **on the record's own committed text and on nothing new**: the same note
already quotes Andreas putting this man at the head of the march to the Missouri. Nothing else
about the record moved, and the note now says the flags were false and that the paragraph above
them said otherwise.

**FINDING 2 — the seven households were safe by coincidence.** `validate.py`'s scene gate built
its blocked list out of `data/structures/` alone, while the error it prints on the *household*
side says any record touching the removal *"blocks a scene from being marked released"*. That
consequence did not follow. The households were covered anyway because **all 11 of their
`lives_at`/`works_at` links land on a structure that is flagged too** — a fact nothing required,
nothing measured, and nothing would have noticed the loss of. A flagged household with a null
`lives_at` and an unflagged workplace passed clean; that scene is now a committed self-test.

**FINDING 3 — the same sentence, read the other way, is a deliberate NO and not a defect.**
`chappel_infant_school`, `walker_meeting_house` and `watkins_school_house` each say
*"review_required is set false … but the call is worth a second opinion"*, and each is false.
So the gate tests **both directions** rather than "prose mentions the removal ⇒ set the flag".
A gate that could not tell finding 1 from finding 3 would have been an instrument arguing for
its own conclusion. What it leaves open is **K35**: three of the nine flagged structures state
no reason anywhere, and the building side has no field a reason could live in.

**FOUR ABSOLUTE ASSERTIONS AND NO RATCHET**, deliberately — a ratchet is the right instrument
for a fault being paid down, and this is a commitment. Prose matches field; `touches_removal`
implies `review_required` at household AND person level; the flag reaches the building
(11 of 11); and — behavioural, against the real dataset — a scene with `released` forced true
is refused for **exactly** the union of flagged ids across every layer, so a gate that restated
the rule cannot pass while the validator disagrees with it. `tools/review_constraint_baseline.json`
makes the asymmetry explicit: **adding a flag is free, clearing one fails** and names what
clearing it would mean.

**The gate was verified to fail, on four separate injections** — the Caldwell flag cleared
again, `cobweb_castle` unflagged under three households, a person given `touches_removal`
without `review_required`, and the validator reverted to structures-only. Each exits 1 with the
divergence named, and the restored tree passes.

**Verified:** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs`
green against the published mirror. **The desktop half was NOT run and is not claimed as
passed** — it needs ~13 minutes against this harness's 10-minute per-command ceiling, which the
ROADMAP's run-budget box records. This parcel changes no renderer file, no geometry and no
coordinate.

**What it did NOT do:** it moved no building, household or coordinate, invented nothing and
regraded nothing. No liberty is owed — `docs/LIBERTIES.md` records inventions, and there is no
invention here. It did not decide whether the three unexplained structure flags need a reason
field; that is K35 and it is an owner's choice, not a gate's.

## New 2026-08-16 — there is a bridge in this scene over a watercourse the scene does not contain

**T-E5(a).** The terrain spec defers four in-town water features under one shared phrase —
*"existence documented, geometry conjectural"*. Existence is a claim about a **place**; a scene is
a **date**. Nobody had asked the second question of any of the four, and they do not answer it
alike.

| dossier zone | feature | at 1835-07-01 | what dates it |
|---|---|---|---|
| 14 | The slough | **present** (inferred) | a structure this project already stands in the scene |
| 15 | **The public-square pond** | **not established** (inferred) | nothing — and one document argues both ways |
| 16 | The Frog Pond, Lake & LaSalle | present (inferred) | a newspaper, one year late to the day |
| 17 | The Wells Street marsh | present (inferred) | the sentence that gives the slough gives what it drains |

**THE SHARPEST FINDING IS NOT THE POND.** `slough_log_bridge` — *The Slough Log Bridge, Water
Street* — is a committed structure standing on 1835-07-01, and its own `documented_range` note
quotes the source running that crossing *"until after 1840"*. Zone 14, the slough it crosses, is
deferred and undrawn. **A visitor walks onto a timber crossing laid over open prairie**, and has
been able to since the bridge landed. That is not an argument for cutting a conjectural channel —
the depth and width are still unsourced and parcel (c) still owns them. It is the proof that the
four were never on one footing, which one shared phrase implied they were.

**On the pond the answer is `not_established`, and deliberately NOT "it was not there".** One
document, `chicagology_prefire273`, carries both sides, and nobody had noticed that it does.
**FOR:** its slough sentence has the stream draining *"the pond and the marsh extending up Wells
Street"* as a live feature of a drainage system whose bridge outlives the scene by five years.
**AGAINST**, and the deferral weighed none of these three:

1. **The quotation dates nothing** — *"was then a pond"*, a past tense against an **1857** present,
   in a document this project's own source record identifies as built on **Hubbard's Chicago as he
   found it in 1818** and **Davis's 1832** drawing.
2. **The dossier's own row says the wrong season** — row 15 reads *"seasonal … water 0.5–2 ft deep
   **in spring**"*, and the scene date is **1 July**. The row stated a season; the deferral read a
   scene.
3. **Two county buildings already stand on that block, before the scene date** — the **estray
   pen**, Chicago's first public building, on the south-west corner from **March 1832**, and the
   **log jail** on the north-west corner from the **fall of 1833**. A pound is not built in a pond.

**The buildings do not refute a pond — they BOUND one, and that is the whole result.** A
whole-block pond is refused by this project's own committed records; a partial one is untouched by
them and is exactly the deliverable T-E5's third question asked for, which no source reached can
supply. So the date and the extent are **one question** and neither is settled. `existence
documented, geometry conjectural` was true of a place and was being read as though it were true of
the scene, and the geometry it called conjectural is not a detail to fill in later — it decides
whether water stands under Chicago's first public building.

**T-E5's fallback is discharged and NO LIBERTY IS OWED.** Its instruction was to write a
`docs/LIBERTIES.md` entry saying the square is drawn dry if it could not be settled honestly.
Nothing was invented, no confidence moved, and the square was **already** drawn dry and already
recorded as such in text a visitor reads. What was missing was the reason, and the reason is now in
that same visitor-facing text — the four `why` strings `ground.js` renders. Prose in the spec is
stripped from the terrain's staleness hash, so it cost no bake.

**AND IT COST SOMETHING DOWNSTREAM NOBODY WOULD HAVE GONE LOOKING FOR.**
`data/fauna/zones/f04_marsh.json` rested **three claims** on the pond quotation as in-scene
evidence — muskrat `presence` and mallard `presence` were `attested` on **that quotation alone**,
the muskrat's note reading *"direct evidence of animals present in numbers at a named location
inside the scene box"*. It is not: it is evidence about a place at an unknown time. **No grade
moved**, and that is measured rather than convenient — what carries `attested` is Andreas's *"ducks
and muskrats in the marshes"*, and the marshes he names **are** the habitat this zone plants
(`z04_marsh`'s extent is a buffer of the mapped water, the river-shore strip, and has never reached
the square). The animal is attested in the habitat the scene draws and is no longer attested at a
named block the scene draws dry; the notes now say which of the two they mean.

**The gate was verified to fail, on four separate injections.** An undated deferral, an `inferred`
grade with its reasoning blanked, a zone number nothing defers, and a source that does not resolve
— each exits 1 with the divergence named, and the restored file passes. It holds the correspondence
in **both** directions, so a fifth in-town water feature cannot be deferred undated and a dating
entry cannot outlive the deferral it grades. Which zones it covers is **declared**, not sniffed
out of the prose `why`: a regex over prose reads like a rule until a name changes under it, which
is what R-W4a was and what the smoke's own `/terrain|water/i` filter was.

**Verified:** `tools/check.sh` green. `SMOKE_VIEWPORT=mobile node tools/smoke_renderer.mjs` green
against the published mirror. **The desktop half was NOT run and this is not claimed as passed** —
it needs ~13 minutes against this harness's 10-minute per-command ceiling, which the ROADMAP's run
budget section records. This parcel changes no renderer file, no geometry and no coordinate; what
it changes that a browser loads at all is four `why` strings in a sidecar and one changelog entry.

**What it did NOT do:** it modelled, moved and sized nothing — all four features remain deferred.
It edited no research dossier (those are committed verbatim, which is why the disagreement lives in
`docs/RESEARCH/public_square_pond.md`). And it did not answer **how much** of the square was wet,
which is **T-E5(b)** and needs a bake.

## New 2026-08-16 — the adoption rule nine block parcels supplied by hand is code now, and it changes nothing

**K28 is done**, and the honest headline is that **not one household, roof or coordinate moved**.
Since T-A9 on 2026-08-15, nine block parcels have refused a trade a second roof and every one of
them wrote the refusal down as *a choice rather than a rule*, because method rule 6 was silent on
three things at once. All three are decided and two of them are now gates.

**The settlement is permissive on the table and strict on the rate**, deliberately — settling all
three conservatively would have been caution dressed as method:

- **(i) tests 2 and 3 read two PROJECTIONS of the housing table, not a set of pairs.** The
  stricter pair reading is **refused**, on rule 6's own standard rather than on taste: requiring
  the pair refuses the **fourteenth labouring household** (T-A4's D1 west of the river, argued in
  exactly the projected form), which rule 6 names as one of the **four decisions its third test
  recovers** — and the same paragraph says a test that has to be told the answers is a preference.
  What the projections admit is measured, not waved at: **20 (family, division) pairs across 8
  trades** that this layer houses none of.
- **(ii) there IS a cap — one adoption per trade per block parcel.** A block is an artefact of the
  drawing rather than a unit of the town, which is the reason for the cap and not an objection to
  it: without one, the granularity of the plat sets the rate at which this census grows. It is
  also what makes (i) safe — the projections widen *which* roofs are eligible, the cap bounds *how
  fast* any of them may move a count.
- **(iii) test 1 means the trade's OWN committed text, not method rule 3's list of unbounded
  trades.** Being unbounded says where a number came from; test 1 asks whether the number is too
  low. Only the **carpenters and labourers** state it, so the laundresses' D2 and the teamsters'
  D4 are refused — **with the remedy named**: argue the floor in that trade's own argument, from
  the town, and the roofs follow.

**Both gates were proven to bite before merge**, against mutated copies of the programme rather
than by inspection: a second carpenter on `blk_south_water_wells`'s D4 and a laundress on
`blk_randolph_franklin`'s D2 — the two roofs nine parcels refused by hand — each fail with the
clause named. The floor predicate is **imported** from `tools/measure_adoption_tests.py` into the
gate rather than restated, so the report and the gate cannot drift apart about what a floor is.
That tool also no longer tells its reader the question is open, which it did in four places.

**All 21 standing block adoptions already obeyed the cap**, which is why nothing moved. The value
is that the tenth block cannot drift.

**What was and was NOT run.** `./tools/check.sh` — the dev gate — is **green**.
`node tools/smoke_renderer.mjs` was run at **mobile (390x780) only**; the desktop half **was not
run**, because a single foreground command on this runner is capped at ten minutes and the desktop
half takes about thirteen (K21, measured). This parcel changes one authored JSON's `method` prose
and two tools: **no renderer file, no record, no geometry, no coordinate, no material**. Say so
rather than implying both halves ran.

## New 2026-08-16 — one new household renamed 73 of 113 invented residents, not the 17-25 eleven parcels reported

**K20 is done.** `tools/generate_inferred_names.py` dealt each `(community, sex)` pool round **by
index**, so an invented name was a function of how many people sorted ahead of you. Eleven parcels
measured the resulting churn in passing and reported 17-to-72; every one of them was a single
sample at a single arbitrary point in a hash order. `tools/measure_name_churn.py` is the
instrument — it inserts a synthetic household **in memory**, re-runs the allocator and counts who
gets renamed — and over **240 insertions across all six trades** the distribution is not centred
near a fifth of the layer: mean **40.4** for a carpenter, **worst 73 of 113**, and only **1 of 40**
carpenter probes renamed nobody.

**The allocator is now insertion-local: worst 10 of 113 on the same 240 probes, mean 4.6.** Each
person has their own deterministic ordering of the pool and claims the least-used name they are
permitted, so a name depends on who you collide with rather than on how many people precede you.
A third of the improvement comes from **unwelding the given name from the surname**: a repeated
given name is what a town looks like and claims nothing, so it is now each person's first
preference with no ledger at all, while a surname — which reads as kinship — keeps the ledger and
the floor rule.

**The residual is the POOL, and the report proves that rather than asserting it.** Each probe
prints its bucket's pressure. At **0.14x** (pool with room) an insertion renames **at most one**
person — literally K20's acceptance criterion. At **2.03x** (36 surnames dealt to 73 men) it
renames up to ten, because there is no spare name at the floor. **Ten renames at 2.03x is a pool
that is too small; ten at 0.14x would be an allocator that is still not local.** Widening the
pools is evidence work — more named 1835 Chicagoans out of Andreas and the rolls — not a tuning
knob, and at 3x pressure the residual will climb again.

**A bug the fix exposed:** unwelding the two halves let two people draw the same pair, and the
first run shipped **two Alvah Hastings**. That is refused outright now and all 113 full names are
distinct — true by accident before, true by assertion now.

**The one-time cost is the whole layer**: **113 of 113 renamed across 101 household files**,
recorded as **L111**. It invents nothing new — same pools, same grades, same `name_basis`
citations and notes; a different invented name is the same claim about the same nobody.

**What was and was NOT run, stated rather than implied.** `./tools/check.sh` — the dev gate — is
**green**, including the new step (`measure_name_churn.py --gate`, ~2 s) and `compile_scene.py
--all --check` over the 331 regenerated sidecars. `node tools/smoke_renderer.mjs` was run at
**mobile (390x780) only, 214 passed / 0 failed**; the desktop half **was not run**, because a
single foreground command on this runner is capped at ten minutes and the desktop half takes
about thirteen (K21, measured). Nothing visual changed here — the diff is name strings in
records and sidecars, no renderer file, no geometry, no material, no coordinate — so the risk the
desktop half covers is not the risk this parcel carries. Say so rather than implying both halves
ran.

## New 2026-08-16 — the town has no chimney material, and no record anywhere says what a roof is made of

**R-W2a**, the material sheet, is written: `docs/RESEARCH/materials.md`. It is measured out of
the shipped GLBs rather than read off the generators, because the source and the bytes have
disagreed here before. **334 assets carry 1,353 material slots, resolving to 32 names, 41 base
colours and 18 roughness values.** Every one is `metallicFactor 0`, `doubleSided`, `OPAQUE`,
and carries no map of any kind — §1 item 9's "zero textures anywhere" is confirmed at the byte
level, not quoted.

**Two findings block texturing outright, and neither is a rendering problem.**

- **The chimney is not a material in this project.** `frame_dwelling`, `frame_storefront` and
  `log_dwelling` all build their stacks with `M_ROOF`, so **219 chimney stacks on 199 buildings
  are painted with the roof's colour**, `0.34, 0.30, 0.27` at roughness 0.90. The 90 inferred
  placeholders, meanwhile, ship a real `placeholder_chimney_brick`. The town has a brick
  chimney material and the archetype buildings do not use it — and `log_dwelling`'s own
  docstring argues that a frontier stack is stick-and-clay or fieldstone, a different object
  from a framed house's brick stack, which renders identically to it. Opened as **R-W2c**, and
  it opens with a research question rather than a palette.
- **No record states a roof covering.** 315 records state a roof *type* and 309 a pitch;
  **zero** say what the roof is made of. The board roof `outbuilding` argues for is separated
  from a shingle field by **0.03 of roughness and nothing else** — identical colour, identical
  name, in the shipped bytes. The repository's one direct attestation, the North Side school's
  "sheeted and shingled roof", is read by nothing. Roofs cannot be textured until an attribute
  exists to select the covering, and that is a schema change across 315 records.

**And one documented fact is committed, correct, and rendered by nothing.** `cobweb_castle`
carries `cladding: clapboard_part_way_up`, **`attested`**, sourced to `andreas_1884_v1` —
David McKee's "the agency-house being afterward clapboarded part way up". It is a
`log_dwelling`, which does not read `cladding` at all, and the value is not even in
`CLADDINGS`. `cladding` is stated on 27 records and read on 22.

**R-G1's "there is no roughness variation anywhere" is corrected, and the correction changes
what W2 builds.** Between surfaces there are already 18 argued values spanning 0.15 to 1.00.
What does not exist is variation *within* a surface: every square metre of every wall has one
roughness, which is why nothing reads as painted, weathered or wet. **The deliverable is a
roughness map, not better constants** — do not spend a round re-tuning the 18 numbers.

**What was NOT run, stated rather than implied.** This parcel changed no code, no parameter
and no record, so `node tools/smoke_renderer.mjs` was **not** run at either viewport and
`tools/publish.sh` produced no mirror change beyond the changelog. `./tools/check.sh` passed
green, and it is the dev gate. Nothing here has been rendered, because there is nothing here
to render.

## New 2026-08-16 — a building has been taken out of the town, and the town's public buildings are three

**T-I3(a).** The programme schedules six civic or public-service roofs and every generator has
refused to mass one since L93, on the ground that the archetype behind the family speaks only
garrison words. The refusal is now the research instead. **On 1835-07-01 the town's public
buildings with a roof are three — `log_jail`, `council_house`, `chicago_lighthouse_1832` — and
this project already had all three.** `estray_pen` is public and roofless. The enumeration is
`docs/RESEARCH/civic_public_buildings_1835.md`, and every citation in it is Andreas: **no new
source was needed and none was invented.**

**The finding is the fourth building. The court-house was not built yet.** 332 structures resolved
into the 1835 scene and 331 do; `cook_county_courthouse_1835` is re-dated to the fall and resolves
into 1836 instead. Its record said, at length and honestly, that nothing it had reached fixed a
month, and reasoned from a flat prior over a twelve-month window that the building was about half
likely to be standing. **The window was never twelve months.** Andreas's town-period narrative:
*"During the fall of the year (1835,) a one-story and basement brick court-house was erected on
the northeast corner of the square, on Clark and Randolph streets"* (scan p. 369). His chronology
lists it under 1835 at **November** (scan p. 1317). And the county Recorder *"removed his office
toward the end of October to the new building recently erected by the county on the public
square"* (scan p. 305). Three statements — a narrative, an index and a biography — and not one is
earlier than the fall.

**The dataset had already said so, in another file, for four days.** The physical-roof reconciliation gives this record `roof_count: 0` with the reasoning *"Production chronology places construction in fall 1835; no courthouse roof should stand on 1 July"* — committed 2026-08-12, one day after the structure record that stood the building on the square. So from 12 August one document in this dataset held the court-house unbuilt while another drew it, and nothing read the two together; the walkthrough's own release notes even carried the reconciliation's reading out to visitors — *"a courthouse that was not built until the autumn"* — while the walkthrough drew it. **The one that was right is the one with no citation at all.** The reconciliation's "production chronology" cites nothing; the record cites Andreas and says the opposite, because what it cited was a caption.

**The citation the record had was a picture.** It cited *"a section headed 'THE FIRST
COURT-HOUSE.' at scan p. 373"*. Scan p. 373 is a PLATE; those words are an engraving's caption,
printed under *"Copyright secured by A. T. Andreas, 1884."* The paragraph that carries the date is
four scan pages earlier. This is the second time in this project a citation has resolved to a
heading rather than to a sentence, and it is the whole cause: every gate here asks whether a
building is inside its lot, clear of the roadway, on permitted ground and clear of its neighbours.
The gate that asks whether it existed yet is the date gate, and a range authored from a caption
passes it perfectly.

**Two of the record's own hedges are settled and both say it was better than it knew.** It warned
that Andreas's north-east siting "is the 1837 BUILDING" and might be contaminating an 1835 record
— Andreas gives that corner to this one, in the sentence that dates it. It ruled out brick because
"the first brick building in Chicago is 1837" — that is the first brick HOUSE, and Andreas calls
this court-house brick. **Neither is applied. Both need the bake**, because a changed form value
stales the mesh; they are recorded on the record as amendments.

**No anonymous roof may claim to be a public building, and that is now asserted.**
`tools/measure_institutional_claims.py` runs in `check.sh` against every committed record rather
than only the ones a generator is about to write — **absolute zero** for the worship and civic
families, because they are enumerable, and a **ratchet at one** for the schools, naming the single
anonymous North Division school L93 records rather than deletes. All three halves were broken
deliberately before the gate was trusted.

**What a slot would have been spent on is not a building.** The crosswalk says the family spans
*"jail/blockhouse; engine/service; adapted offices"*, and every adapted office in Chicago that
summer was a room in somebody's private premises. The United States Land Office was open from May
1835 and transacting Beaubien's pre-emption four weeks before the scene date — and it was rooms on
the east side of Lake Street, with Andreas noting that the Register and Receiver *"were usually at
their private offices"*. The post office was a counter in Hogan's store. The county's own officers
were private until late October. Three guards added to `data/exclusions.json`, and
`first_fire_engine_house` amended because it dated the ENGINE while the HOUSE is later still.

**What is NOT done, and it is the number.** Three of the six I3 slots are a count of nothing, and
the target still says six. The inventory's arithmetic is closed — family targets sum into
district-group rows, rows into district targets, districts into `roof_total: 665`, and
`reconcile_665.py` asserts all three — so the three cannot simply be removed. The two exits are
two different claims about the town (662 roofs, or three roofs that were not civic), the research
settles neither, and choosing one would invent exactly the kind of aggregate this parcel just
removed. **T-I3(b), blocked on the owner.** Also unmoved: `estray_pen`'s phase id still reads
`pen_1833` after its year was corrected to 1832, because a phase id is half of a baked asset's
filename.

## 2026-08-16 — the buildings in the streets are drawn wrong, not placed wrong, and the town's georeference is exonerated

**K30(b)**, the attributing half, and it moved nothing. K30(a) measured 29 buildings lapping
a platted corridor and left the deep cluster without a cause. The cause is now a command,
`tools/measure_corridor_intrusion.py --reflect`.

**The suspect this project named is refuted, by arithmetic.** South Water is georeferenced
through modern Wacker Drive, which was built on made ground, so a displaced centreline would
displace every record on that street alike. It does not: the 13 deep South Water anchors
stand **11.64–15.30 m** from the committed centreline against a platted half-width of
**12.192 m**. The corridor and the placements agree to about a metre, the disagreement has
**both signs**, and a displacement that explained a 4.51–8.17 m intrusion would have to be
4.51–8.17 m.

**The cause is two conventions that were never reconciled.** The derivation convention puts
a record's point on its FRONTAGE — the position notes say *"offset 12.2 m, half an 80 ft
platted street"*. The drawing convention puts local `(0, 0)` at the polygon's minimum corner,
so the body grows north and east from that point; **331 of the 333 committed footprints do
it.** A south-side building with its point on the south kerb is therefore drawn into the
roadway **by its own full depth**. All 13 deep South Water records declare the south side and
all 13 are drawn northward from the kerb; across the whole table, **all 17 deep records have
their body drawn toward the street from their own anchor**. Reflecting each body about its
own point takes **12 of the 17 under 1 m**, five of them to exactly zero. K30(a)'s recentring
was the wrong operation on the right suspect — it moves a body half its depth, and cannot
clear a fault whose size *is* its depth.

**The shallow tail is answered and is not to be fixed.** Once a body is drawn on the correct
side of its own point, what is left in the roadway **is how far that point stands inside the
corridor** — to within **0.10 m** over the six records the law covers. So the two terms are
separable and unequal: the drawing term is a building's depth, 4.51–8.17 m; the point term is
**0.35–1.69 m**, which is what a derived corridor and a hand-traced centreline disagree by.
`tremont_house_1`, `exchange_coffee_house` and `western_hotel` are their point's penetration
and nothing else, and their bodies are **already drawn correctly** — reflecting them sends
them 12 m into the road, which is the check that the law is about the point. Twelve nudged
buildings would have bought nothing.

**A bridge in a street is not a building in a street.** `slough_log_bridge` is now
categorised as street furniture — derived from its own archetype *and* function, never from
a list of ids — and its row stays in the table, in the baseline and under the ratchet. The
exemption's obvious abuse is to relabel a store as a bridge, so the gate refuses any category
change; `peck_store` was disguised as a `bridge_timber` crossing before the rule was trusted
and the gate caught it.

**What is NOT done.** Nothing was redrawn. The repair changes footprints, so it changes every
affected mesh and needs a bake the improve runner cannot do — that is **K30(c)**. Three deep
records are not the frontage fault and are named rather than averaged in:
`newberry_dole_warehouse`, whose point is 7.00 m inside the corridor and whose own note says
its bank is disputed; `hogan_store`, derived to the Lake/Market junction at the wedge; and
`temple_building`, which improves but does not clear. **No coordinate, dimension, footprint or
confidence moved, and nothing was invented.**

## 2026-08-16 — 29 buildings are drawn standing in the town's own streets, and every one of them was placed by hand

**K30(a)**, the measuring half. T-A9 found three documented stores inside the South Water
Street corridor and T-A12 found two more, and the entry that collected them asked for the
distribution rather than the anecdotes. It is a command now —
`tools/measure_corridor_intrusion.py` — and `tools/check.sh` runs it.

**29 of the town's 332 placed phases lap one of the 13 platted corridors.** 16 have their
centroid in one, which is T-A7's test; 9 have their authored position point in one. South
Water carries 14 of the 29 and the deepest at **12.10 m**, but the set spans **eight**
streets — Randolph, Clark, State, Lake, Dearborn, Wells and Canal as well — so
"all of them are on South Water" does not survive the full measurement.

**Every one of the 29 is a `research`-layer record.** Zero of the anonymous reconstruction
roofs and zero of the inferred-household roofs lap any corridor. Every generator has asked
`plat_corridors.intrusion()` before placing anything since K7, and this parcel commits that
as an **absolute** assertion rather than a ratchet: a generated roof in a roadway is a
regression. Both halves of the gate were broken deliberately before being trusted.

**The depths are bimodal, and the gap is the finding.** Nothing at all sits between 1.98 m
and 3.48 m: 17 records deep, 12 shallow. **13 of the 17 deep are South Water.** The shallow
tail is spread over six streets at ≤ 1.98 m, which is what a derived corridor and a traced
centreline can honestly disagree by — T-A7's "a metre or two proud of its own frontage". The
deep cluster is not that, and it has no attributed cause yet. *(K30(b), the entry above,
attributed it the same day: the cause is the drawing convention, and the shallow tail's
"metre or two" is now measured at 0.35–1.69 m rather than described.)*

**Two numbers that were quoted and do not reproduce.** T-A7's *fourteen* records with their
centroid in a roadway is **16** — measured at `52641c46`, the commit that states it, as well
as today, and it is the same 16 both times, so the layer has not grown. And two of the four
buildings T-A7 names are printed against the wrong street, because a centroid at an
intersection is inside **two** corridors and nothing said which to report.

**The one systematic cause that could be tested here was tested and is refuted.** The
position sits at the footprint polygon's origin, which is a vertex on 332 of 333 records, so
a building derived to a street corner is drawn with a corner on that point — a good enough
mechanism that 20 of the 29 anchors stand on legal ground while the body reaches into the
street. Centring every footprint on its own anchor clears 5, improves 14 and makes **10
worse**, the Tremont House by 7.59 m. `--recentre` keeps the refutation runnable.

**What is unverified:** the desktop half of `tools/smoke_renderer.mjs`, for the usual reason
— the harness's ten-minute per-command ceiling (ROADMAP, "the run budget"). `tools/check.sh`
passed and the mobile half passed against the published mirror. This parcel ships no data,
renderer or scene change, so there is nothing in it a browser could load differently: **no
record, coordinate, dimension or confidence moved**, and no building was touched.

## New 2026-08-16 — every card's dossier link was a 404 on the deployed site, and 30 of them should never have been links

**K26.** Each building card ends with a link to the research write-up behind the building, and
`popup.js` composed it as a path relative to the walkthrough. `tools/publish.sh` leaves `docs/`
out of the payload by design, so **all 332 links 404'd on the deployed site** — measured, not
reasoned about: `…github.io/custom/chicago/4d/docs/RESEARCH/sauganash_hotel.md` returns 404 and
the same dossier on GitHub returns 200. The link resolved in the source tree, which is the one
place it was ever clicked.

**The link is now absolute and goes to GitHub**, which renders markdown; `main` rather than `dev`,
because that is the branch a visitor's copy was promoted from (0 of the 55 distinct dossier paths
currently linked are dev-only, so the lag is nil today).

**The 30 are the finding the parcel did not predict.** The compiler asserted
`docs/RESEARCH/<id>.md` by convention and never asked whether the file existed — right about 302
records, wrong about 30, every one a *documented* building whose write-up has not been done (the
courthouse, the log jail, the estray pen, St Mary's, the Temple Building, the Presbyterian church,
Kinzie & Hunter's warehouse). Those cards now say *no dossier written for this building yet* and
offer no anchor. The 30 remain a research debt and `tools/check_dossier_links.py` names them every
run.

**Why it survived:** the smoke asserted the card's TEXT contained the path, which was true on every
run while every link was broken. It now reads the `href` and asserts it leaves this origin, with
`temple_building` as the discriminating no-link case. `validate.py` had gated the *open question*
dossier pointer's existence since it was written; the building card's pointer never had it.

**What is unverified:** the desktop half of `tools/smoke_renderer.mjs`, for the usual reason — the
harness's ten-minute per-command ceiling (ROADMAP, "the run budget"). `tools/check.sh` passed and
the mobile half passed against the published mirror, **219 passed / 0 failed**. The two new
assertions were additionally run at 1280×800 against the same mirror by an ad-hoc script — both
green, zero page errors, in 7.5 s — so what is unverified at desktop is the rest of the suite, not
this parcel's own claims. That number is worth noting on its own: booting the published walk-
through and reading two cards at desktop costs seconds, and the desktop half's thirteen minutes
are its road-contrast and horizon captures. A test-name filter would let it run as two commands
that each fit.

**No geometry, dimension, coordinate or confidence moved**: 30 sidecars lose a path that pointed
at nothing, and the rest are untouched.

## New 2026-08-16 — the ground still stands over the road it carries, and the fix costs 1,116 bytes

**R-W6**, which expected to prove the horizontal artefact invisible and instead measured it on
South Water Street. R-BUG3c repaired the 306 mm VERTICAL lattice by reading heights back off the
heightfield at load; the same quantiser moves E and N, nothing corrects that, and a vertex
conformed at a displaced position holds the field's height for the wrong place.

**Measured at all 259,689 of the field's own sample points, after `conformGroundToField()`, by
interpolating the containing triangle in plan** — `tools/measure_terrain_horizontal.mjs`, with the
14-bit rebuild coming back **byte-for-byte identical to the file in `assets/web/`**, so the
numbers are the shipping ones:

| encoding | KB | lattice | plan displacement | drawn surface vs field (rms / p99 / max) | past the 22 mm road lift |
|---|---|---|---|---|---|
| master | 6296 | float | — | 1.3 / 3.8 / **7.7 mm** | — |
| **shipped, 14-bit** | 671 | 306.4 mm | **273.1 mm** | 2.1 / 7.9 / **46.3 mm** | **87** (44 dry) |
| **16-bit — taken** | 672 | 76.6 mm | 52.0 mm | 1.4 / 3.8 / **12.9 mm** | **0** |
| uncompressed | 6296 | float | 0.0 mm | 1.3 / 3.8 / **7.7 mm** | 0 |

**The closest over-budget sample stands 1.9 m from South Water Street's centreline** — inside a
10.5 m travelled track — **30.2 mm above the field, carrying a road lifted 22 mm.** That is
R-BUG3c's failure mode surviving its own fix, on the street the owner reported it from, at 1/5
the amplitude and on 0.03 % of the town. The mechanism is slope, not size: the 87 samples sit at
a median slope of **18 %**, and flat platted prairie cannot show this at any bit depth.

**The decision, made by measurement rather than preference.** The terrain keeps shipping
quantised — the uncompressed file buys 12.9 mm → 7.7 mm for 5.8 MB, and 7.7 mm is DECIMATION
every row carries — at **16 bits on the epoch meshes only**: +1,116 bytes, against +105.7 KB
(+2.4 %) measured for raising the whole payload to buy nothing measurable, because precision is
per-mesh and every asset that is not the terrain or the water already lands inside 4.8 mm
(median 0.5 mm). Two corrections ride with it: R-BUG3c's *"E and N move by up to 153 mm"* was
arithmetic and the measured figure is **273.1 mm** in plan; and 15 bits is *bigger* than 16.

**What is unverified:** the desktop half of `tools/smoke_renderer.mjs` — the ten-minute
per-command ceiling. The mobile half was run against a published mirror carrying the 16-bit
ground: **218 passed, 0 failed**. **No GLB ships with this parcel**: `assets/web/` belongs to the
nightly bake, so the ground a visitor loads stays 14-bit until `chicago-4d-bake.yml` next runs.

## New 2026-08-15 — 623 invented details cited a band the specification never wrote, and 42 of them were unfindable

**K33**, the other half of K25's subject, and it is worse in kind: not a value outside its band but
a value with **no band to be inside**. K25(a) opened it at 581 from the prose census. The measured
figure is **623 values on 227 of 249 records** — `paint` 220, `chimneys` 93, `board_gap_m` 69,
`plan` 46, `door`/`door_side` 37 each, `bays` 35, `porch` 23, `goods_door`/`goods_door_side` 8 each,
`gallery` 4, `shopfront` 1 — **and `roof_pitch_deg` 42.**

**The 42 are the finding, and the reason they were missed is structural.** Five families — A3, A4,
A5, W4, W5 — write their roof as *"gable or shed"*: a form with no slope in it. Every one of their
records still carried a note saying the pitch was a type-level choice within the family band.
K25(a)'s banded half could not see them because **a value with no band is never tested against
one**, so the tool walked past exactly the records where the fault is total rather than partial.
The generous keyword was a floor on the prose census; the *classification* was a second floor
nobody had named.

**Route 2 (split the note) was chosen, and route 3 was measured as unavailable.** Grading these a
level lower would stale 249 committed GLBs — `generators/mesh_inputs.py` hashes the confidence
FLOATS into the mesh input recipe, which is the same wall T-V1(b) and K25(b) sit behind. **Prose is
not hashed**, so the honest repair and the affordable one are the same repair here. That is a
coincidence and is written up as one, because next time it will not be.

**The note negates the lede rather than dropping a citation.** Every affected value is prefixed by
a generator paragraph reading *"the spec is cited because the invention is bounded by it"* — the
exact untrue claim — so a silent removal would have left the false impression standing. The
replacement opens `NOT BOUNDED BY THE SPECIFICATION, and the sentence above about the invention
being bounded does not hold for this value`, names the family and the field, and says the value is
the reconstruction generator's type default. Each parcel's own closing clause is kept verbatim.

**`tools/band_notes.py` is the single predicate**, imported by all five generators that author the
sentence and by `tools/measure_band_claims.py` that audits it — `family_bands.py`'s lesson, applied
before it could bite again. The assertion runs in `--gate` and `--strict` and is **absolute: no
baseline, no allowance**, deliberately unlike the K25 ratchet beside it, because a prose repair
costs no bake and can block nothing. **Proved in three directions before being trusted:** 623 red
against the pre-repair data, 0 after, and a hand-planted fresh offender caught. An unclassified
field carrying a citation also fails, so the next invented fitting cannot inherit one by default.

**Residual, stated rather than tidied:** `sources` on these 623 values still lists the spec while
the note now says the spec does not bound them. The spec IS the source of the family assignment
behind the archetype default, so it is not simply wrong — but the two fields no longer agree, and
that wants a decision rather than a sweep. **No value moved and no geometry moved:** 623 note
strings, one new tool, five generator call sites, one gate assertion.

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the
harness caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP,
"the run budget"). `tools/check.sh` and the mobile half both passed. This parcel changes **no
geometry, no dimension and no renderer code** — only note prose, which is stripped from every mesh
input hash in this project.

## New 2026-08-15 — it is 98 values, not 54, and 24 causes, not 98 — and roof pitch had never been measured

**K25(a)**, the measurement half. The parcel was scoped from an eave count taken on 193 records.
Asked properly — every reconstructed record in the dataset and every form value the crosswalk
authors a testable band for — **1135 values were tested against a band and 98 are outside it, on
80 of 249 records**: **54 eaves, 38 roof pitches, 4 storey counts, 2 footprints, 0 roof forms.**
The eave figure of 54 survived the widening by coincidence, and T-V1(a)'s 40 is its anonymous half.
**Roof pitch had never been measured by anything in this project**, and it is the second-largest
fault in the dataset's provenance.

**The 98 are 24 causes.** Thirteen (family, value) pairs hold all 54 eaves and **six degree
constants hold all 38 pitches**: 2.78 m against D3's 8–9 ft on 20 records, 2.05 m against D2's
7–8 ft on 10 and against **W4's 9–18 ft on 3** (the worst, +2.27 ft), 18.0° against D2's 4:12 floor
on 21. **Seven metre values account for all 54 eaves** — 2.05, 2.75, 2.78, 3.25, 5.05, 5.20, 5.35 —
which is the archetype table, not a measurement of anything. The generator picks the value from the
**archetype** and the note cites the **family**.

**Pitch is a unit mismatch and nothing else.** The crosswalk authors rise:run; the generator authors
whole degrees. 4:12 is 18.435° and the shed constant is 18.0°, so 21 D2 sheds sit **0.10 of a 1:12
step** under a floor they would have cleared had the value been authored in the band's own units.
All 38 are within one step.

**The sub-1-ft question K25 left open is decided: they are failures.** 46 of 54 eaves are within a
foot and nearness is exactly what a retyped constant looks like. The only slack in the tool is
1.5 mm for the metre round-trip.

**A second fault, reported and not gated.** The same sentence is on values the specification does
not bound at all — **`paint` on 227 records, 220 against a family that never mentions paint;
`board_gap_m` on 99 against a specification that names no board gap anywhere; `chimneys` on 150,
93 silent.** There is no band to be inside. The instrument is a keyword and therefore a floor, so
it prints rather than fails, and it is opened as **K33** with the decision it needs stated.

**`tools/measure_band_claims.py --gate` runs on every `check.sh`, as a ratchet.** The strict
assertion **fails today and is meant to** (`--strict`, exit 1, 98 findings); what gates is the
committed census in `tools/band_claims_baseline.json` — a new offender, or a committed one whose
value moved, fails. **Both halves were broken on purpose and proved to fail** before being trusted:
a planted 4.9 m D1 wall is caught as NEW, and repairing `recon_1835_north_d3_002` without rewriting
the baseline is caught as an unrecorded repair. The fault may shrink and may not grow.

**K25(b) is blocked exactly where T-V1(b) is blocked** — every offender is on a canonically baked
parcel, and the repair cannot pass the gate it must pass to reach the branch the bake reads. **No
dimension moved here.**

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the
harness caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP,
"the run budget"). `tools/check.sh` and the mobile half both passed. This parcel changes **no data,
no geometry and no renderer code**: what ships is one new tool, its committed census, one gate step
and documentation.

## New 2026-08-15 — the twins are all in one parcel, and 40 notes are wrong about their own source

**T-V1(a)**, the measurement half. R-G1 blamed `south_water` for a horizon of one gable repeated,
and that row had already been fixed twice before this parcel was claimed: the phase-one South
parcel samples its footprints, and all twelve `phase3` platted-block parcels sample footprint and
eave. Measured across all **218** anonymous roofs, **every twin in the town is in one parcel** —
`phase2_north_division_initial`, written before the sampling rule existed. Sixty roofs, twenty-three
families, **24 distinct massings; 36 of the 60 share a footprint AND an eave with another roof of
their own family**.

**THE CENSUS FOUND SOMETHING BIGGER THAN THE TWINS.** Every invented dimension carries the note
*"Type-level choice within the &lt;family&gt; band"*, and that sentence is the entire defence for the
invention. **40 of the 218 eaves are outside the band their own note cites** — 18 in `phase1_south`,
17 in `phase2_north`, 5 in `phase2_west`. The phase-one parcel is the sharp case: it samples its
FOOTPRINT and carries the sentence saying so, while its eave is still one constant per family. So a
record can hold a true sentence about its plan and a false one about its wall, in the same note
style, and nothing distinguished them. This is ROADMAP **K25**'s fault measured on a second layer;
**none of the 40 is fixed here.**

**`tools/measure_massing_variety.py --gate` runs on every `check.sh`.** Its subject is a sentence
the data itself makes: the 138 records that say `sampled deterministically` are held to it — inside
the band, unique within family and parcel. **Both clauses were broken on purpose and proved to
fail** before being trusted. Everything else it reports and does not fail, and the tool's docstring
says why in as many words: *do not read a pass here as "the town is a distribution"*.

**One real bug, fixed.** The eave floor that keeps an invented outbuilding tall enough to carry its
own door was `DOOR_HEADROOM_M = 2.05` — a **man** door — applied to every door-carrying family,
including the wagon doors on W1, W2, W5, F1 and A2. A wagon door is 3.00 m in the clear. It never
bit because those families stood at a retyped 3.42 m; the moment the North parcel sampled its band,
`recon_1835_north_w1_*` failed by name at 2.821 m with no header. `eave_floor(family, door)` now
asks `outbuilding_params.DOOR_SIZE_M` instead of carrying a hand-copied constant — the same fault
this parcel is about, in miniature. The 90 block records are **byte-identical** across the change.
The sampling rule itself moved to `tools/family_bands.py`, which both generators now import.

**T-V1(b) IS WRITTEN, MEASURED AND CANNOT LAND HERE — read its ROADMAP box before touching any
dimension on a baked record.** Wiring the North generator to `family_bands` was implemented and run:
every placement gate passed (no collision, no corridor intrusion, nothing off the terrain, nothing
over the 0.35 m relief contract), and it takes **36 twins to 0, 24 distinct massings to 60, and 17
out-of-band eaves to 0**. It was reverted because the sixty North GLBs are canonical Blender bakes:
changing a dimension stales all sixty, `validate.py --all` is the dev gate, there is no Blender on
this runner, and `chicago-4d-bake.yml` bakes **from `dev`** — so the fix cannot pass the gate it must
pass to reach the branch the bake reads. **That circle stands in front of K25(b) and every parcel
that would move a dimension on the 128 canonically-baked roofs.** Three routes are written up for
the owner; choosing one is a policy question and an overnight run did not make it.

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the harness
caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP, "the run
budget"). `tools/check.sh` and the mobile half both passed. **This parcel changes no data, no
geometry and no renderer code**: what ships is two new tools, one gate step, an import in the block
generator whose 90 records are byte-identical, and documentation.

## New 2026-08-15 — sixteen refusals were made against candidacies this layer never actually had

**T-A3h**, the backfill of `blk_randolph_dearborn` — the one block that landed before rule 6 had its
third test, and so the one block never asked who lived on it. The adoptions are the two the parcel
predicted: the **D3** on lot 0 to a twentieth carpenter's household, the **D1** on lot 3 to a
twenty-third labouring one. Inferred households **99 → 101**, persons **111 → 113**, adopted
anonymous roofs **102 → 104**, and **standing roofs unchanged at 322** — nothing was built, moved or
regraded. Recorded in **L109**.

**THE FINDING IS ABOUT THE ROOFS IT REFUSED.** The block also deals a **D4** and a **D2**, and both
print ADOPTABLE — the carpenters' "second roof" and the labourers', exactly as at eight blocks
before it. Nobody had asked what those verdicts are made of. This layer houses **one** carpenter in
a D4 and that household stands in the **North** Division; it houses **four** labourers in a D2 and
all four stand in the **North** or the **West**. Every carpenter and every labourer it houses in the
**South** Division lives in a D3 or a D1. **Neither second roof is a (family, division) pair this
layer has ever housed.**

**It passes because rule 6 says its three tests are independent, in as many words.** Test 2 reads
the set of families and test 3 the set of divisions, so a roof is admitted on a family taken out of
one division and a division taken out of another family. `tools/measure_adoption_tests.py --pairs`,
added here, prints the cost: **20 pairs across 8 trades are admitted by the projections and housed by
nothing**, and test 1 leaves exactly **two** of them adoptable — the carpenters' D4/south and the
labourers' D2/south, which are precisely the two roofs every second-roof refusal has been about.
Sixteen refusals across nine blocks were refusals of a candidacy assembled from evidence that is
never about the same roof twice.

**THE STRICTER READING IS NOT TAKEN, AND THE REASON IS COMMITTED RATHER THAN ASSERTED.** Requiring
the pair would refuse the **fourteenth labouring household** — T-A4's D1 in the West Division,
adopted when this layer housed labourers west of the river only in D2 shanties, and argued in
exactly the projected form. Rule 6 names that adoption as one of the four its third test *recovers*,
so a pair reading breaks the calibration the rule rests on. The tool reports a `pair housed` column
and gates nothing; **ROADMAP K28 now has three things to settle rather than two**, and the cap
question it was opened for may be a question about an empty set.

**What is unverified here:** the desktop half of `tools/smoke_renderer.mjs` was not run — the
harness caps a single command at ten minutes and the desktop half needs about thirteen (ROADMAP,
"the run budget"). `tools/check.sh` and the mobile half both passed. This parcel changes no renderer
code and no geometry; what a browser loads that is new is two `occupants` blocks and the names on
67 invented persons.

## Fixed 2026-08-15 — a quarter of the modelled land was never open to a builder, and nothing said so

**T-E2**, lane 3's first parcel after T-E1 registered the 1830 sheet. Two grounds outside the plat
are now refused: the **United States Reservation** east of State Street and the **sand bar across
the river mouth**.

**The number is the argument.** Of the **121.18 ha** of modelled land standing above the water
surface in this scene, **32.10 ha — 26.5 %** is one or the other: the reservation 22.57 ha, the bar
9.53 ha. Every gate this project had asked whether a placement cleared its neighbours, its lot
lines, the platted roadway, the modelled terrain and the relief. None of them asked whether the
ground was ever for sale. L107 found that hole inside the plat five days' work ago and closed it
for blocks; this is the same hole where it is four times bigger.

**Nothing moved, because nothing was there yet — and that is luck, not a rule.** Seventeen
structure records stand on the two grounds and all seventeen keep their places: the fort's stockade,
parade and eleven buildings, the garrison garden, the 1832 lighthouse, Beaubien's homestead and
barn, and the south pier, which touches both. **Zero anonymous roofs.** Every recipe so far has been
keyed to a platted block, and the reservation was never platted, so the ground was spared by the
order the work happened in. The gate lands green on the day it is written, and both of its
assertions were proved to fail before it was trusted: removing one permission fails it by name, and
shrinking the bar polygon to a sliver fails the under-coverage count with 11,100 cells.

**THE REFUSAL IS DOCUMENTED; THE BOUNDARY IS INFERRED, DERIVED, AND HONESTLY SHORT.** Andreas gives
the reservation as 75.69 acres, the southwest fractional quarter of Section 10 — unplatted, outside
the town's own eastern boundary, and under Beaubien's five-week-old pre-emption claim on the scene
date. Not one vertex of the polygon is authored: its west and south sides are the quarter's two
survey lines resolved from the single control point `wright_1834_gcps.json` **G1**, whose own note
has said since the datum work that Madison's line continues east as the reservation's south
boundary; its third side is the committed waterline the trace already calls the reservation's lake
shore. **The derived polygon comes to 65.70 acres against the documented 75.69 — 13.2 % short — and
it is not tuned to close the gap.** The candidates (a meander line east of the 1834 waterline, the
trace's own +/-20 m, a shore trace that leaves its window south of Madison) are named and none is
measured.

**So the polygon is a floor, and the floor is checked rather than trusted.** The gate re-counts, on
every `check.sh`, the cells of modelled land above the water surface that stand east of the west
line, north of Madison, south of the main stem and inside neither polygon. Today that count is
**zero** — the polygons reach every square metre of ground the terrain models there. **T-E3 extends
the terrain east and south, and that is the parcel this assertion exists to catch.**

**Still open, and honestly open:** four structures the 1830 plate draws — Mark Beaubien's,
Elijah Wentworth's cabin, La Framboise's cabin and store, Porter's log cabin — have no record, no
exclusion and no tested survival to 1835-07-01. T-E2 lists them as open questions rather than
inventing dispositions, in the new disposition table at the foot of
`docs/RESEARCH/chicago_1830_claims.md`. **Mark Beaubien's is the one inside the modelled area.**
The reservation's own residue is recorded too: the 562 cells the first pass flagged as
unclassified turned out to be entirely the waterline tolerance band, every one of them between
-0.10 m and 0.00 m, and none of them ground.

## New 2026-08-15 — the town's public square was being offered to invented houses, and two documented ones were already standing on it

**T-A16.** `blk_randolph_lasalle` — Randolph, Clark, Washington, LaSalle — was claimed as the last
open block entry on its row and **was not built**. It is **the public square**: Andreas calls it
*the square* and *the court-house square*, this project's own ground control names its corners
*NW / SE corner of the Public Square block*, and it carries the estray pen (its south-west corner,
March 1833, Chicago's first public building), the log jail (north-west, fall 1833) and the first
Cook County court-house (1835). The 665-roof programme was dealing it four invented private roofs —
an `A1`, a `D3`, a `D4` and a `D5`. The block is now **reserved**: no lots, no roofs, a refusal in
the block generator, and a gate in `check.sh`. **Standing roofs unchanged at 322; remaining 343, 1
of them on covered ground** (was 5 — the square held four of the five). The plat grid drops from
152 lots to **144**. Recorded in **L107**.

**EVERY PLACEMENT GATE THIS PROJECT HAS PASSED THE TWO BUILDINGS THAT WERE STANDING ON IT, AND THAT
IS THE HEADLINE.** `wright_building_to_let_a` and `_b`, John Wright's two documented cottages to
let, were placed in *"the South Division band the recipes use for ordinary dwellings"* and that band
ran across the square. Their placement was tested for clearance from other buildings, for its own
lot lines, for the platted roadway and for buildable ground — every question this project knew how
to ask about a position, and **not one of them was whether the ground was for sale**. They have been
moved: each takes the nearest free platted lot no committed block recipe has already spoken for, 83 m
and 69 m, onto the Randolph frontage of the two blocks facing the square. The pair is split, and the
split is stated — the only ground that kept them on one block was 200 m further off and faced two
different streets, and one advertisement offering two buildings never said they shared a holding.

**The defect is upstream of the schedule.** `tools/generate_plat_lots.py` subdivides every block it
can build, because that is what the Thompson module says a block is; it has no way to ask whether a
block was ever offered in lots. So the reservation withdraws the **lot lines** and not merely the
schedule's permission to use them, and `lots_per_face_withheld` records what the module would have
drawn so the withdrawal is visible rather than looking like a generator failure.

**THE RESERVATION IS `inferred` AND IS NOT PROMOTED.** No source this project holds states that the
square was reserved from sale. What it holds is the block's name, the county's three buildings on
it, the dossier's own reading of the rest of it — *"open, unimproved, fenced or unfenced prairie
block"* — and one period description of the ground itself: *"Our public Square was then a pond,
where the Indians had trapped the muskrat, and where the first settlers hunted ducks."* The grade
stays where the evidence puts it, and `tools/measure_reserved_ground.py` prints what a refutation
would change.

**THE POND IS DOCUMENTED AND IS NOT MODELLED — T-E5.** The terrain carries no standing water on this
block and the marsh flora zone is a buffer of the mapped water, so the square renders as dry prairie
with three public buildings on it. That is a second false statement about the same ground. It is
opened rather than closed here, with the three questions that have to be settled before any ground
moves.

**The eleventh K20 measurement is 0 of 111** carried-over invented persons renamed, against 12-of-110
at T-A15 and a range of 7 %–72 % over the nine before it. Zero for a structural reason: **this parcel
inserts and removes no person**, so the allocator has nothing to shift. That is the first evidence in
nine measurements about *what* perturbs it.

**Unverified here:** the desktop half of `tools/smoke_renderer.mjs` — this parcel changes data, tools
and docs only, and the desktop half does not fit the runner's ten-minute per-command ceiling (see
ROADMAP § THE RUN BUDGET). `tools/check.sh` and the mobile half of the smoke were both run green
against the published mirror.

## New 2026-08-15 — the block opposite the courthouse, and two of yesterday's three adoption candidacies do not reproduce

**T-A15.** `blk_randolph_clark` — Randolph, Dearborn, Washington, Clark — now carries **eight
anonymous roofs**: a store-residence, five dwellings, a woodshed and a privy, on six of its seven
free lots, with lot 1 left open and lot 0 held by the inferred gunsmith's shop. **Standing roofs
314 → 322; remaining 351 → 343, 5 of them on covered ground** (was 13). Inferred households 98 → 99,
inferred persons 110 → 111. Recorded in **L106**. **The recipe cleared every placement gate on its
first run** — the eighth block in a row. The block stands across Clark Street from the public square
(county courthouse, both Wright buildings to let, the estray pen) with Dearborn Street, the bridge
street, for its east face; it is the first block parcel dealt **both** larger house families at once
and the first to stand a **`C2` store-residence**. One adoption: the `D1` log cabin on lot 3 becomes
the twenty-second inferred labouring household.

**TWO OF T-A14's THREE ADOPTION CANDIDACIES DO NOT REPRODUCE, AND THIS IS THE HEADLINE.** The entry
directly below records that its `D2` passes all three of method rule 6's tests for the
**laundresses** and its `D4` for the **teamsters**. Tests 2 and 3 hold for both. **Test 1 does
not**: rule 6 asks whether the trade's *own argument* states in its committed text that its count is
a floor rather than a bound, and neither of those arguments contains any such statement — the only
occurrence of the word in the laundress argument is Andreas's *"with the floor covered besides"*, a
plank floor in a boarding house. Only the **carpenters** and the **labourers** state it.
`tools/measure_adoption_tests.py` is committed so the next parcel **runs** rule 6 rather than
recalling it, and prints the sentence each verdict rests on. The T-A14 entry below and L105 are left
standing verbatim; what is corrected is the method. **K28's question narrows**: not "may a trade
that has not asked for a roof be given one" but "does test 1 mean the trade's own text, or method
rule 3's list of unbounded trades" — two readings that disagree for exactly two trades. Run on this
block's `D2`, exactly one trade passes: the labourers, taking a second roof, refused for the eighth
time on the same conservative reading.

**The face rule reproduced exactly — the first time that can be said.** `tools/
measure_street_frontage.py randolph washington` returns Randolph 7 research / 7 inferred-household
against Washington 1 / 0, the same 14 against 1 T-A14 measured on the same pair, from a command
rather than from a memory. The third layer read 18 and 12 and is excluded, not merged.

**The face rule ranks dwellings, and this block had a store, so the rule was EXTENDED — see K32.**
A store-residence's claim on the better frontage was taken to be functional rather than social, so
the `C2` took Randolph's third free lot and the `D6` that would have had it went to the head of the
back street. That is an invention about 1835 commerce made by an agent; it is flagged rather than
left to repeat, and **K29 is circling the same question from the other side**.

**THE END RULE IS EXHAUSTED ON THIS ROW — see K31.** Distance to the Dearborn Street drawbridge runs
**318.3 / 321.1 / 325.8 m** across the Randolph frontage and 376.4 → 388.2 m behind. Far/near on the
front face is **1.02×** against T-A14's 1.11, T-A13's 1.13 and T-A12's 2.93, and the absolute spread
is **7.5 m** — under a third of one lot's 24.6 m frontage. The cause is geometric: the bridge bears
**10.4° east of north** from the block centre while the face runs east–west, so the criterion sees
only **18 %** of any along-street displacement. It was followed anyway on T-A13's reasoning, and on
this block a stronger criterion agrees with it (lot 6 is the corner on Dearborn, the bridge street),
which is exactly what K31 must not assume holds elsewhere. **Do not quote the end rule as if it
ordered anything on the Randolph–Washington row without re-measuring it.**

**Unverified here:** the desktop half of `tools/smoke_renderer.mjs` — this parcel changes data and
docs only, and the desktop half does not fit the runner's ten-minute per-command ceiling (see
ROADMAP § THE RUN BUDGET). `tools/check.sh` and the mobile half of the smoke were both run green
against the published mirror.

## New 2026-08-15 — a block with no front, and the face rule's first measurement does not reproduce

**T-A14.** `blk_randolph_franklin` — Randolph, Wells, Washington, Franklin — now carries **eight
anonymous roofs**, six principal, a stable and a privy, on six of its seven free lots, with lot 1
left open and lot 2 held by Harmon's log cabin. **Standing roofs 306 → 314; remaining 359 → 351, 13
of them on covered ground** (was 21). Inferred households 96 → 98, inferred persons 108 → 110.
Recorded in L105. **The recipe cleared every placement gate on its first run** — the seventh block in
a row — and it is the first block parcel of this shape to commit a tool, for the reason below. It is
the first block on the row **two streets back**, and the first **neither of whose faces the town's
record calls a front**.

**T-A13'S FACE-RULE MEASUREMENT DOES NOT REPRODUCE, AND THIS IS THE HEADLINE.** The entry directly
below reports **Lake 12, Randolph 2, South Water 9** for "every documented or inferred structure
whose footprint centroid stands within 25 m of a street's committed centreline". No filter
recoverable from this repository produces those numbers — the stated one gives **Lake 17 / Randolph 7
/ South Water 14** on the research layer alone — and the filter actually used was never written down.
The judgement it supported survives every filter tried (Lake is the better face by a wide margin);
what failed is **reproducibility**, which on a project whose product is provenance is the more
serious of the two. `tools/measure_street_frontage.py` is committed so the next parcel runs the
measurement rather than remembering it. **The T-A13 entry below is left standing verbatim**, and so
is L104: LIBERTIES.md is append-only and what is corrected is the method.

**The count reports its three evidence layers separately and never sums them.** The anonymous roofs
the block parcels themselves place stood at **15 on Randolph and 9 on Washington** when this
arrangement was chosen and read **18 and 12** the moment the parcel built — a face rule counting that
layer reads the programme's own output back as evidence. Excluded, this block's answer is **14
against 1**: Randolph carries 7 research-layer records and 7 inferred-household buildings, and
**Washington Street's entire documented 1835 frontage is the estray pen**, the town's pound for stray
animals.

**The end rule's spread has thinned for a second block running.** Distance to the Dearborn Street
drawbridge runs **527.8 m** at lot 6 to **584.0 m** at lot 0 on the Randolph frontage and **568.5 m**
at lot 7 to **621.0 m** at lot 1 behind. The far end of the front face stands **1.11×** as far from
the bridge as the near end, against T-A13's 1.13 and T-A12's 2.93, and the front face's absolute
spread is **56.2 m** against T-A13's 68.2 m. Followed anyway on T-A13's reasoning, and recorded as
closer to arbitrary than ordered.

**The "second roof" question has been the wrong question for six blocks.** The D4 and D2 that every
block since T-A9 has refused as *second* roofs for the carpenters and labourers are also the
**first** roofs of the **teamsters** and the **laundresses** — the other two of method rule 2's four
unbounded trades, each housed in that one family and no other, each already in the South Division,
each passing all three of rule 6's tests on those roofs. **Sixteen anonymous D2 and D4 roofs stand in
the South Division under exactly that description.** K28 is settling a larger question than it was
opened on: not whether a trade may take a second roof, but whether rule 6 may hand a roof to a trade
that never asked for one.

**The ninth K20 measurement is 61 of 108** carried-over invented persons renamed, against 67-of-106
at T-A13 and 7-of-102 at T-A11. Seven measurements span 7 % to 72 % with nothing fixed or broken
between them. K20 still owns the fix.

**Unverified here:** the desktop half of `smoke_renderer.mjs` does not fit this runner's ten-minute
per-command ceiling and was not run; the mobile half was, and `tools/check.sh` — which is the dev
gate — passed. See the run-budget box in ROADMAP.

## New 2026-08-15 — the first block off the business front, and the rule that arranged the row stops meaning anything on it

**T-A13.** `blk_lake_market` — Lake, Franklin, Randolph, Market — now carries **seven anonymous
roofs**, five principal, a stable and a privy, on five of its six free lots, with lot 3 left open and
lots 0 and 1 held by the Sauganash Hotel with Philo Carpenter's log drug store, and by the packer's
dwelling. **Standing roofs 299 → 306; remaining 366 → 359, 21 of them on covered ground** (was 28).
Inferred households 94 → 96, inferred persons 106 → 108. Recorded in L104. **The recipe cleared every
placement gate on its first run and no tool changed** — the sixth block in a row. It is the **first
block of this parcel shape that is not on South Water Street**; every open entry left in the schedule
is on Randolph.

**The face rule was asserted five times and is measured here, because neither of this block's faces
is South Water.** Five parcels sent their better dwellings to "the business front" and named that
front by the street's documented use — which says nothing about a block bounded by Lake and Randolph.
Counting every documented or inferred structure whose footprint centroid stands within **25 m** of a
street's committed centreline: **Lake 12, Randolph 2, South Water 9.** Lake's twelve are the
Sauganash, the Green Tree, the Exchange Coffee House, the Tremont, the Mansion House, both churches,
Hogan's store, Goss & Cobb's saddlery, Pierce's blacksmith shop, Dole's south warehouse and
Carpenter's log shop; Randolph's two are the log jail and the Western Hotel. The rule now rests on a
measurement rather than a habit, **and it is still an invention**: no source says a better dwelling
stood on the better street.

**The end rule's order survives and its meaning does not, and that is the finding.** T-A11's
criterion — distance to the Dearborn Street drawbridge — runs **532.2 m** at lot 6 to **600.4 m** at
lot 0 on the Lake frontage and **576.3 m** at lot 7 to **640.0 m** at lot 1 behind, ordering the lots
exactly as it has on every block of the row. What changed is the size of the difference. On T-A12's
block the far end stood **2.93×** as far from the bridge as the near end; here, **1.13×**. The
absolute spread of the front face is **68.2 m** against T-A12's 70.2 m — the same block, moved half a
kilometre. **The criterion is now separating two lots a resident would have called the same distance
from the bridge.** It was followed anyway, because changing criteria on the block where the first
stops flattering the answer is how an invention starts to look like a finding — but the arrangement
on this block is closer to arbitrary than on any block of the row, and L104 says so.

**K30 gets its first control measurement, and it is a factor of twenty to forty.** K30 has five
documented buildings standing 4.5–8.2 m inside the platted South Water corridor and asks whether
that is one bad stretch of street or a uniform grid bias. The first two documented roofs measured
against a **different** corridor are on this block: the **Sauganash Hotel intrudes 0.19 m** into the
Lake corridor and **Philo Carpenter's log drug store 0.22 m** — inside the plat's own precision of
standing on the kerb line. Two cases are not a survey; they are the control K30 did not have, and
they point away from a uniform bias. Nothing was moved.

**Two documented roofs share lot 0 and the derived occupancy table names the smaller one.** The
Sauganash puts 94.33 m² of its 96.0 m² on the lot and the log shop 28.58 m² of its 29.7 m²; the
source says the shop stood against the Sauganash's public bar and the footprints touch at 0.00 m, so
the record agrees with itself. `plat_occupancy` names the first holder by id — the log shop — so
**the town's most-documented building is not the one that table credits with its own corner.** It
cost this parcel nothing and it will mislead anyone reading that table for what stands where.

**Unverified here:** the desktop half of `smoke_renderer.mjs` does not fit this runner's ten-minute
per-command ceiling and was not run; the mobile half was, and `tools/check.sh` — which is the dev
gate — passed. See the run-budget box in ROADMAP.

## New 2026-08-15 — the business front is built end to end, and the rule that filled it points the other way on its last block

**T-A12.** `blk_south_water_dearborn` — South Water, State, Lake, Dearborn — now carries **six
anonymous roofs**, five principal and one privy, on five of its six free lots, with lot 7 (the
Lake-and-State corner) left open and lots 1 and 6 held by the Mansion House and the Chappel infant
school. **Standing roofs 293 → 299; remaining 372 → 366, 28 of them on covered ground** (was 34).
Inferred households 92 → 94, inferred persons 104 → 106. Recorded in L103. **The recipe cleared
every placement gate on its first run and no tool changed** — the fifth block in a row. State Street
is the platted town's eastern limit, so **the South Water row is closed**: every block of the
business front is now built, and every open entry left in the schedule is one street back or
further.

**The rule that arranged all five blocks reverses direction on the last one, and that is the
finding.** Four parcels put their better roofs "nearer the town-centre end"; T-A11 stopped asserting
that as a compass direction and measured it — the distance to the **Dearborn Street drawbridge**,
the only crossing of the main stem in July 1835. On the four blocks before this one the bridge lay
east, so the compass and the criterion agreed and nothing separated them. This block's bridge end is
its **west** end: lot 0's frontage is **36.4 m** from it, lots 2 and 4 are **57.7 m** and **81.7 m**,
lot 6 is **106.6 m**, and the back street runs **126.4 m** at lot 1 to **161.1 m** at lot 7. The
parcel follows the committed criterion rather than the compass, which is the whole point of having
replaced one with the other — and the lot left open is again the farthest of the eight from the only
bridge in town.

**A third criterion was tried and is recorded as UNDECIDABLE, which is worth more than a third
number.** A single landmark is a thin basis, so the parcel asked where the *mass* of documented
building is. The footprint-weighted centroid of all **83 documented roofs (19,145 m²)** lands at
local **E 939, N 123**, east of this block, making lot 6 nearest at **189.9 m** against lot 0's
**250.8 m**. Excluding the Fort Dearborn reservation — 13 roofs, **10,460 m²** — moves it to
**E 737, N 88** and reverses the answer: **95.0 m** at lot 0 against **115.9 m** at lot 6. The
criterion therefore turns entirely on whether a military reservation counts as part of the town,
which is a judgment and not a measurement, and its whole spread across the north tier without the
fort is **20.9 m** against the bridge's **70.2 m**.

**K30 is now half-measured and all five of its cases are on one street.** Both of this block's
documented South Water buildings stand in the platted roadway — the **Chicago American office**
**6.91 m** in and **Frederick Thomas's shop 6.25 m**, **148.6 m²** of documented roof on ground the
plat calls street. With T-A9's three (4.5 m, 6.6 m, 8.2 m) that is five documented buildings, all on
South Water, all between 4.5 and 8.2 m in. That is the shape of a centreline or width error on one
stretch, not of a uniform bias across the grid — which is the distribution K30 was opened to find.
Nothing was moved: a position with a source outranks a corridor this project derived.

**Two further confirmations, both of things earlier parcels had to argue.** T-A7's lap case has a
**fifth** instance and it is the largest that costs a lot nothing — the American office laps lot 0 by
**10.74 m²** with **0.00 m²** inside the buildable inset. And T-A11's refusal of the lateral offset
is confirmed independently and more cleanly: from the committed placement, 1.5 m further west buys
**0.01 m** of clearance for 0.76 m of lot-line margin and 3.0 m buys **0.22 m** for 2.26 m, where
half a metre of extra setback buys **0.50 m** and costs neither. The parcel's closest approach is
**7.01 m** against a 3 m gate.

**The row closes with K28 open, and the count is four blocks of five.** The D4 and the D2 this block
was dealt each pass rule 6's three tests read literally and both are refused on the same
conservative reading. One block of the row dealt neither floor trade a second roof, one dealt it to
the carpenters alone, and three dealt it to both. **The seventh K20 measurement is 59 of 104**,
against 7-of-102, 72-of-100, 19-of-98 and 32-of-96 — five readings spanning 7 % to 72 % with nothing
fixed or broken between them.

## New 2026-08-15 — the fourth business-front block, and the first time the row's "better end" is a measurement

**T-A11.** `blk_south_water_clark` — South Water, Dearborn, Lake, Clark — now carries **five
anonymous roofs**, four principal and one privy, on four of its five free lots, with lot 1 (the
Lake-and-Clark corner) left open and lots 0, 6 and 7 held by Harmon & Loomis's store, John Bates
Jr.'s auction room and the first Tremont House. **Standing roofs 288 → 293; remaining 377 → 372,
34 of them on covered ground** (was 39). Inferred households 90 → 92, inferred persons 102 → 104.
Recorded in L102. **The recipe cleared every placement gate on its first run and no tool changed**
— the fourth block in a row.

**THE ROW HAS PUT ITS BETTER ROOFS "NEARER THE TOWN-CENTRE END" THREE TIMES AND NEVER SAID WHAT WAS
AT THAT END.** This block's east end is Dearborn Street, and the **Dearborn Street drawbridge** —
the only crossing of the main stem in July 1835, already a committed structure record, its south
abutment at the foot of Dearborn on South Water — measures the claim: **35.6 m** from lot 6's
frontage, 55.5 m from lot 4's, 78.1 m from lot 2's, **101.7 m** from lot 0's, and on the back
street 126.3 m at lot 7 out to **158.2 m at lot 1**, which is the lot left open. No source says a
better house stood nearer the bridge, so the arrangement is as invented as it was; what changed is
that it is invented against a re-derivable number instead of a compass direction.

**AND THE FACE HALF OF THE SAME RULE MEETS ITS FIRST COUNTER-EXAMPLE.** Three parcels have called
South Water the valuable frontage and Lake the back street. The largest documented footprint on
this block is on Lake: the first **Tremont House at 139.3 m²**, against 92.9 m² for the auction
room, 92.9 m² for Harmon & Loomis's store and 46.5 m² for Pruyne & Kimball's drug store. The rule
is kept — it is a typology for where anonymous dwellings of different tiers go — but it is now
recorded as *not* a claim about which street was worth more, before four blocks of repetition
turned it into one.

**T-A7's lap case has a fourth instance and it is the first that costs a lot nothing at all.** The
drug store laps lot 2 by **4.66 m²**, and **0.00 m² of it is inside the buildable inset**: the
whole lap lies in the 1.5 m margin strip. Two of the store's corners are 0.70 m and 0.65 m inside
the platted lot line and the other two are 5.4 m out in the road, a **5.55 m** intrusion into the
South Water corridor. With L100's 22.1 m² of buildable lap, Kinzie's 9.7 m² and
`recon_1835_west_018`'s 11.9 m², the case now spans its whole range.

**THE OFFSET THAT ANSWERED THE LAST BLOCK'S LAP DOES ALMOST NOTHING HERE, AND THE MEASUREMENT SAYS
WHY.** T-A10 moved a shanty west to clear Church's store. On lot 2 the same move buys **0.03 m at
1.5 m of offset and 0.33 m at 3.0 m** — the 3 m version costing 1.26 m of lot-line margin — where
half a metre of extra setback buys **0.50 m** by itself. Church's store stood deep inside its lot;
this one stands in the roadway, so only the setback changes the distance. The cottage is set back
7.5 m and clears it by **6.83 m** against a 3 m gate, the closest approach in the parcel. The
lateral offsets left in the recipe are jitter and are labelled jitter.

**FIVE SOUTH DIVISION HOUSEHOLDS LIVE IN A D5, THREE BLOCKS RUNNING HAVE BEEN DEALT ONE, AND NO
PARCEL HAD EVER RECORDED WHY NONE OF THEM TAKES IT.** Rule 6's family and division tests pass on
this block's D5 for the baker, the butcher, the blacksmith and both clerks. All five fail test one
— their committed arguments do not call their counts floors, and two of them cap themselves
outright ("only one, because a bakehouse serves a great many people and nothing attests a second").
A refusal nobody writes down is indistinguishable from a rule nobody applied, so it is written down
now.

**K28 GETS A THIRD PRECEDENT INSTEAD OF A SECOND.** The D4 on lot 2 passes all three tests for the
carpenters exactly as T-A9's and T-A10's did, and was refused again on the conservative reading.
Three for three is the ordinary shape of a South Division block, not a recurring edge — the
question should be settled rather than collect a fourth. The labourers were dealt no D2 here, the
first block since T-A8 where their second-roof question did not arise.

**THE SIXTH K20 MEASUREMENT IS THE SMALLEST EVER RECORDED: 7 of 102** carried-over invented persons
renamed, against 72-of-100 at T-A10, 19-of-98 at T-A9, 32-of-96 at T-A8 and 25-of-94 at T-A2h.
Nothing was fixed in between. It is the hash-position mechanism L101 identified, confirmed from the
other end of its range, and it is not evidence that the churn is under control. K20 still owns the
fix.

## New 2026-08-15 — the third business-front block, and the name churn is three times worse than reported

**T-A10.** `blk_south_water_lasalle` — South Water, Clark, Lake, LaSalle — now carries **seven
anonymous roofs**, five principal and two yard buildings, on five of its six free lots, with lot 1
(the Lake-and-LaSalle corner) left open, lot 6 held by the Chicago Democrat's office and lot 5 by
Thomas Church's store. **Standing roofs 281 → 288; remaining 384 → 377, 39 of them on covered
ground** (was 46). Inferred households 88 → 90, inferred persons 100 → 102. Recorded in L101. **The
recipe cleared every placement gate on its first run and no tool changed** — the third block in a
row.

**THE FIRST BLOCK OF THE ROW THAT ARRIVED WITH A DOCUMENTED ROOF ON BOTH FACES.** The frontage
argument T-A8 opened and T-A9 tested — best dwellings to South Water, meanest to Lake — has so far
been free to apply, because the back street was empty on both earlier blocks. Church's store stands
on this one's Lake frontage. The arrangement was applied anyway, so a log cabin and a plank shanty
now stand on a frontage that already carries a documented store. Same invention, less room; L101
says so rather than letting the pattern read as automatic.

**T-A7's `west_018` case has a third and much larger instance, measured here.** Church's store is
seated on lot 5 by test one — **59.3 m² of 92.9 m² there against 33.6 m² on lot 3** — but **22.1 m²
of the lot 3 lap is inside lot 3's buildable inset**, so a lot the schedule reads as free carries a
documented building across its frontage corner. Against 9.7 m² (Kinzie, none of it buildable) and
11.9 m² (`recon_1835_west_018`), this is the biggest yet, and unlike Kinzie's it is *inside* the
buildable part. It is 2.4 % of the lot's buildable area, so the lot still took a roof: the shanty is
offset west, away from the store, and clears it by **7.56 m** against a 3 m gate — the closest
approach anywhere in this parcel. No rule changed and nothing was moved; the number is recorded so
the next parcel to meet the case has three data points instead of two.

**K28 IS NO LONGER A ONE-OFF, WHICH IS THE ARGUMENT FOR SETTLING IT.** T-A9 found rule 6 silent on
how many roofs of one block a trade may take and reported it as a case no block had offered before.
This block offered the identical case: four of its five dwellings pass all three tests for one trade
or the other, the D3 *and* the D4 for carpenters, the D1 *and* the D2 for labourers. Two consecutive
blocks have now dealt both floor trades both of the families they are housed in, so this is what a
five-or-six-dwelling block in the South Division looks like rather than a coincidence. One adoption
per trade was taken again, on T-A9's reading and recorded as a choice.

**AND THE K28 ID IS USED TWICE IN THIS REPOSITORY.** ROADMAP `K28` is the rule-6 question above;
the published-mirror gate that landed as PR #147 also shipped under the name K28 and has no ROADMAP
entry of its own. Both are real work and neither is wrong — the collision is in the label. A
disambiguation line is added at the ROADMAP heading so every existing citation resolves; renumbering
landed work is not a block parcel's call. This is the same defect T-A9 found in L99's pointer, in the
opposite direction.

**THE FIFTH K20 MEASUREMENT IS THE ONE THAT BREAKS THE "A FIFTH OF THE LAYER" DESCRIPTION.**
Inserting two households renamed **72 of the 100 carried-over invented persons**, against 19-of-98
(T-A9), 32-of-96 (T-A8), 25-of-94 (T-A2h) and 17-of-33-touched (T-A5). No grade moved, every
`name_basis` kept its pool citation, and `check.sh` re-derives all 102 — this is churn, not a
provenance failure. The mechanism is not random: `tools/generate_inferred_names.py` deals names
round-robin through each community-and-sex pool in a stable hash order of person id, so one new
person landing early in a large bucket renames everything after it. The spread from 19 to 72 is
purely where the new ids hashed. K20's fix still belongs in its own parcel; this is the fifth block
to ride along on it, and the first where the side effect is larger than the parcel.

## Fixed 2026-08-15 — the general case behind R-BUG3c-b: nothing checked what actually ships

**K28.** #145 fixed the terrain quantiser and ended on one line: *do not measure the file you built,
measure the file you ship.* It also said plainly what it had not done — "Nothing else in this
project measures a published artefact against its own source, and nobody has looked for the next
instance of it." This is that gate.

**The invariant is total, which is what makes it cheap.** `tools/publish.sh` is almost entirely
`cp`: the mirror is meant to be the repository, rearranged. So **every published file must be
byte-identical to its source**, unless it is on a declared list — and each entry on that list has to
say what transforms the bytes and **name the gate that measures the SHIPPED form**. That second
column is the whole point: it is the question nobody asked about the terrain, now written down
beside every place it applies.

Current state: **521 files byte-identical, 296 transformed under 4 declared rules, 0 unmapped.**

**It found two unchecked files on its first run**, which is the argument for it.

- **`build.json` was two days stale.** It claimed version `8909332` built `2026-08-13T19:18:05Z`
  while the mirror beside it was from today at a different commit. Nothing in `publish.sh` ever
  rewrote it — it had been written once, by hand. `tools/test_dev_preview.mjs` and `docs/PIPELINE.md`
  both read it, so both were reading a stale claim about what shipped. `publish.sh` now regenerates
  it every run from the same two variables the visible build stamp uses, so the machine-readable
  twin and the human-readable one cannot disagree.
- **The mirror's `index.html`** is written once from a heredoc and traced to nothing. It is a
  redirect stub with no claim in it, so it needs no gate — but that is now recorded, so if it ever
  grows a claim the absence is visible.

**The gate was verified to fail.** A single trailing newline appended to the published
`data/datum.json` fails it with the divergence named and the source path quoted; restoring the file
passes. A check that has never failed is not a check — the same standard K27 was held to earlier
today.

**What this does NOT do, stated so it is not assumed.** It compares BYTES for copies. It does not
verify that a declared *transform* preserves what the transform is supposed to preserve — that is
per-transform work, and it is exactly what #145 had to do by hand for the terrain. The 293 GLB
derivatives are declared, not checked; **R-W6** already asks whether the same quantiser moves E and
N by up to 153 mm and whether the terrain should ship quantised at all, and nobody has looked.

## FIXED 2026-08-15 — the ground you see IS the ground the town is anchored to now, and neither surface had moved

**R-BUG3c-b**, the half (a) refused to guess at. The 9.6–13.1 cm disagreement (a) measured is real,
and **neither the drawn mesh nor the sampler was wrong**. The gap is introduced *between* them, by
the publish step, after the only gate that measures it.

`generators/terrain_gen.py` ray-casts its decimated ground against the heightfield and refuses to
export past **30 mm**. Its master honours that to **2.5 mm** — as exact as the field it is built
from. The file a browser loads is the derivative `gltf-transform optimize` writes afterwards in
`tools/bake.sh`, and that quantises POSITION to **14 bits under one uniform node scale**. The scale
is set by the widest axis; this mesh is **5,020 m wide** (a 2,020 m box plus 1.5 km of skirt each
side) and **8.6 m tall**, so the vertical rungs are **306 mm** apart. Measured on the shipped bytes:
**rms 85 mm, max 228 mm**.

**No setting fixes it, and that was measured rather than assumed.** 16 bits — the maximum the format
offers — still lands on a 76.6 mm lattice. Only turning compression off meets the tolerance, at
**6.45 MB against 688 KB**.

**The fix is not a fudge and deliberately not `LIFT_M`.** The renderer reads the ground's heights
back off the heightfield as it loads (`conformGroundToField()`), so the surface a visitor sees and
the surface everything is placed on are the same surface by construction. All **124,141** vertices
move, by up to **227.6 mm**; the residual is **0.24 µm**, which is float32 storage.

**Three gates missed this and all three missed it the same way: they compare the render to another
render.** A quantised ground looks perfectly correct. Two gates now hold a measurement instead —
`check.sh` asserts the committed master and reports the derivative, and the smoke asserts the
surface actually DRAWN against the sampler, green at both viewports.

**Unflattering, and worth keeping in view.** This is the third parcel on one owner report. R-BUG3
fixed a real contrast fault and declared the bug closed; the owner reproduced it the same day.
R-BUG3c-a measured the cause and fixed nothing, which is the only reason this fix is the right one
rather than a nudge to `LIFT_M` that would have left buildings, collision and flora still wrong. The
lesson is one line: **do not measure the file you built, measure the file you ship.** Nothing else
in this project measures a published artefact against its own source, and nobody has looked for the
next instance of it.

**Still open, and honestly open:** the same quantiser moves E and N by up to **153 mm** and nothing
corrects that. It is invisible on a decimated prairie as far as anyone has checked — and nobody has
actually checked. That is **R-W6**, along with whether the terrain should ship quantised at all.
## MEASURED 2026-08-15 — the drawn terrain and the heightfield are DIFFERENT DATA, not a decimation

**R-BUG3c-b.** R-BUG3c-a found the drawn ground sitting 9.6–13.1 cm above `terrain.surfaceHeight()`
at the owner's pose. This asks which of the two moved, by testing the drawn mesh's **own vertices**
against the sampler — 5,962 vertices across 30 terrain meshes, water excluded.

Three outcomes were possible and they are mutually exclusive. Near-zero everywhere would mean the
mesh IS the heightfield, decimated, and the burial is an interpolation artefact of coarse triangles.
A constant offset would mean a datum shift. Random would mean different data.

| | |
|---|---|
| min / max | **−3.077 m / +2.744 m** |
| 5th / 95th percentile | −2.465 / +1.519 |
| median | +0.026 |
| mean ± sd | +0.087 ± **1.036** |
| vertices within 5 mm | **182 of 5,962 (3.1 %)** |

**It is the third outcome.** The spread is METRES, not centimetres, so this is not coarse-triangle
interpolation; and the standard deviation is 1.04 m against a mean of 0.09 m, so it is not a datum
shift either. **The baked terrain GLB and `heightfield.bin` are different surfaces**, roughly
co-located — the median is 26 mm — and locally disagreeing by up to three metres.

**The 13 cm at the owner's pose was the local value of a much larger disagreement.** Everything
anchored to the sampler — roads, flora, buildings, collision — is placed against a surface that
differs from the drawn one by up to 3 m somewhere in the scene.

**Still not established, and this is now the whole question: which one is authoritative.** One of
these was generated from a terrain spec the other no longer matches, or one is stale. Until that is
settled nothing should be moved: raising `LIFT_M`, re-baking, or regenerating the heightfield could
each be the change that destroys the correct surface. The next step is to re-derive both from the
committed terrain spec and see which reproduces.

## New 2026-08-15 — the second business-front block, and the second roof each trade was refused

**T-A9.** `blk_south_water_wells` — South Water, LaSalle, Lake, Wells — now carries **eight
anonymous roofs**, six principal and two yard buildings, on six of its seven free lots, with lot 1
(the Lake-and-Wells corner) left open and lot 6 held by Rufus Brown's boarding house. **Standing
roofs 273 → 281; remaining 392 → 384, 46 of them on covered ground** (was 54). Inferred households
86 → 88, inferred persons 98 → 100. Recorded in L100. **The recipe cleared every placement gate on
its first run and no tool changed** — the second block in a row to do so, which is what T-A8 said a
block parcel should now look like.

**THE FINDING IS THAT RULE 6 DOES NOT SAY WHAT IT WAS ASSUMED TO SAY, AND IT IS OPENED AS K28.**
Read literally, **four** of this block's six dwellings pass all three adoption tests for one trade
or the other — the D3 *and the D4* for carpenters (one carpenter household stands in a D4, in the
North Division), the D1 *and the D2* for labourers (four stand in D2s). The rule is silent on how
many roofs of one block a single trade may take, because no block before this one dealt a trade two
of its families. One adoption per trade was taken and the other two refused, on the reading that
rule 6's own opening sentence — the mix is a claim about the town, not about what has been drawn —
forbids one block's deal from raising a trade's count twice. **That is a choice and is recorded as
one**, in both census arguments and in L100, so the next parcel meets an argument it can disagree
with rather than a precedent it has to guess at. K28 is raised to make it code.

**Three documented stores on this block stand INSIDE the platted South Water corridor** — Jones's
grocery by **4.5 m**, Philo Carpenter's store by **6.6 m**, Peck's store by **8.2 m**; two of the
three lap no lot of the block at all. T-A7 established that pre-plat records can stand "a metre or
two proud" of their frontage and measured what that does to occupancy; the intrusion itself had
never been measured. It cost this parcel nothing — the nearest invented roof to any of the three is
**7.99 m** against a 3 m gate — so it is opened as **K30** rather than touched inside a block
parcel. Three named buildings are drawn standing in a street, and either the street, the positions
or 1835 South Water Street is what is wrong.

**L99's commercial-frontage parcel did not exist.** That entry says the question was opened as a
ROADMAP parcel; the ID it names was already carrying the confidence-band parcel, so there has been
a liberty with no work item behind it. It is opened properly as **K29**, and this block is its
second instance: the programme dealt a log cabin and a plank shanty to the town's busiest
commercial frontage for the second time running, and three South Water blocks are still open.

**A fourth measurement of K20:** inserting two households renamed **19 of the 98 carried-over
invented persons**, against 32-of-96 at T-A8, 25-of-94 at T-A2h and 17-of-33-touched at T-A5. No
grade moved and every `name_basis` kept its pool citation, so this is churn rather than a
provenance failure — for the fourth block in a row.

## Fixed 2026-08-15 — the changelog's merge driver was corrupting the file, silently, every time

**K27.** `.gitattributes` merged `js/changelog.js` with `merge=union` so that two branches each
shipping an entry would not conflict. The stated hazard was "two branches editing the same existing
entry", called rare; the everyday prepend was called safe. **That is backwards.**

Union is a LINE union and a changelog entry is not a line. When both sides prepend, the shared
closing `    ] },` is common context and survives **once** — so the first entry swallows the second
and the literal is left with an unclosed bracket. The result is still valid JavaScript, so
`node --check` passes it and nothing downstream notices.

**Measured: five consecutive merges in one day** (#126, #132, #136, #139 and R-BUG4) each produced
exactly this corruption and each needed the same manual repair — rebuild from the base copy and
re-stamp. Union did not prevent a single conflict. It converted five loud conflicts into five silent
corruptions that had to be repaired by hand regardless.

The changelog merges normally now. Two branches that both ship an entry conflict, loudly, at the
merge, and the resolution is the obvious one: keep both, newest first, re-run
`tools/stamp-changelog.mjs`.

**And a claim in that comment needed correcting, though not the way I first wrote it.** The comment
said "the contract check catches that — versions must be strictly decreasing". I recorded that as
never written. **That was wrong: the rule exists in `check-changelog.mjs` and always has.** What it
cannot do is report — it sits after the module load, and the shape walk above it exits the moment a
bracket is unbalanced. The merge that duplicates a version is the same merge that breaks the shape,
so every run died on the shape first and the duplicate was never named; the hand repair then rebuilt
the file from a base copy and took the duplicate with it. A correct check, unreachable in precisely
the case it was written for.

The version rule is now enforced in the **text scan** as well, which runs before that exit, so a
duplicate is named even when the literal will not load — and gaps in the numbering are reported too,
because a gap means an entry was dropped in a merge. Verified to fail on an injected duplicate
before being committed.

**The same `merge=union` line and the same exposure exist in the other fleet apps** (polecat-platform
docs/SHELL-API.md § the fleet changelog contract). This repo is fixed; the fleet is not.

## MEASURED 2026-08-15 — the ground you see is not the ground the town is anchored to

**R-BUG3c-a.** The owner reproduced the invisible near-field road with the R-BUG3 fix in. The cause
is now measured, and it is not the streets at all.

At the reported pose, the DRAWN ground sits **9.6 to 13.1 cm above `terrain.surfaceHeight()`**, the
sampler that roads, plants, buildings and collision are all placed with — over the whole hundred
metres, not just near the camera. `LIFT_M`, the road's lift above that sampler, is **22 mm**. The
roadway is under the visible ground along its entire length here, and so is anything else rooted by
the same sampler, which is why the grass tufts disappear with it.

**Why the road still shows beyond about seven metres:** the polygon offset wins at range and loses
up close, because depth-buffer resolution is finest near the camera. The crossover is a function of
distance alone — which is why the boundary is a clean horizontal line at a constant radius, the one
feature of the owner's screenshots that no other explanation accounted for.

**A visitor stands 13 cm sunk into the terrain they can see.** Eye at 2.455 over a sampler reading
0.775 is the recorded 1.68 m of eye height; the drawn ground under that same point is 0.906.

**What is NOT established: which of the two is wrong.** The drawn surface is a baked GLB, the
sampler reads `heightfield.bin`, both descend from the same terrain spec, and this measurement says
only that they disagree. Raising `LIFT_M` would hide a datum disagreement behind a fudge and leave
buildings and collision wrong. Landed as a measurement, red, with no fix — which is what the parcel
asked for and what saved R-BUG2 from a fix that would have made things worse.

## New 2026-08-15 — five invented houses on the town's business front, and the share-out that put them there

**T-A8**, and it is the first block parcel since T-A5 that actually built a block: T-A6 and T-A7
each set out to fill one in and finished up repairing the arithmetic that decides what a block may
be dealt. `blk_south_water_franklin` — South Water, Wells, Lake, Franklin — now carries **seven
anonymous roofs**, five principal and two yard buildings, on five of its six free lots, with lot 1
(the Lake-and-Franklin corner) left open. **Standing roofs 266 → 273; remaining 399 → 392, 54 of
them on covered ground** (was 61). Inferred households 84 → 86, inferred persons 96 → 98; totals
158 households and 194 people. Recorded in L99.

**The recipe cleared every placement gate on its first run and no tool changed**, which is the
shape T-A2 predicted these would settle into and which T-A6 and T-A7 both interrupted.

**THE FINDING IS ABOUT THE SHARE-OUT, NOT ABOUT THIS BLOCK, AND IT IS OPENED AS K25.** This is the
first block this lane has filled on South Water Street — the town's business front, where every
documented roof on or beside the block is commercial: the Temple Building, the Exchange Coffee
House, J. H. Kinzie's forwarding store, Newberry & Dole's warehouse west and H. Jones's store east.
The 665-roof programme dealt it **five ordinary dwellings, one of them a D2 plank shanty**, because
`tools/reconcile_665.py` apportions families by DISTRICT and has no notion of what a street was
for. The block was built as dealt — the apportionment is the programme's claim and overriding it by
hand on the day it produces an awkward result is how a reconstruction becomes a picture somebody
liked — but the defect is now written down in three places rather than absorbed silently, and it
will recur on `blk_south_water_wells`, `blk_south_water_lasalle`, `blk_south_water_clark`,
`blk_south_water_dearborn` and `blk_lake_market`: **six of the ten open blocks front a commercial
street.**

**T-A7's second test is vindicated by measurement, which is what this block was in a position to
do.** T-A7 left lot 2 schedulable because Kinzie's store laps it only inside the 1.5 m margin
strip. If that had been too generous, this parcel is where it would have failed. It did not: the
lot 2 roof stands **7.3 m** from Kinzie's store against a 3.0 m separation gate, and every other
roof this parcel places is further from its own nearest neighbour than that.

**Both adoptable trades passed rule 6 on one block, for the first time since the rule took its
third test.** Exactly two trades' committed arguments call their own counts a floor — carpenter and
labourer — and this block was dealt a D3 and a D1 in the South Division, which is precisely the
family each is already housed in there. Both were adopted (13th carpenter, 15th labourer). Adopting
only one, as every parcel before this did, would have been a preference rather than the rule
choosing.

**K20 measured a third time, and it is the worst reading yet.** Inserting two households renamed
**28 of the 84 carried-over inferred households and 32 of the 96 carried-over invented persons** —
a third of the layer — against 25-of-94 at T-A2h and 17-of-33-touched at T-A5. No grade moved, no
`name_basis` lost its pool citation, and `check.sh` re-derives all 98, so this is churn rather than
a provenance failure. K20's own text says the fix belongs in its own parcel; it has now ridden
along with a block three times, and it is the reason this PR's diff is 47 files wide for a change
whose real content is seven buildings.

**AND IT DOES NOT SHIP. THE DESKTOP DRAW-CALL BUDGET IS EXCEEDED AND THIS PARCEL IS WHAT EXCEEDED
IT.** `tools/check.sh` is green. The mobile viewport is green — 419 assertions, zero page errors.
The desktop viewport fails four assertions for one reason. Measured on the published mirror at
1280×800, both runs full and in the foreground:

| | draw calls | budget | verdict |
|---|---|---|---|
| `dev@52641c4` (baseline) | **75** | 80 | pass |
| this branch, +7 roofs | **84** | 80 | **fail**, and the three per-tier detail ceilings with it |

**Seven roofs cost nine draw calls.** R-G1 projected +11 per 19 records; the observed rate here is
steeper, and it was spent against five calls of headroom. This is **R-W5a**, arriving earlier than
its own straight line predicted, and the operational consequence is blunt: **lane 2 cannot land
another block until R-W5a lands.** Nine open blocks remain and not one of them is smaller than the
one that broke it.

**Three things were NOT done to make it green**, listed because each is a tempting shortcut. The
budget was not raised — an assertion moved to admit what it was measuring is not a gate. Roofs were
not dropped — the schedule deals seven, and building five to satisfy a frame rate is fitting the
town to the renderer. R-W5a was not fixed in this run — it is a lane 1 parcel with a lane 1 PR
already in flight, and batching the scene is a unit of its own.

**One renderer-adjacent fix IS in this branch, because the parcel could not be diagnosed without
it.** `tools/smoke_renderer.mjs` filtered terrain problems with `/terrain|water/i` against the
whole message, so `blk_south_water_franklin` — the first block whose id contains the word — turned
two ordinary placeholder-asset notes into a reported terrain load failure. Anchored to
`/^\s*(terrain|water)\b/i`, which is what the code's own comment always claimed, and verified
against real `terrain <epoch>: …` and `water: …` messages in both directions. Five of the ten open
blocks are `blk_south_water_*`.

**What this parcel did NOT do.** It did not re-apportion the schedule (K25), it did not fix the
name allocator (K20), it did not fix the draw-call budget (R-W5a), and it did not answer whether
one open lot per block is the right vacancy — the question T-A6 left standing and nothing here
touches.
## Fixed 2026-08-15 — a wet corner was deleting whole panels of road, dry half included

**R-BUG4**, owner-reported from South Water Street as a clean-edged green quadrilateral punched
through the roadway. `streets.js` dropped a panel outright when the centreline **or any of its four
corners** fell on water. The comment said the edge test kept a bank road from painting over water
where its legal corridor reached it — the right aim and the wrong instrument, because deleting the
panel takes the dry half with it.

It clips at the waterline now, each end trimmed on each side independently by bisection out from
the dry centreline. Asymmetric on purpose: a bank road is wet on one side only, and shrinking it
symmetrically would throw the dry verge away as well. The centreline test is unchanged — a road
whose centre is in the river is a crossing, and a crossing is a bridge's job.

**Measured on the built geometry:** 4,843 panels have a dry centreline, **all 4,843 now reach the
ribbon**, 28 clipped at the waterline, 0 dropped as sub-metre slivers, **62.7 m of roadway
recovered**. The `13 quads / ~30 m` first recorded for this bug was read off a truncated probe
listing and was **half the true figure**; a sorted table read from its tail is not a total, and the
number in the roadmap and changelog is now the measured one.

The gate asserts the invariant rather than the number — every panel with a dry centreline reaches
the ribbon, the only permitted absences being sub-metre slivers, which are counted and printed —
and it asserts that clipping actually happens, so a later simplification back to deleting the panel
fails in CI rather than in a screenshot.

## REOPENED 2026-08-15 — the owner reproduced the invisible road WITH the fix in, and it is not the streets

Reported again the same evening, mobile, Lake Street approaching Franklin — after the entry below
declared it solved. Reproduced at that exact pose. **Forced fully opaque, depth-writing, at the
marker pass's own polygon offset, the ribbon still reaches only row 937 of 1560: the bottom 40 %
of the frame holds no roadway at any opacity.** And it is not a streets fault — per-row detail
energy falls from 1.0-2.4 above row 1000 to 0.2 below row 1120, so the road, the grass tufts and
the ground texture all vanish together at one radius. The geometry is present (32 street vertices
within 10 m); something is burying it. Recorded as **R-BUG3c**, top of the rendering queue, with
the untested hypothesis named and the instruction to measure the drawn terrain against
`terrain.surfaceHeight()` before changing anything.

**The gate went green because its new station stands AT a crossing** — one of the few places the
near ground is intact — and the owner was 172 ft short of one. Third time on this bug that the
answer was where the gate was pointed, and the parcel that wrote that lesson down repeated it.

A second, separate fault came out of the same reports (**R-BUG4**): `addRecord` drops a whole road
quad when ANY of its four corners is water, dry half included. **13 quads / ~30 m of roadway
deleted while the centreline is dry land**; Kinzie loses 14.2 % of itself. Clip at the waterline,
do not discard.

## New 2026-08-15 — the horizon-timber figure was scoring the town's roofs, and the fix for it is subtraction rather than a colour test

**R-W4a.** RENDERING § 5 asks for **≥ 90 %** horizon-timber column coverage. The number answering
that question counted **any** break in the skyline above the land/sky line, and a gable end breaks
a skyline as surely as an oak — R-G1 caught `prairie_south` moving 0.364 → 0.436 on nineteen new
roofs with no renderer change. **Corrected, `prairie_south` reads 0.295 desktop where it read
0.632, and 62 % of what was counted as timber there was the town** (409 of 1053 measured columns
broke on a roof and on nothing else). Across the 22 station-viewports the mean falls **0.672 →
0.582**, and the number meeting the target falls **1 → 0**. Full table in `docs/ROADMAP.md`
§ R-W4a.

**The discriminator this project had written down does not work, and that was measured rather
than argued.** R-G1 proposed the crown-hue channel — "a whitewashed gable is not green". At the
first hit pixel of every broken column, desktop: grey gables at `prairie_south` sit at ΔG−B
**+22.4**, hazed timber at `prairie_west` ranges **+0.1 to +17.5**. The two populations overlap
completely, because the horizon sky is strongly blue-dominant and every non-sky pixel clears a +3
G−B test — the channel was a not-sky detector, so the old figure was testing the same condition
twice. **No colour test can separate them in principle here**: L17 makes extinction total by
1500 m, so distant timber and a distant wall both converge on the fog colour.

**What replaced it takes the town away instead of guessing.** The harness photographs each
station twice from the identical pose — once as the visitor sees it, once with the `structures`
group hidden — and measures the horizon in the second frame. Timber by construction: no
threshold, no hue, nothing to tune, and **the figure cannot move when a block lands**. The old
number is kept at its old value under a name that says what it counts (skyline breaks), so
2026-08-14's baseline is still comparable and no past figure was silently redefined.

**Two properties of the new figure that must be quoted with it.** It rises at six of the
22 station-viewports, because a building can stand in front of timber and hide it — it answers
*is the horizon timbered*, not *can the visitor see timber past the town*, which is the right
question for a target derived from photographs of a treeline. And `from_above` is an aerial pose
whose band is not a horizon at all (0.212 / 0.156, town share 0 %): do not average it in without
saying so.

**Unverified / not claimed:** nothing about the renderer changed, so no scene claim moves with
this. The cost of the second capture is measured (13 min 12 s for the full both-viewport run,
against ~12 min without it) and `--no-mask` opts out. Putting the town back was checked rather
than assumed: 5, 9 and 51 differing pixels of 1,024,000 across the change, inside the harness's
own cross-process residual, with the `--stability` contract passing byte-identical.

## Partly fixed 2026-08-15 — the road at a crossing, the two stations that never stood on one, and a gate that abstained exactly when it should have shouted

## New 2026-08-15 — the road gate can now see contrast as well as lightness, and the photograph it was told to calibrate against has no road in it

**R-M1a.** The owner ruled on 2026-08-14 that the road gate should score exposure-invariant
**contrast** and keep an absolute **floor** — both bars, not a replacement — after R-W1
legitimately changed the scene's exposure, preserved the road/ground ratio to within 0.4 %, and
lost a gate it had not regressed. Both numbers are now measured at every road band, at both
viewports. **Neither is gated**, and that split is deliberate: the parcel's own acceptance names
three builds to smoke and the lane allows a parcel two, so it was split into *land the
measurement* and *set the bars* before it was claimed. A gate that moves at the same moment as
its own baseline has no baseline.

**The measurement is verified against a number this project committed before the code to compute
it existed.** R-W1's parked working recorded Weber **0.1217** at `from_above`, desktop,
100–250 m, taken by hand at the point of use on `dev@d762a19`. `weberContrast()` reads **0.1217
at n 11** against R-W1's n=11, eleven commits later. The 250–600 m band moved 0.0940 → 0.0999
(+6.3 %) with ΔL\* 2.36 → 2.4 in step, which is R-BUG3's alpha-and-opaque work reaching a band
R-BUG3 predicted it would leave untouched — small, real, and R-M1b's to explain.

**The finding that matters more than the baseline: Weber has no ceiling as its background goes
dark, and one band already demonstrates it.** `lake_market`, desktop, 100–250 m reads
**`weber 8.8023` over a ground of `L* 3.0`**, where the same band on mobile reads 0.1339 over
L\* 53.5. Nothing is wrong with the road there — ΔL\* is 18.0 at 100 % perceptible. The road's
projected probes on that viewport simply land against something almost black, and a ratio whose
denominator is the light in the background is unbounded when the background has none. **A median
Weber over a band can therefore be set by its darkest probes rather than by its roads.** That is
the precise failure the owner's ruling anticipated by pairing the ratio with a floor instead of
swapping one bar for the other, and it is the number the bars would have been fitted against had
they been set in the same change as the baseline.

**And R-M1's threshold source does not exist.** The parcel says to derive the bars by measuring
"what contrast a real dirt track holds against real prairie" in the R-REF1 photograph.
**There is no dirt track in that photograph.** `tools/measure_reference.py` now surveys the land
region and prints it: the widest contiguous bare-earth run anywhere below the horizon is
**332 px = 8.2 % of the frame width, at −38.2°** — the bottom edge of the frame, at the
photographer's own feet, and it is dry stems and litter between plants rather than a surface. The
widest run with no green excess at all is 11.1 % at −0.4°, which is the hazed treeline and is not
ground. The soil-like *fraction* is 3 % over the whole land region and rises to 18.5 % in the
bottom 5°, which is exactly why a fraction cannot decide this and a run length can: a track
crossing that frame would be contiguous across a large part of its width at some elevation, and
nothing in it is.

This is the second time this project has been handed a target that its own reference cannot
supply. The first is recorded above under the 2026-08-10 prairie sweep — a horizon-timber brief
specifying "Weber 0.036–0.067", of which STATUS says it *"does not exist in the reference at any
threshold — that error was the brief's, not the builder's."* Nothing R-REF1 actually landed is
weakened by this: all four sky readings, the horizon band and the canopy contrast still
reproduce, and they are what `world.js` and `trees.js` quote. **R-M1b is therefore blocked on a
threshold source, not on effort**, and the three honest options — a second cited photograph that
does show a track, a cited published detection threshold labelled as a claim about eyes rather
than roads, or R-M1a's own baseline frozen and labelled provisional — are written out in
`docs/ROADMAP.md` § R-M1b for the owner to choose between. Do not pick a number and call it
derived.

## Fixed 2026-08-15 — the town was paying a draw call per colour of paint, and the next 399 roofs now cost none

**R-W5a.** The draw-call budget was the one thing both overnight lanes were waiting on: R-G1
measured **+11 draw calls for 19 new roofs**, straight-lining to about **+240 against a budget of
80** over the 399 roofs still to come, and it had already parked a block of houses (T-A8, PR #132).
It is not a growth problem any more. It is **zero**.

**The cause, and it was hiding in plain sight.** `buildings.js` sorts the town into one
`BatchedMesh` per distinct material, and the key included the base colour. Every one of the 47
batches was the same `MeshStandardMaterial` in every respect a renderer distinguishes — metalness
0, **no map of any kind**, `DoubleSide`, opaque, `alphaTest` 0, smooth-shaded. The only fields that
differed were `color`, with **39 distinct values across 47 batches**, and `roughness`, with 16. The
town was spending forty-seven draw calls to render two numbers, and buying another one every time a
block landed carrying a paint nothing else in town used. **R-G1's "+11" was 11 new material
GROUPS, not 11 objects** — which is precisely why it was uniform at bearings 150° apart: the cost
counts paints in frame, not buildings.

**The fix carries colour per vertex and is arithmetically identical, which is the only reason it is
allowed here.** `material.color` is already in the renderer's linear working space; three's
`<color_fragment>` multiplies `diffuseColor.rgb` by the `color` attribute with no colour-space
conversion of its own; and the confidence view's tint was already applied *after* that chunk. So
the shader does the same product in a different order, and a documented white wall still renders at
the value its record claims, to the bit. Roughness is additionally compared at three decimals,
which merges the bespoke masters' float32 `0.8999999761581421` with the generated infill's `0.9`.

**`tools/critic_shots.mjs`, source tree, both viewports, before and after on the same `dev`:**

| draw calls | `sauganash` | `s'nash_wing` | `lake_market` | `f_post_office` | `forks` | `green_tree` | `south_water` | `from_above` | `prairie_south` | `prairie_west` | `river_bank` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop before | 75 | 78 | 90 | 66 | 98 | 103 | 96 | 72 | 95 | **109** | 56 |
| desktop after | 56 | 58 | 60 | 57 | 68 | 70 | 66 | 59 | 62 | **75** | 52 |
| mobile before | 72 | 74 | 78 | 60 | 82 | 99 | 94 | 72 | 93 | **106** | 49 |
| mobile after | 54 | 55 | 58 | 51 | 64 | 68 | 64 | 59 | 61 | **73** | 47 |

**Batches 47 → 16; station-viewports over the ≤ 80 budget 11 of 22 → 0 of 22.** A new roof of any
colour now joins an existing batch, so T-A8 and the 399 roofs behind it cost nothing.

**What it cost, stated in numbers rather than reassurance.** Triangles are **identical to the
triangle at all 22 station-viewports** — nothing was dropped to buy the calls. The frames are *not*
byte-identical: 2 of 22 hash the same, and the rest differ on **0.013 % of pixels**, in 7–195
scattered components whose largest is 56 px, all on building silhouettes — depth ties at coincident
surfaces resolving the other way under a changed draw order. Worst single pixel 93/255;
**whole-frame mean |Δ| 0.003–0.005 of one 8-bit count**. No surface anywhere is repainted.

**What it does not do.** It does not touch the water surface, post-processing or dynamic resolution
(R-W5b, still open, still carrying R-BUG1's river flicker), and it leaves 16 batches where 1 is
reachable — the roughness half needs a shader patch and is written up as **R-W5a2** with its
numbers already measured. The budget is met with 5 calls of headroom at the worst station and the
growth term is zero, so that half buys margin, not a fix.

## Fixed 2026-08-15 — the road at your feet, the two stations that never stood on one, and a gate that abstained exactly when it should have shouted

**R-BUG3, owner-reported on mobile, on the dev preview with R-BUG2's fix already in:** standing on
Franklin Street approaching Randolph, the wheel ruts read in the mid-distance and *"it should not
be invisible when I am standing on it."* True. The near band now scores **3.1 L\* with 80 % of
probes perceptible** on mobile and 3.2 / 60 % on desktop, against **1.5 / 30 %** before, measured
on the published mirror. Every band past 40 m is untouched by the near-field fix.

**The parcel's first move measured nothing, and that is the finding.** It said: add a `[2, 40]`
band, expect it to fail, and that failure is the acceptance. Added, and the band collected **one
probe** at `south_water` and **none** at `from_above` — because **neither gated station stands on
a road**. `south_water` is **101 m from the centreline it is named after** (that is T-V2, now
measured rather than suspected) and 17 m from the nearest one; `from_above` is 175 m up. The window
was wrong in two dimensions, distance and pose, and the failing gate could only show one of them.
There is now a third station: `lake_market`, reached the way a visitor reaches it — by clicking a
verified street-control intersection in the Go to tab — which then turns to look along the
centreline underfoot, a bearing read off the committed path. The arrival pose alone was not enough
either: the shipped jump faces a fixed bearing, which at a crossing points diagonally into the
block and put **zero** road probes inside 100 m.

**The prime suspect is refuted, and no grass was cleared.** The parcel named near-field sward
occlusion as most likely, with an explicit non-licence against widening a clearing corridor to win
a score. The harness now re-shoots its road markers with the sward and the trees hidden, so an
occluded probe is distinguishable from an absent one — and in the near band **all ten probes are
marked either way**. Nothing is hiding the road. `flora.js` is untouched, no recorded ground cover
moved, and the non-licence never had to be tested. Every band now reports the discrimination
(`seen N of M projected, K clear of flora`), because telling occlusion from flatness is the
distinction three gates in a row failed to draw.

**The fault, stated more precisely than "the alpha is too low".** An alpha here is a **coverage
fraction** — what share of the ground is bare earth rather than grass — and that is the right
picture of a mixture only where one pixel spans many patches of it. At a walker's feet one pixel
spans one patch, which in life is either earth or grass, and the blend paints a uniform wash of
grass-with-a-hint-of-dirt instead. The harness measures both ends of it: the same near probes with
the ribbon forced **fully opaque** score **3.4 L\***, so the contrast was sitting in the ribbon's
own colour and the shipped alpha was spending under half of it. The near field also has less to spend — the
ground underfoot is genuinely darker than at range, **L\* 51.0 against 52.7–56.3**. The fix scales
alpha by 2.4 inside 15 m, fading to nothing by 40 m. Recorded as **L98**.

**The durable half is the gating rule.** A band gated on *how many probes were SEEN* gates itself
out at precisely the moment the thing it measures goes wrong: a road nobody can see reports n=0,
which is indistinguishable from a stretch with no road in it, and the check passes by abstention.
Bands are now gated on how many probes were **PROJECTED** — on screen, and therefore owed a
picture. This is the third time this one bug has been a question of what the gate was pointed at,
and the first fix that makes the gate fail loudly rather than quietly decline to answer.

**A second fault, found by the new station and fixed with it.** At desktop, 100–250 m from the
crossing, the ribbon scored **0.0 L\*** while the marker pass was frontmost — R-BUG2's fault 1
again, its polygon offset having been tuned until the bands *at the two stations then gated*
passed. Deepened to the marker pass's own values, that band reads **18.0 L\* at 100 %
perceptible**. And the opaque diagnostic had to be fixed before it could be believed: its first
form let the terrain paint back over the ribbon and reported a 0.0 ceiling under a healthy road.
It writes depth now, as the marker pass always did. A diagnostic that lies quietly is worse than
no diagnostic, and this one lied in the direction of *nothing to see here* — the same direction as
every other instrument in this bug's history.

**What is not fixed.** The near band has the least headroom of any band a walker actually stands
in: its ceiling fully opaque is **3.4 L\* on mobile and 4.3 on desktop**, against 5.9–6.9 at the
same station's 40–100 m and at both aerial bands — and **20 % of near probes on mobile, 40 % on
desktop, cannot clear the perceptibility threshold even at full opacity**. (Not "the lowest of any
band", which an earlier draft of this said: at that station the 600–4000 m band is lower still, and
that is a road at a kilometre rather than one underfoot.) Opacity has nearly run out as an
instrument here. L98 names the honest
successor: a textured coverage, earth and grass resolved as patches at the scale a near pixel can
show, so the eye integrates the recorded fraction rather than the blender pre-mixing it. That
belongs to **R-W2**, where the 1.4 texture score already lives.
## New 2026-08-15 — a refusal nobody could tell apart from an unanswered question

**K21.** Rule 6 of the household programme lets a block roof be adopted by an argued household
only if three tests pass, and the second asks whether the roof's family is one this layer already
houses that trade in. **For four trades that question had no answer at all.** `brickmaker`,
`packer`, `sawyer` and `wheelwright` live exclusively on the 31 roofs this layer *raises* rather
than adopts, and those records named no family in any field a gate could read — eight further
trades were partly in the same position, 17 households in total. T-A5 refused the sawyer adoption
on that silence and said at the time that it could not tell the refusal from an unanswered
question.

**The answer was a transcription, not a decision.** Every one of the 31 buildings was dealt a
crosswalk family by the programme, and every one has always *said* so in prose — the footprint note
reads "a 16 x 22 ft rectangle from the **D3** family band", and each form value cites the same
band. The band was committed in two places and readable in neither. Writing it into
`reconstruction.family` therefore **invents nothing and owes `docs/LIBERTIES.md` nothing**; rule 6
gains no fourth clause, and no trade is granted a pass — a trade whose families are readable can
still fail the test.

| | before | after |
|---|---:|---:|
| census trades resolving rule 6's family test | 25 of 29, four of them not at all | **29 of 29** |
| trade-family pairs the test can compare against | — | **44** |
| households standing on a roof that names no family | 17 | **0** |

**The durable half is the gate.** `tools/generate_inferred_households.py` fails if any roof a
household *lives or works in* names no family in the crosswalk — over both links, because a shop's
family is as much a claim about the town as a cottage's. The test cannot go silent again without a
gate saying so.

**The parcel's own suspicion was refuted.** It flagged `inf_sawyer_dwelling_b` massing as an
`outbuilding` while `_a` masses as a `frame_dwelling`. They differ because **they were dealt
different families**, D3 and D2, and each resolves through its own family's committed archetype —
the record's existence note says so in as many words. The real split is five W4 shops massed two
ways, all of them one-storey, which W4's own licence does not explain.

**And underneath that, the finding worth more than the parcel.** Reading each committed form value
against its family's band shows **54 of 193 reconstructed roofs sit outside the band their own note
cites** — 39 of 162 anonymous, 15 of 31 bespoke, worst `inf_laundry_north` at 280 sq ft against an
A5 band of 48–192. The cause is that the form generators choose values by **archetype** and attach
a note citing the **family**. A note that cites a band is the defence for the invention; where the
value is outside it the note is wrong about its own source. That is **K25**, split so the
measurement lands before anything moves.

**Two gates caught what reading would not have.** `reconcile_665.py` classified roofs by whether a
reconstruction block was *present*, so all 31 silently moved from `inferred_household_programme` to
`generated` — totals unchanged, attribution wrong. And `compile_scene.py` sent every
reconstruction-block record to the anonymous-infill dossier; the household layer has its own and now
points at it. Which surfaced **K26**: `publish.sh` deliberately keeps `docs/` out of the payload, so
on the deployed site **all 276 building cards link to a 404**.

## New 2026-08-15 — the photograph the sky is calibrated against is now in the repository, and it checks out

**R-REF1.** `renderers/web/js/world.js` derives its sky exposure, the whole of its
horizon-restore fit and the colour distance converges on from readings taken off one
photograph, quoted in the comments as `bar/dupage_tallgrass_2018-07-24.jpg`. **That file was
in no checkout.** `git ls-files` returned nothing for it on 2026-08-14, which made every sky
number in the renderer a quotation that could be read and not checked — and it was blocking
two parcels, R-W1 (whose targets §5 asks to be re-anchored by measuring a reference through
this code) and R-M1 (whose road-contrast thresholds are supposed to be derived from what a
real dirt track holds against real prairie, rather than picked to fit today's build).

**It is committed, and it is the right file.** Cassi Saari, *Restored tallgrass prairie in
DuPage County, Illinois*, 24 July 2018, Wikimedia Commons, at
`data/sources/assets/saari_2018_dupage_tallgrass/dupage_tallgrass_2018-07-24.jpg` with source
record `saari_2018_dupage_tallgrass`. Identification did not rest on the filename: the
Commons description is *"Prairie planting on former agricultural field in DuPage County"* —
the same restoration-not-remnant finding the 2026-08-10 sweep made about this photograph —
and the file's own EXIF says Samsung SM-G930V, **2018-07-24 09:32:25**, 26 mm equivalent,
orientation upright.

**The proof is that the numbers come back out of it.** `python3 tools/measure_reference.py`,
new with this parcel, re-measures the readings `world.js` quotes:

| reading | quoted in `world.js` | re-measured 2026-08-15 |
|---|---|---|
| 12 px above the sky/land step (the `HORIZON_RESTORE` fit target and the haze colour) | (136,163,192) | **(137,162,187)** |
| sky at ~14.4° above the horizon | (101,153,209) | **(97,151,208)** |
| sky at 8° | (125,165,205) | **(119,163,206)** |
| sky at 4° | (137,166,200) | **(133,166,201)** |

Nothing in the renderer was touched to make these agree, and the residual — a few units in
red and blue — is the one the code predicts: the tool averages the full frame width, the
original readings were taken at the shot's own view azimuth, and `world.js` records that the
model's horizon *brightness* is azimuth-dependent even where its hue is not.

**A second confirmation arrived unasked.** The 26 mm equivalent gives 57.0 px/deg vertically
and the sky/land step sits at row 820 of 3024, which puts the camera pitch at **−12.1°**. The
2026-08-10 prairie sweep had already established, from an entirely different direction, that
"the reference photographer had tilted down ~12°" — a correction that invalidated two rounds
of tuning at the time. Two derivations of the same number that never saw each other. The
useful form of it is that the frame is now **solved**: `elevation(row) = (820 − row) / 57.0`
degrees, reaching 14.4° above the horizon and 38.7° below. Any reading taken from this
photograph can now state the elevation it was taken at, which is what both of this project's
reference disagreements turned out to be about.

**The rights are recorded rather than assumed, and they are not permissive.** CC BY-SA 4.0,
attribution required. The file is committed **byte-for-byte unmodified** — SHA-1
`0da00f1178e7790b04c05364d78f7cb6a43992ae`, checked against the SHA-1 the Commons API reports
for the file page — so what this repository redistributes is the licensed work and not an
adaptation, and ShareAlike is not triggered by its presence. **Deriving from it would trigger
it**: a crop, a resample, a texture or a LUT is an adaptation that CC BY-SA 4.0 requires be
released under CC BY-SA 4.0. The project derives nothing from it (it is measured, never
sampled), `tools/publish.sh` does not copy `data/sources/`, and `assets/LICENSES.md` now
carries the clearance as an explicit, reasoned exception to its CC0/CC-BY-only default.

**One figure did not reproduce, and is left standing as a question rather than closed.**
`world.js` gives the bar's most distant land as (118,146,145); the 12 px immediately below the
step measure (106,130,140), because a naive band on that row lands partly on the far treeline
rather than on open sward. The original reading states no recipe, so this is a recipe
mismatch, not a contradiction — whoever needs that number next should define where it comes
from before quoting it.

**What this parcel did NOT do:** change a single rendered pixel. No renderer file was touched,
no threshold moved, no target re-anchored. R-W1 and R-M1 own those, and both are now unblocked.

## New 2026-08-15 — a lot was called free because a building's centroid was in the road

**T-A7.** T-A6 (below) made a block's room a function of its free lots. This is about how a lot
was known to be free: *no committed footprint has its centroid inside it*. The centroid is a
proxy for the building, and it fails on exactly the records the plat grid was built to correct —
a building placed from typed coordinates before the plat module existed can stand a metre or two
proud of its own street frontage, which puts its centroid in the ROADWAY and therefore in no lot
of any block. **Fourteen committed records were in that position.** Measured at `dev@968e389`:

| the building | block | lot | of itself on that lot | in the buildable part |
|---|---|---|---|---|
| **Temple Building** | `blk_south_water_franklin` | 0 | 18.6 m², 27 % | 4.2 m² |
| **Harmon & Loomis's store** | `blk_south_water_clark` | 0 | 29.2 m², 31 % | 9.5 m² |
| **Chicago Democrat office** | `blk_south_water_lasalle` | 6 | 31.2 m², 34 % | 11.4 m² |
| **Cook County courthouse** | `blk_randolph_lasalle` | 6 | 5.1 m², 13 % | 0.4 m² |
| `recon_1835_south_d5_034` | `blk_lake_dearborn` | 3 | 25.5 m², 36 % | 15.1 m² |

Four of the five are named, documented buildings, and the schedule was offering their lots to
anonymous invented roofs. **The claimed block is the sharpest case**: `blk_south_water_franklin`
was dealt six principal roofs for what it called seven free lots, and the Temple Building is on
one of them.

**The rule now has two tests, and each answers a different way of being wrong.** They live in
`tools/plat_occupancy.py`, which is the ONLY implementation — `tools/reconcile_665.py` and
`tools/generate_block_infill.py` both import it, where T-A6 had left them with a copy each.

1. **A building stands on the lot most of it is on**, by measured area. The same claim the
   centroid made, made about the building instead of about a point inside it. On the committed
   dataset it is purely additive: **no record changes lot**, occupied lots go 79 → 84, and
   nothing that read taken became free.
2. **It occupies that lot only where it reaches the lot's buildable part** — the lot inset by
   the 1.5 m every new roof must keep from its own lot lines. **J. H. Kinzie's store earns this
   test**: 9.7 m² of it lies on `blk_south_water_franklin` lot 2 and *none* inside the buildable
   inset, so a roof still fits there clear of it and the schedule may still deal one. Without
   test two the town would lose roofs it can honestly have.

**The ledger had the same defect from the other side.** A roof was attributed to a block by its
position POINT, so three buildings whose point is in the roadway were counted as standing in no
block at all: the **Exchange Coffee House** (which holds nine tenths of a lot of the claimed
block), **Harmon & Loomis's store** and the **Tremont House**. Their roofs were never subtracted
from the headroom of the block they physically stand in. A roof standing on a block's lot stands
in that block.

**What it cost.** Schedulable-on-covered-ground **66 → 61**; gated on coverage **333 → 338**.
Standing roofs are unchanged at 266, remaining at 399 — nothing was built or removed. Four blocks
lose a free lot each and `blk_south_water_clark` also gains two standing roofs, so its deal drops
from 7 to 5.

**What it measured and deliberately did not call occupancy.** `recon_1835_west_018` laps 11.9 m²
onto `blk_randolph_clinton` lot 2, where T-A4 stands a principal roof. Test one seats it on lot 4,
where 82 % of it is, so that placement stands. A rule that called every lap an occupation would
have condemned a committed, gated placement over a corner of a building, and whether two roofs
may stand three metres apart across a conjectural side lot line is the separation gate's question
— which it passed. Recorded here so the silence is not mistaken for nobody having looked.

**What this parcel did NOT do:** build a block. T-A7 claimed `blk_south_water_franklin` and found
it could not be built honestly; it returns to the queue with a corrected deal — 7 roofs, 5
principal and 2 ancillary, on six free lots.

## New 2026-08-15 — half the open blocks were scheduled roofs their own lots could not hold

**T-A6.** The 665-roof schedule counted a block's room in ROOFS and never in LOTS, and a principal
roof needs a free lot. Measured across the ten open blocks at `dev@f6f2bcb`, against the placement
gates in `tools/generate_block_infill.py` that would have refused them:

| block | lots | free | dealt principal | what the recipe would have hit |
|---|---|---|---|---|
| `blk_south_water_clark` | 8 | 6 | **7** | **unwritable** — no seventh free lot exists |
| `blk_lake_market` | 8 | 6 | **7** | **unwritable** — no seventh free lot exists |
| `blk_south_water_wells` | 8 | 7 | 7 | fills the block; no lot left open |
| `blk_randolph_franklin` | 8 | 7 | 7 | fills the block; no lot left open |
| `blk_randolph_clark` | 8 | 7 | 7 | fills the block; no lot left open |
| `blk_randolph_dearborn` | 8 | 3 | **0** (one ancillary) | **unwritable** — a yard building behind no roof |

**Five of the ten, and three distinct failures, not one.** Two blocks were dealt more principal
roofs than they had lots, which no recipe could have written down at all. Three were dealt exactly
as many as they had free, which is writable and *worse*: it silently spends the vacancy the parcel
recipe's own placement rule promises — *"a block at capacity is a claim about 1835 that the
evidence does not support; the schedule's capacity is a ceiling"* — so the first parcel to take one
would have filled a block to capacity while passing every gate. And `blk_randolph_dearborn`, the
T-A3h backfill, was dealt a single yard building and no principal roof to stand it behind: the same
blindness seen from the other end, because an ancillary roof's gate is that it serves a principal
roof the same parcel built.

**Why it was invisible.** Occupancy was counted in roofs — `standing_roofs` — so two roofs on one
lot and two roofs on two lots subtracted the same amount of headroom. The block generator has
derived true lot occupancy since T-A4 and the schedule never did, so the two halves of the same
question were being answered by different arithmetic. Nothing shipped wrong: the gates that would
have caught each of these are real and would have fired. **The defect was that they fire at the
END of a parcel** — after a run has claimed a block, read the schedule and written a recipe.

**The fix is that the deal now knows what a lot is.** `tools/reconcile_665.py` derives lot
occupancy by the *same rule the generator uses* — footprint centroid against the committed lot
polygon — and a block's room becomes `principal = min(free lots − 1, roof headroom)` with
`ancillary` bounded by both the 154:511 ratio and the principals themselves. The deal offers a
token a unit cannot take to the next unit instead of dropping it, so every marginal still closes,
and a new assertion fails the build if any unit is ever dealt past its room.

**What it cost, and the number is the point.** Schedulable-on-covered-ground **71 → 66**; gated on
coverage **328 → 333**. Five roofs moved from "buildable now" to "waiting on coverage" because
they never had anywhere to stand. **All ten open blocks are now buildable and every one of them
keeps a lot open**, which is the state T-A7 onward can be run from without re-deriving this.

**What this parcel did NOT do:** build a block. T-A6 claimed `blk_randolph_franklin` and found it
was one of the three that could not be built honestly; the block is released back to the queue with
a corrected mix (6 principal + 2 ancillary, one lot open) for the next run to take.

## New 2026-08-15 — the card adds its own claims up, and 204 of 279 buildings have nothing attested about them

**K23b**, the substantive half of the owner's report and the sequel to K23a below. Every
provenance card now opens with **`What did we include, and where did it come from?`** — three
rows, one per level, naming the claims that stand at each and saying where they came from.

**It is a partition, which is the whole of why it can be gated.** Every graded claim the card
renders lands in exactly one row, so the release check is a RECOUNT rather than a look: pick
every building at both viewports, tally the confidence chips off the RENDERED card, and require
the section's three numbers to be those numbers. **276 of 276 loaded buildings agree.** The
recount reuses the older chip-coverage gate's own selector on purpose — two definitions of "a
claim on this card" is how a summary would come to disagree with the card while both gates
stayed green.

**The dataset, counted for the first time this way.** 279 records carry **3,675 graded claims —
199 `attested`, 509 `inferred`, 2,967 `reconstructed`.** **204 of the 279 have no attested claim
at all**, so a row that rendered only when it had something would go silent on three quarters of
the town at the exact moment a visitor needs telling. It says *"Nothing about this building is
attested by a source."* instead.

**A citation means a different thing at each level.** `From` on an attested claim; `Bounded by`
on an invented one — 193 anonymous roofs cite the reconstruction spec and Andreas on every
attribute, and one `sources:` label over all three rows would have printed a nineteenth-century
history as attribution for a building nobody claims stood there.

**Two findings that are not the section.**

- **69 buildings have inventions that nothing is recorded as bounding.** Of the 270 records with
  at least one `reconstructed` claim, 69 cite nothing on any of them, so their `Bounded by` line
  reads *"Nothing is cited as bounding these."* The bottom tier requires a note and not a source
  — deliberately — but nobody had ever counted the consequence. The Sauganash Hotel is one of the
  69. Visible now rather than fixed; whether those should acquire a bound is research.
- **Attested is not built, on 14 records.** The Western Hotel's stables are attested by a
  pre-fire account and there is nothing of them in the model. A summary of what was *included*
  that counted them under "attested" and stopped would name something that is not there, so the
  row repeats the mark the table below already carries: *Not in the model: stables*.

## New 2026-08-15 — 193 buildings were named a grade better than their own record, and the release gate was holding it in place

**K23a**, owner-reported from a card on the dev preview. The heading read **"Inferred A1 stable
#07"** and every chip beneath it read **RECONSTRUCTED**. The heading was the wrong one, on
**193 structure records** — every anonymous roof this project has ever generated.

**It is the residue of a fix that worked.** The v76 merge of 2026-08-13 moved 9,076 values onto
`attested / inferred / reconstructed` and re-graded 1,694 that had claimed to be reasoning when
they were invention. It moved the DATA. The PROSE is hardcoded in the generators, and it did not
move — so `inferred` went from being the BOTTOM tier (where "Inferred A1 stable" was honest) to
the MIDDLE one, *reasoned from evidence about this particular thing*, which an anonymous
count-unit is precisely not. **Nothing about any building changed here**: not a position, a
dimension, a source or a grade. Only what the card calls them.

**Scale, exactly, so a later sweep can tell drift from a fresh fault.** 193 names; 162
`symbolic_location` strings; 193 `research_note` openers partitioning cleanly into 142
`RECOMMENDED / GENERATED`, 31 `INFERRED BUILDING` and 20 `INFERRED / GENERATED`; every
`change_note` on an anonymous roof; the card's own reconstruction flag; and the household and
person labels of the K1 layer. **`recommended` is the word this project renamed away from BY NAME
on 2026-08-13** and then printed on 142 cards for a fortnight.

**Five generators, not the two the parcel listed — and a sixth stage that is not a generator.**
`generate_inferred_names.py` runs AFTER the household programme and rewrites the household's own
label. Regenerating households without it deletes every invented resident's name and
`name_basis` — the whole of K18 — and **the household programme's `--check` cannot see this**,
because it overlays the naming pass before comparing. `--check` is green either way. The order is
`generate_inferred_households.py` then `generate_inferred_names.py`, and it is now written into
ROADMAP K23a where the next person will look.

**The gate was enforcing the fault.** `smoke_renderer.mjs` asserted the household label matched
`/inferred/`. So the thing that should have caught this was requiring it. That assertion is
pinned to the head's own `grade` now, and a new whole-registry check fails the release on any
name opening with a grade its record does not carry, or with any of the three retired words —
with the fault planted in the same pass, so a gate scanning a clean tree cannot be mistaken for
a gate scanning nothing.

**Two things outside the app were worse than the cards.** `docs/PROVENANCE.md` — the page you
send someone to when they ask what the grades mean — still defined `documented / inferred /
conjectural`, so a record written by following it **fails the build**. And `validate.py`'s own
errors named the wrong tier: a sourceless `attested` value reported *"documented requires at
least one source_id"*. Both corrected; ROADMAP K16, which proposed a third vocabulary that never
shipped, is **CLOSED as superseded**.

**Still open, and it is the half the owner cared most about.** K23b — *say what was INCLUDED at
each level and where it came from* — is untouched. The names are no longer wrong; the cards still
do not tell a visitor that a building's footprint, height, roof form and position were all
invented and only its block was reasoned.

## New 2026-08-14 — the block where two layers of this reconstruction met on the same ground, and the adoption rule grew a third test

**T-A5.** `blk_randolph_market` — Randolph, Franklin, Washington, Market — is the first South
Division block of the Randolph row and now carries **eight anonymous roofs**: four dwellings, one
per lot on four of the six free lots, and four yard buildings off the block alley. **Standing roofs
258 → 266; remaining 407 → 399, 71 of them on ground the project has coverage for.** Households
**155 → 156**, persons **191 → 192**. Recorded in **L97**. The parcel authors no coordinates: every
metre is read off the committed K7 lot polygons, which is what has made every block since T-A2 a
recipe entry rather than a geometry argument. The recipe cleared every one of the generator's
placement gates on its first run — no lot-line, separation, corridor, relief or occupancy failure
to iterate against — which is what the accumulated gates of T-A2 through T-A4 were for.

**The block was already built on by THIS project's other half.** L95 recorded the first
partly-built block and the roofs in its way came from the pre-plat West Division density recipe.
Here the two standing roofs are `inf_sawyer_dwelling_a` and `_b` — the dwellings of the occupation
census's own two sawyer households, placed from typed local-ENU coordinates before the plat module
existed. The layer that argues who the town held and the layer that fills its blocks have now
collided, and the T-A4 machinery absorbed it without a change: occupancy derived from the committed
footprints, lots 4 and 6 refused a second principal roof, headroom spent on the six free lots.

**Where the vacancy falls was decided by arithmetic, and the parcel says so rather than dressing it
up.** Both standing roofs sit on the Randolph face, so the two lots free there are exactly the two
the frontage-value typology wants for the better cottages, and the programme's alternating vacancy
has nowhere to fall but Washington. Had the schedule dealt one roof fewer the pattern would have
read as deliberate. `arrangement_note` and L97 both state it.

### The third adoption test — the question T-A4 left open, settled

T-A2h's rule 6 had **two** tests: the trade's committed argument must call its count a floor, and
the roof's family must be one this layer already houses that trade in. T-A4 met a case neither
covered — a D3 carpenter roof on the first West Division block, when all eleven carpenter
households stood north or south — and refused it **by hand**, leaving the question to T-A5.

**Rule 6 now has three tests**, the third being the roof's **division**. It is the family test made
about the other axis of the same table: where a trade lived is as much a claim about the town as
what it lived in. **It was checked against every adoption decision taken before it and recovers all
four** — T-A2h's carpenter adopted, T-A2h's labourer adopted, T-A4's labourer adopted, T-A4's
carpenter refused. A test that had to be told those answers would be a preference; one that
recovers them is a rule. This block's D3 on lot 7 passes all three, so a twelfth carpenter household
is inferred (carpenter 11 → 12) and the other seven roofs stay anonymous count-units.

### What the test cannot answer, and it is not about the trades — **K21**

The sawyers whose two roofs stand on this very block **pass test 1** — their argument reads "two
sawyer households are inferred, **the smallest number that answers the demand**" — and fail test 2
for a reason that has nothing to do with sawyers: their dwellings are bespoke
`inf_sawyer_dwelling_*` records carrying no `reconstruction.family` at all, so the question "which
family does this layer house that trade in" has nothing to read. **Four trades of twenty-nine are
housed that way and only that way** — brickmaker, packer, sawyer, wheelwright — and eight more are
partly so. For those four the second test is **silent, not negative**, and silence is currently
being read as refusal. That is the conservative direction and it is not the same thing. Opened as
ROADMAP K21.

### K20 measured again, from a one-household insertion

Inserting a single household renamed **17 of the 33** carried-over invented persons in the touched
household files, because the name allocator deals by index. T-A2h's two-person insertion renamed
25 of 94; this is the same defect at the same rate and it is still open. Nothing about anybody's
argued history changed — only the invented name attached to it. The churn is why this parcel's diff
touches 24 household files for one addition.

## Fixed 2026-08-14 — the roads were invisible, every street check was green, and the prime suspect was innocent

R-BUG2, owner-reported: *"the town roads seem to disappear in places and when you fly over them
you lose them."* True at both viewports. **Two independent faults**, and the mechanism the parcel
named as most likely turned out to be the one thing that was helping.

**The gate could not see any of it, and that is the first thing that was wrong.**
`tools/smoke_renderer.mjs` asserted seventeen street records, ~100 000 vertices, drape error under
1e-5 m, no vertex over water — all true, all green, all beside the point. **Draped is not seen.**
Nothing in this repository asked whether a road reached the screen.

**What the new check does.** `roadContrast()` holds the scene at two anchors a visitor is offered —
`south_water` at eye height down an open street, `from_above` at the aerial anchor — and takes
three frames: the real render **R**, the same geometry drawn as an opaque marker with a
deliberately deeper polygon offset **M**, and the scene with the streets hidden **O**. A probe on a
committed centreline counts only where **M** reached the screen, so roads genuinely hidden behind a
building, a tree or a rise leave the sample rather than scoring as faults, while a road losing the
depth fight to the terrain stays in it. The score is `|L*(R) − L*(O)|` on the critic harness's own
`labL`. Bars: median **ΔL\* ≥ 1.8** and **≥ 55 %** of probes at ΔL\* ≥ 2 per band, gated to 600 m.

**Measured with the fault in — both bars fail, which is the acceptance:** `south_water` 250–600 m
**0.3 L\*, 14 % perceptible**; `from_above` 100–250 m **1.1 L\*, 0 % of eleven probes**. With the
fix, desktop: `south_water` **4.2 / 3.9 / 4.0** across 40–100, 100–250, 250–600 m at 70 / 89 / 92 %,
`from_above` **2.9 / 2.4** at 91 / 63 %.

**Fault 1 — the depth fight, and it is the reported "in places".** A road is earth painted flat on
the terrain at the same height, held in front by one unit of polygon offset. Depth precision
degrades with distance, so past ~250 m the terrain won in patches. `−4 / −8` alone took the failing
band to **3.3 L\* / 71 %**. No vertex moved; `worstDrape` still gates at 1e-5 m.

**Fault 2 — the road was 4 % opaque, and it is the reported loss from the air.** At the aerial
anchor the ribbon is wide, unoccluded and wins depth, and it still scored 1.1 / 0 % — *neither* the
offset *nor* the thin-ribbon rule moved that band at all. A lightly worn track's alpha was
`0.08 + ruts*0.54 − crown*0.04`: 8 % earth over 92 % prairie away from the ruts, 4 % at the crown.
Baselines raised to **0.54 / 0.38 / 0.28**, modulation shape and class ordering untouched, recorded
as **L96** amending L79 — which already recorded these numbers as invention rather than measurement.

**Refuted — mip-averaged alpha falling under `alphaTest`.** The parcel's prime suspect, and the
shape of the v74 treeline bug. Turning mipmaps off made **every** band worse (`south_water`
250–600 m: 22 % of probes reaching the screen with mips, **6 %** without). The mip chain is holding
a sub-pixel ribbon together, not erasing it. `minFilter` is unchanged, and the instruction to
measure before choosing is what stopped a "fix" that would have made this worse.

**Not acted on:** `transparent: true` with `alphaTest` does sort a town-wide mesh on a meaningless
bounding-sphere centre, and the opaque queue measured slightly better — but an unblended
alpha-tested fragment draws at full strength, which would make every road solid and delete the
graded/worn/light distinction the dataset carries. If the sort ever bites, the answer is
per-record `renderOrder`, not opacity.

**What this cost the gate to learn:** `from_above` is an aerial anchor, and leaving the camera
there broke the horizon-timber check downstream — it reads the band the tree solver builds around
the camera and reported nought of nought covered bearings. A measurement that moves the camera owes
the next one its pose back.

## New 2026-08-14 — the first block across the river, on ground that was already partly built

**T-A4.** `blk_randolph_clinton` — Randolph, Canal, Washington, Clinton — is the first West
Division block the plat module reaches and now carries **seven anonymous roofs**: four dwellings on
four lots, three yard buildings off the alley. The town stands at **258 roofs of 665**; 407 remain
and **79 of those have modelled ground**. One lot is left bare on purpose. The geometry half was a
recipe entry and nothing else, exactly as T-A2 predicted for the third time running — what this
block cost was in the gates, and it is the first one that could have found this.

**Three roofs were already standing on it, and nothing could see them.** Every block parcel so far
arrived at empty ground, so treating all eight lots as free was correct twice and would have been
wrong here: `recon_1835_west_018`, `_019` and `_021` sit inside this block, placed from typed
coordinates months before the plat module existed, and **no record of theirs names a lot** because
there were no lots to name. The one-principal-per-lot check reads only the records the parcel
builds, so an occupied lot and a free one were the same thing to it, and **the separation gate does
not close the difference: two principal roofs twelve metres apart on one twenty-five-metre lot pass
every test in the file.** A second house on somebody's lot would not have looked like a defect from
any direction — the town would simply have been slightly denser than the ground it stands on.

**The fix derives the answer rather than asking for it.** Which lots are taken is read off the
committed footprints of the records that stand there; a recipe that had to be told would be a
second opinion about the same ground, which is the defect the plat module was built to retire. Two
gates ride with it. A yard building must stand on a lot this parcel gave a principal roof, because
a yard building behind somebody else's house is a claim about their household. And **every lot of
the block must now be built on, already occupied, or named open with its reasoning** — those three
were counted in three places and nothing made them meet, so a lot could have been called open in
the recipe with a house standing on it, which is a false statement about the town in the file that
documents the town. All five refusals were verified by committing each one deliberately.

**Two things this block exposed by not being South.** The visitor-facing location line on every
generated record read *"South Division"* as a literal — true of every record that had ever existed
and wrong on all seven of these, which is the shape of defect only a first case finds. And the
665-roof ledger attributed **every anonymous roof in the West Division to the Wolf Point recipe**,
because until today that was the same set: it read the seven new roofs as seven of that recipe's
own placements emitted out of order and refused to derive at all. It counts by the programme phase
each record names now, and the West recipe's remainder holds at **35**, unchanged, with seven West
roofs standing beside it.

**One household adopted, one refused, and the refusal is about the rule rather than the roof.** The
block deals a D1 and a D3 — the two families T-A2h's rule admits. The D1 log cabin is adopted: the
labourer's count is a floor by its own committed text, D1 is the family this layer houses nine of
its eleven housed labourers in, and this layer **already places two labouring households in the
West Division**, so nothing crosses a division line the programme had not already argued.
Households **154 → 155**, persons **190 → 191**. The D3 carpenter is refused: rule 6's two tests
are silent on division and all eleven carpenter households stand north or south, so a twelfth west
of the river would be a new claim about where the town's carpenters lived, arriving as a side
effect of a block parcel — the exact failure mode rule 6 exists to prevent. **Whether the rule
takes a division test is now ROADMAP T-A5's to settle**, once, rather than each parcel's to decide
again. No human figure is drawn (L1), unchanged.

## New 2026-08-14 — the baseline scored: **4.18 of 10**, and two of the three headline numbers were measuring the wrong thing

**R-G1.** The scored half of G0.2 is in, and the bar it was measured against is the one §0 says
can actually be held: eight axes, 1–10, five named stations, written justification, a specific
fix for every axis under 8, against this project's own reference set — the twelve pre-fire
pictorial plates and the verified tallgrass photographs — and never against a commercial game
frame. Pass is **mean ≥ 8.0 with no axis below 7**. The baseline is **4.18**, and **every one of
the eight axes is below 7**. That is the number later phases have to beat, and it is recorded
before W1 touches the renderer precisely so that there is something to beat.

**The protocol's independence condition is satisfied and worth stating.** This parcel wrote no
code at all — `git diff --stat` for it is three documents and a changelog entry — and the run
that built `tools/critic_shots.mjs` and `tools/critic_metrics.mjs` was a different one. The
scorer read the frames.

### The scores

| station | light | material | texture | geometry | atmosphere | post | composition | history | mean |
|---|---|---|---|---|---|---|---|---|---|
| `sauganash` | 3 | 3 | 1 | 5 | 4 | 4 | 6 | 7 | **4.13** |
| `first_post_office` | 3 | 4 | 1 | 6 | 4 | 4 | 7 | 8 | **4.63** |
| `south_water` | 3 | 3 | 1 | 3 | 4 | 4 | 4 | 5 | **3.38** |
| `prairie_west` | 5 | 5 | 2 | 5 | 4 | 4 | 6 | 7 | **4.75** |
| `river_bank` | 2 | 3 | 2 | 4 | 5 | 3 | 6 | 7 | **4.00** |
| **axis mean** | **3.2** | **3.6** | **1.4** | **4.6** | **4.2** | **3.8** | **5.8** | **6.8** | **4.18** |

Desktop 1280×800. The mobile set was captured and measured in the same run and is **not
scored** — the rubric is a reading of frames and five stations at one viewport is what the
protocol asks for; a second viewport would double the reading without changing which phase owns
anything. Six stations (`sauganash_wing`, `lake_market`, `forks`, `green_tree`, `from_above`,
`prairie_south`) were read for context and deliberately not scored.

**Texture at 1.4 is the floor of the whole exercise and it is not a surprise** — §1 item 9 says
there are zero texture maps on 244 assets, and the frames show it: clapboard is *geometry*, a
roof is one flat value, chinking is a second flat value, and the only texture in a town frame is
the ground. **Historical accuracy at 6.8 is the ceiling**, and it is the axis this project is
actually good at: at `first_post_office` the footprint is Andreas twice over, the position is
surveyed, and the unresolved reads are carried on the record instead of being resolved into the
geometry. The gap between 1.4 and 6.8 is the shape of this project — the research is ahead of
the rendering by five points on a ten-point scale.

### Why each axis scored what it did, and the one fix that moves it

Every axis is below 8, so every axis carries a fix and a phase. The fixes are written into
`docs/ROADMAP.md` against the parcel that owns them.

**Lighting & shadow — 3.2 → W1.** The only cast shadow legible in the five frames is each
chimney's, on the roof beside it. The directional light casts and the ground receives, so the
shadow map is not switched off — it is geometry: at 12:30 on 1 July at
41.89° N the sun stands **70.5°** up and a shadow is **0.354 ×** the height of what throws it, so
a house's shadow lies under its own eaves and a walker's frame carries almost no shadow
information. The scene note chose that hour deliberately, to light the south elevation the
records call white, and the trade is sound — but its cost has never been written down, and it is
this: **form has to be carried by something other than shadow, and the two candidates are both
switched off** (AO is `baked_ao: false` on all 244 assets, §1 item 10; environment lighting is
built and not installed, §1 item 11). Against that, `HemisphereLight` at **2.4** under a
`DirectionalLight` at **3.0** is a 0.44 fill ratio, which flattens what little modelling the
angle leaves. *Fix: W1 installs the exposed HDRI, and the hemisphere and bounce come DOWN in the
same change — the trap already written on the parcel. Nothing here argues for moving the hour.*

**Material realism — 3.6 → W2 (no-Blender half).** Every surface is one flat colour. A roof, a
whitewashed clapboard wall, a hewn log and its chinking, and a chimney differ only in hue —
there is no roughness variation anywhere in the town, so nothing reads as painted, weathered or
wet. The Wau-Bun blue shutters at `sauganash` sit at the same value as the glazing beside them.
*Fix: the material sheet W2's no-Blender half is already scoped to write — which surfaces exist,
what each is made of, and which archetype parameter selects it.*

**Texture detail & tiling — 1.4 → W2.** Zero texture maps on 244 assets; the ground is the only
textured surface in a town frame and its near field is a grazing-angle smear. The axis cannot
rise until W2's bake half lands. *Fix: W2, both halves; nothing else moves this.*

**Geometric detail & silhouette — 4.6 → W2/W3, and one item for lane 2.** Massing is good — the
`sauganash` ell and knee wall, `first_post_office`'s eave overhang and log ends, `river_bank`'s
cordgrass — and openings are where the silhouette fails: no reveal, no sill, no sash, no muntin
anywhere in the set, so the 6-over-6 rhythm the Green Tree plate documents does not exist. The
worse failure is at `south_water`, and it is a **data** failure rather than a rendering one: the
horizon row of the business street is one gable stamped a dozen times at even spacing, where the
research knows a store, an auction room, two newspaper offices and a warehouse. *Fix: openings to
W3's cage work and W2's params; the repeated stamp to lane 2 — the anonymous placeholder massing
needs per-record variation in width, pitch and eave height drawn from the family band it already
carries.*

**Atmosphere — 4.2 → W4.** The sky is a cloudless gradient at every station, and the 200–1500 m
band holds nothing for the haze to act on, so the far treeline meets its sky with no separation
at four of the five. The one place it works is `river_bank`, where the far shore genuinely
recedes — the 2026-08-13 far-timber fix is visible in the frame. *Fix: W4, items 1–6, plus a sky
that is not a single gradient.*

**Post-processing — 3.8 → W5.** Tone mapping and nothing else. Visible stair-stepping on the
`sauganash` ridge and along the water/vegetation boundary at `river_bank`, where the water plane
also shows rectangular stepping against the emergent stand. *Fix: W5's SMAA pass, and R-BUG1 is
in the same frame.*

**Composition — 5.8 → the anchors, not a phase.** Four of the five stations frame their subject
honestly. `south_water` does not: 60 % of its frame is foreground grass and the business street
it is named for is a 40-pixel band on the horizon. An anchor a visitor is offered should show the
thing it is named after. *Fix: `south_water`'s anchor in `data/scenes/1835.json` wants a position
on the street rather than in the field south of it — one record, no code, and it is the cheapest
point on this whole table.*

**Historical accuracy — 6.8 → mostly earned, one real deduction.** `first_post_office` scores 8:
evidence footprint, surveyed position, unresolved reads carried on the record. The deduction is
at `south_water` (5) for the same repeated stamp — uniformity that no source claims, understating
what the research knows — and at `prairie_west` (7) for the flower load. **CORRECTED 2026-08-15
by R-W4c(a): the "two orders of magnitude" this paragraph used to claim was a measurement error,
and it was 18× too big.** `0.0012` is what the flower-load recipe reports, and that recipe misses
94.5 % of the bloom at this station — its hue cut at 50° puts a yellow coneflower in with the
grass. Measured by hiding the flower heads and subtracting, the render's true bloom here is
**2.19 %** of hued ground. Against the 4–6 % target that is a factor of two to three, which is
still a real deduction and still not fixed. Read ROADMAP R-W4c(a) before quoting either number —
in particular, the 4–6 % target was itself derived with the blind recipe and is **not yet on the
same scale** as the 2.19 %. *Fix: R-W4c(b) for the flower load, which must re-derive the target
first; lane 2 for the stamp.*

### The three findings that are not scores

**1. Two of the three numbers §1 item 7 rests on are measuring the canopy, not shadow.** The
baseline recorded "shadows still clip to literal black — 12,063 pure `(0,0,0)` pixels at
`river_bank`, 11,015 at `first_post_office`" and a darkest ground decile as low as **L 0.93**.
Both are real measurements and both are attributed to the wrong surface. Connected components of
the literal-black mask, with their bounding boxes:

| station | literal black | components | of it in components lying **entirely above** the median land/sky row |
|---|---|---|---|
| `first_post_office` | 11,015 | 9 | **100 %** (largest 8,376 px, x957–1144 y42–117 — the crown at top right) |
| `river_bank` | 12,063 | 14 | **94 %** (six crown clusters, all y ≤ 230, boundary row 369) |
| `prairie_south` | 2,315 | 10 | **99.7 %** (all y ≤ 261, boundary row 395) |
| `sauganash_wing` | 61 | 1 | **100 %** (one crown edge) |

Not one literal-black pixel in the desktop set is on shaded ground. They are the shaded side of
the near-tree canopy — the `timber` `MeshStandardMaterial`, vertex-coloured, quantising to zero
where a leaf faces away from a 70.5° sun. The darkest-decile figure is the same surface reached
a second way: the metric finds "ground" as everything below the per-column land/sky line, and in
a column carrying a tree that line is the *top of the crown*, so the crown counts as ground.
Measured at `river_bank`: **63,711 pixels at L < 2, of which 95.7 % lie above the median land/sky
row**; the decile pool is ~55,000, so the L 0.93 reading is a canopy measurement end to end.
`south_water` 92.7 %, `first_post_office` 88.6 %. **`sauganash_wing` and `lake_market` are the
exceptions** — their near-black is 90–94 % *below* that row and is a different population, not
diagnosed here.

Consequence, and it changes what W1 does: **raising the shadow floor will not move either
number.** What lights a leaf facing away from the sun is the environment term W1 exists to
install, or a floor on the crown's darkest albedo. The fix stays in W1; the mechanism named in
§1 item 7 does not survive.

**2. The horizon-timber metric cannot tell a treeline from a townscape, and the town just moved
it.** The recipe counts a horizon column as timbered if any pixel in the band above the land/sky
line falls 3 luma below, or 3 G−B above, the sky extrapolated from the 20 rows over it. A gable
end breaking the skyline satisfies that as surely as an oak. Re-running the harness on today's
`dev` — with **no renderer change since the baseline** (`git diff --stat 282dd9a..HEAD --
renderers/` is `changelog.js`, 41 lines, and nothing else) — nine stations reproduce their timber
figures and **`prairie_south` moves from 0.364 to 0.436 all / 0.340 to 0.441 centre**, a 20 %
gain. What changed between the two runs is 19 anonymous roofs (T-A2 and T-A3), and the frame
shows them: the left third of `prairie_south`'s skyline is grey gable ends. **The § 5 target of
≥ 90 % horizon timber coverage can therefore be satisfied by building the town**, which is not
what item 5 was ever about. R-W4 owns the target; it needs a discriminator, or a second metric
that measures only columns with no structure in them, before its acceptance number means
anything.

**3. Lane 2 is spending the draw-call budget faster than lane 1 can recover it.** **RESOLVED
2026-08-15 by R-W5a — see the top of this file.** The +11 was 11 new material GROUPS, the growth
term is now zero, and no station is over budget at either viewport. The reading below is kept as
the measurement that found it. Same two runs,
same renderer, +19 structure records (242 → 261, +7.9 %):

| | `sauganash` | `s'nash_wing` | `lake_market` | `f_post_office` | `forks` | `green_tree` | `south_water` | `from_above` | `prairie_south` | `prairie_west` | `river_bank` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| desktop baseline | 65 | 66 | 78 | 66 | 87 | 91 | 85 | 67 | 73 | 97 | 56 |
| desktop today | 65 | 77 | 89 | 66 | 98 | 102 | 96 | 67 | 84 | 108 | 56 |
| mobile baseline | 62 | 63 | 66 | 60 | 82 | 88 | 83 | 61 | 71 | 94 | 49 |
| mobile today | 62 | 72 | 77 | 60 | 82 | 99 | 94 | 61 | 82 | 105 | 49 |

**Exactly +11 desktop at seven of eleven stations and exactly 0 at the other four** — and
triangles rose by only 244–562, so this is per-object cost, not geometry. Stations over the
**≤ 80** budget go **4 → 6** on desktop and **4 → 5** on mobile; the worst goes 97 → 108. The
uniformity is the part nobody has explained: +11 at bearings 150° apart, and +0 at `from_above`,
which sees the whole town. **Straight-line extrapolation on the remaining 414 roofs is about
+240 draw calls** against a budget of 80. That is not a reason to slow lane 2 down — the roofs
are the product — but the budget cannot be met by tuning after the fact, and R-W5 should treat
batching as its first question rather than its last. The `from_above` zero is a lead: something
already drops these objects at distance.

### What this does not do

It changes no code, moves no building and re-measures no reference photograph. The §5 targets
that were set from the uncommitted 2026-08-10 sweep still need re-anchoring by measuring a
reference plate through `tools/critic_metrics.mjs`, which is still a one-line job and is still
not done. And a rubric score is one reader's judgement with its reasoning attached — the fixes
below are the durable half, not the number.

## New 2026-08-14 — two roofs of ten given an occupant, and the rule that refused the other eight

**T-A2h.** The parcel was expected to argue about the town's trade mix. What it found is that a
block parcel puts ten dwellings on the plat faster than any such argument can move, so the
question that mattered was **who is allowed to start one**. The occupation census is a claim about
Chicago — 3,265 people in 398 dwellings, calibrated against Andreas's 1833 roster — and a census
that grows every time somebody draws a cottage is a census fitted to the model. Two of
`blk_randolph_wells`'s ten roofs are adopted into the inferred-household layer; the other eight
stay anonymous count-units, which is what they already were.

**The rule now lives in the household programme's own `method` list**, where the next parcel will
read it. A block roof may be adopted only where BOTH tests pass: the trade's committed argument
states in its own text that its count is a **floor rather than a bound**, and the roof's family is
one this layer **already houses that trade in**.

- **Two of twenty-nine trades pass the first test** — the carpenter (*"the shop count is a floor
  under the trade, not a measure of it"*) and the labourer (*"still a small fraction of what 3,265
  people implies"*). Everything else states a ceiling — the plasterer's and the drover's say *"and
  no more"* outright — or is bounded by a workshop or store family's roof target. Two apparent
  further matches are a false positive worth naming: *floor* appears in the laundress and
  boarding-house-keeper entries only inside the Andreas quotation *"with the floor covered
  besides"*.
- **The second test, measured against the layer as it stands, picks the same two families.** All 8
  of the layer's adopted labouring households live in a D1 and 9 of its 10 carpenters in a D3 —
  and a D1 log cabin and a D3 one-room cottage are two of the seven dwellings this block deals.
  The tests were derived independently and agreed on the first block they were applied to, which
  is the only reason to trust either of them.
- **Households 152 → 154, persons 188 → 190, adopted anonymous roofs 83 → 85, standing roofs
  unchanged at 251.** This parcel built nothing, moved nothing and regraded nothing. The two
  roofs' presence, position and footprint are exactly as invented after the adoption as before it;
  what they gain is an argued occupant instead of a blank. Recorded as **L94**.
- **The H1 and H2 houses are the refusal worth keeping.** The schedule allows 18 larger houses and
  14 merchant or professional houses in the whole town, and their occupants are the most likely
  people in this dataset to be nameable. Inventing an anonymous merchant into one would break the
  programme's own rule never to infer a person where a documented one is available. Those two want
  T-I3's treatment — a reading of the record — and not a draw from a census.
- **The adoption is authored once and gated in both directions.** `tools/generate_block_infill.py`
  now reads the household ledger through `tools/inferred_occupancy.py`, exactly as the three
  earlier anonymous parcels do, so no generated record is hand-edited and the drift check that
  makes these parcels trustworthy still binds. A household pointed at an ancillary roof fails by
  name — a yard building serves the lot it stands behind, and nobody lives in a privy — and a roof
  the ledger names that no recipe builds fails by name. **Verified by doing each.**
- **What it churned and did not fix, recorded as ROADMAP K20.** Adding two people renamed **25 of
  the 94** reconstructed residents. The invented-name allocator deals names round each pool by
  index within a bucket, so an insertion shifts everyone after it. No grade moved and every name
  re-derives under `--check`, but the generator's own docstring says the assignment is a function
  of a person's id when it is a function of the whole population — and every future block parcel
  will rewrite a quarter of the town's invented names as a side effect until that is fixed.

**Gates:** `tools/check.sh` green; `node tools/smoke_renderer.mjs` green at 390×780 and 1280×800,
zero page errors, run against the source tree and again with `--published`.

## New 2026-08-14 — a block filled in, and the table nothing had ever read

**T-A2.** `blk_randolph_wells` — Randolph, LaSalle, Washington, Wells — stood empty and now
carries **ten anonymous roofs**: seven principal buildings on seven of its eight lots, three yard
buildings off the alley, to the family mix the 665-roof schedule apportioned it. The town stands
at **242 roofs of 665**; 423 remain and **95 of those have modelled ground**. One lot is left
bare on purpose, and which lot is arbitrary — recorded as such in **L92**, with the frontage
argument (larger houses to Randolph, rougher dwellings to Washington) written down so it can be
disagreed with.

**The parcel authors no coordinates, and that is the durable half.** The three earlier infill
parcels each hand-wrote their own eastings and northings, because the plat module did not exist
when they were written. `tools/generate_block_infill.py` reads every metre off the committed lot
polygons of the K7 grid: the recipe says which family stands on which lot, whether it fronts the
street or the alley, and how far back. The defect class K7 exposed — seven buildings standing in
the middle of the road, put there by a recipe that had never asked where the road was — is now
retired by construction rather than by a gate catching it afterwards. The gate still runs: the
generator tests every footprint against its own lot lines, the platted corridors, every other
footprint in the dataset, the heightfield and the archetype, before it writes a file.

**A table this project had been carrying and never reading.** `family_bands_ft` in the building
inventory has bands for 21 of the programme's 35 families. The other 14 — **H1, H2, H3, C4,
T1-T3, W5, F3, F4, I1-I3, M1** — had none, so the earlier generators could only build the
families somebody had separately retyped into Python, while the schedule went on apportioning H1
and H2 to blocks. `1835_family_archetype_crosswalk.json` has held the footprint band, storey
count, eave height and placeholder archetype for **all 35** the whole time, and agrees with
`family_bands_ft` on every one of the 21 they share. The generator reads the crosswalk. **H1 and
H2 stand for the first time**, and no band is retyped anywhere.

**One number was moved to fit an archetype, and it is written down.** The A3 privy's authored
eave band runs 6-7 ft and its bottom is below what the outbuilding archetype needs to carry its
own door plus a header — refused by name at 1.891 m. The sample is now drawn from the part of the
authored band the archetype can build (2.07 m, beside phase one's privies at 2.05), and a family
whose whole band sits under that floor fails loudly rather than being quietly raised out of its
typology.

**And a command that quietly destroyed a night's Blender work, found by running it.**
`generators/inferred_placeholder.py` builds the flagged placeholder massing for a new anonymous
record. Its `--check` path has stood aside since 2026-08-13 for any asset the canonical bake has
superseded — `kind: generated` in the manifest — for the stated reason that demanding the
placeholder bytes back would forbid the upgrade the bake exists to perform. **Its BUILD path did
not.** Run once for ten new records, it also rewrote the 128 already-baked ones: 113 KB of
canonical archetype geometry down to a 4.9 KB flagged box each, with their manifest entries
stamped back to `kind: placeholder` so nothing downstream could tell the difference. It reproduces
on a clean `dev` checkout, so it is not a local accident.

**Every gate stayed green through it**, which is the part worth keeping. A placeholder that
matches its record is precisely what the gates check for, so 128 buildings collapsing to boxes is
a state the whole suite regards as correct — and the published smoke passed against it, 204 and
201 assertions, before anyone noticed. What caught it was reading a `git status` that had 461
files in it when the parcel touched ten. The build path now asks the same question the check path
asks and reports `built 10 … 128 superseded by a canonical bake`; the asymmetry between a check
and the build it checks was the whole defect. The four gate runs above were then re-run from
scratch against the restored bake.

**What did NOT ship, stated plainly: the households.** T-A2 as written also called for household
records. Adopting these ten roofs means restating the occupation census — the household generator
gates the census and the households against each other in both directions — and that census is
the population layer's weakest joint, derived from five in-dataset calibrations rather than
cited. Re-arguing it as a side effect of a block parcel would be exactly the kind of silent
re-decision this project refuses. **The ten roofs are unoccupied**, no household names them, and
the work is queued as **ROADMAP T-A2h**. No human figure is drawn (L1), unchanged.

## New 2026-08-14 — 232 roofs stand of 665, and only 105 of the rest have anywhere to go

**T-A1.** The 665-roof programme has been subtracted from for the first time. The target was
authored in `data/reconstruction/1835_building_inventory.json` on 2026-08-11 and never moved
against what was built; the family crosswalk still called **617 roofs remaining** while
**232** were standing, a figure wrong by more than a third of the programme, and the next
block parcel was going to schedule against it. The remainder is now DERIVED —
`tools/reconcile_665.py` → `data/reconstruction/1835_665_roof_programme.json`, re-derived by
`tools/check.sh` like the plat grid and the liberties. A ledger about a town that grows most
nights cannot be a number somebody typed.

**242 records are 232 physical roofs.** Twelve records are a drawbridge, three bridges, two
piers, a palisade, a parade ground, a garrison garden, an open livestock pound, a courthouse
the production chronology puts in the autumn and a hotel still a construction shell — the
physical-roof
reconciliation credits them with no roof, which is what it is for. One record is two cabins
and the ledger counts the low reading. By district: **South 100, West 41, North 81, Fort 10**
against targets of 370 / 135 / 150 / 10. **433 remain.**

**The number that changes what lane 2 does is 105.** The plat module reaches 19 blocks
holding 152 lots. At the reviewed phase-1 parcel's own density — one principal roof per lot,
ancillary at the programme's own 154:511 — those blocks have **105 roofs of headroom**, and
seven of them, the whole Lake Street belt, are already at or over it. The other **328 roofs
have no modelled ground to stand on**: 20 in `blk_south_water_market` and
`blk_south_water_clinton`, which the plat module refuses because South Water's committed
centreline stops 24 m and 878 m short of them; 35 held by the West recipe's own gate at local
E −700 m; and 273 in ground with no committed street control at all — east of State, south of
Washington, west of Clinton, and the entire North Division, which the grid covers by not a
single block. **The 665-roof programme is coverage-bound, not recipe-bound.** Lane 2 has
roughly ten block parcels in it before § S9 street control and the terrain extensions are the
only thing left to do.

**Six family targets are already exceeded, by nine roofs, and that is reported rather than
hidden.** C1 stores, I2 and T2, W1, W4 and W5 all carry more roofs than the 2026-08-11 target
allows, every one of them evidence the research placed after the target was written. A
documented roof is not removable, so the nine come out of the invented family with the most
slack (D4). The same rule runs inside each district against the group matrix — North holds
three institutional roofs and two warehouses more than its share, all of them attested.

**What this does not do.** It builds nothing and moves nothing: every count here is a
function of records that were already committed. The per-block family mix is an
apportionment of the district's remainder, not a claim that any block held those families —
it exists so the schedule adds up, and the block parcels that consume it grade every value
they emit at the invented tier as they always have. Two authored files were corrected where
they stated something untrue about what has been built: the West parcel's status
(`reviewed_recipe_not_rendered`, when 20 of its 55 roofs stand), the roof reconciliation's
status (`planned`, when it is done and this ledger reads it), the North recipe's "remaining
90 roofs" (69 after reconciliation), and the crosswalk's superseded 617.

## The rendering program is live, and overnight work no longer ships to production

**2026-08-14.** Two things changed on the owner's instruction, and together they set what
tonight's loop does.

`docs/RENDERING.md` is **ACTIVE** (reviewed and merged, PR #106). The W track and the G0
critic harness are buildable now; the H (`walk-hd`) and N (native engine) tracks and every
remaining `OWNER DECISION` stay gated exactly as written. The approved KTX-Software install
landed on the bake runner, which unblocks W2's textures — note what it fixes: `bake.sh` asks
for `--texture-compress ktx2` only when the `ktx` binary is present, because gltf-transform
aborts the *whole* optimize when it is absent, meshopt included.

This app is now on a **two-tier `dev` → `main` pipeline** (`docs/PIPELINE.md`), the two-tier
form of the fleet pilot in `kevinrhaas/jobtracker.polecat.live`. Steward parcels and the
nightly bake branch off `dev` and PR into `dev`; merging there publishes only the integration
preview at **`/custom/chicago/4d/dev/walk/?year=1835`** — noindex, banner-marked,
`build.json` reporting `tier: dev`. **Production moves only when the owner dispatches
`chicago-4d-promote-to-prod.yml`.** Promotion is gated; deploy is not, and never will be.

Two defects are recorded rather than fixed, both pinned by gates so they cannot grow:
**79 of 742,581 terrain vertices face downward** (0.011 %, isolated, no visible artefact —
ROADMAP T-BUG2, distinct from the black wedge that was fixed today), and **the river edge
flickers when flying** (ROADMAP R-BUG1, almost certainly depth-buffer fighting between the
water plane and the ground crossing it, owned by the R-W5 parcel). *R-BUG1 was closed
2026-08-16 — the guess in that sentence was right about the fight and wrong about the owner:
it was the camera's near plane, not the water material. See the top of this file.*

## The second block repeated the shape, and refused one of its roofs

**2026-08-14.** `blk_randolph_dearborn` — the easternmost block the plat module reaches on the
Randolph tier — carries **nine of the ten roofs the schedule dealt it**. Standing roofs
**242 → 251**, remaining **423 → 414**, 86 of them on ground the project has coverage for. The
geometry half of T-A3 was a recipe entry and nothing else, which is exactly what T-A2 said it
would be. The two things worth reading are what the repeat exposed.

**The tenth roof was civic, and it is deferred rather than built.** I3 resolves through the
`fort_structure` placeholder, and every building kind that archetype offers is a garrison word —
quarters, barracks, blockhouse, magazine, guard, sutler, artillery. Massing an anonymous town
civic building through it would have stood a garrison building 750 m from the fort. The crosswalk
had already written the condition on its own entry: the family *"spans unlike functions; they must
reconcile to named public records before selecting construction"*. So the generator now refuses
I1, I2 and I3 **by name**, quoting the committed sentence each refusal enforces, and a roof the
schedule dealt but the parcel did not build must be named in the recipe with its reasoning — a
gate that bites in both directions, so a family cannot be quietly dropped and a deferral cannot
be used to hide one. The distinction being drawn: an anonymous *dwelling* is a count-unit toward
a documented aggregate; an anonymous *public building* asserts that an institution stood here and
left no record, and this town's public buildings are few enough to be listed. **One anonymous I2
still stands in the North Division** from a parcel written before any of this, massed as a generic
frame block; it is recorded in L93 rather than removed, and it is not a precedent that extends.
ROADMAP **T-I3** now owns the research the refusal is waiting on.

**A latent defect from the first block, caught by the second, on a two-centimetre margin.**
`lot_frame()` chose a lot's alley edge as the edge nearest the alley's CENTROID — which sits at
the block's centre, so on an END lot the side lot line running back toward it is nearly as close
as the alley edge. Measured on this block: **38.93 m against 38.95 m**, and two of its four end
lots picked the side line, framing a building broadside to its own street and over the
neighbouring lot. **What reported it was the lot-margin gate at 1.44 m against a 1.5 m bound** —
a millimetre-scale complaint about a ninety-degree error, which is the part to remember. Measuring
to the alley strip separates the same two edges by 0.2 m and 26.3 m, and a structural check now
rides with it (front and rear are the same length to within the plat's skew; a 20 % disagreement
means one is a side line). **`blk_randolph_wells` cleared the old tie by 1.3 m in 37, so nothing
T-A2 committed moves** — it was one block's proportions away from the same failure, and it had
been green.

Tonight's loop is expected to produce **one parcel per run from two lanes that cannot
collide** (`docs/ROADMAP.md` → "THE OVERNIGHT LANES"): lane 1 RENDERING touches renderer and
tool files, lane 2 TOWN COMPLETION touches data only. **R-G0** (the critic harness), **T-A1**
(the 665-roof reconciliation) and the first two blocks off the reconciled schedule (**T-A2**,
**T-A3**) are all in, so the NEXT UP picks are **R-W1** (light) and **R-W4** (atmosphere) in
lane 1; **T-A4…** (one open block per run, now adopting in the same run) and **T-I3** (the
civic roofs T-A3 refused — research, not massing) in lane 2. **T-A2h** is in too. Today's
count is **261 structure records — 251 physical roofs of a 665 target — 154 households, 190
persons**. Everything arrives as a PR into `dev` and waits there.


Honest state of the project. Things that are unverified stay labeled unverified; a gate that
was skipped is recorded as skipped. Updated in the same commit as the work it describes.

**Last updated:** 2026-08-14 · **Phase:** S0, S1 (datum), S2-partial (terrain + river at the
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

## The critic baseline — 2026-08-14

**RENDERING G0.1 is in and G0.2's numeric half with it.** `tools/critic_shots.mjs` stands at
eleven fixed stations — the eight scene anchors from `data/scenes/1835.json`, driven by the
walkthrough's own `goTo` so the rig cannot drift from the viewpoints a visitor is offered,
plus three re-established prairie-sweep stands — at both release viewports, with the animation
clock held from before the render loop's second tick and the DOM chrome hidden.
`tools/critic_metrics.mjs` reads the PNGs with no dependencies at all, which means the same
code can measure a reference photograph and one of our frames. **That has never been true
here before**, and it is the reason the numbers below are worth recording.

**Read these as a baseline, not as a scoreboard.** Four things have to be said before the
tables, or they will be quoted wrongly:

1. **They are not comparable to the 2026-08-10 prairie sweep's figures.** That harness was
   never committed and neither were its station coordinates, so both the code and the camera
   positions are new. Where a §5 target was set from the sweep's implementation, the target
   needs re-anchoring by measuring a reference photograph through THIS code — which is now a
   one-line job and is not yet done.
2. **The measurement conventions are the harness's own** and are stated in the head of
   `tools/critic_metrics.mjs`: what counts as sky, how the land/sky line is found, the band
   the horizon timber is looked for in, and how a crown pixel is identified. They are fixed so
   that two rounds are comparable; they are not claims about 1835.
3. **Flower load is only meaningful at the open-prairie stations.** In a frame with streets,
   walls and roofs in it the denominator is not vegetation.
4. **The crown metrics need a crown.** `from_above` reports them because the harness reports
   everything, but 1,142 crown pixels in an aerial frame is not a canopy measurement.

Both baseline runs were **11/11 byte-identical between two separate browser processes** at
both viewports, and every station's pitch matched its declaration.

**desktop 1280×800**

| station | timber all | timber centre | crown fine | crown G−B | decile L | literal black px | RMS far/mid/near | flower load | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|
| `sauganash` | 0.637 | 0.666 | 0.579 | 44.9 | 5.76 | 0 | 10.4 / 7.5 / 0.8 | 0.0301 | 65 / 332,455 |
| `sauganash_wing` | 0.493 | 0.475 | 0.566 | 17.4 | 1.73 | 61 | 11.8 / 7.0 / 0.9 | 0.0383 | 66 / 376,563 |
| `lake_market` | 0.518 | 0.588 | 0.550 | 24.6 | 3 | 0 | 12.0 / 5.8 / 1.1 | 0.0327 | 78 / 484,554 |
| `first_post_office` | 0.847 | 0.937 | 0.552 | 12.2 | 5.35 | 11015 | 9.7 / 8.8 / 9.9 | 0.0004 | 66 / 393,698 |
| `forks` | 0.739 | 0.784 | 0.725 | 35.1 | 25.58 | 0 | 10.0 / 7.1 / 11.4 | 0.0013 | 87 / 596,618 |
| `green_tree` | 0.731 | 0.735 | 0.670 | 20.3 | 30.88 | 0 | 12.9 / 5.3 / 0.9 | 0.0017 | 91 / 553,498 |
| `south_water` **†** | 0.889 | 0.903 | 1.004 | 27.4 | 2.95 | 0 | 17.0 / 26.7 / 30.1 | 0.0575 | 85 / 570,718 |
| `from_above` | 0.212 | 0.180 | 0.830 | 0.2 | 28.24 | 0 | 3.8 / 6.7 / 9.7 | 0.0019 | 67 / 433,090 |
| `prairie_south` | 0.364 | 0.340 | 0.682 | 27.8 | 3.27 | 2315 | 14.8 / 5.0 / 8.7 | 0.0031 | 73 / 512,018 |
| `prairie_west` | 0.832 | 0.850 | 0.629 | 24.1 | 13.67 | 0 | 14.4 / 21.8 / 27.7 | 0.0012 | 97 / 618,686 |
| `river_bank` | 0.641 | 0.719 | 0.740 | 47.9 | 0.93 | 12063 | 13.2 / 23.9 / 29.9 | 0.0022 | 56 / 371,691 |

**mobile 390×780**

| station | timber all | timber centre | crown fine | crown G−B | decile L | literal black px | RMS far/mid/near | flower load | draws / triangles |
|---|---|---|---|---|---|---|---|---|---|
| `sauganash` | 0.756 | 0.823 | 0.572 | 26.3 | 19.49 | 0 | 13.5 / 1.6 / 0.3 | 0.0042 | 62 / 330,283 |
| `sauganash_wing` | 0.667 | 0.592 | 0.625 | 22.5 | 18.78 | 0 | 13.4 / 1.6 / 0.4 | 0.0092 | 63 / 323,946 |
| `lake_market` | 0.697 | 0.719 | 0.597 | 15.9 | 15.21 | 0 | 13.3 / 2.0 / 0.4 | 0.0177 | 66 / 377,012 |
| `first_post_office` | 0.919 | 0.989 | 0.541 | 21.1 | 5.26 | 1763 | 14.7 / 9.4 / 0.4 | 0.0001 | 60 / 386,536 |
| `forks` | 0.749 | 0.731 | 1.337 | 37.5 | 23.42 | 0 | 11.6 / 11.8 / 10.6 | 0 | 82 / 573,840 |
| `green_tree` | 0.767 | 0.746 | 0.740 | 23.6 | 39.46 | 0 | 6.2 / 1.2 / 0.5 | 0.0002 | 88 / 537,659 |
| `south_water` **†** | 0.836 | 0.811 | 0.755 | 35.9 | 7.54 | 0 | 24.1 / 33.9 / 25.1 | 0.0128 | 83 / 550,065 |
| `from_above` | 0.156 | 0.192 | 0.774 | 4.2 | 25.33 | 0 | 6.3 / 11.9 / 10.5 | 0.0012 | 61 / 377,201 |
| `prairie_south` | 0.467 | 0.492 | 0.612 | 30.8 | 13.76 | 267 | 10.3 / 12.9 / 8.1 | 0.0018 | 71 / 476,074 |
| `prairie_west` | 0.679 | 0.696 | 0.772 | 24.1 | 10.65 | 0 | 21.0 / 30.8 / 19.6 | 0.0003 | 94 / 605,366 |
| `river_bank` | 0.713 | 0.773 | 0.814 | 40.3 | 2.77 | 2154 | 21.9 / 33.2 / 6.0 | 0.0004 | 49 / 365,353 |

**† `south_water` here is the RETIRED stand — local `(260, -95)`, "South Water Street, looking
east", which stood 101 m south of the centreline of the street it is named for and framed a field.**
T-V2 (#135) moved the anchor on 2026-08-15 to `(329.8, 7.0)`, the Wells Street corner, and every
`south_water` figure shot from 2026-08-16 onwards measures that stand instead. **The two are not
comparable and neither is a correction of the other — they are two places.** Both stands were
re-shot on one build on 2026-08-23 so the move can be read separately from the town's growth; see
*Re-shot 2026-08-23 — the `south_water` baseline row measures a stand that no longer exists* at the
top of this file. No other station in these tables moved; `newberry_dole_wharf` (T-0041) and
`north_branch_bridge_deck` (T-0001) were added to the scene afterwards and have no row here at all,
so the rig now stands at **thirteen** stations against this table's eleven.

**What the baseline says, against the RENDERING §5 targets.**

- **Horizon timber coverage is short of 90 % nearly everywhere** — 0.21 to 0.89 desktop, best
  at `first_post_office` (0.847) and worst looking down at the town from the air. § 1 item 5
  stands, and R-W4 owns it.
- **Shadows still clip to literal black.** 12,063 pure `(0,0,0)` pixels at `river_bank`,
  11,015 at `first_post_office`, 2,315 at `prairie_south` on desktop, and the darkest decile
  runs as low as **L 0.93** against the § 5 floor of **L ≥ 14**. § 1 item 7 stands, and R-W1
  owns it.
- **Sunlit crowns are no longer blue.** G−B is positive at every station (+0.2 to +47.9), well
  clear of the ≥ +10 target at nine of eleven, where the sweep measured −19 to −26. The colour
  bugs fixed on 2026-08-11 are the reason; this is the first measurement that says so.
- **Grain still collapses with depth, but not uniformly** — `sauganash` reads 10.4 / 7.5 / 0.8
  far/mid/near on desktop, `river_bank` 13.2 / 23.9 / 29.9. The stations that look down a
  street or across water hold their grain; the ones looking over open sward lose it. § 1 item
  4 stands.
- **Flower load at the prairie stations is 0.0031 and 0.0012** against the honest 4–6 %
  target. ~~Two orders of magnitude short~~ — **the gap is 18× smaller than that, and this
  bullet was wrong (R-W4c(a), 2026-08-15).** Those are the *recipe's* figures and the recipe
  misses 94.5 % of the bloom at `prairie_west`, counting 69.7 % of the pixels a flower painted
  as the plant it is being compared against. Measured by subtraction, the bloom is **0.0219 /
  0.0187 / 0.0076** at `prairie_west` / `prairie_south` / `river_bank`. The recipe figures are
  kept because the 2026-08-14 baseline is on them.
- **Draw calls exceed the ≤ 80 budget at four stations** — `prairie_west` 97 desktop / 94
  mobile, `green_tree` 91/88, `forks` 87/82, `south_water` 85/83. **This is new information,
  not a new fault**: the budget has only ever been measured at the spawn station, where it
  passes at 65/62, so nobody had stood anywhere else with the counter running. Recorded in
  ROADMAP against R-W5, which owns the draw-call work.

**What is NOT in this baseline, stated plainly.** The 8-axis rubric score G0.2 also asks for is
**not run**. The protocol requires a critic that did not write the code under review, and the
run that built the harness cannot be that critic without making the score meaningless. It is
parcelled as ROADMAP **R-G1** and the baseline is incomplete until it lands.

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
| **Smoke** | **PASS 2026-08-14** — `tools/check.sh` green, and `node tools/smoke_renderer.mjs` green at both release viewports in all four combinations the gate asks for: source tree **204 mobile / 201 desktop**, published mirror **204 / 201**, zero page errors throughout, with the town at 261 records. Run as four separate foreground commands because a full pass exceeds ten minutes. The history below is the record of how those assertions were earned. **PASS 2026-08-13, and for the first time against the files that actually ship.** `tools/check.sh` is green, and `node tools/smoke_renderer.mjs` passes **361 assertions** at both release viewports (390x780 and 1280x800) with zero page errors — run twice, once against the source tree and once with `--published` against the mirror. **The second run is the one that matters and it did not exist until now.** A sidecar's `gltf/<name>.glb` resolves to the UNCOMPRESSED masters in the source tree and to the meshopt + quantised derivatives on the site, so nothing that ran had ever loaded a compressed asset — and a renderer bug that only exists in the quantised path collapsed all 242 structures to 2 m boxes on the live site for several days, through two attempted fixes, with the gate fully green the whole time. The size assertion was also measuring the TALLEST building in the scene, which passes with one correct building and 241 broken ones; it now measures every structure against its own record, including its documented wall height. Reintroducing the fault fails the new checks by name on all 242. `tools/bake.sh` runs the published smoke after publish. Draw calls and triangles at the spawn station: **59 / 332,455** desktop, inside the 80 / 1,000,000 Full-detail budget. The two halves still run as separate foreground commands, because a full pass exceeds ten minutes. |
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
      prairie. ~~Measured flower load: planting 12.91 %, virgin remnant 1.79–5.54 %. The honest
      target is **4–6 %, not 13.89 %**.~~ **THE CORRECTION WAS RIGHT AND ITS NUMBERS ARE
      WITHDRAWN, 2026-08-15 by R-W4c(b1).** Neither clause survives checking. **No never-plowed
      remnant photograph is committed to this repository and no source record describes one** —
      the phrase occurs once in `data/sources/`, inside the record of the planting, citing
      nothing — so the 1.79–5.54 % half is unsourced. And 12.91 % does not reproduce: the
      committed recipe reads **5.54 %** on that frame, 7.02 % on its nearest quarter and 25.82 %
      with its two tests reordered. **There is therefore no 4–6 % target**, and this file must
      not be read as setting one. `node tools/measure_bloom_target.mjs` prints all of it;
      ROADMAP § R-W4c(b1) carries the reasoning and the three routes out.
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
