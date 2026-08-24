#!/usr/bin/env python3
"""Generate the town's frontage works — the plank walks, the board crossings, the
hitching posts and the named boards on posts that stand between a building and the
street it fronts on.

WHAT THIS IS. Ticket **T-0082** wrote it for the Green Tree Tavern, the third of the four
pieces T-0042 (*image-accuracy pass: the Green Tree Tavern*) was split into, and ticket
**T-0090** made it a town rule by adding the second building. The owner's reference views
of both houses describe the ground in front of them, and none of it is furniture standing
in a yard — it is the STREET side of the building:

  * image 6, the Braunhold engraving of the Green Tree, 1838: *"post-mounted hanging
    signboard at the corner; plank sidewalks with board crossings"*;
  * image 7, the Trowbridge drawing of the Green Tree: *"the hanging 'GREEN TREE' sign on
    its post"*, and a dirt road with grass verges;
  * image 8, the Petford watercolour of the Sauganash, 1831: *"plank sidewalk with a board
    crossing over the road; two posts (hitching/corner posts) at the road edge"*;
  * image 9, the Braunhold engraving of the Sauganash: *"plank walks on both frontages,
    hitching posts"*;
  * image 10, the Trowbridge drawing of the Sauganash, which stands a saddled horse at one
    of those posts — L1 reference only, and never depicted.

All are read from `data/sources/assets/owner_brief_2026_08_18/README.md`, which is the
written record of eleven owner-supplied reference images. They are **tier 5 pictorial**:
they may drive massing, materials, furniture and setting, and they may never drive a
coordinate. So WHAT stands here comes from the plates and WHERE is derived from the
committed footprint, the committed placement and the committed street corridor — the
same division `tools/generate_yard_goods.py` keeps for the same buildings' yards.

WHY IT IS A LAYER OF ITS OWN rather than more yard goods. A barrel or a wagon stands on
a building's own ground and is derived from its walls alone. A walk and a crossing stand
in the STREET, and the number that decides where they may lie is the street's — the
travelled track's own half-width out of `data/streets/1835.json`. These records are the
first things in the project derived from a building and a street at once, and tickets
T-0066 (a board carrying its location's name) and T-0069 (fences and plank sidewalks
along the streets) are the town-wide standards they set two buildings at a time.

**ONE RULE, A TABLE OF BUILDINGS.** T-0082 wrote "the second and the twentieth cost
nothing but a line here", and T-0090 spent that line: `BUILDINGS` below is the whole
difference between the two records this writes. What is per-building is the PROSE — which
plate says what, and what the plate shows — and two switches the plates decide:

  * `sign`: a named board on a post at the corner, which the Green Tree's plates show and
    the Sauganash's do not. A building with no `sign` keeps the blank wall board
    `tools/generate_business_signboards.py` hangs on it by rule (docs/LIBERTIES.md L130).
  * `hitching`: posts at the road edge, which the Sauganash's plates show and the Green
    Tree's do not — its plates put a wagon shed and a bench there instead (L134).

Nothing else differs. Every dimension, every clearance and every refusal below is the same
rule at both buildings, and `--check` re-derives both records byte for byte.

THE LETTERING, and it is the one decision in this parcel that needed arguing rather
than deriving. `docs/LIBERTIES.md` L25 decided that the town's one documented sign — the
Wolf Point Tavern's painted wolf — is drawn as a blank board, because no description of
the painting survives, and L130 applied that to all twenty-four boards the signage layer
hangs. **That reasoning does not reach the Green Tree's board.** L25's subject is an IMAGE
nobody has described; that board's subject is a NAME, the plate states it in as many
words, and the name is already in this repository as
`data/structures/green_tree_tavern.json` `name`. Refusing to letter it would not be
caution, it would be discarding evidence the project holds — which is precisely the
reading AGENTS.md § RECONSTRUCTED IS A TIER exists to refuse. So that board carries GREEN
TREE, the wording is graded `inferred` against the plate, and what stays invented is the
LETTERFORM: the face, the size, the spacing and the colour, none of which any source
gives. That split is L135. **The Sauganash gets no lettering**, and not because the rule
is being rationed: none of its three views shows a name board at all.

THE WALL BOARD THIS REPLACES. `tools/generate_business_signboards.py` hangs a blank
board on the Green Tree's front wall by rule (L130). The plates show ONE board at that
inn and it is on a post at the corner, so that generator now refuses this frontage in
writing rather than the town drawing the same claim twice. The Sauganash's plates show no
board at all, so its wall board stands and that generator is not touched.

    python3 tools/generate_frontage_works.py            write the records
    python3 tools/generate_frontage_works.py --check    re-derive and diff
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

# The plat's own face arithmetic (T-0077/T-0078), imported rather than copied:
# which line a block face is, which way its fronts look, and where along it a
# point lands. `tools/` is this script's own directory, so it is on sys.path.
from block_faces import face_frame, project

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIDECARS = DATA / "sidecars" / "1835"
STREETS = DATA / "streets" / "1835.json"
WHARVES = DATA / "wharves" / "river_landings.json"
LOTS = DATA / "traces" / "vectors" / "thompson_lots.json"
EPOCH = DATA / "terrain" / "epochs" / "e1834_harbor_cut"
OUTDIR = DATA / "frontage"
INDEX = OUTDIR / "index.json"

# THE WALK, and why these numbers are here rather than on a record. A walk's WIDTH,
# its rise out of the mud and its plank pitch are HOW a walk is drawn, not a claim
# about this street — the division `enclosures.js` makes between a fence's line (the
# record's) and a rail's thickness (the renderer's). Nothing in this project measures
# a Chicago sidewalk of 1835; six feet is two people passing, and the plank sizes are
# the ordinary sawn stock the same generator already uses for a bench.
WALK_W_M = 1.83          # 6 ft
WALK_CLEAR_M = 0.20      # air between the wall face and the inner edge of the deck
WALK_RISE_M = 0.11       # the deck top over the ground it crosses
PLANK_T_M = 0.055
PLANK_PITCH_M = 0.26     # ~10 in boards, laid with a hair of daylight between them

# THE CROSSING. Four boards laid the way a foot travels rather than across it, which
# is what a crossing is FOR: it spans the ruts instead of lying in them. Its width is
# a stride and a half, not a walk's.
CROSSING_W_M = 1.22      # 4 ft
CROSSING_PLANKS = 4
CROSSING_MARGIN_M = 0.6  # past the far edge of the travelled track, onto dry ground

# THE POST AND ITS BOARD. A pole with a cross-arm at its head and the board hanging
# under the arm — the shape image 4 describes at the Wolf Tavern and image 7 at this
# inn. Every number is invented and none is a record's.
POST_H_M = 3.60
POST_SQ_M = 0.18
ARM_M = 1.55
ARM_T_M = 0.09
HANGER_DROP_M = 0.18
BOARD_W_M = 1.30
BOARD_H_M = 0.55
BOARD_T_M = 0.055
POST_VERGE_M = 0.90      # the post stands this far beyond the outer edge of the walk

# THE HITCHING POSTS (T-0090). Images 8 and 9 put posts at the road edge in front of
# the Sauganash and image 10 ties a saddled horse to one. A hitching post is chest-high
# to a horse and stout enough to hold one, with a capped head so the rein does not lift
# off — and not one of those numbers is a record's either. They stand in the same verge
# the sign post does, at the thirds of the frontage, because a post at the very corner
# is the sign post's ground and a post in the middle is in front of the door.
HITCH_H_M = 1.30
HITCH_SQ_M = 0.16
HITCH_CAP_SQ_M = 0.22
HITCH_CAP_T_M = 0.07
HITCH_VERGE_M = 0.90     # beyond the outer edge of the walk, as the sign post stands
HITCH_ALONG = (0.28, 0.72)   # fractions of the front wall's length

# A wall only gets a walk if a street is actually there. The corridor is 80 ft and the
# buildings sit on its edge, so a frontage wall is within half of it of the centreline;
# a wall further off than this is a yard wall and gets nothing.
STREET_REACH_M = 22.0

# AND THE STREET HAS TO LIE IN FRONT OF THE WALL, NOT BESIDE IT. Added by T-0090, the
# first run to put a second building through this rule, because the second building
# found the hole: the Sauganash's east wall is a side wall in the middle of its block,
# and the nearest point of Lake Street's centreline — which runs across the far END of
# that wall — came out a hair's breadth outward of it. The old test asked only for a
# positive component and passed on 0.13 m of it out of 16 m, laying a walk down the
# building's flank and calling it a frontage.
#
# So the outward component must DOMINATE the distance: the street's nearest point must
# lie within 60 degrees of the wall's own outward normal. Every real frontage measured
# here clears it by a mile (0.998 and better at both buildings, because a building on a
# platted lot sits square to its street); the flank measured 0.008. The clause separates
# a frontage from a flank by two orders of magnitude, which is why it can be a constant
# rather than a judgement.
FRONTAGE_DOMINANCE = 0.5

# THE RIVER PLANK WALK (T-0119). The owner, standing at the State Street slough's
# mouth: "the pedestrian plank sidewalk bridge crossing it close to the river
# should exist and run along the river towards the town." The third record this
# generator writes, and the first NOT derived from a building: its fixed points
# are the Slough Log Bridge's committed deck (the crossing rides it), the traced
# south bank (the walk threads the verge between the South Water track and the
# water), and Jones's landing (data/wharves/river_landings.json), which is where
# the town's wharf walks begin and the run therefore ends. The knots BETWEEN
# those pins are authored here, exactly as the terrain spec's swale lines are,
# and every one of them is audited on every run: each board station must stand
# on dry committed ground and clear the travelled track, or this generator
# refuses to write the record.
RIVER_WALK_ID = "river_plank_walk"
RIVER_APPROACH_M = 1.7     # the crossing footway reaches this far past each deck end
RIVER_DECK_MARGIN_M = 0.05  # the walkable footway strip is this much wider than its boards
RIVER_DRY_M = 0.03         # least ground elevation under a board centre, m over datum
RIVER_CROSS_CLEAR_M = 1.3  # a crossing runs past the track edge by this much each side

# The authored knots, local ENU metres, east to west. Reach ends that meet the
# crossing footway or the Dearborn board crossing are DERIVED below, not listed.
RIVER_EAST_REACH = [[760.0, 14.6], [731.0, 13.8]]     # deck west end .. Dearborn
RIVER_WEST_REACH = [[667.0, 13.9], [638.0, 14.4], [600.0, 15.0], [576.0, 15.4],
                    [537.0, 15.4], [497.0, 15.3], [489.0, 14.6]]  # Dearborn .. La Salle mouth
RIVER_WHARF_REACH = [[459.5, 14.3], [455.0, 24.0], [448.0, 32.0], [428.0, 37.5],
                     [396.0, 40.2], [357.5, 40.3]]    # La Salle mouth .. Jones's landing
RIVER_DEARBORN_CROSS_N = 13.92   # the board crossing over Dearborn runs level at this N

# THE TOWN'S STREET EDGE (T-0069). The owner, of the first Cook County jail
# engraving: "note the fences lining the street and what appears to be plank
# sidewalks. all of the streets should be updated like this... at least south of
# the river or near the river." Four plates in the same brief agree — image 1
# (the jail: board fences at the frontage line with a plank walk at their foot),
# images 8 and 9 (the Sauganash: plank walks on BOTH frontages with board
# crossings over the road) and image 6 (the Green Tree: plank walks and
# crossings). Those are the same two treatments this generator already writes at
# two buildings; what T-0069 adds is that they stop being a building's frontage
# and become the STREET'S EDGE, laid from the platted grid rather than from a
# wall.
#
# WHY THE PLAT AND NOT THE SIDECARS. A walk "at the lot line" needs a lot line,
# and this project has one: `data/traces/vectors/thompson_lots.json`, whose every
# block edge IS a committed street centreline offset by half the committed 80 ft
# corridor (its own `_doc` says so, and tools/generate_plat_lots.py re-derives it
# on every commit). So the treatment comes off the street network by
# construction: move a centreline and every walk below moves with it. Nothing
# here is hand-placed on one block.
#
# THE BOUNDARY DRAWN, and it is the ticket's own words: the two streets that run
# ALONG the river's south bank — SOUTH WATER STREET, which IS the bank, and LAKE
# STREET one block behind it — through the platted blocks between Market Street
# and State Street. Both frontages of Lake, and the one frontage South Water has
# (its north side is the river bank, wharves and landings, not a platted block).
# That is "at least south of the river or near the river", and it is the town's
# whole trading core in 1835.
#
# RANDOLPH STREET WAS BUILT, MEASURED AND TAKEN BACK OUT (T-0127/T-0188), and the
# reading is written here because it is the only thing that answers "why is this
# tuple still two streets" for the next run. Randolph is the widest frontage the
# platted grid holds — 14 block faces against Lake's 12 and South Water's 5 — and
# through this same rule it lays 13 faces and +1,237.9 m of walk, +14 crossings,
# +14 fences, +97 walking decks. Built and published, it read, at the T-0135
# stand set on the published mirror, desktop 1280x800, at the axial stand (Lake
# Street at Canal, east):
#
#   full      1,378,984 -> 1,497,588 of 1,400,000   (+118,604; 97,588 OVER)
#   balanced  1,205,762 -> 1,355,638 of 1,210,000   (+149,876; 145,638 OVER)
#   light       812,753 ->   869,731 of 1,050,000   (inside, 180,269 spare)
#
# — mobile 390x780 the same shape (+115,360 and +150,684, both tiers over). THE
# LEVER T-0115 COSTED FOR THIS PARCEL WAS TAKEN FIRST AND IT IS NOT ENOUGH: the
# ground-hugging boards no longer cast into the shadow map (see `frontage.js`
# `standingChunk` and `main.js applyShadowTier`), and turning OFF the layer's five
# remaining shadow casters at that stand — the fences this ledger argued should
# keep casting, and the shared mesh with the sign post on it — reads 44,110
# triangles and 3 calls, measured, against a 145,638 shortfall.
# THE BINDING FACT IS NOT RANDOLPH: `balanced` stood at 1,205,762 of 1,210,000
# BEFORE this parcel — 4,238 triangles, 0.35 % — and `full` at 1.5 %, where
# T-0135 set both on 2026-08-22 with "about 6 % of headroom". No street tier fits
# until that is addressed, and raising a ceiling a fifth time to fit one reading
# is what T-0135 named as the bug rather than the remedy.
#
# So Randolph, Washington, the cross streets' own frontages and the West Division
# across the South Branch stay out, and the record's own `refused` carries every
# one of these numbers rather than a promise.
EDGE_STREETS = ("south_water", "lake")
EDGE_SKIP_BLOCKS = ("blk_lake_clinton",)   # across the South Branch — see above
EDGE_FENCE_CLEAR_M = 0.25   # daylight between the fence line and the walk's inner edge
EDGE_OFFSET_M = EDGE_FENCE_CLEAR_M + WALK_W_M / 2.0   # walk centre, out from the lot line
EDGE_SPAN_M = 5.2           # the march step: twenty boards, and the unit a face is laid in
EDGE_FLAT_M = 0.07          # relief a single walking deck may carry (see the audit)
EDGE_DRY_M = 0.15           # least ground under a board centre, m over datum
EDGE_MIN_RUN_M = 10.4       # two spans; a shorter stretch is a landing, not a sidewalk
EDGE_DECK_MAX_M = 20.8      # four spans: the longest one flat walking surface
# HOW FAR A WALKING DECK REACHES PAST THE BOARDS IT COVERS. A deck is a polygon
# and a visitor standing exactly on its edge is a point-in-polygon question with
# no good answer: the gate found one sample in a hundred and thirteen standing in
# the mud at the seam between a walk and the crossing that continues it. So each
# deck laps this far past its own stretch at both ends, which closes every seam
# and every run end at the cost of a hand's breadth of lifted ground.
EDGE_DECK_LAP_M = 0.08
EDGE_BUILDING_CLEAR_M = 0.0  # a committed wall inside the deck refuses the board, full stop
EDGE_PLANK_PITCH_M = 0.32   # 12.5 in boards — a street walk's stock, wider than an inn's
EDGE_STRINGER_PITCH_M = 2.08  # boards to a stringer bay (see the note on cost)
EDGE_STRINGER_ROLL_M = 0.04   # ground a single bay-length stringer may span (audited)
EDGE_CROSS_STEP_M = 1.8       # a crossing is cut this often along its run
# A TOWN'S WORTH OF BOARDS IS A DIFFERENT ARITHMETIC FROM AN INN'S FRONTAGE, and
# these three numbers are the whole of the difference. A walk board is a box, and
# of its twelve triangles the two facing the earth under it are the ones nobody
# will ever stand low enough to see; a stringer bay carries several boards where
# the two inns' walks carry one each; and street stock is wider than an inn's
# trim. Measured at the release gate's own stand these three take the layer from
# 61.6 to 42.8 triangles a metre, which is what makes a whole street affordable
# at all — and not one of them moves a board a millimetre from where it lies.
EDGE_PLANK_UNDERSIDE = False
# HOW THE STREET EDGE IS CHUNKED: one mesh per RUN of walk, carrying the
# crossings that spring from it and the fence standing behind it. A chunk's
# bounding sphere is what the frustum and the sun's own box test, so chunk size is
# a straight trade — finer chunks cull better and cost a draw call each — and it
# was measured three ways rather than guessed: per run (~55 m), per 120 m reach
# and per 200 m reach. Coarser chunks cull worse, and the cost lands on the tier
# that can least afford it: at 200 m the MAIN pass drew nearly half the town's
# street edge from a stand that could see sixty metres of it, and `light` — the
# floor a weak machine has to hold — read 595,079 of 600,000 against 583,033 per
# run. Per run wins on the number that matters and spends draw calls instead,
# which the owner ruled on 2026-08-21 is the cheaper of the two.
EDGE_CROSS_W_M = 1.83       # a corner crossing is a walk's width, not a stride's
EDGE_CROSS_PLANKS = 6
EDGE_TRACK_MARGIN_M = 0.35  # least verge between the walk's outer edge and the track

# THE STREET-LINING FENCE. The jail engraving's fences stand at the frontage
# line, in front of the building and behind the walk, which is where a fence goes
# when the lot is improved and the building is NOT built out to the street. That
# is the rule: a lot gets a street fence iff it is improved and its own committed
# walls stand back from its frontage line. A lot built to the line needs none —
# the building IS the street wall, which is what the engraving shows either side
# of its fenced yards.
EDGE_FENCE_SETBACK_M = 3.0  # least distance from the frontage line to the nearest wall
EDGE_FENCE_H_M = 1.37       # 4 ft 6 in — a street fence, not the Sauganash's private 6 ft
EDGE_FENCE_BOARD_W_M = 0.305
EDGE_FENCE_BOARD_GAP_M = 0.006
EDGE_FENCE_POST_SPACING_M = 2.44
EDGE_FENCE_POST_SQ_M = 0.12
EDGE_FENCE_COURSES = 2

# THE SOUTH WATER PLACEMENTS (T-0127), NAMED HERE BECAUSE THE RECORD IS WHERE A
# READER MEETS THEM. Eleven documented buildings on South Water Street's south
# side were placed in August 2026 by reading the MODERN West Wacker Drive
# centreline out of OpenStreetMap and stepping half a platted street south of it
# — each record says so in its own `position.note`, and several already warn that
# "modern Wacker Drive is not exactly the 1835 South Water Street line". Measured
# against this project's OWN committed line they stood 4.51 to 8.17 m out past
# the platted frontage, in the roadway, and the march below refused the sidewalk
# around every one of them.
#
# SIX WERE RECONCILED UNDER T-0188 and their walls now stand 1.50 m back from the
# committed frontage line, the same margin `tools/generate_block_infill.py` gives
# every reconstructed unit on these faces. THE OTHER FIVE COULD NOT BE, and the
# reason was a finding rather than a shrug: reconciled onto the plat a building
# SEATS on a platted lot, and for those five that lot was one the 665-roof
# schedule had dealt to the anonymous South Water frontage run, which the
# placement gate refused to deal a second roof.
#
# T-0199 UNTANGLED IT AND ALL ELEVEN NOW STAND ON THE PLAT. The measurement that
# decided it is `tools/measure_frontage_entitlement.py`: the town's eight
# party-line runs were dealt 20 lots of frontage and STAND ON 12, because a run
# packs from one end of its strip and three of its units fit inside one lot of
# this grid. Eight platted lots were entitled to a run that has never had a roof
# on them, and four of the five refusals were those lots. The fifth, Philo
# Carpenter's store, shares lot 2 of `blk_south_water_wells` with the run's third
# unit — 25.04 m of frontage against T-0079's measured ceiling of three units —
# and the only thing that had to give was a clearance: the recipe stood that unit
# 2.4 m along the face from a store that was 6.62 m out in the roadway, so the
# plan gap was legal on the diagonal and became 2.40 m against a 3.00 m gate the
# moment both walls stood on one line. The unit steps 0.60 m west. No roof left
# the town.
EDGE_RECONCILED = {
    "harmon_loomis_store": 6.81, "madore_beaubien_house": 7.48,
    "peck_store": 6.01, "chicago_democrat_office": 6.61,
    "temple_building": 6.90, "jh_kinzie_forwarding_store": 8.38,
    "h_jones_store": 9.67, "carpenter_south_water_store": 8.12,
    "pruyne_kimball_drugstore": 7.05, "chicago_american_office": 8.41,
    "frederick_thomas_shop": 7.75,
}
EDGE_UNRECONCILED: dict[str, tuple[float, str, int, float]] = {}

# The record's own id, and the liberty that claims every invented metre in it.
STREET_EDGE_ID = "town_street_edge"
STREET_EDGE_RECORD_ID = "town_street_edge"
STREET_EDGE_LIBERTY = "L160"


# ---------------------------------------------------------------------------- #
# THE TABLE. One entry per building whose own reference views describe its street
# side. Everything here is PROSE and two switches; the rule below is shared.
# ---------------------------------------------------------------------------- #
BUILDINGS = [
    {
        "structure_id": "green_tree_tavern",
        "out": "green_tree_frontage.json",
        "record_id": "green_tree_frontage",
        "name": ("The Green Tree's frontage: plank walks, a board crossing, and its "
                 "named board on a post"),
        "noun": "inn",
        "liberty": "L135",
        "sign": {"text": "GREEN TREE"},
        "hitching": None,
        "doc": (
            "The Green Tree's frontage works — the plank walks along its two street "
            "walls, the board crossing over Canal, and the named board on its post at "
            "the corner. NOT a structure record and NOT geometry that comes out of "
            "Blender: a walk is boards laid on ground this project has already built "
            "and a post is a pole standing on it, so both are derived from the "
            "committed footprint, the committed placement and the committed street "
            "corridor, and drawn at load by renderers/web/js/frontage.js. Generated by "
            "tools/generate_frontage_works.py and re-derived byte for byte by "
            "tools/check.sh, because 'where a walk may lie' is a rule and a rule has "
            "to be auditable."
        ),
        "existence_sources": ["trowbridge_green_tree_1902"],
        "existence_note": (
            "NO SOURCE RECORD IN THIS REPOSITORY STATES THAT A WALK, A CROSSING OR "
            "A POST STOOD ON THIS GROUND ON 1 JULY 1835. What is held is two "
            "owner-supplied reference views of this inn, written up verbatim at "
            "data/sources/assets/owner_brief_2026_08_18/README.md: image 6, the "
            "Braunhold engraving of 1838, gives 'post-mounted hanging signboard at "
            "the corner; plank sidewalks with board crossings', and image 7, the "
            "Trowbridge drawing, gives 'the hanging \"GREEN TREE\" sign on its "
            "post'. Both are tier-5 pictorial and retrospective. ONE OF THE TWO IS "
            "NOW A SOURCE RECORD: T-0075 identified image 7 as W. E. S. Trowbridge's "
            "drawing 'The Green Tree Tavern in 1835', signed and dated 1902, and it "
            "is cited here as `trowbridge_green_tree_1902`. Image 6, the Braunhold "
            "engraving, is stated to be an Andreas 1884 plate and is not reproduced "
            "on any page this project holds, so it stays a committed path and the "
            "README's identification table says what was searched. A citation does "
            "not promote the claim: a tier-5 retrospective may drive setting and may "
            "never drive a coordinate, so this is still a reconstruction in this "
            "project's third tier, graded and claimed as one: docs/LIBERTIES.md L135."
        ),
        "claim_key": "lettering",
        "claim_block": {
            "value": "GREEN TREE",
            "confidence": "inferred",
            "geometry": "drawn",
            "sources": ["trowbridge_green_tree_1902"],
            "note": (
                "THE FIRST LETTERING THIS PROJECT HAS EVER DRAWN, and the decision is "
                "argued rather than assumed. docs/LIBERTIES.md L25 leaves the Wolf "
                "Point Tavern's board blank and L130 leaves twenty-four more blank, "
                "for a reason that does not reach this one: L25's subject is an IMAGE "
                "nobody has described — no source says how the wolf was painted — "
                "while this board's subject is a NAME, image 7 states it in as many "
                "words, and the name is already committed on "
                "data/structures/green_tree_tavern.json. Leaving it blank would be "
                "discarding evidence the project holds. So the WORDING is graded "
                "`inferred` against the plate, and what remains invented is the "
                "LETTERFORM — the face, the size, the spacing, the colour and the "
                "paint's wear — which no source gives and which L135 claims. The other "
                "boards in the town stay blank: nothing states what any of THEM said."
            ),
        },
        "walk_evidence": (
            "The Braunhold engraving of the Green Tree "
            "(data/sources/assets/owner_brief_2026_08_18/README.md, image 6) shows "
            "plank sidewalks with board crossings at this building — a tier-5 "
            "retrospective view, which may drive setting and may never drive a "
            "coordinate."
        ),
        "crossing_evidence": (
            "Image 6 gives *plank sidewalks with board crossings* at this inn and "
            "image 8 the same at the Sauganash, so the fact is the plates' and every "
            "dimension is invented."
        ),
        "post_evidence": (
            "Image 6 puts a post-mounted hanging signboard at this inn's corner and "
            "image 7 says what is on it."
        ),
        "sign_text_note": (
            "`trowbridge_green_tree_1902` — W. E. S. Trowbridge's drawing 'The "
            "Green Tree Tavern in 1835', signed 1902, image 7 of the owner's brief "
            "of 2026-08-18 and identified under T-0075 on 2026-08-22. The plate was "
            "retrieved and read: the board hangs from a post at the street edge and "
            "is lettered GREEN TREE. The wording is the plate's; the letterform is "
            "ours (docs/LIBERTIES.md L135)."
        ),
        "treatment_mid": (
            f"Post {POST_H_M} m tall and {POST_SQ_M} m square, a {ARM_M} m cross-arm "
            f"at its head, and a {BOARD_W_M} x {BOARD_H_M} m board hanging "
            f"{HANGER_DROP_M} m under the arm. "
        ),
        "rule_mid": (
            "the post stands at the corner the front and left walls make, outside "
            "both walks and clear of the track. "
        ),
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: a Chicago town order on "
            "sidewalks — the corporation legislated wooden walks within a few years of "
            "1835 and an order of the right date would give a width and a material at "
            "a stroke; a tax, insurance or sale description naming a walk in front of a "
            "lot; or holding the Braunhold plate as a proper source record with its "
            "institution and date. The Trowbridge plate IS one now "
            "(`trowbridge_green_tree_1902`, T-0075, 2026-08-22), which is what turned "
            "the lettering's warrant from a committed path into a citation; the "
            "Braunhold engraving of 1838 is still cited by path and the next attempt "
            "at it should go to Andreas volume I at page-image level. Neither "
            "citation moves this layer off reconstruction — a plate may say a walk "
            "was the treatment and can never say one stood on THIS ground."
        ),
    },
    {
        "structure_id": "sauganash_hotel",
        "out": "sauganash_frontage.json",
        "record_id": "sauganash_frontage",
        "name": ("The Sauganash's frontage: plank walks on both fronts, a board "
                 "crossing, and hitching posts at the road edge"),
        "noun": "hotel",
        "liberty": "L136",
        "sign": None,
        "hitching": {"count": 2},
        "doc": (
            "The Sauganash Hotel's frontage works — the plank walks along its two "
            "street walls, the board crossing over the road, and the two hitching "
            "posts at the road edge. NOT a structure record and NOT geometry that "
            "comes out of Blender: a walk is boards laid on ground this project has "
            "already built and a post is a pole standing on it, so both are derived "
            "from the committed footprint, the committed placement and the committed "
            "street corridor, and drawn at load by renderers/web/js/frontage.js. "
            "Generated by tools/generate_frontage_works.py and re-derived byte for "
            "byte by tools/check.sh, because 'where a walk may lie' is a rule and a "
            "rule has to be auditable."
        ),
        "existence_note": (
            "NO SOURCE RECORD IN THIS REPOSITORY STATES THAT A WALK, A CROSSING OR A "
            "POST STOOD ON THIS GROUND ON 1 JULY 1835. What is held is three "
            "owner-supplied reference views of this hotel, written up verbatim at "
            "data/sources/assets/owner_brief_2026_08_18/README.md: image 8, the "
            "Petford watercolour of 1831, gives 'plank sidewalk with a board crossing "
            "over the road' and 'two posts (hitching/corner posts) at the road edge'; "
            "image 9, the Braunhold engraving, gives 'plank walks on both frontages, "
            "hitching posts'; image 10, the Trowbridge drawing, stands a saddled horse "
            "at one of those posts — reference for use only, and never depicted, which "
            "is the L1 constraint. All three are tier-5 pictorial and retrospective. "
            "ONE OF THE THREE IS NOW A SOURCE RECORD: T-0075 identified image 10 as "
            "W. E. S. Trowbridge's drawing of the Sauganash, and it is cited here as "
            "`trowbridge_sauganash_hotel` — the plate that stands the posts at the "
            "road edge and the board fence behind. The Petford watercolour is a "
            "museum object needing an accession number and the Braunhold engraving is "
            "an Andreas plate not reproduced on any page this project holds, so both "
            "stay committed paths; the README's identification table says what was "
            "searched. A citation does not promote the claim: this is still a "
            "reconstruction in this project's third tier, graded and claimed as one: "
            "docs/LIBERTIES.md L136."
        ),
        "existence_sources": ["trowbridge_sauganash_hotel"],
        "claim_key": "board_on_a_post",
        "claim_block": {
            "value": False,
            "confidence": "inferred",
            "note": (
                "NO NAMED BOARD ON A POST HERE, and the absence is a reading rather "
                "than an omission. The Green Tree's two views both show one board at "
                "that inn, post-mounted at the corner and lettered, which is why the "
                "frontage layer draws it and docs/LIBERTIES.md L135 argues the "
                "letterform. THIS hotel's three views show posts at the road edge and "
                "no name board on any of them: images 8 and 9 call them hitching or "
                "corner posts and image 10 ties a horse to one. So the posts are drawn "
                "as what the plates show, the hotel keeps the blank wall board "
                "tools/generate_business_signboards.py hangs on every trading frontage "
                "by rule (L130), and nothing here is lettered — the project letters a "
                "board only where a plate says what it said."
            ),
        },
        "walk_evidence": (
            "The Petford watercolour of 1831 and the Braunhold engraving in Andreas "
            "(data/sources/assets/owner_brief_2026_08_18/README.md, images 8 and 9) "
            "show a plank sidewalk at this building and walks on BOTH its frontages — "
            "tier-5 retrospective views, which may drive setting and may never drive a "
            "coordinate."
        ),
        "crossing_evidence": (
            "Image 8 gives *plank sidewalk with a board crossing over the road* at "
            "this hotel — the 'landings' of the owner's ask — so the fact is the "
            "plate's and every dimension is invented."
        ),
        "post_evidence": (
            "Images 8 and 9 put posts at this hotel's road edge and image 10 ties a "
            "saddled horse to one."
        ),
        "sign_text_note": None,
        "treatment_mid": (
            f"Hitching posts {HITCH_H_M} m tall and {HITCH_SQ_M} m square under a "
            f"{HITCH_CAP_SQ_M} m capped head, standing {HITCH_VERGE_M} m beyond the "
            "outer edge of the walk. "
        ),
        "rule_mid": (
            "the hitching posts stand in that same verge outside the front walk, at "
            f"{HITCH_ALONG[0]:.2f} and {HITCH_ALONG[1]:.2f} of the front wall's "
            "length, and each is refused if it would stand in the track. "
        ),
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: a Chicago town order on "
            "sidewalks — the corporation legislated wooden walks within a few years of "
            "1835 and an order of the right date would give a width and a material at "
            "a stroke; a tax, insurance or sale description naming a walk in front of "
            "this lot; or holding the Petford and Braunhold plates as proper source "
            "records with their institutions and dates. The Trowbridge plate IS one "
            "now (`trowbridge_sauganash_hotel`, T-0075, 2026-08-22) and `existence` "
            "cites it; the Petford needs a Chicago History Museum accession number "
            "and the Braunhold needs Andreas volume I at page-image level. What would "
            "NOT move: the two posts' own dimensions, which no order and no plate "
            "will ever give."
        ),
    },
]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _round(x: float, places: int = 2) -> float:
    """Round toward a stable decimal so `--check` diffs bytes, not float noise."""
    return round(x + 0.0, places) + 0.0


def _to_enu(u: float, v: float, place: dict) -> tuple[float, float]:
    """A footprint coordinate to local ENU metres.

    docs/GLB-CONTRACT.md: polygon `u` -> +X, polygon `v` -> -Z, ENU `local_e` -> +X
    and `local_n` -> -Z, and the node's yaw is `-rotation_deg` about +Y. The same
    three lines `tools/generate_business_signboards.py` composes, and no other.
    """
    th = math.radians(-(place.get("rotation_deg") or 0.0))
    x, z = u, -v
    xr = x * math.cos(th) + z * math.sin(th)
    zr = -x * math.sin(th) + z * math.cos(th)
    return (place.get("local_e") or 0.0) + xr, (place.get("local_n") or 0.0) - zr


def _unit(dx: float, dy: float) -> tuple[float, float]:
    L = math.hypot(dx, dy)
    return (0.0, 0.0) if L == 0 else (dx / L, dy / L)


def _nearest_on_path(pt, path) -> tuple[float, tuple[float, float]]:
    """(distance, foot) from a point to an open polyline in local ENU metres."""
    x, y = pt
    best = (float("inf"), (x, y))
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
        fx, fy = x1 + t * dx, y1 + t * dy
        d = math.hypot(x - fx, y - fy)
        if d < best[0]:
            best = (d, (fx, fy))
    return best


def _streets() -> dict:
    doc = _load(STREETS)
    default_track = 7.0
    out = {}
    for s in doc.get("streets", []):
        out[s["id"]] = {
            "name": s.get("name_1835") or s["id"],
            "path": [tuple(p) for p in s.get("path_local_enu_m", [])],
            "track_w": float(s.get("track_width_m") or default_track),
        }
    return out


def _street_facing(mid, normal, streets: dict) -> tuple[str | None, dict, float, dict]:
    """Which street a wall faces: the nearest centreline that lies IN FRONT of it.

    Outward is the first test that matters. A rear wall can be as close to a street
    as a front wall is to another one, and a walk laid on the wrong side of a
    building would be a walk through its own yard.

    In front is the second, and it is the one T-0090 had to add (FRONTAGE_DOMINANCE
    above). A street that lies beside a wall rather than in front of it is reported
    back as `aside` so the refusal can say which test refused it and why, rather
    than the wall silently reading as having no street at all.
    """
    best = (None, {}, float("inf"))
    aside: dict = {}
    for sid, st in streets.items():
        if len(st["path"]) < 2:
            continue
        d, foot = _nearest_on_path(mid, st["path"])
        outward = (foot[0] - mid[0]) * normal[0] + (foot[1] - mid[1]) * normal[1]
        if outward <= 0 or d > STREET_REACH_M:
            continue
        if outward < FRONTAGE_DOMINANCE * d:
            if not aside or d < aside["dist"]:
                aside = {"name": st["name"], "dist": d, "outward": outward}
            continue
        if d < best[2]:
            best = (sid, st, d)
    return best[0], best[1], best[2], aside


def build(cfg: dict) -> tuple[list, list, list]:
    """The walks, the crossings and the posts of ONE building, every refusal stated."""
    sid_b = cfg["structure_id"]
    noun = cfg["noun"]
    walks: list = []
    posts: list = []
    refused: list = []

    sc_path = SIDECARS / f"{sid_b}.json"
    if not sc_path.exists():
        return [], [], [{"structure_id": sid_b, "why": (
            f"the {noun} is not standing in data/sidecars/1835 — nothing is laid on its "
            "frontage.")}]
    sc = _load(sc_path)
    place = sc.get("placement") or {}
    poly = (sc.get("footprint") or {}).get("polygon") or []
    if place.get("local_e") is None or len(poly) < 3:
        return [], [], [{"structure_id": sid_b, "why": (
            f"the {noun} has no placed footprint — no frontage can be derived.")}]

    u0 = min(p[0] for p in poly)
    u1 = max(p[0] for p in poly)
    v0 = min(p[1] for p in poly)
    v1 = max(p[1] for p in poly)
    streets = _streets()

    # The four walls of the committed footprint, each as (label, endpoint, endpoint)
    # in footprint coordinates. The front is the max-v edge by docs/GLB-CONTRACT.md,
    # and every other wall is named relative to it rather than by compass, because
    # the compass depends on the rotation and the contract does not.
    walls = [
        ("front", (u0, v1), (u1, v1)),
        ("left", (u0, v0), (u0, v1)),
        ("right", (u1, v1), (u1, v0)),
        ("rear", (u1, v0), (u0, v0)),
    ]

    corner_world = _to_enu(u0, v1, place)   # where the front and the left wall meet
    laid: dict = {}

    for label, a_uv, b_uv in walls:
        a = _to_enu(*a_uv, place)
        b = _to_enu(*b_uv, place)
        along = _unit(b[0] - a[0], b[1] - a[1])
        # Outward is to the LEFT of a -> b. The four walls above are wound so that
        # the inside of the footprint is on the RIGHT of every one of them, and the
        # footprint -> ENU map above preserves orientation (u runs to ENU +N and v
        # to ENU -E on this record, a rotation and not a reflection), so the sign
        # survives the transform. A wall whose normal came out inward would lay its
        # walk inside the building, which is why this is checked by the outward test
        # in _street_facing rather than trusted.
        normal = (-along[1], along[0])
        mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        sid, st, dist, aside = _street_facing(mid, normal, streets)
        if sid is None and aside:
            refused.append({"structure_id": sid_b, "wall": label, "why": (
                f"the nearest street outward of this wall is {aside['name']}, and it "
                f"lies BESIDE the wall rather than in front of it — {aside['outward']:.2f} m "
                f"of its {aside['dist']:.2f} m stands outward, where a frontage needs "
                f"{FRONTAGE_DOMINANCE:.0%}. A walk laid here would run down the "
                f"{noun}'s flank and call it a frontage — no walk is laid.")})
            continue
        if sid is None:
            refused.append({"structure_id": sid_b, "wall": label, "why": (
                f"no street centreline lies outward of this wall within "
                f"{STREET_REACH_M:.0f} m — a walk here would be a walk through the "
                f"{noun}'s own yard.")})
            continue
        off = WALK_CLEAR_M + WALK_W_M / 2.0
        centre_a = (a[0] + normal[0] * off, a[1] + normal[1] * off)
        centre_b = (b[0] + normal[0] * off, b[1] + normal[1] * off)
        # A walk must lie on the near side of the travelled way, never in it.
        edge = dist - (WALK_CLEAR_M + WALK_W_M) - st["track_w"] / 2.0
        if edge <= 0:
            refused.append({"structure_id": sid_b, "wall": label, "why": (
                f"the {st['name']} track reaches to within {dist:.2f} m of this wall "
                f"and a {WALK_W_M:.2f} m walk laid off it would lie in the travelled "
                "way — no walk is laid.")})
            continue
        laid[label] = {"normal": normal, "along": along, "street": sid, "dist": dist,
                       "track_w": st["track_w"], "a": centre_a, "b": centre_b,
                       "len": math.hypot(b[0] - a[0], b[1] - a[1]), "wall_a": a}
        walks.append({
            "id": f"{sid_b}_walk_{label}",
            "belongs_to": sid_b,
            "kind": "plank_walk",
            "confidence": "reconstructed",
            "street": sid,
            "street_name": st["name"],
            "centreline_local_enu_m": [[_round(centre_a[0]), _round(centre_a[1])],
                                       [_round(centre_b[0]), _round(centre_b[1])]],
            "width_m": WALK_W_M,
            "rise_m": WALK_RISE_M,
            "plank_run": "across",
            "plank_pitch_m": PLANK_PITCH_M,
            "plank_thickness_m": PLANK_T_M,
            "wall_offset_m": _round(WALK_CLEAR_M),
            "verge_to_track_m": _round(edge),
            "note": (
                f"A PLANK WALK ON THE {noun.upper()}'S FRONTAGE, and the plates are "
                f"the whole reason it is here. {cfg['walk_evidence']} So WHERE is "
                f"derived: the deck lies "
                f"{WALK_CLEAR_M:.2f} m off the {label} wall, {WALK_W_M:.2f} m wide, "
                f"leaving {edge:.2f} m of verge between its outer edge and the "
                f"{st['name']} track — which is the number that decides a walk may lie "
                "here at all. What is invented is the width, the rise, the plank "
                "pitch, and that a walk stood on this ground at noon on 1 July 1835: "
                f"docs/LIBERTIES.md {cfg['liberty']}."
            ),
        })

    # ---- the crossing ------------------------------------------------------ #
    # Over the street the FRONT wall faces, springing from the front walk at the
    # corner end — which is where a crossing is, because a crossing joins corners.
    front = laid.get("front")
    if front is None:
        refused.append({"structure_id": sid_b, "wall": "front", "why": (
            "no walk lies on the front, so nothing springs a crossing off it.")})
    else:
        n = front["normal"]
        # Start at the corner end of the front walk's outer edge, one board's width
        # in from the very corner so the crossing does not clip the post's ground.
        start = (front["a"][0] + n[0] * (WALK_W_M / 2.0) + front["along"][0] * CROSSING_W_M,
                 front["a"][1] + n[1] * (WALK_W_M / 2.0) + front["along"][1] * CROSSING_W_M)
        run = (front["dist"] - (WALK_CLEAR_M + WALK_W_M)
               + front["track_w"] / 2.0 + CROSSING_MARGIN_M)
        end = (start[0] + n[0] * run, start[1] + n[1] * run)
        walks.append({
            "id": f"{sid_b}_crossing_front",
            "belongs_to": sid_b,
            "kind": "board_crossing",
            "confidence": "reconstructed",
            "street": front["street"],
            "street_name": streets[front["street"]]["name"],
            "centreline_local_enu_m": [[_round(start[0]), _round(start[1])],
                                       [_round(end[0]), _round(end[1])]],
            "width_m": CROSSING_W_M,
            "rise_m": _round(WALK_RISE_M / 2.0),
            "plank_run": "along",
            "plank_count": CROSSING_PLANKS,
            "plank_thickness_m": PLANK_T_M,
            "run_m": _round(run),
            "note": (
                f"A BOARD CROSSING OVER THE STREET. {cfg['crossing_evidence']} Its "
                "boards run "
                "the way a foot travels rather than across it, which is what a crossing "
                "is FOR — it spans the ruts instead of lying in them; a walk's boards "
                "run the other way. WHERE is derived: it leaves the front walk's outer "
                f"edge and runs {run:.2f} m, which is the walk's own verge plus half the "
                f"{streets[front['street']]['name']} track plus "
                f"{CROSSING_MARGIN_M:.2f} m onto the dry ground beyond it, so it reaches "
                "across the travelled way rather than stopping in it. It lies lower than "
                f"the walk because a wheel crosses it. docs/LIBERTIES.md {cfg['liberty']}."
            ),
        })

    # ---- the board on its post --------------------------------------------- #
    # AT THE CORNER, in the verge outside both walks. Image 6 says *at the corner*
    # and image 7 draws it on a post, so the corner is the plates' and the stand is
    # derived from the two walks that meet there. Only a building whose own views
    # show a named board gets one — the Sauganash's do not, and it gets none.
    left = laid.get("left")
    if cfg["sign"] is None:
        pass
    elif front is None or left is None:
        refused.append({"structure_id": sid_b, "wall": "corner", "why": (
            "the post stands at the corner two walks make, and one of the two was "
            "refused — no board is put on a post.")})
    else:
        out_f = WALK_CLEAR_M + WALK_W_M + POST_VERGE_M
        out_l = WALK_CLEAR_M + WALK_W_M + POST_VERGE_M
        at = (corner_world[0] + front["normal"][0] * out_f + left["normal"][0] * out_l,
              corner_world[1] + front["normal"][1] * out_f + left["normal"][1] * out_l)
        reach = front["dist"] - out_f - front["track_w"] / 2.0
        if reach <= 0:
            refused.append({"structure_id": sid_b, "wall": "corner", "why": (
                f"a post {out_f:.2f} m out from the front wall would stand in the "
                f"{streets[front['street']]['name']} track — no board is put on a "
                "post.")})
        else:
            bearing = float(place.get("rotation_deg") or 0.0)
            posts.append({
                "id": f"{sid_b}_sign_post",
                "belongs_to": sid_b,
                "kind": "sign_post",
                "confidence": "reconstructed",
                "at_local_enu_m": [_round(at[0]), _round(at[1])],
                "facade_bearing_deg": _round(bearing, 1),
                "post_height_m": POST_H_M,
                "post_square_m": POST_SQ_M,
                "arm_m": ARM_M,
                "arm_bearing": "along the front wall, away from the corner",
                "board_w_m": BOARD_W_M,
                "board_h_m": BOARD_H_M,
                "board_thickness_m": BOARD_T_M,
                "hanger_drop_m": HANGER_DROP_M,
                "text": cfg["sign"]["text"],
                "text_confidence": "inferred",
                "text_sources_note": cfg["sign_text_note"],
                "clear_of_track_m": _round(reach),
                "note": (
                    "THE NAMED BOARD ON ITS POST, at the corner of the two streets. "
                    f"{cfg['post_evidence']} WHERE is derived: the post "
                    f"stands {out_f:.2f} m out from each of the two walls that make "
                    "the corner — clear of both walks by "
                    f"{POST_VERGE_M:.2f} m — with {reach:.2f} m still between it and "
                    "the travelled track. Its cross-arm runs along the front wall away "
                    "from the corner, so the board's face looks down the street the "
                    f"{noun} fronts on. The pole, the arm and the board are invented in "
                    "every dimension, and so is the letterform; the WORDING is the "
                    f"plate's. docs/LIBERTIES.md {cfg['liberty']}."
                ),
            })

    # ---- the hitching posts (T-0090) --------------------------------------- #
    # In the verge outside the FRONT walk, at the thirds of the frontage. The plates
    # say posts stand at this hotel's road edge; how many and how far apart is the
    # rule's, and a post that would stand in the travelled track is refused rather
    # than pulled in to fit.
    hitch = cfg["hitching"]
    if hitch is None:
        pass
    elif front is None:
        refused.append({"structure_id": sid_b, "wall": "front", "why": (
            "no walk lies on the front, so there is no verge outside it for a "
            "hitching post to stand in.")})
    else:
        n = front["normal"]
        out_f = WALK_CLEAR_M + WALK_W_M + HITCH_VERGE_M
        reach = front["dist"] - out_f - front["track_w"] / 2.0
        base = front["wall_a"]
        for i, frac in enumerate(HITCH_ALONG[:hitch["count"]], start=1):
            if reach <= 0:
                refused.append({"structure_id": sid_b, "wall": f"front hitching post {i}",
                                "why": (
                    f"a post {out_f:.2f} m out from the front wall would stand in the "
                    f"{streets[front['street']]['name']} track — no post is set.")})
                continue
            along_m = frac * front["len"]
            at = (base[0] + front["along"][0] * along_m + n[0] * out_f,
                  base[1] + front["along"][1] * along_m + n[1] * out_f)
            posts.append({
                "id": f"{sid_b}_hitching_post_{i}",
                "belongs_to": sid_b,
                "kind": "hitching_post",
                "confidence": "reconstructed",
                "at_local_enu_m": [_round(at[0]), _round(at[1])],
                "facade_bearing_deg": _round(float(place.get("rotation_deg") or 0.0), 1),
                "post_height_m": HITCH_H_M,
                "post_square_m": HITCH_SQ_M,
                "cap_square_m": HITCH_CAP_SQ_M,
                "cap_thickness_m": HITCH_CAP_T_M,
                "along_frontage_frac": frac,
                "clear_of_track_m": _round(reach),
                "note": (
                    "A POST AT THE ROAD EDGE, for a rider to tie to. "
                    f"{cfg['post_evidence']} The horse itself is reference for use and "
                    "scale only and is never depicted, which is the standing L1 "
                    "constraint. WHERE is derived: it stands "
                    f"{out_f:.2f} m out from the front wall — {HITCH_VERGE_M:.2f} m "
                    f"clear of the walk's outer edge — at {frac:.2f} of the frontage's "
                    f"own length, with {reach:.2f} m still between it and the "
                    f"{streets[front['street']]['name']} track. The height, the "
                    "section and the capped head are invented, and so is that a post "
                    "stood on this ground at noon on 1 July 1835: docs/LIBERTIES.md "
                    f"{cfg['liberty']}."
                ),
            })

    walks.sort(key=lambda w: w["id"])
    posts.sort(key=lambda p: p["id"])
    refused.sort(key=lambda r: (r["structure_id"], r.get("wall", "")))
    return walks, posts, refused


def record(cfg: dict, walks: list, posts: list, refused: list) -> dict:
    rec = {
        "_doc": cfg["doc"],
        "id": cfg["record_id"],
        "name": cfg["name"],
        "kind": "frontage",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same frame "
            "data/signage/, data/yard/ and the sidecars' placement.local_e / local_n use."
        ),
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": list(cfg.get("existence_sources", ())),
            "note": cfg["existence_note"],
        },
    }
    rec[cfg["claim_key"]] = cfg["claim_block"]
    rec["treatment"] = {
        "confidence": "reconstructed",
        "note": (
            f"Walk {WALK_W_M} m wide, {WALK_CLEAR_M} m off the wall, its deck "
            f"{WALK_RISE_M} m over the ground, {PLANK_T_M} m boards at a "
            f"{PLANK_PITCH_M} m pitch laid ACROSS the way a foot travels. Crossing "
            f"{CROSSING_W_M} m wide and {CROSSING_PLANKS} boards laid ALONG it, "
            "reaching past the far edge of the travelled track by "
            f"{CROSSING_MARGIN_M} m. " + cfg["treatment_mid"] + "Not one of those "
            "numbers is a record's; they are how the "
            "layer is DRAWN, the division the enclosure layer makes between a "
            "fence's line and a rail's thickness."
        ),
    }
    rec["rule"] = {
        "note": (
            "A wall gets a walk iff a street centreline lies OUTWARD of it within "
            f"{STREET_REACH_M:.0f} m, lies IN FRONT of it rather than beside it "
            f"({FRONTAGE_DOMINANCE:.0%} of the distance to it standing outward), and "
            "the walk's outer edge still clears that "
            "street's own travelled track; a crossing springs from the walk on the "
            "wall the building fronts on and runs until it is past the far edge of "
            "the track; " + cfg["rule_mid"] + "Every wall that is "
            "refused says which test refused it. Read the clauses and their "
            "reasons in tools/generate_frontage_works.py."
        ),
        "street_reach_m": STREET_REACH_M,
    }
    rec["walks"] = walks
    rec["posts"] = posts
    rec["refused"] = refused
    rec["research_note"] = cfg["research_note"]
    return rec


# ---------------------------------------------------------------------------- #
# THE RIVER PLANK WALK (T-0119) — the crossing footway at the slough mouth and
# the riverside walk along the south bank towards town.
# ---------------------------------------------------------------------------- #

def _heightfield():
    """The committed heightfield, imported lazily so the two building records
    can still regenerate on a checkout with no terrain epoch."""
    from heightfield import Heightfield  # tools/ is this script's own directory
    hf = Heightfield.load(EPOCH)
    if hf is None:
        raise SystemExit("generate_frontage_works: no committed heightfield at "
                         f"{EPOCH} — the river walk cannot be audited, so it is "
                         "not written")
    return hf


def _polyline_stations(line, pitch=PLANK_PITCH_M):
    """Every board centre along a polyline, the same march frontage.js makes."""
    out = []
    for i in range(len(line) - 1):
        (ax, ay), (bx, by) = line[i], line[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        n = max(1, round(seg / pitch))
        step = seg / n
        for j in range(n):
            t = (j + 0.5) * step / seg
            out.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    return out


def _n_on_path(path, e):
    """The path's own N at easting `e`, linearly interpolated (South Water runs
    monotonically in E through the whole reach this walk threads)."""
    for i in range(len(path) - 1):
        (e0, n0), (e1, n1) = path[i], path[i + 1]
        if min(e0, e1) <= e <= max(e0, e1) and e0 != e1:
            return n0 + (n1 - n0) * (e - e0) / (e1 - e0)
    return None


def _e_on_path(path, n):
    """The path's own E at northing `n` — Dearborn runs south-north."""
    for i in range(len(path) - 1):
        (e0, n0), (e1, n1) = path[i], path[i + 1]
        if min(n0, n1) <= n <= max(n0, n1) and n0 != n1:
            return e0 + (e1 - e0) * (n - n0) / (n1 - n0)
    return None


def _audit_river_reach(name, line, hf, streets, problems):
    """Every board station on dry committed ground, clear of the travelled way.

    This is the walk's own placement gate, run on every regeneration: the knots
    above are authored, and an authored coordinate nobody re-audits is a number
    somebody typed. A station under water or in the track refuses the RECORD,
    not just the board — the whole run is one claim.
    """
    sw = streets.get("south_water")
    hw = WALK_W_M / 2.0
    for (e, n) in _polyline_stations(line):
        g = hf.height(e, n)
        if g < RIVER_DRY_M:
            problems.append(f"{name}: board at ({e:.1f}, {n:.1f}) stands on ground at "
                            f"{g:+.2f} m — under or at the water, no walk is written")
        if sw:
            centre = _n_on_path(sw["path"], e)
            if centre is not None:
                edge = centre + sw["track_w"] / 2.0
                if n - hw < edge - 1e-9:
                    problems.append(f"{name}: board at ({e:.1f}, {n:.1f}) laps the "
                                    f"South Water track (edge N {edge:.2f}) — no walk "
                                    "is written")


def build_river_walk() -> tuple[list, list]:
    """The river plank walk's four runs, every fixed point read from the record
    that committed it, every authored knot audited against the committed ground."""
    problems: list[str] = []

    # THE CROSSING'S FIXED POINT: the Slough Log Bridge's committed deck. The
    # sidecar's placement is the same one the walker's deck registry reads, so
    # the footway and the surface a visitor stands on are one set of numbers.
    bridge = _load(SIDECARS / "slough_log_bridge.json")
    place = bridge.get("placement") or {}
    poly = (bridge.get("footprint") or {}).get("polygon") or []
    if place.get("vertical_anchor") != "water" or not isinstance(
            place.get("walk_surface_m"), (int, float)):
        raise SystemExit("generate_frontage_works: the Slough Log Bridge sidecar no "
                         "longer carries a water-anchored walk_surface_m — the "
                         "crossing footway has nothing to ride")
    if float(place.get("rotation_deg") or 0.0) != 0.0:
        raise SystemExit("generate_frontage_works: the Slough Log Bridge deck has "
                         "rotated — the footway derivation below assumes the "
                         "committed east-west deck and must be re-derived")
    deck_y = float(place["walk_surface_m"])          # a water anchor is datum zero
    e0 = float(place["local_e"])
    n0 = float(place["local_n"])
    deck_e0, deck_e1 = e0 + min(p[0] for p in poly), e0 + max(p[0] for p in poly)
    deck_n_mid = n0 + (min(p[1] for p in poly) + max(p[1] for p in poly)) / 2.0

    # THE RUN'S FAR END: Jones's landing, the easternmost wharf on the South
    # Water bank — where the town's wharf walks begin, so where this walk stops.
    wharves = _load(WHARVES)
    jones = next((w for w in wharves.get("wharves", [])
                  if w.get("structure_id") == "h_jones_store"), None)
    if jones is None:
        raise SystemExit("generate_frontage_works: h_jones_store no longer states a "
                         "wharf — the river walk's west terminus is gone and the "
                         "authored run must be re-bounded")
    foot = jones["bank_foot_local_enu_m"]
    end = RIVER_WHARF_REACH[-1]
    if math.hypot(end[0] - foot[0], end[1] - foot[1]) > 6.5:
        raise SystemExit("generate_frontage_works: the river walk's last knot is "
                         f"{math.hypot(end[0] - foot[0], end[1] - foot[1]):.1f} m from "
                         "Jones's landing — the wharf moved, re-author the run's end")

    streets = _streets()
    hf = _heightfield()

    # THE DEARBORN CROSSING'S FIXED LINE: the street's own committed centreline,
    # crossed square where the walk meets it, reaching past the travelled track
    # by the same margin every crossing this generator writes keeps.
    dearborn = streets["dearborn"]
    dcross_e = _e_on_path(dearborn["path"], RIVER_DEARBORN_CROSS_N)
    reach = dearborn["track_w"] / 2.0 + RIVER_CROSS_CLEAR_M
    cross_e_east = _round(dcross_e + reach)
    cross_e_west = _round(dcross_e - reach)

    footway_line = [[_round(deck_e0 - RIVER_APPROACH_M), _round(deck_n_mid)],
                    [_round(deck_e1 + RIVER_APPROACH_M), _round(deck_n_mid)]]
    span_hw = _round(WALK_W_M / 2.0 + RIVER_DECK_MARGIN_M)
    deck_span = [[_round(deck_e0), _round(deck_n_mid - span_hw)],
                 [_round(deck_e1), _round(deck_n_mid - span_hw)],
                 [_round(deck_e1), _round(deck_n_mid + span_hw)],
                 [_round(deck_e0), _round(deck_n_mid + span_hw)]]

    east_line = ([[_round(deck_e0 - RIVER_APPROACH_M), _round(deck_n_mid)]]
                 + [[_round(e), _round(n)] for e, n in RIVER_EAST_REACH]
                 + [[cross_e_east, RIVER_DEARBORN_CROSS_N]])
    west_line = ([[cross_e_west, RIVER_DEARBORN_CROSS_N]]
                 + [[_round(e), _round(n)] for e, n in RIVER_WEST_REACH])
    wharf_line = [[_round(e), _round(n)] for e, n in RIVER_WHARF_REACH]

    # The audits. The footway's own boards ride the committed deck, so only its
    # two approach ends are asked of the ground; every other board is.
    for e, n in footway_line:
        if hf.height(e, n) < RIVER_DRY_M:
            problems.append(f"{RIVER_WALK_ID}: the crossing footway's approach at "
                            f"({e:.1f}, {n:.1f}) stands on wet ground")
    _audit_river_reach(f"{RIVER_WALK_ID} east reach", east_line, hf, streets, problems)
    _audit_river_reach(f"{RIVER_WALK_ID} west reach", west_line, hf, streets, problems)
    _audit_river_reach(f"{RIVER_WALK_ID} wharf reach", wharf_line, hf, streets, problems)
    # And the stated reason for the one break in the run must still be true: the
    # gap between the two reaches crosses the La Salle slough's traced mouth. If
    # this ground ever comes up dry, the refusal below is wrong and the walk
    # should be re-authored continuous.
    gap_mid_e = (west_line[-1][0] + wharf_line[0][0]) / 2.0
    gap_mid_n = (west_line[-1][1] + wharf_line[0][1]) / 2.0
    if hf.height(gap_mid_e, gap_mid_n) >= 0.0:
        problems.append(f"{RIVER_WALK_ID}: the La Salle mouth gap at ({gap_mid_e:.1f}, "
                        f"{gap_mid_n:.1f}) is dry ground — the stated refusal no "
                        "longer holds, re-author the run continuous")
    if problems:
        raise SystemExit("generate_frontage_works: the river walk failed its own "
                         "placement audit:\n  - " + "\n  - ".join(problems))

    liberty = "L153"
    walks = [
        {
            "id": f"{RIVER_WALK_ID}_crossing_footway",
            "belongs_to": RIVER_WALK_ID,
            "kind": "plank_walk",
            "confidence": "reconstructed",
            "rides": "slough_log_bridge",
            "centreline_local_enu_m": footway_line,
            "width_m": WALK_W_M,
            "rise_m": WALK_RISE_M,
            "plank_run": "across",
            "plank_pitch_m": PLANK_PITCH_M,
            "plank_thickness_m": PLANK_T_M,
            "deck_m": _round(deck_y),
            "deck_span_local_enu_m": deck_span,
            "note": (
                "THE PLANK FOOTWAY OVER THE SLOUGH MOUTH — what a person walking "
                "Water Street actually crosses the drain on. The Slough Log Bridge "
                "is the committed structure (its record carries the crossing's "
                "evidence); this footway is the pedestrian surface the owner asked "
                "for on 2026-08-20, laid along the deck's own centre. WHERE is "
                "derived, not authored: the run is the committed deck's extent "
                f"(E {deck_e0:.1f}..{deck_e1:.1f}) plus {RIVER_APPROACH_M} m onto "
                "each graded approach, and `deck_m` is the deck surface the sidecar "
                "already states (`walk_surface_m` over a water anchor), so the "
                "boards ride the same number the walker's deck registry reads. Over "
                "the carved channel the boards lie on the deck; on the approaches "
                "they take the ground, exactly as every other walk this layer "
                f"lays. docs/LIBERTIES.md {liberty}."
            ),
        },
        {
            "id": f"{RIVER_WALK_ID}_east_reach",
            "belongs_to": RIVER_WALK_ID,
            "kind": "plank_walk",
            "confidence": "reconstructed",
            "centreline_local_enu_m": east_line,
            "width_m": WALK_W_M,
            "rise_m": WALK_RISE_M,
            "plank_run": "across",
            "plank_pitch_m": PLANK_PITCH_M,
            "plank_thickness_m": PLANK_T_M,
            "note": (
                "THE RIVERSIDE WALK'S FIRST REACH, from the crossing footway's west "
                "end along the south bank to the Dearborn Street crossing. The line "
                "threads the verge between the South Water track's own edge and the "
                "traced waterline, and every board station is audited against both "
                "on every regeneration — dry committed ground under the deck, the "
                "travelled way clear beside it. The knots between the two fixed "
                f"ends are invented: docs/LIBERTIES.md {liberty}."
            ),
        },
        {
            "id": f"{RIVER_WALK_ID}_dearborn_crossing",
            "belongs_to": RIVER_WALK_ID,
            "kind": "board_crossing",
            "confidence": "reconstructed",
            "street": "dearborn",
            "street_name": dearborn["name"],
            "centreline_local_enu_m": [[cross_e_east, RIVER_DEARBORN_CROSS_N],
                                       [cross_e_west, RIVER_DEARBORN_CROSS_N]],
            "width_m": CROSSING_W_M,
            "rise_m": _round(WALK_RISE_M / 2.0),
            "plank_run": "along",
            "plank_count": CROSSING_PLANKS,
            "plank_thickness_m": PLANK_T_M,
            "run_m": _round(2 * reach),
            "note": (
                "A BOARD CROSSING OVER DEARBORN STREET, where the riverside walk "
                "crosses the drawbridge's graded approach. WHERE is derived: the "
                "crossing sits square on Dearborn's committed centreline at "
                f"E {dcross_e:.2f} and runs {2 * reach:.1f} m — the {dearborn['track_w']} m "
                f"track plus {RIVER_CROSS_CLEAR_M} m of dry ground each side — and "
                "its boards run the way the foot travels, up and over the approach "
                "fill, because a crossing spans the ruts instead of lying in them. "
                f"Every dimension is the layer's own. docs/LIBERTIES.md {liberty}."
            ),
        },
        {
            "id": f"{RIVER_WALK_ID}_west_reach",
            "belongs_to": RIVER_WALK_ID,
            "kind": "plank_walk",
            "confidence": "reconstructed",
            "centreline_local_enu_m": west_line,
            "width_m": WALK_W_M,
            "rise_m": WALK_RISE_M,
            "plank_run": "across",
            "plank_pitch_m": PLANK_PITCH_M,
            "plank_thickness_m": PLANK_T_M,
            "note": (
                "THE RIVERSIDE WALK'S SECOND REACH, from the Dearborn crossing west "
                "along the bank to the La Salle slough's traced mouth, where the "
                "bank itself is interrupted (see `refused`). The verge pinches "
                "where the bank crowds the street — near E +667 the walk holds a "
                "hand's width off the track edge with the water at its outer "
                "boards — and every station is audited for both on every "
                f"regeneration. The knots are invented: docs/LIBERTIES.md {liberty}."
            ),
        },
        {
            "id": f"{RIVER_WALK_ID}_wharf_reach",
            "belongs_to": RIVER_WALK_ID,
            "kind": "plank_walk",
            "confidence": "reconstructed",
            "centreline_local_enu_m": wharf_line,
            "width_m": WALK_W_M,
            "rise_m": WALK_RISE_M,
            "plank_run": "across",
            "plank_pitch_m": PLANK_PITCH_M,
            "plank_thickness_m": PLANK_T_M,
            "note": (
                "THE RIVERSIDE WALK'S LAST REACH, from the west lip of the La Salle "
                "mouth out along the swinging bank to Jones's landing — the "
                "easternmost wharf on the South Water bank, whose committed "
                "`bank_foot` this reach is audited to end within a landing's width "
                "of. That wharf is where the town's own riverfront walking surface "
                "begins, which is what bounds this run on the west. The knots are "
                f"invented: docs/LIBERTIES.md {liberty}."
            ),
        },
    ]
    walks.sort(key=lambda w: w["id"])
    refused = [
        {
            "structure_id": RIVER_WALK_ID,
            "wall": "the La Salle slough mouth (E +489 to +459)",
            "why": (
                "the La Salle slough's traced mouth re-entrant interrupts the bank "
                "between the walk's two western reaches, and no crossing is "
                "committed there — the street record itself says South Water "
                "'crossed on fill or a culvert nothing describes'. A plank span "
                "over that water would invent a structure, so no board is laid: "
                "the street's own unbroken fill carries the foot passenger between "
                "the reaches, and the gap is asserted to still be wet on every "
                "regeneration."
            ),
        },
    ]
    return walks, refused


def river_record(walks: list, refused: list) -> dict:
    total = 0.0
    for w in walks:
        line = w["centreline_local_enu_m"]
        for i in range(len(line) - 1):
            total += math.hypot(line[i + 1][0] - line[i][0], line[i + 1][1] - line[i][1])
    bounds_note = (
        "WHAT BOUNDED THE RUN, in one place: the crossing footway's extent is the "
        "Slough Log Bridge's committed deck plus its graded approaches; the walk's "
        "line is the verge between the South Water track's committed edge and the "
        "traced 1834 bank; the run breaks at the La Salle slough's traced mouth, "
        "where no crossing is committed and the street's own fill carries the foot "
        "passenger; and it ends at Jones's landing, the easternmost committed "
        "wharf, where the town's riverfront walking surface begins. Everything "
        "between those pins is invented and audited: docs/LIBERTIES.md L153."
    )
    return {
        "_doc": (
            "The river plank walk (T-0119) — the plank footway over the State "
            "Street slough's mouth on the Slough Log Bridge's committed deck, and "
            "the riverside walk that carries on from it along the south bank of "
            "the main stem towards town, ending at Jones's landing where the "
            "committed wharves begin. NOT a structure record and NOT baked "
            "geometry: boards laid on ground and on a deck this project has "
            "already built, drawn at load by renderers/web/js/frontage.js. "
            "Generated by tools/generate_frontage_works.py and re-derived byte "
            "for byte by tools/check.sh; the generator audits every board "
            "station against the committed heightfield and the committed street "
            "before it will write this file."
        ),
        "id": "river_walk_frontage",
        "name": ("The river plank walk: the footway over the slough mouth, and "
                 "the riverside walk to Jones's landing"),
        "kind": "frontage",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same "
            "frame data/signage/, data/yard/ and the sidecars' placement.local_e "
            "/ placement.local_n use."
        ),
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": [],
            "note": (
                "NO SOURCE RECORD IN THIS REPOSITORY STATES THAT A PLANK FOOTWAY "
                "CROSSED THE SLOUGH MOUTH OR THAT A WALK RAN ALONG THE BANK ON "
                "1 JULY 1835. What is held: the crossing itself is documented — "
                "the Slough Log Bridge's record carries 'where Water Street "
                "crossed it a log bridge was needed until after 1840' — and the "
                "owner asked for the pedestrian surface and the riverside run in "
                "as many words on 2026-08-20, under the standing 2026-08-18 "
                "ruling that reconstructed items may be added liberally so long "
                "as they are labelled. This walk is that: a reconstruction in "
                "the project's third tier, graded and claimed as one at "
                "docs/LIBERTIES.md L153, with every invented coordinate audited "
                "against the committed ground it is laid on."
            ),
        },
        "treatment": {
            "confidence": "reconstructed",
            "note": (
                f"Walk {WALK_W_M} m wide, its deck {WALK_RISE_M} m over the "
                f"ground, {PLANK_T_M} m boards at a {PLANK_PITCH_M} m pitch laid "
                "ACROSS the way a foot travels — the same drawn treatment as "
                "every walk this layer lays. Over the bridge deck the boards "
                "ride the committed `walk_surface_m` and the stringers are "
                "omitted (boards on a deck lie on the deck); everywhere else "
                "each board samples the terrain under its own centre. The "
                f"Dearborn crossing is {CROSSING_W_M} m wide, {CROSSING_PLANKS} "
                "boards laid ALONG the run. Not one of these numbers is a "
                "record's; they are how the layer is DRAWN."
            ),
        },
        "rule": {
            "note": (
                "The river walk's fixed points are committed records — the "
                "bridge deck, the Dearborn centreline, Jones's landing — and its "
                "authored knots are audited on every regeneration: every board "
                "station must stand on committed ground above the water "
                f"({RIVER_DRY_M} m over datum) and clear the South Water track's "
                "own edge, the crossing must span Dearborn's track with "
                f"{RIVER_CROSS_CLEAR_M} m to spare each side, the run must end "
                "within a landing's width of Jones's committed bank foot, and "
                "the one gap in the run must still be wet. Any of those failing "
                "refuses the whole record. Read the clauses in "
                "tools/generate_frontage_works.py."
            ),
        },
        "card": {
            "id": RIVER_WALK_ID,
            "name": "The river plank walk",
            "symbolic_location": (
                "Along the south bank of the main stem: over the State Street "
                "slough's mouth on the Slough Log Bridge, then west along the "
                "Water Street verge to Jones's landing."
            ),
            "position_note": bounds_note,
            "attributes": {
                "existence": {
                    "value": True,
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": (
                        "Asked for by the owner at the slough mouth, 2026-08-20: "
                        "'the pedestrian plank sidewalk bridge crossing it close "
                        "to the river should exist and run along the river "
                        "towards the town.' No 1835 source describes a walk on "
                        "this bank; the crossing it rides is the documented "
                        "Slough Log Bridge."
                    ),
                },
                "run_m": {
                    "value": _round(total, 1),
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": (
                        "The whole run, crossing footway and Dearborn boards "
                        "included, bounded by the bridge's committed deck ends "
                        "and Jones's committed landing — nothing measured, "
                        "everything derived or invented and audited."
                    ),
                },
                "width_m": {
                    "value": WALK_W_M,
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": "Six feet — two people passing; the layer's own drawn width.",
                },
                "crossing_deck_m": {
                    "value": 0.83,
                    "confidence": "inferred",
                    "sources": [],
                    "note": (
                        "The Slough Log Bridge's own committed walk_surface_m, "
                        "carried, not claimed: the boards over the water ride "
                        "the deck the bridge record already states."
                    ),
                },
            },
            "research_note": (
                "A walk from data/frontage/ — not a structure record. " + bounds_note
                + " What would move it off reconstruction: a Chicago town order "
                "on sidewalks of the right date; any tax, insurance or sale "
                "description naming a walk on the Water Street bank; or a view "
                "of the slough mouth showing what the crossing's walking "
                "surface actually was."
            ),
        },
        "walks": walks,
        "posts": [],
        "refused": refused,
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: a Chicago town "
            "order on sidewalks — the corporation legislated wooden walks "
            "within a few years of 1835; a grading or wharfing order for Water "
            "Street east of Dearborn; any view of the slough mouth or the South "
            "Water bank showing the crossing's surface or a bank walk; or a "
            "committed crossing at the La Salle mouth, which would close the "
            "one gap in the run."
        ),
    }


# ---------------------------------------------------------------------------- #
# THE TOWN'S STREET EDGE (T-0069) — plank sidewalks at the lot line, board
# crossings at the corners, and the fences that line the street behind them.
#
# Everything below is derived from two committed things and nothing else: the
# platted block grid (whose every face is a committed street centreline offset by
# half the committed corridor) and the committed footprints standing on it. The
# march is the whole rule — a face is walked in EDGE_SPAN_M steps, each step is
# asked four questions, and the steps that answer them become the walk. A step
# that fails says which question failed it, and the answer is written into the
# record's `refused` rather than quietly skipped.
# ---------------------------------------------------------------------------- #


def _lots() -> dict:
    return _load(LOTS)


def _placed_footprints() -> list[dict]:
    """Every committed footprint in the scene, placed into local ENU.

    Read once and carried as a centre + radius + polygon, because the march below
    asks "is a wall standing on this board" thousands of times and all but a
    handful of those questions are answered by one squared distance.
    """
    out = []
    for path in sorted(SIDECARS.glob("*.json")):
        sc = _load(path)
        place = sc.get("placement") or {}
        poly = (sc.get("footprint") or {}).get("polygon") or []
        if place.get("local_e") is None or len(poly) < 3:
            continue
        pts = [_to_enu(u, v, place) for u, v in poly]
        ce = sum(p[0] for p in pts) / len(pts)
        cn = sum(p[1] for p in pts) / len(pts)
        r = max(math.hypot(p[0] - ce, p[1] - cn) for p in pts)
        out.append({"id": sc.get("id") or path.stem, "pts": pts,
                    "e": ce, "n": cn, "r": r,
                    "at": (float(place["local_e"]), float(place["local_n"]))})
    return out


def _inside(pt, poly) -> bool:
    """Point in polygon, local ENU. The same ray cast every other tool here uses."""
    x, y = pt
    hit = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


def _wall_on(point, half_w, outward, buildings) -> str | None:
    """The committed building standing where a board of this width would lie, or None.

    Three probes across the deck — both edges and the centre — because a wall that
    clips the outer half of a walk is as much in the way as one that covers it,
    and a board is only 1.83 m wide.
    """
    for b in buildings:
        if (b["e"] - point[0]) ** 2 + (b["n"] - point[1]) ** 2 > (b["r"] + half_w + 1.0) ** 2:
            continue
        for off in (-half_w, 0.0, half_w):
            probe = (point[0] + outward[0] * off, point[1] + outward[1] * off)
            if _inside(probe, b["pts"]):
                return b["id"]
    return None


def _march(frame, offset_m, half_w, hf, buildings, span_m=EDGE_SPAN_M):
    """Walk a block face in EDGE_SPAN_M steps and ask each step whether a walk may
    be laid on it. Returns (spans, why) — one entry per step.

    The four questions, and each is a way a plank sidewalk goes wrong:

      * **Is the ground there at all?** A step outside the committed heightfield
        has nothing to lay a board on.
      * **Is it dry?** The La Salle and State Street sloughs cross these
        frontages, and a board over open water is a bridge nobody committed.
      * **Is it flat enough to be ONE walking surface?** The walker stands on a
        registered deck at one height per span (see `footway_decks` below), so a
        span whose ground rolls by more than EDGE_FLAT_M would leave a visitor
        floating over its low end. Where the land rolls, the walk breaks.
      * **Is anything already standing on it?** Several documented South Water
        stores were placed off the modern kerb rather than off this project's
        platted line and stand out past it. A walk laid through one of them
        would be a walk through a wall.
    """
    origin = frame["origin"]
    along = frame["along"]
    outward = frame["outward"]
    length = frame["length"]
    steps = max(1, round(length / span_m))
    step = length / steps
    # THREE LINES, not one. The deck is 1.83 m wide and its stringers stand on
    # its own edges, so a step is sampled on the walk's centre AND on the two
    # lines the timber actually reaches the ground on. A centreline-only march
    # would call a cross-sloped verge flat and leave the downhill stringer
    # hanging.
    stringer = half_w - 0.09
    lines = (0.0, -stringer, stringer)
    spans = []
    for i in range(steps):
        lo = i * step
        hi = lo + step
        blocked = None
        stations = max(2, int(round(step / PLANK_PITCH_M)))
        by_line = [[] for _ in lines]
        for j in range(stations + 1):
            t = lo + (hi - lo) * j / stations
            pt = (origin[0] + along[0] * t + outward[0] * offset_m,
                  origin[1] + along[1] * t + outward[1] * offset_m)
            for k, off in enumerate(lines):
                by_line[k].append(hf.height(pt[0] + outward[0] * off,
                                            pt[1] + outward[1] * off))
            if blocked is None:
                blocked = _wall_on(pt, half_w, outward, buildings)
        heights = [h for line in by_line for h in line]
        low = min(heights)
        high = max(heights)
        # The stringer bay's own question, and it is the one that decides
        # whether a bay-length stringer may replace a board-length pair: a box
        # has a flat underside, so it reaches the LOWEST ground it spans and
        # stands proud of the highest by the difference. Asked per stringer line
        # over every window one bay long.
        bay_stations = max(1, int(round(EDGE_STRINGER_PITCH_M / (step / stations))))
        roll = 0.0
        for line in by_line[1:]:
            for a in range(0, max(1, len(line) - bay_stations)):
                window = line[a:a + bay_stations + 1]
                roll = max(roll, max(window) - min(window))
        if blocked:
            why = f"{blocked} stands on it"
        elif low < EDGE_DRY_M:
            why = f"the ground under it is {low:+.2f} m — at or under the water"
        elif high - low > EDGE_FLAT_M:
            why = (f"the ground under it rolls {high - low:.2f} m, past the "
                   f"{EDGE_FLAT_M} m one walking deck may carry")
        elif roll > EDGE_STRINGER_ROLL_M:
            why = (f"the ground under one stringer bay rolls {roll:.3f} m, past the "
                   f"{EDGE_STRINGER_ROLL_M} m a bay-length stringer may span")
        else:
            why = None
        spans.append({"lo": lo, "hi": hi, "low": low, "high": high,
                      "roll": roll, "why": why})
    return spans


def _runs_from(spans):
    """Consecutive laid steps, grouped into runs no shorter than EDGE_MIN_RUN_M."""
    runs = []
    start = None
    for i, sp in enumerate(spans):
        if sp["why"] is None and start is None:
            start = i
        if sp["why"] is not None and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(spans)))
    return [(a, b) for a, b in runs if spans[b - 1]["hi"] - spans[a]["lo"] >= EDGE_MIN_RUN_M]


def _decks(spans, a, b, frame, offset_m, half_w, rise_m):
    """The walking surfaces a run publishes to the walker.

    T-0045 gave this project a deck registry and T-0119 put a plank walk on it;
    this is the same machinery at town scale. A deck is FLAT — one height over one
    rectangle — so the run is cut into the longest pieces whose ground stays
    inside EDGE_FLAT_M, and each piece takes the HIGHEST ground under it plus the
    walk's own rise. Highest and not mean: the walker's rule is
    `max(deck, ground)`, so a deck under the ground at any point would drop the
    visitor off its planks onto the mud in the middle of a sidewalk.
    """
    origin = frame["origin"]
    along = frame["along"]
    outward = frame["outward"]
    out = []
    i = a
    while i < b:
        j = i + 1
        low = spans[i]["low"]
        high = spans[i]["high"]
        while j < b:
            nlow = min(low, spans[j]["low"])
            nhigh = max(high, spans[j]["high"])
            if nhigh - nlow > EDGE_FLAT_M:
                break
            if spans[j]["hi"] - spans[i]["lo"] > EDGE_DECK_MAX_M:
                break
            low, high = nlow, nhigh
            j += 1
        lo = spans[i]["lo"] - EDGE_DECK_LAP_M
        hi = spans[j - 1]["hi"] + EDGE_DECK_LAP_M
        pts = []
        for t, s in ((lo, -1), (hi, -1), (hi, 1), (lo, 1)):
            e = origin[0] + along[0] * t + outward[0] * (offset_m + s * half_w)
            n = origin[1] + along[1] * t + outward[1] * (offset_m + s * half_w)
            pts.append([_round(e), _round(n)])
        out.append({"y": _round(high + rise_m, 3), "pts": pts,
                    "ground_roll_m": _round(high - low, 3)})
        i = j
    return out


def _point_on(frame, t, offset_m):
    return (frame["origin"][0] + frame["along"][0] * t + frame["outward"][0] * offset_m,
            frame["origin"][1] + frame["along"][1] * t + frame["outward"][1] * offset_m)


def _track_verge(frame, offset_m, half_w, streets, street_id) -> float:
    """Least distance from the walk's outer edge to the travelled track's edge,
    measured against the street's own committed centreline rather than assumed
    from the corridor. A walk in the travelled way is the one thing this layer
    has refused since T-0082, and the plat's own offset is not a substitute for
    asking."""
    st = streets.get(street_id)
    if not st or len(st["path"]) < 2:
        return -1.0
    worst = float("inf")
    steps = max(2, int(frame["length"] / 4.0))
    for i in range(steps + 1):
        t = frame["length"] * i / steps
        edge = _point_on(frame, t, offset_m + half_w)
        d, _ = _nearest_on_path(edge, st["path"])
        worst = min(worst, d - st["track_w"] / 2.0)
    return worst


def _edge_faces(lots_doc):
    """Every platted block face that fronts one of the two covered streets, with
    its committed frame. The faces are the plat's, and the plat's are the street
    network's: `tools/generate_plat_lots.py` builds every one of these edges by
    offsetting a committed centreline out of `data/streets/1835.json`."""
    out = []
    for block in lots_doc.get("blocks", []):
        if block["id"] in EDGE_SKIP_BLOCKS:
            continue
        bounded = block.get("bounded_by") or {}
        for face in ("north", "south"):
            street = bounded.get(face)
            if street not in EDGE_STREETS:
                continue
            frame = face_frame(block, face)
            # The block lies south of a street it bounds on its NORTH face, so
            # that face stands on the street's SOUTH side, and the other way
            # round. The side is what pairs two faces across the same road.
            out.append({
                "block": block, "face": face, "street": street,
                "side": "south" if face == "north" else "north",
                "frame": frame,
            })
    out.sort(key=lambda f: (f["street"], f["side"], f["frame"]["origin"][0]))
    return out


def _fence_runs(entry, laid, buildings, hf, refused):
    """The street-lining fences on one face: one run per stretch of improved lots
    whose own walls stand back from the frontage line.

    THE RULE, and each clause is the engraving read literally. A lot gets a
    street fence iff (1) it is one of the plat's own lots on this face, (2) a
    committed building stands on it — an unimproved lot is prairie and the town
    did not fence prairie, (3) that building is NOT built out to the frontage
    line, because where it is the BUILDING is the street wall and a fence in
    front of it would be a second one, and (4) the walk was actually laid at its
    foot, which is what the plate shows and what keeps a fence off ground this
    generator has already refused as wet, rolling or occupied.
    """
    frame = entry["frame"]
    block = entry["block"]
    face = entry["face"]
    runs = []
    for index, lot in enumerate(block.get("lots", [])):
        if lot.get("tier") != face:
            continue
        spans = [project(frame, tuple(p)) for p in lot["polygon"]]
        s0 = min(s for s, _ in spans)
        s1 = max(s for s, _ in spans)
        here = [b for b in buildings if _inside(b["at"], lot["polygon"])]
        if not here:
            refused.append({"structure_id": f"{block['id']}_lot{index}",
                            "wall": f"{block['id']} {face} face, lot {index}",
                            "why": ("no committed building stands on this platted lot — an "
                                    "unimproved lot is open prairie and takes no street "
                                    "fence.")})
            continue
        setback = min(-project(frame, p)[1] for b in here for p in b["pts"])
        if setback < EDGE_FENCE_SETBACK_M:
            refused.append({"structure_id": f"{block['id']}_lot{index}",
                            "wall": f"{block['id']} {face} face, lot {index}",
                            "why": (f"{here[0]['id']} stands {setback:.2f} m from this lot's "
                                    f"frontage line, inside the {EDGE_FENCE_SETBACK_M} m a "
                                    "street fence needs — the building IS the street wall "
                                    "here, and a fence in front of it would be a second "
                                    "one.")})
            continue
        # Clipped to the walk actually laid at its foot, then only the part of
        # that clip which is long enough to be a fence rather than a gatepost.
        for lo, hi in laid:
            a = max(s0, lo)
            b = min(s1, hi)
            if b - a < 6.0:
                continue
            runs.append({"a": a, "b": b, "lot": index, "chunk": None,
                         "setback": setback, "who": here[0]["id"]})
    # Neighbouring lots share a fence line, so their runs are welded into one
    # rather than drawn as two fences that meet at a post nobody described.
    runs.sort(key=lambda r: r["a"])
    welded = []
    for r in runs:
        if welded and r["a"] - welded[-1]["b"] < 0.5:
            welded[-1]["b"] = max(welded[-1]["b"], r["b"])
            welded[-1]["lots"].append(r["lot"])
            welded[-1]["setback"] = min(welded[-1]["setback"], r["setback"])
            continue
        welded.append({"a": r["a"], "b": r["b"], "lots": [r["lot"]],
                       "setback": r["setback"]})
    return welded


def build_street_edge() -> tuple[list, list, list, dict]:
    """The town's street edge: the walks, the corner crossings, the street-lining
    fences, and every refusal that shaped them."""
    hf = _heightfield()
    streets = _streets()
    lots_doc = _lots()
    buildings = _placed_footprints()
    faces = _edge_faces(lots_doc)
    half_w = WALK_W_M / 2.0

    walks: list = []
    fences: list = []
    refused: list = []
    laid_by_face: dict = {}
    census = {"faces": 0, "runs": 0, "walk_m": 0.0, "crossings": 0, "cross_m": 0.0,
              "fences": 0, "fence_m": 0.0, "decks": 0}

    for entry in faces:
        block = entry["block"]
        face = entry["face"]
        frame = entry["frame"]
        street = entry["street"]
        name = streets[street]["name"]
        key = f"{block['id']}_{face}"
        verge = _track_verge(frame, EDGE_OFFSET_M, half_w, streets, street)
        if verge < EDGE_TRACK_MARGIN_M:
            refused.append({"structure_id": key, "wall": f"{block['id']} {face} face", "why": (
                f"a walk at this face's lot line would leave {verge:.2f} m between its "
                f"outer edge and the {name} track, under the {EDGE_TRACK_MARGIN_M} m a "
                "walk must keep out of the travelled way — no walk is laid.")})
            continue
        spans = _march(frame, EDGE_OFFSET_M, half_w, hf, buildings)
        runs = _runs_from(spans)
        if not runs:
            worst = spans[0]["why"] if spans else "the face has no length"
            refused.append({"structure_id": key, "wall": f"{block['id']} {face} face", "why": (
                f"no stretch of this face {EDGE_MIN_RUN_M:.1f} m long passed the march "
                f"(first refusal: {worst}) — no walk is laid.")})
            continue
        census["faces"] += 1
        laid = []
        for k, (a, b) in enumerate(runs, start=1):
            lo = spans[a]["lo"]
            hi = spans[b - 1]["hi"]
            laid.append((lo, hi))
            # One mesh per run, named on the record rather than decided in the
            # renderer: "which timber shares a bounding sphere" is a property of
            # the ground it stands on, and the record is what holds the ground.
            chunk = f"{key}_{k}"
            start = _point_on(frame, lo, EDGE_OFFSET_M)
            end = _point_on(frame, hi, EDGE_OFFSET_M)
            decks = _decks(spans, a, b, frame, EDGE_OFFSET_M, half_w, WALK_RISE_M)
            census["runs"] += 1
            census["walk_m"] += hi - lo
            census["decks"] += len(decks)
            walks.append({
                "id": f"{key}_walk_{k}",
                "belongs_to": STREET_EDGE_ID,
                "kind": "plank_walk",
                "confidence": "reconstructed",
                "street": street,
                "street_name": name,
                "chunk": chunk,
                "centreline_local_enu_m": [[_round(start[0]), _round(start[1])],
                                           [_round(end[0]), _round(end[1])]],
                "width_m": WALK_W_M,
                "rise_m": WALK_RISE_M,
                "plank_run": "across",
                "plank_pitch_m": EDGE_PLANK_PITCH_M,
                "plank_thickness_m": PLANK_T_M,
                "plank_underside": EDGE_PLANK_UNDERSIDE,
                "stringer_pitch_m": EDGE_STRINGER_PITCH_M,
                "lot_line_offset_m": _round(EDGE_OFFSET_M),
                "verge_to_track_m": _round(verge),
                "footway_decks": decks,
                "note": (
                    f"THE PLANK SIDEWALK ON THE {name.upper()} FRONTAGE of "
                    f"{block['id']}'s {face} face, at the lot line. WHERE is DERIVED and "
                    "nothing here is placed: the face is a committed street centreline "
                    "offset by half the committed 80 ft corridor "
                    "(data/traces/vectors/thompson_lots.json, re-derived by "
                    "tools/generate_plat_lots.py), and the walk's centre lies "
                    f"{EDGE_OFFSET_M:.3f} m outward of it — {EDGE_FENCE_CLEAR_M} m of "
                    "daylight off the fence line and half a walk's width — leaving "
                    f"{verge:.2f} m of verge between its outer edge and the {name} track. "
                    f"This run is the stretch from {lo:.1f} m to {hi:.1f} m along the "
                    "face that passed the march: dry committed ground, flat enough for "
                    "one walking deck, and nothing already standing on it. What is "
                    "invented is the width, the rise, the plank pitch and that a walk "
                    "stood on this ground at noon on 1 July 1835: docs/LIBERTIES.md "
                    f"{STREET_EDGE_LIBERTY}."
                ),
            })
        laid_by_face[key] = {"entry": entry, "laid": laid, "verge": verge,
                             "chunks": [f"{key}_{k}" for k in range(1, len(runs) + 1)]}
        for run in _fence_runs(entry, laid, buildings, hf, refused):
            a = run["a"]
            b = run["b"]
            chunk = None
            for k, (lo, hi) in enumerate(laid, start=1):
                if a >= lo - 1e-6 and b <= hi + 1e-6:
                    chunk = f"{key}_{k}"
            if chunk is None:
                continue
            p0 = _point_on(frame, a, 0.0)
            p1 = _point_on(frame, b, 0.0)
            census["fences"] += 1
            census["fence_m"] += b - a
            fences.append({
                "id": f"{key}_fence_{len(fences) + 1}",
                "belongs_to": STREET_EDGE_ID,
                "kind": "board_fence",
                "confidence": "reconstructed",
                "street": street,
                "street_name": name,
                "chunk": chunk,
                "path_local_enu_m": [[_round(p0[0]), _round(p0[1])],
                                     [_round(p1[0]), _round(p1[1])]],
                "height_m": EDGE_FENCE_H_M,
                "board_width_m": EDGE_FENCE_BOARD_W_M,
                "board_gap_m": EDGE_FENCE_BOARD_GAP_M,
                "post_spacing_m": EDGE_FENCE_POST_SPACING_M,
                "post_square_m": EDGE_FENCE_POST_SQ_M,
                "rail_courses": EDGE_FENCE_COURSES,
                "lots": run["lots"],
                "least_setback_m": _round(run["setback"]),
                "note": (
                    "A FENCE LINING THE STREET, on the lot line with the plank walk at "
                    "its foot — which is the first Cook County jail engraving read "
                    "literally (data/sources/assets/owner_brief_2026_08_18/README.md, "
                    "image 1: board fences at the frontage line, a plank walk beside "
                    f"them). WHERE is derived: it stands on {block['id']}'s own platted "
                    f"frontage line from {a:.1f} m to {b:.1f} m along the {face} face, "
                    f"covering lot(s) {', '.join(str(i) for i in run['lots'])} — every "
                    "one of them improved by a committed building whose nearest wall "
                    f"stands {run['setback']:.2f} m back from that line, which is the "
                    "clause that decides a fence is what lines the street here rather "
                    "than a wall. The board width, the gap, the bay, the post and the "
                    "height are the treatment the plate shows and no source gives: "
                    f"docs/LIBERTIES.md {STREET_EDGE_LIBERTY}."
                ),
            })

    # ---- the crossings ----------------------------------------------------- #
    # A crossing joins two walks, so every one below is derived from the two ends
    # it joins and from nothing else. Two kinds: over a CROSS street, where a walk
    # runs on down the same side of the same street past a corner; and over the
    # street ITSELF, where a walk faces another across the road — which is what
    # images 8 and 9 show at the Sauganash.
    def crossing(cid, a_pt, b_pt, street_id, chunk, why):
        st = streets[street_id]
        run = math.hypot(b_pt[0] - a_pt[0], b_pt[1] - a_pt[1])
        stations = max(2, int(round(run / PLANK_PITCH_M)))
        low = float("inf")
        high = -float("inf")
        for i in range(stations + 1):
            t = i / stations
            e = a_pt[0] + (b_pt[0] - a_pt[0]) * t
            n = a_pt[1] + (b_pt[1] - a_pt[1]) * t
            g = hf.height(e, n)
            low = min(low, g)
            high = max(high, g)
        if low < EDGE_DRY_M:
            refused.append({"structure_id": cid, "wall": f"crossing over {st['name']}",
                            "why": (f"the ground under it falls to {low:+.2f} m — at or "
                                    "under the water; no crossing is laid.")})
            return
        rise = _round(WALK_RISE_M / 2.0)
        # The crossing's own walking decks: the same flat-deck rule the walks
        # keep, cut straight out of the run because a crossing is one straight
        # line and its relief is measured end to end.
        decks = []
        pieces = max(1, math.ceil(run / EDGE_DECK_MAX_M))
        hw = EDGE_CROSS_W_M / 2.0
        ux = (b_pt[0] - a_pt[0]) / run
        un = (b_pt[1] - a_pt[1]) / run
        rolled = 0.0
        for p in range(pieces):
            t0 = run * p / pieces - EDGE_DECK_LAP_M
            t1 = run * (p + 1) / pieces + EDGE_DECK_LAP_M
            plow = float("inf")
            phigh = -float("inf")
            for i in range(max(2, int((t1 - t0) / PLANK_PITCH_M)) + 1):
                t = t0 + (t1 - t0) * i / max(2, int((t1 - t0) / PLANK_PITCH_M))
                g = hf.height(a_pt[0] + ux * t, a_pt[1] + un * t)
                plow = min(plow, g)
                phigh = max(phigh, g)
            rolled = max(rolled, phigh - plow)
            pts = []
            for t, s in ((t0, -1), (t1, -1), (t1, 1), (t0, 1)):
                pts.append([_round(a_pt[0] + ux * t - un * s * hw),
                            _round(a_pt[1] + un * t + ux * s * hw)])
            decks.append({"y": _round(phigh + rise, 3), "pts": pts,
                          "ground_roll_m": _round(phigh - plow, 3)})
        if rolled > EDGE_FLAT_M * 2:
            refused.append({"structure_id": cid, "wall": f"crossing over {st['name']}",
                            "why": (f"the ground under it rolls {rolled:.2f} m inside one "
                                    "walking deck; no crossing is laid.")})
            return
        census["crossings"] += 1
        census["cross_m"] += run
        census["decks"] += len(decks)
        walks.append({
            "id": cid,
            "belongs_to": STREET_EDGE_ID,
            "kind": "board_crossing",
            "confidence": "reconstructed",
            "street": street_id,
            "street_name": st["name"],
            "chunk": chunk,
            "centreline_local_enu_m": [[_round(a_pt[0]), _round(a_pt[1])],
                                       [_round(b_pt[0]), _round(b_pt[1])]],
            "width_m": EDGE_CROSS_W_M,
            "rise_m": rise,
            "plank_run": "along",
            "plank_count": EDGE_CROSS_PLANKS,
            "plank_thickness_m": PLANK_T_M,
            "plank_underside": EDGE_PLANK_UNDERSIDE,
            "plank_step_m": EDGE_CROSS_STEP_M,
            "run_m": _round(run),
            "footway_decks": decks,
            "note": (
                f"A BOARD CROSSING OVER {st['name'].upper()}. {why} Its boards run the "
                "way a foot travels rather than across it, which is what a crossing is "
                "FOR — it spans the ruts instead of lying in them — and it lies lower "
                "than the walk because a wheel crosses it. WHERE is derived: the two "
                "ends are the two walks it joins, so the run is the corridor those "
                f"walks stop either side of, {run:.1f} m of it, and the crossing exists "
                "only where both of them were laid. docs/LIBERTIES.md "
                f"{STREET_EDGE_LIBERTY}."
            ),
        })

    # Along a side: consecutive faces on the same side of the same street, joined
    # over the cross street between them.
    sides: dict = {}
    for key, rec in laid_by_face.items():
        sides.setdefault((rec["entry"]["street"], rec["entry"]["side"]), []).append((key, rec))
    for (street, side), members in sorted(sides.items()):
        members.sort(key=lambda m: m[1]["entry"]["frame"]["origin"][0])
        for (ka, ra), (kb, rb) in zip(members, members[1:]):
            fa = ra["entry"]["frame"]
            fb = rb["entry"]["frame"]
            end = _point_on(fa, ra["laid"][-1][1], EDGE_OFFSET_M)
            start = _point_on(fb, rb["laid"][0][0], EDGE_OFFSET_M)
            gap = math.hypot(start[0] - end[0], start[1] - end[1])
            cid = f"{ka}_crossing_{kb}"
            if gap > 34.0:
                refused.append({"structure_id": cid, "wall": "corner crossing", "why": (
                    f"the two walks stop {gap:.1f} m apart, wider than the platted "
                    "corridor between them — the walk on one side was refused short of "
                    "its corner, so no crossing is laid.")})
                continue
            crossing(cid, end, start, street, ra["chunks"][-1],
                     "Images 6 and 8 give plank sidewalks WITH board crossings at the "
                     "town's two inns, so the fact is the plates' and every dimension "
                     "is invented.")
    # Across a street: the two sides of the same street, where a face on one is
    # opposite a face on the other.
    for street in EDGE_STREETS:
        north = sides.get((street, "north"), [])
        south = sides.get((street, "south"), [])
        for kn, rn in north:
            fn = rn["entry"]["frame"]
            n0 = fn["origin"][0]
            n1 = n0 + fn["length"]
            for ks, rs in south:
                fs = rs["entry"]["frame"]
                s0 = fs["origin"][0]
                s1 = s0 + fs["length"]
                overlap = min(n1, s1) - max(n0, s0)
                if overlap < 40.0:
                    continue
                # At the WEST end of the overlap, a few metres in: a crossing over
                # the road is at a corner, not in the middle of a block.
                at_e = max(n0, s0) + 4.0
                tn = at_e - n0
                ts = at_e - s0
                if not any(lo <= tn <= hi for lo, hi in rn["laid"]):
                    continue
                if not any(lo <= ts <= hi for lo, hi in rs["laid"]):
                    continue
                a_pt = _point_on(fn, tn, EDGE_OFFSET_M)
                b_pt = _point_on(fs, ts, EDGE_OFFSET_M)
                crossing(f"{kn}_crossing_over_{street}", a_pt, b_pt, street,
                         rn["chunks"][0],
                         "The Petford watercolour and the Braunhold engraving of the "
                         "Sauganash (images 8 and 9) both put a board crossing over the "
                         "road between walks on opposite frontages.")
                break

    # THE BOUNDARY, WRITTEN DOWN WHERE EVERY OTHER REFUSAL IS. A face this
    # generator never looked at leaves no trace of its own, so the two clauses
    # that bounded the run say so here rather than only in a comment.
    refused.append({
        "structure_id": "town_street_edge",
        "wall": ("Randolph Street, Washington Street and the cross streets' own "
                 "frontages"),
        "why": (
            "REFUSED ON A FRAME BUDGET, AND THE NUMBER IS HERE RATHER THAN A PROMISE "
            "(T-0127/T-0188). The owner's ask reaches further than this record does — "
            "'all of the streets should be updated like this' — and every one of these "
            "is the same rule on more platted faces, with no new argument in it. "
            "RANDOLPH WAS BUILT AND MEASURED RATHER THAN ESTIMATED: 13 more faces, "
            "+1,237.9 m of walk, +14 crossings, +14 fences. Published and read at the "
            "release gate's whole stand set, desktop, at the axial stand, it takes "
            "`full` from 1,378,984 to 1,497,588 against a 1,400,000 ceiling and "
            "`balanced` from 1,205,762 to 1,355,638 against 1,210,000 — over by 97,588 "
            "and 145,638, and the same shape on mobile. `light`, the tier a weak "
            "machine boots into, stays inside with 180,269 to spare. THE LEVER T-0115 "
            "COSTED FOR IT WAS TAKEN FIRST AND IS NOT ENOUGH: the plank walks no "
            "longer cast into the shadow map, and turning off every shadow caster this "
            "layer has left at that stand is worth a measured 44,110 triangles against "
            "that 145,638. AND THE BINDING FACT "
            "IS NOT RANDOLPH — `balanced` stood 4,238 triangles (0.35 %) inside its "
            "ceiling BEFORE this parcel, where T-0135 set it two days earlier with "
            "about 6 % of headroom, so no street tier of any size fits today. "
            "WASHINGTON adds 7 faces. THE CROSS STREETS (Market, Franklin, Wells, La "
            "Salle, Clark, Dearborn, State) are 34 platted faces and 3,562.8 m of walk "
            "— three times this whole record — and they also need a code change rather "
            "than only a name in `EDGE_STREETS`: `_edge_faces` enumerates a block's "
            "NORTH and SOUTH faces, and a cross street bounds its EAST and WEST ones. "
            "Until then a walker turning a corner still steps off the boards."
        ),
    })
    for sid, (out_m, block_id, lot, shift_m) in sorted(EDGE_UNRECONCILED.items()):
        refused.append({
            "structure_id": sid,
            "wall": "its own South Water frontage, unreconciled with the plat",
            "why": (
                f"REFUSED IN WRITING, PER STORE (T-0127). This building stands {out_m} m "
                f"OUT PAST {block_id}'s committed frontage line, in the platted roadway, "
                "because its coordinate was derived from the MODERN West Wacker Drive "
                "centreline rather than from this project's own committed South Water "
                "line — the record says so in its own position note. The walk is refused "
                "along the stretch it covers, which is why South Water's frontage still "
                f"comes out in pieces here. THE REPAIR IS MEASURED: {shift_m} m along the "
                "face's inward normal would put its north wall 1.50 m back from the line, "
                "the margin every reconstructed unit on this face keeps. IT WAS NOT "
                f"APPLIED, and the reason is nameable: reconciled, this building seats on "
                f"lot {lot} of {block_id}, which the 665-roof schedule has already dealt "
                "to the anonymous South Water frontage run, and "
                "tools/generate_block_infill.py refuses to deal a roof to a lot that "
                "already carries one. Re-scoring that block's headroom is a second piece "
                "of work; six of the eleven South Water placements were reconciled under "
                "T-0127 and these five wait on it."
            ),
        })
    refused.append({
        "structure_id": "blk_lake_clinton",
        "wall": "Lake Street's West Division frontage, across the South Branch",
        "why": (
            "this block stands in the WEST DIVISION, across the South Branch from "
            "the town the owner's 'south of the river or near the river' names, "
            "and it is separated from every other face on this record by a river "
            "with one bridge on it. The same rule would lay the same walk there; "
            "it belongs with the rest of the town in the follow-up ticket rather "
            "than as one stranded block."
        ),
    })
    walks.sort(key=lambda w: w["id"])
    fences.sort(key=lambda f: f["id"])
    refused.sort(key=lambda r: (r["structure_id"], r.get("wall", "")))
    census["walk_m"] = _round(census["walk_m"], 1)
    census["cross_m"] = _round(census["cross_m"], 1)
    census["fence_m"] = _round(census["fence_m"], 1)
    return walks, fences, refused, census


def street_edge_record(walks: list, fences: list, refused: list, census: dict) -> dict:
    bounds_note = (
        "WHAT BOUNDED THE RUN, in one place. The treatment is laid on the platted "
        "block faces that front THREE east-west streets of the South Division — "
        "SOUTH WATER STREET, which is the river bank itself; LAKE STREET one block "
        "behind it, both frontages; and RANDOLPH STREET one block behind that, both "
        "frontages — between Market Street and State Street. South Water and Lake are "
        "the owner's 'at least south of the river or near the river' and the town's "
        "trading core in 1835; Randolph is the first tier that is not on the river, "
        "added because 'all of the streets should be updated like this' does not stop "
        "at the bank. Every face is a committed street centreline offset by half the "
        "committed 80 ft corridor, so the line a walk lies on is the street network's "
        "and not this file's: move a centreline and every board here moves with it. "
        "Within that boundary the march decides, face by face and step by step — a "
        "stretch carries a walk where the ground is dry committed ground, flat enough "
        "for one walking deck, clear of the travelled track and clear of anything "
        "already standing on it — and `refused` says which clause refused every "
        "stretch that does not. THE SOUTH WATER FRONTAGES USED TO COME OUT IN PIECES, "
        "and the reason was a finding rather than a fault of this rule: eleven "
        "documented buildings on that side were placed against the MODERN kerb rather "
        "than against this project's own platted line and stood 4.5 to 8.2 m out past "
        "it, so the march refused the boards around every one of them. All eleven now "
        "stand on the plat — six reconciled under T-0188, the last five under T-0199, "
        "each translated along its own block face's inward normal until its north wall "
        "stood 1.50 m back from the committed frontage line, and no along-street "
        "position moved. What still refuses a stretch of this street is its own ground "
        "and the buildings that ARE the street wall, both named in `refused`. "
        "Randolph Street, Washington Street, the cross streets' own frontages and the "
        "West Division across the South Branch are the same rule on more faces. Every "
        "one of them was RUN THROUGH THIS RULE AND MEASURED before being refused — "
        "Randolph was built, published and read at the release gate's whole stand set "
        "— and `refused` carries the triangle counts that refused them rather than a "
        "promise."
    )
    return {
        "_doc": (
            "The town's street edge (T-0069) — the plank sidewalks at the lot line, "
            "the board crossings at the corners, and the board fences that line the "
            "street behind them, along South Water Street and Lake Street. NOT "
            "structure records and NOT baked geometry: boards and posts standing on "
            "ground this project has already built, drawn at load by "
            "renderers/web/js/frontage.js. GENERATED by "
            "tools/generate_frontage_works.py from the committed plat grid and the "
            "committed footprints, and re-derived byte for byte by tools/check.sh — "
            "because 'which stretch of which street carries a walk' is a rule and a "
            "rule has to be auditable. Nothing here is hand-placed on one block: move "
            "a street centreline in data/streets/1835.json and every walk, crossing "
            "and fence in this file moves with it."
        ),
        "id": STREET_EDGE_RECORD_ID,
        "name": ("The town's street edge: plank sidewalks, board crossings and the "
                 "fences that line the street"),
        "kind": "frontage",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same frame "
            "data/streets/1835.json, data/traces/vectors/thompson_lots.json and the "
            "sidecars' placement.local_e / local_n use."
        ),
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": [],
            "note": (
                "NO SOURCE RECORD IN THIS REPOSITORY STATES THAT A WALK, A CROSSING OR "
                "A FENCE STOOD ON ANY PARTICULAR STRETCH OF THESE STREETS ON 1 JULY "
                "1835. What is held is four owner-supplied reference views, written up "
                "verbatim at data/sources/assets/owner_brief_2026_08_18/README.md, and "
                "the owner's own reading of the first of them: of the first Cook County "
                "jail engraving (image 1), 'note the fences lining the street and what "
                "appears to be plank sidewalks. all of the streets should be updated "
                "like this... at least south of the river or near the river.' Image 6 "
                "(the Green Tree) gives 'plank sidewalks with board crossings'; image 8 "
                "(the Petford watercolour of the Sauganash) gives 'plank sidewalk with "
                "a board crossing over the road'; image 9 (the Braunhold engraving of "
                "the same hotel) gives 'plank walks on both frontages'. All four are "
                "tier-5 pictorial and retrospective: they may drive setting, materials "
                "and treatment and they may never drive a coordinate, which is exactly "
                "the division kept here — WHAT stands is the plates', WHERE is the "
                "committed plat's. The plates are not yet held as source records "
                "(T-0075 owns that), so `sources` is deliberately empty and the "
                "citation is a committed path. That is a reconstruction in this "
                "project's third tier and it is graded and claimed as one: "
                f"docs/LIBERTIES.md {STREET_EDGE_LIBERTY}."
            ),
        },
        "treatment": {
            "confidence": "reconstructed",
            "note": (
                f"Walk {WALK_W_M} m wide, its inner edge {EDGE_FENCE_CLEAR_M} m off the "
                f"lot line, its deck {WALK_RISE_M} m over the ground, {PLANK_T_M} m "
                f"boards at a {EDGE_PLANK_PITCH_M} m pitch — street stock, wider than "
                f"the {PLANK_PITCH_M} m trim on the two inns' own walks — laid ACROSS "
                "the way a foot travels, and each board still samples the terrain under "
                "its own centre. The boards carry no underside: two triangles a board, "
                "facing the earth they are laid on, on tens of thousands of them. Its "
                f"stringers are laid at a {EDGE_STRINGER_PITCH_M} m bay rather than "
                "under every board: a town's worth of sidewalk is tens of thousands of "
                "small boxes, the stringer under a board is a quarter of the walk's "
                "silhouette and three quarters of its cost, and the ground these "
                "streets cross is flat enough (the march refuses any stretch that rolls "
                f"more than {EDGE_FLAT_M} m inside a walking deck) that a bay-length "
                "stringer meets it as closely as a board-length one did. Crossings "
                f"{EDGE_CROSS_W_M} m wide and {EDGE_CROSS_PLANKS} boards laid ALONG the "
                f"run. Fences {EDGE_FENCE_H_M} m tall — 4 ft 6 in, a street fence and "
                "not the Sauganash's private six-foot yard wall — of "
                f"{EDGE_FENCE_BOARD_W_M} m boards butted at {EDGE_FENCE_BOARD_GAP_M} m "
                f"on {EDGE_FENCE_COURSES} stringers, posts every "
                f"{EDGE_FENCE_POST_SPACING_M} m. Not one of those numbers is a "
                "record's; they are how the layer is DRAWN."
            ),
        },
        "rule": {
            "note": (
                "A block face carries a walk iff it fronts one of the covered "
                "streets and a walk at its lot line still clears that street's own "
                f"travelled track by {EDGE_TRACK_MARGIN_M} m. The face is then MARCHED "
                f"in {EDGE_SPAN_M} m steps, and a step carries boards iff the ground "
                f"under it stands at least {EDGE_DRY_M} m over datum, rolls no more "
                f"than {EDGE_FLAT_M} m (which is what lets the whole step be ONE deck a "
                "visitor stands on), and carries no committed footprint. Consecutive "
                f"carrying steps become a run; a run under {EDGE_MIN_RUN_M} m is a "
                "landing rather than a sidewalk and is dropped. A crossing exists only "
                "where two runs stop either side of one corridor. A lot gets a street "
                "fence iff it is improved and its nearest committed wall stands "
                f"{EDGE_FENCE_SETBACK_M} m or more back from its own frontage line — "
                "where it does not, the building is the street wall. Every refusal "
                "below names the clause that refused it. Read them in "
                "tools/generate_frontage_works.py."
            ),
            "covered_streets": list(EDGE_STREETS),
            "faces_laid": census["faces"],
            "walk_m": census["walk_m"],
            "crossing_m": census["cross_m"],
            "fence_m": census["fence_m"],
            "walking_decks": census["decks"],
        },
        "card": {
            "id": STREET_EDGE_ID,
            "name": "The town's street edge",
            "symbolic_location": (
                "South Water Street and Lake Street, between Market Street and State "
                "Street — the plank sidewalks at the lot line, the board crossings at "
                "the corners and over the road, and the fences behind them."
            ),
            "position_note": bounds_note,
            "attributes": {
                "existence": {
                    "value": True,
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": (
                        "Asked for by the owner, 2026-08-18, of the first Cook County "
                        "jail engraving: 'note the fences lining the street and what "
                        "appears to be plank sidewalks. all of the streets should be "
                        "updated like this... at least south of the river or near the "
                        "river.' No 1835 source names a walk or a fence on any "
                        "particular stretch of these streets."
                    ),
                },
                "walk_m": {
                    "value": census["walk_m"],
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": (
                        f"{census['runs']} run(s) of sidewalk on {census['faces']} "
                        "platted block face(s), plus "
                        f"{census['cross_m']} m of board crossing at "
                        f"{census['crossings']} corner(s). Nothing measured: every "
                        "metre is derived from the committed plat and audited against "
                        "the committed ground."
                    ),
                },
                "fence_m": {
                    "value": census["fence_m"],
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": (
                        f"{census['fences']} street-lining fence run(s), on the lots "
                        "the rule found improved and standing back from their own "
                        "frontage line."
                    ),
                },
                "width_m": {
                    "value": WALK_W_M,
                    "confidence": "reconstructed",
                    "sources": [],
                    "note": "Six feet — two people passing; the layer's own drawn width.",
                },
            },
            "research_note": (
                "A walk from data/frontage/ — not a structure record. " + bounds_note
                + " What would move it off reconstruction: a Chicago town order on "
                "sidewalks of the right date — the corporation legislated wooden walks "
                "within a few years of 1835, and an order would give a width and a "
                "material at a stroke; a tax, insurance or sale description naming a "
                "walk or a fence in front of a named lot; or holding the jail, Green "
                "Tree and Sauganash plates as proper source records (T-0075)."
            ),
        },
        "walks": walks,
        "fences": fences,
        "posts": [],
        "refused": refused,
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: a Chicago town order on "
            "sidewalks or on lawful fences of the right date; a tax, insurance or sale "
            "description naming a walk or a fence in front of a named lot; or holding "
            "the four reference plates as proper source records with their institutions "
            "and dates (T-0075). AND ONE THING THAT CHANGED THE SHAPE OF THE RUN "
            "WITHOUT CHANGING ITS EVIDENCE, finished here: eleven documented South "
            "Water Street buildings were placed against the modern kerb rather than "
            "against this project's own platted line and stood 4.5 to 8.2 m out past "
            "it, which is why the walk on that side broke around them. T-0188 "
            "reconciled six — the same derivation each record already describes, run "
            "against this project's committed street line instead of a modern one — "
            "and T-0199 the last five, which had been refused because each seated on a "
            "platted lot the 665-roof schedule had dealt to that block's anonymous "
            "frontage run. What answered that refusal was a measurement rather than a "
            "concession: the town's eight party-line runs were dealt 20 lots of "
            "frontage and stand on 12, so four of the five stores were being kept out "
            "of the town by an entitlement no roof was using, and the fifth shares its "
            "lot with a run that had room for it. No anonymous roof left the street."
        ),
    }


def index_record() -> dict:
    """The manifest the renderer fetches before it fetches anything else.

    Generated with the records rather than kept by hand, because a record written
    and never listed is a record nobody draws — and `--check` would have called that
    green.
    """
    return {
        "_doc": (
            "Manifest for the frontage layer — the plank walks, the board crossings, "
            "the hitching posts and the named boards on posts that stand between a "
            "building and the street it fronts on. A static host cannot be globbed, "
            "which is why this file exists: the renderer fetches this manifest and "
            "then exactly the files it names, never a probe. Nothing here is a "
            "structure record and nothing here is baked geometry: a walk is boards "
            "laid on ground this project has already built and a post is a pole "
            "standing on it, so both are derived from the committed footprint, the "
            "committed placement and the committed street corridor, and drawn by "
            "renderers/web/js/frontage.js from these numbers alone. Records AND this "
            "manifest are GENERATED by tools/generate_frontage_works.py and re-derived "
            "byte for byte by tools/check.sh, because \"where a walk may lie\" is a "
            "rule and a rule has to be auditable."
        ),
        "version": 1,
        "scene": "1835",
        "scene_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin — the same frame "
            "data/signage/, data/yard/ and the sidecars' placement.local_e / local_n use."
        ),
        "frontage": [{"id": c["record_id"], "file": c["out"]} for c in BUILDINGS]
        + [{"id": "river_walk_frontage", "file": "river_walk_frontage.json"},
           {"id": STREET_EDGE_RECORD_ID, "file": "town_street_edge.json"}],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()

    wanted: list[tuple[Path, str, str]] = []
    totals = [0, 0, 0]
    for cfg in BUILDINGS:
        walks, posts, refused = build(cfg)
        totals = [totals[0] + len(walks), totals[1] + len(posts), totals[2] + len(refused)]
        text = json.dumps(record(cfg, walks, posts, refused), indent=2,
                          ensure_ascii=False) + "\n"
        wanted.append((OUTDIR / cfg["out"], text, cfg["structure_id"]))
    river_walks, river_refused = build_river_walk()
    totals = [totals[0] + len(river_walks), totals[1], totals[2] + len(river_refused)]
    wanted.append((OUTDIR / "river_walk_frontage.json",
                   json.dumps(river_record(river_walks, river_refused), indent=2,
                              ensure_ascii=False) + "\n",
                   "the river plank walk"))
    edge_walks, edge_fences, edge_refused, edge_census = build_street_edge()
    totals = [totals[0] + len(edge_walks), totals[1], totals[2] + len(edge_refused)]
    fences_written = len(edge_fences)
    wanted.append((OUTDIR / "town_street_edge.json",
                   json.dumps(street_edge_record(edge_walks, edge_fences, edge_refused,
                                                 edge_census), indent=2,
                              ensure_ascii=False) + "\n",
                   "the town's street edge"))
    wanted.append((INDEX, json.dumps(index_record(), indent=2, ensure_ascii=False) + "\n",
                   "the manifest"))

    if args.check:
        drift = []
        for path, text, who in wanted:
            if not path.exists():
                drift.append(f"{path.relative_to(ROOT)} is missing ({who})")
            elif path.read_text(encoding="utf-8") != text:
                drift.append(f"{path.relative_to(ROOT)} has drifted from the rule in "
                             f"tools/generate_frontage_works.py ({who})")
        if drift:
            print("FRONTAGE DRIFT")
            for d in drift:
                print(f"  - {d}")
            return 1
        print(f"verified {len(BUILDINGS) + 2} frontage record(s): {totals[0]} "
              f"walk/crossing run(s), {fences_written} street-lining fence run(s) and "
              f"{totals[1]} post(s) ({totals[2]} refusal(s) stated)")
        return 0

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for path, text, _ in wanted:
        path.write_text(text, encoding="utf-8")
    print(f"wrote {len(BUILDINGS) + 2} frontage record(s) and their manifest — "
          f"{totals[0]} walk/crossing run(s), {fences_written} street-lining fence "
          f"run(s), {totals[1]} post(s) ({totals[2]} refused)")
    print(f"  street edge: {edge_census['faces']} block face(s), "
          f"{edge_census['walk_m']} m of walk in {edge_census['runs']} run(s), "
          f"{edge_census['crossings']} crossing(s) ({edge_census['cross_m']} m), "
          f"{edge_census['fences']} fence run(s) ({edge_census['fence_m']} m), "
          f"{edge_census['decks']} walking deck(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
