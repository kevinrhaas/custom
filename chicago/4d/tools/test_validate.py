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


def phase(pid: str, frm: str, to: str, form: dict | None = None) -> dict:
    return {
        "id": pid,
        "documented_range": {"from": frm, "to": to, "confidence": "documented",
                             "sources": ["s1"]},
        "position": {"utm_e": None, "utm_n": None, "symbolic_location": "somewhere",
                     "confidence": "conjectural"},
        "footprint": {"polygon": [[0, 0], [1, 0], [1, 1]], "confidence": "conjectural"},
        "form": form or {},
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


def liberty(lid: str, title: str, subjects: list, text: str = "",
            covers: list | None = None, section: str = "per_subject") -> dict:
    return {"id": lid, "title": title, "section": section, "subjects": subjects,
            "covers": covers or [],
            "fields": [{"label": "Decision", "text": text}]}


def covers(structure: str, aspect: str, phase_id: str | None = None) -> dict:
    return {"structure": structure, "phase": phase_id, "aspect": aspect}


def test_liberties_cover_conjectural_inventions() -> None:
    """A drawn shape nobody can defend has to be admitted somewhere a visitor reads.

    The load-bearing case is the third one: a liberty whose prose is all about
    footprints and placement, and which names the building, but which claims
    nothing. That is exactly the entry the old wording-matched rule accepted — and
    an entry can talk about a footprint while discharging something else entirely,
    so the building's invented outline went unrecorded while looking covered.
    """
    structures = {"x.json": {"id": "x", "phases": [phase("p", "1831-01-01", "1851-01-01")]}}

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L1", "No people, anywhere", []),
    ]}, rep)
    check("a conjectural footprint with no liberty at all is an error",
          any("footprint is conjectural" in e for e in rep.errors), rep.errors)
    check("a conjectural position with no liberty at all is an error",
          any("position is conjectural" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L2", "x: both footprints are invented", ["x"], covers=[covers("x", "footprint")]),
        liberty("L3", "x: placed from the shape of the bank", ["x"],
                covers=[covers("x", "position", "p")]),
    ]}, rep)
    check("claiming the footprint and the placement satisfies the check",
          not rep.errors, rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L4", "x: the footprint question, and how the building was placed", ["x"],
                "The outline drawn under it and its position were both discussed at length."),
    ]}, rep)
    check("prose about footprints and placement does not cover them — only a claim does",
          any("footprint is conjectural" in e for e in rep.errors)
          and any("position is conjectural" in e for e in rep.errors), rep.errors)
    check("the error says which liberties do name the building",
          any("L4" in e for e in rep.errors), rep.errors)
    check("the error shows the Covers token that would fix it",
          any("`x.p.footprint`" in e for e in rep.errors), rep.errors)

    # Naming a phase claims that phase and no other. A second phase invented the
    # same way needs its own admission — the whole point of phase granularity.
    rep = V.Report()
    two = {"x.json": {"id": "x", "phases": [phase("p", "1831-01-01", "1841-01-01"),
                                            phase("q", "1841-01-01", "1851-01-01")]}}
    V.check_liberties_coverage(two, {"liberties": [
        liberty("L5", "x: the first footprint is invented", ["x"],
                covers=[covers("x", "footprint", "p"), covers("x", "position")]),
    ]}, rep)
    check("a phase-scoped claim does not silently cover a sibling phase",
          any("x/q" in e and "footprint" in e for e in rep.errors)
          and not any("x/p" in e and "footprint" in e for e in rep.errors), rep.errors)
    check("a structure-scoped claim covers every phase that drew that aspect",
          not any("position is conjectural" in e for e in rep.errors), rep.errors)

    # The claims answer for themselves: over-claiming is as much a
    # misrepresentation as under-claiming.
    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L6", "x: everything is invented", ["x"],
                covers=[covers("x", "footprint"), covers("x", "position"),
                        covers("ghost", "footprint"), covers("x", "position", "nosuch")]),
    ]}, rep)
    check("a claim against a structure that does not exist is an error",
          any("'ghost.footprint'" in e for e in rep.errors), rep.errors)
    check("a claim against a phase that does not exist is an error",
          any("no phase 'nosuch'" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    settled = {"x.json": {"id": "x", "phases": [phase("p", "1831-01-01", "1851-01-01")]}}
    settled["x.json"]["phases"][0]["footprint"]["confidence"] = "documented"
    settled["x.json"]["phases"][0]["position"]["confidence"] = "documented"
    V.check_liberties_coverage(settled, {"liberties": [
        liberty("L7", "x: the footprint was invented", ["x"], covers=[covers("x", "footprint")]),
    ]}, rep)
    check("claiming an invention that the data no longer contains is an error",
          any("is not conjectural" in e and "L7" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(settled, {"liberties": [
        liberty("L7", "x: the footprint was invented — settled by the 1834 survey", ["x"],
                covers=[covers("x", "footprint")], section="resolved"),
    ]}, rep)
    check("the same claim under Resolved is not an error — evidence is allowed to arrive",
          not rep.errors, rep.errors)

    rep = V.Report()
    documented = {"x.json": {"id": "x", "phases": [phase("p", "1831-01-01", "1851-01-01")]}}
    documented["x.json"]["phases"][0]["footprint"]["confidence"] = "inferred"
    documented["x.json"]["phases"][0]["position"]["confidence"] = "inferred"
    V.check_liberties_coverage(documented, {"liberties": []}, rep)
    check("an empty liberties file is an error, not a silent pass",
          any("data/liberties.json" in e for e in rep.errors), rep.errors)


def test_liberties_cover_invented_form() -> None:
    """The requirement reaches past the drawn geometry to what the record states.

    A conjectural `roof_type` builds a gable and a visitor sees a gable; a
    conjectural `gallery: false` renders a plain front and a visitor sees a plain
    front. Neither announces itself the way an invented outline does, which is the
    argument for holding them to the same rule rather than a weaker one.
    """
    form = {"roof_type": {"value": "gable", "confidence": "conjectural",
                          "note": "PLACEHOLDER. Typical for the type."},
            "stories": {"value": 2, "confidence": "documented", "sources": ["s1"]}}
    structures = {"x.json": {"id": "x", "phases": [phase("p", "1831-01-01", "1851-01-01", form)]}}
    geometry = [covers("x", "footprint"), covers("x", "position")]

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L1", "x: the outline and the placement are invented", ["x"], covers=geometry),
    ]}, rep)
    check("a conjectural form attribute with no claim is an error",
          any("form.roof_type is conjectural" in e for e in rep.errors), rep.errors)
    check("owning up to the geometry does not cover what the record says the building was",
          not any("footprint is conjectural" in e for e in rep.errors), rep.errors)
    check("the error shows the form token that would fix it",
          any("`x.p.form.roof_type`" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L2", "x: outline, placement and roof", ["x"],
                covers=geometry + [covers("x", "form.roof_type", "p")]),
    ]}, rep)
    check("claiming the form attribute satisfies the check", not rep.errors, rep.errors)

    check("a documented form attribute is never required to be claimed",
          not any("form.stories" in e for e in rep.errors), rep.errors)

    # Over-claiming a form attribute has to fail for the same reason over-claiming
    # a footprint does: an admission to something we did not invent reads as
    # diligence and provides none.
    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L3", "x: everything about the roof was invented", ["x"],
                covers=geometry + [covers("x", "form.roof_type", "p"),
                                   covers("x", "form.stories", "p")]),
    ]}, rep)
    check("claiming an attribute that is not conjectural is an error",
          any("form.stories" in e and "is not conjectural" in e for e in rep.errors), rep.errors)


def test_covers_field_parses_to_claims() -> None:
    """The grammar the document is written in, checked at its own level.

    The aspect is the last segment and comes from a closed set, which is what
    tells `x.footprint` (all phases) from `x.p.footprint` (one) without guessing.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    import compile_liberties as C

    problems: list[str] = []
    claims = C.parse_covers("`x.footprint`, `x.p1.position`", "L1", problems)
    check("a two-segment token covers the structure, not one phase",
          claims[0] == {"structure": "x", "phase": None, "aspect": "footprint"}, claims)
    check("a three-segment token names its phase",
          claims[1] == {"structure": "x", "phase": "p1", "aspect": "position"}, claims)
    check("well-formed tokens report no problems", not problems, problems)

    problems = []
    claims = C.parse_covers("`x.p1.form.roof_type`, `x.form.gallery`", "L1b", problems)
    check("a form token keeps its prefix as part of the aspect",
          claims[1] == {"structure": "x", "phase": "p1", "aspect": "form.roof_type"}, claims)
    check("a form token without a phase covers the structure",
          claims[0] == {"structure": "x", "phase": None, "aspect": "form.gallery"}, claims)
    check("well-formed form tokens report no problems", not problems, problems)

    problems = []
    C.parse_covers("`x.roof_type`, `x`, the footprint", "L2", problems)
    check("an aspect outside the vocabulary is reported", any("roof_type" in p for p in problems),
          problems)
    check("a bare structure id is reported", any("'x'" in p for p in problems), problems)
    check("prose in a Covers field is reported, not silently parsed",
          any("the footprint" in p for p in problems), problems)

    problems = []
    C.parse_covers("  ", "L3", problems)
    check("a Covers field that claims nothing is reported",
          any("claims nothing" in p for p in problems), problems)


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
