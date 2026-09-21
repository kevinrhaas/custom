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

It is more than three runs of work, so it was split (T-1491/T-1492/T-1493, and T-1492
again into T-1512/T-1513). **T-1491 wrote only the rungs the committed evidence already
reaches** — 1, 3 for the adopted firms, and 6 — recorded rung 2 as **measured empty**,
and for every other row wrote down the REACH, the narrowest thing the evidence actually
gives, with `seat: null` and the ticket that owed the seat.

**T-1512 seats the two reconstructed rungs the EVIDENCE still bounds**, and only those:

  * **rung 3, for the 21 street-only firms the face adoption refused.** The paper names
    a platted street and no roof on it was free. They stand on the FACE of that street —
    `seat.kind: street_face` — with no roof, no lot and no coordinate. The street is the
    evidence and keeps its tier; standing them on the face without a roof is the
    reconstructed step, and the row says so.
  * **rung 4, for every household whose own record names a division.** The division is
    the evidence; the BAND inside it is this pass's reconstruction, and it is the
    placement policy's own clause for the head's trade. Where no clause of the policy
    reaches that trade — `occupation: none_recorded`, and the trades the policy has no
    dwelling clause for — the band is the division's own ground and nothing narrower,
    and the row says that rather than dealing a class the record does not carry.

**Rung 5 is NOT dealt here.** 1,186 households carry no division at all, and banding them
means dealing a division AND a class no source gives, counted against the reconstruction
order book. That is T-1513, and until it runs those rows stay `owed` and say so.

No coordinate is invented by this file, no household record is written to by it, and the
division on a rung-4 seat is always the one the household's own card already carries.

THE ONE THING THIS FILE IS NOT.

It is not a second opinion on anything already adjudicated. The business half is a
strict restatement of `data/research/location_spend.json` (T-1239): assertion 4 fails if
a single firm's rung stops agreeing with the grade that file gives it, and assertion 5
fails if the 62 unplaceable firms are not the same 62. The household half is read from
the committed household records and from nothing else — `lives_at` is the seat, and a
household whose record names no roof gets no roof here.

WHAT A ROW SAYS, AND WHY EACH FIELD IS THERE.

    rung          the rung that fired: structure | lot | face | division_band |
                  unplaceable | owed
    seat          the thing it stands on, or null. NEVER set on an `owed` row. A seat
                  carries its own `kind`: structure, street_face or division_band —
                  and only a `structure` seat names a building this dataset holds.
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

POLICY = ROOT / "data" / "reconstruction" / "1835_placement_policy.json"

SCENE_DATE = "1835-07-01"
TICKET = "T-1512"
TICKETS = ["T-1491", "T-1512"]

# Who owes the seat a row does not have. A roof the paper reaches but the town has not
# raised is owed to the district build tickets; a household no source places anywhere is
# owed to T-1513, which deals the division AND the class rung 5 needs.
OWED_POLICY_ONLY = "T-1513"
OWED_BUILD = "T-1200..T-1209"

# The business grade -> (rung, reach, owed_to). A strict restatement of T-1239's
# adjudication; assertion 4 refuses any drift between this table and that file.
# `street_only_unseated` moved from `owed` to rung 3 in T-1512: the face adoption could
# not find the firm a free ROOF, which is not the same as not finding it a FACE.
FROM_GRADE = {
    "structure_committed": ("structure", "structure", None),
    "structure_pending": ("owed", "structure_owed", OWED_BUILD),
    "street_only_adopted": ("face", "face", None),
    "street_only_unseated": ("face", "face", None),
    "unplaceable": ("unplaceable", "none", None),
}

# ---- the band vocabulary (T-1512) ------------------------------------------ #
#
# A BAND IS AN ADJUDICATION OVER THE COMMITTED PLACEMENT POLICY, NOT A NEW READING.
# `data/reconstruction/1835_placement_policy.json` states twelve clauses, each one
# addressed to a set of ROOF FAMILY letters. A household is not a roof family, so the
# one thing this table does is say which clause a head's trade puts the household under
# — and it says it for the trades the policy's dwelling clauses actually reach, and for
# no others. Everything unlisted falls to `division_ground` below, which asserts nothing
# beyond the division the card already carries.
#
# Every value here is a clause id of that file. Assertion 9 refuses one that is not.
TRADE_CLAUSE = {
    # merchant_and_professional_dwellings (H1, H2, D7) — "the better houses take the
    # Randolph-Washington tier a block back from the trade, and the north tier under
    # Kinzie". The merchants and the professions the town's own register names.
    "merchant": "merchant_and_professional_dwellings",
    "lumber_merchant": "merchant_and_professional_dwellings",
    "forwarding_and_commission": "merchant_and_professional_dwellings",
    "clothier": "merchant_and_professional_dwellings",
    "druggist": "merchant_and_professional_dwellings",
    "grocer": "merchant_and_professional_dwellings",
    "auctioneer": "merchant_and_professional_dwellings",
    "attorney": "merchant_and_professional_dwellings",
    "physician": "merchant_and_professional_dwellings",
    "editor": "merchant_and_professional_dwellings",
    "surveyor": "merchant_and_professional_dwellings",
    "speculator": "merchant_and_professional_dwellings",
    "banker": "merchant_and_professional_dwellings",
    "land_agent": "merchant_and_professional_dwellings",
    # tradesman_dwellings (D3-D6) — "the frame cottages fall on the side streets behind
    # the principal frontages". The crafts that keep a shop and a cottage.
    "blacksmith": "tradesman_dwellings",
    "carpenter": "tradesman_dwellings",
    "ship_carpenter": "tradesman_dwellings",
    "mason": "tradesman_dwellings",
    "plasterer": "tradesman_dwellings",
    "painter": "tradesman_dwellings",
    "brickmaker": "tradesman_dwellings",
    "printer": "tradesman_dwellings",
    "watchmaker": "tradesman_dwellings",
    "silversmith": "tradesman_dwellings",
    "gunsmith": "tradesman_dwellings",
    "cooper": "tradesman_dwellings",
    "cabinetmaker": "tradesman_dwellings",
    "wheelwright": "tradesman_dwellings",
    "saddler": "tradesman_dwellings",
    "shoemaker": "tradesman_dwellings",
    "tailor": "tradesman_dwellings",
    "hatter": "tradesman_dwellings",
    "baker": "tradesman_dwellings",
    "butcher": "tradesman_dwellings",
    "barber_surgeon": "tradesman_dwellings",
    "dressmaker": "tradesman_dwellings",
    "milliner": "tradesman_dwellings",
    # labourer_dwellings (D1, D2) — "cabins and shanties take the small lots, the
    # fringes and the ground nobody is bidding on".
    "labourer": "labourer_dwellings",
    "laundress": "labourer_dwellings",
    "domestic": "labourer_dwellings",
    "servant": "labourer_dwellings",
    "cook": "labourer_dwellings",
    "teamster": "labourer_dwellings",
    "carter": "labourer_dwellings",
    "boatman": "labourer_dwellings",
    "sailor": "labourer_dwellings",
    # heavy_and_noxious_trades (W5) — "packing, tanning, slaughtering and soap-boiling
    # go to the branches and out of the town's nose".
    "packer": "heavy_and_noxious_trades",
    "tanner": "heavy_and_noxious_trades",
    "slaughterer": "heavy_and_noxious_trades",
    "soap_boiler": "heavy_and_noxious_trades",
    # lodging_near_the_landings (T1-T3, H3) — "an inn stands where the traveller
    # arrives".
    "tavern_keeper": "lodging_near_the_landings",
    "innkeeper": "lodging_near_the_landings",
    "boarding_house_keeper": "lodging_near_the_landings",
    # garrison_reservation (M1) — the military reservation, unplatted, no street.
    "soldier": "garrison_reservation",
}

# The band a household falls to when no clause of the policy reaches its head's trade.
# It is NOT a clause and it is not pretending to be one: it names the division the card
# already carries and stops there.
DIVISION_GROUND = "division_ground"

# The divisions the town holds. `outside_town` is rung 6 and not a band: the evidence
# does not fail to place these households, it places them somewhere else.
TOWN_DIVISIONS = ("south", "west", "north", "fort")


class Refused(Exception):
    """A limit this file may not cross."""


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def committed_structures() -> set[str]:
    return {p.stem for p in sorted(STRUCTURES.glob("*.json"))}


_HOUSEHOLD_CACHE: list[dict] | None = None


def household_records() -> list[dict]:
    """Every committed household card. Read once — `--self-test` re-asserts fifteen
    times over and the cards are 1,393 files."""
    global _HOUSEHOLD_CACHE
    if _HOUSEHOLD_CACHE is None:
        _HOUSEHOLD_CACHE = [read_json(p) for p in sorted(HOUSEHOLDS.glob("*.json"))]
    return _HOUSEHOLD_CACHE


_POLICY_CACHE: dict[str, dict] | None = None


def policy_clauses() -> dict[str, dict]:
    """The committed placement policy's clauses, by id. Nothing else is read from it."""
    global _POLICY_CACHE
    if _POLICY_CACHE is None:
        _POLICY_CACHE = {c["id"]: c for c in read_json(POLICY)["clauses"]}
    return _POLICY_CACHE


def head_trade(hh: dict) -> str | None:
    """The trade the household's OWN record gives its head, or None.

    `none_recorded` is a recorded absence, not a trade, and it returns None — a head
    with no trade is banded by the division alone, never by a class dealt for them.
    """
    head = hh.get("head")
    for person in hh.get("persons") or []:
        if person.get("id") == head:
            value = (person.get("occupation") or {}).get("value")
            return value if value and value != "none_recorded" else None
    return None


def band_for(division: str, trade: str | None, clauses: dict[str, dict]) -> dict:
    """The band a household in `division` with `trade` falls in.

    Two outcomes and no third. Either the policy holds a dwelling clause for the trade,
    and the band is that clause inside the division the card already names; or it does
    not, and the band is the division's own ground — which adds nothing to what the card
    said. The division is NEVER changed here: it is the evidence, and the band is the
    only reconstructed part of the seat.
    """
    clause_id = TRADE_CLAUSE.get(trade or "")
    if clause_id and clause_id in clauses:
        clause = clauses[clause_id]
        prefers = [t.split(":", 1)[1] for t in clause.get("prefers") or []
                   if t.startswith("division:")]
        return {
            "band": f"{division}/{clause_id}",
            "clause": clause_id,
            "clause_applies_to": list(clause.get("applies_to") or []),
            "clause_tier": clause.get("tier"),
            "statement": clause.get("note"),
            "division_is_the_clause_preference": (division in prefers) if prefers else None,
            "from_trade": trade,
        }
    return {
        "band": f"{division}/{DIVISION_GROUND}",
        "clause": None,
        "clause_applies_to": [],
        "clause_tier": None,
        "statement": ("No dwelling clause of the placement policy reaches this "
                      "household's head, so the band is the division the record names "
                      "and nothing narrower. A class is not dealt for them here."),
        "division_is_the_clause_preference": None,
        "from_trade": trade,
    }


def business_names() -> dict[str, str]:
    """register_id -> the firm's name, for the rows the spend adjudicates."""
    names = {}
    for path in sorted(BUSINESSES.glob("*.json")):
        rec = read_json(path)
        if rec.get("register_id"):
            names[rec["register_id"]] = rec.get("name") or rec["id"]
    return names


# ---- the household half ---------------------------------------------------- #


def household_row(hh: dict, committed: set[str], clauses: dict[str, dict]) -> dict:
    """One household, seated at the first rung that fires.

    Rung 1 fires on `lives_at`, the only field that names a roof. Rung 4 fires on the
    card's own `division` — the band inside it is reconstructed, the division is not.
    Rung 5 is T-1513's and does not fire here: a household with no division at all
    stays `owed` and says whose it is.
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
        "band": None,
        "seed": None,
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
    if division in TOWN_DIVISIONS:
        trade = head_trade(hh)
        band = band_for(division, trade, clauses)
        row["rung"] = "division_band"
        row["seat"] = {"kind": "division_band", "id": band["band"],
                       "division": division, "clause": band["clause"]}
        row["reach"] = "division"
        row["reach_value"] = division
        row["tier"] = "reconstructed"
        row["basis"] = band["statement"]
        row["band"] = band
        # The deal makes no draw: the division is the card's and the clause follows from
        # the head's trade, so the same inputs give the same band every time. The seed is
        # the key that determined it, kept so a reader can retrace the deal — not a die.
        row["seed"] = f"{hh['id']}|{division}|{trade or 'no_trade'}|T-1512"
        if band["clause"]:
            row["words"] = (
                f"The record reaches the {division} division and nothing narrower. Inside "
                f"it the placement policy bands this household by its head's trade "
                f"({trade}): {band['statement']} The division is the evidence; the band "
                "is reconstruction, and no lot, roof or coordinate is claimed by it.")
            row["replaceable_by"] = ("a source naming a street, a corner or a building "
                                     "for this household")
        else:
            row["words"] = (
                f"The record reaches the {division} division and nothing narrower, and "
                "the head's trade is not one the placement policy has a dwelling clause "
                "for — so this household is banded to that division's own ground and no "
                "class is dealt for it. The division is the evidence; standing them "
                "anywhere inside it is reconstruction.")
            row["replaceable_by"] = ("a source giving this household's head a trade, or "
                                     "naming a street, a corner or a building for them")
        return row
    row["rung"] = "owed"
    row["owed_to"] = OWED_POLICY_ONLY
    row["reach"] = "none"
    row["words"] = ("No source places this household anywhere in the town — the record "
                    "gives a name and no address. Banding them needs a division AND a "
                    "class no source carries, counted against the reconstruction order "
                    f"book; that is owed to {OWED_POLICY_ONLY} and is not guessed here.")
    row["replaceable_by"] = "any source that places this household in a division or nearer"
    return row


# ---- the business half ----------------------------------------------------- #


def business_row(placement: dict, names: dict[str, str]) -> dict:
    grade = placement["grade"]
    if grade not in FROM_GRADE:
        raise Refused(f"{placement['business_id']}: unknown adjudicated grade {grade!r}")
    rung, reach, owed = FROM_GRADE[grade]
    street = placement.get("evidence_street")
    if placement.get("model_seat"):
        # The spend adjudicated a roof. Nothing here may move it.
        seat = {"kind": "structure", "id": placement["model_seat"]}
    elif grade == "street_only_unseated":
        # T-1512: the face adoption could not find this firm a free ROOF on the street
        # its advertisement names. That is not the same as not finding it a FACE. It
        # stands on the face — no roof, no lot, no coordinate, and the street it stands
        # on is the one the paper printed.
        seat = {"kind": "street_face", "id": placement["register_action_target"],
                "street_name": street}
    else:
        seat = None
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
        words = (f"The paper reaches {street} and nothing narrower, and no ROOF on it "
                 "could be adopted — every one is spoken for. So this firm stands on the "
                 "FACE itself: on that street, in no building this model holds, with no "
                 "lot and no coordinate claimed. The street is the reading; standing them "
                 "on it without a roof is the reconstructed step.")
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
        "tier": ("reconstructed" if grade == "street_only_unseated"
                 else "inferred" if rung in ("structure", "face") else None),
        "basis": placement.get("clause"),
        "words": words,
        "replaceable_by": ("a printing that names a lot, a corner ordinal or a building "
                           "for this firm"),
        "owed_to": owed,
        "band": None,
        "seed": (f"{placement['business_id']}|{placement['register_action_target']}|T-1512"
                 if grade == "street_only_unseated" else None),
        "seat_is_substitutable": bool(placement.get("seat_is_substitutable")),
        "adjudicated_grade": grade,
    }


# ---- the file -------------------------------------------------------------- #


def build() -> dict:
    committed = committed_structures()
    spend = read_json(SPEND)
    names = business_names()
    clauses = policy_clauses()
    rows = [household_row(hh, committed, clauses) for hh in household_records()]
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
        "tickets": TICKETS,
        "parent_ticket": "T-1198",
        "generated_by": "tools/seat_known_1835.py --build",
        "scene_date": SCENE_DATE,
        "not_a_reading": (
            "Rungs 1, 3-for-an-adopted-firm and 6 restate a seat some other committed "
            "record already made. Rung 3 for a refused street-only firm and rung 4 are "
            "RECONSTRUCTION (T-1512): each carries tier `reconstructed`, the clause it "
            "rests on, a seed and what would retire it, and neither adds a street or a "
            "division the record did not already carry. Rung 5 belongs to "
            + OWED_POLICY_ONLY + " and is not dealt here. No coordinate, no lot and no "
            "roof is invented by this pass, and no household record is written to."),
        "bands": {
            "what_a_band_is": (
                "an adjudication over data/reconstruction/1835_placement_policy.json — "
                "the division the household's own card carries, and the policy clause "
                "its head's trade falls under. A band claims no lot, no roof and no "
                "coordinate; it says which ground inside a division the policy puts a "
                "household of this kind on."),
            "division_ground": (
                "the band for a head whose trade no dwelling clause of the policy "
                "reaches — including every head recorded `none_recorded`. It names the "
                "division and stops, so that a household with no trade is not dealt a "
                "class it never had."),
            "trade_to_clause": dict(sorted(TRADE_CLAUSE.items())),
            "clauses_used": sorted({c for c in TRADE_CLAUSE.values()}),
        },
        "inputs": [
            "data/residents/households/",
            "data/reconstruction/1835_placement_policy.json",
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
                          "substitutable, no lot, no anchor. A firm the adoption could "
                          "seat on a roof of that face carries a `structure` seat; one "
                          "it could not carries the `street_face` itself (T-1512)."},
                {"rung": "division_band", "ladder": 4,
                 "means": "the division the household's own record names, banded inside "
                          "it by the placement policy clause its head's trade falls "
                          "under — or by the division's own ground where no clause "
                          "reaches that trade. Reconstruction, seeded, no coordinate."},
                {"rung": "unplaceable", "ladder": 6,
                 "means": "the evidence contradicts every band inside the town"},
                {"rung": "owed", "ladder": None,
                 "means": "the evidence reaches something, and the seat it implies is "
                          "owed to another ticket. `seat` is null and stays null."},
            ],
            "reaches": ["structure", "structure_owed", "face", "division", "none"],
            "seat_kinds": ["structure", "street_face", "division_band"],
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
            "by_seat_kind": dict(sorted(
                {k: sum(1 for r in rows if r["seat"] and r["seat"]["kind"] == k)
                 for k in ("structure", "street_face", "division_band")}.items())),
            "by_band": dict(sorted(
                {r["seat"]["id"]: sum(1 for x in rows
                                      if x["seat"] and x["seat"]["kind"] == "division_band"
                                      and x["seat"]["id"] == r["seat"]["id"])
                 for r in rows
                 if r["seat"] and r["seat"]["kind"] == "division_band"}.items())),
            "reconstructed_seats": sum(1 for r in rows
                                       if r["seat"] and r["tier"] == "reconstructed"),
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
        seat = row["seat"]
        if seat and seat["kind"] == "structure" and seat["id"] not in committed:
            raise Refused(f"{row['id']}: seated on {seat['id']}, which is not a "
                          "committed structure — no seat may be invented here")
        if seat and seat["kind"] not in ("structure", "street_face", "division_band"):
            raise Refused(f"{row['id']}: seat kind {seat['kind']!r} is not one this "
                          "book holds")
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
        seat = row["seat"]
        roof = seat["id"] if seat and seat["kind"] == "structure" else None
        if roof != placement.get("model_seat"):
            raise Refused(f"{row['id']}: its roof is not the one the spend adjudicated")
        # 4b (T-1512). A firm the adoption could not seat stands on the FACE of the
        # street the register acted on, and on no roof.
        if placement["grade"] == "street_only_unseated":
            if not seat or seat["kind"] != "street_face":
                raise Refused(f"{row['id']}: the adoption refused it a roof, so it must "
                              "stand on the street face — and it does not")
            if seat["id"] != placement["register_action_target"]:
                raise Refused(f"{row['id']}: seated on the face of {seat['id']!r}, which "
                              "is not the street the register acted on")
            if row["tier"] != "reconstructed":
                raise Refused(f"{row['id']}: a face seat with no roof under it is "
                              "reconstruction and must say so")

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

    # 9 (T-1512). Every band is the division the card carries, and a clause the
    # committed policy holds — or the division's own ground and no class at all.
    clauses = policy_clauses()
    hh_by_id = {hh["id"]: hh for hh in household_records()}
    banded = [r for r in rows if r["rung"] == "division_band"]
    for row in banded:
        hh = hh_by_id[row["id"]]
        division = hh.get("division")
        seat = row["seat"]
        if seat["kind"] != "division_band":
            raise Refused(f"{row['id']}: rung 4 and the seat is not a band")
        if seat["division"] != division or not seat["id"].startswith(f"{division}/"):
            raise Refused(f"{row['id']}: banded into {seat['division']!r} while its own "
                          f"record says {division!r} — a band may not move a household "
                          "out of the division its evidence names")
        if row["tier"] != "reconstructed":
            raise Refused(f"{row['id']}: a band is reconstruction and must carry the tier")
        if not row["seed"]:
            raise Refused(f"{row['id']}: a reconstructed seat with no seed")
        clause_id = seat["clause"]
        if clause_id is not None and clause_id not in clauses:
            raise Refused(f"{row['id']}: cites placement-policy clause {clause_id!r}, "
                          "which that file does not hold")
        trade = head_trade(hh)
        if clause_id is None and TRADE_CLAUSE.get(trade or ""):
            raise Refused(f"{row['id']}: its head is a {trade} and the policy has a "
                          "clause for that trade — the band fell to the division ground "
                          "anyway")
        if clause_id is not None and trade is None:
            raise Refused(f"{row['id']}: banded by a clause while its record gives its "
                          "head no trade — no class may be dealt here")

    # 10 (T-1512). Every household whose record names a town division and no roof is
    # banded. None is left owed, and none without a division is banded.
    row_by_id = {r["id"]: r for r in rows if r["kind"] == "household"}
    for hh in household_records():
        row = row_by_id[hh["id"]]
        has_roof = bool((hh.get("lives_at") or {}).get("value"))
        in_division = hh.get("division") in TOWN_DIVISIONS
        if in_division and not has_roof and row["rung"] != "division_band":
            raise Refused(f"{hh['id']}: its record names the {hh['division']} division "
                          f"and it sits at rung {row['rung']!r}")
        if not in_division and row["rung"] == "division_band":
            raise Refused(f"{hh['id']}: banded into a division its record does not name")

    # 11 (T-1512). Rung 5 is not dealt here. Every household with no division at all is
    # still owed, and it is owed to the ticket that deals it.
    for row in rows:
        if row["kind"] == "household" and row["rung"] == "owed":
            if row["reach"] != "none" or row["owed_to"] != OWED_POLICY_ONLY:
                raise Refused(f"{row['id']}: an owed household must reach nothing and "
                              f"owe {OWED_POLICY_ONLY}")

    # 12 (T-1512). No reconstructed seat carries a coordinate, a lot or a roof.
    for row in rows:
        seat = row["seat"]
        if not seat or row["tier"] != "reconstructed":
            continue
        for forbidden in ("lot", "lot_id", "coordinates", "local_enu_m", "structure",
                          "structure_id", "position"):
            if forbidden in seat:
                raise Refused(f"{row['id']}: a reconstructed seat has grown a "
                              f"{forbidden!r} — this pass invents no ground")

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

    # ---- T-1512's own limits ---- #

    def a_band_moves_a_household(d):
        row = pick("household", "division_band")(d)
        other = next(v for v in TOWN_DIVISIONS if v != row["seat"]["division"])
        row["seat"] = {**row["seat"], "division": other, "id": f"{other}/x"}

    def a_band_cites_a_clause_the_policy_lacks(d):
        row = pick("household", "division_band")(d)
        row["seat"] = {**row["seat"], "clause": "a_clause_nobody_wrote"}

    def a_band_loses_its_tier(d):
        pick("household", "division_band")(d)["tier"] = "inferred"

    def a_band_loses_its_seed(d):
        pick("household", "division_band")(d)["seed"] = None

    def a_household_in_a_division_is_left_owed(d):
        row = pick("household", "division_band")(d)
        row["rung"], row["seat"], row["owed_to"] = "owed", None, OWED_POLICY_ONLY

    def an_unplaced_household_is_banded(d):
        row = pick("household", "owed")(d)
        row["rung"] = "division_band"
        row["seat"] = {"kind": "division_band", "id": "south/x",
                       "division": "south", "clause": None}
        row["tier"], row["seed"] = "reconstructed", "x"

    def a_face_firm_moves_street(d):
        row = next(r for r in d["rows"]
                   if r.get("adjudicated_grade") == "street_only_unseated")
        row["seat"] = {**row["seat"], "id": "a_street_the_paper_did_not_print"}

    def a_face_firm_stops_saying_it_is_reconstruction(d):
        row = next(r for r in d["rows"]
                   if r.get("adjudicated_grade") == "street_only_unseated")
        row["tier"] = "inferred"

    def a_reconstructed_seat_grows_a_lot(d):
        row = pick("household", "division_band")(d)
        row["seat"] = {**row["seat"], "lot": "blk_16_lot_7"}

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
    fires("a band that moves a household out of its own division", a_band_moves_a_household)
    fires("a band citing a clause the policy does not hold",
          a_band_cites_a_clause_the_policy_lacks)
    fires("a band that stops calling itself reconstruction", a_band_loses_its_tier)
    fires("a reconstructed band with no seed", a_band_loses_its_seed)
    fires("a household whose record names a division and is left owed",
          a_household_in_a_division_is_left_owed)
    fires("a household banded into a division its record does not name",
          an_unplaced_household_is_banded)
    fires("a face seat moved off the street the paper printed", a_face_firm_moves_street)
    fires("a roofless face seat that stops saying it is reconstruction",
          a_face_firm_stops_saying_it_is_reconstruction)
    fires("a reconstructed seat that grows a lot", a_reconstructed_seat_grows_a_lot)

    if faults:
        print("SELF-TEST FAILED — these assertions did not fire: " + ", ".join(faults))
        return 1
    print("all 23 assertions fire when broken")
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
