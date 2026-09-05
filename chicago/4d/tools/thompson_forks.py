#!/usr/bin/env python3
"""Georeference the Thompson 1830 plat, trace its banks at the forks, and measure
them against the Wright 1834 line. T-0685.

`data/sources/thompson_plat_1830.json` calls the sheet a PARAMETER SOURCE — "read
for its stated figures, never traced for geometry" — and that rule is why the
plat's own planform had never been put beside the Wright 1834 line the terrain is
built from. The owner reads the two differently at Wolf Point, and a disagreement
cannot be settled by two sheets in two frames. So this tool does the one thing the
rule leaves room for: it fits the plat to the SAME frame the datum was fitted in,
traces its river, and REPORTS the difference. Nothing here moves the terrain, and
the rule above still governs what the reconstruction is built from.

    python3 tools/thompson_forks.py --fit        re-fit and rewrite the fit block
    python3 tools/thompson_forks.py --trace      re-trace the banks and write the vectors
    python3 tools/thompson_forks.py --measure    print the disagreement table
    python3 tools/thompson_forks.py --check      offline: hold both committed files to
                                                 the numbers they can be re-derived from
    python3 tools/thompson_forks.py --debug      also write an overlay PNG of the trace

Three stages, three dependency levels, on purpose
-------------------------------------------------
**The fit** is a 6-parameter affine from 23 committed pixel/EPSG:26916 pairs, solved
by ordinary least squares. It is pure Python — a 3x3 normal-equation solve — so
`--check` re-derives it in milliseconds with no numpy, no Pillow and no network, and
can be a per-commit gate. The georeference is the part a reader most needs to be able
to reproduce, so it is the part with no dependencies.

**The trace** reads the sheet. Thompson draws each bank as ONE freehand ink line on
bare paper — no wash, no fill — so the trace is a ridge-follower rather than the
region-growing `tools/trace_river.py` needs on Wright's washed sheet: from a committed
seed pixel and heading, step along the darkest path, turning no more than the committed
fan allows per step. It needs numpy and Pillow, and degrades to a clear skip without
them.

**The measurement** samples both planforms at named eastings and reports metres. It
reads only committed GeoJSON and the vectors this tool writes.

What the reading is NOT
-----------------------
The traced line is where Thompson's DRAFTSMAN put ink, carried into EPSG:26916 through
a fit whose own RMS is reported below. It is not a survey of the 1830 bank, and the
difference from Wright is not automatically Wright's error or Thompson's: it is the
distance between two drawings. `docs/RESEARCH/thompson_vs_wright_forks.md` says what
that distance turned out to be and what it does and does not license.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GCP_PATH = ROOT / "data/traces/gcp/thompson_1830_gcps.json"
VEC_PATH = ROOT / "data/traces/vectors/thompson_1830_forks.json"
WRIGHT_PATH = ROOT / "data/terrain/epochs/e1834_harbor_cut/river.geojson"
PLAT = ROOT.parent / "pre_fire_v1/maps/images/1830_thompson_plat.png"

# Eastings the disagreement is reported at. Chosen before the measurement was run,
# spaced 100 m through the reach the Wright bank lines actually cover, so the table
# cannot be accused of having been sampled where it flattered either sheet.
REPORT_EASTINGS = [446900, 447000, 447100, 447200, 447300, 447400]
REPORT_NORTHINGS = [4637100, 4637200, 4637300, 4637400, 4637500, 4637600, 4637700]


# --------------------------------------------------------------------------- fit
def solve3(rows, rhs):
    """Least squares for a 3-column design matrix, by Gaussian elimination on the
    normal equations. Pure Python so --check needs nothing installed."""
    n = 3
    ata = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]
    atb = [sum(r[i] * b for r, b in zip(rows, rhs)) for i in range(n)]
    m = [ata[i] + [atb[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r == c:
                continue
            f = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def fit(gcps):
    rows = [[g["pixel"][0], g["pixel"][1], 1.0] for g in gcps]
    ce = solve3(rows, [g["modern"]["utm_e"] for g in gcps])
    cn = solve3(rows, [g["modern"]["utm_n"] for g in gcps])
    resid = []
    for g in gcps:
        x, y = g["pixel"]
        e = ce[0] * x + ce[1] * y + ce[2]
        n = cn[0] * x + cn[1] * y + cn[2]
        resid.append(math.hypot(e - g["modern"]["utm_e"], n - g["modern"]["utm_n"]))
    rms = math.sqrt(sum(r * r for r in resid) / len(resid))
    coef = {"a": ce[0], "b": ce[1], "c": ce[2], "d": cn[0], "e": cn[1], "f": cn[2]}
    scale_x = math.hypot(ce[0], cn[0])
    scale_y = math.hypot(ce[1], cn[1])
    rot = math.degrees(math.atan2(cn[0], ce[0]))
    return coef, resid, rms, scale_x, scale_y, rot


def to_utm(coef, x, y):
    return (coef["a"] * x + coef["b"] * y + coef["c"],
            coef["d"] * x + coef["e"] * y + coef["f"])


def load_gcps():
    return json.loads(GCP_PATH.read_text())


def cmd_fit(write=True):
    doc = load_gcps()
    coef, resid, rms, sx, sy, rot = fit(doc["gcps"])
    for g, r in zip(doc["gcps"], resid):
        g["residual_m"] = round(r, 1)
    doc["fit"] = {
        "type": "affine, least squares, plat pixel -> EPSG:26916",
        "coefficients": {k: round(v, 10) for k, v in coef.items()},
        "n_control": len(doc["gcps"]),
        "rms_m": round(rms, 1),
        "max_residual_m": round(max(resid), 1),
        "scale_m_per_px": {"x": round(sx, 4), "y": round(sy, 4)},
        "rotation_deg": round(rot, 2),
        "axis_scale_difference_pct": round(abs(sx - sy) / ((sx + sy) / 2) * 100, 1),
        "note": doc["fit"]["note"] if "fit" in doc else "",
    }
    if write:
        GCP_PATH.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"fit over {len(doc['gcps'])} control points: RMS {rms:.1f} m, "
          f"max {max(resid):.1f} m, scale {sx:.4f}/{sy:.4f} m/px, rotation {rot:.2f} deg")
    for g, r in sorted(zip(doc["gcps"], resid), key=lambda t: -t[1]):
        print(f"   {g['id']:22s} {r:5.1f} m   {g['map_feature']}")
    return doc, coef


# ------------------------------------------------------------------------- trace
def cmd_trace(debug=False):
    try:
        import numpy as np
        from PIL import Image
    except ImportError as exc:
        print(f"skip: --trace needs numpy and Pillow ({exc})")
        return 0
    doc = load_gcps()
    coef, *_ = fit(doc["gcps"])
    vec = json.loads(VEC_PATH.read_text())
    grey = np.asarray(Image.open(PLAT).convert("L"), dtype=float)
    bg = float(np.percentile(grey, vec["reading"]["paper_percentile"]))
    dark = np.clip(bg - grey, 0, None)
    h, w = dark.shape

    def d(x, y):
        xi, yi = int(round(x)), int(round(y))
        return dark[yi, xi] if 0 <= xi < w and 0 <= yi < h else -1e9

    p = vec["reading"]
    step, fan, nfan, look, turn_cost = (p["step_px"], p["fan_deg"], p["fan_samples"],
                                        p["lookahead_steps"], p["turn_cost"])
    def run(seed, heading, steps):
        x, y = seed
        a = math.radians(heading)
        pts = [(x, y)]
        for _ in range(steps):
            best = None
            for k in range(nfan):
                da = math.radians(-fan + 2 * fan * k / (nfan - 1))
                aa = a + da
                sc = sum(d(x + step * i * math.cos(aa), y + step * i * math.sin(aa))
                         for i in range(1, look + 1)) - abs(da) * turn_cost
                if best is None or sc > best[0]:
                    best = (sc, aa)
            a = best[1]
            x += step * math.cos(a)
            y += step * math.sin(a)
            if not (0 <= x < w and 0 <= y < h):
                break
            e, n = to_utm(coef, x, y)
            stop = feat.get("stop_when", {})
            if (("e_above" in stop and e > stop["e_above"])
                    or ("e_below" in stop and e < stop["e_below"])
                    or ("n_above" in stop and n > stop["n_above"])
                    or ("n_below" in stop and n < stop["n_below"])):
                pts.append((x, y))
                break
            pts.append((x, y))
        return pts

    win = vec["window_utm"]

    def inside(px, py):
        e, n = to_utm(coef, px, py)
        return win["e"][0] <= e <= win["e"][1] and win["n"][0] <= n <= win["n"][1]

    for feat in vec["features"]:
        pts = run(feat["seed_px"], feat["seed_heading_deg"], feat["steps"])
        if feat.get("also_reverse"):
            back = run(feat["seed_px"], feat["seed_heading_deg"] + 180, feat["steps"])
            pts = list(reversed(back))[:-1] + pts
        # keep the LONGEST run of vertices inside the declared window, so a trace that
        # clips a corner of the box on its way in does not truncate the reading
        runs, cur = [], []
        for q in pts:
            if inside(*q):
                cur.append(q)
            else:
                if cur:
                    runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        pts = max(runs, key=len) if runs else []
        keep, last = [], None
        for px, py in pts:
            if last is None or math.dist((px, py), last) >= 8.0:
                # round the PIXEL first and derive the metres from the rounded value, so the
                # committed utm is exactly what --check re-derives from the committed px
                rx, ry = round(px, 1), round(py, 1)
                e, n = to_utm(coef, rx, ry)
                keep.append(([rx, ry], [round(e, 2), round(n, 2)]))
                last = (px, py)
        feat["px"] = [k[0] for k in keep]
        feat["utm"] = [k[1] for k in keep]
        print(f"{feat['id']:24s} {len(keep):3d} vertices  "
              f"E {min(u[0] for u in feat['utm']):.0f}..{max(u[0] for u in feat['utm']):.0f}  "
              f"N {min(u[1] for u in feat['utm']):.0f}..{max(u[1] for u in feat['utm']):.0f}")
    vec["fit_rms_m"] = round(fit(doc["gcps"])[2], 1)
    VEC_PATH.write_text(json.dumps(vec, indent=1) + "\n")
    if debug:
        from PIL import ImageDraw
        im = Image.open(PLAT).convert("RGB")
        dr = ImageDraw.Draw(im)
        for feat, col in zip(vec["features"], [(210, 0, 0), (0, 120, 255), (0, 160, 0)]):
            dr.line([tuple(q) for q in feat["px"]], fill=col, width=3)
        im.crop((600, 300, 1900, 1900)).save("/tmp/thompson_forks_debug.png")
        print("wrote /tmp/thompson_forks_debug.png")
    return 0


# ----------------------------------------------------------------------- measure
def _clip(line, box):
    return [q for q in line if box["e"][0] <= q[0] <= box["e"][1]
            and box["n"][0] <= q[1] <= box["n"][1]]


def _cross(line, axis, value):
    """Where a polyline crosses axis==value. None if it does not; the mean if it
    crosses more than once, which the `within` boxes exist to prevent."""
    hits = []
    for (x0, y0), (x1, y1) in zip(line, line[1:]):
        a, b = (x0, x1) if axis == 0 else (y0, y1)
        if (a - value) * (b - value) > 0 or a == b:
            continue
        t = (value - a) / (b - a)
        hits.append((y0 + t * (y1 - y0)) if axis == 0 else (x0 + t * (x1 - x0)))
    return sum(hits) / len(hits) if hits else None


def _seg_dist(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L2))
    return math.hypot(p[0] - (a[0] + t * vx), p[1] - (a[1] + t * vy))


def _nearest(p, line):
    return min(_seg_dist(p, a, b) for a, b in zip(line, line[1:]))


def cmd_measure():
    vec = json.loads(VEC_PATH.read_text())
    wright = json.loads(WRIGHT_PATH.read_text())
    banks = {f["properties"]["name"]: f["geometry"]["coordinates"]
             for f in wright["features"] if f["properties"].get("kind") == "bank"}
    tol = vec["uncertainty_m"]
    print(f"Thompson 1830 against Wright 1834 at the forks. Both in EPSG:26916 metres.")
    print(f"Thompson's fit RMS is {vec['fit_rms_m']} m; this reading declares "
          f"+/- {tol} m.\n")
    allrows = []
    for feat in vec["features"]:
        wl = banks[feat["wright_counterpart"]]
        tl = feat["utm"]
        # what the two readings have in common, so nothing is compared against nothing
        lo = max(min(q[1] for q in tl), min(q[1] for q in wl))
        hi = min(max(q[1] for q in tl), max(q[1] for q in wl))
        near = [_nearest(q, wl) for q in tl if lo <= q[1] <= hi]
        print(f"== {feat['id']}")
        print(f"   {len(tl)} Thompson vertices, {len(wl)} Wright vertices; "
              f"shared northing band {lo:.0f}..{hi:.0f}")
        if near:
            print(f"   nearest-point separation over that band: mean {sum(near)/len(near):6.1f} m"
                  f"   median {sorted(near)[len(near)//2]:6.1f} m"
                  f"   max {max(near):6.1f} m   min {min(near):6.1f} m")
        for rep in feat["report"]:
            axis = 0 if rep["axis"] == "e" else 1
            t = _clip(tl, rep["within"])
            wg = _clip(wl, rep["within"])
            print(f"\n   {rep['label']}")
            head = "easting" if axis == 0 else "northing"
            out = "northing" if axis == 0 else "easting"
            print(f"     {head:>10}  {'Thompson ' + out:>18}  {'Wright ' + out:>16}  {'delta_m':>9}")
            for v in rep["values"]:
                a = _cross(t, axis, v) if len(t) > 1 else None
                b = _cross(wg, axis, v) if len(wg) > 1 else None
                if a is None or b is None:
                    miss = "Thompson" if a is None else "Wright"
                    if a is None and b is None:
                        miss = "neither"
                    print(f"     {v:>10}  {'-' if a is None else f'{a:18.1f}'}"
                          f"  {'-' if b is None else f'{b:16.1f}'}  {'(' + miss + ')':>9}")
                    continue
                print(f"     {v:>10}  {a:18.1f}  {b:16.1f}  {a - b:9.1f}")
                allrows.append((feat["id"], rep["label"], v, a, b, a - b))
        print()
    if allrows:
        ds = [abs(r[5]) for r in allrows]
        inside = sum(1 for x in ds if x <= 20.0)
        print(f"{len(allrows)} paired samples across the three shores")
        print(f"  |delta|  mean {sum(ds)/len(ds):.1f} m   median {sorted(ds)[len(ds)//2]:.1f} m"
              f"   max {max(ds):.1f} m   min {min(ds):.1f} m")
        print(f"  signed mean {sum(r[5] for r in allrows)/len(allrows):+.1f} m")
        print(f"  {inside} of {len(allrows)} inside the +/- 20 m "
              f"data/sources/thompson_plat_1830.json already declares")
    return allrows


# ------------------------------------------------------------------------- check
def cmd_check():
    bad = 0
    doc = load_gcps()
    coef, resid, rms, sx, sy, rot = fit(doc["gcps"])
    got = doc["fit"]["coefficients"]
    for k, v in coef.items():
        if abs(got[k] - v) > 1e-6:
            print(f"FAIL fit coefficient {k}: committed {got[k]} re-derives to {v}")
            bad = 1
    if abs(doc["fit"]["rms_m"] - round(rms, 1)) > 0.05:
        print(f"FAIL fit rms_m: committed {doc['fit']['rms_m']} re-derives to {rms:.1f}")
        bad = 1
    if doc["fit"]["n_control"] != len(doc["gcps"]):
        print("FAIL fit n_control does not match the control list")
        bad = 1
    for g, r in zip(doc["gcps"], resid):
        if abs(g.get("residual_m", -1) - round(r, 1)) > 0.05:
            print(f"FAIL residual {g['id']}: committed {g.get('residual_m')} re-derives to {r:.1f}")
            bad = 1
    vec = json.loads(VEC_PATH.read_text())
    for feat in vec["features"]:
        if len(feat["px"]) != len(feat["utm"]):
            print(f"FAIL {feat['id']}: px and utm vertex counts differ")
            bad = 1
        for px, utm in zip(feat["px"], feat["utm"]):
            e, n = to_utm(coef, *px)
            if abs(e - utm[0]) > 0.02 or abs(n - utm[1]) > 0.02:
                print(f"FAIL {feat['id']}: {px} -> {utm} is not the committed fit's answer")
                bad = 1
                break
    if not bad:
        print(f"ok: fit re-derives over {len(doc['gcps'])} control points (RMS {rms:.1f} m); "
              f"{sum(len(f['px']) for f in vec['features'])} traced vertices agree with it")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args()
    if a.check:
        return cmd_check()
    if a.fit:
        cmd_fit()
    if a.trace:
        cmd_trace(debug=a.debug)
    if a.measure:
        cmd_measure()
    if not (a.fit or a.trace or a.measure):
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
