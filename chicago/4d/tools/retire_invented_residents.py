#!/usr/bin/env python3
"""Documented people take the roofs the town invented a stand-in for (T-0264).

    python3 tools/retire_invented_residents.py            write
    python3 tools/retire_invented_residents.py --check    re-derive and diff
    python3 tools/retire_invented_residents.py --report   who was paired with what, and why not

WHAT THIS IS FOR. `tools/generate_inferred_households.py` raised 101 households
because the town of 1 July 1835 demonstrably needed that many of those trades and
NO DOCUMENTED PERSON WAS AVAILABLE to put in them; `tools/generate_inferred_names.py`
then gave each head an invented name so that the layer reads as a town rather than
as a table. Both said, in as many words, that the invention would be retired the day
a real person turned up. The newspaper reading turned up 2,201 of them, and
`tools/compile_register.py` sorts the ones whose trade the town invented a household
for into the action `replace_invented`. This is the pass that spends them.

THE HOUSEHOLD KEEPS ITS STRUCTURE AND LOSES ITS INVENTION. The dwelling, the
workplace, the division, the trade argument and every placement in the record are
untouched and stay `reconstructed`: nothing here claims to know where a documented
man slept. What changes is the person standing in the slot — an invented name graded
`reconstructed` becomes a real name graded `attested`, cited to the issue and column
that prints it, and `name_basis` (the invented-name pool citation) is REMOVED, because
validate.py is right that a name_basis on a documented person understates what is
known about a real one.

NOTHING HERE IS AUTHORED, and the same contract binds it that binds the gazetteer and
the register: `--check` re-derives the pairing from committed inputs and refuses a
household this pass would not produce. A hand-placed resident is a place to put a
famous name on a roof without an argument.

THE PAIRING, AND WHY IT REFUSES MORE THAN IT TAKES

The register's `replace_invented` list is a TRADE match and nothing more, and taken
at face value it would put firms, duplicate readings and men with known addresses
into reconstructed cottages. Six refusals stand between it and the town, and every
one of them is a refusal to assert something the corpus does not carry:

  1. NOT A FIRM. 'Dally & Youngs', 'Matthias Mason & Co.', 'Pierce & Abbott' are
     partnership styles that the extraction filed as persons. A firm is not a man and
     may not be given a bed. (T-0337 and T-0338 are the tickets that will teach the
     gazetteer to tell them apart; until then this pass refuses the shape.)
  2. NOT A BRACKETED READING. A name the transcriber could not read whole —
     '[uncertain: W. H. Taylor]', 'Pierce & Abb[ott]' — is a reading about a printing,
     not a name to put on a card. The unbracketed printing of the same man, where the
     corpus has one, is taken instead.
  3. A FORENAME OR AN INITIAL IS REQUIRED. 'Brown' and 'Rockwell' are bare surnames,
     and 'Mr. Graves' is a surname with an honorific in front of it. A bare surname
     can be any one of several men (T-0341), so it names nobody.
  4. NOT SOMEBODY THE TOWN ALREADY HOLDS. A candidate whose surname is already borne
     by anybody in `data/residents/` is refused outright — not merely one who matches
     a resident's initials. That is deliberately blunter than the gazetteer's identity
     policy, which cannot yet merge 'J. T. Temple' with 'John T. Temple' (T-0348), and
     bluntness in this direction costs a retirement while the alternative mints a
     second John T. Temple living somewhere else in the same town.
  5. NOT SOMEBODY THE PAPERS PLACE. If a candidate's surname is a proprietor of a
     business the register can put on a street — `enrich_existing`, `new_building` or
     `street_only` — then that man has an address, and the seeding tickets (T-0263,
     T-0306) are the ones that owe him a roof. An invented household is a slot for a
     person the record CANNOT place; putting a placeable man in one would contradict
     the placement his own advertisement gives.
  6. NOT SOMEBODY THE PAPERS FIRST NAME AFTER THE SCENE DATE. `compile_register.py`
     excludes a business whose first issue is later than 1 July 1835, on the ground
     that nothing evidences it standing on the scene date; a person is under the same
     rule and for the same reason. D. S. Dewey is first printed on 22 July 1835 and is
     refused here, three weeks after the town this dataset describes.
  7. ONE SURNAME, ONCE. No two people this pass mints share a surname, for the reason
     `generate_inferred_names.py` gives about invented ones: a shared surname reads as
     kinship, and here it is likelier still to be two readings of one man.

What survives is ranked by how much evidence the corpus carries for the person — a
name in a notice or an advertisement before a name in a post-office letter list
(the owner's ruling 1 makes a letter-list name enough to MINT a resident, and this
pass takes it as weaker than a notice for choosing WHICH resident), then by how many
times the papers name him, then by how early, then by id so the order is total. The
households of a trade are filled in the layer's own ordinal order, and a trade with
fewer surviving candidates than households retires as many as it can and leaves the
rest invented — which is the honest result, not a shortfall to be made up by
loosening a rule above.

WHERE THIS SITS IN THE PIPELINE. build the households, RETIRE, then name whoever is
left. Retirement before naming, because a name invented for a person who is about to
be replaced is a name allocated out of a pool that the next person then cannot have —
and because the allocator is insertion-local, running the two the other way round
made the committed names irreproducible. `generate_inferred_households.py --check`
composes all three and compares against the end of the pipeline.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
PROGRAMME = DATA / "reconstruction" / "1835_inferred_household_programme.json"
RESEARCH = DATA / "research" / "newspapers"
REGISTER = RESEARCH / "register_1835.json"
GAZETTEER = RESEARCH / "gazetteer.json"
EXTRACTED = RESEARCH / "extracted"

sys.path.insert(0, str(ROOT / "tools"))
from compile_gazetteer import slug, unmarked  # noqa: E402

# The publication record a claim's issue belongs to. The 1833-11-26 issue keeps its
# own senior record — it is the one issue read from the page scans rather than from a
# transcription, and data/sources/chicago_democrat_1833_1835.json says so itself.
SCENE_DATE = "1835-07-01"

ISSUE_SOURCE = {"chicago_democrat_1833_11_26": "chicago_democrat_1833_11_26"}
RUN_SOURCE = (("chicago_democrat_", "chicago_democrat_1833_1835"),
              ("chicago_american_", "chicago_american_1835"))

# Titles and suffixes the papers set around a name. They are not forenames, and
# reading 'Mr.' as the initial M is what would let a bare surname past refusal 3.
HONORIFICS = {"mr", "mrs", "messrs", "miss", "dr", "capt", "col", "gen", "rev", "maj",
              "hon", "esq", "jr", "sr", "sen", "jun", "junr", "senr"}

# A partnership style, as the papers set one. Refusal 1.
FIRM_SHAPE = re.compile(r"&|\band\b|\bco\.|\bcompany\b|\bbro(?:s|ther|thers)?\b", re.I)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(doc, indent: int) -> str:
    return json.dumps(doc, indent=indent, ensure_ascii=False) + "\n"


# --------------------------------------------------------------------------
# names


def split_name(name: str) -> tuple[str, list[str]]:
    """('Foot, S.') and ('S. Foot') both → ('Foot', ['S.']). Honorifics dropped."""
    text = unmarked(name or "").strip()
    if "," in text:
        family, fore = text.split(",", 1)
    else:
        words = text.split()
        family, fore = (words[-1] if words else ""), " ".join(words[:-1])
    fore_words = [w for w in fore.split() if slug(w.strip(".")) not in HONORIFICS]
    family_words = [w for w in family.split() if slug(w.strip(".")) not in HONORIFICS]
    return " ".join(family_words).strip(), fore_words


def identity(name: str) -> tuple[str, tuple[str, ...]]:
    family, fore = split_name(name)
    return slug(family), tuple(w[0].lower() for w in
                               re.findall(r"[^\W\d_]+", " ".join(fore), re.UNICODE))


def display(name: str) -> str:
    """The name as a card should print it: forenames first, honorifics kept off.

    The corpus prints the same man both ways — 'Foot, S.' in a letter list and
    'S. Foot' in a notice — because a list is alphabetised and a notice is not. The
    inversion is a property of the printing, not of the name.
    """
    family, fore = split_name(name)
    return " ".join(fore + [family]).strip()


# --------------------------------------------------------------------------
# the corpus behind a candidate


def source_for(issue_id: str) -> str:
    if issue_id in ISSUE_SOURCE:
        return ISSUE_SOURCE[issue_id]
    for prefix, sid in RUN_SOURCE:
        if issue_id.startswith(prefix):
            return sid
    raise SystemExit(f"no source record for issue {issue_id!r}")


def claim_text(cache: dict, ref: str) -> tuple[str, dict]:
    """The normalized reading of one claim, and its locator."""
    issue_id, cid = ref.split("#", 1)
    if issue_id not in cache:
        cache[issue_id] = load(EXTRACTED / f"{issue_id}.json")
    for claim in cache[issue_id]["claims"]:
        if claim["id"] == cid:
            return claim.get("normalized") or claim.get("quote") or "", claim.get("locator") or {}
    return "", {}


def issue_date(issue_id: str) -> str:
    return issue_id.rsplit("_", 3)[-3] + "-" + issue_id.rsplit("_", 2)[-2] + "-" + \
        issue_id.rsplit("_", 1)[-1]


def witness(cache: dict, gz: dict) -> tuple[str, str, str]:
    """The best single printing to quote: the earliest mention that carries text.

    Returns (source_id, citation, quotation). A letter-list line is a name and a
    column number and nothing else, so the quotation may be very short; that is what
    the evidence is and the note says which kind it is.
    """
    for ref in gz["mentions"]:
        text, locator = claim_text(cache, ref)
        if not text.strip():
            continue
        issue_id = ref.split("#", 1)[0]
        page, col = locator.get("issue_page"), locator.get("column")
        where = ", ".join(x for x in (f"p. {page}" if page else "",
                                      f"col. {col}" if col else "") if x)
        cite = f"{issue_date(issue_id)} {ref.split('#', 1)[1]}" + (f" ({where})" if where else "")
        snippet = " ".join(text.split())
        if len(snippet) > 320:
            snippet = snippet[:317].rstrip() + "…"
        return source_for(issue_id), cite, snippet
    ref = gz["mentions"][0]
    return source_for(ref.split("#", 1)[0]), f"{issue_date(ref.split('#', 1)[0])} " \
        f"{ref.split('#', 1)[1]}", ""


# --------------------------------------------------------------------------
# the pairing


def pairing(report: bool = False) -> list[dict]:
    """The retirement table: which documented person takes which invented roof.

    Derived wholly from committed files, and from none that this pass writes — the
    town it measures itself against is the DOCUMENTED layer, the 72 households the
    reconstruction programme did not raise, so re-running on its own output produces
    the same table.
    """
    programme = load(PROGRAMME)
    register = load(REGISTER)
    gazetteer = {p["id"]: p for p in load(GAZETTEER)["persons"]}

    invented_ids = {h["id"] for h in programme["households"]}
    order = {h["id"]: h["ordinal"] for h in programme["households"]}

    # Refusal 4's exclusion set, and refusal 5's. Both are read off files this pass
    # never writes, which is what makes the table idempotent.
    town_surnames: set[str] = set()
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = load(path)
        if doc["id"] in invented_ids:
            continue
        for person in doc.get("persons", []):
            family, _ = split_name(person.get("name") or "")
            if family:
                town_surnames.add(slug(family))
    placed_surnames: set[str] = set()
    for business in register["businesses"]:
        if business["action"] not in ("enrich_existing", "new_building", "street_only"):
            continue
        for proprietor in business.get("proprietors") or []:
            for part in re.split(r"\s*(?:&|,|\band\b)\s*", unmarked(proprietor)):
                words = part.split()
                if words:
                    placed_surnames.add(slug(words[-1]))

    # The invented heads, per trade, in the layer's own ordinal order.
    slots: dict[str, list[str]] = {}
    for hid in sorted(invented_ids):
        doc = load(HOUSEHOLDS / f"{hid}.json")
        head = next((p for p in doc["persons"] if p.get("relationship") == "head"), None)
        if head is None:
            continue
        slots.setdefault(head["occupation"]["value"], []).append(hid)
    for trade in slots:
        slots[trade].sort(key=lambda h: (order.get(h, 9_999), h))

    candidates: dict[str, list[dict]] = {}
    refusals: list[tuple[str, str, str]] = []
    # THE CANDIDATE SET IS THE REGISTER'S FACTS, NOT ITS ACTIONS, and that is a
    # circularity fix rather than a preference. `compile_register.py` reads the town to
    # decide who is a `replace_invented` candidate — a documented butcher is one only
    # while an INVENTED butcher household is still standing. So the moment this pass
    # spends that household the action flips to `new_resident`, and a pairing keyed on
    # the action would stop deriving its own committed output the next time the register
    # was rebuilt. The trade a paper prints about a person does not move, and neither
    # does the authored occupation census that raised the households, so the candidacy
    # test is built from those two: a documented person whose trade is one the
    # reconstruction programme raised a household for.
    invented_trades = {h["occupation"] for h in programme["households"]}
    for person in register["persons"]:
        trade = person.get("occupation")
        if trade not in invented_trades:
            continue
        name = person["name"]
        why = None
        if FIRM_SHAPE.search(name):
            why = "a partnership style, not a man (refusal 1)"
        elif "[" in name:
            why = "the transcriber could not read the name whole (refusal 2)"
        else:
            family, initials = identity(name)
            if not family or not initials:
                why = "a bare surname names nobody (refusal 3)"
            elif family in town_surnames:
                why = f"the town already holds a {family.title()} (refusal 4)"
            elif family in placed_surnames:
                why = f"the papers give a {family.title()} an address (refusal 5)"
            elif gazetteer[person["id"]]["first_seen"] > SCENE_DATE:
                why = (f"first printed {gazetteer[person['id']]['first_seen']}, after the "
                       f"scene date (refusal 6)")
        if why:
            refusals.append((trade, name, why))
            continue
        gz = gazetteer[person["id"]]
        key = identity(name)
        rank = (0 if not person["letter_list_only"] else 1, -len(gz["mentions"]),
                gz["first_seen"], person["id"])
        bucket = candidates.setdefault(trade, [])
        prior = next((c for c in bucket if c["key"] == key), None)
        entry = {"key": key, "rank": rank, "person": person, "gz": gz,
                 "name": display(name)}
        if prior is None:
            bucket.append(entry)
        elif rank < prior["rank"]:
            # The same man under two printings. Keep the better-evidenced reading and
            # the printing that reads as a name rather than as a letter-list inversion.
            prior.update(entry)
        elif "," in name and "," not in prior["person"]["name"]:
            pass
        elif "," not in name and "," in prior["person"]["name"]:
            prior["name"] = display(name)

    table: list[dict] = []
    spent: set[str] = set()
    cache: dict = {}
    for trade in sorted(slots):
        bucket = sorted(candidates.get(trade, []), key=lambda c: c["rank"])
        picks = []
        for entry in bucket:
            family = entry["key"][0]
            if family in spent:
                refusals.append((trade, entry["person"]["name"],
                                 "this pass already seated a %s (refusal 7)" % family.title()))
                continue
            picks.append(entry)
            spent.add(family)
            if len(picks) == len(slots[trade]):
                break
        for hid, entry in zip(slots[trade], picks):
            sid, cite, quote = witness(cache, entry["gz"])
            table.append({
                "household": hid, "trade": trade, "name": entry["name"],
                "person_id": entry["person"]["id"], "source": sid, "citation": cite,
                "quote": quote, "mentions": len(entry["gz"]["mentions"]),
                "first_seen": entry["gz"]["first_seen"],
                "last_seen": entry["gz"]["last_seen"],
                "letter_list_only": entry["person"]["letter_list_only"],
            })
        if report:
            print(f"{trade:<18} {len(slots[trade]):>2} invented, "
                  f"{len(candidates.get(trade, [])):>2} candidate(s) survive, "
                  f"{len(picks)} retired")
    if report:
        print()
        for trade, name, why in sorted(refusals):
            print(f"  refused  {trade:<16} {name:<34} {why}")
    return sorted(table, key=lambda r: r["household"])


# --------------------------------------------------------------------------
# the record


def retired_person(head: dict, row: dict, argument: str) -> dict:
    """The documented head, built out of the invented one it replaces.

    The trade argument the invention was raised on is KEPT, in the note, because it is
    still the reason this household is in the dataset — what changes is that the town
    no longer has to invent somebody to satisfy it.
    """
    trade = row["trade"].replace("_", " ")
    person = {
        "id": head["id"],
        "name": row["name"],
        "relationship": "head",
        "grade": "attested",
        "sources": [row["source"]],
        "occupation": {
            "value": row["trade"],
            # The trade is what the paper prints about him, so it grades on the paper
            # and not on the census argument that raised the household.
            "confidence": "attested",
            "sources": [row["source"]],
            "note": (f"THE PAPERS NAME HIM A {trade.upper()}. "
                     + (f"{row['citation']}: “{row['quote']}”. " if row["quote"]
                        else f"{row['citation']}. ")
                     + f"The corpus names him {row['mentions']} time(s), "
                     f"{row['first_seen']} to {row['last_seen']}"
                     + (", in post-office letter lists only — the owner's ruling of "
                        "2026-08-28 makes a listed name enough to mint a resident, and "
                        "the trade is the register's match rather than the paper's word"
                        if row["letter_list_only"] else "")
                     + ". THE HOUSEHOLD'S OWN ARGUMENT IS UNCHANGED and is why this "
                     "roof is in the dataset at all: " + argument),
        },
        "note": (
            "A DOCUMENTED PERSON IN A RECONSTRUCTED HOUSEHOLD, AND THE TWO HALVES OF "
            "THAT ARE GRADED SEPARATELY. The person is real and the papers name him: "
            f"{row['citation']}, and {row['mentions']} mention(s) between "
            f"{row['first_seen']} and {row['last_seen']}. WHERE HE LIVED AND WORKED IS "
            "STILL RECONSTRUCTED — the dwelling, the workplace and the division on this "
            "record are the ones the inferred-household programme dealt to the invented "
            "resident this replaces, and NOTHING HERE CLAIMS THEY ARE HIS. No source "
            "this project holds gives him an address; if one did, the register would "
            "have placed him and tools/retire_invented_residents.py would have refused "
            "him for that reason (refusal 5). This is what T-0264 retires: the town "
            "raised this household because it demonstrably needed the trade and had "
            "nobody documented to put in it, and it now has somebody. The invented name "
            "and its `name_basis` are gone with the invention. No figure is drawn "
            "(docs/LIBERTIES.md L1); the liberty taken is the housing, not the man."
        ),
    }
    if "sex" in head:
        person["sex"] = head["sex"]
    return person


def household_name(doc: dict, row: dict) -> str:
    trade = row["trade"].replace("_", " ")
    family = split_name(row["name"])[0]
    return (f"The {family} household — a documented {trade} in a reconstructed "
            f"household ({doc.get('division', '')} division)")


def apply(docs: dict[str, dict], table: list[dict]) -> int:
    """Retire in place. `docs` is {household_id: record}; returns how many were spent.

    THE TRADE ARGUMENT IS READ FROM THE PROGRAMME, not from the head being replaced.
    Reading it off the record would make this pass non-idempotent — the second run
    would quote its own first run's note back at itself — and an idempotent overlay is
    what lets `--check` re-derive the committed tree.
    """
    census = {c["occupation"]: c for c in load(PROGRAMME)["occupation_census"]}
    spent = 0
    for row in table:
        doc = docs.get(row["household"])
        if doc is None:
            continue
        head = next((p for p in doc["persons"] if p.get("relationship") == "head"), None)
        if head is None:
            continue
        argument = census[row["trade"]]["argument"]
        doc["persons"] = [retired_person(head, row, argument) if p is head else p
                          for p in doc["persons"]]
        doc["name"] = household_name(doc, row)
        spent += 1
    return spent


def reindex(index: dict, docs: dict[str, dict]) -> None:
    """The manifest's per-row grade tallies and totals follow the records."""
    for entry in index["households"]:
        doc = docs.get(entry["id"])
        if doc is None:
            continue
        tally: dict[str, int] = {}
        for person in doc.get("persons", []):
            grade = person.get("grade")
            if grade:
                tally[grade] = tally.get(grade, 0) + 1
        if tally:
            entry["grades"] = dict(sorted(tally.items()))
    totals = {"attested": 0, "inferred": 0, "reconstructed": 0}
    for entry in index["households"]:
        for grade, n in entry["grades"].items():
            totals[grade] = totals.get(grade, 0) + n
    index["counts"]["by_grade"] = totals


def overlay(files: dict) -> dict:
    """Apply the retirement to an in-memory {path: text} map and hand it back.

    The household programme calls this between its own build and the naming pass, so
    its drift check compares against the end of the pipeline rather than a midpoint.
    """
    out = dict(files)
    table = pairing()
    docs = {}
    for path, text in files.items():
        if path.parent == HOUSEHOLDS:
            doc = json.loads(text)
            docs[doc["id"]] = (path, doc)
    plain = {hid: doc for hid, (_, doc) in docs.items()}
    apply(plain, table)
    for hid, (path, doc) in docs.items():
        out[path] = dumps(doc, 1)
    index_path = next((p for p in files if p.name == "index.json"), None)
    if index_path is not None:
        index = json.loads(files[index_path])
        reindex(index, plain)
        out[index_path] = dumps(index, 1)
    return out


def build() -> dict[Path, str]:
    """The pass, run against the committed tree."""
    table = pairing()
    docs = {}
    for row in table:
        path = HOUSEHOLDS / f"{row['household']}.json"
        docs[row["household"]] = load(path)
    apply(docs, table)
    files = {HOUSEHOLDS / f"{hid}.json": dumps(doc, 1) for hid, doc in docs.items()}
    index = load(INDEX)
    reindex(index, docs)
    files[INDEX] = dumps(index, 1)
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and report any drift without writing")
    ap.add_argument("--report", action="store_true",
                    help="print the pairing and every refusal, and write nothing")
    args = ap.parse_args()

    if args.report:
        table = pairing(report=True)
        print()
        for row in table:
            print(f"  {row['household']:<34} {row['name']:<24} {row['citation']}")
        print(f"\n  {len(table)} invented household(s) retired")
        return 0

    files = build()
    if args.check:
        drift = [p for p, text in sorted(files.items())
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        for path in drift:
            print(f"   DRIFT: {path.relative_to(ROOT)}")
        if drift:
            print(f"   {len(drift)} file(s) differ from what this pass derives")
            return 1
        table = pairing()
        print(f"   OK: {len(table)} documented resident(s) hold the roofs the town "
              f"invented a stand-in for")
        return 0

    for path, text in sorted(files.items()):
        path.write_text(text, encoding="utf-8")
    table = pairing()
    print(f"retired {len(table)} invented household head(s) in favour of documented people")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
