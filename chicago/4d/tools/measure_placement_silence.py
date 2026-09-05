#!/usr/bin/env python3
"""A house's live placement against everything its own printings said (T-0440).

    python3 tools/measure_placement_silence.py            the report
    python3 tools/measure_placement_silence.py --check    the invariant, as a gate

WHAT THIS COUNTS, AND WHY IT IS COUNTED RATHER THAN ARGUED.

`compile_gazetteer.py` mints a house's dict from WHICHEVER CLAIM MINTS THE KEY — the
earliest printing the corpus carries — and takes `placement` and `street` from it.
Every later printing's placement is kept as a READING with its own dates (T-0345), but
until T-0440 nothing downstream of the mint ever revised the live one. So a standing
advertisement that ran without an address in its first week and with one afterwards
stood at `{"class": "none"}` for good, `compile_register.resolve_anchor` was handed no
anchor, and the row read `unplaceable` — while three of the house's own printings said
otherwise a few lines below in the same file.

Clark, Filer & Co. is the house it was found on: silent on 1834-05-28, then *"their ware
house on South water St. five [doors east] of the corner [of Randolph st.]"* on
1834-06-11, 1834-06-18 and 1834-07-02, and `unplaceable` in the register throughout.
T-0440 asked for the count of others before it asked for a repair, because a defect one
house shows is a bug and a defect fourteen show is a rule choosing wrongly.

THE TWO POPULATIONS, AND ONLY ONE OF THEM IS THIS PASS'S TO FIX.

  * **SILENT, THEN PLACED** — the live placement places nothing and some printing of the
    same house does. A printing that omits the address does not contradict one that gives
    it; it simply did not repeat it, which is what a standing advertisement does every
    other week. There is no judgement about a house that MOVED to be made here, so
    `compile_gazetteer` takes the earliest placing reading and this report expects the
    count to be ZERO on a compiled tree. `--check` asserts exactly that.

  * **PLACED, THEN PLACED BETTER** — the live placement already puts the house somewhere
    and a later printing puts it somewhere narrower, or somewhere else. Preferring one
    printed address to another is a statement about the house or about the advertisement,
    and the only thing in this project that may make it is the authored `anchor_changes`
    rule, which has to name the anchors verbatim and say what the corpus leaves open.
    **Nothing here repairs these and nothing should**: they are REPORTED, with the class
    they hold and the class they were outranked by, so the queue can see how many are
    waiting on a judgement.

The rank is `compile_gazetteer.placement_rank`, read from that module rather than
retyped, so this report and the compiler cannot disagree about what outranks what.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from compile_gazetteer import SCENE_DATE, placement_rank  # noqa: E402

GAZETTEER = ROOT / "data" / "research" / "newspapers" / "gazetteer.json"
REGISTER = ROOT / "data" / "research" / "newspapers" / "register_1835.json"


def survey():
    """Every house whose live placement is outranked by one of its own readings."""
    gaz = json.loads(GAZETTEER.read_text(encoding="utf-8"))
    reg = {b["id"]: b for b in json.loads(REGISTER.read_text(encoding="utf-8"))["businesses"]}
    scene_iso = SCENE_DATE.isoformat()
    silent, outranked, after_scene = [], [], []
    for biz in gaz["businesses"]:
        live = placement_rank(biz.get("placement"))
        readings = biz.get("placement_readings") or []
        placing = [r for r in readings if placement_rank(r.get("placement")) > 0]
        if not placing:
            continue
        best = max(placement_rank(r.get("placement")) for r in placing)
        if best <= live:
            continue
        # An address first printed after 1 July 1835 was not up on 1 July 1835, so a
        # house whose only placing printings run after the scene date is not a defect —
        # it is the bound working. Reported on its own line, never counted as silence.
        in_scene = [r for r in placing if r["first_issue"] <= scene_iso]
        anchors = sorted({(r.get("class"), r.get("anchor") or "",
                           (r.get("placement") or {}).get("street") or "")
                          for r in placing})
        row = {
            "id": biz["id"], "name": biz.get("name"),
            "live_class": (biz.get("placement") or {}).get("class") or "none",
            "best_class": next(r.get("class") for r in placing
                               if placement_rank(r.get("placement")) == best),
            "readings": len(readings), "distinct_placing_anchors": len(anchors),
            "action": (reg.get(biz["id"]) or {}).get("action"),
            "took_a_later_printing": bool(biz.get("placement_from")),
        }
        if live == 0 and not in_scene:
            after_scene.append(row)
        else:
            (silent if live == 0 else outranked).append(row)
    return silent, outranked, after_scene


def report() -> int:
    silent, outranked, after_scene = survey()
    gaz = json.loads(GAZETTEER.read_text(encoding="utf-8"))
    print("A HOUSE'S LIVE PLACEMENT AGAINST ITS OWN PRINTINGS — T-0440\n")
    took = [b for b in gaz["businesses"] if b.get("placement_from")]
    print("  house(s) compiled                                          %4d"
          % len(gaz["businesses"]))
    print("  — placed by a printing later than the one that minted them %4d"
          % len(took))
    print("  — live placement places NOTHING while a printing does      %4d  "
          "(this is the defect; it must be 0)" % len(silent))
    print("  — live placement outranked by a printed address            %4d  "
          "(a judgement, and `anchor_changes` owns it)" % len(outranked))
    print("  — placed by no printing on or before %s          %4d  "
          "(the scene-date bound, working)" % (SCENE_DATE.isoformat(), len(after_scene)))
    if took:
        print("\nSILENT WHEN MINTED, PLACED BY A LATER PRINTING — repaired here")
        for b in sorted(took, key=lambda b: b["id"]):
            frm = b["placement_from"]
            street = frm.get("street_from_reading")
            print("  %-52s %-11s %s%s"
                  % (b["id"], (b.get("placement") or {}).get("class"),
                     frm["first_issue"], "  street: %s" % street if street else ""))
    if silent:
        print("\nSTILL SILENT WHILE A PRINTING PLACES THEM — the defect, unrepaired")
        for r in sorted(silent, key=lambda r: r["id"]):
            print("  %-52s %s -> %s" % (r["id"], r["live_class"], r["best_class"]))
    if after_scene:
        print("\nPLACED ONLY BY A PRINTING AFTER THE SCENE DATE — left silent on "
              "purpose (AGENTS.md rule 3)")
        for r in sorted(after_scene, key=lambda r: r["id"]):
            print("  %-52s would have been %-11s register: %s"
                  % (r["id"], r["best_class"], r["action"]))
    if outranked:
        print("\nA PRINTED ADDRESS OUTRANKED BY A LATER PRINTED ADDRESS — left alone on "
              "purpose;\nreordering two printed addresses is a judgement and "
              "`anchor_changes` is where it is written")
        for r in sorted(outranked, key=lambda r: r["id"]):
            print("  %-52s %-11s outranked by %-11s %d distinct anchor(s), register: %s"
                  % (r["id"], r["live_class"], r["best_class"],
                     r["distinct_placing_anchors"], r["action"]))
    return 0


def check() -> int:
    silent, outranked, after_scene = survey()
    if silent:
        print("PLACEMENT SILENCE FAIL — %d house(s) hold a live placement that places "
              "nothing while one of their own printings places them:" % len(silent))
        for r in sorted(silent, key=lambda r: r["id"]):
            print("  - %s (%s, outranked by %s). compile_gazetteer.py takes the earliest "
                  "placing reading; re-run `tools/compile_gazetteer.py --build`."
                  % (r["id"], r["live_class"], r["best_class"]))
        return 1
    took = len([1 for b in json.loads(GAZETTEER.read_text(encoding="utf-8"))["businesses"]
                if b.get("placement_from")])
    print("  ok    no house is placed by a printing that gave no address; %d house(s) "
          "take a later printing's, %d wait on an `anchor_changes` judgement, %d are "
          "placed by nothing printed on or before the scene date"
          % (took, len(outranked), len(after_scene)))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="fail if any house is left placed by a silent printing")
    args = ap.parse_args()
    raise SystemExit(check() if args.check else report())
