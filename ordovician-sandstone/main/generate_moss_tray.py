#!/usr/bin/env python3
"""
Ordovician Sandstone Moss Tray + Drip Tray Generator
=====================================================
Two-piece assembly:
  Piece 1 — Moss Tray  : 40 mm deep organic hollow tray
  Piece 2 — Drip Tray  : 18 mm saucer with 4 organic swoop nubs

The exterior shell uses the real Illinois sandstone strata ring data
(non-uniformly scaled from circular to oval to match tray dimensions).

Rim taper: the top 4 mm of the outer wall tapers inward to a thin edge.
Floor: flat cap rings bracket the organic strata so the slicer never sees
       zero-thickness or floating layers.
Drain holes + nub alignment holes are solid sub-mesh cylinders (slicer cuts).

Outputs (written next to this script):
  moss_tray.stl / moss_tray.3mf
  drip_tray.stl / drip_tray.3mf

Usage:
  python3 generate_moss_tray.py            # both pieces
  python3 generate_moss_tray.py --piece tray
  python3 generate_moss_tray.py --piece drip
"""

import argparse
import math
import os
import re
import struct
import sys
import zipfile
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
SCAD_SOURCE = SCRIPT_DIR / ".." / "raw" / "1-illinois_sandstone_cylinder_v3.scad"

# ── Sandstone source constants (must match parse_original_scad) ───────────────
BASELINE_HEIGHT     = 120.0
BASELINE_NUM_LAYERS = 111
RING_PTS            = 120   # points per ring

# ── Design parameters ─────────────────────────────────────────────────────────
TRAY_TOP_L    = 200.0   # moss tray top, long side (outer)
TRAY_TOP_W    = 150.0   # moss tray top, short side (outer)
BASE_BOT_L    = 180.0   # drip tray base, long side (outer)
BASE_BOT_W    = 130.0   # drip tray base, short side (outer)

TRAY_HEIGHT   = 40.0    # moss tray depth
SAUCER_WALL   = 15.0    # drip tray wall height
SAUCER_FLOOR  = 3.0     # drip tray floor thickness
SAUCER_HEIGHT = SAUCER_WALL + SAUCER_FLOOR   # 18 mm
TOTAL_H       = TRAY_HEIGHT + SAUCER_HEIGHT   # 58 mm  (taper span)

WALL_T        = 4.0     # wall thickness (both pieces)
FLOOR_T       = 3.0     # floor thickness (moss tray)

# Rim taper: outer wall tapers inward over the top TAPER_H mm
TAPER_H       = 4.0     # mm of taper zone
RIM_WALL_T    = 0.6     # wall thickness at the very rim (mm)

# Strata Z undulation scaling (1.0 = same absolute amplitude as original SCAD)
STRATA_Z_SCALE = 0.0    # planar rings — per-point Z deviation breaks slicer cross-sections

# Swoop nub parameters
NUB_BASE_R    = 8.0     # radius at saucer floor (16 mm dia footprint)
NUB_TOP_R     = 5.0     # radius at nub top (10 mm dia)
NUB_TOTAL_H   = 20.0    # 15 mm inside saucer + 5 mm above rim
NUB_PTS       = 24      # angular points per nub ring
NUB_RING_STEPS = 10     # rings for smooth taper profile

# Nub positions (centre of each nub, relative to saucer centre)
# Kept well inside the interior cavity so the nub base + organic strata
# undulation never overlap the wall.
NUB_OFFSET_L  = 36.0
NUB_OFFSET_W  = 20.0
NUB_POSITIONS = [
    ( NUB_OFFSET_L,  NUB_OFFSET_W),
    (-NUB_OFFSET_L,  NUB_OFFSET_W),
    (-NUB_OFFSET_L, -NUB_OFFSET_W),
    ( NUB_OFFSET_L, -NUB_OFFSET_W),
]

# Smooth interior: sized to fit inside the *tightest* sandstone inward bump.
# Sandstone radius varies ~±14 % from its mean, so the inner ellipse must be
# scaled to ≤ 0.86 × nominal half-axis (then minus WALL_T) to guarantee that
# the smooth interior stays inside the organic exterior everywhere.
SMOOTH_SCALE  = 0.82    # extra 4 % safety beyond the 0.86 worst-case

# Nub receivers in moss tray floor: 1 mm clearance over nub base
NUB_RECEIVER_R = NUB_BASE_R + 1.0   # 9 mm

# Drain holes (through the moss tray floor)
DRAIN_HOLE_R  = 3.5     # 7 mm dia (large enough to clearly survive slicer thresholds)
DRAIN_HOLE_N  = 12
DRAIN_HOLE_PTS = 16


# ─────────────────────────────────────────────────────────────────────────────
# Sandstone ring loader (reads Illinois SCAD polyhedron)
# ─────────────────────────────────────────────────────────────────────────────

_orig_rings      = None
_orig_ring_avg_z = None
_orig_radius     = None   # average XY radius of the source cylinder


def _parse_original_scad(filepath):
    points = []
    point_re = re.compile(r'\[\s*([^,]+),\s*([^,]+),\s*([^\]]+)\]')
    with open(filepath) as f:
        for line in f:
            if 'faces' in line and '=' in line:
                break
            m = point_re.search(line)
            if m:
                points.append((float(m.group(1)),
                               float(m.group(2)),
                               float(m.group(3))))
    rings = []
    ring_avg_z = []
    for i in range(BASELINE_NUM_LAYERS):
        ring = points[i * RING_PTS:(i + 1) * RING_PTS]
        rings.append(ring)
        ring_avg_z.append(sum(p[2] for p in ring) / RING_PTS)
    return rings, ring_avg_z


def _load_scad():
    global _orig_rings, _orig_ring_avg_z, _orig_radius
    if _orig_rings is not None:
        return
    rings, ring_avg_z = _parse_original_scad(str(SCAD_SOURCE))
    _orig_rings      = rings
    _orig_ring_avg_z = ring_avg_z
    mid = rings[len(rings) // 2]
    _orig_radius = sum(math.sqrt(p[0]**2 + p[1]**2) for p in mid) / len(mid)
    print(f"  SCAD: {len(rings)} rings, avg radius = {_orig_radius:.1f} mm")


def sandstone_ring(z_local, half_l, half_w, frac):
    """
    Return RING_PTS points for one strata ring.

    frac   : 0.0 = top of the piece, 1.0 = bottom
    z_local: nominal Z for this ring (before strata undulation)
    half_l : half-length of the oval at this level
    half_w : half-width  of the oval at this level

    The ring XY is taken from the Illinois sandstone source (scaled to oval)
    and the per-point Z undulation from the source is added to z_local.
    """
    _load_scad()
    n = len(_orig_rings)
    # frac=0 → top of SCAD (ring n-1); frac=1 → bottom of SCAD (ring 0)
    orig_pos = (1.0 - frac) * (n - 1)
    i_lo = max(0, int(math.floor(orig_pos)))
    i_hi = min(i_lo + 1, n - 1)
    alpha = orig_pos - i_lo

    ring_z_mean = _orig_ring_avg_z[i_lo] * (1 - alpha) + _orig_ring_avg_z[i_hi] * alpha

    result = []
    for j in range(RING_PTS):
        p_lo = _orig_rings[i_lo][j]
        p_hi = _orig_rings[i_hi][j]
        x_o = p_lo[0] + (p_hi[0] - p_lo[0]) * alpha
        y_o = p_lo[1] + (p_hi[1] - p_lo[1]) * alpha
        z_o = p_lo[2] + (p_hi[2] - p_lo[2]) * alpha

        # Non-uniform scale: circle → oval
        x = x_o / _orig_radius * half_l
        y = y_o / _orig_radius * half_w

        # Strata Z undulation (deviation from ring mean, scaled)
        z_dev = z_o - ring_z_mean
        result.append((x, y, z_local + z_dev * STRATA_Z_SCALE))

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Geometry helpers
# ─────────────────────────────────────────────────────────────────────────────

def lerp(a, b, t):
    return a + (b - a) * t


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def cross(u, v):
    return (u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0])


def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length < 1e-12:
        return (0.0, 0.0, 0.0)
    return (v[0]/length, v[1]/length, v[2]/length)


def taper_dims(z_from_top):
    """Return (length, width) at z_from_top [0 = moss tray top, TOTAL_H = saucer base]."""
    t = z_from_top / TOTAL_H
    return lerp(TRAY_TOP_L, BASE_BOT_L, t), lerp(TRAY_TOP_W, BASE_BOT_W, t)


def offset_ring_inward(ring, wall_t):
    """Offset ring points inward by wall_t in XY (Z preserved)."""
    cx = sum(p[0] for p in ring) / len(ring)
    cy = sum(p[1] for p in ring) / len(ring)
    inner = []
    for (x, y, z) in ring:
        dx, dy = x - cx, y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 1e-9:
            inner.append((x, y, z))
        else:
            inner.append((x - dx/dist * wall_t,
                          y - dy/dist * wall_t, z))
    return inner


def smooth_ellipse_ring(z, half_l, half_w, n_pts=RING_PTS):
    """Pure ellipse ring at z, CCW from above."""
    return [(half_l * math.cos(2.0 * math.pi * i / n_pts),
             half_w * math.sin(2.0 * math.pi * i / n_pts),
             z) for i in range(n_pts)]


# ─────────────────────────────────────────────────────────────────────────────
# Polygon-with-holes triangulator (ear clipping + hole bridging)
# ─────────────────────────────────────────────────────────────────────────────

def _pit(p, a, b, c, eps=1e-9):
    d1 = (p[0]-b[0])*(a[1]-b[1]) - (a[0]-b[0])*(p[1]-b[1])
    d2 = (p[0]-c[0])*(b[1]-c[1]) - (b[0]-c[0])*(p[1]-c[1])
    d3 = (p[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(p[1]-a[1])
    # Strictly inside: all same sign, all magnitudes > eps
    return ((d1 >  eps) and (d2 >  eps) and (d3 >  eps)) or \
           ((d1 < -eps) and (d2 < -eps) and (d3 < -eps))


def _seg_intersect(a, b, c, d):
    """True if segments ab and cd properly cross (shared endpoints excluded)."""
    def ccw(p, q, r):
        return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    eps = 1e-9
    d1 = ccw(c, d, a)
    d2 = ccw(c, d, b)
    d3 = ccw(a, b, c)
    d4 = ccw(a, b, d)
    return ((d1 >  eps and d2 < -eps) or (d1 < -eps and d2 >  eps)) and \
           ((d3 >  eps and d4 < -eps) or (d3 < -eps and d4 >  eps))


def _bridge_one_hole(poly, hole, blocker_segs):
    """
    Bridge a CW hole into a CCW outer polygon. Picks the shortest visible
    bridge between any outer vertex and any hole vertex (segment must not
    cross poly edges, hole edges, or any blocker segment).
    """
    poly_segs = [(poly[i], poly[(i+1) % len(poly)]) for i in range(len(poly))]
    hole_segs = [(hole[i], hole[(i+1) % len(hole)]) for i in range(len(hole))]
    all_segs  = poly_segs + hole_segs + blocker_segs

    def shares_endpoint(s, p, q):
        sa, sb = s
        return ((abs(sa[0]-p[0]) < 1e-7 and abs(sa[1]-p[1]) < 1e-7) or
                (abs(sb[0]-p[0]) < 1e-7 and abs(sb[1]-p[1]) < 1e-7) or
                (abs(sa[0]-q[0]) < 1e-7 and abs(sa[1]-q[1]) < 1e-7) or
                (abs(sb[0]-q[0]) < 1e-7 and abs(sb[1]-q[1]) < 1e-7))

    candidates = []
    for oi, op in enumerate(poly):
        for hi, hp in enumerate(hole):
            d = (op[0]-hp[0])**2 + (op[1]-hp[1])**2
            candidates.append((d, oi, hi))
    candidates.sort()

    chosen_oi = chosen_hi = -1
    for _, oi, hi in candidates:
        op = poly[oi]; hp = hole[hi]
        blocked = False
        for s in all_segs:
            if shares_endpoint(s, op, hp):
                continue
            if _seg_intersect(op, hp, s[0], s[1]):
                blocked = True
                break
        if not blocked:
            chosen_oi, chosen_hi = oi, hi
            break
    if chosen_oi < 0:
        chosen_oi = candidates[0][1]
        chosen_hi = candidates[0][2]

    op = poly[chosen_oi]
    hole_rot = hole[chosen_hi:] + hole[:chosen_hi]
    return (poly[:chosen_oi+1] + hole_rot + [hole_rot[0]] + [op] + poly[chosen_oi+1:])


def _earclip(poly):
    """Ear-clip a simple CCW polygon (with possible zero-width slits).
    When the strict pit-test gets stuck, retries with the test disabled
    on the remaining sliver to push past degenerate slit configurations."""
    tris    = []
    indices = list(range(len(poly)))
    safety  = 12 * len(indices)
    strict  = True
    while len(indices) > 3 and safety > 0:
        safety -= 1
        n = len(indices)
        ear_at = -1
        # Pick the best convex ear (smallest area = least likely to enclose verts)
        best_score = None
        best_ii = -1
        for ii in range(n):
            ip = indices[(ii - 1) % n]
            ic = indices[ii]
            iN = indices[(ii + 1) % n]
            a, b, c = poly[ip], poly[ic], poly[iN]
            cross = (b[0]-a[0]) * (c[1]-a[1]) - (b[1]-a[1]) * (c[0]-a[0])
            if cross <= 1e-9:
                continue
            if strict:
                ok = True
                for jj in indices:
                    if jj == ip or jj == ic or jj == iN:
                        continue
                    pj = poly[jj]
                    if ((abs(pj[0]-a[0]) < 1e-7 and abs(pj[1]-a[1]) < 1e-7) or
                        (abs(pj[0]-b[0]) < 1e-7 and abs(pj[1]-b[1]) < 1e-7) or
                        (abs(pj[0]-c[0]) < 1e-7 and abs(pj[1]-c[1]) < 1e-7)):
                        continue
                    if _pit(pj, a, b, c):
                        ok = False
                        break
                if not ok:
                    continue
            # Score: prefer smaller triangle (less likely to enclose anything new)
            if best_score is None or cross < best_score:
                best_score = cross
                best_ii = ii
        if best_ii >= 0:
            ip = indices[(best_ii - 1) % len(indices)]
            ic = indices[best_ii]
            iN = indices[(best_ii + 1) % len(indices)]
            a, b, c = poly[ip], poly[ic], poly[iN]
            tris.append([a[2], b[2], c[2]])
            indices.pop(best_ii)
            ear_at = best_ii
        if ear_at < 0:
            if strict:
                strict = False  # Drop the pit-test, push past slits
                continue
            sys.stderr.write(f"  WARN: ear-clip stuck with {len(indices)} verts left\n")
            xs = [poly[i][0] for i in indices]
            ys = [poly[i][1] for i in indices]
            sys.stderr.write(f"    stuck region x:[{min(xs):.1f},{max(xs):.1f}] y:[{min(ys):.1f},{max(ys):.1f}]\n")
            break
    if len(indices) == 3:
        a = poly[indices[0]]; b = poly[indices[1]]; c = poly[indices[2]]
        tris.append([a[2], b[2], c[2]])
    return tris


def _point_in_polygon(p, poly):
    x, y = p[0], p[1]
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-30) + xi):
            inside = not inside
        j = i
    return inside


def triangulate_with_holes(outer, holes):
    """outer CCW, holes CW (from above). Entries are (x, y, vidx).
    Uses mapbox_earcut for a robust polygon-with-holes triangulation."""
    import mapbox_earcut as _earcut
    import numpy as _np
    all_pts = list(outer)
    ring_ends = [len(all_pts)]
    for h in holes:
        all_pts.extend(h)
        ring_ends.append(len(all_pts))
    verts = _np.array([[p[0], p[1]] for p in all_pts], dtype=_np.float64)
    rings = _np.array(ring_ends, dtype=_np.uint32)
    tris = _earcut.triangulate_float64(verts, rings)
    # Map flat triangle indices → real vertex indices (3rd elem of each pt)
    result = []
    for i in range(0, len(tris), 3):
        a, b, c = int(tris[i]), int(tris[i+1]), int(tris[i+2])
        result.append([all_pts[a][2], all_pts[b][2], all_pts[c][2]])
    return result


def apply_rim_taper(outer_rings, inner_rings):
    """
    Taper the outer wall over the top TAPER_H mm.
    The outer ring is pulled toward the inner ring using a smoothstep blend,
    leaving RIM_WALL_T of wall at z=0.  inner_rings is unchanged.
    Returns a new list of (possibly modified) outer_rings.
    """
    if TAPER_H <= 0:
        return outer_rings
    result = []
    for k, (outer, inner) in enumerate(zip(outer_rings, inner_rings)):
        z_avg = sum(p[2] for p in outer) / len(outer)
        if z_avg <= -TAPER_H:
            result.append(outer)
            continue
        # t: 0 at bottom of taper zone (-TAPER_H), 1 at rim (0)
        t = smoothstep((z_avg + TAPER_H) / TAPER_H)
        tapered = []
        for j in range(len(outer)):
            ox, oy, oz = outer[j]
            ix, iy, _  = inner[j]
            dx, dy = ox - ix, oy - iy
            gap = math.sqrt(dx*dx + dy*dy)
            # At rim (t=1) keep exactly RIM_WALL_T between outer and inner
            rim_scale = (RIM_WALL_T / gap) if gap > 1e-6 else 1.0
            scale = 1.0 - t * (1.0 - rim_scale)
            tapered.append((ix + dx * scale, iy + dy * scale, oz))
        result.append(tapered)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# STL / 3MF writers
# ─────────────────────────────────────────────────────────────────────────────

def write_stl(filepath, all_points, faces):
    with open(filepath, 'wb') as f:
        f.write(b'Binary STL - Ordovician Moss Tray'.ljust(80, b'\0'))
        f.write(struct.pack('<I', len(faces)))
        for face in faces:
            p0, p1, p2 = all_points[face[0]], all_points[face[1]], all_points[face[2]]
            u = (p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2])
            v = (p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2])
            n = normalize(cross(u, v))
            f.write(struct.pack('<3f', *n))
            f.write(struct.pack('<3f', *p0))
            f.write(struct.pack('<3f', *p1))
            f.write(struct.pack('<3f', *p2))
            f.write(struct.pack('<H', 0))


_CONTENT_TYPES = """\
<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>"""

_RELS = """\
<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel0"
    Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>"""


def write_3mf(filepath, all_points, faces):
    vertices_xml = "\n".join(
        f'        <vertex x="{p[0]:.4f}" y="{p[1]:.4f}" z="{p[2]:.4f}"/>'
        for p in all_points)
    triangles_xml = "\n".join(
        f'        <triangle v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>'
        for f in faces)
    model_xml = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US"
  xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
  <resources>
    <object id="1" type="model">
      <mesh>
        <vertices>
{vertices_xml}
        </vertices>
        <triangles>
{triangles_xml}
        </triangles>
      </mesh>
    </object>
  </resources>
  <build>
    <item objectid="1"/>
  </build>
</model>"""
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', _CONTENT_TYPES)
        zf.writestr('_rels/.rels', _RELS)
        zf.writestr('3D/3dmodel.model', model_xml)


# ─────────────────────────────────────────────────────────────────────────────
# Wall mesh builder
# ─────────────────────────────────────────────────────────────────────────────

def build_wall_mesh(outer_rings, inner_rings):
    """
    Build outer side + inner side (reversed winding) + top annulus faces.
    Does NOT close the bottom — callers add their own floor.
    outer_rings[0] / inner_rings[0] = top rim (z=0 in local coords).
    Returns (all_points, faces, n_outer_pts).
    """
    P = RING_PTS
    all_points = []
    for ring in outer_rings:
        all_points.extend(ring)
    n_outer_pts = len(all_points)
    for ring in inner_rings:
        all_points.extend(ring)

    faces = []
    n_o = len(outer_rings)
    n_i = len(inner_rings)

    # Outer side faces
    for i in range(n_o - 1):
        for j in range(P):
            j1 = (j + 1) % P
            a = i*P + j;       b = i*P + j1
            c = (i+1)*P + j1;  d = (i+1)*P + j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # Inner side faces (reversed winding → normal inward)
    for i in range(n_i - 1):
        for j in range(P):
            j1 = (j + 1) % P
            a = n_outer_pts + i*P + j
            b = n_outer_pts + i*P + j1
            c = n_outer_pts + (i+1)*P + j1
            d = n_outer_pts + (i+1)*P + j
            faces.append([a, c, b])
            faces.append([a, d, c])

    # Top annulus: outer[0] ↔ inner[0]
    for j in range(P):
        j1 = (j + 1) % P
        oa = j;          ob = j1
        ia = n_outer_pts + j; ib = n_outer_pts + j1
        faces.append([oa, ob, ib])
        faces.append([oa, ib, ia])

    return all_points, faces, n_outer_pts


# ─────────────────────────────────────────────────────────────────────────────
# Organic swoop nub
# ─────────────────────────────────────────────────────────────────────────────

def build_swoop_nub(cx, cy, z_base, n_rings=NUB_RING_STEPS, n_pts=NUB_PTS):
    """
    Organic tapered nub: wide at saucer floor, narrowing to flat top.
    No cantilever — radius always decreases from base to top.
    Profile: quadratic taper (fast near top, slow near base = swoop feel).
    """
    N = n_pts
    pts = []
    ring_starts = []

    for k in range(n_rings):
        t = k / (n_rings - 1)
        # Quadratic: stays wide near base, narrows quickly toward top
        r = lerp(NUB_BASE_R, NUB_TOP_R, t * t)
        z = z_base + NUB_TOTAL_H * t
        ring_starts.append(len(pts))
        for i in range(N):
            angle = 2.0 * math.pi * i / N
            pts.append((cx + r * math.cos(angle),
                        cy + r * math.sin(angle),
                        z))

    faces = []
    # Side strips
    for k in range(n_rings - 1):
        s0 = ring_starts[k]
        s1 = ring_starts[k + 1]
        for j in range(N):
            j1 = (j + 1) % N
            a, b, c, d = s0+j, s0+j1, s1+j1, s1+j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # Base cap (normal DOWN)
    ctr_base = len(pts)
    pts.append((cx, cy, z_base))
    for j in range(N):
        faces.append([ctr_base, ring_starts[0]+(j+1)%N, ring_starts[0]+j])

    # Top cap (normal UP)
    ctr_top = len(pts)
    pts.append((cx, cy, z_base + NUB_TOTAL_H))
    top_start = ring_starts[-1]
    for j in range(N):
        faces.append([ctr_top, top_start+j, top_start+(j+1)%N])

    return pts, faces


# ─────────────────────────────────────────────────────────────────────────────
# Through-hole cylinder helper (slicer cuts these from the floor)
# ─────────────────────────────────────────────────────────────────────────────

def _round_cylinder(cx, cy, z_top, height, radius, n_pts=16):
    N = n_pts
    def ring(z):
        return [(cx + radius * math.cos(2*math.pi*i/N),
                 cy + radius * math.sin(2*math.pi*i/N), z)
                for i in range(N)]
    top_ring = ring(z_top)
    bot_ring = ring(z_top - height)
    pts   = top_ring + bot_ring
    faces = []
    for j in range(N):
        j1 = (j+1) % N
        a, b, c, d = j, j1, N+j1, N+j
        faces.append([a, b, c])
        faces.append([a, c, d])
    ctr_t = len(pts); pts.append((cx, cy, z_top))
    for j in range(N):
        faces.append([ctr_t, j, (j+1)%N])
    ctr_b = len(pts); pts.append((cx, cy, z_top - height))
    for j in range(N):
        faces.append([ctr_b, N+(j+1)%N, N+j])
    return pts, faces


# ─────────────────────────────────────────────────────────────────────────────
# Moss Tray
# ─────────────────────────────────────────────────────────────────────────────

def build_moss_tray():
    print("Building moss tray…")
    _load_scad()

    # ── Outer rings: organic sandstone, z=0 to z=-TRAY_HEIGHT ────────────
    n_out_org = max(6, round(RING_PTS * TRAY_HEIGHT / BASELINE_HEIGHT))
    print(f"  Outer layers: {n_out_org}")

    outer_rings = []
    for k in range(n_out_org):
        frac    = k / (n_out_org - 1)
        z_local = -TRAY_HEIGHT * frac
        z_glob  =  TRAY_HEIGHT * frac
        L, W    = taper_dims(z_glob)
        ring    = sandstone_ring(z_local, L/2, W/2, frac)
        if k == 0 or k == n_out_org - 1:
            ring = [(p[0], p[1], z_local) for p in ring]
        outer_rings.append(ring)

    # ── Inner rings: outer organic offset inward (SAME XY pattern → uniform wall) ─
    inner_wall_h = TRAY_HEIGHT - FLOOR_T
    n_inn_org = max(5, round(RING_PTS * inner_wall_h / BASELINE_HEIGHT))
    inner_rings = []
    for k in range(n_inn_org):
        frac_inn = k / (n_inn_org - 1)
        z_local  = -inner_wall_h * frac_inn
        z_glob   =  inner_wall_h * frac_inn
        L, W     = taper_dims(z_glob)
        # Use the SAME frac the outer would use at this z so the organic
        # XY pattern aligns — guarantees uniform WALL_T thickness everywhere.
        frac_org = z_glob / TRAY_HEIGHT
        organic  = sandstone_ring(z_local, L/2, W/2, frac_org)
        inner_rings.append(offset_ring_inward(organic, WALL_T))

    # ── Rim taper: outer toward organic inner proxy aligned to outer z-levels ─
    inner_proxy = []
    for k in range(n_out_org):
        frac    = k / (n_out_org - 1)
        z_local = -TRAY_HEIGHT * frac
        z_glob  =  TRAY_HEIGHT * frac
        L, W    = taper_dims(z_glob)
        organic = sandstone_ring(z_local, L/2, W/2, frac)
        inner_proxy.append(offset_ring_inward(organic, WALL_T))
    outer_rings = apply_rim_taper(outer_rings, inner_proxy)

    # ── Pack wall vertices ────────────────────────────────────────────────
    P = RING_PTS
    all_points = []
    for r in outer_rings: all_points.extend(r)
    n_outer_pts = len(all_points)
    for r in inner_rings: all_points.extend(r)

    faces = []
    n_o = len(outer_rings)
    n_i = len(inner_rings)

    # Outer side faces (normal outward)
    for i in range(n_o - 1):
        for j in range(P):
            j1 = (j+1) % P
            a = i*P+j;       b = i*P+j1
            c = (i+1)*P+j1;  d = (i+1)*P+j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # Inner side faces (reversed winding → normal inward)
    for i in range(n_i - 1):
        for j in range(P):
            j1 = (j+1) % P
            a = n_outer_pts + i*P + j
            b = n_outer_pts + i*P + j1
            c = n_outer_pts + (i+1)*P + j1
            d = n_outer_pts + (i+1)*P + j
            faces.append([a, c, b])
            faces.append([a, d, c])

    # Top annulus (z=0): outer[0] ↔ inner[0]
    for j in range(P):
        j1 = (j+1) % P
        oa = j;              ob = j1
        ia = n_outer_pts+j;  ib = n_outer_pts+j1
        faces.append([oa, ob, ib])
        faces.append([oa, ib, ia])

    # ── Hole specs: (cx, cy, radius, n_pts) ──────────────────────────────
    holes_spec = []
    for (nx, ny) in NUB_POSITIONS:
        holes_spec.append((nx, ny, NUB_RECEIVER_R, 16))
    # 4×3 grid of drain holes, spread across the floor, clear of nub receivers
    drain_xs = [-55.0, -22.0, 22.0, 55.0]
    drain_ys = [-18.0, 0.0, 18.0]
    for dx in drain_xs:
        for dy in drain_ys:
            holes_spec.append((dx, dy, DRAIN_HOLE_R, DRAIN_HOLE_PTS))

    z_top_floor = -inner_wall_h        # interior surface of floor
    z_bot_floor = -TRAY_HEIGHT         # exterior bottom

    top_outer_start = n_outer_pts + (n_i - 1) * P
    bot_outer_start = (n_o - 1) * P

    # Emit hole ring vertices (top and bottom), CW from above so they read
    # as proper holes in CCW outer boundaries.
    hole_top_idx = []
    hole_bot_idx = []
    for (hx, hy, hr, hn) in holes_spec:
        top_start = len(all_points)
        for ii in range(hn):
            ang = -2.0 * math.pi * ii / hn   # CW from above
            all_points.append((hx + hr * math.cos(ang),
                               hy + hr * math.sin(ang),
                               z_top_floor))
        hole_top_idx.append(list(range(top_start, top_start + hn)))

        bot_start = len(all_points)
        for ii in range(hn):
            ang = -2.0 * math.pi * ii / hn
            all_points.append((hx + hr * math.cos(ang),
                               hy + hr * math.sin(ang),
                               z_bot_floor))
        hole_bot_idx.append(list(range(bot_start, bot_start + hn)))

    # ── Triangulate top floor cap (normal UP) ────────────────────────────
    top_outer = [(all_points[top_outer_start + j][0],
                  all_points[top_outer_start + j][1],
                  top_outer_start + j) for j in range(P)]
    top_holes = []
    for k, (hx, hy, hr, hn) in enumerate(holes_spec):
        top_holes.append([(all_points[hole_top_idx[k][m]][0],
                           all_points[hole_top_idx[k][m]][1],
                           hole_top_idx[k][m]) for m in range(hn)])
    print("  Triangulating interior floor…")
    top_tris = triangulate_with_holes(top_outer, top_holes)
    faces.extend(top_tris)

    # ── Triangulate bottom floor cap (normal DOWN → reverse winding) ─────
    bot_outer = [(all_points[bot_outer_start + j][0],
                  all_points[bot_outer_start + j][1],
                  bot_outer_start + j) for j in range(P)]
    bot_holes = []
    for k, (hx, hy, hr, hn) in enumerate(holes_spec):
        bot_holes.append([(all_points[hole_bot_idx[k][m]][0],
                           all_points[hole_bot_idx[k][m]][1],
                           hole_bot_idx[k][m]) for m in range(hn)])
    print("  Triangulating exterior bottom…")
    bot_tris = triangulate_with_holes(bot_outer, bot_holes)
    for tri in bot_tris:
        faces.append([tri[0], tri[2], tri[1]])

    # ── Hole cylinder walls (top ↔ bottom, normals inward) ───────────────
    for k, (hx, hy, hr, hn) in enumerate(holes_spec):
        top_ring = hole_top_idx[k]
        bot_ring = hole_bot_idx[k]
        for ii in range(hn):
            i1 = (ii + 1) % hn
            t0, t1 = top_ring[ii], top_ring[i1]
            b0, b1 = bot_ring[ii], bot_ring[i1]
            # Winding chosen so face normals point into the hole interior
            faces.append([t0, b0, b1])
            faces.append([t0, b1, t1])

    print(f"  Points: {len(all_points):,}  Faces: {len(faces):,}")
    return all_points, faces


# ─────────────────────────────────────────────────────────────────────────────
# Drip Tray
# ─────────────────────────────────────────────────────────────────────────────

def build_drip_tray():
    print("Building drip tray…")
    _load_scad()

    z_off_glob = TRAY_HEIGHT   # saucer top is 40 mm down the global taper

    # ── Outer rings (full saucer height: z=0 to z=-18) ───────────────────
    n_out_org = max(4, round(RING_PTS * SAUCER_HEIGHT / BASELINE_HEIGHT))
    outer_rings = []
    for k in range(n_out_org):
        frac    = k / (n_out_org - 1)
        z_local = -SAUCER_HEIGHT * frac
        z_glob  =  z_off_glob + SAUCER_HEIGHT * frac
        L, W    = taper_dims(z_glob)
        ring    = sandstone_ring(z_local, L/2, W/2, frac)
        if k == 0 or k == n_out_org - 1:
            ring = [(p[0], p[1], z_local) for p in ring]
        outer_rings.append(ring)

    # ── Inner rings: SMOOTH ellipse (wall height only z=0 to z=-SAUCER_WALL)
    n_inn_org = max(3, round(RING_PTS * SAUCER_WALL / BASELINE_HEIGHT))
    inner_rings = []
    for k in range(n_inn_org):
        frac_inn = k / (n_inn_org - 1)
        z_local  = -SAUCER_WALL * frac_inn
        z_glob   =  z_off_glob + SAUCER_WALL * frac_inn
        L, W     = taper_dims(z_glob)
        # Match outer's SCAD frac at this z (outer uses k/(n-1) over SAUCER_HEIGHT)
        frac_org = (-z_local) / SAUCER_HEIGHT
        organic  = sandstone_ring(z_local, L/2, W/2, frac_org)
        inner_rings.append(offset_ring_inward(organic, WALL_T))

    # ── Rim taper (outer toward organic inner proxy aligned to outer z-levels) ─
    inner_proxy = []
    for k in range(n_out_org):
        frac    = k / (n_out_org - 1)
        z_local = -SAUCER_HEIGHT * frac
        z_glob  =  z_off_glob + SAUCER_HEIGHT * frac
        L, W    = taper_dims(z_glob)
        organic = sandstone_ring(z_local, L/2, W/2, frac)
        inner_proxy.append(offset_ring_inward(organic, WALL_T))
    outer_rings = apply_rim_taper(outer_rings, inner_proxy)

    # ── Pack points ───────────────────────────────────────────────────────
    P = RING_PTS
    all_points = []
    for r in outer_rings: all_points.extend(r)
    n_outer_pts = len(all_points)
    for r in inner_rings: all_points.extend(r)

    faces = []
    n_o = len(outer_rings)
    n_i = len(inner_rings)

    # Outer side faces
    for i in range(n_o - 1):
        for j in range(P):
            j1 = (j+1) % P
            a = i*P+j;       b = i*P+j1
            c = (i+1)*P+j1;  d = (i+1)*P+j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # Inner side faces (reversed winding)
    for i in range(n_i - 1):
        for j in range(P):
            j1 = (j+1) % P
            a = n_outer_pts + i*P + j
            b = n_outer_pts + i*P + j1
            c = n_outer_pts + (i+1)*P + j1
            d = n_outer_pts + (i+1)*P + j
            faces.append([a, c, b])
            faces.append([a, d, c])

    # Top annulus (z=0): outer[0] ↔ inner[0]
    for j in range(P):
        j1 = (j+1) % P
        oa = j;              ob = j1
        ia = n_outer_pts+j;  ib = n_outer_pts+j1
        faces.append([oa, ob, ib])
        faces.append([oa, ib, ia])

    # Exterior bottom cap (z=-SAUCER_HEIGHT): fan normal DOWN
    bot_start   = (n_o - 1) * P
    ctr_bot     = len(all_points)
    all_points.append((0.0, 0.0, -SAUCER_HEIGHT))
    for j in range(P):
        j1 = (j+1) % P
        faces.append([ctr_bot, bot_start+j1, bot_start+j])

    # Interior floor cap (z=-SAUCER_WALL): fan normal UP (into cavity)
    last_inn    = n_outer_pts + (n_i - 1) * P
    ctr_floor   = len(all_points)
    all_points.append((0.0, 0.0, -SAUCER_WALL))
    for j in range(P):
        j1 = (j+1) % P
        faces.append([ctr_floor, last_inn+j, last_inn+j1])

    # ── Swoop nubs ────────────────────────────────────────────────────────
    z_nub_base = -SAUCER_WALL   # nubs rise from interior floor level
    for (nx, ny) in NUB_POSITIONS:
        nub_pts, nub_faces = build_swoop_nub(nx, ny, z_nub_base)
        base = len(all_points)
        all_points.extend(nub_pts)
        faces.extend([[base+f[0], base+f[1], base+f[2]] for f in nub_faces])

    print(f"  Points: {len(all_points):,}  Faces: {len(faces):,}")
    return all_points, faces


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--piece', choices=['tray', 'drip', 'both'],
                        default='both')
    args = parser.parse_args()

    if args.piece in ('tray', 'both'):
        pts, faces = build_moss_tray()
        stl_path = SCRIPT_DIR / 'moss_tray.stl'
        mf_path  = SCRIPT_DIR / 'moss_tray.3mf'
        write_stl(str(stl_path), pts, faces)
        write_3mf(str(mf_path),  pts, faces)
        print(f"  ✓ {stl_path.name}  ({os.path.getsize(stl_path)/1024/1024:.1f} MB)")
        print(f"  ✓ {mf_path.name}")

    if args.piece in ('drip', 'both'):
        pts, faces = build_drip_tray()
        stl_path = SCRIPT_DIR / 'drip_tray.stl'
        mf_path  = SCRIPT_DIR / 'drip_tray.3mf'
        write_stl(str(stl_path), pts, faces)
        write_3mf(str(mf_path),  pts, faces)
        print(f"  ✓ {stl_path.name}  ({os.path.getsize(stl_path)/1024/1024:.1f} MB)")
        print(f"  ✓ {mf_path.name}")

    print("\nDone.")


if __name__ == '__main__':
    main()
