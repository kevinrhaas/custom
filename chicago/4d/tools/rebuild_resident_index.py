#!/usr/bin/env python3
"""THE ONE OWNER OF data/residents/index.json (T-0715).

`index.json` is a MANIFEST: every household row and every count in it is a
restatement of something the household records in `data/residents/households/`
already say. Nothing in a row is authored. So the file is a derivation, and
until this tool existed it was not derived — it was PATCHED, by whichever pass
happened to be running:

  * `mint_civic_residents.apply()`   rebuilt the civic rows and copied the rest
                                     verbatim (`keep = [... not in mine_ids]`)
  * `mint_civic_residents.apply_regrade()`  rewrote only the rows it touched,
                                     and on a run where the proposal is already
                                     spent it touches nothing at all
  * `mint_placed_residents`, `generate_inferred_households`,
    `synthesize_resident_research`, `apply_census_1840_bridges`  — each the
                                     same shape: own a slice, copy the rest

A household that no pass owns — an `hh_inf_*`, a documented resident, a
letter-list mint — could therefore have its grade changed by any OTHER pass and
keep for ever a manifest row saying something else. Landing #797 found 18 such
households, 12 of them people this project had itself regraded, and the counts
had inherited the error because `counts.by_grade` is summed from the ROWS.

The fix is not another patcher. It is this: ONE function that reads the records
off disk and states the whole layer, and a gate that refuses a committed file
which is not what it produces.

    python3 tools/rebuild_resident_index.py            # rewrite the manifest
    python3 tools/rebuild_resident_index.py --check    # gate: committed == derived
    python3 tools/rebuild_resident_index.py --selftest # the derivation's own tests

WHAT IS DERIVED, AND FROM WHAT

  row.id, row.file            the record's own id and its path
  row.head, row.division      copied from the record
  row.lives_at/.works_at      the `value` of the record's confidence block
  row.present_on_scene_date   likewise
  row.review_required         copied from the record
  row.persons                 len(record.persons)
  row.grades                  the tally of person.grade, sorted
  row.letter_list_only        True iff source_pass == 'letter_list'   (else absent)
  row.civic_mint              True iff source_pass == 'civic'         (else absent)
  row.projected_resident      True iff any person is a projected_resident (else absent)
  row.census_1840_linked      how many persons carry `later_census`   (0 -> absent)

  counts.households           len(rows)
  counts.persons              sum of row.persons
  counts.by_grade             sum of row.grades, with all three rungs present
  counts.letter_list_only     persons carrying `letter_list_only`
  counts.civic_mint           persons carrying `civic_mint`
  counts.projected_residents  persons whose resident_subtype is projected_resident
  counts.census_1840_linked   persons carrying `later_census`

A boolean flag is written ONLY when true. That is what three of the four
existing writers already do (`if pr: row[...] = True else: row.pop(...)`), and
the fourth wrote `projected_resident: false` onto 450 civic rows — 450 rows
saying, at length, nothing. Anything else the top of the file carries —
`_doc`, `version`, `scene_date`, `dossier`, `vocabulary`,
`researched_not_resident`, and a memorial count like
`reconstructed_removed_in_2026_09_02_synthesis` — is AUTHORED and is carried
through untouched.

A row key this derivation does not know is a hard error rather than a silent
drop: a pass that starts writing a new manifest field has to teach it here,
which is the whole point of there being one owner.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESIDENTS = DATA / "residents"
HOUSEHOLDS = RESIDENTS / "households"
INDEX = RESIDENTS / "index.json"

GRADES = ("attested", "inferred", "reconstructed")
PROJECTED = "projected_resident"

# The canonical key order of a manifest row, flags included. Absent flags simply
# drop out, so every row in the file shares one order.
ROW_KEYS = ("id", "file", "letter_list_only", "civic_mint", "head", "division",
            "persons", "grades", "lives_at", "works_at", "present_on_scene_date",
            "review_required", "projected_resident", "census_1840_linked")

# The counts this derivation owns. Any other key in `counts` is authored and kept.
DERIVED_COUNTS = ("households", "persons", "by_grade", "letter_list_only",
                  "projected_residents", "census_1840_linked", "civic_mint")

REBUILD_CMD = "python3 tools/rebuild_resident_index.py"


def _value(block) -> object:
    """The `value` of a confidence block, or None when the block is absent."""
    return (block or {}).get("value")


def derive_row(doc: dict) -> dict:
    """The manifest row a household record implies. Total: no row is authored."""
    persons = doc.get("persons") or []
    tally: dict = {}
    for person in persons:
        tally[person["grade"]] = tally.get(person["grade"], 0) + 1
    row = {
        "id": doc["id"],
        "file": f"households/{doc['id']}.json",
        "head": doc.get("head"),
        "division": doc.get("division"),
        "persons": len(persons),
        "grades": dict(sorted(tally.items())),
        "lives_at": _value(doc.get("lives_at")),
        "works_at": _value(doc.get("works_at")),
        "present_on_scene_date": _value(doc.get("present_on_scene_date")),
        "review_required": doc.get("review_required"),
    }
    if doc.get("source_pass") == "letter_list":
        row["letter_list_only"] = True
    if doc.get("source_pass") == "civic":
        row["civic_mint"] = True
    if any(p.get("resident_subtype") == PROJECTED for p in persons):
        row[PROJECTED] = True
    linked = sum(1 for p in persons if p.get("later_census"))
    if linked:
        row["census_1840_linked"] = linked
    return {k: row[k] for k in ROW_KEYS if k in row}


def rebuild(index: dict, docs: dict) -> dict:
    """State the whole manifest from `docs` — a {path: record} of the layer.

    The authored half of the file is carried through in its committed order;
    only `households` and the derived `counts` keys are restated.
    """
    rows = sorted((derive_row(doc) for doc in docs.values()), key=lambda r: r["id"])
    people = [p for doc in docs.values() for p in doc.get("persons") or []]

    totals = {g: 0 for g in GRADES}
    for row in rows:
        for grade, n in row["grades"].items():
            totals[grade] = totals.get(grade, 0) + n

    derived = {
        "households": len(rows),
        "persons": sum(row["persons"] for row in rows),
        "by_grade": totals,
        "letter_list_only": sum(1 for p in people if p.get("letter_list_only")),
        "projected_residents": sum(1 for p in people
                                   if p.get("resident_subtype") == PROJECTED),
        "census_1840_linked": sum(1 for p in people if p.get("later_census")),
        "civic_mint": sum(1 for p in people if p.get("civic_mint")),
    }

    counts = dict(index.get("counts") or {})
    for key in DERIVED_COUNTS:
        counts[key] = derived[key]
    # Keep the committed key order where the file already has one, so a rebuild
    # that changes nothing changes no bytes.
    order = list((index.get("counts") or {}).keys())
    order += [k for k in DERIVED_COUNTS if k not in order]

    out = dict(index)
    out["counts"] = {k: counts[k] for k in order}
    out["households"] = rows
    return out


def load_records() -> dict:
    return {p: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(HOUSEHOLDS.glob("*.json"))}


def dumps(index: dict) -> str:
    return json.dumps(index, indent=1, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# the gate


def unknown_row_keys(index: dict) -> list:
    """Row keys this derivation cannot state — a pass wrote a field nobody owns."""
    return sorted({k for row in index.get("households") or []
                   for k in row if k not in ROW_KEYS})


def diagnose(committed: dict, derived: dict) -> list:
    """ONE message per KIND of drift, each naming the rebuild. #797 read this
    same fault as 19 per-household errors in `validate.py` plus a different
    sentence in six other steps, none of which named the cause."""
    problems = []
    rows_c = {r.get("id"): r for r in committed.get("households") or []}
    rows_d = {r["id"]: r for r in derived["households"]}

    missing = sorted(set(rows_d) - set(rows_c))
    extra = sorted(set(rows_c) - set(rows_d))
    if missing:
        problems.append(f"{len(missing)} household record(s) have no manifest row "
                        f"({', '.join(missing[:5])}{'...' if len(missing) > 5 else ''})")
    if extra:
        problems.append(f"{len(extra)} manifest row(s) name no household record "
                        f"({', '.join(extra[:5])}{'...' if len(extra) > 5 else ''})")

    stale = [hid for hid in sorted(set(rows_c) & set(rows_d))
             if rows_c[hid] != rows_d[hid]]
    if stale:
        problems.append(f"{len(stale)} manifest row(s) disagree with their household "
                        f"record ({', '.join(stale[:5])}"
                        f"{'...' if len(stale) > 5 else ''}); the record is authoritative")

    counts_c, counts_d = committed.get("counts") or {}, derived["counts"]
    off = [k for k in DERIVED_COUNTS if counts_c.get(k) != counts_d[k]]
    if off:
        problems.append("counts " + ", ".join(
            f"{k} {counts_c.get(k)!r} should be {counts_d[k]!r}" for k in off))

    if not problems and dumps(committed) != dumps(derived):
        problems.append("the committed file is not byte-identical to the rebuild "
                        "(key order or formatting)")
    return problems


def check() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    unknown = unknown_row_keys(index)
    if unknown:
        print(f"  FAIL  data/residents/index.json rows carry key(s) no derivation "
              f"owns: {', '.join(unknown)}. Teach {REBUILD_CMD} to derive them "
              f"(ROW_KEYS) rather than hand-patching the manifest.")
        return 1
    derived = rebuild(index, load_records())
    problems = diagnose(index, derived)
    if problems:
        print("  FAIL  data/residents/index.json is not what the household records "
              "say. It is a DERIVATION, not a file to edit:")
        for p in problems:
            print(f"          - {p}")
        print(f"        Run `{REBUILD_CMD}` and commit the result. If a pass wrote "
              f"these rows by hand, make it call rebuild() instead (T-0715).")
        return 1
    n = len(derived["households"])
    print(f"  ok    data/residents/index.json re-derives from all {n} household "
          f"record(s), counts included")
    return 0


def write() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    unknown = unknown_row_keys(index)
    if unknown:
        print(f"refusing to rebuild: rows carry key(s) no derivation owns: "
              f"{', '.join(unknown)}")
        return 1
    before = INDEX.read_text(encoding="utf-8")
    after = dumps(rebuild(index, load_records()))
    if before == after:
        print("data/residents/index.json already states the records; nothing written")
        return 0
    INDEX.write_text(after, encoding="utf-8")
    changed = sum(1 for a, b in zip(before.splitlines(), after.splitlines()) if a != b)
    print(f"rewrote data/residents/index.json from the household records "
          f"({changed}+ line(s) changed)")
    return 0


# ---------------------------------------------------------------------------
# self-tests: the derivation, not the data


def selftest() -> int:
    ok = True

    def eq(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print(f"  FAIL  {label}: {got!r} != {want!r}")
        else:
            print(f"  ok    {label}")

    doc = {
        "id": "hh_x", "head": "x", "division": "north", "source_pass": "civic",
        "lives_at": {"value": "b1"}, "works_at": {"value": None},
        "present_on_scene_date": {"value": "present"}, "review_required": False,
        "persons": [{"id": "x", "grade": "attested", "civic_mint": True},
                    {"id": "y", "grade": "inferred",
                     "resident_subtype": "projected_resident"}],
    }
    row = derive_row(doc)
    eq("a flag is written only when true", "letter_list_only" in row, False)
    eq("civic_mint comes off source_pass", row["civic_mint"], True)
    eq("grades tally the persons", row["grades"], {"attested": 1, "inferred": 1})
    eq("a projected person marks the row", row["projected_resident"], True)
    eq("no 1840 link, no key", "census_1840_linked" in row, False)
    eq("key order is canonical",
       list(row), [k for k in ROW_KEYS if k in row])

    plain = derive_row({"id": "hh_y", "head": "y", "division": "south",
                        "source_pass": "documented", "review_required": True,
                        "persons": [{"id": "z", "grade": "attested",
                                     "later_census": {"sheet": 1}}]})
    eq("an unstated confidence block reads as None", plain["lives_at"], None)
    eq("an 1840 link is counted", plain["census_1840_linked"], 1)
    eq("no projected person, no key", "projected_resident" in plain, False)

    index = {"_doc": "d", "counts": {"households": 0, "persons": 0,
                                     "by_grade": {}, "memorial": 108},
             "households": [{"id": "gone"}]}
    out = rebuild(index, {"a": doc, "b": {
        "id": "hh_y", "head": "y", "division": "south", "source_pass": "letter_list",
        "review_required": False, "persons": [{"id": "z", "grade": "inferred",
                                               "letter_list_only": True}]}})
    eq("every record gets a row, sorted", [r["id"] for r in out["households"]],
       ["hh_x", "hh_y"])
    eq("a row naming no record is dropped",
       any(r["id"] == "gone" for r in out["households"]), False)
    eq("counts come from the rows", out["counts"]["persons"], 3)
    eq("by_grade carries every rung", out["counts"]["by_grade"],
       {"attested": 1, "inferred": 2, "reconstructed": 0})
    eq("an authored count survives the rebuild", out["counts"]["memorial"], 108)
    eq("the authored half survives too", out["_doc"], "d")
    eq("person counts are people, not rows", out["counts"]["civic_mint"], 1)

    eq("a rebuild of a rebuild is a no-op", rebuild(out, {"a": doc, "b": {
        "id": "hh_y", "head": "y", "division": "south", "source_pass": "letter_list",
        "review_required": False, "persons": [{"id": "z", "grade": "inferred",
                                               "letter_list_only": True}]}}), out)

    stale = json.loads(json.dumps(out))
    stale["households"][0]["grades"] = {"attested": 2}
    eq("drift is diagnosed as one message", len(diagnose(stale, out)), 1)
    eq("and the message names the record as authoritative",
       "authoritative" in diagnose(stale, out)[0], True)

    eq("an unknown row key is caught",
       unknown_row_keys({"households": [{"id": "a", "invented": 1}]}), ["invented"])

    print("selftest: " + ("all pass" if ok else "FAILURES"))
    return 0 if ok else 1


def main(argv: list) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--check" in argv:
        return check()
    return write()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
