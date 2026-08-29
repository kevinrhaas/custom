#!/usr/bin/env python3
"""Which committed street a roof FRONTS, asked of the geometry and not of a note.

T-0367. Every reconstructed dwelling in this town already knows where it stands and
which way its front looks — `placement.rotation_deg` is pinned by
`docs/GLB-CONTRACT.md` as the facade bearing, degrees clockwise from grid north — and
until now nothing could ask it the one question that follows from those two facts:
*what does the front look at?* The street a roof addresses lived only in the prose of
a `symbolic_location` or a placement note, which is a sentence a generator wrote and
not a measurement, and which no other pass could read.

That gap is what refused twenty-six documented tradesmen in
`tools/replace_invented_residents.py`. The papers say where those men were — Botsford
at the corner of Dearborn and Lake, Graves baking on South Water — and the deal could
not honour a printed address because it had no way to ask a reconstructed roof which
street it was on. It could only refuse.

    tools/fronting_street.py                        every inferred-household roof
    tools/fronting_street.py recon_1835_north_d5_026
    tools/fronting_street.py --street south_water   what fronts one street
    tools/fronting_street.py --all                  every committed roof

WHAT "FRONTS" MEANS HERE, EXACTLY

A roof fronts a street when a ray cast from the middle of its facade, along the facade
bearing, enters that street's platted corridor within `REACH_M` metres without
entering another street's corridor first. Three parts, and each is deliberate:

* **From the facade, not from the centroid.** The front is a side of the building, and
  a corner lot's centroid is equidistant from two streets while its facade is not.
  Botsford's corner is exactly the case the whole ticket turns on.
* **Along the facade bearing.** A building whose back is to South Water does not front
  South Water however close it stands. This is the test that makes the answer a
  property of the RECORD's own geometry rather than of proximity.
* **The first corridor it reaches.** A ray down a long block eventually crosses some
  street; the one it crosses first is the one the front looks at.

`REACH_M` is 45 m: a platted block between two E-W corridors is about 100 m deep, so a
roof on the far side of its own block is looking across the block at the far street and
does not front it, while every setback this project's generators use — the deepest is
`generate_block_infill`'s yard row, which stands back from the frontage by most of a
lot — falls inside it. A roof whose ray reaches nothing inside 45 m fronts NO committed
street, and that is a real answer: the north-division clusters and the fort ground are
not on the platted grid at all.

A corridor is a street's committed centreline offset both ways by half its own platted
module (`corridor_width_m`, or the 80 ft town module from `data/traces/
street_control.json`), and it is only as long as the centreline this project has drawn:
the interior test below refuses the rounded cap past a street's last vertex, so a
building beyond South Water's drawn east end does not front it. That is the same rule
`tools/plat_corridors.py` states for intrusion, made for the same reason.

WHAT THIS IS NOT. It is not evidence about the roof. A reconstructed dwelling's
position is conjectural and stays conjectural; asking it which street it fronts reads
the reconstruction's own arrangement back, and every caller must say so. It answers
"where did this project put this roof", never "where was this building".
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from plat_occupancy import layer_of_record, world_polygon  # noqa: E402

DATA = ROOT / "data"
STRUCTURES = DATA / "structures"

# How far in front of its own facade a roof may look and still be said to front what it
# finds. See the module docstring: shorter than a platted block is depth, longer than
# any setback this project's generators use.
REACH_M = 45.0

# The ray is marched rather than intersected, because a corridor is a polyline offset
# and not a convex body. A quarter of a metre is two orders of magnitude finer than the
# 20 m position uncertainty every one of these placements carries.
STEP_M = 0.25


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _streets() -> list[dict]:
    doc = load(DATA / "streets" / "1835.json")
    default = float(doc["corridor_width_m"])
    control = load(DATA / "traces" / "street_control.json")
    town_half = float(control["platted_street"]["half_width_m"])
    if abs(default - town_half * 2) > 1e-6:
        raise SystemExit("the street table's default corridor and the committed street "
                         "module disagree; one of them has moved and this module must "
                         "not choose between them")
    out = []
    for street in doc["streets"]:
        width = street.get("corridor_width_m", default)
        out.append({
            "id": street["id"],
            "name": street["name_1835"],
            "path": [(float(e), float(n)) for e, n in street["path_local_enu_m"]],
            "half_width_m": float(width) / 2.0,
        })
    return out


def streets() -> dict[str, dict]:
    """Every committed street, by id, with its own half corridor."""
    return {s["id"]: s for s in _streets()}


# Words that stand between "the corner of" and a street's own name. They are
# stripped from the back of a phrase so that "the east end of South Water Street"
# and "South Water Street" resolve to the same corridor.
_STREET_WORD = re.compile(r"^streets?$")


def _keys(lanes: dict) -> dict[str, str]:
    """Every printed form of a committed street's name, lowercased, to its id.

    'South Water Street' answers to 'south water', and 'La Salle Street' also to
    'lasalle' because the corpus prints it closed up as often as spaced. Nothing
    answers to a bare 'water': the town had two Water streets and choosing between
    them is a reading of the page, not of this table (T-0305).
    """
    out: dict[str, str] = {}
    for street_id, street in lanes.items():
        name = re.sub(r"\s+streets?$", "", street["name"].lower()).strip()
        if name.startswith("the "):      # 'The fort road', 'The bank track'
            continue
        out[name] = street_id
        if " " in name:
            out[name.replace(" ", "")] = street_id
    return out


def named_streets(place: str, lanes: dict | None = None) -> tuple[list[str], list[str]]:
    """The committed streets a place phrase names, and the ones it cannot identify.

    The gazetteer prints a place as prose — 'the corner of Dearborn and Lake
    streets', 'the east end of South Water Street', 'the market square, Chicago'.
    This reads the street names out of that prose and NOTHING else: a phrase with no
    'street' in it names no street here, so the Public Square and the market square
    resolve to nothing rather than to Market Street.

    The second list is the honest half. 'Water Street' is printed five times in this
    corpus and there were two of them; it comes back unresolved, and a caller that
    needs a street must say so rather than guess.
    """
    lanes = streets() if lanes is None else lanes
    keys = _keys(lanes)
    tokens = re.findall(r"[a-z]+", (place or "").lower())
    found: list[str] = []
    unresolved: list[str] = []
    for i, token in enumerate(tokens):
        if not _STREET_WORD.match(token):
            continue
        window = tokens[max(0, i - 5):i]
        segments, current = [], []
        for word in window:
            if word == "and":
                segments.append(current)
                current = []
            else:
                current.append(word)
        segments.append(current)
        for segment in segments:
            if not segment:
                continue
            for span in (3, 2, 1):
                phrase = " ".join(segment[-span:]) if len(segment) >= span else None
                if phrase and phrase in keys:
                    if keys[phrase] not in found:
                        found.append(keys[phrase])
                    break
            else:
                if segment[-1] not in unresolved:
                    unresolved.append(segment[-1])
    return found, unresolved


def _inside_corridor(point, street) -> bool:
    """Is the point within half a corridor of the street's centreline, off a cap?

    The projection has to land strictly INSIDE a segment. A point beyond a street's
    last vertex is nearest to that vertex, and counting it would extend every corridor
    by a half-disc the plat does not have — the same refusal `tools/plat_corridors.py`
    makes by clipping its rings to the drawn centreline.
    """
    px, py = point
    path = street["path"]
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        dx, dy = bx - ax, by - ay
        span = dx * dx + dy * dy
        if span == 0:
            continue
        t = ((px - ax) * dx + (py - ay) * dy) / span
        if not 0.0 <= t <= 1.0:
            continue
        if math.hypot(px - (ax + t * dx), py - (ay + t * dy)) <= street["half_width_m"]:
            return True
    return False


def facade(polygon: list, bearing_deg: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """The middle of the front wall, and the unit vector the front looks along.

    `rotation_deg` is the facade bearing clockwise from grid north (GLB-CONTRACT), so
    the outward direction is (sin, cos) in ENU. The facade is the footprint's frontmost
    edge along that direction: the vertices whose projection is within a centimetre of
    the greatest, averaged. A rectangle gives its two front corners and their midpoint;
    an L-plan gives the front of whichever wing stands forward, which is the wall a
    visitor on the street sees.
    """
    theta = math.radians(float(bearing_deg or 0.0))
    look = (math.sin(theta), math.cos(theta))
    reach = [p[0] * look[0] + p[1] * look[1] for p in polygon]
    front = max(reach)
    on_face = [p for p, r in zip(polygon, reach) if front - r <= 0.01]
    mid = (sum(p[0] for p in on_face) / len(on_face),
           sum(p[1] for p in on_face) / len(on_face))
    return mid, look


def fronts_of_polygon(polygon: list, bearing_deg: float,
                      lanes: dict | None = None) -> dict | None:
    """The street this footprint's facade looks into, or None."""
    lanes = streets() if lanes is None else lanes
    (ex, ny), look = facade(polygon, bearing_deg)
    steps = int(REACH_M / STEP_M)
    for k in range(steps + 1):
        point = (ex + look[0] * STEP_M * k, ny + look[1] * STEP_M * k)
        for street in lanes.values():
            if _inside_corridor(point, street):
                return {"street": street["id"], "name": street["name"],
                        "reach_m": round(STEP_M * k, 2)}
    return None


def _placed_phase(record: dict) -> dict | None:
    for phase in record.get("phases") or []:
        position = phase.get("position") or {}
        polygon = (phase.get("footprint") or {}).get("polygon") or []
        if position.get("utm_e") is not None and len(polygon) >= 3:
            return phase
    return None


def fronts(record: dict, datum: dict | None = None,
           lanes: dict | None = None) -> dict | None:
    """Which committed street this structure record's front looks at, or None."""
    phase = _placed_phase(record)
    if phase is None:
        return None
    datum = load(DATA / "datum.json") if datum is None else datum
    polygon = world_polygon(phase, datum)
    return fronts_of_polygon(polygon, phase["position"].get("rotation_deg") or 0.0, lanes)


def table(ids: list[str] | None = None, layer: str | None = None) -> dict[str, dict | None]:
    """structure id -> its fronted street (or None), for every committed record."""
    datum = load(DATA / "datum.json")
    lanes = streets()
    out: dict[str, dict | None] = {}
    for path in sorted(STRUCTURES.glob("*.json")):
        record = load(path)
        if ids is not None and record["id"] not in ids:
            continue
        if layer is not None and layer_of_record(record) != layer:
            continue
        out[record["id"]] = fronts(record, datum, lanes)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="structure ids (default: the household layer)")
    ap.add_argument("--all", action="store_true", help="every committed roof")
    ap.add_argument("--street", help="list only what fronts this street id")
    args = ap.parse_args()

    if args.ids:
        rows = table(ids=args.ids)
        missing = [i for i in args.ids if i not in rows]
        if missing:
            print(f"no committed structure record for {', '.join(missing)}")
            return 1
    else:
        rows = table(layer=None if args.all else "inferred_household")
    if args.street:
        rows = {k: v for k, v in rows.items() if v and v["street"] == args.street}

    print(f"the street each roof's FACADE looks into, within {REACH_M:g} m "
          f"(reconstructed arrangement, not evidence)\n")
    for structure_id, front in sorted(rows.items()):
        if front:
            print(f"  {structure_id:34s} {front['name']:20s} {front['reach_m']:6.2f} m")
        else:
            print(f"  {structure_id:34s} {'—  no committed street in front':20s}")
    seated = sum(1 for f in rows.values() if f)
    print(f"\n  {seated} of {len(rows)} roof(s) front a committed street")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
