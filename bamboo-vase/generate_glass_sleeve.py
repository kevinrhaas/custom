#!/usr/bin/env python3
"""
Glass-insert bamboo sleeve — fluted planter that takes a straight glass cylinder.
================================================================================

The printed part is now a decorative fluted SLEEVE; a straight glass vase drops
inside and holds the water (so no waterproofing at all). Instead of a flat
sliced rim, the top FLUTES FADE and the wall leans in on a simple STRAIGHT CONE
TAPER (no curve, no lip) up to meet the glass — a clean transition from the
printed body into the glass cylinder.

Glass insert (measured):
  * Height    148 mm
  * OD        100.3-100.9 mm  (use 100.9 for fit)
  * Wall      3.5 mm  (ID ~93.8)

Fit / proportions (defaults):
  * Bore ID 101.9 mm  -> 0.5 mm/side slip fit over the glass.
  * Solid closed floor (4 mm) — the glass rests on it (no drainage hole).
  * Glass rests on the floor; sleeve is 127 mm tall so ~25 mm of glass + its
    rounded rim rises above the coved collar.
  * Body wall (bore -> flute valley) 3.5 mm; ribs add on top of that.

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
CLEARANCE = 0.5              # radial slip fit over the glass
WALL_MIN = 3.5              # body wall, bore -> flute valley
FLOOR = 4.0                 # solid floor thickness
FLOOR_HOLE_DIA = 0.0        # center push-hole diameter (0 = solid floor)
SLEEVE_H = 127.0            # overall printed height (glass reveal = GLASS_H+FLOOR - SLEEVE_H)
NECK_H = 22.0              # height of the straight cone taper at the top
RIM_LIP = 1.2               # rim wall thickness where the taper meets the glass
N_THETA = 128               # AD5M/fuzzy-friendly resolution
N_Z = 130


def build_sleeve(n_waves, amp, belly=0.0):
    r_glass = GLASS_OD / 2.0
    r_bore = r_glass + CLEARANCE                 # 50.95
    r_hole = FLOOR_HOLE_DIA / 2.0
    top_r = r_bore + RIM_LIP                      # outer radius at the rim
    z_neck = SLEEVE_H - NECK_H
    H = SLEEVE_H

    def outer_mean(z):
        base = r_bore + WALL_MIN + belly * math.sin(math.pi * min(z, z_neck) / z_neck)
        if z <= z_neck:
            return base
        # Straight cone taper: a simple linear lean-in from the body to the rim,
        # no curve, no lip. The flutes fade over the taper so the top is a clean
        # smooth cone meeting the glass.
        u = (z - z_neck) / NECK_H
        return base + (top_r - base) * u

    def env(z):
        if z <= z_neck:
            return 1.0
        return 1.0 - smoothstep(0.0, 1.0, (z - z_neck) / NECK_H)

    def r_out(theta, z):
        return outer_mean(z) + amp * env(z) * (0.5 + 0.5 * math.cos(n_waves * theta))

    n = N_THETA
    th = [2 * math.pi * i / n for i in range(n)]
    cs = [math.cos(t) for t in th]
    sn = [math.sin(t) for t in th]

    mesh = Mesh()

    # OUTER surface (z = 0 .. H)
    O = [[None] * n for _ in range(N_Z + 1)]
    for j in range(N_Z + 1):
        z = H * j / N_Z
        for i in range(n):
            r = r_out(th[i], z)
            O[j][i] = (r * cs[i], r * sn[i], z)
    for j in range(N_Z):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = O[j][i], O[j][i2], O[j + 1][i2], O[j + 1][i]
            mesh.quad(a, b, c, d, (a[0] + c[0], a[1] + c[1], 0.0))

    # INNER bore (z = FLOOR .. H), plumb cylinder r_bore
    I = [[None] * n for _ in range(N_Z + 1)]
    for j in range(N_Z + 1):
        z = FLOOR + (H - FLOOR) * j / N_Z
        for i in range(n):
            I[j][i] = (r_bore * cs[i], r_bore * sn[i], z)
    for j in range(N_Z):
        for i in range(n):
            i2 = (i + 1) % n
            a, b, c, d = I[j][i], I[j][i2], I[j + 1][i2], I[j + 1][i]
            mesh.quad(a, b, c, d, (-a[0], -a[1], 0.0))

    # TOP rim (outer_top -> bore_top)
    for i in range(n):
        i2 = (i + 1) % n
        mesh.quad(O[N_Z][i], O[N_Z][i2], I[N_Z][i2], I[N_Z][i], (0, 0, 1))

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
                height=SLEEVE_H, reveal=reveal, rim=RIM_LIP, tris=len(mesh.tris))
    return mesh, info


VARIANTS = [
    # name          n_waves  amp   belly
    ("14rib-base",   14,      4.0,  0.0),   # zen-classic match
    ("11rib-medium", 11,      5.5,  0.0),   # beefier
    ("8rib-chunky",   8,      7.0,  0.0),   # bold rounded lobes
    ("6rib-bold",     6,      8.5,  0.0),   # dramatic scallops
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
