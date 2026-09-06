#!/usr/bin/env python3
"""Synthesize completed resident research into the evidence-only 1835 population.

T-0487..T-0490.  Write with no arguments; `--check` validates the committed
invariants.  The 1840 census is retained as later evidence and never silently
back-projected into the 1835 scene.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

# T-0838.  `--drift` runs this writer against a throwaway copy of the tree and compares,
# so the copy needs to be able to tell the tool where its data lives.  Set by `--drift`
# on the subprocess it spawns and by nothing else; a bare run resolves as it always did.
ROOT = Path(os.environ["SYNTH_SCRATCH_ROOT"]) if os.environ.get("SYNTH_SCRATCH_ROOT") \
    else Path(__file__).resolve().parents[1]
# The DATA root is overridable (above); the tools directory is NOT — it is where this
# file lives. Deriving the import path from ROOT instead breaks `--drift`, whose scratch
# copy carries data and no tools: measured, ModuleNotFoundError on rebuild_resident_index.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rebuild_resident_index import rebuild  # noqa: E402  (the manifest's one owner)

CHICAGO = ROOT.parent
REPO = CHICAGO.parent
DATA = ROOT / "data"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
STRUCTURES = DATA / "structures"
RESEARCH = DATA / "research" / "residents"
REFERENCE = CHICAGO / "reference" / "resident-research"
CENSUS_DIR = CHICAGO / "reference" / "census1840" / "validation"
CENSUS_CSV = CENSUS_DIR / "H_1840_chicago_with_names_partial.csv"
SITE = REPO / "site" / "chicago" / "4d"
PROGRAMME = DATA / "reconstruction" / "1835_inferred_household_programme.json"
LEDGER = RESEARCH / "synthesis_2026_09_02.json"
SUMMARY = ROOT / "docs" / "RESEARCH" / "resident-household-synthesis-2026-09-02.md"
CENSUS_SOURCE = DATA / "sources" / "census_1840_chicago_name_crosswalk.json"
DRIFT_BASELINE = RESEARCH / "synthesis_drift_baseline.json"
PROJECTED = "projected_resident"

# Every note prefix this tool has ever written, stripped repeatedly before the current
# one is applied.  The `--check` step re-derives this file, so a re-run must land on the
# same bytes; the earlier single-pass strip knew only the short corroborated prefix and
# stacked a second copy of the long one's second sentence on every pass (T-0491).
NOTE_PREFIXES = re.compile(
    r"^(?:INDEPENDENTLY CORROBORATED RESIDENT\. "
    r"|PROJECTED RESIDENT\. Documented in Chicago post-office evidence but not "
    r"independently corroborated strongly enough for attested circa-1835 residence\. "
    r"|Originally documented in Chicago post-office evidence; independent resident "
    r"research now corroborates the identity\. "
    r"|GRADED BY THE OWNER'S RATIFIED LADDER.*?\(T-0822\)\. )", re.I)


# T-0822 — THE LADDER SUPERSEDES THIS FILE'S LETTER-LIST RULE, and the reason is the one
# `mint_civic_residents.py` already gives for declining in the other direction.
#
# This pass grades a `letter_list_only` person out of ONE corpus: the resident-research
# CSVs under reference/resident-research.  No row there means the research found nothing
# it could tie to the name — a documented no-find in THAT corpus, and not a finding about
# the poll lists, the militia enrolments or the press.  The owner's grading ladder,
# ratified 2026-09-03 and applied by `mint_civic_residents.py --regrade` (T-0515, T-0699),
# reads seven domains; where a rung fires it writes it onto the card as
# `resident_research.rule` + `regraded_on`, with the rows it read in `civic_evidence` and
# `press_evidence`.
#
# So this pass was demoting 62 grades the ladder had ruled on, using evidence it had not
# read: 17 people back to `inferred` and all 62 back to `projected_resident`, on cards the
# cohort being run had nothing to do with.  Every cohort ticket in the programme had to
# notice the reversion and undo it by hand before it could merge — T-0508 did it twice —
# which is a trap and not a workflow.  The grade and the note on those 17 cards said
# opposite things in the meantime, and a reader got whichever the card showed first.
#
# `mint_civic_residents.py` already declines the mirror image of this: it will not
# downgrade a person carrying an adjudicated `resident_research` outcome, because "a rung
# fired on the evidence it could see is not a finding about the evidence it could not",
# and because "the synthesis would put the grade straight back".  The deference was
# one-directional, and that asymmetry was the bug.  It is mutual now — neither tool
# overturns a grade the other has explicitly ruled on, and the beaten rule is recorded on
# the card rather than left to be rediscovered.
#
# WHAT STILL CROSSES THE LINE, both ways: NEW evidence.  A corroborated research outcome
# is a second reading the ladder never made, so it still promotes a ladder-graded person
# to `attested`.  Only the DEMOTION defers.
def ladder_ruled(person):
    """Has the owner's ratified ladder ruled on this identity's grade?

    True only for the stamp `apply_regrade` writes when a rung actually FIRED. A
    declined downgrade writes `resident_research.refusals` and no stamp, so it is
    not a ruling on the grade and this pass is free to grade as it always did.
    """
    rr = person.get("resident_research") or {}
    return bool(rr.get("regraded_on") and rr.get("rule"))


def ladder_prefix(person):
    """The note that says which rule won and which one was beaten (T-0822)."""
    rr = person.get("resident_research") or {}
    return (f"GRADED BY THE OWNER'S RATIFIED LADDER — rule {rr.get('rule')}, applied "
            f"{rr.get('regraded_on')}. This identity is {person.get('grade')} because that "
            f"rung fired on the civic and press rows recorded on this card, which the "
            f"resident-research corpus does not read. This programme's letter-list rule of "
            f"2026-09-02 would call it a projected resident on the absence of a research "
            f"row; it is superseded here, and a no-find in one corpus is not a finding "
            f"about another (T-0822). ")


RETIREMENT_NOTE = "T-0489: reconstructed occupancy retired; evidence-based person retained and unplaced."

# T-0516 — THE BUILDINGS HALF OF THE SAME RULING, two days late.
#
# The owner's ask of 2026-09-03: "when you remove a reconstructed resident, make sure
# that if there is a structure you already made for them, you can abandon that structure
# or remove it because we will want to do a sweep later and assign these residents a
# place to live and work". Asked which, he ruled: "Keep as anonymous stock."
#
# T-0489 did the people half and marked the stock `unassigned`, and stopped there. The
# 31 roofs the inferred-household layer RAISED went on declaring
# `reconstruction.status: "inferred_household"` — a status the schema defines as "a roof
# the inferred-household layer raised BECAUSE an argued household needed somewhere to be,
# and it carries an occupants block naming that household" — while naming households no
# file has held since 2 September. Every gate that classifies a roof by its layer went on
# crediting them to a programme with no people in it.
#
# So this is where they enrol as anonymous stock, next to the `resident_assignment` the
# same ruling wrote, because a retirement that leaves half the record behind is the fault
# it was written to fix. No geometry is touched: the roof is the same roof, at the same
# point, on the same footprint. What changes is what the record CLAIMS.
RETIRED_ROOF_PHASE = "phase2_inferred_households"
RETIRED_ROOF_OCCUPANTS = {
    "value": "Anonymous stock; no occupant is claimed",
    "confidence": "reconstructed",
    "note": ("ANONYMOUS STOCK (T-0516). This roof was raised by the inferred-household "
             "programme because an argued household needed somewhere to be; the owner "
             "retired that reconstructed resident population on 2026-09-02 and ruled the "
             "geometry kept - \"keep as anonymous stock\" - so the household this roof "
             "was raised for no longer exists and nobody is claimed to be here. It is "
             "unassigned until the later placement sweep, and it is counted as one of "
             "the anonymous count-units of the 665-roof programme. THE ROOF'S OWN "
             "EXISTENCE, POSITION AND FOOTPRINT REMAIN CONJECTURAL and are unchanged by "
             "the retirement: what was withdrawn is the occupant, not the building. The "
             "trade it was raised for is kept in `reconstruction.occupation` and in this "
             "record's own name, because that is what the placement sweep works from; "
             "the argument that raised it is kept as history in "
             "data/reconstruction/1835_inferred_household_programme.json."),
}


def retire_roof(doc):
    """Enrol one raised household roof in the anonymous stock, or leave it alone.

    Returns True when this record was one of the 31. Keyed on the programme phase and
    not on the status, so it is idempotent: a roof already enrolled is recognised as
    this layer's and re-asserted rather than skipped by a status test that has already
    flipped. `inventory_class` and `sequence` are NOT written - an anonymous roof dealt
    by a parcel carries its place in that deal, and these were authored one at a time
    against the occupation census, so there is no place to record. Minting one would
    invent a position in a deal that never dealt them; the schema carries the exception
    rather than the data carrying a fiction.
    """
    block = doc.get("reconstruction") or {}
    if block.get("programme_phase") != RETIRED_ROOF_PHASE:
        return False
    block["status"] = "inferred_anonymous"
    doc["reconstruction"] = block
    doc["occupants"] = dict(RETIRED_ROOF_OCCUPANTS)
    return True


def note_once(text, sentence):
    """Append `sentence` to a note exactly once, however many runs have appended it.

    Straight concatenation grew the note by one sentence on every re-run, and the gate
    re-derives this file, so five passes left five copies (T-0491).
    """
    kept = re.sub(r"\s{2,}", " ", (text or "").replace(sentence, "")).strip()
    return (kept + " " + sentence).strip()


def strip_note_prefixes(text):
    """Remove every leading prefix this tool writes, however many have accumulated."""
    while True:
        stripped = NOTE_PREFIXES.sub("", text, count=1)
        if stripped == text: return text
        text = stripped

CORROBORATED = {"corroborated", "corroborated_enrichment"}
CANDIDATE = {"candidate", "candidate_identity"}
RANK = {"no_corroboration_yet": 0, "no_corroboration": 0,
        "candidate": 1, "candidate_identity": 1,
        "corroborated": 2, "corroborated_enrichment": 2}
ABBR = {"wm": "william", "chas": "charles", "jas": "james", "jno": "john",
        "geo": "george", "thos": "thomas", "benj": "benjamin", "saml": "samuel",
        "nathl": "nathaniel", "natl": "nathaniel", "danl": "daniel",
        "edwd": "edward", "robt": "robert"}
OCCUPATIONS = [
    (r"dry[- ]goods", "dry_goods_merchant"),
    (r"forwarding|commission", "forwarding_and_commission"),
    (r"blacksmith", "blacksmith"), (r"shoemaker|bootmaker|boots? and shoes?", "shoemaker"),
    (r"carpenter", "carpenter"), (r"joiner", "joiner"), (r"brick ?maker", "brickmaker"),
    (r"mason", "mason"), (r"plasterer", "plasterer"), (r"tailor", "tailor"),
    (r"saddler", "saddler"), (r"cooper", "cooper"), (r"baker", "baker"),
    (r"butcher", "butcher"), (r"physician|doctor", "physician"),
    (r"attorney|lawyer", "attorney"), (r"printer", "printer"), (r"editor", "editor"),
    (r"surveyor", "surveyor"), (r"postmaster", "postmaster"),
    (r"minister|clergyman", "minister"), (r"priest", "priest"),
    (r"schoolteacher|teacher", "schoolteacher"), (r"merchant", "merchant"),
    (r"grocer", "grocer"), (r"druggist", "druggist"), (r"auctioneer", "auctioneer"),
    (r"farmer", "farmer"), (r"labou?rer", "labourer"), (r"teamster", "teamster"),
    (r"clerk", "clerk"), (r"seaman|sailor", "seaman"), (r"boatman", "boatman"),
    (r"trader", "trader")]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, doc, indent=1):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")


def value(block):
    return block.get("value") if isinstance(block, dict) else block


def ids(text):
    return [x.strip() for x in re.split(r"[;,]", text or "") if x.strip()]


def name_key(name):
    words = re.findall(r"[a-z]+", re.sub(r"\[[^\]]*\]", "", name or "").lower())
    titles = {"mr", "mrs", "miss", "dr", "rev", "capt", "col", "maj", "esq", "jr", "sr"}
    return " ".join(ABBR.get(w, w) for w in words if w not in titles)


def source_doc(sid):
    path = DATA / "sources" / f"{sid}.json"
    try: return load(path) if path.exists() else {}
    except Exception: return {}


def findings():
    out = {}
    for path in sorted(RESEARCH.glob("*findings.json")):
        try: doc = load(path)
        except Exception: continue
        ticket = doc.get("ticket") or path.stem
        default = doc.get("default_outcome") or "no_corroboration_yet"
        overrides = doc.get("overrides") or {}
        for pid in doc.get("completed_person_ids") or []:
            item = dict(overrides.get(pid) or {})
            item.setdefault("outcome", default)
            item.setdefault("summary", doc.get("default_summary"))
            item["ticket"] = ticket; item["reviewed_on"] = doc.get("reviewed_on")
            old = out.get(pid)
            if old is None or RANK.get(item["outcome"], 0) >= RANK.get(old.get("outcome"), 0):
                out[pid] = item
    return out


def research_rows():
    out = findings()
    for path in sorted(REFERENCE.glob("T-*/*_resident_research.csv")):
        try:
            rows = csv.DictReader(path.open(newline="", encoding="utf-8-sig"))
            for row in rows:
                pid = (row.get("person_id") or "").strip()
                if not pid: continue
                item = dict(out.get(pid) or {})
                outcome = (row.get("outcome") or item.get("outcome") or "no_corroboration_yet").strip()
                if RANK.get(outcome, 0) >= RANK.get(item.get("outcome"), 0):
                    item.update({"outcome": outcome, "ticket": path.parent.name,
                        "name_transcribed": (row.get("name_transcribed") or "").strip(),
                        "name_normalized": (row.get("name_normalized") or "").strip(),
                        "stratum": (row.get("stratum") or "").strip(),
                        "candidate_ids": ids(row.get("candidate_ids") or ""),
                        "proposed_facts": (row.get("proposed_facts") or "").strip(),
                        "evidence_for": (row.get("evidence_for") or "").strip(),
                        "evidence_against": (row.get("evidence_against") or "").strip(),
                        "sources": ids(row.get("source_ids") or ""),
                        "source_urls_tiers": (row.get("source_urls_tiers") or "").strip(),
                        "queries": (row.get("queries") or "").strip(),
                        "reviewed_on": (row.get("access_date") or item.get("reviewed_on") or "").strip(),
                        "notes": (row.get("notes") or "").strip()})
                    out[pid] = item
        except Exception:
            continue
    for item in out.values():
        if item.get("sources"):
            item["sources"] = [s for s in item["sources"] if s not in FINDING_AIDS]
    return out


def research_block(item):
    block = {"programme": "resident-research-2026", "ticket": item.get("ticket"),
             "outcome": item.get("outcome"), "reviewed_on": item.get("reviewed_on"),
             "asserted_identity": item.get("outcome") in CORROBORATED}
    for src, dst in (("proposed_facts","proposed_facts"),("evidence_for","evidence_for"),
                     ("evidence_against","evidence_against"),("summary","summary"),
                     ("notes","notes"),("sources","source_ids"),("candidate_ids","candidate_ids")):
        if item.get(src): block[dst] = item[src]
    if item.get("candidates"): block["candidates"] = item["candidates"]
    return block


# T-0837.  A FINDING AID IS NOT A SOURCE FOR A PERSON, and this writer was carrying one
# onto cards.  `read_newberry_index.py` states the rule and gates it: the Newberry
# genealogical index is a 1960 finding aid, "the whole failure mode of an index is that a
# surname in it looks like evidence", and its id may not appear anywhere under
# data/residents.  The research CSVs legitimately record it — a reader consulted it, and
# saying so is how the next reader knows the shelf was looked at — but `research_block`
# copies a row's `source_ids` onto the card verbatim, so thirteen cards in the standing
# spend cited it and the Newberry gate would have gone red the moment they landed.  The
# id is dropped where the rows are READ, so neither the card's citation list nor a
# promotion's `sources` can carry it.
FINDING_AIDS = {"newberry_genealogical_index"}


def independent(item):
    return [s for s in item.get("sources") or []
            if s not in {"chicago_democrat_1833_1835", "chicago_american_1835"}]


def item_text(item):
    """Only what the research pass itself wrote about THIS person."""
    return " ".join([item.get("proposed_facts") or "", item.get("evidence_for") or "",
                     item.get("summary") or ""])


def evidence_text(item):
    bits = [item_text(item)]
    for sid in independent(item):
        doc = source_doc(sid)
        bits += [str(doc.get(k) or "") for k in ("citation","locator","note","describes_date")]
    return " ".join(bits)


SCENE_YEAR = 1835

# T-0837 (of T-0814) — A TRADE PRINTED AFTER THE SCENE IS NOT AN 1835 OCCUPATION.
#
# The guard above reads a trade only out of the pass's own words, because a cited volume's
# imprint describes the BOOK.  Two defects survived that and stood in the drift T-0838
# measured, both of them promotions to `attested` on the 1835 `occupation` field:
#
#   bailey_bennet -> carpenter, cited to Fergus 1839 and Norris 1843.  The pass's own row
#     ends "Carried as 1837 and 1839 evidence; the 1835 grade does not move" — the reader
#     refused the back-projection in writing and the writer did it anyway.
#   chapman_chas_h -> printer, cited to Fergus 1839, which prints him a REAL ESTATE
#     DEALER.  "printer" is in the pass's words only in "where 'II.' is the printer's H" —
#     the compositor of the volume, the T-0510 defect recurring inside the row itself.
#
# Both deleted the `later_occupation` pointer T-0693 wrote for exactly these people, and
# the note that says why: "a directory of 1839 is evidence about 1839".  So two guards,
# and each one alone refuses both:
#
#   DATE.  A trade reaches the 1835 field only if a corroborating source demonstrably
#     describes 1835 or earlier.  `describes_date` is the field that says so; a source
#     that will not say when ("nineteenth century") is not evidence about the scene, and
#     refusing it is the conservative direction.
#   POSSESSIVE.  "the printer's H" is a trade predicated of the volume, not of the man.
#
# A refusal is not a silence: every one is named in the ledger's `refused_promotions`
# with the trade, the sources and the reason, so what did not land is as readable as what
# did.  The card keeps `none_recorded` for 1835 and keeps T-0693's dated pointer.
def source_years(sid):
    return [int(y) for y in re.findall(r"\b(1[6-9]\d{2})\b", str(source_doc(sid).get("describes_date") or ""))]


def describes_scene_or_earlier(srcs):
    """Does any corroborating source say, in `describes_date`, that it is about 1835 or
    before?  Unreadable dates count as no such claim."""
    years = [y for sid in srcs for y in source_years(sid)]
    return bool(years) and min(years) <= SCENE_YEAR


def promote(person, hh, item):
    srcs = independent(item)
    if not srcs: return [], []
    text = evidence_text(item); low = text.lower(); changes = []; refused = []
    # A TRADE IS READ ONLY OUT OF THE PASS'S OWN WORDS.  A cited volume's imprint is a
    # description of the BOOK, not of the person: Norris 1844 was printed by Ellis &
    # Fergus and the St Cyr register was kept by a priest, and scanning those citations
    # gave Gregory E. Legg the occupation "priest" and B. S. Morris "printer" (T-0510).
    # Cohort 13 found the same defect independently and on two other people: the St Mary's
    # register made Josette Beaubien a priest, and a directory made William Hanford Adams
    # a printer (T-0508).  Neither was ever committed.
    own = item_text(item).lower()
    for pat, occ in OCCUPATIONS:
        m = re.search(pat, own)
        if m:
            old = person.get("occupation") or {}
            if not (value(old) in (None, "", "none_recorded") or old.get("confidence") == "reconstructed"):
                break
            # T-0837: the two guards.  Possessive first, because it says the match is not
            # about this person at all; the date guard then says it is not about 1835.
            tail = re.match(r"['\u2019]s(?:\s+\S+)?", own[m.end():])
            if tail:
                refused.append({"field": "occupation", "value": occ, "source_ids": srcs,
                    "reason": f"the pass's words carry '{occ}' only as a possessive "
                              f"('{own[m.start():m.end()] + tail.group(0)}'), which describes the "
                              "volume or its compositor and not this person's trade "
                              "(T-0510, T-0837)"})
                break
            if not describes_scene_or_earlier(srcs):
                refused.append({"field": "occupation", "value": occ, "source_ids": srcs,
                    "reason": "no corroborating source describes 1835 or earlier, so this trade "
                              "is evidence about a later year and is not an 1835 occupation; the "
                              "dated later_occupation pointer on this card is what holds it "
                              "(T-0693, T-0837)"})
                break
            person["occupation"] = {"value": occ, "confidence": "attested", "sources": srcs,
                "note": f"{item.get('ticket')}: independently corroborated resident research. " +
                        (item.get("evidence_for") or item.get("summary") or "")}
            changes.append(f"occupation={occ}")
            break
    for pat in (r"(?:moved|came|arrived|settled)\s+(?:to|in|at)\s+chicago(?:,? illinois)?\s+(?:in )?(18[0-3]\d)",
                r"(?:moved|came|arrived|settled)\s+(?:here|there)\s+in\s+(18[0-3]\d)"):
        m = re.search(pat, low)
        if m and int(m.group(1)) <= 1835:
            year = int(m.group(1)); old = hh.get("arrival") or {}
            if value(old) in (None, "") or old.get("confidence") in ("reconstructed", "inferred"):
                hh["arrival"] = {"value": f"{year:04d}", "confidence": "attested",
                    "sources": srcs, "precision": "year",
                    "note": f"YEAR PRECISION ONLY. {item.get('ticket')} states arrival/move to Chicago in {year}; no month or day is asserted."}
                changes.append(f"arrival={year}")
            break
    byear = None
    for pat in (r"\bborn(?:\s+\w+){0,5}\s+(17\d{2}|18[0-2]\d)\b", r"\((17\d{2}|18[0-2]\d)[–-]\d{4}\)"):
        m = re.search(pat, text, re.I)
        if m: byear = int(m.group(1)); break
    if byear:
        person.setdefault("biographical_evidence", {})["birth_year"] = {"value": byear,
            "confidence": "attested", "sources": srcs,
            "note": "Birth year stated by independently corroborating source(s)."}
        person["biographical_evidence"]["age_on_1835_07_01"] = {"value": {"min": 1834-byear, "max": 1835-byear},
            "confidence": "inferred", "sources": srcs,
            "note": "Age range derived from birth year because birth month/day is not asserted here."}
        changes.append(f"birth_year={byear}")
    family = [p.strip() for p in re.split(r";|\n", item.get("proposed_facts") or "")
              if re.search(r"\b(?:married|wife|husband|widow|widower|son|daughter|children?|family)\b", p, re.I)]
    if family:
        person.setdefault("biographical_evidence", {})["family"] = {"value": family, "confidence": "attested",
            "sources": srcs, "note": "Retained as biographical evidence; no weakly linked household members were minted."}
        changes.append("family_evidence")
    return changes, refused


def census_source():
    return {"id":"census_1840_chicago_name_crosswalk","type":"dataset",
        "citation":"1840 U.S. Census, Chicago, Cook County, Illinois — committed head-of-household transcription/IPUMS serial crosswalk and household variables.",
        "date":"1840","describes_date":"1840",
        "locator":"chicago/reference/census1840/validation/H_1840_chicago_with_names_partial.csv",
        "repository":"chicago/reference/census1840/validation/","tier":1,"rights_status":"public_domain",
        "asset_use":"text_only","verified":True,
        "note":"Name-reading and serial-mapping confidence are retained separately. Later evidence relative to the 1835-07-01 scene; no automatic back-projection."}


def i(row, key):
    try: return int(float(row.get(key))) if row.get(key) not in (None, "") else None
    except Exception: return None


def attach_census(persons, ledger):
    if not CENSUS_CSV.exists(): ledger["census_1840"]={"error":"crosswalk missing"}; return
    rows = list(csv.DictReader(CENSUS_CSV.open(newline="", encoding="utf-8-sig")))
    rows = [r for r in rows if (r.get("head_name_normalized") or "").strip()
            and "low" not in (r.get("name_confidence") or "").lower()
            and "low" not in (r.get("serial_mapping_confidence") or "").lower()]
    by_name = defaultdict(list)
    for pid,(p,_h) in persons.items():
        if name_key(p.get("name")): by_name[name_key(p.get("name"))].append(pid)
    census_names = defaultdict(list)
    for row in rows: census_names[name_key(row.get("head_name_normalized") or row.get("head_name_transcribed"))].append(row)
    linked=[]; ambiguous=[]; unmatched=[]
    for key,crows in sorted(census_names.items()):
        pids=by_name.get(key,[])
        if len(crows)==1 and len(pids)==1:
            row=crows[0]; pid=pids[0]; p,_=persons[pid]
            p["later_census"]={"year":1840,"source_id":"census_1840_chicago_name_crosswalk",
                "serial":i(row,"serial"),"head_name_transcribed":row.get("head_name_transcribed"),
                "head_name_normalized":row.get("head_name_normalized"),"name_confidence":row.get("name_confidence"),
                "serial_mapping_confidence":row.get("serial_mapping_confidence"),"census_page":i(row,"census_page"),
                "census_row":i(row,"census_row"),"source_image":row.get("source_image") or None,
                "household":{"persons":i(row,"numperhh"),"children":i(row,"nchild"),"male":i(row,"nmale"),
                             "female":i(row,"nfemale"),"foreign_born":i(row,"nforeign"),
                             "agriculture":i(row,"nindagr"),"commerce":i(row,"nindcom"),
                             "manufacturing":i(row,"nindmfg")},
                "note":"LATER EVIDENCE, NOT A BACK-PROJECTION. This is the 1840 federal census household, five years after the scene date; household composition is not asserted for 1835 without another source."}
            linked.append({"person_id":pid,"serial":i(row,"serial"),"name":row.get("head_name_normalized")})
        elif pids: ambiguous.append({"name_key":key,"person_ids":pids,"serials":[i(r,"serial") for r in crows]})
        else: unmatched += [{"name":r.get("head_name_normalized") or r.get("head_name_transcribed"),
                             "serial":i(r,"serial"),"page":i(r,"census_page"),"row":i(r,"census_row")} for r in crows]
    ledger["census_1840"]={"eligible_named_rows":len(rows),"linked":linked,"ambiguous":ambiguous,
        "unmatched_named_heads":unmatched,
        "rule":"One-to-one normalized-name links only; 1840 household facts remain dated later evidence."}


def workbook_inventory():
    try: from openpyxl import load_workbook
    except Exception: return [{"error":"openpyxl unavailable"}]
    out=[]
    for path in sorted(CENSUS_DIR.glob("*.xlsx")):
        try: wb=load_workbook(path,read_only=True,data_only=True)
        except Exception as exc: out.append({"file":path.name,"error":str(exc)}); continue
        sheets=[]
        for ws in wb.worksheets:
            best=[]; bestrow=None
            for rno,row in enumerate(ws.iter_rows(min_row=1,max_row=min(ws.max_row or 1,20),values_only=True),1):
                vals=[str(v).strip() for v in row if v not in (None,"")]
                if len(vals)>len(best): best=vals[:60]; bestrow=rno
            sheets.append({"sheet":ws.title,"rows":ws.max_row,"columns":ws.max_column,
                           "probable_header_row":bestrow,"probable_headers":best})
        out.append({"file":path.name,"sheets":sheets}); wb.close()
    return out


DROP=object()
def scrub(obj, targets):
    if isinstance(obj,str): return DROP if obj in targets else obj
    if isinstance(obj,list): return [x for v in obj if (x:=scrub(v,targets)) is not DROP]
    if isinstance(obj,dict): return {k:x for k,v in obj.items() if (x:=scrub(v,targets)) is not DROP}
    return obj


def rebuild_index(index,docs,stats):
    """The rows and counts from the manifest's one owner (T-0715), plus the three
    things this programme AUTHORS: the vocabulary it ratifies, the frozen count of
    what the 2026-09-02 synthesis retired, and the manifest's own prose."""
    rebuild(index,docs)
    index.setdefault("vocabulary",{})["grades"]=["attested","inferred","reconstructed"]
    index["vocabulary"]["resident_subtypes"]=[PROJECTED]
    index["counts"]["reconstructed_removed_in_2026_09_02_synthesis"]=stats["removed_people"]
    index["_doc"]=("Manifest for data/residents/. Person grade is the top-level resident-evidence classification: attested = confidently corroborated real named circa-1835 Chicago resident; inferred = real named person reasonably believed to belong to the circa-1835 population; reconstructed is reserved for a later explicit reconstruction pass and is intentionally zero after the 2026-09-02 synthesis. resident_subtype projected_resident is the weakest evidence-based inferred subset. Per-attribute confidence is independent. later_census is explicitly 1840 evidence and is never silently back-projected to 1835.")
    return index


def snapshot(index):
    c=index.get("counts") or {}; b=c.get("by_grade") or {}
    return {"households":int(c.get("households") or 0),"persons":int(c.get("persons") or 0),
        "attested":int(b.get("attested") or 0),"inferred":int(b.get("inferred") or 0),
        "reconstructed":int(b.get("reconstructed") or 0),"letter_list_only":int(c.get("letter_list_only") or 0),
        "projected_residents":int(c.get("projected_residents") or 0),"census_1840_linked":int(c.get("census_1840_linked") or 0)}


def summary(before,after,ledger,stats):
    outcomes=ledger["research"]["outcome_counts"]; census=ledger.get("census_1840") or {}; promoted=ledger["research"]["promoted_facts"]
    lines=["# Resident and household evidence synthesis — 2 September 2026","",
      "T-0487 → T-0490 synthesis of the completed newspaper/letter-list sweep, resident-research cohorts and committed 1840 Chicago census work. Scene date: **1835-07-01**.","",
      "## Population layer: before → after","","| Measure | Before | After |","|---|---:|---:|",
      f"| Households | {before['households']} | {after['households']} |",f"| Person entries | {before['persons']} | {after['persons']} |",
      f"| Attested | {before['attested']} | {after['attested']} |",f"| Inferred | {before['inferred']} | {after['inferred']} |",
      f"| Reconstructed | {before['reconstructed']} | {after['reconstructed']} |",f"| Letter-list-only flag | {before['letter_list_only']} | {after['letter_list_only']} |",
      f"| Projected residents | 0 | {after['projected_residents']} |",f"| Linked to named 1840 census household | 0 | {after['census_1840_linked']} |","",
      f"**{stats['removed_people']} reconstructed people were retired** and {stats['removed_households']} empty household containers removed. {stats['retained_hh_inf']} evidence-based people/households formerly seated by the reconstructed programme were retained but made unplaced. Reconstructed building stock was abandoned as unassigned rather than deleted.","",
      "## Research adjudication","",f"The synthesis resolved **{ledger['research']['reviewed_people']} unique research outcomes**: "+", ".join(f"{k}: {v}" for k,v in sorted(outcomes.items()))+".","",
      "A post-office letter now documents a real named person considered reachable through Chicago; it is not automatic proof of Chicago residence. Independently corroborated letter-list identities are `attested`; other qualifying letter-list names are `inferred` + `projected_resident`. Candidate identities remain explicitly unasserted with evidence for/against retained.","",
      f"**The owner's ratified grading ladder outranks that letter-list rule** (T-0822). {len(ledger['research'].get('letter_list_deferred_to_ladder') or [])} letter-list people carry a rung `mint_civic_residents.py --regrade` fired on the seven domains the ladder reads (T-0515, T-0699), recorded on the card as `resident_research.rule` + `regraded_on`. This pass reads one corpus — the resident-research CSVs — so the absence of a row there is a no-find in that corpus and not a finding about the poll lists, the enrolments or the press. It no longer demotes those grades, and each of those cards now carries the ladder's rule and the rule it beat in the note. New evidence still crosses the line in both directions: a corroborated research outcome promotes a ladder-graded person to `attested`.","",
      "## Profile enrichment","",f"Structured promotion changed **{len(promoted)} corroborated profiles** where independent sources state usable facts (occupation, Chicago arrival year, birth-year/family evidence). Candidate-only matches never supply canonical facts.",""]
    for row in promoted[:60]: lines.append(f"- `{row['person_id']}` ({row['ticket']}): "+", ".join(row["changes"]))
    lines += ["","## 1840 census evidence","",f"**{len(census.get('linked') or [])} one-to-one resident links** were made to named 1840 census heads. Each link retains serial/page/row and separate name/serial mapping confidence plus household totals.","",
      "**1840 is later evidence, not the 1835 household.** Children, spouses, ages and industry totals are not projected backward without a separate bridge.","",
      f"Unmatched named 1840 heads: **{len(census.get('unmatched_named_heads') or [])}**; ambiguous links: **{len(census.get('ambiguous') or [])}**. These remain follow-up research rather than silent 1835 promotions.","",
      "The committed census workbooks are inventoried in the machine ledger (sheet names/dimensions/probable headers) but no 1835 resident is minted solely from an 1840 appearance.","",
      "## Placement / structures","","The retained evidence population is intentionally allowed to be unplaced. Structures that only inherited occupants from the retired reconstructed-household programme remain as anonymous/unassigned building stock for the later full placement sweep; no replacement home or workplace was invented here.",""]
    return "\n".join(lines)


# T-0838 (of T-0814) — THE DRIFT GATE.
#
# Every other generated artefact here is held to its generator by re-derivation:
# `data/datum.json` is re-derived by check.sh, baked geometry by `validate.py --stale`.
# This writer, which owns the `resident_research` block on all 1,404 people, was not.
# `--check` re-derives the population IN MEMORY and validates the invariants; it never
# compares that derivation against the committed cards, so on 2026-09-05 a writer whose
# output stood 132 household files away from the repository still reported `OK: 1404
# people` and check.sh was satisfied.  T-0509's eight corroborations were sitting in that
# gap, invisible.
#
# Why a scratch tree rather than a `write=False` pass.  The committed state is the result
# of THIS writer followed by `apply_census_1840_bridges.apply()`, which the tail of
# `main()` runs precisely so a run of either tool converges on the same bytes (T-0491).
# A synthesis-only in-memory derivation would therefore disagree with the repository
# wherever the bridges own the answer, and report drift that is not there.  Running the
# real pair, unmodified, against a copy of the tree is what the ticket's own measurement
# did, and it cannot drift from the thing it is checking.
#
# Why a baseline rather than a hard fail on any difference.  The standing drift is a
# hundred-odd cards of unspent promotion that WANT READING before they land, by the
# tickets entitled to rule on them — T-0814 split that spend out to T-0837 for exactly
# that reason.  A hard fail would have turned check.sh red for every run in the repo
# until that reading was done.  So the gate is a RATCHET: the drift standing today is
# written down file by file, a file that drifts and is not on that list fails, and a file
# on the list that stops drifting fails too, so the list can only shrink and a spend has
# to shrink it in its own commit.  New invisible drift is what this makes impossible.
DRIFT_ROOTS = ("chicago/4d/data", "chicago/4d/docs/RESEARCH", "site/chicago/4d/data")


def _scratch(tmp: Path) -> Path:
    """A throwaway REPO root the writer can be run against: the trees it writes copied,
    the reference library it only reads symlinked."""
    for rel in DRIFT_ROOTS:
        dst = tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(REPO / rel, dst)
    (tmp / "chicago" / "reference").symlink_to(CHICAGO / "reference")
    return tmp


def _files(root: Path) -> set:
    return {q.relative_to(root) for rel in DRIFT_ROOTS for q in (root / rel).rglob("*") if q.is_file()}


def drift_paths():
    """The repo-relative files the writer would change, add or delete, in sorted order."""
    with tempfile.TemporaryDirectory(prefix="synthesis-drift-") as tmp:
        scratch = _scratch(Path(tmp))
        run = subprocess.run([sys.executable, str(Path(__file__).resolve())],
                             cwd=str(ROOT), capture_output=True, text=True,
                             env={**os.environ, "SYNTH_SCRATCH_ROOT": str(scratch / "chicago" / "4d")})
        if run.returncode != 0:
            raise SystemExit("the writer failed on its own scratch copy:\n" + (run.stderr or run.stdout))
        out = []
        for rel in sorted(_files(scratch) | _files(REPO)):
            a, b = REPO / rel, scratch / rel
            if not a.exists() or not b.exists() or a.read_bytes() != b.read_bytes():
                out.append(rel.as_posix())
        return out


def promotion_self_test():
    """The two T-0837 guards have to refuse, and the promotion they guard has to still land.

    Written against the three rows that were actually standing in the T-0838 drift, so
    the test says what the defect WAS and not merely that a regex matches.
    """
    problems = []
    cases = (
        # label, item, expect (None to refuse), the reason fragment a refusal must carry
        ("bailey_bennet: a trade printed in 1839 and 1843",
         {"ticket": "T-0509", "sources": ["chicago_democrat_1833_1835",
                                          "fergus_chicago_directory_1839",
                                          "norris_chicago_directory_1843"],
          "summary": "Fergus 1839 prints 'Bailey, Bennett, carpenter and builder'. "
                     "Carried as 1837 and 1839 evidence; the 1835 grade does not move."},
         None, "describes 1835 or earlier"),
        ("chapman_chas_h: the compositor of the volume, not the man",
         {"ticket": "T-0509", "sources": ["fergus_chicago_directory_1839"],
          "summary": "Fergus 1839 prints 'Chapman, Charles II., real estate dealer, "
                     "Randolph street', where 'II.' is the printer's H."},
         None, "possessive"),
        ("a trade the scene's own newspaper prints still lands",
         {"ticket": "T-0509", "sources": ["chicago_democrat_1833_1835", "hathaway_1834"],
          "summary": "The Democrat advertises him a blacksmith on Water street in 1834."},
         "blacksmith", None))
    for label, item, want, fragment in cases:
        person, hh = {"occupation": {"value": "none_recorded"}}, {}
        changes, refused = promote(person, hh, item)
        got = (person.get("occupation") or {}).get("value")
        if want is None:
            if got != "none_recorded":
                problems.append(f"{label}: the guard did not refuse — occupation became {got!r}")
            elif not refused:
                problems.append(f"{label}: refused silently, with nothing named in the ledger")
            elif fragment not in " ".join(r["reason"] for r in refused):
                problems.append(f"{label}: refused for the wrong reason — {refused[0]['reason']!r}")
        elif got != want:
            problems.append(f"{label}: expected occupation {want!r}, got {got!r} (changes={changes})")
    # And the guard must not fire on a card that already carries a trade: the refusal is
    # about what may be WRITTEN into the 1835 field, never about what is already there.
    person = {"occupation": {"value": "farmer", "confidence": "attested"}}
    changes, refused = promote(person, {}, {"ticket": "T-0509", "sources": ["fergus_chicago_directory_1839"],
                                            "summary": "a carpenter in 1839"})
    if refused or (person["occupation"]["value"] != "farmer"):
        problems.append("a card that already states a trade was touched by the guard")
    if problems:
        [print(" -", q) for q in problems]
        print("PROMOTION SELF-TEST FAIL")
        return 1
    print(f"ok: the occupation guards refuse {len(cases) - 1} back-projection(s), name each "
          "refusal, and still land a trade the scene's own sources print")
    return 0


def ratchet(allowed, now):
    """The ratchet, as arithmetic: what drifts undeclared, and what has stopped drifting.

    Named and lifted out of `drift()` so `--drift-self-test` can exercise the RULE rather
    than the day's baseline.  It used to test the rule by perturbing the committed list,
    which meant the test went dark the moment the list emptied — and an empty list is the
    goal state, reached the day T-0837 spent the last of the standing drift.
    """
    return sorted(set(now) - set(allowed)), sorted(set(allowed) - set(now))


def drift(write_baseline=False):
    paths = drift_paths()
    if write_baseline:
        dump(DRIFT_BASELINE, {
            "ticket": "T-0838",
            "note": ("The files the committed tree and a fresh run of this writer disagree on. "
                     "The gate is a ratchet: a file that drifts and is not listed here fails, and "
                     "a listed file that stops drifting fails too, so a spend has to shrink this "
                     "list in its own commit. Regenerate with --write-baseline, never by hand. "
                     "T-0837 owns spending what is standing."),
            "count": len(paths), "paths": paths}, 2)
        print(f"  wrote {DRIFT_BASELINE.relative_to(REPO)}: {len(paths)} file(s) standing")
        return 0
    if not DRIFT_BASELINE.exists():
        print(f"  FAIL {DRIFT_BASELINE.relative_to(REPO)} is missing — run --write-baseline")
        return 1
    allowed = set((load(DRIFT_BASELINE).get("paths") or []))
    new, healed = ratchet(allowed, set(paths))
    now = set(paths)
    for path in new[:10]:
        print(f"  FAIL {path} has drifted from the writer and is not on the T-0838 baseline")
    if len(new) > 10:
        print(f"  FAIL …and {len(new) - 10} more")
    if new:
        print("  Run tools/synthesize_resident_research.py and read what it proposes before "
              "landing it — or, if the drift is deliberate and ruled on, --write-baseline.")
    for path in healed[:10]:
        print(f"  FAIL {path} no longer drifts — shrink the baseline in this commit (--write-baseline)")
    if len(healed) > 10:
        print(f"  FAIL …and {len(healed) - 10} more")
    if new or healed:
        return 1
    print(f"  ok    the writer stands {len(now)} known file(s) from the tree, "
          "every one of them on the T-0838 baseline")
    return 0


def drift_self_test():
    """The gate has to fire.  Both directions, and on any baseline including an empty one."""
    problems = []
    a, b = "chicago/4d/data/residents/households/hh_a.json", "chicago/4d/data/residents/households/hh_b.json"
    for label, allowed, now, want_new, want_healed in (
            ("undeclared drift on an empty baseline", set(), {a}, [a], []),
            ("undeclared drift beside a declared one", {a}, {a, b}, [b], []),
            ("healed drift", {a, b}, {a}, [], [b]),
            ("both at once", {a}, {b}, [b], [a]),
            ("a baseline that matches the tree", {a}, {a}, [], []),
            ("nothing standing at all", set(), set(), [], [])):
        new, healed = ratchet(allowed, now)
        if (new, healed) != (want_new, want_healed):
            problems.append(f"{label}: got new={new} healed={healed}, want new={want_new} healed={want_healed}")
    baseline = load(DRIFT_BASELINE) if DRIFT_BASELINE.exists() else None
    if baseline is None:
        problems.append("the drift baseline is missing — run --write-baseline")
    else:
        paths = baseline.get("paths")
        if not isinstance(paths, list):
            problems.append("the drift baseline has no `paths` list")
        elif baseline.get("count") != len(paths):
            problems.append(f"the drift baseline's count ({baseline.get('count')}) is not len(paths) ({len(paths)})")
    if problems:
        [print(" -", p) for p in problems]
        print("DRIFT SELF-TEST FAIL")
        return 1
    n = len((baseline or {}).get("paths") or [])
    print(f"ok: the ratchet fires in both directions; the committed baseline stands {n} file(s)")
    return 0


def check():
    index=load(INDEX); docs=[load(p) for p in HOUSEHOLDS.glob("*.json")]; people=[p for d in docs for p in d.get("persons") or []]; problems=[]
    rec=[p.get("id") for p in people if p.get("grade")=="reconstructed"]
    if rec: problems.append(f"{len(rec)} reconstructed people remain")
    bad=[p.get("id") for p in people if p.get("resident_subtype")==PROJECTED and p.get("grade")!="inferred"]
    if bad: problems.append(f"{len(bad)} projected residents are not inferred")
    actual=Counter(p.get("grade") for p in people); declared=(index.get("counts") or {}).get("by_grade") or {}
    for g in ("attested","inferred","reconstructed"):
        if int(declared.get(g) or 0)!=actual.get(g,0): problems.append(f"index {g} count disagrees with records")
    if not LEDGER.exists() or not SUMMARY.exists(): problems.append("synthesis ledger/summary missing")
    programme=load(PROGRAMME)
    if programme.get("resident_population_active") is not False:
        problems.append("retired reconstructed resident programme is not marked inactive")
    for d in docs:
        if str(d.get("id") or "").startswith("hh_inf_") and (value(d.get("lives_at")) is not None or value(d.get("works_at")) is not None):
            problems.append(f"{d.get('id')} survived synthesis but is still placed")
    for path in sorted(STRUCTURES.glob("*.json")):
        d=load(path)
        if not (str(d.get("id") or path.stem).startswith("inf_")
                or (d.get("reconstruction") or {}).get("programme_phase")==RETIRED_ROOF_PHASE):
            continue
        a=d.get("resident_assignment") or {}
        if a.get("status") != "unassigned":
            problems.append(f"{path.name} is inferred stock without resident_assignment=unassigned")
        # T-0516. The three ways a retired roof can go back to claiming an occupant, and
        # every one of them has already happened once on this dataset: a status that
        # still names the retired layer, an `occupants` block naming a household no file
        # holds, and a slot minted to satisfy the anonymous status's required fields.
        block=d.get("reconstruction") or {}
        if block.get("programme_phase")==RETIRED_ROOF_PHASE:
            if block.get("status")!="inferred_anonymous":
                problems.append(f"{path.name} still stands as {block.get('status')} for a household retired 2026-09-02")
            if "sequence" in block or "inventory_class" in block:
                problems.append(f"{path.name} carries a parcel slot it was never dealt")
            if (d.get("occupants") or {}).get("value")!=RETIRED_ROOF_OCCUPANTS["value"]:
                problems.append(f"{path.name} claims an occupant the retirement withdrew")
    dead=sorted({m for p in STRUCTURES.glob("*.json")
                 for m in re.findall(r"hh_inf_[a-z0-9_]+", p.read_text(encoding="utf-8"))}
                - {str(d.get("id")) for d in docs})
    if dead: problems.append(f"{len(dead)} retired household id(s) are still named by a structure record: {', '.join(dead[:3])}")
    if problems:
        print("RESIDENT SYNTHESIS FAIL"); [print(" -",p) for p in problems]; return 1
    print(f"OK: {len(people)} people; {actual.get('attested',0)} attested, {actual.get('inferred',0)} inferred, 0 reconstructed; {sum(p.get('resident_subtype')==PROJECTED for p in people)} projected")
    return 0


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true")
    ap.add_argument("--drift",action="store_true",help="the T-0814 ratchet: what the writer would change, against the committed baseline")
    ap.add_argument("--write-baseline",action="store_true",help="regenerate the drift baseline (never hand-edit it)")
    ap.add_argument("--drift-self-test",action="store_true")
    ap.add_argument("--promotion-self-test",action="store_true",help="the T-0837 guards: a trade printed after the scene is not an 1835 occupation")
    args=ap.parse_args()
    if args.drift_self_test: return drift_self_test()
    if args.promotion_self_test: return promotion_self_test()
    if args.drift or args.write_baseline: return drift(write_baseline=args.write_baseline)
    if args.check: return check()
    index=load(INDEX); current_before=snapshot(index)
    prior_ledger=load(LEDGER) if LEDGER.exists() else {}
    before=(prior_ledger.get("before") if current_before.get("reconstructed")==0 and prior_ledger.get("before") else current_before)
    docs={p:load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))}; research=research_rows()
    stats={"removed_people":0,"removed_households":0,"retained_hh_inf":0,"structures_unassigned":0,"roofs_enrolled_anonymous":0}; removed_people=set(); removed_hh=set(); unlink_people=set()
    for path in list(docs):
        doc=docs[path]; kept=[]
        for p in doc.get("persons") or []:
            if p.get("grade")=="reconstructed": stats["removed_people"]+=1; removed_people.add(p.get("id")); continue
            kept.append(p)
        doc["persons"]=kept
        if not kept: stats["removed_households"]+=1; removed_hh.add(doc.get("id") or path.stem); del docs[path]; continue
        if doc.get("head") not in {p.get("id") for p in kept}: doc["head"]=next((p.get("id") for p in kept if p.get("relationship")=="head"),kept[0].get("id"))
        if str(doc.get("id") or "").startswith("hh_inf_"):
            stats["retained_hh_inf"]+=1; unlink_people.update(p.get("id") for p in kept if p.get("id")); head=next((p for p in kept if p.get("id")==doc.get("head")),kept[0])
            doc["name"]=f"Evidence-only household — {head.get('name',doc.get('head'))}"; doc["division"]="unplaced"
            doc["lives_at"]={"value":None,"confidence":"reconstructed","note":"T-0489: former dwelling assignment came from the retired reconstructed-household programme; real resident retained unplaced."}
            doc["works_at"]={"value":None,"confidence":"reconstructed","note":"T-0489: no workplace is assigned from a reconstructed household; later placement requires evidence."}
            doc["research_note"]=note_once(doc.get("research_note"), RETIREMENT_NOTE)
    if prior_ledger and stats["removed_people"] == 0 and stats["removed_households"] == 0:
        prior_retirement=prior_ledger.get("retirement") or {}
        stats["removed_people"]=int(prior_retirement.get("removed_people") or 0)
        stats["removed_households"]=int(prior_retirement.get("removed_households") or 0)
    persons={p.get("id"):(p,d) for d in docs.values() for p in d.get("persons") or [] if p.get("id")}
    outcomes=Counter(); promoted=[]; refused_promotions=[]; unmatched=[]; deferred=[]
    for pid,item in sorted(research.items()):
        outcome=item.get("outcome") or "no_corroboration_yet"; outcomes[outcome]+=1
        if pid not in persons: unmatched.append({"person_id":pid,"outcome":outcome,"name":item.get("name_normalized")}); continue
        p,hh=persons[pid]
        # MERGE, DO NOT CLOBBER (T-0508).  This block is co-owned: the synthesis writes the
        # outcome and its evidence, and mint_civic_residents.py --regrade writes `refusals`
        # onto the same key (T-0515/T-0699) — a standing downgrade the ladder declined to
        # apply, which is a ruling and not a restatement.  Assigning a fresh dict deleted
        # 143 of them the first time this pass was re-run after that ticket landed, in files
        # this cohort does not even touch.  Keys this function derives still win.
        merged=dict(p.get("resident_research") or {}); merged.update(research_block(item))
        p["resident_research"]=merged
        if p.get("letter_list_only"):
            if outcome in CORROBORATED:
                p["grade"]="attested"; p.pop("resident_subtype",None); p["sources"]=list(dict.fromkeys((p.get("sources") or [])+independent(item)))
                prefix="INDEPENDENTLY CORROBORATED RESIDENT. "
            elif ladder_ruled(p):
                # T-0822. The ladder ruled this identity on evidence this corpus does not
                # read; the grade and the subtype are its call, and the note says so.
                deferred.append(pid)
                prefix=ladder_prefix(p)
            else:
                p["grade"]="inferred"; p["resident_subtype"]=PROJECTED
                prefix="PROJECTED RESIDENT. Documented in Chicago post-office evidence but not independently corroborated strongly enough for attested circa-1835 residence. "
            existing = p.get("note") or ""
            existing = strip_note_prefixes(existing)
            if outcome in CORROBORATED:
                existing = re.sub(r"^KNOWN ONLY FROM THE POST OFFICE\.\s*", "", existing, flags=re.I)
                existing = re.sub(r"Nothing else in the corpus names this person[^.]*\.\s*", "", existing, flags=re.I)
                existing = re.sub(r"No (?:arrival|trade|occupation)[^.]*\.\s*", "", existing, flags=re.I)
                prefix = "INDEPENDENTLY CORROBORATED RESIDENT. Originally documented in Chicago post-office evidence; independent resident research now corroborates the identity. "
            p["note"]=(prefix+existing).strip()
        if outcome in CORROBORATED:
            changes,refusals=promote(p,hh,item)
            if changes: promoted.append({"person_id":pid,"ticket":item.get("ticket"),"changes":changes,"source_ids":independent(item)})
            for r in refusals: refused_promotions.append({"person_id":pid,"ticket":item.get("ticket"),**r})
    missing=[]
    for pid,(p,_hh) in persons.items():
        if not (p.get("letter_list_only") and pid not in research): continue
        if ladder_ruled(p):
            # T-0822, and this is where fifteen of the seventeen were being demoted: no
            # research row is a no-find in this corpus, never a finding about the seven
            # domains the ladder read. Defer, and rewrite the note to match the grade.
            deferred.append(pid)
            p["note"]=(ladder_prefix(p)+strip_note_prefixes(p.get("note") or "")).strip()
            continue
        p["grade"]="inferred"; p["resident_subtype"]=PROJECTED; missing.append(pid)
    ledger={"date":"2026-09-02","scene_date":"1835-07-01","tickets":["T-0487","T-0488","T-0489","T-0490"],
        "owner_ruling":{"attested":"confidently corroborated real named circa-1835 Chicago resident","inferred":"real named person reasonably believed to belong to circa-1835 Chicago","projected_resident":"inferred subtype documented in at least one relevant source but too thin/ambiguous for stronger profile","reconstructed":"reserved for later explicit reconstruction; zero now"},
        "research":{"reviewed_people":len(research),"outcome_counts":dict(sorted(outcomes.items())),"unmatched_research_person_ids":unmatched,"letter_list_missing_research_row":missing,"letter_list_deferred_to_ladder":sorted(set(deferred)),"promoted_facts":promoted,"refused_promotions":sorted(refused_promotions,key=lambda r:(r["person_id"],r["field"]))},
        "census_workbook_inventory":workbook_inventory(),"structure_policy":"Keep reconstructed building stock as anonymous unassigned stock; remove retired resident occupancy references instead of deleting geometry."}
    attach_census(persons,ledger); dump(CENSUS_SOURCE,census_source(),2)
    targets={x for x in removed_people|removed_hh|unlink_people if x}; changed=[]
    for path in sorted(STRUCTURES.glob("*.json")):
        try: doc=load(path)
        except Exception: continue
        sid=str(doc.get("id") or path.stem)
        if not (sid.startswith("inf_") or sid.startswith("recon_")): continue
        old=json.dumps(doc,sort_keys=True,ensure_ascii=False); clean=scrub(doc,targets)
        if clean is DROP: continue
        doc=clean
        # T-0516: the layer is what decides this, not the id. T-0489 matched on the
        # `inf_` prefix and the household layer raised 31 roofs of which ONE is not
        # named that way - `physicians_office`, minted before the prefix convention -
        # so it alone was never marked unassigned and was still declaring an occupant
        # a fortnight after the population that occupied it was retired.
        if sid.startswith("inf_") or (doc.get("reconstruction") or {}).get("programme_phase")==RETIRED_ROOF_PHASE:
            doc["resident_assignment"]={"status":"unassigned","confidence":"reconstructed","note":"T-0489 owner ruling 2026-09-02: reconstructed resident population retired; building retained as anonymous stock for later placement."}; stats["structures_unassigned"]+=1
            if retire_roof(doc): stats["roofs_enrolled_anonymous"]+=1
        if json.dumps(doc,sort_keys=True,ensure_ascii=False)!=old: dump(path,doc,1); changed.append(path)
    index=rebuild_index(index,docs,stats); dump(INDEX,index,1)
    for path,doc in docs.items(): dump(path,doc,1)
    for path in HOUSEHOLDS.glob("*.json"):
        if path not in docs: path.unlink()
    after=snapshot(index); ledger["before"]=before; ledger["after"]=after; ledger["retirement"]=stats; dump(LEDGER,ledger,2); SUMMARY.write_text(summary(before,after,ledger,stats),encoding="utf-8")
    programme=load(PROGRAMME); programme["resident_population_active"]=False; programme["resident_population_status"]="Retired from resident list by owner ruling 2026-09-02; building stock may remain anonymous until a later explicit reconstructed-population pass."; dump(PROGRAMME,programme,2)
    sitehh=SITE/"data"/"residents"/"households"; sitehh.mkdir(parents=True,exist_ok=True); names={p.name for p in docs}
    for p in sitehh.glob("*.json"):
        if p.name not in names: p.unlink()
    # Minified, matching tools/publish.sh: the published residents layer is under a
    # size budget the authored tree is not (see the comment there).
    for p,d in docs.items():
        (sitehh/p.name).write_text(json.dumps(d,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    (SITE/"data"/"residents"/"index.json").write_text(
        json.dumps(load(INDEX),ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    sitestruct=SITE/"data"/"structures"
    if sitestruct.exists():
        for p in changed:
            q=sitestruct/p.name
            if q.exists(): q.write_text(p.read_text(encoding="utf-8"),encoding="utf-8")
    # T-0491. `attach_census` above is the 2 September partial name matcher, and the
    # adjudicated v4 identity bridges outrank it — `apply_census_1840_bridges.py` owns
    # them and keeps this file's result underneath as `legacy_partial_matcher`. The two
    # writers shared the ledger and the summary and neither deferred, so the committed
    # state depended on which of them ran last, and re-deriving one of them turned the
    # other's gate red. The synthesis hands the 1840 layer back to its owner here, so a
    # run of either tool converges on the same bytes.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import apply_census_1840_bridges
    if apply_census_1840_bridges.apply() != 0:
        raise SystemExit("the 1840 identity bridges did not re-apply cleanly")
    after=snapshot(load(INDEX))
    print(json.dumps({"before":before,"after":after,"research_reviewed":len(research),"outcomes":dict(outcomes),"promoted_profiles":len(promoted),"letter_list_deferred_to_ladder":len(set(deferred)),"census_links":len((load(LEDGER).get("census_1840") or {}).get("linked") or []),"retirement":stats},indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
