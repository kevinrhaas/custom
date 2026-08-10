"""bridge_timber — the log bridges over the branches of the Chicago River.

The North Branch bridge (winter 1831-32) and the Lake Street raft bridge over the South
Branch (winter 1832-33) are described in the same two numbers: **about 10 ft wide,
clearing the water by about 6 ft**, of logs. This archetype builds the fixed, piered
form — stringers on cribs or piles, carrying a puncheon deck. The floating raft is a
different structure and gets its own archetype; see bridge_timber_params for why
pointing a raft at this one would be a false claim of solidity.

The north-branch bridge is documented in 1832-33 as "formed of stringers and only
fitted for foot passengers" and "useless for teams", yet on 18 Aug 1835 it carried the
war-dance procession — hundreds of people at once. Something happened in between and
nothing records what. The archetype's defaults build the *later* reading, because the
scene date is 1835-07-01: four stringers rather than two, a full plank deck rather than
a walkway. Both of those are `inferred` at best and the records should say so.

## Railings: deliberately none

**Decision: no railing, and the parameter defaults to False.** The reasoning, recorded
here because the absence is as much a claim as a presence would be:

- No source reached attests a railing on either log bridge. The dossier's crossing
  table gives width, clearance and construction and nothing else.
- The one qualitative description we have runs the other way. "Formed of stringers and
  only fitted for foot passengers" and "useless for teams" describe something closer to
  a causeway of logs than to a piece of civil engineering, and a railing is the part
  you add when you have finished the parts that hold the bridge up.
- A railing is unusually load-bearing visually. A railed bridge reads as considered
  infrastructure; an unrailed one reads as a plank over water. Adding one to look
  finished would change what a visitor believes about how developed the town was, which
  is precisely the kind of silent gap-filling AGENTS.md rule 2 forbids.
- The counter-argument, stated so it is on the record: the 1834 Dearborn Street
  drawbridge was a real piece of engineering and the town clearly could build one, and
  a procession of hundreds crossing a 6-ft-high unrailed deck is an alarming picture.
  That is an argument for the 1835 rebuild having been substantial — not evidence about
  a railing. If a source turns up, set `railing: true` on the record with its own
  confidence; the geometry is written and will build at `conjectural` until something
  better exists.

## Local origin: z = 0 is the water, not the ground

docs/GLB-CONTRACT.md pins a structure's local origin to "y = 0 at the base of the
walls". A bridge has no walls and its documented dimension is a clearance above the
*water*, so this archetype anchors z = 0 at the design water surface: the deck sits at
+clearance +structure, and the cribs run down through zero into the river. A renderer
placing one of these must therefore place it against the water plane, not the terrain.
That is a genuine hole in the contract rather than a deviation from it, and it is
called out in the report for this parcel.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.logwork import (  # noqa: E402
    COURSE_M, HEWN_RGBA, hewn_log_wall, log_prism,
)
from common.mesh import MeshBuilder, simple_material  # noqa: E402
from archetypes.bridge_timber_params import BridgeTimberParams  # noqa: E402

M_LOG, M_DECK, M_FILL = 0, 1, 2

PLANK_PITCH_M = 0.42      # a split puncheon, flat face up
# How far the cribs and piles run below the waterline before the mesh stops. They
# actually reached the riverbed; there is no point modelling what the water hides, and
# the renderer's water plane sits at z = 0 in this local frame.
SUBMERGED_M = 0.55

DECK_RGBA = (0.47, 0.41, 0.32, 1.0)   # weathered split-log deck, greyer than a wall log
# Crib fill: river stone and gravel, not the pale clay-and-lime that chinks a cabin.
# Reusing CHINK_RGBA here made the piers read as stacks of whitewashed slabs.
FILL_RGBA = (0.300, 0.295, 0.270, 1.0)


def build(params: BridgeTimberParams, name: str):
    """Build the bridge. Returns a Blender object at the local origin; z = 0 is the
    water surface (see the module docstring), y-up is handled by the exporter."""
    params.validate()
    b = MeshBuilder(name)

    # For a bridge the documented description IS dimensional — "about ten feet wide,
    # clearing the water by about six feet, of logs" is the whole of it — so width and
    # clearance sit in the character set that drives the deck and stringers, where a
    # building's width would not. Span and pier spacing stay out of it: nobody
    # recorded the river's width at the crossing or anything at all about the piers.
    # The rule (least-confident-wins over the attributes that say what the thing WAS)
    # is unchanged; the membership of that set is what differs. See
    # bridge_timber_params' module docstring and frame_tavern.build.
    c_struct = params.worst_conf("construction", "width_m", "clearance_m")
    c_pier = params.worst_conf("pier_kind", "pier_spacing_m")

    deck_z = params.deck_height_m
    stringer_top = deck_z - params.plank_t_m
    bearing_z = stringer_top - params.stringer_d_m      # underside = the clearance line

    _stringers(b, params, stringer_top, c_struct)
    _deck(b, params, deck_z, c_struct)

    for xp in params.pier_x:
        _pier(b, params, xp, bearing_z, c_pier)
    if params.abutments:
        _abutments(b, params, bearing_z, params.conf("abutments"))
    if params.railing:
        _railing(b, params, deck_z, params.conf("railing"))

    mats = [
        simple_material("log", HEWN_RGBA, roughness=0.93),
        simple_material("deck", DECK_RGBA, roughness=0.95),
        simple_material("fill", FILL_RGBA, roughness=0.98),
    ]
    return b.to_object(mats)


def _stringer_y(p: BridgeTimberParams) -> list[float]:
    """Stringer centre-lines across the deck.

    Inset by half a diameter, so the outermost log's outer face lands on the deck edge
    and stays visible from the bank. A deeper inset tucks the stringers entirely under
    the overhanging plank ends, which loses the only word any source gives us about
    how this bridge was built: "formed of stringers".
    """
    n = p.stringer_count
    inset = p.stringer_d_m * 0.5
    lo, hi = inset, p.width_m - inset
    if n == 1:
        return [p.width_m / 2.0]
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def _stringers(b: MeshBuilder, p: BridgeTimberParams, top_z: float,
               conf: float) -> None:
    """Round log stringers, one run per bay.

    Broken at every support rather than run continuously, because that is how a log
    bridge is built — nobody had 15 m logs — and because the butt joints over each
    bent are the detail that tells a viewer where the piers are from the bank.
    """
    r = p.stringer_d_m / 2.0
    zc = top_z - r
    edges = [0.0] + list(p.pier_x) + [p.span_m]
    for y in _stringer_y(p):
        for a, c in zip(edges, edges[1:]):
            # overlap the bearings slightly so the joints are lapped, not butted in
            # mid-air
            log_prism(b, (a - 0.18, y, zc), (c + 0.18, y, zc), r, conf, M_LOG)


def _deck(b: MeshBuilder, p: BridgeTimberParams, deck_z: float, conf: float) -> None:
    """A puncheon deck: split logs laid across the stringers, flat face up.

    Every plank is its own box. The first version was one slab with a proud face per
    plank stamped on top, which was cheaper and looked like a concrete slab scored
    with lines: the deck edge stayed dead straight, so from the bank — where anyone
    standing at the forks actually sees this bridge — there was nothing to say it was
    made of logs. Individual planks give a ragged edge of plank butts, which is the
    detail that carries the whole read. Roughly four hundred triangles on the one
    surface a visitor walks across is a fair trade.
    """
    t = p.plank_t_m
    over = 0.06                      # plank ends overhanging the outer stringers
    y0, y1 = -over, p.width_m + over

    n = max(int(p.span_m / PLANK_PITCH_M), 2)
    pitch = p.span_m / n
    gap = 0.022
    for i in range(n):
        xa, xb = i * pitch + gap / 2, (i + 1) * pitch - gap / 2
        # Split logs vary; nudging alternate ends stops the butts lining up into a
        # sawn edge. Deterministic, not random — the build has to be reproducible.
        ja = 0.035 if i % 3 == 0 else (-0.02 if i % 3 == 1 else 0.0)
        b.add_box(xa, y0 - ja, deck_z - t, xb, y1 + ja, deck_z, conf, M_DECK,
                  skip=("bottom",))


def _pier(b: MeshBuilder, p: BridgeTimberParams, xp: float, bearing_z: float,
          conf: float) -> None:
    """One intermediate support: a log crib, or a bent of driven piles."""
    if p.pier_kind == "pile":
        _pile_bent(b, p, xp, bearing_z, conf)
        return
    half = 0.58
    _crib(b, xp - half, 0.42, xp + half, p.width_m - 0.42, bearing_z, conf)
    _cap(b, p, xp, bearing_z, conf)


def _crib(b: MeshBuilder, x0: float, y0: float, x1: float, y1: float,
          top_z: float, conf: float) -> None:
    """A log crib: courses of logs laid up in alternating directions, the ends
    protruding at the corners, and the box filled with whatever came out of the river.

    Built by the same `hewn_log_wall` that builds the cabins, which is the point — a
    crib corner and a cabin corner are the same joint and should look it — but with a
    coarser course and a shallower relief. Crib logs were heavier than wall logs and
    nobody chinked them, so the line between courses is a packed seam of stone and
    gravel rather than a band of lime, and it takes the grey M_FILL rather than the
    cabins' pale clay. Reusing the cabin colour here made every pier read as a stack
    of whitewashed slabs.
    """
    hewn_log_wall(b, x0, y0, x1, y1, -SUBMERGED_M, top_z, conf, M_LOG, M_FILL,
                  skip=("bottom",), course=COURSE_M * 1.35, relief=0.016)


def _cap(b: MeshBuilder, p: BridgeTimberParams, xp: float, bearing_z: float,
         conf: float) -> None:
    """A cap log across the crib head, which is what the stringers actually bear on."""
    r = 0.17
    log_prism(b, (xp, -0.10, bearing_z - r), (xp, p.width_m + 0.10, bearing_z - r),
              r, conf, M_LOG)


def _pile_bent(b: MeshBuilder, p: BridgeTimberParams, xp: float, bearing_z: float,
               conf: float) -> None:
    """Three driven piles and a cap log. Cheaper than a crib in triangles and in
    1830s labour, and the alternative reading of "log construction" — which of the two
    either bridge actually used is unattested, so `pier_kind` is a record's choice."""
    r = 0.15
    for i in range(3):
        y = p.width_m * (i + 0.5) / 3.0
        log_prism(b, (xp, y, -SUBMERGED_M - 0.4), (xp, y, bearing_z - 0.34), r,
                  conf, M_LOG)
    _cap(b, p, xp, bearing_z, conf)


def _abutments(b: MeshBuilder, p: BridgeTimberParams, bearing_z: float,
               conf: float) -> None:
    """A crib at each bank for the end bays to land on.

    The bridge has to bear on something at the ends and no source says what, so these
    are conjectural by default and are built the same way as the piers so at least the
    invention is consistent with itself. Kept slimmer than a pier: in a scene most of
    an abutment is inside the bank, and a full-sized crib at each end made a 17 m
    bridge look like it was propped on two grain elevators.
    """
    d = 0.62
    for x0, x1 in ((-d, 0.16), (p.span_m - 0.16, p.span_m + d)):
        _crib(b, x0, 0.22, x1, p.width_m - 0.22, bearing_z, conf)


def _railing(b: MeshBuilder, p: BridgeTimberParams, deck_z: float,
             conf: float) -> None:
    """A pole rail on posts. OFF by default — see the module docstring for the
    argument, which is the substantive part of this function."""
    h, r = 0.95, 0.06
    step = max(p.span_m / max(round(p.span_m / 2.2), 1), 1.0)
    n = int(p.span_m / step)
    for y, sgn in ((0.0, -1), (p.width_m, 1)):
        yy = y + sgn * 0.05
        for i in range(n + 1):
            x = min(i * step, p.span_m)
            b.add_box(x - 0.06, yy - 0.06, deck_z, x + 0.06, yy + 0.06, deck_z + h,
                      conf, M_LOG, skip=("bottom",))
        log_prism(b, (-0.10, yy, deck_z + h - r), (p.span_m + 0.10, yy, deck_z + h - r),
                  r, conf, M_LOG)
