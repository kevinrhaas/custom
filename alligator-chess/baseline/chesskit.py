#!/usr/bin/env python3
"""chesskit — the shared geometry kernel for the faceted chess set.

Everything in the set is built from three primitives, so that every piece
shares one visual language and one printability story:

  1. ``Silhouette``  a closed side-view outline (the X/Z plane) whose knots
     each carry a half-width and a chamfer. ``chamfered_extrude`` turns it
     into a faceted slab: broad flat side planes, hard bevels running to the
     silhouette edge. This is the low-poly look — every surface is planar and
     every crease is a real edge, never a smoothed one.

  2. ``polygon_base``  a stacked N-gon plinth. Rotationally faceted, tiered,
     and always the same family of steps so all six pieces sit on a matching
     foot.

  3. Boolean detail cuts (``wedge_cutter``, ``slab``) for eyes, mouths and
     panel grooves, resolved with exact CSG so the result stays watertight.

Units are millimetres, Z is up, the piece sits on Z=0 and faces +X.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import trimesh

Vec2 = tuple[float, float]


# --------------------------------------------------------------------------
# Silhouette
# --------------------------------------------------------------------------


@dataclass
class Knot:
    """One vertex of the side-view outline.

    x, z      position in the side-view plane (mm)
    w         half-width of the flat side plane at this knot (mm)
    chamfer   how far the bevel eats into the silhouette (mm)
    bevel     how deep the bevel runs in Y; defaults to ``chamfer``
    """

    x: float
    z: float
    w: float
    chamfer: float = 1.0
    bevel: float | None = None

    @property
    def b(self) -> float:
        return self.chamfer if self.bevel is None else self.bevel


class Silhouette:
    """A closed, counter-clockwise outline in the X/Z plane."""

    def __init__(self, knots: Sequence[Knot]):
        if len(knots) < 3:
            raise ValueError("a silhouette needs at least three knots")
        self.knots = list(knots)
        if self._signed_area() < 0:
            self.knots.reverse()

    def _signed_area(self) -> float:
        pts = [(k.x, k.z) for k in self.knots]
        return 0.5 * sum(
            pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
            for i in range(len(pts))
        )

    def outward_normals(self) -> list[Vec2]:
        """Per-knot outward normal, mitred between the two adjacent edges."""
        n = len(self.knots)
        pts = np.array([[k.x, k.z] for k in self.knots], dtype=float)
        edge_n = []
        for i in range(n):
            d = pts[(i + 1) % n] - pts[i]
            length = math.hypot(*d) or 1.0
            # CCW polygon in X/Z -> outward normal is (dz, -dx)
            edge_n.append((d[1] / length, -d[0] / length))
        out = []
        for i in range(n):
            a = edge_n[i - 1]
            b = edge_n[i]
            v = (a[0] + b[0], a[1] + b[1])
            length = math.hypot(*v)
            if length < 1e-9:
                v, length = b, 1.0
            # Mitre: lengthen so the inset stays parallel to both edges.
            cos_half = max(0.35, math.sqrt(max(0.0, (1.0 + (a[0] * b[0] + a[1] * b[1])) / 2.0)))
            out.append((v[0] / length / cos_half, v[1] / length / cos_half))
        return out


def chamfered_extrude(sil: Silhouette) -> trimesh.Trimesh:
    """Faceted slab: flat side planes at y=+-w, bevelled down to the outline."""
    knots = sil.knots
    n = len(knots)
    normals = sil.outward_normals()

    core, edge = [], []
    for k, nrm in zip(knots, normals):
        core.append((k.x - nrm[0] * k.chamfer, k.z - nrm[1] * k.chamfer))
        edge.append((k.x, k.z))

    rings: list[list[tuple[float, float, float]]] = [[], [], [], []]
    for i, k in enumerate(knots):
        cx, cz = core[i]
        ex, ez = edge[i]
        inner_y = max(0.05, k.w - k.b)
        rings[0].append((cx, -k.w, cz))
        rings[1].append((ex, -inner_y, ez))
        rings[2].append((ex, +inner_y, ez))
        rings[3].append((cx, +k.w, cz))

    verts: list[tuple[float, float, float]] = []
    for ring in rings:
        verts.extend(ring)
    faces: list[tuple[int, int, int]] = []

    def ring_idx(r: int, i: int) -> int:
        return r * n + (i % n)

    # Bands between successive rings.
    for r in range(3):
        for i in range(n):
            a, b = ring_idx(r, i), ring_idx(r, i + 1)
            c, d = ring_idx(r + 1, i), ring_idx(r + 1, i + 1)
            faces.append((a, b, d))
            faces.append((a, d, c))

    # Side caps. Ear-clipped, NOT fanned from the centroid: the core ring goes
    # concave wherever the outline has a notch (a mane, a crenellation, a
    # crown), and a centroid fan hands CSG a self-intersecting solid there.
    cap = ear_clip([core[i] for i in range(n)])
    for r, flip in ((0, True), (3, False)):
        for a, b, c in cap:
            tri = (ring_idx(r, a), ring_idx(r, b), ring_idx(r, c))
            faces.append(tri[::-1] if flip else tri)

    mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    mesh.fix_normals()
    return mesh


def ear_clip(poly: Sequence[Vec2]) -> list[tuple[int, int, int]]:
    """Triangulate a simple polygon by ear clipping. Handles concave outlines."""
    pts = [np.array(p, float) for p in poly]
    n = len(pts)
    idx = list(range(n))
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
               for i in range(n))
    if area < 0:
        idx.reverse()

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    out: list[tuple[int, int, int]] = []
    guard = 0
    while len(idx) > 3 and guard < 4 * n * n:
        guard += 1
        clipped = False
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if cross(a, b, c) <= 1e-12:
                continue                       # reflex or degenerate
            if any(_in_triangle(pts[j], a, b, c)
                   for j in idx if j not in (i0, i1, i2)):
                continue                       # another vertex inside the ear
            out.append((i0, i1, i2))
            idx.pop(k)
            clipped = True
            break
        if not clipped:                        # numerically stuck: fan the rest
            break
    for k in range(1, len(idx) - 1):
        out.append((idx[0], idx[k], idx[k + 1]))
    return out


def _in_triangle(p, a, b, c) -> bool:
    def side(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])
    d1, d2, d3 = side(a, b, p), side(b, c, p), side(c, a, p)
    return not ((d1 < -1e-12 or d2 < -1e-12 or d3 < -1e-12)
                and (d1 > 1e-12 or d2 > 1e-12 or d3 > 1e-12))


# --------------------------------------------------------------------------
# Rotational plinth
# --------------------------------------------------------------------------


def polygon_base(tiers: Sequence[tuple[float, float]], sides: int = 16,
                 phase: float | None = None) -> trimesh.Trimesh:
    """Stacked N-gon plinth from (radius, z) knots, bottom first.

    Consecutive knots with the same z make a hard step; the profile is closed
    with a flat floor and a flat top disc.
    """
    if phase is None:
        phase = math.pi / sides
    ang = [phase + 2 * math.pi * i / sides for i in range(sides)]
    cos = [math.cos(a) for a in ang]
    sin = [math.sin(a) for a in ang]

    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []
    rings: list[int] = []
    for radius, z in tiers:
        rings.append(len(verts))
        for c, s in zip(cos, sin):
            verts.append((radius * c, radius * s, z))

    for r in range(len(tiers) - 1):
        lo, hi = rings[r], rings[r + 1]
        for i in range(sides):
            j = (i + 1) % sides
            faces.append((lo + i, lo + j, hi + j))
            faces.append((lo + i, hi + j, hi + i))

    floor = len(verts)
    verts.append((0.0, 0.0, tiers[0][1]))
    for i in range(sides):
        faces.append((floor, rings[0] + (i + 1) % sides, rings[0] + i))
    roof = len(verts)
    verts.append((0.0, 0.0, tiers[-1][1]))
    last = rings[-1]
    for i in range(sides):
        faces.append((roof, last + i, last + (i + 1) % sides))

    mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    mesh.fix_normals()
    return mesh


# --------------------------------------------------------------------------
# Detail cutters
# --------------------------------------------------------------------------


def wedge_cutter(section: Sequence[Vec2], y0: float, y1: float,
                 taper: float = 0.0) -> trimesh.Trimesh:
    """Prism from an X/Z polygon swept in Y, optionally tapering to a knife.

    ``taper`` shrinks the section toward its centroid at the y1 end; taper=1.0
    collapses it to a point, giving the V-groove used for mouths and eyes.
    """
    pts = np.array(section, dtype=float)
    centre = pts.mean(axis=0)
    n = len(pts)

    if taper >= 0.999:
        # True pyramid: one apex vertex, so the tip stays manifold.
        verts = [(p[0], y0, p[1]) for p in pts] + [(centre[0], y1, centre[1])]
        faces = [(i, (i + 1) % n, n) for i in range(n)]
        faces += [(0, i + 1, i) for i in range(1, n - 1)]
        mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
        mesh.fix_normals()
        return mesh

    far = centre + (pts - centre) * (1.0 - taper)
    verts = [(p[0], y0, p[1]) for p in pts] + [(p[0], y1, p[1]) for p in far]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j))
        faces.append((i, n + j, n + i))
    for i in range(1, n - 1):
        faces.append((0, i + 1, i))
        faces.append((n, n + i, n + i + 1))

    mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    mesh.fix_normals()
    return mesh


def slab(section: Sequence[Vec2], y0: float, y1: float) -> trimesh.Trimesh:
    return wedge_cutter(section, y0, y1, taper=0.0)


def groove_along(path: Sequence[Vec2], apex_y, reach: float = 12.0,
                 half_angle: float = 40.0, lip: float = 0.15) -> trimesh.Trimesh:
    """A V-groove cutter following an X/Z polyline, cut in from +Y.

    The cutter is a triangular prism whose apex sits at ``apex_y``; its walls
    open at ``half_angle`` from the Y axis, so the groove they leave in the
    surface has printable walls and its width is set purely by how deep the
    apex is buried. ``lip`` keeps a sliver of flat bottom so the boolean has
    no knife-edge to snag on.

    ``apex_y`` may be a single value or one per path point — use the latter to
    hold a constant groove depth as the flank it runs across changes width.
    """
    pts = np.array(path, dtype=float)
    n = len(pts)
    if n < 2:
        raise ValueError("a groove needs at least two path points")
    apex = np.full(n, float(apex_y)) if np.isscalar(apex_y) else np.asarray(apex_y, float)
    if len(apex) != n:
        raise ValueError("apex_y must be scalar or one value per path point")

    # Per-point normal in the X/Z plane.
    normals = []
    for i in range(n):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        d = b - a
        length = math.hypot(*d) or 1.0
        normals.append(np.array([d[1] / length, -d[0] / length]))

    spread = lip + reach * math.tan(math.radians(half_angle))

    verts: list[tuple[float, float, float]] = []
    for i in range(n):
        p, nrm = pts[i], normals[i]
        lo = p - nrm * spread
        hi = p + nrm * spread
        outer_y = apex[i] + reach
        verts.append((lo[0], outer_y, lo[1]))          # 3i
        verts.append((hi[0], outer_y, hi[1]))          # 3i+1
        verts.append((p[0] - nrm[0] * lip, apex[i], p[1] - nrm[1] * lip))  # 3i+2

    # Extend the two ends so the prism starts and finishes outside the solid.
    faces: list[tuple[int, int, int]] = []
    for i in range(n - 1):
        a0, a1, a2 = 3 * i, 3 * i + 1, 3 * i + 2
        b0, b1, b2 = 3 * (i + 1), 3 * (i + 1) + 1, 3 * (i + 1) + 2
        for (p, q), (r, s) in (((a0, a2), (b0, b2)), ((a2, a1), (b2, b1)), ((a1, a0), (b1, b0))):
            faces.append((p, q, s))
            faces.append((p, s, r))
    faces.append((0, 1, 2))
    faces.append((3 * (n - 1) + 2, 3 * (n - 1) + 1, 3 * (n - 1)))

    mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    mesh.fix_normals()
    return mesh


def pocket(section: Sequence[Vec2], surface_y: float, depth: float,
           reach: float = 4.0, taper: float = 1.0) -> trimesh.Trimesh:
    """A pyramidal recess: ``section`` is the opening left in a flat +Y face.

    The cutter is projected back from outside the solid so the opening lands
    at ``surface_y`` at exactly the requested size, with its point ``depth``
    below the surface.
    """
    apex_y = surface_y - depth
    outer_y = surface_y + reach
    grow = (outer_y - apex_y) / max(depth, 1e-6)
    pts = np.array(section, dtype=float)
    centre = pts.mean(axis=0)
    grown = centre + (pts - centre) * grow
    return wedge_cutter(grown, outer_y, apex_y, taper=taper)


def hull(points: Sequence[Sequence[float]]) -> trimesh.Trimesh:
    """Convex hull of a point cloud — the workhorse for planar slice cutters.

    Every facet-defining cut in the set is expressed this way: name the corners
    of the block you want gone and let the hull close it. The resulting cut is
    exactly planar, which is what keeps the low-poly read honest.
    """
    cloud = trimesh.points.PointCloud(np.array(points, dtype=float))
    mesh = cloud.convex_hull
    mesh.fix_normals()
    return mesh


def slice_block(anchor_a: Vec2, anchor_b: Vec2, z_lo: float, z_hi: float,
                y_far: float = 45.0) -> trimesh.Trimesh:
    """Block bounded by the vertical plane through two (x, y) plan anchors.

    A vertical cutting plane leaves a flat, draft-free facet — which is what
    every taper in the set is made of. The block is clipped to z in
    [z_lo, z_hi] so the cut stays local to one feature.
    """
    (xa, ya), (xb, yb) = anchor_a, anchor_b
    pts = []
    for z in (z_lo, z_hi):
        pts += [(xa, ya, z), (xb, yb, z), (xa, y_far, z), (xb, y_far, z)]
    return hull(pts)


def slice_block_z(anchor_a: Vec2, anchor_b: Vec2, x_lo: float, x_hi: float,
                  y_far: float = 45.0) -> trimesh.Trimesh:
    """Block bounded by the plane through two (z, y) elevation anchors.

    The companion to ``slice_block``: this one drafts a mass in or out as it
    rises, which is how the neck loses width toward the head. The block spans
    only z in [z_a, z_b], so put the anchors where the plane has already left
    the solid.
    """
    (za, ya), (zb, yb) = anchor_a, anchor_b
    pts = []
    for x in (x_lo, x_hi):
        pts += [(x, ya, za), (x, y_far, za), (x, yb, zb), (x, y_far, zb)]
    return hull(pts)


def plane_block(through: Sequence[Sequence[float]], x_range: Vec2, z_range: Vec2,
                y_far: float = 45.0) -> trimesh.Trimesh:
    """Block on the +Y side of the plane through three (x, y, z) points.

    The general case of ``slice_block`` / ``slice_block_z``: a cutting plane
    that tilts in x AND z at once. Used where one flat facet has to do two
    jobs — the knight's lip line is also the break where the jaw narrows, and
    a plane that slopes both ways gives a single crease doing both.

    Put ``z_range`` where the plane has already left the solid, or its end caps
    become flat ceilings.
    """
    (p, q, r) = (np.asarray(t, float) for t in through)
    # Solve y = a + b*x + c*z through the three points.
    m = np.array([[1.0, p[0], p[2]], [1.0, q[0], q[2]], [1.0, r[0], r[2]]])
    a, b, c = np.linalg.solve(m, np.array([p[1], q[1], r[1]]))

    pts = []
    for x in x_range:
        for z in z_range:
            pts.append((x, a + b * x + c * z, z))
            pts.append((x, y_far, z))
    return hull(pts)


def mirror_y(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    out = mesh.copy()
    out.apply_scale((1.0, -1.0, 1.0))
    out.fix_normals()
    return out


# --------------------------------------------------------------------------
# Quality gates
# --------------------------------------------------------------------------


def printability(mesh: trimesh.Trimesh, limit_deg: float = 45.0) -> dict:
    """Downward-facing area steeper than ``limit_deg`` from vertical.

    A face whose normal points down at more than ``limit_deg`` off straight
    down... expressed the usual slicer way: overhang angle is measured from
    the build plate normal, so a wall at 0 deg is vertical and 90 deg is a
    ceiling. Anything past ``limit_deg`` needs support.
    """
    normals = mesh.face_normals
    areas = mesh.area_faces
    nz = normals[:, 2]
    overhang_deg = np.degrees(np.arcsin(np.clip(-nz, -1.0, 1.0)))
    # Flat floors (nz == -1) rest on the plate, they are not overhangs.
    on_plate = mesh.triangles[:, :, 2].max(axis=1) < 1e-6
    bad = (overhang_deg > limit_deg) & (~on_plate)
    return {
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "volume_mm3": float(mesh.volume),
        "euler": int(mesh.euler_number),
        "faces": int(len(mesh.faces)),
        "bounds": mesh.bounds.tolist(),
        "overhang_area_mm2": float(areas[bad].sum()),
        "overhang_fraction": float(areas[bad].sum() / areas.sum()),
        "worst_overhang_deg": float(overhang_deg[~on_plate].max()) if (~on_plate).any() else 0.0,
        "unsupported_faces": int(bad.sum()),
    }


# --------------------------------------------------------------------------
# The fleet plinth — every piece in the set stands on this one
# --------------------------------------------------------------------------

PLINTH_R = 17.45        # circumradius; 17.11 across the flats of the 16-gon
PLINTH_TOP_R = 15.9
PLINTH_TOP_Z = 15.6
PLINTH_SIDES = 16

# Four bands, read off the reference: a tall vertical flange at the bottom,
# then three drums each stepping in at a hard shoulder, then the collar the
# figure springs from. Every step faces UP, so the plinth has zero overhang.
PLINTH_TIERS = [
    (PLINTH_R - 0.75, 0.0),   # lifted, so the first layer cannot flare out
    (PLINTH_R, 0.8),
    (PLINTH_R, 4.2),          # bottom flange, vertical band, the widest point
    (17.05, 4.2),             # hard step
    (16.95, 8.4),
    (16.55, 8.4),             # hard step
    (16.45, 12.6),
    (16.00, 12.6),            # hard step
    (PLINTH_TOP_R, 15.0),     # collar
    (15.20, PLINTH_TOP_Z),    # top chamfer into the figure
]


def fleet_plinth() -> trimesh.Trimesh:
    return polygon_base(PLINTH_TIERS, sides=PLINTH_SIDES)


# --------------------------------------------------------------------------
# Measuring the solid
# --------------------------------------------------------------------------


def flank_at(mesh: trimesh.Trimesh, x: float, z: float) -> float:
    """Half-width of the solid at (x, z) — the real one, not a prediction.

    Detail cuts have to be placed relative to the surface they land on, and
    after a stack of booleans that surface is not something a formula can
    predict; predicting it is how a pocket ends up punching through a
    silhouette. So ask the solid: slice it at height z and interpolate the
    outline where it crosses x.

    Sampling vertices instead does NOT work — the middle of a large flat facet
    has no vertices in it, so a vertex query there returns nothing and a cut
    placed on the answer saws the piece in half.
    """
    section = mesh.section(plane_origin=[0.0, 0.0, z], plane_normal=[0.0, 0.0, 1.0])
    if section is None:
        return 0.0
    best = 0.0
    for path in section.discrete:
        pts = np.asarray(path, float)
        for a, b in zip(pts[:-1], pts[1:]):
            if (a[0] - x) * (b[0] - x) > 0:
                continue                       # segment does not span x
            span = b[0] - a[0]
            t = 0.5 if abs(span) < 1e-9 else (x - a[0]) / span
            best = max(best, abs(a[1] + t * (b[1] - a[1])))
    return float(best)


# The thinnest triangle allowed to ship. Chained CSG leaves needles where two
# cutting planes graze; below this width they are unrepresentable in a float32
# STL and are nothing but noise for a slicer.
NEEDLE_LIMIT = 0.005


def triangle_altitude(mesh: trimesh.Trimesh) -> np.ndarray:
    """Shortest height of each triangle, in mm — how THIN the needle is.

    Aspect ratio is the wrong test for a low-poly solid: a long flat facet
    split into two triangles is legitimately elongated and perfectly fine. What
    is not fine is a triangle a few microns thick, which is what chained
    booleans leave behind where two cutting planes graze at near-zero
    incidence. Altitude measures exactly that, in units a printer understands.
    """
    tri = mesh.triangles
    longest = np.max(np.stack([
        np.linalg.norm(tri[:, 1] - tri[:, 0], axis=1),
        np.linalg.norm(tri[:, 2] - tri[:, 1], axis=1),
        np.linalg.norm(tri[:, 0] - tri[:, 2], axis=1)], axis=1), axis=1)
    return np.where(longest > 0, 2 * mesh.area_faces / longest, 0.0)


def cull_slivers(mesh: trimesh.Trimesh, min_altitude: float = NEEDLE_LIMIT) -> trimesh.Trimesh:
    """Weld sub-resolution vertices and drop needles, then re-close the shell.

    The bar is NEEDLE_LIMIT: forty times coarser than float32 can represent at
    these coordinates (so the triangle survives the STL round-trip meaningfully)
    and four hundred times finer than the finest resin layer (so nothing that
    was ever going to be manufactured is touched).

    Needles are COLLAPSED, not deleted. Welding the two near-coincident
    vertices makes the needle degenerate and turns its two neighbours into a
    shared edge, so dropping it afterwards leaves the shell closed — whereas
    deleting the face outright punches a hole that no hole-filler reliably
    closes on a faceted solid.
    """
    out = mesh.copy()
    # Escalate the collapse tolerance: a groove that fades out on a surface
    # leaves a triangle whose SHORT edge is just above any fixed threshold
    # while the triangle itself is still a needle. The ceiling stays low enough
    # that no real feature can be collapsed.
    tol = min_altitude
    for _ in range(6):
        out = _collapse_short_edges(out, tol, sliver_limit=min_altitude)
        out.update_faces(out.nondegenerate_faces())
        out.update_faces(out.unique_faces())
        out.remove_unreferenced_vertices()
        if (triangle_altitude(out) >= min_altitude).all():
            break
        tol = min(tol * 2.0, 0.04)
    out.fix_normals()
    return out


def _collapse_short_edges(mesh: trimesh.Trimesh, tol: float,
                          sliver_limit: float = 0.0,
                          max_move: float = 0.5) -> trimesh.Trimesh:
    """Union-find edge collapse for every edge shorter than ``tol``.

    Deliberately not trimesh's hash-based ``merge_vertices``: that rounds
    coordinates into buckets, so two vertices 4 microns apart that happen to
    straddle a bucket boundary are never merged — which is exactly the case
    that produces these needles in the first place.

    Chained booleans also leave a second kind of sliver: a triangle whose three
    vertices are near-collinear, so it has no short edge at all and no length
    threshold can find it. Those are caught by ``sliver_limit`` — collapse the
    shortest edge of any triangle thinner than that, provided doing so moves a
    vertex less than ``max_move``.
    """
    v = np.asarray(mesh.vertices, float)
    edges = mesh.edges_unique
    lengths = np.linalg.norm(v[edges[:, 0]] - v[edges[:, 1]], axis=1)
    doomed = list(edges[lengths < tol])

    if sliver_limit > 0:
        thin = np.where(triangle_altitude(mesh) < sliver_limit)[0]
        for f in thin:
            tri = mesh.faces[f]
            pairs = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
            a, b = min(pairs, key=lambda e: np.linalg.norm(v[e[0]] - v[e[1]]))
            if np.linalg.norm(v[a] - v[b]) < max_move * 2:
                doomed.append((a, b))

    parent = np.arange(len(v))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b in doomed:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    roots = np.array([find(i) for i in range(len(v))])
    if (roots == np.arange(len(v))).all():
        return mesh

    # Each cluster collapses to its centroid.
    order, inverse = np.unique(roots, return_inverse=True)
    merged = np.zeros((len(order), 3))
    np.add.at(merged, inverse, v)
    counts = np.bincount(inverse, minlength=len(order))[:, None]
    out = trimesh.Trimesh(vertices=merged / counts,
                          faces=inverse[mesh.faces], process=False)
    return out


def layer_report(mesh: trimesh.Trimesh, step: float = 0.4) -> dict:
    """Slice the piece and look for what actually kills a print.

    Overhang angle is the number everyone quotes, but the failure that
    genuinely ruins a piece is an ISLAND: a layer containing a loop that has
    nothing under it, so the nozzle starts extruding into air. A steep overhang
    on a region that is still connected to the layer below droops; an island
    falls off. This walks every layer and reports both, plus the thinnest
    section (area/perimeter), which flags anything too fine to print.
    """
    lo, hi = mesh.bounds[0][2], mesh.bounds[1][2]
    heights = np.arange(lo + step / 2, hi, step)
    empty, islands = [], []
    thinnest = (float("inf"), None)
    for z in heights:
        section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if section is None:
            empty.append(round(float(z), 2))
            continue
        flat, _ = section.to_2D()
        loops = len(flat.discrete)
        if loops > 1:
            islands.append((round(float(z), 2), loops))
        perimeter = sum(np.linalg.norm(np.diff(d, axis=0), axis=1).sum()
                        for d in flat.discrete)
        if perimeter:
            t = 2 * flat.area / perimeter
            if t < thinnest[0]:
                thinnest = (float(t), round(float(z), 2))
    return {
        "layers": int(len(heights)),
        "layer_height_mm": step,
        "empty_layers": empty,
        "layers_with_islands": islands,
        "thinnest_section_mm": round(thinnest[0], 2),
        "thinnest_at_z": thinnest[1],
    }


def write_stl(mesh: trimesh.Trimesh, path, name: str = "chess_piece") -> None:
    """Binary STL, written by hand so the header carries the piece name."""
    import struct

    tris = mesh.triangles
    normals = mesh.face_normals
    header = name.encode("ascii", "replace")[:79].ljust(80, b"\0")
    with open(path, "wb") as fh:
        fh.write(header)
        fh.write(struct.pack("<I", len(tris)))
        for nrm, tri in zip(normals, tris):
            fh.write(struct.pack("<3f", *nrm))
            for v in tri:
                fh.write(struct.pack("<3f", *v))
            fh.write(struct.pack("<H", 0))
