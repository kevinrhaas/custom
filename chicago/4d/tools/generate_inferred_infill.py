#!/usr/bin/env python3
"""Generate the explicitly conjectural phase-one anonymous building parcel.

The authored inputs are the 665-roof ledger and the compact parcel recipe under
``data/reconstruction``.  The outputs are ordinary one-file-per-structure records,
so the existing schema, confidence, liberty, scene and terrain gates apply to them.

This tool deliberately does not make the parcel authoritative.  Every individual
presence, footprint and position is conjectural; only the aggregate family bands
and district programme are inferred from the owner-supplied specification.
"""

from __future__ import annotations

import argparse
import hashlib
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
PARCEL_PATH = DATA / "reconstruction" / "1835_phase1_south_mixed_blocks.json"
SOURCE_ID = "owner_chicago_1835_reconstruction_spec_2026"
PHASE_ID = "inferred_1835"
PREFIX = "recon_1835_south_"

sys.path.insert(0, str(ROOT / "generators"))


def load(path: Path):
    return json.loads(path.read_text())


def stable_fraction(key: str, slot: int) -> float:
    raw = hashlib.sha256(f"{key}:{slot}".encode()).digest()
    return int.from_bytes(raw[:4], "big") / 0xFFFFFFFF


def inferred(value, reason: str):
    return {
        "value": value,
        "confidence": "inferred",
        "sources": [SOURCE_ID],
        "note": reason,
    }


def finish_for(key: str) -> tuple[str, str]:
    # Weighted toward unpainted material, matching the specification's 55% target.
    bucket = stable_fraction(key, 9)
    if bucket < .34:
        return "fresh_timber", "unpainted"
    if bucket < .58:
        return "weathered_timber", "unpainted"
    if bucket < .75:
        return "whitewash", "whitewash"
    if bucket < .84:
        return "ochre", "unpainted"
    if bucket < .92:
        return "red_oxide", "red"
    return "mixed_patch", "unpainted"


def dimensions(family: str, seq: int, bands: dict[str, list[float]]) -> tuple[float, float]:
    lo_w, lo_d, hi_w, hi_d = bands[family]
    key = f"{family}:{seq}"
    width_ft = lo_w + (hi_w - lo_w) * (.18 + .70 * stable_fraction(key, 1))
    depth_ft = lo_d + (hi_d - lo_d) * (.15 + .72 * stable_fraction(key, 2))
    width, depth = width_ft * .3048, depth_ft * .3048
    # The current frame dwelling generator is eaves-front. D5/D6 can reach a
    # gable-front proportion at the edge of their bands, so keep this first parcel
    # inside the implemented family while the eventual D5/D6 archetypes are built.
    if family.startswith("D") and family not in ("D1", "D2") and depth > width * 1.46:
        width = min(hi_w * .3048, depth / 1.46)
    return round(width, 3), round(depth, 3)


def archetype_for(family: str) -> str:
    if family == "D1":
        return "log_dwelling"
    if family == "D2" or family.startswith(("W", "A")) or family == "F1":
        return "outbuilding"
    if family.startswith("D"):
        return "frame_dwelling"
    return "frame_storefront"


def function_for(family: str) -> str:
    return {
        "D1": "older log dwelling", "D2": "rough plank dwelling or shanty",
        "D3": "one-room frame cottage", "D4": "two-room frame cottage",
        "D5": "deep-plan frame cottage", "D6": "one-and-a-half-story frame cottage",
        "D7": "small two-story frame house", "C1": "small shop or office",
        "C2": "store-residence", "C3": "narrow two-story store",
        "W1": "blacksmith shop", "W2": "carpenter or joiner shop",
        "W3": "cooper, wagon, or wheelwright shop", "W4": "small artisan shop",
        "F1": "freight or storage shed", "F2": "narrow two-story warehouse",
        "A1": "stable", "A2": "barn or carriage shed", "A3": "privy",
        "A4": "woodshed or storage shed", "A5": "small utility building",
    }[family]


def form_for(family: str, seq: int, finish: str, width: float, depth: float) -> dict:
    why = (f"Type-level choice within the {family} band in the 2026 reconstruction "
           "specification; it is not evidence for this anonymous instance.")
    construction = "balloon_frame" if stable_fraction(f"{family}:{seq}", 6) < .52 else "braced_frame"

    if family == "D1":
        return {
            "stories": inferred(1, why), "wall_height_m": inferred(2.62, why),
            "roof_type": inferred("gable", why), "roof_pitch_deg": inferred(38.0, why),
            "construction": inferred("log", why), "loft": inferred(True, why),
            "chimneys": inferred(1, why),
        }

    if family.startswith("D") and family != "D2":
        stories = 1.5 if family == "D6" else (2 if family == "D7" else 1)
        wall = 3.6 if family == "D6" else (5.05 if family == "D7" else 2.78)
        bays = 5 if family == "D7" else (3 if width >= 5.4 else 2)
        plan = "centre_passage" if family == "D7" else ("single_pen" if family == "D3" else "hall_parlour")
        result = {
            "stories": inferred(stories, why), "wall_height_m": inferred(wall, why),
            "roof_type": inferred("gable", why),
            "roof_pitch_deg": inferred(44.0 if family == "D6" else 38.0, why),
            "construction": inferred(construction, why), "plan": inferred(plan, why),
            "bays": inferred(bays, why), "chimneys": inferred(1, why),
            "paint": inferred(finish, why),
        }
        if stable_fraction(f"{family}:{seq}", 7) < .58:
            result["porch"] = inferred("stoop", why)
        return result

    if family.startswith(("C", "F")) and family != "F1":
        stories = 2 if family in ("C3", "F2") else 1
        return {
            "stories": inferred(stories, why),
            "wall_height_m": inferred(5.35 if stories == 2 else 3.25, why),
            "roof_type": inferred("gable", why), "roof_pitch_deg": inferred(34.0, why),
            "gable_front": inferred(family in ("C1", "C2", "C3"), why),
            "construction": inferred(construction, why),
            "cladding": inferred("clapboard" if family != "F2" else "vertical_board", why),
            "paint": inferred(finish, why), "loft": inferred(family == "C2", why),
            "chimneys": inferred(1 if not family.startswith("F") else 0, why),
            "shopfront": inferred(not family.startswith("F"), why),
            "goods_door": inferred(True, why), "goods_door_side": inferred("end", why),
        }

    door = "man"
    if family in ("W1", "W3", "F1", "A2"):
        door = "wagon"
    elif family in ("W2", "A1"):
        door = "stable"
    roof = "shed" if family in ("D2", "A3", "A4") else "gable"
    wall = 2.05 if family == "A3" else (3.42 if door == "wagon" else 2.75)
    material = "plank"
    if family == "A1" and min(width, depth) >= 2.2:
        material = "log"
    elif family in ("A2", "W2"):
        material = "light_frame"
    return {
        "wall_height_m": inferred(wall, why), "roof_type": inferred(roof, why),
        "roof_pitch_deg": inferred(18.0 if roof == "shed" else 32.0, why),
        "construction": inferred(material, why), "door": inferred(door, why),
        "door_side": inferred("front", why),
        "loft": inferred(family in ("W2", "A1", "A2"), why),
        "board_gap_m": inferred(.012, why), "paint": inferred(finish, why),
    }


def block_name(e: float) -> str:
    if e < 330: return "Franklin and Wells"
    if e < 450: return "Wells and LaSalle"
    if e < 575: return "LaSalle and Clark"
    if e < 700: return "Clark and Dearborn"
    return "Dearborn and State"


def make_record(seq: int, family: str, e: float, n: float, row: dict,
                inventory: dict, datum: dict) -> dict:
    sid = f"{PREFIX}{family.lower()}_{seq:03d}"
    width, depth = dimensions(family, seq, inventory["family_bands_ft"])
    jitter_e = (stable_fraction(sid, 3) - .5) * 1.2
    jitter_n = (stable_fraction(sid, 4) - .5) * 1.5
    rotation = round((stable_fraction(sid, 5) - .5) * 2.8, 2)
    local_e, local_n = round(e + jitter_e, 3), round(n + jitter_n, 3)
    finish_key, finish = finish_for(sid)
    ancillary = family.startswith("A")
    yard_group = row.get("yard_group")
    reconstruction = {
        "status": "inferred_anonymous", "family": family, "district": "south",
        "inventory_class": "ancillary" if ancillary else "principal_functional",
        "programme_phase": "phase1_south_mixed_blocks", "source_id": SOURCE_ID,
        "sequence": seq, "finish_key": finish_key,
        "roof_condition": ("fresh", "darkened", "patched", "weathered")[seq % 4],
        "age_state": ("new", "recent", "established", "older_frontier")[seq % 4],
    }
    if yard_group:
        reconstruction["yard_group"] = yard_group

    blocks = block_name(local_e)
    location = f"Anonymous inferred roof in the South Division block between {blocks}, south of Lake Street"
    function = function_for(family)
    return {
        "id": sid,
        "name": f"Inferred {family} {function} #{seq:03d}",
        "archetype": archetype_for(family),
        "phases": [{
            "id": PHASE_ID,
            "documented_range": {
                "from": "1835-01-01", "to": "1835-12-31", "confidence": "conjectural",
                "note": "This is an anonymous count-unit created to begin the July 1835 aggregate roof target. No evidence establishes that this particular building existed."
            },
            "position": {
                "utm_e": round(datum["origin_utm_e"] + local_e, 3),
                "utm_n": round(datum["origin_utm_n"] + local_n, 3),
                "rotation_deg": rotation, "symbolic_location": location,
                "confidence": "conjectural",
                "note": "Interpretive lot placement inside a measured street grid. It preserves mixed-block spacing and open lots but is not a recovered parcel position.",
                "derivation": {"method": "not_derivable", "reason": "No parcel-by-parcel July 1835 roof register survives in the supplied evidence."}
            },
            "footprint": {
                "polygon": [[0, 0], [width, 0], [width, depth], [0, depth]],
                "confidence": "conjectural",
                "note": f"A {width:.2f} × {depth:.2f} m rectangle sampled deterministically inside the {family} family band; no individual dimensions are documented."
            },
            "form": form_for(family, seq, finish, width, depth),
            "change_note": "Inferred anonymous July 1835 infill. It may later be replaced by a named, better-evidenced roof through an explicit inventory substitution."
        }],
        "function": inferred(function, f"Assigned from the {family} production family to satisfy the aggregate South Division mix; no occupant or individual use is known."),
        "reconstruction": reconstruction,
        "research_note": "RECOMMENDED / GENERATED, NOT A DOCUMENTED NAMED BUILDING. Family and aggregate district role follow the owner-supplied 2026 specification; exact presence, location, footprint, finish and instance-level form are interpretive.",
        "review_required": False
    }


def validate_programme(inventory: dict, parcel: dict, records: list[dict]) -> None:
    if sum(inventory["family_targets"].values()) != inventory["targets"]["roof_total"]:
        raise SystemExit("family targets do not sum to the 665-roof target")
    matrix_total = sum(v["total"] for v in inventory["district_group_matrix"].values())
    if matrix_total != inventory["targets"]["roof_total"]:
        raise SystemExit("district/group matrix does not sum to the 665-roof target")
    for district, row in inventory["districts"].items():
        total = sum(v[district] for v in inventory["district_group_matrix"].values())
        if total != row["target"]:
            raise SystemExit(f"{district} matrix column is {total}, expected {row['target']}")
    principal = sum(1 for r in records if r["reconstruction"]["inventory_class"] == "principal_functional")
    ancillary = len(records) - principal
    if (len(records), principal, ancillary) != (48, parcel["principal_functional"], parcel["ancillary"]):
        raise SystemExit(f"phase-one parcel counts are {(len(records), principal, ancillary)}, expected (48, 40, 8)")
    counts = Counter(r["reconstruction"]["family"] for r in records)
    for family, count in counts.items():
        if count > inventory["family_targets"][family]:
            raise SystemExit(f"phase-one {family} count {count} exceeds programme target")

    # Prove each record resolves through the current archetype before it is written.
    for rec in records:
        module = importlib.import_module(f"archetypes.{rec['archetype']}_params")
        module.from_phase(rec["phases"][0])


def records_from_inputs() -> list[dict]:
    inventory, parcel, datum = load(INVENTORY_PATH), load(PARCEL_PATH), load(DATA / "datum.json")
    records = []
    for row in parcel["rows"]:
        for e, family in row["placements"]:
            records.append(make_record(len(records) + 1, family, float(e), float(row["local_n"]), row, inventory, datum))
    validate_programme(inventory, parcel, records)
    return records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    records = records_from_inputs()
    drift = []
    for rec in records:
        path = STRUCTURES / f"{rec['id']}.json"
        text = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists():
                drift.append(f"{path.relative_to(ROOT)} is missing")
            elif path.read_text() != text:
                drift.append(f"{path.relative_to(ROOT)} has drifted from the parcel recipe")
        else:
            path.write_text(text)
    if drift:
        print("INFERRED INFILL DRIFT")
        for item in drift:
            print(f"  - {item}")
        return 1
    mode = "verified" if args.check else "generated"
    print(f"{mode} {len(records)} inferred anonymous South Division records (40 principal, 8 ancillary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
