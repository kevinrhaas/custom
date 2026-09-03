#!/usr/bin/env python3
"""Apply/check recovered 1840 census household evidence and 1835 identity bridges.

Issue #669.  The 210-row census dataset is dated 1840 evidence.  The bridge CSV
is the adjudication boundary for attaching an 1840 head to an existing 1835
canonical resident.  `validated` and `provisional` are kept distinct, and no
1840 spouse/child/boarder is minted into the 1835 household from census counts.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HOUSEHOLDS = DATA / "residents" / "households"
INDEX = DATA / "residents" / "index.json"
RESEARCH = DATA / "research" / "residents"
BRIDGES = RESEARCH / "census_1840_identity_bridges.csv"
CENSUS_DIR = DATA / "census" / "1840"
CENSUS_INDEX = CENSUS_DIR / "index.json"
CENSUS_ROWS = CENSUS_DIR / "household_heads.csv.gz"
LEDGER = RESEARCH / "synthesis_2026_09_02.json"
SUMMARY = ROOT / "docs" / "RESEARCH" / "resident-household-synthesis-2026-09-02.md"
SITE = ROOT.parent.parent / "site" / "chicago" / "4d"
SOURCE_ID = "census_1840_chicago_v4_research"
ALLOWED_STATUS = {"validated", "provisional"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc, indent=1):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")


def as_int(row, key):
    v = str(row.get(key) or "").strip()
    return int(v) if v else None


def census_rows():
    if not CENSUS_ROWS.exists():
        raise ValueError(f"missing census evidence file: {CENSUS_ROWS}")
    with gzip.open(CENSUS_ROWS, "rt", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    manifest = load(CENSUS_INDEX)
    expected = int(manifest.get("records") or 0)
    if len(rows) != expected or expected != 210:
        raise ValueError(f"census household row count drift: file={len(rows)} manifest={expected}, expected 210")
    serials = [as_int(r, "serial") for r in rows]
    if any(s is None for s in serials) or len(set(serials)) != len(serials):
        raise ValueError("1840 SERIAL values are blank or non-unique")
    pages = sorted({as_int(r, "page") for r in rows})
    if pages != [229, 230, 231, 232, 233, 234, 235]:
        raise ValueError(f"unexpected census page coverage: {pages}")
    return rows


def bridge_rows():
    with BRIDGES.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    seen_person = set(); seen_serial = set()
    for row in rows:
        pid = row["person_id"].strip(); serial = as_int(row, "serial")
        status = (row.get("bridge_status") or "").strip()
        if status not in ALLOWED_STATUS:
            raise ValueError(f"invalid bridge_status for {pid}: {status!r}")
        if not pid or pid in seen_person:
            raise ValueError(f"duplicate/blank bridge person_id: {pid!r}")
        if serial is None or serial in seen_serial:
            raise ValueError(f"duplicate/blank bridge serial: {serial!r}")
        seen_person.add(pid); seen_serial.add(serial)
    return rows


def census_lookup(rows):
    return {as_int(r, "serial"): r for r in rows}


def later_census(row, census):
    serial = as_int(row, "serial")
    source = census[serial]
    household = {
        "persons": as_int(source, "persons"),
        "children_under_10": as_int(source, "children_lt_10"),
        "male": as_int(source, "males"),
        "female": as_int(source, "females"),
        "agriculture": as_int(source, "agriculture"),
        "commerce": as_int(source, "commerce"),
        "manufactures_trades": as_int(source, "manufactures_trades"),
        "inland_navigation": as_int(source, "inland_navigation"),
        "professions_engineering": as_int(source, "professions_engineering"),
        "foreigners_not_naturalized": as_int(source, "foreigners_not_naturalized"),
        "illiterate_over_21": as_int(source, "illiterate_gt_21"),
    }
    return {
        "year": 1840,
        "source_id": SOURCE_ID,
        "serial": serial,
        "head_name_transcribed": source.get("raw_scan_reading") or row["census_name"].strip(),
        "head_name_normalized": source.get("preferred_name") or row["canonical_name"].strip(),
        "name_confidence": source.get("name_confidence") or row["identity_confidence"].strip().title(),
        "identity_confidence": row["identity_confidence"].strip().title(),
        "bridge_status": row["bridge_status"].strip(),
        "serial_mapping_confidence": source.get("serial_confidence") or row["serial_mapping_confidence"].strip(),
        "census_page": as_int(source, "page"),
        "census_row": as_int(source, "row"),
        "source_image": source.get("source_image") or row["source_image"].strip() or None,
        "source_kind": source.get("source_kind") or None,
        "household": household,
        "bridge_basis": row["bridge_basis"].strip(),
        "note": "LATER EVIDENCE, NOT A BACK-PROJECTION. This is the 1840 federal census household, five years after the 1835-07-01 scene; its household composition is not asserted for 1835 without separate evidence."
    }


def docs_and_people():
    docs = {p: load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))}
    people = {}
    for path, doc in docs.items():
        for person in doc.get("persons") or []:
            pid = person.get("id")
            if pid:
                if pid in people:
                    raise ValueError(f"duplicate canonical person id: {pid}")
                people[pid] = (person, path, doc)
    return docs, people


def rebuild_index(index, docs):
    old = {r.get("id"): r for r in index.get("households") or []}
    rows=[]; grades=Counter(); letter=projected=census=0
    for path, doc in sorted(docs.items(), key=lambda kv: kv[1].get("id", kv[0].name)):
        people = doc.get("persons") or []
        g = Counter(p.get("grade") for p in people if p.get("grade")); grades.update(g)
        ll = sum(bool(p.get("letter_list_only")) for p in people)
        pr = sum(p.get("resident_subtype") == "projected_resident" for p in people)
        ce = sum(bool(p.get("later_census")) for p in people)
        letter += ll; projected += pr; census += ce
        hid = doc.get("id"); row = dict(old.get(hid) or {})
        def val(block): return block.get("value") if isinstance(block, dict) else block
        row.update({"id":hid,"file":f"households/{path.name}","head":doc.get("head"),
                    "division":doc.get("division"),"persons":len(people),
                    "grades":dict(sorted(g.items())),"lives_at":val(doc.get("lives_at")),
                    "works_at":val(doc.get("works_at")),
                    "present_on_scene_date":val(doc.get("present_on_scene_date")),
                    "review_required":bool(doc.get("review_required"))})
        if ll: row["letter_list_only"] = True
        else: row.pop("letter_list_only", None)
        if pr: row["projected_resident"] = True
        else: row.pop("projected_resident", None)
        if ce: row["census_1840_linked"] = ce
        else: row.pop("census_1840_linked", None)
        rows.append(row)
    index["households"] = rows
    counts = dict(index.get("counts") or {})
    counts.update({
        "households": len(rows),
        "persons": sum(r["persons"] for r in rows),
        "by_grade": {"attested": grades.get("attested",0), "inferred": grades.get("inferred",0), "reconstructed": grades.get("reconstructed",0)},
        "letter_list_only": letter,
        "projected_residents": projected,
        "census_1840_linked": census,
    })
    index["counts"] = counts
    return index


def update_ledger(rows, all_census):
    ledger = load(LEDGER)
    old = dict(ledger.get("census_1840") or {})
    linked = [{"person_id":r["person_id"].strip(), "serial":as_int(r,"serial"), "name":r["canonical_name"].strip(),
               "page":as_int(r,"census_page"), "row":as_int(r,"census_row"),
               "bridge_status":r["bridge_status"].strip(),
               "identity_confidence":r["identity_confidence"].strip(),
               "serial_mapping_confidence":r["serial_mapping_confidence"].strip()} for r in rows]
    validated = [r for r in linked if r["bridge_status"] == "validated"]
    provisional = [r for r in linked if r["bridge_status"] == "provisional"]
    ledger["census_1840"] = {
        "recovery_issue": 669,
        "named_household_heads_retained": len(all_census),
        "serial_linked_household_heads_retained": len(all_census),
        "linked": linked,
        "validated_identity_bridges": len(validated),
        "provisional_identity_bridges": len(provisional),
        "not_yet_linked_to_canonical_1835_resident": len(all_census) - len(linked),
        "legacy_partial_matcher": {
            "eligible_named_rows": old.get("eligible_named_rows"),
            "linked": old.get("linked") or [],
            "ambiguous": old.get("ambiguous") or [],
            "unmatched_named_heads": old.get("unmatched_named_heads") or [],
            "rule": old.get("rule"),
        },
        "rule": "All 210 resolved 1840 row-to-SERIAL household records are retained as dated evidence. Canonical 1835 links require an explicit adjudicated person_id bridge and are graded validated or provisional; no fuzzy/common-name promotion."
    }
    dump(LEDGER, ledger, 2)


def update_summary(rows, all_census):
    validated = [r for r in rows if r["bridge_status"] == "validated"]
    provisional = [r for r in rows if r["bridge_status"] == "provisional"]
    nlinks = len(rows)
    text = SUMMARY.read_text(encoding="utf-8")
    text = re.sub(r"\| Linked to named 1840 census household \|\s*0\s*\|\s*\d+\s*\|",
                  f"| Linked to named 1840 census household | 0 | {nlinks} |", text)
    section = f'''## 1840 census evidence

The recovered v4 work is now retained as a complete dated census layer: **{len(all_census)} named 1840 household-head rows on printed pages 229–235, all with resolved IPUMS SERIALs and household demographic fields**. These records live under `data/census/1840/` whether or not they can yet be tied safely to a 1 July 1835 resident.

Canonical resident linkage is a separate assertion. There are currently **{len(validated)} validated High-confidence 1835↔1840 identity bridges** — John Murphy (1840 p.233 r.30, SERIAL 5102066) and William Hanford Adams (p.229 r.9, SERIAL 5101954) — plus **{len(provisional)} provisional bridge**, John Miller ↔ John J. Miller (p.232 r.3, SERIAL 5102035). Miller is independently attested as the Chicago tanner and 1833 trustee, but the 1840 middle initial is new, so the link remains Medium/provisional rather than High.

**1840 is later evidence, not the 1835 household.** Household totals, children, sex structure, industry, foreigner and literacy fields are retained under the census dataset and `later_census` links for household-reconciliation research, but are not projected backward to 1 July 1835. Murphy's 1840 household has 6 people; Adams 2; Miller 5. Those counts do not themselves mint spouses, children, partners, servants or boarders into the 1835 resident layer.

The old September 2 “0 links / 29 unmatched heads” result is preserved in the machine ledger as the **legacy partial matcher** result. It came from the older pages-234/235 partial CSV plus exact normalized-name matching and did not consume the later v4 adjudication.

'''
    text = re.sub(r"## 1840 census evidence\n.*?(?=## Placement / structures)", section, text, flags=re.S)
    SUMMARY.write_text(text, encoding="utf-8")


def apply():
    all_rows = census_rows(); lookup = census_lookup(all_rows)
    rows = bridge_rows(); docs, people = docs_and_people()
    for row in rows:
        pid = row["person_id"].strip(); serial = as_int(row, "serial")
        if pid not in people:
            raise SystemExit(f"bridge person_id not found in canonical residents: {pid}")
        if serial not in lookup:
            raise SystemExit(f"bridge SERIAL not found in 210-row census dataset: {serial}")
        person, _path, _doc = people[pid]
        person["later_census"] = later_census(row, lookup)
    for path, doc in docs.items(): dump(path, doc, 1)
    index = rebuild_index(load(INDEX), docs); dump(INDEX, index, 1)
    update_ledger(rows, all_rows); update_summary(rows, all_rows)
    site_hh = SITE / "data" / "residents" / "households"; site_hh.mkdir(parents=True, exist_ok=True)
    for row in rows:
        _person, path, doc = people[row["person_id"].strip()]
        dump(site_hh / path.name, doc, 1)
    site_index = SITE / "data" / "residents" / "index.json"; site_index.parent.mkdir(parents=True, exist_ok=True)
    site_index.write_text(INDEX.read_text(encoding="utf-8"), encoding="utf-8")
    return check()


def check():
    all_rows = census_rows(); lookup = census_lookup(all_rows)
    rows = bridge_rows(); docs, people = docs_and_people(); problems=[]
    expected = {r["person_id"].strip(): r for r in rows}
    for pid, row in expected.items():
        if pid not in people:
            problems.append(f"bridge person missing: {pid}"); continue
        serial = as_int(row,"serial")
        if serial not in lookup:
            problems.append(f"bridge serial absent from 210-row census dataset: {serial}"); continue
        got = people[pid][0].get("later_census") or {}
        if got.get("serial") != serial or got.get("census_page") != as_int(row,"census_page") or got.get("census_row") != as_int(row,"census_row"):
            problems.append(f"bridge drift for {pid}")
        if got.get("bridge_status") != row.get("bridge_status"):
            problems.append(f"bridge status drift for {pid}")
    actual_links = [p for p,_path,_doc in people.values() if p.get("later_census")]
    index = load(INDEX); counts=index.get("counts") or {}
    if int(counts.get("census_1840_linked") or 0) != len(actual_links): problems.append("index census_1840_linked disagrees with resident records")
    if int(counts.get("households") or 0) != len(docs): problems.append("index household count disagrees with records")
    people_count=sum(len(d.get("persons") or []) for d in docs.values())
    if int(counts.get("persons") or 0) != people_count: problems.append("index person count disagrees with records")
    ledger=load(LEDGER); census=ledger.get("census_1840") or {}
    validated=sum(r["bridge_status"]=="validated" for r in rows); provisional=sum(r["bridge_status"]=="provisional" for r in rows)
    if int(census.get("named_household_heads_retained") or 0) != 210: problems.append("ledger does not retain all 210 census heads")
    if int(census.get("validated_identity_bridges") or 0) != validated: problems.append("ledger validated bridge count disagrees")
    if int(census.get("provisional_identity_bridges") or 0) != provisional: problems.append("ledger provisional bridge count disagrees")
    summary=SUMMARY.read_text(encoding="utf-8")
    if "**210 named 1840 household-head rows" not in summary: problems.append("summary census coverage is stale")
    site_index=SITE/"data"/"residents"/"index.json"
    if not site_index.exists() or site_index.read_text(encoding="utf-8") != INDEX.read_text(encoding="utf-8"): problems.append("published resident index mirror is stale")
    for pid,row in expected.items():
        if pid not in people: continue
        _p,path,_doc=people[pid]; site_path=SITE/"data"/"residents"/"households"/path.name
        if not site_path.exists() or site_path.read_text(encoding="utf-8") != path.read_text(encoding="utf-8"): problems.append(f"published household mirror stale: {path.name}")
    adams=people.get("adams_william_h")
    if adams and len(adams[2].get("persons") or []) != 1: problems.append("Adams 1840 second person was incorrectly back-projected into 1835")
    if problems:
        print("CENSUS BRIDGE FAIL")
        for p in problems: print(" -", p)
        return 1
    print(f"OK: 210 census households retained; {validated} validated + {provisional} provisional resident bridges; {len(docs)} resident households; {people_count} canonical persons")
    return 0


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__": raise SystemExit(main())
