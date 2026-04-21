#!/usr/bin/env python3
"""
Parametric Sandstone Strata Cylinder Generator
===============================================
Reads the original Illinois Sandstone SCAD polyhedron and regenerates it
with parametric control over:
  - target_height  : total height in mm (baseline = 120mm)
  - num_layers     : number of strata ring-layers (baseline = 110)

The generator preserves the original organic form and strata flow by
interpolating between the original rings when adding/removing layers,
and scaling in the vertical (Z) axis only.

Usage examples:
  # Default (120mm, 110 layers) - recreate original
  python3 generate_sandstone.py

  # Taller model (180mm) with same number of strata layers (layers get thicker)
  python3 generate_sandstone.py --height 180

  # Same height but twice the strata detail
  python3 generate_sandstone.py --layers 220

  # 50% scale (60mm) with proportionally fewer layers
  python3 generate_sandstone.py --height 60 --layers 55

  # Use a percentage of baseline height
  python3 generate_sandstone.py --height-percent 150

  # Use a scale factor
  python3 generate_sandstone.py --height-scale 0.75

  # Output to specific file
  python3 generate_sandstone.py --height 200 -o my_tall_sandstone.scad

  # Hollow tube with 2mm wall (default)
  python3 generate_sandstone.py --hollow

  # Hollow with custom wall thickness
  python3 generate_sandstone.py --wall 3.5

  # Tall hollow vase
  python3 generate_sandstone.py --height 200 --wall 2.5

  # Hollow with solid base (default 2mm)
  python3 generate_sandstone.py --hollow --base

  # Hollow with precise solid base height
  python3 generate_sandstone.py --hollow --base 9.46

  # Hollow with solid base + center hole (default 2mm diameter)
  python3 generate_sandstone.py --hollow --base 9.46 --base-hole

  # Hollow with solid base + 79mm center hole
  python3 generate_sandstone.py --hollow --base 9.46 --base-hole 79

  # Sharp, pronounced strata ledges (more dramatic effect)
  python3 generate_sandstone.py --height 180 --sharp

  # Vase mode: create a cylindrical vase for a 78mm × 176mm cylinder
  # with 3mm wall and 3mm base
  python3 generate_sandstone.py --vase --vase-interior-diameter 78 \\
                                 --vase-interior-height 176 \\
                                 --vase-wall 3 --vase-base 3
"""

import argparse
import math
import os
import re
import struct
import sys
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────
BASELINE_HEIGHT = 120.0       # mm – original model height
BASELINE_NUM_LAYERS = 111     # original ring count (0 through 110)
POINTS_PER_RING = 120         # angular samples per ring (3° spacing)
SCRIPT_DIR = Path(__file__).parent
DEFAULT_SOURCE = SCRIPT_DIR / ".." / "raw" / "1-illinois_sandstone_cylinder_v3.scad"


# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_original_scad(filepath):
    """Parse the original SCAD polyhedron into structured ring data.

    The original model has 111 rings of 120 points each (3° angular
    spacing, 0° through 357°) plus two center points.

    Returns:
        rings       : list of lists – rings[i][j] = (x, y, z)
        center_bot  : (x, y, z) – bottom center point
        center_top  : (x, y, z) – top center point
        ring_avg_z  : list of float – average Z per ring
    """
    points = []
    point_re = re.compile(r'\[\s*([^,]+),\s*([^,]+),\s*([^\]]+)\]')

    with open(filepath) as f:
        for line in f:
            if 'faces' in line and '=' in line:
                break
            m = point_re.search(line)
            if m:
                x = float(m.group(1))
                y = float(m.group(2))
                z = float(m.group(3))
                points.append((x, y, z))

    total = len(points)
    n_ring_points = BASELINE_NUM_LAYERS * POINTS_PER_RING  # 13310

    # Structured data
    rings = []
    ring_avg_z = []
    for i in range(BASELINE_NUM_LAYERS):
        start = i * POINTS_PER_RING
        end = start + POINTS_PER_RING
        ring = points[start:end]
        rings.append(ring)
        avg_z = sum(p[2] for p in ring) / POINTS_PER_RING
        ring_avg_z.append(avg_z)

    # Center points (last two)
    center_bot = points[total - 2]   # (0, 0, 0)
    center_top = points[total - 1]   # (0, 0, 120)

    return rings, center_bot, center_top, ring_avg_z


# ── Interpolation ────────────────────────────────────────────────────────────

def lerp(a, b, t):
    """Linear interpolation between scalars a and b."""
    return a + (b - a) * t


def lerp_point(p1, p2, t):
    """Linearly interpolate between two 3D points."""
    return (lerp(p1[0], p2[0], t),
            lerp(p1[1], p2[1], t),
            lerp(p1[2], p2[2], t))


def interpolate_rings(original_rings, ring_avg_z, num_new_layers, target_height,
                      sharp=False):
    """Generate new rings by interpolating original ring data.

    Two modes:
      sharp=False (default):
        XY profiles are linearly blended between the two bracketing
        original rings.  Produces smooth, natural strata that match the
        look of the original model.

      sharp=True:
        XY profiles snap to the NEAREST original ring (nearest-neighbor).
        Creates crisp, pronounced ledges — a more dramatic strata effect.

    In both modes, Z is positioned at the correct height for the target
    scale, with the original per-vertex Z undulation offset preserved
    proportionally.
    """
    n_orig = len(original_rings)
    z_scale = target_height / BASELINE_HEIGHT
    new_rings = []

    for k in range(num_new_layers):
        # Normalized position [0, 1]
        if num_new_layers == 1:
            t_new = 0.5
        else:
            t_new = k / (num_new_layers - 1)

        # Map to original ring index space [0, n_orig - 1]
        orig_pos = t_new * (n_orig - 1)
        i_lo = int(math.floor(orig_pos))
        i_hi = min(i_lo + 1, n_orig - 1)
        alpha = orig_pos - i_lo

        # For sharp mode: snap to the nearest original ring for XY
        if sharp:
            i_nearest = i_lo if alpha < 0.5 else i_hi

        ring = []
        for j in range(POINTS_PER_RING):
            if sharp:
                # Nearest-neighbor: exact XY from closest original ring
                p_src = original_rings[i_nearest][j]
                x = p_src[0]
                y = p_src[1]
            else:
                # Linear blend of XY between bracketing rings (default)
                p_lo = original_rings[i_lo][j]
                p_hi = original_rings[i_hi][j]
                x = lerp(p_lo[0], p_hi[0], alpha)
                y = lerp(p_lo[1], p_hi[1], alpha)

            # Z: interpolate then scale (always smooth for vertical position)
            p_lo = original_rings[i_lo][j]
            p_hi = original_rings[i_hi][j]
            z_interp = lerp(p_lo[2], p_hi[2], alpha)
            z = z_interp * z_scale

            ring.append((x, y, z))

        new_rings.append(ring)

    return new_rings


# ── Vase Generation ──────────────────────────────────────────────────────────

def generate_vase_rings(interior_diameter, interior_height, wall_thickness, num_layers):
    """Generate rings for a simple cylindrical vase.
    
    Creates a uniformly cylindrical vase sized to contain an interior cylinder.
    The exterior diameter is interior_diameter + 2*wall_thickness.
    
    Args:
        interior_diameter : diameter of the interior cavity (mm)
        interior_height   : height of the interior cavity (mm)
        wall_thickness    : wall thickness (mm)
        num_layers        : number of rings to generate
        
    Returns:
        rings : list of ring point lists
    """
    exterior_radius = (interior_diameter + 2 * wall_thickness) / 2.0
    
    rings = []
    for i in range(num_layers):
        # Normalize height position [0, 1]
        if num_layers == 1:
            t = 0.5
        else:
            t = i / (num_layers - 1)
        
        z = t * interior_height
        
        # Generate ring of points at this height on the exterior cylinder
        ring = []
        for j in range(POINTS_PER_RING):
            angle = 2.0 * math.pi * j / POINTS_PER_RING
            x = exterior_radius * math.cos(angle)
            y = exterior_radius * math.sin(angle)
            ring.append((x, y, z))
        
        rings.append(ring)
    
    return rings


# ── Face Generation ──────────────────────────────────────────────────────────

def generate_faces(total_rings, pts_per_ring, center_bot_idx, center_top_idx):
    """Generate triangle faces for the cylinder mesh.

    The ring layout in the point array is:
      ring 0        = flat bottom cap ring  (z = 0)
      ring 1..N-2   = organic strata rings
      ring N-1      = flat top cap ring     (z = target_height)

    Returns list of [a, b, c] index triples.
    """
    faces = []
    P = pts_per_ring

    # ── Side faces: stitch all adjacent rings (including cap-to-organic) ──
    for i in range(total_rings - 1):
        for j in range(P):
            j_next = (j + 1) % P

            a = i * P + j
            b = i * P + j_next
            c = (i + 1) * P + j_next
            d = (i + 1) * P + j

            # Two triangles per quad
            faces.append([a, b, c])
            faces.append([a, c, d])

    # ── Bottom cap: fan from center to flat bottom ring (ring 0) ─────────
    for j in range(P):
        j_next = (j + 1) % P
        faces.append([center_bot_idx, j_next, j])

    # ── Top cap: fan from center to flat top ring (last ring) ────────────
    last_ring_start = (total_rings - 1) * P
    for j in range(P):
        j_next = (j + 1) % P
        faces.append([center_top_idx, last_ring_start + j, last_ring_start + j_next])

    return faces


# ── Mesh Building ────────────────────────────────────────────────────────────

def build_mesh(new_rings, target_height):
    """Build the complete mesh (points + faces) with flat cap rings.

    Returns:
        all_points : list of (x, y, z) tuples
        faces      : list of [a, b, c] index triples
    """
    P = POINTS_PER_RING

    # Build flat cap rings from the XY of the first/last organic rings
    # This eliminates top/bottom artifacts from organic Z-undulation
    first_organic = new_rings[0]
    last_organic = new_rings[-1]
    flat_bottom_ring = [(p[0], p[1], 0.0) for p in first_organic]
    flat_top_ring = [(p[0], p[1], target_height) for p in last_organic]

    # Full ring list: flat_bottom + organic layers + flat_top
    all_rings = [flat_bottom_ring] + list(new_rings) + [flat_top_ring]
    total_rings = len(all_rings)  # N_organic + 2

    # Flatten ring points
    all_points = []
    for ring in all_rings:
        all_points.extend(ring)

    # Add center points
    center_bot = (0.0, 0.0, 0.0)
    center_top = (0.0, 0.0, target_height)
    center_bot_idx = len(all_points)
    all_points.append(center_bot)
    center_top_idx = len(all_points)
    all_points.append(center_top)

    # Generate faces
    faces = generate_faces(total_rings, P, center_bot_idx, center_top_idx)

    return all_points, faces


def offset_ring_inward(ring, wall_thickness):
    """Offset a ring of (x, y, z) points inward by wall_thickness in XY.

    For each point, computes the direction from the ring's XY centroid
    to the point and moves it inward along that direction.
    This preserves the organic profile shape on the inner wall.
    """
    # Compute XY centroid of the ring
    cx = sum(p[0] for p in ring) / len(ring)
    cy = sum(p[1] for p in ring) / len(ring)

    inner_ring = []
    for (x, y, z) in ring:
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 1e-9:
            # Point is at centroid – can't offset, keep as-is
            inner_ring.append((x, y, z))
        else:
            # Unit vector from centroid to point
            ux = dx / dist
            uy = dy / dist
            # Move inward (toward centroid)
            new_x = x - ux * wall_thickness
            new_y = y - uy * wall_thickness
            inner_ring.append((new_x, new_y, z))

    return inner_ring


def generate_hole_ring_matched(reference_ring, hole_radius, z):
    """Generate a hole ring with the same number of points and angular
    positions as *reference_ring*, but at *hole_radius* from the Z axis.

    This guarantees a clean 1:1 stitch with no degenerate triangles
    or seam artefacts, because every outer/inner ring point has a
    directly corresponding hole-ring point on the same radial line.
    """
    ring = []
    for (x, y, _) in reference_ring:
        angle = math.atan2(y, x)
        hx = hole_radius * math.cos(angle)
        hy = hole_radius * math.sin(angle)
        ring.append((hx, hy, z))
    return ring


def build_hollow_vase_mesh(outer_rings, inner_diameter, target_height, solid_base=0.0):
    """Build a manifold hollow vase: organic sandstone outer shell, cylindrical inner bore.

    Strategy for a watertight manifold mesh
    ─────────────────────────────────────────
    We keep the inner ring Z values **identical** to the corresponding
    outer ring Z values (point-for-point).  This avoids T-junctions and
    non-manifold edges caused by mismatched heights.

    Layout
    ──────
    Ring index k spans 0 … N-1 where
        ring 0      = flat cap at z=0          (outer + inner)
        rings 1..N-2 = organic strata           (outer + inner)
        ring N-1    = flat cap at z=H           (outer + inner)

    Point array layout
    ──────────────────
    [0  … N_outer-1]  outer rings flattened  (N rings × P pts)
    [N_outer … end]   inner rings flattened  (N rings × P pts)

    Faces
    ─────
    1. Outer side quads  (outward-facing)
    2. Inner side quads  (inward-facing, reversed winding)
    3. Bottom annulus    (downward-facing) — outer ring 0 ↔ inner ring 0
    4. Top annulus       (upward-facing)   — outer ring N-1 ↔ inner ring N-1
    5. Floor annulus     (upward-facing)   — at z≈solid_base, outer ↔ inner
       + vertical inner wall from z=0 to z=solid_base if solid_base > 0
    """
    P = POINTS_PER_RING
    inner_radius = inner_diameter / 2.0

    # ── Build outer ring list ──────────────────────────────────────────
    # Force first ring to z=0 and last ring to z=target_height
    # so cap faces never share edges with side faces.
    all_outer = []
    for k, ring in enumerate(outer_rings):
        if k == 0:
            all_outer.append([(p[0], p[1], 0.0) for p in ring])
        elif k == len(outer_rings) - 1:
            all_outer.append([(p[0], p[1], target_height) for p in ring])
        else:
            all_outer.append(list(ring))
    N = len(all_outer)   # total ring count

    # ── Build matching inner rings: same Z as outer, but at inner_radius ─
    all_inner = []
    for ring in all_outer:
        inner_ring = []
        for (x, y, z) in ring:
            angle = math.atan2(y, x)
            inner_ring.append((inner_radius * math.cos(angle),
                                inner_radius * math.sin(angle),
                                z))
        all_inner.append(inner_ring)

    # ── Flatten points ─────────────────────────────────────────────────
    all_points = []
    for ring in all_outer:
        all_points.extend(ring)
    O = len(all_points)          # offset to first inner point
    for ring in all_inner:
        all_points.extend(ring)

    def o(ring_i, j):   # outer point index
        return ring_i * P + j
    def inn(ring_i, j): # inner point index
        return O + ring_i * P + j

    faces = []

    # ── Pre-compute floor_idx if solid base ────────────────────────────
    def avg_z(ring):
        return sum(p[2] for p in ring) / len(ring)

    if solid_base > 0:
        floor_idx = 1
        for idx in range(1, N):
            if avg_z(all_outer[idx]) >= solid_base - 1e-6:
                floor_idx = idx
                break
    else:
        floor_idx = 0

    faces = []

    # ── 1. Outer side quads ────────────────────────────────────────────
    for i in range(N - 1):
        for j in range(P):
            jn = (j + 1) % P
            a, b = o(i, j),    o(i, jn)
            c, d = o(i+1, jn), o(i+1, j)
            faces.append([a, b, c])
            faces.append([a, c, d])

    # ── 2. Inner side quads (only above floor) ──────────────────────────
    inner_start = floor_idx if solid_base > 0 else 0
    for i in range(inner_start, N - 1):
        for j in range(P):
            jn = (j + 1) % P
            a, b = inn(i, j),    inn(i, jn)
            c, d = inn(i+1, jn), inn(i+1, j)
            faces.append([a, c, b])
            faces.append([a, d, c])

    # ── 3. Bottom face ──────────────────────────────────────────────────
    if solid_base > 0:
        # Solid base: bottom is a full disc (outer ring 0 fanned to center)
        center_bot_idx = len(all_points)
        all_points.append((0.0, 0.0, 0.0))
        for j in range(P):
            jn = (j + 1) % P
            faces.append([center_bot_idx, o(0, jn), o(0, j)])
    else:
        # Open tube: bottom is an annulus outer↔inner at z=0
        for j in range(P):
            jn = (j + 1) % P
            faces.append([o(0, j),  inn(0, j),  inn(0, jn)])
            faces.append([o(0, j),  inn(0, jn), o(0, jn)])

    # ── 4. Top annulus (z=H face, looking upward) ──────────────────────
    for j in range(P):
        jn = (j + 1) % P
        faces.append([o(N-1, j),  o(N-1, jn),  inn(N-1, jn)])
        faces.append([o(N-1, j),  inn(N-1, jn), inn(N-1, j)])

    # ── 5. Solid base floor ─────────────────────────────────────────────
    if solid_base > 0:
        # Floor disc: fan from inn(floor_idx) ring down to a center point.
        # This is entirely within the inner cylinder — no outer ring edges
        # are reused, so no manifold violations.
        floor_z = avg_z(all_inner[floor_idx])
        center_floor_idx = len(all_points)
        all_points.append((0.0, 0.0, floor_z))

        for j in range(P):
            jn = (j + 1) % P
            # Upward-facing (CCW from above)
            faces.append([center_floor_idx, inn(floor_idx, j), inn(floor_idx, jn)])

    return all_points, faces


    """Build a hollow tube mesh with inner and outer walls.

    Structure:
      - Outer shell: flat_bottom + organic rings + flat_top (faces outward)
      - Inner shell: offset inward, starting at z = solid_base
      - If solid_base > 0: solid bottom disc at z=0 + inner floor at z=solid_base
        If base_hole_diameter > 0: both discs become annuli with a cylindrical
        tube connecting the holes through the solid base
      - If solid_base == 0: bottom is an annulus (open tube)
      - Top annulus: connects outer last ring to inner last ring

    Returns:
        all_points : list of (x, y, z) tuples
        faces      : list of [a, b, c] index triples
    """
    P = POINTS_PER_RING

    # ── Outer rings (same as solid) ──────────────────────────────────────
    first_organic = new_rings[0]
    last_organic = new_rings[-1]
    flat_bottom_outer = [(p[0], p[1], 0.0) for p in first_organic]
    flat_top_outer = [(p[0], p[1], target_height) for p in last_organic]
    outer_rings = [flat_bottom_outer] + list(new_rings) + [flat_top_outer]
    total_outer_rings = len(outer_rings)

    # ── Determine which outer rings are above the solid base ─────────────
    def ring_avg_z(ring):
        return sum(p[2] for p in ring) / len(ring)

    inner_start_idx = 0
    if solid_base > 0:
        for idx, ring in enumerate(outer_rings):
            if ring_avg_z(ring) >= solid_base - 1e-6:
                inner_start_idx = idx
                break
        else:
            inner_start_idx = total_outer_rings

    inner_source_rings = outer_rings[inner_start_idx:]

    # ── Build inner rings (offset inward) ────────────────────────────────
    inner_rings_offset = [offset_ring_inward(ring, wall_thickness) for ring in inner_source_rings]

    # If solid_base > 0, force the first inner ring to sit at z = solid_base
    if solid_base > 0 and len(inner_rings_offset) > 0:
        inner_rings_offset[0] = [
            (p[0], p[1], solid_base) for p in inner_rings_offset[0]
        ]

    total_inner_rings = len(inner_rings_offset)

    # ── Flatten all points ───────────────────────────────────────────────
    all_points = []
    for ring in outer_rings:
        all_points.extend(ring)
    outer_count = len(all_points)

    for ring in inner_rings_offset:
        all_points.extend(ring)

    faces = []

    # ── Outer side faces (normal outward) ────────────────────────────────
    for i in range(total_outer_rings - 1):
        for j in range(P):
            j_next = (j + 1) % P
            a = i * P + j
            b = i * P + j_next
            c = (i + 1) * P + j_next
            d = (i + 1) * P + j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # ── Inner side faces (normal inward = reversed winding) ──────────────
    for i in range(total_inner_rings - 1):
        for j in range(P):
            j_next = (j + 1) % P
            a = outer_count + i * P + j
            b = outer_count + i * P + j_next
            c = outer_count + (i + 1) * P + j_next
            d = outer_count + (i + 1) * P + j
            faces.append([a, c, b])
            faces.append([a, d, c])

    # ── Bottom closure ───────────────────────────────────────────────────
    hole_radius = base_hole_diameter / 2.0 if base_hole_diameter > 0 else 0.0

    if solid_base > 0:
        if hole_radius > 0:
            # Use outer ring 0 angles for both hole rings so the hole
            # cylinder is perfectly aligned and every point has a direct
            # 1:1 partner — no mismatched-count stitching, no seam.
            outer_ring_0 = all_points[0:P]

            # ── Bottom annulus: outer ring 0 → hole ring at z=0 ──────
            hole_bot_ring = generate_hole_ring_matched(
                outer_ring_0, hole_radius, 0.0)
            hole_bot_start = len(all_points)
            all_points.extend(hole_bot_ring)

            for j in range(P):
                j_next = (j + 1) % P
                # Downward-facing normal (CW from above)
                faces.append([j, hole_bot_start + j,
                              hole_bot_start + j_next])
                faces.append([j, hole_bot_start + j_next, j_next])

            # ── Inner floor annulus: inner ring 0 → hole at z=base ───
            hole_floor_ring = generate_hole_ring_matched(
                outer_ring_0, hole_radius, solid_base)
            hole_floor_start = len(all_points)
            all_points.extend(hole_floor_ring)

            inner_floor_start = outer_count
            for j in range(P):
                j_next = (j + 1) % P
                # Upward-facing normal (CCW from above)
                faces.append([inner_floor_start + j,
                              inner_floor_start + j_next,
                              hole_floor_start + j_next])
                faces.append([inner_floor_start + j,
                              hole_floor_start + j_next,
                              hole_floor_start + j])

            # ── Hole tube: connect z=0 ring to z=base ring ──────────
            for j in range(P):
                j_next = (j + 1) % P
                a = hole_bot_start + j
                b = hole_bot_start + j_next
                c = hole_floor_start + j_next
                d = hole_floor_start + j
                # Inward-facing normals (toward Z axis)
                faces.append([a, d, c])
                faces.append([a, c, b])
        else:
            # Solid bottom disc: fan from a center point at z=0
            center_bot = (0.0, 0.0, 0.0)
            center_bot_idx = len(all_points)
            all_points.append(center_bot)
            for j in range(P):
                j_next = (j + 1) % P
                faces.append([center_bot_idx, j_next, j])

            # Inner floor disc: fan from center at z = solid_base
            center_floor = (0.0, 0.0, solid_base)
            center_floor_idx = len(all_points)
            all_points.append(center_floor)
            inner_floor_start = outer_count
            for j in range(P):
                j_next = (j + 1) % P
                faces.append([center_floor_idx, inner_floor_start + j, inner_floor_start + j_next])

        # Annular wall connecting outer ring at inner_start_idx to inner ring 0
        outer_lip_start = inner_start_idx * P
        inner_lip_start = outer_count
        for j in range(P):
            j_next = (j + 1) % P
            o_a = outer_lip_start + j
            o_b = outer_lip_start + j_next
            i_a = inner_lip_start + j
            i_b = inner_lip_start + j_next
            faces.append([o_a, i_a, i_b])
            faces.append([o_a, i_b, o_b])
    else:
        # No solid base: bottom annulus
        for j in range(P):
            j_next = (j + 1) % P
            o_a = j
            o_b = j_next
            i_a = outer_count + j
            i_b = outer_count + j_next
            faces.append([o_a, i_a, i_b])
            faces.append([o_a, i_b, o_b])

    # ── Top annulus (connects outer last ring to inner last ring) ────────
    top_outer_start = (total_outer_rings - 1) * P
    top_inner_start = outer_count + (total_inner_rings - 1) * P
    for j in range(P):
        j_next = (j + 1) % P
        o_a = top_outer_start + j
        o_b = top_outer_start + j_next
        i_a = top_inner_start + j
        i_b = top_inner_start + j_next
        faces.append([o_a, o_b, i_b])
        faces.append([o_a, i_b, i_a])

    return all_points, faces


# ── SCAD Output ──────────────────────────────────────────────────────────────

def write_scad(filepath, all_points, faces, target_height, num_layers):
    """Write a complete parametric OpenSCAD file."""
    with open(filepath, 'w') as f:
        f.write(f"""\
// ═══════════════════════════════════════════════════════════════════════════
// Parametric Illinois Sandstone Strata Cylinder
// ═══════════════════════════════════════════════════════════════════════════
//
// Generated by generate_sandstone.py
// Baseline: {BASELINE_HEIGHT}mm tall, {BASELINE_NUM_LAYERS} strata layers,
//           {POINTS_PER_RING} angular points per ring
//
// This file was generated with:
//   target_height = {target_height} mm
//   num_layers    = {num_layers}
//
// ── OpenSCAD Fine-Tuning Parameter ──────────────────────────────────────
// Adjust this to make small height tweaks without regenerating.
// 1.0 = no change from the generated height.

/* [Height Fine-Tuning] */
fine_tune_scale = 1.0;  // [0.25:0.01:4.0]

// ── Render ──────────────────────────────────────────────────────────────

scale([1, 1, fine_tune_scale])
""")
        f.write("polyhedron(\n")
        f.write("  points = [\n")

        # Write points
        for idx, (x, y, z) in enumerate(all_points):
            comma = "," if idx < len(all_points) - 1 else ""
            f.write(f"        [{x:.5f}, {y:.5f}, {z:.5f}]{comma}\n")

        f.write("      ],\n")
        f.write("      faces = [\n")

        # Write faces
        for idx, face in enumerate(faces):
            comma = "," if idx < len(faces) - 1 else ""
            f.write(f"        [{face[0]}, {face[1]}, {face[2]}]{comma}\n")

        f.write("      ],\n")
        f.write("      convexity = 10\n")
        f.write("    );\n")


# ── STL Output ───────────────────────────────────────────────────────────────

def cross(u, v):
    """Cross product of two 3-element tuples."""
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def normalize(v):
    """Normalize a 3-element vector; returns (0,0,0) for zero-length."""
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length < 1e-12:
        return (0.0, 0.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def write_stl(filepath, all_points, faces):
    """Write a binary STL file from the mesh data.

    Binary STL format:
      - 80-byte header
      - 4-byte uint32 triangle count
      - Per triangle (50 bytes):
          12 bytes normal (3 × float32)
          36 bytes vertices (3 × 3 × float32)
          2 bytes attribute byte count (0)
    """
    num_triangles = len(faces)

    with open(filepath, 'wb') as f:
        # Header (80 bytes)
        header = b'Binary STL - Parametric Sandstone Cylinder'
        header = header.ljust(80, b'\0')
        f.write(header)

        # Triangle count
        f.write(struct.pack('<I', num_triangles))

        # Triangles
        for face in faces:
            p0 = all_points[face[0]]
            p1 = all_points[face[1]]
            p2 = all_points[face[2]]

            # Compute face normal
            u = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            v = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
            n = normalize(cross(u, v))

            # Normal
            f.write(struct.pack('<3f', n[0], n[1], n[2]))
            # Vertices
            f.write(struct.pack('<3f', p0[0], p0[1], p0[2]))
            f.write(struct.pack('<3f', p1[0], p1[1], p1[2]))
            f.write(struct.pack('<3f', p2[0], p2[1], p2[2]))
            # Attribute byte count
            f.write(struct.pack('<H', 0))


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate a parametric sandstone strata cylinder SCAD file, or a vase.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # ── Vase vs Sandstone mode selection ─────────────────────────────────
    parser.add_argument(
        "--vase", action="store_true", default=False,
        help="Generate a simple cylindrical vase instead of sandstone model"
    )
    parser.add_argument(
        "--vase-sandstone", action="store_true", default=False,
        help="Generate sandstone with vase dimensions (organic exterior, hollow interior)"
    )

    parser.add_argument(
        "--vase-solid", action="store_true", default=False,
        help="Generate solid sandstone scaled to vase exterior dimensions (no bore)"
    )

    # ── Vase-specific arguments ──────────────────────────────────────────
    parser.add_argument(
        "--vase-interior-diameter", type=float, default=78.0,
        help="Interior diameter of the vase cavity (mm, default 78.0)"
    )
    parser.add_argument(
        "--vase-interior-height", type=float, default=176.0,
        help="Interior height of the vase cavity (mm, default 176.0)"
    )
    parser.add_argument(
        "--vase-wall", type=float, default=3.0,
        help="Vase wall thickness (mm, default 3.0)"
    )
    parser.add_argument(
        "--vase-base", type=float, default=3.0,
        help="Vase solid base thickness (mm, default 3.0)"
    )
    parser.add_argument(
        "--vase-layers", type=int, default=50,
        help="Number of layers for vase rings (default 50)"
    )

    # ── Sandstone-specific arguments ─────────────────────────────────────
    height_group = parser.add_mutually_exclusive_group()
    height_group.add_argument(
        "--height", type=float, default=None,
        help=f"Target height in mm (baseline = {BASELINE_HEIGHT}mm)"
    )
    height_group.add_argument(
        "--height-percent", type=float, default=None,
        help="Height as percentage of baseline (100 = no change)"
    )
    height_group.add_argument(
        "--height-scale", type=float, default=None,
        help="Height scale factor (1.0 = no change)"
    )

    parser.add_argument(
        "--layers", type=int, default=None,
        help=f"Number of strata ring-layers (baseline = {BASELINE_NUM_LAYERS})"
    )
    parser.add_argument(
        "--layer-scale", type=float, default=None,
        help="Scale factor for number of layers (1.0 = baseline count)"
    )
    parser.add_argument(
        "--sharp", action="store_true", default=False,
        help="Use sharp nearest-neighbor XY snapping for crisp, "
             "pronounced strata ledges (default: smooth blending)"
    )
    parser.add_argument(
        "--hollow", action="store_true", default=False,
        help="Make the model hollow (tube) with default 2mm wall"
    )
    parser.add_argument(
        "--wall", type=float, default=None,
        help="Wall thickness in mm (implies hollow). Default: 2.0"
    )
    parser.add_argument(
        "--base", type=float, nargs='?', const=2.0, default=None,
        help="Solid base height in mm (implies hollow). "
             "Use --base alone for 2mm, or --base 9.46 for precise value"
    )
    parser.add_argument(
        "--base-hole", type=float, nargs='?', const=2.0, default=None,
        help="Diameter of center hole through the solid base (mm). "
             "Use --base-hole alone for 2mm, or --base-hole 79 for larger. "
             "Requires --base."
    )
    parser.add_argument(
        "--source", type=str, default=str(DEFAULT_SOURCE),
        help="Path to the original SCAD file"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Output SCAD filename (default: auto-generated)"
    )

    args = parser.parse_args()

    # ── VASE MODE (simple cylindrical) ───────────────────────────────────
    if args.vase and not args.vase_sandstone:
        print("Generating VASE model")
        interior_diameter = args.vase_interior_diameter
        interior_height = args.vase_interior_height
        wall_thickness = args.vase_wall
        solid_base = args.vase_base
        num_layers = args.vase_layers
        
        print(f"  Interior: ⌀{interior_diameter:.1f}mm × {interior_height:.1f}mm")
        print(f"  Wall:     {wall_thickness:.2f}mm")
        print(f"  Base:     {solid_base:.2f}mm")
        print(f"  Layers:   {num_layers}")
        
        # Generate simple cylindrical vase rings
        new_rings = generate_vase_rings(interior_diameter, interior_height, 
                                        wall_thickness, num_layers)
        target_height = interior_height
        
        # Build hollow mesh
        all_points, faces = build_hollow_mesh(
            new_rings, target_height, wall_thickness,
            solid_base, 0.0)
        n_pts = len(all_points)
        n_faces = len(faces)
        
        # Output filename
        if args.output:
            base_output = args.output
            if base_output.lower().endswith('.scad'):
                base_output = base_output[:-5]
            elif base_output.lower().endswith('.stl'):
                base_output = base_output[:-4]
        else:
            d_tag = f"{interior_diameter:.0f}mm"
            h_tag = f"{interior_height:.0f}mm"
            w_tag = f"wall{wall_thickness:.0f}"
            b_tag = f"base{solid_base:.0f}"
            base_output = f"vase_{d_tag}x{h_tag}_{w_tag}_{b_tag}"
        
        scad_path = base_output + '.scad'
        stl_path = base_output + '.stl'
        
        # Write outputs
        write_scad(scad_path, all_points, faces, target_height, num_layers)
        write_stl(stl_path, all_points, faces)
        
        stl_size = os.path.getsize(stl_path)
        stl_mb = stl_size / (1024 * 1024)
        
        print(f"\n✓ SCAD: {scad_path}")
        print(f"✓ STL:  {stl_path}  ({stl_mb:.1f} MB)")
        print(f"  Points: {n_pts:,}  |  Faces: {n_faces:,}")
        print(f"  Interior cavity: ⌀{interior_diameter:.1f}mm × {interior_height:.1f}mm")
        print(f"  Wall thickness:  {wall_thickness:.2f}mm")
        print(f"  Base thickness:  {solid_base:.2f}mm")
        return
    
    # ── VASE-SOLID MODE (solid sandstone scaled to vase exterior) ────────
    if args.vase_solid:
        interior_diameter = args.vase_interior_diameter
        interior_height = args.vase_interior_height
        wall_thickness = args.vase_wall
        target_height = interior_height
        exterior_diameter = interior_diameter + 2 * wall_thickness
        exterior_radius = exterior_diameter / 2.0
        num_layers = args.vase_layers if args.vase_layers != 50 else max(2, int(round(BASELINE_NUM_LAYERS * (target_height / BASELINE_HEIGHT))))
        print(f"Generating SOLID SANDSTONE vase shell")
        print(f"  Exterior: ⌀{exterior_diameter:.1f}mm × {target_height:.1f}mm")
        print(f"  Layers:   {num_layers}")
        source_path = args.source
        if not os.path.exists(source_path):
            print(f"ERROR: Source file not found: {source_path}", file=sys.stderr)
            sys.exit(1)
        rings, center_bot, center_top, ring_avg_z = parse_original_scad(source_path)
        new_rings = interpolate_rings(rings, ring_avg_z, num_layers, target_height, sharp=args.sharp)
        first_ring = new_rings[0]
        current_radius = sum(math.sqrt(p[0]**2 + p[1]**2) for p in first_ring) / len(first_ring)
        scale_factor = exterior_radius / current_radius if current_radius > 1e-6 else 1.0
        print(f"  Scaling: {scale_factor:.3f}x  ({current_radius:.2f}mm → {exterior_radius:.2f}mm radius)")
        scaled_rings = [[(p[0]*scale_factor, p[1]*scale_factor, p[2]) for p in ring] for ring in new_rings]
        all_points, faces = build_mesh(scaled_rings, target_height)
        n_pts = len(all_points)
        n_faces = len(faces)
        if args.output:
            base_output = args.output
            if base_output.lower().endswith('.scad'): base_output = base_output[:-5]
            elif base_output.lower().endswith('.stl'): base_output = base_output[:-4]
        else:
            base_output = f"vase_solid_sandstone_{exterior_diameter:.0f}mmx{target_height:.0f}mm_{num_layers}L"
        scad_path = base_output + '.scad'
        stl_path  = base_output + '.stl'
        write_scad(scad_path, all_points, faces, target_height, num_layers)
        write_stl(stl_path, all_points, faces)
        stl_mb = os.path.getsize(stl_path) / (1024*1024)
        print(f"\n✓ SCAD: {scad_path}")
        print(f"✓ STL:  {stl_path}  ({stl_mb:.1f} MB)")
        print(f"  Points: {n_pts:,}  |  Faces: {n_faces:,}")
        print(f"  Exterior: ⌀{exterior_diameter:.1f}mm × {target_height:.1f}mm  (solid, no bore)")
        return

    # ── VASE-SANDSTONE MODE (sandstone exterior with vase interior) ──────
    if args.vase_sandstone:
        print("Generating VASE with SANDSTONE exterior")
        interior_diameter = args.vase_interior_diameter
        interior_height = args.vase_interior_height
        wall_thickness = args.vase_wall
        solid_base = args.vase_base
        target_height = interior_height
        
        # Resolve vase layer count
        num_layers = args.vase_layers if args.vase_layers != 50 else max(2, int(round(BASELINE_NUM_LAYERS * (interior_height / BASELINE_HEIGHT))))
        
        print(f"  Interior: ⌀{interior_diameter:.1f}mm × {interior_height:.1f}mm")
        print(f"  Wall:     {wall_thickness:.2f}mm")
        print(f"  Base:     {solid_base:.2f}mm")
        print(f"  Layers:   {num_layers}")
        
        # Parse original sandstone
        source_path = args.source
        if not os.path.exists(source_path):
            print(f"ERROR: Source file not found: {source_path}", file=sys.stderr)
            sys.exit(1)
        
        print(f"\nParsing sandstone strata from: {source_path}")
        rings, center_bot, center_top, ring_avg_z = parse_original_scad(source_path)
        
        # Generate sandstone rings at vase height
        new_rings = interpolate_rings(rings, ring_avg_z, num_layers, target_height,
                                      sharp=args.sharp)
        
        # Scale rings to fit vase exterior dimensions
        # Interior diameter + 2 wall thickness = exterior diameter
        exterior_diameter = interior_diameter + 2 * wall_thickness
        exterior_radius = exterior_diameter / 2.0
        
        # Find current average radius (average distance of ring points from origin)
        first_ring = new_rings[0]
        radius_sum = sum(math.sqrt(p[0]**2 + p[1]**2) for p in first_ring)
        current_radius = radius_sum / len(first_ring)
        
        scale_factor = exterior_radius / current_radius if current_radius > 1e-6 else 1.0
        
        print(f"  Current radius:  {current_radius:.2f}mm")
        print(f"  Target radius:   {exterior_radius:.2f}mm")
        print(f"  Scaling rings:   {scale_factor:.3f}x (for ⌀{exterior_diameter:.1f}mm exterior)")
        
        # Apply scaling to rings
        scaled_rings = []
        for ring in new_rings:
            scaled_ring = [(p[0]*scale_factor, p[1]*scale_factor, p[2]) for p in ring]
            scaled_rings.append(scaled_ring)
        
        # Build hollow mesh with perfect cylindrical interior
        all_points, faces = build_hollow_vase_mesh(
            scaled_rings, interior_diameter, target_height, solid_base)
        n_pts = len(all_points)
        n_faces = len(faces)
        
        # Output filename
        if args.output:
            base_output = args.output
            if base_output.lower().endswith('.scad'):
                base_output = base_output[:-5]
            elif base_output.lower().endswith('.stl'):
                base_output = base_output[:-4]
        else:
            d_tag = f"{interior_diameter:.0f}mm"
            h_tag = f"{interior_height:.0f}mm"
            w_tag = f"wall{wall_thickness:.0f}"
            b_tag = f"base{solid_base:.0f}"
            l_tag = f"{num_layers}L"
            base_output = f"vase_sandstone_{d_tag}x{h_tag}_{w_tag}_{b_tag}_{l_tag}"
        
        scad_path = base_output + '.scad'
        stl_path = base_output + '.stl'
        
        # Write outputs
        write_scad(scad_path, all_points, faces, target_height, num_layers)
        write_stl(stl_path, all_points, faces)
        
        stl_size = os.path.getsize(stl_path)
        stl_mb = stl_size / (1024 * 1024)
        
        print(f"\n✓ SCAD: {scad_path}")
        print(f"✓ STL:  {stl_path}  ({stl_mb:.1f} MB)")
        print(f"  Points: {n_pts:,}  |  Faces: {n_faces:,}")
        print(f"  Interior cavity: ⌀{interior_diameter:.1f}mm × {interior_height:.1f}mm")
        print(f"  Exterior shell: ⌀{exterior_diameter:.1f}mm × {interior_height:.1f}mm")
        print(f"  Wall thickness:  {wall_thickness:.2f}mm")
        print(f"  Base thickness:  {solid_base:.2f}mm")
        print(f"  Strata layers:   {num_layers}")
        return
    
    # ── SANDSTONE MODE ───────────────────────────────────────────────────
    # Resolve target height
    if args.height is not None:
        target_height = args.height
    elif args.height_percent is not None:
        target_height = BASELINE_HEIGHT * (args.height_percent / 100.0)
    elif args.height_scale is not None:
        target_height = BASELINE_HEIGHT * args.height_scale
    else:
        target_height = BASELINE_HEIGHT

    # Resolve number of layers
    if args.layers is not None:
        num_layers = max(2, args.layers)  # minimum 2 rings
    elif args.layer_scale is not None:
        num_layers = max(2, int(round(BASELINE_NUM_LAYERS * args.layer_scale)))
    else:
        # Default: scale layers proportionally with height so strata
        # density matches the original (~1.09mm per layer).
        # Nearest-neighbor XY interpolation preserves sharp ledges
        # even when extra layers are added.
        num_layers = max(2, int(round(BASELINE_NUM_LAYERS * (target_height / BASELINE_HEIGHT))))

    # Parse original
    source_path = args.source
    if not os.path.exists(source_path):
        print(f"ERROR: Source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing original: {source_path}")
    rings, center_bot, center_top, ring_avg_z = parse_original_scad(source_path)
    print(f"  → {len(rings)} rings × {POINTS_PER_RING} points/ring")
    print(f"  → Original height: {BASELINE_HEIGHT}mm")

    # Generate new rings
    print(f"\nGenerating parametric model:")
    print(f"  Target height : {target_height:.1f} mm "
          f"({target_height/BASELINE_HEIGHT*100:.0f}% of baseline)")
    print(f"  Strata layers : {num_layers} "
          f"({num_layers/BASELINE_NUM_LAYERS*100:.0f}% of baseline)")
    layer_thickness = target_height / max(1, num_layers - 1)
    print(f"  Avg layer step: {layer_thickness:.2f} mm")
    print(f"  Strata mode : {'SHARP (nearest-neighbor)' if args.sharp else 'SMOOTH (blended)'}")

    new_rings = interpolate_rings(rings, ring_avg_z, num_layers, target_height,
                                   sharp=args.sharp)

    # ── Resolve hollow / wall / base / hole ───────────────────────────────
    wall_thickness = None
    solid_base = 0.0
    base_hole_diameter = 0.0

    if args.wall is not None:
        wall_thickness = args.wall
    elif args.hollow or args.base is not None or args.base_hole is not None:
        wall_thickness = 2.0  # default wall

    if args.base is not None:
        solid_base = args.base
        if wall_thickness is None:
            wall_thickness = 2.0  # --base implies hollow

    if args.base_hole is not None:
        base_hole_diameter = args.base_hole
        # --base-hole implies --base (default 2mm) and hollow
        if solid_base <= 0:
            solid_base = 2.0
        if wall_thickness is None:
            wall_thickness = 2.0

    is_hollow = wall_thickness is not None

    if is_hollow:
        mode_parts = [f"wall = {wall_thickness:.2f} mm"]
        if solid_base > 0:
            mode_parts.append(f"solid base = {solid_base:.2f} mm")
        if base_hole_diameter > 0:
            mode_parts.append(f"base hole ⌀{base_hole_diameter:.2f} mm")
        print(f"  Mode        : HOLLOW ({', '.join(mode_parts)})")
    else:
        print(f"  Mode        : SOLID")

    # ── Build mesh ────────────────────────────────────────────────────────
    if is_hollow:
        all_points, faces = build_hollow_mesh(
            new_rings, target_height, wall_thickness,
            solid_base, base_hole_diameter)
    else:
        all_points, faces = build_mesh(new_rings, target_height)
    n_pts = len(all_points)
    n_faces = len(faces)

    # ── Output filenames ─────────────────────────────────────────────────
    if args.output:
        base_output = args.output
        # Strip extension if provided
        if base_output.lower().endswith('.scad'):
            base_output = base_output[:-5]
        elif base_output.lower().endswith('.stl'):
            base_output = base_output[:-4]
    else:
        h_tag = f"{target_height:.0f}mm"
        l_tag = f"{num_layers}L"
        w_tag = ""
        if is_hollow:
            w_tag = f"_wall{wall_thickness:.0f}"
            if solid_base > 0:
                base_str = f"{solid_base:.2f}".rstrip('0').rstrip('.')
                w_tag += f"_base{base_str}"
            if base_hole_diameter > 0:
                hole_str = f"{base_hole_diameter:.2f}".rstrip('0').rstrip('.')
                w_tag += f"_hole{hole_str}"
        base_output = f"illinois_sandstone_parametric_{h_tag}_{l_tag}{w_tag}"

    scad_path = base_output + '.scad'
    stl_path = base_output + '.stl'

    # ── Write SCAD ───────────────────────────────────────────────────────
    write_scad(scad_path, all_points, faces, target_height, num_layers)

    # ── Write STL ────────────────────────────────────────────────────────
    write_stl(stl_path, all_points, faces)

    stl_size = os.path.getsize(stl_path)
    stl_mb = stl_size / (1024 * 1024)

    print(f"\n✓ SCAD: {scad_path}")
    print(f"✓ STL:  {stl_path}  ({stl_mb:.1f} MB)")
    print(f"  Points: {n_pts:,}  |  Faces: {n_faces:,}")
    print(f"  Height: {target_height:.1f}mm  |  Layers: {num_layers}")
    if is_hollow:
        print(f"  Wall:   {wall_thickness:.2f}mm  |  Mode: hollow")
        if solid_base > 0:
            print(f"  Base:   {solid_base:.2f}mm  |  solid floor")
        if base_hole_diameter > 0:
            print(f"  Hole:   ⌀{base_hole_diameter:.2f}mm  |  center base hole")
    print(f"\n  The SCAD file has a 'fine_tune_scale' parameter for")
    print(f"  additional height tweaks without regenerating.")


if __name__ == "__main__":
    main()
