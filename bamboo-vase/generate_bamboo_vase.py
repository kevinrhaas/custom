#!/usr/bin/env python3
"""
Bamboo Wave-Ring Vase — parametric STL generator (pure Python, no dependencies)
==============================================================================

Design brief
------------
A "Wave Ring" vessel for a bunch of lucky (curly) bamboo:
  * Plant   ~ 610 mm (24 in) tall, top-heavy, curly stalks + foliage.
  * Bunch   ~ 76 mm (3 in) across at the base (the stalk bundle).
Water is held with the print + a coat of spray rubber (Flex Seal / Plasti Dip).
Glass beads are poured around the bunch to CENTER it and to add low ballast so a
tall, top-heavy plant does not tip.

Design philosophy (the short version)
-------------------------------------
  * ONE gesture: continuous vertical flutes wrapping the body (like an ensō
    that never closes). Nothing else competes with it.
  * Vertical flutes => ZERO overhangs printed upright, and a natural grip.
  * Mass low, walls thick: the vessel + beads + water put the center of gravity
    near the floor. Stability is designed in, not hoped for.
  * Straight (plumb) interior so a spray-rubber coat goes on clean and even.
  * Proportions from thirds / gentle golden ratios rather than round numbers.

Geometry model
--------------
The INTERIOR is the honest shape: a plumb (vertical) cylinder of radius
`inner_r`, with a solid floor. This guarantees:
  * no interior overhang (walls never close inward),
  * a smooth surface that is easy to seal.

The EXTERIOR is the interior offset outward by the wall thickness, plus the
flute term, plus an optional subtle belly:

    r_out(theta, z) = inner_r + wall + belly(z) + amp * (0.5 + 0.5*cos(n*theta))

Using (0.5 + 0.5*cos) keeps flute VALLEYS exactly `wall` thick (never thinner)
and CRESTS `wall + amp` thick — so the wall is strongest where the ribs are, and
we never print a paper-thin valley. Flutes run the full height (to the rim and
to the base) exactly like the reference card, so the walls stay perfectly plumb
and overhang-free. The belly (if any) is a gentle barrel added to the outside
only; it stays well under 45 deg so it also prints support-free.

Everything is in millimetres.
"""

import math
import struct
import os

# ----------------------------------------------------------------------------
# Reference measurements (from the user's photos)
# ----------------------------------------------------------------------------
BUNCH_DIA = 76.0          # mm, stalk bundle across the base (~3 in)
PLANT_HEIGHT = 610.0      # mm, overall plant height (~24 in) -- for proportion notes

# ----------------------------------------------------------------------------
# Small math helpers
# ----------------------------------------------------------------------------
def smoothstep(e0, e1, x):
    if e1 == e0:
        return 0.0 if x < e0 else 1.0
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3.0 - 2.0 * t)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normalize(a):
    m = math.sqrt(dot(a, a))
    if m < 1e-12:
        return (0.0, 0.0, 1.0)
    return (a[0] / m, a[1] / m, a[2] / m)


# ----------------------------------------------------------------------------
# Mesh container with orientation-safe triangle insertion
# ----------------------------------------------------------------------------
class Mesh:
    def __init__(self):
        self.tris = []  # list of (p0, p1, p2) with outward-facing winding

    def add(self, p0, p1, p2, ref):
        """Add a triangle, flipping it so its normal points along `ref`
        (the geometric outward direction). Makes the STL orientation robust
        regardless of how we happened to order the corners."""
        n = cross(sub(p1, p0), sub(p2, p0))
        if dot(n, ref) < 0.0:
            p1, p2 = p2, p1
        self.tris.append((p0, p1, p2))

    def quad(self, a, b, c, d, ref):
        """Add a quad a-b-c-d as two triangles."""
        self.add(a, b, c, ref)
        self.add(a, c, d, ref)

    def write_binary_stl(self, path):
        with open(path, "wb") as f:
            f.write(b"\x00" * 80)                       # 80-byte header
            f.write(struct.pack("<I", len(self.tris)))  # triangle count
            for p0, p1, p2 in self.tris:
                n = normalize(cross(sub(p1, p0), sub(p2, p0)))
                f.write(struct.pack("<3f", *n))
                f.write(struct.pack("<3f", *p0))
                f.write(struct.pack("<3f", *p1))
                f.write(struct.pack("<3f", *p2))
                f.write(struct.pack("<H", 0))
        return len(self.tris)


# ----------------------------------------------------------------------------
# Vase generator
# ----------------------------------------------------------------------------
def build_vase(inner_dia=105.0,     # interior diameter at the wall (bead + bunch space)
               height=130.0,        # overall vessel height
               n_waves=14,          # number of flutes around
               amp=4.0,             # flute depth (crest sits amp beyond the valley)
               belly=3.0,           # gentle exterior barrel (0 = perfectly plumb)
               wall=2.8,            # min wall thickness (at flute valleys)
               floor=4.0,           # solid floor thickness
               n_theta=None,        # angular resolution (auto if None)
               n_z=None):           # vertical resolution (auto if None)
    """Return (Mesh, info_dict) for one vase variant."""
    inner_r = inner_dia / 2.0
    if n_theta is None:
        n_theta = max(256, n_waves * 14)
    if n_z is None:
        n_z = max(80, int(round(height / 1.5)))

    # Exterior mean/crest radius as a function of (theta, z)
    def belly_z(z):
        # subtle barrel: peaks at mid-height, zero at both ends
        return belly * math.sin(math.pi * (z / height))

    def r_out(theta, z):
        flute = amp * (0.5 + 0.5 * math.cos(n_waves * theta))
        return inner_r + wall + belly_z(z) + flute

    mesh = Mesh()

    # Precompute angle samples
    thetas = [2.0 * math.pi * i / n_theta for i in range(n_theta)]
    cs = [math.cos(t) for t in thetas]
    sn = [math.sin(t) for t in thetas]

    # ---- OUTER WALL (z = 0 .. height) ----
    outer = [[None] * n_theta for _ in range(n_z + 1)]
    for iz in range(n_z + 1):
        z = height * iz / n_z
        for it in range(n_theta):
            r = r_out(thetas[it], z)
            outer[iz][it] = (r * cs[it], r * sn[it], z)
    for iz in range(n_z):
        for it in range(n_theta):
            it2 = (it + 1) % n_theta
            a = outer[iz][it]
            b = outer[iz][it2]
            c = outer[iz + 1][it2]
            d = outer[iz + 1][it]
            # outward reference = radial direction at the quad centre
            mx = (a[0] + b[0] + c[0] + d[0]) / 4.0
            my = (a[1] + b[1] + c[1] + d[1]) / 4.0
            mesh.quad(a, b, c, d, (mx, my, 0.0))

    # ---- INNER WALL (cavity: z = floor .. height), plumb cylinder ----
    inner = [[None] * n_theta for _ in range(n_z + 1)]
    z_floor = floor
    for iz in range(n_z + 1):
        z = z_floor + (height - z_floor) * iz / n_z
        for it in range(n_theta):
            inner[iz][it] = (inner_r * cs[it], inner_r * sn[it], z)
    for iz in range(n_z):
        for it in range(n_theta):
            it2 = (it + 1) % n_theta
            a = inner[iz][it]
            b = inner[iz][it2]
            c = inner[iz + 1][it2]
            d = inner[iz + 1][it]
            # inward reference = toward the axis
            mx = (a[0] + b[0] + c[0] + d[0]) / 4.0
            my = (a[1] + b[1] + c[1] + d[1]) / 4.0
            mesh.quad(a, b, c, d, (-mx, -my, 0.0))

    # ---- TOP RIM (annulus connecting outer top ring to inner top ring) ----
    for it in range(n_theta):
        it2 = (it + 1) % n_theta
        a = outer[n_z][it]
        b = outer[n_z][it2]
        c = inner[n_z][it2]
        d = inner[n_z][it]
        mesh.quad(a, b, c, d, (0.0, 0.0, 1.0))

    # ---- OUTER BOTTOM CAP (scalloped disk at z = 0) ----
    center_bottom = (0.0, 0.0, 0.0)
    for it in range(n_theta):
        it2 = (it + 1) % n_theta
        a = outer[0][it]
        b = outer[0][it2]
        mesh.add(center_bottom, a, b, (0.0, 0.0, -1.0))

    # ---- INNER FLOOR CAP (disk at z = floor, faces up into the cavity) ----
    center_floor = (0.0, 0.0, z_floor)
    for it in range(n_theta):
        it2 = (it + 1) % n_theta
        a = inner[0][it]
        b = inner[0][it2]
        mesh.add(center_floor, a, b, (0.0, 0.0, 1.0))

    # ---- INFO ----
    outer_max_dia = 2.0 * (inner_r + wall + belly + amp)   # crest at belly
    outer_min_dia = 2.0 * (inner_r + wall)                 # valley at ends
    # worst-case exterior overhang from the belly barrel (deg from vertical)
    belly_slope = belly * math.pi / height                 # max |dr/dz| of belly term
    overhang_deg = math.degrees(math.atan(belly_slope))
    cavity_depth = height - floor
    # approximate usable water/bead volume (plumb cylinder cavity)
    cavity_vol_ml = math.pi * inner_r ** 2 * cavity_depth / 1000.0
    bead_gap = (inner_dia - BUNCH_DIA) / 2.0

    info = dict(
        inner_dia=inner_dia, height=height, n_waves=n_waves, amp=amp,
        belly=belly, wall=wall, floor=floor,
        outer_max_dia=outer_max_dia, outer_min_dia=outer_min_dia,
        overhang_deg=overhang_deg, cavity_depth=cavity_depth,
        cavity_vol_ml=cavity_vol_ml, bead_gap=bead_gap,
        n_theta=n_theta, n_z=n_z, tris=len(mesh.tris),
    )
    return mesh, info


# ----------------------------------------------------------------------------
# Optional drop-in CENTERING COLLAR
# ----------------------------------------------------------------------------
def build_collar(inner_dia=105.0,          # must match the vase's interior diameter
                 bunch_dia=BUNCH_DIA,
                 bunch_clearance=6.0,       # extra room around the bunch
                 plug_height=12.0,          # how far it drops into the cavity
                 flange=8.0,                # how far the top lip overhangs the rim
                 thickness=3.0,             # flange thickness
                 n_theta=256):
    """A clean top-hat ring that drops into the rim: the central hole holds the
    bunch dead-centre while glass beads fill around it below. Pour the beads in
    first, stand the bunch, then slide this down over the stalks to rest on the
    rim. Print FLANGE-SIDE DOWN (fully support-free that way).

    Cross-section (a stepped tube, closed and manifold):

        hole_r        plug_r  flange_r
          |             |        |
          |   plug      |        |   z_top
          |_____________|        |
          |             |________|   thickness
          |                      |
          |______________________|   z=0  (flange bottom, on the rim)
    """
    plug_r = inner_dia / 2.0 - 0.4          # slides into the cavity with a little slop
    flange_r = inner_dia / 2.0 + flange     # rests on the rim
    hole_r = (bunch_dia + bunch_clearance) / 2.0

    mesh = Mesh()
    thetas = [2.0 * math.pi * i / n_theta for i in range(n_theta)]
    cs = [math.cos(t) for t in thetas]
    sn = [math.sin(t) for t in thetas]

    # Printed flange-side down: z=0 is the flange (bottom), plug rises upward.
    z_top = plug_height

    def ring(r, z, it):
        return (r * cs[it], r * sn[it], z)

    for it in range(n_theta):
        it2 = (it + 1) % n_theta

        # bottom face: flange_r .. hole_r at z=0 (faces down)
        mesh.quad(ring(flange_r, 0, it), ring(flange_r, 0, it2),
                  ring(hole_r, 0, it2), ring(hole_r, 0, it), (0, 0, -1))

        # outer flange wall: flange_r cylinder z=0..thickness (faces out)
        a = ring(flange_r, 0, it)
        mesh.quad(a, ring(flange_r, 0, it2),
                  ring(flange_r, thickness, it2), ring(flange_r, thickness, it),
                  (a[0], a[1], 0))

        # flange top step: flange_r .. plug_r at z=thickness (faces up)
        mesh.quad(ring(flange_r, thickness, it), ring(flange_r, thickness, it2),
                  ring(plug_r, thickness, it2), ring(plug_r, thickness, it), (0, 0, 1))

        # plug outer wall: plug_r cylinder z=thickness..z_top (faces out)
        a = ring(plug_r, thickness, it)
        mesh.quad(a, ring(plug_r, thickness, it2),
                  ring(plug_r, z_top, it2), ring(plug_r, z_top, it),
                  (a[0], a[1], 0))

        # plug top: plug_r .. hole_r at z=z_top (faces up)
        mesh.quad(ring(plug_r, z_top, it), ring(plug_r, z_top, it2),
                  ring(hole_r, z_top, it2), ring(hole_r, z_top, it), (0, 0, 1))

        # hole inner wall: hole_r cylinder z=0..z_top (faces in)
        a = ring(hole_r, 0, it)
        mesh.quad(a, ring(hole_r, 0, it2),
                  ring(hole_r, z_top, it2), ring(hole_r, z_top, it),
                  (-a[0], -a[1], 0))

    info = dict(inner_dia=inner_dia, hole_dia=2 * hole_r, flange_dia=2 * flange_r,
                plug_height=plug_height, tris=len(mesh.tris))
    return mesh, info


# ----------------------------------------------------------------------------
# Variant catalogue
# ----------------------------------------------------------------------------
VARIANTS = [
    # name              inner_dia  height  n_waves  amp   belly
    ("zen-squat",        112.0,     95.0,    12,    5.0,  0.0),   # wide, grounded, deep lobes
    ("zen-classic",      105.0,    130.0,    14,    4.0,  3.0),   # balanced hero, subtle belly
    ("zen-tall",         100.0,    170.0,    16,    3.5,  4.0),   # more presence, deeper well
    ("fine-flute",       105.0,    130.0,    24,    2.5,  0.0),   # fine modern ribbing, great grip
    ("bold-wave",        105.0,    125.0,     9,    6.5,  4.0),   # dramatic pumpkin lobes
    ("zen-mini",          95.0,     90.0,    12,    4.0,  0.0),   # snug / compact
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "stl")
    os.makedirs(out, exist_ok=True)

    rows = []
    for name, dia, h, n, amp, belly in VARIANTS:
        mesh, info = build_vase(inner_dia=dia, height=h, n_waves=n, amp=amp, belly=belly)
        path = os.path.join(out, f"bamboo-vase-{name}.stl")
        ntri = mesh.write_binary_stl(path)
        rows.append((name, info, ntri))
        print(f"[vase]   {name:12s} "
              f"H={info['height']:.0f} dia_out={info['outer_max_dia']:.0f} "
              f"waves={info['n_waves']:2d} amp={info['amp']:.1f} "
              f"belly={info['belly']:.1f} overhang={info['overhang_deg']:.1f}deg "
              f"vol~{info['cavity_vol_ml']:.0f}ml beads~{info['bead_gap']:.0f}mm "
              f"tris={ntri}")

    # centering collars for the two most common interior sizes
    for dia in (105.0, 112.0):
        cmesh, cinfo = build_collar(inner_dia=dia)
        cpath = os.path.join(out, f"centering-collar-{int(dia)}mm.stl")
        cn = cmesh.write_binary_stl(cpath)
        print(f"[collar] dia={dia:.0f} hole={cinfo['hole_dia']:.0f} "
              f"flange={cinfo['flange_dia']:.0f} tris={cn}")

    print("\nDone. STLs written to:", out)


if __name__ == "__main__":
    main()
