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


def test_an_exclusion_expires_at_its_own_earliest_scene() -> None:
    """The date gate runs both ways.

    An entry saying a building dates from 1837 is a correct exclusion from 1835
    and a wrong one from 1837 — and the second cannot be caught by comparing
    against the records, because an excluded structure has no record to compare
    with. In a year-parameterized project that difference is the whole point.
    """
    excl = {"excluded": [{"id": "saloon_building", "name": "Saloon Building",
                          "reason": "built 1836", "earliest_scene": "1837",
                          "sources": ["s1"]}]}
    rep = V.Report()
    V.validate_scene(scene(), {}, EPOCHS, excl, rep)
    check("an 1837 building is legitimately excluded from an 1835 scene", not rep.errors,
          rep.errors)

    rep = V.Report()
    V.validate_scene(scene("1837-07-01"), {}, EPOCHS, excl, rep)
    check("the same entry excluded from its own earliest scene is an error",
          any("earliest_scene" in e for e in rep.errors), rep.errors)


def test_exclusions_carry_a_reason_and_a_citation_that_resolves() -> None:
    """Rule one — never invent a source — applied where nothing applied it."""
    def run(entry: dict) -> list:
        rep = V.Report()
        V.check_exclusions({"excluded": [entry]}, {"s1"}, rep)
        return rep.errors

    good = {"id": "saloon_building", "name": "Saloon Building",
            "reason": "built 1836", "sources": ["s1"]}
    check("a named, reasoned, cited exclusion passes", not run(good), run(good))
    check("a citation that resolves in no source record is an error",
          any("does not resolve" in e for e in run({**good, "sources": ["nope"]})),
          run({**good, "sources": ["nope"]}))
    check("excluding a structure with no citation at all is an error",
          any("no sources" in e for e in run({**good, "sources": []})))
    check("an exclusion with no stated reason is a deletion, and an error",
          any("no reason" in e for e in run({**good, "reason": ""})))


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
          any("neither conjectural, nor declared" in e and "L7" in e
              for e in rep.errors), rep.errors)

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
          any("form.stories" in e and "neither conjectural, nor declared" in e
              for e in rep.errors), rep.errors)


def test_geometry_declaration_is_required_for_unread_attributes() -> None:
    """An attribute no generator reads is a claim with no geometry behind it.

    This is the omission half of the standard, and it is harder than the
    invention half for a reason worth stating: an invention leaves a mark in the
    record — a `conjectural` tag — and an omission leaves none at all. A
    `documented` attested value the archetype never reads looks exactly like a
    `documented` value it builds. The only thing that can tell them apart is the
    generator's own declaration of what it consumes, which is why the rule is
    driven from there rather than from a reviewer noticing.
    """
    consumed = {"a": frozenset({"roof_type"})}
    form = {"roof_type": {"value": "gable", "confidence": "documented", "sources": ["s1"]},
            "signage": {"value": "painted_wolf_sign", "confidence": "documented",
                        "sources": ["s1"]}}
    st = {"x.json": {"id": "x", "archetype": "a",
                     "phases": [phase("p", "1831-01-01", "1851-01-01", form)]}}

    rep = V.Report()
    V.check_geometry_declarations(st, consumed, rep)
    check("an attribute the archetype never reads must declare what the mesh does",
          any("form.signage" in e and "never reads it" in e for e in rep.errors), rep.errors)
    check("an attribute the archetype does read needs no declaration",
          not any("form.roof_type" in e for e in rep.errors), rep.errors)

    # Declaring over an attribute that IS built is a false admission, and would
    # quietly excuse a real omission if the parameter were ever dropped.
    rep = V.Report()
    form["roof_type"]["geometry"] = "absent"
    form["signage"]["geometry"] = "absent"
    V.check_geometry_declarations(st, consumed, rep)
    check("declaring geometry on an attribute the archetype builds is an error",
          any("form.roof_type" in e and "reads this attribute" in e for e in rep.errors),
          rep.errors)
    del form["roof_type"]["geometry"]

    # 'absent' over a false value admits to leaving out something the record says
    # was never there — the difference between a gap and a nothing.
    rep = V.Report()
    form["log_core"] = {"value": False, "confidence": "inferred", "note": "rejected reading",
                        "geometry": "absent"}
    V.check_geometry_declarations(st, consumed, rep)
    check("admitting to omitting a value the record says is false is an error",
          any("form.log_core" in e and "not there" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    form["log_core"]["geometry"] = "record_only"
    V.check_geometry_declarations(st, consumed, rep)
    check("a rejected reading declares record_only and passes", not rep.errors, rep.errors)

    rep = V.Report()
    form["signage"]["geometry"] = "invisible"
    V.check_geometry_declarations(st, consumed, rep)
    check("a geometry state outside the vocabulary is an error",
          any("'invisible'" in e for e in rep.errors), rep.errors)
    form["signage"]["geometry"] = "absent"

    # An archetype with no params module yet is skipped, not assumed to build
    # nothing: "no generator written" and "the generator ignores it" are
    # different states and only one is a finding.
    rep = V.Report()
    V.check_geometry_declarations(st, {}, rep)
    check("an archetype with no declared CONSUMED set is skipped, not indicted",
          not rep.errors, rep.errors)


def test_liberties_cover_omissions_and_simplifications() -> None:
    """An omission owes the document an entry exactly as an invention does.

    The discriminating case is the last one: `record_only` claims nothing is
    missing, so requiring a liberty for it would push the document toward
    admitting to things that were never taken — which devalues every admission
    that was.
    """
    consumed = {"a": frozenset({"roof_type"})}
    form = {"roof_type": {"value": "gable", "confidence": "documented", "sources": ["s1"]},
            "stables": {"value": True, "confidence": "documented", "sources": ["s1"],
                        "geometry": "absent"},
            "chimneys": {"value": 2, "confidence": "inferred", "note": "two on both views",
                         "geometry": "simplified"},
            "log_core": {"value": False, "confidence": "inferred", "note": "rejected",
                         "geometry": "record_only"}}
    st = {"x.json": {"id": "x", "archetype": "a",
                     "phases": [phase("p", "1831-01-01", "1851-01-01", form)]}}
    geometry = [covers("x", "footprint"), covers("x", "position")]

    rep = V.Report()
    V.check_liberties_coverage(st, {"liberties": [
        liberty("L1", "x: the outline and the placement are invented", ["x"], covers=geometry),
    ]}, rep, consumed)
    check("an attested feature the mesh omits with no liberty is an error",
          any("form.stables" in e and "'absent'" in e for e in rep.errors), rep.errors)
    check("a value a fixed default stands in for is an error too",
          any("form.chimneys" in e and "'simplified'" in e for e in rep.errors), rep.errors)
    check("the error says the model does not show what the record states",
          any("the model does not show" in e for e in rep.errors), rep.errors)
    check("a rejected reading owes no admission",
          not any("form.log_core" in e for e in rep.errors), rep.errors)
    check("an attribute the archetype builds owes no admission",
          not any("form.roof_type" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(st, {"liberties": [
        liberty("L2", "x: the outline, the placement, the yard and the stacks", ["x"],
                covers=geometry + [covers("x", "form.stables", "p"),
                                   covers("x", "form.chimneys", "p")]),
    ]}, rep, consumed)
    check("claiming both discharges them", not rep.errors, rep.errors)

    # Over-claiming an omission fails for the same reason over-claiming an
    # invention does. `roof_type` is built from the record, so admitting to
    # leaving it out is an admission to something that did not happen.
    rep = V.Report()
    V.check_liberties_coverage(st, {"liberties": [
        liberty("L3", "x: we left the roof off", ["x"],
                covers=geometry + [covers("x", "form.stables", "p"),
                                   covers("x", "form.chimneys", "p"),
                                   covers("x", "form.roof_type", "p")]),
    ]}, rep, consumed)
    check("claiming to have omitted something that is built is an error",
          any("form.roof_type" in e and "neither conjectural, nor declared" in e
              for e in rep.errors), rep.errors)

    # Without the archetype map the omission rule cannot run at all, and must not
    # pretend it did — the invention half still stands on its own.
    rep = V.Report()
    V.check_liberties_coverage(st, {"liberties": [
        liberty("L4", "x: the outline and the placement are invented", ["x"], covers=geometry),
    ]}, rep)
    check("with no CONSUMED map the omission rule reports nothing rather than guessing",
          not rep.errors, rep.errors)


def test_archetypes_declare_what_they_consume() -> None:
    """Every committed archetype states which attributes reach its mesh.

    Without this the gate above silently stops asking: an archetype that forgets
    the declaration would report zero unread attributes, which looks identical to
    an archetype that reads all of them.
    """
    rep = V.Report()
    consumed = V.archetype_consumed(rep)
    check("every params module declares a CONSUMED set", not rep.errors, rep.errors)
    check("the shipped archetypes are covered",
          {"frame_tavern", "log_dwelling"} <= set(consumed), sorted(consumed))
    check("the sets name real parameters, not prose",
          all(isinstance(a, str) and a.islower() for s in consumed.values() for a in s),
          consumed)


def test_consumed_attributes_actually_reach_the_parameters() -> None:
    """A declared attribute must MOVE something, not merely be listed.

    `CONSUMED` is the claim "this value reaches the mesh", and the omission gate
    excuses an attribute from admitting anything on the strength of it. So a name
    in that set which `from_phase` never reads is worse than an undeclared one: it
    is an admission the record is let off making, for geometry that is not there.

    That is not hypothetical. It has happened twice, both times because the record
    and the resolver spelled the same thing differently — `frame_extension` against
    `frame_addition`, and `chimney` against the `chimneys` every record states,
    which left Samuel Miller's second stack unbuilt while the count sat in the
    record looking built. Neither resolver ever complained, because a resolver
    reading an absent attribute just takes its default.

    The check is mechanical: perturb each stated value that its archetype declares
    it consumes, resolve again, and require the parameters to differ. A perturbation
    the parameters refuse outright counts as read — a ParamError is the loudest
    possible evidence that the value arrived.
    """
    import copy
    import json as _json

    sys.path.insert(0, str(V.ROOT / "generators"))
    resolvers, errors = {}, []
    for mod_path in sorted((V.ROOT / "generators" / "archetypes").glob("*_params.py")):
        mod = __import__(f"archetypes.{mod_path.stem}", fromlist=["from_phase"])
        resolvers[mod_path.stem.removesuffix("_params")] = mod

    def perturb(value):
        """A different value of the same kind, or None when there is nothing to try."""
        if isinstance(value, bool):
            return not value
        if isinstance(value, (int, float)):
            return value + 1
        if isinstance(value, str):
            return value + "_perturbed"
        return None

    def reaches(mod, ph: dict, attr: str) -> bool | None:
        """Does this attribute's VALUE change the parameters? None if untestable.

        Only the value is moved, never the confidence — `from_phase` copies every
        attribute's confidence into the parameters whatever it does with the value,
        so perturbing the whole block would report every attribute as read.
        """
        other = perturb(((ph.get("form") or {}).get(attr) or {}).get("value"))
        if other is None:
            return None
        moved = copy.deepcopy(ph)
        moved["form"][attr]["value"] = other
        try:
            return mod.from_phase(moved) != mod.from_phase(ph)
        except mod.ParamError:
            return True

    consumed = V.archetype_consumed()
    tested = 0
    records = {}
    for path in sorted((V.ROOT / "data" / "structures").glob("*.json")):
        st = _json.loads(path.read_text())
        records[st["id"]] = st
        arch = st.get("archetype")
        mod = resolvers.get(arch)
        if mod is None or arch not in consumed:
            continue
        for ph in st.get("phases", []):
            for attr in sorted((ph.get("form") or {}).keys()):
                if attr not in consumed[arch]:
                    continue
                got = reaches(mod, ph, attr)
                if got is None:
                    continue
                tested += 1
                if not got:
                    errors.append(f"{st['id']}/{ph['id']}: form.{attr} is in {arch}'s "
                                  f"CONSUMED set, but changing its value resolves to "
                                  f"identical parameters — the generator is not reading it")

    check("every consumed attribute the records state changes the parameters",
          not errors, "; ".join(errors))
    check("the check had real attributes to exercise", tested >= 20, f"{tested} exercised")

    # The discriminating cases, because a probe that cannot fail proves nothing.
    # `cladding` is the shape of the defect: stated by the record, ignored by the
    # resolver, and honest about it — it declares geometry: 'simplified'. If it were
    # ever added to CONSUMED without a parameter behind it, the loop above must say so.
    sauganash = records["sauganash_hotel"]["phases"][-1]
    ft = resolvers["frame_tavern"]
    check("an attribute the resolver ignores does not move the parameters",
          reaches(ft, sauganash, "cladding") is False)
    check("an attribute the resolver reads does",
          reaches(ft, sauganash, "stories") is True)


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


def test_mesh_input_hash_tracks_geometry_not_prose() -> None:
    """The staleness gate is only worth having if "stale" means "different building".

    A hash that fires on a rewritten note teaches the reader to ignore it, and an
    ignored gate is how a documented frame extension went unbuilt for a week. So
    the discriminating cases are asserted in both directions: prose moves nothing,
    and everything the builder can see moves the hash.
    """
    import copy  # noqa: PLC0415

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generators"))
    import mesh_inputs as M  # noqa: PLC0415

    st = {"id": "t", "archetype": "log_dwelling"}
    base = {
        "id": "p",
        "footprint": {"polygon": [[0, 0], [10, 0], [10, 6], [0, 6]],
                      "confidence": "conjectural"},
        "form": {
            "stories": {"value": 1, "confidence": "inferred", "note": "a note"},
            "construction": {"value": "log", "confidence": "documented"},
            "wall_height_m": {"value": 2.6, "confidence": "inferred"},
            "sign": {"value": "painted_wolf_sign", "confidence": "documented"},
        },
    }
    sha = M.structure_inputs_sha(st, base)

    def altered(fn) -> str:
        ph = copy.deepcopy(base)
        fn(ph)
        return M.structure_inputs_sha(st, ph)

    # --- things that cannot move a vertex ---
    check("rewriting a note does not make a mesh stale",
          altered(lambda p: p["form"]["stories"].update(note="rewritten at length")) == sha)
    check("a geometry declaration does not make a mesh stale",
          altered(lambda p: p["form"]["sign"].update(geometry="absent")) == sha)
    check("adding a source citation does not make a mesh stale",
          altered(lambda p: p["form"]["construction"].update(sources=["s1", "s2"])) == sha)
    check("the phase's own prose does not make a mesh stale",
          altered(lambda p: p.update(change_note="what changed and why")) == sha)

    # --- things that do ---
    check("a value the archetype reads makes the mesh stale",
          altered(lambda p: p["form"]["wall_height_m"].update(value=3.1)) != sha)
    check("a confidence change makes the mesh stale, because it is shaded into "
          "the geometry", altered(lambda p: p["form"]["stories"]
                                  .update(confidence="conjectural")) != sha)
    check("a redrawn footprint makes the mesh stale",
          altered(lambda p: p["footprint"].update(
              polygon=[[0, 0], [12, 0], [12, 7], [0, 7]])) != sha)

    # The Wolf Point case, which is what the whole rule was written for: the
    # record spells the sign `signage`, the archetype reads `sign`, so the
    # rename that fixes it is a different building and has to be re-baked.
    check("renaming an attribute to the name the archetype reads is a rebuild",
          altered(lambda p: p["form"].__setitem__(
              "signage", p["form"].pop("sign"))) != sha)

    # A default that changes silently is the same failure wearing a different hat.
    check("the derived properties are inside the hash",
          "addition_height_m" in M.structure_inputs_doc(st, base)["params"]["derived"])


def test_manifest_declares_the_scheme_the_generators_compute() -> None:
    """A re-stamp that forgets the scheme field would disable the gate quietly."""
    import json  # noqa: PLC0415

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generators"))
    import mesh_inputs as M  # noqa: PLC0415

    manifest = json.loads((V.ROOT / "assets" / "manifest.json").read_text())
    check("the committed manifest was stamped under the current scheme",
          manifest.get("inputs_scheme") == M.SCHEME,
          f"{manifest.get('inputs_scheme')!r} vs {M.SCHEME!r}")


class _Ramp:
    """A test heightfield: flat at `west` metres west of x, at `east` east of it.

    A step rather than a slope, because the thing under test is whether the
    check looks at the whole contact outline or only at the point the record
    happens to be placed on, and a step makes the difference unmissable.
    """

    def __init__(self, west: float, east: float, at_e: float = 5.0) -> None:
        self.west, self.east, self.at_e = west, east, at_e

    def height(self, e: float, n: float) -> float:  # noqa: ARG002 — n is flat
        return self.west if e < self.at_e else self.east


def _landing(structures, contacts, field, resolvers):
    return V.unlanded_values(structures, {"s.json": scene()}, V.Report(),
                             field, (0.0, 0.0), contacts, resolvers)


def _box(pid: str = "p", origin=(0.0, 0.0), poly=None) -> dict:
    ph = phase(pid, "1831-01-01", "1851-01-01")
    ph["position"] = {"utm_e": origin[0], "utm_n": origin[1], "rotation_deg": 0.0,
                      "confidence": "conjectural"}
    ph["footprint"] = {"polygon": poly or [[0, 0], [10, 0], [10, 6], [0, 6]],
                       "confidence": "conjectural"}
    return ph


def test_ground_contact_measures_the_whole_outline() -> None:
    """A structure has to reach the ground, and the origin is not the outline.

    The failure this rules out is the one the placement code invites: a building
    is put down at `terrain.height()` of its origin corner, so the origin sits on
    the ground by construction and the far corner can be anywhere.
    """
    st = {"x.json": {"id": "x", "archetype": "a", "phases": [_box()]}}
    contacts = {"a": {"mode": "perimeter", "anchor": None, "contact_z": None}}
    resolvers = {"a": lambda ph: object()}

    flat = _landing(st, contacts, _Ramp(0.0, 0.0), resolvers)
    check("a building on flat ground lands", not flat, flat)

    # The origin corner (0, 0) still sits on 0.0 — only the far half drops away.
    stepped = _landing(st, contacts, _Ramp(0.0, -1.2), resolvers)
    check("a building whose far corner hangs over a drop does not land",
          [f[0] for f in stepped] == ["x"], stepped)


def test_ground_contact_tolerance_is_the_step_up_rule() -> None:
    """0.35 m, and it is the walker's number rather than a fresh one."""
    st = {"x.json": {"id": "x", "archetype": "a", "phases": [_box()]}}
    contacts = {"a": {"mode": "perimeter", "anchor": None, "contact_z": None}}
    resolvers = {"a": lambda ph: object()}
    check("a step a person could take is not a finding",
          not _landing(st, contacts, _Ramp(0.0, -0.30), resolvers))
    check("a step a person could not take is",
          bool(_landing(st, contacts, _Ramp(0.0, -0.40), resolvers)))


def test_ground_contact_of_a_crossing_is_its_deck() -> None:
    """`ends` mode: only the end edges meet the ground, and at deck height.

    The discriminating case is a deck over a channel. Every sample between the
    ends is over water and would fail a perimeter test trivially — so a check
    that measured the whole outline would report every bridge ever built.
    """
    poly = [[0, 0], [20, 0], [20, 3], [0, 3]]
    st = {"b.json": {"id": "b", "archetype": "c", "phases": [_box(poly=poly)]}}

    class Channel:
        """Banks at +1.0, a bed at -3.0 between local E 4 and 16."""

        def height(self, e, n):  # noqa: ARG002
            return -3.0 if 4.0 < e < 16.0 else 1.0

    resolvers = {"c": lambda ph: object()}
    high = {"c": {"mode": "ends", "anchor": "water", "contact_z": lambda p: 2.22}}
    check("a deck 2.22 m over banks 1.0 m high does not land",
          [f[0] for f in _landing(st, high, Channel(), resolvers)] == ["b"])

    low = {"c": {"mode": "ends", "anchor": "water", "contact_z": lambda p: 1.10}}
    check("the same deck at bank height lands, and the water between is not counted",
          not _landing(st, low, Channel(), resolvers))


def test_ground_contact_declaration_is_checked_both_ways() -> None:
    """An unadmitted gap fails, and so does an admission with no gap."""
    gap = [("x", "p", "ground_contact", "structure x/p", 2.42)]

    rep = V.Report()
    V.check_ground_contact({"x.json": {"id": "x", "phases": [_box()]}}, gap, rep)
    check("a structure standing off the ground and saying nothing is an error",
          any("step-up rule" in e for e in rep.errors), rep.errors)

    declared = _box()
    declared["ground_contact"] = {"state": "approach_not_modelled", "note": "no source."}
    rep = V.Report()
    V.check_ground_contact({"x.json": {"id": "x", "phases": [declared]}}, gap, rep)
    check("declaring it satisfies the check", not rep.errors, rep.errors)

    rep = V.Report()
    V.check_ground_contact({"x.json": {"id": "x", "phases": [declared]}}, [], rep)
    check("declaring it while sitting on the ground is an error too",
          any("it lands" in e for e in rep.errors), rep.errors)

    bare = _box()
    bare["ground_contact"] = {"state": "approach_not_modelled", "note": "  "}
    rep = V.Report()
    V.check_ground_contact({"x.json": {"id": "x", "phases": [bare]}}, gap, rep)
    check("a state with no reasoning is an error", any("no note" in e for e in rep.errors),
          rep.errors)


def test_ground_contact_owes_the_liberties_document_an_entry() -> None:
    """The gap is an invention nobody drew, so the document has to own it."""
    ph = _box()
    ph["footprint"]["confidence"] = "documented"
    ph["position"]["confidence"] = "documented"
    structures = {"x.json": {"id": "x", "phases": [ph]}}
    unlanded = [("x", "p", "ground_contact", "structure x/p", 2.42)]

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L1", "x stands on nothing", ["x"]),
    ]}, rep, {}, unlanded)
    check("a structure that reaches no ground and no liberty saying so is an error",
          any("arriving nowhere" in e and "ground_contact" in e for e in rep.errors),
          rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L1", "x stands on nothing", ["x"],
                covers=[covers("x", "ground_contact", "p")]),
    ]}, rep, {}, unlanded)
    check("claiming it satisfies the check", not rep.errors, rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L1", "x stands on nothing", ["x"],
                covers=[covers("x", "ground_contact", "p")]),
    ]}, rep, {}, [])
    check("claiming a landing that is fine is an over-claim",
          any("standing off the ground" in e for e in rep.errors), rep.errors)


# --------------------------------------------------------------------------
# flora: the July phenology traps
# --------------------------------------------------------------------------
#
# docs/research/02-flora.md states these as rules a modeller should follow. A
# rule a modeller should follow is a rule a modeller will one day not follow, so
# the validator makes each of them unrepresentable and these tests prove it does.
# The dossier's own words: rendering 2 m turkey-foot seed heads on big bluestem
# in July is "the single most common historical-reconstruction error".

FLORA_VOCAB = {
    "roles": list(V.FLORA_ROLES),
    "forms_flora": ["grass_clump", "grass_arching", "sedge_tussock", "cattail", "forb_spike",
                    "forb_umbel", "scape_leafless", "mat_prostrate"],
    "forms_trees": ["tree_gallery"],
    "forms_unimplemented": ["vine_drape"],
    "phenology": list(V.FLORA_PHENOLOGY),
}


def flora_sp(**over) -> dict:
    sp = {
        "id": "x_y", "binomial": "Genus species", "common": "a plant",
        "role": "matrix", "form": "grass_clump",
        "abundance": {"cover_fraction": [0.1, 0.2]},
        "height_m": [0.5, 1.0],
        "july": {"phenology": "vegetative", "foliage_rgb": [90, 118, 60],
                 "inflorescence": None, "appearance": "leafy"},
        "confidence": "conjectural",
    }
    july = over.pop("july", None)
    sp.update(over)
    if july:
        sp["july"] = {**sp["july"], **july}
    return sp


def flora_errors(sp: dict) -> list:
    rep = V.Report()
    V.check_flora_species("z01_test", sp, {"s1"}, FLORA_VOCAB, rep, {})
    return rep.errors


def test_the_three_warm_season_grasses_cannot_have_july_seed_heads() -> None:
    """The single most common historical-reconstruction error, made unrepresentable."""
    for binomial in ("Andropogon gerardii", "Sorghastrum nutans", "Panicum virgatum"):
        errs = flora_errors(flora_sp(binomial=binomial, july={
            "phenology": "flowering",
            "inflorescence": {"shape": "spike", "rgb": [190, 170, 120],
                              "height_frac": 0.9, "size_m": [0.1, 0.2]}}))
        check(f"a flowering culm on {binomial} in July is an error",
              any("VEGETATIVE in mid-July" in e for e in errs), errs)

    errs = flora_errors(flora_sp(binomial="Andropogon gerardii", height_m=[1.6, 2.0]))
    check("big bluestem at its September height in a July record is an error",
          any("September height" in e for e in errs), errs)

    check("the same grass, vegetative and half height, is fine",
          not flora_errors(flora_sp(binomial="Andropogon gerardii", height_m=[0.8, 1.2])))


def test_cordgrass_and_bluejoint_must_be_in_flower() -> None:
    """The positive half of the same rule: cordgrass IS the tall element in July."""
    for binomial in ("Sporobolus michauxianus", "Calamagrostis canadensis"):
        errs = flora_errors(flora_sp(binomial=binomial))
        check(f"{binomial} recorded vegetative in July is an error",
              any("IS in flower in mid-July" in e for e in errs), errs)


def test_the_july_cattail_is_brown_and_fruiting() -> None:
    green = flora_sp(binomial="Typha latifolia", role="emergent", form="cattail",
                     abundance={"stems_per_m2": [30, 60]}, height_m=[1.5, 2.4],
                     july={"phenology": "fruiting", "foliage_rgb": [110, 132, 96],
                           "inflorescence": {"shape": "spadix", "rgb": [120, 160, 70],
                                             "height_frac": 0.8, "size_m": [0.15, 0.25],
                                             "fruit": True}})
    check("a green cattail spike in July is an error",
          any("BROWN" in e for e in flora_errors(green)), flora_errors(green))

    spring = flora_sp(binomial="Typha latifolia", role="emergent", form="cattail",
                      abundance={"stems_per_m2": [30, 60]}, height_m=[1.5, 2.4],
                      july={"phenology": "flowering", "foliage_rgb": [110, 132, 96],
                            "inflorescence": {"shape": "spadix", "rgb": [92, 62, 40],
                                              "height_frac": 0.8, "size_m": [0.15, 0.25]}})
    check("a cattail still flowering in July is an error",
          any("FRUITING in July" in e for e in flora_errors(spring)), flora_errors(spring))

    ok = flora_sp(binomial="Typha latifolia", role="emergent", form="cattail",
                  abundance={"stems_per_m2": [30, 60]}, height_m=[1.5, 2.4],
                  july={"phenology": "fruiting", "foliage_rgb": [110, 132, 96],
                        "inflorescence": {"shape": "spadix", "rgb": [92, 62, 40],
                                          "height_frac": 0.8, "size_m": [0.15, 0.25],
                                          "fruit": True}})
    check("a brown mature cattail passes", not flora_errors(ok), flora_errors(ok))

    banned = flora_sp(binomial="Typha angustifolia", role="emergent", form="cattail",
                      abundance={"stems_per_m2": [10, 20]}, height_m=[1.5, 2.4])
    check("a post-settlement cattail cannot be recorded at all",
          any("post-settlement arrival" in e for e in flora_errors(banned)),
          flora_errors(banned))


def test_ramps_have_no_leaves_in_july() -> None:
    """The plant the city is named for, and the trap it sets for a summer scene."""
    leafy = flora_sp(id="allium_tricoccum", binomial="Allium tricoccum", role="forb",
                     form="forb_umbel",
                     july={"phenology": "flowering", "foliage_rgb": [90, 150, 70],
                           "inflorescence": {"shape": "umbel_domed", "rgb": [236, 236, 228],
                                             "height_frac": 0.95, "size_m": [0.03, 0.05]}})
    check("green ramp foliage in a July record is an error",
          any("LEAFLESS" in e for e in flora_errors(leafy)), flora_errors(leafy))

    bare = flora_sp(id="allium_tricoccum", binomial="Allium tricoccum", role="forb",
                    form="scape_leafless", abundance={"stems_per_m2": [20, 60]},
                    height_m=[0.2, 0.4],
                    july={"phenology": "leafless", "foliage_rgb": None,
                          "inflorescence": {"shape": "umbel_domed", "rgb": [236, 236, 228],
                                            "height_frac": 0.95, "size_m": [0.03, 0.05]}})
    check("leafless scapes with a white umbel pass", not flora_errors(bare), flora_errors(bare))


def test_vegetative_and_budding_carry_nothing_in_flower() -> None:
    for ph in ("vegetative", "budding"):
        errs = flora_errors(flora_sp(july={
            "phenology": ph,
            "inflorescence": {"shape": "spike", "rgb": [230, 200, 60],
                              "height_frac": 0.9, "size_m": [0.05, 0.1]}}))
        check(f"'{ph}' with an inflorescence is an error",
              any("requires inflorescence null" in e for e in errs), errs)


def test_a_tawny_sward_is_not_july() -> None:
    """The October negative control, refused at the record rather than by eye."""
    errs = flora_errors(flora_sp(july={"foliage_rgb": [176, 158, 96]}))
    check("straw-coloured foliage in a July record is an error",
          any("not a July green" in e for e in errs), errs)
    check("a July green passes", not flora_errors(flora_sp(july={"foliage_rgb": [86, 104, 62]})))


def test_past_bloom_shows_a_fruit_not_a_flower() -> None:
    """Zizia is yellow in May and green in July; blue flag is blue in June."""
    yellow = flora_sp(binomial="Zizia aurea", role="forb", form="forb_umbel", july={
        "phenology": "past_bloom",
        "inflorescence": {"shape": "umbel_compound", "rgb": [230, 200, 60],
                          "height_frac": 0.9, "size_m": [0.05, 0.09]}})
    check("a past-bloom record still carrying the flower colour is an error",
          any("shows a fruit, not its flower colour" in e for e in flora_errors(yellow)),
          flora_errors(yellow))

    blue = flora_sp(binomial="Iris virginica", role="forb", form="forb_umbel", july={
        "phenology": "past_bloom",
        "inflorescence": {"shape": "capsule", "rgb": [96, 96, 190],
                          "height_frac": 0.7, "size_m": [0.05, 0.09]}})
    check("a blue flag still in flower in July is an error",
          any("shows a fruit, not its flower colour" in e for e in flora_errors(blue)),
          flora_errors(blue))

    green = flora_sp(binomial="Zizia aurea", role="forb", form="forb_umbel", july={
        "phenology": "past_bloom",
        "inflorescence": {"shape": "umbel_compound", "rgb": [140, 152, 86],
                          "height_frac": 0.9, "size_m": [0.05, 0.09], "fruit": True}})
    check("a green schizocarp passes", not flora_errors(green), flora_errors(green))


def test_abundance_takes_exactly_one_unit() -> None:
    both = flora_sp(abundance={"cover_fraction": [0.1, 0.2], "density_per_ha": [10, 20]})
    check("two abundance units in one entry is an error",
          any("EXACTLY ONE" in e for e in flora_errors(both)), flora_errors(both))
    over = flora_sp(abundance={"cover_fraction": [0.2, 1.4]})
    check("a cover fraction above 1 is an error",
          any("cover_fraction" in e for e in flora_errors(over)), flora_errors(over))


def test_a_form_the_vocabulary_does_not_declare_is_an_error() -> None:
    errs = flora_errors(flora_sp(form="grass_swirly"))
    check("an undeclared draw archetype is an error",
          any("not declared in index.json's vocabulary" in e for e in errs), errs)
    check("a form declared as unimplemented is allowed through",
          not flora_errors(flora_sp(form="vine_drape", role="thicket")))


class _FlatField:
    """A tiny all-land heightfield for the extent evaluator."""

    cols = rows = 5
    cell_m = 10.0
    origin_e = origin_n = 0.0

    def _at(self, i: int, j: int) -> float:  # noqa: ARG002 — flat on purpose
        return 1.0


def _zone(zid: str, extent: dict, plantable: bool = True) -> dict:
    return {"id": zid, "extent": extent, "plantable_in_scene": plantable}


def test_two_zones_may_not_tie_on_priority() -> None:
    rep = V.Report()
    zones = {"z01_a": _zone("z01_a", {"kind": "everywhere", "priority": 20}),
             "z02_b": _zone("z02_b", {"kind": "everywhere", "priority": 20})}
    V.check_flora_extents(zones, _FlatField(), rep)
    check("overlapping zones at equal priority are a data error",
          any("share priority" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    zones["z02_b"]["extent"]["priority"] = 21
    V.check_flora_extents(zones, _FlatField(), rep)
    check("distinct priorities resolve the overlap",
          not any("share priority" in e for e in rep.errors), rep.errors)


def test_a_zone_off_the_modelled_ground_has_to_say_so() -> None:
    """Zones 8 and 9 have no ground in this scene. The record must not pretend."""
    rep = V.Report()
    far = {"kind": "everywhere", "box": {"e": [1400, 1680], "n": [-320, 320]}, "priority": 12}
    V.check_flora_extents({"z08_lakeshore": _zone("z08_lakeshore", far, plantable=True)},
                          _FlatField(), rep)
    check("claiming a zone is plantable when nothing matches it is an error",
          any("plantable_in_scene is True" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_flora_extents({"z08_lakeshore": _zone("z08_lakeshore", far, plantable=False)},
                          _FlatField(), rep)
    check("recorded honestly as not plantable, it passes",
          not rep.errors, rep.errors)

    rep = V.Report()
    here = {"kind": "everywhere", "priority": 20}
    V.check_flora_extents({"z01_a": _zone("z01_a", here, plantable=False)}, _FlatField(), rep)
    check("a zone that does cover ground may not claim it does not",
          any("plantable_in_scene is False" in e for e in rep.errors), rep.errors)


def _flora_tree(mutate=None) -> Path:
    """A minimal, valid data/flora tree in a temp dir, optionally broken first.

    Built rather than copied so the test never writes inside data/ — other agents
    work this repo at the same time, and a test that edits a committed record is
    a test that can lose somebody's work.
    """
    import json as _json  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    root = Path(tempfile.mkdtemp()) / "flora"
    (root / "zones").mkdir(parents=True)
    (root / "palettes").mkdir(parents=True)
    pal = {"id": "p1", "name": "test", "greens": [[46, 60, 32], [68, 84, 44], [92, 110, 58]],
           "ground": {"rgb": [72, 84, 48], "wet_rgb": [58, 60, 40]}}
    zone = {
        "id": "z01_test", "zone": 1, "name": "test", "dossier": "docs/research/02-flora.md",
        "scene_date": "1835-07-01", "palette": "p1", "plantable_in_scene": True,
        "cover": {"matrix_fraction": 1.0, "bare_soil_fraction": 0.0,
                  "standing_water_fraction": 0.0},
        "ground": {"rgb": [72, 84, 48], "wet_rgb": [58, 60, 40]},
        "extent": {"kind": "everywhere", "priority": 20, "confidence": "conjectural"},
        "species": [flora_sp()], "confidence": "conjectural",
    }
    index = {
        "version": 1, "scene_date": "1835-07-01",
        "zones": [{"id": "z01_test", "zone": 1, "file": "zones/z01_test.json",
                   "palette": "p1", "priority": 20, "plantable_in_scene": True,
                   "extent": zone["extent"], "ground_rgb": [72, 84, 48],
                   "ground_wet_rgb": [58, 60, 40], "bare_soil_fraction": 0.0}],
        "palettes": [{"id": "p1", "file": "palettes/p1.json"}],
        "vocabulary": FLORA_VOCAB,
    }
    if mutate:
        mutate(index, zone, pal)
    (root / "zones" / "z01_test.json").write_text(_json.dumps(zone))
    (root / "palettes" / "p1.json").write_text(_json.dumps(pal))
    (root / "index.json").write_text(_json.dumps(index))
    return root


def _flora_check(mutate=None) -> list:
    root = _flora_tree(mutate)
    old, rep = V.FLORA, V.Report()
    try:
        V.FLORA = root
        V.check_flora({"s1"}, None, rep, {})
    finally:
        V.FLORA = old
    return rep.errors


def test_the_flora_manifest_must_agree_with_its_zone_records() -> None:
    """A denormalised copy that has drifted is worse than no copy at all."""
    check("a clean flora tree passes", not _flora_check(), _flora_check())

    def drift(index, zone, pal):
        index["zones"][0]["ground_rgb"] = [1, 2, 3]
    errs = _flora_check(drift)
    check("a manifest colour that disagrees with its zone record is an error",
          any("disagrees with the zone record" in e for e in errs), errs)

    def drift_priority(index, zone, pal):
        index["zones"][0]["priority"] = 99
    errs = _flora_check(drift_priority)
    check("a manifest priority that disagrees with the extent is an error",
          any("priority in the manifest disagrees" in e for e in errs), errs)

    def missing_file(index, zone, pal):
        index["zones"][0]["file"] = "zones/nope.json"
    errs = _flora_check(missing_file)
    check("a manifest entry naming a file that does not exist is an error",
          any("which does not exist" in e for e in errs), errs)


def test_a_palette_is_tuning_and_may_not_cite_a_source() -> None:
    def cited(index, zone, pal):
        pal["sources"] = ["s1"]
    errs = _flora_check(cited)
    check("a palette carrying a source_id is an error",
          any("must not carry a source_id" in e for e in errs), errs)

    def october(index, zone, pal):
        pal["greens"] = [[150, 148, 104], [176, 168, 120], [196, 190, 140]]
    errs = _flora_check(october)
    check("a straw foliage ramp is an error",
          any("not all July greens" in e for e in errs), errs)


def test_the_scene_date_and_the_phenology_block_must_agree() -> None:
    def october(index, zone, pal):
        index["scene_date"] = zone["scene_date"] = "1835-10-27"
    errs = _flora_check(october)
    check("an October scene_date against a july phenology block is an error",
          any("is not in July" in e for e in errs), errs)


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
