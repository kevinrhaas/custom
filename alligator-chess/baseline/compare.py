#!/usr/bin/env python3
"""Measure a render against the reference numbers in reference.py.

Renders the piece at the reference camera, extracts the silhouette, normalises
it against its own bounding box and reports the per-height error against
``reference.SILHOUETTE``. Also writes an overlay PNG: the render in grey with
the reference outline drawn over it, so a human (or a critic) can see exactly
where it drifts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

import reference
import render as renderer

HERE = Path(__file__).parent


def silhouette_mask(img: np.ndarray) -> np.ndarray:
    """Piece pixels: anything meaningfully greener/darker than the backdrop."""
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return (g.astype(int) - b.astype(int) > 12) & (r < 220)


def profile(mask: np.ndarray, heights) -> tuple[list, tuple]:
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    y0, y1 = rows.min(), rows.max()
    x0, x1 = cols.min(), cols.max()
    h, w = y1 - y0, x1 - x0

    out = []
    for v in heights:
        row = int(round(y0 + v * h))
        row = min(max(row, y0), y1)
        xs = np.where(mask[row])[0]
        if len(xs) == 0:
            out.append((v, None, None))
        else:
            out.append((v, (xs.min() - x0) / w, (xs.max() - x0) / w))
    return out, (x0, y0, w, h)


def measure(mesh, out_png: Path | None = None, size: int = 1232) -> dict:
    tmp = HERE / "preview" / "_compare.png"
    tmp.parent.mkdir(exist_ok=True)
    renderer.render(mesh, tmp, size=size, **reference.CAMERA)
    img = np.asarray(Image.open(tmp).convert("RGB"))
    mask = silhouette_mask(img)

    heights = [v for v, _, _ in reference.SILHOUETTE]
    got, box = profile(mask, heights)

    rows = []
    worst = 0.0
    for (v, ul, ur), (_, rl, rr) in zip(got, reference.SILHOUETTE):
        if ul is None:
            rows.append((v, None, None, None, None))
            continue
        el, er = ul - rl, ur - rr
        worst = max(worst, abs(el), abs(er))
        rows.append((v, ul, ur, el, er))

    if out_png is not None:
        _overlay(img, box, out_png)

    inside = [r for r in rows if r[3] is not None
              and abs(r[3]) <= reference.TOLERANCE and abs(r[4]) <= reference.TOLERANCE]
    return {
        "rows": rows,
        "worst_abs_error": worst,
        "within_tolerance": len(inside),
        "checked": len(rows),
        "tolerance": reference.TOLERANCE,
        "aspect": box[2] / box[3],
        "reference_aspect": reference.ASPECT,
    }


def _overlay(img: np.ndarray, box, path: Path) -> None:
    x0, y0, w, h = box
    out = (img.astype(float) * 0.55 + 255 * 0.45).astype(np.uint8)
    canvas = Image.fromarray(out)
    px = canvas.load()
    for v, ul, ur in reference.SILHOUETTE:
        yy = int(round(y0 + v * h))
        for u, colour in ((ul, (200, 40, 40)), (ur, (200, 40, 40))):
            xx = int(round(x0 + u * w))
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    if 0 <= xx + dx < canvas.width and 0 <= yy + dy < canvas.height:
                        px[xx + dx, yy + dy] = colour
    canvas.save(path)


def main() -> None:
    import knight

    mesh = knight.build()
    result = measure(mesh, HERE / "preview" / "overlay.png")
    print(f"{'v':>7} {'left':>8} {'right':>8} {'dL':>8} {'dR':>8}")
    for v, ul, ur, el, er in result["rows"]:
        if ul is None:
            print(f"{v:7.3f}  (empty row)")
            continue
        flag = "  <-- " if max(abs(el), abs(er)) > reference.TOLERANCE else ""
        print(f"{v:7.3f} {ul:8.3f} {ur:8.3f} {el:+8.3f} {er:+8.3f}{flag}")
    print(f"\nwithin tolerance: {result['within_tolerance']}/{result['checked']}"
          f"  (tol {result['tolerance']})")
    print(f"worst error: {result['worst_abs_error']:.3f}")
    print(f"aspect {result['aspect']:.4f} vs reference {result['reference_aspect']:.4f}")
    return 0 if result["within_tolerance"] == result["checked"] else 1


if __name__ == "__main__":
    sys.exit(main())
