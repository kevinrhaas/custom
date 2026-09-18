#!/usr/bin/env python3
"""T-1144 acceptance 8: a research writer may not mint a `reconstructed` resident.

`grade` is the resident-EVIDENCE classification on a person: `attested` for a
confidently corroborated real named circa-1835 Chicagoan, `inferred` for one
reasonably believed to belong to that population. A third value exists in the
vocabulary — `reconstructed` — and it is reserved. It means a person the sources
do not name, drawn from the population model to fill a count the town needs. The
owner retired the previous reconstructed population on 2026-09-02 and ruled that
it comes back only under an explicit programme file; T-1167 is where that begins.

The danger this refuses is not a writer that sets the field on purpose. It is the
quiet one: a mint that falls through to a default, or a later pass that copies a
grade off a reconstructed neighbour, and the town gains people no source names
without anyone deciding that it should. `mint_documented_residents.py`,
`mint_letter_list_residents.py` and `mint_placed_residents.py` each hardcode
`"grade": "attested"` today and `synthesize_resident_research.py` retires any
reconstructed person it meets — so this is an invariant that happens to hold, and
nothing asserted it. T-1228's lesson on this same gate file is that an invariant
nobody asserts is one a refactor may delete unseen.

So: every writer of the resident layer calls `refuse()` on what it is about to
write, in EVERY mode including `--check`, and `--check` here proves every one of
them is still wired. The reconstruction generator T-1167 brings simply does not call it;
that is the whole boundary, and it is one line per writer to see.

What this does NOT touch: per-attribute `confidence`. A record may say
`{"value": null, "confidence": "reconstructed", "note": "Not attested."}` about
one field of a real attested person, and hundreds do. That is a statement about
one fact, not about whether the person existed, and refusing it would be wrong.

  python3 tools/refuse_reconstructed_grade.py --check
  python3 tools/refuse_reconstructed_grade.py --self-test
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reconstructed_person import is_reconstructed  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
PROGRAMME_TICKET = "T-1167"

RESERVED = "reconstructed"
# What a research writer may emit. The reserved third value is deliberately absent.
WRITABLE_GRADES = ("attested", "inferred")

# The writers of data/residents/, and the EXACT call each one must carry.
# Named here rather than discovered, so deleting a writer's hook is a failure and
# not a silently shorter list — and spelled as the call rather than the module,
# because importing a refusal and never calling it is the shape this is for.
WIRED_WRITERS = {
    "tools/synthesize_resident_research.py":
        'refuse(docs, "synthesize_resident_research.py")',
    "tools/mint_documented_residents.py":
        'refuse_texts(files, "mint_documented_residents.py")',
    "tools/mint_letter_list_residents.py":
        'refuse_texts(files, "mint_letter_list_residents.py")',
    "tools/mint_placed_residents.py":
        'refuse_texts(files, "mint_placed_residents.py")',
    # T-1170. A fifth writer, and the first one that is not a mint: it seats the family
    # members the sources NAME on a head this layer already carries. The counted ones are
    # the reconstruction programme's and are on the other side of this boundary.
    "tools/spend_stated_families.py":
        'refusal.refuse(changed, WRITER)',
}


class ReconstructedGradeRefused(Exception):
    """A writer tried to emit a resident grade it is not allowed to emit."""


def persons(doc):
    """The person records inside one household document."""
    if not isinstance(doc, dict):
        return []
    return [p for p in (doc.get("persons") or []) if isinstance(p, dict)]


def claimed_by_the_programme(person) -> bool:
    """A person a STAGE of the reconstruction programme wrote and can re-derive.

    T-1171 was the first stage to write one, and it writes them INSIDE cards the research
    mints own. A mint rebuilds its card whole, so `resident_mint_carry` carries those
    people through the rebuild — and a blanket refusal would then fire on a mint for
    carrying what it did not mint. The distinction this gate makes, and the one that
    matters, is whether a stage CLAIMS the person: `reconstruct_residents_1835.py --check`
    re-derives every claimed person from that stage's own seeds and refuses a single
    differing byte, so a mint that learned to stamp a stage key on an invention would be
    caught there, by a gate it could only pass by drawing the invention for real.

    What stays refused here is the leak this file was written for: a `reconstructed` grade
    arriving from a default or copied off a neighbour, which no stage claims and nothing
    can re-derive. `reconstructed_person.py` holds the test; this is its name here.
    """
    return is_reconstructed(person)


def offences(doc, label):
    """Every person in `doc` whose grade a research writer may not emit."""
    out = []
    for person in persons(doc):
        grade = person.get("grade")
        if grade in WRITABLE_GRADES:
            continue
        if grade == RESERVED and claimed_by_the_programme(person):
            continue
        pid = person.get("id") or person.get("name") or "(unnamed person)"
        if grade == RESERVED:
            out.append(f"{label}: {pid} is graded `{RESERVED}`")
        else:
            out.append(f"{label}: {pid} is graded `{grade}`, which is not a grade "
                       f"a research writer may emit")
    return out


def shown(label):
    """A label a reader can act on: repo-relative for a path, verbatim otherwise."""
    if isinstance(label, Path):
        try:
            return str(label.relative_to(ROOT))
        except ValueError:
            return label.name
    return str(label)


def refuse(docs, writer):
    """Refuse the write if any person in `docs` carries a grade this writer may not emit.

    `docs` maps a label — a path, an id, anything a reader can act on — to a
    household document. Call it on what you are ABOUT to write, in every mode,
    so that `--check` refuses on the same rule the write does.
    """
    bad = []
    for label, doc in docs.items():
        bad.extend(offences(doc, shown(label)))
    if not bad:
        return
    raise ReconstructedGradeRefused(
        f"{writer} would emit {len(bad)} resident(s) it may not:\n  "
        + "\n  ".join(bad[:10])
        + (f"\n  …and {len(bad) - 10} more" if len(bad) > 10 else "")
        + f"\n`{RESERVED}` is reserved for the reconstruction programme "
          f"({PROGRAMME_TICKET}); a research mint never emits it. "
          f"A writer may emit {' or '.join(WRITABLE_GRADES)}."
    )


def refuse_texts(files, writer):
    """The same refusal over the {path: json text} map the three mints build."""
    docs = {}
    for path, text in files.items():
        try:
            docs[path] = json.loads(text)
        except json.JSONDecodeError:
            continue
    refuse(docs, writer)


def check():
    problems = []

    committed = {p.name: json.loads(p.read_text(encoding="utf-8"))
                 for p in sorted(HOUSEHOLDS.glob("*.json"))}
    # THE LAYER MAY NOW HOLD RECONSTRUCTED PEOPLE, AND ONLY THE PROGRAMME'S.
    # This assertion read "none at all" while the programme had built no stage and
    # the count was zero. T-1171 built one, and a rule whose truth depended on an
    # empty set would have made the first legitimate reconstruction look like the
    # leak it exists to catch. What it refuses now is the leak itself: a person
    # graded `reconstructed` whom no stage of T-1167's programme claims. The
    # programme's own `--check` holds those it does claim to the record contract;
    # the writers' wiring below is unchanged and is still the boundary.
    try:
        refuse(committed, "the committed resident layer")
    except ReconstructedGradeRefused as exc:
        problems.append(str(exc))

    for rel, call in WIRED_WRITERS.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel} is gone, and this gate names it as a writer of "
                            f"the resident layer")
        elif call not in path.read_text(encoding="utf-8"):
            problems.append(f"{rel} no longer calls `{call}`: it can emit a "
                            f"`{RESERVED}` resident and nothing would refuse it")

    if problems:
        print("RECONSTRUCTED-GRADE REFUSAL FAIL")
        for p in problems:
            print(" -", p)
        return 1
    people = sum(len(persons(d)) for d in committed.values())
    claimed = sum(1 for d in committed.values() for p in persons(d)
                  if p.get("grade") == RESERVED)
    print(f"   OK: {people} resident(s) across {len(committed)} household(s); "
          f"{claimed} graded `{RESERVED}`, every one of them claimed by a stage of "
          f"{PROGRAMME_TICKET}'s programme; all {len(WIRED_WRITERS)} writers refuse it")
    return 0


def self_test():
    failures = []

    def raises(docs, why):
        try:
            refuse(docs, "a test writer")
        except ReconstructedGradeRefused as exc:
            return str(exc)
        failures.append(f"no refusal: {why}")
        return ""

    def passes(docs, why):
        try:
            refuse(docs, "a test writer")
        except ReconstructedGradeRefused as exc:
            failures.append(f"refused what it should allow ({why}): {exc}")

    # 1. The thing itself: one person graded `reconstructed`, and the message has
    #    to name the person and the programme, or a reader cannot act on it.
    message = raises({"hh_test.json": {"id": "hh_test", "persons": [
        {"id": "p_test", "name": "A Test", "grade": RESERVED}]}},
        "a person graded reconstructed")
    if message and "p_test" not in message:
        failures.append("the refusal does not name the offending person")
    if message and PROGRAMME_TICKET not in message:
        failures.append(f"the refusal does not say where reconstruction does belong "
                        f"({PROGRAMME_TICKET})")

    # 2. What the writers actually emit today is allowed.
    passes({"hh_ok.json": {"id": "hh_ok", "persons": [
        {"id": "p_a", "grade": "attested"}, {"id": "p_b", "grade": "inferred"}]}},
        "attested and inferred")

    # 3. THE DISTINCTION. A per-attribute confidence of `reconstructed` is a
    #    statement about one fact of a real person, not about the person, and
    #    hundreds of committed records carry it. Refusing it would be wrong.
    passes({"hh_attr.json": {"id": "hh_attr", "persons": [{
        "id": "p_c", "grade": "attested",
        "occupation": {"value": None, "confidence": RESERVED, "note": "Not attested."},
        "lives_at": {"value": None, "confidence": RESERVED, "note": "Not attested."}}]}},
        "a per-attribute confidence of reconstructed")

    # 3b. A reconstructed person a STAGE of the programme claims is carried, not minted:
    #     the mints rebuild their cards whole and `resident_mint_carry` carries those
    #     people through. Refusing that would fire on a mint for keeping what it did not
    #     write. The claim is what makes it safe — the programme's own --check re-derives
    #     every claimed person from its seeds — and a reconstructed person NO stage claims
    #     is still refused, which is the leak this file exists for.
    passes({"hh_stage.json": {"id": "hh_stage", "persons": [
        {"id": "rc_p", "grade": RESERVED,
         "reconstruction": {"stage": "modelled_families"}}]}},
        "a person a stage of the reconstruction programme claims")
    raises({"hh_loose.json": {"id": "hh_loose", "persons": [
        {"id": "p_loose", "grade": RESERVED, "reconstruction": {"programme": "x"}}]}},
        "a reconstructed person no stage claims")

    # 4. A grade outside the vocabulary is refused too — the fall-through case is
    #    how a default would arrive, and it would not spell itself `reconstructed`.
    raises({"hh_odd.json": {"id": "hh_odd", "persons": [
        {"id": "p_d", "grade": "guessed"}]}}, "a grade outside the vocabulary")
    raises({"hh_none.json": {"id": "hh_none", "persons": [
        {"id": "p_e", "name": "No Grade"}]}}, "a person with no grade at all")

    # 5. A household with no persons is not an offence: the mints write container
    #    records, and refusing them would refuse the whole tree.
    passes({"hh_empty.json": {"id": "hh_empty", "persons": []}}, "an empty household")

    # 6. The mints hand this a {path: text} map; it must refuse through the parse.
    try:
        refuse_texts({"hh_t.json": json.dumps(
            {"id": "hh_t", "persons": [{"id": "p_f", "grade": RESERVED}]})},
            "a test mint")
        failures.append("no refusal: reconstructed grade arriving as JSON text")
    except ReconstructedGradeRefused:
        pass

    # 7. The wiring assertion — the one that keeps this from becoming decoration.
    #    It is the CALL that is looked for, not the import, and the test of that is
    #    a source that imports the refusal and never uses it. This is what check()
    #    runs, on a string, so no writer has to be broken to prove it.
    imported_unused = ("from refuse_reconstructed_grade import refuse_texts\n"
                       "def build():\n    return {}\n")
    for rel, call in WIRED_WRITERS.items():
        if call in imported_unused:
            failures.append(f"the wiring test for {rel} passes a source that imports "
                            f"the refusal and never calls it")

    # 8. ...and that every named writer really does carry its call today.
    for rel, call in WIRED_WRITERS.items():
        path = ROOT / rel
        if not path.exists() or call not in path.read_text(encoding="utf-8"):
            failures.append(f"{rel} does not carry `{call}` today")

    if failures:
        print("RECONSTRUCTED-GRADE REFUSAL SELF-TEST FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print(f"ok: the refusal fires on a `{RESERVED}` grade, on an unknown grade and on "
          f"a missing one; it leaves per-attribute `{RESERVED}` confidence alone; and "
          f"it is wired into all {len(WIRED_WRITERS)} writers of the resident layer")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.check:
        return check()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
