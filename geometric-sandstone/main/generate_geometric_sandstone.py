#!/usr/bin/env python3
"""
Parametric Geometric Sandstone Lamp Generator
=============================================
A geometric cousin of the Ordovician sandstone lamp.  Same idea — strata
layers stacked up a roughly cylindrical body whose radius swells and pinches
to give an organic "sandstone motion" — but rendered with STRAIGHT, JAGGED
walls instead of smooth curves.

How it differs from ordovician-sandstone/generate_sandstone.py
--------------------------------------------------------------
  * The original parses a hand-sculpted polyhedron and interpolates between
    its 120-point smooth rings.  This generator is fully PROCEDURAL — the
    strata "motion" comes from layered sine waves + value noise, so no source
    mesh is needed.
  * Each layer's cross-section is a FACETED POLYGON (default 10 sides) drawn
    with straight chords.  Walls are flat panels meeting at sharp corners.
    Per-corner jitter that drifts up the height makes the angles jagged and
    irregular while still following the overall strata flow.

Geometry / manifold strategy mirrors the proven sandstone hollow build:
  outer faceted shell + inner faceted shell (offset inward) + solid base disc
  with a clean cylindrical centre hole.  Every ring shares the same point
  count and angular ordering, so the mesh stitches 1:1 with no T-junctions.

The flat facets are kept truly planar even though the cap/hole rings are
high resolution: each ring has facets*subdiv points, and the points between
two corners are linearly interpolated ALONG the straight corner-to-corner
chord.  That gives crisp flat walls AND smooth round holes/caps at once.

Usage examples:
  # Default — 150mm, 10 facets, fits the standard base (wall2, base9.46, hole66)
  python3 generate_geometric_sandstone.py

  # Chunkier crystal (7 facets) and a taller lamp
  python3 generate_geometric_sandstone.py --facets 7 --height 180

  # More jagged / irregular angles
  python3 generate_geometric_sandstone.py --facet-jitter 0.10 --strata-amp 0.14

  # Spiral the facets up the height for diagonal ridges
  python3 generate_geometric_sandstone.py --twist 25

  # Different random rock — change the seed
  python3 generate_geometric_sandstone.py --seed 7

  # Solid (no bore) display object
  python3 generate_geometric_sandstone.py --solid
"""

import argparse
import math
import os
import struct

# ── Constants ────────────────────────────────────────────────────────────────
BASELINE_HEIGHT = 150.0   # mm – default lamp height
BASELINE_LAYERS = 139     # strata-layer density that matches the 150mm sandstone
MEAN_RADIUS = 45.0        # mm – mean exterior radius (≈90mm dia, matches original)


# ── Deterministic value noise ────────────────────────────────────────────────

def _smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


class ValueNoise1D:
    """Tiny seeded 1-D value-noise: random values on integer nodes, smoothly
    interpolated.  Deterministic for a given seed so results are reproducible.
    """

    def __init__(self, seed, size=512):
        self.size = size
        # Simple LCG so we don't depend on Python's RNG internals
        state = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        vals = []
        for _ in range(size):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            vals.append(state / 0x7FFFFFFF * 2.0 - 1.0)  # [-1, 1]
        self.vals = vals

    def at(self, x):
        x0 = math.floor(x)
        frac = x - x0
        a = self.vals[int(x0) % self.size]
        b = self.vals[int(x0 + 1) % self.size]
        return a + (b - a) * _smoothstep(frac)


# ── Procedural strata profile ────────────────────────────────────────────────

def _lcg_list(seed, count, lo=-1.0, hi=1.0):
    """Deterministic list of `count` values in [lo, hi] from a tiny LCG."""
    state = (seed * 1103515245 + 12345) & 0x7FFFFFFF
    out = []
    for _ in range(count):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        out.append(lo + (hi - lo) * (state / 0x7FFFFFFF))
    return out


class StrataProfile:
    """Computes the exterior radius of a facet corner at a given height and
    facet index.

    Three layered ingredients, matching the look of the original sandstone:
      1. discrete strata BANDS  — stacked shelves with their own radius, the
         dominant sedimentary look.  `band_blend` controls how sharply each
         ledge cuts vs. how much neighbouring layers MERGE and blend.
      2. a smooth strata 'motion' — gentle sine swell/pinch over the bands.
      3. per-corner jitter        — the jagged, irregular angles.
    """

    def __init__(self, mean_radius, strata_amp, facet_jitter, taper, seed,
                 strata_bands=22, band_amp=0.07, band_blend=0.4):
        self.R0 = mean_radius
        self.strata_amp = strata_amp
        self.facet_jitter = facet_jitter
        self.taper = taper
        self.band_amp = band_amp
        self.band_blend = max(1e-3, min(1.0, band_blend))
        # Independent noise channels
        self.n_strata = ValueNoise1D(seed * 7 + 1)
        self.n_corner = ValueNoise1D(seed * 13 + 5)
        # Randomised but seed-stable phases for the sine bands
        nseed = ValueNoise1D(seed * 101 + 3)
        self.p1 = nseed.at(0.5) * math.pi
        self.p2 = nseed.at(1.5) * math.pi
        self.p3 = nseed.at(2.5) * math.pi

        # ── Build the stacked strata bands ──
        B = max(2, strata_bands)
        # Uneven band thicknesses -> natural, irregular layering
        thick = [1.0 + 0.6 * v for v in _lcg_list(seed * 17 + 2, B, -1, 1)]
        total = sum(thick)
        edges = [0.0]
        for th in thick:
            edges.append(edges[-1] + th / total)        # 0 .. 1
        self.centers = [(edges[i] + edges[i + 1]) / 2 for i in range(B)]
        self.offs = _lcg_list(seed * 29 + 4, B, -1, 1)   # per-band shelf radius
        self.B = B

    def band(self, t):
        """Stacked-shelf strata value in [-1, 1].

        Each band is a near-flat shelf at its own radius; between band centres
        the value transitions.  `band_blend`→0 makes hard ledges (distinct
        layers); →1 makes the layers merge/blend smoothly.
        """
        c = self.centers
        if t <= c[0]:
            return self.offs[0]
        if t >= c[-1]:
            return self.offs[-1]
        # find the bracketing band centres
        i = 0
        while i < self.B - 1 and not (c[i] <= t <= c[i + 1]):
            i += 1
        u = (t - c[i]) / (c[i + 1] - c[i])               # 0..1 between centres
        h = self.band_blend * 0.5
        # Flat shelves with a transition of width ~band_blend around u=0.5
        w = max(0.0, min(1.0, (u - (0.5 - h)) / (2 * h)))
        return self.offs[i] + (self.offs[i + 1] - self.offs[i]) * _smoothstep(w)

    def strata(self, t):
        """Smooth global swell/pinch in [-1, 1] layered over the bands."""
        s = (0.55 * math.sin(2 * math.pi * 3.5 * t + self.p1)
             + 0.30 * math.sin(2 * math.pi * 7.0 * t + self.p2)
             + 0.15 * math.sin(2 * math.pi * 13.0 * t + self.p3))
        s += 0.35 * self.n_strata.at(t * 9.0)
        return max(-1.0, min(1.0, s))

    def corner_radius(self, facet, t):
        """Exterior radius (mm) of corner *facet* at height fraction *t*."""
        rel = (self.band_amp * self.band(t)
               + self.strata_amp * self.strata(t))
        base = self.R0 * (1.0 + rel)
        # Per-corner jitter drifts slowly up the height -> jagged but flowing
        jit = self.n_corner.at(facet * 4.7 + t * 6.0)
        base += self.R0 * self.facet_jitter * jit
        base *= (1.0 - self.taper * t)
        return base


# ── Ring (faceted cross-section) generation ──────────────────────────────────

def make_ring(profile, facets, subdiv, t, height, twist_rad):
    """Build one faceted ring as facets*subdiv points on straight chords.

    Corner f sits at angle (2π f / facets + twist*t) and radius from the
    strata profile.  Points between corner f and f+1 are linearly interpolated
    along the straight chord, so each facet edge is perfectly flat.
    """
    z = t * height
    # Corner positions for this layer
    corners = []
    for f in range(facets):
        ang = 2 * math.pi * f / facets + twist_rad * t
        r = profile.corner_radius(f, t)
        corners.append((r * math.cos(ang), r * math.sin(ang)))

    ring = []
    for f in range(facets):
        c0 = corners[f]
        c1 = corners[(f + 1) % facets]
        for s in range(subdiv):
            u = s / subdiv
            x = c0[0] + (c1[0] - c0[0]) * u
            y = c0[1] + (c1[1] - c0[1]) * u
            ring.append((x, y, z))
    return ring


def offset_ring_inward(ring, wall):
    """Offset every point toward the Z axis by *wall* (radial)."""
    out = []
    for (x, y, z) in ring:
        d = math.hypot(x, y)
        if d < 1e-9:
            out.append((x, y, z))
        else:
            out.append((x - x / d * wall, y - y / d * wall, z))
    return out


def hole_ring_matched(reference_ring, hole_radius, z):
    """Hole ring with one point per reference point, on the same radial line.
    Guarantees a clean 1:1 stitch with no degenerate triangles."""
    ring = []
    for (x, y, _) in reference_ring:
        a = math.atan2(y, x)
        ring.append((hole_radius * math.cos(a), hole_radius * math.sin(a), z))
    return ring


# ── Mesh assembly ────────────────────────────────────────────────────────────

def avg_z(ring):
    return sum(p[2] for p in ring) / len(ring)


def build_solid_mesh(rings, height):
    """Solid faceted body: side quads + bottom fan + top fan."""
    P = len(rings[0])
    pts = []
    for r in rings:
        pts.extend(r)
    faces = []
    N = len(rings)
    for i in range(N - 1):
        for j in range(P):
            jn = (j + 1) % P
            a, b = i * P + j, i * P + jn
            c, d = (i + 1) * P + jn, (i + 1) * P + j
            faces.append([a, b, c])
            faces.append([a, c, d])
    # Bottom fan (z=0)
    cb = len(pts); pts.append((0.0, 0.0, 0.0))
    for j in range(P):
        jn = (j + 1) % P
        faces.append([cb, jn, j])
    # Top fan (z=H)
    ct = len(pts); pts.append((0.0, 0.0, height))
    last = (N - 1) * P
    for j in range(P):
        jn = (j + 1) % P
        faces.append([ct, last + j, last + jn])
    return pts, faces


def build_hollow_mesh(outer_rings, height, wall, solid_base, hole_d):
    """Hollow faceted lamp: outer shell, inner shell (above the solid base),
    solid base disc with a clean cylindrical centre hole, open top.

    Mirrors the manifold strategy of the sandstone generator's hollow build.
    """
    P = len(outer_rings[0])
    N = len(outer_rings)
    hole_r = hole_d / 2.0 if hole_d > 0 else 0.0

    # Which outer ring is the first at/above the solid base height
    floor_idx = 0
    if solid_base > 0:
        for idx in range(N):
            if avg_z(outer_rings[idx]) >= solid_base - 1e-6:
                floor_idx = idx
                break

    # Inner rings (offset inward), only from the floor up.
    inner_source = outer_rings[floor_idx:]
    inner_rings = [offset_ring_inward(r, wall) for r in inner_source]
    if solid_base > 0 and inner_rings:
        inner_rings[0] = [(x, y, solid_base) for (x, y, _) in inner_rings[0]]
    M = len(inner_rings)

    # ── Flatten points: outer rings, then inner rings ──
    pts = []
    for r in outer_rings:
        pts.extend(r)
    outer_count = len(pts)
    for r in inner_rings:
        pts.extend(r)

    faces = []

    # 1. Outer side quads (outward)
    for i in range(N - 1):
        for j in range(P):
            jn = (j + 1) % P
            a, b = i * P + j, i * P + jn
            c, d = (i + 1) * P + jn, (i + 1) * P + j
            faces.append([a, b, c])
            faces.append([a, c, d])

    # 2. Inner side quads (inward = reversed winding)
    for i in range(M - 1):
        for j in range(P):
            jn = (j + 1) % P
            a = outer_count + i * P + j
            b = outer_count + i * P + jn
            c = outer_count + (i + 1) * P + jn
            d = outer_count + (i + 1) * P + j
            faces.append([a, c, b])
            faces.append([a, d, c])

    # 3. Bottom closure + solid base
    if solid_base > 0:
        outer_ring0 = pts[0:P]
        # Bottom annulus: outer ring0 (z=0) -> hole ring (z=0), downward
        hole_bot = hole_ring_matched(outer_ring0, hole_r, 0.0)
        hb = len(pts); pts.extend(hole_bot)
        for j in range(P):
            jn = (j + 1) % P
            faces.append([j, hb + j, hb + jn])
            faces.append([j, hb + jn, jn])
        # Inner floor annulus: inner ring0 (z=base) -> hole ring (z=base), up
        hole_floor = hole_ring_matched(outer_ring0, hole_r, solid_base)
        hf = len(pts); pts.extend(hole_floor)
        inner_floor = outer_count
        for j in range(P):
            jn = (j + 1) % P
            faces.append([inner_floor + j, inner_floor + jn, hf + jn])
            faces.append([inner_floor + j, hf + jn, hf + j])
        # Hole tube: z=0 ring -> z=base ring (inward facing)
        for j in range(P):
            jn = (j + 1) % P
            a, b = hb + j, hb + jn
            c, d = hf + jn, hf + j
            faces.append([a, d, c])
            faces.append([a, c, b])
        # No lip: outer wall runs full height to z=0 and the cavity floor
        # annulus (inner -> hole) caps the void, so the radial cross-section
        # closes cleanly without reusing the outer wall's ring edges.
    else:
        # Open tube bottom: annulus outer ring0 <-> inner ring0 at z=0
        for j in range(P):
            jn = (j + 1) % P
            faces.append([j, outer_count + j, outer_count + jn])
            faces.append([j, outer_count + jn, jn])

    # 4. Top annulus (open top): outer last <-> inner last
    to = (N - 1) * P
    ti = outer_count + (M - 1) * P
    for j in range(P):
        jn = (j + 1) % P
        faces.append([to + j, to + jn, ti + jn])
        faces.append([to + j, ti + jn, ti + j])

    return pts, faces


# ── Output: SCAD + binary STL ────────────────────────────────────────────────

def write_scad(path, pts, faces, height, facets, layers):
    with open(path, 'w') as f:
        f.write(f"""\
// ═══════════════════════════════════════════════════════════════════════════
// Parametric Geometric Sandstone Lamp
// ═══════════════════════════════════════════════════════════════════════════
// Generated by generate_geometric_sandstone.py
//   height = {height} mm   facets = {facets}   strata layers = {layers}
//
// Straight, faceted strata walls following a procedural sandstone "motion".
//
/* [Height Fine-Tuning] */
fine_tune_scale = 1.0;  // [0.25:0.01:4.0]

scale([1, 1, fine_tune_scale])
""")
        f.write("polyhedron(\n  points = [\n")
        for i, (x, y, z) in enumerate(pts):
            c = "," if i < len(pts) - 1 else ""
            f.write(f"        [{x:.5f}, {y:.5f}, {z:.5f}]{c}\n")
        f.write("      ],\n      faces = [\n")
        for i, fc in enumerate(faces):
            c = "," if i < len(faces) - 1 else ""
            f.write(f"        [{fc[0]}, {fc[1]}, {fc[2]}]{c}\n")
        f.write("      ],\n      convexity = 10\n    );\n")


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


def _norm(v):
    L = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    return (0.0, 0.0, 0.0) if L < 1e-12 else (v[0] / L, v[1] / L, v[2] / L)


def write_stl(path, pts, faces):
    with open(path, 'wb') as f:
        f.write(b'Binary STL - Geometric Sandstone Lamp'.ljust(80, b'\0'))
        f.write(struct.pack('<I', len(faces)))
        for fc in faces:
            p0, p1, p2 = pts[fc[0]], pts[fc[1]], pts[fc[2]]
            u = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            v = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
            n = _norm(_cross(u, v))
            f.write(struct.pack('<3f', *n))
            f.write(struct.pack('<3f', *p0))
            f.write(struct.pack('<3f', *p1))
            f.write(struct.pack('<3f', *p2))
            f.write(struct.pack('<H', 0))


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Generate a parametric geometric (faceted) sandstone lamp.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--height", type=float, default=BASELINE_HEIGHT,
                    help=f"Target height in mm (default {BASELINE_HEIGHT:.0f})")
    ap.add_argument("--layers", type=int, default=None,
                    help="Strata layer count (default scales with height)")
    ap.add_argument("--facets", type=int, default=7,
                    help="Polygon sides per cross-section (default 7)")
    ap.add_argument("--subdiv", type=int, default=8,
                    help="Mesh points per facet edge — keeps walls flat while "
                         "caps/holes stay round (default 8)")
    ap.add_argument("--radius", type=float, default=MEAN_RADIUS,
                    help=f"Mean exterior radius in mm (default {MEAN_RADIUS:.0f})")
    ap.add_argument("--strata-bands", type=int, default=22,
                    help="Number of stacked sediment bands/shelves (default 22)")
    ap.add_argument("--band-amp", type=float, default=0.07,
                    help="Strata shelf depth, fraction of radius (default 0.07)")
    ap.add_argument("--band-blend", type=float, default=0.4,
                    help="0 = hard ledges (distinct layers), 1 = fully merged/"
                         "blended layers (default 0.4)")
    ap.add_argument("--strata-amp", type=float, default=0.05,
                    help="Smooth swell layered over the bands, fraction of "
                         "radius (default 0.05)")
    ap.add_argument("--facet-jitter", type=float, default=0.05,
                    help="Per-corner jaggedness, fraction of radius (default 0.05)")
    ap.add_argument("--taper", type=float, default=0.0,
                    help="Top narrowing, fraction of radius over full height "
                         "(default 0.0 = straight)")
    ap.add_argument("--twist", type=float, default=12.0,
                    help="Total facet rotation over the height, degrees. "
                         "Combined with --facet-jitter this gives the jagged, "
                         "spiralling strata (default 12; 0 = vertical edges)")
    ap.add_argument("--seed", type=int, default=42,
                    help="Random seed for the procedural rock (default 42)")
    ap.add_argument("--wall", type=float, default=2.0,
                    help="Wall thickness in mm (default 2.0)")
    ap.add_argument("--base", type=float, default=9.46,
                    help="Solid base height in mm (default 9.46)")
    ap.add_argument("--base-hole", type=float, default=66.0,
                    help="Centre hole diameter in mm (default 66.0)")
    ap.add_argument("--solid", action="store_true",
                    help="Solid model (no hollow/base/hole)")
    ap.add_argument("-o", "--output", type=str, default=None,
                    help="Output basename (default auto-generated)")
    args = ap.parse_args()

    height = args.height
    layers = args.layers if args.layers else max(
        2, int(round(BASELINE_LAYERS * height / BASELINE_HEIGHT)))
    facets = max(3, args.facets)
    subdiv = max(1, args.subdiv)
    twist_rad = math.radians(args.twist)

    profile = StrataProfile(args.radius, args.strata_amp, args.facet_jitter,
                            args.taper, args.seed, args.strata_bands,
                            args.band_amp, args.band_blend)

    rings = [make_ring(profile, facets, subdiv, k / (layers - 1), height,
                       twist_rad) for k in range(layers)]

    if args.solid:
        pts, faces = build_solid_mesh(rings, height)
        mode = "SOLID"
    else:
        pts, faces = build_hollow_mesh(rings, height, args.wall,
                                       args.base, args.base_hole)
        mode = "HOLLOW"

    if args.output:
        base = args.output
        for ext in ('.scad', '.stl'):
            if base.lower().endswith(ext):
                base = base[:-len(ext)]
    else:
        tag = f"{height:.0f}mm_{facets}fac_{layers}L"
        if not args.solid:
            tag += f"_wall{args.wall:.0f}_base{args.base:g}_hole{args.base_hole:g}"
        else:
            tag += "_solid"
        base = f"geometric_sandstone_{tag}"

    scad_path, stl_path = base + '.scad', base + '.stl'
    write_scad(scad_path, pts, faces, height, facets, layers)
    write_stl(stl_path, pts, faces)

    stl_mb = os.path.getsize(stl_path) / (1024 * 1024)
    print(f"Geometric Sandstone Lamp  [{mode}]")
    print(f"  Height : {height:.1f} mm   Facets : {facets}   Layers : {layers}")
    print(f"  Mean r : {args.radius:.1f} mm   bands {args.strata_bands}"
          f"(±{args.band_amp*100:.0f}%, blend {args.band_blend:.2f})"
          f"   swell±{args.strata_amp*100:.0f}%"
          f"   jitter±{args.facet_jitter*100:.0f}%   twist {args.twist:.0f}°")
    if not args.solid:
        print(f"  Wall   : {args.wall:.2f} mm   Base : {args.base:.2f} mm"
              f"   Hole : ⌀{args.base_hole:.1f} mm")
    print(f"  Points : {len(pts):,}   Faces : {len(faces):,}")
    print(f"\n✓ SCAD: {scad_path}")
    print(f"✓ STL:  {stl_path}  ({stl_mb:.1f} MB)")


if __name__ == "__main__":
    main()
