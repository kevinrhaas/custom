#!/usr/bin/env python3
"""One row per home, workplace and business-location CLAIM the project holds — T-1230.

THE PROBLEM THIS ANSWERS. Where somebody lived, where he worked and where a house stood
is adjudicated in five different committed files, each with its own row shape, its own
vocabulary and its own idea of what "placed" means: the scene-date register decides what
the town does about a printed address, `street_face_adoptions.json` decides which roof a
street-only house takes, and the two back-projection ledgers decide whether a directory
address printed in 1839, 1843 or 1844 may be read back onto 1835 ground. Nothing reads
all five together. So the plain questions T-1147 asks — how many location claims does
this project hold, what stopped each one going narrower, and which ticket owns the ones
still open — could only be answered by opening five files and translating between them.

    python3 tools/reconcile_locations.py             re-derive and write the table
    python3 tools/reconcile_locations.py --check     re-derive and diff against committed
    python3 tools/reconcile_locations.py --report    the location axis, to stdout
    python3 tools/reconcile_locations.py --self-test prove the refusals fire

WHAT IS DERIVED HERE, AND WHAT IS ONLY CARRIED
----------------------------------------------
**No adjudication is made in this file.** Every disposition below is the verdict a
committed ledger already reached, copied with the ledger named in the row's own
`ledger` field — a location re-argued in a second file is a second location, and the
whole point of the table is that a later rung (T-1198's address book, T-1231's
relationships) can be added WITHOUT re-reading the evidence. Three things are derived,
each mechanical and each named:

  * `disposition` — the ledger's own outcome mapped onto one declared vocabulary, so
    that `enrich_existing`, `placed` and an adopted street face can be counted together.
    The mapping is the table DISPOSITION_OF_* below and is total: a ledger outcome this
    file has never met stops the build rather than falling into a bucket unseen.
  * `superseded_printing` — whether a business's placement READING is the one its record
    now stands on. A standing advertisement was reset week after week and the settings
    disagree; the gazetteer keeps every reading and stands the record on one of them.
    A reading that is not the live one is not a fault and not a second location, and
    counting it as a live claim would triple the town's location evidence overnight.
  * the household seating class — structure / lot / face / division / none, most
    specific first, over every household in the layer. It is a count and not a row,
    because a household with no location statement has made no claim.

WHAT THIS FILE MAY NOT DO
-------------------------
It may not grade. Where the ledger that placed a claim states no confidence — the
register grades no placement; it decides an action — the row carries `confidence: null`
and `confidence_silent_because` names the ledger that is silent. Manufacturing a grade
here would put a number on the card that no source ever said.

It may not close a standing question. Four printings in the Chicago American contradict
themselves about a street (T-0305), and three more questions stand open at T-0251,
T-0386 and T-1087. A claim under one of them carries `standing_question` BESIDE the
disposition its ledger reached; the question stays the owner's, and T-1235 retains or
resolves it. The four are read from `measure_american_contradictions.QUESTIONS` rather
than restated, so a question that closes there closes here in the same commit.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAZETTEER = DATA / "research" / "newspapers" / "gazetteer.json"
REGISTER = DATA / "research" / "newspapers" / "register_1835.json"
ADOPTIONS = DATA / "research" / "newspapers" / "street_face_adoptions.json"
ADDRESS_BP = DATA / "research" / "directories" / "address_back_projection.json"
RESIDENCE_BP = DATA / "research" / "directories" / "residence_back_projection.json"
HOUSEHOLDS = DATA / "residents" / "households"
OUT = DATA / "research" / "location_reconciliation.json"

SCENE_DATE = "1835-07-01"

#: The one vocabulary every ledger's verdict is mapped onto. Declared here so that
#: `--check` can refuse a disposition this file does not know, and so that a reader
#: meets the whole set in one place rather than inferring it from the rows.
DISPOSITIONS = {
    "placed_structure":
        "the claim reaches an individual committed structure",
    "placed_face":
        "the claim reaches a labelled street face and claims no lot and no roof of "
        "its own",
    "street_only_unadopted":
        "a platted street is named and nothing narrower, and no face on it was free "
        "to take the house",
    "unplaceable":
        "no usable anchor was printed, so the claim reaches no ground at all",
    "superseded_printing":
        "a second setting of the same advertisement places this subject, and the "
        "record stands on that one",
    "not_present_at_scene_date":
        "the subject is not in the town on the scene date, so its printed address "
        "positions nothing here",
    "already_better_placed":
        "an 1835 placement already holds this subject, and a later address may not "
        "displace one",
    "refused_back_projection":
        "the address was printed after the scene date and a clause of the "
        "back-projection policy refused it",
}

#: The register's action → this table's disposition. Total by construction: an action
#: this map has never met is a build failure, not a default.
DISPOSITION_OF_ACTION = {
    "enrich_existing": "placed_structure",
    "new_building": "placed_structure",
    "street_only": "street_only_unadopted",   # upgraded to placed_face by an adoption
    "unplaceable": "unplaceable",
}

#: The two back-projection ledgers' outcome → this table's disposition.
DISPOSITION_OF_BACKPROJECTION = {
    "placed": "placed_face",
    "already_better_placed": "already_better_placed",
    "refused": "refused_back_projection",
}

#: Which ticket owns a claim this project has deliberately left open. `T-0305` is read
#: from the declared questions rather than listed here.
STANDING_QUESTIONS = {
    "T-0305": "The Chicago American contradicts itself about this street, and none of "
              "the four is closeable from the material this repository holds.",
}


def load(path: Path):
    return json.loads(path.read_text())


def american_questions() -> dict[str, str]:
    """business id → T-0305, read off the declared questions rather than restated."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from measure_american_contradictions import QUESTIONS
    return {q["gazetteer_id"]: q["question"] for q in QUESTIONS if q.get("gazetteer_id")}


def source_of(claim: str) -> str:
    """A claim id is `<issue_id>#<claim>`; the issue id is the source."""
    return claim.split("#", 1)[0]


def row(**kw) -> dict:
    """Every row has every field. A missing key is a silence nobody can see."""
    base = {
        "row_id": None, "subject_kind": None, "subject_id": None, "subject_name": None,
        "household_id": None, "person_id": None, "business_id": None,
        "relation": None, "source_ids": [], "claim_or_record_ids": [],
        "describes_date": None, "describes_date_last": None, "date_precision": None,
        "printed_place": None,
        "resolved_street": None, "resolved_street_id": None, "resolved_face": None,
        "resolved_anchor": None, "resolved_structure": None,
        "confidence": None, "confidence_from": None, "confidence_silent_because": None,
        "disposition": None, "limit_clause": None, "ledger": None,
        "standing_question": None,
    }
    unknown = set(kw) - set(base)
    if unknown:
        raise SystemExit(f"reconcile_locations: unknown row field(s) {sorted(unknown)}")
    base.update(kw)
    return base


# --------------------------------------------------------------------------- businesses

def _triple(placement: dict) -> tuple:
    """What makes two settings of an advertisement the SAME placement.

    Not dict equality. The gazetteer's live `placement` is a reconciliation across the
    settings — it carries whichever transcription was clearest, so it is rarely
    byte-identical to any one of them, and five houses of 179 matched no reading at all
    when this was written as `==`. What a reading either agrees or disagrees with is the
    class, the anchor and the street: everything else is the compositor.
    """
    return (placement.get("class"), placement.get("anchor"), placement.get("street"))


def business_rows() -> list[dict]:
    gaz = {b["id"]: b for b in load(GAZETTEER)["businesses"]}
    reg = {b["id"]: b for b in load(REGISTER)["businesses"]}
    adopted = {a["business_id"]: a for a in load(ADOPTIONS)["adoptions"]}
    refused = {r["business_id"]: r for r in load(ADOPTIONS)["refusals"]}
    questions = american_questions()

    rows: list[dict] = []
    for bid in sorted(gaz):
        biz, entry = gaz[bid], reg.get(bid)
        if entry is None:
            raise SystemExit(f"reconcile_locations: {bid} is in the gazetteer and not "
                             f"in the register — the register is not a full read")
        live = biz.get("placement") or {}
        readings = biz.get("placement_readings") or []
        question = "T-0305" if bid in questions else None
        evidence = biz.get("evidence") or {}

        if not entry.get("present_at_scene_date"):
            rows.append(row(
                row_id=f"{bid}#premises",
                subject_kind="business", subject_id=bid, subject_name=biz.get("name"),
                business_id=bid, relation="premises",
                source_ids=sorted({source_of(c) for c in (biz.get("mentions") or [])}),
                claim_or_record_ids=list(biz.get("mentions") or []),
                describes_date=evidence.get("first_issue"),
                describes_date_last=evidence.get("last_issue"),
                date_precision="issue_range",
                printed_place=live.get("offset_text") or live.get("street"),
                standing_question=question,
                disposition="not_present_at_scene_date",
                ledger=str(REGISTER.relative_to(ROOT)),
                confidence_silent_because="the register decides presence, not a grade",
                limit_clause=entry.get("exclusion_note")
                or "The register does not hold this house in the town on the scene "
                   "date, so its printed address places nothing in 1835."))
            continue

        agree = [r for r in readings
                 if _triple(r.get("placement") or {}) == _triple(live)]
        claims = [c for r in agree for c in (r.get("claims") or [])] \
            or list(biz.get("mentions") or [])
        firsts = [r.get("first_issue") for r in agree if r.get("first_issue")]
        lasts = [r.get("last_issue") for r in agree if r.get("last_issue")]
        common = dict(
            row_id=f"{bid}#premises",
            subject_kind="business", subject_id=bid, subject_name=biz.get("name"),
            business_id=bid, relation="premises",
            source_ids=sorted({source_of(c) for c in claims}),
            claim_or_record_ids=claims,
            describes_date=min(firsts) if firsts else evidence.get("first_issue"),
            describes_date_last=max(lasts) if lasts else evidence.get("last_issue"),
            date_precision="issue_range",
            printed_place=live.get("offset_normalized") or live.get("offset_text")
            or live.get("street"),
            standing_question=question,
        )
        disposition = DISPOSITION_OF_ACTION.get(entry.get("action"))
        if disposition is None:
            raise SystemExit(f"reconcile_locations: {bid} carries register action "
                             f"{entry.get('action')!r}, which this table has never met "
                             f"— extend DISPOSITION_OF_ACTION deliberately")
        anchor = entry.get("anchor") or {}
        if disposition == "placed_structure":
            rows.append(row(**common,
                            disposition=disposition,
                            resolved_street=entry.get("street"),
                            resolved_street_id=entry.get("street_id"),
                            resolved_anchor={"kind": anchor.get("kind"),
                                             "target": anchor.get("target"),
                                             "via": anchor.get("via")},
                            resolved_structure=entry.get("action_target"),
                            ledger=str(REGISTER.relative_to(ROOT)),
                            confidence_silent_because=(
                                "the register decides an action, not a grade; the "
                                "roof's own record carries the building's"),
                            limit_clause=entry.get("action_note")
                            or "The printed anchor resolves to a committed structure; "
                               "nothing narrower than a building is claimed."))
        elif bid in adopted:
            a = adopted[bid]
            rows.append(row(**common,
                            disposition="placed_face",
                            resolved_street=a.get("street_name"),
                            resolved_street_id=a.get("street_id"),
                            resolved_face=a.get("face"),
                            resolved_anchor={"kind": "street_face",
                                             "target": a.get("street_id"),
                                             "via": "street_face_adoptions"},
                            resolved_structure=a.get("structure_id"),
                            confidence=a.get("roof_confidence"),
                            confidence_from=str(ADOPTIONS.relative_to(ROOT)),
                            ledger=str(ADOPTIONS.relative_to(ROOT)),
                            limit_clause=a.get("note")
                            or "The advertisement names a street and nothing narrower, "
                               "so this house takes a face and no lot."))
        elif disposition == "street_only_unadopted":
            r = refused.get(bid)
            rows.append(row(**common,
                            disposition=disposition,
                            resolved_street=entry.get("street"),
                            resolved_street_id=entry.get("street_id"),
                            ledger=str(ADOPTIONS.relative_to(ROOT)) if r
                            else str(REGISTER.relative_to(ROOT)),
                            confidence_silent_because=(
                                "no roof was taken, so no roof's grade applies"),
                            limit_clause=(f"{r['refusal']} — {r['detail']}" if r else
                                          "A platted street is named and nothing "
                                          "narrower, and the street-face deal did not "
                                          "reach this house.")))
        else:
            rows.append(row(**common,
                            disposition=disposition,
                            ledger=str(REGISTER.relative_to(ROOT)),
                            confidence_silent_because=(
                                "nothing was placed, so nothing is graded"),
                            limit_clause=entry.get("action_note")
                            or "The paper gives no anchor."))

        # And the settings that DISAGREE with the reading the record stands on. Kept
        # because a disagreement between settings is evidence, and counted apart
        # because three settings of one shop are not three shops.
        for n, reading in enumerate(readings):
            placement = reading.get("placement") or {}
            if _triple(placement) == _triple(live):
                continue
            rclaims = list(reading.get("claims") or [])
            rows.append(row(
                row_id=f"{bid}#superseded{n:02d}",
                subject_kind="business", subject_id=bid, subject_name=biz.get("name"),
                business_id=bid, relation="premises_superseded",
                source_ids=sorted({source_of(c) for c in rclaims}),
                claim_or_record_ids=rclaims,
                describes_date=reading.get("first_issue"),
                describes_date_last=reading.get("last_issue"),
                date_precision=("issue"
                                if reading.get("first_issue") == reading.get("last_issue")
                                else "issue_range"),
                printed_place=placement.get("offset_normalized")
                or placement.get("offset_text") or placement.get("street"),
                standing_question=question,
                disposition="superseded_printing",
                ledger=str(GAZETTEER.relative_to(ROOT)),
                confidence_silent_because=(
                    "a superseded setting is not graded — the record stands on "
                    "another one"),
                limit_clause=(
                    "This setting reads "
                    + (f"{placement.get('class')!r}" if placement.get("class") else "nothing")
                    + (f" at {placement.get('anchor')}" if placement.get("anchor") else "")
                    + (f" on {placement.get('street')}" if placement.get("street") else "")
                    + f"; the record stands on a setting reading {live.get('class')!r}"
                    + (f" on {live.get('street')}" if live.get("street") else "")
                    + ". The disagreement is kept because it is evidence, and counted "
                      "apart because settings of one advertisement are not premises.")))
    return rows


# -------------------------------------------------------------------------- households

#: Most specific first. The class a household is counted under is the first that fits.
SEATING_CLASSES = ("structure", "lot", "face", "division", "none")


def household_docs() -> list[dict]:
    return [load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))]


def seating_class(hh: dict, faces: set[str]) -> str:
    if (hh.get("lives_at") or {}).get("value"):
        return "structure"
    if hh.get("lot") or hh.get("lot_id"):
        return "lot"
    if hh["id"] in faces:
        return "face"
    if hh.get("division") not in (None, "unplaced"):
        return "division"
    return "none"


def household_rows(docs: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for hh in docs:
        for field, relation in (("lives_at", "home"), ("works_at", "workplace")):
            claim = hh.get(field) or {}
            if not claim.get("value"):
                continue
            rows.append(row(
                row_id=f"{hh['id']}#{field}",
                subject_kind="household", subject_id=hh["id"], subject_name=hh.get("name"),
                household_id=hh["id"], person_id=hh.get("head"), relation=relation,
                source_ids=list(claim.get("sources") or []),
                claim_or_record_ids=[f"{hh['id']}#{field}"],
                describes_date=SCENE_DATE, describes_date_last=SCENE_DATE,
                date_precision="scene_date",
                printed_place=claim.get("value"),
                resolved_structure=claim.get("value"),
                resolved_anchor={"kind": "structure", "target": claim.get("value"),
                                 "via": f"residents/households/{hh['id']}.json"},
                confidence=claim.get("confidence"),
                confidence_from=f"data/residents/households/{hh['id']}.json",
                disposition="placed_structure",
                ledger=f"data/residents/households/{hh['id']}.json",
                limit_clause=claim.get("note")
                or "The card names a committed structure; nothing narrower than a "
                   "building is claimed."))
    return rows


def back_projection_rows(path: Path, relation: str) -> list[dict]:
    doc = load(path)
    ledger = str(path.relative_to(ROOT))
    rows: list[dict] = []
    for n, r in enumerate(doc["rows"]):
        disposition = DISPOSITION_OF_BACKPROJECTION.get(r.get("outcome"))
        if disposition is None:
            raise SystemExit(f"reconcile_locations: {ledger} carries outcome "
                             f"{r.get('outcome')!r}, which this table has never met")
        clause = r.get("clause")
        limit = r.get("reason") or ""
        if clause:
            limit = f"Clause {clause}. {limit}"
        rows.append(row(
            row_id=f"{relation}#{n:03d}#{r['person_id']}",
            subject_kind="household", subject_id=r["household_id"],
            subject_name=r.get("person"),
            household_id=r["household_id"], person_id=r.get("person_id"),
            relation=relation,
            source_ids=list(r.get("sources") or []),
            claim_or_record_ids=[f"{ledger}#rows[{n}]"],
            describes_date=str(r.get("describes_date")),
            describes_date_last=str(r.get("describes_date")),
            date_precision="directory_year",
            printed_place=r.get("address_as_printed"),
            resolved_street=r.get("face"),
            resolved_street_id=r.get("street_id"),
            resolved_face=r.get("placement"),
            resolved_anchor=({"kind": "street_face", "target": r.get("street_id"),
                              "via": ledger} if r.get("street_id") else None),
            confidence=("reconstructed" if disposition == "placed_face" else None),
            confidence_from=(ledger if disposition == "placed_face" else None),
            confidence_silent_because=(
                None if disposition == "placed_face"
                else "nothing was placed, so nothing is graded"),
            disposition=disposition,
            ledger=ledger,
            limit_clause=limit or (
                "A directory printed after the scene date states this address; the "
                "back-projection policy decides whether it may be read backwards."),
            standing_question=None))
    return rows


# ------------------------------------------------------------------------------ derive

def limits_of(rows: list[dict]) -> dict[str, int]:
    """T-1147's three business location limits, counted off the rows themselves.

    Shared by `derive` and the gate on purpose: a count that is written once and
    checked against nothing is how 56/61/62 could drift from the rows it describes.
    """
    limits = {"structure": 0, "street_only": 0, "unplaceable": 0}
    for r in rows:
        if r["relation"] != "premises" or r["disposition"] == "not_present_at_scene_date":
            continue
        if r["disposition"] == "placed_structure":
            limits["structure"] += 1
        elif r["disposition"] in ("placed_face", "street_only_unadopted"):
            limits["street_only"] += 1
        elif r["disposition"] == "unplaceable":
            limits["unplaceable"] += 1
    return limits


def derive() -> dict:
    docs = household_docs()
    rows = business_rows()
    rows += household_rows(docs)
    rows += back_projection_rows(ADDRESS_BP, "later_workplace")
    rows += back_projection_rows(RESIDENCE_BP, "later_home")

    faces = {r["household_id"] for r in rows
             if r["relation"] == "later_home" and r["disposition"] == "placed_face"}
    classes = {c: 0 for c in SEATING_CLASSES}
    for hh in docs:
        classes[seating_class(hh, faces)] += 1

    limits = limits_of(rows)

    by_disposition: dict[str, int] = {}
    by_relation: dict[str, int] = {}
    for r in rows:
        by_disposition[r["disposition"]] = by_disposition.get(r["disposition"], 0) + 1
        by_relation[r["relation"]] = by_relation.get(r["relation"], 0) + 1

    return {
        "schema": 1,
        "generated_by": "tools/reconcile_locations.py",
        "scene_date": SCENE_DATE,
        "_doc":
            "DERIVED, NEVER AUTHORED. One row per home, workplace and business-location "
            "CLAIM this project holds, gathered from the five committed ledgers that "
            "already adjudicate them and translated into one vocabulary. Rebuilt by "
            "tools/reconcile_locations.py; tools/check.sh refuses a committed copy a "
            "rebuild would not produce. Nothing is adjudicated here — every disposition "
            "is the verdict its `ledger` reached, and a row that wants a different "
            "verdict is a change to that ledger, not to this file.",
        "nothing_is_adjudicated_here":
            "Every disposition below is carried from the committed ledger named in the "
            "row's own `ledger` field. Where that ledger states no confidence — the "
            "scene-date register decides an action, not a grade — the row carries a "
            "null confidence and says which ledger is silent. A grade invented here "
            "would put a number on the card that no source ever said.",
        "the_standing_questions_stay_open":
            "A claim under one of the four owner-retained source questions carries "
            "`standing_question` beside the disposition its ledger reached. The "
            "question is not answered here; T-1235 retains or resolves it.",
        "compiled_from": [
            str(p.relative_to(ROOT)) for p in
            (GAZETTEER, REGISTER, ADOPTIONS, ADDRESS_BP, RESIDENCE_BP)
        ] + ["data/residents/households/*.json"],
        "dispositions": DISPOSITIONS,
        "counts": {
            "rows": len(rows),
            "by_relation": by_relation,
            "by_disposition": by_disposition,
            "business_location_limits": limits,
            "household_seating_classes": classes,
            "households": len(docs),
            "standing_question_rows": sum(1 for r in rows if r["standing_question"]),
        },
        "rows": rows,
    }


def write(doc: dict) -> None:
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    c = doc["counts"]
    print(f"wrote {OUT.relative_to(ROOT)} — {c['rows']} row(s) over "
          f"{len(c['by_relation'])} relation(s)")


def gate(doc: dict) -> list[str]:
    """The refusals. Each one is a way this table could go quietly wrong."""
    bad: list[str] = []
    rows = doc["rows"]
    if not rows:
        bad.append("the table holds no location claim at all")
    seen: set[str] = set()
    for r in rows:
        who = r.get("row_id") or "<unnamed row>"
        if who in seen:
            bad.append(f"{who} appears twice — a row id is a claim's name")
        seen.add(who)
        if r.get("disposition") not in DISPOSITIONS:
            bad.append(f"{who} carries disposition {r.get('disposition')!r}, which is "
                       f"not in the declared vocabulary")
        if not r.get("limit_clause"):
            bad.append(f"{who} does not say what stopped it — a claim with no limit "
                       f"clause is a silence")
        if not r.get("ledger"):
            bad.append(f"{who} names no ledger, so nothing says who adjudicated it")
        if r.get("confidence") is None and not r.get("confidence_silent_because"):
            bad.append(f"{who} has no confidence and does not say which ledger is "
                       f"silent about it")
        if r.get("confidence") is not None and not r.get("confidence_from"):
            bad.append(f"{who} carries a grade and does not say where it was read")
        if r.get("disposition") == "placed_structure" and not r.get("resolved_structure"):
            bad.append(f"{who} is placed on a structure and names none")
        if r.get("disposition") == "placed_face" and not r.get("resolved_face") \
                and not r.get("resolved_street_id"):
            bad.append(f"{who} is placed on a face and names neither face nor street")
        if r.get("disposition") in ("unplaceable", "street_only_unadopted") \
                and r.get("resolved_structure"):
            bad.append(f"{who} reaches no building and has been given one — this table "
                       f"may not place what its ledger refused")
        if not r.get("source_ids") and not r.get("claim_or_record_ids"):
            bad.append(f"{who} rests on no source and no record — that is not a claim")
    c = doc["counts"]
    if c["rows"] != len(rows):
        bad.append("the row count does not count the rows")
    if sum(c["household_seating_classes"].values()) != c["households"]:
        bad.append("the seating classes do not cover every household exactly once")
    if set(c["household_seating_classes"]) != set(SEATING_CLASSES):
        bad.append("the seating classes are not the declared four-plus-none")
    # T-1147's 123 location limits. Every business the register holds in the town on
    # the scene date falls in exactly one of the three, and a claim that quietly moved
    # from `unplaceable` to `placed_structure` without a source is the one thing the
    # parent ticket says may never happen unseen.
    live = [r for r in rows if r["relation"] == "premises"
            and r["disposition"] != "not_present_at_scene_date"]
    if sum(c["business_location_limits"].values()) != len(live):
        bad.append("the three business location limits do not cover every business the "
                   "register holds in the town exactly once")
    if c["business_location_limits"] != limits_of(rows):
        bad.append("the three business location limits no longer count the rows they "
                   "are the limits of — a house has been promoted or demoted without "
                   "the count following it")
    return bad


def check(doc: dict) -> int:
    bad = gate(doc)
    if bad:
        for line in bad[:20]:
            print(f"FAIL: {line}")
        if len(bad) > 20:
            print(f"FAIL: … and {len(bad) - 20} more")
        return 1
    if not OUT.exists():
        print(f"FAIL: {OUT.relative_to(ROOT)} is missing — run the tool without --check")
        return 1
    if load(OUT) != doc:
        print(f"FAIL: {OUT.relative_to(ROOT)} no longer matches what the committed "
              f"ledgers re-derive to. Re-run tools/reconcile_locations.py and commit "
              f"the result.")
        return 1
    c = doc["counts"]
    lim = c["business_location_limits"]
    print(f"OK   {OUT.relative_to(ROOT)} re-derives exactly ({c['rows']} row(s); "
          f"business limits {lim['structure']}/{lim['street_only']}/"
          f"{lim['unplaceable']} structure/street-only/unplaceable)")
    return 0


def report(doc: dict) -> int:
    c = doc["counts"]
    print(f"location reconciliation — {c['rows']} claim(s)\n")
    print("by relation:")
    for k in sorted(c["by_relation"]):
        print(f"  {k:<18} {c['by_relation'][k]:>5}")
    print("\nby disposition:")
    for k in sorted(c["by_disposition"]):
        print(f"  {k:<26} {c['by_disposition'][k]:>5}   {DISPOSITIONS[k]}")
    print("\nbusiness location limits (T-1147 ¶9):")
    for k, v in c["business_location_limits"].items():
        print(f"  {k:<14} {v:>5}")
    print("\nhousehold seating classes (T-1147 ¶9):")
    for k in SEATING_CLASSES:
        print(f"  {k:<14} {c['household_seating_classes'][k]:>5}")
    print(f"\n{c['standing_question_rows']} row(s) stand under an open source question.")
    return 0


def self_test() -> int:
    import copy
    failures: list[str] = []

    def fires(what: str, doc: dict, needle: str) -> None:
        if any(needle in line for line in gate(doc)):
            print(f"   self-test | FAIL as designed: {what}")
        else:
            failures.append(what)
            print(f"   self-test | NOT CAUGHT: {what}")

    good = derive()
    problems = gate(good)
    if problems:
        failures.append("the committed ledgers do not pass this table's own gate")
        for line in problems[:10]:
            print(f"   self-test | unexpected: {line}")
    else:
        print("   self-test | ok: the ledgers' own claims pass the gate")

    d = copy.deepcopy(good); d["rows"] = []; d["counts"]["rows"] = 0
    fires("the table goes empty", d, "no location claim at all")

    d = copy.deepcopy(good); d["rows"][0]["disposition"] = "placed_somewhere_nice"
    fires("a disposition outside the vocabulary", d, "not in the declared vocabulary")

    d = copy.deepcopy(good); d["rows"][0]["limit_clause"] = ""
    fires("a claim stops saying what stopped it", d, "no limit clause")

    d = copy.deepcopy(good); d["rows"][0]["ledger"] = None
    fires("a row stops naming who adjudicated it", d, "names no ledger")

    d = copy.deepcopy(good)
    hit = next((r for r in d["rows"] if r["disposition"] == "unplaceable"), None)
    if hit is None:
        failures.append("no unplaceable claim to test the placement refusal")
    else:
        hit["resolved_structure"] = "new_york_house"
        fires("an unplaceable claim is given a building", d, "may not place what its")

    d = copy.deepcopy(good)
    hit = next((r for r in d["rows"] if r["confidence"] is None), None)
    if hit is None:
        failures.append("no ungraded claim to test the silence refusal")
    else:
        hit["confidence_silent_because"] = None
        fires("an ungraded claim stops saying which ledger is silent", d,
              "does not say which ledger")

    d = copy.deepcopy(good)
    hit = next((r for r in d["rows"] if r["confidence"] is not None), None)
    if hit is None:
        failures.append("no graded claim to test the provenance refusal")
    else:
        hit["confidence_from"] = None
        fires("a grade stops saying where it was read", d, "does not say where")

    d = copy.deepcopy(good)
    d["counts"]["household_seating_classes"]["none"] += 1
    fires("a household is counted twice in the seating classes", d,
          "do not cover every household")

    d = copy.deepcopy(good)
    hit = next((r for r in d["rows"] if r["relation"] == "premises"
                and r["disposition"] == "unplaceable"), None)
    if hit is None:
        failures.append("no unplaceable business to test the location-limit invariant")
    else:
        hit["disposition"] = "placed_structure"
        hit["resolved_structure"] = "new_york_house"
        fires("a business is quietly promoted out of the 123 location limits", d,
              "no longer count the rows")

    d = copy.deepcopy(good); d["rows"].append(copy.deepcopy(d["rows"][0]))
    d["counts"]["rows"] += 1
    fires("one claim is written twice", d, "appears twice")

    if failures:
        print("SELF-TEST FAILED: " + "; ".join(failures))
        return 1
    print("self-test ok")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff against the committed table")
    ap.add_argument("--report", action="store_true", help="the location axis, to stdout")
    ap.add_argument("--self-test", action="store_true",
                    help="prove this tool's own refusals fire")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    doc = derive()
    if args.check:
        return check(doc)
    if args.report:
        return report(doc)
    write(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
