#!/usr/bin/env python3
"""The platted street corridors, as one question asked in one place.

ROADMAP K7 phase two (a). The grid report found buildings standing in the road; the
generator that put them there had never asked. Both sides now read this module, so the
gate and the report cannot answer differently — which is the same reason
`generators/mesh_inputs.py` exists for the staleness hash.

What a corridor IS here: a committed street centreline from `data/streets/1835.json`,
offset both ways by half the platted module in `data/traces/street_control.json`. It is
therefore only as long as the centreline this project has drawn, and a building beyond a
street's drawn end is not in it. The geometry is `generate_plat_lots.corridor_rings` —
imported rather than copied.

What a corridor IS NOT: the travelled way. L79 records that the visible tracks run
5.8-10.5 m inside an 80 ft legal corridor, so a building inside the corridor is not
necessarily a building in anybody's way. That is exactly why this module reports a DEPTH
and lets each caller set its own bar: an invented placement has no business in the
roadway at all, while an attested frontage that lands a few metres inside it is a
measurement about the georeference and about the plat, not a defect in the record.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from generate_plat_lots import (  # noqa: E402
    DATA, corridor_rings, load, point_in_polygon, point_to_ring_m, street_lines,
)

# Footprint edges are sampled at this pitch before the point test. A corridor is 24 m
# wide and no footprint in this dataset is, so a building cannot straddle one without
# putting a sample inside it; the sampling is there for the corner cases at a corridor's
# drawn END, where the ring turns.
SAMPLE_M = 0.5


def corridors() -> dict:
    """Every grid street's platted corridor, by street id."""
    control = load(DATA / "traces" / "street_control.json")
    half_width = float(control["platted_street"]["half_width_m"])
    lines = street_lines(load(DATA / "streets" / "1835.json"))
    return {sid: {"name": lines[sid]["name"], "ring": ring, "points": lines[sid]["points"]}
            for sid, ring in corridor_rings(lines, half_width).items()}


def sampled(polygon: list, pitch: float = SAMPLE_M) -> list:
    """A polygon's vertices plus points along its edges."""
    points = []
    for i, a in enumerate(polygon):
        b = polygon[(i + 1) % len(polygon)]
        steps = max(1, int(math.dist(a, b) / pitch))
        points += [(a[0] + (b[0] - a[0]) * k / steps, a[1] + (b[1] - a[1]) * k / steps)
                   for k in range(steps)]
    return points


def intrusion(polygon: list, lanes: dict | None = None) -> tuple[str | None, float]:
    """The deepest a footprint reaches into any platted corridor.

    Returns the street id and the depth in metres, or `(None, 0.0)` if the footprint is
    clear of every corridor. Depth is measured from the corridor's own edge, so it is how
    far into the roadway the building's worst corner stands — not a distance to the
    centreline.
    """
    lanes = corridors() if lanes is None else lanes
    worst_id, worst = None, 0.0
    points = sampled(polygon)
    for street_id, lane in lanes.items():
        ring = lane["ring"]
        for point in points:
            if point_in_polygon(point, ring):
                depth = point_to_ring_m(point, ring)
                if depth > worst:
                    worst_id, worst = street_id, depth
    return worst_id, worst
