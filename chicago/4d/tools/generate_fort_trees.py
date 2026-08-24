#!/usr/bin/env python3
"""Generate the wood `p4_0` draws outside Fort Dearborn's walls (T-0098).

WHAT THIS IS. T-0044's image-accuracy pass listed eight gaps between the render and the two
committed Fort Dearborn plates. Number 8: *"No trees at the fort; `p4_0` puts a tree mass
east of the walls and `p4_1` trees round the buildings on both banks."* The render had none.
This tool stands them — by a RULE derived from the palisade's own committed footprint, the
way `tools/generate_fort_apron.py` derives the bare ground round the same walls, because a
tree mass a plate attests and does not place is a rule and never a list somebody typed.

**AND IT PUTS THEM ON THE OTHER SIDE, BECAUSE THE PLATE DOES.** T-0044's row 8 and this
ticket's own title say *east*. Both were read by eye. `tools/measure_fort_trees_plate.py`
measures the plate instead and the reading does not survive:

  * segmented for foliage, `p4_0` carries **33 334 connected pixels of canopy on the
    frame-RIGHT** of the drawn stockade, running from the stockade's end to the edge of the
    plate. On the frame-LEFT the largest connected patch is **924 px of bank grass on the
    viewer's own side of the river**, below the waterline. There is no mass on that side.
  * and frame-right is **WEST**, which is settled off the stand rather than off the picture:
    `p4_0`'s viewpoint is the north bank at local `1145, 300` looking SOUTH
    (`docs/RESEARCH/fort_dearborn_image_accuracy.md`; the render from it, HUD compass S
    180 deg, is `docs/RESEARCH/fort_from_the_north_bank_2026-08-19.png`), and the committed
    `chicago_lighthouse_1832` — 46.8 m WEST of the fort's centre — draws to the frame-RIGHT
    of the fort in that very shot.

So the wood stands WEST of the walls. The ticket's acceptance asks for trees *where the
plate puts them*, and this is where the plate puts them; the compass word in its title is
the thing that was wrong. The correction is written up in
`docs/RESEARCH/fort_dearborn_image_accuracy.md`.

THE RULE, and it is a rule rather than a list precisely so it can be argued with:

  **Every point of a deterministic grid on the ground OUTSIDE THE WEST WALL — beyond the
  fort's own apron, out to `REACH_M`, wrapping `FLANK_M` past each end of that wall —
  carries a stem, unless one of the renderer's own refusals declines it.**

Not one coordinate is authored. The band is derived from
`data/sidecars/1835/fort_dearborn_palisade.json`'s `footprint.polygon` and `placement` in
the frame `docs/GLB-CONTRACT.md` fixes, and its inner edge is read out of
`data/enclosures/fort_dearborn_apron.json`'s own `apron_width_m` rather than retyped — so if
the fort is re-placed, re-sized, or its apron re-cut, the wood follows or this file's
`--check` goes red in `tools/check.sh`.

WHAT THE REFUSALS ARE. Each is the renderer's own, asked here with a working margin on top
so a stem this tool deals can never be one `renderers/web/js/trees.js` then declines (a
declined stem is a `problems` line and the release smoke fails on it): the heightfield's
extent, the planter's dry floor, `blocked()`'s 4.5 m clearance off every committed
footprint, `streets.js`'s travelled track and shoulder, every committed fence line, the
fort's own trodden apron, and every stem already standing in the other two planting records.
**The refusals are what shape the wood.** The band as drawn reaches over the river's own
bend north-west of the fort; the dry floor cuts it back to the ground between the wall and
the water, which is exactly the falling ground the plate draws the mass on.

WHAT DECIDES THE SPECIES, and it is the measurement rather than a preference. `p4_0`'s
crowns stand **127 px above the wall foot**: 8.8 m on the fort's committed 53 m footprint,
10.9 m on its committed picket height, plus the fall of the bank the trees stand on, which
this tool derives from the committed heightfield. Of the three trees
`data/flora/zones/z10_settled_town.json` records, exactly one has a recorded height band
that can carry a crown that low — the relict **black willow**, banded 9-14 m, whose own note
in that record reads *"Left along the bank where the landing was cut."* The relict elm
(16-24 m) and the relict cottonwood (18-26 m) are REFUSED and the refusal is printed and
recorded: a 20 m cottonwood here would tower over a fort the plate draws it level with, and
`trees.js` would refuse the stem anyway if a height outside the band were stated.

WHAT IS INVENTED, plainly, and claimed in `docs/LIBERTIES.md`:

  * **How far west the wood reaches.** The plate does not bound it — the mass runs out of
    the right edge of the picture — so `REACH_M` is this project's number and nothing else's.
  * **How far it wraps past the wall's two ends** (`FLANK_M`), and how close its stems stand
    (`STEP_M`, dealt at the crown width the zone records for the species, so the canopy
    closes the way the plate's does).
  * **Every coordinate and every height**, inside the bounds above.

WHAT IS NOT INVENTED. That trees stood at this fort, on this side of it, at about this
height: that is what the plate draws and what the measurement above reads off it. And no
position here is plate-derived — `p4_0` is TIER 5 PICTORIAL and may never drive a
coordinate; it drives the SIDE, the crown height and nothing else.

WHAT WOULD MOVE IT OFF RECONSTRUCTION: an 1830s survey of the United States Reservation
showing timber; a garrison return or quartermaster's account of wood on the reservation; or
an identification of either plate against a dated original that would raise it above tier 5.

    python3 tools/generate_fort_trees.py            write the record
    python3 tools/generate_fort_trees.py --check    re-derive and diff
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from heightfield import Heightfield  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PALISADE = DATA / "sidecars" / "1835" / "fort_dearborn_palisade.json"
APRON = DATA / "enclosures" / "fort_dearborn_apron.json"
SIDECARS = DATA / "sidecars" / "1835"
STREETS = DATA / "streets" / "1835.json"
ENCLOSURES = DATA / "enclosures"
ZONE = DATA / "flora" / "zones" / "z10_settled_town.json"
EPOCH = DATA / "terrain" / "epochs" / "e1834_harbor_cut"
STANDING = [DATA / "flora" / "plantings" / "sauganash_yard.json",
            DATA / "flora" / "plantings" / "town_dooryard_plantings.json"]
OUT = DATA / "flora" / "plantings" / "fort_dearborn_wood.json"

ZONE_ID = "z10_settled_town"

# THE THREE INVENTED NUMBERS, and they are the whole of the invention.
#
# REACH_M — how far west of the apron the wood runs. The plate CANNOT bound this: the mass
# leaves the right edge of the picture (measured: it reaches column 1537 of 1538), so the
# number is this project's. 45 m is chosen as the distance at which the refusals below,
# not this constant, decide the wood's outline — the river's own bend cuts the band off
# before it is spent on three of its four rows, which is checked and printed by build().
REACH_M = 45.0
# FLANK_M — how far the wood wraps past the wall's two ends. The plate shows the mass
# beginning AT the stockade's west end in bearing (measured: 15 px past it, about a metre
# at the fort's own depth), which is a statement about bearing and not about plan, so a
# modest wrap is the honest reading of it and 8 m is that wrap.
FLANK_M = 8.0
# STEP_M — the grid the stems are dealt on. Not free: the zone records the species' crown
# at 6-10 m wide, and a canopy that CLOSES — which is what the plate draws, one connected
# mass with no sky through it — wants its stems inside a crown width of each other. 7.5 m
# is the middle of that band, and the jitter keeps the grid from reading as a plantation.
STEP_M = 7.5
JITTER_M = 1.6

# The measured crown height, straight off tools/measure_fort_trees_plate.py: 127 px above
# the wall foot, on the two scales that file prints rather than averages — the fort's
# committed 53 m footprint (14.37 px/m) and its committed picket height (11.62 px/m). The
# fall of the bank under the trees is ADDED to both by build(), derived from the committed
# heightfield rather than stated here.
MEASURED_CROWN_M = (8.8, 10.9)

# The renderer's own refusals, each with a working margin on top (the same margins
# tools/generate_dooryard_plantings.py deals against, for the same reason).
CLEAR_MARGIN_M = 4.5      # trees.js CLEAR_MARGIN — nothing grows nearer a wall
FOOTPRINT_MARGIN_M = 5.0  # this tool's stricter bound over CLEAR_MARGIN_M
TRACK_SHOULDER_M = 0.65   # streets.js blocksGrowth's shoulder off the track
TRACK_MARGIN_M = 2.0      # this tool's stricter bound over the shoulder
FENCE_MARGIN_M = 1.2      # no bole in a committed fence line
DRY_FLOOR_M = 0.9         # trees.js asks +0.20 over water; this tool asks more
STEM_SPACING_M = 3.0      # stems keep clear of the stems already standing
EDGE_INSET_M = 6.0        # and off the heightfield's own edge

SEED = "t98-fort-dearborn-wood-v1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def rnd(key: str) -> float:
    """Deterministic uniform [0,1) from a grid key — a re-run re-derives the same wood."""
    digest = hashlib.sha256(f"{SEED}:{key}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def to_enu(u: float, v: float, place: dict) -> tuple[float, float]:
    """A footprint coordinate to local ENU metres, in the frame docs/GLB-CONTRACT.md fixes.

    The same three lines generate_fort_apron.py uses to leave the fort's own frame: polygon
    `u` -> +X, polygon `v` -> -Z, ENU `local_e` -> +X and `local_n` -> -Z, node yaw
    `-rotation_deg` about +Y.
    """
    th = math.radians(-(place.get("rotation_deg") or 0.0))
    x, z = u, -v
    xr = x * math.cos(th) + z * math.sin(th)
    zr = -x * math.sin(th) + z * math.cos(th)
    return (place.get("local_e") or 0.0) + xr, (place.get("local_n") or 0.0) - zr


def footprint_world(sidecar):
    """A committed footprint in local ENU, placed the way walker.js places it."""
    fp = (sidecar.get("footprint") or {}).get("polygon") or []
    pl = sidecar.get("placement") or {}
    e0, n0 = pl.get("local_e"), pl.get("local_n")
    th = math.radians(pl.get("rotation_deg") or 0.0)
    c, s = math.cos(th), math.sin(th)
    return [(e0 + u * c + v * s, n0 - u * s + v * c) for u, v in fp]


def poly_contains(pt, poly) -> bool:
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def seg_dist(p, a, b) -> float:
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def poly_edge_dist(p, poly) -> float:
    return min(seg_dist(p, poly[i], poly[(i + 1) % len(poly)])
               for i in range(len(poly)))


def path_dist(p, path) -> float:
    return min(seg_dist(p, path[i], path[i + 1]) for i in range(len(path) - 1))


def world():
    """Everything a stem must stand clear of, read once and derived from committed files."""
    obstructions = []
    for path in sorted(SIDECARS.glob("*.json")):
        sc = load(path)
        pl = sc.get("placement") or {}
        if pl.get("local_e") is None:
            continue
        # walker.js footprintsFrom(): a water-anchored footprint is a deck and a record
        # drawn by another layer is a fence line, not a wall. Both excluded there, both
        # excluded here.
        if pl.get("vertical_anchor") == "water" or sc.get("drawn_by"):
            continue
        fp = footprint_world(sc)
        if len(fp) >= 3:
            obstructions.append(fp)
    streets = []
    for st in load(STREETS)["streets"]:
        pts = st.get("path_local_enu_m") or []
        if len(pts) >= 2:
            streets.append((pts, float(st.get("track_width_m") or 0.0)))
    fences, aprons = [], []
    for path in sorted(ENCLOSURES.glob("*.json")):
        if path.name == "index.json":
            continue
        rec = load(path)
        for run in rec.get("runs") or []:
            pts = run.get("path_local_enu_m") or []
            if len(pts) >= 2:
                fences.append(pts)
        # The treated GROUND of an enclosure record — the fort's own trodden apron is one,
        # and nothing grows on ground a record says is bare and trodden.
        for band in rec.get("bands") or []:
            ring = band.get("ring_local_enu_m") or []
            if len(ring) >= 3:
                aprons.append(ring)
    hf = Heightfield.load(EPOCH)
    if hf is None:
        raise SystemExit("no heightfield at " + str(EPOCH))
    taken = []
    for path in STANDING:
        for stem in load(path)["stems"]:
            taken.append(tuple(stem["at_local_enu_m"]))
    return obstructions, streets, fences, aprons, hf, taken


def refusal(p, obstructions, streets, fences, aprons, hf, taken):
    """Why this point may not carry a stem, or None if it may.

    Every clause is one of `renderers/web/js/trees.js`'s own refusals, asked of a point this
    tool chose rather than of one the planting loop offered.
    """
    e, n = p
    if not (hf.origin_e + EDGE_INSET_M <= e
            <= hf.origin_e + (hf.cols - 1) * hf.cell_m - EDGE_INSET_M
            and hf.origin_n + EDGE_INSET_M <= n
            <= hf.origin_n + (hf.rows - 1) * hf.cell_m - EDGE_INSET_M):
        return "off the modelled field"
    if hf.height(e, n) < float(hf.meta.get("water_surface_m", 0.0)) + DRY_FLOOR_M:
        return "in the river or below the planter's dry floor"
    for ring in aprons:
        if poly_contains(p, ring):
            return "on the fort's own trodden apron"
    for fp in obstructions:
        cx = sum(q[0] for q in fp) / len(fp)
        cy = sum(q[1] for q in fp) / len(fp)
        if abs(e - cx) > 60 or abs(n - cy) > 60:
            continue
        if poly_contains(p, fp) or poly_edge_dist(p, fp) < FOOTPRINT_MARGIN_M:
            return "inside a committed footprint or within its clearance"
    for pts, track_w in streets:
        if path_dist(p, pts) < track_w / 2 + TRACK_SHOULDER_M + TRACK_MARGIN_M:
            return "on a travelled track or its shoulder"
    for pts in fences:
        if path_dist(p, pts) < FENCE_MARGIN_M:
            return "in a committed fence line"
    for te, tn in taken:
        if math.hypot(e - te, n - tn) < STEM_SPACING_M:
            return "on a stem another planting record already states"
    return None


def species_by_band(zone, crown_m):
    """Which of the zone's recorded trees can carry the crown the plate draws.

    The rule, and the whole reason the species is not a preference: a stem's height has to
    lie inside its species' OWN recorded band or trees.js refuses to draw it, and the
    plate's measured crown height is what this record has to stand up. So the species is
    whichever of the zone's trees has a band that OVERLAPS the measured crown range, and
    every other one is refused in writing.
    """
    lo, hi = crown_m
    chosen, refused = [], []
    for sp in zone["species"]:
        if sp.get("role") != "tree":
            continue
        band = sp["height_m"]
        if band[0] <= hi and band[1] >= lo:
            chosen.append((sp["id"], band, (max(lo, band[0]), min(hi, band[1]))))
        else:
            refused.append(f"{sp['id']} is banded {band[0]}-{band[1]} m, which cannot carry "
                           f"a {lo:.1f}-{hi:.1f} m crown — refused, and trees.js would "
                           f"refuse the stem too")
    return chosen, refused


def build():
    pal = load(PALISADE)
    place = pal["placement"]
    poly = pal["footprint"]["polygon"]
    u_lo = min(u for u, _ in poly)
    v_lo = min(v for _, v in poly)
    v_hi = max(v for _, v in poly)
    apron_m = float(load(APRON)["derived_from"]["apron_width_m"])

    obstructions, streets, fences, aprons, hf, taken = world()
    zone = load(ZONE)

    # THE BANK'S OWN FALL, derived rather than stated: the plate's crowns are measured
    # against the ground at the WALL FOOT, and the wood stands on ground that falls away
    # from it, so the same skyline is a taller tree by exactly that fall.
    wall_mid = to_enu(u_lo, (v_lo + v_hi) / 2, place)
    band_mid = to_enu(u_lo - apron_m - REACH_M / 2, (v_lo + v_hi) / 2, place)
    fall = max(0.0, hf.height(*wall_mid) - hf.height(*band_mid))
    crown = (MEASURED_CROWN_M[0] + fall, MEASURED_CROWN_M[1] + fall)

    chosen, sp_refused = species_by_band(zone, crown)
    if len(chosen) != 1:
        raise SystemExit(
            f"the rule does not name one species: {len(chosen)} of "
            f"{ZONE_ID}'s trees can carry a {crown[0]:.1f}-{crown[1]:.1f} m crown "
            f"({', '.join(c[0] for c in chosen) or 'none'}). A tie or a blank is a real "
            "finding about the zone record and must be resolved there, not here.")
    species, band, height_range = chosen[0]

    stems, refused = [], []
    # The grid, laid in the FORT'S OWN FRAME so the wood is square to the wall it stands
    # off — which is what makes it derived from the fort rather than from the compass.
    rows = int(round((REACH_M) / STEP_M))
    cols = int(round((v_hi - v_lo + 2 * FLANK_M) / STEP_M))
    dealt = 0
    for i in range(rows + 1):
        for j in range(cols + 1):
            key = f"{i}:{j}"
            u = u_lo - apron_m - i * STEP_M - (rnd(key + ":u") - 0.5) * 2 * JITTER_M
            v = v_lo - FLANK_M + j * STEP_M + (rnd(key + ":v") - 0.5) * 2 * JITTER_M
            e, n = to_enu(u, v, place)
            p = (round(e, 2), round(n, 2))
            dealt += 1
            why = refusal(p, obstructions, streets, fences, aprons, hf, taken)
            if why:
                refused.append(f"{key} at {p[0]}, {p[1]}: {why}")
                continue
            h = round(height_range[0]
                      + (height_range[1] - height_range[0]) * rnd(key + ":h"), 1)
            stems.append({
                "id": f"fort_wood_{i:02d}_{j:02d}",
                "species": species,
                "at_local_enu_m": list(p),
                "height_m": h,
                "confidence": "reconstructed",
                "note": (f"DEALT BY RULE at grid {key} of the band west of the fort's west "
                         f"wall, beyond its own {apron_m:g} m apron. {h} m is inside both "
                         f"the species' recorded {band[0]}-{band[1]} m band and the "
                         f"{crown[0]:.1f}-{crown[1]:.1f} m crown measured off p4_0."),
            })
            taken.append(p)
    return {
        "stems": stems, "refused": refused, "dealt": dealt,
        "species": species, "band": band, "height_range": height_range,
        "species_refused": sp_refused, "crown": crown, "fall": fall,
        "apron_m": apron_m,
    }


def record(b):
    return {
        "_doc": (
            "A PLANTING RECORD in the shape T-0091 established and T-0074 generalised: "
            "woody stems whose position is STATED rather than dealt from the land. This "
            "one is GENERATED — tools/generate_fort_trees.py holds the rule, prints why "
            "every refused point was refused, and re-derives this file byte for byte in "
            "tools/check.sh."
        ),
        "id": "fort_dearborn_wood",
        "name": "The wood outside Fort Dearborn's west wall",
        "kind": "planting",
        "scene": "1835",
        "target_date": "1835-07-01",
        "generated_by": "tools/generate_fort_trees.py",
        "generated_from": [
            "data/sidecars/1835/fort_dearborn_palisade.json",
            "data/enclosures/fort_dearborn_apron.json",
            "data/sidecars/1835/*.json",
            "data/streets/1835.json",
            "data/enclosures/*.json",
            "data/flora/zones/z10_settled_town.json",
            "data/terrain/epochs/e1834_harbor_cut/heightfield.json",
            "data/sources/assets/prefire_views_kevin_2026_08/p4_0.png",
        ],
        "belongs_to": ["fort_dearborn_palisade"],
        "in_enclosure": None,
        "zone": ZONE_ID,
        "existence": {
            "value": True,
            "confidence": "inferred",
            "sources": ["chicagology_prefire273"],
            "note": (
                "THE TREATMENT AND THE SIDE ARE THE PLATE'S; THE SPECIES ARE THE ZONE'S; "
                "EVERY COORDINATE IS THIS PROJECT'S. p4_0 — the coloured Fort Dearborn "
                "view in data/sources/assets/prefire_views_kevin_2026_08/, the plate this "
                "project shoots the fort against — draws a substantial tree mass outside "
                "the walls, and p4_1 draws trees round the buildings on both banks. "
                "Measured with tools/measure_fort_trees_plate.py, that mass is 33 334 "
                "connected pixels of canopy on the FRAME-RIGHT of the drawn stockade, "
                "against a largest frame-left patch of 924 px which is bank grass on the "
                "viewer's own side of the river. Frame-right is WEST: p4_0's stand is the "
                "north bank looking south, and the committed chicago_lighthouse_1832, 46.8 "
                "m west of the fort's centre, draws to the frame-right of the fort in the "
                "render from that same stand. The plates are tier-5 retrospective and are "
                "not source records here yet (T-0055, T-0075), so they carry the FACT and "
                "no coordinate — the same reading T-0091 and T-0074 record. The cited "
                "source_id carries the other half: chicagology_prefire273 stands behind "
                "data/flora/zones/z10_settled_town.json, whose relict black willow — 'Left "
                "along the bank where the landing was cut' — is the species every stem "
                "here names."
            ),
        },
        "stems": b["stems"],
        "refused": b["refused"],
        "research_note": (
            f"{len(b['stems'])} STEMS OF {len(b['stems']) and b['species'].upper()} WEST OF "
            f"THE FORT'S WEST WALL, EVERY ONE DEALT BY THE RULE IN "
            "tools/generate_fort_trees.py AND RE-DERIVED ON EVERY COMMIT. "
            "THE SIDE IS A CORRECTION, and it is the point of this record: T-0044's "
            "image-accuracy row 8 and ticket T-0098's own title both say the mass is EAST "
            "of the walls, both were read by eye, and the measurement says west. The "
            f"reading is in tools/measure_fort_trees_plate.py and the write-up in "
            "docs/RESEARCH/fort_dearborn_image_accuracy.md. "
            f"THE SPECIES IS THE MEASUREMENT'S, NOT A PREFERENCE: p4_0's crowns stand 127 "
            f"px above the wall foot, which is 8.8 m on the fort's committed 53 m "
            f"footprint and 10.9 m on its committed picket height, plus the "
            f"{b['fall']:.2f} m the bank falls under the wood — a "
            f"{b['crown'][0]:.1f}-{b['crown'][1]:.1f} m crown. Of "
            f"{ZONE_ID}'s three recorded trees only the relict black willow is banded low "
            f"enough to carry it; " + "; ".join(b["species_refused"]) + ". Every stem's "
            f"height is dealt inside {b['height_range'][0]:.1f}-{b['height_range'][1]:.1f} "
            "m, which is the overlap of the species' recorded band and the measured crown "
            "— so a stem is inside the band trees.js checks AND inside what the plate "
            "shows. "
            f"THE OUTLINE IS THE REFUSALS' AND NOT THIS FILE'S: {b['dealt']} grid points "
            f"were dealt and {len(b['refused'])} refused, most of them for standing in the "
            "river's own bend north-west of the fort, which is what cuts the wood back to "
            "the falling ground between the wall and the water — the ground the plate "
            "draws the mass on. WHAT IS INVENTED: how far west the wood reaches (the plate "
            "cannot bound it — the mass leaves the right edge of the picture), how far it "
            "wraps past the wall's ends, how close the stems stand, and every coordinate "
            "and height inside those bounds. Claimed in docs/LIBERTIES.md. WHAT IS "
            "DELIBERATELY NOT HERE: the two-storey frame house the plate draws inside this "
            "mass, which is a STRUCTURE record and not a flora one, and which no source "
            "this project holds identifies; and any claim about the ground under the wood, "
            "which the sward layer still draws as it drew it."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()
    b = build()
    text = json.dumps(record(b), indent=2, ensure_ascii=False) + "\n"
    summary = (f"{len(b['stems'])} stems of {b['species']} at "
               f"{b['height_range'][0]:.1f}-{b['height_range'][1]:.1f} m, "
               f"{len(b['refused'])} of {b['dealt']} grid points refused")
    if args.check:
        if not OUT.exists():
            print(f"FORT WOOD DRIFT\n  - {OUT.relative_to(ROOT)} is missing")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"FORT WOOD DRIFT\n  - {OUT.relative_to(ROOT)} has drifted from the "
                  f"rule in tools/generate_fort_trees.py")
            return 1
        print(f"verified {summary}")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
