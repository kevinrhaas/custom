#!/usr/bin/env python3
"""Printed pages 47-50 of Fergus 1839: the Fort Dearborn Addition sale, and the
population table (T-0666).

`read_fergus_1839.py` read the alphabetical directory (printed 5-36) and the churches
and hotels (printed 37); `read_fergus_1839_election.py` read the charter election of
2 May 1837 (printed 40-46). These are the last four pages of the appendices, and they
are two different objects on the same sheets:

  printed 47-49 (leaves 59-61)  LOTS SOLD IN FT. DEARBORN ADDITION TO THE TOWN OF
                                CHICAGO, from the 10th to the 24th June, 1839 — the
                                Beaubien, or Reservation, lands. Block, lot, bidder
                                and amount, in four columns twice over per page.
  printed 50   (leaf 62)        POPULATION OF CHICAGO — the volume's own year-by-year
                                table, 1835 to 1876, plus two projections.

  tools/read_fergus_1839_lots.py --map      RE-DERIVE the row map from the scan (NETWORK)
  tools/read_fergus_1839_lots.py --build    write the two claims files
  tools/read_fergus_1839_lots.py --check    rebuild in memory and diff (the gate)
  tools/read_fergus_1839_lots.py --report    the reading counted, and what it could not read
  tools/read_fergus_1839_lots.py --self-test  the three judging rules, fired against breakage

WHY THERE IS A ROW MAP. Both objects are set in columns, and archive.org's OCR reads a
columned page in the order the scanner met the ink, not the order the printer set it.
The flat text of leaf 60 runs the whole left column, then the right column's numbers,
then the right column's names — so a bidder read off the committed text lands beside
somebody else's lot, and the population table's flat text puts 1863 under 1849. The
parent ticket said so and said not to read it off the flat text.

The fix is the one thing the flat text threw away: the word COORDINATES the OCR
carries. `--map` fetches `fergusdirectoryo00ferg_djvu.xml`, splits each page at its
gutter, groups words into printed ROWS by their vertical centre and into CELLS by the
column bands written out below, and commits what it found as
`data/research/directories/fergus_1839_lots_rowmap.json` — for every cell, the exact
[line, from, to] spans of the committed page text it is made of. That is the same
standing as the committed page text itself: derived from the scan by a re-runnable
rule, over the network, and therefore not in `check.sh`. What IS in `check.sh` is
`--check`, which rebuilds the claims offline out of the committed text plus the map,
and `research_domains.py --check`, which rebuilds every quote out of the committed
text through those same spans — so a span that points at the wrong ink fails the gate.

THE COLUMN BANDS ARE WRITTEN OUT, NOT SNIFFED. Six half-pages, six lines of table.
The three sheets are set at three different offsets across the page and a rule that
found the columns for one found the running head for another; T-0664 wrote its line
map out by eye for the same reason, and this is that map one step less by eye.

WHAT DATE THIS IS. The sale ran 10-24 June 1839, so every lot claim carries
`describes_date: "1839-06"` and NOT 1835. These are the Fort Dearborn reservation
lands, which in 1835 were the garrison's and were not lots at all: the ground is south
and east of the river mouth and the plat is four years after the scene date. A bidder
here is a name that MAY corroborate a man in the town and never mints one, and nothing
in this file mints or regrades anybody. The population table's rows each carry the
year the FIGURE describes, which for the first row is 1835.

THE COMPILER'S WARNING BINDS THESE PAGES TOO. Printed page 3: the volume is Fergus's
1876 completion, out of Old Settlers' recollections, of a list he set up from memory
in 1839. The sale list reads like a clerk's abstract and may well be one, but this
reading cannot show that it is, so it is graded as everything else in the volume is.

WHAT IT REFUSES TO READ. A great many of the numerals in this table are destroyed in
the scan — lot 33 prints as `'l ">` over two lines, $303 as `3°3` and `jjj`, $511 as
`51 1`, and printed page 49's left-hand lot column collapses after two lines into a
smear of rotated type (`<J\\Ui`, `00^1`, `In)`). Every such cell is committed with its value NULL and
its ink kept verbatim in `as_printed`, never guessed from the run it sits in. The
sequence would usually give it away, and a number recovered from its neighbours is an
inference wearing a reading's clothes; T-0670 is the ticket for settling them off the
page images, where they can be READ.
"""
import json, os, re, statistics, sys, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = os.path.join(ROOT, "data/research/directories")
TEXT = os.path.join(DOMAIN, "text")
MAP = os.path.join(DOMAIN, "fergus_1839_lots_rowmap.json")
LOTS_OUT = os.path.join(DOMAIN, "claims/fergus_1839_ft_dearborn_lots.json")
POP_OUT = os.path.join(DOMAIN, "claims/fergus_1839_population.json")
COVERAGE = os.path.join(DOMAIN, "coverage.json")

ITEM = "fergusdirectoryo00ferg"
URL = "https://archive.org/download/%s/%s_djvu.xml" % (ITEM, ITEM)
LEAF_TO_PRINTED = -12
SOURCE_ID = "fergus_chicago_directory_1839"

# THE COLUMN BANDS, by leaf and half. `gutter` is the x that divides the page's two
# halves; within a half, a word's LEFT EDGE decides its cell: below `block` it is the
# block number, below `lot` the lot number, below `bidder` the bidder, and anything
# further right is the amount. Read off the word coordinates of these three pages and
# written out here because the three sheets do not share an offset.
BANDS = {
    #  leaf  gutter  half   block   lot   bidder(→amount beyond)
    (59, "L"): dict(lo=0,    hi=1040, block=320,  lot=390,  bidder=860),
    (59, "R"): dict(lo=1040, hi=9999, block=1075, lot=1145, bidder=1600),
    (60, "L"): dict(lo=0,    hi=1230, block=530,  lot=600,  bidder=1100),
    (60, "R"): dict(lo=1230, hi=9999, block=1275, lot=1350, bidder=1850),
    (61, "L"): dict(lo=0,    hi=1030, block=375,  lot=420,  bidder=900),
    (61, "R"): dict(lo=1030, hi=9999, block=1100, lot=1160, bidder=1700),
}
# The population table, printed page 50, is TWO pairs of columns per half.
POP_BANDS = [
    dict(lo=430,  hi=900,  year=600,  first=1835),   # 1835-1848
    dict(lo=1000, hi=1500, year=1200, first=1849),   # 1849-1862
    dict(lo=1550, hi=1990, year=1700, first=1863),   # 1863-1876
]
POP_LEAF = 62
LOT_LEAVES = (59, 60, 61)
# Rows on a page are set about 55 px apart and a cell stands about 40 px tall, so two
# words belong to the same printed row when their vertical centres are within this.
ROW_PX = 34
# The tight first pass. No printed row on these pages sets two of its own cells more
# than this far apart vertically; every gathering past it has to earn its way back.
TIGHT_PX = 12
# The header band of each page: the running head, the title block and the column
# heads. Everything above this y on a lot page is not a row of the table.
TABLE_TOP = {59: 1340, 60: 380, 61: 370, 62: 400}

RESERVED = re.compile(r"reserved|forfeited", re.I)
# A bidder cell is a NAME when it carries a word of three or more letters — every
# surname on these three pages does, and no ditto mark does. Everything else in the
# bidder column is the printer's ditto (`II`, `11`, `It`, `»`, `„`, `"`, `-`) or the
# scan's ruin of one, and it means the name above it.
NAME = re.compile(r"[A-Za-z]{3}")
INT = re.compile(r"^\$?([0-9][0-9,]*)$")


# ---------------------------------------------------------------- the scan (network)

def header_like(line: str) -> bool:
    """fetch_fergus_1839_pages.py's running-head test, verbatim — one definition."""
    s = line.strip()
    if not s or len(s) > 45:
        return False
    if len(s) <= 3:
        return True
    letters = [c for c in s if c.isalpha()]
    return not letters or sum(c.isupper() for c in letters) / len(letters) > 0.7


def page_words(page):
    """Every word of a page as (x0, ycentre, text, line_index, char_from, char_to).

    The line index and the character offsets are into the COMMITTED page text, and
    they are computed by replaying `fetch_fergus_1839_pages.py`'s renderer rather
    than by searching the text for the word — a page with `II` on forty lines cannot
    be searched, only replayed.
    """
    raw = []
    for line in page.iter("LINE"):
        ws = line.findall("WORD")
        if ws:
            raw.append(ws)
    lefts = [int(ws[0].get("coords").split(",")[0]) for ws in raw]
    if not lefts:
        return []
    median = statistics.median(lefts)
    out, head = [], True
    for idx, ws in enumerate(raw):
        text = " ".join((w.text or "") for w in ws)
        prefix = 0
        if head and header_like(text):
            pass
        else:
            head = False
            if lefts[idx] - median > 25:
                prefix = 2
        at = prefix
        for w in ws:
            body = w.text or ""
            x0, y1, x1, y0 = [int(v) for v in w.get("coords").split(",")]
            if body.strip():
                out.append((x0, (y0 + y1) // 2, body, idx + 1, at, at + len(body)))
            at += len(body) + 1
    return out


def rows_of(words, band, names, top):
    """The words of one column-half, gathered into the rows the printer set.

    Grouping by vertical centre alone does not work on printed page 49, whose lines
    are set tight enough that two of them fall inside one row's tolerance: the OCR
    boxes of `S. N. Dexter  305` and `B. McDonald  331` overlap, and a single pass
    welds them into one row bidding $305331. So the gathering is done twice. First a
    TIGHT pass, at a threshold no printed row can straddle, which over-splits every
    row into its cells; then adjacent groups are merged back while they can be — and
    two groups can be merged only when they COLLIDE IN NO COLUMN. Two printed rows
    both carry a bidder and both carry an amount, so they collide and stay apart; the
    three fragments of one printed row land in three different columns and rejoin.
    """
    sel = sorted([w for w in words if band["lo"] <= w[0] < band["hi"] and w[1] >= top],
                 key=lambda w: (w[1], w[0]))
    tight = []
    for w in sel:
        if tight and w[1] - tight[-1][-1][1] <= TIGHT_PX:
            tight[-1].append(w)
        else:
            tight.append([w])

    def columns(group):
        return {c for c, ws in cells_of(group, band, names).items() if ws}

    rows = []
    for group in tight:
        cols = columns(group)
        if rows and group[0][1] - rows[-1][0][-1][1] <= ROW_PX and not (cols & rows[-1][1]):
            rows[-1][0].extend(group)
            rows[-1][1] |= cols
        else:
            rows.append([list(group), cols])
    return [sorted(r[0], key=lambda w: w[0]) for r in rows]


def cells_of(row, band, names):
    """Split one row into its named cells on the band's left-edge thresholds."""
    out = {n: [] for n in names}
    out[names[-1] + "_beyond"] = []
    for w in row:
        for n in names:
            if w[0] < band[n]:
                out[n].append(w)
                break
        else:
            out[names[-1] + "_beyond"].append(w)
    return out


def spans_of(ws):
    """The committed-text spans a cell's words occupy, merged where they adjoin."""
    out = []
    for x0, y, body, line, a, b in sorted(ws, key=lambda w: (w[3], w[4])):
        if out and out[-1]["line"] == line and out[-1]["to"] + 1 == a:
            out[-1]["to"] = b
        else:
            out.append({"line": line, "from": a, "to": b})
    return out


def build_map(xml_path=None):
    data = open(xml_path, "rb").read() if xml_path else \
        urllib.request.urlopen(URL, timeout=240).read()
    pages = ET.fromstring(data).findall(".//OBJECT")
    doc = {"schema": 1,
           "_doc": "GENERATED by tools/read_fergus_1839_lots.py --map, over the network, "
                   "out of the word coordinates of %s_djvu.xml. Every cell names the "
                   "[line, from, to] spans of the committed page text it is made of, so "
                   "the reading built from it is rebuilt and checked OFFLINE. Hand-edit "
                   "and --check says so." % ITEM,
           "generated_by": "tools/read_fergus_1839_lots.py --map",
           "item": ITEM, "lots": [], "population": []}
    for leaf in LOT_LEAVES:
        words = page_words(pages[leaf - 1])
        for half in ("L", "R"):
            band = BANDS[(leaf, half)]
            for row in rows_of(words, band, ["block", "lot", "bidder"], TABLE_TOP[leaf]):
                cells = cells_of(row, band, ["block", "lot", "bidder"])
                amount = cells.pop("bidder_beyond", [])
                doc["lots"].append({
                    "leaf": leaf, "half": half, "y": row[0][1],
                    "block": spans_of(cells["block"]), "lot": spans_of(cells["lot"]),
                    "bidder": spans_of(cells["bidder"]), "amount": spans_of(amount)})
    words = page_words(pages[POP_LEAF - 1])
    for band in POP_BANDS:
        for row in rows_of(words, band, ["year"], TABLE_TOP[POP_LEAF]):
            cells = cells_of(row, band, ["year"])
            figure = cells.pop("year_beyond", [])
            doc["population"].append({
                "leaf": POP_LEAF, "y": row[0][1], "column_first_year": band["first"],
                "year": spans_of(cells["year"]), "figure": spans_of(figure)})
    return doc


# ------------------------------------------------------------------ the reading

def leaf_text(leaf):
    with open(os.path.join(TEXT, "fergus_1839_leaf_%03d.txt" % leaf), encoding="utf-8") as fh:
        return fh.read().splitlines()


def ink(lines, spans):
    """The verbatim ink of a cell, out of the committed text, exactly as its spans cut it."""
    return "\n".join(lines[s["line"] - 1][s["from"]:s["to"]] for s in spans)


def flat(text):
    return re.sub(r"\s+", " ", text).strip()


def as_int(text):
    m = INT.match(flat(text).replace(" ", ""))
    if not m:
        return None
    try:
        return int(m.group(1).replace(",", ""))
    except ValueError:
        return None


def reads_as_ditto(bidder_ink: str, amount_ink: str) -> bool:
    """A MARK IN THE BIDDER COLUMN IS A DITTO ONLY WHERE A PRICE IS PRINTED.

    The printer's brace, which gathers the reserved lots of a block, breaks into the
    same one- and two-character wreckage the ditto does — a paren, a semicolon, a
    `J`, a backslash, a `1`, an `II` — and reading a brace as a ditto hands the man
    above somebody else's lot. A
    lot that sold has an amount printed against it and a lot held back has none, so
    INK in the amount column is what separates them. Ink, not a readable number:
    twenty-two of these prices are wreckage too, and `45o` is still a price.
    """
    if not bidder_ink.strip() or RESERVED.search(bidder_ink) or NAME.search(bidder_ink):
        return False
    return bool(amount_ink.strip())


def carry_block(block, lot, last_block, last_lot):
    """THE BLOCK IS CARRIED, AND SAYS SO. Returns (block, carried, last_block, last_lot).

    A block number is printed once, against the first lot of its run, and governs
    until the next one. Carrying it is an inference and it is flagged on every row
    that takes it. It is carried only while the lot numbers keep RISING: a lot that
    restarts is a new block whose number the scan lost, and the run stops there
    rather than lending block 10 to blocks 11 and 12 the way printed page 49's ruined
    lot column would invite.
    """
    if block is not None:
        return block, False, block, lot if lot is not None else 0
    if last_block is not None and (lot is None or lot > last_lot):
        return last_block, True, last_block, lot if lot is not None else last_lot
    if lot is not None:
        return None, False, None, None
    return None, False, last_block, last_lot


def build():
    texts = {leaf: leaf_text(leaf) for leaf in LOT_LEAVES + (POP_LEAF,)}
    rowmap = json.loads(open(MAP, encoding="utf-8").read())

    # PASS 1 — the ink of every mapped row, and the WRAPPED NAMES folded back into the
    # row above. A bidder too long for the column is set on a second line, and the OCR
    # gives that line a row of its own: `T. Church and H.` on one, `O. Stone` and the
    # price on the next. A row whose block AND lot cells are empty — not destroyed,
    # EMPTY — carrying a name under a row that has a lot and no price is that second
    # line, and it is folded back rather than shipped as a bidder of its own.
    raw = []
    for row in rowmap["lots"]:
        lines = texts[row["leaf"]]
        cell = {k: ink(lines, row[k]) for k in ("block", "lot", "bidder", "amount")}
        if not any(v.strip() for v in cell.values()):
            continue
        cell["_spans"] = row["block"] + row["lot"] + row["bidder"] + row["amount"]
        cell["_leaf"], cell["_half"] = row["leaf"], row["half"]
        wrapped = (raw and not cell["block"].strip() and not cell["lot"].strip()
                   and NAME.search(cell["bidder"]) and not RESERVED.search(cell["bidder"])
                   and raw[-1]["_leaf"] == row["leaf"] and raw[-1]["_half"] == row["half"]
                   and raw[-1]["lot"].strip() and not raw[-1]["amount"].strip())
        if wrapped:
            prev = raw[-1]
            prev["bidder"] = (prev["bidder"] + "\n" + cell["bidder"]).strip("\n")
            prev["amount"] = (prev["amount"] + "\n" + cell["amount"]).strip("\n")
            prev["_spans"] = prev["_spans"] + cell["_spans"]
            prev["_wrapped"] = True
            continue
        raw.append(cell)

    lots, n, last_bidder, last_block, last_lot = [], 0, None, None, None
    illegible = {"lot": 0, "amount": 0, "block": 0}
    for cell in raw:
        quote = "\n".join(v for v in (cell["block"], cell["lot"], cell["bidder"],
                                      cell["amount"]) if v)
        spans = cell["_spans"]
        block, lot = as_int(cell["block"]), as_int(cell["lot"])
        if lot == 0:
            lot = None
        amount = as_int(cell["amount"])
        withheld = RESERVED.search(cell["bidder"])
        named = bool(NAME.search(cell["bidder"])) and not withheld
        ditto = reads_as_ditto(cell["bidder"], cell["amount"])
        if named:
            last_bidder = re.sub(r"\s+[.,]$", "",
                                 flat(cell["bidder"].replace("\n", " "))).rstrip(",")
        if cell["block"].strip() and block is None:
            illegible["block"] += 1
        if cell["lot"].strip() and lot is None:
            illegible["lot"] += 1
        if cell["amount"].strip() and amount is None:
            illegible["amount"] += 1
        block, carried, last_block, last_lot = carry_block(block, lot, last_block, last_lot)
        n += 1
        bidder = last_bidder if (named or ditto) else None
        lots.append({
            "id": "f1839_lot%04d" % n,
            "kind": "person" if bidder else "civic",
            "reading": "transcription_mediated",
            "quote": quote,
            "normalized": {
                "as_printed": {k: flat(v) or None for k, v in cell.items()
                               if not k.startswith("_")},
                "bidder": bidder,
                "bidder_ditto": ditto,
                "bidder_wrapped": bool(cell.get("_wrapped")),
                "block": block,
                "block_carried": carried,
                "lot": lot,
                "amount_usd": amount,
                "withheld_from_sale": withheld.group(0).lower() if withheld else None,
                "addition": "Fort Dearborn Addition to the Town of Chicago",
            },
            "locator": {
                "text_file": "fergus_1839_leaf_%03d.txt" % cell["_leaf"],
                "spans": spans,
                "lines": [min(s["line"] for s in spans), max(s["line"] for s in spans)],
                "page": "fergus_1839_leaf_%03d" % cell["_leaf"],
                "printed_page": cell["_leaf"] + LEAF_TO_PRINTED,
                "column": cell["_half"],
            },
            "describes_date": "1839-06",
            "entities": [bidder] if bidder else [],
            "town_finding": False,
            "notes": None,
        })

    pop, m, unread = [], 0, []
    for row in rowmap["population"]:
        lines = texts[POP_LEAF]
        year_ink, figure_ink = ink(lines, row["year"]), ink(lines, row["figure"])
        year = as_int(re.sub(r"[.\s]+$", "", flat(year_ink)))
        if year is None or not (1835 <= year <= 1876):
            if year_ink.strip() and figure_ink.strip():
                unread.append(flat(year_ink + " " + figure_ink))
            continue
        m += 1
        figure = as_int(figure_ink.replace(".", ""))
        spans = row["year"] + row["figure"]
        pop.append({
            "id": "f1839_pop%02d" % m,
            "kind": "civic",
            "reading": "transcription_mediated",
            "quote": "\n".join(v for v in (year_ink, figure_ink) if v),
            "normalized": {
                "as_printed": {"year": flat(year_ink) or None,
                               "figure": flat(figure_ink) or None},
                "year": year,
                "population": figure,
                "of": "Chicago",
                "column_reconstructed": True,
            },
            "locator": {
                "text_file": "fergus_1839_leaf_%03d.txt" % POP_LEAF,
                "spans": spans,
                "lines": [min(s["line"] for s in spans), max(s["line"] for s in spans)],
                "page": "fergus_1839_leaf_%03d" % POP_LEAF,
                "printed_page": POP_LEAF + LEAF_TO_PRINTED,
            },
            "describes_date": "%d" % year,
            "entities": [],
            "town_finding": True,
            "notes": None if figure is not None else
                     "the figure is destroyed in the scan and is left null rather than "
                     "recovered from the run it sits in",
        })

    corpus = {
        "item": ITEM,
        "url": "https://archive.org/details/%s" % ITEM,
        "what": "Allen County Public Library Genealogy Center scan of Robert Fergus, "
                "Fergus' Directory of the City of Chicago, 1839 (Chicago: Fergus Printing "
                "Company, 1876). 86 leaves. Printed pages 47-50 are leaves 59-62.",
        "committed": True,
        "how": "tools/fetch_fergus_1839_pages.py commits the page text; "
               "tools/read_fergus_1839_lots.py --map commits the row map that puts the "
               "columns back in printed order, out of the same scan's word coordinates.",
    }
    lots_doc = {
        "schema": 1,
        "_doc": "GENERATED by tools/read_fergus_1839_lots.py --build out of the committed "
                "page text in data/research/directories/text/ and the committed row map "
                "beside it. Hand-edit and --check says so. Fergus' Directory of the City of "
                "Chicago, 1839, printed pages 47-49: LOTS SOLD IN FT. DEARBORN ADDITION TO "
                "THE TOWN OF CHICAGO, from the 10th to the 24th June, 1839, inclusive — "
                "known as the Beaubien, or Reservation, lands. One claim per printed row: "
                "block, lot, bidder and amount.",
        "generated_by": "tools/read_fergus_1839_lots.py --build",
        "source_id": SOURCE_ID,
        "corpus": corpus,
        "reading_note": "transcription_mediated throughout: archive.org's OCR of the printed "
                        "page, machine-read and not checked against the image by eye. The "
                        "damage is left in every cell on purpose — a tidied cell cannot be "
                        "found again on the page. The columns are the hazard here rather "
                        "than the spelling: the OCR reads a four-column table in the order "
                        "the scanner met the ink, so the printed rows are put back from the "
                        "word coordinates by --map and every cell carries the spans of the "
                        "committed text it is made of. A numeral the scan destroyed is NULL "
                        "and its ink is kept in as_printed; it is never recovered from the "
                        "run it sits in. T-0670 owns settling those off the page images.",
        "date_note": "1839, NOT 1835. The sale ran 10-24 June 1839 and every claim carries "
                     "describes_date 1839-06. This ground is the Fort Dearborn reservation, "
                     "which in July 1835 was the garrison's and was not lots at all, so no "
                     "row here places anybody in the scene. A bidder is a name that MAY "
                     "corroborate a man in the town; under the ratified grading ladder a "
                     "later appearance alone never makes an 1835 resident, and nothing in "
                     "this file mints or regrades anybody.",
        "compiler_note": "Printed page 3, already recorded in data/sources/%s.json: the "
                         "volume is Fergus's 1876 completion, out of Old Settlers' "
                         "recollections, of a list he set up from memory in 1839. This list "
                         "reads like a clerk's abstract of the sale and may well be one; "
                         "this reading cannot show that it is, so it is graded as the rest "
                         "of the volume is." % SOURCE_ID,
        "ditto_note": "The printer sets a repeated bidder as a ditto mark, and the scan "
                      "ruins it into II, 11, It, », „ and a dozen more. A bidder cell with "
                      "no word of three or more letters is read as a ditto and carries the "
                      "name above it with bidder_ditto true — the mark IS the printer "
                      "saying the same name, so the name is not an inference, but which "
                      "mark it was is not recoverable and the ink is kept in as_printed.",
        "counts": {
            "claims": len(lots),
            "rows": n,
            "bidders_named": len({c["normalized"]["bidder"] for c in lots
                                  if c["normalized"]["bidder"]}),
            "rows_with_a_lot_number": sum(1 for c in lots if c["normalized"]["lot"] is not None),
            "rows_with_an_amount": sum(1 for c in lots
                                       if c["normalized"]["amount_usd"] is not None),
            "cells_the_scan_destroyed": illegible,
            "aggregate_printed_usd": 100000,
        },
        "claims": lots,
    }
    pop_doc = {
        "schema": 1,
        "_doc": "GENERATED by tools/read_fergus_1839_lots.py --build. Hand-edit and --check "
                "says so. Fergus' Directory of the City of Chicago, 1839, printed page 50: "
                "POPULATION OF CHICAGO, the volume's own year-by-year table.",
        "generated_by": "tools/read_fergus_1839_lots.py --build",
        "source_id": SOURCE_ID,
        "corpus": corpus,
        "reading_note": "transcription_mediated. THE PAIRING IS RECONSTRUCTED AND SAYS SO. "
                        "The table is set as three pairs of year-and-figure columns and the "
                        "OCR interleaves them — its flat text puts 1863 under 1849 and "
                        "strands the last column's figures — so no row here is read off the "
                        "committed text in reading order. Each row is put back from the word "
                        "coordinates: a year and a figure are one row when their vertical "
                        "centres agree inside 28 px within one pair of columns, and every "
                        "claim carries column_reconstructed true. Fourteen figures in the "
                        "1863-1876 column are swallowed by the leader dots and are NULL. ONE ROW IS "
                        "MISSING ENTIRELY, and it is named in counts rather than left as a "
                        "silent gap: the 1840 line is printed `1 S40 .... 4,47!*` in this "
                        "scan and neither its year nor its figure can be read, so there is "
                        "no 1840 claim here at all. The census of 1840 is held elsewhere in "
                        "this repo and is not borrowed to fill it.",
        "date_note": "Each claim's describes_date is the year the FIGURE describes, not the "
                     "year of the volume. The first row is the one this project wants: "
                     "Fergus prints Chicago's 1835 population as 3,265.",
        "projection_note": "The table's last two lines are not counts and are not read here: "
                           "1885 estimated by Jno S. Wright at 1,000,000 and 1911 estimated "
                           "by J. X. Balestier at 2,000,000. They are projections printed in "
                           "1876 and belong with the volume's rhetoric, which follows them on "
                           "the same page.",
        "counts": {"claims": len(pop),
                   "years": [c["normalized"]["year"] for c in pop],
                   "figures_read": sum(1 for c in pop if c["normalized"]["population"] is not None),
                   "figures_the_scan_destroyed": sum(1 for c in pop
                                                     if c["normalized"]["population"] is None),
                   "rows_whose_year_the_scan_destroyed": unread},
        "claims": pop,
    }
    return lots_doc, pop_doc


def write(path, doc):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def self_test() -> int:
    """The three rules that do this reading's judging, fired against cases that break them.

    Every one of them is a rule about what NOT to write down, which is the kind that
    fails silently: a brace read as a ditto, a block lent to its neighbour and a
    numeral recovered from its run all produce a fuller-looking file, and nothing else
    in check.sh would notice.
    """
    bad = []

    def want(got, expect, what):
        if got != expect:
            bad.append("%s: expected %r, got %r" % (what, expect, got))

    # 1. the ditto, and the brace that looks exactly like one
    want(reads_as_ditto("II", "211"), True, "a ditto with a price is a ditto")
    want(reads_as_ditto("II", "45o"), True, "a ditto with a RUINED price is still a ditto")
    want(reads_as_ditto(")", ""), False, "a brace with no price is not a ditto")
    want(reads_as_ditto("J", ""), False, "a brace leg with no price is not a ditto")
    want(reads_as_ditto("A. Bronson,", "303"), False, "a name is not a ditto")
    want(reads_as_ditto("' Reserved.", ""), False, "a withheld lot is not a ditto")
    want(reads_as_ditto("", "211"), False, "a price with no mark at all invents no bidder")

    # 2. the block, carried only while the lots rise
    want(carry_block(4, 1, None, None), (4, False, 4, 1), "a printed block is not carried")
    want(carry_block(None, 2, 4, 1), (4, True, 4, 2), "a rising lot carries its block")
    want(carry_block(None, 1, 4, 22), (None, False, None, None),
         "a lot that restarts ends the run rather than lending block 4 to block 5")
    want(carry_block(None, None, 4, 3), (4, True, 4, 3),
         "a row whose lot the scan destroyed stays inside the run it sits in")
    want(carry_block(None, 3, None, None), (None, False, None, None),
         "no run, no block")

    # 3. the numerals, refused rather than repaired
    want(as_int("3\u00b03"), None, "$303 printed as 3\u00b03 is not read as 33")
    want(as_int("jjj"), None, "a destroyed price is not read")
    want(as_int("51 1"), 511, "a price the OCR broke into two words rejoins — the "
         "CELL is the unit of a reading here, and both halves are its own ink")
    want(as_int("$2657"), 2657, "a clean price is read")
    want(as_int("1,557"), 1557, "a clean price with a comma is read")

    # 4. and the three of them, on the committed reading itself
    lots, pop = build()
    by_id = {c["id"]: c for c in lots["claims"]}
    block4 = [c for c in lots["claims"] if c["normalized"]["block"] == 4
              and c["locator"]["printed_page"] == 47]
    braced = [c for c in block4 if (c["normalized"]["lot"] or 99) <= 6]
    want(bool(braced), True, "printed page 47 still has block 4's braced lots")
    want([c["normalized"]["bidder"] for c in braced], [None] * len(braced),
         "the brace over block 4's first six lots gives nobody a lot")
    p49 = [c for c in lots["claims"] if c["locator"]["printed_page"] == 49
           and c["locator"]["column"] == "L"]
    want(bool(p49), True, "printed page 49's left half is still read")
    smeared = [c for c in p49 if (c["normalized"]["as_printed"]["lot"] or "") in
               ("<J\\Ui", "00^1", "'O", "In)", "Oo", "4-", "Qn^i")]
    want(len(smeared) >= 6, True,
         "printed page 49's rotated lot column is still in the reading, as ink")
    want({c["normalized"]["lot"] for c in smeared}, {None},
         "and not one of those numerals is recovered from the run it sits in")
    want({c["normalized"]["block"] for c in smeared}, {None},
         "nor is a block lent to them off the page before")
    want(any(c["normalized"]["bidder_ditto"] for c in lots["claims"]), True,
         "the dittoed rows are still read")
    want(1835 in [c["normalized"]["year"] for c in pop["claims"]], True,
         "the population table still opens on 1835")
    want([c["normalized"]["population"] for c in pop["claims"]
          if c["normalized"]["year"] == 1835], [3265],
         "and Fergus still prints 3,265 against it")
    want([c["normalized"]["year"] for c in pop["claims"] if c["normalized"]["year"] == 1840],
         [], "the 1840 line, whose year and figure are both destroyed, is not invented")
    del by_id

    if bad:
        print("fergus 1839 lots self-test: " + "; ".join(bad), file=sys.stderr)
        return 1
    print("fergus 1839 lots: the ditto, the carried block and the refused numeral all fire")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    if "--map" in sys.argv:
        local = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--from=")), None)
        doc = build_map(local)
        write(MAP, doc)
        print("row map: %d lot rows, %d population rows" % (len(doc["lots"]), len(doc["population"])))
        return 0
    lots_doc, pop_doc = build()
    if "--build" in sys.argv:
        write(LOTS_OUT, lots_doc)
        write(POP_OUT, pop_doc)
        print("  wrote %d lot claims and %d population claims"
              % (len(lots_doc["claims"]), len(pop_doc["claims"])))
        return 0
    if "--report" in sys.argv:
        c = lots_doc["counts"]
        print("FT. DEARBORN ADDITION, 10-24 June 1839 — printed pages 47-49")
        print("  %d printed rows, %d named bidders" % (c["rows"], c["bidders_named"]))
        print("  lot number read on %d rows, amount read on %d" %
              (c["rows_with_a_lot_number"], c["rows_with_an_amount"]))
        print("  cells the scan destroyed: %s" % c["cells_the_scan_destroyed"])
        for claim in lots_doc["claims"]:
            nz = claim["normalized"]
            print("   bk %-4s lot %-4s %-28s %s" % (
                nz["block"] if nz["block"] is not None else "?",
                nz["lot"] if nz["lot"] is not None else "?",
                (nz["bidder"] or nz["withheld_from_sale"] or "?")[:28],
                "$%s" % nz["amount_usd"] if nz["amount_usd"] is not None
                else "(%s)" % (nz["as_printed"]["amount"] or "-")))
        print("POPULATION OF CHICAGO — printed page 50")
        for claim in pop_doc["claims"]:
            nz = claim["normalized"]
            print("   %d  %s" % (nz["year"], nz["population"] if nz["population"] is not None
                                 else "(%s)" % nz["as_printed"]["figure"]))
        return 0
    bad = []
    for path, doc in ((LOTS_OUT, lots_doc), (POP_OUT, pop_doc)):
        if not os.path.exists(path):
            bad.append("%s is not committed" % os.path.basename(path))
        elif json.loads(open(path, encoding="utf-8").read()) != doc:
            bad.append("%s no longer rebuilds out of the committed text and row map"
                       % os.path.basename(path))
    if bad:
        print("fergus 1839 lots: " + "; ".join(bad), file=sys.stderr)
        return 1
    print("fergus 1839 printed 47-50: %d lot claims and %d population claims rebuild"
          % (len(lots_doc["claims"]), len(pop_doc["claims"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
