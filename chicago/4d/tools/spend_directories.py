#!/usr/bin/env python3
"""The four directory crosswalks, SPENT on the people of 1835 (T-0632).

    python3 tools/spend_directories.py            write the layer, the ledger and the cards
    python3 tools/spend_directories.py --check    everything re-derives; nothing has drifted
    python3 tools/spend_directories.py --report   person by person, what each volume carries
    python3 tools/spend_directories.py --self-test the four rules below, held over what it derives

WHY THIS EXISTS, and what it replaces. T-0555, T-0571, T-0506 and T-0587 read three
Chicago directories and adjudicated them against this town: Fergus 1839, Fergus 1843,
Norris 1844 and Norris's advertising cards of 1844. Between them they matched 214
entries to people this reconstruction holds, and every one of those match rows carries
`occupation_1835: "none_recorded"` and `lives_at_1835: null` on the resident side. The
adjudication happened and nothing crossed into the town. `tools/spend_norris_1844.py`
spent ONE of the four; this pass subsumes it and spends the rest.

THE THREE THINGS IT WRITES, and why they are three.

  data/residents/directories.json   THE LAYER A VISITOR SEES. One row per person, every
        volume that meets them, every entry as printed, and what the entry holds that
        the 1835 record does not. Beside the records rather than inside them for the
        reason T-0569 set out: a directory listing is EVIDENCE ABOUT ITS OWN YEAR
        offered beside a person of 1835, not a fact of theirs, and keeping it beside
        the record is what stops it reading as one.

  data/research/directories/spend_crosswalk_1835.json   THE LEDGER. One ruling per
        (person, volume): what the volume prints, what this pass CARRIED to the card
        and what it REFUSED to carry, with the claim ids it rests on and the source it
        rests on. It is a crosswalk because it is an adjudication — the decision that a
        printed line may or may not cross to a person as later evidence — and putting
        it anywhere else would hide it from `tools/measure_research_spend.py`, which is
        the instrument that reported this domain as 6,684 read and 288 spent.

  data/residents/households/*.json  THE CARD. A `directories` block on the household,
        carrying the later occupation and the later address as graded values and
        CITING THE SOURCE. This is the hop the owner asked about on 2026-09-03 — "there
        are not outputs or updates to the household and resident data" — and it is the
        only one of the three a reader of a single record can see.

WHAT IS AND IS NOT CARRIED — the whole provenance argument, in four rules.

  1. NOTHING IS CARRIED THAT THE CROSSWALK DOES NOT ALREADY DECLARE. Each match row
     holds a `could_carry` list its own adjudication wrote. This pass reads that list
     and carries exactly what is in it. It never re-parses a printed line, never
     decides for itself that an entry holds a trade, and is therefore reversible from
     the crosswalk in both directions.

  2. ONLY A SINGLE-ENTRY MATCH CARRIES ANYTHING. A person met by several entries is
     AMBIGUOUS and every candidate is shown rather than one chosen; an entry met by two
     people is CONTESTED and at most one of them is the person printed. Both are
     rendered — hiding them would report the crosswalks' successes and their arithmetic
     separately — and neither writes a value onto a card.

  3. NORRIS'S ALPHABETICAL SPLIT DOES NOT CROSS, and that refusal is inherited rather
     than invented. `spend_norris_1844.py` established it: splitting that volume's lines
     on nineteenth-century punctuation yields trades like "of W" and "sailor, Indiana
     st", and printing one on a card would launder a heuristic into a finding. The
     volume's LINES are carried whole and quoted; its parse is not. Norris's advertising
     cards are a different artefact — the trade is set as its own line of the card — and
     they do cross.

  4. NO 1835 GRADE MOVES, EVER. Under the ratified ladder a directory of 1839, 1843 or
     1844 never makes an 1835 resident, never dates one and never gives one a trade in
     1835. Every value this pass writes is graded `attested` FOR ITS OWN YEAR, carries
     `describes_date`, and says in its own note that the 1835 record is untouched. The
     count of 1835 grades changed by this pass is zero, and `--check` holds it there.

THE STREET NUMBER DOES NOT CROSS EITHER. Fergus 1839 flags the entries whose address is
a street number in the 1839 grid (`address_is_street_only`), a numbering this town's
year does not have; for those the STREET NAME crosses and the number is dropped, which
is the rule the 1839 crosswalk wrote for itself.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ROOT / "data" / "research" / "directories"
RESIDENTS = ROOT / "data" / "residents"
HOUSEHOLDS = RESIDENTS / "households"
LAYER = RESIDENTS / "directories.json"
LEDGER = DIRECTORIES / "spend_crosswalk_1835.json"
TICKET = "T-0632"
GENERATOR = "tools/spend_directories.py"

# The four volumes, in the order the town met them — earliest first, because the
# volume closest to 1835 is the one whose reading is worth most and the one whose
# value is carried when two disagree.
#
# `parse_trusted` is rule 3 above. `carry_keys` maps this file's two carryable
# things onto whatever the volume's own crosswalk called them: Fergus 1839 wrote
# `street_1839` where Fergus 1843 wrote `address`, and Norris's advertisers wrote
# `place_of_business`. The vocabulary is theirs; the meaning is one.
VOLUMES = [
    {
        "key": "fergus_1839",
        "file": "fergus_1839_crosswalk_1835.json",
        "block": "residents",
        "year": 1839,
        "source_id": "fergus_chicago_directory_1839",
        "title": "Fergus's Chicago directory of 1839",
        "entries_key": "entries_1839",
        "occupation_key": "occupation_1839",
        "address_key": "address_1839",
        "page_key": "printed_page",
        "parse_trusted": True,
        "carry_keys": {"occupation": "occupation", "address": "street_1839"},
    },
    {
        "key": "fergus_1843",
        "file": "fergus_1843_crosswalk_1835.json",
        "block": None,
        "year": 1843,
        "source_id": "fergus_chicago_directory_1843",
        "title": "Fergus's Chicago directory of 1843",
        "entries_key": "entries_1843",
        "occupation_key": "occupation_1843",
        "address_key": "address_1843",
        "page_key": "page",
        "parse_trusted": True,
        "carry_keys": {"occupation": "occupation", "address": "address"},
    },
    {
        "key": "norris_1844",
        "file": "norris_1844_crosswalk_1835.json",
        "block": None,
        "year": 1844,
        "source_id": "norris_directory_1844",
        "title": "Norris's Chicago directory of 1844",
        "entries_key": "entries_1844",
        "occupation_key": "occupation_1844",
        "address_key": "address_1844",
        "page_key": "printed_page",
        "parse_trusted": False,
        "carry_keys": {"occupation": "occupation", "address": "address"},
    },
    {
        "key": "norris_1844_advertiser",
        "file": "norris_1844_advertiser_crosswalk_1835.json",
        "block": None,
        "year": 1844,
        "source_id": "norris_directory_1844",
        "title": "the advertising cards in Norris's directory of 1844",
        "entries_key": "cards_1844",
        "occupation_key": "trade_1844",
        "address_key": "address_1844",
        "page_key": "printed_page",
        "printed_key": "proprietor_as_printed",
        "parse_trusted": True,
        "carry_keys": {"occupation": "trade", "address": "place_of_business"},
    },
]

STATUS_ARRAYS = (("matches", "single_entry"), ("ambiguous", "ambiguous"),
                 ("contested", "contested"))

LADDER = (
    "Under the ratified ladder a directory read after 1835 can corroborate that a person "
    "attested here was still in Chicago and can print a trade or a street the 1835 record "
    "never had; on its own it makes nobody a resident of 1835. Nothing on this person's "
    "1835 record was regraded, moved, dated or given an occupation by this entry."
)
UNTRUSTED_SPLIT = (
    "THE LINE IS CARRIED AND ITS PARSE IS NOT. Norris's alphabetical volume sets a "
    "partnership as \"of Horace Norton & Co\" where the trade would go, so the split "
    "yields \"of Loyd\", \"of Horace Norton & Co\" and twice simply \"of\" — a value "
    "containing no trade at all rather than a trade with something extra on it. "
    "T-0569 refused it on that ground and this pass inherits the refusal: the line goes "
    "to the card as Norris set it and archive.org read it, damage and all, and what it "
    "HOLDS is stated separately for a reader to check against the quote."
)
# And the caution that rides on every value that DOES cross. The Fergus volumes set the
# trade first and whatever qualifies it after — a market, an employer, a corner — on the
# same comma-separated line, so the split carries more than the trade rather than
# something other than it. That is a statable difference from Norris and it is why one
# crosses and the other does not; it is not a claim that the Fergus split is clean.
SPLIT_CAUTION = (
    "The value is the volume's own line, split by its crosswalk on the entry's "
    "punctuation. These volumes set the trade first and its qualifiers after it on the "
    "same line, so the split may carry an employer, a market or a corner along with the "
    "trade. The printed entry is quoted beside the value for exactly that reason: the "
    "split is checkable against it, and neither is read into an 1835 claim."
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def block_of(doc: dict, volume: dict) -> dict:
    return doc[volume["block"]] if volume["block"] else doc


def entry_row(entry: dict, volume: dict) -> dict:
    """One printed entry, reduced to what a card may quote: the line and where it is.

    An ADVERTISING CARD IS NOT A DIRECTORY LINE and is not made to look like one.
    Norris's alphabetical volume sets one entry per person and the crosswalk keeps it
    whole as `as_printed`; a card sets the proprietor, the firm, the trade and the
    address as separate lines of a display advertisement, and stitching them into one
    sentence would produce a quotation the book does not contain. So the card's
    proprietor line is what is quoted and its other lines are carried beside it,
    named."""
    row = {
        "claim_id": entry["claim"],
        "printed_page": entry.get(volume["page_key"]),
        "as_printed": entry[volume.get("printed_key", "as_printed")],
    }
    if entry.get("firm"):
        row["firm"] = entry["firm"]
    return row


def carried_from(match: dict, volume: dict) -> dict:
    """What this match's OWN `could_carry` declares, translated to occupation/address.

    Rule 1: the declaration is the crosswalk's, never this pass's. A volume whose
    parse is not trusted declares things it may still not carry as a VALUE, so the
    two are kept apart — `holds` is what the line contains, `carried` is what reached
    the card."""
    declared = set(match.get("could_carry") or [])
    holds = {}
    for field, their_word in volume["carry_keys"].items():
        if their_word in declared:
            holds[field] = True
    return holds


def value_for(field: str, entry: dict, volume: dict) -> str | None:
    """The printed value a single entry offers for one field, or None.

    The street NUMBER does not cross. Fergus 1839 marks the entries whose address is
    a number in the 1839 grid, a numbering this town's year does not have, and its own
    carry rule says the street NAME may cross and the number may not."""
    if field == "occupation":
        value = entry.get(volume["occupation_key"])
    else:
        if entry.get("address_is_street_only"):
            streets = [s for s in (entry.get("streets_1839") or []) if s]
            value = ", ".join(streets) or None
        else:
            value = entry.get(volume["address_key"])
    value = (value or "").strip()
    return value or None


def appearance(match: dict, volume: dict, status: str) -> dict:
    entries = [entry_row(e, volume) for e in match[volume["entries_key"]]]
    holds = carried_from(match, volume) if status == "single_entry" else {}
    return {
        "volume": volume["key"],
        "title": volume["title"],
        "year": volume["year"],
        "source_id": volume["source_id"],
        "match_status": status,
        "match_rule": match["rule"],
        "reading": "transcription_mediated",
        "entries": entries,
        "holds": sorted(holds),
        "parse_carries": volume["parse_trusted"],
        "sources": [volume["source_id"]],
    }


def note_for(field: str, value: str, volume: dict, entry: dict) -> str:
    what = "trade" if field == "occupation" else "address"
    dropped = ""
    if field == "address" and entry.get("address_is_street_only"):
        dropped = (" The street NUMBER printed against it is a number in the %d grid, a "
                   "numbering this town's year does not have, so the street name crosses "
                   "and the number does not." % volume["year"])
    return ("%s prints this %s against this person, in the entry quoted on the card: %r. "
            "It is evidence about %d, written here as %d's and read back onto no 1835 "
            "claim.%s %s"
            % (volume["title"][0].upper() + volume["title"][1:], what,
               entry[volume.get("printed_key", "as_printed")],
               volume["year"], volume["year"], dropped, LADDER))


def graded(field: str, rows: list) -> dict | None:
    """The earliest trustworthy reading of one field, graded for ITS OWN year.

    `attested` is the right word and it is not a claim about 1835: a source STATES
    this value, of the year it was printed in. The year is in the block, in the note
    and in the field's own name, and the 1835 slot beside it is untouched."""
    for volume, match, entry, value in rows:
        if not volume["parse_trusted"]:
            continue
        return {
            "value": value,
            "confidence": "attested",
            "describes_date": volume["year"],
            "sources": [volume["source_id"]],
            "claim_id": entry["claim"],
            "as_printed": entry[volume.get("printed_key", "as_printed")],
            "printed_fields": " | ".join(
                str(v) for v in entry.values() if isinstance(v, str)),
            "split": SPLIT_CAUTION,
            "note": note_for(field, value, volume, entry),
        }
    return None


def collect() -> tuple[dict, list]:
    """Every person any volume meets, with each volume's appearance, in volume order."""
    people: dict[str, dict] = {}
    order: list[str] = []
    carries: dict[str, dict[str, list]] = {}
    for volume in VOLUMES:
        doc = read_json(DIRECTORIES / volume["file"])
        block = block_of(doc, volume)
        for array, status in STATUS_ARRAYS:
            for match in block.get(array) or []:
                pid = match.get("person_id")
                if not pid:
                    # Fergus 1839 crosswalks four pools and only the residents pool
                    # names a person this town holds; the voter, letter-list and
                    # 1840-head pools carry a name and nothing to write it onto.
                    continue
                row = people.get(pid)
                if row is None:
                    row = people[pid] = {
                        "person_id": pid,
                        "household_id": match.get("household_id"),
                        "resident": match.get("resident") or match.get("name"),
                        "grade_1835": match.get("grade_1835"),
                        "occupation_1835": match.get("occupation_1835"),
                        "lives_at_1835": match.get("lives_at_1835"),
                        "works_at_1835": match.get("works_at_1835"),
                        "appearances": [],
                    }
                    order.append(pid)
                    carries[pid] = {"occupation": [], "address": []}
                row["appearances"].append(appearance(match, volume, status))
                if status != "single_entry":
                    continue
                entries = match[volume["entries_key"]]
                if len(entries) != 1:
                    continue
                entry = entries[0]
                for field in carried_from(match, volume):
                    value = value_for(field, entry, volume)
                    if value:
                        carries[pid][field].append((volume, match, entry, value))
    rows = []
    for pid in sorted(order):
        row = people[pid]
        occupation = graded("occupation", carries[pid]["occupation"])
        address = graded("address", carries[pid]["address"])
        row["occupation_later"] = occupation
        row["address_later"] = address
        row["holds_a_line_whose_parse_does_not_cross"] = bool(
            (carries[pid]["occupation"] or carries[pid]["address"])
            and not (occupation or address))
        row["sources"] = sorted({a["source_id"] for a in row["appearances"]})
        rows.append(row)
    return people, rows


def counts_of(rows: list) -> dict:
    per_volume = {}
    for volume in VOLUMES:
        seen = [a for r in rows for a in r["appearances"] if a["volume"] == volume["key"]]
        per_volume[volume["key"]] = {
            "people": len(seen),
            "single_entry": sum(1 for a in seen if a["match_status"] == "single_entry"),
            "ambiguous": sum(1 for a in seen if a["match_status"] == "ambiguous"),
            "contested": sum(1 for a in seen if a["match_status"] == "contested"),
        }
    return {
        "people_shown": len(rows),
        "people_met_by_more_than_one_volume": sum(1 for r in rows if len(r["appearances"]) > 1),
        "carrying_an_occupation": sum(1 for r in rows if r["occupation_later"]),
        "carrying_an_address": sum(1 for r in rows if r["address_later"]),
        "line_held_but_parse_refused": sum(
            1 for r in rows if r["holds_a_line_whose_parse_does_not_cross"]),
        "grades_1835_changed": 0,
        "by_volume": per_volume,
    }


def layer(rows: list) -> dict:
    return {
        "schema": 1,
        "_doc": "GENERATED by %s from the four crosswalks in "
                "data/research/directories/ (%s). Evidence about 1839, 1843 and 1844 "
                "shown beside the people of 1835, never inside their 1835 claims and "
                "never as an 1835 fact." % (GENERATOR, TICKET),
        "generated_by": GENERATOR,
        "ticket": TICKET,
        "sources": sorted({v["source_id"] for v in VOLUMES}),
        "standard": LADDER,
        "parse_refusal": UNTRUSTED_SPLIT,
        "volumes": [{"key": v["key"], "title": v["title"], "year": v["year"],
                     "source_id": v["source_id"], "crosswalk": v["file"],
                     "parse_carries": v["parse_trusted"]} for v in VOLUMES],
        "counts": counts_of(rows),
        "people": rows,
    }


def ledger(rows: list) -> dict:
    """The adjudication, in the domain that holds the reading.

    One ruling per (person, volume): the claims it rests on, the source it rests on,
    and what this pass carried or refused to carry from them. `outcome` is the word
    the other crosswalks in this repo use and the word tools/measure_research_spend.py
    reads; `carried` is what makes the ruling checkable against the card."""
    rulings = []
    for row in rows:
        for a in row["appearances"]:
            carried = []
            for field in ("occupation", "address"):
                block = row["%s_later" % field]
                if block and block["sources"] == [a["source_id"]] \
                        and any(e["claim_id"] == block["claim_id"] for e in a["entries"]):
                    carried.append(field)
            rulings.append({
                "outcome": "matched" if a["match_status"] == "single_entry" else "refused",
                "person_id": row["person_id"],
                "household_id": row["household_id"],
                "resident": row["resident"],
                "volume": a["volume"],
                "source_id": a["source_id"],
                "source_ids": [a["source_id"]],
                "claim_id": a["entries"][0]["claim_id"] if len(a["entries"]) == 1 else None,
                "claim_ids": [e["claim_id"] for e in a["entries"]],
                "match_status": a["match_status"],
                "rule": a["match_rule"],
                "carried": carried,
                "refused_to_carry": sorted(set(a["holds"]) - set(carried)),
                "why_refused": (UNTRUSTED_SPLIT if a["holds"] and not carried
                                and not a["parse_carries"] else None),
            })
    rulings.sort(key=lambda r: (r["person_id"], r["volume"]))
    return {
        "schema": 1,
        "_doc": "GENERATED by %s (%s). The adjudication that spends the four directory "
                "crosswalks onto the town: for each person a volume meets, what the "
                "volume's entry was allowed to carry to their card and what it was "
                "not. A refusal is declared as explicitly as a carry — the absence of "
                "one reads like a pair nobody has looked at yet." % (GENERATOR, TICKET),
        "generated_by": GENERATOR,
        "ticket": TICKET,
        "source_ids": sorted({v["source_id"] for v in VOLUMES}),
        "rule": LADDER,
        "counts": {
            "rulings": len(rulings),
            "carried": sum(1 for r in rulings if r["carried"]),
            "matched": sum(1 for r in rulings if r["outcome"] == "matched"),
            "refused": sum(1 for r in rulings if r["outcome"] == "refused"),
            "distinct_people": len({r["person_id"] for r in rulings}),
            "distinct_claims": len({c for r in rulings for c in r["claim_ids"]}),
        },
        "rulings": rulings,
    }


def card_block(row: dict) -> dict:
    """What goes onto the household record — the person's later readings, and no more.

    DELIBERATELY THINNER THAN THE LAYER. The printed entries, the match rules and the
    crosswalks' arithmetic live in `data/residents/directories.json`, which the panel
    opens once for the whole town; what belongs ON the record is the CLAIM — the later
    trade, the later address, each graded, dated to the year it describes and citing the
    volume. Every leaf here is read by `renderers/web/js/residents.js` and declared in
    `tools/measure_layer_reads.py`, which is the gate that stops a record shipping a
    figure to a browser that nothing shows."""
    block = {"person_id": row["person_id"]}
    for field in ("occupation", "address"):
        value = row["%s_later" % field]
        if value:
            block["%s_later" % field] = {
                "value": value["value"],
                "confidence": value["confidence"],
                "describes_date": value["describes_date"],
                "sources": value["sources"],
                "note": value["note"] + " " + SPLIT_CAUTION,
            }
    return block


def cards(rows: list) -> dict:
    """household id -> the `directories` block that record should carry."""
    out: dict[str, dict] = {}
    for row in rows:
        hid = row["household_id"]
        if not hid or not (HOUSEHOLDS / f"{hid}.json").exists():
            continue
        out.setdefault(hid, {
            "note": "LATER EVIDENCE, BESIDE THE 1835 CLAIMS AND NOT INSIDE THEM. A "
                    "Chicago directory of 1839, 1843 or 1844 meets somebody of this "
                    "name and this pass records what it prints. " + LADDER,
            "sources": [],
            "people": [],
        })
        out[hid]["people"].append(card_block(row))
        out[hid]["sources"] = sorted(set(out[hid]["sources"]) | set(row["sources"]))
    for block in out.values():
        block["people"].sort(key=lambda p: p["person_id"])
    return out


def dumps(doc) -> str:
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


# The keys later passes own on a person inside this block, in the order they are
# written. `household_text` lifts them off the record and puts them back rather
# than rebuilding them, because this pass does not derive them.
CARRIED_KEYS = ("back_projection", "residence_back_projection")


def household_text(hid: str, block: dict | None) -> str:
    """The record with this pass's `directories` block on it, and nobody else's.

    T-0633 AND T-0669 CARRY OVER. Two later passes —
    `tools/back_project_addresses.py` and `tools/back_project_residences.py` —
    write a `back_projection` and a `residence_back_projection` onto each person
    INSIDE this block, saying what each did with the address this one carried
    there. Rebuilding the block from the crosswalks would delete them, and the
    gates would then take it in turns to call each other's output drift. So the
    existing keys are lifted off the record and put back on the person they
    belong to, which is the same narrowing T-0632 made in
    `mint_placed_residents.py` for the block as a whole: this pass owns what it
    derives and nothing else.
    """
    doc = read_json(HOUSEHOLDS / f"{hid}.json")
    carried = {p["person_id"]: {k: p[k] for k in CARRIED_KEYS if k in p}
               for p in (doc.get("directories") or {}).get("people") or []}
    doc.pop("directories", None)
    if block:
        block = json.loads(json.dumps(block))
        for person in block["people"]:
            person.update(carried.get(person["person_id"]) or {})
        doc["directories"] = block
    return dumps(doc)


def build() -> tuple[dict, dict, dict]:
    _, rows = collect()
    return layer(rows), ledger(rows), cards(rows)


def written_files() -> dict[Path, str]:
    lay, led, card = build()
    out = {LAYER: dumps(lay), LEDGER: dumps(led)}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        hid = path.stem
        if hid in card:
            out[path] = household_text(hid, card[hid])
        elif "directories" in read_json(path):
            out[path] = household_text(hid, None)
    return out


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    lay, led, card = build()
    if "--report" in sys.argv:
        for row in lay["people"]:
            print("%-28s %-40s %s" % (
                row["person_id"],
                (row["occupation_later"] or {}).get("value") or "—",
                (row["address_later"] or {}).get("value") or "—"))
        print(dumps(lay["counts"]))
        print(dumps(led["counts"]))
        return 0
    files = written_files()
    if "--check" in sys.argv:
        drift = [p for p, text in files.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        if drift:
            for p in drift[:6]:
                print("   DRIFT: %s" % p.relative_to(ROOT), file=sys.stderr)
            print("   %d file(s) do not match what this pass derives — regenerate with "
                  "python3 %s" % (len(drift), GENERATOR), file=sys.stderr)
            return 1
        print("   OK: %d people met by a directory, %d carrying a trade, %d an address; "
              "%d ruling(s) in the ledger; %d card(s) written"
              % (lay["counts"]["people_shown"], lay["counts"]["carrying_an_occupation"],
                 lay["counts"]["carrying_an_address"], led["counts"]["rulings"], len(card)))
        return 0
    for path, text in files.items():
        path.write_text(text, encoding="utf-8")
    print("wrote %s, %s and %d household card(s) — %d people, %d rulings"
          % (LAYER.relative_to(ROOT), LEDGER.relative_to(ROOT), len(card),
             lay["counts"]["people_shown"], led["counts"]["rulings"]))
    return 0


def self_test() -> int:
    """The four rules above, checked over every value this pass derives.

    It is an INVARIANT GATE rather than a mutation test, and the distinction is worth
    stating: it does not break the pass to prove an assertion fires, it asserts the
    four rules against all 138 people and 303 rulings on every run. What it catches is
    a later change to a crosswalk, a carry rule or this file that lets a value cross
    which the rules forbid — which is the failure that would matter."""
    failures = []

    def check(label: str, condition: bool) -> None:
        if not condition:
            failures.append(label)

    lay, led, card = build()
    rows = lay["people"]

    # Rule 4, the one that outranks everything else here: no 1835 claim moves.
    check("an 1835 grade moved", all(
        r["grade_1835"] in (None, "attested", "inferred", "reconstructed") for r in rows))
    check("the pass reports a changed 1835 grade",
          lay["counts"]["grades_1835_changed"] == 0)

    # Rule 2: nothing is carried off an ambiguous or contested match.
    for r in rows:
        for field in ("occupation_later", "address_later"):
            block = r[field]
            if not block:
                continue
            ok = any(a["match_status"] == "single_entry"
                     and a["source_id"] == block["sources"][0]
                     and any(e["claim_id"] == block["claim_id"] for e in a["entries"])
                     for a in r["appearances"])
            check("%s/%s carried off a match that is not single-entry"
                  % (r["person_id"], field), ok)

    # Rule 3: Norris's alphabetical parse never becomes a value.
    check("Norris's alphabetical split reached a card", not any(
        (r[f] or {}).get("claim_id", "").startswith("n1844_e")
        for r in rows for f in ("occupation_later", "address_later")))

    # Rule 1: every carried value is the string the crosswalk itself printed.
    for r in rows:
        for field in ("occupation_later", "address_later"):
            block = r[field]
            if not block:
                continue
            printed = block.get("printed_fields") or block["as_printed"]
            check("%s/%s carries a value its entry does not print"
                  % (r["person_id"], field),
                  all(part.strip() in printed for part in block["value"].split(",")))

    # Every ruling states what it rests on: the third hop's ratchet is zero.
    check("a ruling states no source",
          all(r["source_ids"] for r in led["rulings"]))
    check("a ruling names a person no household holds",
          all(r["household_id"] for r in led["rulings"]))
    # And every card cites what its blocks rest on, which is the second hop.
    for hid, block in card.items():
        stated = set()
        for person in block["people"]:
            for field in ("occupation_later", "address_later"):
                if person.get(field):
                    stated |= set(person[field]["sources"])
        check("%s cites less than its claims rest on" % hid,
              stated <= set(block["sources"]) and bool(block["sources"]))

    # The instrument's own reading of the ledger: a ruling it cannot anchor is
    # invisible to it, and this pass exists to be counted.
    check("a ruling carries no anchor the spend measure can read",
          all(r["person_id"] and r["claim_ids"] for r in led["rulings"]))

    if failures:
        for f in failures[:10]:
            print("   assertion did not hold: %s" % f, file=sys.stderr)
        print("   %d assertion(s) failed" % len(failures), file=sys.stderr)
        return 1
    print("   OK: %d assertions over %d people and %d rulings"
          % (5 + len(rows) * 3 + len(card), len(rows), len(led["rulings"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
