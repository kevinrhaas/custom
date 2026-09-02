#!/usr/bin/env python3
"""One-shot T-0478 reconciliation of resident manifest and published mirrors."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
RESIDENTS = ROOT / "data/residents"
SIDE = ROOT / "data/sidecars/1835"
SITE = REPO / "site/chicago/4d"


def sync_index() -> None:
    household_path = RESIDENTS / "households/hh_porthier_joseph.json"
    household = json.loads(household_path.read_text())
    index_path = RESIDENTS / "index.json"
    index = json.loads(index_path.read_text())
    matches = [row for row in index["households"] if row["id"] == "hh_porthier_joseph"]
    if len(matches) != 1:
        raise SystemExit(f"expected one Porthier manifest row, found {len(matches)}")
    matches[0]["present_on_scene_date"] = household["present_on_scene_date"]["value"]
    index_path.write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n")
    if matches[0]["present_on_scene_date"] != "absent":
        raise SystemExit("Porthier scene-date presence did not reconcile to absent")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def sync_published() -> None:
    # T-0478 changes two canonical households and resident research outputs. Copy the
    # canonical files and the sidecars re-derived from them without deleting unrelated
    # published files that may be owned by concurrent work.
    for name in ("hh_porthier_joseph.json", "hh_pruyne_kimberly.json"):
        copy_file(
            RESIDENTS / "households" / name,
            SITE / "data/residents/households" / name,
        )
    copy_file(RESIDENTS / "index.json", SITE / "data/residents/index.json")
    copy_file(RESIDENTS / "research_pilot.json", SITE / "data/residents/research_pilot.json")
    for source in SIDE.glob("*.json"):
        copy_file(source, SITE / "data/sidecars/1835" / source.name)
    copy_file(ROOT / "tickets/tickets.json", SITE / "tickets.json")


def assert_closeout() -> None:
    index = json.loads((RESIDENTS / "index.json").read_text())
    porthier = next(row for row in index["households"] if row["id"] == "hh_porthier_joseph")
    household = json.loads((RESIDENTS / "households/hh_porthier_joseph.json").read_text())
    if porthier["present_on_scene_date"] != household["present_on_scene_date"]["value"]:
        raise SystemExit("Porthier resident manifest still disagrees with canonical household")

    research = json.loads((RESIDENTS / "research_pilot.json").read_text())
    if research.get("cohort_size") != 300 or len(research.get("reviews", [])) != 300:
        raise SystemExit("cumulative resident research payload is not 300 reviews")
    pass4 = next((p for p in research.get("passes", []) if p.get("ticket") == "T-0478"), None)
    expected = {
        "corroborated_enrichment": 22,
        "candidate_identity": 4,
        "no_corroboration": 49,
    }
    if not pass4 or pass4.get("counts") != expected:
        raise SystemExit(f"pass-four outcome census is wrong: {pass4}")

    csv_path = REPO / "chicago/reference/resident-research/T-0478/T-0478_resident_research.csv"
    if not csv_path.exists() or sum(1 for _ in csv_path.open(encoding="utf-8")) != 76:
        raise SystemExit("T-0478 CSV must contain header plus 75 resident rows")

    source = json.loads((ROOT / "data/sources/chicago_newspapers_mulford_1835.json").read_text())
    if source.get("type") != "newspaper" or source.get("rights_status") != "check_required":
        raise SystemExit("Mulford newspaper source still violates source vocabulary")

    ticket = (ROOT / "tickets/T-0478-research-fourth-75-person-real-resident-cohort.md").read_text()
    if "state: done" not in ticket or "pr: 641" not in ticket:
        raise SystemExit("T-0478 ticket is not closed against PR #641")

    mirror_pairs = [
        (RESIDENTS / "index.json", SITE / "data/residents/index.json"),
        (RESIDENTS / "research_pilot.json", SITE / "data/residents/research_pilot.json"),
        (RESIDENTS / "households/hh_porthier_joseph.json", SITE / "data/residents/households/hh_porthier_joseph.json"),
        (RESIDENTS / "households/hh_pruyne_kimberly.json", SITE / "data/residents/households/hh_pruyne_kimberly.json"),
        (SIDE / "residents_sources.json", SITE / "data/sidecars/1835/residents_sources.json"),
    ]
    for source_path, mirror_path in mirror_pairs:
        if not mirror_path.exists() or source_path.read_bytes() != mirror_path.read_bytes():
            raise SystemExit(f"published mirror differs: {mirror_path.relative_to(REPO)}")
    print("T-0478 reconciliation assertions: PASS")


def main() -> int:
    sync_index()
    sync_published()
    assert_closeout()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
