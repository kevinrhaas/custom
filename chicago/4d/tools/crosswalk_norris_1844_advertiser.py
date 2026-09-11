#!/usr/bin/env python3
"""Norris's 1844 ADVERTISING DIRECTORY against the 1835 residents (T-0568).

    tools/crosswalk_norris_1844_advertiser.py [--check]

The only place a name on an 1844 advertising card is allowed to touch a person
standing in the scene of 1 July 1835. It touches them as CORROBORATION and as a
CANDIDATE trade, never as an 1835 fact: under the ratified grading ladder an 1844
listing alone never makes an 1835 resident, and nothing here regrades anybody or
writes a business. The file this writes is a proposal for T-0569, which spends it.

THE RULE, written out so it reads back without the code:
  A card names PROPRIETORS. Each proprietor whose printed name carries both a
  surname and a given name or initial is compared against every person in the
  residents layer. The SURNAME must match after both are folded (case, punctuation
  and the scanner's standing confusions removed) AND the first initials must agree.
  A surname-only agreement is a REFUSAL, however good it looks — Norris lists
  eleven Smiths, and a card that says only "Skinner & Smith" says two surnames and
  nothing else. Where an 1835 person meets more than one card on that rule the match
  is AMBIGUOUS and is filed as such, not resolved; where two 1835 people meet ONE
  PRINTED PROPRIETOR the match is CONTESTED and is not made.

  THE CONTEST IS OVER A PRINTED NAME, NOT OVER A CARD (T-0987). A display card is
  bought by a FIRM and prints its partners: "Loyd, Blakesley & Co." sets A. Loyd,
  H. A. Blakesley and Henry Norton over one advertisement, and the North-Western
  Land Agency sets William B. Ogden beside William E. Jones. Until this ticket the
  contest was keyed on the card, so two men who met two DIFFERENT printed names on
  one card were filed as rivals for it and neither was matched — on the reasoning
  that "at most one of them is the man who paid for it", which is false of a
  partnership that prints both partners. Rivalry is now keyed on the (card,
  proprietor) pair: two residents are rivals only where they meet the SAME printed
  name, which is the only place the old reasoning holds.

WHAT A MATCH IS WORTH, and it is less than it looks. An advertising card is a
SUBSCRIPTION: the firms in this section are the ones that paid Norris, so the
section is not the town's trades but the part of them with money for display type in
1844. A match therefore says that a surname and an initial the 1835 layer holds also
stood over a Chicago shop nine years later. That is corroboration of continuity and
a candidate trade, and the carry, when T-0569 makes it, is stated as 1844 evidence.
"""
import json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trade_recorded     # "does the layer hold a trade?" (T-0867), imported not restated
import tiebreak           # the tie discriminator (T-0696), imported not restated

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, "data/research/directories/claims/norris_1844_advertiser.json")
HH = os.path.join(ROOT, "data/residents/households")
OUT = os.path.join(ROOT, "data/research/directories/norris_1844_advertiser_crosswalk_1835.json")

# The same fold the directory-proper crosswalk uses, so the two files agree about
# what "the same surname" means and can be read side by side.
FOLD = [(r"[^a-z]", ""), (r"^mc", "mac"), (r"^m$", ""), (r"ii", "n"), (r"rn", "m"),
        (r"vv", "w"), (r"1", "l"), (r"0", "o")]
TITLES = ("mrs", "miss", "mr", "dr", "doctor", "capt", "col", "rev", "gen", "maj")
SUFFIXES = ("jr", "sr", "jun", "junr", "esq", "md", "2d")


def fold(name: str) -> str:
    s = (name or "").lower()
    for pat, rep in FOLD:
        s = re.sub(pat, rep, s)
    return s


def split_printed(name: str):
    """A printed proprietor name into (given, surname). Returns (None, None) when the
    card gives a surname alone — 'Skinner', 'Hovey' — which is never enough to match."""
    toks = [t.strip(".,'\"") for t in (name or "").replace(",", " ").split()]
    toks = [t for t in toks if t and t.strip(".").lower() not in SUFFIXES]
    toks = [t for t in toks if t.lower() not in TITLES]
    if len(toks) < 2:
        return None, None
    return " ".join(toks[:-1]), toks[-1]


def initial(given: str) -> str:
    for tok in (given or "").split():
        bare = tok.strip(".,'\"").lower()
        if bare in TITLES:
            continue
        for ch in tok:
            if ch.isalpha():
                return ch.lower()
    return ""


def residents():
    out = []
    for fn in sorted(os.listdir(HH)):
        if not fn.endswith(".json"):
            continue
        doc = json.load(open(os.path.join(HH, fn), encoding="utf-8"))
        for p in doc.get("persons") or []:
            name = (p.get("name") or "").strip()
            if not name or (p.get("id") or "").endswith("_household"):
                continue
            parts = name.replace(",", " ").split()
            if len(parts) < 2:
                continue
            out.append({
                "person_id": p.get("id"),
                "household_id": doc.get("id"),
                "name": name,
                "surname": parts[-1],
                "given": " ".join(parts[:-1]),
                "grade": p.get("grade"),
                "occupation": ((p.get("occupation") or {}).get("value")),
                "occupation_confidence": ((p.get("occupation") or {}).get("confidence")),
                "lives_at": ((doc.get("lives_at") or {}).get("value")),
                "works_at": ((doc.get("works_at") or {}).get("value")),
            })
    return out


def main():
    cards = json.load(open(CARDS, encoding="utf-8"))["claims"]

    # Every proprietor the advertiser names, keyed for matching. A card with three
    # partners offers three names; a card with none offers none.
    by_key = defaultdict(list)
    surnames = defaultdict(list)
    named, surname_only = 0, 0
    for c in cards:
        for printed in c["normalized"]["proprietors"]:
            given, surname = split_printed(printed)
            if not surname:
                surname_only += 1
                _, bare = None, [t.strip(".,'\"") for t in printed.split() if t.strip(".,'\"")]
                if bare:
                    surnames[fold(bare[-1])].append((c, printed))
                continue
            named += 1
            row = (c, printed)
            surnames[fold(surname)].append(row)
            if fold(surname) and initial(given):
                by_key[(fold(surname), initial(given))].append(row)

    def card_row(c, printed):
        n = c["normalized"]
        return {
            "claim": c["id"],
            "proprietor_as_printed": printed,
            "firm": n["firm"],
            "trade_1844": n["trade"],
            "address_1844": n["address"],
            "printed_page": c["locator"]["printed_page"],
        }

    matches, ambiguous, refusals = [], [], []
    people = residents()
    for r in people:
        key = (fold(r["surname"]), initial(r["given"]))
        hits = by_key.get(key, [])
        if not hits:
            if fold(r["surname"]) in surnames:
                refusals.append({
                    "resident": r["name"], "person_id": r["person_id"],
                    "surname_on_a_card": r["surname"],
                    "cards_under_that_surname": len(surnames[fold(r["surname"])]),
                    "rule": "The surname %r stands on an 1844 advertising card and no "
                            "proprietor under it carries the initial %r of %r. A "
                            "surname-only agreement is a refusal."
                            % (r["surname"], initial(r["given"]).upper() or "-", r["name"]),
                })
            continue
        rows = [card_row(c, printed) for c, printed in hits]
        rec = {
            "resident": r["name"], "person_id": r["person_id"],
            "household_id": r["household_id"], "grade_1835": r["grade"],
            "occupation_1835": r["occupation"],
            "occupation_1835_confidence": r["occupation_confidence"],
            "lives_at_1835": r["lives_at"], "works_at_1835": r["works_at"],
            "rule": "Surname %r folds to the same string as the card's, and the given "
                    "name of both begins %s." % (r["surname"], initial(r["given"]).upper()),
            "cards_1844": rows,
        }
        carries = []
        # `none_recorded` IS NO OCCUPATION (T-0867) — the same predicate, and the
        # same bug, as the directory-proper crosswalk carried until this ticket.
        if trade_recorded.absent(r["occupation"]) and any(x["trade_1844"] for x in rows):
            carries.append("trade")
        if not r["works_at"] and any(x["address_1844"] for x in rows):
            carries.append("place_of_business")
        rec["could_carry"] = carries
        rec["carry_rule"] = ("Whatever is carried is carried as 1844 evidence with "
                             "describes_date 1844 on the note, never as an 1835 fact, "
                             "and the grade of the person does not move. An advertising "
                             "card is a paid subscription: it is evidence that the firm "
                             "existed in 1844 and none at all that it existed in 1835.")
        (matches if len(rows) == 1 else ambiguous).append(rec)

    # RIVALRY IS OVER A PRINTED NAME (T-0987). Keyed on the (card, proprietor) pair,
    # so the partners a firm prints over one advertisement are not made rivals for it.
    claimed = defaultdict(list)
    for m in matches:
        row = m["cards_1844"][0]
        claimed[(row["claim"], row["proprietor_as_printed"])].append(m)
    contested = []
    for (_cid, printed), rivals in sorted(claimed.items()):
        if len(rivals) > 1:
            for m in rivals:
                m["contested_with"] = [x["resident"] for x in rivals if x is not m]
                m["rule"] += (" CONTESTED: %d residents of 1835 meet the one printed name "
                              "%r on that rule, and at most one of them is the man it "
                              "names. The match is not made." % (len(rivals), printed))
                contested.append(m)
    matches = [m for m in matches if "contested_with" not in m]

    # T-0696, THE TIE DISCRIMINATOR, read here for the first time. A trade may NARROW
    # a tie and never make one a match: the narrowed tie is filed in `discriminated`,
    # the losing side is filed as SILENT rather than contradicted, nothing moves into
    # `matches` and no grade moves. A premises and a year are REFUSED discriminators —
    # tools/tiebreak.py carries both refusals and why.
    discriminated = []
    for (_cid, printed), rivals in sorted(claimed.items()):
        if len(rivals) < 2:
            continue
        trade = rivals[0]["cards_1844"][0]["trade_1844"]
        result = tiebreak.narrow([
            {"key": m["person_id"], "occupation_1835": m["occupation_1835"],
             "printed": trade} for m in rivals])
        winner = next((m for m in rivals if m["person_id"] == result["named"]), None)
        note = tiebreak.block(result, winner["occupation_1835"] if winner else None,
                              winner["occupation_1835_confidence"] if winner else None)
        for m in rivals:
            m["discriminator"] = note or {"kind": tiebreak.KIND, "named": None,
                                          "why": result["why"], "sides": result["sides"]}
        if note:
            discriminated.append({
                "tie": "contested",
                "proprietor_as_printed": printed,
                "firm": rivals[0]["cards_1844"][0]["firm"],
                "claim": _cid,
                "rivals": [m["resident"] for m in rivals],
                "named": winner["resident"],
                "person_id": winner["person_id"],
                "discriminator": note,
            })

    # The other shape of the same tie: one person of 1835 meeting several cards. The
    # sides are the cards and the trade is the one the resident carries, so the same
    # rule reads it without restatement.
    #
    # AND THE PRIOR QUESTION THE CARDS ANSWER FIRST: whether the ambiguity is over WHO
    # or over WHICH ADVERTISEMENT. Where every card a resident meets prints the SAME
    # proprietor name the identification is not in doubt on this file's own rule — one
    # man advertising two or three businesses, as G. S. Hubbard advertises forwarding
    # and fire insurance on facing pages. That is recorded, and it still carries
    # nothing: which of his cards a trade or a place of business should be read off is
    # exactly what stays unsettled, and T-0696 forbids resolving a tie into a match.
    for m in ambiguous:
        names = sorted({c["proprietor_as_printed"] for c in m["cards_1844"]})
        m["proprietor_names_printed"] = names
        m["ambiguity_is_over"] = "which card" if len(names) == 1 else "which name"
        if len(names) == 1:
            m["rule"] += (" The %d cards all print the one name %r, so what is ambiguous "
                          "is WHICH ADVERTISEMENT and not which man. The match is still "
                          "not made and nothing is carried: a tie is filed, never "
                          "resolved into a match (T-0696)."
                          % (len(m["cards_1844"]), names[0]))
        result = tiebreak.narrow([
            {"key": c["claim"], "occupation_1835": m["occupation_1835"],
             "printed": c["trade_1844"]} for c in m["cards_1844"]])
        note = tiebreak.block(result, m["occupation_1835"], m["occupation_1835_confidence"])
        m["discriminator"] = note or {"kind": tiebreak.KIND, "named": None,
                                      "why": result["why"], "sides": result["sides"]}
        if note:
            named = next(c for c in m["cards_1844"] if c["claim"] == result["named"])
            discriminated.append({
                "tie": "ambiguous",
                "resident": m["resident"],
                "person_id": m["person_id"],
                "cards": len(m["cards_1844"]),
                "named": named["proprietor_as_printed"],
                "firm": named["firm"],
                "claim": named["claim"],
                "discriminator": note,
            })

    doc = {
        "schema": 1,
        "_doc": "GENERATED by tools/crosswalk_norris_1844_advertiser.py. The proprietors "
                "of Norris's 1844 Advertising Directory against the 1835 residents layer. "
                "A PROPOSAL: it changes no resident record and writes no business, and "
                "under the ratified ladder an 1844 card alone never makes an 1835 "
                "resident or an 1835 business.",
        "generated_by": "tools/crosswalk_norris_1844_advertiser.py",
        "source_id": "norris_directory_1844",
        "rule": __doc__.split("THE RULE, written out")[1].split("WHAT A MATCH")[0].strip(),
        "discriminator_rule": tiebreak.__doc__.split("THE RULING")[1].split(
            "Run it directly")[0].strip(),
        "refused_discriminators": tiebreak.REFUSED_DISCRIMINATORS,
        "what_a_match_is_worth": __doc__.split("WHAT A MATCH IS WORTH")[1].strip(),
        "counts": {
            "cards": len(cards),
            "proprietor_names_printed": named + surname_only,
            "proprietors_with_a_given_name_or_initial": named,
            "proprietors_printed_as_a_surname_alone_unmatchable": surname_only,
            "residents_considered": len(people),
            "matched_one_card": len(matches),
            "matched_more_than_one_ambiguous": len(ambiguous),
            "one_printed_proprietor_contested_by_two_residents": len(contested),
            "ties_narrowed_by_a_trade": len(discriminated),
            "of_those_contested": sum(1 for d in discriminated if d["tie"] == "contested"),
            "of_those_ambiguous": sum(1 for d in discriminated if d["tie"] == "ambiguous"),
            "ambiguities_over_which_card_not_which_man": sum(
                1 for m in ambiguous if m["ambiguity_is_over"] == "which card"),
            "surname_present_initial_absent_refused": len(refusals),
            "could_carry_trade": sum(1 for m in matches if "trade" in m["could_carry"]),
            "could_carry_place_of_business": sum(
                1 for m in matches if "place_of_business" in m["could_carry"]),
        },
        "matches": sorted(matches, key=lambda m: m["resident"]),
        "contested": sorted(contested, key=lambda m: m["resident"]),
        "discriminated": sorted(discriminated, key=lambda d: d["claim"]),
        "ambiguous": sorted(ambiguous, key=lambda m: m["resident"]),
        "refusals": sorted(refusals, key=lambda m: m["resident"]),
    }
    if "--check" in sys.argv:
        if not os.path.exists(OUT):
            print("advertiser crosswalk: %s is not committed" % OUT, file=sys.stderr)
            return 1
        if json.load(open(OUT, encoding="utf-8")) != doc:
            print("advertiser crosswalk: committed file does not match — regenerate",
                  file=sys.stderr)
            return 1
        print("advertiser crosswalk: matches the committed file")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(doc["counts"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
