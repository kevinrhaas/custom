#!/usr/bin/env python3
"""One owner for `data/residents/index.json`: every row re-derived from the card on disk.

WHY THIS EXISTS (T-0715, found landing #797). The index had two part-owners and no whole
owner. `mint_civic_residents.apply()` rebuilt the rows for the households IT minted and
carried the rest across verbatim; `apply_regrade()` touched only the rows it changed that
run, which on the normal steady state — the proposal already spent — is none of them. So a
household neither pass owns (an `hh_inf_*`, a documented resident, a letter-list mint) could
have its grade changed by any other pass and keep an index row that said something else, for
ever. The totals inherited it, because `counts.by_grade` is summed from the ROWS: #797 read
`attested: 505, inferred: 899` against the records' `attested: 523, inferred: 881`.

THE RULE THIS TOOL ENFORCES. **The records are the truth and the index is their summary.**
Every derived field on a row is a copy of something in `households/<id>.json`, so a row can
always be thrown away and rebuilt. Nothing here reads a source, grades anybody, or changes a
card: a disagreement between index and record is ALWAYS resolved in the record's favour.

WHAT IS DERIVED, and from where:

    id, file                    the household file's own id and name
    head, division              record top level
    persons                     len(record.persons)
    grades                      the person grades, tallied
    lives_at, works_at,
    present_on_scene_date       the .value of the record's attested block
    review_required             record top level
    letter_list_only            any person carries the letter-list flag
    civic_mint                  any person carries the civic-mint flag
    projected_resident          any person is resident_subtype projected_resident
    census_1840_linked          HOW MANY persons carry a later_census block (a count,
                                not a flag — that is what apply_census_1840_bridges wrote)

The four flags are written only when they are true/non-zero, which is the form
`synthesize_resident_research.rebuild_index` settled on; the mint's own writer used to emit
`projected_resident: false` as well, and that disagreement is why 450 rows carried the key
and 211 identical-in-meaning rows did not. `counts` is re-derived from the records the same
way. Keys this tool does not own — `_doc`, `version`, `scene_date`, `dossier`, `vocabulary`,
`researched_not_resident`, and any count it does not compute — are carried across untouched.

    tools/rebuild_resident_index.py --write      rebuild the committed index
    tools/rebuild_resident_index.py --check      it still re-derives (the gate)
    tools/rebuild_resident_index.py --self-test  the assertions still fire when broken

ONE FAULT, ONE MESSAGE. Before this, drift showed up as one error PER HOUSEHOLD out of
`validate.py` (19 of them in #797) plus a differently-worded sentence out of
`synthesize_resident_research.py`, none of which named the cause or the fix. `--check` prints
what disagrees, capped, and then the single line that repairs it.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                 # chicago/4d
HOUSEHOLDS = ROOT / "data/residents/households"
INDEX = ROOT / "data/residents/index.json"

PROJECTED = "projected_resident"
GRADES = ("attested", "inferred", "reconstructed")

# The counts this tool owns. Anything else under `counts` belongs to the pass that wrote it
# (`reconstructed_removed_in_2026_09_02_synthesis` is a frozen historical figure, not a
# tally of the layer as it stands) and is carried across untouched.
OWNED_COUNTS = ("households", "persons", "by_grade", "letter_list_only",
                "projected_residents", "census_1840_linked", "civic_mint")

REPAIR = "rebuild it with: python3 tools/rebuild_resident_index.py --write"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(doc) -> str:
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def value(block):
    """The `.value` of an attested block, or None where the record carries none."""
    return (block or {}).get("value") if isinstance(block, dict) else None


def row_for(doc: dict, filename: str) -> dict:
    """The index row a household record implies. The only derivation there is."""
    people = doc.get("persons") or []
    tally: dict = {}
    for person in people:
        grade = person.get("grade")
        if grade:
            tally[grade] = tally.get(grade, 0) + 1
    # Key order is the one the committed manifest already carries — the pass flags sit
    # between `file` and `head`, the derived ones after `review_required`. It is cosmetic
    # to a reader and not to a diff: a rebuild that re-orders 1,380 rows buries the row
    # that actually changed.
    row = {"id": doc.get("id"), "file": f"households/{filename}"}
    if any(p.get("letter_list_only") for p in people):
        row["letter_list_only"] = True
    if any(p.get("civic_mint") for p in people):
        row["civic_mint"] = True
    row.update({
        "head": doc.get("head"),
        "division": doc.get("division"),
        "persons": len(people),
        "grades": dict(sorted(tally.items())),
        "lives_at": value(doc.get("lives_at")),
        "works_at": value(doc.get("works_at")),
        "present_on_scene_date": value(doc.get("present_on_scene_date")),
        "review_required": bool(doc.get("review_required")),
    })
    if any(p.get("resident_subtype") == PROJECTED for p in people):
        row[PROJECTED] = True
    linked = sum(1 for p in people if p.get("later_census"))
    if linked:
        row["census_1840_linked"] = linked
    return row


def rows_from(docs: dict) -> list:
    """Every card on disk, as rows, in the manifest's own id order."""
    rows = [row_for(doc, path.name) for path, doc in docs.items()]
    return sorted(rows, key=lambda r: str(r["id"]))


def counts_from(rows: list, docs: dict) -> dict:
    by_grade = {g: 0 for g in GRADES}
    persons = 0
    for row in rows:
        persons += row["persons"]
        for grade, n in row["grades"].items():
            by_grade[grade] = by_grade.get(grade, 0) + n
    people = [p for doc in docs.values() for p in doc.get("persons") or []]
    return {
        "households": len(rows),
        "persons": persons,
        "by_grade": by_grade,
        "letter_list_only": sum(1 for p in people if p.get("letter_list_only")),
        "projected_residents": sum(1 for p in people
                                   if p.get("resident_subtype") == PROJECTED),
        "census_1840_linked": sum(1 for p in people if p.get("later_census")),
        "civic_mint": sum(1 for p in people if p.get("civic_mint")),
    }


def read_households(root: Path | None = None) -> dict:
    root = root or HOUSEHOLDS
    return {path: load(path) for path in sorted(root.glob("*.json"))}


def rebuild(index: dict, docs: dict) -> dict:
    """`index` with its rows and owned counts re-derived. Everything else survives."""
    out = copy.deepcopy(index)
    rows = rows_from(docs)
    out["households"] = rows
    # In place, so a count keeps the position it has always had and a rebuild does not
    # re-order the block; an owned count the file has never carried is appended.
    counts = dict(out.get("counts") or {})
    derived = counts_from(rows, docs)
    counts.update({k: v for k, v in derived.items() if k in counts})
    counts.update({k: v for k, v in derived.items() if k not in counts})
    out["counts"] = counts
    return out


# ---------------------------------------------------------------------------
# the difference, said once
# ---------------------------------------------------------------------------

def shown(row: dict, key: str) -> str:
    """A row value for a message. A key the row does not carry is ABSENT, not None —
    three of these four flags are written only when true, so `None` would read as a
    value the manifest holds rather than one it declines to write."""
    return repr(row[key]) if key in row else "absent"


def differences(committed: dict, wanted: dict) -> list:
    """Every disagreement, as sentences. Empty means the index re-derives."""
    out: list = []
    have = {r.get("id"): r for r in committed.get("households") or []}
    want = {r.get("id"): r for r in wanted.get("households") or []}
    for hid in sorted(set(want) - set(have)):
        out.append(f"household '{hid}' has a card on disk and no row in the manifest")
    for hid in sorted(set(have) - set(want)):
        out.append(f"household '{hid}' has a manifest row and no card on disk")
    for hid in sorted(set(have) & set(want)):
        a, b = have[hid], want[hid]
        for key in sorted(set(a) | set(b)):
            if a.get(key) != b.get(key):
                out.append(f"household '{hid}' {key} is {shown(a, key)} in the manifest and "
                           f"{shown(b, key)} on the card")
    hc, wc = committed.get("counts") or {}, wanted.get("counts") or {}
    for key in OWNED_COUNTS:
        if key in wc and hc.get(key) != wc.get(key):
            out.append(f"counts.{key} is {hc.get(key)!r} and the records hold {wc.get(key)!r}")
    return out


def cmd_check(index_path: Path | None = None, root: Path | None = None,
              quiet: bool = False) -> list:
    index_path = index_path or INDEX
    committed = load(index_path)
    wanted = rebuild(committed, read_households(root))
    bad = differences(committed, wanted)
    if quiet:
        return bad
    if not bad:
        print(f"  ok    data/residents/index.json re-derives from the "
              f"{len(wanted['households'])} card(s) on disk")
        return bad
    # ONE fault, said once, with the fix. The per-row lines are evidence, not the finding.
    print(f"data/residents/index.json has drifted from the household records — "
          f"{len(bad)} disagreement(s). The RECORD is authoritative; "
          f"{REPAIR}", file=sys.stderr)
    for line in bad[:20]:
        print(f"    {line}", file=sys.stderr)
    if len(bad) > 20:
        print(f"    … and {len(bad) - 20} more", file=sys.stderr)
    return bad


def cmd_write(index_path: Path | None = None, root: Path | None = None) -> int:
    index_path = index_path or INDEX
    committed = load(index_path)
    wanted = rebuild(committed, read_households(root))
    changed = differences(committed, wanted)
    text = dumps(wanted)
    if text == index_path.read_text(encoding="utf-8"):
        print("data/residents/index.json already re-derives; nothing written")
        return 0
    index_path.write_text(text, encoding="utf-8")
    print(f"data/residents/index.json rebuilt from "
          f"{len(wanted['households'])} card(s) — {len(changed)} disagreement(s) repaired")
    return 0


# ---------------------------------------------------------------------------
# self-test — the assertions fire when the layer is broken
# ---------------------------------------------------------------------------

def cmd_self_test() -> list:
    bad: list = []

    def want(got, expected, what):
        if got != expected:
            brief = repr(got)
            if len(brief) > 200:
                brief = brief[:200] + " …"
            bad.append(f"{what}: got {brief}, expected {expected!r}")

    committed = load(INDEX)
    docs = read_households()
    want(bool(docs), True, "the real households directory is readable")
    want(len(differences(committed, rebuild(committed, docs))), 0,
         "the committed index re-derives from the committed cards")

    # A grade changed on a card the mints do not own is the exact fault of T-0715: the
    # regrade passes would leave the row alone and only validate.py would ever notice.
    path, doc = next(iter(docs.items()))
    broken = copy.deepcopy(docs)
    broken[path] = copy.deepcopy(doc)
    broken[path]["persons"][0]["grade"] = ("inferred"
                                           if doc["persons"][0].get("grade") == "attested"
                                           else "attested")
    want(any("grades is" in d for d in differences(committed, rebuild(committed, broken))),
         True, "a grade changed on a card is caught as a row disagreement")

    # …and the totals must move with it, because a stale row used to poison the sum.
    want(any(d.startswith("counts.by_grade")
             for d in differences(committed, rebuild(committed, broken))),
         True, "a grade changed on a card moves counts.by_grade")

    # A card with no row, and a row with no card, are both 404s on a static host.
    fewer = dict(list(docs.items())[1:])
    want(any("no row in the manifest" in d or "no card on disk" in d
             for d in differences(committed, rebuild(committed, fewer))),
         True, "a card and a row that do not pair up are caught")

    # The flags are derived, never carried: dropping the person flag drops the row flag.
    flagged = next((p for p, d in docs.items()
                    if any(x.get("civic_mint") for x in d.get("persons") or [])), None)
    want(flagged is not None, True, "the layer still holds a civic-minted household")
    if flagged is not None:
        stripped = copy.deepcopy(docs)
        stripped[flagged] = copy.deepcopy(docs[flagged])
        for person in stripped[flagged]["persons"]:
            person.pop("civic_mint", None)
        want(any("civic_mint is True in the manifest and absent on the card" in d
                 for d in differences(committed, rebuild(committed, stripped))),
             True, "a row flag the card no longer supports is caught")

    # Nothing outside the manifest's rows and owned counts is touched by a rebuild.
    rebuilt = rebuild(committed, docs)
    for key in ("_doc", "version", "scene_date", "dossier", "vocabulary",
                "researched_not_resident"):
        want(rebuilt.get(key), committed.get(key), f"a rebuild leaves {key} alone")
    want(rebuilt["counts"].get("reconstructed_removed_in_2026_09_02_synthesis"),
         (committed.get("counts") or {}).get("reconstructed_removed_in_2026_09_02_synthesis"),
         "a rebuild leaves a count it does not own alone")

    for line in bad:
        print(f"  FAIL  {line}", file=sys.stderr)
    if not bad:
        print("resident index self-test: all assertions fire")
    return bad


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return 1 if cmd_self_test() else 0
    if args.check:
        return 1 if cmd_check() else 0
    if args.write:
        return cmd_write()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
