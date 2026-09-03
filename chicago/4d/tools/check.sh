#!/usr/bin/env bash
# The per-commit gate. Seconds, no Blender, runs in every agent sandbox.
#
# A gate that takes four minutes gets skipped, so this one deliberately does not
# build geometry. Content builds live in tools/bake.sh and run on demand.
#
#   tools/check.sh            the gate
#   tools/check.sh --strict   warnings are errors (used before a release)
set -uo pipefail
cd "$(dirname "$0")/.."

STRICT=""
[ "${1:-}" = "--strict" ] && STRICT="--strict"

FAILED=0
step() {
  local label="$1"; shift
  printf '\n\033[1m== %s\033[0m\n' "$label"
  if "$@"; then
    return 0
  else
    FAILED=1
    printf '\033[31m   ^ %s failed\033[0m\n' "$label"
    return 1
  fi
}

step "dataset (schema, provenance, date gates, licenses, staleness, publish)" \
  python3 tools/validate.py --all $STRICT

step "validator self-tests" \
  python3 tools/test_validate.py

# A book's page numbers are its locators, and for Hubbard's autobiography they are DERIVED:
# the committed text is the Internet Archive's djvu OCR, which carries no page breaks at all,
# so the leaf boundaries are carried onto it from the deposited scan. A derivation that is not
# gated drifts, and this one is cheap — it reads committed files only and needs no poppler.
step "book page indexes still match the text they index" \
  python3 tools/build_book_page_index.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/build_book_page_index.py --self-test

# Runs early and costs milliseconds, because the fault it catches is cheap to
# make and expensive to ship: on 2026-08-24 three conflict-marker lines rode a
# merge into docs/LIBERTIES.md, compiled into data/liberties.json, published to
# the mirror and PROMOTED TO PRODUCTION, where a visitor opening L180 or L181
# read `<<<<<<< HEAD` in the Evidence panel. Every structural gate passed it:
# the liberties gate asks whether the markdown and the compiled JSON agree, and
# they agreed perfectly — both carried the same garbage.
step "no committed file carries a conflict marker" \
  python3 tools/test_no_conflict_markers.py

step "…and its own assertions still fire when broken" \
  python3 tools/test_no_conflict_markers.py --self-test

# Anonymous reconstruction infill is authored as a compact parcel recipe, then
# expanded to ordinary one-file-per-structure records and visibly flagged GLBs.
# Both derivations must stay reproducible without Blender.
step "inferred infill records match the 665-roof programme" \
  python3 tools/generate_inferred_infill.py --check

step "North Division initial parcel matches its reviewed recipe" \
  python3 tools/generate_north_infill.py --check

step "West Division approaches parcel matches its recipe" \
  python3 tools/generate_west_infill.py --check

# The block parcels are the same shape of derivation with one difference worth the
# extra step: they author no coordinates at all. Every metre comes from the committed
# lot polygons, so a hand-nudged building would show up here as drift rather than as a
# plausible-looking number sitting beside a derived grid.
step "platted block parcels match their recipe and the committed lots" \
  python3 tools/generate_block_infill.py --check

# The inferred-household layer (K1 phase two) is the same shape of thing: an
# authored recipe — an occupation census, a roof-adoption table and a placement
# list — expanded into households, occupancy blocks and structure records. It also
# re-runs its own placement gates, so a centre that drifts onto another building,
# onto water or off the modelled ground fails here rather than in a bake.
step "inferred households, adoptions and their buildings match the programme" \
  python3 tools/synthesize_resident_research.py --check

step "inferred placeholder GLBs match their records" \
  python3 generators/inferred_placeholder.py --check

# The clapboard stock, both halves of it. The named deal re-derives its own 24 records
# (T-0049) — that half was never gated, so a hand-edited board width would have sat in
# the tree looking exactly like a dealt one. The recipes deal the other 131 and their
# own --check above holds those values byte for byte, but a recipe that stopped dealing
# ALTOGETHER would pass every one of those checks: a record with no siding_exposure_m is
# a perfectly well-formed record. It just puts 131 walls back on one course, invisibly,
# which is the defect T-0112 closed. So this asks the town-wide question instead.
step "every clapboard wall's stock re-derives from its deal" \
  python3 tools/deal_siding_stock.py --check

# The platted block and lot grid is generated from the Thompson module and the
# committed street lines, never traced off the 1834 sheets. Re-deriving it here is
# what keeps it a derivation: a hand-nudged block face would otherwise sit in the
# repo looking exactly like a surveyed one.
step "the platted block and lot grid re-derives from the module" \
  python3 tools/generate_plat_lots.py --check

# And the grid's own refusals still fire. The one that matters is the youngest: four
# crossings can be found and still describe no block, because two committed centrelines
# can converge to less than a corridor apart before they get there. Measured 2026-08-29
# by T-0183 on the closure the owner ruled for at Market x South Water, which emitted a
# 4,411 m2 bowtie with a plausible depth rather than refusing.
step "…and a block whose rows have crossed is refused rather than emitted" \
  python3 tools/generate_plat_lots.py --self-test

# The dooryard garden pickets are the first record on the enclosure layer whose evidence
# is a TREATMENT and not a place — the Kinzie-view plate shows picket-fenced garden plots
# and no source puts a garden on any lot in this town. So the answer to "why this lot" is
# a RULE, and a rule that is not re-derived is a list somebody typed: this re-runs it
# against the committed lots, footprints, functions and households (ROADMAP K5 (a), T-0052).
step "the dooryard garden pickets re-derive from the rule that chose their lots" \
  python3 tools/generate_dooryard_pickets.py --check

# The lot-line yard fences are the same shape of claim at town scale: the owner asked for
# more fences, image 12 of his brief shows an 1830s town where every property is enclosed,
# and no source names a fence on any lot in Chicago. So WHICH lots and WHICH fence is a
# rule again — the committed plat for the lines, the committed footprints for where the
# yard begins, and the street records' own traffic classes for the type — re-derived here
# so kilometres of fence stay auditable rather than several hundred typed numbers (T-0068).
step "the lot-line yard fences re-derive from the rule that chose their lots and types" \
  python3 tools/generate_lot_line_fences.py --check

# The dooryard plantings are the same shape one layer greener: the owner's brief and its
# image 12 attest a TREATMENT — trees and bushes kept close around the houses — and no
# source counts or places any particular house's stems. So which house keeps what is a
# RULE over the committed dwellings, streets, fences and ground, re-derived here so the
# 125 stems stay auditable rather than 125 numbers somebody typed (T-0074).
step "the dooryard plantings re-derive from the rule that dealt their stems" \
  python3 tools/generate_dooryard_plantings.py --check

# And the planted rows are the same shape again, on the one flora treatment this project
# has in WORDS rather than in pictures: Wau-Bun states "a broad green space was inclosed
# between it and the river, and shaded by a row of Lombardy poplars", at a house that is
# excluded from this scene. Seven committed plates draw that row and five agree on four
# stems at 0.195 of their own height apart; not one of them shows a poplar anywhere else
# in Chicago. So the treatment is the source's, the count and the rhythm are measured,
# and WHICH GROUND GETS ONE is a rule over the committed dwellings — re-derived here so
# the twelve stems and the refusal beside them stay auditable (T-0117).
step "the planted poplar rows re-derive from the rule that chose their greens" \
  python3 tools/generate_planted_rows.py --check

# The business signboards are the same shape of claim one layer over: exactly one record
# in this dataset ATTESTS a sign, and the boards on the other two dozen frontages are a
# reconstruction chosen by a rule about trades rather than a list of shops somebody liked.
# Re-derived here against the committed sidecars, so the rule stays the answer to "why
# this frontage" (ROADMAP K5 (b), T-0039).
step "the business signboards re-derive from the rule that chose their frontages" \
  python3 tools/generate_business_signboards.py --check

# The yard goods are the third record of this shape and the first whose evidence is an
# ORDINANCE: the village corporation legislated in November 1833 about timber, stone,
# brick, boxes and barrels stacked in the streets, which attests the treatment and not one
# location. So "which frontage gets goods" is a rule again, re-derived here against the
# committed sidecars and the wagon-yard perimeter (ROADMAP K5 (c), T-0040).
step "the yard goods re-derive from the rule that chose their frontages" \
  python3 tools/generate_yard_goods.py --check

# And the OTHER HALF of that ordinance, which the goods record refused in writing:
# timber, stone and brick are building material on a lot that is going up, not a
# trader's stock on his own frontage. The rule's load-bearing clause is that the
# structure record has to STATE the construction state itself — a date test would read
# a first-attestation year as a groundbreaking and deal stacks of brick to buildings
# that had stood for a year — so exactly one lot in this scene qualifies, and this
# re-derives which one and where the piles stand (T-0057).
step "the building material re-derives from the rule that chose the lots" \
  python3 tools/generate_lot_building_material.py --check

# The fort apron is the same shape of claim about GROUND rather than about things standing
# on it: both committed Fort Dearborn plates draw the ground round the stockade as bare
# trodden earth, no source states a foot of it, and the render grew prairie to the pickets.
# So "how far out is it bare" is a rule, derived from the palisade's own committed footprint
# and placement, and re-derived here — along with the four assertions the rule has to be true
# for, which fail this gate rather than a reviewer's attention (T-0097).
step "the fort apron re-derives from the palisade it is measured off" \
  python3 tools/generate_fort_apron.py --check

# And the layer above that ground: the wood p4_0 draws outside the same walls (T-0098). Same
# shape again — the plate attests a tree mass and places nothing, so which ground carries a
# stem is a rule off the palisade's own footprint and its apron's own width, re-derived here.
# The rule also picks the SPECIES rather than a preference: of the zone's three recorded
# trees only one is banded low enough to carry the crown height measured off the plate, and
# a re-banded zone record must therefore fail this gate rather than quietly plant a
# cottonwood that would tower over the fort the plate draws it level with.
step "the fort wood re-derives from the palisade and the apron it stands off" \
  python3 tools/generate_fort_trees.py --check

# T-0008 took every chimney in the town off the ROOF material — R-W2a finding 1, a stack
# painted whatever weathering condition its own roof was dealt — and nothing measured the
# result, so it left ten stacks behind for four months: `fort_structure` was excluded
# deliberately (1816, before the town had a brick-yard) and the exclusion outlived the
# reason for it, which T-0137 answered off the fort's own attested brick. This gate is what
# stops that class of miss recurring, and it is stated on the BYTES rather than on any
# generator: a stack has to clear the roof to draw at all, so a building whose record counts
# a chimney and whose highest geometry IS the roof material has its stack inside the roof's
# own primitive. It reads the committed masters' accessor bounds and decodes no mesh.
step "no stack in the town is painted the colour of the roof it passes through" \
  python3 tools/measure_stack_fabric.py --gate --quiet

# Its neighbour, on the same accessor bounds and the same principle (T-0333). The Town of
# Chicago's by-law of 5 August 1835 section 18 — chicago_democrat_1835_08_19#c005 — carries
# every stove pipe or chimney "at least eighteen inches above the roof" under a five-dollar
# penalty, which is the first documented DIMENSIONAL constraint this project holds on
# anything above a roof line. Every stack in the town already clears it; this is the ratchet
# that stops one dropping back under. It does NOT decide which buildings the by-law reaches:
# section 22's corporation limits are T-0334's and are not drawn yet, and nothing here is
# conformed to a rule that may not bind it, because nothing has to move.
step "every stack is carried eighteen inches above its roof, as the by-law of 5 August 1835 requires" \
  python3 tools/measure_stack_ordinance.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_stack_ordinance.py --self-test

# The river wharves are the fourth record of this shape and the first whose rule
# reads a record's OWN attribute rather than a trade table: a sidecar standing on
# the scene date whose `dock` is true and graded attested or inferred. Two
# records in this town qualify and both state their dock in the same sentence of
# the same dossier; every other river frontage is refused by the same clause. The
# outline is derived from the traced bank, the committed footprint and the
# committed heightfield, so a re-traced bank or a moved warehouse must move the
# wharf with it or fail here (ROADMAP K5 (e), T-0041).
step "the river wharves re-derive from the records that state a dock" \
  python3 tools/generate_river_wharves.py --check

# ROADMAP K5 (e) also asked for "a river-wharf mode of pier_crib", so that a town
# assembled from GLBs alone would carry its docks; T-0059 was that clause and was
# WITHDRAWN on 2026-08-27 on the three readings this holds. Not on an opinion about
# wharves: on the count of renderers that could read such a GLB (one, and it draws
# the wharves already), on the count of drawn-at-load layers that owe a generator
# half (nine of nine, so the debt is general and the wharf is not special), and on
# what each route into the bake re-stales. The last of those cuts BOTH ways and the
# gate states it either way — a mode inside pier_crib.py costs two meshes, which is
# cheap, while a new archetype edits build.py's registry and costs the town. The
# reading is gated rather than remembered because every figure in it is a thing the
# tree can change underneath the decision: a second renderer, a tenth layer, or the
# first drawn layer to grow a generator each fail here and send somebody back to the
# ticket.
step "the case T-0059 was withdrawn on still holds" \
  python3 tools/measure_generator_half.py --gate --quiet

# The frontage works are the fifth record of this shape and the first derived from
# a building AND a street at once: where a plank walk may lie is decided by the
# travelled track's own half-width out of data/streets/1835.json, not by the wall
# alone. Re-derived here for the same reason as the four above — "which wall gets a
# walk" is a rule, and a rule that is not re-run is a rule nobody is keeping (T-0082).
step "the frontage works re-derive from the rule that chose their walls" \
  python3 tools/generate_frontage_works.py --check

# AND THE HALF OF THAT RULE NO RECORD EXERCISES. A cross street bounds a block on
# its EAST and WEST faces; every street this record carries today bounds one on the
# north and south. T-0192 enumerated all four and made every ordering in that
# generator axis-aware, then measured the seven cross streets over all three
# scene-detail ceilings and left them out — so the east/west path ships with an
# empty covered tuple and the re-derivation above cannot touch it. This drives it
# over all seven, in hundredths of a second, so it is code somebody is keeping
# rather than code waiting to rot until the frame budget is won back.
step "the street edge's cross-street faces enumerate as the plat says" \
  python3 tools/test_frontage_faces.py

step "…and those assertions still fire when the enumeration is broken" \
  python3 tools/test_frontage_faces.py --self-test

# The 665-roof programme's remainder is a function of what has been built, and the town
# grows most nights. Left as an authored number it goes stale silently — the crosswalk
# called 617 roofs remaining while 232 were standing — and the next block parcel schedules
# against a figure that is wrong by a third of the programme.
step "the 665-roof programme reconciles with the town that stands" \
  python3 tools/reconcile_665.py --check

# T-0233, and the question the recipes cannot answer by being read: does a party-line
# run stand on the lots it was dealt? It does not — 8 of the 19 dealt lots carry none of
# their own run's roofs — and the ticket ruled that a RESERVATION rather than a defect,
# because `reconcile_665`'s free-lot arithmetic is derived from committed footprints and
# has never read a recipe's deal, so nothing is withheld from the programme by it. What
# was wrong was only that nobody could see it, which is why the measurement is wired in
# here instead of left as a command somebody remembers. The gate itself is the ceiling
# T-0079 established — `ROW_UNITS_PER_LOT` units per dealt lot, every roof already
# standing on those lots counted against it — and it passes today, so it is cheap.
step "no party-line run carries more roofs than the frontage it was dealt" \
  python3 tools/measure_frontage_entitlement.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_frontage_entitlement.py --self-test

# T-0163. The plat grid is the cartesian product of its east-west rows and north-south
# columns, so it proposes blocks that never existed, and it reports every refusal the same
# way — as a distance. A distance cannot tell "the centreline has not been carried there
# yet" from "these two streets never met", and both were being scheduled as headroom
# waiting on the same owed trace. This carries each refused block's named street toward it
# and samples the run against the committed heightfield: a run that crosses water is two
# banks, not a gap. It is what keeps the classification in the programme honest, so a block
# cannot quietly go back to promising roofs that no street control can deliver.
step "a refused block is short of control, or was never a block" \
  python3 tools/measure_block_gating.py --check

# T-0026, and the same fault one district wide. The programme's South balance — 120 roofs,
# the largest of the three gated ones — named STREET CONTROL as its blocker and sent the
# next parcel to go and carry a centreline. Measured, the blocker is the ground: the box
# ends at local N -400 m, INSIDE Washington Street's platted corridor, every north-south
# column of the south plat has its committed line cut at that same edge, and Madison — the
# plat's south boundary — is 125 m further south. The plat's last tier, six blocks and 48
# lots, is 100 % unmodelled. Two assertions: no committed platted block stands off the
# modelled ground (absolute, and it is what fires the day control is carried south without
# the terrain following), and the programme's stated southern coverage is the measured one.
step "no platted block stands off the modelled ground, and the south's blocker is the measured one" \
  python3 tools/measure_southern_ground.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_southern_ground.py --self-test

# The two numbers on the FRONT screen (T-0036): buildings standing and people housed.
# Both are reads of the roof programme and the residents layer, and the most visible
# possible place to carry a stale number is the panel a visitor sees before anything
# else. Re-derived here so a run that builds ten roofs and forgets to regenerate the
# census fails at the commit rather than shipping a town that says it is smaller than
# it is. Also refuses a household whose `lives_at` names a structure the scene does not
# carry, which would silently drop people out of the count.
step "the gate's town census re-derives from the roofs and the residents" \
  python3 tools/town_census.py --check

# Ground the town held in common is not building ground, and every gate this project
# had asked whether a building CLEARED the roadway, stood inside its own lot lines and
# missed its neighbours — never whether the ground it stood on was for sale. Two
# documented rental cottages spent five days standing on the public square for exactly
# that reason (ROADMAP T-A16). The reservation is authored data; this runs it.
step "nothing unpermitted stands on reserved ground" \
  python3 tools/measure_reserved_ground.py --gate

# The same question outside the plat, where it is bigger: 26.5 % of the modelled land
# above the water surface is the United States Reservation or the sand bar across the
# river mouth, neither was ever open to a private builder, and neither was refused by
# anything (ROADMAP T-E2). This also carries the under-coverage assertion — the polygons
# are resolved from the traces, so a terrain extension that outruns them fails here.
step "nothing unpermitted stands on refused ground, and the refusal still reaches it" \
  python3 tools/measure_no_build_ground.py --gate

# T-0134. The plate the Dearborn reach was built from draws warehouses on BOTH banks and
# only the north one stands. The south side was refused on a single spot reading taken by
# hand — "the corridor reaches to within about 1.7 m of the waterline" — and the whole bank
# was left empty on it. This is that refusal as a command, at every relief tolerance it
# could turn on: beside the platted street not one position takes the smallest footprint
# family F1 allows. It fails if a fit ever APPEARS, because a fit is the question re-opening
# and not a number to bank — which is the assertion that fires the day the terrain is
# extended, the plat is re-derived or the waterline is re-traced.
step "the south bank at the Dearborn reach still carries no ground outside its own street" \
  python3 tools/measure_south_bank_ground.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_south_bank_ground.py --self-test

# The terrain spec defers four in-town water features — the slough, the public-square
# pond, the Frog Pond and the Wells Street marsh — under one shared phrase, "existence
# documented, geometry conjectural". Existence is a claim about a PLACE and the scene is
# a date, and not one of the four had ever been asked where it stands on 1835-07-01
# (ROADMAP T-E5(a)). They do not answer alike: the slough is dated by the bridge this
# project already stands over it, the Frog Pond by a newspaper one year late, and the
# pond is argued in both directions by the same document. This holds the correspondence
# in both directions, so a fifth feature cannot be deferred undated and a dating entry
# cannot outlive the deferral it grades.
step "every deferred in-town water feature is dated against the scene" \
  python3 tools/measure_intown_water.py --gate

# The fifth of those features is no longer deferred, and the thing that most obviously
# depends on it had nobody watching it. The Slough Log Bridge is the only built thing in
# this dataset that exists to answer the terrain, and for two months it stood over dry
# prairie because zone 14 was not carved (T-0109). T-0005 carved it and T-0118 put its
# last reach square under this deck — both aimed elsewhere, neither gated here, and a
# swale line nudged a metre west would put the crossing back over solid ground with every
# other check still green. This joins the bridge's placement to the ground beneath it.
step "the slough crossing spans open water, and nothing else stands in the cut" \
  python3 tools/measure_slough_crossing.py --gate

# And the feature that crossing's own drain runs OUT of. "How much of the public
# square was wet" (T-0027) presumes a fraction can be read off the block, and it
# cannot: the terrain draws the square at the South Division plain's +2.9 ft with
# an inch and a half of relief — inside the spec's own declared micro-relief
# noise — so there is no basin there and a wet fraction read off it would be a
# read of the noise seed. The answer is a DEPTH: the dossier's own bed for zone 15
# is +1.0 to +2.0 ft, which the committed ground stands 0.84 to 1.96 ft above. So
# the square is planted as the flora dossier names it — ZONE 3, by name, the
# heading of the section that authors sedge meadow — and NO WATER IS DRAWN. This
# holds all of that: zero water, absolutely; no landform, so the zero stays a
# statement about the model; the sedge polygon still the committed plat's ring;
# and the drain still heading at the block it is named for.
step "no water stands on the public square, and its sward is the one the dossier names" \
  python3 tools/measure_public_square.py --gate

# Every generator asks whether the roof it is about to place stands in a platted street,
# and no invented roof has ever been allowed to. Nothing had ever asked it of the records
# a PERSON placed, so the answer arrived as anecdotes — three buildings in T-A9, two more
# in T-A12 — and the distribution behind them was never measured (ROADMAP K30). It is 29
# records, all of them documented and none of them generated. This holds that: a ratchet
# on the 29, and an ABSOLUTE assertion that no generated roof laps a corridor, which the
# placement gate already guarantees and which is therefore enforceable at zero.
step "no building has newly been drawn standing in a platted street" \
  python3 tools/measure_corridor_intrusion.py --gate --quiet

# The absolute half of that gate rests on ONE reading: which evidence layer a record
# belongs to. It used to be read off the record's ID PREFIX, and `physicians_office`
# carries no prefix while being a product of the inferred-household programme — so a
# generated record was scored against the ratchet, which may be re-baselined, instead of
# against the absolute, which may not (T-0221). The reading moved onto the record itself
# in plat_occupancy.layer_of_record; this puts a generated roof in a roadway, in memory,
# under both readings and checks which one the gate catches.
step "…and its absolute assertion still fires when a generated roof is put in a street" \
  python3 tools/measure_corridor_intrusion.py --self-test

# Two generators build party-line rows onto the committed block faces and each asserts
# that ITS OWN run stands on one line; neither could see the other. The Lake face of
# blk_lake_clark is built by both and carried two lines 0.70 m apart, ten metres apart
# along the face and so not yet reading as a step (T-0104). This is the gate beside the
# two: it takes the face line out of the committed plat, projects every front wall onto
# it, and refuses a face carrying more than one — absolutely, with no ratchet, because
# after T-0104 the number is zero. It also closes party walls from BOTH sides, which is
# the case neither run-local gate can reach when the other half belongs to another
# generator.
# T-0226. North Water Street's line was a hand-drawn schematic that ran 477.4 m of its
# 843.3 m inside the water mask, so the renderer drew no roadway at all across that
# reach — and NOTHING SAW IT, because the panel-accounting gate asks whether every panel
# with a DRY centreline reached the ribbon and every one of them did. A street whose
# centreline is wet is invisible to that question by construction. The line is now
# derived from the committed north bank, and this is the gate that keeps it derived: it
# re-runs the derivation and refuses a committed line that is not the one it produces,
# so a bank that moves under the street is a red build rather than a silent hole.
step "north water street is still the line its own derivation produces, and still dry" \
  python3 tools/derive_north_water.py --gate

# T-0372. "Still dry" was a weaker question than it sounded: the gate above asks whether
# any BEND stands in water, and a street can hug a bank for a hundred metres without
# putting a vertex in it. The derivation now carries a clearance rule with two tiers —
# the open reach owes the half module less the fit's own give, and the two ends, where
# the street meets the water on purpose (it stops at the fork and crosses on a deck),
# owe five metres. This is the proof the rule refuses each tier, and that the two
# exemptions are load-bearing rather than a way of saying nothing.
step "…and its own assertions still fire when broken" \
  python3 tools/derive_north_water.py --self-test

step "a block face carries one street line, across every generator that builds on it" \
  python3 tools/measure_street_line.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_street_line.py --self-test

# One line per face says nothing about what the wall on it is MADE of. L99 and L100 both
# worried that the schedule "will keep dealing cabins to commercial frontage", and the
# block recipes quietly acted on it: every log dwelling the five South Water blocks were
# dealt was put on the Lake face, leaving 15 invented buildings on South Water's line and
# not one of them log — against a documented record for the same line that carries Hogan's
# log store, and against the only picture of that row, which draws it as log AND frame
# shoulder to shoulder. T-0022 measured that, refused the re-apportionment K29 proposed,
# and moved the arrangement instead. This holds it: a principal street's INVENTED frontage
# may not be more uniform in construction than the documented record of the same street.
# A floor of one, absolute — the plate gives no ratio, so a share would be a number
# somebody chose.
step "no principal frontage is more uniform than the record it reconstructs" \
  python3 tools/measure_frontage_fabric.py --gate --quiet

step "…and its own assertion still fires when broken" \
  python3 tools/measure_frontage_fabric.py --self-test

# What a frontage is MADE OF was T-0022; what a non-dwelling standing on it is FOR is
# T-0024, legacy K32. The face rule ranks dwellings — best to the better street, meanest
# to the back one — and T-A15, dealt the first store any block parcel had had to place,
# extended the ranking to cover it rather than leaving the placement unreasoned. That
# extension was an agent's invention about 1835 commerce and was opened for the next
# commercial family to follow or refute. It is refused as a RULE and replaced by one that
# can be read off the committed record instead of argued: not one of the 31 documented
# stores, warehouses and workshops in this town stands on a light street, and every
# documented store standing on a platted street stands on its line. Two absolute
# assertions over the roofs the block parcels place, no ratchet, both green the day they
# were written — which is the only kind of absolute worth adding.
step "no block parcel stands a non-dwelling where the documented record puts none" \
  python3 tools/measure_face_rule.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_face_rule.py --self-test

# A dwelling nobody named is a count-unit toward a documented aggregate; a PUBLIC
# building nobody named is the claim that an institution stood here and left no record
# at all. ROADMAP T-I3 enumerated them: on 1835-07-01 the town's public buildings with a
# roof are three, all three are committed named records, and every other public function
# in Chicago was carried on inside a private building. generate_block_infill.py has
# refused the institutional families by name since L93, but only for the blocks — the
# North, West and phase-one parcels ran before it existed and nothing had ever asked the
# committed records. This asks all of them: absolute zero for I1 and I3, a ratchet at the
# one anonymous I2 that L93 records rather than deletes.
#
# T-0032 CLOSED THE OTHER HALF, which had been open since T-I3: the I3 target was SIX and
# the town's civic roofs are three, so three slots counted nothing and the schedule went on
# dealing them to blocks where every generator refused them. The step now settles every
# civic candidate against the committed dataset — a roof that stood, a building that came
# later, a function that never had a building of its own — and holds the target and the
# institutional district row to that ledger. It is the shape of fault this project has been
# bitten by twice: the court-house stood in the scene for four days while another file
# already credited it no roof, because nothing read the two together.
step "no anonymous roof claims to be a public building, and the civic target is the ledger" \
  python3 tools/measure_institutional_claims.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_institutional_claims.py --self-test

# THE OTHER NINE ROWS, which T-0032 found were cross-checked against nothing (T-0211).
# The matrix carries the same aggregate two ways that were authored independently — ten
# group rows and four division columns — and reconcile_665.py asserted only that the
# families sum to their group and the districts to the total. Nothing read a group's split
# BY DIVISION, which is precisely the pair T-0032 found disagreeing.
#
# The I3 repair does not generalise and this does not attempt it: a row above what stands
# is the ordinary, correct case for nine of these ten rows, because an anonymous dwelling
# is a legitimate count-unit toward a documented aggregate. What is asserted is the weaker
# pair that still catches the fault — the matrix must add up in BOTH directions, and a
# division standing OVER one of its group rows must say so. The second is a ratchet on a
# real residual: the North Division stands seven roofs above its rows (six freight, one
# the L93 school), reconcile_665.py clamped the negative away, and the seven slots it
# sheds to pay for them come out of the North's ordinary dwellings where nobody could see
# the transfer. Both figures are now in the programme document.
step "the group rows add up by division too, and every division over one declares it" \
  python3 tools/measure_group_district_rows.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_group_district_rows.py --self-test

# Uniformity is a claim, and no source makes it. 138 of the 218 anonymous records say
# in their own footprint note that the rectangle was sampled inside the family's
# authored band; this holds them to it, and prints the census of what still is not —
# 36 stamped massings and 40 eaves outside the band their own note cites, all of them
# on parcels whose meshes are canonical bakes (ROADMAP T-V1(b), K25). Read the census;
# a pass here is not "the town is a distribution".
step "the anonymous massings that claim a sampled band have one" \
  python3 tools/measure_massing_variety.py --gate

# The same sentence, asked of every reconstructed record and every value the crosswalk
# authors a testable band for. "Type-level choice within the D3 band" is the entire
# defence for inventing a building, so a value outside the band it cites is a note that
# is wrong about its own source — 98 of them, on 80 of 249 records (ROADMAP K25). The
# strict assertion FAILS today and is meant to: --strict runs it. What runs here is the
# ratchet, because the repair needs a bake and a permanently red dev gate would block
# every unrelated parcel behind it. A new offender, or a committed one whose value
# moved, fails. The fault may shrink and may not grow.
step "no reconstructed value is newly outside the band its own note cites" \
  python3 tools/measure_band_claims.py --gate --quiet

# The value NO record states and every visitor sees: the RIDGE the sampled pitch and
# the sampled footprint make together (T-0145). The crosswalk authors a `ridge_ft` band
# beside every eave band and nothing had ever read that column, so a parcel could repair
# its pitches into their band and push its roofs out of theirs — the fault moved one
# field over. This models the ridge from the archetype's own roof arithmetic, checks
# that model against the ridge the committed GLB actually carries, and ratchets the
# residual the same way the band-claims gate does. The residual is real and mostly
# structural: for several families no pitch inside the authored pitch band reaches the
# authored ridge band at the footprint the family authors.
step "no reconstructed roof's ridge is newly outside its family band" \
  python3 tools/measure_ridge_band.py

# ...and the same question asked of the SPECIFICATION rather than of a roof (T-0148).
# The gate above holds the eave a record happens to carry fixed, which made its residual
# read as a conflict between two committed bands — "no pitch reaches the ridge band at
# the footprint the family authors". The eave is not fixed: it is the second value the
# crosswalk authors as a band and the samplers draw from, so a ridge band is reachable
# from a (footprint, eave) PAIR. Swept that way, every family's four claims — footprint,
# eave, pitch, ridge — are satisfiable at every footprint in its own band, so nothing in
# the specification has to give way and the residual above is all repair. This holds that
# true: a crosswalk edit that authors a family which cannot be built to its own ridge band
# fails here, at the specification, instead of four runs later as a roof nobody can raise.
step "every family's footprint, eave, pitch and ridge bands are satisfiable at once" \
  python3 tools/measure_ridge_reach.py --quiet

# ...and the residual THAT gate printed as three NOTE lines, joined to what the
# generators actually deal (T-0179). Nine families are offered a SHED by their roof line
# and four cannot reach their own ridge band as one, because a shed's plane climbs the
# whole span where a gable climbs half. Nothing was broken, because no parcel dealt those
# four a shed — but which families get a shed was decided FIVE times, once inside each
# parcel, and the five had already drifted over A5. The rule now lives in
# tools/roof_form.py alone, the refusal is written on the card a visitor opens, and the
# step above holds the two together: a family dealt a form its own bands cannot carry, a
# record that does not carry its family's refusal, or a parcel that grows its own copy of
# the shed set all fail here.
step "…and its own assertions still fire when broken" \
  python3 tools/measure_ridge_reach.py --self-test

# And the question the two gates above cannot ask, because they read what LANDED: is
# every family the 665-roof schedule may deal to a platted block buildable at every
# size its own band allows? A family comes up rarely — there are two H1s and two H2s in
# the whole parcel — so a band whose tail the archetype refuses looks fine until the
# schedule deals into the tail and the run dies. This deals each family four hundred
# instances through the generator's own sampling and asks the archetype to build each
# one. It found H2 unbuildable over the top third of its authored eave band, D6 over
# the bottom of its own, a rounding step that put a pitch outside the band it was drawn
# from, and W2 fatal to the generator on the day it is first dealt (T-0142).
# T-0172 took the sweep off the block generator alone and onto all FOUR anonymous
# parcels — west, South Division infill and the inferred households deal the same
# families through the same archetypes and had never been asked. None of them refuses a
# deal; every one of them authors form values as per-family CONSTANTS whose note cites
# the family band, and 31 of those constants sit outside the band they cite. The gate is
# therefore a RATCHET from here: a refusal never passes, and an off-band claim passes
# only while tools/family_deal_baseline.json names it with the reason it stands.
step "every family every parcel may deal builds, and every band claim is named" \
  python3 tools/measure_family_deal.py --gate

# AGENTS.md puts one constraint above the work — the final removal of the Potawatomi
# from Chicago is August 1835, inside this project's first target year — and gives it
# one mechanism: review_required on any record blocks a scene from being marked
# released. Nothing had ever measured what that sentence covers (ROADMAP K34). It
# covered the buildings: the seven flagged households blocked nothing, and were safe
# only by the coincidence that each lives or works in a building that is flagged too.
# One record said in its own prose that it carried the flag and never had. Four
# absolute assertions and no ratchet, because this is a commitment rather than a fault
# being paid down.
step "the standing constraint reaches every record that claims it" \
  python3 tools/measure_review_constraint.py --gate

# The same shape of question asked of AGENTS.md rule 6 — a check_required source
# "may be cited in text but must not have assets derived from it", and
# docs/PROVENANCE.md says the validator enforces it. What the validator compares
# is two fields of the same source record: rights_status against the source's own
# asset_use label, so it can only fire once an author has written the violation
# down, and no source in this dataset ever has (ROADMAP K41). This asks the town
# instead, using the read-sets the archetypes and the terrain generator already
# declare. The population is banked by name: it may shrink and may not grow, and
# a repair has to be recorded with --update in the commit that made it.
step "no unresolved source is newly built into the town" \
  python3 tools/measure_rights_derivation.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_rights_derivation.py --self-test

# K41's residual, and the question one layer out: the buildings and the ground
# declare which of their figures reaches a vertex, and data/flora and data/fauna
# never had. 100 figures across the two layers, 38 of them read by the renderer
# and 58 by nothing at all — including the whole of data/fauna, which no file
# under renderers/ opens and publish.sh does not copy to the site (ROADMAP K42).
# The map is Python and the reader is JavaScript, so every declaration is scanned
# against the renderer sources with the comments stripped, in both directions.
step "every flora and fauna figure is declared read or banked unread" \
  python3 tools/measure_layer_reads.py --gate

step "…and its own assertions still fire when broken" \
  python3 tools/measure_layer_reads.py --self-test

# The same question one level in, and it is a different question: the read-set
# above says a FIGURE is read if any renderer source reads it, and no reader in
# this project receives every record. flora.js takes five roles and fifteen
# forms; trees.js takes two roles, five forms and FOUR of the manifest's ten
# zones. So 339 of the 1,880 (record, figure) pairs the map calls read reach
# nothing, six records reach no reader at all — four of them the lakeshore's
# woody scrub, which its own zone prose describes to a visitor — and three
# recorded July inflorescences draw no flower (ROADMAP K44). Every cohort is
# scanned out of the renderer rather than restated here, and all three
# populations are banked exactly: they may not grow, and a repair has to be
# recorded with --update in the commit that made it.
step "every flora record reaches the reader its figures are read by" \
  python3 tools/measure_flora_reach.py --gate

step "…and its own assertions still fire when broken" \
  python3 tools/measure_flora_reach.py --self-test

# The step after that one, and it is a different question again. K44 measured
# ROUTING — which reader is handed the record — and named the repair its finding
# implies: "add z08_lakeshore to TIMBER_ZONES and the four dune records are
# drawn". Measured, that repair draws nothing (ROADMAP K45(a)). TIMBER_ZONES is a
# SPECIES table: trees.js takes height, crown, foliage and density out of those
# files and then places from a hand-written COMMUNITIES mix, never from a zone's
# extent — z07_bur_oak_savanna's declared box is 4.4 km outside the modelled
# field and its oaks are drawn regardless. So a routed record whose species is in
# no mix is drawn nowhere, which the American sycamore has been all along, and
# the woody planter is a fixed 632 m square inside a field it reaches 27 % of.
# Both populations are banked and neither may worsen.
step "every routed woody record can be selected by something that places it" \
  python3 tools/measure_planting_reach.py --gate

step "…and its own assertions still fire when broken" \
  python3 tools/measure_planting_reach.py --self-test

# The population BOTH woody gates were blind to. smoke_renderer.mjs asserts that
# "woody vegetation never occupies the river mask" off trees.group.userData.stations
# — written only inside the near-field planter's 632 m square — and the flora half
# walks instance matrices on a lattice centred on the camera. FAR_TIMBER is neither:
# five bodies of timber authored as polylines and drawn as a horizon silhouette, and
# nothing had ever asked those polylines where they stand. One of them, the belt whose
# own note says it follows South Water Street, was 39 of 39 samples over the main stem
# and 3.347 m under its surface — the line of trees across the channel in the owner's
# screenshot (ROADMAP R-BUG5). T-0031 put it back on land (0 of 136) and the step below
# keeps it there. The renderer refuses water absolutely now; this holds the table, and
# scans the clip so it cannot quietly come back out.
step "no body of far timber stands in the river" \
  python3 tools/measure_far_timber.py --gate

step "…and its own assertions still fire when broken" \
  python3 tools/measure_far_timber.py --self-test

# T-0031 / R-BUG5(b). The belt that stood in the channel is back on land, on a line
# DERIVED from the committed `south_water` centreline rather than authored beside
# it — the owner's route 1, with the side of the street recorded as L191. The stub
# it replaced was drawn on a Wells Street 66.7 m east of the committed centreline,
# and that error is half of why it ended up in the river, so the belt is re-derived
# here on every commit. Move South Water Street and this fails until the belt moves
# with it.
step "the South Water timber belt re-derives from the street it is cut from" \
  python3 tools/derive_timber_belt.py --check

# T-0094 was filed saying the fort's pickets are flat-topped. They are not, and
# have not been since the archetype was written: the committed master carries
# 0.312 m of sharpened head on every one of its 768 posts, 8.4 % of the picket,
# and a visitor at the north wall sees the sawtooth. The claim had never been
# measured, which is how it reached a ticket. This holds the property so it cannot
# be re-filed off a screenshot, and so a flattened archetype or a decimation pass
# that ate the apexes would be named here rather than found by eye.
#
# THE PLATE HALF OF THAT FILE DOES NOT GATE, deliberately. p4_0 is a tier-5
# retrospective lithograph; it may inform a value and it may refute a claim made
# about itself, and it may not hold a build red. Run the file without --gate for
# the plate reading, which also needs Pillow and skips without it.
step "the fort's stockade is still pointed" \
  python3 tools/measure_picket_plate.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_picket_plate.py --self-test

# NOTE ON THE TWO FORT STEPS THAT FOLLOW, because they look inconsistent and are
# not. T-0094's plate half deliberately does NOT gate: it asks whether a tier-5
# retrospective lithograph supports a claim about the MODEL, and a lithograph may
# not hold a build red. T-0095's does gate, and its live assertion is a different
# question — the third one, which reads the RECORD and fires the day someone gives
# a corner work a height, a roof or a lantern on that plate's authority. Its other
# two assertions read a committed image that cannot change, so the only thing they
# can catch is the detector moving under them, which is what its baseline is for.
# One asks the plate about the town; the other asks the town about the plate.

# Fort Dearborn's gates are built SHUT on purpose — the archetype's own words: a
# fort with its gates standing open makes a claim about the hour of the day, and
# the garrison is attested for the scene date. Both of them stood a quarter open.
# One leaf of each pair was placed from a midpoint that collapsed onto its own
# jamb, so 0.90 m of a 3.6 m gateway was daylight straight through the wall and
# 0.90 m of leaf lay across the pickets outside the frame — in the committed GLB,
# so in the bytes a visitor downloaded. This reads the shipped mesh rather than
# re-deriving the placement, because the derivation was the fault (T-0095).
step "Fort Dearborn's documented gates are shut" \
  python3 tools/measure_fort_gates.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_fort_gates.py --self-test

# T-0095 was filed saying p4_0 "draws the corner works RISING ABOVE the curtain
# with their own pyramidal roofs and small lanterns". It does not. It raises two
# such works and both stand over the MIDDLE of the wall, at 0.435 and 0.521 of the
# drawn run; the one angle the plate shows unoccluded is drawn plain, and the other
# is behind a tree. This is the second Fort Dearborn parcel in two days seeded by a
# plate read with the eye (T-0094 was the first), so the refutation is held by a
# measurement rather than by a paragraph — and its third assertion fires the day
# the record is built to the misreading anyway.
step "p4_0 raises no work at either angle of the fort it draws" \
  python3 tools/measure_fort_works_plate.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_fort_works_plate.py --self-test

# T-0197 audited the rest of that table, because three of its eight rows had been
# struck as wrong in a week and rows 1, 2 and 6 had never been measured at all —
# while already carrying TWO built ways on the reservation. Row 2 is the first row
# of that table to survive measurement: p4_0 draws one bare corridor, it meets the
# wall at the gate, it runs west, and it reaches the shore. Row 1's "both plates"
# is struck (p4_1 draws no way at the fort, on a detector that finds the way it
# draws elsewhere on the same bank). Row 6's flagstaff stands at 0.495 of the wall
# — over the gate, not in the parade where exclusions.json puts the FIRST fort's.
# Two of the three assertions here ask the TOWN about the plates, which is why this
# one gates where T-0094's plate half does not: they fire the day fort_bank_track
# is swung back east, or either way's geometry_confidence is promoted on the
# strength of a tier-5 lithograph.
step "the ways the fort plates draw are still the ways the town was built to" \
  python3 tools/measure_fort_ways_plate.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_fort_ways_plate.py --self-test

# The datum must remain the output of its committed ground control, never a
# hand-edited number. Skips (exit 0) when pyproj is not installed.
step "datum re-derivation" \
  python3 tools/rederive_datum.py

# The liberties the walkthrough shows must still be the ones the markdown
# states. LIBERTIES.md is append-only and is the source of truth; data/
# liberties.json is derived and committed so the site needs no build step, which
# only holds up if drift is a gate failure rather than a discovery.
#
# Since T-0054 it also asks WHICH SECTION each entry is in, from two independent
# statements — the heading it sits under and the `**Resolved:**` line in its own
# text — because `resolved` is the section validate.py stops checking. It used to
# be the last section in a document whose one rule is that liberties are
# APPENDED, so 23 entries landed in the exemption by doing what they were told,
# and the drift check above could not see it: the markdown and the JSON agreed,
# both reading the fault the same way (the T-0207 shape).
step "liberties derived from docs/LIBERTIES.md" \
  python3 tools/compile_liberties.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/compile_liberties.py --self-test

# The renderer reads the sidecars and never the dataset, which only keeps the
# walkthrough and the archive together if a record edited without a recompile is
# a failure here rather than a discovery on the deployed site.
step "sidecars derived from data/" \
  python3 tools/compile_scene.py --all --check

# Every building card offers a link to the write-up behind the building, and on
# the deployed site all 332 of them were a 404: publish.sh leaves docs/ out of
# the payload by design, so the link resolved in the source tree and nowhere a
# visitor stands (ROADMAP K26). The link is now absolute and this asserts both
# halves of it — that every linked dossier is a file here, and that the base the
# renderer composes with still points at this app inside its repository.
step "every dossier link a card offers resolves" \
  python3 tools/check_dossier_links.py

# Renderer JS must at least parse. The repo's deploy workflow does the same thing
# for site/, and a syntax error there is a blank page for everyone.
check_js() {
  local n=0 bad=0
  while IFS= read -r -d '' f; do
    n=$((n + 1))
    node --input-type=module --check < "$f" 2>/dev/null || {
      echo "   parse error: $f"; bad=1
    }
  done < <(find renderers -name '*.js' -not -path '*/vendor/*' -print0 2>/dev/null)
  echo "   $n module(s) parsed"
  return $bad
}
step "renderer modules parse" check_js

# The ground the town is ANCHORED to and the ground it is DRAWN as, compared on
# the committed bytes. `generators/terrain_gen.py` refuses to export a mesh more
# than 30 mm from the heightfield — inside a Blender run this gate cannot make,
# so nothing re-checked the committed master afterwards, and R-BUG3c was a 306 mm
# disagreement nobody could see. This asserts the master and REPORTS the shipped
# derivative, which is quantised by the publish step and conformed at load; the
# surface actually drawn is asserted by tools/smoke_renderer.mjs.
step "the ground mesh still meets the heightfield the walker samples" \
  node tools/measure_terrain_fit.mjs --gate

# The OTHER two axes, which conformGroundToField() cannot repair — it reads a
# height back off the field at a vertex's shipped (E, N), so a vertex the
# quantiser moved in plan holds the right height for the wrong place, and on the
# east banks' 60-90 % slopes that cost 77 mm where the road ribbon has 22.
# generators/terrain_gen.py now derives the skirt margin so the publish step's
# POSITION rung divides the terrain grid exactly, which puts every ground vertex
# on a rung and takes the displacement to zero. This asserts the zero on the
# bytes rather than the arithmetic on the generator's side of the bake (T-0152).
step "the shipped ground stands where the master does, and inside the road lift" \
  node tools/measure_terrain_horizontal.mjs --gate

# The shrub archetype's own bounds, which are the only two numbers in it the
# RESEARCH owns: the clump keeps the half-width its record states, and a leaf
# spray stays a mass of leaves rather than shrinking towards a single leaf it
# cannot draw at two triangles. K57 measured that "hold the total plate area and
# refine the grain" trades the first for coverage, so the bound is a gate rather
# than a paragraph. The third assertion is a ratchet on the coverage itself.
step "the shrub keeps its recorded width and its shell is not see-through" \
  node tools/measure_spray_grain.mjs --gate --quiet

# The changelog contract, on every run rather than only when somebody remembers
# it. AGENTS.md has always told an agent to run this by hand before merging, and
# on 2026-08-13 the file was corrupted BY A MERGE — `.gitattributes` merges it
# with `merge=union`, so both parents were green and the union of them was not.
# A hand-run check cannot cover a file that a merge rewrites; this one can.
step "changelog contract" \
  node tools/check-changelog.mjs

# The ticket queue: the operational "what next" the owner ordered on 2026-08-17
# after his own requests went untraceable in the ROADMAP. Duplicate ids, queue
# drift, a stale BOARD, a block with no stated question — all merge-refusing.
step "ticket queue" \
  node tools/ticket.mjs check

# The link between the two: the shipped derivative against the master it was
# compressed from. `--stale` gates data -> master and check_published.mjs gates
# assets/web -> the mirror, and NOTHING gated the step in between, which is the one
# with the moving parts — two gltf-transform passes whose own comments in bake.sh
# record a bug that "collapsed every building to a two-metre box shipped past a fully
# green gate — twice" (ROADMAP K36). Triangles, node identity, the contract's
# attributes and the world bounding box are all answerable from the glTF JSON chunk,
# so this costs a second and no decoder. The material half is a ratchet, and K36(b)
# emptied it: 334 of 334 now, so the next offender is the first entry.
#
# K38 added assertion 8, which is the one that covers the OTHER writers. `assets/web/`
# is written by three scripts and four of their branches copy a master through, and a
# master copied over its own derivative satisfies assertions 1-7 by construction —
# measured, two of them passed the whole of this file. The 93 legitimate passthroughs
# are banked by name and both directions fail. A new placeholder therefore needs
# `--write-baseline` in the commit that adds it: the decision is recorded, not found.
step "the shipped derivative still describes the master's building" \
  python3 tools/measure_web_derivatives.py --gate --quiet

# The gate above has eight assertions and, until K37, nothing had ever watched one
# of them fail — its --self-test breaks each in memory against the real tree and
# was reporting SELF-TEST FAIL on a clean tree because a mutation it could no
# longer apply read as a miss. It costs a second, so run it here rather than
# trusting that someone runs it by hand.
step "…and its own assertions still fire when broken" \
  python3 tools/measure_web_derivatives.py --self-test

# T-0158, and it is the SECOND fault of this exact shape. `build.py --ao` baked
# occlusion that read min 0.000 / max 1.000 in Blender's own buffer and reached the
# GLB as min 0 / max 0 — every one of 262,144 texels — while the run exited 0, the
# GLB grew 4 KB and assets/manifest.json recorded `baked_ao: true`. Under glTF an
# occlusion of 0 means FULLY occluded, so the manifest was asserting good AO on an
# asset whose ambient light was extinguished. Nothing at all read the texture. This
# does, off the exported bytes, with no Blender and no numpy: an asset that carries
# an occlusion texture must carry occlusion, and the manifest must agree with the
# file in both directions. Costs a quarter-second on a town whose 348 masters all
# carry `baked_ao: false` — the moment one does not, it has a reader.
step "a shipped occlusion texture carries occlusion, and the manifest agrees" \
  python3 generators/ao_export.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 generators/ao_export.py --self-test

# Does the site ship what the repository says it ships? R-BUG3c-b (#145) cost
# three parcels because the ground a browser loads was quantised by a publish
# step AFTER the only gate that measured it, and every gate passed because every
# gate compared a render to another render. #145 fixed that instance and left
# the general case open in as many words: "Nothing else in this project measures
# a published artefact against its own source." This is that gate. publish.sh is
# almost entirely `cp`, so the invariant is total — every published file is
# byte-identical to its source unless it is on a declared list that has to name
# what transforms it and which gate measures the SHIPPED form. It found two
# unchecked files on its first run, one of them a build.json two days stale.
# Skipped rather than failed when the mirror is absent, so a fresh checkout that
# has not published yet still gates cleanly.
if [ -d ../../site/chicago/4d ]; then
  step "published mirror matches its source" \
    node tools/check_published.mjs
fi

# …and the one file in that mirror whose SOURCE is rewritten after publish.sh has
# already run. `ticket.mjs done` needs the PR number that only exists once the PR
# is open, which is after the publish, so the documented order left the gate above
# red every single time and a remembered extra publish.sh was what actually held
# it together (T-0154; it broke on T-0153/PR #318). ticket.mjs now carries the file
# to the mirror itself. This asserts BOTH halves in a sandbox — that closing a
# ticket ends green, AND that a mirror somebody else made stale still fails, which
# is the half a fix like this one could quietly destroy.
step "closing a ticket leaves the mirror fresh, and a stale one still fails" \
  node tools/test_ticket_mirror.mjs

# The same trap, one file over (T-0155). changelog.js is published to TWO paths
# check_published compares byte for byte, and stamp-changelog.mjs rewrites the
# source — so a run that stamps AFTER publish.sh was red for following the rules.
# The stamper now carries both mirrors itself. Both halves again: that stamping
# late ends green, AND that a mirror somebody else made stale still fails.
step "stamping the changelog leaves both mirrors fresh, and a stale one still fails" \
  node tools/test_changelog_mirror.mjs

# T-0180. The nightly bake decides whether it produced anything by asking this
# script, so the script's own assertions are the gate on that decision. The two
# it exists to hold are the two that would silently break it: publish.sh stamping
# a THIRD path, and the exclusion widening from "the stamp moved" to "those two
# files moved" — after which a real change to build.json or to the gate page
# would stop opening a PR, which is the same dead signal in the other direction.
step "the bake's content test refuses the stamp and nothing else" \
  python3 tools/bake_content_changed.py --self-test

# The duplicate-id remedy, tested in the only state it ever runs in. `restamp`
# used to find the ticket by FILE (its own comment explains that with two files
# sharing an id, nothing else can tell them apart) and then edit the queue by ID,
# so it rewrote whichever of the two lines the owner had ranked higher — a coin
# toss, and on 2026-08-27 it clobbered a real ticket's line and left a stale one
# behind with every gate green (T-0217). This runs the repair on BOTH orderings of
# the same fixture, because the old code passed one of them by luck.
step "restamp moves the queue line it was handed, not the other one" \
  node tools/test_ticket_restamp.mjs

# The other restamp, and the more dangerous one: `tools/restamp_inputs.py` rewrites
# `assets/manifest.json`'s input hashes without a bake, which is the only honest
# answer to a change in the input-hash RECIPE (T-0164) and would be a silent way to
# bless a stale mesh at any other moment. Its guard is that a SCHEME constant must
# have moved, and a committed tree — where the schemes agree by construction — is
# exactly the negative fixture that proves the guard still holds.
step "restamping the input hashes is refused when no recipe changed" \
  python3 tools/test_restamp_inputs.py

# The integration preview's assembler. It lives at the repo root because the
# deploy workflow does, but nothing else tests it, and it is the only thing that
# marks the preview as a preview — the noindex, the banner, the build stamp. A
# preview that quietly stops saying "DEV PREVIEW" is one screenshot away from
# being reported as a production bug. Skipped rather than failed when the script
# is absent, so a checkout of chicago/4d alone still gates cleanly.
if [ -f ../../.github/chicago-4d-dev-preview.mjs ]; then
  step "dev preview assembles, marked and stamped" \
    node tools/test_dev_preview.mjs
fi

# Every JSON in data/ must be loadable — a stray comma here breaks the whole build
# in a place far from the edit that caused it.
check_json() {
  python3 - <<'PY'
import json, sys
from pathlib import Path
bad = 0
n = 0
for p in sorted(Path("data").rglob("*.json")):
    n += 1
    try:
        json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"   invalid JSON: {p}: {e}")
        bad = 1
print(f"   {n} data file(s) parsed")
sys.exit(bad)
PY
}
# Attested must cite a source, an inference must record what it reasoned from,
# and NOTHING on an invented structure may outrank the invention that put it
# there. That last rule is the one that mattered: without it, 158 buildings that
# never existed graded their wall heights as evidence and rendered solid.
# The invented names, re-derived. Deterministic from each person's id, so a name
# that changed without the pools or the generator changing is a real finding.
step "the reconstructed residents' invented names re-derive" \
  python3 tools/synthesize_resident_research.py --check

# Re-deriving is not the same as being STABLE. The allocator dealt each pool by
# index, so a name was a function of how many people sorted ahead of you and one
# new household rewrote up to 73 of the 113 invented names — a diff in which the
# parcel's real additions could not be found, and in which a name that drifted
# because something was wrong would have been invisible (ROADMAP K20). Nothing
# caught it because --check re-derives the town as it stands and never asks what
# happens when it grows. This asks: it inserts a synthetic household in memory
# and counts who gets renamed.
step "one new household renames only the people it collides with" \
  python3 tools/measure_name_churn.py --gate --probes 8 --quiet

# And the pass that RETIRES an invented name (T-0264): where the newspaper
# register found a documented person for a trade the town had invented a
# household for, the documented man takes the roof. Re-derived here because the
# deal is a derivation and not a list — six refusals shape it, and a candidate
# that quietly stopped being refused would otherwise plant a real man on a roof
# his own record contradicts. `--report` prints the deal and every refusal.
step "the documented residents on reconstructed roofs re-derive from the register" \
  python3 tools/synthesize_resident_research.py --check

# And the pass that ADDS one (T-0376). The register's `new_resident` people are
# the ones this reconstruction does not hold at all; where it can also read a
# trade, that trade is by construction one the occupation census never invented a
# roof for, so the only thing the town can do with the man is mint him. Gated for
# the same reason as the deal above: eight refusals shape the set, and one of
# them quietly ceasing to fire would put a firm, a man at the mouth of the
# St. Joseph, or a second copy of a real resident into the town's people.
# `--report` prints the mint and every refusal with its reason.
step "the minted documented residents re-derive from the register" \
  python3 tools/synthesize_resident_research.py --check

# And the pass that adds the rest of that half (T-0373): the `new_resident` people
# the papers name with NO trade at all. There is no trade to anchor them, so the
# whole pass is a residency test — the corpus must place them inside the town and
# nowhere outside it, a bare "Chicago" must be corroborated by an address, a second
# issue or the committed company they are printed beside, and the name itself must be
# printed clear of the transcription's uncertainty marks. Gated because a refusal
# that quietly stopped firing would mint 'The Blanshard household' out of the letters
# `fG. BL NSHARD`, or seat a steamboat passenger from Green Bay in the town.
# `--report` prints the 4 minted and all 382 refusals with their reasons.
step "the residency-tested residents re-derive from the register" \
  python3 tools/mint_placed_residents.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/mint_placed_residents.py --self-test

# And the pass beside it, on the other half of `new_resident` (T-0378, T-0379). A person
# the register reads ONLY from the post office's lists of uncalled-for letters has no
# trade, so the pass above cannot reach him. It used to take only the names held in more
# than one return and leave the rest to a decision the owner had not made; he made it on
# 2026-08-30 — HOLD ALL OF THEM — and this pass now mints every name its refusals admit,
# which is most of the people in the town. Gated for the same reason and more of it: the
# refusals are the only thing between a post-office list and the town's population, and
# one of them quietly ceasing to fire would now be worth hundreds of records rather than
# one. `--report` prints the mint and every refusal with its reason; `--scale` counts
# what the ruling did to the town on whatever tree it is run against.
step "the minted letter-list residents re-derive from the register" \
  python3 tools/synthesize_resident_research.py --check

# T-0491. The 1840 identity bridges — three adjudicated links from a canonical 1835
# resident to a named head of household in the federal census five years later. The
# contract is that 1840 is LATER EVIDENCE: the 210 census rows are retained whole, a
# canonical link needs an explicit adjudicated person_id and is graded `validated` or
# `provisional`, and no 1840 spouse, child or boarder is minted into an 1835 household
# from a count. `--check` re-derives all of that, and it ran nowhere but its own
# workflow, so PR #670 could add a bridge, leave the manifest counts and the published
# mirror behind it, and merge on a gate that never looked. It looks here now, beside the
# synthesis it shares the ledger with.
step "the 1840 identity bridges re-derive and back-project nothing" \
  python3 tools/apply_census_1840_bridges.py --check

# THE OTHER HALF OF THE SAME QUESTION, and the owner asked it on 2026-09-03: "i see
# lots of research being done ... but there are not outputs or updates to the household
# and resident data". The bridges gate above proves the links the project HAS made are
# honest. It cannot notice the links it never made. On that day census_1840 held 562
# names read off the sheets and a crosswalk of `passes: [], merges: [], refusals: []` —
# every reading ticket green, every output filed, and nothing across. coverage.json
# makes an unread image fail rather than pass quietly; this makes an unruled NAME do
# the same. It is a ratchet, not a target: reading ahead of the bridge is the method,
# so the gap may sit where it sits and may not silently widen.
step "no research domain reads further ahead of the town than its baseline" \
  python3 tools/measure_research_spend.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_research_spend.py --self-test

# T-0442, T-0462, T-0463, T-0478, and T-0479. These reviews sit beside household facts on purpose: a plausible
# biography must stay a candidate until something more than the name bridges it
# to the 1835 record. Re-derive the fixed cohort and its public review payload.
step "the 75-person real-resident research cohort is fixed" \
  python3 tools/select_resident_research_pilot.py --gate

step "the second non-overlapping 75-person research cohort is fixed" \
  python3 tools/select_resident_research_pass_2.py --gate

step "the third non-overlapping 75-person research cohort is fixed" \
  python3 tools/select_resident_research_pass_3.py --gate

step "the fourth non-overlapping 75-person research cohort is fixed" \
  python3 tools/select_resident_research_pass_4.py --gate

step "the fifth non-overlapping 75-person research cohort is fixed" \
  python3 tools/select_resident_research_pass_5.py --gate

# T-0492 fixes cohorts 13, 14 and 15 in one selector, BEFORE their three tickets run,
# so T-0508, T-0509 and T-0510 do not edit this file and the same population frame at
# the same moment in three parallel runs. The frame is 228 named residents carrying no
# research row — measured, not the ticket's estimated 237 — chunked 76/76/76. 225 of
# them are the pilot, pass 2 and pass 3 cohorts, reserved and never researched (T-0511),
# which is why the gate refuses overlap with a completed RESEARCH ROW and not with a
# reservation. docs/RESEARCH/resident-research-pass-13.md carries the arithmetic.
step "the thirteenth research cohort is fixed" \
  python3 tools/select_resident_research_pass_13.py --gate

step "the fourteenth research cohort is fixed" \
  python3 tools/select_resident_research_pass_14.py --gate

step "the fifteenth research cohort is fixed" \
  python3 tools/select_resident_research_pass_15.py --gate

step "all 375 reviewed residents have reproducible research outcomes" \
  python3 tools/compile_resident_research_pilot.py --gate

# …and the ruling's own conditions, which --check cannot see. --check proves the records
# are what the pass derives; this proves the DERIVATION is what the owner permitted —
# every minted person carrying `letter_list_only` and the dated return behind it, and not
# one of them holding a roof, a trade, a second member or a building that names them. The
# failure mode it guards is silent: a later generator that deals roofs by household would
# put seven hundred invented dwellings in the town off a post-office list, and nothing
# about any single record would look wrong.
step "the letter-list cohort is what the owner's ruling permits" \
  python3 tools/mint_letter_list_residents.py --gate

step "…and that gate's own assertions still fire when broken" \
  python3 tools/mint_letter_list_residents.py --self-test

step "the three levels mean what they say" \
  python3 tools/audit_confidence.py --strict

step "data JSON parses" check_json

# Almost every Playwright tool here is a MEASURING instrument, and the rule is
# that a change is measured before it is claimed. Twelve of the sixteen could
# not be pointed at a browser, so on a runner without Playwright's own build
# they died before their first frame — which turns "measured" into "asserted"
# without anyone deciding to (T-0153).
step "every browser-launching tool honours PW_EXECUTABLE" \
  node tools/check_tool_browser.mjs

# The road-legibility gate fires once per STATION while the measurement is per
# BAND, so a band could collapse 55 points inside a passing station and the
# suite would print the same totals before and after. The movement report is
# what makes that visible; this is the report's own self-test, which replays
# R-W1's merge and requires it to name south_water 250-600 m unprompted (T-0016).
step "the road-band movement report names a band that moved" \
  node tools/road_band_movement.mjs --self-test

# T-0100. The street layer graded a ribbon by its surface and its wear and never
# by `geometry_confidence`, so an INVENTED ROUTE under an attested surface would
# have drawn at full confidence. It is degenerate in today's data — every street
# is pinned at `reconstructed` wear already — which is exactly why it needed a
# test rather than an eyeball: nothing on screen can show it either way. The
# test slices the expression out of streets.js instead of copying it, so the
# shipped grade and the tested grade cannot drift apart, and it carries a
# tripwire that fires the day the data makes the fix matter.
step "a street's invented line reaches the picture" \
  node tools/test_street_confidence.mjs

# K49(d) warned for a week that a spatial filter running after the stratified
# deal selects a BIASED set of ranks, and told every later parcel not to use
# `stratum` in a filtered layer on the strength of it. T-0018 refuted that: the
# position-to-rank map is re-keyed per block, so a rule that reads only position
# cannot lean. This runs the refutation's own control pair every time — a filter
# written to read the rank must be caught, a rank-blind one at the same rate must
# not — so the day someone makes the deal rank-correlated, the claim stops being
# refuted here rather than in a census six weeks later. It reads the deal out of
# flora.js rather than keeping a copy, so it fails by name if that file moves.
step "a spatial filter still cannot bias the sward's rank deal" \
  node tools/measure_rank_bias.mjs --self-test

# The smoke's parts get re-cut whenever the town outgrows the ten-minute foreground
# ceiling — four of them in 2026 alone — and docs/SMOKE-BUDGET.md's map of "which
# parts cover which change" is the kind of table that goes quietly wrong the first
# time a renderer module is renamed under it. So the map is not prose: it is a
# structure in tools/smoke_budget.mjs, and this holds it against the tree. It fails
# if a mapped path no longer exists, if a part of the body is covered by no row, if
# `PARTS` in smoke_renderer.mjs has moved out from under it, or if an unmapped path
# ever stops meaning THE WHOLE GATE — which is the property that makes the recipe
# safe to follow (T-0235).
step "the smoke's change-to-parts map still matches the tree" \
  node tools/smoke_budget.mjs --self-test

# The 1833-1835 newspaper corpus is the PAPERS epic's foundation: eighty-six issues
# that the project could not cite until they had a register to resolve against. The
# register is only worth something if it is true, so this asserts the count rather
# than observing it (a silently dropped issue is otherwise invisible), requires dates
# to increase strictly per publication, and re-hashes every derived text file. The
# deposit itself is on `main` and not on `dev` (T-0275), which is why the check knows
# three deposit states and not two: present, absent, and PARTIAL — and partial is
# always red, because that is the state that means damage.
step "the newspaper corpus resolves, and nothing under data/research/ is published" \
  python3 tools/newspaper_corpus.py --check

# T-0492. The newspapers' pipeline is the one that works, and six more domains are about
# to be read in parallel by runs that cannot see each other — the civic lists, the 1830
# and 1840 census, a church register, books and directories. If each invents its own file
# shape, the consolidation re-reads ten dialects and the refusals nobody wrote down have
# to be made again. So the shape is fixed before the sweep starts: a CLOSED kind
# vocabulary, a required reading grade, a coverage declaration where a declared item
# nothing reaches is a hole, an identity crosswalk that declares its refusals as carefully
# as its merges, and — for the two domains whose text this repo commits — the same
# verbatim gate the papers carry, which rebuilds every quote out of the committed lines
# and refuses one that differs by a character. The scaffold is EMPTY on purpose.
step "the research domains hold one shape" \
  python3 tools/research_domains.py --check

# T-0566, T-0569. Norris's 1844 directory arrived as three generated files that no
# gate re-derived: the 2,073 entries, the crosswalk that proposes which of them meet
# the people of 1835, and the layer the panel renders those meetings from. A hand-edit
# to any of them — a match nudged out of "ambiguous", a refusal quietly dropped, a
# trade written into a card — would have shipped unopposed. All three rebuild and diff.
step "Norris's 1844 directory entries re-derive from the committed page text" \
  python3 tools/read_norris_1844.py --check

step "…and the 1835 crosswalk re-derives from those entries" \
  python3 tools/crosswalk_norris_1844.py --check

step "…and the 1844 findings the cards show re-derive from that crosswalk" \
  python3 tools/spend_norris_1844.py --check

# T-0554. The Calumet Club's old-settlers receptions are a source SERIES read out of the
# Tribune's reprints, and the thing that goes wrong with a source like this is silent
# drift: a name hand-tidied, a quote paraphrased, a merge asserted in a file and never
# written onto the record it names. So the rolls are REBUILT from the committed
# transcription and compared, every quote is rebuilt out of the same lines, and every
# merge has to be present on the resident record it claims.
step "the old-settlers rolls rebuild from their committed transcription" \
  python3 tools/old_settlers.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/old_settlers.py --self-test

step "…and its own assertions still fire when broken" \
  python3 tools/research_domains.py --self-test

# T-0557. The Illinois State Archives' land tract sales are the first source this project
# reads that is not about people at all — it is a register of TRANSACTIONS, and the way it
# goes wrong is by being read as a census. A purchase says a man bought ground; only the
# register's own Residence column says where he lived, and it names a county. So the
# reading is rebuilt from the committed deposit and diffed, the grade a row carries has to
# follow from that column rather than from the buying, and the three sections the
# database truncated at its own 150-row ceiling must never appear in the coverage
# declaration — a ceiling recorded as a completed read is the one error here nothing
# downstream could catch.
step "the land tract sales re-derive from their committed deposit" \
  python3 tools/read_land_sales.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/read_land_sales.py --self-test

# T-0571. Fergus's 1843 directory is the earliest complete Chicago directory this project
# can reach, and its two halves are segmented by two different rules — the shouted head of
# a trade card on page 1, the current letter section on pages 2-4 — because the printer set
# them differently and the web transcription this repo holds does not indent a turned line.
# A segmenter that quietly loses forty entries is invisible to every other gate here, so the
# reading is REBUILT from the committed text and compared, and the per-page counts are held
# to what coverage.json declares. The crosswalk is rebuilt the same way: it is a proposal
# that changes no resident record, and a hand-edit of a proposal is how one becomes a fact
# nobody decided.
step "Fergus's 1843 directory rebuilds from its committed text, at the declared counts" \
  python3 tools/read_fergus_1843.py --check

step "…and its crosswalk to the 1835 residents rebuilds too" \
  python3 tools/crosswalk_fergus_1843.py --check

# T-0588. The dating pass over Norris's 1844 firms is a measurement whose ANSWER IS NO —
# no printing this project holds dates any of the 207 firms at or before 1835, so nothing
# was written to the businesses layer. A negative result is the easiest artefact in the
# repository to corrupt: nobody re-reads it, and a hand-edit that promotes one firm to
# "dated 1834" would put a business in the town on nobody's authority. So the whole file
# rebuilds from its four committed inputs and diffs, and the rules it rests on — that the
# sketch route reads the printed quote and never this project's own gloss, that a
# one-surname firm needs an agreeing initial, that a founding year has to be carried by
# founding language — are asserted with cases that fire.
step "Norris's 1844 firms re-derive their dating against 1835" \
  python3 tools/date_norris_1844_businesses.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/date_norris_1844_businesses.py --self-test

# T-0556. An INVENTORY of a website is the one research artefact that rots silently: it
# is a set of judgements about pages nobody will open again, and the only way to notice
# that a section was quietly dropped from it is to go and re-walk the site. So the county
# index page is committed RAW beside the readable cache, and this re-extracts its links
# and refuses an inventory that has no row for one of them — the ticket's acceptance
# ("covers every section the index links, none skipped silently") as an assertion rather
# than as a hope. It also rebuilds every quote the assessment filed in passing out of the
# committed text, because a quote from a website is a quote from something that can change
# under you.
# T-0574. Fergus's list of the deaths of Chicago's old settlers, and the one source this
# project holds that carries AGES AT DEATH — which are birth years, by subtraction this
# project does and the page does not. Two things need holding. The segmenting, because the
# transcription wraps a long entry without indenting the turn and the rule that tells a turn
# from a man is delicate: "Oct. 12, 1877" under O is the tail of Daniel O'Hara's entry, and a
# rule reading the section letter alone made a new man of the month. And the GRADE, because
# an arithmetic birth window that quietly became `documented` would be this project's own
# invention wearing a citation. The gate rebuilds both files out of the committed text, holds
# the count to what coverage.json declares, and refuses a record that claims the scene year
# or grades a derived birth above `inferred`.
step "Fergus's old-settler death notices rebuild from their committed text" \
  python3 tools/read_fergus_obits.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/read_fergus_obits.py --self-test

step "the Genealogy Trails inventory covers every section the county index links" \
  python3 tools/read_genealogytrails.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/read_genealogytrails.py --self-test
# T-0562. The seventh domain, and the one that needs a gate of its own. The Newberry
# Library's genealogical index is a FINDING AID: a card heads a family surname and names
# the book that treats it, and it never places a person anywhere. Its whole failure mode
# is that a surname in it looks like evidence, so the assertion that matters here is the
# last one — the source id may not appear behind a resident, a household or a building.
# The rest holds the reading honest: every `as_read` is rebuilt out of the committed
# card text, the committed text is held to the sha256 the extraction recorded, no record
# may be graded above `transcription_mediated`, and the hand-adjudicated precision sample
# must still be adjudicating cards that are actually in the records.
step "the Newberry index stays a finding aid, and its reading rebuilds from the cards" \
  python3 tools/read_newberry_index.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/read_newberry_index.py --self-test
# T-0590. The reading above is worth nothing until somebody rules on what it offered.
# Volume 1 put up 319 leads and made 0 merges, and a lead nobody has answered reads
# exactly like a lead nobody has looked at. The rulings are derived, not authored, so
# the gate that matters is that the file still re-derives: a hand-edited outcome, a
# lead that stopped being ruled on, or a merge appearing in a finding aid's crosswalk
# all fail here rather than in a spend measure three weeks later.
step "every Newberry lead is ruled on, anchored, and re-derives from the cards" \
  python3 tools/rule_newberry_leads.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/rule_newberry_leads.py --self-test
# T-0572. The 134 Black Hawk War veterans who enrolled AT CHICAGO in 1832. Two
# assertions carry this one. First, the reading is taken from the CACHED PAGE and not
# from the flattened text, because the flattening drops an empty cell and 94 of the 134
# rows leave the Rank cell empty — read from the text alone, `INDIAN` could be the rank
# or the company and nothing on the page would say which. Second, 83 of the 134 names
# carry no surname comma (the French and Potawatomi forms), so the parse anchors on the
# table row and the gate fails if that count moves: a comma filter would silently drop
# exactly the part of this town the reconstruction is least able to lose.
step "the Black Hawk War enrollments read 134 rows and keep the 83 without a surname" \
  python3 tools/read_blackhawk_war.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/read_blackhawk_war.py --self-test

# T-0573. Father St. Cyr's marriage register and his death page, the first Chicago
# church record. The assertion that carries this one is the page's OWN ARITHMETIC: the
# article prints its tally by priest — St. Cyr 22 marriages, Schaeffer 18, O'Meara 87,
# Plunkett 1 — and the parse of the entries returns exactly those four numbers
# independently. Nobody here has seen the register or the Review, so that agreement is
# the only check this reading can have, and it fails if any of the four moves. The other
# one is the trap the ticket named: footnote 5 puts three of the first four entries at
# Bear Creek, Sangamon County, not Chicago, and those rows carry it themselves.
step "St. Cyr's register reads 128 marriages against the article's own 22+18+87+1" \
  python3 tools/read_st_cyr_register.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/read_st_cyr_register.py --self-test

step "…and its own assertions still fire when broken" \
  python3 tools/newspaper_corpus.py --self-test

step "the .docx extractor is deterministic and keeps its uncertainty brackets" \
  python3 tools/docx_text.py --self-test

# T-0257. The corpus made the papers citable; this is what a READING out of them looks
# like once it has been made, and the gate that keeps one honest. The assertion worth
# knowing about: a claim names the exact transcription lines its quote is built from,
# and this reassembles the quote out of the transcription and refuses any that differs
# by a character. "Never silently smoothed" is otherwise a hope — a tidied quote is
# invisible to every other check here, and the smoothed reading has a field of its own
# (`normalized`) to live in. gazetteer.json is GENERATED, so this also refuses a
# hand-edit to it, the same way the board and the published mirror are refused stale.
step "every newspaper claim resolves, quotes verbatim, and the gazetteer is compiled" \
  python3 tools/compile_gazetteer.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/compile_gazetteer.py --self-test

# T-0305. Four times in its thirteen issues the Chicago American contradicts ITSELF about
# a street, or prints one and loses the cross street that would locate it — the tailor's
# Franklin-or-Lake, which Water street Wm. Sabine and John Dave[s] stood in, and the corner
# of S. B. Cobb's saddlery. None of the four is closeable from the material this repository
# holds: the page images are held outside it, and three of the four subjects appear nowhere
# in the Democrat but a post-office letter list. So the four are DECLARED — each printing
# by claim, page, column and the exact substring it has to carry — and re-derived here,
# along with the negative half over all 73 Democrat issues. The day one of them is answered,
# by an image or by an extraction pass reaching a card nobody has read, this says so instead
# of docs/RESEARCH/american_self_contradictions.md going quietly out of date.
step "the American's four self-contradictions still read as declared" \
  python3 tools/measure_american_contradictions.py --gate

step "…and its own assertions still fire when broken" \
  python3 tools/measure_american_contradictions.py --self-test

# T-0262. The gazetteer says what was PRINTED; the register says what the town has to
# do about it — for every business an action and, where the action needs one, a
# committed target; for every person whether the town already holds them, invented a
# stand-in for them, or has never heard of them. It is DERIVED from the gazetteer and
# the committed dataset, so this refuses a hand-edit for the same reason the gazetteer
# gate does: a hand-edited register is a place to promote a business into the town
# without an argument, and the seeding tickets read it as if it were derived.
step "the scene-date register re-derives, and every action names its target" \
  python3 tools/compile_register.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/compile_register.py --self-test

# And what the town DOES with the register's `street_only` businesses (T-0354). The owner
# ruled on 2026-08-29 that a business the paper places on a platted street and nothing
# narrower adopts a reconstructed roof already standing on that street face;
# docs/STREET-FACE-ADOPTION.md is the policy and this re-derives the allocation. Gated
# rather than committed once because all four of the ruling's limits are assertions about
# a moving town: a roof that gets promoted, a roof that becomes a household's dwelling, a
# second business landing on one roof, or a record that quietly grows a lot field are each
# a silent breach of the ruling, and each one fails here. `--report` prints the deal, every
# refusal with its reason, and both readings of what "standing on that face" means.
step "the street-face adoptions re-derive, and no adopted business claims a lot" \
  python3 tools/adopt_street_faces.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/adopt_street_faces.py --self-test

# THE OTHER HALF OF THE SAME PROBLEM (T-0384, the owner's ruling of 2026-08-30). Where the
# adoptions answer "the paper names a face and no position", this answers "the paper names
# a position and no lot": a count of doors off a named corner — "on South-Water st. one
# door from Dearborn street" — places a store along the face, and AN ORDINAL IS STILL NOT A
# LOT. The limit is written in a field rather than in prose (`lot_claim` on the record) and
# this proves the chain: that the reading and the declaration name the same records, that
# the declaration is well formed and the record has grown no lot field under another name,
# that the plat's barred-lot map is IDENTICAL with the declaring records in the town and
# out of it — the transparency PR #514 lacked, which switched off the business-front clause
# and cost a dealt roof — and that the metres between a door and a corner, which are this
# project's arithmetic and not the paper's, are admitted at a liberty. `--report` prints
# the sweep of every `n doors` phrase the corpus holds. docs/CORNER-ORDINAL.md is the policy.
step "an ordinal off a corner places a position and claims no lot" \
  python3 tools/measure_corner_ordinals.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_corner_ordinals.py --self-test

# SPENDING that allocation is a second gate, because the table and the structure records
# are two files and a policy that only reaches one of them is a policy the visitor never
# sees (T-0417). tools/inferred_occupancy.py is the ledger both the household programme
# and the adoptions hand their `occupants` block to; the generators' own `--check` above
# already refuses a record that has drifted from it, so what is left to prove here is that
# the ledger refuses a malformed adoption rather than passing it through — and that the
# two programmes never both claim one roof.
step "…and the ledger that spends them into the roofs refuses every way one could lie" \
  python3 tools/inferred_occupancy.py --self-test

# AND THE THIRD WAY A PAPER PLACES A BUILDING (T-0423): it prints a LOT AND A BLOCK. Where
# an adoption claims a face and an ordinal claims neither, this claims the plat's own unit,
# and there is exactly one of it in the corpus — G. Spring's For-Sale notice, six printings,
# "LOT No. 7, in block No. 16 … on Lake street". The address is authored in
# data/research/newspapers/lot_addresses.json and NOTHING ELSE about it is: the block number
# resolves through the committed numbering, the lot number through the committed lot grid,
# and which roof stands at the address is derived from its footprint. Gated rather than
# committed once for the same reason the adoptions are — every step of that chain moves when
# the town does. A block renumbered, a lot line redrawn, a second roof built onto the lot or
# a phase promoted because a documented address landed on it all fail here.
step "the lot-and-block address re-derives, and seating it promotes no roof" \
  python3 tools/lot_addresses.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/lot_addresses.py --self-test

# THE 1840 CENSUS LINE -> IPUMS SERIAL JOIN (T-0504). IPUMS holds 964 Chicago households as
# age-band counts with no names; every one of them is also a ruled line on a page image that
# carries the head's name, and the twenty-six free-white age-band columns are the only thing
# the two share. The join is DERIVED from the committed page readings rather than kept by
# hand — which is what the owner's lost v3/v4 workbooks were — so the thing worth gating is
# that it still re-derives: a page reading that changes and a crosswalk that does not is
# exactly the drift a workbook cannot report and this can. --check also holds the refusals:
# an ambiguous fingerprint attaches no serial, a serial is attached to at most one line, and
# a column the page does not close against the enumerator's own foot total is not compared.
step "the 1840 census line-to-serial crosswalk re-derives from the page readings" \
  python3 tools/census_1840_fingerprint.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/census_1840_fingerprint.py --self-test
# T-0513. The consolidation, and the reason it is gated rather than reported: it is the
# only file that says, for one identity, everything the project knows — and it is DERIVED
# from seven domains that each move on their own ticket. A source read on Tuesday that
# never reaches the master is the exact failure the owner named ("there are not outputs or
# updates to the household and resident data"), and it looks like nothing at all until
# somebody rebuilds by hand. --check rebuilds from the domains and fails if the committed
# files have drifted; the invariants it holds are the acceptance's own — one row per
# identity, no record claimed by two identities, every refusal carrying a rule that exists,
# and no row graded above what its rung of the ratified ladder allows.
step "the cross-domain identity master re-derives, and no grade stands above its rung" \
  python3 tools/consolidate_resident_evidence.py --check

step "…and its own assertions still fire when broken" \
  python3 tools/consolidate_resident_evidence.py --self-test

printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf '\033[32mCHECK PASS\033[0m\n'
else
  printf '\033[31mCHECK FAIL\033[0m — fix the above before committing\n'
fi
exit $FAILED
