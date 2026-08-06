#!/usr/bin/env python3
"""The baseline piece: a faceted knight.

This is the reference form for the whole set. Everything downstream — pawn,
bishop, rook, queen, king — reuses the plinth, the chamfer language and the
construction method defined here, and swaps only what happens above the
shoulders.

The construction method, in three moves:

  1. **Constant-width slabs.** Each mass (head, body) is a chamfered extrusion
     of a side-view outline at ONE half-width, so its flank is a single flat
     plane rather than a dome. Unioning a narrow head slab onto a wide body
     slab is what produces the hard jowl step.
  2. **Planar slice cuts.** Taper and draft are subtracted with flat blocks
     (``slice_block``), never modelled by varying width — that keeps every
     facet genuinely planar and every crease a straight line.
  3. **Grooves and pockets** for the lip line, the eye and the shoulder panel.

Printability rules the whole set inherits:
  * 34 mm plinth, 60 mm tall, 16-sided stepped foot, printed upright.
  * The plinth only ever narrows going up — no overhang anywhere in the foot.
  * Bevels sit at atan(0.80) = 39 deg from vertical.
  * The one horizontal ceiling in the form — the underside of the muzzle — is
    replaced by a 42 deg tent, so the piece needs no support at all.
"""

from __future__ import annotations

from pathlib import Path

import trimesh

from chesskit import (
    Knot,
    Silhouette,
    chamfered_extrude,
    groove_along,
    hull,
    plane_block,
    mirror_y,
    pocket,
    polygon_base,
    printability,
    slice_block,
    slice_block_z,
    write_stl,
)

HERE = Path(__file__).parent

# --------------------------------------------------------------------------
# Set-wide constants
# --------------------------------------------------------------------------

BASE_R = 17.45         # plinth circumradius (16-gon: 17.1 across the flats)
BASE_TOP_R = 15.1
BASE_TOP_Z = 15.6      # where the plinth ends and the figure begins
HEIGHT = 60.0
SIDES = 16

HEAD_W = 6.2           # half-width of the skull / mane slab
BODY_W = 8.6           # half-width of the neck / chest slab at the shoulder

# Bevel depth as a fraction of the chamfer. 0.80 -> the bevel plane under a
# horizontal silhouette edge sits at atan(0.80) = 38.7 deg from vertical,
# comfortably inside the 45 deg support-free window.
BEVEL_RATIO = 0.80


def K(x: float, z: float, c: float = 1.6, b: float | None = None) -> Knot:
    """A silhouette knot. Width is set per-slab, so it is not a knot property."""
    return Knot(x, z, 0.0, c, c * BEVEL_RATIO if b is None else b)


def at_width(knots, w: float) -> Silhouette:
    return Silhouette([Knot(k.x, k.z, w, k.chamfer, k.b) for k in knots])


# --------------------------------------------------------------------------
# The plinth — shared by every piece in the set
# --------------------------------------------------------------------------

# Four bands, read straight off the reference: a tall vertical flange at the
# bottom, then three drums each stepping in at a hard shoulder. Every step
# faces UP, so the whole plinth prints without a single overhang.
BASE_TIERS = [
    (BASE_R - 0.75, 0.0),   # slight lift so the first layer cannot flare
    (BASE_R, 0.8),
    (BASE_R, 4.0),          # bottom flange, vertical band
    (16.95, 4.0),           # hard step in
    (16.8, 8.2),
    (16.3, 8.2),            # hard step in
    (16.0, 12.4),
    (15.4, 12.4),           # hard step in
    (BASE_TOP_R, 15.2),     # collar
    (14.5, BASE_TOP_Z),     # top chamfer into the figure
]


def build_base() -> trimesh.Trimesh:
    return polygon_base(BASE_TIERS, sides=SIDES)


# --------------------------------------------------------------------------
# Outlines
# --------------------------------------------------------------------------
#
# Read the reference from the chest upward: the chest leans forward out of the
# collar, the throat draws back, the jaw is thrown forward at a hard notch, the
# muzzle runs out as a long wedge, the brow and crown rise behind it, and the
# mane falls away in six teeth to the shoulder.

CHEST = [
    K(10.6, 11.0, 1.2),               # buried in the plinth
    K(12.0, BASE_TOP_Z, 1.5),         # chest springs from the collar
    K(12.5, 21.0, 1.9),               # chest at its most forward
    K(11.9, 27.5, 1.9),
    K(10.1, 34.0, 1.9),
    K(7.6, 39.5, 1.8),
    K(6.1, 43.2, 1.5),                # throat, a straight run
    K(5.8, 44.8, 1.2),                # jaw notch (concave)
]

MUZZLE_AND_SKULL = [
    K(12.2, 45.2, 1.5),               # jaw underside
    K(18.8, 45.6, 1.5),
    K(24.6, 46.0, 1.3),               # chin: the lower lip leads the nose
    K(22.4, 50.2, 1.0),               # nose front, strongly raked back
    K(19.6, 52.4, 1.2),
    K(13.4, 53.8, 1.6),               # nostril break
    K(9.8, 55.6, 1.9),
    K(5.0, 57.3, 2.2),                # brow
    K(0.8, 59.0, 2.2),                # forehead
    K(-2.0, 60.0, 2.0),               # crown
    K(-3.2, 58.7, 1.5),               # ear, thrown back
    K(-6.8, 56.4, 1.3),               # notch behind the ear (concave)
]

# Mane: five teeth down the back, peak then valley. Each tooth's underside
# runs 22-32 deg from vertical, so the whole crest self-supports.
MANE = [
    K(-10.7, 54.6, 1.1),              # tooth 1
    K(-9.0, 51.2, 0.9),
    K(-12.9, 48.4, 1.1),              # tooth 2
    K(-11.1, 45.0, 0.9),
    K(-13.6, 42.0, 1.1),              # tooth 3
    K(-12.4, 38.6, 0.9),
    K(-14.7, 35.6, 1.2),              # tooth 4
    K(-13.5, 32.2, 1.0),
    K(-15.8, 29.2, 1.2),              # tooth 5
    K(-14.6, 25.8, 1.1),
]

SHOULDER_BACK = [
    K(-17.2, 19.6, 1.6),              # shoulder swells back out
    K(-14.2, BASE_TOP_Z, 1.5),
    K(-10.6, 10.5, 1.2),
]

# The head slab carries the whole figure at head width; the wider body slab is
# unioned under it, so the step between them reads as the jowl.
HEAD_OUTLINE = CHEST + MUZZLE_AND_SKULL + MANE + SHOULDER_BACK

# The body slab closes under the skull and then follows the mane teeth, so the
# crest is full-bodied rather than a fin.
BODY_OUTLINE = CHEST + [
    K(10.0, 47.6, 1.3),               # jowl, tucked under the cheek
    K(3.8, 51.8, 1.5),
    K(-6.2, 54.2, 1.5),               # neck crest, right under the ear notch
] + MANE + SHOULDER_BACK


# --------------------------------------------------------------------------
# Planar slice cuts
# --------------------------------------------------------------------------


def muzzle_taper() -> list[trimesh.Trimesh]:
    """Draw the muzzle sides in toward the nose — two flat facets a side."""
    cuts = [
        # Upper muzzle: head width at the brow drawing in to 2.9 at the nose.
        slice_block((2.0, HEAD_W), (24.8, 3.3), 43.0, 62.0),
        # A second, softer break so the muzzle reads as a wedge, not a knife.
        slice_block((-4.0, HEAD_W + 1.4), (13.0, 5.3), 50.5, 62.0),
    ]
    return [c for cut in cuts for c in (cut, mirror_y(cut))]


def skull_draft() -> list[trimesh.Trimesh]:
    """Bring the back of the skull in behind the ear, matching the reference."""
    cut = slice_block((-7.0, HEAD_W - 0.9), (3.0, HEAD_W + 1.4), 52.0, 62.0)
    return [cut, mirror_y(cut)]


def jaw_draft() -> list[trimesh.Trimesh]:
    """The lip line and the jaw taper, cut as ONE sloped plane.

    The most valuable cut in the piece, and it does three jobs at once:

      * its upper edge is the lip line — a single straight crease running the
        length of the muzzle, sloping down toward the throat exactly as the
        reference does, instead of a groove fighting a separate taper;
      * below that edge the jaw narrows to a keel, which gives the muzzle its
        triangular horse section rather than a flat bill;
      * the facet itself sits 41 deg from vertical, so the muzzle underside is
        drafted rather than left as a flat ceiling.

    The plane runs through: the lip line at the throat end, the lip line at the
    nose, and the keel under the throat end.
    """
    cut = plane_block(
        through=[(9.5, 5.35, 47.3), (24.0, 3.40, 48.8), (24.0, 2.40, 46.0)],
        x_range=(9.5, 27.0),
        z_range=(41.0, 52.5),
    )
    return [cut, mirror_y(cut)]


def neck_draft() -> list[trimesh.Trimesh]:
    """The neck sheds width continuously as it rises.

    Without this the body is a parallel-sided slab: correct in profile, wrong
    from the front or the back. The draft is gentle enough (4 mm over 36 mm of
    height) that the flank stays effectively vertical for printing, and it
    gives the shoulder a real flare into the plinth.
    """
    cut = slice_block_z((16.2, BODY_W + 0.2), (61.0, BODY_W - 3.4), -18.0, 14.0)
    return [cut, mirror_y(cut)]


def head_draft() -> list[trimesh.Trimesh]:
    """Taper the skull toward the crown so the head is not a mushroom cap."""
    cut = slice_block_z((46.0, 7.4), (61.0, 4.9), -11.0, 9.0)
    return [cut, mirror_y(cut)]


def mane_taper() -> list[trimesh.Trimesh]:
    """Taper the crest so each tooth reads as a wedge, not a paddle."""
    cut = slice_block((-6.0, BODY_W + 0.5), (-17.5, 7.5), 18.0, 62.0)
    return [cut, mirror_y(cut)]


# --------------------------------------------------------------------------
# Detail cuts
# --------------------------------------------------------------------------


def flank_y(x: float) -> float:
    """Half-width of the muzzle flank at x, after the taper cuts."""
    return HEAD_W - max(0.0, x - 2.0) * (HEAD_W - 3.4) / 23.0


def nostril() -> list[trimesh.Trimesh]:
    """A small slot high on the muzzle, where the top plane breaks."""
    section = [(21.4, 52.0), (18.4, 52.6), (19.8, 51.4)]
    cut = pocket(section, surface_y=3.7, depth=0.8, reach=4.0)
    return [cut, mirror_y(cut)]


def eye_socket() -> list[trimesh.Trimesh]:
    """Triangular recess under a hard brow, one each side."""
    section = [(10.6, 56.1), (4.6, 54.9), (9.6, 52.9)]
    cut = pocket(section, surface_y=5.35, depth=1.5, reach=5.0)
    return [cut, mirror_y(cut)]


def shoulder_crease() -> list[trimesh.Trimesh]:
    """Angular panel on the chest, echoing the jowl step above it."""
    path = [(10.3, 35.5), (11.9, 28.5), (11.6, 21.5)]
    cut = groove_along(path, apex_y=8.0 - 1.5, reach=8.0, half_angle=34.0)
    return [cut, mirror_y(cut)]


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def build() -> trimesh.Trimesh:
    head = chamfered_extrude(at_width(HEAD_OUTLINE, HEAD_W))
    body = chamfered_extrude(at_width(BODY_OUTLINE, BODY_W))

    piece = head.union(body).union(build_base())

    for cut in (muzzle_taper() + skull_draft() + jaw_draft() + head_draft()
                + neck_draft() + mane_taper()
                + nostril() + eye_socket() + shoulder_crease()):
        piece = piece.difference(cut)

    piece.merge_vertices()
    piece.update_faces(piece.nondegenerate_faces())
    piece.remove_unreferenced_vertices()
    piece.fix_normals()

    piece.apply_translation((0.0, 0.0, -piece.bounds[0][2]))
    return piece


def main() -> None:
    piece = build()
    (HERE / "stl").mkdir(exist_ok=True)
    out = HERE / "stl" / "knight_baseline.stl"
    write_stl(piece, out, "alligator-chess baseline knight")

    print(f"wrote {out}")
    for key, value in printability(piece).items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
