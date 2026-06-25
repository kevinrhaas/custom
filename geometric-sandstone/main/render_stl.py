#!/usr/bin/env python3
"""
Dependency-free shaded render of a binary STL to SVG (painter's algorithm).

Gives a solid, lit preview of the lamp — far more faithful than the wireframe
schematics — so angular shelves, printable overhangs, irregular sides and
merging/splitting strata are all visible.  Render to PNG with headless Chromium.

  python3 render_stl.py lamp.stl -o lamp.svg --az 25 --el 62
"""
import argparse
import math
import struct


def read_stl(path):
    with open(path, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        tris = []
        for _ in range(n):
            f.read(12)
            vs = [struct.unpack("<3f", f.read(12)) for _ in range(3)]
            f.read(2)
            tris.append(vs)
    return tris


def rotate(p, az, el):
    ca, sa = math.cos(az), math.sin(az)
    x, y, z = p
    x, y = x * ca - y * sa, x * sa + y * ca      # spin about Z
    ce, se = math.cos(el), math.sin(el)
    y, z = y * ce - z * se, y * se + z * ce       # tilt about X
    return (x, y, z)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stl")
    ap.add_argument("-o", "--output", default="render.svg")
    ap.add_argument("--az", type=float, default=25.0, help="azimuth deg")
    ap.add_argument("--el", type=float, default=62.0, help="elevation deg")
    ap.add_argument("--width", type=int, default=520)
    ap.add_argument("--color", default="#c9a36a", help="base stone colour")
    ap.add_argument("--bg", default="#f0ece3")
    a = ap.parse_args()

    az, el = math.radians(a.az), math.radians(90 - a.el)
    tris = read_stl(a.stl)

    # Light in view space (upper-left-front), screen: +x right, +z up, +y depth.
    L = (-0.35, -0.45, 0.82)
    Ln = math.sqrt(sum(c * c for c in L))
    L = tuple(c / Ln for c in L)
    br = int(a.color[1:3], 16), int(a.color[3:5], 16), int(a.color[5:7], 16)

    faces = []
    for vs in tris:
        rv = [rotate(p, az, el) for p in vs]
        # view normal
        u = tuple(rv[1][i] - rv[0][i] for i in range(3))
        w = tuple(rv[2][i] - rv[0][i] for i in range(3))
        n = (u[1] * w[2] - u[2] * w[1],
             u[2] * w[0] - u[0] * w[2],
             u[0] * w[1] - u[1] * w[0])
        nl = math.sqrt(sum(c * c for c in n))
        if nl < 1e-12:
            continue
        n = tuple(c / nl for c in n)
        if n[1] < 0:                      # back-face cull (camera looks +Y)
            continue
        ndl = max(0.0, sum(n[i] * L[i] for i in range(3)))
        shade = 0.45 + 0.55 * ndl
        depth = sum(p[1] for p in rv) / 3.0
        poly = [(p[0], p[2]) for p in rv]    # (x -> screen x, z -> screen y up)
        faces.append((depth, shade, poly))

    faces.sort(key=lambda t: t[0])           # far first

    xs = [p[0] for _, _, poly in faces for p in poly]
    ys = [p[1] for _, _, poly in faces for p in poly]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    pad = 14
    sc = (a.width - 2 * pad) / (maxx - minx)
    H = (maxy - miny) * sc + 2 * pad
    tx = lambda x: (x - minx) * sc + pad
    ty = lambda y: H - ((y - miny) * sc + pad)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{a.width}" '
           f'height="{H:.0f}" viewBox="0 0 {a.width} {H:.0f}">',
           f'<rect width="100%" height="100%" fill="{a.bg}"/>']
    for _, shade, poly in faces:
        r = int(br[0] * shade); g = int(br[1] * shade); b = int(br[2] * shade)
        pts = " ".join(f"{tx(x):.1f},{ty(y):.1f}" for x, y in poly)
        col = f"#{r:02x}{g:02x}{b:02x}"
        out.append(f'<polygon points="{pts}" fill="{col}" stroke="{col}" '
                   f'stroke-width="0.4"/>')
    out.append('</svg>')
    with open(a.output, "w") as f:
        f.write("\n".join(out))
    print(f"✓ render: {a.output}  ({len(faces)} faces)")


if __name__ == "__main__":
    main()
