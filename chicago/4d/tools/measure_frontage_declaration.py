#!/usr/bin/env python3
"""Does a frontage run stand across every lot its recipe entry declares?

T-0429 found the first one that did not. `blk_south_water_lasalle`'s first deal
declared lots 0, 2 and 4 of its South Water face and its three units stood on lot 4
alone: the run is anchored `corner: east` and packed back west until the roofs it was
dealt ran out, which happened inside the eastmost lot. T-0449 was opened to measure the
other eight entries of that row and correct them the same way. This tool is that
measurement, committed so it is a gate rather than a reading somebody once took.

WHAT IS MEASURED. A frontage entry's `lots` list is projected onto the block face out of
`tools/block_faces.py`, and so is every committed footprint of the entry's own frontage
slots. A lot is REACHED when the run's along-face span overlaps the lot's, and lots that
do not come to the face at all are not candidates — `frontage_strip` in
`tools/generate_block_infill.py` refuses those with the same test, so the two files agree
about which lots a north-face run could possibly stand on. Nothing here authors a
coordinate: the run's span is read off the committed structure records and the lot spans
off the committed plat grid.

WHAT THE FIELD TURNED OUT TO BE DOING, and it is why this tool reports rather than
corrects. `frontage.lots` answers three questions at once:

  1. the run's own strip — `frontage_strip` runs it from the west line of the westmost
     declared lot to the east line of the eastmost, and an east-anchored run takes its
     anchor off that eastmost line;
  2. the block's lot classes — `check_block` puts every declared lot in `built on by this
     parcel`, which is also what makes an ancillary yard building on that lot stand
     behind a roof of the same parcel;
  3. the block's declared BUSINESS FRONT — `shared_business_fronts` in
     `tools/plat_occupancy.py` applies the owner's 2026-08-27 clause (a documented store
     at the street does not exhaust a business-front lot) only to `int(index) for index
     in frontage["lots"]`.

So narrowing a declaration to the ground its run measurably stands on does not only
retract a false claim; it withdraws the owner's clause from the lots it drops, and on
this row two of them carry a documented store and a yard building of the same parcel.
Measured on this branch, `generate_block_infill.py --check` refuses all three of the
remaining corrections, each for a coupled reason and none for the declaration itself:

    franklin  [4, 6] -> [6]     the yard building on lot 4 stands behind no roof
    wells  [0, 2, 4] -> [2, 4]  the yard building on lot 0 stands behind h_jones_store
    dearborn [0,2,4] -> [4]     the yard building on lot 0 stands behind chicago_american_office

Those three stand in `CONCEDED` below with the measurement that found them. Everything
else has to be exact, so a NEW over-declaration — a run dealt lots it never reaches — is
a failure here at the commit that writes it, which is the whole point of gating a
reading nobody would otherwise take twice.

    tools/measure_frontage_declaration.py            report every entry
    tools/measure_frontage_declaration.py --check    the gate
    tools/measure_frontage_declaration.py --self-test
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from block_faces import extent, face_frame, project
from plat_occupancy import footprints

ROOT = Path(__file__).resolve().parent.parent
LOTS = ROOT / "data" / "traces" / "vectors" / "thompson_lots.json"
DATUM = ROOT / "data" / "datum.json"
PARCELS = ROOT / "data" / "reconstruction" / "1835_platted_block_parcels.json"
PREFIX = "recon_1835_blk_"

# The same half-metre `frontage_strip` allows a lot before it calls it off the face, and
# the same sliver an overlap has to beat before it counts as standing across a lot.
REACH_M = 0.5
OVERLAP_M = 0.01

# The three entries this gate concedes, with what refuses the correction. Each is a
# statement about a coupling, not about the geometry: the measurement below is not in
# doubt on any of them and the narrowed list is written down so the next run does not
# have to take the reading again. T-0449 measured these on 2026-09-12; the follow-on
# ticket it split out carries the decision.
CONCEDED = {
    "phase3_platted_block_south_water_franklin": (
        [6],
        "T-0449, 2026-09-12. The three units stand 77.13 m to 95.04 m along the face and "
        "lot 6 runs 71.47 m to 96.54 m, so the run is inside lot 6 alone and lot 4 "
        "(47.06 m to 72.12 m) carries none of it. Narrowing it to [6] is refused by "
        "`check_block`: this parcel's A3 yard building stands on lot 4, and a lot no "
        "roof of the parcel stands on leaves that yard building serving nothing. "
        "Correcting the declaration therefore means re-lotting a roof, which moves "
        "geometry and is not this ticket's to do."),
    "phase3_platted_block_south_water_wells": (
        [2, 4],
        "T-0449, 2026-09-12. The three units stand 36.15 m to 71.71 m and lot 0 runs "
        "-0.63 m to 24.40 m, so the run never crosses back into it; lots 2 and 4 carry "
        "the whole run. Narrowing it to [2, 4] withdraws the owner's 2026-08-27 "
        "business-front clause from lot 0 — `shared_business_fronts` reads it off this "
        "very list — so H. Jones's store exhausts the lot and this parcel's A3 yard "
        "building on it reads as standing behind a store the parcel did not build. The "
        "clause is about a FACE and the field it is keyed to is about a RUN; which of "
        "the two moves is the follow-on ticket's question."),
    "phase3_platted_block_south_water_dearborn": (
        [4],
        "T-0449, 2026-09-12. The three units stand 59.67 m to 77.28 m; lot 4 runs "
        "51.86 m to 78.78 m and carries all of them, lot 2 stops at 52.86 m and lot 0 at "
        "26.94 m. T-0432 already recorded this block as a live instance and deliberately "
        "left the entry alone. Narrowing it to [4] fails the same way `wells` does, with "
        "the Chicago American's office in place of H. Jones's store."),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_units(entry: dict) -> list[str]:
    """The record ids of the entry's own frontage slots, numbered as the generator does."""
    seq0 = int(entry.get("seq_start", 1))
    return [f"{PREFIX}{entry['block_id'].removeprefix('blk_')}_{slot['family'].lower()}_{seq:02d}"
            for seq, slot in enumerate(entry["slots"], start=seq0)
            if slot.get("stands_on") == "frontage"]


def reached(entry: dict, block: dict, placed: dict[str, list[tuple[float, float]]]
            ) -> tuple[list[int], tuple[float, float]]:
    """(the lots the run measurably stands across, its along-face span)."""
    frame = face_frame(block, entry["frontage"]["face"])
    spans = [extent(frame, placed[sid]) for sid in run_units(entry) if sid in placed]
    if not spans:
        raise SystemExit(f"{entry['programme_phase']}: the entry names a frontage run "
                         f"and no committed record stands on it")
    run = (min(s[0] for s in spans), max(s[1] for s in spans))
    out = []
    for index, lot in enumerate(block["lots"]):
        corners = [project(frame, tuple(p)) for p in lot["polygon"]]
        if max(c[1] for c in corners) < -REACH_M:
            continue                                  # this lot is not on this face
        lo, hi = min(c[0] for c in corners), max(c[0] for c in corners)
        if min(run[1], hi) - max(run[0], lo) > OVERLAP_M:
            out.append(index)
    return out, run


def survey() -> list[dict]:
    grid, datum = load(LOTS), load(DATUM)
    blocks = {block["id"]: block for block in grid["blocks"]}
    placed: dict[str, list[tuple[float, float]]] = {}
    for sid, world in footprints(datum):
        placed.setdefault(sid, world)
    out = []
    for entry in load(PARCELS)["blocks"]:
        if not entry.get("frontage"):
            continue
        lots, run = reached(entry, blocks[entry["block_id"]], placed)
        declared = [int(i) for i in entry["frontage"]["lots"]]
        out.append({"phase": entry["programme_phase"], "block": entry["block_id"],
                    "declared": declared, "reached": lots, "run": run,
                    "over": [i for i in declared if i not in lots]})
    return out


def faults(rows: list[dict]) -> tuple[list[str], list[str]]:
    """(faults, conceded) — an entry declaring ground its run never reaches."""
    bad, conceded = [], []
    for row in rows:
        if not row["over"]:
            continue
        line = (f"{row['phase']}: the run stands {row['run'][0]:.2f} m to "
                f"{row['run'][1]:.2f} m along its face, which is lot(s) {row['reached']}, "
                f"and the entry declares {row['declared']} — lot(s) {row['over']} carry "
                f"none of it")
        allowed, why = CONCEDED.get(row["phase"], (None, None))
        if allowed == row["reached"]:
            conceded.append(f"{line}\n    CONCEDED: {why}")
        else:
            bad.append(line)
    for phase, (allowed, _) in CONCEDED.items():
        if not any(row["phase"] == phase and row["over"] for row in rows):
            bad.append(f"{phase} is conceded to {allowed} and no longer over-declares. "
                       f"A concession outliving its defect hides the next one — remove it")
    return bad, conceded


def self_test() -> None:
    grid = load(LOTS)
    block = next(b for b in grid["blocks"] if b["id"] == "blk_south_water_lasalle")
    frame = face_frame(block, "north")
    # The lots of a north face alternate with the Lake-face lots and the two project onto
    # the same stretch of the along axis, so the reach filter is what keeps a Lake lot out
    # of a South Water answer. Without it every north-face run reads twice the ground.
    north = [i for i, lot in enumerate(block["lots"])
             if max(project(frame, tuple(p))[1] for p in lot["polygon"]) >= -REACH_M]
    assert north == [0, 2, 4, 6], north
    # An entry that declares exactly what it reaches is silent, and T-0429's corrected
    # lasalle entry is the worked example the whole ticket is measured against.
    rows = survey()
    lasalle = next(r for r in rows if r["phase"] == "phase3_platted_block_south_water_lasalle")
    assert lasalle["declared"] == lasalle["reached"] == [4], lasalle
    assert not lasalle["over"], lasalle
    # And a concession only holds for the list that was measured: widen it by a lot and
    # the gate has to refuse it again, or a stale concession would cover a new defect.
    bad, conceded = faults([dict(r, over=[0]) if r["phase"] in CONCEDED else r
                            for r in rows])
    assert len(conceded) == len(CONCEDED), (bad, conceded)
    moved = [dict(r, reached=[9]) if r["phase"] in CONCEDED else r for r in rows]
    assert len(faults(moved)[0]) == len(CONCEDED), faults(moved)
    print("measure_frontage_declaration self-test: ok")


def main() -> int:
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return 0
    rows = survey()
    bad, conceded = faults(rows)
    if "--check" in args:
        for line in conceded:
            print(f"  conceded: {line}")
        for line in bad:
            print(f"  {line}")
        if bad:
            print(f"{len(bad)} frontage entr(ies) declare ground their run never reaches")
            return 1
        print(f"{len(rows)} frontage entr(ies) measured, {len(conceded)} conceded")
        return 0
    for row in rows:
        flag = "  <-- over-declared" if row["over"] else ""
        print(f"{row['phase']:<55} declared {str(row['declared']):<10} "
              f"reached {str(row['reached']):<10} run {row['run'][0]:7.2f}..{row['run'][1]:7.2f} m{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
