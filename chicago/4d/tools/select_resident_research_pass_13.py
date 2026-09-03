#!/usr/bin/env python3
"""Fix cohorts 13, 14 and 15 — the named residents that have no research row.

    tools/select_resident_research_pass_13.py            (re)write the manifest
    tools/select_resident_research_pass_13.py --gate     the committed manifest is current

T-0492 fixes all three here, in one file, so that T-0508, T-0509 and T-0510 do not
edit `tools/check.sh` and the same population frame at the same moment in three
parallel runs. `_14.py` and `_15.py` are two lines each and import this.

WHAT THE FRAME ACTUALLY IS, MEASURED RATHER THAN ASSERTED. The ticket asks for 237
named people with no research row, in three cohorts of 79. The tree holds **228**,
and the arithmetic is worth writing down because the difference is not rounding:

    238  people carrying no `resident_research` block at all
     -5  unnamed placeholders ("The rest of the Beaubien household, unnamed" and
         four like it) — a count, not a person, and outside every cohort since the
         pilot
     -5  real named people whose ids and containers are `inf_*` / `hh_inf_*`
         (J. Garland, J. W. Reed, Dr. Josiah C. Goodhue, Thomas S. Eels,
         J. Shrigley), retained unplaced by T-0489. `select_resident_research_pass_5.py`
         refuses an `inf_` id outright and this follows it. They are real people and
         they are worth researching; that is a ticket, not a silent inclusion here.
    ---
    228  = 76 + 76 + 76

AND WHERE THEY COME FROM, WHICH IS THE SURPRISE. 225 of the 228 are the **pilot,
pass 2 and pass 3 cohorts** — reserved, and never researched: no findings ledger,
no reference package, no row on any person. That is T-0511's finding from the other
side. So T-0492's acceptance clause "zero overlap with passes 1-12" cannot be met
as written — the population that satisfies it is THREE PEOPLE — and the non-overlap
that carries the meaning is stated instead:

  * zero overlap AMONG 13, 14 and 15;
  * zero overlap with the 611 people who DO carry a research row, which is passes
    4-12 and the reference packages behind them.

Researching a person the pilot reserved in June and never reviewed is the work the
owner asked for. Refusing to, because a reservation exists, is how 225 people stay
unresearched for ever.

THE FRAME IS FROZEN, and deliberately. It was measured on 2026-09-03 against
`data/residents/households/*.json`, sorted inside each stratum, round-robin
interleaved across the three strata and chunked in fixed order. A person who
acquires a research row after this — which is what T-0508 to T-0510 are for — does
NOT make the manifest stale; a person who VANISHES, or turns into a placeholder,
does, and the gate says so.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESIDENTS = ROOT / "data" / "residents"
RESEARCH = ROOT / "data" / "research" / "residents"

# Frozen 2026-09-03. Sorted within `established_profile`, `letter_list_only_present`
# and `letter_list_only_uncertain`, then interleaved one from each in turn, so no
# cohort is all of one stratum and the three are comparable to each other.
FRAME = (
    "adams_william_h", "ll_aiker_samuel", "ll_aaron_parcel",
    "bates_john_jr", "ll_akers_simon", "ll_absolam_reel",
    "beaubien_jean_baptiste", "ll_allen_william", "ll_adam_vandorwerk",
    "beaubien_josette", "ll_allin_richard", "ll_alanson_b_vaughan",
    "beaubien_madore", "ll_alling_prudde", "ll_alexander_wilkes",
    "beaubien_mark", "ll_anderson_eli_f", "ll_alexr_h_tucker",
    "beckford_printer", "ll_anstin_al", "ll_alfred_churchill",
    "blodgett_tyler_k", "ll_archer_joseph", "ll_alison_b_vaughn",
    "brown_lemuel", "ll_avery_charles", "ll_almon_perring",
    "brown_mrs_rufus", "ll_ayres_levi", "ll_alonzo_castle",
    "brown_rufus", "ll_bailly_joseph", "ll_alonzo_murray",
    "caldwell_billy", "ll_bakwith_albert", "ll_alonzo_murry",
    "calhoun_john", "ll_bebee_orson", "ll_alva_crandal",
    "carpenter_philo", "ll_beddlecome_ash", "ll_alva_dunlap",
    "carver_david", "ll_beeson_william", "ll_amanda_miner",
    "casey_edward_w", "ll_beger_tobias", "ll_amos_rathburn",
    "caton_john_dean", "ll_bemis_samuel_c", "ll_amy_c_wear",
    "church_thomas", "ll_benton_datas_e", "ll_andrew_miles",
    "clybourne_archibald", "ll_benubien_charl", "ll_angeline_vann",
    "cobb_silas_b", "ll_bishop_j_e", "ll_anthony_heere",
    "cohen_peter", "ll_blair_william_g", "ll_aram_winsor",
    "couch_ira", "ll_bloget_josiah_i", "ll_archibald_knox",
    "couch_james", "ll_blood_amos", "ll_aron_parcell",
    "davis_john", "ll_bly_rouse", "ll_asa_brundage",
    "davis_t_o", "ll_boardman_elect", "ll_asa_doel",
    "doc_a_garrett", "ll_boles_george", "ll_austin_parsalls",
    "doc_byram_king", "ll_bostwick_e_b", "ll_b_r_paige",
    "doc_e_l_thrall", "ll_bradstreet_j_p", "ll_bennet_bailey",
    "doc_elmira_fowler", "ll_brookins_david", "ll_caleb_foster",
    "doc_h_b_clarke", "ll_brooks_gardner", "ll_carl_romer",
    "doc_h_c_bennett", "ll_brush_matthias", "ll_charles_c_drake",
    "doc_h_crocker", "ll_bullen_jeduthnn", "ll_charles_h_bartlett",
    "doc_h_sherman", "ll_bullock_stephen", "ll_charles_t_richards",
    "doc_henry_moore", "ll_burbee_jonathan", "ll_chas_h_chapman",
    "doc_j_a_marshall", "ll_burdick_paul", "ll_chester_house",
    "doc_j_curtiss", "ll_butterfield_ben", "ll_clark_b_albee",
    "doc_j_h_collins", "ll_byam_seth", "ll_constant_abbott",
    "doc_james_grant", "ll_case_nehemiah", "ll_curtis_parkes",
    "doc_r_stewart", "ll_chadwick_joseph", "ll_d_v_s_torry",
    "doc_samuel_lewis", "ll_chamberlain_l_c", "ll_dangerfield_dunn",
    "doc_wm_sabine", "ll_chambers_john", "ll_david_ingersall",
    "dole_george_w", "ll_chanpagne_batist", "ll_david_p_frame",
    "egan_emeline", "ll_chappel_eliza_mir", "ll_dean_farren",
    "egan_william_b", "ll_chase_peter", "ll_eben_griswold",
    "elston_daniel", "ll_clark_erastus", "ll_ebenozer_alden",
    "fullerton_alexander", "ll_codding_sally", "ll_elam_tuller",
    "gale_stephen_f", "ll_comstock_h_h", "ll_eli_benn",
    "goss_o", "ll_cook_rowland_i", "ll_elihu_d_filer",
    "greene_john", "ll_cooley_edward_v", "ll_elijah_wentworth_sen",
    "hamilton_richard_j", "ll_covell_thomas_r", "ll_enos_covalt",
    "harmon_charles_l", "ll_curtenius_fred_k", "ll_franklin_spalding",
    "harmon_elijah_d", "ll_curtis_liman", "ll_frederick_w_page",
    "harmon_isaac_d", "ll_davenport_dennis", "ll_george_r_makepiece",
    "heacock_russel_e", "ll_demans_j_t", "ll_gregory_e_legg",
    "hogan_john_s_c", "ll_dement_wm", "ll_h_vanderbogart",
    "hubbard_gurdon", "ll_dow_albert_f", "ll_hannah_hurlburt",
    "ingersoll_chester", "ll_ehjah_doolittle", "ll_hiram_eager",
    "jones_benjamin", "ll_fairchilds_ransom", "ll_jacob_langer",
    "kinzie_john_h", "ll_felch_alaneon", "ll_james_mcfadden",
    "kinzie_juliette", "ll_force_john", "ll_jesse_holder",
    "owen_thomas_jv", "ll_ford_ebenezer", "ll_john_musgrave",
    "pearsons_hiram", "ll_galusha_ezra", "ll_jonathan_folliott",
    "peck_philip", "ll_gooding_caroline", "ll_joshua_kinsey",
    "placed_b_s_morris", "ll_hail_aifred", "ll_lucius_b_albyn",
    "placed_hoit_thomas", "ll_maccoy_lorenzo", "ll_m_vaughton_angus",
    "placed_j_k_boyer", "ll_nelson_mary", "ll_morris_cutler",
    "placed_j_w_fell", "ll_oakley_benjamin_w", "ll_orange_chauncy",
    "porter_eliza_chappel", "ll_paddock_harriet", "ll_ostrander_catherine",
    "porter_jeremiah", "ll_payne_win", "ll_pierce_howley",
    "robinson_alexander", "ll_preston_stephen_ii", "ll_roy_k_westover",
    "robinson_catherine", "ll_saunders_william_s", "ll_s_stephens",
    "snow_george_w", "ll_soren_helen", "ll_samuel_stuart",
    "spring_giles", "ll_starkweather_rob_t", "ll_theophilus_renwick",
    "taylor_augustine", "ll_sunny_miches", "ll_willard_conter",
    "temple_children_four", "ll_vyekoff_henry_s", "ll_wm_loring",
    "temple_john_t", "temple_mrs_john_t", "wright_john",

)

CHUNKS = {13: (0, 76), 14: (76, 152), 15: (152, 228)}
ORDINALS = {13: "thirteenth", 14: "fourteenth", 15: "fifteenth"}
TICKETS = {13: "T-0508", 14: "T-0509", 15: "T-0510"}

PRIOR_COHORTS = (
    "pilot_75_cohort.json",
    *("pass_%02d_75_cohort.json" % n for n in range(2, 12)),
    "pass_12_11_cohort.json",
)


def out_path(pass_no: int) -> Path:
    return RESEARCH / ("pass_%d_76_cohort.json" % pass_no)


def load_people() -> dict:
    """Every person in the tree, read from the household files themselves.

    NOT from `index.json`: on 2026-09-03 the index lists 824 households and 825
    stand on disk (`hh_adams_william_h.json` is unlisted — T-0491's finding). The
    records are the town; the index is a summary of it, and a cohort must not move
    because a summary is behind.
    """
    people = {}
    for path in sorted((RESIDENTS / "households").glob("*.json")):
        household = json.loads(path.read_text(encoding="utf-8"))
        for person in household.get("persons") or []:
            pid = person.get("id")
            if pid in people:
                raise SystemExit("duplicate person id %s" % pid)
            people[pid] = (household, person)
    return people


def stratum_of(household: dict, person: dict) -> str:
    if not person.get("letter_list_only"):
        return "established_profile"
    return "letter_list_only_%s" % household["present_on_scene_date"]["value"]


def member(people: dict, person_id: str) -> dict:
    """Validate one frozen member against the records as they stand today."""
    if person_id not in people:
        raise SystemExit("frozen cohort member %s is no longer in the town" % person_id)
    household, person = people[person_id]
    if person.get("grade") == "reconstructed":
        raise SystemExit("%s: a reconstructed person is outside these cohorts" % person_id)
    if person_id.startswith("inf_") or str(household.get("id", "")).startswith("hh_inf_"):
        raise SystemExit("%s: an inf_* record is outside these cohorts" % person_id)
    name = person.get("name") or ""
    if not name or "unnamed" in name.lower():
        raise SystemExit("%s: an unnamed placeholder is outside these cohorts" % person_id)
    return {
        "household_id": household["id"],
        "person_id": person_id,
        "name": name,
        "stratum": stratum_of(household, person),
        "starting_grade": person.get("grade"),
        "starting_presence": household["present_on_scene_date"]["value"],
        "letter_list_returns": person.get("letter_list_returns", []),
        "sources": sorted(person.get("sources", [])),
    }


def researched_ids(people: dict) -> set:
    return {pid for pid, (_h, p) in people.items() if p.get("resident_research")}


def derive(pass_no: int) -> dict:
    if len(FRAME) != 228 or len(set(FRAME)) != 228:
        raise SystemExit("the frozen frame is not 228 unique people: %d/%d"
                         % (len(FRAME), len(set(FRAME))))
    people = load_people()
    lo, hi = CHUNKS[pass_no]
    ids = list(FRAME[lo:hi])
    rows = [member(people, pid) for pid in ids]

    # Zero overlap among the three, which is the collision lock T-0508 to T-0510
    # run against in parallel.
    for other, (olo, ohi) in CHUNKS.items():
        if other == pass_no:
            continue
        if overlap := set(FRAME[olo:ohi]).intersection(ids):
            raise SystemExit("cohort %d overlaps cohort %d: %s"
                             % (pass_no, other, sorted(overlap)))

    # Zero overlap with the people who already carry a research row. This is the
    # non-overlap that means something; see the module docstring for why "zero
    # overlap with passes 1-12" is not the same claim and is not made.
    if overlap := researched_ids(people).intersection(ids):
        raise SystemExit("cohort %d claims people who already carry a research row: %s"
                         % (pass_no, sorted(overlap)))

    strata = {}
    for row in rows:
        strata[row["stratum"]] = strata.get(row["stratum"], 0) + 1

    reserved_by_earlier_passes = set()
    for name in PRIOR_COHORTS:
        path = RESEARCH / name
        if path.exists():
            reserved_by_earlier_passes.update(
                r["person_id"] for r in json.loads(path.read_text(encoding="utf-8"))["people"])

    return {
        "_doc": "%s's fixed %s cohort: 76 named residents carrying no research row. "
                "The manifest is a reservation and identity lock; research outcomes "
                "live in the findings ledger beside it."
                % (TICKETS[pass_no], ORDINALS[pass_no]),
        "version": 1,
        "ticket": TICKETS[pass_no],
        "scene_date": "1835-07-01",
        "generated_by": "tools/select_resident_research_pass_13.py",
        "selection_policy":
            "Frozen 2026-09-03 from data/residents/households/*.json: every named "
            "person carrying no resident_research block, excluding unnamed placeholders "
            "and inf_*/hh_inf_* records, sorted within the established / present-list / "
            "uncertain-list strata, interleaved one from each stratum in turn, and "
            "chunked 76/76/76 in fixed order. A member that later acquires a research "
            "row does not make the manifest stale; a member that leaves the town does.",
        "population_frame": {
            "named_people_without_a_research_row": 228,
            "cohort_13_14_15_sizes": [76, 76, 76],
            "sample_size": len(rows),
            "already_reserved_by_passes_1_to_12": len(
                reserved_by_earlier_passes.intersection(ids)),
            "reservation_note":
                "225 of the 228 were reserved by the pilot, pass 2 and pass 3 and never "
                "researched — no findings ledger, no reference package, no row on any "
                "person (T-0511). These cohorts research them. Overlap with a "
                "RESERVATION is intended; overlap with a completed research row is "
                "refused above.",
            "strata": strata,
        },
        "people": rows,
    }


def run(pass_no: int, argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    doc = derive(pass_no)
    path = out_path(pass_no)
    if args.gate:
        # The committed manifest is the frozen thing; formatting is not evidence.
        if not path.exists() or json.loads(path.read_text(encoding="utf-8")) != doc:
            raise SystemExit("%s is stale; regenerate it without --gate"
                             % path.relative_to(ROOT))
        print("resident research pass %d: %d people, committed manifest current"
              % (pass_no, len(doc["people"])))
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("resident research pass %d: wrote %d people (%s)"
          % (pass_no, len(doc["people"]),
             ", ".join("%s %s" % (v, k) for k, v in sorted(doc["population_frame"]["strata"].items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(run(13))
