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
BASELINE_NUM_LAYERS = 110     # original ring count
POINTS_PER_RING = 121         # angular samples per ring
SCRIPT_DIR = Path(__file__).parent
DEFAULT_SOURCE = SCRIPT_DIR / "1-illinois_sandstone_cylinder_v3.scad"


# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_original_scad(filepath):
    """Parse the original SCAD polyhedron into structured ring data.

    Returns:
        rings       : list of lists – rings[i][j] = (x, y, z)
        extra_top   : list of (x, y, z) – extra top-cap edge points
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

    # Extra top-cap points (between ring data and center points)
    extra_top = points[n_ring_points:total - 2]

    # Center points (last two)
    center_bot = points[total - 2]   # (0, 0, 0)
    center_top = points[total - 1]   # (0, 0, 120)

    return rings, extra_top, center_bot, center_top, ring_avg_z


# ── Interpolation ────────────────────────────────────────────────────────────

def lerp(a, b, t):
    """Linear interpolation between scalars a and b."""
    return a + (b - a) * t


def lerp_point(p1, p2, t):
    """Linearly interpolate between two 3D points."""
    return (lerp(p1[0], p2[0], t),
            lerp(p1[1], p2[1], t),
            lerp(p1[2], p2[2], t))


def interpolate_rings(original_rings, ring_avg_z, num_new_layers, target_height):
    """Generate new rings by interpolating original ring data.

    Strategy:
      - Each original ring sits at a normalized position t_i = i / (N_orig - 1)
      - Each new ring sits at t_k = k / (N_new - 1)
      - For each new ring, find the bracketing originals and interpolate
      - X and Y are interpolated (preserving cross-section shape transitions)
      - Z is interpolated and then scaled to the target height

    This preserves the organic strata character: undulations are smoothly
    blended between neighboring original layers, and the overall profile
    (wavy cylinder with varying radii) is maintained.
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

        ring = []
        for j in range(POINTS_PER_RING):
            p_lo = original_rings[i_lo][j]
            p_hi = original_rings[i_hi][j]

            # Interpolate XY directly (shape blending)
            x = lerp(p_lo[0], p_hi[0], alpha)
            y = lerp(p_lo[1], p_hi[1], alpha)

            # For Z: interpolate then scale
            # The original Z values encode both the layer's base height
            # and the organic undulation offset from that base.
            z_interp = lerp(p_lo[2], p_hi[2], alpha)
            z = z_interp * z_scale

            ring.append((x, y, z))

        new_rings.append(ring)

    return new_rings


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


def build_hollow_mesh(new_rings, target_height, wall_thickness):
    """Build a hollow tube mesh with inner and outer walls.

    Structure:
      - Outer shell: flat_bottom + organic rings + flat_top (faces outward)
      - Inner shell: same rings offset inward (faces inward / reversed)
      - Bottom annulus: connects outer ring 0 to inner ring 0
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

    # ── Inner rings (offset inward) ──────────────────────────────────────
    inner_rings = [offset_ring_inward(ring, wall_thickness) for ring in outer_rings]

    total_rings = len(outer_rings)

    # ── Flatten all points ───────────────────────────────────────────────
    # Layout: [outer ring 0..N-1] then [inner ring 0..N-1]
    all_points = []
    for ring in outer_rings:
        all_points.extend(ring)
    outer_count = len(all_points)  # = total_rings * P

    for ring in inner_rings:
        all_points.extend(ring)

    faces = []

    # ── Outer side faces (normal outward) ────────────────────────────────
    for i in range(total_rings - 1):
        for j in range(P):
            j_next = (j + 1) % P
            a = i * P + j
            b = i * P + j_next
            c = (i + 1) * P + j_next
            d = (i + 1) * P + j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # ── Inner side faces (normal inward = reversed winding) ──────────────
    for i in range(total_rings - 1):
        for j in range(P):
            j_next = (j + 1) % P
            a = outer_count + i * P + j
            b = outer_count + i * P + j_next
            c = outer_count + (i + 1) * P + j_next
            d = outer_count + (i + 1) * P + j
            # Reversed winding for inward-facing normals
            faces.append([a, c, b])
            faces.append([a, d, c])

    # ── Bottom annulus (connects outer ring 0 to inner ring 0) ───────────
    # Normal faces downward (outward from the tube)
    for j in range(P):
        j_next = (j + 1) % P
        o_a = j
        o_b = j_next
        i_a = outer_count + j
        i_b = outer_count + j_next
        faces.append([o_a, i_a, i_b])
        faces.append([o_a, i_b, o_b])

    # ── Top annulus (connects outer last ring to inner last ring) ────────
    # Normal faces upward (outward from the tube)
    top_outer_start = (total_rings - 1) * P
    top_inner_start = outer_count + (total_rings - 1) * P
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
        description="Generate a parametric sandstone strata cylinder SCAD file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

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
        "--hollow", action="store_true", default=False,
        help="Make the model hollow (tube) with default 2mm wall"
    )
    parser.add_argument(
        "--wall", type=float, default=None,
        help="Wall thickness in mm (implies hollow). Default: 2.0"
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

    # ── Resolve target height ────────────────────────────────────────────
    if args.height is not None:
        target_height = args.height
    elif args.height_percent is not None:
        target_height = BASELINE_HEIGHT * (args.height_percent / 100.0)
    elif args.height_scale is not None:
        target_height = BASELINE_HEIGHT * args.height_scale
    else:
        target_height = BASELINE_HEIGHT

    # ── Resolve number of layers ─────────────────────────────────────────
    if args.layers is not None:
        num_layers = max(2, args.layers)  # minimum 2 rings
    elif args.layer_scale is not None:
        num_layers = max(2, int(round(BASELINE_NUM_LAYERS * args.layer_scale)))
    else:
        # Default: scale layers proportionally with height
        num_layers = max(2, int(round(BASELINE_NUM_LAYERS * (target_height / BASELINE_HEIGHT))))

    # ── Parse original ───────────────────────────────────────────────────
    source_path = args.source
    if not os.path.exists(source_path):
        print(f"ERROR: Source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing original: {source_path}")
    rings, extra_top, center_bot, center_top, ring_avg_z = parse_original_scad(source_path)
    print(f"  → {len(rings)} rings × {POINTS_PER_RING} points/ring")
    print(f"  → Original height: {BASELINE_HEIGHT}mm")

    # ── Generate new rings ───────────────────────────────────────────────
    print(f"\nGenerating parametric model:")
    print(f"  Target height : {target_height:.1f} mm "
          f"({target_height/BASELINE_HEIGHT*100:.0f}% of baseline)")
    print(f"  Strata layers : {num_layers} "
          f"({num_layers/BASELINE_NUM_LAYERS*100:.0f}% of baseline)")
    layer_thickness = target_height / max(1, num_layers - 1)
    print(f"  Avg layer step: {layer_thickness:.2f} mm")

    new_rings = interpolate_rings(rings, ring_avg_z, num_layers, target_height)

    # ── Resolve hollow / wall ────────────────────────────────────────────
    wall_thickness = None
    if args.wall is not None:
        wall_thickness = args.wall
    elif args.hollow:
        wall_thickness = 2.0  # default wall

    is_hollow = wall_thickness is not None

    if is_hollow:
        print(f"  Mode        : HOLLOW (wall = {wall_thickness:.1f} mm)")
    else:
        print(f"  Mode        : SOLID")

    # ── Build mesh ────────────────────────────────────────────────────────
    if is_hollow:
        all_points, faces = build_hollow_mesh(new_rings, target_height, wall_thickness)
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
        w_tag = f"_wall{wall_thickness:.0f}" if is_hollow else ""
        base_output = str(SCRIPT_DIR /
            f"illinois_sandstone_parametric_{h_tag}_{l_tag}{w_tag}")

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
        print(f"  Wall:   {wall_thickness:.1f}mm  |  Mode: hollow")
    print(f"\n  The SCAD file has a 'fine_tune_scale' parameter for")
    print(f"  additional height tweaks without regenerating.")


if __name__ == "__main__":
    main()
