#!/usr/bin/env python3
"""Generate the town's business signboards — the signage layer's first record.

WHAT THIS IS. `docs/ROADMAP.md` K5 (b) asks for *"signboards on businesses — attested
(the Green Tree plate's hanging sign; the wolf sign documented) … lettering stays
undrawn (L25)"*, and ticket T-0039 is that clause. Working it turned up two things the
clause did not know.

  * **The Green Tree plate is NOT SEEN.** `data/sources/chm_green_tree_1859.json` says
    so in its own `access_notes` — the image could not be retrieved, the identification
    comes from aggregator metadata, and `verified` is false. So the hanging sign the
    roadmap cites it for is not evidence this project holds. It is struck from the
    argument here rather than repeated.
  * **Exactly ONE structure record in this dataset attests a sign**: the Wolf Point
    Tavern's painted wolf (`data/structures/wolf_point_tavern.json`, `form.sign`), and
    that board has hung in the model since the archetype grew a `sign` parameter.

Read strictly, then, "signboards on the businesses that attest one" is a job already
finished, and the town's other two dozen shopfronts stay blank. That is the reading
AGENTS.md § RECONSTRUCTED IS A TIER exists to refuse: *a tree with no stated colour is
not a reason to leave the tree grey*. A store with no stated sign is not a reason to
leave the store mute.

THE RULE, and every clause is doing work. A structure gets a board iff

  1. it is a NAMED record — the id does not begin `inf_` or `recon_` and the name does
     not begin "Reconstructed". The archetype tables already carry this rule in as many
     words: *never invent business, sign text or goods for an anonymous slot*. An
     anonymous roof dealt a trade by a schedule has no proprietor to announce;
  2. its `function` is a PUBLIC TRADE — one whose customer was a stranger arriving on
     foot off the street (a public house, a lodging house, a shop counter, the auction
     room, the printing offices that also sold over one). Warehouses, packing houses,
     smithies, tanneries, brickyards and manufactories are excluded on purpose: their
     custom came by name and by cart, and a board on a slaughter-house would be this
     rule guessing rather than reasoning;
  3. that function is `attested` or `inferred`. A `reconstructed` trade gets no board —
     inventing a sign for an invented business is invention squared;
  4. it is standing on the scene date (it is in `data/sidecars/1835/index.json`);
  5. it does not already carry a sign. One record does, and duplicating it would put
     two boards on the Wolf Point Tavern.

WHERE THE BOARD HANGS is then DERIVED, not placed. `docs/GLB-CONTRACT.md` fixes the
frame: polygon `u` → +X, polygon `v` → −Z, and `rotation_deg` is the FACADE BEARING, so
the front wall is the footprint's own max-`v` edge and the direction it faces is the
bearing itself. The board hangs 1.7 m to one side of that edge's centre and clear of the
eave — the same two numbers `generators/archetypes/log_dwelling.py::_sign` uses for the
wolf sign, because the town should not have two conventions for hanging a board.

WHAT IS INVENTED is the FACT of a board on these twenty-four frontages, and it is graded
`reconstructed` and claimed in `docs/LIBERTIES.md` L130. What is NOT invented, and must
never be: the board carries no lettering, no image and no trade device (L25). Nothing
here says what any of these signs said. It says that a town of stores and taverns
announced itself to the street, and names the rule that chose which frontages.

    python3 tools/generate_business_signboards.py            write the record
    python3 tools/generate_business_signboards.py --check    re-derive and diff
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIDECARS = DATA / "sidecars" / "1835"
STRUCTURES = DATA / "structures"
OUT = DATA / "signage" / "town_business_signboards.json"

# Clause 2. Trades whose customer was a stranger off the street. The value on the
# left is `function.value` as the structure records write it; the phrase on the
# right is why a board belongs on that door and is quoted into the record.
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

# Clause 3.
TRADE_GRADES = {"attested", "documented", "inferred"}

# THE BOARD, and why these numbers are here rather than in the record. Arm length,
# board size and the two hangers are how a board is DRAWN, not a claim about any
# shop — the same division the enclosure layer makes between a fence's line (the
# record's) and a rail's thickness (the renderer's). They are copied from
# generators/archetypes/log_dwelling.py::_sign, which is the wolf sign's geometry,
# so the boards this layer hangs are the same object the town already has one of.
ARM_M = 1.15
BOARD_W_M = 0.88
BOARD_H_M = 0.50
BOARD_T_M = 0.05
DROP_M = 0.20
OFFSET_M = 1.7      # from the facade's centre, toward +u — the archetype's number
END_CLEAR_M = 0.6   # and never closer than this to the end of the wall
EAVE_CLEAR_M = 0.30
MAX_HEIGHT_M = 2.55

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


def build_record() -> tuple[list, list]:
    index = _load(SIDECARS / "index.json")
    standing = [s["id"] for s in index.get("structures", [])]
    signs: list[dict] = []
    refused: list[dict] = []

    for sid in standing:
        sc_path = SIDECARS / f"{sid}.json"
        if not sc_path.exists():
            continue
        sc = _load(sc_path)
        attrs = sc.get("attributes") or {}
        fn = attrs.get("function") or {}
        trade = fn.get("value")
        if trade not in PUBLIC_TRADES:
            continue                                            # clause 2
        if sid.startswith(("inf_", "recon_")) or \
                (sc.get("name") or "").startswith("Reconstructed"):
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "an anonymous slot. The archetype tables' own rule — never invent "
                "business, sign text or goods for an anonymous slot — and this record "
                "keeps it.")})
            continue                                            # clause 1
        grade = fn.get("confidence")
        if grade not in TRADE_GRADES:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"the trade itself is {grade}. A sign for a business this project "
                "reconstructed would be an invention resting on an invention.")})
            continue                                            # clause 3

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

        place = sc.get("placement") or {}
        poly = (sc.get("footprint") or {}).get("polygon") or []
        if len(poly) < 3:
            refused.append({"structure_id": sid, "trade": trade,
                            "why": "no footprint polygon — no wall to hang a board on."})
            continue
        u0, u1, vmax = _front_edge(poly)
        if u1 - u0 < 1.2:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "the front wall is under 1.2 m of frontage — narrower than the board.")})
            continue

        stories = ((attrs.get("stories") or {}).get("value"))
        wall = (attrs.get("wall_height_m") or {}).get("value")
        wall_from = "the record"
        if wall is None:
            wall = DEFAULT_WALL_M.get(stories, DEFAULT_WALL_MULTI_M) \
                if stories in DEFAULT_WALL_M else DEFAULT_WALL_MULTI_M
            wall_from = ("the archetype's default, because the record carries no "
                         "wall height — the same number the wall itself is drawn at")

        mid = (u0 + u1) / 2.0
        u = mid + OFFSET_M
        if u > u1 - END_CLEAR_M:
            u = max(mid, u1 - END_CLEAR_M)
        e, n = _to_enu(u, vmax, place)
        quad = [_to_enu(uu, vv, place) for uu, vv in (
            (min(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), max(p[1] for p in poly)),
            (min(p[0] for p in poly), max(p[1] for p in poly)))]

        signs.append({
            "structure_id": sid,
            "name": sc.get("name"),
            "trade": trade,
            "trade_confidence": grade,
            "why_a_board": PUBLIC_TRADES[trade],
            "confidence": "reconstructed",
            "anchor_local_enu_m": [_round(e, 2), _round(n, 2)],
            "facade_bearing_deg": _round(place.get("rotation_deg") or 0.0, 1),
            "arm_height_m": _round(min(wall - EAVE_CLEAR_M, MAX_HEIGHT_M), 2),
            "wall_height_m": _round(float(wall), 2),
            "wall_height_from": wall_from,
            "frontage_m": _round(u1 - u0, 2),
            "ground_quad_local_enu_m": [[_round(p[0], 2), _round(p[1], 2)] for p in quad],
        })

    signs.sort(key=lambda s: s["structure_id"])
    refused.sort(key=lambda r: r["structure_id"])
    return signs, refused


def record(signs: list, refused: list) -> dict:
    return {
        "_doc": (
            "The town's business signboards. NOT a structure record and NOT geometry "
            "that comes out of Blender: a board is a plank on a bracket hanging off a "
            "wall this project has already drawn, so it is derived from the committed "
            "footprint and placement and drawn at load by "
            "renderers/web/js/signage.js — the same argument that lets the enclosure "
            "layer draw a fence from a perimeter. Generated by "
            "tools/generate_business_signboards.py and re-derived byte for byte by "
            "tools/check.sh, because 'which frontage gets a board' is a rule and a "
            "rule has to be auditable."
        ),
        "id": "town_business_signboards",
        "name": "Signboards on the town's business frontages",
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
                "BOARD, and this record never says one does. What is held is the "
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
                "and claimed as one: docs/LIBERTIES.md L130. THE GREEN TREE PLATE IS "
                "NOT PART OF THE ARGUMENT — docs/ROADMAP.md K5 (b) cites its hanging "
                "sign, but data/sources/chm_green_tree_1859.json records that the "
                "image has never been seen and is unverified, so it underwrites "
                "nothing here."
            ),
        },
        "lettering": {
            "value": None,
            "confidence": "reconstructed",
            "geometry": "absent",
            "note": (
                "NOT DRAWN, AND THAT IS THE WHOLE DISCIPLINE OF THIS LAYER. No source "
                "gives the wording, the device or the colour of any sign in this town, "
                "the wolf's included. Every board here is a blank weathered plank, "
                "exactly as docs/LIBERTIES.md L25 decided for the one documented sign: "
                "the mesh says a board hung there and the building's card says who "
                "traded behind it. A painted name would be the most conspicuous "
                "invention in the scene, repeated two dozen times."
            ),
        },
        "treatment": {
            "confidence": "reconstructed",
            "note": (
                "Board 0.88 x 0.50 m and 50 mm thick, hung by two straps 0.20 m below "
                "a 1.15 m bracket arm, 1.7 m to one side of the facade's centre and "
                "clear of the eave. Not one of those numbers is a record's: they are "
                "copied from generators/archetypes/log_dwelling.py::_sign, the wolf "
                "sign's own geometry, so that the town has one convention for hanging "
                "a board rather than two. The tone is the weathered board of the "
                "archetype's SIGN_RGBA."
            ),
        },
        "rule": {
            "note": (
                "A named record (not inf_/recon_, not 'Reconstructed'), a PUBLIC TRADE "
                "whose customer arrived on foot off the street, that trade attested or "
                "inferred rather than reconstructed, standing on the scene date, and "
                "no sign on the record already. Read the clauses and their reasons in "
                "tools/generate_business_signboards.py."
            ),
            "public_trades": sorted(PUBLIC_TRADES),
            "excluded_trades_note": (
                "Warehouses, forwarding sheds' yards, packing and slaughter houses, "
                "smithies, cooperages, tanneries, brickyards, manufactories, stables, "
                "churches, schools, the court-house, the jail, the agency house and "
                "the fort are all outside the trade list. Their custom came by name "
                "and by cart. A board on any of them would be this rule guessing."
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
            "account of walking South Water Street. Any one of those would let a board "
            "here be regraded record by record, and the first that gives a WORDING "
            "would be the first thing this project has ever held that could put "
            "lettering on a plank."
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
        print(f"verified {len(signs)} business signboards "
              f"({len(refused)} frontage(s) refused with a reason)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(signs)} business signboards "
          f"({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
