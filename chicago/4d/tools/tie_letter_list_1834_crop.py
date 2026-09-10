#!/usr/bin/env python3
"""The 1834-01-28 crop of the 1 January 1834 letter list, tied to the printed roster (T-1008).

    tools/tie_letter_list_1834_crop.py            the tie, the coverage and the differences
    tools/tie_letter_list_1834_crop.py --json     the same, machine-readable
    tools/tie_letter_list_1834_crop.py --apply    write the ties into c001 and the coverage
                                                  block into the roster
    tools/tie_letter_list_1834_crop.py --check    the committed files still carry them
    tools/tie_letter_list_1834_crop.py --self-test  the assertions still fire

WHY THIS EXISTS, AND WHAT IT ANSWERS THAT T-0424 COULD NOT.

T-0424 read the page image and counted the printed list: 170 lines, in
`data/research/newspapers/letter_list_1834_01_01_printed.json`. It then tied the
SEVENTY-EIGHT names of claims c026 and c027 -- the 1834-03-04 crop -- to their printed
lines, and reported the shortfall as `the ninety-two lines the crops never carried`.

THAT NINETY-TWO WAS ITSELF A FLOOR, and in the other direction. 1834-03-04 is the NINTH
impression of this return; the cohort was minted from the FOURTH, 1834-01-28, whose claim
c001 carries ninety-eight entities of its own. Nobody had ever tied those to the roster,
so the list of lines that reach no card was arithmetic over one crop rather than a
measurement over both. Tie c001 as well and the two crops between them carry 131 of the
170 printed lines. THE NUMBER OF LINES NO CLAIM CARRIES IS THIRTY-NINE, not ninety-two.

HOW A CROP LINE IS TIED TO A PRINTED LINE. The same rule as T-0424, over a harder crop.
The 1834-03-04 crop cut one sub-column, so its entities are in printed order and the tie
is a walk down one list. The 1834-01-28 transcription reads the page in PHYSICAL ROWS
across both sub-columns -- `Hiram Bennett` (left line 11) then `Lewis Kerchevel` (right
line 96) then `Anthony Heere` (left line 12) -- so its order is the interleave
L1, R86, L2, R87, ... , L85, R170, and a tie is an order-preserving alignment against
THAT sequence. `--check` asserts the whole property: every entity's position in the
interleaved reading order strictly increases down the claim. Ninety-seven of the
ninety-eight entities also carry enough letters to recognise their own line and are tied
`by: text`; one does not and says `by: position`, exactly as T-0424 admits its own.

  * `Reka Basten` -> line 17, `A. P. Benton`. It stands between `Mary Barrows` (line 16)
    and `Avice Blodget` (line 18) and no other line of the list can sit there. The
    1834-03-04 crop reads the same line `.E. Bonton` and T-0424 tied it to 17 by text, so
    the two crops agree on the line while agreeing on none of its letters.

  * `John S. C. Hogan` is the postmaster's signature, which the roster counts separately
    and is NOT a line of the list. It is tied `signature`, as T-0424 ties c027's.

NOTHING HERE RENAMES A CARD, DELIBERATELY, and that is the one place this tool departs
from T-0424's. `--apply` there writes the printed line into `normalized`, which is how
`hh_crisey_william`, `hh_pease_h` and `hh_plumer_f` lost their ladder rung -- a card whose
name the page contradicts SHOULD stop agreeing with the ladder, but renaming a resident
card is the same decision as minting one and T-1008 says so. c001 is the crop the 97
residents were MINTED from, so overwriting its `normalized` would rename cards in bulk as
a side effect of a measurement. So this tool RECORDS the difference instead: every entity
gets `read_at_image` carrying the printed line, the image's setting of it and the crop's
own reading, and `--report` prints the disagreements as a list for the pass that will
adjudicate them. A corrected claim over an uncorrected card is worse than neither
(T-1008), so nothing is corrected here and everything is stated.

WHAT THE THIRTY-NINE ARE. They are the lines of the printed return that NO crop of it
carries, so no claim names them, so the gazetteer never saw them and the mint could not
reach them. `tools/mint_letter_list_1834_unread.py` is the pass that mints them; this one
measures them and writes the count into the roster's own `coverage` block, so the package
states the printed 170 and what reached a claim beside it.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from read_letter_list_1834_image import (  # noqa: E402  — one owner for the tie rule
    ROSTER, letters, line_text, load, recognises,
)

CROP = ROOT / "data/research/newspapers/extracted/chicago_democrat_1834_01_28.json"
NINTH = ROOT / "data/research/newspapers/extracted/chicago_democrat_1834_03_04.json"
CLAIM = "c001"
SIGNATURE = "John S. C. Hogan"

# Entity position in c001's `entities` -> line of the printed list, and how the tie was
# made. `text` where the crop fragment recognises its own line, `position` where only the
# interleaved reading order does. Derived by an order-preserving alignment and then
# checked line by line; `--check` re-asserts the monotonicity the derivation relied on.
MAPPING = [
    (11, 'text'), (96, 'text'), (12, 'text'), (97, 'text'), (13, 'text'),
    (98, 'text'), (14, 'text'), (99, 'text'), (15, 'text'), (16, 'text'),
    (17, 'position'), (18, 'text'), (19, 'text'), (20, 'text'), (21, 'text'),
    (22, 'text'), (26, 'text'), (111, 'text'), (27, 'text'), (112, 'text'),
    (28, 'text'), (113, 'text'), (29, 'text'), (32, 'text'), (117, 'text'),
    (33, 'text'), (118, 'text'), (34, 'text'), (119, 'text'), (37, 'text'),
    (41, 'text'), (126, 'text'), (42, 'text'), (127, 'text'), (43, 'text'),
    (128, 'text'), (44, 'text'), (129, 'text'), (130, 'text'), (46, 'text'),
    (131, 'text'), (47, 'text'), (132, 'text'), (48, 'text'), (133, 'text'),
    (49, 'text'), (134, 'text'), (50, 'text'), (135, 'text'), (51, 'text'),
    (136, 'text'), (137, 'text'), (53, 'text'), (138, 'text'), (54, 'text'),
    (139, 'text'), (55, 'text'), (140, 'text'), (58, 'text'), (143, 'text'),
    (59, 'text'), (60, 'text'), (145, 'text'), (61, 'text'), (146, 'text'),
    (147, 'text'), (63, 'text'), (148, 'text'), (64, 'text'), (149, 'text'),
    (65, 'text'), (150, 'text'), (67, 'text'), (68, 'text'), (153, 'text'),
    (70, 'text'), (155, 'text'), (71, 'text'), (156, 'text'), (72, 'text'),
    (73, 'text'), (158, 'text'), (159, 'text'), (75, 'text'), (160, 'text'),
    (76, 'text'), (161, 'text'), (78, 'text'), (163, 'text'), (164, 'text'),
    (80, 'text'), (165, 'text'), (81, 'text'), (166, 'text'), (82, 'text'),
    (167, 'text'), (170, 'text'), ("signature", 'text'),]


def reading_order_position(n):
    """Where line `n` falls when the page is read across in physical rows.

    The list is set in two sub-columns of eighty-five. A row carries left line `i` and
    right line `85 + i`, and the 1834-01-28 transcription reads them in that order, so
    the sequence a tie must be monotone in is L1, R86, L2, R87, ... , L85, R170.
    """
    return 2 * n - 1 if n <= 85 else 2 * (n - 85)


def crop_entities(doc=None):
    doc = doc if doc is not None else json.loads(CROP.read_text())
    return {c["id"]: c for c in doc["claims"]}[CLAIM]["entities"]


def resolve(roster=None, doc=None):
    """Every c001 entity beside the printed line this tie gives it."""
    roster = roster or load()
    entities = crop_entities(doc)
    if len(entities) != len(MAPPING):
        raise AssertionError("%s carries %d entities, the mapping has %d"
                             % (CLAIM, len(entities), len(MAPPING)))
    out = []
    for i, (n, by) in enumerate(MAPPING):
        ent = entities[i]
        prior = ent.get("read_at_image", {}).get("crop_normalized")
        row = {"claim": CLAIM, "entity": i, "as_printed": ent["as_printed"],
               "crop": prior if prior is not None else ent.get("normalized"),
               "line": n, "by": by}
        row["at_image"] = SIGNATURE if n == "signature" else line_text(roster, n)
        out.append(row)
    return out


def crop_letters(row):
    return letters(row["crop"] or "").replace("uncertain", "")


def completes(row):
    """The page COMPLETES the crop: every letter the crop states, the page states too.

    `[uncertain: Childress]` beside `James Childress` is a forename the crop lost, not a
    reading the page contradicts, and `[?]` and `[…]` mark the loss outright. T-0424
    completed the other crop's cut readings and nothing here re-opens that.
    """
    crop = row["crop"] or ""
    if "[?]" in crop or "[…]" in crop:
        return True
    a, b = crop_letters(row), letters(row["at_image"])
    return a in b or a == b


def contradicts(row):
    """The crop states letters the page does not. This is the disagreement T-1008 owns."""
    return not completes(row) and crop_letters(row) != letters(row["at_image"])


def ninth_lines(doc=None):
    """The printed lines claims c026 and c027 already carry (T-0424)."""
    doc = doc if doc is not None else json.loads(NINTH.read_text())
    claims = {c["id"]: c for c in doc["claims"]}
    held = set()
    for cid in ("c026", "c027"):
        for ent in claims[cid]["entities"]:
            n = ent.get("read_at_image", {}).get("printed_line")
            if isinstance(n, int):
                held.add(n)
    return held


def coverage(rows, roster, ninth):
    """What reached a claim, and the lines that reached none."""
    fourth = {r["line"] for r in rows if isinstance(r["line"], int)}
    both = fourth | ninth
    unread = [n for n in range(1, len(roster["lines"]) + 1) if n not in both]
    return {"printed_lines": len(roster["lines"]),
            "carried_by_1834_01_28": sorted(fourth),
            "carried_by_1834_03_04": sorted(ninth),
            "carried_by_both": sorted(fourth & ninth),
            "carried_by_neither": unread}


def report(rows, roster, ninth):
    cov = coverage(rows, roster, ninth)
    printed = cov["printed_lines"]
    fourth, ninth_n = len(cov["carried_by_1834_01_28"]), len(cov["carried_by_1834_03_04"])
    both = printed - len(cov["carried_by_neither"])
    print("THE TWO CROPS OF ONE RETURN, AGAINST THE PRINTED LIST")
    print("  %d lines stand in the Chicago post office's 1 January 1834 return." % printed)
    print("  The 1834-01-28 crop (c001) carries %d of them, and the postmaster's signature."
          % fourth)
    print("  The 1834-03-04 crop (c026, c027) carries %d, tied by T-0424." % ninth_n)
    print("  %d lines are carried by BOTH. Between them the crops carry %d of %d, %d per"
          % (len(cov["carried_by_both"]), both, printed, round(100.0 * both / printed)))
    print("  cent of the list. T-0424's `ninety-two lines the crops never carried' was the")
    print("  shortfall of ONE crop; over both of them THE NUMBER IS %d."
          % len(cov["carried_by_neither"]))
    print()
    print("HOW THE %d TIES WERE MADE" % len(rows))
    by_text = sum(1 for r in rows if r["by"] == "text" and r["line"] != "signature")
    print("  %d by text -- the crop fragment recognises its own printed line." % by_text)
    for r in rows:
        if r["by"] == "position":
            print("  by position: crop `%s` -> line %d, %s"
                  % (r["as_printed"], r["line"], r["at_image"]))
    print("  the signature `%s` is tied `signature`; the roster counts it" % SIGNATURE)
    print("  separately and it is not a line of the list.")
    print()
    print("WHAT THE TWO READINGS DISAGREE ON -- recorded, NOT corrected (T-1008).")
    print("Each of these is a line whose type the crop states and states differently. The")
    print("card the cohort minted carries the crop's reading; the page carries the other.")
    print("Renaming a resident card is the same decision as minting one, so the difference")
    print("is set down here for the pass that adjudicates it.")
    for r in rows:
        if contradicts(r):
            print("  line %-3s crop `%s`" % (r["line"], r["crop"]))
            print("  %-8s page `%s`" % ("", r["at_image"]))
    print("  %d of %d readings are contradicted; the rest the page completes or\n  confirms." % (sum(1 for r in rows if contradicts(r)), len(rows)))
    print()
    print("THE %d LINES NO CROP CARRIES -- the pool `mint_letter_list_1834_unread.py` mints."
          % len(cov["carried_by_neither"]))
    for n in cov["carried_by_neither"]:
        print("  line %-3d %-5s %s" % (n, roster["lines"][n - 1]["column"],
                                       line_text(roster, n)))


APPLIED_NOTE = (
    " EVERY ENTITY BELOW IS NOW TIED TO ITS PRINTED LINE (T-1008), in `read_at_image`. "
    "This crop is the FOURTH of nine impressions of one return; T-0424 read the page image "
    "of the NINTH and tied claims c026 and c027 to it, and the roster it produced -- "
    "`data/research/newspapers/letter_list_1834_01_01_printed.json`, 170 lines in two "
    "sub-columns of eighty-five -- is the same list this crop cuts. The tie is by the "
    "interleaved reading order the transcription follows, L1, R86, L2, R87 and so on down "
    "the page, and ninety-seven of the ninety-eight entities also carry enough letters to "
    "recognise their own line; the ninety-eighth, `Reka Basten`, is line 17, `A. P. "
    "Benton`, by position alone, and the other crop reads that same line `.E. Bonton`. "
    "`John S. C. Hogan` is the postmaster's signature and is tied `signature`, not a line. "
    "NOTHING IS RENAMED HERE. T-0424's pass wrote the printed line into `normalized`, and "
    "the three cards that renamed under it lost a ladder rung; this crop is the one the "
    "cohort's ninety-seven residents were minted FROM, so `normalized` keeps the crop's "
    "own reading and `read_at_image.at_image` carries the page's beside it. Where the two "
    "differ the difference is RECORDED, and "
    "`tools/tie_letter_list_1834_crop.py --report` lists them. WHAT THE TIE MEASURES: "
    "the two crops between them carry 131 of the 170 printed lines, so fifty-five of the "
    "ninety-two T-0424 could not see are carried after all -- and THIRTY-NINE lines are "
    "carried by neither "
    "crop, which is the real shortfall and the pool T-1008 mints."
)


def apply(doc, rows, roster, ninth):
    claims = {c["id"]: c for c in doc["claims"]}
    claim = claims[CLAIM]
    for r in rows:
        ent = claim["entities"][r["entity"]]
        tie = {"printed_line": r["line"], "tied_by": r["by"],
               "crop_normalized": r["crop"],
               "at_image": r["at_image"],
               "roster": "data/research/newspapers/letter_list_1834_01_01_printed.json"}
        if contradicts(r):
            tie["page_contradicts_crop"] = True
        ent["read_at_image"] = tie
    if APPLIED_NOTE.strip() not in claim["notes"]:
        claim["notes"] = claim["notes"] + APPLIED_NOTE
    roster["coverage"] = dict(coverage(rows, roster, ninth), **{
        "_doc": "WHAT REACHED A CLAIM, AND WHAT DID NOT (T-1008). The printed list is 170 "
                "lines; the claims extracted from it are two crops of two different "
                "impressions of the same return, and neither carries the whole. "
                "`carried_by_neither` is the pool of lines that reach no claim, so reach "
                "no gazetteer entry, so could not be minted -- the measurement T-0424's "
                "arithmetic over one crop could not make. Derived by "
                "`tools/tie_letter_list_1834_crop.py`; `--check` re-derives it.",
    })
    return doc, roster


def check():
    roster = load()
    doc = json.loads(CROP.read_text())
    rows = resolve(roster, doc)
    ninth = ninth_lines()
    fail = []

    # 1. The tie is monotone in the interleaved reading order -- the property the
    #    alignment that produced MAPPING was allowed to assume, re-asserted here.
    prev, prev_line = 0, None
    for r in rows:
        if r["line"] == "signature":
            continue
        p = reading_order_position(r["line"])
        if p <= prev:
            fail.append("entity %d (line %s) does not follow line %s in reading order"
                        % (r["entity"], r["line"], prev_line))
        prev, prev_line = p, r["line"]

    # 2. Every tie called `text` is one the crop fragment can actually recognise.
    for r in rows:
        if r["by"] == "text" and r["line"] != "signature" \
                and not recognises(r["as_printed"], r["at_image"]):
            fail.append("entity %d claims a textual tie to line %s (`%s`) and `%s` does "
                        "not recognise it" % (r["entity"], r["line"], r["at_image"],
                                              r["as_printed"]))

    # 3. No printed line is claimed by two entities of this crop.
    seen = {}
    for r in rows:
        if r["line"] == "signature":
            continue
        if r["line"] in seen:
            fail.append("line %s is tied to entities %d and %d"
                        % (r["line"], seen[r["line"]], r["entity"]))
        seen[r["line"]] = r["entity"]

    # 4. The committed claim carries the tie, and `normalized` is UNCHANGED -- this pass
    #    records, it does not rename (T-1008).
    for r in rows:
        ent = crop_entities(doc)[r["entity"]]
        tie = ent.get("read_at_image")
        if not tie:
            fail.append("entity %d carries no read_at_image" % r["entity"])
            continue
        if tie.get("printed_line") != r["line"]:
            fail.append("entity %d carries line %r and the tie is %r"
                        % (r["entity"], tie.get("printed_line"), r["line"]))
        if ent.get("normalized") != tie.get("crop_normalized"):
            fail.append("entity %d: normalized is %r and the crop read %r -- this pass "
                        "must not rename" % (r["entity"], ent.get("normalized"),
                                             tie.get("crop_normalized")))

    # 5. The roster's coverage block is what re-deriving it produces.
    want = coverage(rows, roster, ninth)
    got = {k: v for k, v in (roster.get("coverage") or {}).items() if k != "_doc"}
    if got != want:
        fail.append("the roster's coverage block is not what this tool re-derives "
                    "(%d lines carried by neither crop committed, %d re-derived)"
                    % (len(got.get("carried_by_neither") or []),
                       len(want["carried_by_neither"])))
    return fail


def self_test():
    """The assertions above, broken on purpose."""
    roster = load()
    doc = json.loads(CROP.read_text())
    rows = resolve(roster, doc)
    out = []

    swapped = [dict(r) for r in rows]
    swapped[4]["line"], swapped[6]["line"] = swapped[6]["line"], swapped[4]["line"]
    prev, bad = 0, False
    for r in swapped:
        if r["line"] == "signature":
            continue
        p = reading_order_position(r["line"])
        if p <= prev:
            bad = True
        prev = p
    out.append(("a tie out of reading order is caught", bad))

    out.append(("a textual tie to the wrong line is caught",
                not recognises(rows[0]["as_printed"], line_text(roster, 170))))

    r = dict(rows[0]); r["crop"] = "Somebody Else"
    out.append(("a reading the page contradicts is reported", contradicts(r)))

    r = dict(rows[0]); r["crop"] = "[?] Bennett"
    out.append(("a CUT reading is not reported as a contradiction", not contradicts(r)))

    fake = dict(roster, coverage={"printed_lines": 1})
    got = {k: v for k, v in fake["coverage"].items() if k != "_doc"}
    out.append(("a coverage block that does not re-derive is caught",
                got != coverage(rows, roster, ninth_lines())))

    for label, ok in out:
        print("  %-52s %s" % (label, "OK" if ok else "FAIL"))
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
        print("the 1834-01-28 tie: %s" % ("OK" if not fail else "%d problem(s)" % len(fail)))
        return 1 if fail else 0

    roster = load()
    doc = json.loads(CROP.read_text())
    rows = resolve(roster, doc)
    ninth = ninth_lines()

    if args.apply:
        doc, roster = apply(doc, rows, roster, ninth)
        CROP.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        ROSTER.write_text(json.dumps(roster, indent=1, ensure_ascii=False) + "\n")
        print("wrote %d ties into %s and the coverage block into %s"
              % (len(rows), CROP.name, ROSTER.name))
        return 0
    if args.json:
        print(json.dumps({"ties": rows, "coverage": coverage(rows, roster, ninth)},
                         indent=1, ensure_ascii=False))
        return 0
    report(rows, roster, ninth)
    return 0


if __name__ == "__main__":
    sys.exit(main())
