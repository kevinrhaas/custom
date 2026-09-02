#!/usr/bin/env python3
"""One-shot T-0478 closeout helper. Remove after successful use."""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
RESIDENTS = ROOT / "data/residents"
RESEARCH = ROOT / "data/research/residents"
REFERENCE = REPO / "chicago/reference/resident-research/T-0478"
SITE = REPO / "site/chicago/4d"


def run(*args: str, cwd: Path = ROOT) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def wire_gate() -> None:
    path = ROOT / "tools/check.sh"
    text = path.read_text()
    text = text.replace(
        "# T-0442, T-0462, and T-0463. These reviews sit beside household facts on purpose:",
        "# T-0442, T-0462, T-0463, and T-0478. These reviews sit beside household facts on purpose:",
    )
    old = '''step "the third non-overlapping 75-person research cohort is fixed" \\
  python3 tools/select_resident_research_pass_3.py --gate

step "all 225 reviewed residents have reproducible research outcomes" \\
  python3 tools/compile_resident_research_pilot.py --gate'''
    new = '''step "the third non-overlapping 75-person research cohort is fixed" \\
  python3 tools/select_resident_research_pass_3.py --gate

step "the fourth non-overlapping 75-person research cohort is fixed" \\
  python3 tools/select_resident_research_pass_4.py --gate

step "all 300 reviewed residents have reproducible research outcomes" \\
  python3 tools/compile_resident_research_pilot.py --gate'''
    if old in text:
        text = text.replace(old, new, 1)
    elif "the fourth non-overlapping 75-person research cohort is fixed" not in text:
        raise SystemExit("expected resident-research gate block not found")
    path.write_text(text)


def people_index() -> dict[str, tuple[dict, dict]]:
    index_doc = json.loads((RESIDENTS / "index.json").read_text())
    out = {}
    for entry in index_doc["households"]:
        household = json.loads((RESIDENTS / entry["file"]).read_text())
        for person in household.get("persons", []):
            out[person["id"]] = (household, person)
    return out


def source_meta(source_ids: list[str]) -> tuple[str, str, str]:
    urls, tiers, limitations = [], [], []
    for sid in source_ids:
        path = ROOT / "data/sources" / f"{sid}.json"
        if not path.exists():
            continue
        rec = json.loads(path.read_text())
        url = rec.get("url") or rec.get("source_url")
        if url:
            urls.append(url)
        if rec.get("locator"):
            urls.append(f"{sid}: {rec['locator']}")
        if rec.get("tier") is not None:
            tiers.append(f"{sid}:{rec['tier']}")
        limitations.extend(rec.get("what_it_does_not_supply", []))
        if rec.get("note"):
            limitations.append(rec["note"])
    return " | ".join(urls), " | ".join(tiers), " | ".join(limitations)


def write_csv() -> None:
    manifest = json.loads((RESEARCH / "pass_04_75_cohort.json").read_text())
    findings = json.loads((RESEARCH / "pass_04_findings.json").read_text())
    people = people_index()
    headers = [
        "ticket","cohort","person_id","household_id","name_transcribed","name_normalized",
        "stratum","seed_source_id","seed_source_date","letter_list_dates","research_outcome",
        "identity_confidence","residence_confidence","household_confidence","occupation_confidence",
        "candidate_ids","proposed_birth","proposed_death","proposed_arrival_migration",
        "proposed_occupation_trade","proposed_address_property","proposed_spouse_kin",
        "proposed_civic_voter_census","proposed_household_facts","evidence_for","evidence_against",
        "source_ids","source_urls_locators","source_tiers","queries","access_dates",
        "source_limitations","recommended_data_action","notes",
    ]
    candidate_ids = {
        "mulford_e_h": "cand_mulford_james_h",
        "ll_timothy_titcomb": "cand_timothy_titcomb_wheeling",
        "ll_ward_hanibal": "cand_hannibal_ward_dupage",
        "ll_white_edson": "cand_edson_white_joliet",
    }
    proposals = {
        "handy_major": {"proposed_civic_voter_census": "1833 river-improvement work"},
        "mason_matthias": {"proposed_occupation_trade": "blacksmith; shop opened fall 1833"},
        "maxwell_philip": {"proposed_birth": "Full birth data supplied by cited medical history", "proposed_occupation_trade": "Fort Dearborn surgeon, 1833–1836"},
        "mckee_david": {"proposed_occupation_trade": "government/agency blacksmith", "proposed_address_property": "near foot of State Street"},
        "meeker_joseph": {"proposed_arrival_migration": "arrived Chicago early 1833", "proposed_occupation_trade": "builder; Sunday-school librarian 16 Mar 1835", "proposed_civic_voter_census": "First Presbyterian institutional roles"},
        "miller_john": {"proposed_occupation_trade": "tanner", "proposed_address_property": "first tannery near North Branch/forks, 1831"},
        "murphy_john": {"proposed_occupation_trade": "Exchange Coffee House keeper, Aug 1834–1836", "proposed_spouse_kin": "Harriet Murphy", "proposed_household_facts": "John and Harriet Murphy jointly associated with Exchange Coffee House"},
        "norton_nelson_r": {"proposed_arrival_migration": "arrived 16 Nov 1833", "proposed_occupation_trade": "shipwright / bridge builder", "proposed_civic_voter_census": "Dearborn Street drawbridge work, Mar–Jun 1834"},
        "pierce_asahel": {"proposed_arrival_migration": "arrived Oct 1833", "proposed_occupation_trade": "blacksmith / agricultural-implement maker"},
        "porthier_joseph": {"proposed_arrival_migration": "left Chicago 27 Feb 1835; brief return; left again 21 Mar; Milwaukee 23 Mar 1835", "proposed_occupation_trade": "blacksmith striker", "proposed_household_facts": "scene-date presence corrected to absent"},
        "pruyne_peter": {"proposed_occupation_trade": "druggist; partner in Chicago's second drug store from early 1833", "proposed_spouse_kin": "married Rebecca Sherman 20 Aug 1835 (after scene date)"},
        "kimberly_edmund_s": {"proposed_birth": "1803-04-07, Troy, New York", "proposed_arrival_migration": "moved to Chicago in 1832", "proposed_occupation_trade": "physician; drug-store partner", "proposed_spouse_kin": "married Marie Theresa Ellis 16 May 1829", "proposed_civic_voter_census": "1833 town trustee; 1834 cholera-hospital authorization"},
        "sproat_grenville": {"proposed_occupation_trade": "teacher; English and Classical School, fall 1833"},
        "st_cyr_john_mary": {"proposed_arrival_migration": "appointed to Chicago in 1833; recalled 1837", "proposed_occupation_trade": "Catholic priest", "proposed_civic_voter_census": "first Mass and first Catholic church in Chicago"},
        "steele_ashbel": {"proposed_civic_voter_census": "Cook County coroner in the 1835 period"},
        "sweet_alanson": {"proposed_arrival_migration": "moved from Chicago to Milwaukee in 1835; exact departure relative to 1 Jul unresolved", "proposed_occupation_trade": "stone mason"},
        "thomas_frederick": {"proposed_occupation_trade": "barber-surgeon; retail druggist"},
        "walters_william": {"proposed_occupation_trade": "proprietor, Wolf Point Tavern, 1833–1836"},
        "watkins_john": {"proposed_occupation_trade": "teacher in Chicago, 1835"},
        "kinzie_james": {"proposed_occupation_trade": "auctioneer", "proposed_civic_voter_census": "Wolf Point / early town affairs"},
        "kinzie_robert_a": {"proposed_arrival_migration": "mostly Chicago 1825–1840", "proposed_occupation_trade": "merchant; Kinzie, Davis & Hyde member in 1835", "proposed_address_property": "frame store built 1832"},
        "ll_seth_paine": {"proposed_arrival_migration": "Montpelier, Vermont → Chicago, 1834"},
    }
    proposed_fields = [
        "proposed_birth","proposed_death","proposed_arrival_migration","proposed_occupation_trade",
        "proposed_address_property","proposed_spouse_kin","proposed_civic_voter_census","proposed_household_facts",
    ]
    default = {"outcome":"no_corroboration", "summary":findings["default_summary"], "sources":[], "candidates":[]}
    outcome_map = {"corroborated_enrichment":"corroborated", "candidate_identity":"candidate", "no_corroboration":"no_corroboration"}
    rows = []
    for member in manifest["people"]:
        pid = member["person_id"]
        household, person = people[pid]
        name = person["name"]
        result = findings["overrides"].get(pid, default)
        outcome = outcome_map[result["outcome"]]
        candidates = result.get("candidates", [])
        evidence_against = " | ".join(x for c in candidates for x in c.get("conflicts", []))
        source_ids = result.get("sources", [])
        urls, tiers, limitations = source_meta(source_ids)
        proposed = {k:"" for k in proposed_fields}
        proposed.update(proposals.get(pid, {}))
        if result.get("population_updates"):
            proposed["proposed_household_facts"] = json.dumps(result["population_updates"], ensure_ascii=False)
        if outcome == "corroborated":
            identity = "strong corroboration"
            action = "Adjudicate in T-0487; promote qualifying facts in T-0488 with per-attribute provenance."
        elif outcome == "candidate":
            identity = "strong candidate; explicitly unasserted"
            action = "Retain candidate unasserted; resolve in T-0487 before any canonical identity/household change."
        else:
            identity = "unresolved / no safe external match"
            action = "No canonical change. Retain documented negative-search receipt for T-0487/future research."
        if pid in {"porthier_joseph", "pruyne_peter", "kimberly_edmund_s"}:
            action += " T-0478 already carries the specific safe household-record correction/enrichment where applicable."
        queries = result.get("queries", [t.format(name=name) for t in findings["query_templates"]])
        occupation = (person.get("occupation") or {}).get("value") or "none recorded"
        rows.append({
            "ticket":"T-0478", "cohort":"4", "person_id":pid, "household_id":household["id"],
            "name_transcribed":name, "name_normalized":name, "stratum":member["stratum"],
            "seed_source_id":" | ".join(person.get("sources", [])), "seed_source_date":"",
            "letter_list_dates":" | ".join(person.get("letter_list_returns", [])),
            "research_outcome":outcome, "identity_confidence":identity,
            "residence_confidence":f"current scene-date status: {household['present_on_scene_date']['value']}",
            "household_confidence":"existing canonical container; composition not re-adjudicated by this research pass",
            "occupation_confidence":f"current occupation: {occupation}",
            "candidate_ids":candidate_ids.get(pid, ""), **proposed,
            "evidence_for":result["summary"], "evidence_against":evidence_against,
            "source_ids":" | ".join(source_ids), "source_urls_locators":urls, "source_tiers":tiers,
            "queries":" | ".join(queries), "access_dates":findings["reviewed_on"],
            "source_limitations":limitations or "Candidate and no-find decisions are bounded by the sources searched; name similarity alone was not accepted as identity evidence.",
            "recommended_data_action":action, "notes":result["summary"],
        })
    if len(rows) != 75:
        raise SystemExit(f"expected 75 CSV rows, got {len(rows)}")
    counts = {k:sum(r["research_outcome"] == k for r in rows) for k in ("corroborated","candidate","no_corroboration")}
    expected = {"corroborated":22, "candidate":4, "no_corroboration":49}
    if counts != expected:
        raise SystemExit(f"unexpected pass-four CSV counts: {counts}")
    out = REFERENCE / "T-0478_resident_research.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out.relative_to(REPO)}: {counts}")


def refresh_mirrors() -> None:
    (SITE / "data/residents").mkdir(parents=True, exist_ok=True)
    (SITE / "data/sidecars/1835").mkdir(parents=True, exist_ok=True)
    shutil.copy2(RESIDENTS / "research_pilot.json", SITE / "data/residents/research_pilot.json")
    shutil.copy2(ROOT / "data/sidecars/1835/residents_sources.json", SITE / "data/sidecars/1835/residents_sources.json")
    shutil.copy2(ROOT / "tickets/tickets.json", SITE / "tickets.json")


def main() -> int:
    for required in (
        REFERENCE / "README.md",
        REFERENCE / "T-0478_resident_research_working.xlsx",
        RESEARCH / "pass_04_75_cohort.json",
        RESEARCH / "pass_04_findings.json",
    ):
        if not required.exists():
            raise SystemExit(f"missing completion artifact: {required.relative_to(REPO)}")
    wire_gate()
    run("python3", "tools/compile_resident_research_pilot.py")
    run("python3", "tools/compile_scene.py", "--scene", "1835")
    write_csv()
    run("node", "tools/ticket.mjs", "done", "T-0478", "--pr", "641")
    refresh_mirrors()
    run("python3", "tools/select_resident_research_pass_4.py", "--gate")
    run("python3", "tools/compile_resident_research_pilot.py", "--gate")
    run("python3", "tools/compile_scene.py", "--scene", "1835", "--check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
