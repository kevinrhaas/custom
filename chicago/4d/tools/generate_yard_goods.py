#!/usr/bin/env python3
"""Generate the goods standing at the town's trading frontages — the yard layer.

WHAT THIS IS. `docs/ROADMAP.md` K5 (c) asks for *"yard objects: wagons/drays …, crates
and barrels at the stores"*, and ticket T-0040 is that clause for the taverns and the
stores. Unlike the signboards one layer over, this one does not start from silence: the
town legislated about it.

THE EVIDENCE, AND IT IS AN ORDINANCE. `data/sources/chicago_democrat_1833_11_26.json`
carries the village ordinances of 7 November 1833 complete, and **Ordinance 9 is about
timber, stone, brick, boxes and barrels stacked in the streets**. A corporation does not
legislate against a thing nobody does. That is a tier-1 contemporary statement that
Chicago's streets in the town's own first winter had boxes and barrels standing in them,
made twenty months before the scene date and by the people who had to walk round them.

What the ordinance does NOT give is a single location. It says the town, not the corner.
So the shape of this record is the same as the pickets' and the signboards': the evidence
is a TREATMENT and the answer to "why this frontage" has to be a RULE.

THE RULE, and every clause is doing work. A frontage gets goods iff

  1. it is a NAMED record — the id does not begin `inf_` or `recon_` and the name does not
     begin "Reconstructed". The archetype tables' own rule is *never invent business, sign
     text or goods for an anonymous slot*, and it names goods explicitly;
  2. its `function` is a GOODS-KEEPING TRADE — one whose stock arrived in boxes and
     barrels off a lake schooner and stood on the ground before it went inside. The
     taverns and hotels are in for the reason the stores are: a public house takes its
     provisions in by the barrel and puts the empties back out. Smithies, tanneries,
     manufactories, stables, churches, schools, the court-house and the jail are out —
     they kept stuff, but not a merchant's stock on a public frontage;
  3. that function is `attested` or `inferred`. A `reconstructed` trade gets no goods,
     for the same reason it gets no sign: invention squared;
  4. it is standing on the scene date (it is in `data/sidecars/1835/index.json`);
  5. it stands on the TOWN's ground. The fort's provision store and the sutler's store
     are refused in writing: they are federal ground inside a palisade, outside the
     corporation whose ordinance is the whole evidence here, and there is no public
     street in front of either of them;
  6. the strip in front of its facade is clear — nothing is placed where it would stand
     inside another building's committed footprint.

WHERE THE GOODS STAND is then DERIVED, not placed, exactly as a board's anchor is.
`docs/GLB-CONTRACT.md` fixes the frame: polygon `u` → +X, polygon `v` → −Z, and
`rotation_deg` is the FACADE BEARING, so the front wall is the footprint's own max-`v`
edge. The goods stand against that wall, 0.55 m out from its plane, at the end of the
frontage the signboard does not occupy — `tools/generate_business_signboards.py` hangs
its board 1.7 m toward +u of the facade centre, so this piles the barrels from the −u end
and the door between them stays clear. How many is arithmetic on the frontage and not a
lottery: one barrel per 2.2 m of usable wall, capped at four, a crate past them once
there is 4 m of wall to hold one, and a second crate stacked on it at 7 m.

THE ONE WAGON, and why there is one rather than twenty. No source in this repository puts
a wagon at any place in this town on any day. One place is named for them:
`data/enclosures/western_hotel_wagon_yard.json`, whose attested sentence is *"In the rear
was the large stable and the yard into which the trains were driven."* So a wagon stands
in the yard the source calls a wagon yard, at the point in it derived to be furthest from
every fence line and every committed wall, and nowhere else. Scattering drays along Lake
Street would be this record inventing traffic; refusing to draw a wagon at all would leave
the one yard the town describes as a wagon yard empty. The ticket asked for wagons and
gets the one the evidence carries, with the refusal written down.

WHAT IS INVENTED is every object on this record: that these particular frontages had goods
out on 1 July 1835, how many, and what a barrel, a crate and a wagon of this place and year
looked like. All of it is graded `reconstructed` and claimed in `docs/LIBERTIES.md` L131.
What is NOT invented and must never be: no barrel carries a mark, a brand, a merchant's
name or a stencil, and no crate is labelled — the same discipline L25 and L130 keep for the
signboards, and for the same reason. Nothing here says what was in any of them.

    python3 tools/generate_yard_goods.py            write the record
    python3 tools/generate_yard_goods.py --check    re-derive and diff
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generators"))
from archetypes.frame_tavern_params import from_phase as _tavern_params  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIDECARS = DATA / "sidecars" / "1835"
STRUCTURES = DATA / "structures"
ENCLOSURES = DATA / "enclosures"
OUT = DATA / "yard" / "town_trade_goods.json"

# Clause 2. `function.value` as the structure records write it, and why goods belong on
# that ground. The phrase on the right is quoted into the record, frontage by frontage.
GOODS_TRADES = {
    "tavern_inn": "a public house takes its provisions in by the barrel and puts the empties back out",
    "hotel": "a public house takes its provisions in by the barrel and puts the empties back out",
    "boarding_house": "a lodging house is fed out of the same barrels a tavern is",
    "store": "a counter whose stock arrives in boxes and barrels off a lake schooner",
    "store_residence": "a counter whose stock arrives in boxes and barrels off a lake schooner",
    "store_and_dwelling": "a counter whose stock arrives in boxes and barrels off a lake schooner",
    "dwelling_and_store": "a counter whose stock arrives in boxes and barrels off a lake schooner",
    "dwelling_and_trading_house": "a trading house's stock stands on the ground before it goes inside",
    "grocery_and_provision_store": "provisions are sold out of the barrel they arrived in",
    "drug_store": "a counter whose stock arrives in boxes and barrels off a lake schooner",
    "printing_office_and_store": "an office that sold over a counter, and paper travels in cases",
    "forwarding_and_commission_store": "a forwarding house IS goods standing between a vessel and a wagon",
    "forwarding_commission_warehouse": "a forwarding house IS goods standing between a vessel and a wagon",
    "auction_room": "an auction's lots stand out where they can be looked over",
}

# Clause 3.
TRADE_GRADES = {"attested", "documented", "inferred"}

# Clause 5. Federal ground inside the palisade. The corporation's ordinance is the whole
# evidence on this record and it did not reach these two doors.
FORT_TRADES = {"provision store", "sutler's store"}

# THE OBJECTS, and why their sizes are here rather than on the record. A barrel's girth
# and a crate's boards are HOW a thing is drawn, not a claim about any shop — the same
# division the enclosure layer makes between a fence's line (the record's) and a rail's
# thickness (the renderer's). They are written into the record's `form` block once, graded
# and noted there, and the renderer reads them from it.
BARREL_H_M = 0.84          # 33 in — a provision barrel on its head
BARREL_BELLY_D_M = 0.53    # 21 in at the bilge
BARREL_HEAD_D_M = 0.45     # 17.5 in at the head
CRATE_L_M = 1.05
CRATE_W_M = 0.72
CRATE_H_M = 0.62
CRATE_2_SCALE = 0.72       # the case stacked on the first one is smaller

STANDOFF_M = 0.55          # from the facade plane to the goods' own centre line
END_CLEAR_M = 0.50         # never closer than this to the end of the wall
BARREL_PITCH_M = 0.62      # centre to centre in a row: a barrel and a hand's width
MIN_FRONTAGE_M = 2.0       # under this there is no footway to stand anything on
BARREL_PER_M = 2.2         # one upright barrel per this much usable wall
BARREL_MAX = 4
CRATE_AT_M = 4.0           # usable wall before a crate is put out
CRATE2_AT_M = 7.0          # and before a second one is stacked on it
LAID_AT_M = 5.0            # a public house's empty, on its side, at this much wall

# THE WAGON. A farm wagon of the period, recorded converted from feet.
WAGON_BODY_L_M = 3.05      # 10 ft
WAGON_BODY_W_M = 1.07      # 3 ft 6 in
WAGON_BODY_H_M = 0.55
WAGON_BED_Y_M = 0.95       # the bed's underside above the ground
WAGON_REAR_WHEEL_D_M = 1.37   # 4 ft 6 in
WAGON_FRONT_WHEEL_D_M = 1.07  # 3 ft 6 in
WAGON_TONGUE_M = 2.75
WAGON_CLEAR_M = 1.6        # the half-width of ground a parked wagon needs round it

# THE GREEN TREE'S YARD — ticket T-0080, and the first place in this town where a
# PICTURE rather than a rule says what stood outside a door. The Trowbridge drawing
# of the inn (data/sources/assets/owner_brief_2026_08_18/README.md, image 7) shows
# farm wagons standing in the yard and a bench against the front wall. It is a tier-5
# retrospective view and may drive furniture and setting as this project's third tier,
# never a coordinate — so WHAT is here comes from the plate and WHERE is derived from
# the committed footprint, the same division every layer on this ground keeps.
GREEN_TREE_ID = "green_tree_tavern"
GT_WALL_CLEAR_M = 1.0      # a wagon stands this far off the rear wall it is drawn up to
GT_WAGON_MAX = 3           # the yard's own width decides the count; this is its ceiling

# THE WAGON SHED AT THE GREEN TREE — ticket T-0081, the second thing the Trowbridge
# drawing puts on this inn's ground: an OPEN-SIDED WAGON SHED with a COVERED WAGON
# standing under it. Everything here is a size, never a place; where the shed stands
# is derived from the committed footprint the same way the wagons' stands were.
GT_SHED_END_M = 0.50       # air past each end of the wagon's body, along the wall
GT_SHED_HEADROOM_M = 0.35  # clear air over the tilt at the open eave
GT_SHED_PITCH_DEG = 12.0   # the lean-to's fall, out from the wall it leans on
GT_SHED_POST_M = 0.14      # 5.5 in square posts under the open side
GT_SHED_PLATE_M = 0.16     # the plates and the rafters over them

# THE TILT — the covered wagon's canvas, on bows over the same farm wagon body the
# yard already draws. A rise and an overhang, and nothing else: the bows under it
# are not drawn for the reason the barrels' hoops are not.
WAGON_TILT_RISE_M = 1.10       # the canvas's rise over the body's top rail
WAGON_TILT_OVERHANG_M = 0.12   # the canvas pulled past the end bows

# THE BENCH. A backless plank bench, recorded converted from feet: 6 ft long, 14 in
# deep, 18 in to the seat, on two plank ends. Not one of those numbers is a record's.
BENCH_L_M = 1.83
BENCH_SEAT_D_M = 0.36
BENCH_SEAT_H_M = 0.46
BENCH_PLANK_T_M = 0.045


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _round(x: float, places: int = 2) -> float:
    """Round toward a stable decimal so `--check` diffs bytes, not float noise."""
    return round(x + 0.0, places) + 0.0


def _to_enu(u: float, v: float, place: dict) -> tuple[float, float]:
    """A footprint coordinate to local ENU metres — the signboard generator's frame.

    docs/GLB-CONTRACT.md: polygon `u` → +X, polygon `v` → −Z, ENU `local_e` → +X and
    `local_n` → −Z, and the node's yaw is `-rotation_deg` about +Y.
    """
    th = math.radians(-(place.get("rotation_deg") or 0.0))
    x, z = u, -v
    xr = x * math.cos(th) + z * math.sin(th)
    zr = -x * math.sin(th) + z * math.cos(th)
    return (place.get("local_e") or 0.0) + xr, (place.get("local_n") or 0.0) - zr


def _front_edge(polygon: list) -> tuple[float, float, float]:
    """The front wall: the footprint's max-`v` edge, as (u_min, u_max, v)."""
    vmax = max(p[1] for p in polygon)
    on = [p[0] for p in polygon if abs(p[1] - vmax) < 1e-6]
    if len(on) < 2:
        return 0.0, 0.0, vmax
    return min(on), max(on), vmax


def _footprint_world(sidecar: dict) -> list[tuple[float, float]]:
    """A committed footprint in local ENU metres, placed and rotated."""
    poly = (sidecar.get("footprint") or {}).get("polygon") or []
    place = sidecar.get("placement") or {}
    if place.get("local_e") is None or len(poly) < 3:
        return []
    return [_to_enu(u, v, place) for u, v in poly]


def _poly_contains(pt, poly) -> bool:
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def _dist_to_polygon(pt, poly) -> float:
    """Distance from a point to a polygon's boundary; negative when inside it."""
    x, y = pt
    best = float("inf")
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
        best = min(best, math.hypot(x - (x1 + t * dx), y - (y1 + t * dy)))
    return -best if _poly_contains(pt, poly) else best


def _dist_to_path(pt, path) -> float:
    """Distance from a point to an open polyline — a fence run is not a ring."""
    x, y = pt
    best = float("inf")
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
        best = min(best, math.hypot(x - (x1 + t * dx), y - (y1 + t * dy)))
    return best


def _standing() -> tuple[list[str], dict]:
    index = _load(SIDECARS / "index.json")
    ids = [s["id"] for s in index.get("structures", [])]
    cars = {}
    for sid in ids:
        path = SIDECARS / f"{sid}.json"
        if path.exists():
            cars[sid] = _load(path)
    return ids, cars


# --------------------------------------------------------------------------- #
# the frontages                                                                #
# --------------------------------------------------------------------------- #

def build_frontages(ids: list[str], cars: dict) -> tuple[list, list]:
    worlds = {sid: _footprint_world(sc) for sid, sc in cars.items()}
    frontages: list[dict] = []
    refused: list[dict] = []

    for sid in ids:
        sc = cars.get(sid)
        if sc is None:
            continue
        attrs = sc.get("attributes") or {}
        fn = attrs.get("function") or {}
        trade = fn.get("value")
        if trade in FORT_TRADES:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "it stands on federal ground inside the fort's palisade. The whole "
                "evidence on this record is the village corporation's Ordinance 9 of "
                "7 November 1833, and the corporation's streets did not reach this door; "
                "there is no public frontage in front of it to stand a barrel on. The "
                "garrison's stores are a different claim and would need a different "
                "source.")})
            continue                                            # clause 5
        if trade not in GOODS_TRADES:
            continue                                            # clause 2
        if sid.startswith(("inf_", "recon_")) or \
                (sc.get("name") or "").startswith("Reconstructed"):
            refused.append({"structure_id": sid, "trade": trade, "why": (
                "an anonymous slot. The archetype tables' own rule — never invent "
                "business, sign text or GOODS for an anonymous slot — names goods in as "
                "many words, and this record keeps it.")})
            continue                                            # clause 1
        grade = fn.get("confidence")
        if grade not in TRADE_GRADES:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"the trade itself is {grade}. Stock standing outside a business this "
                "project reconstructed would be an invention resting on an invention.")})
            continue                                            # clause 3

        place = sc.get("placement") or {}
        poly = (sc.get("footprint") or {}).get("polygon") or []
        if len(poly) < 3 or place.get("local_e") is None:
            refused.append({"structure_id": sid, "trade": trade,
                            "why": "no placed footprint — no frontage to stand goods on."})
            continue
        u0, u1, vmax = _front_edge(poly)
        run = (u1 - u0) - 2 * END_CLEAR_M
        if run < MIN_FRONTAGE_M:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"only {max(run, 0):.2f} m of usable frontage — under the "
                f"{MIN_FRONTAGE_M:.2f} m this record calls a footway.")})
            continue

        bearing = float(place.get("rotation_deg") or 0.0)
        # Out of the wall, in ENU. `rotation_deg` IS the facade bearing, so the outward
        # normal is (sin b, cos b) and the along-wall direction is the +u axis.
        b = math.radians(bearing)
        others = [(oid, w) for oid, w in worlds.items() if oid != sid and len(w) >= 3]

        def at(u_along: float) -> tuple[float, float]:
            e, n = _to_enu(u_along, vmax, place)
            return e + math.sin(b) * STANDOFF_M, n + math.cos(b) * STANDOFF_M

        items: list[dict] = []
        n_barrels = max(1, min(BARREL_MAX, int(run // BARREL_PER_M)))
        u = u0 + END_CLEAR_M + BARREL_PITCH_M / 2
        for _ in range(n_barrels):
            e, n = at(u)
            items.append({"kind": "barrel", "pose": "upright",
                          "at_local_enu_m": [_round(e), _round(n)],
                          "bearing_deg": _round(bearing, 1)})
            u += BARREL_PITCH_M
        if run >= LAID_AT_M and trade in ("tavern_inn", "hotel", "boarding_house"):
            u += 0.35
            e, n = at(u)
            items.append({"kind": "barrel", "pose": "laid",
                          "at_local_enu_m": [_round(e), _round(n)],
                          "bearing_deg": _round(bearing, 1)})
            u += 0.65
        if run >= CRATE_AT_M:
            u += CRATE_L_M / 2 + 0.15
            e, n = at(u)
            items.append({"kind": "crate", "tier": 0,
                          "at_local_enu_m": [_round(e), _round(n)],
                          "bearing_deg": _round(bearing, 1)})
            if run >= CRATE2_AT_M:
                items.append({"kind": "crate", "tier": 1,
                              "at_local_enu_m": [_round(e), _round(n)],
                              "bearing_deg": _round(bearing, 1)})
            u += CRATE_L_M / 2

        # Clause 6. Nothing stands inside a neighbour's committed footprint.
        kept, dropped = [], []
        for item in items:
            pt = tuple(item["at_local_enu_m"])
            hit = next((oid for oid, w in others if _poly_contains(pt, w)), None)
            if hit:
                dropped.append(hit)
            else:
                kept.append(item)
        if dropped:
            refused.append({"structure_id": sid, "trade": trade, "why": (
                f"{len(dropped)} object(s) fell inside "
                f"{sorted(set(dropped))[0]}'s committed footprint, which stands over "
                "this frontage's own strip; they are dropped rather than nudged, because "
                "a nudged coordinate is a placed one.")})
        if not kept:
            continue

        quad = [_to_enu(uu, vv, place) for uu, vv in (
            (min(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), min(p[1] for p in poly)),
            (max(p[0] for p in poly), max(p[1] for p in poly)),
            (min(p[0] for p in poly), max(p[1] for p in poly)))]

        frontages.append({
            "structure_id": sid,
            "name": sc.get("name"),
            "trade": trade,
            "trade_confidence": grade,
            "why_goods": GOODS_TRADES[trade],
            "confidence": "reconstructed",
            "facade_bearing_deg": _round(bearing, 1),
            "frontage_m": _round(u1 - u0),
            "usable_frontage_m": _round(run),
            "standoff_m": STANDOFF_M,
            "ground_quad_local_enu_m": [[_round(p[0]), _round(p[1])] for p in quad],
            "items": kept,
        })

    frontages.sort(key=lambda f: f["structure_id"])
    refused.sort(key=lambda r: r["structure_id"])
    return frontages, refused


# --------------------------------------------------------------------------- #
# the wagon                                                                    #
# --------------------------------------------------------------------------- #

def build_wagons(cars: dict) -> tuple[list, list]:
    """One wagon, in the yard a source calls a wagon yard, at a derived point."""
    path = ENCLOSURES / "western_hotel_wagon_yard.json"
    if not path.exists():
        return [], [{"enclosure_id": "western_hotel_wagon_yard",
                     "why": "the enclosure record is missing — no wagon is drawn."}]
    yard = _load(path)
    runs = [r.get("path_local_enu_m") or [] for r in yard.get("runs", [])]
    pts = [p for r in runs for p in r]
    if len(pts) < 3:
        return [], [{"enclosure_id": yard.get("id"),
                     "why": "the yard record carries no fence line to derive a stand from."}]
    e_lo, e_hi = min(p[0] for p in pts), max(p[0] for p in pts)
    n_lo, n_hi = min(p[1] for p in pts), max(p[1] for p in pts)

    walls = [(sid, w) for sid, w in
             ((sid, _footprint_world(sc)) for sid, sc in cars.items()) if len(w) >= 3]

    # THE STAND IS SEARCHED, NOT CHOSEN: a 0.25 m lattice over the yard's own bounding
    # box, keeping the point whose least clearance — to every committed wall and to
    # every fence line of the yard — is greatest. Ties break toward the south and then
    # the west, so the answer does not depend on iteration order.
    best, best_clear = None, -1.0
    step = 0.25
    steps_e = int((e_hi - e_lo) / step)
    steps_n = int((n_hi - n_lo) / step)
    for i in range(steps_n + 1):
        n = _round(n_lo + i * step, 3)
        for j in range(steps_e + 1):
            e = _round(e_lo + j * step, 3)
            clear = min(min(_dist_to_polygon((e, n), w) for _, w in walls),
                        min(_dist_to_path((e, n), r) for r in runs if len(r) >= 2))
            if clear > best_clear + 1e-9:
                best, best_clear = (e, n), clear
    if best is None or best_clear < WAGON_CLEAR_M:
        return [], [{"enclosure_id": yard.get("id"), "why": (
            f"the widest clear stand in the yard is {max(best_clear, 0):.2f} m from the "
            f"nearest wall or fence, under the {WAGON_CLEAR_M:.2f} m a parked wagon "
            "needs. No wagon is drawn rather than one drawn through a wall.")}]

    # The yard is longer north-south than east-west and its two gateways are on Canal
    # (west) and Randolph (north), so a wagon standing in it stands along the yard's own
    # long axis. The bearing is the axis, derived from the box, not picked.
    bearing = 0.0 if (n_hi - n_lo) >= (e_hi - e_lo) else 90.0
    return [{
        "id": "western_hotel_wagon_yard_wagon",
        "in_enclosure": yard.get("id"),
        "belongs_to": "western_hotel",
        "confidence": "reconstructed",
        "at_local_enu_m": [_round(best[0]), _round(best[1])],
        "bearing_deg": _round(bearing, 1),
        "clearance_m": _round(best_clear),
        "note": (
            "THE ONE WAGON IN THE TOWN, and the reason there is one rather than twenty. "
            "No source this project holds puts a wagon at any place in Chicago on any "
            "day. One place is NAMED for them: data/enclosures/western_hotel_wagon_yard"
            ".json rests on chicagology_prefire278's 'In the rear was the large stable "
            "and the yard into which the trains were driven', which is a yard, in a "
            "stated place, that wagons were driven into. THE STAND IS DERIVED: a 0.25 m "
            "lattice over the yard's own bounding box, keeping the point whose least "
            f"clearance to every committed wall and every fence line is greatest — "
            f"{_round(best_clear):.2f} m here. The bearing is the yard's long axis. What "
            "is invented is that a wagon was standing in it at noon on 1 July 1835, and "
            "the wagon itself: docs/LIBERTIES.md L131."
        ),
    }], [{"enclosure_id": "*", "why": (
        "EVERY OTHER PLACE IN THE TOWN, refused in writing. docs/ROADMAP.md K5 (c) "
        "offers 'wagons/drays (documented mired on Lake St)' — this project holds no "
        "source record for that, and a dray dropped into Lake Street on the strength of "
        "a roadmap parenthesis would be traffic invented to look busy. Wagons at the "
        "stores, at the forwarding houses' doors and on South Water Street are all "
        "plausible and none of them is attested; the yard whose own name is the "
        "attestation gets the wagon, and the rest wait for a source.")}]


# --------------------------------------------------------------------------- #
# the Green Tree's yard                                                        #
# --------------------------------------------------------------------------- #

def build_green_tree_yard(cars: dict) -> tuple[list, list, list, list]:
    """The wagons, the bench and the wagon shed the Trowbridge view puts at this inn.

    The plate gives the FURNITURE — wagons in the yard, a bench against the front
    wall, an open-sided wagon shed with a covered wagon under it — and a tier-5
    retrospective view may not give a position. So every stand here is derived from
    `data/structures/green_tree_tavern.json`'s own committed footprint and placement,
    and any stand that comes out inside another building's committed wall is refused
    in writing rather than nudged.
    """
    sc = cars.get(GREEN_TREE_ID)
    if not sc:
        return [], [], [], [{"structure_id": GREEN_TREE_ID, "why": (
            "the inn is not standing in data/sidecars/1835 — nothing is put in its yard.")}]
    place = sc.get("placement") or {}
    poly = (sc.get("footprint") or {}).get("polygon") or []
    if place.get("local_e") is None or len(poly) < 3:
        return [], [], [], [{"structure_id": GREEN_TREE_ID, "why": (
            "the inn has no placed footprint — nothing in its yard can be derived.")}]

    u0 = min(p[0] for p in poly)
    u1 = max(p[0] for p in poly)
    v0 = min(p[1] for p in poly)
    v1 = max(p[1] for p in poly)
    front_w = u1 - u0                     # the front wall's own width, 25 ft here
    bearing = float(place.get("rotation_deg") or 0.0)      # the facade bearing

    walls = [(sid, w) for sid, w in
             ((sid, _footprint_world(other)) for sid, other in cars.items()
              if sid != GREEN_TREE_ID) if len(w) >= 3]

    refused: list = []

    # ---- the rear ell, which moved the wall the wagons draw up to ---------- #
    # Since T-0083 the record BUILDS John Gray's low rear addition — a gabled
    # tail off the rear gable end, form.rear_ell, sized by the archetype's own
    # parameters. It stands on the ground the wagons stood on, so the wagons
    # draw up square to ITS far wall instead: same rule, measured from the built
    # rear face. The depth is read from the same parameter resolution the
    # generator uses, so the two cannot drift apart.
    ell_d = 0.0
    rec = _load(STRUCTURES / f"{GREEN_TREE_ID}.json")
    ph = next((p for p in rec.get("phases", []) if p.get("id") == sc.get("phase")),
              (rec.get("phases") or [None])[0])
    if ph is not None and rec.get("archetype") == "frame_tavern":
        tp = _tavern_params(ph)
        if tp.rear_ell:
            ell_d = tp.rear_ell_depth_m

    # ---- the wagons -------------------------------------------------------- #
    # THE YARD'S DEPTH IS THE HOUSE'S OWN FRONT WIDTH, measured from the built
    # rear face (the ell's far wall where the record builds one). Nothing
    # measures this yard, and a yard has to be some depth before a wagon can be
    # put in it; the only length this record holds for the building is its
    # footprint, so the ground behind the built rear face is taken to run back
    # as far as the front is wide. It is an invention and is claimed as one —
    # but it is bounded by the building rather than picked, and it never
    # reaches the next street.
    rear_v = v0 - ell_d
    yard_depth = front_w
    reach = GT_WALL_CLEAR_M + WAGON_BODY_L_M + WAGON_TONGUE_M
    wagons: list = []
    if reach > yard_depth:
        refused.append({"structure_id": GREEN_TREE_ID, "why": (
            f"a wagon with its tongue down reaches {reach:.2f} m back from the wall and "
            f"the yard is taken as {yard_depth:.2f} m deep — no wagon is drawn rather "
            "than one standing in the next lot.")})
    else:
        # Drawn up square to the built rear face, tongues out into the yard: the
        # wagons stand across the yard, not along it, because that face is the
        # only line in the record to be square to.
        v_centre = rear_v - (GT_WALL_CLEAR_M + WAGON_BODY_L_M / 2)
        lo = u0 + WAGON_CLEAR_M
        hi = u1 - WAGON_CLEAR_M
        pitch = 2 * WAGON_CLEAR_M
        n = 0 if hi < lo else min(GT_WAGON_MAX, int((hi - lo) / pitch) + 1)
        if n == 0:
            refused.append({"structure_id": GREEN_TREE_ID, "why": (
                f"the rear wall is {front_w:.2f} m wide and a parked wagon needs "
                f"{2 * WAGON_CLEAR_M:.2f} m of it — no stand fits.")})
        # From the FAR end of the wall inward, so the order does not depend on which
        # way the footprint happens to be wound.
        for i in range(n):
            u = hi - i * pitch
            e, nn = _to_enu(u, v_centre, place)
            clear = min([_dist_to_polygon((e, nn), w) for _, w in walls] or [1e9])
            if clear < WAGON_CLEAR_M:
                refused.append({"structure_id": GREEN_TREE_ID, "why": (
                    f"the stand at local E {_round(e)} N {_round(nn)} is {clear:.2f} m "
                    f"from the nearest committed wall, under the {WAGON_CLEAR_M:.2f} m a "
                    "parked wagon needs — that wagon is not drawn.")})
                continue
            wagons.append({
                "id": f"green_tree_tavern_yard_wagon_{i + 1}",
                "belongs_to": GREEN_TREE_ID,
                "confidence": "reconstructed",
                "at_local_enu_m": [_round(e), _round(nn)],
                "bearing_deg": _round((bearing + 180.0) % 360.0, 1),
                "clearance_m": _round(min(clear, 999.0)),
                "note": (
                    "A FARM WAGON IN THE GREEN TREE'S YARD, and the picture is the whole "
                    "reason it is here. The Trowbridge drawing of this inn "
                    "(data/sources/assets/owner_brief_2026_08_18/README.md, image 7) "
                    "shows farm wagons standing in its yard — a tier-5 retrospective "
                    "view, which may drive furniture and setting and may never drive a "
                    "coordinate. So WHERE is derived: the wagons stand drawn up square "
                    "to the building's built rear face — since T-0083 that is the rear "
                    "ell's far wall — tongues out, "
                    f"{GT_WALL_CLEAR_M:.2f} m clear of it, spaced at the "
                    f"{2 * WAGON_CLEAR_M:.2f} m of ground a parked wagon needs, laid in "
                    "from the far end of that wall. The yard is taken to run back as far "
                    "as the front is wide, which is the only length this record has. "
                    "What is invented is the depth of that yard, that a wagon stood in it "
                    "at noon on 1 July 1835, and the wagon itself: docs/LIBERTIES.md L131 "
                    "and L133."
                ),
            })

    # ---- the bench --------------------------------------------------------- #
    # AGAINST THE FRONT WALL, at the end of the frontage the goods do not occupy.
    # The barrels pile from the -u end, so the +u end at ground level is the clear
    # one — the same division of one wall three layers already make. Until T-0082
    # this inn also carried a wall board hung 1.7 m toward +u at 2.55 m up, which
    # was the third of the three; that board now stands on a post at the street
    # corner and the frontage layer owns it, and the bench is unmoved because it
    # was never the board it had to miss — it is 2 m under where the board hung.
    benches: list = []
    u_c = u1 - END_CLEAR_M - BENCH_L_M / 2
    if u_c - BENCH_L_M / 2 < u0:
        refused.append({"structure_id": GREEN_TREE_ID, "why": (
            f"the front wall is {front_w:.2f} m and a {BENCH_L_M:.2f} m bench with "
            f"{END_CLEAR_M:.2f} m of end clearance does not stand on it — no bench.")})
    else:
        e, nn = _to_enu(u_c, v1 + BENCH_SEAT_D_M / 2, place)
        benches.append({
            "id": "green_tree_tavern_front_bench",
            "belongs_to": GREEN_TREE_ID,
            "kind": "bench",
            "confidence": "reconstructed",
            "at_local_enu_m": [_round(e), _round(nn)],
            "bearing_deg": _round(bearing, 1),
            "note": (
                "THE BENCH AGAINST THE FRONT WALL, and the people on it are not drawn. "
                "The Trowbridge drawing of this inn "
                "(data/sources/assets/owner_brief_2026_08_18/README.md, image 7) shows a "
                "bench of sitters against the front wall of the Green Tree. THE SITTERS "
                "ARE REFERENCE ONLY — AGENTS.md's standing constraint on depicting people "
                "is not relaxed by a plate, and v1 ships no human figures at all — so what "
                "is taken from the picture is the BENCH, which is the buildable fact in it. "
                "Its stand is derived: against the front wall at the +u end, "
                f"{END_CLEAR_M:.2f} m in from the end of the frontage, which is the end "
                "the barrels do not pile at. Its size is invented: docs/LIBERTIES.md L133."
            ),
        })

    # ---- the wagon shed, and the covered wagon standing in it -------------- #
    sheds, shed_wagons, shed_refused = _green_tree_wagon_shed(sc, place, poly, walls)
    wagons.extend(shed_wagons)
    refused.extend(shed_refused)

    return wagons, benches, sheds, refused


def _green_tree_wagon_shed(sc: dict, place: dict, poly: list,
                           walls: list) -> tuple[list, list, list]:
    """The open-sided wagon shed at the inn's yard end, and the tilt under it.

    WHAT THE PLATE GIVES: an open-sided wagon shed attached at the left of the
    house with a covered wagon standing under it. WHAT IT MAY NOT GIVE: which
    wall, and how big. Both are derived here.

    WHICH WALL, and this is the one judgement in the function. The plate's word is
    "left", which is a word about a viewpoint and not about a building — so it is
    read as *the end of the elevation away from the streets*, and three committed
    facts say the same wall. The placement record puts the front on Canal (west)
    and the long side on Lake (south), so the yard is the north and east ground.
    T-0080's two farm wagons already stand off the east (rear) wall, one metre
    clear of it. That leaves the NORTH side wall, which is the only wall of this
    inn that is neither a street frontage nor already occupied — and a wagon shed
    is a yard building, entered off the yard rather than off a corporation street.
    WHAT IS NOT HONOURED, said out loud rather than smoothed over: the committed
    massing runs this building's ridge along its depth (`frame_tavern` lays the
    ridge on the longer axis, 12.19 m here against 7.62 m), which puts its GABLES
    on the front and the rear and makes the north wall an eaves wall. So the shed
    stands at the left END and not at a gable, and the gable half of the plate is
    a correction to the building's fabric, which is bake-gated and is T-0083's.

    HOW BIG is arithmetic on numbers this record already carries: the bay is as
    long as the wagon's body with half a metre of air at each end, as deep as the
    ground `WAGON_CLEAR_M` gives a parked wagon, and its open eave stands a
    hand's breadth over the tilt it has to cover.
    """
    refused: list = []
    u0 = min(p[0] for p in poly)
    u1 = max(p[0] for p in poly)
    v0 = min(p[1] for p in poly)
    v1 = max(p[1] for p in poly)
    side_run = v1 - v0                      # the north wall's own run, 40 ft here
    bearing = float(place.get("rotation_deg") or 0.0)
    # The outward normal of the +u wall as a compass bearing. The facade's normal
    # is +v and its bearing is the placement's rotation, and +u is a quarter turn
    # from +v in this frame — the same derivation `_to_enu` does, read backwards.
    out_bearing = (bearing + 90.0) % 360.0

    depth = 2 * WAGON_CLEAR_M                       # out from the wall
    length = WAGON_BODY_L_M + 2 * GT_SHED_END_M     # along the wall
    tilt_top = WAGON_BED_Y_M + WAGON_BODY_H_M + WAGON_TILT_RISE_M
    eave = tilt_top + GT_SHED_HEADROOM_M            # the open side's plate
    head = eave + depth * math.tan(math.radians(GT_SHED_PITCH_DEG))

    if length > side_run:
        return [], [], [{"structure_id": GREEN_TREE_ID, "why": (
            f"a bay long enough for a wagon is {length:.2f} m and the side wall runs "
            f"{side_run:.2f} m — no shed is drawn rather than one longer than the "
            "wall it leans on.")}]
    # A lean-to is spiked to a wall UNDER that wall's own eaves. The record states
    # this building's wall height, so the constraint is checkable rather than
    # eyeballed, and a shed that would stand through the clapboard is refused.
    wall_h = ((sc.get("attributes") or {}).get("wall_height_m") or {}).get("value")
    if isinstance(wall_h, (int, float)) and head + GT_SHED_PLATE_M > wall_h:
        return [], [], [{"structure_id": GREEN_TREE_ID, "why": (
            f"the lean-to's plate would meet the wall {head + GT_SHED_PLATE_M:.2f} m "
            f"up and the record gives this building {wall_h:.2f} m of wall — no shed "
            "is drawn rather than one through the first-floor windows.")}]

    # The bay stands at the YARD end of that wall: it starts at the rear wall's own
    # plane and runs forward, so it is behind the Canal frontage the sign, the bench
    # and the barrels occupy, and it never reaches the Lake Street corner.
    v_c = v0 + length / 2
    u_c = u1 + depth / 2
    e, nn = _to_enu(u_c, v_c, place)

    # Clearance is measured from the covered ground's own corners, not from its
    # centre: a 3.2 x 4.05 m roof is the largest thing this layer has ever put on
    # the ground and its centre clearing a wall says nothing about its corners.
    corners = [_to_enu(u, v, place) for u, v in (
        (u1, v0), (u1, v0 + length), (u1 + depth, v0 + length), (u1 + depth, v0))]
    clear = min([_dist_to_polygon(c, w) for c in corners for _, w in walls] or [1e9])
    if clear < GT_WALL_CLEAR_M:
        return [], [], [{"structure_id": GREEN_TREE_ID, "why": (
            f"the shed's covered ground comes within {clear:.2f} m of another "
            f"committed wall, under the {GT_WALL_CLEAR_M:.2f} m a building is given — "
            "no shed is drawn rather than one built into a neighbour.")}]

    shed = {
        "id": "green_tree_tavern_wagon_shed",
        "belongs_to": GREEN_TREE_ID,
        "kind": "wagon_shed",
        "confidence": "reconstructed",
        "at_local_enu_m": [_round(e), _round(nn)],
        "bearing_deg": _round(out_bearing, 1),
        "length_m": _round(length),
        "depth_m": _round(depth),
        "eave_m": _round(eave),
        "head_m": _round(head),
        "clearance_m": _round(min(clear, 999.0)),
        "note": (
            "AN OPEN-SIDED WAGON SHED AT THE INN'S YARD END, and the picture is the "
            "whole reason it is here. The Trowbridge drawing of this inn "
            "(data/sources/assets/owner_brief_2026_08_18/README.md, image 7) shows an "
            "open-sided wagon shed attached at the left of the house with a covered "
            "wagon standing under it — a tier-5 retrospective view, which may drive "
            "furniture and setting and may never drive a coordinate. WHICH WALL IS "
            "DERIVED: the placement record puts the front on Canal and the long side "
            "on Lake, T-0080's wagons already stand off the rear wall, and that leaves "
            "the north side wall — the only one of this inn's four that is neither a "
            "street frontage nor already occupied, and a wagon shed is entered off a "
            "yard rather than off a corporation street. WHAT IS NOT HONOURED: the "
            "committed massing lays this building's ridge along its longer axis, which "
            "puts its gables on the front and the rear, so this stands at the left END "
            "and not at a gable; the gable is a correction to the building's fabric and "
            "is bake-gated (T-0083). HOW BIG IS ARITHMETIC on numbers already here: the "
            f"bay is {length:.2f} m along the wall (the wagon's body and "
            f"{GT_SHED_END_M:.2f} m of air at each end) by {depth:.2f} m out from it "
            f"(the ground a parked wagon is given), its open eave stands {eave:.2f} m "
            f"up ({GT_SHED_HEADROOM_M:.2f} m over the tilt it covers) and its plate "
            f"meets the wall {head:.2f} m up at {GT_SHED_PITCH_DEG:.0f} degrees. What "
            "is invented is that this inn had a wagon shed on 1 July 1835 and every "
            "dimension of it: docs/LIBERTIES.md L134. NOT THE SAME THING as the low "
            "one-storey additions John Gray describes at each end of the house — those "
            "are attributes of the BUILDING, dated three to six years after the scene "
            "and deliberately excluded from its footprint; this is a yard structure on "
            "the yard's own ground, and it does not date them."
        ),
    }

    # The covered wagon standing under it, on the same centre as the bay: a shed
    # a wagon cannot stand in is not what the plate shows. It is the yard's own
    # farm wagon with a tilt over it, laid along the wall because that is the way
    # a 4.05 m bay takes a 3.05 m body, tongue down and out of the open end.
    wagon = {
        "id": "green_tree_tavern_shed_wagon",
        "belongs_to": GREEN_TREE_ID,
        "under_shed": shed["id"],
        "tilt": True,
        "confidence": "reconstructed",
        "at_local_enu_m": [_round(e), _round(nn)],
        "bearing_deg": _round((out_bearing + 90.0) % 360.0, 1),
        "clearance_m": _round(min(clear, 999.0)),
        "note": (
            "THE COVERED WAGON UNDER THE SHED, from the same plate and standing on the "
            "same derived centre as the bay over it. It is the farm wagon this record "
            "already draws — the body, the wheels and the tongue are L131's invented "
            "numbers and have not moved — with a TILT added: canvas on bows, "
            f"{WAGON_TILT_RISE_M:.2f} m of rise over the body's top rail and "
            f"{WAGON_TILT_OVERHANG_M:.2f} m pulled past the end bows, open at both "
            "ends. The bows themselves are not drawn, for the reason the barrels' "
            "hoops are not: under the canvas there is nothing to see. It lies ALONG "
            "the wall because that is how a 4.05 m bay takes a 3.05 m body, with the "
            "tongue down and out of the open end into the yard. What is invented is "
            "the wagon, the tilt and the fact that either stood here on 1 July 1835: "
            "docs/LIBERTIES.md L131 and L134."
        ),
    }
    return [shed], [wagon], refused


# --------------------------------------------------------------------------- #
# the record                                                                   #
# --------------------------------------------------------------------------- #

def record(frontages: list, refused: list, wagons: list, wagons_refused: list,
           benches: list, sheds: list) -> dict:
    items = sum(len(f["items"]) for f in frontages)
    return {
        "_doc": (
            "Goods standing at the town's trading frontages — barrels and cases on the "
            "footway at the taverns and the stores, the wagons standing in the yard a "
            "source calls a wagon yard and in the Green Tree's, the bench against that "
            "inn's front wall and the open-sided wagon shed at its yard end with a "
            "covered wagon under it. NOT structure records and NOT geometry that comes out "
            "of Blender: a barrel on a footway is a small object standing on ground this "
            "project has already drawn, so it is derived from the committed footprints "
            "and placements and drawn at load by renderers/web/js/yard.js — the same "
            "argument that lets the enclosure layer draw a fence from a perimeter and "
            "the signage layer hang a board off a wall. Generated by "
            "tools/generate_yard_goods.py and re-derived byte for byte by "
            "tools/check.sh, because 'which frontage gets goods' is a rule and a rule "
            "has to be auditable."
        ),
        "id": "town_trade_goods",
        "name": "Goods at the town's trading frontages",
        "kind": "yard_goods",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same frame "
            "data/enclosures/ and data/signage/ and the sidecars' placement.local_e / "
            "local_n use."
        ),
        "counts": {
            "frontages": len(frontages),
            "objects": items,
            "wagons": len(wagons),
            "benches": len(benches),
            "sheds": len(sheds),
        },
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": ["chicago_democrat_1833_11_26", "chicagology_prefire278"],
            "note": (
                "UNLIKE THE SIGNBOARDS ONE LAYER OVER, THIS ONE DOES NOT START FROM "
                "SILENCE — THE TOWN LEGISLATED ABOUT IT. The village ordinances of "
                "7 November 1833 are carried complete in the first issue of the Chicago "
                "Democrat (data/sources/chicago_democrat_1833_11_26.json, tier 1, "
                "verified from the scan), and ORDINANCE 9 IS ABOUT TIMBER, STONE, BRICK, "
                "BOXES AND BARRELS STACKED IN THE STREETS. A corporation does not "
                "legislate against a thing nobody does: that is a contemporary statement, "
                "by the people who had to walk round them, that Chicago's streets had "
                "boxes and barrels standing in them. WHAT IT DOES NOT GIVE IS A "
                "LOCATION — it says the town, not the corner, and it is twenty months "
                "before the scene date. So the FACT of goods on a public frontage is "
                "well founded and WHICH frontage is a rule, and the rule is what this "
                "record is generated from. The wagon rests on a second source and one "
                "sentence of it: chicagology_prefire278's 'the yard into which the trains "
                "were driven'. NOTHING HERE IS PROMOTED ABOVE reconstructed on the "
                "strength of either: no source states that any of these particular "
                "buildings had anything outside its door on 1 July 1835."
            ),
        },
        "ordinance": {
            "source_id": "chicago_democrat_1833_11_26",
            "value": "Ordinance 9: timber, stone, brick, boxes and barrels stacked in the streets",
            "confidence": "attested",
            "note": (
                "Quoted here as the source record's own summary of the item, not as a "
                "transcription of the ordinance's text — the page image is the source and "
                "this project's holding of it is a summary line in "
                "data/sources/chicago_democrat_1833_11_26.json § what_it_supplies. WHAT "
                "THIS LAYER DELIBERATELY DOES NOT DO WITH IT: the ordinance is about "
                "goods IN THE STREETS, which is the stronger reading, and nothing here is "
                "drawn in a roadway. Every object stands within 0.55 m of the wall it "
                "belongs to, on the footway strip — the restrained reading, chosen "
                "because a barrel standing in the travelled way would be a claim about "
                "the width of the road as well as about the goods, and because the "
                "roadway is where a visitor walks. TIMBER, STONE AND BRICK ARE NOT DRAWN "
                "EITHER: they are building material on a lot under construction rather "
                "than a merchant's stock on his own frontage, they belong to whichever "
                "building was going up that week, and this record has no way to say "
                "which. That half of Ordinance 9 is filed as its own ticket."
            ),
        },
        "form": {
            "barrel_height_m": {
                "value": BARREL_H_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. 0.84 m is 33 in, the height of a provision barrel of the "
                    "period standing on its head. No source in this repository gives the "
                    "size of any cask in Chicago. What bounds it is the trade the "
                    "research already holds: docs/research/08-fauna.md records Hubbard "
                    "packing 5,000 hogs in 1834 that had to be 'stowed away in bulk' for "
                    "want of barrels until they came from Cleveland at a dollar apiece, "
                    "so the barrel here is the provision barrel that trade turned on."
                ),
            },
            "barrel_belly_diameter_m": {
                "value": BARREL_BELLY_D_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. 0.53 m is 21 in at the bilge. Nothing attests it. It is "
                    "the proportion a coopered cask has to have — the staves bow or they "
                    "cannot be drawn up tight — and it is what makes the object read as "
                    "a barrel rather than as a drum."
                ),
            },
            "barrel_head_diameter_m": {
                "value": BARREL_HEAD_D_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. 0.45 m is 17.5 in at the head, about six sevenths of the "
                    "bilge. Nothing attests it. NO HOOPS ARE DRAWN AS SEPARATE "
                    "GEOMETRY — a hoop is 20 mm of iron and at any distance a visitor "
                    "stands it is a line, not a solid, so drawing one would spend "
                    "triangles on something the eye cannot resolve."
                ),
            },
            "crate_size_m": {
                "value": [CRATE_L_M, CRATE_W_M, CRATE_H_M],
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. A case 1.05 x 0.72 x 0.62 m — a two-man lift. Nothing "
                    "attests a case, its size or its boards. Ordinance 9 names 'boxes' "
                    "and this is what this record draws one as. The second case stacked "
                    "on it is 0.72 of its size, which is nothing but the difference that "
                    "makes a stack read as two objects."
                ),
            },
            "wagon_body_m": {
                "value": [WAGON_BODY_L_M, WAGON_BODY_W_M, WAGON_BODY_H_M],
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. A body 10 ft by 3 ft 6 in and 22 in deep, recorded "
                    "converted, on wheels 4 ft 6 in behind and 3 ft 6 in in front — a "
                    "farm wagon, which is what 'the trains driven into the yard' were. "
                    "Not one of those numbers is attested for Chicago or for this yard. "
                    "The spoke count, the rim and the hub are the renderer's and are "
                    "claimed in the same liberty."
                ),
            },
            "bench_size_m": {
                "value": [BENCH_L_M, BENCH_SEAT_D_M, BENCH_SEAT_H_M],
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. A backless plank bench 6 ft long, 14 in deep and 18 in to "
                    "the seat, on two plank ends, recorded converted. The Trowbridge view "
                    "of the Green Tree shows a bench against the front wall and shows how "
                    "long it is only against the people sitting on it, who are reference "
                    "and are not drawn — so the length is read off the wall it stands "
                    "against rather than off them, and the section is a joiner's plank of "
                    "the period and nothing more. Nothing attests any of it."
                ),
            },
            "bench_plank_m": {
                "value": BENCH_PLANK_T_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED — 45 mm of sawn plank for the seat and its two ends. HOW a "
                    "bench is drawn rather than a claim about this one, kept on the record "
                    "with its other sizes so the renderer reaches for no number of its own."
                ),
            },
            "wagon_tilt_m": {
                "value": [WAGON_TILT_RISE_M, WAGON_TILT_OVERHANG_M],
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. The covered wagon's canvas rises 1.10 m over the body's "
                    "top rail — about 3 ft 7 in, which is the height a person has to "
                    "have to sit under a tilt — and is pulled 0.12 m past the end bows. "
                    "Nothing attests a covered wagon at this inn or anywhere in this "
                    "town; the Trowbridge drawing of the Green Tree shows one standing "
                    "under its wagon shed and the ordinary width of the same farm wagon "
                    "body is what the arch springs from. THE BOWS ARE NOT DRAWN AS "
                    "SEPARATE GEOMETRY, the barrels' hoops' argument exactly: under the "
                    "canvas there is nothing to see. The tilt is open at both ends, "
                    "which is what the plate shows and is also the honest half — a "
                    "gathered canvas end is a shape nothing here can state."
                ),
            },
            "shed_bay_m": {
                "value": [WAGON_BODY_L_M + 2 * GT_SHED_END_M, 2 * WAGON_CLEAR_M],
                "confidence": "reconstructed",
                "note": (
                    "INVENTED, but it is arithmetic on numbers this record already "
                    "carries rather than a pair of figures picked to look right: the "
                    "bay is the wagon's own 3.05 m body with 0.50 m of air at each end, "
                    "by the 3.20 m of ground WAGON_CLEAR_M gives a parked wagon. "
                    "Nothing measures this shed, and no source states that the Green "
                    "Tree had one — the Trowbridge drawing shows it. Its stand is "
                    "derived from the committed footprint and is argued on the shed's "
                    "own record."
                ),
            },
            "shed_timber_m": {
                "value": [GT_SHED_POST_M, GT_SHED_PLATE_M],
                "confidence": "reconstructed",
                "note": (
                    "INVENTED — 0.14 m posts under the open side and 0.16 m plates and "
                    "rafters over them, which is a 5.5 in stick and a 6 in one. HOW the "
                    "shed is drawn rather than a claim about this one, kept on the "
                    "record with its other sizes so the renderer reaches for no number "
                    "of its own, the same division bench_plank_m makes."
                ),
            },
            "shed_pitch_deg": {
                "value": GT_SHED_PITCH_DEG,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. A lean-to falling 12 degrees away from the wall it is "
                    "spiked to — 0.68 m over the bay's 3.20 m. Nothing states the "
                    "shed's roof, its pitch or its covering. What bounds it is the "
                    "shape: the roof has to shed water away from the house and has to "
                    "clear the tilt at its low edge, and 12 degrees is the shallowest "
                    "fall that does both over this depth. The roof is drawn as boards "
                    "in the layer's own timber, not as shingles: nothing says which, "
                    "and boards are what an open shed in this town was likeliest to "
                    "carry."
                ),
            },
            "marks": {
                "value": None,
                "confidence": "reconstructed",
                "geometry": "absent",
                "note": (
                    "NOT DRAWN, AND IT IS THE SAME DISCIPLINE THE SIGNBOARDS KEEP. No "
                    "barrel carries a brand, a merchant's name, a stencil or a mark of "
                    "any kind, and no case is labelled. Nothing this project holds says "
                    "what was in any barrel in Chicago on this date, still less whose it "
                    "was, and painted names on two hundred casks would be the most "
                    "conspicuous fiction in the scene — the point docs/LIBERTIES.md L25 "
                    "settled for the one documented sign and L130 generalised."
                ),
            },
        },
        "rule": {
            "note": (
                "A named record (not inf_/recon_, not 'Reconstructed'), a GOODS-KEEPING "
                "trade whose stock arrived in boxes and barrels, that trade attested or "
                "inferred rather than reconstructed, standing on the scene date, on the "
                "TOWN's ground rather than inside the fort's palisade, and a strip in "
                "front of the facade clear of every other committed footprint. How many "
                "objects is arithmetic on the frontage — one barrel per 2.2 m of usable "
                "wall to a cap of four, a case past them at 4 m, a second case stacked "
                "at 7 m, and a public house's empty laid on its side at 5 m — never a "
                "lottery. Read the clauses and their reasons in "
                "tools/generate_yard_goods.py."
            ),
            "goods_trades": sorted(GOODS_TRADES),
            "excluded_trades_note": (
                "Smithies, cooperages, tanneries, brickyards, packing and slaughter "
                "houses, manufactories, stables, warehouses without a counter, the "
                "churches, the schools, the court-house, the jail, the agency house and "
                "every dwelling are outside the trade list. Several of them plainly kept "
                "stuff outside — a cooperage most of all — but what they kept was tools "
                "and material rather than a merchant's stock on a public frontage, and "
                "the rule would be guessing. The fort's provision store and sutler's "
                "store are refused separately and in writing: federal ground, no "
                "corporation street in front of the door."
            ),
            "placement_note": (
                "The goods stand at the end of the frontage the SIGNBOARD does not "
                "occupy. tools/generate_business_signboards.py hangs its board 1.7 m "
                "toward +u of the facade's centre, so this piles from the -u end and the "
                "door between them stays clear — two layers derived from the same wall "
                "that would otherwise be derived into each other. The Green Tree is the "
                "one frontage here with no wall board to keep clear of (T-0082 moved its "
                "board to a post at the street corner), and the goods pile from the same "
                "end anyway: the barrels were derived before the board moved and moving "
                "them now would be a change nothing asked for."
            ),
        },
        "frontages": frontages,
        "wagons": wagons,
        "benches": benches,
        "sheds": sheds,
        "refused": refused,
        "wagons_refused": wagons_refused,
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: the missing fourth page of "
            "the Democrat's first issue, which would carry more of the ordinances and may "
            "carry Ordinance 9's own text and its penalty; any later Chicago corporation "
            "order about obstructions, which would say what was being obstructed with; an "
            "insurance or tax description of a South Water Street lot; a traveller's "
            "account of walking the street; or the pre-fire photographs of surviving "
            "1830s frontages actually opened at their holding institutions. WHAT THIS "
            "RECORD IS STILL SHORT OF, stated rather than left to be noticed: Ordinance "
            "9's timber, stone and brick are not drawn at all; nothing stands in a "
            "roadway though the ordinance is about roadways; and the wagons in this town "
            "still stand at two addresses out of hundreds — the yard a source names for "
            "wagons, and the one inn a picture shows them in. T-0064 is the ticket for "
            "the rest of a frontier town's traffic. THE SHED IS THE FIRST ROOF THIS "
            "LAYER HAS EVER DRAWN, and it is worth saying what that does not mean: it "
            "is not a structure record, it has no archetype and it is not baked, "
            "because it is derived from a committed footprint the way a fence and a "
            "signboard are. If a second yard building is ever wanted the question to "
            "ask first is whether it belongs here or in data/structures/."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()
    ids, cars = _standing()
    frontages, refused = build_frontages(ids, cars)
    wagons, wagons_refused = build_wagons(cars)
    gt_wagons, benches, sheds, gt_refused = build_green_tree_yard(cars)
    wagons = wagons + gt_wagons
    wagons_refused = wagons_refused + gt_refused
    text = json.dumps(record(frontages, refused, wagons, wagons_refused, benches, sheds),
                      indent=2, ensure_ascii=False) + "\n"
    objects = sum(len(f["items"]) for f in frontages)
    if args.check:
        if not OUT.exists():
            print(f"YARD GOODS DRIFT\n  - {OUT.relative_to(ROOT)} is missing")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"YARD GOODS DRIFT\n  - {OUT.relative_to(ROOT)} has drifted from the "
                  f"rule in tools/generate_yard_goods.py")
            return 1
        print(f"verified {objects} object(s) on {len(frontages)} trading frontage(s), "
              f"{len(wagons)} wagon(s), {len(benches)} bench(es) and {len(sheds)} "
              f"shed(s) ({len(refused)} frontage(s) refused with a reason)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {objects} object(s) on {len(frontages)} "
          f"frontage(s), {len(wagons)} wagon(s), {len(benches)} bench(es), "
          f"{len(sheds)} shed(s) ({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
