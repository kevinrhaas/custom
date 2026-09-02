#!/usr/bin/env python3
"""Derive T-0479's fixed fifth 75-person resident-research cohort.

Pass 5 was claimed while T-0478 was still in flight. The selector retains
a frozen copy of all 75 T-0478 person ids as the historical collision lock and
keeps the claim-time population frame stable while validating current residents.
"""
from __future__ import annotations

import argparse
import json

from select_resident_research_pass_2 import ROOT, RESIDENTS, PILOT, load_people

OUT = ROOT / "data/research/residents/pass_05_75_cohort.json"
PASS2 = ROOT / "data/research/residents/pass_02_75_cohort.json"
PASS3 = ROOT / "data/research/residents/pass_03_75_cohort.json"

# These are the only remaining non-letter-list entries that are both real and
# individually named after the pilot and passes 2-4 are claimed.  Unnamed/count
# placeholders and hypothesised inf_* people are deliberately not substituted.
ESTABLISHED_IDS = (
    "pratt_oscar", "kercheval_gholson", "kimball_walter",
    "lampman_henry_s", "hall_benjamin", "murphy_harriet",
    "taylor_charles", "temple_peter", "wright_john_s",
)

PRESENT_LETTER_IDS = (
    "ll_dalton_edward", "ll_damels_samuel", "ll_darling_daniel",
    "ll_day_ann_airs", "ll_dean_james_l", "ll_demotte_lenac",
    "ll_dilbee_david_b", "ll_dykine_elias_s", "ll_fadhams_ddward",
    "ll_failor_william", "ll_fitzlugh_daniel_i", "ll_food_alonzo_c",
    "ll_forceman_robert_r", "ll_fre_humphrey_lemuel", "ll_gabbs_james_i1",
    "ll_gariner_joseph", "ll_gilman_eli", "ll_glen_james_l",
    "ll_gooding_jaines", "ll_goodsough_harriet_m", "ll_gordon_william",
    "ll_gould_a_b", "ll_green_damel_m", "ll_harris_david",
    "ll_harrison_caleb", "ll_hart_edwin_c", "ll_hartman_peter",
    "ll_hateh_betsey", "ll_hickcox_joseph", "ll_holliday_william",
    "ll_holmes_hiram", "ll_hopkins_henry", "ll_hugunin_leonard_c",
)

UNCERTAIN_LETTER_IDS = (
    "ll_daniel_hasslen", "ll_daniel_howland", "ll_daniel_newton",
    "ll_daniel_o_robian", "ll_daniel_platt", "ll_daniel_roberson",
    "ll_david_ayers", "ll_david_bigelow", "ll_david_dickson",
    "ll_david_groover", "ll_david_harris", "ll_e_dimmick",
    "ll_e_simons", "ll_e_w_conte", "ll_edward_a_rogers",
    "ll_edward_b_coleman", "ll_edward_poor", "ll_edward_trimble",
    "ll_elias_maynard", "ll_elijah_dix", "ll_elijah_garton",
    "ll_elisha_h_hazzard", "ll_eliza_pearce", "ll_esther_preston",
    "ll_ezekiel_turner", "ll_f_c_berger", "ll_f_h_morland",
    "ll_f_plumer", "ll_ford_freeman", "ll_francis_perry",
    "ll_geo_a_burlingame", "ll_george_b_parmlee", "ll_hezekiah_gifford",
)

# Frozen from steward/resident-research-pass-4 at the point T-0479 was claimed.
PASS4_ESTABLISHED_IDS = (
    "haddock_edward", "handy_major", "mason_matthias", "maxwell_philip",
    "mckee_david", "meeker_joseph", "miller_john", "mulford_e_h",
    "murphy_john", "norton_nelson_r", "pierce_asahel", "porthier_joseph",
    "pruyne_peter", "kimberly_edmund_s", "sproat_grenville", "st_cyr_john_mary",
    "steele_ashbel", "stow_william_h", "sweet_alanson", "taylor_anson_h",
    "thomas_frederick", "walters_william", "watkins_john", "kinzie_james",
    "kinzie_robert_a",
)
PASS4_PRESENT_LETTER_IDS = (
    "ll_sewyer_edward_f", "ll_shattick_walter", "ll_shepherd_albert",
    "ll_shielde_willam", "ll_simpaon_lyman", "ll_simpson_john_p",
    "ll_skinner_heury_c", "ll_smith_elded", "ll_sorton_lymor",
    "ll_souee_theson", "ll_spencer_william", "ll_spicer_charles",
    "ll_sprague_willinm_b", "ll_stallord_arnold", "ll_stark_b_b",
    "ll_stater_asa_p", "ll_steel_richard", "ll_stevens_issac",
    "ll_stocking_austin", "ll_stoel_c_ii", "ll_stold_abraham_f",
    "ll_strode_p_m", "ll_strong_george", "ll_swapp_abram",
    "ll_swearingen_david",
)
PASS4_UNCERTAIN_LETTER_IDS = (
    "ll_seth_b_doane", "ll_seth_paine", "ll_seth_wescott",
    "ll_sidney_arrowsmith", "ll_sidney_dyer", "ll_simmons_medad_i",
    "ll_stephen_andress", "ll_stephen_mack", "ll_stephen_may",
    "ll_stith_sherrygood", "ll_thos_w_donkin", "ll_timothy_barbour",
    "ll_timothy_titcomb", "ll_tindal_james", "ll_tryon_david",
    "ll_vandeventer_wm", "ll_w_l_d_ewing", "ll_w_y_lewin",
    "ll_wampler_westley", "ll_ward_hanibal", "ll_wells_charles",
    "ll_westley_diggins", "ll_wheeler_orson", "ll_white_edson",
    "ll_whiting_henry",
)
PASS4_CLAIMED_IDS = (set(PASS4_ESTABLISHED_IDS) |
                     set(PASS4_PRESENT_LETTER_IDS) |
                     set(PASS4_UNCERTAIN_LETTER_IDS))


def compact_member(index: dict, person_id: str, stratum: str) -> dict:
    if person_id not in index:
        raise SystemExit(f"fixed cohort member {person_id} is missing")
    household, person = index[person_id]
    if person.get("grade") == "reconstructed":
        raise SystemExit(f"{person_id}: reconstructed person is outside T-0479")
    if person_id.startswith("inf_") or household["id"].startswith("hh_inf_"):
        raise SystemExit(f"{person_id}: hypothesised inf_* person is outside T-0479")
    if "unnamed" in person.get("name", "").lower():
        raise SystemExit(f"{person_id}: unnamed placeholder is outside T-0479")
    letter = bool(person.get("letter_list_only"))
    if stratum == "remaining_named_non_letter" and letter:
        raise SystemExit(f"{person_id}: remaining established person became letter-list-only")
    if stratum.startswith("letter_list_only_") and not letter:
        raise SystemExit(f"{person_id}: postal-list person no longer marked letter_list_only")
    expected_presence = "present" if stratum == "letter_list_only_present" else None
    if expected_presence and household["present_on_scene_date"]["value"] != expected_presence:
        raise SystemExit(f"{person_id}: pass-five present stratum changed")
    if stratum == "letter_list_only_uncertain" and household["present_on_scene_date"]["value"] != "uncertain":
        raise SystemExit(f"{person_id}: pass-five uncertain stratum changed")
    return {"household_id": household["id"], "person_id": person_id, "stratum": stratum}


def derive() -> dict:
    index, _ = load_people()
    pilot_ids = {row["person_id"] for row in json.loads(PILOT.read_text())["people"]}
    pass2_ids = {row["person_id"] for row in json.loads(PASS2.read_text())["people"]}
    pass3_ids = {row["person_id"] for row in json.loads(PASS3.read_text())["people"]}
    prior_merged = pilot_ids | pass2_ids | pass3_ids

    people = [compact_member(index, pid, "remaining_named_non_letter") for pid in ESTABLISHED_IDS]
    people += [compact_member(index, pid, "letter_list_only_present") for pid in PRESENT_LETTER_IDS]
    people += [compact_member(index, pid, "letter_list_only_uncertain") for pid in UNCERTAIN_LETTER_IDS]
    ids = [row["person_id"] for row in people]

    if overlap := prior_merged.intersection(ids):
        raise SystemExit(f"T-0479 overlaps merged resident research: {sorted(overlap)}")
    if overlap := PASS4_CLAIMED_IDS.intersection(ids):
        raise SystemExit(f"T-0479 overlaps claimed T-0478 work: {sorted(overlap)}")
    if len(PASS4_CLAIMED_IDS) != 75:
        raise SystemExit(f"frozen T-0478 collision lock changed size: {len(PASS4_CLAIMED_IDS)}")
    if len(people) != 75 or len(set(ids)) != 75:
        raise SystemExit(f"pass five must contain 75 unique people, got {len(people)}/{len(set(ids))}")

    strata = {
        "remaining_named_non_letter": sum(r["stratum"] == "remaining_named_non_letter" for r in people),
        "letter_list_only_present": sum(r["stratum"] == "letter_list_only_present" for r in people),
        "letter_list_only_uncertain": sum(r["stratum"] == "letter_list_only_uncertain" for r in people),
    }
    expected = {"remaining_named_non_letter": 9, "letter_list_only_present": 33,
                "letter_list_only_uncertain": 33}
    if strata != expected:
        raise SystemExit(f"pass-five strata changed: {strata}")

    # The eligible frame is a claim-time property of this frozen cohort. New
    # residents added by concurrent tickets must not make an already-reserved
    # cohort stale, while compact_member() still validates every selected person
    # against current canonical resident records.
    technical_nonreconstructed = 848
    return {
        "_doc": "T-0479's fixed fifth 75-person cohort. The compact manifest carries identity and stratum only; the selector validates current resident records.",
        "version": 1,
        "ticket": "T-0479",
        "scene_date": "1835-07-01",
        "generated_by": "tools/select_resident_research_pass_5.py",
        "population_frame": {
            "technical_nonreconstructed_entries": technical_nonreconstructed,
            "merged_reviews_before_pass": len(prior_merged),
            "pass4_claimed_not_yet_merged": len(PASS4_CLAIMED_IDS),
            "prior_reviewed_or_claimed": len(prior_merged | PASS4_CLAIMED_IDS),
            "sample_size": 75,
            "cumulative_reviewed_or_claimed": len(prior_merged | PASS4_CLAIMED_IDS) + 75,
            "strata": strata,
        },
        "people": people,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args()
    doc = derive()
    rendered = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        # The committed manifest is intentionally compact. Formatting is not
        # evidence; compare the parsed frozen manifest to the re-derived object.
        if not OUT.exists() or json.loads(OUT.read_text()) != doc:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale; regenerate without --gate")
        print("resident research pass five: 75 people, committed manifest current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered)
    print("resident research pass five: wrote 75 people (9 remaining named non-letter, 33 present-list, 33 uncertain-list)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
