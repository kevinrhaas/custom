#!/usr/bin/env python3
"""Validate T-0478's fourth resident-research pass and its compact completion sidecar."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from select_resident_research_pass_4 import derive as derive_cohort

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/research/residents/pass_04_75_cohort.json"
FINDINGS = ROOT / "data/research/residents/pass_04_findings.json"
PRIOR = ROOT / "data/residents/research_pilot.json"
OUT = ROOT / "data/research/residents/pass_04_public.json"
ALLOWED = ("corroborated_enrichment", "candidate_identity", "no_corroboration")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def derive() -> dict:
    manifest = load(MANIFEST)
    findings = load(FINDINGS)
    prior = load(PRIOR)

    expected_manifest = derive_cohort()
    if manifest != expected_manifest:
        raise SystemExit("pass_04_75_cohort.json is stale against the fixed selector")

    if manifest.get("ticket") != "T-0478" or findings.get("ticket") != "T-0478":
        raise SystemExit("pass four ticket id changed")
    people = manifest.get("people", [])
    ids = [row.get("person_id") for row in people]
    if len(ids) != 75 or len(set(ids)) != 75:
        raise SystemExit(f"T-0478 must contain 75 unique people, got {len(ids)}/{len(set(ids))}")

    prior_reviews = prior.get("reviews", [])
    if len(prior_reviews) != 225:
        raise SystemExit(f"expected 225 prior compiled reviews, got {len(prior_reviews)}")
    prior_ids = {row.get("person_id") for row in prior_reviews}
    if overlap := prior_ids.intersection(ids):
        raise SystemExit(f"T-0478 overlaps the first 225 reviews: {sorted(overlap)}")

    frame = manifest.get("population_frame", {})
    if frame.get("previously_reviewed") != 225 or frame.get("cumulative_reviewed") != 300:
        raise SystemExit("T-0478 cumulative review frame must read 225 prior / 300 cumulative")

    cohort_ids = set(ids)
    overrides = findings.get("overrides", {})
    if extras := set(overrides) - cohort_ids:
        raise SystemExit(f"T-0478 findings outside cohort: {sorted(extras)}")

    source_ids = {p.stem for p in (ROOT / "data/sources").glob("*.json")}
    reviews = []
    for person in people:
        pid = person["person_id"]
        result = overrides.get(pid, {
            "outcome": "no_corroboration",
            "summary": findings["default_summary"],
            "sources": [],
            "candidates": [],
        })
        outcome = result.get("outcome")
        if outcome not in ALLOWED:
            raise SystemExit(f"{pid}: invalid research outcome {outcome!r}")
        if not result.get("summary"):
            raise SystemExit(f"{pid}: research outcome has no summary")

        cited = set(result.get("sources", []))
        candidates = result.get("candidates", [])
        if outcome == "candidate_identity" and not candidates:
            raise SystemExit(f"{pid}: candidate outcome carries no candidate")
        for candidate in candidates:
            if candidate.get("asserted") is not False:
                raise SystemExit(f"{pid}: candidate must be explicitly unasserted")
            cited.update(candidate.get("sources", []))
        if missing := cited - source_ids:
            raise SystemExit(f"{pid}: unresolved source ids {sorted(missing)}")

        reviews.append({
            "person_id": pid,
            "stratum": person["stratum"],
            "outcome": outcome,
        })

    counts = {k: sum(r["outcome"] == k for r in reviews) for k in ALLOWED}
    if sum(counts.values()) != 75:
        raise SystemExit("T-0478 outcomes must resolve all 75 people")
    if counts != {
        "corroborated_enrichment": 22,
        "candidate_identity": 4,
        "no_corroboration": 49,
    }:
        raise SystemExit(f"T-0478 outcome counts drifted: {counts}")

    return {
        "_doc": "T-0478 fourth-pass resident research completion sidecar. Detailed summaries, sources, candidates and queries remain in pass_04_findings.json and the durable T-0478 workbook/CSV.",
        "version": 1,
        "ticket": "T-0478",
        "scene_date": "1835-07-01",
        "reviewed_on": findings["reviewed_on"],
        "prior_reviewed": 225,
        "cohort_size": 75,
        "cumulative_reviewed": 300,
        "eligible_real_named_people": frame["eligible_real_named_people"],
        "counts": counts,
        "reviews": reviews,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true")
    args = parser.parse_args()

    doc = derive()
    if args.gate:
        if not OUT.exists() or load(OUT) != doc:
            raise SystemExit("data/research/residents/pass_04_public.json is stale")
        print(f"resident research pass four: 75 current; 300 cumulative ({doc['counts']})")
        return 0

    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(f"resident research pass four: wrote 75; 300 cumulative ({doc['counts']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
