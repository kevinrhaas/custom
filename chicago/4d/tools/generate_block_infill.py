#!/usr/bin/env python3
"""Generate one platted block of anonymous infill from the 665-roof schedule.

ROADMAP T-A2 onward. The three parcels before this one — phase-one South, the West
approaches, the North Division cluster — each authored their own coordinates: a row
northing and a list of eastings, or a centre per slot. That was the only thing
available before the plat module existed. It does not survive the module: the block
and lot grid (`tools/generate_plat_lots.py`, ROADMAP K7) knows where the lots are, and
a recipe that retypes coordinates beside it is a second opinion about the same ground.
The K7 slice found seven buildings standing in the road for exactly that reason.

So this generator authors NO coordinates. The recipe says which family stands on which
lot and whether it fronts the street or the alley; every metre comes from the committed
lot polygon. That is also what makes the parcel shape repeat (T-A3…T-An): the next block
is a recipe entry, not a new geometry argument.

**Family geometry comes from the crosswalk, not from this file.**
`data/reconstruction/1835_family_archetype_crosswalk.json` already carries, per family,
the footprint band, the storey count, the eave height and the placeholder archetype it
resolves through. The earlier generators retyped some of that into Python and could only
build the families somebody had retyped — which is why `family_bands_ft` in the building
inventory has no H1 or H2 band at all, while the schedule apportions H1 and H2 to this
very block. Read where the numbers are authored and every family the programme can name
becomes buildable. The crosswalk agrees with `family_bands_ft` on all 21 families both
of them carry; it also covers the 14 they do not.

Every record this writes is an invention: an anonymous count-unit toward a documented
aggregate. Presence, position, footprint and every form value grade at the bottom tier
with a reasoning note, and no lot is numbered — this project has never read Thompson's
numbering off a sheet, and standing on a generated lot is not standing on a recovered one.
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRUCTURES = DATA / "structures"
RECIPE_PATH = DATA / "reconstruction" / "1835_platted_block_parcels.json"
CROSSWALK_PATH = DATA / "reconstruction" / "1835_family_archetype_crosswalk.json"
INVENTORY_PATH = DATA / "reconstruction" / "1835_building_inventory.json"
LOTS_PATH = DATA / "traces" / "vectors" / "thompson_lots.json"
SOURCE_ID = "owner_chicago_1835_reconstruction_spec_2026"
PHASE_ID = "inferred_1835"
PREFIX = "recon_1835_blk_"

sys.path.insert(0, str(ROOT / "generators"))
sys.path.insert(0, str(ROOT / "tools"))

# An adopted roof's `occupants` block is authored ONCE, in the household programme's
# ledger, and handed to whichever generator owns the roof — the arrangement the three
# earlier anonymous parcels already use. Writing the adoption here as well would put it
# in two places and let them disagree, and hand-editing a generated record would fail
# the drift check that makes these parcels trustworthy in the first place.
from inferred_occupancy import occupancy  # noqa: E402

OCCUPANCY = occupancy()

# The same separation the household parcel enforces. A generated building that lands
# three metres from another one is not a dense town, it is two records occupying one
# yard, and nothing downstream can tell them apart.
MIN_SEPARATION_M = 3.0
# A footprint must clear its own lot line by this much. Side lot lines are conjectural
# (K7: four lots to a face is a reading of ONE block), so a wall ON one would be
# asserting a line the grid does not have.
LOT_MARGIN_M = 1.5
# The walker's step tolerance, from the household parcel's placement gate.
MAX_RELIEF_M = 0.30


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def stable_fraction(key: str, slot: int) -> float:
    import hashlib
    raw = hashlib.sha256(f"{key}:{slot}".encode()).digest()
    return int.from_bytes(raw[:4], "big") / 0xFFFFFFFF


INVENTED_NOTE = (
    "INVENTED, NOT DERIVED. This value comes from a typology in the reconstruction "
    "spec — what a building of this kind was ordinarily like — and NOT from evidence "
    "about this particular building, because there is no particular building: the "
    "structure itself is an invention filling a demonstrable need of the town. The "
    "spec is cited because the invention is bounded by it, which is what makes it "
    "defensible rather than arbitrary; the GRADE is the bottom tier because nothing "
    "here is a reading of a source about this thing. "
)


def invented(value, reason: str) -> dict:
    return {"value": value, "confidence": "reconstructed", "sources": [SOURCE_ID],
            "note": INVENTED_NOTE + reason}


# --------------------------------------------------------------------------
# the family table, read from the crosswalk
# --------------------------------------------------------------------------

FOOTPRINT_RE = re.compile(r"^\s*(\d+)x(\d+)\s*-\s*(\d+)x(\d+)")
RANGE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")


def families() -> dict[str, dict]:
    """Per-family geometry and archetype, as the crosswalk authors them."""
    table: dict[str, dict] = {}
    for fam in load(CROSSWALK_PATH)["families"]:
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


# --------------------------------------------------------------------------
# the families this generator refuses to mass, and why each one
# --------------------------------------------------------------------------
#
# A family with no form rule is ordinarily a gap: somebody adds the rule and the
# next recipe uses it. The three institutional families are NOT that, and the
# generic message ("add one before a recipe uses it") is the wrong instruction for
# them, because each carries a precondition the crosswalk already wrote down and
# adding a form rule would step straight over it. They are refused by name, with
# the precondition quoted, so a parcel that meets one of these slots has to defer
# it and say so rather than reach for a shape.
#
# The distinction that makes this more than caution: an anonymous DWELLING is the
# ordinary case in a town of 3,000 whose householders were never enumerated
# roof by roof. An anonymous PUBLIC building is a different claim — that an
# institution stood here and left no record at all — and 1835 Chicago's public
# buildings are few enough to be nameable.
REFUSED_FAMILIES = {
    "I1": (
        "worship or meeting buildings. The crosswalk schedules four of them and says "
        "the schedule 'explicitly calls for four custom assets' which the placeholder "
        "'must not genericize'. Each is a named congregation with its own dossier, so "
        "an anonymous one is not a count-unit toward them — it is a fifth."
    ),
    "I2": (
        "schools and community-use structures. The crosswalk gives the family two "
        "roofs and says each 'needs named-record reconciliation'. (One anonymous I2 "
        "stands in the North Division from an earlier parcel, written before this rule "
        "and before this generator existed; it is recorded in docs/LIBERTIES.md rather "
        "than quietly removed, and it is not a precedent this generator extends.)"
    ),
    "I3": (
        "civic or public-service structures. The family resolves through the "
        "fort_structure placeholder, whose whole vocabulary of building kinds is "
        "garrison words — quarters, barracks, blockhouse, magazine, store, guard, "
        "sutler, artillery — and none of them names the adapted office or the engine "
        "house the crosswalk says this family spans. Massing an anonymous town civic "
        "building through it would stand a garrison building in the middle of the "
        "platted town. The crosswalk states the precondition itself: the six-roof "
        "aggregate 'spans unlike functions; they must reconcile to named public "
        "records before selecting construction'."
    ),
}


FUNCTIONS = {
    "D1": "older log dwelling", "D2": "rough plank dwelling or shanty",
    "D3": "one-room frame cottage", "D4": "two-room frame cottage",
    "D5": "deep-plan frame cottage", "D6": "one-and-a-half-story frame cottage",
    "D7": "small two-story frame house",
    "H1": "larger one-and-a-half-story house", "H2": "merchant or professional house",
    "C1": "small shop or office", "C2": "store-residence",
    "C3": "narrow two-story store",
    "W1": "blacksmith shop", "W2": "carpenter or joiner shop",
    "W3": "cooper, wagon, or wheelwright shop", "W4": "small artisan shop",
    "F1": "freight or storage shed", "F2": "narrow two-story warehouse",
    "A1": "stable", "A2": "barn or carriage shed", "A3": "privy",
    "A4": "woodshed or storage shed", "A5": "small utility building",
}


def finish_for(key: str) -> tuple[str, str]:
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


def form_for(family: str, spec: dict, key: str, width: float, paint: str) -> dict:
    """Form values, with the storey count and eave height read off the crosswalk."""
    why = (f"Type-level choice within the {family} band in the supplied reconstruction "
           "specification; it is not evidence for this anonymous instance.")
    levels, loft = storeys(spec["levels"])
    construction = "balloon_frame" if stable_fraction(key, 6) < .52 else "braced_frame"
    # Only the door-carrying outbuilding families take the headroom floor; a house's
    # eave band is far above it and clamping there would be inventing a storey height.
    floor = DOOR_HEADROOM_M if family.startswith(("A", "W")) or family in ("D2", "F1") else 0.0
    wall = wall_height_m(family, spec["eave_ft"], key, floor)

    if family == "D1":
        return {
            "stories": invented(1, why), "wall_height_m": invented(wall, why),
            "roof_type": invented("gable", why), "roof_pitch_deg": invented(38.0, why),
            "construction": invented("log", why), "loft": invented(True, why),
            "chimneys": invented(1, why),
        }

    if family.startswith(("D", "H")) and family != "D2":
        big = family in ("D7", "H2")
        plan = "centre_passage" if big else ("single_pen" if family == "D3" else "hall_parlour")
        result = {
            "stories": invented(levels, why), "wall_height_m": invented(wall, why),
            "roof_type": invented("gable", why),
            "roof_pitch_deg": invented(44.0 if levels == 1.5 else 38.0, why),
            "construction": invented(construction, why), "plan": invented(plan, why),
            "bays": invented(5 if big else (3 if width >= 5.4 else 2), why),
            "chimneys": invented(2 if big else 1, why),
            "paint": invented(paint, why),
        }
        if stable_fraction(key, 7) < .58:
            result["porch"] = invented("stoop", why)
        return result

    if family.startswith(("C", "F")) and family != "F1":
        return {
            "stories": invented(levels, why), "wall_height_m": invented(wall, why),
            "roof_type": invented("gable", why), "roof_pitch_deg": invented(34.0, why),
            "gable_front": invented(family.startswith("C"), why),
            "construction": invented(construction, why),
            "cladding": invented("clapboard" if family != "F2" else "vertical_board", why),
            "paint": invented(paint, why), "loft": invented(family == "C2", why),
            "chimneys": invented(1 if not family.startswith("F") else 0, why),
            "shopfront": invented(not family.startswith("F"), why),
            "goods_door": invented(True, why), "goods_door_side": invented("end", why),
        }

    if not family.startswith(("A", "W")) and family != "D2" and family != "F1":
        raise SystemExit(f"{family} has no form rule in this generator; add one before "
                         f"a recipe uses it")

    door = "man"
    if family in ("W1", "W3", "F1", "A2"):
        door = "wagon"
    elif family in ("W2", "A1"):
        door = "stable"
    roof = "shed" if family in ("D2", "A3", "A4") else "gable"
    material = "plank"
    if family == "A1":
        material = "log"
    elif family in ("A2", "W2"):
        material = "light_frame"
    return {
        "wall_height_m": invented(wall, why), "roof_type": invented(roof, why),
        "roof_pitch_deg": invented(18.0 if roof == "shed" else 32.0, why),
        "construction": invented(material, why), "door": invented(door, why),
        "door_side": invented("front", why), "loft": invented(loft, why),
        "board_gap_m": invented(.012, why), "paint": invented(paint, why),
    }


# --------------------------------------------------------------------------
# geometry, entirely from the committed lot polygons
# --------------------------------------------------------------------------

def _mid(a, b):
    return ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)


def lot_frame(lot: dict, alley: list[tuple[float, float]]) -> dict:
    """The lot's street edge, its alley edge and the axes a building stands on.

    Which edge fronts the street is asked of the geometry rather than of the vertex
    order, because the lot polygons do not wind consistently: on the first block the
    north tier listed its street edge first and the south tier listed its alley edge
    first.

    **The rear edge is the one nearest the alley STRIP, not the alley's centroid,
    and the second block is what proved the difference matters.** A block's alley
    centroid sits at the block's own centre, so for an END lot the side lot line
    running back toward that centre is very nearly as close to it as the lot's alley
    edge is: on `blk_randolph_dearborn` the two came out 38.93 m and 38.95 m apart —
    two centimetres over a thirty-nine metre lever — and two of that block's four end
    lots picked the side lot line. A building framed off a side line stands broadside
    to its own street and hangs over the neighbouring lot; the margin gate caught it
    at 1.44 m against a 1.5 m bound, which is a millimetre-scale complaint about a
    ninety-degree error. Measuring to the strip separates the same two edges by
    0.2 m and 26.3 m. `blk_randolph_wells` cleared the centroid tie by 1.3 m in 37 —
    a 3 % margin — so nothing it committed moves, but it was never more than the
    block's proportions away from the same failure.
    """
    poly = [tuple(p) for p in lot["polygon"]]
    edges = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    rear = min(edges, key=lambda e: distance_to_edges(_mid(*e), alley))
    rm = _mid(*rear)
    front = max(edges, key=lambda e: math.dist(_mid(*e), rm))
    fm = _mid(*front)
    # Front and rear are the two block-face-parallel edges of the same lot, so they
    # are the same length to within the plat's own skew. A side lot line is twice
    # that on these blocks, which makes this a cheap structural check on the choice
    # above rather than a tolerance anybody has to tune.
    front_len, rear_len = math.dist(*front), math.dist(*rear)
    if abs(front_len - rear_len) > .20 * max(front_len, rear_len):
        raise SystemExit(f"lot frame is not square to the block: a {front_len:.1f} m "
                         f"frontage against a {rear_len:.1f} m rear edge — one of them "
                         f"is a side lot line")
    span = math.dist(fm, rm)
    if span <= 0:
        raise SystemExit("degenerate lot polygon")
    inward = ((rm[0] - fm[0]) / span, (rm[1] - fm[1]) / span)
    return {
        "front_mid": fm, "rear_mid": rm, "depth_m": span,
        "front_len_m": math.dist(*front), "rear_len_m": math.dist(*rear),
        "inward": inward, "polygon": poly,
    }


def place(edge_mid: tuple[float, float], inward: tuple[float, float],
          setback: float, lateral: float, width: float,
          depth: float) -> tuple[float, float, float]:
    """(local_e, local_n, bearing) for a building standing off one lot edge.

    `inward` points from the edge into the lot, so the facade faces out of it — the
    street for a frontage building, the alley for a yard one. The returned coordinate
    is the footprint's (0, 0) corner, which is what the GLB contract anchors on.
    """
    bearing = math.degrees(math.atan2(inward[0], inward[1])) % 360.0
    # local +x, the frontage axis: `inward` turned 90 degrees clockwise.
    axis = (inward[1], -inward[0])
    cx = edge_mid[0] + inward[0] * (setback + depth / 2.0) + axis[0] * lateral
    cy = edge_mid[1] + inward[1] * (setback + depth / 2.0) + axis[1] * lateral
    theta = math.radians(bearing)
    cos, sin = math.cos(theta), math.sin(theta)
    return (cx - width * .5 * cos - depth * .5 * sin,
            cy + width * .5 * sin - depth * .5 * cos,
            round(bearing, 2))


def world_polygon(record: dict, datum: dict) -> list[tuple[float, float]]:
    phase = record["phases"][0]
    pos, poly = phase["position"], phase["footprint"]["polygon"]
    theta = math.radians(float(pos.get("rotation_deg") or 0))
    cos, sin = math.cos(theta), math.sin(theta)
    e0 = float(pos["utm_e"]) - float(datum["origin_utm_e"])
    n0 = float(pos["utm_n"]) - float(datum["origin_utm_n"])
    return [(e0 + u * cos + v * sin, n0 - u * sin + v * cos) for u, v in poly]


def point_in_polygon(pt: tuple[float, float], poly: list[tuple[float, float]]) -> bool:
    e, n = pt
    inside = False
    for i in range(len(poly)):
        e1, n1 = poly[i]
        e2, n2 = poly[(i + 1) % len(poly)]
        if (n1 > n) != (n2 > n):
            x = e1 + (n - n1) * (e2 - e1) / (n2 - n1)
            if x > e:
                inside = not inside
    return inside


def distance_to_edges(pt: tuple[float, float], poly: list[tuple[float, float]]) -> float:
    best = float("inf")
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        vx, vy = b[0] - a[0], b[1] - a[1]
        span = vx * vx + vy * vy
        t = 0.0 if span == 0 else max(0.0, min(1.0, ((pt[0] - a[0]) * vx + (pt[1] - a[1]) * vy) / span))
        best = min(best, math.dist(pt, (a[0] + t * vx, a[1] + t * vy)))
    return best


def polygon_gap(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> float:
    """Nearest approach between two convex-ish footprints; 0 if they overlap."""
    for pt in a:
        if point_in_polygon(pt, b):
            return 0.0
    for pt in b:
        if point_in_polygon(pt, a):
            return 0.0
    return min(min(distance_to_edges(pt, b) for pt in a),
               min(distance_to_edges(pt, a) for pt in b))


# --------------------------------------------------------------------------
# records
# --------------------------------------------------------------------------

def make_record(block: dict, slot: dict, lot_index: int, frame: dict,
                spec: dict, family: str, datum: dict, seq: int) -> dict:
    sid = f"{PREFIX}{block['block_id'].removeprefix('blk_')}_{family.lower()}_{seq:02d}"
    if spec["band_ft"] is None:
        raise SystemExit(f"{family} has no numeric footprint band in the crosswalk")
    width, depth = dimensions_m(family, spec["band_ft"], sid)

    fronts_alley = slot["stands_on"] == "alley"
    edge_mid = frame["rear_mid"] if fronts_alley else frame["front_mid"]
    inward = ((-frame["inward"][0], -frame["inward"][1]) if fronts_alley
              else frame["inward"])
    setback = float(slot["setback_m"])
    lateral = float(slot.get("lateral_m") or 0.0)
    local_e, local_n, bearing = place(edge_mid, inward, setback, lateral, width, depth)

    finish_key, paint = finish_for(sid)
    function = FUNCTIONS.get(family) or (spec["label"] or family).lower()
    ancillary = slot["inventory_class"] == "ancillary"
    bounded = block["bounded_by"]
    faces = bounded["south"] if fronts_alley else slot["fronts"]
    # The division is the block's own, not this generator's. Both blocks before
    # `blk_randolph_clinton` were South Division, so a literal "South Division" here
    # read correctly on every record that existed and would have written the wrong
    # division into the visitor-facing location line of the first West one.
    where = (f"Anonymous inferred roof in the {block['district'].title()} Division "
             f"block bounded by "
             f"{bounded['north'].replace('_', ' ').title()}, "
             f"{bounded['east'].replace('_', ' ').title()}, "
             f"{bounded['south'].replace('_', ' ').title()} and "
             f"{bounded['west'].replace('_', ' ').title()}")
    where += (f"; a yard building off the block alley behind the {slot['fronts'].title()} "
              "Street frontage" if fronts_alley
              else f"; standing back from the {faces.title()} Street frontage")

    position_note = (
        "Interpretive placement on a GENERATED lot, not a recovered parcel. The lot "
        "geometry is the K7 plat module's — this project has never read Thompson's "
        "numbering off a sheet, and the side lot lines and the alley are conjectural "
        f"even where the block face is not. The building stands {setback:.1f} m back "
        f"from its {'alley' if fronts_alley else 'street'} edge, which is a typology "
        "for the period and not a measurement of this lot. The whole footprint — not "
        "its centre — is tested against the platted street corridors, against its own "
        "lot lines and against every other footprint in the dataset, so no invented "
        "building of this parcel stands in the roadway; clearing the roadway is not "
        "the same as standing on a recovered lot.")

    reconstruction = {
        "status": "inferred_anonymous", "family": family, "district": block["district"],
        "inventory_class": slot["inventory_class"],
        "programme_phase": block["programme_phase"], "source_id": SOURCE_ID,
        "block_id": block["block_id"], "lot_index": lot_index,
        "stands_on": slot["stands_on"], "fronts": slot["fronts"],
        "sequence": seq, "finish_key": finish_key,
        "roof_condition": ("fresh", "darkened", "patched", "weathered")[seq % 4],
        "age_state": ("new", "recent", "established", "older_frontier")[seq % 4],
    }
    mapping = (" H-family house massing currently resolves through the frame dwelling "
               "archetype; no larger house generator is implemented."
               if family.startswith("H") else "")
    return {
        "id": sid,
        "name": f"Inferred {family} {function} #{seq:02d}",
        "archetype": spec["archetype"],
        "phases": [{
            "id": PHASE_ID,
            "documented_range": {
                "from": "1835-01-01", "to": "1835-12-31", "confidence": "reconstructed",
                "note": "Anonymous count-unit toward the July 1835 665-roof programme. No evidence establishes that this particular building existed, and no source names an occupant of this lot."
            },
            "position": {
                "utm_e": round(float(datum["origin_utm_e"]) + local_e, 3),
                "utm_n": round(float(datum["origin_utm_n"]) + local_n, 3),
                "rotation_deg": bearing, "symbolic_location": where,
                "confidence": "reconstructed", "note": position_note,
                "derivation": {"method": "not_derivable", "reason": "No parcel-by-parcel July 1835 roof register survives in the supplied evidence, and no lot in this block is numbered."}
            },
            "footprint": {
                "polygon": [[0, 0], [width, 0], [width, depth], [0, depth]],
                "confidence": "reconstructed",
                "note": f"A {width:.2f} × {depth:.2f} m rectangle sampled deterministically inside the {family} family's authored footprint band; no individual dimensions are documented."
            },
            "form": form_for(family, spec, sid, width, paint),
            "change_note": "Inferred anonymous July 1835 block infill; a better-evidenced named roof substitutes for a compatible count-unit rather than increasing the 665-roof total."
        }],
        "function": invented(function, f"Assigned from the {family} family to satisfy the block's scheduled mix; no occupant or individual use is known."),
        **({"occupants": OCCUPANCY[sid]} if sid in OCCUPANCY else {}),
        "reconstruction": reconstruction,
        "research_note": ("RECOMMENDED / GENERATED, NOT A DOCUMENTED NAMED BUILDING. The "
                          "block, its scheduled roof count and its family mix follow the "
                          "665-roof programme; exact presence, lot, position, footprint, "
                          "finish and instance-level form are interpretive." + mapping),
        "review_required": False,
    }


def build_block(block: dict, table: dict[str, dict], lots_by_id: dict[str, dict],
                datum: dict) -> list[dict]:
    grid = lots_by_id.get(block["block_id"])
    if grid is None:
        raise SystemExit(f"{block['block_id']} is not a block of the committed plat grid")
    alley = [tuple(p) for p in grid["alley_local_enu_m"]]
    frames = [lot_frame(lot, alley) for lot in grid["lots"]]

    records = []
    for seq, slot in enumerate(block["slots"], start=1):
        lot_index = int(slot["lot"])
        if not 0 <= lot_index < len(frames):
            raise SystemExit(f"{block['block_id']} has no lot {lot_index}")
        family = slot["family"]
        if family in REFUSED_FAMILIES:
            raise SystemExit(
                f"{block['block_id']}: this generator refuses to mass {family} — "
                f"{REFUSED_FAMILIES[family]} Defer the slot in the recipe's `deferred` "
                f"list with the reason, or reconcile it to a named record first.")
        spec = table.get(family)
        if spec is None:
            raise SystemExit(f"family {family} is not in the crosswalk")
        records.append(make_record(block, slot, lot_index, frames[lot_index], spec,
                                   family, datum, seq))
    check_block(block, grid, frames, records, datum)
    return records


# --------------------------------------------------------------------------
# the gates, run before a single file is written
# --------------------------------------------------------------------------

def check_block(block: dict, grid: dict, frames: list[dict], records: list[dict],
                datum: dict) -> None:
    from plat_corridors import corridors, intrusion  # noqa: PLC0415
    from heightfield import Heightfield  # noqa: PLC0415

    mine = [(r["id"], world_polygon(r, datum)) for r in records]

    # the schedule the recipe claims against
    counts = Counter(r["reconstruction"]["family"] for r in records)
    if dict(counts) != block["families"]:
        raise SystemExit(f"{block['block_id']}: the slots deal {dict(counts)}, the "
                         f"claimed schedule mix is {block['families']}")
    principal = sum(1 for r in records
                    if r["reconstruction"]["inventory_class"] == "principal_functional")
    claimed = block["drawn_from_schedule"]
    if (principal, len(records) - principal) != (claimed["principal"], claimed["ancillary"]):
        raise SystemExit(f"{block['block_id']}: {principal} principal / "
                         f"{len(records) - principal} ancillary against a claim of "
                         f"{claimed['principal']} / {claimed['ancillary']}")
    if len(records) > claimed["headroom"]:
        raise SystemExit(f"{block['block_id']}: {len(records)} roofs exceed the block's "
                         f"{claimed['headroom']} of headroom")

    # A parcel may build FEWER roofs than the schedule dealt it, but only by naming
    # each missing slot and the refusal it rests on. Without this, "the block carries
    # nine roofs" and "the schedule dealt it ten" are two numbers in two files and
    # nothing makes them meet — which is how a slot gets dropped for being awkward
    # rather than for being wrong, and the ledger reads as though it were never dealt.
    deferred = block.get("deferred") or []
    dealt_p = claimed.get("dealt_principal", claimed["principal"])
    dealt_a = claimed.get("dealt_ancillary", claimed["ancillary"])
    shortfall = (dealt_p - claimed["principal"]) + (dealt_a - claimed["ancillary"])
    if shortfall < 0:
        raise SystemExit(f"{block['block_id']}: the parcel claims to build more roofs "
                         f"than the schedule dealt it")
    if shortfall != len(deferred):
        raise SystemExit(f"{block['block_id']}: the schedule dealt {dealt_p + dealt_a} "
                         f"roofs and the parcel builds {len(records)}, but "
                         f"{len(deferred)} slot(s) are deferred — every roof dealt and "
                         f"not built must be named in `deferred` with its reason")
    for entry in deferred:
        family = entry.get("family")
        if family not in REFUSED_FAMILIES:
            raise SystemExit(f"{block['block_id']}: {family} is deferred, but this "
                             f"generator does not refuse {family} by name. A slot may "
                             f"only be deferred for a refusal the code states; "
                             f"anything else is a roof quietly dropped")
        if family in block["families"]:
            raise SystemExit(f"{block['block_id']}: {family} is both built and deferred")
        if len((entry.get("why") or "").split()) < 40:
            raise SystemExit(f"{block['block_id']}: the deferral of {family} does not "
                             f"state its reasoning. A refusal this project cannot read "
                             f"back is indistinguishable from an omission")

    # one principal roof per lot, and no lot carries two
    used = [r["reconstruction"]["lot_index"] for r in records
            if r["reconstruction"]["inventory_class"] == "principal_functional"]
    if len(set(used)) != len(used):
        raise SystemExit(f"{block['block_id']}: two principal roofs on one lot")

    # every other placed footprint in the dataset, in this block's local frame
    others = []
    for path in sorted(STRUCTURES.glob("*.json")):
        doc = load(path)
        if doc["id"] in {sid for sid, _ in mine}:
            continue
        for phase in doc.get("phases") or []:
            pos = phase.get("position") or {}
            poly = (phase.get("footprint") or {}).get("polygon") or []
            if pos.get("utm_e") is None or len(poly) < 3:
                continue
            others.append((doc["id"], world_polygon({"phases": [phase]}, datum)))

    # --- the lots this block ALREADY carries -------------------------------
    #
    # The check above asks whether this parcel put two roofs on one lot. It has
    # never been able to ask the question that matters on an occupied block —
    # whether the lot was free in the first place — because it reads only the
    # records this parcel builds, and the two blocks before this one were empty.
    # `blk_randolph_clinton` is the first block off the schedule that was not:
    # three roofs from the pre-plat West parcel stand on three of its eight lots,
    # placed from typed coordinates before the plat module existed, so nothing in
    # the dataset says which lot they are on. A free lot and a lot with somebody
    # else's house on it looked identical here, and the three-metre separation
    # gate does not close the difference: two principal roofs can stand twelve
    # metres apart on one twenty-five-metre lot and pass every test in this file.
    #
    # A lot is occupied by the footprint standing on it, so occupancy is DERIVED
    # from the committed records rather than authored in the recipe — a recipe
    # that had to be told which lots were taken would be a second opinion about
    # the same ground, which is the defect the plat module exists to retire.
    occupied: dict[int, str] = {}
    for other_id, other in others:
        centre = (sum(p[0] for p in other) / len(other),
                  sum(p[1] for p in other) / len(other))
        for index, frame in enumerate(frames):
            if point_in_polygon(centre, frame["polygon"]):
                occupied.setdefault(index, other_id)
    for record in records:
        recon = record["reconstruction"]
        index, holder = recon["lot_index"], occupied.get(recon["lot_index"])
        if holder is None:
            continue
        if recon["inventory_class"] == "principal_functional":
            raise SystemExit(f"{block['block_id']}: lot {index} already carries "
                             f"{holder}, so a principal roof cannot stand on it. The "
                             f"schedule's headroom is the block's, not the lot's")
        raise SystemExit(f"{block['block_id']}: the yard building on lot {index} "
                         f"stands behind {holder}, which this parcel did not build. A "
                         f"yard building is a claim about the household on its own lot")
    for record in records:
        recon = record["reconstruction"]
        if (recon["inventory_class"] != "principal_functional"
                and recon["lot_index"] not in set(used)):
            raise SystemExit(f"{block['block_id']}: the yard building on lot "
                             f"{recon['lot_index']} stands behind no roof — an ancillary "
                             f"building serves the lot it is in the yard of")

    # Every lot is built on, already taken, or open, and the recipe says which.
    # Without this the three classes are counted in three places and nothing makes
    # them meet: a lot could be called open in the recipe while a house stood on it,
    # which is a false statement about the town in the file that documents the town.
    open_entries = block.get("open_lots")
    if open_entries is None:
        single = block.get("open_lot")
        open_entries = [single] if single else []
    named_open = [int(entry["lot"]) for entry in open_entries]
    if len(set(named_open)) != len(named_open):
        raise SystemExit(f"{block['block_id']}: a lot is named open twice")
    for entry in open_entries:
        if len((entry.get("why") or "").split()) < 12:
            raise SystemExit(f"{block['block_id']}: lot {entry['lot']} is left open "
                             f"without saying why. Which lot is arbitrary, and an "
                             f"arbitrary choice nobody wrote down is indistinguishable "
                             f"from a slot that went missing")
    classes = {"built on by this parcel": set(used),
               "already carrying a roof": set(occupied),
               "named open in the recipe": set(named_open)}
    for name, indices in classes.items():
        for other_name, other_indices in classes.items():
            if name < other_name and indices & other_indices:
                raise SystemExit(f"{block['block_id']}: lot(s) "
                                 f"{sorted(indices & other_indices)} are both {name} "
                                 f"and {other_name}")
    accounted = set().union(*classes.values())
    if accounted != set(range(len(frames))):
        missing = sorted(set(range(len(frames))) - accounted)
        raise SystemExit(f"{block['block_id']}: lot(s) {missing} are neither built on, "
                         f"already occupied, nor named open. Every lot of a block this "
                         f"parcel claims has to be accounted for")

    # every footprint inside its own lot, clear of the conjectural side lines
    for record, (sid, poly) in zip(records, mine):
        lot = frames[record["reconstruction"]["lot_index"]]["polygon"]
        for pt in poly:
            if not point_in_polygon(pt, lot):
                raise SystemExit(f"{sid} reaches outside lot "
                                 f"{record['reconstruction']['lot_index']}")
            gap = distance_to_edges(pt, lot)
            if gap < LOT_MARGIN_M:
                raise SystemExit(f"{sid} stands {gap:.2f} m from its own lot line, "
                                 f"inside the {LOT_MARGIN_M} m margin")

    # nothing in the platted roadway. The lots are offset from the corridors, so this
    # cannot fail while the lot test passes — which is the point of running it anyway:
    # if the two ever disagree, the disagreement is the finding.
    lanes = corridors()
    for sid, poly in mine:
        street, depth = intrusion(poly, lanes)
        if street:
            raise SystemExit(f"{sid} reaches {depth:.1f} m inside the platted "
                             f"{lanes[street]['name']} corridor")

    # nothing within three metres of anything else in the dataset
    for sid, poly in mine:
        for other_id, other in others + [(s, p) for s, p in mine if s != sid]:
            gap = polygon_gap(poly, other)
            if gap < MIN_SEPARATION_M:
                raise SystemExit(f"{sid} stands {gap:.2f} m from {other_id}")

    # buildable ground, on the surface the walker uses
    field = Heightfield.load(DATA / "terrain" / "epochs" / "e1834_harbor_cut")
    if field is None:
        raise SystemExit("cannot validate placements: the committed heightfield is missing")
    for sid, poly in mine:
        pts = []
        for i, a in enumerate(poly):
            b = poly[(i + 1) % len(poly)]
            steps = max(2, int(math.dist(a, b)))
            pts += [(a[0] + (b[0] - a[0]) * k / steps, a[1] + (b[1] - a[1]) * k / steps)
                    for k in range(steps)]
        if not all(field.covers(e, n) for e, n in pts):
            raise SystemExit(f"{sid} falls outside the modelled terrain")
        heights = [field.height(e, n) for e, n in pts]
        if min(heights) < -.10:
            raise SystemExit(f"{sid} stands on the water side of the terrain")
        if max(heights) - min(heights) > MAX_RELIEF_M:
            raise SystemExit(f"{sid} spans {max(heights) - min(heights):.2f} m of relief")

    # the programme is a ceiling, not a budget to overspend
    inventory = load(INVENTORY_PATH)
    standing = Counter()
    for path in sorted(STRUCTURES.glob("*.json")):
        doc = load(path)
        recon = doc.get("reconstruction") or {}
        if recon.get("status") == "inferred_anonymous" and doc["id"] not in {s for s, _ in mine}:
            standing[recon["family"]] += 1
    for family, count in counts.items():
        target = inventory["family_targets"].get(family)
        if target is None:
            raise SystemExit(f"family {family} has no target in the building inventory")
        if standing[family] + count > target:
            raise SystemExit(f"{family}: {standing[family] + count} anonymous roofs "
                             f"against a programme target of {target}")

    # and every record resolves through the archetype it names
    for record in records:
        module = importlib.import_module(f"archetypes.{record['archetype']}_params")
        module.from_phase(record["phases"][0])


# --------------------------------------------------------------------------

def records_from_inputs() -> list[dict]:
    recipe = load(RECIPE_PATH)
    table = families()
    lots_by_id = {b["id"]: b for b in load(LOTS_PATH)["blocks"]}
    datum = load(DATA / "datum.json")
    records: list[dict] = []
    for block in recipe["blocks"]:
        records += build_block(block, table, lots_by_id, datum)
    ids = [r["id"] for r in records]
    if len(set(ids)) != len(ids):
        raise SystemExit("two block slots produced the same record id")

    # The adoption gate, in both directions. A household may name a roof this generator
    # owns, but only a PRINCIPAL one: an A-family roof is a stable, a privy or a woodshed
    # standing behind somebody's lot, and housing a household in one would be inventing an
    # occupant for a shed. The other direction — a roof the ledger names and no recipe
    # builds — would leave an adoption pointing at nothing, which is how a household
    # quietly loses its dwelling when a recipe is edited.
    by_id = {r["id"]: r for r in records}
    for sid in sorted(sid for sid in OCCUPANCY if sid.startswith(PREFIX)):
        record = by_id.get(sid)
        if record is None:
            raise SystemExit(f"the inferred-household programme adopts {sid}, which no "
                             f"block recipe builds")
        recon = record["reconstruction"]
        if recon["inventory_class"] != "principal_functional":
            raise SystemExit(f"{sid} is an ancillary {recon['family']} roof and cannot be "
                             f"adopted: a yard building serves the lot it stands behind, "
                             f"and an adoption is a claim about who lived or worked in a "
                             f"building")
    return records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the committed records still re-derive from the recipe")
    args = ap.parse_args()

    records = records_from_inputs()
    expected = {f"{r['id']}.json" for r in records}
    drift = []
    for rec in records:
        path = STRUCTURES / f"{rec['id']}.json"
        text = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists():
                drift.append(f"{path.relative_to(ROOT)} is missing")
            elif path.read_text(encoding="utf-8") != text:
                drift.append(f"{path.relative_to(ROOT)} has drifted from the block recipe")
        else:
            path.write_text(text, encoding="utf-8")
    for path in sorted(STRUCTURES.glob(f"{PREFIX}*.json")):
        if path.name not in expected:
            drift.append(f"{path.relative_to(ROOT)} is not in any block recipe")
    if drift:
        print("PLATTED BLOCK INFILL DRIFT")
        for item in drift:
            print(f"  - {item}")
        return 1
    blocks = len(load(RECIPE_PATH)["blocks"])
    mode = "verified" if args.check else "generated"
    print(f"{mode} {len(records)} anonymous roofs across {blocks} platted block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
