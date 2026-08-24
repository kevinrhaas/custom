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
  python3 tools/generate_inferred_households.py --check

step "inferred placeholder GLBs match their records" \
  python3 generators/inferred_placeholder.py --check

# The platted block and lot grid is generated from the Thompson module and the
# committed street lines, never traced off the 1834 sheets. Re-deriving it here is
# what keeps it a derivation: a hand-nudged block face would otherwise sit in the
# repo looking exactly like a surveyed one.
step "the platted block and lot grid re-derives from the module" \
  python3 tools/generate_plat_lots.py --check

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

# The frontage works are the fifth record of this shape and the first derived from
# a building AND a street at once: where a plank walk may lie is decided by the
# travelled track's own half-width out of data/streets/1835.json, not by the wall
# alone. Re-derived here for the same reason as the four above — "which wall gets a
# walk" is a rule, and a rule that is not re-run is a rule nobody is keeping (T-0082).
step "the frontage works re-derive from the rule that chose their walls" \
  python3 tools/generate_frontage_works.py --check

# The 665-roof programme's remainder is a function of what has been built, and the town
# grows most nights. Left as an authored number it goes stale silently — the crosswalk
# called 617 roofs remaining while 232 were standing — and the next block parcel schedules
# against a figure that is wrong by a third of the programme.
step "the 665-roof programme reconciles with the town that stands" \
  python3 tools/reconcile_665.py --check

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

# Every generator asks whether the roof it is about to place stands in a platted street,
# and no invented roof has ever been allowed to. Nothing had ever asked it of the records
# a PERSON placed, so the answer arrived as anecdotes — three buildings in T-A9, two more
# in T-A12 — and the distribution behind them was never measured (ROADMAP K30). It is 29
# records, all of them documented and none of them generated. This holds that: a ratchet
# on the 29, and an ABSOLUTE assertion that no generated roof laps a corridor, which the
# placement gate already guarantees and which is therefore enforceable at zero.
step "no building has newly been drawn standing in a platted street" \
  python3 tools/measure_corridor_intrusion.py --gate --quiet

# Two generators build party-line rows onto the committed block faces and each asserts
# that ITS OWN run stands on one line; neither could see the other. The Lake face of
# blk_lake_clark is built by both and carried two lines 0.70 m apart, ten metres apart
# along the face and so not yet reading as a step (T-0104). This is the gate beside the
# two: it takes the face line out of the committed plat, projects every front wall onto
# it, and refuses a face carrying more than one — absolutely, with no ratchet, because
# after T-0104 the number is zero. It also closes party walls from BOTH sides, which is
# the case neither run-local gate can reach when the other half belongs to another
# generator.
step "a block face carries one street line, across every generator that builds on it" \
  python3 tools/measure_street_line.py --gate --quiet

step "…and its own assertions still fire when broken" \
  python3 tools/measure_street_line.py --self-test

# A dwelling nobody named is a count-unit toward a documented aggregate; a PUBLIC
# building nobody named is the claim that an institution stood here and left no record
# at all. ROADMAP T-I3 enumerated them: on 1835-07-01 the town's public buildings with a
# roof are three, all three are committed named records, and every other public function
# in Chicago was carried on inside a private building. generate_block_infill.py has
# refused the institutional families by name since L93, but only for the blocks — the
# North, West and phase-one parcels ran before it existed and nothing had ever asked the
# committed records. This asks all of them: absolute zero for I1 and I3, a ratchet at the
# one anonymous I2 that L93 records rather than deletes.
step "no anonymous roof claims to be a public building" \
  python3 tools/measure_institutional_claims.py --gate --quiet

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

# And the question the two gates above cannot ask, because they read what LANDED: is
# every family the 665-roof schedule may deal to a platted block buildable at every
# size its own band allows? A family comes up rarely — there are two H1s and two H2s in
# the whole parcel — so a band whose tail the archetype refuses looks fine until the
# schedule deals into the tail and the run dies. This deals each family four hundred
# instances through the generator's own sampling and asks the archetype to build each
# one. It found H2 unbuildable over the top third of its authored eave band, D6 over
# the bottom of its own, a rounding step that put a pitch outside the band it was drawn
# from, and W2 fatal to the generator on the day it is first dealt (T-0142).
step "every family the block schedule may deal builds at every size its band allows" \
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
# own note says it follows South Water Street, is 39 of 39 samples over the main stem
# and 3.347 m under its surface — the line of trees across the channel in the owner's
# screenshot (ROADMAP R-BUG5). The renderer refuses it absolutely now; this holds the
# table, and scans the clip so it cannot quietly come back out.
step "no body of far timber stands in the river" \
  python3 tools/measure_far_timber.py --gate

step "…and its own assertions still fire when broken" \
  python3 tools/measure_far_timber.py --self-test

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

# The datum must remain the output of its committed ground control, never a
# hand-edited number. Skips (exit 0) when pyproj is not installed.
step "datum re-derivation" \
  python3 tools/rederive_datum.py

# The liberties the walkthrough shows must still be the ones the markdown
# states. LIBERTIES.md is append-only and is the source of truth; data/
# liberties.json is derived and committed so the site needs no build step, which
# only holds up if drift is a gate failure rather than a discovery.
step "liberties derived from docs/LIBERTIES.md" \
  python3 tools/compile_liberties.py --check

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
  python3 tools/generate_inferred_names.py --check

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

printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf '\033[32mCHECK PASS\033[0m\n'
else
  printf '\033[31mCHECK FAIL\033[0m — fix the above before committing\n'
fi
exit $FAILED
