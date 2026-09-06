#!/usr/bin/env python3
"""Register the National Archives / Historic Urban Plans scan of Wright 1834.

The project's whole Wright geometry is keyed to ONE raster: the BPL/Leventhal
copy (`commonwealth:js957744g`, 4204 x 5166 px), whose pixel space the eight
ground-control points in `data/traces/gcp/wright_1834_gcps.json` live in. The
owner added a second copy in 2026-09-05 —
`chicago/pre_fire_v1/maps/images/1834-wright-map.jpg`, the Historic Urban Plans
(Ithaca) reproduction of the National Archives ORIGINAL, 5050 x 6628 px at 600
dpi — and at that resolution numerals are legible that the BPL scan cannot
resolve. Nothing could cite it, because a reading off a raster is evidence about
THAT raster and this project had no frame for it (T-0787).

    python3 tools/register_wright_nara.py               re-fit and write the JSON
    python3 tools/register_wright_nara.py --check       re-fit and diff against committed
    python3 tools/register_wright_nara.py --check-properties
                                                        offline: the literals only

What is being registered, and what the two sheets actually are
--------------------------------------------------------------
They are NOT two scans of one artifact. Opened side by side at the title, the
BPL sheet carries drop-shadowed block capitals and roman "DRWN BY J. S. WRIGHT,
ACCORDING TO SURVEY" — the finished, coloured drawing — while the NARA sheet is
hand-lettered throughout, "Chicago / by / Jas. S. Wright / according to survey",
in one hand with the tear repaired on cloth. Two drawings of one survey.

And yet their GEOMETRY corresponds at 1:1. The patch correspondences below,
taken blind across the whole sheet, land on scale 1.000 with no rotation and a
constant offset near (+316, +659) px: the second drawing was laid out from the
first at the same size, and the two reproductions happen to have been made at
nearly the same effective ppi. That is the finding this file exists to record,
and it is what makes the new sheet usable: a feature read on it comes back into
BPL pixel space, and therefore into the datum, through one affine.

Method — why patches and not points
-----------------------------------
Hand-picking control in the new sheet by eye would produce a second set of
opinions about eight street crossings, and the difference between the two sets
would then mix the sheets' real disagreement with two pickers' aim. So the fit
is measured instead: N square patches of the BPL raster, spread over the drawing
and chosen without reference to what they contain, each located in the NARA
raster by normalised cross-correlation over a small scale/rotation search. The
affine is least-squares over the patches that correlate above threshold; the
residual is reported in pixels, and the eight BPL control crossings are carried
through it and checked BY EYE afterwards (`control_checks` in the output).

Needs numpy, Pillow and the network (the BPL raster comes from IIIF, as in
tools/trace_river.py). Degrades to a clear skip without them, which is why
`--check-properties` — the offline half — is what tools/check.sh runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
NARA_REL = "chicago/pre_fire_v1/maps/images/1834-wright-map.jpg"
OUT = ROOT / "data/traces/gcp/wright_1834_nara_gcps.json"
BPL_GCPS = ROOT / "data/traces/gcp/wright_1834_gcps.json"
IIIF = "https://iiif.digitalcommonwealth.org/iiif/2/commonwealth:js957744g"

NARA_SHA256 = "dbb92c0188881d9b6cdf84801b9185a5715496a328125bde895a04058b173266"
NARA_SIZE = [5050, 6628]
BPL_SIZE = [4204, 5166]

# The patch grid, in BPL pixel coordinates: origin, step, patch side, and the
# correlation floor a patch must clear to be used as control.
PATCH = {"x0": 300, "y0": 300, "nx": 4, "ny": 5, "step_x": 950, "step_y": 950,
         "side": 700, "ncc_floor": 0.30, "residual_tol_px": 25, "min_inliers": 10}
SEARCH = {"scales": [0.98, 0.99, 1.00, 1.01, 1.02], "rotations_deg": [-1.0, 0.0, 1.0],
          "downsample": 4}


def die(msg: str, code: int = 1):
    print(msg)
    return code


def _fetch_bpl(cache: Path) -> bytes:
    if cache.exists():
        return cache.read_bytes()
    url = f"{IIIF}/full/full/0/default.jpg"
    with urllib.request.urlopen(url, timeout=300) as r:  # noqa: S310
        raw = r.read()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(raw)
    return raw


def _ncc(img, tpl, np):
    """Normalised cross-correlation of tpl over img; (best, (y, x) top-left)."""
    th, tw = tpl.shape
    H, W = img.shape
    t = tpl - tpl.mean()
    tn = float(np.linalg.norm(t))
    if tn == 0 or th >= H or tw >= W:
        return -1.0, (0, 0)
    num = np.fft.irfft2(np.fft.rfft2(img, (H, W)) * np.conj(np.fft.rfft2(t, (H, W))), (H, W))
    num = num[:H - th + 1, :W - tw + 1]
    ii = np.zeros((H + 1, W + 1), np.float64)
    i2 = np.zeros((H + 1, W + 1), np.float64)
    ii[1:, 1:] = np.cumsum(np.cumsum(img, 0), 1)
    i2[1:, 1:] = np.cumsum(np.cumsum(img * img, 0), 1)

    def box(I):
        return I[th:, tw:] - I[:-th, tw:] - I[th:, :-tw] + I[:-th, :-tw]

    S, S2 = box(ii), box(i2)
    var = S2 - S * S / (th * tw)
    var[var < 1e-6] = 1e-6
    r = num / (np.sqrt(var) * tn)
    idx = np.unravel_index(int(np.argmax(r)), r.shape)
    return float(r[idx]), (int(idx[0]), int(idx[1]))


def correspond(np, Image):
    ds = SEARCH["downsample"]
    nara_img = Image.open(REPO / NARA_REL).convert("L")
    bpl_raw = _fetch_bpl(Path("/tmp/wright_1834_bpl_full.jpg"))
    import io
    bpl_img = Image.open(io.BytesIO(bpl_raw)).convert("L")
    if list(nara_img.size) != NARA_SIZE or list(bpl_img.size) != BPL_SIZE:
        raise SystemExit(f"raster size changed: nara={nara_img.size} bpl={bpl_img.size}")
    nara = np.asarray(nara_img.reduce(ds), np.float32)
    bpl = np.asarray(bpl_img.reduce(ds), np.float32)

    out = []
    for j in range(PATCH["ny"]):
        for i in range(PATCH["nx"]):
            bx = PATCH["x0"] + i * PATCH["step_x"]
            by = PATCH["y0"] + j * PATCH["step_y"]
            side = PATCH["side"]
            if bx + side > BPL_SIZE[0] or by + side > BPL_SIZE[1]:
                continue
            p = bpl[by // ds:(by + side) // ds, bx // ds:(bx + side) // ds]
            pim = Image.fromarray(p.astype("uint8"))
            best = None
            for s in SEARCH["scales"]:
                for th in SEARCH["rotations_deg"]:
                    im = pim.resize((max(4, round(pim.size[0] * s)),
                                     max(4, round(pim.size[1] * s))), Image.LANCZOS)
                    if th:
                        im = im.rotate(th, resample=Image.BILINEAR, expand=True,
                                       fillcolor=int(p.mean()))
                    t = np.asarray(im, np.float32)
                    v, (yy, xx) = _ncc(nara, t, np)
                    if best is None or v > best[0]:
                        best = (v, s, th,
                                (xx + t.shape[1] / 2) * ds, (yy + t.shape[0] / 2) * ds)
            v, s, th, cx, cy = best
            out.append({
                "id": f"P{j}{i}",
                "bpl_patch": [bx, by, side, side],
                "bpl_px": [bx + side / 2, by + side / 2],
                "nara_px": [round(cx, 1), round(cy, 1)],
                "ncc": round(v, 3),
                "search_scale": s,
                "search_rotation_deg": th,
                "used": None,
            })
    return out


def fit_affine(np, src, dst):
    """Least-squares affine src -> dst. Returns (a,b,c,d,e,f), residuals."""
    A = np.array([[x, y, 1.0] for x, y in src])
    X = np.array([p[0] for p in dst])
    Y = np.array([p[1] for p in dst])
    cx, *_ = np.linalg.lstsq(A, X, rcond=None)
    cy, *_ = np.linalg.lstsq(A, Y, rcond=None)
    pred = np.stack([A @ cx, A @ cy], 1)
    res = np.linalg.norm(pred - np.array(dst), axis=1)
    return (float(cx[0]), float(cx[1]), float(cx[2]),
            float(cy[0]), float(cy[1]), float(cy[2])), res


def consensus_fit(np, corr):
    """Fit NARA px -> BPL px, dropping the patches that do not agree with the rest.

    A patch laid on the lake wash or on blank paper correlates against anything;
    that is not a picking error to be argued about, it is a patch with nothing in
    it, and the sheet itself says so — its match sits thousands of pixels from
    where every other patch puts it. So the outlier test is the CONSENSUS, not the
    correlation score: fit, drop the worst residual, refit, until every surviving
    patch is inside residual_tol_px.
    """
    live = [c for c in corr if c["ncc"] >= PATCH["ncc_floor"]]
    while True:
        coeffs, res = fit_affine(np, [c["nara_px"] for c in live], [c["bpl_px"] for c in live])
        worst = int(res.argmax())
        if res[worst] <= PATCH["residual_tol_px"] or len(live) <= PATCH["min_inliers"]:
            break
        live.pop(worst)
    keep = {id(c) for c in live}
    for c in corr:
        c["used"] = id(c) in keep
    if len(live) < PATCH["min_inliers"] or res.max() > PATCH["residual_tol_px"]:
        raise SystemExit(f"no consensus: {len(live)} patches, max residual {res.max():.0f} px")
    return coeffs, res, live


def apply_affine(c, x, y):
    a, b, cc, d, e, f = c
    return a * x + b * y + cc, d * x + e * y + f


def compose(outer, inner):
    """outer o inner, both (a,b,c,d,e,f) acting on (x, y)."""
    a1, b1, c1, d1, e1, f1 = inner
    a2, b2, c2, d2, e2, f2 = outer
    return (a2 * a1 + b2 * d1, a2 * b1 + b2 * e1, a2 * c1 + b2 * f1 + c2,
            d2 * a1 + e2 * d1, d2 * b1 + e2 * e1, d2 * c1 + e2 * f1 + f2)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_properties() -> int:
    """Offline: the committed file against this file's constants. No numpy."""
    bad = []
    if not OUT.exists():
        return die(f"MISSING {OUT}")
    d = json.loads(OUT.read_text())
    r = d["raster"]
    if r["path"] != NARA_REL:
        bad.append(f"raster.path {r['path']!r} != {NARA_REL!r}")
    if [r["width"], r["height"]] != NARA_SIZE:
        bad.append(f"raster size {[r['width'], r['height']]} != {NARA_SIZE}")
    if r["sha256"] != NARA_SHA256:
        bad.append("raster.sha256 does not match the constant in the generator")
    p = REPO / NARA_REL
    if p.exists():
        got = sha256(p)
        if got != NARA_SHA256:
            bad.append(f"the working copy of the sheet hashes {got[:12]}…, not the registered scan")
    else:
        print(f"   note: {NARA_REL} not in this checkout; checked the record only")
    if d["method"]["patch_grid"] != PATCH or d["method"]["search"] != SEARCH:
        bad.append("method block does not match the generator's parameters")
    used = [c for c in d["correspondences"] if c["used"]]
    if len(used) < 8:
        bad.append(f"only {len(used)} correspondences above the floor; the fit needs 8")
    fit = d["fit_nara_to_bpl"]
    for c in used:  # the affine really does carry its own control
        x, y = apply_affine([fit["coefficients"][k] for k in "abcdef"], *c["nara_px"])
        dx, dy = x - c["bpl_px"][0], y - c["bpl_px"][1]
        if (dx * dx + dy * dy) ** 0.5 > fit["max_px"] + 0.6:
            bad.append(f"{c['id']} residual exceeds the recorded max_px")
    chain = d["fit_nara_to_utm"]["coefficients"]
    bpl = json.loads(BPL_GCPS.read_text())["fit"]["coefficients"]
    want = compose([bpl[k] for k in "abcdef"], [fit["coefficients"][k] for k in "abcdef"])
    for k, w in zip("abcdef", want):
        if abs(chain[k] - w) > 1e-6:
            bad.append(f"fit_nara_to_utm.{k} is not the composition of the two committed affines")
    coeffs = [fit["coefficients"][k] for k in "abcdef"]
    for c in d["control_checks"]:
        missing = [k for k in ("bpl_gcp", "feature", "nara_px_predicted", "nara_px_read",
                               "bpl_px_read", "residual_px", "residual_m") if k not in c]
        if missing:
            bad.append(f"control check {c.get('bpl_gcp')} is missing {', '.join(missing)}")
            continue
        # the residual is arithmetic on two readings, so recompute it rather than trust it
        x, y = apply_affine(coeffs, *c["nara_px_read"])
        got = ((x - c["bpl_px_read"][0]) ** 2 + (y - c["bpl_px_read"][1]) ** 2) ** 0.5
        if abs(got - c["residual_px"]) > 0.15:
            bad.append(f"{c['bpl_gcp']}: residual_px {c['residual_px']} is not "
                       f"{got:.1f}, what the two readings give through the affine")
    bar = d["scale_bar"]
    for sheet, want_px in (("nara", NARA_SIZE[0]), ("bpl", BPL_SIZE[0])):
        b = bar[sheet]
        if not 0 < b["fitted_px_per_ft"] < 1:
            bad.append(f"scale_bar.{sheet}: px_per_ft out of range")
        m = 0.3048 / b["fitted_px_per_ft"]
        if abs(m - b["m_per_px"]) > 0.0005:
            bad.append(f"scale_bar.{sheet}: m_per_px {b['m_per_px']} is not 0.3048/px_per_ft")
        if b["band_px"][0] > want_px or b["band_px"][2] > want_px:
            bad.append(f"scale_bar.{sheet}: band is off the sheet")
    seen = set()
    for r in d["lacunae"]["regions"]:
        if r["id"] in seen:
            bad.append(f"lacuna {r['id']} declared twice")
        seen.add(r["id"])
        if r["confidence"] not in ("documented", "inferred", "conjectural"):
            bad.append(f"lacuna {r['id']}: confidence {r['confidence']!r} is not a grade")
        box = r.get("box_px")
        if box and (box[0] >= box[2] or box[1] >= box[3]
                    or box[2] > NARA_SIZE[0] or box[3] > NARA_SIZE[1]):
            bad.append(f"lacuna {r['id']}: box_px is empty or off the sheet")
    if not d["lacunae"].get("second_portion"):
        bad.append("the caption names two missing portions; the record must say where the "
                   "second one stands, even when the answer is that it was not found")
    if bad:
        print("FAIL — the registration record and its generator disagree:")
        for b in bad:
            print("   " + b)
        return 1
    print(f"   ok: {OUT.name} carries {len(used)} correspondences, "
          f"rms {fit['rms_px']} px, and the chained affine composes")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="re-fit and diff against the committed file")
    ap.add_argument("--check-properties", action="store_true",
                    help="offline: hold the committed file to this file's literals")
    args = ap.parse_args()
    if args.check_properties:
        return check_properties()
    try:
        import numpy as np
        from PIL import Image
    except ModuleNotFoundError as e:
        return die(f"SKIP: {e.name} not installed (pip install numpy pillow)")
    Image.MAX_IMAGE_PIXELS = None

    corr = correspond(np, Image)
    coeffs, res, used = consensus_fit(np, corr)
    bpl_fit = json.loads(BPL_GCPS.read_text())["fit"]["coefficients"]
    chain = compose([bpl_fit[k] for k in "abcdef"], coeffs)
    prior = json.loads(OUT.read_text()) if OUT.exists() else {}
    doc = dict(prior)
    doc["_doc"] = (
        "Registration of the National Archives / Historic Urban Plans reproduction of "
        "Wright 1834 against the BPL master this project already traces. Pixel coordinates "
        "under `nara_px` are in THIS sheet's own space (5050 x 6628). Generated by "
        "tools/register_wright_nara.py — the fit and the correspondences are computed; the "
        "control checks, the scale bar and the lacunae are read by eye and hand-written."
    )
    doc["raster"] = {
        "path": NARA_REL,
        "width": NARA_SIZE[0], "height": NARA_SIZE[1],
        "sha256": NARA_SHA256,
        "dpi": 600,
        "source_id": "wright_1834_nara_hup",
    }
    doc["registered_against"] = {
        "source_id": "wright_1834",
        "iiif_image": IIIF,
        "width": BPL_SIZE[0], "height": BPL_SIZE[1],
        "gcps": "data/traces/gcp/wright_1834_gcps.json",
    }
    doc["method"] = {"patch_grid": PATCH, "search": SEARCH,
                     "note": "Patches are placed on a blind grid over the BPL sheet and located "
                             "in the NARA sheet by normalised cross-correlation. A patch below "
                             "ncc_floor is carried in the record and excluded from the fit."}
    doc["fit_nara_to_bpl"] = {
        "type": "affine, least squares, NARA/HUP pixel -> BPL pixel",
        "coefficients": dict(zip("abcdef", [round(v, 8) for v in coeffs])),
        "rms_px": round(float((res ** 2).mean() ** 0.5), 2),
        "max_px": round(float(res.max()), 2),
        "n": len(used),
    }
    doc["fit_nara_to_utm"] = {
        "type": "affine, NARA/HUP pixel -> EPSG:26916, composed with the BPL fit",
        "coefficients": dict(zip("abcdef", [round(v, 9) for v in chain])),
    }
    doc["correspondences"] = corr
    if args.check:
        if not prior:
            return die("no committed file to check against")
        old = prior["fit_nara_to_bpl"]["coefficients"]
        drift = max(abs(old[k] - doc["fit_nara_to_bpl"]["coefficients"][k]) for k in "abcdef")
        print(f"   re-fit max coefficient drift {drift:.6g}")
        return 0 if drift < 1e-6 else 1
    OUT.write_text(json.dumps(doc, indent=2) + "\n")
    print(f"wrote {OUT} — {len(used)}/{len(corr)} patches, rms {doc['fit_nara_to_bpl']['rms_px']} px")
    return 0


if __name__ == "__main__":
    sys.exit(main())
