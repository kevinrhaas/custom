#!/usr/bin/env python3
"""The lines of the 1 January 1834 letter list no crop of it carries (T-1008).

    tools/claim_letter_list_1834_unread.py            what the claim would say
    tools/claim_letter_list_1834_unread.py --json     the claim itself
    tools/claim_letter_list_1834_unread.py --apply    write it into the 1834-03-04 issue
    tools/claim_letter_list_1834_unread.py --check    the committed claim re-derives
    tools/claim_letter_list_1834_unread.py --self-test  the assertions still fire

WHY THERE IS A CLAIM HERE AT ALL. Everything this project knows about a printed page
reaches the town through a CLAIM: a claim carries entities, `compile_gazetteer.py` reads
entities into people, `compile_register.py` decides what the town does not hold, and
`mint_letter_list_residents.py` mints under the owner's ruling of 2026-08-30. A line of
the list that no claim names is invisible to all four, however plainly it stands on the
page. T-0424 read the page image and found 170 printed lines; T-1008's tie of the
1834-01-28 crop found that the two crops between them carry 131 of them. THE OTHER
THIRTY-NINE STAND IN THE SOURCE AND IN NO CLAIM, and this is the claim that names them.

THE EVIDENCE IS THE IMAGE, NOT A TRANSCRIPTION, and the claim says so. The two existing
claims are crops of a segmenter's output — cut columns with an advertisement interleaved,
which is exactly why they lost these lines. This one is read off the scan the roster
records: Internet Archive `chicago1835-newspaper-chicago-democrat-1834`,
`Jan1834-Mar1834.pdf`, jp2 page 0019, page 4 of Vol. I No. 15 of 1834-03-04, printed
column 2, at the IIIF regions the roster names. `reading` is `scan_verified` for that
reason and for no other.

NOTHING IS AUTHORED. Every entity is derived from the roster's own `as_printed` and its
`coverage` block, both of which `tools/tie_letter_list_1834_crop.py` maintains; `--check`
re-derives the whole claim and diffs it against the committed one, so a line added to the
roster or a tie changed in the crop moves this claim or fails the gate.

THE THREE LINES THAT ARE NOT ONE PERSON'S NAME, handled here rather than left to a rule
that cannot see them (T-1008's second acceptance clause). All three are carried by the
1834-01-28 crop, so none is in the thirty-nine, and all three are stated anyway because
the crop's reading of each lost the thing that makes it not a name:

  * `Lamira & Laura Carrier` (line 36) NAMES TWO WOMEN. The crop read it
    `[uncertain: Lamira] [or] Laura Carrier` — one person under two possible forenames —
    and a garbled reading is refused, so the town holds neither. The page sets an
    ampersand, not an `or`: the office held letters for both. They are minted here, as
    two entities, and they are the only entities in this claim that are not one of the
    thirty-nine.
  * `Axtel & Steele` (line 131) IS A FIRM. The crop read it `[?] Steele` and refusal 1
    caught it as garbled, which is the right answer for the wrong reason. It is entered
    as a firm so refusal 2 — `a firm, not a person` — is the rule that holds it out.
  * `Jesse B. Winn & Co.` (line 163) IS A FIRM, AND THE TOWN ALREADY HOLDS A CARD FOR IT.
    The crop lost the `& Co.` and read `Jesse B. Winn`, so refusal 2 never saw a firm and
    `hh_winn_jesse_b` was minted as a person. This claim states the printed line; it does
    NOT retire the card, because unminting a resident is the same decision as minting one
    and T-1008 says that decision is stated, not taken in passing. `--report` names it.

WHAT THE THIRTY-NINE ARE NOT. They are not new evidence and they are not a new return:
they are the rest of ONE return the project already holds, and T-0299's rule that one
list mints once is kept — these lines have never minted, here or anywhere. The mint that
follows is `mint_letter_list_residents.py`, unchanged, under its own eight refusals, and
most of these names will be refused by refusal 7 or 8 because the town already carries
the surname. That is the ruling working, not the pool failing.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from read_letter_list_1834_image import ROSTER, load  # noqa: E402

ISSUE = ROOT / "data/research/newspapers/extracted/chicago_democrat_1834_03_04.json"
CLAIM_ID = "c033"
ROSTER_PATH = "data/research/newspapers/letter_list_1834_01_01_printed.json"

# The line that names two people, and the names it names. Stated here because a rule that
# splits on `&` would also split the two firm lines, and this list is three lines long.
TWO_PEOPLE = {36: ["Lamira Carrier", "Laura Carrier"]}
FIRMS = {131: "Axtel & Steele", 163: "Jesse B. Winn & Co."}
ALREADY_A_CARD = {163: "hh_winn_jesse_b"}


def printed_name(as_printed):
    """The roster's setting of a line, as a NAME.

    The list marks a line for which more than one letter waits with a trailing count —
    `Almond Axtell 2`, `Daniel B. Clevinger 4`. A digit is never part of a name (the rule
    `mint_letter_list_residents.unread_initial` states and `consolidate_resident_evidence.
    split_name` states before it), and here it is not even a misread initial: it is the
    office's tally. It is dropped, and `as_printed` keeps it.
    """
    return re.sub(r"\s+\d+$", "", as_printed).strip()


def rows(roster=None):
    """Every entity this claim carries, in printed order."""
    roster = roster or load()
    lines = {L["n"]: L for L in roster["lines"]}
    cov = roster["coverage"]
    out = []
    for n in cov["carried_by_neither"]:
        as_printed = lines[n]["as_printed"]
        out.append({"line": n, "as_printed": as_printed,
                    "normalized": printed_name(as_printed),
                    "why": "carried by no crop of this return"})
    for n, names in sorted(TWO_PEOPLE.items()):
        for name in names:
            out.append({"line": n, "as_printed": lines[n]["as_printed"],
                        "normalized": name,
                        "why": "one printed line naming two people"})
    for n, firm in sorted(FIRMS.items()):
        out.append({"line": n, "as_printed": lines[n]["as_printed"],
                    "normalized": firm, "why": "a firm, not a person",
                    "firm": True})
    out.sort(key=lambda r: (r["line"], r["normalized"]))
    return out


NOTES = (
    "THE THIRTY-NINE LINES OF THE 1 JANUARY 1834 RETURN THAT NO CROP OF IT CARRIES, read "
    "at the page image (T-1008). This is the SAME return and the SAME printing as claims "
    "c026 and c027 of this issue -- Vol. I No. 15, page 4, printed column 2 -- and it is "
    "not a second reading of them. T-0424 read the whole page and set every line down in "
    "`" + ROSTER_PATH + "`, 170 lines in two sub-columns of eighty-five over John S. C. "
    "Hogan's signature; c026 and c027 are a crop of that page and carry 76 of the lines, "
    "and claim c001 of the 1834-01-28 issue is a crop of the FOURTH impression of the same "
    "return and carries 97. Between them the two crops carry 131. The thirty-nine entities "
    "below marked `carried by no crop of this return` are the rest of the list: names the "
    "Chicago post office held a letter for on 1 January 1834, printed in this project's own "
    "source, which reached no claim and therefore no card -- not because a ruling refused "
    "them but because the segmenter's crops had lost them. THE EVIDENCE IS THE SCAN: "
    "Internet Archive `chicago1835-newspaper-chicago-democrat-1834`, `Jan1834-Mar1834.pdf`, "
    "sha256 9fdfe5762de29a2581dcffb0a2b2140a15eb04b1811747aa37d78bbda92022d3, jp2 page "
    "0019, at the IIIF regions the roster records, which is why this claim reads "
    "`scan_verified` while the crops read `transcription_mediated`. THREE ENTITIES ARE NOT "
    "AMONG THE THIRTY-NINE and are here because the crops' reading of their line lost what "
    "makes it not a personal name: line 36 sets `Lamira & Laura Carrier` and names TWO "
    "women, which the crop read as one woman under two possible forenames and a garbled "
    "reading refused; lines 131 and 163 set `Axtel & Steele` and `Jesse B. Winn & Co.` and "
    "are FIRMS, which the crops read `[?] Steele` and `Jesse B. Winn`. The town already "
    "holds `hh_winn_jesse_b`, minted as a person from the truncated reading; this claim "
    "states the printed line and does not retire the card, because unminting a resident is "
    "the same decision as minting one. NOTHING IS MINTED HERE -- "
    "`tools/mint_letter_list_residents.py` mints, under the owner's ruling of 2026-08-30 "
    "and its own eight refusals, and T-0299's rule that one list mints once is kept "
    "because none of these lines has ever minted. `as_printed` is the type's own setting, "
    "including the trailing count of letters waiting; `normalized` drops that count, "
    "because a digit is never part of a name. Derived, not authored: "
    "`tools/claim_letter_list_1834_unread.py --check` re-derives this claim from the "
    "roster and diffs it."
)


def build(roster=None):
    roster = roster or load()
    rs = rows(roster)
    img = roster["image"]
    quote = "\n".join("%s" % r["as_printed"] for r in rs if not r.get("firm"))
    claim = {
        "id": CLAIM_ID,
        "kind": "person",
        "reading": "scan_verified",
        "quote": quote,
        "normalized": "; ".join(r["normalized"] for r in rs) + ".",
        "locator": {
            "artifact_role": "page_image",
            "issue_page": roster["printing_read"]["issue_page"],
            "column": roster["printing_read"]["printed_column"],
            "read_at_image": {
                "internet_archive_item": img["internet_archive_item"],
                "file": img["file"],
                "file_sha256": img["file_sha256"],
                "jp2_page": img["jp2_page"],
                "iiif_base": img["iiif_base"],
                "regions_read": img["regions_read"],
            },
        },
        "letter_list_only": True,
        "entities": [],
        "notes": NOTES,
    }
    for r in rs:
        ent = {
            "as_printed": r["as_printed"],
            "normalized": r["normalized"],
            "role": ("a firm named in the Chicago post-office letter list of 1 January 1834"
                     if r.get("firm") else
                     "named in the Chicago post-office letter list of 1 January 1834"),
            "reading": "scan_verified",
            "read_at_image": {
                "printed_line": r["line"],
                "tied_by": "image",
                "why_here": r["why"],
                "roster": ROSTER_PATH,
            },
        }
        if r.get("firm"):
            ent["is_firm"] = True
            if r["line"] in ALREADY_A_CARD:
                ent["read_at_image"]["town_already_holds"] = ALREADY_A_CARD[r["line"]]
        claim["entities"].append(ent)
    return claim


def committed(doc=None):
    doc = doc if doc is not None else json.loads(ISSUE.read_text())
    for c in doc["claims"]:
        if c["id"] == CLAIM_ID:
            return c
    return None


def report(claim):
    firms = [e for e in claim["entities"] if e.get("is_firm")]
    two = [e for e in claim["entities"]
           if e["read_at_image"]["why_here"] == "one printed line naming two people"]
    rest = [e for e in claim["entities"]
            if not e.get("is_firm") and e not in two]
    print("CLAIM %s OF chicago_democrat_1834_03_04 -- the list's unread remainder" % CLAIM_ID)
    print("  %d entities: %d lines no crop carries, %d people on one line that names two,"
          % (len(claim["entities"]), len(rest), len(two)))
    print("  %d firms." % len(firms))
    print()
    print("THE %d LINES THAT REACH NO CLAIM TODAY" % len(rest))
    for e in rest:
        print("  line %-3d %-24s as printed `%s`"
              % (e["read_at_image"]["printed_line"], e["normalized"], e["as_printed"]))
    print()
    print("THE LINE THAT NAMES TWO PEOPLE")
    for e in two:
        print("  line %-3d %-24s as printed `%s`"
              % (e["read_at_image"]["printed_line"], e["normalized"], e["as_printed"]))
    print()
    print("THE FIRM LINES -- entered as firms so refusal 2 holds them out")
    for e in firms:
        held = e["read_at_image"].get("town_already_holds")
        print("  line %-3d %-24s%s"
              % (e["read_at_image"]["printed_line"], e["normalized"],
                 "" if not held else "  -- THE TOWN ALREADY HOLDS %s, minted as a "
                                     "person from a crop that lost the `& Co.`" % held))


def check():
    want = build()
    got = committed()
    fail = []
    if got is None:
        return ["%s is not committed to %s" % (CLAIM_ID, ISSUE.name)]
    if got != want:
        for k in sorted(set(want) | set(got)):
            if want.get(k) != got.get(k):
                fail.append("%s: the committed claim's `%s` is not what this tool "
                            "re-derives" % (CLAIM_ID, k))
    roster = load()
    lines = {L["n"] for L in roster["lines"]}
    for e in want["entities"]:
        n = e["read_at_image"]["printed_line"]
        if n not in lines:
            fail.append("entity `%s` cites line %r, which the roster does not print"
                        % (e["normalized"], n))
    people = [e for e in want["entities"] if not e.get("is_firm")]
    if any(re.search(r"\d", e["normalized"]) for e in people):
        fail.append("a personal name carries a digit; the trailing count is not a name")
    return fail


def self_test():
    out = [
        ("the trailing count of letters is not part of the name",
         printed_name("Almond Axtell 2") == "Almond Axtell"),
        ("a name with no count is untouched",
         printed_name("Constant Abbott") == "Constant Abbott"),
        ("a glyph the image cannot read stays in the name",
         printed_name("Wooster Harrison [?]") == "Wooster Harrison [?]"),
        ("the claim carries one entity per line no crop carries, plus the three",
         len(build()["entities"]) == len(load()["coverage"]["carried_by_neither"]) + 4),
        ("a firm line is entered as a firm, not as a person",
         all(e.get("is_firm") for e in build()["entities"]
             if e["read_at_image"]["printed_line"] in FIRMS)),
        ("the line that names two people carries two entities",
         len([e for e in build()["entities"]
              if e["read_at_image"]["printed_line"] == 36]) == 2),
        ("an issue holding no such claim is caught",
         committed({"claims": []}) is None),
    ]
    for label, ok in out:
        print("  %-56s %s" % (label, "OK" if ok else "FAIL"))
    return [label for label, ok in out if not ok]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        bad = self_test()
        print("%d assertion(s) did not fire" % len(bad))
        return 1 if bad else 0
    if args.check:
        fail = check()
        for f in fail:
            print("FAIL %s" % f)
        print("the unread remainder claim: %s"
              % ("OK" if not fail else "%d problem(s)" % len(fail)))
        return 1 if fail else 0

    claim = build()
    if args.apply:
        doc = json.loads(ISSUE.read_text())
        doc["claims"] = [c for c in doc["claims"] if c["id"] != CLAIM_ID] + [claim]
        doc["claims"].sort(key=lambda c: c["id"])
        ISSUE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print("wrote %s (%d entities) into %s"
              % (CLAIM_ID, len(claim["entities"]), ISSUE.name))
        return 0
    if args.json:
        print(json.dumps(claim, indent=2, ensure_ascii=False))
        return 0
    report(claim)
    return 0


if __name__ == "__main__":
    sys.exit(main())
