#!/usr/bin/env python3
"""Which lot of the platted grid every committed footprint stands on.

ROADMAP T-A7. **One implementation, imported by both halves.** T-A6 made the
schedule's room a function of FREE LOTS rather than of roofs, and required the two
halves to derive occupancy "the same way" — which they did, by each carrying its own
copy of the same rule. `tools/reconcile_665.py` decided how many principal roofs a
block could take; `tools/generate_block_infill.py` decided whether the lot the recipe
named was free. Two copies of one rule is how they drift, and a schedule that deals a
roof its own generator refuses is the failure T-A6 exists to prevent. Both now call
this module and there is nothing left to disagree about.

**A building stands on the lot most of it is on, measured, and occupies that lot when
it reaches the part of it another roof would need.** Two tests, and each answers a
failure the centroid rule could not.

*Test one — one building, one lot, by area.* The centroid is a proxy for the building,
and it fails in exactly the case the plat grid was built to handle: a building placed
from typed coordinates before the module existed, standing a metre or two proud of its
own street frontage. Its centroid is then in the ROADWAY, so it stands on no lot of any
block, while a quarter of the building sits on the lot a principal roof is about to be
dealt. Measured on the committed dataset at T-A7, fourteen records were in that
position, the Temple Building among them: 27 % of it is on `blk_south_water_franklin`
lot 0 and it read as standing on nothing at all. Nothing MOVES lot under this test —
every record that has a centroid in a lot has its greatest overlap in the same lot —
so it only ever finds ground the old rule could not see.

*Test two — it has to reach the buildable part.* A footprint may lap over a lot line
without taking anything from the lot: the generator already requires every new roof to
clear its own lot lines by `LOT_MARGIN_M` = 1.5 m, so a neighbour lapping only into
that margin strip has taken a strip no roof could have used anyway. Kinzie's store is
the case — 9.7 m² of it lies on `blk_south_water_franklin` lot 2 and none of it inside
the lot's buildable inset, so that lot is free and the schedule may deal it a roof. The
test needs no constant of its own; it is the placement gate's own margin, read from
the generator so the two cannot drift apart.

Together they are also what keeps this from being a rule that condemns the town it
already built. `recon_1835_west_018` laps 11.9 m² onto `blk_randolph_clinton` lot 2,
where T-A4 stands a principal roof: test one seats that building on lot 4, where 82 %
of it is, so lot 2 stays the roof's own. Whether two roofs three metres apart on
neighbouring lots is right is the separation gate's question and it passed at the time.

The overlap is exact rather than sampled: lot polygons are convex, so clipping the
footprint against the lot (Sutherland–Hodgman) gives the intersection itself. The
subject polygon need not be convex; the clip polygon must be, which is checked.

`SLIVER_M2` is a numerical tolerance and not a policy. Two polygons that share an edge
intersect in a few square millimetres of rounding, and the tolerance is far below
anything a placement gate allows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRUCTURES = ROOT / "data" / "structures"

# A tenth of a metre square. See the module docstring: a tolerance, not a threshold.
SLIVER_M2 = 0.01

# The margin every new roof must keep from its own lot lines. Authored HERE and imported
# by `tools/generate_block_infill.py`, which enforces it on the roofs it places, because
# the two are the same number: the buildable part of a lot is the lot inset by the
# margin, and a neighbour lapping only into the margin strip has taken nothing a roof
# could have stood on. Side lot lines are conjectural (K7: four lots to a face is a
# reading of ONE block), so a wall ON one would be asserting a line the grid does not
# have — which is why the margin exists at all.
LOT_MARGIN_M = 1.5


def world_polygon(phase: dict, datum: dict) -> list[tuple[float, float]]:
    """A phase's footprint in the scene's local ENU frame, metres from the datum."""
    pos, poly = phase["position"], phase["footprint"]["polygon"]
    theta = math.radians(float(pos.get("rotation_deg") or 0))
    cos, sin = math.cos(theta), math.sin(theta)
    e0 = float(pos["utm_e"]) - float(datum["origin_utm_e"])
    n0 = float(pos["utm_n"]) - float(datum["origin_utm_n"])
    return [(e0 + u * cos + v * sin, n0 - u * sin + v * cos) for u, v in poly]


def footprints(datum: dict, exclude: set[str] | frozenset[str] = frozenset()
               ) -> list[tuple[str, list[tuple[float, float]]]]:
    """(structure_id, world polygon) for every committed phase that has both.

    Every phase, not the first: a structure that was rebuilt on a different footprint
    stands on whichever lots its phases stand on, and the ledger counts the roof once
    either way.
    """
    placed: list[tuple[str, list[tuple[float, float]]]] = []
    for path in sorted(STRUCTURES.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["id"] in exclude:
            continue
        for phase in record.get("phases") or []:
            position = phase.get("position") or {}
            polygon = (phase.get("footprint") or {}).get("polygon") or []
            if position.get("utm_e") is None or len(polygon) < 3:
                continue
            placed.append((record["id"], world_polygon(phase, datum)))
    return placed


def _signed_area(poly: list[tuple[float, float]]) -> float:
    total = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        total += x1 * y2 - x2 * y1
    return total / 2


def area(poly: list[tuple[float, float]]) -> float:
    return abs(_signed_area(poly))


def _convex(poly: list[tuple[float, float]]) -> bool:
    sign = 0
    for i in range(len(poly)):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % len(poly)]
        cx, cy = poly[(i + 2) % len(poly)]
        cross = (bx - ax) * (cy - by) - (by - ay) * (cx - bx)
        if abs(cross) < 1e-9:
            continue
        here = 1 if cross > 0 else -1
        if sign == 0:
            sign = here
        elif here != sign:
            return False
    return True


def overlap_area(subject: list[tuple[float, float]],
                 convex_clip: list[tuple[float, float]]) -> float:
    """Area the subject polygon shares with a CONVEX clip polygon, in square metres."""
    if not _convex(convex_clip):
        raise SystemExit("plat_occupancy: the clip polygon is not convex, so the "
                         "intersection below would be silently wrong. Lot polygons are "
                         "convex by construction — a concave one is the finding")
    clip = convex_clip if _signed_area(convex_clip) > 0 else convex_clip[::-1]

    def inside(p, a, b) -> bool:
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

    def crossing(p1, p2, a, b):
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, a, b
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return p2
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    out = list(subject)
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        source, out = out, []
        if not source:
            return 0.0
        previous = source[-1]
        for point in source:
            if inside(point, a, b):
                if not inside(previous, a, b):
                    out.append(crossing(previous, point, a, b))
                out.append(point)
            elif inside(previous, a, b):
                out.append(crossing(previous, point, a, b))
            previous = point
    return area(out) if len(out) >= 3 else 0.0


def inset(convex_poly: list[tuple[float, float]], metres: float
          ) -> list[tuple[float, float]]:
    """The convex polygon shrunk by `metres` on every side — a lot's buildable part.

    Returns an empty list where the inset eats the polygon, which on a lot of these
    proportions cannot happen and on a hypothetical narrow one correctly means no roof
    fits.
    """
    poly = convex_poly if _signed_area(convex_poly) > 0 else convex_poly[::-1]
    out = list(poly)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        length = math.dist(a, b)
        if length == 0:
            continue
        # inward normal of a counter-clockwise edge
        nx, ny = -(b[1] - a[1]) / length, (b[0] - a[0]) / length
        a2 = (a[0] + nx * metres, a[1] + ny * metres)
        b2 = (b[0] + nx * metres, b[1] + ny * metres)
        source, out = out, []
        if not source:
            return []

        def keeps(p, a2=a2, b2=b2) -> bool:
            return (b2[0] - a2[0]) * (p[1] - a2[1]) - (b2[1] - a2[1]) * (p[0] - a2[0]) >= 0

        def meet(p1, p2, a2=a2, b2=b2):
            (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, a2, b2
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom == 0:
                return p2
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

        previous = source[-1]
        for point in source:
            if keeps(point):
                if not keeps(previous):
                    out.append(meet(previous, point))
                out.append(point)
            elif keeps(previous):
                out.append(meet(previous, point))
            previous = point
    return out if len(out) >= 3 else []


def seated_lots(grid: dict, datum: dict,
                exclude: set[str] | frozenset[str] = frozenset()
                ) -> dict[str, dict[int, list[str]]]:
    """{block_id: {lot_index: EVERY structure seated on it}} across the whole grid.

    Both tests, in order: a building's lot is the one it has the greatest area on, and
    it occupies that lot only if it reaches inside the lot's buildable inset. See the
    module docstring for why each is there and what each was measured against.

    The list, rather than one name, is T-0199. `occupied_lots` below has always kept the
    first structure by id and thrown the rest away, because until now the only question
    asked of it was "is this lot free", which one name answers. The core density
    standard (T-0079) made a second question askable: a lot of a party-line business
    frontage carries up to `ROW_UNITS_PER_LOT` roofs, so HOW MANY stand on it is the
    count that binds, and a map that names one of three cannot supply it. Both callers
    read the same map; the one that needs a name still takes the first.
    """
    frames = [(block["id"], index, [tuple(p) for p in lot["polygon"]])
              for block in grid["blocks"] for index, lot in enumerate(block["lots"])]
    buildable = {(bid, index): inset(polygon, LOT_MARGIN_M)
                 for bid, index, polygon in frames}

    taken: dict[str, dict[int, list[str]]] = {}
    for structure_id, world in footprints(datum, exclude):
        seat, best = None, SLIVER_M2
        for bid, index, polygon in frames:
            here = overlap_area(world, polygon)
            if here > best:
                seat, best = (bid, index), here
        if seat is None:
            continue
        room = buildable[seat]
        if not room or overlap_area(world, room) <= SLIVER_M2:
            continue
        # A structure whose phases were rebuilt on one lot is one roof there, not two.
        here_ids = taken.setdefault(seat[0], {}).setdefault(seat[1], [])
        if structure_id not in here_ids:
            here_ids.append(structure_id)
    return taken


def occupied_lots(grid: dict, datum: dict,
                  exclude: set[str] | frozenset[str] = frozenset()
                  ) -> dict[str, dict[int, str]]:
    """{block_id: {lot_index: the structure standing on it}} across the whole grid.

    Where two structures hold one lot the first by id is named. The map's job is to say
    the lot is taken and by something nameable, not to arbitrate between them — that
    two roofs share a lot is the separation gate's question, and this one's answer is
    the same either way. `seated_lots` above is the same measurement without the
    discard, for the caller that needs the count rather than a name.
    """
    return {block: {index: ids[0] for index, ids in sorted(lots.items())}
            for block, lots in seated_lots(grid, datum, exclude).items()}


def block_of_structure(taken: dict[str, dict[int, str]]) -> dict[str, str]:
    """{structure_id: the block whose lots it stands on}, from an occupancy map.

    The ledger attributes a roof to a block by its position POINT, which is the same
    proxy failing the same way: three documented buildings — the Exchange Coffee House,
    Harmon & Loomis's store and the Tremont House — have their position point in the
    roadway and their building on a lot, so they were counted as standing in no block
    at all while occupying one of its eight lots. A roof that stands on a block's lot
    stands in that block.
    """
    home: dict[str, str] = {}
    for block_id, lots in sorted(taken.items()):
        for _, structure_id in sorted(lots.items()):
            home.setdefault(structure_id, block_id)
    return home
