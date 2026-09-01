#!/usr/bin/env python3
"""Compile T-0442's reviewed 75-person pilot into the public resident payload.

The household records remain the authority for asserted identity.  This file
publishes a separate research review so a possible name match can be useful
without silently becoming the person in the 1835 record.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COHORT = ROOT / "data/research/residents/pilot_75_cohort.json"
OUT = ROOT / "data/residents/research_pilot.json"
REVIEWED = "2026-08-31"

# Only findings that add something beyond the starting record are overrides.
# Everything else receives an explicit negative result rather than an invented
# biography.  `asserted` is deliberately false even for strong candidates; a
# later identity-adjudication ticket must move a fact into a household record.
OVERRIDES = {
    "caton_john_dean": {
        "outcome": "corroborated_enrichment",
        "summary": "An Illinois Courts institutional biography independently places Caton in Chicago in 1833 and as a justice of the peace in 1834; it gives his birth as 19 March 1812 in Monroe, New York.",
        "sources": ["illinois_courts_caton_biography"],
        "candidates": [],
    },
    "dole_george_w": {
        "outcome": "corroborated_enrichment",
        "summary": "The Encyclopedia of Chicago biographical index identifies George W. Dole as born 29 February 1800 in Troy, New York. Birthplace is not substituted for the record's immediate pre-Chicago origin.",
        "sources": ["encyclopedia_chicago_biographical_index_d"],
        "candidates": [],
    },
    "carpenter_philo": {
        "outcome": "corroborated_enrichment",
        "summary": "The Encyclopedia of Chicago independently corroborates Carpenter's 1832 arrival and his standing as Chicago's first druggist, but supplies no safer household composition for July 1835.",
        "sources": ["encyclopedia_chicago_medical_pharmaceutical"],
        "candidates": [],
    },
    "doc_j_h_collins": {
        "outcome": "corroborated_enrichment",
        "summary": "The Papers of Abraham Lincoln identifies the attorney as James H. Collins, says he moved to Illinois in 1833, and records his 1834 Chicago practice with former student John D. Caton. The partner and occupation jointly resolve the initials more strongly than name alone.",
        "sources": ["papers_abraham_lincoln_james_h_collins"],
        "candidates": [],
    },
    "doc_a_garrett": {
        "outcome": "candidate_identity",
        "summary": "A strong candidate is Augustus Garrett, an early Chicago auctioneer later elected mayor. The project record prints only an initial, so the candidate is not merged without an independent initials-to-name bridge.",
        "sources": ["cpl_augustus_garrett_biography"],
        "candidates": [{"name": "Augustus Garrett", "assessment": "strong", "asserted": False,
            "basis": "Unusual surname, same city and period, and matching auction trade.",
            "conflicts": ["The 1835 newspaper record gives only A. Garrett."],
            "sources": ["cpl_augustus_garrett_biography"]}],
    },
    "doc_j_curtiss": {
        "outcome": "candidate_identity",
        "summary": "A strong candidate is attorney James Curtiss, later mayor. The trade, city and date align, but the newspaper record gives only J. Curtiss, so the identification remains unasserted.",
        "sources": ["cpl_james_curtiss_biography"],
        "candidates": [{"name": "James Curtiss", "assessment": "strong", "asserted": False,
            "basis": "Matching surname and initial, Chicago legal practice, and contemporaneous period.",
            "conflicts": ["No reviewed source explicitly equates the abbreviated newspaper name with the mayor."],
            "sources": ["cpl_james_curtiss_biography"]}],
    },
    "placed_b_s_morris": {
        "outcome": "candidate_identity",
        "summary": "Buckner Stith Morris is a strong candidate for B. S. Morris, but unusual matching initials are not alone enough to import his later mayoral biography.",
        "sources": ["cpl_buckner_stith_morris_biography"],
        "candidates": [{"name": "Buckner Stith Morris", "assessment": "strong", "asserted": False,
            "basis": "Exact unusual initials and surname in Chicago in the same period.",
            "conflicts": ["The 1835 record supplies no occupation or full given names."],
            "sources": ["cpl_buckner_stith_morris_biography"]}],
    },
    "ll_brookins_david": {
        "outcome": "candidate_identity",
        "summary": "A DuPage County history describes a David Brookins who sold carriages in Chicago before moving his family west. It is a useful regional candidate, not proof that the letter-list name is the same man.",
        "sources": ["dupage_history_david_brookins"],
        "candidates": [{"name": "David Brookins, carriage seller", "assessment": "possible", "asserted": False,
            "basis": "Exact name, early Chicago business, and later residence in nearby DuPage County.",
            "conflicts": ["The county history does not identify the 1835 post-office return."],
            "sources": ["dupage_history_david_brookins"]}],
    },
    "ll_james_mcfadden": {
        "outcome": "candidate_identity",
        "summary": "A La Salle County history supplies a competing James McFadden in northern Illinois, but places his activity at Dayton and Galena rather than Chicago. It is retained as a conflict, not merged.",
        "sources": ["lasalle_history_james_mcfadden"],
        "candidates": [{"name": "James McFadden of Dayton/Galena", "assessment": "rejected", "asserted": False,
            "basis": "Exact name and northern Illinois chronology.",
            "conflicts": ["The source places him away from Chicago during the relevant period."],
            "sources": ["lasalle_history_james_mcfadden"]}],
    },
    "placed_j_w_fell": {
        "outcome": "candidate_identity",
        "summary": "Jesse W. Fell was tested and rejected as the default expansion of J. W. Fell: institutional histories place Jesse in Vandalia in winter 1834–35 and founding Clinton in 1835. The abbreviated Chicago person remains unresolved.",
        "sources": ["mclean_history_jesse_w_fell", "papers_abraham_lincoln_clinton"],
        "candidates": [{"name": "Jesse Weldon Fell", "assessment": "rejected", "asserted": False,
            "basis": "Matching initials and an Illinois career.",
            "conflicts": ["Contemporaneous chronology places Jesse Fell in Vandalia and Clinton, not at the Chicago address."],
            "sources": ["mclean_history_jesse_w_fell", "papers_abraham_lincoln_clinton"]}],
    },
    "ll_alanson_b_vaughan": {
        "outcome": "candidate_identity",
        "summary": "Later Minnesota county histories contain the same unusual name, Alanson B. Vaughan. No reviewed source bridges that later settler to Chicago's letter return, so the lead remains possible only.",
        "sources": ["mower_history_alanson_vaughan"],
        "candidates": [{"name": "Alanson B. Vaughan of Mower County", "assessment": "possible", "asserted": False,
            "basis": "Exact uncommon full name in a later Midwestern record.",
            "conflicts": ["No migration or household record connects him to the Chicago letter-list entry."],
            "sources": ["mower_history_alanson_vaughan"]}],
    },
}


def derive() -> dict:
    cohort = json.loads(COHORT.read_text())
    reviews = []
    for person in cohort["people"]:
        pid, name = person["person_id"], person["name"]
        result = OVERRIDES.get(pid, {
            "outcome": "no_corroboration",
            "summary": "No reliable record found in the reviewed web, institutional-history, digitized-book, newspaper-index and genealogy-finding-aid searches could be tied to this 1835 Chicago person without relying on the name alone.",
            "sources": [],
            "candidates": [],
        })
        reviews.append({
            "person_id": pid,
            "household_id": person["household_id"],
            "name_as_recorded": name,
            "starting_evidence": person["starting_evidence"],
            "reviewed_on": REVIEWED,
            "outcome": result["outcome"],
            "summary": result["summary"],
            "queries": [f'"{name}" Chicago 1835', f'"{name}" Illinois genealogy'],
            "sources": result["sources"],
            "candidates": result["candidates"],
            "identity_rule": "No candidate fact is asserted unless a source bridges the candidate to the 1835 Chicago record by more than name similarity.",
        })
    counts = {key: sum(r["outcome"] == key for r in reviews) for key in
              ("corroborated_enrichment", "candidate_identity", "no_corroboration")}
    source_ids = {path.stem for path in (ROOT / "data/sources").glob("*.json")}
    for review in reviews:
        cited = set(review["sources"])
        for candidate in review["candidates"]:
            if candidate.get("asserted") is not False:
                raise SystemExit(f"{review['person_id']}: candidate must be explicitly unasserted")
            cited.update(candidate.get("sources", []))
        missing = cited - source_ids
        if missing:
            raise SystemExit(f"{review['person_id']}: unresolved source ids {sorted(missing)}")
    return {
        "_doc": "T-0442 public research reviews. Candidate biographies are leads, not asserted resident facts.",
        "version": 1,
        "ticket": "T-0442",
        "scene_date": "1835-07-01",
        "reviewed_on": REVIEWED,
        "cohort_size": len(reviews),
        "eligible_real_named_people": cohort["population_frame"]["eligible_real_named_people"],
        "counts": counts,
        "reviews": reviews,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true")
    args = parser.parse_args()
    doc = derive()
    if len(doc["reviews"]) != 75 or sum(doc["counts"].values()) != 75:
        raise SystemExit("pilot must compile exactly 75 reviews")
    rendered = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.gate:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit("data/residents/research_pilot.json is stale")
        print(f"resident research reviews: 75 current ({doc['counts']})")
    else:
        OUT.write_text(rendered)
        print(f"resident research reviews: wrote 75 ({doc['counts']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
