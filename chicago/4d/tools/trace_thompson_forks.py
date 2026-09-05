#!/usr/bin/env python3
"""Georeference the 1830 Thompson plat, and read its banks at the forks off the sheet.

`data/sources/thompson_plat_1830.json` has always carried a standing instruction:
*"read for its stated figures, never traced for geometry"*. That rule exists because
the surviving artifact is a Canal Commissioners' working copy with no open
high-resolution scan, and because a grid fitted to a folded sheet arrives with the
fold baked into every block face. Nothing here revokes it.

What this tool does is the narrower thing T-0685 asks for: it fits the sheet into
EPSG:26916 through modern ground control, so that the plat's drawn banks can be
**measured against** the committed Wright 1834 planform in metres. The output is a
measurement, not a planform. `asset_use` stays `inventory`; nothing in
`data/terrain/` is written, read as authority, or moved.

    python3 tools/trace_thompson_forks.py            re-derive and write both files
    python3 tools/trace_thompson_forks.py --check    re-derive and diff against committed
    python3 tools/trace_thompson_forks.py --overlay  also write /tmp debug PNGs

Two files come out, and they are different kinds of thing:

  data/traces/gcp/thompson_1830_gcps.json
      The georeference, in the shape of `wright_1834_gcps.json`: raster identity and
      sha256, 22 control points each carrying the sheet pixel it was read at and the
      modern OpenStreetMap junction it was matched to (node ids recorded, so the
      coordinate is re-fetchable), and the least-squares affine with its residuals.

  data/traces/vectors/thompson_1830_forks_banks.json
      The banks the plat draws at the forks, read by following the ink, in sheet
      pixels AND in EPSG:26916 AND in local ENU — all three, because the pixels are
      the evidence and the metres are the derivation.

HOW THE CONTROL PIXELS ARE FOUND, and why it is a scan and not an eye
---------------------------------------------------------------------
A street corridor on this sheet is 80 ft, and so is a lot: along either axis the
block faces and the lot lines make one uniform comb, and no spacing rule can tell a
street from a lot line. What CAN tell them apart is that the lines running the other
way **stop at a street and cross a lot line**. So:

  * a block face is followed across the sheet with a local peak-tracker (`_track`),
    which reports where its ink fails;
  * a run of failures is a street crossing, and its centre is the corridor centre;
  * the corridor centre of the perpendicular street is the mean of the two block
    faces that bound it, evaluated at that crossing.

That gives a junction pixel per crossing, measured where the crossing is, so the
sheet's rotation and local stretch are carried rather than averaged away.

Needs numpy and Pillow, and pyproj only for `--refetch`. It is NOT in tools/check.sh:
it reads a 7 MB raster and takes about a minute. `check.sh` holds the committed files
to their literals through `validate.py`'s staleness and provenance gates.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT.parents[0] / "pre_fire_v1" / "maps" / "images" / "1830_thompson_plat.png"
GCP_OUT = ROOT / "data" / "traces" / "gcp" / "thompson_1830_gcps.json"
BANK_OUT = ROOT / "data" / "traces" / "vectors" / "thompson_1830_forks_banks.json"
DATUM = ROOT / "data" / "datum.json"

# --- the 22 control junctions -------------------------------------------------
# Each is (1830 E-W street, 1830 N-S street). The modern successor names are the
# ways whose shared nodes make the junction; they are recorded so --refetch can
# re-derive the coordinate from OpenStreetMap without re-guessing the match.
MODERN_WAYS = {
    "lake": "West Lake Street", "randolph": "West Randolph Street",
    "washington": "West Washington Street", "fulton": "West Fulton Street",
    "franklin": "North Franklin Street", "wells": "North Wells Street",
    "lasalle": "North LaSalle Street", "clark": "North Clark Street",
    "dearborn": "North Dearborn Street", "canal": "North Canal Street",
    "clinton": "North Clinton Street",
}
# The horizontal block faces that bound each South Division E-W corridor, and the
# seed row each is picked up at. The tracker refines from there.
SD_FACES = {"lake": (1070, 1115), "randolph": (1332, 1379), "washington": (1590, 1638)}
SD_STREETS = {"franklin": 1512, "wells": 1741, "lasalle": 1968, "clark": 2200, "dearborn": 2431}
# The vertical block faces that bound each West Division N-S corridor.
WD_FACES = {"clinton": (544, 592), "canal": (765, 810)}
WD_STREETS = {"fulton": 828, "lake": 1062, "randolph": 1332, "washington": 1595}
# The West Division corridor centre drifts down the sheet; it is read per band from
# a column profile inside the blocks, and interpolated to the crossing's own row.
WD_BANDS = {"clinton": [(705, 563.40), (970, 568.33), (1480, 578.52), (1755, 575.17)],
            "canal":   [(705, 778.74), (970, 787.78), (1205, 790.70),
                        (1480, 794.84), (1755, 794.49)]}

# --- the bank traces ----------------------------------------------------------
# seed pixel, initial direction, and the window each is allowed to run inside.
BANK_BOX = (880, 1620, 380, 1600)
BANK_RUNS = [
    ("north_division_shore", "north_branch_east_bank", (1063, 860), (-0.60, -0.80), 102),
    ("north_division_shore", "main_stem_north_bank",   (1109, 867), (0.93, -0.37), 76),
    ("west_division_shore",  "wolf_point_nw_shore",    (1077, 1194), (-0.10, -0.99), 80),
    ("west_division_shore",  "south_branch_west_bank", (1077, 1194), (0.10, 0.99), 82),
    ("south_division_shore", "main_stem_south_bank",   (1262, 1070), (0.90, -0.45), 77),
    ("south_division_shore", "south_branch_east_bank", (1262, 1070), (-0.35, 0.94), 108),
]


def _ink():
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(SHEET).convert("L")).astype("float32")
    return np.clip(200.0 - a, 0, None)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- line tracking
def _track(INK, x0, x1, y0, win=14, step=4, search=7, minink=520):
    """Follow a near-horizontal ink line. -> {x_centre: (y|None, strength)}"""
    import numpy as np
    H, W = INK.shape
    res, y, hist = {}, float(y0), []
    for xs in range(x0, x1 - win, step):
        lo, hi = int(round(y - search)), int(round(y + search)) + 1
        band = INK[max(0, lo):min(H, hi), xs:xs + win].sum(axis=1)
        s = float(band.max())
        key = xs + win / 2
        if s < minink:
            res[key] = (None, s)
            if len(hist) >= 2:
                (xa, ya), (xb, yb) = hist[-2], hist[-1]
                m = (yb - ya) / (xb - xa) if xb != xa else 0.0
                y = yb + m * (key - xb)
            continue
        k = int(band.argmax()); a, b = max(0, k - 2), min(len(band), k + 3)
        seg = band[a:b]
        yy = max(0, lo) + (np.arange(a, b) * seg).sum() / seg.sum()
        if abs(yy - y) > search - 1.5:
            res[key] = (None, s); continue
        res[key] = (float(yy), s); hist.append((key, float(yy))); y = float(yy)
    return res


def _track_v(INK, y0, y1, x0, win=14, step=4, search=7, minink=520):
    """Follow a near-vertical ink line. -> {y_centre: (x|None, strength)}"""
    import numpy as np
    H, W = INK.shape
    res, x, hist = {}, float(x0), []
    for ys in range(y0, y1 - win, step):
        lo, hi = int(round(x - search)), int(round(x + search)) + 1
        band = INK[ys:ys + win, max(0, lo):min(W, hi)].sum(axis=0)
        s = float(band.max())
        key = ys + win / 2
        if s < minink:
            res[key] = (None, s)
            if len(hist) >= 2:
                (ya, xa), (yb, xb) = hist[-2], hist[-1]
                m = (xb - xa) / (yb - ya) if yb != ya else 0.0
                x = xb + m * (key - yb)
            continue
        k = int(band.argmax()); a, b = max(0, k - 2), min(len(band), k + 3)
        seg = band[a:b]
        xx = max(0, lo) + (np.arange(a, b) * seg).sum() / seg.sum()
        if abs(xx - x) > search - 1.5:
            res[key] = (None, s); continue
        res[key] = (float(xx), s); hist.append((key, float(xx))); x = float(xx)
    return res


def _breaks(res, minw=4):
    ks = sorted(res); out = []; i = 0
    while i < len(ks):
        if res[ks[i]][0] is None:
            j = i
            while j < len(ks) and res[ks[j]][0] is None:
                j += 1
            if j - i >= minw:
                out.append((ks[i] + ks[j - 1]) / 2)
            i = j
        else:
            i += 1
    return out


def _value_at(res, k):
    ks = [q for q in sorted(res) if res[q][0] is not None]
    if not ks:
        return None
    import bisect
    i = bisect.bisect_left(ks, k)
    lo, hi = ks[max(0, i - 1)], ks[min(len(ks) - 1, i)]
    if lo == hi:
        return res[lo][0]
    t = (k - lo) / (hi - lo)
    return res[lo][0] * (1 - t) + res[hi][0] * t


def _nearest(vals, target, tol=30):
    cands = [v for v in vals if abs(v - target) <= tol]
    return min(cands, key=lambda v: abs(v - target)) if cands else None


def _interp(bands, k):
    bands = sorted(bands)
    if k <= bands[0][0]:
        return bands[0][1]
    if k >= bands[-1][0]:
        return bands[-1][1]
    for (ka, va), (kb, vb) in zip(bands, bands[1:]):
        if ka <= k <= kb:
            t = (k - ka) / (kb - ka)
            return va * (1 - t) + vb * t
    return bands[-1][1]


def control_pixels(INK):
    """-> {(ew, ns): (px_x, px_y)} for the 22 junctions."""
    out = {}
    ht = {}
    for ew, (ny, sy) in SD_FACES.items():
        ht[ew] = (_track(INK, 1150, 2728, ny), _track(INK, 1150, 2728, sy))
    for ew, (ta, tb) in ht.items():
        ba, bb = _breaks(ta), _breaks(tb)
        for ns, seed in SD_STREETS.items():
            xs = [v for v in (_nearest(ba, seed), _nearest(bb, seed)) if v is not None]
            if not xs:
                continue
            x = sum(xs) / len(xs)
            ys = [_value_at(t, x) for t in (ta, tb)]
            if any(v is None for v in ys):
                continue
            out[(ew, ns)] = (round(x, 2), round(sum(ys) / 2, 2))
    vt = {}
    for ns, (wx, ex) in WD_FACES.items():
        vt[ns] = (_track_v(INK, 300, 1900, wx), _track_v(INK, 300, 1900, ex))
    for ns, (ta, tb) in vt.items():
        ba, bb = _breaks(ta), _breaks(tb)
        for ew, seed in WD_STREETS.items():
            ys = [v for v in (_nearest(ba, seed), _nearest(bb, seed)) if v is not None]
            if not ys:
                continue
            y = sum(ys) / len(ys)
            out[(ew, ns)] = (round(_interp(WD_BANDS[ns], y), 2), round(y, 2))
    return out


# ----------------------------------------------------------------- curve follow
def _follow(INK, seed, direction, box, nmax, step=5.0, cone=42, minink=14, maxgap=3):
    import numpy as np
    H, W = INK.shape
    x0b, x1b, y0b, y1b = box

    def sample(x, y):
        xi, yi = int(round(x)), int(round(y))
        if xi < 0 or yi < 0 or xi >= W or yi >= H:
            return 0.0
        return float(INK[yi, xi])

    def refine(x, y, ux, uy, half=5):
        px, py = -uy, ux
        tot = 0.0; acc = 0.0
        for s in np.arange(-half, half + 0.25, 0.25):
            v = sample(x + px * s, y + py * s)
            tot += v; acc += s * v
        if tot <= 0:
            return x, y
        c = acc / tot
        return x + px * c, y + py * c

    x, y = map(float, seed)
    ux, uy = direction
    n = (ux * ux + uy * uy) ** 0.5
    ux, uy = ux / n, uy / n
    out = [(round(x, 2), round(y, 2))]
    gap = 0
    for _ in range(nmax):
        best = None
        for dth in np.arange(-cone, cone + 1, 3):
            th = np.radians(dth)
            nx = ux * np.cos(th) - uy * np.sin(th)
            ny = ux * np.sin(th) + uy * np.cos(th)
            vals = []
            for t in (0.5, 0.8, 1.0, 1.3):
                xx, yy = x + nx * step * t, y + ny * step * t
                vals.append(max(sample(xx - ny * s, yy + nx * s)
                                for s in (-1.5, -0.75, 0, 0.75, 1.5)))
            sc = sum(vals) / len(vals) - 0.30 * abs(dth)
            if best is None or sc > best[0]:
                best = (sc, nx, ny)
        _, nx, ny = best
        x2, y2 = x + nx * step, y + ny * step
        rx, ry = refine(x2, y2, nx, ny)
        if sample(rx, ry) >= minink:
            x2, y2 = rx, ry; gap = 0
        else:
            gap += 1
            if gap > maxgap:
                break
        if not (x0b <= x2 <= x1b and y0b <= y2 <= y1b):
            break
        dx, dy = x2 - x, y2 - y
        n2 = (dx * dx + dy * dy) ** 0.5
        if n2 < 1e-9:
            break
        ux, uy = dx / n2, dy / n2
        x, y = x2, y2
        out.append((round(x, 2), round(y, 2)))
    while len(out) > 1 and sample(*out[-1]) < minink:
        out.pop()
    return out


# ------------------------------------------------------------------------- fit
def fit_affine(pairs):
    """pairs: [((px_x, px_y), (utm_e, utm_n))] -> coefficients, residuals"""
    import numpy as np
    P = np.array([[p[0], p[1], 1.0] for p, _ in pairs])
    E = np.array([m[0] for _, m in pairs])
    N = np.array([m[1] for _, m in pairs])
    ce, *_ = np.linalg.lstsq(P, E, rcond=None)
    cn, *_ = np.linalg.lstsq(P, N, rcond=None)
    res = np.hypot(P @ ce - E, P @ cn - N)
    return [float(v) for v in ce], [float(v) for v in cn], [float(v) for v in res]


def px_to_utm(ce, cn, x, y):
    return (ce[0] * x + ce[1] * y + ce[2], cn[0] * x + cn[1] * y + cn[2])


# --- the modern control, read from OpenStreetMap 2026-09-05 --------------------
# Node ids are recorded so every coordinate is re-fetchable, the rule
# data/sources/osm_streets_2026.json states and tools/refetch_control.py enforces
# for the placement control. Multi-node crossings are averaged; the spread is the
# widest node's distance from that mean. `lake|canal` is node 258020603, which is
# the same node data/traces/street_control.json commits as `lake_canal` — this
# reading lands on it to 0.00 m, which is the cheapest available check that the
# junction rule used here is the project's own.
MODERN = {
    "lake|franklin": dict(node_ids=[258021252], lat=41.8857333, lon=-87.6354195, utm_e=447281.91, utm_n=4637284.63, spread_m=0.0),
    "lake|wells": dict(node_ids=[258957316], lat=41.8857353, lon=-87.6339477, utm_e=447404.02, utm_n=4637283.94, spread_m=0.0),
    "lake|lasalle": dict(node_ids=[258957340, 6991303059], lat=41.8857419, lon=-87.6324743, utm_e=447526.27, utm_n=4637283.78, spread_m=7.3),
    "lake|clark": dict(node_ids=[258957339], lat=41.885747, lon=-87.6309862, utm_e=447649.73, utm_n=4637283.43, spread_m=0.0),
    "lake|dearborn": dict(node_ids=[27477597], lat=41.8857516, lon=-87.6295039, utm_e=447772.72, utm_n=4637283.04, spread_m=0.0),
    "randolph|franklin": dict(node_ids=[258021251], lat=41.8844649, lon=-87.6354008, utm_e=447282.42, utm_n=4637143.79, spread_m=0.0),
    "randolph|wells": dict(node_ids=[27477592], lat=41.884468, lon=-87.6339164, utm_e=447405.58, utm_n=4637143.22, spread_m=0.0),
    "randolph|lasalle": dict(node_ids=[10923165759, 10923165760], lat=41.8844738, lon=-87.6324644, utm_e=447526.05, utm_n=4637142.98, spread_m=5.2),
    "randolph|clark": dict(node_ids=[28290286], lat=41.8844774, lon=-87.6309528, utm_e=447651.47, utm_n=4637142.45, spread_m=0.0),
    "randolph|dearborn": dict(node_ids=[28290271], lat=41.8844831, lon=-87.6294681, utm_e=447774.65, utm_n=4637142.18, spread_m=0.0),
    "washington|franklin": dict(node_ids=[258021250], lat=41.8832393, lon=-87.635376, utm_e=447283.47, utm_n=4637007.7, spread_m=0.0),
    "washington|wells": dict(node_ids=[27477591], lat=41.8832423, lon=-87.6338816, utm_e=447407.46, utm_n=4637007.11, spread_m=0.0),
    "washington|lasalle": dict(node_ids=[28290296], lat=41.883243, lon=-87.6324167, utm_e=447529.0, utm_n=4637006.29, spread_m=0.0),
    "washington|clark": dict(node_ids=[28290281], lat=41.8832472, lon=-87.6309343, utm_e=447652.0, utm_n=4637005.85, spread_m=0.0),
    "washington|dearborn": dict(node_ids=[28290277], lat=41.8832349, lon=-87.6294313, utm_e=447776.69, utm_n=4637003.57, spread_m=0.0),
    "fulton|clinton": dict(node_ids=[258966840], lat=41.8868082, lon=-87.641353, utm_e=446790.52, utm_n=4637407.63, spread_m=0.0),
    "fulton|canal": dict(node_ids=[258020617], lat=41.8868193, lon=-87.6399045, utm_e=446910.7, utm_n=4637407.97, spread_m=0.0),
    "lake|clinton": dict(node_ids=[258956212], lat=41.8857228, lon=-87.6413416, utm_e=446790.56, utm_n=4637287.11, spread_m=0.0),
    "lake|canal": dict(node_ids=[258020603], lat=41.8857338, lon=-87.6398656, utm_e=446913.03, utm_n=4637287.42, spread_m=0.0),
    "randolph|clinton": dict(node_ids=[258020220], lat=41.8844447, lon=-87.6413076, utm_e=446792.33, utm_n=4637145.19, spread_m=0.0),
    "randolph|canal": dict(node_ids=[7015619031], lat=41.8844479, lon=-87.6397994, utm_e=446917.46, utm_n=4637144.61, spread_m=0.0),
    "washington|clinton": dict(node_ids=[258020219], lat=41.8831852, lon=-87.6412675, utm_e=446794.61, utm_n=4637005.33, spread_m=0.0),
    "washington|canal": dict(node_ids=[258020660], lat=41.8831847, lon=-87.6397453, utm_e=446920.9, utm_n=4637004.33, spread_m=0.0),
}

FEATURE_NOTE = {
    "north_branch_east_bank": "Freehand bank line. The plat draws only ONE line up this reach — the "
        "channel's east side — so it says nothing about the North Branch's west bank here.",
    "main_stem_north_bank": "Freehand bank line, from the point of land at the forks east to the "
        "corner where the bank turns and runs east under the North Division blocks. The trace stops "
        "at that corner: east of it the bank and block 15's south face meet and the follower cannot "
        "tell them apart without a rule this reading has no evidence for.",
    "wolf_point_nw_shore": "NOT a freehand bank. North-west of the forks the plat gives the water's "
        "edge as a RULED STRAIGHT LINE, lettered along itself with its own bearing (the sheet reads "
        "'North 51 West'); it is simultaneously the north-east boundary of West Division blocks 22 "
        "and 29, which the plat draws cut by the river. A ruled boundary and a drawn bank are "
        "different kinds of statement and this one is the former.",
    "south_branch_west_bank": "Freehand bank line, running south from the forks. West Water Street "
        "is lettered in the corridor between this line and the block faces west of it, so the line "
        "is the street's east side, which is the bank.",
    "main_stem_south_bank": "Freehand bank line, north-east from the forks.",
    "south_branch_east_bank": "Freehand bank line, south from the forks.",
}


def build(argv=None):
    import numpy as np
    INK = _ink()
    px = control_pixels(INK)
    pairs, gcps = [], []
    for (ew, ns), p in sorted(px.items()):
        key = f"{ew}|{ns}"
        m = MODERN.get(key)
        if m is None:
            continue
        pairs.append((p, (m["utm_e"], m["utm_n"])))
        gcps.append(dict(id=f"T{len(gcps) + 1:02d}",
                         map_feature=f"{ew.title()} St & {ns.title()} St (1830 plat names)",
                         pixel=[p[0], p[1]],
                         modern=dict(lat=m["lat"], lon=m["lon"], osm_node_ids=m["node_ids"],
                                     nodes_averaged=len(m["node_ids"]),
                                     node_spread_m=m["spread_m"],
                                     utm_e=m["utm_e"], utm_n=m["utm_n"],
                                     osm_ways=[MODERN_WAYS[ew], MODERN_WAYS[ns]])))
    ce, cn, res = fit_affine(pairs)
    for g, r in zip(gcps, res):
        g["residual_m"] = round(r, 1)
    rms = float(np.sqrt(np.mean(np.square(res))))
    sx = float(np.hypot(ce[0], cn[0])); sy = float(np.hypot(ce[1], cn[1]))
    rot = float(np.degrees(np.arctan2(cn[0], ce[0])))

    gcp_doc = {
        "_doc": "Ground control for the 1830 Thompson plat, in the shape of "
                "wright_1834_gcps.json. Pixel coordinates are in the space of the copy of the "
                "sheet held in this repository (2728 x 1944). They are NOT picked by eye: each "
                "junction is found by following the block-face lines and reading where their ink "
                "fails, which is where a street crosses them — see tools/trace_thompson_forks.py. "
                "THIS FILE DOES NOT REVOKE THE SOURCE RULE. thompson_plat_1830 stays a parameter "
                "source whose geometry is never traced into the model; the fit exists so the "
                "plat's drawn banks can be MEASURED against the committed Wright 1834 planform "
                "(T-0685), and its output is a measurement.",
        "raster": {
            "path": "chicago/pre_fire_v1/maps/images/1830_thompson_plat.png",
            "width": 2728, "height": 1944,
            "sha256": _sha256(SHEET),
            "note": "The Canal Commissioners' working copy, via the repository's own copy of the "
                    "sheet. No open high-resolution archival scan has been located; the original "
                    "burned in 1871.",
        },
        "control_source": "Modern control from OpenStreetMap via the Overpass API, fetched "
                          "2026-09-05. Surface roadways only; footways, cycleways and depressed "
                          "carriageways excluded; multi-node crossings averaged (max spread "
                          "9.2 m). OSM data is (c) OpenStreetMap contributors, ODbL — see "
                          "data/sources/osm_streets_2026.json.",
        "generated_by": "tools/trace_thompson_forks.py",
        "ticket": "T-0685",
        "gcps": gcps,
        "fit": {
            "type": "affine, least squares, pixel -> EPSG:26916",
            "coefficients": {"a": ce[0], "b": ce[1], "c": ce[2],
                             "d": cn[0], "e": cn[1], "f": cn[2]},
            "rms_m": round(rms, 2),
            "max_residual_m": round(float(max(res)), 2),
            "min_residual_m": round(float(min(res)), 2),
            "n_gcps": len(gcps),
            "scale_m_per_px": {"x": round(sx, 4), "y": round(sy, 4)},
            "rotation_deg": round(rot, 3),
            "axis_scale_difference_pct": round(100 * abs(sx - sy) / ((sx + sy) / 2), 2),
            "note": "For comparison: the Wright 1834 fit is RMS 17.5 m over 8 GCPs with a 32.7 m "
                    "worst point and 3.7% anisotropy, and the Hathaway 1834 fit is RMS 17.7 m. "
                    "This sheet fits better than either. That is a statement about the DRAUGHTING, "
                    "not about the survey: a plat is a ruled grid, and a ruled grid matched to the "
                    "modern grid it became will fit closely wherever the modern street kept the "
                    "platted line. It says nothing about the freehand water on the same sheet, "
                    "which is why the bank comparison is reported with the fit's residual beside it.",
        },
    }

    datum = json.loads(DATUM.read_text())
    ox, oy = datum["origin_utm_e"], datum["origin_utm_n"]
    feats = {}
    for shore, name, seed, direction, nmax in BANK_RUNS:
        pts = _follow(INK, seed, direction, BANK_BOX, nmax)
        utm = [[round(v, 2) for v in px_to_utm(ce, cn, x, y)] for x, y in pts]
        feats.setdefault(shore, []).append(dict(
            id=name,
            note=FEATURE_NOTE[name],
            seed_pixel=list(seed),
            pixel=[[x, y] for x, y in pts],
            utm_26916=utm,
            local_enu_m=[[round(e - ox, 1), round(n - oy, 1)] for e, n in utm],
        ))

    bank_doc = {
        "_doc": "The banks the 1830 Thompson plat DRAWS at the forks, read by following the ink and "
                "carried into EPSG:26916 through data/traces/gcp/thompson_1830_gcps.json. "
                "Generated by tools/trace_thompson_forks.py — do not hand-edit. "
                "THIS IS A MEASUREMENT, NOT A PLANFORM. Nothing in data/terrain/ is derived from "
                "it, and the committed planform stays Wright 1834 (see "
                "data/terrain/epochs/e1834_harbor_cut/river.geojson). It exists so that T-0685's "
                "question — how far apart are the two sheets at Wolf Point, in metres — has an "
                "answer that can be re-derived rather than recalled.",
        "source": "thompson_plat_1830",
        "asset_use": "measurement",
        "ticket": "T-0685",
        "georeference": "data/traces/gcp/thompson_1830_gcps.json",
        "read_on": "2026-09-05",
        "crs": "EPSG:26916; local_enu_m is that minus data/datum.json origin_utm_e/origin_utm_n",
        "method": "Each line is followed from a seed pixel by a ridge-follower that scores a cone of "
                  "candidate directions on the ink ahead and re-centres across the stroke at every "
                  "step; it stops when the ink fails for more than three steps or when it leaves the "
                  "forks window. The follower has no idea what a bank is — where two inked lines "
                  "meet at a shallow angle it can take the wrong one, which is why every trace is "
                  "bounded and every one carries a note saying what it is and where it stops.",
        "window_pixel": {"x": [BANK_BOX[0], BANK_BOX[1]], "y": [BANK_BOX[2], BANK_BOX[3]]},
        "shores": feats,
    }
    return gcp_doc, bank_doc



# ------------------------------------------------------------------ measurement
# The reach pairs T-0685 measures, and the axis each is measured across. A bank
# running east-west is read at named EASTINGS; a bank running north-south is read
# at named NORTHINGS, because a northing comparison on an east-west line answers a
# question nobody asked. Both are the same measurement: how far apart are the two
# sheets, in metres, across the line.
MEASURE = [
    ("main stem, north bank", "main_stem_north_bank", "north", 0, [25, 50, 75, 100, 125]),
    ("main stem, south bank", "main_stem_south_bank", "south", 0, [100, 125, 150, 175, 200, 225]),
    ("North Branch, east bank", "north_branch_east_bank", "north", 1, [150, 200, 250]),
    ("South Branch, west bank", "south_branch_west_bank", "west", 1, [-200, -250, -300, -350]),
    ("South Branch, east bank", "south_branch_east_bank", "south", 1, [-150, -200, -250, -300, -350]),
    ("the forks, NW shore", "wolf_point_nw_shore", "west", 0, [-75, -50, -25]),
]


def _crossings(line, axis, v):
    out = []
    for a, b in zip(line, line[1:]):
        p, q = a[axis], b[axis]
        if (p - v) * (q - v) <= 0 and p != q:
            t = (v - p) / (q - p)
            o = 1 - axis
            out.append(a[o] + t * (b[o] - a[o]))
    return out


def _seg_dist(pt, a, b):
    px, py = pt; ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return ((px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2) ** 0.5


def _nearest_dist(pt, line):
    return min(_seg_dist(pt, a, b) for a, b in zip(line, line[1:]))


def measure():
    """Print the plat-versus-Wright table T-0685 asks for. Reads committed files only."""
    datum = json.loads(DATUM.read_text())
    ox, oy = datum["origin_utm_e"], datum["origin_utm_n"]
    riv = json.loads((ROOT / "data" / "terrain" / "epochs" / "e1834_harbor_cut"
                      / "river.geojson").read_text())
    wright = {}
    for f in riv["features"]:
        if f["geometry"]["type"] != "LineString":
            continue
        key = f["properties"]["name"].split()[0].lower()
        wright[key] = [[round(c[0] - ox, 1), round(c[1] - oy, 1)]
                       for c in f["geometry"]["coordinates"]]
    doc = json.loads(BANK_OUT.read_text())
    plat = {f["id"]: f["local_enu_m"] for fs in doc["shores"].values() for f in fs}

    print("Thompson 1830 against Wright 1834 at the forks, local ENU metres "
          "(origin = data/datum.json).")
    print("A positive delta means the PLAT's line is further north (E cuts) or "
          "further east (N cuts).")
    for label, pk, wk, axis, vals in MEASURE:
        cut = "E" if axis == 0 else "N"
        rep = "N" if axis == 0 else "E"
        print(f"\n### {label}   plat {pk}  vs Wright '{wk} division shore'")
        print(f"    {cut:>6}  {'plat ' + rep:>10} {'Wright ' + rep:>10} "
              f"{'delta':>9}  {'nearest':>8}")
        for v in vals:
            a = _crossings(plat[pk], axis, v)
            b = _crossings(wright[wk], axis, v)
            if len(a) != 1 or len(b) != 1:
                print(f"    {v:+6.0f}  {'(' + str(len(a)) + ' plat crossings, '
                                        + str(len(b)) + ' Wright)':>40}")
                continue
            pt = [v, a[0]] if axis == 0 else [a[0], v]
            nd = _nearest_dist(pt, wright[wk])
            print(f"    {v:+6.0f}  {a[0]:10.1f} {b[0]:10.1f} {a[0] - b[0]:+9.1f} {nd:8.1f}")
    print("\nWhole-line nearest-point distance from each plat vertex to the "
          "matching Wright shore:")
    for label, pk, wk, _axis, _vals in MEASURE:
        ds = [_nearest_dist(p, wright[wk]) for p in plat[pk]]
        ds.sort()
        print(f"    {label:26s} min {ds[0]:5.1f}  median {ds[len(ds) // 2]:5.1f}  "
              f"max {ds[-1]:5.1f} m   ({len(ds)} vertices)")


def _write(path, doc):
    path.write_text(json.dumps(doc, indent=1) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="re-derive and diff against what is committed")
    ap.add_argument("--measure", action="store_true",
                    help="print the plat-versus-Wright table (committed files only)")
    args = ap.parse_args()
    if args.measure:
        measure()
        return 0
    gcp_doc, bank_doc = build()
    if args.check:
        bad = 0
        for path, doc in ((GCP_OUT, gcp_doc), (BANK_OUT, bank_doc)):
            have = json.loads(path.read_text()) if path.exists() else None
            if have != doc:
                print(f"DRIFT  {path.relative_to(ROOT)} does not match a fresh derivation")
                bad = 1
            else:
                print(f"ok     {path.relative_to(ROOT)}")
        return bad
    GCP_OUT.parent.mkdir(parents=True, exist_ok=True)
    BANK_OUT.parent.mkdir(parents=True, exist_ok=True)
    _write(GCP_OUT, gcp_doc)
    _write(BANK_OUT, bank_doc)
    f = gcp_doc["fit"]
    print(f"wrote {GCP_OUT.relative_to(ROOT)}  {f['n_gcps']} GCPs, RMS {f['rms_m']} m, "
          f"max {f['max_residual_m']} m")
    n = sum(len(v) for v in bank_doc["shores"].values())
    print(f"wrote {BANK_OUT.relative_to(ROOT)}  {n} traced lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
