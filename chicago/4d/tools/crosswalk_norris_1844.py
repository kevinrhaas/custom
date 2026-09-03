#!/usr/bin/env python3
"""Norris 1844 against the 1835 residents (T-0555).

The ONLY place a name in an 1844 directory is allowed to touch a person standing
in the scene of 1 July 1835. It touches them as CORROBORATION and as CANDIDATE
ENRICHMENT, never as an 1835 fact: under the ratified grading ladder an 1844
listing alone never makes an 1835 resident, and nothing here regrades anybody.
The file this writes is a proposal for the pass that spends it; it changes no
resident record.

The rule, written out so it reads back without the code:
  SURNAME must match after both are folded (case, punctuation and the scanner's
  usual confusions removed), AND the first initial of the given name must match.
  A surname-only agreement is a REFUSAL, however good it looks — Norris lists
  eleven Smiths. Where one 1835 person meets more than one 1844 entry on that
  rule the match is AMBIGUOUS and is filed as such, not resolved.
"""
import json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data/research/directories/claims/norris_1844_directory_entries.json")
HH = os.path.join(ROOT, "data/residents/households")
INDEX = os.path.join(ROOT, "data/residents/index.json")
OUT = os.path.join(ROOT, "data/research/directories/norris_1844_crosswalk_1835.json")

# The scanner's standing confusions in this volume, folded out of the surname
# before it is compared. Nothing here changes a quote.
FOLD = [(r"[^a-z]", ""), (r"^mc", "mac"), (r"^m$", ""), (r"ii", "n"), (r"rn", "m"),
        (r"vv", "w"), (r"1", "l"), (r"0", "o")]


def fold(name: str) -> str:
    s = (name or "").lower()
    for pat, rep in FOLD:
        s = re.sub(pat, rep, s)
    return s


def initial(given: str) -> str:
    for tok in (given or "").split():
        bare = tok.strip(".,'\"").lower()
        if bare in ("mrs", "miss", "mr", "dr", "capt", "col", "rev", "gen", "maj"):
            continue
        for ch in tok:
            if ch.isalpha():
                return ch.lower()
    return ""


def residents():
    """Every person the 1835 layer holds, with the household they belong to."""
    out = []
    for fn in sorted(os.listdir(HH)):
        if not fn.endswith(".json"):
            continue
        doc = json.load(open(os.path.join(HH, fn), encoding="utf-8"))
        for p in doc.get("persons") or []:
            name = (p.get("name") or "").strip()
            if not name or p.get("id", "").endswith("_household"):
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


def blank_occupation(value) -> bool:
    """True where the 1835 layer records a trade. `none_recorded` records none."""
    return bool(value) and value != "none_recorded"


def main():
    entries = json.load(open(ENTRIES, encoding="utf-8"))["claims"]
    by_key = defaultdict(list)
    for c in entries:
        n = c["normalized"]
        if n["firm"] or not n["surname"]:
            continue
        key = (fold(n["surname"]), initial(n["given"]))
        if key[0] and key[1]:
            by_key[key].append(c)
    surnames = defaultdict(list)
    for c in entries:
        n = c["normalized"]
        if not n["firm"] and n["surname"]:
            surnames[fold(n["surname"])].append(c)

    matches, ambiguous, refusals = [], [], []
    people = residents()
    for r in people:
        key = (fold(r["surname"]), initial(r["given"]))
        hits = by_key.get(key, [])
        if not hits:
            if fold(r["surname"]) in surnames:
                refusals.append({
                    "resident": r["name"], "person_id": r["person_id"],
                    "surname_in_1844": r["surname"],
                    "candidates": len(surnames[fold(r["surname"])]),
                    "rule": "The surname %r is in Norris 1844 and no entry under it carries "
                            "the initial %r of %r. A surname-only agreement is a refusal."
                            % (r["surname"], initial(r["given"]).upper() or "-", r["name"]),
                })
            continue
        rows = [{
            "claim": h["id"],
            "as_printed": h["normalized"]["as_printed"],
            "printed_page": h["locator"]["printed_page"],
            "occupation_1844": h["normalized"]["occupation"],
            "address_1844": h["normalized"]["address"],
        } for h in hits]
        rec = {
            "resident": r["name"], "person_id": r["person_id"],
            "household_id": r["household_id"], "grade_1835": r["grade"],
            "occupation_1835": r["occupation"],
            "lives_at_1835": r["lives_at"], "works_at_1835": r["works_at"],
            "rule": "Surname %r folds to the same string as the 1844 entry's, and the "
                    "given name of both begins %s." % (r["surname"], initial(r["given"]).upper()),
            "entries_1844": rows,
        }
        carries = []
        # `none_recorded` IS NO OCCUPATION. The residents layer writes that
        # sentinel where a person's trade was never attested, so the truthiness
        # test this line used to make read 23 of the 48 matched people as
        # already having a trade and reported `could_carry_occupation: 0` — a
        # nil that looked like a finding and was a bug. Twenty-one of them have
        # a trade printed against their name in 1844 (T-0569).
        if not blank_occupation(r["occupation"]) and any(x["occupation_1844"] for x in rows):
            carries.append("occupation")
        if not r["lives_at"] and any(x["address_1844"] for x in rows):
            carries.append("address")
        rec["could_carry"] = carries
        rec["carry_rule"] = ("Whatever is carried is carried as 1844 evidence with "
                             "describes_date 1844 on the note, never as an 1835 fact, and "
                             "the grade of the person does not move.")
        rec["resident_given_is_initial_only"] = all(
            len(t.strip(".,")) <= 1 for t in r["given"].split() if t.strip(".,").isalpha())
        (matches if len(rows) == 1 else ambiguous).append(rec)

    # ONE 1844 ENTRY, TWO 1835 PEOPLE is not a match, it is a collision — Anson H.
    # Taylor and Augustine Deodat Taylor both meet "Taylor, A. D." on the initial
    # rule and at most one of them is that man. Contested pairs come out of matches.
    claimed = defaultdict(list)
    for m in matches:
        claimed[m["entries_1844"][0]["claim"]].append(m)
    contested = []
    for claim_id, rivals in sorted(claimed.items()):
        if len(rivals) > 1:
            for m in rivals:
                m["contested_with"] = [x["resident"] for x in rivals if x is not m]
                m["rule"] += (" CONTESTED: %d residents of 1835 meet this one 1844 entry on "
                              "that rule, and at most one of them is the man printed. The "
                              "match is not made." % len(rivals))
                contested.append(m)
    matches = [m for m in matches if "contested_with" not in m]

    doc = {
        "schema": 1,
        "_doc": "GENERATED by tools/crosswalk_norris_1844.py. Norris's 1844 directory against "
                "the 825 households of the 1835 residents layer. A PROPOSAL: it changes no "
                "resident record, and under the ratified ladder an 1844 listing alone never "
                "makes an 1835 resident.",
        "generated_by": "tools/crosswalk_norris_1844.py",
        "source_id": "norris_directory_1844",
        "rule": __doc__.split("The rule, written out")[1].strip(),
        "counts": {
            "residents_considered": len(people),
            "matched_one_1844_entry": len(matches),
            "matched_more_than_one_ambiguous": len(ambiguous),
            "one_1844_entry_contested_by_two_residents": len(contested),
            "surname_present_initial_absent_refused": len(refusals),
            "could_carry_occupation": sum(1 for m in matches if "occupation" in m["could_carry"]),
            "could_carry_address": sum(1 for m in matches if "address" in m["could_carry"]),
        },
        "matches": sorted(matches, key=lambda m: m["resident"]),
        "contested": sorted(contested, key=lambda m: m["resident"]),
        "ambiguous": sorted(ambiguous, key=lambda m: m["resident"]),
        "refusals": sorted(refusals, key=lambda m: m["resident"]),
    }
    if "--check" in sys.argv:
        if json.load(open(OUT, encoding="utf-8")) != doc:
            print("norris crosswalk: committed file does not match — regenerate", file=sys.stderr)
            return 1
        print("norris crosswalk: matches the committed file")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(doc["counts"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
