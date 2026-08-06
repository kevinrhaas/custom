#!/usr/bin/env python3
"""Measure a render against the reference numbers in reference.py.

Renders the piece at the reference camera, extracts the silhouette, normalises
it against its own bounding box and reports the per-height error against
``reference.SILHOUETTE``. Also writes an overlay PNG: the render in grey with
the reference outline drawn over it, so a human (or a critic) can see exactly
where it drifts.
"""

from __future__ import annotations

import math
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
        "absolute": absolute_scale(mesh),
        "landmarks": landmark_report(mask, box),
    }


def absolute_scale(mesh) -> dict:
    """Reach and span in millimetres — what the normalised table cannot see.

    ``profile`` normalises u against the render's own bounding box, so a muzzle
    that is uniformly too long simply rescales the u axis and every error
    cancels. That blind spot has to be closed separately: measure the projected
    silhouette in real units and compare it against the reference's own.
    """
    yaw = math.radians(reference.CAMERA["yaw"])
    v = np.asarray(mesh.vertices, float)
    image_x = -v[:, 0] * math.sin(yaw) + v[:, 1] * math.cos(yaw)
    left, right = float(image_x.min()), float(image_x.max())
    height = float(mesh.bounds[1][2] - mesh.bounds[0][2])
    return {
        "muzzle_reach_mm": round(-left, 2),
        "plinth_reach_mm": round(right, 2),
        "span_mm": round(right - left, 2),
        "reach_in_plinth_radii": round(-left / right, 3),
        "height_mm": round(height, 2),
        "reference_span_mm": reference.SPAN_MM,
        "reference_reach_in_plinth_radii": reference.REACH_IN_PLINTH_RADII,
        "reference_height_mm": reference.HEIGHT_MM,
    }


def mane_landmarks(mask: np.ndarray, box) -> list[float]:
    """The v of each mane tooth tip, found as local maxima of the right edge.

    `reference.LANDMARKS` was dead code: nothing read it, so the mane could
    drift out of pitch while all twenty outline rows still passed — the rows
    are sampled at fixed heights and simply miss where the tips land.
    """
    x0, y0, w, h = box
    edge = []
    for row in range(y0, y0 + h + 1):
        xs = np.where(mask[row])[0]
        edge.append((xs.max() - x0) / w if len(xs) else -1.0)
    edge = np.array(edge)

    peaks = []
    span = max(3, h // 60)
    for i in range(span, len(edge) - span):
        if edge[i] <= 0:
            continue
        if edge[i] >= edge[i - span:i + span + 1].max() and edge[i] > 0.85:
            peaks.append(i)
    # collapse runs of adjacent rows into one tip each
    tips, run = [], [peaks[0]] if peaks else []
    for i in peaks[1:]:
        if i - run[-1] <= span:
            run.append(i)
        else:
            tips.append(sum(run) / len(run))
            run = [i]
    if run:
        tips.append(sum(run) / len(run))
    return [t / h for t in tips if 0.03 < t / h < 0.62]


def landmark_report(mask: np.ndarray, box) -> list[tuple]:
    got = mane_landmarks(mask, box)
    want = [(k, v) for k, (u, v) in sorted(reference.LANDMARKS.items(),
                                           key=lambda kv: kv[1][1])
            if k.startswith("mane_tooth")]
    rows = []
    for (name, v_ref), v_got in zip(want, got + [None] * len(want)):
        rows.append((name, v_ref, v_got,
                     None if v_got is None else v_got - v_ref))
    return rows


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
          f"  (tol {result['tolerance']} of width = "
          f"{reference.TOLERANCE_AS_HEIGHT_FRACTION:.3f} of height)")
    print(f"worst error: {result['worst_abs_error']:.3f} of width"
          f" = {result['worst_abs_error'] * result['aspect']:.3f} of height"
          f"  (the prose allows 0.025 of height)")
    print(f"aspect {result['aspect']:.4f} vs reference {result['reference_aspect']:.4f}")
    print("\nabsolute scale (mm, projected at the reference camera):")
    a = result["absolute"]
    print(f"  span            {a['span_mm']:6.2f}  vs reference {a['reference_span_mm']:.2f}")
    print(f"  height          {a['height_mm']:6.2f}  vs reference {a['reference_height_mm']:.2f}")
    print(f"  muzzle reach    {a['reach_in_plinth_radii']:6.3f}  vs reference "
          f"{a['reference_reach_in_plinth_radii']:.3f}  plinth-radii")
    print("\nmane tooth tips (v of each tip, from reference.LANDMARKS):")
    bad = 0
    for name, v_ref, v_got, err in result["landmarks"]:
        if v_got is None:
            print(f"  {name:14s}  {v_ref:.3f}  NOT FOUND"); bad += 1; continue
        flag = "  <-- " if abs(err) > reference.TOLERANCE else ""
        bad += abs(err) > reference.TOLERANCE
        print(f"  {name:14s}  want {v_ref:.3f}  got {v_got:.3f}  {err:+.3f}{flag}")
    print(f"  {len(result['landmarks']) - bad}/{len(result['landmarks'])} within tolerance")
    return 0 if result["within_tolerance"] == result["checked"] else 1


if __name__ == "__main__":
    sys.exit(main())
