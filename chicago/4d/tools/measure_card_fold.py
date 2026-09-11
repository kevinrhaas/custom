#!/usr/bin/env python3
"""The candidate test run again with a FUZZY KEY, and what it newly proposes (T-1002).

THE QUESTION, and T-0961 found it the hard way. `clusters()` in
tools/consolidate_town_cards.py buckets the town's cards by the surname AS A STRING and
then weighs the forenames with `compatible()`, which asks for the same word or an initial
that word begins with. Both folds are EXACT. So three pairs of cards a reading of one
table found to be one man each — Madore/Medore Beaubien, Clybourn/Clybourne Archibald,
Russel/Russell E. Heacock — were never refused and never deferred by that machinery.
They were NEVER PROPOSED, because each differs by one letter, and the file of rulings has
no way to say how many pairs of that shape it could not see.

This is the count it could not state. It is a MEASUREMENT and not a proposal: running it
changes no committed file, and nothing here folds a card. The rule that folds a card is
written by hand in data/residents/card_merge_rulings.json, one cluster at a time, which
is the standing answer T-1001 gave to the same question at the land register — see C9 and
tools/measure_surname_fold.py.

THE TWO COHORTS, which are the ticket's own words: edit distance 1 on the surname, and on
the forename where the surname folds.

    A   the surname is ONE LETTER apart and the forenames are compatible under the
        exact rule already written — Clybourn/Clybourne Archibald is this shape
    B   the surname agrees letter for letter and the first forename token is ONE LETTER
        apart — Madore/Medore Beaubien and Russel/Russell E. Heacock are this shape

AND THE DEGENERATE CASE, which is cohort B's own ceiling and the reason it is reported
apart. Every initial is one letter from every other initial: 'D Harmon' against 'M D
Harmon', 'J Green' against 'M Jones'. A fuzzy forename test that admits a SINGLE-LETTER
token proposes every pair of initials in every surname and says nothing. So cohort B asks
that both first tokens be WORDS, and the pairs that fail only on that are counted here and
never listed as proposals.

THE ANSWER, measured on the tree T-1002 was written against — quoted rather than gated,
because the residents layer grows on almost every ticket and a gate on these numbers would
go red for everybody. The first column is the count BEFORE this ticket's own three folds
landed, which is the number the ticket was ruled on; the second is what this file prints
on the tree that shipped it:

                                                   before   after
    person cards                                    1,377   1,374
    …carrying a name the test can parse             1,376   1,373
    pairs the EXACT candidate test already joins       21      21
    cohort A   the surname one letter apart            63      62
    cohort B   the forename one letter apart            8       6
    degenerate, counted and never proposed             22      22

So the three T-1002 found by hand are three of seventy-one, and seventy-one is far more
than one run can rule. Three are ruled in card_merge_rulings.json under C10 — which is
why the first column falls by exactly three — and the remaining sixty-eight are an EPIC
under the queue's own filing rule, carrying this list.

    tools/measure_card_fold.py             the counts
    tools/measure_card_fold.py --detail    every pair, cohort by cohort
    tools/measure_card_fold.py --self-test the assertions still fire when broken
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import consolidate_town_cards as ctc                      # noqa: E402
from measure_surname_fold import one_letter_apart         # noqa: E402


def exact_pairs(rows: list) -> set:
    """Every pair of cards the EXACT candidate test already joins.

    These are the pairs card_merge_rulings.json already covers, and the gate in
    consolidate_town_cards.py --check refuses to pass while one of them is unruled. A
    fuzzy key ADDS to that test, so they are subtracted before anything is proposed.
    """
    seen = set()
    for cluster in ctc.clusters([dict(row) for row in rows]):
        ids = [card["person"] for card in cluster["cards"]]
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                seen.add(tuple(sorted((ids[i], ids[j]))))
    return seen


def proposals(rows: list | None = None) -> dict:
    """The pairs a fuzzy key newly proposes, in cohorts, plus the degenerate count."""
    rows = rows if rows is not None else ctc.read_town()
    named = []
    for row in rows:
        parsed = ctc.forename_tokens(row["name"])
        if parsed:
            row = dict(row, parsed=parsed)
            named.append(row)
    already = exact_pairs(rows)

    out = {"cards": len(rows), "named": len(named), "exact_pairs": len(already),
           "a": [], "b": [], "degenerate": []}
    for i in range(len(named)):
        for j in range(i + 1, len(named)):
            one, two = named[i], named[j]
            surname_a, given_a = one["parsed"]
            surname_b, given_b = two["parsed"]
            if tuple(sorted((one["person"], two["person"]))) in already:
                continue
            pair = (one, two)
            if surname_a != surname_b:
                # cohort A — the surname is one letter apart and the forenames agree
                # under the rule already written. Nothing about the forename is loosened.
                if one_letter_apart(surname_a, surname_b) and ctc.compatible(
                        one["parsed"], two["parsed"]):
                    out["a"].append(pair)
            elif given_a and given_b and one_letter_apart(given_a[0], given_b[0]):
                # cohort B — the surname folds exactly, so the forename is the thing the
                # distance is spent on. A SINGLE LETTER is not a word: see the module doc.
                if len(given_a[0]) == 1 or len(given_b[0]) == 1:
                    out["degenerate"].append(pair)
                else:
                    out["b"].append(pair)
    for key in ("a", "b", "degenerate"):
        out[key].sort(key=lambda pair: (pair[0]["person"], pair[1]["person"]))
    return out


def show(found: dict, detail: bool) -> None:
    print(f"{found['cards']} person card(s), {found['named']} with a parseable name")
    print(f"{found['exact_pairs']} pair(s) the exact candidate test already joins "
          f"— already ruled, and subtracted below")
    print(f"{len(found['a'])} cohort A   the surname one letter apart, "
          f"forenames compatible")
    print(f"{len(found['b'])} cohort B   the surname exact, the forename one letter apart")
    print(f"{len(found['degenerate'])} degenerate  an initial against an initial — "
          f"counted, never proposed")
    if not detail:
        return
    for key, what in (("a", "COHORT A — the surname one letter apart"),
                      ("b", "COHORT B — the forename one letter apart"),
                      ("degenerate", "DEGENERATE — an initial is one letter from "
                                     "every other initial, and this is not a proposal")):
        print(f"\n{what}  ({len(found[key])})")
        for one, two in found[key]:
            print(f"   {one['person']:<32} {one['name']:<30} | "
                  f"{two['person']:<32} {two['name']}")


def self_test() -> int:
    fails = []

    def ok(cond, why):
        if not cond:
            fails.append(why)

    def card(person, name):
        return {"household": "hh_" + person, "person": person, "name": name,
                "doc": {"id": "hh_" + person}, "record": {"id": person}}

    rows = [
        card("clybourn_a", "Archibald Clybourn"),
        card("clybourne_a", "Archibald Clybourne"),
        card("heacock_russel_e", "Russel E. Heacock"),
        card("heacock_russell_e", "Russell E Heacock"),
        card("harmon_d", "D Harmon"),
        card("harmon_m", "M Harmon"),
        card("allen_james", "James Allen"),
        card("allen_j", "J Allen"),
        card("brown_mary", "Mary Brown"),
    ]
    found = proposals(rows)
    got = {key: {(a["person"], b["person"]) for a, b in found[key]}
           for key in ("a", "b", "degenerate")}

    ok(got["a"] == {("clybourn_a", "clybourne_a")},
       "cohort A must hold the one pair whose surname is a letter apart, and nothing "
       "else — this is the Clybourn/Clybourne shape T-0961 found by hand")
    ok(got["b"] == {("heacock_russel_e", "heacock_russell_e")},
       "cohort B must hold the doubled l and nothing else — the Heacock shape")
    ok(got["degenerate"] == {("harmon_d", "harmon_m")},
       "two initials of one surname must be counted as DEGENERATE and never proposed: "
       "every initial is one letter from every other, and a test that proposes them "
       "proposes the whole alphabet")
    ok(found["exact_pairs"] == 1,
       "the exact candidate test must still find James Allen and J Allen, so that pair "
       "is subtracted rather than proposed again")
    ok(not any((a["person"], b["person"]) == ("allen_j", "allen_james")
               for key in ("a", "b") for a, b in found[key]),
       "…and a pair the exact test already joins must never appear as a NEW proposal")
    ok(all("brown_mary" not in (a["person"], b["person"])
           for key in ("a", "b", "degenerate") for a, b in found[key]),
       "a lone surname must be proposed against nothing")

    ok(one_letter_apart("madore", "medore") and not one_letter_apart("madore", "madore"),
       "the distance must admit a substitution and refuse an identity — the exact "
       "bucket is counted by the candidate test and must not be counted twice here")

    for fail in fails:
        print(f"   {fail}")
    print(f"   {'OK: every assertion holds' if not fails else f'{len(fails)} failed'}")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--detail", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    show(proposals(), args.detail)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
