#!/usr/bin/env python3
"""
Glass-insert bamboo sleeve — fluted planter that takes a straight glass cylinder.
================================================================================

The printed part is now a decorative fluted SLEEVE; a straight glass vase drops
inside and holds the water (so no waterproofing at all). It is the zen-classic
fluted body (plumb, full-height flutes, flat top rim) bored for the glass, with
just a TINY QUARTER-ROUND BEVEL softening the sharp top rim edge — nothing else.

Glass insert (measured):
  * Height    148 mm
  * OD        100.3-100.9 mm  (use 100.9 for fit)
  * Wall      3.5 mm  (ID ~93.8)

Fit / proportions (defaults):
  * Bore ID 101.9 mm  -> 0.5 mm/side slip fit over the glass.
  * Solid closed floor (4 mm) — the glass rests on it (no drainage hole).
  * Sleeve height = glass height + floor, so the glass sits FLUSH with the rim.
  * Body wall (bore -> flute valley) 5.5 mm; the fluted body bows out (barrel)
    via `belly`; a 5 mm quarter-round bevel softens the top rim edge.

Interior stays a plumb cylinder (the glass bore). Exterior = bore + wall + flute,
with the flutes fading and the wall coving in over the top `neck_h`. Vertical
flutes => no overhangs. Millimetres. Pure Python, no dependencies.
"""
import math
import os
from generate_bamboo_vase import Mesh, smoothstep

# ---- glass insert ----
GLASS_OD = 100.9
GLASS_H = 148.0

# ---- fit / build ----
CLEARANCE = 0.5             # radial slip fit over the glass
WALL_MIN = 5.5              # body wall, bore -> flute valley (thick enough for a 5mm bevel)
FLOOR = 4.0                 # solid floor thickness
FLOOR_HOLE_DIA = 0.0        # center push-hole diameter (0 = solid floor)
SLEEVE_H = GLASS_H + FLOOR  # printed height = flush with the top of the glass
ROUNDOVER_R = 5.0           # quarter-round bevel on the top rim edge (<= WALL_MIN)
N_THETA = 128               # AD5M/fuzzy-friendly resolution
N_Z = 130


def build_sleeve(n_waves, amp, belly=0.0):
    r_glass = GLASS_OD / 2.0
    r_bore = r_glass + CLEARANCE                 # 50.95
    r_hole = FLOOR_HOLE_DIA / 2.0
    H = SLEEVE_H
    z_round = H - ROUNDOVER_R                     # where the top-edge bevel begins

    def r_body(theta, z):
        # fluted body that bows out (barrel) via `belly`, peaking at mid-height
        # and returning to the wall at the base and rim (so the bevel always has
        # a full WALL_MIN to work with).
        bow = belly * math.sin(math.pi * z / H)
        return r_bore + WALL_MIN + bow + amp * (0.5 + 0.5 * math.cos(n_waves * theta))

    def r_out(theta, z):
        # Bowed fluted body with a flat top rim; the sharp top OUTER edge is
        # softened by a quarter-round bevel over the last ROUNDOVER_R mm (rolls
        # in, tangent horizontal at the rim). No taper, neck, or dome.
        if z <= z_round:
            return r_body(theta, z)
        rb = r_body(theta, z_round)          # freeze body radius at the bevel start
        dz = z - z_round
        return (rb - ROUNDOVER_R) + math.sqrt(max(0.0, ROUNDOVER_R ** 2 - dz ** 2))

    n = N_THETA
    th = [2 * math.pi * i / n for i in range(n)]
    cs = [math.cos(t) for t in th]
    sn = [math.sin(t) for t in th]

    mesh = Mesh()

    # OUTER surface: coarse up the plumb body, dense through the top roundover
    NB = max(60, int(z_round / 1.5))
    NR = 12
    zs_outer = [z_round * j / NB for j in range(NB)] + \
               [z_round + ROUNDOVER_R * k / NR for k in range(NR + 1)]
    O = [[(r_out(th[i], z) * cs[i], r_out(th[i], z) * sn[i], z) for i in range(n)]
         for z in zs_outer]
    for j in range(len(zs_outer) - 1):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = O[j][i], O[j][i2], O[j + 1][i2], O[j + 1][i]
            mesh.quad(a, b, c, d, (a[0] + c[0], a[1] + c[1], 0.0))

    # INNER bore (z = FLOOR .. H), plumb cylinder r_bore
    NI = max(30, int((H - FLOOR) / 3))
    zs_inner = [FLOOR + (H - FLOOR) * j / NI for j in range(NI + 1)]
    I = [[(r_bore * cs[i], r_bore * sn[i], z) for i in range(n)] for z in zs_inner]
    for j in range(len(zs_inner) - 1):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = I[j][i], I[j][i2], I[j + 1][i2], I[j + 1][i]
            mesh.quad(a, b, c, d, (-a[0], -a[1], 0.0))

    # TOP rim (outer_top -> bore_top) — flat annulus at z = H
    for i in range(n):
        i2 = (i + 1) % n
        mesh.quad(O[-1][i], O[-1][i2], I[-1][i2], I[-1][i], (0, 0, 1))

    if r_hole > 0.0:
        # center push-hole wall (r_hole, z = 0 .. FLOOR), faces into the hole
        Hb = [(r_hole * cs[i], r_hole * sn[i], 0.0) for i in range(n)]
        Hf = [(r_hole * cs[i], r_hole * sn[i], FLOOR) for i in range(n)]
        for i in range(n):
            i2 = (i + 1) % n
            mesh.quad(Hb[i], Hb[i2], Hf[i2], Hf[i], (-cs[i], -sn[i], 0.0))
            mesh.quad(O[0][i], O[0][i2], Hb[i2], Hb[i], (0, 0, -1))   # bottom annulus
            mesh.quad(I[0][i], I[0][i2], Hf[i2], Hf[i], (0, 0, 1))    # inner floor annulus
    else:
        # solid floor: full disks (fan to center) top and bottom
        cb = (0.0, 0.0, 0.0)
        cf = (0.0, 0.0, FLOOR)
        for i in range(n):
            i2 = (i + 1) % n
            mesh.add(cb, O[0][i], O[0][i2], (0, 0, -1))   # bottom disk, faces down
            mesh.add(cf, I[0][i], I[0][i2], (0, 0, 1))    # inner floor disk, faces up

    reveal = (GLASS_H + FLOOR) - SLEEVE_H
    info = dict(n_waves=n_waves, amp=amp, bore=2 * r_bore,
                outer_valley=2 * (r_bore + WALL_MIN), outer_crest=2 * (r_bore + WALL_MIN + amp),
                height=SLEEVE_H, reveal=reveal, bevel=ROUNDOVER_R, tris=len(mesh.tris))
    return mesh, info


VARIANTS = [
    # name           n_waves  amp   belly (bow-out at mid-height)
    ("14rib-bow3",   14,      4.0,   3.0),   # subtle bow
    ("14rib-bow6",   14,      4.0,   6.0),   # moderate bow (near the original)
    ("14rib-bow10",  14,      4.0,  10.0),   # full barrel bow
    ("11rib-bow7",   11,      5.5,   7.0),   # beefier ribs, bowed
    ("8rib-bow8",     8,      7.0,   8.0),   # bold lobes, bowed
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "stl", "glass-sleeve")
    os.makedirs(out, exist_ok=True)
    for name, n, amp, belly in VARIANTS:
        mesh, info = build_sleeve(n, amp, belly)
        path = os.path.join(out, f"glass-sleeve-{name}.stl")
        nt = mesh.write_binary_stl(path)
        print(f"[{name:13s}] ribs={info['n_waves']:2d} depth={info['amp']:.1f}  "
              f"bore={info['bore']:.1f}  OD valley/crest={info['outer_valley']:.0f}/{info['outer_crest']:.0f}  "
              f"H={info['height']:.0f} reveal={info['reveal']:.0f}mm tris={nt}")


if __name__ == "__main__":
    main()
