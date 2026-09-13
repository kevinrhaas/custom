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

A boundary is resolved one of three ways, and the region's own `boundary.method` says
which — the file drives this command rather than this command knowing the regions:

* `derived` — the reservation, built from one control point, the plat's own bearing and
  the traced waterline.
* `committed_polygon` — the bar, lifted whole from a feature of a committed trace.
* `plate_read` — a ring MEASURED off a raster in pixels and resolved to ground by that
  reading's own stated transform (T-0891). The pixels are the reading; the metres are a
  derivation of them, and this command re-derives them rather than trusting the copy the
  trace stores, so a transform edited away from the ring it produced fails loudly. It is
  the same discipline `data/datum.json` is held to, and it is what lets a ring read off a
  plate enter this file without a hand-typed vertex.

Three things fail the gate, and the third is the one worth having:

1. A structure standing on refused ground that the region does not permit.
2. A permitted entry naming a record that is not there — a permission list that can go
   stale in silence is a way of turning the gate off.
3. UNDER-COVERAGE. Every cell of the committed heightfield above the water surface,
   east of the reservation's west line, north of Madison's line and south of the main
   stem, must fall inside one of the polygons. It does today, exactly: the count is
   zero. T-E3 extends the terrain east and south, and when it does, this is the
   assertion that will notice that the polygons no longer reach the ground.

Regions may NEST — the Fort Cemetery stands wholly inside the reservation — so the share
of modelled land that is refused is counted over the UNION of the polygons and never by
adding the regions up. A nested region is not redundant: it refuses the same ground on
its own evidence, and its boundary does not move when the reservation's floor does.
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


def plate_ring(control):
    """A ring measured off a raster in pixels, resolved to local ground by the reading's
    own transform — and RE-DERIVED here rather than read out of the trace's metres.

    `control` is the region's `boundary.control`, and it names the trace, the source that
    trace reads, the key the ring sits under and the label the plate letters it with. All
    four are asserted: a reading that is renamed, re-sourced or re-lettered is a different
    reading, and this must not silently accept it in place of the one the region cites.

    The transform is the three numbers a plate reading states — an anchor pixel, where
    that pixel lands in local ENU, and a scale — plus the orientation the pixels are
    measured in. Only `+x east` / `+y south` is understood; a plate measured any other way
    stops here instead of being resolved by the wrong sign.
    """
    trace = load(ROOT / control["trace"])
    if trace.get("source_id") != control["source_id"]:
        raise SystemExit(f"{control['trace']} reads {trace.get('source_id')!r}, and the "
                         f"region cites {control['source_id']!r}")
    reading = trace.get(control["ring"])
    if reading is None:
        raise SystemExit(f"{control['trace']} no longer carries a {control['ring']!r} ring")
    if reading.get("label_as_read") != control["label"]:
        raise SystemExit(f"{control['ring']} is lettered {reading.get('label_as_read')!r} "
                         f"and the region cites {control['label']!r}")

    transform = trace["the_transform"]
    orientation = transform.get("orientation", "")
    if "+x east" not in orientation or "+y south" not in orientation:
        raise SystemExit(f"{control['trace']} is measured {orientation!r}; this command "
                         "resolves +x east / +y south pixels only")
    (ax, ay) = transform["anchor_px"]
    (ae, an) = transform["anchor_local_enu_m"]
    scale = transform["scale_m_per_px"]
    ring = [(ae + (x - ax) * scale, an - (y - ay) * scale)
            for x, y in reading["corners_px"]]

    # The trace states the same corners in metres. They are a DERIVATION of the pixels,
    # so they are checked against this one rather than used: the tolerance is the rounding
    # the trace prints to, and anything larger is the transform and the ring disagreeing.
    stored = reading["corners_local_enu_m"]
    if len(stored) != len(ring):
        raise SystemExit(f"{control['ring']} has {len(reading['corners_px'])} corners in "
                         f"pixels and {len(stored)} in metres")
    for i, ((e, n), (se, sn)) in enumerate(zip(ring, stored)):
        drift = max(abs(e - se), abs(n - sn))
        if drift > 0.02:
            raise SystemExit(
                f"{control['ring']} corner {i} re-derives from its own transform to "
                f"({e:.2f}, {n:.2f}) and the trace stores ({se:.2f}, {sn:.2f}) — "
                f"{drift:.2f} m apart; the transform and the ring no longer agree")
    return ring


def resolve(region):
    """The ring for one authored region, dispatched on the method the region declares."""
    boundary = region["boundary"]
    method = boundary.get("method")
    if method == "derived":
        return reservation_ring()[0]
    if method == "committed_polygon":
        return bar_ring()
    if method == "plate_read":
        return plate_ring(boundary["control"])
    raise SystemExit(f"{region['id']} declares boundary method {method!r}, and this "
                     "command resolves derived, committed_polygon and plate_read")


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
    # The under-coverage window is drawn on the reservation's own two survey lines, so
    # that region has to be here and has to be the derived one.
    derived = [r["id"] for r in authored.values() if r["boundary"].get("method") == "derived"]
    if derived != ["fort_dearborn_reservation"]:
        raise SystemExit(f"the derived region is {derived}, and the under-coverage window "
                         "is drawn on the reservation's west and south lines")
    _, madison, section = reservation_ring()
    rings = {region_id: resolve(region) for region_id, region in authored.items()}

    placed = footprints(load(DATA / "datum.json"))
    field = Heightfield.load(EPOCH)
    if field is None:
        raise SystemExit("cannot measure refused ground: the committed heightfield is missing")
    cell = field.cell_m

    # ONE walk of the heightfield, answering three questions at once: how much modelled
    # land each region holds, how much the regions hold BETWEEN them (they may nest, so
    # this is a union and not a sum), and whether any land in the reservation's window
    # falls outside every one of them.
    land_cells = {region_id: 0 for region_id in rings}
    union_cells = 0
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
            hits = [rid for rid, poly in rings.items() if inside((e, n), poly)]
            for rid in hits:
                land_cells[rid] += 1
            if hits:
                union_cells += 1
            elif not (n >= SOUTH_BANK_N or e < section(n) or n < madison(e)):
                outside += 1

    regions, problems = [], []
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
        within = [other for other, poly in rings.items()
                  if other != region_id and all(inside(p, poly) for p in polygon)]
        regions.append({
            "id": region_id, "name": region["name"], "rows": rows,
            "acres": ring_area(polygon) / 4046.8564,
            "land_ha": land_cells[region_id] * cell * cell / 10_000,
            "within": within,
        })

    if outside:
        problems.append(
            f"{outside} cell(s) of modelled ground above the water surface stand east "
            "of the reservation's west line, north of Madison and south of the main "
            "stem, and inside neither refused region — the polygons no longer reach "
            "the ground the terrain models")
    refused_ha = union_cells * cell * cell / 10_000
    return regions, problems, outside, scene_land, cell, refused_ha


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true",
                        help="exit 1 when something unpermitted stands on refused ground")
    args = parser.parse_args()

    regions, problems, outside, scene_land, cell, refused_ha = measure()
    for region in regions:
        nested = ""
        if region["within"]:
            names = {r["id"]: r["name"] for r in regions}
            nested = " — inside " + ", ".join(names[i] for i in region["within"])
        print(f"   {region['name']} — {region['acres']:.2f} acres enclosed, "
              f"{region['land_ha']:.2f} ha of it modelled land{nested}")
        for row in region["rows"]:
            mark = "ok " if row["permitted"] else "REFUSED"
            print(f"      {mark:>7}  {row['structure']}  "
                  f"{row['corners_in']}/{row['of']} corners in")
        if not region["rows"]:
            print("      nothing stands here")
    scene_ha = scene_land * cell * cell / 10_000
    print(f"   {refused_ha:.2f} ha refused of {scene_ha:.2f} ha of modelled land "
          f"above the water surface — {100 * refused_ha / scene_ha:.1f} % "
          "(the union of the regions; nested ground is counted once)")
    print(f"   under-coverage: {outside} cell(s) of modelled land outside every region")
    for problem in problems:
        print(f"   {problem}")
    return 1 if (problems and args.gate) else 0


if __name__ == "__main__":
    raise SystemExit(main())
