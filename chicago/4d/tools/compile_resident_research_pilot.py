#!/usr/bin/env python3
"""Compile every reviewed resident-research pass into the public payload."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS2_COHORT = ROOT / "data/research/residents/pass_02_75_cohort.json"
PASS2_FINDINGS = ROOT / "data/research/residents/pass_02_findings.json"
OUT = ROOT / "data/residents/research_pilot.json"

def load(path: Path) -> dict:
    return json.loads(path.read_text())

def derive() -> dict:
    prior, cohort, findings = load(OUT), load(PASS2_COHORT), load(PASS2_FINDINGS)
    baseline = prior.get("reviews", [])[:75]
    if len(baseline) != 75 or prior.get("tickets", [prior.get("ticket")])[0] != "T-0442":
        raise SystemExit("expected the committed T-0442 75-review baseline")
    prior_ids = {r["person_id"] for r in baseline}
    cohort_ids = {p["person_id"] for p in cohort["people"]}
    if prior_ids & cohort_ids:
        raise SystemExit(f"research passes overlap: {sorted(prior_ids & cohort_ids)}")
    if extras := set(findings["overrides"]) - cohort_ids:
        raise SystemExit(f"pass-two findings outside cohort: {sorted(extras)}")
    reviews = list(baseline)
    for person in cohort["people"]:
        pid, name = person["person_id"], person["name"]
        result = findings["overrides"].get(pid, {"outcome": "no_corroboration", "summary": findings["default_summary"], "sources": [], "candidates": []})
        reviews.append({
            "person_id": pid, "household_id": person["household_id"], "name_as_recorded": name,
            "starting_evidence": person["starting_evidence"], "reviewed_on": findings["reviewed_on"],
            "outcome": result["outcome"], "summary": result["summary"],
            "queries": result.get("queries", [t.format(name=name) for t in findings["query_templates"]]),
            "sources": result.get("sources", []), "candidates": result.get("candidates", []),
            "identity_rule": "Candidate facts remain unasserted until a source bridges the candidate to the historical record by more than name similarity."
        })
    source_ids = {p.stem for p in (ROOT / "data/sources").glob("*.json")}
    for review in reviews:
        cited = set(review["sources"])
        for candidate in review["candidates"]:
            if candidate.get("asserted") is not False:
                raise SystemExit(f"{review['person_id']}: candidate must be explicitly unasserted")
            cited.update(candidate.get("sources", []))
        if missing := cited - source_ids:
            raise SystemExit(f"{review['person_id']}: unresolved source ids {sorted(missing)}")
    outcomes = ("corroborated_enrichment", "candidate_identity", "no_corroboration")
    counts = {k: sum(r["outcome"] == k for r in reviews) for k in outcomes}
    pass2 = reviews[75:]
    pass2_counts = {k: sum(r["outcome"] == k for r in pass2) for k in outcomes}
    return {"_doc": "T-0442 and T-0462 public resident research reviews. Candidate biographies are leads, not asserted resident facts.",
        "version": 2, "ticket": "T-0462", "tickets": ["T-0442", "T-0462"], "scene_date": "1835-07-01",
        "reviewed_on": findings["reviewed_on"], "cohort_size": len(reviews),
        "eligible_real_named_people": cohort["population_frame"]["eligible_real_named_people"],
        "counts": counts, "passes": [{"ticket": "T-0442", "size": 75, "counts": {k: sum(r["outcome"] == k for r in baseline) for k in outcomes}},
        {"ticket": "T-0462", "size": 75, "counts": pass2_counts}], "reviews": reviews}

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--gate", action="store_true"); args = parser.parse_args()
    doc = derive()
    if len(doc["reviews"]) != 150 or sum(doc["counts"].values()) != 150:
        raise SystemExit("resident research must compile exactly 150 non-overlapping reviews")
    rendered = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        if not OUT.exists() or OUT.read_text() != rendered: raise SystemExit("data/residents/research_pilot.json is stale")
        print(f"resident research reviews: 150 current ({doc['counts']})")
    else:
        OUT.write_text(rendered); print(f"resident research reviews: wrote 150 ({doc['counts']})")
    return 0

if __name__ == "__main__": raise SystemExit(main())
