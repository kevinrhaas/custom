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

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIDECARS = DATA / "sidecars" / "1835"
STREETS = DATA / "streets" / "1835.json"
WHARVES = DATA / "wharves" / "river_landings.json"
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
        "existence_note": (
            "NO SOURCE RECORD IN THIS REPOSITORY STATES THAT A WALK, A CROSSING OR "
            "A POST STOOD ON THIS GROUND ON 1 JULY 1835. What is held is two "
            "owner-supplied reference views of this inn, written up verbatim at "
            "data/sources/assets/owner_brief_2026_08_18/README.md: image 6, the "
            "Braunhold engraving of 1838, gives 'post-mounted hanging signboard at "
            "the corner; plank sidewalks with board crossings', and image 7, the "
            "Trowbridge drawing, gives 'the hanging \"GREEN TREE\" sign on its "
            "post'. Both are tier-5 pictorial and retrospective, and the plates "
            "themselves are not yet held as source records — T-0075 owns that — so "
            "`sources` is deliberately empty and the citation is a committed path. "
            "That is a reconstruction in this project's third tier and it is graded "
            "and claimed as one: docs/LIBERTIES.md L135."
        ),
        "claim_key": "lettering",
        "claim_block": {
            "value": "GREEN TREE",
            "confidence": "inferred",
            "geometry": "drawn",
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
            "data/sources/assets/owner_brief_2026_08_18/README.md, image 7 — "
            "the Trowbridge drawing of this inn, described there as 'the "
            "hanging \"GREEN TREE\" sign on its post'. The plate is not held "
            "as a source record yet; T-0075 owns making one, and until it does "
            "the citation is a committed path rather than a source_id."
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
            "lot; or holding the Braunhold and Trowbridge plates as proper source "
            "records with their institutions and dates (T-0075), which would turn the "
            "committed path in `existence.note` into a source_id and the lettering's "
            "warrant into a citation."
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
            "is the L1 constraint. All three are tier-5 pictorial and retrospective, "
            "and the plates themselves are not yet held as source records — T-0075 "
            "owns that — so `sources` is deliberately empty and the citation is a "
            "committed path. That is a reconstruction in this project's third tier and "
            "it is graded and claimed as one: docs/LIBERTIES.md L136."
        ),
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
            "this lot; or holding the Petford, Braunhold and Trowbridge plates as "
            "proper source records with their institutions and dates (T-0075), which "
            "would turn the committed path in `existence.note` into a source_id. What "
            "would NOT move: the two posts' own dimensions, which no order and no plate "
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
            "sources": [],
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
        + [{"id": "river_walk_frontage", "file": "river_walk_frontage.json"}],
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
        print(f"verified {len(BUILDINGS) + 1} frontage record(s): {totals[0]} "
              f"walk/crossing run(s) and {totals[1]} post(s) "
              f"({totals[2]} refusal(s) stated)")
        return 0

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for path, text, _ in wanted:
        path.write_text(text, encoding="utf-8")
    print(f"wrote {len(BUILDINGS) + 1} frontage record(s) and their manifest — "
          f"{totals[0]} walk/crossing run(s), {totals[1]} post(s) ({totals[2]} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
