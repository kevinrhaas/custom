#!/usr/bin/env python3
"""One-shot: rename every legacy hh_doc_/hh_placed_/hh_ll_ household to a plain id.

    python3 tools/rename_household_ids.py             write (renames + patches index.json)
    python3 tools/rename_household_ids.py --check     the full map, zero writes
    python3 tools/rename_household_ids.py --self-test the mechanics, on fixtures

WHAT THIS IS FOR. T-0599 stopped the three mint tools (mint_documented_residents.py,
mint_placed_residents.py, mint_letter_list_residents.py) from minting any NEW
household under a legacy hh_doc_/hh_placed_/hh_ll_ prefix — a household minted from
then on gets the same plain `hh_<surname>_<given>` id the ~73 hand-authored
households already used, and records which pass minted it in a `source_pass` field
instead. That closed the race; it did not touch the 747 households already minted
under a legacy prefix before it landed. This tool is that second half: it renames
those 747 to the same plain shape, adds `source_pass` to each, and patches the one
manifest row each has in data/residents/index.json to match.

WHY THIS IS NOT "JUST RE-RUN THE MINT TOOLS". Two of the three mint tools' own
`--check` are already dirty against the committed tree — a LATER, separate
resident-research enrichment pass hand-patches household content (`resident_research`,
an upgraded `grade`) without going through the mint tool and without changing the id.
Running a mint tool in write mode would silently overwrite that enrichment on
hundreds of files. So this tool never calls a mint tool's write path: it touches
ONLY id-shaped fields — `id`, the head person's `persons[].id`, `head`, and the new
`source_pass` key — on the household file, plus the matching `id`/`file`/`head`
manifest row, and leaves every other byte on both files exactly as it was.

THE ID SOURCE, for a household that is already committed rather than freshly
minted, is the head person's own `persons[i]["name"]` field (located via
`doc["head"]`) — the same normalized display name the mint tools themselves used
at mint time, run through the identical `plain_fragment()` (surname first, matching
how the ~73 hand-authored households are already named) that a fresh mint of the
same person would produce today. This is what makes the rename reproducible rather
than invented: re-deriving the map fresh finds the SAME 747 target ids every time.

THE DISAMBIGUATION SUFFIX (`_2`, `_3`, ...) is a defensive backstop, not evidence
that collisions exist. `town_family_names()` in the mint tools already refuses a
candidate by bare surname before any id is generated, one household per surname per
pass — so two different real people can never reach id-generation with the same
slug in the first place. A repo-wide dry run at the time this tool was written found
zero collisions among the 747, in either direction. The suffix exists so a future
re-run of this tool (a straggler minted in the window before T-0599 merged, say)
cannot silently overwrite an unrelated household that happens to already hold the
base id.

WHAT THIS TOOL DOES NOT DO. It does not touch `hh_inf_*` households (a separate,
unrelated pipeline) or any household that is not legacy-prefixed. It does not
re-run `publish.sh`, and it does not touch the frozen, gated selector scripts
(`select_resident_research_*.py`), the resident-research findings ledgers
(`pass_NN_findings.json`), the `T-*/…_resident_research.csv` files, or
`smoke_renderer.mjs`'s three literal household ids — those reference the OLD ids
by hardcoded value and need their own pass, in their own ticket, edited at the
source rather than patched after the fact. Until that pass lands, running this
tool in write mode will make those references stale; `--check` prints a reminder
of that scope boundary so it is never mistaken for "the migration is done".

IDEMPOTENT. A run that finds no household left with a legacy prefix REFUSES rather
than silently doing nothing (`tools/rename_confidence_vocab.py`'s precedent for
this hazard class) — a second run is either a bug (something reintroduced a legacy
id) or a mistake (the tool was invoked after the migration already landed), and
either way the right answer is to say so loudly, not exit 0 having touched nothing.
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
INDEX = ROOT / "data" / "residents" / "index.json"

sys.path.insert(0, str(ROOT / "tools"))
from mint_documented_residents import MINTED_PASSES, dumps, load, plain_fragment  # noqa: E402

INDEX_ROW_KEYS = ("id", "file", "head")


def legacy_pass(hid: str) -> str | None:
    """Which pass minted this id under the old scheme, or None if it is plain
    (or hh_inf_, which is a different pipeline and never touched here)."""
    for pass_name, prefix in MINTED_PASSES:
        if hid.startswith(prefix):
            return pass_name
    return None


def head_person(doc: dict) -> dict | None:
    hid = doc.get("head")
    for p in doc.get("persons") or []:
        if p.get("id") == hid:
            return p
    return None


def read_households(root: pathlib.Path = HOUSEHOLDS) -> dict[pathlib.Path, dict]:
    return {p: load(p) for p in sorted(root.glob("*.json"))}


def build_map(docs: dict[pathlib.Path, dict]) -> tuple[dict[str, str], list[str]]:
    """{old_id: new_id} for every legacy-prefixed household in docs, plus any
    problems that should refuse the run. Pure — no I/O, no mutation."""
    problems: list[str] = []
    legacy: dict[str, tuple[dict, str]] = {}
    staying: set[str] = set()
    for path, doc in docs.items():
        hid = doc.get("id")
        if hid != path.stem:
            problems.append(f"{path.name}: id '{hid}' does not match its filename stem")
            continue
        pass_name = legacy_pass(hid)
        if pass_name:
            legacy[hid] = (doc, pass_name)
        else:
            staying.add(hid)

    if not legacy:
        problems.append("no household carries a legacy hh_doc_/hh_placed_/hh_ll_ prefix — "
                         "already migrated, or there was never anything to migrate")
        return {}, problems

    taken = set(staying)
    id_map: dict[str, str] = {}
    for old_id in sorted(legacy):
        doc, pass_name = legacy[old_id]
        persons = doc.get("persons") or []
        if len(persons) != 1:
            problems.append(f"{old_id}: carries {len(persons)} person(s), not the 1 every "
                             f"legacy-prefixed household is expected to hold — refusing rather "
                             f"than guessing which one the id should follow")
            continue
        head = head_person(doc)
        if head is None or not (head.get("name") or "").strip():
            problems.append(f"{old_id}: its head person cannot be found or has no name")
            continue
        base_id = "hh_" + plain_fragment(head["name"])
        candidate, n = base_id, 2
        while candidate in taken:
            candidate = f"{base_id}_{n}"
            n += 1
        id_map[old_id] = candidate
        taken.add(candidate)

    if problems:
        return {}, problems
    if len(set(id_map.values())) != len(id_map):
        problems.append("BUG: the disambiguation loop produced a duplicate target id — "
                         "refusing rather than trusting a broken invariant")
        return {}, problems
    return id_map, problems


def rewrite_household(doc: dict, new_id: str, pass_name: str) -> dict:
    """A new dict: id, the head person's persons[].id, and head rewritten to
    new_id's shape, source_pass inserted right after head (matching where the
    mint tools themselves place it on a fresh mint) — every other key, and every
    other key's VALUE, carried over untouched and in its original order."""
    old_pid = doc["head"]
    new_pid = new_id.removeprefix("hh_")
    out: dict = {}
    for key, value in doc.items():
        if key == "id":
            out["id"] = new_id
        elif key == "head":
            out["head"] = new_pid
            out["source_pass"] = pass_name
        elif key == "persons":
            out["persons"] = [
                dict(p, id=new_pid) if p.get("id") == old_pid else p
                for p in value
            ]
        else:
            out[key] = value
    return out


def rewrite_index(index: dict, id_map: dict[str, str]) -> dict:
    """The manifest with id/file/head patched on the affected rows, re-sorted by
    id — every other row, and every other key on the affected rows, untouched."""
    out = copy.deepcopy(index)
    rows = out["households"]
    for row in rows:
        new_id = id_map.get(row.get("id"))
        if new_id is None:
            continue
        row["id"] = new_id
        row["file"] = f"households/{new_id}.json"
        row["head"] = new_id.removeprefix("hh_")
    rows.sort(key=lambda r: r["id"])
    return out


def report(id_map: dict[str, str]) -> None:
    for old_id in sorted(id_map):
        print(f"   {old_id}  ->  {id_map[old_id]}")
    print(f"\n   {len(id_map)} household(s) would be renamed; data/residents/index.json's "
          f"matching rows would be patched (id/file/head) and re-sorted.")
    print("   NOT touched by this tool: the frozen selector scripts, the resident-research "
          "findings ledgers, the *_resident_research.csv files, smoke_renderer.mjs's literal "
          "ids, and the published site/ mirror — each needs its own pass before the old ids "
          "are safe to remove from the tree.")


def apply(id_map: dict[str, str], docs: dict[pathlib.Path, dict]) -> None:
    by_id = {doc["id"]: (path, doc) for path, doc in docs.items()}
    index = load(INDEX)
    new_index = rewrite_index(index, id_map)
    INDEX.write_text(dumps(new_index), encoding="utf-8")
    for old_id, new_id in id_map.items():
        path, doc = by_id[old_id]
        pass_name = legacy_pass(old_id)
        new_doc = rewrite_household(doc, new_id, pass_name)
        path.write_text(dumps(new_doc), encoding="utf-8")
        path.rename(path.with_name(f"{new_id}.json"))
    print(f"renamed {len(id_map)} household(s); patched data/residents/index.json")


def self_test() -> int:
    """The mechanics, proved on fixtures — never against the committed tree."""
    failed = 0

    def want(label, got, expect):
        nonlocal failed
        if got == expect:
            print(f"   ok   {label}")
        else:
            failed += 1
            print(f"   FAIL {label}: got {got!r}, expected {expect!r}")

    # --- build_map: the plain id, and the surname-first shape -------------------
    doc_a = {
        "id": "hh_doc_a_garrett", "head": "doc_a_garrett", "division": "unplaced",
        "persons": [{"id": "doc_a_garrett", "name": "A. Garrett", "relationship": "head"}],
    }
    doc_b = {
        "id": "hh_ll_b_s_morris", "head": "ll_b_s_morris", "division": "unplaced",
        "persons": [{"id": "ll_b_s_morris", "name": "B. S. Morris", "relationship": "head"}],
    }
    staying = {"id": "hh_smith_john", "head": "smith_john", "division": "south", "persons": [
        {"id": "smith_john", "name": "John Smith", "relationship": "head"},
    ]}
    docs = {
        pathlib.Path("hh_doc_a_garrett.json"): doc_a,
        pathlib.Path("hh_ll_b_s_morris.json"): doc_b,
        pathlib.Path("hh_smith_john.json"): staying,
    }
    id_map, problems = build_map(docs)
    want("no problems on a clean fixture", problems, [])
    want("hh_doc_a_garrett -> hh_garrett_a", id_map.get("hh_doc_a_garrett"), "hh_garrett_a")
    want("hh_ll_b_s_morris -> hh_morris_b_s (surname first)",
         id_map.get("hh_ll_b_s_morris"), "hh_morris_b_s")
    want("the plain household is left alone", "hh_smith_john" in id_map, False)

    # --- build_map: disambiguation against a name already taken -----------------
    doc_c = {
        "id": "hh_placed_john_smith", "head": "placed_john_smith", "division": "unplaced",
        "persons": [{"id": "placed_john_smith", "name": "John Smith", "relationship": "head"}],
    }
    collide = {**docs, pathlib.Path("hh_placed_john_smith.json"): doc_c}
    id_map2, problems2 = build_map(collide)
    want("a name already held by a staying household gets a suffix",
         id_map2.get("hh_placed_john_smith"), "hh_smith_john_2")
    want("collision fixture still reports no problems", problems2, [])

    # --- build_map: refusals ------------------------------------------------------
    two_person = {
        "id": "hh_ll_two_person", "head": "ll_two_person", "division": "unplaced",
        "persons": [
            {"id": "ll_two_person", "name": "A B", "relationship": "head"},
            {"id": "ll_two_person_2", "name": "C D", "relationship": "spouse"},
        ],
    }
    _, problems3 = build_map({pathlib.Path("hh_ll_two_person.json"): two_person})
    want("a legacy household with a second member is refused",
         any("two_person" in p and "1 person" not in p for p in problems3)
         or any("carries 2 person" in p for p in problems3), True)

    _, problems4 = build_map({pathlib.Path("hh_smith_john.json"): staying})
    want("nothing legacy-prefixed refuses rather than silently doing nothing",
         any("already migrated" in p for p in problems4), True)

    mismatched = {
        "id": "hh_doc_wrong_name", "head": "doc_wrong_name", "division": "unplaced",
        "persons": [{"id": "doc_wrong_name", "name": "X", "relationship": "head"}],
    }
    _, problems5 = build_map({pathlib.Path("hh_doc_other_name.json"): mismatched})
    want("an id that disagrees with its own filename is refused",
         any("does not match its filename stem" in p for p in problems5), True)

    # --- rewrite_household: field order, id-shaped edits, everything else kept --
    original = {
        "id": "hh_doc_a_garrett", "name": "The Garrett household", "division": "unplaced",
        "head": "doc_a_garrett", "arrival": {"value": "1834"},
        "persons": [
            {"id": "doc_a_garrett", "name": "A. Garrett", "relationship": "head",
             "occupation": {"value": "auctioneer"}},
        ],
    }
    rewritten = rewrite_household(original, "hh_garrett_a", "documented")
    want("id rewritten", rewritten["id"], "hh_garrett_a")
    want("head rewritten to the plain person id", rewritten["head"], "garrett_a")
    want("source_pass recorded", rewritten.get("source_pass"), "documented")
    want("source_pass placed immediately after head",
         list(rewritten.keys()).index("source_pass"),
         list(rewritten.keys()).index("head") + 1)
    want("the head person's own id follows the household id",
         rewritten["persons"][0]["id"], "garrett_a")
    want("an untouched field is untouched",
         rewritten["arrival"], {"value": "1834"})
    want("an untouched person field is untouched",
         rewritten["persons"][0]["occupation"], {"value": "auctioneer"})
    want("the household name is not rewritten (a later pass' job, not id-shaped)",
         rewritten["name"], "The Garrett household")

    # --- rewrite_index: targeted 3-field edit, re-sorted, other rows/keys kept ---
    index = {
        "vocabulary": {"grades": ["attested"]},
        "households": [
            {"id": "hh_doc_a_garrett", "file": "households/hh_doc_a_garrett.json",
             "head": "doc_a_garrett", "division": "unplaced", "persons": 1,
             "lives_at": None},
            {"id": "hh_smith_john", "file": "households/hh_smith_john.json",
             "head": "smith_john", "division": "south", "persons": 1},
        ],
    }
    new_index = rewrite_index(index, {"hh_doc_a_garrett": "hh_garrett_a"})
    ids = [r["id"] for r in new_index["households"]]
    want("the manifest re-sorts by the new id", ids, sorted(ids))
    edited = next(r for r in new_index["households"] if r["id"] == "hh_garrett_a")
    want("the row's file field follows the new id",
         edited["file"], "households/hh_garrett_a.json")
    want("the row's head field follows the new person id", edited["head"], "garrett_a")
    want("an untouched row key on the edited row is untouched", edited["division"], "unplaced")
    untouched = next(r for r in new_index["households"] if r["id"] == "hh_smith_john")
    want("the untouched row is untouched", untouched["division"], "south")
    want("the vocabulary block is untouched", new_index["vocabulary"], {"grades": ["attested"]})
    want("the original index is not mutated in place",
         index["households"][0]["id"], "hh_doc_a_garrett")

    # --- apply(): the actual write + rename, on a throwaway directory ----------
    with tempfile.TemporaryDirectory() as tmp:
        troot = pathlib.Path(tmp)
        (troot / "hh_doc_a_garrett.json").write_text(dumps(original), encoding="utf-8")
        tdocs = read_households(troot)
        tid_map, tproblems = build_map(tdocs)
        want("apply() fixture map has no problems", tproblems, [])
        by_id = {doc["id"]: (path, doc) for path, doc in tdocs.items()}
        for old_id, new_id in tid_map.items():
            path, doc = by_id[old_id]
            new_doc = rewrite_household(doc, new_id, legacy_pass(old_id))
            path.write_text(dumps(new_doc), encoding="utf-8")
            path.rename(path.with_name(f"{new_id}.json"))
        want("the old filename is gone", (troot / "hh_doc_a_garrett.json").exists(), False)
        want("the new filename exists", (troot / "hh_garrett_a.json").exists(), True)
        on_disk = load(troot / "hh_garrett_a.json")
        want("the id on disk matches the new filename", on_disk["id"], "hh_garrett_a")

    if failed:
        print(f"   {failed} assertion(s) failed")
        return 1
    print("   OK: all mechanics fixtures pass")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="print the full map, write nothing")
    ap.add_argument("--self-test", action="store_true", help="the mechanics, on fixtures")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    docs = read_households()
    id_map, problems = build_map(docs)

    if problems:
        for p in problems:
            print(f"   REFUSED: {p}")
        return 2

    if args.check:
        report(id_map)
        return 0

    apply(id_map, docs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
