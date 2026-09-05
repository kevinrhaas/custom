#!/usr/bin/env python3
"""Fergus 1839's Fort Dearborn Addition lot sale, spent on the people it names (T-0681).

    python3 tools/spend_fergus_1839_lots.py             write the ledger and the cards
    python3 tools/spend_fergus_1839_lots.py --check     everything re-derives; nothing drifted
    python3 tools/spend_fergus_1839_lots.py --report    person by person, how many lots
    python3 tools/spend_fergus_1839_lots.py --self-test the rules below, held over what it derives

WHY THIS EXISTS. T-0666 read printed pages 47-50 of Fergus' Chicago Directory for 1839 —
the lots sold in the Fort Dearborn Addition between the 10th and the 24th of June 1839 —
and T-0666's crosswalk matched 11 of its 100 bidders to people this town holds a card for.
Not one of those 11 cards said so. The reading landed, the adjudication landed, and the
evidence stopped one step short of the person it was about, which is the exact shape the
owner reported on 2026-09-03 when he asked whether he should be concerned that research
was not reaching the household data.

WHAT THE MEASURE COULD AND COULD NOT SEE, because it matters for what "done" means here.
`tools/measure_research_spend.py`'s second hop reported the directories domain at 3
unwritten, not 11, and both numbers are honest about different things. The hop asks
whether the CARD cites the volume, and it reads citations at the household level; eight of
these eleven households already cited `fergus_chicago_directory_1839` on the strength of
T-0635's later-lists pass — the 1837 city-election poll and the 1839 city register — so the
hop was satisfied while the LOT SALE had reached nobody. Only Amasa Wright, Arthur Bronson
and R. C. Bristol were visible to it. So this pass is not sized by the counter: it writes
all eleven, and the counter going 3 -> 0 is a consequence rather than the deliverable.

WHAT IS AND IS NOT WRITTEN, in four rules — pass 2's rules, unchanged, because the defect
they guard against is the same one.

  1. ONLY WHAT THE CROSSWALK ALREADY DECLARED. This pass re-adjudicates nothing. It reads
     `residents.matches` and writes those 11 rows. The 3 `ambiguous` and 26 `contested`
     rows are rivals still standing, and the 89 surname-only refusals are refusals; none of
     them writes anything. The voter, letter-list and 1840-head pools match a row in
     another reading rather than a card in this town, and this pass does not touch them.

  2. TWO FIELDS AND NO OTHERS. A person gains the source id in `sources` and a paragraph in
     `note`. Nothing else — not a grade, not an arrival, not a claim block, not a
     placement, and above all not `present_on_scene_date`. `--self-test` holds that by
     diffing a record through the applier and asserting the changed key set.

  3. NO GRADE MOVES, and the crosswalk itself forbids it. Its `carry_rule` says in its own
     words that a sale four years after the scene date is corroboration of CONTINUED
     RESIDENCE and not of July 1835, and that the grade does not move on it alone. That
     sentence is quoted onto every card this pass writes, so the limit travels with the
     evidence. T-0515 applies the ladder against every source at once.

  4. THE LOT IS NOT A LOCATION, and this is the rule most easily lost. The Fort Dearborn
     Addition is the reservation ground, platted into lots in 1839; in July 1835 it was the
     garrison's and was not platted at all. A block and lot number on these pages places no
     house, no shop and no household in the town this project builds, and the paragraph
     says so out loud rather than leaving a reader to infer it from a date.

ONE PARAGRAPH PER PERSON, NOT PER LOT. Arthur Bronson took fifteen lots; he is named in one
paragraph naming all fifteen, each with its block, its lot, its price and the claim id it
was read into, so nothing is lost by the fold.

THE LEDGER IS NOT A CROSSWALK, deliberately, and for the reason passes 1-3 gave:
`data/research/directories/fergus_1839_lots_spend_1835.json` carries no "crosswalk" in its
name so that `measure_research_spend.py` does not read a record of WRITES as a second
adjudication and report the pass grading its own homework.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ROOT / "data" / "research" / "directories"
LOTS = DIRECTORIES / "fergus_1839_lots_crosswalk_1835.json"
LEDGER = DIRECTORIES / "fergus_1839_lots_spend_1835.json"
HOUSEHOLDS = ROOT / "data" / "residents" / "households"

SCHEMA = 1

# The volume, and the only id written onto a card. The crosswalk states it at the top of
# the file, and it is the same volume T-0635's later-lists pass cites: one book, four
# readings.
SOURCE_ID = "fergus_chicago_directory_1839"

# The sentence that says a paragraph is this pass's, so re-running it is idempotent and
# `--check` can find its own work without guessing. It must not be a prefix of, or
# contained by, T-0635's marker — the two passes write onto many of the same cards.
MARKER = ("FERGUS 1839'S FORT DEARBORN ADDITION LOT SALE — JUNE 1839 EVIDENCE, "
          "NEVER AN 1835 FACT.")

LADDER_LIMIT = (
    "This pass WRITES THE EVIDENCE AND MOVES NO GRADE. Under the ratified ladder (T-0513) a "
    "second independent source is what lifts a projected resident, and a lot sale forty-eight "
    "months after the scene date is a second source about CONTINUED RESIDENCE rather than "
    "about July 1835. T-0515 applies the ladder against every source at once; this pass "
    "hands it the evidence and not the verdict."
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc) -> None:
    path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


# --- what the crosswalk says -----------------------------------------------------------

def lot_entry(lot: dict) -> dict:
    """One lot line, reduced to what a card is told about it."""
    return {
        "claim_id": lot["claim"],
        "block": lot.get("block"),
        "block_carried": lot.get("block_carried"),
        "lot": lot.get("lot"),
        "amount_usd": lot.get("amount_usd"),
        "printed_page": lot.get("printed_page"),
        "bidder_ditto": lot.get("bidder_ditto"),
        "describes_date": "1839-06",
    }


def matches() -> list:
    """One row per PERSON, in the crosswalk's own order.

    A ledger that re-sorted its input would stop being a re-derivation of it, so the order
    here is the order the crosswalk printed. A person who bid under more than one printed
    form of their name keeps one row and gains both forms' lots.
    """
    rows = []
    for row in load(LOTS)["residents"]["matches"]:
        entries = []
        printed = []
        for bid in row.get("bids_1839") or []:
            if bid.get("bidder_as_printed") and bid["bidder_as_printed"] not in printed:
                printed.append(bid["bidder_as_printed"])
            for lot in bid.get("lots") or []:
                entries.append(lot_entry(lot))
        rows.append({
            "household_id": row["household_id"],
            "person_id": row["person_id"],
            "name": row.get("name"),
            "source_id": SOURCE_ID,
            "grade_1835": row.get("grade_1835"),
            "bidder_as_printed": printed,
            "rules": [row["rule"]] if row.get("rule") else [],
            "entries": entries,
        })
    return rows


def carry_rule() -> str:
    """The crosswalk's OWN limit, quoted rather than paraphrased."""
    return load(LOTS)["carry_rule"]


# --- what a card is told ---------------------------------------------------------------

def _price(entry: dict) -> str:
    """A price the scan destroyed is said to be missing, never guessed at."""
    if entry.get("amount_usd") is None:
        return "at a price the scan destroyed"
    return "for $%s" % entry["amount_usd"]


def _cite(entry: dict) -> str:
    block = "block %s" % entry["block"] if entry.get("block") is not None else "an unread block"
    lot = "lot %s" % entry["lot"] if entry.get("lot") is not None else "an unread lot"
    where = ("printed page %s" % entry["printed_page"]) if entry.get("printed_page") else "unpaged"
    carried = ", block carried down the column" if entry.get("block_carried") else ""
    return "%s %s %s (%s, %s%s)" % (block, lot, _price(entry), entry["claim_id"], where, carried)


def paragraph(row: dict) -> str:
    """What one person's card is told, and the whole of it."""
    entries = row["entries"]
    n = len(entries)
    printed = " and ".join("“%s”" % p for p in row["bidder_as_printed"]) or "an unread form"
    known = [e["amount_usd"] for e in entries if e.get("amount_usd") is not None]
    total = ("The prices read total $%d%s." % (
        sum(known),
        "" if len(known) == n else " across the %d of %d lots whose price the scan left legible"
                                   % (len(known), n)))
    cites = "; ".join(_cite(e) for e in entries)
    rule = row["rules"][0] if row["rules"] else "stated in the crosswalk"
    return (
        "%s Fergus' Chicago Directory for 1839 prints the lots sold in the Fort Dearborn "
        "Addition between the 10th and the 24th of June 1839, and this person bid on %d of "
        "them, entered as %s: %s. %s %s Identity by the crosswalk's own rule: %s "
        "(data/research/directories/fergus_1839_lots_crosswalk_1835.json). %s"
        % (MARKER, n, printed, cites, total, carry_rule(), rule, LADDER_LIMIT))


# --- the ledger ------------------------------------------------------------------------

def ledger_doc() -> dict:
    rows = matches()
    crosswalk = load(LOTS)
    counts = crosswalk["counts"]
    return {
        "schema": SCHEMA,
        "_doc": (
            "GENERATED by tools/spend_fergus_1839_lots.py. The ledger of T-0681: which of "
            "T-0666's Fort Dearborn Addition lot-sale resident matches were written onto "
            "the card they name, and what each card was told. It is a record of WRITES, not "
            "of adjudications — the adjudication is "
            "fergus_1839_lots_crosswalk_1835.json — and it deliberately carries no "
            "'crosswalk' in its name so that measure_research_spend.py does not count a "
            "write as a second ruling."),
        "generated_by": "tools/spend_fergus_1839_lots.py",
        "ticket": "T-0681",
        "pass": "consolidation pass 4",
        "source_id": SOURCE_ID,
        "reads": ["data/research/directories/fergus_1839_lots_crosswalk_1835.json"],
        "writes": "data/residents/households/*.json — persons[].sources and persons[].note",
        "carry_rule": carry_rule(),
        "what_the_lot_is_not": crosswalk["what_the_sale_does_not_give"],
        "counts": {
            "matched_rulings": len(crosswalk["residents"]["matches"]),
            "people_written": len(rows),
            "households_touched": len({r["household_id"] for r in rows}),
            "grades_changed": 0,
            "lots_carried": sum(len(r["entries"]) for r in rows),
            "lots_whose_price_the_scan_destroyed": sum(
                1 for r in rows for e in r["entries"] if e.get("amount_usd") is None),
            "dollars_read": sum(e["amount_usd"] for r in rows for e in r["entries"]
                                if e.get("amount_usd") is not None),
            "people_bidding_more_than_one_lot": sum(1 for r in rows if len(r["entries"]) > 1),
        },
        "not_written": [
            {
                "rule": "F1",
                "why": ("a `contested` or `ambiguous` row is a rival still standing: the "
                        "crosswalk did not choose between the bearers of the name, and a "
                        "card that cited the volume anyway would print an undecided "
                        "identity as a decided one"),
                "rulings": counts["residents_ambiguous"] + counts["residents_contested"],
            },
            {
                "rule": "F2",
                "why": ("a surname-only agreement is a refusal in this crosswalk and in the "
                        "newspapers' ratified rules — the volume lists forty-one Smiths — "
                        "and refusals are not spent"),
                "rulings": counts["residents_surname_only_refused"],
            },
            {
                "rule": "F3",
                "why": ("the voter, letter-list and 1840-head pools match a row in ANOTHER "
                        "reading rather than a person this town holds a card for. They are "
                        "corroboration between readings and there is no card to write them "
                        "onto"),
                "rulings": (counts["voters_matched_one_bidder"]
                            + counts["letter_list_matched_one_bidder"]
                            + counts["heads_1840_matched_one_bidder"]),
            },
            {
                "rule": "F4",
                "why": ("no grade moves here, and no PLACEMENT is written at all. The block "
                        "and lot are ground platted in 1839 out of the garrison's "
                        "reservation; they place nobody in the town of 1835"),
                "rulings": 0,
            },
        ],
        "people": [
            {
                "household_id": r["household_id"],
                "person_id": r["person_id"],
                "name": r["name"],
                "source_id": r["source_id"],
                "grade_1835": r["grade_1835"],
                "bidder_as_printed": r["bidder_as_printed"],
                "rules": r["rules"],
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
        print("fergus 1839 lot sale: written onto %d resident record(s)" % touched)
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
        bad.extend(_gaps_over(row, person))
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


def check(quiet: bool = False) -> int:
    rows = matches()
    if not LEDGER.exists():
        print("   the ledger is missing: %s" % LEDGER.relative_to(ROOT))
        return 1
    if load(LEDGER) != ledger_doc():
        print("   %s no longer re-derives from the crosswalk — re-run the tool"
              % LEDGER.relative_to(ROOT))
        return 1
    bad = gaps(rows) + strays(rows)
    if bad:
        for line in bad[:20]:
            print("   %s" % line)
        if len(bad) > 20:
            print("   …and %d more" % (len(bad) - 20))
        return 1
    if not quiet:
        print("fergus 1839 lot sale: %d lot(s) on %d card(s), no strays"
              % (sum(len(r["entries"]) for r in rows), len(rows)))
    return 0


def report() -> int:
    rows = matches()
    print("%-30s %-24s %5s %10s  %s" % ("household", "person", "lots", "dollars", "as printed"))
    print("-" * 92)
    for r in rows:
        known = [e["amount_usd"] for e in r["entries"] if e.get("amount_usd") is not None]
        print("%-30s %-24s %5d %10d  %s"
              % (r["household_id"], r["person_id"], len(r["entries"]), sum(known),
                 ", ".join(r["bidder_as_printed"])))
    print("-" * 92)
    print("%d people, %d lots, $%d read"
          % (len(rows), sum(len(r["entries"]) for r in rows),
             sum(e["amount_usd"] for r in rows for e in r["entries"]
                 if e.get("amount_usd") is not None)))
    return 0


def _gaps_over(row: dict, person: dict) -> list:
    """gaps() for one already-loaded person — what the self-test needs and the gate reuses."""
    out = []
    if SOURCE_ID not in (person.get("sources") or []):
        out.append("%s/%s — matched by the crosswalk and the card does not cite %s"
                   % (row["household_id"], row["person_id"], SOURCE_ID))
    if MARKER not in (person.get("note") or ""):
        out.append("%s/%s — matched by the crosswalk and the card carries no paragraph"
                   % (row["household_id"], row["person_id"]))
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
    want("every row must carry at least one lot",
         all(r["entries"] for r in rows))
    want("every lot must name the claim it was read into",
         all(e["claim_id"] for r in rows for e in r["entries"]))
    want("every paragraph must carry the marker and the source id",
         all(MARKER in paragraph(r) for r in rows))

    # Rule 4, held in the text: the paragraph must SAY the lot places nobody in 1835, not
    # leave a reader to work it out from the date.
    want("every paragraph must say the lot is not a location for 1835",
         all("THE LOT IS NOT A LOCATION FOR 1835" in paragraph(r) for r in rows))

    # The marker must be distinguishable from T-0635's, which lands on the same cards.
    want("this marker must not be confusable with the later-lists pass's",
         "LATER LISTS" not in MARKER)

    # Rule 2, held over a synthetic record: two keys move and no others.
    before = {"id": "x", "name": "X", "grade": "projected_resident",
              "sources": ["some_source"], "note": "Existing sentence.",
              "occupation": {"value": "cooper", "confidence": "inferred"},
              "present_on_scene_date": {"value": "present", "confidence": "inferred"}}
    after = json.loads(json.dumps(before))
    apply_to_person(after, rows[0])
    moved = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
    want("the applier moved keys other than sources and note: %s" % sorted(moved),
         moved == {"sources", "note"})
    want("the grade must not move", after["grade"] == before["grade"])
    want("present_on_scene_date must not move",
         after["present_on_scene_date"] == before["present_on_scene_date"])
    want("the earlier note must survive", before["note"] in after["note"])
    want("the citation must be added, not replaced", "some_source" in after["sources"])

    # …and it must be idempotent: a second application changes nothing.
    twice = json.loads(json.dumps(after))
    apply_to_person(twice, rows[0])
    want("a second application must change nothing", twice == after)

    # A price the scan destroyed must be SAID to be missing, never printed as $0.
    want("a destroyed price must be said, not guessed",
         _price({"amount_usd": None}) == "at a price the scan destroyed")

    # The gate must FIRE when its two failures are staged.
    stripped = json.loads(json.dumps(after))
    stripped["sources"] = ["some_source"]
    want("gaps must fire on a card that stopped citing the source",
         any("does not cite" in g for g in _gaps_over(rows[0], stripped)))
    silent = json.loads(json.dumps(after))
    silent["note"] = "Existing sentence."
    want("gaps must fire on a card that carries no paragraph",
         any("no paragraph" in g for g in _gaps_over(rows[0], silent)))

    for line in fails:
        print("   %s" % line)
    print("fergus 1839 lot sale self-test: %s" % ("FAILED" if fails else "ok"))
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
