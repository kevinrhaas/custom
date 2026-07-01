#!/usr/bin/env python3
"""
Preview generator — writes a small SVG per variant so you can compare the
family at a glance (flute count/depth from the top, proportions from the side)
without opening a slicer. Pure Python, no dependencies.
"""
import math
import os
from generate_bamboo_vase import VARIANTS, BUNCH_DIA

WALL = 2.8
FLOOR = 4.0

BG = "#f4f2ec"
INK = "#2f3b32"
BODY = "#3a4a3f"
BODY2 = "#4b5f51"
BEAD = "#cfe3d6"
BUNCH = "#7bb661"
WATER = "#dfeee6"


def belly_z(z, h, belly):
    return belly * math.sin(math.pi * (z / h))


def top_view(cx, cy, scale, dia, n, amp, belly):
    inner_r = dia / 2.0
    # exterior crest outline at mid-height (belly at max)
    pts = []
    N = 720
    for i in range(N + 1):
        th = 2 * math.pi * i / N
        r = inner_r + WALL + belly + amp * (0.5 + 0.5 * math.cos(n * th))
        pts.append((cx + scale * r * math.cos(th), cy + scale * r * math.sin(th)))
    path = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
    s = []
    s.append(f'<path d="{path}" fill="{BODY}" stroke="{INK}" stroke-width="1.2"/>')
    # interior circle + water/bead annulus
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{scale*inner_r:.2f}" fill="{BEAD}" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{scale*BUNCH_DIA/2:.2f}" fill="{BUNCH}" stroke="{INK}" stroke-width="0.8"/>')
    return "\n".join(s)


def side_view(cx, top, scale, dia, h, amp, belly):
    inner_r = dia / 2.0
    # crest & valley silhouettes vs z
    crest_r = lambda z: inner_r + WALL + belly_z(z, h, belly) + amp
    valley_r = lambda z: inner_r + WALL + belly_z(z, h, belly)
    N = 60
    left = []
    right = []
    for i in range(N + 1):
        z = h * i / N
        y = top + scale * (h - z)
        left.append((cx - scale * crest_r(z), y))
        right.append((cx + scale * crest_r(z), y))
    outline = [(cx - scale * crest_r(0), top + scale * h)]  # bottom-left
    outline += left[::-1]  # up left side
    outline += right       # down right side
    path = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in outline) + " Z"
    s = []
    s.append(f'<path d="{path}" fill="{BODY2}" stroke="{INK}" stroke-width="1.2"/>')
    # interior cavity (dashed) — water/bead well from the floor to the rim
    s.append(f'<rect x="{cx-scale*inner_r:.2f}" y="{top:.2f}" width="{2*scale*inner_r:.2f}" '
             f'height="{scale*(h-FLOOR):.2f}" fill="{WATER}" fill-opacity="0.55" '
             f'stroke="{INK}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    return "\n".join(s)


def make_svg(name, dia, h, n, amp, belly):
    W, H = 460, 360
    scale = 1.7
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    parts.append(f'<text x="20" y="30" font-family="Helvetica,Arial" font-size="20" '
                 f'font-weight="700" fill="{INK}">{name}</text>')
    outer_dia = dia + 2 * (WALL + belly + amp)
    parts.append(f'<text x="20" y="50" font-family="Helvetica,Arial" font-size="12" fill="{INK}">'
                 f'{n} waves &#183; {amp:.1f}mm depth &#183; H {h:.0f}mm &#183; &#8960;{outer_dia:.0f}mm'
                 f' &#183; interior &#8960;{dia:.0f}mm</text>')
    # top view (left)
    parts.append(top_view(140, 210, scale, dia, n, amp, belly))
    parts.append(f'<text x="140" y="330" font-family="Helvetica,Arial" font-size="11" '
                 f'fill="{INK}" text-anchor="middle">top &#8212; flutes + beads (green = bunch)</text>')
    # side view (right)
    parts.append(side_view(345, 95, scale, dia, h, amp, belly))
    parts.append(f'<text x="345" y="330" font-family="Helvetica,Arial" font-size="11" '
                 f'fill="{INK}" text-anchor="middle">side &#8212; dashed = water/bead cavity</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "img", "previews")
    os.makedirs(out, exist_ok=True)
    for name, dia, h, n, amp, belly in VARIANTS:
        svg = make_svg(name, dia, h, n, amp, belly)
        with open(os.path.join(out, f"{name}.svg"), "w") as f:
            f.write(svg)
        print("wrote", os.path.join("img", "previews", f"{name}.svg"))


if __name__ == "__main__":
    main()
