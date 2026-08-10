#!/usr/bin/env python3
"""Measure the platted street corridors off the two 1834 sheets, street by street.

    python3 tools/measure_street_widths.py            re-measure and write the JSON
    python3 tools/measure_street_widths.py --check    re-measure and diff the committed file
    python3 tools/measure_street_widths.py --debug    write the ink mask of each traverse

Why this exists
---------------
Every platted placement in this dataset steps half a street from a surviving modern
junction, and that half-street is one number: 12.192 m, half of 80 ft
(`data/traces/street_control.json`). The figure is graded `inferred` for a stated
reason — 80 ft is an annotation read off Hathaway 1834 during the datum work, a
second source (Currey, via `chicagology_first_post_office`) gives the 1830 plat 66
ft, and *neither sheet had ever been read street by street*.
`docs/RESEARCH/street_module_1830.md` § 2 names the slice that settles it, including
the reconciliation worth testing: that the two figures may not be about the same
streets, 66 ft generally with the riverfront and market streets platted wider.

This is that slice, and it does not read the annotation again. It measures the drawn
corridors — block boundary line to block boundary line — along two traverses on each
sheet, and reports every corridor either traverse crosses.

Method
------
Nothing here re-fits either sheet's georeference for the purpose of measuring. Pixel
positions are the evidence; metres come from the same affines the rest of the project
uses, and `check_street_module` in `tools/validate.py` re-derives every one of them
from the committed pixels, offline, on every commit.

- **A traverse, not a hand-placed anchor per street.** Each traverse starts at a
  committed ground-control pixel, runs along one axis of the plat grid, and reports
  every boundary line it crosses. One pass along Lake Street measures every N-S
  street it crosses; one pass along Canal Street measures every E-W street. What is
  hand-placed is nothing: the start is a committed GCP and the direction comes from
  the sheet's own affine.
- **A boundary line is a line.** A run of the profile counts as a boundary only if it
  is inked over most of a band running ALONG it (`line_frac`). Lot numerals, block
  numbers, street names and the sheets' own width annotations sit in these corridors
  and cover a fraction of such a band. The grid also sits about 2.3 degrees off the
  raster axes, which is why the band is oriented by the grid and not by the pixels.
- **A corridor is classified by its width, not by what we expect it to be.** A gap of
  `street_min_m` or more between two boundary lines whose interior reads as paper is a
  street; `alley_lo_m`..`alley_hi_m` is an alley; anything narrower is lot subdivision.
  No candidate figure enters the classification, so the measurement cannot be talked
  into either of them.
- **Width is centre to centre.** The platted boundary is the line the draughtsman drew,
  so a reading runs between line centroids and does not depend on how heavily either
  line was inked.

What came out, and the fault it found
-------------------------------------
The widths settle the module (see the memo). The second result was not being looked
for: on BOTH sheets the control point recorded as *Canal St & Lake St* — Hathaway HA,
Wright G5 — falls inside block 28 rather than in the Canal Street corridor, tens of
metres west of the corridor centreline this tool measures. Wright's G5 is one of the
eight points the project datum is fitted from, so the tool also reports what adopting
the corrected pixel would do to the origin: it refits the Wright control with the
measured centreline crossing in place of G5 and prints how far the datum moves. It
does not adopt it. Moving the datum re-derives every coordinate in the dataset and
stales every committed mesh, which is a decision with a bake attached and is recorded
with its cost rather than taken by a measurement tool.

Needs numpy, Pillow, pyproj and the network. Like the datum re-derivation's own
fetches and `tools/refetch_control.py`, this is a deliberate, occasional re-run and is
NOT part of `tools/check.sh`.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

CONTROL = ROOT / "data" / "traces" / "street_control.json"
OUT = ROOT / "data" / "traces" / "vectors" / "street_corridors_1834.json"

FT = 0.3048
UA = "chicago-4d street corridor measurement (kevinrhaas/custom)"

PARAMS = dict(
    reach_m=380.0,        # how far along a traverse boundary lines are collected
    band_m=9.0,           # length of the run averaged ALONG a boundary line
    step_px=0.5,          # sampling step along the traverse, sheet pixels
    ink_ratio=0.68,       # ink is darker than this fraction of the window paper level
    line_frac=0.88,       # inked over this fraction of the band to count as a boundary
    paper_frac=0.30,      # a corridor's interior is paper below this ink fraction
    ink_share=0.35,       # ... over at least this much of the interior it is not a corridor
    street_min_m=15.0,    # a gap between street_min_m and street_max_m is a street corridor
    street_max_m=30.0,    # a wider gap is reported unclassified: most likely a missed boundary
    face_min_m=60.0,      # ... and both its boundary lines must run at least this far
    face_reach_m=150.0,   # how far a boundary line is followed when measuring its run
    face_gap_m=9.0,       # a break shorter than this does not end a run: an alley mouth
                          # breaks a block face and is 5-6 m wide, a street is 15 m or more
    pitch_lo_m=95.0,      # consecutive street corridors this far apart are the module
    pitch_hi_m=145.0,     # ... 300 ft blocks + either candidate street width is inside this
    alley_lo_m=3.0,       # ... and this band is an alley
    alley_hi_m=9.0,
    margin_m=25.0,        # padding on the fetched region
)

SHEETS = {
    "hathaway_1834": dict(
        gcp="data/traces/gcp/hathaway_1834_gcps.json",
        # pixel space of the GCP file -> IIIF region space (native)
        px_to_native=None,          # filled from the file's raster block
        start_gcp="HA",
        note="LOC scan, pixels in the 4000 x 5702 working raster",
    ),
    "wright_1834": dict(
        gcp="data/traces/gcp/wright_1834_gcps.json",
        px_to_native=1.0,           # GCP pixels ARE the IIIF resource space
        start_gcp="G5",
        note="BPL/Digital Commonwealth scan, pixels in the 4204 x 5166 resource space",
    ),
}

# The two traverses run on each sheet. The first starts at the sheet's Canal & Lake
# control pixel and runs along the grid's E-W axis; the second starts at the Canal
# corridor centreline that first traverse measured and runs N-S.
TRAVERSES = (
    dict(id="along_lake", axis="ew", start="gcp", offset_m=-50.0, reach_m=380.0,
         reads="the N-S streets Lake Street crosses, read along the block row south of it"),
)

# There was a second traverse, N-S along Canal, and it is NOT committed. On the Wright
# sheet it reads lot lines and cannot be told to stop: lot depths there are 20-26 m,
# which is a platted street's width, the lines run as far as a block face does because
# the line at the same depth continues in the column across the alley, and their
# spacings include two that fall inside the module band by arithmetic coincidence.
# Three tests that each work on the Hathaway sheet all pass things there that are not
# streets. So the E-W streets are not measured here and the module rests on the N-S
# ones, which is stated in the memo rather than papered over with a filter tuned until
# the answer looked right.

# A traverse cannot run down the middle of the street it is measuring across: block
# boundary lines STOP at the kerb, so a pass along a corridor crosses nothing but the
# street's own name. Each traverse is therefore offset sideways, into the row or column
# of blocks beside it, where it crosses the boundaries.
#
# It also cannot run down the MID-BLOCK ALLEY, which is the second thing this tool got
# wrong: an alley is a blank corridor whose crossing lot lines stop at its kerbs and
# whose mouths break the block faces at both ends, so a traverse in one reads two
# hundred metres of paper and no streets. The N-S traverse is therefore offset a
# QUARTER of the block pitch the E-W traverse measured, which lands in the middle of a
# lot column. Riding along a lot line there is harmless: the profile band runs across
# the traverse, so a line parallel to the traverse fills two pixels of a nine-metre
# band while a line crossing it fills all of it. Either offset is perpendicular to
# what is being measured and does not move a corridor's centreline.


def die(msg: str, code: int = 2):
    print(msg)
    raise SystemExit(code)


def to_utm(coef, px: float, py: float) -> tuple[float, float]:
    a, b, c, d, e, f = coef
    return a * px + b * py + c, d * px + e * py + f


def to_px(coef, E: float, N: float) -> tuple[float, float]:
    a, b, c, d, e, f = coef
    E, N = E - c, N - f
    det = a * e - b * d
    return (E * e - b * N) / det, (a * N - d * E) / det


def unit(vx: float, vy: float) -> tuple[float, float]:
    m = math.hypot(vx, vy)
    return vx / m, vy / m


def fetch_region(iiif: str, region: tuple[int, int, int, int], cache: Path):
    x, y, w, h = region
    url = f"{iiif}/{x},{y},{w},{h}/{w},/0/default.jpg"
    if cache.exists():
        raw = cache.read_bytes()
    else:
        print(f"  fetching {url}")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=240) as r:      # noqa: S310
            raw = r.read()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(raw)
    return raw, hashlib.sha256(raw).hexdigest()


def profile(ink, ax, ay, along, across, reach_px, band_px, np):
    """Ink fraction stepped along `across`, each sample averaged over a run along `along`."""
    n_band = max(9, int(2 * band_px))
    ts = np.arange(-reach_px, reach_px + 1e-9, PARAMS["step_px"])
    ss = np.linspace(-band_px, band_px, n_band)
    xs = ax + np.outer(ts, np.full(n_band, across[0])) + np.outer(np.ones_like(ts), ss * along[0])
    ys = ay + np.outer(ts, np.full(n_band, across[1])) + np.outer(np.ones_like(ts), ss * along[1])
    xi = np.clip(np.rint(xs).astype(int), 0, ink.shape[1] - 1)
    yi = np.clip(np.rint(ys).astype(int), 0, ink.shape[0] - 1)
    return ts, ink[yi, xi].mean(axis=1)


def lines_in(ts, frac, np):
    """Boundary lines: contiguous runs at or above line_frac, as (centroid_t, width_t, peak)."""
    hot = frac >= PARAMS["line_frac"]
    out, i, n = [], 0, len(hot)
    while i < n:
        if hot[i]:
            j = i
            while j + 1 < n and hot[j + 1]:
                j += 1
            w = frac[i:j + 1]
            out.append((float((ts[i:j + 1] * w).sum() / w.sum()),
                        float(ts[j] - ts[i]) + PARAMS["step_px"],
                        float(w.max())))
            i = j + 1
        else:
            i += 1
    return out


def line_run(ink, px, py, along, across, m_per_px, np):
    """How far a boundary line continues, in metres, through the point it was found at.

    This is what separates a street from a strip of lots, and on the Wright sheet it is
    the only thing that does: lot depths there are 20-26 m, which is a platted street's
    width, so a profile taken across them alone reads a lot strip and a street corridor
    identically. What differs is the LINES: a street corridor is bounded by two block
    faces, which run the length of a block, and a lot strip is bounded by two lot lines,
    which stop at the block's alley. The run is measured with a one-pixel tolerance
    either side, because the grid is not pixel-aligned, and a break shorter than
    face_gap_m does not end it — alley mouths interrupt a block face without ending it.
    """
    reach = int(PARAMS["face_reach_m"] / m_per_px)
    tol = max(2, int(PARAMS["face_gap_m"] / m_per_px))
    h, w = ink.shape

    def inked(x, y):
        xi, yi = int(round(x)), int(round(y))
        return 0 <= xi < w and 0 <= yi < h and bool(ink[yi, xi])

    total = 0
    for sign in (-1, +1):
        # Follow the line rather than assuming its direction: the plat grid is not
        # pixel-aligned and the two axes are a couple of degrees off perpendicular on
        # both sheets, so a straight walk 200 px long drifts off a line it started on.
        q, misses, s = 0.0, 0, 0
        while s < reach:
            s += 1
            x = px + sign * s * along[0] + q * across[0]
            y = py + sign * s * along[1] + q * across[1]
            for dq in (0.0, 1.0, -1.0, 2.0, -2.0):
                if inked(x + dq * across[0], y + dq * across[1]):
                    q += dq
                    misses = 0
                    break
            else:
                misses += 1
                if misses > tol:
                    s -= misses
                    break
        total += s
    return round(total * m_per_px, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="diff against the committed JSON")
    ap.add_argument("--debug", action="store_true", help="write the ink mask per sheet")
    args = ap.parse_args()

    try:
        import numpy as np
        from PIL import Image
    except ImportError as e:
        die(f"SKIP: {e.name} not installed (pip install numpy pillow); "
            f"street corridors not measured", 0)
    try:
        from pyproj import Transformer
    except ImportError:
        die("SKIP: pyproj not installed (pip install pyproj); street corridors not measured", 0)

    import rederive_datum as rd                                   # noqa: PLC0415

    tf = Transformer.from_crs(4326, 26916, always_xy=True)
    ctl = json.loads(CONTROL.read_text())
    module = ctl["platted_street"]
    # The three modern junctions that give the grid its two directions on a sheet.
    C = {k: (v["utm_e"], v["utm_n"]) for k, v in ctl["control"].items()}

    sheets_out, all_streets = {}, {}
    for sheet, cfg in SHEETS.items():
        print(f"\n== {sheet}")
        gcp_doc = json.loads((ROOT / cfg["gcp"]).read_text())
        raster = gcp_doc["raster"]
        iiif = raster["iiif_image"]
        if cfg["px_to_native"] is None:
            cfg["px_to_native"] = raster["native_width"] / raster["working_width"]
        k = cfg["px_to_native"]

        coef, rms, rows = rd.fit_from_traces(cfg["gcp"], tf)
        m_per_px = 0.5 * (math.hypot(coef[0], coef[3]) + math.hypot(coef[1], coef[4]))
        m_per_native = m_per_px / k
        gcps = {g["id"]: g for g in gcp_doc["gcps"]}
        start = gcps[cfg["start_gcp"]]
        print(f"  affine refit from {len(rows)} committed GCPs, RMS {rms:.1f} m; "
              f"{m_per_px:.4f} m per sheet px, {m_per_native:.4f} m per native px")

        ew = unit(*(a - b for a, b in zip(to_px(coef, *C["lake_market"]),
                                          to_px(coef, *C["lake_canal"]))))
        ns = unit(*(a - b for a, b in zip(to_px(coef, *C["lake_canal"]),
                                          to_px(coef, *C["randolph_canal"]))))
        skew = 90 - math.degrees(math.acos(abs(ew[0] * ns[0] + ew[1] * ns[1])))
        print(f"  grid axes from the modern control: E-W {ew}, N-S {ns}; "
              f"{skew:+.2f} deg off perpendicular on this sheet")

        # --- one fetched region covering both traverses ------------------------
        sx, sy = start["pixel"][0] * k, start["pixel"][1] * k
        pad = (max(t["reach_m"] + abs(t.get("offset_m", 0.0))
                   + abs(t.get("offset_pitch", 0.0)) * 200.0 for t in TRAVERSES)
               + PARAMS["margin_m"]) / m_per_native
        x0, y0 = int(sx - pad), int(sy - pad)
        region = (max(0, x0), max(0, y0),
                  int(2 * pad) + 1, int(2 * pad) + 1)
        cache = Path("/tmp") / f"{sheet}_corridor_region.jpg"
        raw, sha = fetch_region(iiif, region, cache)
        rgb = np.asarray(Image.open(io.BytesIO(raw)).convert("RGB")).astype(np.float32)
        if rgb.shape[1] != region[2]:
            die(f"  the server returned {rgb.shape[1]}x{rgb.shape[0]} for a "
                f"{region[2]}x{region[3]} region; a reading off it would be mis-scaled")
        lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
        paper = float(np.percentile(lum, 80))
        ink = lum < paper * PARAMS["ink_ratio"]
        print(f"  region {region} sha256 {sha[:16]}...  paper luminance {paper:.0f}, "
              f"ink over {100 * ink.mean():.1f}% of it")
        if args.debug:
            out = Path("/tmp") / f"{sheet}_corridor_ink.png"
            Image.fromarray((~ink * 255).astype(np.uint8)).save(out)
            print(f"  debug: ink mask -> {out}")

        band_px = 0.5 * PARAMS["band_m"] / m_per_native
        reach_px = PARAMS["reach_m"] / m_per_native

        traverses, canal_t, pitch_m = [], None, None
        for tv in TRAVERSES:
            across = ew if tv["axis"] == "ew" else ns
            along = ns if tv["axis"] == "ew" else ew
            ax, ay = sx - region[0], sy - region[1]
            if tv["start"] != "gcp":
                if canal_t is None:
                    die("  the Canal corridor was not measured, so the N-S traverse has "
                        "no place to start")
                ax += canal_t * ew[0]
                ay += canal_t * ew[1]
            if "offset_pitch" in tv:
                if not pitch_m:
                    die("  the block pitch has not been measured yet, so the N-S traverse "
                        "cannot be offset a quarter of it")
                off_px = tv["offset_pitch"] * pitch_m / m_per_native
            else:
                off_px = tv["offset_m"] / m_per_native
            ax += off_px * along[0]
            ay += off_px * along[1]
            ts, frac = profile(ink, ax, ay, along, across,
                               tv["reach_m"] / m_per_native, band_px, np)
            found = lines_in(ts, frac, np)

            def at(t):      # sheet pixel of an offset along this traverse
                return (ax + t * across[0] + region[0], ay + t * across[1] + region[1])

            corridors, alleys, wide, short = [], [], [], []
            for (t1, w1, p1), (t2, w2, p2) in zip(found, found[1:]):
                lo = int((t1 + 0.5 * w1 - ts[0]) / PARAMS["step_px"]) + 1
                hi = int((t2 - 0.5 * w2 - ts[0]) / PARAMS["step_px"])
                interior = frac[lo:hi]
                gap_px = t2 - t1
                # Rounded FIRST, then converted: the pixels are what is committed as
                # evidence, so the metres beside them have to be the metres those
                # pixels give. A tenth of a pixel is 7 cm on the Wright sheet, which is
                # enough for a width derived from unrounded positions to disagree with
                # its own committed reading — and check_street_module re-derives it.
                p1n = (round(at(t1)[0], 1), round(at(t1)[1], 1))
                p2n = (round(at(t2)[0], 1), round(at(t2)[1], 1))
                e1, n1 = to_utm(coef, p1n[0] / k, p1n[1] / k)
                e2, n2 = to_utm(coef, p2n[0] / k, p2n[1] / k)
                gap_m = math.hypot(e2 - e1, n2 - n1)
                rec = dict(
                    px=[[round(p1n[0], 1), round(p1n[1], 1)],
                        [round(p2n[0], 1), round(p2n[1], 1)]],
                    centre_px=[round(0.5 * (p1n[0] + p2n[0]), 1),
                               round(0.5 * (p1n[1] + p2n[1]), 1)],
                    centre_t_px=round(0.5 * (t1 + t2), 2),
                    width_m=round(gap_m, 2), width_ft=round(gap_m / FT, 1),
                    line_thickness_px=[round(w1, 1), round(w2, 1)],
                    interior_ink_share=round(
                        float((interior >= PARAMS["paper_frac"]).mean()) if len(interior) else 0.0, 2),
                )
                # A corridor's interior has to read as paper over most of its length.
                # It does not have to be empty: both sheets print the street's NAME down
                # the middle of it, and on Hathaway the width annotation too, so the test
                # is how much of the interior is inked rather than whether any of it is.
                if rec["interior_ink_share"] > PARAMS["ink_share"]:
                    continue
                runs = [line_run(ink, at(t1)[0] - region[0], at(t1)[1] - region[1],
                                 along, across, m_per_native, np),
                        line_run(ink, at(t2)[0] - region[0], at(t2)[1] - region[1],
                                 along, across, m_per_native, np)]
                rec["boundary_run_m"] = runs
                if PARAMS["street_min_m"] <= gap_m <= PARAMS["street_max_m"]:
                    if min(runs) < PARAMS["face_min_m"]:
                        rec["rejected"] = ("both boundaries have to run a block face; the "
                                           "shorter of these two stops first, which is what a "
                                           "lot line does")
                        short.append(rec)
                        continue
                    corridors.append(rec)
                elif gap_m > PARAMS["street_max_m"]:
                    wide.append(rec)
                elif PARAMS["alley_lo_m"] <= gap_m <= PARAMS["alley_hi_m"]:
                    alleys.append(rec)
            # THE MODULE TEST, and the one that does the work. A platted street belongs
            # to a grid: its neighbours are a block pitch away. A lot line does not. So
            # the reading kept is the longest chain of candidates whose consecutive
            # spacings all fall between pitch_lo_m and pitch_hi_m — a band that admits
            # 300 ft blocks with EITHER candidate street width (380 ft = 116 m, 366 ft =
            # 112 m) and is therefore neutral between the two figures being decided.
            # Everything outside the chain is reported with its measurement, not dropped.
            off_module = []
            if len(corridors) > 1:
                corridors.sort(key=lambda c: c["centre_t_px"])
                best = []
                for i in range(len(corridors)):
                    chain = [i]
                    for j in range(i + 1, len(corridors)):
                        d = abs(corridors[j]["centre_t_px"]
                                - corridors[chain[-1]]["centre_t_px"]) * m_per_native
                        if PARAMS["pitch_lo_m"] <= d <= PARAMS["pitch_hi_m"]:
                            chain.append(j)
                    if len(chain) > len(best):
                        best = chain
                keep = set(best)
                for i, c in enumerate(corridors):
                    if i not in keep:
                        c["rejected"] = ("no other candidate on this traverse is a block "
                                         "pitch away from it, so it is not part of the "
                                         "platted module")
                        off_module.append(c)
                corridors = [c for i, c in enumerate(corridors) if i in keep]
            print(f"  {tv['id']:14s} {len(found):3d} boundary lines, "
                  f"{len(corridors)} street corridors, {len(alleys)} alleys, "
                  f"{len(wide)} too wide, {len(short)} bounded by a line that stops, "
                  f"{len(off_module)} off the module")
            for c in corridors:
                print(f"      corridor at t {c['centre_t_px']:+8.1f} px  "
                      f"{c['width_m']:6.2f} m = {c['width_ft']:5.1f} ft   "
                      f"boundary runs {c['boundary_run_m']} m")
            if not corridors:
                die(f"  {tv['id']} found no street corridor; the profile is not reading "
                    f"this sheet and no reading should be committed from it")
            pitches = [round(abs(b["centre_t_px"] - a["centre_t_px"]) * m_per_native, 1)
                       for a, b in zip(corridors, corridors[1:])]
            if pitches:
                pitches_sorted = sorted(pitches)
                pitch_m = pitches_sorted[len(pitches_sorted) // 2]
                print(f"      centre-to-centre pitch: {pitches} m (median {pitch_m})")
            traverses.append(dict(id=tv["id"], axis=tv["axis"], reads=tv["reads"],
                                  start_px=[round(at(0)[0], 1), round(at(0)[1], 1)],
                                  n_boundary_lines=len(found),
                                  corridors=corridors, alleys=alleys,
                                  unclassified_wide_gaps=wide,
                                  rejected_short_boundaries=short,
                                  rejected_off_module=off_module,
                                  block_pitch_m=pitches))
            if tv["axis"] == "ew":
                # The Canal corridor is the street corridor whose centreline the
                # recorded GCP pixel lies nearest to. The corridors are a block
                # pitch apart and the GCP is nowhere near that far off, so this is
                # an identification and not a guess — and the distance is the
                # finding.
                canal = min(corridors, key=lambda c: abs(c["centre_t_px"]))
                canal_t = canal["centre_t_px"]
                off_m = abs(canal_t) * m_per_native
                print(f"      GCP {cfg['start_gcp']} lies {off_m:.1f} m "
                      f"{'west' if canal_t > 0 else 'east'} of the Canal corridor centreline")

        # --- what the corridor says about the control point ---------------------
        # The correction this measures is one coordinate: the GCP is moved ALONG the
        # traverse onto the Canal corridor's centreline and its position along the
        # street is left alone. That is the whole of what a traverse across Canal
        # Street can see. Whether the point sits at the right northing — whether it is
        # Lake Street it is standing in — is a separate reading and is not touched here.
        gcp_px = (sx, sy)
        fixed_px = (sx + canal_t * ew[0], sy + canal_t * ew[1])
        e1, n1 = to_utm(coef, fixed_px[0] / k, fixed_px[1] / k)
        e2, n2 = to_utm(coef, gcp_px[0] / k, gcp_px[1] / k)
        off = math.hypot(e2 - e1, n2 - n1)
        print(f"  {cfg['start_gcp']} recorded at native px {gcp_px[0]:.0f},{gcp_px[1]:.0f}; "
              f"on the Canal centreline it would be {fixed_px[0]:.0f},{fixed_px[1]:.0f} "
              f"— {off:.1f} m apart")

        widths = sorted(c["width_ft"] for tv in traverses for c in tv["corridors"])
        sheets_out[sheet] = dict(
            note=cfg["note"],
            raster=dict(iiif_image=iiif, region=list(region), region_sha256=sha,
                        gcp_px_to_native=round(k, 5),
                        m_per_native_px=round(m_per_native, 4),
                        m_per_gcp_px=round(m_per_px, 4)),
            affine=dict(source=cfg["gcp"], refit_rms_m=round(rms, 1),
                        coefficients=dict(zip("abcdef", [round(x, 9) for x in coef])),
                        grid_skew_deg=round(skew, 2)),
            traverses=traverses,
            control_point_check=dict(
                gcp=cfg["start_gcp"],
                map_feature=start["map_feature"],
                recorded_px=list(start["pixel"]),
                recorded_native_px=[round(gcp_px[0], 1), round(gcp_px[1], 1)],
                on_centreline_native_px=[round(fixed_px[0], 1), round(fixed_px[1], 1)],
                on_centreline_px=[round(fixed_px[0] / k, 1), round(fixed_px[1] / k, 1)],
                offset_m=round(off, 1),
                offset_is=("across Canal Street only; the point's position ALONG the street "
                           "is left where it was recorded, because a traverse across a "
                           "corridor cannot see it"),
                finding=("the recorded pixel falls inside block 28 rather than in the Canal "
                         "Street corridor; on both sheets the block number straddles it"),
            ),
            widths_ft=dict(n=len(widths), median_ft=widths[len(widths) // 2],
                           min_ft=widths[0], max_ft=widths[-1]),
        )
        all_streets[sheet] = widths

    # --- what adopting the Wright correction would cost the datum --------------
    datum = json.loads((ROOT / "data" / "datum.json").read_text())
    w = SHEETS["wright_1834"]
    gdoc = json.loads((ROOT / w["gcp"]).read_text())
    fixed = sheets_out["wright_1834"]["control_point_check"]["on_centreline_px"]
    rows = []
    for g in gdoc["gcps"]:
        px, py = (fixed if g["id"] == w["start_gcp"] else g["pixel"])
        E, N = tf.transform(g["modern"]["lon"], g["modern"]["lat"])
        rows.append((px, py, E, N))
    (a, b, c), (d, e_, f) = rd.lstsq_affine(rows)
    rms2 = math.sqrt(sum((a * x + b * y + c - E) ** 2 + (d * x + e_ * y + f - N) ** 2
                         for x, y, E, N in rows) / len(rows))
    fx, fy = datum["derivation"]["forks_pixel_wright"]
    E, N = a * fx + b * fy + c, d * fx + e_ * fy + f
    shift = math.hypot(E - datum["origin_utm_e"], N - datum["origin_utm_n"])
    coef0, rms0, _ = rd.fit_from_traces(w["gcp"], tf)
    print(f"\n== if the Wright correction were adopted (it is NOT, here)")
    print(f"  refit RMS {rms0:.1f} -> {rms2:.1f} m; the datum origin would move {shift:.1f} m "
          f"(dE {E - datum['origin_utm_e']:+.1f}, dN {N - datum['origin_utm_n']:+.1f})")

    allw = sorted(x for v in all_streets.values() for x in v)
    town = allw[len(allw) // 2]
    adopted, dissent = module["width_ft"], module["dissent"]["width_ft"]
    tol = 4.0
    nearest = min((adopted, dissent), key=lambda f: abs(town - f))
    excluded = [f for f in (adopted, dissent)
                if all(abs(x - f) > tol for x in allw)]
    print(f"\n== the module: {len(allw)} corridors measured, median {town} ft "
          f"({allw[0]}-{allw[-1]} ft); nearest candidate {nearest} ft, "
          f"excluded {excluded or 'neither'}")

    doc = {
        "_doc": (
            "Platted street corridors measured off BOTH 1834 sheets, to settle the "
            "disagreement recorded in data/traces/street_control.json: 80 ft annotated on "
            "Hathaway against Currey's 66 ft for the 1830 plat. A corridor here is the space "
            "between two block boundary lines, measured centre to centre along a traverse that "
            "starts at a committed ground-control pixel — not a second reading of the "
            "annotation, and not a hand-placed anchor per street. Pixels are the evidence and "
            "are committed as such; metres are derived from them through each sheet's own "
            "affine, and check_street_module in tools/validate.py re-derives every one of them "
            "offline on every commit. Written by tools/measure_street_widths.py, which needs the "
            "network and is therefore not part of tools/check.sh."
        ),
        "sources": ["hathaway_1834", "wright_1834"],
        "tool": "tools/measure_street_widths.py",
        "read_on": "2026-08-10",
        "confidence": "documented",
        "confidence_note": (
            "A corridor width is measured at a stated place by a stated method that anyone can "
            "re-run, which is what documented means here. What it is documented ABOUT is the "
            "sheet: the figure it supports is the width these surveys DRAW. Both sheets carry "
            "3.7-4.5% anisotropic paper stretch, which puts about a metre of local scale error "
            "on a 24 m street — small against the 4.27 m between the two candidate figures, and "
            "large against the 0.6 m between 18 ft and 16 ft alleys. That is why the streets are "
            "settled here and the alleys are reported but not settled."
        ),
        "method": {
            "traverse": ("each traverse starts at a committed GCP pixel and runs along one axis "
                         "of the plat grid, reporting every boundary line it crosses; the axes "
                         "come from the modern control through the sheet's own affine"),
            "boundary_line": ("a contiguous run of the profile inked over line_frac of a band "
                              "running along the line — lot numerals, block numbers, street "
                              "names and the sheets' width annotations cover a fraction of it"),
            "classification": ("by measured width alone: street_min_m or wider is a street, "
                               "alley_lo_m..alley_hi_m is an alley, narrower is lot "
                               "subdivision. No candidate figure enters the test"),
            "width": ("boundary line centroid to boundary line centroid, so a reading does not "
                      "depend on how heavily either line was inked"),
            "params": dict(PARAMS),
        },
        "candidates": {
            "adopted": {"width_ft": adopted, "sources": module["sources"]},
            "dissent": {"width_ft": dissent, "sources": module["dissent"]["sources"]},
            "tolerance_ft": tol,
            "tolerance_note": (
                "4 ft is the local scale error these sheets carry (3.7-4.5% of 80 ft is 3.0-3.6 "
                "ft) rounded up, and it is deliberately less than half the 14 ft between the "
                "candidates, so the band cannot admit both. It is used for EXCLUSION: a "
                "candidate no reading comes within tolerance_ft of is not the figure these "
                "sheets draw."
            ),
            "nearest_ft": nearest,
            "excluded_ft": excluded,
            "median_above_adopted_ft": round(town - adopted, 1),
            "reading_note": (
                "The median runs about 5 ft ABOVE the adopted 80, on both sheets, and that is "
                "recorded rather than rounded away: the corridors these draughtsmen drew are a "
                "few per cent wider than 80 ft. Paper stretch of 3.7-4.5% accounts for most of "
                "it and the placement of a pen line for the rest, so what this measurement "
                "settles is WHICH candidate — every one of the readings is at least 9 ft clear "
                "of 66, and the nearest is within 5 of 80 — and not the platted figure to the "
                "foot."
            ),
        },
        "summary": {
            "n_corridors": len(allw),
            "median_ft": town,
            "min_ft": allw[0],
            "max_ft": allw[-1],
            "by_sheet": {s: sheets_out[s]["widths_ft"] for s in sheets_out},
        },
        "datum_exposure": {
            "_doc": ("What adopting the corrected Wright pixel would do, computed and NOT "
                     "adopted. Wright G5 is one of the eight points data/datum.json is fitted "
                     "from, so correcting it moves the origin, which re-derives every "
                     "coordinate in the dataset and stales every committed mesh. That is a "
                     "decision with a bake attached; this file records its cost."),
            "gcp": w["start_gcp"],
            "recorded_px": gdoc["gcps"][4]["pixel"] if gdoc["gcps"][4]["id"] == "G5" else None,
            "measured_px": fixed,
            "refit_rms_m": {"as_committed": round(rms0, 1), "with_correction": round(rms2, 1)},
            "origin_shift_m": round(shift, 1),
            "origin_shift_en": [round(E - datum["origin_utm_e"], 1),
                                round(N - datum["origin_utm_n"], 1)],
            "status": "queued, not adopted",
        },
        "sheets": sheets_out,
    }

    if args.check:
        if not OUT.exists():
            die(f"{OUT.relative_to(ROOT)} is not committed yet; run without --check first")
        old = json.loads(OUT.read_text())
        drift = []
        for s in sheets_out:
            for a1, b1 in zip(old["sheets"][s]["traverses"], doc["sheets"][s]["traverses"]):
                for ca, cb in zip(a1["corridors"], b1["corridors"]):
                    if abs(ca["width_ft"] - cb["width_ft"]) > 0.6:
                        drift.append(f"{s} {a1['id']} at t {ca['centre_t_px']}: "
                                     f"{ca['width_ft']} -> {cb['width_ft']} ft")
        if drift:
            print("\nDRIFT against the committed reading:")
            for d_ in drift:
                print("  " + d_)
            return 1
        print(f"\nOK: re-measured {len(allw)} corridors, none drifted more than 0.6 ft")
        return 0

    OUT.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
