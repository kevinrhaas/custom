#!/usr/bin/env python3
"""Turn the owner's newspaper deposit into a resolvable index (T-0256).

WHAT THIS BUILDS. `data/research/newspapers/corpus.json` — one entry per ISSUE
of the Chicago Democrat (1833-11-26 to 1835-08-26) and the Chicago American
(1835-06-08 to 1835-08-29), each naming the text a citation resolves against,
its sha256, the .docx it came from, how complete the scan is, and where the
transcription set's own manifest and validation notes say so. Plus the derived
text itself, under `data/research/newspapers/text/`, for every transcription in
the deposit that ships as .docx only.

WHERE THE DEPOSIT LIVES, AND WHY THIS TOOL IS NOT IN check.sh.
`chicago/reference/newspapers/` is the owner's archival deposit. This project
READS it and never writes to it — and it is not, today, on every branch: the
deposit was pushed to `main` on 2026-08-27 and `dev` has not been back-merged,
so a dev checkout has no Transcriptions/ directory at all. That is why the
BUILDER (this file, which needs the deposit) and the GATE
(`tools/check_newspaper_corpus.py`, which needs only corpus.json and the derived
text this repo owns) are two programs. check.sh runs the gate.

    tools/build_newspaper_corpus.py                 # write corpus.json + text
    tools/build_newspaper_corpus.py --check         # re-derive, diff, change nothing
    tools/build_newspaper_corpus.py --deposit DIR   # read the deposit elsewhere

WHICH TRANSCRIPTION AN ISSUE CITES. Several issues carry more than one. The
order is stated rather than assumed, and it is recorded on every entry:

  1. A transcription of a COMPLETE scan beats one of a partial scan.
  2. At equal completeness, the one with a committed .txt beats a .docx-only
     one — that is the deliverable the set's own manifest measures.

Rule 1 is not academic. The 1835-07-08 Democrat — the issue one week after the
scene date — is transcribed twice: once from a three-page scan whose fourth page
is missing, and once, later, from a complete four-page scan. The partial is the
one with the .txt and the manifest row, so rule 2 alone would have cited the
short reading of the most interesting week in the run. It is kept as an
alternate, because the two readings of the same issue are worth comparing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import docx_text

ROOT = Path(__file__).resolve().parent.parent          # chicago/4d
REPO = ROOT.parent.parent                              # the custom repo root
DEPOSIT = REPO / "chicago" / "reference" / "newspapers" / "Transcriptions"
OUT_DIR = ROOT / "data" / "research" / "newspapers"
TEXT_DIR = OUT_DIR / "text"
CORPUS = OUT_DIR / "corpus.json"

PUBLICATIONS = {
    "Chicago_Democrat": {
        "id": "chicago_democrat",
        "title": "Chicago Democrat",
        "source_id": "chicago_democrat_1833_1835",
        "set_dir": "Chicago_Democrat_1833-11_to_1835-08",
    },
    "Chicago_American": {
        "id": "chicago_american",
        "title": "Chicago American",
        "source_id": "chicago_american_1835",
        "set_dir": "Chicago_American_1835-06_to_1835-08",
    },
}

# Chicago_<Paper>_<YYYY-MM-DD>_<Vol…>_<No…>_Transcription[-2].(docx|txt)
STEM = re.compile(
    r"^(?P<paper>Chicago_(?:Democrat|American))_"
    r"(?P<date>\d{4}-\d{2}-\d{2})_"
    r"(?P<issue>.+?)"
    r"_Transcription(?P<variant>-\d)?$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


CANONICAL_DEPOSIT = "chicago/reference/newspapers/Transcriptions"

# Where the deposit was actually read from this run. A citation resolves against
# the CANONICAL path above whatever happens here: on a branch that does not carry
# the deposit (see the module docstring) it is read from a checkout of `main`
# elsewhere on disk, and a corpus recording that temporary location would be a
# corpus nobody else could resolve.
_deposit_root: Path | None = None


def rel(path: Path) -> str:
    """The path a citation resolves against: repo-root-relative, POSIX."""
    resolved = path.resolve()
    if _deposit_root is not None:
        try:
            return f"{CANONICAL_DEPOSIT}/{resolved.relative_to(_deposit_root).as_posix()}"
        except ValueError:
            pass
    return resolved.relative_to(REPO).as_posix()


# ---------------------------------------------------------------------------
# reading the deposit
# ---------------------------------------------------------------------------

VOL_NO = re.compile(r"^Vol(?:ume)?(?P<vol>[0-9IVX]+)_No(?P<no>[0-9]+)$", re.I)
ROMAN = {"1": "I", "2": "II", "I": "I", "II": "II"}


def parse_issue_token(token: str) -> tuple[str, str, str | None]:
    """'Vol2_No11' -> ('II', '11', None); 'Extra' -> ('', 'Extra', 'extra');
    'Vol2_No12_Partial' -> ('II', '12', 'partial')."""
    qualifier = None
    if token.endswith("_Partial"):
        token, qualifier = token[: -len("_Partial")], "partial"
    if token == "Extra":
        return "", "Extra", "extra"
    m = VOL_NO.match(token)
    if not m:
        return "", token, qualifier
    return ROMAN.get(m.group("vol"), m.group("vol")), m.group("no"), qualifier


STATUS_LINE = re.compile(r"^(?:Status|Completeness):\s*(?P<v>.+)$", re.M)


def read_completeness(text: str) -> tuple[str, str]:
    """('complete'|'partial', the transcription's own sentence about it)."""
    m = STATUS_LINE.search(text)
    stated = m.group("v").strip() if m else ""
    lowered = stated.lower()
    if "partial" in lowered or "is absent" in lowered or "is missing" in lowered:
        return "partial", stated
    if stated:
        return "complete", stated
    return "unstated", ""


# THE DEPOSIT USES THREE MARKER DIALECTS, not one. T-0256 quotes the first of
# them as though it were universal; it covers 26 of 86 issues. All three carry a
# page and a column, which is what the citation convention actually needs, and
# the dialect is recorded on every entry so a reader knows what to grep for.
#
#   A  ===== ISSUE PAGE n / [SOURCE ]PDF PAGE m / COLUMN k OF 6 =====
#      the 1834 diplomatic .txt set
#   B  Newspaper Page n — Source PDF Page m   /   Column k
#      the OCR-rebuild .docx set: the 1835 Democrat tail and all of the American
#   C  a SOURCE PDF PAGE banner, in either of its own two forms, then
#      --- Column k --- headings: the 1833 .txt set
#   D  [Source PDF page m; newspaper page n; column k]
#   E  --- SOURCE PDF PAGE m, COLUMN k ---
#      the 1835 Jan-Jul .txt set uses D and E in roughly equal measure
RULE_A = re.compile(r"^===== ISSUE PAGE (\d+) / (?:SOURCE )?PDF PAGE \d+ / COLUMN \d+ OF \d+ =====$")
PAGE_B = re.compile(r"^Newspaper Page (\d+) — Source PDF Page \d+$")
COLUMN_B = re.compile(r"^Column \d+$")
PAGE_C = re.compile(r"^(?:SOURCE PDF PAGE (\d+)"
                   r"|===== (?:SOURCE|ORIGINAL) PDF PAGE \d+ / ISSUE PAGE (\d+) =====)$")
COLUMN_C = re.compile(r"^--- Column \d+ ---$")
RULE_D = re.compile(r"^\[Source PDF page \d+; newspaper page (\d+); column \d+\]$")
RULE_E = re.compile(r"^--- SOURCE PDF PAGE (\d+), COLUMN \d+ ---$")


def count_markers(text: str) -> dict:
    """Page and column markers, in whichever dialect the transcription uses.

    A claim that cannot name its column cannot be made, so an issue with no
    column marker at all is a finding and the gate says so."""
    pages = {k: set() for k in "ABCDE"}
    cols = dict.fromkeys("ABCDE", 0)
    for line in text.split("\n"):
        m = RULE_A.match(line)
        if m:
            pages["A"].add(m.group(1))
            cols["A"] += 1
            continue
        m = PAGE_B.match(line)
        if m:
            pages["B"].add(m.group(1))
            continue
        m = PAGE_C.match(line)
        if m:
            pages["C"].add(m.group(1) or m.group(2))
            continue
        m = RULE_D.match(line)
        if m:
            pages["D"].add(m.group(1))
            cols["D"] += 1
            continue
        m = RULE_E.match(line)
        if m:
            pages["E"].add(m.group(1))
            cols["E"] += 1
            continue
        if COLUMN_B.match(line):
            cols["B"] += 1
        elif COLUMN_C.match(line):
            cols["C"] += 1
    names = {"A": "issue_page_column_rule", "B": "page_heading_column_heading",
             "C": "pdf_page_banner_column_dash", "D": "bracketed_page_column",
             "E": "pdf_page_column_dash"}
    best = max("ABCDE", key=lambda k: cols[k])
    return {"marker_dialect": names[best] if cols[best] else "none",
            "pages": len(pages[best]), "column_markers": cols[best]}


def load_manifests(set_dir: Path) -> dict[str, dict]:
    """date -> the row the set's own manifest keeps about that issue."""
    rows: dict[str, dict] = {}
    for csv_path in sorted(set_dir.glob("*_Issue_Manifest.csv")):
        with csv_path.open(newline="", encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                date = (row.get("date") or row.get("printed_date") or "").strip()
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                    continue
                rows[date] = {
                    "manifest": rel(csv_path),
                    "word_count": int(row["word_count"]) if row.get("word_count", "").strip()
                    else None,
                    "uncertainty_markers": int(row["uncertainty_markers"])
                    if row.get("uncertainty_markers", "").strip() else None,
                    "scan_status": (row.get("scan_status") or "").strip() or None,
                    "manifest_note": (row.get("notes") or "").strip() or None,
                }
    return rows


def validation_notes_for(set_dir: Path, date: str) -> str | None:
    """The set ships one validation note per YEAR-block; name the one that
    covers this issue rather than all three."""
    year = date[:4]
    best = None
    for md in sorted(set_dir.glob("*_Validation_Notes.md")):
        if year in md.name:
            best = md
    return rel(best) if best else None


def collect(deposit: Path) -> list[dict]:
    """Every transcription file in the deposit, grouped into issues."""
    issues: dict[tuple[str, str], dict] = {}
    for key, pub in PUBLICATIONS.items():
        set_dir = deposit / pub["set_dir"]
        if not set_dir.is_dir():
            raise SystemExit(f"deposit is missing {set_dir}")
        manifests = load_manifests(set_dir)
        for path in sorted(set_dir.iterdir()):
            if path.suffix not in (".docx", ".txt"):
                continue
            m = STEM.match(path.stem)
            if not m:
                # The 1833 'Verified' reading of the three supplied scan pages
                # does not follow the naming convention; it is handled below.
                continue
            if m.group("paper") != key:
                continue
            # A .docx beside its own .txt is the SAME transcription in another
            # container, not a second reading of the issue. The .txt is the
            # deliverable the manifest measures and it is already committed; the
            # .docx is recorded as its source and its text is not re-derived.
            # (T-0256: issues with a committed .txt are cited at their reference
            # path and not copied.)
            if path.suffix == ".docx" and path.with_suffix(".txt").is_file():
                continue
            date = m.group("date")
            vol, no, qualifier = parse_issue_token(m.group("issue"))
            entry = issues.setdefault((pub["id"], date), {
                "publication": pub, "date": date, "vol": vol, "no": no,
                "manifest": manifests.get(date, {}),
                "validation_notes": validation_notes_for(set_dir, date),
                "files": [],
            })
            if vol and not entry["vol"]:
                entry["vol"], entry["no"] = vol, no
            entry["files"].append({
                "path": path, "suffix": path.suffix, "qualifier": qualifier,
                "variant": m.group("variant") or "",
            })
    return list(issues.values())


VERIFIED_1833 = "Chicago_Democrat_1833_11-16-Verified_Transcription.docx"


def transcription_record(f: dict, *, deposit_rel: bool) -> dict:
    path: Path = f["path"]
    if path.suffix == ".txt":
        text = path.read_text(encoding="utf-8")
        text_path, origin = rel(path), "reference"
        text_sha, text_bytes = sha256(path), path.stat().st_size
        docx = path.with_suffix(".docx")
    else:
        text = docx_text.extract(path)
        blob = text.encode("utf-8")
        text_path = f"chicago/4d/data/research/newspapers/text/{path.stem}.txt"
        origin = "derived"
        text_sha = hashlib.sha256(blob).hexdigest()
        text_bytes = len(blob)
        docx = path
    completeness, stated = read_completeness(text)
    rec = {
        "text_path": text_path,
        "text_origin": origin,
        "text_sha256": text_sha,
        "text_bytes": text_bytes,
        "words": len(text.split()),
        "completeness": completeness,
        "completeness_stated": stated,
        "uncertainty_brackets": text.count("[uncertain")
        + text.count("[illegible]") + text.count("[missing at edge]")
        + text.count("[unclear:") + text.count("[damaged]"),
    }
    rec.update(count_markers(text))
    if docx.is_file():
        rec["source_docx"] = rel(docx)
        rec["source_docx_sha256"] = sha256(docx)
    return rec, text


COMPLETENESS_RANK = {"complete": 0, "unstated": 1, "partial": 2}


def preference_key(rec: dict) -> tuple:
    """Rule 1 then rule 2, both stated in this module's docstring. A
    transcription that states nothing about its scan sits between the two: it is
    not evidence of completeness, and it is not the partial reading either."""
    return (COMPLETENESS_RANK[rec["completeness"]],
            0 if rec["text_origin"] == "reference" else 1,
            rec["text_path"])


def build(deposit: Path) -> tuple[dict, dict[str, str]]:
    global _deposit_root
    _deposit_root = deposit.resolve()
    out_text: dict[str, str] = {}
    entries: list[dict] = []

    for grouped in collect(deposit):
        pub = grouped["publication"]
        records = []
        for f in sorted(grouped["files"], key=lambda f: (f["path"].name)):
            rec, text = transcription_record(f, deposit_rel=True)
            if rec["text_origin"] == "derived":
                out_text[rec["text_path"]] = text
            records.append(rec)
        records.sort(key=preference_key)
        chosen, alternates = records[0], records[1:]
        man = grouped["manifest"]
        entry = {
            "id": f"{pub['id']}_{grouped['date']}",
            "publication": pub["title"],
            "publication_id": pub["id"],
            "source_id": pub["source_id"],
            "date": grouped["date"],
            "volume": grouped["vol"],
            "number": grouped["no"],
            "citation_stem": (
                f"{pub['title']}, {grouped['date']}"
                + (f", Vol. {grouped['vol']}, No. {grouped['no']}" if grouped["vol"]
                   else f", {grouped['no']}")),
        }
        entry.update(chosen)
        entry["manifest_word_count"] = man.get("word_count")
        entry["manifest_uncertainty_markers"] = man.get("uncertainty_markers")
        entry["manifest"] = man.get("manifest")
        entry["manifest_scan_status"] = man.get("scan_status")
        entry["manifest_note"] = man.get("manifest_note")
        entry["validation_notes"] = grouped["validation_notes"]
        entry["alternate_transcriptions"] = alternates
        entries.append(entry)

    # The 1833 'Verified' reading. It is not an issue: it transcribes the SAME
    # three supplied scan pages that data/sources/chicago_democrat_1833_11_26.json
    # describes, under a filename that says 11-16, and its own first line reports
    # 'NOV. 19, 1833' at the top of supplied page 1. Three dates, one artefact, and
    # this project does not get to pick one quietly — it is carried as an alternate
    # on the first issue with the discrepancy written down.
    vpath = deposit / PUBLICATIONS["Chicago_Democrat"]["set_dir"] / VERIFIED_1833
    if vpath.is_file():
        rec, text = transcription_record(
            {"path": vpath, "suffix": ".docx", "qualifier": None, "variant": ""},
            deposit_rel=True)
        out_text[rec["text_path"]] = text
        rec["note"] = (
            "A second, independently made reading of the three supplied scan pages of "
            "the Democrat's first issue. THREE DATES ATTACH TO ONE ARTEFACT and none "
            "of them is settled here: the filename says 1833_11-16, this reading's own "
            "text reports 'NOV. 19, 1833' at the top of supplied page 1, and "
            "data/sources/chicago_democrat_1833_11_26.json — which was made by reading "
            "the scans directly — dates the set 1833-11-26 and states that its page2.jpg "
            "is the front page carrying the full masthead. A citation from this file "
            "names this file; it does not settle the issue date.")
        first = next(e for e in entries
                     if e["publication_id"] == "chicago_democrat" and e["date"] == "1833-11-26")
        first["alternate_transcriptions"].append(rec)

    entries.sort(key=lambda e: (e["publication_id"], e["date"]))
    pubs = []
    for key in PUBLICATIONS:
        pub = PUBLICATIONS[key]
        mine = [e for e in entries if e["publication_id"] == pub["id"]]
        pubs.append({
            "id": pub["id"], "title": pub["title"], "source_id": pub["source_id"],
            "set_dir": f"chicago/reference/newspapers/Transcriptions/{pub['set_dir']}",
            "first_issue": mine[0]["date"], "last_issue": mine[-1]["date"],
            "issue_count": len(mine),
        })

    corpus = {
        "generated_by": "chicago/4d/tools/build_newspaper_corpus.py",
        "gated_by": "chicago/4d/tools/check_newspaper_corpus.py",
        "deposit_root": "chicago/reference/newspapers/Transcriptions",
        "deposit_is_read_only": (
            "The deposit is the owner's archive. This project reads it and never "
            "writes to it. It was pushed to main on 2026-08-27 and is not on every "
            "branch, which is why the gate verifies by sha256 and reports an absent "
            "deposit rather than resolving paths blindly."),
        "reading": "transcription_mediated",
        "reading_note": (
            "T-0256 ruling 2. Every claim taken from this corpus is read through an "
            "OCR-assisted transcription and not off the page scan, grades `documented` "
            "carrying `reading: transcription_mediated`, and preserves the "
            "transcription's own uncertainty brackets. Where a scan exists and is read, "
            "the scan is the authority and the transcription-mediated claim upgrades."),
        "citation_convention": (
            "publication, issue date, Vol./No., issue page and column as the "
            "transcription's own markers give them, then the text file and its line "
            "range. The deposit uses two marker dialects and both carry page and "
            "column: `===== ISSUE PAGE n / PDF PAGE m / COLUMN k OF 6 =====` in the "
            "diplomatic .txt set, and a `Newspaper Page n — Source PDF Page m` heading "
            "followed by `Column k` headings in the OCR-rebuild set. A claim that "
            "cannot name its column cannot be made."),
        "fields": {
            "text_path": "the text a citation resolves against, repo-root-relative",
            "text_origin": "`reference` — a .txt committed in the deposit; `derived` — "
                           "extracted from the .docx by tools/docx_text.py into this repo",
            "text_sha256": "of the file at text_path. The gate checks by content, not by "
                           "path: a rewritten transcription must not slip past its own "
                           "citations",
            "words": "COUNTED from the text, on every entry, by this tool",
            "manifest_word_count": "the figure the transcription set's own manifest gives, "
                                   "or null where the set ships no manifest — the whole "
                                   "Chicago American, and the 1835 Democrat tail",
            "completeness": "`complete` / `partial` / `unstated`, taken from the "
                            "transcription's own Status or Completeness line",
            "marker_dialect": "which of the deposit's five page/column marker dialects this "
                              "text uses; see citation_convention",
            "alternate_transcriptions": "other readings of the SAME issue, not other "
                                        "issues. Not counted in issue_count",
        },
        "issue_count": len(entries),
        "publications": pubs,
        "issues": entries,
    }
    return corpus, out_text


def write(corpus: dict, texts: dict[str, str]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if TEXT_DIR.is_dir():
        for stale in TEXT_DIR.glob("*.txt"):
            if f"chicago/4d/data/research/newspapers/text/{stale.name}" not in texts:
                stale.unlink()
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in sorted(texts.items()):
        (REPO / path).write_text(text, encoding="utf-8", newline="\n")
    CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--deposit", type=Path, default=DEPOSIT)
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff against the tree; write nothing")
    args = ap.parse_args(argv)

    if not args.deposit.is_dir():
        print(f"the deposit is not in this tree: {args.deposit}", file=sys.stderr)
        print("It lives on `main` under chicago/reference/newspapers/. Nothing to do; "
              "the gate is tools/check_newspaper_corpus.py.", file=sys.stderr)
        return 2

    corpus, texts = build(args.deposit)

    if args.check:
        bad = 0
        want = json.dumps(corpus, indent=2, ensure_ascii=False) + "\n"
        if not CORPUS.is_file() or CORPUS.read_text(encoding="utf-8") != want:
            print("data/research/newspapers/corpus.json does not match the deposit "
                  "— re-run tools/build_newspaper_corpus.py", file=sys.stderr)
            bad += 1
        for path, text in sorted(texts.items()):
            have = REPO / path
            if not have.is_file() or have.read_text(encoding="utf-8") != text:
                print(f"{path} does not match its .docx", file=sys.stderr)
                bad += 1
        if bad:
            return 1
        print(f"corpus check: {corpus['issue_count']} issues and {len(texts)} derived "
              f"text files re-derive from the deposit byte for byte")
        return 0

    write(corpus, texts)
    print(f"wrote {rel(CORPUS)} — {corpus['issue_count']} issues "
          f"({', '.join(f'{p['title']} {p['issue_count']}' for p in corpus['publications'])}), "
          f"{len(texts)} derived text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
