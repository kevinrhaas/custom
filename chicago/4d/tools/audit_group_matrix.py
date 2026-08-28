#!/usr/bin/env python3
"""Audit `district_group_matrix` against the town that actually stands (T-0211).

`data/reconstruction/1835_building_inventory.json` carries the same aggregate three
ways — `family_targets` (35 families), `district_group_matrix` (10 groups x 4
districts) and `districts` (4 totals). `tools/reconcile_665.py` asserts that all
three SUM to `roof_total`, and that each group's families sum to that group's row
total. **Nothing asserted anything about a group's split BY DISTRICT**, and the two
views were authored independently.

T-0032 (PR #388) found what that permits, on the tenth row. `institutional_public`
read south 10 / west 1 / north 1 while the town's named institutional records stood
south 5 / west 1 / north 3. Every sum closed. The consequence was live:
`reconcile_665.py` apportioned the south's phantom institutional headroom into family
I3, the block schedule dealt those slots to blocks whose generator refuses
institutional families by name (L93), and the North Division was told it had room for
one institutional roof while three already stood there.

## What this tool asserts, and what it deliberately does not

**The fix for I3 does not generalise.** An institutional row can be held to a census
because Chicago's public buildings are enumerable. Dwellings, stores and barns are
not — an anonymous dwelling is a legitimate count-unit toward a documented aggregate,
so "the row equals what stands" is the WRONG assertion for the other nine rows, and a
cell standing UNDER its target is the programme working, not a defect.

What can be asserted is weaker and still catches the T-0032 shape:

1. **The three views agree on the district axis too.** Each row's four cells sum to
   its own `total`; each district COLUMN sums to that district's `districts[d].target`;
   the row totals sum to `roof_total`. All three held when this was written, and none
   of them was checked anywhere — the matrix could have been edited into disagreement
   with the district totals and only the district totals would have been believed.

2. **An overshoot is DECLARED, not clamped.** Where a district already stands OVER its
   group row, `reconcile_665.py` clamps with `max(0, ...)` and sheds the excess in an
   unnamed loop, so a row that is wrong by five roofs looks exactly like a row that is
   right. Every overshoot must therefore appear in the inventory's
   `district_group_overshoots` with its size and the reason it is tolerated. An
   undeclared overshoot fails; so does a declaration whose size no longer matches the
   dataset, and so does one for a cell that has stopped overshooting — a stale
   declaration is the same silence one step later.

    tools/audit_group_matrix.py             print the 10-row x 4-district audit
    tools/audit_group_matrix.py --check     the gate
    tools/audit_group_matrix.py --self-test prove the gate's assertions still fire
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "tools"))

from reconcile_665 import (DATA, DISTRICTS, RECON, group_of, load,  # noqa: E402
                           occupied_lots, standing_roofs)


def measure(inventory) -> dict:
    """What stands, per (district, group), from the committed structure records."""
    grid = load(DATA / "traces" / "vectors" / "thompson_lots.json")
    datum = load(DATA / "datum.json")
    rows = standing_roofs(grid, datum, occupied_lots(grid, datum))
    built: dict[tuple[str, str], int] = {}
    for row in rows:
        n = row["roofs_min"]
        if not n:
            continue
        key = (row["district"], group_of(row["family"]))
        built[key] = built.get(key, 0) + n
    return built


def audit(inventory, built) -> dict:
    """The audit itself: every (district, group) pair with target, standing and gap."""
    matrix = inventory["district_group_matrix"]
    cells = []
    for group, row in matrix.items():
        for district in DISTRICTS:
            target = row[district]
            standing = built.get((district, group), 0)
            cells.append({"district": district, "group": group, "target": target,
                          "standing": standing, "gap": target - standing})
    return {"cells": cells,
            "over": [c for c in cells if c["gap"] < 0]}


def shed_for(inventory, built, district) -> tuple[int, dict[str, int]]:
    """The roofs the district's remainder cannot carry, and where reconcile takes them.

    This reproduces `reconcile_665.programme_document`'s own clamp-and-shed so the
    audit can PRICE it. The point of the ticket is that this loop is unnamed there;
    reading it here is what makes the price sayable.
    """
    matrix = inventory["district_group_matrix"]
    standing = sum(built.get((district, g), 0) for g in matrix)
    remainder = inventory["districts"][district]["target"] - standing
    head = {g: max(0, matrix[g][district] - built.get((district, g), 0)) for g in matrix}
    tally: dict[str, int] = {}
    for _ in range(max(0, sum(head.values()) - remainder)):
        group = sorted(head, key=lambda g: (-head[g], g))[0]
        head[group] -= 1
        tally[group] = tally.get(group, 0) + 1
    return sum(tally.values()), tally


def report(inventory, built) -> str:
    matrix = inventory["district_group_matrix"]
    out = []
    out.append("each cell is target/standing, then the gap: + is room the programme "
               "still has, - is a district already over its row")
    out.append("")
    head = "%-24s %s %8s" % ("group", "".join("%17s" % d for d in DISTRICTS), "row total")
    out.append(head)
    out.append("-" * len(head))
    for group, row in matrix.items():
        cols = []
        for district in DISTRICTS:
            target, stands = row[district], built.get((district, group), 0)
            gap = target - stands
            cols.append("%12s%+5d" % ("%d/%d" % (target, stands), gap))
        out.append("%-24s %s %8d" % (group, "".join(cols), row["total"]))
    out.append("-" * len(head))
    cols = []
    for district in DISTRICTS:
        col = sum(matrix[g][district] for g in matrix)
        stands = sum(built.get((district, g), 0) for g in matrix)
        cols.append("%12s%+5d" % ("%d/%d" % (col, stands), col - stands))
    out.append("%-24s %s %8d" % ("column", "".join(cols),
                                 sum(matrix[g]["total"] for g in matrix)))
    out.append("")
    over = audit(inventory, built)["over"]
    if not over:
        out.append("No district stands over its group row.")
    for cell in over:
        out.append("OVER  %-8s %-24s target %3d, stands %3d, over by %d"
                   % (cell["district"], cell["group"], cell["target"],
                      cell["standing"], -cell["gap"]))
    out.append("")
    for district in DISTRICTS:
        n, tally = shed_for(inventory, built, district)
        if n:
            out.append("SHED  %-8s %d roof(s) taken from %s to pay for the overshoot above"
                       % (district, n, ", ".join("%s (%d)" % (g, c)
                                                 for g, c in sorted(tally.items()))))
    return "\n".join(out)


def failures(inventory, built) -> list[str]:
    matrix = inventory["district_group_matrix"]
    bad: list[str] = []

    # 1. the three views agree on the district axis
    for group, row in matrix.items():
        four = sum(row[d] for d in DISTRICTS)
        if four != row["total"]:
            bad.append(f"{group}: its four district cells sum to {four}, "
                       f"not the row's own total of {row['total']}")
    for district in DISTRICTS:
        col = sum(matrix[g][district] for g in matrix)
        target = inventory["districts"][district]["target"]
        if col != target:
            bad.append(f"{district}: the matrix column sums to {col}, "
                       f"not the district's own target of {target}")
    rows_total = sum(matrix[g]["total"] for g in matrix)
    if rows_total != inventory["targets"]["roof_total"]:
        bad.append(f"the matrix row totals sum to {rows_total}, "
                   f"not roof_total {inventory['targets']['roof_total']}")

    # 2. every overshoot is declared, at its measured size, and no declaration is stale
    declared = {k: v for k, v in inventory.get("district_group_overshoots", {}).items()
                if not k.startswith("$")}
    over = {"%s.%s" % (c["district"], c["group"]): c for c in audit(inventory, built)["over"]}
    for key, cell in sorted(over.items()):
        if key not in declared:
            bad.append(f"{key} stands {cell['standing']} against a row of {cell['target']} "
                       f"— over by {-cell['gap']}, and undeclared. Add it to "
                       f"district_group_overshoots with the reason it is tolerated, or "
                       f"correct the row.")
            continue
        entry = declared[key]
        if entry.get("target") != cell["target"] or entry.get("over") != -cell["gap"]:
            bad.append(f"{key}: declared target {entry.get('target')} over by "
                       f"{entry.get('over')}, measured target {cell['target']} over by "
                       f"{-cell['gap']} — the declaration is stale, re-read it")
        if not str(entry.get("why", "")).strip():
            bad.append(f"{key}: declared with no `why`, which is the silence this "
                       f"gate exists to close")
    for key in sorted(declared):
        if key not in over:
            bad.append(f"{key} is declared as an overshoot and does not overshoot — "
                       f"remove the declaration")
    return bad


def self_test() -> int:
    """Break each assertion in turn on a copy, and require it to fire."""
    inventory = load(RECON / "1835_building_inventory.json")
    built = measure(inventory)
    if failures(inventory, built):
        print("self-test cannot run: the committed inventory is already failing")
        return 1

    cases = []

    bent = copy.deepcopy(inventory)
    bent["district_group_matrix"]["ordinary_dwellings"]["south"] += 1
    cases.append(("a row cell moved without its total", bent, "four district cells sum"))

    bent = copy.deepcopy(inventory)
    bent["districts"]["north"]["target"] += 1
    cases.append(("a district total moved without its column", bent, "matrix column sums to"))

    bent = copy.deepcopy(inventory)
    bent["targets"]["roof_total"] += 1
    cases.append(("roof_total moved without the rows", bent, "row totals sum to"))

    bent = copy.deepcopy(inventory)
    bent.pop("district_group_overshoots", None)
    cases.append(("an overshoot left undeclared", bent, "undeclared"))

    bent = copy.deepcopy(inventory)
    key = next(k for k in bent["district_group_overshoots"] if not k.startswith("$"))
    bent["district_group_overshoots"][key]["over"] += 1
    cases.append(("a declaration gone stale", bent, "the declaration is stale"))

    bent = copy.deepcopy(inventory)
    key = next(k for k in bent["district_group_overshoots"] if not k.startswith("$"))
    bent["district_group_overshoots"][key]["why"] = "   "
    cases.append(("a declaration with no reason", bent, "no `why`"))

    bent = copy.deepcopy(inventory)
    bent["district_group_overshoots"]["south.inns_taverns"] = {
        "target": 5, "over": 1, "why": "invented for the self-test"}
    cases.append(("a declaration for a cell that is fine", bent, "does not overshoot"))

    failed = 0
    for label, broken, expect in cases:
        found = failures(broken, built)
        if any(expect in f for f in found):
            print(f"  ok   {label}")
        else:
            print(f"  FAIL {label}: expected {expect!r}, got {found}")
            failed = 1

    # …and the gate must not cry wolf on a cell that is legitimately UNDER its row,
    # which is what nine of these ten rows look like and must keep looking like.
    under = copy.deepcopy(inventory)
    under["district_group_matrix"]["ordinary_dwellings"]["south"] += 1
    under["district_group_matrix"]["ordinary_dwellings"]["total"] += 1
    under["districts"]["south"]["target"] += 1
    under["targets"]["roof_total"] += 1
    if failures(under, built):
        print("  FAIL a row raised above what stands must stay green")
        failed = 1
    else:
        print("  ok   a row raised above what stands stays green")
    return failed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail on an unasserted gap")
    parser.add_argument("--self-test", action="store_true",
                        help="prove the gate's own assertions still fire")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    inventory = load(RECON / "1835_building_inventory.json")
    built = measure(inventory)
    if args.check:
        bad = failures(inventory, built)
        for line in bad:
            print(f"  {line}")
        if bad:
            print(f"{len(bad)} unasserted gap(s) in district_group_matrix")
            return 1
        over = audit(inventory, built)["over"]
        print(f"district_group_matrix: 40 cells, {len(over)} declared overshoot(s), "
              f"three views agreeing on both axes")
        return 0
    print(report(inventory, built))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
