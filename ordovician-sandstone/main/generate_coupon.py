#!/usr/bin/env python3
"""
Sandstone Transparency Test Coupon Generator
============================================
Carves a short section out of the *real* Illinois Sandstone lamp wall so a
filament's light transmission can be tested quickly, without printing the full
180 mm shade.

The coupon is a short open ring — a mini version of the lamp bottom — that
reproduces the exact wall the real lamp uses:

  * true 2 mm wall thickness (the variable that controls how much light glows
    through)
  * true strata texture at the 180 mm lamp's vertical scale (not compressed)
  * open top and bottom, no floor, so the light shines straight up through the
    walls

Because it is short and wide (≈100 mm across, ≈30 mm tall) it is inherently
stable, and because the walls are near-vertical with open ends it prints with
no supports and no infill (spiral/vase mode works too).

Set it *over* a small light, sit a light *next to* it, or drop a light *inside*
it — the walls glow either way.

Usage:
  python3 generate_coupon.py                 # default 30 mm full ring
  python3 generate_coupon.py --coupon-height 40
  python3 generate_coupon.py --arc 120       # 120° curved panel instead of a full ring
  python3 generate_coupon.py --wall 1.2      # thinner wall to test a brighter glow
"""

import argparse
import math
import os

import generate_sandstone as gs

# Match the uploaded lamp exactly: 180 mm tall, 2 mm wall, smooth strata.
LAMP_HEIGHT = 180.0
LAMP_LAYERS = 166


def crop_rings(rings, coupon_height):
    """Keep only the rings whose average Z falls within the coupon height.

    Returns a subset of the full-height rings, preserving their real Z values
    (and therefore the real strata pitch of the 180 mm lamp).
    """
    kept = []
    for ring in rings:
        avg_z = sum(p[2] for p in ring) / len(ring)
        if avg_z <= coupon_height:
            kept.append(ring)
    # Always keep at least two rings so the mesh builder has a wall to work with.
    if len(kept) < 2:
        kept = rings[:2]
    return kept


def keep_arc(rings, arc_degrees):
    """Trim each ring to a contiguous angular wedge, producing a curved panel.

    Points are evenly spaced by index (POINTS_PER_RING over 360°), so we select
    a fixed, contiguous band of indices — the same indices on every ring — which
    keeps the point count uniform and the mesh clean. The band is centered on
    the far side of the ring (index ~P/2) so it never straddles the 0° seam.
    """
    P = gs.POINTS_PER_RING
    n_pts = max(2, int(round(arc_degrees / 360.0 * P)) + 1)
    n_pts = min(n_pts, P)
    center = P // 2
    lo = center - n_pts // 2
    hi = lo + n_pts
    return [ring[lo:hi] for ring in rings]


def build_open_ring(rings, coupon_height, wall):
    """Build a watertight open ring (no floor) from cropped lamp rings.

    Outer organic wall + inner wall offset inward by ``wall``, closed by a
    bottom annulus at z=0 and a top annulus at z=coupon_height. The first and
    last rings are flattened *in place* to z=0 / z=coupon_height so the print
    gets clean flat rims — we do not append extra cap rings (doing so would
    duplicate a ring that already sits at z=0 and create degenerate,
    non-manifold slivers).
    """
    n = len(rings)
    P = len(rings[0])

    def flatten(ring_list):
        out = []
        for k, ring in enumerate(ring_list):
            if k == 0:
                out.append([(x, y, 0.0) for (x, y, _) in ring])
            elif k == n - 1:
                out.append([(x, y, coupon_height) for (x, y, _) in ring])
            else:
                out.append(list(ring))
        return out

    outer = flatten(rings)
    inner = flatten([gs.offset_ring_inward(r, wall) for r in rings])

    pts = []
    for ring in outer:
        pts.extend(ring)
    O = len(pts)
    for ring in inner:
        pts.extend(ring)

    def o(i, j):
        return i * P + j

    def inn(i, j):
        return O + i * P + j

    faces = []
    # Outer side wall (outward-facing)
    for i in range(n - 1):
        for j in range(P):
            jn = (j + 1) % P
            faces.append([o(i, j), o(i, jn), o(i + 1, jn)])
            faces.append([o(i, j), o(i + 1, jn), o(i + 1, j)])
    # Inner side wall (reversed winding, inward-facing)
    for i in range(n - 1):
        for j in range(P):
            jn = (j + 1) % P
            faces.append([inn(i, j), inn(i + 1, jn), inn(i, jn)])
            faces.append([inn(i, j), inn(i + 1, j), inn(i + 1, jn)])
    # Bottom annulus (outer ring 0 <-> inner ring 0, downward-facing)
    for j in range(P):
        jn = (j + 1) % P
        faces.append([o(0, j), inn(0, j), inn(0, jn)])
        faces.append([o(0, j), inn(0, jn), o(0, jn)])
    # Top annulus (outer ring N-1 <-> inner ring N-1, upward-facing)
    for j in range(P):
        jn = (j + 1) % P
        faces.append([o(n - 1, j), o(n - 1, jn), inn(n - 1, jn)])
        faces.append([o(n - 1, j), inn(n - 1, jn), inn(n - 1, j)])

    return pts, faces


def build_arc_panel(rings, coupon_height, wall):
    """Build a curved wall panel (open arc) by extruding cropped ring segments
    inward by ``wall`` and stitching outer↔inner surfaces plus the four edges.
    """
    P_outer_rings = rings
    inner_rings = [gs.offset_ring_inward(r, wall) for r in P_outer_rings]

    # Force flat top/bottom edges so the panel has clean, printable rims.
    def flatten(ring_list):
        out = []
        n = len(ring_list)
        for k, ring in enumerate(ring_list):
            if k == 0:
                out.append([(x, y, 0.0) for (x, y, _) in ring])
            elif k == n - 1:
                out.append([(x, y, coupon_height) for (x, y, _) in ring])
            else:
                out.append(list(ring))
        return out

    outer = flatten(P_outer_rings)
    inner = flatten(inner_rings)

    pts = []
    index = {}

    def add(p):
        idx = len(pts)
        pts.append(p)
        return idx

    N = len(outer)
    M = len(outer[0])  # points per (trimmed) ring — assumed uniform
    o_idx = [[add(outer[i][j]) for j in range(M)] for i in range(N)]
    i_idx = [[add(inner[i][j]) for j in range(M)] for i in range(N)]

    faces = []
    # Outer surface (outward)
    for i in range(N - 1):
        for j in range(M - 1):
            a, b = o_idx[i][j], o_idx[i][j + 1]
            c, d = o_idx[i + 1][j + 1], o_idx[i + 1][j]
            faces.append([a, b, c]); faces.append([a, c, d])
    # Inner surface (reversed winding)
    for i in range(N - 1):
        for j in range(M - 1):
            a, b = i_idx[i][j], i_idx[i][j + 1]
            c, d = i_idx[i + 1][j + 1], i_idx[i + 1][j]
            faces.append([a, c, b]); faces.append([a, d, c])
    # Bottom edge
    for j in range(M - 1):
        a, b = o_idx[0][j], o_idx[0][j + 1]
        c, d = i_idx[0][j + 1], i_idx[0][j]
        faces.append([a, c, b]); faces.append([a, d, c])
    # Top edge
    for j in range(M - 1):
        a, b = o_idx[N - 1][j], o_idx[N - 1][j + 1]
        c, d = i_idx[N - 1][j + 1], i_idx[N - 1][j]
        faces.append([a, b, c]); faces.append([a, c, d])
    # Left edge (j=0) and right edge (j=M-1)
    for i in range(N - 1):
        # left
        a, b = o_idx[i][0], o_idx[i + 1][0]
        c, d = i_idx[i + 1][0], i_idx[i][0]
        faces.append([a, b, c]); faces.append([a, c, d])
        # right
        a, b = o_idx[i][M - 1], o_idx[i + 1][M - 1]
        c, d = i_idx[i + 1][M - 1], i_idx[i][M - 1]
        faces.append([a, d, c]); faces.append([a, c, b])

    return pts, faces


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--coupon-height", type=float, default=30.0,
                    help="Height of the coupon in mm (default 30)")
    ap.add_argument("--wall", type=float, default=2.0,
                    help="Wall thickness in mm (default 2.0 — matches the lamp)")
    ap.add_argument("--arc", type=float, default=None,
                    help="Produce a curved panel spanning this many degrees "
                         "instead of a full ring (e.g. 120)")
    ap.add_argument("--source", type=str, default=str(gs.DEFAULT_SOURCE),
                    help="Path to the original sandstone SCAD source")
    ap.add_argument("-o", "--output", type=str, default=None,
                    help="Output basename (default: auto-generated)")
    args = ap.parse_args()

    rings, _, _, ring_avg_z = gs.parse_original_scad(args.source)
    full = gs.interpolate_rings(rings, ring_avg_z, LAMP_LAYERS, LAMP_HEIGHT,
                                sharp=False)
    cropped = crop_rings(full, args.coupon_height)

    if args.arc is not None:
        cropped = keep_arc(cropped, args.arc)
        pts, faces = build_arc_panel(cropped, args.coupon_height, args.wall)
        shape_tag = f"arc{args.arc:.0f}"
    else:
        pts, faces = build_open_ring(cropped, args.coupon_height, args.wall)
        shape_tag = "ring"

    if args.output:
        base = args.output
        for ext in (".stl", ".scad"):
            if base.lower().endswith(ext):
                base = base[:-len(ext)]
    else:
        h = f"{args.coupon_height:.0f}mm"
        w = f"wall{args.wall:.1f}".rstrip('0').rstrip('.')
        base = f"sandstone-transparency-coupon-{shape_tag}-{h}-{w}"

    stl_path = base + ".stl"
    scad_path = base + ".scad"
    gs.write_stl(stl_path, pts, faces)
    gs.write_scad(scad_path, pts, faces, args.coupon_height, len(cropped))

    stl_mb = os.path.getsize(stl_path) / (1024 * 1024)
    print(f"✓ STL:  {stl_path}  ({stl_mb:.2f} MB)")
    print(f"✓ SCAD: {scad_path}")
    print(f"  Shape:  {'full ring' if args.arc is None else f'{args.arc:.0f}° arc panel'}")
    print(f"  Size:   ⌀~100mm × {args.coupon_height:.0f}mm tall, {args.wall:.1f}mm wall")
    print(f"  Points: {len(pts):,}  |  Faces: {len(faces):,}")


if __name__ == "__main__":
    main()
