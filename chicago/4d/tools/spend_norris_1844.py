#!/usr/bin/env python3
"""Norris's 1844 directory spent on the 1835 residents layer (T-0569).

    python3 tools/spend_norris_1844.py            rebuild the file
    python3 tools/spend_norris_1844.py --check    re-derive and diff
    python3 tools/spend_norris_1844.py --report   what it carries, person by person

T-0566 read the directory and T-0555's crosswalk proposed which of its 2,073
entries meet the people this town holds. Neither of them touched a resident, and
until a visitor can see the meeting it is a file in a research directory that
argues with nobody. This is the pass that spends it.

WHY IT IS A LAYER BESIDE THE RECORDS AND NOT A KEY INSIDE THEM. Most of the
people this reaches live in records that a mint regenerates byte for byte —
`mint_letter_list_residents.py --check` and its four siblings diff the whole file
— so a block written into them would be drift by the next gate that runs. It is
also the argument T-0442 already made for candidate identities: an 1844 listing
is EVIDENCE ABOUT 1844 offered beside a person, not a fact of theirs, and keeping
it beside the record is what stops it reading as one. `research_pilot.json` is
the same shape, loaded the same way and joined on `person_id` in the panel.

WHAT IS AND IS NOT CARRIED. Nothing here regrades anybody, moves anybody, dates
anybody or writes a trade or a street into an 1835 claim. Under the ratified
ladder an 1844 listing alone never makes an 1835 resident. What the pass does is
say, on the person's own card: the book prints this line, on this page, under a
rule you can check, and here is what the line holds that the 1835 record does not.

THE THREE STATUSES ARE NOT ONE. A person met by exactly one entry that no other
1835 person meets is a single-entry match. A person met by several entries is
AMBIGUOUS and every candidate is printed rather than one chosen. An entry met by
two 1835 people is CONTESTED and at most one of them is the man printed, so no
match is made. All three are shown, because a card that showed only the first
would be reporting the crosswalk's successes and hiding its arithmetic.

The 171 refusals — the surname is in the book and no entry under it carries the
person's initial — stay in `data/research/directories/norris_1844_crosswalk_1835.json`
and reach no card. A refusal on that rule is a statement about eleven Smiths
rather than about the person, and 171 cards saying "looked, and the rule says no"
would bury the 67 that say something.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CROSSWALK = os.path.join(ROOT, "data/research/directories/norris_1844_crosswalk_1835.json")
OUT = os.path.join(ROOT, "data/residents/directory_1844.json")
SOURCE_ID = "norris_directory_1844"

NINE_YEARS = (
    "Norris's directory is of 1844, nine years after the day this town is built for. "
    "It can corroborate that a person attested here in 1835 was still in Chicago, and "
    "it can print a trade or a street the 1835 record never had; on its own it makes "
    "nobody a resident of 1835. Nothing on this person's record was regraded, moved, "
    "dated or given an occupation by this entry."
)
READING = (
    "The line is archive.org's OCR of the printed page, not checked against the image "
    "by eye, and its damage is left in the quote on purpose — a tidied quote cannot be "
    "found again."
)
LACK = {"occupation": "no trade", "address": "no street"}


def carry_sentence(carries: list[str], status: str) -> str:
    """What the 1844 line holds that the 1835 record does not — or that it holds none."""
    if status != "single_entry":
        return ("Nothing is carried from an entry this record does not claim as this "
                "person's.")
    if not carries:
        return ("The 1835 record already states what this line could have supplied, so "
                "the entry is corroboration and nothing else.")
    return ("The 1835 record has %s, and the 1844 line prints one. That is 1844 evidence, "
            "shown here and written into no 1835 claim."
            % " and ".join(LACK[c] for c in carries))


def status_sentence(status: str, n: int, contested_with: list[str]) -> str:
    if status == "single_entry":
        return ("One entry in the volume meets this person on the rule below, and no "
                "other person in this town meets that entry.")
    if status == "ambiguous":
        return ("%d entries in the volume meet this person on the rule below and this "
                "record does not choose between them. All of them are printed here."
                % n)
    return ("The one entry that meets this person is also met by %s, and at most one of "
            "them is the man printed, so no match is made."
            % " and ".join(contested_with or ["another person in this town"]))


def person(rec: dict, status: str) -> dict:
    # THE PRINTED LINE, AND NOT THE PARSE OF IT. The crosswalk splits each line
    # into a trade and an address on nineteenth-century punctuation, and on this
    # volume that split is the weakest thing in the reading: "Adams, W. H. of
    # W. H. A. & Co. residence iasalle. street" yields the trade "of W". Printing
    # that on a card would launder a heuristic into a finding. The line goes to
    # the card whole, as Norris set it and as archive.org read it, and the split
    # survives only in `carries` — a statement that the line HOLDS a trade or a
    # street the 1835 record lacks, which a reader checks against the quote.
    entries = [{
        "claim_id": e["claim"],
        "printed_page": e["printed_page"],
        "as_printed": e["as_printed"],
    } for e in rec["entries_1844"]]
    carries = list(rec.get("could_carry") or []) if status == "single_entry" else []
    contested_with = list(rec.get("contested_with") or [])
    return {
        "person_id": rec["person_id"],
        "household_id": rec["household_id"],
        "resident": rec["resident"],
        "year": 1844,
        "match_status": status,
        "match_rule": rec["rule"],
        "reading": "transcription_mediated",
        "entries": entries,
        "carries": carries,
        "contested_with": contested_with,
        "note": " ".join([status_sentence(status, len(entries), contested_with),
                          carry_sentence(carries, status), NINE_YEARS, READING]),
        "sources": [SOURCE_ID],
    }


def build() -> dict:
    cw = json.load(open(CROSSWALK, encoding="utf-8"))
    people = ([person(r, "single_entry") for r in cw["matches"]]
              + [person(r, "ambiguous") for r in cw["ambiguous"]]
              + [person(r, "contested") for r in cw["contested"]])
    people.sort(key=lambda p: p["person_id"])
    carried = [p for p in people if p["carries"]]
    return {
        "schema": 1,
        "_doc": "GENERATED by tools/spend_norris_1844.py from "
                "data/research/directories/norris_1844_crosswalk_1835.json (T-0569). "
                "Evidence about 1844 shown beside the people of 1835, never inside "
                "their records and never as an 1835 fact.",
        "generated_by": "tools/spend_norris_1844.py",
        "year": 1844,
        "source_id": SOURCE_ID,
        "sources": [SOURCE_ID],
        "standard": "An 1844 directory entry corroborates and enriches; under the "
                    "ratified ladder it never makes an 1835 resident. Every person here "
                    "keeps the grade, the occupation, the residence and the dates their "
                    "1835 evidence gave them.",
        "refusals_not_shown": "The %d people whose surname is in the volume under no "
                              "entry carrying their initial are refused in the crosswalk "
                              "and reach no card." % len(cw["refusals"]),
        "counts": {
            "residents_considered": cw["counts"]["residents_considered"],
            "people_shown": len(people),
            "single_entry": sum(1 for p in people if p["match_status"] == "single_entry"),
            "ambiguous": sum(1 for p in people if p["match_status"] == "ambiguous"),
            "contested": sum(1 for p in people if p["match_status"] == "contested"),
            "refused_in_crosswalk": len(cw["refusals"]),
            "carrying_a_trade": sum(1 for p in carried if "occupation" in p["carries"]),
            "carrying_a_street": sum(1 for p in carried if "address" in p["carries"]),
        },
        "people": people,
    }


def main() -> int:
    doc = build()
    if "--report" in sys.argv:
        for p in doc["people"]:
            print("%-28s %-12s %s" % (p["person_id"], p["match_status"],
                                      "; ".join(e["as_printed"] for e in p["entries"])))
        print(json.dumps(doc["counts"], indent=1))
        return 0
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != text:
            print("norris 1844 residents layer: committed file does not match — regenerate",
                  file=sys.stderr)
            return 1
        print("norris 1844 residents layer: matches the committed file (%d people)"
              % len(doc["people"]))
        return 0
    open(OUT, "w", encoding="utf-8").write(text)
    print("wrote %s — %d people" % (os.path.relpath(OUT, ROOT), len(doc["people"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
