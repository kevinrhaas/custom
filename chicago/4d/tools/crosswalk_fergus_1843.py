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
  Fergus lists thirty-one Smiths. AND, since T-0670, where BOTH readings print a
  full forename and the two full forenames DISAGREE the match is refused as well:
  the initial rule was written for a town of 848 names and it declared
  `Abbott, Thomas L.` onto Titus H. Abbott once T-0514 minted 532 more. An
  initial standing against a full name is untouched and stays a match. The
  forename rule lives in tools/name_agreement.py, which carries its own
  self-test. Where one 1835 person meets more than one 1843 entry on that rule
  the match is AMBIGUOUS and is filed as such, not resolved; where two 1835
  people meet one 1843 entry it is CONTESTED and no match is made.

WHAT THIS DIRECTORY CARRIES THAT NORRIS'S DOES NOT is a date of death. Fergus
compiled the volume in 1896 and set each man's death in brackets after his entry —
"[died June 6, 1882, aged 67.]" — which, with the age, is a year of birth. Those
brackets are carried onto the match as `death_note_1843` for T-0574, which is the
ticket that reads them as birth years. They are not spent here.
"""
import json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import name_agreement as na  # the forename rule, imported rather than restated
import tiebreak            # the tie discriminator (T-0696), likewise

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
                "occupation_confidence": ((p.get("occupation") or {}).get("confidence")),
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

    matches, ambiguous, refusals, forename_refusals = [], [], [], []
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
        kept, refused = [], []
        for h in hits:
            note = na.refusal(r["given"], h["normalized"]["given"])
            (refused if note else kept).append((h, note))
        for h, note in refused:
            row = row_of(h)
            row.update(note)
            forename_refusals.append({
                "resident": r["name"], "person_id": r["person_id"],
                "grade_1835": r["grade"], "entry_1843": row,
            })
        if not kept:
            continue
        rows = [row_of(h) for h, _ in kept]
        rec = {
            "resident": r["name"], "person_id": r["person_id"],
            "household_id": r["household_id"], "grade_1835": r["grade"],
            "occupation_1835": r["occupation"],
            "occupation_1835_confidence": r["occupation_confidence"],
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

    # T-0696. THE TIE DISCRIMINATOR. A trade may NARROW a tie and never make one
    # a match: the narrowed tie is filed below in `discriminated`, the losing
    # side is filed as SILENT rather than contradicted, nothing moves into
    # `matches` and no grade moves. A premises and a year are REFUSED
    # discriminators — tools/tiebreak.py carries both refusals and why.
    discriminated = []
    for _cid, rivals in sorted(claimed.items()):
        if len(rivals) < 2:
            continue
        printed = rivals[0]["entries_1843"][0]["occupation_1843"]
        result = tiebreak.narrow([
            {"key": m["person_id"], "occupation_1835": m["occupation_1835"],
             "printed": printed} for m in rivals])
        winner = next((m for m in rivals if m["person_id"] == result["named"]), None)
        note = tiebreak.block(result, winner["occupation_1835"] if winner else None,
                              winner["occupation_1835_confidence"] if winner else None)
        for m in rivals:
            m["discriminator"] = note or {"kind": tiebreak.KIND, "named": None,
                                          "why": result["why"], "sides": result["sides"]}
        if note:
            discriminated.append({
                "tie": "contested",
                "entry_1843": rivals[0]["entries_1843"][0]["as_printed"],
                "claim": _cid,
                "rivals": [m["resident"] for m in rivals],
                "named": winner["resident"],
                "person_id": winner["person_id"],
                "discriminator": note,
            })

    # The other shape of the same tie: one person of 1835 meeting several
    # printed lines. The sides are the printed entries and the trade is the one
    # the resident carries, so the same rule reads it without restatement.
    for m in ambiguous:
        result = tiebreak.narrow([
            {"key": e["claim"], "occupation_1835": m["occupation_1835"],
             "printed": e["occupation_1843"]} for e in m["entries_1843"]])
        note = tiebreak.block(result, m["occupation_1835"], m["occupation_1835_confidence"])
        m["discriminator"] = note or {"kind": tiebreak.KIND, "named": None,
                                      "why": result["why"], "sides": result["sides"]}
        if note:
            named = next(e for e in m["entries_1843"] if e["claim"] == result["named"])
            discriminated.append({
                "tie": "ambiguous",
                "resident": m["resident"],
                "person_id": m["person_id"],
                "entries": len(m["entries_1843"]),
                "named": named["as_printed"],
                "claim": named["claim"],
                "discriminator": note,
            })

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
        "discriminator_rule": tiebreak.__doc__.split("THE RULING")[1].split(
            "Run it directly")[0].strip(),
        "refused_discriminators": tiebreak.REFUSED_DISCRIMINATORS,
        "counts": {
            "residents_considered": len(people),
            "matched_one_1843_entry": len(matches),
            "matched_more_than_one_ambiguous": len(ambiguous),
            "one_1843_entry_contested_by_two_residents": len(contested),
            "surname_present_initial_absent_refused": len(refusals),
            "initial_agreed_forenames_disagreed_refused": len(forename_refusals),
            "of_those_a_garbled_printed_forename": sum(
                1 for f in forename_refusals if f["entry_1843"]["garbled_reading"]),
            "residents_left_with_no_1843_entry_by_that_refusal": len(
                {f["person_id"] for f in forename_refusals}
                - {m["person_id"] for m in matches + ambiguous + contested}),
            "ties_narrowed_by_a_trade": len(discriminated),
            "of_those_contested": sum(1 for d in discriminated if d["tie"] == "contested"),
            "of_those_ambiguous": sum(1 for d in discriminated if d["tie"] == "ambiguous"),
            "could_carry_occupation": sum(1 for m in matches if "occupation" in m["could_carry"]),
            "could_carry_address": sum(1 for m in matches if "address" in m["could_carry"]),
            "could_carry_death_note": sum(1 for m in matches
                                          if "death_note" in m["could_carry"]),
        },
        "matches": sorted(matches, key=lambda m: m["resident"]),
        "discriminated": sorted(discriminated, key=lambda d: (d["tie"], d["claim"])),
        "contested": sorted(contested, key=lambda m: m["resident"]),
        "ambiguous": sorted(ambiguous, key=lambda m: m["resident"]),
        "refusals": sorted(refusals, key=lambda m: m["resident"]),
        "forename_refusals": sorted(forename_refusals,
                                    key=lambda m: (m["resident"], m["entry_1843"]["claim"])),
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
