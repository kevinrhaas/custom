#!/usr/bin/env python3
"""Put the land-sale tracts on the ground, and name the ground under a roof (T-0609).

    tools/resolve_land_tracts.py --build   derive ground.json and write `land_owner`
    tools/resolve_land_tracts.py --check   the gate: re-derive and refuse any drift
    tools/resolve_land_tracts.py --report  print what resolved, what refused, what it reached
    tools/resolve_land_tracts.py --self-test   the gate's assertions still fire when broken

THE HOLE THIS CLOSES. `data/research/land_sales/entries.json` holds 375 federal, canal
and school-section sales and a structured `tract` for each; `data/structures/` holds 372
buildings and a footprint for each. Nothing joined them, so the register could say who
entered the ground under Fort Dearborn and the walkthrough could not.

WHAT A `land_owner` BLOCK CLAIMS, AND THE THREE THINGS IT DOES NOT. It claims that the
tract the register describes, put on the ground by the construction below, contains this
structure's committed position — that is, THE PATENT FOR THIS GROUND WAS ENTERED BY THIS
MAN ON THIS DATE. It does NOT claim he still held the ground on the scene date (the
register records an entry, not a chain of title), it does NOT claim he lived there or
ever stood on it (the domain README's first discipline: a sale is not a resident), and
it does NOT claim the entry held — Beaubien's pre-emption over the Fort Dearborn
reservation is the one every reader will recognise, and it was litigated for years.

THE CONSTRUCTION, and it is a liberty (L219). The Public Land Survey grid is not traced
anywhere in this project. It is carried from ONE committed control point — `G1` in
`data/traces/gcp/wright_1834_gcps.json`, State & Madison, whose own note has said since
the datum work that it is the *PLSS section corner: sections 9/10/15/16, T39N R14E* — on
the plat's own east-west bearing, which Lake, Randolph and Washington agree on to the
sixth decimal, in nominal one-mile squares. Both the point and the bearing are inherited
from `tools/measure_no_build_ground.py` rather than re-argued, which is the same pair
L108 and L182 already build the reservation's boundary and Madison's line from.

WHAT THAT BUYS AND WHERE IT STOPS. A nominal mile is not a surveyed mile: a township's
north and west tiers absorb its closing error, and no second corner is held to measure
the drift against. So the grid is carried ONLY as far as the ground this project models
— the four sections that meet at G1 — and every tract outside them is recorded as read
and NOT put on the ground. Inside them the assignment is graded by its own margin: a
structure more than 40 m (twice the working horizontal uncertainty of anything traced
off the 1834 sheets) inside its tract is `inferred`, and one nearer a tract line than
that is `reconstructed`, with the margin printed on the row. An INVENTED roof — one a
recipe dealt to a lot — is `reconstructed` whatever its margin, because nothing on an
invented structure may outrank the invention that put it there.

THE TWO FRACTIONS ARE NOT GRID SQUARES, and are resolved from committed geometry
instead. The south-west fractional quarter of section 10 — Beaubien's 75.69 acres — is
the reservation ring `measure_no_build_ground.py` already derives and `check.sh` already
re-derives. The north fraction of section 10 — Robert A. Kinzie's 102.29 acres, which is
Kinzie's Addition — is that section clipped to the committed north bank of the main stem.

THE SCHOOL SECTION, AND WHAT ITS ROWS NOW SAY (T-0798). Every town-lot and block-only
row in this register is in **section 16**, the school section, sold at the October 1833
auction. Until T-0797 traced its plat those 336 rows were the largest silence here — read,
and not put on the ground, because a block number named ground this repo could not point
at. It can now: `data/traces/vectors/school_section_blocks_1834.json` carries all 142
blocks measured off J. S. Wright's 1834 survey, and each row is seated on the polygon its
own block number names.

  THE BLOCK, NOT THE LOT, and the distinction is the whole discipline of the placement.
  The sheet's ruled LOT lines are not traced, so a row that names lot 6 of block 48 is
  put on block 48 and its lot is carried as read and left unplaced. A block averages
  about a hectare and the auction sold most of them to several men apiece, so a roof
  standing inside one was not necessarily bought by any given purchaser of it. Block
  placements therefore reach NO structure, by rule and not by accident — `structures` is
  empty on every row of this kind, and `--self-test` holds it. Nothing here mints a
  person, a roof or a residence: the register's first discipline, that a sale is not a
  resident, is untouched.

  A NUMBER THE SHEET DOES NOT CARRY IS REFUSED, never nudged onto a neighbouring
  polygon. Today no row needs that refusal — all 136 blocks the sale names are on the
  sheet — and the two witnesses agree in the one place worth checking: Wright writes
  `Reserved` across blocks 1, 87, 88 and 142 and draws no numeral on them, and the
  auction, held a year earlier by a different hand, sells a lot in none of the four.

The other large silence is section 9's south-east quarter — the original town, where 254
of the 372 structures stand. The canal commissioners sold those lots, not the land
office, and the register does not hold them; that absence is the domain README's, not a
hole here.
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

DATA = ROOT / "data"
DOMAIN = DATA / "research" / "land_sales"
GROUND = DOMAIN / "ground.json"
STRUCTURES = DATA / "structures"
SCHOOL_BLOCKS = DATA / "traces" / "vectors" / "school_section_blocks_1834.json"
SOURCE_ID = "isa_public_domain_land_tract_sales"
GENERATED_BY = "tools/resolve_land_tracts.py --build"

MILE_M = 1609.344          # the nominal section side; a surveyed one is not held here
QUARTER_M = MILE_M / 2
HALF_QUARTER_E = MILE_M / 4
ACRE_M2 = 4046.8564224
SAFE_MARGIN_M = 40.0       # twice the working horizontal uncertainty (data/datum.json)

# NOTHING ON AN INVENTED STRUCTURE MAY OUTRANK THE INVENTION THAT PUT IT THERE — the
# standing rule `tools/audit_confidence.py` holds for every graded block in the corpus,
# and it bites hardest here. The tract is real and the register's description of it is
# read; what is invented is the ROOF STANDING ON IT, dealt to a lot by a recipe. So a
# claim about the ground under a roof that is not there cannot be graded above the roof,
# whatever margin it has, and 44 of the 63 drop for that reason rather than for geometry.
INVENTED_ID = re.compile(r"^(recon_|inf_)")
ENVELOPE_PAD_M = 200.0     # how far past the modelled ground the grid is still carried

SALE_TYPES = {"FD": "federal land sale (cash entry)",
              "SC": "school section sale",
              "CN": "canal land sale"}

# The four sections that meet at the one control point this project holds. The grid is
# not carried past them: see the module docstring.
REACH_SECTIONS = ("09", "10", "15", "16")


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def dump(p: Path, doc) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- the grid

def section_grid():
    """(to_grid, from_grid, bearing, corner). Local ENU <-> metres east/north of G1.

    The pair is inherited from measure_no_build_ground rather than re-argued, so the
    section grid, the reservation's west line and Madison's line cannot drift apart.
    """
    from measure_no_build_ground import plat_bearing, section_corner  # noqa: PLC0415
    slope = plat_bearing()
    ge, gn = section_corner()
    norm = math.hypot(1.0, slope)
    ux, uy = 1.0 / norm, slope / norm            # east along the plat
    vx, vy = -slope / norm, 1.0 / norm           # north along the plat

    def to_grid(x, y):
        dx, dy = x - ge, y - gn
        return (dx * ux + dy * uy, dx * vx + dy * vy)

    def from_grid(e, n):
        return (ge + e * ux + n * vx, gn + e * uy + n * vy)

    return to_grid, from_grid, slope, (ge, gn)


def section_cell(section: str) -> tuple[int, int]:
    """(column, row) of a section in its township, column 0 west, row 0 south.

    Sections are numbered boustrophedon from the north-east corner: 1-6 east to west
    across the north tier, 7-12 west to east across the next, and so on.
    """
    n = int(section)
    if not 1 <= n <= 36:
        raise SystemExit(f"section {section!r} is not 1-36")
    tier = (n - 1) // 6                       # 0 = north tier
    index = (n - 1) % 6
    column = index if tier % 2 else 5 - index
    return column, 5 - tier


def section_box(section: str) -> tuple[float, float, float, float]:
    """(east0, east1, north0, north1) of a T39N R14E section, in metres from G1.

    G1 is the corner of sections 9, 10, 15 and 16, which is the corner between columns
    2 and 3 and between rows 3 and 4 — so that corner is the grid's origin.
    """
    column, row = section_cell(section)
    return ((column - 3) * MILE_M, (column - 2) * MILE_M,
            (row - 4) * MILE_M, (row - 3) * MILE_M)


def aliquot_box(section: str, part: str):
    """The rectangle a `NE`, `E2NE` or `SENE` description names, or None.

    Only the shapes `read_land_sales.py` already resolves are read here; a description
    that tool leaves `unparsed` is left unparsed, never guessed at.
    """
    core = part
    for suffix in ("VOID", "VO", "FR"):
        if core.endswith(suffix):
            core = core[: -len(suffix)]
            break
    e0, e1, n0, n1 = section_box(section)

    def quarter(q, box):
        qe0, qe1, qn0, qn1 = box
        me, mn = (qe0 + qe1) / 2, (qn0 + qn1) / 2
        east = q[1] == "E"
        north = q[0] == "N"
        return (me if east else qe0, qe1 if east else me,
                mn if north else qn0, qn1 if north else mn)

    if len(core) == 2 and core[0] in "NS" and core[1] in "EW":
        return quarter(core, (e0, e1, n0, n1))
    if len(core) == 4 and core[0] in "NS" and core[1] in "EW":
        return quarter(core[:2], quarter(core[2:], (e0, e1, n0, n1)))
    if len(core) == 4 and core[1] == "2":
        box = quarter(core[2:], (e0, e1, n0, n1))
        be0, be1, bn0, bn1 = box
        half = core[0]
        if half == "E":
            return ((be0 + be1) / 2, be1, bn0, bn1)
        if half == "W":
            return (be0, (be0 + be1) / 2, bn0, bn1)
        if half == "N":
            return (be0, be1, (bn0 + bn1) / 2, bn1)
        if half == "S":
            return (be0, be1, bn0, (bn0 + bn1) / 2)
    return None


# ------------------------------------------------------- committed fractions

def committed_fractions(to_grid):
    """The two section-10 fractions, as rings in local ENU.

    Neither is a grid square. `sw_fractional_quarter` is the reservation ring
    measure_no_build_ground already derives from G1, Madison's line and the traced
    waterline (L108). `north_fraction` is section 10 clipped to the committed north
    bank of the main stem, which is what makes it Kinzie's Addition and not a quarter.
    """
    import measure_no_build_ground as nbg  # noqa: PLC0415

    ring, _madison, _section = nbg.reservation_ring()

    north_shore = None
    for feature in load(nbg.SHORELINE)["features"]:
        props = feature["properties"]
        if props.get("kind") == "shore" and props.get("name", "").startswith("North shore"):
            datum = load(DATA / "datum.json")
            north_shore = [(x - datum["origin_utm_e"], y - datum["origin_utm_n"])
                           for x, y in feature["geometry"]["coordinates"]]
    if north_shore is None:
        raise SystemExit("the shoreline no longer carries a 'North shore' line; the "
                         "north fraction of section 10 cannot be bounded")

    # THE WATER IS NOBODY'S TRACT. A structure standing on the river or the lake falls
    # inside a section like everything else, and a section is not what it stands on. The
    # committed water surface is the test; today it catches the south pier, whose record
    # sits out on the crib, and not the north pier, whose record sits at its landward
    # root on the bank.
    water = None
    for feature in load(nbg.SHORELINE)["features"]:
        if feature["properties"].get("kind") == "water":
            datum = load(DATA / "datum.json")
            water = [[(x - datum["origin_utm_e"], y - datum["origin_utm_n"])
                      for x, y in ring_coords]
                     for ring_coords in feature["geometry"]["coordinates"]]
    if water is None:
        raise SystemExit("the shoreline no longer carries a 'water' polygon")
    return ring, north_shore, water


def point_in_ring(p, ring) -> bool:
    x, y = p
    inside = False
    for i in range(len(ring)):
        (ax, ay), (bx, by) = ring[i], ring[(i + 1) % len(ring)]
        if (ay > y) != (by > y):
            t = (y - ay) / (by - ay)
            if x < ax + (bx - ax) * t:
                inside = not inside
    return inside


def ring_distance(p, ring) -> float:
    """Distance from a point to a ring's boundary."""
    x, y = p
    best = float("inf")
    for i in range(len(ring)):
        (ax, ay), (bx, by) = ring[i], ring[(i + 1) % len(ring)]
        dx, dy = bx - ax, by - ay
        span = dx * dx + dy * dy
        t = 0.0 if span == 0 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / span))
        best = min(best, math.hypot(x - (ax + dx * t), y - (ay + dy * t)))
    return best


def shore_north_of(p, line) -> tuple[bool, float] | tuple[None, None]:
    """(is the point north of this shore line, how far from it). (None, None) off its span."""
    x, y = p
    best = None
    for i in range(len(line) - 1):
        (ax, ay), (bx, by) = line[i], line[i + 1]
        if min(ax, bx) <= x <= max(ax, bx) and ax != bx:
            t = (x - ax) / (bx - ax)
            at = ay + (by - ay) * t
            if best is None or abs(y - at) < abs(y - best):
                best = at
    if best is None:
        return None, None
    return y > best, abs(y - best)


def ring_area_m2(ring) -> float:
    total = 0.0
    for i in range(len(ring)):
        (ax, ay), (bx, by) = ring[i], ring[(i + 1) % len(ring)]
        total += ax * by - bx * ay
    return abs(total) / 2


# ------------------------------------------------------------- the structures

def placed_structures():
    """[(id, path, record, local ENU position)] for every structure with a position."""
    datum = load(DATA / "datum.json")
    out = []
    for path in sorted(STRUCTURES.glob("*.json")):
        record = load(path)
        for phase in record["phases"]:
            pos = phase.get("position") or {}
            if pos.get("utm_e") is None:
                continue
            out.append((record["id"], path, record,
                        (pos["utm_e"] - datum["origin_utm_e"],
                         pos["utm_n"] - datum["origin_utm_n"])))
            break
    return out


def envelope(points, to_grid):
    xs, ys = [], []
    for _id, _p, _r, (x, y) in points:
        e, n = to_grid(x, y)
        xs.append(e)
        ys.append(n)
    return (min(xs) - ENVELOPE_PAD_M, max(xs) + ENVELOPE_PAD_M,
            min(ys) - ENVELOPE_PAD_M, max(ys) + ENVELOPE_PAD_M)


# ------------------------------------------------- the school section's own plat

# `LOT6BL48` is lot 6 of block 48; `BL106` is the block with no lot named; the register
# suffixes a cancelled sale VOID or VO. Nothing else in section 16 is a block reference,
# and a string this does not match is refused rather than coaxed into one.
SCHOOL_BLOCK = re.compile(r"^(?:LOT(\d+))?BL(\d+)(?:VOID|VO)?$")


def school_section_blocks():
    """block number -> the polygon T-0797 measured off Wright's 1834 survey.

    The trace is the one this project holds for section 16: 142 blocks, read off the
    sheet's own rules, with the two independent numeral readings of T-0797 and T-0875
    agreeing cell for cell. It is read here rather than re-derived, so a correction to
    the plat moves the sale rows with it.
    """
    doc = load(SCHOOL_BLOCKS)
    return {b["block_number"]: b for b in doc["blocks"]}, doc


# ------------------------------------------------------------------ the join

REFUSALS = {
    "off_the_modelled_ground":
        "Read, and not put on the ground. The section is not one of the four that meet "
        "at the only PLSS corner this project holds, so the nominal-mile grid would be "
        "carried past any ground this reconstruction models and past anything that "
        "could check it. No structure could stand on it either way.",
    "block_not_on_the_sheet":
        "Read, and not put on the ground. The row names a block of the SCHOOL SECTION "
        "that Wright's 1834 survey does not carry a numeral for, so the sale record and "
        "the sheet disagree about what that number names. The disagreement is written "
        "here and nothing is picked: putting the row on the nearest plausible polygon "
        "would be inventing the agreement the two witnesses do not have.",
    "description_not_read":
        "Read, and not put on the ground. `read_land_sales.py` leaves this legal "
        "description unparsed rather than guess at it, and guessing at it here would "
        "put the guess one layer further from the page that carries it.",
}


def resolve(entries, to_grid, from_grid, reach):
    """One row per sale: where it lands, or why it does not."""
    ring, north_shore, _water = committed_fractions(to_grid)
    plat, _plat_doc = school_section_blocks()
    e_lo, e_hi, n_lo, n_hi = reach
    rows = []
    for entry in entries:
        tract = entry["tract"]
        row = {
            "record_id": entry["record_id"],
            "purchaser_as_read": entry["purchaser_as_read"],
            "purchaser_normalized": entry["purchaser_normalized"],
            "date_purchased": entry["date_purchased"],
            "type_of_sale": entry["type_of_sale"],
            "acres_as_read": entry["acres"],
            "township": tract["township"], "range": tract["range"],
            "section": tract["section"], "part": tract["part"],
            "resolves": tract["resolves"], "void": tract["void"],
            "ground": None, "refusal": None, "note": None,
        }
        rows.append(row)

        if tract["township"] != "39N" or tract["range"] != "14E" \
                or tract["section"] not in REACH_SECTIONS:
            row["refusal"] = "off_the_modelled_ground"
            continue
        box = section_box(tract["section"])
        if box[1] < e_lo or box[0] > e_hi or box[3] < n_lo or box[2] > n_hi:
            row["refusal"] = "off_the_modelled_ground"
            continue

        # The two fractions of section 10 are not grid squares and are resolved from
        # committed geometry. Order matters: SWFR is tested before the aliquot grid
        # would hand back a full 160-acre quarter it is not.
        if tract["section"] == "10" and tract["part"].startswith("SWFR"):
            row["ground"] = {"kind": "committed_polygon",
                             "name": "the south-west fractional quarter of section 10",
                             "ring_local_enu": [[round(x, 3), round(y, 3)] for x, y in ring],
                             "acres_derived": round(ring_area_m2(ring) / ACRE_M2, 2)}
            row["note"] = (
                "THE UNITED STATES RESERVATION. This is the same tract L108 already "
                "derives for `1835_no_build_ground.json` — from G1, Madison's line and "
                "the traced waterline — so the polygon is inherited rather than built "
                "again, and `check.sh` already re-derives it. The register's own row is "
                "the second, independent witness to the date L108 quotes from Andreas: "
                "Beaubien's pre-emption, 28 May 1835, five weeks before the scene date. "
                "The derived polygon is short of the documented 75.69 acres for the "
                "reasons L108 states, and is a floor rather than the reservation. "
                "WHETHER THE ENTRY HELD IS NOT READ HERE: it was disputed, and this row "
                "records the entry the register carries and nothing about its outcome.")
            continue
        if tract["section"] == "10" and tract["part"].startswith("NFR"):
            row["ground"] = {"kind": "committed_clip",
                             "name": "the north fraction of section 10",
                             "section_box": [round(v, 3) for v in box],
                             "clipped_to": "north of the committed north bank of the main stem"}
            row["note"] = (
                "KINZIE'S ADDITION. The north fraction of section 10 is the section "
                "north of the river, which is why the register prints 102.29 acres and "
                "not a quarter's 160. It is resolved as the section's own grid box "
                "clipped to the committed north bank of the main stem "
                "(`e1834_harbor_cut/shoreline.geojson`), so no boundary here is "
                "authored. The two rows the register carries for it — one plain, one "
                "with the school-section marker — are the same entry printed twice.")
            continue

        if tract["section"] == "16" and SCHOOL_BLOCK.match(tract["part"]):
            m = SCHOOL_BLOCK.match(tract["part"])
            lot, number = m.group(1), int(m.group(2))
            block = plat.get(number)
            if block is None:
                row["refusal"] = "block_not_on_the_sheet"
                row["note"] = (f"The sale names block {number} of the school section and "
                               f"Wright's sheet numbers {len(plat)} blocks that do not "
                               f"include it.")
                continue
            row["ground"] = {
                "kind": "school_section_block",
                "name": (f"block {number} of the school section, section 16 T39N R14E"
                         + (f" (lot {lot} within it, not placed)" if lot else "")),
                "block_number": number,
                "block_id": block["id"],
                "lot_as_read": lot,
                "ring_local_enu": [[round(x, 3), round(y, 3)]
                                   for x, y in block["boundary_local_enu_m"]],
                "acres_derived": round(block["area_m2"] / ACRE_M2, 2),
                "numeral_on_the_sheet": block["numeral"]["on_sheet"],
                "geometry_confidence": block["geometry_confidence"],
                "trace": "data/traces/vectors/school_section_blocks_1834.json"}
            row["note"] = (
                "THE BLOCK, NOT THE LOT. The row is placed on the block polygon T-0797 "
                "measured off J. S. Wright's 1834 survey of the school section; the LOT "
                "inside it is carried as read and is NOT put on the ground, because the "
                "sheet's ruled lot lines are not traced. So this says the purchaser "
                "bought ground somewhere inside this block on this date, and it does not "
                "say where inside it. A block here averages a hectare and the auction "
                "sold most of them to several men, so nothing on it may be read as the "
                "owner of a particular roof — see `structures`, which is empty by rule "
                "for every row of this kind."
                + ("" if block["numeral"]["on_sheet"] else
                   " The sheet writes no numeral on this block and the serpentine "
                   "sequence supplies it: see the trace's own note."))
            continue

        box = aliquot_box(tract["section"], tract["part"])
        if box is None:
            row["refusal"] = "description_not_read"
            continue
        e0, e1, n0, n1 = box
        row["ground"] = {
            "kind": "aliquot_grid",
            "name": f"{tract['part']} of section {tract['section']}, T39N R14E",
            "box_local_enu": [round(v, 3) for v in box],
            "corners_local_enu": [[round(c, 3) for c in from_grid(e, n)]
                                  for e, n in ((e0, n0), (e1, n0), (e1, n1), (e0, n1))],
            "acres_derived": round((e1 - e0) * (n1 - n0) / ACRE_M2, 2)}
    return rows


def reach_structures(rows, structures, to_grid):
    """Which structure each resolved tract contains, and how safely."""
    ring, north_shore, water = committed_fractions(to_grid)

    def in_water(p):
        if not point_in_ring(p, water[0]):
            return False
        return not any(point_in_ring(p, hole) for hole in water[1:])

    assigned = {}
    for row in rows:
        row["structures"] = []
        if row["ground"] is None or row["void"]:
            continue
        for sid, _path, _record, (x, y) in structures:
            if in_water((x, y)):
                continue
            e, n = to_grid(x, y)
            kind = row["ground"]["kind"]
            # A BLOCK IS NOT A LOT. A school-section row lands on a block polygon and the
            # lot inside it is not traced, so a roof standing in that block was not
            # necessarily bought by this purchaser — the auction sold most blocks to
            # several men. Reaching a structure from one would claim exactly the thing
            # the placement refuses to claim, so it reaches none, by rule.
            if kind == "school_section_block":
                continue
            if kind == "aliquot_grid":
                e0, e1, n0, n1 = row["ground"]["box_local_enu"]
                if not (e0 <= e < e1 and n0 <= n < n1):
                    continue
                margin = min(e - e0, e1 - e, n - n0, n1 - n)
            elif kind == "committed_polygon":
                if not point_in_ring((x, y), ring):
                    continue
                margin = ring_distance((x, y), ring)
            else:
                e0, e1, n0, n1 = row["ground"]["section_box"]
                if not (e0 <= e < e1 and n0 <= n < n1):
                    continue
                north, gap = shore_north_of((x, y), north_shore)
                if north is not True:
                    continue
                margin = min(e - e0, e1 - e, n - n0, n1 - n, gap)
            row["structures"].append({"id": sid, "margin_m": round(margin, 1)})
            assigned.setdefault(sid, []).append((row, round(margin, 1)))
    return assigned


def school_section_counts(rows):
    """Who bought the south, counted off the rows that landed on the plat.

    THE FIRST HONEST STATEMENT OF IT this project can make: until T-0797 traced the
    blocks, every one of these rows read `Read, and not put on the ground`.
    """
    sixteen = [r for r in rows if r["section"] == "16" and r["township"] == "39N"
               and r["range"] == "14E"]
    placed = [r for r in sixteen if r["ground"]
              and r["ground"]["kind"] == "school_section_block"]
    by_block, by_buyer, dates = {}, {}, []
    named_a_lot = 0
    for row in placed:
        n = row["ground"]["block_number"]
        by_block.setdefault(n, []).append(row["record_id"])
        by_buyer.setdefault(row["purchaser_normalized"], set()).add(n)
        if row["ground"]["lot_as_read"]:
            named_a_lot += 1
        if row["date_purchased"]:
            dates.append(row["date_purchased"])
    plat, plat_doc = school_section_blocks()
    reserved = [n for n in plat_doc["summary"]["reserved"]]
    busiest = sorted(by_block.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
    keenest = sorted(by_buyer.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
    return {
        "rows_in_the_section": len(sixteen),
        "put_on_a_block": len(placed),
        "of_which_name_a_lot_inside_it": named_a_lot,
        "of_which_name_the_block_alone": len(placed) - named_a_lot,
        "refused": {key: sum(1 for r in sixteen if r["refusal"] == key)
                    for key in REFUSALS if any(r["refusal"] == key for r in sixteen)},
        "blocks_on_the_sheet": len(plat),
        "blocks_that_changed_hands": len(by_block),
        "blocks_never_sold": sorted(set(plat) - set(by_block)),
        "blocks_reserved_on_the_sheet": reserved,
        "reserved_blocks_the_sale_names": sorted(set(reserved) & set(by_block)),
        "first_sale": min(dates) if dates else None,
        "last_sale": max(dates) if dates else None,
        "distinct_purchasers": len(by_buyer),
        "busiest_blocks": [{"block": n, "rows": len(ids)} for n, ids in busiest],
        "keenest_purchasers": [{"purchaser": who, "blocks": len(bs)}
                               for who, bs in keenest],
    }


MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def plain_date(iso: str) -> str:
    try:
        y, m, d = iso.split("-")
        return f"{int(d)} {MONTHS[int(m) - 1]} {y}"
    except (ValueError, IndexError):
        return iso


STANDING_NOTE = (
    "WHAT THIS ROW CLAIMS AND WHAT IT DOES NOT. It claims that the tract the Illinois "
    "State Archives' land-sale register describes contains this structure's committed "
    "position — the patent for this ground was ENTERED by this man on this date. It "
    "does not claim he still held the ground on 1 July 1835, that he lived here, or "
    "that he ever stood on it: a sale is a transaction, and the register's only column "
    "about residence names a county. THE SECTION LINES ARE CONSTRUCTED, NOT TRACED "
    "(L219): the grid is carried from the single PLSS corner at State & Madison, on the "
    "plat's own east-west bearing, in nominal one-mile squares.")


def land_owner_block(structure_id, rows_for_structure) -> dict:
    """The `land_owner` block written onto one structure record."""
    invented = bool(INVENTED_ID.match(structure_id))
    rows = sorted(rows_for_structure, key=lambda pair: pair[0]["record_id"])
    primary, margin = rows[0]
    names = []
    for row, _m in rows:
        if row["purchaser_normalized"] not in names:
            names.append(row["purchaser_normalized"])
    who = names[0]
    value = f"The ground was entered by {who}, {plain_date(primary['date_purchased'])}"

    parts = [primary["note"]] if primary["note"] else []
    if len(names) > 1:
        parts.append("THE REGISTER SPELLS THE PURCHASER MORE THAN ONE WAY for this same "
                     "tract — " + "; ".join(names) + " — and the spellings are carried "
                     "rather than merged, which is the land_sales crosswalk's standing "
                     "rule: tract agreement is where two spellings MIGHT be one man and "
                     "is never proof that they are.")
    elif len(rows) > 1:
        parts.append(f"The register prints {len(rows)} rows for this tract; the earliest "
                     "is quoted and the rest are listed on the row.")
    if invented:
        parts.append(f"THE ROOF IS AN INVENTION AND THIS CANNOT OUTRANK IT. The "
                     f"footprint stands {margin:.0f} m inside the tract's nearest "
                     "boundary, which on a documented building would carry the middle "
                     "tier, but this building was dealt to its lot by a recipe and is "
                     "not there. The tract is real and the register's words about it "
                     "are read; what is graded here is the claim that THIS roof stands "
                     "on it, and that claim is the recipe's.")
    elif margin >= SAFE_MARGIN_M:
        parts.append(f"THE MARGIN IS {margin:.0f} m: this footprint stands that far "
                     "inside the tract's nearest boundary, which is more than twice the "
                     "working horizontal uncertainty of anything traced off the 1834 "
                     "sheets (about 20 m), so the assignment survives the error the "
                     "construction carries.")
    else:
        parts.append(f"THE MARGIN IS ONLY {margin:.0f} m, which is inside the working "
                     "horizontal uncertainty of the georeference (about 20 m) doubled, "
                     "so the grade drops a tier: the tract is right if the constructed "
                     "line is, and nothing here proves the line to better than that.")
    parts.append(STANDING_NOTE)

    return {
        "value": value,
        "confidence": ("reconstructed" if invented or margin < SAFE_MARGIN_M
                       else "inferred"),
        "sources": [SOURCE_ID],
        "note": " ".join(parts),
        "tract": primary["ground"]["name"],
        "entries": [row["record_id"] for row, _m in rows],
        "date_purchased": primary["date_purchased"],
        "type_of_sale": SALE_TYPES.get(primary["type_of_sale"], primary["type_of_sale"]),
        "margin_m": margin,
        "generated_by": GENERATED_BY,
    }


def derive():
    """(ground document, {structure id: land_owner block})."""
    entries = load(DOMAIN / "entries.json")["entries"]
    to_grid, from_grid, slope, corner = section_grid()
    structures = placed_structures()
    reach = envelope(structures, to_grid)
    rows = resolve(entries, to_grid, from_grid, reach)
    assigned = reach_structures(rows, structures, to_grid)

    blocks = {sid: land_owner_block(sid, pairs) for sid, pairs in sorted(assigned.items())}

    # Where the structures that got nothing are, so the silence is measured rather
    # than left as an absence a reader has to notice.
    unreached = {}
    for sid, _path, _record, (x, y) in structures:
        if sid in blocks:
            continue
        e, n = to_grid(x, y)
        where = None
        for section in REACH_SECTIONS:
            e0, e1, n0, n1 = section_box(section)
            if e0 <= e < e1 and n0 <= n < n1:
                where = section
                break
        unreached.setdefault(where or "outside the four sections", []).append(sid)

    resolved = [r for r in rows if r["ground"]]
    counts = {
        "entries": len(rows),
        "put_on_the_ground": len(resolved),
        "refused": {key: sum(1 for r in rows if r["refusal"] == key) for key in REFUSALS},
        "structures_placed": len(structures),
        "structures_reached": len(blocks),
        "structures_reached_by_grade": {
            grade: sum(1 for b in blocks.values() if b["confidence"] == grade)
            for grade in ("inferred", "reconstructed")},
        "structures_unreached_by_section": {k: len(v) for k, v in sorted(unreached.items())},
        "school_section": school_section_counts(rows),
    }

    doc = {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": GENERATED_BY,
        "ticket": "T-0609",
        "note": __doc__.split("\n\n", 1)[1].strip(),
        "construction": {
            "control_point": "G1, State & Madison — the PLSS corner of sections "
                             "9/10/15/16, T39N R14E (data/traces/gcp/wright_1834_gcps.json)",
            "control_point_local_enu": [round(corner[0], 3), round(corner[1], 3)],
            "control_point_residual_m": 13.9,
            "bearing_slope": slope,
            "section_side_m": MILE_M,
            "sections_carried": list(REACH_SECTIONS),
            "safe_margin_m": SAFE_MARGIN_M,
            "liberty": "L219",
        },
        "refusal_reasons": REFUSALS,
        "counts": counts,
        "tracts": rows,
        "structures_unreached_by_section": {k: sorted(v) for k, v in sorted(unreached.items())},
    }
    return doc, blocks


# ------------------------------------------------------------- build / check

def structure_paths():
    return {load(p)["id"]: p for p in sorted(STRUCTURES.glob("*.json"))}


def place_block(record: dict, want: dict) -> dict:
    """The record with `land_owner` seated after `occupants`, replacing any old one.

    The old block is DROPPED rather than copied through. Iterating a record that already
    carries `land_owner` and re-laying it at its own key would put the stale value back
    after the new one, and the write would silently do nothing — which is exactly what
    happened the first time this ran, and is why `--self-test` holds it below.
    """
    ordered = {}
    for key, value in record.items():
        if key == "land_owner":
            continue
        ordered[key] = value
        if key == "occupants":
            ordered["land_owner"] = want
    if "land_owner" not in ordered:
        ordered["land_owner"] = want
    return ordered


def write_blocks(blocks, dry_run=False):
    """Put `land_owner` on the records it reaches and take it off the ones it does not.

    Returns the list of (id, action) it did or would do. The block is generated, so a
    record that stops being reached must LOSE it — a stale owner is worse than none.
    """
    actions = []
    for sid, path in structure_paths().items():
        record = load(path)
        want = blocks.get(sid)
        have = record.get("land_owner")
        if want == have:
            continue
        if want is None:
            actions.append((sid, "remove"))
            if not dry_run:
                record.pop("land_owner")
                dump(path, record)
            continue
        actions.append((sid, "write" if have is None else "update"))
        if not dry_run:
            dump(path, place_block(record, want))
    return actions


def build():
    doc, blocks = derive()
    dump(GROUND, doc)
    actions = write_blocks(blocks)
    counts = doc["counts"]
    print(f"ground.json: {counts['put_on_the_ground']} of {counts['entries']} tracts on "
          f"the ground; {counts['structures_reached']} of {counts['structures_placed']} "
          f"structures reached; {len(actions)} record(s) changed")


def check():
    doc, blocks = derive()
    problems = []
    if not GROUND.exists():
        problems.append("data/research/land_sales/ground.json is missing")
    elif load(GROUND) != doc:
        problems.append("data/research/land_sales/ground.json has drifted from what "
                        "tools/resolve_land_tracts.py --build derives")
    for sid, action in write_blocks(blocks, dry_run=True):
        problems.append(f"{sid}: its land_owner block would be {action}d by --build")
    if problems:
        for p in problems:
            print("  " + p, file=sys.stderr)
        raise SystemExit("the land-tract join does not re-derive")
    print(f"the land-tract join re-derives: {doc['counts']['put_on_the_ground']} tracts "
          f"on the ground, {doc['counts']['structures_reached']} structures reached")


def report():
    doc, blocks = derive()
    counts = doc["counts"]
    print("TRACTS")
    print(f"  read                         {counts['entries']}")
    print(f"  put on the ground            {counts['put_on_the_ground']}")
    for key, n in counts["refused"].items():
        print(f"  refused: {key:<28} {n}")
    print("\nSTRUCTURES")
    print(f"  placed                       {counts['structures_placed']}")
    print(f"  reached by a tract           {counts['structures_reached']}")
    for grade, n in counts["structures_reached_by_grade"].items():
        print(f"    {grade:<26} {n}")
    print("  reached by nothing, by section:")
    for section, n in counts["structures_unreached_by_section"].items():
        print(f"    section {section:<20} {n}")
    ss = counts["school_section"]
    print("\nTHE SCHOOL SECTION — who bought the south at the auction of October 1833")
    print(f"  rows in section 16           {ss['rows_in_the_section']}")
    print(f"  put on a block               {ss['put_on_a_block']}")
    print(f"    naming a lot inside it     {ss['of_which_name_a_lot_inside_it']}")
    print(f"    naming the block alone     {ss['of_which_name_the_block_alone']}")
    for key, n in ss["refused"].items():
        print(f"  refused: {key:<28} {n}")
    print(f"  blocks on Wright's sheet     {ss['blocks_on_the_sheet']}")
    print(f"  blocks that changed hands    {ss['blocks_that_changed_hands']}")
    print(f"  blocks never sold            {', '.join(str(n) for n in ss['blocks_never_sold'])}")
    print(f"    of those, marked Reserved  {', '.join(str(n) for n in ss['blocks_reserved_on_the_sheet'])}")
    print(f"  distinct purchasers          {ss['distinct_purchasers']}")
    print(f"  the sale ran                 {ss['first_sale']} to {ss['last_sale']}")
    print("  the blocks that changed hands most:")
    for row in ss["busiest_blocks"]:
        print(f"    block {row['block']:<4} {row['rows']} row(s)")
    print("  the purchasers on the most blocks (as the register spelled them):")
    for row in ss["keenest_purchasers"]:
        print(f"    {row['purchaser']:<26} {row['blocks']} block(s)")

    print("\nTHE GROUND UNDER THE TOWN")
    by_tract = {}
    for sid, block in blocks.items():
        by_tract.setdefault((block["tract"], block["value"]), []).append(sid)
    for (tract, value), ids in sorted(by_tract.items()):
        print(f"  {value}")
        print(f"    {tract} — {len(ids)} structure(s), e.g. {', '.join(sorted(ids)[:3])}")


def self_test():
    """The gate's own assertions still fire when the thing they hold is broken."""
    checks = []

    # The section grid is boustrophedon and G1 is the 9/10/15/16 corner.
    assert section_cell("1") == (5, 5) and section_cell("6") == (0, 5)
    assert section_cell("7") == (0, 4) and section_cell("12") == (5, 4)
    box9, box10, box15, box16 = (section_box(s) for s in ("09", "10", "15", "16"))
    assert box9[1] == 0 and box9[2] == 0, "section 9's SE corner is not G1"
    assert box10[0] == 0 and box10[2] == 0, "section 10's SW corner is not G1"
    assert box15[0] == 0 and box15[3] == 0, "section 15's NW corner is not G1"
    assert box16[1] == 0 and box16[3] == 0, "section 16's NE corner is not G1"
    checks.append("the four sections meet at G1")

    # An aliquot description resolves to the rectangle it names, and no other.
    e0, e1, n0, n1 = aliquot_box("09", "E2NE")
    assert (e0, e1, n0, n1) == (-QUARTER_M / 2, 0.0, QUARTER_M, MILE_M), (e0, e1, n0, n1)
    assert aliquot_box("09", "W2NE")[1] == -QUARTER_M / 2
    assert aliquot_box("09", "SENE") is not None
    assert aliquot_box("16", "BL27") is None, "a block number is not an aliquot"
    assert aliquot_box("16", "LOT6BL48") is None, "a town lot is not an aliquot"
    checks.append("aliquot descriptions resolve, and only aliquot descriptions")

    # Acreage falls out of the construction at the register's own figures.
    quarter = aliquot_box("09", "NE")
    acres = (quarter[1] - quarter[0]) * (quarter[3] - quarter[2]) / ACRE_M2
    assert abs(acres - 160) < 1, acres
    half = aliquot_box("09", "E2NE")
    acres = (half[1] - half[0]) * (half[3] - half[2]) / ACRE_M2
    assert abs(acres - 80) < 1, acres
    checks.append("a quarter measures 160 acres and a half-quarter 80")

    # A void row confers nothing.
    doc, blocks = derive()
    voided = {r["record_id"] for r in doc["tracts"] if r["void"]}
    for block in blocks.values():
        assert not (set(block["entries"]) & voided), block["entries"]
    checks.append("no void entry reaches a structure")

    # A record that already carries a block takes the NEW one, not its own old one.
    seated = place_block({"id": "x", "occupants": {}, "land_owner": {"value": "old"},
                          "research_note": ""}, {"value": "new"})
    assert seated["land_owner"] == {"value": "new"}, seated["land_owner"]
    assert list(seated) == ["id", "occupants", "land_owner", "research_note"], list(seated)
    assert place_block({"id": "x"}, {"value": "new"})["land_owner"] == {"value": "new"}
    checks.append("a rewritten block replaces the old one instead of being replaced by it")

    # Every refusal names a reason the document explains.
    for row in doc["tracts"]:
        assert (row["ground"] is None) != (row["refusal"] is None), row["record_id"]
        if row["refusal"]:
            assert row["refusal"] in doc["refusal_reasons"], row["refusal"]
    checks.append("every row either lands or says why it does not")

    # Section 16 is the school section, and since T-0797 traced its plat every row of it
    # either lands on a block or says why not. T-0675 walked the section to its end and
    # 337 rows came back rather than the ceiling's 150, one of which reads its lot as
    # `06126` — unparsed, and refused as that rather than as the plat.
    sixteen = [r for r in doc["tracts"] if r["section"] == "16" and r["township"] == "39N"]
    assert sixteen and len(sixteen) == 337, len(sixteen)
    landed = [r for r in sixteen if r["ground"]]
    assert all(r["ground"]["kind"] == "school_section_block" for r in landed)
    assert all(r["refusal"] in {"block_not_on_the_sheet", "description_not_read"}
               for r in sixteen if not r["ground"])
    checks.append(f"{len(landed)} of {len(sixteen)} school-section rows land on a block "
                  "of Wright's plat, and the rest say why they do not")

    # A block placement is a block and not a lot: it reaches no roof, ever.
    assert all(not r["structures"] for r in landed), "a block placement reached a roof"
    checks.append("no school-section block placement claims the ground under a roof")

    # The two witnesses to the reservation agree. Wright writes `Reserved` across four
    # blocks and draws no numeral on them; the auction, held a year earlier by a
    # different hand, sells lots in 136 blocks and in none of those four. Neither
    # reading was made from the other.
    ss = doc["counts"]["school_section"]
    assert ss["blocks_reserved_on_the_sheet"] == [1, 87, 88, 142], ss
    assert ss["reserved_blocks_the_sale_names"] == [], ss
    assert set(ss["blocks_reserved_on_the_sheet"]) <= set(ss["blocks_never_sold"])
    checks.append("the sale sells no lot in any of the four blocks the sheet reserves")

    # A block number the sheet does not carry is refused rather than nudged onto a
    # neighbour. Today there are none, so the assertion is held over a forged row.
    plat, _ = school_section_blocks()
    assert 999 not in plat and SCHOOL_BLOCK.match("LOT4BL999")
    assert SCHOOL_BLOCK.match("BL106").group(1) is None
    assert SCHOOL_BLOCK.match("LOT3BL4VOID").groups() == ("3", "4")
    assert SCHOOL_BLOCK.match("06126") is None
    checks.append("a bare block, a lot-and-block, a voided row and an unread "
                  "description are each read as what they are")

    for line in checks:
        print("  ok  " + line)
    print(f"{len(checks)} assertion group(s) still fire")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.build:
        build()
    elif args.check:
        check()
    elif args.report:
        report()
    elif args.self_test:
        self_test()
    else:
        parser.error("one of --build, --check, --report, --self-test")


if __name__ == "__main__":
    main()
