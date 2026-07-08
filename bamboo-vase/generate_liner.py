#!/usr/bin/env python3
"""
Watertight inner liner cup for the zen-classic vase (print in PETG).
====================================================================

The idea: instead of sealing the decorative PLA shell, drop a simple straight-
walled cup inside it that actually holds the water. PETG bonds between layers
far better than PLA, so with solid walls + floor it prints watertight on its own
(a spray-rubber coat is then just optional insurance).

Fit (to the zen-classic interior — a plumb 105 mm bore, 126 mm deep):
  * Body OD 104 mm  -> 0.5 mm radial slip-fit into the 105 mm bore.
  * Body height 125 mm -> bottom rests on the vase floor (weight carried there,
    not by the rim).
  * Short flared rim (OD ~109 mm) seats on the vase lip, hides the gap, and
    gives you something to grip when lifting the liner out.
  * Interior ID 100 mm -> ~12 mm of bead room around the 76 mm bunch.

Prints upright, open end up, NO supports (the rim flare is a gentle ~18 deg
cone, not an overhang). Millimetres. Pure Python, no dependencies.
"""
import math
import os
from generate_bamboo_vase import Mesh

# ---- fit parameters ----
BORE_DIA = 105.0          # vase interior diameter (zen-classic)
CAVITY_DEPTH = 126.0      # vase floor-to-rim depth
RADIAL_CLEARANCE = 0.5    # slip fit per side

# ---- liner geometry ----
WALL = 2.0                # side wall thickness (PETG, watertight with 4 perimeters)
FLOOR = 2.5               # solid floor thickness
BODY_H = 125.0            # straight body height (rests on vase floor)
FLARE_H = 6.0             # rim flare rise
FLARE_OUT = 2.5           # rim flare radial growth
CHAMFER_H = 1.0           # bottom lead-in chamfer (eases insertion)
N_THETA = 128


def build_liner():
    r_body = BORE_DIA / 2.0 - RADIAL_CLEARANCE     # 52.0
    r_in = r_body - WALL                            # 50.0
    r_flare = r_body + FLARE_OUT                     # 54.5
    r_cham = r_body - 0.6
    H = BODY_H + FLARE_H                             # 131.0

    def r_out(z):
        if z < CHAMFER_H:
            return r_cham + (r_body - r_cham) * (z / CHAMFER_H)
        if z <= BODY_H:
            return r_body
        return r_body + (r_flare - r_body) * (z - BODY_H) / FLARE_H

    n = N_THETA
    th = [2 * math.pi * i / n for i in range(n)]
    cs = [math.cos(t) for t in th]
    sn = [math.sin(t) for t in th]

    nZ = 220
    zs_out = [H * j / nZ for j in range(nZ + 1)]
    zs_in = [FLOOR + (H - FLOOR) * j / nZ for j in range(nZ + 1)]

    mesh = Mesh()

    # OUTER wall
    O = [[(r_out(z) * cs[i], r_out(z) * sn[i], z) for i in range(n)] for z in zs_out]
    for j in range(nZ):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = O[j][i], O[j][i2], O[j + 1][i2], O[j + 1][i]
            mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
            mesh.quad(a, b, c, d, (mx, my, 0.0))

    # INNER wall (plumb r_in)
    I = [[(r_in * cs[i], r_in * sn[i], z) for i in range(n)] for z in zs_in]
    for j in range(nZ):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = I[j][i], I[j][i2], I[j + 1][i2], I[j + 1][i]
            mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
            mesh.quad(a, b, c, d, (-mx, -my, 0.0))

    # TOP rim (inner_top -> outer_top)
    for i in range(n):
        i2 = (i + 1) % n
        mesh.quad(O[nZ][i], O[nZ][i2], I[nZ][i2], I[nZ][i], (0, 0, 1))

    # BOTTOM outer cap (disk at z=0)
    cb = (0.0, 0.0, 0.0)
    for i in range(n):
        i2 = (i + 1) % n
        mesh.add(cb, O[0][i], O[0][i2], (0, 0, -1))

    # INNER floor cap (disk at z=FLOOR, faces up into the cup)
    cf = (0.0, 0.0, FLOOR)
    for i in range(n):
        i2 = (i + 1) % n
        mesh.add(cf, I[0][i], I[0][i2], (0, 0, 1))

    water_ml = math.pi * r_in ** 2 * (H - FLOOR) / 1000.0
    info = dict(body_od=2 * r_body, id=2 * r_in, flare_od=2 * r_flare, height=H,
                wall=WALL, floor=FLOOR, clearance=RADIAL_CLEARANCE,
                float_gap=CAVITY_DEPTH - BODY_H, water_ml=water_ml, tris=len(mesh.tris))
    return mesh, info


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "stl")
    os.makedirs(out, exist_ok=True)
    mesh, info = build_liner()
    path = os.path.join(out, "liner-zen-classic-petg.stl")
    n = mesh.write_binary_stl(path)
    print(f"liner: body OD {info['body_od']:.0f}  ID {info['id']:.0f}  flare OD {info['flare_od']:.0f}  "
          f"H {info['height']:.0f}mm  wall {info['wall']}  floor {info['floor']}")
    print(f"       slip-fit {info['clearance']}mm/side into 105mm bore, rests on vase floor, "
          f"~{info['water_ml']:.0f} ml to the brim, tris={n}")


if __name__ == "__main__":
    main()
