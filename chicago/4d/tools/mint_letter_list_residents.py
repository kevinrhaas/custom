#!/usr/bin/env python3
"""The names the post office held letters for TWICE become residents (T-0378).

    python3 tools/mint_letter_list_residents.py           write
    python3 tools/mint_letter_list_residents.py --check   re-derive and diff
    python3 tools/mint_letter_list_residents.py --report  the mint and every refusal

WHAT THIS IS FOR, AND WHY IT IS NOT THE WHOLE LIST.

The owner's ruling of 2026-08-28 is that a name in the post office's list of
uncalled-for letters is enough to make somebody a resident. `register_1835.json`
carries such people the town does not hold in the thousands, and
`tools/mint_documented_residents.py` cannot reach one of them: its pool is a
`new_resident` WITH a trade, and a letter-list name has none. Put them through that
pass's eight refusals and most of a thousand survive — a town of a few hundred people
where three residents in four would be a name on a post-office list and nothing else.
That is a question about the SCALE of this reconstruction and it belongs to the owner;
it is ticket T-0379.

NO FIGURE FOR THAT COHORT IS WRITTEN DOWN HERE, DELIBERATELY. The corpus grows on
most weeks the loop runs, and a count copied into prose is wrong the next time a
transcription lands — the ones this docstring used to carry (1,530 in the pool, 726
surviving, ten in more than one return) were all stale inside a fortnight. Run
`--scale-report` instead: it prices the cohort through the very refusals below, on
whatever the tree currently holds, and prints what each of the owner's three answers
would do to the town.

THIS PASS TAKES THE SLICE THE CORPUS ITSELF RANKS HIGHEST, and the ranking is a rule
rather than a sample. The Democrat reprinted one return of uncalled-for letters over
consecutive weekly issues, so a name's MENTIONS are not its RETURNS: grouping a name's
issues at a gap of more than sixty days separates a reprint from a genuinely later list.
A name the office held once is a person somebody wrote to. A name it held in two returns
sixteen months apart is a person somebody kept believing was reachable at Chicago, and it
is the strongest thing a letter list can say about residence.

WHAT THE RECORD CLAIMS, AND WHAT IT REFUSES TO.

A letter list gives a name and nothing else — no trade, no street, no household, no
arrival. So these records claim a PERSON and no more: `occupation` is `none_recorded`
graded `reconstructed`, exactly as this dataset already writes the absence of a trade for
a wife or a child, and the dwelling, the division, the origin, the family and the party
are each written unattested in their own block. `letter_list_only: true` rides on the
person, because the parent ticket's whole point is that the two evidence strengths must
stay distinguishable forever: a letter-list name and a man who advertised his shop are
not the same claim, and `renderers/web/js/residents.js` says so on the card.

THE LIMIT THIS PASS CANNOT CLOSE, stated rather than hidden. The Chicago post office
served the country around the town as well as the town, so an uncalled-for letter is
evidence that its writer believed the addressee reachable at Chicago and not proof that
he slept there. Refusal 6 catches the ones the corpus places somewhere else by name; it
cannot catch a settler the corpus never places at all. A scan read, a land record or a
second corpus that places one of these ten outside the town retires that record, and the
note on every one of them says so.

THE REFUSALS, all eight of `mint_documented_residents.py`'s, on the same reasoning, plus
the precedence rule this pass owes the one beside it:

  1. `garbled`                — the transcription bracketed the name as uncertain.
  2. `a firm, not a person`.
  3. `first evidence after the scene date` — AGENTS.md rule 3.
  4. `no surname the corpus prints`.
  5. `a surname and nothing else` — index.json's `darwin_of_canada` decision.
  6. `placed where this project cannot put him in the town`.
  7. `the town already names a <Surname>` — and for this pass that INCLUDES the
     households `mint_documented_residents.py` minted. A man the papers give a trade is
     better evidenced than a name on a letter list, so where the two passes would reach
     for one family name the documented pass keeps it and this one gives way.
  8. `surname already minted` — one surname, one household, across this pass.

WHY THE POOL READS `enrich` BACK. Same as the documented pass: the register is compiled
FROM the committed town, so the moment this pass mints somebody the compiler stops calling
him `new_resident`. An `enrich` whose target is one of THIS pass's own person ids is read
back as what it is — this pass's previous answer — so the derivation still holds the run
after it lands.
"""
from __future__ import annotations

import argparse
import datetime
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

SCENE_DATE = "1835-07-01"
PREFIX = "hh_ll_"
PERSON_PREFIX = "ll_"
DIVISION = "unplaced"

# The gap that separates one return of uncalled-for letters from the next. The
# Democrat reprinted a list over two and three consecutive weekly issues, so
# anything at a week's distance is the SAME return read twice; the returns
# themselves are quarterly. Sixty days is wider than any reprint run in this
# corpus and narrower than any interval between returns in it, and the ten names
# this admits are unchanged anywhere from 30 to 200 days.
RETURN_GAP_DAYS = 60
RETURNS_REQUIRED = 2

# Everything below is shared with tools/mint_documented_residents.py, which is the
# pass this one sits beside. Importing it would make one pass's refusals depend on
# the other's file being loadable; the two are deliberately independent programmes
# over the same register, and each states its own rules in its own docstring.
TITLES = {"dr", "mr", "mrs", "miss", "jr", "sr", "esq", "capt", "col", "maj",
          "rev", "messrs"}
FEMALE_TITLES = {"mrs", "miss"}
MALE_TITLES = {"mr"}
FIRM = re.compile(r"&| and |\bco\b|\bcompany\b", re.I)
UNCERTAIN = re.compile(r"\[|uncertain", re.I)
BARE_TOWN = {"chicago", "the town of chicago"}
STREETS = DATA / "streets" / "1835.json"
STRUCTURES = DATA / "structures"
PAPERS = (("chicago_democrat_", "chicago_democrat_1833_1835"),
          ("chicago_american_", "chicago_american_1835"))
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
    """'Foot, S.' -> 'S. Foot'. The papers print both orders; a card shows one."""
    if "," not in name:
        return name.strip()
    head, _, tail = name.partition(",")
    tail = tail.strip()
    return f"{tail} {head.strip()}".strip() if tail else head.strip()


def slug(name: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_",
                                     " ".join(words(name)).lower())).strip("_")


def issue_date(claim_id: str) -> datetime.date | None:
    m = re.search(r"(\d{4})_(\d{2})_(\d{2})", claim_id.split("#")[0])
    if not m:
        return None
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def issue_of(claim_id: str) -> str:
    """'chicago_democrat_1834_06_11#c003' -> 'the Democrat of 11 June 1834, column 3'."""
    stem = claim_id.split("#")[0]
    col = claim_id.split("#")[1] if "#" in claim_id else ""
    d = issue_date(claim_id)
    if d is None:
        return claim_id
    paper = "the American" if "american" in stem else "the Democrat"
    tail = f", column {int(col[1:])}" if col.startswith("c") and col[1:].isdigit() else ""
    return f"{paper} of {d.day} {MONTHS[d.month - 1]} {d.year}{tail}"


def returns_of(mentions) -> list[list[str]]:
    """A name's mentions grouped into the RETURNS they are printings of.

    Consecutive issues carrying the same list are one return read more than once;
    a gap wider than RETURN_GAP_DAYS is the next list. Mentions with no readable
    issue date fall into the run they are printed among rather than being dropped.
    """
    dated = sorted(((issue_date(c), c) for c in mentions),
                   key=lambda p: (p[0] or datetime.date.min, p[1]))
    groups: list[list[str]] = []
    last: datetime.date | None = None
    for when, cid in dated:
        if not groups or (when and last and (when - last).days > RETURN_GAP_DAYS):
            groups.append([])
        groups[-1].append(cid)
        last = when or last
    return groups


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
    """Every place name this project can resolve INSIDE the town it models."""
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
        if isinstance(doc.get("name"), str) and norm(doc["name"]):
            places.add(norm(doc["name"]))
        for aka in doc.get("aka") or []:
            if isinstance(aka, str) and norm(aka):
                places.add(norm(aka))
    return places


def town_family_names(docs: dict, index: dict, skip_prefix: str | None = PREFIX) -> set[str]:
    """The family names the committed dataset already has something to say about.

    THIS PASS'S OWN OUTPUT IS EXCLUDED and nothing else is — refusal 7's precedence
    rule, and this pass sits LAST in the three-way order that
    `mint_documented_residents.MINTED_PREFIXES` documents. The two passes above it
    skip these `hh_ll_` records, so neither derivation is changed by anything minted
    here; this one sees both `hh_doc_` and `hh_placed_` and gives way to them.

    `skip_prefix=None` is what --scale-report reads the town through: the cohort it
    prices is a LATER pass than this one, so the households this one has already
    minted are committed and standing, and a surname they hold is a surname the town
    names.
    """
    known: set[str] = set()
    for path, doc in docs.items():
        if skip_prefix and path.name.startswith(skip_prefix):
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

def norm_place(s: str) -> str:
    return re.sub(r"[^a-z ]", "", (s or "").lower()).strip()


def letter_list_pool(register: dict) -> list[dict]:
    """Every letter-list-only name the town does not hold.

    Includes this pass's own previous answer, read back as an `enrich` on one of its
    own person ids — see the docstring's last paragraph.
    """
    return [p for p in register["persons"]
            if p.get("letter_list_only")
            and (p.get("action") == "new_resident"
                 or (p.get("action") == "enrich"
                     and str(p.get("action_target") or "").startswith(PERSON_PREFIX)))]


def apply_refusals(candidates: list[dict], gazetteer: dict, known: set[str],
                   in_town: set[str]):
    """The eight refusals, in order, over an already-ranked list of candidates.

    Held apart from `mint` because --scale-report prices a DIFFERENT cohort out of
    the same pool, and the price is only worth anything if it is paid through these
    exact rules rather than a second implementation of them that could drift.
    Refusal 8 depends on the order it is handed, so ranking is the caller's job.
    """
    taken: set[str] = set()
    accepted, refusals = [], []
    for cand in candidates:
        gaz = gazetteer[cand["id"]]
        name = cand["name"]
        fam = surname(name)
        outside = [p for p in (gaz.get("associated_places") or [])
                   if norm_place(p) not in in_town]
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
            reason = "a surname and nothing else"
        elif outside:
            reason = ("placed where this project cannot put him in the town ("
                      + "; ".join(outside) + ")")
        elif fam in known:
            reason = f"the town already names a {fam.title()}"
        elif fam in taken:
            reason = "surname already minted"
        if reason:
            refusals.append((cand["id"], name, len(returns_of(gaz["mentions"])), reason))
            continue
        taken.add(fam)
        accepted.append((cand, gaz))
    return accepted, refusals


def mint(docs: dict, index: dict):
    """Choose who joins the town. Returns (accepted, refusals)."""
    register = load(REGISTER)
    gazetteer = {p["id"]: p for p in load(GAZETTEER)["persons"]}
    known = town_family_names(docs, index)
    in_town = in_town_places()

    candidates = [p for p in letter_list_pool(register)
                  if len(returns_of(gazetteer[p["id"]]["mentions"])) >= RETURNS_REQUIRED]
    candidates.sort(key=lambda p: (-len(returns_of(gazetteer[p["id"]]["mentions"])),
                                   -len(gazetteer[p["id"]]["mentions"]),
                                   p["first_seen"], p["id"]))
    return apply_refusals(candidates, gazetteer, known, in_town)


# ---------------------------------------------------------------------------
# the records
# ---------------------------------------------------------------------------

def record(cand: dict, gaz: dict) -> dict:
    name = display(cand["name"])
    fam = surname(cand["name"]).title()
    sources = paper_for(gaz["mentions"])
    where = cited(gaz["mentions"])
    printed = sorted({v["as_printed"] for v in gaz.get("variants") or []})
    groups = returns_of(gaz["mentions"])
    returns_said = "; ".join(issue_of(g[0]) for g in groups)
    titles = titles_in(cand["name"])
    pid = PERSON_PREFIX + slug(cand["name"])
    span = (f"{cand['first_seen']} to {cand['last_seen']}")

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
    person["letter_list_only"] = True
    person["occupation"] = {
        "value": "none_recorded",
        "confidence": "reconstructed",
        "note": ("No source records an occupation for this person. A list of uncalled-for "
                 "letters prints a name and nothing else, and this pass will not read a "
                 "trade into one: the absence is recorded here rather than filled in from "
                 "what a man of that name might have done."),
    }
    person["sources"] = list(sources)
    person["note"] = (
        f"KNOWN ONLY FROM THE POST OFFICE, AND HELD THERE MORE THAN ONCE. The papers "
        f"print " + " and ".join(f"'{p}'" for p in printed)
        + f" in {len(groups)} separate returns of letters remaining uncalled-for at the "
        f"Chicago post office — {returns_said} — across {span}. Nothing else in the "
        f"corpus names this person: no trade, no street, no household, no arrival. So "
        f"the record around them carries the person and nothing more, every other claim "
        f"written unattested in its own block. Cited at {where}. "
        f"WHY TWO RETURNS AND NOT ONE: the Democrat reprinted a single return over "
        f"consecutive weekly issues, so a repeated printing is not repeated evidence; a "
        f"name in a LATER return is somebody who was still being written to, months on, "
        f"by a correspondent who believed them reachable at Chicago. Far more names in "
        f"the same pool are printed in one return only and this reconstruction does not "
        f"hold them — ticket T-0379 is that question and it is the owner's, and "
        f"`tools/mint_letter_list_residents.py --scale-report` counts them on the corpus "
        f"as it stands rather than as it stood when this note was written. "
        f"THE LIMIT: the Chicago office served the country around the town, so a letter "
        f"waiting here is not proof of a bed here. A scan read, a land record or a second "
        f"corpus that places this person outside the town retires this record. "
        f"No figure is drawn (docs/LIBERTIES.md L1). READ THROUGH A TRANSCRIPTION, not a "
        f"scan: the owner's ruling of 2026-08-28 grades a transcription-mediated reading "
        f"as documented, and the source record for the run states that standard and its "
        f"limits."
    )

    present = "present" if cand["last_seen"] >= SCENE_DATE else "uncertain"
    doc = {
        "id": PREFIX + slug(cand["name"]),
        "name": f"The {fam} household — a name from the post office's letter lists, unplaced in the town",
        "division": DIVISION,
        "head": pid,
        "arrival": {
            "value": cand["first_seen"],
            "confidence": "inferred",
            "sources": list(sources),
            "note": (f"A BOUND FROM THE PAPER, NOT AN ARRIVAL. The first return holding a "
                     f"letter for this name is {issue_of(gaz['mentions'][0])}, so somebody "
                     f"was writing to them at Chicago by {cand['first_seen']} and at no "
                     f"stated time before it; nothing reached says when they came. Last "
                     f"printed {cand['last_seen']}."),
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
            "note": ("Not attested. NOTHING IS BEING WITHHELD HERE: a letter list gives a "
                     "name and no address, and 52 households in this dataset were already "
                     "in that position before this one was written."),
        },
        "works_at": {
            "value": None, "confidence": "reconstructed",
            "note": ("Not attested. No trade is recorded for this person at all, so there "
                     "is no premises to look for among the committed records."),
        },
        "present_on_scene_date": {
            "value": present,
            "confidence": "inferred",
            "sources": list(sources),
            "note": ((f"A letter was still waiting for this name at "
                      f"{issue_of(groups[-1][0])}, on or after the scene date, so the "
                      f"corpus itself puts somebody expecting them at Chicago at "
                      f"{cand['last_seen']}.")
                     if present == "present" else
                     (f"THE CORPUS STOPS BEFORE THE SCENE DATE. The last return holding a "
                      f"letter for this name is {issue_of(groups[-1][0])}, and nothing "
                      f"reached either follows this person to 1 July 1835 or says they "
                      f"left. A documented resident whose whereabouts on one day are "
                      f"unknown is `uncertain` here rather than dropped: that is the same "
                      f"distinction index.json draws for Jeremiah Porter, and it is a "
                      f"finding rather than a gap.")),
        },
        "persons": [person],
        "touches_removal": False,
        "review_required": False,
        "research_note": (
            f"MINTED FROM THE LETTER LISTS (T-0378), AND THE HOUSEHOLD IS A CONTAINER "
            f"RATHER THAN AN ARGUMENT. Every other record in this dataset argues for a "
            f"household — a family the sources count, or a trade the town demonstrably "
            f"needed. This one argues for a PERSON, and on the weakest evidence this "
            f"project accepts for one: the post office at Chicago held a letter for "
            f"{name} in {len(groups)} separate returns and nobody called for it. "
            f"`data/residents/` has no way to carry a person except inside a household, "
            f"so one was written around them and told to claim nothing: one member, no "
            f"dwelling, no division, no trade, no family, no arrival beyond the bound the "
            f"paper sets. `letter_list_only` is true on the person so that this evidence "
            f"and a shopkeeper's advertisement never read as the same claim — on the card "
            f"a visitor opens as well as in the file. "
            f"tools/mint_letter_list_residents.py derives the whole minted set and prints "
            f"every candidate it refused, with the reason."
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
    # The count sentence's own half of the parent's ask: the panel says how many
    # of the people it lists are known only from the post office, so the evidence
    # strength is legible before a visitor opens anything.
    final = {path: doc for path, doc in docs.items()
             if not path.name.startswith(PREFIX)}
    final.update({path: json.loads(text) for path, text in files.items()
                  if path != INDEX})
    index["counts"]["letter_list_only"] = sum(
        1 for doc in final.values() for person in doc.get("persons") or []
        if person.get("letter_list_only"))
    files[INDEX] = dumps(index, 1)
    return files, accepted, refusals


def report(accepted, refusals) -> None:
    print(f"MINTED — {len(accepted)} letter-list resident(s)")
    for cand, gaz in accepted:
        groups = returns_of(gaz["mentions"])
        print(f"  {PREFIX + slug(cand['name']):30s} {display(cand['name'])[:26]:28s} "
              f"({len(groups)} return(s), {len(gaz['mentions'])} printing(s), "
              f"{cand['first_seen']}..{cand['last_seen']})")
    print(f"\nREFUSED — {len(refusals)} candidate(s) in more than one return, with the reason")
    for cid, name, n, reason in refusals:
        print(f"  {name[:30]:32s} {n} return(s)  {reason}")


# ---------------------------------------------------------------------------
# the cohort this pass does NOT mint, priced for the owner (T-0379)
# ---------------------------------------------------------------------------

def scale_report() -> None:
    """What the 1-return cohort would cost the town, through these same refusals.

    This pass mints the names the post office held letters for in more than one
    return. The names it held ONCE are the rest of the pool, and whether the
    reconstruction should hold them is a question about the SCALE of the town rather
    than about evidence — it is T-0379, and it is the owner's. This prints the
    numbers that question needs, re-derived on whatever the tree currently holds, so
    the answer is given against today's town and not against a figure measured on a
    dev that has since moved.

    THE RANKING, and why it is dates and not printings. Every name here is in exactly
    one return, so `returns` cannot separate them and `printings` counts a reprint run
    the Democrat carried over consecutive weekly issues — repeated printing is not
    repeated evidence, which is this pass's founding argument. What does vary is WHEN
    the office was holding the letter: a return four months before the scene date says
    more about who was at Chicago on 1 July 1835 than one eighteen months before it.
    So the head of the list is dated, and the table below is cut by return.
    """
    docs = {path: load(path) for path in sorted(HOUSEHOLDS.glob("*.json"))}
    index = load(INDEX)
    register = load(REGISTER)
    gazetteer = {p["id"]: p for p in load(GAZETTEER)["persons"]}
    in_town = in_town_places()
    # skip_prefix=None: the 12 households this pass has already minted are committed
    # and standing, so refusal 7 must see their surnames like any other resident's.
    known = town_family_names(docs, index, skip_prefix=None)

    pool = letter_list_pool(register)
    multi = [p for p in pool
             if len(returns_of(gazetteer[p["id"]]["mentions"])) >= RETURNS_REQUIRED]
    single = [p for p in pool
              if len(returns_of(gazetteer[p["id"]]["mentions"])) < RETURNS_REQUIRED]

    def return_date(cand):
        groups = returns_of(gazetteer[cand["id"]]["mentions"])
        for cid in groups[0] if groups else []:
            when = issue_date(cid)
            if when:
                return when
        return datetime.date.min

    single.sort(key=lambda p: (-return_date(p).toordinal(),
                               -len(gazetteer[p["id"]]["mentions"]),
                               p["first_seen"], p["id"]))
    accepted, refusals = apply_refusals(single, gazetteer, known, in_town)

    persons_now = index["counts"]["persons"]
    households_now = index["counts"]["households"]
    ll_now = index["counts"].get("letter_list_only", 0)

    print("T-0379 — THE SINGLE-RETURN COHORT, PRICED THROUGH THIS PASS'S OWN REFUSALS")
    print(f"\nTHE POOL — letter-list-only names the town does not hold: {len(pool)}")
    print(f"  {len(multi):5d} printed in more than one return   — minted by this pass (T-0378)")
    print(f"  {len(single):5d} printed in exactly ONE return      — T-0379's question")

    print(f"\nTHE EIGHT REFUSALS over those {len(single)}, in the order they are applied")
    tally: dict[str, int] = {}
    for _cid, _name, _n, reason in refusals:
        key = reason.split(" (")[0]
        if key.startswith("the town already names"):
            key = "the town already names that family"
        tally[key] = tally.get(key, 0) + 1
    for reason, n in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"  {n:5d}  {reason}")
    print(f"  {'-' * 5}")
    print(f"  {len(refusals):5d}  refused, and {len(accepted)} survive")

    print(f"\nOPTION A — HOLD ALL {len(accepted)}")
    print(f"  persons     {persons_now:5d} -> {persons_now + len(accepted)}")
    print(f"  households  {households_now:5d} -> {households_now + len(accepted)}")
    share = (ll_now + len(accepted)) / (persons_now + len(accepted)) * 100
    print(f"  of the people a visitor could open, {share:.1f}% would be a name on a "
          f"post-office list and nothing else")
    print(f"  (today: {ll_now} of {persons_now}, "
          f"{ll_now / persons_now * 100:.1f}%)")

    print(f"\nOPTION B — HOLD THE DATED HEAD. Survivors by the return that printed")
    print(f"  them, newest first; the running column is the cost of taking every")
    print(f"  return down to and including that row.")
    print(f"  {'return of':>18}  {'survivors':>9}  {'persons':>9}  {'% of town':>9}")
    running = 0
    by_return: dict = {}
    for cand, _gaz in accepted:
        by_return.setdefault(return_date(cand), []).append(cand)
    for when in sorted(by_return, reverse=True):
        running += len(by_return[when])
        total = persons_now + running
        pct = (ll_now + running) / total * 100
        said = (f"{when.day} {MONTHS[when.month - 1]} {when.year}"
                if when != datetime.date.min else "an undated printing")
        print(f"  {said:>18}  {len(by_return[when]):9d}  "
              f"{persons_now:4d} -> {total:<4d}  {pct:8.1f}%")

    print(f"\nOPTION C — HOLD THEM IN A LIGHTER FORM than a household. What a record")
    print(f"  costs today, so the alternative can be priced against it: each of the 12")
    print(f"  households this pass minted is one person, one file, and no dwelling,")
    print(f"  division, family or party — every absence written out in its own block.")
    print(f"  {len(accepted)} more of those is {len(accepted)} files and "
          f"{len(accepted)} households whose `lives_at` names nothing.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and report any drift without writing")
    ap.add_argument("--report", action="store_true",
                    help="print the mint and every refusal")
    ap.add_argument("--scale-report", action="store_true",
                    help="price the single-return cohort this pass refuses (T-0379)")
    args = ap.parse_args()

    if args.scale_report:
        scale_report()
        return 0

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
        print(f"   OK: {len(accepted)} letter-list resident(s) minted from the register, "
              f"{len(refusals)} candidate(s) refused")
        return 0

    for p in sorted(HOUSEHOLDS.glob(f"{PREFIX}*.json")):
        if p not in files:
            p.unlink()
    for p, text in files.items():
        p.write_text(text, encoding="utf-8")
    print(f"minted {len(accepted)} letter-list resident(s); refused "
          f"{len(refusals)} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
