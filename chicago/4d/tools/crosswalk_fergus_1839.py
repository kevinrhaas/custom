#!/usr/bin/env python3
"""Fergus' 1839 directory against the four pools of 1835 names (T-0506).

The ONLY place a name in the 1839 directory is allowed to touch a person standing
in the scene of 1 July 1835. It touches them as CORROBORATION and as CANDIDATE
ENRICHMENT, never as an 1835 fact: under the ratified grading ladder a later
listing alone never makes an 1835 resident, and NOTHING HERE MINTS OR REGRADES
ANYBODY. The file this writes is a proposal for the passes that spend it —
T-0513 consolidates it, T-0514 and T-0515 are the ones allowed to write people.

The rule, written out so it reads back without the code:
  SURNAME must match after both are folded (case, punctuation and the
  transcriber's usual confusions removed), AND the first initial of the given
  name must match. A surname-only agreement is a REFUSAL, however good it looks —
  this directory lists forty-one Smiths. Where one 1835 name meets more than one
  1839 entry on that rule the match is AMBIGUOUS and is filed as such, not
  resolved; where two 1835 people meet one 1839 entry it is CONTESTED and no match
  is made.

FOUR POOLS, because the ticket asks for four and they are not the same object.
The residents layer is the town as it stands, and a match there is enrichment of a
record that already exists. The voter, poll and tax entries (T-0493), the
letter-list and newspaper persons, and the 1840 heads are LISTS OF NAMES, and a
match there is one more line of evidence about a name the project has not yet
made into a person. They are counted separately and never mixed.

WHAT THIS DIRECTORY WILL NOT GIVE, however well a name matches: an address. Fergus
prints on page 3 that no street but Lake carried numbers in 1839 and that "the
numbers now given are those of the present day" — 1876's. The street NAME crosses;
the number does not, and `address_is_street_only` says which rows are which.
"""
import json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data/research/directories/claims/fergus_1839_directory_entries.json")
HH = os.path.join(ROOT, "data/residents/households")
VOTERS = os.path.join(ROOT, "data/research/civic/voter_crosswalk.json")
GAZETTEER = os.path.join(ROOT, "data/research/newspapers/gazetteer.json")
HEADS_1840 = os.path.join(ROOT, "data/research/census_1840/resident_crosswalk.json")
OUT = os.path.join(ROOT, "data/research/directories/fergus_1839_crosswalk_1835.json")

FOLD = [(r"[^a-z]", ""), (r"^mc", "mac"), (r"^m$", ""), (r"ii", "n"), (r"rn", "m"),
        (r"vv", "w"), (r"1", "l"), (r"0", "o")]
TITLES = ("mrs", "miss", "mr", "dr", "capt", "col", "rev", "gen", "maj", "hon", "esq")


def fold(name: str) -> str:
    s = (name or "").lower()
    for pat, rep in FOLD:
        s = re.sub(pat, rep, s)
    return s


def initial(given: str) -> str:
    for tok in (given or "").split():
        if tok.strip(".,'\"").lower() in TITLES:
            continue
        for ch in tok:
            if ch.isalpha():
                return ch.lower()
    return ""


def split_name(name: str):
    """A pool name as surname + given. 'W. H. Adams' and 'Adams, W. H.' both work."""
    name = (name or "").strip()
    if "," in name:
        surname, given = name.split(",", 1)
        return surname.strip(" ."), given.strip(" .")
    parts = [p for p in name.replace(".", ". ").split() if p]
    parts = [p for p in parts if p.strip(".,").lower() not in TITLES]
    if len(parts) < 2:
        return "", ""
    return parts[-1].strip(" ."), " ".join(parts[:-1])


def residents():
    """Every person the 1835 layer holds, with the household they belong to."""
    out = []
    for fn in sorted(os.listdir(HH)):
        if not fn.endswith(".json"):
            continue
        doc = json.load(open(os.path.join(HH, fn), encoding="utf-8"))
        for p in doc.get("persons") or []:
            name = (p.get("name") or "").strip()
            if not name or (p.get("id") or "").endswith("_household"):
                continue
            surname, given = split_name(name)
            if not surname or not given:
                continue
            out.append({
                "name": name, "surname": surname, "given": given,
                "person_id": p.get("id"), "household_id": doc.get("id"),
                "grade": p.get("grade"),
                "occupation": ((p.get("occupation") or {}).get("value")),
                "lives_at": ((doc.get("lives_at") or {}).get("value")),
            })
    return out


def list_pool(path, key, name_of, label_of):
    doc = json.load(open(path, encoding="utf-8"))
    out = []
    for row in doc.get(key) or []:
        name = name_of(row)
        surname, given = split_name(name)
        if not surname or not given:
            continue
        out.append({"name": name, "surname": surname, "given": given,
                    "label": label_of(row)})
    return out


def row_of(entry):
    n = entry["normalized"]
    return {
        "claim": entry["id"],
        "as_printed": n["as_printed"],
        "printed_page": entry["locator"]["printed_page"],
        "occupation_1839": n["occupation"],
        "address_1839": n["address"],
        "streets_1839": n["streets"],
        # Fergus's own warning, applied per row: a number off Lake street is 1876's.
        "address_is_street_only": bool(n["number_is_1876"]),
    }


def index(entries):
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
    return by_key, surnames


def match_pool(pool, by_key, surnames, extra=None):
    """One pool against the index. Returns (matched, ambiguous, refused)."""
    matched, ambiguous, refused = [], [], []
    for r in pool:
        f, i = fold(r["surname"]), initial(r["given"])
        hits = by_key.get((f, i), []) if i else []
        if not hits:
            if f in surnames:
                refused.append({
                    "name": r["name"],
                    "candidates_under_that_surname": len(surnames[f]),
                    "rule": "The surname %r is in Fergus 1839 and no entry under it carries "
                            "the initial %r of %r. A surname-only agreement is a refusal."
                            % (r["surname"], (i or "-").upper(), r["name"]),
                })
            continue
        rec = {"name": r["name"],
               "rule": "Surname %r folds to the same string as the 1839 entry's, and the "
                       "given name of both begins %s." % (r["surname"], i.upper()),
               "entries_1839": [row_of(h) for h in hits]}
        if extra:
            rec.update(extra(r))
        (matched if len(hits) == 1 else ambiguous).append(rec)
    return matched, ambiguous, refused


def main():
    entries = json.load(open(ENTRIES, encoding="utf-8"))["claims"]
    by_key, surnames = index(entries)

    people = residents()
    res_matched, res_ambiguous, res_refused = match_pool(
        people, by_key, surnames,
        extra=lambda r: {"person_id": r["person_id"], "household_id": r["household_id"],
                         "grade_1835": r["grade"], "occupation_1835": r["occupation"],
                         "lives_at_1835": r["lives_at"]})
    # What a match COULD carry, if the pass that spends it decides to. The residents
    # layer writes `none_recorded` where it holds no trade, and 738 of its 849 people
    # carry that — an absent trade is the field's most common value, not a null.
    for m in res_matched:
        carries = []
        has_trade = m["occupation_1835"] not in (None, "", "none_recorded", "unknown")
        if not has_trade and any(x["occupation_1839"] for x in m["entries_1839"]):
            carries.append("occupation")
        if any(x["streets_1839"] for x in m["entries_1839"]):
            carries.append("street_1839")
        m["could_carry"] = carries
        m["carry_rule"] = ("Whatever is carried is carried as 1839 evidence with "
                           "describes_date 1839 on the note, never as an 1835 fact, and the "
                           "grade of the person does not move. The street NAME may cross; "
                           "the street NUMBER may not — see address_is_street_only.")

    # ONE 1839 ENTRY, TWO 1835 PEOPLE is a collision, not a match.
    claimed = defaultdict(list)
    for m in res_matched:
        claimed[m["entries_1839"][0]["claim"]].append(m)
    contested = []
    for _, rivals in sorted(claimed.items()):
        if len(rivals) > 1:
            for m in rivals:
                m["contested_with"] = [x["name"] for x in rivals if x is not m]
                m["rule"] += (" CONTESTED: %d residents of 1835 meet this one 1839 entry on "
                              "that rule, and at most one of them is the person printed. The "
                              "match is not made." % len(rivals))
                contested.append(m)
    res_matched = [m for m in res_matched if "contested_with" not in m]

    voters = list_pool(VOTERS, "entries", lambda r: r.get("normalized") or r.get("as_read"),
                       lambda r: r.get("list"))
    v_matched, v_ambiguous, v_refused = match_pool(voters, by_key, surnames)
    letters = list_pool(GAZETTEER, "persons", lambda r: r.get("name"),
                        lambda r: r.get("id"))
    l_matched, l_ambiguous, l_refused = match_pool(letters, by_key, surnames)
    heads = list_pool(HEADS_1840, "heads", lambda r: r.get("normalized") or r.get("as_read"),
                      lambda r: r.get("familysearch_id"))
    h_matched, h_ambiguous, h_refused = match_pool(heads, by_key, surnames)

    doc = {
        "schema": 1,
        "_doc": "GENERATED by tools/crosswalk_fergus_1839.py. Fergus' 1839 directory against "
                "the 1835 residents layer, the voter and poll lists, the letter-list and "
                "newspaper persons, and the 1840 heads. A PROPOSAL: it changes no resident "
                "record, mints nobody and regrades nobody. Under the ratified ladder an 1839 "
                "listing alone never makes an 1835 resident.",
        "generated_by": "tools/crosswalk_fergus_1839.py",
        "source_id": "fergus_chicago_directory_1839",
        "ticket": "T-0506",
        "rule": __doc__.split("The rule, written out")[1].split("FOUR POOLS")[0].strip(),
        "scene_relation": "1839 is four years after the scene date of 1 July 1835, and this "
                          "volume is Fergus's 1876 completion of a list first set up from "
                          "memory in 1839. Evidence about 1839, recalled in 1876.",
        "mints_or_regrades": False,
        "address_rule": "An address number in this directory is an 1876 number everywhere "
                        "except Lake street, on the compiler's own statement (printed page 3). "
                        "Only the street name crosses; address_is_street_only marks every row "
                        "where the printed number must be dropped.",
        "inputs": [
            {"what": "Fergus 1839 personal entries indexed", "n": sum(len(v) for v in surnames.values())},
            {"what": "residents layer, persons", "path": "data/residents/households/", "n": len(people)},
            {"what": "voter, poll and tax list entries (T-0493)",
             "path": "data/research/civic/voter_crosswalk.json", "n": len(voters)},
            {"what": "letter-list and newspaper persons",
             "path": "data/research/newspapers/gazetteer.json", "n": len(letters)},
            {"what": "1840 heads of household read in this repo",
             "path": "data/research/census_1840/resident_crosswalk.json", "n": len(heads)},
        ],
        "counts": {
            "residents_matched_one_entry": len(res_matched),
            "residents_ambiguous": len(res_ambiguous),
            "residents_contested": len(contested),
            "residents_surname_only_refused": len(res_refused),
            "voters_matched_one_entry": len(v_matched),
            "voters_ambiguous": len(v_ambiguous),
            "voters_surname_only_refused": len(v_refused),
            "letter_list_matched_one_entry": len(l_matched),
            "letter_list_ambiguous": len(l_ambiguous),
            "letter_list_surname_only_refused": len(l_refused),
            "heads_1840_matched_one_entry": len(h_matched),
            "heads_1840_ambiguous": len(h_ambiguous),
            "heads_1840_surname_only_refused": len(h_refused),
            "residents_could_carry_occupation": sum(
                1 for m in res_matched if "occupation" in m["could_carry"]),
            "residents_could_carry_street": sum(
                1 for m in res_matched if "street_1839" in m["could_carry"]),
        },
        "residents": {
            "matches": sorted(res_matched, key=lambda m: m["name"]),
            "contested": sorted(contested, key=lambda m: m["name"]),
            "ambiguous": sorted(res_ambiguous, key=lambda m: m["name"]),
            "refusals": sorted(res_refused, key=lambda m: m["name"]),
        },
        "voters": {"matches": sorted(v_matched, key=lambda m: m["name"]),
                   "ambiguous": sorted(v_ambiguous, key=lambda m: m["name"]),
                   "refusals": sorted(v_refused, key=lambda m: m["name"])},
        "letter_list": {"matches": sorted(l_matched, key=lambda m: m["name"]),
                        "ambiguous": sorted(l_ambiguous, key=lambda m: m["name"]),
                        "refusals": sorted(l_refused, key=lambda m: m["name"])},
        "heads_1840": {"matches": sorted(h_matched, key=lambda m: m["name"]),
                       "ambiguous": sorted(h_ambiguous, key=lambda m: m["name"]),
                       "refusals": sorted(h_refused, key=lambda m: m["name"])},
    }
    if "--check" in sys.argv:
        if json.load(open(OUT, encoding="utf-8")) != doc:
            print("fergus 1839 crosswalk: the committed file does not match — regenerate",
                  file=sys.stderr)
            return 1
        print("fergus 1839 crosswalk: matches the committed file")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(doc["counts"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
