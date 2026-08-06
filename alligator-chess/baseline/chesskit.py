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

    # Side caps, fanned from the ring centroid so a non-planar cap still closes.
    for r, flip in ((0, True), (3, False)):
        pts = np.array([verts[ring_idx(r, i)] for i in range(n)])
        centre = tuple(pts.mean(axis=0))
        ci = len(verts)
        verts.append(centre)
        for i in range(n):
            a, b = ring_idx(r, i), ring_idx(r, i + 1)
            faces.append((ci, b, a) if flip else (ci, a, b))

    mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    mesh.fix_normals()
    return mesh


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
