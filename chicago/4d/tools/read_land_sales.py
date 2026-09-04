#!/usr/bin/env python3
"""The Illinois State Archives land tract sales, read into the research shape (T-0557).

    tools/read_land_sales.py --build       derive every generated file from the TSV
    tools/read_land_sales.py --check       the gate: re-derive and refuse any drift
    tools/read_land_sales.py --self-test   the gate's assertions still fire when broken

WHAT THIS READS. `data/research/land_sales/text/*.tsv` are the committed deposits —
one per township sweep, one row per sale, every field exactly as the database printed
it, harvested by
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

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = ROOT / "data" / "research" / "land_sales"
RESIDENTS = ROOT / "data" / "residents"
SOURCE_ID = "isa_public_domain_land_tract_sales"

# THE DEPOSITS, AND WHY THIS LIST IS APPEND-ONLY. One sweep writes one deposit, and a
# record's `ls####` id is its position in this order. Those ids are cited from
# `ground.json` and from the `land_owner` block on 63 structures, so a deposit is added
# at the END of the list and an existing one never moves: reordering would silently
# repoint every one of those citations at a different sale.
#   (file, the ticket that swept it, the townships it covers)
DEPOSITS = (
    ("isa_land_tract_sales_t39n_t40n_r14e_through_1836.tsv", "T-0557",
     (("39N", "14E"), ("40N", "14E"))),
    ("isa_land_tract_sales_t39n_r13e_through_1836.tsv", "T-0677", (("39N", "13E"),)),
    ("isa_land_tract_sales_t38n_r14e_through_1836.tsv", "T-0677", (("38N", "14E"),)),
    ("isa_land_tract_sales_t38n_r15e_through_1836.tsv", "T-0677", (("38N", "15E"),)),
    ("isa_land_tract_sales_t40n_r13e_through_1836.tsv", "T-0677", (("40N", "13E"),)),
    ("isa_land_tract_sales_t41n_r14e_through_1836.tsv", "T-0677", (("41N", "14E"),)),
)
TSV = DEPOSITS[0][0]

# The sections whose query returned exactly 150 rows — the database's per-query ceiling,
# and it offers no paging. Their rows below are the first 150 the search returned and NOT
# the section; they are carried, and the section is not declared read. Naming them here is
# what stops a later pass reading the truncation as completeness. Three are the school
# section and two West Division sections of the town itself (T-0557); the fourth is the
# school section of the township immediately west (T-0677). T-0678 holds the problem of
# reading past the ceiling — section is the finest grain this source's search offers, so
# it needs a different source and not a cleverer query.
TRUNCATED = {("39N", "14E", "16"), ("39N", "14E", "21"), ("39N", "14E", "29"),
             ("39N", "13E", "16")}

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


def stem_of(tsv: str) -> str:
    """`isa_land_tract_sales_t39n_r13e_through_1836.tsv` -> `t39n_r13e_through_1836`."""
    return tsv[len("isa_land_tract_sales_"):-len(".tsv")]


def read_deposit(domain: Path, tsv: str, ticket: str) -> list:
    lines = (domain / "text" / tsv).read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    if head != COLS:
        raise SystemExit("land_sales: %s's header is not the harvest's header" % tsv)
    rows = []
    for n, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) != len(COLS):
            raise SystemExit("land_sales: %s line %d has %d cells, not %d"
                             % (tsv, n, len(cells), len(COLS)))
        row = dict(zip(COLS, cells))
        row["_line"], row["_file"], row["_ticket"] = n, tsv, ticket
        rows.append(row)
    return rows


def read_tsv(domain: Path) -> list:
    """Every committed deposit, in DEPOSITS order — which is what fixes the record ids."""
    rows = []
    for tsv, ticket, _ in DEPOSITS:
        if (domain / "text" / tsv).exists():
            rows += read_deposit(domain, tsv, ticket)
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


def build_records(rows: list) -> dict:
    records = []
    for i, row in enumerate(rows, start=1):
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
                "truncated_section": (row["township"], row["range"], row["section"]) in
                                     [tuple(t) for t in TRUNCATED],
            },
            "tract": tract(row),
        })
    return records


def records_doc(tsv: str, ticket: str, records: list) -> dict:
    return {
        "schema": 1,
        "domain": "land_sales",
        "source_id": SOURCE_ID,
        "generated_by": "tools/read_land_sales.py --build",
        "deposit": "text/" + tsv,
        "ticket": ticket,
        "note": "Every field is the database's own. `normalized` reads the register's "
                "SURNAME FORENAME back as a name and corrects no spelling. `confidence` "
                "is documented only where the register itself states a residence of COOK.",
        "records": records,
    }


def build_coverage(rows: list) -> dict:
    # A DECLARATION is a promise that something in the domain reaches the item, and the
    # gate is right to call a declared item nothing reaches a hole. Every section of every
    # swept township was queried; only the ones that returned a sale through 1836 can be
    # declared. The rest were read and were empty, which is a fact worth keeping and is
    # not coverage — so it is kept beside the declaration rather than inside it. Each
    # sweep declares under its own ticket, because a declaration that cannot be traced to
    # the pass that made it cannot be audited.
    truncated = ["T%s R%s sec %s" % tr for tr in sorted(TRUNCATED)]
    by_ticket, empty = {}, []
    for tsv, ticket, townships in DEPOSITS:
        reached = sorted({list_name(r) for r in rows if r["_file"] == tsv})
        queried = ["T%s R%s sec %02d" % (tw, rg, s)
                   for tw, rg in townships for s in range(1, 37)]
        by_ticket.setdefault(ticket, []).extend(n for n in reached if n not in truncated)
        empty.extend(n for n in queried if n not in reached and n not in truncated)
    return {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/read_land_sales.py --build",
        "note": "The reading is BY SECTION because the database returns at most 150 rows "
                "per query and offers no paging. Two hundred and fifty-two section "
                "queries were run — seven townships of the third principal meridian, "
                "sections 01-36 each: T39N R14E and T40N R14E, the two the town stands "
                "on (T-0557), and the five that ring them, T39N R13E, T38N R14E, "
                "T38N R15E, T40N R13E and T41N R14E (T-0677). A section that returned "
                "fewer than 150 rows was read whole. The four that returned exactly 150 "
                "are NOT declared here: what this project holds for them is the first 150 "
                "rows the search would give, and declaring that as coverage would record a "
                "ceiling as a completed read. A declaration promises that a record reaches "
                "the item, so a section that was queried and held no sale through 1836 is "
                "listed under `queried_no_sales_through_1836` instead — read, empty, and "
                "not a hole.",
        "declarations": [{
            "unit": "list",
            "ticket": ticket,
            "note": "Read in full: the section query returned fewer than the database's "
                    "150-row ceiling, so every sale it holds through 1836 is in the "
                    "deposit.",
            "items": sorted(items),
        } for ticket, items in sorted(by_ticket.items())],
        "queried_no_sales_through_1836": {
            "ticket": "T-0557, T-0677",
            "note": "Queried section by section and read whole; the section holds no sale "
                    "dated on or before 31 December 1836. Read, empty, and not a hole.",
            "items": sorted(empty),
        },
        "not_read": {
            "ticket": "T-0678",
            "truncated_at_the_150_row_ceiling": truncated,
            "townships_not_read": [],
            "note": "An undeclared item is not read yet and is not a fault. The ring "
                    "townships T-0557 left unread were swept by T-0677 and none is left. "
                    "What remains is the ceiling itself: the search offers "
                    "section/township/range/meridian and county and nothing finer, and the "
                    "result page has no paging, offset or sort, so these four sections "
                    "need a different source rather than a narrower query. T-0678 holds "
                    "it.",
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


def build_resident_crosswalk(rows: list) -> dict:
    """Propose a correspondence between a purchaser and a person the town already holds.

    ONE rule, and it is deliberately the strictest of the ones this project uses: the
    surname must agree, exactly one person of that surname may exist in the residents
    layer, and the purchaser's first forename must agree with that person's first
    forename in full — or be a single initial that matches it, which is a weaker match
    and is graded as one. Everything else is a refusal, written out with the rule that
    made it, because an absent match reads exactly like a pair nobody looked at.
    """
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
                "evidence": ["data/research/land_sales/text/" + TSV],
            })
            continue
        if len(candidates) != 1:
            refusals.append({
                "a": as_read,
                "b": "%d residents named %s" % (len(candidates), surname.title()),
                "rule": "%s is refused against %s: the rule needs exactly one person of "
                        "the surname in the residents layer, and there are %d."
                        % (as_read, "%d residents named %s" % (len(candidates), surname.title()),
                           len(candidates)),
                "evidence": ["data/residents/index.json"],
            })
            continue
        pid, name, hh = candidates[0]
        their = name.split()[0].upper()
        mine = givens[0]
        if mine == their:
            grade, why = "forename_agrees", "in full"
        elif len(mine) == 1 and their.startswith(mine):
            grade, why = "initial_agrees", "as an initial only"
        else:
            refusals.append({
                "a": as_read, "b": name,
                "rule": "%s is refused against %s: the surname agrees and the forename "
                        "does not." % (as_read, name),
                "evidence": ["data/residents/" + (RESIDENTS / "index.json").name],
            })
            continue
        matches.append({
            "purchaser_as_read": as_read,
            "resident_id": pid,
            "resident_name": name,
            "household_id": hh,
            "match": grade,
            "rule": "%s matches %s: the residents layer holds exactly one person of the "
                    "surname and the forename agrees %s." % (as_read, name, why),
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
    return {
        "schema": 1,
        "domain": "land_sales",
        "generated_by": "tools/read_land_sales.py --build",
        "note": "PROPOSALS, not identities. Nothing here mints a resident, regrades one, "
                "or writes to data/residents/. T-0514 and T-0515 spend this file.",
        "counts": {"purchasers": len({r["purchaser"] for r in rows}),
                   "matched": len(matches), "refused": len(refusals)},
        "matches": matches,
        "refusals": refusals,
    }


def build_crosswalk(rows: list) -> dict:
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
                        "evidence": ["data/research/land_sales/text/" + TSV],
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
        "passes": [{"ticket": "T-0557", "what": "Every pair of differently-spelled "
                    "purchasers entering the same tract in T39N R14E and T40N R14E "
                    "through 1836.", "merges": 0, "refusals": len(refusals)}],
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
        "scope": "Third principal meridian, seven townships — T39N and T40N R14E, the "
                 "two the town stands on, and the five that ring them: T39N R13E, "
                 "T38N R14E, T38N R15E, T40N R13E and T41N R14E — every sale dated on or "
                 "before 31 December 1836.",
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


GENERATED = tuple("records/entries_%s.json" % stem_of(d[0]) for d in DEPOSITS) + (
    "entries.json", "coverage.json", "crosswalk.json", "resident_crosswalk.json")


def derive(domain: Path) -> dict:
    rows = read_tsv(domain)
    records = build_records(rows)
    out = {}
    for tsv, ticket, _ in DEPOSITS:
        if not (domain / "text" / tsv).exists():
            continue
        out["records/entries_%s.json" % stem_of(tsv)] = records_doc(
            tsv, ticket, [rec for rec, row in zip(records, rows) if row["_file"] == tsv])
    out["entries.json"] = build_entries(rows, records)
    out["coverage.json"] = build_coverage(rows)
    out["crosswalk.json"] = build_crosswalk(rows)
    out["resident_crosswalk.json"] = build_resident_crosswalk(rows)
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
    if not (domain / "text" / TSV).exists():
        return ["land_sales: the deposit %s is not committed" % TSV]
    # A deposit the harvest wrote and this file does not list would be committed evidence
    # that nothing reads — the quietest way a research domain goes wrong. It is a gate
    # failure, not a warning.
    listed = {d[0] for d in DEPOSITS}
    for f in sorted((domain / "text").glob("*.tsv")):
        if f.name not in listed:
            bad.append("land_sales: the deposit %s is committed and is not in DEPOSITS — "
                       "nothing reads it. Append it to tools/read_land_sales.py." % f.name)
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
    (d / "text" / TSV).write_text(
        "\t".join(COLS) + "\n"
        + "\t".join(["0000001", "CHIPMAN ANSEL", "COOK", "", "E2NE", "04", "39N", "14E",
                     "3", "COOK", "80.00", "1.25", "100.00", "FD", "11/17/1834", "687",
                     "267"]) + "\n"
        + "\t".join(["0000002", "BRIGGS", "UNKNOWN", "", "LOT8BL47", "07", "39N", "14E",
                     "3", "COOK", "0000.00", "000.00", "40.00", "SC", "10/24/1833", "817",
                     "029"]) + "\n", encoding="utf-8")
    build(d, quiet=True)
    return d


def self_test() -> int:
    fired = []
    with tempfile.TemporaryDirectory() as td:
        d = _fixture(Path(td))
        if check(d, quiet=True):
            print("SELF-TEST: the fixture is not green to begin with"); return 1

        recs = load(d / ("records/entries_%s.json" % stem_of(TSV)))
        if recs["records"][0]["confidence"] != "documented":
            print("SELF-TEST: a COOK residence must grade documented"); return 1
        fired.append("a COOK residence grades documented")
        if recs["records"][1]["confidence"] != "inferred":
            print("SELF-TEST: a purchase with no stated residence must grade inferred"); return 1
        fired.append("a purchase with no stated residence grades inferred")

        cross = load(d / "resident_crosswalk.json")
        if not any(r["a"] == "BRIGGS" for r in cross["refusals"]):
            print("SELF-TEST: a surname-only purchaser must be refused"); return 1
        fired.append("a surname-only purchaser is refused")

        cov = load(d / "coverage.json")
        if any(i in cov["declarations"][0]["items"] for i in ("T39N R14E sec 16",
                                                             "T39N R14E sec 21",
                                                             "T39N R14E sec 29")):
            print("SELF-TEST: a truncated section must not be declared read"); return 1
        fired.append("a section truncated at the 150-row ceiling is not declared read")

        for rel, breaker in (
            ("entries.json", lambda doc: doc.update({"count": 999})),
            ("coverage.json", lambda doc: doc["declarations"][0]["items"].append("T99N R99E sec 01")),
            ("crosswalk.json", lambda doc: doc["merges"].append({"into": "x", "from": "y"})),
            ("resident_crosswalk.json", lambda doc: doc["refusals"].clear()),
            ("records/entries_%s.json" % stem_of(TSV),
             lambda doc: doc["records"][0].update({"as_read": "CHIPMAN ANCEL"})),
        ):
            doc = load(d / rel)
            breaker(doc)
            dump(d / rel, doc)
            if not check(d, quiet=True):
                print("SELF-TEST: a hand-edit to %s did not fail the gate" % rel); return 1
            fired.append("a hand-edit to %s fails the gate" % rel)
            build(d, quiet=True)

        stray = d / "text" / "isa_land_tract_sales_t99n_r99e_through_1836.tsv"
        stray.write_text("\t".join(COLS) + "\n", encoding="utf-8")
        if not any("is committed and is not in DEPOSITS" in b for b in check(d, quiet=True)):
            print("SELF-TEST: a deposit nothing reads did not fail the gate"); return 1
        fired.append("a committed deposit no DEPOSITS entry reads fails the gate")
        stray.unlink()

        line = (d / "text" / TSV).read_text(encoding="utf-8").replace("E2NE", "E2NW")
        (d / "text" / TSV).write_text(line, encoding="utf-8")
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
