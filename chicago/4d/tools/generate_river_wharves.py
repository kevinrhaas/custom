#!/usr/bin/env python3
"""Derive the town's river wharves from the records that state or claim one.

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

THE RULE, and it is the whole answer to "why these frontages and no others".
It has two arms:

    STATED — a sidecar standing on the scene date whose own `dock` attribute
    is true and graded `attested` or `inferred`. The two forwarding
    warehouses, unchanged from T-0041.

    CLAIMED — a sidecar standing on the scene date whose documented FUNCTION
    is one of the river trades (`RIVER_TRADES` below), and whose river wall
    stands within `FRONTS_RIVER_M` of the traced 1834 bank. No source states
    a dock at any of these; the trade is what defends the claim, and every
    such deck is graded `reconstructed` with the owner's brief as the source
    that bounds it.

The claimed arm is T-0062, on the owner's 2026-08-18 ruling ("you can add more
docks!" — the general form of it is recorded in AGENTS.md § RECONSTRUCTED IS A
TIER). T-0041 shipped the narrower reading — stated docks only, on the argument
that a wharf on an invented dock is an invention on an invention — and the
owner overrode it: his brief's images 3 and 11
(`data/sources/assets/owner_brief_2026_08_18/README.md`) draw masts crowding
the reach below the drawbridge and the South Water bank as a continuous
working frontage, which two docks cannot carry. A TRADE RULE is how the claim
is made auditable — the same shape as the signboards' trade table and the yard
goods' ordinance rule, and it deliberately does NOT author a `dock` attribute
onto the claimed records: an attribute edit re-hashes the record's resolved
parameters and stales its committed baked mesh, which no dock can justify.
Run over the whole town the rule admits seven candidates: the two stated
docks, and five documented river-trade frontages. Four are then refused as
DRAWINGS, each with its reason in the record — Peck's, Harmon & Loomis's and
Thomas Church's because the traced south bank ends at Wells and cannot place a
deck east of it (T-0106 owns extending it; Church's would also fail the
frontage cap), and Hogan's because the bank bends at Wolf Point and the
standard outline's face runs aground there — so five wharves stand: the two
stated, J. H. Kinzie's forwarding store, Jones's grocery and provision store,
and Robert Kinzie's store on the west bank. Everything else on the river is
still refused.

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

# The grades under which a statement is EVIDENCE rather than an invention.
# They gate both arms of the rule: a dock attribute must carry one to be a
# stated dock, and a trade must carry one before it can claim a dock — a
# reconstructed shop with a reconstructed trade growing a dock would be an
# invention on an invention on an invention.
DOCK_GRADES = ("attested", "documented", "inferred")

# The trades that claim a landing (T-0062, the owner's 2026-08-18 override).
# A forwarding or commission house works other men's cargo over the bank; a
# grocery and provision store or a general merchant received nearly everything
# it sold off a vessel. What is NOT here is as deliberate as what is: the drug
# stores, the printing offices, the taverns and every dwelling on the same
# frontage claim nothing, because their business does not defend the claim.
RIVER_TRADES = frozenset({
    "forwarding_and_commission_store",
    "grocery_and_provision_store",
    "store",
    "store_and_dwelling",
})

# INVENTED, with its bound stated in the record's form block: how far a claimed
# frontage's river wall may stand from the traced bank and still be read as
# working over it — the platted street between the row and the water plus the
# bank strip. The four candidates the rule admits today stand 11-40 m out; the
# nearest it refuses stands 61 m and a block inland.
FRONTS_RIVER_M = 45.0

# The source that bounds every claimed dock: the owner's 2026-08-18 brief
# (images 3 and 11 — masts crowding the reach below the drawbridge, the South
# Water bank a continuous working frontage) and its standing ruling.
OWNER_SPEC = "owner_chicago_1835_reconstruction_spec_2026"

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


def nearest_on(points: list, p: tuple) -> tuple[float, tuple, tuple]:
    """(distance, foot point, unit tangent) for the nearest segment of a polyline."""
    best = None
    for a, b in zip(points, points[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx
                                                   + (p[1] - a[1]) * dy) / L2))
        q = (a[0] + t * dx, a[1] + t * dy)
        d = math.hypot(p[0] - q[0], p[1] - q[1])
        if best is None or d < best[0]:
            L = math.sqrt(L2) or 1.0
            best = (d, q, (dx / L, dy / L))
    return best


def _stand_wharf(sid: str, sc: dict, banks: list, field, refused: list,
                 cap_m: float | None = None) -> dict | None:
    """Derive one deck outline, or record exactly why none can stand here.

    The geometry is one derivation for both arms of the rule — a stated dock
    and a claimed one differ in what ADMITS them, never in how the deck is
    stood — so it lives in one function and cannot come to disagree with
    itself. Returns the wharf's geometric fields, or None with the refusal
    appended.
    """
    place = sc.get("placement") or {}
    poly = (sc.get("footprint") or {}).get("polygon") or []
    if len(poly) < 3:
        refused.append({"structure_id": sid,
                        "why": "no footprint polygon — no wall to serve."})
        return None                                          # no wall
    u0, u1, vmax = _front_edge(poly)
    wall_a = _to_enu(u0, vmax, place)
    wall_b = _to_enu(u1, vmax, place)
    mid = ((wall_a[0] + wall_b[0]) / 2.0, (wall_a[1] + wall_b[1]) / 2.0)
    frontage = math.hypot(wall_b[0] - wall_a[0], wall_b[1] - wall_a[1])

    near = [(nearest_on(b["points"], mid), b) for b in banks]
    (dist, foot, tangent), bank = min(near, key=lambda r: r[0][0])

    # The traced bank has to actually REACH the frontage it would serve. Past
    # the trace's own terminus the nearest point is that terminus for every
    # building beyond it, so two docks east of the end would be drawn standing
    # on one another at the trace's last vertex — which is how T-0062 found
    # this clause: the south-bank trace ends at Wells (local e ≈ 390) and both
    # Peck's and Harmon & Loomis's decks landed on the same foot. A dock past
    # the trace is not refused as a claim, only as a drawing: extending the
    # traced 1834 bank is what draws it (T-0106), not a different rule.
    ends = (bank["points"][0], bank["points"][-1])
    if min(math.hypot(foot[0] - p[0], foot[1] - p[1]) for p in ends) < 0.5:
        refused.append({"structure_id": sid, "why": (
            "the traced 1834 bank does not reach this frontage — its nearest "
            "point is the trace's own end, so the deck's place on the river "
            "cannot be derived. Extending the committed bank trace is what "
            "draws this dock (T-0106), not a different rule.")})
        return None                                          # bank reach

    # A claimed dock has to FRONT the water it would work: a store a street's
    # width from the bank trades over that bank, a store a block inland trades
    # over a road. The stated docks carry no cap — their sentence puts them at
    # the river wherever the record stands.
    if cap_m is not None and dist > cap_m:
        refused.append({"structure_id": sid, "why": (
            f"its river wall stands {dist:.1f} m from the traced bank, past "
            f"the {cap_m:.0f} m a working frontage spans (the street and the "
            "bank strip). A store this far inland trades over a road, and a "
            "dock is not claimed for it.")})
        return None                                          # fronts the river
    # Outward is across the bank, away from the building it serves. Deriving
    # it from the building rather than from the polygon's winding is what
    # keeps a wharf on the water when a bank line is re-traced the other way.
    nx, ny = -tangent[1], tangent[0]
    if (foot[0] - mid[0]) * nx + (foot[1] - mid[1]) * ny < 0:
        nx, ny = -nx, -ny

    half = frontage / 2.0 + APRON_M
    heel = (foot[0] - nx * HEEL_IN_M, foot[1] - ny * HEEL_IN_M)
    face = (foot[0] + nx * FACE_OUT_M, foot[1] + ny * FACE_OUT_M)
    corners = [                       # heel-left, heel-right, face-right, face-left
        (heel[0] - tangent[0] * half, heel[1] - tangent[1] * half),
        (heel[0] + tangent[0] * half, heel[1] + tangent[1] * half),
        (face[0] + tangent[0] * half, face[1] + tangent[1] * half),
        (face[0] - tangent[0] * half, face[1] - tangent[1] * half),
    ]

    # The deck may not reach the building it serves: a wharf that laps a wall
    # is a modelling error wearing a wharf's clothes, and the two stated
    # placements were authored with exactly this strip left clear ("about 8 m
    # back from the traced bank to leave the dock its ground"; "about 14 m
    # back ... so the strip between it and the water can carry the dock").
    clearance = min(nearest_on([wall_a, wall_b], c)[0] for c in corners[:2])
    if clearance < 1.0:
        refused.append({"structure_id": sid, "why": (
            f"its heel would come within {clearance:.2f} m of the building's "
            "own river wall. A wharf that laps the wall it serves is a "
            "modelling error, and this record refuses to draw one.")})
        return None                                          # wall clearance

    # What the invented outline implies, measured on the committed bed rather
    # than assumed: how much water a vessel lying at this face would have.
    depths = []
    for t in (-half, 0.0, half):
        e = face[0] + tangent[0] * t
        n = face[1] + tangent[1] * t
        depths.append(-field.height(e, n) if field and field.covers(e, n) else None)
    if any(d is None for d in depths):
        refused.append({"structure_id": sid, "why": (
            "its face falls outside the modelled ground, so the depth at it "
            "cannot be measured and the wharf is not drawn.")})
        return None                                          # measurable depth

    # And the face has to be wholly over water. Where the bank bends — Wolf
    # Point found this — the standard outline's apron can land one end of the
    # face on dry ground, and a dock run aground is not a dock. The record
    # refuses the standard form rather than inventing a bespoke one: a deck
    # shaped to this bend would be a further invention, and it can be its own
    # parcel if the frontage earns it.
    if min(depths) <= 0.0:
        refused.append({"structure_id": sid, "why": (
            f"its face would run aground — the modelled bed at the face's run "
            f"gives {', '.join(f'{d:.2f}' for d in depths)} m of water, and a "
            "deck whose face ends on dry ground is not a dock. The bank bends "
            "here; the standard outline does not, and no bespoke one is "
            "invented for it.")})
        return None                                          # face afloat

    return {
        "structure_id": sid,
        "name": sc.get("name"),
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
        sc = _load(path)
        attrs = sc.get("attributes") or {}

        # ---- the stated arm: the record's own dock attribute --------------- #
        dock = attrs.get("dock")
        if isinstance(dock, dict) and dock.get("value"):
            grade = dock.get("confidence")
            if grade not in DOCK_GRADES:
                refused.append({"structure_id": sid, "why": (
                    f"its dock attribute is graded {grade}, and only a STATED "
                    "dock (attested, documented, inferred) enters by attribute. "
                    "A claimed dock enters by the trade rule below (T-0062) — "
                    "not by authoring the attribute, which is also what keeps a "
                    "record's baked mesh out of the claim's blast radius.")})
                continue
            w = _stand_wharf(sid, sc, banks, field, refused)
            if w is None:
                continue
            w.update({
                "dock_confidence": grade,
                "dock_sources": dock.get("sources") or [],
            })
            wharves.append(w)
            continue

        # ---- the claimed arm: the river-trade rule (T-0062) ---------------- #
        # A dock nobody stated, claimed for a frontage because its DOCUMENTED
        # trade worked over this bank — the same shape of reconstruction as the
        # signboards' trade table and the yard goods' ordinance rule. Two
        # clauses admit a candidate: the sidecar's own function is one of the
        # river trades, and that function is itself evidence rather than an
        # invention — a reconstructed shop with a reconstructed trade growing a
        # dock would be an invention on an invention on an invention.
        fn = attrs.get("function") or {}
        if fn.get("value") not in RIVER_TRADES:
            continue
        if fn.get("confidence") not in DOCK_GRADES:
            continue        # an invented trade claims nothing
        w = _stand_wharf(sid, sc, banks, field, refused, cap_m=FRONTS_RIVER_M)
        if w is None:
            continue
        w.update({
            "dock_confidence": "reconstructed",
            "dock_sources": [OWNER_SPEC],
            "claimed_by": "river_trade_rule",
            "trade": fn.get("value"),
            "trade_confidence": fn.get("confidence"),
        })
        wharves.append(w)

    wharves.sort(key=lambda w: w["structure_id"])
    refused.sort(key=lambda r: r["structure_id"])
    return wharves, refused


def record(wharves: list, refused: list) -> dict:
    return {
        "_doc": (
            "The town's river wharves — a plank deck on timber cribs at each "
            "frontage whose own record states a dock (the two forwarding "
            "warehouses) or whose documented river trade claims one under the "
            "T-0062 rule (the working stores at the forks and along South "
            "Water). NOT structure records and NOT geometry that comes out of "
            "Blender: a deck on cribs "
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
        "name": "The river wharves: the forwarding warehouses and the traders' landings",
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
            "sources": ["andreas_1884_v1",
                        "owner_chicago_1835_reconstruction_spec_2026"],
            "note": (
                "TWO OF THESE DOCKS ARE STATED AND THE REST ARE CLAIMED, AND "
                "EVERY DIMENSION OF ALL OF THEM IS INVENTED. What is held for "
                "the stated pair: docs/research/03-structures-north.md §3.10 — "
                "'Kinzie & Hunter and Dole & Newberry each had a warehouse WITH "
                "ITS DOCK ALONG THE RIVER FRONT' — which is the clause that "
                "attests the Kinzie & Hunter building at all; and Andreas "
                "independently names 'Newberry & Dole's wharf' as the place the "
                "schooner Illinois, the first vessel through the new cut, was "
                "cheered on 12 July 1834 (scan p. 503). The traders' landings "
                "(T-0062) rest on no such sentence: each is claimed by a rule "
                "about trades, on the owner's 2026-08-18 ruling and his brief's "
                "two river views (images 3 and 11 — masts crowding the reach "
                "below the drawbridge, the bank a continuous working frontage). "
                "A frontage whose documented business is forwarding, commission, "
                "provisions or general merchandise worked over this bank, so the "
                "rule claims it a landing; docs/LIBERTIES.md L145 records the "
                "invention and its bounds. What is NOT held, anywhere in this "
                "project: the length, the width, the height, the construction or "
                "the condition of any dock on this river. NOTHING HERE IS "
                "PROMOTED ABOVE reconstructed: a dock is stated or defensibly "
                "claimed, and this is what a dock is drawn as."
            ),
        },
        "rule": {
            "note": (
                "Two arms. STATED: a sidecar standing on the scene date whose "
                "own `dock` attribute is true and graded attested or inferred — "
                "the two forwarding warehouses, unchanged from T-0041. CLAIMED "
                "(T-0062): a sidecar whose documented function is one of the "
                "river trades below and whose river wall stands within "
                "fronts_river_m of the traced 1834 bank — no source states a "
                "dock at any of these, and the trade is what defends the claim. "
                "Run over the whole town the two arms admit seven candidates; "
                "four are refused as drawings with their reasons in this "
                "record's refused list (three because the traced south bank "
                "ends at Wells and cannot place a deck east of it — T-0106 — "
                "and one because the bank bends at Wolf Point and the standard "
                "outline's face runs aground), so five wharves stand. "
                "Everything else on the river is still refused: the lumber "
                "landing, the ferry, the anonymous row, every invented shop — a "
                "reconstructed trade claims nothing. Read the clauses and their "
                "reasons in tools/generate_river_wharves.py."
            ),
            "dock_grades": list(DOCK_GRADES),
            "claimed_trades": sorted(RIVER_TRADES),
            "fronts_river_m": FRONTS_RIVER_M,
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
            "fronts_river_m": {
                "value": FRONTS_RIVER_M,
                "confidence": "reconstructed",
                "note": (
                    "INVENTED, AND IT GATES THE CLAIMED ARM ONLY. How far a "
                    "claimed frontage's river wall may stand from the traced "
                    "bank and still be read as working over it: the platted "
                    "street between the row and the water plus the bank strip. "
                    "The candidates the rule admits today stand 11-40 m out and "
                    "the nearest it refuses stands 61 m and a block inland, so "
                    "the figure separates the two populations with margin on "
                    "both sides. A stated dock carries no cap — its sentence "
                    "puts it at the river wherever the record stands."
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
            "Illinois was cheered at one of the two stated wharves in July 1834 and is "
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff, write nothing")
    args = ap.parse_args()
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
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(wharves)} river wharf/wharves "
          f"({len(refused)} refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
