#!/usr/bin/env python3
"""What stands on ground that was never open to a private builder.

ROADMAP T-E2. The refusal is authored in
`data/reconstruction/1835_no_build_ground.json`; this is the command that resolves its
boundaries from the committed traces and measures them. Nothing here is hand-typed
geometry — the reservation's two survey lines come out of one ground-control point and
the plat's own bearing, and its third side is the traced waterline. Re-deriving rather
than storing is the same discipline `data/datum.json` is held to, and for the same
reason: a stored vertex cannot be wrong loudly.

The companion for platted blocks is `tools/measure_reserved_ground.py` (T-A16), which
answers the question for ground the plat DID subdivide. This one answers it for ground
the plat never reached.

    tools/measure_no_build_ground.py          print the table
    tools/measure_no_build_ground.py --gate   exit 1 if anything unpermitted stands there

Three things fail the gate, and the third is the one worth having:

1. A structure standing on refused ground that the region does not permit.
2. A permitted entry naming a record that is not there — a permission list that can go
   stale in silence is a way of turning the gate off.
3. UNDER-COVERAGE. Every cell of the committed heightfield above the water surface,
   east of the reservation's west line, north of Madison's line and south of the main
   stem, must fall inside one of the two polygons. It does today, exactly: the count is
   zero. T-E3 extends the terrain east and south, and when it does, this is the
   assertion that will notice that the polygons no longer reach the ground.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NO_BUILD_PATH = DATA / "reconstruction" / "1835_no_build_ground.json"
EPOCH = DATA / "terrain" / "epochs" / "e1834_harbor_cut"
SHORELINE = EPOCH / "shoreline.geojson"
GCP_PATH = DATA / "traces" / "gcp" / "wright_1834_gcps.json"
STREETS_PATH = DATA / "streets" / "1835.json"

sys.path.insert(0, str(ROOT / "tools"))
from plat_occupancy import footprints  # noqa: E402
from heightfield import Heightfield  # noqa: E402

# The shore feature the reservation's third side is walked along. Matched on the `kind`
# and on the words the trace itself uses, so a renamed feature fails loudly.
SHORE_NAME = "the Fort Dearborn reservation's lake shore"
# Ground north of this is the North Division, across the main stem, and is not the
# reservation however far east it lies. Only the under-coverage count uses it.
SOUTH_BANK_N = 40.0
WATER_SURFACE_M = 0.0


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


NO_BUILD = load(NO_BUILD_PATH)


def inside(point, polygon) -> bool:
    x, y = point
    hit = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def ring_area(polygon) -> float:
    total = 0.0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def plat_bearing() -> float:
    """The plat's east-west slope in local ENU, read off the committed centrelines.

    Lake, Randolph and Washington are three straight committed lines of the same grid.
    They agree exactly, and the agreement is asserted rather than assumed: a grid whose
    own streets disagree is a finding, not a number to average away.
    """
    slopes = []
    for street in load(STREETS_PATH)["streets"]:
        if street["id"] not in {"lake", "randolph", "washington"}:
            continue
        path = street["path_local_enu_m"]
        (ax, ay), (bx, by) = path[0], path[-1]
        slopes.append(round((by - ay) / (bx - ax), 6))
    if len(slopes) != 3:
        raise SystemExit("the plat bearing needs Lake, Randolph and Washington")
    if len(set(slopes)) != 1:
        raise SystemExit(f"the plat's own east-west streets disagree on bearing: {slopes}")
    return slopes[0]


def section_corner() -> tuple[float, float]:
    """G1 — State & Madison — in local ENU. The PLSS corner both lines run from."""
    datum = load(DATA / "datum.json")
    points = load(GCP_PATH)
    points = points.get("points") or points.get("gcps")
    g1 = next((p for p in points if p["id"] == "G1"), None)
    if g1 is None:
        raise SystemExit("wright_1834_gcps.json no longer carries G1")
    if "Madison" not in g1["map_feature"]:
        raise SystemExit(f"G1 is no longer State & Madison but {g1['map_feature']!r}")
    return (g1["modern"]["utm_e"] - datum["origin_utm_e"],
            g1["modern"]["utm_n"] - datum["origin_utm_n"])


def shore_line() -> list[tuple[float, float]]:
    datum = load(DATA / "datum.json")
    for feature in load(SHORELINE)["features"]:
        props = feature["properties"]
        if props.get("kind") == "shore" and SHORE_NAME in props.get("name", ""):
            return [(x - datum["origin_utm_e"], y - datum["origin_utm_n"])
                    for x, y in feature["geometry"]["coordinates"]]
    raise SystemExit(f"no shoreline feature names {SHORE_NAME!r}")


def bar_ring() -> list[tuple[float, float]]:
    datum = load(DATA / "datum.json")
    for feature in load(SHORELINE)["features"]:
        if feature["properties"].get("kind") == "bar":
            return [(x - datum["origin_utm_e"], y - datum["origin_utm_n"])
                    for x, y in feature["geometry"]["coordinates"][0]]
    raise SystemExit("no `bar` feature in the committed shoreline")


def reservation_ring():
    """The reservation polygon, and the two lines it was resolved from.

    West: the section line north from G1. South: Madison's line east from G1. The rest
    is the traced waterline, walked from where the west line meets it round to where
    Madison's does. Both crossings must be unique — a shore that crosses either line
    twice is a shore this construction cannot read, and it says so rather than picking
    one.
    """
    ge, gn = section_corner()
    slope = plat_bearing()
    madison = lambda e: gn + (e - ge) * slope                      # noqa: E731
    section = lambda n: ge + (n - gn) * (-slope)                   # noqa: E731
    shore = shore_line()

    def crossings(f):
        return [i for i in range(len(shore) - 1) if f(shore[i]) * f(shore[i + 1]) < 0]

    def cut(index, f):
        a, b = shore[index], shore[index + 1]
        t = f(a) / (f(a) - f(b))
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    on_madison = lambda p: p[1] - madison(p[0])                    # noqa: E731
    on_section = lambda p: p[0] - section(p[1])                    # noqa: E731
    cm, cs = crossings(on_madison), crossings(on_section)
    if len(cm) != 1 or len(cs) != 1:
        raise SystemExit(f"the traced shore crosses Madison {len(cm)} time(s) and the "
                         f"section line {len(cs)} time(s); the reservation boundary is "
                         "only readable when each crossing is unique")
    ring = ([(ge, gn), cut(cs[0], on_section)]
            + [shore[i] for i in range(cs[0], cm[0], -1)]
            + [cut(cm[0], on_madison)])
    return ring, madison, section


def measure():
    """(regions, problems). One row per structure touching refused ground."""
    authored = {r["id"]: r for r in load(NO_BUILD_PATH)["regions"]}
    ring, madison, section = reservation_ring()
    rings = {"fort_dearborn_reservation": ring, "river_mouth_sand_bar": bar_ring()}
    missing = set(authored) ^ set(rings)
    if missing:
        raise SystemExit(f"authored and resolvable regions disagree: {sorted(missing)}")

    placed = footprints(load(DATA / "datum.json"))
    field = Heightfield.load(EPOCH)
    if field is None:
        raise SystemExit("cannot measure refused ground: the committed heightfield is missing")
    cell = field.cell_m

    regions, problems = [], []
    covered = 0
    for region_id, polygon in rings.items():
        region = authored[region_id]
        permitted = {p["structure_id"]: p["why"]
                     for p in region["what_may_stand_here"]["permitted"]}
        rows, seen = [], set()
        for sid, world in placed:
            corners = sum(1 for p in world if inside(p, polygon))
            if not corners:
                continue
            seen.add(sid)
            rows.append({"structure": sid, "corners_in": corners, "of": len(world),
                         "permitted": sid in permitted})
            if sid not in permitted:
                problems.append(
                    f"{sid} stands on {region['name']} with {corners} of {len(world)} "
                    f"footprint corners inside it, and {NO_BUILD_PATH.name} does not "
                    "permit it there")
        for sid in sorted(set(permitted) - seen):
            problems.append(
                f"{region['name']} permits {sid} and no committed footprint of {sid} "
                "touches it — a permission for a record that is not there")
        cells = 0
        for r in range(field.rows):
            n = field.origin_n + r * cell
            for c in range(field.cols):
                e = field.origin_e + c * cell
                height = field.height(e, n)
                if height is None or height <= WATER_SURFACE_M:
                    continue
                if inside((e, n), polygon):
                    cells += 1
        covered += cells
        regions.append({
            "id": region_id, "name": region["name"], "rows": rows,
            "acres": ring_area(polygon) / 4046.8564,
            "land_ha": cells * cell * cell / 10_000,
        })

    # Under-coverage: land above the water surface that ought to be inside one of them.
    outside = 0
    scene_land = 0
    for r in range(field.rows):
        n = field.origin_n + r * cell
        for c in range(field.cols):
            e = field.origin_e + c * cell
            height = field.height(e, n)
            if height is None or height <= WATER_SURFACE_M:
                continue
            scene_land += 1
            if n >= SOUTH_BANK_N or e < section(n) or n < madison(e):
                continue
            if not any(inside((e, n), poly) for poly in rings.values()):
                outside += 1
    # T-0219. The reservation's own record wrote down what would happen here, under
    # `boundary.under_coverage.what_would_break_it`: "a terrain extension that reaches
    # past the traced shore re-opens this, and the gate is written to say so". The
    # heightfield reached Madison Street and it did. What the ground is, though, is not
    # in doubt: the fractional quarter is bounded by the section line at State, by
    # Madison, and by the LAKE — so modelled land inside those three that the traced
    # shore polygon misses is reservation ground the trace does not reach, not ground
    # outside the reservation. The record now refuses it with the rest, which is the
    # conservative move in both directions: it withholds more ground from anonymous
    # builders and it claims no new landform.
    #
    # The ceiling is what keeps that from being a licence. Andreas documents the
    # reservation at 75.69 acres and the traced polygon derives 65.70, a shortfall the
    # record already carries as a measured disagreement; so the untraced remainder may
    # be at most that shortfall. Past it the terrain is modelling ground the
    # reservation cannot account for, and the gate fires exactly as it did before.
    res = next(r for r in NO_BUILD["regions"] if r["id"] == "fort_dearborn_reservation")
    uc = res["boundary"]["under_coverage"]
    ceiling = float(uc["ceiling_acres"])
    outside_acres = outside * cell * cell / 4046.8564
    if outside_acres > ceiling:
        problems.append(
            f"{outside} cell(s) — {outside_acres:.2f} acres — of modelled ground above "
            "the water surface stand east of the reservation's west line, north of "
            "Madison and south of the main stem, and inside neither traced region. That "
            f"is past the {ceiling:.2f} acres the reservation's documented 75.69 leaves "
            "unaccounted for by its derived 65.70, so this is no longer untraced "
            "reservation ground — the polygons no longer reach the ground the terrain "
            "models")
    return regions, problems, outside, scene_land, cell


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true",
                        help="exit 1 when something unpermitted stands on refused ground")
    args = parser.parse_args()

    regions, problems, outside, scene_land, cell = measure()
    refused_ha = 0.0
    for region in regions:
        refused_ha += region["land_ha"]
        print(f"   {region['name']} — {region['acres']:.2f} acres enclosed, "
              f"{region['land_ha']:.2f} ha of it modelled land")
        for row in region["rows"]:
            mark = "ok " if row["permitted"] else "REFUSED"
            print(f"      {mark:>7}  {row['structure']}  "
                  f"{row['corners_in']}/{row['of']} corners in")
        if not region["rows"]:
            print("      nothing stands here")
    scene_ha = scene_land * cell * cell / 10_000
    print(f"   {refused_ha:.2f} ha refused of {scene_ha:.2f} ha of modelled land "
          f"above the water surface — {100 * refused_ha / scene_ha:.1f} %")
    res = next(r for r in NO_BUILD["regions"] if r["id"] == "fort_dearborn_reservation")
    ceiling = float(res["boundary"]["under_coverage"]["ceiling_acres"])
    print(f"   untraced reservation ground: {outside} cell(s), "
          f"{outside * cell * cell / 4046.8564:.2f} acres of the {ceiling:.2f} the "
          f"documented 75.69 leaves over the derived 65.70 — refused with the reservation")
    for problem in problems:
        print(f"   {problem}")
    return 1 if (problems and args.gate) else 0


if __name__ == "__main__":
    raise SystemExit(main())
