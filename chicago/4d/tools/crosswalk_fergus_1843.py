#!/usr/bin/env python3
"""Fergus 1843 against the 1835 residents (T-0571).

The ONLY place a name in an 1843 directory is allowed to touch a person standing
in the scene of 1 July 1835. It touches them as CORROBORATION and as CANDIDATE
ENRICHMENT, never as an 1835 fact: under the ratified grading ladder a later
listing alone never makes an 1835 resident, and nothing here regrades anybody.
The file this writes is a proposal for the pass that spends it (T-0569); it
changes no resident record.

The rule, written out so it reads back without the code:
  SURNAME must match after both are folded (case, punctuation and the
  transcriber's usual confusions removed), AND the first initial of the given
  name must match. A surname-only agreement is a REFUSAL, however good it looks —
  Fergus lists thirty-one Smiths. Where one 1835 person meets more than one 1843
  entry on that rule the match is AMBIGUOUS and is filed as such, not resolved;
  where two 1835 people meet one 1843 entry it is CONTESTED and no match is made.

WHAT THIS DIRECTORY CARRIES THAT NORRIS'S DOES NOT is a date of death. Fergus
compiled the volume in 1896 and set each man's death in brackets after his entry —
"[died June 6, 1882, aged 67.]" — which, with the age, is a year of birth. Those
brackets are carried onto the match as `death_note_1843` for T-0574, which is the
ticket that reads them as birth years. They are not spent here.
"""
import json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data/research/directories/claims/fergus_1843_directory_entries.json")
HH = os.path.join(ROOT, "data/residents/households")
OUT = os.path.join(ROOT, "data/research/directories/fergus_1843_crosswalk_1835.json")

# The transcriber's and the printer's standing confusions in this volume, folded
# out of the surname before it is compared. Nothing here changes a quote.
FOLD = [(r"[^a-z]", ""), (r"^mc", "mac"), (r"^m$", ""), (r"ii", "n"), (r"rn", "m"),
        (r"vv", "w"), (r"1", "l"), (r"0", "o")]
DEATH = re.compile(r"^(died|d\.|killed|suicide|drowned|lost)", re.I)


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


def death_note(entry):
    for note in entry["normalized"].get("bracket_notes") or []:
        if DEATH.match(note.strip()):
            return note
    return None


def row_of(entry):
    n = entry["normalized"]
    return {
        "claim": entry["id"],
        "as_printed": n["as_printed"],
        "page": entry["locator"]["page"],
        "section": n["section"],
        "trade_heading": n["trade_heading"],
        "occupation_1843": n["occupation"],
        "address_1843": n["address"],
        "death_note_1843": death_note(entry),
    }


def main():
    entries = json.load(open(ENTRIES, encoding="utf-8"))["claims"]
    by_key, surnames = defaultdict(list), defaultdict(list)
    for c in entries:
        n = c["normalized"]
        if n["firm"] or not n["surname"]:
            continue
        f = fold(n["surname"])
        if not f:
            continue
        surnames[f].append(c)
        i = initial(n["given"])
        if i:
            by_key[(f, i)].append(c)

    matches, ambiguous, refusals = [], [], []
    people = residents()
    for r in people:
        f, i = fold(r["surname"]), initial(r["given"])
        hits = by_key.get((f, i), [])
        if not hits:
            if f in surnames:
                refusals.append({
                    "resident": r["name"], "person_id": r["person_id"],
                    "surname_in_1843": r["surname"],
                    "candidates": len(surnames[f]),
                    "rule": "The surname %r is in Fergus 1843 and no entry under it carries "
                            "the initial %r of %r. A surname-only agreement is a refusal."
                            % (r["surname"], i.upper() or "-", r["name"]),
                })
            continue
        rows = [row_of(h) for h in hits]
        rec = {
            "resident": r["name"], "person_id": r["person_id"],
            "household_id": r["household_id"], "grade_1835": r["grade"],
            "occupation_1835": r["occupation"],
            "lives_at_1835": r["lives_at"], "works_at_1835": r["works_at"],
            "rule": "Surname %r folds to the same string as the 1843 entry's, and the "
                    "given name of both begins %s." % (r["surname"], i.upper()),
            "entries_1843": rows,
        }
        carries = []
        if not r["occupation"] and any(x["occupation_1843"] for x in rows):
            carries.append("occupation")
        if not r["lives_at"] and any(x["address_1843"] for x in rows):
            carries.append("address")
        if any(x["death_note_1843"] for x in rows):
            carries.append("death_note")
        rec["could_carry"] = carries
        rec["carry_rule"] = ("Whatever is carried is carried as 1843 evidence with "
                             "describes_date 1843 on the note, never as an 1835 fact, and "
                             "the grade of the person does not move. The death note is "
                             "T-0574's, not this file's.")
        rec["resident_given_is_initial_only"] = all(
            len(t.strip(".,")) <= 1 for t in r["given"].split() if t.strip(".,").isalpha())
        (matches if len(rows) == 1 else ambiguous).append(rec)

    # ONE 1843 ENTRY, TWO 1835 PEOPLE is not a match, it is a collision, and at
    # most one of them is the man printed. Contested pairs come out of matches.
    claimed = defaultdict(list)
    for m in matches:
        claimed[m["entries_1843"][0]["claim"]].append(m)
    contested = []
    for _, rivals in sorted(claimed.items()):
        if len(rivals) > 1:
            for m in rivals:
                m["contested_with"] = [x["resident"] for x in rivals if x is not m]
                m["rule"] += (" CONTESTED: %d residents of 1835 meet this one 1843 entry on "
                              "that rule, and at most one of them is the person printed. The "
                              "match is not made." % len(rivals))
                contested.append(m)
    matches = [m for m in matches if "contested_with" not in m]

    doc = {
        "schema": 1,
        "_doc": "GENERATED by tools/crosswalk_fergus_1843.py. Fergus's 1843 directory against "
                "the 1835 residents layer. A PROPOSAL: it changes no resident record, and "
                "under the ratified ladder an 1843 listing alone never makes an 1835 "
                "resident. T-0569 is the pass that spends it; T-0574 is the pass that "
                "spends the death notes.",
        "generated_by": "tools/crosswalk_fergus_1843.py",
        "source_id": "fergus_chicago_directory_1843",
        "rule": __doc__.split("The rule, written out")[1].split("WHAT THIS DIRECTORY")[0].strip(),
        "counts": {
            "residents_considered": len(people),
            "matched_one_1843_entry": len(matches),
            "matched_more_than_one_ambiguous": len(ambiguous),
            "one_1843_entry_contested_by_two_residents": len(contested),
            "surname_present_initial_absent_refused": len(refusals),
            "could_carry_occupation": sum(1 for m in matches if "occupation" in m["could_carry"]),
            "could_carry_address": sum(1 for m in matches if "address" in m["could_carry"]),
            "could_carry_death_note": sum(1 for m in matches
                                          if "death_note" in m["could_carry"]),
        },
        "matches": sorted(matches, key=lambda m: m["resident"]),
        "contested": sorted(contested, key=lambda m: m["resident"]),
        "ambiguous": sorted(ambiguous, key=lambda m: m["resident"]),
        "refusals": sorted(refusals, key=lambda m: m["resident"]),
    }
    if "--check" in sys.argv:
        if json.load(open(OUT, encoding="utf-8")) != doc:
            print("fergus crosswalk: committed file does not match — regenerate",
                  file=sys.stderr)
            return 1
        print("fergus crosswalk: matches the committed file")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(doc["counts"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
