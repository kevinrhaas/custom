#!/usr/bin/env python3
"""The School Section's grid, off Wright's 1834 sheet and onto the ground.

Section 16, T39N R14E — the mile square south of Madison Street the state sold in
October 1833 to fund the schools. Wright drew it whole: 13 columns of blocks by 12
tiers, 142 of the 156 cells numbered and the other 14 taken by the South Branch.
None of it existed in this project before T-0797; the plat module stops at Madison.

It joins the project's two readings of that grid and does the arithmetic between them.
`data/traces/school_section_block_numbering.json` (T-0875) says which FIGURE stands in
which cell, and says in terms that its own local-metre grid is for crops only.
`data/traces/school_section_module_1834.json` (T-0876) is the other half: the ruled lines
in the registered scan's pixels, the street each is lettered as, and the module those give.
Neither is complete without the other, and the two were read independently:

    tools/read_school_section_grid.py --build       write the derived blocks
    tools/read_school_section_grid.py --check       committed == derived, and the reading is sound
    tools/read_school_section_grid.py --self-test   the arithmetic, on cases whose answer is known
    tools/read_school_section_grid.py --sale-test   what the October 1833 sale says about the reservations

WHY THE MODULE IS MEASURED RATHER THAN BORROWED. The Original Town's block is 320 by
380 feet with an alley through it. This one is not: it is 318 by 368 feet and has no
alley, and the difference is read off the sheet rather than assumed. The ticket asked
for that in terms, and a borrowed module would have put every one of the 142 blocks a
few metres from where Wright drew it, all the way across a mile.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MODULE = DATA / "traces" / "school_section_module_1834.json"
NUMBERING = DATA / "traces" / "school_section_block_numbering.json"
GCP = DATA / "traces" / "gcp" / "wright_1834_nara_hup_gcps.json"
DATUM = DATA / "datum.json"
OUT = DATA / "reconstruction" / "1835_school_section_blocks.json"
GROUND = DATA / "research" / "land_sales" / "ground.json"

CORRIDOR_M = 24.384  # 80 ft, the town's platted street module and the sheet's own mean


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ the geometry

def affine():
    """NA-sheet pixel -> local ENU metres, through the committed registration."""
    c = load(GCP)["fit"]["coefficients"]
    d = load(DATUM)
    a, b, cc, dd, e, f = c["a"], c["b"], c["c"], c["d"], c["e"], c["f"]
    ox, oy = d["origin_utm_e"], d["origin_utm_n"]

    def to_local(px: float, py: float) -> tuple[float, float]:
        return (a * px + b * py + cc - ox, dd * px + e * py + f - oy)

    return to_local


def corner_pixel(vx: float, hy: float, tilt: float, vref: float, href: float):
    """Where north-south line `vx` meets east-west line `hy`, in sheet pixels.

    The grid leans in the raster, so neither line is axis-aligned:
        x(y) = vx - t*(y - vref)        y(x) = hy + t*(x - href)
    Two lines, two unknowns, and the substitution closes in one step.
    """
    t = tilt
    x = (vx - t * (hy - t * href - vref)) / (1.0 + t * t)
    y = hy + t * (x - href)
    return x, y


def inset_polygon(corners, metres: float):
    """Shrink a convex quadrilateral by `metres` measured perpendicular to each side.

    The cell is the ground from street centreline to street centreline; the BLOCK is
    what is left when each of the four corridors gives up its half. Sides are offset
    inward and re-intersected, which is exact for a quadrilateral this near-rectangular.
    """
    n = len(corners)
    cx = sum(p[0] for p in corners) / n
    cy = sum(p[1] for p in corners) / n
    lines = []
    for i in range(n):
        (ax, ay), (bx, by) = corners[i], corners[(i + 1) % n]
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy)
        if length == 0:
            raise SystemExit("a cell side of zero length cannot be inset")
        nx, ny = -dy / length, dx / length
        if nx * (cx - ax) + ny * (cy - ay) < 0:
            nx, ny = -nx, -ny
        lines.append(((ax + nx * metres, ay + ny * metres),
                      (bx + nx * metres, by + ny * metres)))
    out = []
    for i in range(n):
        p = intersect(lines[i - 1], lines[i])
        if p is None:
            raise SystemExit("two sides of a cell are parallel and cannot be mitred")
        out.append([round(p[0], 2), round(p[1], 2)])
    return out


def intersect(first, second):
    (x1, y1), (x2, y2) = first
    (x3, y3), (x4, y4) = second
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9:
        return None
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / den,
            (a * (y3 - y4) - (y1 - y2) * b) / den)


def area(polygon) -> float:
    s = 0.0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


# ------------------------------------------------------------------- the derivation

def derive() -> dict:
    trace = load(MODULE)
    numbering = load(NUMBERING)
    to_local = affine()
    tilt = trace["tilt"]["tangent"]
    vref = trace["tilt"]["north_south_reference_y"]
    href = trace["tilt"]["east_west_reference_x"]
    ns = {line["index"]: line for line in trace["lines"]["north_south"]}
    ew = {line["index"]: line for line in trace["lines"]["east_west"]}

    blocks = []
    for entry in sorted(numbering["blocks"], key=lambda b: b["number"]):
        col, tier = entry["column"], entry["tier"]
        cell = []
        for vi, hj in ((col, tier), (col + 1, tier), (col + 1, tier + 1), (col, tier + 1)):
            px, py = corner_pixel(ns[vi]["pixel_x"], ew[hj]["pixel_y"], tilt, vref, href)
            cell.append(to_local(px, py))
        blocks.append({
            "id": f"ss_blk_{entry['number']:03d}",
            "block_number": entry["number"],
            "column": col,
            "tier": tier,
            "tract": trace["tract"],
            "numeral_confidence": entry["confidence"],
            "numeral_on_sheet": entry["numeral_on_sheet"],
            "numeral_crop_px": entry["numeral_crop_px"],
            "written_on_sheet": entry.get("written_on_sheet"),
            "lettered_reserved": entry["number"] in set(trace["reserved"]["blocks"]),
            "cell_local_enu_m": [[round(x, 2), round(y, 2)] for x, y in cell],
            "block_local_enu_m": inset_polygon(cell, CORRIDOR_M / 2.0),
            "bounded_by": {
                "north": ew[tier].get("name"),
                "south": ew[tier + 1].get("name"),
                "west": ns[col].get("name"),
                "east": ns[col + 1].get("name"),
            },
        })
    for block in blocks:
        block["block_area_m2"] = round(area(block["block_local_enu_m"]), 1)

    streets = []
    for line in trace["lines"]["east_west"]:
        j = line["index"]
        a = corner_pixel(ns[1]["pixel_x"], line["pixel_y"], tilt, vref, href)
        b = corner_pixel(ns[14]["pixel_x"], line["pixel_y"], tilt, vref, href)
        streets.append({
            "line_index": j,
            "name": line.get("name"),
            "name_on_sheet": line["name_on_sheet"],
            "path_local_enu_m": [[round(v, 1) for v in to_local(*a)],
                                 [round(v, 1) for v in to_local(*b)]],
        })

    corners = {}
    for key, (vi, hj) in {"north_west": (1, 1), "north_east": (14, 1),
                          "south_east": (14, 13), "south_west": (1, 13)}.items():
        px, py = corner_pixel(ns[vi]["pixel_x"], ew[hj]["pixel_y"], tilt, vref, href)
        corners[key] = [round(v, 1) for v in to_local(px, py)]
    span_e = corners["north_east"][0] - corners["north_west"][0]
    span_n = corners["north_west"][1] - corners["south_west"][1]

    return {
        "$schema_note": (
            "GENERATED by tools/read_school_section_grid.py --build, from the numerals in "
            "data/traces/school_section_block_numbering.json and the ruled lines in "
            "data/traces/school_section_module_1834.json. Do not hand-edit: --check re-derives it and "
            "fails on any difference. Both readings are traces; only the arithmetic between them is here."),
        "id": "school_section_blocks_1835",
        "ticket": "T-0876",
        "generated_by": "tools/read_school_section_grid.py --build",
        "source_id": "wright_1834_nara_hup",
        "target_date": "1835-07-01",
        "tract": "school_section_1833",
        "geometry_confidence": "inferred",
        "geometry_note": (
            "The lines are read off the sheet and carried through the committed registration, whose own "
            "RMS against modern control is 16.2 m. That is the working uncertainty of every corner here, "
            "and it is larger than the difference between any two candidate readings of a ruled line. "
            "`cell_local_enu_m` is centreline to centreline; `block_local_enu_m` is the same cell with "
            "half of an 80 ft corridor taken off each side, which is the width the sheet's own drawn "
            "street pairs measure."),
        "what_is_not_here": (
            "No lot. No roof. No land-sale row placed. The section was sold and not built, and T-0798 "
            "is the ticket that spends the sale onto these numbers."),
        "corridor_width_m": CORRIDOR_M,
        "section": {
            "corners_local_enu_m": corners,
            "span_east_m": round(span_e, 1),
            "span_north_m": round(span_n, 1),
            "a_mile_is_m": 1609.344,
            "note": (
                "A section is a mile square. This one measures "
                f"{span_e:.0f} m by {span_n:.0f} m — {span_e / 1609.344 * 100:.1f}% and "
                f"{span_n / 1609.344 * 100:.1f}% of a mile. The east-west figure is the sheet's honest "
                "scale; the north-south overrun is the registration's known 5.2% axis anisotropy, which "
                "the manuscript's mounting put in the long axis. It is stated rather than corrected: "
                "correcting it here would put this grid out of the frame everything else is in."),
        },
        "counts": {
            "blocks": len(blocks),
            "numerals_read": sum(1 for b in blocks if b["numeral_on_sheet"]),
            "numerals_inferred": sum(1 for b in blocks if not b["numeral_on_sheet"]),
            "lettered_reserved": sum(1 for b in blocks if b["lettered_reserved"]),
            "cells_the_south_branch_takes": 13 * 12 - len(numbering["blocks"]),
        },
        "east_west_lines": streets,
        "blocks": blocks,
    }


# ------------------------------------------------------------------------ the sale

def sale_test() -> dict:
    """Which of the 142 numbers the October 1833 auction never sold a lot in."""
    ground = load(GROUND)
    rows = [t for t in ground["tracts"] if t.get("refusal") == "subdivision_plat_not_held"]
    sold: dict[int, int] = {}
    for row in rows:
        m = re.search(r"BL(?:K|OCK)?\s*(\d+)", (row.get("part") or "").upper())
        if m:
            sold[int(m.group(1))] = sold.get(int(m.group(1)), 0) + 1
    untouched = [n for n in range(1, 143) if n not in sold]
    reserved = sorted(load(MODULE)["reserved"]["blocks"])
    return {
        "rows": len(rows),
        "blocks_sold": len(sold),
        "untouched": untouched,
        "reserved": reserved,
        "reserved_untouched": [n for n in reserved if n in untouched],
        "reserved_sold": {n: sold[n] for n in reserved if n in sold},
        "untouched_and_not_lettered": [n for n in untouched if n not in reserved],
        "sold_in_119": sold.get(119, 0),
    }


# ----------------------------------------------------------------------- the checks

def check(quiet: bool = False) -> int:
    problems: list[str] = []
    module = load(MODULE)
    numbering = load(NUMBERING)

    # THE TWO READINGS HAVE TO AGREE ABOUT THE SHAPE OF THE GRID. They were taken
    # independently — T-0875 read figures off the sheet without this lattice, T-0876
    # picked the lattice off ink without the figures — and that is worth nothing unless
    # somebody asks them the same question. A lattice of 14 by 13 lines is 13 columns by
    # 12 tiers; the numbering says how many of those 156 cells carry a figure and where
    # the river takes the rest. If those two ever part company the join below is arithmetic
    # over a mismatch, and it must not be built.
    columns = len(module["lines"]["north_south"]) - 1
    tiers = len(module["lines"]["east_west"]) - 1
    if (columns, tiers) != (numbering["grid"]["columns"], numbering["grid"]["tiers"]):
        problems.append(f"the module rules {columns}x{tiers} and the numbering reads "
                        f"{numbering['grid']['columns']}x{numbering['grid']['tiers']}")
    numbers = sorted(b["number"] for b in numbering["blocks"])
    if numbers != list(range(1, 143)):
        problems.append("the numbering does not carry 1..142 exactly once")
    for entry in numbering["blocks"]:
        if not 1 <= entry["column"] <= columns or not 1 <= entry["tier"] <= tiers:
            problems.append(f"block {entry['number']} sits at column {entry['column']}, "
                            f"tier {entry['tier']}, which the module does not rule")

    # And the module's own claims about itself.
    for axis in ("north_south", "east_west"):
        lines = module["lines"][axis]
        picks = [line["pixel_" + ("x" if axis == "north_south" else "y")] for line in lines]
        if picks != sorted(picks):
            problems.append(f"the {axis} lines are not in order across the sheet")
        for line in lines:
            if line["name_on_sheet"] != (line["name"] is not None):
                problems.append(f"{axis} line {line['index']} disagrees with itself about "
                                "whether the sheet letters it")
    named = sum(1 for line in module["lines"]["east_west"] if line["name_on_sheet"])
    if named != 4:
        problems.append(f"the sheet letters four tiers and the module carries {named}")

    # THE RESERVATIONS ARE READ IN TWO FILES AND MUST NOT PART. T-0875 sees `Reserved`
    # only where the sheet writes it INSTEAD of a numeral, so it has the two corner blocks
    # and not 87 and 88, where the word stands beside the figures. This file carries all
    # four. A cell T-0875 letters Reserved and this one does not is a reading that has
    # drifted, and it fails here rather than in whatever spends it.
    theirs = {b["number"] for b in numbering["blocks"]
              if str(b.get("written_on_sheet") or "").lower() == "reserved"}
    ours = set(module["reserved"]["blocks"])
    if theirs - ours:
        problems.append(f"the numbering letters {sorted(theirs - ours)} Reserved and the module does not")
    for number in ours:
        if number not in {b["number"] for b in numbering["blocks"]}:
            problems.append(f"the module reserves block {number} and the numbering has no such block")

    if not OUT.exists():
        problems.append(f"{OUT.relative_to(ROOT)} is missing — run --build")
    else:
        if json.dumps(derive(), sort_keys=True) != json.dumps(load(OUT), sort_keys=True):
            problems.append(f"{OUT.relative_to(ROOT)} is not what the two readings derive — run --build")

    sale = sale_test()
    if sorted(sale["reserved_untouched"]) != sorted(sale["reserved"]):
        problems.append("a block the sheet letters Reserved carries a lot sale: "
                        f"{sale['reserved_sold']}")

    if problems:
        for p in problems:
            print(f"  FAULT  {p}")
        print(f"school section grid: {len(problems)} fault(s)")
        return 1
    if not quiet:
        read = sum(1 for b in numbering["blocks"] if b["numeral_on_sheet"])
        print(f"school section grid: {len(numbers)} blocks on {columns}x{tiers} cells, "
              f"{read} numerals read, the two readings agree on the grid, "
              f"and the sale corroborates all {len(sale['reserved'])} reservations")
    return 0


def self_test() -> int:
    """The arithmetic, on cases whose answer is known independently."""
    failures: list[str] = []
    trace = load(MODULE)
    numbering = load(NUMBERING)
    to_local = affine()
    tilt = trace["tilt"]["tangent"]
    vref = trace["tilt"]["north_south_reference_y"]
    href = trace["tilt"]["east_west_reference_x"]

    # 1. The corner solver lands on both lines it was given.
    x, y = corner_pixel(2000.0, 4000.0, tilt, vref, href)
    if abs(x - (2000.0 - tilt * (y - vref))) > 1e-6:
        failures.append("the corner is not on its north-south line")
    if abs(y - (4000.0 + tilt * (x - href))) > 1e-6:
        failures.append("the corner is not on its east-west line")

    # 2. Zero tilt is the trivial answer, exactly.
    if corner_pixel(10.0, 20.0, 0.0, 0.0, 0.0) != (10.0, 20.0):
        failures.append("with no tilt the corner is not the pair it was given")

    # 3. The registration carries G1 to where the GCP file says it lies.
    g1 = next(g for g in load(GCP)["gcps"] if g["id"] == "G1")
    datum = load(DATUM)
    want = (g1["modern"]["utm_e"] - datum["origin_utm_e"],
            g1["modern"]["utm_n"] - datum["origin_utm_n"])
    got = to_local(*g1["pixel"])
    if math.dist(want, got) > load(GCP)["fit"]["rms_m"] + 1.0:
        failures.append("the affine does not put G1 within the fit's own RMS of its control")

    # 4. A unit square inset by a quarter has half the side and a quarter the area.
    square = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    small = inset_polygon(square, 25.0)
    if abs(area(small) - 2500.0) > 1e-6:
        failures.append("insetting a 100 m square by 25 m does not leave 2500 m2")

    # 5. Insetting by nothing changes nothing.
    if [[round(x, 2), round(y, 2)] for x, y in square] != inset_polygon(square, 0.0):
        failures.append("insetting by zero moved a corner")

    # 6. Every derived block is inside its own cell, and smaller than it.
    for block in derive()["blocks"][:12]:
        if area(block["block_local_enu_m"]) >= area(block["cell_local_enu_m"]):
            failures.append(f"{block['id']}: the block is not smaller than its cell")

    # 7. The sale test finds the reservations and does not find block 119.
    sale = sale_test()
    if sale["sold_in_119"] == 0:
        failures.append("the sale test says nothing was sold in block 119, and nine lots were")
    if 142 in sale["untouched"] and 142 not in sale["reserved"]:
        failures.append("142 is untouched by the sale and is not carried as reserved")

    # 8. The measured module is not Thompson's.
    block_m = trace["module"]["block_m"]
    if abs(block_m[0] - 96.8) > 1.0 or abs(block_m[1] - 112.2) > 1.0:
        failures.append("the recorded block module is not the one measured off the sheet")

    # 9. The lattice this file picks and the one T-0875 picked for its crops describe the
    #    same grid on the ground. They were measured apart and neither is the other's
    #    source, so agreement is a fact and disagreement past the sheet's own stretch
    #    would mean one of them is reading a different set of lines.
    theirs = load(NUMBERING)["grid"]
    ours = derive()
    mine_e = [ours["blocks"][0]["cell_local_enu_m"][0][0]]
    gap = abs(theirs["column_lines_local_e_m"][0] - ours["section"]["corners_local_enu_m"]["north_west"][0])
    if gap > 40.0:
        failures.append(f"the two readings' west lines stand {gap:.0f} m apart, which is past "
                        "the registration's own uncertainty")

    if failures:
        for f in failures:
            print(f"  FAIL  {f}")
        return 1
    print("read_school_section_grid: 9 self-test(s) pass")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--sale-test", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.build:
        OUT.write_text(json.dumps(derive(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        doc = load(OUT)
        print(f"wrote {OUT.relative_to(ROOT)}: {doc['counts']['blocks']} blocks, "
              f"{doc['counts']['numerals_read']} numerals read off the sheet")
        return 0
    if args.self_test:
        return self_test()
    if args.sale_test:
        sale = sale_test()
        print(f"section 16 lot sales read: {sale['rows']} rows over {sale['blocks_sold']} blocks")
        print(f"blocks the sale never touches: {sale['untouched']}")
        print(f"the sheet letters Reserved: {sale['reserved']}")
        print(f"reserved and never sold: {sale['reserved_untouched']}")
        print(f"never sold and not lettered: {sale['untouched_and_not_lettered']}")
        print(f"lots sold in block 119 (T-0791 read it as the reserved corner): {sale['sold_in_119']}")
        return 0
    return check(quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
