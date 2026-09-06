#!/usr/bin/env python3
"""The one owner of data/residents/index.json (T-0715).

The manifest is a SUMMARY of data/residents/households/*.json and nothing else.
Every row's `head`, `division`, `persons`, `grades`, `lives_at`, `works_at`,
`present_on_scene_date`, `review_required` and its four evidence flags are
denormalised copies of the record on disk, and `counts` is a tally of those rows.

Before this module, four minting passes and four rewriting passes each patched
the SLICE of the manifest they owned and left the rest verbatim:

    keep = [r for r in index["households"] if r["id"] not in mine_ids]

So a household that no pass owned - an `hh_inf_*` inferred household, a
documented resident, a letter-list mint - could have its grade changed by any
other pass and keep a manifest row saying something else for ever, and the
totals, summed from the ROWS, inherited the error. Landing #797 found 18 such
households, 12 of them people this project had itself regraded, and no writer
in the tree would have healed them.

The fix is not a better patch. It is that the manifest has ONE derivation, over
the WHOLE layer, that every writer calls:

    from rebuild_resident_index import rebuild
    rebuild(index, docs)          # docs: {Path: household dict}, the whole layer

and that `tools/check.sh` re-derives it, so drift is a red build rather than a
hunt through 19 per-household errors.

    python3 tools/rebuild_resident_index.py --check    re-derive and compare
    python3 tools/rebuild_resident_index.py --write    re-derive and write

WHAT IT DOES NOT TOUCH: `_doc`, `version`, `scene_date`, `dossier`,
`vocabulary`, `researched_not_resident`, and any `counts` key that is not
derivable from the cards (the frozen
`reconstructed_removed_in_2026_09_02_synthesis` figure is the one today). Those
are authored, not summarised, and a derivation that overwrote them would be
deleting evidence to make a tally tidy.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESIDENTS = ROOT / "data" / "residents"
HOUSEHOLDS = RESIDENTS / "households"
INDEX = RESIDENTS / "index.json"

PROJECTED = "projected_resident"
GRADES = ("attested", "inferred", "reconstructed")

# The row's key order, fixed here rather than inherited from whichever pass
# happened to mint the household. Every committed shape is a subset of this
# order, so adopting it is a normalisation and not a reshuffle.
ROW_KEYS = ("id", "file", "letter_list_only", "civic_mint", "head", "division",
            "persons", "grades", "lives_at", "works_at", "present_on_scene_date",
            "review_required", PROJECTED, "census_1840_linked")

# The count keys this derivation owns. Anything else in `counts` is authored and
# is carried through untouched, in its committed position.
DERIVED_COUNTS = ("households", "persons", "by_grade", "letter_list_only",
                  "projected_residents", "census_1840_linked", "civic_mint")


def _value(field):
    """A record's fields are {value, confidence, ...} blocks; the row copies the value."""
    return field.get("value") if isinstance(field, dict) else field


def load_households(root: Path | None = None) -> dict[Path, dict]:
    """Every household card on disk, which is the whole input to the derivation."""
    houses = (root or HOUSEHOLDS)
    return {p: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(houses.glob("*.json"))}


def household_docs(docs) -> dict[Path, dict]:
    """The household cards out of a pass's in-memory file map.

    Passes carry mixed maps - the manifest itself, a register, a proposal - so
    the filter is on the layer's own directory, not on the caller's discipline.
    """
    out = {}
    for path, doc in (docs or {}).items():
        path = Path(path)
        if path.name == "index.json" or path.suffix != ".json":
            continue
        if path.parent.name != "households":
            continue
        if isinstance(doc, (str, bytes)):
            doc = json.loads(doc)
        if isinstance(doc, dict) and doc.get("id"):
            out[path] = doc
    return out


def row_for(path: Path, doc: dict) -> dict:
    """One manifest row, derived from one household card and nothing else."""
    persons = doc.get("persons") or []
    tally: dict[str, int] = {}
    for person in persons:
        grade = person.get("grade")
        if grade:
            tally[grade] = tally.get(grade, 0) + 1
    row = {
        "id": doc.get("id"),
        "file": f"households/{path.name}",
        "head": doc.get("head"),
        "division": doc.get("division"),
        "persons": len(persons),
        "grades": dict(sorted(tally.items())),
        "lives_at": _value(doc.get("lives_at")),
        "works_at": _value(doc.get("works_at")),
        "present_on_scene_date": _value(doc.get("present_on_scene_date")),
        "review_required": bool(doc.get("review_required")),
    }
    # The evidence flags, each present only when true - the shape the manifest
    # already carries, and the shape the Evidence panel reads.
    if any(p.get("letter_list_only") for p in persons):
        row["letter_list_only"] = True
    if any(p.get("civic_mint") for p in persons):
        row["civic_mint"] = True
    if any(p.get("resident_subtype") == PROJECTED for p in persons):
        row[PROJECTED] = True
    linked = sum(1 for p in persons if p.get("later_census"))
    if linked:
        row["census_1840_linked"] = linked
    return {k: row[k] for k in ROW_KEYS if k in row}


def rebuild(index: dict, docs=None) -> dict:
    """Re-derive EVERY row and every derived count from the cards, in place.

    `docs` is a pass's in-memory {path: household} map - the whole layer as that
    pass will leave it, not the slice it minted. Omit it to read the committed
    cards off disk.
    """
    houses = household_docs(docs) if docs is not None else load_households()
    rows = sorted((row_for(path, doc) for path, doc in houses.items()),
                  key=lambda r: r["id"])
    index["households"] = rows

    grades = {g: 0 for g in GRADES}
    for row in rows:
        for grade, n in row["grades"].items():
            grades[grade] = grades.get(grade, 0) + n
    people = [p for doc in houses.values() for p in (doc.get("persons") or [])]
    derived = {
        "households": len(rows),
        "persons": sum(r["persons"] for r in rows),
        "by_grade": grades,
        "letter_list_only": sum(1 for p in people if p.get("letter_list_only")),
        "projected_residents": sum(1 for p in people
                                   if p.get("resident_subtype") == PROJECTED),
        "census_1840_linked": sum(1 for p in people if p.get("later_census")),
        "civic_mint": sum(1 for p in people if p.get("civic_mint")),
    }
    counts = dict(index.get("counts") or {})
    counts.update(derived)                       # in place for keys already there
    index["counts"] = counts
    return index


def dumps(obj) -> str:
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def differences(committed: dict, derived: dict, limit: int = 12) -> list[str]:
    """Human sentences for what drifted, ordered rows-then-counts."""
    out: list[str] = []
    was = {r.get("id"): r for r in committed.get("households") or []}
    now = {r.get("id"): r for r in derived.get("households") or []}
    for hid in sorted(set(was) | set(now)):
        a, b = was.get(hid), now.get(hid)
        if a == b:
            continue
        if a is None:
            out.append(f"household '{hid}' has a card and no manifest row")
        elif b is None:
            out.append(f"household '{hid}' has a manifest row and no card")
        else:
            for key in sorted(set(a) | set(b)):
                if a.get(key) != b.get(key):
                    out.append(f"household '{hid}' {key}: manifest {a.get(key)!r}, "
                               f"cards {b.get(key)!r}")
    ca, cb = committed.get("counts") or {}, derived.get("counts") or {}
    for key in DERIVED_COUNTS:
        if ca.get(key) != cb.get(key):
            out.append(f"counts.{key}: manifest {ca.get(key)!r}, cards {cb.get(key)!r}")
    if len(out) > limit:
        out = out[:limit] + [f"… and {len(out) - limit} more"]
    return out


FIX = "python3 tools/rebuild_resident_index.py --write"


def main(argv: list[str]) -> int:
    write = "--write" in argv
    committed = json.loads(INDEX.read_text(encoding="utf-8"))
    derived = rebuild(json.loads(json.dumps(committed)))
    if write:
        # The published mirror is NOT a copy - tools/publish.sh transforms the
        # residents layer and check_published_residents.mjs gates the transform -
        # so this writes the source and leaves the mirror to the publisher.
        INDEX.write_text(dumps(derived), encoding="utf-8")
        print(f"rebuilt {INDEX.relative_to(ROOT)} from "
              f"{derived['counts']['households']} household cards")
        return 0
    if dumps(committed) == dumps(derived):
        print(f"data/residents/index.json re-derives from its "
              f"{derived['counts']['households']} household cards")
        return 0
    print("data/residents/index.json is DERIVED from the household cards and no "
          "longer matches them.\n"
          f"  The cards are authoritative. Run: {FIX}\n"
          "  What drifted:", file=sys.stderr)
    for line in differences(committed, derived):
        print(f"    {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
