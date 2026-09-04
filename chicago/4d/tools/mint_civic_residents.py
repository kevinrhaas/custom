"""The people the town's own lists name and the residents layer never held (T-0514).

    python3 tools/mint_civic_residents.py --build      write
    python3 tools/mint_civic_residents.py --check      re-derive and diff
    python3 tools/mint_civic_residents.py --report     the mint and every refusal
    python3 tools/mint_civic_residents.py --scale      what this pass did to the town
    python3 tools/mint_civic_residents.py --gate       the invariants this pass owes
    python3 tools/mint_civic_residents.py --self-test  those assertions, broken on purpose

WHAT THIS PASS IS, AND THE RULING IT APPLIES.

The owner ratified a grading ladder on 2026-09-03 — quoted in full in T-0514 and in
`docs/RESEARCH/resident-grading-policy.md` — and T-0513 spent it: `tools/consolidate_
resident_evidence.py --build` reads the seven source domains, clusters them into
identities, and writes `data/research/residents/grading_proposal.json`, which says per
identity what the ladder makes of it. That file is a PROPOSAL and nothing in it was ever
written onto a card. Measured on `dev` before this pass: of the 85 men on the 1835 poll
list only 37 had even a surname in the residents layer. Half the voter-list men — Bread,
Pixby, Kennicott, Ulrich, Trowbridge, Alvin Calhoun — were in no record at all, and the
muster rolls, the tax list, the St Cyr register and the death notices were in the same
position.

This pass writes those people. It mints a household and a person for every identity the
proposal grades `attested` or `inferred` (`projected_resident` included) that the town
does not already carry, on the evidence of the CIVIC lists (poll, tax, muster), the
CHURCH register, the contemporary PRESS, the BOOKS (the two directories and the old
settlers' death notices) and the 1840 CENSUS — every domain except the post office's
lists of uncalled-for letters, which belongs to the pass beside this one.

NO COUNT IS WRITTEN DOWN HERE, DELIBERATELY, for the reason
`mint_letter_list_residents.py` gives at length: the corpus grows most weeks the loop
runs and a figure copied into prose is wrong by the next transcription. Run `--report`
for the mint and every refusal, `--scale` for what the pass is worth to the town.

WHERE IT SITS AMONG THE MINTS, AND WHY IT IS BESIDE THE LETTER LISTS RATHER THAN ABOVE.

T-0514 asked for this pass ABOVE `mint_letter_list_residents.py` in the precedence
`mint_documented_residents.MINTED_PREFIXES` documents, so that where two passes reach
for one family name the better-evidenced one keeps it. Working it showed the precedence
is not what these two passes need, and refusal 3 is why.

That refusal makes the two pools DISJOINT by construction: an identity whose only source
inside the scene year is a post-office letter list is refused here, because the pass
beside this one has already ruled on exactly that pool and the owner's ruling of
2026-08-30 held all of it. Nothing this pass mints rests on a letter list, and nothing
the letter-list pass mints rests on anything else. Two passes over disjoint pools do not
need a precedence between them.

What they do need is not to read each other's output as a prior claim, and that IS a
change to the family-name test: `town_family_names`'s `skip` now carries `("civic",
"hh_civic_")` in all three older mints. The reason is that refusal — "the town already
names a <Surname>" — is a proxy for identity resolution over evidence that is a bare
name, and it is the right proxy there: a letter addressed to `Smith` at Chicago is
probably the Smith the town already holds. This pass does not need the proxy. Its
identities come from the consolidation, which resolves on surname AND forename
signature against every domain at once, and refusal 2 hands back every identity that
resolution reaches. Letting the older passes see these households instead would retire
hundreds of committed letter-list records on a surname collision alone — a deletion the
owner has not ruled on, and the opposite of the one he did make.

WHAT THE RECORD CLAIMS, AND WHAT IT REFUSES TO.

The same claim the three passes before it make, and no more: a PERSON, inside a
household container that is the only way `data/residents/` can carry one. `division` is
`unplaced`; `lives_at` and `works_at` are null with the note saying why — the placement
sweep assigns homes and workplaces once the resident list is complete, which is the
owner's own sequencing and not this pass's to pre-empt. `occupation` reads
`none_recorded`, the residents vocabulary's own word for an absent record: a poll list,
a muster roll and a baptismal entry each print a name and no trade, and where a later
directory prints one it is a trade of 1843, which T-0633 exists to back-project under a
rule this pass does not have. `origin`, `party_size_on_arrival`, `reason_for_coming` and
the family are each written unattested in their own block. No figure is drawn (L1).

`arrival` is a BOUND and says so: `not_later_than` the earliest record inside the scene
year that names the person, at that record's own precision — a full date where the
paper gives one, the year's end where a list gives only a year. Where that bound falls
after 1 July 1835 the validator warns that it straddles the scene date; the note says so
in words, which is what the validator asks for, and `present_on_scene_date` is
`uncertain` rather than `present` for exactly those people.

`present_on_scene_date` is `present` only where the record BRACKETS the day — the person
is named at Chicago at or before 1 July 1835 and named again at or after it. Everyone
else is `uncertain` with the reason: the lists stop before the scene date and nothing
follows them to it. `uncertain` rather than dropped is the distinction index.json draws
for Jeremiah Porter, and it is a finding, not a gap.

THE EVIDENCE BLOCKS, and one deviation from the ticket that is recorded rather than
hidden. T-0514 asked for `civic_evidence[]`, `census_evidence[]` (1830),
`church_evidence[]` and `book_evidence[]`. Four notes on that:

  * There is no 1830 census domain in the consolidation to read — `read_census_1840` is
    the only census reader it has, and `census_1830_peoria_county_chicago_precinct` is a
    source the identity master never offers. `census_evidence[]` therefore carries 1840
    rows, which are LATER evidence and can never be a residency source on their own
    (refusal 3 and the ladder's G0 both say so); they corroborate a person the scene-year
    record already reaches.
  * `press_evidence[]` is added, because the ticket's four blocks have no home for the
    contemporary newspapers and the ladder's G1b — a Chicago paper of 1833-1835 printing
    the person by name in the town — is the largest single rung in this pool.
  * Every row carries the ladder rule id that fired for the identity, the list it was
    read from, the transcription AS READ, the locator and the source id, so a card can
    show the reading and a reader can go back to the page.
  * The books are the two directories and the old settlers' death notices together:
    both are a later book's recollection of an earlier town, and the ladder treats them
    the same way.

THE TENSION WITH `mint_placed_residents.py`, stated rather than buried. That pass put
the register's tradeless `new_resident` people through a residency test derived from the
corpus (L213) and refused 382 of them — "a name printed in a Chicago paper is not a
Chicago resident". The owner's ladder, ratified a fortnight later, reads the same
evidence differently at G1b. This pass applies the ladder, because the ladder is the
ratified rule and T-0514 is the instruction to spend it; `--report` counts how many of
the people it mints that older test had refused, so the disagreement stays visible and
countable instead of being settled quietly. docs/LIBERTIES.md L215 is where it is
admitted.

THE REFUSALS, in the order they fire, each one printed by `--report`:

  1. `the ladder does not reach this identity`   — the proposal grades it
     `not_1835_resident` or abstains (G0, G5). Nothing is minted from an 1839 directory
     or an 1840 census appearance alone, which is the ladder's own first sentence.
  2. `the town already carries this person`      — the consolidation resolved the
     identity onto a committed card. T-0515 regrades those; this pass never touches one.
  3. `the town has researched this person and left them out` — index.json's
     `researched_not_resident` list is the exclusions-style half of this dataset and it
     outranks any mint. A finding that somebody is NOT in this scene was argued once and
     is not quietly reversed by a pass that reads the same name off a list.
  4. `an 1832 enrollment alone is earlier evidence and never mints` — the Black Hawk War
     enrollment record states its own ladder: "An 1832 enrollment is EARLIER evidence and
     never an 1835 residence on its own: it places the man in this town in 1832, which is
     why it dates and corroborates rather than mints"
     (`data/research/civic/records/blackhawk_war_1832_chicago.json`, `the_ladder`). That
     reading is the project's and this pass does not overturn it from a rung the
     consolidation assigns generically. It also keeps this pass away from the 94 rows the
     index prints in the INDIAN company with no surname comma at all: their names cannot
     be read in a surname-first model without inventing an order for them, and any record
     touching the removal is subject to AGENTS.md's standing constraint rather than to a
     mint tool's judgement.
  5. `the post office's letter lists are the pass beside this one's pool` — every
     appearance inside the scene year is a letter list. See above.
  6. `a firm, not a person` — and it fires before the surname rule below, because "&
     Co" reads as a two-letter family name and the firm is the truer finding.
  7. `the transcription bracketed the name as uncertain`.
  8. `no name the corpus prints as a family name` — nothing that could be a surname.
  9. `no appearance inside the scene year` — there is no record to bound an arrival at
     or before the scene date with, so minting one would assert an arrival the sources
     do not reach. A later-only source is never a residency source.
 10. `a duplicate of a person the town already carries` — the id this identity would
     take is already a person's. The consolidation did not link them and this pass will
     not overwrite a card to find out; it is a merge for the consolidation to make.
 12. `no evidence block this pass writes` — no appearance in a domain with a block.
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
PROPOSAL = DATA / "research" / "residents" / "grading_proposal.json"
MASTER = DATA / "research" / "residents" / "identity_master.json"
LEDGER = DATA / "research" / "residents" / "regrade_t0705.json"

sys.path.insert(0, str(ROOT / "tools"))
from mint_documented_residents import (  # noqa: E402  (shared, deliberately)
    FIRM, PAPERS, SCENE_DATE, UNCERTAIN, display, dumps, household_id, load,
    minted_by, plain_fragment, slug, surname, words,
)

PASS_NAME = "civic"
PREFIX = "hh_civic_"      # legacy shape only; T-0599 ids are plain and this never fires
DIVISION = "unplaced"
SCENE_YEAR = 1835

# The proposal's grades this pass writes. `not_1835_resident` and the abstention are
# refusal 1; `reconstructed` is not a grade any mint may assign (index.json keeps it at
# zero after the 2026-09-02 synthesis and this pass does not reopen it).
MINTABLE_GRADES = ("attested", "inferred")

LETTER_LIST_CLASS = "newspaper_letter_list"

# The 1832 muster, and the reading the project already committed to for it. Quoted from
# `data/research/civic/records/blackhawk_war_1832_chicago.json`'s own `the_ladder` field
# so the two cannot drift apart silently. See refusal 4.
MUSTER_CLASS = "muster_1832"
NO_DATE = "not read from this record"
MUSTER_LADDER = ("An 1832 enrollment is EARLIER evidence and never an 1835 residence on "
                 "its own: it places the man in this town in 1832, which is why it dates "
                 "and corroborates rather than mints")

# Which block each domain of the identity master writes to, and the words a note uses
# for it. `census_1840` is LATER evidence: it corroborates, it never carries a record on
# its own — see the docstring on the ticket's `census_evidence[] (1830)`.
BLOCKS = {
    "civic": ("civic_evidence", "the town's own civic lists"),
    "church": ("church_evidence", "the St Cyr register"),
    "newspapers": ("press_evidence", "the Chicago papers of 1833-1835"),
    "directories": ("book_evidence", "the printed directories"),
    "old_settlers": ("book_evidence", "the old settlers' death notices"),
    "census_1840": ("census_evidence", "the 1840 federal census of Cook County"),
}
BLOCK_KEYS = ("civic_evidence", "census_evidence", "church_evidence",
              "book_evidence", "press_evidence")

# The identity master names its census pages' source by the domain rather than by a
# source record — `read_census_1840`'s own fallback — and the newspapers reader hands
# every mention one domain label for two papers. Both are resolved here, because a
# person's `sources[]` has to name a file in data/sources/ or the validator fails it.
SOURCE_ALIAS = {"census_1840_cook_county": "census_1840_chicago_familysearch_images"}
NEWSPAPER_DOMAIN_SOURCE = "chicago_newspapers_1833_1835"

MONTHS = ("January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December")

YEAR = re.compile(r"(1[6-9]\d\d)")
ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


# ---------------------------------------------------------------------------
# dates: what a record says about WHEN, read as loosely as the sources write it
# ---------------------------------------------------------------------------

def year_of(value) -> int | None:
    m = YEAR.search(str(value or ""))
    return int(m.group(1)) if m else None


def bound_of(value) -> str | None:
    """The latest day a `describes_date` permits, as an ISO date, or None.

    A full date is its own bound. A bare year is bounded at the year's end and NOT at
    its start: the list says the man was there that year, not that he was there in
    January. Everything else the sources print — a death notice's `d. 14 Mar. 1861` —
    is read for its year and bounded the same way.
    """
    s = str(value or "").strip()
    if ISO.match(s):
        return s
    y = year_of(s)
    return f"{y}-12-31" if y else None


def in_window(app: dict) -> bool:
    """Does this appearance describe a date inside the scene year or before it?"""
    y = year_of(app.get("describes_date"))
    return y is not None and y <= SCENE_YEAR


def pretty(iso: str) -> str:
    m = ISO.match(iso or "")
    if not m:
        return iso
    return f"{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]} {m.group(1)}"


# ---------------------------------------------------------------------------
# the pool, and the refusals
# ---------------------------------------------------------------------------

def source_of(app: dict) -> str | None:
    """The source id an appearance cites, resolved to a file in data/sources/."""
    sid = app.get("source_id")
    if sid == NEWSPAPER_DOMAIN_SOURCE:
        loc = str(app.get("locator") or "")
        for prefix, paper in PAPERS:
            if loc.startswith(prefix):
                return paper
        return None
    return SOURCE_ALIAS.get(sid, sid)


def has_family_name(name: str) -> bool:
    """Is there a token here that could BE a family name? (the letter-list pass's rule 4)"""
    fam = surname(name)
    return bool(fam) and len(re.sub(r"[^a-z]", "", fam)) >= 3


def decide(row: dict, appearances: list, town_person_ids: set,
           excluded: set | None = None, own: set | None = None,
           taken_above: set | None = None) -> tuple[bool, str]:
    """The nine refusals, in order. Returns (accepted, reason) — reason is '' if minted.

    A pure function of its arguments so `--self-test` can fire every rule at a fixture
    instead of at the tree, which is what keeps the assertions meaningful when the
    corpus grows.
    """
    name = row.get("name") or ""
    if row.get("grade") not in MINTABLE_GRADES:
        return False, (f"the ladder does not reach this identity "
                       f"({row.get('rule')} → {row.get('grade')})")
    if row.get("canonical_person_id") and row["canonical_person_id"] not in (own or set()):
        return False, (f"the town already carries this person "
                       f"({row['canonical_person_id']})")
    if plain_fragment(name) in (excluded or set()):
        return False, (f"the town has researched this person and left them out "
                       f"({plain_fragment(name)})")
    scene_year = [a for a in appearances if in_window(a)]
    if scene_year and all(a.get("evidence_class") == MUSTER_CLASS for a in scene_year):
        return False, "an 1832 enrollment alone is earlier evidence and never mints"
    if scene_year and all(a.get("evidence_class") == LETTER_LIST_CLASS for a in scene_year):
        return False, "the post office's letter lists are the pass beside this one's pool"
    if FIRM.search(name):
        return False, "a firm, not a person"
    if UNCERTAIN.search(name):
        return False, "the transcription bracketed the name as uncertain"
    if not has_family_name(name):
        return False, "no name the corpus prints as a family name"
    if not scene_year:
        return False, "no appearance inside the scene year"
    if plain_fragment(name) in (taken_above or set()):
        return False, (f"the residency-tested pass above this one takes this person "
                       f"({plain_fragment(name)})")
    if plain_fragment(name) in town_person_ids:
        return False, (f"a duplicate of a person the town already carries "
                       f"({plain_fragment(name)})")
    if not any(a.get("domain") in BLOCKS for a in appearances):
        return False, "no evidence block this pass writes"
    return True, ""


# ---------------------------------------------------------------------------
# the record
# ---------------------------------------------------------------------------

def evidence_blocks(row: dict, appearances: list) -> tuple[dict, list]:
    """The per-domain evidence blocks, and the source ids they cite."""
    blocks: dict = {k: [] for k in BLOCK_KEYS}
    sources: list = []
    for app in sorted(appearances, key=lambda a: (str(a.get("describes_date") or ""),
                                                  str(a.get("record_id") or ""))):
        spec = BLOCKS.get(app.get("domain"))
        if not spec:
            continue
        sid = source_of(app)
        if not sid:
            continue
        key, _ = spec
        blocks[key].append({
            "list": app.get("evidence_class"),
            "as_read": app.get("as_read"),
            "locator": app.get("locator"),
            "record_id": app.get("record_id"),
            # Six old-settlers death notices carry no date the reader captured. The
            # absence is written down rather than left as an empty field: `bound_of`
            # reads no year out of it, so such a row can never become an arrival bound,
            # and the validator's own rule (an evidence row states its date) is met by
            # saying there is none rather than by leaving the key blank.
            "describes_date": app.get("describes_date") or NO_DATE,
            "source": sid,
            "rule": row.get("rule"),
        })
        if sid not in sources:
            sources.append(sid)
    return {k: v for k, v in blocks.items() if v}, sorted(sources)


def arrival_block(appearances: list, sources: list) -> dict:
    scene_year = [a for a in appearances if in_window(a)]
    dated = sorted(((b, str(a.get("record_id") or ""), a) for a in scene_year
                    if (b := bound_of(a.get("describes_date")))), key=lambda t: t[:2])
    value, _rid, app = dated[0]
    late = value > SCENE_DATE
    note = (f"A BOUND FROM THE RECORD, NOT AN ARRIVAL. {app.get('list') or app.get('evidence_class')} "
            f"names this person at Chicago by {pretty(value)} and nothing says when they came. ")
    if late:
        note += ("THE BOUND FALLS AFTER THE SCENE DATE and the record says so rather than "
                 "narrowing it: the earliest source that names this person is later than "
                 "1 July 1835, so they may have arrived after the day this scene models. "
                 "present_on_scene_date is `uncertain` for that reason.")
    else:
        note += ("The bound is at or before the scene date, so the person was at Chicago "
                 "by 1 July 1835 on this record's own evidence.")
    return {
        "value": value,
        "confidence": "inferred",
        "sources": sources,
        "note": note,
        "precision": "not_later_than",
    }


def presence_block(appearances: list, sources: list) -> dict:
    before = [a for a in appearances
              if (b := bound_of(a.get("describes_date"))) and b <= SCENE_DATE]
    after = [a for a in appearances
             if (b := bound_of(a.get("describes_date"))) and b >= SCENE_DATE]
    if before and after:
        return {
            "value": "present",
            "confidence": "inferred",
            "sources": sources,
            "note": ("THE RECORD BRACKETS THE DAY. This person is named at Chicago at or "
                     "before 1 July 1835 and named again at or after it, so the sources "
                     "reach across the scene date rather than stopping at one side of it. "
                     "Inferred, not documented: no source says where they were on the day."),
        }
    return {
        "value": "uncertain",
        "confidence": "inferred",
        "sources": sources,
        "note": ("THE RECORD DOES NOT REACH THE DAY. Every source that names this person "
                 "falls on one side of 1 July 1835, and nothing follows them to it or says "
                 "they left. `uncertain` rather than dropped — the distinction index.json "
                 "draws for Jeremiah Porter, and a finding, not a gap."),
    }


def unattested(note: str) -> dict:
    return {"value": None, "confidence": "reconstructed", "note": note}


def carry_over(doc: dict, prior: dict | None) -> dict:
    """Keep what ANOTHER pass wrote onto one of this pass's cards.

    A minted household is not this tool's private file once it is in the tree: the
    directory spend (T-0632) writes a `directories` block onto the card, the old-settlers
    roll writes a citation, the research passes write a `resident_research` block. This
    pass owns the keys it writes and re-derives them every run; everything else that is
    on the record is somebody else's finding and is preserved verbatim, at the end of the
    record and of the person, where a stable order keeps `--check` byte-identical.
    """
    if not prior or prior.get("source_pass") != PASS_NAME:
        return doc
    for key, value in prior.items():
        if key not in doc:
            doc[key] = value
    by_id = {p.get("id"): p for p in prior.get("persons") or []}
    for person in doc["persons"]:
        old = by_id.get(person["id"]) or {}
        for key, value in old.items():
            if key not in person:
                person[key] = value
        # Two keys this pass DOES write are also written to by other passes, and both
        # are additive there. `tools/old_settlers.py --apply-citations` puts the roll's
        # source on the person and APPENDS its sentence to the note, marker-guarded, and
        # its own gate then requires both to be on the record. So the union of the
        # sources is kept, and any tail another pass appended after this pass's own note
        # is kept with it — recognised as a tail precisely because this pass's note is
        # re-derived and is therefore the prefix it was appended to. If the derivation
        # ever changes the note out from under a tail, the prefix stops matching, the
        # tail is dropped, and that pass's own `--check` says so rather than the sentence
        # disappearing quietly.
        person["sources"] = sorted(set(person["sources"]) | set(old.get("sources") or []))
        was = (old.get("note") or "")
        if was.startswith(person["note"]) and len(was) > len(person["note"]):
            person["note"] = person["note"] + was[len(person["note"]):]
    return doc


def record(row: dict, appearances: list, docs: dict, taken_ids: set) -> dict:
    name = display(row.get("name") or "")
    hid = household_id(name, PREFIX, PASS_NAME, docs, taken_ids)
    pid = plain_fragment(name)
    n = 2
    while pid in taken_ids:
        pid, n = f"{plain_fragment(name)}_{n}", n + 1
    blocks, sources = evidence_blocks(row, appearances)
    lists = sorted({str(e["list"]) for rows in blocks.values() for e in rows})
    arrival = arrival_block(appearances, sources)
    person = {
        "id": pid,
        "name": name,
        "relationship": "head",
        "grade": row["grade"],
        # The manifest's own flag for which pass wrote this person, so a card and the
        # Evidence panel can hold the civic cohort apart from the letter-list one
        # without fetching a thousand records (the letter lists' `letter_list_only`
        # does the same job for the pass beside this one).
        "civic_mint": True,
        "ladder_rule": row.get("rule"),
        "occupation": {
            "value": "none_recorded",
            "confidence": "reconstructed",
            "note": ("No source in this pass's evidence records an occupation for this "
                     "person. A poll list, a tax list, a muster roll and a baptismal "
                     "entry each print a name and no trade, and where a later directory "
                     "prints one it is a trade of 1843 — T-0633 is the rule for "
                     "back-projecting that, and this pass does not have it."),
        },
        "sources": sources,
        "note": note_for(row, lists, arrival),
    }
    person.update(blocks)
    if row.get("resident_subtype"):
        person["resident_subtype"] = row["resident_subtype"]
    fam = surname(name).title() or name
    return {
        "id": hid,
        "name": f"The {fam} household — a name the town's own records carry",
        "division": DIVISION,
        "head": pid,
        "source_pass": PASS_NAME,
        "arrival": arrival,
        "party_size_on_arrival": unattested("Not attested."),
        "origin": unattested("Not attested."),
        "reason_for_coming": unattested("Not attested."),
        "lives_at": unattested(
            "Not attested: the lists that name this person give no address. The placement "
            "sweep assigns homes once the resident list is complete (T-0514, the owner's "
            "own sequencing) and this pass will not guess one."),
        "works_at": unattested(
            "Not attested. No trade is recorded here, so there is no premises to seek; "
            "T-0633 is where a later directory's address gets back-projected."),
        "present_on_scene_date": presence_block(appearances, sources),
        "persons": [person],
        "touches_removal": False,
        "review_required": False,
        "research_note": (
            "MINTED FROM THE CONSOLIDATED CIVIC, CHURCH, PRESS, BOOK AND CENSUS EVIDENCE "
            "(T-0513, T-0514). THE HOUSEHOLD IS A CONTAINER, NOT AN ARGUMENT: every other "
            "record here is written unattested in its own block, because the lists that "
            "name this person name a person and not a family. What is claimed is that the "
            "sources cited on the member below name them at Chicago, and the grade is the "
            "owner's ratified ladder applied by "
            "tools/consolidate_resident_evidence.py --build and spent by "
            "tools/mint_civic_residents.py, which prints every refusal. "
            "docs/LIBERTIES.md L215 carries the liberty and the tension with L213."),
    }


def note_for(row: dict, lists: list, arrival: dict) -> str:
    rung = {
        "G1a": "THE 1835 POLL LIST AND A SECOND INDEPENDENT SOURCE.",
        "G1b": "A CONTEMPORARY CHICAGO PAPER OF 1833-1835 PRINTS THIS PERSON BY NAME IN THE TOWN.",
        "G2a": "THE 1835 POLL LIST ALONE.",
        "G2b": "AN 1833 OR 1834 LIST — POLL, TAX OR MUSTER — WITH ANOTHER SOURCE.",
        "G2c": "THE ST CYR REGISTER OF 1833-1835 NAMES THIS PERSON IN THE PARISH.",
        "G2d": "HUBBARD, FERGUS OR NORRIS NAMES THIS PERSON WITH A TRADE OR AN ADDRESS.",
        "G2e": "A CHICAGO POST-OFFICE LETTER LIST OF 1833-1835 AND NOTHING STRONGER.",
        "G3": "A SINGLE APPEARANCE AND NOTHING ELSE.",
        "G4": "TWO OR MORE APPEARANCES, NONE OF A CLASS A HIGHER RUNG ACCEPTS.",
    }.get(row.get("rule"), "THE LADDER'S OWN READING OF THIS EVIDENCE.")
    head = ""
    if row.get("resident_subtype") == "projected_resident":
        head = ("PROJECTED RESIDENT. Documented once and corroborated by nothing else, so "
                "the weakest rung of `inferred` the owner's ladder defines. ")
    return (
        f"{head}{rung} Read from {', '.join(lists)}. "
        f"THE GRADE IS THE OWNER'S RATIFIED LADDER OF 2026-09-03 ({row.get('rule')}), applied "
        f"to every identity at once by tools/consolidate_resident_evidence.py and spent onto "
        f"this card by tools/mint_civic_residents.py; the evidence blocks below carry the "
        f"reading AS READ, its locator and the record it came from, so the page can be gone "
        f"back to. WHAT IS RECONSTRUCTED: everything except the person and the sources — no "
        f"dwelling, no trade, no origin, no family, no party. {arrival['note']} "
        f"No figure is drawn (L1)."
    )


# ---------------------------------------------------------------------------
# the build
# ---------------------------------------------------------------------------

def town_person_ids(docs: dict) -> set:
    return {p.get("id") for doc in docs.values() for p in doc.get("persons") or []}


def excluded_ids(index: dict) -> set:
    """The people this project researched and left OUT of the scene, by id and by name.

    index.json's `researched_not_resident` is the exclusions-style half of the dataset
    and adding to it is preferred to deleting from it. A mint that seated one of them
    would reverse an argued finding by accident. Refusal 3.
    """
    out: set = set()
    for entry in index.get("researched_not_resident") or []:
        if entry.get("id"):
            out.add(entry["id"])
        if entry.get("name"):
            out.add(plain_fragment(entry["name"]))
    return out


def placed_takes(docs: dict, index: dict) -> set:
    """The people `mint_placed_residents.py` mints, asked of the pass itself.

    Refusal 10. Asked rather than hard-coded because the answer moves with the register,
    and a list copied into this file would be a precedence rule that silently stopped
    being one. The town it is asked about is the town WITHOUT this pass's own output, so
    the question is the precedence question — who would take this person if this pass did
    not exist — and not a reading of what this pass has already done.
    """
    import mint_placed_residents as placed
    accepted = placed.mint(docs, index)[0]
    return {plain_fragment(display(cand["name"])) for cand in
            (a[0] if isinstance(a, tuple) else a for a in accepted)}


def pool(docs: dict, proposal: dict, master: dict, index: dict, own: set):
    """Every identity the proposal offers, put through `decide()` in a stable order.

    WHY THE POOL READS ITS OWN ANSWER BACK, and it is the same reason the three passes
    beside this one do. `grading_proposal.json` is compiled FROM the committed town, so
    the moment this pass seats somebody the consolidation starts resolving that identity
    onto the card it just wrote and hands back a `canonical_person_id` for them. Read
    naively, refusal 2 would then fire on every person this pass has ever minted and the
    next `--build` would delete all of them. A canonical id that points at one of THIS
    pass's own people is read as what it is — this pass's previous answer — so the
    derivation still holds the run after it lands.

    `town_layer` appearances are dropped for the same reason and a second one: the
    consolidation's own reader says that layer is "not a source — it is what the sources
    are spent onto", so letting it into the refusals would mean an identity that rests on
    the 1832 muster alone stops resting on the muster alone the moment this pass declines
    it and something else seats them.
    """
    apps = {i["id"]: [a for a in (i.get("appearances") or [])
                      if a.get("domain") != "town_layer"]
            for i in master.get("identities", [])}
    known = town_person_ids(docs)
    excluded = excluded_ids(index)
    above = placed_takes(docs, index)
    accepted, refusals = [], []
    for row in sorted(proposal.get("proposals", []), key=lambda r: r["identity"]):
        appearances = apps.get(row["identity"], [])
        ok, reason = decide(row, appearances, known, excluded, own, above)
        if ok:
            accepted.append((row, appearances))
        else:
            refusals.append((row, reason))
    return accepted, refusals


def build(preload: dict | None = None):
    docs = ({p: json.loads(t) for p, t in preload.items() if p != INDEX}
            if preload is not None
            else {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))})
    index = (json.loads(preload[INDEX]) if preload is not None and INDEX in preload
             else load(INDEX))
    proposal, master = load(PROPOSAL), load(MASTER)

    mine_paths = {p for p, doc in docs.items() if minted_by(p, doc, PASS_NAME, PREFIX)}
    # This pass must not read its OWN output back as "the town already carries this
    # person" — refusal 2 and refusal 8 would both fire on the second run and delete
    # every household the first one seated. See mint_documented_residents.MINTED_PREFIXES.
    others = {p: d for p, d in docs.items() if p not in mine_paths}
    own = {person.get("id") for path in mine_paths
           for person in docs[path].get("persons") or []}
    accepted, refusals = pool(others, proposal, master, index, own)

    files, rows = {}, []
    taken: set = set()
    for row, appearances in accepted:
        doc = record(row, appearances, others, taken)
        doc = carry_over(doc, docs.get(HOUSEHOLDS / f"{doc['id']}.json"))
        if doc["id"] in taken:
            raise SystemExit(f"two identities mint the same household id {doc['id']}")
        taken.add(doc["id"])
        taken.add(doc["persons"][0]["id"])
        files[HOUSEHOLDS / f"{doc['id']}.json"] = dumps(doc, 1)
        tally: dict = {}
        for person in doc["persons"]:
            tally[person["grade"]] = tally.get(person["grade"], 0) + 1
        rows.append({
            "id": doc["id"],
            "file": f"households/{doc['id']}.json",
            "civic_mint": True,
            "head": doc["head"],
            "division": doc["division"],
            "persons": len(doc["persons"]),
            "grades": dict(sorted(tally.items())),
            "lives_at": doc["lives_at"]["value"],
            "works_at": doc["works_at"]["value"],
            "present_on_scene_date": doc["present_on_scene_date"]["value"],
            "review_required": doc["review_required"],
            "projected_resident": any(p.get("resident_subtype") == "projected_resident"
                                      for p in doc["persons"]),
        })

    mine_ids = {p.stem for p in mine_paths}
    keep = [r for r in index["households"] if r["id"] not in mine_ids]
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

    final = dict(others)
    final.update({path: json.loads(text) for path, text in files.items()})
    index["counts"]["civic_mint"] = sum(
        1 for doc in final.values() for person in doc.get("persons") or []
        if person.get("civic_mint"))
    index["counts"]["projected_residents"] = sum(
        1 for doc in final.values() for person in doc.get("persons") or []
        if person.get("resident_subtype") == "projected_resident")
    files[INDEX] = dumps(index, 1)
    return files, accepted, refusals, mine_paths


# ---------------------------------------------------------------------------
# reports
# ---------------------------------------------------------------------------

def reason_key(reason: str) -> str:
    return reason.split(" (")[0]


def report(accepted, refusals) -> None:
    print(f"MINTED — {len(accepted)} civic/church/press/book resident(s)")
    by_rule: dict = {}
    by_grade: dict = {}
    for row, _apps in accepted:
        by_rule[row["rule"]] = by_rule.get(row["rule"], 0) + 1
        key = (row["grade"], row.get("resident_subtype") or "-")
        by_grade[key] = by_grade.get(key, 0) + 1
    for (grade, sub), n in sorted(by_grade.items()):
        print(f"  {n:5d}  {grade} / {sub}")
    for rule, n in sorted(by_rule.items()):
        print(f"  {n:5d}  {rule}")
    print(f"\nREFUSED — {len(refusals)} identity/identities out of the same pool, with the reason")
    tally: dict = {}
    for _row, reason in refusals:
        tally[reason_key(reason)] = tally.get(reason_key(reason), 0) + 1
    for reason, n in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"  {n:5d}  {reason}")
    print()
    for row, _apps in accepted:
        print(f"  MINT   {row['identity'][:44]:46s} {row['rule']:4s} {row['grade']}")
    for row, reason in refusals:
        print(f"  REFUSE {row['identity'][:44]:46s} {reason}")


def scale_report() -> None:
    """What this pass is worth to the town, re-derived rather than remembered."""
    docs = {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))}
    mine = {p: d for p, d in docs.items() if minted_by(p, d, PASS_NAME, PREFIX)}
    persons = sum(len(d.get("persons") or []) for d in docs.values())
    ours = sum(len(d.get("persons") or []) for d in mine.values())
    grades: dict = {}
    domains: dict = {}
    for d in mine.values():
        for p in d.get("persons") or []:
            grades[p["grade"]] = grades.get(p["grade"], 0) + 1
            for key in BLOCK_KEYS:
                if p.get(key):
                    domains[key] = domains.get(key, 0) + 1
    print(f"{len(docs)} household(s), {persons} person(s) in the town")
    print(f"{len(mine)} household(s), {ours} person(s) from this pass "
          f"({(100.0 * ours / persons if persons else 0):.1f}% of the town)")
    for grade, n in sorted(grades.items()):
        print(f"  {n:5d}  {grade}")
    for key, n in sorted(domains.items()):
        print(f"  {n:5d}  carry {key}")


# ---------------------------------------------------------------------------
# the gate — the invariants this pass owes, proved on whatever tree it is run on
# ---------------------------------------------------------------------------

def gate_problems(docs: dict, index: dict) -> list:
    problems = []
    rows = {r["id"]: r for r in index.get("households") or []}
    mine = {p: d for p, d in docs.items() if minted_by(p, d, PASS_NAME, PREFIX)}
    for path, doc in sorted(mine.items()):
        where = doc.get("id") or path.stem
        people = doc.get("persons") or []
        if len(people) != 1:
            problems.append(f"{where}: {len(people)} member(s); this pass mints households "
                            f"of one and never invents a family")
        for p in people:
            if not p.get("civic_mint"):
                problems.append(f"{where}/{p.get('id')}: lost civic_mint, the flag that keeps "
                                f"this cohort's evidence strength legible")
            if not any(p.get(k) for k in BLOCK_KEYS):
                problems.append(f"{where}/{p.get('id')}: carries no evidence block; a person "
                                f"minted here is minted FROM a reading and must show it")
            if p.get("occupation", {}).get("value") != "none_recorded":
                problems.append(f"{where}/{p.get('id')}: gained a trade; no source in this "
                                f"pass records one")
            if p.get("grade") not in MINTABLE_GRADES:
                problems.append(f"{where}/{p.get('id')}: grade {p.get('grade')!r} is not one "
                                f"this pass may assign")
            if not p.get("sources"):
                problems.append(f"{where}/{p.get('id')}: cites no source")
            for key in BLOCK_KEYS:
                for e in p.get(key) or []:
                    if not e.get("as_read") or not e.get("rule"):
                        problems.append(f"{where}/{p.get('id')}: an evidence row without a "
                                        f"reading or the rule that fired it")
            classes = {e.get("list") for k in BLOCK_KEYS for e in p.get(k) or []}
            if classes and classes <= {LETTER_LIST_CLASS}:
                problems.append(f"{where}/{p.get('id')}: rests on a letter list alone, which "
                                f"is the pass beside this one's pool")
            if classes and classes <= {MUSTER_CLASS}:
                problems.append(f"{where}/{p.get('id')}: rests on the 1832 muster alone, and "
                                f"an 1832 enrollment dates a man rather than minting him")
        for key in ("lives_at", "works_at"):
            if (doc.get(key) or {}).get("value"):
                problems.append(f"{where}: gained a {key}; the placement sweep does that, "
                                f"once the resident list is complete")
        arr = doc.get("arrival") or {}
        if arr.get("precision") != "not_later_than":
            problems.append(f"{where}: arrival precision {arr.get('precision')!r}; every "
                            f"arrival this pass writes is a BOUND and says so")
        if (doc.get("present_on_scene_date") or {}).get("value") == "present" \
                and not (doc.get("present_on_scene_date") or {}).get("note"):
            problems.append(f"{where}: present_on_scene_date without its reasoning")
        row = rows.get(where)
        if row is None:
            problems.append(f"{where}: minted here and absent from the manifest")
        elif not row.get("civic_mint"):
            problems.append(f"{where}: the manifest row does not carry civic_mint")
    counted = (index.get("counts") or {}).get("civic_mint")
    actual = sum(1 for d in mine.values() for p in d.get("persons") or []
                 if p.get("civic_mint"))
    if counted != actual:
        problems.append(f"counts.civic_mint is {counted!r} and the tree holds {actual}")
    return problems


def read_tree():
    docs = {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))}
    return docs, load(INDEX)


def gate() -> int:
    docs, index = read_tree()
    problems = gate_problems(docs, index)
    for p in problems:
        print(f"   {p}")
    if problems:
        print(f"   {len(problems)} problem(s)")
        return 1
    mine = sum(1 for p, d in docs.items() if minted_by(p, d, PASS_NAME, PREFIX))
    print(f"   OK: {mine} civic-minted household(s) claim a person, a reading and no more")
    return 0


# ---------------------------------------------------------------------------
# the assertions, broken on purpose
# ---------------------------------------------------------------------------

def _row(**kw):
    base = {"identity": "id_fixture", "name": "Ezra Fixture", "canonical_person_id": None,
            "rule": "G1a", "grade": "attested", "resident_subtype": None,
            "evidence": [], "evidence_classes": []}
    base.update(kw)
    return base


def _app(**kw):
    base = {"domain": "civic", "record_id": "poll_1835_999",
            "source_id": "chicago_voter_lists_1833_1835_irad", "as_read": "E. Fixture",
            "normalized": "Ezra Fixture", "locator": "poll_1835",
            "describes_date": "1835", "evidence_class": "poll_1835"}
    base.update(kw)
    return base


REFUSAL_CASES = (
    ("a mint the ladder does not reach",
     _row(grade="not_1835_resident", rule="G0"), [_app()], set(),
     "the ladder does not reach"),
    ("a person the town already carries",
     _row(canonical_person_id="fixture_ezra"), [_app()], set(),
     "the town already carries"),
    ("a later-only source used as a residency source",
     _row(rule="G3", grade="inferred"),
     [_app(domain="directories", source_id="fergus_chicago_directory_1843",
           locator="South Water", describes_date="1843", evidence_class="directory_1843")],
     set(), "no appearance inside the scene year"),
    ("a letter list as the only scene-year source",
     _row(rule="G2e", grade="inferred"),
     [_app(domain="newspapers", source_id="chicago_newspapers_1833_1835",
           locator="chicago_democrat_1834_07_02#c032", describes_date="1834-07-02",
           evidence_class="newspaper_letter_list")],
     set(), "the pass beside this one's pool"),
    ("a duplicate of an existing person",
     _row(), [_app()], {"fixture_ezra"}, "a duplicate of a person the town already carries"),
    ("an 1832 enrollment and nothing else",
     _row(rule="G3", grade="inferred"),
     [_app(source_id="blackhawk_war_chicago_enrollments_isa", locator="muster",
           describes_date="1832", evidence_class="muster_1832")],
     set(), "an 1832 enrollment alone"),
    ("a firm, not a person",
     _row(name="Fixture & Co"), [_app()], set(), "a firm, not a person"),
    ("a bracketed transcription",
     _row(name="Ezra [Fixture]"), [_app()], set(), "bracketed the name as uncertain"),
    ("a name with nothing that could be a surname",
     _row(name="E. S."), [_app()], set(), "no name the corpus prints as a family name"),
    ("a mint with no evidence block",
     _row(rule="G3", grade="inferred"),
     [_app(domain="town_layer", evidence_class="town_layer")], set(),
     "no evidence block this pass writes"),
)


def self_test() -> int:
    failed = 0
    for label, row, apps, known, want in REFUSAL_CASES:
        ok, reason = decide(row, apps, known, set(), set(), set())
        if ok or want not in reason:
            failed += 1
            print(f"   FAIL {label}: accepted={ok} reason={reason!r}, wanted {want!r}")
    ok, reason = decide(_row(), [_app()], set(), set(), set(), set())
    if not ok:
        failed += 1
        print(f"   FAIL the control case is refused: {reason!r}")
    ok, reason = decide(_row(), [_app()], set(), set(), set(), {"fixture_ezra"})
    if ok or "the residency-tested pass above this one" not in reason:
        failed += 1
        print(f"   FAIL this pass does not give way to the pass above it: {reason!r}")
    ok, reason = decide(_row(canonical_person_id="fixture_ezra"), [_app()], set(), set(),
                        {"fixture_ezra"})
    if not ok:
        failed += 1
        print(f"   FAIL this pass refuses its OWN previous answer read back: {reason!r}")
    ok, reason = decide(_row(), [_app()], set(), {"fixture_ezra"}, set(), set())
    if ok or "researched this person and left them out" not in reason:
        failed += 1
        print(f"   FAIL a researched-and-excluded person is minted: {reason!r}")
    if MUSTER_LADDER not in json.dumps(
            load(DATA / "research" / "civic" / "records"
                 / "blackhawk_war_1832_chicago.json").get("the_ladder", "")):
        failed += 1
        print("   FAIL the muster's own ladder line has moved; refusal 4 quotes a "
              "sentence the record no longer makes")

    # the record itself, on the control fixture: the shape the gate then polices
    doc = record(_row(), [_app()], {}, set())
    person = doc["persons"][0]
    for label, cond in (
            ("the person carries the civic_mint flag", person.get("civic_mint")),
            ("the person carries an evidence block", person.get("civic_evidence")),
            ("the evidence row carries the rule that fired", 
             (person.get("civic_evidence") or [{}])[0].get("rule") == "G1a"),
            ("the arrival is a bound", doc["arrival"]["precision"] == "not_later_than"),
            ("the arrival bound is the year's end, not its start",
             doc["arrival"]["value"] == "1835-12-31"),
            ("a bound after the scene date leaves presence uncertain",
             doc["present_on_scene_date"]["value"] == "uncertain"),
            ("no dwelling is dealt", doc["lives_at"]["value"] is None),
            ("no trade is read in", person["occupation"]["value"] == "none_recorded"),
            ("the source resolves to a file, not a domain label",
             person["sources"] == ["chicago_voter_lists_1833_1835_irad"]),
    ):
        if not cond:
            failed += 1
            print(f"   FAIL {label}")

    # a foreign block on one of this pass's cards survives a re-derivation
    base = record(_row(), [_app()], {}, set())
    prior = json.loads(json.dumps(base))
    prior["directories"] = {"note": "written by another pass"}
    prior["persons"][0]["resident_research"] = {"ticket": "T-0485"}
    kept = carry_over(record(_row(), [_app()], {}, set()), prior)
    prior["persons"][0]["sources"] = (prior["persons"][0]["sources"]
                                      + ["chicago_tribune_1882_04_25_old_settler_deaths"])
    prior["persons"][0]["note"] = prior["persons"][0]["note"] + " THE ROLL IS WORTH THIS."
    kept = carry_over(record(_row(), [_app()], {}, set()), prior)
    if kept.get("directories") != {"note": "written by another pass"} \
            or kept["persons"][0].get("resident_research") != {"ticket": "T-0485"}:
        failed += 1
        print("   FAIL another pass's findings do not survive a re-derivation")
    if "chicago_tribune_1882_04_25_old_settler_deaths" not in kept["persons"][0]["sources"] \
            or not kept["persons"][0]["note"].endswith("THE ROLL IS WORTH THIS."):
        failed += 1
        print("   FAIL a citation another pass wrote onto the card does not survive")
    if carry_over(record(_row(), [_app()], {}, set()),
                  dict(prior, source_pass="letter_list")).get("directories"):
        failed += 1
        print("   FAIL carry_over took a record that is not this pass's")

    # the two source labels the identity master hands over unresolved
    if source_of(_app(domain="newspapers", source_id="chicago_newspapers_1833_1835",
                      locator="chicago_democrat_1835_02_11#c003")) \
            != "chicago_democrat_1833_1835":
        failed += 1
        print("   FAIL a Democrat mention does not resolve to the Democrat")
    if source_of(_app(domain="census_1840", source_id="census_1840_cook_county")) \
            != "census_1840_chicago_familysearch_images":
        failed += 1
        print("   FAIL the census domain label does not resolve to a committed source")

    # and the gate's own assertions, broken on a copy of the committed tree
    docs, index = read_tree()
    if gate_problems(docs, index):
        print("   the committed tree does not pass its own gate; fix that first")
        return 1
    mine = [p for p, d in docs.items() if minted_by(p, d, PASS_NAME, PREFIX)]
    if mine:
        victim = sorted(mine)[0]

        def broken(mutate):
            d = {pathlib.Path(k): v for k, v in
                 json.loads(json.dumps({str(k): v for k, v in docs.items()})).items()}
            i = json.loads(json.dumps(index))
            mutate(d, i)
            return gate_problems(d, i)

        cases = [
            ("a person loses its evidence blocks",
             lambda d, i: [d[victim]["persons"][0].pop(k)
                           for k in BLOCK_KEYS if k in d[victim]["persons"][0]],
             "no evidence block"),
            ("a person loses the civic_mint flag",
             lambda d, i: d[victim]["persons"][0].pop("civic_mint"), "civic_mint"),
            ("a household gains a roof",
             lambda d, i: d[victim]["lives_at"].update(value="sauganash_hotel"), "lives_at"),
            ("a person gains a trade",
             lambda d, i: d[victim]["persons"][0]["occupation"].update(value="carpenter"),
             "gained a trade"),
            ("a household gains an invented wife",
             lambda d, i: d[victim]["persons"].append(
                 dict(d[victim]["persons"][0], id="invented_wife")), "member(s)"),
            ("the arrival stops being a bound",
             lambda d, i: d[victim]["arrival"].update(precision="year"), "arrival precision"),
            ("the manifest row loses the flag",
             lambda d, i: [r.pop("civic_mint") for r in i["households"]
                           if r["id"] == d[victim]["id"]], "civic_mint"),
        ]
        for label, mutate, want in cases:
            found = broken(mutate)
            if not any(want in p for p in found):
                failed += 1
                print(f"   FAIL {label}: the gate did not name it ({found[:2]})")
    if failed:
        print(f"   {failed} assertion(s) failed")
        return 1
    print(f"   OK: {len(REFUSAL_CASES)} refusals, the record's own shape and the gate's "
          f"assertions all fire")
    return 0


# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# --regrade: the ladder's verdict on the people the town ALREADY carries
# ---------------------------------------------------------------------------
#
# T-0705, the first half of T-0515. `--build` above SEATS people the town does not
# hold. This mode writes nothing new: it takes `grading_proposal.json`'s
# `changes_to_existing_people` — 158 rows where the ratified ladder disagrees with the
# grade a committed card carries — and applies the ones the evidence rows support.
#
# WHY IT IS A SEPARATE MODE AND NOT PART OF THE BUILD. `--build` derives WHOLE cards
# from the proposal and rewrites them; the people here are somebody else's cards, most
# of them the letter-list mint's, and this pass may only reach into two fields of them
# plus the evidence it can cite. Keeping the two apart is what lets `--check` above go
# on proving the mint byte for byte while this pass edits records it does not own.
#
# THE FOUR REFUSALS, AND WHY EACH IS A REFUSAL RATHER THAN A GRADE. The ticket's own
# rule is that nothing may be graded DOWN without a refusal recorded on the person, and
# the same discipline is applied upward: a proposal this pass declines is written onto
# the card as a refusal with its reason, so the next reader sees the argument and not a
# silence. Measured on dev at the claim: 36 R1, 20 R2, 43 R3, 3 R4, 56 applied.

REGRADE_TICKET = "T-0705"
REGRADE_LADDER_RATIFIED = "2026-09-03"

# The run date, written as a constant rather than read from the clock. `--regrade
# --check` re-applies the whole pass to the committed tree and diffs it, so a
# `date.today()` here would turn the gate red at midnight for no change in the data.
REGRADE_ON = "2026-09-04"

# The consolidation's own reader says this layer "is not a source — it is what the
# sources are spent onto", so it never counts toward corroboration.
NOT_A_SOURCE = "town_layer"

LETTER_LIST_CLASSES = {LETTER_LIST_CLASS}

# The passes that re-derive a person's whole card byte for byte. A regrade written on
# top of one of them is reverted by its next `--build`, silently, so it is refused here
# and named instead. Asked of the record rather than hard-coded per person.
DERIVED_BY = {
    "civic": "tools/mint_civic_residents.py --build",
    "placed": "tools/mint_placed_residents.py --build",
    "documented": "tools/mint_documented_residents.py --build",
}

REGRADE_MARK = "REGRADED ON THE RATIFIED LADDER"
REGRADE_SENTINEL = " — THE RECORD BELOW WAS WRITTEN BEFORE THAT RULING. "

GRADE_ORDER = {"attested": 2, "inferred": 1}

# The bucket headings the report groups by. Each person still carries their OWN sentence
# on their own card and in the row beneath the heading — these say what the rule is, not
# what it found on any one of them.
REFUSAL_HEADLINE = {
    "R0": "the town no longer carries the person the proposal names",
    "R1": "the ladder abstains (G5) and an abstention is not a verdict",
    "R2": "the proposal leaves `projected_resident` on the post office alone",
    "R3": "the demotion is blind to a source the card cites and the ladder does not read",
    "R4": "another pass re-derives the whole card and would revert the grade",
}


def strip_regrade(note: str) -> str:
    """Drop a prefix a previous run of this pass wrote, so re-applying is idempotent."""
    text = note or ""
    if text.startswith(REGRADE_MARK) and REGRADE_SENTINEL in text:
        return text.split(REGRADE_SENTINEL, 1)[1]
    return text


def covered_sources(master: dict) -> set:
    """Every source id the consolidation's seven domains can actually cite.

    This is the boundary R3 is drawn on. The ladder was compiled from these domains and
    from nothing else, so a card citing a source outside them rests on ground the
    proposal never weighed — which is the very argument rule G5 makes when it abstains,
    asked one rung lower.
    """
    out: set = set()
    for identity in master.get("identities", []):
        for app in identity.get("appearances") or []:
            if app.get("domain") == NOT_A_SOURCE:
                continue
            sid = source_of(app)
            if sid:
                out.add(sid)
    return out


def lowers(change: dict) -> bool:
    """Is this proposal a demotion — a grade down, or a plain person made projected."""
    before, after = change["from"], change["to"]
    if GRADE_ORDER.get(after.get("grade"), 0) < GRADE_ORDER.get(before.get("grade"), 0):
        return True
    return (before.get("resident_subtype") is None
            and after.get("resident_subtype") == "projected_resident")


def regrade_decide(change: dict, row: dict, doc: dict, person: dict,
                   covered: set) -> tuple[str | None, str]:
    """(refusal id, sentence) — the id is None when the proposal is applied."""
    pid = change["person_id"]

    pass_name = str(doc.get("source_pass") or "")
    if pass_name in DERIVED_BY:
        return "R4", (
            f"the card is re-derived byte for byte by `{DERIVED_BY[pass_name]}`, so a grade "
            f"written here would be reverted by that pass's next build without anyone being "
            f"told. The change belongs in the pass that owns the card and is refused rather "
            f"than written and lost.")

    if change["to"].get("grade") is None:
        return "R1", (
            "the ladder ABSTAINS (rule G5): every appearance this consolidation can see "
            "describes a date after the scene year, and the card rests on sources outside "
            "the seven domains it reads. G5 exists to decline to demote such a person on "
            "later evidence, and a pass that read the abstention as a verdict would be "
            "doing the one thing the rule forbids.")

    classes = {c for c in (row.get("evidence_classes") or []) if c != NOT_A_SOURCE}
    drops_projected = (change["from"].get("resident_subtype") == "projected_resident"
                       and change["to"].get("resident_subtype") is None)
    if drops_projected and classes <= LETTER_LIST_CLASSES:
        return "R2", (
            "the proposal lifts this person out of `projected_resident` on the post office "
            "alone — every evidence class behind it is a Chicago letter list. T-0515's "
            "reading of the owner's tiers binds: a letter-list name leaves "
            "`projected_resident` when something OTHER than a letter list names them, and "
            "nothing here does. The evidence rows do not support the proposal.")

    if lowers(change):
        outside = [s for s in (person.get("sources") or []) if s not in covered]
        if outside:
            return "R3", (
                "the demotion is blind: this card cites "
                + ", ".join(f"`{s}`" for s in sorted(outside))
                + ", which the consolidation's seven domains do not read, so the proposal "
                  "cannot be the whole account of what the grade rests on. Refused on the "
                  "same argument G5 makes, one rung lower.")

    return None, ""


def transition_says(change: dict, row: dict, appearances: list) -> str:
    """Why the CHANGE follows, in the ladder's own terms — not just which rule fired.

    Quoting the rule alone reads wrong on a subtype move: G2e's words are about
    declining `attested`, and a card that only quoted them would leave a reader asking
    what any of it had to do with the mark coming off. So the move itself is stated,
    and it is stated from the evidence rows rather than asserted.
    """
    classes = sorted({c for c in (row.get("evidence_classes") or []) if c != NOT_A_SOURCE})
    named = ", ".join(f"`{c}`" for c in classes) or "no class the consolidation reads"
    n = len(appearances)
    before, after = change["from"], change["to"]
    if before.get("resident_subtype") == "projected_resident" and not after.get("resident_subtype"):
        return (f"`projected_resident` is the ladder's mark for a single appearance and "
                f"nothing else (G3). This person stands in {n} appearance(s) across "
                f"{len(classes)} evidence class(es) — {named} — so the mark comes off and "
                f"the grade stands where it was.")
    if not before.get("resident_subtype") and after.get("resident_subtype") == "projected_resident":
        return (f"the card is put back to `projected_resident`: {n} appearance(s) across "
                f"{named}, which is the weakest reading the ladder accepts for a resident.")
    if GRADE_ORDER.get(after.get("grade"), 0) > GRADE_ORDER.get(before.get("grade"), 0):
        return (f"the rung above is reached on {n} appearance(s) across {named}.")
    return (f"the higher grade is not reached on what this card cites: {n} appearance(s) "
            f"across {named}.")


def regrade_ledger(docs: dict, index: dict) -> list:
    """THE RULING OF THE DAY, compiled once from the proposal and then committed.

    WHY THIS IS A FILE AND NOT A DERIVATION RE-RUN EVERY TIME. `grading_proposal.json`
    is compiled FROM the committed town, and `changes_to_existing_people` is by
    definition the rows where the proposal and a card DISAGREE. The moment this pass
    writes a card the disagreement is gone, the row leaves the proposal, and a pass that
    recomputed its decisions from the proposal would find nothing to do and no longer be
    able to say what it had done. `--build` above has the same shape of problem and
    solves it by reading its own answer back; this pass cannot, because the evidence for
    a decision is the disagreement itself.

    So the ruling is compiled ONCE, with `--regrade --ledger`, and committed. It carries
    everything a decision rests on — the rule, the ladder's words, the move, the refusal
    and the evidence rows read on the day — so applying it is a pure function of the
    file and stays true when the sources under it are re-read. That is what a ruling is:
    a record of what was decided on what was known, not a thing recomputed forever.
    """
    proposal, master = load(PROPOSAL), load(MASTER)
    ladder = proposal.get("ladder") or {}
    rows = {}
    for row in proposal.get("proposals", []):
        row = dict(row)
        row["_ladder_says"] = (ladder.get(row.get("rule")) or {}).get("says") or ""
        rows[row["identity"]] = row
    apps = {i["id"]: [a for a in (i.get("appearances") or [])
                      if a.get("domain") != NOT_A_SOURCE]
            for i in master.get("identities", [])}
    covered = covered_sources(master)

    seats: dict = {}
    for doc in docs.values():
        for person in doc.get("persons") or []:
            if person.get("id"):
                seats[person["id"]] = (doc, person)

    out = []
    for change in sorted(proposal.get("changes_to_existing_people") or [],
                         key=lambda c: c["person_id"]):
        row = rows.get(change["identity"], {"rule": change["rule"], "_ladder_says": ""})
        appearances = apps.get(change["identity"], [])
        seat = seats.get(change["person_id"])
        entry = {
            "person_id": change["person_id"],
            "identity": change["identity"],
            "rule": change["rule"],
            "ladder_says": row.get("_ladder_says") or "",
            "from": change["from"],
            "to": change["to"],
            "lowers": lowers(change),
        }
        if seat is None:
            entry["decision"] = "R0"
            entry["refusal_says"] = "the town no longer carries this person id"
            out.append(entry)
            continue
        doc, person = seat
        rid, why = regrade_decide(change, row, doc, person, covered)
        entry["decision"] = rid or "applied"
        if rid:
            entry["refusal_says"] = why
            out.append(entry)
            continue
        blocks, cited = evidence_blocks(row, appearances)
        entry["moved"] = transition_says(change, row, appearances)
        entry["evidence"] = blocks
        entry["sources"] = cited
        if entry["lowers"]:
            entry["refusal_says"] = (
                f"the grade `{change['from'].get('grade')}` is REFUSED on the ratified "
                f"ladder: {entry['ladder_says'] or 'rule ' + change['rule']} Every source "
                f"this card cites is one the consolidation reads, so there is no evidence "
                f"outside the ladder's seven domains for the higher grade to rest on.")
        out.append(entry)
    return out


def regrade_person(person: dict, entry: dict) -> dict:
    """The person as this pass leaves them. Pure: same ledger row, same bytes, always."""
    out = dict(person)
    research = dict(out.get("resident_research") or {})
    rule = entry["rule"]
    says = (entry.get("ladder_says") or "").strip()
    before = f"{entry['from'].get('grade')}"
    if entry["from"].get("resident_subtype"):
        before += f"/{entry['from']['resident_subtype']}"
    after = f"{entry['to'].get('grade')}"
    if entry["to"].get("resident_subtype"):
        after += f"/{entry['to']['resident_subtype']}"

    refusals = [r for r in (research.get("refusals") or [])
                if r.get("ticket") != REGRADE_TICKET]
    refused = entry["decision"] != "applied"

    if refused or entry.get("refusal_says"):
        refusals.append({
            "ticket": REGRADE_TICKET,
            "refused_on": REGRADE_ON,
            # A refusal of the PROPOSAL carries its rule id; a demotion that was applied
            # carries D1, the refusal of the grade the card used to claim. The ticket's
            # rule is that no grade is lowered without one, so it is written here on the
            # person who was lowered rather than only in a report.
            "refusal": entry["decision"] if refused else "D1",
            "proposal": f"{before} -> {after}",
            "rule": rule,
            "refusal_says": entry["refusal_says"],
        })
    if refusals:
        research["refusals"] = refusals
    if refused:
        out["resident_research"] = research
        return out

    for key in BLOCK_KEYS:
        if entry.get("evidence", {}).get(key):
            out[key] = entry["evidence"][key]
    out["sources"] = list(dict.fromkeys(list(out.get("sources") or [])
                                        + list(entry.get("sources") or [])))

    out["grade"] = entry["to"]["grade"]
    if entry["to"].get("resident_subtype"):
        out["resident_subtype"] = entry["to"]["resident_subtype"]
    else:
        out.pop("resident_subtype", None)

    research["regraded_on"] = REGRADE_ON
    research["regrade_ticket"] = REGRADE_TICKET
    research["rule"] = f"{rule} — {says}" if says else rule
    research["regraded_from"] = before
    research["regraded_to"] = after
    research["ladder_ratified"] = REGRADE_LADDER_RATIFIED
    research["regrade_says"] = entry.get("moved") or ""
    out["resident_research"] = research

    body = strip_regrade(out.get("note") or "")
    out["note"] = (
        f"{REGRADE_MARK} ({REGRADE_TICKET}, rule {rule}): {before} -> {after}. "
        f"{entry.get('moved') or ''} The ladder's words for {rule}: {says}".strip()
        + REGRADE_SENTINEL + body).strip()
    return out


def regrade_build(preload: dict | None = None):
    """(files to write, applied rows, refused rows) — a pure read of ledger + tree."""
    docs = ({pathlib.Path(p): json.loads(t) for p, t in preload.items()
             if pathlib.Path(p) != INDEX}
            if preload is not None
            else {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))})
    index = (json.loads(preload[INDEX]) if preload is not None and INDEX in preload
             else load(INDEX))
    entries = load(LEDGER)["rulings"]

    where: dict = {}
    for path, doc in docs.items():
        for i, person in enumerate(doc.get("persons") or []):
            if person.get("id"):
                where[person["id"]] = (path, i)

    touched: dict = {}
    applied, refused = [], []
    for entry in entries:
        seat = where.get(entry["person_id"])
        # R4 is the one refusal that writes NOTHING: the card is re-derived whole by
        # another pass, so even a refusal noted on it would be wiped by that pass's next
        # build and would read, wrongly, as a refusal nobody ever made.
        if seat is None or entry["decision"] == "R4":
            refused.append(entry)
            continue
        path, i = seat
        doc = touched.get(path) or json.loads(json.dumps(docs[path]))
        doc["persons"][i] = regrade_person(doc["persons"][i], entry)
        touched[path] = doc
        (applied if entry["decision"] == "applied" else refused).append(entry)

    files = {path: dumps(doc, 1) for path, doc in touched.items()}

    # index.json carries a per-household grade tally and two counts this pass moves.
    # They are re-derived from the tree AS THIS PASS LEAVES IT, so the manifest and the
    # cards cannot disagree — `synthesize_resident_research.py --check` compares them.
    final = dict(docs)
    final.update({p: json.loads(t) for p, t in files.items()})
    by_id = {doc["id"]: doc for doc in final.values() if doc.get("id")}
    for entry in index["households"]:
        doc = by_id.get(entry["id"])
        if not doc:
            continue
        tally: dict = {}
        for person in doc.get("persons") or []:
            tally[person["grade"]] = tally.get(person["grade"], 0) + 1
        entry["grades"] = dict(sorted(tally.items()))
        # Only where the row already carries the flag. Three passes write these rows and
        # they do not all emit it; adding the key to a row whose owner omits it turns
        # that pass's own byte-for-byte check red for a field it never claimed.
        if "projected_resident" in entry:
            entry["projected_resident"] = any(
                p.get("resident_subtype") == "projected_resident"
                for p in doc.get("persons") or [])
    totals = {"attested": 0, "inferred": 0, "reconstructed": 0}
    for entry in index["households"]:
        for grade, n in entry["grades"].items():
            totals[grade] = totals.get(grade, 0) + n
    index["counts"]["by_grade"] = totals
    index["counts"]["projected_residents"] = sum(
        1 for doc in final.values() for p in doc.get("persons") or []
        if p.get("resident_subtype") == "projected_resident")
    files[INDEX] = dumps(index, 1)
    return files, applied, refused


def regrade_report(applied, refused) -> None:
    print(f"{'REGRADED':<10}{len(applied)} proposal(s) applied\n")
    for entry in applied:
        before = entry["from"].get("grade")
        if entry["from"].get("resident_subtype"):
            before += "/" + entry["from"]["resident_subtype"]
        after = entry["to"].get("grade")
        if entry["to"].get("resident_subtype"):
            after += "/" + entry["to"]["resident_subtype"]
        print(f"  {entry['rule']:<5}{entry['person_id']:<34}{before} -> {after}")
    buckets: dict = {}
    for entry in refused:
        buckets.setdefault(entry["decision"], []).append(entry)
    print(f"\n{'REFUSED':<10}{len(refused)} proposal(s) declined, "
          f"each written on the person except R4\n")
    for rid in sorted(buckets):
        rows = buckets[rid]
        print(f"  {rid}  {len(rows):>3}  {REFUSAL_HEADLINE.get(rid, '')}")
        for entry in rows:
            print(f"        {entry['rule']:<5}{entry['person_id']:<34}"
                  f"{entry.get('refusal_says', '')}")


def regrade_scale() -> None:
    """What the pass is worth to the town, counted rather than asserted."""
    before = load(INDEX)["counts"]
    files, applied, refused = regrade_build()
    after = json.loads(files[INDEX])["counts"]
    print("what --regrade does to the town")
    for key in ("by_grade", "projected_residents"):
        print(f"  {key}: {before.get(key)}  ->  {after.get(key)}")
    print(f"  rulings: {len(applied)} applied, {len(refused)} refused")



def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--scale", action="store_true")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ledger", action="store_true",
                    help="with --regrade: compile the ruling from the proposal. Run ONCE; "
                         "see the file's own _doc for why it is not recomputed")
    ap.add_argument("--regrade", action="store_true",
                    help="apply the ladder to the people the town already carries (T-0705); "
                         "composes with --check and --report")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.gate:
        return gate()

    if args.regrade:
        if args.ledger:
            docs = {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))}
            rulings = regrade_ledger(docs, load(INDEX))
            LEDGER.write_text(dumps({
                "schema": 1,
                "ticket": REGRADE_TICKET,
                "generated_by": "tools/mint_civic_residents.py --regrade --ledger",
                "compiled_on": REGRADE_ON,
                "ladder_ratified": REGRADE_LADDER_RATIFIED,
                "compiled_from": [
                    "data/research/residents/grading_proposal.json",
                    "data/research/residents/identity_master.json",
                    "data/residents/households/",
                ],
                "_doc": (
                    "THE RULING, not a derivation. `changes_to_existing_people` in the "
                    "grading proposal is by definition the rows where the ladder and a "
                    "committed card DISAGREE, so the moment the card is written the row "
                    "leaves the proposal and the decision can no longer be recomputed "
                    "from it. This file is compiled once, carries everything each "
                    "decision rested on — the rule, the ladder's words, the move, the "
                    "refusal and the evidence rows read on the day — and "
                    "`--regrade` applies it. Recompiling it against a town this pass has "
                    "already written would produce an empty file; that is the point, and "
                    "it is why the compile is a separate switch."),
                "counts": {
                    "rulings": len(rulings),
                    "applied": sum(1 for r in rulings if r["decision"] == "applied"),
                    "refused": sum(1 for r in rulings if r["decision"] != "applied"),
                },
                "refusals": REFUSAL_HEADLINE,
                "rulings": rulings,
            }, 1), encoding="utf-8")
            print(f"wrote {LEDGER.relative_to(ROOT)}; {len(rulings)} ruling(s)")
            return 0
        if args.scale:
            regrade_scale()
            return 0
        files, applied, refused = regrade_build()
        if args.report:
            regrade_report(applied, refused)
            return 0
        if args.check:
            stale = [p for p, text in sorted(files.items())
                     if not p.exists() or p.read_text(encoding="utf-8") != text]
            for path in stale:
                print(f"   {path.relative_to(ROOT)} does not match the regrade")
            if stale:
                print(f"   {len(stale)} file(s) differ; run --regrade")
                return 1
            print(f"   OK: {len(applied)} regrade(s) and {len(refused)} refusal(s) "
                  f"re-derive byte for byte")
            return 0
        for path, text in sorted(files.items()):
            path.write_text(text, encoding="utf-8")
        print(f"wrote {len(files)} file(s); {len(applied)} regraded, {len(refused)} refused")
        return 0

    if args.scale:
        scale_report()
        return 0

    files, accepted, refusals, mine_paths = build()
    if args.report:
        report(accepted, refusals)
        return 0
    if args.check:
        stale = []
        for path, text in sorted(files.items()):
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path)
        for path in sorted(mine_paths):
            if path not in files:
                stale.append(path)
        for path in stale:
            print(f"   {path.relative_to(ROOT)} does not match the derivation")
        if stale:
            print(f"   {len(stale)} file(s) differ; run --build")
            return 1
        print(f"   OK: {len(accepted)} civic resident(s) re-derive byte for byte")
        return 0

    for path in sorted(mine_paths):
        if path not in files:
            path.unlink()
    for path, text in sorted(files.items()):
        path.write_text(text, encoding="utf-8")
    print(f"wrote {len(files)} file(s); {len(accepted)} minted, {len(refusals)} refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
