#!/usr/bin/env python3
"""The scene-date register: who and what the papers put in Chicago on 1 July 1835.

    tools/compile_register.py --build       recompile register_1835.json
    tools/compile_register.py --check       the gate
    tools/compile_register.py --self-test   the gate's assertions still fire

WHAT THIS IS FOR (T-0262). The reading passes filled `gazetteer.json` with 221
businesses and 2,201 people read out of the 1833-1835 papers. A gazetteer is an
index of what was PRINTED; it says nothing about what the model should build. This
turns it into the register the seeding tickets work from — for every business, is it
standing on the scene date, where, and what does the town have to do about it; for
every person, is that somebody the town already has, somebody it invented a stand-in
for, or somebody new.

NOTHING HERE IS AUTHORED. The register is derived, wholly, from the gazetteer and
from the committed dataset beside it, and `--check` re-derives it and refuses a
committed file that a rebuild would not produce. That is the same contract
gazetteer.json is under and for the same reason: a hand-edited register is a place to
quietly promote a business into the town without an argument.

THE OWNER'S THREE RULINGS, 2026-08-28, and where each one lands here:

  1. A LETTER-LIST NAME IS ENOUGH TO MINT A RESIDENT. So a person known only from the
     post-office lists takes an action like any other — `new_resident` — and carries
     `letter_list_only: true` beside it. The counts report the two strengths
     separately, because 1,594 of the 2,201 are letter-list-only and a total that
     hides that is a number nobody can act on.
  2. TRANSCRIPTION-MEDIATED READINGS GRADE `documented`. Nothing here re-grades
     anything; the flag lives on the claim and travels with it.
  3. A DOCUMENTED BUSINESS IS BUILT AT THE SCENE DATE UNLESS CONTRADICTED — and this
     tool reads the word BEFORE in that ruling, which the gazetteer does not.
     `built_at_scene_date` there is `not contradicted_by`, whatever the contradiction
     is dated: a firm dissolved in August 1835 is struck out of a July town it was
     demonstrably standing in. The exclusion test here is a contradiction dated ON OR
     BEFORE the scene date. A LATER one is recorded, not obeyed —
     `dissolved_after_scene_date` — and the business stands.

TWO EXCLUSIONS, AND THE SECOND ONE NOW READS THE PAPER RATHER THAN A PROXY (T-0356).
T-0262 asked to exclude "entries whose only 1835 evidence `announces_opening` after
Jul 1", and there was no such field to read, so this tool used the derivable proxy
instead: a business whose FIRST issue postdated the scene date was excluded as
`first_evidence_after_scene_date`. Conservative in the direction provenance wants,
and NOT the same question — and the re-read of the thirty-eight it caught is what
settles that. Wm. H. Taylor's boot store advertised over a dateline of 8 JULY 1834,
Wm. H. Kennicott said he had practised dentistry in the town "for the past year",
Samuel Lewis's music-school copy is dated 22 June, S. Abell's 24 June and John
Holbrook's 10 June. Five houses excluded from a town they were printed standing in,
because the first SURVIVING issue that carried them falls in August.

So `announces_opening` is a field now (tools/compile_gazetteer.py § OPENING_DATINGS)
and the exclusion reads it. The DATING is what decides:

  stated    the paper names a date the house WILL open. After the scene date, that is
            the paper saying it was not open then — `opening_announced_after_scene_date`.
            Four houses: Cromelien's wine branch (14 Aug), Everts' high school for young
            gentlemen (10 Aug), Hunt's for young ladies (17 Aug) and Lyon's wholesale
            grocery (1 Sep).
  effected  an opening already made, dated by the advertisement's own dateline. It bounds
            the opening from ABOVE and can never exclude — "has opened", printed on 7
            August, is silent about 1 July. On or before the scene date it is the
            opposite: positive evidence the house stood.
  undated   an opening the printing dates nowhere. It decides nothing either way.

WHAT REPLACED THE PROXY IS NOT NOTHING. A business first printed in August and never
announcing an opening now stands in the July town under ruling 3 — documented, not
contradicted — and that is a LIBERTY, the forward twin of `survival_liberty_required`.
`backdating_liberty_required` names it: existence documented only after the scene date,
presence on the scene date assumed, and no opening notice dated on or before it to
carry the assumption. It is computed here and never asserted, exactly as its twin is.

WHAT AN ACTION MEANS, for the seeding tickets that consume this:

  enrich_existing  a committed structure already carries this business, matched on the
                   proprietors' surnames. The town needs a fuller record, not a roof.
  new_building     nothing committed carries it AND the paper's own placement resolves
                   against the committed town — a corner of two platted streets, or a
                   landmark that is a committed structure, or one hop through another
                   documented business that is. Placeable; T-0263's queue.
  street_only      documented and placeable no further than a street face. The paper
                   named a street this town has, and nothing narrower.
  unplaceable      no street the model holds, OR the firm's own record puts it out of
                   town (T-0355, `outside_plat`). Recorded, not buildable.

AND WHAT A PERSON ACTION MEANS:

  enrich           `data/residents/` already holds this person, matched under the
                   gazetteer's OWN identity policy (surname plus forename initials,
                   imported from compile_gazetteer so the two tools cannot drift).
  replace_invented a documented person whose occupation is one the town INVENTED a
                   household for. The candidate to retire that invention (T-0264).
  new_resident     everybody else. Ruling 1: a letter-list name is enough.

THE RETIREMENT COUNT IS A COUNT OF INVENTED HOUSEHOLDS, NOT OF PEOPLE, and it is
capped per trade by construction: three documented tailors retire at most the number
of invented tailors the town holds. Reporting the matched persons instead would
report 2,201 people retiring 133 households, which is not a number about anything.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compile_gazetteer import (  # noqa: E402  — the identity policy has one home
    REPO, ROOT, RESEARCH, GAZETTEER,
    SCENE_DATE, dumps, firm_surnames, initials, load_json, slug, surname, unmarked,
)

import re  # noqa: E402

REGISTER = RESEARCH / "register_1835.json"
STRUCTURES = ROOT / "data" / "structures"
STREETS = ROOT / "data" / "streets" / "1835.json"
RESIDENTS = ROOT / "data" / "residents"

SCHEMA_VERSION = 1

BUSINESS_ACTIONS = ("enrich_existing", "new_building", "street_only", "unplaceable")
PERSON_ACTIONS = ("enrich", "replace_invented", "new_resident")
EXCLUSIONS = ("contradicted_before_scene_date", "opening_announced_after_scene_date")

# Words that carry no identity in a name or an anchor: articles, the honorifics the
# papers set before a name, and the four nouns that appear in half the storefronts in
# town. Dropping them is what lets "Messrs. Newberry & Dole's store" meet the committed
# record "Newberry & Dole Warehouse"; keeping them would make every anchor unique.
ANCHOR_STOP = {
    "the", "a", "an", "of", "and", "at", "in", "on", "s", "to", "his", "their", "its",
    "street", "streets", "st", "sts", "messrs", "mr", "mrs", "dr", "esq", "jr", "sen",
    "new", "chicago", "late", "one", "two", "three", "door", "doors", "opposite",
    "next", "near", "above", "below", "east", "west", "north", "south", "side",
}

# The trade a paper prints is prose; `data/residents/` speaks a closed occupation
# vocabulary. This is the whole of the translation between them and it is deliberately
# a table rather than a matcher: a fuzzy trade match would silently retire an invented
# household on a word that happened to collide. First hit in order wins, so the
# compound trades sit above the words they contain.
TRADE_TO_OCCUPATION = (
    # ORDER IS THE RULE HERE: the first needle that appears anywhere in the printed
    # trade wins, so a longer trade whose letters contain a shorter one has to be
    # listed above it. "mill" sits inside "milliner", which is how every milliner in
    # this corpus was being compiled as a MILLER (T-0376) — Elmira Fowler, who
    # advertised "Millinery & Dress Making" on Dearborn Street in November 1834, and
    # Mrs H. Sherman, who took a room two doors from the Mansion House a month later.
    # A dressmaker recorded as a grain miller is not a near miss; it is a trade the
    # paper never gives her, and this project may not mint a resident over one.
    ("millinery", "milliner"),
    ("milliner", "milliner"),
    ("dress making", "dressmaker"),
    ("dressmaking", "dressmaker"),
    ("dress maker", "dressmaker"),
    ("dressmaker", "dressmaker"),
    ("forwarding and commission", "forwarding_and_commission"),
    ("boarding house", "boarding_house_keeper"),
    ("soap", "soap_and_candle_maker"),
    ("candle", "soap_and_candle_maker"),
    ("ship carpenter", "ship_carpenter"),
    ("dry goods", "dry_goods_merchant"),
    ("hardware", "hardware_merchant"),
    ("harness", "harness_maker"),
    ("watchmaker", "watchmaker"),
    ("wheelwright", "wheelwright"),
    ("lumber", "lumber_merchant"),
    ("attorney", "attorney"),
    ("counsellor", "attorney"),
    ("auction", "auctioneer"),
    ("bakery", "baker"),
    ("bake", "baker"),
    ("baker", "baker"),
    ("barber", "barber_surgeon"),
    ("blacksmith", "blacksmith"),
    ("brick", "brickmaker"),
    ("builder", "builder"),
    ("butcher", "butcher"),
    ("cabinet", "joiner"),
    ("carpenter", "carpenter"),
    ("chair", "joiner"),
    ("clothier", "clothier"),
    ("clothing", "clothier"),
    ("cooper", "cooper"),
    ("dentist", "dentist"),
    ("drover", "drover"),
    ("druggist", "druggist"),
    ("drug", "druggist"),
    ("editor", "editor"),
    ("ferry", "ferryman"),
    ("gunsmith", "gunsmith"),
    ("grocer", "grocer"),
    ("grocery", "grocer"),
    ("groceries", "grocer"),
    ("hotel", "hotel_keeper"),
    ("joiner", "joiner"),
    ("mason", "mason"),
    ("miller", "miller"),
    ("mill", "miller"),
    ("painter", "painter"),
    ("physician", "physician"),
    ("plasterer", "plasterer"),
    ("post office", "postmaster"),
    ("printer", "printer"),
    ("printing", "printer"),
    ("saddler", "saddler"),
    ("saddle", "saddler"),
    ("sailmaker", "sailmaker"),
    ("sawyer", "sawyer"),
    ("school", "schoolteacher"),
    ("shoemaker", "shoemaker"),
    ("boot", "shoemaker"),
    ("shoe", "shoemaker"),
    ("surveyor", "surveyor"),
    ("tailor", "tailor"),
    ("tanner", "tanner"),
    ("tavern", "tavern_keeper"),
    ("public house", "tavern_keeper"),
    ("teamster", "teamster"),
    ("trader", "trader"),
    ("merchant", "merchant"),
    ("store", "merchant"),
)


# --------------------------------------------------------------------------
# normalising an anchor, a name and a street


def words(text):
    """The identity-bearing words of a name or an anchor, lower-cased."""
    t = unmarked(text or "").lower().replace("&", " and ")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return [w for w in t.split() if w and w not in ANCHOR_STOP]


def street_key(name):
    """'South Water-street' → 'south_water'. The plat's key, or '' for a road it lacks."""
    t = re.sub(r"[^a-z0-9]+", " ", (name or "").lower())
    t = re.sub(r"\b(street|streets|st|sts)\b", " ", t)
    return "_".join(t.split())


def occupation_of(text):
    """The residents vocabulary's word for a printed trade, or None."""
    t = (text or "").lower()
    for needle, occ in TRADE_TO_OCCUPATION:
        if needle in t:
            return occ
    return None


# --------------------------------------------------------------------------
# the committed town, read once


def read_town(structures_dir=STRUCTURES, streets_file=STREETS, residents_dir=RESIDENTS):
    """Index the committed dataset the register resolves against.

    Read in sorted filename order and reduced to sets, so the register does not depend
    on the order a filesystem hands back.
    """
    town = {"structures": [], "streets": {}, "residents": [], "invented": {},
            "has_creek": False}

    for path in sorted(Path(structures_dir).glob("*.json")):
        d = load_json(path)
        names = [d.get("name") or ""] + list(d.get("aka") or [])
        occ_prose = (d.get("occupants") or {}).get("value") or ""
        occ = scene_date_occupants(occ_prose)
        function = (d.get("function") or {}).get("value")
        town["structures"].append({
            "id": d["id"],
            "name": d.get("name"),
            "name_words": [set(words(n)) for n in names if words(n)],
            # T-0385: the same names with a disambiguator this project added taken off,
            # kept as their own pool so the relaxed match can never overreach the exact one.
            "undisambiguated_words": [set(words(u)) for u in
                                      (undisambiguated(n) for n in names) if u and words(u)],
            "aka_head_words": [set(words(head_of(n))) for n in names[1:] if words(head_of(n))],
            "occupant_words": set(words(occ)),
            "occupant_text": occ,
            "aka_texts": [head_of(n) for n in names[1:]],
            "identity_text": " ; ".join([d.get("name") or "", occ_prose]
                                        + [head_of(n) for n in names[1:]]),
            "function": function,
            "occupation": occupation_of((function or "").replace("_", " ")),
            "anonymous": d["id"].startswith(("recon_", "inf_")),
        })

    for s in load_json(streets_file).get("streets", []):
        town["streets"][street_key(s["name_1835"])] = s["id"]
        town["streets"][s["id"]] = s["id"]

    # The creek marker in OUTSIDE_MARKERS is only sound while this stays False.
    town["has_creek"] = any(
        "creek" in n.lower()
        for st in town["structures"] for n in [st["name"] or ""] + st["aka_texts"])

    for path in sorted(Path(residents_dir, "households").glob("*.json")):
        d = load_json(path)
        for p in d.get("persons", []):
            occ = p.get("occupation")
            town["residents"].append({
                "household": d["id"],
                "person": p["id"],
                "name": p.get("name"),
                "grade": p.get("grade"),
                "occupation": occ.get("value") if isinstance(occ, dict) else occ,
            })

    # The invented layer, per trade: how many households the town raised because no
    # documented person was available for that trade. This is the ceiling on what the
    # register can retire, and it is a count of HOUSEHOLDS — one invented cooper's
    # household is one thing to retire however many people it holds.
    for r in town["residents"]:
        if r["grade"] in ("reconstructed", "inferred") and r["occupation"]:
            town["invented"].setdefault(r["occupation"], set()).add(r["household"])
    town["invented"] = {k: sorted(v) for k, v in sorted(town["invented"].items())}
    return town


# A DISAMBIGUATOR THIS PROJECT ADDS, IN THE THREE SHAPES IT WRITES THEM (T-0385). A
# record's name is written for a catalogue that has to hold two buildings of one name
# apart, so `tremont_house_1` is called "Tremont House (the first)" with aka "Tremont
# House I" and "the old Tremont House" — three names, every one of them carrying an
# ordinal or an age this project supplied, and none of them the two words the American
# sets: "the Tremont House". Whole-set equality then matched nothing, and four
# businesses lost the only anchor they have on one editorial habit.
#
# THE SHAPE IS THE WHOLE GUARD, and a word list would not have been one. `first` and
# `old` are ordinary words that sources also print — "the First Baptist meeting house",
# "Chicago's first post office" — and striking them wherever they fall turns a
# congregation's name and a historical superlative into anchors they are not. So only
# the three positions this project writes a disambiguator in are stripped: a TRAILING
# parenthetical, a TRAILING roman numeral, and a LEADING `old`. Every one of them is an
# editorial suffix or prefix on a name that is complete without it. The leading form
# is `old` alone and not the ordinals: this project writes "the old Tremont House" and
# "Tremont House (the first)", never "the first Tremont House", so a leading ordinal is
# always somebody else's word — "the First Baptist meeting house" is a congregation.
TRAILING_PAREN = re.compile(r"\s*\((?:the\s+)?(?:first|second|third|fourth|older|"
                            r"earlier|old|new|later|i|ii|iii|iv)\)\s*$", re.I)
TRAILING_NUMERAL = re.compile(r"\s+(?:i{1,3}|iv)\s*$", re.I)
LEADING_OLD = re.compile(r"^\s*(the\s+)?(?:old|older)\s+", re.I)


def undisambiguated(name):
    """`name` with a disambiguator this project appended or prefixed taken off, or None.

    None when the name carries none — a name nobody disambiguated is already the name
    a source would print, and it is matched exactly by the rule above.
    """
    out = TRAILING_PAREN.sub("", name or "")
    out = TRAILING_NUMERAL.sub("", out)
    out = LEADING_OLD.sub(lambda m: m.group(1) or "", out)
    out = out.strip()
    return out if out and out != (name or "").strip() else None


def match_landmarks(town, anchor_words):
    """EVERY committed structure an anchor NAMES, in id order. A list, never a pick.

    Whole-set equality, not containment: an anchor is only a landmark when it is the
    same set of identity-bearing words as a record's name or aka. Containment would put
    'the store' on the first store in the town.

    AND IT RETURNS ALL OF THEM, BECAUSE A NAME IS NOT ALWAYS ONE BUILDING. This used to
    end `return sorted(hits)[0] if hits else None`, which is an alphabetical tie-break
    wearing a resolution's clothes: where two committed records answer to one name, the
    register seated the business in whichever id sorted first and wrote "the landmark is
    the committed structure X" over a coin toss, with nothing in the file to say a
    second record had answered to the same name. `structures_sharing_a_name` in the
    register's `compiled_from` block counts the town's exposure (T-0386); the named case
    is John Wright's two buildings to let, `wright_building_to_let_a` and `_b`, which
    are one advertisement's two buildings under one proprietor's name, and the piers,
    the two branch bridges and the school houses are the same shape. `resolve_anchor`
    refuses the ambiguity rather than taking the first.

    THE ONE RELAXATION, AND WHERE ITS GUARD NOW LIVES (T-0385). Exact equality is tried
    first and always wins. Only when it finds nothing is each record retried on its
    names with the disambiguator this project added stripped off — so the American's
    "the Tremont House" reaches `tremont_house_1`, whose every name carries an ordinal
    or an age no printing of 1835 has. Nothing is stripped from the ANCHOR: the paper's
    words are the evidence and are read as printed. The relaxed pass returns a LIST like
    the exact one, and that is the guard rather than a weakening of it — the
    disambiguator is precisely what tells two houses of one name apart, so an anchor
    that omits it cannot choose between them, and a second Tremont in the dataset gives
    two hits which `resolve_anchor` refuses as ambiguous. Written that way round, the
    refusal is REPORTED in the register's own note (T-0386's mechanism) instead of
    disappearing into a silent None, which is what the first cut of this rule did.
    """
    if not anchor_words:
        return []
    hits = sorted({s["id"] for s in town["structures"]
                   if any(anchor_words == pool for pool in s["name_words"])})
    if hits:
        return hits
    return sorted({s["id"] for s in town["structures"]
                   if any(anchor_words == pool
                          for pool in s.get("undisambiguated_words") or [])})


# A phrase that locates a building by ANOTHER building is not that building's name.
# `aka: ["the cabins near Wentworth's tavern"]` names cabins; the tavern in it is the
# landmark they are near. Cutting an aka at its first locative word is what stops a
# surname on the far side of that word from being read as an occupant, which is how
# Elijah Wentworth's tavern on Flag Creek matched a row of log cabins at Wolf Point.
LOCATIVE = re.compile(
    r"\b(near|next|adjoining|adjacent|opposite|behind|beside|between|above|below|"
    r"at|on|by|from|off|over|under|toward|towards|facing)\b", re.I)


def head_of(name):
    """A name with any locative tail cut away. 'Log cabins at Wolf Point' → 'Log cabins'."""
    return LOCATIVE.split(name or "", maxsplit=1)[0]


# A DATE QUALIFICATION ON AN OCCUPANT IS A STATEMENT THAT HE IS NOT THERE NOW (T-0355).
# `wolf_point_tavern_stable` records "the tavern's keeper of the day — Elijah Wentworth
# in 1831, William Walters on the scene date", and the sentence names its scene-date
# occupant in the same breath as the man who preceded him. Read whole, the line put
# E. Wentworth's tavern — which is on Flag Creek, eighteen miles out on the Ottawa road
# — inside a Wolf Point stable, three times over.
#
# The clause is the unit, because that is how these lines are written: a comma, a
# semicolon or a spaced dash separates one tenancy from the next. A clause that dates
# ITSELF to a year the scene date does not fall in describes a FORMER occupant and is
# no evidence of who is in the building on 1 July 1835. A clause carrying no year at
# all says nothing about date and is kept — the great majority of these lines.
#
# Only the WORDS are filtered. `occupant_text` reports the scene-date reading so the
# register's evidence quotes what actually matched, and `identity_text` keeps the whole
# prose, because a forename printed anywhere in the record can still contradict a
# paper's (initials_compatible is a veto, and a veto wants every word it can get).
OCCUPANT_CLAUSE = re.compile(r"\s*[;,]\s*|\s+[\u2014\u2013-]\s+")
YEAR_SPAN = re.compile(r"\b(1[78]\d\d)(?:\s*[-\u2013]\s*(\d{2,4}))?\b")


def year_spans(text):
    """Every year or year range a clause states, as inclusive (from, to) pairs.

    '1833-34' is 1833 to 1834 and '1834-1836' is 1834 to 1836; a two-digit tail takes
    its century from the year it hangs off, which is how the committed records write it.
    """
    out = []
    for start, tail in YEAR_SPAN.findall(text or ""):
        start = int(start)
        end = start
        if tail:
            end = int(tail)
            if end < 100:
                end += start - start % 100
        out.append((start, max(start, end)))
    return out


def scene_date_occupants(text, scene_year=SCENE_DATE.year):
    """An occupants line with the clauses it dates away from the scene date struck out.

    Returns the surviving clauses rejoined. A clause survives when it states no year, or
    when a year it states — or a range it states — covers the scene year.
    """
    kept = []
    for clause in OCCUPANT_CLAUSE.split(text or ""):
        clause = clause.strip()
        if not clause:
            continue
        spans = year_spans(clause)
        if spans and not any(a <= scene_year <= b for a, b in spans):
            continue
        kept.append(clause)
    return "; ".join(kept)


FORENAME_RUN = r"((?:[A-Z][A-Za-z]*\.?\s+){0,3})"


def forenames_before(text, sn):
    """Every forename run this text prints before the surname `sn`, as word tuples.

    'John H. Kinzie, forwarding merchant' → [('john', 'h')]. An empty run — the surname
    printed bare, as 'Jones, grocer' — yields the empty tuple, which is compatible with
    anything: a record that does not print a forename cannot contradict one.
    """
    out = []
    for m in re.finditer(FORENAME_RUN + r"\b([A-Z][a-z]+)\b", text or ""):
        if slug(m.group(2)) != sn:
            continue
        out.append(tuple(w.strip(".").lower() for w in m.group(1).split()))
    return out


def forenames_of(name):
    """The forename words of a printed name, in order. 'R. A. Kinzie' → ('r', 'a')."""
    name = unmarked(name or "").strip()
    fore = name.split(",", 1)[1] if "," in name else " ".join(name.split()[:-1])
    return tuple(w.lower() for w in re.findall(r"[^\W\d_]+", fore, re.UNICODE))


def forenames_agree(a, b):
    """Two forename runs for one surname, compared as far as both of them go.

    The initial has to match, which is the papers' abbreviating habit respected. TWO
    SPELLED-OUT FORENAMES HAVE TO MATCH WHOLE, which is the refinement a building needs
    and a letter list does not: 'John S. Kinzie' and the James Kinzie House share an
    initial and are two different Kinzies, and an initials-only rule put the one inside
    the other.
    """
    for x, y in zip(a, b):
        if not x or not y or x[0] != y[0]:
            return False
        if len(x) > 1 and len(y) > 1 and x != y:
            return False
    return True


def initials_compatible(text, require, proprietors):
    """The person half of the identity policy, applied to a BUILDING's own prose.

    A firm matches a record on surnames (T-0304), which is right for firms and wrong for
    the men a building is named after: J. H. Kinzie's store and R. A. Kinzie were one
    surname and two brothers, and matching on 'kinzie' alone put the younger brother's
    business inside the elder's store. So where the record prints a forename for the
    surname and the paper prints one too, they must agree on the initials they share —
    the same prefix rule the resident match uses, because the papers abbreviate.

    IT IS ASKED OF THE WHOLE RECORD, not of the field the surname was found in. A record
    named 'Dole's Warehouse' whose occupants line reads 'George W. Dole' prints a
    forename; letting the bare name match on its own would just route every disagreement
    round the guard by dropping to the next tier.
    """
    for who in proprietors:
        for sn in firm_surnames(who) & require:
            mine = forenames_of(who)
            if not mine:
                continue
            runs = [r for r in forenames_before(text, sn) if r]
            if not runs:
                continue
            if not any(forenames_agree(r, mine) for r in runs):
                return False
    return True


def match_occupant(town, require, business_occupation, proprietors):
    """The committed structure that ALREADY CARRIES this firm, with its evidence tier.

    Returns (structure_id, tier) or (None, None). Three tiers, tried in order, and the
    third is the only one that has to argue:

      occupants  the record's own statement of who is in the building. Trusted alone:
                 a building can hold a printing office and a dry-goods store at once,
                 and demanding that the trades agree would throw away exactly the
                 record that says both are there.
      name       the record is NAMED for the firm.
      aka        an alternate name carries the firm — accepted only when the trades
                 also agree, because an aka is where a record keeps its loosest
                 descriptions. 'Taylor's tavern' is a real aka of the Wolf Point
                 Tavern and W. H. Taylor's boot and shoe store is a different Taylor.

    ANONYMOUS RECONSTRUCTED AND INFERRED ROOFS ARE NOT CANDIDATES. `recon_*` and `inf_*`
    are invented buildings; one of them cannot ALREADY carry a documented business, and
    quietly matching a firm into one would launder an invention into the documented
    layer. Putting a documented business into an anonymous roof is a decision T-0263
    makes deliberately, with the adoption written down.
    """
    if not require:
        return None, None, None
    for tier in ("occupants", "name", "aka"):
        hits = []
        for s in town["structures"]:
            if s["anonymous"]:
                continue
            if tier == "occupants":
                pools, text = [s["occupant_words"]], s["occupant_text"]
            elif tier == "name":
                pools, text = s["name_words"][:1], s["name"] or ""
            else:
                pools, text = s["aka_head_words"], " ; ".join(s["aka_texts"])
                if not (business_occupation and s["occupation"] == business_occupation):
                    continue
            if not any(pool and require <= pool for pool in pools):
                continue
            if not initials_compatible(s["identity_text"], require, proprietors):
                continue
            hits.append((s["occupation"] != business_occupation, s["id"], text))
        if hits:
            # The trades agreeing is the tie-break, then the id — so a firm that matches
            # both a tavern and that tavern's stable lands on the tavern, and the choice
            # does not depend on the order the files were read in.
            _, sid, text = sorted(hits)[0]
            return sid, tier, text
    return None, None, None


# OUTSIDE THE PLAT IS A THING THE PAPERS SAY, AND SAYING IT ENDS THE MATTER (T-0355).
# A tavern eighteen miles out on the Ottawa road cannot be in a Wolf Point stable
# whoever kept it, and no reading of a committed record's prose should be able to put
# it there. This is the general form of that fault: the firm's OWN record states where
# it stands, and when what it states is outside the committed town, no match against
# the committed town is admissible — not on an occupants line, not on a name, not on
# an aka, and the town does not build it either.
#
# THREE MARKERS, AND EACH IS A POSITIVE STATEMENT, never an absence. A business the
# papers place nowhere is `unplaceable` already and is not this; a business this rule
# excludes is one whose own printed placement puts it out of town.
#
#   miles   a distance in miles. The plat is under a mile across, so nothing inside it
#           is ever described in miles.
#   road    a ROAD LEADING TO somewhere. The town's own ways are streets and are named
#           as streets; 'the road from Chicago leading to Ottawa' is a road out of it.
#   creek   a named creek. The committed town holds the river and its two branches and
#           no creek of any name — checked in read_town, not asserted here — so a named
#           creek is ground this reconstruction does not cover.
#
# Counted over the 242 gazetteer businesses on 2026-08-29: five hits, and all five are
# genuinely out of town (the four Flag Creek readings of Wentworth's tavern, and Richard
# M. Sweet's barn on the Dupage, which the gazetteer's own note already calls outside).
OUTSIDE_MARKERS = (
    ("a distance in miles", re.compile(r"\b(?:[A-Za-z0-9-]+\s+)?miles?\b", re.I)),
    ("a road leading out of town", re.compile(r"\broad\b[^.;]{0,40}?\bto\b", re.I)),
    ("a named creek", re.compile(r"\b[A-Z][a-z]+\s+Creek\b")),
)


def structures_sharing_a_name(town):
    """How many identity-word sets the committed town holds under MORE THAN ONE record.

    The exposure `match_landmarks` refuses: every one of these is a name an anchor could
    print and no record could claim alone. Derived on every build so the figure cannot
    go stale in prose, and reported by `--check` (T-0386).
    """
    seen = {}
    for s in town["structures"]:
        for pool in s["name_words"]:
            if pool:
                seen.setdefault(frozenset(pool), set()).add(s["id"])
    return sum(1 for ids in seen.values() if len(ids) > 1)


def outside_the_plat(business, town):
    """Why the firm's own record puts it outside the committed town, or None.

    Reads everything the gazetteer prints about WHERE the business is — its name, which
    is the paper's own wording, and every field of its placement. A marker that names a
    creek is only believed while the committed town holds no creek; if one is ever
    committed the marker retires itself rather than mis-excluding a business on it.
    """
    placement = business.get("placement") or {}
    text = " | ".join(str(placement.get(k) or "")
                      for k in ("anchor", "offset_normalized", "offset_text", "note"))
    text = (business.get("name") or "") + " | " + text
    for why, pattern in OUTSIDE_MARKERS:
        if why == "a named creek" and town["has_creek"]:
            continue
        m = pattern.search(text)
        if m:
            return "%s — %r" % (why, m.group(0).strip())
    return None


CORNER = re.compile(r"corner of\s+(.{0,40}?)\s+and\s+(.{0,40})", re.I)


def streets_in(town, text, require_suffix):
    """Every platted street a phrase names, as street ids.

    The plat's own names are the dictionary, matched whole-word with a hyphen or a space
    between the parts, because the papers set 'South Water-street' and 'South Water
    street' interchangeably.

    `require_suffix` asks that the name be FOLLOWED by 'st'/'street', and it is the
    difference between reading a phrase and reading a corner. In free prose it must be
    on: 'Lake' alone is a lake here as often as a street, and 'the road to Lake Michigan'
    is not a placement on Lake Street. Inside 'corner of X and Y' it must be off,
    because the papers write the suffix once for both — 'corner of Dearborn and
    Lake-sts.' names two streets and suffixes neither of them.
    """
    found = set()
    for key, sid in town["streets"].items():
        if "_" not in key and len(key) < 4:
            continue
        pattern = r"\b%s\b" % key.replace("_", "[ -]")
        if require_suffix:
            pattern += r"[ -]*(?:street|streets|st|sts)\b"
        if re.search(pattern, text or "", re.I):
            found.add(sid)
    return sorted(found)


def resolve_anchor(town, business, by_firm):
    """Where the paper's own placement lands in the committed town.

    Six outcomes, and the note on each says which one and why, because the seeding
    tickets have to be able to argue with it:

      corner     both streets named are on the committed plat
      structure  the landmark is a committed structure
      business   the landmark is another DOCUMENTED business which is itself resolved —
                 one hop and no more. 'One door east of Brewster, Hogan & Co.' is only
                 as placed as Brewster, Hogan & Co. is, and a chain of guesses is not
                 a placement.
      street     the anchor is a REACH of a platted street and nothing narrower — 'the
                 east end of South Water-street'. It is a real resolution and it is not
                 a placement, so it reads as its own kind rather than as a failure.
      ambiguous  the anchor NAMES something the town holds, and the town holds it more
                 than once. 'J. Wright's' is `wright_building_to_let_a` and `_b`. This
                 is a finding and not a failure: the name was recognised and the choice
                 between the records is not the paper's to make, so it is refused and
                 both are named. It never places (T-0386).
      unresolved everything else, stated

    Only the first three put a building on the ground; `street` and `unresolved` do not,
    which is what the action rules below turn on.
    """
    placement = business.get("placement") or {}
    text = " ".join(str(x) for x in (placement.get("anchor"),
                                     placement.get("offset_normalized"),
                                     placement.get("offset_text")) if x)
    if not text.strip():
        return {"kind": "unresolved", "target": None, "streets": None, "via": None,
                "note": "The paper gives no anchor."}

    m = CORNER.search(text)
    if m:
        a, b = streets_in(town, m.group(1), False), streets_in(town, m.group(2), False)
        pair = sorted(set(a) | set(b))
        if len(a) == 1 and len(b) == 1 and len(pair) == 2:
            return {"kind": "corner", "target": None, "streets": pair, "via": None,
                    "note": "A crossing of two platted streets: %s." % " and ".join(pair)}
        return {"kind": "unresolved", "target": None, "streets": None, "via": None,
                "note": "A corner of %r and %r, and the plat resolves %s."
                        % (m.group(1).strip(), m.group(2).strip(),
                           "both sides to %s" % pair if pair else "neither side")}

    anchor_words = set(words(placement.get("anchor")))
    if anchor_words:
        sids = match_landmarks(town, anchor_words)
        if len(sids) > 1:
            return {"kind": "ambiguous", "target": None, "streets": None, "via": None,
                    "note": "The landmark %r is the name of %d committed structures — "
                            "%s — and the anchor does not say which. Refused: the paper "
                            "names one building and this project holds more than one "
                            "under that name, so any pick between them would be this "
                            "file's and not the paper's."
                            % (placement.get("anchor"), len(sids), ", ".join(sids))}
        if sids:
            return {"kind": "structure", "target": sids[0], "streets": None, "via": None,
                    "note": "The landmark is the committed structure %s." % sids[0]}
        # One hop: the landmark is another documented business. Same refusal — the
        # corpus prints one house under more than one heading, so a firm name can
        # answer for two records here exactly as a building name can above.
        others = sorted({other_id for other_id, other in by_firm
                         if other_id != business["id"] and other
                         and set(words(other)) == anchor_words})
        if len(others) > 1:
            return {"kind": "ambiguous", "target": None, "streets": None, "via": None,
                    "note": "The landmark %r is the name of %d documented businesses — "
                            "%s — and the anchor does not say which. Refused: one hop "
                            "off a house this corpus holds twice is not a placement."
                            % (placement.get("anchor"), len(others), ", ".join(others))}
        if others:
            return {"kind": "business", "target": None, "streets": None,
                    "via": others[0],
                    "note": "The landmark is another documented business (%s), which "
                            "places this one exactly as well as that one is placed."
                            % others[0]}
    named = streets_in(town, placement.get("anchor"), True)
    if named:
        return {"kind": "street", "target": None, "streets": named, "via": None,
                "note": "The anchor is a reach of %s and names nothing narrower."
                        % " and ".join(named)}
    return {"kind": "unresolved", "target": None, "streets": None, "via": None,
            "note": "The anchor %r names nothing the committed town holds."
                    % (placement.get("anchor") or text)}


# --------------------------------------------------------------------------
# the register


def anchor_change(town, business, by_firm):
    """The dated anchor change a house's own printings carry, resolved (T-0345).

    `anchor` above resolves the ONE placement the gazetteer holds live at the scene
    date. This is the rest of the history, and it exists because holding a superseded
    anchor as a second standing placement is how a placement sweep puts one shop in two
    places: Matthias Mason & Co.'s notice reads "nearly opposite Graves' Tavern" to
    1834-06-11 and "opposite the Tremont House" from 1834-09-10, and the register
    carried both as if they were live at once.

    Every superseded anchor is resolved against the committed town the same way the
    live one is, so a later pass can see what each reading WOULD have placed — which is
    the whole difference between a shop that moved and a landmark that was renamed, and
    this file decides neither.
    """
    change = business.get("anchor_change")
    if not change:
        return None
    return {
        "live_anchor": change["live_anchor"],
        "live_reason": change["live_reason"],
        "changes": change["changes"],
        "rule": change["rule"],
        "cannot_say": change["cannot_say"],
        "history": [dated_anchor(town, business, by_firm, w)
                    for w in change["history"]],
    }


# structure / corner / business put a building on the ground, `street` names a reach and
# nothing narrower, `unresolved` is a statement that the town holds no such thing. An
# anchor printed four ways is resolved on its BEST reading, because the four are declared
# to be one landmark and "Graves' Tavern" resolving where "Graves' Tavern, on Main-street"
# does not is a fact about how much of the sentence one reading pass swept into the field.
# `ambiguous` outranks `unresolved` because it RECOGNISED the name and outranks nothing
# else, because it places nothing: a reading that resolves to a street beats a reading
# that resolves to two buildings and cannot choose.
ANCHOR_KIND_RANK = {"unresolved": 0, "ambiguous": 1, "street": 2, "business": 3,
                    "corner": 4, "structure": 4}


def dated_anchor(town, business, by_firm, window):
    """One anchor of a dated history, with every reading of it resolved."""
    readings = [dict(r, resolved=resolve_anchor(
        town, {"id": business["id"], "placement": r["placement"]}, by_firm))
        for r in window["readings"]]
    best = max(readings,
               key=lambda r: (ANCHOR_KIND_RANK.get(r["resolved"]["kind"], 0),
                              -readings.index(r)))
    return {
        "anchor": window["anchor"],
        "first_issue": window["first_issue"],
        "last_issue": window["last_issue"],
        "claims": window["claims"],
        "live_at_scene_date": window["live_at_scene_date"],
        "resolved": best["resolved"],
        "resolved_on_reading": best["anchor"],
        "readings": [{"anchor": r["anchor"], "first_issue": r["first_issue"],
                      "last_issue": r["last_issue"], "claims": r["claims"],
                      "resolved": r["resolved"]} for r in readings],
    }


def compile_register(gazetteer, town, quiet=True):
    """Derive the register. Returns (doc, problems). Nothing here reads the clock."""
    problems = []
    scene = SCENE_DATE.isoformat()
    by_firm = sorted((b["id"], b["name"]) for b in gazetteer["businesses"])

    businesses = []
    for b in sorted(gazetteer["businesses"], key=lambda x: x["id"]):
        first, last = b["evidence"]["first_issue"], b["evidence"]["last_issue"]

        # Ruling 3, with the word BEFORE honoured (see the module docstring).
        before = [c for c in b["contradicted_by"] if c["issue"] <= scene]
        after = [c for c in b["contradicted_by"] if c["issue"] > scene]
        exclusion, exclusion_note = None, None
        if before:
            exclusion = "contradicted_before_scene_date"
            exclusion_note = ("Contradicted on or before the scene date by %s."
                              % ", ".join("%s (%s, %s)" % (c["claim"], c["kind"], c["issue"])
                                          for c in before))
        # T-0356. Only a STATED future opening can exclude, and it excludes on its own
        # date. An `effected` or `undated` announcement is recorded and obeyed by nothing.
        announced = b.get("opening_announced") or []
        stated_after = sorted(o for o in announced
                              if o.get("dating") == "stated" and (o.get("iso") or "") > scene)
        if not before and stated_after:
            o = stated_after[0]
            exclusion = "opening_announced_after_scene_date"
            exclusion_note = ("%s announces this house opening on %s, after the scene date "
                              "— \u201c%s\u201d. %s"
                              % (o["claim"], o["iso"], o["verbatim"], o["note"]))

        # The forward twin of the survival liberty: documented only after the scene date,
        # and standing in the July town on the assumption that it was already there.
        opened_by_scene = any((o.get("iso") or "") <= scene for o in announced if o.get("iso"))
        backdating = (exclusion is None and first > scene and not opened_by_scene)

        entry = {
            "id": b["id"],
            "name": b["name"],
            "trade": b.get("trade"),
            "occupation": occupation_of(b.get("trade")),
            "proprietors": b.get("proprietors") or [],
            "street": b.get("street"),
            "street_id": town["streets"].get(street_key(b.get("street"))),
            "placement_class": (b.get("placement") or {}).get("class"),
            "evidence": {"first_issue": first, "last_issue": last},
            "present_at_scene_date": exclusion is None,
            "exclusion": exclusion,
            "exclusion_note": exclusion_note,
            "dissolved_after_scene_date": [c["claim"] for c in after] if after else [],
            "opening_announced": announced,
            "survival_liberty_required": bool(b.get("survival_liberty_required")) and exclusion is None,
            "backdating_liberty_required": backdating,
            "anchor": resolve_anchor(town, b, by_firm),
            "anchor_change": anchor_change(town, b, by_firm),
            "outside_plat": outside_the_plat(b, town),
            "action": None,
            "action_target": None,
            "match_tier": None,
            "match_evidence": None,
            "action_note": None,
        }

        # enrich_existing: the committed town already carries this house, matched on
        # ALL the partners' surnames. The partners come out of the gazetteer's OWN firm
        # policy (T-0304), because a `proprietors` entry is routinely a whole style —
        # 'Clark, Filer & Co.', 'H. Doty & Co.', 'Kinzie & Hall' — and taking its last
        # word for a surname reads those three firms as 'co', 'co' and 'hall'. Two of
        # them then matched Daniel Elston's soap works, whose occupants line ends '& Co.'
        require = set()
        for p in entry["proprietors"]:
            require |= firm_surnames(p)
        require.discard("")
        committed, tier, evidence = (None, None, None)
        if not entry["outside_plat"]:
            committed, tier, evidence = match_occupant(
                town, require, entry["occupation"], entry["proprietors"])

        if exclusion is not None:
            entry["action"] = "unplaceable"
            entry["action_note"] = ("Excluded from the scene-date town: %s "
                                    "No action; the record is kept so the exclusion can "
                                    "be argued with." % exclusion_note)
        elif entry["outside_plat"]:
            entry["action"] = "unplaceable"
            entry["action_note"] = (
                "The paper puts this business outside the committed town — %s — so no "
                "structure inside it carries the firm and none is built for it. %s"
                % (entry["outside_plat"], entry["anchor"]["note"]))
        elif committed:
            entry["action"] = "enrich_existing"
            entry["action_target"] = committed
            entry["match_tier"] = tier
            entry["match_evidence"] = evidence
            entry["action_note"] = ("%s already stands and its %s carries %s — %r. The "
                                    "papers add trade, goods and dates to a record that "
                                    "exists." % (committed, tier, ", ".join(sorted(require)),
                                                 (evidence or "")[:160]))
        elif entry["anchor"]["kind"] in ("corner", "structure", "business"):
            entry["action"] = "new_building"
            entry["action_target"] = (entry["anchor"]["target"]
                                      or entry["anchor"]["via"]
                                      or "+".join(entry["anchor"]["streets"] or []))
            entry["action_note"] = ("Placeable against the committed town. %s"
                                    % entry["anchor"]["note"])
        elif entry["street_id"]:
            entry["action"] = "street_only"
            entry["action_target"] = entry["street_id"]
            entry["action_note"] = ("The paper names %s and nothing narrower; %s"
                                    % (entry["street"], entry["anchor"]["note"][0].lower()
                                       + entry["anchor"]["note"][1:]))
        else:
            entry["action"] = "unplaceable"
            entry["action_note"] = ("No street the model holds. %s"
                                    % entry["anchor"]["note"])

        if entry["action"] not in BUSINESS_ACTIONS:
            problems.append("%s: action %r is not in the vocabulary" % (b["id"], entry["action"]))
        if entry["action"] in ("enrich_existing", "new_building") and not entry["action_target"]:
            problems.append("%s: a %s action must name its committed target or anchor"
                            % (b["id"], entry["action"]))
        if not entry["present_at_scene_date"] and not entry["exclusion_note"]:
            problems.append("%s: an exclusion must name its contradiction" % b["id"])
        if entry["placement_class"] is None:
            problems.append("%s: no placement class" % b["id"])
        # The three ways a dated anchor history could quietly go back to being two
        # standing placements, which is the defect T-0345 is about.
        ac = entry["anchor_change"]
        if ac:
            live = [w for w in ac["history"] if w["live_at_scene_date"]]
            if len(live) != 1:
                problems.append("%s: %d of this house's anchors are live at the scene "
                                "date — exactly one printed anchor stands on %s, which "
                                "is the whole point of dating the change"
                                % (b["id"], len(live), scene))
            elif live[0]["anchor"] != ac["live_anchor"]:
                problems.append("%s: the live anchor is named %r and the dated history "
                                "makes it %r" % (b["id"], ac["live_anchor"],
                                                 live[0]["anchor"]))
            elif entry["anchor"] not in [r["resolved"] for r in live[0]["readings"]]:
                problems.append("%s: the row resolves its anchor to something no reading "
                                "of the LIVE printing resolves to (%s) — the register "
                                "would be placing this house against a superseded "
                                "printing" % (b["id"], entry["anchor"]["note"]))
            for w in ac["history"]:
                # ONLY THE READINGS THAT PLACE SOMETHING (T-0385). A `street`
                # resolution names a reach and puts no building on the ground — this
                # file says so three times over — so it cannot disagree with a
                # placement about WHERE the house is; it can only be less specific
                # than one. That is the ordinary shape of a group: the readings
                # differ in how much of the sentence the reading pass swept into the
                # anchor field, and one of them swept a street clause in with it.
                # Tuthill King's advertisement is the case — "three doors north of an
                # unread anchor, in Dearborn Street" resolves to the reach of Dearborn
                # and "the Tremont House" to the hotel on it, and refusing that pair
                # would have refused a group for being partly legible. The assertion
                # that matters is untouched: two readings that each PLACE a building
                # must place it in the same spot.
                placed = {(r["resolved"]["kind"], r["resolved"]["target"],
                           r["resolved"]["via"], tuple(r["resolved"]["streets"] or []))
                          for r in w["readings"]
                          if r["resolved"]["kind"] in ("corner", "structure", "business")}
                if len(placed) > 1:
                    problems.append(
                        "%s: the readings grouped under the anchor %r resolve to %d "
                        "different things in the committed town (%s) — they were "
                        "declared one landmark, and one landmark is one place"
                        % (b["id"], w["anchor"], len(placed),
                           ", ".join(sorted(str(x) for x in placed))))
        businesses.append(entry)

    # ---- persons -----------------------------------------------------------
    # The identity key is the gazetteer's own: surname plus forename initials, so
    # 'Cohen, P.' never becomes 'Cohen, J.' here either. A resident whose forename is
    # printed whole and a gazetteer name printed 'P. Cohen' share initials ('p',) and
    # match; two initials against one match only on the leading one, which is what the
    # papers' own abbreviating habit requires.
    resident_by_key = {}
    for r in town["residents"]:
        key = (surname(r["name"] or ""), initials(r["name"] or ""))
        if key[0]:
            resident_by_key.setdefault(key, []).append(r)

    def resident_match(name):
        sn, ini = surname(name), initials(name)
        if not sn:
            return None
        for key, rs in sorted(resident_by_key.items()):
            if key[0] != sn:
                continue
            other = key[1]
            n = min(len(ini), len(other))
            if ini[:n] == other[:n] and (n > 0 or not ini and not other):
                return rs[0]
        return None

    trade_of_person = {}
    for b in gazetteer["businesses"]:
        occ = occupation_of(b.get("trade"))
        if not occ:
            continue
        for p in b.get("proprietors") or []:
            trade_of_person.setdefault(slug(p), occ)

    persons = []
    for p in sorted(gazetteer["persons"], key=lambda x: x["id"]):
        occ = None
        for o in p.get("occupations") or []:
            occ = occupation_of(o)
            if occ:
                break
        occ = occ or trade_of_person.get(slug(p["name"]))
        match = resident_match(p["name"])
        entry = {
            "id": p["id"],
            "name": p["name"],
            "occupation": occ,
            "letter_list_only": bool(p.get("letter_list_only")),
            "first_seen": p.get("first_seen"),
            "last_seen": p.get("last_seen"),
            "action": None,
            "action_target": None,
            "action_note": None,
        }
        if match:
            entry["action"] = "enrich"
            entry["action_target"] = match["person"]
            entry["action_note"] = ("data/residents/ already holds this person as %s "
                                    "(%s, %s). The papers add mentions and dates."
                                    % (match["person"], match["household"], match["grade"]))
        elif occ and occ in town["invented"]:
            entry["action"] = "replace_invented"
            entry["action_target"] = occ
            entry["action_note"] = ("A documented %s. The town invented %d household(s) "
                                    "of this trade because no documented person was "
                                    "available; this is a candidate to retire one."
                                    % (occ, len(town["invented"][occ])))
        else:
            entry["action"] = "new_resident"
            entry["action_note"] = ("Ruling 1: a named person the town does not hold. "
                                    + ("Known only from the post-office letter lists."
                                       if entry["letter_list_only"] else
                                       "Named in a claim other than a letter list."))
        if entry["action"] not in PERSON_ACTIONS:
            problems.append("%s: action %r is not in the vocabulary" % (p["id"], entry["action"]))
        persons.append(entry)

    # ---- counts ------------------------------------------------------------
    def tally(rows, field):
        out = {}
        for r in rows:
            out[r[field] or "none"] = out.get(r[field] or "none", 0) + 1
        return dict(sorted(out.items()))

    present = [b for b in businesses if b["present_at_scene_date"]]
    candidates = {}
    for p in persons:
        if p["action"] == "replace_invented":
            candidates.setdefault(p["action_target"], 0)
            candidates[p["action_target"]] += 1
    # Capped per trade: N documented tailors retire at most the invented tailors held.
    retirable = {t: min(n, len(town["invented"].get(t, [])))
                 for t, n in sorted(candidates.items())}

    counts = {
        "businesses": {
            "total": len(businesses),
            "present_at_scene_date": len(present),
            "excluded": tally([b for b in businesses if b["exclusion"]], "exclusion"),
            "by_action": tally(businesses, "action"),
            "by_placement_class": tally(businesses, "placement_class"),
            "present_by_action": tally(present, "action"),
            "outside_the_plat": sum(1 for b in businesses if b["outside_plat"]),
            "survival_liberty_required": sum(1 for b in present if b["survival_liberty_required"]),
            "backdating_liberty_required": sum(1 for b in present
                                               if b["backdating_liberty_required"]),
            "dissolved_after_scene_date": sum(1 for b in businesses if b["dissolved_after_scene_date"]),
        },
        "persons": {
            "total": len(persons),
            "by_action": tally(persons, "action"),
            "letter_list_only": sum(1 for p in persons if p["letter_list_only"]),
        },
        "invented_residents": {
            "households_by_trade": {k: len(v) for k, v in town["invented"].items()},
            "households_total": sum(len(v) for v in town["invented"].values()),
            "retirable_by_trade": {k: v for k, v in retirable.items() if v},
            "retirable_total": sum(retirable.values()),
        },
    }

    doc = {
        "schema": SCHEMA_VERSION,
        "generated_by": "tools/compile_register.py --build",
        "scene_date": scene,
        "_doc": ("DERIVED, NEVER AUTHORED. Rebuilt from gazetteer.json and the committed "
                 "town by tools/compile_register.py; tools/check.sh refuses a committed "
                 "copy a rebuild would not produce. Edit the gazetteer or the dataset, "
                 "not this file."),
        "compiled_from": {
            "gazetteer": {"claims": gazetteer["counts"]["claims"],
                          "persons": gazetteer["counts"]["persons"],
                          "businesses": gazetteer["counts"]["businesses"]},
            "structures": len(town["structures"]),
            "structures_sharing_a_name": structures_sharing_a_name(town),
            "streets": len({v for v in town["streets"].values()}),
            "resident_persons": len(town["residents"]),
        },
        "counts": counts,
        "businesses": businesses,
        "persons": persons,
    }
    if not quiet:
        print("  ok    %d business(es) → %s" % (len(businesses), counts["businesses"]["by_action"]))
        print("        %d person(s) → %s" % (len(persons), counts["persons"]["by_action"]))
    return doc, problems


# --------------------------------------------------------------------------
# build, check, self-test


def build():
    doc, problems = compile_register(load_json(GAZETTEER), read_town(), quiet=False)
    for p in problems:
        print("  FAIL  " + p, file=sys.stderr)
    if problems:
        return 1
    REGISTER.write_text(dumps(doc), encoding="utf-8")
    print("  wrote %s" % REGISTER.relative_to(REPO))
    return 0


def check():
    bad = []
    if not REGISTER.exists():
        return ["%s is missing — run tools/compile_register.py --build"
                % REGISTER.relative_to(REPO)]
    doc, problems = compile_register(load_json(GAZETTEER), read_town())
    bad.extend(problems)

    committed = REGISTER.read_text(encoding="utf-8")
    if committed != dumps(doc):
        bad.append("%s is not what a rebuild produces — run "
                   "tools/compile_register.py --build and commit the result"
                   % REGISTER.relative_to(REPO))

    # The acceptance clause of T-0262, kept as a gate rather than a claim in a PR:
    # every action names a target where its own kind requires one, and every exclusion
    # names its contradiction. Re-asserted against the COMMITTED file, because that is
    # what the seeding tickets read.
    on_disk = load_json(REGISTER)
    for b in on_disk.get("businesses", []):
        if b["action"] in ("enrich_existing", "new_building") and not b["action_target"]:
            bad.append("%s: %s names no target" % (b["id"], b["action"]))
        if b["exclusion"] and not b["exclusion_note"]:
            bad.append("%s: excluded and says nothing about why" % b["id"])
        if not b["exclusion"] and not b["present_at_scene_date"]:
            bad.append("%s: absent from the scene date with no exclusion" % b["id"])
    for p in on_disk.get("persons", []):
        if p["action"] not in PERSON_ACTIONS:
            bad.append("%s: action %r is not in the vocabulary" % (p["id"], p["action"]))
        if not p["action_note"]:
            bad.append("%s: an action with no note" % p["id"])

    # The two T-0257 fixtures, named in the ticket's acceptance: they resolve to an
    # action with a committed target, or the register says precisely why not. Pinned
    # here so a change that quietly drops them out of the town cannot pass.
    for fixture in ("business_peter_cohen", "business_j_s_c_hogan"):
        row = next((b for b in on_disk["businesses"] if b["id"] == fixture), None)
        if row is None:
            bad.append("%s: the T-0257 fixture is not in the register" % fixture)
            continue
        if not row["action_note"]:
            bad.append("%s: the T-0257 fixture takes an action it does not explain" % fixture)
    if not bad:
        print("  ok    register: %d business(es), %d person(s), %d invented household(s) retirable"
              % (len(on_disk["businesses"]), len(on_disk["persons"]),
                 on_disk["counts"]["invented_residents"]["retirable_total"]))
        ambiguous = [b["id"] for b in on_disk["businesses"]
                     if b["anchor"]["kind"] == "ambiguous"]
        print("  ok    %d committed name(s) are held by more than one structure; an "
              "anchor naming one is refused, not placed (%d today)"
              % (on_disk["compiled_from"]["structures_sharing_a_name"], len(ambiguous)))
    return bad


def self_test():
    """Every assertion above must be capable of firing."""
    town = {
        "structures": [
            {"id": "dole_warehouse_south", "name": "Dole's Warehouse",
             "name_words": [{"dole", "warehouse"}], "aka_head_words": [], "aka_texts": [],
             "occupant_words": {"dole", "forwarder"},
             "occupant_text": "George W. Dole, forwarder", "function": "warehouse",
             "identity_text": "Dole's Warehouse ; George W. Dole, forwarder",
             "occupation": None, "anonymous": False},
            {"id": "wolf_point_tavern", "name": "Wolf Point Tavern",
             "name_words": [{"wolf", "point", "tavern"}, {"taylor", "tavern"}],
             "aka_head_words": [{"taylor", "tavern"}], "aka_texts": ["Taylor's tavern"],
             "occupant_words": {"william", "walters", "landlord"},
             "occupant_text": "William Walters, landlord", "function": "tavern_inn",
             "identity_text": "Wolf Point Tavern ; William Walters, landlord ; Taylor's tavern",
             "occupation": "tavern_keeper", "anonymous": False},
            # T-0386's own case, and it is a real one: ONE advertisement of two
            # buildings to let under one proprietor's name. Nothing distinguishes them
            # but the (east)/(west) disambiguators this project added, so an anchor
            # reading 'John Wright's Building to Let' answers to both.
            {"id": "wright_building_to_let_a", "name": "John Wright's Building to Let",
             "name_words": [{"john", "wright", "building", "let"}],
             "aka_head_words": [], "aka_texts": [], "occupant_words": set(),
             "occupant_text": "", "function": "dwelling_to_let",
             "identity_text": "John Wright's Building to Let",
             "occupation": None, "anonymous": False},
            {"id": "wright_building_to_let_b", "name": "John Wright's Building to Let",
             "name_words": [{"john", "wright", "building", "let"}],
             "aka_head_words": [], "aka_texts": [], "occupant_words": set(),
             "occupant_text": "", "function": "dwelling_to_let",
             "identity_text": "John Wright's Building to Let",
             "occupation": None, "anonymous": False},
            {"id": "recon_1835_north_i2_015", "name": "Reconstructed meeting hall #015",
             "name_words": [{"reconstructed", "meeting", "hall", "015"}],
             "aka_head_words": [], "aka_texts": [], "occupant_words": set(),
             "occupant_text": "", "function": "meeting hall",
             "identity_text": "Reconstructed meeting hall #015",
             "occupation": None, "anonymous": True},
        ],
        "streets": {"south_water": "south_water", "clark": "clark", "lake": "lake"},
        "residents": [{"household": "hh_x", "person": "cohen_peter", "name": "Peter Cohen",
                       "grade": "attested", "occupation": "clothier"},
                      {"household": "hh_inf_baker", "person": "inf_baker_01",
                       "name": "Silas Stiles", "grade": "reconstructed", "occupation": "baker"}],
        "invented": {"baker": ["hh_inf_baker"]},
        "has_creek": False,
    }
    failures = []
    CASES = [0]

    def unit(label, got, want):
        CASES[0] += 1
        if got != want:
            failures.append("%s: got %r, wanted %r" % (label, got, want))

    def case(label, gaz, want):
        CASES[0] += 1
        doc, problems = compile_register(gaz, town)
        if problems:
            failures.append("%s: unexpected problems %r" % (label, problems))
            return None
        got = want(doc)
        if got is not True:
            failures.append("%s: %s" % (label, got))
        return doc

    def gaz(businesses=(), persons=()):
        return {"counts": {"claims": 0, "persons": len(persons), "businesses": len(businesses)},
                "businesses": list(businesses), "persons": list(persons)}

    def biz(bid, **kw):
        b = {"id": bid, "name": kw.get("name", bid), "trade": kw.get("trade"),
             "proprietors": kw.get("proprietors", []), "street": kw.get("street"),
             "goods": [], "placement": kw.get("placement", {"class": "none", "anchor": None}),
             "evidence": {"first_issue": kw.get("first", "1834-01-01"),
                          "last_issue": kw.get("last", "1835-06-01"), "copy_dates": []},
             "contradicted_by": kw.get("contradicted", []),
             "opening_announced": kw.get("announced", []),
             "mentions": [], "built_at_scene_date": True,
             "survival_liberty_required": kw.get("survival", False)}
        if kw.get("anchor_change"):
            b["anchor_change"] = kw["anchor_change"]
        return b

    def refuses(label, gaz, want):
        """A case that must be REFUSED, and on the sentence it is refused with."""
        CASES[0] += 1
        _, problems = compile_register(gaz, town)
        if not any(want in p for p in problems):
            failures.append("%s: expected a refusal mentioning %r, got %r"
                            % (label, want, problems))

    def person(pid, name, **kw):
        return {"id": pid, "name": name, "variants": [], "mentions": [],
                "first_seen": "1835-01-01", "last_seen": "1835-06-01",
                "letter_list_only": kw.get("letter_list_only", False),
                "occupations": kw.get("occupations", []), "associated_places": []}

    # 1. A contradiction BEFORE the scene date excludes; one AFTER does not.
    case("contradiction before the scene date excludes",
         gaz([biz("b1", contradicted=[{"claim": "c#1", "kind": "notice", "issue": "1834-06-11"}])]),
         lambda d: True if d["businesses"][0]["exclusion"] == "contradicted_before_scene_date"
         else "excluded as %r" % d["businesses"][0]["exclusion"])
    case("a dissolution AFTER the scene date leaves the firm standing",
         gaz([biz("b1", street="South Water Street",
                  contradicted=[{"claim": "c#1", "kind": "notice", "issue": "1835-08-08"}])]),
         lambda d: True if (d["businesses"][0]["present_at_scene_date"]
                            and d["businesses"][0]["dissolved_after_scene_date"] == ["c#1"])
         else "present=%r after=%r" % (d["businesses"][0]["present_at_scene_date"],
                                       d["businesses"][0]["dissolved_after_scene_date"]))

    # 2. T-0356. The exclusion reads the paper's own opening notice, and the DATING is
    #    what decides. Every case below was a live reading in the 1835 corpus.
    def opening(dating, iso, claim="c#1", verbatim="will open", note="a reading"):
        return {"claim": claim, "issue": "1835-08-05", "dating": dating, "iso": iso,
                "verbatim": verbatim, "note": note}

    case("a STATED opening after the scene date excludes, and quotes the paper",
         gaz([biz("b1", first="1835-08-05", last="1835-08-05",
                  announced=[opening("stated", "1835-08-14",
                                     verbatim="open a Branch of their House")])]),
         lambda d: True if (d["businesses"][0]["exclusion"] == "opening_announced_after_scene_date"
                            and "1835-08-14" in d["businesses"][0]["exclusion_note"]
                            and "open a Branch of their House" in d["businesses"][0]["exclusion_note"])
         else "excluded as %r, %r" % (d["businesses"][0]["exclusion"],
                                      d["businesses"][0]["exclusion_note"]))
    case("a STATED opening on or before the scene date does not exclude",
         gaz([biz("b1", street="Lake Street", first="1835-08-05", last="1835-08-05",
                  announced=[opening("stated", "1835-06-20")])]),
         lambda d: True if d["businesses"][0]["present_at_scene_date"]
         else "excluded as %r" % d["businesses"][0]["exclusion"])
    case("an EFFECTED opening after the scene date never excludes — it bounds from above",
         gaz([biz("b1", street="Lake Street", first="1835-08-19", last="1835-08-19",
                  announced=[opening("effected", "1835-08-18", verbatim="she has taken a room")])]),
         lambda d: True if (d["businesses"][0]["present_at_scene_date"]
                            and d["businesses"][0]["action"] == "street_only")
         else "excluded as %r" % d["businesses"][0]["exclusion"])
    case("an UNDATED opening decides nothing",
         gaz([biz("b1", street="Lake Street", first="1835-08-05", last="1835-08-05",
                  announced=[opening("undated", None, verbatim="has just opened")])]),
         lambda d: True if d["businesses"][0]["present_at_scene_date"]
         else "excluded as %r" % d["businesses"][0]["exclusion"])
    case("a contradiction before the scene date outranks a stated opening",
         gaz([biz("b1", first="1835-08-05", last="1835-08-05",
                  announced=[opening("stated", "1835-08-14")],
                  contradicted=[{"claim": "c#9", "kind": "notice", "issue": "1834-06-11"}])]),
         lambda d: True if d["businesses"][0]["exclusion"] == "contradicted_before_scene_date"
         else "excluded as %r" % d["businesses"][0]["exclusion"])

    # 2b. THE PROXY IS GONE, and this is the case that proves it: a house whose first
    #     surviving issue is August and whose copy is dated a year earlier stands in the
    #     July town, on no liberty at all. Wm. H. Taylor's boot store, 8 July 1834.
    case("first evidence after the scene date no longer excludes by itself",
         gaz([biz("b1", street="Lake Street", first="1835-08-08", last="1835-08-08")]),
         lambda d: True if (d["businesses"][0]["present_at_scene_date"]
                            and d["businesses"][0]["exclusion"] is None)
         else "excluded as %r" % d["businesses"][0]["exclusion"])
    case("standing on August evidence alone is a backdating liberty",
         gaz([biz("b1", street="Lake Street", first="1835-08-08", last="1835-08-08")]),
         lambda d: True if d["businesses"][0]["backdating_liberty_required"]
         else "backdating_liberty_required=%r" % d["businesses"][0]["backdating_liberty_required"])
    case("an opening dated before the scene date clears the backdating liberty",
         gaz([biz("b1", street="Lake Street", first="1835-08-05", last="1835-08-05",
                  announced=[opening("effected", "1834-07-08",
                                     verbatim="HAS opened an extensive Boot, Shoe and Leather Store")])]),
         lambda d: True if (d["businesses"][0]["present_at_scene_date"]
                            and not d["businesses"][0]["backdating_liberty_required"])
         else "backdating_liberty_required=%r" % d["businesses"][0]["backdating_liberty_required"])
    case("a house documented before the scene date owes no backdating liberty",
         gaz([biz("b1", street="Lake Street", first="1834-05-01", last="1835-06-01")]),
         lambda d: True if not d["businesses"][0]["backdating_liberty_required"]
         else "backdating_liberty_required=%r" % d["businesses"][0]["backdating_liberty_required"])

    # 3. The four actions, each on its own ground.
    case("a committed structure carrying the proprietor takes enrich_existing",
         gaz([biz("b1", proprietors=["George W. Dole"], street="South Water Street")]),
         lambda d: True if (d["businesses"][0]["action"] == "enrich_existing"
                            and d["businesses"][0]["action_target"] == "dole_warehouse_south")
         else "action=%r target=%r" % (d["businesses"][0]["action"],
                                       d["businesses"][0]["action_target"]))
    case("a corner of two platted streets takes new_building",
         gaz([biz("b1", street="South Water Street", placement={
             "class": "corner", "anchor": "the corner of South Water and Clark streets"})]),
         lambda d: True if (d["businesses"][0]["action"] == "new_building"
                            and d["businesses"][0]["anchor"]["streets"] == ["clark", "south_water"])
         else "action=%r anchor=%r" % (d["businesses"][0]["action"], d["businesses"][0]["anchor"]))
    case("a street with no anchor takes street_only",
         gaz([biz("b1", street="Lake Street", placement={"class": "street_only", "anchor": None})]),
         lambda d: True if (d["businesses"][0]["action"] == "street_only"
                            and d["businesses"][0]["action_target"] == "lake")
         else "action=%r target=%r" % (d["businesses"][0]["action"],
                                       d["businesses"][0]["action_target"]))
    case("no street the model holds takes unplaceable",
         gaz([biz("b1", street="Flag Creek", placement={"class": "none", "anchor": None})]),
         lambda d: True if d["businesses"][0]["action"] == "unplaceable"
         else "action=%r" % d["businesses"][0]["action"])

    # 4. The one-hop chain, and that it is only one hop.
    case("a landmark that is another documented business resolves one hop",
         gaz([biz("b1", name="Newberry & Dole", street="South Water Street"),
              biz("b2", street="South Water Street", placement={
                  "class": "relative", "anchor": "Messrs. Newberry & Dole"})]),
         lambda d: True if (d["businesses"][1]["anchor"]["kind"] == "business"
                            and d["businesses"][1]["anchor"]["via"] == "b1")
         else "anchor=%r" % d["businesses"][1]["anchor"])

    # 4a. T-0386. A NAME THE TOWN HOLDS TWICE IS REFUSED, NEVER TIE-BROKEN. The pick
    #     this replaces was `sorted(hits)[0]` — an alphabetical coin toss that the
    #     register then reported as "the landmark is the committed structure X".
    case("an anchor naming TWO committed structures is refused, not placed",
         gaz([biz("b1", street="South Water Street", placement={
             "class": "relative", "anchor": "John Wright's Building to Let"})]),
         lambda d: True if (d["businesses"][0]["anchor"]["kind"] == "ambiguous"
                            and d["businesses"][0]["anchor"]["target"] is None
                            and "wright_building_to_let_a" in d["businesses"][0]["anchor"]["note"]
                            and "wright_building_to_let_b" in d["businesses"][0]["anchor"]["note"]
                            and d["businesses"][0]["action"] == "street_only")
         else "anchor=%r action=%r" % (d["businesses"][0]["anchor"],
                                       d["businesses"][0]["action"]))
    case("…and an anchor naming exactly ONE still places on it",
         gaz([biz("b1", street="Lake Street", placement={
             "class": "relative", "anchor": "Dole's Warehouse"})]),
         lambda d: True if (d["businesses"][0]["anchor"]["kind"] == "structure"
                            and d["businesses"][0]["anchor"]["target"] == "dole_warehouse_south"
                            and d["businesses"][0]["action"] == "new_building")
         else "anchor=%r action=%r" % (d["businesses"][0]["anchor"],
                                       d["businesses"][0]["action"]))
    case("an anchor naming TWO documented businesses is refused on the hop too",
         gaz([biz("b1", name="Newberry & Dole", street="South Water Street"),
              biz("b2", name="Newberry & Dole", street="South Water Street"),
              biz("b3", street="South Water Street", placement={
                  "class": "relative", "anchor": "Messrs. Newberry & Dole"})]),
         lambda d: True if (d["businesses"][2]["anchor"]["kind"] == "ambiguous"
                            and d["businesses"][2]["anchor"]["via"] is None
                            and d["businesses"][2]["action"] == "street_only")
         else "anchor=%r action=%r" % (d["businesses"][2]["anchor"],
                                       d["businesses"][2]["action"]))
    unit("the town's exposure is counted, not asserted",
         structures_sharing_a_name(town), 1)

    # 4b. The guards on enrich_existing, each on the case that forced it.
    case("a firm style in `proprietors` yields its PARTNERS, not its '& Co.'",
         gaz([biz("b1", proprietors=["H. Doty & Co."], street="Lake Street")]),
         lambda d: True if d["businesses"][0]["action"] != "enrich_existing"
         else "matched %r on a firm suffix" % d["businesses"][0]["action_target"])
    case("two spelled-out forenames must match whole, not by initial",
         gaz([biz("b1", proprietors=["Georgina Dole"], street="Lake Street")]),
         lambda d: True if d["businesses"][0]["action"] != "enrich_existing"
         else "Georgina matched George's warehouse")
    case("an abbreviated forename still matches a spelled-out one",
         gaz([biz("b1", proprietors=["G. W. Dole"], street="Lake Street")]),
         lambda d: True if d["businesses"][0]["action_target"] == "dole_warehouse_south"
         else "target=%r" % d["businesses"][0]["action_target"])
    case("an aka matches only when the trades agree",
         gaz([biz("b1", proprietors=["E. Taylor"], trade="boots and shoes",
                  street="Lake Street")]),
         lambda d: True if d["businesses"][0]["action"] != "enrich_existing"
         else "a boot store matched %r" % d["businesses"][0]["action_target"])
    case("…and it does match when they do",
         gaz([biz("b1", proprietors=["E. Taylor"], trade="tavern", street="Lake Street")]),
         lambda d: True if (d["businesses"][0]["action"] == "enrich_existing"
                            and d["businesses"][0]["match_tier"] == "aka")
         else "action=%r tier=%r" % (d["businesses"][0]["action"],
                                     d["businesses"][0]["match_tier"]))
    case("an anonymous reconstructed roof is never an enrich_existing target",
         gaz([biz("b1", proprietors=["Amos Hall"], street="Lake Street")]),
         lambda d: True if d["businesses"][0]["action"] != "enrich_existing"
         else "matched the invented roof %r" % d["businesses"][0]["action_target"])
    case("a reach of a platted street resolves as a street, not as a failure",
         gaz([biz("b1", street="South Water Street", placement={
             "class": "relative", "anchor": "the east end of South Water-street"})]),
         lambda d: True if (d["businesses"][0]["anchor"]["kind"] == "street"
                            and d["businesses"][0]["action"] == "street_only")
         else "anchor=%r action=%r" % (d["businesses"][0]["anchor"]["kind"],
                                       d["businesses"][0]["action"]))

    # 4c. THE DATED ANCHOR CHANGE (T-0345). A house whose printed anchor changed on a
    # date carries ONE live placement and the superseded ones as dated history; the
    # guards below are the three ways that could go back to being two standing
    # placements, which is the defect the ticket is about.
    def reading(a, first, last):
        return {"anchor": a, "class": "relative", "first_issue": first,
                "last_issue": last, "claims": ["c#%s" % a],
                "placement": {"class": "relative", "anchor": a}}

    def window(name, live, readings, first="1834-01-01", last="1834-06-01"):
        return {"anchor": name, "why": None, "first_issue": first, "last_issue": last,
                "readings": [reading(a, first, last) for a in readings],
                "claims": ["c#%s" % a for a in readings], "live_at_scene_date": live,
                "placement": {"class": "relative", "anchor": readings[0]}}

    def history(*windows, **kw):
        return {"rule": "the anchor changed", "cannot_say": "which side of it moved",
                "live_anchor": kw.get("live_anchor", "the hotel"),
                "live_reason": "the later of the two, printed before the scene date",
                "changes": [], "history": list(windows)}

    case("a superseded anchor is resolved and kept, and does not place the house",
         gaz([biz("b1", street="Lake Street",
                  placement={"class": "relative", "anchor": "the hotel"},
                  anchor_change=history(
                      window("Wolf Point Tavern", False, ["Wolf Point Tavern"]),
                      window("the hotel", True, ["the hotel"],
                             "1834-09-10", "1834-12-10")))]),
         lambda d: True if (
             d["businesses"][0]["anchor_change"]["history"][0]["resolved"]["target"]
             == "wolf_point_tavern"
             and d["businesses"][0]["anchor"]["kind"] == "unresolved"
             and d["businesses"][0]["action"] == "street_only")
         else "superseded=%r live=%r action=%r"
              % (d["businesses"][0]["anchor_change"]["history"][0]["resolved"],
                 d["businesses"][0]["anchor"], d["businesses"][0]["action"]))
    case("an anchor printed four ways resolves on the reading that resolves best",
         gaz([biz("b1", street="Lake Street",
                  placement={"class": "relative", "anchor": "the hotel"},
                  anchor_change=history(
                      window("Wolf Point Tavern", False,
                             ["Wolf Point Tavern, on Main-street", "Wolf Point Tavern"]),
                      window("the hotel", True, ["the hotel"],
                             "1834-09-10", "1834-12-10")))]),
         lambda d: True if (
             d["businesses"][0]["anchor_change"]["history"][0]["resolved_on_reading"]
             == "Wolf Point Tavern")
         else "resolved on %r"
              % d["businesses"][0]["anchor_change"]["history"][0]["resolved_on_reading"])
    refuses("two anchors live at the scene date is two standing placements",
            gaz([biz("b1", street="Lake Street",
                     placement={"class": "relative", "anchor": "the hotel"},
                     anchor_change=history(
                         window("Wolf Point Tavern", True, ["Wolf Point Tavern"]),
                         window("the hotel", True, ["the hotel"])))]),
            "are live at the scene date")
    refuses("the named live anchor must be the one the dates make live",
            gaz([biz("b1", street="Lake Street",
                     placement={"class": "relative", "anchor": "the hotel"},
                     anchor_change=history(
                         window("Wolf Point Tavern", True, ["Wolf Point Tavern"]),
                         window("the hotel", False, ["the hotel"])))]),
            "the dated history makes it")
    refuses("the row may not place the house on a superseded printing",
            gaz([biz("b1", street="Lake Street",
                     placement={"class": "relative", "anchor": "Wolf Point Tavern"},
                     anchor_change=history(
                         window("Dole's Warehouse", False, ["Dole's Warehouse"]),
                         window("the hotel", True, ["the hotel"])))]),
            "no reading of the LIVE printing resolves to")
    refuses("readings called one landmark may not resolve to two",
            gaz([biz("b1", street="Lake Street",
                     placement={"class": "relative", "anchor": "the hotel"},
                     anchor_change=history(
                         window("the tavern", False,
                                ["Wolf Point Tavern", "Dole's Warehouse"]),
                         window("the hotel", True, ["the hotel"])))]),
            "one landmark is one place")
    # …but a reading that places NOTHING cannot disagree with one that does (T-0385).
    # A street clause swept into the anchor field resolves to a reach, and a group is
    # allowed to be partly legible.
    case("a street reach in a group does not contradict the placement in it",
         gaz([biz("b1", street="Lake Street",
                  placement={"class": "relative", "anchor": "Wolf Point Tavern"},
                  anchor_change=history(
                      window("Wolf Point Tavern", True,
                             ["Wolf Point Tavern", "an unread anchor in Lake Street"],
                             "1834-01-01", "1835-06-01"),
                      live_anchor="Wolf Point Tavern"))]),
         lambda d: True if (d["businesses"][0]["anchor"]["target"] == "wolf_point_tavern"
                            and d["businesses"][0]["action"] == "new_building")
         else "anchor=%r action=%r" % (d["businesses"][0]["anchor"],
                                       d["businesses"][0]["action"]))
    # 4c. T-0355 — the two readings that put a Flag Creek tavern in a Wolf Point stable.
    # First the occupants line that caused it, read directly, because the town fixture
    # above supplies `occupant_words` ready-made and cannot exercise the clause filter.
    unit("a clause dated to another year is not a scene-date occupant",
         scene_date_occupants("the tavern's keeper of the day \u2014 Elijah Wentworth in "
                              "1831, William Walters on the scene date"),
         "the tavern's keeper of the day; William Walters on the scene date")
    unit("a clause stating no year is kept whole",
         scene_date_occupants("William Walters, landlord"), "William Walters; landlord")
    unit("a range that covers the scene date is kept",
         scene_date_occupants("William Walters 1833-1836"), "William Walters 1833-1836")
    unit("a two-digit range takes its century from its own head",
         scene_date_occupants("Eliza Chappel and her infant school, 1833-34"),
         "Eliza Chappel and her infant school")
    unit("a year range is one span, not two loose years",
         year_spans("1833-34 and 1836"), [(1833, 1834), (1836, 1836)])

    # 4d. T-0385 — the disambiguator this project adds to a name, and the anchor no
    # printing carries it in. Nine cases. The fourth is the guard, and since T-0386 it
    # is expressed the way the register now expresses every ambiguity: TWO hits, which
    # `resolve_anchor` refuses in writing, rather than a silent None.
    def named(*records):
        """A fixture town of `(id, *names)` records, indexed the way read_town does."""
        return {"structures": [
            {"id": r[0], "name": r[1],
             "name_words": [set(words(n)) for n in r[1:] if words(n)],
             "undisambiguated_words": [set(words(u)) for u in
                                       (undisambiguated(n) for n in r[1:])
                                       if u and words(u)]}
            for r in records]}

    tremont = named(("tremont_house_1", "Tremont House (the first)", "Tremont House I",
                     "the old Tremont House"))
    unit("an anchor the record disambiguates still reaches it",
         match_landmarks(tremont, set(words("the Tremont House"))), ["tremont_house_1"])
    unit("and the record's own disambiguated name reaches it exactly as before",
         match_landmarks(tremont, set(words("the old Tremont House"))),
         ["tremont_house_1"])
    unit("an exact match is never given up for a relaxed one",
         match_landmarks(named(("a", "Tremont House"), ("b", "Tremont House (the second)")),
                         set(words("the Tremont House"))), ["a"])
    unit("two houses one ordinal apart are BOTH returned, for resolve_anchor to refuse",
         match_landmarks(named(("a", "Tremont House (the first)"), ("b", "Tremont House II")),
                         set(words("the Tremont House"))), ["a", "b"])
    unit("the relaxation reaches nothing on an unrelated name",
         match_landmarks(tremont, set(words("the Mansion House"))), [])
    # AND THE THREE IT MUST NOT REACH: `first` and `old` inside a name are the source's
    # own words, not this project's editorial suffix, and striking them would invent an
    # anchor. Each of these was a live false positive on the first cut of this rule.
    unit("a congregation's own name is not a disambiguator",
         match_landmarks(named(("temple_building", "the First Baptist meeting house")),
                         set(words("the Baptist meeting house"))), [])
    unit("a historical superlative is not a disambiguator",
         match_landmarks(named(("hogan_store", "Chicago's first post office")),
                         set(words("the post office"))), [])
    unit("nor is an age the source itself prints in the middle of a name",
         match_landmarks(named(("x", "the log store at Lake and South Water")),
                         set(words("the store at Lake and South Water"))), [])
    unit("undisambiguated() leaves a name nobody disambiguated alone",
         undisambiguated("the First Baptist meeting house"), None)

    # Then the guard the fault generalises to: the firm's own record says where it is.
    case("a distance in miles refuses every match into the committed town",
         gaz([biz("b1", proprietors=["George W. Dole"], street="Lake Street", placement={
             "class": "relative", "anchor": "thirteen miles south of Chicago"})]),
         lambda d: True if (d["businesses"][0]["action"] == "unplaceable"
                            and d["businesses"][0]["outside_plat"])
         else "action=%r outside=%r" % (d["businesses"][0]["action"],
                                        d["businesses"][0]["outside_plat"]))
    case("a road leading out of town refuses it too",
         gaz([biz("b1", proprietors=["George W. Dole"], placement={
             "class": "relative", "anchor": "the road from Chicago leading to Ottawa"})]),
         lambda d: True if d["businesses"][0]["action"] == "unplaceable"
         else "action=%r target=%r" % (d["businesses"][0]["action"],
                                       d["businesses"][0]["action_target"]))
    case("a named creek in the firm's own name refuses it, placement or no placement",
         gaz([biz("b1", name="E. Wentworth's tavern, Flag Creek",
                  proprietors=["George W. Dole"])]),
         lambda d: True if (d["businesses"][0]["action"] == "unplaceable"
                            and "Flag Creek" in d["businesses"][0]["outside_plat"])
         else "action=%r outside=%r" % (d["businesses"][0]["action"],
                                        d["businesses"][0]["outside_plat"]))
    case("a firm the papers do NOT put out of town still enriches",
         gaz([biz("b1", proprietors=["George W. Dole"], street="Lake Street")]),
         lambda d: True if (d["businesses"][0]["action"] == "enrich_existing"
                            and d["businesses"][0]["outside_plat"] is None)
         else "action=%r outside=%r" % (d["businesses"][0]["action"],
                                        d["businesses"][0]["outside_plat"]))

    # 5. The identity policy is the gazetteer's, imported and not re-invented.
    case("a resident already held takes enrich",
         gaz(persons=[person("p1", "P. Cohen")]),
         lambda d: True if (d["persons"][0]["action"] == "enrich"
                            and d["persons"][0]["action_target"] == "cohen_peter")
         else "action=%r target=%r" % (d["persons"][0]["action"], d["persons"][0]["action_target"]))
    case("a different forename initial NEVER matches a resident",
         gaz(persons=[person("p1", "J. Cohen")]),
         lambda d: True if d["persons"][0]["action"] == "new_resident"
         else "action=%r" % d["persons"][0]["action"])
    case("a documented baker is a candidate to retire the invented one",
         gaz(persons=[person("p1", "Amos Thing", occupations=["baker"])]),
         lambda d: True if (d["persons"][0]["action"] == "replace_invented"
                            and d["persons"][0]["action_target"] == "baker")
         else "action=%r target=%r" % (d["persons"][0]["action"], d["persons"][0]["action_target"]))
    case("a letter-list name still mints a resident, flagged",
         gaz(persons=[person("p1", "Obadiah Nobody", letter_list_only=True)]),
         lambda d: True if (d["persons"][0]["action"] == "new_resident"
                            and d["persons"][0]["letter_list_only"])
         else "action=%r flag=%r" % (d["persons"][0]["action"], d["persons"][0]["letter_list_only"]))

    # 6. The retirement count is capped by what the town actually invented.
    case("three documented bakers retire ONE invented baker household",
         gaz(persons=[person("p%d" % i, "%s Baker%d" % (n, i), occupations=["baker"])
                      for i, n in enumerate(("Amos", "Ezra", "Silas"), start=1)]),
         lambda d: True if d["counts"]["invented_residents"]["retirable_total"] == 1
         else "retirable=%r" % d["counts"]["invented_residents"]["retirable_total"])

    # 7. Determinism: the same inputs twice, byte for byte.
    g = gaz([biz("b1", proprietors=["George W. Dole"], street="Lake Street")],
            [person("p1", "P. Cohen")])
    if dumps(compile_register(g, town)[0]) != dumps(compile_register(g, town)[0]):
        failures.append("determinism: two compiles of one input differ")

    for f in failures:
        print("  FAIL  " + f, file=sys.stderr)
    if not failures:
        print("  ok    %d self-test case(s)" % CASES[0])
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.build:
        return build()
    if args.self_test:
        return self_test()
    bad = check()
    for b in bad:
        print("  FAIL  " + b, file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
