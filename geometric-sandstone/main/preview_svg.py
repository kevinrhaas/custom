#!/usr/bin/env python3
"""
Dependency-free preview for the geometric sandstone lamp (no numpy/matplotlib).

Two views (choose with --view):
  side  — front elevation silhouette with strata ledges shaded.  Best for
          seeing the layers stack, merge and blend (default).
  iso   — isometric wireframe: vertical = faceted corner edges, horizontal
          = strata rings.

Reuses StrataProfile so the preview matches the generator parameters exactly.

  python3 preview_svg.py --facets 7 --band-blend 0.4 -o preview.svg
"""
import argparse
import math

from generate_geometric_sandstone import StrataProfile, MEAN_RADIUS, \
    BASELINE_HEIGHT, BASELINE_LAYERS


def build_profile(a):
    return StrataProfile(a.radius, a.strata_amp, a.facet_jitter, a.taper,
                         a.seed, a.strata_bands, a.band_amp, a.band_blend)


def corner_xyz(prof, a, f, k, F, L, tw, height):
    t = k / (L - 1)
    ang = 2 * math.pi * f / F + tw * t
    r = prof.corner_radius(f, t)
    return r * math.cos(ang), r * math.sin(ang), t * height, r, ang


def render_side(prof, a, F, L, tw):
    """Front-elevation silhouette: right/left X-extent of the ring per layer,
    with horizontal strata band boundaries — shows the ledges blending."""
    rights, lefts = [], []
    for k in range(L):
        xs = []
        for f in range(F):
            x, y, z, r, ang = corner_xyz(prof, a, f, k, F, L, tw, a.height)
            xs.append(x)
        z = k / (L - 1) * a.height
        rights.append((max(xs), z))
        lefts.append((min(xs), z))

    minx = min(p[0] for p in lefts)
    maxx = max(p[0] for p in rights)
    pad, sc = 10, 3.0
    w = (maxx - minx) + 2 * pad
    h = a.height + 2 * pad

    def tx(x):
        return (x - minx + pad) * sc

    def ty(z):
        return (h - (z + pad)) * sc        # z up

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*sc:.0f}" '
           f'height="{h*sc:.0f}" viewBox="0 0 {w*sc:.0f} {h*sc:.0f}">',
           '<rect width="100%" height="100%" fill="#f5f1e8"/>']
    # Silhouette polygon (up the right edge, down the left edge)
    pts = [(tx(x), ty(z)) for x, z in rights] + \
          [(tx(x), ty(z)) for x, z in reversed(lefts)]
    poly = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<polygon points="{poly}" fill="#d9b98a" stroke="#7a5a32" '
               f'stroke-width="1.5"/>')
    # Strata band boundaries as horizontal ledge lines across the silhouette
    edges = []
    acc = 0.0
    # reconstruct band edges from centres for drawing
    c = prof.centers
    edges = [0.0] + [(c[i] + c[i + 1]) / 2 for i in range(len(c) - 1)] + [1.0]
    for e in edges:
        z = e * a.height
        # find silhouette extent near this z
        k = min(L - 1, max(0, int(round(e * (L - 1)))))
        lx, rx = lefts[k][0], rights[k][0]
        out.append(f'<line x1="{tx(lx):.1f}" y1="{ty(z):.1f}" '
                   f'x2="{tx(rx):.1f}" y2="{ty(z):.1f}" '
                   f'stroke="#9c7038" stroke-width="0.6" opacity="0.55"/>')
    out.append(f'<text x="6" y="{h*sc-8:.0f}" font-family="monospace" '
               f'font-size="13" fill="#6b6457">geometric-sandstone (side)  '
               f'{a.height:.0f}mm · {F} facets · {a.strata_bands} bands · '
               f'blend {a.band_blend:.2f} · twist {math.degrees(tw):.0f}°</text>')
    out.append('</svg>')
    return "\n".join(out), w * sc, h * sc


def render_iso(prof, a, F, L, tw):
    def cxy(f, k):
        x, y, z, r, ang = corner_xyz(prof, a, f, k, F, L, tw, a.height)
        sx = (x - y) * 0.866
        sy = (x + y) * 0.5 - z
        return sx, sy

    segs = []
    for f in range(F):
        ang0 = 2 * math.pi * f / F
        front = math.cos(ang0) - math.sin(ang0) > 0
        for k in range(L - 1):
            x1, y1 = cxy(f, k)
            x2, y2 = cxy(f, k + 1)
            segs.append((x1, y1, x2, y2,
                         "#3a342c" if front else "#b9ad97",
                         1.1 if front else 0.7))
    for k in range(0, L, max(1, a.ring_every)):
        pts = [cxy(f, k) for f in range(F)] + [cxy(0, k)]
        for i in range(len(pts) - 1):
            segs.append((*pts[i], *pts[i + 1], "#c98a3c", 0.6))

    xs = [s[0] for s in segs] + [s[2] for s in segs]
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    pad, sc = 12, 4.0
    w = (maxx - minx) + 2 * pad
    h = (maxy - miny) + 2 * pad

    def tx(x):
        return (x - minx + pad) * sc

    def ty(y):
        return (y - miny + pad) * sc

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*sc:.0f}" '
           f'height="{h*sc:.0f}" viewBox="0 0 {w*sc:.0f} {h*sc:.0f}">',
           '<rect width="100%" height="100%" fill="#f5f1e8"/>']
    for x1, y1, x2, y2, col, wd in segs:
        out.append(f'<line x1="{tx(x1):.1f}" y1="{ty(y1):.1f}" '
                   f'x2="{tx(x2):.1f}" y2="{ty(y2):.1f}" stroke="{col}" '
                   f'stroke-width="{wd*sc*0.5:.2f}" stroke-linecap="round"/>')
    out.append('</svg>')
    return "\n".join(out), w * sc, h * sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--view", choices=["side", "iso"], default="side")
    ap.add_argument("--height", type=float, default=BASELINE_HEIGHT)
    ap.add_argument("--layers", type=int, default=BASELINE_LAYERS)
    ap.add_argument("--facets", type=int, default=7)
    ap.add_argument("--radius", type=float, default=MEAN_RADIUS)
    ap.add_argument("--strata-bands", type=int, default=22)
    ap.add_argument("--band-amp", type=float, default=0.07)
    ap.add_argument("--band-blend", type=float, default=0.4)
    ap.add_argument("--strata-amp", type=float, default=0.05)
    ap.add_argument("--facet-jitter", type=float, default=0.05)
    ap.add_argument("--taper", type=float, default=0.0)
    ap.add_argument("--twist", type=float, default=12.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ring-every", type=int, default=6)
    ap.add_argument("-o", "--output", default="preview.svg")
    a = ap.parse_args()

    prof = build_profile(a)
    F, L, tw = max(3, a.facets), max(2, a.layers), math.radians(a.twist)
    svg = (render_side if a.view == "side" else render_iso)(prof, a, F, L, tw)[0]
    with open(a.output, 'w') as fp:
        fp.write(svg)
    print(f"✓ preview ({a.view}): {a.output}")


if __name__ == "__main__":
    main()
