#!/usr/bin/env python3
"""The one sampling rule: a family's authored band, and how an instance is drawn from it.

`data/reconstruction/1835_family_archetype_crosswalk.json` authors, per family, the
footprint band, the storey count, the eave band and the placeholder archetype. This
module is the single place that reads them and the single place that turns a band into
an instance's dimensions.

It exists because the same arithmetic was in two files and only one of them ran it.
`tools/generate_block_infill.py` samples inside the band, so its twelve blocks carry a
size distribution; `tools/generate_north_infill.py` retyped one value per family into
Python, so its sixty roofs were the same building sixty times (ROADMAP T-V1). Uniformity
is itself a claim and no source makes it, so the rule moved here and both parcels import
it rather than one of them owning it.

**Sampling adds variety, not knowledge.** Every value it returns is an invention bounded
by the family band; it grades at the bottom tier wherever it lands, exactly as the
constant it replaced did. What changes is that the band is now used as the range it was
authored as instead of being collapsed to a point.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generators"))
CROSSWALK_PATH = ROOT / "data" / "reconstruction" / "1835_family_archetype_crosswalk.json"

FOOTPRINT_RE = re.compile(r"^\s*(\d+)x(\d+)\s*-\s*(\d+)x(\d+)")
RANGE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")


def stable_fraction(key: str, slot: int) -> float:
    raw = hashlib.sha256(f"{key}:{slot}".encode()).digest()
    return int.from_bytes(raw[:4], "big") / 0xFFFFFFFF


def families() -> dict[str, dict]:
    """Per-family geometry and archetype, as the crosswalk authors them."""
    table: dict[str, dict] = {}
    for fam in json.loads(CROSSWALK_PATH.read_text(encoding="utf-8"))["families"]:
        geom = fam.get("key_geometry_parameters") or {}
        entry = {
            "label": fam.get("label"),
            "archetype": fam.get("current_placeholder_archetype"),
            "levels": geom.get("levels"),
            "eave_ft": geom.get("eave_ft"),
            "band_ft": None,
        }
        m = FOOTPRINT_RE.match(str(geom.get("footprint_ft") or ""))
        if m:
            entry["band_ft"] = [int(m.group(1)), int(m.group(2)),
                                int(m.group(3)), int(m.group(4))]
        table[fam["id"]] = entry
    return table


def dimensions_m(family: str, band_ft: list[int], key: str) -> tuple[float, float]:
    """A rectangle sampled deterministically inside the family's authored band.

    The sampling is the phase-one parcel's, unchanged, so the same family reads the
    same size distribution wherever it stands.
    """
    lo_w, lo_d, hi_w, hi_d = band_ft
    width_ft = lo_w + (hi_w - lo_w) * (.18 + .70 * stable_fraction(key, 1))
    depth_ft = lo_d + (hi_d - lo_d) * (.15 + .72 * stable_fraction(key, 2))
    width, depth = width_ft * .3048, depth_ft * .3048
    # The implemented frame dwelling is eaves-front. Families whose band reaches a
    # gable-front proportion are held inside the archetype that exists rather than
    # being drawn as something the generator cannot build.
    if family.startswith(("D", "H")) and family not in ("D1", "D2") and depth > width * 1.46:
        width = min(hi_w * .3048, depth / 1.46)
    return round(width, 3), round(depth, 3)


def storeys(levels: str) -> tuple[float, bool]:
    """(storeys, has a loft) from the crosswalk's `levels` string."""
    text = str(levels or "1").strip()
    loft = "loft" in text
    head = text.split("+")[0].strip()
    try:
        return float(head), loft
    except ValueError:
        raise SystemExit(f"cannot read a storey count from levels '{levels}'")


# A door has to fit under a wall, and two of the small ancillary families are authored
# with an eave band whose bottom is below the height the implemented outbuilding needs
# to carry its own man door plus a header — A3 runs 6-7 ft, and a sample at 1.891 m is
# refused by name. The band is not wrong: the phase-one parcel's privies stand at
# 2.05 m, which is 6.73 ft and inside it. Uniform sampling across the band is what is
# wrong. So the sample is taken from the part of the authored band the archetype can
# actually build, and a family whose whole band is below that floor fails loudly rather
# than being quietly raised out of its own typology.
DOOR_HEADROOM_M = 2.05


def wall_height_m(family: str, eave_ft: str, key: str, floor: float = 0.0) -> float:
    m = RANGE_RE.match(str(eave_ft or ""))
    if not m:
        raise SystemExit(f"{family}: eave height '{eave_ft}' is not a numeric band")
    lo, hi = float(m.group(1)) * .3048, float(m.group(2)) * .3048
    if floor > hi:
        raise SystemExit(f"{family}: the authored eave band {eave_ft} ft tops out at "
                         f"{hi:.2f} m, below the {floor:.2f} m its archetype needs to "
                         f"carry a door")
    lo = max(lo, floor)
    return round(lo + (hi - lo) * stable_fraction(key, 8), 3)


# Which families take a headroom floor at all. Only the door-carrying outbuilding
# families do; a house's eave band is far above it and clamping there would be
# inventing a storey height.
#
# HOW HIGH the floor is depends on WHICH DOOR, and that is not a constant. 2.05 m is
# the phase-one privies' height and carries a man door, but a wagon door is 3.00 m in
# the clear and the outbuilding archetype refuses a wall that cannot header it — which
# is how the North parcel's blacksmith shop failed the moment it started sampling its
# own band instead of standing at a retyped 3.42 m. So the floor is asked of the
# archetype's own door table rather than retyped here: retyping it is the fault this
# module exists to fix.
def eave_floor(family: str, door: str = "man") -> float:
    if not (family.startswith(("A", "W")) or family in ("D2", "F1")):
        return 0.0
    from archetypes.outbuilding_params import DOOR_SIZE_M  # noqa: PLC0415
    head = DOOR_SIZE_M.get(door, DOOR_SIZE_M["man"])[1]
    return max(DOOR_HEADROOM_M, round(head + DOOR_HEADER_M, 3))


# The stock over a door's clear opening, as the outbuilding archetype's own validator
# measures it: a wall must stand more than this above the door head.
DOOR_HEADER_M = 0.08
