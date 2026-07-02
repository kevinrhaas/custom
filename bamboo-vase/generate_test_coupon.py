#!/usr/bin/env python3
"""
Wall test coupon — a small slice of a vase's exterior wall for finish testing.
=============================================================================

Cuts a ~20 mm-tall patch out of the side wall of a chosen variant (default
zen-classic) with the REAL exterior geometry: true cylinder curvature, true
wall cross-section, and a full flute (a crest with a valley on each side). It is
oriented to print STANDING UP — z is vertical, exactly as the wall sits on the
vase — so the layer lines run across the exterior the same way they will on the
finished piece. That makes it a faithful sample for testing paints, primers,
sanding, spray finishes, etc. Print a handful and change the approach per copy
in your slicer.

A small flat foot is fused to the bottom so the thin panel stands on the bed
without tipping. The panel and foot are emitted as two closed (watertight)
solids that overlap at the base; every slicer unions overlapping bodies at
slice time, so it prints as one fused part.

Pure Python, no dependencies. Millimetres.
"""
import math
import os
import struct
from generate_bamboo_vase import Mesh

# --- variant wall parameters (must match generate_bamboo_vase.VARIANTS) ------
VARIANT_PARAMS = {
    #                inner_dia  n_waves  amp   belly  height
    "zen-classic":  (105.0,     14,      4.0,  3.0,   130.0),
    "zen-squat":    (112.0,     12,      5.0,  0.0,    95.0),
    "zen-tall":     (100.0,     16,      3.5,  4.0,   170.0),
    "fine-flute":   (105.0,     24,      2.5,  0.0,   130.0),
    "bold-wave":    (105.0,      9,      6.5,  4.0,   125.0),
    "zen-mini":     ( 95.0,     12,      4.0,  0.0,    90.0),
}
WALL = 2.8          # matches build_vase default (min wall at valleys)

# --- coupon settings ---------------------------------------------------------
COUPON_HEIGHT = 20.0    # mm, height of the wall patch
N_FLUTES = 1            # how many full flutes wide (1 => a crest between two valleys)
FOOT_HEIGHT = 4.0       # mm, thickness of the standing foot
FOOT_MARGIN = 4.0       # mm, how far the foot extends past the panel footprint
N_ANG = 96              # angular samples across the patch
N_Z = 48                # vertical samples


def build_coupon(variant="zen-classic"):
    inner_dia, n, amp, belly, height = VARIANT_PARAMS[variant]
    inner_r = inner_dia / 2.0

    z_center = height / 2.0                    # sample from the belly region
    z_bot = z_center - COUPON_HEIGHT / 2.0
    z_top = z_center + COUPON_HEIGHT / 2.0

    def belly_z(z):
        return belly * math.sin(math.pi * (z / height))

    # angular window = N_FLUTES full periods, centred on a crest (phase 0)
    period = 2.0 * math.pi / n
    ang_half = N_FLUTES * period / 2.0
    phis = [(-ang_half + 2 * ang_half * i / N_ANG) for i in range(N_ANG + 1)]
    zs = [z_bot + (z_top - z_bot) * j / N_Z for j in range(N_Z + 1)]

    def r_out(phi, z):
        # crest at phi=0 because cos(n*0)=1
        return inner_r + WALL + belly_z(z) + amp * (0.5 + 0.5 * math.cos(n * phi))

    # build front (fluted) and back (smooth interior cylinder) grids
    front = [[None] * (N_Z + 1) for _ in range(N_ANG + 1)]
    back = [[None] * (N_Z + 1) for _ in range(N_ANG + 1)]
    for i, phi in enumerate(phis):
        cp, sp = math.cos(phi), math.sin(phi)
        for j, z in enumerate(zs):
            ro = r_out(phi, z)
            front[i][j] = (ro * cp, ro * sp, z)
            back[i][j] = (inner_r * cp, inner_r * sp, z)

    mesh = Mesh()

    # FRONT surface (outward radial)
    for i in range(N_ANG):
        for j in range(N_Z):
            a, b = front[i][j], front[i + 1][j]
            c, d = front[i + 1][j + 1], front[i][j + 1]
            mx = (a[0] + b[0] + c[0] + d[0]) / 4.0
            my = (a[1] + b[1] + c[1] + d[1]) / 4.0
            mesh.quad(a, b, c, d, (mx, my, 0.0))

    # BACK surface (inward radial)
    for i in range(N_ANG):
        for j in range(N_Z):
            a, b = back[i][j], back[i + 1][j]
            c, d = back[i + 1][j + 1], back[i][j + 1]
            mx = (a[0] + b[0] + c[0] + d[0]) / 4.0
            my = (a[1] + b[1] + c[1] + d[1]) / 4.0
            mesh.quad(a, b, c, d, (-mx, -my, 0.0))

    # SIDE edges (constant phi at i=0 and i=N_ANG)
    for (i, sgn) in ((0, -1.0), (N_ANG, 1.0)):
        phi = phis[i]
        # outward tangential reference (points away from the patch centre)
        ref = (-sgn * math.sin(phi), sgn * math.cos(phi), 0.0)
        for j in range(N_Z):
            a = back[i][j]
            b = front[i][j]
            c = front[i][j + 1]
            d = back[i][j + 1]
            mesh.quad(a, b, c, d, ref)

    # TOP edge (z_top) and BOTTOM edge (z_bot)
    for (j, refz) in ((N_Z, 1.0), (0, -1.0)):
        for i in range(N_ANG):
            a = back[i][j]
            b = front[i][j]
            c = front[i + 1][j]
            d = back[i + 1][j]
            mesh.quad(a, b, c, d, (0.0, 0.0, refz))

    # ---- recentre: bottom to z=0, centre x/y near origin ----
    xs = [p[0] for row in front + back for p in row]
    ys = [p[1] for row in front + back for p in row]
    dx = -(min(xs) + max(xs)) / 2.0
    dy = -(min(ys) + max(ys)) / 2.0
    dz = -z_bot
    mesh.tris = [tuple((px + dx, py + dy, pz + dz) for (px, py, pz) in t) for t in mesh.tris]

    # footprint bbox after shift
    fxmin, fxmax = min(xs) + dx, max(xs) + dx
    fymin, fymax = min(ys) + dy, max(ys) + dy

    # ---- FOOT: a flat box from z=0..FOOT_HEIGHT, overlapping the panel base ----
    x0, x1 = fxmin - FOOT_MARGIN, fxmax + FOOT_MARGIN
    y0, y1 = fymin - FOOT_MARGIN, fymax + FOOT_MARGIN
    z0, z1 = 0.0, FOOT_HEIGHT
    _add_box(mesh, x0, x1, y0, y1, z0, z1)

    info = dict(variant=variant, coupon_h=COUPON_HEIGHT, arc_w=2 * ang_half * (inner_r + WALL + belly),
                flutes=N_FLUTES, wall_min=WALL, wall_max=WALL + belly + amp,
                foot=(x1 - x0, y1 - y0, FOOT_HEIGHT), tris=len(mesh.tris),
                overall=(x1 - x0, y1 - y0, COUPON_HEIGHT))
    return mesh, info


def _add_box(mesh, x0, x1, y0, y1, z0, z1):
    v = {
        0: (x0, y0, z0), 1: (x1, y0, z0), 2: (x1, y1, z0), 3: (x0, y1, z0),
        4: (x0, y0, z1), 5: (x1, y0, z1), 6: (x1, y1, z1), 7: (x0, y1, z1),
    }
    faces = [
        ((0, 1, 2, 3), (0, 0, -1)),   # bottom
        ((4, 5, 6, 7), (0, 0, 1)),    # top
        ((0, 1, 5, 4), (0, -1, 0)),   # -y
        ((1, 2, 6, 5), (1, 0, 0)),    # +x
        ((2, 3, 7, 6), (0, 1, 0)),    # +y
        ((3, 0, 4, 7), (-1, 0, 0)),   # -x
    ]
    for (a, b, c, d), ref in faces:
        mesh.quad(v[a], v[b], v[c], v[d], ref)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "stl")
    os.makedirs(out, exist_ok=True)
    variant = "zen-classic"
    mesh, info = build_coupon(variant)
    path = os.path.join(out, f"test-coupon-{variant}.stl")
    n = mesh.write_binary_stl(path)
    print(f"[coupon] {variant}: patch {info['arc_w']:.1f}mm wide x {info['coupon_h']:.0f}mm tall, "
          f"{info['flutes']} flute, wall {info['wall_min']:.1f}-{info['wall_max']:.1f}mm")
    print(f"         foot {info['foot'][0]:.1f} x {info['foot'][1]:.1f} x {info['foot'][2]:.1f}mm, "
          f"overall bbox ~{info['overall'][0]:.1f} x {info['overall'][1]:.1f} x {info['overall'][2]:.1f}mm, "
          f"tris={n}")
    print("wrote", os.path.relpath(path, here))


if __name__ == "__main__":
    main()
