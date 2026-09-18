#!/usr/bin/env python3
"""T-1167: the ONE writer of a `reconstructed` resident, and its programme's gate.

`grade: reconstructed` means a person the sources do not name, drawn from the
population model to fill a count the town demonstrably needs. The owner retired the
previous reconstructed population on 2026-09-02 because nothing said, in one place,
what had been invented or what would replace it, and ruled that it comes back only
under an explicit programme file. That file is
`data/reconstruction/1835_resident_reconstruction_programme.json`; this tool is the
only thing allowed to act on it.

THE BOUNDARY, IN ONE LINE. Every research writer of `data/residents/` calls
`tools/refuse_reconstructed_grade.refuse()` and may emit only `attested` or
`inferred`. This tool does not call it. That asymmetry IS the rule, it is asserted
from both sides — `refuse_reconstructed_grade.py --check` proves the four writers
still carry their call, and `--self-test` below proves this one is held to the
record contract instead — and neither half is a comment.

A STAGE IS A TICKET. Bands 3A-3C each own one stage of one deterministic build, so
the whole reconstructed layer re-derives from the programme rather than accreting.
`--stage <key> --build` runs one; `--check` re-derives every IMPLEMENTED stage and
holds the committed layer to the record contract; `--self-test` runs the mutation
cases. No stage is implemented by T-1167 itself: this ticket writes no person, and
`--build` says so rather than inventing a default.

  python3 tools/reconstruct_residents_1835.py --list
  python3 tools/reconstruct_residents_1835.py --stage attribute_fill_sex_age --build
  python3 tools/reconstruct_residents_1835.py --check
  python3 tools/reconstruct_residents_1835.py --self-test
"""

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_attribute_tiers import BASIS_KINDS, REPLACEABLE_KINDS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROGRAMME = ROOT / "data" / "reconstruction" / "1835_resident_reconstruction_programme.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
RETIRED = ROOT / "data" / "reconstruction" / "1835_inferred_household_programme.json"
NAME_POOLS = ROOT / "data" / "reconstruction" / "1835_invented_name_pools.json"

RECONSTRUCTED = "reconstructed"
# The stage that alone may write a Native or Metis reconstruction (owner, 2026-09-17).
UNDERDOCUMENTED_STAGE = "underdocumented"
# Communities whose reconstruction is confined to that stage and carries the review.
REVIEWED_COMMUNITIES = ("native", "potawatomi", "metis", "métis", "indigenous")
# The id a reconstructed person's own record must wear, so a grep finds every invention.
INVENTED_PERSON_PREFIX = "rc_"
READMISSION_PASS = "reconstructed_readmission"


# --------------------------------------------------------------------------
# the programme
# --------------------------------------------------------------------------

def load_programme() -> dict:
    return json.loads(PROGRAMME.read_text(encoding="utf-8"))


def stages(prog: dict) -> dict:
    return {s["key"]: s for s in prog.get("stages", [])}


def seed_for(household_id: str, bucket: str) -> str:
    """The seed a reader can retype. See the programme's `seed_rule`."""
    return f"{household_id}:{bucket}"


def draw(seed: str) -> int:
    """The integer a seed draws. Deterministic across runs, machines and Pythons."""
    return int.from_bytes(hashlib.blake2s(seed.encode("utf-8"), digest_size=8).digest(), "big")


# --------------------------------------------------------------------------
# the record contract — what a reconstructed person owes
# --------------------------------------------------------------------------

def check_reconstructed_person(where: str, person: dict, stage_keys, error) -> None:
    """Refuse a reconstructed person that cannot show its working.

    `validate.py` holds the same contract over the committed layer; this is the
    writer's own copy so a stage is refused BEFORE it writes rather than after.
    """
    basis = person.get("basis")
    if not isinstance(basis, dict):
        error(where, "a reconstructed person requires a `basis` naming the model row or the "
                     "rule it was drawn from")
    else:
        if basis.get("kind") not in BASIS_KINDS:
            error(where, f"basis.kind {basis.get('kind')!r} is not one of {sorted(BASIS_KINDS)}")
        if not str(basis.get("id") or "").strip():
            error(where, "basis.id must name the model row or the rule")
        if not str(basis.get("note") or "").strip():
            error(where, "basis.note must state why this person follows from that basis")

    kind = (basis or {}).get("kind") if isinstance(basis, dict) else None
    seed = person.get("seed")
    if kind == "model" and not str(seed or "").strip():
        error(where, "a person DRAWN from a model requires the `seed` that redraws them - a "
                     "draw nobody can reproduce is not a reconstruction")
    if kind == "rule" and seed is not None:
        error(where, "a person argued from a rule carries no `seed`; nothing was drawn")

    rep = person.get("replaceable_by")
    if not isinstance(rep, dict):
        error(where, "a reconstructed person requires `replaceable_by` saying what evidence "
                     "would retire them")
    else:
        if rep.get("kind") not in REPLACEABLE_KINDS:
            error(where, f"replaceable_by.kind {rep.get('kind')!r} is not one of "
                         f"{sorted(REPLACEABLE_KINDS)}")
        if not str(rep.get("match") or "").strip():
            error(where, "replaceable_by.match must say which evidence retires this person")

    rc = person.get("reconstruction")
    if not isinstance(rc, dict) or rc.get("stage") not in stage_keys:
        error(where, f"a reconstructed person must name the programme stage that wrote them, "
                     f"one of {sorted(stage_keys)} - a person no stage claims is a person the "
                     f"programme cannot re-derive")
        return

    community = str(rc.get("community") or "").strip().lower()
    if community in REVIEWED_COMMUNITIES:
        if rc.get("stage") != UNDERDOCUMENTED_STAGE:
            error(where, f"a {community} reconstruction may be written ONLY by stage "
                         f"'{UNDERDOCUMENTED_STAGE}' (T-1177), not by '{rc.get('stage')}'")
        if rc.get("review_required") is not True or rc.get("touches_removal") is not True:
            error(where, f"a {community} reconstruction carries review_required and "
                         f"touches_removal, both true - AGENTS.md's Indigenous-history review")


def check_invented_name(where: str, person: dict, taken_names: set, error) -> None:
    """An invented name may never be a real person's name, nor outrank the invention."""
    pid = str(person.get("id") or "")
    if not pid.startswith(INVENTED_PERSON_PREFIX):
        return  # a re-admission under a read name; it is not invented and owes no pool
    name = " ".join(str(person.get("name") or "").split()).lower()
    if name and name in taken_names:
        error(where, f"the invented name {person.get('name')!r} is already borne by an attested "
                     f"or inferred person - a reader who met that name as a finding would meet "
                     f"it again as an invention")
    basis = person.get("name_basis")
    if not isinstance(basis, dict) or basis.get("confidence") != RECONSTRUCTED:
        error(where, "an invented name carries a name_basis graded 'reconstructed' naming the "
                     "pool it came from")


# --------------------------------------------------------------------------
# reading the committed layer
# --------------------------------------------------------------------------

def read_layer():
    """(reconstructed persons as (where, person), names borne by real people)."""
    reconstructed, real_names = [], set()
    for path in sorted(HOUSEHOLDS.glob("hh_*.json")):
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path.name}: {exc}")
        for person in rec.get("persons") or []:
            where = f"{path.name}:{person.get('id')}"
            if person.get("grade") == RECONSTRUCTED:
                reconstructed.append((where, person))
            else:
                name = " ".join(str(person.get("name") or "").split()).lower()
                if name:
                    real_names.add(name)
    return reconstructed, real_names


# --------------------------------------------------------------------------
# the stages, and the modules that build them
# --------------------------------------------------------------------------
#
# A STAGE IS A TICKET, and a stage large enough to need its own measurement, its own
# model file and its own gate gets its own module rather than another thousand lines
# here. The programme file names the module in `built_by`; this table is the writer's
# own copy, and `--check` holds the two together so a stage cannot be marked implemented
# with nothing behind it.

def _build_attribute_fill_sex_age() -> int:
    import reconstruct_sex_age
    return reconstruct_sex_age.build()


def _check_attribute_fill_sex_age() -> int:
    import reconstruct_sex_age
    return reconstruct_sex_age.check()


def _build_modelled_families() -> int:
    import reconstruct_modelled_families
    return reconstruct_modelled_families.build()


def _check_modelled_families() -> int:
    import reconstruct_modelled_families
    return reconstruct_modelled_families.check()


STAGE_BUILDERS = {"attribute_fill_sex_age": _build_attribute_fill_sex_age,
                  "modelled_families": _build_modelled_families}
STAGE_CHECKERS = {"attribute_fill_sex_age": _check_attribute_fill_sex_age,
                  "modelled_families": _check_modelled_families}


# --------------------------------------------------------------------------
# modes
# --------------------------------------------------------------------------

def cmd_list(prog: dict) -> int:
    print(f"{prog['id']} - {len(prog['stages'])} stage(s), written by {prog['written_by']}")
    for s in prog["stages"]:
        mark = "built" if s.get("implemented") else "not yet"
        print(f"  {s['key']:<26} {s['ticket']}  [{mark}]  {s['title']}")
    ob = prog["model_inputs"]["order_book"]
    if not (ROOT / ob["file"]).exists():
        print(f"\n  the order book ({ob['ticket']}) has not landed: {ob['file']}")
        print("  no stage may BUILD until it does - a reconstruction with no quota has "
              "nothing to stop at.")
    return 0


def cmd_build(prog: dict, key: str) -> int:
    table = stages(prog)
    if key not in table:
        print(f"FAIL unknown stage '{key}'. Known: {', '.join(sorted(table))}", file=sys.stderr)
        return 2
    stage = table[key]
    ob = prog["model_inputs"]["order_book"]
    if not (ROOT / ob["file"]).exists():
        print(f"REFUSED stage '{key}' ({stage['ticket']}): the order book has not landed "
              f"({ob['file']}, {ob['ticket']}). It is the quota, and a reconstruction with no "
              f"quota has nothing to stop at.", file=sys.stderr)
        return 1
    if not stage.get("implemented"):
        print(f"REFUSED stage '{key}': {stage['ticket']} has not been built yet. T-1167 opened "
              f"the programme and this writer; it deliberately writes no person. Implement the "
              f"stage in {stage['ticket']} and set `implemented` in the programme file.",
              file=sys.stderr)
        return 1
    builder = STAGE_BUILDERS.get(key)
    if builder is None:
        print(f"FAIL stage '{key}' is marked implemented but carries no build - the programme "
              f"file and this writer disagree", file=sys.stderr)
        return 2
    return builder()


def cmd_check(prog: dict) -> int:
    problems: list[str] = []

    def error(where, msg):
        problems.append(f"{where}: {msg}")

    table = stages(prog)

    # the programme is internally answerable
    if prog.get("written_by") != "tools/reconstruct_residents_1835.py":
        error("programme", "written_by does not name this tool")
    rows = prog["model_inputs"]["rows"]
    model = ROOT / prog["model_inputs"]["town_model"]
    if not model.exists():
        error("programme", f"town model {prog['model_inputs']['town_model']} is missing")
    for stage in prog["stages"]:
        for row in stage["draws_from"]:
            if row not in rows:
                error(f"stage {stage['key']}", f"draws from '{row}', which model_inputs.rows "
                                               f"does not define")
    if UNDERDOCUMENTED_STAGE not in table:
        error("programme", f"no '{UNDERDOCUMENTED_STAGE}' stage - the constraint that confines "
                           f"a Native or Metis reconstruction has nothing to name")
    for path in (NAME_POOLS, RETIRED):
        if not path.exists():
            error("programme", f"{path.name} is missing")

    # the retired programme stays retired
    if RETIRED.exists():
        old = json.loads(RETIRED.read_text(encoding="utf-8"))
        if old.get("resident_population_active") is not False:
            error(RETIRED.name, "resident_population_active is not false - the 2026-09-02 "
                                "retirement is what this programme supersedes WITHOUT restoring")

    # every reconstructed person in the committed layer answers to a stage
    reconstructed, real_names = read_layer()
    for where, person in reconstructed:
        check_reconstructed_person(where, person, set(table), error)
        check_invented_name(where, person, real_names, error)

    built = [s["key"] for s in prog["stages"] if s.get("implemented")]
    for key in built:
        if key not in STAGE_BUILDERS:
            error(f"stage {key}", "is marked implemented and this writer has no build for "
                                  "it - the programme file and the writer disagree")
    if problems:
        for p in problems:
            print(f"  FAIL {p}")
        return 1
    print(f"  ok    the programme answers for {len(prog['stages'])} stage(s); "
          f"{len(built)} implemented")
    print(f"  ok    {len(reconstructed)} reconstructed person(s) in data/residents/, each "
          f"holding the record contract")
    if not built:
        print("  ok    no stage has been built yet (T-1167 opened the programme and wrote "
              "nobody), so there is no draw to re-derive")
    for key in built:
        checker = STAGE_CHECKERS.get(key)
        if checker is None:
            continue
        print(f"  ---   stage '{key}' re-derives its own draw:")
        if checker() != 0:
            return 1
    return 0


def cmd_self_test() -> int:
    """The mutations the contract must refuse, one case per rule it states."""
    stage_keys = {"modelled_families", UNDERDOCUMENTED_STAGE}

    def refusals(person, taken=frozenset()):
        out = []
        check_reconstructed_person("case", person, stage_keys, lambda w, m: out.append(m))
        check_invented_name("case", person, set(taken), lambda w, m: out.append(m))
        return out

    good = {
        "id": "rc_bardwell_lucy", "name": "Lucy Bardwell", "grade": RECONSTRUCTED,
        "name_basis": {"confidence": RECONSTRUCTED, "note": "Drawn from the yankee pool."},
        "basis": {"kind": "model", "id": "household_size",
                  "note": "The head's own size band in the 1840 histogram wants one more."},
        "seed": seed_for("hh_rc_bardwell_lucy", "household_size"),
        "replaceable_by": {"kind": "person", "match": "a source naming this household's wife"},
        "reconstruction": {"stage": "modelled_families", "community": "yankee"},
    }

    cases = []

    def case(name, person, want, taken=frozenset()):
        cases.append((name, person, want, taken))

    case("a well-formed reconstruction passes", good, False)

    no_basis = {k: v for k, v in good.items() if k != "basis"}
    case("a reconstructed person without a basis is refused", no_basis, True)

    no_seed = dict(good); no_seed.pop("seed")
    case("a value drawn from a model without its seed is refused", no_seed, True)

    ruled = dict(good)
    ruled["basis"] = {"kind": "rule", "id": "head_rule", "note": "Argued, not drawn."}
    case("a rule-argued person carrying a seed is refused", ruled, True)

    ruled_ok = dict(ruled); ruled_ok.pop("seed")
    case("...and passes once the decorative seed is gone", ruled_ok, False)

    no_rep = {k: v for k, v in good.items() if k != "replaceable_by"}
    case("a reconstruction with no replacement rule is refused", no_rep, True)

    no_stage = dict(good); no_stage["reconstruction"] = {"community": "yankee"}
    case("a person no stage claims is refused", no_stage, True)

    wrong_stage = dict(good)
    wrong_stage["reconstruction"] = {"stage": "modelled_families", "community": "metis",
                                     "review_required": True, "touches_removal": True}
    case("a Metis reconstruction outside stage 'underdocumented' is refused", wrong_stage, True)

    unreviewed = dict(good)
    unreviewed["reconstruction"] = {"stage": UNDERDOCUMENTED_STAGE, "community": "native"}
    case("a Native reconstruction without its review is refused", unreviewed, True)

    reviewed = dict(good)
    reviewed["reconstruction"] = {"stage": UNDERDOCUMENTED_STAGE, "community": "native",
                                  "review_required": True, "touches_removal": True}
    case("...and passes in its own stage, carrying the review", reviewed, False)

    case("an invented name that an attested person already bears is refused",
         good, True, taken={"lucy bardwell"})

    over_graded = dict(good)
    over_graded["name_basis"] = {"confidence": "inferred", "note": "Drawn from the pool."}
    case("an invented name graded above the invention is refused", over_graded, True)

    readmission = {
        "id": "gale_abram", "name": "Abram Gale", "grade": RECONSTRUCTED,
        "basis": {"kind": "rule", "id": "readmission",
                  "note": "A read name the research withheld, re-admitted at its evidence limit."},
        "replaceable_by": {"kind": "person", "match": "a second independent source at the scene date"},
        "reconstruction": {"stage": "modelled_families", "community": "yankee"},
    }
    case("a re-admitted read name needs no name_basis and no pool", readmission, False,
         taken={"abram gale"})

    failures = 0
    for name, person, want_refused, taken in cases:
        got = refusals(person, taken)
        if bool(got) != want_refused:
            failures += 1
            print(f"  FAIL {name}: expected {'a refusal' if want_refused else 'a pass'}, "
                  f"got {got or 'a pass'}")
        else:
            print(f"  ok    {name}")

    # the seed is a string a reader can retype, and it redraws the same number
    a = seed_for("hh_rc_bardwell_lucy", "household_size")
    if a != "hh_rc_bardwell_lucy:household_size" or draw(a) != draw(a):
        failures += 1
        print("  FAIL the seed rule does not match the programme file")
    elif draw(a) == draw(seed_for("hh_rc_bardwell_lucy", "sex_ratio")):
        failures += 1
        print("  FAIL two buckets of one household draw the same number")
    else:
        print("  ok    the seed is a retypable string and each bucket draws its own number")

    # THE BOUNDARY, read from the syntax rather than from the prose. The docstring
    # above NAMES the refusal in order to explain the asymmetry, so a substring search
    # over the file would find its own explanation and fail. An AST walk sees imports
    # and calls and not the sentence that describes them.
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported = any(
        (isinstance(n, ast.Import) and any("refuse_reconstructed_grade" in a.name for a in n.names))
        or (isinstance(n, ast.ImportFrom) and "refuse_reconstructed_grade" in (n.module or ""))
        for n in ast.walk(tree))
    called = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                 and n.func.id in ("refuse", "refuse_texts")
                 for n in ast.walk(tree))
    if imported or called:
        failures += 1
        print("  FAIL this writer imports or calls the research writers' refusal - it is the "
              "one tool that may mint the grade, and wiring the refusal in would retire the "
              "programme the owner asked for")
    else:
        print("  ok    the one writer of the grade does not call the refusal the four "
              "research writers carry")

    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", help="the programme stage to run")
    ap.add_argument("--list", action="store_true", help="print the stage table")
    ap.add_argument("--build", action="store_true", help="run the stage named by --stage")
    ap.add_argument("--check", action="store_true", help="re-derive and hold the committed layer")
    ap.add_argument("--self-test", action="store_true", help="the mutations the contract refuses")
    args = ap.parse_args()

    if args.self_test:
        return cmd_self_test()
    if not PROGRAMME.exists():
        print(f"FAIL {PROGRAMME.relative_to(ROOT)} is missing - the programme is the only "
              f"authority under which a reconstructed resident may be written", file=sys.stderr)
        return 2
    prog = load_programme()
    if args.list:
        return cmd_list(prog)
    if args.build:
        if not args.stage:
            print("FAIL --build needs --stage", file=sys.stderr)
            return 2
        return cmd_build(prog, args.stage)
    if args.check:
        return cmd_check(prog)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
