#!/usr/bin/env python3
"""make_samples.py - build the SAMPLE photo set for the memories album.

Procedurally paints soft, impressionistic "family photographs" for a fictional
family (Walter & June Hale), then develops each one in the look of its era
(sepia cabinet card, deckled silver print, 1950s glossy, Kodachrome square,
1980s 4x6 with an orange date stamp, modern digital) and writes:

  site/memories/photos/sample/<id>.jpg          1600px long edge, q80, progressive
  site/memories/photos/sample/thumbs/<id>.jpg   480px long edge, q75
  site/memories/data/library.json               the manifest
  memories/tools/contact-sheet.jpg              review sheet (not deployed)

Deterministic: every image is seeded from a CRC of its id. Re-run any time:

  python3 memories/tools/make_samples.py            # everything
  python3 memories/tools/make_samples.py wedding-1948 grand-canyon-1966   # just these

Dependencies: Pillow + numpy only.
"""
import io
import json
import math
import os
import sys
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE = os.path.join(ROOT, 'site', 'memories')
OUT = os.path.join(SITE, 'photos', 'sample')
THUMBS = os.path.join(OUT, 'thumbs')
MANIFEST = os.path.join(SITE, 'data', 'library.json')
SHEET = os.path.join(HERE, 'contact-sheet.jpg')

LONG_EDGE = 1600
THUMB_EDGE = 480
RENDER_SCALE = 0.62  # scenes are painted smaller then enlarged: they are soft anyway

# ---------------------------------------------------------------- fonts
_GYRE = '/usr/share/texmf/fonts/opentype/public/tex-gyre/'
_FONTS = {
    'serif': [_GYRE + 'texgyretermes-regular.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'],
    'serif_b': [_GYRE + 'texgyretermes-bold.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'],
    'serif_i': [_GYRE + 'texgyretermes-italic.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'],
    'roman': ['/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Regular.ttf', _GYRE + 'texgyretermes-regular.otf'],
    'roman_i': ['/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Italic.ttf', _GYRE + 'texgyretermes-italic.otf'],
    'hand': [_GYRE + 'texgyrechorus-mediumitalic.otf', _GYRE + 'texgyretermes-italic.otf'],
    'type': [_GYRE + 'texgyrecursor-regular.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'],
    'type_b': [_GYRE + 'texgyrecursor-bold.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'],
    'sans_b': ['/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'],
    'sans': ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
}
_font_cache = {}


def font(name, px):
    key = (name, int(px))
    if key not in _font_cache:
        for path in _FONTS[name]:
            if os.path.exists(path):
                _font_cache[key] = ImageFont.truetype(path, max(6, int(px)))
                break
        else:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


# ---------------------------------------------------------------- numeric helpers
def _box0(a, r):
    n = a.shape[0]
    p = np.concatenate([np.repeat(a[:1], r + 1, 0), a, np.repeat(a[-1:], r, 0)], 0)
    c = np.cumsum(p, 0, dtype=np.float32)
    return (c[2 * r + 1:2 * r + 1 + n] - c[:n]) / (2 * r + 1)


def gauss(a, sigma):
    """Separable gaussian (3 box passes) on 2-D or 3-D float arrays."""
    if sigma <= 0.3:
        return a
    a = np.asarray(a, np.float32)
    w = math.sqrt(12 * sigma * sigma / 3 + 1)
    r = max(1, int(round((w - 1) / 2)))
    for _ in range(3):
        a = _box0(a, r)
    a = np.swapaxes(a, 0, 1)
    for _ in range(3):
        a = _box0(a, r)
    return np.swapaxes(a, 0, 1)


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(float(lerp(x, y, t)) for x, y in zip(c1, c2))


def shade(c, k):
    return tuple(max(0.0, min(1.0, x * k)) for x in c)


def lum(a):
    return a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11


def scurve(x, k):
    s = lambda v: 1 / (1 + np.exp(-k * (v - 0.5)))
    lo, hi = s(0.0), s(1.0)
    return (s(x) - lo) / (hi - lo)


def fnoise(h, w, rng, scales=(3, 6, 12, 24), weights=None, aspect=None):
    """Smooth fractal noise in 0..1."""
    weights = weights or [1.0 / (i + 1) for i in range(len(scales))]
    out = np.zeros((h, w), np.float32)
    for s, wt in zip(scales, weights):
        sh = max(2, int(s))
        sw = max(2, int(s * (aspect if aspect else w / h)))
        small = rng.random((sh, sw)).astype(np.float32)
        im = Image.fromarray(small, 'F').resize((w, h), Image.BICUBIC)
        out += np.asarray(im) * wt
    out -= out.min()
    out /= max(1e-6, out.max())
    return out


def resize_f(a, w, h):
    """Resize a float HxWxC array with PIL bicubic per channel."""
    if a.ndim == 2:
        return np.asarray(Image.fromarray(a.astype(np.float32), 'F').resize((w, h), Image.BICUBIC))
    return np.stack([resize_f(a[..., i], w, h) for i in range(a.shape[2])], -1)


def to_img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def from_img(im):
    return np.asarray(im.convert('RGB'), np.float32) / 255.0


# ---------------------------------------------------------------- canvas
class Canvas:
    """Float RGB canvas. Positions: x as fraction of width, y as fraction of
    height. Sizes (radii, widths, blur) are in units of the HEIGHT."""

    def __init__(self, W, H, seed):
        self.W, self.H = int(W), int(H)
        self.a = np.zeros((self.H, self.W, 3), np.float32)
        self.rng = np.random.default_rng(seed)
        self.aspect = self.W / self.H
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        self.yy, self.xx = yy / self.H, xx / self.W

    # coordinate helpers
    def P(self, pts):
        return [(x * self.W, y * self.H) for x, y in pts]

    def mask(self, draw, blur=0.0):
        m = Image.new('L', (self.W, self.H), 0)
        draw(ImageDraw.Draw(m))
        if blur > 0:
            m = m.filter(ImageFilter.GaussianBlur(blur * self.H))
        return np.asarray(m, np.float32) / 255.0

    def apply(self, m, color, alpha=1.0, mode='over'):
        col = np.asarray(color, np.float32)
        if col.ndim == 1:
            col = col[None, None, :]
        m = (m * alpha)[..., None]
        if mode == 'add':
            self.a += col * m
        elif mode == 'mul':
            self.a *= (1 - m) + col * m
        elif mode == 'screen':
            self.a = 1 - (1 - self.a) * (1 - col * m)
        else:
            self.a = self.a * (1 - m) + col * m

    def fill(self, color):
        self.a[:] = np.asarray(color, np.float32)

    def vgrad(self, stops, apply=True, x=False):
        t = self.xx if x else self.yy
        pos = [s[0] for s in stops]
        out = np.stack([np.interp(t, pos, [s[1][i] for s in stops]) for i in range(3)], -1).astype(np.float32)
        if apply:
            self.a[:] = out
        return out

    def ellipse(self, cx, cy, rx, ry, color, blur=0.0, alpha=1.0, mode='over'):
        X, Y, RX, RY = cx * self.W, cy * self.H, rx * self.H, ry * self.H
        m = self.mask(lambda d: d.ellipse([X - RX, Y - RY, X + RX, Y + RY], fill=255), blur)
        self.apply(m, color, alpha, mode)
        return m

    def poly(self, pts, color, blur=0.0, alpha=1.0, mode='over'):
        P = self.P(pts)
        m = self.mask(lambda d: d.polygon(P, fill=255), blur)
        self.apply(m, color, alpha, mode)
        return m

    def rect(self, x0, y0, x1, y1, color, blur=0.0, alpha=1.0, mode='over', radius=0):
        P = [x0 * self.W, y0 * self.H, x1 * self.W, y1 * self.H]
        R = radius * self.H
        if R > 0:
            m = self.mask(lambda d: d.rounded_rectangle(P, R, fill=255), blur)
        else:
            m = self.mask(lambda d: d.rectangle(P, fill=255), blur)
        self.apply(m, color, alpha, mode)
        return m

    def line(self, pts, width, color, blur=0.0, alpha=1.0, mode='over'):
        P = self.P(pts)
        Wd = max(1, int(round(width * self.H)))
        m = self.mask(lambda d: d.line(P, fill=255, width=Wd, joint='curve'), blur)
        self.apply(m, color, alpha, mode)
        return m

    def glow(self, cx, cy, r, color, strength=1.0, mode='add', ry=None):
        ry = r if ry is None else ry
        dx = (self.xx - cx) * self.W / self.H
        dy = self.yy - cy
        g = np.exp(-(dx * dx / (2 * r * r) + dy * dy / (2 * ry * ry))).astype(np.float32)
        self.apply(g, color, strength, mode)

    def blur(self, sigma):
        self.a = gauss(self.a, sigma * self.H)

    def noise_tint(self, color, amount, scales=(3, 6, 12), mode='over'):
        n = fnoise(self.H, self.W, self.rng, scales)
        self.apply(n, color, amount, mode)

    def text(self, xy, s, fname, size, color, anchor='mm', blur=0.0, alpha=1.0, mode='over', spacing=0):
        f = font(fname, size * self.H)
        X, Y = xy[0] * self.W, xy[1] * self.H
        if spacing:
            m = self.mask(lambda d: _spaced(d, X, Y, s, f, spacing * self.H, anchor), blur)
        else:
            m = self.mask(lambda d: d.text((X, Y), s, font=f, fill=255, anchor=anchor), blur)
        self.apply(m, color, alpha, mode)
        return m


def _spaced(d, X, Y, s, f, sp, anchor):
    widths = [f.getlength(ch) for ch in s]
    total = sum(widths) + sp * (len(s) - 1)
    x = X - total / 2 if anchor[0] == 'm' else (X - total if anchor[0] == 'r' else X)
    for ch, w in zip(s, widths):
        d.text((x, Y), ch, font=f, fill=255, anchor='l' + anchor[1])
        x += w + sp


# ---------------------------------------------------------------- groups (lit, soft figures)
class Group:
    """Draw several opaque parts, then light, soften and composite them as one."""

    def __init__(self, cv):
        self.cv = cv
        self.im = Image.new('RGBA', (cv.W, cv.H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    @staticmethod
    def _c(col):
        return tuple(int(max(0, min(1, c)) * 255 + 0.5) for c in col[:3]) + (255,)

    def ellipse(self, cx, cy, rx, ry, col):
        self.d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=self._c(col))

    def poly(self, pts, col):
        self.d.polygon([tuple(p) for p in pts], fill=self._c(col))

    def rect(self, x0, y0, x1, y1, col, r=0):
        if r > 0:
            self.d.rounded_rectangle([x0, y0, x1, y1], r, fill=self._c(col))
        else:
            self.d.rectangle([x0, y0, x1, y1], fill=self._c(col))

    def line(self, pts, w, col):
        self.d.line([tuple(p) for p in pts], fill=self._c(col), width=max(1, int(w)), joint='curve')

    def limb(self, p0, p1, w0, w1, col):
        (x0, y0), (x1, y1) = p0, p1
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        self.poly([(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2),
                   (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)], col)
        self.ellipse(x0, y0, w0 / 2, w0 / 2, col)
        self.ellipse(x1, y1, w1 / 2, w1 / 2, col)

    def commit(self, blur=0.004, light=(-0.6, -0.7), shade_amt=0.3, rim=0.18, rim_col=(1, 0.96, 0.88),
               alpha=1.0, rim_px=None, round_=0.006, ao=0.35, tex=0.12):
        """round_: organic merge of parts (H units); ao: darken toward silhouette edges (volume);
        tex: low-frequency mottling (folds, light through leaves)."""
        cv = self.cv
        arr = np.asarray(self.im, np.float32) / 255.0
        A = arr[..., 3]
        if A.max() <= 0:
            return
        ys, xs = np.nonzero(A > 0.5)
        if len(xs) == 0:
            return
        # work only inside the bounding box (fast)
        pad = int(cv.H * (round_ * 3 + blur * 4 + 0.02)) + 4
        bx0, bx1 = max(0, xs.min() - pad), min(cv.W, xs.max() + pad + 1)
        by0, by1 = max(0, ys.min() - pad), min(cv.H, ys.max() + pad + 1)
        A = A[by0:by1, bx0:bx1]
        rgb = arr[by0:by1, bx0:bx1, :3].copy()
        hh, ww = A.shape
        if round_ > 0:
            r = round_ * cv.H
            Ab = gauss(A, r)
            Am = np.clip((Ab - 0.32) / 0.36, 0, 1)
            Am = Am * Am * (3 - 2 * Am)
            num = gauss(rgb * A[..., None], r * 0.7)
            den = gauss(A, r * 0.7)[..., None]
            rgb = np.where(den > 1e-3, num / np.maximum(den, 1e-3), rgb)
            A = Am
        cx, cy = xs.mean() - bx0, ys.mean() - by0
        half = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 + 1
        lx, ly = light
        n = math.hypot(lx, ly) or 1
        lx, ly = lx / n, ly / n
        X = np.arange(ww, dtype=np.float32)[None, :]
        Y = np.arange(hh, dtype=np.float32)[:, None]
        proj = np.clip(((X - cx) * lx + (Y - cy) * ly) / half, -1, 1)
        rgb *= (1 + shade_amt * proj)[..., None]
        if ao > 0:  # rounded volume: darker toward the silhouette, offset away from light
            k = max(2.0, half * 0.12)
            inner = gauss(A, k)
            sh = np.roll(np.roll(inner, int(round(ly * k * 0.6)), 0), int(round(lx * k * 0.6)), 1)
            rgb *= (1 - ao + ao * np.clip(sh * 1.6 - 0.25, 0, 1))[..., None]
        if tex > 0:
            t = fnoise(hh, ww, cv.rng, (3, 7, 15), (1, 0.6, 0.3))
            rgb *= (1 - tex + 2 * tex * t)[..., None]
        if rim > 0:
            k = rim_px or max(2, int(cv.H * 0.006))
            sh = np.roll(np.roll(A, int(round(-ly * k)), 0), int(round(-lx * k)), 1)
            rr = gauss(np.clip(A - sh, 0, 1), k * 0.7)
            rgb += (rr * rim)[..., None] * np.asarray(rim_col, np.float32)
        s = blur * cv.H
        pre = gauss(rgb * A[..., None], s)
        A2 = gauss(A, s) * alpha
        sub = cv.a[by0:by1, bx0:bx1]
        cv.a[by0:by1, bx0:bx1] = sub * (1 - A2[..., None]) + pre * alpha


# ---------------------------------------------------------------- figures
SKIN = (0.86, 0.68, 0.56)
SKIN_OLD = (0.84, 0.69, 0.60)


def _arm(g, S, side, spec, U, col, skin, sleeve_short=False, hand=True):
    if isinstance(spec, (int, float)):
        a1 = a2 = spec
    else:
        a1, a2 = spec
    up, lo = 0.19 * U, 0.17 * U
    t1, t2 = math.radians(a1), math.radians(a2)
    E = (S[0] + side * math.sin(t1) * up, S[1] + math.cos(t1) * up)
    Hd = (E[0] + side * math.sin(t2) * lo, E[1] + math.cos(t2) * lo)
    g.limb(S, E, 0.052 * U, 0.042 * U, col)
    g.limb(E, Hd, 0.04 * U, 0.03 * U, skin if sleeve_short else col)
    if hand:
        g.ellipse(Hd[0], Hd[1] + 0.006 * U, 0.016 * U, 0.02 * U, shade(skin, 0.92))
    return Hd


def person(cv, x, y, h, top=(0.3, 0.3, 0.33), bottom=None, skin=SKIN, hair=(0.18, 0.12, 0.08),
           hairstyle='short', dress=None, hat=None, hat_col=None, arms=None, pose='stand', child=False,
           facing=1, build=1.0, short_sleeves=False, shoes=(0.1, 0.08, 0.07), g=None, commit=True,
           legs_col=None, view='front', turn=0.5, **kw):
    """A soft human figure, never with features. (x, y) = feet (or seat for pose='ride');
    h = standing height (H units). view='back' for a figure seen from behind."""
    own = g is None
    g = g or Group(cv)
    U = h * cv.H
    X, Y = x * cv.W, y * cv.H
    bottom = bottom or top
    legs_col = legs_col or (bottom if not dress else skin)
    rng = cv.rng
    if arms is None:
        arms = (rng.uniform(2, 9), rng.uniform(2, 9))
    hipf, shf, hrx, hry = (0.42, 0.29, 0.07, 0.08) if child else (0.48, 0.335, 0.047, 0.059)
    if pose in ('stand', 'stride'):
        hipY = Y - hipf * U
    elif pose in ('sit', 'sitfront'):
        hipY = Y - (0.23 if child else 0.27) * U
    elif pose == 'floor':
        hipY = Y - 0.04 * U
    else:  # ride
        hipY = Y
    shY = hipY - shf * U
    headY = shY - 0.022 * U - hry * U
    sw = (0.095 if child else 0.108) * U * build
    hw = (0.07 if child else 0.078) * U * build
    if dress:
        sw *= 0.88
        hw *= 0.95
    tx = facing * turn * 0.012 * U  # how far the face is turned toward `facing`
    # long hair behind the shoulders
    if hairstyle == 'long':
        g.poly([(X - 0.06 * U, headY), (X + 0.06 * U, headY), (X + 0.07 * U, shY + 0.07 * U),
                (X - 0.07 * U, shY + 0.07 * U)], hair)
    # legs
    if pose in ('stand', 'stride'):
        spread = (0.035 if pose == 'stand' else 0.09) * (0.8 if child else 1)
        lean = rng.uniform(-0.01, 0.01) * U
        for s in (-1, 1):
            fx = X + s * spread * U + lean
            g.limb((X + s * hw * 0.45, hipY - 0.02 * U), (fx, Y - 0.025 * U), 0.075 * U * build, 0.038 * U, legs_col)
            g.ellipse(fx + facing * 0.01 * U, Y - 0.014 * U, 0.03 * U, 0.015 * U, shoes)
    elif pose == 'sit':
        for s in (-1, 1):
            K = (X + facing * 0.21 * U + s * 0.025 * U, hipY - 0.01 * U)
            g.limb((X + s * hw * 0.35, hipY), K, 0.08 * U, 0.05 * U, legs_col)
            g.limb(K, (K[0] + facing * 0.012 * U, Y - 0.022 * U), 0.05 * U, 0.036 * U, legs_col)
            g.ellipse(K[0] + facing * 0.03 * U, Y - 0.013 * U, 0.03 * U, 0.015 * U, shoes)
    elif pose == 'sitfront':
        for s in (-1, 1):
            kx = X + s * 0.055 * U
            g.ellipse(kx, hipY + 0.005 * U, 0.05 * U, 0.045 * U, legs_col)
            g.limb((kx, hipY + 0.01 * U), (kx + s * 0.01 * U, Y - 0.02 * U), 0.055 * U, 0.038 * U, legs_col)
            g.ellipse(kx + s * 0.012 * U, Y - 0.012 * U, 0.03 * U, 0.016 * U, shoes)
    elif pose == 'floor':
        g.ellipse(X + facing * 0.04 * U, hipY - 0.005 * U, 0.17 * U, 0.05 * U, legs_col)
    elif pose == 'ride':
        K = (X + facing * 0.1 * U, Y + 0.16 * U)
        g.limb((X, Y), K, 0.08 * U, 0.052 * U, legs_col)
        F = (K[0] - facing * 0.035 * U, K[1] + 0.2 * U)
        g.limb(K, F, 0.05 * U, 0.038 * U, legs_col)
        g.ellipse(F[0] + facing * 0.018 * U, F[1], 0.032 * U, 0.016 * U, shoes)
    # skirt
    waistY = hipY - 0.08 * U
    if dress:
        hem = {'knee': Y - 0.25 * U, 'mid': Y - 0.16 * U, 'long': Y - 0.004 * U}.get(dress, Y - 0.22 * U)
        flare = kw.pop('flare', 1.0)
        if pose == 'sit':
            K = X + facing * 0.23 * U
            g.poly([(X - 0.07 * U, waistY), (X + 0.07 * U, waistY), (K + facing * 0.03 * U, hipY - 0.045 * U),
                    (K + facing * 0.035 * U, hipY + 0.12 * U), (K - facing * 0.06 * U, hipY + 0.15 * U),
                    (X - facing * 0.085 * U, hipY + 0.05 * U)], bottom)
        elif pose == 'floor':
            g.ellipse(X + facing * 0.03 * U, hipY - 0.012 * U, 0.2 * U, 0.065 * U, bottom)
        elif pose == 'sitfront':
            low = hem if dress == 'long' else min(hem, Y - 0.12 * U)
            g.poly([(X - 0.07 * U, waistY), (X + 0.07 * U, waistY), (X + 0.13 * U * flare, hipY + 0.02 * U),
                    (X + 0.12 * U * flare, low), (X - 0.12 * U * flare, low), (X - 0.13 * U * flare, hipY + 0.02 * U)],
                   bottom)
            g.ellipse(X, low, 0.12 * U * flare, 0.016 * U, bottom)
        else:
            hwid = (0.12 if dress != 'long' else 0.16) * U * flare
            g.poly([(X - 0.07 * U, waistY), (X + 0.07 * U, waistY), (X + hwid, hem - 0.01 * U),
                    (X - hwid, hem - 0.01 * U)], bottom)
            g.ellipse(X, hem - 0.01 * U, hwid, 0.018 * U, bottom)
    # torso: chest + waist + sloping shoulders
    g.poly([(X - 0.03 * U, shY - 0.012 * U), (X + 0.03 * U, shY - 0.012 * U), (X + sw, shY + 0.03 * U),
            (X + sw * 0.95, shY + 0.11 * U), (X + hw, (waistY if dress else hipY) + 0.01 * U),
            (X - hw, (waistY if dress else hipY) + 0.01 * U), (X - sw * 0.95, shY + 0.11 * U),
            (X - sw, shY + 0.03 * U)], top)
    g.ellipse(X, shY + 0.1 * U, sw * 0.92, 0.1 * U, top)
    if not dress:
        g.ellipse(X, hipY - 0.03 * U, hw * 1.02, 0.06 * U, top if pose not in ('sit', 'sitfront') else bottom)
    # arms
    hands = []
    for s, spec in zip((-1, 1), arms):
        if spec is None:
            continue
        hands.append(_arm(g, (X + s * (sw - 0.03 * U), shY + 0.045 * U), s, spec, U, top, skin, short_sleeves))
    # neck & head
    g.rect(X - 0.02 * U, headY + 0.03 * U, X + 0.02 * U, shY + 0.01 * U, shade(skin, 0.85))
    hb = -facing * turn * 0.01 * U  # hair mass sits toward the back of the head
    if view == 'back':
        g.ellipse(X, headY, hrx * U * 1.06, hry * U * 1.02, hair)
        if hairstyle in ('bob', 'wave', 'curly', 'long', 'bun'):
            g.ellipse(X, headY + 0.03 * U, hrx * U * 1.25, hry * U * 0.8, hair)
        if hairstyle == 'bun':
            g.ellipse(X, headY + 0.01 * U, 0.03 * U, 0.028 * U, shade(hair, 0.9))
    elif hairstyle in ('short', 'thin', 'bald'):
        hs = {'short': (1.08, 1.0), 'thin': (1.04, 0.96), 'bald': (1.0, 0.8)}[hairstyle]
        g.ellipse(X + hb, headY - 0.01 * U, hrx * U * hs[0], hry * U * hs[1], hair)
        g.ellipse(X + tx, headY + 0.008 * U, hrx * U * 0.94, hry * U * 0.93, skin)
    elif hairstyle == 'baby':
        g.ellipse(X + tx, headY, hrx * U, hry * U, skin)
        g.ellipse(X, headY - 0.04 * U, 0.04 * U, 0.02 * U, hair)
    else:  # bob / wave / curly / long / bun
        big = 1.32 if hairstyle in ('wave', 'curly') else 1.22
        g.ellipse(X + hb, headY - 0.004 * U, hrx * U * big, hry * U * 1.06, hair)
        if hairstyle in ('bob', 'wave', 'curly', 'long'):
            for s in (-1, 1):
                g.ellipse(X + hb + s * hrx * U * 0.9, headY + 0.035 * U, 0.026 * U, 0.034 * U, hair)
        if hairstyle == 'bun':
            g.ellipse(X + hb * 2, headY - 0.065 * U, 0.03 * U, 0.025 * U, hair)
        g.ellipse(X + tx, headY + 0.012 * U, hrx * U * 0.9, hry * U * 0.88, skin)
    # hats
    hc = hat_col or (0.18, 0.16, 0.14)
    if hat == 'fedora':
        g.ellipse(X, headY - 0.04 * U, 0.085 * U, 0.016 * U, hc)
        g.rect(X - 0.048 * U, headY - 0.09 * U, X + 0.048 * U, headY - 0.04 * U, hc, r=0.018 * U)
    elif hat == 'garrison':
        g.poly([(X - 0.055 * U, headY - 0.032 * U), (X + 0.058 * U, headY - 0.045 * U),
                (X + 0.046 * U, headY - 0.072 * U), (X - 0.048 * U, headY - 0.062 * U)], hc)
    elif hat == 'sunhat':
        g.ellipse(X, headY - 0.03 * U, 0.12 * U, 0.022 * U, hc)
        g.ellipse(X, headY - 0.048 * U, 0.055 * U, 0.035 * U, hc)
    elif hat == 'cap':
        g.ellipse(X, headY - 0.032 * U, 0.054 * U, 0.036 * U, hc)
        g.ellipse(X + facing * 0.045 * U, headY - 0.02 * U, 0.045 * U, 0.01 * U, hc)
    elif hat == 'scarf':
        g.ellipse(X, headY - 0.006 * U, hrx * U * 1.3, hry * U * 1.12, hc)
        g.ellipse(X + tx, headY + 0.016 * U, hrx * U * 0.82, hry * U * 0.78, skin)
    if own and commit:
        ck = {k: v for k, v in kw.items() if k in ('blur', 'light', 'shade_amt', 'rim', 'rim_col', 'alpha',
                                                   'round_', 'ao', 'tex')}
        ck.setdefault('round_', 0.004 * h / 0.5 + 0.002)
        g.commit(**ck)
    return g, hands


def shadow(cv, x, y, rx, ry, alpha=0.4, blur=0.01, color=(0, 0, 0)):
    cv.ellipse(x, y, rx, ry, color, blur=blur, alpha=alpha)


def horse(cv, x, y, s, col=(0.35, 0.24, 0.16), facing=1, g=None, mane=None):
    """s = height at withers (H units). (x, y) = ground point under the barrel."""
    g = g or Group(cv)
    U = s * cv.H
    X, Y = x * cv.W, y * cv.H
    f = facing
    dark = shade(col, 0.55)
    mane = mane or shade(col, 0.4)
    # far legs (slightly darker)
    for lx, bend in ((-0.36, 0.05), (0.3, -0.02)):
        top = (X + f * lx * U, Y - 0.62 * U)
        knee = (X + f * (lx + bend) * U, Y - 0.3 * U)
        g.limb(top, knee, 0.11 * U, 0.06 * U, shade(col, 0.75))
        g.limb(knee, (knee[0], Y - 0.03 * U), 0.055 * U, 0.05 * U, shade(col, 0.7))
        g.ellipse(knee[0], Y - 0.025 * U, 0.04 * U, 0.025 * U, dark)
    # tail
    g.poly([(X - f * 0.55 * U, Y - 0.92 * U), (X - f * 0.62 * U, Y - 0.86 * U), (X - f * 0.66 * U, Y - 0.5 * U),
            (X - f * 0.6 * U, Y - 0.4 * U), (X - f * 0.56 * U, Y - 0.6 * U)], mane)
    # barrel, rump, chest
    g.ellipse(X, Y - 0.78 * U, 0.5 * U, 0.22 * U, col)
    g.ellipse(X - f * 0.4 * U, Y - 0.8 * U, 0.2 * U, 0.21 * U, col)
    g.ellipse(X + f * 0.38 * U, Y - 0.78 * U, 0.19 * U, 0.2 * U, col)
    # neck + head
    g.poly([(X + f * 0.22 * U, Y - 0.92 * U), (X + f * 0.5 * U, Y - 1.42 * U), (X + f * 0.66 * U, Y - 1.36 * U),
            (X + f * 0.56 * U, Y - 0.72 * U)], col)
    g.poly([(X + f * 0.5 * U, Y - 1.44 * U), (X + f * 0.64 * U, Y - 1.42 * U), (X + f * 0.9 * U, Y - 1.14 * U),
            (X + f * 0.86 * U, Y - 1.06 * U), (X + f * 0.74 * U, Y - 1.1 * U), (X + f * 0.56 * U, Y - 1.28 * U)], col)
    g.ellipse(X + f * 0.86 * U, Y - 1.1 * U, 0.05 * U, 0.05 * U, shade(col, 0.85))
    g.poly([(X + f * 0.52 * U, Y - 1.42 * U), (X + f * 0.5 * U, Y - 1.54 * U), (X + f * 0.58 * U, Y - 1.44 * U)], col)
    # mane
    g.poly([(X + f * 0.2 * U, Y - 0.95 * U), (X + f * 0.48 * U, Y - 1.44 * U), (X + f * 0.53 * U, Y - 1.4 * U),
            (X + f * 0.3 * U, Y - 0.95 * U)], mane)
    # near legs
    for lx, bend in ((-0.3, 0.06), (0.36, 0.0)):
        top = (X + f * lx * U, Y - 0.62 * U)
        knee = (X + f * (lx + bend) * U, Y - 0.3 * U)
        g.limb(top, knee, 0.12 * U, 0.065 * U, col)
        g.limb(knee, (knee[0] + f * 0.01 * U, Y - 0.03 * U), 0.06 * U, 0.052 * U, col)
        g.ellipse(knee[0] + f * 0.01 * U, Y - 0.022 * U, 0.042 * U, 0.026 * U, dark)
    return g


def dog(cv, x, y, s, col=(0.55, 0.4, 0.25), facing=1, g=None, sit=False):
    """s = shoulder height (H units)."""
    g = g or Group(cv)
    U = s * cv.H
    X, Y = x * cv.W, y * cv.H
    f = facing
    ear = shade(col, 0.6)
    if sit:
        g.ellipse(X - f * 0.15 * U, Y - 0.35 * U, 0.35 * U, 0.33 * U, col)
        g.limb((X + f * 0.15 * U, Y - 0.6 * U), (X + f * 0.2 * U, Y - 0.04 * U), 0.14 * U, 0.1 * U, col)
        g.poly([(X - f * 0.05 * U, Y - 0.6 * U), (X + f * 0.3 * U, Y - 1.05 * U), (X + f * 0.45 * U, Y - 0.95 * U),
                (X + f * 0.3 * U, Y - 0.45 * U)], col)
        hx, hy = X + f * 0.4 * U, Y - 1.08 * U
    else:
        for lx in (-0.42, -0.3, 0.32, 0.44):
            g.limb((X + f * lx * U, Y - 0.55 * U), (X + f * (lx + 0.02) * U, Y - 0.04 * U), 0.13 * U, 0.09 * U,
                   shade(col, 0.85 if lx in (-0.3, 0.44) else 1.0))
        g.ellipse(X, Y - 0.62 * U, 0.52 * U, 0.2 * U, col)
        g.poly([(X - f * 0.45 * U, Y - 0.7 * U), (X - f * 0.75 * U, Y - 1.0 * U), (X - f * 0.7 * U, Y - 1.05 * U),
                (X - f * 0.4 * U, Y - 0.78 * U)], col)
        g.poly([(X + f * 0.3 * U, Y - 0.72 * U), (X + f * 0.5 * U, Y - 1.05 * U), (X + f * 0.65 * U, Y - 0.98 * U),
                (X + f * 0.55 * U, Y - 0.6 * U)], col)
        hx, hy = X + f * 0.6 * U, Y - 1.08 * U
    g.ellipse(hx, hy, 0.16 * U, 0.14 * U, col)
    g.ellipse(hx + f * 0.15 * U, hy + 0.05 * U, 0.1 * U, 0.07 * U, shade(col, 0.95))
    g.ellipse(hx + f * 0.24 * U, hy + 0.03 * U, 0.03 * U, 0.025 * U, (0.08, 0.06, 0.05))
    g.poly([(hx - f * 0.06 * U, hy - 0.1 * U), (hx - f * 0.16 * U, hy - 0.02 * U), (hx - f * 0.12 * U, hy + 0.14 * U),
            (hx - f * 0.02 * U, hy + 0.02 * U)], ear)
    return g


def car(cv, x, y, L, body=(0.2, 0.25, 0.3), roof=None, facing=1, wagon=False, wood=False, g=None,
        glass=(0.55, 0.6, 0.65), luggage=False):
    """1950s-60s automobile, side view. (x,y) ground centre; L = length (H units)."""
    g = g or Group(cv)
    U = L * cv.H
    X, Y = x * cv.W, y * cv.H
    f = facing
    roof = roof or body
    # body
    g.rect(X - 0.5 * U, Y - 0.27 * U, X + 0.5 * U, Y - 0.09 * U, body, r=0.07 * U)
    if wagon:
        g.poly([(X - 0.48 * U * f, Y - 0.25 * U), (X - 0.47 * U * f, Y - 0.43 * U), (X + 0.1 * U * f, Y - 0.43 * U),
                (X + 0.24 * U * f, Y - 0.26 * U)], roof)
        for wx0, wx1 in ((-0.44, -0.24), (-0.21, -0.03), (0.0, 0.17)):
            a0, a1 = sorted((X + wx0 * U * f, X + wx1 * U * f))
            top = Y - 0.405 * U
            g.poly([(a0, Y - 0.28 * U), (a0, top), (a1, top), (a1 + (0.05 * U if (wx1 == 0.17) == (f > 0) else 0),
                                                                  Y - 0.28 * U)], glass)
        if luggage:
            g.rect(X - 0.4 * U, Y - 0.52 * U, X + 0.02 * U, Y - 0.43 * U, (0.55, 0.45, 0.3), r=0.015 * U)
            g.rect(X - 0.34 * U, Y - 0.58 * U, X - 0.12 * U, Y - 0.51 * U, (0.3, 0.38, 0.45), r=0.015 * U)
            g.rect(X - 0.45 * U, Y - 0.44 * U, X + 0.07 * U, Y - 0.425 * U, (0.7, 0.7, 0.7))
    else:
        g.poly([(X - 0.32 * U * f, Y - 0.26 * U), (X - 0.22 * U * f, Y - 0.44 * U), (X + 0.08 * U * f, Y - 0.44 * U),
                (X + 0.22 * U * f, Y - 0.26 * U)], roof)
        for wx0, wx1 in ((-0.27, -0.08), (-0.05, 0.13)):
            a0, a1 = X + wx0 * U * f, X + wx1 * U * f
            g.poly([(a0 - 0.03 * U * f, Y - 0.28 * U), (a0 + 0.04 * U * f, Y - 0.415 * U),
                    (a1 + (0.0 if wx1 < 0 else -0.02) * U * f, Y - 0.415 * U), (a1 + 0.05 * U * f, Y - 0.28 * U)], glass)
    if wood:
        g.rect(X - 0.47 * U, Y - 0.245 * U, X + 0.25 * U * f if f > 0 else X + 0.47 * U, Y - 0.14 * U,
               (0.5, 0.33, 0.18), r=0.01 * U)
    # chrome strip + bumpers
    g.rect(X - 0.48 * U, Y - 0.2 * U, X + 0.48 * U, Y - 0.19 * U, (0.85, 0.85, 0.85))
    g.rect(X - 0.53 * U, Y - 0.15 * U, X - 0.44 * U, Y - 0.11 * U, (0.82, 0.82, 0.82), r=0.02 * U)
    g.rect(X + 0.44 * U, Y - 0.15 * U, X + 0.53 * U, Y - 0.11 * U, (0.82, 0.82, 0.82), r=0.02 * U)
    # wheels
    for wx in (-0.31, 0.31):
        cx = X + wx * U
        g.ellipse(cx, Y - 0.085 * U, 0.1 * U, 0.1 * U, (0.12, 0.12, 0.13))
        g.ellipse(cx, Y - 0.085 * U, 0.075 * U, 0.075 * U, (0.86, 0.86, 0.84))
        g.ellipse(cx, Y - 0.085 * U, 0.05 * U, 0.05 * U, (0.5, 0.5, 0.52))
        g.ellipse(cx, Y - 0.085 * U, 0.03 * U, 0.03 * U, (0.8, 0.8, 0.8))
    return g


def tree(cv, x, y, h, crown=(0.25, 0.32, 0.18), trunk=(0.25, 0.2, 0.15), blur=0.004, light=(-0.6, -0.8),
         spread=1.0, n=14, alpha=1.0, rng=None):
    rng = rng or cv.rng
    g = Group(cv)
    U = h * cv.H
    X, Y = x * cv.W, y * cv.H
    g.limb((X, Y), (X + 0.02 * U, Y - 0.55 * U), 0.06 * U, 0.035 * U, trunk)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, 0.25) * U * spread
        cx = X + math.cos(a) * r * 1.2
        cy = Y - 0.68 * U + math.sin(a) * r * 0.8
        rr = rng.uniform(0.12, 0.2) * U * spread
        g.ellipse(cx, cy, rr, rr * 0.85, shade(crown, rng.uniform(0.85, 1.1)))
    g.commit(blur=blur, light=light, shade_amt=0.45, rim=0.15, alpha=alpha)


def pine(cv, x, y, h, col=(0.12, 0.2, 0.15), blur=0.003, light=(-0.6, -0.8), alpha=1.0, rng=None):
    rng = rng or cv.rng
    g = Group(cv)
    U = h * cv.H
    X, Y = x * cv.W, y * cv.H
    g.rect(X - 0.015 * U, Y - 0.15 * U, X + 0.015 * U, Y, (0.2, 0.15, 0.1))
    tiers = 6
    for i in range(tiers):
        t = i / (tiers - 1)
        yb = Y - 0.1 * U - t * 0.75 * U
        w = (0.22 - 0.17 * t) * U * rng.uniform(0.85, 1.15)
        g.poly([(X - w, yb), (X + rng.uniform(-0.02, 0.02) * U, yb - 0.3 * U), (X + w, yb)],
               shade(col, rng.uniform(0.85, 1.1)))
    g.commit(blur=blur, light=light, shade_amt=0.4, rim=0.1, alpha=alpha)


def ridge(cv, base, amp, color, blur=0.004, rough=0.5, steps=80, seed_off=0, alpha=1.0, jag=1.0):
    rng = np.random.default_rng(int(cv.rng.integers(1 << 30)) + seed_off)
    xs = np.linspace(-0.02, 1.02, steps)
    v = np.cumsum(rng.normal(0, 1, steps)) * rough
    v = v - v.mean()
    v = v / (np.abs(v).max() + 1e-6)
    v = v + rng.normal(0, 0.15 * jag, steps)
    pts = [(xx, base - amp * (0.5 + 0.5 * vv)) for xx, vv in zip(xs, v)]
    pts += [(1.02, 1.05), (-0.02, 1.05)]
    return cv.poly(pts, color, blur=blur, alpha=alpha)


def treeline(cv, base, h, color, blur=0.006, n=60, alpha=1.0, var=0.25):
    rng = cv.rng
    g = Group(cv)
    for i in range(n):
        x = rng.uniform(-0.05, 1.05) * cv.W
        r = h * cv.H * rng.uniform(0.5, 1.0)
        cy = base * cv.H - r * rng.uniform(0.3, 0.9)
        g.ellipse(x, cy, r * rng.uniform(0.6, 1.1), r, shade(color, rng.uniform(1 - var, 1 + var)))
    g.rect(-5, base * cv.H - h * cv.H * 0.3, cv.W + 5, base * cv.H + 2, color)
    g.commit(blur=blur, shade_amt=0.15, rim=0.0, alpha=alpha)


def clouds(cv, n, y0, y1, color=(1, 1, 1), alpha=0.6, blur=0.03, size=0.06):
    rng = cv.rng
    for _ in range(n):
        cx, cy = rng.uniform(-0.1, 1.1), rng.uniform(y0, y1)
        for _ in range(5):
            cv.ellipse(cx + rng.uniform(-0.06, 0.06), cy + rng.uniform(-0.015, 0.015),
                       size * rng.uniform(0.6, 1.4), size * rng.uniform(0.25, 0.5), color, blur=blur,
                       alpha=alpha * rng.uniform(0.4, 0.8))


def bokeh(cv, pts, r, colors, strength=0.6, blur=0.004):
    rng = cv.rng
    for i, (x, y) in enumerate(pts):
        c = colors[i % len(colors)]
        rr = r * rng.uniform(0.75, 1.25)
        cv.ellipse(x, y, rr, rr, c, blur=blur, alpha=strength * rng.uniform(0.5, 1.0), mode='add')


# ================================================================ darkroom (era looks)
def _tone(L, stops):
    pos = [s[0] for s in stops]
    return np.stack([np.interp(L, pos, [s[1][i] for s in stops]) for i in range(3)], -1).astype(np.float32)


def _grain(rng, H, W, amt, sigma=0.75, color=0.0):
    n = rng.standard_normal((H, W)).astype(np.float32)
    n = gauss(n, sigma)
    n /= (n.std() + 1e-6)
    if color:
        c = gauss(rng.standard_normal((H, W, 3)).astype(np.float32), sigma * 1.6)
        c /= (c.std() + 1e-6)
        return n[..., None] * amt + c * amt * color
    return n * amt


def _vignette(H, W, amt, power=2.2, cx=0.5, cy=0.5):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx / W - cx) * 2
    dy = (yy / H - cy) * 2
    r = np.sqrt(dx * dx * 0.85 + dy * dy * 0.85)
    return 1 - amt * np.clip(r, 0, 1.6) ** power


def _sat(a, k):
    L = lum(a)[..., None]
    return L + (a - L) * k


ERAS = {
    #            contrast  fade  grain  soft  vign  halation
    'sepia':    dict(k=4.2, fade=0.07, grain=0.028, soft=1.6, vig=0.42, hal=0.22),
    'silver':   dict(k=4.8, fade=0.05, grain=0.026, soft=1.3, vig=0.36, hal=0.18),
    'bw50':     dict(k=5.2, fade=0.03, grain=0.022, soft=1.0, vig=0.28, hal=0.14),
    'kodacolor': dict(k=3.0, fade=0.08, grain=0.02, soft=1.2, vig=0.3, hal=0.16),
    'kodachrome': dict(k=3.6, fade=0.05, grain=0.018, soft=1.0, vig=0.3, hal=0.14),
    'faded70':  dict(k=2.8, fade=0.09, grain=0.02, soft=1.2, vig=0.28, hal=0.16),
    'glossy80': dict(k=3.4, fade=0.03, grain=0.016, soft=0.9, vig=0.32, hal=0.1),
    'digital00': dict(k=3.2, fade=0.0, grain=0.012, soft=0.4, vig=0.12, hal=0.0),
    'digital10': dict(k=3.0, fade=0.01, grain=0.008, soft=0.5, vig=0.18, hal=0.04),
    'object':   dict(k=2.6, fade=0.0, grain=0.01, soft=0.5, vig=0.22, hal=0.0),
}


def develop(a, era, rng):
    p = ERAS[era]
    H, W = a.shape[:2]
    S = max(H, W)
    a = np.clip(a, 0, 1.5)
    if p['soft']:
        a = gauss(a, p['soft'])
    mono = era in ('sepia', 'silver', 'bw50')
    if mono:
        L = np.clip(lum(a), 0, 1.2)
        if p['hal']:
            L = L + p['hal'] * gauss(np.clip(L - 0.72, 0, 1), S * 0.012)
        L = scurve(np.clip(L, 0, 1), p['k'])
        # uneven age: slow mottling of density
        if era != 'bw50':
            L = L * (0.94 + 0.08 * fnoise(H, W, rng, (2, 4, 8)))
        L = L * _vignette(H, W, p['vig'])
        L = L + _grain(rng, H, W, p['grain']) * (0.35 + 2.4 * L * (1 - L))
        L = np.clip(L, 0, 1)
        L = p['fade'] + L * (1 - p['fade'] - (0.03 if era == 'sepia' else 0.015))
        if era == 'sepia':
            out = _tone(L, [(0, (0.13, 0.085, 0.055)), (0.45, (0.47, 0.35, 0.24)),
                            (0.8, (0.82, 0.71, 0.55)), (1, (0.95, 0.9, 0.78))])
        elif era == 'silver':
            out = _tone(L, [(0, (0.07, 0.065, 0.06)), (0.5, (0.47, 0.455, 0.43)), (1, (0.95, 0.935, 0.9))])
        else:
            out = _tone(L, [(0, (0.04, 0.04, 0.045)), (0.5, (0.49, 0.49, 0.49)), (1, (0.97, 0.97, 0.96))])
        return np.clip(out, 0, 1)
    # ---- colour
    if p['hal']:
        hl = gauss(np.clip(lum(a) - 0.7, 0, 1), S * 0.012)
        a = a + p['hal'] * hl[..., None] * np.array([1.0, 0.45, 0.25], np.float32)
    a = np.clip(a, 0, 1)
    L = lum(a)
    if era == 'kodachrome':
        a = _sat(a, 1.18)
        a = scurve(np.clip(a, 0, 1), p['k'])
        sh = (1 - L)[..., None] ** 2
        hi = L[..., None] ** 2
        a = a + sh * np.array([-0.03, 0.01, 0.035]) + hi * np.array([0.04, 0.015, -0.04])
    elif era == 'kodacolor':
        a = _sat(a, 0.92)
        a = scurve(np.clip(a, 0, 1), p['k'])
        a = a * np.array([1.05, 0.95, 0.84]) + np.array([0.03, 0.02, 0.02])
    elif era == 'faded70':
        a = _sat(a, 0.88)
        a = scurve(np.clip(a, 0, 1), p['k'])
        a = a * np.array([1.04, 0.93, 0.83]) + np.array([0.02, 0.0, 0.03])
    elif era == 'glossy80':
        a = _sat(a, 1.12)
        a = scurve(np.clip(a, 0, 1), p['k'])
        a = a * np.array([1.03, 1.0, 0.95])
    elif era == 'digital00':
        a = _sat(a, 1.08)
        a = scurve(np.clip(a, 0, 1), p['k'])
        a = a * np.array([0.98, 1.0, 1.03])
        a = a + 0.6 * (a - gauss(a, 2.0))  # in-camera sharpening
    elif era in ('digital10', 'object'):
        a = _sat(a, 1.04)
        a = scurve(np.clip(a, 0, 1), p['k'])
        a = a * np.array([1.02, 1.0, 0.97])
    a = np.clip(a, 0, 1)
    a = a * _vignette(H, W, p['vig'])[..., None]
    L = lum(a)
    a = a + _grain(rng, H, W, p['grain'], color=0.35)[...] * (0.4 + 2.2 * L * (1 - L))[..., None]
    if p['fade']:
        a = p['fade'] * np.array([1.0, 0.85, 0.95]) + a * (1 - p['fade'] * 1.4)
    return np.clip(a, 0, 1)


# ================================================================ prints & frames
ORIENT = {'P': (1200, 1600), 'L': (1600, 1200), 'S': (1600, 1600), 'P6': (1067, 1600), 'L6': (1600, 1067),
          'L3': (1600, 1067), 'L5': (1600, 1280), 'P5': (1280, 1600)}


def frame_geometry(style, W, H):
    m = min(W, H)
    if style == 'cabinet':
        return int(0.09 * W), int(0.065 * H), W - int(0.09 * W), H - int(0.17 * H)
    if style == 'deckle':  # print sits on a black album page
        pm, b = int(0.06 * m), int(0.05 * m)
        return pm + b, pm + b, W - pm - b, H - pm - b
    if style == 'scallop':
        pm, b = int(0.035 * m), int(0.055 * m)
        return pm + b, pm + b, W - pm - b, H - pm - b
    if style == 'border':
        b = int(0.055 * m)
        return b, b, W - b, H - b
    if style == 'kodak':
        b = int(0.045 * m)
        return b, b, W - b, H - b
    return 0, 0, W, H


def _paper(H, W, rng, base, amt=0.03):
    n = fnoise(H, W, rng, (4, 16, 64), (0.5, 0.3, 0.2))
    fine = gauss(rng.standard_normal((H, W)).astype(np.float32), 0.8) * 0.012
    return np.asarray(base, np.float32)[None, None] * (1 - amt + amt * 2 * n[..., None]) + fine[..., None]


def _edge_wave(n, rng, kind, scale):
    t = np.arange(n, dtype=np.float32)
    if kind == 'deckle':
        per = 11 * scale
        w = 0.5 + 0.5 * np.sin(2 * np.pi * t / per + rng.uniform(0, 6))
        w = w ** 0.7 * 5 * scale + rng.normal(0, 0.7 * scale, n)
        w = np.convolve(w, np.ones(3) / 3, 'same')
        return w
    if kind == 'scallop':
        per = 34 * scale
        ph = (t / per) % 1.0
        return (1 - np.sqrt(np.clip(1 - (2 * ph - 1) ** 2, 0, 1))) * 9 * scale
    return np.zeros(n, np.float32)


def _print_mask(W, H, box, kind, rng, scale):
    x0, y0, x1, y1 = box
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    top = y0 + _edge_wave(W, rng, kind, scale)[None, :]
    bot = y1 - _edge_wave(W, rng, kind, scale)[None, :]
    lef = x0 + _edge_wave(H, rng, kind, scale)[:, None]
    rig = x1 - _edge_wave(H, rng, kind, scale)[:, None]
    m = np.clip(yy - top + 0.5, 0, 1) * np.clip(bot - yy + 0.5, 0, 1) * np.clip(xx - lef + 0.5, 0, 1) * np.clip(
        rig - xx + 0.5, 0, 1)
    return m.astype(np.float32)


def _wear(out, rng, box, amt, color=(0.96, 0.94, 0.9)):
    """Corner wear, tiny abrasions and the odd fibre - strongest at corners."""
    H, W = out.shape[:2]
    x0, y0, x1, y1 = box
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    corners = [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]
    for cx, cy in corners:
        for _ in range(int(40 * amt)):
            r = abs(rng.normal(0, 0.035)) * min(W, H)
            a = rng.uniform(0, 2 * math.pi)
            px, py = cx + math.cos(a) * r, cy + math.sin(a) * r
            s = rng.uniform(0.6, 2.6)
            d.ellipse([px - s, py - s, px + s, py + s], fill=int(rng.uniform(90, 230)))
    for _ in range(int(60 * amt)):  # dust specks across the whole print
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        s = rng.uniform(0.5, 1.8)
        d.ellipse([px - s, py - s, px + s, py + s], fill=int(rng.uniform(60, 180)))
    for _ in range(int(3 * amt)):  # fine hairline scratches
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        a = rng.uniform(0, math.pi)
        L = rng.uniform(30, 160)
        pts = [(px + math.cos(a) * t + rng.normal(0, 1.2), py + math.sin(a) * t + rng.normal(0, 1.2))
               for t in np.linspace(0, L, 8)]
        d.line(pts, fill=int(rng.uniform(50, 120)), width=1)
    m = np.asarray(im.filter(ImageFilter.GaussianBlur(0.6)), np.float32)[..., None] / 255.0
    return out * (1 - m) + np.asarray(color, np.float32) * m


def _crease(out, rng, box, amt=0.5):
    """A soft bent-corner crease: light ridge with a shadow beside it."""
    H, W = out.shape[:2]
    x0, y0, x1, y1 = box
    corner = rng.integers(4)
    cx = x0 if corner in (0, 2) else x1
    cy = y0 if corner in (0, 1) else y1
    L = rng.uniform(0.08, 0.16) * min(W, H)
    sx = 1 if cx == x0 else -1
    sy = 1 if cy == y0 else -1
    p0 = (cx + sx * L * rng.uniform(0.9, 1.4), cy)
    p1 = (cx, cy + sy * L * rng.uniform(0.9, 1.4))
    for off, val, col in ((0, 1, 1.0), (2.2, 1, 0.0)):
        im = Image.new('L', (W, H), 0)
        ImageDraw.Draw(im).line([(p0[0] + off * sx, p0[1] + off * sy), (p1[0] + off * sx, p1[1] + off * sy)],
                                fill=255, width=2)
        m = np.asarray(im.filter(ImageFilter.GaussianBlur(1.0)), np.float32)[..., None] / 255 * amt * 0.6
        out = out * (1 - m) + col * m
    return out


def _orange_digits(out, text, x, y, hgt):
    """Seven-segment, orange LED date imprint (1980s-90s point-and-shoot)."""
    H, W = out.shape[:2]
    segs = {'0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd', '6': 'afgedc',
            '7': 'abc', '8': 'abcdefg', '9': 'abcdfg'}
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    w = hgt * 0.5
    t = max(2, hgt * 0.11)
    sk = 0.12  # italic skew
    cx = x
    for ch in text:
        if ch == ' ':
            cx += w * 0.9
            continue
        if ch == "'":
            d.polygon([(cx, y), (cx + t, y), (cx - t * 0.5, y + hgt * 0.3)], fill=255)
            cx += w * 0.5
            continue
        P = lambda u, v: (cx + u * w + (hgt - v * hgt) * sk, y + v * hgt)
        seg = {'a': (P(0.1, 0), P(0.9, 0)), 'b': (P(1, 0.06), P(1, 0.46)), 'c': (P(1, 0.54), P(1, 0.94)),
               'd': (P(0.1, 1), P(0.9, 1)), 'e': (P(0, 0.54), P(0, 0.94)), 'f': (P(0, 0.06), P(0, 0.46)),
               'g': (P(0.1, 0.5), P(0.9, 0.5))}
        for s in segs.get(ch, ''):
            d.line(seg[s], fill=255, width=int(t))
        cx += w * 1.45
    m = np.asarray(im.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
    glow = gauss(m, hgt * 0.25)
    out = out + glow[..., None] * np.array([0.6, 0.22, 0.0]) * 0.8
    out = out * (1 - m[..., None] * 0.9) + m[..., None] * 0.9 * np.array([1.0, 0.58, 0.16])
    return np.clip(out, 0, 1)


def frame(photo, style, W, H, rng, stamp=None, wear=1.0, mono=True, studio=None):
    """Place a developed photo into its physical print and return the final RGB float image."""
    x0, y0, x1, y1 = frame_geometry(style, W, H)
    m = min(W, H)
    scale = m / 1200
    if style in ('glossy', 'digital', 'object', None):
        out = photo.copy()
        if style == 'glossy' and stamp:
            hgt = 0.036 * H
            out = _orange_digits(out, stamp, W - 0.06 * W - len(stamp) * hgt * 0.7, H - 0.075 * H - hgt, hgt)
        return out
    if style == 'cabinet':
        out = _paper(H, W, rng, (0.2, 0.18, 0.15), 0.06)
        # bevelled gilt edge around the window
        for inset, col, wdt in ((-14, (0.62, 0.5, 0.3), 3), (-7, (0.32, 0.27, 0.2), 2)):
            im = Image.new('L', (W, H), 0)
            ImageDraw.Draw(im).rectangle([x0 + inset * scale, y0 + inset * scale, x1 - inset * scale,
                                          y1 - inset * scale], outline=255, width=int(wdt * scale))
            mm = np.asarray(im.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[..., None] / 255
            out = out * (1 - mm) + np.asarray(col) * mm
        out[y0:y1, x0:x1] = photo
        # inner shadow of the window
        sh = np.zeros((H, W), np.float32)
        sh[y0:y1, x0:x1] = 1
        inner = 1 - gauss(1 - sh, 6 * scale)
        out *= (0.75 + 0.25 * inner)[..., None]
        if studio:
            im = Image.new('L', (W, H), 0)
            d = ImageDraw.Draw(im)
            d.text((W / 2, y1 + (H - y1) * 0.42), studio[0], font=font('roman_i', 0.042 * H), fill=255, anchor='mm')
            d.text((W / 2, y1 + (H - y1) * 0.7), studio[1], font=font('roman', 0.022 * H), fill=255, anchor='mm')
            mm = np.asarray(im.filter(ImageFilter.GaussianBlur(0.7)), np.float32)[..., None] / 255
            gold = np.array([0.66, 0.53, 0.3]) * (0.85 + 0.3 * fnoise(H, W, rng, (8, 32)))[..., None]
            out = out * (1 - mm * 0.85) + gold * mm * 0.85
        out = _wear(out, rng, (0, 0, W, H), 1.2 * wear, color=(0.42, 0.38, 0.32))
        out = _wear(out, rng, (x0, y0, x1, y1), 0.6 * wear)
        return np.clip(out, 0, 1)
    if style in ('deckle', 'scallop'):
        page = _paper(H, W, rng, (0.075, 0.07, 0.065) if style == 'deckle' else (0.16, 0.15, 0.135), 0.1)
        b = int(0.05 * m) if style == 'deckle' else int(0.055 * m)
        box = (x0 - b, y0 - b, x1 + b, y1 + b)
        pm = _print_mask(W, H, box, style, rng, scale)
        paper_col = (0.93, 0.9, 0.82) if mono else (0.95, 0.94, 0.91)
        pr = _paper(H, W, rng, paper_col, 0.025)
        # yellowing toward the print edge
        edge = gauss(1 - pm, 0.02 * m)
        pr = pr * (1 - 0.18 * edge[..., None] * np.array([0.3, 0.6, 1.4]))
        pr[y0:y1, x0:x1] = photo
        # drop shadow on the page
        shd = gauss(np.roll(np.roll(pm, int(4 * scale), 0), int(3 * scale), 1), 5 * scale)
        page *= (1 - 0.6 * shd)[..., None]
        out = page * (1 - pm[..., None]) + pr * pm[..., None]
        out = _wear(out, rng, box, 1.4 * wear)
        if rng.random() < 0.6 * wear:
            out = _crease(out, rng, box, 0.6)
        if style == 'deckle':  # black paper photo corners
            cs = int(0.085 * m)
            for (cx, cy, sx, sy) in ((box[0], box[1], 1, 1), (box[2], box[1], -1, 1), (box[0], box[3], 1, -1),
                                     (box[2], box[3], -1, -1)):
                ox, oy = cx - sx * 0.012 * m, cy - sy * 0.012 * m
                tri = [(ox, oy), (ox + sx * cs, oy), (ox, oy + sy * cs)]
                im = Image.new('L', (W, H), 0)
                ImageDraw.Draw(im).polygon(tri, fill=255)
                tm = np.asarray(im.filter(ImageFilter.GaussianBlur(0.8)), np.float32)
                sm = gauss(np.roll(np.roll(tm, int(2 * scale), 0), int(2 * scale), 1), 3 * scale) / 255
                out *= (1 - 0.5 * sm)[..., None]
                tm = tm[..., None] / 255
                out = out * (1 - tm) + np.array([0.055, 0.05, 0.048]) * tm
                # a hint of sheen along the hypotenuse
                im2 = Image.new('L', (W, H), 0)
                ImageDraw.Draw(im2).line([tri[1], tri[2]], fill=255, width=2)
                hm = np.asarray(im2.filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None] / 255
                out = out + hm * 0.06
        return np.clip(out, 0, 1)
    # plain bordered prints ('border' 1950s glossy, 'kodak' 1960s-70s)
    paper_col = (0.95, 0.945, 0.925) if style == 'border' else (0.955, 0.945, 0.91)
    out = _paper(H, W, rng, paper_col, 0.02)
    out[y0:y1, x0:x1] = photo
    if style == 'kodak' and stamp:
        im = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(im)
        d.text((x1 - 0.01 * W, (y1 + H) / 2), stamp, font=font('sans_b', 0.019 * m), fill=255, anchor='rm')
        mm = np.asarray(im.filter(ImageFilter.GaussianBlur(0.5)), np.float32)[..., None] / 255
        out = out * (1 - mm * 0.55) + np.array([0.4, 0.38, 0.36]) * mm * 0.55
    out = _wear(out, rng, (0, 0, W, H), 0.5 * wear)
    if rng.random() < 0.3 * wear:
        out = _crease(out, rng, (0, 0, W, H), 0.45)
    # slight sheen gradient of a glossy print under a scanner lamp
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    out = out * (0.985 + 0.03 * yy)
    return np.clip(out, 0, 1)


# ================================================================ scenes
# Palette: scenes are painted in natural colour; mono eras are converted later.
SKY = (0.72, 0.8, 0.88)
DRESS_ROSE = (0.72, 0.42, 0.45)


def baby(cv, x, y, h, gown=(0.96, 0.95, 0.92), skin=SKIN, hair=(0.62, 0.48, 0.32), blur=0.003):
    g = Group(cv)
    U = h * cv.H
    X, Y = x * cv.W, y * cv.H
    g.poly([(X - 0.13 * U, Y - 0.5 * U), (X + 0.13 * U, Y - 0.5 * U), (X + 0.38 * U, Y - 0.02 * U),
            (X - 0.38 * U, Y - 0.02 * U)], gown)
    g.ellipse(X, Y - 0.02 * U, 0.38 * U, 0.07 * U, gown)
    for s in (-1, 1):
        g.ellipse(X + s * 0.12 * U, Y + 0.03 * U, 0.06 * U, 0.04 * U, skin)
    g.ellipse(X, Y - 0.48 * U, 0.17 * U, 0.17 * U, gown)
    for s in (-1, 1):
        g.limb((X + s * 0.14 * U, Y - 0.56 * U), (X + s * 0.2 * U, Y - 0.33 * U), 0.1 * U, 0.08 * U, gown)
        g.ellipse(X + s * 0.17 * U, Y - 0.28 * U, 0.05 * U, 0.05 * U, skin)
    g.ellipse(X, Y - 0.6 * U, 0.06 * U, 0.04 * U, shade(skin, 0.95))
    g.ellipse(X, Y - 0.79 * U, 0.155 * U, 0.165 * U, skin)
    g.ellipse(X - 0.02 * U, Y - 0.92 * U, 0.1 * U, 0.04 * U, hair)
    for s in (-1, 1):
        g.ellipse(X + s * 0.05 * U, Y - 0.8 * U, 0.025 * U, 0.015 * U, shade(skin, 0.88))
    g.commit(blur=blur, light=(-0.8, -0.6), shade_amt=0.35, rim=0.25)


def chair_rocker(cv, x, y, h, col=(0.3, 0.22, 0.15), facing=1):
    g = Group(cv)
    U = h * cv.H
    X, Y = x * cv.W, y * cv.H
    f = facing
    g.limb((X - f * 0.12 * U, Y - 0.3 * U), (X - f * 0.2 * U, Y - 0.95 * U), 0.03 * U, 0.03 * U, col)
    g.limb((X - f * 0.02 * U, Y - 0.3 * U), (X - f * 0.08 * U, Y - 0.95 * U), 0.03 * U, 0.03 * U, col)
    for t in np.linspace(0.45, 0.9, 5):
        g.limb((X - f * (0.12 + 0.1 * t) * U, Y - t * U), (X - f * (0.02 + 0.08 * t) * U, Y - t * U), 0.025 * U,
               0.025 * U, col)
    g.rect(X - 0.18 * U, Y - 0.33 * U, X + 0.2 * U, Y - 0.29 * U, col)
    for lx in (-0.14, 0.16):
        g.limb((X + lx * U, Y - 0.3 * U), (X + lx * U, Y - 0.05 * U), 0.03 * U, 0.03 * U, col)
    pts = [(X + t * U, Y - 0.04 * U + (t * t) * 0.25 * U) for t in np.linspace(-0.32, 0.32, 12)]
    g.line(pts, 0.03 * U, col)
    g.commit(blur=0.003, shade_amt=0.2, rim=0.1)


def sc_june_baby(cv):
    cv.vgrad([(0, (0.42, 0.38, 0.33)), (0.7, (0.55, 0.5, 0.43)), (1, (0.35, 0.3, 0.25))])
    cv.glow(0.48, 0.38, 0.28, (0.35, 0.32, 0.27), 0.9)
    cv.noise_tint((0.25, 0.22, 0.2), 0.35, (3, 7, 14))
    cv.ellipse(0.62, 0.25, 0.25, 0.18, (0.3, 0.3, 0.28), blur=0.08, alpha=0.4)  # painted foliage on backdrop
    cv.ellipse(0.2, 0.55, 0.2, 0.3, (0.28, 0.26, 0.23), blur=0.08, alpha=0.5)
    cv.blur(0.01)
    # draped table / cushion with a fur throw
    cv.rect(0, 0.7, 1, 1, (0.3, 0.26, 0.22), blur=0.01)
    cv.ellipse(0.5, 0.8, 0.5, 0.12, (0.78, 0.74, 0.68), blur=0.012)
    for i in range(70):
        x = cv.rng.uniform(0.1, 0.9)
        cv.line([(x, 0.76 + cv.rng.uniform(0, 0.08)), (x + cv.rng.uniform(-0.03, 0.03), 0.9 + cv.rng.uniform(0, 0.05))],
                0.006, (0.88, 0.85, 0.8), blur=0.004, alpha=0.35)
    cv.ellipse(0.5, 0.88, 0.48, 0.05, (0.2, 0.17, 0.14), blur=0.03, alpha=0.5)
    shadow(cv, 0.52, 0.79, 0.24, 0.03, 0.4, 0.015)
    baby(cv, 0.5, 0.78, 0.5)


def mesa_ridge(cv, base, amp, col, haze=(0.75, 0.75, 0.85), hz=0.0, blur=0.003, seed_off=0, stripe=0.14,
               freq=160, steps=140, shadow_col=None):
    rng = np.random.default_rng(zlib.crc32(b'mesa') + seed_off)
    xs = np.linspace(-0.02, 1.02, steps)
    v = np.cumsum(rng.normal(0, 1, steps))
    v = np.convolve(v - v.mean(), np.ones(5) / 5, 'same')
    v = v / (np.abs(v).max() + 1e-6)
    q = np.round(v * 2.5) / 2.5
    prof = 0.7 * q + 0.3 * v
    prof = np.convolve(prof, np.ones(3) / 3, 'same')
    pts = [(xx, base - amp * (0.5 + 0.5 * pp)) for xx, pp in zip(xs, prof)] + [(1.02, 1.05), (-0.02, 1.05)]
    m = cv.mask(lambda d: d.polygon(cv.P(pts), fill=255), blur)
    n = fnoise(cv.H, cv.W, rng, (2, 5, 11))
    stripes = 0.5 + 0.5 * np.sin(cv.yy * freq + n * 7)
    clefts = fnoise(cv.H, cv.W, rng, (3, 8, 16), aspect=cv.aspect * 5)
    field = np.asarray(col, np.float32)[None, None] * (1 - stripe * stripes)[..., None]
    field *= (0.7 + 0.45 * clefts)[..., None]
    # the faces of the cliffs fall into shade below each rim
    ytop = np.interp(cv.xx[0], xs, [p[1] for p in pts[:steps]])[None, :]
    depth = np.clip((cv.yy - ytop) / (amp * 2.0), 0, 1)
    field *= (1.05 - 0.35 * depth)[..., None]
    field = field * (1 - hz) + np.asarray(haze, np.float32) * hz
    cv.apply(m, field)


def sc_grand_canyon(cv):
    cv.vgrad([(0, (0.25, 0.45, 0.72)), (0.28, (0.55, 0.68, 0.82)), (0.4, (0.82, 0.83, 0.85))])
    clouds(cv, 5, 0.04, 0.22, (1, 1, 1), 0.6, size=0.09)
    haze = (0.78, 0.76, 0.84)
    layers = [(0.4, 0.05, (0.75, 0.6, 0.55), 0.75, 0.004), (0.47, 0.08, (0.8, 0.56, 0.42), 0.55, 0.0035),
              (0.55, 0.11, (0.82, 0.52, 0.34), 0.38, 0.003), (0.66, 0.14, (0.78, 0.45, 0.27), 0.2, 0.0025),
              (0.8, 0.16, (0.68, 0.38, 0.22), 0.06, 0.002)]
    for i, (b, amp, col, hz, bl) in enumerate(layers):
        mesa_ridge(cv, b, amp, col, haze, hz, bl, seed_off=i * 7 + 3, freq=120 + i * 40)
    cv.blur(0.0015)
    # foreground: rock ledge, pipe railing, the family looking out (seen from behind)
    mesa_ridge(cv, 0.93, 0.05, (0.42, 0.3, 0.2), blur=0.006, seed_off=99, stripe=0.05, freq=60)
    cv.rect(0, 0.775, 1, 0.783, (0.32, 0.32, 0.3), blur=0.002)
    for x in np.arange(0.03, 1, 0.14):
        cv.rect(x, 0.775, x + 0.005, 0.92, (0.3, 0.3, 0.29), blur=0.002)
    L = (-0.9, -0.4)
    fam = [(0.33, 0.95, 0.36, dict(top=(0.88, 0.86, 0.8), bottom=(0.55, 0.5, 0.4), hairstyle='short',
                                   arms=(4, (60, 70)), short_sleeves=True)),
           (0.4, 0.955, 0.33, dict(top=(0.3, 0.55, 0.55), bottom=(0.85, 0.82, 0.75), hairstyle='wave',
                                   hat='scarf', hat_col=(0.85, 0.75, 0.55), hair=(0.35, 0.22, 0.12))),
           (0.5, 0.96, 0.31, dict(top=(0.82, 0.55, 0.58), dress='knee', hairstyle='long', hair=(0.42, 0.28, 0.15))),
           (0.585, 0.97, 0.27, dict(top=(0.7, 0.25, 0.2), bottom=(0.3, 0.32, 0.45), child=True, hairstyle='short',
                                    hair=(0.3, 0.2, 0.12), hat='cap', hat_col=(0.2, 0.3, 0.5))),
           (0.65, 0.975, 0.22, dict(top=(0.88, 0.78, 0.35), dress='knee', child=True, hairstyle='bob',
                                    hair=(0.55, 0.4, 0.22)))]
    for x, yb, h, kw in fam:
        shadow(cv, x + 0.03, yb, 0.06, 0.012, 0.35, 0.01)
        person(cv, x, yb, h, light=L, rim=0.45, blur=0.0035, view='back', **kw)


def balloon(cv, x, y, r, col, string_to=None):
    if string_to:
        cv.line([(x, y + r), string_to], 0.002, (0.9, 0.9, 0.9), blur=0.002, alpha=0.6)
    g = Group(cv)
    g.ellipse(x * cv.W, y * cv.H, r * cv.H * 0.88, r * cv.H, col)
    g.commit(blur=0.004, light=(-0.6, -0.7), shade_amt=0.45, rim=0.0)
    cv.ellipse(x - r * 0.3 / cv.aspect, y - r * 0.4, r * 0.18, r * 0.25, (1, 1, 1), blur=r * 0.15, alpha=0.6)


# ================================================================ pipeline
def render(spec):
    W, H = ORIENT[spec['orient']]
    seed = zlib.crc32(spec['id'].encode())
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = frame_geometry(spec['frame'], W, H)
    pw, ph = x1 - x0, y1 - y0
    rs = spec.get('rs', RENDER_SCALE)
    cv = Canvas(round(pw * rs), round(ph * rs), seed)
    spec['scene'](cv)
    a = cv.a if rs == 1 else resize_f(cv.a, pw, ph)
    a = develop(a, spec['era'], rng)
    out = frame(a, spec['frame'], W, H, rng, stamp=spec.get('stamp'), wear=spec.get('wear', 1.0),
                mono=spec['era'] in ('sepia', 'silver', 'bw50'), studio=spec.get('studio'))
    return to_img(out)


# ---------------------------------------------------------------- prop helpers
def box(cv, x0, y0, x1, y1, col, blur=0.003, light=(-0.6, -0.7), r=0.0, ao=0.25, tex=0.06, shade_amt=0.25, rim=0.1,
        alpha=1.0):
    g = Group(cv)
    g.rect(x0 * cv.W, y0 * cv.H, x1 * cv.W, y1 * cv.H, col, r=r * cv.H)
    g.commit(blur=blur, light=light, ao=ao, tex=tex, shade_amt=shade_amt, rim=rim, round_=0, alpha=alpha)


def blob(cv, x, y, rx, ry, col, blur=0.003, light=(-0.6, -0.7), ao=0.4, tex=0.08, shade_amt=0.35, rim=0.15,
         alpha=1.0):
    g = Group(cv)
    g.ellipse(x * cv.W, y * cv.H, rx * cv.H, ry * cv.H, col)
    g.commit(blur=blur, light=light, ao=ao, tex=tex, shade_amt=shade_amt, rim=rim, round_=0, alpha=alpha)


def shapes(cv, polys, col, blur=0.003, light=(-0.6, -0.7), ao=0.25, tex=0.08, shade_amt=0.25, rim=0.1, round_=0.0,
           alpha=1.0):
    g = Group(cv)
    for pts in polys:
        g.poly(cv.P(pts), col)
    g.commit(blur=blur, light=light, ao=ao, tex=tex, shade_amt=shade_amt, rim=rim, round_=round_, alpha=alpha)


def light_field(cv, cx, cy, r, lo=0.45, power=1.6):
    """Multiply the scene by a soft pool of light (flash fall-off, window light)."""
    dx = (cv.xx - cx) * cv.aspect
    dy = cv.yy - cy
    d = np.sqrt(dx * dx + dy * dy) / r
    f = lo + (1 - lo) * np.clip(1 - d, 0, 1) ** power
    cv.a *= f[..., None]


def window_frame(cv, x0, y0, x1, y1, glass, trim=(0.92, 0.9, 0.86), panes=(2, 2), blur=0.003, glow=0.0):
    cv.rect(x0 - 0.012, y0 - 0.012 * cv.aspect, x1 + 0.012, y1 + 0.012 * cv.aspect, trim, blur=blur)
    g = cv.vgrad([(y0, glass), (y1, shade(glass, 0.75))], apply=False)
    cv.rect(x0, y0, x1, y1, g, blur=blur)
    if glow:
        cv.glow((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * cv.aspect * 0.6, glass, glow)
    for i in range(1, panes[0]):
        x = x0 + (x1 - x0) * i / panes[0]
        cv.line([(x, y0), (x, y1)], 0.006, trim, blur=blur)
    for i in range(1, panes[1]):
        y = y0 + (y1 - y0) * i / panes[1]
        cv.line([(x0, y), (x1, y)], 0.006, trim, blur=blur)


def siding(cv, x0, y0, x1, y1, col, gap=0.03, dark=0.7, alpha=0.5):
    for y in np.arange(y0 + gap, y1, gap):
        cv.line([(x0, y), (x1, y)], 0.0035, shade(col, dark), blur=0.0015, alpha=alpha)


def bungalow(cv, x0, x1, yb, wall_h, roof_h, wall=(0.86, 0.85, 0.8), roof=(0.3, 0.28, 0.27), trim=(0.95, 0.94, 0.9),
             blur=0.003, light=(-0.7, -0.5), door_col=(0.35, 0.25, 0.2), glass=(0.35, 0.4, 0.45)):
    yt = yb - wall_h
    box(cv, x0, yt, x1, yb, wall, blur=blur, light=light, ao=0.12, tex=0.05)
    siding(cv, x0, yt, x1, yb, wall)
    mx = (x0 + x1) / 2
    ov = 0.03
    shapes(cv, [[(x0 - ov, yt + 0.01), (mx, yt - roof_h), (x1 + ov, yt + 0.01)]], roof, blur=blur, light=light,
           ao=0.1, tex=0.15)
    cv.poly([(x0 - ov, yt + 0.01), (x1 + ov, yt + 0.01), (x1 - 0.02, yt + 0.04), (x0 + 0.02, yt + 0.04)], (0, 0, 0),
            blur=0.01, alpha=0.35)  # eave shadow
    w = x1 - x0
    window_frame(cv, x0 + w * 0.1, yb - wall_h * 0.72, x0 + w * 0.3, yb - wall_h * 0.3, glass, trim, blur=blur)
    window_frame(cv, x1 - w * 0.3, yb - wall_h * 0.72, x1 - w * 0.1, yb - wall_h * 0.3, glass, trim, blur=blur)
    box(cv, mx - w * 0.06, yb - wall_h * 0.78, mx + w * 0.06, yb, door_col, blur=blur, light=light)
    cv.ellipse(mx + w * 0.04, yb - wall_h * 0.4, 0.006, 0.006, (0.85, 0.75, 0.4), blur=0.002)


def ground_tex(cv, y0, col, amt=0.18, scales=(4, 10, 30)):
    n = fnoise(cv.H, cv.W, cv.rng, scales, aspect=cv.aspect * 2.5)
    m = np.clip((cv.yy - y0) * 200, 0, 1)
    cv.a *= (1 - m * amt + m * amt * 2 * n)[..., None]


def shrub(cv, x, y, r, col=(0.22, 0.3, 0.18), blur=0.004, n=7, light=(-0.6, -0.7)):
    g = Group(cv)
    for _ in range(n):
        g.ellipse((x + cv.rng.uniform(-r, r) / cv.aspect) * cv.W, (y - cv.rng.uniform(0, r * 0.8)) * cv.H,
                  r * cv.H * cv.rng.uniform(0.4, 0.7), r * cv.H * cv.rng.uniform(0.35, 0.6),
                  shade(col, cv.rng.uniform(0.85, 1.15)))
    g.commit(blur=blur, light=light, ao=0.45, tex=0.2, shade_amt=0.4, rim=0.12, round_=0.003)


# ================================================================ beginnings
def sc_june_baby(cv):
    cv.vgrad([(0, (0.42, 0.38, 0.33)), (0.7, (0.55, 0.5, 0.43)), (1, (0.35, 0.3, 0.25))])
    cv.glow(0.45, 0.35, 0.3, (0.35, 0.32, 0.27), 1.0)
    cv.noise_tint((0.25, 0.22, 0.2), 0.35, (3, 7, 14))
    cv.ellipse(0.7, 0.22, 0.25, 0.2, (0.28, 0.28, 0.26), blur=0.07, alpha=0.5)  # painted foliage on the backdrop
    cv.ellipse(0.15, 0.5, 0.2, 0.3, (0.28, 0.26, 0.23), blur=0.07, alpha=0.5)
    cv.blur(0.01)
    # draped table with a fur throw
    cv.rect(0, 0.68, 1, 1, (0.3, 0.26, 0.22), blur=0.012)
    blob(cv, 0.5, 0.8, 0.52, 0.13, (0.8, 0.76, 0.7), blur=0.008, ao=0.5, tex=0.2)
    for i in range(90):
        x = cv.rng.uniform(0.05, 0.95)
        y = 0.73 + cv.rng.uniform(0, 0.1)
        cv.line([(x, y), (x + cv.rng.uniform(-0.03, 0.03), y + cv.rng.uniform(0.04, 0.09))],
                0.005, (0.9, 0.87, 0.82), blur=0.004, alpha=0.3)
    shadow(cv, 0.53, 0.79, 0.22, 0.03, 0.45, 0.015)
    baby(cv, 0.5, 0.79, 0.48)
    light_field(cv, 0.42, 0.5, 0.75, 0.55, 1.2)


def baby(cv, x, y, h, gown=(0.93, 0.92, 0.88), skin=SKIN, hair=(0.4, 0.3, 0.2), blur=0.0035):
    g = Group(cv)
    U = h * cv.H
    X, Y = x * cv.W, y * cv.H
    g.poly([(X - 0.12 * U, Y - 0.5 * U), (X + 0.12 * U, Y - 0.5 * U), (X + 0.36 * U, Y - 0.04 * U),
            (X + 0.3 * U, Y), (X - 0.33 * U, Y), (X - 0.37 * U, Y - 0.04 * U)], gown)
    g.ellipse(X - 0.02 * U, Y - 0.02 * U, 0.36 * U, 0.06 * U, gown)
    g.ellipse(X + 0.1 * U, Y + 0.02 * U, 0.055 * U, 0.035 * U, skin)
    g.ellipse(X - 0.13 * U, Y + 0.025 * U, 0.05 * U, 0.03 * U, skin)
    g.ellipse(X, Y - 0.46 * U, 0.17 * U, 0.17 * U, gown)
    g.limb((X - 0.14 * U, Y - 0.55 * U), (X - 0.12 * U, Y - 0.3 * U), 0.1 * U, 0.085 * U, gown)
    g.ellipse(X - 0.08 * U, Y - 0.27 * U, 0.045 * U, 0.04 * U, skin)
    g.limb((X + 0.14 * U, Y - 0.55 * U), (X + 0.22 * U, Y - 0.38 * U), 0.1 * U, 0.085 * U, gown)
    g.ellipse(X + 0.24 * U, Y - 0.34 * U, 0.045 * U, 0.042 * U, skin)
    g.ellipse(X, Y - 0.6 * U, 0.07 * U, 0.04 * U, shade(skin, 0.95))
    g.ellipse(X + 0.01 * U, Y - 0.78 * U, 0.15 * U, 0.16 * U, skin)
    g.ellipse(X - 0.02 * U, Y - 0.9 * U, 0.11 * U, 0.05 * U, hair)
    g.commit(blur=blur, light=(-0.8, -0.6), shade_amt=0.35, rim=0.25, round_=0.012, ao=0.35, tex=0.1)


def sc_rose_porch(cv):
    r = cv.rng
    cv.vgrad([(0, (0.92, 0.93, 0.9)), (0.55, (0.82, 0.84, 0.78)), (1, (0.58, 0.62, 0.42))])
    for i in range(6):
        tree(cv, 0.62 + i * 0.08, 0.64, 0.5 + r.uniform(-0.1, 0.1), crown=(0.5, 0.58, 0.42), blur=0.01)
    cv.rect(0.55, 0.62, 1, 1, (0.65, 0.7, 0.5), blur=0.01)
    cv.blur(0.014)
    # house wall (left), clapboard
    box(cv, -0.02, 0, 0.6, 1, (0.66, 0.64, 0.6), light=(1, -0.3), ao=0.0, tex=0.12, shade_amt=0.25, blur=0.002)
    siding(cv, 0, 0.0, 0.6, 0.82, (0.66, 0.64, 0.6), gap=0.036, dark=0.6, alpha=0.6)
    box(cv, 0.06, 0.16, 0.22, 0.8, (0.14, 0.12, 0.1), blur=0.003)  # door
    cv.rect(0.075, 0.19, 0.205, 0.43, (0.42, 0.4, 0.37), alpha=0.6, blur=0.003)
    window_frame(cv, 0.3, 0.2, 0.48, 0.5, (0.3, 0.3, 0.32), trim=(0.85, 0.84, 0.8))
    cv.rect(0.3, 0.2, 0.48, 0.5, (0.9, 0.9, 0.86), alpha=0.18, blur=0.02)  # lace curtain
    # porch ceiling shadow & floor
    cv.rect(-0.02, -0.02, 1.02, 0.09, (0.22, 0.2, 0.18), blur=0.006)
    cv.poly([(0, 0.79), (1, 0.81), (1, 1), (0, 1)], (0.46, 0.43, 0.39), blur=0.002)
    for x in np.arange(-0.2, 1.2, 0.045):
        cv.line([(0.5 + (x - 0.5) * 0.75, 0.8), (0.5 + (x - 0.5) * 1.5, 1)], 0.003, (0.3, 0.28, 0.25), alpha=0.45)
    cv.ellipse(0.75, 0.86, 0.35, 0.05, (0.85, 0.83, 0.75), blur=0.04, alpha=0.3)  # light spilling onto boards
    for x in (0.585, 0.975):
        box(cv, x - 0.022, 0.05, x + 0.022, 0.81, (0.88, 0.86, 0.82), light=(1, 0), shade_amt=0.4, ao=0.2)
    box(cv, 0.6, 0.5, 0.96, 0.525, (0.86, 0.84, 0.8), blur=0.003)
    box(cv, 0.6, 0.745, 0.96, 0.76, (0.86, 0.84, 0.8), blur=0.003)
    for x in np.arange(0.62, 0.95, 0.03):
        cv.rect(x, 0.52, x + 0.009, 0.75, (0.84, 0.82, 0.78), blur=0.002)
    # potted geranium on the boards
    box(cv, 0.035, 0.74, 0.1, 0.83, (0.55, 0.38, 0.28), r=0.005)
    shrub(cv, 0.068, 0.74, 0.06, col=(0.3, 0.38, 0.25))
    # chair back (behind her)
    for xx in (0.36, 0.48):
        cv.line([(xx, 0.4), (xx - 0.004, 0.84)], 0.012, (0.25, 0.18, 0.12), blur=0.003)
    for yy in (0.42, 0.47, 0.52):
        cv.line([(0.36, yy), (0.48, yy)], 0.01, (0.28, 0.2, 0.14), blur=0.003)
    shadow(cv, 0.43, 0.86, 0.17, 0.025, 0.55)
    cv.line([(0.33, 0.86), (0.43, 0.875), (0.53, 0.86)], 0.01, (0.25, 0.18, 0.12), blur=0.003)  # rocker
    g, _ = person(cv, 0.42, 0.855, 0.6, top=(0.2, 0.18, 0.2), dress='long', hairstyle='bun', hair=(0.72, 0.7, 0.67),
                  pose='sitfront', arms=((8, -55), (8, -60)), skin=SKIN_OLD, commit=False, turn=1.0)
    U = 0.6 * cv.H
    X, Y = 0.42 * cv.W, 0.855 * cv.H
    g.poly([(X - 0.08 * U, Y - 0.35 * U), (X + 0.08 * U, Y - 0.35 * U), (X + 0.1 * U, Y - 0.06 * U),
            (X - 0.1 * U, Y - 0.06 * U)], (0.84, 0.82, 0.77))  # apron
    g.commit(blur=0.0045, light=(0.9, -0.3), rim=0.3, round_=0.006)


def sc_hale_farm(cv):
    r = cv.rng
    cv.vgrad([(0, (0.45, 0.55, 0.7)), (0.5, (0.85, 0.87, 0.88)), (0.56, (0.9, 0.9, 0.88))])
    clouds(cv, 7, 0.08, 0.35, (1, 1, 1), 0.8, blur=0.025, size=0.1)
    treeline(cv, 0.57, 0.05, (0.3, 0.36, 0.28), blur=0.006, n=50)
    cv.rect(0, 0.565, 1, 1, (0.62, 0.6, 0.42))
    ground_tex(cv, 0.565, (0, 0, 0), 0.2)
    # furrows converging
    for k in np.linspace(-1.5, 2.5, 34):
        cv.line([(0.62 + (k - 0.5) * 0.02, 0.6), (0.5 + (k - 0.5) * 0.9, 1.05)], 0.004, (0.38, 0.35, 0.25),
                blur=0.003, alpha=0.5)
    cv.rect(0, 0.565, 1, 0.62, (0.55, 0.58, 0.42), alpha=0.8, blur=0.006)
    # barn
    bx0, bx1, by = 0.2, 0.48, 0.6
    box(cv, bx0, 0.38, bx1, by, (0.55, 0.3, 0.25), light=(-1, -0.2), shade_amt=0.3, tex=0.1)
    for x in np.arange(bx0 + 0.01, bx1, 0.012):
        cv.line([(x, 0.38), (x, by)], 0.002, (0.3, 0.16, 0.12), alpha=0.5)
    mx = (bx0 + bx1) / 2
    shapes(cv, [[(bx0 - 0.015, 0.39), (bx0 + 0.02, 0.29), (mx, 0.24), (bx1 - 0.02, 0.29), (bx1 + 0.015, 0.39)]],
           (0.3, 0.28, 0.27), light=(-1, -0.3), tex=0.2)
    box(cv, mx - 0.045, 0.45, mx + 0.045, by, (0.3, 0.16, 0.12))
    for a, b in (((mx - 0.045, 0.45), (mx + 0.045, by)), ((mx + 0.045, 0.45), (mx - 0.045, by))):
        cv.line([a, b], 0.005, (0.88, 0.86, 0.8), blur=0.002)
    cv.rect(mx - 0.05, 0.445, mx + 0.05, 0.452, (0.88, 0.86, 0.8))
    cv.rect(mx - 0.02, 0.3, mx + 0.02, 0.35, (0.2, 0.12, 0.1))  # hay door
    # silo
    box(cv, 0.5, 0.25, 0.56, by, (0.7, 0.68, 0.64), light=(-1, -0.2), shade_amt=0.5, ao=0.3)
    blob(cv, 0.53, 0.25, 0.034, 0.03, (0.6, 0.6, 0.6), shade_amt=0.5)
    for y in np.arange(0.27, by, 0.025):
        cv.line([(0.5, y), (0.56, y)], 0.002, (0.45, 0.43, 0.4), alpha=0.6)
    # windmill
    wx = 0.78
    for a, b in (((wx - 0.03, by + 0.01), (wx - 0.004, 0.2)), ((wx + 0.03, by + 0.01), (wx + 0.004, 0.2))):
        cv.line([a, b], 0.004, (0.3, 0.3, 0.3), blur=0.002)
    for y in np.arange(0.28, 0.6, 0.06):
        t = (y - 0.2) / 0.4
        cv.line([(wx - 0.004 - 0.026 * t, y), (wx + 0.004 + 0.026 * t, y)], 0.0025, (0.3, 0.3, 0.3), blur=0.002)
    for k in range(18):
        a = k * math.pi / 9
        cv.line([(wx, 0.19), (wx + math.cos(a) * 0.05 / cv.aspect, 0.19 + math.sin(a) * 0.05)], 0.004,
                (0.32, 0.32, 0.32), blur=0.002)
    cv.poly([(wx, 0.19), (wx + 0.08, 0.17), (wx + 0.08, 0.21)], (0.32, 0.32, 0.32), blur=0.002)
    tree(cv, 0.1, 0.6, 0.38, crown=(0.28, 0.34, 0.22), blur=0.004)
    tree(cv, 0.93, 0.61, 0.3, crown=(0.3, 0.36, 0.24), blur=0.004)
    # fence posts receding at right
    for i in range(9):
        t = i / 8
        x = 0.98 - t * 0.3
        y = 0.98 - t * 0.33
        hgt = 0.2 * (1 - t * 0.85)
        cv.rect(x - 0.006 * (1 - t * 0.8), y - hgt, x + 0.006 * (1 - t * 0.8), y, (0.35, 0.3, 0.25), blur=0.002)
    cv.line([(0.98, 0.84), (0.68, 0.635)], 0.003, (0.3, 0.3, 0.3), blur=0.002)
    cv.line([(0.98, 0.9), (0.68, 0.645)], 0.003, (0.3, 0.3, 0.3), blur=0.002)
    person(cv, 0.6, 0.62, 0.07, top=(0.4, 0.45, 0.55), hat='fedora', blur=0.003)


def sc_boys_fence(cv):
    r = cv.rng
    cv.vgrad([(0, (0.85, 0.87, 0.86)), (0.5, (0.8, 0.82, 0.76)), (1, (0.62, 0.62, 0.48))])
    tree(cv, 0.75, 0.62, 0.75, crown=(0.4, 0.45, 0.32), blur=0.012, spread=1.4, n=20)
    treeline(cv, 0.58, 0.07, (0.55, 0.6, 0.45), blur=0.015)
    cv.rect(0, 0.57, 1, 1, (0.68, 0.68, 0.5), blur=0.01)
    ground_tex(cv, 0.58, None, 0.15)
    cv.blur(0.012)
    # rail fence
    for x in (0.08, 0.5, 0.92):
        box(cv, x - 0.012, 0.42, x + 0.012, 0.9, (0.45, 0.38, 0.3), light=(-1, -0.3), shade_amt=0.4, tex=0.2)
    for y in (0.5, 0.66):
        box(cv, -0.02, y, 1.02, y + 0.03, (0.52, 0.45, 0.36), light=(0, -1), shade_amt=0.4, tex=0.25)
    # two boys sitting on the top rail
    boys = [(0.36, dict(top=(0.82, 0.8, 0.74), bottom=(0.35, 0.38, 0.45), hair=(0.25, 0.18, 0.12), hat='cap',
                        hat_col=(0.3, 0.28, 0.25), arms=(10, (5, -50)))),
            (0.56, dict(top=(0.5, 0.48, 0.45), bottom=(0.4, 0.36, 0.3), hair=(0.6, 0.45, 0.28),
                        arms=((5, -40), 20)))]
    for x, kw in boys:
        person(cv, x, 0.8, 0.48, child=True, pose='sitfront', blur=0.0045, light=(-0.8, -0.6), rim=0.3, **kw)
    # dog sitting below
    shadow(cv, 0.24, 0.92, 0.07, 0.015, 0.4)
    dog(cv, 0.22, 0.92, 0.16, col=(0.3, 0.24, 0.18), facing=1, sit=True).commit(blur=0.005, round_=0.006,
                                                                                 light=(-0.8, -0.6))


def sc_walter_uniform(cv):
    cv.vgrad([(0, (0.52, 0.5, 0.47)), (1, (0.3, 0.29, 0.28))])
    cv.glow(0.62, 0.3, 0.3, (0.32, 0.31, 0.29), 1.0)
    cv.noise_tint((0.2, 0.2, 0.2), 0.25, (2, 5))
    cv.rect(-0.05, -0.05, 0.22, 1.05, (0.22, 0.2, 0.19), blur=0.03, alpha=0.8)  # studio drape
    for x in (0.03, 0.09, 0.15):
        cv.line([(x, 0), (x + 0.02, 1)], 0.02, (0.35, 0.33, 0.31), blur=0.02, alpha=0.5)
    cv.blur(0.02)
    # a draped pedestal he rests his hand on
    box(cv, 0.72, 0.68, 0.95, 1.02, (0.35, 0.33, 0.3), light=(-1, -0.4), shade_amt=0.4, ao=0.35, tex=0.15)
    blob(cv, 0.835, 0.68, 0.1, 0.025, (0.42, 0.4, 0.37), shade_amt=0.4)
    olive = (0.47, 0.44, 0.33)
    h, fy = 1.0, 1.1
    g, _ = person(cv, 0.5, fy, h, top=olive, bottom=olive, hat='garrison', hat_col=shade(olive, 0.9),
                  arms=(4, (25, 40)), commit=False, turn=1.4, facing=-1, hair=(0.18, 0.13, 0.09))
    U = h * cv.H
    X = 0.5 * cv.W
    shY = fy * cv.H - (0.48 + 0.335) * U
    g.poly([(X - 0.024 * U, shY - 0.012 * U), (X + 0.024 * U, shY - 0.012 * U), (X + 0.01 * U, shY + 0.13 * U),
            (X - 0.01 * U, shY + 0.13 * U)], (0.72, 0.69, 0.58))  # shirt & tie
    g.poly([(X - 0.007 * U, shY), (X + 0.007 * U, shY), (X + 0.005 * U, shY + 0.13 * U),
            (X - 0.005 * U, shY + 0.13 * U)], (0.33, 0.3, 0.22))
    for sx in (-1, 1):
        g.rect(X + sx * 0.055 * U - 0.025 * U, shY + 0.07 * U, X + sx * 0.055 * U + 0.025 * U, shY + 0.087 * U,
               shade(olive, 0.82))
    for k in range(3):
        g.ellipse(X, shY + 0.18 * U + k * 0.055 * U, 0.005 * U, 0.005 * U, (0.72, 0.64, 0.42))
    g.commit(blur=0.0045, light=(-0.9, -0.5), rim=0.35, shade_amt=0.45, round_=0.005, ao=0.4)
    light_field(cv, 0.45, 0.32, 0.9, 0.55, 1.0)


# ================================================================ Walter & June
def veil(cv, x, y_head, y_floor, w, alpha=0.55):
    pts = [(x - 0.02, y_head), (x + 0.02, y_head), (x + w, y_floor), (x - w * 0.6, y_floor)]
    cv.poly(pts, (0.97, 0.97, 0.95), blur=0.01, alpha=alpha)


def sc_wedding(cv):
    cv.fill((0.72, 0.7, 0.66))
    # stone blocks
    for row, y in enumerate(np.arange(0, 0.75, 0.05)):
        off = 0.06 if row % 2 else 0
        for x in np.arange(-0.1 + off, 1.1, 0.12):
            cv.rect(x + 0.003, y + 0.003, x + 0.117, y + 0.047, shade((0.74, 0.72, 0.68), cv.rng.uniform(0.9, 1.08)),
                    blur=0.002)
    cv.noise_tint((0.5, 0.48, 0.45), 0.3)
    # arched doorway
    cv.rect(0.22, 0.2, 0.78, 0.8, (0.6, 0.58, 0.55), blur=0.002)
    cv.ellipse(0.5, 0.2, 0.21, 0.16, (0.6, 0.58, 0.55), blur=0.002)
    cv.rect(0.27, 0.22, 0.73, 0.8, (0.1, 0.09, 0.09), blur=0.002)
    cv.ellipse(0.5, 0.22, 0.17, 0.13, (0.1, 0.09, 0.09), blur=0.002)
    cv.line([(0.5, 0.1), (0.5, 0.8)], 0.006, (0.2, 0.18, 0.17), blur=0.002)
    cv.blur(0.006)
    # steps
    for i, y in enumerate((0.78, 0.84, 0.9, 0.96)):
        box(cv, -0.02, y, 1.02, y + 0.065, shade((0.8, 0.78, 0.74), 1 - i * 0.03), light=(0, -1), tex=0.1, ao=0.1)
        cv.rect(-0.02, y + 0.055, 1.02, y + 0.066, (0.3, 0.3, 0.3), blur=0.004, alpha=0.4)
    # the couple
    veil(cv, 0.6, 0.28, 0.9, 0.17, 0.5)
    shadow(cv, 0.52, 0.86, 0.25, 0.02, 0.45)
    g, _ = person(cv, 0.4, 0.86, 0.62, top=(0.13, 0.13, 0.15), hairstyle='short', hair=(0.15, 0.1, 0.07),
                  arms=(6, (-8, -40)), commit=False, turn=0.8, facing=1)
    U = 0.62 * cv.H
    g.ellipse(0.4 * cv.W - 0.06 * U, 0.86 * cv.H - 0.74 * U, 0.012 * U, 0.012 * U, (0.95, 0.95, 0.95))
    g.poly([(0.4 * cv.W - 0.015 * U, 0.86 * cv.H - 0.82 * U), (0.4 * cv.W + 0.015 * U, 0.86 * cv.H - 0.82 * U),
            (0.4 * cv.W, 0.86 * cv.H - 0.68 * U)], (0.9, 0.9, 0.88))
    g.commit(blur=0.004, light=(-0.6, -0.8), rim=0.25, round_=0.005)
    g, hands = person(cv, 0.6, 0.865, 0.56, top=(0.95, 0.94, 0.91), dress='long', flare=1.35, hairstyle='wave',
                      hair=(0.2, 0.14, 0.1), arms=((10, -60), (5, -30)), commit=False, turn=0.8, facing=-1)
    for hx, hy in hands[:1]:
        for k in range(9):
            g.ellipse(hx + cv.rng.normal(0, 0.02) * U, hy + cv.rng.normal(0.01, 0.02) * U, 0.02 * U, 0.02 * U,
                      shade((0.92, 0.9, 0.85), cv.rng.uniform(0.8, 1.05)))
    g.commit(blur=0.004, light=(-0.6, -0.8), rim=0.2, round_=0.005, ao=0.3)
    veil(cv, 0.6, 0.29, 0.75, 0.1, 0.25)


def sc_starved_rock(cv):
    r = cv.rng
    cv.vgrad([(0, (0.85, 0.88, 0.9)), (1, (0.6, 0.6, 0.55))])
    # far canyon wall with waterfall
    cv.rect(0.25, 0.05, 0.75, 0.8, (0.7, 0.66, 0.58), blur=0.006)
    cv.noise_tint((0.45, 0.42, 0.36), 0.4, (3, 9, 20))
    for y in np.arange(0.1, 0.8, 0.04):
        cv.line([(0.25, y + r.uniform(-0.01, 0.01)), (0.75, y + r.uniform(-0.01, 0.01))], 0.004, (0.5, 0.46, 0.4),
                blur=0.004, alpha=0.4)
    cv.rect(0.485, 0.05, 0.515, 0.78, (0.97, 0.97, 0.97), blur=0.006, alpha=0.9)
    cv.glow(0.5, 0.75, 0.06, (1, 1, 1), 0.6, ry=0.04)
    treeline(cv, 0.08, 0.06, (0.3, 0.35, 0.28), blur=0.006)
    cv.blur(0.005)
    # pool
    cv.rect(0.0, 0.76, 1.0, 1.0, (0.45, 0.48, 0.48), blur=0.004)
    cv.rect(0.47, 0.76, 0.53, 1.0, (0.8, 0.8, 0.8), blur=0.02, alpha=0.35)
    # near canyon walls, left and right, in shadow
    for side in (0, 1):
        x0, x1 = (-0.05, 0.3) if side == 0 else (0.7, 1.05)
        pts = [(x0, -0.05), (x1 + (r.uniform(-0.03, 0.03)), -0.05)]
        edge = x1 if side == 0 else x0
        ys = np.linspace(0, 1.05, 14)
        wobble = [edge + r.uniform(-0.04, 0.04) for _ in ys]
        if side == 0:
            poly = [(x0, -0.05)] + list(zip(wobble, ys)) + [(x0, 1.05)]
        else:
            poly = [(x1, -0.05)] + list(zip(wobble, ys)) + [(x1, 1.05)]
        g = Group(cv)
        g.poly(cv.P(poly), (0.55, 0.5, 0.42))
        g.commit(blur=0.004, light=(1 if side == 0 else -1, -0.3), ao=0.4, tex=0.35, shade_amt=0.35, rim=0.2,
                 round_=0.003)
    for y in np.arange(0.0, 1.0, 0.035):
        cv.line([(-0.05, y), (0.3, y + 0.01)], 0.003, (0.35, 0.3, 0.25), blur=0.003, alpha=0.35)
        cv.line([(0.7, y + 0.01), (1.05, y)], 0.003, (0.35, 0.3, 0.25), blur=0.003, alpha=0.35)
    # a ledge with the honeymooners
    shapes(cv, [[(0.6, 0.82), (0.95, 0.8), (1.05, 0.86), (1.05, 1.05), (0.55, 1.05)]], (0.62, 0.57, 0.48),
           light=(-0.6, -1), tex=0.3)
    person(cv, 0.74, 0.84, 0.22, top=(0.25, 0.25, 0.27), bottom=(0.35, 0.33, 0.3), arms=(5, (-10, -30)), blur=0.003)
    person(cv, 0.79, 0.845, 0.2, top=(0.85, 0.83, 0.78), dress='knee', bottom=(0.4, 0.38, 0.36), hairstyle='wave',
           hair=(0.2, 0.15, 0.1), arms=((10, -30), 8), blur=0.003)
    # overhanging branch in front
    for k in range(3):
        cv.line([(1.05, 0.02 + k * 0.03), (0.75, 0.06 + k * 0.05), (0.55, 0.03 + k * 0.06)], 0.01, (0.1, 0.1, 0.08),
                blur=0.01, alpha=0.7)
    for _ in range(40):
        cv.ellipse(r.uniform(0.5, 1.05), r.uniform(0.0, 0.18), 0.03, 0.015, (0.12, 0.14, 0.1), blur=0.012, alpha=0.6)


def sc_dancing(cv):
    r = cv.rng
    cv.vgrad([(0, (0.15, 0.14, 0.13)), (0.7, (0.28, 0.26, 0.24)), (1, (0.4, 0.38, 0.35))])
    # string lights in swags
    for k in range(3):
        y0 = 0.08 + k * 0.08
        pts = [(x, y0 + 0.06 * math.sin(math.pi * ((x * 3) % 1))) for x in np.linspace(0, 1, 22)]
        bokeh(cv, pts, 0.02 + k * 0.004, [(1, 0.95, 0.8)], 0.8, 0.006)
    for i in range(10):  # other couples
        x = r.uniform(0, 1)
        person(cv, x, 0.86, 0.5, top=r.choice([(0.2, 0.2, 0.22), (0.7, 0.68, 0.65)]),
               dress=r.choice([None, 'mid']), hairstyle=r.choice(['short', 'wave']), blur=0.012, rim=0.1,
               alpha=0.85, round_=0.01)
    cv.blur(0.01)
    cv.rect(0, 0.82, 1, 1, (0.5, 0.46, 0.4), blur=0.02, alpha=0.6)  # floor sheen
    cv.ellipse(0.5, 0.9, 0.4, 0.05, (0.85, 0.8, 0.7), blur=0.03, alpha=0.25)
    g, _ = person(cv, 0.44, 0.92, 0.72, top=(0.12, 0.12, 0.14), arms=(10, (60, 95)), commit=False, turn=1.0,
                  hair=(0.15, 0.1, 0.07))
    person(cv, 0.56, 0.92, 0.66, top=(0.88, 0.86, 0.82), dress='mid', flare=1.45, hairstyle='wave',
           hair=(0.22, 0.15, 0.1), arms=((70, 100), (40, 80)), g=g, commit=False, turn=1.0, facing=-1)
    g.commit(blur=0.005, light=(-0.4, -0.9), rim=0.3, round_=0.006)
    light_field(cv, 0.5, 0.55, 0.9, 0.55, 1.2)


def sc_first_house(cv):
    r = cv.rng
    cv.vgrad([(0, (0.62, 0.7, 0.8)), (0.45, (0.88, 0.9, 0.9))])
    clouds(cv, 4, 0.05, 0.25, (1, 1, 1), 0.6)
    treeline(cv, 0.5, 0.06, (0.4, 0.45, 0.35), blur=0.01)
    cv.rect(0, 0.5, 1, 1, (0.6, 0.66, 0.48))
    ground_tex(cv, 0.5, None, 0.2)
    cv.blur(0.004)
    bungalow(cv, 0.2, 0.8, 0.6, 0.2, 0.17)
    box(cv, 0.47, 0.6, 0.53, 0.63, (0.75, 0.73, 0.7))  # stoop
    cv.poly([(0.47, 0.63), (0.53, 0.63), (0.56, 1.0), (0.44, 1.0)], (0.8, 0.79, 0.76), blur=0.003)  # walk
    shrub(cv, 0.25, 0.61, 0.05)
    shrub(cv, 0.75, 0.61, 0.05)
    cv.rect(0.66, 0.2, 0.69, 0.3, (0.45, 0.35, 0.3), blur=0.003)  # chimney
    # the new sapling, staked
    cv.line([(0.32, 0.82), (0.32, 0.6)], 0.004, (0.3, 0.25, 0.2), blur=0.002)
    cv.line([(0.335, 0.82), (0.335, 0.62)], 0.003, (0.6, 0.55, 0.45), blur=0.002)
    shrub(cv, 0.32, 0.62, 0.05, col=(0.35, 0.42, 0.28))
    shadow(cv, 0.42, 0.85, 0.06, 0.012, 0.35)
    shadow(cv, 0.6, 0.85, 0.07, 0.012, 0.35)
    person(cv, 0.6, 0.85, 0.3, top=(0.3, 0.3, 0.33), bottom=(0.35, 0.35, 0.38), arms=(6, (-5, -60)), blur=0.003,
           light=(-0.7, -0.6), turn=0.5, facing=-1)
    person(cv, 0.66, 0.855, 0.28, top=(0.8, 0.75, 0.7), dress='knee', flare=1.2, hairstyle='wave',
           hair=(0.2, 0.14, 0.1), blur=0.003, light=(-0.7, -0.6), arms=((10, -40), 12))
    person(cv, 0.71, 0.86, 0.14, top=(0.9, 0.88, 0.86), dress='knee', child=True, hairstyle='bob',
           hair=(0.5, 0.38, 0.25), blur=0.003, arms=((40, 30), 8))


def picnic_blanket(cv, x0, x1, y0, y1, col1, col2, n=10):
    pts = [(x0 + 0.06, y0), (x1 - 0.06, y0), (x1, y1), (x0, y1)]
    cv.poly(pts, col1, blur=0.003)
    for i in range(n + 1):
        t = i / n
        a = (lerp(x0 + 0.06, x1 - 0.06, t), y0)
        b = (lerp(x0, x1, t), y1)
        cv.line([a, b], 0.012 if i % 2 else 0.004, col2, blur=0.003, alpha=0.6)
    for i in range(1, 6):
        t = (i / 6) ** 1.2
        y = lerp(y0, y1, t)
        cv.line([(lerp(x0 + 0.06, x0, t), y), (lerp(x1 - 0.06, x1, t), y)], 0.01, col2, blur=0.003, alpha=0.55)


def sc_picnic(cv):
    r = cv.rng
    cv.vgrad([(0, (0.75, 0.82, 0.88)), (0.42, (0.9, 0.92, 0.92))])
    cv.rect(0, 0.4, 1, 0.47, (0.75, 0.82, 0.85), blur=0.004)  # the lake
    cv.rect(0, 0.4, 1, 0.405, (0.95, 0.95, 0.95), blur=0.003, alpha=0.6)
    cv.rect(0, 0.46, 1, 1, (0.52, 0.6, 0.4))
    ground_tex(cv, 0.46, None, 0.25)
    cv.blur(0.008)
    # big shade tree at the left with dappled shadow
    cv.ellipse(0.35, 0.78, 0.6, 0.18, (0.0, 0.0, 0.0), blur=0.05, alpha=0.35)
    cv.rect(0.06, 0.0, 0.11, 0.7, (0.25, 0.2, 0.16), blur=0.004)
    for _ in range(30):
        cv.ellipse(r.uniform(-0.1, 0.7), r.uniform(-0.1, 0.18), 0.12, 0.07, shade((0.22, 0.3, 0.18), r.uniform(0.8, 1.2)),
                   blur=0.015, alpha=0.9)
    picnic_blanket(cv, 0.2, 0.8, 0.66, 0.95, (0.92, 0.9, 0.85), (0.55, 0.2, 0.2))
    box(cv, 0.68, 0.66, 0.78, 0.74, (0.62, 0.5, 0.32), r=0.01, tex=0.25)  # basket
    cv.line([(0.69, 0.67), (0.73, 0.6), (0.77, 0.67)], 0.006, (0.5, 0.4, 0.25), blur=0.002)
    box(cv, 0.3, 0.66, 0.325, 0.73, (0.75, 0.3, 0.25), r=0.005)  # thermos
    person(cv, 0.44, 0.83, 0.42, top=(0.88, 0.86, 0.82), bottom=(0.45, 0.45, 0.48), pose='sitfront',
           arms=((15, -40), 30), short_sleeves=True, blur=0.004, light=(0.6, -0.8), turn=0.8, facing=1)
    person(cv, 0.58, 0.83, 0.4, top=(0.7, 0.6, 0.65), dress='mid', hairstyle='wave', hair=(0.2, 0.14, 0.1),
           pose='sitfront', arms=((10, -55), (10, -55)), blur=0.004, light=(0.6, -0.8), turn=0.8, facing=-1)
    for _ in range(25):  # sun flecks through leaves
        cv.ellipse(r.uniform(0, 1), r.uniform(0.5, 1), 0.02, 0.008, (1, 0.98, 0.9), blur=0.008, alpha=0.25)


# ================================================================ a growing family
def armchair(cv, x, y, w, h, col, blur=0.004, light=(-0.9, -0.4), part='all'):
    """part='back' (draw before the sitter), 'arms' (after), or 'all'."""
    g = Group(cv)
    X, Y, Wd, Hd = x * cv.W, y * cv.H, w * cv.H, h * cv.H
    if part in ('all', 'back'):
        g.rect(X - Wd * 0.5, Y - Hd, X + Wd * 0.5, Y - Hd * 0.35, col, r=Wd * 0.18)  # back
        g.rect(X - Wd * 0.42, Y - Hd * 0.42, X + Wd * 0.42, Y - Hd * 0.05, shade(col, 1.05), r=Wd * 0.05)
    if part in ('all', 'arms'):
        for s in (-1, 1):
            g.rect(X + s * Wd * 0.5 - Wd * 0.12, Y - Hd * 0.55, X + s * Wd * 0.5 + Wd * 0.12, Y - Hd * 0.02,
                   shade(col, 0.95), r=Wd * 0.08)
    g.commit(blur=blur, light=light, ao=0.45, tex=0.15, shade_amt=0.35, rim=0.1, round_=0.004)


def sc_margaret_baby(cv):
    cv.fill((0.55, 0.52, 0.48))
    for x in np.arange(0, 1, 0.06):  # striped wallpaper
        cv.rect(x, 0, x + 0.025, 1, (0.6, 0.58, 0.54), alpha=0.5)
    # bright window at left with sheer curtains
    cv.rect(-0.02, 0.08, 0.3, 0.62, (1, 1, 0.98), blur=0.006)
    cv.glow(0.12, 0.35, 0.3, (1, 0.98, 0.94), 0.5)
    for x in np.arange(0.0, 0.3, 0.025):
        cv.line([(x, 0.06), (x + 0.01, 0.65)], 0.008, (0.85, 0.84, 0.8), blur=0.006, alpha=0.4)
    cv.rect(0.29, 0.04, 0.36, 0.7, (0.75, 0.72, 0.68), blur=0.01, alpha=0.9)  # drape
    cv.rect(0, 0.78, 1, 1, (0.4, 0.36, 0.32), blur=0.004)
    cv.blur(0.008)
    light_field(cv, 0.1, 0.35, 1.3, 0.35, 1.3)
    armchair(cv, 0.56, 0.95, 0.42, 0.72, (0.3, 0.28, 0.27), part='back')
    g, hands = person(cv, 0.56, 0.95, 0.86, top=(0.42, 0.4, 0.42), dress='long', flare=1.25, hairstyle='wave',
                      hair=(0.16, 0.11, 0.08), pose='sitfront', arms=((18, -75), (10, -85)), commit=False, turn=1.4,
                      facing=-1)
    U = 0.86 * cv.H
    X, Y = 0.56 * cv.W, 0.95 * cv.H
    # the baby bundle in her arms, head toward the window
    g.ellipse(X - 0.01 * U, Y - 0.43 * U, 0.14 * U, 0.06 * U, (0.97, 0.97, 0.95))
    g.ellipse(X - 0.12 * U, Y - 0.455 * U, 0.06 * U, 0.05 * U, (0.97, 0.97, 0.95))
    g.ellipse(X - 0.115 * U, Y - 0.45 * U, 0.033 * U, 0.035 * U, SKIN)
    g.commit(blur=0.004, light=(-1, -0.3), rim=0.5, shade_amt=0.45, ao=0.35, round_=0.005)
    armchair(cv, 0.56, 0.95, 0.42, 0.72, (0.3, 0.28, 0.27), part='arms')
    # little table with lamp
    box(cv, 0.86, 0.6, 0.98, 0.95, (0.3, 0.24, 0.2), light=(-1, -0.3))
    shapes(cv, [[(0.88, 0.42), (0.96, 0.42), (0.98, 0.52), (0.86, 0.52)]], (0.85, 0.82, 0.75), light=(-1, -0.3))
    cv.rect(0.917, 0.52, 0.923, 0.6, (0.3, 0.28, 0.25))


def sc_first_car(cv):
    r = cv.rng
    cv.vgrad([(0, (0.62, 0.72, 0.82)), (0.5, (0.88, 0.9, 0.9))])
    tree(cv, 0.15, 0.62, 0.7, crown=(0.35, 0.42, 0.3), blur=0.012, spread=1.3, n=20)
    bungalow(cv, 0.55, 1.1, 0.62, 0.3, 0.12, blur=0.008)
    cv.rect(0, 0.6, 1, 1, (0.55, 0.62, 0.45), blur=0.004)
    ground_tex(cv, 0.6, None, 0.2)
    cv.poly([(0.25, 0.6), (0.6, 0.6), (0.95, 1.05), (-0.1, 1.05)], (0.78, 0.77, 0.74), blur=0.003)  # driveway
    cv.blur(0.006)
    shadow(cv, 0.47, 0.88, 0.4, 0.04, 0.5, 0.012)
    c = car(cv, 0.45, 0.88, 0.62, body=(0.25, 0.27, 0.3), roof=(0.85, 0.85, 0.82), facing=1)
    c.commit(blur=0.0035, light=(-0.4, -1), shade_amt=0.25, ao=0.3, rim=0.25, round_=0.003, tex=0.04)
    cv.rect(0.2, 0.705, 0.68, 0.712, (1, 1, 1), blur=0.003, alpha=0.5)  # chrome glint along the body
    person(cv, 0.78, 0.9, 0.42, top=(0.9, 0.88, 0.85), bottom=(0.3, 0.3, 0.34), short_sleeves=True,
           arms=((30, -60), 6), facing=-1, turn=1, blur=0.0035, hair=(0.18, 0.12, 0.08))
    person(cv, 0.88, 0.92, 0.22, top=(0.75, 0.72, 0.7), dress='knee', child=True, hairstyle='bob',
           hair=(0.45, 0.32, 0.2), blur=0.0035)
    person(cv, 0.94, 0.93, 0.16, top=(0.4, 0.42, 0.5), bottom=(0.35, 0.35, 0.4), child=True, hair=(0.6, 0.48, 0.3),
           blur=0.0035)


def party_hat(cv, x, y, h, col, stripe=(1, 1, 1)):
    shapes(cv, [[(x - h * 0.28 / cv.aspect, y), (x, y - h), (x + h * 0.28 / cv.aspect, y)]], col, blur=0.004,
           light=(-0.6, -0.7), ao=0.2)
    cv.line([(x - h * 0.18 / cv.aspect, y - h * 0.3), (x + h * 0.1 / cv.aspect, y - h * 0.6)], 0.006, stripe,
            blur=0.004, alpha=0.6)
    cv.ellipse(x, y - h, 0.012, 0.012, stripe, blur=0.003)


def sc_birthday(cv):
    r = cv.rng
    cv.vgrad([(0, (0.42, 0.4, 0.37)), (1, (0.55, 0.52, 0.48))])
    cv.rect(0.6, 0.05, 0.85, 0.3, (0.7, 0.68, 0.64), blur=0.02, alpha=0.6)  # picture on wall
    cv.rect(0.08, 0.0, 0.3, 0.35, (0.75, 0.74, 0.7), blur=0.02, alpha=0.4)
    cv.blur(0.01)
    kids = [(0.18, 0.4, (0.75, 0.72, 0.7), 'bob', (0.8, 0.3, 0.3)), (0.33, 0.43, (0.4, 0.42, 0.5), 'short', (0.3, 0.5, 0.8)),
            (0.5, 0.38, (0.9, 0.88, 0.85), 'short', (0.9, 0.8, 0.3)), (0.67, 0.42, (0.7, 0.6, 0.65), 'bob', (0.3, 0.6, 0.4)),
            (0.83, 0.44, (0.45, 0.45, 0.45), 'short', (0.8, 0.4, 0.6))]
    for x, h, col, hs, hat in kids:
        U = 0.62 + (h - 0.4) * 0.6
        person(cv, x, 1.0, U, top=col, child=True, hairstyle=hs, hair=(0.4, 0.3, 0.2),
               arms=((20, -40), (20, -40)), blur=0.005, light=(0, -0.5), turn=r.uniform(-1, 1), shade_amt=0.15,
               rim=0.3, ao=0.2)
        party_hat(cv, x, 1.0 - 0.87 * U, 0.09, hat)
    # table with cloth
    box(cv, -0.02, 0.62, 1.02, 1.02, (0.93, 0.92, 0.9), light=(0, -1), ao=0.1, tex=0.05)
    cv.rect(-0.02, 0.62, 1.02, 0.64, (1, 1, 1), blur=0.005, alpha=0.4)
    # cake
    g = Group(cv)
    g.rect(0.39 * cv.W, 0.6 * cv.H, 0.61 * cv.W, 0.74 * cv.H, (0.95, 0.94, 0.92))
    g.ellipse(0.5 * cv.W, 0.6 * cv.H, 0.11 * cv.W, 0.035 * cv.H, (1, 1, 1))
    g.ellipse(0.5 * cv.W, 0.74 * cv.H, 0.11 * cv.W, 0.035 * cv.H, (0.95, 0.94, 0.92))
    g.commit(blur=0.003, light=(0, -1), ao=0.35, shade_amt=0.1, rim=0.0, round_=0)
    for k in range(10):
        cv.ellipse(0.4 + k * 0.022, 0.66 + 0.01 * math.sin(k), 0.008, 0.008, (0.85, 0.82, 0.8), blur=0.002)
    for x in (0.47, 0.5, 0.53):
        cv.rect(x - 0.003, 0.52, x + 0.003, 0.6, (0.95, 0.95, 0.95))
        cv.ellipse(x, 0.505, 0.006, 0.014, (1, 1, 0.9), blur=0.002)
        cv.glow(x, 0.505, 0.02, (1, 0.9, 0.7), 0.35)
    cv.glow(0.5, 0.5, 0.15, (1, 0.9, 0.75), 0.12)
    light_field(cv, 0.5, 0.6, 0.95, 0.55, 1.0)


def sc_county_fair(cv):
    r = cv.rng
    cv.vgrad([(0, (0.75, 0.8, 0.86)), (0.55, (0.9, 0.9, 0.88)), (0.62, (0.72, 0.68, 0.62)), (1, (0.58, 0.53, 0.46))])
    clouds(cv, 6, 0.05, 0.3, (1, 1, 1), 0.5)
    cx, cy, R = 0.82, 0.3, 0.24
    for k in range(16):
        a = k * math.pi / 8
        cv.line([(cx, cy), (cx + math.cos(a) * R / cv.aspect, cy + math.sin(a) * R)], 0.003, (0.35, 0.35, 0.37),
                blur=0.004, alpha=0.8)
        cv.rect(cx + math.cos(a) * R / cv.aspect - 0.012, cy + math.sin(a) * R,
                cx + math.cos(a) * R / cv.aspect + 0.012, cy + math.sin(a) * R + 0.035, (0.4, 0.35, 0.33), blur=0.004)
    im = cv.mask(lambda d: d.ellipse([(cx - R / cv.aspect) * cv.W, (cy - R) * cv.H, (cx + R / cv.aspect) * cv.W,
                                      (cy + R) * cv.H], outline=255, width=max(2, int(0.006 * cv.H))), 0.003)
    cv.apply(im, (0.35, 0.35, 0.37))
    cv.line([(cx, cy), (cx - 0.07, 0.62)], 0.008, (0.35, 0.35, 0.37), blur=0.004)
    cv.line([(cx, cy), (cx + 0.07, 0.62)], 0.008, (0.35, 0.35, 0.37), blur=0.004)
    for tx, tw, th in ((0.08, 0.16, 0.2), (0.3, 0.12, 0.16), (0.56, 0.1, 0.13)):
        cv.poly([(tx - tw / 2, 0.6), (tx, 0.6 - th), (tx + tw / 2, 0.6)], (0.92, 0.9, 0.86), blur=0.005)
        for k in range(5):
            x0 = tx - tw / 2 + k * tw / 5
            cv.poly([(x0, 0.6), (tx, 0.6 - th), (x0 + tw / 10, 0.6)], (0.6, 0.25, 0.25), blur=0.005, alpha=0.8)
        cv.rect(tx - tw / 2, 0.6, tx + tw / 2, 0.64, (0.85, 0.83, 0.78), blur=0.005)
    for i in range(26):
        person(cv, r.uniform(0.0, 1.0), 0.66 + r.uniform(0, 0.03), 0.17 + r.uniform(-0.02, 0.02),
               top=mix((0.3, 0.3, 0.35), (0.9, 0.88, 0.85), r.random()), bottom=(0.25, 0.25, 0.3),
               hat=r.choice([None, 'fedora', None]), dress=r.choice([None, 'knee']),
               hairstyle=r.choice(['short', 'bob']), blur=0.006, rim=0.0)
    cv.blur(0.007)
    ground_tex(cv, 0.62, None, 0.15)
    # the horse, with Walter up
    shadow(cv, 0.48, 0.9, 0.26, 0.03, 0.5)
    hg = horse(cv, 0.45, 0.9, 0.4, col=(0.36, 0.25, 0.17), facing=1)
    U = 0.4 * cv.H
    X, Y = 0.45 * cv.W, 0.9 * cv.H
    hg.ellipse(X + 0.83 * U, Y - 1.17 * U, 0.025 * U, 0.06 * U, (0.85, 0.82, 0.78))  # blaze
    g, _ = person(cv, 0.44, 0.9 - 0.4 * 1.0, 0.46, top=(0.92, 0.9, 0.86), bottom=(0.3, 0.32, 0.38), pose='ride',
                  hat='fedora', hat_col=(0.75, 0.72, 0.65), arms=((25, 70), (-25, -75)), short_sleeves=True,
                  g=hg, commit=False, turn=1.0)
    hg.commit(blur=0.004, light=(-0.6, -0.8), shade_amt=0.3, rim=0.35, round_=0.004, ao=0.35)
    cv.line([(0.44 + 0.2 * 0.46 / cv.aspect, 0.9 - 0.4 - 0.46 * 0.25), (0.45 + 0.6 * 0.4 / cv.aspect, 0.9 - 0.4 * 1.32)],
            0.004, (0.1, 0.08, 0.07), blur=0.002)
    # out-of-focus rail fence in the foreground
    cv.rect(-0.02, 0.83, 0.32, 0.87, (0.55, 0.5, 0.42), blur=0.014)
    cv.rect(0.05, 0.76, 0.08, 1.02, (0.5, 0.45, 0.38), blur=0.014)
    cv.rect(0.26, 0.76, 0.29, 1.02, (0.5, 0.45, 0.38), blur=0.014)


def sc_backyard(cv):
    r = cv.rng
    cv.vgrad([(0, (0.55, 0.72, 0.88)), (0.4, (0.85, 0.9, 0.92))])
    treeline(cv, 0.42, 0.1, (0.3, 0.45, 0.28), blur=0.012)
    # picket fence
    cv.rect(0, 0.36, 1, 0.5, (0.35, 0.5, 0.3), blur=0.006)
    for x in np.arange(0, 1.02, 0.025):
        cv.poly([(x, 0.5), (x, 0.4), (x + 0.008, 0.39), (x + 0.016, 0.4), (x + 0.016, 0.5)], (0.95, 0.94, 0.9),
                blur=0.003)
    cv.rect(0, 0.42, 1, 0.43, (0.9, 0.9, 0.86), blur=0.003)
    cv.rect(0, 0.48, 1, 1, (0.4, 0.62, 0.3))
    ground_tex(cv, 0.48, None, 0.22)
    # clothesline with sheets
    cv.line([(0.05, 0.2), (0.5, 0.24), (0.95, 0.2)], 0.003, (0.5, 0.5, 0.5), blur=0.002)
    for x in (0.12, 0.3, 0.6):
        y = 0.2 + 0.04 * (1 - abs((x - 0.5) / 0.45))
        shapes(cv, [[(x, y), (x + 0.14, y + 0.004), (x + 0.135, y + 0.22), (x + 0.005, y + 0.21)]],
               (0.97, 0.96, 0.94), light=(-0.8, -0.5), blur=0.004, tex=0.12)
    cv.blur(0.004)
    # sprinkler arc
    for k in range(260):
        t = r.uniform(-1, 1)
        x = 0.55 + t * 0.28
        y = 0.74 - 0.3 * (1 - t * t) + r.normal(0, 0.012)
        cv.ellipse(x, y, 0.004, 0.004, (1, 1, 1), blur=0.002, alpha=0.6, mode='add')
    cv.glow(0.55, 0.6, 0.18, (0.9, 0.95, 1), 0.25, ry=0.12)
    cv.ellipse(0.55, 0.78, 0.015, 0.008, (0.4, 0.4, 0.4), blur=0.002)
    for x, h, col, kw in ((0.38, 0.3, (0.3, 0.45, 0.8), dict(child=True, pose='stride', arms=(70, 60))),
                          (0.7, 0.26, (0.9, 0.35, 0.4), dict(child=True, pose='stride', dress='knee', hairstyle='bob',
                                                              arms=(80, 90), facing=-1)),
                          (0.84, 0.18, (0.95, 0.85, 0.3), dict(child=True, dress='knee', hairstyle='bob',
                                                               arms=(20, 30)))):
        shadow(cv, x + 0.02, 0.92 - (0.3 - h) * 0.3, 0.05, 0.01, 0.35)
        person(cv, x, 0.92 - (0.3 - h) * 0.3, h, top=col, bottom=col, legs_col=SKIN, short_sleeves=True,
               blur=0.004, light=(-0.6, -0.8), hair=(0.45, 0.32, 0.18), **kw)
    shadow(cv, 0.2, 0.95, 0.05, 0.01, 0.35)
    dog(cv, 0.18, 0.94, 0.1, col=(0.75, 0.6, 0.4), facing=1).commit(blur=0.004, round_=0.004)


def sc_christmas(cv):
    r = cv.rng
    cv.fill((0.62, 0.55, 0.45))
    cv.noise_tint((0.5, 0.42, 0.32), 0.3)
    window_frame(cv, 0.68, 0.12, 0.92, 0.55, (0.75, 0.82, 0.9), glow=0.25)
    cv.rect(0, 0.72, 1, 1, (0.45, 0.32, 0.25))
    ground_tex(cv, 0.72, None, 0.15)
    cv.rect(0, 0.71, 1, 0.73, (0.85, 0.8, 0.7), blur=0.003)  # baseboard
    cv.blur(0.006)
    # the tree
    tree_pts = []
    for i in range(7):
        t = i / 6
        yb = 0.82 - t * 0.66
        w = (0.2 - 0.17 * t)
        tree_pts.append([(0.28 - w, yb), (0.28, yb - 0.2), (0.28 + w, yb)])
    shapes(cv, tree_pts, (0.12, 0.28, 0.16), light=(0.8, -0.3), ao=0.5, tex=0.35, blur=0.004, round_=0.004)
    for k in range(60):  # tinsel
        x = r.uniform(0.12, 0.44)
        y = r.uniform(0.2, 0.8)
        if abs(x - 0.28) < (y - 0.12) * 0.3:
            cv.line([(x, y), (x + 0.002, y + 0.04)], 0.002, (0.85, 0.85, 0.9), blur=0.002, alpha=0.5)
    bulbs = []
    for k in range(40):
        y = r.uniform(0.2, 0.8)
        w = (y - 0.14) * 0.3
        bulbs.append((0.28 + r.uniform(-w, w), y))
    bokeh(cv, bulbs, 0.016, [(1, 0.3, 0.2), (0.3, 0.5, 1), (1, 0.8, 0.2), (0.3, 0.9, 0.4), (1, 0.5, 0.8)], 0.9,
          0.004)
    for x, y in bulbs:
        cv.glow(x, y, 0.025, (1, 0.8, 0.6), 0.08)
    cv.rect(0.27, 0.8, 0.29, 0.84, (0.3, 0.2, 0.15))
    # presents
    for x0, w, h, col, rib in ((0.1, 0.12, 0.08, (0.8, 0.2, 0.2), (0.95, 0.85, 0.3)),
                               (0.25, 0.1, 0.1, (0.25, 0.45, 0.7), (1, 1, 1)),
                               (0.36, 0.14, 0.07, (0.9, 0.85, 0.6), (0.8, 0.2, 0.2)),
                               (0.55, 0.09, 0.06, (0.3, 0.6, 0.35), (1, 0.9, 0.9))):
        box(cv, x0, 0.86 - h, x0 + w, 0.86, col, light=(0.8, -0.6))
        cv.rect(x0 + w * 0.45, 0.86 - h, x0 + w * 0.55, 0.86, rib, alpha=0.9)
    # paper on the floor
    for _ in range(14):
        x, y = r.uniform(0.3, 0.9), r.uniform(0.85, 0.98)
        shapes(cv, [[(x, y), (x + 0.05, y - 0.02), (x + 0.07, y + 0.02), (x + 0.02, y + 0.03)]],
               r.choice([(0.85, 0.25, 0.2), (0.95, 0.92, 0.85), (0.3, 0.5, 0.75)]), blur=0.004)
    # the kids on the floor, Dad in his robe
    armchair(cv, 0.86, 0.88, 0.22, 0.42, (0.45, 0.5, 0.42), part='back')
    person(cv, 0.86, 0.88, 0.55, top=(0.55, 0.25, 0.25), bottom=(0.55, 0.25, 0.25), pose='sitfront',
           hairstyle='short', arms=((10, -60), (10, -70)), blur=0.004, light=(0.9, -0.4), turn=1.2, facing=-1)
    armchair(cv, 0.86, 0.88, 0.22, 0.42, (0.45, 0.5, 0.42), part='arms')
    person(cv, 0.5, 0.93, 0.34, top=(0.85, 0.8, 0.9), bottom=(0.7, 0.6, 0.75), dress='knee', child=True,
           hairstyle='bob', pose='floor', hair=(0.45, 0.3, 0.18), arms=((30, -40), (30, -40)), blur=0.004,
           light=(-0.8, -0.4), turn=-1.0)
    person(cv, 0.67, 0.95, 0.3, top=(0.5, 0.6, 0.8), child=True, pose='floor', hair=(0.55, 0.4, 0.22),
           arms=((30, -50), (40, 0)), blur=0.004, light=(-0.8, -0.4), turn=-1, facing=-1)
    light_field(cv, 0.5, 0.6, 1.0, 0.6, 1.0)


def sc_easter(cv):
    r = cv.rng
    cv.fill((0.72, 0.42, 0.35))  # brick
    for row, y in enumerate(np.arange(0, 0.62, 0.025)):
        off = 0.03 if row % 2 else 0
        cv.line([(0, y), (1, y)], 0.004, (0.85, 0.82, 0.78), alpha=0.6)
        for x in np.arange(off, 1, 0.06):
            cv.line([(x, y), (x, y + 0.025)], 0.003, (0.85, 0.82, 0.78), alpha=0.5)
    cv.noise_tint((0.55, 0.3, 0.25), 0.35)
    box(cv, 0.3, 0.05, 0.7, 0.55, (0.95, 0.94, 0.9))  # door surround
    box(cv, 0.36, 0.09, 0.64, 0.55, (0.3, 0.42, 0.38))
    cv.rect(0.4, 0.13, 0.6, 0.3, (0.6, 0.65, 0.65), alpha=0.6)
    shrub(cv, 0.12, 0.62, 0.15, col=(0.25, 0.38, 0.22))
    shrub(cv, 0.9, 0.62, 0.15, col=(0.25, 0.38, 0.22))
    cv.blur(0.006)
    for i, y in enumerate((0.55, 0.66, 0.77, 0.88)):
        box(cv, 0.12 - i * 0.04, y, 0.88 + i * 0.04, y + 0.11, (0.68, 0.66, 0.62), light=(0, -1), ao=0.1, tex=0.15)
    # three kids on the steps
    person(cv, 0.5, 0.56, 0.34, top=(0.8, 0.72, 0.85), dress='knee', hairstyle='bob', hair=(0.4, 0.28, 0.16),
           blur=0.004, arms=(8, 6), light=(-0.6, -0.8))
    person(cv, 0.32, 0.67, 0.3, top=(0.3, 0.35, 0.45), bottom=(0.3, 0.32, 0.38), child=True, blur=0.004,
           hair=(0.35, 0.25, 0.15), arms=(4, 4), light=(-0.6, -0.8))
    g, hands = person(cv, 0.66, 0.78, 0.25, top=(0.98, 0.88, 0.45), dress='knee', flare=1.3, child=True,
                      hairstyle='bob', hair=(0.6, 0.45, 0.25), hat='easter', hat_col=(0.97, 0.95, 0.88),
                      arms=(8, (20, -30)), commit=False)
    hx, hy = hands[-1]
    U = 0.25 * cv.H
    g.ellipse(hx, hy + 0.05 * U, 0.08 * U, 0.06 * U, (0.8, 0.65, 0.4))
    g.ellipse(hx, hy + 0.01 * U, 0.075 * U, 0.03 * U, (0.6, 0.85, 0.5))
    g.commit(blur=0.004, light=(-0.6, -0.8), round_=0.004)


# ================================================================ summers & road trips
def sc_route66_motel(cv):
    r = cv.rng
    cv.vgrad([(0, (0.08, 0.12, 0.3)), (0.55, (0.3, 0.3, 0.5)), (0.75, (0.95, 0.6, 0.4)), (0.8, (0.9, 0.7, 0.5))])
    for _ in range(20):
        cv.ellipse(r.uniform(0, 1), r.uniform(0, 0.4), 0.0025, 0.0025, (1, 1, 1), alpha=r.uniform(0.2, 0.8),
                   mode='add')
    ridge(cv, 0.8, 0.05, (0.2, 0.15, 0.2), blur=0.003, rough=0.3)
    cv.rect(0, 0.8, 1, 1, (0.12, 0.1, 0.12))
    # the low motel with lit doors
    box(cv, 0.0, 0.7, 0.62, 0.83, (0.3, 0.25, 0.28))
    cv.rect(0.0, 0.68, 0.64, 0.7, (0.2, 0.17, 0.2))
    for x in np.arange(0.03, 0.6, 0.09):
        cv.rect(x, 0.74, x + 0.035, 0.8, (1, 0.8, 0.45), blur=0.003)
        cv.glow(x + 0.018, 0.77, 0.03, (1, 0.7, 0.4), 0.3)
    # the sign
    cv.rect(0.74, 0.25, 0.755, 0.83, (0.15, 0.12, 0.15))
    shapes(cv, [[(0.58, 0.12), (0.95, 0.12), (0.95, 0.42), (0.58, 0.42)]], (0.2, 0.25, 0.3), blur=0.003)
    neon = Image.new('L', (cv.W, cv.H), 0)
    d = ImageDraw.Draw(neon)
    f = font('sans_b', 0.085 * cv.H)
    d.text((0.765 * cv.W, 0.2 * cv.H), 'MOTEL', font=f, fill=255, anchor='mm')
    f2 = font('serif_i', 0.045 * cv.H)
    d.text((0.765 * cv.W, 0.29 * cv.H), 'Desert Rose', font=f2, fill=255, anchor='mm')
    m = np.asarray(neon.filter(ImageFilter.GaussianBlur(1.0)), np.float32) / 255
    cv.apply(m, (1, 0.45, 0.6), 1.0)
    cv.apply(gauss(m, 0.02 * cv.H), (1, 0.3, 0.5), 2.2, mode='add')
    # arrow in turquoise neon
    arrow = [(0.5, 0.5), (0.85, 0.5), (0.85, 0.47), (0.92, 0.53), (0.85, 0.59), (0.85, 0.56), (0.5, 0.56)]
    am = cv.mask(lambda dd: dd.line(cv.P(arrow + [arrow[0]]), fill=255, width=max(2, int(0.008 * cv.H))), 0.002)
    cv.apply(am, (0.5, 1, 0.95))
    cv.apply(gauss(am, 0.02 * cv.H), (0.2, 0.9, 0.9), 2.0, mode='add')
    vac = Image.new('L', (cv.W, cv.H), 0)
    ImageDraw.Draw(vac).text((0.71 * cv.W, 0.53 * cv.H), 'VACANCY', font=font('sans_b', 0.03 * cv.H), fill=255,
                             anchor='mm')
    vm = np.asarray(vac.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
    cv.apply(vm, (1, 0.3, 0.2))
    cv.apply(gauss(vm, 0.012 * cv.H), (1, 0.2, 0.1), 1.6, mode='add')
    # the wagon parked out front
    c = car(cv, 0.3, 0.92, 0.5, body=(0.35, 0.4, 0.45), wagon=True, wood=True, glass=(0.2, 0.2, 0.25), facing=-1)
    c.commit(blur=0.004, light=(0.5, -1), shade_amt=0.2, rim=0.5, rim_col=(1, 0.5, 0.6), ao=0.4, round_=0.003)


def sc_station_wagon(cv):
    r = cv.rng
    cv.vgrad([(0, (0.3, 0.55, 0.85)), (0.45, (0.75, 0.82, 0.88))])
    mesa_ridge(cv, 0.5, 0.12, (0.75, 0.55, 0.45), (0.8, 0.8, 0.88), 0.45, 0.004, seed_off=21, stripe=0.08)
    cv.rect(0, 0.5, 1, 1, (0.82, 0.7, 0.52), blur=0.003)
    ground_tex(cv, 0.5, None, 0.2, (6, 20, 60))
    for _ in range(25):
        shrub(cv, r.uniform(0, 1), r.uniform(0.52, 0.62), 0.012, col=(0.5, 0.5, 0.35), blur=0.004)
    cv.poly([(0.47, 0.5), (0.53, 0.5), (1.4, 1.05), (-0.4, 1.05)], (0.3, 0.3, 0.32), blur=0.003)  # road
    cv.poly([(0.497, 0.5), (0.503, 0.5), (0.53, 1.05), (0.47, 1.05)], (0.9, 0.82, 0.4), blur=0.003, alpha=0.8)
    cv.blur(0.003)
    # Route 66 shield sign
    cv.rect(0.165, 0.38, 0.172, 0.7, (0.4, 0.4, 0.42), blur=0.002)
    shapes(cv, [[(0.13, 0.26), (0.21, 0.26), (0.21, 0.31), (0.19, 0.37), (0.168, 0.4), (0.15, 0.37), (0.13, 0.31)]],
           (0.95, 0.95, 0.92), blur=0.003)
    cv.text((0.168, 0.275), 'US', 'sans_b', 0.022, (0.1, 0.1, 0.1), blur=0.002)
    cv.text((0.168, 0.33), '66', 'sans_b', 0.06, (0.1, 0.1, 0.1), blur=0.002)
    shadow(cv, 0.68, 0.86, 0.3, 0.035, 0.55, 0.008)
    c = car(cv, 0.66, 0.86, 0.6, body=(0.7, 0.75, 0.72), roof=(0.7, 0.75, 0.72), wagon=True, wood=True,
            luggage=True, facing=-1)
    c.commit(blur=0.0035, light=(-0.3, -1), shade_amt=0.25, ao=0.3, rim=0.3, round_=0.003)
    person(cv, 0.34, 0.9, 0.44, top=(0.9, 0.88, 0.82), bottom=(0.55, 0.5, 0.42), short_sleeves=True,
           arms=((30, -70), (30, -80)), blur=0.0035, light=(-0.3, -1), rim=0.35, turn=1.0, hat='fedora',
           hat_col=(0.85, 0.8, 0.65))
    cv.rect(0.31, 0.62, 0.37, 0.66, (0.95, 0.92, 0.85), blur=0.003)  # the map
    person(cv, 0.42, 0.91, 0.28, top=(0.85, 0.3, 0.25), bottom=(0.3, 0.35, 0.5), child=True, blur=0.0035,
           light=(-0.3, -1), rim=0.35, hair=(0.4, 0.28, 0.15))


def lake(cv, y0, y1, col_far, col_near, sky_reflect=0.4):
    g = cv.vgrad([(y0, col_far), (y1, col_near)], apply=False)
    cv.rect(-0.02, y0, 1.02, y1 + 0.02, g, blur=0.002)
    for _ in range(140):
        y = cv.rng.uniform(y0, y1)
        x = cv.rng.uniform(-0.1, 1.1)
        L = cv.rng.uniform(0.02, 0.12) * (0.4 + (y - y0) / (y1 - y0))
        cv.line([(x, y), (x + L, y)], 0.002 + 0.004 * (y - y0) / (y1 - y0), (1, 1, 1), blur=0.002,
                alpha=sky_reflect * cv.rng.uniform(0.1, 0.5))


def reflect(cv, y_axis, y0, y1, strength=0.6, blur=0.01):
    """Mirror the band [y0, y_axis] of the canvas into [y_axis, y1] and blend (water reflection)."""
    H = cv.H
    a0, a1, b1 = int(y0 * H), int(y_axis * H), int(y1 * H)
    src = cv.a[a0:a1][::-1]
    n = min(len(src), b1 - a1)
    if n <= 0:
        return
    refl = gauss(src[:n], blur * H)
    w = np.linspace(strength, strength * 0.4, n, dtype=np.float32)[:, None, None]
    cv.a[a1:a1 + n] = cv.a[a1:a1 + n] * (1 - w) + refl * w * 0.85


def sc_lake_cabin(cv):
    r = cv.rng
    cv.vgrad([(0, (0.35, 0.45, 0.65)), (0.45, (0.95, 0.75, 0.55))])
    clouds(cv, 5, 0.1, 0.3, (1, 0.8, 0.7), 0.5)
    treeline(cv, 0.47, 0.06, (0.15, 0.2, 0.18), blur=0.005, n=80)
    for i in range(14):
        pine(cv, r.uniform(0, 1), 0.47, r.uniform(0.08, 0.14), col=(0.12, 0.18, 0.15), blur=0.004)
    # cabin at the right, among the pines
    box(cv, 0.6, 0.35, 0.85, 0.47, (0.4, 0.28, 0.2), light=(-1, -0.3))
    for y in np.arange(0.36, 0.47, 0.015):
        cv.line([(0.6, y), (0.85, y)], 0.003, (0.25, 0.17, 0.12), alpha=0.6)
    shapes(cv, [[(0.58, 0.36), (0.725, 0.27), (0.87, 0.36)]], (0.25, 0.22, 0.2))
    for x in (0.64, 0.77):
        cv.rect(x, 0.38, x + 0.04, 0.43, (1, 0.8, 0.45), blur=0.003)
        cv.glow(x + 0.02, 0.405, 0.03, (1, 0.7, 0.35), 0.4)
    for x in (0.55, 0.9, 0.95):
        pine(cv, x, 0.48, 0.3, col=(0.1, 0.16, 0.12), blur=0.004)
    lake(cv, 0.47, 1.0, (0.55, 0.5, 0.55), (0.2, 0.25, 0.3), 0.3)
    reflect(cv, 0.47, 0.2, 0.75, 0.55)
    cv.blur(0.003)
    # dock with June sitting at the end
    cv.poly([(0.0, 0.78), (0.42, 0.62), (0.48, 0.63), (0.12, 1.02), (0.0, 1.02)], (0.45, 0.38, 0.3), blur=0.003)
    for t in np.linspace(0, 1, 12):
        cv.line([(lerp(0.0, 0.42, t), lerp(0.78, 0.62, t)), (lerp(0.12, 0.48, t), lerp(1.02, 0.63, t))], 0.003,
                (0.3, 0.25, 0.2), alpha=0.6)
    person(cv, 0.43, 0.64, 0.16, top=(0.85, 0.5, 0.45), dress='knee', hairstyle='wave', hair=(0.3, 0.2, 0.12),
           pose='sitfront', blur=0.003, view='back', light=(0.5, -1), rim=0.4, rim_col=(1, 0.7, 0.5))
    # rowboat tied up
    shapes(cv, [[(0.22, 0.86), (0.4, 0.86), (0.37, 0.9), (0.25, 0.9)]], (0.75, 0.3, 0.25), blur=0.003)
    light_field(cv, 0.6, 0.35, 1.2, 0.7, 1.0)


def sc_fishing(cv):
    r = cv.rng
    cv.vgrad([(0, (0.62, 0.68, 0.75)), (0.48, (0.98, 0.85, 0.7)), (0.5, (0.95, 0.85, 0.75))])
    cv.glow(0.7, 0.45, 0.12, (1, 0.9, 0.7), 0.8)
    treeline(cv, 0.5, 0.04, (0.45, 0.48, 0.5), blur=0.006, n=60)
    lake(cv, 0.5, 1.0, (0.85, 0.8, 0.75), (0.35, 0.42, 0.48), 0.5)
    reflect(cv, 0.5, 0.3, 0.8, 0.5, 0.012)
    # mist banks
    for _ in range(10):
        cv.ellipse(r.uniform(-0.1, 1.1), r.uniform(0.45, 0.6), 0.4, 0.03, (1, 0.97, 0.92), blur=0.03, alpha=0.35)
    cv.blur(0.003)
    # the rowboat, Uncle Frank and Robert
    bx, by = 0.45, 0.72
    cv.ellipse(bx, by + 0.035, 0.3, 0.02, (0.2, 0.22, 0.25), blur=0.01, alpha=0.4)
    person(cv, 0.38, by + 0.01, 0.3, top=(0.65, 0.2, 0.18), bottom=(0.35, 0.33, 0.3), pose='sitfront', hat='cap',
           hat_col=(0.25, 0.3, 0.25), arms=((20, -40), (50, 60)), blur=0.004, light=(0.8, -0.5), rim=0.5,
           rim_col=(1, 0.85, 0.6), turn=1)
    person(cv, 0.53, by + 0.01, 0.26, top=(0.85, 0.8, 0.6), bottom=(0.3, 0.35, 0.5), pose='sitfront',
           hair=(0.45, 0.3, 0.16), arms=((40, 50), (15, -30)), blur=0.004, light=(0.8, -0.5), rim=0.5,
           rim_col=(1, 0.85, 0.6), turn=-1, facing=-1)
    shapes(cv, [[(0.22, by - 0.04), (0.68, by - 0.04), (0.64, by + 0.03), (0.27, by + 0.03)]], (0.55, 0.42, 0.3),
           light=(0.8, -0.6), blur=0.004, tex=0.2)
    cv.line([(0.22, by - 0.04), (0.68, by - 0.04)], 0.004, (0.75, 0.65, 0.5), blur=0.002)
    # rods and lines
    cv.line([(0.43, by - 0.12), (0.62, by - 0.33)], 0.003, (0.2, 0.18, 0.15), blur=0.002)
    cv.line([(0.62, by - 0.33), (0.8, by + 0.02)], 0.0012, (0.9, 0.9, 0.9), blur=0.002, alpha=0.5)
    cv.line([(0.46, by - 0.1), (0.3, by - 0.3)], 0.003, (0.2, 0.18, 0.15), blur=0.002)
    cv.line([(0.3, by - 0.3), (0.15, by + 0.05)], 0.0012, (0.9, 0.9, 0.9), blur=0.002, alpha=0.5)
    for x in (0.8, 0.15):
        cv.ellipse(x, by + 0.05, 0.02, 0.004, (1, 1, 1), blur=0.003, alpha=0.4)


def umbrella(cv, x, y_top, r, pole_h, cols):
    cv.line([(x, y_top), (x + 0.01, y_top + pole_h)], 0.006, (0.85, 0.85, 0.85), blur=0.002)
    n = 8
    polys = []
    for k in range(n):
        a0 = math.pi + k * math.pi / n
        a1 = a0 + math.pi / n
        p0 = (x + math.cos(a0) * r / cv.aspect, y_top + 0.06 + math.sin(a0) * r * 0.35)
        p1 = (x + math.cos(a1) * r / cv.aspect, y_top + 0.06 + math.sin(a1) * r * 0.35)
        shapes(cv, [[(x, y_top), p0, p1]], cols[k % len(cols)], blur=0.004, light=(-0.6, -0.8), ao=0.15, tex=0.05)


def sc_dunes_beach(cv):
    r = cv.rng
    cv.vgrad([(0, (0.4, 0.62, 0.85)), (0.4, (0.82, 0.88, 0.9))])
    clouds(cv, 4, 0.06, 0.25, (1, 1, 1), 0.7, size=0.08)
    lake(cv, 0.4, 0.58, (0.45, 0.65, 0.7), (0.35, 0.6, 0.62), 0.6)
    for y in (0.5, 0.54, 0.57):
        cv.line([(-0.1, y), (1.1, y + 0.005)], 0.006, (1, 1, 1), blur=0.006, alpha=0.6)
    cv.rect(-0.02, 0.57, 1.02, 1.02, (0.9, 0.82, 0.66), blur=0.004)
    ground_tex(cv, 0.58, None, 0.12, (10, 30, 80))
    cv.blur(0.003)
    # the umbrella, towel, June in the shade
    cv.ellipse(0.32, 0.86, 0.22, 0.05, (0.3, 0.25, 0.2), blur=0.02, alpha=0.4)
    shapes(cv, [[(0.18, 0.83), (0.4, 0.81), (0.46, 0.9), (0.22, 0.93)]], (0.3, 0.5, 0.75), blur=0.004)
    person(cv, 0.3, 0.88, 0.36, top=(0.95, 0.6, 0.3), dress='knee', hairstyle='wave', hair=(0.35, 0.22, 0.12),
           hat='sunhat', hat_col=(0.95, 0.9, 0.7), pose='sitfront', legs_col=SKIN, short_sleeves=True,
           arms=((15, -40), (15, -50)), blur=0.004, light=(-0.4, -1), shade_amt=0.15)
    umbrella(cv, 0.33, 0.42, 0.24, 0.48, [(0.95, 0.95, 0.92), (0.9, 0.3, 0.25)])
    # Eleanor running toward the water, Danny's beach ball
    person(cv, 0.72, 0.72, 0.28, top=(0.2, 0.55, 0.65), dress='knee', legs_col=SKIN, short_sleeves=True,
           hairstyle='long', hair=(0.5, 0.35, 0.18), pose='stride', arms=(60, 40), view='back', blur=0.004,
           light=(-0.4, -1))
    blob(cv, 0.85, 0.8, 0.03, 0.03, (0.95, 0.9, 0.85), shade_amt=0.4)
    cv.ellipse(0.85, 0.8, 0.03, 0.01, (0.9, 0.25, 0.2), blur=0.002, alpha=0.8)
    # dune grass along the bottom edge, out of focus
    for _ in range(80):
        x = r.uniform(-0.05, 1.05)
        cv.line([(x, 1.02), (x + r.uniform(-0.05, 0.05), r.uniform(0.82, 0.93))], 0.006, (0.55, 0.6, 0.35),
                blur=0.008, alpha=0.7)


def sc_campfire(cv):
    r = cv.rng
    cv.vgrad([(0, (0.04, 0.06, 0.14)), (0.5, (0.1, 0.12, 0.22)), (0.6, (0.05, 0.05, 0.07))])
    for _ in range(40):
        cv.ellipse(r.uniform(0, 1), r.uniform(0, 0.4), 0.002, 0.002, (1, 1, 1), alpha=r.uniform(0.2, 0.7),
                   mode='add')
    for i in range(12):
        pine(cv, r.uniform(-0.05, 1.05), 0.6, r.uniform(0.3, 0.55), col=(0.02, 0.03, 0.03), blur=0.004)
    cv.rect(0, 0.6, 1, 1, (0.06, 0.05, 0.05))
    cv.glow(0.5, 0.78, 0.35, (0.9, 0.4, 0.1), 0.35)
    # the family around the fire, lit from it
    for x, h, kw in ((0.2, 0.42, dict(top=(0.5, 0.3, 0.25), hat='cap', turn=1)),
                     (0.33, 0.36, dict(top=(0.4, 0.45, 0.6), dress='mid', hairstyle='wave', turn=1)),
                     (0.68, 0.38, dict(top=(0.6, 0.55, 0.4), hairstyle='long', dress='mid', facing=-1, turn=1)),
                     (0.82, 0.34, dict(top=(0.3, 0.35, 0.3), child=True, facing=-1, turn=1))):
        person(cv, x, 0.86, h, pose='sitfront', blur=0.004, light=((0.5 - x) * 4, 0.2), rim=0.9,
               rim_col=(1, 0.55, 0.2), shade_amt=0.6, hair=(0.3, 0.2, 0.12), arms=((20, -40), (30, 20)),
               **kw)
    cv.line([(0.26, 0.7), (0.45, 0.76)], 0.003, (0.35, 0.25, 0.15), blur=0.002)
    cv.line([(0.62, 0.69), (0.53, 0.75)], 0.003, (0.35, 0.25, 0.15), blur=0.002)
    # logs and flames
    for a, b in (((0.42, 0.88), (0.58, 0.84)), ((0.43, 0.84), (0.57, 0.88))):
        cv.line([a, b], 0.025, (0.2, 0.12, 0.08), blur=0.003)
    for k in range(9):
        x = 0.5 + r.normal(0, 0.02)
        hgt = r.uniform(0.08, 0.17)
        w = r.uniform(0.02, 0.035)
        col = mix((1, 0.55, 0.1), (1, 0.9, 0.5), r.random())
        cv.poly([(x - w, 0.86), (x + r.uniform(-0.02, 0.02), 0.86 - hgt), (x + w, 0.86)], col, blur=0.008, alpha=0.8,
                mode='add')
    cv.glow(0.5, 0.82, 0.05, (1, 0.8, 0.4), 0.9)
    for _ in range(30):
        cv.ellipse(0.5 + r.normal(0, 0.05), r.uniform(0.4, 0.75), 0.0025, 0.0025, (1, 0.7, 0.3), alpha=0.8,
                   mode='add')
    light_field(cv, 0.5, 0.8, 0.8, 0.35, 1.2)


# ================================================================ the later years
def cake(cv, x, y, w, h, tiers=2, col=(0.97, 0.96, 0.93), trim=(0.9, 0.6, 0.65), candles=0, gold=False):
    """Iced cake standing on a table at (x, y) bottom-centre; w, h in H units."""
    for t in range(tiers):
        ww = w * (1 - 0.3 * t)
        hh = h / tiers
        yb = y - t * hh
        g = Group(cv)
        X, Wp = x * cv.W, ww * cv.H / 2
        g.rect(X - Wp, (yb - hh) * cv.H, X + Wp, yb * cv.H, col)
        g.ellipse(X, yb * cv.H, Wp, ww * 0.12 * cv.H, col)
        g.ellipse(X, (yb - hh) * cv.H, Wp, ww * 0.12 * cv.H, shade(col, 1.03))
        g.commit(blur=0.003, light=(-0.4, -1), ao=0.4, shade_amt=0.15, rim=0.0, round_=0, tex=0.03)
        for k in range(14):
            a = math.pi * (k + 0.5) / 14
            cv.ellipse(x - math.cos(a) * ww / 2 / cv.aspect, yb - hh + math.sin(a) * ww * 0.12, 0.009, 0.008,
                       trim, blur=0.002)
            cv.ellipse(x - math.cos(a) * ww / 2 / cv.aspect, yb + math.sin(a) * ww * 0.12 - 0.004, 0.008, 0.007,
                       trim, blur=0.002, alpha=0.8)
    top = y - h - w * 0.06
    for k in range(candles):
        cx = x + (k - (candles - 1) / 2) * 0.035 / cv.aspect * 1.4
        cv.rect(cx - 0.004 / cv.aspect * 1.4, top - 0.07, cx + 0.004 / cv.aspect * 1.4, top, (0.95, 0.92, 0.85))
        cv.ellipse(cx, top - 0.083, 0.006, 0.014, (1, 0.95, 0.75), blur=0.002)
        cv.glow(cx, top - 0.085, 0.025, (1, 0.75, 0.4), 0.5)


def sc_anniversary_40(cv):
    r = cv.rng
    cv.vgrad([(0, (0.2, 0.15, 0.12)), (0.6, (0.32, 0.24, 0.18)), (1, (0.22, 0.17, 0.13))])
    for x in np.arange(0.0, 1.0, 0.16):  # wood panelling
        cv.rect(x + 0.005, 0.1, x + 0.15, 0.7, (0.4, 0.3, 0.22), alpha=0.35, blur=0.01)
    bokeh(cv, [(r.uniform(0, 1), r.uniform(0.0, 0.35)) for _ in range(26)], 0.035, [(1, 0.8, 0.55)], 0.18, 0.012)
    for i in range(8):  # guests, out of focus
        person(cv, r.uniform(0, 1), 0.95, 0.62, top=mix((0.25, 0.25, 0.32), (0.7, 0.52, 0.5), r.random()),
               hairstyle=r.choice(['short', 'wave', 'thin']), dress=r.choice([None, 'knee']), blur=0.015, rim=0.05,
               alpha=0.85, hair=mix((0.2, 0.15, 0.1), (0.8, 0.78, 0.75), r.random()))
    shapes(cv, [[(0.2, 0.05), (0.8, 0.05), (0.8, 0.15), (0.2, 0.15)]], (0.95, 0.93, 0.86), blur=0.005)
    cv.text((0.5, 0.1), 'HAPPY 40th ANNIVERSARY', 'serif_b', 0.055, (0.72, 0.55, 0.2), blur=0.004)
    cv.blur(0.01)
    for x, y, c in ((0.07, 0.24, (0.95, 0.95, 0.95)), (0.14, 0.19, (0.85, 0.2, 0.25)), (0.03, 0.15, (0.95, 0.8, 0.3)),
                    (0.93, 0.22, (0.85, 0.2, 0.25)), (0.98, 0.15, (0.95, 0.95, 0.95))):
        balloon(cv, x, y, 0.075, c, string_to=(x + 0.01, 0.75))
    # Walter and June cutting the cake together
    g, _ = person(cv, 0.41, 1.25, 1.0, top=(0.16, 0.18, 0.28), hairstyle='thin', hair=(0.8, 0.8, 0.78),
                  skin=SKIN_OLD, arms=(8, (-10, -70)), commit=False, turn=1.0, facing=1)
    X, U = 0.41 * cv.W, 1.0 * cv.H
    shY = 1.25 * cv.H - (0.48 + 0.335) * U
    g.poly([(X - 0.02 * U, shY), (X + 0.02 * U, shY), (X + 0.008 * U, shY + 0.16 * U), (X - 0.008 * U, shY + 0.16 * U)],
           (0.92, 0.9, 0.88))
    g.poly([(X - 0.007 * U, shY + 0.01 * U), (X + 0.007 * U, shY + 0.01 * U), (X + 0.005 * U, shY + 0.15 * U),
            (X - 0.005 * U, shY + 0.15 * U)], (0.55, 0.15, 0.2))
    person(cv, 0.57, 1.25, 0.92, top=DRESS_ROSE, dress='mid', hairstyle='wave', hair=(0.86, 0.85, 0.83),
           skin=SKIN_OLD, arms=((-10, -70), 10), g=g, commit=False, turn=1.0, facing=-1)
    g.commit(blur=0.005, light=(0.1, -1), rim=0.15, shade_amt=0.2, round_=0.006, ao=0.3)
    box(cv, -0.02, 0.8, 1.02, 1.02, (0.94, 0.93, 0.9), light=(0, -1), ao=0.05, tex=0.05)
    cake(cv, 0.5, 0.86, 0.36, 0.24, tiers=2, candles=0, trim=(0.92, 0.75, 0.78))
    cv.text((0.5, 0.78), '40', 'hand', 0.07, (0.75, 0.58, 0.25), blur=0.002)
    cv.line([(0.47, 0.5), (0.53, 0.62)], 0.006, (0.85, 0.85, 0.85), blur=0.002)  # the knife
    light_field(cv, 0.5, 0.55, 0.85, 0.4, 1.1)


def sc_leaves(cv):
    r = cv.rng
    cv.vgrad([(0, (0.75, 0.8, 0.85)), (0.5, (0.9, 0.85, 0.75))])
    for i in range(7):
        tree(cv, r.uniform(-0.05, 1.05), 0.55, r.uniform(0.5, 0.8),
             crown=r.choice([(0.85, 0.5, 0.15), (0.9, 0.7, 0.2), (0.7, 0.3, 0.12)]), blur=0.015, spread=1.3, n=18)
    bungalow(cv, 0.6, 1.2, 0.55, 0.28, 0.12, wall=(0.9, 0.88, 0.82), blur=0.012)
    cv.rect(0, 0.54, 1, 1, (0.5, 0.55, 0.32), blur=0.006)
    ground_tex(cv, 0.55, None, 0.2)
    cv.blur(0.01)
    leaf_cols = [(0.85, 0.45, 0.12), (0.9, 0.65, 0.2), (0.65, 0.3, 0.12), (0.75, 0.5, 0.2), (0.55, 0.35, 0.18)]
    for _ in range(500):  # leaves on the lawn, thicker in the pile
        if r.random() < 0.6:
            x, y = 0.45 + r.normal(0, 0.12), 0.8 + r.normal(0, 0.05)
        else:
            x, y = r.uniform(0, 1), r.uniform(0.6, 1)
        cv.ellipse(x, y, 0.012, 0.007, r.choice(leaf_cols), blur=0.003, alpha=0.9)
    blob(cv, 0.45, 0.8, 0.28, 0.08, (0.7, 0.42, 0.15), ao=0.5, tex=0.4, blur=0.005, alpha=0.7)
    for _ in range(200):
        x, y = 0.45 + r.normal(0, 0.11), 0.78 + r.normal(0, 0.035)
        cv.ellipse(x, y, 0.012, 0.007, r.choice(leaf_cols), blur=0.003, alpha=0.95)
    # Danny mid-jump, Peggy half-buried in the pile
    person(cv, 0.38, 0.62, 0.3, top=(0.25, 0.45, 0.7), bottom=(0.3, 0.3, 0.4), child=True, arms=(150, 140),
           pose='stride', hair=(0.55, 0.38, 0.2), blur=0.006, light=(-0.6, -0.8))
    person(cv, 0.58, 0.86, 0.3, top=(0.85, 0.3, 0.45), child=True, hairstyle='long', hair=(0.45, 0.3, 0.16),
           pose='floor', arms=(120, 100), blur=0.0045, light=(-0.6, -0.8), turn=-1)
    for _ in range(80):
        x, y = 0.55 + r.normal(0, 0.06), 0.8 + r.normal(0, 0.03)
        cv.ellipse(x, y, 0.012, 0.007, r.choice(leaf_cols), blur=0.003, alpha=0.95)
    for _ in range(40):  # leaves in the air
        cv.ellipse(r.uniform(0.25, 0.7), r.uniform(0.45, 0.75), 0.012, 0.008, r.choice(leaf_cols), blur=0.006,
                   alpha=0.9)
    cv.line([(0.85, 0.95), (0.95, 0.45)], 0.006, (0.6, 0.45, 0.3), blur=0.004)  # rake
    cv.line([(0.82, 0.97), (0.9, 0.93)], 0.012, (0.3, 0.6, 0.3), blur=0.004)


def sc_tire_swing(cv):
    r = cv.rng
    cv.vgrad([(0, (0.7, 0.8, 0.85)), (0.6, (0.75, 0.82, 0.7))])
    for _ in range(25):
        cv.ellipse(r.uniform(0, 1), r.uniform(0, 0.6), 0.12, 0.08, shade((0.35, 0.5, 0.28), r.uniform(0.8, 1.3)),
                   blur=0.03, alpha=0.8)
    cv.rect(0, 0.6, 1, 1, (0.4, 0.55, 0.28), blur=0.01)
    ground_tex(cv, 0.6, None, 0.2)
    cv.blur(0.012)
    # trunk and the branch
    shapes(cv, [[(-0.05, 1.02), (-0.05, -0.02), (0.2, -0.02), (0.18, 0.4), (0.22, 1.02)]], (0.35, 0.28, 0.22),
           light=(1, -0.3), ao=0.4, tex=0.35, blur=0.006)
    shapes(cv, [[(0.1, 0.02), (1.05, -0.02), (1.05, 0.04), (0.15, 0.09)]], (0.3, 0.24, 0.18), light=(0, -1),
           tex=0.3, blur=0.006)
    for _ in range(20):
        cv.ellipse(r.uniform(0.2, 1.05), r.uniform(-0.05, 0.06), 0.06, 0.03, (0.25, 0.4, 0.2), blur=0.012)
    # rope, tire and Peggy
    tx, ty = 0.6, 0.62
    cv.line([(0.62, 0.04), (tx, ty - 0.08)], 0.006, (0.75, 0.68, 0.55), blur=0.002)
    shadow(cv, 0.62, 0.95, 0.12, 0.02, 0.4)
    person(cv, tx, ty + 0.05, 0.3, top=(0.95, 0.75, 0.3), dress='knee', child=True, hairstyle='long',
           hair=(0.5, 0.35, 0.18), pose='sitfront', arms=(170, 170), blur=0.004, light=(-0.6, -0.8), legs_col=SKIN)
    g = Group(cv)
    U = cv.H
    g.ellipse(tx * cv.W, ty * U, 0.13 * U, 0.05 * U, (0.12, 0.12, 0.13))
    g.ellipse(tx * cv.W, ty * U - 0.008 * U, 0.08 * U, 0.025 * U, (0.0, 0.0, 0.0))
    g.commit(blur=0.004, light=(-0.6, -1), ao=0.3, rim=0.2, round_=0)
    cv.ellipse(tx, ty - 0.01, 0.07, 0.022, (0.95, 0.75, 0.3), blur=0.004)  # her skirt over the rim
    # Grandpa Walter, behind, ready to push
    person(cv, 0.33, 0.92, 0.62, top=(0.55, 0.3, 0.28), bottom=(0.5, 0.48, 0.42), hairstyle='thin',
           hair=(0.82, 0.82, 0.8), skin=SKIN_OLD, arms=((40, 60), 10), blur=0.0045, light=(-0.6, -0.8), turn=1)
    cv.rect(0.27, 0.42, 0.39, 0.6, (0.4, 0.2, 0.18), alpha=0.25, blur=0.01)  # plaid hint


def mylar_digit(cv, ch, x, y, size, col=(0.85, 0.68, 0.3)):
    m = cv.mask(lambda d: d.text((x * cv.W, y * cv.H), ch, font=font('serif_b', size * cv.H), fill=255,
                                 anchor='mm'), 0)
    m2 = gauss(m, size * cv.H * 0.03)
    m = np.clip(m2 * 1.6 - 0.3, 0, 1)
    inner = gauss(m, size * cv.H * 0.04)
    field = np.asarray(col, np.float32)[None, None] * (0.55 + 0.7 * inner[..., None])
    hl = np.clip(inner - np.roll(np.roll(inner, 6, 0), 6, 1), 0, 1)
    field = field + hl[..., None] * 1.6
    cv.apply(m, field)


def sc_anniversary_50(cv):
    r = cv.rng
    cv.vgrad([(0, (0.82, 0.8, 0.75)), (1, (0.65, 0.6, 0.55))])
    for x in np.arange(0, 1, 0.08):
        cv.line([(x, 0), (x, 0.7)], 0.01, (0.9, 0.88, 0.82), alpha=0.4)
    cv.blur(0.006)
    mylar_digit(cv, '5', 0.33, 0.2, 0.3)
    mylar_digit(cv, '0', 0.68, 0.22, 0.3)
    cv.line([(0.33, 0.35), (0.42, 0.6)], 0.002, (0.9, 0.9, 0.9), alpha=0.5)
    cv.line([(0.68, 0.37), (0.58, 0.6)], 0.002, (0.9, 0.9, 0.9), alpha=0.5)
    cv.blur(0.004)
    g, _ = person(cv, 0.36, 1.05, 0.75, top=(0.2, 0.22, 0.3), hairstyle='thin', hair=(0.85, 0.85, 0.83),
                  skin=SKIN_OLD, arms=(8, (-10, -60)), commit=False, turn=0.8, pose='sitfront')
    person(cv, 0.64, 1.05, 0.7, top=(0.7, 0.62, 0.8), dress='mid', hairstyle='wave', hair=(0.9, 0.89, 0.87),
           skin=SKIN_OLD, arms=((-10, -60), 8), g=g, commit=False, turn=0.8, facing=-1, pose='sitfront')
    g.commit(blur=0.0045, light=(0, -1), rim=0.15, shade_amt=0.2, round_=0.006, ao=0.3)
    cv.ellipse(0.48, 0.47, 0.025, 0.03, (0.95, 0.85, 0.85), blur=0.004)  # corsage
    box(cv, -0.02, 0.76, 1.02, 1.02, (0.95, 0.94, 0.9), light=(0, -1), ao=0.05, tex=0.05)
    cake(cv, 0.5, 0.88, 0.42, 0.14, tiers=1, trim=(0.9, 0.75, 0.35), candles=0)
    cv.text((0.5, 0.82), '50', 'hand', 0.075, (0.8, 0.62, 0.22), blur=0.002)
    for x in (0.12, 0.88):
        cv.ellipse(x, 0.82, 0.04, 0.012, (0.85, 0.85, 0.88), blur=0.003)
        cv.rect(x - 0.008, 0.72, x + 0.008, 0.82, (0.9, 0.9, 0.92), alpha=0.6, blur=0.002)  # glasses
    light_field(cv, 0.5, 0.5, 0.95, 0.45, 1.1)


def sc_june_garden(cv):
    r = cv.rng
    cv.vgrad([(0, (0.55, 0.7, 0.88)), (0.4, (0.8, 0.86, 0.9))])
    treeline(cv, 0.42, 0.12, (0.3, 0.45, 0.25), blur=0.01)
    for x in np.arange(0, 1.02, 0.03):  # fence
        cv.rect(x, 0.33, x + 0.018, 0.55, (0.95, 0.95, 0.93), blur=0.004)
    cv.rect(0, 0.4, 1, 0.415, (0.93, 0.93, 0.9), blur=0.004)
    cv.rect(0, 0.52, 1, 1, (0.35, 0.5, 0.25))
    ground_tex(cv, 0.52, None, 0.25)
    # hollyhocks along the fence
    for x in np.arange(0.03, 0.97, 0.07):
        hgt = r.uniform(0.25, 0.4)
        cv.line([(x, 0.6), (x + r.uniform(-0.01, 0.01), 0.6 - hgt)], 0.006, (0.3, 0.45, 0.2), blur=0.003)
        col = r.choice([(0.95, 0.45, 0.6), (0.9, 0.25, 0.35), (0.98, 0.85, 0.9), (0.95, 0.75, 0.3)])
        for k in range(7):
            cv.ellipse(x + r.uniform(-0.012, 0.012), 0.6 - hgt * (0.3 + 0.1 * k), 0.016, 0.016, col, blur=0.004)
    cv.blur(0.004)
    # rose bed in front
    for _ in range(18):
        shrub(cv, r.uniform(0, 1), r.uniform(0.8, 1.0), 0.06, col=(0.25, 0.42, 0.2), blur=0.006)
    for _ in range(40):
        cv.ellipse(r.uniform(0, 1), r.uniform(0.72, 0.98), 0.016, 0.014, r.choice([(0.9, 0.25, 0.3), (0.98, 0.7, 0.75)]),
                   blur=0.006)
    person(cv, 0.55, 0.82, 0.5, top=(0.82, 0.88, 0.95), bottom=(0.6, 0.6, 0.65), hairstyle='wave',
           hair=(0.92, 0.92, 0.9), skin=SKIN_OLD, hat='sunhat', hat_col=(0.9, 0.85, 0.65), arms=((30, -40), 20),
           blur=0.003, light=(-0.5, -1), rim=0.3, turn=1, facing=-1)
    shapes(cv, [[(0.6, 0.62), (0.66, 0.6), (0.68, 0.68), (0.61, 0.69)]], (0.4, 0.6, 0.45), blur=0.003)  # watering can
    cv.line([(0.66, 0.63), (0.72, 0.58)], 0.006, (0.4, 0.6, 0.45), blur=0.002)


def sc_last_christmas(cv):
    r = cv.rng
    cv.fill((0.55, 0.42, 0.32))
    cv.noise_tint((0.45, 0.33, 0.25), 0.3)
    window_frame(cv, 0.06, 0.12, 0.26, 0.55, (0.12, 0.16, 0.3), trim=(0.9, 0.88, 0.82))
    cv.rect(0, 0.78, 1, 1, (0.35, 0.25, 0.2))
    # lamp
    cv.glow(0.32, 0.35, 0.12, (1, 0.8, 0.5), 0.5)
    shapes(cv, [[(0.28, 0.3), (0.36, 0.3), (0.38, 0.4), (0.26, 0.4)]], (1, 0.9, 0.7), blur=0.004, ao=0, shade_amt=0)
    # the tree with warm white lights, far right, out of focus
    shapes(cv, [[(0.78, 0.82), (0.9, 0.05), (1.05, 0.82)]], (0.1, 0.22, 0.12), blur=0.012, tex=0.3)
    pts = []
    for _ in range(50):
        y = r.uniform(0.1, 0.8)
        w = (y - 0.05) * 0.18
        pts.append((0.91 + r.uniform(-w, w), y))
    bokeh(cv, pts, 0.03, [(1, 0.85, 0.55), (1, 0.75, 0.45)], 0.55, 0.004)
    cv.blur(0.008)
    # sofa
    g = Group(cv)
    g.rect(0.12 * cv.W, 0.36 * cv.H, 0.85 * cv.W, 0.9 * cv.H, (0.45, 0.35, 0.3), r=0.04 * cv.H)
    g.commit(blur=0.005, light=(-0.6, -0.8), ao=0.4, tex=0.12, round_=0)
    fam = [(0.22, dict(top=(0.3, 0.35, 0.55), hairstyle='long', hair=(0.5, 0.35, 0.2), dress='mid', turn=1)),
           (0.4, dict(top=(0.7, 0.15, 0.2), hairstyle='wave', hair=(0.92, 0.92, 0.9), dress='mid', skin=SKIN_OLD,
                      turn=0.8)),
           (0.55, dict(top=(0.3, 0.32, 0.3), hairstyle='thin', hair=(0.92, 0.92, 0.9), skin=SKIN_OLD, turn=-0.8,
                       facing=-1)),
           (0.73, dict(top=(0.55, 0.5, 0.45), hairstyle='short', hair=(0.4, 0.28, 0.16), turn=-1, facing=-1))]
    for x, kw in fam:
        person(cv, x, 0.98, 0.82, pose='sitfront', arms=((15, -55), (15, -45)), blur=0.0045, light=(-0.4, -0.9),
               rim=0.25, rim_col=(1, 0.85, 0.6), **kw)
    box(cv, 0.12, 0.8, 0.85, 0.95, (0.42, 0.32, 0.28), light=(-0.6, -0.8), ao=0.3, tex=0.1)  # sofa seat front
    for x0, w, col in ((0.3, 0.1, (0.8, 0.2, 0.2)), (0.6, 0.08, (0.85, 0.75, 0.4)), (0.45, 0.12, (0.25, 0.4, 0.6))):
        box(cv, x0, 0.92, x0 + w, 1.0, col, light=(-0.6, -0.8))
    light_field(cv, 0.45, 0.5, 1.0, 0.55, 1.0)


def sc_walter_porch(cv):
    r = cv.rng
    cv.vgrad([(0, (0.85, 0.88, 0.85)), (1, (0.55, 0.6, 0.45))])
    for _ in range(20):
        cv.ellipse(r.uniform(0.3, 1.1), r.uniform(0.0, 0.55), 0.1, 0.08, shade((0.45, 0.58, 0.32), r.uniform(0.8, 1.3)),
                   blur=0.03)
    bokeh(cv, [(r.uniform(0.35, 1), r.uniform(0.0, 0.5)) for _ in range(25)], 0.03, [(1, 0.95, 0.75)], 0.25, 0.01)
    cv.blur(0.016)
    box(cv, -0.02, -0.02, 0.32, 1.02, (0.85, 0.82, 0.76), light=(1, -0.2), ao=0.0, tex=0.06)  # house wall
    siding(cv, -0.02, 0, 0.32, 1, (0.85, 0.82, 0.76), gap=0.03, alpha=0.45)
    box(cv, 0.3, -0.02, 0.36, 0.8, (0.95, 0.94, 0.9), light=(1, -0.2), shade_amt=0.4)  # porch post
    cv.poly([(0, 0.8), (1, 0.78), (1, 1), (0, 1)], (0.55, 0.5, 0.45), blur=0.003)
    for x in np.arange(-0.2, 1.2, 0.06):
        cv.line([(0.5 + (x - 0.5) * 0.8, 0.79), (0.5 + (x - 0.5) * 1.4, 1)], 0.003, (0.4, 0.36, 0.32), alpha=0.4)
    # golden late-afternoon light
    cv.glow(0.9, 0.2, 0.5, (1, 0.85, 0.6), 0.25)
    armchair(cv, 0.58, 0.9, 0.3, 0.52, (0.75, 0.68, 0.55), light=(0.8, -0.6), part='back')
    g, hands = person(cv, 0.58, 0.86, 0.62, top=(0.45, 0.42, 0.35), bottom=(0.5, 0.48, 0.45), hairstyle='thin',
                      hair=(0.93, 0.93, 0.92), skin=SKIN_OLD, pose='sitfront', arms=((10, -60), (25, -10)),
                      commit=False, turn=1.0, facing=1)
    U = 0.62 * cv.H
    X = 0.58 * cv.W
    shY = 0.86 * cv.H - 0.27 * U - 0.335 * U
    g.poly([(X - 0.03 * U, shY), (X + 0.03 * U, shY), (X, shY + 0.1 * U)], (0.9, 0.88, 0.85))  # collar
    g.commit(blur=0.0035, light=(0.8, -0.6), rim=0.45, rim_col=(1, 0.85, 0.6), round_=0.005, ao=0.35, shade_amt=0.35)
    armchair(cv, 0.58, 0.9, 0.3, 0.52, (0.75, 0.68, 0.55), light=(0.8, -0.6), part='arms')
    cv.line([(0.76, 0.88), (0.72, 0.5)], 0.008, (0.3, 0.22, 0.15), blur=0.003)  # his cane
    cv.ellipse(0.715, 0.5, 0.018, 0.01, (0.3, 0.22, 0.15), blur=0.003)
    box(cv, 0.84, 0.72, 0.96, 0.84, (0.7, 0.4, 0.3), r=0.01)  # flower pot
    shrub(cv, 0.9, 0.72, 0.07, col=(0.3, 0.45, 0.25))
    for _ in range(10):
        cv.ellipse(0.9 + r.uniform(-0.05, 0.05), 0.68 + r.uniform(-0.04, 0.03), 0.012, 0.012, (0.95, 0.3, 0.4),
                   blur=0.004)


# ================================================================ keepsakes (photographed objects)
def linen(cv, base=(0.86, 0.83, 0.77)):
    cv.fill(base)
    H, W = cv.H, cv.W
    rng = cv.rng
    rows = np.asarray(Image.fromarray(rng.random((H, max(2, W // 60))).astype(np.float32), 'F')
                      .resize((W, H), Image.BILINEAR))
    cols = np.asarray(Image.fromarray(rng.random((max(2, H // 60), W)).astype(np.float32), 'F')
                      .resize((W, H), Image.BILINEAR))
    weave = (rows - 0.5) * 0.05 + (cols - 0.5) * 0.05
    cv.a *= (1 + weave)[..., None]
    cv.noise_tint(shade(base, 0.85), 0.35, (2, 4, 8))


def wood_surface(cv, base=(0.45, 0.3, 0.2), dark=(0.28, 0.17, 0.1), vertical=False, scale=1.0):
    rng = cv.rng
    H, W = cv.H, cv.W
    t = cv.xx if vertical else cv.yy
    warp = fnoise(H, W, rng, (2, 4), aspect=None)
    rings = 0.5 + 0.5 * np.sin((t * 38 * scale + warp * 5) * math.pi)
    if vertical:
        streak = np.asarray(Image.fromarray(rng.random((H // 30 + 2, W // 2)).astype(np.float32), 'F')
                            .resize((W, H), Image.BICUBIC))
    else:
        streak = np.asarray(Image.fromarray(rng.random((H // 2, W // 30 + 2)).astype(np.float32), 'F')
                            .resize((W, H), Image.BICUBIC))
    k = np.clip(0.55 * rings ** 3 + 0.45 * streak, 0, 1)
    b, d = np.asarray(base, np.float32), np.asarray(dark, np.float32)
    cv.a[:] = b * (1 - k[..., None]) + d * k[..., None]


class Obj:
    """An object drawn flat on its own canvas with an alpha mask, then laid onto the surface."""

    def __init__(self, w, h, seed):
        self.cv = Canvas(w, h, seed)
        self.alpha = np.zeros((h, w), np.float32)

    def shape(self, draw):
        m = Image.new('L', (self.cv.W, self.cv.H), 0)
        draw(ImageDraw.Draw(m), self.cv.W, self.cv.H)
        m = m.filter(ImageFilter.GaussianBlur(0.7))
        self.alpha = np.maximum(self.alpha, np.asarray(m, np.float32) / 255)


def lay(cv, obj, cx, cy, angle=0.0, lift=0.012, shadow_alpha=0.45, shadow_blur=0.012, light=(-0.5, -0.8)):
    rgb = np.clip(obj.cv.a, 0, 1)
    rgba = np.dstack([rgb, obj.alpha])
    im = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), 'RGBA')
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    arr = np.asarray(im, np.float32) / 255
    h, w = arr.shape[:2]
    X0 = int(cx * cv.W - w / 2)
    Y0 = int(cy * cv.H - h / 2)
    full_a = np.zeros((cv.H, cv.W), np.float32)
    full_rgb = np.zeros((cv.H, cv.W, 3), np.float32)
    xs0, ys0 = max(0, X0), max(0, Y0)
    xs1, ys1 = min(cv.W, X0 + w), min(cv.H, Y0 + h)
    full_a[ys0:ys1, xs0:xs1] = arr[ys0 - Y0:ys1 - Y0, xs0 - X0:xs1 - X0, 3]
    full_rgb[ys0:ys1, xs0:xs1] = arr[ys0 - Y0:ys1 - Y0, xs0 - X0:xs1 - X0, :3]
    off = lift * cv.H
    sh = np.roll(np.roll(full_a, int(-light[1] * off), 0), int(-light[0] * off), 1)
    sh = gauss(sh, shadow_blur * cv.H)
    cv.a *= (1 - shadow_alpha * sh)[..., None]
    contact = gauss(full_a, 2.0)
    cv.a *= (1 - 0.25 * contact)[..., None]
    A = full_a[..., None]
    cv.a = cv.a * (1 - A) + full_rgb * A


def handwrite(cv, lines, x0, y0, lh, size, ink, fname='hand', slope=0.0, jitter=0.12, width=None, alpha=0.92):
    """Lines of handwriting: per-word baseline wobble, per-line drift, ink pressure."""
    rng = cv.rng
    m = Image.new('L', (cv.W, cv.H), 0)
    px = size * cv.H
    for i, line in enumerate(lines):
        if not line:
            continue
        if isinstance(line, tuple):
            line, dx, sz = line
        else:
            dx, sz = 0.0, 1.0
        f = font(fname, px * sz * rng.uniform(0.97, 1.03))
        L = Image.new('L', (cv.W, int(px * 3)), 0)
        d = ImageDraw.Draw(L)
        x = (x0 + dx) * cv.W
        for word in line.split(' '):
            yy = px * 1.2 + rng.normal(0, px * jitter * 0.4)
            d.text((x, yy), word, font=f, fill=int(255 * rng.uniform(0.82, 1.0)), anchor='ls')
            x += f.getlength(word + ' ') * rng.uniform(0.97, 1.08)
        L = L.rotate(rng.normal(slope, 0.5), resample=Image.BICUBIC, center=(x0 * cv.W, px * 1.2))
        top = int((y0 + i * lh) * cv.H - px * 1.2 + rng.normal(0, px * 0.05))
        m.paste(Image.composite(L, m.crop((0, top, cv.W, top + L.height)), L), (0, top))
    mm = np.asarray(m.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    pressure = 0.75 + 0.25 * fnoise(cv.H, cv.W, rng, (6, 14))
    cv.apply(mm * pressure, ink, alpha)


def sc_plaque(cv):
    linen(cv, (0.84, 0.81, 0.76))
    W, H = int(cv.W * 0.68), int(cv.H * 0.72)
    o = Obj(W, H, 7)
    c = o.cv
    R = int(0.06 * H)
    o.shape(lambda d, w, h: d.rounded_rectangle([0, 0, w - 1, h - 1], R, fill=255))
    wood_surface(c, (0.42, 0.25, 0.14), (0.24, 0.13, 0.07))
    # bevel: lighter top-left edge, darker bottom-right, routed groove
    for k, (col, a) in enumerate((((1, 0.9, 0.8), 0.22), ((0, 0, 0), 0.35))):
        m = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(m)
        if k == 0:
            d.rounded_rectangle([0, 0, W - 1, H - 1], R, outline=255, width=int(0.025 * H))
            mm = np.asarray(m.filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
            mm *= np.clip(1.2 - c.xx - c.yy, 0, 1)
        else:
            d.rounded_rectangle([0, 0, W - 1, H - 1], R, outline=255, width=int(0.025 * H))
            mm = np.asarray(m.filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
            mm *= np.clip(c.xx + c.yy - 0.8, 0, 1)
        c.apply(mm, col, a * 2)
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([0.05 * W, 0.06 * H, 0.95 * W, 0.94 * H], R * 0.7, outline=255,
                                        width=max(2, int(0.006 * H)))
    mm = np.asarray(m.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    c.apply(mm, (0.12, 0.06, 0.03), 0.7)
    c.apply(np.roll(np.roll(mm, 2, 0), 2, 1), (0.9, 0.75, 0.6), 0.2)
    # varnish sheen
    c.glow(0.3, 0.2, 0.35, (1, 0.95, 0.85), 0.12)
    # brass plate
    px0, py0, px1, py1 = 0.13, 0.17, 0.87, 0.83
    plate = c.vgrad([(0, (0.62, 0.48, 0.22)), (0.35, (0.93, 0.82, 0.52)), (0.6, (0.8, 0.66, 0.36)),
                     (1, (0.58, 0.44, 0.2))], apply=False, x=True)
    brushed = np.asarray(Image.fromarray(c.rng.random((H // 1, max(2, W // 80))).astype(np.float32), 'F')
                         .resize((W, H), Image.BILINEAR))
    plate = plate * (0.94 + 0.12 * brushed[..., None])
    plate *= (0.92 + 0.12 * (1 - c.yy))[..., None]
    pm = c.rect(px0, py0, px1, py1, plate, radius=0.01)
    c.rect(px0, py1 - 0.006, px1, py1 + 0.012, (0, 0, 0), blur=0.008, alpha=0.4)
    # engraved border and text: dark fill with a bright lower lip
    def engrave(draw):
        m = Image.new('L', (W, H), 0)
        draw(ImageDraw.Draw(m))
        mm = np.asarray(m.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
        c.apply(np.roll(np.roll(mm, 2, 0), 1, 1), (1, 0.95, 0.75), 0.5)
        c.apply(mm, (0.14, 0.1, 0.05), 0.92)
    engrave(lambda d: d.rounded_rectangle([(px0 + 0.025) * W, (py0 + 0.035) * H, (px1 - 0.025) * W,
                                           (py1 - 0.035) * H], 8, outline=255, width=3))
    cx = 0.5 * W
    engrave(lambda d: d.text((cx, 0.31 * H), 'WALTER HALE', font=font('serif_b', 0.085 * H), fill=255, anchor='mm'))
    engrave(lambda d: d.line([(cx - 0.12 * W, 0.4 * H), (cx + 0.12 * W, 0.4 * H)], fill=255, width=2))
    engrave(lambda d: d.text((cx, 0.49 * H), '25 Years of Faithful Service', font=font('serif_i', 0.07 * H),
                             fill=255, anchor='mm'))
    engrave(lambda d: d.text((cx, 0.6 * H), 'JOLIET STEEL WORKS', font=font('serif', 0.052 * H), fill=255,
                             anchor='mm'))
    engrave(lambda d: d.text((cx, 0.7 * H), '1947 – 1972', font=font('serif', 0.052 * H), fill=255,
                             anchor='mm'))
    for sx, sy in ((px0 + 0.03, py0 + 0.05), (px1 - 0.03, py0 + 0.05), (px0 + 0.03, py1 - 0.05),
                   (px1 - 0.03, py1 - 0.05)):
        c.ellipse(sx, sy, 0.013, 0.013, (0.55, 0.42, 0.2), blur=0.001)
        c.ellipse(sx - 0.002, sy - 0.003, 0.007, 0.007, (0.98, 0.9, 0.65), blur=0.002)
        c.line([(sx - 0.008, sy), (sx + 0.008, sy)], 0.003, (0.3, 0.22, 0.1))
    c.glow(0.4, 0.3, 0.25, (1, 0.95, 0.8), 0.15)
    lay(cv, o, 0.5, 0.5, angle=-2.5, lift=0.02, shadow_alpha=0.5, shadow_blur=0.018)
    light_field(cv, 0.45, 0.4, 1.1, 0.7, 1.2)


def sc_medal(cv):
    # navy velvet of the presentation case
    cv.fill((0.1, 0.12, 0.22))
    cv.noise_tint((0.05, 0.06, 0.12), 0.5, (3, 6, 12))
    n = gauss(cv.rng.standard_normal((cv.H, cv.W)).astype(np.float32), 1.0) * 0.03
    cv.a += n[..., None]
    light_field(cv, 0.4, 0.4, 1.0, 0.55, 1.0)
    W, H = int(cv.W * 0.42), int(cv.H * 0.82)
    o = Obj(W, H, 11)
    c = o.cv
    rib_h = 0.33
    o.shape(lambda d, w, h: d.polygon([(0.18 * w, 0), (0.82 * w, 0), (0.82 * w, rib_h * h), (0.18 * w, rib_h * h)],
                                      fill=255))
    stripes = [(0.82, 0.25, 0.2), (0.85, 0.75, 0.25), (0.25, 0.5, 0.3), (0.25, 0.35, 0.65), (0.55, 0.3, 0.55),
               (0.8, 0.2, 0.18), (0.9, 0.88, 0.85), (0.8, 0.2, 0.18), (0.55, 0.3, 0.55), (0.25, 0.35, 0.65),
               (0.25, 0.5, 0.3), (0.85, 0.75, 0.25), (0.82, 0.25, 0.2)]
    widths = [1, 1, 1, 1, 1, 2.5, 0.5, 2.5, 1, 1, 1, 1, 1]
    tot = sum(widths)
    x = 0.18
    for col, wdt in zip(stripes, widths):
        w = 0.64 * wdt / tot
        c.rect(x, 0, x + w + 0.002, rib_h, col)
        x += w
    weave = np.asarray(Image.fromarray(c.rng.random((H // 3, 4)).astype(np.float32), 'F').resize((W, H)))
    c.a *= (0.85 + 0.25 * weave)[..., None]
    c.a *= (0.8 + 0.3 * np.clip(1 - np.abs(c.xx - 0.45) * 2, 0, 1))[..., None]  # folds catch light
    c.rect(0.18, rib_h - 0.02, 0.82, rib_h, (0, 0, 0), blur=0.01, alpha=0.4)
    # ring and medal
    o.shape(lambda d, w, h: d.ellipse([0.44 * w, (rib_h - 0.005) * h, 0.56 * w, (rib_h + 0.055) * h], fill=255))
    c.ellipse(0.5, rib_h + 0.025, 0.028, 0.028, (0.55, 0.4, 0.22))
    c.ellipse(0.5, rib_h + 0.025, 0.016, 0.016, (0.1, 0.12, 0.22))
    mr = 0.29
    my = rib_h + 0.06 + mr * H / W * 0 + 0.29 * (W / H)
    o.shape(lambda d, w, h: d.ellipse([0.5 * w - mr * w, my * h - mr * w, 0.5 * w + mr * w, my * h + mr * w],
                                      fill=255))
    R = mr * W / H  # radius in H units
    bronze = np.asarray((0.62, 0.42, 0.24), np.float32)
    dx = (c.xx - 0.5) * c.aspect
    dy = c.yy - my
    rr = np.sqrt(dx * dx + dy * dy) / R
    lightf = 0.75 + 0.45 * np.clip(-(dx + dy) / R, -1, 1)
    field = bronze[None, None] * lightf[..., None]
    rim = np.clip(1 - np.abs(rr - 0.93) / 0.05, 0, 1)
    field += rim[..., None] * 0.15
    field *= (0.9 + 0.2 * fnoise(H, W, c.rng, (8, 20)))[..., None]
    m = (rr <= 1.0).astype(np.float32)
    c.apply(m, field)
    # embossed lettering around the rim and centre
    def emboss(draw, a=1.0):
        mm = Image.new('L', (W, H), 0)
        draw(ImageDraw.Draw(mm))
        mm = np.asarray(mm.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
        c.apply(np.roll(np.roll(mm, -2, 0), -2, 1), (1, 0.85, 0.6), 0.55 * a)
        c.apply(np.roll(np.roll(mm, 2, 0), 2, 1), (0.2, 0.12, 0.05), 0.55 * a)
        c.apply(mm, (0.7, 0.5, 0.3), 0.6 * a)
    txt = 'UNITED STATES OF AMERICA'
    f = font('serif_b', 0.032 * H)
    Rp = R * H * 0.78
    def arc(d):
        n = len(txt)
        for i, ch in enumerate(txt):
            ang = math.radians(-150 + 120 * i / (n - 1))
            px = 0.5 * W + Rp * math.cos(ang)
            py = my * H + Rp * math.sin(ang)
            ci = Image.new('L', (int(0.06 * H), int(0.06 * H)), 0)
            ImageDraw.Draw(ci).text((ci.width / 2, ci.height / 2), ch, font=f, fill=255, anchor='mm')
            ci = ci.rotate(-math.degrees(ang) - 90, resample=Image.BICUBIC)
            d._image.paste(255, (int(px - ci.width / 2), int(py - ci.height / 2)), ci)
    emboss(arc)
    emboss(lambda d: d.text((0.5 * W, my * H - 0.01 * H), 'WORLD WAR II', font=font('serif_b', 0.045 * H), fill=255,
                            anchor='mm'))
    emboss(lambda d: d.text((0.5 * W, my * H + 0.06 * H), '1941 – 1945', font=font('serif_b', 0.036 * H),
                            fill=255, anchor='mm'))
    emboss(lambda d: d.ellipse([0.5 * W - Rp * 1.12, my * H - Rp * 1.12, 0.5 * W + Rp * 1.12, my * H + Rp * 1.12],
                               outline=255, width=3), 0.6)
    c.glow(0.38, my - R * 0.4, 0.06, (1, 0.9, 0.75), 0.35)
    lay(cv, o, 0.5, 0.5, angle=4, lift=0.012, shadow_alpha=0.6, shadow_blur=0.01)


def index_card(o, ruled=True):
    c = o.cv
    W, H = c.W, c.H
    o.shape(lambda d, w, h: d.rounded_rectangle([0, 0, w - 1, h - 1], int(0.02 * h), fill=255))
    c.a[:] = _paper(H, W, c.rng, (0.95, 0.92, 0.84), 0.04)
    c.a *= (1 - 0.12 * gauss(1 - o.alpha, 0.03 * H))[..., None]  # aged edges
    if ruled:
        c.line([(0, 0.2), (1, 0.2)], 0.004, (0.85, 0.4, 0.45), alpha=0.7)
        for y in np.arange(0.29, 0.97, 0.088):
            c.line([(0, y), (1, y)], 0.0025, (0.5, 0.62, 0.8), alpha=0.6)


def sc_recipe(cv):
    wood_surface(cv, (0.68, 0.52, 0.36), (0.5, 0.36, 0.24), scale=0.6)  # butcher block
    dust = gauss((cv.rng.random((cv.H, cv.W)) > 0.985).astype(np.float32), 1.2) * 3
    haze = np.exp(-(((cv.xx - 0.88) * cv.aspect) ** 2 + (cv.yy - 0.12) ** 2) / (2 * 0.16 ** 2))
    cv.apply(np.clip(dust * haze, 0, 1), (1, 1, 1), 0.55)
    cv.apply(haze.astype(np.float32), (1, 0.98, 0.95), 0.22)
    W, H = int(cv.W * 0.7), int(cv.W * 0.7 * 3 / 5)
    o = Obj(W, H, 23)
    index_card(o)
    c = o.cv
    ink = (0.12, 0.16, 0.38)
    handwrite(c, [('Apple Pie', 0.0, 1.25)], 0.06, 0.14, 0.1, 0.08, ink)
    handwrite(c, [('from Mother', 0.0, 1.0)], 0.6, 0.15, 0.1, 0.055, ink)
    lines = ['6 tart apples (Jonathans) sliced thin',
             '3/4 cup sugar, 2 Tbsp flour',
             '1 tsp cinnamon, pinch of nutmeg',
             'squeeze of lemon, dot with butter',
             'Bake 425° about 50 min.',
             'till it bubbles thru the slits!']
    handwrite(c, lines, 0.06, 0.27, 0.088, 0.058, ink, jitter=0.15)
    # well-loved: a butter spot and a coffee ring
    c.ellipse(0.78, 0.62, 0.07, 0.06, (0.85, 0.72, 0.4), blur=0.02, alpha=0.35, mode='mul')
    ring = c.mask(lambda d: d.ellipse([0.08 * W, 0.6 * H, 0.08 * W + 0.36 * H, 0.96 * H], outline=255, width=5), 3)
    c.apply(ring, (0.7, 0.5, 0.3), 0.35)
    c.ellipse(0.35, 0.5, 0.25, 0.2, (0.9, 0.8, 0.6), blur=0.08, alpha=0.2, mode='mul')
    lay(cv, o, 0.46, 0.53, angle=4, lift=0.008, shadow_alpha=0.4, shadow_blur=0.008)
    light_field(cv, 0.45, 0.4, 1.1, 0.65, 1.2)


def sc_love_letter(cv):
    linen(cv, (0.88, 0.85, 0.8))
    # envelope underneath
    W, H = int(cv.W * 0.82), int(cv.W * 0.82 * 0.45)
    e = Obj(W, H, 31)
    e.shape(lambda d, w, h: d.rectangle([0, 0, w - 1, h - 1], fill=255))
    ec = e.cv
    ec.a[:] = _paper(H, W, ec.rng, (0.9, 0.86, 0.76), 0.05)
    ec.rect(0.86, 0.08, 0.96, 0.4, (0.45, 0.3, 0.5))
    ec.text((0.91, 0.24), '3¢', 'serif_b', 0.12, (0.9, 0.85, 0.85))
    pm = ec.mask(lambda d: d.ellipse([0.68 * W, 0.08 * H, 0.68 * W + 0.3 * H, 0.38 * H], outline=255, width=3), 0.6)
    ec.apply(pm, (0.25, 0.22, 0.25), 0.6)
    ec.text((0.68 + 0.15 * H / W, 0.2), 'JOLIET', 'sans_b', 0.04, (0.25, 0.22, 0.25), alpha=0.6)
    ec.text((0.68 + 0.15 * H / W, 0.27), 'MAR 1947', 'sans_b', 0.035, (0.25, 0.22, 0.25), alpha=0.6)
    for k in range(4):
        ec.line([(0.55, 0.12 + k * 0.04), (0.72, 0.13 + k * 0.04)], 0.006, (0.25, 0.22, 0.25), alpha=0.5)
    handwrite(ec, ['Miss June Novak', '412 Cass Street', 'Joliet, Illinois'], 0.36, 0.55, 0.13, 0.1,
              (0.15, 0.12, 0.25))
    lay(cv, e, 0.48, 0.82, angle=-6, lift=0.006, shadow_alpha=0.35)
    # the letter, folded in thirds
    W, H = int(cv.W * 0.66), int(cv.W * 0.66 * 1.3)
    o = Obj(W, H, 37)
    o.shape(lambda d, w, h: d.rectangle([0, 0, w - 1, h - 1], fill=255))
    c = o.cv
    c.a[:] = _paper(H, W, c.rng, (0.95, 0.93, 0.87), 0.04)
    for y in (1 / 3, 2 / 3):
        c.rect(0, y - 0.02, 1, y, (0, 0, 0), blur=0.02, alpha=0.08)
        c.line([(0, y), (1, y)], 0.002, (1, 1, 1), alpha=0.6)
        c.rect(0, y, 1, y + 0.03, (1, 1, 1), blur=0.02, alpha=0.1)
    ink = (0.12, 0.13, 0.32)
    handwrite(c, ['March 9, 1947'], 0.6, 0.07, 0.05, 0.03, ink)
    body = ['My dearest June,', '',
            'I have read your letter so many times',
            'the folds are wearing thin. Mother says',
            'I am no use to anyone this week and',
            'she is right. I keep thinking of the',
            'dance at the Rialto and how you laughed',
            'when I stepped on your foot - twice.',
            '',
            'I spoke to your father on Sunday.',
            'He did not say no. I am taking that',
            'as the best news a fellow could get.',
            '',
            'Save me every dance in June.', '']
    handwrite(c, body, 0.08, 0.14, 0.047, 0.034, ink, jitter=0.12)
    handwrite(c, [('All my love,', 0.42, 1.0), ('Walter', 0.5, 1.25)], 0.08, 0.86, 0.06, 0.036, ink)
    c.ellipse(0.85, 0.08, 0.14, 0.1, (0.85, 0.75, 0.55), blur=0.06, alpha=0.2, mode='mul')
    lay(cv, o, 0.5, 0.43, angle=3, lift=0.008, shadow_alpha=0.4)
    light_field(cv, 0.45, 0.35, 1.2, 0.65, 1.1)


def sc_report_card(cv):
    wood_surface(cv, (0.5, 0.36, 0.24), (0.32, 0.2, 0.12), scale=0.8)
    W, H = int(cv.W * 0.74), int(cv.W * 0.74 * 1.35)
    o = Obj(W, H, 41)
    o.shape(lambda d, w, h: d.rectangle([0, 0, w - 1, h - 1], fill=255))
    c = o.cv
    c.a[:] = _paper(H, W, c.rng, (0.86, 0.8, 0.64), 0.05)
    c.a *= (1 - 0.15 * gauss(1 - o.alpha, 0.03 * H))[..., None]
    t = (0.2, 0.18, 0.16)
    c.text((0.5, 0.06), 'JOLIET PUBLIC SCHOOLS', 'serif_b', 0.032, t)
    c.text((0.5, 0.1), 'Report to Parents', 'serif_i', 0.026, t)
    c.line([(0.1, 0.13), (0.9, 0.13)], 0.002, t)
    c.text((0.1, 0.17), 'Pupil', 'type', 0.019, t, anchor='lm')
    c.text((0.1, 0.205), 'Grade', 'type', 0.019, t, anchor='lm')
    c.text((0.55, 0.205), 'Year', 'type', 0.019, t, anchor='lm')
    c.text((0.1, 0.24), 'Teacher', 'type', 0.019, t, anchor='lm')
    for y, x0 in ((0.177, 0.2), (0.212, 0.2), (0.212, 0.63), (0.247, 0.24)):
        c.line([(x0, y), (0.9, y)], 0.0012, t, alpha=0.6)
    ink = (0.12, 0.14, 0.35)
    handwrite(c, [('Margaret Hale', 0.12, 1.0)], 0.1, 0.172, 0.04, 0.028, ink)
    handwrite(c, [('Four', 0.12, 1.0)], 0.1, 0.207, 0.04, 0.028, ink)
    handwrite(c, [('1959 - 60', 0.0, 1.0)], 0.65, 0.207, 0.04, 0.028, ink)
    handwrite(c, [('Miss Dolan', 0.16, 1.0)], 0.1, 0.242, 0.04, 0.028, ink)
    subj = ['Reading', 'Arithmetic', 'Spelling', 'Language', 'Penmanship', 'Social Studies', 'Music', 'Conduct']
    grades = [['A', 'A', 'A', 'A'], ['B', 'B+', 'A-', 'A'], ['A', 'A', 'A', 'A'], ['A-', 'A', 'A', 'A'],
              ['B', 'B', 'B+', 'B+'], ['A', 'A-', 'A', 'A'], ['A', 'A', 'A', 'A'], ['S', 'S-', 'S', 'S']]
    gx0, gx1, gy0, rh = 0.1, 0.9, 0.29, 0.042
    cols = [0.1, 0.46, 0.57, 0.68, 0.79, 0.9]
    c.rect(gx0, gy0, gx1, gy0 + rh, (0.75, 0.7, 0.55), alpha=0.5)
    for i, hd in enumerate(['1st', '2nd', '3rd', '4th']):
        c.text(((cols[i + 1] + cols[i + 2]) / 2, gy0 + rh / 2), hd, 'type_b', 0.018, t)
    c.text((0.12, gy0 + rh / 2), 'SUBJECT', 'type_b', 0.018, t, anchor='lm')
    for k in range(len(subj) + 2):
        c.line([(gx0, gy0 + k * rh), (gx1, gy0 + k * rh)], 0.0015, t, alpha=0.7)
    for x in cols:
        c.line([(x, gy0), (x, gy0 + (len(subj) + 1) * rh)], 0.0015, t, alpha=0.7)
    for i, (s, gr) in enumerate(zip(subj, grades)):
        y = gy0 + (i + 1) * rh + rh / 2
        c.text((0.12, y), s, 'type', 0.019, t, anchor='lm')
        for j, g in enumerate(gr):
            handwrite(c, [(g, (cols[j + 1] + cols[j + 2]) / 2 - 0.02 - gx0, 1.0)], gx0, y + 0.012, rh, 0.026, ink,
                      jitter=0.05)
    cy = gy0 + (len(subj) + 1) * rh + 0.05
    c.text((0.1, cy), "Teacher's Remarks", 'type_b', 0.019, t, anchor='lm')
    handwrite(c, ['Margaret is a joy to have in class and a', 'wonderful reader. If only she would stop',
                  'chatting with Linda during arithmetic!'], 0.1, cy + 0.06, 0.045, 0.03, ink, jitter=0.15)
    c.text((0.1, cy + 0.22), "Parent's Signature", 'type', 0.019, t, anchor='lm')
    c.line([(0.37, cy + 0.227), (0.9, cy + 0.227)], 0.0012, t, alpha=0.6)
    handwrite(c, [('Mrs. Walter Hale', 0.3, 1.0)], 0.1, cy + 0.222, 0.04, 0.03, (0.1, 0.1, 0.12))
    c.ellipse(0.85, 0.9, 0.2, 0.1, (0.8, 0.7, 0.5), blur=0.05, alpha=0.25, mode='mul')
    lay(cv, o, 0.5, 0.5, angle=-2, lift=0.008, shadow_alpha=0.45)
    light_field(cv, 0.4, 0.35, 1.2, 0.6, 1.2)


def sc_vmail(cv):
    wood_surface(cv, (0.4, 0.27, 0.17), (0.25, 0.15, 0.09), scale=0.7)
    # the brown window envelope beneath
    W, H = int(cv.W * 0.8), int(cv.W * 0.8 * 0.5)
    e = Obj(W, H, 51)
    e.shape(lambda d, w, h: d.rectangle([0, 0, w - 1, h - 1], fill=255))
    ec = e.cv
    ec.a[:] = _paper(H, W, ec.rng, (0.72, 0.6, 0.42), 0.06)
    ec.rect(0.12, 0.35, 0.62, 0.75, (0.85, 0.82, 0.75), alpha=0.5)
    ec.text((0.12, 0.15), 'WAR & NAVY DEPARTMENTS', 'sans_b', 0.06, (0.3, 0.22, 0.15), anchor='lm')
    ec.text((0.12, 0.25), 'V-MAIL SERVICE', 'sans_b', 0.06, (0.3, 0.22, 0.15), anchor='lm')
    ec.text((0.9, 0.2), 'OFFICIAL BUSINESS', 'sans', 0.045, (0.3, 0.22, 0.15), anchor='rm')
    lay(cv, e, 0.42, 0.8, angle=-8, lift=0.006, shadow_alpha=0.35)
    # the V-mail sheet: a small photographic print of the letter
    W, H = int(cv.W * 0.62), int(cv.W * 0.62 * 1.25)
    o = Obj(W, H, 53)
    o.shape(lambda d, w, h: d.rectangle([0, 0, w - 1, h - 1], fill=255))
    c = o.cv
    c.a[:] = _paper(H, W, c.rng, (0.9, 0.9, 0.88), 0.03)
    t = (0.15, 0.15, 0.17)
    c.rect(0.04, 0.03, 0.96, 0.19, t, alpha=0.0)
    m = c.mask(lambda d: d.rectangle([0.04 * W, 0.03 * H, 0.96 * W, 0.2 * H], outline=255, width=2))
    c.apply(m, t, 0.8)
    c.text((0.5, 0.05), 'V — — —  M A I L', 'sans_b', 0.026, t)
    c.text((0.08, 0.09), 'TO:', 'sans_b', 0.016, t, anchor='lm')
    c.text((0.55, 0.09), 'FROM:', 'sans_b', 0.016, t, anchor='lm')
    ink = (0.1, 0.1, 0.12)
    handwrite(c, ['Miss June Novak', '412 Cass Street', 'Joliet, Illinois'], 0.08, 0.125, 0.025, 0.02, ink)
    handwrite(c, ['Pvt. Walter Hale', 'Co. B, 134th Inf.', 'APO 35, c/o PM NY'], 0.55, 0.125, 0.025, 0.02, ink)
    c.rect(0.75, 0.21, 0.95, 0.27, t, alpha=0.0)
    m = c.mask(lambda d: d.ellipse([0.74 * W, 0.205 * H, 0.94 * W, 0.275 * H], outline=255, width=2))
    c.apply(m, (0.2, 0.2, 0.3), 0.5)
    c.text((0.84, 0.24), 'PASSED', 'sans_b', 0.014, (0.2, 0.2, 0.3), alpha=0.5)
    body = ['Oct. 14, 1944', 'Dear June,',
            'Your letter with the photograph came',
            'yesterday and I have it in my pocket now.',
            'The fellows all want to know who the pretty',
            'girl is and I tell them to mind their',
            'own business. It has rained for a week.',
            'I would trade my boots for one of your',
            "mother's pies. Tell Frank to behave and",
            "tell your mother I'm wearing the socks.",
            'Write soon. Keep the porch light on.',
            '', 'Yours, Walter']
    handwrite(c, body, 0.08, 0.32, 0.05, 0.033, ink, jitter=0.12)
    c.a = gauss(c.a, 0.9)  # photographically reduced: a touch soft
    lay(cv, o, 0.55, 0.45, angle=5, lift=0.008, shadow_alpha=0.45)
    light_field(cv, 0.5, 0.35, 1.2, 0.6, 1.2)


# ================================================================ the album
CHAPTERS = [
    dict(id='beginnings', title='Where it all began', cover='walter-uniform-1943',
         blurb='Before they were Grandma and Grandpa, they were two kids from Joliet, a farm, a front porch, '
               'and a war that kept them writing letters.'),
    dict(id='walter-june', title='Walter & June', cover='wedding-1948',
         blurb='A wedding on a windy June day, a honeymoon among the canyons, and a little house that would '
               'hold sixty years of life.'),
    dict(id='growing', title='A growing family', cover='county-fair-horse-1957',
         blurb='Margaret, Robert and Eleanor arrive, and the house fills up with birthday candles, Christmas '
               'mornings and muddy shoes.'),
    dict(id='summers', title='Summers & road trips', cover='grand-canyon-1966',
         blurb='Every summer the station wagon got packed to the roof and pointed somewhere new, or back to '
               'the lake, which was even better.'),
    dict(id='keepsakes', title='Keepsakes', cover='service-plaque-1972',
         blurb='The things they tucked away in the cedar chest, photographed so everyone can see them up close.'),
    dict(id='later', title='The later years', cover='anniversary-50th-1998',
         blurb='Anniversaries, grandkids, and the long, happy porch afternoons of a life well shared.'),
]


def P(id, chapter, title, caption, year, place, scene, orient, frame, era, approx=False, kind='photo',
      download=None, **kw):
    return dict(id=id, chapter=chapter, title=title, caption=caption, year=year, approx=approx, place=place,
                kind=kind, scene=scene, orient=orient, frame=frame, era=era, downloadName=download, **kw)


OBJ = dict(frame='object', era='object', rs=1.0)

PHOTOS = [
    # ---- where it all began
    P('june-baby-1925', 'beginnings', 'June, six months old',
      "June in her christening gown at Kessler Studio. Grandma Rose said she wouldn't sit still until the "
      "photographer whistled 'Bye Bye Blackbird.'",
      1925, 'Joliet, Illinois', sc_june_baby, 'P', 'cabinet', 'sepia', studio=('Kessler Studio', 'JOLIET, ILL.'),
      download='June Hale - six months old - 1925.jpg'),
    P('walter-frank-fence-1930', 'beginnings', 'Walter and Frank on the fence',
      'Walter (left) and his little brother Frank, the future Uncle Frank, on the back fence with Skip the dog. '
      'Frank always swore he was the taller one.',
      1930, 'Hale farm, Manhattan, Illinois', sc_boys_fence, 'L', 'deckle', 'sepia', approx=True,
      download='Walter and Frank on the fence - about 1930.jpg'),
    P('rose-porch-1932', 'beginnings', 'Grandma Rose on the porch',
      'Grandma Rose in her rocker on the Cass Street porch, apron on as always. That geranium outlived two '
      'rocking chairs and one very determined cat.',
      1932, 'Joliet, Illinois', sc_rose_porch, 'L', 'deckle', 'sepia', approx=True,
      download='Grandma Rose on the porch - about 1932.jpg'),
    P('hale-farm-1936', 'beginnings', 'The Hale farm',
      'The farm outside Manhattan where Walter and Uncle Frank grew up: the red barn, the silo, and the windmill '
      'that squeaked all night long.',
      1936, 'Manhattan, Illinois', sc_hale_farm, 'L', 'deckle', 'silver', approx=True,
      download='The Hale farm - about 1936.jpg'),
    P('walter-uniform-1943', 'beginnings', 'Walter in uniform',
      "Walter's Army portrait, taken the week before he shipped out. June kept it on her dresser through the "
      'whole war, and for most of the years after.',
      1943, 'Joliet, Illinois', sc_walter_uniform, 'P', 'deckle', 'silver',
      download='Walter Hale - Army portrait - 1943.jpg'),
    P('vmail-1944', 'beginnings', 'V-mail from Walter',
      "A V-mail letter Walter sent June from France. He mentions the rain, her mother's pies, and asks her to "
      'keep the porch light on.',
      1944, 'France', sc_vmail, 'P', kind='letter', download='V-mail from Walter to June - 1944.jpg', **OBJ),
    # ---- Walter & June
    P('wedding-1948', 'walter-june', "Walter & June's wedding",
      "Walter and June on the steps of St. Mary's. Her veil caught the wind just as the shutter clicked, and "
      'she always said that was the best part of the wedding.',
      1948, "St. Mary's, Joliet, Illinois", sc_wedding, 'P', 'border', 'silver',
      download='Walter and June - wedding day - 1948.jpg'),
    P('starved-rock-1948', 'walter-june', 'Honeymoon at Starved Rock',
      'Three days at Starved Rock for the honeymoon. Walter climbed out on the ledge for this one, and June '
      'never quite forgave him.',
      1948, 'Starved Rock State Park, Illinois', sc_starved_rock, 'L', 'deckle', 'silver',
      download='Honeymoon at Starved Rock - 1948.jpg'),
    P('dancing-1950', 'walter-june', 'Dancing at the VFW',
      "Walter and June at the VFW New Year's dance. He'd been taking lessons in secret, and by then he only "
      'stepped on her feet once a night.',
      1950, 'Joliet, Illinois', sc_dancing, 'L', 'border', 'bw50',
      download='Walter and June dancing - 1950.jpg'),
    P('picnic-1951', 'walter-june', 'Sunday picnic',
      'A Sunday picnic by the water: the red checked blanket, a thermos of lemonade, and a basket June packed as '
      'if she were feeding the whole parish.',
      1951, 'Channahon, Illinois', sc_picnic, 'L', 'scallop', 'bw50', approx=True,
      download='Walter and June - Sunday picnic - about 1951.jpg'),
    P('first-house-1952', 'walter-june', 'The first house',
      'The day Walter and June got the keys to the little house on Hickory Street. Walter planted the maple that '
      'morning; Margaret, age two, supervised.',
      1952, 'Hickory Street, Joliet, Illinois', sc_first_house, 'S', 'scallop', 'bw50',
      download='The house on Hickory Street - 1952.jpg'),
    # ---- a growing family
    P('margaret-baby-1950', 'growing', 'June and baby Margaret',
      'June with brand-new Margaret by the front window, two weeks old and already running the house.',
      1950, 'Joliet, Illinois', sc_margaret_baby, 'P', 'border', 'bw50',
      download='June and baby Margaret - 1950.jpg'),
    P('first-car-1955', 'growing', 'The first car',
      "Walter's pride and joy, a two-tone Chevrolet bought used in 1955. Margaret and Robert were allowed to "
      'look at the car, not touch it.',
      1955, 'Hickory Street, Joliet, Illinois', sc_first_car, 'L', 'scallop', 'bw50',
      download='Walter and the first car - 1955.jpg'),
    P('robert-birthday-1956', 'growing', 'Robert turns three',
      "Robert's third birthday party: five kids, five paper hats, three candles, and Pepper the dog waiting "
      'patiently under the table for crumbs.',
      1956, 'Joliet, Illinois', sc_birthday, 'L', 'border', 'bw50',
      download='Robert turns three - 1956.jpg'),
    P('county-fair-horse-1957', 'growing', 'Dad on a horse at the county fair',
      "Walter on a borrowed horse at the Will County Fair. He told the kids he'd been a cowboy before the war; "
      'the horse knew better.',
      1957, 'Will County Fair, Peotone, Illinois', sc_county_fair, 'L', 'border', 'bw50',
      download='Walter on a horse at the Will County Fair - 1957.jpg'),
    P('backyard-sprinkler-1959', 'growing', 'Sprinkler days',
      'August in the backyard: Robert and Margaret racing through the sprinkler, Eleanor deciding whether to '
      'risk it, and Pepper the dog barking at all of them.',
      1959, 'Hickory Street, Joliet, Illinois', sc_backyard, 'S', 'kodak', 'kodacolor', stamp='AUG  59',
      wear=0.7, download='Sprinkler days in the backyard - 1959.jpg'),
    P('christmas-morning-1961', 'growing', 'Christmas morning',
      'Christmas morning, 1961. The kids were up at five; Walter, in his good red robe, was not. That long box '
      'under the tree is the Lionel train.',
      1961, 'Hickory Street, Joliet, Illinois', sc_christmas, 'S', 'kodak', 'kodacolor', stamp='DEC  61',
      wear=0.7, download='Christmas morning - 1961.jpg'),
    P('easter-steps-1963', 'growing', 'Easter on the front steps',
      'Easter Sunday: Margaret in her new spring coat, Robert in a clip-on tie, and Eleanor holding the basket '
      "she wouldn't put down all day.",
      1963, 'Hickory Street, Joliet, Illinois', sc_easter, 'P', 'kodak', 'kodacolor', stamp='APR  63', wear=0.6,
      download='Easter on the front steps - 1963.jpg'),
    # ---- summers & road trips
    P('route66-motel-1965', 'summers', 'The Desert Rose Motel',
      'First night out on Route 66, somewhere in New Mexico. The kids voted for the motel with the pinkest neon '
      'sign, and nobody regretted it.',
      1965, 'Route 66, New Mexico', sc_route66_motel, 'P', 'kodak', 'kodachrome', stamp='JUN  65', wear=0.5,
      download='The Desert Rose Motel - Route 66 - 1965.jpg'),
    P('grand-canyon-1966', 'summers', 'The Grand Canyon',
      'Walter, June, Margaret, Robert and Eleanor at the rim of the Grand Canyon. June made everyone stand well '
      'back from the railing, and then took this picture.',
      1966, 'Grand Canyon, Arizona', sc_grand_canyon, 'L', 'kodak', 'kodachrome', stamp='JUL  66', wear=0.5,
      download='The Grand Canyon - 1966.jpg'),
    P('station-wagon-1967', 'summers', 'The station wagon',
      'The Country Squire wagon loaded to the roof, somewhere on Route 66. Walter is studying the map he never '
      'admitted he needed; Robert is "helping."',
      1967, 'Route 66, Arizona', sc_station_wagon, 'L', 'kodak', 'kodachrome', stamp='JUL  67', wear=0.5,
      download='The station wagon on Route 66 - 1967.jpg'),
    P('lake-cabin-1968', 'summers', 'Evening at the lake cabin',
      'Evening at the cabin on Long Lake: June at the end of the dock, the rowboat tied up for the night, and '
      'supper keeping warm inside.',
      1968, 'Long Lake, Wisconsin', sc_lake_cabin, 'S', 'kodak', 'faded70', stamp='AUG  68', wear=0.6,
      download='Evening at the lake cabin - 1968.jpg'),
    P('fishing-uncle-frank-1969', 'summers', 'Fishing with Uncle Frank',
      'Uncle Frank and Robert out in the boat at dawn. Frank claimed a four-pound bass that morning; the photo, '
      'sadly, does not include the fish.',
      1969, 'Long Lake, Wisconsin', sc_fishing, 'L', 'kodak', 'faded70', stamp='AUG  69', wear=0.6,
      download='Fishing with Uncle Frank - 1969.jpg'),
    P('dunes-beach-1971', 'summers', 'A day at the Dunes',
      'A hot July Saturday at the Indiana Dunes. June claimed the shade under the umbrella while Eleanor ran '
      'straight for Lake Michigan.',
      1971, 'Indiana Dunes, Indiana', sc_dunes_beach, 'S', 'kodak', 'faded70', stamp='JUL  71', wear=0.6,
      download='A day at the Indiana Dunes - 1971.jpg'),
    P('campfire-1973', 'summers', 'Campfire at the cabin',
      'Last night of summer at the lake cabin: marshmallows, ghost stories from Uncle Frank, and everyone '
      'smelling like woodsmoke for a week.',
      1973, 'Long Lake, Wisconsin', sc_campfire, 'L', 'kodak', 'faded70', stamp='AUG  73', wear=0.6,
      download='Campfire at the cabin - 1973.jpg'),
    # ---- keepsakes
    P('love-letter-1947', 'keepsakes', 'A letter to June',
      "Walter's letter to June from March 1947, the spring before the wedding. Found in her jewelry box, folded "
      'and refolded until the creases went soft.',
      1947, 'Joliet, Illinois', sc_love_letter, 'P', kind='letter', download='Letter from Walter to June - 1947.jpg',
      **OBJ),
    P('victory-medal', 'keepsakes', "Walter's service medal",
      "Walter's World War II Victory Medal, kept in its blue box in the top dresser drawer. He never talked "
      'about it much, but he never moved it either.',
      1946, '', sc_medal, 'P5', kind='keepsake', approx=True, download='Walter Hale - Victory Medal.jpg', **OBJ),
    P('apple-pie-recipe', 'keepsakes', "June's apple pie recipe",
      "June's apple pie in her own hand, copied from Grandma Rose. The butter stain is original. Jonathan apples "
      'only, no exceptions.',
      None, '', sc_recipe, 'L', kind='keepsake', download="June's apple pie recipe card.jpg", **OBJ),
    P('report-card-1960', 'keepsakes', "Margaret's report card",
      "Margaret's fourth-grade report card: straight A's in reading, and a note from Miss Dolan about talking in "
      'class that surprised nobody in the family.',
      1960, 'Joliet, Illinois', sc_report_card, 'P', kind='keepsake',
      download="Margaret Hale - 4th grade report card - 1960.jpg", **OBJ),
    P('service-plaque-1972', 'keepsakes', "Walter's 25-year plaque",
      'The walnut plaque Joliet Steel Works gave Walter for twenty-five years of service. It hung by the back '
      'door, where he saw it every morning on his way out.',
      1972, 'Joliet, Illinois', sc_plaque, 'L', kind='keepsake',
      download='Walter Hale - 25 Years of Service plaque - 1972.jpg', **OBJ),
    # ---- the later years
    P('anniversary-40th-1988', 'later', '40th anniversary party',
      'Walter and June cutting the cake at their 40th anniversary party at the VFW hall. Robert gave a toast '
      'that made everyone cry, including Robert.',
      1988, 'Joliet, Illinois', sc_anniversary_40, 'L6', 'glossy', 'glossy80', stamp="'88 6 18",
      download='40th anniversary party - 1988.jpg'),
    P('peggy-danny-leaves-1991', 'later', 'Peggy and Danny in the leaves',
      'Grandpa Walter raked that pile three times before Peggy and Danny let it stay a pile. Every October in the '
      'Hickory Street backyard.',
      1991, 'Hickory Street, Joliet, Illinois', sc_leaves, 'L6', 'glossy', 'glossy80', stamp="'91 10 27",
      download='Peggy and Danny in the leaves - 1991.jpg'),
    P('tire-swing-1993', 'later', "Grandpa's tire swing",
      'Grandpa Walter giving Peggy a push on the tire swing he hung from the old maple, the same tree he planted '
      'the day he and June moved in.',
      1993, 'Hickory Street, Joliet, Illinois', sc_tire_swing, 'P6', 'glossy', 'glossy80', stamp="'93 7 4",
      download="Peggy on Grandpa's tire swing - 1993.jpg"),
    P('anniversary-50th-1998', 'later', '50th anniversary',
      'Fifty years. Walter and June at their golden anniversary dinner, with the balloons Danny insisted on and '
      'the corsage Walter picked out himself.',
      1998, 'Joliet, Illinois', sc_anniversary_50, 'P6', 'glossy', 'glossy80', stamp="'98 6 20",
      download='Walter and June - 50th anniversary - 1998.jpg'),
    P('june-garden-2004', 'later', 'June in her garden',
      'June among her hollyhocks and roses at eighty, politely refusing all offers of help with the watering can.',
      2004, 'Hickory Street, Joliet, Illinois', sc_june_garden, 'L', 'digital', 'digital00',
      download='June in her garden - 2004.jpg'),
    P('last-christmas-2010', 'later', 'Our last Christmas together',
      'Christmas 2010, the last one with Grandma June. Everyone squeezed onto the couch, and Grandpa Walter fell '
      'asleep before the pie came out.',
      2010, 'Hickory Street, Joliet, Illinois', sc_last_christmas, 'L', 'digital', 'digital10',
      download='Our last Christmas together - 2010.jpg'),
    P('walter-porch-2016', 'later', 'Walter at 95',
      'Walter on the Hickory Street porch at ninety-five, cane within reach, waving at every car that went by '
      'and most of the dogs.',
      2016, 'Hickory Street, Joliet, Illinois', sc_walter_porch, 'P', 'digital', 'digital10',
      download='Walter at 95 on the porch - 2016.jpg'),
]


# ================================================================ output
def save_jpeg(im, path, quality):
    im.save(path, 'JPEG', quality=quality, progressive=True, optimize=True, subsampling='4:2:0')


def thumb_of(im):
    w, h = im.size
    s = THUMB_EDGE / max(w, h)
    return im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)


def write_manifest():
    photos = []
    for p in PHOTOS:
        path = os.path.join(OUT, p['id'] + '.jpg')
        with Image.open(path) as im:
            w, h = im.size
        photos.append({
            'id': p['id'], 'chapter': p['chapter'], 'title': p['title'], 'caption': p['caption'],
            'year': p['year'], 'approx': bool(p['approx']), 'place': p['place'], 'kind': p['kind'],
            'src': '../photos/sample/%s.jpg' % p['id'],
            'thumb': '../photos/sample/thumbs/%s.jpg' % p['id'],
            'download': '../photos/sample/%s.jpg' % p['id'],
            'downloadName': p['downloadName'] or (p['title'] + '.jpg'),
            'w': w, 'h': h,
        })
    data = {'chapters': CHAPTERS, 'photos': photos}
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def contact_sheet():
    cell, pad, label = 300, 14, 40
    cols = 6
    rows = math.ceil(len(PHOTOS) / cols)
    sheet = Image.new('RGB', (cols * (cell + pad) + pad, rows * (cell + pad + label) + pad), (40, 38, 36))
    d = ImageDraw.Draw(sheet)
    f = font('sans', 13)
    for i, p in enumerate(PHOTOS):
        with Image.open(os.path.join(THUMBS, p['id'] + '.jpg')) as im:
            im = im.convert('RGB')
            im.thumbnail((cell, cell), Image.LANCZOS)
            x = pad + (i % cols) * (cell + pad)
            y = pad + (i // cols) * (cell + pad + label)
            sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
            d.text((x + cell / 2, y + cell + 12), p['id'], font=f, fill=(225, 220, 210), anchor='mm')
            d.text((x + cell / 2, y + cell + 28), p['chapter'], font=f, fill=(150, 145, 135), anchor='mm')
    sheet.save(SHEET, quality=85)


def main(argv):
    os.makedirs(THUMBS, exist_ok=True)
    want = set(argv)
    ids = {p['id'] for p in PHOTOS}
    unknown = want - ids - {'--sheet'}
    if unknown:
        sys.exit('unknown id(s): ' + ', '.join(sorted(unknown)))
    for p in PHOTOS:
        if want - {'--sheet'} and p['id'] not in want:
            continue
        im = render(p)
        save_jpeg(im, os.path.join(OUT, p['id'] + '.jpg'), 80)
        save_jpeg(thumb_of(im), os.path.join(THUMBS, p['id'] + '.jpg'), 75)
        print('%-28s %4dx%-4d %s' % (p['id'], im.width, im.height, p['era']), flush=True)
    write_manifest()
    contact_sheet()
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print('%d photos, %.2f MB in photos/sample/' % (len(PHOTOS), total / 1e6))


if __name__ == '__main__':
    main(sys.argv[1:])
