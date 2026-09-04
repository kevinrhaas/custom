#!/usr/bin/env python3
"""The federal tract sales, SPENT on the people they name (T-0635, consolidation pass 2).

    python3 tools/spend_land_sales.py             write the ledger and the cards
    python3 tools/spend_land_sales.py --check     everything re-derives; nothing drifted
    python3 tools/spend_land_sales.py --report    person by person, which sales meet them
    python3 tools/spend_land_sales.py --self-test the rules below, held over what it derives

WHY THIS EXISTS. `tools/measure_research_spend.py` asks whether a ruling that names a
person in this town ever reached that PERSON'S CARD. On the morning of 2026-09-05 it
answered, for land_sales, that the domain had reached nobody at all — and that was the
instrument being wrong twice over, which is the finding consolidation pass 2 opened with:

  * `resident_crosswalk.json` states its verdict as the ARRAY HEADING (`matches`) and puts
    no `outcome` on the entry, and the second hop read the verdict from `outcome` alone.
    Thirty-five rulings binding a purchaser to a person this town holds were invisible.
  * the same file stated no `source_id`, so even once seen not one of the thirty-five was
    judgeable: a ruling that never says what it rests on cannot be checked against a card.

Both are fixed in the commit that adds this file, and what they uncovered is this pass's
work: thirty-five rulings, thirty-one people, no card citing the register.

WHAT THE REGISTER IS, and the discipline it forces. The Illinois State Archives' Public
Domain Land Tract Sales database records who ENTERED a tract of federal land, when, at
what price. It is not a list of residents and the domain's own README says so: the only
column that speaks to where a purchaser lived is `Residence`, and for thirty-two of these
thirty-five rulings it reads UNKNOWN (two read ILLINOIS, one COOK — none of them reads
Chicago). So a sale corroborates that a man of that name was transacting for ground around
this town in these years. It places nobody, houses nobody, and grades nobody.

WHAT IS AND IS NOT WRITTEN, in four rules.

  1. ONLY WHAT THE CROSSWALK ALREADY DECLARED. This pass re-adjudicates nothing. It reads
     `matches` and writes those; the 396 refusals name nobody to write to. Re-running it
     after a re-adjudication moves exactly the rows the re-adjudication moved.

  2. TWO FIELDS AND NO OTHERS. A person gains the source id in `sources` and a paragraph in
     `note`. Nothing else is touched — not a grade, not an arrival, not a claim block, not
     a placement. `--self-test` holds that by diffing a record through the applier and
     asserting the changed key set.

  3. NO GRADE MOVES. The ratified ladder (T-0513) is applied by T-0515 against every source
     at once; a pass that wrote the evidence and graded off it in the same breath would be
     marking its own work. The count of grades this pass changes is zero and `--check`
     holds it there. This is pass 1's rule (T-0634) unchanged.

  4. THE FOUR INITIAL-ONLY MATCHES ARE WRITTEN, and the clause that admits them is named
     rather than assumed. `PRUYNE P`, `PRUYNE P AND CO`, `GARRETT A ET CO` and `PEARSONS H`
     agree with their person on the surname and on an initial, with exactly one bearer of
     the surname in the layer. T-0670, closed inside this pass's own window, ratified the
     boundary in as many words: *"an initial against a full name stays a match; two full
     names that differ do not."* None of the four puts two full forenames against each
     other. Every card says which of its spellings was initial-only, so a reader can see
     the weaker half of the evidence without opening the crosswalk.

THE LEDGER IS NOT A CROSSWALK, deliberately, and for the reason pass 1 wrote down:
`measure_research_spend.py` counts any file with "crosswalk" in its name as an
adjudication, so a ledger of WRITES named like one would report thirty-one new rulings
reaching a person and thirty-one of them written — the pass grading its own homework and
inflating both columns of the measurement it exists to move.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAND = ROOT / "data" / "research" / "land_sales"
CROSSWALK = LAND / "resident_crosswalk.json"
RECORDS_DIR = LAND / "records"
LEDGER = LAND / "land_sales_spend_1835.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"

SCHEMA = 1

# The one source this whole domain reads from, and the only id written onto a card.
SOURCE_ID = "isa_public_domain_land_tract_sales"

# The sentence that says a paragraph is this pass's, so re-running it is idempotent and
# `--check` can find its own work without guessing.
MARKER = "THE FEDERAL TRACT SALES — A TRANSACTION, NOT A RESIDENCE."

LADDER_LIMIT = (
    "This pass WRITES THE EVIDENCE AND MOVES NO GRADE — under the ratified ladder (T-0513) "
    "the grade is applied by T-0515 against every source at once, and a purchase "
    "corroborates rather than mints.")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc) -> None:
    path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


# --- what the crosswalk already ruled -------------------------------------------------

def records_index() -> dict:
    out = {}
    for path in sorted(RECORDS_DIR.glob("*.json")):
        for row in load(path).get("records") or []:
            out[row["id"]] = row
    return out


def matches() -> list:
    """One row per PERSON the crosswalk matched, folding that person's spellings together.

    Order is the crosswalk's own — a ledger that re-sorted its input would stop being a
    re-derivation of it — and inside a person the spellings keep the order they were read
    in. Three people carry two purchaser spellings apiece (Hiram Pearsons, Walter Loomis
    Newberry, Peter Pruyne) and one paragraph naming both is easier to read than two
    paragraphs saying the same thing twice.
    """
    recs = records_index()
    order: list = []
    seen: dict = {}
    for entry in load(CROSSWALK)["matches"]:
        key = (entry["household_id"], entry["resident_id"])
        if key not in seen:
            seen[key] = {
                "household_id": entry["household_id"],
                "person_id": entry["resident_id"],
                "resident_name": entry["resident_name"],
                "source_id": SOURCE_ID,
                "spellings": [],
            }
            order.append(seen[key])
        sales = [recs[r] for r in entry["record_ids"] if r in recs]
        dates = sorted(s["sale"]["date_purchased"] for s in sales
                       if (s.get("sale") or {}).get("date_purchased"))
        tracts = sorted({(s.get("locator") or {}).get("list") for s in sales
                         if (s.get("locator") or {}).get("list")})
        seen[key]["spellings"].append({
            "purchaser_as_read": entry["purchaser_as_read"],
            "record_ids": list(entry["record_ids"]),
            "sales": len(entry["record_ids"]),
            "first_sale": dates[0] if dates else None,
            "last_sale": dates[-1] if dates else None,
            "tracts": tracts,
            "match": entry["match"],
            "rule": entry["rule"],
            "residence_column": entry["residence_column"],
            "evidence_grade": entry["evidence_grade"],
        })
    return order


def paragraph(row: dict) -> str:
    """What one person's card is told, and the whole of it."""
    cites = "; ".join(
        "“%s” — %d sale%s %s, %s (%s)"
        % (s["purchaser_as_read"], s["sales"], "" if s["sales"] == 1 else "s",
           ("on %s" % s["first_sale"]) if s["first_sale"] == s["last_sale"]
           else ("between %s and %s" % (s["first_sale"], s["last_sale"])),
           ", ".join(s["tracts"]) or "tract not stated",
           ", ".join(s["record_ids"][:3]) + (", …" if len(s["record_ids"]) > 3 else ""))
        for s in row["spellings"])
    residences = sorted({s["residence_column"] for s in row["spellings"]})
    initial_only = [s["purchaser_as_read"] for s in row["spellings"]
                    if s["match"] == "initial_agrees"]
    weaker = ""
    if initial_only:
        weaker = (" The spelling%s %s agree%s with this person on the surname and on an "
                  "initial only, with one bearer of the surname in the layer: a weaker "
                  "match, admitted under T-0670's clause that an initial against a full "
                  "name stays a match while two full forenames that differ do not."
                  % ("" if len(initial_only) == 1 else "s",
                     " and ".join("“%s”" % n for n in initial_only),
                     "s" if len(initial_only) == 1 else ""))
    return (
        "%s The Illinois State Archives' Public Domain Land Tract Sales database records "
        "this name entering federal ground around the town: %s. A sale is a TRANSACTION "
        "and never a residence — the register's Residence column reads %s here, so it says "
        "a man of this name was buying land in these years and nothing about where he "
        "lived or what stood on the ground. The reading is transcription-mediated; the "
        "adjudication is data/research/land_sales/resident_crosswalk.json.%s %s"
        % (MARKER, cites, " and ".join("'%s'" % r for r in residences), weaker,
           LADDER_LIMIT))


# --- the ledger -----------------------------------------------------------------------

def ledger_doc() -> dict:
    rows = matches()
    doc = load(CROSSWALK)
    per_match: dict = {}
    for row in rows:
        for s in row["spellings"]:
            per_match[s["match"]] = per_match.get(s["match"], 0) + 1
    return {
        "schema": SCHEMA,
        "_doc": (
            "GENERATED by tools/spend_land_sales.py. The ledger of T-0635's second "
            "consolidation pass: which of resident_crosswalk.json's matched rulings were "
            "written onto the card they name, and what each card was told. It is a record "
            "of WRITES, not of adjudications — the adjudication is resident_crosswalk.json "
            "and this file deliberately carries no 'crosswalk' in its name so that "
            "measure_research_spend.py does not count a write as a second ruling."),
        "generated_by": "tools/spend_land_sales.py",
        "ticket": "T-0635",
        "source_id": SOURCE_ID,
        "reads": "data/research/land_sales/resident_crosswalk.json",
        "writes": "data/residents/households/*.json — persons[].sources and persons[].note",
        "counts": {
            "matched_rulings": len(doc["matches"]),
            "people_written": len(rows),
            "households_touched": len({r["household_id"] for r in rows}),
            "grades_changed": 0,
            "per_match_rule": per_match,
            "refused_not_written": len(doc["refusals"]),
        },
        "refusals": [
            {
                "rule": "L1",
                "why": ("a refusal names no person to write to: the crosswalk ruled that "
                        "the purchaser and the resident are not one man, and a card that "
                        "cited the register anyway would print a rejected identity"),
                "rulings": len(doc["refusals"]),
            },
            {
                "rule": "L2",
                "why": ("no grade moves here, and no placement is proposed. A purchase is "
                        "a transaction; the Residence column is the only thing in this "
                        "register that speaks to where a man lived, and it does not say "
                        "Chicago for any of these rulings"),
                "rulings": 0,
            },
        ],
        "people": rows,
    }


# --- writing the cards ----------------------------------------------------------------

def apply_to_person(person: dict, row: dict) -> bool:
    """The ONLY mutation this tool performs. Two keys, and rule 2 is held here."""
    changed = False
    if SOURCE_ID not in (person.get("sources") or []):
        person["sources"] = (person.get("sources") or []) + [SOURCE_ID]
        changed = True
    note = (person.get("note") or "").strip()
    if MARKER not in note:
        person["note"] = (note + " " + paragraph(row)).strip()
        changed = True
    return changed


def apply(quiet: bool = False) -> int:
    touched = 0
    for row in matches():
        path = HOUSEHOLDS / ("%s.json" % row["household_id"])
        hh = load(path)
        for person in hh.get("persons") or []:
            if person.get("id") != row["person_id"]:
                continue
            if apply_to_person(person, row):
                touched += 1
                dump(path, hh)
    if not quiet:
        print("land tract sales: written onto %d resident record(s)" % touched)
    return touched


def build(quiet: bool = False) -> int:
    dump(LEDGER, ledger_doc())
    apply(quiet=quiet)
    if not quiet:
        print("wrote %s" % LEDGER.relative_to(ROOT))
    return 0


# --- the gate -------------------------------------------------------------------------

def gaps(rows: list) -> list:
    """Every ruling has to be ON the record it names, or the ruling is only a file."""
    bad = []
    for row in rows:
        path = HOUSEHOLDS / ("%s.json" % row["household_id"])
        if not path.exists():
            bad.append("%s: household %s no longer exists"
                       % (row["person_id"], row["household_id"]))
            continue
        person = next((p for p in load(path).get("persons") or []
                       if p.get("id") == row["person_id"]), None)
        if person is None:
            bad.append("%s: person is no longer in %s"
                       % (row["person_id"], row["household_id"]))
            continue
        if SOURCE_ID not in (person.get("sources") or []):
            bad.append("%s is matched to the tract sales and its record does not cite "
                       "'%s' — run tools/spend_land_sales.py" % (row["person_id"], SOURCE_ID))
        if MARKER not in (person.get("note") or ""):
            bad.append("%s is matched to the tract sales and its record does not say what "
                       "they are worth — run tools/spend_land_sales.py" % row["person_id"])
    return bad


def strays(rows: list) -> list:
    """And nobody the crosswalk did NOT match may carry this pass's paragraph."""
    wanted = {(r["household_id"], r["person_id"]) for r in rows}
    bad = []
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        hh = load(path)
        for person in hh.get("persons") or []:
            if MARKER not in (person.get("note") or ""):
                continue
            if (hh.get("id"), person.get("id")) not in wanted:
                bad.append("%s carries this pass's paragraph and the crosswalk matches no "
                           "sale to it" % person.get("id"))
    return bad


def check(quiet: bool = False) -> int:
    faults = []
    rows = matches()
    if LEDGER.exists():
        if load(LEDGER) != ledger_doc():
            faults.append("%s no longer re-derives from resident_crosswalk.json — run "
                          "tools/spend_land_sales.py" % LEDGER.name)
    else:
        faults.append("%s is missing — run tools/spend_land_sales.py" % LEDGER.name)
    faults += gaps(rows)
    faults += strays(rows)
    if faults:
        print("land-sales spend: %d fault(s)" % len(faults))
        for f in faults[:40]:
            print("   " + f)
        return 1
    if not quiet:
        print("land-sales spend: %d ruling(s) on %d card(s), all written, no strays"
              % (sum(len(r["spellings"]) for r in rows), len(rows)))
    return 0


def report() -> int:
    for row in matches():
        print("%-28s %s" % (row["person_id"], row["resident_name"]))
        for s in row["spellings"]:
            print("    %-22s %2d sale(s)  %s  %s"
                  % (s["purchaser_as_read"], s["sales"], s["match"],
                     ", ".join(s["tracts"])))
    return 0


# --- the self-test --------------------------------------------------------------------

def self_test() -> int:
    fired = []

    def fires(label: str, ok: bool):
        fired.append(label)
        if not ok:
            print("SELF-TEST FAILED: %s" % label)
            raise SystemExit(1)

    rows = matches()
    fires("the crosswalk's matched rulings all reach a person",
          all(r["person_id"] and r["household_id"] for r in rows))

    # Rule 2, held by diffing a record through the applier.
    person = {"id": "x", "name": "X", "grade": "inferred", "sources": ["s"], "note": "n"}
    before = json.loads(json.dumps(person))
    apply_to_person(person, rows[0])
    changed = {k for k in set(person) | set(before) if person.get(k) != before.get(k)}
    fires("the applier touches `sources` and `note` and nothing else",
          changed == {"sources", "note"})
    fires("the applier is idempotent", apply_to_person(person, rows[0]) is False)
    fires("no grade moves", person["grade"] == before["grade"])

    # Rule 4: an initial-only spelling says so on the card, naming the clause.
    initial = next(r for r in rows
                   if any(s["match"] == "initial_agrees" for s in r["spellings"]))
    fires("an initial-only match names T-0670's clause on the card",
          "T-0670" in paragraph(initial))
    full = next(r for r in rows
                if all(s["match"] == "forename_agrees" for s in r["spellings"]))
    fires("a full-forename match does not claim a clause it did not need",
          "T-0670" not in paragraph(full))

    # The paragraph may never say the register places anybody.
    fires("every paragraph says a sale is not a residence",
          all("never a residence" in paragraph(r) for r in rows))

    # The ledger is not a crosswalk, and the reason is load-bearing.
    fires("the ledger's own name keeps it out of the spend measure",
          "crosswalk" not in LEDGER.name)

    print("land-sales spend self-test: %d assertion(s) fired" % len(fired))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.check:
        return check()
    if args.report:
        return report()
    return build()


if __name__ == "__main__":
    sys.exit(main())
