#!/usr/bin/env python3
"""Generate the bounded, anonymous 60-roof North Division parcel.

The authored recipe fixes an aggregate mix and review layout, not sixty recovered
buildings.  Consequently every generated instance says, in machine-readable and
visitor-facing fields, that its presence, position and footprint are conjectural.

This generator intentionally uses only archetypes already implemented in the
repository.  H1 temporarily resolves through ``frame_dwelling`` while the larger
H2-H3 and I2 forms use generic rectangular ``frame_tavern`` massing; none of those
mappings claims that a boarding house was a tavern or a hall was an inn.
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRUCTURES = DATA / "structures"
INVENTORY_PATH = DATA / "reconstruction" / "1835_building_inventory.json"
RECIPE_PATH = DATA / "reconstruction" / "1835_north_division_initial_parcel.json"
SOURCE_ID = "owner_chicago_1835_reconstruction_spec_2026"
PHASE_ID = "inferred_1835"
PROGRAMME_PHASE = "phase2_north_division_initial"
PREFIX = "recon_1835_north_"

sys.path.insert(0, str(ROOT / "generators"))
sys.path.insert(0, str(ROOT / "tools"))

# Phase two of the inferred-residents programme adopts some of these anonymous roofs
# as the dwellings and shops of inferred households (docs/ROADMAP.md K1). The link is
# data, not a hand edit: this generator still re-derives every record byte for byte,
# and the occupancy block arrives from the household programme's ledger.
from inferred_occupancy import occupancy  # noqa: E402

OCCUPANCY = occupancy()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def inferred(value, reason: str):
    return {"value": value, "confidence": "inferred", "sources": [SOURCE_ID], "note": reason}


def archetype_for(family: str) -> str:
    if family == "D1":
        return "log_dwelling"
    if family.startswith("D") and family != "D2" or family == "H1":
        return "frame_dwelling"
    if family.startswith("C"):
        return "frame_storefront"
    if family.startswith("T") or family.startswith("I") or family in ("H2", "H3"):
        return "frame_tavern"
    return "outbuilding"


FUNCTIONS = {
    "D1": "older log dwelling", "D2": "rough plank dwelling or shanty",
    "D3": "one-room frame cottage", "D4": "two-room frame cottage",
    "D5": "deep-plan frame cottage", "D6": "one-and-a-half-story frame cottage",
    "D7": "small two-story frame house", "H1": "small boarding house",
    "H2": "medium boarding house", "H3": "large boarding house",
    "C1": "small shop or office", "C2": "store-residence",
    "T1": "small inn or tavern", "W1": "blacksmith shop",
    "W2": "carpenter or joiner shop", "W5": "large workshop",
    "F1": "freight or storage shed", "I2": "schoolhouse or meeting hall",
    "A1": "stable", "A2": "barn or carriage shed", "A3": "privy",
    "A4": "woodshed or storage shed", "A5": "small utility building",
}


def finish_for(seq: int) -> tuple[str, str]:
    # A deterministic sequence weighted toward unpainted material.  ``finish_key``
    # is the inventory vocabulary; the second value is the current archetypes'.
    keys = ("fresh_timber", "weathered_timber", "fresh_timber", "whitewash",
            "weathered_timber", "red_oxide", "ochre", "mixed_patch")
    key = keys[(seq * 5) % len(keys)]
    paint = {"whitewash": "whitewash", "red_oxide": "red"}.get(key, "unpainted")
    return key, paint


def form_for(family: str, seq: int, paint: str) -> dict:
    why = (f"Type-level choice within the {family} band in the supplied reconstruction "
           "specification; it is not evidence for this anonymous North Division instance.")
    frame = "balloon_frame" if seq % 2 else "braced_frame"

    if family == "D1":
        return {
            "stories": inferred(1, why), "wall_height_m": inferred(2.5, why),
            "roof_type": inferred("gable", why), "roof_pitch_deg": inferred(35.0, why),
            "construction": inferred("log", why), "loft": inferred(True, why),
            "chimneys": inferred(1, why),
        }

    if family.startswith("D") and family != "D2" or family == "H1":
        if family in ("D6", "H1"):
            stories, wall, pitch = 1.5, 3.6, 42.0
        elif family in ("D7", "H2", "H3"):
            stories, wall, pitch = 2, 5.05, 38.0
        else:
            stories, wall, pitch = 1, 2.78, 38.0
        plan = "centre_passage" if family in ("D7", "H2", "H3") else (
            "single_pen" if family == "D3" else "hall_parlour")
        return {
            "stories": inferred(stories, why), "wall_height_m": inferred(wall, why),
            "roof_type": inferred("gable", why), "roof_pitch_deg": inferred(pitch, why),
            "construction": inferred(frame, why), "plan": inferred(plan, why),
            "bays": inferred(5 if family in ("D7", "H2", "H3") else 3, why),
            "chimneys": inferred(2 if family.startswith("H") else 1, why),
            "paint": inferred(paint, why),
        }

    if family.startswith("C"):
        return {
            "stories": inferred(1, why), "wall_height_m": inferred(3.25, why),
            "roof_type": inferred("gable", why), "roof_pitch_deg": inferred(33.0, why),
            "gable_front": inferred(True, why), "construction": inferred(frame, why),
            "cladding": inferred("clapboard", why), "paint": inferred(paint, why),
            "loft": inferred(family == "C2", why), "chimneys": inferred(1, why),
            "shopfront": inferred(True, why), "goods_door": inferred(True, why),
            "goods_door_side": inferred("end", why),
        }

    if family.startswith("T") or family.startswith("I") or family in ("H2", "H3"):
        # The I2 school/meeting-hall is a flagged generic block until a dedicated
        # institutional archetype exists; the function and research note stay I2.
        return {
            "stories": inferred(1 if family == "I2" else 2, why),
            "wall_height_m": inferred(3.3 if family == "I2" else 5.2, why),
            "roof_type": inferred("gable", why), "roof_pitch_deg": inferred(38.0, why),
            "construction": inferred("braced_frame", why), "paint": inferred(paint, why),
            "gallery": inferred(False, why), "chimneys": inferred(1 if family == "I2" else 2, why),
        }

    door = "wagon" if family in ("W1", "W2", "W5", "F1", "A2") else (
        "stable" if family == "A1" else "man")
    roof = "shed" if family in ("D2", "A3", "A4", "A5") else "gable"
    wall = 3.42 if door == "wagon" else (2.75 if door == "stable" else 2.05)
    construction = "light_frame" if family in ("W2", "A1", "A2") else "plank"
    return {
        "wall_height_m": inferred(wall, why), "roof_type": inferred(roof, why),
        "roof_pitch_deg": inferred(18.0 if roof == "shed" else 32.0, why),
        "construction": inferred(construction, why), "door": inferred(door, why),
        "door_side": inferred("front", why),
        "loft": inferred(family in ("W2", "W5", "A1", "A2"), why),
        "board_gap_m": inferred(.012, why), "paint": inferred(paint, why),
    }


def footprint_origin(center_e: float, center_n: float, width: float, depth: float,
                     bearing: float) -> tuple[float, float]:
    """Convert the recipe's centre anchor to the GLB contract's (0, 0) corner."""
    theta = math.radians(bearing)
    cos, sin = math.cos(theta), math.sin(theta)
    return (center_e - width * .5 * cos - depth * .5 * sin,
            center_n + width * .5 * sin - depth * .5 * cos)


# Slot 41's authored centre crosses the steep east-fringe ridge: its perimeter
# spans 1.43 m of relief, four times the walker's step tolerance.  The anonymous
# placement has a 25 m review radius, so move its centre 7.1 m to nearby dry,
# coherent ground rather than emit another visible ground layer or bury the walls.
TERRAIN_ADJUSTMENTS = {41: (-5.0, 5.0)}


def make_record(row: list, datum: dict) -> dict:
    seq, suffix, center_e, center_n, family, inventory_class, width_ft, depth_ft, bearing, cluster, yard_group = row
    sid = f"{PREFIX}{suffix}"
    de, dn = TERRAIN_ADJUSTMENTS.get(seq, (0.0, 0.0))
    center_e, center_n = float(center_e) + de, float(center_n) + dn
    width, depth = round(float(width_ft) * .3048, 3), round(float(depth_ft) * .3048, 3)
    local_e, local_n = footprint_origin(center_e, center_n, width, depth, float(bearing))
    finish_key, paint = finish_for(seq)
    function = FUNCTIONS[family]
    adjusted = (f" Slot {seq} is shifted {math.hypot(de, dn):.1f} m within the recipe's "
                "25 m control radius so its entire perimeter meets one terrain surface."
                if de or dn else "")
    position_note = ("Interpretive placement within the reviewed North Division cluster. "
                     "The recipe coordinate is a production-layout control, not a recovered lot."
                     + adjusted)
    symbolic = (f"Anonymous inferred roof in North Division cluster {cluster}; "
                "between the north bank and Michigan Street")
    reconstruction = {
        "status": "inferred_anonymous", "family": family, "district": "north",
        "inventory_class": inventory_class, "programme_phase": PROGRAMME_PHASE,
        "source_id": SOURCE_ID, "sequence": int(seq), "finish_key": finish_key,
        "roof_condition": ("fresh", "darkened", "patched", "weathered")[seq % 4],
        "age_state": ("new", "recent", "established", "older_frontier")[seq % 4],
    }
    if yard_group:
        reconstruction["yard_group"] = yard_group
    mapping_note = (" H-family boarding-house massing currently uses a generic frame "
                    "dwelling/block archetype." if family.startswith("H") else
                    " I2 currently uses a generic rectangular frame block because no "
                    "institutional generator is implemented." if family == "I2" else "")
    return {
        "id": sid, "name": f"Inferred {family} {function} #{seq:03d}",
        "archetype": archetype_for(family),
        "phases": [{
            "id": PHASE_ID,
            "documented_range": {
                "from": "1835-01-01", "to": "1835-12-31", "confidence": "conjectural",
                "note": "Anonymous count-unit toward the July 1835 programme. No evidence establishes that this particular building existed."
            },
            "position": {
                "utm_e": round(float(datum["origin_utm_e"]) + local_e, 3),
                "utm_n": round(float(datum["origin_utm_n"]) + local_n, 3),
                "rotation_deg": float(bearing), "symbolic_location": symbolic,
                "confidence": "conjectural", "note": position_note,
                "derivation": {"method": "not_derivable", "reason": "No parcel-by-parcel July 1835 North Division roof register survives in the supplied evidence."}
            },
            "footprint": {
                "polygon": [[0, 0], [width, 0], [width, depth], [0, depth]],
                "confidence": "conjectural",
                "note": f"A {width_ft:g} × {depth_ft:g} ft rectangle assigned by the reconstruction recipe within the {family} family band; no individual dimensions are documented."
            },
            "form": form_for(family, int(seq), paint),
            "change_note": "Inferred anonymous July 1835 North Division infill; a better-evidenced named roof substitutes for a compatible count-unit rather than increasing the 665-roof total."
        }],
        "function": inferred(function, f"Assigned from the {family} family to satisfy the aggregate North Division mix; no occupant or individual use is known."),
        **({"occupants": OCCUPANCY[sid]} if sid in OCCUPANCY else {}),
        "reconstruction": reconstruction,
        "research_note": ("RECOMMENDED / GENERATED, NOT A DOCUMENTED NAMED BUILDING. "
                          "Aggregate mix follows the supplied specification; exact presence, "
                          "position, footprint, finish and instance-level form are interpretive."
                          + mapping_note),
        "review_required": False,
    }


def world_polygon(record: dict, datum: dict) -> list[tuple[float, float]]:
    phase = record["phases"][0]
    pos, poly = phase["position"], phase["footprint"]["polygon"]
    theta = math.radians(float(pos.get("rotation_deg", 0)))
    cos, sin = math.cos(theta), math.sin(theta)
    e0 = float(pos["utm_e"]) - float(datum["origin_utm_e"])
    n0 = float(pos["utm_n"]) - float(datum["origin_utm_n"])
    return [(e0 + u * cos + v * sin, n0 - u * sin + v * cos) for u, v in poly]


def polygons_overlap(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> bool:
    """Strict convex-polygon SAT; touching edges are permitted."""
    for poly in (a, b):
        for i, p in enumerate(poly):
            q = poly[(i + 1) % len(poly)]
            axis = (-(q[1] - p[1]), q[0] - p[0])
            pa = [x * axis[0] + y * axis[1] for x, y in a]
            pb = [x * axis[0] + y * axis[1] for x, y in b]
            if max(pa) <= min(pb) + .05 or max(pb) <= min(pa) + .05:
                return False
    return True


def validate(records: list[dict], inventory: dict, recipe: dict, datum: dict) -> None:
    expected = recipe["inventory"]
    classes = Counter(r["reconstruction"]["inventory_class"] for r in records)
    families = Counter(r["reconstruction"]["family"] for r in records)
    if len(records) != expected["roof_total"]:
        raise SystemExit(f"North recipe generated {len(records)} roofs, expected {expected['roof_total']}")
    if classes != Counter({"principal_functional": expected["principal_functional"],
                           "ancillary": expected["ancillary"]}):
        raise SystemExit(f"North inventory-class mix drifted: {dict(classes)}")
    if families != Counter(expected["family_totals"]):
        raise SystemExit(f"North family mix drifted: {dict(families)}")
    for family, count in families.items():
        if count > inventory["family_targets"][family]:
            raise SystemExit(f"North {family} count {count} exceeds programme target")

    # Every form must resolve through a currently implemented archetype.
    for record in records:
        module = importlib.import_module(f"archetypes.{record['archetype']}_params")
        module.from_phase(record["phases"][0])

    polygons = [(r["id"], world_polygon(r, datum)) for r in records]
    for i, (sid, poly) in enumerate(polygons):
        for other_sid, other in polygons[:i]:
            if polygons_overlap(poly, other):
                raise SystemExit(f"North recipe collision: {sid} overlaps {other_sid}")

    # Use the same committed surface the walker uses: every perimeter must be on
    # covered, dry ground and stay within its 0.35 m step-height contract.
    from heightfield import Heightfield  # noqa: PLC0415
    field = Heightfield.load(DATA / "terrain" / "epochs" / "e1834_harbor_cut")
    if field is None:
        raise SystemExit("North recipe cannot validate: committed heightfield is missing")
    for sid, poly in polygons:
        heights = [field.height(e, n) for e, n in poly]
        if not all(field.covers(e, n) for e, n in poly):
            raise SystemExit(f"{sid} falls outside modelled terrain")
        if min(heights) < -.10:
            raise SystemExit(f"{sid} intersects the authoritative water side of the terrain")
        if max(heights) - min(heights) > .35:
            raise SystemExit(f"{sid} spans {max(heights) - min(heights):.2f} m of relief; its walls would not share the walker surface")


def records_from_inputs() -> list[dict]:
    inventory, recipe, datum = load(INVENTORY_PATH), load(RECIPE_PATH), load(DATA / "datum.json")
    records = [make_record(row, datum) for row in recipe["placements"]]
    validate(records, inventory, recipe, datum)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report missing, changed, or extra North outputs")
    args = parser.parse_args()
    records = records_from_inputs()
    expected = {f"{r['id']}.json" for r in records}
    drift = []
    for record in records:
        path = STRUCTURES / f"{record['id']}.json"
        text = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists():
                drift.append(f"{path.relative_to(ROOT)} is missing")
            elif path.read_text(encoding="utf-8") != text:
                drift.append(f"{path.relative_to(ROOT)} has drifted from the North recipe")
        else:
            path.write_text(text, encoding="utf-8")
    extras = sorted(p.name for p in STRUCTURES.glob(f"{PREFIX}*.json") if p.name not in expected)
    drift.extend(f"data/structures/{name} is outside the bounded 60-roof parcel" for name in extras)
    if drift:
        print("NORTH INFILL DRIFT")
        for item in drift:
            print(f"  - {item}")
        return 1
    mode = "verified" if args.check else "generated"
    print(f"{mode} {len(records)} inferred anonymous North Division records (45 principal, 15 ancillary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
