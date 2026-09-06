#!/usr/bin/env python3
"""What stands on ground this project holds was not private building ground.

ROADMAP T-A16. The reservation itself is authored in
`data/reconstruction/1835_reserved_ground.json`; this is the command that measures it,
and it exists for the same reason `tools/measure_street_frontage.py` and
`tools/measure_adoption_tests.py` do — a rule nobody can run is a rule the next parcel
has to remember, and this project has now twice found a remembered number to be wrong.

A structure is ON reserved ground when any part of its footprint falls inside the
block's boundary. Not its centroid: the estray pen stands on the square's own corner
and the court-house overhangs Randolph Street, and a centroid test answers neither
of them the way a visitor would.

    tools/measure_reserved_ground.py          print the table
    tools/measure_reserved_ground.py --gate   exit 1 if anything unpermitted stands there

The gate is the one `tools/check.sh` runs. It fails on a structure the reservation does
not name, and it fails just as loudly on a permitted entry naming a record that does not
exist — a permission list that can go stale silently is a way of turning the gate off.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESERVED_PATH = DATA / "reconstruction" / "1835_reserved_ground.json"
LOTS_PATH = DATA / "traces" / "vectors" / "thompson_lots.json"
SCHOOL_SECTION_PATH = DATA / "reconstruction" / "1835_school_section_blocks.json"

sys.path.insert(0, str(ROOT / "tools"))
from plat_occupancy import footprints  # noqa: E402


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


def blocks_that_exist() -> dict[str, dict]:
    """Every block any module in this project emits, by id.

    There are two grids now. The Original Town's comes from the Thompson module and has
    been here since T-A16; the School Section's arrived with T-0797, off Wright's own
    sheet and with its own block dimensions. A reservation may name a block in either,
    and the gate below fails a reservation naming a block in NEITHER — which is the
    check that matters, because a reserved id nothing emits is a rule with no ground
    under it. Both are keyed the same way: an id and a boundary in local ENU metres.
    """
    grid = {b["id"]: b for b in load(LOTS_PATH)["blocks"]}
    if SCHOOL_SECTION_PATH.exists():
        for block in load(SCHOOL_SECTION_PATH)["blocks"]:
            grid[block["id"]] = {
                "id": block["id"],
                "boundary_local_enu_m": block["block_local_enu_m"],
                # The section was sold in lots and this project has not traced that
                # subdivision, so the module emits no `lots` here and the gate's
                # "still subdivides it" clause has nothing to catch. T-0798 is the
                # ticket that would change that, and it must not change it silently.
            }
    return grid


def measure() -> tuple[list[dict], list[str]]:
    """(rows, problems). One row per structure touching reserved ground."""
    reserved = {b["block_id"]: b for b in load(RESERVED_PATH)["blocks"]}
    grid = blocks_that_exist()
    datum = load(DATA / "datum.json")
    placed = footprints(datum)

    rows: list[dict] = []
    problems: list[str] = []
    for block_id, hold in sorted(reserved.items()):
        block = grid.get(block_id)
        if block is None:
            problems.append(f"{block_id}: reserved, and the plat module does not emit it")
            continue
        if block.get("lots"):
            problems.append(f"{block_id}: reserved, and the committed grid still "
                            f"subdivides it into {len(block['lots'])} lots")
        boundary = block["boundary_local_enu_m"]
        permitted = {p["structure_id"]: p["why"]
                     for p in hold["what_may_stand_here"]["permitted"]}
        seen: set[str] = set()
        for sid, polygon in placed:
            corners = sum(1 for p in polygon if inside(p, boundary))
            if not corners:
                continue
            seen.add(sid)
            rows.append({
                "block": block_id, "structure": sid,
                "corners_in": corners, "of": len(polygon),
                "permitted": sid in permitted,
                "why": permitted.get(sid, ""),
            })
            if sid not in permitted:
                problems.append(
                    f"{sid} stands on {block_id} ({hold['name']}) with {corners} of "
                    f"{len(polygon)} footprint corners inside it, and the reservation "
                    "does not permit it there")
        for sid in sorted(set(permitted) - seen):
            problems.append(
                f"{block_id} permits {sid} to stand on it and no committed footprint of "
                f"{sid} touches the block — a permission for a record that is not there")
    return rows, problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true",
                        help="exit 1 when something unpermitted stands on reserved ground")
    args = parser.parse_args()

    rows, problems = measure()
    for row in rows:
        mark = "ok " if row["permitted"] else "REFUSED"
        print(f"   {mark:>7}  {row['block']}  {row['structure']}  "
              f"{row['corners_in']}/{row['of']} corners in")
    if not rows:
        print("   nothing stands on reserved ground")
    for problem in problems:
        print(f"   {problem}")
    print(f"   {len(rows)} structure(s) on reserved ground, "
          f"{sum(1 for r in rows if not r['permitted'])} of them unpermitted")
    return 1 if (problems and args.gate) else 0


if __name__ == "__main__":
    raise SystemExit(main())
