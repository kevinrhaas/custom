#!/usr/bin/env python3
"""
Fuzzy-skin finish test coupons — labeled on the base plate.
===========================================================

Each coupon is a slice of the zen-classic side wall (true curvature + one full
flute, printed STANDING so the layer lines match the real vase) sitting on a
flat nameplate. The finish name is RAISED on top of the plate, in front of the
wall, so the fluted test surface stays completely clean for judging the finish.

Fuzzy skin itself is a *slicer* setting (OrcaSlicer / Bambu Studio), not part of
the mesh. Print one coupon per row of the table in the README, set the matching
fuzzy-skin parameters in the slicer, and the embossed name tells you which is
which afterwards.

Pure Python, no dependencies. Millimetres.
"""
import math
import os
from generate_bamboo_vase import Mesh
from generate_test_coupon import VARIANT_PARAMS, WALL

# ---- coupon / plate settings ----
VARIANT = "zen-classic"
COUPON_HEIGHT = 22.0     # mm, height of the wall patch
N_FLUTES = 1             # full flutes wide (crest between two valleys)
PLATE_H = 4.0            # mm, nameplate thickness
PLATE_MARGIN = 4.0       # mm, plate overhang around the wall footprint
LABEL_RELIEF = 0.8       # mm, how far the letters stand up
LABEL_GAP = 3.0          # mm, gap between wall front and the label block
LABEL_END = 3.0          # mm, plate margin in front of the label
PIXEL_MAX = 0.9          # mm, max bitmap pixel size (caps letter size)
N_ANG = 96
N_Z = 52

# ---- 5x7 blocky font (only the glyphs we need + space) ----
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "N": ["#...#", "##..#", "#.#.#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}
GLYPH_W, GLYPH_H = 5, 7


def add_box(mesh, x0, x1, y0, y1, z0, z1):
    v = {0: (x0, y0, z0), 1: (x1, y0, z0), 2: (x1, y1, z0), 3: (x0, y1, z0),
         4: (x0, y0, z1), 5: (x1, y0, z1), 6: (x1, y1, z1), 7: (x0, y1, z1)}
    for (a, b, c, d), ref in [((0, 1, 2, 3), (0, 0, -1)), ((4, 5, 6, 7), (0, 0, 1)),
                              ((0, 1, 5, 4), (0, -1, 0)), ((1, 2, 6, 5), (1, 0, 0)),
                              ((2, 3, 7, 6), (0, 1, 0)), ((3, 0, 4, 7), (-1, 0, 0))]:
        mesh.quad(v[a], v[b], v[c], v[d], ref)


def build_coupon(label):
    inner_dia, n, amp, belly, height = VARIANT_PARAMS[VARIANT]
    inner_r = inner_dia / 2.0
    z_center = height / 2.0
    z_bot, z_top = z_center - COUPON_HEIGHT / 2.0, z_center + COUPON_HEIGHT / 2.0

    def belly_z(z):
        return belly * math.sin(math.pi * (z / height))

    def r_out(phi, z):
        return inner_r + WALL + belly_z(z) + amp * (0.5 + 0.5 * math.cos(n * phi))

    period = 2.0 * math.pi / n
    ang_half = N_FLUTES * period / 2.0
    phis = [(-ang_half + 2 * ang_half * i / N_ANG) for i in range(N_ANG + 1)]
    zs = [z_bot + (z_top - z_bot) * j / N_Z for j in range(N_Z + 1)]

    # front (fluted) grid in vase frame
    fx = [[r_out(p, z) * math.cos(p) for z in zs] for p in phis]
    fy = [[r_out(p, z) * math.sin(p) for z in zs] for p in phis]

    x_back = min(min(col) for col in fx) - 2.5
    dx, dz = -x_back, -z_bot                 # back plane -> x=0, base -> z=0
    y_max = max(max(abs(v) for v in col) for col in fy)

    F = [[(fx[i][j] + dx, fy[i][j], zs[j] + dz) for j in range(N_Z + 1)] for i in range(N_ANG + 1)]
    B = [[(0.0, -y_max + 2 * y_max * i / N_ANG, zs[j] + dz) for j in range(N_Z + 1)] for i in range(N_ANG + 1)]
    panel_depth = max(F[i][j][0] for i in range(N_ANG + 1) for j in range(N_Z + 1))

    mesh = Mesh()
    # front (curved, fluted) and back (flat)
    for i in range(N_ANG):
        for j in range(N_Z):
            mesh.quad(F[i][j], F[i + 1][j], F[i + 1][j + 1], F[i][j + 1], (1, 0, 0))
            mesh.quad(B[i][j], B[i + 1][j], B[i + 1][j + 1], B[i][j + 1], (-1, 0, 0))
    # top & bottom rims (front edge <-> back edge)
    for i in range(N_ANG):
        mesh.quad(F[i][N_Z], F[i + 1][N_Z], B[i + 1][N_Z], B[i][N_Z], (0, 0, 1))
        mesh.quad(F[i][0], F[i + 1][0], B[i + 1][0], B[i][0], (0, 0, -1))
    # left & right side rims (front edge <-> back edge)
    for j in range(N_Z):
        mesh.quad(F[0][j], B[0][j], B[0][j + 1], F[0][j + 1], (0, -1, 0))
        mesh.quad(F[N_ANG][j], B[N_ANG][j], B[N_ANG][j + 1], F[N_ANG][j + 1], (0, 1, 0))

    # ---- label sizing ----
    label = label.upper()
    ncols = GLYPH_W * len(label) + (len(label) - 1)   # 1px inter-glyph gap
    usable_y = 2 * y_max - 2.0
    p = min(PIXEL_MAX, usable_y / ncols, (2 * y_max) / ncols)
    text_w = ncols * p
    text_h = GLYPH_H * p

    # label block sits on the plate, in front of the wall
    label_x0 = panel_depth + LABEL_GAP
    label_x1 = label_x0 + text_h

    # ---- nameplate ----
    plate_x0 = -PLATE_MARGIN
    plate_x1 = label_x1 + LABEL_END
    plate_y0 = -(y_max + PLATE_MARGIN)
    plate_y1 = (y_max + PLATE_MARGIN)
    add_box(mesh, plate_x0, plate_x1, plate_y0, plate_y1, 0.0, PLATE_H)

    # ---- raised letters on the plate top (rows -> +x, cols -> +y) ----
    # Letters are separate solids embedded 0.5mm into the plate and grown by a
    # tiny epsilon so neighbours overlap volumetrically (no coincident faces) —
    # the slicer unions them into clean relief.
    y_start = -text_w / 2.0
    eps = 0.02
    zl0, zl1 = PLATE_H - 0.5, PLATE_H + LABEL_RELIEF
    for ci, ch in enumerate(label):
        glyph = FONT.get(ch, FONT[" "])
        base_col = ci * (GLYPH_W + 1)
        for r in range(GLYPH_H):
            row = glyph[r]
            c = 0
            while c < GLYPH_W:
                if row[c] == "#":
                    c0 = c
                    while c < GLYPH_W and row[c] == "#":
                        c += 1
                    # run [c0, c) -> one box (merge horizontally)
                    yy0 = y_start + (base_col + c0) * p - eps
                    yy1 = y_start + (base_col + c) * p + eps
                    xx0 = label_x0 + r * p - eps
                    xx1 = label_x0 + (r + 1) * p + eps
                    add_box(mesh, xx0, xx1, yy0, yy1, zl0, zl1)
                else:
                    c += 1

    info = dict(label=label, pixel=p, text=(text_w, text_h),
                plate=(plate_x1 - plate_x0, plate_y1 - plate_y0, PLATE_H),
                overall=(plate_x1 - plate_x0, plate_y1 - plate_y0, COUPON_HEIGHT),
                tris=len(mesh.tris))
    return mesh, info


# name -> (fuzzy-skin settings summary)  [settings live in the README table]
COUPONS = [
    # stock noise types (as shown in the screenshots, default params)
    "CLASSIC", "PERLIN", "BILLOW", "RIDGED", "VORONOI",
    # curated recipes (beyond defaults)
    "BARK", "SUEDE", "RIPPLE", "CRYSTAL",
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "stl", "fuzzy")
    os.makedirs(out, exist_ok=True)
    for label in COUPONS:
        mesh, info = build_coupon(label)
        path = os.path.join(out, f"fuzzy-coupon-{label.lower()}.stl")
        n = mesh.write_binary_stl(path)
        print(f"[{label:8s}] pixel={info['pixel']:.2f}mm text {info['text'][0]:.1f}x{info['text'][1]:.1f} "
              f"plate {info['plate'][0]:.0f}x{info['plate'][1]:.0f}x{info['plate'][2]:.0f} "
              f"tris={n}")
    print("\nWrote", len(COUPONS), "coupons to", os.path.relpath(out, here))


if __name__ == "__main__":
    main()
