#!/usr/bin/env python3
"""What a party-line run was DEALT, and what it actually STANDS ON.

T-0199. Five documented South Water Street stores could not be reconciled with the
committed plat because each, put back on its own street line, seats on a platted lot
the 665-roof schedule had already dealt to the anonymous frontage run standing on that
block face — and `tools/generate_block_infill.py` refused, in its own words, to "deal a
roof to a lot that already carries one". T-0188 named all five in writing and left the
untangling to this instrument, because the question underneath them cannot be answered
by reading the recipe: **does the run stand on the lots it was dealt?**

Measured on the committed dataset, it does not, and not by a little. Of the eight
anonymous roofs on the three blocks in question, every one stands on lot 4 or lot 2 —
and the recipes deal those runs lots 0, 2 and 4. Three lots of frontage were entitled
and one or two were occupied, because a run PACKS from one end of its own strip and
`ROW_UNITS_PER_LOT` of its units fit inside a single lot of this grid.

**That gap is not a defect in the recipes; it is what T-0079 built.** Before the core
density standard a run carried exactly one roof per lot it was dealt, so "dealt" and
"stood on" were the same list and nothing distinguished them. T-0079 retired that — a
row is a claim about the FACE, bounded by the metres of frontage it stands on and not
by the conjectural side lines it crosses — and the two lists came apart the moment it
landed. Nothing measured them apart until a documented building wanted the difference.

So the refusal these five met was the PRE-T-0079 ceiling still standing at the gate:
one roof to a lot, applied to a layer whose whole point is that it is denser than the
lot grid. The rule this module authors is the same protection expressed in the unit
T-0079 established, and it is not looser where it matters:

    a run's frontage carries ROW_UNITS_PER_LOT units per lot it was dealt, and
    every roof already standing on those lots counts against that ceiling.

A block dealt one lot and carrying three units is at its ceiling under both rules, so
nothing that was refused for want of ground is now let through — `blk_lake_clark` and
both `blk_randolph_dearborn` deals sit at exactly 3 of 3 and a documented roof seating
on their lot would still fail. What changes is the block that was refused for want of
an ENTITLEMENT it was not using: three units against nine, with six units of frontage
unbuilt and a documented store standing out in the roadway because a list said the lot
was spoken for.

Nothing here authors a coordinate or a count. `ROW_UNITS_PER_LOT` is imported from
`tools/reconcile_665.py`, where the schedule deals against it; occupancy is
`tools/plat_occupancy.py`, the same module the gate and the schedule already share; and
the run's own units are read out of the committed records' `reconstruction.frontage`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRUCTURES = DATA / "structures"
RECIPE_PATH = DATA / "reconstruction" / "1835_platted_block_parcels.json"
LOTS_PATH = DATA / "traces" / "vectors" / "thompson_lots.json"

sys.path.insert(0, str(ROOT / "tools"))

from plat_occupancy import seated_lots  # noqa: E402
from reconcile_665 import ROW_UNITS_PER_LOT  # noqa: E402


def run_ceiling(dealt_lots) -> int:
    """Units of party-line frontage the lots a run was dealt can carry.

    T-0079's figure, in T-0079's unit: the smallest lot on the committed grid carries
    23.56 m of frontage, the plat module keeps 1.5 m clear of a side line at each end
    of a run, and the committed party-line units average 6.072 m wide, so 3.39 units
    fit on the meanest lot in the town and the fourth does not.
    """
    return ROW_UNITS_PER_LOT * len(list(dealt_lots))


def frontage_load(dealt_lots, run_units, seated: dict[int, list[str]]
                  ) -> tuple[int, int, dict[int, list[str]]]:
    """(load, ceiling, the roofs already standing on the lots the run was dealt).

    `seated` is one block's slice of `plat_occupancy.seated_lots`, taken with the
    parcel's own records excluded — so what it names is everything the run did not
    build. The load is the run's units plus those roofs, because both are roofs on the
    same metres of frontage and the ceiling is a count of roofs.
    """
    standing = {index: list(seated.get(index, ())) for index in dealt_lots
                if seated.get(index)}
    load = int(run_units) + sum(len(ids) for ids in standing.values())
    return load, run_ceiling(dealt_lots), standing


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parcel_records() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """({block_id: everything this parcel built there}, {deal: its run's units}).

    A block may carry more than one deal (`blk_randolph_dearborn` carries two, on its
    two faces), so a run is identified by the recipe entry's own `programme_phase` and
    not by the block. Counting a block's runs together would read six units against one
    face's ceiling and refuse a town that is standing.
    """
    built: dict[str, list[str]] = {}
    units: dict[str, list[str]] = {}
    for path in sorted(STRUCTURES.glob("recon_1835_blk_*.json")):
        record = load(path)
        recon = record.get("reconstruction") or {}
        block = recon.get("block_id")
        if not block:
            continue
        built.setdefault(block, []).append(record["id"])
        if recon.get("frontage"):
            units.setdefault(recon["programme_phase"], []).append(record["id"])
    return built, units


def survey() -> list[dict]:
    """One row per block face carrying a party-line run."""
    datum = load(DATA / "datum.json")
    grid = load(LOTS_PATH)
    blocks = {block["id"]: block for block in grid["blocks"]}
    recipe = load(RECIPE_PATH)
    built, units = parcel_records()

    rows: list[dict] = []
    for entry in recipe["blocks"]:
        frontage = entry.get("frontage")
        if not frontage:
            continue
        block_id = entry["block_id"]
        block = blocks.get(block_id)
        if block is None:
            continue
        mine = set(built.get(block_id, ()))
        seated = seated_lots({"blocks": [block]}, datum, exclude=mine).get(block_id, {})
        # every lot this run's own units seat on, by the same two tests
        theirs = seated_lots({"blocks": [block]}, datum).get(block_id, {})
        run = units.get(entry["programme_phase"], [])
        stands_on = sorted({index for index, ids in theirs.items()
                            if set(ids) & set(run)})
        dealt = list(frontage["lots"])
        load_n, ceiling, standing = frontage_load(dealt, len(run), seated)
        rows.append({
            "block": block_id, "face": frontage["face"], "dealt": dealt,
            "stands_on": stands_on, "units": len(run), "load": load_n,
            "ceiling": ceiling, "standing": standing,
        })
    return rows


def report(rows: list[dict]) -> None:
    print(f"party-line frontage runs, dealt lots against the ground they stand on "
          f"({ROW_UNITS_PER_LOT} units per dealt lot)\n")
    print(f"{'block':<30} {'face':<6} {'dealt':<12} {'stands on':<12} "
          f"{'units':>5} {'load':>5} {'ceil':>5}  roofs already on the dealt lots")
    for row in rows:
        standing = ", ".join(f"lot {index}: {'+'.join(ids)}"
                             for index, ids in sorted(row["standing"].items())) or "—"
        print(f"{row['block']:<30} {row['face']:<6} "
              f"{str(row['dealt']):<12} {str(row['stands_on']):<12} "
              f"{row['units']:>5} {row['load']:>5} {row['ceiling']:>5}  {standing}")
    unused = sum(len(set(r["dealt"]) - set(r["stands_on"])) for r in rows)
    print(f"\n{len(rows)} runs · {sum(r['units'] for r in rows)} units · "
          f"{unused} dealt lot(s) carry none of their run's own roofs")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true",
                    help="fail if a run's frontage carries more roofs than it can")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rows = survey()
    if not args.quiet:
        report(rows)

    if args.gate:
        over = [r for r in rows if r["load"] > r["ceiling"]]
        for row in over:
            print(f"FAIL {row['block']} {row['face']} face: {row['units']} run unit(s) "
                  f"and {row['load'] - row['units']} roof(s) already standing on the "
                  f"{len(row['dealt'])} lot(s) it was dealt — {row['load']} against a "
                  f"ceiling of {row['ceiling']}", file=sys.stderr)
        if over:
            return 1
        print(f"\nOK — every run inside its own frontage: worst is "
              f"{max((r['load'], r['block']) for r in rows)[1]} at "
              f"{max(r['load'] for r in rows)} of "
              f"{max(rows, key=lambda r: r['load'])['ceiling']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
