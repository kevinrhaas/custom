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


def test_the_watch_list_stops_a_promotion_it_only_used_to_ask_for() -> None:
    """The third category, and the sentence that had nothing behind it.

    `watch_list` has said since the scaffold that its entries are listed "so
    nobody promotes them to documented without new evidence". One of the four IS
    a committed record, so that sentence is checkable — and until this gate,
    nothing checked it. The discriminating case is therefore not a malformed
    entry but a well-formed one whose record has quietly been promoted.
    """
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    (tmp / "docs").mkdir()
    (tmp / "docs" / "d.md").write_text("## 1. Conflict: built 1834 or 1835?\n", encoding="utf-8")

    def entry(**over) -> dict:
        base = {"id": "western_hotel", "name": "Western Hotel",
                "question": "1834 or 1835?", "in_dataset": True,
                "carried_by": "frame_1834.documented_range",
                "dossier": {"file": "docs/d.md", "anchor": "Conflict: built 1834 or 1835?"},
                "sources": ["s1"]}
        base.update(over)
        return base

    def record(conf: str) -> dict:
        return {"w.json": {"id": "western_hotel", "phases": [
            {"id": "frame_1834",
             "documented_range": {"from": "1834-01-01", "to": "1840-12-31",
                                  "confidence": conf, "sources": ["s1"]}}]}}

    def run(item: dict, structures: dict | None = None, excluded=()) -> list:
        rep = V.Report()
        V.check_watch_list({"watch_list": [item], "excluded": list(excluded)},
                           structures if structures is not None else record("inferred"),
                           {"s1"}, rep, root=tmp)
        return rep.errors

    check("an open question on an inferred claim passes", not run(entry()), run(entry()))
    check("the same claim promoted to documented is an error",
          any("documented" in e for e in run(entry(), record("documented"))),
          run(entry(), record("documented")))
    check("an entry in the dataset that does not name the claim carrying the doubt fails",
          any("which claim" in e for e in run(entry(carried_by=""))))
    check("carried_by naming a phase the record does not have is an error",
          any("does not have" in e for e in run(entry(carried_by="nope.documented_range"))))
    check("carried_by naming something that is not a graded claim is an error",
          any("not a graded claim" in e for e in run(entry(carried_by="frame_1834.id"))))

    # both directions against the dataset — the L12 drift, which is a document
    # and its data disagreeing because nobody carried a change back
    check("declaring in_dataset with no such record is an error",
          any("no record of that id" in e for e in run(entry(), {})))
    check("a committed record the entry still calls unbuilt is an error",
          any("disagree" in e for e in run(entry(in_dataset=False))))

    # rule one, and the sentence that stands in for a citation when there is none
    check("a citation that resolves in no source record is an error",
          any("does not resolve" in e for e in run(entry(sources=["nope"]))))
    check("no sources and no stated reason for having none is an error",
          any("no_source_record" in e for e in run(entry(sources=[]))))
    check("no sources WITH the reason stated passes",
          not run(entry(sources=[], no_source_record="the dossier names no page")),
          run(entry(sources=[], no_source_record="the dossier names no page")))

    # a pointer into research that nobody can follow is not one
    check("a dossier file that is not committed is an error",
          any("not a committed file" in e
              for e in run(entry(dossier={"file": "docs/gone.md", "anchor": "x"}))))
    check("a dossier anchor that is not in the file is an error",
          any("anchor" in e for e in run(entry(dossier={"file": "docs/d.md",
                                                       "anchor": "not in there"}))))
    check("an entry with no question at all is an error",
          any("no question" in e for e in run(entry(question=""))))
    check("an id that is both excluded and an open question is an error",
          any("either ruled out" in e
              for e in run(entry(), excluded=[{"id": "western_hotel"}])))


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


def test_presence_is_held_to_the_confidence_contract() -> None:
    """The claim that decides whether a building is in the town at all.

    Every other `documented` value owes a resolving source. The date span was
    outside that rule until it started reaching the provenance card, which is
    exactly when an unsourced "documented" becomes a claim a visitor reads.
    """
    rep = V.Report()
    V.check_range("w", {"from": "1833-01-01", "to": "1880-12-31",
                        "confidence": "documented"}, {"s1"}, rep)
    check("a documented span with no source is an error",
          any("requires at least one source_id" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_range("w", {"from": "1833-01-01", "to": "1880-12-31",
                        "confidence": "documented", "sources": ["s1"]}, {"s1"}, rep)
    check("a documented span citing a resolving source passes", not rep.errors, rep.errors)

    # The discriminating case: the rule is about `documented`, not about every
    # range. An inferred span states its reasoning instead, and demanding a source
    # of it would push records towards citing something decorative.
    rep = V.Report()
    V.check_range("w", {"from": "1833-01-01", "to": "1836-12-31",
                        "confidence": "inferred", "note": "because"}, {"s1"}, rep)
    check("an inferred span with reasoning and no source passes", not rep.errors, rep.errors)


def test_the_card_is_fed_the_claims_it_renders() -> None:
    """A field the renderer reads and the compiler never writes renders nothing.

    This is not hypothetical: `popup.js` has read `documented_range` since the card
    was written and `compile_scene.py` did not emit it, so the one claim the whole
    scene rests on displayed as an empty string on every building for the life of
    the project, silently, with every gate green. Nothing could have caught it —
    the compiler was consistent with itself and `--check` only proves that. So the
    contract is asserted here instead: what the card reads off a sidecar has to be
    in the sidecar.
    """
    import json
    root = Path(__file__).resolve().parent.parent
    card = (root / "renderers/web/js/popup.js").read_text()
    # The structure sidecars are the ones the index lists — not "every file in
    # the directory minus the ones I remembered", which stops being true as soon
    # as another derived document is compiled beside them.
    index = json.loads((root / "data/sidecars/1835/index.json").read_text())
    records = [json.loads((root / "data" / e["sidecar"]).read_text())
               for e in index.get("structures", [])]
    check("the 1835 scene has sidecars to check", bool(records), "no sidecars found")

    for field in ("documented_range", "change_note"):
        check(f"the card reads {field}", f"s.{field}" in card, "not read by popup.js")
        missing = [r["id"] for r in records if field not in r]
        check(f"every 1835 sidecar carries {field}", not missing,
              f"absent on: {', '.join(missing)}")

    for field in ("position_note", "position_sources", "position_confidence"):
        check(f"the card reads placement.{field}", f"p.{field}" in card,
              "not read by popup.js")
        missing = [r["id"] for r in records if field not in r.get("placement", {})]
        check(f"every 1835 sidecar carries placement.{field}", not missing,
              f"absent on: {', '.join(missing)}")

    # The key can be present and say nothing, which renders the same as absent.
    # Asserted only where the value is structural rather than authored: the phase
    # resolution proves a span exists, while a note is a record's to write or not.
    blank = [r["id"] for r in records
             if not all((r.get("documented_range") or {}).get(k)
                        for k in ("from", "to", "confidence"))]
    check("every 1835 sidecar states a dated span and how sure it is",
          not blank, f"incomplete on: {', '.join(blank)}")


def liberty(lid: str, title: str, subjects: list, text: str = "",
            covers: list | None = None, section: str = "per_subject") -> dict:
    return {"id": lid, "title": title, "section": section, "subjects": subjects,
            "covers": covers or [],
            "fields": [{"label": "Decision", "text": text}]}


def covers(structure: str, aspect: str, phase_id: str | None = None) -> dict:
    return {"domain": "structure", "structure": structure, "phase": phase_id, "aspect": aspect}


def ground_covers(epoch: str, claim: str) -> dict:
    return {"domain": "terrain", "epoch": epoch, "claim": claim}


def ground_index(claims: dict, epoch: str = "e1834_harbor_cut") -> dict:
    """A terrain claim index of the shape `compile_scene.ground_claims` yields."""
    return {epoch: {cid: {"id": cid, "label": cid.split(".")[-1], "confidence": conf}
                    for cid, conf in claims.items()}}


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


def test_liberties_cover_what_the_ground_invents() -> None:
    """The terrain invents too, and until now no check could see that it had.

    Every other case in this file is about a building, because the gate read
    `data/structures/` and nothing else — so a 6 m bank face nobody recorded, on
    every bank in the box, was admitted only because somebody noticed and wrote
    L32. A liberty owed to attention is the arrangement this gate replaces.

    Two discriminating cases carry the design. The first is that the epoch is
    part of the claim: `docs/EPOCHS.md` versions the ground, so an admission
    about one shoreline must not silently discharge whatever the next one makes
    up. The second is that the domains do not reach into each other — a terrain
    token is not a structure named `terrain`, and neither can satisfy the other's
    obligation.
    """
    ground = ground_index({"bank": "conjectural",
                           "swales.west_prairie_swale_a": "conjectural",
                           "water": "documented"})
    empty: dict = {}

    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [
        liberty("L1", "No people, anywhere", []),
    ]}, rep, None, None, ground)
    check("a conjectural bank face with no liberty at all is an error",
          any("terrain e1834_harbor_cut/bank" in e for e in rep.errors), rep.errors)
    check("a conjectural swale with no liberty at all is an error",
          any("swales.west_prairie_swale_a" in e for e in rep.errors), rep.errors)
    check("the error quotes the token that would discharge it",
          any("`terrain.e1834_harbor_cut.bank`" in e for e in rep.errors), rep.errors)
    check("a documented ground claim owes no admission",
          not any("/water" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [
        liberty("L2", "Terrain: the bank face is a shape nobody recorded", [],
                covers=[ground_covers("e1834_harbor_cut", "bank"),
                        ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a")]),
    ]}, rep, None, None, ground)
    check("claiming both ground inventions satisfies the check", not rep.errors, rep.errors)

    # The epoch is load-bearing. An admission about the 1830 ground says nothing
    # about the 1834 ground, and a check that shrugged at the difference would
    # let the second scene ship with the first scene's confession attached.
    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [
        liberty("L3", "Terrain: the bank face is a shape nobody recorded", [],
                covers=[ground_covers("e1830_pre_cut", "bank"),
                        ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a")]),
    ]}, rep, None, None, ground)
    check("a claim against another epoch does not discharge this one's invention",
          any("terrain e1834_harbor_cut/bank" in e for e in rep.errors), rep.errors)
    check("and the claim against an epoch that is not committed is itself an error",
          any("no terrain epoch 'e1830_pre_cut'" in e for e in rep.errors), rep.errors)

    # Over-claiming, exactly as on a record. The water plane is documented, so
    # admitting to having invented it reads as diligence and provides none.
    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [
        liberty("L4", "Terrain: everything about the ground is a guess", [],
                covers=[ground_covers("e1834_harbor_cut", "bank"),
                        ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a"),
                        ground_covers("e1834_harbor_cut", "water")]),
    ]}, rep, None, None, ground)
    check("claiming to have invented a documented ground claim is an error",
          any("terrain.e1834_harbor_cut.water" in e and "neither conjectural" in e
              for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [
        liberty("L5", "Terrain: the bank face is a shape nobody recorded", [],
                covers=[ground_covers("e1834_harbor_cut", "bank"),
                        ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a")]),
        liberty("L6", "Terrain: the bed was sounded after all", [],
                covers=[ground_covers("e1834_harbor_cut", "water")], section="resolved"),
    ]}, rep, None, None, ground)
    check("a resolved entry may keep a claim the evidence has settled",
          not rep.errors, rep.errors)

    # A token naming a block the spec does not grade admits to nothing a visitor
    # can read, because the claims ARE what the Evidence panel shows.
    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [
        liberty("L7", "Terrain: the bank face and something else", [],
                covers=[ground_covers("e1834_harbor_cut", "bank"),
                        ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a"),
                        ground_covers("e1834_harbor_cut", "esplanade")]),
    ]}, rep, None, None, ground)
    check("a claim on a block the spec does not grade is an error",
          any("makes no graded claim 'esplanade'" in e for e in rep.errors), rep.errors)

    # The two domains are separate obligations. A structure's invention is not
    # discharged by a ground claim and the reverse holds too.
    structures = {"x.json": {"id": "x", "phases": [phase("p", "1831-01-01", "1851-01-01")]}}
    rep = V.Report()
    V.check_liberties_coverage(structures, {"liberties": [
        liberty("L8", "Terrain: the bank face is a shape nobody recorded", ["x"],
                covers=[ground_covers("e1834_harbor_cut", "bank"),
                        ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a")]),
    ]}, rep, None, None, ground)
    check("a ground admission does not cover a building's invented outline",
          any("footprint is conjectural" in e for e in rep.errors), rep.errors)
    check("and the ground's own claims stay discharged while it fails",
          not any("terrain e1834_harbor_cut/bank" in e for e in rep.errors), rep.errors)

    # With no terrain index the rule reports nothing rather than pretending the
    # ground invented nothing — the same shape as the CONSUMED map above.
    rep = V.Report()
    V.check_liberties_coverage(empty, {"liberties": [liberty("L9", "No people", [])]}, rep)
    check("with no terrain index the ground rule reports nothing rather than guessing",
          not rep.errors, rep.errors)


def test_the_checked_ground_is_the_ground_on_the_panel() -> None:
    """The set a liberty may admit to is the set a visitor reads. One enumeration.

    A gate walking its own copy of the spec would agree with the panel until the
    day somebody added a zone — and the new zone would be the one nobody had to
    own up to, which is precisely the failure the rule exists to prevent, one
    level up from where it was last found.
    """
    spec = {
        "bank": {"face_m": 6.0, "confidence": "conjectural"},
        "swales": [{"id": "new_zone_nobody_admitted_to", "depth_ft": 1.0,
                    "confidence": "conjectural"}],
        "water": {"surface_ft": 0.0, "confidence": "documented", "sources": ["s1"]},
    }
    rep = V.Report()
    index = V.terrain_claim_index({"e1834_harbor_cut": spec}, rep)
    check("the index is built off the compiler the panel renders from",
          not rep.errors and set(index["e1834_harbor_cut"])
          == {"bank", "swales.new_zone_nobody_admitted_to", "water"},
          sorted(index.get("e1834_harbor_cut", {})))

    owed = V.terrain_conjectural_values(index)
    check("a zone added to the spec is owed an admission the day it appears",
          sorted(cid for _e, cid, _l, _w in owed)
          == ["bank", "swales.new_zone_nobody_admitted_to"], owed)

    rep = V.Report()
    V.check_liberties_coverage({}, {"liberties": [
        liberty("L1", "Terrain: the bank face", [],
                covers=[ground_covers("e1834_harbor_cut", "bank")]),
    ]}, rep, None, None, index)
    check("and the gate demands it by name",
          any("new_zone_nobody_admitted_to" in e for e in rep.errors), rep.errors)


def test_the_committed_ground_admits_to_everything_it_invents() -> None:
    """The real dataset, against the real document.

    `test_real_dataset_passes` covers this through `validate.py --all`, but this
    one states the number, because the whole slice is the claim that the ground's
    inventions are inside the gate rather than only inside the panel.
    """
    rep = V.Report()
    index = V.terrain_claim_index(V.load_terrain_specs(rep), rep)
    owed = V.terrain_conjectural_values(index)
    check("the committed terrain states inventions a visitor walks on",
          len(owed) >= 6, f"{len(owed)} conjectural ground claim(s)")

    liberties = V.load_json(V.DATA / "liberties.json", rep) or {}
    claimed = {(c.get("epoch"), c.get("claim"))
               for e in liberties.get("liberties", [])
               for c in (e.get("covers") or []) if c.get("domain") == "terrain"}
    missing = [f"{e}.{c}" for e, c, _l, _w in owed if (e, c) not in claimed]
    check("and docs/LIBERTIES.md admits to every one of them", not missing, missing)


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
          claims[0] == covers("x", "footprint"), claims)
    check("a three-segment token names its phase",
          claims[1] == covers("x", "position", "p1"), claims)
    check("well-formed tokens report no problems", not problems, problems)

    problems = []
    claims = C.parse_covers("`x.p1.form.roof_type`, `x.form.gallery`", "L1b", problems)
    check("a form token keeps its prefix as part of the aspect",
          claims[1] == covers("x", "form.roof_type", "p1"), claims)
    check("a form token without a phase covers the structure",
          claims[0] == covers("x", "form.gallery"), claims)
    check("well-formed form tokens report no problems", not problems, problems)

    # The ground's namespace. It is deliberately NOT the structures' grammar, so
    # the parse is asserted to produce a different shape rather than a structure
    # named `terrain` — which is what a reader would have to disentangle later.
    problems = []
    claims = C.parse_covers("`terrain.e1834_harbor_cut.bank`, "
                            "`terrain.e1834_harbor_cut.swales.west_prairie_swale_a`",
                            "L4", problems)
    check("a terrain token parses into the terrain domain, not into a structure",
          claims[0] == ground_covers("e1834_harbor_cut", "bank"), claims)
    check("a ground claim keeps the group its id carries",
          claims[1] == ground_covers("e1834_harbor_cut", "swales.west_prairie_swale_a"), claims)
    check("well-formed terrain tokens report no problems", not problems, problems)
    check("both domains round-trip to the text the document wrote",
          [C.claim_token(c) for c in claims]
          == ["terrain.e1834_harbor_cut.bank",
              "terrain.e1834_harbor_cut.swales.west_prairie_swale_a"],
          [C.claim_token(c) for c in claims])

    problems = []
    C.parse_covers("`terrain.bank`, `terrain.e1834_harbor_cut`", "L5", problems)
    check("a terrain token without an epoch is reported, not read as a structure",
          any("terrain.bank" in p for p in problems), problems)
    check("a terrain token naming no claim is reported",
          any("terrain.e1834_harbor_cut'" in p for p in problems), problems)

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


SIDECAR_SHAPE = {
    "name": None,
    "aka": None,                       # a list — a leaf, as far as the scan goes
    "documented_range": {"from": None, "to": None, "confidence": None},
    "placement": {"local_e": None, "rotation_deg": None},
    "attributes": {"wall_height_m": {"value": None}},
}


def test_the_renderer_cannot_read_a_sidecar_field_the_compiler_never_writes() -> None:
    """The § 28 failure class, mechanised.

    `popup.js` read `documented_range` for the life of the project and
    `compile_scene.py` never wrote it, so the card's load-bearing claim rendered
    as an empty string and every gate stayed green: each half was consistent with
    itself. This is the check that compares the two halves.
    """
    def reads(js):
        return [p for _, p in V.sidecar_field_reads(js, SIDECAR_SHAPE)]

    def missing(js):
        return [p for p in reads(js) if not _resolves(p)]

    def _resolves(path):
        node = SIDECAR_SHAPE
        for seg in path.split("."):
            if not isinstance(node, dict):
                return True
            if seg not in node:
                return False
            node = node[seg]
        return True

    check("a field the compiler writes is read without complaint",
          not missing("const s = record.sidecar;\nreturn s.name;"),
          missing("const s = record.sidecar;\nreturn s.name;"))

    js = "const s = record.sidecar;\nif (s.asset_is_placeholder) flag();"
    check("a field no sidecar carries is caught", missing(js) == ["asset_is_placeholder"],
          missing(js))

    # The bug this class produces is always one level in from where you look: the
    # popup binds `placement` and then reads six fields off the binding.
    js = "const s = record.sidecar;\nconst p = s.placement ?? {};\nreturn p.rotation_deg + p.tilt;"
    check("a name bound to a sidecar block is followed into its fields",
          missing(js) == ["placement.tilt"], missing(js))

    # A list or a string is not a namespace. `aka.length` is a read of `aka`, and
    # a scan that called `length` a missing field would cry wolf on every array.
    js = "const s = record.sidecar;\nreturn s.aka.length && s.aka.map(String).join();"
    check("resolution stops at a value rather than reading into it", not missing(js),
          missing(js))

    # A name bound to a value binds nothing further: `e` here is a number, and
    # the `e` of a catch block two lines later is a different variable entirely.
    # A scan that followed it would report `e.message` against the sidecar.
    js = ("const s = record.sidecar;\nconst e = s.placement.local_e;\n"
          "try { g(e); } catch (e) { log(e.message); }")
    check("reusing a name bound to a value cannot invent a missing field",
          not missing(js), missing(js))

    js = "if (record.sidecar?.placement?.local_e) place();"
    check("a chain read straight off record.sidecar needs no binding",
          reads(js) == ["placement.local_e"], reads(js))

    js = "// this line used to read s.asset_is_placeholder\nconst s = record.sidecar;"
    check("a field named in a comment is not a read of it", not missing(js), missing(js))

    # A scanner that quietly stopped matching would pass every renderer ever
    # written, which is the failure mode a green gate cannot show you.
    real = sorted(p for p in (Path(__file__).resolve().parent.parent / "renderers").rglob("*.js")
                  if "vendor" not in p.parts)
    found = {f.name: V.sidecar_field_reads(f.read_text()) for f in real}
    live = {k: v for k, v in found.items() if v}
    check("the scan still finds the renderer's real reads",
          len(live) >= 4 and sum(len(v) for v in live.values()) >= 20,
          f"{len(live)} module(s), {sum(len(v) for v in live.values())} read(s)")
    check("the popup asks the sidecar whether the building was here",
          any(p == "documented_range" for _, p in found.get("popup.js", [])),
          found.get("popup.js"))
    check("and no longer asks it whether the mesh is a placeholder",
          not any("placeholder" in p for _, p in found.get("popup.js", [])),
          found.get("popup.js"))


def test_the_ground_is_held_to_the_rules_a_record_answers_to() -> None:
    """The terrain spec grades itself as carefully as a structure record and was
    checked by nothing, because until the ground claims reached the Evidence
    panel the file was read only by the generator. A citation there could have
    named a source that never existed — the second file after `exclusions.json`
    where rule one went unenforced, and this one is quoted to a visitor."""
    def run(spec: dict) -> tuple:
        rep = V.Report()
        V.check_terrain_claims({"s1"}, rep, {"e": spec})
        return rep.errors, rep.warnings

    good = {"water": {"surface_ft": 0.0, "confidence": "documented", "sources": ["s1"],
                      "note": "flat"}}
    check("a cited documented claim passes", not run(good)[0], run(good)[0])

    bad_src = {"water": {**good["water"], "sources": ["nope"]}}
    check("a citation that resolves in no source record is an error",
          any("does not resolve" in e for e in run(bad_src)[0]), run(bad_src)[0])

    uncited = {"water": {**good["water"], "sources": []}}
    check("documented with no source is an error, as it is on a record",
          any("documented with no source" in e for e in run(uncited)[0]), run(uncited)[0])

    # The spec's own caveat, enforced: no land vertex may claim to be documented,
    # because no contour survey of the 1835 town site exists. It was true because
    # whoever wrote the spec kept it true, and the walkthrough now shows the
    # sentence to visitors.
    land = {"divisions": [{"id": "south_division", "near_ft": 2.4,
                           "confidence": "documented", "sources": ["s1"], "note": "n"}]}
    check("a land elevation claiming to be documented is an error",
          any("land elevation marked documented" in e for e in run(land)[0]), run(land)[0])

    # Inferred-with-no-reasoning was a warning until 2026-08-10, and what held it
    # there was the staleness hash rather than the data: the only place to write a
    # ground claim's reasoning is terrain_spec.json, and that file's bytes were
    # hashed into the terrain's freshness, so a sentence of prose cost a Blender
    # bake. The hash strips prose now (generators/terrain_inputs.py), so the rule
    # is an error here exactly as it is on a structure record.
    thin = {"surface_materials": [{"zone": "north_division", "material": "loam",
                                   "confidence": "inferred"}]}
    errs, warns = run(thin)
    check("inferred with no reasoning is an error, as it is on a record",
          any("no reasoning recorded" in e for e in errs), f"{errs} / {warns}")
    reasoned = {"surface_materials": [{**thin["surface_materials"][0], "note": "why"}]}
    check("inferred with reasoning passes", not run(reasoned)[0], run(reasoned)[0])

    # The gate walks the same enumeration the panel does, so a zone added to the
    # spec is inside the rule the day it appears — the alternative is a checked
    # set that quietly stops being the displayed set.
    grown = {"divisions": [{"id": "brand_new_zone", "near_ft": 1.0,
                            "confidence": "documented", "sources": ["s1"], "note": "n"}]}
    check("a zone nobody has heard of is checked the day it is added",
          any("brand_new_zone" in e for e in run(grown)[0]), run(grown)[0])


def test_the_panel_shows_what_the_spec_grades() -> None:
    """The ground's claims are derived from the spec, not authored beside it.

    The failure this forecloses is the one § 28 found on the provenance card: a
    surface that reads a field the compiler never writes renders nothing, silently
    and forever. Here the compiler and the gate share one enumeration, so the
    assertion worth making is that the committed spec's graded blocks all arrive.
    """
    import json
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "tools"))
    import compile_scene as C  # noqa: PLC0415

    spec = json.loads((root / "data/terrain/epochs/e1834_harbor_cut"
                       / "terrain_spec.json").read_text())
    claims = C.ground_claims(spec, {})
    by_id = {c["id"]: c for c in claims}
    check("the committed spec yields claims", len(claims) >= 19, f"{len(claims)}")
    check("the water plane is documented and the bank face is not",
          by_id["water"]["confidence"] == "documented"
          and by_id["bank"]["confidence"] == "conjectural",
          f"{by_id['water']['confidence']} / {by_id['bank']['confidence']}")
    # `channel_profile` grades itself under `bed_confidence`. A claim that names
    # its grade differently is exactly the one an enumeration drops silently, and
    # renaming the key would still re-stale the ground: prose is out of the
    # terrain hash since 2026-08-10, a key that is not prose is not.
    check("a block that grades itself under another key is not dropped",
          by_id["channel_profile"]["confidence_key"] == "bed_confidence",
          str(by_id.get("channel_profile")))
    # A swale's `line` is eleven numbers describing the alignment its own entry
    # admits is invented. Figures are the spec's; geometry is not a figure.
    swale = by_id["swales.west_prairie_swale_a"]
    check("a claim carries the spec's own figures and not its geometry",
          {f["key"] for f in swale["fields"]} == {"half_width_m", "depth_ft", "dossier_zone"},
          str([f["key"] for f in swale["fields"]]))

    doc = json.loads((root / "data/sidecars/1835/terrain.json").read_text())
    check("the compiled ground doc carries the spec's caveat verbatim",
          doc["standard"] == spec["critical_caveat"])
    check("and the relief a visitor is told about is measured, not asserted",
          any("Measured from the committed heightfield" in c["text"]
              for c in doc["context"]), str(doc["context"])[:200])


def _terrain_inputs():
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "generators"))
    import terrain_inputs as T  # noqa: PLC0415
    return T, root / "data/terrain/epochs/e1834_harbor_cut"


def test_writing_a_ground_claims_reasoning_costs_no_bake() -> None:
    """Prose in the terrain spec is not a mesh input, and it used to be one.

    The ground's staleness hash was the concatenated BYTES of the spec, the two
    traced vector files, the datum and `terrain_gen.py`. So a sentence of
    reasoning written into the only file a ground claim's reasoning can go in
    reported the committed terrain as stale, and the reasoning rule had to stand
    as a warning because the fix could not land without Blender. That is
    `mesh_inputs`' "a hash that cries stale over a rewritten note gets
    disbelieved", still standing on the terrain side.

    The two directions are asserted together on purpose: a hash that ignores
    prose and a hash that ignores everything are the same hash until something
    numeric moves.
    """
    import copy  # noqa: PLC0415
    import json  # noqa: PLC0415
    import shutil  # noqa: PLC0415
    import tempfile  # noqa: PLC0415

    T, ep = _terrain_inputs()
    doc = T.terrain_inputs_doc(ep)
    base = T.terrain_inputs_sha(ep)

    def prose_keys(node) -> list:
        if isinstance(node, dict):
            return [k for k in node if T.is_prose(k)] + \
                   [k for v in node.values() for k in prose_keys(v)]
        if isinstance(node, list):
            return [k for v in node for k in prose_keys(v)]
        return []

    committed = json.loads((ep / "terrain_spec.json").read_text())
    check("the committed spec really does carry prose (else this proves nothing)",
          bool(prose_keys(committed)), "no prose keys in terrain_spec.json")
    check("and none of it survives into the input document",
          not prose_keys(doc), str(prose_keys(doc)))

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / ep.name
        shutil.copytree(ep, tmp)
        check("the copy hashes the same as the epoch it was copied from",
              T.terrain_inputs_sha(tmp) == base)

        spec = json.loads((tmp / "terrain_spec.json").read_text())
        rewritten = copy.deepcopy(spec)

        def rewrite(node) -> None:
            if isinstance(node, dict):
                for k, v in node.items():
                    if T.is_prose(k):
                        node[k] = "REWRITTEN"
                    else:
                        rewrite(v)
            elif isinstance(node, list):
                for v in node:
                    rewrite(v)

        rewrite(rewritten)
        check("rewriting every note, caveat and citation in the spec changes it",
              rewritten != spec, "the rewrite was a no-op")
        (tmp / "terrain_spec.json").write_text(json.dumps(rewritten, indent=1))
        check("...and the ground does not go stale for it",
              T.terrain_inputs_sha(tmp) == base, T.terrain_inputs_sha(tmp))

        # The same rule reaches the traced vectors, which carry a note per feature.
        river = json.loads((tmp / "river.geojson").read_text())
        rewrite(river)
        (tmp / "river.geojson").write_text(json.dumps(river, indent=1))
        check("nor for a note rewritten on a traced bank line",
              T.terrain_inputs_sha(tmp) == base, T.terrain_inputs_sha(tmp))

        # ...and the direction that matters more: a number the generator reads.
        moved = json.loads((tmp / "terrain_spec.json").read_text())
        moved["bank"]["face_m"] = float(moved["bank"]["face_m"]) + 1.0
        (tmp / "terrain_spec.json").write_text(json.dumps(moved, indent=1))
        check("moving the bank face by a metre DOES stale the ground",
              T.terrain_inputs_sha(tmp) != base)

        # A zone added to the spec is an input the day it appears — the denylist
        # is what makes that true, and an allowlist of today's keys would not.
        grown = json.loads((tmp / "terrain_spec.json").read_text())
        grown["swales"].append({"id": "invented_swale", "line": [[0, 0], [1, 1]],
                                "half_width_m": 5.0, "depth_ft": 0.5,
                                "confidence": "conjectural"})
        (tmp / "terrain_spec.json").write_text(json.dumps(grown, indent=1))
        check("and a zone nobody had heard of is a mesh input the day it is added",
              T.terrain_inputs_sha(tmp) != base)


def ground_claim_fixture(cid: str, conf: str, fields: list, label: str | None = None) -> dict:
    """One claim of the shape `compile_scene.ground_claims` yields, with figures."""
    return {"id": cid, "label": label or cid.split(".")[-1], "confidence": conf,
            "fields": fields, "sources": [], "citations": [], "notes": []}


def test_the_ground_must_say_what_it_does_not_build() -> None:
    """A figure on the panel with no vertex behind it has to say so.

    This is the omission rule arriving on the terrain, and the case that argues
    for it is in the committed data: five surface materials, two of them
    `documented`, over a ground mesh that is one earth colour edge to edge. The
    confidence chip grades how sure we are of the soil and cannot say that none
    of it was built.

    Both directions are pinned, as on the structure side. A declaration over a
    figure the generator DOES read is the more dangerous of the two errors — it
    reads as diligence and would silently excuse a real omission the day the
    generator stopped reading the value.
    """
    consumed = {"bank": frozenset({"face_m"}),
                "surface_materials": frozenset()}
    index = {"e1834_harbor_cut": {
        "bank": ground_claim_fixture("bank", "conjectural", [
            {"key": "face_m", "value": 6.0},
            {"key": "profile", "value": "ease_out", "mesh": "restated_in_code"},
        ]),
        "surface_materials.south": ground_claim_fixture(
            "surface_materials.south", "documented", [{"key": "material", "value": "loam"}]),
    }}

    rep = V.Report()
    V.check_ground_geometry(index, consumed, rep)
    check("a stated figure the generator never reads, undeclared, is an error",
          any("'material'" in e and "nothing in the ground comes from it" in e
              for e in rep.errors), rep.errors)
    check("a figure the generator does read owes no declaration",
          not any("'face_m'" in e for e in rep.errors), rep.errors)
    check("and a declared one is accepted",
          not any("'profile'" in e for e in rep.errors), rep.errors)

    # The declaration has to be one of the four states, and the fourth is the
    # ground's own: the water plane is a literal zero in the generator, so the
    # mesh agrees with the spec without reading it.
    rep = V.Report()
    V.check_ground_geometry({"e1834_harbor_cut": {"bank": ground_claim_fixture(
        "bank", "conjectural", [{"key": "profile", "value": "x", "mesh": "invented"}])}},
        consumed, rep)
    check("a declaration outside the vocabulary is an error",
          any("not one of" in e for e in rep.errors), rep.errors)

    # The false admission.
    rep = V.Report()
    V.check_ground_geometry({"e1834_harbor_cut": {"bank": ground_claim_fixture(
        "bank", "conjectural", [{"key": "face_m", "value": 6.0, "mesh": "absent"}])}},
        consumed, rep)
    check("declaring an omission over a figure the ground IS built from is an error",
          any("'face_m'" in e and "nothing to declare" in e for e in rep.errors), rep.errors)

    # "The generator ignores this block" and "nobody has said" are different
    # states, and only one of them is a finding — the same rule archetype_consumed
    # applies to an archetype with no params module.
    rep = V.Report()
    V.check_ground_geometry({"e1834_harbor_cut": {"lagoons.x": ground_claim_fixture(
        "lagoons.x", "inferred", [{"key": "depth_ft", "value": 2.0}])}}, consumed, rep)
    check("a graded block CONSUMED says nothing about is an error, not a pass",
          any("'lagoons'" in e for e in rep.errors), rep.errors)


def test_an_unbuilt_ground_figure_owes_the_document_an_admission() -> None:
    """The ground's omissions are claimed in the same namespace its inventions are.

    Per FIELD in the spec and per CLAIM in the document, because
    `terrain.<epoch>.<claim>` is the vocabulary `docs/LIBERTIES.md` already writes
    in and a soil profile is not separably admittable from the block that states
    it. `record_only` and `restated_in_code` owe nothing: neither is a thing
    missing from the model.
    """
    consumed = {"surface_materials": frozenset(), "bank": frozenset({"face_m"})}
    index = {"e1834_harbor_cut": {
        "surface_materials.south": ground_claim_fixture(
            "surface_materials.south", "documented",
            [{"key": "material", "value": "loam", "mesh": "simplified"}]),
        "bank": ground_claim_fixture("bank", "inferred", [
            {"key": "face_m", "value": 6.0},
            {"key": "dossier_zone", "value": 13, "mesh": "record_only"},
        ]),
    }}

    rep = V.Report()
    V.check_liberties_coverage({}, {"liberties": [liberty("L1", "No people", [])]},
                               rep, None, None, index, consumed)
    check("a soil the ground is not made of, unclaimed, is an error",
          any("surface_materials.south" in e and "does not contain" in e
              for e in rep.errors), rep.errors)
    check("a record_only figure owes the document nothing",
          not any("terrain e1834_harbor_cut/bank" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_liberties_coverage({}, {"liberties": [
        liberty("L2", "Terrain: the ground says what it is made of and nothing is", [],
                covers=[ground_covers("e1834_harbor_cut", "surface_materials.south")]),
    ]}, rep, None, None, index, consumed)
    check("claiming it satisfies the check", not rep.errors, rep.errors)

    # And the over-claim direction has to survive the new kind of obligation: a
    # documented claim that owes an admission for an OMISSION must not be
    # reported as an admission to an invention it never made.
    rep = V.Report()
    V.check_liberties_coverage({}, {"liberties": [
        liberty("L3", "Terrain: the bank face", [],
                covers=[ground_covers("e1834_harbor_cut", "bank")]),
    ]}, rep, None, None, index, consumed)
    check("claiming a block that is neither invented nor unbuilt is still an error",
          any("terrain.e1834_harbor_cut.bank" in e and "neither conjectural" in e
              for e in rep.errors), rep.errors)


def test_declared_terrain_reads_are_real_reads() -> None:
    """CONSUMED is a claim about `terrain_gen.py`, so it is checked against it.

    The map lives in `terrain_inputs.py` rather than beside `build_field`,
    because that generator's bytes are hashed into the ground and a constant no
    builder reads would have re-staled the terrain — see that module. What
    co-location would have bought is bought here instead: every key declared
    consumed must appear in the generator as a subscript or a `.get()`, so a
    declaration that stops being true fails rather than quietly excusing an
    omission. It is the terrain's answer to
    `test_consumed_attributes_actually_reach_the_parameters`, one step weaker —
    a text scan proves the key is read, not that the value moves a vertex — and
    the generator needs numpy to run at all, which `check.sh` deliberately does
    not have.
    """
    import re  # noqa: PLC0415
    root = Path(__file__).resolve().parent.parent
    T, _ = _terrain_inputs()
    src = (root / "generators/terrain_gen.py").read_text()

    def reads(key: str) -> bool:
        return bool(re.search(rf"""\[\s*['"]{re.escape(key)}['"]\s*\]""", src)
                    or re.search(rf"""\.get\(\s*['"]{re.escape(key)}['"]""", src))

    declared = sorted({k for keys in T.CONSUMED.values() for k in keys})
    missing = [k for k in declared if not reads(k)]
    check("every key declared consumed is actually read by the generator",
          not missing, f"{len(declared)} declared, unread: {missing}")
    check("the scan can tell the difference (it is a regex, so prove it can fail)",
          not reads("material") and not reads("bank_crest_ft"),
          "the generator now reads a key the spec declares unbuilt, so this "
          "scan proves nothing")


def test_terrain_prose_is_not_read_by_the_generator() -> None:
    """The denylist is a claim about the generator, so it is checked against it.

    Stripping a key from the hash asserts that no code turning the spec into
    vertices reads it. That is true today by inspection, and inspection is what
    this family of checks exists to replace — so the assertion is made against
    the source: no module under `generators/` may subscript or `.get()` a key the
    hash throws away. It stays a text scan for the same reason
    `check_sidecar_contract` is one: it errs loudly rather than quietly.
    """
    root = Path(__file__).resolve().parent.parent
    T, _ = _terrain_inputs()
    import re  # noqa: PLC0415

    mods = [root / "generators/terrain_gen.py"] + sorted((root / "generators/common").glob("*.py"))
    keys = sorted(T.PROSE_KEYS) + ["e_fold_note"]
    offenders = []
    for m in mods:
        src = m.read_text()
        for k in keys:
            # a READ — `d["note"]` or `d.get("note")`. Writing `"_doc": "..."` into
            # the generator's own output is not a read and must not be flagged.
            if re.search(rf"""\[\s*['"]{re.escape(k)}['"]\s*\]""", src) or \
               re.search(rf"""\.get\(\s*['"]{re.escape(k)}['"]""", src):
                offenders.append(f"{m.name} reads {k!r}")
    check("no generator reads a key the terrain hash strips", not offenders, str(offenders))
    check("the scan can see a read at all (it is a regex, so prove it fires)",
          bool(re.search(r"""\[\s*['"]grid['"]\s*\]""",
                         (root / "generators/terrain_gen.py").read_text())),
          "the generator stopped reading spec['grid'], so this scan proves nothing")


def test_a_restatement_is_held_to_the_half_it_restates() -> None:
    """`restated_in_code` is a promise, and a promise nothing checks is a note.

    The other three `mesh:` states say the ground does not contain a figure, and a
    reader who doubts one can go and look at the ground. This one says the mesh
    contains exactly what the figure says and gets it from somewhere else — a
    claim about two documents at once, held together until now by the hand that
    wrote them. Every kind of restatement is exercised here, including the two
    directions of the declaration itself, because an admission nobody made and a
    check guarding nothing are different failures with the same green result.
    """
    EP = "e1834_harbor_cut"

    def idx(cid, fields):
        return {EP: {cid: ground_claim_fixture(cid, "inferred", fields)}}

    # (1) figure — the restatement and the build instruction disagree.
    restates = {"divisions": {"bank_crest_ft": ("figure", "near_ft")}}
    rep = V.Report()
    V.check_restated_agreement(idx("divisions.south", [
        {"key": "near_ft", "value": 2.4},
        {"key": "bank_crest_ft", "value": 3.1, "mesh": "restated_in_code"}]), restates, rep)
    check("a crest that stopped matching the level the ramp is built to is an error",
          any("'bank_crest_ft'" in e and "'near_ft'" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_restated_agreement(idx("divisions.south", [
        {"key": "near_ft", "value": 2.4},
        {"key": "bank_crest_ft", "value": 2.4, "mesh": "restated_in_code"}]), restates, rep)
    check("and agreeing passes", not rep.errors, rep.errors)

    # (2) artifact — held against the heightfield the bake actually wrote, in the
    # units that artifact uses. This is the strong one: the thing being agreed
    # with is the ground, not a description of it.
    art = {"water": {"surface_ft": ("artifact", "heightfield.json:water_surface_m", 0.3048)}}
    rep = V.Report()
    V.check_restated_agreement(idx("water", [
        {"key": "surface_ft", "value": 1.5, "mesh": "restated_in_code"}]), art, rep)
    check("a water surface the committed ground does not have is an error",
          any("water_surface_m" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_restated_agreement(idx("water", [
        {"key": "surface_ft", "value": 0.0, "mesh": "restated_in_code"}]), art, rep)
    check("and the committed zero passes", not rep.errors, rep.errors)

    # (3) both directions of the declaration. A figure carrying the state with
    # nothing named on the other side of it is back where § 35 found it; an entry
    # naming a figure that no longer declares the state is a check guarding a
    # promise nobody made, which reads as diligence and is worse.
    rep = V.Report()
    V.check_restated_agreement(idx("bank", [
        {"key": "profile", "value": "ease_out", "mesh": "restated_in_code"}]),
        {"bank": {}}, rep)
    check("declaring the state with no named second half is an error",
          any("'profile'" in e and "unnamed second half" in e for e in rep.errors), rep.errors)

    rep = V.Report()
    V.check_restated_agreement(idx("divisions.south", [
        {"key": "near_ft", "value": 2.4},
        {"key": "bank_crest_ft", "value": 2.4, "mesh": "record_only"}]), restates, rep)
    check("a restatement declared as something that owes nothing is an error",
          any("'bank_crest_ft'" in e and "guarding" in e for e in rep.errors), rep.errors)


def test_a_prose_restatement_is_pinned_to_the_line_it_describes() -> None:
    """Prose cannot be compared to Python, so the weak check is labelled weak.

    A formula written out for a reader and implemented separately in
    `terrain_gen.py` can only be held to the presence of the line it names. That
    buys the realistic drift — the code moves and the sentence is left describing
    a cross-section the ground no longer has — and nothing else, which is why
    `RESTATES` says so and this test proves the two failure directions rather
    than the claim.
    """
    EP = "e1834_harbor_cut"

    def run(expr, key="profile"):
        rep = V.Report()
        V.check_restated_agreement(
            {EP: {"bank": ground_claim_fixture("bank", "conjectural", [
                {"key": key, "value": "written out for a reader",
                 "mesh": "restated_in_code"}])}},
            {"bank": {key: ("code", expr)}}, rep)
        return rep

    check("the ease-out the spec describes is in the generator",
          not run("ramp = 1.0 - (1.0 - t_bank) ** 2").errors,
          run("ramp = 1.0 - (1.0 - t_bank) ** 2").errors)
    check("a line that is not there is an error",
          any("appears 0 times" in e for e in run("ramp = smoothstep(t_bank)").errors),
          run("ramp = smoothstep(t_bank)").errors)

    # The comment trap, which is not hypothetical: `check_sidecar_contract`
    # reported ITSELF on its first run, because the comment explaining why a field
    # is no longer read names that field. A scan that a comment can satisfy proves
    # nothing at all, so the phrase below — which exists in `terrain_gen.py` only
    # inside the comment arguing for the ease-out — must not count as an
    # implementation of anything.
    check("a phrase that lives only in a comment does not satisfy the scan",
          any("appears 0 times" in e for e in run("undercut by the flow").errors),
          run("undercut by the flow").errors)

    # ...and the stripper has to know a `#` in a string from a comment, or it
    # would blank half the generator and pass everything.
    src = 'a = "keep # this"  # drop this\nb = 2\n'
    out = V.strip_py_comments(src)
    check("stripping comments leaves string literals alone",
          '"keep # this"' in out and "drop this" not in out, out)
    check("and leaves the line structure where it was",
          out.count("\n") == src.count("\n"), repr(out))


def test_a_placement_is_recomputed_from_its_control() -> None:
    """The claim is "the west face stands on the Canal frontage", not "E = 446937.4".

    So the discriminating case is a ROTATION. Five placements in this dataset are
    corner lots offset half a platted street from a modern intersection, and the
    coordinate they record is the footprint polygon's own origin — which, once a
    facade bearing turns the building, is not the corner the claim is about. A
    check that compared the recorded coordinate against the kerb would pass a
    building standing in the right place, pass a building rotated out of its lot,
    and have no opinion about which it was looking at. Both cases are asserted
    below, on one building, with only `rotation_deg` and the origin differing.
    """
    import json as _json
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    (tmp / "traces").mkdir(parents=True)
    (tmp / "terrain" / "epochs" / "e1").mkdir(parents=True)

    def control(**over) -> dict:
        doc = {
            "platted_street": {"width_ft": 66, "half_width_m": 10.0,
                               "confidence": "inferred", "note": "a stated reading",
                               "sources": ["s1"]},
            "streets": {"a": {"name": "A St", "axis": "ns"},
                        "b": {"name": "B St", "axis": "ew"}},
            "control": {"a_b": {"streets": ["a", "b"], "utm_e": 1000.0, "utm_n": 2000.0,
                                "osm_node_ids": [1], "osm_ways": ["A St", "B St"],
                                "lat": 41.0, "lon": -87.0}},
        }
        doc.update(over)
        return doc

    # a channel running north-south between E 1100 and E 1200, at every northing
    (tmp / "terrain" / "epochs" / "e1" / "river.geojson").write_text(_json.dumps({
        "type": "FeatureCollection", "features": [{
            "type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [
                [[1100, 0], [1200, 0], [1200, 9999], [1100, 9999], [1100, 0]]]}}]}),
        encoding="utf-8")

    def rec(pos: dict, poly=None) -> dict:
        base = {"utm_e": 1010.0, "utm_n": 2010.0, "confidence": "inferred"}
        base.update(pos)
        return {"t.json": {"id": "t", "phases": [{
            "id": "p",
            "position": base,
            "footprint": {"polygon": poly or [[0, 0], [5, 0], [5, 4], [0, 4]],
                          "confidence": "inferred"}}]}}

    CORNER = {"method": "platted_corner", "control": "a_b", "constraints": [
        {"face": "west", "street": "a", "kerb": "east"},
        {"face": "south", "street": "b", "kerb": "north"}]}

    def run(structures: dict, doc: dict | None = None) -> list:
        (tmp / "traces" / "street_control.json").write_text(
            _json.dumps(doc if doc is not None else control()), encoding="utf-8")
        rep = V.Report()
        V.check_position_derivations(structures, {"s1"}, rep, data_root=tmp)
        return rep.errors

    ok = rec({"derivation": CORNER})
    check("a corner lot standing on both frontages passes", not run(ok), run(ok))
    off = rec({"utm_e": 1013.0, "derivation": CORNER})
    check("the same building 3 m off its frontage is an error",
          any("west face" in e for e in run(off)), run(off))

    # the discriminating pair: the same claim, the same lot, the building turned
    turned = rec({"utm_e": 1014.0, "rotation_deg": 270.0, "derivation": CORNER})
    check("a building rotated onto its lot passes", not run(turned), run(turned))
    unturned = rec({"rotation_deg": 270.0, "derivation": CORNER})
    check("the unrotated origin at the same coordinate is an error",
          any("west face" in e for e in run(unturned)), run(unturned))

    # both directions
    check("coordinates with no derivation at all is an error",
          any("no `position.derivation`" in e for e in run(rec({}))))
    check("not_derivable without a reason is an error",
          any("undeclared" in e for e in run(rec({"derivation": {"method": "not_derivable"}}))))
    check("not_derivable WITH a reason passes",
          not run(rec({"derivation": {"method": "not_derivable", "reason": "no street here"}})))
    check("a control that does not resolve is an error",
          any("does not resolve" in e for e in
              run(rec({"derivation": dict(CORNER, control="nope")}))))
    check("a kerb on the wrong axis of its street is an error",
          any("no north kerb" in e for e in run(rec({"derivation": dict(
              CORNER, constraints=[{"face": "west", "street": "a", "kerb": "north"}])}))))

    # the control file's own rules
    nodeless = control(control={"a_b": {"streets": ["a", "b"], "utm_e": 1000.0,
                                        "utm_n": 2000.0}})
    check("control with no node ids and no stated gap is an error",
          any("cannot be re-fetched" in e for e in run(ok, nodeless)), run(ok, nodeless))
    check("the same control saying so passes",
          not run(ok, control(control={"a_b": {"streets": ["a", "b"], "utm_e": 1000.0,
                                               "utm_n": 2000.0, "gap": "ids not recorded"}})))

    # ids are re-fetchability; the names are re-derivability. The fault they
    # catch is a node set that re-fetches perfectly and is the wrong junction.
    unnamed = control(control={"a_b": {"streets": ["a", "b"], "utm_e": 1000.0, "utm_n": 2000.0,
                                       "osm_node_ids": [1], "lat": 41.0, "lon": -87.0}})
    check("node ids with no street names to re-derive the set from is an error",
          any("`osm_ways`" in e for e in run(ok, unnamed)), run(ok, unnamed))
    uncoordinated = control(control={"a_b": {"streets": ["a", "b"], "utm_e": 1000.0,
                                             "utm_n": 2000.0, "osm_node_ids": [1],
                                             "osm_ways": ["A St", "B St"]}})
    check("node ids with no lat/lon is an error",
          any("no lat/lon" in e for e in run(ok, uncoordinated)), run(ok, uncoordinated))

    # a crossing is derived from the traced bank instead, and the ends have to meet it
    def bridge(e0: float, var: float = 0.0, note: str = "why") -> dict:
        return rec({"utm_e": e0, "utm_n": 2000.0, "derivation": {
            "method": "traced_waterline", "control": "a_b",
            "centreline": {"axis": "n", "control_variance_m": var},
            "ends": {"epoch": "e1", "faces": ["west", "east"]},
            "note": note}},
            poly=[[0, 0], [100, 0], [100, 3], [0, 3]])
    check("a deck landing on both traced banks passes", not run(bridge(1100.0, var=1.5)),
          run(bridge(1100.0, var=1.5)))
    check("a deck a metre short of the bank is an error",
          any("meets no traced" in e for e in run(bridge(1102.0, var=1.5))))
    check("a variance from control that is not the declared one is an error",
          any("declares" in e for e in run(bridge(1100.0, var=0.0))))
    check("a declared variance with nothing explaining it is an error",
          any("explains it nowhere" in e for e in run(bridge(1100.0, var=1.5, note=""))))


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
