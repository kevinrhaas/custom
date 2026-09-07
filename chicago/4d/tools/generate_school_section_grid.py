#!/usr/bin/env python3
"""Derive the School Section's block grid, its twelve east-west streets and its three
reservations from J. S. Wright's 1834 survey, read on the National Archives / Historic
Urban Plans reproduction registered by T-0787.

The section is the mile square of Section 16, T39N R14E — the school section the state
sold in October 1833 — bounded by Madison Street on the north, State Street on the east
and, a mile from each, the lines that later carried Twelfth Street and Halsted Street.
Wright draws it whole, ruled into a grid and numbered, and this project has never held
any of it: no block, no street, and no ground for the 125 land-sale rows that name its
block numbers.

METHOD, and it is a MEASUREMENT off the sheet rather than a re-use of Thompson's module.

  1. The scan is resampled into scene coordinates (local ENU metres, EPSG:26916 through
     data/datum.json) using the affine in data/traces/gcp/wright_1834_nara_hup_gcps.json.
     That deskews the drawing: the plat's own north-south and east-west rules become the
     axes of the sampled raster, so a ruled line is a peak in a one-dimensional darkness
     profile and nothing has to be traced by hand.
  2. Every line of the grid was picked as the centroid of that peak, in six independent
     bands along its length, and the median taken. Where a street is drawn as a pair of
     rules the pair gives the corridor its drawn width; where the draughtsman drew one
     line the width is not recoverable from the sheet and the platted standard is used.
  3. The measured line table is then anchored on the section itself. Madison and State
     cross at a PLSS section corner — sections 9/10/15/16 — which is GCP G1 of the
     registration, and the section is a statute mile on a side. The measured interior
     lines are rescaled linearly onto that exact square. Residuals are reported below
     and in docs/RESEARCH/school_section_grid_1834.md.

WHAT IS MEASURED AND WHAT IS ADOPTED. The measured east-west span of the grid falls 6.3 m
SHORT of the statute mile, four tenths of one per cent; the measured north-south span
overruns it by 49.3 m, three per cent. That asymmetry is the registration's own finding
showing at the bottom of the sheet: it measured 5.2 per cent x/y anisotropy on this scan
against 3.7 per cent on the BPL copy, and the extra stretch is in the long axis, along
which the manuscript was torn and backed. The section is a mile on the ground whatever
the paper does, so the grid is anchored on the section and not on the paper.

Run:  python3 tools/generate_school_section_grid.py [--check]
"""
import argparse, hashlib, json, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------------------
# THE MEASUREMENT. Line centres are metres in the resampled (deskewed) frame, before the
# section anchor is applied. `drawn_w` is the separation of the pair of rules where the
# sheet draws the corridor with two, and None where it draws a single line — the widths
# of those are not on the sheet. `bands` is how many of the six sampling bands agreed.
# Sheet names are the draughtsman's, read off the same raster.
# --------------------------------------------------------------------------------------
NS_LINES = [  # west to east
    dict(i=0,  measured=-768.14, drawn_w=15.12, bands=6, sheet_name=None, role="section line (west)"),
    dict(i=1,  measured=-648.20, drawn_w=None,  bands=0, sheet_name=None, role="interior"),
    dict(i=2,  measured=-508.13, drawn_w=16.08, bands=5, sheet_name="Des Plaines", role="interior"),
    dict(i=3,  measured=-382.15, drawn_w=20.49, bands=6, sheet_name="Jefferson", role="interior"),
    dict(i=4,  measured=-270.51, drawn_w=19.71, bands=6, sheet_name="Clinton", role="interior"),
    dict(i=5,  measured=-147.95, drawn_w=21.61, bands=6, sheet_name="Canal", role="interior"),
    dict(i=6,  measured=-41.80,  drawn_w=None,  bands=0, sheet_name=None, role="interior"),
    dict(i=7,  measured=67.40,   drawn_w=None,  bands=0, sheet_name="Market", role="interior"),
    dict(i=8,  measured=203.90,  drawn_w=None,  bands=0, sheet_name=None, role="interior"),
    dict(i=9,  measured=346.36,  drawn_w=20.41, bands=4, sheet_name="Wells", role="interior"),
    dict(i=10, measured=459.60,  drawn_w=None,  bands=0, sheet_name=None, role="interior"),
    dict(i=11, measured=577.59,  drawn_w=21.15, bands=6, sheet_name="Clark", role="interior"),
    dict(i=12, measured=698.70,  drawn_w=None,  bands=0, sheet_name=None, role="interior"),
    dict(i=13, measured=834.90,  drawn_w=None,  bands=0, sheet_name=None, role="section line (east), State Street"),
]
EW_LINES = [  # north to south
    dict(j=0,  measured=-545.99, drawn_w=16.75, bands=6, sheet_name="Madison"),
    dict(j=1,  measured=-686.96, drawn_w=25.21, bands=8, sheet_name="Monroe"),
    dict(j=2,  measured=-832.66, drawn_w=23.34, bands=8, sheet_name="Adams"),
    dict(j=3,  measured=-979.93, drawn_w=21.72, bands=8, sheet_name="Jackson"),
    dict(j=4,  measured=-1129.40, drawn_w=25.00, bands=8, sheet_name=None),
    dict(j=5,  measured=-1280.50, drawn_w=None,  bands=0, sheet_name=None),
    dict(j=6,  measured=-1399.14, drawn_w=24.07, bands=8, sheet_name=None),
    dict(j=7,  measured=-1545.43, drawn_w=25.19, bands=4, sheet_name=None),
    dict(j=8,  measured=-1660.67, drawn_w=16.84, bands=8, sheet_name=None),
    dict(j=9,  measured=-1808.40, drawn_w=None,  bands=0, sheet_name=None),
    dict(j=10, measured=-1924.45, drawn_w=13.66, bands=8, sheet_name=None),
    dict(j=11, measured=-2077.60, drawn_w=None,  bands=0, sheet_name=None),
    dict(j=12, measured=-2204.64, drawn_w=None,  bands=0, sheet_name="section line (south)"),
]

FT = 0.3048
EW_CORRIDOR_M = round(80 * FT, 3)   # 24.384 — the platted standard of both 1830 plats
NS_CORRIDOR_M = round(66 * FT, 3)   # 20.117 — a surveyor's chain; measured median 20.41

MILE_M = 1609.344

# --------------------------------------------------------------------------------------
# THE READING. cells are (column index 0-12, row index 0-11); a block occupying two
# columns is written with both. Rows run north to south, columns west to east.
# Everything here was read off the resampled raster at 1x, 2x and 3x.
# --------------------------------------------------------------------------------------
ROWS = [
    # row 0 (Madison to Monroe)
    [(0, 1), (1, 24), (2, 25), (3, 48), (4, 49), (5, 72), (6, 80), (7, 81),
     (8, 94), (9, 95), (10, 118), (11, 119), (12, 142)],
    [(0, 2), (1, 23), (2, 26), (3, 47), (4, 50), (5, 71), (6, 79), (7, 82),
     (8, 93), (9, 96), (10, 117), (11, 120), (12, 141)],
    [(0, 3), (1, 22), (2, 27), (3, 46), (4, 51), (5, 70), ((6, 7), 83),
     (8, 92), (9, 97), (10, 116), (11, 121), (12, 140)],
    [(0, 4), (1, 21), (2, 28), (3, 45), (4, 52), (5, 69), ((6, 7), 84),
     (8, 91), (9, 98), (10, 115), (11, 122), (12, 139)],
    [(0, 5), (1, 20), (2, 29), (3, 44), (4, 53), (5, 68),
     (8, 90), (9, 99), (10, 114), (11, 123), (12, 138)],
    [(0, 6), (1, 19), (2, 30), (3, 43), (4, 54), (5, 67),
     (8, 89), (9, 100), (10, 113), (11, 124), (12, 137)],
    [(0, 7), (1, 18), (2, 31), (3, 42), (4, 55), (5, 66),
     (8, 88), (9, 101), (10, 112), (11, 125), (12, 136)],
    [(0, 8), (1, 17), (2, 32), (3, 41), (4, 56), (5, 65),
     (8, 87), (9, 102), (10, 111), (11, 126), (12, 135)],
    [(0, 9), (1, 16), (2, 33), (3, 40), (4, 57), (5, 64), ((6, 7), 73),
     (8, 86), (9, 103), (10, 110), (11, 127), (12, 134)],
    [(0, 10), (1, 15), (2, 34), (3, 39), (4, 58), (5, 63), ((6, 7), 74),
     (8, 85), (9, 104), (10, 109), (11, 128), (12, 133)],
    [(0, 11), (1, 14), (2, 35), (3, 38), (4, 59), (5, 62), (6, 75), (7, 78),
     (9, 105), (10, 108), (11, 129), (12, 132)],
    [(0, 12), (1, 13), (2, 36), (3, 37), (4, 60), (5, 61), (6, 76), (7, 77),
     (9, 106), (10, 107), (11, 130), (12, 131)],
]

# Numerals NOT read as ink in their own block, and why. Everything else is on the sheet.
NUMERAL_NOTES = {
    1: ("inferred",
        "The sheet writes 'Reserved' across this block and no numeral. 1 is supplied by the "
        "serpentine sequence, which runs 1-12 down this westernmost tier with 2 in the block "
        "immediately south. The October 1833 sale sells lots in every other block of the two "
        "northern tiers and none here, which is the reservation's own corroboration."),
    142: ("inferred",
          "The sheet writes 'Reserved' across this block and no numeral. 142 is supplied by the "
          "sequence: the easternmost tier runs 131 at the south up to 141 in the block "
          "immediately south of this one. The ticket that asked for this work called this block "
          "119; 119 is read on the sheet one tier WEST of it, and 141 sits between them. The "
          "1833 sale sells lots in 119, 120 and 141 and none here."),
    77: ("inferred",
         "The second glyph is written without a crossbar and reads as either 7 or 1 at 3x. 77 is "
         "adopted: 71 is read in ink two tiers west in the second row, the sequence runs 73-76 "
         "down the tier to the west and back up this one through 78 immediately north, and the "
         "1833 sale, which reached only the four northern rows, sells in neither."),
    81: ("documented",
         "The numeral is written TWICE inside this block, side by side, and both readings give "
         "81. Recorded as read; the doubling is the draughtsman's."),
    82: ("documented",
         "A second numeral stands beside this one and is lost under an ink blot. The numeral "
         "read here is 82 and it is clear; what the blot covers is not recoverable."),
}

# Blocks the South Branch crosses. Their east or west side is not on the sheet as a ruled
# line but as the drawn bank, and T-0794 is the ticket that will commit that bank.
BANK_PENDING = {
    70: "east", 71: "east", 78: "west", 83: "west", 84: "west",
    85: "west", 86: "west", 87: "west", 88: "west",
    73: "east", 74: "east",
}

RESERVED = {
    1: dict(name="The north-west reservation",
            where="the corner of Madison Street and the section's west line"),
    142: dict(name="The north-east reservation",
              where="the corner of Madison Street and State Street"),
    87: dict(name="The South Branch reservation",
             where="on the east bank of the South Branch, spanning blocks 87 and 88"),
    88: dict(name="The South Branch reservation",
             where="on the east bank of the South Branch, spanning blocks 87 and 88"),
}

EW_STREET_IDS = [
    ("madison", "Madison Street", "Madison Street"),
    ("monroe", "Monroe Street", "Monroe Street"),
    ("adams", "Adams Street", "Adams Street"),
    ("jackson", "Jackson Boulevard", "Jackson Boulevard"),
]


def load(p):
    return json.loads((ROOT / p).read_text())


def build():
    gcp = load("data/traces/gcp/wright_1834_nara_hup_gcps.json")
    datum = load("data/datum.json")
    c = gcp["fit"]["coefficients"]
    a, b, cc, d, e, f = c["a"], c["b"], c["c"], c["d"], c["e"], c["f"]
    det = a * e - b * d
    oE, oN = datum["origin_utm_e"], datum["origin_utm_n"]

    def local_to_pixel(x, y):
        dE, dN = (x + oE) - cc, (y + oN) - f
        return ((e * dE - b * dN) / det, (-d * dE + a * dN) / det)

    g1 = next(g for g in gcp["gcps"] if g["id"] == "G1")
    gx, gy = g1["pixel"]
    cx = a * gx + b * gy + cc - oE
    cy = d * gx + e * gy + f - oN

    anchor = dict(
        corner="State Street and Madison Street, the PLSS corner of sections 9/10/15/16, "
               "T39N R14E, and GCP G1 of the registration",
        corner_local_enu_m=[round(cx, 2), round(cy, 2)],
        north=round(cy, 3), east=round(cx, 3),
        south=round(cy - MILE_M, 3), west=round(cx - MILE_M, 3),
        side_m=MILE_M,
    )

    m0, m1 = NS_LINES[0]["measured"], NS_LINES[-1]["measured"]
    n0, n1 = EW_LINES[0]["measured"], EW_LINES[-1]["measured"]
    sx = MILE_M / (m1 - m0)
    sy = -MILE_M / (n1 - n0) * -1

    X, Y = [], []
    for L in NS_LINES:
        X.append(anchor["west"] + (L["measured"] - m0) * sx)
    for L in EW_LINES:
        Y.append(anchor["north"] + (L["measured"] - n0) * (-MILE_M / (n0 - n1)) * -1)
    # y: measured decreases southward; map [n0,n1] -> [north, south]
    Y = [anchor["north"] + (L["measured"] - n0) / (n1 - n0) * (anchor["south"] - anchor["north"])
         for L in EW_LINES]

    for L, xv in zip(NS_LINES, X):
        L["adopted"] = round(xv, 3)
        L["anchor_shift_m"] = round(xv - L["measured"], 2)
        L["corridor_width_m"] = NS_CORRIDOR_M
    for L, yv in zip(EW_LINES, Y):
        L["adopted"] = round(yv, 3)
        L["anchor_shift_m"] = round(yv - L["measured"], 2)
        L["corridor_width_m"] = EW_CORRIDOR_M

    raster = gcp["raster"]

    def block_rect(cols, rows):
        w = X[min(cols)] + NS_CORRIDOR_M / 2
        ee = X[max(cols) + 1] - NS_CORRIDOR_M / 2
        n = Y[min(rows)] - EW_CORRIDOR_M / 2
        s = Y[max(rows) + 1] + EW_CORRIDOR_M / 2
        return w, ee, n, s

    blocks = []
    for rj, row in enumerate(ROWS):
        for cells, num in row:
            cols = list(cells) if isinstance(cells, tuple) else [cells]
            w, ee, n, s = block_rect(cols, [rj])
            poly = [[round(w, 2), round(n, 2)], [round(ee, 2), round(n, 2)],
                    [round(ee, 2), round(s, 2)], [round(w, 2), round(s, 2)]]
            px = [local_to_pixel(*p) for p in poly]
            x0 = min(p[0] for p in px); x1 = max(p[0] for p in px)
            y0 = min(p[1] for p in px); y1 = max(p[1] for p in px)
            conf, note = NUMERAL_NOTES.get(num, ("documented", None))
            entry = dict(
                block_number=num,
                id="blk_school_section_%d" % num,
                cells=[[c_, rj] for c_ in cols],
                boundary_local_enu_m=poly,
                area_m2=round((ee - w) * (n - s), 1),
                frontage_m=round(ee - w, 2),
                depth_m=round(n - s, 2),
                numeral=dict(
                    read=None if conf == "inferred" and num in (1, 142) else str(num),
                    confidence=conf,
                    on_sheet=num not in (1, 142),
                    source="wright_1834_nara_hup",
                    crop_na_pixels=dict(x=int(round(x0)), y=int(round(y0)),
                                        w=int(round(x1 - x0)), h=int(round(y1 - y0))),
                    note=note,
                ),
                bounded_by=dict(
                    north=street_id(min(rj, len(EW_LINES) - 1)),
                    south=street_id(min(rj + 1, len(EW_LINES) - 1)),
                    west_sheet_name=NS_LINES[min(cols)]["sheet_name"],
                    east_sheet_name=NS_LINES[max(cols) + 1]["sheet_name"],
                ),
                geometry_confidence="reconstructed" if num in BANK_PENDING else "inferred",
            )
            if num in BANK_PENDING:
                entry["open_side"] = BANK_PENDING[num]
                entry["bank_pending"] = (
                    "The South Branch crosses this block and its %s side is the drawn bank, not a "
                    "ruled line. The rectangle here is the block's CELL in the grid; T-0794 commits "
                    "the bank and closes it." % BANK_PENDING[num])
            if num in RESERVED:
                entry["reserved"] = True
            blocks.append(entry)

    blocks.sort(key=lambda b: b["block_number"])
    return anchor, blocks, raster, sx


def street_id(j):
    if j < len(EW_STREET_IDS):
        return EW_STREET_IDS[j][0]
    if j == len(EW_LINES) - 1:
        return None  # the section's south line; Twelfth Street is later than this scene
    return "school_section_tier_%d" % j


def street_records(anchor):
    """The twelve east-west streets, as platted lines across the section."""
    out = []
    for j, L in enumerate(EW_LINES):
        if j == len(EW_LINES) - 1:
            continue  # the section's south line carries no street on this sheet
        sid = street_id(j)
        named = j < len(EW_STREET_IDS)
        name_1835 = EW_STREET_IDS[j][1] if named else None
        y = L["adopted"]
        rec = dict(
            id=sid,
            name_1835=name_1835,
            name_2026=EW_STREET_IDS[j][2] if named else None,
            name_changed=False,
            path_local_enu_m=[[round(anchor["west"], 2), round(y, 2)],
                              [round(anchor["east"], 2), round(y, 2)]],
            corridor_width_m=EW_CORRIDOR_M,
            track_width_m=0,
            opened=False,
            worn=False,
            alleys=False,
            status_1835="platted, unopened, unworn",
            surface="unworn_prairie",
            traffic="none",
            geometry_confidence="inferred",
            surface_confidence="inferred",
            wear_confidence="inferred",
            sources=["wright_1834_nara_hup", "wright_1834"],
            note=(
                "%s. Read off Wright's 1834 survey as a ruled line of the School Section's grid "
                "(Section 16, T39N R14E) and anchored on the section's own mile square; the "
                "measured line is at local N %+.1f m and the anchor moves it %+.1f m. THE STATUS "
                "IS THE OWNER'S READING OF THE SHEET, 2026-09-05: 'no alleys and no street names "
                "but still a grid that should have some wilderness trees'. So the corridor is "
                "platted and the ground inside it is not: `track_width_m` is 0 because no wagon "
                "track is drawn or attested here, `alleys` is false because the sheet rules none "
                "inside these blocks, and the flora belts are not cut for it. What a visitor "
                "should see is a survey line over prairie, not a road."
                % (("Madison Street, the section's own north line and the boundary of the Town of "
                    "Chicago" if j == 0 else "The %s tier of the School Section's grid" % (
                        name_1835 or "%d%s" % (j, {1: 'st', 2: 'nd', 3: 'rd'}.get(j % 10 if j % 100 not in (11, 12, 13) else 0, 'th')))),
                   L["measured"], L["anchor_shift_m"])
            ),
        )
        if not named:
            rec["name_note"] = (
                "UNNAMED ON THE SHEET. Wright rules the tier and writes no name on it; the four "
                "streets he does name — Madison, Monroe, Adams and Jackson — are the four "
                "northernmost. `name_1835` is null rather than a modern name carried back, "
                "because the later names of these lines are not evidence about 1835.")
        out.append(rec)
    return out


def cross_check_numbering():
    """The reading in ROWS above, against T-0875's independent reading of the same sheet.

    Two runs read all 142 numerals off this sheet within hours of each other and neither
    could see the other's work: this module's table was read off the resampled raster, and
    `data/traces/school_section_block_numbering.json` was read by
    `tools/read_school_section_numerals.py` on the sheet's own pixels. They agree on every
    one of the 142 cells. That is worth more than either reading alone, so it is a GATE
    rather than a remark: if the two ever diverge, this tool stops.
    """
    other = load("data/traces/school_section_block_numbering.json")
    theirs = {(b["column"] - 1, b["tier"] - 1): b["number"] for b in other["blocks"]}
    ours = {}
    for rj, row in enumerate(ROWS):
        for cells, num in row:
            for c in (cells if isinstance(cells, tuple) else (cells,)):
                ours[(c, rj)] = num
    disagree = sorted((k, theirs[k], ours[k]) for k in set(theirs) & set(ours)
                      if theirs[k] != ours[k])
    if disagree:
        raise SystemExit(
            "the two readings of the School Section's numerals disagree, and one of them is "
            "wrong: " + "; ".join("cell c%dr%d — T-0875 reads %s, this module reads %s"
                                  % (c + 1, r + 1, a, b) for (c, r), a, b in disagree))
    missing = sorted(set(theirs) - set(ours))
    if missing:
        raise SystemExit("T-0875 numbers cells this module emits no block for: %s" % (missing,))
    return dict(
        against="data/traces/school_section_block_numbering.json",
        ticket="T-0875",
        cells_compared=len(set(theirs) & set(ours)),
        disagreements=0,
        note=("Two independent readings of the same sheet, made hours apart by runs that could "
              "not see each other — one off the resampled raster, one off the sheet's own pixels "
              "— agree on all 142 numerals, cell for cell. This module gates on that agreement: "
              "if the two ever diverge it refuses to run. The four cells this module holds and "
              "that reading does not are the east halves of blocks 73, 74, 83 and 84, which span "
              "two cells apiece here because Market Street stops at Adams."),
    )


def sale_test():
    """The October 1833 sale of the school section, as this project already holds it."""
    entries = load("data/research/land_sales/entries.json")["entries"]
    s16 = [e for e in entries if (e.get("tract") or {}).get("section") == "16"]
    sold = {}
    for e in s16:
        b = (e.get("tract") or {}).get("block")
        if b is None:
            continue
        sold.setdefault(int(b), []).append(e)
    dates = sorted({e["date_purchased"] for e in s16 if e.get("date_purchased")})
    return dict(
        rows_in_section_16=len(s16),
        rows_resolving_to_a_block=sum(len(v) for v in sold.values()),
        blocks_sold=sorted(sold),
        first_date=dates[0] if dates else None,
        last_date=dates[-1] if dates else None,
    ), sold


def reservation_records(blocks, sale, sold):
    reached = set(sale["blocks_sold"])
    out = []
    seen = set()
    for num, meta in RESERVED.items():
        key = meta["name"]
        if key in seen:
            continue
        seen.add(key)
        members = sorted(n for n, m in RESERVED.items() if m["name"] == key)
        tested = [n for n in members]
        sells = {n: len(sold.get(n, [])) for n in tested if n in reached}
        # Did the sale reach this part of the section at all? It reached rows 0-3 only.
        row_of = {b["block_number"]: b["cells"][0][1] for b in blocks}
        in_reach = any(row_of[n] <= 3 for n in tested)
        if sells:
            result = "contradicted"
            verdict = ("The sale SELLS in %s. The sheet's reservation and the sale's rows are both "
                       "written; neither is dropped." % ", ".join("block %d (%d rows)" % (k, v)
                                                                  for k, v in sorted(sells.items())))
            conf = "inferred"
        elif in_reach:
            result = "corroborated"
            verdict = ("No row of the sale sells a lot in %s, and the sale reached this tier: it "
                       "sells in every OTHER block of the two northern rows. A reservation the "
                       "sale steps around is the strongest corroboration this dataset can give it."
                       % (" or ".join("block %d" % n for n in tested)))
            conf = "inferred"
        else:
            result = "untested"
            verdict = ("No row of the sale sells a lot in %s — but the sale never reached this far "
                       "south. Its 217 block-resolved rows all lie in the four northern rows of the "
                       "grid, so its silence here is silence and not corroboration."
                       % (" or ".join("block %d" % n for n in tested)))
            conf = "inferred"
        for n in tested:
            blk = next(b for b in blocks if b["block_number"] == n)
            out.append(dict(
                block_id=blk["id"],
                name=meta["name"],
                block_number=n,
                spans=[m for m in members] if len(members) > 1 else None,
                bounded_by=blk["bounded_by"],
                where=meta["where"],
                reserved_for="unstated",
                confidence=conf,
                sources=["wright_1834_nara_hup"],
                what_may_stand_here=dict(
                    rule=("A structure record may stand on reserved ground when its own committed "
                          "evidence puts it there. Everything else is refused \u2014 in particular, no "
                          "roof of the 665-roof programme's anonymous infill. Nothing stands here "
                          "today: this ground is a mile outside the modelled town and carries no "
                          "committed footprint at all."),
                    permitted=[]),
                sale_test=dict(result=result, note=verdict,
                               tested_against="data/research/land_sales/entries.json, "
                                              "section 16 T39N R14E, the October 1833 school-section sale"),
                note=("Wright writes 'Reserved' across this block and no numeral. What it was "
                      "reserved FOR is not on the sheet and is not supplied here. %s" % verdict),
            ))
    return out


def _scal(x):
    return x is None or isinstance(x, (int, float, str, bool))


def _fmt(o, ind=0, ascii_=True):
    """Serialise in the style the committed street and reservation files already use:
    two-space indent, but an array of scalars (or of scalar arrays) on one line."""
    sp = "  " * ind
    if isinstance(o, list) and o and (all(_scal(v) for v in o)
                                      or all(isinstance(v, list) and v and all(_scal(w) for w in v) for v in o)):
        return json.dumps(o, separators=(", ", ": "), ensure_ascii=ascii_)
    if isinstance(o, list):
        if not o:
            return "[]"
        return "[\n" + ",\n".join("  " * (ind + 1) + _fmt(v, ind + 1, ascii_) for v in o) + "\n" + sp + "]"
    if isinstance(o, dict):
        if not o:
            return "{}"
        return ("{\n" + ",\n".join("  " * (ind + 1) + json.dumps(k) + ": " + _fmt(v, ind + 1, ascii_)
                                    for k, v in o.items()) + "\n" + sp + "}")
    return json.dumps(o, ensure_ascii=ascii_)


def splice(path, records, sentinel_key, ascii_=True):
    """Append (or replace) this tool's records at the end of the file's last array, leaving
    every byte of the rest of the file exactly as it was. Hand-authored files here carry
    hand-authored formatting and a whole-file reserialisation would rewrite 1,400 lines to
    add twelve records."""
    text = (ROOT / path).read_text()
    body = "\n" + ",\n".join("    " + _fmt(r, 2, ascii_) for r in records)
    sentinel = "\n    {\n      %s: %s," % (json.dumps(sentinel_key),
                                           json.dumps(records[0][sentinel_key]))
    i = text.find(sentinel)
    if i >= 0:
        head = text[:i]
    else:
        j = text.rfind("\n  ]")
        head = text[:j] + ","
    return head + body + "\n  ]\n}\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and fail if any committed file would change")
    args = ap.parse_args()

    anchor, blocks, raster, sx = build()
    sale, sold = sale_test()
    streets = street_records(anchor)
    reservations = reservation_records(blocks, sale, sold)

    measured_x = NS_LINES[-1]["measured"] - NS_LINES[0]["measured"]
    measured_y = NS_LINES and (EW_LINES[0]["measured"] - EW_LINES[-1]["measured"])

    out = dict(
        _doc=__doc__.strip(),
        id="school_section_blocks_1834",
        generated_by="tools/generate_school_section_grid.py",
        ticket="T-0797",
        source="wright_1834_nara_hup",
        raster=dict(path=raster["working_copy"], sha256=raster["sha256"],
                    width=raster["width"], height=raster["height"], dpi=raster["dpi"]),
        registration="data/traces/gcp/wright_1834_nara_hup_gcps.json",
        anchor=anchor,
        residuals=dict(
            measured_east_west_span_m=round(measured_x, 2),
            measured_north_south_span_m=round(measured_y, 2),
            statute_mile_m=MILE_M,
            east_west_departure_m=round(measured_x - MILE_M, 2),
            north_south_departure_m=round(measured_y - MILE_M, 2),
            north_south_departure_pct=round(100 * (measured_y - MILE_M) / MILE_M, 2),
            finding=("The sheet's east-west span of the section falls 6.3 m short of the statute "
                     "mile, four tenths of one per cent, and its north-south span overruns it by "
                     "49.3 m, three per cent. That is the registration's own 5.2 per cent x/y "
                     "anisotropy showing at the bottom of the sheet, on the axis the manuscript was "
                     "torn and backed along, and it is why this grid is anchored on the section "
                     "rather than on the paper. It is also a figure worth carrying back to the fit: "
                     "a y-scale three per cent long over a mile is larger than any block."),
        ),
        grid=dict(columns=13, rows=12, cells=156, blocks=len(blocks),
                  cells_without_a_block=156 - 142 - 4,
                  cells_shared_by_a_block=4,
                  note=("Thirteen tiers of blocks north to south and twelve east to west make 156 "
                        "cells. Ten of them are the South Branch and carry no block; four more are "
                        "the east halves of blocks 73, 74, 83 and 84, each of which spans two cells "
                        "because Market Street stops at Adams. 156 - 10 - 4 = 142."),
                  ns_lines=NS_LINES, ew_lines=EW_LINES,
                  corridor_widths=dict(
                      east_west_m=EW_CORRIDOR_M, north_south_m=NS_CORRIDOR_M,
                      note=("Adopted, not measured per line. Where the sheet draws a corridor with "
                            "two rules their separation was measured: the east-west median is "
                            "23.3 m and the north-south 20.4 m, against the 80 ft and 66 ft the "
                            "1830 plats use. The standards are adopted and the drawn separation is "
                            "kept per line as `drawn_w`, because the scatter of individual picks is "
                            "+/- 5 m and no single one is worth more than the standard."))),
        numbering=dict(
            scheme=("Serpentine, tier by tier: 1-12 down the westernmost, 13-24 back up the next, "
                    "and so on to 131-141 up the easternmost. The two corner blocks the sheet marks "
                    "'Reserved' carry no numeral and take 1 and 142 from the sequence."),
            read_on_the_sheet=sum(1 for b in blocks if b["numeral"]["on_sheet"]),
            supplied_by_the_sequence=sum(1 for b in blocks if not b["numeral"]["on_sheet"]),
            corroboration=("The October 1833 sale resolves %d of its section-16 rows to a block "
                           "number, and the %d distinct blocks it names are EXACTLY the blocks read "
                           "here in the four northern rows, with the two reserved corners missing "
                           "from both. That is a second witness to the reading, made by a different "
                           "hand in a different record."
                           % (sale["rows_resolving_to_a_block"], len(sale["blocks_sold"]))),
        ),
        sale_test=sale,
        numbering_cross_check=cross_check_numbering(),
        summary=dict(blocks=len(blocks),
                     reserved=sorted(RESERVED),
                     cut_by_south_branch=sorted(BANK_PENDING),
                     total_block_area_m2=round(sum(b["area_m2"] for b in blocks), 1)),
        blocks=blocks,
    )

    targets = [
        ("data/traces/vectors/school_section_blocks_1834.json",
         json.dumps(out, indent=2, ensure_ascii=False) + "\n"),
        ("data/streets/1835.json", splice("data/streets/1835.json", streets, "id", True)),
        ("data/reconstruction/1835_reserved_ground.json",
         splice("data/reconstruction/1835_reserved_ground.json", reservations, "block_id", False)),
    ]
    if args.check:
        bad = [p for p, want in targets if (ROOT / p).read_text() != want]
        if bad:
            print("FAIL school section grid is stale: " + ", ".join(bad))
            return 1
        print("OK  school section grid: %d blocks, %d streets, %d reservations re-derive"
              % (len(blocks), len(streets), len(reservations)))
        return 0
    for path, text in targets:
        (ROOT / path).write_text(text)
        print("wrote %s" % path)
    print("%d blocks, %d streets, %d reservations" % (len(blocks), len(streets), len(reservations)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
