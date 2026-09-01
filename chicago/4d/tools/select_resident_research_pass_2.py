#!/usr/bin/env python3
"""Derive T-0462's fixed, non-overlapping 75-person research cohort."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESIDENTS = ROOT / "data" / "residents"
PILOT = ROOT / "data" / "research" / "residents" / "pilot_75_cohort.json"
OUT = ROOT / "data" / "research" / "residents" / "pass_02_75_cohort.json"

KNOWN_IDS = (
    "bates_john_jr", "beaubien_jean_baptiste", "beaubien_josette",
    "beaubien_madore", "beaubien_mark", "caldwell_billy", "calhoun_john",
    "clybourne_archibald", "couch_ira", "hamilton_richard_j",
    "hogan_john_s_c", "kinzie_john_h", "kinzie_juliette",
    "robinson_alexander", "robinson_catherine", "owen_thomas_jv",
    "pearsons_hiram", "peck_philip", "porter_jeremiah",
    "porter_eliza_chappel", "snow_george_w", "spring_giles",
    "taylor_augustine", "temple_john_t", "wright_john",
)

PRESENT_LETTER_IDS = (
    "ll_bailly_joseph", "ll_chappel_eliza_mir", "ll_dement_wm",
    "ll_curtenius_fred_k", "ll_avery_charles", "ll_bemis_samuel_c",
    "ll_blood_amos", "ll_boardman_elect", "ll_bostwick_e_b",
    "ll_bradstreet_j_p", "ll_brooks_gardner", "ll_brush_matthias",
    "ll_burdick_paul", "ll_case_nehemiah", "ll_chamberlain_l_c",
    "ll_cooley_edward_v", "ll_cook_rowland_i", "ll_covell_thomas_r",
    "ll_curtis_liman", "ll_davenport_dennis", "ll_dow_albert_f",
    "ll_fairchilds_ransom", "ll_felch_alaneon", "ll_ford_ebenezer",
    "ll_galusha_ezra",
)

UNCERTAIN_LETTER_IDS = (
    "ll_aaron_parcel", "ll_aron_parcell", "ll_alonzo_murray",
    "ll_alonzo_murry", "ll_caleb_foster", "ll_chester_house",
    "ll_elam_tuller", "ll_david_ingersall", "ll_elihu_d_filer",
    "ll_charles_c_drake", "ll_amanda_miner", "ll_amy_c_wear",
    "ll_angeline_vann", "ll_archibald_knox", "ll_asa_brundage",
    "ll_constant_abbott", "ll_dangerfield_dunn", "ll_david_p_frame",
    "ll_eben_griswold", "ll_elijah_wentworth_sen", "ll_enos_covalt",
    "ll_frederick_w_page", "ll_george_r_makepiece", "ll_gregory_e_legg",
    "ll_hannah_hurlburt",
)


def load_people() -> tuple[dict[str, tuple[dict, dict]], list[dict]]:
    index = json.loads((RESIDENTS / "index.json").read_text())
    households = [json.loads((RESIDENTS / row["file"]).read_text())
                  for row in index["households"]]
    people = {}
    for household in households:
        for person in household.get("persons", []):
            if person["id"] in people:
                raise SystemExit(f"duplicate person id {person['id']}")
            people[person["id"]] = (household, person)
    return people, households


def member(index: dict[str, tuple[dict, dict]], person_id: str,
           evidence: str, reason: str) -> dict:
    if person_id not in index:
        raise SystemExit(f"fixed cohort member {person_id} is missing")
    household, person = index[person_id]
    if person.get("grade") == "reconstructed":
        raise SystemExit(f"{person_id}: reconstructed people are outside T-0462")
    if evidence == "letter_list_only" and not person.get("letter_list_only"):
        raise SystemExit(f"{person_id}: no longer marked letter_list_only")
    if evidence == "established_profile" and person.get("letter_list_only"):
        raise SystemExit(f"{person_id}: established stratum became letter-list-only")
    return {
        "household_id": household["id"], "person_id": person_id,
        "name": person["name"], "starting_evidence": evidence,
        "starting_grade": person["grade"],
        "starting_presence": household["present_on_scene_date"]["value"],
        "starting_occupation": (person.get("occupation") or {}).get("value"),
        "letter_list_returns": person.get("letter_list_returns", []),
        "sources": sorted(person.get("sources", [])),
        "selection_reason": reason,
    }


def derive() -> dict:
    index, households = load_people()
    prior = {row["person_id"] for row in json.loads(PILOT.read_text())["people"]}
    people = [member(index, pid, "established_profile",
                     "Established named resident selected to deepen an existing household profile.")
              for pid in KNOWN_IDS]
    people += [member(index, pid, "letter_list_only",
                      "Distinctive or variant-rich scene-date return name selected for identity and duplicate testing.")
               for pid in PRESENT_LETTER_IDS]
    people += [member(index, pid, "letter_list_only",
                      "Distinctive or variant-rich earlier-return name selected for identity and duplicate testing.")
               for pid in UNCERTAIN_LETTER_IDS]
    ids = [row["person_id"] for row in people]
    if prior.intersection(ids):
        raise SystemExit(f"T-0462 overlaps T-0442: {sorted(prior.intersection(ids))}")
    if len(people) != 75 or len(set(ids)) != 75:
        raise SystemExit(f"pass two must contain 75 unique people, got {len(people)}/{len(set(ids))}")
    strata = {
        "established_profile": sum(row["starting_evidence"] == "established_profile" for row in people),
        "letter_list_only_present": sum(row["starting_evidence"] == "letter_list_only" and row["starting_presence"] == "present" for row in people),
        "letter_list_only_uncertain": sum(row["starting_evidence"] == "letter_list_only" and row["starting_presence"] == "uncertain" for row in people),
    }
    expected = {"established_profile": 25, "letter_list_only_present": 25,
                "letter_list_only_uncertain": 25}
    if strata != expected:
        raise SystemExit(f"pass-two strata changed: {strata}")
    eligible = sum(person.get("grade") != "reconstructed"
                   for household in households for person in household.get("persons", []))
    return {
        "_doc": "T-0462's reproducible second 75-person research cohort; selection is not evidence about a person.",
        "version": 1, "ticket": "T-0462", "scene_date": "1835-07-01",
        "generated_by": "tools/select_resident_research_pass_2.py",
        "population_frame": {"eligible_real_named_people": eligible,
                             "previously_reviewed": len(prior), "sample_size": 75,
                             "cumulative_reviewed": len(prior) + 75, "strata": strata},
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
        print("resident research pass two: 75 people, committed manifest current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered)
    print("resident research pass two: wrote 75 people (25 established, 25 present-list, 25 earlier-list)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
