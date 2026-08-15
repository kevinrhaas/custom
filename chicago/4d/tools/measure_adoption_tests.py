#!/usr/bin/env python3
"""Evaluate method rule 6's three adoption tests for a roof, as a command.

ROADMAP T-A15, and the same move T-A14 made for the face rule. Rule 6 of
`data/reconstruction/1835_inferred_household_programme.json` says an anonymous block
roof may be adopted by an inferred household only where ALL THREE of these pass:

  1. the trade's own argument states IN ITS COMMITTED TEXT that its count is a floor
     rather than a bound;
  2. the roof's FAMILY is one this layer already houses that trade in;
  3. the roof's DIVISION is one this layer already houses that trade in.

Tests 2 and 3 are table lookups and have been reproducible since K21 put a `family` on
every roof this layer raises. **Test 1 is a statement about a paragraph of prose, and
until this tool nothing read it.** Every parcel that has cited it has cited it from
memory, and on 2026-08-15 that produced a claim which does not reproduce: T-A14 recorded
that the D4 it was dealt "passes all three tests" for the TEAMSTERS and the D2 for the
LAUNDRESSES. Measured here, neither trade's argument contains any statement about a floor
at all — the only occurrence of the word in the laundress argument is Andreas's "with the
floor covered besides", which is a plank floor in a boarding house. Only the CARPENTERS
and the LABOURERS state it. That is the difference between a rule and a habit, and it is
why this file exists rather than another remembered number.

**What test 1 is not.** It is not "method rule 3 lists this trade as unbounded". Rule 3
names four trades whose count is argued from the town's building rate rather than from a
roof cap — carpenters, labourers, laundresses, teamsters — and rule 6 could have been
written to point at that list. It was not: it was written to point at the trade's own
argument, which is a stronger requirement, because an argument that has never claimed to
be a floor has never invited anybody to raise it. The two readings disagree for exactly
two trades, and that disagreement is ROADMAP K28's, not this tool's, to settle. So this
prints BOTH: the literal reading it implements, and whether rule 3 names the trade.

Detection is deliberately conservative and always shows its working: a match is a
sentence in which "floor" is used as a predicate of the count, and every matched sentence
is printed so a reader can refuse it. A trade whose argument says nothing is reported as
NOT STATED, which is a failure — silence is not a pass, exactly as T-A5 held for test 2.

Standalone. Not wired into tools/check.sh: it measures a judgement, and a gate that
asserted the judgement would freeze K28's question shut.

Usage:
    tools/measure_adoption_tests.py D1 south          # one roof family in one division
    tools/measure_adoption_tests.py --roof recon_1835_blk_randolph_clark_d1_06
    tools/measure_adoption_tests.py --floors          # which trades state a floor, and why
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRUCTURES = DATA / "structures"
PROGRAMME = DATA / "reconstruction" / "1835_inferred_household_programme.json"

# Rule 3's four trades, quoted from the committed method list rather than retyped as a
# judgement. Used only to REPORT the disagreement described in the module docstring.
RULE_3_UNBOUNDED = ("carpenter", "labourer", "laundress", "teamster")

# "floor" used as a predicate of the count. The negative case this must not match is
# Andreas's "with the floor covered besides" in the laundress argument, where the floor
# is made of planks.
FLOOR_PREDICATE = re.compile(
    r"\b(?:is|as|still|remains|calls\s+itself|stated\s+as|state[sd]?)\s+"
    r"(?:a|its\s+own)?\s*\bfloor\b"
    r"|\ba\s+floor\s+(?:by|under|beneath)\b",
    re.IGNORECASE,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def family_of(structure_id: str) -> str | None:
    """The programme family a committed roof carries, or None.

    K21 put `reconstruction.family` on every roof this layer raises; the block parcels'
    roofs have carried it from the start. A roof with no family answers no test.
    """
    path = STRUCTURES / f"{structure_id}.json"
    if not path.exists():
        return None
    record = load(path)

    def find(node):
        if isinstance(node, dict):
            if isinstance(node.get("family"), str):
                return node["family"]
            for value in node.values():
                found = find(value)
                if found:
                    return found
        elif isinstance(node, list):
            for value in node:
                found = find(value)
                if found:
                    return found
        return None

    return find(record)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.])\s+", text) if s.strip()]


def floor_evidence(argument: str) -> list[str]:
    """Sentences in which the trade's own argument calls its count a floor."""
    return [s for s in sentences(argument) if FLOOR_PREDICATE.search(s)]


def table(programme: dict) -> dict[str, set[tuple[str, str]]]:
    """trade -> {(family, division)} this layer already houses it in."""
    housed: dict[str, set[tuple[str, str]]] = {}
    for household in programme["households"]:
        family = family_of(household["lives_at"]) if household.get("lives_at") else None
        if not family:
            continue
        housed.setdefault(household["occupation"], set()).add(
            (family, household["division"]))
    return housed


def report(programme: dict, family: str, division: str, verbose: bool) -> int:
    housed = table(programme)
    census = {e["occupation"]: e for e in programme["occupation_census"]}
    print(f"method rule 6, evaluated for a {family} roof in the "
          f"{division} division\n")
    print(f"  {'trade':<22}{'1 floor stated':<16}{'2 family':<11}"
          f"{'3 division':<12}verdict")
    passing = []
    for trade in sorted(census):
        pairs = housed.get(trade, set())
        families = {f for f, _ in pairs}
        divisions = {d for _, d in pairs}
        if family not in families and division not in divisions:
            continue
        evidence = floor_evidence(census[trade]["argument"])
        t1, t2, t3 = bool(evidence), family in families, division in divisions
        verdict = "ADOPTABLE" if (t1 and t2 and t3) else "refused"
        if t1 and t2 and t3:
            passing.append(trade)
        rule3 = " *" if (not t1 and trade in RULE_3_UNBOUNDED) else ""
        print(f"  {trade:<22}{('yes' if t1 else 'NOT STATED') + rule3:<16}"
              f"{('yes' if t2 else 'no'):<11}{('yes' if t3 else 'no'):<12}{verdict}")
        if verbose and evidence:
            for line in evidence:
                print(f"      floor: {line}")
    print()
    if passing:
        print(f"  {len(passing)} trade(s) pass all three tests: {', '.join(passing)}")
    else:
        print("  no trade passes all three tests — this roof stays an anonymous "
              "count-unit")
    print("\n  * method rule 3 names this trade unbounded, but its own argument never "
          "claims a\n    floor, so it fails test 1 as rule 6 is written. That "
          "disagreement is ROADMAP K28.")
    print("\n  Passing all three is permission, not an instruction. Whether a trade that "
          "has\n  not asked for a roof may be given one is ROADMAP K28 and is open.")
    return 0


def floors(programme: dict) -> int:
    census = programme["occupation_census"]
    print("test 1 — which trades state, in their own committed argument, that their "
          "count is a floor\n")
    for entry in sorted(census, key=lambda e: e["occupation"]):
        evidence = floor_evidence(entry["argument"])
        mark = "STATED    " if evidence else "not stated"
        rule3 = "  <- rule 3 calls this trade unbounded" if (
            not evidence and entry["occupation"] in RULE_3_UNBOUNDED) else ""
        print(f"  {entry['occupation']:<22}{mark}{rule3}")
        for line in evidence[:1]:
            print(f"      {line}")
    print("\n  A trade rule 3 calls unbounded whose argument never claims a floor fails "
          "test 1\n  on the literal reading rule 6 is written in. See ROADMAP K28.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("family", nargs="?", help="programme family, e.g. D1")
    ap.add_argument("division", nargs="?", help="south | north | west")
    ap.add_argument("--roof", help="read the family from a committed structure id")
    ap.add_argument("--floors", action="store_true",
                    help="report test 1 for every trade and quote the evidence")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="quote the sentence each floor verdict rests on")
    args = ap.parse_args()

    programme = load(PROGRAMME)
    if args.floors:
        return floors(programme)

    family, division = args.family, args.division
    if args.roof:
        family = family_of(args.roof)
        if not family:
            print(f"{args.roof}: no committed record, or it names no family")
            return 1
        record = load(STRUCTURES / f"{args.roof}.json")
        division = division or (record.get("reconstruction") or {}).get("district")
    if not family or not division:
        ap.error("give a family and a division, or --roof, or --floors")
    return report(programme, family.upper(), division.lower(), args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
