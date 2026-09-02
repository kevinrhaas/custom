#!/usr/bin/env python3
"""Derive T-0463's fixed, non-overlapping 75-person research cohort."""
from __future__ import annotations
import argparse
import json

from select_resident_research_pass_2 import ROOT, RESIDENTS, PILOT, load_people, member

OUT = ROOT / "data/research/residents/pass_03_75_cohort.json"
PASS2 = RESIDENTS.parent / "research" / "residents" / "pass_02_75_cohort.json"

ESTABLISHED_IDS = (
    "beckford_printer", "blodgett_tyler_k", "brown_lemuel", "brown_rufus",
    "brown_mrs_rufus", "carver_david", "casey_edward_w", "church_thomas",
    "cobb_silas_b", "cohen_peter", "couch_james", "davis_john", "davis_t_o",
    "egan_emeline", "elston_daniel", "fullerton_alexander", "gale_stephen_f",
    "goss_o", "greene_john", "harmon_charles_l", "harmon_elijah_d",
    "harmon_isaac_d", "heacock_russel_e", "ingersoll_chester", "jones_benjamin",
)

PRESENT_LETTER_IDS = (
    "ll_aiker_samuel", "ll_akers_simon", "ll_allen_william", "ll_allin_richard",
    "ll_alling_prudde", "ll_anderson_eli_f", "ll_archer_joseph", "ll_ayres_levi",
    "ll_bakwith_albert", "ll_bebee_orson", "ll_beeson_william",
    "ll_benton_datas_e", "ll_bishop_j_e", "ll_blair_william_g", "ll_bly_rouse",
    "ll_bullen_jeduthnn", "ll_bullock_stephen", "ll_burbee_jonathan",
    "ll_butterfield_ben", "ll_chadwick_joseph", "ll_chambers_john",
    "ll_chanpagne_batist", "ll_chase_peter", "ll_clark_erastus",
    "ll_comstock_h_h",
)

UNCERTAIN_LETTER_IDS = (
    "ll_absolam_reel", "ll_adam_vandorwerk", "ll_alexander_wilkes",
    "ll_alexr_h_tucker", "ll_alfred_churchill", "ll_alison_b_vaughn",
    "ll_almon_perring", "ll_alonzo_castle", "ll_alva_crandal", "ll_alva_dunlap",
    "ll_amos_rathburn", "ll_andrew_miles", "ll_anthony_heere", "ll_aram_winsor",
    "ll_asa_doel", "ll_austin_parsalls", "ll_b_r_paige", "ll_bennet_bailey",
    "ll_carl_romer", "ll_charles_h_bartlett", "ll_charles_t_richards",
    "ll_chas_h_chapman", "ll_clark_b_albee", "ll_curtis_parkes",
    "ll_ebenozer_alden",
)

def derive() -> dict:
    index, households = load_people()
    # The compiled payload grows when this pass is added, so its review list cannot
    # be used as the prior set. Read the two fixed manifests that predate T-0463.
    reviewed = ({row["person_id"] for row in json.loads(PILOT.read_text())["people"]}
                | {row["person_id"] for row in json.loads(PASS2.read_text())["people"]})
    people = [member(index, pid, "established_profile",
                     "Established named resident selected to deepen an existing household profile.")
              for pid in ESTABLISHED_IDS]
    people += [member(index, pid, "letter_list_only",
                      "Distinctive or variant-rich scene-date return selected for identity and duplicate testing.")
               for pid in PRESENT_LETTER_IDS]
    people += [member(index, pid, "letter_list_only",
                      "Distinctive or variant-rich earlier return selected for identity and duplicate testing.")
               for pid in UNCERTAIN_LETTER_IDS]
    ids = [row["person_id"] for row in people]
    if overlap := reviewed.intersection(ids):
        raise SystemExit(f"T-0463 overlaps prior reviews: {sorted(overlap)}")
    if len(people) != 75 or len(set(ids)) != 75:
        raise SystemExit(f"pass three must contain 75 unique people, got {len(people)}/{len(set(ids))}")
    strata = {
        "established_profile": sum(r["starting_evidence"] == "established_profile" for r in people),
        "letter_list_only_present": sum(r["starting_evidence"] == "letter_list_only" and r["starting_presence"] == "present" for r in people),
        "letter_list_only_uncertain": sum(r["starting_evidence"] == "letter_list_only" and r["starting_presence"] == "uncertain" for r in people),
    }
    expected = {"established_profile": 25, "letter_list_only_present": 25,
                "letter_list_only_uncertain": 25}
    if strata != expected:
        raise SystemExit(f"pass-three strata changed: {strata}")
    eligible = sum(p.get("grade") != "reconstructed" for h in households for p in h.get("persons", []))
    return {"_doc": "T-0463's reproducible third 75-person research cohort; selection is not evidence about a person.",
            "version": 1, "ticket": "T-0463", "scene_date": "1835-07-01",
            "generated_by": "tools/select_resident_research_pass_3.py",
            "population_frame": {"eligible_real_named_people": eligible,
                                 "previously_reviewed": len(reviewed), "sample_size": 75,
                                 "cumulative_reviewed": len(reviewed) + 75, "strata": strata},
            "people": people}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--gate", action="store_true"); args = ap.parse_args()
    rendered = json.dumps(derive(), indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        if not OUT.exists() or OUT.read_text() != rendered: raise SystemExit(f"{OUT.relative_to(ROOT)} is stale")
        print("resident research pass three: 75 people, committed manifest current"); return 0
    OUT.write_text(rendered)
    print("resident research pass three: wrote 75 people (25 established, 25 present-list, 25 earlier-list)")
    return 0

if __name__ == "__main__": raise SystemExit(main())
