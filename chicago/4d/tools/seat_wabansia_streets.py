#!/usr/bin/env python3
"""Seat Wabansia's street grid on the committed town grid.

    tools/seat_wabansia_streets.py            print what it would write
    tools/seat_wabansia_streets.py --write    write data/streets/1835.json and the trace
    tools/seat_wabansia_streets.py --check    re-derive the committed lines from the reading

The readings are `data/traces/wabansia_streets.json` (T-0790, the seven east-west
corridors and their names) and `data/traces/wabansia_block_numbering.json` (T-1074,
the tiers, the columns and the tract's west margin). Neither authors ground — both say
so in their own words — and this tool is the one that does.

WHY NOT JUST COMMIT THE PIXELS, which is `seat_kinzie_addition_streets.py`'s argument
and is the same one here. Wabansia's south line IS Kinzie Street: Wright letters
`Kinzie` in that corridor, and the committed `kinzie` is the same street off the
Thompson plat. Carried through the NA sheet's own affine, Wright's Kinzie lands south
of the committed line and leaning the wrong way — 9.1 m out at the tract's west end,
1.4 m at its east, because the sheet's drawn bearing in this corner is about 1.2 deg
off the one the committed grid takes from modern control over a baseline four times
longer. That is the fit's error, not the plat's: the registration admits 16.19 m RMS on
eight control points and none of them is within 900 m of this tract.

So the sheet is asked for what it measures well — the perpendicular distance from one
ruled corridor to the next, inside one corner of one raster — and the committed grid is
asked for where that ladder hangs and which way it lies. Every line here is PARALLEL to
committed `kinzie` and offset north of it by the sheet's own measured tier pitches,
accumulated. Nothing is fitted to modern pavement and nothing is chosen to look right.

WHAT IS NOT SEATED, and why each is somebody else's:

  * The two north-south corridors. Wright letters no name on either (T-1074), and this
    project does not commit an unnamed street.
  * The east reach into the water-lot tract — Kain's and Hight's subdivision, the wedge
    between the east column and the river. T-1077 read it as a lot strip; its corridors
    `Kain` and `Water` cross the lots and are not these streets continued.
  * `kinzie` itself, which stops at local east -320 and is extrapolated 418 m west to
    meet this tract. Wright draws it the whole way and the committed line should be
    carried, but carrying an attested street moves platted lot lines and re-scores the
    corridor-intrusion count, so it is its own unit of work.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STREETS = ROOT / "data/streets/1835.json"
TRACE = ROOT / "data/traces/wabansia_streets.json"
BLOCKS = ROOT / "data/traces/wabansia_block_numbering.json"
GCP = ROOT / "data/traces/gcp/wright_1834_nara_hup_gcps.json"
DATUM = ROOT / "data/datum.json"
BRANCHES = ROOT / "data/terrain/epochs/e1834_harbor_cut/branches.geojson"
OUT = ROOT / "data/traces/wabansia_seating.json"
FT = 0.3048

# The datum street, and the streets seated off it, south to north. `kinzie` is the
# tract's own south line and is already committed; it is the anchor, not an output.
DATUM_ID = "kinzie"
SEATED = ["hubbard", "owen", "hight", "sailors", "trade", "free"]

NAME_2026 = {}   # nothing in this repository attests a modern name in this tract
NAME_NOTE = ("`name_2026` is null because no source in this repository attests what this "
             "street is called today. The registration's eight control points are all in "
             "the Original Town and Kinzie's Addition; none is within 900 m of Wabansia, "
             "so `osm_streets_2026` cannot be asked the question by crossing. A modern "
             "name is not evidence about 1835 and is not guessed at here.")

NOTE = (
    "Wabansia, surveyed 1831 — the earliest speculative addition laid out at Chicago — and "
    "drawn whole on J. S. Wright's 1834 survey, which letters the tract `Wonbonsia` and this "
    "street `{sheet}`. GEOMETRY: the corridor is read off the sheet by "
    "tools/read_wabansia_streets.py and recorded in data/traces/wabansia_streets.json, "
    "found not by width — Wabansia's blocks are four lots deep at a 33 px lot pitch and its "
    "corridors run 28.9-39.2 px, so the two populations overlap and a width test returned "
    "four wrong corridors out of five — but as the rule pair that brackets Wright's own "
    "lettering. The LINE is that reading laid off `kinzie` by tools/seat_wabansia_streets.py: "
    "parallel to the committed line and north of it by the perpendicular distance Wright's "
    "own Kinzie corridor stands from this one on the sheet. Wabansia's south line is Kinzie "
    "Street, "
    "and carried through the sheet's own affine Wright's Kinzie lands 9.1 m south of the "
    "committed line at the tract's west end and 1.4 m at its east — a bearing about 1.2 deg "
    "off, against a registration that admits 16.19 m RMS with no control point within 900 m "
    "of this tract. So the sheet measures the ladder and the committed grid holds it. "
    "CORRIDOR: 24.02 m. The method reads the Original Town's platted 80 ft corridors on this "
    "sheet at 83.6 ft (three readings, sd 5.2) and Wabansia's at 82.3 ft (seven readings, sd "
    "10.4), which against a platted 80 ft is 78.8 ft — so Wabansia is platted on the town's "
    "own street width, and the reading cannot distinguish 78.8 ft from 80 ft inside a control "
    "that itself spreads 5.2 ft. The recorded figure is the read one, not the round one. "
    "STATUS follows `madison`'s and `ohio_north`'s: platted ground, not road. In 1835 this "
    "tract is a survey over prairie — `track_width_m` is 0 because no wagon track is drawn or "
    "attested on it, `alleys` is false because the sheet rules none inside these blocks, and "
    "the confidences say `inferred` because the line is read off Wright's sheet as a ruled "
    "line and anchored on committed control, not traced from a plat this project holds. "
    "EXTENT stops where the reading stops: west at the tract's own boundary rule, east at the "
    "last block corner T-1074 read on the tiers this street divides. Wright carries the grid "
    "east into the water-lot tract — Kain's and Hight's subdivision — and that wedge is "
    "T-1077's, read as a lot strip and not seated. T-0790, piece 3."
)

OCCUPANCY = {
    "question": "whoever the sources put on this ground before 1 July 1835",
    "found": [
        {
            "as_printed": "Doctor Kimberl",
            "normalized": "[uncertain: Doctor Kimberly]",
            "role": "occupant",
            "occupations": ["physician"],
            "claim": "chicago_democrat_1834_07_16#c017",
            "gazetteer_id": "person_uncertain_doctor_kimberly",
            "what": ("a dwelling of four rooms, a kitchen, a barn and a garden, in Wabansia, "
                     "occupied by a doctor and advertised through Col. Hamilton — the only "
                     "house in this run of the Democrat described room by room"),
            "confidence": "documented",
            "note": ("The name is CUT AT THE RIGHT EDGE of the column and the gazetteer "
                     "brackets it; E. S. Kimberly stands in the same issue's candidate list "
                     "and is NOT identified with the doctor. The advertisement places a "
                     "household in Wabansia on 16 July 1834, eleven months before this "
                     "scene's date, and places it NOWHERE INSIDE IT: no block, no lot, no "
                     "street. Seating the streets does not seat this house, and no structure "
                     "is minted from it here."),
        }
    ],
    "searched": [
        "data/research/newspapers/extracted/*.json — every claim naming Wabansia",
        "data/research/newspapers/gazetteer.json — every person with Wabansia in associated_places",
        "data/residents/households/*.json",
    ],
    "reading": ("ONE household, unplaced. Wabansia is named in the Democrat three other times "
                "and each is the same lithographic town map advertised for sale by Kinzie & "
                "Forsyth (1834-07-02, 1834-11-05, 1834-11-19) — a claim about what the town's "
                "inhabitants thought its extent was, not about who lived there. So the tract "
                "this reading draws is, on the evidence this project holds, a survey over "
                "prairie with one doctor's house somewhere in it."),
    "leaves_open": ("data/research/newspapers/place_vocabulary.json still resolves `Wabansia` "
                    "as UNDECIDED on basis B4 — 'a survey adjacent to the town that this "
                    "project commits none of' — and names T-0790 as the ticket that would "
                    "settle it. That sentence is now false of the ground and the ruling is "
                    "the owner's B-rule to change, not this tool's."),
}


# ------------------------------------------------------------------ the frame

def _frame():
    g = json.loads(GCP.read_text())
    d = json.loads(DATUM.read_text())
    c = g["fit"]["coefficients"]

    def to_local(px, py):
        return (c["a"] * px + c["b"] * py + c["c"] - d["origin_utm_e"],
                c["d"] * px + c["e"] * py + c["f"] - d["origin_utm_n"])

    return to_local


def _unit(a, b):
    d = (b[0] - a[0], b[1] - a[1])
    n = math.hypot(*d)
    return (d[0] / n, d[1] / n)


def _extents(trace, blocks):
    """The west and east pixel bound of each corridor, from T-1074's block grid.

    A corridor divides two tiers and is bounded by what those tiers are bounded by:
    west at the tract's own boundary rule (the OUTER of the west margin's pair, averaged
    over the two tiers, because the boundary slants), east at the farther of the two
    tiers' last block corner. The two disagree by 166 px at Sailors Street, where the
    grid jogs and the blocks south of it are a lot wider than the blocks north; the
    street runs the length of the longer tier because that tier's blocks front it."""
    tiers = {t["id"]: t for t in blocks["tiers"]}
    margin = {w["tier"]: w for w in blocks["west_margin"]}
    east = {}
    for col in blocks["columns"]:
        east[col["tier"]] = max(east.get(col["tier"], 0.0), col["east_px"])
    adj = {}
    ids = {s["id"] for s in trace["streets"]}
    for t in blocks["tiers"]:
        if t["south"] in ids:
            adj.setdefault(t["south"], []).append(t["id"])
        if t["north"] in ids:
            adj.setdefault(t["north"], []).append(t["id"])
    out = {}
    for sid, ts in adj.items():
        ends = sorted((east[t] for t in ts), reverse=True)
        out[sid] = {
            "tiers": sorted(ts),
            "west_px": round(sum(margin[t]["rule_px_x"][0] for t in ts) / len(ts), 2),
            "east_px": ends[0], "east_px_nearer": ends[-1],
        }
    return out, tiers, margin, east


def _bank_px(to_local):
    """The committed west bank of the North Branch, carried back into sheet pixels, so
    the grid's east edge can be checked against water this project already holds."""
    g = json.loads(BRANCHES.read_text())
    d = json.loads(DATUM.read_text())
    c = json.loads(GCP.read_text())["fit"]["coefficients"]
    a, b, dd, e = c["a"], c["b"], c["d"], c["e"]
    c0, f0 = c["c"] - d["origin_utm_e"], c["f"] - d["origin_utm_n"]
    det = a * e - b * dd
    for feat in g["features"]:
        if feat["properties"].get("name", "").startswith("West bank of the North Branch"):
            pts = []
            for X, Y in feat["geometry"]["coordinates"]:
                u, v = X - d["origin_utm_e"] - c0, Y - d["origin_utm_n"] - f0
                pts.append(((e * u - b * v) / det, (-dd * u + a * v) / det))
            return sorted(pts, key=lambda p: p[1])
    raise SystemExit("the committed west bank of the North Branch is not in branches.geojson")


def _at_y(poly, y):
    for (x0, y0), (x1, y1) in zip(poly, poly[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return None


# ------------------------------------------------------------------ the seating

def build():
    trace = json.loads(TRACE.read_text())
    blocks = json.loads(BLOCKS.read_text())
    doc = json.loads(STREETS.read_text())
    by = {s["id"]: s for s in doc["streets"]}
    to_local = _frame()
    shear = trace["method"]["shear_ew"]
    read = {s["id"]: s for s in trace["streets"]}
    ext, tiers, margin, east = _extents(trace, blocks)

    kin = by[DATUM_ID]["path_local_enu_m"]
    u = _unit(kin[0], kin[-1])            # along Kinzie, eastward
    nrm = (-u[1], u[0])                   # off Kinzie, northward
    kz = read[DATUM_ID]

    def kinzie_py(px):
        """Wright's Kinzie corridor centre, in raster rows, at this column."""
        return kz["centre_px_y"] + shear * (px - kz["ref_px_x"])

    def seat(px, py):
        """A sheet pixel on modern ground.

        EASTING is the sheet's own through the registration's affine; no control
        constrains this tract along its own streets and none is invented. NORTHING is
        the committed `kinzie` line's at that easting, plus the perpendicular distance
        north of Wright's own Kinzie corridor, measured on the sheet. So the sheet
        supplies the ladder and the committed grid supplies where it hangs and which
        way it lies."""
        E = to_local(px, py)[0]
        a = to_local(px, kinzie_py(px))
        b = to_local(px, py)
        d = math.copysign(math.dist(a, b), kinzie_py(px) - py)
        t = (E - kin[0][0]) / u[0]
        base = (kin[0][0] + t * u[0], kin[0][1] + t * u[1])
        return [round(base[0] + d * nrm[0], 2), round(base[1] + d * nrm[1], 2)]

    bank = _bank_px(to_local)
    m_per_px = math.dist(to_local(900, 1500), to_local(900, 1501))

    out, evidence = [], []
    for sid in SEATED:
        s, x = read[sid], ext[sid]
        y0, rx = s["centre_px_y"], s["ref_px_x"]

        def py(px):
            return y0 + shear * (px - rx)

        # THE EAST END is the farther of the two tiers' last block corner — the tier
        # whose blocks are wider fronts the street for its whole length — UNLESS that
        # corner falls east of the committed west bank of the North Branch, in which
        # case the nearer tier's is taken. A platted line is not committed across water
        # this project already holds. It bites once, at Sailors Street, where the grid
        # jogs two lots east and T-1074's corner for tier 4 stands 65.6 m inside the
        # committed water. Which of the two readings is wrong is not settled here: the
        # bank is traced from this same sheet and T-1078 has it short of Wright's ink on
        # two stretches of the east side already.
        far, near = x["east_px"], x["east_px_nearer"]
        bx_far = _at_y(bank, py(far))
        over = None if bx_far is None else round((far - bx_far) * m_per_px, 1)
        east_px = near if (over is not None and over > 0 and near < far) else far

        path = [seat(x["west_px"], py(x["west_px"])), seat(east_px, py(east_px))]
        out.append(_entry(sid, s, path))

        bx = _at_y(bank, py(east_px))
        evidence.append({
            "id": sid, "name_on_sheet": s["name_on_sheet"],
            "tiers": x["tiers"], "west_px": x["west_px"],
            "east_px": east_px, "east_px_refused": far if east_px != far else None,
            "centre_px_y": y0, "ref_px_x": rx,
            "north_of_kinzie_m": round(math.dist(
                to_local(rx, kinzie_py(rx)), to_local(rx, y0)), 2),
            "path_local_enu_m": path,
            "east_end_past_committed_bank_m": None if bx is None
                else round((east_px - bx) * m_per_px, 1),
            "refused_end_past_committed_bank_m": over if east_px != far else None,
        })

    poly = _polygon(seat, tiers, margin, east, kz, shear)
    return doc, by, out, evidence, trace, poly


def _polygon(seat, tiers, margin, east, kz, shear):
    """The BLOCK GRID's outline, from T-1074's own corners, seated the same way.

    It is not the tract's outline and is not called one. Wabansia runs east of these
    blocks to the North Branch, over the water-lot wedge — Kain's and Hight's
    subdivision — which T-1077 read as a lot strip and deliberately did not seat. The
    tract polygon waits on that."""
    order = ["t1", "t2", "t3", "t4", "t5", "t6", "t7"]
    south_px_y = kz["rule_px_y"][0]          # Kinzie Street's north rule
    north_px_y = tiers["t1"]["y_px"][0]      # the tract boundary T-1074 read
    ring = []
    ring.append(seat(margin["t7"]["rule_px_x"][0], south_px_y))
    for t in reversed(order):
        ring.append(seat(margin[t]["rule_px_x"][0], tiers[t]["mid_px_y"]))
    ring.append(seat(margin["t1"]["rule_px_x"][0], north_px_y))
    ring.append(seat(east["t1"], north_px_y))
    for t in order:
        ring.append(seat(east[t], tiers[t]["mid_px_y"]))
    ring.append(seat(east["t7"], south_px_y))
    ring.append(ring[0])
    return ring


def _entry(sid, s, path):
    n2026 = NAME_2026.get(sid)
    e = {
        "id": f"{sid}_wabansia" if sid in ("free",) and False else sid,
        "name_1835": f"{s['name_on_sheet']} Street",
        "name_2026": n2026,
        "name_changed": False,
        "path_local_enu_m": path,
        "corridor_width_m": 24.02,
        "track_width_m": 0,
        "opened": False,
        "worn": False,
        "alleys": False,
        "status_1835": "platted, unopened, unworn",
        "surface": "unworn_prairie",
        "traffic": "none",
        "geometry_confidence": "inferred",
        "surface_confidence": "inferred",
        "wear_confidence": "inferred",
        "sources": ["wright_1834_nara_hup", "wright_1834"],
        "note": NOTE.format(sheet=s["name_on_sheet"]),
    }
    if n2026 is None:
        e["name_note"] = NAME_NOTE
    return e


# ------------------------------------------------------------------ the write

def _render(entry, indent=4):
    text = json.dumps(entry, indent=2, ensure_ascii=False)

    def collapse(m):
        return re.sub(r"\s*\n\s*", " ", m.group(0)).replace("[ ", "[").replace(" ]", "]")

    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"\[[^\[\]{}]*\]", collapse, text)
    pad = " " * indent
    return "\n".join(pad + ln for ln in text.split("\n"))


def _splice(text, entries):
    """Append the new streets WITHOUT re-serialising the file, for the reason
    seat_kinzie_addition_streets.py gives: a writer that re-emits this document changes
    a thousand lines of escaping to add six streets, and a reviewer cannot see that."""
    tail = re.compile(r'\n  \]\n\}\s*$')
    if not tail.search(text):
        raise SystemExit("data/streets/1835.json does not end in the shape this tool expects")
    body = ",\n".join(_render(e) for e in entries)
    return tail.sub(",\n" + body + "\n  ]\n}\n", text)


def _trace_doc(evidence, trace, poly):
    return {
        "_doc": __doc__,
        "ticket": "T-1070",
        "datum": {
            "street": DATUM_ID,
            "committed_in": "data/streets/1835.json",
            "why": ("Wabansia's south line is Kinzie Street on Wright's sheet and Kinzie "
                    "Street is committed off the Thompson plat. It is the one line the two "
                    "surveys share, so it is the one thing the ladder can hang from."),
        },
        "method": {
            "rung": ("each street's perpendicular distance north of Kinzie Street, the sum of "
                     "the sheet's measured tier pitches between them"),
            "bearing": "the committed kinzie line's, not the sheet's",
            "easting": ("the sheet's own, through the registration's affine. No control "
                        "constrains the along-street position of this tract and none is "
                        "invented: the seating is a translation north, not a fit."),
            "tier_pitch_source": "data/traces/wabansia_streets.json § module.tier_pitch_m.each",
        },
        "sheet_vs_committed_kinzie": trace["cross_check"],
        "shear_between_columns": {
            "what": ("T-0790 read the seven corridors in three different columns of the "
                     "sheet — `col_west` at x 700, `col_trade` at 880, `col_east` at 990 — "
                     "because Wright letters the names inside the corridors and a name is "
                     "ink in exactly the gap the reading is trying to find. A rule row is "
                     "reported at its window's own left edge, and the rules lean: "
                     "dy/dx 0.019. So two corridors read in different columns are not "
                     "directly subtractable, and `module.tier_pitch_px` in that file "
                     "subtracts them anyway."),
            "effect_px": {"free_to_trade": 2.09, "trade_to_sailors": 3.42},
            "handled": ("This seating never subtracts two rows. Every distance is measured "
                        "between a street's own row and Wright's Kinzie corridor carried to "
                        "that same column by the shear, so the lean cancels. It is why "
                        "`north_of_kinzie_m` for Free and Trade stands 4.1 m and 2.5 m "
                        "north of the running sum of that table."),
            "not_a_correction_of": ("data/traces/wabansia_streets.json, which is a reading "
                                    "and is left as read. The module figure it reports is "
                                    "a mean over six spacings and the lean is inside its "
                                    "own 3.01 m sd."),
        },
        "streets": evidence,
        "block_grid_polygon_local_enu_m": poly,
        "tract_polygon_local_enu_m": {
            "seated": False,
            "why": ("Wabansia runs east of the block grid to the North Branch, over the "
                    "water-lot wedge — Kain's and Hight's subdivision — which T-1077 read "
                    "as a lot strip and deliberately did not seat. Until that wedge is on "
                    "modern ground the tract has no east boundary and this project will "
                    "not draw one; `block_grid_polygon_local_enu_m` is the part of "
                    "Wabansia this reading can outline and is not called the tract."),
        },
        "occupancy_before_1835_07_01": OCCUPANCY,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="the committed street lines still re-derive from the readings")
    a = ap.parse_args()
    doc, by, out, evidence, trace, poly = build()

    if a.check:
        bad = []
        for s in out:
            have = by.get(s["id"])
            if have is None:
                bad.append(f"{s['id']} is not in data/streets/1835.json")
                continue
            for a0, b0 in zip(have.get("path_local_enu_m", []), s["path_local_enu_m"]):
                if max(abs(a0[0] - b0[0]), abs(a0[1] - b0[1])) > 0.02:
                    bad.append(f"{s['id']}: committed {have['path_local_enu_m']}, "
                               f"re-derived {s['path_local_enu_m']}")
                    break
            for k in ("corridor_width_m", "name_1835", "name_2026", "status_1835",
                      "sources", "track_width_m", "surface", "traffic", "note"):
                if have.get(k) != s[k]:
                    bad.append(f"{s['id']}.{k}: committed {have.get(k)!r}, re-derived {s[k]!r}")
        if OUT.exists():
            was = json.loads(OUT.read_text())
            now = _trace_doc(evidence, trace, poly)
            for key in ("streets", "block_grid_polygon_local_enu_m"):
                if json.dumps(was.get(key), sort_keys=True) != \
                   json.dumps(now[key], sort_keys=True):
                    bad.append(f"{OUT.name} § {key} does not re-derive from the readings")
        else:
            bad.append(f"{OUT.name} is missing")
        for line in bad:
            print("RED  " + line)
        print(f"wabansia streets: {len(out)} line(s) re-derive from the readings in "
              f"data/traces/wabansia_streets.json and wabansia_block_numbering.json"
              if not bad else f"{len(bad)} disagreement(s)")
        return 1 if bad else 0

    for s, ev in zip(out, evidence):
        print(f'{s["id"]:9s} {s["name_1835"]:18s} {ev["north_of_kinzie_m"]:8.2f} m N of kinzie  '
              f'{s["path_local_enu_m"]}')
        if ev["east_end_past_committed_bank_m"] is not None:
            print(f'{"":9s} east end vs committed west bank: '
                  f'{ev["east_end_past_committed_bank_m"]:+.1f} m')
    if a.write:
        fresh = [s for s in out if s["id"] not in by]
        STREETS.write_text(_splice(STREETS.read_text(), fresh))
        OUT.write_text(json.dumps(_trace_doc(evidence, trace, poly),
                                   indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {STREETS.relative_to(ROOT)} and {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
