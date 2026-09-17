#!/usr/bin/env python3
"""Derive `reaches_scene` on every resident role, and hold the singular
`occupation` to the roles that actually cover the scene date.

WHY THIS IS A TOOL AND NOT A FIELD SOMEBODY TYPES. `persons[].roles[]` (T-1223,
the first piece of T-1145) is the plural, dated replacement for one `occupation`
block, and the one thing a role must never be able to do is talk itself into
1835. Daniel Elston made soap in 1833, inspected schools in 1839 and pressed
brick in 1844, and the model showed `soap_and_candle_maker`, graded as an
ATTESTED 1835 occupation, out of an advertisement printed nineteen months before
the scene. Whether a role reaches 1 July 1835 is a question about that role's own
dates and nothing else, so it is DERIVED here, checked by `tools/validate.py`,
and refused when a record disagrees with its own arithmetic.

THE RULE IS CONSERVATIVE ON PURPOSE. A partial date is a range - `on: "1839"` at
`precision: "year"` covers the whole of 1839, because that is what the register
says and nothing narrower. A `from` with no `to` is an OPEN start and does NOT
continue: "still advertising in August 1834" is not evidence of trading in July
1835. `precision: "unknown"` reaches nothing, ever.

    python3 tools/roles.py --check    # gate: every reaches_scene matches its dates
    python3 tools/roles.py --write    # re-derive them into the household cards
    python3 tools/roles.py            # report what the layer carries
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import role_reaches, role_window          # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RESIDENTS = ROOT / "data" / "residents"
HOUSEHOLDS = RESIDENTS / "households"


def scene_date() -> str:
    return json.loads((RESIDENTS / "index.json").read_text(encoding="utf-8"))["scene_date"]


def cards() -> list[Path]:
    return sorted(HOUSEHOLDS.glob("*.json"))


def walk(scene: str):
    """(path, household, person, role, wanted) for every role in the layer."""
    for path in cards():
        doc = json.loads(path.read_text(encoding="utf-8"))
        for person in doc.get("persons") or []:
            for role in person.get("roles") or []:
                yield path, doc, person, role, role_reaches(role, scene)


def self_test() -> int:
    """The window rule, broken on purpose in each of the four ways that matter.

    Every one of these is a way a role could back-project itself into 1 July 1835,
    which is the fault T-1145 was filed against. They are asserted here rather than
    trusted because the rule is three lines of date arithmetic and the whole of the
    ticket rests on it.
    """
    scene = "1835-07-01"
    cases = [
        ("a day inside the window reaches it",
         {"on": "1835-07-01", "precision": "day"}, True),
        ("a day outside it does not",
         {"on": "1833-11-26", "precision": "day"}, False),
        ("a YEAR is a range and 1835 covers the scene",
         {"on": "1835", "precision": "year"}, True),
        ("…and 1839 does not",
         {"on": "1839", "precision": "year"}, False),
        ("a MONTH is a range and 1835-07 covers the scene",
         {"on": "1835-07", "precision": "month"}, True),
        ("a closed span containing the scene reaches it",
         {"from": "1833-11-26", "to": "1836", "precision": "year"}, True),
        ("an OPEN span does not continue - still advertising in 1834 is not "
         "evidence of trading in 1835",
         {"from": "1833-11-26", "to": None, "precision": "day"}, False),
        ("an UNDATED role reaches nothing, whatever else is on it",
         {"on": None, "from": None, "to": None, "precision": "unknown"}, False),
        ("a span that ends before the scene does not reach it",
         {"from": "1833-11-26", "to": "1834-07-02", "precision": "day"}, False),
    ]
    bad = 0
    for label, role, want in cases:
        got = role_reaches(role, scene)
        ok = got == want
        bad += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {label} → {got} (wanted {want})")
    # And the drift report itself: a role whose stored flag disagrees with its dates
    # has to be CAUGHT, or --check is a green light that reads nothing.
    planted = {"role": "brickmaker", "on": "1843", "precision": "year",
               "reaches_scene": True}
    caught = bool(planted.get("reaches_scene")) != role_reaches(planted, scene)
    print(f"  {'ok  ' if caught else 'FAIL'} a hand-set reaches_scene that its dates "
          f"refuse is caught")
    bad += 0 if caught else 1
    if bad:
        print(f"roles --self-test: {bad} assertion(s) did not fire")
        return 1
    print("roles --self-test: every assertion fired")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="refuse a reaches_scene that disagrees with the role's own dates")
    ap.add_argument("--write", action="store_true", help="re-derive reaches_scene in place")
    ap.add_argument("--self-test", action="store_true", dest="self_test",
                    help="prove the window rule by breaking it")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    scene = scene_date()
    drift: list[str] = []
    touched: dict[Path, dict] = {}
    people: set[str] = set()
    rows = 0
    reaching = 0

    for path, doc, person, role, want in walk(scene):
        rows += 1
        people.add(person.get("id"))
        if want:
            reaching += 1
        if bool(role.get("reaches_scene")) != want:
            w = role_window(role)
            drift.append(f"{person.get('id')} / {role.get('role')}: reaches_scene is "
                         f"{role.get('reaches_scene')!r}, and {w or 'an undated role'} "
                         f"makes it {want}")
            if args.write:
                role["reaches_scene"] = want
                touched[path] = doc

    if args.write:
        for path, doc in touched.items():
            path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"roles: {rows} assertion(s) on {len(people)} person(s); "
              f"re-derived {len(drift)} in {len(touched)} card(s)")
        return 0

    print(f"roles: {rows} assertion(s) on {len(people)} person(s); "
          f"{reaching} reach {scene}")
    if args.check:
        if drift:
            for line in drift[:20]:
                print(f"  FAIL {line}")
            print(f"roles --check: {len(drift)} role(s) disagree with their own dates. "
                  f"reaches_scene is derived - run tools/roles.py --write")
            return 1
        print("roles --check: every reaches_scene matches the role's own dates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
