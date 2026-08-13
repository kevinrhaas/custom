"""frame_tavern — a two-storey frame tavern with an optional attached log wing.

The Sauganash is the reference case, and it is deliberately the first archetype
because it exercises the whole confidence model in one building: the white
two-storey block and its blue shutters are documented, the footprint and roof are
invented, and the attached log wing is inferred from two derivative images.

On construction: balloon framing was developed in Chicago in 1832-33 and became
the dominant local method, but the Sauganash frame block predates that by a year,
so `braced_frame` is the better reading. The geometry that follows is exterior
massing and cladding — the framing question changes stud rhythm behind the
sheathing, which is not modelled at this LOD. Recorded here so the next person
does not assume it was overlooked; see docs/RESEARCH/sauganash_hotel.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.mesh import (  # noqa: E402
    LOG_RGBA, PAINT_RGBA, ROOF_RGBA, SHUTTER_RGBA, MeshBuilder, simple_material,
)
from archetypes.frame_tavern_params import FrameTavernParams  # noqa: E402

# Materials are indices into the list passed to to_object(), in this order.
M_WALL, M_ROOF, M_LOG, M_SHUTTER, M_GLASS = 0, 1, 2, 3, 4

CLAPBOARD_COURSE_M = 0.14   # exposed face of a period clapboard, ~5.5 in
CORNER_LOG_D = 0.22         # hewn log face


def build(params: FrameTavernParams, name: str):
    """Build the tavern. Returns a Blender object at the local origin, y-up handled
    by the exporter (Blender is z-up internally)."""
    params.validate()
    b = MeshBuilder(name)

    w, d = params.width_m, params.depth_m

    # Massing confidence describes the building's CHARACTER, not the precision of
    # its dimensions. Those are two different kinds of not-knowing, and folding
    # them together misrepresents the evidence.
    #
    # The Sauganash forced the distinction. Wau-Bun documents "a pretentious
    # white two-story building, with bright-blue wooden shutters" — we know what
    # this building WAS. What no source gives is a dimension. The first version
    # of this rule drove the massing off the footprint, so a conjectural size
    # dithered the entire building into ghost massing, which told a viewer we
    # knew nothing about a comparatively well-attested structure. That is a
    # misrepresentation in the direction of false modesty, and it is just as
    # wrong as overclaiming.
    #
    # So: the massing takes the confidence of the attributes that say what the
    # building was — its storey count, how it was built, what it was clad in.
    # Dimensional uncertainty is real and is carried honestly elsewhere: the
    # footprint keeps its own confidence in the sidecar, and the placement
    # carries uncertainty_m. Both surface in the popup.
    c_mass = params.worst_conf("stories", "construction", "cladding")
    c_roof = params.worst_conf("roof_type", "roof_pitch_deg")
    c_clad = params.worst_conf("cladding", "paint")

    wall_z = params.wall_height_m

    # main block — omit the bottom, it is never seen and costs two triangles per
    # building across the whole town
    b.add_box(0, 0, 0, w, d, wall_z, c_mass, M_WALL, skip=("bottom",))

    # clapboard courses as shallow relief on the two long elevations. Cheap
    # geometry, but it is what makes a frame building read as frame rather than
    # as a painted box at walking distance.
    _clapboard(b, w, d, wall_z, c_clad)

    ridge_z = b.add_gable_roof(0, 0, w, d, wall_z, params.roof_pitch_deg, c_roof,
                               M_ROOF, ridge_along_x=(w >= d))

    # windows: five bays upper, four plus a centred door below — the arrangement
    # both surviving depictions show. Fenestration is not separately attested, so
    # it inherits the massing's confidence at best.
    c_fen = params.conf("fenestration", "inferred")
    _fenestration(b, params, w, d, wall_z, c_fen)

    if params.log_wing:
        _log_wing(b, params, d)

    # chimneys — as many stacks as the record counts, on the ridge line.
    c_ch = params.conf("chimneys")
    for fx in _stack_fractions(params.chimneys):
        cx = w * fx
        b.add_box(cx - 0.45, d / 2 - 0.45, wall_z, cx + 0.45, d / 2 + 0.45,
                  ridge_z + 0.55, c_ch, M_ROOF, skip=("bottom",))

    mats = [
        simple_material("wall", PAINT_RGBA.get(params.paint, PAINT_RGBA["unpainted"])),
        simple_material("roof", ROOF_RGBA, roughness=0.9),
        simple_material("log", LOG_RGBA, roughness=0.9),
        simple_material("shutter",
                        SHUTTER_RGBA.get(params.shutters or "", SHUTTER_RGBA["green"])),
        simple_material("glass", (0.09, 0.11, 0.13, 1.0), roughness=0.25),
    ]
    return b.to_object(mats)


def _stack_fractions(n: int) -> tuple[float, ...]:
    """Where n stacks stand, as fractions of the frontage.

    The pair sits at 0.22 and 0.78 — the positions this archetype has always used,
    read off the two retrospective depictions of the Sauganash, and kept exactly so
    that making the count a parameter does not quietly move the buildings that
    already had the number the record states. More than two spaces evenly between
    the same two ends; one goes to 0.22 rather than to the middle, because a single
    stack on a central-hall block stands at an end of the block and not in the hall.

    None of these positions is attested for any building in the dataset. The count
    is the record's and the arrangement is the archetype's; docs/LIBERTIES.md says so.
    """
    if n <= 0:
        return ()
    if n == 1:
        return (0.22,)
    step = (0.78 - 0.22) / (n - 1)
    return tuple(0.22 + i * step for i in range(n))


def _clapboard(b: MeshBuilder, w: float, d: float, wall_z: float, conf: float) -> None:
    """Horizontal lap courses, modelled as a thin proud lip per course."""
    lip = 0.018
    n = int(wall_z / CLAPBOARD_COURSE_M)
    for i in range(1, n):
        z = i * CLAPBOARD_COURSE_M
        for y, ny in ((0.0, -lip), (d, d + lip)):
            b.add_poly([(0, y, z), (w, y, z), (w, ny, z - 0.02), (0, ny, z - 0.02)],
                       conf, M_WALL)


def _fenestration(b: MeshBuilder, params: FrameTavernParams, w: float, d: float,
                  wall_z: float, conf: float) -> None:
    """Recessed window reveals plus shutters where attested.

    Windows are recesses rather than holes: at this LOD an opening would show the
    inside of the far wall, and interiors are out of scope.
    """
    story_h = wall_z / max(params.stories, 1)
    win_w, win_h, depth = 0.85, 1.35, 0.06
    c_shut = params.conf("shutters", "inferred")

    for story in range(params.stories):
        z0 = story * story_h + story_h * 0.30
        bays = 5
        for i in range(bays):
            cx = w * (i + 0.5) / bays
            # Ground-floor centre bay is the entrance instead of a window. The
            # entrance is on the FACADE, which is the +y face in Blender and
            # therefore faces north once exported — bearing 0 per the contract.
            if story == 0 and i == bays // 2:
                yy = d + depth
                b.add_poly([(cx + 0.6, yy, 0), (cx - 0.6, yy, 0),
                            (cx - 0.6, yy, 2.1), (cx + 0.6, yy, 2.1)],
                           conf, M_GLASS)
                continue
            for y, sgn in ((0.0, -1.0), (d, 1.0)):
                yy = y + sgn * depth
                # Wind by the elevation's outward normal. Using one point order
                # for both faces leaves the +y openings facing INTO the building;
                # that was invisible only because the exporter writes
                # doubleSided by default, which is not a guarantee to build on.
                x0q, x1q = ((cx - win_w / 2, cx + win_w / 2) if sgn < 0
                            else (cx + win_w / 2, cx - win_w / 2))
                b.add_poly([(x0q, yy, z0), (x1q, yy, z0),
                            (x1q, yy, z0 + win_h), (x0q, yy, z0 + win_h)],
                           conf, M_GLASS)
                if params.shutters:
                    for side in (-1, 1):
                        x0 = cx + side * (win_w / 2)
                        x1 = x0 + side * (win_w * 0.42)
                        yl = y + sgn * (depth * 0.4)
                        lo, hi = min(x0, x1), max(x0, x1)
                        a_, b_ = (lo, hi) if sgn < 0 else (hi, lo)
                        b.add_poly([(a_, yl, z0), (b_, yl, z0),
                                    (b_, yl, z0 + win_h), (a_, yl, z0 + win_h)],
                                   c_shut, M_SHUTTER)


def _log_wing(b: MeshBuilder, params: FrameTavernParams, main_d: float) -> None:
    """The 1829 log cabin surviving as an attached single-storey wing.

    Both surviving depictions (Braunhold's engraving in Andreas 1884 and Kurz &
    Allison panel 14, 1893) show it at the left front of the frame block, log
    courses and corner notching plainly drawn. They are not independent — the
    later composition follows the earlier — so this is `inferred`, and the wing
    carries that confidence rather than the main block's.
    """
    c = params.conf("log_wing", "inferred")
    ww, wd, wh = params.log_wing_width_m, params.log_wing_depth_m, params.log_wing_height_m

    # Projects forward from the facade, which is +y in Blender (north once
    # exported). y1 is the wall it abuts, y0 the far face.
    y1, y0 = main_d, main_d + wd
    b.add_box(0, y1, 0, ww, y0, wh, c, M_LOG, skip=("bottom", "front"))

    # individual log courses, so it reads as log and not as a stained box
    course = 0.30
    n = int(wh / course)
    for i in range(1, n):
        z = i * course
        b.add_poly([(ww, y0, z), (0, y0, z), (0, y0 + 0.015, z - 0.015),
                    (ww, y0 + 0.015, z - 0.015)], c, M_LOG)
        for x in (0.0, ww):
            sgn = -1 if x == 0.0 else 1
            b.add_poly([(x, y1, z), (x, y0, z), (x + sgn * 0.015, y0, z - 0.015),
                        (x + sgn * 0.015, y1, z - 0.015)], c, M_LOG)
        # protruding notched log ends at the corners
        for x in (0.0, ww):
            sgn = -1 if x == 0.0 else 1
            b.add_box(min(x, x + sgn * CORNER_LOG_D), y0, z - course * 0.5,
                      max(x, x + sgn * CORNER_LOG_D), y0 + CORNER_LOG_D,
                      z - course * 0.5 + 0.16, c, M_LOG)

    # lean-to roof, tight to the wing and sloping up to meet the frame block
    oh, rise, thk = 0.12, 0.5, 0.09
    yf, yb = y0 + oh, y1
    for dz in (0.0, -thk):                      # upper and lower faces
        b.add_poly([(-oh, yf, wh + dz), (ww + oh, yf, wh + dz),
                    (ww + oh, yb, wh + rise + dz), (-oh, yb, wh + rise + dz)], c, M_ROOF)
    # fascia along the eave, and closed rake edges — a roof with an edge reads as
    # a roof; a single plane reads as a floating slab
    b.add_poly([(-oh, yf, wh - thk), (ww + oh, yf, wh - thk),
                (ww + oh, yf, wh), (-oh, yf, wh)], c, M_ROOF)
    for x in (-oh, ww + oh):
        b.add_poly([(x, yf, wh - thk), (x, yf, wh),
                    (x, yb, wh + rise), (x, yb, wh + rise - thk)], c, M_ROOF)
