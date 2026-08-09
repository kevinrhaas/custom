#!/usr/bin/env python3
"""Tests for the validator's load-bearing rules.

These exist because the date gate and the confidence contract are the two things
that quietly ruin historical reconstructions when they silently stop working.
A gate nobody tests is a gate nobody has.

    python3 tools/test_validate.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  pass  {name}")
    else:
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))
        FAILURES.append(name)


def phase(pid: str, frm: str, to: str) -> dict:
    return {
        "id": pid,
        "documented_range": {"from": frm, "to": to, "confidence": "documented",
                             "sources": ["s1"]},
        "position": {"utm_e": None, "utm_n": None, "symbolic_location": "somewhere",
                     "confidence": "conjectural"},
        "footprint": {"polygon": [[0, 0], [1, 0], [1, 1]], "confidence": "conjectural"},
        "form": {},
    }


def scene(date: str = "1835-07-01", released: bool = False) -> dict:
    return {"id": "t", "title": "t", "target_date": date,
            "terrain_epoch": "e", "layers": ["structures"], "released": released}


EPOCHS = {"e": {"id": "e", "from": "1833-07-01", "to": "1848-12-31"}}


def test_date_gate_excludes_later_building() -> None:
    """The Saloon Building problem: correct for 1836, wrong for 1835."""
    rep = V.Report()
    structures = {
        "sauganash.json": {"id": "sauganash", "phases": [phase("p", "1831-01-01", "1851-03-04")]},
        "saloon.json": {"id": "saloon_building", "phases": [phase("p", "1836-01-01", "1871-10-09")]},
    }
    V.validate_scene(scene(), structures, EPOCHS, {}, rep)
    note = " ".join(rep.notes)
    check("1836 building excluded from an 1835 scene",
          "1 structure(s) included" in note and "saloon_building" in note, note)
    check("date gate produces no error for a legitimate exclusion", not rep.errors, rep.errors)


def test_overlapping_phases_are_an_error() -> None:
    rep = V.Report()
    structures = {"x.json": {"id": "x", "phases": [phase("a", "1830-01-01", "1840-01-01"),
                                                   phase("b", "1834-01-01", "1845-01-01")]}}
    V.validate_scene(scene(), structures, EPOCHS, {}, rep)
    check("two phases covering one scene date is a hard error",
          any("phases cover scene" in e for e in rep.errors), rep.errors)


def test_epoch_must_cover_scene_date() -> None:
    rep = V.Report()
    V.validate_scene(scene("1830-01-01"), {}, EPOCHS, {}, rep)
    check("scene date outside its terrain epoch is an error",
          any("does not include target_date" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.validate_scene(scene(), {}, {}, {}, rep)
    check("unresolvable terrain epoch is an error",
          any("does not resolve" in e for e in rep.errors), rep.errors)


def test_review_required_blocks_release() -> None:
    rep = V.Report()
    structures = {"x.json": {"id": "x", "review_required": True,
                             "phases": [phase("p", "1831-01-01", "1851-01-01")]}}
    V.validate_scene(scene(released=True), structures, EPOCHS, {}, rep)
    check("review_required blocks a scene from being released",
          any("review_required" in e for e in rep.errors), rep.errors)


def test_exclusions_cannot_contradict_the_dataset() -> None:
    rep = V.Report()
    structures = {"x.json": {"id": "saloon_building",
                             "phases": [phase("p", "1831-01-01", "1851-01-01")]}}
    excl = {"excluded": [{"id": "saloon_building", "reason": "built 1836"}]}
    V.validate_scene(scene(), structures, EPOCHS, excl, rep)
    check("a structure both excluded and resolving into the scene is an error",
          any("exclusions.json" in e for e in rep.errors), rep.errors)


def test_confidence_contract() -> None:
    ids = {"s1"}

    rep = V.Report()
    V.check_attested("w", "k", {"value": 1, "confidence": "documented"}, ids, rep)
    check("documented without a source is an error",
          any("requires at least one source_id" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_attested("w", "k", {"value": 1, "confidence": "documented", "sources": ["nope"]}, ids, rep)
    check("documented citing an unresolvable source is an error",
          any("does not resolve" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_attested("w", "k", {"value": 1, "confidence": "inferred"}, ids, rep)
    check("inferred without stated reasoning is an error",
          any("requires a note" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_attested("w", "k", {"value": 1, "confidence": "inferred", "note": "because"}, ids, rep)
    check("inferred with reasoning passes", not rep.errors, rep.errors)

    rep = V.Report()
    V.check_attested("w", "k", {"value": 1, "confidence": "conjectural", "sources": ["s1"]}, ids, rep)
    check("conjectural citing a source warns", rep.warnings, "expected a warning")


def test_wide_range_rule_targets_guesses_not_facts() -> None:
    rep = V.Report()
    V.check_range("w", {"from": "1831-01-01", "to": "1851-03-04",
                        "confidence": "documented", "sources": ["s1"]}, {"s1"}, rep)
    check("a documented 20-year span does not warn (the Sauganash stood that long)",
          not rep.warnings, rep.warnings)

    rep = V.Report()
    V.check_range("w", {"from": "1820-01-01", "to": "1860-01-01",
                        "confidence": "conjectural"}, set(), rep)
    check("an undocumented 40-year span warns", rep.warnings, "expected a warning")

    rep = V.Report()
    V.check_range("w", {"from": "1840-01-01", "to": "1830-01-01"}, set(), rep)
    check("a reversed range is an error",
          any("precedes" in e for e in rep.errors), rep.errors)


def test_real_dataset_passes() -> None:
    """The shipped dataset must satisfy its own rules."""
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "validate.py")],
                       capture_output=True, text=True)
    check("the committed dataset validates clean", r.returncode == 0,
          r.stdout[-400:] + r.stderr[-400:])


def main() -> int:
    print("validator tests\n")
    for fn in sorted((f for name, f in globals().items()
                      if name.startswith("test_") and callable(f)),
                     key=lambda f: f.__code__.co_firstlineno):
        print(f"{fn.__name__}:")
        fn()
        print()
    if FAILURES:
        print(f"FAIL — {len(FAILURES)} check(s) failed: {', '.join(FAILURES)}")
        return 1
    print("PASS — all checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
