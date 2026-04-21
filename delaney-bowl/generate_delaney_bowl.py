#!/usr/bin/env python3
"""
Generate a wavy Delaney bowl mesh as watertight STL + SCAD polyhedron.

This avoids OpenSCAD CSG subtraction artifacts at the rim by explicitly
stitching outer wall, inner wall, top rim band, floor annulus, and bottom.
"""

import argparse
import math
import os
import struct
from collections import Counter


def clamp(x, a, b):
    return a if x < a else (b if x > b else x)


def smoothstep(e0, e1, x):
    if abs(e1 - e0) < 1e-12:
        return 1.0 if x >= e1 else 0.0
    t = clamp((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def rim_z_offset(theta_deg, zfrac, waves, amp, irregular, phase_deg, falloff_width):
    if amp <= 0 or waves <= 0:
        return 0.0

    n = max(int(waves), 1)
    ph = phase_deg
    k = clamp(irregular, 0.0, 1.0)
    w = smoothstep(1.0 - falloff_width, 1.0, zfrac)

    base_val = math.sin(math.radians(n * theta_deg + ph))
    mix1 = (
        0.6 * math.sin(math.radians((n + 3) * theta_deg + 1.3 * ph))
        + 0.4 * math.sin(math.radians(max(1, n - 2) * theta_deg - 0.9 * ph))
    )
    mixed = (1.0 - k) * base_val + k * mix1
    return amp * mixed * w


def r_at_z(base_radius, pitch_deg, z):
    return base_radius + z * math.tan(math.radians(pitch_deg))


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def normalize(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if length < 1e-12:
        return (0.0, 0.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def build_mesh(args):
    n_t = max(12, args.fn_theta)
    n_z = max(2, args.fn_z)

    floor_frac = clamp(args.bottom_thickness / args.height, 0.0, 1.0)

    outer_rings = []
    for i_z in range(n_z + 1):
        frac = i_z / n_z
        z = args.height * frac
        ring = []
        for i_t in range(n_t):
            th = 360.0 * i_t / n_t
            r = max(0.5, r_at_z(args.base_radius, args.pitch_deg, z))
            dz = rim_z_offset(
                th,
                frac,
                args.rim_z_waves,
                args.rim_z_amp,
                args.rim_z_irregular,
                args.rim_z_phase_deg,
                args.rim_z_falloff_width,
            )
            zz = z + dz
            ring.append((r * math.cos(math.radians(th)), r * math.sin(math.radians(th)), zz))
        outer_rings.append(ring)

    n_inner_z = max(1, int(round(n_z * (1.0 - floor_frac))))
    inner_rings = []
    for i_z in range(n_inner_z + 1):
        frac = floor_frac + (1.0 - floor_frac) * (i_z / n_inner_z)
        z = args.height * frac
        ring = []
        for i_t in range(n_t):
            th = 360.0 * i_t / n_t
            r_outer = max(0.5, r_at_z(args.base_radius, args.pitch_deg, z))
            r_inner = max(0.5, r_outer - args.wall_thickness)
            if i_z == 0:
                # Floor ring must be perfectly flat — no waviness
                zz = z
            else:
                dz = rim_z_offset(
                    th,
                    frac,
                    args.rim_z_waves,
                    args.rim_z_amp,
                    args.rim_z_irregular,
                    args.rim_z_phase_deg,
                    args.rim_z_falloff_width,
                )
                zz = z + dz
            ring.append((r_inner * math.cos(math.radians(th)), r_inner * math.sin(math.radians(th)), zz))
        inner_rings.append(ring)

    points = []
    for ring in outer_rings:
        points.extend(ring)
    outer_count = len(points)

    for ring in inner_rings:
        points.extend(ring)

    # Floor center at exact floor height (flat, no waviness)
    floor_z = args.bottom_thickness
    floor_center_idx = len(points)
    points.append((0.0, 0.0, floor_z))

    bottom_center_idx = len(points)
    bottom_avg_z = sum(p[2] for p in outer_rings[0]) / n_t
    points.append((0.0, 0.0, bottom_avg_z))

    faces = []

    # Outer wall
    for i in range(len(outer_rings) - 1):
        for j in range(n_t):
            jn = (j + 1) % n_t
            a = i * n_t + j
            b = i * n_t + jn
            c = (i + 1) * n_t + jn
            d = (i + 1) * n_t + j
            faces.append((a, b, c))
            faces.append((a, c, d))

    # Inner wall (reversed winding)
    for i in range(len(inner_rings) - 1):
        for j in range(n_t):
            jn = (j + 1) % n_t
            a = outer_count + i * n_t + j
            b = outer_count + i * n_t + jn
            c = outer_count + (i + 1) * n_t + jn
            d = outer_count + (i + 1) * n_t + j
            faces.append((a, c, b))
            faces.append((a, d, c))

    # Top rim band
    outer_top_start = (len(outer_rings) - 1) * n_t
    inner_top_start = outer_count + (len(inner_rings) - 1) * n_t
    for j in range(n_t):
        jn = (j + 1) % n_t
        oa = outer_top_start + j
        ob = outer_top_start + jn
        ia = inner_top_start + j
        ib = inner_top_start + jn
        faces.append((oa, ob, ib))
        faces.append((oa, ib, ia))

    inner_floor_start = outer_count

    # Inner floor disk (faces upward into cavity)
    for j in range(n_t):
        jn = (j + 1) % n_t
        a = inner_floor_start + j
        b = inner_floor_start + jn
        faces.append((floor_center_idx, a, b))

    # Outer bottom disk (faces downward)
    outer_bottom_start = 0
    for j in range(n_t):
        jn = (j + 1) % n_t
        a = outer_bottom_start + j
        b = outer_bottom_start + jn
        faces.append((bottom_center_idx, b, a))

    return points, faces


def write_binary_stl(path, points, faces):
    with open(path, "wb") as f:
        header = b"Binary STL - Delaney Bowl (stitched shell)"
        f.write(header.ljust(80, b"\0"))
        f.write(struct.pack("<I", len(faces)))

        for tri in faces:
            p0 = points[tri[0]]
            p1 = points[tri[1]]
            p2 = points[tri[2]]
            u = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            v = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
            n = normalize(cross(u, v))

            f.write(struct.pack("<3f", *n))
            f.write(struct.pack("<3f", *p0))
            f.write(struct.pack("<3f", *p1))
            f.write(struct.pack("<3f", *p2))
            f.write(struct.pack("<H", 0))


def write_scad_polyhedron(path, points, faces):
    with open(path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by generate_delaney_bowl.py\n")
        f.write("polyhedron(\n")
        f.write("  points = [\n")
        for i, (x, y, z) in enumerate(points):
            comma = "," if i < len(points) - 1 else ""
            f.write(f"    [{x:.6f}, {y:.6f}, {z:.6f}]{comma}\n")
        f.write("  ],\n")
        f.write("  faces = [\n")
        for i, tri in enumerate(faces):
            comma = "," if i < len(faces) - 1 else ""
            f.write(f"    [{tri[0]}, {tri[1]}, {tri[2]}]{comma}\n")
        f.write("  ],\n")
        f.write("  convexity = 20\n")
        f.write(");\n")


def is_edge_manifold(faces):
    edges = Counter()
    for a, b, c in faces:
        for u, v in ((a, b), (b, c), (c, a)):
            edge = (u, v) if u < v else (v, u)
            edges[edge] += 1
    bad = [edge for edge, count in edges.items() if count != 2]
    return len(bad) == 0, len(bad)


def parse_args():
    p = argparse.ArgumentParser(description="Generate repaired Delaney bowl STL/SCAD")
    p.add_argument("--base-radius", type=float, default=60.0)
    p.add_argument("--height", type=float, default=20.0)
    p.add_argument("--pitch-deg", type=float, default=40.0)
    p.add_argument("--wall-thickness", type=float, default=5.0)
    p.add_argument("--bottom-thickness", type=float, default=2.0)

    p.add_argument("--rim-z-waves", type=int, default=3)
    p.add_argument("--rim-z-amp", type=float, default=9.0)
    p.add_argument("--rim-z-irregular", type=float, default=0.45)
    p.add_argument("--rim-z-phase-deg", type=float, default=0.0)
    p.add_argument("--rim-z-falloff-width", type=float, default=0.99)

    p.add_argument("--fn-theta", type=int, default=180)
    p.add_argument("--fn-z", type=int, default=60)

    p.add_argument("-o", "--output", type=str, default="delaney-bowl-fixed")
    return p.parse_args()


def main():
    args = parse_args()

    if args.height <= 0:
        raise ValueError("--height must be > 0")
    if args.wall_thickness <= 0:
        raise ValueError("--wall-thickness must be > 0")
    if args.bottom_thickness < 0:
        raise ValueError("--bottom-thickness must be >= 0")
    if args.bottom_thickness >= args.height:
        raise ValueError("--bottom-thickness must be < --height")

    points, faces = build_mesh(args)

    manifold, bad_edges = is_edge_manifold(faces)
    print(f"Points: {len(points):,}")
    print(f"Faces:  {len(faces):,}")
    print(f"Edge-manifold: {'YES' if manifold else 'NO'}")
    if not manifold:
        print(f"  Non-2-manifold edge count: {bad_edges}")

    out_base = args.output
    if out_base.lower().endswith((".stl", ".scad")):
        out_base = out_base.rsplit(".", 1)[0]

    stl_path = out_base + ".stl"
    scad_path = out_base + ".scad"

    write_binary_stl(stl_path, points, faces)
    write_scad_polyhedron(scad_path, points, faces)

    print(f"Wrote STL:  {stl_path} ({os.path.getsize(stl_path)/(1024*1024):.2f} MB)")
    print(f"Wrote SCAD: {scad_path}")


if __name__ == "__main__":
    main()
