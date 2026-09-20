#!/usr/bin/env python3
"""The address book: where every known household and firm stands, at the rung its
evidence reaches — and, where the evidence does not reach a seat, what it DOES reach
and who owes the seat.

    tools/seat_known_1835.py --build      write the address book
    tools/seat_known_1835.py --check      re-derive, diff, re-assert every limit
    tools/seat_known_1835.py --self-test  break the assertions and require them to fire
    tools/seat_known_1835.py --report     print the counts

WHAT THIS IS FOR.

T-1198 asked for one row per household and per business, each seated at the first rung
of a six-rung ladder that fires:

    1  structure       a named roof
    2  lot             an address, a corner ordinal, a lot-and-block line
    3  face            a street and nothing narrower, housed on a block face
    4  division_band   a division from the evidence, banded by the placement policy
    5  policy_only     nothing in the evidence; the policy's band by class alone
    6  unplaceable     the evidence CONTRADICTS every band

It is three runs of work, not one, so it was split (T-1491/T-1492/T-1493). **This
ticket is the first piece and it writes only the rungs the committed evidence already
reaches.** Rungs 4 and 5 are reconstruction — they deal a band to a household no source
places — and dealing them here, in the same pass that reads the evidence, is exactly how
a reconstructed band comes to look like a reading. So this pass seats rungs 1, 3 and 6,
records rung 2 as **measured empty**, and for every other row writes down the REACH —
the narrowest thing the evidence actually gives — with `seat: null` and the ticket that
owes the seat. No coordinate is invented here, and the file says so about itself.

THE ONE THING THIS FILE IS NOT.

It is not a second opinion on anything already adjudicated. The business half is a
strict restatement of `data/research/location_spend.json` (T-1239): assertion 4 fails if
a single firm's rung stops agreeing with the grade that file gives it, and assertion 5
fails if the 62 unplaceable firms are not the same 62. The household half is read from
the committed household records and from nothing else — `lives_at` is the seat, and a
household whose record names no roof gets no roof here.

WHAT A ROW SAYS, AND WHY EACH FIELD IS THERE.

    rung          the rung that fired: structure | lot | face | unplaceable | owed
    seat          the thing it stands on, or null. NEVER set on an `owed` row.
    reach         what the evidence narrows to: structure | structure_owed | lot |
                  face | division | none
    reach_value   the street or the division the reach names, where it names one
    tier          the confidence the seat carries, from the record that made it
    basis         the clause or rule the seat rests on, in the words of its own source
    words         the sentence the household card shows a visitor
    replaceable_by  what would move this row UP the ladder
    owed_to       the ticket that owes the seat, on an `owed` row

`words` is the point of the whole file. Before it, 1,186 household cards said "No known
address" and stopped, which reads as an absence in the town rather than an absence in the
record. A visitor is owed the difference between "nobody wrote down where they lived",
"the paper names their street and no more" and "the evidence puts them outside the town",
and those are three different sentences.

THE RUNG-2 CLAIM IS MEASURED, NOT ASSUMED.

`data/research/newspapers/lot_addresses.json` is the whole of this project's lot-and-block
evidence and it carries ONE address — G. Spring's dwelling-house on lot 7 of block 16 —
which names no household and no firm. So rung 2 stands empty, and assertion 7 re-reads the
ledger on every run: the day a second lot address arrives naming somebody, the gate fails
here rather than the rung quietly staying empty.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HOUSEHOLDS = ROOT / "data" / "residents" / "households"
INDEX = ROOT / "data" / "residents" / "index.json"
SPEND = ROOT / "data" / "research" / "location_spend.json"
LOT_ADDRESSES = ROOT / "data" / "research" / "newspapers" / "lot_addresses.json"
BUSINESSES = ROOT / "data" / "businesses"
STRUCTURES = ROOT / "data" / "structures"

OUT = ROOT / "data" / "reconstruction" / "1835_address_book.json"

SCENE_DATE = "1835-07-01"
TICKET = "T-1491"

# Who owes the seat a row does not have. The reconstructed rungs are T-1492's; a roof
# the paper reaches but the town has not raised is owed to the district build tickets.
OWED_RECONSTRUCTED = "T-1492"
OWED_BUILD = "T-1200..T-1209"

# The business grade -> (rung, reach, owed_to). A strict restatement of T-1239's
# adjudication; assertion 4 refuses any drift between this table and that file.
FROM_GRADE = {
    "structure_committed": ("structure", "structure", None),
    "structure_pending": ("owed", "structure_owed", OWED_BUILD),
    "street_only_adopted": ("face", "face", None),
    "street_only_unseated": ("owed", "face", OWED_RECONSTRUCTED),
    "unplaceable": ("unplaceable", "none", None),
}

# The divisions the town holds. `outside_town` is rung 6 and not a band: the evidence
# does not fail to place these households, it places them somewhere else.
TOWN_DIVISIONS = ("south", "west", "north", "fort")


class Refused(Exception):
    """A limit this file may not cross."""


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def committed_structures() -> set[str]:
    return {p.stem for p in sorted(STRUCTURES.glob("*.json"))}


def household_records() -> list[dict]:
    return [read_json(p) for p in sorted(HOUSEHOLDS.glob("*.json"))]


def business_names() -> dict[str, str]:
    """register_id -> the firm's name, for the rows the spend adjudicates."""
    names = {}
    for path in sorted(BUSINESSES.glob("*.json")):
        rec = read_json(path)
        if rec.get("register_id"):
            names[rec["register_id"]] = rec.get("name") or rec["id"]
    return names


# ---- the household half ---------------------------------------------------- #


def household_row(hh: dict, committed: set[str]) -> dict:
    """One household, seated at the first rung that fires.

    Only rung 1 can fire on the evidence this project holds today: `lives_at` is the
    only field that names a roof, and the lot ledger names no household. Everything
    else records its reach and names the ticket that owes it a seat.
    """
    lives = hh.get("lives_at") or {}
    works = hh.get("works_at") or {}
    seat_id = lives.get("value")
    works_id = works.get("value")
    division = hh.get("division") or "unplaced"
    basis = lives.get("basis") or {}
    row = {
        "id": hh["id"],
        "kind": "household",
        "name": hh.get("name") or hh["id"],
        "rung": None,
        "seat": None,
        "works_seat": ({"kind": "structure", "id": works_id}
                       if works_id and works_id in committed else None),
        "reach": None,
        "reach_value": None,
        "division": division,
        "tier": None,
        "basis": None,
        "words": None,
        "replaceable_by": None,
        "owed_to": None,
    }
    if seat_id:
        row["rung"] = "structure"
        row["seat"] = {"kind": "structure", "id": seat_id}
        row["reach"] = "structure"
        row["tier"] = lives.get("tier") or lives.get("confidence")
        row["basis"] = basis.get("note") or lives.get("note")
        row["words"] = (f"Seated at a named roof — the strongest rung this ladder has. "
                        f"The household record carries the seat at {row['tier']}.")
        rb = lives.get("replaceable_by") or {}
        row["replaceable_by"] = rb.get("match") or "a source naming a different building"
        return row
    if division == "outside_town":
        row["rung"] = "unplaceable"
        row["reach"] = "none"
        row["words"] = ("The evidence puts this household OUTSIDE the town, so no seat "
                        "inside it will be dealt for them. This is a placement, not a gap.")
        row["replaceable_by"] = "a source placing this household inside the town"
        return row
    row["rung"] = "owed"
    row["owed_to"] = OWED_RECONSTRUCTED
    if division in TOWN_DIVISIONS:
        row["reach"] = "division"
        row["reach_value"] = division
        row["words"] = (f"The evidence reaches the {division} division and nothing "
                        f"narrower. A band inside it is owed to {OWED_RECONSTRUCTED}; "
                        "until that is dealt, no ground here is this household's.")
        row["replaceable_by"] = ("a source naming a street, a corner or a building for "
                                 "this household")
        return row
    row["reach"] = "none"
    row["words"] = ("No source places this household anywhere in the town — the record "
                    "gives a name and no address. Where it stood is owed to the "
                    f"placement policy ({OWED_RECONSTRUCTED}) and is not guessed here.")
    row["replaceable_by"] = "any source that places this household in a division or nearer"
    return row


# ---- the business half ----------------------------------------------------- #


def business_row(placement: dict, names: dict[str, str]) -> dict:
    grade = placement["grade"]
    if grade not in FROM_GRADE:
        raise Refused(f"{placement['business_id']}: unknown adjudicated grade {grade!r}")
    rung, reach, owed = FROM_GRADE[grade]
    seat = ({"kind": "structure", "id": placement["model_seat"]}
            if rung in ("structure", "face") and placement.get("model_seat") else None)
    street = placement.get("evidence_street")
    if grade == "structure_committed":
        words = ("The advertisement's anchor reaches a roof this town has built, and the "
                 "firm is seated on it.")
    elif grade == "structure_pending":
        words = ("The advertisement's anchor reaches a roof the town has NOT built yet. "
                 f"The seat waits on the district build tickets ({OWED_BUILD}); the "
                 "evidence is good enough for a roof and the roof is not there.")
    elif grade == "street_only_adopted":
        words = (f"The paper reaches {street} and nothing narrower. The street-face "
                 "adoption houses this firm on that face, which is housing and not a "
                 "reading: substitutable, no lot, no anchor.")
    elif grade == "street_only_unseated":
        words = (f"The paper reaches {street} and nothing narrower, and no face could be "
                 f"adopted — every roof on it is spoken for. A face is owed to "
                 f"{OWED_RECONSTRUCTED}.")
    else:
        words = ("The paper reaches no ground this model holds. This firm stays in the "
                 "register, unplaced, with its printed reason — and it is not moved by "
                 "any rule of the placement policy.")
    return {
        "id": placement["business_id"],
        "kind": "business",
        "name": names.get(placement["business_id"], placement["business_id"]),
        "rung": rung,
        "seat": seat,
        "works_seat": None,
        "reach": reach,
        "reach_value": street,
        "division": None,
        "tier": "inferred" if rung in ("structure", "face") else None,
        "basis": placement.get("clause"),
        "words": words,
        "replaceable_by": ("a printing that names a lot, a corner ordinal or a building "
                           "for this firm"),
        "owed_to": owed,
        "seat_is_substitutable": bool(placement.get("seat_is_substitutable")),
        "adjudicated_grade": grade,
    }


# ---- the file -------------------------------------------------------------- #


def build() -> dict:
    committed = committed_structures()
    spend = read_json(SPEND)
    names = business_names()
    rows = [household_row(hh, committed) for hh in household_records()]
    rows += [business_row(p, names) for p in spend["placements"]]

    by_rung: dict[str, int] = {}
    by_reach: dict[str, int] = {}
    for row in rows:
        by_rung[row["rung"]] = by_rung.get(row["rung"], 0) + 1
        by_reach[row["reach"]] = by_reach.get(row["reach"], 0) + 1
    households = [r for r in rows if r["kind"] == "household"]
    businesses = [r for r in rows if r["kind"] == "business"]

    lot_ledger = read_json(LOT_ADDRESSES)
    return {
        "$schema_note": "Derived. Do not hand-edit — tools/seat_known_1835.py --build "
                        "writes it and --check re-derives it.",
        "id": "1835_address_book",
        "ticket": TICKET,
        "parent_ticket": "T-1198",
        "generated_by": "tools/seat_known_1835.py --build",
        "scene_date": SCENE_DATE,
        "not_a_reading": (
            "Only rungs 1, 3 and 6 are seated here, and each restates a seat some other "
            "committed record already made. Rungs 4 and 5 are reconstruction and belong "
            "to " + OWED_RECONSTRUCTED + "; this file records their REACH and leaves "
            "`seat` null. No coordinate is invented by this pass."),
        "inputs": [
            "data/residents/households/",
            "data/research/location_spend.json",
            "data/research/newspapers/lot_addresses.json",
            "data/businesses/",
            "data/structures/",
        ],
        "vocabulary": {
            "rungs": [
                {"rung": "structure", "ladder": 1,
                 "means": "a named roof this town has built"},
                {"rung": "lot", "ladder": 2,
                 "means": "an address, a corner ordinal or a lot-and-block line that "
                          "narrows to the plat's own unit",
                 "stands_empty_because": (
                     "the committed lot-address ledger carries "
                     f"{len(lot_ledger['addresses'])} address(es) and none of them names "
                     "a household or a firm")},
                {"rung": "face", "ladder": 3,
                 "means": "a street and nothing narrower, housed on a block face — "
                          "substitutable, no lot, no anchor"},
                {"rung": "unplaceable", "ladder": 6,
                 "means": "the evidence contradicts every band inside the town"},
                {"rung": "owed", "ladder": None,
                 "means": "the evidence reaches something, and the seat it implies is "
                          "owed to another ticket. `seat` is null and stays null."},
            ],
            "reaches": ["structure", "structure_owed", "face", "division", "none"],
        },
        "counts": {
            "rows": len(rows),
            "households": len(households),
            "businesses": len(businesses),
            "by_rung": dict(sorted(by_rung.items())),
            "by_reach": dict(sorted(by_reach.items())),
            "households_by_rung": dict(sorted(
                {r["rung"]: sum(1 for x in households if x["rung"] == r["rung"])
                 for r in households}.items())),
            "businesses_by_rung": dict(sorted(
                {r["rung"]: sum(1 for x in businesses if x["rung"] == r["rung"])
                 for r in businesses}.items())),
            "seated": sum(1 for r in rows if r["seat"]),
            "owed": sum(1 for r in rows if r["rung"] == "owed"),
        },
        "rows": rows,
    }


def write(doc: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")


def read_committed():
    try:
        return read_json(OUT)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# ---- the limits ------------------------------------------------------------ #


def assertions(doc: dict) -> None:
    rows = doc["rows"]
    committed = committed_structures()
    spend = read_json(SPEND)

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise Refused("a row appears twice — one row per household and per firm")

    households = {r["id"] for r in rows if r["kind"] == "household"}
    on_disk = {p.stem for p in HOUSEHOLDS.glob("*.json")}
    if households != on_disk:
        missing = sorted(on_disk - households)[:3]
        extra = sorted(households - on_disk)[:3]
        raise Refused("the household rows are not the committed households "
                      f"(missing {missing}, extra {extra})")

    firms = {r["id"] for r in rows if r["kind"] == "business"}
    adjudicated = {p["business_id"] for p in spend["placements"]}
    if firms != adjudicated:
        raise Refused("the business rows are not the adjudicated firms of "
                      "data/research/location_spend.json")

    for row in rows:
        if row["seat"] and row["seat"]["id"] not in committed:
            raise Refused(f"{row['id']}: seated on {row['seat']['id']}, which is not a "
                          "committed structure — no seat may be invented here")
        if row["rung"] == "owed" and row["seat"]:
            raise Refused(f"{row['id']}: an owed row carries a seat. The whole point of "
                          "the rung is that it does not.")
        if row["rung"] == "owed" and not row["owed_to"]:
            raise Refused(f"{row['id']}: owed, and it does not say to whom")
        if not row["words"]:
            raise Refused(f"{row['id']}: no words — the card would have nothing to say")
        if not row["replaceable_by"]:
            raise Refused(f"{row['id']}: nothing would move it up the ladder")

    # 4. The business half is a strict restatement of T-1239's adjudication.
    by_id = {r["id"]: r for r in rows if r["kind"] == "business"}
    for placement in spend["placements"]:
        want_rung, want_reach, want_owed = FROM_GRADE[placement["grade"]]
        row = by_id[placement["business_id"]]
        if (row["rung"], row["reach"], row["owed_to"]) != (want_rung, want_reach, want_owed):
            raise Refused(f"{row['id']}: rung {row['rung']!r}/{row['reach']!r} does not "
                          f"restate the adjudicated grade {placement['grade']!r}")
        seat = row["seat"]["id"] if row["seat"] else None
        if seat != (placement["model_seat"] if want_rung in ("structure", "face") else None):
            raise Refused(f"{row['id']}: its seat is not the one the spend adjudicated")

    # 5. The 62 unplaceable firms stay unplaceable.
    unplaceable = {r["id"] for r in rows
                   if r["kind"] == "business" and r["rung"] == "unplaceable"}
    published = {p["business_id"] for p in spend["placements"]
                 if p["grade"] == "unplaceable"}
    if unplaceable != published:
        raise Refused("the unplaceable firms are not the ones the spend publishes — "
                      "a rung <= 3 fact must be cited before one of them moves")

    # 6. A household is seated where, and only where, its own record names a roof.
    seated = {r["id"] for r in rows
              if r["kind"] == "household" and r["rung"] == "structure"}
    named = {hh["id"] for hh in household_records()
             if (hh.get("lives_at") or {}).get("value")}
    if seated != named:
        raise Refused("the seated households are not the households whose committed "
                      "record names a roof")

    # 7. Rung 2 stands empty, and the ledger that would fill it is re-read to say so.
    if any(r["rung"] == "lot" for r in rows):
        raise Refused("a row sits at rung 2 and this pass writes none — if the lot "
                      "ledger has grown, seat it deliberately, with its address quoted")
    ledger = read_json(LOT_ADDRESSES)["addresses"]
    claimed = next(v for v in doc["vocabulary"]["rungs"] if v["rung"] == "lot")
    if str(len(ledger)) not in claimed["stands_empty_because"]:
        raise Refused("the lot ledger has changed size and the rung still claims the old "
                      "one — re-read it before saying the rung is empty")

    # 8. The counts are what the rows say.
    fresh = build()["counts"]
    if fresh != doc["counts"]:
        raise Refused("the committed counts are not what the rows say")


def report(doc: dict) -> str:
    c = doc["counts"]
    out = [f"{c['rows']} rows — {c['households']} households, {c['businesses']} firms",
           f"  seated: {c['seated']}    owed: {c['owed']}"]
    for rung, n in c["by_rung"].items():
        out.append(f"  rung {rung:<12} {n}")
    for reach, n in c["by_reach"].items():
        out.append(f"  reach {reach:<11} {n}")
    return "\n".join(out) + "\n"


def check() -> int:
    committed = read_committed()
    if committed is None:
        print(f"REFUSED: {OUT.relative_to(ROOT)} is missing or unreadable — run --build")
        return 1
    fresh = build()
    if fresh["rows"] != committed["rows"]:
        fresh_by = {r["id"]: r for r in fresh["rows"]}
        old_by = {r["id"]: r for r in committed["rows"]}
        added = sorted(set(fresh_by) - set(old_by))
        gone = sorted(set(old_by) - set(fresh_by))
        changed = sorted(k for k in set(fresh_by) & set(old_by)
                         if fresh_by[k] != old_by[k])
        print("REFUSED: a rebuild would not produce the committed address book.")
        for label, items in (("added", added), ("gone", gone), ("changed", changed)):
            if items:
                print(f"  {label} ({len(items)}): {', '.join(items[:5])}"
                      + (" ..." if len(items) > 5 else ""))
        return 1
    try:
        assertions(committed)
    except Refused as exc:
        print(f"REFUSED: {exc}")
        return 1
    c = committed["counts"]
    print(f"{c['rows']} address-book rows — {c['seated']} seated, {c['owed']} owed; "
          f"by rung {c['by_rung']}")
    return 0


def self_test() -> int:
    """Break each limit and require its assertion to fire."""
    doc = read_committed() or build()
    faults = []

    def fires(name, mutate):
        broken = json.loads(json.dumps(doc))
        mutate(broken)
        try:
            assertions(broken)
        except Refused as exc:
            print(f"  fires: {name} -> {str(exc)[:110]}")
            return
        faults.append(name)

    def pick(kind, rung):
        return lambda d: next(r for r in d["rows"]
                              if r["kind"] == kind and r["rung"] == rung)

    def duplicate(d):
        d["rows"].append(json.loads(json.dumps(d["rows"][0])))

    def a_household_vanishes(d):
        d["rows"].remove(pick("household", "owed")(d))

    def a_firm_vanishes(d):
        d["rows"].remove(pick("business", "unplaceable")(d))

    def an_invented_seat(d):
        pick("household", "owed")(d)["seat"] = {"kind": "structure",
                                                "id": "a_building_nobody_holds"}

    def an_owed_row_takes_a_roof(d):
        row = pick("household", "owed")(d)
        row["seat"] = {"kind": "structure", "id": sorted(committed_structures())[0]}

    def an_owed_row_owes_nobody(d):
        pick("household", "owed")(d)["owed_to"] = None

    def a_row_says_nothing(d):
        pick("household", "owed")(d)["words"] = ""

    def a_row_cannot_be_retired(d):
        pick("business", "unplaceable")(d)["replaceable_by"] = ""

    def a_firm_changes_rung(d):
        pick("business", "unplaceable")(d)["rung"] = "face"

    def an_unplaceable_firm_is_seated(d):
        row = pick("business", "unplaceable")(d)
        row["rung"] = "structure"
        row["reach"] = "structure"

    def a_household_is_seated_from_nowhere(d):
        row = pick("household", "owed")(d)
        row["rung"] = "structure"

    def a_row_climbs_to_rung_two(d):
        pick("household", "owed")(d)["rung"] = "lot"

    def the_lot_ledger_claim_goes_stale(d):
        claimed = next(v for v in d["vocabulary"]["rungs"] if v["rung"] == "lot")
        claimed["stands_empty_because"] = "the ledger carries 99 addresses and names nobody"

    def the_counts_drift(d):
        d["counts"]["seated"] += 1

    fires("a duplicated row", duplicate)
    fires("a household that loses its row", a_household_vanishes)
    fires("a firm that loses its row", a_firm_vanishes)
    fires("a seat the dataset does not hold", an_invented_seat)
    fires("an owed row that acquires a roof", an_owed_row_takes_a_roof)
    fires("an owed row that names no successor", an_owed_row_owes_nobody)
    fires("a row with nothing to say on a card", a_row_says_nothing)
    fires("a row nothing would retire", a_row_cannot_be_retired)
    fires("a firm whose rung stops restating the spend", a_firm_changes_rung)
    fires("an unplaceable firm that gets seated", an_unplaceable_firm_is_seated)
    fires("a household seated with no roof in its record", a_household_is_seated_from_nowhere)
    fires("a row that climbs to the empty rung 2", a_row_climbs_to_rung_two)
    fires("a stale reading of the lot-address ledger", the_lot_ledger_claim_goes_stale)
    fires("counts that drift from the rows", the_counts_drift)

    if faults:
        print("SELF-TEST FAILED — these assertions did not fire: " + ", ".join(faults))
        return 1
    print("all 14 assertions fire when broken")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    if "--check" in argv:
        return check()
    if "--report" in argv:
        print(report(read_committed() or build()), end="")
        return 0
    if "--build" in argv:
        doc = build()
        assertions(doc)
        write(doc)
        print(f"wrote {OUT.relative_to(ROOT)}")
        print(report(doc), end="")
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
