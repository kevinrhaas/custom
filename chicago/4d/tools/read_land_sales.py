#!/usr/bin/env python3
"""The Illinois State Archives land tract sales, read into the research shape (T-0557).

    tools/read_land_sales.py --build       derive every generated file from the TSV
    tools/read_land_sales.py --check       the gate: re-derive and refuse any drift
    tools/read_land_sales.py --self-test   the gate's assertions still fire when broken

WHAT THIS READS. `data/research/land_sales/text/*.tsv` is the committed deposit: one
row per sale, every field exactly as the database printed it, harvested by
`tools/harvest_land_sales.py --sweep` (which reaches the network and is therefore run
deliberately, never by the gate). Everything else under `data/research/land_sales/`
is derived from that file by --build and re-derived by --check, so a hand-edit to a
generated file is a gate failure and not a silent divergence.

WHY A SALE IS NOT A RESIDENT, and it is the only thing about this source that
matters. The register records a TRANSACTION. A man who entered eighty acres in T40N
R14E in 1835 may have been standing in Chicago, in Vandalia, or in Connecticut; the
purchase says only that he bought. The one column that speaks to where he lived is
`Residence`, and it names a COUNTY — COOK, MACON, VERMILION — never a town. So:

  * a purchase alone proposes NOTHING about residence, and this file grades it
    `inferred` with the reasoning written on the row;
  * a purchase whose Residence column reads COOK is contemporary evidence that the
    purchaser lived in Cook County on the date of sale, and is graded `documented`
    for exactly that and no more — Cook County in 1835 is far larger than the town;
  * nothing here mints a resident or regrades one. `resident_crosswalk.json` proposes
    a correspondence and states the rule that made it; T-0514 and T-0515 write people.

A surname-only purchaser is always a refusal, however good the tract agreement is.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import namesake  # noqa: E402  (the namesake rule this imports rather than restates)

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = ROOT / "data" / "research" / "land_sales"
RESIDENTS = ROOT / "data" / "residents"
SOURCE_ID = "isa_public_domain_land_tract_sales"
# THE DEPOSITS, IN THE ORDER THEY WERE ADDED, and that order is load-bearing. Record
# ids are positional — `ls0001` upward across the whole reading — and data/structures/
# *.json cite them by id, so a new deposit APPENDS and never renumbers what is already
# cited. Each carries the (township, range) pairs its sweep asked for, section by
# section, and the ticket that read them; coverage is derived from exactly that.
DEPOSITS = (
    {"tsv": "isa_land_tract_sales_t39n_t40n_r14e_through_1836.tsv",
     "ticket": "T-0675", "pairs": ((39, 14), (40, 14))},
    {"tsv": "isa_land_tract_sales_t39n_t40n_r13e_t38n_t41n_r14e_t38n_r15e_through_1836.tsv",
     "ticket": "T-0676", "pairs": ((39, 13), (40, 13), (38, 14), (41, 14), (38, 15))},
)


def deposit_of(name: str) -> dict:
    for d in DEPOSITS:
        if d["tsv"] == name:
            return d
    raise SystemExit("land_sales: no deposit named %s" % name)


def records_name(tsv: str) -> str:
    """The records file a deposit derives: one per deposit, named after it."""
    return "records/entries_" + tsv[len("isa_land_tract_sales_"):-len(".tsv")] + ".json"

# T-0557 read three sections of T39N R14E — 16, 21 and 29 — as truncated: their section
# query returned exactly 150 rows, the database's per-page ceiling, and the pass took
# that for the end of what could be asked. It is not. The results page carries a More
# button whose keyset cursor walks the rest, `harvest_land_sales.py` follows it, and
# T-0675 read all three whole: 337 sales through 1836 in section 16, 4 in 21, 4 in 29,
# against the 154 the first page gave. So no section of these two townships is
# truncated now, and nothing here may say the source cannot be paged.
TRUNCATED = set()

# The database's own abbreviations, expanded only where the expansion is the Archives'
# own and not this project's guess. Anything absent stays as the register wrote it.
SALE_TYPES = {"FD": "federal land sale (cash entry)",
              "SC": "school section sale",
              "CN": "canal land sale"}

COLS = ["purchase_no", "purchaser", "residence", "social_status", "aliquot_or_lot",
        "section", "township", "range", "meridian", "county", "acres", "price_per_acre",
        "total_price", "type_of_sale", "date_purchased", "volume", "page"]

# `LOT8BL47` is a town lot; `E2NE` is a half quarter-section. The two resolve to
# different things on the ground and the distinction is kept structurally rather than
# left for a downstream regex to guess at.
LOT = re.compile(r"^LOT(\d+)BL(\d+)$")
HALF = re.compile(r"^([NSEW])2([NS][EW])(FR|VOID|VO)?$")
QUARTER = re.compile(r"^([NS][EW])([NS][EW])?(FR|VOID|VO)?$")

SUFFIXES = {"JR", "SR", "II", "III"}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def dump(p: Path, doc) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_tsv(domain: Path) -> list:
    """Every committed deposit, in DEPOSITS order, each row carrying the file it is on.

    A row's citation is a file AND a line, so the file travels with the row: two
    deposits both have a line 2 and they are not the same sale.
    """
    rows = []
    for dep in DEPOSITS:
        path = domain / "text" / dep["tsv"]
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        head = lines[0].split("\t")
        if head != COLS:
            raise SystemExit("land_sales: the deposit's header is not the harvest's header")
        for n, line in enumerate(lines[1:], start=2):
            if not line.strip():
                continue
            cells = line.split("\t")
            if len(cells) != len(COLS):
                raise SystemExit("land_sales: %s line %d has %d cells, not %d"
                                 % (dep["tsv"], n, len(cells), len(COLS)))
            row = dict(zip(COLS, cells))
            row["_line"] = n
            row["_file"] = dep["tsv"]
            rows.append(row)
    return rows


def tract(row: dict) -> dict:
    """The tract a footprint can be resolved against — structured, never smoothed.

    `part` is the aliquot description as the register wrote it. `resolves` says what
    kind of thing it is, because a town lot and a half quarter-section are not the
    same object and a map that treats them alike puts a house in a cornfield.
    """
    part = row["aliquot_or_lot"]
    t = {"section": row["section"], "township": row["township"], "range": row["range"],
         "meridian": row["meridian"], "part": part, "resolves": "unparsed",
         "lot": None, "block": None, "void": part.endswith(("VOID", "VO"))}
    m = LOT.match(part)
    if m:
        t["resolves"] = "town_lot"
        t["lot"], t["block"] = m.group(1), m.group(2)
        return t
    if HALF.match(part):
        t["resolves"] = "half_quarter_section"
        return t
    if QUARTER.match(part):
        t["resolves"] = "quarter_section" if len(QUARTER.match(part).group(0).rstrip("FRVOID")) <= 2 \
            else "quarter_quarter_section"
        return t
    return t


def iso_date(us: str) -> str:
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", us)
    return "%s-%s-%s" % (m.group(3), m.group(1), m.group(2)) if m else us


def normalize_name(as_read: str) -> str:
    """`DEVINPORT WILLIAM` reads back as `William Devinport`. The register's spelling is
    NEVER corrected here — that is what `resident_crosswalk.json` is for."""
    parts = [p for p in as_read.split() if p]
    if not parts:
        return as_read
    surname, given = parts[0], parts[1:]
    suffix = ""
    if given and given[-1].upper() in SUFFIXES:
        suffix = " " + given[-1].title()
        given = given[:-1]
    out = " ".join(g.title() if len(g) > 1 else g.upper() for g in given)
    return (out + " " + surname.title() + suffix).strip()


def surname_of(as_read: str) -> str:
    return (as_read.split() or [""])[0].upper()


def givens_of(as_read: str) -> list:
    return [p.upper() for p in as_read.split()[1:] if p.upper() not in SUFFIXES]


def list_name(row: dict) -> str:
    return "T%s R%s sec %s" % (row["township"], row["range"], row["section"])


def build_records(rows: list, start: int = 1) -> dict:
    records = []
    for i, row in enumerate(rows, start=start):
        cook = row["residence"].upper() == "COOK"
        records.append({
            "id": "ls%04d" % i,
            "as_read": row["purchaser"],
            "normalized": normalize_name(row["purchaser"]),
            "locator": {"list": list_name(row), "line": row["_line"],
                        "purchase_no": row["purchase_no"],
                        "volume": row["volume"], "page": row["page"],
                        "text_file": row["_file"]},
            "reading": "transcription_mediated",
            "confidence": "documented" if cook else "inferred",
            "notes": ("The register's Residence column reads COOK: contemporary evidence "
                      "that this purchaser lived in Cook County on %s, and evidence of "
                      "nothing narrower — the county in 1835 reaches far beyond the town."
                      % iso_date(row["date_purchased"])) if cook else
                     ("Residence %r. A purchase is a transaction and not a residence, so "
                      "the row is graded inferred: what it documents is that this name "
                      "entered this tract on %s."
                      % (row["residence"] or "(blank)", iso_date(row["date_purchased"]))),
            "sale": {
                "purchase_no": row["purchase_no"],
                "residence_as_read": row["residence"],
                "social_status_as_read": row["social_status"],
                "date_purchased": iso_date(row["date_purchased"]),
                "date_as_read": row["date_purchased"],
                "acres": row["acres"],
                "price_per_acre": row["price_per_acre"],
                "total_price": row["total_price"],
                "type_of_sale": row["type_of_sale"],
                "type_of_sale_expanded": SALE_TYPES.get(row["type_of_sale"]),
                "county": row["county"],
                "volume": row["volume"],
                "page": row["page"],
            },
            "tract": tract(row),
        })
    return {
        "schema": 1,
        "domain": "land_sales",
        "source_id": SOURCE_ID,
        "generated_by": "tools/read_land_sales.py --build",
        "note": "Every field is the database's own. `normalized` reads the register's "
                "SURNAME FORENAME back as a name and corrects no spelling. `confidence` "
                "is documented only where the register itself states a residence of COOK.",
        "records": records,
    }


def build_coverage(rows: list) -> dict:
    # A DECLARATION is a promise that something in the domain reaches the item, and the
    # gate is right to call a declared item nothing reaches a hole. Every section of
    # every township in DEPOSITS was queried; only the ones that returned a sale through
    # 1836 can be declared. The rest were read and were empty, which is a fact worth
    # keeping and is not coverage — so it is kept beside the declaration rather than
    # inside it, one block per deposit, because the two readings are two promises.
    reached = {list_name(r) for r in rows}
    truncated = ["T%s R%s sec %s" % tr for tr in sorted(TRUNCATED)]
    declarations, empty = [], []
    for dep in DEPOSITS:
        queried = ["T%dN R%dE sec %02d" % (tw, rg, sn)
                   for tw, rg in dep["pairs"] for sn in range(1, 37)]
        declarations.append({
            "unit": "list",
            "ticket": dep["ticket"],
            "note": "Read in full: the section query was walked to its end through the "
                    "More cursor, so every sale it holds through 1836 is in %s."
                    % dep["tsv"],
            "items": [n for n in queried if n in reached and n not in truncated],
        })
        empty.append({
            "ticket": dep["ticket"],
            "deposit": dep["tsv"],
            "note": "Walked section by section to the end of the results; the section "
                    "holds no sale dated on or before 31 December 1836. Read, empty, and "
                    "not a hole.",
            "items": [n for n in queried if n not in reached and n not in truncated],
        })
    townships = ", ".join("T%dN R%dE" % tr for dep in DEPOSITS for tr in dep["pairs"])
    return {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/read_land_sales.py --build",
        "note": "The reading is BY SECTION because a whole-township query stops at the "
                "database's 150-row page and looks complete. %d section queries were run "
                "(%s, third principal meridian, sections 01-36) and each was walked to "
                "its end through the results page's own More button, whose keyset cursor "
                "returns the rows after the last one shown (T-0675). Every section here "
                "is therefore read whole, including the three — 16, 21 and 29 — that "
                "T-0557 declared truncated because it took the first page for the whole. "
                "A declaration promises that a record reaches the item, so a section that "
                "was walked and held no sale through 1836 is listed under "
                "`queried_no_sales_through_1836` instead — read, empty, and not a hole. "
                "T-0676 added the five ring townships, which are the last of what T-0610 "
                "asked for: nothing around the town is unread now."
                % (36 * sum(len(d["pairs"]) for d in DEPOSITS), townships),
        "declarations": declarations,
        "queried_no_sales_through_1836": empty,
        "not_read": {
            "ticket": "T-0676",
            "truncated_at_the_150_row_ceiling": truncated,
            "townships_not_read": [],
            "note": "Nothing is left unread of what T-0610 asked for: T-0675 walked the "
                    "two townships the town stands on to the end of every section, and "
                    "T-0676 did the same for the five ring townships. Both lists are kept "
                    "as the shape a future hole would fill. What remains outside this "
                    "domain is stated in the README and is not a hole in it: purchasers "
                    "whose stated residence is Cook County but whose ground lies "
                    "elsewhere, which the database cannot be asked for, and the canal "
                    "sections, which the land office did not sell.",
        },
    }


def resident_names() -> list:
    """Every person the residents layer holds, as (id, name, household id)."""
    out = []
    index = load(RESIDENTS / "index.json")
    for entry in index.get("households") or []:
        path = RESIDENTS / entry["file"]
        if not path.exists():
            continue
        hh = load(path)
        for person in hh.get("persons") or []:
            if person.get("name"):
                out.append((person.get("id"), person["name"], hh.get("id")))
    return out


def build_resident_crosswalk(rows: list, ids: dict) -> dict:
    """Propose a correspondence between a purchaser and a person the town already holds.

    THE SURNAME GATHERS THE RIVALS AND THE FORENAME DECIDES BETWEEN THEM (T-0697).
    Until this ticket the middle clause was a COUNT — exactly one person of the surname
    could exist in the residents layer — and a count of namesakes says nothing about the
    reading in hand. It made the rule fire LESS as the town grew truer: T-0514 seated 531
    people and this crosswalk LOST three rulings with nothing new read. The reading is now
    put to every person of the surname and named onto the one it agrees with, on the merge
    rules this project already ratified (`tools/namesake.py`, which restates identity
    master's M1/M2/M3 and R3/R4 and imports the directories' forename rule). Two
    survivors or none is still a refusal, written out with the rivals NAMED, because an
    absent match reads exactly like a pair nobody looked at — and "there are 5" never said
    which five people refused the reading.
    """
    # `record_ids` is the ruling's anchor: WHICH sales this purchaser spelling was
    # adjudicated from. tools/measure_research_spend.py asks for it in as many words —
    # "a spelling pair whose evidence names no unit this domain has read — write the
    # record id" — and it is provenance either way: a refusal a reader cannot trace back
    # to the rows behind it is a refusal nobody can check.
    by_name = {}
    for row in rows:
        by_name.setdefault(row["purchaser"], []).append(ids[row["purchase_no"]])
    people = resident_names()
    by_surname = {}
    for pid, name, hh in people:
        by_surname.setdefault(name.split()[-1].upper(), []).append((pid, name, hh))
    matches, refusals = [], []
    seen = set()
    for row in rows:
        as_read = row["purchaser"]
        if as_read in seen:
            continue
        seen.add(as_read)
        surname, givens = surname_of(as_read), givens_of(as_read)
        cook = row["residence"].upper() == "COOK"
        candidates = by_surname.get(surname, [])
        if not givens:
            refusals.append({
                "a": as_read, "b": "(the residents layer)",
                "rule": "%r is a surname with no forename, and a surname-only purchaser "
                        "is always a refusal against %s however well the tract agrees."
                        % (as_read, "(the residents layer)"),
                "record_ids": sorted(by_name[as_read]),
                "evidence": ["data/research/land_sales/text/" + row["_file"]],
            })
            continue
        if not candidates:
            refusals.append({
                "a": as_read, "b": "0 residents named %s" % surname.title(),
                "rule": "%s is refused against 0 residents named %s: the residents layer "
                        "holds nobody of the surname." % (as_read, surname.title()),
                "record_ids": sorted(by_name[as_read]),
                "evidence": ["data/residents/index.json"],
            })
            continue
        ruling = namesake.choose(" ".join(givens), [
            {"key": pid, "name": name, "given": " ".join(name.split()[:-1])}
            for pid, name, hh in candidates])
        if not ruling["named"]:
            rival_names = [r["name"] for r in ruling["rivals"]]
            refusals.append({
                "a": as_read,
                "b": rival_names[0] if len(rival_names) == 1
                     else "%d residents named %s" % (len(candidates), surname.title()),
                "rule": "%s is refused against %s: %s."
                        % (as_read, " and ".join(rival_names) if len(rival_names) <= 3
                           else "%d residents named %s" % (len(candidates), surname.title()),
                           ruling["why"]),
                "rivals": ruling["rivals"],
                "record_ids": sorted(by_name[as_read]),
                "evidence": ["data/residents/index.json"],
            })
            continue
        pid, name, hh = [c for c in candidates if c[0] == ruling["named"]][0]
        grade = ruling["grade"]
        why = "in full" if grade == "forename_agrees" else "as an initial only"
        matches.append({
            "purchaser_as_read": as_read,
            "record_ids": sorted(by_name[as_read]),
            "resident_id": pid,
            "resident_name": name,
            "household_id": hh,
            "match": grade,
            "rule": "%s matches %s: %s, and the forename agrees %s."
                    % (as_read, name, ruling["why"], why),
            "rivals": ruling["rivals"] if len(candidates) > 1 else [],
            "residence_column": row["residence"],
            "evidence_grade": "documented" if cook else "inferred",
            "what_it_evidences": (
                "The register states this purchaser's residence as COOK, so the sale is "
                "contemporary evidence that a man of this name lived in Cook County on "
                "the date of sale. It is not evidence that he lived in the town."
                if cook else
                "A purchase and nothing more. It dates and places a transaction; it "
                "proposes no residence, and under the ratified ladder it corroborates "
                "rather than mints."),
        })
    # T-0697, and it is the same rule read from the other end. `choose` asks which of
    # several people of a surname a reading names; this asks whether several readings
    # named onto ONE person are one man. `H Bond` is met by both HARVEY and HEMAN and
    # the initial cannot say which, and `WENTWORTH ELIJAH SEN` is the father of
    # `WENTWORTH ELIJAH` against a town holding one card. Both groups are refused
    # whole, with the rival readings named: keeping the first and dropping the rest
    # would be the count of namesakes again, wearing a hat.
    by_person = {}
    for mt in matches:
        by_person.setdefault(mt["resident_id"], []).append(mt)
    kept = []
    for mt in matches:
        group = by_person[mt["resident_id"]]
        if len(group) == 1:
            kept.append(mt)
            continue
        verdict = namesake.collide([{"key": g["purchaser_as_read"],
                                     "given": " ".join(g["purchaser_as_read"].split()[1:])}
                                    for g in group])
        if verdict["same_man"]:
            kept.append(mt)
            continue
        refusals.append({
            "a": mt["purchaser_as_read"], "b": mt["resident_name"],
            "rule": "%s is refused against %s: %s."
                    % (mt["purchaser_as_read"], mt["resident_name"], verdict["why"]),
            "rival_readings": [g["purchaser_as_read"] for g in group
                               if g["purchaser_as_read"] != mt["purchaser_as_read"]],
            "record_ids": mt["record_ids"],
            "evidence": ["data/residents/index.json"],
        })
    matches = kept
    return {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/read_land_sales.py --build",
        # T-0635. What this file adjudicates FROM, stated once at the top in the narrow
        # form T-0598 asks for. Every ruling below rests on the same deposit — the
        # Illinois public-domain tract-sales database — so a per-entry repetition would
        # say nothing a reader could not read here. Without it the second hop of
        # tools/measure_research_spend.py counted all fourteen matches UNSOURCED, which
        # is that instrument saying, correctly, that a crosswalk which cannot name what
        # it rests on cannot be spent.
        "source_id": SOURCE_ID,
        "note": "PROPOSALS, not identities. Nothing here mints a resident, regrades one, "
                "or writes to data/residents/. T-0514 and T-0515 spend this file.",
        "counts": {"purchasers": len({r["purchaser"] for r in rows}),
                   "matched": len(matches), "refused": len(refusals)},
        "matches": matches,
        "refusals": refusals,
    }


def build_crosswalk(rows: list, ids: dict) -> dict:
    """The within-domain identity layer: two spellings in THIS source, one purchaser.

    The only rule strong enough to use here is tract agreement — the same aliquot part
    of the same section entered on dates a fortnight apart, once VOID and once not, is
    the register re-writing an entry it had cancelled. That is a refusal all the same,
    because a re-entry can be a different man buying cancelled ground, and this project
    would rather carry two rows than invent one person.
    """
    by_tract = {}
    for row in rows:
        key = (row["township"], row["range"], row["section"],
               re.sub(r"(VOID|VO|FR)$", "", row["aliquot_or_lot"]))
        by_tract.setdefault(key, []).append(row)
    refusals = []
    for key, group in sorted(by_tract.items()):
        names = sorted({r["purchaser"] for r in group})
        if len(names) < 2:
            continue
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                if surname_of(a) == surname_of(b) or givens_of(a) == givens_of(b):
                    refusals.append({
                        "a": a, "b": b,
                        "rule": "%s and %s entered the same tract (T%s R%s sec %s, %s) and "
                                "are not merged: tract agreement is where two spellings "
                                "MIGHT be one man, and it is never proof that they are."
                                % (a, b, key[0], key[1], key[2], key[3]),
                        "record_ids": sorted(ids[r["purchase_no"]] for r in group
                                             if r["purchaser"] in (a, b)),
                        "evidence": sorted({"data/research/land_sales/text/" + r["_file"]
                                            for r in group}),
                    })
    return {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/read_land_sales.py --build",
        "note": "The ONLY place two differently-spelled names in this domain may become "
                "one person, in data/research/newspapers/identity.json's shape and under "
                "its rules. No merge is made here at all, and every near-pair the tract "
                "index found is written out as a refusal so the next pass does not have "
                "to find them again.",
        "passes": [{
            "ticket": dep["ticket"],
            "what": "Every pair of differently-spelled purchasers entering the same tract "
                    "in %s through 1836."
                    % " and ".join("T%dN R%dE" % tr for tr in dep["pairs"]),
            "merges": 0,
            "refusals": sum(1 for r in refusals
                            if "data/research/land_sales/text/" + dep["tsv"] in r["evidence"]),
        } for dep in DEPOSITS],
        "merges": [],
        "refusals": refusals,
    }


def build_entries(rows: list, records: list) -> dict:
    """`entries.json` — the flat, verbatim list T-0557 asked for, one object per sale."""
    return {
        "schema": 1,
        "domain": "land_sales",
        "source_id": SOURCE_ID,
        "generated_by": "tools/read_land_sales.py --build",
        "scope": "Third principal meridian, %s, every sale dated on or before "
                 "31 December 1836."
                 % ", ".join("T%dN R%dE" % tr for dep in DEPOSITS for tr in dep["pairs"]),
        "note": "Fields are the database's own, unsummarised. `tract` is derived and is "
                "the only computed field here.",
        "count": len(rows),
        "entries": [{
            "record_id": rec["id"],
            "purchase_no": row["purchase_no"],
            "purchaser_as_read": row["purchaser"],
            "purchaser_normalized": rec["normalized"],
            "residence_as_read": row["residence"],
            "social_status_as_read": row["social_status"],
            "aliquot_or_lot_as_read": row["aliquot_or_lot"],
            "section": row["section"], "township": row["township"],
            "range": row["range"], "meridian": row["meridian"], "county": row["county"],
            "acres": row["acres"], "price_per_acre": row["price_per_acre"],
            "total_price": row["total_price"], "type_of_sale": row["type_of_sale"],
            "date_purchased": iso_date(row["date_purchased"]),
            "date_purchased_as_read": row["date_purchased"],
            "volume": row["volume"], "page": row["page"],
            "tract": rec["tract"],
        } for row, rec in zip(rows, records)],
    }


GENERATED = tuple(records_name(d["tsv"]) for d in DEPOSITS) + (
    "entries.json", "coverage.json", "crosswalk.json", "resident_crosswalk.json")


def derive(domain: Path) -> dict:
    """Every generated file, from every committed deposit.

    One records file PER DEPOSIT, named after it, and the ids run on across them in
    DEPOSITS order — so the second reading appends to the first rather than renumbering
    the ids data/structures/*.json already cite.
    """
    rows = read_tsv(domain)
    out, ordered, n = {}, [], 1
    for dep in DEPOSITS:
        mine = [r for r in rows if r["_file"] == dep["tsv"]]
        recs = build_records(mine, start=n)
        n += len(mine)
        out[records_name(dep["tsv"])] = recs
        ordered += recs["records"]
    ids = {row["purchase_no"]: rec["id"] for row, rec in zip(rows, ordered)}
    out["entries.json"] = build_entries(rows, ordered)
    out["coverage.json"] = build_coverage(rows)
    out["crosswalk.json"] = build_crosswalk(rows, ids)
    out["resident_crosswalk.json"] = build_resident_crosswalk(rows, ids)
    return out


def build(domain: Path = DOMAIN, quiet: bool = False) -> int:
    out = derive(domain)
    for rel, doc in out.items():
        dump(domain / rel, doc)
    if not quiet:
        x = out["resident_crosswalk.json"]["counts"]
        print("land sales: %d sales, %d purchasers, %d matched, %d refused"
              % (out["entries.json"]["count"], x["purchasers"], x["matched"], x["refused"]))
    return 0


def check(domain: Path = DOMAIN, quiet: bool = False) -> list:
    bad = []
    missing = [d["tsv"] for d in DEPOSITS if not (domain / "text" / d["tsv"]).exists()]
    if missing:
        return ["land_sales: the deposit %s is not committed" % m for m in missing]
    out = derive(domain)
    for rel, doc in out.items():
        path = domain / rel
        if not path.exists():
            bad.append("land_sales: %s is not committed — run --build" % rel)
            continue
        if load(path) != doc:
            bad.append("land_sales: %s has drifted from the deposit — it is generated by "
                       "tools/read_land_sales.py --build and must not be hand-edited" % rel)
    if not bad and not quiet:
        print("land sales: %d sales re-derived from the deposit, no drift"
              % out["entries.json"]["count"])
    return bad


def _fixture(tmp: Path) -> Path:
    d = tmp / "land_sales"
    (d / "text").mkdir(parents=True)
    (d / "text" / DEPOSITS[0]["tsv"]).write_text(
        "\t".join(COLS) + "\n"
        + "\t".join(["0000001", "CHIPMAN ANSEL", "COOK", "", "E2NE", "04", "39N", "14E",
                     "3", "COOK", "80.00", "1.25", "100.00", "FD", "11/17/1834", "687",
                     "267"]) + "\n"
        + "\t".join(["0000002", "BRIGGS", "UNKNOWN", "", "LOT8BL47", "07", "39N", "14E",
                     "3", "COOK", "0000.00", "000.00", "40.00", "SC", "10/24/1833", "817",
                     "029"]) + "\n"
        # Section 16 is the school section, the deepest of the three the More cursor
        # opened (T-0675). A sale in it must reach coverage like any other; until then
        # the fixture could not tell "declared read" from "refused as truncated" at all.
        + "\t".join(["0000003", "HALE JOHN", "UNKNOWN", "", "LOT2BL79", "16", "39N",
                     "14E", "3", "COOK", "0000.00", "000.00", "60.00", "SC",
                     "10/22/1833", "817", "100"]) + "\n", encoding="utf-8")
    # The second deposit — the ring townships (T-0676). It is in the fixture because a
    # reading spread over two files is exactly what can go wrong quietly: ids that
    # restart, a coverage block that declares one file's sections against the other's
    # rows, a citation that names the wrong deposit.
    (d / "text" / DEPOSITS[1]["tsv"]).write_text(
        "\t".join(COLS) + "\n"
        + "\t".join(["0000004", "HUNTER EDWARD E", "UNKNOWN", "", "E2SW", "02", "38N",
                      "14E", "3", "COOK", "80.00", "1.25", "100.00", "FD", "11/15/1834",
                      "687", "260"]) + "\n", encoding="utf-8")
    build(d, quiet=True)
    return d


def self_test() -> int:
    fired = []
    with tempfile.TemporaryDirectory() as td:
        d = _fixture(Path(td))
        if check(d, quiet=True):
            print("SELF-TEST: the fixture is not green to begin with"); return 1

        recs = load(d / records_name(DEPOSITS[0]["tsv"]))
        if recs["records"][0]["confidence"] != "documented":
            print("SELF-TEST: a COOK residence must grade documented"); return 1
        fired.append("a COOK residence grades documented")
        if recs["records"][1]["confidence"] != "inferred":
            print("SELF-TEST: a purchase with no stated residence must grade inferred"); return 1
        fired.append("a purchase with no stated residence grades inferred")

        cross = load(d / "resident_crosswalk.json")
        briggs = [r for r in cross["refusals"] if r["a"] == "BRIGGS"]
        if not briggs:
            print("SELF-TEST: a surname-only purchaser must be refused"); return 1
        fired.append("a surname-only purchaser is refused")
        # A ruling that names no record is a ruling nobody can check, and the spend
        # meter counts it as nothing at all.
        if briggs[0].get("record_ids") != ["ls0002"]:
            print("SELF-TEST: a refusal must name the records it was made from"); return 1
        fired.append("a refusal names the records it was made from")

        ring = load(d / records_name(DEPOSITS[1]["tsv"]))
        if [r["id"] for r in ring["records"]] != ["ls0004"]:
            print("SELF-TEST: the second deposit's ids must continue the first's"); return 1
        if ring["records"][0]["locator"]["text_file"] != DEPOSITS[1]["tsv"]:
            print("SELF-TEST: a record must cite the deposit it is on"); return 1
        fired.append("a second deposit appends its ids and cites its own file")

        cov = load(d / "coverage.json")
        # T-0675 read the three sections T-0557 could not, so they MUST be declared now;
        # the assertion is the same discipline pointed the other way — a section whose
        # sales are in the deposit and whose coverage is silent is a hole in the record.
        if "T39N R14E sec 16" not in cov["declarations"][0]["items"]:
            print("SELF-TEST: a section whose sales are held must be declared read")
            return 1
        if cov["not_read"]["truncated_at_the_150_row_ceiling"]:
            print("SELF-TEST: no section of R14E is truncated after T-0675"); return 1
        # The ring's own declaration, under its own ticket: a second deposit that read
        # nothing would look exactly like one whose sections all came back empty.
        ringdec = [x for x in cov["declarations"] if x["ticket"] == DEPOSITS[1]["ticket"]]
        if [x["items"] for x in ringdec] != [["T38N R14E sec 02"]]:
            print("SELF-TEST: the ring deposit must declare the sections it reached"); return 1
        if "T38N R14E sec 01" not in cov["queried_no_sales_through_1836"][1]["items"]:
            print("SELF-TEST: a ring section walked and empty must be recorded as read"); return 1
        fired.append("every section walked whole is declared read, and none is truncated")

        for rel, breaker in (
            ("entries.json", lambda doc: doc.update({"count": 999})),
            ("coverage.json", lambda doc: doc["declarations"][0]["items"].append("T99N R99E sec 01")),
            ("crosswalk.json", lambda doc: doc["merges"].append({"into": "x", "from": "y"})),
            ("resident_crosswalk.json", lambda doc: doc["refusals"].clear()),
            (records_name(DEPOSITS[0]["tsv"]),
             lambda doc: doc["records"][0].update({"as_read": "CHIPMAN ANCEL"})),
            (records_name(DEPOSITS[1]["tsv"]),
             lambda doc: doc["records"][0].update({"as_read": "HUNTER EDWARD"})),
        ):
            doc = load(d / rel)
            breaker(doc)
            dump(d / rel, doc)
            if not check(d, quiet=True):
                print("SELF-TEST: a hand-edit to %s did not fail the gate" % rel); return 1
            fired.append("a hand-edit to %s fails the gate" % rel)
            build(d, quiet=True)

        tsv = d / "text" / DEPOSITS[0]["tsv"]
        tsv.write_text(tsv.read_text(encoding="utf-8").replace("E2NE", "E2NW"),
                       encoding="utf-8")
        if not check(d, quiet=True):
            print("SELF-TEST: a changed deposit did not fail the gate"); return 1
        fired.append("a changed deposit fails the gate")

    print("read_land_sales --self-test: %d assertions fire when broken" % len(fired))
    for f in fired:
        print("  · %s" % f)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.build:
        return build()
    if args.check:
        bad = check()
        for b in bad:
            print("  ✗ %s" % b)
        return 1 if bad else 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
