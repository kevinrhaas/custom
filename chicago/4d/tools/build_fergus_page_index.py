#!/usr/bin/env python3
"""Page boundaries for the committed text of Fergus' Historical Series Nos. 26-29.

    tools/build_fergus_page_index.py --build   re-derive the text and the index
    tools/build_fergus_page_index.py --check   the gate (committed files only)
    tools/build_fergus_page_index.py --self-test

WHY THIS FILE EXISTS, AND WHY IT IS NOT build_book_page_index.py. That tool solves
a hard problem: Hubbard's committed text is Internet Archive djvu output with NO
page breaks in it at all, so the leaf boundaries have to be carried across from a
second artifact by a difflib alignment, and 1 leaf of 208 could not be placed.

The Fergus deposit has no such problem and deserves no such machinery. What was
deposited at `chicago/reference/fergus/` is the Internet Archive's hOCR search
text TOGETHER WITH ITS OWN PAGE INDEX — `fergushistorical2629unse_hocr_pageindex
.json`, a list of `[text_start, text_end, hocr_start, hocr_end]`, one entry per
scanned leaf, whose first two numbers are exact character offsets into the search
text. The boundaries are therefore not derived, not aligned and not disputable:
they are the scanner's own, read straight off the deposit. This file's whole job
is to turn those character offsets into the 1-based LINE numbers a claim's locator
cites, and to say which of the four Fergus numbers each leaf belongs to.

WHAT IS MECHANICAL AND WHAT IS READ.

  leaf          mechanical. The scan's sheet number, 1-based, 858 of them.
  char/line     mechanical, from the deposit's own index.
  part          READ. The four title pages were read off the scan and are named in
                PARTS below with the leaf each was read on; every leaf between two
                title pages belongs to the earlier one. Nothing else decides it.
  printed_page  READ where the OCR of the running head gives a folio, and carried
                by the constant leaf-to-folio offset elsewhere. The offset is NOT
                constant over a part — an inserted plate shifts it — so the read
                folios are grouped into RUNS of a single offset, a run is filled
                only inside its own leaf span, and a leaf between two runs keeps
                `printed_page: null`. A folio read that contradicts every run is
                discarded and counted, not written: `1 843` in the directory's own
                running head is a year and would otherwise be read as a folio.

The text this indexes is the deposit search text COPIED BYTE FOR BYTE. It is not
cleaned, not re-flowed and not re-OCR'd: `tools/research_domains.py --check`
rebuilds every quote out of it line by line, so a single edit here would silently
invalidate every quote in the domain. --check re-asserts the copy by sha256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent            # chicago/4d
REPO = ROOT.parent.parent                                # the custom checkout
DEPOSIT = REPO / "chicago" / "reference" / "fergus"
SEARCHTEXT = DEPOSIT / "fergushistorical2629unse_hocr_searchtext"
PAGEINDEX = DEPOSIT / "fergushistorical2629unse_hocr_pageindex.json"

BOOKS = ROOT / "data" / "research" / "books"
TEXT = BOOKS / "text" / "fergus_26_29.txt"
INDEX = BOOKS / "page_index" / "fergus_26_29.json"

# READ OFF THE SCAN, and the only judgement in this file. Each entry is the leaf
# the number's own title page stands on and the title as that page prints it.
PARTS = [
    {"key": "front", "leaf": 1,
     "title": "Library plate, Internet Archive statement and the volume's collective "
              "title-page 'FERGUS' HISTORICAL SERIES No. 26-29' (leaf 10)"},
    {"key": "fergus_26", "leaf": 16,
     "title": "Fergus' Historical Series No. 26 — A Discourse on the Aborigines of the "
              "Ohio Valley, by William Henry Harrison, with the Manners and Customs "
              "matter printed after it"},
    {"key": "fergus_27", "leaf": 204,
     "title": "Fergus' Historical Series No. 27 — The Illinois and Indiana Indians, by "
              "Hiram W. Beckwith (title page leaf 208)"},
    {"key": "fergus_28", "leaf": 396,
     "title": "Fergus' Historical Series No. 28 — Directory of the City of Chicago, "
              "Illinois, for 1843, compiled by Robert Fergus (title page leaf 400)"},
    {"key": "fergus_29", "leaf": 646,
     "title": "Fergus' Historical Series No. 29 — Biographical Sketch of Joseph Duncan, "
              "Fifth Governor of Illinois, by Julia Duncan Kirby (title page leaf 658)"},
]

FOLIO_RUN_MIN = 4          # a run of fewer read folios than this is not a run


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_deposit():
    raw = SEARCHTEXT.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    spans = json.loads(PAGEINDEX.read_text(encoding="utf-8"))
    return raw, text, spans


def line_starts(text: str) -> list:
    """Character offset of the start of every 1-based line."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def line_of(starts: list, offset: int) -> int:
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


DIGIT_FIX = str.maketrans({"l": "1", "I": "1", "i": "1", "O": "0", "o": "0", "S": "5"})


def read_folio(page_text: str):
    """The folio the running head prints, or None. Verso leads, recto trails."""
    for line in page_text.splitlines():
        line = line.strip()
        if len(line) < 6:
            continue
        m = re.match(r"^([0-9lIiOoS]{1,3})[ .,]+[A-Z]", line)
        if m:
            try:
                return int(m.group(1).translate(DIGIT_FIX))
            except ValueError:
                return None
        m = re.search(r"[A-Za-z.,:;'’]\s+([0-9lIiOoS]{1,3})\s*$", line)
        if m:
            try:
                return int(m.group(1).translate(DIGIT_FIX))
            except ValueError:
                return None
        return None
    return None


def folio_runs(reads: list):
    """Group (leaf, folio) reads into runs of one constant leaf-folio offset.

    A run is {offset, first_leaf, last_leaf, reads}; an offset shared by fewer than
    FOLIO_RUN_MIN reads is not a run at all, and every read the surviving runs
    contradict is discarded by the caller, which is where the assignment is made.
    """
    by_offset = {}
    for leaf, folio in reads:
        by_offset.setdefault(leaf - 2 * folio, []).append(leaf)
    runs = []
    for offset, leaves in by_offset.items():
        if len(leaves) < FOLIO_RUN_MIN:
            continue
        runs.append({"offset": offset, "first_leaf": min(leaves),
                     "last_leaf": max(leaves), "reads": len(leaves)})
    runs.sort(key=lambda r: r["first_leaf"])
    return runs


def build_pages(text: str, spans: list):
    starts = line_starts(text)
    # The final newline opens a line number the file does not have; a leaf that ends
    # on it is clamped back onto the last real line.
    part_of = {}
    for i, part in enumerate(PARTS):
        end = PARTS[i + 1]["leaf"] - 1 if i + 1 < len(PARTS) else len(spans)
        for leaf in range(part["leaf"], end + 1):
            part_of[leaf] = part["key"]

    n_lines = len(text.splitlines())
    raw_pages = []
    for i, span in enumerate(spans):
        a, b = int(span[0]), int(span[1])
        body = text[a:b]
        raw_pages.append({
            "leaf": i + 1,
            "part": part_of.get(i + 1, "front"),
            "char_start": a,
            "char_end": b,
            "line_start": min(line_of(starts, a), n_lines),
            "line_end": min(line_of(starts, max(a, b - 1)), n_lines),
            "blank": not body.strip(),
            "opens": re.sub(r"\s+", " ", body).strip()[:80],
            "_body": body,
        })

    reads = []
    for page in raw_pages:
        folio = read_folio(page["_body"])
        if folio is not None and 1 <= folio <= 400:
            reads.append((page["leaf"], folio))
    runs = folio_runs(reads)

    read_at = dict(reads)
    discarded = []
    for page in raw_pages:
        leaf = page["leaf"]
        printed, source = None, None
        for run in runs:
            if run["first_leaf"] <= leaf <= run["last_leaf"] and (leaf - run["offset"]) % 2 == 0:
                printed = (leaf - run["offset"]) // 2
                source = "read" if read_at.get(leaf) == printed else "offset"
                break
        # A read that the runs contradict is DISCARDED and counted, never written.
        if leaf in read_at and read_at[leaf] != printed:
            discarded.append((leaf, read_at[leaf]))
        page["printed_page"] = printed
        page["folio_source"] = source
        del page["_body"]
    return raw_pages, runs, discarded


def build() -> int:
    raw, text, spans = read_deposit()
    TEXT.parent.mkdir(parents=True, exist_ok=True)
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    TEXT.write_bytes(raw)
    pages, runs, discarded = build_pages(text, spans)
    doc = {
        "schema": 1,
        "id": "fergus_26_29",
        "title": "Fergus' Historical Series, Nos. 26-29 (Chicago: Fergus Printing "
                 "Company, 1883-1885), bound in one volume",
        "archive_item": "fergushistorical2629unse",
        "generated_by": "tools/build_fergus_page_index.py --build",
        "_doc": "Leaf boundaries read straight out of the deposit's OWN hOCR page "
                "index, which carries exact character offsets into the deposit search "
                "text; nothing here is aligned or guessed. `leaf` is the scan's sheet "
                "number, 1-based; `line_start`/`line_end` are inclusive 1-based line "
                "numbers into text/fergus_26_29.txt, which is what a claim's locator "
                "cites. `printed_page` is the folio the book itself prints and every "
                "part restarts its own numbering, so a folio is only ever meaningful "
                "beside its `part`.",
        "text_file": "fergus_26_29.txt",
        "text_sha256": sha256(raw),
        "text_bytes": len(raw),
        "text_lines": len(text.splitlines()),
        "deposit_searchtext": "chicago/reference/fergus/fergushistorical2629unse_hocr_searchtext",
        "deposit_pageindex": "chicago/reference/fergus/fergushistorical2629unse_hocr_pageindex.json",
        "deposit_sha256": sha256(raw),
        "leaves": len(pages),
        "leaves_blank": sum(1 for p in pages if p["blank"]),
        "folios_read": sum(1 for p in pages if p["folio_source"] == "read"),
        "folios_by_offset": sum(1 for p in pages if p["folio_source"] == "offset"),
        "folio_runs": runs,
        "folios_discarded": [{"leaf": leaf, "read": folio} for leaf, folio in discarded],
        "parts": PARTS,
        "pages": pages,
    }
    INDEX.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s (%d bytes) and %s (%d leaves, %d folios read, %d carried, "
          "%d discarded)" % (TEXT.relative_to(ROOT), len(raw), INDEX.relative_to(ROOT),
                             len(pages), doc["folios_read"], doc["folios_by_offset"],
                             len(discarded)))
    return 0


def check() -> int:
    bad = []
    if not TEXT.exists():
        bad.append("the committed text is missing")
    if not INDEX.exists():
        bad.append("the page index is missing")
    if bad:
        for b in bad:
            print("FAIL: %s" % b)
        return 1
    raw = TEXT.read_bytes()
    doc = json.loads(INDEX.read_text(encoding="utf-8"))
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()

    if doc.get("text_sha256") != sha256(raw):
        bad.append("text_sha256 does not match the committed text — somebody edited a "
                   "transcription, and every quote in the domain is now unchecked")
    if SEARCHTEXT.exists() and SEARCHTEXT.read_bytes() != raw:
        bad.append("the committed text is no longer byte-identical to the deposit")
    if doc.get("text_lines") != len(lines):
        bad.append("text_lines says %s, the file has %d" % (doc.get("text_lines"), len(lines)))

    pages = doc.get("pages") or []
    if len(pages) != doc.get("leaves"):
        bad.append("leaves says %s, pages holds %d" % (doc.get("leaves"), len(pages)))
    keys = {p["key"] for p in PARTS}
    last_end = 0
    for page in pages:
        where = "leaf %s" % page.get("leaf")
        if page.get("part") not in keys:
            bad.append("%s: part %r is not one of the volume's parts" % (where, page.get("part")))
        if page.get("char_start") < last_end:
            bad.append("%s: char_start runs backwards" % where)
        last_end = page.get("char_end")
        ls, le = page.get("line_start"), page.get("line_end")
        if not (1 <= ls <= le <= len(lines)):
            bad.append("%s: lines %s-%s are not in the committed text" % (where, ls, le))
        if page.get("printed_page") is not None and page.get("folio_source") not in ("read", "offset"):
            bad.append("%s: a printed_page with no folio_source" % where)
    if last_end != len(text):
        bad.append("the last leaf ends at %d, the text is %d characters" % (last_end, len(text)))

    for b in bad:
        print("FAIL: %s" % b)
    if bad:
        return 1
    print("OK: %d leaves over %d lines; %d folios read, %d carried by offset, %d discarded"
          % (len(pages), len(lines), doc.get("folios_read", 0),
             doc.get("folios_by_offset", 0), len(doc.get("folios_discarded") or [])))
    return 0


def self_test() -> int:
    """The two assertions that matter, on fixtures, without touching the deposit."""
    failures = []
    starts = line_starts("a\nbb\nccc\n")
    if [line_of(starts, o) for o in (0, 2, 5, 8)] != [1, 2, 3, 3]:
        failures.append("line_of does not map character offsets onto 1-based lines")
    if read_folio("  4 HARRISONS HISTORICAL DISCOURSE.\nthe great increase\n") != 4:
        failures.append("a verso folio is not read")
    if read_folio("ABORIGINES OF THE OHIO VALLEY. 5\nreal history\n") != 5:
        failures.append("a recto folio is not read")
    runs = folio_runs([(700, 23), (708, 27), (718, 32), (724, 35), (410, 843)])
    if len(runs) != 1 or runs[0]["offset"] != 654:
        failures.append("the folio run is not found")
    pages, runs2, discarded = build_pages(
        "x\n", [[0, 2, 0, 0]])
    if len(pages) != 1 or pages[0]["leaf"] != 1:
        failures.append("build_pages does not index a one-leaf fixture")
    for f in failures:
        print("FAIL: %s" % f)
    print("self-test: %d assertion(s) failed" % len(failures))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.build:
        return build()
    return check()


if __name__ == "__main__":
    sys.exit(main())
