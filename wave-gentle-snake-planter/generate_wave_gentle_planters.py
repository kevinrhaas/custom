#!/usr/bin/env python3
"""
Wave Gentle snake-plant planter family, v2.

This version restudies the reference image:
  - squat rounded bowl silhouette, flatter foot, plump middle, tucked mouth
  - ribs are wandering ribbons that split and rejoin, not even bamboo flutes
  - support-free tray system using five broad raised support discs/mounds
  - pot floor stays 6 mm thick with drain openings around support zones

No third-party packages are required.
"""

import math
import os
import struct
from dataclasses import dataclass
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent

MOUTH_INNER_R = 90.0
BODY_H = 150.0
FLOOR_T = 6.0
WALL = 3.4
TRAY_WALL_H = 20.0
TRAY_FLOOR_T = 3.2
SUPPORT_H = 25.0

N_THETA = 336
N_Z = 112
FLOOR_SEG = N_THETA

SUPPORTS = [
    (0.0, 0.0, 18.0),
    (43.0, 0.0, 19.5),
    (0.0, 43.0, 19.5),
    (-43.0, 0.0, 19.5),
    (0.0, -43.0, 19.5),
]


def smoothstep(a, b, x):
    if a == b:
        return 0.0 if x < a else 1.0
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def clamp(x, a, b):
    return max(a, min(b, x))


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

    def extend(self, other):
        self.tris.extend(other.tris)

    def write_stl(self, path):
        with open(path, "wb") as f:
            f.write(b"Wave Gentle planter v2".ljust(80, b"\0"))
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
    ribs: int
    amp: float
    branch: float
    drift: float
    width: float
    belly: float
    seed: float


VARIANTS = [
    Variant("01-reference-soft-bowl", 15, 5.6, 0.52, 0.16, 0.060, 18.0, 0.2),
    Variant("02-tall-gentle-current", 17, 4.7, 0.45, 0.20, 0.052, 15.0, 1.1),
    Variant("03-deep-branching-wave", 13, 6.7, 0.66, 0.22, 0.070, 20.0, 2.0),
    Variant("04-quiet-many-ribbons", 21, 3.9, 0.36, 0.13, 0.044, 14.0, 2.8),
    Variant("05-organic-split-flow", 16, 5.9, 0.72, 0.25, 0.058, 19.0, 3.7),
    Variant("06-broad-soft-swell", 11, 7.4, 0.58, 0.18, 0.082, 21.0, 4.6),
]


def angle_delta(a, b):
    return (a - b + math.pi) % (2.0 * math.pi) - math.pi


def polar(r, t, z):
    return (r * math.cos(t), r * math.sin(t), z)


def inner_radius(zfrac):
    # Smooth printable interior: narrower bottom, full 180 mm mouth.
    return 62.0 + (MOUTH_INNER_R - 62.0) * (smoothstep(0.02, 1.0, zfrac) ** 0.62)


def bowl_bulge(zfrac, v):
    # Reference silhouette: flat-ish foot, round shoulder, tucked mouth.
    belly = v.belly * (math.sin(math.pi * zfrac) ** 0.82)
    lower_round = 5.0 * smoothstep(0.02, 0.22, zfrac) * (1.0 - smoothstep(0.36, 0.62, zfrac))
    rim_tuck = 3.2 * smoothstep(0.84, 1.0, zfrac)
    return belly + lower_round - rim_tuck


def ridge_center(base, zfrac, i, v):
    ph = v.seed + i * 1.731
    drift = v.drift * math.sin(2.0 * math.pi * zfrac + ph)
    drift += 0.45 * v.drift * math.sin(4.0 * math.pi * zfrac + ph * 0.71)
    drift += 0.025 * math.sin(7.0 * math.pi * zfrac + ph)
    return base + drift


def ridge_field(theta, zfrac, v):
    # Ribs split in the middle and rejoin near foot/rim. The split is smooth,
    # not a hard Y-junction, so the surface remains printable and calm.
    total = 0.0
    max_possible = 0.0
    split_profile = math.sin(math.pi * zfrac) ** 1.25
    rim_fade = 1.0 - 0.52 * smoothstep(0.88, 1.0, zfrac)
    foot_fade = smoothstep(0.02, 0.13, zfrac)
    for i in range(v.ribs):
        base = 2.0 * math.pi * i / v.ribs
        ph = v.seed + i * 0.91
        c = ridge_center(base, zfrac, i, v)
        local_amp = 0.82 + 0.18 * math.sin(ph)
        split = v.branch * (2.0 * math.pi / v.ribs) * split_profile * (0.75 + 0.25 * math.sin(ph * 1.7))
        width = v.width * (0.88 + 0.18 * math.sin(ph + 2.0 * zfrac))
        # One ribbon becomes two soft shoulders through the middle.
        for off, weight in ((-split, 0.55), (split, 0.55), (0.0, 0.20 * (1.0 - split_profile))):
            d = angle_delta(theta, c + off)
            g = math.exp(-0.5 * (d / width) ** 2)
            total += local_amp * weight * g
            max_possible += weight
    return clamp(total * foot_fade * rim_fade, 0.0, 1.55)


def outer_radius(theta, z, v):
    zfrac = z / BODY_H
    base = inner_radius(zfrac) + WALL + bowl_bulge(zfrac, v)
    ribs = v.amp * ridge_field(theta, zfrac, v)
    lip_chamfer = 2.5 * smoothstep(0.965, 1.0, zfrac)
    return base + ribs - lip_chamfer


def add_ring_wall(mesh, rings, outward=True):
    for iz in range(len(rings) - 1):
        for it in range(len(rings[0])):
            it2 = (it + 1) % len(rings[0])
            a, b = rings[iz][it], rings[iz][it2]
            c, d = rings[iz + 1][it2], rings[iz + 1][it]
            mx = (a[0] + b[0] + c[0] + d[0]) / 4.0
            my = (a[1] + b[1] + c[1] + d[1]) / 4.0
            ref = (mx, my, 0.0) if outward else (-mx, -my, 0.0)
            mesh.quad(a, b, c, d, ref)


def point_in_support(x, y, clearance=4.0):
    for sx, sy, sr in SUPPORTS:
        if (x - sx) ** 2 + (y - sy) ** 2 < (sr + clearance) ** 2:
            return True
    return False


def drain_open(rm, tm):
    x, y = rm * math.cos(tm), rm * math.sin(tm)
    if point_in_support(x, y, 7.0):
        return False
    # Four long curved drains between the support discs. All openings have
    # vertical walls and stay away from the floor perimeter.
    if 22.0 < rm < 54.0:
        for k in range(4):
            center = math.radians(45.0 + 90.0 * k)
            if abs(angle_delta(tm, center)) < math.radians(7.0):
                return True
    return False


def add_drain_floor(mesh, radius, z0, z1):
    radial = [8.0, 16.0, 22.0, 30.0, 38.0, 46.0, 54.0, radius]
    radial = sorted(set(r for r in radial if r < radius - 0.25) | {radius})
    thetas = [2.0 * math.pi * i / FLOOR_SEG for i in range(FLOOR_SEG)]

    def p(r, t, z):
        return (r * math.cos(t), r * math.sin(t), z)

    solid = {}
    for ir in range(len(radial) - 1):
        rm = 0.5 * (radial[ir] + radial[ir + 1])
        for it in range(FLOOR_SEG):
            tm = thetas[it] + math.pi / FLOOR_SEG
            solid[(ir, it)] = not drain_open(rm, tm)

    center0 = (0.0, 0.0, z0)
    center1 = (0.0, 0.0, z1)
    r_center = radial[0]
    for it in range(FLOOR_SEG):
        t0, t1 = thetas[it], thetas[(it + 1) % FLOOR_SEG]
        mesh.add(center1, p(r_center, t0, z1), p(r_center, t1, z1), (0, 0, 1))
        mesh.add(center0, p(r_center, t0, z0), p(r_center, t1, z0), (0, 0, -1))

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
            if nkey[0] < 0:
                continue
            if nkey[0] >= len(radial) - 1:
                continue
            if nkey not in solid or not solid[nkey]:
                mesh.quad(*quad, ref)


def build_pot(v):
    mesh = Mesh()
    thetas = [2.0 * math.pi * i / N_THETA for i in range(N_THETA)]
    outer, inner = [], []
    for iz in range(N_Z + 1):
        z = BODY_H * iz / N_Z
        outer.append([polar(outer_radius(t, z, v), t, z) for t in thetas])
        zi = FLOOR_T + (BODY_H - FLOOR_T) * iz / N_Z
        inner.append([polar(inner_radius(zi / BODY_H), t, zi) for t in thetas])

    add_ring_wall(mesh, outer, True)
    add_ring_wall(mesh, inner, False)

    for it in range(N_THETA):
        it2 = (it + 1) % N_THETA
        mesh.quad(outer[-1][it], outer[-1][it2], inner[-1][it2], inner[-1][it], (0, 0, 1))

    floor_r = inner_radius(FLOOR_T / BODY_H)
    add_drain_floor(mesh, floor_r, 0.0, FLOOR_T)
    for it, t in enumerate(thetas):
        it2 = (it + 1) % N_THETA
        t2 = thetas[it2]
        mesh.quad(
            outer[0][it], outer[0][it2],
            polar(floor_r, t2, 0.0), polar(floor_r, t, 0.0),
            (0, 0, -1),
        )
    return mesh


def tray_radius(theta, zfrac, v):
    low = 77.0 + 1.6 * ridge_field(theta, 0.05, v)
    high = 92.5 + 1.2 * ridge_field(theta, 0.12, v)
    return low + (high - low) * smoothstep(0.0, 1.0, zfrac)


def cylinder(cx, cy, r, z0, z1, n=96, cap_bottom=False):
    mesh = Mesh()
    angles = [2.0 * math.pi * i / n for i in range(n)]
    bottom = [(cx + r * math.cos(a), cy + r * math.sin(a), z0) for a in angles]
    top = [(cx + r * math.cos(a), cy + r * math.sin(a), z1) for a in angles]
    ctop = (cx, cy, z1)
    cbottom = (cx, cy, z0)
    for i in range(n):
        i2 = (i + 1) % n
        mx = 0.5 * (top[i][0] + top[i2][0]) - cx
        my = 0.5 * (top[i][1] + top[i2][1]) - cy
        mesh.quad(bottom[i], bottom[i2], top[i2], top[i], (mx, my, 0))
        mesh.add(ctop, top[i], top[i2], (0, 0, 1))
        if cap_bottom:
            mesh.add(cbottom, bottom[i], bottom[i2], (0, 0, -1))
    return mesh


def build_tray(v):
    mesh = Mesh()
    n_z = 38
    thetas = [2.0 * math.pi * i / N_THETA for i in range(N_THETA)]
    outer, inner = [], []
    for iz in range(n_z + 1):
        z = TRAY_WALL_H * iz / n_z
        zf = z / TRAY_WALL_H
        outer.append([polar(tray_radius(t, zf, v), t, z) for t in thetas])
        zi = TRAY_FLOOR_T + (TRAY_WALL_H - TRAY_FLOOR_T) * iz / n_z
        zif = zi / TRAY_WALL_H
        inner.append([polar(tray_radius(t, zif, v) - 5.2, t, zi) for t in thetas])
    add_ring_wall(mesh, outer, True)
    add_ring_wall(mesh, inner, False)

    for it in range(N_THETA):
        it2 = (it + 1) % N_THETA
        mesh.quad(outer[-1][it], outer[-1][it2], inner[-1][it2], inner[-1][it], (0, 0, 1))
        mesh.add((0, 0, 0), outer[0][it], outer[0][it2], (0, 0, -1))
        mesh.add((0, 0, TRAY_FLOOR_T), inner[0][it], inner[0][it2], (0, 0, 1))

    # Five broad support mounds. They overlap the saucer floor slightly so
    # slicers merge them into one printed part; no thin load-bearing walls.
    for sx, sy, sr in SUPPORTS:
        mesh.extend(cylinder(sx, sy, sr, TRAY_FLOOR_T - 0.15, SUPPORT_H, 96, True))
    return mesh


def write_readme(rows):
    notes = {
        "01-reference-soft-bowl": "closest to the reference: plump silhouette, moderate branching",
        "02-tall-gentle-current": "slightly calmer and more vertical",
        "03-deep-branching-wave": "stronger split/rejoin ribs and deeper shadows",
        "04-quiet-many-ribbons": "more numerous fine ribbons, less dramatic",
        "05-organic-split-flow": "most wandering and organic",
        "06-broad-soft-swell": "fewest, broadest, roundest waves",
    }
    lines = [
        "# Wave Gentle Snake Planter STL Set",
        "",
        "V2 restudies the reference image: squat rounded bowl silhouette, tucked 180 mm mouth, and ribs that split and rejoin as smooth ribbons.",
        "",
        "Common dimensions:",
        "- clear inner mouth opening: 180 mm",
        f"- planter height: {BODY_H:.0f} mm",
        f"- pot floor thickness: {FLOOR_T:.0f} mm",
        f"- tray rim height: {TRAY_WALL_H:.0f} mm",
        f"- support mound top height: {SUPPORT_H:.0f} mm, leaving about 5 mm visual gap above the tray rim",
        "- support system: five broad tray mounds under solid floor zones; drain openings sit around the mounds",
        "",
        "| Variation | Ribs | Branching | Note |",
        "|---|---:|---:|---|",
    ]
    for v, _, _ in rows:
        lines.append(f"| {v.name} | {v.ribs} | {v.branch:.2f} | {notes[v.name]} |")
    lines += [
        "",
        "Print notes:",
        "- Print pot and tray upright, no supports.",
        "- Use a normal solid-wall profile, not vase mode.",
        "- Use at least 4 perimeters and enough bottom layers for the 6 mm floor.",
        "- The tray mounds are intentionally broad discs to carry weight safely.",
        "- FDM planters can seep; seal the pot interior if it will hold wet soil directly.",
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
        print(f"{v.name}: pot tris={len(pot.tris)} edges={pot.edge_report()} tray tris={len(tray.tris)} edges={tray.edge_report()}")
    write_readme(rows)


if __name__ == "__main__":
    main()
