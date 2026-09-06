#!/usr/bin/env python3
"""The federal land tract sales, spent on the people they name (T-0636, consolidation pass 3).

    python3 tools/spend_land_sales.py             write the ledger and the cards
    python3 tools/spend_land_sales.py --check     everything re-derives; nothing drifted
    python3 tools/spend_land_sales.py --report    person by person, what the register sold them
    python3 tools/spend_land_sales.py --self-test the rules below, held over what it derives

WHY THIS EXISTS. T-0634 was consolidation pass 1 and spent the town's own rolls of
1833-1835; T-0635 was pass 2 and spent Fergus 1839's two later lists. This is pass 3, and
its window opens where pass 2 closed. One crosswalk landed in that window whose rulings
name a person this town holds a card for and had never reached that card:

    data/research/land_sales/resident_crosswalk.json   T-0557 / T-0676   35 residents matched

`tools/measure_research_spend.py`'s second hop reported land_sales at 35 reached, 35
judgeable and 0 on a card — the largest single unwritten block left in the town, and the
whole of the gap that pass 3 can close. The other three unwritten rulings in the same
measurement are Fergus 1839's Fort Dearborn lot bids, and they are NOT taken here: they
have a ticket of their own, T-0681, and a pass that swept up another ticket's work would
leave the queue lying about what is left to do.

WHAT THIS SOURCE IS, AND THE LIMIT THAT TRAVELS WITH IT. The register is the Illinois
State Archives' Public Domain Land Tract Sales database, read for the townships around
Chicago through 1836. A row says a NAME ENTERED A TRACT ON A DAY. It does not say the
purchaser lived there, or lived anywhere; the register's own `Residence` column is the only
thing on the page that speaks to residence at all, and on these 35 people it reads COOK,
ILLINOIS or UNKNOWN — a county, a state, or nothing, and never a town. So the paragraph
written onto a card says purchase and says it in those words, and the crosswalk's own
`what_it_evidences` sentence is quoted onto every card rather than paraphrased.

WHAT IS AND IS NOT WRITTEN, in four rules — pass 1's and pass 2's rules, unchanged, because
the defect they guard against is the same one.

  1. ONLY WHAT THE CROSSWALK ALREADY DECLARED. This pass re-adjudicates nothing. It reads
     `matches[]` and writes those. The 396 `refusals` are rivals still standing and write
     nothing.

  2. TWO FIELDS AND NO OTHERS. A person gains the source id in `sources` and a paragraph in
     `note`. Nothing else is touched — not a grade, not an arrival, not a claim block, not
     a placement, and above all not `present_on_scene_date`. `--self-test` holds that by
     diffing a record through the applier and asserting the changed key set.

  3. NO GRADE MOVES, and here the crosswalk itself forbids it: every match carries
     `what_it_evidences` — "A purchase and nothing more… under the ratified ladder it
     corroborates rather than mints." That sentence is quoted onto every card this pass
     writes, so the limit travels with the evidence. T-0515 applies the ladder against every
     source at once.

  4. ONE PARAGRAPH PER PERSON, NOT PER ENTRY. Peter Pruyne is matched three times — as
     PRUYNE P, as PRUYNE P AND CO and as PRUYNE PETER — and is told once, in a paragraph
     naming all three readings and every record id behind them, so nothing is lost by the
     fold.

THE LEDGER IS NOT A CROSSWALK, deliberately, and for the reason passes 1 and 2 gave:
`data/research/land_sales/resident_spend_1835.json` carries no "crosswalk" in its name so
that `measure_research_spend.py` does not read a record of WRITES as a second adjudication
and report the pass grading its own homework.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAND_SALES = ROOT / "data" / "research" / "land_sales"
CROSSWALK = LAND_SALES / "resident_crosswalk.json"
RECORDS = LAND_SALES / "records"
LEDGER = LAND_SALES / "resident_spend_1835.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"

SCHEMA = 1

# The register, and the only id written onto a card. The crosswalk states it at the top of
# the file and every record file states the same one.
SOURCE_ID = "isa_public_domain_land_tract_sales"

# The sentence that says a paragraph is this pass's, so re-running it is idempotent and
# `--check` can find its own work without guessing.
MARKER = "THE FEDERAL LAND TRACT SALES — A PURCHASE, AND NEVER A RESIDENCE."

# THE SAME REGISTER, IN A PASS THIS ONE SUPERSEDED (T-0677). This tool was rewritten between
# T-0635 and T-0636, and the earlier version is still pushed on `steward/salvage-t0635-mine`
# — where T-0677's own text sends the next run to find it. Run it against dev today and all
# thirty-one of these cards gain a SECOND paragraph about the tract sales, differently worded
# and saying the same thing. Neither gate below could see that: `gaps` asks only whether the
# paragraph is PRESENT and `strays` only whether an unruled card carries one. T-0677 measured
# it — `tools/check.sh` went green with every one of the thirty-one cards doubled. `doubles`
# is that hole closed, and this tuple is what a superseded paragraph looks like.
SUPERSEDED_MARKERS = (
    "THE FEDERAL TRACT SALES — A TRANSACTION, NOT A RESIDENCE.",
)

LADDER_LIMIT = (
    "This pass WRITES THE EVIDENCE AND MOVES NO GRADE. Under the ratified ladder (T-0513) a "
    "second independent source is what lifts a projected resident, and a land entry is a "
    "second source about a TRANSACTION rather than about who was living at Chicago on 1 July "
    "1835 — a man may buy a quarter-section he never sees. T-0515 applies the ladder against "
    "every source at once; this pass hands it the evidence and not the verdict."
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc) -> None:
    path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


# --- what the register says ------------------------------------------------------------

def records() -> dict:
    """Every land-sale row this project has read, by id."""
    out = {}
    for path in sorted(RECORDS.glob("*.json")):
        doc = load(path)
        for row in doc.get("records") or []:
            out[row["id"]] = row
    return out


def tract_of(row: dict) -> str:
    """A tract as a reader of the register would name it.

    THE REGISTER SELLS TWO DIFFERENT THINGS and the difference matters to this town. Most
    rows are country land — a part of a section, entered from the government and priced by
    the acre. But the school section, T39N R14E section 16, was platted and sold by the lot
    and by the block at the sale of 1833: those rows are `SC`, they name a lot and a block
    or a bare block, and most of them state 0000.00 acres because there are no acres to
    state. A summary that folded the two together would report a man who bought seven lots
    inside the town as having bought nothing at all.
    """
    t = row.get("tract") or {}
    where = "sec %s T%s R%s" % (t.get("section"), t.get("township"), t.get("range"))
    if t.get("resolves") == "town_lot" and t.get("lot") and t.get("block"):
        return "lot %s of block %s of the school section (%s)" % (t["lot"], t["block"], where)
    part = t.get("part") or "—"
    if (row.get("sale") or {}).get("type_of_sale") == "SC":
        return "%s of the school section (%s), as read" % (part, where)
    return "%s %s" % (part, where)


def entry(rid: str, row: dict) -> dict:
    """One register row, reduced to what a card is told about it."""
    sale = row.get("sale") or {}
    loc = row.get("locator") or {}
    return {
        "record_id": rid,
        "as_read": row.get("as_read"),
        "date_purchased": sale.get("date_purchased"),
        "acres": sale.get("acres"),
        "total_price": sale.get("total_price"),
        "type_of_sale": sale.get("type_of_sale_expanded") or sale.get("type_of_sale"),
        "residence_as_read": sale.get("residence_as_read"),
        "county": sale.get("county"),
        "tract": tract_of(row),
        "resolves": (row.get("tract") or {}).get("resolves"),
        "sale_kind": ("school_section" if sale.get("type_of_sale") == "SC"
                      else "federal_entry"),
        "purchase_no": loc.get("purchase_no"),
        "volume": sale.get("volume"),
        "page": sale.get("page"),
    }


def matches() -> list:
    """One row per PERSON, folding a person's several purchaser spellings together.

    Order is the crosswalk's own — a ledger that re-sorted its input would stop being a
    re-derivation of it — and a person matched more than once keeps the position their
    first match gave them.
    """
    rows = records()
    order: list = []
    seen: dict = {}
    for m in load(CROSSWALK)["matches"]:
        key = (m["household_id"], m["resident_id"])
        if key not in seen:
            seen[key] = {
                "household_id": m["household_id"],
                "person_id": m["resident_id"],
                "name": m.get("resident_name"),
                "source_id": SOURCE_ID,
                "purchaser_spellings": [],
                "rules": [],
                "carry": [],
                "entries": [],
            }
            order.append(seen[key])
        cell = seen[key]
        spelling = m.get("purchaser_as_read")
        if spelling and spelling not in cell["purchaser_spellings"]:
            cell["purchaser_spellings"].append(spelling)
        if m.get("rule") and m["rule"] not in cell["rules"]:
            cell["rules"].append(m["rule"])
        if m.get("what_it_evidences") and m["what_it_evidences"] not in cell["carry"]:
            cell["carry"].append(m["what_it_evidences"])
        for rid in m.get("record_ids") or []:
            row = rows.get(rid)
            if row is None:
                continue
            cell["entries"].append(entry(rid, row))
    return order


def totals(row: dict) -> dict:
    """Acres, dollars and the span of dates — summed off the rows, never retyped."""
    def num(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
    dates = sorted(e["date_purchased"] for e in row["entries"] if e.get("date_purchased"))
    lots = [e for e in row["entries"] if e.get("sale_kind") == "school_section"]
    country = [e for e in row["entries"] if e.get("sale_kind") != "school_section"]
    return {
        "entries": len(row["entries"]),
        "acres": round(sum(num(e["acres"]) for e in row["entries"]), 2),
        "dollars": round(sum(num(e["total_price"]) for e in row["entries"]), 2),
        "first_purchase": dates[0] if dates else None,
        "last_purchase": dates[-1] if dates else None,
        "tracts": sorted({e["tract"] for e in country}),
        "school_section": sorted({e["tract"] for e in lots}),
        "residence_as_read": sorted({e["residence_as_read"] or "UNKNOWN"
                                     for e in row["entries"]}),
    }


# --- what a card is told ---------------------------------------------------------------

def paragraph(row: dict) -> str:
    """What one person's card is told, and the whole of it."""
    t = totals(row)
    spellings = ", ".join("“%s”" % s for s in row["purchaser_spellings"])
    span = (t["first_purchase"] if t["first_purchase"] == t["last_purchase"]
            else "%s to %s" % (t["first_purchase"], t["last_purchase"]))
    ids = ", ".join(e["record_id"] for e in row["entries"])
    residence = ", ".join(t["residence_as_read"])
    bought = []
    if t["tracts"]:
        bought.append("%d federal land entr%s — %s"
                      % (len(t["tracts"]), "y" if len(t["tracts"]) == 1 else "ies",
                         "; ".join(t["tracts"])))
    if t["school_section"]:
        bought.append("%d parcel%s of the school section — %s"
                      % (len(t["school_section"]),
                         "" if len(t["school_section"]) == 1 else "s",
                         "; ".join(t["school_section"])))
    lot_note = (" THE SCHOOL-SECTION ROWS ARE GROUND INSIDE THE TOWN, NOT FARMLAND: section "
                "16 of T39N R14E was platted and sold off by lot and by block at the sale of "
                "1833, which is why the register states 0000.00 acres against most of them. "
                "Ground inside the town is nearer to this reconstruction than a "
                "quarter-section is, and it is still a purchase: the register names a "
                "purchaser and never an occupant, and nothing here puts this person on that "
                "ground." if t["school_section"] else "")
    return (
        "%s The Illinois State Archives' Public Domain Land Tract Sales register enters this "
        "person %d time%s, as %s, %s: %s, %.2f acres stated in all, for $%.2f (%s). THE "
        "REGISTER'S OWN RESIDENCE COLUMN "
        "READS %s on these rows: a county, a state or nothing, and never a town, which is why "
        "a purchase here places nobody.%s %s Identity by the crosswalk's own rule: %s "
        "(data/research/land_sales/resident_crosswalk.json). %s"
        % (MARKER, t["entries"], "" if t["entries"] == 1 else "s", spellings, span,
           " and ".join(bought), t["acres"], t["dollars"], ids, residence, lot_note,
           " ".join(row["carry"]),
           row["rules"][0] if row["rules"] else "stated in the crosswalk", LADDER_LIMIT))


# --- the ledger ------------------------------------------------------------------------

def ledger_doc() -> dict:
    rows = matches()
    xw = load(CROSSWALK)
    return {
        "schema": SCHEMA,
        "_doc": (
            "GENERATED by tools/spend_land_sales.py. The ledger of T-0636's consolidation "
            "pass 3: which of the land-sale crosswalk's resident matches were written onto "
            "the card they name, and what each card was told. It is a record of WRITES, not "
            "of adjudications — the adjudication is resident_crosswalk.json — and it "
            "deliberately carries no 'crosswalk' in its name so that "
            "measure_research_spend.py does not count a write as a second ruling."),
        "generated_by": "tools/spend_land_sales.py",
        "ticket": "T-0636",
        "pass": "consolidation pass 3",
        "source_id": SOURCE_ID,
        "reads": [
            "data/research/land_sales/resident_crosswalk.json",
            "data/research/land_sales/records/*.json",
        ],
        "writes": "data/residents/households/*.json — persons[].sources and persons[].note",
        "carry_rule": xw.get("note"),
        "counts": {
            "matched_rulings": len(xw["matches"]),
            "people_written": len(rows),
            "households_touched": len({r["household_id"] for r in rows}),
            "grades_changed": 0,
            "entries_carried": sum(len(r["entries"]) for r in rows),
            "acres_carried": round(sum(totals(r)["acres"] for r in rows), 2),
            "school_section_parcels_carried": sum(len(totals(r)["school_section"])
                                                  for r in rows),
            "matched_more_than_once": sum(1 for r in rows
                                          if len(r["purchaser_spellings"]) > 1),
        },
        "not_written": [
            {
                "rule": "L1",
                "why": ("a refusal is a rival still standing: the crosswalk did not choose "
                        "between the bearers of the name, and a card that cited the register "
                        "anyway would print an undecided identity as a decided one"),
                "rulings": xw["counts"]["refused"],
            },
            {
                "rule": "L2",
                "why": ("Fergus 1839's Fort Dearborn lot bids are the other three rulings "
                        "the second hop reports unwritten, and they belong to T-0681. A "
                        "consolidation pass that swept up another open ticket's work would "
                        "leave the queue lying about what is left to do"),
                "rulings": 3,
            },
            {
                "rule": "L3",
                "why": ("no grade moves here, and no residence is asserted. The register's "
                        "Residence column reads COOK, ILLINOIS or UNKNOWN on every one of "
                        "these rows; the ratified ladder reads every source at once and "
                        "T-0515 applies it"),
                "rulings": 0,
            },
        ],
        "people": [
            {
                "household_id": r["household_id"],
                "person_id": r["person_id"],
                "name": r["name"],
                "source_id": r["source_id"],
                "purchaser_spellings": r["purchaser_spellings"],
                "rules": r["rules"],
                "totals": totals(r),
                "entries": r["entries"],
                "written": paragraph(r),
            }
            for r in rows
        ],
    }


# --- the write -------------------------------------------------------------------------

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
        if not path.exists():
            continue
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


# --- the gate --------------------------------------------------------------------------

def _person(row: dict):
    path = HOUSEHOLDS / ("%s.json" % row["household_id"])
    if not path.exists():
        return None
    for person in load(path).get("persons") or []:
        if person.get("id") == row["person_id"]:
            return person
    return None


def gaps(rows: list) -> list:
    """Every ruling has to be ON the record it names, or the ruling is only a file."""
    bad = []
    for row in rows:
        person = _person(row)
        if person is None:
            bad.append("%s/%s — the record the ruling names does not exist"
                       % (row["household_id"], row["person_id"]))
            continue
        if SOURCE_ID not in (person.get("sources") or []):
            bad.append("%s/%s — matched by the crosswalk and the card does not cite %s"
                       % (row["household_id"], row["person_id"], SOURCE_ID))
        if MARKER not in (person.get("note") or ""):
            bad.append("%s/%s — matched by the crosswalk and the card carries no paragraph"
                       % (row["household_id"], row["person_id"]))
    return bad


def strays(rows: list) -> list:
    """…and a card may not carry this pass's paragraph without a ruling behind it."""
    ruled = {(r["household_id"], r["person_id"]) for r in rows}
    bad = []
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        hh = load(path)
        for person in hh.get("persons") or []:
            if MARKER not in (person.get("note") or ""):
                continue
            if (hh.get("id"), person.get("id")) not in ruled:
                bad.append("%s/%s — carries this pass's paragraph and no crosswalk match "
                           "names them" % (hh.get("id"), person.get("id")))
    return bad


def _doubles_over(household_id: str, person: dict) -> list:
    """doubles() for one already-loaded person — what the self-test needs and the gate reuses."""
    note = person.get("note") or ""
    out = []
    if note.count(MARKER) > 1:
        out.append("%s/%s — carries this pass's paragraph %d times; the register is written "
                   "onto a card once" % (household_id, person.get("id"), note.count(MARKER)))
    for old in SUPERSEDED_MARKERS:
        if old in note:
            out.append("%s/%s — carries a superseded tract-sales paragraph beside this one; "
                       "the register is written onto a card once"
                       % (household_id, person.get("id")))
    return out


def doubles() -> list:
    """…and a card says this register ONCE, however many passes have written it.

    Two ways a card ends up saying it twice and both are silent to the two gates above:
    this pass's own paragraph appended a second time, or a superseded pass's paragraph
    left standing beside it.
    """
    bad = []
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        hh = load(path)
        for person in hh.get("persons") or []:
            bad.extend(_doubles_over(hh.get("id"), person))
    return bad


def check(quiet: bool = False) -> int:
    rows = matches()
    if not LEDGER.exists():
        print("   the ledger is missing: %s" % LEDGER.relative_to(ROOT))
        return 1
    if load(LEDGER) != ledger_doc():
        print("   %s no longer re-derives from the crosswalk and the records — re-run the "
              "tool" % LEDGER.relative_to(ROOT))
        return 1
    bad = gaps(rows) + strays(rows) + doubles()
    if bad:
        for line in bad[:20]:
            print("   %s" % line)
        if len(bad) > 20:
            print("   …and %d more" % (len(bad) - 20))
        return 1
    if not quiet:
        print("land tract sales: %d entry/entries on %d card(s), no strays, none written twice"
              % (sum(len(r["entries"]) for r in rows), len(rows)))
    return 0


def report() -> int:
    rows = matches()
    print("%-34s %-28s %7s %10s %5s  %s"
          % ("household", "person", "entries", "acres", "sec16", "span"))
    print("-" * 96)
    for r in rows:
        t = totals(r)
        span = (t["first_purchase"] if t["first_purchase"] == t["last_purchase"]
                else "%s..%s" % (t["first_purchase"], t["last_purchase"]))
        print("%-34s %-28s %7d %10.2f %5d  %s"
              % (r["household_id"], r["person_id"], t["entries"], t["acres"],
                 len(t["school_section"]), span))
    print("-" * 96)
    print("%d people, %d entries, %.2f acres, %d school-section parcel(s)"
          % (len(rows), sum(len(r["entries"]) for r in rows),
             sum(totals(r)["acres"] for r in rows),
             sum(len(totals(r)["school_section"]) for r in rows)))
    return 0


def _gaps_over(row: dict, person: dict) -> list:
    """gaps() for one already-loaded person — what the self-test needs and the gate reuses."""
    out = []
    if SOURCE_ID not in (person.get("sources") or []):
        out.append("%s/%s — does not cite %s" % (row["household_id"], row["person_id"],
                                                 SOURCE_ID))
    if MARKER not in (person.get("note") or ""):
        out.append("%s/%s — no paragraph" % (row["household_id"], row["person_id"]))
    return out


def self_test() -> int:
    fails = []

    def want(label, cond):
        if not cond:
            fails.append(label)

    rows = matches()
    want("the crosswalk must name at least one person", bool(rows))
    want("every row must name a household and a person",
         all(r["household_id"] and r["person_id"] for r in rows))
    want("every entry must name the register row it was read from",
         all(e["record_id"] for r in rows for e in r["entries"]))
    want("every entry must carry the date the tract was entered",
         all(e["date_purchased"] for r in rows for e in r["entries"]))
    want("every paragraph must carry the marker and the source id",
         all(MARKER in paragraph(r) for r in rows))
    want("every paragraph must quote the crosswalk's own carry sentence",
         all(all(c in paragraph(r) for c in r["carry"]) for r in rows))
    want("no paragraph may assert residence at Chicago",
         all("lived at Chicago" not in paragraph(r) for r in rows))

    # Rule 2, held over a synthetic record: two keys move and no others.
    before = {"id": "x", "name": "X", "grade": "projected_resident",
              "sources": ["some_source"], "note": "Existing sentence.",
              "occupation": {"value": "cooper", "confidence": "inferred"}}
    after = json.loads(json.dumps(before))
    apply_to_person(after, rows[0])
    moved = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
    want("the applier moved keys other than sources and note: %s" % sorted(moved),
         moved == {"sources", "note"})
    want("the grade must not move", after["grade"] == before["grade"])
    want("the earlier note must survive", before["note"] in after["note"])
    want("the citation must be added, not replaced", "some_source" in after["sources"])

    # …and it must be idempotent: a second application changes nothing.
    twice = json.loads(json.dumps(after))
    apply_to_person(twice, rows[0])
    want("a second application must change nothing", twice == after)

    # The gate must FIRE when its two failures are staged.
    stripped = json.loads(json.dumps(after))
    stripped["sources"] = ["some_source"]
    want("gaps must fire on a card that stopped citing the source",
         any("does not cite" in g for g in _gaps_over(rows[0], stripped)))
    silent = json.loads(json.dumps(after))
    silent["note"] = "Existing sentence."
    want("gaps must fire on a card that carries no paragraph",
         any("no paragraph" in g for g in _gaps_over(rows[0], silent)))

    # …and the third gate must fire on both ways a card comes to say it twice (T-0677).
    want("doubles must stay silent on the card the applier actually writes",
         not _doubles_over("hh_x", after))
    doubled = json.loads(json.dumps(after))
    doubled["note"] = doubled["note"] + " " + paragraph(rows[0])
    want("doubles must fire on a card carrying this pass's paragraph twice",
         any("2 times" in d for d in _doubles_over("hh_x", doubled)))
    rival = json.loads(json.dumps(after))
    rival["note"] = rival["note"] + " " + SUPERSEDED_MARKERS[0] + " …"
    want("doubles must fire on a superseded tract-sales paragraph left standing",
         any("superseded" in d for d in _doubles_over("hh_x", rival)))

    for line in fails:
        print("   %s" % line)
    print("land tract sales self-test: %s" % ("FAILED" if fails else "ok"))
    return 1 if fails else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--self-test", action="store_true", dest="self_test")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.check:
        return check(quiet=args.quiet)
    if args.report:
        return report()
    return build(quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
