#!/usr/bin/env python3
"""The land tract sales, put on the ground, and joined to the structures they reach (T-0609).

    tools/resolve_land_tracts.py --build       derive tracts.json, the join, and the
                                               land_owner block on every structure reached
    tools/resolve_land_tracts.py --check       the gate: re-derive and refuse any drift
    tools/resolve_land_tracts.py --self-test   the gate's assertions still fire when broken

WHAT THIS JOINS, AND WHY THE JOIN DID NOT EXIST. `data/research/land_sales/` holds 375
federal, canal and school-section sales in T39N R14E and T40N R14E, each naming a
purchaser and an aliquot part of a section. `data/structures/` holds 372 buildings, each
carrying a position in UTM metres. Nothing joined the two: the register said who bought
the ground and the dataset said what stands on it, and no file said whose ground a
building stands on. This resolves each tract to a rectangle on this project's own frame
and asks, of every structure, which rectangle contains it.

THE GRID IS A CONSTRUCTION AND NOT A SURVEY, and that is the one thing to know before
reading any number below. This project holds exactly ONE PLSS control point — `G1` in
`data/traces/gcp/wright_1834_gcps.json`, State & Madison, the corner of sections
9/10/15/16 of T39N R14E — and no section-line trace at all. So the grid here is that
corner, carried on the plat's own east-west bearing (the slope Lake, Randolph and
Washington agree on to the sixth decimal) at the nominal section mile of 5280 US survey
feet. It is the same construction `L108` already declared for the United States
Reservation's west and south lines and `L109` for Madison's centreline, extended from two
lines to the whole grid, and it is graded `inferred` for the same reasons: G1 carries a
13.9 m residual, anything read off the 1834 sheets carries about 20 m, and a real township
is not nominal — its sections close on their own corners, not on six exact miles.

WHAT IS REFUSED, AND IT IS MOST OF THE REGISTER. A rectangle can only be computed for a
REGULAR aliquot. Three classes get none:

  * FRACTIONAL parts (`NFR`, `SWFR`, `NWFRPTNW`, `E2NEFR` …) are bounded by a meander
    line — the lake shore, the river, an Indian boundary — and not by the grid. Their
    true outline is on a plat this project has not read, and the nominal rectangle is not
    it. Nothing is drawn for them. That refusal costs this join the two tracts a reader
    would most want: the southwest fractional quarter of section 10, which is the Fort
    Dearborn reservation John Baptist Beaubien pre-empted on 1835-05-28, and the north
    fraction of the same section, entered by Robert A. Kinzie in 1831.
  * TOWN LOTS and whole BLOCKS in the school section (`LOT7BL48`, `BL27`) are lots on the
    canal commissioners' 1833 plat of section 16. Placing them needs that plat, which is
    a different reading and a different ticket.
  * VOIDED entries carry the tract's rectangle like any other, but confer no owner: a
    voided sale is a sale that did not stand, and the register keeps the row.

AND A PURCHASE IS NOT A TITLE. `land_owner` on a structure names the person who entered
that tract FROM THE UNITED STATES, on the date the register gives. It does not say the
ground had not been sold on since — most of the sales this join lands on are from 1830,
five years before the scene date, in a town whose whole business in 1835 was selling land
again. The block says so in its own note, carries `inferred`, and cites the register.
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
DOMAIN = DATA / "research" / "land_sales"
STRUCTURES = DATA / "structures"
SOURCE_ID = "isa_public_domain_land_tract_sales"
GCP_PATH = DATA / "traces" / "gcp" / "wright_1834_gcps.json"
STREETS_PATH = DATA / "streets" / "1835.json"

# 5280 US survey feet, the nominal section mile the rectangular survey was run at.
# The US survey foot is 1200/3937 m exactly; the definition is what is carried here
# rather than a rounded metre figure, because the grid is six of these long.
SECTION_MILE_M = 5280.0 * 1200.0 / 3937.0

# The three east-west streets of the plat whose committed centrelines fix its bearing.
# Named here rather than imported so this tool states its own inputs; the assertion that
# they agree is `measure_no_build_ground.plat_bearing`'s and is repeated below.
BEARING_STREETS = ("lake", "randolph", "washington")

# G1 is the corner of sections 9, 10, 15 and 16 — so it stands on the east line of the
# third column of sections and the south line of the second row. Everything else in the
# township is stepped off that.
G1_SECTIONS = (9, 10, 15, 16)
G1_TOWNSHIP, G1_RANGE = "39N", "14E"

REGULAR_QUARTER = ("NE", "NW", "SE", "SW")
HALF = ("E2", "W2", "N2", "S2")


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def dump(p: Path, doc) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# the frame


def plat_bearing() -> float:
    """The plat's east-west slope in local ENU, read off the committed centrelines.

    The same three streets and the same assertion as `measure_no_build_ground`: a grid
    whose own streets disagree is a finding, not a number to average away.
    """
    slopes = []
    for street in load(STREETS_PATH)["streets"]:
        if street["id"] not in BEARING_STREETS:
            continue
        path = street["path_local_enu_m"]
        (ax, ay), (bx, by) = path[0], path[-1]
        slopes.append(round((by - ay) / (bx - ax), 6))
    if len(slopes) != len(BEARING_STREETS):
        raise SystemExit("the plat bearing needs Lake, Randolph and Washington")
    if len(set(slopes)) != 1:
        raise SystemExit("the plat's own east-west streets disagree on bearing: %s" % slopes)
    return slopes[0]


def control_point() -> tuple[float, float]:
    """G1 — State & Madison — in local ENU metres, with its identity asserted."""
    datum = load(DATA / "datum.json")
    points = load(GCP_PATH)
    points = points.get("points") or points.get("gcps")
    g1 = next((p for p in points if p["id"] == "G1"), None)
    if g1 is None:
        raise SystemExit("wright_1834_gcps.json no longer carries G1")
    if "Madison" not in g1["map_feature"]:
        raise SystemExit("G1 is no longer State & Madison but %r" % g1["map_feature"])
    if "9/10/15/16" not in g1["feature_note"]:
        raise SystemExit("G1's note no longer calls it the corner of sections 9/10/15/16, "
                         "and this whole grid is stepped off that identity")
    return (g1["modern"]["utm_e"] - datum["origin_utm_e"],
            g1["modern"]["utm_n"] - datum["origin_utm_n"])


def section_cell(section: int) -> tuple[int, int]:
    """A section number to its (column from the west, row from the north), both 1..6.

    The rectangular survey numbers a township boustrophedon — 1 at the northeast corner,
    west along the first tier, then east along the second. So an odd tier runs east-west
    and an even tier west-east, and that single alternation is the whole rule.
    """
    if not 1 <= section <= 36:
        raise ValueError("section %d is not in a township" % section)
    row = (section - 1) // 6 + 1
    k = section - 6 * (row - 1)
    col = (7 - k) if row % 2 == 1 else k
    return col, row


def township_origin(township: str, rng: str, g1: tuple[float, float]) -> tuple[float, float] | None:
    """The southwest corner of a township, in (east, north) MILES from G1 on the frame.

    G1 stands at column 3's east line and row 2's south line of T39N R14E, so that
    township's southwest corner is three miles west and four miles south of it. T40N R14E
    is the township directly north: six miles up the same range line. No other township
    is stepped off, because nothing here holds a control point in one.
    """
    if rng != G1_RANGE:
        return None
    col, row = section_cell(G1_SECTIONS[0])          # section 9 -> column 3, row 2
    east_miles = -float(col)                          # G1 is on that column's EAST line
    north_miles = -float(6 - row)                     # and on that row's SOUTH line
    if township == "39N":
        return east_miles, north_miles
    if township == "40N":
        return east_miles, north_miles + 6.0
    return None


def aliquot_box(part: str) -> tuple[float, float, float, float] | None:
    """A regular aliquot to its box inside a section, in fractions of a section.

    Returned as (u0, v0, u1, v1) from the section's southwest corner, u east, v north.
    Only REGULAR parts resolve. Anything carrying FR (fractional) or VO/VOID here is
    refused by the caller before this is reached.
    """
    if part in REGULAR_QUARTER:
        u0 = 0.5 if part.endswith("E") else 0.0
        v0 = 0.5 if part.startswith("N") else 0.0
        return u0, v0, u0 + 0.5, v0 + 0.5
    m = re.fullmatch(r"(E2|W2|N2|S2)(NE|NW|SE|SW)", part)
    if m:
        half, quarter = m.groups()
        qu0 = 0.5 if quarter.endswith("E") else 0.0
        qv0 = 0.5 if quarter.startswith("N") else 0.0
        if half == "E2":
            return qu0 + 0.25, qv0, qu0 + 0.5, qv0 + 0.5
        if half == "W2":
            return qu0, qv0, qu0 + 0.25, qv0 + 0.5
        if half == "N2":
            return qu0, qv0 + 0.25, qu0 + 0.5, qv0 + 0.5
        return qu0, qv0, qu0 + 0.5, qv0 + 0.25
    m = re.fullmatch(r"(NE|NW|SE|SW)(NE|NW|SE|SW)", part)
    if m:
        inner, quarter = m.groups()
        qu0 = 0.5 if quarter.endswith("E") else 0.0
        qv0 = 0.5 if quarter.startswith("N") else 0.0
        u0 = qu0 + (0.25 if inner.endswith("E") else 0.0)
        v0 = qv0 + (0.25 if inner.startswith("N") else 0.0)
        return u0, v0, u0 + 0.25, v0 + 0.25
    return None


class Frame:
    """The constructed PLSS grid, and the two conversions every number here goes through."""

    def __init__(self) -> None:
        self.slope = plat_bearing()
        self.g1 = control_point()
        theta = math.atan(self.slope)
        self.ux, self.uy = math.cos(theta), math.sin(theta)
        self.vx, self.vy = -math.sin(theta), math.cos(theta)

    def to_miles(self, e: float, n: float) -> tuple[float, float]:
        """Local ENU metres to (east, north) miles from G1 along the plat's own axes."""
        de, dn = e - self.g1[0], n - self.g1[1]
        return ((de * self.ux + dn * self.uy) / SECTION_MILE_M,
                (de * self.vx + dn * self.vy) / SECTION_MILE_M)

    def to_enu(self, u: float, v: float) -> tuple[float, float]:
        um, vm = u * SECTION_MILE_M, v * SECTION_MILE_M
        return (round(self.g1[0] + um * self.ux + vm * self.vx, 3),
                round(self.g1[1] + um * self.uy + vm * self.vy, 3))


# --------------------------------------------------------------------------
# the resolution


def refusal_for(part: str, resolves: str) -> str | None:
    """Why this tract gets no rectangle, or None if it gets one."""
    if resolves == "town_lot" or re.fullmatch(r"BL\d+", part):
        return ("a lot or a block on the canal commissioners' 1833 plat of the school "
                "section, which this project has not read; the section's rectangle is "
                "known and the lot's place inside it is not")
    if "FR" in part:
        return ("a fractional part, bounded by a meander line — the lake shore, the river "
                "or the Indian boundary — and not by the grid; the nominal rectangle is "
                "not its outline and drawing it would be an invention")
    if part.endswith("VOID") or part.endswith("VO"):
        return ("the register's own VOID mark rides in the aliquot column, so the part "
                "cannot be read cleanly; the sale it voids is carried by its twin row")
    if aliquot_box(part) is None:
        return "the aliquot column does not parse to a regular part of a section"
    return None


def tract_key(entry: dict) -> str:
    t = entry["tract"]
    return "T%s R%s sec %s %s" % (t["township"], t["range"], t["section"], t["part"])


def resolve_tracts(frame: Frame, entries: list) -> tuple[list, list]:
    """Every distinct tract in the register, resolved to a rectangle or refused."""
    seen: dict[str, dict] = {}
    for e in entries:
        t = e["tract"]
        key = tract_key(e)
        rec = seen.get(key)
        if rec is None:
            rec = seen[key] = {
                "tract": key,
                "township": t["township"], "range": t["range"],
                "section": t["section"], "part": t["part"],
                "resolves": t["resolves"],
                "geometry": None, "refusal": None,
                "sales": [],
            }
        rec["sales"].append({
            "record_id": e["record_id"],
            "purchaser_as_read": e["purchaser_as_read"],
            "purchaser_normalized": e["purchaser_normalized"],
            "date_purchased": e["date_purchased"],
            "type_of_sale": e["type_of_sale"],
            "acres": e["acres"],
            "void": bool(t.get("void")),
        })

    resolved, refused = [], []
    for key in sorted(seen):
        rec = seen[key]
        why = refusal_for(rec["part"], rec["resolves"])
        origin = township_origin(rec["township"], rec["range"], frame.g1)
        if why is None and origin is None:
            why = ("no control point stands in T%s R%s, so this grid cannot be stepped "
                   "into it from G1" % (rec["township"], rec["range"]))
        if why is not None:
            rec["refusal"] = why
            rec.pop("geometry")
            refused.append(rec)
            continue
        col, row = section_cell(int(rec["section"]))
        su = origin[0] + (col - 1)
        sv = origin[1] + (6 - row)
        u0, v0, u1, v1 = aliquot_box(rec["part"])
        box = [(su + u0, sv + v0), (su + u1, sv + v0), (su + u1, sv + v1), (su + u0, sv + v1)]
        ring = [list(frame.to_enu(u, v)) for u, v in box]
        rec["geometry"] = {
            "kind": "rectangle",
            "confidence": "inferred",
            "local_enu_m": ring + [ring[0]],
            "miles_from_g1": {"east": [round(su + u0, 6), round(su + u1, 6)],
                              "north": [round(sv + v0, 6), round(sv + v1, 6)]},
            "acres_nominal": round((u1 - u0) * (v1 - v0) * 640.0, 2),
        }
        rec.pop("refusal")
        resolved.append(rec)
    return resolved, refused


def structure_positions() -> list:
    """Every structure's earliest positioned phase, in local ENU metres."""
    datum = load(DATA / "datum.json")
    oe, on = datum["origin_utm_e"], datum["origin_utm_n"]
    out = []
    for path in sorted(STRUCTURES.glob("*.json")):
        rec = load(path)
        for phase in rec["phases"]:
            pos = phase.get("position") or {}
            if pos.get("utm_e") is None or pos.get("utm_n") is None:
                continue
            out.append({"id": rec["id"], "path": path, "phase": phase["id"],
                        "e": pos["utm_e"] - oe, "n": pos["utm_n"] - on})
            break
    return out


def join(frame: Frame, resolved: list, structures: list) -> dict:
    """Which resolved tract contains each structure's position."""
    boxes = []
    for rec in resolved:
        mf = rec["geometry"]["miles_from_g1"]
        boxes.append((mf["east"][0], mf["north"][0], mf["east"][1], mf["north"][1], rec))
    rows = []
    for s in structures:
        u, v = frame.to_miles(s["e"], s["n"])
        hit = None
        for u0, v0, u1, v1, rec in boxes:
            if u0 <= u < u1 and v0 <= v < v1:
                hit = rec
                break
        row = {"structure_id": s["id"], "phase_id": s["phase"],
               "miles_from_g1": {"east": round(u, 6), "north": round(v, 6)},
               "tract": hit["tract"] if hit else None}
        if hit:
            row["purchasers"] = [
                {"name": x["purchaser_normalized"], "as_read": x["purchaser_as_read"],
                 "record_id": x["record_id"], "date_purchased": x["date_purchased"],
                 "type_of_sale": x["type_of_sale"]}
                for x in sorted(hit["sales"], key=lambda x: x["record_id"]) if not x["void"]]
            if not row["purchasers"]:
                row["tract"] = None
                row.pop("purchasers")
                row["note"] = "every sale of this tract in the register is voided"
        rows.append(row)
    return {"rows": rows,
            "reached": sum(1 for r in rows if r.get("tract")),
            "unreached": sum(1 for r in rows if not r.get("tract"))}


LAND_OWNER_NOTE = (
    "DERIVED, and re-derived by tools/resolve_land_tracts.py --check: this block is not "
    "hand-authored and a hand-edit fails the gate. This structure's committed position "
    "falls inside {tract} on the PLSS grid this project constructs from its ONE control "
    "point — G1, State & Madison, the corner of sections 9/10/15/16 — carried on the "
    "plat's own east-west bearing at the nominal section mile. The grid is a "
    "construction and not a survey (L218), G1 carries a 13.9 m residual and the position "
    "itself carries the record's own uncertainty, so a structure near a section line may "
    "be on the other side of it. AND A PURCHASE IS NOT A TITLE: {who} entered this tract "
    "from the United States on {when}, which is what the register records and all it "
    "records. It does not say who held the ground on 1 July 1835, in a town whose whole "
    "business that year was selling it again."
)


def land_owner_block(row: dict) -> dict:
    who = " and ".join(p["name"] for p in row["purchasers"])
    when = " and ".join(sorted({p["date_purchased"] for p in row["purchasers"]}))
    return {
        "tract": row["tract"],
        "purchasers": row["purchasers"],
        "confidence": "inferred",
        "sources": [SOURCE_ID],
        "note": LAND_OWNER_NOTE.format(tract=row["tract"], who=who, when=when),
    }


def structure_docs(joined: dict) -> dict:
    """Every structure file whose land_owner block this derivation decides, path -> doc."""
    by_id = {r["structure_id"]: r for r in joined["rows"] if r.get("tract")}
    out = {}
    for path in sorted(STRUCTURES.glob("*.json")):
        rec = load(path)
        row = by_id.get(rec["id"])
        want = land_owner_block(row) if row else None
        if want is None and "land_owner" not in rec:
            continue
        rec.pop("land_owner", None)
        if want is not None:
            keys = list(rec)
            rec["land_owner"] = want
            if "phases" in keys:                      # keep the prose block above the phases
                rec = {k: (want if k == "land_owner" else rec[k])
                       for k in (keys[:keys.index("phases")] + ["land_owner"]
                                 + keys[keys.index("phases"):])}
        out[path] = rec
    return out


def derive() -> tuple[dict, dict]:
    frame = Frame()
    entries = load(DOMAIN / "entries.json")["entries"]
    resolved, refused = resolve_tracts(frame, entries)
    structures = structure_positions()
    joined = join(frame, resolved, structures)
    tracts = {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/resolve_land_tracts.py --build",
        "note": ("Every distinct tract in the register, resolved to a rectangle on this "
                 "project's constructed PLSS grid or refused with the reason. The grid is "
                 "one control point and a bearing, not a survey; see the module docstring "
                 "and L218. Coordinates are local ENU metres from data/datum.json."),
        "frame": {
            "control_point": "G1 (State & Madison), data/traces/gcp/wright_1834_gcps.json",
            "control_point_local_enu_m": [round(frame.g1[0], 3), round(frame.g1[1], 3)],
            "control_point_is": "the corner of sections 9, 10, 15 and 16, T39N R14E",
            "bearing_slope": frame.slope,
            "bearing_from": "the committed centrelines of Lake, Randolph and Washington",
            "section_mile_m": round(SECTION_MILE_M, 4),
            "townships_stepped": ["T39N R14E", "T40N R14E"],
            "confidence": "inferred",
        },
        "counts": {"tracts": len(resolved) + len(refused),
                   "resolved": len(resolved), "refused": len(refused),
                   "sales": len(entries)},
        "resolved": resolved,
        "refused": refused,
    }
    join_doc = {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/resolve_land_tracts.py --build",
        "note": ("Which resolved tract each structure's committed position falls in. A row "
                 "with no tract stands on ground the register either did not sell as a "
                 "regular aliquot or sold in a form this pass refuses to draw — which is "
                 "most of the town, because the plat itself is fractional section 9 and "
                 "the school section's lots are unplaced."),
        "counts": {"structures": len(structures),
                   "reached": joined["reached"], "unreached": joined["unreached"]},
        "rows": joined["rows"],
    }
    return ({"tracts.json": tracts, "structure_tracts.json": join_doc},
            structure_docs(joined))


def build(quiet: bool = False) -> int:
    domain_docs, struct_docs = derive()
    for rel, doc in domain_docs.items():
        dump(DOMAIN / rel, doc)
    for path, doc in struct_docs.items():
        dump(path, doc)
    if not quiet:
        c = domain_docs["tracts.json"]["counts"]
        j = domain_docs["structure_tracts.json"]["counts"]
        print("land tracts: %d tracts, %d resolved, %d refused; %d of %d structures reached"
              % (c["tracts"], c["resolved"], c["refused"], j["reached"], j["structures"]))
    return 0


def check(quiet: bool = False) -> list:
    bad = []
    domain_docs, struct_docs = derive()
    for rel, doc in domain_docs.items():
        path = DOMAIN / rel
        if not path.exists():
            bad.append("land tracts: %s is not committed — run --build" % rel)
        elif load(path) != doc:
            bad.append("land tracts: %s has drifted — it is generated by "
                       "tools/resolve_land_tracts.py --build and must not be hand-edited" % rel)
    for path, doc in struct_docs.items():
        if load(path) != doc:
            bad.append("land tracts: %s carries a land_owner block that is not the one this "
                       "join derives — the block is generated, not authored" % path.name)
    for path in sorted(STRUCTURES.glob("*.json")):
        if path in struct_docs:
            continue
        if "land_owner" in load(path):
            bad.append("land tracts: %s carries a land_owner block and no tract reaches it"
                       % path.name)
    if not bad and not quiet:
        c = domain_docs["tracts.json"]["counts"]
        j = domain_docs["structure_tracts.json"]["counts"]
        print("land tracts: %d tracts re-resolved, %d structures reached, no drift"
              % (c["tracts"], j["reached"]))
    return bad


# --------------------------------------------------------------------------


def self_test() -> int:
    fired = []

    if section_cell(1) != (6, 1):
        print("SELF-TEST: section 1 is the northeast corner of a township"); return 1
    fired.append("section 1 sits at the township's northeast corner")
    if section_cell(9) != (3, 2) or section_cell(10) != (4, 2):
        print("SELF-TEST: sections 9 and 10 must straddle G1's column line"); return 1
    if section_cell(16) != (3, 3) or section_cell(15) != (4, 3):
        print("SELF-TEST: sections 15 and 16 must lie south of 9 and 10"); return 1
    fired.append("sections 9/10/15/16 close on one corner, which is what G1 is")
    if section_cell(31) != (1, 6) or section_cell(36) != (6, 6):
        print("SELF-TEST: the sixth tier runs 31 west to 36 east"); return 1
    fired.append("the boustrophedon alternates tier by tier")

    if aliquot_box("E2NE") != (0.75, 0.5, 1.0, 1.0):
        print("SELF-TEST: E2NE is the east half of the northeast quarter"); return 1
    if aliquot_box("W2SW") != (0.0, 0.0, 0.25, 0.5):
        print("SELF-TEST: W2SW is the west half of the southwest quarter"); return 1
    if aliquot_box("NESW") != (0.25, 0.25, 0.5, 0.5):
        print("SELF-TEST: NESW is the northeast quarter of the southwest quarter"); return 1
    fired.append("a regular aliquot resolves to its own quarter of the section")

    for part, resolves, word in (("E2NEFR", "half_quarter_section", "fractional"),
                                 ("LOT7BL48", "town_lot", "canal commissioners"),
                                 ("BL27", "unparsed", "canal commissioners"),
                                 ("E2NEVOID", "half_quarter_section", "VOID"),
                                 ("ADDFRSEC", "unparsed", "fractional")):
        why = refusal_for(part, resolves)
        if not why or word not in why:
            print("SELF-TEST: %s must be refused for being %s" % (part, word)); return 1
    fired.append("fractional parts, town lots, whole blocks and voided rows are refused")
    if refusal_for("E2NE", "half_quarter_section") is not None:
        print("SELF-TEST: a regular aliquot must not be refused"); return 1
    fired.append("a regular aliquot is not refused")

    frame = Frame()
    a = frame.to_enu(0.0, 0.0)
    if abs(a[0] - frame.g1[0]) > 1e-6 or abs(a[1] - frame.g1[1]) > 1e-6:
        print("SELF-TEST: the frame's origin must be G1 itself"); return 1
    east = frame.to_enu(1.0, 0.0)
    d = math.hypot(east[0] - a[0], east[1] - a[1])
    if abs(d - SECTION_MILE_M) > 1e-3:
        print("SELF-TEST: one mile east must be one section mile long, got %.3f" % d); return 1
    fired.append("the frame is orthonormal at the section mile, anchored on G1")
    u, v = frame.to_miles(*frame.to_enu(-0.375, 0.75))
    if abs(u + 0.375) > 1e-6 or abs(v - 0.75) > 1e-6:   # to_enu rounds to the mm
        print("SELF-TEST: the two conversions must invert each other"); return 1
    fired.append("metres and miles convert back to each other")

    o39 = township_origin("39N", "14E", frame.g1)
    o40 = township_origin("40N", "14E", frame.g1)
    if o39 != (-3.0, -4.0):
        print("SELF-TEST: T39N R14E's southwest corner is 3 miles west, 4 south of G1"); return 1
    if o40 != (-3.0, 2.0):
        print("SELF-TEST: T40N R14E stands six miles north of T39N"); return 1
    if township_origin("39N", "13E", frame.g1) is not None:
        print("SELF-TEST: no township outside R14E may be stepped into"); return 1
    fired.append("only the two townships a control point can reach are stepped")

    bad = check(quiet=True)
    if bad:
        print("SELF-TEST: the committed derivation is already drifted: %s" % bad[0]); return 1
    fired.append("the committed files re-derive cleanly before anything is broken")

    # Everything below is generated, so breaking it on the real tree and rebuilding is
    # the same restore the gate itself performs — and it is the only way to prove the
    # gate FIRES rather than merely that it can pass.
    reached = next(r["structure_id"] for r in
                   load(DOMAIN / "structure_tracts.json")["rows"] if r.get("tract"))
    unreached = next(r["structure_id"] for r in
                     load(DOMAIN / "structure_tracts.json")["rows"] if not r.get("tract"))
    try:
        for rel, breaker, what in (
            ("tracts.json", lambda d: d["counts"].update({"resolved": 999}),
             "a hand-edit to tracts.json"),
            ("structure_tracts.json", lambda d: d["rows"][0].update({"tract": "T1N R1E sec 01 NE"}),
             "a hand-edit to the join"),
        ):
            doc = load(DOMAIN / rel)
            breaker(doc)
            dump(DOMAIN / rel, doc)
            if not check(quiet=True):
                print("SELF-TEST: %s did not fail the gate" % what); return 1
            fired.append("%s fails the gate" % what)
            build(quiet=True)

        doc = load(STRUCTURES / ("%s.json" % reached))
        doc["land_owner"]["purchasers"][0]["name"] = "Nobody At All"
        dump(STRUCTURES / ("%s.json" % reached), doc)
        if not check(quiet=True):
            print("SELF-TEST: a rewritten land_owner did not fail the gate"); return 1
        fired.append("a hand-written land_owner on a structure fails the gate")
        build(quiet=True)

        doc = load(STRUCTURES / ("%s.json" % unreached))
        doc["land_owner"] = {"tract": "invented"}
        dump(STRUCTURES / ("%s.json" % unreached), doc)
        if not check(quiet=True):
            print("SELF-TEST: a land_owner on unreached ground did not fail the gate"); return 1
        fired.append("a land_owner on a structure no tract reaches fails the gate")
    finally:
        build(quiet=True)

    print("resolve_land_tracts --self-test: %d assertions fire when broken" % len(fired))
    for f in fired:
        print("  · %s" % f)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.build:
        return build()
    if args.check:
        bad = check()
        for b in bad:
            print("  ✗ %s" % b)
        return 1 if bad else 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
