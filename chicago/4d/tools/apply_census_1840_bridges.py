#!/usr/bin/env python3
"""Apply/check adjudicated 1840 census identity bridges (issue #669).

This intentionally does not fuzzy-match census names.  The bridge CSV is the
adjudication boundary: only an existing canonical person_id explicitly present
there may receive a later_census record.  Household counts remain dated 1840
and never mint 1835 household members.
"""
from __future__ import annotations

import argparse
import csv
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
SCOPE = RESEARCH / "census_1840_row_serial_scope.json"
LEDGER = RESEARCH / "synthesis_2026_09_02.json"
SUMMARY = ROOT / "docs" / "RESEARCH" / "resident-household-synthesis-2026-09-02.md"
SITE = ROOT.parent.parent / "site" / "chicago" / "4d"
SOURCE_ID = "census_1840_chicago_v4_research"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc, indent=1):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")


def as_int(row, key):
    v = (row.get(key) or "").strip()
    return int(v) if v else None


def bridge_rows():
    with BRIDGES.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    seen_person = set(); seen_serial = set()
    for row in rows:
        pid = row["person_id"].strip(); serial = as_int(row, "serial")
        if not pid or pid in seen_person:
            raise ValueError(f"duplicate/blank bridge person_id: {pid!r}")
        if serial is None or serial in seen_serial:
            raise ValueError(f"duplicate/blank bridge serial: {serial!r}")
        seen_person.add(pid); seen_serial.add(serial)
    return rows


def later_census(row):
    return {
        "year": 1840,
        "source_id": SOURCE_ID,
        "serial": as_int(row, "serial"),
        "head_name_transcribed": row["census_name"].strip(),
        "head_name_normalized": row["canonical_name"].strip(),
        "name_confidence": row["identity_confidence"].strip().title(),
        "identity_confidence": row["identity_confidence"].strip().title(),
        "serial_mapping_confidence": row["serial_mapping_confidence"].strip().replace("-", " ").title(),
        "census_page": as_int(row, "census_page"),
        "census_row": as_int(row, "census_row"),
        "source_image": row["source_image"].strip() or None,
        "household": {
            "persons": as_int(row, "persons_1840"),
            "children_under_10": as_int(row, "children_under_10_1840"),
            "male": as_int(row, "male_1840"),
            "female": as_int(row, "female_1840"),
        },
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


def update_ledger(rows):
    ledger = load(LEDGER)
    old = dict(ledger.get("census_1840") or {})
    scope = load(SCOPE)
    linked = [{"person_id":r["person_id"].strip(), "serial":as_int(r,"serial"), "name":r["canonical_name"].strip(),
               "page":as_int(r,"census_page"), "row":as_int(r,"census_row"),
               "identity_confidence":r["identity_confidence"].strip(),
               "serial_mapping_confidence":r["serial_mapping_confidence"].strip()} for r in rows]
    ledger["census_1840"] = {
        "recovery_issue": 669,
        "v4_named_heads_reviewed": int(scope["named_household_head_rows_under_review"]),
        "v4_best_resident_set_rows_with_serial": int(scope["best_resident_set_rows_with_serial"]),
        "linked": linked,
        "validated_identity_bridges": len(linked),
        "not_promoted_from_v4_to_1835": int(scope["named_household_head_rows_under_review"]) - len(linked),
        "ambiguous": [],
        "legacy_partial_matcher": {
            "eligible_named_rows": old.get("eligible_named_rows"),
            "linked": old.get("linked") or [],
            "ambiguous": old.get("ambiguous") or [],
            "unmatched_named_heads": old.get("unmatched_named_heads") or [],
            "rule": old.get("rule"),
        },
        "rule": "Explicit adjudicated person_id bridges from recovered v4 research only. No fuzzy/common-name promotion; 1840 household facts remain dated later evidence."
    }
    dump(LEDGER, ledger, 2)


def update_summary(nlinks):
    text = SUMMARY.read_text(encoding="utf-8")
    text = re.sub(r"\| Linked to named 1840 census household \|\s*0\s*\|\s*\d+\s*\|",
                  f"| Linked to named 1840 census household | 0 | {nlinks} |", text)
    section = f'''## 1840 census evidence

**{nlinks} validated 1835↔1840 identity links** are now attached to canonical residents from the recovered v4 census/resident adjudication: John Murphy (1840 p.233 r.30, IPUMS SERIAL 5102066) and William Hanford Adams (p.229 r.9, SERIAL 5101954). Both retain identity and SERIAL-mapping confidence separately.

The recovered v4 work covers **210 named 1840 household heads on printed pages 229–235** and carries **117 row→IPUMS SERIAL assignments** in the best-resident set. Those 117 SERIAL-bearing rows are not 117 asserted 1835 identities: only the two direct/high-confidence bridges above are promoted to the canonical 1835 layer; the rest remain later-only or candidate evidence pending an independent 1835 bridge.

**1840 is later evidence, not the 1835 household.** Household totals, children, sex structure and industry variables are retained under `later_census` for household-reconciliation research, but are not projected backward to 1 July 1835. In particular, the 1840 Murphy household has 6 persons (2 children under 10; 3 male; 3 female) and the Adams household has 2 persons (1 male; 1 female); no missing 1835 spouse/child is minted from those counts alone.

The old September 2 result of “0 links / 29 unmatched heads” is retained in the machine ledger as the **legacy partial matcher** result. It came from the older pages-234/235 CSV plus exact normalized-name matching and did not consume the later v4 adjudication.

'''
    text = re.sub(r"## 1840 census evidence\n.*?(?=## Placement / structures)", section, text, flags=re.S)
    SUMMARY.write_text(text, encoding="utf-8")


def apply():
    rows = bridge_rows(); docs, people = docs_and_people()
    for row in rows:
        pid = row["person_id"].strip()
        if pid not in people:
            raise SystemExit(f"bridge person_id not found in canonical residents: {pid}")
        person, _path, _doc = people[pid]
        person["later_census"] = later_census(row)
    for path, doc in docs.items(): dump(path, doc, 1)
    index = rebuild_index(load(INDEX), docs); dump(INDEX, index, 1)
    update_ledger(rows); update_summary(len(rows))
    site_hh = SITE / "data" / "residents" / "households"; site_hh.mkdir(parents=True, exist_ok=True)
    for row in rows:
        _person, path, doc = people[row["person_id"].strip()]
        dump(site_hh / path.name, doc, 1)
    site_index = SITE / "data" / "residents" / "index.json"; site_index.parent.mkdir(parents=True, exist_ok=True)
    site_index.write_text(INDEX.read_text(encoding="utf-8"), encoding="utf-8")
    return check()


def check():
    rows = bridge_rows(); docs, people = docs_and_people(); problems=[]
    expected = {r["person_id"].strip(): r for r in rows}
    actual_links = {pid:p.get("later_census") for pid,(p,_path,_doc) in people.items() if p.get("later_census")}
    for pid, row in expected.items():
        if pid not in people:
            problems.append(f"bridge person missing: {pid}"); continue
        got = people[pid][0].get("later_census") or {}
        if got.get("serial") != as_int(row,"serial") or got.get("census_page") != as_int(row,"census_page") or got.get("census_row") != as_int(row,"census_row"):
            problems.append(f"bridge drift for {pid}")
    unexpected = sorted(set(actual_links) - set(expected))
    if unexpected: problems.append(f"later_census exists outside adjudicated bridge sidecar: {unexpected}")
    index = load(INDEX); counts=index.get("counts") or {}
    if int(counts.get("census_1840_linked") or 0) != len(rows): problems.append("index census_1840_linked disagrees with bridge CSV")
    if int(counts.get("households") or 0) != len(docs): problems.append("index household count disagrees with records")
    people_count=sum(len(d.get("persons") or []) for d in docs.values())
    if int(counts.get("persons") or 0) != people_count: problems.append("index person count disagrees with records")
    ledger=load(LEDGER); census=ledger.get("census_1840") or {}
    if int(census.get("validated_identity_bridges") or 0) != len(rows): problems.append("ledger bridge count disagrees")
    summary=SUMMARY.read_text(encoding="utf-8")
    if f"**{len(rows)} validated 1835↔1840 identity links**" not in summary: problems.append("summary census section is stale")
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
    print(f"OK: {len(rows)} validated census identity bridges; {len(docs)} households; {people_count} canonical persons; no 1840 household members back-projected")
    return 0


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__": raise SystemExit(main())
