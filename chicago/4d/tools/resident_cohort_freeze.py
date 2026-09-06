#!/usr/bin/env python3
"""What a FROZEN research cohort manifest is, on both the gate and the write (T-0764).

    tools/resident_cohort_freeze.py --self-test    the assertions, fired against breakage

    freeze.gate(path, derived, label)              what --gate asserts
    freeze.write(path, derived, message)           what a regeneration is allowed to change

THE GATE CONTRACT BELOW IS T-0745's, taken from `steward/t-0745-cohort-freeze-gate`
unchanged; that branch's ticket said "take it or leave it, but do not lose it". T-0764
is the other half of the same defect and it is the half that loses evidence: exempting
the snapshot from the GATE stops a manifest being called stale, but the documented
remedy for a stale manifest — regenerate without `--gate` — still OVERWRITES the
snapshot with today's tree. `write()` below is the half that was missing.

WHY THIS FILE EXISTS. Eight cohort manifests are written by
`tools/select_resident_research_*.py` and each one is described, in its own text, as
frozen: "the ids are frozen, so a resident minted later is not retro-claimed as
researched", and "a person who acquires a research row after this does NOT make the
manifest stale". Every one of them was nevertheless gated by RE-DERIVING the whole
document from today's tree and demanding byte equality. Those two statements cannot
both hold. A re-derivation asserts the tree has not moved since the freeze, and the
tree moving is precisely what the cohorts are for:

  * researching a cohort writes a `resident_research` row onto each of its members,
    which is what `researched_ids()` refuses at selection — so a completed pass makes
    its own gate fire. On 2026-09-05 cohorts 13, 14 and 15 were red on all 76 of 76
    of their own people;
  * a source landing on a card moves that person's `sources`, `grade` and
    `occupation` — so the pilot, pass 2 and pass 3 manifests read `stale` because
    three of their 225 people had gained a land-sales entry and a death notice.

Neither is a defect in the manifest. Both were reported as one, for two days, on
every branch cut from dev.

WHAT IS FROZEN, AND SO WHAT IS GATED. The manifest is a RESERVATION and an identity
lock: it says which people this pass owns, in a fixed order, and nothing about them
that a later reading may not change. So the gate asserts the frozen thing —

  1. the committed file's person ids, IN ORDER, are the ones the selector's frame
     still yields.  This is the collision lock three parallel runs work against;
  2. every id still names a real person in `data/residents/households/`, carrying a
     name, and not an unnamed placeholder ("the rest of the household, unnamed").
     THIS is the staleness the manifests' own text describes — a person who VANISHES,
     or turns into a count;
  3. every committed row carries exactly the fields the selector emits, so a snapshot
     cell cannot be silently dropped or invented;
  4. everything in the document OUTSIDE `people` and `population_frame` matches the
     derivation exactly.

— and it does not assert the SNAPSHOT: the per-person `starting_*`, `sources`,
`letter_list_returns` and `stratum` cells, and the `population_frame` counts, which
record the tree as it stood when the cohort was fixed. It reports how many of them
have moved since, because that number is worth seeing and is not a failure.

AND SO WHAT A REGENERATION MAY CHANGE. `write()` carries the committed snapshot
forward. A person already in the manifest keeps the `starting_*`, `sources`,
`letter_list_returns` and `stratum` cells the manifest was frozen with, and the
document keeps its committed `population_frame`; a person the frame yields for the
first time is frozen at today's values, because that is the moment that person's
cohort membership begins. Everything else — the identity cells the tree owns, and
every document field outside the snapshot — is rewritten from the derivation, which
is what a regeneration is for.

WHAT THIS CANNOT RECOVER. The snapshots on disk today are NOT the day each cohort was
fixed: every manifest has been regenerated between five and fifteen times since, most
recently by PR #863 on 2026-09-05, and each of those writes replaced the freeze with
the tree of its own afternoon. Nothing here reconstructs those values — a snapshot
lifted out of an old commit and re-committed today would be this project asserting a
provenance it cannot show, which is the one thing it does not do. What this file
guarantees is forward: from its first write, a cell is written once.

WHAT THIS DOES NOT WEAKEN. The novelty refusal — "zero overlap with the people who
already carry a research row" — is meaningful when a cohort is SELECTED and is
self-refuting afterwards, so it stays on the write path, unchanged and still fatal
there. A new manifest claiming somebody another pass has ruled on is refused before
it is ever committed.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSEHOLDS = ROOT / "data" / "residents" / "households"

# The document keys that record the tree as it stood at the freeze rather than the
# reservation itself. Everything else is compared exactly.
SNAPSHOT_DOC_KEYS = ("population_frame",)

# The per-person cells that record the tree at the freeze. `starting_*` is a prefix
# because the selectors each emit their own set of them (evidence, grade, presence,
# occupation); the rest are named. Everything not matched here — `person_id`,
# `household_id`, `name`, `selection_reason` — is the reservation or the tree's own
# identity, and a regeneration is allowed to rewrite it.
SNAPSHOT_ROW_KEYS = ("sources", "letter_list_returns", "stratum")


def is_snapshot_key(key: str) -> bool:
    return key.startswith("starting_") or key in SNAPSHOT_ROW_KEYS


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


def check(committed: dict, derived: dict, people: dict) -> tuple[list, int]:
    """The four assertions. Returns (failures, cells that moved since the freeze)."""
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
        moved += sum(1 for k in mirror if row[k] != mirror[k])
    return fails, moved


def preserve(committed: dict | None, derived: dict) -> tuple[dict, int]:
    """The document a regeneration may write. Returns (doc, cells held back).

    The derivation, with every snapshot cell the committed manifest already carries put
    back over it. A person the committed manifest does not hold is frozen at today's
    values; a document with no committed manifest beside it IS the freeze and passes
    through untouched.
    """
    if committed is None:
        return derived, 0
    doc = copy.deepcopy(derived)
    held = 0

    for key in SNAPSHOT_DOC_KEYS:
        if key in doc and key in committed:
            if doc[key] != committed[key]:
                held += 1
            doc[key] = copy.deepcopy(committed[key])

    frozen = {row.get("person_id"): row for row in committed.get("people", [])}
    for row in doc.get("people", []):
        was = frozen.get(row.get("person_id"))
        if was is None:
            continue
        for key in list(row):
            # A cell the committed row does not carry is a field the selector has
            # since started emitting; it freezes now, at today's value.
            if is_snapshot_key(key) and key in was:
                if row[key] != was[key]:
                    held += 1
                row[key] = copy.deepcopy(was[key])
    return doc, held


def write(path: Path, derived: dict, message: str) -> int:
    """Regenerate one manifest without rewriting its freeze."""
    committed = None
    if path.exists():
        committed = json.loads(path.read_text(encoding="utf-8"))
    doc, held = preserve(committed, derived)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    note = ""
    if held:
        note = ("; %d snapshot cell(s) held at the value the cohort was frozen with, "
                "which a regeneration may not rewrite" % held)
    print("%s%s" % (message, note))
    return 0


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
    derived, people = _fixture()
    cases, bad = [], 0

    def case(label, committed, live, expect_fail):
        nonlocal bad
        fails, _moved = check(committed, derived, live)
        ok = bool(fails) == expect_fail
        if not ok:
            bad += 1
        cases.append(("ok   " if ok else "FAIL ", label,
                      fails[0] if fails else "no failure"))

    case("the committed manifest IS the derivation", copy.deepcopy(derived), people, False)

    moved = copy.deepcopy(derived)
    moved["people"][0]["starting_grade"] = "attested"
    moved["population_frame"]["eligible_real_named_people"] = 999
    case("a snapshot cell moving is the research landing, not staleness", moved, people, False)

    reordered = copy.deepcopy(derived)
    reordered["people"].reverse()
    case("the ids in a different order fail", reordered, people, True)

    swapped = copy.deepcopy(derived)
    swapped["people"][0]["person_id"] = "c_three"
    case("a person the frame no longer yields fails", swapped, people, True)

    case("a person who has left the residents layer fails",
         copy.deepcopy(derived), {"a_one": people["a_one"]}, True)

    case("a person who has become an unnamed placeholder fails",
         copy.deepcopy(derived),
         {**people, "b_two": ({}, {"id": "b_two", "name": "The rest, unnamed"})}, True)

    dropped = copy.deepcopy(derived)
    del dropped["people"][1]["starting_grade"]
    case("a snapshot field dropped from a row fails", dropped, people, True)

    invented = copy.deepcopy(derived)
    invented["people"][1]["starting_trade"] = "cooper"
    case("a field invented on a row fails", invented, people, True)

    doc = copy.deepcopy(derived)
    doc["generated_by"] = "tools/somebody_elses_selector.py"
    case("a document field outside the snapshot must match exactly", doc, people, True)

    # ---- the write path: what a regeneration may and may not rewrite (T-0764)

    def wcase(label, ok, detail):
        nonlocal bad
        if not ok:
            bad += 1
        cases.append(("ok   " if ok else "FAIL ", label, detail))

    # The tree has moved under a committed cohort in every way it can: a grade rose, a
    # source landed, the household count changed, and one member moved house.
    committed = copy.deepcopy(derived)
    today = copy.deepcopy(derived)
    today["people"][0]["starting_grade"] = "attested"
    today["people"][0]["household_id"] = "hh_moved"
    today["people"][1]["stratum"] = "t"
    today["population_frame"]["eligible_real_named_people"] = 999
    kept, held = preserve(committed, today)

    wcase("a regeneration may not rewrite a starting_* cell",
          kept["people"][0]["starting_grade"] == "inferred",
          "starting_grade stayed %r" % kept["people"][0]["starting_grade"])
    wcase("a regeneration may not rewrite the population frame",
          kept["population_frame"]["eligible_real_named_people"] == 400,
          "frame stayed %r" % kept["population_frame"]["eligible_real_named_people"])
    wcase("a regeneration may not rewrite a member's stratum",
          kept["people"][1]["stratum"] == "s", "stratum stayed %r" % kept["people"][1]["stratum"])
    wcase("a regeneration DOES rewrite the tree's own identity cells",
          kept["people"][0]["household_id"] == "hh_moved",
          "household_id followed the tree to %r" % kept["people"][0]["household_id"])
    wcase("the held-back cells are counted and reported", held == 3, "held %d" % held)

    # A cohort with nothing committed beside it is being frozen right now.
    first, held_first = preserve(None, copy.deepcopy(today))
    wcase("the first write IS the freeze and passes through untouched",
          first == today and held_first == 0, "held %d" % held_first)

    # A person the committed manifest never held freezes at today's values.
    grew = copy.deepcopy(today)
    grew["people"].append({"person_id": "c_three", "name": "C Three", "stratum": "u",
                           "starting_grade": "attested"})
    kept2, _ = preserve(committed, grew)
    wcase("a member the freeze does not hold is frozen at today's values",
          kept2["people"][2]["starting_grade"] == "attested", "new member took today's grade")

    # And what is written stays gateable: the preserved document must pass check().
    fails, _ = check(kept, today, people)
    wcase("what a regeneration writes still passes the gate against today's derivation",
          not fails, fails[0] if fails else "no failure")

    for mark, label, detail in cases:
        print("  %s %s → %s" % (mark, label, detail[:110]))
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
