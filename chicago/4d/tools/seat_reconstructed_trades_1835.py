#!/usr/bin/env python3
"""THE STAFFING JOIN, RECONSTRUCTED HALF: where the people nobody named worked.

T-1433, piece 2 of 3 of T-1189.

    tools/seat_reconstructed_trades_1835.py --build       write persons[].employment
    tools/seat_reconstructed_trades_1835.py --check       re-derive, refuse drift
    tools/seat_reconstructed_trades_1835.py --self-test   the guards, fired on the real data

THE GAP THIS CLOSES. T-1432 carried across every workplace a SOURCE names: 144 rows,
110 cards. It said so itself, and named this ticket for the rest. The rest is 524
people — the residents this project RECONSTRUCTED, each given a trade by the town
model and not one of them given anywhere to follow it. A card that says `carpenter`
and nothing else is a trade with no town attached to it, and 524 of them is most of
the working population of the reconstructed town.

WHAT IT WRITES, AND WHAT IT REFUSES TO WRITE. One block, `persons[].employment`, on
every reconstructed trade-holder who has no `workplaces`. It mints NOBODY, raises no
business, and moves no person: the seat is a POINTER from a card the layer already
holds to a house the layer already holds, drawn by a stated rule and reproducible from
the seed it carries. Where no house can be pointed at, the block says that instead,
in the words of the ruling that decided it — a stated absence, never a blank.

WHY `employment` AND NOT `workplaces`. `workplaces` is T-1432's field and T-1432's
gate asserts it BOTH ways: an entry there with no business record naming that person
back is a fossil and the gate fails on it. That assertion is worth more than the
convenience of one field, because it is the thing that keeps the attested join honest.
A reconstructed seat is the other kind of claim — nobody named it, this project drew
it — so it gets the other word, and the two can never be read as one. The business
side of the join, the `staff[]` row that would make a seat visible from the house,
is T-1434's: it mints the shortfall the model still says is missing, and a business
card that printed a reconstructed hand before the shortfall was minted would be a
half-filled house reading as a full one.

THE FIVE ANSWERS. Every person in scope gets exactly one, and each is a different
statement about the evidence:

  `seated`                  the staffing model names a class of house that employed
                            this trade, the layer holds such a house at the scene
                            date, and it has room in its band. The block names the
                            house, the role and the term of the order rule that chose
                            it.
  `class_held_no_house`     the model names the class and the layer holds no house of
                            it trading on 1 July 1835, or every one of them is full to
                            the band's high end. The block names the class and the
                            count.
  `keeps_their_own_house`   the premises ruling says this trade kept premises of its
                            own and the model does not employ it in anybody else's.
                            A seat would demote a principal to a hand. The house is
                            owed, and the block says which ticket owes it.
  `no_employer_named`       the premises ruling says the trade kept no premises of its
                            own AND the model employs it nowhere — the soldier at the
                            post, the laundress over her own tub, the farmer on his own
                            ground. The block carries the ruling's own words for why.
  `no_ruling`               the trade is in the resident layer's occupation vocabulary
                            and `premises_rulings.json` has never ruled on it. Five
                            people stand here and the block says so rather than
                            guessing; T-1404 owns the ruling.

THE ORDER RULE, AND WHICH OF ITS TERMS ACTUALLY BITES TODAY. The ticket asks for the
nearest house of the trade in the person's own division, seeded. That is three terms
and they are applied in that order, but two of them are INERT against the data as it
stands and the report counts exactly how often each one decided a seat, so the day
they start biting is visible rather than assumed:

  1. DIVISION. A business record carries no `division` today and that is not an
     oversight — `tools/build_order_book_1835.py` says it in the book: "EVERY BUSINESS
     BUCKET IS `unassigned` BY DIVISION TODAY ... assigning premises to a division is
     T-1182's audit and T-1198's seating." This tool reads the field and does not
     invent it. Deriving one from the street would be that audit performed by a tool
     with no licence for it, and it would be wrong besides: Lake Street runs from local
     easting -320 to +900 and crosses the South Branch, so half the register's street-
     only premises sit on lines that straddle a division line.
  2. NEAREST. Both ends must resolve to committed coordinates. 30 of 197 business
     records name a structure; 12 of 414 reconstructed households are seated at one,
     because seating them is T-1198's and T-1199's and both stand below this ticket in
     the queue. So this term decides the few it can and stands aside for the rest.
  3. THE SEEDED DRAW. What is left: a deterministic order over the candidate houses,
     keyed on the person, the trade and the house. It is a draw and the block says it
     is a draw — `chosen_by` carries the term that decided, so no reader has to take
     the tool's word for which one did.

CAPACITY IS THE MODEL'S, NOT THIS TOOL'S. A house may take no more hands in a role
than `count_high` for that role in its class. That bound is why `class_held_no_house`
exists at all: 23 reconstructed dressmakers against the one dressmaking house the
register carries is not a shop with 23 hands in it, it is a town owed more shops, and
the report says how many.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESIDENTS = ROOT / "data" / "residents"
BUSINESSES = ROOT / "data" / "businesses"
STRUCTURES = ROOT / "data" / "structures"
PREMISES_RULINGS = ROOT / "data" / "businesses" / "rulings" / "premises_rulings.json"
STAFFING_MODEL = ROOT / "data" / "reconstruction" / "1835_business_staffing_model.json"
RESIDENT_INDEX = RESIDENTS / "index.json"
REPORT_OUT = ROOT / "data" / "reconstruction" / "1835_reconstructed_seating.json"

SCENE_DATE = "1835-07-01"
TICKET = "T-1433"
PARENT_TICKET = "T-1189"

#: Every directory of the resident layer that holds household-shaped records with a
#: `persons[]` list. T-1432 read only `households/`; the reconstructed people this
#: ticket is about are mostly NOT there — 308 of them stand in `reconstructed_trades/`,
#: which is the stage that drew them — so a pass that read one directory would miss
#: three fifths of its own population and report a finished job.
RESIDENT_DIRS = ("households", "reconstructed_trades", "lodgers", "underdocumented",
                 "transients", "readmitted", "merged")

#: The slot on the person, for the same reason `workplaces` has one: the four mints
#: rebuild a card whole and `tools/resident_mint_carry.py` carries the foreign keys
#: back. Anything appended at the TAIL lands behind the keys `spend_person_sex_age.py`
#: and `reconstruct_sex_age.py` pop and re-append, and reads as drift by turns. This
#: block goes immediately after `workplaces` where a card has one and after
#: `occupation` where it does not — the attested answer first, then the drawn one.
AFTER_KEYS = ("workplaces", "occupation", "roles")

#: A value the occupation field uses to say the sources record no trade. It is not a
#: trade and nobody is seated on it.
NOT_A_TRADE = ("none_recorded", "not_recorded", "unknown", None, "")


class Fault(Exception):
    """A refusal, printed and exited on. Never a warning."""


def _sentence(text) -> str:
    """A quoted ruling, ended so the sentence after it does not run into it. The
    ruling's own words are never otherwise touched: several of them end mid-clause
    ("exercised at an establishment the person does not keep") and that is how the
    adjudication reads, not a fault to be tidied away."""
    text = (text or "").strip()
    return text if text.endswith((".", "!", "?")) else text + "."


# ------------------------------------------------------------------ reading --

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load() -> dict:
    for path in (PREMISES_RULINGS, STAFFING_MODEL, RESIDENT_INDEX):
        if not path.exists():
            raise Fault(f"{path.relative_to(ROOT)} is missing")
    records = []
    for name in RESIDENT_DIRS:
        folder = RESIDENTS / name
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.json")):
            records.append((path, _load_json(path)))
    if not records:
        raise Fault("the residents layer holds no household records")
    businesses = [_load_json(p) for p in sorted(BUSINESSES.glob("*.json"))
                  if p.name != "index.json"]
    if not businesses:
        raise Fault("the business layer holds no records")
    return {
        "records": records,
        "businesses": businesses,
        "rulings": {r["occupation"]: r for r in _load_json(PREMISES_RULINGS)["rulings"]},
        "model": _load_json(STAFFING_MODEL),
        # THE ROLE A SEAT CARRIES IS THE STAFFING MODEL'S OWN TERM, and the model
        # already states the rule it may be written onto a person under: its
        # `vocabulary_gaps` say a term "may not be written onto a person until
        # data/residents/index.json carries it". So the vocabulary this gate holds the
        # role to is the resident layer's `occupations`, not the businesses schema's
        # `role` enum. The two are different words for different places — the schema's
        # enum governs a row ON A BUSINESS RECORD, which this pass never writes — and
        # holding a card to the register's enum would refuse `domestic`, `teamster` and
        # fourteen other terms the model staffs houses with and the resident layer
        # already speaks.
        "occupations": list(_load_json(RESIDENT_INDEX)["vocabulary"]["occupations"]),
    }


def structure_points() -> dict:
    """Every structure that states a position, at its scene-date phase, in UTM metres.
    A structure with no position is not a point and is never guessed at."""
    points: dict = {}
    if not STRUCTURES.is_dir():
        return points
    for path in sorted(STRUCTURES.glob("*.json")):
        if path.name == "index.json":
            continue
        record = _load_json(path)
        for phase in record.get("phases") or []:
            position = phase.get("position") or {}
            if position.get("utm_e") is None or position.get("utm_n") is None:
                continue
            points.setdefault(record.get("id"),
                              (float(position["utm_e"]), float(position["utm_n"])))
    return points


# ----------------------------------------------------------------- deriving --

def employing_classes(model: dict) -> dict:
    """occupation_term -> the (class, role, high) rows of the staffing model that put a
    person of that trade to work in somebody else's house. The model's own table; no
    trade is added to it here."""
    out: dict = {}
    for klass in model.get("classes") or []:
        for role in klass.get("staff_roles") or []:
            term = role.get("occupation_term")
            if not term:
                continue
            out.setdefault(term, []).append({
                "class": klass["class"],
                "reads_as": klass.get("reads_as"),
                "occupations_in_this_class": list(klass.get("occupations_in_this_class") or []),
                "role": role.get("role"),
                "count_typical": int(role.get("count_typical") or 0),
                "count_high": int(role.get("count_high") or 0),
                "basis": role.get("basis"),
                "note": role.get("note"),
            })
    for rows in out.values():
        rows.sort(key=lambda r: (r["class"], r["role"]))
    return out


def principal_classes(model: dict) -> dict:
    """occupation -> the classes of house that trade KEEPS. A principal is not seated
    as somebody else's hand."""
    out: dict = {}
    for klass in model.get("classes") or []:
        for occupation in klass.get("occupations_in_this_class") or []:
            out.setdefault(occupation, []).append(klass["class"])
    for rows in out.values():
        rows.sort()
    return out


def houses_by_occupation(businesses: list) -> dict:
    """The business records trading on the scene date, by the occupation the layer
    gives them. A record with no `occupation` is staffable as no kind of house — the
    staffing model already refuses those nine by name — and is not a candidate."""
    out: dict = {}
    for business in businesses:
        if not business.get("present_at_scene_date"):
            continue
        occupation = business.get("occupation")
        if not occupation:
            continue
        out.setdefault(occupation, []).append(business)
    for rows in out.values():
        rows.sort(key=lambda b: b["id"])
    return out


def business_point(business: dict, points: dict):
    """The house on the ground, where the register places it AT a structure this
    project holds. A street-only or unplaceable premises is not a point."""
    for location in business.get("locations") or []:
        structure = location.get("structure_id")
        if structure and structure in points:
            return points[structure]
    return None


def household_point(record: dict, points: dict):
    lives_at = record.get("lives_at")
    value = lives_at.get("value") if isinstance(lives_at, dict) else lives_at
    return points.get(value) if value else None


def business_division(business: dict):
    """The division the RECORD states, and nothing derived. See the module docstring:
    the order book reserves this assignment to T-1182 and T-1198, and today no record
    carries one. Reading the field rather than hard-coding `None` is what makes the
    term start biting the day those tickets write it."""
    for location in business.get("locations") or []:
        if location.get("division"):
            return location["division"]
    return business.get("division")


def rank_key(person_id: str, trade: str, business_id: str) -> str:
    return hashlib.sha256(f"{person_id}:{trade}:{business_id}".encode()).hexdigest()


def in_scope(person: dict) -> bool:
    """A reconstructed trade with nowhere to follow it. An ATTESTED trade with no
    workplace is not this ticket's: the sources named the trade and named no house,
    and drawing one would put a man the record knows into a shop nobody put him in."""
    occupation = person.get("occupation") or {}
    if occupation.get("confidence") != "reconstructed":
        return False
    if occupation.get("value") in NOT_A_TRADE:
        return False
    return not person.get("workplaces")


def seat_one(person: dict, record: dict, trade: str, context: dict) -> dict:
    """The one block this person gets. Pure: it reads the context and the counters and
    returns the answer, so the self-test can fire it on a mutated copy."""
    pid = person.get("id")
    ruling = context["rulings"].get(trade)
    employers = context["employing"].get(trade) or []
    principal_of = context["principal"].get(trade) or []
    division = record.get("division")
    base = {
        "kind": None,
        "trade": trade,
        "premises": ruling.get("premises") if ruling else None,
        "division_of_the_person": division,
        "business_id": None,
        "business_name": None,
        "role": None,
        "tier": "reconstructed",
        "seed": f"{pid}:employment",
        "ticket": TICKET,
        "parent_ticket": PARENT_TICKET,
    }

    if ruling is None:
        base.update({
            "kind": "no_ruling",
            "basis": {
                "kind": "rule",
                "id": "premises_rulings_has_not_ruled_on_this_trade",
                "note": "data/businesses/rulings/premises_rulings.json rules, trade by "
                        "trade, whether a trade implied premises of its own. It has no "
                        "ruling for this one, so this pass does not know whether this "
                        "person kept a house or worked in somebody else's, and it will "
                        "not decide that by seating them. T-1404 owns the ruling table.",
            },
            "replaceable_by": {
                "kind": "ruling",
                "match": "a premises ruling for this trade, after which this block "
                         "re-derives to a seat or to a stated absence",
            },
            "chosen_by": [],
        })
        return base

    # A KEEPER IS NOT A HAND. Where the premises ruling says this trade kept premises
    # of its own AND the model employs it in nobody else's house, the person is owed a
    # house rather than a seat in one. THE TWO QUESTIONS ARE NOT THE SAME QUESTION, and
    # that is why this branch needs BOTH halves: `own_premises` rules on whether the
    # trade implies a shop of its own for the purpose of RAISING a business record,
    # while the staffing model rules on whether a house of some class HIRED that trade.
    # A dressmaker answers yes to both — she might keep a shop, and the millinery houses
    # the register carries employed dressmakers — and the seat below is the honest
    # answer for her, because the layer holds those houses and it does not hold hers.
    if ruling.get("premises") == "own_premises" and not employers:
        base.update({
            "kind": "keeps_their_own_house",
            "classes": principal_of,
            "basis": {
                "kind": "rule",
                "id": "the_premises_ruling_gives_this_trade_a_house_of_its_own",
                "note": f"The premises ruling: {_sentence(ruling.get('basis'))} "
                        + (f"The staffing model keeps {', '.join(principal_of)} at this "
                           f"trade and employs it in no class. " if principal_of else
                           "The staffing model employs this trade in no class of house "
                           "either, so there is not even somebody else's counter to "
                           "stand behind. ")
                        + "Seating this person as somebody else's hand would demote a "
                          "keeper to a clerk to close a count. The house is owed and "
                          "T-1434 mints the layer's shortfall.",
            },
            "replaceable_by": {
                "kind": "business",
                "match": "a house of this trade raised for this person, after which the "
                         "seat is theirs and this block becomes a proprietorship",
            },
            "chosen_by": [],
        })
        return base

    # AND NO PREMISES OF THEIR OWN EITHER. The ruling says the trade kept no house and
    # the model hires it into none: the soldier at the post, the laundress over her own
    # tub, the farmer on his own ground. The absence is the reading and the ruling's own
    # words are the reason for it.
    if not employers:
        base.update({
            "kind": "no_employer_named",
            "basis": {
                "kind": "ruling",
                "id": "no_fixed_premises_and_no_class_employs_this_trade",
                "note": f"The premises ruling: {_sentence(ruling.get('basis'))} The "
                        f"staffing model employs this trade in no class of house, so "
                        f"there is no house "
                        f"to point at and this pass names none. The absence is the "
                        f"reading.",
            },
            "replaceable_by": {
                "kind": "business",
                "match": "an establishment record for the place this ruling names — the "
                         "post, the school, the household served — after which the seat "
                         "re-derives onto it",
            },
            "chosen_by": [],
        })
        return base

    # THE CANDIDATE HOUSES, over every class of the model that employs this trade.
    candidates = []
    for row in employers:
        for occupation in row["occupations_in_this_class"]:
            for business in context["houses"].get(occupation) or []:
                taken = context["filled"].get((business["id"], row["role"]), 0)
                if taken >= row["count_high"]:
                    continue
                candidates.append((business, row))
    if not candidates:
        classes = sorted({row["class"] for row in employers})
        base.update({
            "kind": "class_held_no_house",
            "classes": classes,
            "basis": {
                "kind": "rule",
                "id": "the_class_that_employs_this_trade_holds_no_room",
                "note": f"The staffing model employs this trade in "
                        f"{', '.join(classes)}, and the business layer holds no house of "
                        f"that kind trading on {SCENE_DATE} with room left in its band. "
                        f"A house may take no more hands in a role than the model's own "
                        f"`count_high` for it, so the overflow is a town owed more houses "
                        f"and not a shop with more hands in it than the model allows.",
            },
            "replaceable_by": {
                "kind": "business",
                "match": "a house of this class raised or read into the layer, after "
                         "which this person seats at it",
            },
            "chosen_by": [],
        })
        return base

    # THE ORDER RULE. Three terms, in order, and the one that DECIDED is recorded.
    point = household_point(record, context["points"])
    ranked = []
    for business, row in candidates:
        same_division = 1 if (division and business_division(business) == division) else 0
        other = business_point(business, context["points"])
        if point and other:
            distance = ((point[0] - other[0]) ** 2 + (point[1] - other[1]) ** 2) ** 0.5
            measured = 1
        else:
            distance = 0.0
            measured = 0
        ranked.append((-same_division, -measured, distance,
                       rank_key(pid, trade, business["id"]), business, row))
    ranked.sort(key=lambda r: r[:4])
    best = ranked[0]
    business, row = best[4], best[5]
    chosen_by = []
    if -best[0]:
        chosen_by.append("division_match")
    if -best[1]:
        chosen_by.append("nearest")
    if not chosen_by:
        chosen_by.append("seeded_draw")
    base.update({
        "kind": "seated",
        "business_id": business["id"],
        "business_name": business.get("name"),
        "role": row["role"],
        "establishment_class": row["class"],
        "basis": {
            "kind": "model",
            "id": f"1835_business_staffing_model#{row['class']}.{row['role']}",
            "note": f"The staffing model puts {row['count_typical']} of this role in "
                    f"{row['reads_as'] or row['class']} at the typical band and "
                    f"{row['count_high']} at the high end, on "
                    f"{row['basis']}. {row['note'] or ''} This person is a reconstructed "
                    f"resident of the trade with no workplace of their own; the house is "
                    f"one the business layer already holds, and this row points at it "
                    f"rather than raising anything.".strip(),
        },
        "replaceable_by": {
            "kind": "person",
            "match": "a source naming where this person worked, which retires the draw",
        },
        "chosen_by": chosen_by,
        "candidates_considered": len(ranked),
    })
    context["filled"][(business["id"], row["role"])] = \
        context["filled"].get((business["id"], row["role"]), 0) + 1
    return base


def derive(data: dict) -> dict:
    """The seating, deterministic and order-free: people are taken in person-id order
    over the records in path order, so the same layer always deals the same seats."""
    context = {
        "rulings": data["rulings"],
        "employing": employing_classes(data["model"]),
        "principal": principal_classes(data["model"]),
        "houses": houses_by_occupation(data["businesses"]),
        "points": structure_points(),
        "filled": {},
    }
    occupations = set(data["occupations"])
    people = []
    for path, record in data["records"]:
        for person in record.get("persons") or []:
            if in_scope(person):
                people.append((person.get("id"), path.name, record, person))
    people.sort(key=lambda row: (row[0] or "", row[1]))
    by_person: dict = {}
    for pid, _name, record, person in people:
        if not pid:
            raise Fault("a person in scope carries no id and cannot be seated")
        if pid in by_person:
            raise Fault(f"{pid} stands in the resident layer twice and would be seated "
                        "twice — the convergence T-1190 owns is the place for that")
        block = seat_one(person, record, (person["occupation"]["value"]), context)
        if block["kind"] == "seated" and block["role"] not in occupations:
            raise Fault(f"{pid}: role '{block['role']}' is not a term "
                        "data/residents/index.json carries, so it may not be written "
                        "onto a card — the staffing model's own vocabulary_gaps rule")
        by_person[pid] = block
    return {"by_person": by_person, "filled": context["filled"], "context": context}


# ------------------------------------------------------------------ writing --

def place(person: dict, block) -> dict:
    """The person with `employment` in its fixed slot, or with it removed where this
    pass gives them none."""
    out: dict = {}
    placed = False
    after = next((k for k in AFTER_KEYS if k in person), None)
    for key, value in person.items():
        if key == "employment":
            continue
        out[key] = value
        if block and not placed and key == after:
            out["employment"] = block
            placed = True
    if block and not placed:
        out["employment"] = block
    return out


def apply_to_records(data: dict, seating: dict) -> list:
    out = []
    for path, record in data["records"]:
        rebuilt = dict(record)
        rebuilt["persons"] = [place(p, seating["by_person"].get(p.get("id")))
                              for p in (record.get("persons") or [])]
        out.append((path, json.dumps(rebuilt, indent=1, ensure_ascii=False) + "\n"))
    return out


# ------------------------------------------------------------------- report --

def report(data: dict, seating: dict) -> dict:
    blocks = list(seating["by_person"].values())
    by_kind: dict = {}
    by_trade: dict = {}
    by_chosen: dict = {"division_match": 0, "nearest": 0, "seeded_draw": 0}
    for block in blocks:
        by_kind[block["kind"]] = by_kind.get(block["kind"], 0) + 1
        trade = by_trade.setdefault(block["trade"], {"people": 0, "kinds": {}})
        trade["people"] += 1
        trade["kinds"][block["kind"]] = trade["kinds"].get(block["kind"], 0) + 1
        for term in block.get("chosen_by") or []:
            by_chosen[term] = by_chosen.get(term, 0) + 1
    houses = sorted({(bid, role): n for (bid, role), n in seating["filled"].items()}.items())
    divisions = sum(1 for b in data["businesses"] if business_division(b))
    with_point = sum(1 for b in data["businesses"]
                     if business_point(b, seating["context"]["points"]))
    seated_homes = sum(1 for _p, r in data["records"]
                       if household_point(r, seating["context"]["points"]))
    return {
        "$schema_note": "DERIVED — regenerate with tools/seat_reconstructed_trades_1835.py "
                        "--build; tools/check.sh re-derives it. Do not hand-edit.",
        "id": "1835_reconstructed_seating",
        "ticket": TICKET,
        "parent_ticket": PARENT_TICKET,
        "target_date": SCENE_DATE,
        "generated_by": "tools/seat_reconstructed_trades_1835.py --build",
        "not_a_reading": "an adjudication over committed files — no page of any source is "
                         "read here, no person is written and no business is raised",
        "writes_no_person": True,
        "raises_no_business": True,
        "what_it_writes": "persons[].employment on every reconstructed trade-holder with "
                          "no workplaces — a pointer at a house the business layer already "
                          "holds, or a stated reason there is none",
        "inputs": [
            "data/residents/{" + ",".join(RESIDENT_DIRS) + "}/*.json",
            "data/businesses/*.json",
            "data/businesses/rulings/premises_rulings.json",
            "data/reconstruction/1835_business_staffing_model.json",
            "data/structures/*.json",
        ],
        "counts": {
            "people_in_scope": len(blocks),
            "by_kind": dict(sorted(by_kind.items())),
            "houses_taking_a_reconstructed_hand": len({bid for (bid, _r) in
                                                       seating["filled"]}),
            "seats_by_house_and_role": [
                {"business_id": bid, "role": role, "seats": n}
                for (bid, role), n in houses
            ],
        },
        "which_term_of_the_order_rule_decided": {
            "what_this_is": "The ticket asks for the nearest house of the trade in the "
                            "person's own division, seeded. Two of those three terms are "
                            "inert against the layer as it stands, and this count is how "
                            "a reader sees that rather than taking the rule's word for it.",
            "division_match": by_chosen["division_match"],
            "nearest": by_chosen["nearest"],
            "seeded_draw": by_chosen["seeded_draw"],
            "why_division_is_inert": "No business record carries a division. The order "
                                     "book says why in its own words — 'EVERY BUSINESS "
                                     "BUCKET IS `unassigned` BY DIVISION TODAY ... "
                                     "assigning premises to a division is T-1182's audit "
                                     "and T-1198's seating' — and this tool reads the "
                                     "field rather than deriving one, because deriving "
                                     "one is that audit done without a licence for it. "
                                     f"Business records stating a division today: {divisions}.",
            "why_nearest_is_nearly_inert": "Both ends must resolve to committed "
                                           f"coordinates. {with_point} of "
                                           f"{len(data['businesses'])} business records "
                                           "name a structure this project holds, and "
                                           f"{seated_homes} of "
                                           f"{len(data['records'])} resident records are "
                                           "seated at one. Seating the reconstructed "
                                           "households is T-1198's and T-1199's.",
        },
        "by_trade": {k: by_trade[k] for k in sorted(by_trade)},
        "what_this_does_not_do": {
            "the_business_side_is_T-1434s": "Nothing is written onto a business record "
                                            "here. `staff[]` stays as the register left "
                                            "it until T-1434 has minted the shortfall, so "
                                            "a business card cannot print a half-filled "
                                            "house as a full one.",
            "T-1434": "Mints the shortfall to the model's typical band, gives every "
                      "working-age person a workplace or an explicit not_employed reason, "
                      "fills the order book's employment buckets and prints the people on "
                      "the business card.",
            "the_attested_half": "T-1432 wrote persons[].workplaces from the rows a source "
                                 "names. This pass never touches that field and never "
                                 "seats a person who has one.",
        },
    }


# --------------------------------------------------------------- the refusals --

def verify(data: dict, seating: dict, records) -> int:
    """The seating as it stands on disk, asserted both ways."""
    want = seating["by_person"]
    seen = 0
    for path, record in records:
        for person in record.get("persons") or []:
            pid = person.get("id")
            block = person.get("employment")
            if block is None:
                if pid in want:
                    raise Fault(f"{pid} is a reconstructed trade-holder with no workplace "
                                "and their card carries no employment — run "
                                "tools/seat_reconstructed_trades_1835.py --build")
                continue
            seen += 1
            if pid not in want:
                raise Fault(f"{path.name}/{pid} carries an employment block and is not in "
                            "scope for one — a card with a workplace, or with no "
                            "reconstructed trade, keeps no seat. The join has a fossil "
                            "on it")
            if json.dumps(block, sort_keys=True) != json.dumps(want[pid], sort_keys=True):
                raise Fault(f"{pid}'s employment no longer re-derives — run "
                            "tools/seat_reconstructed_trades_1835.py --build")
    return seen


def assert_the_model_is_not_exceeded(data: dict, seating: dict) -> None:
    """The one refusal that matters: a house with more reconstructed hands in a role
    than the staffing model's high end for that role. That would be people invented
    here, under a rule that says it invents nobody."""
    caps: dict = {}
    for term, rows in employing_classes(data["model"]).items():
        for row in rows:
            for occupation in row["occupations_in_this_class"]:
                for business in houses_by_occupation(data["businesses"]).get(occupation) or []:
                    key = (business["id"], row["role"])
                    caps[key] = max(caps.get(key, 0), row["count_high"])
    for key, filled in sorted(seating["filled"].items()):
        cap = caps.get(key)
        if cap is None:
            raise Fault(f"{key[0]} took a '{key[1]}' the staffing model does not put in a "
                        "house of its class")
        if filled > cap:
            raise Fault(f"{key[0]} holds {filled} reconstructed '{key[1]}' and the "
                        f"staffing model's high end for that role is {cap} — this pass "
                        "would be inventing hands")


# ------------------------------------------------------------------ commands --

def cmd_build() -> int:
    data = load()
    seating = derive(data)
    assert_the_model_is_not_exceeded(data, seating)
    for path, text in apply_to_records(data, seating):
        if path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
    doc = report(data, seating)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    counts = doc["counts"]
    kinds = counts["by_kind"]
    print(f"OK: the 1835 reconstructed seating — {counts['people_in_scope']} reconstructed "
          f"trade-holders answered, {kinds.get('seated', 0)} seated in "
          f"{counts['houses_taking_a_reconstructed_hand']} houses, "
          f"{counts['people_in_scope'] - kinds.get('seated', 0)} given a stated reason "
          "there is no house to point at; nobody minted, no business raised")
    return 0


def cmd_check() -> int:
    if not REPORT_OUT.exists():
        raise Fault(f"{REPORT_OUT.relative_to(ROOT)} has never been built")
    data = load()
    seating = derive(data)
    assert_the_model_is_not_exceeded(data, seating)
    for path, text in apply_to_records(data, seating):
        if path.read_text(encoding="utf-8") != text:
            raise Fault(f"{path.name} no longer matches the seating it should carry — run "
                        "tools/seat_reconstructed_trades_1835.py --build")
    verify(data, seating, data["records"])
    was = json.loads(REPORT_OUT.read_text(encoding="utf-8"))
    now = report(data, seating)
    if json.dumps(was, sort_keys=True) != json.dumps(now, sort_keys=True):
        raise Fault(f"{REPORT_OUT.relative_to(ROOT)} no longer re-derives — run "
                    "tools/seat_reconstructed_trades_1835.py --build")
    print(f"OK: {now['counts']['people_in_scope']} reconstructed trade-holders re-derive "
          "to the seats and stated absences their cards carry")
    return 0


def _fires(what: str, thunk) -> None:
    try:
        thunk()
    except Fault:
        return
    raise Fault(f"the guard against {what} did not fire")


def cmd_self_test() -> int:
    data = load()
    seating = derive(data)

    # ONE: a fossil — an employment block on a card this pass does not seat.
    def fossil():
        records = []
        planted = False
        for path, record in data["records"]:
            copy = json.loads(json.dumps(record))
            for person in copy.get("persons") or []:
                if not planted and person.get("id") not in seating["by_person"]:
                    person["employment"] = {"kind": "seated"}
                    planted = True
            records.append((path, copy))
        if not planted:
            raise Fault("the self-test found no out-of-scope card to plant a fossil on")
        verify(data, seating, records)
    _fires("a card carrying a seat it is not owed", fossil)

    # TWO: a lost block — a card in scope whose employment has been dropped.
    def lost():
        records = []
        dropped = False
        for path, record in data["records"]:
            copy = json.loads(json.dumps(record))
            for person in copy.get("persons") or []:
                if not dropped and person.get("id") in seating["by_person"]:
                    person.pop("employment", None)
                    dropped = True
            records.append((path, copy))
        if not dropped:
            raise Fault("the self-test found no seated card to drop")
        verify(data, seating, records)
    _fires("a seated card that has lost its block", lost)

    # THREE: drift — the same card, a different seat.
    def drift():
        records = []
        bent = False
        for path, record in data["records"]:
            copy = json.loads(json.dumps(record))
            for person in copy.get("persons") or []:
                if not bent and person.get("id") in seating["by_person"]:
                    person["employment"] = dict(person.get("employment") or {},
                                                business_id="biz_not_a_house")
                    bent = True
            records.append((path, copy))
        verify(data, seating, records)
    _fires("a seat that no longer re-derives", drift)

    # FOUR: the model exceeded — one more hand than the band's high end allows.
    def exceeded():
        bent = dict(seating)
        key = next(iter(sorted(seating["filled"])), None)
        if key is None:
            raise Fault("the self-test found no filled seat to overfill")
        bent["filled"] = dict(seating["filled"])
        bent["filled"][key] = 9999
        assert_the_model_is_not_exceeded(data, bent)
    _fires("a house staffed past the model's high end", exceeded)

    # FIVE: a role the businesses schema does not hold may not be written.
    def bad_role():
        bent = json.loads(json.dumps(data["model"]))
        for klass in bent["classes"]:
            for role in klass.get("staff_roles") or []:
                role["role"] = "shop_walker"
        derive({**data, "model": bent})
    _fires("a role the resident vocabulary does not hold", bad_role)

    print("OK: all five assertions of the reconstructed seating fire when broken")
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
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
