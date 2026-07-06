#!/usr/bin/env python3
"""
Wave Gentle snake-plant planter family.

Generates six paired STL designs:
  - planter body with 180 mm mouth, smooth interior, drain holes, chamfered lip
  - integrated-looking 20 mm drip tray with a printable 3-lug twist lock

The mesh is generated explicitly as closed STL surfaces. No CAD boolean engine
or third-party Python package is required.
"""

import math
import os
import struct
from dataclasses import dataclass
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

MOUTH_INNER_DIA = 180.0
MOUTH_INNER_R = MOUTH_INNER_DIA / 2.0
WALL = 3.2
FLOOR_T = 6.0
BODY_H = 150.0
BODY_BOTTOM_R = 69.0
TRAY_H = 20.0
TRAY_FLOOR_T = 3.2
ASSEMBLY_GAP = 5.0

N_THETA = 288
N_Z = 96
FLOOR_SEG = N_THETA


def smoothstep(a, b, x):
    if a == b:
        return 0.0 if x < a else 1.0
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    m = math.sqrt(max(1e-24, dot(a, a)))
    return (a[0] / m, a[1] / m, a[2] / m)


class Mesh:
    def __init__(self):
        self.tris = []

    def add(self, a, b, c, ref):
        n = cross(sub(b, a), sub(c, a))
        if dot(n, ref) < 0.0:
            b, c = c, b
        self.tris.append((a, b, c))

    def quad(self, a, b, c, d, ref):
        self.add(a, b, c, ref)
        self.add(a, c, d, ref)

    def write_stl(self, path):
        with open(path, "wb") as f:
            f.write(b"Wave Gentle planter STL".ljust(80, b"\0"))
            f.write(struct.pack("<I", len(self.tris)))
            for a, b, c in self.tris:
                n = norm(cross(sub(b, a), sub(c, a)))
                f.write(struct.pack("<3f", *n))
                f.write(struct.pack("<3f", *a))
                f.write(struct.pack("<3f", *b))
                f.write(struct.pack("<3f", *c))
                f.write(struct.pack("<H", 0))

    def edge_report(self):
        def key(p):
            return (round(p[0], 5), round(p[1], 5), round(p[2], 5))

        counts = {}
        for tri in self.tris:
            for i, j in ((0, 1), (1, 2), (2, 0)):
                e = tuple(sorted((key(tri[i]), key(tri[j]))))
                counts[e] = counts.get(e, 0) + 1
        naked = sum(1 for v in counts.values() if v == 1)
        bad = sum(1 for v in counts.values() if v != 2)
        return naked, bad, len(counts)


@dataclass
class Variant:
    name: str
    waves: int
    amp: float
    belly: float
    twist_deg: float
    randomness: float
    phase2: float
    lug_sweep: float


VARIANTS = [
    Variant("01-soft-current", 18, 3.0, 5.0, 8.0, 0.25, 0.2, 34.0),
    Variant("02-calm-flute", 24, 2.2, 3.0, 4.0, 0.10, 1.4, 28.0),
    Variant("03-deep-tide", 14, 4.6, 7.0, 12.0, 0.18, 2.1, 38.0),
    Variant("04-organic-drift", 17, 3.8, 6.0, -7.0, 0.55, 3.0, 36.0),
    Variant("05-fine-ripple", 30, 1.8, 2.5, 16.0, 0.20, 0.9, 26.0),
    Variant("06-broad-swell", 11, 5.4, 8.0, -12.0, 0.15, 2.6, 42.0),
]


def angle_delta(a, b):
    return (a - b + math.pi) % (2.0 * math.pi) - math.pi


def wave_term(theta, zfrac, v):
    twist = math.radians(v.twist_deg) * zfrac
    base = 0.5 + 0.5 * math.cos(v.waves * (theta - twist))
    secondary = 0.5 + 0.5 * math.cos((v.waves - 3) * theta + v.phase2 + 1.7 * zfrac)
    tertiary = 0.5 + 0.5 * math.cos(3 * theta - v.phase2 + 2.5 * zfrac)
    raw = (1.0 - v.randomness) * base + v.randomness * (0.72 * base + 0.20 * secondary + 0.08 * tertiary)
    return max(0.0, min(1.0, raw))


def inner_radius(zfrac):
    # Snake-plant friendly: narrower base for soil control, 180 mm clear mouth.
    return BODY_BOTTOM_R + (MOUTH_INNER_R - BODY_BOTTOM_R) * (zfrac ** 0.82)


def belly(zfrac, v):
    return v.belly * math.sin(math.pi * zfrac)


def lug_extra(theta, z, v):
    # Three bayonet lugs grown directly into the lower wall, with printable ramps.
    if z < 7.0 or z > 17.0:
        return 0.0
    zshape = smoothstep(7.0, 10.0, z) * (1.0 - smoothstep(14.0, 17.0, z))
    sweep = math.radians(v.lug_sweep)
    extra = 0.0
    for k in range(3):
        center = 2.0 * math.pi * k / 3.0 + math.radians(10.0)
        d = abs(angle_delta(theta, center))
        if d < sweep / 2.0:
            circum = 0.5 + 0.5 * math.cos(math.pi * d / (sweep / 2.0))
            ramp = 0.82 + 0.18 * math.sin(angle_delta(theta, center) * 2.2)
            extra = max(extra, 7.0 * zshape * circum * ramp)
    return extra


def outer_radius(theta, z, v):
    zfrac = z / BODY_H
    rim_soften = 1.0 - 0.85 * smoothstep(0.955, 1.0, zfrac)
    lip_chamfer = 2.4 * smoothstep(0.965, 1.0, zfrac)
    return (
        inner_radius(zfrac)
        + WALL
        + belly(zfrac, v)
        + v.amp * wave_term(theta, zfrac, v) * rim_soften
        - lip_chamfer
        + lug_extra(theta, z, v)
    )


def polar_point(r, theta, z):
    return (r * math.cos(theta), r * math.sin(theta), z)


def add_ring_wall(mesh, rings, outward=True):
    n_z = len(rings) - 1
    n_t = len(rings[0])
    for iz in range(n_z):
        for it in range(n_t):
            it2 = (it + 1) % n_t
            a, b = rings[iz][it], rings[iz][it2]
            c, d = rings[iz + 1][it2], rings[iz + 1][it]
            mx = (a[0] + b[0] + c[0] + d[0]) / 4.0
            my = (a[1] + b[1] + c[1] + d[1]) / 4.0
            ref = (mx, my, 0.0) if outward else (-mx, -my, 0.0)
            mesh.quad(a, b, c, d, ref)


def drain_open(radial_mid, theta_mid):
    # Center drain plus six softened radial drain slots. Slots are aligned to
    # the polar mesh so their through-walls are explicit and closed.
    if radial_mid < 7.0:
        return True
    if 17.0 < radial_mid < 45.0:
        for k in range(6):
            center = 2.0 * math.pi * k / 6.0 + math.radians(30.0)
            if abs(angle_delta(theta_mid, center)) < math.radians(5.8):
                return True
    return False


def add_drain_floor(mesh, radius, z0, z1):
    # Radial levels are denser near slot boundaries and the central drain.
    radial = [7.0, 10.5, 14.0, 17.0, 22.0, 28.0, 34.0, 40.0, 45.0, 51.0, 58.0, radius]
    radial = sorted(set(r for r in radial if r < radius - 0.5) | {radius})
    thetas = [2.0 * math.pi * i / FLOOR_SEG for i in range(FLOOR_SEG)]

    def p(r, t, z):
        return (r * math.cos(t), r * math.sin(t), z)

    solid = {}
    for ir in range(len(radial) - 1):
        r0, r1 = radial[ir], radial[ir + 1]
        rm = 0.5 * (r0 + r1)
        for it in range(FLOOR_SEG):
            t0, t1 = thetas[it], thetas[(it + 1) % FLOOR_SEG]
            # unwrap final cell midpoint cleanly
            tm = t0 + math.pi / FLOOR_SEG
            solid[(ir, it)] = not drain_open(rm, tm)

    for (ir, it), is_solid in solid.items():
        if not is_solid:
            continue
        r0, r1 = radial[ir], radial[ir + 1]
        t0, t1 = thetas[it], thetas[(it + 1) % FLOOR_SEG]
        a0, b0, c0, d0 = p(r0, t0, z0), p(r1, t0, z0), p(r1, t1, z0), p(r0, t1, z0)
        a1, b1, c1, d1 = p(r0, t0, z1), p(r1, t0, z1), p(r1, t1, z1), p(r0, t1, z1)
        mesh.quad(a1, b1, c1, d1, (0, 0, 1))
        mesh.quad(a0, b0, c0, d0, (0, 0, -1))

        neighbors = [
            ((ir - 1, it), (a0, d0, d1, a1), (-math.cos((t0 + t1) / 2), -math.sin((t0 + t1) / 2), 0)),
            ((ir + 1, it), (b0, c0, c1, b1), (math.cos((t0 + t1) / 2), math.sin((t0 + t1) / 2), 0)),
            ((ir, (it - 1) % FLOOR_SEG), (a0, b0, b1, a1), (-math.sin(t0), math.cos(t0), 0)),
            ((ir, (it + 1) % FLOOR_SEG), (d0, c0, c1, d1), (math.sin(t1), -math.cos(t1), 0)),
        ]
        for nkey, quad, ref in neighbors:
            if nkey[0] >= len(radial) - 1:
                continue
            if nkey not in solid or not solid[nkey]:
                mesh.quad(*quad, ref)


def build_pot(v):
    mesh = Mesh()
    thetas = [2.0 * math.pi * i / N_THETA for i in range(N_THETA)]
    outer = []
    inner = []
    for iz in range(N_Z + 1):
        z = BODY_H * iz / N_Z
        zfrac = z / BODY_H
        outer.append([polar_point(outer_radius(t, z, v), t, z) for t in thetas])
        zi = FLOOR_T + (BODY_H - FLOOR_T) * iz / N_Z
        inner.append([polar_point(inner_radius(zi / BODY_H), t, zi) for t in thetas])

    add_ring_wall(mesh, outer, outward=True)
    add_ring_wall(mesh, inner, outward=False)

    # Chamfered top lip annulus.
    for it in range(N_THETA):
        it2 = (it + 1) % N_THETA
        mesh.quad(outer[-1][it], outer[-1][it2], inner[-1][it2], inner[-1][it], (0, 0, 1))

    # Drainage floor with one center hole plus six radial drain slots.
    floor_r = inner_radius(FLOOR_T / BODY_H)
    add_drain_floor(mesh, floor_r, 0.0, FLOOR_T)

    # Lower exterior bottom annulus outside the drainage floor.
    for it, t in enumerate(thetas):
        it2 = (it + 1) % N_THETA
        t2 = thetas[it2]
        r = floor_r
        mesh.quad(
            outer[0][it], outer[0][it2],
            polar_point(r, t2, 0.0), polar_point(r, t, 0.0),
            (0, 0, -1),
        )

    return mesh


def tray_outer_radius(theta, zfrac, v):
    # Matches the pot's lower visual rhythm, softened for a saucer wall.
    base = BODY_BOTTOM_R + WALL + 2.0
    return base + 0.55 * v.amp * wave_term(theta, 0.08 + 0.12 * zfrac, v)


def shelf_extra(theta, z, v):
    # Internal bayonet shelves, leaving three open lead-in gaps.
    if z < 12.0 or z > 17.5:
        return 0.0
    zshape = smoothstep(12.0, 14.0, z) * (1.0 - smoothstep(16.2, 17.5, z))
    sweep = math.radians(v.lug_sweep + 12.0)
    extra = 0.0
    for k in range(3):
        center = 2.0 * math.pi * k / 3.0 + math.radians(44.0)
        d = abs(angle_delta(theta, center))
        if d < sweep / 2.0:
            extra = max(extra, 7.8 * zshape * (0.5 + 0.5 * math.cos(math.pi * d / (sweep / 2.0))))
    return extra


def build_tray(v):
    mesh = Mesh()
    n_z = 36
    thetas = [2.0 * math.pi * i / N_THETA for i in range(N_THETA)]
    outer = []
    inner = []
    for iz in range(n_z + 1):
        z = TRAY_H * iz / n_z
        zfrac = z / TRAY_H
        # Taper out slightly toward the top, like the blue reference.
        outer.append([polar_point(tray_outer_radius(t, zfrac, v) + 2.5 * zfrac, t, z) for t in thetas])
        zi = TRAY_FLOOR_T + (TRAY_H - TRAY_FLOOR_T) * iz / n_z
        zifrac = zi / TRAY_H
        inner_base = tray_outer_radius(thetas[0], zifrac, v) - 5.0
        row = []
        for t in thetas:
            ir = inner_base - shelf_extra(t, zi, v)
            row.append(polar_point(ir, t, zi))
        inner.append(row)

    add_ring_wall(mesh, outer, outward=True)
    add_ring_wall(mesh, inner, outward=False)

    # Top rim annulus.
    for it in range(N_THETA):
        it2 = (it + 1) % N_THETA
        mesh.quad(outer[-1][it], outer[-1][it2], inner[-1][it2], inner[-1][it], (0, 0, 1))

    # Saucer floor, closed underside and open basin above.
    floor_top = []
    floor_bot = []
    center_top = (0.0, 0.0, TRAY_FLOOR_T)
    center_bot = (0.0, 0.0, 0.0)
    for it, t in enumerate(thetas):
        floor_top.append(inner[0][it])
        floor_bot.append(polar_point(tray_outer_radius(t, 0, v), t, 0.0))
    for it in range(N_THETA):
        it2 = (it + 1) % N_THETA
        mesh.add(center_top, floor_top[it], floor_top[it2], (0, 0, 1))
        mesh.add(center_bot, floor_bot[it], floor_bot[it2], (0, 0, -1))

    return mesh


def write_manifest(rows):
    lines = [
        "# Wave Gentle Snake Planter STL Set",
        "",
        "Common dimensions:",
        f"- clear mouth opening: {MOUTH_INNER_DIA:.0f} mm",
        f"- planter body height: {BODY_H:.0f} mm",
        f"- minimum wall at wave valleys: {WALL:.1f} mm",
        f"- drainage floor thickness: {FLOOR_T:.1f} mm",
        f"- drip tray height: {TRAY_H:.0f} mm",
        f"- intended assembled visual gap: {ASSEMBLY_GAP:.0f} mm between tray rim and pot bottom",
        "",
        "Each variation has a matching pot STL and tray STL. The twist lock uses three rounded bayonet lugs;",
        "drop the pot into the tray openings and turn clockwise until the lugs sit under the internal shelves.",
        "",
        "| Variation | Waves | Wave depth | Belly | Twist | Notes |",
        "|---|---:|---:|---:|---:|---|",
    ]
    notes = {
        "01-soft-current": "balanced hero, close to the reference card",
        "02-calm-flute": "denser and quieter vertical flow",
        "03-deep-tide": "deeper broad waves, more sculptural",
        "04-organic-drift": "most irregular, natural movement",
        "05-fine-ripple": "finest texture, modern and restrained",
        "06-broad-swell": "boldest broad lobes, most rounded",
    }
    for v, _, _ in rows:
        lines.append(f"| {v.name} | {v.waves} | {v.amp:.1f} mm | {v.belly:.1f} mm | {v.twist_deg:.0f} deg | {notes[v.name]} |")
    lines += [
        "",
        "Printing notes:",
        "- Print both parts upright.",
        "- Use at least 3-4 perimeters; the floor and rim are intentionally thick.",
        "- The pot has drain holes, so use a normal solid-wall profile, not vase mode.",
        "- For a water-holding planter, seal the inside after printing; FDM is not reliably waterproof by itself.",
        "- The lock is designed with clearance, but first test-fit gently and sand the tray shelves if your filament over-extrudes.",
    ]
    (OUT_DIR / "README.md").write_text("\n".join(lines) + "\n")


def main():
    rows = []
    for v in VARIANTS:
        pot = build_pot(v)
        tray = build_tray(v)
        pot_path = OUT_DIR / f"wave-gentle-{v.name}-pot.stl"
        tray_path = OUT_DIR / f"wave-gentle-{v.name}-tray.stl"
        pot.write_stl(pot_path)
        tray.write_stl(tray_path)
        rows.append((v, pot, tray))
        print(f"{v.name}: pot tris={len(pot.tris)} edges={pot.edge_report()} | tray tris={len(tray.tris)} edges={tray.edge_report()}")
    write_manifest(rows)


if __name__ == "__main__":
    main()
