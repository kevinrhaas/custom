#!/usr/bin/env python3
"""Compile data/businesses/ — one record per business, with a tier on every field.

    tools/compile_businesses.py --build       rewrite the compiled records
    tools/compile_businesses.py --check       the gate
    tools/compile_businesses.py --self-test   the gate's assertions still fire

T-1310, of T-1180. THERE WAS NOWHERE TO WRITE A BUSINESS DOWN. The business layer was
three DERIVED files — the newspaper claims, gazetteer.json, register_1835.json — and a
business existed in the scene only as a structure whose `function`/`occupants` block
named it. The register row has no staff field, no tier, no `sources[]`, and no dates
beyond the first and last issue a notice ran; a person's `works_at` is a bare structure
id. The owner's ask — a complete list of attested, inferred and then reconstructed
businesses, with the staff of each as part of their proprietors' resident profiles —
had no place to land. This builds the place. IT RECONSTRUCTS NOTHING: every one of the
196 records below is the register's own reading, restated with its tier made explicit
and its limits made queryable.

DERIVED, NEVER AUTHORED, for the same reason the gazetteer and the register are. A
`compiled_from_register` record is rewritten whole by `--build` and `--check` refuses a
committed copy a rebuild would not produce, so a hand edit to a compiled record is a
red gate rather than a silent divergence. A record a human means to author goes in
data/businesses/authored/ — which `--build` reads, validates and carries into the index
untouched. That directory is where T-1182's inferred-by-audit firms and T-1184's
reconstructions will be written; it is empty today, and the compiler is built to find
it empty without complaining.

THE ID SCHEME, AND WHY IT IS NOT THE ONE T-1180 NAMED. T-1180 asks for
`biz_<surname>_<trade>`. Derived over the 196 that scheme collides 27 times — five
houses land on `biz_montgomery_other`, four on `biz_wentworth_tavern`, two on
`biz_calhoun_printing_office` — and each collision is the same question: are these two
printed notices one house or two? That is an identity ruling, it is T-1182's to make
with the sources in front of it, and a compiler that settled it by appending `_2` would
be publishing an adjudication nobody made. So a compiled record takes the register's
own id with its `business_` prefix replaced by `biz_`: 1:1 with the printed notice it
comes from, collision-free by construction, and reversible, with `register_id` on the
record saying so out loud. `biz_<surname>_<trade>` and `rcb_…` stay in the schema for
the records a human authors, where the identity question has an author to answer it.

WHAT A TIER MEANS HERE. The ladder is the resident layer's, unchanged — attested,
inferred, reconstructed. A printed name is attested. The LINK from that printed name to
a town card is a separate claim from the name itself, and it is the register's: where
the register matched the name to a card, `person_id` carries the card and the basis
says which action made the match; where it did not, `person_id` is null and the basis
says the town does not hold that person yet. A null there is a finding, not a gap to be
filled by guessing.

THE LIMITS ARE DATA NOW. 61 of the register's businesses are `street_only` and 62 are
`unplaceable` at the scene date: the paper gives a street and no house, or no anchor at
all. Those are not missing locations — they are locations whose resolution the evidence
stops short of, and they were carried in prose in an `action_note` where nothing could
count them. Each is a `locations[]` entry with a `kind` that names the limit and a
`limit_reason` that quotes the register's reason, so "how many of the town's businesses
can we actually place?" is a query rather than a re-reading.
"""

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compile_gazetteer import (  # noqa: E402  — the identity policy has one home
    ROOT, RESEARCH, GAZETTEER, dumps, load_json,
)

REGISTER = RESEARCH / "register_1835.json"
RULINGS = RESEARCH / "trade_class_rulings.json"
RESIDENTS = ROOT / "data" / "residents"
BUSINESSES = ROOT / "data" / "businesses"
AUTHORED = BUSINESSES / "authored"
INDEX = BUSINESSES / "index.json"
SCHEMA = ROOT / "data" / "businesses.schema.json"
STREETS = ROOT / "data" / "streets" / "1835.json"

REGISTER_PREFIX = "business_"
ID_PREFIX = "biz_"

GRADES = ("attested", "inferred", "reconstructed")


# ---------------------------------------------------------------- reading the town

def person_ids(residents_dir=None):
    """Every person id the resident layer holds, so a link can be refused when it dangles.

    The index lists HEADS, and a proprietor is routinely not one — Archibald Clybourn
    heads a household and the clerk in his market does not — so the ids come from the
    household files themselves rather than from the index's summary rows.
    """
    root = Path(residents_dir or RESIDENTS)
    ids = set()
    for path in sorted(root.glob("households/*.json")) + sorted(root.glob("merged/*.json")):
        doc = load_json(path)
        record = doc.get("superseded_record", doc)
        for person in record.get("persons", []) or []:
            if person.get("id"):
                ids.add(person["id"])
    return ids


def works_at_rows(residents_dir=None):
    """The households whose `works_at` names a structure — the crosswalk's left-hand side."""
    index = load_json(Path(residents_dir or RESIDENTS) / "index.json")
    return [
        {"household_id": h["id"], "head": h.get("head"), "structure_id": h["works_at"]}
        for h in index["households"]
        if h.get("works_at")
    ]


# ---------------------------------------------------------------- building a record

def record_id(register_id):
    if not register_id.startswith(REGISTER_PREFIX):
        raise ValueError("a register business id must start with %r: %r"
                         % (REGISTER_PREFIX, register_id))
    return ID_PREFIX + register_id[len(REGISTER_PREFIX):]


def person_entry(name, role, register_person, town_ids, evidence, claim_ids):
    """One named person on a business, with the LINK tiered separately from the name."""
    resolved = None
    if register_person and register_person.get("action") == "enrich":
        target = register_person.get("action_target")
        if target in town_ids:
            resolved = target

    if resolved:
        basis = ("The register matches the printed name to the town card %s (action: enrich), "
                 "so this is the same person the resident layer already holds." % resolved)
    elif register_person:
        basis = ("The register holds this printed name as %s with action %r: the town does not "
                 "carry a card for them under an id this record can name, so the reading is the "
                 "name and not yet a person." % (register_person["id"], register_person.get("action")))
    else:
        basis = ("A proprietor string the gazetteer reads as a person, which the register's own "
                 "person list does not carry under this spelling. The name is the evidence; no "
                 "link is claimed.")

    return {
        "name": name,
        "person_id": resolved,
        "register_person_id": register_person["id"] if register_person else None,
        "role": role,
        # THE PRINTING WINDOW IS THE BOUND, NOT THE TENURE. The paper says this person
        # was in this house on the days it printed; it does not say when they joined it
        # or left. The dates are carried because they are the only bound there is, and
        # the basis says what they are so no reader takes them for a start and an end.
        "from": evidence.get("first_issue"),
        "to": evidence.get("last_issue"),
        "tier": "attested",
        "basis": basis + " Dated by the printing window, which bounds the reading and does "
                         "not date the partnership.",
        "source_id": "chicago_newspapers_1833_1835",
        "claim_ids": list(claim_ids),
    }


def locations_for(entry, gaz):
    """The register's action, restated as places and as the limits on places."""
    action = entry["action"]
    target = entry.get("action_target")
    note = entry.get("action_note") or ""
    out = []

    if action == "enrich_existing":
        # Matched onto a roof the town already holds. `occupants` matched the structure's
        # own occupants line and is the stronger read of the two; `name` matched the
        # structure's NAME, which a second house of the same style could also answer to.
        occupants = entry.get("match_tier") == "occupants"
        out.append({
            "kind": "premises",
            "structure_id": target,
            "street_id": entry.get("street_id"),
            "face": None,
            "primary": True,
            "from": (entry.get("evidence") or {}).get("first_issue"),
            "to": None,
            "tier": "attested" if occupants else "inferred",
            "basis": ("The register matches this business onto the committed structure %s on its "
                      "%s. %s" % (target, entry.get("match_tier"), note)).strip(),
            "limit_reason": None,
        })
    elif action == "new_building":
        # Placeable, and not placed: the paper anchors the house against a landmark the
        # town holds, but the town holds no roof of this house's own. That is a location
        # with a limit on it, not a premises.
        out.append({
            "kind": "anchored",
            "structure_id": None,
            "street_id": entry.get("street_id"),
            "face": None,
            "primary": True,
            "from": (entry.get("evidence") or {}).get("first_issue"),
            "to": None,
            "tier": "inferred",
            "basis": note or "Placeable against the committed town.",
            "limit_reason": ("The register places this house against %s and the town holds no roof "
                             "of its own for it (action: new_building), so the anchor is as far as "
                             "the reading goes." % (target or "a landmark it names")),
        })
    elif action == "street_only":
        out.append({
            "kind": "street_only",
            "structure_id": None,
            "street_id": entry.get("street_id"),
            "face": None,
            "primary": True,
            "from": (entry.get("evidence") or {}).get("first_issue"),
            "to": None,
            "tier": "inferred",
            "basis": "The paper names a street and no house on it.",
            "limit_reason": note or "The anchor names nothing the committed town holds.",
        })
    else:
        out.append({
            "kind": "unplaceable",
            "structure_id": None,
            "street_id": None,
            "face": None,
            "primary": True,
            "from": (entry.get("evidence") or {}).get("first_issue"),
            "to": None,
            "tier": "inferred",
            "basis": "The register resolved no place for this house at the scene date.",
            "limit_reason": note or "The paper gives no anchor.",
        })

    # A HOUSE THAT MOVED. Four of the register's businesses print one anchor and later
    # another. The earlier siting is a real dated location and is kept as one, unplaced:
    # the `from` anchor is prose the register never resolved to an id, so the record says
    # where the paper put it and says that it could not be resolved. T-1182 audits dated
    # relocations with the sources in front of it.
    for change in ((entry.get("anchor_change") or {}).get("changes") or []):
        out.append({
            "kind": "unplaceable",
            "structure_id": None,
            "street_id": None,
            "face": None,
            "primary": False,
            "from": change.get("after"),
            "to": change.get("before"),
            "tier": "inferred",
            "basis": ("An earlier anchor for this house, printed as “%s” and superseded by "
                      "“%s”." % (change.get("from"), change.get("to"))),
            "limit_reason": ("A prose anchor the register did not resolve to a committed id; kept "
                             "because the house moved and the move is dated."),
        })
    return out


def dates_for(entry):
    announced = [o for o in entry.get("opening_announced") or [] if o.get("iso")]
    evidence = entry.get("evidence") or {}
    first = evidence.get("first_issue")
    dissolved = entry.get("dissolved_after_scene_date") or []

    if announced:
        opened = min(o["iso"] for o in announced)
        precision = "exact"
        basis = ("The paper announces the opening: %s." % "; ".join(
            "%s (%s)" % (o["claim"], o["iso"]) for o in announced))
    elif first:
        opened = first
        precision = "not_later_than"
        basis = ("No opening is announced. The first printing, %s, is the bound: the house was "
                 "trading by then and the record does not say when it began." % first)
    else:
        opened = None
        precision = "unbounded"
        basis = "Neither an opening nor a printing date; the record bounds nothing."

    closed = None
    if dissolved:
        closed = evidence.get("last_issue")
        basis += (" A dissolution is printed after the scene date (%s), so the house is closed at "
                  "the last issue that carries it." % ", ".join(dissolved))

    return {
        "opened": opened,
        "closed": closed,
        "precision": precision,
        "tier": "attested" if announced else "inferred",
        "basis": basis,
    }


def compile_record(entry, gaz, register_persons, town_ids):
    """One register business, restated as a record."""
    by_name = register_persons
    evidence = entry.get("evidence") or {}
    claims = list(gaz.get("mentions") or [])
    people = list(entry.get("partners") or [])
    sole = len(people) == 1 and not (gaz.get("firm_styles") or [])

    proprietors, partners = [], []
    for name in people:
        role = "proprietor" if sole else "partner"
        person = person_entry(name, role, by_name.get(name), town_ids, evidence, claims)
        (proprietors if sole else partners).append(person)

    classes = list(gaz.get("trade_classes") or []) or ["not_stated"]

    return {
        "id": record_id(entry["id"]),
        "register_id": entry["id"],
        "name": entry["name"],
        "provenance": "compiled_from_register",
        "type": classes,
        "trade": entry.get("trade"),
        "occupation": entry.get("occupation"),
        "goods": list(gaz.get("goods") or []),
        "firm_styles": list(entry.get("firm_styles") or []),
        "proprietors": proprietors,
        "partners": partners,
        # THE PAPERS NAME OWNERS AND ALMOST NEVER A CLERK. Empty here is a true reading
        # of the register and not an omission: T-1183 rules the staffing model and
        # T-1189 fills this from it.
        "staff": [],
        "locations": locations_for(entry, gaz),
        "dates": dates_for(entry),
        "evidence": {
            "first_issue": evidence.get("first_issue"),
            "last_issue": evidence.get("last_issue"),
            "copy_dates": list((gaz.get("evidence") or {}).get("copy_dates") or []),
        },
        "present_at_scene_date": bool(entry.get("present_at_scene_date")),
        "exclusion": entry.get("exclusion"),
        "exclusion_note": entry.get("exclusion_note"),
        # NEVER INFERRED FROM A SURNAME. The community of a proprietor is a claim about a
        # person, and the register carries no such claim; reading one off a name is the
        # exact move the resident layer refuses. T-1177 fills this where a source speaks.
        "proprietor_community": "unattested",
        "customers": [],
        "sources": ["chicago_newspapers_1833_1835"],
        "claim_ids": claims,
        "liberties": {
            "survival_required": bool(entry.get("survival_liberty_required")),
            "backdating_required": bool(entry.get("backdating_liberty_required")),
        },
        "review_required": False,
        "replaceable_by": ("A directory, a deed or a later reading that names this house's premises, "
                           "its staff or its dates more exactly than the newspapers do."),
    }


def compile_all(register, gazetteer, town_ids):
    gaz_by_id = {b["id"]: b for b in gazetteer["businesses"]}
    by_name = {}
    for person in register["persons"]:
        by_name.setdefault(person["name"], person)
    records = []
    for entry in register["businesses"]:
        gaz = gaz_by_id.get(entry["id"])
        if gaz is None:
            raise ValueError("register business %s has no gazetteer row" % entry["id"])
        records.append(compile_record(entry, gaz, by_name, town_ids))
    records.sort(key=lambda r: r["id"])
    return records


# ---------------------------------------------------------------- the index

def crosswalk(records, rows):
    """`works_at` → a business, where a business sits in the roof the household names.

    The resident layer's `works_at` is a bare structure id and cannot say WHICH house of
    trade a person worked for; where two businesses share a roof the crosswalk says two,
    because that is what the evidence supports and picking one would be a ruling.
    """
    by_structure = {}
    for record in records:
        for loc in record["locations"]:
            if loc["kind"] == "premises" and loc.get("structure_id"):
                by_structure.setdefault(loc["structure_id"], []).append(record["id"])
    out = []
    for row in rows:
        out.append({
            "household_id": row["household_id"],
            "head": row["head"],
            "structure_id": row["structure_id"],
            "business_ids": sorted(by_structure.get(row["structure_id"], [])),
        })
    return out


# ---------------------------------------------------------- the directory's rows

def street_names():
    """`street_id` -> the name the town used in 1835, for the row a directory prints.

    The corridors are the only place that mapping lives, and a business's
    `street_id` is one of their ids; an id the corridors do not hold comes
    through as its own id rather than as a guess.
    """
    return {s["id"]: s.get("name_1835") or s["id"] for s in load_json(STREETS)["streets"]}


def record_grade(record):
    """The grade of the firm ITSELF, which is not the grade of any one of its rows.

    A business record states tiers in three places — who ran it, where it stood and
    when it opened — and a directory has to answer one question with them: how well
    is this house evidenced? So: `attested` where ANY of those claims is attested (a
    named proprietor, a premises, an announced opening), `reconstructed` where every
    one of them is reconstructed, `inferred` otherwise. The definition is stated here
    and printed in the app, because a grade a reader cannot unpick is a claim.
    """
    tiers = [record["dates"].get("tier")]
    tiers += [loc.get("tier") for loc in record["locations"]]
    tiers += [p.get("tier") for p in record["proprietors"] + record["partners"] + record["staff"]]
    tiers = [t for t in tiers if t]
    if not tiers:
        return "inferred"
    if "attested" in tiers:
        return "attested"
    if all(t == "reconstructed" for t in tiers):
        return "reconstructed"
    return "inferred"


def primary_location(record, streets):
    """The location a row is filed under: the one marked `primary`, else the first.

    A firm with two premises is filed under its principal one and the card prints
    the dated list in full — the list is the record, this is only the row.
    """
    locs = record["locations"]
    if not locs:
        return None
    loc = next((x for x in locs if x.get("primary")), locs[0])
    street_id = loc.get("street_id")
    return {
        "kind": loc.get("kind"),
        "structure_id": loc.get("structure_id"),
        "street_id": street_id,
        "street": streets.get(street_id) if street_id else None,
        "tier": loc.get("tier"),
        "from": loc.get("from"),
        "to": loc.get("to"),
        "limit_reason": loc.get("limit_reason"),
    }


def index_people(record):
    """Everyone the record names, flattened to `{name, person_id, role, tier, from, to}`.

    The directory searches proprietors by name and the card links the ones the town
    holds a card for; both want one list, and the three fields it comes from say the
    same things in the same words.
    """
    out = []
    for field in ("proprietors", "partners", "staff"):
        for person in record[field]:
            out.append({
                "name": person.get("name"),
                "person_id": person.get("person_id"),
                "role": person.get("role") or field[:-1],
                "tier": person.get("tier"),
                "from": person.get("from"),
                "to": person.get("to"),
            })
    return out


def index_row(record, streets):
    """One business as a directory row: everything the list, its filters and its
    counts read, and nothing the card alone needs — the card fetches the record."""
    return {
        "id": record["id"],
        "file": "%s.json" % record["id"],
        "name": record["name"],
        "register_id": record.get("register_id"),
        "provenance": record["provenance"],
        "type": record["type"],
        "present_at_scene_date": record["present_at_scene_date"],
        "grade": record_grade(record),
        "trade": record.get("trade"),
        "occupation": record.get("occupation"),
        "goods": record.get("goods") or [],
        "firm_styles": record.get("firm_styles") or [],
        "people": index_people(record),
        "where": primary_location(record, streets),
        "locations": len(record["locations"]),
        "opened": record["dates"].get("opened"),
        "closed": record["dates"].get("closed"),
        "dates_tier": record["dates"].get("tier"),
        "proprietor_community": record.get("proprietor_community"),
        "review_required": bool(record.get("review_required")),
        "liberties": sorted(k for k, v in (record.get("liberties") or {}).items() if v),
    }


def build_index(records, authored, rows):
    everything = records + authored
    counts_by_type = {}
    for record in everything:
        for kind in record["type"]:
            counts_by_type[kind] = counts_by_type.get(kind, 0) + 1
    counts_by_kind = {}
    for record in everything:
        for loc in record["locations"]:
            counts_by_kind[loc["kind"]] = counts_by_kind.get(loc["kind"], 0) + 1
    linked = sum(1 for r in everything for p in r["proprietors"] + r["partners"] + r["staff"]
                 if p["person_id"])
    named = sum(1 for r in everything for p in r["proprietors"] + r["partners"] + r["staff"])
    counts_by_grade = {}
    counts_by_street = {}
    # By the PRIMARY location, which is not the same tally as `by_location_kind`
    # above: that one counts LOCATIONS, and four of these houses moved inside the
    # window, so a firm filed under the street it ended on still carries an
    # unplaceable earlier address. The directory files a firm once, so it needs
    # the count of FIRMS — 83 unplaceable locations are 79 unplaceable houses.
    counts_by_where = {}
    streets = street_names()
    directory = [index_row(r, streets) for r in sorted(everything, key=lambda r: r["id"])]
    for row in directory:
        counts_by_grade[row["grade"]] = counts_by_grade.get(row["grade"], 0) + 1
        street = (row["where"] or {}).get("street")
        if street:
            counts_by_street[street] = counts_by_street.get(street, 0) + 1
        kind = (row["where"] or {}).get("kind")
        if kind:
            counts_by_where[kind] = counts_by_where.get(kind, 0) + 1
    walk = crosswalk(everything, rows)
    return {
        "schema": 1,
        "_doc": ("DERIVED, NEVER AUTHORED. Rebuilt from register_1835.json, gazetteer.json and "
                 "data/residents/ by tools/compile_businesses.py; tools/check.sh refuses a "
                 "committed copy a rebuild would not produce. Edit the gazetteer, the dataset or "
                 "data/businesses/authored/, not this file."),
        "generated_by": "tools/compile_businesses.py",
        "counts": {
            "records": len(everything),
            "compiled_from_register": len(records),
            "authored": len(authored),
            "present_at_scene_date": sum(1 for r in everything if r["present_at_scene_date"]),
            "by_type": dict(sorted(counts_by_type.items())),
            "by_location_kind": dict(sorted(counts_by_kind.items())),
            "named_people": named,
            "named_people_linked_to_a_town_card": linked,
            "works_at_households": len(walk),
            "works_at_households_resolving_to_a_business": sum(1 for w in walk if w["business_ids"]),
            "by_grade": dict(sorted(counts_by_grade.items())),
            "by_where_kind": dict(sorted(counts_by_where.items())),
            "by_street": dict(sorted(counts_by_street.items())),
        },
        "_businesses_doc": ("THE DIRECTORY'S ROWS. Each carries what the Businesses list, its "
                            "filters and its counts read — the card fetches the record itself "
                            "and prints the rest. `grade` is the firm's own, not any one row's: "
                            "attested where any of who-ran-it, where-it-stood or when-it-opened "
                            "is attested, reconstructed where every one of them is, inferred "
                            "otherwise. `place` is the PRIMARY location; `locations` says how "
                            "many the record holds. The layer states no division for a business "
                            "— street is as near as the record goes."),
        "businesses": directory,
        "_works_at_doc": ("THE CROSSWALK, NOT A RULING. A household's `works_at` names a STRUCTURE; "
                          "this says which business records stand in that structure. Two entries "
                          "mean two houses share the roof and the evidence does not choose between "
                          "them; an empty list means the roof carries no business the register "
                          "knows, which is a finding about the register."),
        "works_at": walk,
    }


# ---------------------------------------------------------------- build / check

def read_authored():
    if not AUTHORED.is_dir():
        return []
    return [load_json(p) for p in sorted(AUTHORED.glob("*.json"))]


def compiled_docs(residents_dir=None):
    register = load_json(REGISTER)
    gazetteer = load_json(GAZETTEER)
    town_ids = person_ids(residents_dir)
    records = compile_all(register, gazetteer, town_ids)
    authored = read_authored()
    return records, authored, build_index(records, authored, works_at_rows(residents_dir))


def build():
    records, authored, index = compiled_docs()
    BUSINESSES.mkdir(parents=True, exist_ok=True)
    AUTHORED.mkdir(parents=True, exist_ok=True)
    wanted = {"%s.json" % r["id"] for r in records} | {"index.json"}
    for path in BUSINESSES.glob("*.json"):
        if path.name not in wanted:
            path.unlink()
    for record in records:
        (BUSINESSES / ("%s.json" % record["id"])).write_text(dumps(record), encoding="utf-8")
    INDEX.write_text(dumps(index), encoding="utf-8")
    problems = semantic_problems(records + authored)
    for problem in problems:
        print("  FAIL  " + problem, file=sys.stderr)
    print("compiled %d business record(s) (%d from the register, %d authored) → %s"
          % (len(records) + len(authored), len(records), len(authored),
             BUSINESSES.relative_to(ROOT)))
    print("  %d named proprietor(s)/partner(s); %d linked to a town card"
          % (index["counts"]["named_people"], index["counts"]["named_people_linked_to_a_town_card"]))
    print("  locations by kind: %s" % index["counts"]["by_location_kind"])
    return 1 if problems else 0


def semantic_problems(records, town_ids=None):
    """The rules a JSON schema cannot state. Every one of these is a --self-test case."""
    town_ids = town_ids if town_ids is not None else person_ids()
    bad = []
    seen = set()
    for record in records:
        rid = record.get("id", "<no id>")
        if rid in seen:
            bad.append("%s: two records carry this id" % rid)
        seen.add(rid)

        for person in record["proprietors"] + record["partners"] + record["staff"]:
            if person["tier"] == "attested" and not (person.get("source_id") or person.get("claim_ids")):
                bad.append("%s: %r is attested and cites nothing" % (rid, person["name"]))
            if not (person.get("basis") or "").strip():
                bad.append("%s: %r carries no basis" % (rid, person["name"]))
            if person["person_id"] is not None and person["person_id"] not in town_ids:
                bad.append("%s: %r links to %s, which the resident layer does not hold"
                           % (rid, person["name"], person["person_id"]))

        primary = [loc for loc in record["locations"] if loc["primary"]]
        if len(primary) != 1:
            bad.append("%s: %d primary location(s); a record has exactly one"
                       % (rid, len(primary)))
        for loc in record["locations"]:
            if loc["kind"] in ("street_only", "unplaceable") and not (loc.get("limit_reason") or "").strip():
                bad.append("%s: a %s location states no limit_reason" % (rid, loc["kind"]))
            if loc["kind"] == "premises" and not loc.get("structure_id"):
                bad.append("%s: a premises location names no structure" % rid)
            if loc["tier"] not in GRADES:
                bad.append("%s: location tier %r is off the ladder" % (rid, loc["tier"]))

        if record["dates"]["tier"] == "attested" and record["dates"]["precision"] != "exact":
            bad.append("%s: dates are attested at precision %r; an attested opening is exact"
                       % (rid, record["dates"]["precision"]))
        if not record["type"]:
            bad.append("%s: no census class" % rid)
    return bad


def schema_problems(records):
    try:
        import jsonschema
    except ImportError:
        print("  note: jsonschema is not installed, so the records were NOT validated "
              "against data/businesses.schema.json. A GATE may not count this as a pass.",
              file=sys.stderr)
        return []
    schema = load_json(SCHEMA)
    validator = jsonschema.Draft202012Validator(schema)
    bad = []
    for record in records:
        for error in sorted(validator.iter_errors(record), key=lambda e: list(e.path)):
            bad.append("%s: %s at %s" % (record.get("id"), error.message,
                                         "/".join(str(p) for p in error.path) or "<root>"))
    return bad


def check():
    if not BUSINESSES.is_dir():
        return ["data/businesses/ does not exist; run tools/compile_businesses.py --build"]
    records, authored, index = compiled_docs()
    bad = []

    committed = {p.name for p in BUSINESSES.glob("*.json")}
    wanted = {"%s.json" % r["id"] for r in records} | {"index.json"}
    for extra in sorted(committed - wanted):
        bad.append("data/businesses/%s is committed and a rebuild does not produce it" % extra)
    for missing in sorted(wanted - committed):
        bad.append("data/businesses/%s is missing; run --build" % missing)

    for record in records:
        path = BUSINESSES / ("%s.json" % record["id"])
        if path.name in committed and path.read_text(encoding="utf-8") != dumps(record):
            bad.append("data/businesses/%s differs from a rebuild — it is DERIVED; edit the "
                       "gazetteer or the dataset, not this file" % path.name)
    if INDEX.exists() and INDEX.read_text(encoding="utf-8") != dumps(index):
        bad.append("data/businesses/index.json differs from a rebuild")

    for record in authored:
        if record.get("provenance") == "compiled_from_register":
            bad.append("%s: an authored record may not claim provenance "
                       "compiled_from_register" % record.get("id"))

    bad += schema_problems(records + authored)
    bad += semantic_problems(records + authored)

    # THE REGISTER MUST POINT AT THE LAYER. compile_register.py writes
    # `business_record_id` on every row; a row whose record is absent is the failure this
    # layer exists to make impossible.
    register = load_json(REGISTER)
    have = {r["id"] for r in records} | {r.get("id") for r in authored}
    for entry in register["businesses"]:
        pointed = entry.get("business_record_id")
        if not pointed:
            bad.append("register business %s carries no business_record_id" % entry["id"])
        elif pointed not in have:
            bad.append("register business %s points at %s, which the layer does not hold"
                       % (entry["id"], pointed))
    return bad


# ---------------------------------------------------------------- self-test

def self_test():
    """Break each assertion and require it to fire. A gate nobody has broken is a hope."""
    failures = []

    def expect(name, records, needle, town_ids=None):
        found = semantic_problems(records, town_ids)
        if not any(needle in problem for problem in found):
            failures.append("%s: expected a refusal mentioning %r, got %r" % (name, needle, found))

    base = {
        "id": "biz_fixture", "register_id": "business_fixture", "name": "A fixture",
        "provenance": "compiled_from_register", "type": ["store"], "trade": "dry goods",
        "occupation": "dry_goods_merchant", "goods": [], "firm_styles": [],
        "proprietors": [{"name": "A. Fixture", "person_id": "fixture_a",
                         "register_person_id": "person_a_fixture", "role": "proprietor",
                         "from": "1835-01-01", "to": "1835-06-01", "tier": "attested",
                         "basis": "the notice prints the name",
                         "source_id": "chicago_newspapers_1833_1835", "claim_ids": ["c001"]}],
        "partners": [], "staff": [],
        "locations": [{"kind": "premises", "structure_id": "fixture_store", "street_id": None,
                       "face": None, "primary": True, "from": "1835-01-01", "to": None,
                       "tier": "attested", "basis": "matched on occupants", "limit_reason": None}],
        "dates": {"opened": "1835-01-01", "closed": None, "precision": "exact",
                  "tier": "attested", "basis": "announced"},
        "evidence": {"first_issue": "1835-01-01", "last_issue": "1835-06-01", "copy_dates": []},
        "present_at_scene_date": True, "exclusion": None, "exclusion_note": None,
        "proprietor_community": "unattested", "customers": [],
        "sources": ["chicago_newspapers_1833_1835"], "claim_ids": ["c001"],
        "liberties": {"survival_required": False, "backdating_required": False},
        "review_required": False, "replaceable_by": "a directory",
    }
    ids = {"fixture_a"}

    clean = semantic_problems([json.loads(json.dumps(base))], ids)
    if clean:
        failures.append("the fixture itself is refused: %r" % clean)

    def mutate(fn):
        doc = json.loads(json.dumps(base))
        fn(doc)
        return [doc]

    def unset_source(doc):
        doc["proprietors"][0]["source_id"] = None
        doc["proprietors"][0]["claim_ids"] = []
    expect("an attested person citing nothing", mutate(unset_source), "cites nothing", ids)

    expect("a person with no basis",
           mutate(lambda d: d["proprietors"][0].update(basis="  ")), "carries no basis", ids)

    expect("a person id the town does not hold",
           mutate(lambda d: d["proprietors"][0].update(person_id="nobody_at_all")),
           "the resident layer does not hold", ids)

    expect("two primary locations",
           mutate(lambda d: d["locations"].append(dict(d["locations"][0]))),
           "primary location(s)", ids)

    def make_street_only(doc):
        doc["locations"][0].update(kind="street_only", structure_id=None, limit_reason=None)
    expect("a limit with no reason", mutate(make_street_only), "states no limit_reason", ids)

    expect("a premises naming no structure",
           mutate(lambda d: d["locations"][0].update(structure_id=None)),
           "names no structure", ids)

    expect("a tier off the ladder",
           mutate(lambda d: d["locations"][0].update(tier="probable")), "off the ladder", ids)

    expect("an attested opening that is not exact",
           mutate(lambda d: d["dates"].update(precision="not_later_than")),
           "an attested opening is exact", ids)

    expect("no census class", mutate(lambda d: d.update(type=[])), "no census class", ids)

    def duplicate(doc):
        pass
    twins = [json.loads(json.dumps(base)), json.loads(json.dumps(base))]
    expect("two records with one id", twins, "two records carry this id", ids)

    # THE COMMITTED COPY IS A DERIVATION, and --check must say so when it is edited.
    # Broken in a temporary copy of the tree so the working tree is never touched.
    if BUSINESSES.is_dir():
        with tempfile.TemporaryDirectory() as tmp:
            sample = sorted(BUSINESSES.glob("biz_*.json"))
            if sample:
                target = sample[0]
                backup = Path(tmp) / target.name
                shutil.copy2(target, backup)
                try:
                    doc = load_json(target)
                    doc["name"] = doc["name"] + " (hand-edited)"
                    target.write_text(dumps(doc), encoding="utf-8")
                    if not any("differs from a rebuild" in b for b in check()):
                        failures.append("a hand-edited compiled record was not refused")
                finally:
                    shutil.copy2(backup, target)

    # The build is deterministic: two compiles of the same input agree byte for byte.
    first, _, index_a = compiled_docs()
    second, _, index_b = compiled_docs()
    if dumps(first) != dumps(second) or dumps(index_a) != dumps(index_b):
        failures.append("the compile is not deterministic")

    for failure in failures:
        print("  FAIL  " + failure, file=sys.stderr)
    if failures:
        return 1
    print("self-test: %d assertion(s) fire when broken, and the compile is deterministic" % 11)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.build:
        return build()
    if args.self_test:
        return self_test()
    bad = check()
    for problem in bad:
        print("  FAIL  " + problem, file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
