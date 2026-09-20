#!/usr/bin/env python3
"""THE 1835 BUSINESS RECONSTRUCTION — one writer, five groups, one quota.

    python3 tools/reconstruct_businesses_1835.py --group stores_and_provisions --build
    python3 tools/reconstruct_businesses_1835.py --check          # every built group
    python3 tools/reconstruct_businesses_1835.py --self-test

T-1184 builds this and T-1185 … T-1188 reuse it. The five reconstruction tickets of the
business band differ in exactly one thing — WHICH ROWS OF THE ORDER BOOK THEY OWN — and the
order book already says which, on every bucket, in `owning_ticket`. So a group here is a key
and a ticket number, the classes are READ from the book rather than restated, and a ticket
that re-cuts the book moves this tool's quota with it. Nothing about the quota lives in this
file; what lives here is the rule for turning a quota row into a house of trade.

WHAT A RECONSTRUCTED BUSINESS IS, AND WHAT IT IS NOT. It is a firm the December 1835 State
census counts and the newspaper register does not hold: the census prints four druggists and
the register carries two, so the town of 1 July 1835 had two apothecaries' shops nobody
wrote the name of. This tool writes those two. It is NOT a reading, it carries no source, it
may never be promoted, and every field on it names the rule that drew it and the evidence
that would retire it — `reconstruction.basis`, `reconstruction.seed`, `replaceable_by`.

THE PROPRIETOR IS ADOPTED, NEVER MINTED. `tools/reconstruct_residents_1835.py` is the one
writer of a person graded `reconstructed` and this tool is deliberately not a second one.
The resident band's `trade_households` stage (T-1347, of T-1173) already drew heads at the
trades the town was short of, and every one of those cards says so itself: "the business
band (T-1184 … T-1188) ADOPTS these heads as its proprietors rather than minting its own, so
the two bands fill one quota." A group whose class orders more houses than that band drew
heads for is REFUSED here rather than quietly under-filled — the shortfall is the resident
band's to draw, and a business tool that minted its own proprietor would order the same
person twice.

THE STYLE IS PERIOD OR IT IS NOTHING. `docs/RESEARCH/business-naming-1835.md` is the guide,
written from the 196 firm styles the register prints, and STYLES below is its executable
half. A reconstructed firm may not reuse an attested firm style, an attested house's name,
or an attested proprietor's name; `--check` refuses each.

THE LOCATION IS A LIMIT. Every record here takes a `street_only` location on a face the
placement rule allows for its class and division — no lot, no roof, no coordinate. T-1195
writes the placement policy properly and T-1199 seats these houses on the lot grid; until
then the face is a deal off a stated rule and the `limit_reason` says exactly that.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compile_businesses import (  # noqa: E402
    derive_proprietor_community,
    person_communities,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESIDENTS = DATA / "residents"
TRADE_HOUSEHOLDS = RESIDENTS / "reconstructed_trades"
AUTHORED = DATA / "businesses" / "authored"
ORDER_BOOK = DATA / "reconstruction" / "1835_reconstruction_order_book.json"
STREETS = DATA / "streets" / "1835.json"
LEDGER = DATA / "reconstruction" / "1835_business_reconstruction.json"
LODGING_MODEL = DATA / "reconstruction" / "1835_lodging_model.json"
LODGERS = DATA / "residents" / "lodgers"

PROGRAMME = "chicago_1835_business_reconstruction"
SCENE_DATE = "1835-07-01"


# ------------------------------------------------------------------- the five groups

GROUPS = {
    "stores_and_provisions": {
        "ticket": "T-1184",
        "title": "stores, book stores and the drug and provision trades",
    },
    "mechanics_shops": {"ticket": "T-1185", "title": "the mechanics' shops"},
    # T-1186 split on 2026-09-20: T-1418 owns the two census rows this group fills
    # (the professions), T-1419 the services the census enumerates nowhere.
    "professions_and_services": {"ticket": "T-1418", "title": "the professions"},
    "lodging_river_and_transport": {
        "ticket": "T-1187", "title": "lodging, the river and transport"},
    "civic_church_school_and_press": {
        "ticket": "T-1188", "title": "the civic, church, school and press establishments"},
}


# ------------------------------------------------- the second quota: a roof, not a count
#
# THE ORDER BOOK CANNOT ORDER A BOARDING HOUSE, and that is a property of the census
# rather than a hole in the book. `business_buckets` in tools/build_order_book_1835.py
# orders against PRINTED COUNTS or not at all, and the December 1835 State census
# enumerates taverns — eight of them, all attested, and the town keeps eight — while it
# never enumerates a boarding house at all. So no shortfall of this class can ever be
# counted, and the first quota has nothing to say about the one part of the lodging
# economy this town demonstrably had: the 1840 schedule's 8.2 people to a dwelling.
#
# What this project HAS already committed is the BUILDING. Five boarding houses stand in
# `data/structures/`; the lodging model (T-1370) apportioned each of them beds out of a
# bracket the town model owns; the lodgers stage (T-1371) put people in those beds and
# named a keeper for every reconstructed one. A house with beds, lodgers and a keeper and
# no firm behind it is an establishment the business layer cannot see — it does not appear
# in the Businesses view, its building card names no trade, and the keeper's own card can
# say she keeps a boarding house while nothing in the town holds one.
#
# So the roof is the quota. One record per STANDING reconstructed lodging roof of the
# class below, and never one for a slot the roof programme has scheduled and not built:
# the 37 unbuilt boarding houses are 333 beds with no roof over them (T-1196 re-derives
# the programme, T-1409 raises the houses) and a firm in a building site is a fiction of a
# different kind. The named houses are not touched either — who kept the New York House in
# 1835 is a research question, and the lodgers stage refused to answer it for exactly this
# reason; their keepers come from the register through T-1404.
ROOF_QUOTA = {
    "lodging_river_and_transport": {
        "ticket": "T-1408",
        "lodging_class": "boarding_house",
        # THE CENSUS CLASS A BOARDING HOUSE TAKES, and why it is not its own. `type` is the
        # ONE taxonomy — the December 1835 State census's classes — so that a business
        # counts against the census without a second crosswalk. That census has no boarding
        # -house line, and `other` is precisely its bucket for a class it never put a figure
        # against. Typing these houses `tavern` would spend the eight-tavern count the
        # register already fills; minting a class the census never printed would put a
        # nineteenth line in a taxonomy whose whole job is to match an eighteen-line
        # document. The trade is carried in `trade` and `occupation`, which are free of it.
        "type": "other",
        "trade": "boarding house",
        "occupation": "boarding_house_keeper",
    },
}

# THE KEEPER'S POSSESSIVE, form 5 of docs/RESEARCH/business-naming-1835.md, which is the
# form this town's own lodging houses take: *Miss Bayne's Boarding and Day School* in the
# register, *Rufus Brown's Boarding House* on the one boarding house the structure layer
# names. NO HONORIFIC IS DEALT. Three of the four keepers the lodgers stage drew are women,
# and `Mrs.` would assert a marriage, `Miss` a want of one; the cards carry neither, because
# the stage minted them as solitary keepers and nothing in the layer says which. A style
# that reached for the honorific would be inventing a marital status to make a sign read
# well — so the possessive stands on the name alone, which asserts only what the card holds.
ROOF_STYLES = {
    "boarding_house": {
        "forms": [
            ("{given} {surname}'s boarding house",
             "the possessive in full, as the structure layer's own *Rufus Brown's Boarding "
             "House* prints it"),
            ("{surname}'s boarding house",
             "the possessive with the forename cut, as *Ingersoll's tavern stand* and "
             "*Stuart's confectionary and perfumery* print it in the register"),
        ],
    },
}


# THE TRADES A CENSUS CLASS IS KEPT BY, in the resident layer's own occupation vocabulary.
# ONE ROW PER CLASS THIS TOOL HAS BEEN ASKED TO BUILD, and no further: a class whose group
# has not run yet is not guessed at here, because deciding that a `refectory_keeper` keeps a
# tavern rather than a store is T-1187's ruling to make and not T-1184's. A bucket whose
# class is missing from this table is refused by name, with the ticket that owes the row.
TRADE_CLASS = {
    "druggist": ["druggist"],
    "store": ["dry_goods_merchant", "grocer", "hardware_merchant", "merchant"],
    "book_store": [],
    # THE TWO CLASSES THE CENSUS COUNTS IN MEN take exactly one trade each, and that is
    # the point of them: "twenty-two lawyers" is twenty-two men, so one drawn head is one
    # office and the person count and the establishment count are the same number. A
    # second trade folded in here would break that identity.
    "lawyer": ["attorney"],
    "physician": ["physician"],
}

# THE FACE A CLASS TAKES, by division, in the order a seeded deal reads them. From the
# register's own distribution of the 61 street-only businesses it prints, which puts the
# retail trades on South Water, Lake and Dearborn in the south division, on the Wolcott–
# Kinzie core and the North Water bank in the north, and on the Canal Street approach and
# West Water in the west. T-1195 writes the placement policy with its evidence and re-cuts
# this; until it does, the rule is this table and the record says so.
FACES = {
    "druggist": {
        "south": ["lake", "south_water", "dearborn"],
        "north": ["kinzie", "north_water"],
        "west": ["canal", "west_water"],
    },
    "store": {
        "south": ["south_water", "lake", "dearborn"],
        "north": ["kinzie", "north_water"],
        "west": ["canal", "west_water"],
    },
    "book_store": {
        "south": ["lake", "dearborn"],
        "north": ["kinzie"],
        "west": ["canal"],
    },
    # THE PROFESSIONS SIT WHERE THE REGISTER ALREADY PUTS THEM. Of the law offices the
    # register resolves a place for, South Water carries Collins & Caton, J. Curtiss and
    # J. D. Caton; Dearborn carries G. Spring, H. C. Bennett and both printings of S.
    # Abell; Lake carries Russell E. Heacock and John Dean Caton. Those three faces, in
    # that order of weight, are the south-division rule.
    "lawyer": {
        "south": ["south_water", "dearborn", "lake"],
        "north": ["kinzie", "north_water"],
        "west": ["canal", "west_water"],
    },
    # AND BOTH PLACED PHYSICIANS ARE ON LAKE STREET: Dr. J. H. Barnard against the New
    # York House and Dr. W. G. Austin "on Lake Street, near the post office" (the American
    # of 8 August 1835). Lake leads, and the two business streets either side of it follow
    # it rather than a rule of their own.
    "physician": {
        "south": ["lake", "south_water", "dearborn"],
        "north": ["kinzie", "north_water"],
        "west": ["canal", "west_water"],
    },
}

# THE PERIOD FORMS, each one attested in the register, with the attested house that carries
# it named beside it so a reader can check the form against a printing. `docs/RESEARCH/
# business-naming-1835.md` is the argument; this is the half a program can run.
STYLES = {
    "druggist": {
        "forms": [
            ("{initial}. {surname}, {goods}",
             "the form 'Frederick Thomas, drugs and paints' prints, with the forename cut to "
             "an initial as 'J. B. Brown, Dearborn Street grocery' and 'S. Foot' do"),
            ("{given} {surname}, {goods}",
             "the form 'Frederick Thomas, drugs and paints' and 'William F. Lyon, Wholesale "
             "Grocery Store' print in full"),
        ],
        "goods": [
            ("drugs and medicines", "Philo Carpenter's own trade line in the register"),
            ("drugs, medicines and dye stuffs",
             "the goods line of Frederick Thomas and Philo Carpenter, cut to the three heads "
             "both of them advertise"),
        ],
        "trade": "druggist and apothecary",
        "occupation": "druggist",
    },
    "store": {
        "forms": [
            ("{initial}. {surname}, {goods}",
             "the form 'B. Jones, grocery and provision store' prints"),
            ("{given} {surname}, {goods}",
             "the form 'William F. Lyon, Wholesale Grocery Store' prints"),
        ],
        "goods": [
            ("dry goods, groceries and hardware",
             "the goods line P. Pruyne & Co. and Clark, Filer & Co. advertise"),
            ("grocery and provision store", "B. Jones's own trade line in the register"),
        ],
        "trade": "store",
        "occupation": None,
    },
    "lawyer": {
        "forms": [
            ("{initial}. {surname}, {goods}",
             "the form 'J. Curtiss, Attorney and Counsellor at Law', 'R. Stewart, attorney' "
             "and 'S. Abell, attorney and counsellor' print — an initial, the surname, and "
             "the practice's own line"),
            ("{given} {surname}, {goods}",
             "the form 'Ebenezer S. More, attorney at law' prints in full"),
        ],
        # EVERY LINE HERE IS A LINE THE REGISTER PRINTS, verbatim, and there are three of
        # them because the town's own notices carry three. Nothing is composed.
        "goods": [
            ("attorney at law",
             "the trade line of Ebenezer S. More and of R. Stewart in the register"),
            ("attorney and counsellor at law",
             "the trade line of Edward W. Casey and James Grant"),
            ("attorney and counsellor at law, and solicitor in chancery",
             "the fullest of the three, and the commonest: G. Spring, H. C. Bennett, J. "
             "Curtiss, Henry Moore and John Dean Caton all print it"),
        ],
        "trade": "attorney and counsellor at law",
        "occupation": "attorney",
    },
    "physician": {
        # THE DOCTOR'S TITLE IS THE FIRM STYLE, and both of the register's physicians carry
        # it: 'Dr. J. H. Barnard' sets the title, initials and surname and no trade at all,
        # and 'Dr. W. G. Austin, botanic physician' sets the same with a line after it.
        "forms": [
            ("Dr. {initial}. {surname}",
             "the form 'Dr. J. H. Barnard' prints — the title, the initials and the surname, "
             "and no trade line"),
            ("Dr. {initial}. {surname}, {goods}",
             "the form 'Dr. W. G. Austin, botanic physician' prints — the same, with the "
             "practice's line after it"),
        ],
        # ONE LINE, AND DELIBERATELY. Austin's own line names the BOTANIC system, which is a
        # medical school a reconstructed man may not be dealt into: the register knows what
        # Austin practised because Austin advertised it, and nothing knows it of a man
        # nobody wrote down. 'Physician' is the register's other printed line and it claims
        # only the trade the census counted.
        "goods": [
            ("physician", "the trade line the register prints under Dr. J. H. Barnard"),
        ],
        "trade": "physician",
        "occupation": "physician",
    },
}


# ------------------------------------------------------------------------- the plumbing

def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def draw(seed, options):
    """The seed rule of the reconstruction programme, unchanged: a STRING a reader can
    retype, hashed with blake2s and read big-endian, indexing a list nobody reorders."""
    digest = hashlib.blake2s(seed.encode("utf-8"), digest_size=8).digest()
    return options[int.from_bytes(digest, "big") % len(options)]


def order_book_buckets(ticket, book=None):
    """The business rows of the order book this ticket owns, in the book's own order."""
    book = book or load_json(ORDER_BOOK)
    family = next(f for f in book["bucket_families"] if f["key"] == "businesses")
    return [b for b in family["buckets"] if b.get("owning_ticket") == ticket]


def trade_heads(root=None):
    """Every reconstructed trade head the resident band drew, by trade, in slot order."""
    root = Path(root or TRADE_HOUSEHOLDS)
    heads = {}
    for path in sorted(root.glob("*.json")):
        doc = load_json(path)
        block = doc.get("trade_household") or {}
        head = next((p for p in doc.get("persons", []) if p.get("id") == doc.get("head")), None)
        if not block.get("trade") or head is None:
            continue
        heads.setdefault(block["trade"], []).append({
            "household_id": doc["id"],
            "person_id": head["id"],
            "name": head["name"],
            "division": doc["division"],
            "slot": block["slot"],
            "trade": block["trade"],
            "community": (head.get("reconstruction") or {}).get("community"),
        })
    for rows in heads.values():
        rows.sort(key=lambda r: r["slot"])
    return heads


def attested_strings(businesses_dir=None):
    """Every firm style, house name and proprietor name the register already prints —
    the collision set an invention may not walk into."""
    root = Path(businesses_dir or (DATA / "businesses"))
    names, people = set(), set()
    for path in sorted(root.glob("biz_*.json")):
        doc = load_json(path)
        names.add(doc["name"].strip().lower())
        for style in doc.get("firm_styles") or []:
            names.add(style.strip().lower())
        for field in ("proprietors", "partners", "staff"):
            for person in doc.get(field) or []:
                people.add((person.get("name") or "").strip().lower())
    return names, people


# ------------------------------------------------------------------- building a record

def initials(name):
    parts = [p for p in name.split() if p]
    return parts[0], parts[-1]


def firm_style(spec, head, seed):
    given, surname = initials(head["name"])
    form, form_basis = draw(seed + ":firm_form", spec["forms"])
    goods, goods_basis = draw(seed + ":goods_line", spec["goods"])
    name = form.format(initial=given[0], given=given, surname=surname, goods=goods)
    return name, goods, ("The style is dealt on the seed printed beside it from the period "
                         "forms the register itself carries: %s. The goods line is %s."
                         % (form_basis, goods_basis))


def record_for(group, bucket, head, ordinal, communities, streets):
    cls = bucket["axes"]["class"]
    spec = STYLES[cls]
    slot = "%s:%s:%03d" % (group, bucket["key"], ordinal)
    name, goods, style_basis = firm_style(spec, head, slot)
    _, surname = initials(head["name"])
    faces = FACES[cls][head["division"]]
    face = draw(slot + ":street_face", faces)

    proprietor = {
        "name": head["name"],
        "person_id": head["person_id"],
        "register_person_id": None,
        "role": "proprietor",
        "from": None,
        "to": None,
        "tier": "reconstructed",
        "basis": (
            "ADOPTED, NOT MINTED. %s is the reconstructed trade head the resident band's "
            "`trade_households` stage drew at %s in the %s division (slot %s), and that card "
            "says itself that the business band adopts these heads rather than minting its "
            "own. One quota, filled once: this house is the establishment that head keeps."
            % (head["name"], head["trade"], head["division"], head["slot"])),
        "source_id": None,
        "claim_ids": [],
    }

    record = {
        "id": "rcb_%s_%s" % (surname.lower().replace("'", "").replace(".", ""), cls),
        "register_id": None,
        "name": name,
        "provenance": "reconstructed",
        "type": [cls],
        "trade": spec["trade"],
        "occupation": spec["occupation"],
        "goods": [goods],
        "firm_styles": [],
        "proprietors": [proprietor],
        "partners": [],
        "staff": [],
        "locations": [{
            "kind": "street_only",
            "structure_id": None,
            "street_id": face,
            "face": None,
            "primary": True,
            "from": None,
            "to": None,
            "tier": "reconstructed",
            "basis": (
                "A FACE, NOT A PREMISES. The placement rule for a %s kept by a %s-division "
                "household deals this house onto %s; the face is drawn on the seed printed in "
                "`reconstruction.seed` from the faces that rule allows, and no lot, roof or "
                "coordinate is claimed. T-1195 writes the placement policy with its evidence "
                "and T-1199 seats this house on the lot grid."
                % (cls, head["division"], streets.get(face, face))),
            "limit_reason": (
                "No source places this house, because no source names it: it exists because "
                "the December 1835 State census counts more of its class than the register "
                "holds. The street is the reconstruction's own deal and stops there."),
        }],
        "dates": {
            "opened": None,
            "closed": None,
            "precision": "unbounded",
            "tier": "reconstructed",
            "basis": (
                "NOTHING DATES THIS HOUSE. The census that orders it was taken in December "
                "1835 and counts a standing trade, not an opening; the record claims that the "
                "house was trading on %s and nothing about either end." % SCENE_DATE),
        },
        "evidence": {},
        "present_at_scene_date": True,
        "exclusion": None,
        "exclusion_note": None,
        "proprietor_community": derive_proprietor_community(
            [proprietor], [], communities),
        "customers": [],
        "sources": [],
        "claim_ids": [],
        "liberties": {"survival_required": False, "backdating_required": False},
        "review_required": False,
        "replaceable_by": (
            "A register, directory or deed naming a real house of this class in the %s "
            "division in 1835 — that house takes this slot and this record is withdrawn."
            % head["division"]),
        "reconstruction": {
            "programme": PROGRAMME,
            "group": group,
            "ticket": GROUPS[group]["ticket"],
            "bucket": bucket["key"],
            "slot": slot,
            "seed": slot,
            "basis": {
                "kind": "model",
                "id": "1835_reconstruction_order_book",
                "note": ("%s. The book leaves %d of this class to reconstruct and this is "
                         "one of them. %s"
                         % (bucket["basis"].rstrip("."), bucket["to_reconstruct"],
                            style_basis)),
            },
            "withdrawn_if": (
                "a source naming a real house of this class, or a re-cut of the order book "
                "that no longer orders this bucket; the retirement runs through --build, "
                "never by hand"),
        },
    }
    return record


# ------------------------------------------------------- the roofs, and who keeps them

def lodging_places(model=None):
    """Every lodging place the model holds, with its beds — the model's own order."""
    model = model or load_json(LODGING_MODEL)
    return list(model["places"])


def roof_keepers(root=None):
    """`{place: keeper}` for the lodging households the lodgers stage wrote a head on.

    Read off the households rather than off that stage's ledger, for the reason the
    liberty counter reads the business records rather than the business index: the
    ledger is a derivation of these cards, and adopting a person out of a derivation
    would be adopting a summary of them.
    """
    root = Path(root or LODGERS)
    out = {}
    for path in sorted(root.glob("*.json")):
        doc = load_json(path)
        block = doc.get("lodging_household") or {}
        head = next((p for p in doc.get("persons", []) if p.get("id") == doc.get("head")), None)
        if not block.get("place") or head is None:
            continue
        out[block["place"]] = {
            "household_id": doc["id"],
            "person_id": head["id"],
            "name": head["name"],
            "sex": head.get("sex"),
            "division": doc["division"],
            "community": (head.get("reconstruction") or {}).get("community"),
        }
    return out


def roof_buckets(group, model=None, keepers=None):
    """The standing reconstructed lodging roofs this group owes a firm, by division.

    Shaped like an order-book bucket so the build loop reads one list, and carrying its
    places so the record can name the roof that bought it. A roof whose keeper the lodgers
    stage never named is NOT ordered: this tool adopts a keeper and never mints one, and a
    house with nobody to keep it is a shortfall stated rather than a person invented.
    """
    spec = ROOF_QUOTA.get(group)
    if spec is None:
        return []
    keepers = keepers if keepers is not None else roof_keepers()
    by_division, unkept = {}, []
    for place in lodging_places(model):
        if place["class"] != spec["lodging_class"] or place["standing"] != "reconstructed":
            continue
        keeper = keepers.get(place["id"])
        if keeper is None:
            unkept.append(place["id"])
            continue
        by_division.setdefault(keeper["division"], []).append(dict(place, keeper=keeper))
    buckets = []
    for division in sorted(by_division):
        places = by_division[division]
        buckets.append({
            "key": "lodging/%s/%s" % (spec["lodging_class"], division),
            "axes": {"class": spec["lodging_class"], "division": division},
            "to_reconstruct": len(places),
            "owning_ticket": spec["ticket"],
            "places": places,
            "unkept": sorted(unkept),
            "basis": ("the lodging model gives %d standing %s roof(s) in the %s division "
                      "their beds and the lodgers stage named a keeper for each"
                      % (len(places), spec["lodging_class"].replace("_", " "), division)),
        })
    return buckets


def roof_style(place, seed):
    given, surname = initials(place["keeper"]["name"])
    form, form_basis = draw(seed + ":firm_form", ROOF_STYLES[place["class"]]["forms"])
    return form.format(initial=given[0], given=given, surname=surname), form_basis


def record_for_roof(group, bucket, place, ordinal, communities):
    spec = ROOF_QUOTA[group]
    keeper = place["keeper"]
    slot = "%s:%s:%03d" % (group, bucket["key"], ordinal)
    name, style_basis = roof_style(place, slot)
    _, surname = initials(keeper["name"])

    proprietor = {
        "name": keeper["name"],
        "person_id": keeper["person_id"],
        "register_person_id": None,
        "role": "proprietor",
        "from": None,
        "to": None,
        "tier": "reconstructed",
        "basis": (
            "ADOPTED, NOT MINTED. %s is the keeper the lodgers stage (T-1371) drew for this "
            "house and printed in data/reconstruction/1835_lodgers_seated.json § keepers; "
            "that card reads the trade off the building it stands in and heads %s. One "
            "quota, filled once: this record is the house they keep, not a second person."
            % (keeper["name"], keeper["household_id"])),
        "source_id": None,
        "claim_ids": [],
    }

    record = {
        "id": "rcb_%s_boarding_house" % surname.lower().replace("'", "").replace(".", ""),
        "register_id": None,
        "name": name,
        "provenance": "reconstructed",
        "type": [spec["type"]],
        "trade": spec["trade"],
        "occupation": spec["occupation"],
        "goods": [],
        "firm_styles": [],
        "proprietors": [proprietor],
        "partners": [],
        "staff": [],
        "locations": [{
            "kind": "premises",
            "structure_id": place["id"],
            "street_id": None,
            "face": None,
            "primary": True,
            "from": None,
            "to": None,
            "tier": "reconstructed",
            "basis": (
                "THE ROOF IS THE PREMISES, and it is the one thing here that was not dealt. "
                "This firm exists because %s stands in data/structures/ with %d ordinary-"
                "night beds in it; the building came first and the house of trade is what "
                "the building was missing. No street is claimed beyond the one the roof "
                "already stands on, and no coordinate is written here at all."
                % (place["id"], place["beds_ordinary"])),
            "limit_reason": None,
        }],
        "dates": {
            "opened": None,
            "closed": None,
            "precision": "unbounded",
            "tier": "reconstructed",
            "basis": (
                "NOTHING DATES THIS HOUSE. The roof it occupies is an anonymous count-unit "
                "dated to the year and to nothing narrower, and a keeping is not an "
                "opening; the record claims that the house was letting beds on %s and "
                "nothing about either end." % SCENE_DATE),
        },
        "evidence": {},
        "present_at_scene_date": True,
        "exclusion": None,
        "exclusion_note": None,
        "proprietor_community": derive_proprietor_community([proprietor], [], communities),
        "customers": [],
        "sources": [],
        "claim_ids": [],
        "liberties": {"survival_required": False, "backdating_required": False},
        "review_required": False,
        "replaceable_by": (
            "A source naming whoever kept a boarding house in the %s division in 1835 — "
            "that keeper takes this roof and this record is withdrawn with the drawn one."
            % bucket["axes"]["division"]),
        "reconstruction": {
            "programme": PROGRAMME,
            "group": group,
            "ticket": spec["ticket"],
            "roof": {
                "structure_id": place["id"],
                "class": place["class"],
                "beds_ordinary": place["beds_ordinary"],
                "keeper_person_id": keeper["person_id"],
                "keeper_household_id": keeper["household_id"],
                "note": (
                    "A STANDING ROOF, NOT A SHORTFALL. The December 1835 State census "
                    "enumerates taverns and never boarding houses, so the order book holds "
                    "no bucket of this class to point at and no count of it is short. What "
                    "is committed is the building: %s stands, the lodging model apportioned "
                    "it %d ordinary-night beds out of a bracket the town model owns, and "
                    "the lodgers stage put people in them and named %s their keeper. The "
                    "firm is what was missing, and it is withdrawn with the roof."
                    % (place["id"], place["beds_ordinary"], keeper["name"])),
            },
            "seed": slot,
            "basis": {
                "kind": "model",
                "id": "1835_lodging_model",
                "note": ("%s. %s. The style is dealt on the seed printed beside it from the "
                         "keeper's possessive, form 5 of the naming guide: %s. No honorific "
                         "is dealt, because nothing on this keeper's card says whether they "
                         "were married, widowed or single and a sign that said so would be "
                         "inventing it."
                         % (bucket["basis"].rstrip("."),
                            ("the keeper is a woman" if keeper["sex"] == "female"
                             else "the keeper is a man" if keeper["sex"] == "male"
                             else "the keeper's sex is not stated"),
                            style_basis)),
            },
            "withdrawn_if": (
                "the retirement of the roof itself, a re-cut lodging model that gives this "
                "house no beds, or a source naming whoever really kept it; the retirement "
                "runs through --build, never by hand"),
        },
    }
    return record


# ------------------------------------------------------------------------ build / check

def build_group(group, communities=None, streets=None, heads=None, book=None):
    """Every record this group's order-book rows call for, in the book's own order."""
    communities = communities if communities is not None else person_communities()
    streets = streets if streets is not None else {
        s["id"]: s.get("name_1835") or s["id"] for s in load_json(STREETS)["streets"]}
    heads = heads if heads is not None else trade_heads()
    records, shortfalls = [], []
    taken = set()
    for bucket in order_book_buckets(GROUPS[group]["ticket"], book):
        owed = bucket["to_reconstruct"]
        if owed <= 0:
            continue
        cls = bucket["axes"]["class"]
        if cls not in TRADE_CLASS or cls not in STYLES:
            raise SystemExit(
                "the order book orders %d of class %r for %s and this tool carries no trade "
                "row or style for it. Add them to TRADE_CLASS and STYLES with the argument "
                "for the mapping, in the ticket that owns the bucket (%s) — a class guessed "
                "at by another group's ticket is a ruling made in the wrong place."
                % (owed, cls, group, bucket["owning_ticket"]))
        candidates = [h for trade in TRADE_CLASS[cls] for h in heads.get(trade, [])]
        candidates = sorted((h for h in candidates if h["person_id"] not in taken),
                            key=lambda h: h["slot"])
        if len(candidates) < owed:
            shortfalls.append((bucket["key"], owed, len(candidates)))
            continue
        for ordinal, head in enumerate(candidates[:owed], start=1):
            taken.add(head["person_id"])
            records.append(record_for(group, bucket, head, ordinal, communities, streets))
    if shortfalls:
        raise SystemExit(
            "the resident band has not drawn enough trade heads for %s:\n%s\n"
            "This tool ADOPTS heads and never mints one — minting here would order the same "
            "person twice. The shortfall is T-1173's to draw." % (group, "\n".join(
                "  %s orders %d and %d head(s) stand at its trades" % row for row in shortfalls)))
    # AND THE ROOFS THAT STAND. The second quota, in the same loop and on the same rules:
    # one record per standing lodging roof, a keeper adopted rather than minted, and a
    # premises location in the building that bought it.
    for bucket in roof_buckets(group):
        for ordinal, place in enumerate(bucket["places"], start=1):
            records.append(record_for_roof(group, bucket, place, ordinal, communities))
    records.sort(key=lambda r: r["id"])
    return records


def collisions(records, businesses_dir=None):
    """An invented style may not be a style the register already prints, and an invented
    house may not be two houses. The name of a real proprietor is checked too: this tool
    adopts a reconstructed person, so a style carrying a real person's name would be one."""
    names, people = attested_strings(businesses_dir)
    bad, seen, ids = [], set(), set()
    for record in records:
        key = record["name"].strip().lower()
        if key in names:
            bad.append("%s: the style %r is one the register already prints"
                       % (record["id"], record["name"]))
        if key in seen:
            bad.append("%s: two reconstructed houses trade under %r" % (record["id"], record["name"]))
        seen.add(key)
        # AND TWO HOUSES MAY NOT SHARE A FILE. The id is built from the keeper's surname and
        # the class, so two keepers of one trade who happen to share a surname would write
        # one record over the other and the build would quietly come out one house short —
        # a shortfall nothing states, which is the one kind this programme must not produce.
        if record["id"] in ids:
            bad.append("%s: two reconstructed houses claim this id; one would overwrite the "
                       "other and the town would be a house short with nothing saying so"
                       % record["id"])
        ids.add(record["id"])
        for person in record["proprietors"] + record["partners"] + record["staff"]:
            if (person["name"] or "").strip().lower() in people:
                bad.append("%s: %r is a name the register prints on a real house"
                           % (record["id"], person["name"]))
            if person["tier"] != "reconstructed":
                bad.append("%s: %r is graded %r on a reconstructed house"
                           % (record["id"], person["name"], person["tier"]))
        if record["sources"] or record["claim_ids"]:
            bad.append("%s: a reconstructed house cites a source" % record["id"])
    return bad


def lodging_table(built):
    """BEDS AGAINST KEEPERS: every lodging place that stands, and the firm behind it.

    The acceptance clause of T-1408, and the reason it is a TABLE rather than a number:
    a house is unkept for more than one reason and the reasons are not interchangeable.
    A reconstructed roof with no firm is this programme's debt. A documented house with no
    firm is a RESEARCH question — the lodgers stage refused to put a drawn proprietor
    inside the New York House and the Sauganash on exactly that ground, and so does this —
    and its keeper reaches the business layer through the register or not at all. The
    table states which, per house, so neither can hide inside the other's count.
    """
    # READ OFF DISK, NOT OFF THE BUILD. --build writes every record before it writes this
    # ledger, so disk is the complete picture and the build's own dict is not: a run that
    # rebuilds one group would otherwise print the other group's standing roofs as unkept.
    firms, seated = business_premises()
    keepers = roof_keepers()
    rows, owed = [], 0
    for place in lodging_places():
        firm = firms.get(place["id"]) or None
        register = sorted(set(seated.get(place["id"], [])))
        keeper = keepers.get(place["id"])
        if place["standing"] == "reconstructed":
            kept_by = "this programme" if firm else None
            if not firm:
                owed += 1
                why = ("NO FIRM. The lodgers stage named no keeper for this roof, so there "
                       "is nobody to adopt and this programme mints none."
                       if keeper is None else
                       "NO FIRM, AND THE KEEPER IS STANDING. This is this programme's debt.")
            else:
                why = None
        else:
            kept_by = "the register" if register else None
            why = (None if register else
                   "A DOCUMENTED HOUSE WITH NO FIRM IN THE REGISTER. Who kept it on the "
                   "scene date is a research question and not a draw; T-1404 raises the "
                   "attested keepers the sources do name, and a reconstructed proprietor "
                   "is never written into a documented building.")
        rows.append({
            "place": place["id"],
            "name": place["name"],
            "class": place["class"],
            "standing": place["standing"],
            "beds_ordinary": place["beds_ordinary"],
            "beds_crowded": place["beds_crowded"],
            "keeper_person": (keeper or {}).get("person_id"),
            "firm": firm,
            "businesses_in_the_register_at_this_roof": register,
            "kept_by": kept_by,
            "why_not": why,
        })
    return {
        "_doc": ("BEDS AGAINST KEEPERS. Every place data/reconstruction/"
                 "1835_lodging_model.json stands, and the house of trade behind it. "
                 "`kept_by` is null where there is none, and `why_not` says which kind of "
                 "absence it is."),
        "places": len(rows),
        "reconstructed_roofs_this_programme_owes_a_firm": owed,
        "rows": rows,
    }


def business_premises(businesses_dir=None):
    """`({roof: firm}, {structure: [register ids]})` — who is seated in which building.

    Two maps, because the two mean different things. The first is what THIS programme
    bought with a standing roof. The second is every other house of trade the layer seats
    in a building, which is what a documented lodging house's keeper would arrive as.
    Read off the records rather than off data/businesses/index.json, because the index is
    derived from them and this table is asked while a build is deciding what it will say.
    """
    root = Path(businesses_dir or (DATA / "businesses"))
    firms, seated = {}, {}
    for path in sorted(list(root.glob("biz_*.json")) + list((root / "authored").glob("*.json"))):
        doc = load_json(path)
        roof = (doc.get("reconstruction") or {}).get("roof") or {}
        if roof.get("structure_id"):
            firms[roof["structure_id"]] = doc["id"]
            continue
        for loc in doc.get("locations") or []:
            if loc.get("kind") == "premises" and loc.get("structure_id"):
                seated.setdefault(loc["structure_id"], []).append(doc["id"])
    return firms, seated


def ledger(built):
    """What was built, by group, class and street — the counts the ticket asks be printed."""
    streets = {s["id"]: s.get("name_1835") or s["id"] for s in load_json(STREETS)["streets"]}
    groups = {}
    for group, records in sorted(built.items()):
        by_class, by_street, by_roof = {}, {}, {}
        for record in records:
            by_class[record["type"][0]] = by_class.get(record["type"][0], 0) + 1
            # A HOUSE BOUGHT BY A ROOF HAS NO STREET TO COUNT, and it is not silently
            # dropped into a `null` row: it is counted by the building it stands in, which
            # is the stronger statement of the two. The street table stays the street table.
            face = record["locations"][0]["street_id"]
            if face is None:
                roof = record["locations"][0]["structure_id"]
                by_roof[roof] = by_roof.get(roof, 0) + 1
                continue
            label = streets.get(face, face)
            by_street[label] = by_street.get(label, 0) + 1
        groups[group] = {
            "ticket": GROUPS[group]["ticket"],
            "title": GROUPS[group]["title"],
            "records": len(records),
            "by_class": dict(sorted(by_class.items())),
            "by_street": dict(sorted(by_street.items())),
            "by_roof": dict(sorted(by_roof.items())),
            "ids": [r["id"] for r in records],
            "proprietors_adopted": [r["proprietors"][0]["person_id"] for r in records],
        }
    return {
        "_doc": ("DERIVED from the reconstruction order book and the resident band's trade "
                 "heads by tools/reconstruct_businesses_1835.py. Do not hand-edit: --check "
                 "re-derives this file and every record it counts, and tools/check.sh runs "
                 "it. The counts are the ticket's own acceptance — by class and by street."),
        "id": PROGRAMME,
        "target_date": SCENE_DATE,
        "written_by": "tools/reconstruct_businesses_1835.py",
        "quota": "data/reconstruction/1835_reconstruction_order_book.json → bucket_families[businesses]",
        "proprietors": ("ADOPTED from data/residents/reconstructed_trades/, never minted. "
                        "tools/reconstruct_residents_1835.py is the one writer of a person."),
        "style_guide": "docs/RESEARCH/business-naming-1835.md",
        "liberty": "docs/LIBERTIES.md § L254",
        "records": sum(len(r) for r in built.values()),
        "groups": groups,
        "lodging": lodging_table(built),
    }


def fills_for(built):
    """`{ticket: {bucket key: records}}` — this build's contribution to the order book."""
    out = {}
    for group, records in built.items():
        ticket = GROUPS[group]["ticket"]
        for record in records:
            # A HOUSE BOUGHT BY A ROOF FILLS NOTHING HERE, and that is not an omission: the
            # order book holds no bucket of its class to fill, which is the whole reason the
            # roof form exists. Carrying it would write a fill against a key the book does
            # not have, and the book's own --build would then be asked to count it.
            bucket = record["reconstruction"].get("bucket")
            if not bucket:
                continue
            out.setdefault(ticket, {})
            out[ticket][bucket] = out[ticket].get(bucket, 0) + 1
    return out


def write_fills(built):
    """Carry this build's fills into the order book and re-derive it.

    `filled` is A COUNTER A FILLER INCREMENTS, and the book's own --build refuses an
    overfilled bucket — so the quota the ticket says these houses may not exceed is
    enforced by the book as well as by the loop above. A group that built nothing still
    clears its own rows, which is how a re-cut that drops a bucket retires its houses.
    """
    import build_order_book_1835 as order_book

    book = load_json(ORDER_BOOK)
    mine = fills_for(built)
    tickets = {GROUPS[g]["ticket"] for g in built}
    kept = [f for f in book.get("fills", []) if f.get("ticket") not in tickets]
    for ticket, buckets in sorted(mine.items()):
        group = next(g for g, spec in GROUPS.items() if spec["ticket"] == ticket)
        kept += [{"bucket": key, "ticket": ticket, "stage": group, "records": n,
                  "by": "tools/reconstruct_businesses_1835.py --build"}
                 for key, n in sorted(buckets.items())]
    # APPENDED, NEVER RE-SORTED. The ledger is in the order the stages filled it and two
    # runs rewriting it whole would collide on every line of a file neither of them changed.
    book["fills"] = kept
    with open(ORDER_BOOK, "w", encoding="utf-8") as handle:
        json.dump(book, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    order_book.cmd_build()


def write(docs, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(docs, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def built_groups():
    """The groups that have records on disk — the ones --check must re-derive."""
    live = set()
    for path in sorted(AUTHORED.glob("rcb_*.json")):
        block = load_json(path).get("reconstruction") or {}
        if block.get("group") in GROUPS:
            live.add(block["group"])
    return sorted(live)


def build(groups):
    built = {}
    for group in groups:
        records = build_group(group)
        bad = collisions(records)
        if bad:
            raise SystemExit("\n".join(["the build refuses itself:"] + ["  " + b for b in bad]))
        built[group] = records
    AUTHORED.mkdir(parents=True, exist_ok=True)
    for group, records in built.items():
        for record in records:
            write(record, AUTHORED / ("%s.json" % record["id"]))
    for path in sorted(AUTHORED.glob("rcb_*.json")):
        block = load_json(path).get("reconstruction") or {}
        if block.get("group") in built and path.stem not in {
                r["id"] for r in built[block["group"]]}:
            path.unlink()
    # THE LEDGER IS THE WHOLE LAYER, NOT THIS RUN. A --build takes one group, because a
    # group is one ticket's quota — but the ledger counts every reconstructed house the
    # town carries, so a group this run did not touch is RE-DERIVED here rather than
    # written empty. It was written empty until T-1408, and nobody could see it while one
    # group existed: the second group's first build blanked the first group's counts and
    # --check then reported the ledger as a hand edit, naming the wrong file and the wrong
    # fault. A ledger that forgets a group when another is rebuilt is not a ledger.
    whole = {g: build_group(g) for g in built_groups() if g not in built}
    whole.update(built)
    write(ledger(whole), LEDGER)
    write_fills(built)
    for group, records in sorted(built.items()):
        print("%s (%s): %d reconstructed business record(s)"
              % (group, GROUPS[group]["ticket"], len(records)))
        for record in records:
            print("   %-28s %-12s %s" % (record["id"], record["type"][0], record["name"]))
    return 0


def check(groups=None):
    groups = groups or built_groups()
    if not groups:
        print("OK: no group of the business reconstruction has been built yet")
        return 0
    bad = []
    built = {}
    for group in groups:
        records = build_group(group)
        built[group] = records
        bad += collisions(records)
        on_disk = {p.stem for p in AUTHORED.glob("rcb_*.json")
                   if (load_json(p).get("reconstruction") or {}).get("group") == group}
        want = {r["id"] for r in records}
        for extra in sorted(on_disk - want):
            bad.append("%s: on disk and the order book does not order it" % extra)
        for missing in sorted(want - on_disk):
            bad.append("%s: the order book orders it and it is not on disk" % missing)
        for record in records:
            path = AUTHORED / ("%s.json" % record["id"])
            if path.exists() and load_json(path) != record:
                bad.append("%s: does not re-derive from its seeds — hand-edited?" % record["id"])
    # AND THE ORDER BOOK'S COUNTER AGREES. `filled` is carried rather than re-derived, so
    # a build that wrote records and did not carry its fill would leave the book reading a
    # quota it had already spent — and the book's overfill gate reading the wrong number.
    tickets = {GROUPS[g]["ticket"] for g in groups}
    book_fills = {}
    for fill in load_json(ORDER_BOOK).get("fills", []):
        if (fill.get("by", "").startswith("tools/reconstruct_businesses_1835.py")
                and fill.get("ticket") in tickets):
            book_fills.setdefault(fill["ticket"], {})[fill["bucket"]] = int(fill["records"])
    if book_fills != fills_for(built):
        bad.append("the order book's fills for %s are not what a rebuild counts: %r against %r"
                   % (", ".join(sorted(tickets)), book_fills, fills_for(built)))

    want_ledger = ledger(built)
    if not LEDGER.exists():
        bad.append("%s is missing — run --build" % LEDGER.relative_to(ROOT))
    elif load_json(LEDGER) != want_ledger:
        bad.append("%s does not match a rebuild" % LEDGER.relative_to(ROOT))
    if bad:
        print("\n".join(["the business reconstruction does not re-derive:"]
                        + ["  " + b for b in bad]))
        return 1
    print("OK: %d reconstructed business record(s) over %d group(s) re-derive from their seeds"
          % (sum(len(r) for r in built.values()), len(built)))
    return 0


# ------------------------------------------------------------------------- the self-test

def self_test():
    """Every refusal above, fired once."""
    failures = []

    def expect(name, fn, needle):
        try:
            fn()
        except SystemExit as exc:
            if needle in str(exc):
                return
            failures.append("%s: refused for the wrong reason: %s" % (name, exc))
            return
        failures.append("%s: was not refused" % name)

    book = load_json(ORDER_BOOK)
    communities = person_communities()
    streets = {s["id"]: s.get("name_1835") or s["id"] for s in load_json(STREETS)["streets"]}
    heads = trade_heads()

    # 1. A class the tool carries no style or trade row for is refused by name.
    fake = json.loads(json.dumps(book))
    family = next(f for f in fake["bucket_families"] if f["key"] == "businesses")
    family["buckets"].append({
        "key": "businesses/lottery_office", "axes": {"class": "lottery_office"},
        "target": 1, "known": 0, "to_reconstruct": 1, "filled": 0,
        "owning_ticket": "T-1184", "basis": "a fixture"})
    expect("an unmapped class",
           lambda: build_group("stores_and_provisions", communities, streets, heads, fake),
           "carries no trade row or style")

    # 2. A quota the resident band has no heads for is refused, never under-filled.
    greedy = json.loads(json.dumps(book))
    family = next(f for f in greedy["bucket_families"] if f["key"] == "businesses")
    for bucket in family["buckets"]:
        if bucket["key"] == "businesses/druggist":
            bucket["to_reconstruct"] = 99
    expect("a quota past the heads drawn",
           lambda: build_group("stores_and_provisions", communities, streets, heads, greedy),
           "has not drawn enough trade heads")

    # 3. A style the register already prints is refused.
    records = build_group("stores_and_provisions", communities, streets, heads)
    clash = json.loads(json.dumps(records))
    clash[0]["name"] = "Philo Carpenter"
    bad = collisions(clash)
    if not any("already prints" in b for b in bad):
        failures.append("an attested firm style was not refused")

    # 4. A reconstructed house that cites a source is refused.
    cited = json.loads(json.dumps(records))
    cited[0]["sources"] = ["chicago_newspapers_1833_1835"]
    if not any("cites a source" in b for b in collisions(cited)):
        failures.append("a reconstructed house citing a source was not refused")

    # 5. Two houses under one style are refused.
    twinned = json.loads(json.dumps(records)) * 2
    if not any("two reconstructed houses" in b for b in collisions(twinned)):
        failures.append("a duplicated style was not refused")

    # 6. The draw is a function of the seed string and nothing else.
    again = build_group("stores_and_provisions", communities, streets, heads)
    if again != records:
        failures.append("two builds of one group differ")

    # 7. Every proprietor is a person the resident layer holds, and is reconstructed.
    ids = {h["person_id"] for rows in heads.values() for h in rows}
    for record in records:
        for person in record["proprietors"]:
            if person["person_id"] not in ids:
                failures.append("%s: proprietor %s is not an adopted trade head"
                                % (record["id"], person["person_id"]))

    # 8. Two houses may not claim one id — one would overwrite the other on disk and the
    #    town would come out a house short with nothing saying so.
    same_id = json.loads(json.dumps(records))[:1] * 2
    same_id[1]["name"] = same_id[1]["name"] + " the second"
    if not any("claim this id" in b for b in collisions(same_id)):
        failures.append("two houses sharing an id were not refused")

    # 9. THE SECOND QUOTA. A standing lodging roof buys a firm, and the record says so the
    #    way the schema demands: a roof block, no order-book bucket, and a premises
    #    location in the very building that bought it.
    roofs = [r for r in build_group("lodging_river_and_transport")
             if (r["reconstruction"].get("roof") or {}).get("structure_id")]
    if not roofs:
        failures.append("the lodging group builds no house on a standing roof")
    for record in roofs:
        block = record["reconstruction"]
        if block.get("bucket") or block.get("slot"):
            failures.append("%s: bought by a roof and naming an order-book row too"
                            % record["id"])
        seat = record["locations"][0]
        if seat["kind"] != "premises" or seat["structure_id"] != block["roof"]["structure_id"]:
            failures.append("%s: bought by a roof it does not stand on" % record["id"])
        if record["proprietors"][0]["person_id"] != block["roof"]["keeper_person_id"]:
            failures.append("%s: keeps a house with somebody else's keeper" % record["id"])

    # 10. A roof whose keeper the lodgers stage never named is NOT ordered. This tool
    #     adopts a keeper and mints nobody, so an unkept roof is a shortfall stated in the
    #     ledger rather than a person invented to fill it.
    keeperless = roof_buckets("lodging_river_and_transport", keepers={})
    if keeperless:
        failures.append("a lodging roof with no keeper was still ordered a firm")

    # 11. A ROOF FILLS NO ORDER-BOOK BUCKET, because the book holds none of its class. A
    #     fill written against a key the book does not have would be counted by the book's
    #     own --build and there is nothing there to count.
    if fills_for({"lodging_river_and_transport": roofs}):
        failures.append("a house bought by a roof wrote a fill into the order book")

    if failures:
        print("\n".join(["self-test FAILED:"] + ["  " + f for f in failures]))
        return 1
    print("OK: 11 assertions of the business reconstruction still fire")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--group", action="append", choices=sorted(GROUPS),
                        help="the reconstruction group to build; repeatable")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.build:
        if not args.group:
            parser.error("--build wants a --group: a group is one ticket's quota")
        return build(args.group)
    if args.check:
        return check(args.group)
    parser.error("one of --build, --check or --self-test")


if __name__ == "__main__":
    raise SystemExit(main())
