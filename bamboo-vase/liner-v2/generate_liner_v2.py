#!/usr/bin/env python3
"""
V2 watertight liner for the ORIGINAL zen-classic bamboo vase (print in PETG).
============================================================================

Fixes vs the v1 liner:
  * No flange / lip — a plain straight-walled cup.
  * Height comes up flush to the vase rim (0.5 mm below), not proud of it.
  * Thicker walls + floor tuned for a 0.6 mm nozzle so it seals reliably.

Fit (to the original zen-classic — measured from the printed 3mf):
  * Interior bore 105.0 mm, 130 mm tall, 4 mm floor -> 126 mm cavity depth.

Liner:
  * Body OD 103.5 mm  -> ~0.75 mm/side slip fit into the 105 mm bore (a touch
    looser than v1 because a 0.6 nozzle lays wider outer walls).
  * Height 125.5 mm   -> rests on the vase floor, top sits 0.5 mm below the rim.
  * Wall 3.0 mm, floor 3.6 mm  -> substantial for a 0.6 nozzle (see README for
    the wave-gentle PETG print settings that seal watertight).
  * Small lead-in chamfer at the bottom edge so it drops in cleanly.

Prints upright, open end up, no supports. Millimetres. Pure Python.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate_bamboo_vase import Mesh  # noqa: E402

# ---- original vase interior (zen-classic) ----
BORE_DIA = 105.0
CAVITY_DEPTH = 126.0        # vase floor-to-rim

# ---- liner ----
OD = 103.5                  # body outer diameter (slip fit)
WALL = 3.0                  # side wall thickness (>=4 perims at 0.6 nozzle)
FLOOR = 3.6                 # solid floor thickness
TOP_GAP = 0.5               # how far below the rim the liner top sits
CHAMFER_H = 1.2             # bottom lead-in chamfer
N_THETA = 160


def build_liner():
    r_out = OD / 2.0
    r_in = r_out - WALL
    r_cham = r_out - 0.8
    H = CAVITY_DEPTH - TOP_GAP                    # 125.5

    def ro(z):
        if z < CHAMFER_H:
            return r_cham + (r_out - r_cham) * (z / CHAMFER_H)
        return r_out

    n = N_THETA
    th = [2 * math.pi * i / n for i in range(n)]
    cs = [math.cos(t) for t in th]
    sn = [math.sin(t) for t in th]

    nZ = 200
    zs_out = [H * j / nZ for j in range(nZ + 1)]
    zs_in = [FLOOR + (H - FLOOR) * j / nZ for j in range(nZ + 1)]

    mesh = Mesh()

    # OUTER wall
    O = [[(ro(z) * cs[i], ro(z) * sn[i], z) for i in range(n)] for z in zs_out]
    for j in range(nZ):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = O[j][i], O[j][i2], O[j + 1][i2], O[j + 1][i]
            mesh.quad(a, b, c, d, (a[0] + c[0], a[1] + c[1], 0.0))

    # INNER wall (plumb)
    I = [[(r_in * cs[i], r_in * sn[i], z) for i in range(n)] for z in zs_in]
    for j in range(nZ):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = I[j][i], I[j][i2], I[j + 1][i2], I[j + 1][i]
            mesh.quad(a, b, c, d, (-a[0], -a[1], 0.0))

    # TOP rim (flat annulus)
    for i in range(n):
        i2 = (i + 1) % n
        mesh.quad(O[nZ][i], O[nZ][i2], I[nZ][i2], I[nZ][i], (0, 0, 1))

    # BOTTOM cap (solid disk) and INNER floor cap
    cb = (0.0, 0.0, 0.0)
    cf = (0.0, 0.0, FLOOR)
    for i in range(n):
        i2 = (i + 1) % n
        mesh.add(cb, O[0][i], O[0][i2], (0, 0, -1))
        mesh.add(cf, I[0][i], I[0][i2], (0, 0, 1))

    water_ml = math.pi * r_in ** 2 * (H - FLOOR) / 1000.0
    info = dict(od=OD, id=2 * r_in, height=H, wall=WALL, floor=FLOOR,
                clearance=(BORE_DIA - OD) / 2.0, top_gap=TOP_GAP,
                water_ml=water_ml, tris=len(mesh.tris))
    return mesh, info


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    mesh, info = build_liner()
    path = os.path.join(here, "liner-zen-classic-v2-petg.stl")
    n = mesh.write_binary_stl(path)
    print(f"v2 liner: OD {info['od']:.1f}  ID {info['id']:.1f}  H {info['height']:.1f}mm  "
          f"wall {info['wall']}  floor {info['floor']}")
    print(f"          {info['clearance']:.2f}mm/side into the 105mm bore, top {info['top_gap']}mm "
          f"below rim, ~{info['water_ml']:.0f} ml, tris={n}")


if __name__ == "__main__":
    main()
