#!/usr/bin/env python3
"""Every one of the 170 printed lines of the 1 January 1834 return, tied to what holds it.

    python3 tools/letter_list_1834_01_01_crosswalk.py            print the report
    python3 tools/letter_list_1834_01_01_crosswalk.py --write    write the committed copy
    python3 tools/letter_list_1834_01_01_crosswalk.py --check    committed copy still true?
    python3 tools/letter_list_1834_01_01_crosswalk.py --self-test the assertions, broken

WHY THIS EXISTS (T-1008). T-0424 read the page image of the return's ninth and last
impression and counted the printed list: 170 lines, in
`data/research/newspapers/letter_list_1834_01_01_printed.json`. T-0310 had already
minted residents from a CROP of the same return — the 1834-01-28 impression — and the
crops an extraction pass reaches are not the list. So the cohort the town holds is a
floor of the return, and until this file existed nobody could say by how much, or which
names were missing, without hand-assembling the answer.

WHAT THIS TOOL IS. The tie, DERIVED. It reads the printed roster and every letter-list
claim entity belonging to any of the return's nine impressions (the impressions come
from `mint_letter_list_residents.RETURNS`, not from a list kept here), and reports, per
printed line, which claim entity carries it and which minted card — if any — reached it.

THE THREE INSTRUMENTS THAT MAY TIE A LINE, strongest first. Each is exact; none of them
guesses, and a line no instrument reaches is reported untied rather than assigned.

  1. `image`   — the entity carries `read_at_image.printed_line`. T-0424 set that field
                 by reading the line at the scan, so the tie is a reading and not an
                 inference. 77 lines.
  2. `exact`   — the entity's normalized name and the printed line are the SAME string
                 once brackets, unread markers, punctuation and the trailing letter
                 count are removed, and exactly one printed line carries that string.
  3. `surname` — among what tiers 1 and 2 left, exactly one untied line and exactly one
                 untied entity share a surname. Unique in BOTH directions, so it is a
                 forced 1-to-1 match rather than a nearest neighbour.

WHAT IT REFUSES TO DO, and this is the whole reason it stops at three tiers. A fourth
tier was measured before being rejected: surname plus the initials of the given names,
unique both ways, ties exactly ONE further line. Everything past that is fuzzy matching
over OCR, which is T-1005's epic and a different decision — a wrong tie writes a
person's letter onto another person's card, and an untied line costs nothing but a row
in this table. So the residue stays a residue and is named in full.

THE TWO RESIDUES ARE THE WORK, not the failure. Lines no entity reaches are names the
post office printed that this reconstruction has never minted. Entities no line reaches
are what the crops read that the corrected image reading does not support — garbles like
`Gustavus C[…]`, and they are why the tiers are exact.

THE THREE LINES THAT ARE NOT A PERSON. The roster names them itself, in
`printed_length`: two firm lines (`Axtel & Steele`, `Jesse B. Winn & Co.`) and one line
addressed to two women (`Lamira & Laura Carrier`). This file classifies all three from
that declaration rather than by reading the ampersand again, and records what
`mint_letter_list_residents.FIRM` does with each. It refuses all three — which is right
for the two firms and is a FINDING for the Carriers, who are two residents the ruling
admits and the pass cannot mint, because the rule that keeps firms out of the town reads
their `&` as a partnership.

THE NAME CONFLICTS. Where a line's own image reading and the name on the card that
reached it disagree, the disagreement is recorded here. It is not repaired here:
renaming a resident card is the same decision as minting one, and T-1008 says so.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import mint_letter_list_residents as m  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROSTER = ROOT / "data/research/newspapers/letter_list_1834_01_01_printed.json"
EXTRACTED = ROOT / "data/research/newspapers/extracted"
HOUSEHOLDS = ROOT / "data/residents/households"
OUT = ROOT / "data/research/newspapers/letter_list_1834_01_01_crosswalk.json"

RETURN = m.RETURNS[0]          # the return of 1 January 1834
assert RETURN["date"] == "1834-01-01", "RETURNS[0] is no longer the 1834-01-01 return"

BRACKETED = re.compile(r"\[[^\]]*\]")
PUNCT = re.compile(r"[‘’'`,.]")
TRAILING_COUNT = re.compile(r"\s+\d+$")


def norm(s: str) -> str:
    """A printed name reduced to what two readings of it can be compared on.

    Brackets and their contents go (they are the reader's apparatus, not the setting),
    then the unread markers, then the punctuation a compositor varies freely, then the
    trailing count — `Eliphalet Atkins 2` is one addressee with two letters waiting.
    """
    s = BRACKETED.sub("", s or "")
    s = s.replace("…", "").replace("?", "")
    s = PUNCT.sub("", s)
    s = TRAILING_COUNT.sub("", s.strip())
    return re.sub(r"\s+", " ", s).strip().lower()


def surname_of(s: str) -> str:
    """The family name, read the way `mint_letter_list_residents` reads it."""
    shown = m.display(s or "")
    return m.surname(shown)


def entities() -> list[dict]:
    """Every letter-list claim entity printed in any impression of this return."""
    out = []
    for issue in RETURN["printings"]:
        path = EXTRACTED / f"chicago_democrat_{issue.replace('-', '_')}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        for claim in doc.get("claims", []):
            if not claim.get("letter_list_only"):
                continue
            for e in claim.get("entities", []):
                out.append({**e, "_issue": issue, "_claim": claim["id"]})
    return out


def cards() -> dict[str, list[dict]]:
    """Letter-list households, indexed by the surname of the person on them."""
    by_surname: dict[str, list[dict]] = collections.defaultdict(list)
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = json.loads(path.read_text())
        if doc.get("source_pass") != "letter_list":
            continue
        for person in doc.get("persons", []):
            by_surname[surname_of(person.get("name", ""))].append({
                "household": doc["id"],
                "person": person.get("id"),
                "name": person.get("name"),
                "returns": list(person.get("letter_list_returns", [])),
            })
    return by_surname


def build() -> dict:
    roster = json.loads(ROSTER.read_text())
    lines = roster["lines"]
    printed = roster["printed_length"]
    firms = set(printed.get("addressee_lines_that_are_firms", []))
    pairs = set(printed.get("addressee_lines_naming_two_people", []))

    ents = entities()
    tie: dict[int, tuple[str, int]] = {}
    used: set[int] = set()
    by_n = {line["n"]: line for line in lines}

    # 1. the reading at the image
    for i, e in enumerate(ents):
        at = e.get("read_at_image") or {}
        n = at.get("printed_line")
        if n and n in by_n and n not in tie:
            tie[n] = ("image", i)
            used.add(i)

    # 2. the same string, and only one line carries it
    exact: dict[str, list[int]] = collections.defaultdict(list)
    for i, e in enumerate(ents):
        if i not in used:
            exact[norm(e.get("normalized") or e.get("as_printed"))].append(i)
    roster_text: dict[str, list[int]] = collections.defaultdict(list)
    for line in lines:
        if line["n"] not in tie:
            roster_text[norm(line["as_printed"])].append(line["n"])
    for text, ns in sorted(roster_text.items()):
        if len(ns) == 1 and exact.get(text):
            tie[ns[0]] = ("exact", exact[text][0])
            used.update(exact[text])

    # 3. one untied line and one untied entity, sharing a surname
    line_sur: dict[str, list[int]] = collections.defaultdict(list)
    ent_sur: dict[str, list[int]] = collections.defaultdict(list)
    for line in lines:
        if line["n"] not in tie:
            line_sur[surname_of(line["as_printed"])].append(line["n"])
    for i, e in enumerate(ents):
        if i not in used:
            ent_sur[surname_of(e.get("normalized") or e.get("as_printed"))].append(i)
    for sur, ns in sorted(line_sur.items()):
        if sur and len(ns) == 1 and len(ent_sur.get(sur, [])) == 1:
            tie[ns[0]] = ("surname", ent_sur[sur][0])
            used.add(ent_sur[sur][0])

    # THE CARD A LINE REACHES, on the same footing as the tie. A surname is not a
    # person: the return prints `Caleb Foster` and `Alburn Foster`, and attaching every
    # Foster card to every Foster line manufactures a name conflict between two
    # different men. So a card is attached only where the pairing is forced.
    by_surname = cards()
    printings = set(RETURN["printings"])
    person_lines = [line for line in lines
                    if line["as_printed"] not in firms
                    and line["as_printed"] not in pairs]
    cohort: dict[str, list[dict]] = {
        sur: [c for c in held if set(c["returns"]) & printings]
        for sur, held in by_surname.items()
    }
    held_by: dict[int, tuple[str, dict]] = {}
    claimed: set[tuple[str, str]] = set()
    for line in person_lines:                      # 1. the card carries the same name
        for card in cohort.get(surname_of(line["as_printed"]), []):
            if norm(card["name"]) == norm(line["as_printed"]):
                held_by[line["n"]] = ("exact", card)
                claimed.add((card["household"], card["person"]))
                break
    open_lines: dict[str, list[dict]] = collections.defaultdict(list)
    for line in person_lines:                      # 2. one line, one card, one surname
        if line["n"] not in held_by:
            open_lines[surname_of(line["as_printed"])].append(line)
    for sur, ls in sorted(open_lines.items()):
        free = [c for c in cohort.get(sur, [])
                if (c["household"], c["person"]) not in claimed]
        if len(ls) == 1 and len(free) == 1:
            held_by[ls[0]["n"]] = ("surname", free[0])
            claimed.add((free[0]["household"], free[0]["person"]))

    rows = []
    conflicts = []
    ambiguous = []
    for line in lines:
        n = line["n"]
        kind = ("firm" if line["as_printed"] in firms else
                "two_people" if line["as_printed"] in pairs else "person")
        row = {
            "n": n,
            "column": line["column"],
            "as_printed": line["as_printed"],
            "kind": kind,
            "tie": tie[n][0] if n in tie else "untied",
        }
        if kind != "person":
            row["mint_refuses_as_firm"] = bool(m.FIRM.search(line["as_printed"]))
        if n in tie:
            e = ents[tie[n][1]]
            row["entity"] = {
                "issue": e["_issue"],
                "claim": e["_claim"],
                "as_printed": e.get("as_printed"),
                "normalized": e.get("normalized"),
            }
        if n in held_by:
            how, card = held_by[n]
            row["card"] = {"held_by": how, **card}
            if norm(card["name"]) != norm(line["as_printed"]):
                conflicts.append({
                    "n": n,
                    "printed_at_image": line["as_printed"],
                    "card_name": card["name"],
                    "household": card["household"],
                    "person": card["person"],
                })
        elif kind == "person" and cohort.get(surname_of(line["as_printed"])):
            row["card"] = None
            row["cards_sharing_the_surname"] = [
                c["household"] for c in cohort[surname_of(line["as_printed"])]]
            ambiguous.append(n)
        rows.append(row)

    reached = [r for r in rows if r.get("card")]

    # THE MIRROR RESIDUE. A card of this cohort that no printed line reached. The
    # surname instrument cannot see one whose family name the image itself corrected —
    # `hh_crisey_william` stands against a line reading `William Crissy`, and `crisey`
    # and `crissy` are not the same surname to any exact rule. These are the cards the
    # mint piece must reconcile, and naming them is what keeps the count honest in both
    # directions.
    orphans = sorted(
        (c for held in cohort.values() for c in held
         if (c["household"], c["person"]) not in claimed),
        key=lambda c: (c["household"], c["person"] or ""))
    tiers = collections.Counter(r["tie"] for r in rows)
    return {
        "schema": 1,
        "_doc": (
            "EVERY PRINTED LINE OF THE 1 JANUARY 1834 RETURN, TIED TO THE CLAIM ENTITY "
            "AND THE MINTED CARD THAT HOLD IT (T-1008). Derived by "
            "tools/letter_list_1834_01_01_crosswalk.py from the roster T-0424 read at "
            "the scan and from every letter-list claim of the return's nine "
            "impressions. Three exact instruments may tie a line and none of them "
            "guesses; a line no instrument reaches is reported untied. The tool's "
            "docstring carries the reasoning, including the fourth tier that was "
            "measured and refused."
        ),
        "generated_by": "tools/letter_list_1834_01_01_crosswalk.py --write",
        "return": {"date": RETURN["date"], "said": RETURN["said"],
                   "printings": list(RETURN["printings"])},
        "roster": str(ROSTER.relative_to(ROOT)),
        "counts": {
            "printed_lines": len(lines),
            "firm_lines": sum(1 for r in rows if r["kind"] == "firm"),
            "two_people_lines": sum(1 for r in rows if r["kind"] == "two_people"),
            "tied": {k: tiers[k] for k in ("image", "exact", "surname") if tiers[k]},
            "tied_total": len(lines) - tiers["untied"],
            "untied_lines": tiers["untied"],
            "claim_entities": len(ents),
            "entities_tied_to_no_line": len(ents) - len(used),
            "lines_reaching_a_card": len(reached),
            "lines_reaching_no_card": len(lines) - len(reached),
            "lines_a_surname_cannot_decide": len(ambiguous),
            "cohort_cards": sum(len(v) for v in cohort.values()),
            "cards_no_printed_line_reached": len(orphans),
            "name_conflicts": len(conflicts),
        },
        "lines_a_surname_cannot_decide": ambiguous,
        "cards_no_printed_line_reached": orphans,
        "name_conflicts": conflicts,
        "lines": rows,
    }


def dumps(doc: dict) -> str:
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def report(doc: dict) -> None:
    c = doc["counts"]
    print(f"\nTHE RETURN OF 1 JANUARY 1834 — {c['printed_lines']} printed lines")
    print(f"  tied at the image        {c['tied'].get('image', 0):>4}")
    print(f"  tied by exact text       {c['tied'].get('exact', 0):>4}")
    print(f"  tied by a unique surname {c['tied'].get('surname', 0):>4}")
    print(f"  UNTIED                   {c['untied_lines']:>4}   "
          f"names the post office printed that no claim of this return reaches")
    print(f"\n  of {c['claim_entities']} claim entities, "
          f"{c['entities_tied_to_no_line']} tie to no printed line")
    print(f"\n  lines reaching a minted card {c['lines_reaching_a_card']:>4}")
    print(f"  lines reaching no card       {c['lines_reaching_no_card']:>4}")
    print(f"    of which a shared surname cannot decide "
          f"{c['lines_a_surname_cannot_decide']:>3}")
    print(f"\n  of {c['cohort_cards']} card(s) citing a printing of this return, "
          f"{c['cards_no_printed_line_reached']} are reached by no printed line")
    for card in doc["cards_no_printed_line_reached"]:
        print(f"    {card['household']:<34} {card['name']}")

    print(f"\n  {c['firm_lines']} firm line(s), {c['two_people_lines']} line(s) "
          f"naming two people")
    for row in doc["lines"]:
        if row["kind"] != "person":
            print(f"    {row['n']:>4}  {row['as_printed']:<24} {row['kind']:<11}"
                  f" mint refuses as a firm: {row['mint_refuses_as_firm']}")
    print(f"\n  {c['name_conflicts']} card(s) whose name the image contradicts")
    for x in doc["name_conflicts"]:
        print(f"    line {x['n']:>4}  image {x['printed_at_image']!r}"
              f"  card {x['card_name']!r}  {x['household']}")
    print()


def self_test() -> int:
    bad = 0
    def eq(got, want, what):
        nonlocal bad
        if got != want:
            bad += 1
            print(f"   FAILED SELF-TEST: {what}: {got!r} != {want!r}")
    eq(norm("[uncertain: Orinda] Miner 2"), "miner", "brackets and the letter count go")
    eq(norm("Rob't. Fisher"), "robt fisher", "punctuation goes")
    eq(norm("Wm. G. Austin"), "wm g austin", "initials stay")
    eq(surname_of("Lamira & Laura Carrier"), "carrier", "the pair reads as one family")
    eq(bool(m.FIRM.search("Lamira & Laura Carrier")), True,
       "the mint pass refuses the Carriers as a firm — the finding this file records")
    doc = build()
    eq(doc["counts"]["printed_lines"], 170, "the roster is still 170 lines")
    eq(doc["counts"]["firm_lines"] + doc["counts"]["two_people_lines"], 3,
       "three lines are not one person")
    ns = [r["n"] for r in doc["lines"]]
    eq(ns, sorted(ns), "the rows keep printed order")
    eq(len({r["n"] for r in doc["lines"]}), 170, "one row per printed line")
    tied = doc["counts"]["tied_total"] + doc["counts"]["untied_lines"]
    eq(tied, 170, "every line is either tied or untied")
    eq(doc["counts"]["lines_reaching_a_card"]
       + doc["counts"]["cards_no_printed_line_reached"],
       doc["counts"]["cohort_cards"],
       "every cohort card is either reached by a line or named as unreached")
    print("   OK: self-test" if not bad else f"   {bad} self-test failure(s)")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    doc = build()
    if args.write:
        OUT.write_text(dumps(doc))
        print(f"   wrote {OUT.relative_to(ROOT)}")
        return 0
    if args.check:
        if not OUT.exists():
            print(f"   MISSING: {OUT.relative_to(ROOT)} — run --write")
            return 1
        if OUT.read_text() != dumps(doc):
            print(f"   DRIFT: {OUT.relative_to(ROOT)} is not what this pass derives"
                  f" — run --write")
            return 1
        print(f"   OK: {OUT.relative_to(ROOT)} matches what this pass derives "
              f"({doc['counts']['printed_lines']} printed lines, "
              f"{doc['counts']['untied_lines']} untied)")
        return 0
    report(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
