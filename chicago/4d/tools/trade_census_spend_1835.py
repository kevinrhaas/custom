#!/usr/bin/env python3
"""SPENDING THE TRADE-CENSUS GAP: the institutions, the documented absences, and the
names the register never held.

T-1006 set the December 1835 State count against the town's business register and
left a shortfall it was forbidden to spend: four druggists against two, two
silversmiths against one, two breweries against one, twenty-two lawyers against
nineteen RECORDS, fourteen physicians against four, and three lines the town held
nothing at all for — lottery office, bank, lyceum and reading room.

T-1007 spends it, and the spend is almost entirely a matter of counting the right
thing.  The census counts PRACTITIONERS; the register counts NOTICES.  Nineteen
lawyer records are fourteen named men.  Four physician records are three names and
one anonymous practitioner — while five more physicians sit on resident cards,
attested, present at the scene date, and invisible to a register compiled from
advertisements, because a doctor with a practice does not advertise it.

    tools/trade_census_spend_1835.py --build       write the spend record
    tools/trade_census_spend_1835.py --check       re-derive it and refuse any drift
    tools/trade_census_spend_1835.py --self-test   the guards, fired on fixtures

THE ONE GUARD THAT MATTERS IS G9.  Every name this file counts already stood in the
repository — on a business record or on a resident card — before the ruling was
written.  This tool cannot mint a person, a business or a roof: a ruling row that
names neither a `business_id` the register holds nor a `person_id` the town cards
hold is a Fault, and that is the mechanical form of T-1007's fourth acceptance.
Where the sources do not fill a census line the residual is reported as a MEASURED
GAP and spent on nothing; the ceiling on such a gap is anonymous stock under the
owner's ruling of 2026-09-02, and never an invented person.

AND AN INSTITUTION IS NOT A BUILDING (G5).  The Lyceum and the Chicago Reading Room
are recorded here as associations — instituted, officered, meeting somewhere — with
`premises: null` and a documented negative saying why.  A ruling that gave either of
them a structure would be refused.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULINGS = ROOT / "data" / "research" / "books" / "trade_census_1835_spend_rulings.json"
CROSSWALK = ROOT / "data" / "research" / "books" / "trade_census_1835_crosswalk.json"
REGISTER = ROOT / "data" / "research" / "newspapers" / "register_1835.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
STRUCTURES = ROOT / "data" / "structures"
EXTRACTED = ROOT / "data" / "research" / "newspapers" / "extracted"
CLAIM_DIRS = (
    ROOT / "data" / "research" / "books" / "claims",
    ROOT / "data" / "research" / "directories" / "claims",
)
SPEND = ROOT / "data" / "research" / "books" / "trade_census_1835_spend.json"

CLAIM = "bk_mose1_006"
SOURCE = "moses_kirkland_history_of_chicago_v1"
SCENE_DATE = "1835-07-01"
CENSUS_WINDOW = "1835-09-01/1835-12-31"
DATE_CAUTION = (
    "THE COUNT IS NOT OF THE SCENE. It was taken between 1 September and December 1835; "
    "the scene is 1 July 1835. A residual below is a MEASURED GAP and never a hole to "
    "fill: a physician who came in September is in the December count and was never in "
    "the July town."
)
ISSUE_CITE = re.compile(r"^([a-z0-9_]+)#(c\d+)$")


class Fault(Exception):
    """A defect in the rulings, phrased for the person who must fix it."""


# ---------------------------------------------------------------------------
# what the town already holds — the only names a ruling may spend


def town_people() -> dict:
    people = {}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        hh = json.loads(path.read_text(encoding="utf-8"))
        for person in hh.get("persons", []):
            people[person["id"]] = {
                "name": person.get("name"),
                "household_id": hh["id"],
                "occupation": (person.get("occupation") or {}).get("value"),
                "grade": person.get("grade"),
                "present_on_scene_date": (hh.get("present_on_scene_date") or {}).get("value"),
            }
    return people


def town_businesses() -> dict:
    reg = json.loads(REGISTER.read_text(encoding="utf-8"))
    return {b["id"]: b for b in reg["businesses"]}


def town_structures() -> set:
    return {p.stem for p in STRUCTURES.glob("*.json")}


def town_claims() -> set:
    ids = set()
    for directory in CLAIM_DIRS:
        for path in sorted(directory.glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            for claim in (doc.get("claims") or []):
                ids.add(claim["id"])
    return ids


def issue_claim_exists(cite: str) -> bool:
    match = ISSUE_CITE.match(cite)
    if not match:
        return False
    path = EXTRACTED / f"{match.group(1)}.json"
    if not path.exists():
        return False
    doc = json.loads(path.read_text(encoding="utf-8"))
    return any(c["id"] == match.group(2) for c in doc.get("claims", []))


# ---------------------------------------------------------------------------
# the guards


def check_sources(where: str, sources, claims: set, seen: dict) -> None:
    for cite in (sources or []):
        if cite in seen:
            ok = seen[cite]
        else:
            ok = cite in claims or issue_claim_exists(cite)
            seen[cite] = ok
        if not ok:
            raise Fault(
                f"G4 {where} cites `{cite}`, and no claim of that id is held. A citation "
                f"this repository cannot resolve is an invented citation — either the "
                f"reading was never landed or the id is mistyped.")


def check_name(where: str, row: dict, people: dict, businesses: dict) -> None:
    """G9 — the guard that makes 'nothing is invented' mechanical rather than hoped for."""
    pid, bid = row.get("person_id"), row.get("business_id")
    if not pid and not bid:
        raise Fault(
            f"G9 {where} names `{row.get('name')}` and gives neither a person_id the town "
            f"cards hold nor a business_id the register holds. THIS FILE MAY NOT MINT A "
            f"NAME: a census line the sources do not fill is a measured gap, not a person.")
    if pid and pid not in people:
        raise Fault(f"G1 {where} cites person `{pid}`, and no card in "
                    f"data/residents/households/ holds that id.")
    if bid and bid not in businesses:
        raise Fault(f"G2 {where} cites business `{bid}`, and the register does not hold it.")
    if bid and not businesses[bid]["present_at_scene_date"]:
        raise Fault(f"G2 {where} counts business `{bid}`, which the register dates out of "
                    f"the scene. A house the register excludes may not be counted into the "
                    f"town by this file.")


def check_institution(inst: dict, people: dict, businesses: dict, structures: set,
                      claims: set, seen: dict) -> dict:
    where = f"institution `{inst['id']}`"
    premises = inst.get("premises") or {}
    if premises.get("value") is not None:
        raise Fault(
            f"G5 {where} carries premises `{premises.get('value')}`. AN INSTITUTION IS NOT "
            f"A BUILDING (S6): the Lyceum and the Reading Room are recorded because the "
            f"corpus documents that neither had a room of its own at the scene date, and a "
            f"structure here would be the reconstruction asserting the opposite.")
    if not (premises.get("note") or "").strip():
        raise Fault(f"G5 {where} has no premises note. A documented negative that does not "
                    f"say what documents it is a gap wearing a confidence.")
    check_sources(f"{where} premises", premises.get("sources"), claims, seen)
    check_sources(f"{where} instituted", (inst.get("instituted") or {}).get("sources"),
                  claims, seen)
    links = []
    for link in inst.get("links", []):
        lwhere = f"{where} link `{link['kind']}`"
        check_sources(lwhere, link.get("sources"), claims, seen)
        if not link.get("sources"):
            raise Fault(f"G4 {lwhere} cites no source. A link between an institution and a "
                        f"townsman is a claim and carries its printing.")
        sid = link.get("structure_id")
        if sid and sid not in structures:
            raise Fault(f"G3 {lwhere} cites structure `{sid}`, which data/structures/ does "
                        f"not hold.")
        pid = link.get("person_id")
        if pid and pid not in people:
            raise Fault(f"G1 {lwhere} cites person `{pid}`, which no resident card holds.")
        bid = link.get("business_id")
        if bid and bid not in businesses:
            raise Fault(f"G2 {lwhere} cites business `{bid}`, which the register does not "
                        f"hold.")
        resolved = dict(link)
        if pid:
            resolved["person_name"] = people[pid]["name"]
            resolved["person_household"] = people[pid]["household_id"]
        if bid:
            resolved["business_name"] = businesses[bid]["name"]
        if sid:
            resolved["structure_exists"] = True
        links.append(resolved)
    out = dict(inst)
    out["links"] = links
    out["has_premises"] = False
    return out


def check_absence(row: dict, classes: dict, claims: set, seen: dict) -> dict:
    where = f"documented absence `{row['class']}`"
    check_sources(where, row.get("sources"), claims, seen)
    if not row.get("sources"):
        raise Fault(f"G8 {where} cites nothing. An absence recorded without the notice that "
                    f"records it is indistinguishable from a hole in the reading.")
    if not (row.get("what_would_overturn_it") or "").strip():
        raise Fault(f"G8 {where} does not say what would overturn it. An absence nobody can "
                    f"argue with is a wall, not a finding.")
    cls = classes.get(row["class"])
    if cls is None:
        raise Fault(f"G6 {where} names a class the December 1835 crosswalk does not count.")
    if cls["town_records_in_town"] != 0:
        raise Fault(
            f"G8 {where} is recorded as an absence, and the crosswalk now counts "
            f"{cls['town_records_in_town']} record(s) for it. The town has GAINED the thing "
            f"this file says it does not have — re-rule the absence rather than re-run this.")
    out = dict(row)
    out["town_records_in_town"] = 0
    out["census_line"] = cls["census_line"]
    return out


def check_shortfall(row: dict, classes: dict, people: dict, businesses: dict,
                    claims: set, seen: dict) -> dict:
    where = f"shortfall ruling `{row['class']}`"
    cls = classes.get(row["class"])
    if cls is None:
        raise Fault(f"G6 {where} names a class the December 1835 crosswalk does not count.")
    if cls["census_count"] != row["census_count"]:
        raise Fault(
            f"G7 {where} was ruled against a census count of {row['census_count']} and the "
            f"crosswalk now reads {cls['census_count']}. The denominator moved under the "
            f"ruling — read `bk_mose1_006` again before touching the arithmetic.")
    if cls["town_records_at_scene_date"] != row["register_records_at_scene_date"]:
        raise Fault(
            f"G7 {where} was ruled against {row['register_records_at_scene_date']} register "
            f"record(s) at the scene date and the crosswalk now counts "
            f"{cls['town_records_at_scene_date']}. A notice was extracted or re-classed "
            f"since the ruling: re-rule it, do not re-derive around it.")
    named, seen_ids = [], set()
    for bucket in ("named_by_register", "named_by_card"):
        for entry in row.get(bucket, []):
            check_name(f"{where} {bucket}", entry, people, businesses)
            check_sources(f"{where} {bucket}", entry.get("sources"), claims, seen)
            key = entry.get("person_id") or entry.get("business_id")
            if key in seen_ids:
                raise Fault(f"G1 {where} counts `{key}` twice. Under S1 a person is counted "
                            f"once, and a double count closes a census line with a ghost.")
            seen_ids.add(key)
            resolved = dict(entry)
            resolved["from"] = "register" if bucket == "named_by_register" else "resident_card"
            if entry.get("person_id"):
                card = people[entry["person_id"]]
                resolved["card_occupation"] = card["occupation"]
                resolved["card_grade"] = card["grade"]
                resolved["card_present_on_scene_date"] = card["present_on_scene_date"]
            named.append(resolved)
    for entry in row.get("documented_but_unnamed", []):
        check_name(f"{where} documented_but_unnamed", entry, people, businesses)
    for entry in row.get("counted_beside_and_not_within", []):
        check_name(f"{where} counted_beside_and_not_within", entry, people, businesses)
        if not (entry.get("note") or "").strip():
            raise Fault(f"G3 {where} names `{entry.get('name')}` beside the count and does "
                        f"not say why it is not in it. A name set aside in silence is a "
                        f"count nobody can check.")
    count = len(named)
    if count > row["census_count"]:
        raise Fault(
            f"G7 {where} counts {count} named against a census line of {row['census_count']}. "
            f"A spend that runs PAST its denominator has stopped being a reconciliation — "
            f"either a name is double-counted or the class boundary is wrong.")
    residual = row["census_count"] - count
    if residual != row["residual"]:
        raise Fault(
            f"G7 {where} states a residual of {row['residual']} and its own rows leave "
            f"{residual} ({row['census_count']} counted less {count} named). The arithmetic "
            f"in the prose must be the arithmetic in the rows.")
    if residual and row.get("residual_verdict") != "measured_gap":
        raise Fault(f"G7 {where} leaves {residual} unaccounted for and does not call it a "
                    f"measured_gap. Under S3 that is the only verdict available: the "
                    f"alternative is inventing somebody.")
    if not (row.get("spend") or "").strip():
        raise Fault(f"G6 {where} says nothing about what it spent. A ruling that reports a "
                    f"number and no reasoning cannot be disagreed with.")
    if row.get("stands_on_liberty") and row["stands_on_liberty"] != "T-0404":
        raise Fault(f"G6 {where} stands on a liberty other than T-0404, which is the only "
                    f"one this ticket was given.")
    return {
        "class": row["class"],
        "census_line": cls["census_line"],
        "unit": row["unit"],
        "census_count": row["census_count"],
        "register_records_at_scene_date": row["register_records_at_scene_date"],
        "named_after_the_spend": count,
        "delta_before": cls["delta"],
        "delta_after": count - row["census_count"],
        "named": named,
        "documented_but_unnamed": row.get("documented_but_unnamed", []),
        "counted_beside_and_not_within": row.get("counted_beside_and_not_within", []),
        "spend": row["spend"],
        "corroboration": row.get("corroboration"),
        "residual": residual,
        "residual_verdict": row["residual_verdict"],
        "residual_note": row["residual_note"],
        "stands_on_liberty": row.get("stands_on_liberty"),
        "handed_on": row.get("handed_on"),
    }


# ---------------------------------------------------------------------------
# the build


def build(rulings: dict, crosswalk: dict, people: dict, businesses: dict,
          structures: set, claims: set) -> dict:
    seen: dict = {}
    classes = {c["class"]: c for c in crosswalk["classes"]}
    institutions = [check_institution(i, people, businesses, structures, claims, seen)
                    for i in rulings["institutions"]]
    absences = [check_absence(a, classes, claims, seen)
                for a in rulings["documented_absences"]]
    shortfalls = [check_shortfall(s, classes, people, businesses, claims, seen)
                  for s in rulings["shortfall_rulings"]]

    # G6 — no shortfall the crosswalk sees is left unaddressed, in silence
    ruled = {s["class"] for s in shortfalls} | {a["class"] for a in absences}
    ruled |= {"lyceum_and_reading_room"} if institutions else set()
    short = {c["class"] for c in crosswalk["classes"]
             if c.get("delta") is not None and c["delta"] < 0}
    missing = sorted(short - ruled)
    if missing:
        raise Fault(
            f"G6 the crosswalk is short on {', '.join(missing)} and this file rules on "
            f"none of them. A shortfall that goes unruled is exactly what T-1007 exists to "
            f"end — rule it, or record it as a documented absence, but do not pass it in "
            f"silence.")
    over = sorted(ruled - short - {"lyceum_and_reading_room"})
    if over:
        raise Fault(
            f"G6 this file rules on {', '.join(over)}, which the crosswalk is no longer "
            f"short on. The town has caught the census up since the ruling was written: "
            f"withdraw the row rather than leaving a spend on a line that needs none.")

    named_total = sum(s["named_after_the_spend"] for s in shortfalls)
    register_total = sum(s["register_records_at_scene_date"] for s in shortfalls)
    return {
        "schema": 1,
        "domain": "books",
        "source_id": SOURCE,
        "claim_id": CLAIM,
        "generated_by": "tools/trade_census_spend_1835.py --build",
        "ticket": "T-1007",
        "not_a_reading": rulings["not_a_reading"],
        "_doc": __doc__.strip(),
        "scene_date": SCENE_DATE,
        "census_window": CENSUS_WINDOW,
        "date_caution": DATE_CAUTION,
        "liberty": rulings["liberty"],
        "boundaries": rulings["boundaries"],
        "creates_nothing": (
            "NO PERSON, BUSINESS OR STRUCTURE WAS CREATED BY THIS SPEND, and guard G9 is why "
            "that is checkable rather than promised: every name counted below resolves to a "
            "record data/research/newspapers/register_1835.json or data/residents/households/ "
            "already held. The two institutions gain no premises (G5). The residuals are "
            "reported and spent on nothing."),
        "institutions": institutions,
        "documented_absences": absences,
        "shortfall": shortfalls,
        "totals": {
            "classes_ruled": len(shortfalls),
            "register_records_at_scene_date": register_total,
            "named_after_the_spend": named_total,
            "names_the_register_never_held": sum(
                1 for s in shortfalls for n in s["named"] if n["from"] == "resident_card"),
            "residual_after_the_spend": sum(s["residual"] for s in shortfalls),
            "institutions_recorded": len(institutions),
            "institutions_given_premises": 0,
            "documented_absences": len(absences),
        },
    }


# ---------------------------------------------------------------------------
# the commands


def render(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def load() -> tuple:
    return (json.loads(RULINGS.read_text(encoding="utf-8")),
            json.loads(CROSSWALK.read_text(encoding="utf-8")),
            town_people(), town_businesses(), town_structures(), town_claims())


def report(doc: dict) -> str:
    out = ["", "class                     census   register   named   residual", "-" * 60]
    for s in doc["shortfall"]:
        out.append(f"{s['class']:<26}{s['census_count']:>6}{s['register_records_at_scene_date']:>11}"
                   f"{s['named_after_the_spend']:>8}{s['residual']:>11}")
    out.append("-" * 60)
    t = doc["totals"]
    out.append(f"{t['names_the_register_never_held']} named practitioners the register never "
               f"held are now counted; {t['residual_after_the_spend']} of the census's people "
               f"remain a measured gap and nothing is created for them.")
    for inst in doc["institutions"]:
        links = ", ".join(f"{l['kind']}→{l.get('person_id') or l.get('structure_id') or l.get('business_id')}"
                          for l in inst["links"])
        out.append(f"institution {inst['id']}: no premises; {links or 'no links'}")
    for a in doc["documented_absences"]:
        out.append(f"documented absence: {a['class']} — {a['census_line']}")
    out.append("\n" + doc["date_caution"])
    return "\n".join(out)


def cmd_build() -> int:
    doc = build(*load())
    SPEND.write_text(render(doc), encoding="utf-8")
    print(f"wrote {SPEND.relative_to(ROOT)}")
    print(report(doc))
    return 0


def cmd_check() -> int:
    if not SPEND.exists():
        print(f"FAIL: {SPEND.relative_to(ROOT)} does not exist — run --build", file=sys.stderr)
        return 1
    fresh = render(build(*load()))
    if fresh != SPEND.read_text(encoding="utf-8"):
        print(f"FAIL: {SPEND.relative_to(ROOT)} no longer re-derives from the rulings, the "
              "register and the resident cards. Run tools/trade_census_spend_1835.py --build "
              "and read the diff — a changed count means a name moved, a card was merged, or "
              "the December denominator was re-read.", file=sys.stderr)
        return 1
    t = json.loads(fresh)["totals"]
    print(f"the trade-census spend re-derives: {t['named_after_the_spend']} named across "
          f"{t['classes_ruled']} short classes, {t['institutions_recorded']} institutions "
          f"with {t['institutions_given_premises']} premises between them, "
          f"{t['residual_after_the_spend']} left as a measured gap")
    return 0


# ---------------------------------------------------------------------------
# the self-test: every guard above, fired


def _fixture() -> tuple:
    rulings = {
        "not_a_reading": "a fixture",
        "liberty": {"id": "T-0404", "note": "n"},
        "boundaries": {"S1": "one"},
        "institutions": [{
            "id": "institution_x", "name": "X", "kind": "k",
            "instituted": {"value": None, "confidence": "inferred", "sources": [], "note": "n"},
            "premises": {"value": None, "confidence": "documented",
                         "sources": [], "note": "documented negative"},
            "links": [{"kind": "officer", "person_id": "p1", "business_id": None,
                       "structure_id": "s1", "sources": ["bk_x_001"], "note": "n"}],
        }],
        "documented_absences": [{
            "class": "bank", "census_count": 1, "verdict": "documented_absence",
            "sources": ["bk_x_001"], "note": "n",
            "what_would_overturn_it": "a notice",
        }],
        "shortfall_rulings": [{
            "class": "druggist", "unit": "business_record", "census_count": 4,
            "register_records_at_scene_date": 2,
            "named_by_register": [{"person_id": None, "business_id": "b1", "name": "A"},
                                  {"person_id": None, "business_id": "b2", "name": "B"}],
            "named_by_card": [{"person_id": "p1", "business_id": None, "name": "C"}],
            "documented_but_unnamed": [], "counted_beside_and_not_within": [],
            "spend": "three, not two", "residual": 1,
            "residual_verdict": "measured_gap", "residual_note": "one short",
        }],
    }
    crosswalk = {"classes": [
        {"class": "druggist", "census_line": "four druggists", "census_count": 4,
         "compared": True, "town_records_in_town": 2, "town_records_at_scene_date": 2,
         "delta": -2},
        {"class": "bank", "census_line": "one bank", "census_count": 1, "compared": True,
         "town_records_in_town": 0, "town_records_at_scene_date": 0, "delta": -1},
    ]}
    people = {"p1": {"name": "C", "household_id": "hh_c", "occupation": "druggist",
                     "grade": "attested", "present_on_scene_date": "present"}}
    businesses = {"b1": {"id": "b1", "name": "A", "present_at_scene_date": True},
                  "b2": {"id": "b2", "name": "B", "present_at_scene_date": True}}
    return rulings, crosswalk, people, businesses, {"s1"}, {"bk_x_001"}


def _fires(args, fragment: str) -> None:
    try:
        build(*args)
    except Fault as exc:
        assert fragment in str(exc), f"wrong fault for {fragment!r}: {exc}"
        return
    raise AssertionError(f"no fault raised where one was due: {fragment}")


def cmd_self_test() -> int:
    import copy

    args = _fixture()
    doc = build(*args)
    assert doc["totals"]["named_after_the_spend"] == 3, doc["totals"]
    assert doc["totals"]["names_the_register_never_held"] == 1, doc["totals"]
    assert doc["totals"]["institutions_given_premises"] == 0

    # G9 — the guard that makes 'nothing is invented' mechanical
    a = copy.deepcopy(args)
    a[0]["shortfall_rulings"][0]["named_by_card"].append({"person_id": None,
                                                          "business_id": None, "name": "Ghost"})
    a[0]["shortfall_rulings"][0]["residual"] = 0
    _fires(a, "MAY NOT MINT A NAME")

    # G1 — a person the cards do not hold
    a = copy.deepcopy(args)
    a[0]["shortfall_rulings"][0]["named_by_card"][0]["person_id"] = "p9"
    _fires(a, "no card in")

    # G2 — a business the register does not hold, and one it dates out of the scene
    a = copy.deepcopy(args)
    a[0]["shortfall_rulings"][0]["named_by_register"][0]["business_id"] = "b9"
    _fires(a, "the register does not hold it")
    a = copy.deepcopy(args)
    a[3]["b1"]["present_at_scene_date"] = False
    _fires(a, "dates out of the scene")

    # G1 — one man counted twice closes a line with a ghost
    a = copy.deepcopy(args)
    a[0]["shortfall_rulings"][0]["named_by_card"].append(
        {"person_id": "p1", "business_id": None, "name": "C again"})
    a[0]["shortfall_rulings"][0]["residual"] = 0
    _fires(a, "counts `p1` twice")

    # G3 — a structure data/structures does not hold
    a = copy.deepcopy(args)
    a[0]["institutions"][0]["links"][0]["structure_id"] = "s9"
    _fires(a, "which data/structures/ does not hold")

    # G4 — an unresolvable citation is an invented citation
    a = copy.deepcopy(args)
    a[0]["institutions"][0]["links"][0]["sources"] = ["bk_nope_001"]
    _fires(a, "invented citation")

    # G5 — AN INSTITUTION IS NOT A BUILDING
    a = copy.deepcopy(args)
    a[0]["institutions"][0]["premises"]["value"] = "some_hall"
    _fires(a, "AN INSTITUTION IS NOT A BUILDING")

    # G6 — a shortfall the crosswalk sees and this file passes over in silence
    a = copy.deepcopy(args)
    a[1]["classes"].append({"class": "brewery", "census_line": "two breweries",
                            "census_count": 2, "compared": True, "town_records_in_town": 1,
                            "town_records_at_scene_date": 1, "delta": -1})
    _fires(a, "short on brewery")

    # G6 — a spend left standing on a line the town has since caught up
    a = copy.deepcopy(args)
    a[1]["classes"][0]["delta"] = 0
    _fires(a, "no longer short on")

    # G7 — the denominator moved under the ruling
    a = copy.deepcopy(args)
    a[1]["classes"][0]["census_count"] = 5
    _fires(a, "denominator moved under the ruling")

    # G7 — the register moved under the ruling
    a = copy.deepcopy(args)
    a[1]["classes"][0]["town_records_at_scene_date"] = 3
    _fires(a, "re-rule it, do not re-derive around it")

    # G7 — the prose arithmetic and the row arithmetic must agree
    a = copy.deepcopy(args)
    a[0]["shortfall_rulings"][0]["residual"] = 2
    _fires(a, "arithmetic in the prose")

    # G7 — a spend that runs past its denominator
    a = copy.deepcopy(args)
    a[1]["classes"][0]["census_count"] = 2
    a[0]["shortfall_rulings"][0]["census_count"] = 2
    _fires(a, "runs PAST its denominator")

    # G7 — a residual that refuses to call itself a gap
    a = copy.deepcopy(args)
    a[0]["shortfall_rulings"][0]["residual_verdict"] = "filled"
    _fires(a, "the only verdict available")

    # G8 — an absence the town has since gained the thing for
    a = copy.deepcopy(args)
    a[1]["classes"][1]["town_records_in_town"] = 1
    _fires(a, "has GAINED the thing")

    # G8 — an absence nobody can argue with
    a = copy.deepcopy(args)
    a[0]["documented_absences"][0]["what_would_overturn_it"] = " "
    _fires(a, "is a wall, not a finding")

    print("trade_census_spend_1835 self-tests pass (17 guards)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    try:
        if args.build:
            return cmd_build()
        if args.check:
            return cmd_check()
        if args.self_test:
            return cmd_self_test()
    except Fault as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(report(build(*load())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
