#!/usr/bin/env python3
"""
Dependency-free isometric wireframe preview for the geometric sandstone lamp.

Reuses StrataProfile so the preview matches whatever parameters you would
pass to the generator.  Emits an .svg (no numpy/matplotlib needed) showing the
faceted strata: vertical corner edges + sampled ring outlines.

  python3 preview_svg.py --facets 10 --strata-amp 0.10 --facet-jitter 0.05 \
                         -o preview.svg
"""
import argparse
import math

from generate_geometric_sandstone import StrataProfile, MEAN_RADIUS, \
    BASELINE_HEIGHT, BASELINE_LAYERS


def iso(x, y, z):
    """Isometric projection -> (sx, sy) with screen-y pointing down."""
    sx = (x - y) * 0.866
    sy = (x + y) * 0.5 - z
    return sx, sy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=float, default=BASELINE_HEIGHT)
    ap.add_argument("--layers", type=int, default=BASELINE_LAYERS)
    ap.add_argument("--facets", type=int, default=10)
    ap.add_argument("--radius", type=float, default=MEAN_RADIUS)
    ap.add_argument("--strata-amp", type=float, default=0.10)
    ap.add_argument("--facet-jitter", type=float, default=0.05)
    ap.add_argument("--taper", type=float, default=0.0)
    ap.add_argument("--twist", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ring-every", type=int, default=6,
                    help="Draw a ring outline every N layers")
    ap.add_argument("-o", "--output", default="preview.svg")
    a = ap.parse_args()

    prof = StrataProfile(a.radius, a.strata_amp, a.facet_jitter, a.taper, a.seed)
    F, L = max(3, a.facets), max(2, a.layers)
    tw = math.radians(a.twist)

    def corner(f, k):
        t = k / (L - 1)
        ang = 2 * math.pi * f / F + tw * t
        r = prof.corner_radius(f, t)
        return iso(r * math.cos(ang), r * math.sin(ang), t * a.height)

    # Collect geometry + bounds
    segs = []  # (x1,y1,x2,y2, stroke, width)
    # Vertical corner edges — these are the jagged straight wall lines
    for f in range(F):
        ang0 = 2 * math.pi * f / F
        # front-ish facets (facing the viewer, +x/-y) drawn darker
        front = math.cos(ang0) - math.sin(ang0) > 0
        for k in range(L - 1):
            x1, y1 = corner(f, k)
            x2, y2 = corner(f, k + 1)
            segs.append((x1, y1, x2, y2,
                         "#3a342c" if front else "#b9ad97",
                         1.1 if front else 0.7))
    # Sampled ring outlines — the strata
    for k in range(0, L, max(1, a.ring_every)):
        pts = [corner(f, k) for f in range(F)] + [corner(0, k)]
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            segs.append((x1, y1, x2, y2, "#c98a3c", 0.6))

    xs = [s[0] for s in segs] + [s[2] for s in segs]
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    pad = 12
    w = (maxx - minx) + 2 * pad
    h = (maxy - miny) + 2 * pad
    sc = 4.0  # upscale for crisp viewing

    def tx(x):
        return (x - minx + pad) * sc

    def ty(y):
        return (y - miny + pad) * sc

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*sc:.0f}" '
           f'height="{h*sc:.0f}" viewBox="0 0 {w*sc:.0f} {h*sc:.0f}">',
           f'<rect width="100%" height="100%" fill="#f5f1e8"/>']
    for x1, y1, x2, y2, col, wd in segs:
        out.append(f'<line x1="{tx(x1):.1f}" y1="{ty(y1):.1f}" '
                   f'x2="{tx(x2):.1f}" y2="{ty(y2):.1f}" '
                   f'stroke="{col}" stroke-width="{wd*sc*0.5:.2f}" '
                   f'stroke-linecap="round"/>')
    out.append(f'<text x="{8}" y="{h*sc-10:.0f}" font-family="monospace" '
               f'font-size="{14}" fill="#6b6457">geometric-sandstone  '
               f'{a.height:.0f}mm · {F} facets · strata±{a.strata_amp*100:.0f}%'
               f' · jitter±{a.facet_jitter*100:.0f}%</text>')
    out.append('</svg>')
    with open(a.output, 'w') as fp:
        fp.write("\n".join(out))
    print(f"✓ preview: {a.output}")


if __name__ == "__main__":
    main()
