#!/usr/bin/env python3
"""T-0505 — every named 1840 head, adjudicated against the 1835 name pools.

    tools/crosswalk_census_1840_heads.py --build   write data/research/census_1840/resident_crosswalk.json
    tools/crosswalk_census_1840_heads.py --check   the outcomes on disk still follow from the inputs
    tools/crosswalk_census_1840_heads.py --report  what each sheet produced, per sheet
    tools/crosswalk_census_1840_heads.py --self-test

WHY THIS EXISTS. After PR #670 exactly three of the 1840 heads were bridged to an
1835 resident — John Murphy, William Hanford Adams, John Miller — and every other
named head on the sheets was in no state at all: not matched, not refused, just
unlooked-at. That is the state the consolidation cannot use, because the absence of
a merge reads exactly like a pair nobody has examined, so the next sweep does the
work again. This file gives EVERY named head an outcome and a reason.

WHAT AN OUTCOME MEANS.

    matched    a named 1840 head and an 1835 person are the same human being, on a
               discriminator that is INDEPENDENT OF THE NAME.
    candidate  the names agree as completely as names can, and nothing beyond the
               name has been found to tell the pair apart or hold them together.
    refused    the pair may not be joined, and the rule says why.

THE LADDER, applied in order; the first rule that fires is the outcome, and the
outcome carries that rule's id. It is deliberately hard to get to `matched`.

    L1  unreadable_name        the read carries an unresolved [?] in the name. A name
                               with a character nobody could make out cannot support an
                               identity in either direction. A name graded `low` but
                               fully spelled is NOT refused here — it goes down the
                               ladder and is capped at `candidate` by L6a.
    L2  no_surname_in_the_1835_pools
                               no 1835 name pool carries the surname at all. This is
                               a real finding, not a gap: the 1840 book is five years
                               of arrivals later than the scene.
    L3  given_name_conflict    the surname agrees and every 1835 bearer of it has a
                               given name that contradicts the head's.
    L4  initial_only           one side gives an initial where the other gives a
                               forename, so the pair rests on a surname and a letter.
    L5  name_is_not_unique     the full name agrees, and it is borne by more than one
                               person on one side or the other. A name two people
                               share cannot identify either of them. This is the rule
                               that refuses John Miller and William Smith, and it
                               refuses them by measurement rather than by a list of
                               names someone decided were common. The 1840 side counts
                               BOTH the lines read here AND the line an existing
                               adjudicated bridge names — see below.
    L6a low_confidence_caps_at_candidate
                               the full name agrees, is unique on both sides, and a
                               discriminator holds — but the reader graded THIS name
                               `low`. The identity may be right and the spelling is not
                               firm enough to assert it, so the head is a candidate and
                               says so. Re-reading the line is what promotes it.
    L6  matched                the full name agrees, is unique on both sides, the read
                               is graded `medium` or better, and an INDEPENDENT
                               discriminator holds: the 1835 person is separately
                               attested in Chicago after the 1840 book was taken (a
                               Fergus 1843 or Norris 1844 directory entry adjudicated to
                               that person id), or an adjudicated 1840 bridge already
                               exists for them.
    L7  candidate              the full name agrees and is unique on both sides, and
                               no independent discriminator was found.

AN EXISTING BRIDGE THAT NAMES A DIFFERENT LINE IS A CONFLICT, NOT A CONFIRMATION.
`census_1840_identity_bridges.csv` locates each of its three bridges by printed page
and row, and those came out of a workbook this repo no longer holds. Where a head
read here carries the same name as a bridge but sits on a DIFFERENT page or row, the
two are two 1840 lines with one name — so L5 refuses the pair and the conflict is
written down, because the alternative is to quietly assert that the bridge and the
line are the same household when nothing has shown that they are.

HOW STRONG THE DISCRIMINATOR IS, SAID OUT LOUD. `directory_persistence` comes from
the Fergus 1843 and Norris 1844 crosswalks, whose own matching rule is a surname and
a first given initial. So the link from an 1835 person to a directory entry is that
strong and no stronger, and every discriminator record says so. What it supplies is
still independent of the 1840 sheet: that this person was in Chicago after the census
was taken, which is the thing a name coincidence cannot supply. Each record also says
whether the directory entry writes the forename out in full and whether it carries an
address — the ticket's own two examples of a discriminator.

WHAT IS NOT A DISCRIMINATOR. An appearance of the SAME NAME on a poll list, a tax
list or a letter list is not independent evidence of identity: it is the same name
again, and it cannot separate two people who share it. Those appearances are
recorded on every outcome as `same_name_support` because they matter to the
consolidation, and they never promote a candidate to matched.

WHAT THIS FILE DOES NOT DO. It mints nothing and regrades nobody, and it changes no
household file. For each `matched` head it writes a PROPOSED `later_census` block in
the exact shape PR #670 wrote, and T-0515 applies them through
tools/apply_census_1840_bridges.py. The ratified ladder binds throughout: 1839/1840
alone is never an 1835 resident, and 1840 household composition is never
back-projected onto the scene.

INPUT THAT IS NOT AVAILABLE. The 1839 Chicago directory is T-0506 and is not
extracted yet; it is declared in `inputs` as unavailable rather than treated as
absent, because a source nobody has read is not a source that says nothing.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "data" / "research"
CENSUS = RESEARCH / "census_1840"
OUT = CENSUS / "resident_crosswalk.json"

TICKET = "T-0505"

# Nineteenth-century clerical abbreviations as the sheets and the lists write them.
ABBREV = {
    "wm": "william", "jno": "john", "jas": "james", "thos": "thomas",
    "chas": "charles", "cha": "charles", "geo": "george", "danl": "daniel",
    "saml": "samuel", "robt": "robert", "jos": "joseph", "benj": "benjamin",
    "edwd": "edward", "edw": "edward", "richd": "richard", "rich": "richard",
    "michl": "michael", "patk": "patrick", "alexr": "alexander", "alex": "alexander",
    "hy": "henry", "jonan": "jonathan", "nathl": "nathaniel", "fredk": "frederick",
    "ths": "thomas", "matw": "matthew", "andw": "andrew", "abm": "abraham",
    "isc": "isaac", "sml": "samuel", "wilm": "william",
}
SUFFIXES = {"jr", "sr", "jun", "sen", "2d", "3d", "ii", "iii", "esq"}
FIRM_TAIL = re.compile(r"\s*&\s*(co|son|sons|bro|bros|brother|brothers)\.?\s*$", re.I)


def load(path: Path):
    with path.open() as fh:
        return json.load(fh)


def parse_name(raw: str) -> dict:
    """Split a written name into given tokens and a surname, and say how sure it is."""
    text = (raw or "").strip()
    uncertain = "[?]" in text
    firm = bool(FIRM_TAIL.search(text))
    text = FIRM_TAIL.sub("", text)
    text = text.replace("[?]", " ")
    text = re.sub(r"[^A-Za-z0-9 .,'-]", " ", text)
    text = text.replace(",", " ").replace(".", " ")
    tokens = [t for t in text.split() if t]
    tokens = [t for t in tokens if t.lower().strip("'-") not in SUFFIXES]
    parts = []
    for t in tokens:
        low = re.sub(r"[^a-z]", "", t.lower())
        if not low:
            continue
        parts.append(ABBREV.get(low, low))
    if not parts:
        return {"surname": "", "given": [], "forename": "", "uncertain": True,
                "firm": firm, "key": ""}
    surname = parts[-1]
    given = parts[:-1]
    forename = next((g for g in given if len(g) > 1), "")
    return {
        "surname": surname,
        "given": given,
        "forename": forename,
        "uncertain": uncertain,
        "firm": firm,
        "key": (forename + "|" + surname) if forename else "",
    }


def initials(given: list) -> list:
    return [g[0] for g in given if g]


# ---------------------------------------------------------------- the 1840 heads

def read_heads() -> list:
    heads = []
    for path in sorted((CENSUS / "pages").glob("*.json")):
        page = load(path)
        if page.get("sheet_side") != "left":
            continue
        sheet_grade = page.get("name_confidence")
        printed = page.get("printed_page")
        for rec in page.get("records") or []:
            raw = rec.get("normalized") or rec.get("as_read") or ""
            if not raw.strip():
                continue
            heads.append({
                "familysearch_id": page.get("familysearch_id"),
                "image": page.get("image"),
                "printed_page": printed if isinstance(printed, int) else None,
                "printed_page_as_written": printed,
                "line": rec.get("line"),
                "as_read": rec.get("as_read") or raw,
                "normalized": raw,
                "name_confidence": rec.get("name_confidence") or sheet_grade,
                "sheet_name_confidence": sheet_grade,
                "cells": rec.get("cells") or {},
                "parsed": parse_name(raw),
            })
    return heads


# ------------------------------------------------------------- the 1835 name pools

def read_residents() -> list:
    people = []
    for path in sorted((ROOT / "data" / "residents" / "households").glob("*.json")):
        hh = load(path)
        for person in hh.get("persons") or []:
            name = person.get("name")
            if not name:
                continue
            occ = person.get("occupation") or {}
            people.append({
                "person_id": person.get("id"),
                "household_id": hh.get("id"),
                "name": name,
                "grade": person.get("grade"),
                "occupation": occ.get("value") if isinstance(occ, dict) else occ,
                "already_bridged": bool(person.get("later_census")),
                "parsed": parse_name(name),
            })
    return people


def read_voters() -> list:
    """The voter pool, each entry carrying the source the civic crosswalk states.

    T-0598: read from that file's own `source_id` rather than written here, so this
    tool cannot drift from what the civic domain says it adjudicated from.
    """
    doc = load(RESEARCH / "civic" / "voter_crosswalk.json")
    source_id = doc.get("source_id")
    out = []
    for entry in doc.get("entries") or []:
        name = entry.get("normalized") or entry.get("as_read") or ""
        if not name.strip():
            continue
        out.append({"name": name, "list": entry.get("list"), "source_id": source_id,
                    "record_id": entry.get("record_id"), "parsed": parse_name(name)})
    return out


def issue_sources() -> dict:
    """issue_id -> source_id, out of the newspapers corpus.

    T-0598: a gazetteer person is a name read out of one or more ISSUES, and the
    corpus is the only place that says which printed source each issue is. Derived
    rather than written down here, so a source id can never be invented for a
    mention whose issue the corpus does not carry.
    """
    doc = load(RESEARCH / "newspapers" / "corpus.json")
    return {i["id"]: i["source_id"] for i in doc.get("issues") or []
            if i.get("id") and i.get("source_id")}


def read_letter_list() -> list:
    doc = load(RESEARCH / "newspapers" / "gazetteer.json")
    by_issue = issue_sources()
    out = []
    for person in doc.get("persons") or []:
        name = person.get("name") or ""
        if not name.strip():
            continue
        # A mention is `<issue_id>#<claim>`; the issue is what carries the source.
        sources = sorted({by_issue[m.split("#", 1)[0]]
                          for m in person.get("mentions") or []
                          if m.split("#", 1)[0] in by_issue})
        out.append({"name": name, "id": person.get("id"), "source_ids": sources,
                    "letter_list_only": bool(person.get("letter_list_only")),
                    "parsed": parse_name(name)})
    return out


# The v4 workbook this table was drawn out of, and the source record that describes
# it: data/sources/resident_research_v4_1835_census_bridge.json cites "Chicago 1835
# Best Resident Set Research v4", which is the `file` every row of
# census_1835_bridge_candidates.json names. Stated, not inferred (T-0598).
BRIDGE_SOURCE_ID = "resident_research_v4_1835_census_bridge"


def read_bridge_candidates() -> list:
    doc = load(RESEARCH / "residents" / "census_1835_bridge_candidates.json")
    out = []
    for row in doc.get("rows") or []:
        name = row.get("Preferred Name") or ""
        if not name.strip():
            continue
        out.append({"name": name, "tier": row.get("1835 Tier"),
                    "source_id": BRIDGE_SOURCE_ID, "parsed": parse_name(name)})
    return out


def read_persistence() -> dict:
    """person_id -> the post-1840 directory entries adjudicated to that person.

    Only the `matches` band counts. `contested` and `ambiguous` are exactly the
    cases the directory crosswalks could not settle, and an unsettled directory
    entry cannot settle a census identity either.
    """
    out = {}
    for name, key, year in (("norris_1844_crosswalk_1835.json", "entries_1844", 1844),
                            ("fergus_1843_crosswalk_1835.json", "entries_1843", 1843)):
        path = RESEARCH / "directories" / name
        if not path.exists():
            continue
        doc = load(path)
        for match in doc.get("matches") or []:
            pid = match.get("person_id")
            if not pid:
                continue
            entries = match.get(key) or []
            printed = [e.get("as_printed") for e in entries if e.get("as_printed")]
            out.setdefault(pid, []).append({
                "year": year, "source_id": doc.get("source_id"),
                "resident_as_matched": match.get("resident"),
                "entries": printed[:3],
            })
    return out


def read_existing_bridges() -> dict:
    path = RESEARCH / "residents" / "census_1840_identity_bridges.csv"
    out = {}
    if not path.exists():
        return out
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("person_id"):
                out[row["person_id"]] = row
    return out


def read_legacy_unmatched() -> list:
    doc = load(RESEARCH / "residents" / "synthesis_2026_09_02.json")
    legacy = ((doc.get("census_1840") or {}).get("legacy_partial_matcher") or {})
    return legacy.get("unmatched_named_heads") or []


# ------------------------------------------------------------------ adjudication

def index_by(pool: list, attr: str) -> dict:
    idx = {}
    for item in pool:
        value = item["parsed"][attr]
        if value:
            idx.setdefault(value, []).append(item)
    return idx


def same_name_support(head_key: str, voters_by_key, letters_by_key, cands_by_key) -> list:
    """Every pool that prints the same name, WITH the source each pool rests on.

    T-0598: a support row naming a pool and not a source says where somebody would
    have to go looking, not what the ruling rests on, and only the second can be
    carried to a resident card. A row whose source cannot be derived carries none —
    an absent source_id is honest, an invented one is the fault this gate exists for.
    """
    support = []
    for entry in voters_by_key.get(head_key, []):
        row = {"pool": "voter_lists", "list": entry["list"],
               "record_id": entry["record_id"], "name": entry["name"]}
        if entry.get("source_id"):
            row["source_id"] = entry["source_id"]
        support.append(row)
    for entry in letters_by_key.get(head_key, []):
        row = {"pool": "letter_list" if entry["letter_list_only"] else "newspapers",
               "id": entry["id"], "name": entry["name"]}
        if entry.get("source_ids"):
            row["source_ids"] = entry["source_ids"]
        support.append(row)
    for entry in cands_by_key.get(head_key, []):
        row = {"pool": "census_1835_bridge_candidates",
               "tier": entry["tier"], "name": entry["name"]}
        if entry.get("source_id"):
            row["source_id"] = entry["source_id"]
        support.append(row)
    return support


def later_census_block(head: dict, resident: dict, basis: str) -> dict:
    """PR #670's shape exactly, and PROPOSED — nothing here is applied."""
    cells = {int(k): v for k, v in (head.get("cells") or {}).items() if str(k).isdigit()}
    return {
        "year": 1840,
        "source_id": "census_1840_chicago_familysearch_images",
        "serial": None,
        "serial_note": "no IPUMS serial is asserted: the page-to-serial fingerprint is "
                       "T-0504 and is not landed. The head is located by image, printed "
                       "page and line, which is what this project read.",
        "head_name_transcribed": head["as_read"],
        "head_name_normalized": head["normalized"],
        "name_confidence": head["name_confidence"],
        "identity_confidence": "provisional",
        "bridge_status": "proposed",
        "serial_mapping_confidence": None,
        "census_page": head["printed_page"],
        "census_row": head["line"],
        "source_image": head["image"],
        "source_kind": "1840 left image, read line by line in this repo",
        "household": {
            "persons_columns_read": len(cells),
            "note": "the left sheet's age/sex columns as read; the TOTAL and the "
                    "employment columns sit on the paired continuation sheet, which "
                    "T-0528 and T-0539 pair. No household count is asserted here.",
        },
        "bridge_basis": basis,
        "note": "LATER EVIDENCE, NOT A BACK-PROJECTION. This is the 1840 federal "
                "census household, five years after the 1835-07-01 scene; its "
                "household composition is not asserted for 1835 without separate "
                "evidence. PROPOSED ONLY — T-0515 applies bridges.",
    }


def adjudicate(head, residents_by_key, residents_by_surname, heads_by_key,
               voters_by_key, letters_by_key, cands_by_key,
               persistence, existing_bridges) -> dict:
    parsed = head["parsed"]
    out = {
        "familysearch_id": head["familysearch_id"],
        "printed_page": head["printed_page"],
        "line": head["line"],
        "as_read": head["as_read"],
        "normalized": head["normalized"],
        "name_confidence": head["name_confidence"],
        "surname": parsed["surname"],
        "forename": parsed["forename"] or None,
    }
    support = same_name_support(parsed["key"], voters_by_key, letters_by_key,
                                cands_by_key) if parsed["key"] else []
    out["same_name_support"] = support

    if parsed["uncertain"] or not parsed["surname"]:
        out["outcome"] = "refused"
        out["rule"] = "L1 unreadable_name"
        out["reason"] = (
            "The name as read is %r, graded %s, and carries a character the reader "
            "could not make out. A name that cannot be spelled cannot support an "
            "identity in either direction — the refusal is of the READING, not of the "
            "person, and a second reading of the line reopens it."
            % (head["as_read"], head["name_confidence"])
        )
        return out

    bearers = residents_by_surname.get(parsed["surname"], [])
    if not bearers:
        out["outcome"] = "refused"
        out["rule"] = "L2 no_surname_in_the_1835_pools"
        out["reason"] = (
            "No person in the residents layer carries the surname %r. The 1840 book "
            "is five years of arrivals after the scene and most of its heads are not "
            "1835 people; a surname absent from 1835 is evidence of that, not a gap "
            "in the reading." % parsed["surname"]
        )
        return out

    exact = residents_by_key.get(parsed["key"], []) if parsed["key"] else []
    if not exact:
        if not parsed["forename"]:
            out["outcome"] = "refused"
            out["rule"] = "L4 initial_only"
            out["reason"] = (
                "The head is written %r — a surname and initials only — and %d person(s) "
                "of 1835 carry the surname %r. A surname and a letter is not an "
                "identity." % (head["normalized"], len(bearers), parsed["surname"])
            )
            out["surname_bearers_1835"] = [b["person_id"] for b in bearers][:8]
            return out
        initial_only_bearers = [b for b in bearers if not b["parsed"]["forename"]
                                and initials(b["parsed"]["given"])[:1] == [parsed["forename"][0]]]
        if initial_only_bearers:
            out["outcome"] = "refused"
            out["rule"] = "L4 initial_only"
            out["reason"] = (
                "The head is %r and the 1835 bearer(s) of %r are written with an initial "
                "only (%s). The pair rests on a surname and one letter, which is not an "
                "identity." % (head["normalized"], parsed["surname"],
                               ", ".join(b["name"] for b in initial_only_bearers[:4]))
            )
            out["surname_bearers_1835"] = [b["person_id"] for b in initial_only_bearers][:8]
            return out
        out["outcome"] = "refused"
        out["rule"] = "L3 given_name_conflict"
        out["reason"] = (
            "The surname %r is carried by %d person(s) of 1835 (%s) and none of their "
            "given names is %r." % (parsed["surname"], len(bearers),
                                    ", ".join(b["name"] for b in bearers[:4]),
                                    parsed["forename"])
        )
        out["surname_bearers_1835"] = [b["person_id"] for b in bearers][:8]
        return out

    rival_heads = [h for h in heads_by_key.get(parsed["key"], []) if h is not head]
    bridge_row = existing_bridges.get(exact[0]["person_id"]) if len(exact) == 1 else None
    bridge_elsewhere = None
    if bridge_row:
        page = bridge_row.get("census_page")
        row_no = bridge_row.get("census_row")
        same_line = (str(page) == str(head["printed_page"])
                     and str(row_no) == str(head["line"]))
        if not same_line:
            bridge_elsewhere = {
                "person_id": exact[0]["person_id"],
                "bridge_census_page": page,
                "bridge_census_row": row_no,
                "bridge_source_image": bridge_row.get("source_image"),
                "bridge_source_workbook": bridge_row.get("source_workbook"),
                "this_line": {"printed_page": head["printed_page"], "line": head["line"],
                              "familysearch_id": head["familysearch_id"]},
                "why": "the adjudicated bridge for this person names printed page %s "
                       "row %s, and this head is printed page %s line %s. Two 1840 "
                       "lines carry the name; neither one identifies the person."
                       % (page, row_no, head["printed_page"], head["line"]),
            }
    if len(exact) > 1 or rival_heads or bridge_elsewhere:
        out["outcome"] = "refused"
        out["rule"] = "L5 name_is_not_unique"
        out["reason"] = (
            "The name %r is borne by %d person(s) of 1835 and appears on %d named 1840 "
            "head line(s). A name that two people share cannot identify either of them, "
            "so the pair is refused by measurement rather than by anyone's list of "
            "common names."
            % (head["normalized"], len(exact),
               len(rival_heads) + 1 + (1 if bridge_elsewhere else 0))
        )
        if bridge_elsewhere:
            out["conflict_with_existing_bridge"] = bridge_elsewhere
            out["reason"] += (" " + bridge_elsewhere["why"] + " The bridge is not "
                              "withdrawn here — this file adjudicates lines, and "
                              "T-0515 owns the bridge table.")
        out["candidates_1835"] = [b["person_id"] for b in exact][:8]
        out["other_1840_lines_with_this_name"] = [
            {"familysearch_id": h["familysearch_id"], "printed_page": h["printed_page"],
             "line": h["line"]} for h in rival_heads][:8]
        return out

    resident = exact[0]
    out["person_id"] = resident["person_id"]
    out["household_id"] = resident["household_id"]
    out["resident_name"] = resident["name"]
    out["resident_grade_1835"] = resident["grade"]

    discriminators = []
    for entry in persistence.get(resident["person_id"], []):
        text = " ".join(entry["entries"]).lower()
        forename = parsed["forename"]
        has_forename = bool(forename) and forename in text
        has_address = bool(re.search(r"\b(res|residence|house|h |bds|bet\.?|near|"
                                     r"corner|cor\.?|st\.?|street)\b", text))
        discriminators.append({
            "kind": "directory_persistence",
            "year": entry["year"],
            "source_id": entry["source_id"],
            "entries": entry["entries"],
            "forename_written_out_in_the_entry": has_forename,
            "entry_carries_an_address": has_address,
            "underlying_adjudication_strength":
                "the directory crosswalk's own matching rule is surname plus first "
                "given initial, so the LINK from the person to this entry is that "
                "strong and no stronger. What it supplies here is independent of the "
                "1840 name either way: a person in Chicago after 1840.",
            "why": "the same person is separately adjudicated into the %d directory%s%s, "
                   "so they were still in Chicago after the 1840 book was taken. That is "
                   "evidence about the PERSON, not about the spelling of the name."
                   % (entry["year"],
                      ", which writes the forename out in full" if has_forename else "",
                      ", at a stated address" if has_address else ""),
        })
    if resident["person_id"] in existing_bridges:
        row = existing_bridges[resident["person_id"]]
        discriminators.append({
            "kind": "existing_adjudicated_bridge",
            "serial": row.get("serial"),
            "bridge_status": row.get("bridge_status"),
            "why": "an 1840 bridge for this person is already adjudicated in "
                   "census_1840_identity_bridges.csv.",
        })
    out["discriminators"] = discriminators

    if discriminators:
        basis = "Full forename and surname agree (%s = %s), the name is unique on both "
        basis = (basis % (head["normalized"], resident["name"])) + (
            "sides, and %s" % "; ".join(d["why"] for d in discriminators))
        if head["name_confidence"] == "low":
            out["outcome"] = "candidate"
            out["rule"] = "L6a low_confidence_caps_at_candidate"
            out["reason"] = (
                basis + " The identity would hold, but the reader graded THIS name "
                "`low`, and a spelling that is not firm may not be asserted as an "
                "identity. Re-reading line %s of %s is what promotes it."
                % (head["line"], head["familysearch_id"])
            )
            out["would_be_matched_on_a_firmer_read"] = True
            return out
        out["outcome"] = "matched"
        out["rule"] = "L6 matched"
        out["reason"] = basis
        out["proposed_later_census"] = later_census_block(head, resident, basis)
        return out

    out["outcome"] = "candidate"
    out["rule"] = "L7 candidate"
    out["reason"] = (
        "Full forename and surname agree (%s = %s) and the name is unique on both "
        "sides, but nothing independent of the name was found: %s carries no "
        "adjudicated 1843 or 1844 directory entry and no existing 1840 bridge. %s"
        % (head["normalized"], resident["name"], resident["person_id"],
           ("The same name appears on %d 1835 list(s), which is the same name again "
            "and does not discriminate." % len(support)) if support
           else "The name appears on no 1835 list beyond the residents layer.")
    )
    return out


def town_findings(rows: list) -> list:
    """The only spatial signal an 1840 sheet carries is the order the enumerator walked."""
    found = []
    joined = [r for r in rows if r["outcome"] in ("matched", "candidate")]
    by_page = {}
    for row in joined:
        by_page.setdefault(row["familysearch_id"], []).append(row)
    for fs_id, page_rows in sorted(by_page.items()):
        page_rows.sort(key=lambda r: r["line"] or 0)
        for a, b in zip(page_rows, page_rows[1:]):
            gap = (b["line"] or 0) - (a["line"] or 0)
            if gap <= 2:
                found.append({
                    "kind": "enumeration_adjacency",
                    "town_finding": True,
                    "familysearch_id": fs_id,
                    "printed_page": a["printed_page"],
                    "lines": [a["line"], b["line"]],
                    "pair": [a["normalized"], b["normalized"]],
                    "person_ids": [a.get("person_id"), b.get("person_id")],
                    "outcomes": [a["outcome"], b["outcome"]],
                    "says": "The enumerator wrote %s and %s %s on printed page %s. An "
                            "1840 enumerator walked a route, so lines that are adjacent "
                            "were dwellings that were near each other IN 1840."
                            % (a["normalized"], b["normalized"],
                               "on consecutive lines" if gap == 1 else "two lines apart",
                               a["printed_page"]),
                    "what_it_does_not_say": "nothing about where either household stood "
                            "in 1835, and nothing that may place a structure. Five years "
                            "separate this order from the scene, and neither head is "
                            "placed on the 1840 ground either.",
                })
    return found


def readjudicate_legacy(legacy, heads, rows, pages_read) -> list:
    """The 29 heads the 2 September legacy matcher left unmatched, given reasons."""
    by_norm = {}
    for row in rows:
        by_norm.setdefault(parse_name(row["normalized"])["key"], []).append(row)
    out = []
    for entry in legacy:
        name = entry.get("name") or ""
        parsed = parse_name(name)
        here = by_norm.get(parsed["key"], []) if parsed["key"] else []
        item = {
            "legacy_name": name,
            "legacy_serial": entry.get("serial"),
            "legacy_page": entry.get("page"),
            "legacy_row": entry.get("row"),
            "found_in_this_repos_reading": bool(here),
        }
        if here:
            row = here[0]
            item["outcome"] = row["outcome"]
            item["rule"] = row["rule"]
            item["reason"] = row["reason"]
            item["read_at"] = {"familysearch_id": row["familysearch_id"],
                               "printed_page": row["printed_page"], "line": row["line"]}
        else:
            page = entry.get("page")
            page_read = page in pages_read
            item["legacy_page_read_in_this_repo"] = page_read
            item["outcome"] = "refused"
            item["rule"] = ("L0b page_read_here_and_the_name_is_not_on_it" if page_read
                            else "L0a page_not_read_here")
            item["reason"] = (
                ("The legacy matcher took %r from printed page %s, and this repo HAS read "
                 "that page line by line: no line on it carries that name. The two "
                 "readings disagree, and the disagreement is the finding — the workbook "
                 "row is refused in favour of the page." % (name, page))
                if page_read else
                ("The legacy matcher took %r from printed page %s, which is not among the "
                 "%d left sheets read here, and no sheet that IS read carries the name. "
                 "It is refused as unverifiable rather than carried forward: the workbook "
                 "is lost (owner's ruling, 2026-09-03, 'They are lost; rebuild'), so the "
                 "row cannot be checked until printed page %s is read — which is what "
                 "T-0496, T-0527, T-0546 and T-0553 are for."
                 % (name, page, len(pages_read), page))
            )
        out.append(item)
    return out


def build() -> dict:
    heads = read_heads()
    residents = read_residents()
    voters = read_voters()
    letters = read_letter_list()
    candidates = read_bridge_candidates()
    persistence = read_persistence()
    existing = read_existing_bridges()

    residents_by_key = index_by(residents, "key")
    residents_by_surname = index_by(residents, "surname")
    heads_by_key = {}
    for head in heads:
        if head["parsed"]["key"]:
            heads_by_key.setdefault(head["parsed"]["key"], []).append(head)

    rows = [adjudicate(h, residents_by_key, residents_by_surname, heads_by_key,
                       index_by(voters, "key"), index_by(letters, "key"),
                       index_by(candidates, "key"), persistence, existing)
            for h in heads]

    counts = {"named_heads": len(rows), "matched": 0, "candidate": 0, "refused": 0}
    by_rule = {}
    for row in rows:
        counts[row["outcome"]] += 1
        by_rule[row["rule"]] = by_rule.get(row["rule"], 0) + 1

    pages_read = {h["printed_page"] for h in heads if h["printed_page"]}
    legacy = readjudicate_legacy(read_legacy_unmatched(), heads, rows, pages_read)
    legacy_counts = {}
    for item in legacy:
        legacy_counts[item["outcome"]] = legacy_counts.get(item["outcome"], 0) + 1

    return {
        "schema": 1,
        "ticket": TICKET,
        "generated_by": "tools/crosswalk_census_1840_heads.py --build",
        # T-0598. What every ruling in this file was adjudicated FROM: the 1840 page
        # images this project read. A ruling that reaches a resident and names no
        # source cannot be carried to that resident's card by any tool, because
        # `persons[].sources` is a list of SOURCE IDS. Corroborating pools are named
        # per support row below, where they are known; this is the floor.
        "source_id": "census_1840_chicago_familysearch_images",
        "what": "Every named head on the 1840 Chicago left sheets read in this repo, "
                "adjudicated against the 1835 name pools: matched, candidate or "
                "refused, each with the rule that decided it.",
        "scene_relation": "LATER EVIDENCE ONLY. The ratified grading ladder binds: an "
                          "1839 or 1840 appearance alone is never an 1835 resident, and "
                          "1840 household composition is never back-projected to the "
                          "1835-07-01 scene.",
        "mints_or_regrades": False,
        "ladder": [
            {"rule": "L1 unreadable_name", "outcome": "refused",
             "says": "an unresolved [?] in the name, or a low-confidence read"},
            {"rule": "L2 no_surname_in_the_1835_pools", "outcome": "refused",
             "says": "no 1835 person carries the surname"},
            {"rule": "L3 given_name_conflict", "outcome": "refused",
             "says": "the surname agrees and every 1835 bearer's given name does not"},
            {"rule": "L4 initial_only", "outcome": "refused",
             "says": "one side gives an initial where the other gives a forename"},
            {"rule": "L5 name_is_not_unique", "outcome": "refused",
             "says": "the full name is borne by more than one person on a side"},
            {"rule": "L6a low_confidence_caps_at_candidate", "outcome": "candidate",
             "says": "the match would hold, but the reader graded this name low"},
            {"rule": "L6 matched", "outcome": "matched",
             "says": "unique full-name agreement, a read graded medium or better, AND "
                     "a discriminator independent of the name"},
            {"rule": "L7 candidate", "outcome": "candidate",
             "says": "unique full-name agreement and nothing independent of the name"},
        ],
        "what_is_not_a_discriminator": "an appearance of the SAME NAME on a poll list, a "
            "tax list or a letter list. It is the same name again and cannot separate "
            "two people who share it, so it is recorded as same_name_support on every "
            "outcome and never promotes a candidate to matched.",
        "inputs": [
            {"what": "1840 left sheets read in this repo",
             "path": "data/research/census_1840/pages/", "available": True,
             "n": len({h["familysearch_id"] for h in heads})},
            {"what": "residents layer, persons", "path": "data/residents/households/",
             "available": True, "n": len(residents)},
            {"what": "voter, poll and tax list entries (T-0493)",
             "path": "data/research/civic/voter_crosswalk.json", "available": True,
             "n": len(voters)},
            {"what": "letter-list and newspaper persons",
             "path": "data/research/newspapers/gazetteer.json", "available": True,
             "n": len(letters)},
            {"what": "recovered v1 workbook bridge rows",
             "path": "data/research/residents/census_1835_bridge_candidates.json",
             "available": True, "n": len(candidates)},
            {"what": "Fergus 1843 and Norris 1844 directory adjudications — the "
                     "independent discriminator",
             "path": "data/research/directories/", "available": True,
             "n": len(persistence)},
            {"what": "the 1839 Chicago directory", "path": None, "available": False,
             "why_unavailable": "T-0506 is open and the directory is not extracted. "
                                "Declared unavailable, not absent: a source nobody has "
                                "read is not a source that says nothing."},
            {"what": "page-to-IPUMS-serial fingerprint", "path": None, "available": False,
             "why_unavailable": "T-0504 is open. Every proposed block therefore carries "
                                "serial: null and locates its head by image, printed "
                                "page and line."},
        ],
        "counts": counts,
        "counts_by_rule": dict(sorted(by_rule.items())),
        "printed_pages_read_here": sorted(pages_read),
        "legacy_29_readjudicated": {
            "counts": legacy_counts,
            "counts_by_rule": {r: sum(1 for h in legacy if h["rule"] == r)
                               for r in sorted({h["rule"] for h in legacy})},
            "heads": legacy,
        },
        "town_findings": town_findings(rows),
        "town_findings_note": "the only spatial signal an 1840 sheet carries is the order "
                              "the enumerator walked it in. Adjacency is reported for "
                              "matched and candidate heads only, and it is an 1840 fact: "
                              "nothing here places a structure on the 1835 ground.",
        "heads": rows,
        "_person_names": {p["person_id"]: p["name"] for p in residents},
    }


DOMAIN_CROSSWALK = CENSUS / "crosswalk.json"


def domain_crosswalk(doc: dict) -> dict:
    """The domain's own identity layer, which T-0505 found empty.

    `crosswalk.json` is where this domain's merges and refusals are declared, and it
    held `passes: [], merges: [], refusals: []` — which reads exactly like a domain
    nobody has looked at. Every `matched` head becomes a merge; every pair that a
    surname brought together and a rule pushed apart becomes a refusal, named on both
    sides. Candidates are neither, and stay in resident_crosswalk.json, because a
    candidate is the one state this file has no shape for.
    """
    existing = load(DOMAIN_CROSSWALK) if DOMAIN_CROSSWALK.exists() else {}
    merges, refusals = [], []
    for row in doc["heads"]:
        here = "printed page %s line %s (%s)" % (row["printed_page"], row["line"],
                                                 row["familysearch_id"])
        if row["outcome"] == "matched":
            frm, into = row["normalized"], row["resident_name"]
            merges.append({
                "from": frm, "into": into,
                "rule": "The 1840 head written %r at %s and the 1835 person %r are one "
                        "man: forename and surname agree in full, the name is unique "
                        "both among the 498 named heads read here and among the 1835 "
                        "persons, and %s"
                        % (frm, here, into,
                           "; ".join(d["why"] for d in row["discriminators"])),
                "evidence": [row["familysearch_id"], "T-0505",
                             "data/research/census_1840/resident_crosswalk.json"]
                            + [d.get("source_id") for d in row["discriminators"]
                               if d.get("source_id")],
                "person_id": row["person_id"],
                "scene_relation": "later evidence only — the merge joins an 1840 line to "
                                  "an 1835 person and asserts nothing about 1835.",
            })
            continue
        if row["rule"].startswith(("L3", "L4", "L5")):
            for pid in (row.get("surname_bearers_1835") or row.get("candidates_1835") or []):
                other = doc["_person_names"].get(pid)
                if not other or other == row["normalized"]:
                    continue
                refusals.append({
                    "a": row["normalized"], "b": other,
                    "rule": "%r at %s is NOT %r: %s"
                            % (row["normalized"], here, other, row["reason"]),
                    "evidence": [row["familysearch_id"], "T-0505", row["rule"]],
                })
    return {
        "schema": existing.get("schema", 1),
        "domain": "census_1840",
        "generated_by": "tools/crosswalk_census_1840_heads.py --build (T-0505)",
        # T-0598: what this domain adjudicated FROM, so a merge here can be carried
        # to a card. `evidence` on each merge below is a list of strings — an image
        # id, a ticket, a path — and is a locator, not a source statement.
        "source_id": "census_1840_chicago_familysearch_images",
        "note": existing.get("note"),
        # REPLACE this pass, never append it. The row was appended unconditionally
        # and the file had accumulated two identical T-0505 passes by the time
        # T-0598 rebuilt it; read_voter_lists.py had already learned this. Rows
        # another pass wrote are carried through untouched.
        "passes": [x for x in (existing.get("passes") or [])
                   if x.get("ticket") != TICKET] + [{
            "ticket": TICKET,
            "what": "every named head on the %d left sheets read in this repo, "
                    "adjudicated against the residents layer, the voter lists, the "
                    "letter-list names and the recovered v1 bridge rows"
                    % len({r["familysearch_id"] for r in doc["heads"]}),
            "heads_adjudicated": doc["counts"]["named_heads"],
            "outcomes": doc["counts"],
            "candidates_are_not_here": "a candidate is neither a merge nor a refusal and "
                    "has no shape in this file; the %d of them live in "
                    "data/research/census_1840/resident_crosswalk.json with their rules."
                    % doc["counts"]["candidate"],
        }],
        "merges": merges,
        "refusals": refusals,
    }


def report(baseline_path: str | None = None) -> int:
    """T-0714 — say what the sheets produced, per sheet, as a number.

    The question the owner asked of this whole layer is "did reading those pages
    produce anything?", and until now the only answer was the total. A sheet is the
    unit that gets READ, so a sheet is the unit the answer has to come in. With
    --baseline <an earlier resident_crosswalk.json> it also names which heads the
    re-derivation ADDED and which outcomes moved, because a re-derivation that moves
    a claim about a person has to be readable line by line, not trusted wholesale.
    """
    if not OUT.exists():
        print("MISSING: %s — run --build" % OUT.relative_to(ROOT))
        return 1
    doc = load(OUT)
    heads = doc.get("heads") or []

    def sheet_key(row):
        return (row.get("printed_page"), row.get("familysearch_id"))

    def page_label(page):
        # 33S7-9YYJ-9MX carries `printed_page: "unknown"` — the number is torn off the
        # image, not missing from the reading. Say that rather than printing None.
        return "unknown" if page in (None, "", "unknown") else str(page)

    sheets: dict = {}
    for row in heads:
        s = sheets.setdefault(sheet_key(row), {"matched": 0, "candidate": 0, "refused": 0})
        s[row["outcome"]] = s.get(row["outcome"], 0) + 1

    print("NAMED 1840 HEADS ADJUDICATED, BY SHEET — %d head(s) off %d sheet(s)"
          % (len(heads), len(sheets)))
    print("  %-8s %-16s %6s %8s %10s %8s" % ("printed", "familysearch", "heads",
                                             "matched", "candidate", "refused"))
    for (page, fsid), s in sorted(sheets.items(), key=lambda kv: (kv[0][0] or 0, kv[0][1])):
        n = s["matched"] + s["candidate"] + s["refused"]
        print("  %-8s %-16s %6d %8d %10d %8d"
              % (page_label(page), fsid, n, s["matched"], s["candidate"], s["refused"]))
    print("  %-8s %-16s %6d %8d %10d %8d"
          % ("total", "", len(heads), doc["counts"]["matched"],
             doc["counts"]["candidate"], doc["counts"]["refused"]))

    if not baseline_path:
        return 0

    was = json.loads(Path(baseline_path).read_text())

    def line_key(row):
        return (row.get("familysearch_id"), row.get("printed_page"), row.get("line"),
                row.get("as_read"))

    before = {line_key(r): r for r in (was.get("heads") or [])}
    added = [r for r in heads if line_key(r) not in before]
    dropped = [r for r in before.values() if line_key(r) not in {line_key(h) for h in heads}]

    by_sheet: dict = {}
    for row in added:
        by_sheet[sheet_key(row)] = by_sheet.get(sheet_key(row), 0) + 1
    print()
    print("AGAINST %s — %d head(s) added, %d dropped"
          % (baseline_path, len(added), len(dropped)))
    for (page, fsid), n in sorted(by_sheet.items(), key=lambda kv: (kv[0][0] or 0, kv[0][1])):
        print("  added  printed %-7s %-16s %4d" % (page_label(page), fsid, n))
    for row in dropped:
        print("  DROPPED  printed %-7s line %-3s %s"
              % (page_label(row.get("printed_page")), row.get("line"),
                 row.get("normalized")))

    moved = [(before[line_key(r)], r) for r in heads
             if line_key(r) in before and before[line_key(r)]["outcome"] != r["outcome"]]
    print()
    print("  %d head(s) already on disk changed outcome" % len(moved))
    for old_row, row in sorted(moved, key=lambda pair: (pair[1].get("printed_page") or 0,
                                                        pair[1].get("line") or 0)):
        print("  %-10s -> %-10s printed %-7s line %-3s %-24s %s"
              % (old_row["outcome"], row["outcome"], page_label(row.get("printed_page")),
                 row.get("line"), row.get("normalized"), row["rule"]))
    return 0


def check() -> int:
    if not OUT.exists():
        print("MISSING: %s — run --build" % OUT.relative_to(ROOT))
        return 1
    on_disk = load(OUT)
    fresh = build()
    fresh.pop("_person_names", None)
    bad = []
    if on_disk.get("counts") != fresh.get("counts"):
        bad.append("counts on disk %r do not follow from the inputs %r"
                   % (on_disk.get("counts"), fresh.get("counts")))
    if len(on_disk.get("heads") or []) != len(fresh["heads"]):
        bad.append("%d head(s) on disk, %d read from the pages"
                   % (len(on_disk.get("heads") or []), len(fresh["heads"])))
    for row in on_disk.get("heads") or []:
        if not row.get("rule") or not row.get("reason"):
            bad.append("a head with no rule or no reason: %r" % row.get("normalized"))
            break
        if row["outcome"] == "matched" and not row.get("proposed_later_census"):
            bad.append("a matched head with no proposed later_census: %r"
                       % row.get("normalized"))
            break
        if row["outcome"] == "matched" and not (row.get("discriminators") or []):
            bad.append("a matched head with no discriminator: %r" % row.get("normalized"))
            break
    legacy = (on_disk.get("legacy_29_readjudicated") or {}).get("heads") or []
    if len(legacy) != 29:
        bad.append("%d legacy head(s) re-adjudicated, expected 29" % len(legacy))
    for bad_line in bad:
        print("BAD: %s" % bad_line)
    if bad:
        return 1
    print("OK: %d named 1840 head(s) — %d matched, %d candidate, %d refused; "
          "%d legacy head(s) re-adjudicated"
          % (fresh["counts"]["named_heads"], fresh["counts"]["matched"],
             fresh["counts"]["candidate"], fresh["counts"]["refused"], len(legacy)))
    return 0


def self_test() -> int:
    failures = []

    def expect(label, got, want):
        if got != want:
            failures.append("%s: got %r, wanted %r" % (label, got, want))

    expect("Wm expands", parse_name("Wm Hanford Adams")["forename"], "william")
    expect("Cha[?]. M. Snow is uncertain", parse_name("Cha[?]. M. Snow")["uncertain"], True)
    expect("suffix dropped", parse_name("H. R. Clark Jr.")["surname"], "clark")
    expect("initials only have no forename", parse_name("W. J. H. Eldridge")["forename"], "")
    expect("firm tail", parse_name("Ch. Ke[?]ch & Co.")["firm"], True)
    expect("Jno folds to John", parse_name("Jno Miller")["key"], "john|miller")

    doc = build()
    expect("no merge in the domain crosswalk lacks a person id",
           all(m.get("person_id") for m in domain_crosswalk(doc)["merges"]), True)
    expect("every domain refusal names both spellings in its rule",
           all(r["a"] in r["rule"] and r["b"] in r["rule"]
               for r in domain_crosswalk(doc)["refusals"]), True)
    expect("every head has an outcome",
           all(r.get("outcome") in ("matched", "candidate", "refused") for r in doc["heads"]),
           True)
    expect("every head has a rule and a reason",
           all(r.get("rule") and r.get("reason") for r in doc["heads"]), True)
    expect("every matched head has a discriminator",
           all(r.get("discriminators") for r in doc["heads"] if r["outcome"] == "matched"),
           True)
    expect("every matched head proposes a later_census block",
           all(r.get("proposed_later_census") for r in doc["heads"] if r["outcome"] == "matched"),
           True)
    expect("no proposed block asserts a serial",
           all(r["proposed_later_census"]["serial"] is None
               for r in doc["heads"] if r["outcome"] == "matched"), True)
    expect("counts add up",
           doc["counts"]["matched"] + doc["counts"]["candidate"] + doc["counts"]["refused"],
           doc["counts"]["named_heads"])
    expect("the 29 legacy heads are all re-adjudicated",
           len(doc["legacy_29_readjudicated"]["heads"]), 29)
    expect("no legacy head is left without a reason",
           all(h.get("reason") for h in doc["legacy_29_readjudicated"]["heads"]), True)
    for line in failures:
        print("FAIL: %s" % line)
    print("self-test: %d assertion(s) failed" % len(failures))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--report", action="store_true",
                    help="what each sheet produced, as a number per sheet")
    ap.add_argument("--baseline", metavar="PATH",
                    help="an earlier resident_crosswalk.json; --report then names the "
                         "heads added and the outcomes that moved")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.report:
        return report(args.baseline)
    if args.check:
        return check()
    if args.build:
        doc = build()
        cross = domain_crosswalk(doc)
        doc.pop("_person_names", None)
        OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        DOMAIN_CROSSWALK.write_text(json.dumps(cross, indent=2, ensure_ascii=False) + "\n")
        print("wrote %s — %d merge(s), %d refusal(s)"
              % (DOMAIN_CROSSWALK.relative_to(ROOT), len(cross["merges"]),
                 len(cross["refusals"])))
        print("wrote %s — %d head(s): %d matched, %d candidate, %d refused"
              % (OUT.relative_to(ROOT), doc["counts"]["named_heads"],
                 doc["counts"]["matched"], doc["counts"]["candidate"],
                 doc["counts"]["refused"]))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
