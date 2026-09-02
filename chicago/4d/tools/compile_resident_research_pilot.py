#!/usr/bin/env python3
"""Compile every reviewed resident-research pass into the public payload."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from select_resident_research_pass_2 import load_people
from select_resident_research_pass_4 import derive as derive_pass4_cohort

ROOT = Path(__file__).resolve().parents[1]
PASS4_COHORT = ROOT / "data/research/residents/pass_04_75_cohort.json"
PASS4_FINDINGS = ROOT / "data/research/residents/pass_04_findings.json"
OUT = ROOT / "data/residents/research_pilot.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def derive() -> dict:
    prior = load(OUT)
    cohort, findings = load(PASS4_COHORT), load(PASS4_FINDINGS)

    # T-0478 deliberately keeps a compact manifest. Prove it still describes the
    # current resident records rather than asking downstream code to trust stale
    # copied names, household ids or presence flags.
    expected_cohort = derive_pass4_cohort()
    if cohort != expected_cohort:
        raise SystemExit("pass-four cohort is stale; regenerate with select_resident_research_pass_4.py")

    baseline = prior.get("reviews", [])[:225]
    tickets = prior.get("tickets", [prior.get("ticket")])
    expected_prior = ["T-0442", "T-0462", "T-0463"]
    if len(baseline) != 225 or tickets[:3] != expected_prior:
        raise SystemExit("expected the committed T-0442/T-0462/T-0463 225-review baseline")

    index, _ = load_people()
    prior_ids = {r["person_id"] for r in baseline}
    cohort_ids = {p["person_id"] for p in cohort["people"]}
    if prior_ids & cohort_ids:
        raise SystemExit(f"research passes overlap: {sorted(prior_ids & cohort_ids)}")
    if extras := set(findings["overrides"]) - cohort_ids:
        raise SystemExit(f"pass-four findings outside cohort: {sorted(extras)}")

    reviews = list(baseline)
    for member in cohort["people"]:
        pid = member["person_id"]
        if pid not in index:
            raise SystemExit(f"pass-four person missing from residents layer: {pid}")
        household, person = index[pid]
        name = person["name"]
        stratum = member["stratum"]
        starting_evidence = (
            "established_profile" if stratum == "established_profile" else "letter_list_only"
        )
        result = findings["overrides"].get(
            pid,
            {
                "outcome": "no_corroboration",
                "summary": findings["default_summary"],
                "sources": [],
                "candidates": [],
            },
        )
        if result["outcome"] not in {
            "corroborated_enrichment",
            "candidate_identity",
            "no_corroboration",
        }:
            raise SystemExit(f"{pid}: unsupported or pending research outcome {result['outcome']!r}")
        reviews.append({
            "person_id": pid,
            "household_id": household["id"],
            "name_as_recorded": name,
            "starting_evidence": starting_evidence,
            "reviewed_on": findings["reviewed_on"],
            "outcome": result["outcome"],
            "summary": result["summary"],
            "queries": result.get(
                "queries", [t.format(name=name) for t in findings["query_templates"]]
            ),
            "sources": result.get("sources", []),
            "candidates": result.get("candidates", []),
            "identity_rule": "Candidate facts remain unasserted until a source bridges the candidate to the historical record by more than name similarity.",
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
    pass_counts = []
    for ticket, start in (("T-0442", 0), ("T-0462", 75), ("T-0463", 150), ("T-0478", 225)):
        review_pass = reviews[start:start + 75]
        pass_counts.append({
            "ticket": ticket,
            "size": 75,
            "counts": {k: sum(r["outcome"] == k for r in review_pass) for k in outcomes},
        })

    pass4_counts = pass_counts[-1]["counts"]
    expected_pass4 = {
        "corroborated_enrichment": 22,
        "candidate_identity": 4,
        "no_corroboration": 49,
    }
    if pass4_counts != expected_pass4:
        raise SystemExit(f"pass-four outcome census changed: {pass4_counts}")

    return {
        "_doc": "T-0442, T-0462, T-0463, and T-0478 public resident research reviews. Candidate biographies are leads, not asserted resident facts.",
        "version": 4,
        "ticket": "T-0478",
        "tickets": ["T-0442", "T-0462", "T-0463", "T-0478"],
        "scene_date": "1835-07-01",
        "reviewed_on": findings["reviewed_on"],
        "cohort_size": len(reviews),
        "eligible_real_named_people": cohort["population_frame"]["eligible_real_named_people"],
        "counts": counts,
        "passes": pass_counts,
        "reviews": reviews,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true")
    args = parser.parse_args()
    doc = derive()
    if len(doc["reviews"]) != 300 or sum(doc["counts"].values()) != 300:
        raise SystemExit("resident research must compile exactly 300 non-overlapping reviews")
    rendered = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit("data/residents/research_pilot.json is stale")
        print(f"resident research reviews: 300 current ({doc['counts']})")
    else:
        OUT.write_text(rendered)
        print(f"resident research reviews: wrote 300 ({doc['counts']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
