#!/usr/bin/env python3
"""Software rasteriser for QA renders — no GPU, no display server.

Flat-shaded facet rendering on a light studio backdrop, deliberately matched
to the reference product photograph: matte olive resin, soft key from the
upper left, cool fill, a soft contact shadow to the lower right.
"""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

BG_TOP = np.array([0.925, 0.925, 0.925])
BG_BOTTOM = np.array([0.878, 0.878, 0.878])
ALBEDO = np.array([0.404, 0.451, 0.333])  # matte olive


def look_at(eye, target, up=(0.0, 0.0, 1.0)):
    eye = np.array(eye, float)
    target = np.array(target, float)
    fwd = target - eye
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, np.array(up, float))
    right /= np.linalg.norm(right)
    true_up = np.cross(right, fwd)
    return eye, np.stack([right, true_up, -fwd])


def render(mesh, path, size=1232, yaw=38.0, elev=9.0, dist=260.0, fov=22.0,
           supersample=3, albedo=ALBEDO, fill=0.843, anchor=(0.497, 0.527)):
    """Render ``mesh`` (Z-up, sitting on Z=0) to a PNG.

    ``fill``/``anchor`` frame the piece the way the reference photograph does:
    the silhouette occupies ``fill`` of the frame height with its bounding box
    centred on ``anchor``. Framing is applied after projection so it never
    disturbs the perspective set by ``dist``/``fov``.
    """
    S = size * supersample
    verts = np.asarray(mesh.vertices, float)
    faces = np.asarray(mesh.faces, int)

    lo, hi = verts.min(axis=0), verts.max(axis=0)
    centre = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2])

    a, e = math.radians(yaw), math.radians(elev)
    eye = centre + dist * np.array([math.cos(e) * math.cos(a),
                                    math.cos(e) * math.sin(a),
                                    math.sin(e)])
    eye, R = look_at(eye, centre)

    f = 1.0 / math.tan(math.radians(fov) / 2.0)

    def project(points):
        cam = (points - eye) @ R.T
        depth = np.maximum(-cam[:, 2], 1e-6)
        return np.stack([cam[:, 0] * f / depth, cam[:, 1] * f / depth, depth], axis=1)

    ndc = project(verts)
    span = ndc[:, 1].max() - ndc[:, 1].min()
    scale = fill * S / max(span, 1e-9)
    ox = S * anchor[0] - scale * (ndc[:, 0].max() + ndc[:, 0].min()) / 2.0
    oy = S * anchor[1] + scale * (ndc[:, 1].max() + ndc[:, 1].min()) / 2.0

    def to_screen(n):
        return np.stack([ox + n[:, 0] * scale, oy - n[:, 1] * scale, n[:, 2]], axis=1)

    screen = to_screen(ndc)

    # ---- background -----------------------------------------------------
    grad = np.linspace(0.0, 1.0, S)[:, None]
    img = (BG_TOP[None, None, :] * (1 - grad[:, :, None])
           + BG_BOTTOM[None, None, :] * grad[:, :, None])
    img = np.repeat(img, S, axis=1).astype(np.float64)

    # ---- contact shadow: project the mesh onto the floor, blur it -------
    floor_dir = np.array([-0.55, -0.62, -1.0])
    floor_dir /= np.linalg.norm(floor_dir)
    t = (verts[:, 2] - lo[2]) / max(1e-6, -floor_dir[2])
    ground = verts + t[:, None] * floor_dir[None, :]
    ground[:, 2] = lo[2]
    gscreen = to_screen(project(ground))
    shadow = np.zeros((S, S))
    _raster_mask(shadow, gscreen[:, :2], faces)
    shadow = _box_blur(shadow, max(3, S // 90), passes=3)
    shadow = np.clip(shadow, 0, 1) * 0.30
    img *= (1.0 - shadow)[:, :, None]

    # ---- lighting -------------------------------------------------------
    tri = verts[faces]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    n = n / np.where(ln < 1e-12, 1.0, ln)

    key = _unit([0.12, 0.52, 0.86])     # high key, just off the camera axis
    fill = _unit([0.86, -0.34, 0.24])   # low fill from the muzzle side
    rim = _unit([-0.72, 0.36, 0.22])    # behind the mane, lifts the crest
    view = _unit(centre - eye)

    lam = (0.92 * np.clip(n @ key, 0, 1)
           + 0.30 * np.clip(n @ fill, 0, 1)
           + 0.26 * np.clip(n @ rim, 0, 1)
           + 0.42)
    half = _unit(key - view)
    spec = 0.07 * np.clip(n @ half, 0, 1) ** 14
    shade = albedo[None, :] * lam[:, None] + spec[:, None]

    colour = np.clip(shade, 0.0, 1.0)
    _raster(img, screen, faces, colour)

    img = np.clip(img, 0, 1) ** (1 / 1.06)
    out = Image.fromarray((img * 255 + 0.5).astype(np.uint8))
    out = out.resize((size, size), Image.LANCZOS)
    out.save(path)
    return path


def _unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def _bbox(pts, S):
    x0 = max(int(np.floor(pts[:, 0].min())), 0)
    x1 = min(int(np.ceil(pts[:, 0].max())) + 1, S)
    y0 = max(int(np.floor(pts[:, 1].min())), 0)
    y1 = min(int(np.ceil(pts[:, 1].max())) + 1, S)
    return x0, x1, y0, y1


def _raster(img, screen, faces, colour):
    S = img.shape[0]
    zbuf = np.full((S, S), np.inf)
    order = np.argsort(-screen[faces][:, :, 2].mean(axis=1))
    for fi in order:
        idx = faces[fi]
        p = screen[idx]
        if p[:, 2].min() <= 0:
            continue
        x0, x1, y0, y1 = _bbox(p, S)
        if x1 <= x0 or y1 <= y0:
            continue
        ax, ay = p[0, 0], p[0, 1]
        bx, by = p[1, 0], p[1, 1]
        cx, cy = p[2, 0], p[2, 1]
        area = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay)
        if abs(area) < 1e-9:
            continue
        ys, xs = np.mgrid[y0:y1, x0:x1]
        xs = xs + 0.5
        ys = ys + 0.5
        w0 = ((bx - ax) * (ys - ay) - (xs - ax) * (by - ay)) / area
        w1 = ((xs - ax) * (cy - ay) - (cx - ax) * (ys - ay)) / area
        w2 = 1.0 - w0 - w1
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not inside.any():
            continue
        z = w2 * p[0, 2] + w1 * p[1, 2] + w0 * p[2, 2]
        sub = zbuf[y0:y1, x0:x1]
        hit = inside & (z < sub)
        if not hit.any():
            continue
        sub[hit] = z[hit]
        img[y0:y1, x0:x1][hit] = colour[fi]


def _raster_mask(mask, pts, faces):
    S = mask.shape[0]
    for idx in faces:
        p = pts[idx]
        x0, x1, y0, y1 = _bbox(p, S)
        if x1 <= x0 or y1 <= y0:
            continue
        ax, ay = p[0]
        bx, by = p[1]
        cx, cy = p[2]
        area = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay)
        if abs(area) < 1e-9:
            continue
        ys, xs = np.mgrid[y0:y1, x0:x1]
        xs = xs + 0.5
        ys = ys + 0.5
        w0 = ((bx - ax) * (ys - ay) - (xs - ax) * (by - ay)) / area
        w1 = ((xs - ax) * (cy - ay) - (cx - ax) * (ys - ay)) / area
        w2 = 1.0 - w0 - w1
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        np.maximum(mask[y0:y1, x0:x1], inside, out=mask[y0:y1, x0:x1])


def _box_blur(a, r, passes=1):
    for _ in range(passes):
        pad = np.pad(a, r, mode="edge")
        cs = np.cumsum(np.cumsum(pad, axis=0), axis=1)
        cs = np.pad(cs, ((1, 0), (1, 0)))
        k = 2 * r + 1
        h, w = a.shape
        a = (cs[k:k + h, k:k + w] - cs[0:h, k:k + w]
             - cs[k:k + h, 0:w] + cs[0:h, 0:w]) / (k * k)
    return a


def contact_sheet(mesh, path, size=420, views=((38, 9), (90, 9), (0, 9), (38, 55))):
    import tempfile
    import os

    tiles = []
    for yaw, elev in views:
        fd, tmp = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        render(mesh, tmp, size=size, yaw=yaw, elev=elev, supersample=2)
        tiles.append(Image.open(tmp).copy())
        os.unlink(tmp)
    sheet = Image.new("RGB", (size * len(tiles), size))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * size, 0))
    sheet.save(path)
    return path
