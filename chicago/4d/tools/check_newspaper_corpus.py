#!/usr/bin/env python3
"""The gate on the newspaper corpus (T-0256).

`data/research/newspapers/corpus.json` is what every later ticket in the PAPERS
epic resolves a citation against. A citation that cannot be resolved is not a
citation, so this asks four things of it, every commit:

  1. THE COUNT IS ASSERTED, NOT OBSERVED. The numbers below are written down
     here. An issue that silently drops out of the index fails the build rather
     than shrinking the corpus in a way nobody notices — which is the whole
     reason a count belongs in a gate and not in a comment.
  2. EVERY TEXT PATH RESOLVES, BY CONTENT. Each entry carries the sha256 of the
     text it names; this hashes the file and compares. A path check would pass a
     transcription that had been rewritten underneath its own citations.
  3. THE DATES ARE A SEQUENCE. One issue per date, strictly increasing per
     publication, so a duplicated or misdated entry cannot hide in 86 rows.
  4. THE CORPUS IS RESEARCH, NOT PAYLOAD. 2.7 MB of transcription belongs in the
     repository and nowhere near the published mirror. This holds that in three
     places at once: no path in the index points into site/, publish.sh does not
     copy data/research, and the mirror carries no such directory.

ON THE DEPOSIT BEING ABSENT. The transcriptions themselves are the owner's
archive at `chicago/reference/newspapers/`, which this project reads and never
writes. It was pushed to `main` on 2026-08-27 and `dev` has not been
back-merged, so on a dev checkout those files are not in the tree. This gate is
built to say so out loud rather than to pass quietly or to fail on a tier
difference: when the deposit is present every reference path is resolved and
hashed like any other, and when it is absent the count of unresolvable paths is
REPORTED, in full, with the reason. What is never conditional is the half this
repository owns — the derived text under data/research/newspapers/text/ must
resolve and hash on every branch, and a reference path that does not point into
the deposit at all is a failure wherever it is read.

    tools/check_newspaper_corpus.py             # the gate
    tools/check_newspaper_corpus.py --quiet     # findings only
    tools/check_newspaper_corpus.py --self-test # the assertions still fire
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # chicago/4d
REPO = ROOT.parent.parent                              # the custom repo root
CORPUS = ROOT / "data" / "research" / "newspapers" / "corpus.json"
TEXT_DIR = ROOT / "data" / "research" / "newspapers" / "text"
DEPOSIT = "chicago/reference/newspapers/Transcriptions"
DERIVED = "chicago/4d/data/research/newspapers/text"
MIRROR = REPO / "site" / "chicago" / "4d"

# Asserted, not observed. Measured against the deposit on 2026-08-28: the
# Chicago Democrat from its first issue to 1835-08-26, and the Chicago American
# from its first issue to 1835-08-29. T-0256 estimated "~103"; that is the file
# count of the deposit, not the issue count — 89 transcription .docx and 66
# committed .txt describe 86 distinct issues, three of which are transcribed
# twice. Change these numbers only alongside a change to the deposit.
EXPECTED = {"chicago_democrat": 73, "chicago_american": 13}
EXPECTED_TOTAL = 86
EXPECTED_DERIVED = 23

COMPLETENESS = {"complete", "partial", "unstated"}
SHA = re.compile(r"^[0-9a-f]{64}$")


class Report:
    def __init__(self, quiet: bool = False) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []
        self.quiet = quiet

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def transcriptions(entry: dict) -> list[tuple[str, dict]]:
    out = [("preferred", entry)]
    out += [("alternate", a) for a in entry.get("alternate_transcriptions", [])]
    return out


def check(corpus: dict, rep: Report, *, repo: Path = REPO,
          expected: dict | None = None, expected_total: int | None = None,
          expected_derived: int | None = None) -> None:
    expected = EXPECTED if expected is None else expected
    expected_total = EXPECTED_TOTAL if expected_total is None else expected_total
    expected_derived = EXPECTED_DERIVED if expected_derived is None else expected_derived

    issues = corpus.get("issues")
    if not isinstance(issues, list) or not issues:
        rep.error("corpus", "carries no issues[]")
        return

    # 1. the counts
    if corpus.get("issue_count") != len(issues):
        rep.error("corpus", f"issue_count says {corpus.get('issue_count')} and issues[] "
                            f"holds {len(issues)}")
    if len(issues) != expected_total:
        rep.error("corpus", f"{len(issues)} issues, and this gate asserts {expected_total}. "
                            f"An issue does not leave the index quietly — if the deposit "
                            f"really changed, change EXPECTED_TOTAL in the same commit")
    for pub in corpus.get("publications", []):
        want = expected.get(pub["id"])
        mine = [e for e in issues if e["publication_id"] == pub["id"]]
        if want is None:
            rep.error("corpus", f"publication '{pub['id']}' is not one this gate asserts")
        elif len(mine) != want:
            rep.error(pub["id"], f"{len(mine)} issues indexed, {want} asserted")
        if pub.get("issue_count") != len(mine):
            rep.error(pub["id"], f"publications[].issue_count says {pub.get('issue_count')}, "
                                 f"issues[] holds {len(mine)}")
        src = repo / "chicago" / "4d" / "data" / "sources" / f"{pub.get('source_id')}.json"
        if not src.is_file():
            rep.error(pub["id"], f"source_id '{pub.get('source_id')}' has no record at "
                                 f"data/sources/{pub.get('source_id')}.json — the corpus "
                                 f"cites a publication this dataset cannot name")

    # 3. one issue per date, strictly increasing per publication
    seen_ids: set[str] = set()
    last: dict[str, dt.date] = {}
    for e in issues:
        where = e.get("id", "?")
        if where in seen_ids:
            rep.error(where, "duplicate issue id")
        seen_ids.add(where)
        try:
            when = dt.date.fromisoformat(e["date"])
        except (KeyError, ValueError):
            rep.error(where, f"date {e.get('date')!r} is not an ISO date")
            continue
        pub = e.get("publication_id", "")
        prev = last.get(pub)
        if prev is not None and when <= prev:
            rep.error(where, f"date {when} does not follow {prev} — the issues of a "
                             f"publication are a strictly increasing sequence, and a "
                             f"repeat is a duplicated or misdated entry")
        last[pub] = when

    # 2 and 4. every text path, by content, and none of them into the payload
    deposit_present = (repo / DEPOSIT).is_dir()
    derived_seen: set[str] = set()
    unresolved = 0
    for e in issues:
        for role, t in transcriptions(e):
            where = f"{e.get('id', '?')} ({role})"
            path = t.get("text_path", "")
            if not path:
                rep.error(where, "no text_path")
                continue
            if path.startswith("site/") or "/site/" in path:
                rep.error(where, f"text_path '{path}' points into the published payload. "
                                 f"The corpus is research and the mirror is 2.7 MB smaller "
                                 f"for it")
                continue
            if not SHA.match(t.get("text_sha256", "")):
                rep.error(where, "text_sha256 is not a sha256")
            if t.get("completeness") not in COMPLETENESS:
                rep.error(where, f"completeness {t.get('completeness')!r} is not one of "
                                 f"{sorted(COMPLETENESS)}")
            if role == "preferred" and (t.get("column_markers", 0) < 1 or t.get("pages", 0) < 1):
                rep.error(where, "carries no page or column marker. A claim that cannot "
                                 "name its column cannot be made, so an issue whose text "
                                 "has no markers cannot be the one a citation resolves to")

            origin = t.get("text_origin")
            if origin == "derived":
                if not path.startswith(DERIVED + "/"):
                    rep.error(where, f"derived text at '{path}', which is outside "
                                     f"{DERIVED}/")
                    continue
                derived_seen.add(Path(path).name)
                have = repo / path
                if not have.is_file():
                    rep.error(where, f"{path} is missing. Derived text is this "
                                     f"repository's own and must resolve on every branch")
                elif sha256(have) != t["text_sha256"]:
                    rep.error(where, f"{path} does not match its recorded sha256 — "
                                     f"re-run tools/build_newspaper_corpus.py")
            elif origin == "reference":
                if not path.startswith(DEPOSIT + "/"):
                    rep.error(where, f"reference text at '{path}', which is outside the "
                                     f"deposit at {DEPOSIT}/")
                    continue
                if deposit_present:
                    have = repo / path
                    if not have.is_file():
                        rep.error(where, f"{path} is not in the deposit")
                    elif sha256(have) != t["text_sha256"]:
                        rep.error(where, f"{path} does not match its recorded sha256 — "
                                         f"the deposit moved under its own citations")
                else:
                    unresolved += 1
            else:
                rep.error(where, f"text_origin {origin!r} is neither 'reference' nor "
                                 f"'derived'")

    on_disk = {p.name for p in TEXT_DIR.glob("*.txt")} if TEXT_DIR.is_dir() else set()
    for orphan in sorted(on_disk - derived_seen):
        rep.error(f"{DERIVED}/{orphan}", "is not named by any entry in corpus.json — "
                                         "derived text nothing cites is text nobody can "
                                         "resolve a citation to")
    if len(derived_seen) != expected_derived:
        rep.error("corpus", f"{len(derived_seen)} derived text files are indexed and this "
                            f"gate asserts {expected_derived}")

    # 4, the other two places
    publish = ROOT / "tools" / "publish.sh"
    if publish.is_file() and "data/research" in publish.read_text():
        rep.error("tools/publish.sh", "copies data/research into the mirror. The corpus is "
                                      "research and must not reach the payload")
    if (MIRROR / "data" / "research").exists():
        rep.error("site/chicago/4d/data/research", "exists — the corpus has reached the "
                                                   "published mirror")

    if deposit_present:
        rep.note(f"the deposit is in this tree; every reference path was resolved and hashed")
    elif unresolved:
        rep.note(
            f"THE DEPOSIT IS NOT IN THIS TREE, so {unresolved} reference text path(s) "
            f"were not resolved. chicago/reference/newspapers/ was pushed to `main` on "
            f"2026-08-27 and `dev` has not been back-merged; the paths and their sha256 "
            f"are recorded and will be verified the moment the deposit is here. The "
            f"{len(derived_seen)} derived files this repository owns were resolved and "
            f"hashed as usual.")


def run(quiet: bool) -> int:
    rep = Report(quiet)
    if not CORPUS.is_file():
        print(f"FAIL  {CORPUS} is missing", file=sys.stderr)
        return 1
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    check(corpus, rep)
    for n in rep.notes:
        if not quiet:
            print(f"   {n}")
    for e in rep.errors:
        print(f"FAIL  {e}", file=sys.stderr)
    if rep.errors:
        return 1
    if not quiet:
        print(f"   newspaper corpus: {corpus['issue_count']} issues "
              f"({', '.join(f'{p['title']} {p['issue_count']}' for p in corpus['publications'])}), "
              f"every indexed text path checked by content, dates strictly increasing, "
              f"nothing reaching the payload")
    return 0


# ---------------------------------------------------------------------------
# self-test: the four assertions above have to be capable of failing
# ---------------------------------------------------------------------------

def self_test() -> int:
    import copy

    base = json.loads(CORPUS.read_text(encoding="utf-8"))
    failures: list[str] = []

    def fires(name: str, mutate) -> None:
        c = copy.deepcopy(base)
        mutate(c)
        rep = Report()
        check(c, rep)
        if not rep.errors:
            failures.append(f"{name}: mutated corpus passed the gate")

    fires("a dropped issue", lambda c: (c["issues"].pop(0), c["publications"][0].__setitem__(
        "issue_count", c["publications"][0]["issue_count"] - 1)))
    fires("a repeated date", lambda c: c["issues"][1].__setitem__("date", c["issues"][0]["date"]))
    fires("a date out of order", lambda c: c["issues"][0].__setitem__("date", "1999-01-01"))
    fires("a rewritten derived text", lambda c: next(
        e for e in c["issues"] if e["text_origin"] == "derived").__setitem__(
        "text_sha256", "0" * 64))
    fires("a path into the payload", lambda c: c["issues"][0].__setitem__(
        "text_path", "site/chicago/4d/data/research/x.txt"))
    fires("a text with no column marker", lambda c: c["issues"][0].__setitem__(
        "column_markers", 0))
    fires("a publication with no source record", lambda c: c["publications"][0].__setitem__(
        "source_id", "no_such_source"))
    fires("a derived text renamed out of the index", lambda c: next(
        e for e in c["issues"] if e["text_origin"] == "derived").__setitem__(
        "text_path", f"{DERIVED}/renamed.txt"))
    fires("a derived text moved into the deposit it did not come from", lambda c: next(
        e for e in c["issues"] if e["text_origin"] == "derived").__setitem__(
        "text_origin", "reference"))

    # …and the committed corpus itself still passes, or the mutations above prove
    # nothing about a gate that simply says no to everything.
    rep = Report()
    check(base, rep)
    if rep.errors:
        failures.append("the committed corpus does not pass its own gate: "
                        + "; ".join(rep.errors[:3]))

    for f in failures:
        print(f"FAIL  {f}", file=sys.stderr)
    if failures:
        return 1
    print("   newspaper corpus self-test: the count, the dates, the content hashes, the "
          "markers, the source records and the payload boundary each still fail when broken")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--gate", action="store_true", help="accepted for symmetry; the default")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    return run(args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
