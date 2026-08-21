#!/usr/bin/env python3
"""Generate the town's business signboards — what each one says, and how it hangs.

WHAT THIS IS. `docs/ROADMAP.md` K5 (b) asked for *"signboards on businesses"* and ticket
T-0039 built the layer: a plank on a bracket, hung off a wall this project had already
drawn, on every frontage a rule selected. Every one of those boards was BLANK, and every
one was hung the same way, because L25 and L130 read the absence of any recorded WORDING
as a reason to paint nothing at all.

T-0066 OVERRULES THAT, on the owner's instruction of 2026-08-18, verbatim: *"you can and
should put the name of the location on the sign board. the sign boards should have
variation in color and style and signage font and color, some signs may hang from an
awning and others may be on the building or painted on the face of the building. you
need to add more signage and be period correct and it is fine if they are
reconstructions."* The standing ruling on invention applies: *"you are totally fine to be
liberal with adding reconstructed items when i ask for things, you can just label and
mark them as such."* So this record now carries, for every board:

  * the WORDING — the name the dataset already gives that location, so a visitor who
    reads the board and then taps it is shown the same words on the card;
  * a MOUNTING — bracket-hung over the footway, hung under an awning, fixed flat on the
    building, standing on a post at the street edge, or the name painted straight onto
    the face of the building;
  * a STYLE — ground colour, letter colour, letterform and panel, from a table of the
    combinations the trade actually used, assigned so that no two boards within
    `NEIGHBOUR_M` of each other share a mounting, a style or a ground colour.

All three are RECONSTRUCTED and graded so. `docs/LIBERTIES.md` **L158** is the claim.

THE RULE THAT CHOOSES A FRONTAGE, and every clause is doing work. A structure gets a
sign iff

  1. it is a NAMED record — the id does not begin `inf_` or `recon_` and the name does
     not begin "Reconstructed". The archetype tables already carry this rule in as many
     words: *never invent business, sign text or goods for an anonymous slot*. An
     anonymous roof dealt a trade by a schedule has no proprietor to announce, and now
     that the boards carry NAMES the clause matters more than it did when they were
     blank: there would be no name to paint;
  2. its `function` is a trade this project will announce. Two classes of them now:
     a PUBLIC TRADE, whose customer was a stranger arriving on foot off the street (a
     public house, a lodging house, a shop counter, the auction room, the printing
     offices that also sold over one) — these get a BOARD; and, added by T-0066, a
     WORKS OR WAREHOUSE trade, whose custom came by name and by cart — these get the
     firm's name PAINTED ON THE BUILDING and never a board swinging over a footway
     nobody walked. Stables, churches, schools, the court-house, the jail, the agency
     house and the fort stay outside both lists;
  3. that function is `attested` or `inferred`. A `reconstructed` trade gets no sign —
     inventing a sign for an invented business is invention squared;
  4. it is standing on the scene date (it is in `data/sidecars/1835/index.json`);
  5. it does not already carry a sign. One record does, and duplicating it would put
     two boards on the Wolf Point Tavern;
  6. it does not already carry a NAMED board on a post at its corner on the frontage
     layer (the Green Tree — T-0082, L135);
  7. and, for the works and warehouse class only, its name carries a PROPRIETOR — a
     possessive or an ampersand. A works painted whose it was. A building this project
     names by a later nickname ("The Old Bank Building") has no proprietor to paint,
     and painting the nickname would put a twentieth-century label on an 1835 wall.

WHERE THE SIGN GOES is then DERIVED, not placed. `docs/GLB-CONTRACT.md` fixes the frame:
polygon `u` → +X, polygon `v` → −Z, and `rotation_deg` is the FACADE BEARING, so the
front wall is the footprint's own max-`v` edge and the direction it faces is the bearing
itself. A hanging board hangs to one side of that edge's centre and clear of the eave;
a wall board and a painted name are centred on it. A POST is the one mounting that
stands in the street rather than on the building, so it is refused — in writing, and the
next mounting in the cycle is taken — wherever the fronting street's own travelled track
comes too close, or wherever the frontage layer already lays a plank walk outside that
wall. That test is `data/streets/1835.json`'s, the same one
`tools/generate_frontage_works.py` uses.

    python3 tools/generate_business_signboards.py            write the record
    python3 tools/generate_business_signboards.py --check    re-derive and diff
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIDECARS = DATA / "sidecars" / "1835"
STRUCTURES = DATA / "structures"
STREETS = DATA / "streets" / "1835.json"
FRONTAGE = DATA / "frontage"
OUT = DATA / "signage" / "town_business_signboards.json"

# Clause 2, first class. Trades whose customer was a stranger off the street. The
# value on the left is `function.value` as the structure records write it; the phrase
# on the right is why a sign belongs on that door and is quoted into the record.
PUBLIC_TRADES = {
    "tavern_inn": "a public house takes its custom from the road",
    "hotel": "a public house takes its custom from the road",
    "boarding_house": "lodging is sold to arrivals who have to find the door",
    "store": "a counter open to the street",
    "store_residence": "a counter open to the street, with the keeper living over it",
    "store_and_dwelling": "a counter open to the street, with the keeper living over it",
    "dwelling_and_store": "a counter open to the street, with the keeper living over it",
    "grocery_and_provision_store": "a counter open to the street",
    "drug_store": "a counter open to the street",
    "forwarding_and_commission_store": "a counting-room a shipper has to find from the wharf",
    "auction_room": "a sale room whose whole trade is being found on the day",
    "saddlery_and_harness_shop": "a craft shop selling finished goods over a counter",
    "printing_office": "an office that took job work and subscriptions from callers",
    "printing_office_and_store": "an office that took job work and sold over a counter",
    "physicians_office": "a consulting room a stranger has to be able to find",
    "shop": "a shop front on a street of stores",
}

# Clause 2, second class — added 2026-08-21 with T-0066. A works or a warehouse did not
# hang a board over a footway; it painted the firm's name on the front, where a carter
# and a shipper could read it off the river or off the road. That is the distinction
# L130's excluded-trades note drew when it left these frontages mute, and the answer to
# it is a DIFFERENT MOUNTING rather than a different silence.
WORKS_TRADES = {
    "blacksmith_shop": "a smith's shop, named on its front for the carter who needs one",
    "forwarding_commission_warehouse": "a warehouse names its firm for the shipper on the river",
    "warehouse_and_slaughter_yard": "a warehouse names its firm for the shipper on the river",
    "slaughterhouse_packing": "a packing house names the firm the drover is delivering to",
    "packing_house": "a packing house names the firm the drover is delivering to",
    "tannery": "a tan-yard names its master for the trade that brings him hides",
    "soap_candle_manufactory": "a manufactory names the firm whose goods leave by the cart-load",
    "brickyard": "a brickyard names its owner for the builder ordering by the thousand",
}

# Which cycle of mountings a trade draws from. Two frontages of the same class in the
# same street get DIFFERENT mountings because the cycle advances; two of different
# classes differ because the cycles do not start in the same place.
TRADE_CLASS = {
    **{t: "house" for t in ("tavern_inn", "hotel", "boarding_house")},
    **{t: "counter" for t in (
        "store", "store_residence", "store_and_dwelling", "dwelling_and_store",
        "grocery_and_provision_store", "drug_store", "shop",
        "saddlery_and_harness_shop")},
    **{t: "office" for t in (
        "printing_office", "printing_office_and_store", "auction_room",
        "forwarding_and_commission_store", "physicians_office")},
    **{t: "works" for t in WORKS_TRADES},
}

# THE MOUNTINGS, and why each class draws from the cycle it does.
#
#  * a PUBLIC HOUSE is read from up the road by somebody who has not arrived yet, so its
#    name goes where it is seen furthest — under a hood over the door, out on a bracket,
#    or on a post at the street edge (which is exactly what the Green Tree does, images 6
#    and 7 of the owner's brief, and what T-0082 already drew there);
#  * a COUNTER is read from the footway by somebody already outside it, so a bracket
#    board over the walk, a board fixed on the front, an awning board, or the name
#    straight on the boards of the building — the Tremont street scene (image 5) shows a
#    whole row of painted fronts;
#  * an OFFICE or a sale room is a door among doors and mostly took a modest board on the
#    building itself;
#  * a WORKS paints its front and never hangs anything (see WORKS_TRADES above).
MOUNTING_CYCLE = {
    "house": ["awning_board", "bracket_board", "post_board"],
    "counter": ["bracket_board", "wall_board", "awning_board", "facade_painted"],
    "office": ["wall_board", "bracket_board", "facade_painted"],
    "works": ["facade_painted"],
}

# THE STYLES. Ground, letters, letterform and panel — the combinations an American
# signwriter of the 1830s worked in. Nothing here is a Chicago record: no wording,
# device or colour of any sign in this town survives, so the whole table is
# reconstruction and is graded as one (L158). What it is NOT is arbitrary: black
# grounds with gilt letters, white lead grounds with black, ochre (the cheapest
# pigment on any colourman's shelf), Venetian red, Prussian blue and Brunswick green
# are the trade's ordinary stock, and the letterforms are the four the period's
# specimen books actually sell — the signwriter's roman, the fat face that is the
# 1830s display letter, the Egyptian slab that arrives with it, and the plain block.
# `aspect` is the board's width-to-height and is part of the variation: two boards on
# one street should not be the same rectangle either.
STYLES = [
    {"id": "gold_on_black", "ground": "#141009", "letter": "#c9a227",
     "face": "signwriter", "panel": "plain", "aspect": 1.85,
     "note": "gilt letters on a black ground, shaded — the commonest painted board of the trade"},
    {"id": "black_on_white", "ground": "#e8e1cf", "letter": "#191410",
     "face": "fat_face", "panel": "double_rule", "aspect": 2.10,
     "note": "black on a white lead ground, the cheapest board a signwriter could sell"},
    {"id": "cream_on_green", "ground": "#1d3226", "letter": "#e7ddc0",
     "face": "signwriter", "panel": "single_rule", "aspect": 1.70,
     "note": "cream on a Brunswick-green ground"},
    {"id": "black_on_ochre", "ground": "#c19a52", "letter": "#1a1309",
     "face": "egyptian", "panel": "plain", "aspect": 2.35,
     "note": "black Egyptian on a yellow-ochre ground"},
    {"id": "cream_on_red", "ground": "#7c3020", "letter": "#efe3c8",
     "face": "fat_face", "panel": "single_rule", "aspect": 1.95,
     "note": "cream fat face on Venetian red"},
    {"id": "white_on_blue", "ground": "#22344f", "letter": "#e9e6dc",
     "face": "grotesque", "panel": "plain", "aspect": 2.20,
     "note": "white block letters on a Prussian-blue ground"},
    {"id": "gold_on_green", "ground": "#16261c", "letter": "#c8a63c",
     "face": "signwriter", "panel": "oval", "aspect": 1.75,
     "note": "gilt letters in an oval field on a dark green ground"},
    {"id": "black_on_timber", "ground": "#cbc2b1", "letter": "#241a10",
     "face": "grotesque", "panel": "plain", "aspect": 2.00,
     "note": "black on a bare weathered board — the tone L130 hung the town's blank boards in"},
    {"id": "red_on_white", "ground": "#e9e2d1", "letter": "#8c2f1f",
     "face": "egyptian", "panel": "oval", "aspect": 1.80,
     "note": "vermilion Egyptian on a white ground"},
    {"id": "white_on_brown", "ground": "#4a3121", "letter": "#e6dccb",
     "face": "fat_face", "panel": "double_rule", "aspect": 2.45,
     "note": "white fat face on a chocolate-brown ground"},
]

# Clause 3.
TRADE_GRADES = {"attested", "documented", "inferred"}

# Clause 6, added 2026-08-18 with ticket T-0082 and kept by T-0066. A frontage whose OWN
# reference view shows a board on a POST at the corner does not also get a second board
# hung on its wall by this rule. The Green Tree is the only one: images 6 and 7 of the
# owner's brief (data/sources/assets/owner_brief_2026_08_18/README.md) both show one
# board at this inn, both put it on a post, and image 7 says GREEN TREE is on it — which
# is now drawn, lettered, by the frontage layer (data/frontage/green_tree_frontage.json,
# docs/LIBERTIES.md L135). That board is the town's exemplar for the post mounting this
# record now uses elsewhere; drawing a second sign here would be the town making the same
# claim twice.
POST_BOARD_IDS = {
    "green_tree_tavern": (
        "it carries a NAMED board on its own post at the street corner instead. "
        "Images 6 and 7 of data/sources/assets/owner_brief_2026_08_18/README.md both "
        "show ONE board at this inn, post-mounted at the corner and lettered GREEN "
        "TREE; it is drawn from data/frontage/green_tree_frontage.json by "
        "renderers/web/js/frontage.js (T-0082, docs/LIBERTIES.md L135). That board is "
        "the exemplar this record's own post mounting is copied from. A second sign "
        "here would be this layer drawing the same claim a second time."
    ),
}

# HOW A SIGN IS DRAWN, and why these numbers are here rather than in a renderer. The
# bracket board's arm, drop and hangers are still the wolf sign's own geometry, copied
# from generators/archetypes/log_dwelling.py::_sign, so the town has one convention for
# hanging a board. Everything T-0066 adds — the awning hood, the wall board's cap, the
# post's stand, the painted band — is invented here in every dimension and the record
# carries each number so the renderer can draw it and this file can bound its reach.
ARM_M = 1.15            # the bracket arm, out of the wall
DROP_M = 0.20           # hangers, arm to board
BOARD_T_M = 0.05
OFFSET_M = 1.7          # a hanging board sits this far off the facade's centre
END_CLEAR_M = 0.6       # and never closer than this to the end of the wall
EAVE_CLEAR_M = 0.30
MAX_HEIGHT_M = 2.55

AWNING_PROJECTION_M = 1.45   # the hood over the door, out of the wall
AWNING_DROP_M = 0.34         # its outer edge below its inner one — the fall of a hood
AWNING_MARGIN_M = 0.45       # hood wider than the board it shelters, each side
WALL_BOARD_PROUD_M = 0.02    # a board fixed flat on the front stands this far off it
BAND_PROUD_M = 0.03          # a name painted on the boards, this far proud to draw
BAND_FOOT_M = 2.30           # and its foot this high, clear of any door head
BAND_EAVE_CLEAR_M = 0.25     # unless the wall has not the height, then under the eave
POST_STAND_M = 1.90          # a post stands this far out from the facade
POST_CLEAR_M = 1.00          # and must leave this much between it and the track edge
POST_ARM_M = 1.30

# The board's own size. A board is as long as its name needs and no longer, inside the
# range the mounting allows and inside the frontage it hangs on.
BOARD_SIZE = {
    "bracket_board": {"base": 0.72, "min": 0.88, "max": 1.46, "aspect_mul": 1.00},
    "awning_board": {"base": 0.84, "min": 1.02, "max": 1.66, "aspect_mul": 1.18},
    "wall_board": {"base": 1.00, "min": 1.24, "max": 2.30, "aspect_mul": 1.45},
    "post_board": {"base": 0.88, "min": 1.10, "max": 1.58, "aspect_mul": 1.05},
    "facade_painted": {"base": 1.70, "min": 2.10, "max": 4.30, "aspect_mul": 2.30},
}
PER_LETTER_M = 0.030
BOARD_H_MIN_M = 0.34
BOARD_H_MAX_M = 1.15
FACADE_MIN_FRONTAGE_M = 3.0   # under this a painted band has nowhere to run

# Two signs closer together than this must not share a mounting, a style or a ground
# colour. 40 m is about a platted lot and a half — near enough that a walker sees both
# at once, which is the test the owner set: *no two are alike on a street*.
NEIGHBOUR_M = 40.0

# The post's street test, borrowed whole from tools/generate_frontage_works.py so that
# two layers deciding "may something stand in this street" decide it the same way.
STREET_REACH_M = 22.0
FRONTAGE_DOMINANCE = 0.5

# Clause 5 and the log_dwelling default, mirrored: `wall_height_m` is optional on a
# record and the archetype resolves 2.5 m for one storey, 4.6 m for more. A board
# hung off a wall this project never measured is hung off the same number the wall
# itself is drawn at, which is the only way the two can agree.
DEFAULT_WALL_M = {1: 2.5, None: 2.5}
DEFAULT_WALL_MULTI_M = 4.6


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _round(x: float, places: int = 3) -> float:
    """Round toward a stable decimal so `--check` diffs bytes, not float noise."""
    return round(x + 0.0, places) + 0.0


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _rank(sid: str, n: int) -> int:
    """A stable integer for a structure id, for the style preference order.

    hashlib rather than `hash()`: Python randomises string hashing per process, and a
    record that re-derives differently on the next run is not a derivation.
    """
    return int(hashlib.sha1(sid.encode("utf-8")).hexdigest()[:8], 16) % n


def _to_enu(u: float, v: float, place: dict) -> tuple[float, float]:
    """A footprint coordinate to local ENU metres.

    docs/GLB-CONTRACT.md: polygon `u` → +X, polygon `v` → −Z, ENU `local_e` → +X and
    `local_n` → −Z, and the node's yaw is `-rotation_deg` about +Y. Composing those
    three lines is this function and nothing else; it is verified against the Green
    Tree, whose record says its front is on Canal to the west and whose rotation is
    270, by `--check` refusing any drift in the numbers below.
    """
    th = math.radians(-(place.get("rotation_deg") or 0.0))
    x, z = u, -v
    xr = x * math.cos(th) + z * math.sin(th)
    zr = -x * math.sin(th) + z * math.cos(th)
    return (place.get("local_e") or 0.0) + xr, (place.get("local_n") or 0.0) - zr


def _front_edge(polygon: list) -> tuple[float, float, float]:
    """The front wall: the footprint's max-`v` edge, as (u_min, u_max, v).

    Rotation 0 faces north and +v is north, so the wall a bearing points out of is
    the one at the largest v. Both L-shaped footprints in the set (Miller House, the
    Western Hotel) reach their full u-extent at that v, so the general case and the
    rectangle agree; a footprint that did not would be caught by the guard below.
    """
    vmax = max(p[1] for p in polygon)
    on = [p[0] for p in polygon if abs(p[1] - vmax) < 1e-6]
    if len(on) < 2:
        return 0.0, 0.0, vmax
    return min(on), max(on), vmax


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
    out = {}
    for s in doc.get("streets", []):
        out[s["id"]] = {
            "name": s.get("name_1835") or s["id"],
            "path": [tuple(p) for p in s.get("path_local_enu_m", [])],
            "track_w": float(s.get("track_width_m") or 7.0),
        }
    return out


def _street_facing(mid, normal, streets: dict):
    """Which street a wall faces: the nearest centreline that lies IN FRONT of it.

    The same two tests `tools/generate_frontage_works.py::_street_facing` makes, for
    the same reason: a rear wall can be as close to a street as a front wall is to
    another one, and a street that runs BESIDE a wall rather than in front of it is
    not the street that wall's sign stands in.
    """
    best = (None, {}, float("inf"))
    for sid, st in streets.items():
        if len(st["path"]) < 2:
            continue
        d, foot = _nearest_on_path(mid, st["path"])
        outward = (foot[0] - mid[0]) * normal[0] + (foot[1] - mid[1]) * normal[1]
        if outward <= 0 or d > STREET_REACH_M:
            continue
        if outward < FRONTAGE_DOMINANCE * d:
            continue
        if d < best[2]:
            best = (sid, st, d)
    return best


def _frontage_walled() -> set:
    """Buildings the frontage layer already lays a plank walk outside of.

    A post stands where a walk lies. Rather than working out which of the two moves,
    this refuses the post at those frontages and takes the next mounting in the cycle
    — a refusal that is written into the record instead of being a silent nudge.
    """
    out = set()
    if not FRONTAGE.is_dir():
        return out
    for path in sorted(FRONTAGE.glob("*.json")):
        if path.name == "index.json":
            continue
        doc = _load(path)
        for walk in doc.get("walks", []):
            if walk.get("belongs_to"):
                out.add(walk["belongs_to"])
    return out


def _sign_text(name: str) -> tuple[str, str]:
    """What is painted, and why it is not simply the record's name verbatim.

    It very nearly is, and that is the point: the card a visitor opens by tapping the
    board has to say what the board says. The one thing dropped is a trailing
    parenthetical — "Tremont House (the first)" is this project telling itself which of
    three Tremonts it is modelling, not something a signwriter put on a board.
    """
    text = name.strip()
    why = "the record's own name, which is what the card shows"
    if text.endswith(")") and "(" in text:
        cut = text.rindex("(")
        stripped = text[:cut].strip()
        if stripped:
            text = stripped
            why = ("the record's own name less its trailing parenthetical, which "
                   "disambiguates the model rather than naming the house")
    return " ".join(text.split()), why


def _candidates() -> tuple[list, list]:
    """Every frontage the rule selects, with its trade class — and every refusal."""
    index = _load(SIDECARS / "index.json")
    standing = [s["id"] for s in index.get("structures", [])]
    picked: list[dict] = []
    refused: list[dict] = []

    for sid in standing:
        sc_path = SIDECARS / f"{sid}.json"
        if not sc_path.exists():
            continue
        sc = _load(sc_path)
        attrs = sc.get("attributes") or {}
        fn = attrs.get("function") or {}
        trade = fn.get("value")
        if trade not in PUBLIC_TRADES and trade not in WORKS_TRADES:
            continue                                            # clause 2
        name = sc.get("name") or ""
        if sid.startswith(("inf_", "recon_")) or name.startswith("Reconstructed"):
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "an anonymous slot. The archetype tables' own rule — never invent "
                "business, sign text or goods for an anonymous slot — and this record "
                "keeps it. Now that a board carries a NAME there is not even one to "
                "paint.")})
            continue                                            # clause 1
        grade = fn.get("confidence")
        if grade not in TRADE_GRADES:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"the trade itself is {grade}. A sign for a business this project "
                "reconstructed would be an invention resting on an invention.")})
            continue                                            # clause 3

        if sid in POST_BOARD_IDS:
            refused.append({"structure_id": sid, "trade": trade,
                            "why": POST_BOARD_IDS[sid]})
            continue                                            # clause 6

        struct = _load(STRUCTURES / f"{sid}.json")
        already = [ph.get("id") for ph in struct.get("phases", [])
                   if (ph.get("form") or {}).get("sign")]
        if already:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "it already has one. This is the single record in the dataset that "
                "ATTESTS a sign, and the board hangs in its GLB already "
                f"(phase {already[0]}, docs/LIBERTIES.md L25). A second board here "
                "would be this layer duplicating the only real one.")})
            continue                                            # clause 5

        if trade in WORKS_TRADES and not ("'s" in name or "&" in name):
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"'{name}' carries no proprietor — no possessive and no ampersand. A "
                "works painted WHOSE it was, and this project names this building by a "
                "later nickname rather than by a firm; painting the nickname would put "
                "a modern label on an 1835 wall.")})
            continue                                            # clause 7

        place = sc.get("placement") or {}
        poly = (sc.get("footprint") or {}).get("polygon") or []
        if len(poly) < 3:
            refused.append({"structure_id": sid, "trade": trade,
                            "why": "no footprint polygon — no wall to put a sign on."})
            continue
        u0, u1, vmax = _front_edge(poly)
        if u1 - u0 < 1.2:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "the front wall is under 1.2 m of frontage — narrower than the board.")})
            continue

        picked.append({
            "sid": sid, "name": name, "trade": trade, "grade": grade,
            "sc": sc, "place": place, "poly": poly,
            "u0": u0, "u1": u1, "vmax": vmax,
            "cls": TRADE_CLASS[trade],
        })

    picked.sort(key=lambda c: c["sid"])
    refused.sort(key=lambda r: r["structure_id"])
    return picked, refused


def _reach(mounting: str, w: float, geom: dict) -> float:
    """The furthest, ON THE GROUND PLAN, any vertex of this sign may sit from its
    own anchor.

    Carried on the record so the smoke can hold every sign to ITS OWN bound rather
    than to one number wide enough for the largest mounting — a transposed axis is
    metres out, and a per-sign bound catches it on the smallest board too. Horizontal
    only, because that is the mistake it is looking for: a sign hung at the wrong
    HEIGHT is caught by the wall-base rule and by the eye, and a sign hung on the
    wrong AXIS is caught here.

    The 0.12 m is the renderer's own small timber — hanger straps, the strut under a
    bracket, the knee brace under a post arm, the cap over a wall board. Those are
    how a sign is DRAWN rather than a claim about any shop, so they stay in
    renderers/web/js/signage.js, and this leaves them room.
    """
    if mounting == "bracket_board":
        out = ARM_M
        along = w / 2.0
    elif mounting == "awning_board":
        out = AWNING_PROJECTION_M
        along = max(w, geom["awning_width_m"]) / 2.0
    elif mounting == "wall_board":
        out = WALL_BOARD_PROUD_M + BOARD_T_M
        along = w / 2.0
    elif mounting == "post_board":
        out = POST_STAND_M + geom["post_square_m"]
        along = POST_ARM_M * 0.55 + w / 2.0
    else:                                          # facade_painted
        out = BAND_PROUD_M
        along = w / 2.0
    return math.hypot(out, along) + 0.12


def build_record() -> tuple[list, list]:
    picked, refused = _candidates()
    streets = _streets()
    walled = _frontage_walled()

    # Clause 2's cycle index: a frontage's rank inside its own trade class, in id
    # order, so the cycle advances down a class rather than down the town.
    class_rank: dict[str, int] = {}
    for cand in picked:
        cand["rank"] = class_rank.get(cand["cls"], 0)
        class_rank[cand["cls"]] = cand["rank"] + 1

    signs: list[dict] = []
    for cand in picked:
        sid = cand["sid"]
        place = cand["place"]
        poly = cand["poly"]
        u0, u1, vmax = cand["u0"], cand["u1"], cand["vmax"]
        frontage = u1 - u0
        mid = (u0 + u1) / 2.0
        attrs = cand["sc"].get("attributes") or {}

        stories = ((attrs.get("stories") or {}).get("value"))
        wall = (attrs.get("wall_height_m") or {}).get("value")
        wall_from = "the record"
        if wall is None:
            wall = DEFAULT_WALL_M.get(stories, DEFAULT_WALL_MULTI_M) \
                if stories in DEFAULT_WALL_M else DEFAULT_WALL_MULTI_M
            wall_from = ("the archetype's default, because the record carries no "
                         "wall height — the same number the wall itself is drawn at")
        head = min(wall - EAVE_CLEAR_M, MAX_HEIGHT_M)

        text, text_from = _sign_text(cand["name"])

        # The centre of the front wall, in ENU, and the way it faces — the two things
        # every mounting test below needs.
        bearing = place.get("rotation_deg") or 0.0
        rad = math.radians(bearing)
        normal = (math.sin(rad), math.cos(rad))          # outward, in ENU
        mid_enu = _to_enu(mid, vmax, place)

        # --- the mounting -----------------------------------------------------
        cycle = MOUNTING_CYCLE[cand["cls"]]
        near = [s for s in signs
                if math.hypot(s["anchor_local_enu_m"][0] - mid_enu[0],
                              s["anchor_local_enu_m"][1] - mid_enu[1]) <= NEIGHBOUR_M]
        taken_mount = {s["mounting"] for s in near}
        mount_notes: list[str] = []
        mounting = cycle[cand["rank"] % len(cycle)]
        for step in range(len(cycle)):
            trial = cycle[(cand["rank"] + step) % len(cycle)]
            if trial == "post_board":
                if sid in walled:
                    mount_notes.append(
                        "a post was refused here because the frontage layer already "
                        "lays a plank walk outside this wall, and a post stands where "
                        "the walk lies")
                    continue
                st_id, st, dist = _street_facing(mid_enu, normal, streets)
                if st_id is None:
                    mount_notes.append(
                        "a post was refused here because no street lies in front of "
                        "this wall within "
                        f"{STREET_REACH_M:.0f} m — a post here would stand in a yard")
                    continue
                reach = dist - POST_STAND_M - st["track_w"] / 2.0
                if reach < POST_CLEAR_M:
                    mount_notes.append(
                        f"a post was refused here because the {st['name']} track "
                        f"reaches to within {reach + POST_CLEAR_M:.2f} m of where the "
                        "post would stand")
                    continue
            if trial == "facade_painted" and frontage < FACADE_MIN_FRONTAGE_M:
                mount_notes.append(
                    f"a painted name was refused here because the front wall is "
                    f"{frontage:.2f} m — under the {FACADE_MIN_FRONTAGE_M:.1f} m a band "
                    "needs to run")
                continue
            if trial in taken_mount and step + 1 < len(cycle):
                mount_notes.append(
                    f"a {trial.replace('_', ' ')} is what this frontage's place in the "
                    f"{cand['cls']} cycle asks for, and a sign within "
                    f"{NEIGHBOUR_M:.0f} m already hangs that way — so the cycle "
                    "advances rather than repeating a neighbour")
                continue                       # a neighbour already hangs one this way
            mounting = trial
            break

        # --- the style --------------------------------------------------------
        taken_style = {s["style"]["id"] for s in near}
        taken_ground = {s["style"]["ground"] for s in near}
        start = _rank(sid, len(STYLES))
        style = STYLES[start]
        for relax in (0, 1):
            found = None
            for k in range(len(STYLES)):
                s = STYLES[(start + k) % len(STYLES)]
                if s["id"] in taken_style:
                    continue
                if relax == 0 and s["ground"] in taken_ground:
                    continue
                found = s
                break
            if found:
                style = found
                break

        # --- the sign's own size ----------------------------------------------
        size = BOARD_SIZE[mounting]
        w = _clamp(size["base"] + PER_LETTER_M * len(text), size["min"], size["max"])
        if mounting == "facade_painted":
            w = min(w, frontage - 1.2)
        else:
            w = min(w, frontage - 2 * END_CLEAR_M)
        w = max(w, 0.7)
        h = _clamp(w / (style["aspect"] * size["aspect_mul"]),
                   BOARD_H_MIN_M, BOARD_H_MAX_M)

        # --- where it sits on the wall ----------------------------------------
        # A hanging board sits to one side of the door; a wall board and a painted
        # band are centred on the front, which is where a painted name goes.
        if mounting in ("bracket_board", "awning_board", "post_board"):
            u = mid + OFFSET_M
            if u > u1 - END_CLEAR_M:
                u = max(mid, u1 - END_CLEAR_M)
        else:
            u = mid
        e, n = _to_enu(u, vmax, place)
        quad = [_to_enu(uu, vv, place) for uu, vv in (
            (min(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), max(p[1] for p in poly)),
            (min(p[0] for p in poly), max(p[1] for p in poly)))]

        geom: dict = {}
        if mounting == "bracket_board":
            geom["arm_m"] = ARM_M
            geom["hanger_drop_m"] = DROP_M
        elif mounting == "awning_board":
            geom["awning_projection_m"] = AWNING_PROJECTION_M
            geom["awning_drop_m"] = AWNING_DROP_M
            geom["awning_width_m"] = _round(
                min(w + 2 * AWNING_MARGIN_M, max(w + 0.2, frontage - 0.8)), 2)
            geom["hanger_drop_m"] = DROP_M
        elif mounting == "wall_board":
            geom["proud_m"] = WALL_BOARD_PROUD_M
        elif mounting == "post_board":
            geom["stand_m"] = POST_STAND_M
            geom["arm_m"] = POST_ARM_M
            geom["hanger_drop_m"] = DROP_M
            # The pole's height is invented inside a hand's range of the Green Tree's
            # 3.60 m, varied by the same stable rank the style uses so that two posts
            # in one street are not the same stick.
            geom["post_height_m"] = _round(3.30 + 0.12 * (_rank(sid, 5)), 2)
            geom["post_square_m"] = 0.16
        else:
            geom["proud_m"] = BAND_PROUD_M

        # THE DATUM, and it is not the same one for every mounting. A sign fixed to
        # a building is measured from the base of that building's walls — the LOWEST
        # of a 5x5 grid of terrain samples under the footprint, which is where
        # buildings.js puts the walls, and any other rule floats a board off its own
        # wall on sloping ground. A POST is not on the building: it stands in the
        # street, on the ground under itself, so its head is measured from there and
        # `arm_height_m` says nothing about it.
        head_y = _round(head, 2)
        datum = ("the base of this building's walls — the lowest of a 5x5 terrain "
                 "grid over the footprint, as buildings.js sets it")
        if mounting == "facade_painted":
            # A PAINTED NAME GOES ABOVE THE DOOR HEAD, which a hung board does not
            # have to think about. `head` is the eave-clear height a BOARD hangs at
            # — 2.55 m at most, because a board is a thing at human height over the
            # footway — and a band painted there lands across the doorway of every
            # frontage that has one, behind any surround that stands proud of the
            # wall. So a band sits with its foot at BAND_FOOT_M, clear of a door
            # head, and drops back under the eave only where the wall has not the
            # height for both. Nothing here is a record's: it is where paint goes
            # on a front, which is a drawing decision.
            top = min(BAND_FOOT_M + h, wall - BAND_EAVE_CLEAR_M)
            head_y = _round(max(top, h + 0.4), 2)
        if mounting == "post_board":
            datum = ("the ground under the post itself, sampled where it stands: the "
                     "post is in the street, not on the building. `post_height_m` is "
                     "its head over that ground and `arm_height_m` does not apply")

        signs.append({
            "structure_id": sid,
            "name": cand["name"],
            "sign_text": text,
            "sign_text_from": text_from,
            "sign_text_confidence": "reconstructed",
            "trade": cand["trade"],
            "trade_confidence": cand["grade"],
            "trade_class": cand["cls"],
            "why_a_board": PUBLIC_TRADES.get(cand["trade"])
            or WORKS_TRADES[cand["trade"]],
            "confidence": "reconstructed",
            "mounting": mounting,
            "mounting_note": "; ".join(mount_notes) or None,
            "style": style,
            "anchor_local_enu_m": [_round(e, 2), _round(n, 2)],
            "facade_bearing_deg": _round(bearing, 1),
            "arm_height_m": head_y,
            "height_datum": datum,
            "board_w_m": _round(w, 2),
            "board_h_m": _round(h, 2),
            "board_thickness_m": BOARD_T_M,
            "geometry": geom,
            "reach_m": _round(_reach(mounting, w, geom), 2),
            "wall_height_m": _round(float(wall), 2),
            "wall_height_from": wall_from,
            "frontage_m": _round(frontage, 2),
            "ground_quad_local_enu_m": [[_round(p[0], 2), _round(p[1], 2)]
                                        for p in quad],
        })

    return signs, refused


def record(signs: list, refused: list) -> dict:
    mounts: dict[str, int] = {}
    for s in signs:
        mounts[s["mounting"]] = mounts.get(s["mounting"], 0) + 1
    return {
        "_doc": (
            "The town's business signs. NOT structure records and NOT geometry that "
            "comes out of Blender: a board is a plank on a bracket, a hood, a post or "
            "a wall this project has already drawn, and a painted name is paint on a "
            "wall it has already drawn, so all of it is derived from the committed "
            "footprint and placement and drawn at load by "
            "renderers/web/js/signage.js — the same argument that lets the enclosure "
            "layer draw a fence from a perimeter. Generated by "
            "tools/generate_business_signboards.py and re-derived byte for byte by "
            "tools/check.sh, because 'which frontage gets a sign, what it says, how it "
            "hangs and what colour it is' is a rule and a rule has to be auditable."
        ),
        "id": "town_business_signboards",
        "name": "Signs on the town's business frontages",
        "kind": "signage",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same frame "
            "data/enclosures/ and the sidecars' placement.local_e / local_n use."
        ),
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": ["drloih_wolf_point", "chicago_democrat_1833_11_26"],
            "note": (
                "NO SOURCE STATES THAT ANY OF THESE PARTICULAR BUILDINGS CARRIED A "
                "SIGN, and this record never says one does. What is held is the "
                "bound: one Chicago business of these years is attested to have hung "
                "a sign — the Wolf Point Tavern's painted wolf, by about 1833 — and "
                "the town's first newspaper, 26 November 1833, is full of businesses "
                "trading under names at named addresses, in a settlement whose own "
                "sources describe its houses being known BY their signs (the Wolf "
                "Point house is 'under the sign of the Travelers' Home'; the Exchange "
                "Coffee House's later 'Illinois Exchange' is recorded as a change of "
                "sign). A named trade on a public street announced itself, and how it "
                "did so in 1830s America is not in dispute. That is a reconstruction "
                "in this project's third tier, not an attestation, and it is graded "
                "and claimed as one: docs/LIBERTIES.md L130 for the fact of a sign, "
                "L158 for its wording, its mounting and its colours. THE GREEN TREE "
                "PLATE IS NOT PART OF THE ARGUMENT — docs/ROADMAP.md K5 (b) cites its "
                "hanging sign, but data/sources/chm_green_tree_1859.json records that "
                "the image has never been seen and is unverified, so it underwrites "
                "nothing here."
            ),
        },
        "lettering": {
            "value": "the name the dataset gives the location, painted on the sign",
            "confidence": "reconstructed",
            "geometry": "canvas texture, drawn at load",
            "note": (
                "DRAWN SINCE 2026-08-21, AND THE REVERSAL IS THE OWNER'S. This block "
                "used to read 'NOT DRAWN, AND THAT IS THE WHOLE DISCIPLINE OF THIS "
                "LAYER', on L25's reasoning generalised: no source gives the wording "
                "of any sign in this town, so every board stayed a blank plank. The "
                "owner's instruction of 2026-08-18 overrules it — 'you can and should "
                "put the name of the location on the sign board … it is fine if they "
                "are reconstructions' — and this project's own standing ruling covers "
                "the tier: 'you are totally fine to be liberal with adding "
                "reconstructed items when i ask for things, you can just label and "
                "mark them as such.' So the WORDING on each sign is the name this "
                "dataset already gives that location (`sign_text`, and the card a "
                "visitor opens by tapping the sign shows the same words), and it is "
                "graded `reconstructed` — the name is the project's, the decision that "
                "a signwriter painted it is not anybody's record. The LETTERFORM, the "
                "colours and the panel come from `style`, a table of the combinations "
                "the trade worked in rather than of anything Chicago recorded. "
                "docs/LIBERTIES.md L158. What is NOT drawn, still: an image or a trade "
                "device on any board. L25 stands for the wolf, and no source describes "
                "the painting on any other."
            ),
        },
        "treatment": {
            "confidence": "reconstructed",
            "note": (
                "Five mountings, chosen by the trade's class and de-conflicted against "
                "every sign within "
                f"{NEIGHBOUR_M:.0f} m so that no two neighbours hang alike: "
                "`bracket_board` (the wolf sign's own geometry — a plank hung by two "
                "straps 0.20 m under a 1.15 m bracket arm, 1.7 m to one side of the "
                "facade's centre and clear of the eave), `awning_board` (the same "
                f"plank under a hood {AWNING_PROJECTION_M} m deep that falls "
                f"{AWNING_DROP_M} m to its outer edge), `wall_board` (a board fixed "
                "flat on the front under a cap), `post_board` (a pole at the street "
                f"edge {POST_STAND_M} m out from the wall, with a cross-arm and the "
                "board under it — the Green Tree's own arrangement, T-0082) and "
                "`facade_painted` (the name straight onto the boards of the building, "
                "no board at all — what image 5 of the owner's brief shows across the "
                f"Tremont's row, standing with its foot {BAND_FOOT_M} m up so it "
                "clears a door head, or lower where the wall has not the height for "
                f"that and {BAND_EAVE_CLEAR_M} m of eave besides). Not one of those "
                "numbers is a record's. A sign's "
                "SIZE is derived from the length of its own name inside the range its "
                "mounting allows and inside the frontage it stands on; its `aspect` "
                "comes from its style, so two boards on one street are not the same "
                "rectangle either."
            ),
            "mountings": {k: mounts[k] for k in sorted(mounts)},
        },
        "rule": {
            "note": (
                "A named record (not inf_/recon_, not 'Reconstructed'), a trade this "
                "project will announce — a PUBLIC TRADE whose customer arrived on foot "
                "off the street, which gets a board, or a WORKS OR WAREHOUSE trade "
                "whose custom came by name and by cart, which gets its firm painted on "
                "the front — that trade attested or inferred rather than "
                "reconstructed, standing on the scene date, no sign on the record "
                "already, no named board already standing on a post at its corner on "
                "the frontage layer, and (for a works only) a proprietor in its own "
                "name. Read the clauses and their reasons in "
                "tools/generate_business_signboards.py."
            ),
            "public_trades": sorted(PUBLIC_TRADES),
            "works_trades": sorted(WORKS_TRADES),
            "mounting_cycles": MOUNTING_CYCLE,
            "styles": [s["id"] for s in STYLES],
            "neighbour_m": NEIGHBOUR_M,
            "excluded_trades_note": (
                "Stables, churches, schools, the court-house, the jail, the agency "
                "house, the fort and every dwelling are outside both trade lists. A "
                "stable is the yard of the house that owns it and announces nothing of "
                "its own; the rest are not trades. Frederick Thomas's shop is refused "
                "one clause further down, because its own record says no source reached "
                "says what he sold."
            ),
        },
        "signs": signs,
        "refused": refused,
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: a Chicago or Cook County "
            "sign ordinance of the 1830s; an insurance, tax or sale description naming "
            "a shop sign; any of the pre-fire photographs of a surviving 1830s "
            "frontage actually being opened at its holding institution (the Green Tree "
            "1859 plate, ICHi-040230, is the nearest and is unseen); or a traveller's "
            "account of walking South Water Street. Any one of those would let a sign "
            "here be regraded record by record — and one that gave a WORDING, a COLOUR "
            "or a MOUNTING for a named house would be the first thing this project has "
            "ever held that could take one of these three off the reconstructed tier."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()
    signs, refused = build_record()
    text = json.dumps(record(signs, refused), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists():
            print(f"SIGNBOARD DRIFT\n  - {OUT.relative_to(ROOT)} is missing")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"SIGNBOARD DRIFT\n  - {OUT.relative_to(ROOT)} has drifted from the "
                  f"rule in tools/generate_business_signboards.py")
            return 1
        print(f"verified {len(signs)} business signs "
              f"({len(refused)} frontage(s) refused with a reason)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(signs)} business signs "
          f"({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
