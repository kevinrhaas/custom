#!/usr/bin/env python3
"""Derive T-0463's fixed, non-overlapping 75-person research cohort.

Pass three deliberately preserves T-0462's 25/25/25 balance while excluding both
prior reviewed cohorts. Selection is deterministic from the authoritative household
records so the committed manifest can be gated against population drift.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESIDENTS = ROOT / "data" / "residents"
RESEARCH = ROOT / "data" / "research" / "residents"
PILOT = RESEARCH / "pilot_75_cohort.json"
PASS2 = RESEARCH / "pass_02_75_cohort.json"
OUT = RESEARCH / "pass_03_75_cohort.json"


def load_people() -> tuple[dict[str, tuple[dict, dict]], list[dict]]:
    index = json.loads((RESIDENTS / "index.json").read_text())
    households = [json.loads((RESIDENTS / row["file"]).read_text())
                  for row in index["households"]]
    people: dict[str, tuple[dict, dict]] = {}
    for household in households:
        for person in household.get("persons", []):
            if person["id"] in people:
                raise SystemExit(f"duplicate person id {person['id']}")
            people[person["id"]] = (household, person)
    return people, households


def prior_ids() -> set[str]:
    ids: set[str] = set()
    for path in (PILOT, PASS2):
        doc = json.loads(path.read_text())
        ids.update(row["person_id"] for row in doc["people"])
    return ids


def member(household: dict, person: dict, evidence: str, reason: str) -> dict:
    if person.get("grade") == "reconstructed":
        raise SystemExit(f"{person['id']}: reconstructed people are outside T-0463")
    return {
        "household_id": household["id"],
        "person_id": person["id"],
        "name": person["name"],
        "starting_evidence": evidence,
        "starting_grade": person["grade"],
        "starting_presence": household["present_on_scene_date"]["value"],
        "starting_occupation": (person.get("occupation") or {}).get("value"),
        "letter_list_returns": person.get("letter_list_returns", []),
        "sources": sorted(person.get("sources", [])),
        "selection_reason": reason,
    }


def derive() -> dict:
    index, households = load_people()
    prior = prior_ids()

    established = []
    present_letter = []
    uncertain_letter = []
    for person_id in sorted(index):
        if person_id in prior:
            continue
        household, person = index[person_id]
        if person.get("grade") == "reconstructed":
            continue
        if person.get("letter_list_only"):
            presence = household["present_on_scene_date"]["value"]
            if presence == "present":
                present_letter.append((household, person))
            elif presence == "uncertain":
                uncertain_letter.append((household, person))
            continue
        # The established stratum is deliberately attested-only. Inferred named
        # people may be real, but this pass should not spend its richer-profile
        # quota validating a person the project itself has not yet attested.
        if person.get("grade") == "attested":
            established.append((household, person))

    chosen = established[:25], present_letter[:25], uncertain_letter[:25]
    if any(len(group) < 25 for group in chosen):
        raise SystemExit("T-0463 no longer has 25 eligible members in every stratum")

    people = [member(hh, p, "established_profile",
                     "Next deterministic attested non-letter-list resident after the two prior cohorts; selected for deeper household research.")
              for hh, p in chosen[0]]
    people += [member(hh, p, "letter_list_only",
                      "Next deterministic scene-date-present letter-list resident after the two prior cohorts; selected for identity, OCR and duplicate testing.")
               for hh, p in chosen[1]]
    people += [member(hh, p, "letter_list_only",
                      "Next deterministic uncertain/earlier letter-list resident after the two prior cohorts; selected for identity, OCR and duplicate testing.")
               for hh, p in chosen[2]]

    ids = [row["person_id"] for row in people]
    overlap = prior.intersection(ids)
    if overlap:
        raise SystemExit(f"T-0463 overlaps earlier cohorts: {sorted(overlap)}")
    if len(people) != 75 or len(set(ids)) != 75:
        raise SystemExit(f"pass three must contain 75 unique people, got {len(people)}/{len(set(ids))}")

    strata = {
        "established_profile": sum(row["starting_evidence"] == "established_profile" for row in people),
        "letter_list_only_present": sum(row["starting_evidence"] == "letter_list_only" and row["starting_presence"] == "present" for row in people),
        "letter_list_only_uncertain": sum(row["starting_evidence"] == "letter_list_only" and row["starting_presence"] == "uncertain" for row in people),
    }
    expected = {"established_profile": 25, "letter_list_only_present": 25,
                "letter_list_only_uncertain": 25}
    if strata != expected:
        raise SystemExit(f"pass-three strata changed: {strata}")

    eligible = sum(person.get("grade") != "reconstructed"
                   for household in households for person in household.get("persons", []))
    return {
        "_doc": "T-0463's reproducible third 75-person research cohort; selection is not evidence about a person.",
        "version": 1,
        "ticket": "T-0463",
        "scene_date": "1835-07-01",
        "generated_by": "tools/select_resident_research_pass_3.py",
        "selection_policy": "Deterministic person-id order within the same 25 established / 25 present-letter / 25 uncertain-letter strata as T-0462, after excluding T-0442 and T-0462.",
        "population_frame": {
            "eligible_real_named_people": eligible,
            "previously_reviewed": len(prior),
            "sample_size": 75,
            "cumulative_reviewed": len(prior) + 75,
            "strata": strata,
        },
        "people": people,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(derive(), indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale; regenerate without --gate")
        print("resident research pass three: 75 people, committed manifest current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered)
    print("resident research pass three: wrote 75 people (25 established, 25 present-list, 25 earlier-list)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
