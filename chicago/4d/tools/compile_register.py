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

TWO EXCLUSIONS, AND THE SECOND ONE IS THE TICKET'S CLAUSE REBUILT OUT OF WHAT THE
DATA ACTUALLY CARRIES. T-0262 asks to exclude "entries whose only 1835 evidence
`announces_opening` after Jul 1". There is no `announces_opening` in the claim
vocabulary — the ticket describes a field the extraction schema never grew — so the
derivable test is the one that answers the same question without inventing one: a
business whose FIRST issue is after the scene date has no evidence whatever that it
stood on 1 July, and is excluded as `first_evidence_after_scene_date`. That is
conservative in the direction provenance wants. It is also not a claim that the
business was absent, so the register keeps every one of them, with the exclusion
named, for a later pass that can read an opening notice properly.

WHAT AN ACTION MEANS, for the seeding tickets that consume this:

  enrich_existing  a committed structure already carries this business, matched on the
                   proprietors' surnames. The town needs a fuller record, not a roof.
  new_building     nothing committed carries it AND the paper's own placement resolves
                   against the committed town — a corner of two platted streets, or a
                   landmark that is a committed structure, or one hop through another
                   documented business that is. Placeable; T-0263's queue.
  street_only      documented and placeable no further than a street face. The paper
                   named a street this town has, and nothing narrower.
  unplaceable      no street the model holds. Recorded, not buildable.

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
EXCLUSIONS = ("contradicted_before_scene_date", "first_evidence_after_scene_date")

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
    # this corpus was being compiled as a MILLER (T-0372) — Elmira Fowler, who
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
    town = {"structures": [], "streets": {}, "residents": [], "invented": {}}

    for path in sorted(Path(structures_dir).glob("*.json")):
        d = load_json(path)
        names = [d.get("name") or ""] + list(d.get("aka") or [])
        occ = (d.get("occupants") or {}).get("value") or ""
        function = (d.get("function") or {}).get("value")
        town["structures"].append({
            "id": d["id"],
            "name": d.get("name"),
            "name_words": [set(words(n)) for n in names if words(n)],
            "aka_head_words": [set(words(head_of(n))) for n in names[1:] if words(head_of(n))],
            "occupant_words": set(words(occ)),
            "occupant_text": occ,
            "aka_texts": [head_of(n) for n in names[1:]],
            "identity_text": " ; ".join([d.get("name") or "", occ]
                                        + [head_of(n) for n in names[1:]]),
            "function": function,
            "occupation": occupation_of((function or "").replace("_", " ")),
            "anonymous": d["id"].startswith(("recon_", "inf_")),
        })

    for s in load_json(streets_file).get("streets", []):
        town["streets"][street_key(s["name_1835"])] = s["id"]
        town["streets"][s["id"]] = s["id"]

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


def match_landmark(town, anchor_words):
    """The committed structure an anchor NAMES, or None.

    Whole-set equality, not containment: an anchor is only a landmark when it is the
    same set of identity-bearing words as a record's name or aka. Containment would put
    'the store' on the first store in the town.
    """
    hits = [s["id"] for s in town["structures"]
            if anchor_words and any(anchor_words == pool for pool in s["name_words"])]
    return sorted(hits)[0] if hits else None


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

    Four outcomes, and the note on each says which one and why, because the seeding
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
        sid = match_landmark(town, anchor_words)
        if sid:
            return {"kind": "structure", "target": sid, "streets": None, "via": None,
                    "note": "The landmark is the committed structure %s." % sid}
        # One hop: the landmark is another documented business.
        for other_id, other in by_firm:
            if other_id == business["id"]:
                continue
            if other and anchor_words and set(words(other)) == anchor_words:
                return {"kind": "business", "target": None, "streets": None,
                        "via": other_id,
                        "note": "The landmark is another documented business (%s), which "
                                "places this one exactly as well as that one is placed."
                                % other_id}
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
        elif first > scene:
            exclusion = "first_evidence_after_scene_date"
            exclusion_note = ("The earliest issue carrying this business is %s, after the "
                              "scene date, so nothing evidences it standing on %s."
                              % (first, scene))

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
            "survival_liberty_required": bool(b.get("survival_liberty_required")) and exclusion is None,
            "anchor": resolve_anchor(town, b, by_firm),
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
        committed, tier, evidence = match_occupant(
            town, require, entry["occupation"], entry["proprietors"])

        if exclusion is not None:
            entry["action"] = "unplaceable"
            entry["action_note"] = ("Excluded from the scene-date town: %s "
                                    "No action; the record is kept so the exclusion can "
                                    "be argued with." % exclusion_note)
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
            "survival_liberty_required": sum(1 for b in present if b["survival_liberty_required"]),
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
    }
    failures = []
    CASES = [0]

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
             "mentions": [], "built_at_scene_date": True,
             "survival_liberty_required": kw.get("survival", False)}
        return b

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

    # 2. First evidence after the scene date excludes, and says so.
    case("first evidence after the scene date excludes",
         gaz([biz("b1", first="1835-08-08", last="1835-08-08")]),
         lambda d: True if (d["businesses"][0]["exclusion"] == "first_evidence_after_scene_date"
                            and "1835-08-08" in d["businesses"][0]["exclusion_note"])
         else "excluded as %r" % d["businesses"][0]["exclusion"])

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
