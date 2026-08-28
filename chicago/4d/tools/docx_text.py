#!/usr/bin/env python3
"""Plain text out of a .docx, with the standard library and nothing else.

WHY THIS EXISTS. The newspaper corpus (T-0256) ships two thirds of its issues as
matched .txt + .docx pairs and the last third — the 1835 Democrat tail and the
entire Chicago American, which is to say EVERY WEEK ON EITHER SIDE OF THE SCENE
DATE — as .docx only. A citation this project cannot resolve to readable text is
not a citation, so those issues need text.

A .docx is a zip of XML. `zipfile` opens it and `xml.etree` reads it, so this
adds no dependency to a fleet whose first house rule is that there are none.

DETERMINISM IS THE CONTRACT, not a nicety. The extracted text is committed under
data/research/newspapers/text/ and cited by file and line range; a re-run that
reflows a paragraph silently invalidates every line number anybody wrote down.
So: document order, no dict iteration, no locale, no timestamps, LF endings, one
trailing newline. `--self-test` builds a .docx in a temp directory, extracts it
twice and asserts the two runs are byte-identical.

WHAT IT DOES NOT DO. It does not read the scan, and it is not a transcription
step: it carries the transcriber's own text across, brackets and page/column
markers intact, and invents nothing. Ruling 2 of T-0256 applies to everything
that comes out of here — a claim taken from this text is
`reading: transcription_mediated`, and a scan read outranks it.

    tools/docx_text.py IN.docx                 # text to stdout
    tools/docx_text.py IN.docx -o OUT.txt      # text to a file
    tools/docx_text.py --self-test             # determinism + shape
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Runs whose text is not part of the document as read: a tracked deletion is
# text somebody took OUT, and a field instruction is markup that happens to be
# stored as characters. Both would otherwise land in the middle of a column.
SKIP_RUN_TEXT = {W + "delText", W + "instrText"}


def _run_text(node: ET.Element) -> str:
    """Text of one <w:r>, in document order, with tabs and breaks preserved."""
    out: list[str] = []
    for el in node.iter():
        tag = el.tag
        if tag == W + "t":
            out.append(el.text or "")
        elif tag == W + "tab":
            out.append("\t")
        elif tag in (W + "br", W + "cr"):
            out.append("\n")
        elif tag == W + "noBreakHyphen":
            out.append("-")
        elif tag == W + "softHyphen":
            out.append("")
        elif tag in SKIP_RUN_TEXT:
            # Present for completeness: iter() reaches these, and reading their
            # .text is exactly the mistake this set exists to prevent.
            continue
    return "".join(out)


def _node_text(node: ET.Element) -> str:
    tag = node.tag
    if tag == W + "r":
        return _run_text(node)
    if tag in SKIP_RUN_TEXT:
        return ""
    if tag in (W + "pPr", W + "rPr", W + "sectPr"):
        return ""
    # hyperlinks, smart tags, content controls, bookmarks: recurse in order.
    return "".join(_node_text(child) for child in node)


def _block_lines(node: ET.Element) -> list[str]:
    """Lines for one block-level element, in document order.

    A paragraph is one line. A table is one line per row, cells joined by a tab
    — the corpus uses tables for the running headers and the odd price list, and
    a tab keeps a column boundary visible without inventing a layout.
    """
    tag = node.tag
    if tag == W + "p":
        return [_node_text(node)]
    if tag == W + "tbl":
        lines: list[str] = []
        for tr in node:
            if tr.tag != W + "tr":
                continue
            cells: list[str] = []
            for tc in tr:
                if tc.tag != W + "tc":
                    continue
                inner: list[str] = []
                for blk in tc:
                    inner.extend(_block_lines(blk))
                cells.append(" ".join(s for s in inner if s).strip())
            lines.append("\t".join(cells))
        return lines
    if tag == W + "sdt":
        lines = []
        for child in node:
            if child.tag == W + "sdtContent":
                for blk in child:
                    lines.extend(_block_lines(blk))
        return lines
    return []


def docx_to_text(data: bytes) -> str:
    """The whole contract, as a pure function of the .docx bytes."""
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find(W + "body")
    if body is None:
        raise ValueError("word/document.xml carries no <w:body>")
    lines: list[str] = []
    for block in body:
        lines.extend(_block_lines(block))
    # Normalise line endings and trailing whitespace per line; keep blank lines,
    # because a blank line between columns is part of how the corpus reads.
    text = "\n".join(ln.replace("\r\n", "\n").replace("\r", "\n").rstrip() for ln in lines)
    text = "\n".join(seg.rstrip() for seg in text.split("\n"))
    return text.rstrip("\n") + "\n"


def extract(path: Path) -> str:
    return docx_to_text(path.read_bytes())


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

_SELF_TEST_DOC = (
    "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:body>"
    "<w:p><w:r><w:t>===== ISSUE PAGE 1 / PDF PAGE 33 / COLUMN 1 OF 6 =====</w:t></w:r></w:p>"
    "<w:p><w:r><w:t xml:space='preserve'>C. &amp; I. HARMON, </w:t></w:r>"
    "<w:r><w:t>[uncertain: dry goods]</w:t></w:r></w:p>"
    "<w:p><w:r><w:t>first</w:t><w:br/><w:t>second</w:t><w:tab/><w:t>tabbed</w:t></w:r></w:p>"
    "<w:p><w:r><w:delText>struck out</w:delText></w:r><w:r><w:t>kept</w:t></w:r></w:p>"
    "<w:p><w:r><w:instrText> PAGE </w:instrText></w:r><w:r><w:t>[illegible]</w:t></w:r></w:p>"
    "<w:tbl><w:tr><w:tc><w:p><w:r><w:t>a</w:t></w:r></w:p></w:tc>"
    "<w:tc><w:p><w:r><w:t>b</w:t></w:r></w:p></w:tc></w:tr></w:tbl>"
    "<w:p><w:r><w:t>   trailing spaces   </w:t></w:r></w:p>"
    "<w:p/>"
    "</w:body></w:document>"
)

_SELF_TEST_EXPECT = (
    "===== ISSUE PAGE 1 / PDF PAGE 33 / COLUMN 1 OF 6 =====\n"
    "C. & I. HARMON, [uncertain: dry goods]\n"
    "first\nsecond\ttabbed\n"
    "kept\n"
    "[illegible]\n"
    "a\tb\n"
    "   trailing spaces\n"
)


def _write_fixture(path: Path) -> None:
    """A .docx is a zip; write one with fixed member order and a fixed date so
    the fixture itself cannot be the source of a difference between runs."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in (
            ("[Content_Types].xml",
             "<?xml version='1.0'?><Types xmlns='http://schemas.openxmlformats.org/"
             "package/2006/content-types'/>"),
            ("word/document.xml", _SELF_TEST_DOC),
        ):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            z.writestr(info, body)


def self_test() -> int:
    import tempfile

    failures: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        fixture = Path(td) / "fixture.docx"
        _write_fixture(fixture)

        first = extract(fixture)
        second = extract(fixture)
        if first.encode() != second.encode():
            failures.append("two extractions of the same file differ — not deterministic")
        if first != _SELF_TEST_EXPECT:
            failures.append(
                "extracted text is not the expected shape\n"
                f"  got:      {first!r}\n  expected: {_SELF_TEST_EXPECT!r}")

        # The assertions above must be capable of failing: a fixture whose text
        # is changed has to come out different, or the comparison proves nothing.
        moved = Path(td) / "moved.docx"
        with zipfile.ZipFile(fixture) as src, zipfile.ZipFile(moved, "w") as dst:
            for name in src.namelist():
                body = src.read(name)
                if name == "word/document.xml":
                    body = body.replace(b"kept", b"altered")
                dst.writestr(zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0)), body)
        if extract(moved) == first:
            failures.append("a changed document extracted identically — the test is blind")

    for f in failures:
        print(f"FAIL  {f}", file=sys.stderr)
    if failures:
        return 1
    print("docx_text self-test: deterministic, brackets and markers preserved, "
          "deletions and field instructions dropped, and the comparison still fires")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("docx", nargs="?", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.docx is None:
        ap.error("give a .docx, or --self-test")
    text = extract(args.docx)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
