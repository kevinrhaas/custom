#!/usr/bin/env python3
"""The documented tradespeople the town never invented a roof for become residents (T-0376).

    python3 tools/mint_documented_residents.py           write
    python3 tools/mint_documented_residents.py --check   re-derive and diff
    python3 tools/mint_documented_residents.py --report  the mint and every refusal

WHAT THIS IS FOR.

`data/research/newspapers/register_1835.json` reads 2,201 people out of the Democrat
and the American and says, for each, what the committed town would have to do about
them. `replace_invented` is the finding that a trade the town INVENTED a household for
has a documented practitioner — T-0366 and T-0367 spend those. `new_resident` is the
rest: 1,967 documented people this reconstruction does not hold at all.

THIS PASS TAKES ONE SLICE OF THAT, AND THE SLICE IS DEFINED BY THE COMPILER RATHER
THAN BY TASTE. `tools/compile_register.py` gives a person `replace_invented` only when
the trade it reads for him is one the occupation census invented a household for, and
`new_resident` otherwise. So a `new_resident` WITH a trade is, by construction, a
tradesman the town has no roof to offer and never did: an attorney, an auctioneer, a
schoolteacher, a milliner, a hardware merchant. Nobody else's pass can reach him, and
this one cannot reach into theirs. The people with no trade at all are T-0373's; the
1,536 known only from the post office's letter lists are T-0374's.

THEY ARRIVE WITHOUT A ROOF, AND THAT IS THE HONEST ANSWER RATHER THAN A GAP.

Nothing reached says where any of these people slept. `data/town_census.json` already
counts 52 households whose `lives_at` names nothing, so this dataset has always been
able to hold a person the sources put in the town and nowhere in it. A household here
is a CONTAINER and not a claim: one person, no dwelling, no division, no family, and
every one of those absences written as `reconstructed` with "Not attested" in its own
note. The division vocabulary gains `unplaced` for exactly this, because writing
`south` because most of the town was south is the kind of quiet invention this project
exists not to make.

THE EIGHT REFUSALS, AND WHY EACH ONE IS THERE.

  1. `garbled`                — the transcription bracketed the name as uncertain.
  2. `a firm, not a person`   — 'Hamilton & Sons'. A firm cannot head a household; it
                                is a BUSINESS, and the businesses are T-0263's.
  3. `first evidence after the scene date` — AGENTS.md rule 3.
  4. `no surname the corpus prints`.
  5. `a surname, a trade, and nothing else` — data/residents/index.json already
                                records this decision, under `darwin_of_canada`: a
                                real Chicago resident the project declined to write
                                because "a person record whose only content is one
                                clause of somebody else's sentence inflates the
                                documented count without adding evidence". A printed
                                name with no forename and no initial is that case.
  6. `placed where this project cannot put him in the town` — the gazetteer gives him
                                a place, and the place is not the town, one of the
                                committed streets, or a committed structure. 'Mouth of
                                the St. Joseph' and 'Green Bay' are how the corpus
                                names people who were somewhere else; 'Cook county' is
                                how it names people who may never have been in the
                                town at all. A Chicago street does NOT refuse — this
                                pass claims no location, so a street in a man's own
                                record is not contradicted by a household that says
                                nothing about where he lived.
  7. `the town already names a <Surname>` — a committed resident, or one of the
                                index's researched-not-resident findings, carries that
                                family name. Deliberately blunt: a wrongly refused
                                candidate costs the town one documented resident, a
                                wrongly accepted one mints a second copy of a real man
                                or answers a question the project has already opened.
  8. `surname already minted`  — one surname, one household, across the whole pass. A
                                shared surname reads as kinship and this pass claims
                                none; it is also how the same man under two printed
                                forms ('J. Bates' and 'Bates, J.') would take two.

WHY THE POOL READS `enrich` BACK.

The register is compiled FROM the committed town, so the moment this pass mints a man
the compiler stops calling him `new_resident` and starts calling him `enrich` — he is
in the town now, and it is right about that. Reading only `new_resident` would make
the pass unre-derivable the run after it lands. So an `enrich` whose target is one of
THIS pass's own person ids is read back into the pool as what it is: this pass's
previous answer.

WHAT THIS FILE WILL NOT DO. It will not invent an occupation, a dwelling, a division,
a sex or a family; it will not cite a claim the gazetteer does not carry; and it will
not upgrade a grade to make a record look better. The PERSON is `attested` — a source
names him and gives him his trade. Everything the household says about him beyond that
is written as unattested, because it is.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
REGISTER = DATA / "research" / "newspapers" / "register_1835.json"
GAZETTEER = DATA / "research" / "newspapers" / "gazetteer.json"
STREETS = DATA / "streets" / "1835.json"
STRUCTURES = DATA / "structures"

SCENE_DATE = "1835-07-01"
PREFIX = "hh_doc_"
LETTER_LIST_PREFIX = "hh_ll_"   # tools/mint_letter_list_residents.py; see town_family_names
PERSON_PREFIX = "doc_"
DIVISION = "unplaced"

PAPERS = (("chicago_democrat_", "chicago_democrat_1833_1835"),
          ("chicago_american_", "chicago_american_1835"))

TITLES = {"dr", "mr", "mrs", "miss", "jr", "sr", "esq", "capt", "col", "maj",
          "rev", "messrs"}
FEMALE_TITLES = {"mrs", "miss"}
MALE_TITLES = {"mr"}
FIRM = re.compile(r"&| and |\bco\b|\bcompany\b", re.I)
UNCERTAIN = re.compile(r"\[|uncertain", re.I)
BARE_TOWN = {"chicago", "the town of chicago"}

MONTHS = ("January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(doc, indent=1):
    return json.dumps(doc, indent=indent, ensure_ascii=False) + "\n"


def words(name: str) -> list[str]:
    name = re.sub(r"\[[^\]]*\]", "", name or "").replace(".", " ").replace(",", " ")
    return [w for w in re.split(r"\s+", name.strip())
            if w and w.lower().strip("'") not in TITLES]


def titles_in(name: str) -> set[str]:
    raw = re.sub(r"\[[^\]]*\]", "", name or "").replace(".", " ").replace(",", " ")
    return {w.lower().strip("'") for w in re.split(r"\s+", raw.strip())} & TITLES


def surname(name: str) -> str:
    """The family name, lowercased, from either order the papers print it in."""
    parts = words(name)
    if not parts:
        return ""
    if "," in name:
        head = words(name.partition(",")[0])
        return (head[-1] if head else parts[0]).lower().strip("'")
    return parts[-1].lower().strip("'")


def display(name: str) -> str:
    """'Foot, S.' → 'S. Foot'. The papers print both orders; a card shows one."""
    if "," not in name:
        return name.strip()
    head, _, tail = name.partition(",")
    tail = tail.strip()
    return f"{tail} {head.strip()}".strip() if tail else head.strip()


def slug(name: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_",
                                     " ".join(words(name)).lower())).strip("_")


def issue_of(claim_id: str) -> str:
    """'chicago_democrat_1834_06_11#c003' → 'the Democrat of 11 June 1834, column 3'."""
    stem = claim_id.split("#")[0]
    col = claim_id.split("#")[1] if "#" in claim_id else ""
    m = re.search(r"(\d{4})_(\d{2})_(\d{2})$", stem)
    if not m:
        return claim_id
    y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
    paper = "the American" if "american" in stem else "the Democrat"
    tail = f", column {int(col[1:])}" if col.startswith("c") and col[1:].isdigit() else ""
    return f"{paper} of {d} {MONTHS[mo - 1]} {y}{tail}"


def paper_for(claim_ids) -> list[str]:
    out = []
    for cid in claim_ids:
        for prefix, sid in PAPERS:
            if cid.startswith(prefix) and sid not in out:
                out.append(sid)
    return out


def cited(mentions) -> str:
    head = "; ".join(issue_of(c) for c in mentions[:6])
    if len(mentions) <= 6:
        return head
    return f"{head}, and {len(mentions) - 6} further mention(s)"


# ---------------------------------------------------------------------------
# what the town already holds
# ---------------------------------------------------------------------------

def in_town_places() -> set[str]:
    """Every place name this project can resolve INSIDE the town it models.

    The committed streets under their 1835 names, every committed structure's own
    name, and the bare town. Derived, so a street record renamed or a building
    added moves this set with it rather than leaving a hand-typed list behind.
    """
    def norm(s):
        return re.sub(r"[^a-z ]", "", (s or "").lower()).strip()

    places = set(BARE_TOWN)
    for street in load(STREETS)["streets"]:
        name = norm(street.get("name_1835"))
        if name:
            places.add(name)
            places.add(name.replace(" street", "").strip())
    for path in sorted(STRUCTURES.glob("*.json")):
        doc = load(path)
        for key in ("name",):
            if isinstance(doc.get(key), str) and norm(doc[key]):
                places.add(norm(doc[key]))
        for aka in doc.get("aka") or []:
            if isinstance(aka, str) and norm(aka):
                places.add(norm(aka))
    return places


def town_family_names(docs: dict, index: dict) -> set[str]:
    """The family names the committed dataset already has something to say about.

    Read from the household records' own person names and from the index's
    researched-not-resident findings — NOT from this pass's own output, which
    would refuse on the second run every man it seated on the first and make
    `--check` pass against any tree at all.

    NOR from the letter-list pass's output, and that is a PRECEDENCE rule rather
    than the same rule twice. `tools/mint_letter_list_residents.py` mints people
    whose only evidence is a name on a list of uncalled-for letters; a man the
    papers give a trade is better evidenced, so where the two passes reach for
    one family name this one keeps it and that one gives way. It reads THIS
    pass's households and refuses on them; this pass cannot see its households at
    all, which is what keeps this derivation unchanged by anything it mints.
    """
    known: set[str] = set()
    for path, doc in docs.items():
        if path.name.startswith(PREFIX) or path.name.startswith(LETTER_LIST_PREFIX):
            continue
        for person in doc.get("persons") or []:
            fam = surname(person.get("name") or "")
            if fam:
                known.add(fam)
    for entry in index.get("researched_not_resident") or []:
        fam = surname(entry.get("name") or "")
        if fam:
            known.add(fam)
    return known


# ---------------------------------------------------------------------------
# the mint
# ---------------------------------------------------------------------------

def mint(docs: dict, index: dict):
    """Choose who joins the town. Returns (accepted, refusals)."""
    register = load(REGISTER)
    gazetteer = {p["id"]: p for p in load(GAZETTEER)["persons"]}
    known = town_family_names(docs, index)
    in_town = in_town_places()

    def norm(s):
        return re.sub(r"[^a-z ]", "", (s or "").lower()).strip()

    # The pool, and its own previous answer read back (see the module docstring).
    candidates = [p for p in register["persons"]
                  if p.get("occupation") and not p.get("letter_list_only")
                  and (p.get("action") == "new_resident"
                       or (p.get("action") == "enrich"
                           and str(p.get("action_target") or "")
                           .startswith(PERSON_PREFIX)))]
    candidates.sort(key=lambda p: (-len(gazetteer[p["id"]]["mentions"]),
                                   p["first_seen"], p["id"]))

    taken: set[str] = set()
    accepted, refusals = [], []
    for cand in candidates:
        gaz = gazetteer[cand["id"]]
        name = cand["name"]
        fam = surname(name)
        outside = [p for p in (gaz.get("associated_places") or [])
                   if norm(p) not in in_town]
        reason = None
        if UNCERTAIN.search(name):
            reason = "garbled"
        elif FIRM.search(name):
            reason = "a firm, not a person"
        elif cand["first_seen"] > SCENE_DATE:
            reason = "first evidence after the scene date"
        elif not fam:
            reason = "no surname the corpus prints"
        elif len(words(name)) < 2:
            reason = "a surname, a trade, and nothing else"
        elif outside:
            reason = ("placed where this project cannot put him in the town ("
                      + "; ".join(outside) + ")")
        elif fam in known:
            reason = f"the town already names a {fam.title()}"
        elif fam in taken:
            reason = "surname already minted"
        if reason:
            refusals.append((cand["occupation"], cand["id"], name, reason))
            continue
        taken.add(fam)
        accepted.append((cand, gaz))
    return accepted, refusals


# ---------------------------------------------------------------------------
# the records
# ---------------------------------------------------------------------------

def record(cand: dict, gaz: dict) -> dict:
    name = display(cand["name"])
    fam = surname(cand["name"]).title()
    trade = cand["occupation"]
    trade_words = trade.replace("_", " ")
    sources = paper_for(gaz["mentions"])
    where = cited(gaz["mentions"])
    printed = sorted({v["as_printed"] for v in gaz.get("variants") or []})
    reads = ", ".join(gaz.get("occupations") or [trade_words])
    places = list(gaz.get("associated_places") or [])
    titles = titles_in(cand["name"])
    pid = PERSON_PREFIX + slug(cand["name"])

    person = {
        "id": pid,
        "name": name,
        "relationship": "head",
        "grade": "attested",
    }
    if titles & FEMALE_TITLES:
        person["sex"] = "female"
    elif titles & MALE_TITLES:
        person["sex"] = "male"
    person["occupation"] = {
        "value": trade,
        "confidence": "attested",
        "sources": list(sources),
        "note": (f"THE TRADE IS THE PAPER'S. The corpus reads it as {reads}, at "
                 f"{where}. The residents vocabulary's nearest period-correct word "
                 f"for it is `{trade}`, and where the corpus prints more than one "
                 f"trade they are all named here rather than reduced to the one the "
                 f"vocabulary could take."),
    }
    person["sources"] = list(sources)
    person["note"] = (
        f"A DOCUMENTED PERSON, AND NOTHING ELSE IS CLAIMED. The papers name "
        + " and ".join(f"'{p}'" for p in printed)
        + f" and give the trade; they do not say where this household lived, who "
        f"else was in it, or when it came. So the record around this person carries "
        f"nothing but the person: no dwelling, no division, no family, each written "
        f"as unattested in its own block rather than filled in from the shape of the "
        f"rest of the town. Cited at {where}. "
        + (f"The corpus associates the name with {', '.join(places)}; that is where "
           f"the paper does business with this person and not a statement about "
           f"where they slept, and the storefront tickets are the ones that may "
           f"stand a shop there. " if places else "")
        + f"THE TOWN NEVER INVENTED A ROOF FOR THIS TRADE. The occupation census "
        f"raised reconstructed households for the trades a town of 3,265 people "
        f"needed and could not document; `{trade}` was not one of them, which is "
        f"why this person could only ever be ADDED and never seated on an existing "
        f"record — data/research/newspapers/register_1835.json calls it "
        f"`new_resident` for exactly that reason. No figure is drawn "
        f"(docs/LIBERTIES.md L1). READ THROUGH A TRANSCRIPTION, not a scan: the "
        f"owner's ruling of 2026-08-28 grades a transcription-mediated reading as "
        f"documented, and the source record for the run states that standard and "
        f"its limits. A scan read that confirms or corrects the name upgrades this "
        f"entry."
    )

    present = "present" if cand["last_seen"] >= SCENE_DATE else "uncertain"
    doc = {
        "id": PREFIX + slug(cand["name"]),
        "name": f"The {fam} household — a documented {trade_words}, unplaced in the town",
        "division": DIVISION,
        "head": pid,
        "arrival": {
            "value": cand["first_seen"],
            "confidence": "inferred",
            "sources": list(sources),
            "note": (f"A BOUND FROM THE PAPER, NOT AN ARRIVAL. The corpus first "
                     f"prints this person at {issue_of(gaz['mentions'][0])}, so they "
                     f"are in the town's paper by {cand['first_seen']} and at no "
                     f"stated time before it; nothing reached says when they came. "
                     f"Last printed {cand['last_seen']}."),
            "precision": "not_later_than",
        },
        "party_size_on_arrival": {
            "value": None, "confidence": "reconstructed", "note": "Not attested.",
        },
        "origin": {
            "value": None, "confidence": "reconstructed", "note": "Not attested.",
        },
        "reason_for_coming": {
            "value": None, "confidence": "reconstructed", "note": "Not attested.",
        },
        "lives_at": {
            "value": None, "confidence": "reconstructed",
            "note": ("Not attested. NOTHING IS BEING WITHHELD HERE: no source reached "
                     "says where this person lived, and 52 households in this dataset "
                     "were already in that position before this one was written."),
        },
        "works_at": {
            "value": None, "confidence": "reconstructed",
            "note": ("Not attested as a structure this project models. The trade is "
                     "documented; the premises are not one of the committed records."),
        },
        "present_on_scene_date": {
            "value": present,
            "confidence": "inferred",
            "sources": list(sources),
            "note": ((f"Printed on or after the scene date — last at "
                      f"{issue_of(gaz['mentions'][-1])} — so the corpus itself puts "
                      f"this person in the town's paper at {cand['last_seen']}.")
                     if present == "present" else
                     (f"THE CORPUS STOPS BEFORE THE SCENE DATE. Last printed "
                      f"{cand['last_seen']}, at {issue_of(gaz['mentions'][-1])}, and "
                      f"nothing reached either follows this person to 1 July 1835 or "
                      f"says they left. A documented resident whose whereabouts on "
                      f"one day are unknown is `uncertain` here rather than dropped: "
                      f"that is the same distinction index.json draws for Jeremiah "
                      f"Porter, and it is a finding rather than a gap.")),
        },
        "persons": [person],
        "touches_removal": False,
        "review_required": False,
        "research_note": (
            f"MINTED FROM THE NEWSPAPER REGISTER (T-0376), AND THE HOUSEHOLD IS A "
            f"CONTAINER RATHER THAN AN ARGUMENT. Every other record in this dataset "
            f"argues for a household — a family the sources count, or a trade the "
            f"town demonstrably needed. This one argues for a PERSON: the Democrat "
            f"and the American name {name} as a {trade_words} at Chicago "
            f"{len(gaz['mentions'])} time(s), and this reconstruction did not hold "
            f"them. `data/residents/` has no way to carry a person except inside a "
            f"household, so one was written around them and told to claim nothing: "
            f"one member, no dwelling, no division, no origin, no arrival beyond the "
            f"bound the paper sets. Reading a family, a house or a quarter of town "
            f"into this record would be reading something the papers do not say. "
            f"tools/mint_documented_residents.py derives the whole minted set and "
            f"prints every candidate it refused, with the reason."
        ),
    }
    return doc


def build(preload: dict | None = None):
    docs = ({p: json.loads(t) for p, t in preload.items() if p != INDEX}
            if preload is not None
            else {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))})
    index = (json.loads(preload[INDEX]) if preload is not None and INDEX in preload
             else load(INDEX))

    accepted, refusals = mint(docs, index)

    files = {}
    rows = []
    seen: set[str] = set()
    for cand, gaz in accepted:
        doc = record(cand, gaz)
        if doc["id"] in seen:
            raise SystemExit(f"two candidates mint the same household id {doc['id']}")
        seen.add(doc["id"])
        files[HOUSEHOLDS / f"{doc['id']}.json"] = dumps(doc, 1)
        tally: dict = {}
        for person in doc["persons"]:
            tally[person["grade"]] = tally.get(person["grade"], 0) + 1
        rows.append({
            "id": doc["id"],
            "file": f"households/{doc['id']}.json",
            "head": doc["head"],
            "division": doc["division"],
            "persons": len(doc["persons"]),
            "grades": dict(sorted(tally.items())),
            "lives_at": doc["lives_at"]["value"],
            "works_at": doc["works_at"]["value"],
            "present_on_scene_date": doc["present_on_scene_date"]["value"],
            "review_required": doc["review_required"],
        })

    keep = [r for r in index["households"] if not r["id"].startswith(PREFIX)]
    index["households"] = sorted(keep + rows, key=lambda r: r["id"])
    totals = {"attested": 0, "inferred": 0, "reconstructed": 0}
    persons = 0
    for row in index["households"]:
        persons += row["persons"]
        for grade, n in row["grades"].items():
            totals[grade] = totals.get(grade, 0) + n
    index["counts"]["households"] = len(index["households"])
    index["counts"]["persons"] = persons
    index["counts"]["by_grade"] = totals
    files[INDEX] = dumps(index, 1)
    return files, accepted, refusals


def report(accepted, refusals) -> None:
    print(f"MINTED — {len(accepted)} documented resident(s)")
    for cand, gaz in accepted:
        print(f"  {PREFIX + slug(cand['name']):34s} {cand['occupation']:26s} "
              f"{display(cand['name'])[:24]:26s} ({len(gaz['mentions'])} mention(s), "
              f"{cand['first_seen']}..{cand['last_seen']})")
    print(f"\nREFUSED — {len(refusals)} candidate(s), with the reason")
    for trade, cid, name, reason in refusals:
        print(f"  {trade:26s} {name[:30]:32s} {reason}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and report any drift without writing")
    ap.add_argument("--report", action="store_true",
                    help="print the mint and every refusal")
    args = ap.parse_args()

    files, accepted, refusals = build()
    if args.report:
        report(accepted, refusals)
        return 0
    if args.check:
        drift = [p for p, text in files.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        stale = [p for p in sorted(HOUSEHOLDS.glob(f"{PREFIX}*.json"))
                 if p not in files]
        for p in drift + stale:
            print(f"   DRIFT: {p.relative_to(ROOT)}")
        if drift or stale:
            print(f"   {len(drift) + len(stale)} file(s) differ from what this pass "
                  f"derives")
            return 1
        print(f"   OK: {len(accepted)} documented resident(s) minted from the "
              f"register, {len(refusals)} candidate(s) refused")
        return 0

    for p in sorted(HOUSEHOLDS.glob(f"{PREFIX}*.json")):
        if p not in files:
            p.unlink()
    for p, text in files.items():
        p.write_text(text, encoding="utf-8")
    print(f"minted {len(accepted)} documented resident(s); refused "
          f"{len(refusals)} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
