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
  is AMBIGUOUS and is filed as such, not resolved; where two 1835 people meet one
  card the match is CONTESTED and is not made.

WHAT A MATCH IS WORTH, and it is less than it looks. An advertising card is a
SUBSCRIPTION: the firms in this section are the ones that paid Norris, so the
section is not the town's trades but the part of them with money for display type in
1844. A match therefore says that a surname and an initial the 1835 layer holds also
stood over a Chicago shop nine years later. That is corroboration of continuity and
a candidate trade, and the carry, when T-0569 makes it, is stated as 1844 evidence.
"""
import json, os, re, sys
from collections import defaultdict

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
            "lives_at_1835": r["lives_at"], "works_at_1835": r["works_at"],
            "rule": "Surname %r folds to the same string as the card's, and the given "
                    "name of both begins %s." % (r["surname"], initial(r["given"]).upper()),
            "cards_1844": rows,
        }
        carries = []
        if not r["occupation"] and any(x["trade_1844"] for x in rows):
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

    claimed = defaultdict(list)
    for m in matches:
        claimed[m["cards_1844"][0]["claim"]].append(m)
    contested = []
    for _, rivals in sorted(claimed.items()):
        if len(rivals) > 1:
            for m in rivals:
                m["contested_with"] = [x["resident"] for x in rivals if x is not m]
                m["rule"] += (" CONTESTED: %d residents of 1835 meet this one card on that "
                              "rule, and at most one of them is the man who paid for it. "
                              "The match is not made." % len(rivals))
                contested.append(m)
    matches = [m for m in matches if "contested_with" not in m]

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
        "what_a_match_is_worth": __doc__.split("WHAT A MATCH IS WORTH")[1].strip(),
        "counts": {
            "cards": len(cards),
            "proprietor_names_printed": named + surname_only,
            "proprietors_with_a_given_name_or_initial": named,
            "proprietors_printed_as_a_surname_alone_unmatchable": surname_only,
            "residents_considered": len(people),
            "matched_one_card": len(matches),
            "matched_more_than_one_ambiguous": len(ambiguous),
            "one_card_contested_by_two_residents": len(contested),
            "surname_present_initial_absent_refused": len(refusals),
            "could_carry_trade": sum(1 for m in matches if "trade" in m["could_carry"]),
            "could_carry_place_of_business": sum(
                1 for m in matches if "place_of_business" in m["could_carry"]),
        },
        "matches": sorted(matches, key=lambda m: m["resident"]),
        "contested": sorted(contested, key=lambda m: m["resident"]),
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
