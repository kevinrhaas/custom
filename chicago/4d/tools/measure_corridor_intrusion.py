#!/usr/bin/env python3
"""How much of this town is drawn standing in its own streets.

ROADMAP K30(a). Every generator in this project asks `plat_corridors.intrusion()` before
it puts a roof anywhere, so no invented building has ever been allowed into a roadway.
Nothing had ever asked the question of the records a PERSON placed. T-A9 measured three of
them by hand, T-A12 added two more, and the entry asked for the distribution rather than
the anecdotes: *"a handful of deep intrusions on one street is a different problem from a
uniform half-metre bias across the grid, and the fix differs accordingly."*

This is the distribution, as a command.

**Two tests, reported separately, because they answer different questions.**

* **lap** — any point of the footprint is inside a platted corridor. This is the drawn
  fault: it is what a visitor standing in the street can see.
* **centroid** — the footprint's centroid is inside one. This is `T-A7`'s test, the one
  that decides whether the lot schedule can see the building at all, and it is a strict
  subset of the lap set.

**A corridor is not the travelled way.** `plat_corridors` says so at length and it governs
here too: L79 records the visible tracks running 5.8-10.5 m inside an 80 ft legal corridor,
so a building 1 m inside a corridor edge is a measurement about the plat and the
georeference, not a building in anybody's way. That is why this tool reports a DEPTH and a
distribution and refuses to name a threshold. **The 2-3.5 m gap in the depths is the one
piece of structure in the data**, and it is reported rather than legislated.

**What it must never do is move a building to make its number smaller.** A position with a
source outranks a corridor this project derived from a module and a traced centreline.

    tools/measure_corridor_intrusion.py                the full table
    tools/measure_corridor_intrusion.py --by-street    the distribution only
    tools/measure_corridor_intrusion.py --recentre     K30(a)'s refuted counterfactual
    tools/measure_corridor_intrusion.py --gate         the ratchet check.sh runs
    tools/measure_corridor_intrusion.py --write-baseline   only to record a repair

This tool exists in the shape it does because of what K30(a) found about T-A7 and T-A14
found about T-A13: a number derived by hand and thrown away does not reproduce, not even at
the commit that states it. Every figure any parcel quotes about corridor intrusion should
come out of here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from generate_plat_lots import point_in_polygon  # noqa: E402
from measure_street_frontage import layer_of  # noqa: E402
from plat_corridors import corridors, intrusion  # noqa: E402
from plat_occupancy import world_polygon  # noqa: E402

BASELINE = ROOT / "tools" / "corridor_intrusion_baseline.json"
STRUCTURES = ROOT / "data" / "structures"

# A depth is quoted and compared to the centimetre. The corridor ring and the footprint
# are both derived, so the last millimetre is arithmetic rather than evidence, and a
# ratchet that fires on floating-point noise is a ratchet that gets switched off.
PLACES = 2
# The ratchet's tolerance. A depth that grows by less than this is not a new fault; a
# depth that grows by more is a building that moved, or a corridor that did.
TOLERANCE_M = 0.01


def placed_phases() -> list[tuple[str, str, dict, list[tuple[float, float]]]]:
    """(structure_id, phase_id, phase, world polygon) for every committed placed phase."""
    datum = json.loads((ROOT / "data" / "datum.json").read_text(encoding="utf-8"))
    out = []
    for path in sorted(STRUCTURES.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        for phase in record.get("phases") or []:
            position = phase.get("position") or {}
            polygon = (phase.get("footprint") or {}).get("polygon") or []
            if position.get("utm_e") is None or len(polygon) < 3:
                continue
            out.append((record["id"], phase["id"], phase, world_polygon(phase, datum)))
    return out


def measure() -> dict:
    """Every committed structure's deepest lap into any platted corridor."""
    datum = json.loads((ROOT / "data" / "datum.json").read_text(encoding="utf-8"))
    lanes = corridors()
    origin_e = float(datum["origin_utm_e"])
    origin_n = float(datum["origin_utm_n"])

    rows: dict[str, dict] = {}
    placed = placed_phases()
    for structure_id, phase_id, phase, polygon in placed:
        street, depth = intrusion(polygon, lanes)
        if street is None:
            continue
        cx = sum(p[0] for p in polygon) / len(polygon)
        cy = sum(p[1] for p in polygon) / len(polygon)
        position = phase["position"]
        anchor = (float(position["utm_e"]) - origin_e, float(position["utm_n"]) - origin_n)
        # Which corridors each point is in. A point at an intersection is in two, so both
        # are recorded rather than the first one a dict iteration happened to reach —
        # that ambiguity is why T-A7's four named cases have been quoted against two
        # different street names in two different write-ups.
        centroid_in = sorted(s for s, lane in lanes.items()
                             if point_in_polygon((cx, cy), lane["ring"]))
        anchor_in = sorted(s for s, lane in lanes.items()
                           if point_in_polygon(anchor, lane["ring"]))
        key = f"{structure_id}:{phase_id}"
        rows[key] = {
            "structure": structure_id,
            "phase": phase_id,
            "layer": layer_of(structure_id),
            "street": street,
            "depth_m": round(depth, PLACES),
            "centroid_in": centroid_in,
            "anchor_in": anchor_in,
            "position_confidence": position.get("confidence"),
        }
    return {
        "placed_phases": len(placed),
        "corridors": len(lanes),
        "lapping": rows,
    }


def _fmt_table(result: dict) -> str:
    rows = sorted(result["lapping"].values(), key=lambda r: -r["depth_m"])
    lines = [f"{'structure':<44}{'street':<14}{'depth m':>8}  {'centroid':<9}{'layer'}"]
    for r in rows:
        centroid = "IN" if r["centroid_in"] else "clear"
        lines.append(f"{r['structure']:<44}{r['street']:<14}{r['depth_m']:>8.2f}  "
                     f"{centroid:<9}{r['layer']}")
    return "\n".join(lines)


def _distribution(result: dict) -> str:
    rows = list(result["lapping"].values())
    by_street: dict[str, list[float]] = {}
    by_layer: dict[str, int] = {}
    for r in rows:
        by_street.setdefault(r["street"], []).append(r["depth_m"])
        by_layer[r["layer"]] = by_layer.get(r["layer"], 0) + 1
    lines = ["", "by street (deepest lap):"]
    for street, depths in sorted(by_street.items(), key=lambda kv: -max(kv[1])):
        lines.append(f"   {street:<14}{len(depths):>3} record(s)   "
                     f"deepest {max(depths):>6.2f} m   shallowest {min(depths):>5.2f} m")
    lines.append("")
    lines.append("by evidence layer:")
    for layer in ("research", "inferred_household", "reconstruction"):
        lines.append(f"   {layer:<22}{by_layer.get(layer, 0):>3}")
    centroid = sum(1 for r in rows if r["centroid_in"])
    anchor = sum(1 for r in rows if r["anchor_in"])
    lines += [
        "",
        f"{len(rows)} of {result['placed_phases']} placed phases lap a platted corridor.",
        f"{centroid} of them have their CENTROID in one (T-A7's test).",
        f"{anchor} of them have their authored POSITION POINT in one.",
    ]
    return "\n".join(lines)


def recentre() -> str:
    """K30(a)'s refuted counterfactual, kept as a command so it stays refuted.

    `docs/GLB-CONTRACT.md` puts a record's position at its footprint polygon's own origin,
    and 332 of the 333 committed footprints have local `(0, 0)` at a VERTEX. So a building
    derived to a street corner is drawn with a corner on that point and its body extending
    wherever the polygon and its rotation send it — which looks like the systematic cause
    of a building standing in a street, and which 20 of the 29 anchors standing on legal
    ground make look likelier still.

    It is not the cause. This re-measures every lapping footprint CENTRED on its own anchor
    and reports what that would do. Anything that reads this as a proposal has read it
    backwards: it is here so the next parcel does not have to re-derive the refutation.
    """
    datum = json.loads((ROOT / "data" / "datum.json").read_text(encoding="utf-8"))
    lanes = corridors()
    origin_e = float(datum["origin_utm_e"])
    origin_n = float(datum["origin_utm_n"])

    rows = []
    for structure_id, _phase_id, phase, polygon in placed_phases():
        street, depth = intrusion(polygon, lanes)
        if street is None:
            continue
        position = phase["position"]
        ax = float(position["utm_e"]) - origin_e
        ay = float(position["utm_n"]) - origin_n
        cx = sum(p[0] for p in polygon) / len(polygon)
        cy = sum(p[1] for p in polygon) / len(polygon)
        centred = [(p[0] - cx + ax, p[1] - cy + ay) for p in polygon]
        _, moved = intrusion(centred, lanes)
        rows.append((structure_id, street, depth, moved))

    cleared = [r for r in rows if r[3] <= 0]
    worse = [r for r in rows if r[3] > r[2] + TOLERANCE_M]
    better = [r for r in rows if r[3] > 0 and r[3] < r[2] - TOLERANCE_M]

    lines = [f"{'structure':<44}{'street':<14}{'as drawn':>9}{'centred':>9}{'':>3}"]
    for structure_id, street, depth, moved in sorted(rows, key=lambda r: r[3] - r[2]):
        mark = "" if abs(moved - depth) <= TOLERANCE_M else ("WORSE" if moved > depth else "")
        lines.append(f"{structure_id:<44}{street:<14}{depth:>9.2f}{moved:>9.2f}   {mark}")
    lines += [
        "",
        f"centring every footprint on its own anchor: {len(cleared)} clear the corridor, "
        f"{len(better)} get shallower, {len(worse)} get DEEPER.",
        "So the anchor convention is not the cause and recentring is not the fix "
        "(ROADMAP K30(a), finding 4).",
    ]
    if worse:
        top = max(worse, key=lambda r: r[3] - r[2])
        lines.append(f"Worst regression: {top[0]} {top[2]:.2f} -> {top[3]:.2f} m "
                     f"(+{top[3] - top[2]:.2f}).")
    return "\n".join(lines)


def _baseline() -> dict:
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def gate(quiet: bool = False) -> int:
    """The ratchet. A new intruder fails; a deeper one fails; a shallower one is a repair.

    Plus one ABSOLUTE assertion that is not a ratchet: no generated roof may lap a
    corridor at all. Every generator already refuses it through the same module, so the
    invariant is enforceable at zero today and any future breach is a regression rather
    than a debt.
    """
    result = measure()
    baseline = _baseline()
    committed = baseline["lapping"]
    failures: list[str] = []

    generated = sorted(k for k, r in result["lapping"].items() if r["layer"] != "research")
    if generated:
        failures.append(
            f"{len(generated)} generated roof(s) lap a platted corridor, which the "
            f"placement gate refuses by construction: {', '.join(generated[:6])}")

    for key, row in sorted(result["lapping"].items()):
        if key not in committed:
            failures.append(f"{key} newly laps {row['street']} by {row['depth_m']:.2f} m")
        elif row["depth_m"] > committed[key]["depth_m"] + TOLERANCE_M:
            failures.append(f"{key} laps {row['street']} deeper: "
                            f"{committed[key]['depth_m']:.2f} -> {row['depth_m']:.2f} m")
        elif row["street"] != committed[key]["street"]:
            failures.append(f"{key} now laps {row['street']}, "
                            f"was {committed[key]['street']}")

    repaired = sorted(set(committed) - set(result["lapping"]))
    shallower = sorted(k for k, r in result["lapping"].items()
                       if k in committed and r["depth_m"] < committed[k]["depth_m"] - TOLERANCE_M)

    if not quiet or failures:
        print(f"   {len(result['lapping'])} of {result['placed_phases']} placed phases lap "
              f"a platted corridor ({len(committed)} committed)")
        print(f"   generated roofs lapping a corridor: {len(generated)} (must be 0)")
    if repaired or shallower:
        print(f"   {len(repaired)} cleared and {len(shallower)} shallower than the "
              f"baseline — re-run with --write-baseline to bank the repair")
    for line in failures:
        print(f"   {line}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--by-street", action="store_true", help="the distribution only")
    parser.add_argument("--recentre", action="store_true",
                        help="K30(a)'s refuted counterfactual, kept so it stays refuted")
    parser.add_argument("--gate", action="store_true", help="the ratchet check.sh runs")
    parser.add_argument("--write-baseline", action="store_true",
                        help="rewrite the committed table — only to record a repair")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.gate:
        return gate(quiet=args.quiet)

    if args.recentre:
        print(recentre())
        return 0

    result = measure()

    if args.write_baseline:
        baseline = _baseline() if BASELINE.exists() else {}
        baseline["$note"] = (
            "ROADMAP K30(a). Every committed structure phase whose footprint laps a "
            "platted street corridor, with the depth in metres from the corridor's own "
            "edge. DERIVED — regenerate with tools/measure_corridor_intrusion.py "
            "--write-baseline, and only ever to record a repair. This file is a RATCHET: "
            "tools/check.sh fails on an intruder that is not here and on a listed one "
            "whose depth has grown. It is NOT an allowance — K30(b) owns the fix, and "
            "these are the numbers it takes as its baseline. Never move a documented "
            "building to make an entry smaller: a position with a source outranks a "
            "corridor this project derived.")
        baseline["measured"] = args.__dict__.get("measured") or "2026-08-16"
        baseline["placed_phases"] = result["placed_phases"]
        baseline["corridors"] = result["corridors"]
        baseline["lapping"] = result["lapping"]
        BASELINE.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
        print(f"   wrote {BASELINE.relative_to(ROOT)}: {len(result['lapping'])} record(s)")
        return 0

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    if not args.by_street:
        print(_fmt_table(result))
    print(_distribution(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
