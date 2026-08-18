#!/usr/bin/env python3
"""Generate the Green Tree's frontage works — its plank walks, its board crossing
and the named board on its own post.

WHAT THIS IS. Ticket **T-0082**, the third of the four pieces T-0042 (*image-accuracy
pass: the Green Tree Tavern*) was split into. Two of the owner's reference views of this
inn describe the ground in front of it, and neither of them is furniture standing in a
yard — they are the STREET side of the building:

  * image 6, the Braunhold engraving of 1838: *"post-mounted hanging signboard at the
    corner; plank sidewalks with board crossings"*;
  * image 7, the Trowbridge drawing: *"the hanging 'GREEN TREE' sign on its post"*, and
    a dirt road with grass verges.

Both are read from `data/sources/assets/owner_brief_2026_08_18/README.md`, which is the
written record of eleven owner-supplied reference images. They are **tier 5 pictorial**:
they may drive massing, materials, furniture and setting, and they may never drive a
coordinate. So WHAT stands here comes from the plates and WHERE is derived from the
committed footprint, the committed placement and the committed street corridor — the
same division `tools/generate_yard_goods.py` keeps for the same building's yard.

WHY IT IS A LAYER OF ITS OWN rather than more yard goods. A barrel or a wagon stands on
a building's own ground and is derived from its walls alone. A walk and a crossing stand
in the STREET, and the number that decides where they may lie is the street's — the
travelled track's own half-width out of `data/streets/1835.json`. This record is the
first thing in the project derived from a building and a street at once, and tickets
T-0066 (a board carrying its location's name) and T-0069 (fences and plank sidewalks
along the streets) are the town-wide standards it sets at one building.

THE LETTERING, and it is the one decision in this parcel that needed arguing rather
than deriving. `docs/LIBERTIES.md` L25 decided that the town's one documented sign — the
Wolf Point Tavern's painted wolf — is drawn as a blank board, because no description of
the painting survives, and L130 applied that to all twenty-four boards the signage layer
hangs. **That reasoning does not reach this board.** L25's subject is an IMAGE nobody has
described; this board's subject is a NAME, the plate states it in as many words, and the
name is already in this repository as `data/structures/green_tree_tavern.json` `name`.
Refusing to letter it would not be caution, it would be discarding evidence the project
holds — which is precisely the reading AGENTS.md § RECONSTRUCTED IS A TIER exists to
refuse. So the board carries GREEN TREE, the wording is graded `inferred` against the
plate, and what stays invented is the LETTERFORM: the face, the size, the spacing and
the colour, none of which any source gives. That split is L135.

THE WALL BOARD THIS REPLACES. `tools/generate_business_signboards.py` hangs a blank
board on the Green Tree's front wall by rule (L130). The plates show ONE board at this
inn and it is on a post at the corner, so that generator now refuses this frontage in
writing rather than the town drawing the same claim twice.

    python3 tools/generate_frontage_works.py            write the record
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
OUT = DATA / "frontage" / "green_tree_frontage.json"

# The building. One record for now, and the rule below is written so that the second
# and the twentieth cost nothing but a line here (T-0069).
STRUCTURE_ID = "green_tree_tavern"
SIGN_TEXT = "GREEN TREE"

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

# A wall only gets a walk if a street is actually there. The corridor is 80 ft and the
# buildings sit on its edge, so a frontage wall is within half of it of the centreline;
# a wall further off than this is a yard wall and gets nothing.
STREET_REACH_M = 22.0


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


def _street_facing(mid, normal, streets: dict) -> tuple[str | None, dict, float]:
    """Which street a wall faces: the nearest centreline that lies OUTWARD of it.

    Outward is the test that matters. A rear wall can be as close to a street as a
    front wall is to another one, and a walk laid on the wrong side of a building
    would be a walk through its own yard.
    """
    best = (None, {}, float("inf"))
    for sid, st in streets.items():
        if len(st["path"]) < 2:
            continue
        d, foot = _nearest_on_path(mid, st["path"])
        outward = (foot[0] - mid[0]) * normal[0] + (foot[1] - mid[1]) * normal[1]
        if outward <= 0 or d > STREET_REACH_M:
            continue
        if d < best[2]:
            best = (sid, st, d)
    return best


def build() -> tuple[list, list, list]:
    """The walks, the crossings and the posts, with every refusal stated."""
    walks: list = []
    posts: list = []
    refused: list = []

    sc_path = SIDECARS / f"{STRUCTURE_ID}.json"
    if not sc_path.exists():
        return [], [], [{"structure_id": STRUCTURE_ID, "why": (
            "the inn is not standing in data/sidecars/1835 — nothing is laid on its "
            "frontage.")}]
    sc = _load(sc_path)
    place = sc.get("placement") or {}
    poly = (sc.get("footprint") or {}).get("polygon") or []
    if place.get("local_e") is None or len(poly) < 3:
        return [], [], [{"structure_id": STRUCTURE_ID, "why": (
            "the inn has no placed footprint — no frontage can be derived.")}]

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
        sid, st, dist = _street_facing(mid, normal, streets)
        if sid is None:
            refused.append({"structure_id": STRUCTURE_ID, "wall": label, "why": (
                f"no street centreline lies outward of this wall within "
                f"{STREET_REACH_M:.0f} m — a walk here would be a walk through the "
                "inn's own yard.")})
            continue
        off = WALK_CLEAR_M + WALK_W_M / 2.0
        centre_a = (a[0] + normal[0] * off, a[1] + normal[1] * off)
        centre_b = (b[0] + normal[0] * off, b[1] + normal[1] * off)
        # A walk must lie on the near side of the travelled way, never in it.
        edge = dist - (WALK_CLEAR_M + WALK_W_M) - st["track_w"] / 2.0
        if edge <= 0:
            refused.append({"structure_id": STRUCTURE_ID, "wall": label, "why": (
                f"the {st['name']} track reaches to within {dist:.2f} m of this wall "
                f"and a {WALK_W_M:.2f} m walk laid off it would lie in the travelled "
                "way — no walk is laid.")})
            continue
        laid[label] = {"normal": normal, "along": along, "street": sid, "dist": dist,
                       "track_w": st["track_w"], "a": centre_a, "b": centre_b}
        walks.append({
            "id": f"{STRUCTURE_ID}_walk_{label}",
            "belongs_to": STRUCTURE_ID,
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
                "A PLANK WALK ON THE INN'S FRONTAGE, and the plates are the whole "
                "reason it is here. The Braunhold engraving of the Green Tree "
                "(data/sources/assets/owner_brief_2026_08_18/README.md, image 6) shows "
                "plank sidewalks with board crossings at this building — a tier-5 "
                "retrospective view, which may drive setting and may never drive a "
                "coordinate. So WHERE is derived: the deck lies "
                f"{WALK_CLEAR_M:.2f} m off the {label} wall, {WALK_W_M:.2f} m wide, "
                f"leaving {edge:.2f} m of verge between its outer edge and the "
                f"{st['name']} track — which is the number that decides a walk may lie "
                "here at all. What is invented is the width, the rise, the plank "
                "pitch, and that a walk stood on this ground at noon on 1 July 1835: "
                "docs/LIBERTIES.md L135."
            ),
        })

    # ---- the crossing ------------------------------------------------------ #
    # Over the street the FRONT wall faces, springing from the front walk at the
    # corner end — which is where a crossing is, because a crossing joins corners.
    front = laid.get("front")
    if front is None:
        refused.append({"structure_id": STRUCTURE_ID, "wall": "front", "why": (
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
            "id": f"{STRUCTURE_ID}_crossing_front",
            "belongs_to": STRUCTURE_ID,
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
                "A BOARD CROSSING OVER THE STREET. Image 6 gives *plank sidewalks with "
                "board crossings* at this inn and image 8 the same at the Sauganash, so "
                "the fact is the plates' and every dimension is invented. Its boards run "
                "the way a foot travels rather than across it, which is what a crossing "
                "is FOR — it spans the ruts instead of lying in them; a walk's boards "
                "run the other way. WHERE is derived: it leaves the front walk's outer "
                f"edge and runs {run:.2f} m, which is the walk's own verge plus half the "
                f"{streets[front['street']]['name']} track plus "
                f"{CROSSING_MARGIN_M:.2f} m onto the dry ground beyond it, so it reaches "
                "across the travelled way rather than stopping in it. It lies lower than "
                "the walk because a wheel crosses it. docs/LIBERTIES.md L135."
            ),
        })

    # ---- the board on its post --------------------------------------------- #
    # AT THE CORNER, in the verge outside both walks. Image 6 says *at the corner*
    # and image 7 draws it on a post, so the corner is the plates' and the stand is
    # derived from the two walks that meet there.
    left = laid.get("left")
    if front is None or left is None:
        refused.append({"structure_id": STRUCTURE_ID, "wall": "corner", "why": (
            "the post stands at the corner two walks make, and one of the two was "
            "refused — no board is put on a post.")})
    else:
        out_f = WALK_CLEAR_M + WALK_W_M + POST_VERGE_M
        out_l = WALK_CLEAR_M + WALK_W_M + POST_VERGE_M
        at = (corner_world[0] + front["normal"][0] * out_f + left["normal"][0] * out_l,
              corner_world[1] + front["normal"][1] * out_f + left["normal"][1] * out_l)
        reach = front["dist"] - out_f - front["track_w"] / 2.0
        if reach <= 0:
            refused.append({"structure_id": STRUCTURE_ID, "wall": "corner", "why": (
                f"a post {out_f:.2f} m out from the front wall would stand in the "
                f"{streets[front['street']]['name']} track — no board is put on a "
                "post.")})
        else:
            bearing = float(place.get("rotation_deg") or 0.0)
            posts.append({
                "id": f"{STRUCTURE_ID}_sign_post",
                "belongs_to": STRUCTURE_ID,
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
                "text": SIGN_TEXT,
                "text_confidence": "inferred",
                "text_sources_note": (
                    "data/sources/assets/owner_brief_2026_08_18/README.md, image 7 — "
                    "the Trowbridge drawing of this inn, described there as 'the "
                    "hanging \"GREEN TREE\" sign on its post'. The plate is not held "
                    "as a source record yet; T-0075 owns making one, and until it does "
                    "the citation is a committed path rather than a source_id."
                ),
                "clear_of_track_m": _round(reach),
                "note": (
                    "THE NAMED BOARD ON ITS POST, at the corner of the two streets. "
                    "Image 6 puts a post-mounted hanging signboard at this inn's "
                    "corner and image 7 says what is on it. WHERE is derived: the post "
                    f"stands {out_f:.2f} m out from each of the two walls that make "
                    "the corner — clear of both walks by "
                    f"{POST_VERGE_M:.2f} m — with {reach:.2f} m still between it and "
                    "the travelled track. Its cross-arm runs along the front wall away "
                    "from the corner, so the board's face looks down the street the "
                    "inn fronts on. The pole, the arm and the board are invented in "
                    "every dimension, and so is the letterform; the WORDING is the "
                    "plate's. docs/LIBERTIES.md L135."
                ),
            })

    walks.sort(key=lambda w: w["id"])
    posts.sort(key=lambda p: p["id"])
    refused.sort(key=lambda r: (r["structure_id"], r.get("wall", "")))
    return walks, posts, refused


def record(walks: list, posts: list, refused: list) -> dict:
    return {
        "_doc": (
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
        "id": "green_tree_frontage",
        "name": "The Green Tree's frontage: plank walks, a board crossing, and its named board on a post",
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
            "note": (
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
        },
        "lettering": {
            "value": SIGN_TEXT,
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
        "treatment": {
            "confidence": "reconstructed",
            "note": (
                f"Walk {WALK_W_M} m wide, {WALK_CLEAR_M} m off the wall, its deck "
                f"{WALK_RISE_M} m over the ground, {PLANK_T_M} m boards at a "
                f"{PLANK_PITCH_M} m pitch laid ACROSS the way a foot travels. Crossing "
                f"{CROSSING_W_M} m wide and {CROSSING_PLANKS} boards laid ALONG it, "
                "reaching past the far edge of the travelled track by "
                f"{CROSSING_MARGIN_M} m. Post {POST_H_M} m tall and {POST_SQ_M} m "
                f"square, a {ARM_M} m cross-arm at its head, and a "
                f"{BOARD_W_M} x {BOARD_H_M} m board hanging {HANGER_DROP_M} m under "
                "the arm. Not one of those numbers is a record's; they are how the "
                "layer is DRAWN, the division the enclosure layer makes between a "
                "fence's line and a rail's thickness."
            ),
        },
        "rule": {
            "note": (
                "A wall gets a walk iff a street centreline lies OUTWARD of it within "
                f"{STREET_REACH_M:.0f} m and the walk's outer edge still clears that "
                "street's own travelled track; a crossing springs from the walk on the "
                "wall the building fronts on and runs until it is past the far edge of "
                "the track; the post stands at the corner the front and left walls "
                "make, outside both walks and clear of the track. Every wall that is "
                "refused says which test refused it. Read the clauses and their "
                "reasons in tools/generate_frontage_works.py."
            ),
            "street_reach_m": STREET_REACH_M,
        },
        "walks": walks,
        "posts": posts,
        "refused": refused,
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
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()
    walks, posts, refused = build()
    text = json.dumps(record(walks, posts, refused), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists():
            print(f"FRONTAGE DRIFT\n  - {OUT.relative_to(ROOT)} is missing")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"FRONTAGE DRIFT\n  - {OUT.relative_to(ROOT)} has drifted from the "
                  f"rule in tools/generate_frontage_works.py")
            return 1
        print(f"verified {len(walks)} walk/crossing run(s) and {len(posts)} sign post(s) "
              f"({len(refused)} wall(s) refused with a reason)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(walks)} walk/crossing run(s), "
          f"{len(posts)} sign post(s) ({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
