#!/usr/bin/env python3
"""What a FROZEN research cohort manifest is, on the write path and on the gate (T-0764).

    tools/resident_cohort_freeze.py --self-test    the contract, fired against breakage

WHY THIS FILE EXISTS. Eight cohort manifests are written by
`tools/select_resident_research_*.py`, and every one of them describes itself as
frozen: "the ids are frozen, so a resident minted later is not retro-claimed as
researched", and "a person who acquires a research row after this does NOT make the
manifest stale". Each row carries `starting_grade`, `starting_evidence`,
`starting_presence`, `starting_occupation`, `sources`, `letter_list_returns` and
`stratum` — a SNAPSHOT of the tree at the moment the cohort was fixed, which is what
makes a finished pass legible: this person came into the cohort at `inferred`, on one
source, and left it at `attested` on three.

Both halves of the machinery contradicted that.

  * THE GATE re-derived the whole document from today's tree and demanded equality, so
    the moment a source landed on any member the manifest read `stale`.
  * THE WRITE, which is the documented remedy for that `stale`, rebuilt every row from
    today's tree — overwriting the snapshot with the very values whose predecessors it
    existed to record. Measured over this repository's own history on 2026-09-06:
    46 of the 82 commits that touched the eight gated manifests rewrote the freeze,
    and 384 snapshot cells were overwritten that way. Nobody read a diff; the numbers
    simply became today's.

So the freeze was recording the day of the last regeneration rather than the day the
cohort was fixed, and the loss was silent in both directions.

WHAT IS FROZEN, AND SO WHAT IS GATED. The manifest is a RESERVATION and an identity
lock: it says which people this pass owns, in a fixed order, and nothing about them
that a later reading may not change. The gate asserts the frozen thing —

  1. the committed file's person ids, IN ORDER, are the ones the selector's frame
     still yields. This is the collision lock parallel runs work against;
  2. every id still names a real person in `data/residents/households/`, carrying a
     name, and not an unnamed placeholder ("the rest of the household, unnamed").
     THIS is the staleness the manifests' own text describes — a person who VANISHES,
     or turns into a count;
  3. every committed row carries exactly the fields the selector emits, so a snapshot
     cell cannot be silently dropped or invented;
  4. everything in the document OUTSIDE `people` and the snapshot document keys
     matches the derivation exactly, and `population_frame.sample_size` still counts
     the people the manifest holds.

— and it does not assert the SNAPSHOT. It REPORTS how many snapshot cells have moved
since the freeze, because that number is the research landing and is worth seeing.

WHAT THIS DOES NOT WEAKEN. The selection-time refusals — the novelty rule ("zero
overlap with the people who already carry a research row"), the strata quotas, the
stratum-membership assertions — are meaningful when a cohort is SELECTED and stay
exactly where they are, inside each selector's `derive`. A new manifest claiming
somebody another pass has ruled on is still refused before it is ever committed.

THE FIRST WRITE IS THE FREEZE. `write()` carries the committed snapshot cells forward
onto the regenerated document for every id the manifest already holds; only an id the
manifest has never held takes today's values, and that is a mint. Identity cells —
`name`, `household_id`, `selection_reason` — are NOT snapshot and are refreshed, so a
corrected name still reaches the manifest.

The contract is bilateral with `docs/RESEARCH/` and with `tools/check.sh`, which runs
`--self-test` beside the eight `--gate` steps.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSEHOLDS = ROOT / "data" / "residents" / "households"

# The per-row cells that record the tree as it stood at the freeze. Everything else on
# a row is identity or provenance and is refreshed by a regeneration.
SNAPSHOT_ROW_KEYS = (
    "starting_grade",
    "starting_evidence",
    "starting_presence",
    "starting_occupation",
    "sources",
    "letter_list_returns",
    "stratum",
)

# The document keys that record the frame as it stood at the freeze rather than the
# reservation itself. Everything else is compared exactly.
SNAPSHOT_DOC_KEYS = ("population_frame",)


def live_people() -> dict:
    """Every person in the residents layer, by id, as (household, person)."""
    out = {}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        hh = json.loads(path.read_text(encoding="utf-8"))
        for person in hh.get("persons", []):
            if person.get("id"):
                out[person["id"]] = (hh, person)
    return out


def is_placeholder(person: dict) -> bool:
    name = person.get("name") or ""
    return not name.strip() or "unnamed" in name.lower()


def _ids(doc: dict) -> list:
    return [row.get("person_id") for row in doc.get("people", [])]


def preserve(committed: dict, derived: dict) -> dict:
    """The regenerated document, with the committed freeze carried forward.

    A snapshot cell is written ONCE — on the write that first put its person in the
    manifest — and every later regeneration reads it back off the committed file. An
    id the manifest has never held is a mint and takes today's values.
    """
    out = json.loads(json.dumps(derived))
    for key in SNAPSHOT_DOC_KEYS:
        if key in committed and key in out:
            out[key] = json.loads(json.dumps(committed[key]))
    frozen = {row.get("person_id"): row for row in committed.get("people", [])}
    for row in out.get("people", []):
        old = frozen.get(row.get("person_id"))
        if old is None:
            continue
        for key in SNAPSHOT_ROW_KEYS:
            if key in row and key in old:
                row[key] = json.loads(json.dumps(old[key]))
    # sample_size counts the people the manifest holds; it is arithmetic on the
    # reservation, not a reading of the tree, so it does not freeze.
    frame = out.get("population_frame")
    if isinstance(frame, dict) and "sample_size" in frame:
        frame["sample_size"] = len(out.get("people", []))
    return out


def check(committed: dict, derived: dict, people: dict) -> tuple[list, int]:
    """The four assertions. Returns (failures, snapshot cells moved since the freeze)."""
    fails = []

    # 4 — everything outside the snapshot is compared exactly.
    for key in derived:
        if key in SNAPSHOT_DOC_KEYS or key == "people":
            continue
        if committed.get(key) != derived[key]:
            fails.append("%s differs from the derivation" % key)
    for key in committed:
        if key not in derived:
            fails.append("%s is in the committed manifest and not in the derivation" % key)
    frame = committed.get("population_frame")
    if isinstance(frame, dict) and "sample_size" in frame:
        if frame["sample_size"] != len(committed.get("people", [])):
            fails.append("population_frame.sample_size is %s and the manifest holds %d people"
                         % (frame["sample_size"], len(committed.get("people", []))))

    # 1 — the ids, in order.
    have, want = _ids(committed), _ids(derived)
    if have != want:
        if set(have) == set(want):
            fails.append("the committed manifest holds the frame's people in a different order")
        else:
            gone = [p for p in have if p not in set(want)]
            new = [p for p in want if p not in set(have)]
            if gone:
                fails.append("the committed manifest claims people the frame no longer yields: %s"
                             % sorted(gone))
            if new:
                fails.append("the frame yields people the committed manifest does not claim: %s"
                             % sorted(new))

    moved = 0
    for row in committed.get("people", []):
        pid = row.get("person_id")
        # 2 — the person is still a real, named person in the tree.
        if pid not in people:
            fails.append("%s is claimed by the manifest and is in no household" % pid)
            continue
        if is_placeholder(people[pid][1]):
            fails.append("%s has become an unnamed placeholder, which no cohort may claim" % pid)
        # 3 — the row carries exactly the fields the selector emits.
        mirror = next((r for r in derived.get("people", []) if r.get("person_id") == pid), None)
        if mirror is None:
            continue
        if set(row) != set(mirror):
            fails.append("%s's row carries %s, and the selector emits %s"
                         % (pid, sorted(row), sorted(mirror)))
            continue
        moved += sum(1 for k in SNAPSHOT_ROW_KEYS if k in mirror and row[k] != mirror[k])
    return fails, moved


def gate(path: Path, derived: dict, label: str) -> int:
    """Run the gate for one committed manifest. Raises SystemExit on failure."""
    if not path.exists():
        raise SystemExit("%s does not exist; write it without --gate" % path.relative_to(ROOT))
    committed = json.loads(path.read_text(encoding="utf-8"))
    fails, moved = check(committed, derived, live_people())
    if fails:
        raise SystemExit("%s is not the frame's frozen cohort:\n  - %s"
                         % (path.relative_to(ROOT), "\n  - ".join(fails)))
    note = ""
    if moved:
        note = ("; %d snapshot cell(s) have moved since the freeze, which is the research "
                "landing and not staleness" % moved)
    print("%s: %d people, the frozen reservation is intact%s"
          % (label, len(committed.get("people", [])), note))
    return 0


def write(path: Path, derived: dict, label: str) -> int:
    """Write the manifest, carrying any existing freeze forward. See `preserve`."""
    minted = len(derived.get("people", []))
    if path.exists():
        committed = json.loads(path.read_text(encoding="utf-8"))
        held = {row.get("person_id") for row in committed.get("people", [])}
        minted = sum(1 for row in derived.get("people", []) if row.get("person_id") not in held)
        derived = preserve(committed, derived)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(derived, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("%s: wrote %d people, %d of them newly frozen (the rest keep the snapshot they "
          "were fixed with)" % (label, len(derived.get("people", [])), minted))
    return 0


# ---------------------------------------------------------------- the self-test

def _fixture():
    derived = {
        "_doc": "a cohort",
        "generated_by": "tools/select_resident_research_test.py",
        "population_frame": {"eligible_real_named_people": 400, "sample_size": 2},
        "people": [
            {"person_id": "a_one", "name": "A One", "stratum": "s", "starting_grade": "inferred"},
            {"person_id": "b_two", "name": "B Two", "stratum": "s", "starting_grade": "inferred"},
        ],
    }
    people = {"a_one": ({}, {"id": "a_one", "name": "A One"}),
              "b_two": ({}, {"id": "b_two", "name": "B Two"})}
    return derived, people


def self_test() -> int:
    import copy
    derived, people = _fixture()
    cases, bad = [], 0

    def case(label, ok, detail):
        nonlocal bad
        if not ok:
            bad += 1
        cases.append(("ok   " if ok else "FAIL ", label, detail))

    def gate_case(label, committed, live, expect_fail):
        fails, _moved = check(committed, derived, live)
        case(label, bool(fails) == expect_fail, fails[0] if fails else "no failure")

    gate_case("the committed manifest IS the derivation", copy.deepcopy(derived), people, False)

    moved = copy.deepcopy(derived)
    moved["people"][0]["starting_grade"] = "attested"
    moved["population_frame"]["eligible_real_named_people"] = 999
    gate_case("a snapshot cell moving is the research landing, not staleness", moved, people, False)

    reordered = copy.deepcopy(derived)
    reordered["people"].reverse()
    gate_case("the ids in a different order fail", reordered, people, True)

    swapped = copy.deepcopy(derived)
    swapped["people"][0]["person_id"] = "c_three"
    gate_case("a person the frame no longer yields fails", swapped, people, True)

    gate_case("a person who has left the residents layer fails",
              copy.deepcopy(derived), {"a_one": people["a_one"]}, True)

    gate_case("a person who has become an unnamed placeholder fails",
              copy.deepcopy(derived),
              {**people, "b_two": ({}, {"id": "b_two", "name": "The rest, unnamed"})}, True)

    dropped = copy.deepcopy(derived)
    del dropped["people"][1]["starting_grade"]
    gate_case("a snapshot field dropped from a row fails", dropped, people, True)

    invented = copy.deepcopy(derived)
    invented["people"][1]["starting_trade"] = "cooper"
    gate_case("a field invented on a row fails", invented, people, True)

    doc = copy.deepcopy(derived)
    doc["generated_by"] = "tools/somebody_elses_selector.py"
    gate_case("a document field outside the snapshot must match exactly", doc, people, True)

    miscounted = copy.deepcopy(derived)
    miscounted["population_frame"]["sample_size"] = 9
    gate_case("a sample_size that does not count the manifest's people fails",
              miscounted, people, True)

    # --- the write path: the freeze is written once.
    frozen = copy.deepcopy(derived)
    today = copy.deepcopy(derived)
    today["people"][0]["starting_grade"] = "attested"
    today["people"][0]["name"] = "A. One, corrected"
    today["population_frame"]["eligible_real_named_people"] = 999
    kept = preserve(frozen, today)
    case("a regeneration keeps the grade the person was frozen at",
         kept["people"][0]["starting_grade"] == "inferred",
         "starting_grade → %r" % kept["people"][0]["starting_grade"])
    case("a regeneration still refreshes a corrected name",
         kept["people"][0]["name"] == "A. One, corrected",
         "name → %r" % kept["people"][0]["name"])
    case("a regeneration keeps the population frame the cohort was fixed against",
         kept["population_frame"]["eligible_real_named_people"] == 400,
         "eligible_real_named_people → %r"
         % kept["population_frame"]["eligible_real_named_people"])

    minted = copy.deepcopy(derived)
    minted["people"].append({"person_id": "c_three", "name": "C Three", "stratum": "s",
                             "starting_grade": "attested"})
    minted["population_frame"]["sample_size"] = 3
    first = preserve(frozen, minted)
    case("a person the manifest has never held is frozen at today's values",
         first["people"][2]["starting_grade"] == "attested",
         "starting_grade → %r" % first["people"][2]["starting_grade"])
    case("sample_size counts the people the manifest holds, frozen frame or not",
         first["population_frame"]["sample_size"] == 3,
         "sample_size → %r" % first["population_frame"]["sample_size"])
    case("preserving twice is the same document (the freeze is idempotent)",
         preserve(frozen, kept) == kept, "second pass differs" )

    for mark, label, detail in cases:
        print("  %s %s → %s" % (mark, label, str(detail)[:110]))
    print("cohort freeze self-test: %d case(s), %d failed" % (len(cases), bad))
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    ap.error("nothing to do: --self-test is this file's only entry point")


if __name__ == "__main__":
    raise SystemExit(main())
