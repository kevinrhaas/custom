#!/usr/bin/env python3
"""Documented people take the reconstructed roofs the register matched (T-0264).

    python3 tools/replace_invented_residents.py           write
    python3 tools/replace_invented_residents.py --check   re-derive and diff
    python3 tools/replace_invented_residents.py --report  the deal and every refusal

WHAT THIS IS FOR.

The town holds 113 households raised because the trade census demanded them and
no documented person was available to fill them. Every one carries an invented
name and a `name_basis` block saying so. `data/research/newspapers/
register_1835.json` now names, per trade, the documented people the papers put in
Chicago — `action: replace_invented` is exactly the register's finding that a
trade the town INVENTED a household for has a documented practitioner. This is
the pass that spends that finding: the documented man takes the roof, the
invented name is retired, and the card shows a real person with a newspaper
citation where it showed an invention.

WHAT THE ROOF KEEPS, AND WHY THE GRADE IS `inferred` AND NOT `attested`.

The PERSON becomes documented; the HOUSEHOLD does not. Nothing says where any of
these men slept, and the dwelling under them is still the reconstruction's — its
existence, its position and its footprint are unchanged and still conjectural.
`inferred` is this vocabulary's word for exactly that: a real person carrying
reconstructed details, with a note saying which details and from what. Grading
them `attested` would claim the dwelling as well as the man, which is the one
thing this pass must not do. docs/LIBERTIES.md L205 owns the placement.

THE DEAL, AND THE SIX REFUSALS THAT SHAPE IT.

The register's candidate list is a compilation and not a nomination: it ranks by
trade and it does not ask whether a name is a man, whether he is already in this
town, or whether he was anywhere near it. Dealing it unguarded would have put a
partnership on a roof as a household head, minted a second John T. Temple, and
moved Bernardus Laughton off the Aux Plaines into the North Division. So a
candidate is REFUSED, and the refusal printed with its reason, when:

  1. `garbled`            — the transcription bracketed the name as uncertain.
                            'A CLY BOUR:' is not somebody's name.
  2. `a firm, not a person` — 'Pierce & Abbott', 'Matthias Mason & Co.',
                            'Johnson & Stevens'. A firm cannot head a household;
                            it is a BUSINESS, and the businesses are T-0263's.
  3. `first evidence after the scene date` — AGENTS.md rule 3. A man first
                            printed on 1835-08-15 is not put in the town of
                            1 July 1835 on the strength of it.
  4. `placed somewhere in particular` — the gazetteer gives him a street, a named
                            house, or a place outside the town. A documented
                            address is EVIDENCE ABOUT WHERE HE WAS, and moving him
                            onto whichever reconstructed roof this deal happened
                            to reach would contradict his own record. Those people
                            belong to the placement tickets (T-0263, T-0306), which
                            put them where the paper puts them. The people this
                            pass takes are the ones the papers place nowhere: for
                            them a reconstructed dwelling is not a contradiction,
                            it is the honest answer to a question no source
                            answers.
  5. `already named in the town` — his surname already appears, capitalised, in a
                            committed structure record, household record or the
                            exclusions. The dataset has something to say about
                            that name already, and a pass that plants him on a
                            reconstructed roof would be answering a question that
                            is already open somewhere else. Deliberately blunt and
                            deliberately over-cautious: a wrongly refused
                            candidate costs a roof, a wrongly accepted one mints
                            a second copy of a real man.
  6. `spoken for by a placeable business` — the register carries a BUSINESS under
                            the same surname that it can put somewhere: an
                            `enrich_existing`, a `new_building` or a `street_only`
                            action. Those are the storefront tickets' to place,
                            and a man cannot be given a reconstructed dwelling in
                            one division while the same pass of work is standing
                            his shop in another. A business the register calls
                            `unplaceable` spoken for nobody and does not refuse.
  7. `surname already dealt` — one surname, one roof. A shared surname reads as
                            kinship and this pass claims none; it is also how the
                            same man under two printed forms ('D. Graves' and
                            'Graves, D.') would otherwise take two roofs.

Candidates that survive are ranked by evidence — mentions first, then earliest
appearance, then id — and paired with that trade's invented roofs in id order.
Everything is deterministic: no randomness, no date, no hand-picked list.

WHAT THIS FILE WILL NOT DO. It will not upgrade a confidence to fill a roof, it
will not cite a claim the gazetteer does not carry, and it will not deal a
candidate past a refusal. A trade whose candidates are all refused keeps its
invented household, and `--report` says which refusal took each one.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import fronting_street  # noqa: E402  (after the path insert, as plat_corridors does)

DATA = ROOT / "data"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
REGISTER = DATA / "research" / "newspapers" / "register_1835.json"
GAZETTEER = DATA / "research" / "newspapers" / "gazetteer.json"
STRUCTURES = DATA / "structures"
EXCLUSIONS = DATA / "exclusions.json"

SCENE_DATE = "1835-07-01"
PREFIX = "hh_inf_"

# The two runs, as they are registered in data/sources/. A claim id carries its
# issue; the SOURCE is the run, which is what every other record in this dataset
# cites and what carries the transcription-mediated standard (the owner's second
# ruling, 2026-08-28) in its own `repository` and `rights_note`.
PAPERS = (("chicago_democrat_", "chicago_democrat_1833_1835"),
          ("chicago_american_", "chicago_american_1835"))

# The two roofs a reconstructed household stands on, and the word each one is
# called by in a refusal or a note. An advertised address is about the second.
ROLES = {"works_at": "shop", "lives_at": "dwelling"}

TITLES = {"dr", "mr", "mrs", "jr", "sr", "esq", "capt", "col", "maj", "rev", "messrs"}
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


def surname(name: str) -> str:
    """The family name, lowercased, from either order the papers print.

    The corpus sets a man as 'S. Lincoln' in one column and 'Lincoln, S.' in the
    letter list two pages later, so the position of the family name is a property
    of the COLUMN and not of the name. A comma is the tell and it is the paper's
    own: reversed forms are printed reversed for alphabetising.
    """
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
        return name
    head, _, tail = name.partition(",")
    tail = tail.strip()
    return f"{tail} {head.strip()}" if tail else head.strip()


def issue_of(claim_id: str) -> str:
    """'chicago_democrat_1834_06_11#c003' → '11 June 1834, column 3'."""
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


# ---------------------------------------------------------------------------
# what the town already names
# ---------------------------------------------------------------------------

def town_surnames() -> set[str]:
    """Every capitalised word the committed dataset already uses as a name.

    Read from the structure records, the household records and the exclusions —
    prose included, because the reason to refuse a candidate is that this project
    has ALREADY said something about that name, and most of what it has said
    lives in a research note rather than in a `name` field.
    """
    known: set[str] = set()
    # NOT the reconstructed households. Their names are this layer's own
    # inventions and guard nothing, and once this pass has written a documented
    # name into one of them, reading it back would refuse that man on the next
    # run as "already named in the town" — a guard that poisons itself and makes
    # --check pass against any tree at all.
    files = (list(STRUCTURES.glob("*.json"))
             + [p for p in HOUSEHOLDS.glob("*.json") if not p.name.startswith(PREFIX)])
    if EXCLUSIONS.exists():
        files.append(EXCLUSIONS)
    for path in files:
        text = path.read_text(encoding="utf-8")
        for word in re.findall(r"\b[A-Z][a-z]{2,}\b", text):
            known.add(word.lower())
    return known


def invented_roofs(docs: dict) -> dict:
    """Trade → the households whose head carries an INVENTED name, in id order.

    `name_basis` is the marker and not the grade: a person may be graded
    `reconstructed` and still be a real person the dataset knows under a
    designation. Only a name the invented-name pools produced is this pass's to
    retire.
    """
    roofs: dict = {}
    for path in sorted(docs, key=lambda p: p.name):
        doc = docs[path]
        if not doc.get("id", "").startswith(PREFIX):
            continue
        for person in doc.get("persons", []):
            if "name_basis" not in person:
                continue
            trade = (person.get("occupation") or {}).get("value")
            if trade:
                roofs.setdefault(trade, []).append((path, doc, person))
    return roofs


# ---------------------------------------------------------------------------
# the deal
# ---------------------------------------------------------------------------

def household_fronts(docs: dict) -> dict:
    """Which committed street each invented household's two roofs FRONT.

    T-0367. `tools/fronting_street.py` asks the geometry: a roof fronts the street
    its facade bearing looks into, within the reach that module states. It is read
    here for one reason — a documented man the papers put on a named street can only
    take a reconstructed household that stands on THAT street, and until this pass
    could ask, every one of them was refused.

    BOTH ROOFS, not the dwelling alone. What the papers print is an ADDRESS OF
    BUSINESS: Montgomery made boots on South Water, Botsford's store was at the
    corner of Dearborn and Lake. A household carries a `works_at` as well as a
    `lives_at`, and it is the workplace that such a line is about. Requiring the
    dwelling to be the match would refuse a man whose shop the reconstruction had
    already put on his own street, which is the opposite of this ticket.

    The answer is not evidence about either roof. Where they stand is the
    reconstruction's arrangement and stays conjectural; what the question buys is
    that the arrangement can now be HONOURED rather than contradicted.
    """
    roofs = [r for rs in invented_roofs(docs).values() for r in rs]
    wanted = sorted({(doc.get(role) or {}).get("value")
                     for _path, doc, _person in roofs for role in ROLES
                     if (doc.get(role) or {}).get("value")})
    return {sid: (front or {}).get("street")
            for sid, front in fronting_street.table(ids=wanted).items()}


def deal(docs: dict):
    """Pair documented candidates with invented roofs. Returns (pairs, refusals)."""
    register = load(REGISTER)
    gazetteer = {p["id"]: p for p in load(GAZETTEER)["persons"]}
    known = town_surnames()
    roofs = invented_roofs(docs)
    lanes = fronting_street.streets()
    fronts = household_fronts(docs)

    pairs, refusals = [], []
    # One surname, one roof, ACROSS the whole deal and not merely within a trade:
    # a shared surname reads as kinship and this pass claims none.
    taken: set[str] = set()
    for trade in sorted(roofs):
        # THE POOL SURVIVES ITS OWN EFFECT. The register is compiled FROM the
        # committed town, so the moment this pass seats a man on a roof the
        # register stops calling him `replace_invented` and starts calling him
        # `enrich` — he is in the town now, and the compiler is right about that.
        # Reading only `replace_invented` would therefore make the deal
        # unre-derivable the run after it lands: the candidate that won would
        # have vanished from the pool that chose him, and `--check` would report
        # drift on a tree nobody had touched. So an `enrich` whose target is a
        # person on a RECONSTRUCTED roof of this trade is read back into the pool
        # as what it is — this pass's own previous answer. The `occupation` test
        # is what keeps the sixteen name-coincidence matches out: an enrich with
        # no trade matched an INVENTED name and says nothing about a tradesman.
        candidates = [p for p in register["persons"]
                      if p.get("action") == "replace_invented"
                      and p.get("action_target") == trade]
        candidates += [p for p in register["persons"]
                       if p.get("action") == "enrich"
                       and p.get("occupation") == trade
                       and str(p.get("action_target") or "").startswith("inf_")]
        candidates.sort(key=lambda p: (-len(gazetteer[p["id"]]["mentions"]),
                                       p["first_seen"], p["id"]))
        # A MAN IS PLACED BY ANY OF HIS PRINTINGS, not only by the one this loop
        # is looking at. 'P. J. Carli' carries no place and 'P. S. Carli' is at
        # the Eagle Tavern; they are one publican, and dealing the first onto a
        # reconstructed roof in the North Division while the second stands in a
        # named house on Lake Street would be two answers to one question. So the
        # placements are collected per SURNAME first and every form of the name
        # is held to them.
        spoken_for: dict[str, str] = {}
        for biz in register["businesses"]:
            if biz.get("action") not in ("enrich_existing", "new_building", "street_only"):
                continue
            for word in re.findall(r"\b[A-Za-z]{3,}\b", biz.get("name") or ""):
                spoken_for.setdefault(word.lower(),
                                      f"{biz['name']}, {biz['action']}")

        placed: dict[str, list[str]] = {}
        for other in candidates:
            where = [p for p in (gazetteer[other["id"]].get("associated_places") or [])
                     if p.strip().lower() not in BARE_TOWN]
            key = surname(other["name"])
            if key and where:
                for place in where:
                    if place not in placed.setdefault(key, []):
                        placed[key].append(place)

        # THE ROOFS OF THIS TRADE, AND THE STREET EACH OF THEM STANDS ON. The
        # street is the roof's own geometry (see `dwelling_fronts`); a roof that
        # fronts no committed street — the north-division clusters are most of
        # them — can still take a man the papers place nowhere, and can never
        # take one they place somewhere.
        free = list(roofs[trade])
        roof_street = {id(roof): {role: fronts.get((roof[1].get(role) or {}).get("value"))
                                  for role in ROLES}
                       for roof in free}
        stood = sorted({lanes[s]["name"] for r in free
                        for s in roof_street[id(r)].values() if s})

        settled, hopefuls = [], []
        for cand in candidates:
            name, gaz = cand["name"], gazetteer[cand["id"]]
            sur = surname(name)
            own = [pl for pl in (gaz.get("associated_places") or [])
                   if pl.strip().lower() not in BARE_TOWN]
            kin = [pl for pl in placed.get(sur, []) if pl not in own]
            reason = None
            if UNCERTAIN.search(name):
                reason = "garbled"
            elif FIRM.search(name):
                reason = "a firm, not a person"
            elif cand["first_seen"] > SCENE_DATE:
                reason = "first evidence after the scene date"
            elif not sur:
                reason = "no surname the corpus prints"
            if reason:
                refusals.append((trade, cand["id"], name, reason, "person"))
                continue
            if own:
                hopefuls.append((cand, gaz, own))
            elif kin:
                # HIS OWN PRINTINGS SAY NOTHING, AND ANOTHER OF HIS SURNAME DOES.
                # The street rule below is only ever run on a man's OWN record,
                # which is what the ticket asks and what the evidence supports: a
                # firm advertising as 'Pierce and Abbott' at Canal and Lake is not
                # Titus H. Abbott's record, and using it to choose his roof would
                # place a man on the strength of a shared surname. It is still
                # enough to REFUSE him — the asymmetry is deliberate, and it is
                # the same one everywhere in this pass: a doubt costs a roof, it
                # never buys one.
                refusals.append((trade, cand["id"], name,
                                 f"another printing of this surname is placed somewhere "
                                 f"in particular ({'; '.join(kin)}), and his own "
                                 f"printings name no street a roof could be matched to",
                                 "person"))
            else:
                settled.append((cand, gaz))

        # THE PLACED MEN GO FIRST, and it is not a courtesy. A man the papers put
        # on a street can take exactly the roofs of his trade that stand on it —
        # often one, frequently none — while a man they place nowhere can take
        # any of them. Dealing the unconstrained half first would let it spend
        # the one roof the constrained half could have used, and the deal would
        # refuse a documented address to keep an arbitrary pairing.
        #
        # THEY ARE ALSO NOT ASKED WHETHER A BUSINESS SPEAKS FOR THEM. That
        # refusal (`spoken_for`, below) exists because a man cannot be given a
        # reconstructed dwelling in one division while the storefront tickets
        # stand his shop in another — the objection is the CONTRADICTION, not the
        # shop. Seating him on his own printed street is the thing that removes
        # it: T-0263 and T-0306 will stand Botsford's store at Dearborn and Lake,
        # and a Lake Street roof is where a Lake Street grocer belongs. What the
        # street rule may never do is seat him ANYWHERE ELSE, and it does not.
        for cand, gaz, own in hopefuls:
            sur = surname(cand["name"])
            wanted, unreadable = [], []
            for place in own:
                ids, unknown = fronting_street.named_streets(place, lanes)
                wanted += [s for s in ids if s not in wanted]
                unreadable += [u for u in unknown if u not in unreadable]
            printed = "; ".join(own)
            if not wanted:
                extra = (f"; '{unreadable[0]} street' is printed here and the town had "
                         f"two of them, so the phrase does not say which (T-0305)"
                         if unreadable else "")
                refusals.append((trade, cand["id"], cand["name"],
                                 f"placed somewhere in particular ({printed}) and no "
                                 f"committed street of this town is named in it{extra}",
                                 "no_street"))
                continue
            names = ", ".join(lanes[s]["name"] for s in wanted)
            # A MAN WHOSE SHOP IS ALREADY SPOKEN FOR DOES NOT ALSO GET THE TRADE'S
            # INVENTED SHOP. The register carries a business under his surname that
            # T-0263/T-0306 can place, so standing him behind the reconstruction's
            # own shop of that trade would give one man two shops on one street. A
            # DWELLING is different and stays open to him: he has only one of those,
            # nothing else in this project is standing it, and a roof on the street
            # he advertised from agrees with his shop instead of duplicating it.
            usable = [r for r in ROLES
                      if not (r == "works_at" and sur in spoken_for)]
            match, role = None, None
            for roof in free:
                hit = next((r for r in usable if roof_street[id(roof)][r] in wanted), None)
                if hit:
                    match, role = roof, hit
                    break
            if match is None:
                shopless = ("; his own shop is spoken for by a placeable business "
                            f"({spoken_for[sur]}), so only a dwelling was open to him"
                            if sur in spoken_for else "")
                stands = (f"the dwellings and shops of the {len(free)} invented "
                          f"{trade.replace('_', ' ')} household(s) still free front "
                          f"{', '.join(stood)}" if stood else
                          f"neither the dwellings nor the shops of the invented "
                          f"{trade.replace('_', ' ')} household(s) front a committed "
                          f"street at all")
                refusals.append((trade, cand["id"], cand["name"],
                                 f"his record puts him on {names} ({printed}) and no "
                                 f"invented roof of this trade stands there — "
                                 f"{stands}{shopless}", "no_roof"))
                continue
            # A ROOF ON HIS STREET IS FREE, AND THESE TWO STILL OUTRANK IT. The
            # street answers WHERE; neither of these is a question about where.
            if sur in known:
                refusals.append((trade, cand["id"], cand["name"],
                                 f"already named in the town ({sur}) — a roof of his "
                                 f"trade does front {names}, but this dataset has that "
                                 f"name open somewhere else and the placement tickets "
                                 f"own it", "masked"))
                continue
            if sur in taken:
                refusals.append((trade, cand["id"], cand["name"],
                                 "surname already dealt", "masked"))
                continue
            free.remove(match)
            taken.add(sur)
            pairs.append((match, cand, gaz, trade,
                          {"street": lanes[roof_street[id(match)][role]]["name"],
                           "roof": ROLES[role], "printed": printed,
                           "wanted": [lanes[s]["name"] for s in wanted]}))

        for cand, gaz in settled:
            sur = surname(cand["name"])
            if sur in spoken_for:
                # The register carries a BUSINESS under this surname that it can
                # put somewhere, and nothing in this man's own printings says
                # where he was — so any roof this deal reached for could be in
                # the wrong division from his own shop. The placed half above is
                # the case where the papers answer that; this is the case where
                # they do not.
                refusals.append((trade, cand["id"], cand["name"],
                                 f"spoken for by a placeable business "
                                 f"({spoken_for[sur]}) and placed nowhere this deal "
                                 f"could match it to", "person"))
                continue
            if sur in known:
                refusals.append((trade, cand["id"], cand["name"],
                                 f"already named in the town ({sur})", "person"))
                continue
            if sur in taken:
                refusals.append((trade, cand["id"], cand["name"],
                                 "surname already dealt", "person"))
                continue
            if not free:
                refusals.append((trade, cand["id"], cand["name"],
                                 "no invented roof of this trade left to take",
                                 "person"))
                continue
            taken.add(sur)
            pairs.append((free.pop(0), cand, gaz, trade, None))
    return pairs, refusals


# ---------------------------------------------------------------------------
# the records
# ---------------------------------------------------------------------------

def rewrite(doc: dict, person: dict, cand: dict, gaz: dict, trade: str,
            placement: dict | None = None) -> None:
    name = display(cand["name"])
    sources = paper_for(gaz["mentions"])
    cited = "; ".join(issue_of(c) for c in gaz["mentions"][:6])
    more = ("" if len(gaz["mentions"]) <= 6
            else f", and {len(gaz['mentions']) - 6} further mention(s)")
    printed = sorted({v["as_printed"] for v in gaz.get("variants") or []})
    trades = ", ".join(gaz.get("occupations") or [trade.replace("_", " ")])
    family = surname(cand["name"]).title()

    person["name"] = name
    person["grade"] = "inferred"
    person["sources"] = list(sources)
    person.pop("name_basis", None)
    person["note"] = (
        f"A DOCUMENTED MAN ON A RECONSTRUCTED ROOF. The papers name him and this "
        f"household's dwelling does not: what is attested is the person and his "
        f"trade, and what remains the reconstruction's is everything about where "
        f"he lived. He is printed as "
        + ", ".join(f"'{p}'" for p in printed)
        + f" and the corpus reads his trade as {trades}. Cited at {cited}{more}. "
        f"THIS ROOF DID NOT COME FROM HIS RECORD. The household was raised by the "
        f"occupation census because the town of 3,265 people in 398 dwellings "
        f"needed a {trade.replace('_', ' ')} and no documented one was available; "
        f"the register (data/research/newspapers/register_1835.json, action "
        f"`replace_invented`) is what says one now is. The dwelling's existence, "
        f"position and footprint are unchanged and still conjectural, and nothing "
        f"here claims he slept in it — only that the town's need for this trade is "
        f"met by a man the papers name rather than by one this project invented. "
        f"The invented name this record used to carry, and its name_basis block, "
        f"are retired: an invented name is not kept beside a documented one. "
        f"No figure is drawn (docs/LIBERTIES.md L1); the placement is L205. "
        + (
            f"HIS OWN RECORD NAMES THE STREET, AND THE ROOF IS ON IT. The corpus "
            f"places him at {placement['printed']}, so he could take no roof of "
            f"this trade but one standing on "
            f"{' or '.join(placement['wanted'])}; the dwelling he now heads "
            f"fronts {placement['street']}, which is why it and not another of "
            f"the trade's roofs. WHICH STREET A RECONSTRUCTED ROOF FRONTS IS "
            f"THIS PROJECT'S ARRANGEMENT AND NOT EVIDENCE ABOUT THE BUILDING: it "
            f"is derived from the roof's committed facade bearing and footprint "
            f"by tools/fronting_street.py, not read out of a note, and it is used "
            f"here only to keep the deal from contradicting the advertisement. "
            f"Nothing claims this is the house he advertised from, or a house at "
            f"all; what is claimed is that a man printed on this street is not "
            f"housed off it. "
            if placement else
            f"He is placed nowhere in particular by his own record, which is one "
            f"way to take a reconstructed roof — the other is to be placed on a "
            f"street a roof of his trade already fronts (T-0367), and this "
            f"record is not that case. "
        )
        + f"READ THROUGH A TRANSCRIPTION, not a scan: the owner's ruling of "
        f"2026-08-28 grades a transcription-mediated reading as documented, and "
        f"the source record for the run states that standard and its limits. A "
        f"scan read that confirms or corrects the name upgrades this entry."
    )
    occ = person.get("occupation") or {}
    occ["confidence"] = "attested"
    occ["sources"] = list(sources)
    occ["note"] = (
        f"THE TRADE IS THE PAPER'S, NOT THE CENSUS'S. The corpus reads him as "
        f"{trades}, at {cited}{more}. This record used to carry the occupation "
        f"census's argument for the trade instead — that a town of this size "
        f"needs so many of them — which is why the household exists; it is no "
        f"longer why this man holds the trade. Where the corpus prints more than "
        f"one trade for him, they are all recorded here and the household's is "
        f"the one the register matched."
    )
    person["occupation"] = occ

    # BOTH TRUTHS IN ONE LINE, and the second one is not decoration: the card
    # prints the head's own grade chip directly under this label, so a label
    # naming a tier the chip contradicts is the K23a fault in the other
    # direction. "a documented cooper" is what changed and "inferred at this
    # roof" is what did not — he is documented as a man and inferred as this
    # household's head. tools/smoke_renderer.mjs PART 3 asserts the two agree.
    doc["name"] = (f"The {family} household — a documented "
                   f"{trade.replace('_', ' ')}, inferred at this roof "
                   f"({doc.get('division', '')} division)")

    # The arrival bound is now the paper's rather than the scene date's. The
    # household used to say `not_later_than 1835-07-01` and explain that nothing
    # dates a hypothesised household; something dates this man.
    doc["arrival"] = {
        "value": cand["first_seen"],
        "confidence": "inferred",
        "sources": list(sources),
        "note": (
            f"A BOUND FROM THE PAPER, NOT AN ARRIVAL. The corpus first prints him "
            f"at {issue_of(gaz['mentions'][0])}, so he is in the town's paper by "
            f"{cand['first_seen']} and at no stated time before it; nothing "
            f"reached says when he came. The household used to carry the scene "
            f"date as its bound, because nothing dated a hypothesised household — "
            f"this is the same claim made against evidence instead of against the "
            f"date the town is being counted on. Last printed "
            f"{cand['last_seen']}."),
        "precision": "not_later_than",
    }
    if placement:
        lives = doc.get("lives_at") or {}
        lives["note"] = (lives.get("note", "").rstrip() + " WHY THIS ROOF AND NOT "
                         f"ANOTHER OF THE TRADE'S (T-0367): the papers place "
                         f"{name} at {placement['printed']}, and of this trade's "
                         f"invented roofs this is one that fronts "
                         f"{placement['street']} — derived from the roof's own "
                         f"facade bearing and footprint by tools/fronting_street.py. "
                         f"The choice is between roofs this project had already "
                         f"placed; it moved nothing and it is not a claim that he "
                         f"lived here.")
        doc["lives_at"] = lives
    doc["research_note"] = (
        doc.get("research_note", "").rstrip()
        + f"\n\nRETIRED AN INVENTED NAME (T-0264). This household was raised by "
        f"the occupation census and named from the invented-name pools. The "
        f"newspaper register matched it to {name}, a documented "
        f"{trade.replace('_', ' ')} the corpus names {len(gaz['mentions'])} "
        + (f"time(s) and places at {placement['printed']}; of this trade's "
           f"invented roofs, this one fronts {placement['street']}, so seating "
           f"him here honours the printed address instead of contradicting it "
           f"(T-0367). He now holds the roof. "
           if placement else
           f"time(s) and places nowhere in particular, and he now holds the roof. ")
        + f"What changed is WHO: the argument for the household, its dwelling and "
        f"its position are untouched and still the reconstruction's, and the "
        f"person's grade is `inferred` — a real man with reconstructed details — "
        f"rather than `attested`, which would claim the dwelling too. "
        f"tools/replace_invented_residents.py derives this deal and prints every "
        f"candidate it refused."
    )


def build(preload: dict | None = None):
    docs = ({p: json.loads(t) for p, t in preload.items()} if preload is not None
            else {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))})
    index_text = None
    if preload is not None and INDEX in preload:
        index_text = preload[INDEX]
        docs.pop(INDEX, None)
    house_docs = {p: d for p, d in docs.items() if p.name.startswith("hh_")}

    pairs, refusals = deal(house_docs)
    files = {}
    for (path, doc, person), cand, gaz, trade, placement in pairs:
        rewrite(doc, person, cand, gaz, trade, placement)
        files[path] = dumps(doc, 1)

    # The manifest's denormalised copies, which validate.py holds equal to the
    # records: the grade tallies move when a person's grade does, and the hh_inf_
    # rows are written by the household programme with a hardcoded
    # {"reconstructed": n} that this pass has just made untrue.
    index = json.loads(index_text) if index_text is not None else load(INDEX)
    changed = {doc["id"]: doc for (_p, doc, _pn), *_rest in pairs}
    for row in index["households"]:
        doc = changed.get(row["id"])
        if not doc:
            continue
        tally: dict = {}
        for person in doc["persons"]:
            tally[person["grade"]] = tally.get(person["grade"], 0) + 1
        row["grades"] = dict(sorted(tally.items()))
    totals = {"attested": 0, "inferred": 0, "reconstructed": 0}
    for row in index["households"]:
        for grade, n in row["grades"].items():
            totals[grade] = totals.get(grade, 0) + n
    index["counts"]["by_grade"] = totals
    files[INDEX] = dumps(index, 1)
    return files, pairs, refusals


def overlay(files: dict) -> dict:
    """Apply this pass to an in-memory {path: text} map and hand it back.

    The third stage of the household pipeline — build, then name, then replace —
    called by tools/generate_inferred_households.py --check for the same reason
    it calls the naming pass: a drift report that compares a midpoint against the
    tree cries wolf on every run.
    """
    out = dict(files)
    replaced, _pairs, _refusals = build(preload={p: t for p, t in files.items()})
    out.update({p: t for p, t in replaced.items() if p in files or p == INDEX})
    return out


def report(pairs, refusals, invented: int | None = None) -> None:
    seated = [p for p in pairs if p[4]]
    print(f"THE DEAL — {len(pairs)} invented name(s) retired, {len(seated)} of them "
          f"on the street the man's own record names")
    for (_path, doc, person), cand, gaz, trade, placement in pairs:
        where = (f"  <- {placement['printed']} -> fronts {placement['street']}"
                 if placement else "")
        print(f"  {doc['id']:34s} {trade:14s} -> {person['name']:24s} "
              f"({cand['id']}, {len(gaz['mentions'])} mention(s), "
              f"{cand['first_seen']}..{cand['last_seen']}){where}")
    if invented is not None:
        print(f"\n  INVENTED HEAD NAMES — {invented} before this pass, "
              f"{invented - len(pairs)} after")
    # THE PLACEMENT REFUSALS, BEFORE AND AFTER (T-0367's fourth acceptance clause).
    # "Before" is not a remembered number. Every candidate below whose kind is not
    # `person` is one the papers put somewhere in particular, and before this pass
    # could read a place, being placed was the WHOLE of the refusal for all of them.
    # So the two counts are one population read twice, and the fourth kind is the
    # finding: for some of these men the placement refusal was standing in front of
    # a refusal that has nothing to do with where they were.
    kinds = {kind: [r for r in refusals if r[4] == kind]
             for kind in ("no_roof", "no_street", "masked")}
    placed = len(seated) + sum(len(v) for v in kinds.values())
    print(f"\n  THE PLACED MEN — the papers put {placed} candidate(s) somewhere in "
          f"particular, and before T-0367 the deal could not read a place, so being "
          f"placed was the whole of the refusal for every one of them. Now:")
    print(f"      {len(seated):3d}  seated on a roof of their own trade fronting "
          f"their own street")
    print(f"      {len(kinds['no_roof']):3d}  refused because no invented roof of "
          f"their trade stands on the street their record names")
    print(f"      {len(kinds['no_street']):3d}  refused because the phrase names no "
          f"committed street of this town")
    print(f"      {len(kinds['masked']):3d}  refused for a reason that is not about "
          f"placement at all, which the old refusal was standing in front of")
    print(f"  The placement refusals therefore fall from {placed} to "
          f"{len(kinds['no_roof']) + len(kinds['no_street'])}, and the deal seats "
          f"{len(seated)}.")
    print(f"\nREFUSED — {len(refusals)} candidate(s), with the reason")
    for trade, cid, name, reason, _kind in refusals:
        print(f"  {trade:14s} {name[:34]:36s} {reason}")


def pipeline_input() -> dict:
    """The households as the two passes BEFORE this one derive them.

    Not the committed tree. This pass is not idempotent against its own output —
    it retires the `name_basis` block that tells it which roofs are invented, so
    re-reading the tree after a write finds nothing to do and a --check built
    that way would pass on any tree whatever, including a hand-edited one. The
    honest input is the same one the household pipeline uses: the programme's own
    output, named, and then dealt.
    """
    import importlib.util
    def _load(name):
        spec = importlib.util.spec_from_file_location(
            name, pathlib.Path(__file__).with_name(f"{name}.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    programme = _load("generate_inferred_households")
    gen_names = _load("generate_inferred_names")
    files, _records, _households = programme.build_all()
    files = gen_names.overlay(files)
    return {p: t for p, t in files.items()
            if p.name.startswith("hh_") or p == INDEX}


def _invented_count() -> int:
    """How many household heads carry an invented name BEFORE this pass runs."""
    files = pipeline_input()
    docs = {p: json.loads(text) for p, text in files.items() if p.name.startswith("hh_")}
    return sum(len(rs) for rs in invented_roofs(docs).values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and report any drift without writing")
    ap.add_argument("--report", action="store_true",
                    help="print the deal and every refusal")
    args = ap.parse_args()

    files, pairs, refusals = build(preload=pipeline_input())
    if args.report:
        report(pairs, refusals, invented=_invented_count())
        return 0
    if args.check:
        drift = [p for p, text in files.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        for p in drift:
            print(f"   DRIFT: {p.relative_to(ROOT)}")
        if drift:
            print(f"   {len(drift)} file(s) differ from what this pass derives")
            return 1
        print(f"   OK: {len(pairs)} documented resident(s) hold the roofs this pass "
              f"deals them, {len(refusals)} candidate(s) refused")
        return 0

    for p, text in files.items():
        p.write_text(text, encoding="utf-8")
    print(f"retired {len(pairs)} invented name(s); refused {len(refusals)} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
