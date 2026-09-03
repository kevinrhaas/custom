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
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
PROJECTED = "projected_resident"

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


def independent(item):
    return [s for s in item.get("sources") or []
            if s not in {"chicago_democrat_1833_1835", "chicago_american_1835"}]


def evidence_text(item):
    bits = [item.get("proposed_facts") or "", item.get("evidence_for") or "", item.get("summary") or ""]
    for sid in independent(item):
        doc = source_doc(sid)
        bits += [str(doc.get(k) or "") for k in ("citation","locator","note","describes_date")]
    return " ".join(bits)


def promote(person, hh, item):
    srcs = independent(item)
    if not srcs: return []
    text = evidence_text(item); low = text.lower(); changes = []
    for pat, occ in OCCUPATIONS:
        if re.search(pat, low):
            old = person.get("occupation") or {}
            if value(old) in (None, "", "none_recorded") or old.get("confidence") == "reconstructed":
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
    return changes


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


def rebuild_index(index, docs, stats):
    old={r.get("id"):r for r in index.get("households") or []}; rows=[]; grades=Counter(); letter=projected=census=0
    for path,doc in sorted(docs.items(),key=lambda kv:kv[1].get("id",kv[0].name)):
        people=doc.get("persons") or []; g=Counter(p.get("grade") for p in people if p.get("grade")); grades.update(g)
        ll=sum(bool(p.get("letter_list_only")) for p in people); pr=sum(p.get("resident_subtype")==PROJECTED for p in people); ce=sum(bool(p.get("later_census")) for p in people)
        letter+=ll; projected+=pr; census+=ce; hid=doc.get("id"); row=dict(old.get(hid) or {})
        row.update({"id":hid,"file":f"households/{path.name}","head":doc.get("head"),"division":doc.get("division"),
                    "persons":len(people),"grades":dict(sorted(g.items())),"lives_at":value(doc.get("lives_at")),
                    "works_at":value(doc.get("works_at")),"present_on_scene_date":value(doc.get("present_on_scene_date")),
                    "review_required":bool(doc.get("review_required"))})
        if ll: row["letter_list_only"]=True
        else: row.pop("letter_list_only",None)
        if pr: row["projected_resident"]=True
        else: row.pop("projected_resident",None)
        if ce: row["census_1840_linked"]=ce
        else: row.pop("census_1840_linked",None)
        rows.append(row)
    index["households"]=rows; index.setdefault("vocabulary",{})["grades"]=["attested","inferred","reconstructed"]
    index["vocabulary"]["resident_subtypes"]=[PROJECTED]
    counts=dict(index.get("counts") or {}); counts.update({"households":len(rows),"persons":sum(r["persons"] for r in rows),
        "by_grade":{"attested":grades.get("attested",0),"inferred":grades.get("inferred",0),"reconstructed":grades.get("reconstructed",0)},
        "letter_list_only":letter,"projected_residents":projected,"census_1840_linked":census,
        "reconstructed_removed_in_2026_09_02_synthesis":stats["removed_people"]})
    index["counts"]=counts
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
      "## Profile enrichment","",f"Structured promotion changed **{len(promoted)} corroborated profiles** where independent sources state usable facts (occupation, Chicago arrival year, birth-year/family evidence). Candidate-only matches never supply canonical facts.",""]
    for row in promoted[:60]: lines.append(f"- `{row['person_id']}` ({row['ticket']}): "+", ".join(row["changes"]))
    lines += ["","## 1840 census evidence","",f"**{len(census.get('linked') or [])} one-to-one resident links** were made to named 1840 census heads. Each link retains serial/page/row and separate name/serial mapping confidence plus household totals.","",
      "**1840 is later evidence, not the 1835 household.** Children, spouses, ages and industry totals are not projected backward without a separate bridge.","",
      f"Unmatched named 1840 heads: **{len(census.get('unmatched_named_heads') or [])}**; ambiguous links: **{len(census.get('ambiguous') or [])}**. These remain follow-up research rather than silent 1835 promotions.","",
      "The committed census workbooks are inventoried in the machine ledger (sheet names/dimensions/probable headers) but no 1835 resident is minted solely from an 1840 appearance.","",
      "## Placement / structures","","The retained evidence population is intentionally allowed to be unplaced. Structures that only inherited occupants from the retired reconstructed-household programme remain as anonymous/unassigned building stock for the later full placement sweep; no replacement home or workplace was invented here.",""]
    return "\n".join(lines)


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
    for path in STRUCTURES.glob("inf_*.json"):
        d=load(path); a=d.get("resident_assignment") or {}
        if a.get("status") != "unassigned":
            problems.append(f"{path.name} is inferred stock without resident_assignment=unassigned")
    if problems:
        print("RESIDENT SYNTHESIS FAIL"); [print(" -",p) for p in problems]; return 1
    print(f"OK: {len(people)} people; {actual.get('attested',0)} attested, {actual.get('inferred',0)} inferred, 0 reconstructed; {sum(p.get('resident_subtype')==PROJECTED for p in people)} projected")
    return 0


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args()
    if args.check: return check()
    index=load(INDEX); current_before=snapshot(index)
    prior_ledger=load(LEDGER) if LEDGER.exists() else {}
    before=(prior_ledger.get("before") if current_before.get("reconstructed")==0 and prior_ledger.get("before") else current_before)
    docs={p:load(p) for p in sorted(HOUSEHOLDS.glob("*.json"))}; research=research_rows()
    stats={"removed_people":0,"removed_households":0,"retained_hh_inf":0,"structures_unassigned":0}; removed_people=set(); removed_hh=set(); unlink_people=set()
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
            doc["research_note"]=((doc.get("research_note") or "")+" T-0489: reconstructed occupancy retired; evidence-based person retained and unplaced.").strip()
    if prior_ledger and stats["removed_people"] == 0 and stats["removed_households"] == 0:
        prior_retirement=prior_ledger.get("retirement") or {}
        stats["removed_people"]=int(prior_retirement.get("removed_people") or 0)
        stats["removed_households"]=int(prior_retirement.get("removed_households") or 0)
    persons={p.get("id"):(p,d) for d in docs.values() for p in d.get("persons") or [] if p.get("id")}
    outcomes=Counter(); promoted=[]; unmatched=[]
    for pid,item in sorted(research.items()):
        outcome=item.get("outcome") or "no_corroboration_yet"; outcomes[outcome]+=1
        if pid not in persons: unmatched.append({"person_id":pid,"outcome":outcome,"name":item.get("name_normalized")}); continue
        p,hh=persons[pid]; p["resident_research"]=research_block(item)
        if p.get("letter_list_only"):
            if outcome in CORROBORATED:
                p["grade"]="attested"; p.pop("resident_subtype",None); p["sources"]=list(dict.fromkeys((p.get("sources") or [])+independent(item)))
                prefix="INDEPENDENTLY CORROBORATED RESIDENT. "
            else:
                p["grade"]="inferred"; p["resident_subtype"]=PROJECTED
                prefix="PROJECTED RESIDENT. Documented in Chicago post-office evidence but not independently corroborated strongly enough for attested circa-1835 residence. "
            existing = p.get("note") or ""
            existing = re.sub(r"^(?:INDEPENDENTLY CORROBORATED RESIDENT\. |PROJECTED RESIDENT\. Documented in Chicago post-office evidence but not independently corroborated strongly enough for attested circa-1835 residence\. )", "", existing, flags=re.I)
            if outcome in CORROBORATED:
                existing = re.sub(r"^KNOWN ONLY FROM THE POST OFFICE\.\s*", "", existing, flags=re.I)
                existing = re.sub(r"Nothing else in the corpus names this person[^.]*\.\s*", "", existing, flags=re.I)
                existing = re.sub(r"No (?:arrival|trade|occupation)[^.]*\.\s*", "", existing, flags=re.I)
                prefix = "INDEPENDENTLY CORROBORATED RESIDENT. Originally documented in Chicago post-office evidence; independent resident research now corroborates the identity. "
            p["note"]=(prefix+existing).strip()
        if outcome in CORROBORATED:
            changes=promote(p,hh,item)
            if changes: promoted.append({"person_id":pid,"ticket":item.get("ticket"),"changes":changes,"source_ids":independent(item)})
    missing=[]
    for pid,(p,_hh) in persons.items():
        if p.get("letter_list_only") and pid not in research: p["grade"]="inferred"; p["resident_subtype"]=PROJECTED; missing.append(pid)
    ledger={"date":"2026-09-02","scene_date":"1835-07-01","tickets":["T-0487","T-0488","T-0489","T-0490"],
        "owner_ruling":{"attested":"confidently corroborated real named circa-1835 Chicago resident","inferred":"real named person reasonably believed to belong to circa-1835 Chicago","projected_resident":"inferred subtype documented in at least one relevant source but too thin/ambiguous for stronger profile","reconstructed":"reserved for later explicit reconstruction; zero now"},
        "research":{"reviewed_people":len(research),"outcome_counts":dict(sorted(outcomes.items())),"unmatched_research_person_ids":unmatched,"letter_list_missing_research_row":missing,"promoted_facts":promoted},
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
        if sid.startswith("inf_"):
            doc["resident_assignment"]={"status":"unassigned","confidence":"reconstructed","note":"T-0489 owner ruling 2026-09-02: reconstructed resident population retired; building retained as anonymous stock for later placement."}; stats["structures_unassigned"]+=1
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
    for p,d in docs.items(): dump(sitehh/p.name,d,1)
    (SITE/"data"/"residents"/"index.json").write_text(INDEX.read_text(encoding="utf-8"),encoding="utf-8")
    sitestruct=SITE/"data"/"structures"
    if sitestruct.exists():
        for p in changed:
            q=sitestruct/p.name
            if q.exists(): q.write_text(p.read_text(encoding="utf-8"),encoding="utf-8")
    print(json.dumps({"before":before,"after":after,"research_reviewed":len(research),"outcomes":dict(outcomes),"promoted_profiles":len(promoted),"census_links":len((ledger.get("census_1840") or {}).get("linked") or []),"retirement":stats},indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
