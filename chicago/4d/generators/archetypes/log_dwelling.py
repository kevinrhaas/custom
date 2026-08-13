"""log_dwelling — a hewn-log building, optionally with a frame addition and a sign.

The commonest building at the forks in 1835 and therefore the archetype that most of
the town will be made of. It has to cover three attested cases without becoming a
kit-of-parts: Wolf Point Tavern (log core, frame extension, painted wolf sign hung
outside by about 1833), Samuel Miller's house (log cabin with a two-storey frame
addition fronting the river) and Rev. Jesse Walker's meeting house ("a small square
log building, originally designed for a school-house" — Wau-Bun). Evidence and its
disagreements: docs/research/03-structures-north.md §2.1, §2.2, §3.1.

**Orientation.** The facade faces NORTH at rotation_deg 0, per the pinned convention
in docs/GLB-CONTRACT.md. In Blender that is the +y face, because the exporter's
`export_yup=True` maps Blender +Y to glTF -Z, which the contract defines as north. The
door, the sign and any front addition are all on +y. Getting this wrong is a silent
error — the building looks fine and faces the wrong way — so it is stated here as well
as in the contract.

**The sign is a board, not a picture.** The wolf sign is documented; what the painted
wolf looked like is not, and no image of it survives. So the geometry is a signboard
hanging from a bracket, and the `sign` parameter carries the *subject* as a string for
the sidecar to report. Painting a wolf on it would be manufacturing evidence in exactly
the way AGENTS.md rule 1 forbids, and it would be the most-photographed invention in
the scene.

**Log courses and corner notching** come from common/logwork.py, which is
frame_tavern._log_wing's visual language factored out. That is deliberate: the
Sauganash's log wing and the Wolf Point Tavern were built by the same handful of people
within a couple of years of each other, and they should look it.

**A note on face winding.** Every quad here is wound so its normal points out of the
building. Blender's exporter writes `doubleSided: true` for a default material, so a
reversed face is invisible today — but the contract says counter-clockwise and outward,
the palette/meshopt steps are entitled to rely on it, and a renderer that ever enables
culling would find holes rather than a bug report. `_panel` exists so no recessed
opening can get this wrong by hand.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.logwork import (  # noqa: E402
    CHINK_RGBA, HEWN_RGBA, RELIEF_M, hewn_log_wall,
)
from common.mesh import (  # noqa: E402
    PAINT_RGBA, ROOF_RGBA, MeshBuilder, simple_material,
)
from archetypes.log_dwelling_params import LogDwellingParams  # noqa: E402

# Materials are indices into the list passed to to_object(), in this order.
M_LOG, M_CHINK, M_ROOF, M_FRAME, M_DARK, M_SIGN = 0, 1, 2, 3, 4, 5

CLAPBOARD_COURSE_M = 0.14   # exposed face of a period clapboard, ~5.5 in
# A weathered board, left deliberately neutral. What colour the Wolf Point signboard
# was painted is unattested; a neutral board makes a claim about as small as geometry
# can make while still being visible.
SIGN_RGBA = (0.60, 0.54, 0.44, 1.0)


def build(params: LogDwellingParams, name: str):
    """Build the dwelling. Returns a Blender object at the local origin, y-up handled
    by the exporter (Blender is z-up internally)."""
    params.validate()
    b = MeshBuilder(name)

    # Massing takes the confidence of the attributes that say what the building WAS,
    # not the precision of its dimensions. The reasoning is set out at length in
    # frame_tavern.build and is not repeated here; the short form is that an unknown
    # size and an unknown form are different kinds of not-knowing, and dithering a
    # well-attested building into ghost massing because nobody wrote down its width
    # misrepresents the evidence in the direction of false modesty.
    #
    # For a log building the construction IS the cladding, so where frame_tavern
    # reads ("stories", "construction", "cladding") this reads ("stories",
    # "construction") — there is no third attribute, not an omission.
    c_mass = params.worst_conf("stories", "construction")
    c_roof = params.worst_conf("roof_type", "roof_pitch_deg")

    # Where the log core sits inside the footprint once the addition is carved out.
    cx0, cy0, cx1, cy1 = _core_extent(params)
    wall_z = params.wall_height_m

    hewn_log_wall(b, cx0, cy0, cx1, cy1, 0.0, wall_z, c_mass, M_LOG, M_CHINK,
                  skip=("bottom", "top"))

    ridge_z = _roof(b, params, cx0, cy0, cx1, cy1, wall_z, c_roof)

    if params.loft:
        _loft_opening(b, params, cx0, cy0, cx1, cy1, wall_z, ridge_z,
                      params.conf("loft"))

    _core_openings(b, params, cx0, cy0, cx1, cy1, wall_z,
                   params.conf("fenestration", "reconstructed"))

    addition_ridge_z = _frame_addition(b, params) if params.frame_addition else None

    _chimneys(b, params, cx0, cy0, cx1, cy1, ridge_z, addition_ridge_z,
              params.conf("chimneys", "reconstructed"))

    if params.sign:
        # The BOARD's confidence is the confidence that a sign hung there. Its size
        # and its bracket are invented, but those are dimensional, and by the
        # convention above dimensions do not drag an object's character down.
        _sign(b, params, params.conf("sign", "reconstructed"))

    mats = [
        simple_material("log", HEWN_RGBA, roughness=0.92),
        simple_material("chinking", CHINK_RGBA, roughness=0.95),
        simple_material("roof", ROOF_RGBA, roughness=0.9),
        simple_material("frame",
                        PAINT_RGBA.get(params.frame_paint, PAINT_RGBA["unpainted"])),
        simple_material("dark", (0.07, 0.08, 0.09, 1.0), roughness=0.4),
        simple_material("sign", SIGN_RGBA, roughness=0.85),
    ]
    return b.to_object(mats)


# ---------------------------------------------------------------- plan geometry

def _core_extent(p: LogDwellingParams) -> tuple[float, float, float, float]:
    """The log core's rectangle inside the footprint bbox.

    The addition is carved OUT of the footprint rather than bolted onto it, so the
    whole building stays inside the polygon the record actually attests. See the
    dataclass docstring in log_dwelling_params.
    """
    w, d = p.width_m, p.depth_m
    if not p.frame_addition:
        return 0.0, 0.0, w, d
    if p.frame_addition_side == "end":
        return 0.0, 0.0, w - p.frame_addition_width_m, d
    return 0.0, 0.0, w, d - p.frame_addition_depth_m


def _addition_extent(p: LogDwellingParams) -> tuple[float, float, float, float]:
    """The frame addition's rectangle. `front` is centred on the facade; `end` runs
    to the +x edge and aligns its front wall with the core's."""
    w, d = p.width_m, p.depth_m
    fw, fd = p.frame_addition_width_m, p.frame_addition_depth_m
    if p.frame_addition_side == "end":
        return w - fw, max(d - fd, 0.0), w, d
    x0 = (w - fw) / 2.0
    return x0, d - fd, x0 + fw, d


def _ridge_along_x(x0, y0, x1, y1) -> bool:
    return (x1 - x0) >= (y1 - y0)


# ------------------------------------------------------------------ primitives

def _panel(b: MeshBuilder, axis: str, plane: float, u0: float, u1: float,
           z0: float, z1: float, outward: int, conf: float, mat: int) -> None:
    """One flat rectangle on an axis-aligned plane, wound to face `outward`.

    `axis` names the plane's normal axis ('x' or 'y'); `u0`/`u1` run along the other
    horizontal axis. Every recess in this module goes through here so none of them can
    end up facing into the building.
    """
    if axis == "y":
        pts = [(u0, plane, z0), (u1, plane, z0), (u1, plane, z1), (u0, plane, z1)]
        natural = -1          # this order's normal points -y
    else:
        pts = [(plane, u0, z0), (plane, u1, z0), (plane, u1, z1), (plane, u0, z1)]
        natural = 1           # this order's normal points +x
    if outward != natural:
        pts.reverse()
    b.add_poly(pts, conf, mat)


def _opening(b: MeshBuilder, axis: str, plane: float, u0: float, u1: float,
             z0: float, z1: float, outward: int, conf: float,
             surround: int = M_FRAME, relief: float = RELIEF_M) -> None:
    """A door or window: a dark opening inside a sawn surround.

    The surround is not decoration. An opening drawn as a bare dark rectangle has to
    sit proud of the log faces to be visible at all, which makes it read as a plaque
    glued to the wall — the first version of this looked exactly like that. A log wall
    cannot have a hole in it without sawn jambs and a head to carry the cut courses,
    so the surround is both the honest detail and the thing that makes the opening
    read as a hole. Two quads, four triangles.

    Both are flat, so the dark panel has to sit very slightly IN FRONT of the surround
    rather than recessed into it — it is entirely inside the surround's outline and
    would otherwise be hidden by it. Six millimetres: enough to order the two reliably,
    little enough that the glass does not visibly bulge out of its own frame.
    """
    off = relief + 0.010
    m = 0.085
    _panel(b, axis, plane + outward * off, u0 - m, u1 + m, z0 - m, z1 + m,
           outward, conf, surround)
    _panel(b, axis, plane + outward * (off + 0.006), u0, u1, z0, z1,
           outward, conf, M_DARK)


def _plate(b: MeshBuilder, x: float, half: float, pts_yz, conf: float,
           mat: int) -> None:
    """A thin flat member lying in a y-z plane, extruded +-`half` in x.

    Both faces and all edges are emitted with outward winding, so a brace read from
    behind is still solid. `pts_yz` is a polygon in (y, z), counter-clockwise as seen
    from +x.
    """
    n = len(pts_yz)
    b.add_poly([(x + half, y, z) for y, z in pts_yz], conf, mat)
    b.add_poly([(x - half, y, z) for y, z in reversed(pts_yz)], conf, mat)
    for i in range(n):
        (ya, za), (yb, zb) = pts_yz[i], pts_yz[(i + 1) % n]
        b.add_poly([(x - half, ya, za), (x - half, yb, zb),
                    (x + half, yb, zb), (x + half, ya, za)], conf, mat)


# ------------------------------------------------------------------------ roof

def _roof(b: MeshBuilder, p: LogDwellingParams, x0, y0, x1, y1,
          eave_z: float, conf: float) -> float:
    """Gable or shed over the log core. Returns the height of the highest point,
    which the chimney needs so its stack clears the ridge."""
    if p.roof_type == "shed":
        return _shed_roof(b, x0, y0, x1, y1, eave_z, p.roof_pitch_deg, conf, M_ROOF)
    return b.add_gable_roof(x0, y0, x1, y1, eave_z, p.roof_pitch_deg, conf, M_ROOF,
                            ridge_along_x=_ridge_along_x(x0, y0, x1, y1))


def _shed_roof(b: MeshBuilder, x0, y0, x1, y1, eave_z, pitch_deg, conf, mat,
               overhang: float = 0.25, thickness: float = 0.10) -> float:
    """A single plane falling from the back (-y, south) wall to the facade (+y).

    Falling toward the facade rather than away from it is the frontier default: the
    tall wall is the one the chimney and the back rooms go against, and rain runs off
    in front of the door where the ground is trodden hard. It is a convention, not an
    attested fact, and it is only ever reached when a record explicitly says shed.
    """
    x0, y0, x1, y1 = x0 - overhang, y0 - overhang, x1 + overhang, y1 + overhang
    rise = (y1 - y0) * math.tan(math.radians(pitch_deg))
    hi = eave_z + rise
    b.add_poly([(x0, y0, hi), (x1, y0, hi), (x1, y1, eave_z), (x0, y1, eave_z)],
               conf, mat)
    b.add_poly([(x0, y1, eave_z - thickness), (x1, y1, eave_z - thickness),
                (x1, y0, hi - thickness), (x0, y0, hi - thickness)], conf, mat)
    b.add_poly([(x0, y1, eave_z - thickness), (x1, y1, eave_z - thickness),
                (x1, y1, eave_z), (x0, y1, eave_z)], conf, mat)          # eave fascia
    for x, sgn in ((x0, -1), (x1, 1)):
        pts = [(y0, hi - thickness), (y0, hi), (y1, eave_z), (y1, eave_z - thickness)]
        if sgn > 0:
            pts.reverse()
        b.add_poly([(x, y, z) for y, z in pts], conf, mat)
    return hi


# -------------------------------------------------------------------- openings

def _loft_opening(b: MeshBuilder, p: LogDwellingParams, x0, y0, x1, y1,
                  wall_z: float, ridge_z: float, conf: float) -> None:
    """The only external trace a loft leaves: a small opening in one gable.

    Not a dormer. Dormers on log cabins are a later, richer habit, and adding one to
    make the loft more visible would be adding evidence rather than reading it.

    One gable, not both, and specifically the gable the chimney is NOT on. The stack
    stands against the -x end and is wider than this opening, so an opening at both
    ends buries one of them inside masonry — invisible in the render and still costing
    its triangles.
    """
    if p.roof_type != "gable":
        return
    zc = wall_z + (ridge_z - wall_z) * 0.42
    hw, hh, out = 0.34, 0.30, 0.07
    if _ridge_along_x(x0, y0, x1, y1):
        yc = (y0 + y1) / 2.0
        _panel(b, "x", x1 + out, yc - hw, yc + hw, zc - hh, zc + hh, 1, conf, M_DARK)
    else:
        xc = (x0 + x1) / 2.0
        _panel(b, "y", y1 + out, xc - hw, xc + hw, zc - hh, zc + hh, 1, conf, M_DARK)


def _core_openings(b: MeshBuilder, p: LogDwellingParams, x0, y0, x1, y1,
                   wall_z: float, conf: float) -> None:
    """Door and windows on the log core.

    Surfaces, not holes: at this LOD a real opening would show the inside of the far
    wall, and interiors are out of scope. Openings in a log wall were few and small
    because every one of them cuts the courses and has to be framed — one door and one
    or two small windows is the type, and a cabin elevation with five bays would be a
    frame building wearing logs.

    When a front addition exists it takes the front door, so the core gets a window
    where its door would have been.
    """
    front_taken = p.frame_addition and p.frame_addition_side == "front"
    story_h = wall_z / max(p.stories, 1)
    xm = (x0 + x1) / 2.0
    span = x1 - x0

    if not front_taken:
        _opening(b, "y", y1, xm - 0.52, xm + 0.52, 0.02, 1.95, 1, conf)

    for story in range(p.stories):
        z0 = story * story_h + story_h * 0.34
        for u in (xm - span * 0.28, xm + span * 0.28):
            _opening(b, "y", y1, u - 0.31, u + 0.31, z0, z0 + 0.72, 1, conf)
        if front_taken and story == 0:
            _opening(b, "y", y1, xm - 0.31, xm + 0.31, z0, z0 + 0.72, 1, conf)
        # One window on the south elevation, none on the gable ends: the gables carry
        # the chimney at one end and the notching at both, and a log gable was rarely
        # pierced.
        _opening(b, "y", y0, xm - 0.31, xm + 0.31, z0, z0 + 0.72, -1, conf)


# ------------------------------------------------------------- frame addition

def _frame_addition(b: MeshBuilder, p: LogDwellingParams) -> float:
    """The clapboarded frame block. Returns its ridge height.

    Its confidence is its own — Miller's two-storey addition is documented, Wolf
    Point's frame part is documented only as "partly frame" with no size — and it does
    not inherit the log core's.

    The ridge height goes back to the caller because a second stack stands on this
    block when the record counts two, and a stack has to clear the roof it comes
    through.
    """
    c = p.worst_conf("frame_addition", "frame_addition_stories")
    c_clad = p.conf("frame_addition", "reconstructed")
    c_fen = p.conf("fenestration", "reconstructed")
    ax0, ay0, ax1, ay1 = _addition_extent(p)
    az = p.addition_height_m

    b.add_box(ax0, ay0, 0.0, ax1, ay1, az, c, M_FRAME, skip=("bottom", "top"))
    _clapboard(b, ax0, ay0, ax1, ay1, az, c_clad)
    # An end addition abuts the log core, so its roof gets no overhang on that side —
    # `add_gable_roof` grows uniformly, and 0.25 m of eave driven into the core's roof
    # plane is a z-fighting stripe right down the most visible surface of the building.
    rx0 = ax0 + 0.26 if p.frame_addition_side == "end" else ax0
    add_ridge_z = b.add_gable_roof(rx0, ay0, ax1, ay1, az, p.roof_pitch_deg, c, M_ROOF,
                                   ridge_along_x=True)

    xm = (ax0 + ax1) / 2.0
    story_h = az / max(p.frame_addition_stories, 1)
    front = p.frame_addition_side == "front"
    rel = 0.026                    # clapboard lip, not log relief
    if front:
        _opening(b, "y", ay1, xm - 0.55, xm + 0.55, 0.02, 2.05, 1, c_fen,
                 relief=rel)
    for story in range(p.frame_addition_stories):
        z0 = story * story_h + story_h * 0.32
        for fx in (0.22, 0.78):
            u = ax0 + (ax1 - ax0) * fx
            if story == 0 and front and abs(u - xm) < 0.9:
                continue
            _opening(b, "y", ay1, u - 0.36, u + 0.36, z0, z0 + 1.05, 1, c_fen,
                     relief=rel)
    # The gable end that is not buried in the log core gets one window per storey.
    if p.frame_addition_side == "end":
        yc = (ay0 + ay1) / 2.0
        for story in range(p.frame_addition_stories):
            z0 = story * story_h + story_h * 0.32
            _opening(b, "x", ax1, yc - 0.36, yc + 0.36, z0, z0 + 1.05, 1, c_fen,
                     relief=rel)
    return add_ridge_z


def _clapboard(b: MeshBuilder, x0, y0, x1, y1, wall_z: float, conf: float) -> None:
    """Horizontal lap courses as a thin proud lip per course, on the two elevations
    that face the town. Same treatment as frame_tavern, so a frame addition and a
    frame tavern read as the same material at fifty metres."""
    lip = 0.018
    n = int(wall_z / CLAPBOARD_COURSE_M)
    for i in range(1, n):
        z = i * CLAPBOARD_COURSE_M
        b.add_poly([(x0, y0, z), (x1, y0, z),
                    (x1, y0 - lip, z - 0.02), (x0, y0 - lip, z - 0.02)], conf, M_FRAME)
        b.add_poly([(x1, y1, z), (x0, y1, z),
                    (x0, y1 + lip, z - 0.02), (x1, y1 + lip, z - 0.02)], conf, M_FRAME)


# ------------------------------------------------------------ chimney and sign

def _chimneys(b: MeshBuilder, p: LogDwellingParams, cx0, cy0, cx1, cy1,
              ridge_z: float, add_ridge_z: float | None, conf: float) -> None:
    """As many stacks as the record counts, placed by the archetype.

    The count is the record's; every other property of a stack here is invented, so
    the arrangement needs an argument rather than a preference, and the argument is
    the one the records themselves give:

    - The first stack stands against the log core's -x gable. That is the frontier
      pattern and it is what this archetype has always built.
    - The second stands on the FRAME ADDITION when there is one. Miller's record
      counts two because "a two-part building of this size — a former tavern with a
      log cabin behind — would normally carry a stack in each element", and putting
      both on the log core would build a number the record gives while contradicting
      the reasoning it gives for the number. It goes against the addition's outer
      gable, mirroring the core's.
    - With no addition, a second stack goes against the core's +x gable, which is
      the other end of the one element there is. No record in the dataset asks for
      this case yet.

    docs/LIBERTIES.md L26 owns all of it.
    """
    if p.chimneys <= 0:
        return
    _stack(b, cx0, cy0, cx1, cy1, ridge_z, conf, at_min_x=True)
    if p.chimneys < 2:
        return
    if p.frame_addition and add_ridge_z is not None:
        ax0, ay0, ax1, ay1 = _addition_extent(p)
        _stack(b, ax0, ay0, ax1, ay1, add_ridge_z, conf, at_min_x=False)
    else:
        _stack(b, cx0, cy0, cx1, cy1, ridge_z, conf, at_min_x=False)


def _stack(b: MeshBuilder, x0, y0, x1, y1, ridge_z: float, conf: float,
           at_min_x: bool) -> None:
    """One exterior stack against a gable end — the -x end, or mirrored to +x.

    Outside the wall, not inside it, which is the frontier pattern: a stick-and-clay
    or fieldstone stack built against the gable can be pulled away from the building
    when it catches fire, and it does not eat floor space. Nothing about the stack is
    attested for any building in the dataset, so it carries the count's confidence
    and no more.
    """
    yc = (y0 + y1) / 2.0
    half = 0.48
    face, out = (x0, -1.0) if at_min_x else (x1, 1.0)

    def span(inset: float, proud: float) -> tuple[float, float]:
        """(low x, high x) for a block reaching `proud` out from the gable face and
        `inset` into it, on whichever side of the building this stack is on."""
        a, c = face + out * proud, face - out * inset
        return (a, c) if a < c else (c, a)

    sx0, sx1 = span(0.08, 0.72)
    b.add_box(sx0, yc - half, 0.0, sx1, yc + half, ridge_z + 0.55,
              conf, M_ROOF, skip=("bottom",))
    # a slight corbel at the head, so it reads as a chimney rather than a post
    hx0, hx1 = span(0.12, 0.82)
    b.add_box(hx0, yc - half - 0.08, ridge_z + 0.55,
              hx1, yc + half + 0.08, ridge_z + 0.72, conf, M_ROOF,
              skip=("bottom",))


def _sign(b: MeshBuilder, p: LogDwellingParams, conf: float) -> None:
    """A signboard hanging from a bracket beside the front door.

    Wolf Point Tavern is the case: a painted sign of a wolf hung outside by about
    1833, and it is the single most distinctive documented thing about the building.
    Everything here except the fact of a hanging board is invention — the arm length,
    the board size, the two hangers — and none of it is a claim about the image, which
    is deliberately absent. See the module docstring.

    It hangs 1.7 m to one side of the front door, on whichever block carries that
    door, and clear of the eave. Two earlier placements failed on looking at them: at
    a fixed fraction of the overall width it landed on the frame extension rather than
    the tavern, and hung on a short arm it read as a placard nailed flat to the wall
    instead of a board swinging off a bracket. A tavern sign has to project — that is
    the whole function of one.
    """
    front = p.frame_addition and p.frame_addition_side == "front"
    if front:
        bx0, _, bx1, face = _addition_extent(p)
        eave = p.addition_height_m
    else:
        bx0, _, bx1, face = _core_extent(p)
        eave = p.wall_height_m
    x = min((bx0 + bx1) / 2.0 + 1.7, bx1 - 0.6)

    z = min(eave - 0.30, 2.55)
    arm, t = 1.15, 0.045
    bw, bh, bt = 0.88, 0.50, 0.05
    drop = 0.20
    yb = face + arm * 0.72          # the board hangs near the outer end of the arm

    # The arm out from the wall, with a strut under it. Kept slim: an earlier version
    # gave the strut a 0.66 m drop and made it two-thirds the width of the board, and
    # the bracket read as the object with a board attached rather than the other way
    # round. On a tavern the board is the point.
    b.add_box(x - t, face, z, x + t, face + arm, z + 2 * t, conf, M_SIGN,
              skip=("front",))
    _plate(b, x, t * 0.55,
           [(face + 0.02, z - 0.38), (face + 0.62, z), (face + 0.02, z)],
           conf, M_SIGN)
    for hx in (x - bw * 0.32, x + bw * 0.32):
        b.add_box(hx - 0.022, yb - 0.018, z - drop, hx + 0.022, yb + 0.018, z,
                  conf, M_SIGN, skip=("top", "bottom"))
    b.add_box(x - bw / 2, yb - bt / 2, z - drop - bh,
              x + bw / 2, yb + bt / 2, z - drop, conf, M_SIGN)
