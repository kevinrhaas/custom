#!/usr/bin/env python3
"""Derive the town's river wharves from the records that state one.

    python3 tools/generate_river_wharves.py            write the record
    python3 tools/generate_river_wharves.py --check    re-derive and diff, write nothing

WHY THIS EXISTS. `docs/ROADMAP.md` K5 (e) asks for *"docks/wharves at the
forwarding houses"* and ticket T-0041 is that clause. Two records in this dataset
state a dock and both of them state it in the same sentence of the same dossier —
*"Kinzie & Hunter and Dole & Newberry each had a warehouse with its dock along the
river front"* (docs/research/03-structures-north.md §3.10) — and Andreas names
*"Newberry & Dole's wharf"* independently, as the place the schooner *Illinois*
was cheered on 12 July 1834 (scan p. 503). Until now BOTH docks carried
`geometry: "absent"`: the strongest chip this project hands out, over nothing at
all, in front of a bare bank. `docs/LIBERTIES.md` L66 recorded that as owed.

So the FACT of a wharf at these two frontages is the best-attested thing on this
layer, and every dimension of it is invented. That is `reconstructed` in this
project's third tier, which AGENTS.md § RECONSTRUCTED IS A TIER says is a licence
to build rather than an admission of defeat.

THE RULE, and it is the whole answer to "why these frontages and no others":

    a sidecar standing on the scene date whose own `dock` attribute is true.

T-0041 shipped that rule with a grade clause — attested or inferred only, no
`reconstructed`, because a dock resting on a reconstructed dock read as an
invention on an invention — and it selected exactly two records. On 2026-08-18
the owner overruled the rationing, verbatim "you can add more docks!" (T-0062,
with the standing ruling in AGENTS.md § RECONSTRUCTED IS A TIER), so five South
Water merchant records now STATE a reconstructed landing, each with its bound in
its own note, and this generator draws them. The selection still lives in the
data: a record with no dock statement — the Temple Building's meeting house on
the same frontage, the lumber landing, the ferry — still gets no wharf, and
"why this frontage" is still answered by a record rather than by this file.

THE WEST BANK WAS OUT OF THAT PASS BY CONSTRUCTION, NOT BY MEASUREMENT (T-0107).
T-0062 stated its five docks on *South Water merchants*, so the town's other two
shores were never asked the question — the North Division shore only carried a
wharf because Kinzie & Hunter's dock happens to be attested, and the west bank at
Wolf Point carried none at all. That is a fact about which records were edited on
2026-08-19, not a finding about Wolf Point. So the trade test now runs on every
river frontage in the town, whichever bank it stands on, and on the west bank it
selects exactly ONE record: Robert A. Kinzie's storehouse, "dealing in groceries
and Indian goods", whose own position note had already reasoned that "a storehouse
trading goods off canoes has a positive reason to face the landing" and set its
facade due east onto the water on that reading. The other four buildings in that
row — Wentworth's tavern, James Kinzie's residence, the Robinson and Caldwell
cabins, Father Walker's log meeting house — state no dock and get none: lodging,
dwelling and worship take nothing off a canoe, which is the Temple Building's
exclusion carried across the river.

AND THE BANK BENDS AT WOLF POINT, which is what clause 6 is for. This layer's
deck is a RECTANGLE set on the bank's own tangent — one standard form, so its
dimensions are invented once (L132) rather than once per site — and a rectangle
run against a curve can put the far end of its face behind the bank, on dry
ground. PR #258 measured that at Hogan's store, whose face runs from 1.10 m of
water at one end to −0.34 m at the other, and refused it rather than invent a
bespoke outline for one frontage. That refusal is now a clause with the measured
figure on the record, the same way the trace-reach refusals carry theirs.

WHAT IS DERIVED AND WHAT IS INVENTED — the division this file exists to keep
auditable:

  DERIVED, from committed data, no free numbers at all
    * the wall the wharf serves: the footprint's own max-`v` edge and the
      committed facade bearing, through `docs/GLB-CONTRACT.md`'s frame — the same
      three lines `tools/generate_business_signboards.py` composes.
    * WHERE the wharf stands: the traced 1834 bank line
      (`data/terrain/epochs/e1834_harbor_cut/river.geojson`), nearest point to the
      middle of that wall. The deck runs ALONG the bank's own tangent, not square
      to the building — a wharf follows the river, and the two differ by 20° here.
    * how deep the water is at its face, and how far it stands clear of the
      building it serves: sampled from the committed heightfield, reported rather
      than assumed, so what the invented outline implies is on the record.

  INVENTED, and every one of them is in `form` with its bound stated
    * how far out the face stands (6.0 m), how far the heel ties back into the
      bank (2.0 m), how far the deck runs past the building each way (3.0 m),
      the deck's thickness, its freeboard rule and its snubbing posts.

Nothing here is baked. A deck on cribs is a box on boxes standing on ground and
water this project already draws, so it is derived from committed numbers and
drawn at load by `renderers/web/js/wharves.js` — the argument that already lets
`data/enclosures/` draw a fence from a perimeter, `data/signage/` hang a board off
a wall and `data/yard/` stand a barrel on the footway. `tools/check.sh` re-derives
this file's output byte for byte, because "which frontage gets a wharf" is a rule
and a rule has to be auditable.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIDECARS = ROOT / "data" / "sidecars" / "1835"
EPOCH = ROOT / "data" / "terrain" / "epochs" / "e1834_harbor_cut"
OUT = ROOT / "data" / "wharves" / "river_landings.json"

sys.path.insert(0, str(ROOT / "tools"))
from heightfield import Heightfield          # noqa: E402  (path set above)

# The grades a dock statement may carry. T-0041 shipped this tuple WITHOUT
# `reconstructed` — a dock resting on a reconstructed dock read as an invention
# on an invention — and the owner overruled that reading on 2026-08-18, verbatim
# "you can add more docks!", with the general ruling recorded in AGENTS.md
# § RECONSTRUCTED IS A TIER: be liberal with reconstructed items when asked,
# label them as such. So a sidecar may now STATE a reconstructed dock (T-0062
# authored five, each with its bound in its own note) and this generator draws
# it. What has not changed: the selection still lives in the DATA — a sidecar
# with no dock statement still gets no wharf, so "why this frontage" is still
# answered by a record and never by this file.
DOCK_GRADES = ("attested", "documented", "inferred", "reconstructed")

# --- the invented figures, all of them, in one place ------------------------ #
# They are copied into the record's `form` block with their reasons; they are
# here as constants so the generator and the record cannot come to disagree.
FACE_OUT_M = 6.0        # how far the deck's face stands beyond the traced bank
HEEL_IN_M = 2.0         # how far its landward edge ties back into the bank
APRON_M = 3.0           # how far it runs past the building it serves, each way
DECK_T_M = 0.14         # the plank deck's thickness
FREEBOARD_M = 0.90      # the least the deck top may stand above the water plane
POST_SIDE_M = 0.22      # a snubbing post, square
POST_HEIGHT_M = 0.75    # and how far it stands proud of the deck
CRIB_W_M = 1.20         # the crib wall under the deck's outer face and its ends


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _round(x: float, places: int = 2) -> float:
    """Round toward a stable decimal so `--check` diffs bytes, not float noise."""
    return round(x + 0.0, places) + 0.0


def _to_enu(u: float, v: float, place: dict) -> tuple[float, float]:
    """A footprint coordinate to local ENU metres.

    `docs/GLB-CONTRACT.md`: polygon `u` → +X, polygon `v` → −Z, ENU `local_e` → +X
    and `local_n` → −Z, and the node's yaw is `-rotation_deg` about +Y. Identical
    to `tools/generate_business_signboards.py::_to_enu`, deliberately: two layers
    reading the same frame two ways is how a building grows two front walls.
    """
    th = math.radians(-(place.get("rotation_deg") or 0.0))
    x, z = u, -v
    xr = x * math.cos(th) + z * math.sin(th)
    zr = -x * math.sin(th) + z * math.cos(th)
    return (place.get("local_e") or 0.0) + xr, (place.get("local_n") or 0.0) - zr


def _front_edge(polygon: list) -> tuple[float, float, float]:
    """The wall the record faces out of: the footprint's max-`v` edge."""
    vmax = max(p[1] for p in polygon)
    on = [p[0] for p in polygon if abs(p[1] - vmax) < 1e-6]
    if len(on) < 2:
        return 0.0, 0.0, vmax
    return min(on), max(on), vmax


def bank_lines() -> list[dict]:
    """The traced 1834 bank lines, in local ENU metres.

    `river.geojson` is EPSG:26916 and the scene is local ENU from
    `data/datum.json`'s origin, which is the one conversion this file makes.
    """
    datum = _load(ROOT / "data" / "datum.json")
    oe, on = float(datum["origin_utm_e"]), float(datum["origin_utm_n"])
    out: list[dict] = []
    for f in _load(EPOCH / "river.geojson").get("features", []):
        geom = f.get("geometry") or {}
        props = f.get("properties") or {}
        if geom.get("type") != "LineString" or props.get("kind") != "bank":
            continue
        out.append({
            "name": props.get("name"),
            "confidence": props.get("confidence"),
            "sources": props.get("sources") or [],
            "points": [(x - oe, y - on) for x, y in geom["coordinates"]],
        })
    return out


def nearest_on(points: list, p: tuple) -> tuple[float, tuple, tuple, float, float]:
    """(distance, foot point, unit tangent, arclength at foot, total arclength)
    for the nearest segment of a polyline. The two arclengths exist for clause
    4b: a deck may only stand where the bank is actually TRACED, and the test is
    its run against the trace's own extent rather than a guess about endpoints.
    """
    best = None
    s = 0.0
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1])
                for a, b in zip(points, points[1:]))
    for a, b in zip(points, points[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        L = math.sqrt(L2) or 1.0
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx
                                                   + (p[1] - a[1]) * dy) / L2))
        q = (a[0] + t * dx, a[1] + t * dy)
        d = math.hypot(p[0] - q[0], p[1] - q[1])
        if best is None or d < best[0]:
            best = (d, q, (dx / L, dy / L), s + t * L, total)
        s += L
    return best


def _face_stations(face: tuple, tangent: tuple, half: float) -> list[tuple]:
    """Where the depth under the deck's face is sampled, at about 1 m intervals.

    THREE POINTS WERE NOT ENOUGH AND THE BEND AT WOLF POINT IS WHY (T-0107). The
    record has always reported the depth at the face's two ends and its middle,
    and that is what it still reports; but a deck outline is a RECTANGLE run
    against a bank that curves, so the shallowest metre of a face is not obliged
    to be one of those three. Sampling the run is what lets clause 6 answer "is
    this deck afloat" about the whole face instead of about three points of it.
    """
    n = max(3, int(round(2.0 * half)) + 1)
    return [(face[0] + tangent[0] * t, face[1] + tangent[1] * t)
            for t in (-half + 2.0 * half * i / (n - 1) for i in range(n))]


def derive_one(sid: str, sc: dict, banks: list, field) -> tuple[str | None, dict | None]:
    """One candidate through the clause table: ('wharf'|'refused'|None, row).

    Split out of `build_record` by T-0107 so the clauses can be fired on
    constructed frontages by `selftest()` as well as on the committed sidecars. A
    refusal clause that never fires on the dataset is a clause nobody has seen
    work, and clause 6 refuses nothing in the town as it stands — every drawn
    face is afloat by a metre. So it is proved on a stand built for it instead of
    being taken on trust.
    """
    dock = (sc.get("attributes") or {}).get("dock")
    if not isinstance(dock, dict) or not dock.get("value"):
        return None, None                                        # clause 1
    grade = dock.get("confidence")
    if grade not in DOCK_GRADES:
        return "refused", {"structure_id": sid, "why": (
            f"its dock is graded {grade!r}, which is not a grade this "
            "project's confidence model has. A statement this layer cannot "
            "classify is a statement it does not draw.")}         # clause 2

    place = sc.get("placement") or {}
    poly = (sc.get("footprint") or {}).get("polygon") or []
    if len(poly) < 3:
        return "refused", {"structure_id": sid,
                           "why": "no footprint polygon — no wall to serve."}
    u0, u1, vmax = _front_edge(poly)                              # clause 3
    wall_a = _to_enu(u0, vmax, place)
    wall_b = _to_enu(u1, vmax, place)
    mid = ((wall_a[0] + wall_b[0]) / 2.0, (wall_a[1] + wall_b[1]) / 2.0)
    frontage = math.hypot(wall_b[0] - wall_a[0], wall_b[1] - wall_a[1])

    near = [(nearest_on(b["points"], mid), b) for b in banks]
    (dist, foot, tangent, foot_s, bank_len), bank = min(near, key=lambda r: r[0][0])
    # Outward is across the bank, away from the building it serves. Deriving
    # it from the building rather than from the polygon's winding is what
    # keeps a wharf on the water when a bank line is re-traced the other way.
    nx, ny = -tangent[1], tangent[0]
    if (foot[0] - mid[0]) * nx + (foot[1] - mid[1]) * ny < 0:
        nx, ny = -nx, -ny

    half = frontage / 2.0 + APRON_M

    # CLAUSE 4b (T-0062): every metre of the deck must stand off a traced
    # metre of bank. The 1834 bank polylines end at local E 390 and three
    # stated South Water landings lie east of that; without this clause all
    # three snapped to the trace's terminal vertex and stacked on one point
    # — a modelling error wearing three wharves' clothes. A landing refused
    # here is STATED AND NOT DRAWN until the trace reaches it (T-0106),
    # because a deck derived from a bank that is not there is derived from
    # nothing.
    if foot_s - half < 0.0 or foot_s + half > bank_len:
        return "refused", {"structure_id": sid, "why": (
            "its frontage lies beyond the traced 1834 bank line, so part of "
            "its deck would stand off bank nobody traced. The dock "
            "statement stands; the landing is drawn when the trace reaches "
            "this reach (T-0106).")}                              # clause 4b

    heel = (foot[0] - nx * HEEL_IN_M, foot[1] - ny * HEEL_IN_M)
    face = (foot[0] + nx * FACE_OUT_M, foot[1] + ny * FACE_OUT_M)
    corners = [                       # heel-left, heel-right, face-right, face-left
        (heel[0] - tangent[0] * half, heel[1] - tangent[1] * half),
        (heel[0] + tangent[0] * half, heel[1] + tangent[1] * half),
        (face[0] + tangent[0] * half, face[1] + tangent[1] * half),
        (face[0] - tangent[0] * half, face[1] - tangent[1] * half),
    ]

    # The deck may not reach the building it serves: a wharf that laps a wall
    # is a modelling error wearing a wharf's clothes, and the two placements
    # were authored with exactly this strip left clear ("about 8 m back from
    # the traced bank to leave the dock its ground"; "about 14 m back ... so
    # the strip between it and the water can carry the dock").
    clearance = min(nearest_on([wall_a, wall_b], c)[0] for c in corners[:2])
    if clearance < 1.0:
        return "refused", {"structure_id": sid, "why": (
            f"its heel would come within {clearance:.2f} m of the building's "
            "own river wall. A wharf that laps the wall it serves is a "
            "modelling error, and this record refuses to draw one.")}  # clause 4

    # What the invented outline implies, measured on the committed bed rather
    # than assumed: how much water a vessel lying at this face would have. The
    # three the record reports are the face's ends and its middle; the run at
    # 1 m is what clauses 5 and 6 are decided on.
    stations = _face_stations(face, tangent, half)
    run = [-field.height(e, n) if field and field.covers(e, n) else None
           for e, n in stations]
    depths = [run[0], run[len(run) // 2], run[-1]]
    if any(d is None for d in run):
        off = next(i for i, d in enumerate(run) if d is None)
        where = -half + 2.0 * half * off / (len(run) - 1)
        return "refused", {"structure_id": sid, "why": (
            "its face falls outside the modelled ground "
            f"{abs(where):.1f} m from its centre, so the depth at it "
            "cannot be measured and the wharf is not drawn.")}    # clause 5

    # CLAUSE 6 (T-0107): THE FACE HAS TO BE AFLOAT ALONG ITS WHOLE RUN. The deck
    # outline is a rectangle set on the bank's own tangent, and THE BANK BENDS —
    # at Wolf Point and again in the wedge where Lake Street runs out at the
    # South Branch. Where it bends away from the deck, the far end of a face
    # standing 6 m off the tangent lands BEHIND the bank, on dry ground: PR #258
    # measured exactly that at Hogan's store, whose face runs from 1.10 m of
    # water at one end to −0.34 m at the other, and refused it rather than invent
    # a bespoke outline for one frontage. That refusal is the rule now. A deck
    # whose face is not in water is not a landing; the alternative — a bespoke
    # outline per bend — would make every wharf's shape a judgement instead of a
    # derivation, and the standard form is the whole reason this layer can claim
    # its dimensions are invented ONCE (L132) rather than once per site.
    least = min(run)
    if least <= 0.0:
        off = min(range(len(run)), key=lambda i: run[i])
        where = -half + 2.0 * half * off / (len(run) - 1)
        return "refused", {"structure_id": sid, "why": (
            f"its deck's face would stand on dry ground: the bed rises to "
            f"{-least:.2f} m ABOVE the water plane {abs(where):.1f} m from the "
            "face's centre, because the bank bends away from the standard "
            "rectangular outline here. The dock statement stands; a landing is "
            "drawn when a deck of the standard form is afloat along its whole "
            "face, and this project will not invent a bespoke outline for one "
            "frontage.")}                                          # clause 6

    return "wharf", {
        "structure_id": sid,
        "name": sc.get("name"),
        "dock_confidence": grade,
        "dock_sources": dock.get("sources") or [],
        "confidence": "reconstructed",
        "bank": bank["name"],
        "bank_confidence": bank["confidence"],
        "bank_sources": bank["sources"],
        "bank_foot_local_enu_m": [_round(foot[0]), _round(foot[1])],
        "bank_tangent": [_round(tangent[0], 4), _round(tangent[1], 4)],
        "waterward_normal": [_round(nx, 4), _round(ny, 4)],
        "deck_quad_local_enu_m": [[_round(c[0]), _round(c[1])] for c in corners],
        "deck_length_m": _round(2 * half),
        "deck_width_m": _round(FACE_OUT_M + HEEL_IN_M),
        "frontage_served_m": _round(frontage),
        "wall_to_bank_m": _round(dist),
        "clearance_to_wall_m": _round(clearance),
        "depth_at_face_m": [_round(d) for d in depths],
        # The shallowest of the 1 m stations, which is the figure clause 6 is
        # decided on. Reported so the margin a drawn landing passes by is on the
        # record rather than in the generator's head — the same reason
        # depth_at_face_m is reported rather than assumed.
        "least_depth_at_face_m": _round(min(run)),
        "face_stations": len(run),
        "facade_bearing_deg": _round(place.get("rotation_deg") or 0.0, 1),
    }


def build_record() -> tuple[list, list]:
    index = _load(SIDECARS / "index.json")
    banks = bank_lines()
    field = Heightfield.load(EPOCH)
    wharves: list[dict] = []
    refused: list[dict] = []

    for entry in index.get("structures", []):
        sid = entry.get("id")
        path = SIDECARS / f"{sid}.json"
        if not sid or not path.exists():
            continue
        kind, row = derive_one(sid, _load(path), banks, field)
        if kind == "wharf":
            wharves.append(row)
        elif kind == "refused":
            refused.append(row)

    wharves.sort(key=lambda w: w["structure_id"])
    refused.sort(key=lambda r: r["structure_id"])
    return wharves, refused


def record(wharves: list, refused: list) -> dict:
    return {
        "_doc": (
            "The town's river wharves and landings — a plank deck on timber "
            "cribs at each frontage whose own record states a dock: the two "
            "forwarding warehouses whose dock the dossier states (T-0041), "
            "the five South Water merchant landings reconstructed under the "
            "owner's ruling of 2026-08-18 (T-0062), and Robert A. Kinzie's "
            "storehouse on the WEST bank at Wolf Point, the first landing this "
            "layer has put on that shore (T-0107). NOT structure "
            "records and NOT geometry that comes out of Blender: a deck on cribs "
            "is a box on boxes standing on ground and water this project already "
            "draws, so it is derived from the committed footprint, the traced "
            "bank and the committed heightfield and drawn at load by "
            "renderers/web/js/wharves.js — the same argument that lets the "
            "enclosure layer draw a fence from a perimeter and the yard layer "
            "stand a barrel on the footway. Generated by "
            "tools/generate_river_wharves.py and re-derived byte for byte by "
            "tools/check.sh, because 'which frontage gets a wharf' is a rule and "
            "a rule has to be auditable."
        ),
        "id": "river_landings",
        "name": "The river wharves and the South Water landings",
        "kind": "wharves",
        "scene": "1835",
        "target_date": "1835-07-01",
        "coordinates": (
            "Local East-North-Up metres from data/datum.json's origin, the same "
            "frame data/enclosures/, data/signage/, data/yard/ and the sidecars' "
            "placement.local_e / local_n use. The water surface is Z = 0 by "
            "construction (data/datum.json § vertical)."
        ),
        "counts": {"wharves": len(wharves), "refused": len(refused)},
        "existence": {
            "value": True,
            "confidence": "reconstructed",
            "sources": ["andreas_1884_v1"],
            "note": (
                "THE FACT OF A WHARF AT THESE TWO FRONTAGES IS THE BEST-ATTESTED "
                "THING ON THIS LAYER AND EVERY DIMENSION OF IT IS INVENTED. What "
                "is held: docs/research/03-structures-north.md §3.10 — 'Kinzie & "
                "Hunter and Dole & Newberry each had a warehouse WITH ITS DOCK "
                "ALONG THE RIVER FRONT' — which is the clause that attests the "
                "Kinzie & Hunter building at all; and Andreas independently names "
                "'Newberry & Dole's wharf' as the place the schooner Illinois, "
                "the first vessel through the new cut, was cheered on 12 July "
                "1834 (scan p. 503). What is NOT held, anywhere in this project: "
                "the length, the width, the height, the construction or the "
                "condition of either dock. Both records carried "
                "geometry: 'absent' over that statement until this layer existed "
                "— the strongest confidence chip in the dataset, over a bare bank "
                "— which docs/LIBERTIES.md L66 recorded as owed and L132 now "
                "claims. NOTHING HERE IS PROMOTED ABOVE reconstructed on the "
                "strength of the sentence: a dock is stated, and this is what a "
                "dock is drawn as. THE FIVE SOUTH WATER LANDINGS (T-0062) STAND "
                "ONE TIER LOWER STILL: no source states a dock at any of them, "
                "and their existence is itself reconstructed under the owner's "
                "ruling of 2026-08-18 ('you can add more docks!'), bounded per "
                "frontage in each record's own dock note — the trade that takes "
                "goods off the water, the working reach the 2026-08-18 brief "
                "shows crowded with masts, and the wharfing-out practice of the "
                "south bank. Claimed at docs/LIBERTIES.md L145. THE WEST BANK'S "
                "ONE LANDING (T-0107) STANDS ON THE SAME FOOTING AND IS BOUNDED "
                "BY ITS OWN RECORD'S TRADE: Robert A. Kinzie's storehouse at "
                "Wolf Point dealt in 'groceries and Indian goods' (chicagology) "
                "and its keeper is Andreas's 'Indian Traders — Robert A. "
                "Kinzie, near Wentworth's tavern' (scan p. 235); the record's "
                "committed position note had already reasoned that 'a "
                "storehouse trading goods off canoes has a positive reason to "
                "face the landing', which is why its facade was set due east "
                "onto the water before any wharf layer existed. NO SOURCE "
                "STATES A DOCK, WHARF OR LANDING ANYWHERE AT WOLF POINT. Each "
                "wharf row "
                "below reports its own dock_confidence, which is the honest "
                "division between the stated docks and the invented ones."
            ),
        },
        "rule": {
            "note": (
                "A sidecar standing on the scene date whose own `dock` attribute "
                "is true. T-0041 shipped the rule with a grade clause — attested "
                "or inferred only — and it selected exactly two records; the "
                "owner overruled the rationing on 2026-08-18 ('you can add more "
                "docks!'), so five South Water merchant records now state a "
                "reconstructed landing, each bounded in its own note, and the "
                "rule draws them too. The selection still lives in the data: a "
                "record with no dock statement — the Temple Building's meeting "
                "house on the same frontage, the lumber landing, the ferry — "
                "still gets no wharf. SINCE T-0107 THE TEST RUNS ON EVERY RIVER "
                "FRONTAGE IN THE TOWN, WHICHEVER BANK IT STANDS ON. T-0062 "
                "stated its docks on South Water merchants, so the other two "
                "shores were never asked: the North Division shore carried a "
                "wharf only because Kinzie & Hunter's dock is attested, and the "
                "WEST bank at Wolf Point carried none at all — which was a fact "
                "about which records had been edited, not a finding about Wolf "
                "Point. On the west bank the trade test selects exactly one "
                "record, Robert A. Kinzie's storehouse; the row's other four — "
                "Wentworth's tavern, James Kinzie's residence, the Robinson and "
                "Caldwell cabins and Father Walker's log meeting house — state "
                "no dock and get none, because lodging, dwelling and worship "
                "take nothing off a canoe. Read the clauses and their reasons in "
                "tools/generate_river_wharves.py."
            ),
            "dock_grades": list(DOCK_GRADES),
            "afloat_clause": (
                "CLAUSE 6, ADDED BY T-0107: the deck's face must stand in water "
                "along its whole run, sampled at about 1 m on the committed "
                "heightfield, and a face that would stand on dry ground is "
                "refused with the measured rise on the record. The deck outline "
                "is a rectangle set on the bank's own tangent — one standard "
                "form, so its dimensions are invented once (L132) rather than "
                "once per site — and THE BANK BENDS, at Wolf Point and again in "
                "the wedge where Lake Street runs out at the South Branch, so a "
                "rectangle run against the curve can put the far end of its face "
                "behind the bank. PR #258 measured that at Hogan's store (1.10 m "
                "of water at one end of the face, −0.34 m at the other) and "
                "refused it rather than invent a bespoke outline for one "
                "frontage; this clause is that refusal made a rule. It refuses "
                "nothing in the town as it stands — every drawn face is afloat "
                "by more than a metre, the least of them 1.06 m at Robert "
                "Kinzie's — so it is proved on constructed frontages instead: "
                "`python3 tools/generate_river_wharves.py --selftest`, which "
                "`--check` runs, and which tools/check.sh already invokes."
            ),
        },
        "form": {
            "face_out_m": {
                "value": FACE_OUT_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. The deck's face stands 6.0 m beyond the traced 1834 "
                    "bank line. No source gives the reach of either dock. What "
                    "bounds it is the bed this project has already modelled: at "
                    "6 m out the channel gives about 1.2 m of water at both sites "
                    "(measured per wharf in depth_at_face_m), so a lighter or a "
                    "scow lies at the face and a loaded lake schooner does not — "
                    "the restrained reading, chosen because a longer deck would be "
                    "a claim about the river trade's tonnage as well as about the "
                    "dock. THE DEPTH IS REPORTED RATHER THAN ASSUMED so that what "
                    "the invented reach implies is on the record and not in "
                    "somebody's head."
                ),
            },
            "heel_in_m": {
                "value": HEEL_IN_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. The deck's landward edge ties 2.0 m back into the "
                    "bank, so the platform meets ground rather than ending on the "
                    "waterline. Nothing attests it; it is the least that reads as "
                    "a wharf built off a bank instead of a raft moored against one."
                ),
            },
            "apron_m": {
                "value": APRON_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. The deck runs 3.0 m past the building's river wall "
                    "at each end, so its length is the frontage it serves plus "
                    "6.0 m. No source gives a length. The bound is the building: a "
                    "dock belonging to one warehouse is about as long as the "
                    "warehouse, with enough deck past the doors to work a cargo "
                    "round it."
                ),
            },
            "deck_thickness_m": {
                "value": DECK_T_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. A 0.14 m plank deck — the same course this project "
                    "already uses for sawn boards (CLAPBOARD_COURSE_M in three "
                    "archetypes, docs/RESEARCH/materials.md). No plank in any "
                    "Chicago dock is described anywhere this project has reached."
                ),
            },
            "freeboard_m": {
                "value": FREEBOARD_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED, AND IT IS A FLOOR RATHER THAN A HEIGHT. The deck "
                    "top is the GROUND'S OWN height along the landward edge, "
                    "sampled from the terrain by the renderer — the bridge deck's "
                    "lesson (T-0001), where a height authored beside the mesh "
                    "instead of taken from it put a walker 1.8 m over the planks. "
                    "Where the bank is lower than 0.90 m above the water plane, "
                    "which it is at both of these sites, the deck holds 0.90 m "
                    "instead: a working deck stands clear of its own river, and "
                    "this project's water surface is a summer-1835 mean with no "
                    "stage record behind it (data/datum.json § vertical). Nothing "
                    "attests the figure."
                ),
            },
            "crib_width_m": {
                "value": CRIB_W_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. The deck stands on a timber crib 1.20 m thick under "
                    "its outer face and its two ends, stepped down to the bed the "
                    "heightfield gives at each bent. Crib construction is what "
                    "this project already models on the harbour works "
                    "(generators/archetypes/pier_crib.py, docs/RESEARCH/"
                    "north_pier.md), so the town has one way of standing timber in "
                    "water rather than two; no source says either river dock was "
                    "built that way. NO STONE FILL IS DRAWN: a crib is a box of "
                    "timber filled with rubble and the fill is not visible from "
                    "outside it, so drawing it would spend triangles on a claim "
                    "nobody can see."
                ),
            },
            "post_side_m": {
                "value": POST_SIDE_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. Three snubbing posts stand along each face, 0.22 m "
                    "square. Nothing attests a post, its spacing or its size. A "
                    "vessel makes fast to something, and a deck with nothing to "
                    "make fast to reads as a platform rather than as a dock."
                ),
            },
            "post_height_m": {
                "value": POST_HEIGHT_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED. 0.75 m proud of the deck, which is a working height "
                    "for a line rather than a measurement of anything."
                ),
            },
        },
        "geometry_note": (
            "The record owns the OUTLINE — where the deck stands, how long and "
            "how wide it is, and the figures above. How that outline becomes "
            "triangles is the renderer's: how many bents the crib is stepped "
            "into, where the three posts stand along the face, and the timber's "
            "tone are in renderers/web/js/wharves.js, the same division "
            "data/yard/ makes with yard.js. THE DECK'S HEIGHT IS NEITHER'S: it "
            "is the terrain's, sampled at the landward edge at load."
        ),
        "not_drawn": (
            "NO VESSEL, NO CARGO, NO CRANE, NO GANGWAY AND NO NAME. The schooner "
            "Illinois was cheered at one of these two wharves in July 1834 and is "
            "not drawn at either: this project holds no description of any vessel "
            "in Chicago at the scene date, and a hull is a larger invention than "
            "the deck it would lie at. Goods are drawn only where the yard layer's "
            "own rule puts them (data/yard/), which is on the town's trading "
            "frontages and not out here."
        ),
        "wharves": wharves,
        "refused": refused,
        "research_note": (
            "WHAT WOULD MOVE ANY OF THIS OFF RECONSTRUCTION: the Chicago Democrat's "
            "advertising columns, where a forwarding house states its street and "
            "sometimes its wharf; the harbour engineers' reports of 1833-1836, "
            "which measure the river's depth and might carry a private wharf line; "
            "a marine list giving the Illinois's draught, which would say whether "
            "she could have lain at a face in 1.2 m of water or was warped in to a "
            "deeper one; or the c. 1835 view that docs/research/03-structures-"
            "north.md describes and this project has never been able to cite. Any "
            "of them would also bear on L66's open question, which is which BANK "
            "each of these two warehouses stood on."
        ),
    }


# --- proving the clauses fire ---------------------------------------------- #
#
# CLAUSE 6 REFUSES NOTHING IN THE TOWN AS IT STANDS. Every drawn face is afloat
# by more than a metre, so on the committed data the new clause is indistinguishable
# from no clause at all — and a refusal nobody has ever seen work is a refusal this
# project has only been told about. So the clause table is fired here on frontages
# built for it: a straight bank, a flat bed, and one thing wrong at a time. It runs
# inside `--check`, which `tools/check.sh` already invokes, so it costs no new gate
# and cannot rot unnoticed.


class _StubBed:
    """A constructed bed: flat water, optionally dry or unmodelled past a line."""

    def __init__(self, depth=1.2, dry_from_n=None, dry_to_n=None, rise=0.35,
                 uncovered_from_n=None):
        self.depth, self.rise = depth, rise
        self.dry_from_n, self.dry_to_n = dry_from_n, dry_to_n
        self.uncovered_from_n = uncovered_from_n

    def covers(self, e, n):
        return self.uncovered_from_n is None or n < self.uncovered_from_n

    def height(self, e, n):
        if self.dry_from_n is not None and n >= self.dry_from_n and (
                self.dry_to_n is None or n <= self.dry_to_n):
            return self.rise                 # ground standing above the water plane
        return -self.depth


_TEST_BANK = [{
    "name": "self-test bank", "confidence": "reconstructed", "sources": [],
    "points": [(0.0, -100.0), (0.0, 100.0)],
}]


def _stand(local_n=0.0, frontage=7.0, grade="reconstructed", dock=True):
    """A frontage whose river wall stands 12 m west of the self-test bank."""
    sc = {"name": "self-test frontage", "attributes": {},
          "placement": {"local_e": -18.0, "local_n": local_n, "rotation_deg": 90.0},
          "footprint": {"polygon": [[0, 0], [frontage, 0], [frontage, 6], [0, 6]]}}
    if dock:
        sc["attributes"]["dock"] = {"value": True, "confidence": grade, "sources": []}
    return sc


def selftest() -> int:
    cases = [
        # (label, sidecar, bed, expected kind, a phrase the reason must carry)
        ("a frontage in open water is drawn",
         _stand(), _StubBed(), "wharf", None),
        ("CLAUSE 6: a face that runs onto dry ground at its end is refused",
         _stand(), _StubBed(dry_from_n=2.0), "refused", "dry ground"),
        ("CLAUSE 6: and a dry patch BETWEEN the reported three is refused too",
         _stand(), _StubBed(dry_from_n=0.5, dry_to_n=1.5), "refused", "dry ground"),
        ("CLAUSE 5: a face off the modelled ground is refused",
         _stand(), _StubBed(uncovered_from_n=2.0), "refused", "modelled ground"),
        ("CLAUSE 4b: a deck running past the trace's end is refused",
         _stand(local_n=99.0), _StubBed(), "refused", "traced 1834 bank"),
        ("CLAUSE 2: a dock graded outside the confidence model is refused",
         _stand(grade="probably"), _StubBed(), "refused", "not a grade"),
        ("CLAUSE 1: a record that states no dock is not a candidate",
         _stand(dock=False), _StubBed(), None, None),
    ]
    bad = 0
    for label, sc, bed, want, phrase in cases:
        kind, row = derive_one("selftest_frontage", sc, _TEST_BANK, bed)
        ok = kind == want and (phrase is None or phrase in (row or {}).get("why", ""))
        detail = (row or {}).get("why", "") if kind == "refused" else (
            f"least {row['least_depth_at_face_m']} m over {row['face_stations']} "
            f"station(s)" if kind == "wharf" else "not a candidate")
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}\n          {detail[:150]}")
        if not ok:
            bad += 1
    # The density itself is the claim in case 3: with the three points the record
    # reports — the face's ends and its middle — that bed reads as open water.
    bed = _StubBed(dry_from_n=0.5, dry_to_n=1.5)
    three_look_wet = all(bed.height(6.0, n) < 0 for n in (-10.0, -3.5, 3.0))
    print(f"  {'ok  ' if three_look_wet else 'FAIL'}  and the three reported points "
          f"read that bed as open water, which is why the run is sampled at 1 m")
    if not three_look_wet:
        bad += 1
    print("WHARF CLAUSES PASS" if not bad else f"WHARF CLAUSES FAIL — {bad} case(s)")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    ap.add_argument("--selftest", action="store_true",
                    help="fire the refusal clauses on constructed frontages")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    wharves, refused = build_record()
    text = json.dumps(record(wharves, refused), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists():
            print(f"WHARF DRIFT\n  - {OUT.relative_to(ROOT)} is missing")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"WHARF DRIFT\n  - {OUT.relative_to(ROOT)} has drifted from the rule "
                  f"in tools/generate_river_wharves.py")
            return 1
        print(f"verified {len(wharves)} river wharf/wharves "
              f"({len(refused)} frontage(s) refused with a reason)")
        return selftest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(wharves)} river wharf/wharves "
          f"({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
