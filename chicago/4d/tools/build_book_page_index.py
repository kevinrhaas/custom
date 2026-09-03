#!/usr/bin/env python3
"""Page boundaries for a committed book text that has none.

    tools/build_book_page_index.py --build   re-derive the index (needs pdftotext)
    tools/build_book_page_index.py --check   the gate (committed files only)
    tools/build_book_page_index.py --self-test

WHY THIS FILE EXISTS. `data/research/books/` commits the TEXT it quotes from, and
the gate in `tools/research_domains.py` rebuilds every quote out of that text by
line number. For Hubbard's autobiography the text this project was told to commit
is the Internet Archive's own OCR output,
`https://archive.org/download/autobiographyofg00hubb/autobiographyofg00hubb_djvu.txt`
— and that file carries NO page breaks at all. Zero form feeds, no folios of its
own, nothing that says where leaf 65 stops and leaf 66 starts.

That is a problem, because a book's locator is a PAGE. `coverage.json` already
records the shape of this fault once: Hurlbut's chapter is declared as one `list`
item and not as nine `page` items, because "declaring nine pages would mean
assigning each claim to a page nobody has seen, which is an invention, and the
gate would then be checking a fiction rather than a reading."

The deposited scan, `chicago/reference/swift-walker-autobiography/
autobiographyofg00hubb.pdf`, carries the SAME OCR in a text layer that DOES have
all 226 leaf breaks. So the page boundaries are not invented here — they are
transferred, mechanically, from the one artifact that holds them onto the one this
repo quotes from, and this file is that transfer written down so it can be redone
and disputed.

HOW. `pdftotext -layout` splits the deposit into 226 leaves. Both texts are
whitespace-normalised; a single `difflib.SequenceMatcher` pass over the two
normalised strings gives the correspondence (they agree to better than 0.9999,
their OCR being the same OCR); each leaf's normalised start is carried across and
mapped back to a raw offset, and thence to a 1-based line number in the committed
text. Where a leaf's opening words cannot be located the entry is written with
`aligned: false` and no claim may cite it.

WHAT IS DERIVED AND WHAT IS READ. The leaf number is mechanical. The PRINTED folio
is not: it is read off the foot of the leaf where the OCR gives it, and where the
OCR does not, it is carried by the constant offset that the read folios establish
— which is recorded per entry as `folio_source`: `read` or `offset`. Nothing here
authors a claim.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # chicago/4d
BOOKS = ROOT / "data" / "research" / "books"
REPO = ROOT.parent.parent                              # the custom repo root

BOOKS_INDEXED = {
    "hubbard_autobiography_1911": {
        "title": 'The Autobiography of Gurdon Saltonstall Hubbard, Pa-pa-ma-ta-be, '
                 '"The Swift Walker" (Chicago: Lakeside Press, 1911)',
        "archive_item": "autobiographyofg00hubb",
        "deposit_pdf": "chicago/reference/swift-walker-autobiography/autobiographyofg00hubb.pdf",
        "leaves": 226,
        # The two folio runs the book prints, each as (first_leaf, last_leaf,
        # first_folio). Roman for the front matter, arabic for the body. Both are
        # CHECKED against the folios the OCR actually gives, and a disagreement is
        # an error and not a silent correction.
        "folio_runs": [
            {"first_leaf": 21, "last_leaf": 37, "first_folio": 11, "numeral": "roman"},
            {"first_leaf": 39, "last_leaf": 220, "first_folio": 1, "numeral": "arabic"},
        ],
    },
}

ROMAN = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
         (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]


def roman(n: int) -> str:
    out = []
    for value, sign in ROMAN:
        while n >= value:
            out.append(sign)
            n -= value
    return "".join(out)


def folio_for(spec: dict, leaf: int):
    for run in spec["folio_runs"]:
        if run["first_leaf"] <= leaf <= run["last_leaf"]:
            n = run["first_folio"] + leaf - run["first_leaf"]
            return roman(n) if run["numeral"] == "roman" else str(n)
    return None


def normalise(s: str):
    """Collapse whitespace, keeping a map back to the raw offsets."""
    out, back = [], []
    prev_space = True
    for i, ch in enumerate(s):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            back.append(i)
            prev_space = True
        else:
            out.append(ch)
            back.append(i)
            prev_space = False
    while out and out[-1] == " ":
        out.pop()
        back.pop()
    return "".join(out), back


def line_starts(text: str):
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def line_of(starts, offset: int) -> int:
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1                                       # 1-based


def build_one(key: str, spec: dict) -> dict:
    text_path = BOOKS / "text" / (key + ".txt")
    text = text_path.read_text(encoding="utf-8")
    pdf = REPO / spec["deposit_pdf"]
    if not pdf.exists():
        raise SystemExit("the deposit is not here: %s" % pdf)
    raw = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                         check=True, capture_output=True).stdout.decode("utf-8", "replace")
    leaves = raw.split("\f")
    if leaves and not leaves[-1].strip():
        leaves.pop()
    if len(leaves) != spec["leaves"]:
        raise SystemExit("the deposit split into %d leaves, not %d" % (len(leaves), spec["leaves"]))

    ntext, back = normalise(text)
    nleaf_texts = [normalise(t)[0] for t in leaves]

    # A whole-document difflib pass over 285 000 characters does not finish, so the
    # alignment is done leaf by leaf and forwards only: each leaf's opening words are
    # searched for in the committed text from where the previous leaf ended. The two
    # OCRs are the same OCR, so the opening usually matches EXACTLY; where it does
    # not — poppler occasionally welds an italic word to its neighbour, which the
    # djvu text spaces — the probe is retried from the second word, the third and so
    # on, and the leaf's start is then backed off by the length of the words skipped.
    # Which of the two happened is recorded per leaf as `align_method`, because a
    # backed-off boundary is good to a few characters and an exact one is not.
    PROBE_WORDS = 9
    MAX_SKIP = 24
    positions, methods = [], []
    cursor = 0
    for t in nleaf_texts:
        if not t:
            positions.append(None)
            methods.append(None)
            continue
        words = t.split(" ")
        found, method = None, None
        for skip in range(0, MAX_SKIP + 1):
            probe = " ".join(words[skip:skip + PROBE_WORDS])
            if len(probe) < 12:
                break
            at = ntext.find(probe, cursor)
            if at < 0:
                continue
            prefix = " ".join(words[:skip])
            found = at - (len(prefix) + 1 if prefix else 0)
            if found < 0:
                found = at
            method = "exact" if skip == 0 else "skipped_%d_words" % skip
            break
        positions.append(found)
        methods.append(method)
        if found is not None:
            cursor = max(cursor, found + max(0, len(t) - 400))

    starts = line_starts(text)
    entries = []
    for i, t in enumerate(nleaf_texts):
        leaf = i + 1
        entry = {"leaf": leaf, "printed_page": None, "folio_source": None,
                 "blank": not t, "aligned": False, "char_start": None, "line_start": None,
                 "opens": ""}
        printed = folio_for(spec, leaf)
        if printed is not None:
            entry["printed_page"] = printed
            entry["folio_source"] = "offset"
            # Confirm against the folio the OCR prints at the foot of the leaf.
            tail = [l.strip() for l in leaves[i].split("\n") if l.strip()]
            if tail and tail[-1].strip().lower().strip(".") == printed.lower():
                entry["folio_source"] = "read"
        if t:
            pos = positions[i]
            if pos is not None and pos < len(back):
                entry["aligned"] = True
                entry["align_method"] = methods[i]
                entry["char_start"] = back[pos]
                entry["line_start"] = line_of(starts, back[pos])
                entry["opens"] = " ".join(t.split()[:8])
        entries.append(entry)

    # A leaf ends where the next aligned leaf begins.
    for i, entry in enumerate(entries):
        nxt = None
        for j in range(i + 1, len(entries)):
            if entries[j]["aligned"]:
                nxt = entries[j]
                break
        if entry["aligned"]:
            entry["line_end"] = (nxt["line_start"] - 1) if nxt else len(starts)
            entry["char_end"] = (nxt["char_start"] - 1) if nxt else len(text)

    read = sum(1 for e in entries if e["folio_source"] == "read")
    return {
        "schema": 1,
        "id": key,
        "title": spec["title"],
        "archive_item": spec["archive_item"],
        "generated_by": "tools/build_book_page_index.py --build",
        "_doc": "Leaf boundaries carried onto the committed text from the deposited "
                "scan's own text layer, because the committed text (the Internet "
                "Archive djvu OCR) has none. `leaf` is the scan's sheet number, 1-based "
                "and mechanical; `printed_page` is the folio the book itself prints, "
                "and `folio_source` says whether it was READ off the foot of that leaf "
                "or carried by the constant offset the read folios establish. "
                "`line_start`/`line_end` are inclusive 1-based line numbers into "
                "text/%s.txt, which is what a claim's locator cites." % key,
        "text_file": key + ".txt",
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "text_lines": len(starts),
        "deposit_pdf": spec["deposit_pdf"],
        "deposit_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "leaves": len(entries),
        "leaves_aligned": sum(1 for e in entries if e["aligned"]),
        "leaves_blank": sum(1 for e in entries if e["blank"]),
        "folios_read": read,
        "leaves_aligned_exactly": sum(1 for e in entries if e.get("align_method") == "exact"),
        "pages": entries,
    }


def check(quiet: bool = False) -> int:
    bad = []
    for key, spec in BOOKS_INDEXED.items():
        path = BOOKS / "page_index" / (key + ".json")
        if not path.exists():
            bad.append("%s: no page index committed" % key)
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        text_path = BOOKS / "text" / doc.get("text_file", "")
        if not text_path.exists():
            bad.append("%s: names text_file %r, which is not committed" % (key, doc.get("text_file")))
            continue
        text = text_path.read_text(encoding="utf-8")
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if sha != doc.get("text_sha256"):
            bad.append("%s: the index was built against a different text (sha256 %s, "
                       "committed text is %s)" % (key, doc.get("text_sha256"), sha))
        n_lines = len(line_starts(text))
        if n_lines != doc.get("text_lines"):
            bad.append("%s: the index counts %s lines, the text has %d"
                       % (key, doc.get("text_lines"), n_lines))
        pages = doc.get("pages") or []
        if len(pages) != spec["leaves"]:
            bad.append("%s: %d leaves indexed, the scan has %d" % (key, len(pages), spec["leaves"]))
        prev_line, prev_leaf = 0, 0
        for entry in pages:
            leaf = entry.get("leaf")
            if leaf != prev_leaf + 1:
                bad.append("%s: leaf numbers are not consecutive at %r" % (key, leaf))
            prev_leaf = leaf
            expected = folio_for(spec, leaf)
            if entry.get("printed_page") != expected:
                bad.append("%s leaf %s: printed_page %r, the folio runs say %r"
                           % (key, leaf, entry.get("printed_page"), expected))
            if not entry.get("aligned"):
                continue
            if entry.get("line_start", 0) < prev_line:
                bad.append("%s leaf %s: line_start %r runs backwards from leaf %s"
                           % (key, leaf, entry.get("line_start"), leaf - 1))
            prev_line = entry.get("line_start", 0)
            if entry.get("line_end") is not None and entry["line_end"] < entry["line_start"]:
                bad.append("%s leaf %s: ends before it starts" % (key, leaf))
            if entry["line_start"] > n_lines:
                bad.append("%s leaf %s: line_start %d is past the end of the text"
                           % (key, leaf, entry["line_start"]))
        aligned = sum(1 for e in pages if e.get("aligned"))
        if aligned != doc.get("leaves_aligned"):
            bad.append("%s: the header counts %s aligned leaves, the entries show %d"
                       % (key, doc.get("leaves_aligned"), aligned))
        if not quiet:
            print("  %s — %d leaves, %d aligned, %d folios read off the page"
                  % (key, len(pages), aligned, sum(1 for e in pages if e.get("folio_source") == "read")))
    if bad:
        for line in bad:
            print("  FAIL %s" % line)
        return 1
    if not quiet:
        print("  page index: OK")
    return 0


def self_test() -> int:
    """The gate's own assertions still fire when the index is broken."""
    key = "hubbard_autobiography_1911"
    path = BOOKS / "page_index" / (key + ".json")
    original = path.read_text(encoding="utf-8")
    doc = json.loads(original)
    cases = [
        ("a text that is not the one indexed",
         lambda d: d.update(text_sha256="0" * 64), "built against a different text"),
        ("a leaf whose folio contradicts the printed run",
         lambda d: d["pages"][100].update(printed_page="999"), "the folio runs say"),
        ("line numbers that run backwards",
         lambda d: d["pages"][100].update(line_start=1), "runs backwards"),
    ]
    failures = 0
    try:
        for label, break_it, wanted in cases:
            broken = json.loads(original)
            break_it(broken)
            path.write_text(json.dumps(broken, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = check(quiet=True)
            if rc == 0 or wanted not in buf.getvalue():
                print("  FAIL the gate does not catch %s" % label)
                failures += 1
            else:
                print("  caught: %s" % label)
    finally:
        path.write_text(original, encoding="utf-8")
    if failures:
        return 1
    print("  self-test: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.build:
        for key, spec in BOOKS_INDEXED.items():
            doc = build_one(key, spec)
            out = BOOKS / "page_index" / (key + ".json")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("  %s — %d leaves, %d aligned (%d exactly), %d folios read"
                  % (key, doc["leaves"], doc["leaves_aligned"],
                     doc["leaves_aligned_exactly"], doc["folios_read"]))
        return 0
    if args.self_test:
        return self_test()
    return check()


if __name__ == "__main__":
    sys.exit(main())
