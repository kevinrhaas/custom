#!/usr/bin/env python3
"""Derive T-0442's fixed, stratified 75-person resident research pilot.

The named cohort is frozen so repeated research runs study the same people.  This
script still re-derives every member from the authoritative household records and
refuses reconstructed people, missing records, duplicate people, or a changed
stratum.  Run with --gate to compare the committed manifest without rewriting it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESIDENTS = ROOT / "data" / "residents"
OUT = ROOT / "data" / "research" / "residents" / "pilot_75_cohort.json"

ESTABLISHED = (
    "hh_carpenter_philo", "hh_caton_john_dean", "hh_dole_george_w",
    "hh_egan_william_b", "hh_hubbard_gurdon",
)

# Fixed after a stratified draw: 25 names recorded present and 25 uncertain.
# All seven letter-list people for whom the corpus records sex are included; the
# rest span the source's name/OCR range.  Freezing the ids prevents a later mint
# or corrected spelling from quietly changing who received research effort.
LETTER_IDS = (
    "hh_ll_hail_aifred", "hh_ll_beddlecome_ash", "hh_ll_gooding_caroline",
    "hh_ll_benubien_charl", "hh_ll_brookins_david", "hh_ll_ehjah_doolittle",
    "hh_ll_boles_george", "hh_ll_vyekoff_henry_s", "hh_ll_demans_j_t",
    "hh_ll_force_john", "hh_ll_bloget_josiah_i", "hh_ll_maccoy_lorenzo",
    "hh_ll_sunny_miches", "hh_ll_anstin_al", "hh_ll_nelson_mary",
    "hh_ll_oakley_benjamin_w", "hh_ll_paddock_harriet", "hh_ll_payne_win",
    "hh_ll_preston_stephen_ii", "hh_ll_starkweather_rob_t", "hh_ll_codding_sally",
    "hh_ll_byam_seth", "hh_ll_soren_helen", "hh_ll_beger_tobias",
    "hh_ll_saunders_william_s", "hh_ll_alanson_b_vaughan",
    "hh_ll_m_vaughton_angus", "hh_ll_ostrander_catherine", "hh_ll_d_v_s_torry",
    "hh_ll_dean_farren", "hh_ll_eli_benn", "hh_ll_franklin_spalding",
    "hh_ll_h_vanderbogart", "hh_ll_hiram_eager", "hh_ll_jacob_langer",
    "hh_ll_james_mcfadden", "hh_ll_jesse_holder", "hh_ll_john_musgrave",
    "hh_ll_jonathan_folliott", "hh_ll_joshua_kinsey", "hh_ll_lucius_b_albyn",
    "hh_ll_morris_cutler", "hh_ll_s_stephens", "hh_ll_orange_chauncy",
    "hh_ll_pierce_howley", "hh_ll_roy_k_westover", "hh_ll_samuel_stuart",
    "hh_ll_theophilus_renwick", "hh_ll_willard_conter", "hh_ll_wm_loring",
)


def load_households() -> dict[str, dict]:
    index = json.loads((RESIDENTS / "index.json").read_text())
    return {
        entry["id"]: json.loads((RESIDENTS / entry["file"]).read_text())
        for entry in index["households"]
    }


def member(hh: dict, evidence: str, reason: str) -> dict:
    person = next((p for p in hh["persons"] if p["id"] == hh["head"]), None)
    if person is None:
        raise SystemExit(f"{hh['id']}: household head is missing")
    if person.get("grade") == "reconstructed":
        raise SystemExit(f"{hh['id']}: reconstructed people are outside T-0442")
    return {
        "household_id": hh["id"],
        "person_id": person["id"],
        "name": person["name"],
        "starting_evidence": evidence,
        "starting_grade": person["grade"],
        "starting_presence": hh["present_on_scene_date"]["value"],
        "starting_occupation": (person.get("occupation") or {}).get("value"),
        "letter_list_returns": person.get("letter_list_returns", []),
        "sources": sorted(person.get("sources", [])),
        "selection_reason": reason,
    }


def derive() -> dict:
    households = load_households()
    people: list[dict] = []

    for hid in ESTABLISHED:
        people.append(member(
            households[hid], "established_profile",
            "Established, occupationally identified resident selected for deeper household research.",
        ))

    richer = sorted(
        (hh for hh in households.values()
         if hh.get("division") == "unplaced"
         and len(hh.get("persons", [])) == 1
         and not hh["persons"][0].get("letter_list_only")
         and hh["persons"][0].get("grade") != "reconstructed"),
        key=lambda hh: hh["id"],
    )
    if len(richer) != 20:
        raise SystemExit(f"expected 20 richer unplaced records, found {len(richer)}")
    for hh in richer:
        people.append(member(
            hh, "newspaper_profile_unplaced",
            "All richer, real named residents still lacking a dwelling were included, not sampled.",
        ))

    for hid in LETTER_IDS:
        hh = households.get(hid)
        if not hh:
            raise SystemExit(f"fixed cohort member {hid} is missing")
        person = hh["persons"][0]
        if not person.get("letter_list_only"):
            raise SystemExit(f"{hid}: no longer marked letter_list_only")
        people.append(member(
            hh, "letter_list_only",
            "Fixed stratified sample of the weakest-evidence cohort: 25 present and 25 uncertain, including every member whose sex was already recorded.",
        ))

    ids = [p["person_id"] for p in people]
    if len(people) != 75 or len(set(ids)) != 75:
        raise SystemExit(f"pilot must contain 75 unique people, got {len(people)}/{len(set(ids))}")
    letter = [p for p in people if p["starting_evidence"] == "letter_list_only"]
    status = {s: sum(p["starting_presence"] == s for p in letter)
              for s in ("present", "uncertain")}
    if status != {"present": 25, "uncertain": 25}:
        raise SystemExit(f"letter-list strata changed: {status}")

    return {
        "_doc": "T-0442's reproducible 75-person research cohort. This is a sampling manifest, not new evidence about any person.",
        "version": 1,
        "scene_date": "1835-07-01",
        "generated_by": "tools/select_resident_research_pilot.py",
        "population_frame": {
            "eligible_real_named_people": sum(
                p["grade"] != "reconstructed"
                for hh in households.values() for p in hh.get("persons", [])),
            "sample_size": 75,
            "strata": {
                "established_profile": 5,
                "newspaper_profile_unplaced": 20,
                "letter_list_only_present": 25,
                "letter_list_only_uncertain": 25,
            },
        },
        "people": people,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true")
    args = parser.parse_args()
    doc = derive()
    rendered = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale; regenerate without --gate")
        print("resident research pilot: 75 people, committed manifest current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered)
    print("resident research pilot: wrote 75 people (5 established, 20 richer unplaced, 50 letter-list)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
