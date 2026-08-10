#!/usr/bin/env python3
"""Trace the 1834 lake shore, the harbour reach and the sand bar off Wright 1834.

The eastern companion to `tools/trace_river.py`. That tool traces the forks; this
one traces the mile of water between the forks box and Lake Michigan — the main
stem past Fort Dearborn, the 1834 harbour cut between its piers, the decaying old
southward channel, the sand bar it runs behind, and the lake shore itself.

    python3 tools/trace_shoreline.py            re-trace and write the GeoJSON
    python3 tools/trace_shoreline.py --check    re-trace and diff against committed
    python3 tools/trace_shoreline.py --debug    also write a PNG overlay of the trace

Why this is a separate window rather than a bigger one
------------------------------------------------------
The forks trace works at a local block percentile, which is what lets it find a
70 m channel threading a town of coloured ward washes. Lake Michigan is drawn as
a wash band a couple of hundred metres wide, and against a *local* background a
band that wide is its own paper: the interior of the lake reads as unshaded and
only its two edges come out. So this trace measures "darker than paper" against
the whole window instead (`bg_block` larger than the region), which is the right
answer here and the wrong answer at the forks. Two windows, two settings, one
affine — rather than one window that does neither job well.

What comes out, and what deliberately does not
----------------------------------------------
The traced water is one connected body: main stem, cut, old channel, lake. Its
boundary is split at the window edge and each run is claimed by a hand-placed
anchor, exactly as the forks trace names its bank runs. Two runs are named:

    south_shore_harbor_reach   south bank of the main stem east of the forks box,
                               the Fort Dearborn reservation's lake shore, and the
                               west bank of the old southward channel
    north_shore_harbor_reach   north bank of the main stem, the inner face of the
                               north pier, and the lake shore north of the harbour

The sand bar comes out as what it is on the map: a hole in the water, traced as a
closed island ring and carried as the water polygon's interior ring.

**Two runs are found and dropped on purpose** — one in the north-east, one behind
the bar. Out in the lake the wash band simply stops, and that stopping line is
where the draughtsman lifted the brush: not a shore, not a depth contour, not
anything. Both are reported on every run, with their extents, and written to no
file. Nothing east of the traced shore is a claim about the lake.

Needs numpy, scipy, Pillow. Like the forks trace and the datum re-derivation this
is a deliberate, occasional re-run and is not part of tools/check.sh; it degrades
to a clear skip when the dependencies or the network are missing.
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

OUT_DIR = ROOT / "data" / "terrain" / "epochs" / "e1834_harbor_cut"
OUT = OUT_DIR / "shoreline.geojson"

IIIF = "https://iiif.digitalcommonwealth.org/iiif/2/commonwealth:js957744g"

# The region of the BPL master scan (resource space, 4204 x 5166) this trace works
# in. Its west edge is the east edge of the forks box (local E +320), so the two
# traces meet with a small overlap rather than a gap; its east edge is INSIDE the
# lake wash for most of its length, which is deliberate — where the window edge
# falls inside the wash, the split marks the boundary as window rather than
# offering it as a shore. Local extent: E +314 .. +1570, N -589 .. +505.
REGION = (1878, 1160, 1802, 1500)

# Hand-placed, like the forks trace's seeds, and the only numbers here read off
# the scan by eye. Seeds select the water; anchors claim a boundary run for a
# name. Both are resource pixels.
SEEDS = {
    "main_stem": (2400, 1700),          # open channel below the Kinzie Addition
    "old_south_channel": (3220, 2060),  # behind the bar, level with the arrow
    "lake": (3600, 1760),               # open lake east of the bar
}
ANCHORS = {
    "south_shore_harbor_reach": (3180, 1940),   # inside the reservation, by its lake shore
    "north_shore_harbor_reach": (2830, 1470),   # north bank opposite the fort
}
ANCHOR_MAX_PX = 60          # a claim further off than this is not a claim

PARAMS = dict(
    bg_block=1600, bg_pct=88,         # paper luminance, measured across the window
    hue_block=280, hue_pct=40,
    dark_lo=20, dark_hi=78,
    hue_tol=11,
    speckle_px=2000,                  # street hatching and type, dropped before closing
    pre_open_r=3,
    close_r=30, open_r=6,
    island_min_px=20000,              # smaller holes are lettering inside the channel
    simplify_px=2.5,
)


def die(msg: str, code: int = 2):
    print(msg)
    raise SystemExit(code)


def fetch_region(cache: Path):
    x, y, w, h = REGION
    url = f"{IIIF}/{x},{y},{w},{h}/full/0/default.jpg"
    if cache.exists():
        raw = cache.read_bytes()
    else:
        print(f"fetching {url}")
        with urllib.request.urlopen(url, timeout=180) as r:  # noqa: S310
            raw = r.read()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(raw)
    return raw, hashlib.sha256(raw).hexdigest()


def split_runs(ring_px, margin=3):
    """Split a traced ring into the runs that are real waterline and the runs that
    are only the edge of the traced window. Pixel space, for the same reason the
    forks trace does it in pixel space: the window is axis-aligned there and the
    local ENU frame is rotated about 1.2 degrees off it."""
    w, h = REGION[2], REGION[3]
    on_edge = [px <= margin or py <= margin or px >= w - 1 - margin or py >= h - 1 - margin
               for px, py in ring_px]
    m = len(ring_px)
    if not any(on_edge):
        return [list(range(m))]
    start = next(i for i in range(m) if on_edge[i])
    runs, cur = [], []
    for k in range(m + 1):
        i = (start + k) % m
        if on_edge[i]:
            if len(cur) > 2:
                runs.append([(cur[0] - 1) % m] + cur + [i])
            cur = []
        else:
            cur.append(i)
    return runs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="diff against the committed GeoJSON")
    ap.add_argument("--debug", action="store_true", help="write a PNG overlay of the trace")
    ap.add_argument("--cache", default=str(Path("/tmp") / "wright_1834_harbor_region.jpg"))
    args = ap.parse_args()

    try:
        import numpy as np
        from PIL import Image
        from scipy import ndimage as ndi
    except ImportError as e:
        die(f"SKIP: {e.name} not installed (pip install numpy scipy pillow); "
            f"shoreline trace not run", 0)

    import trace_river as tr                                    # noqa: PLC0415

    datum = json.loads((ROOT / "data" / "datum.json").read_text())
    if not datum.get("verified"):
        die("REFUSING: data/datum.json is not verified.")
    o_e, o_n = datum["origin_utm_e"], datum["origin_utm_n"]

    coef, rms, n_gcp = tr.affine_from_gcps()
    to_utm = tr.make_to_utm(coef)
    cell_m = 0.5 * (math.hypot(coef[0], coef[3]) + math.hypot(coef[1], coef[4]))
    print(f"affine refit from {n_gcp} GCPs, RMS {rms:.1f} m; {cell_m:.4f} m per map pixel")

    raw, sha = fetch_region(Path(args.cache))
    rgb = np.asarray(Image.open(io.BytesIO(raw)).convert("RGB"))
    print(f"region {REGION} sha256 {sha[:16]}...  {rgb.shape[1]}x{rgb.shape[0]} px")

    # --- segmentation -------------------------------------------------------
    # Same wash test as the forks, read against the window rather than a block.
    tr.PARAMS.update({k: PARAMS[k] for k in
                      ("bg_block", "bg_pct", "hue_block", "hue_pct",
                       "dark_lo", "dark_hi", "hue_tol")})
    wash = tr.wash_mask(rgb, np)
    lab, n = ndi.label(wash)
    sizes = ndi.sum_labels(np.ones_like(lab, np.float32), lab, np.arange(1, n + 1))
    wash = np.isin(lab, 1 + np.flatnonzero(sizes >= PARAMS["speckle_px"]))
    wash = ndi.binary_opening(wash, tr.disk(PARAMS["pre_open_r"], np))

    r = PARAMS["close_r"]
    m = tr._erode(ndi.binary_dilation(wash, tr.disk(r, np)), r, np, ndi)
    m = ndi.binary_dilation(tr._erode(m, PARAMS["open_r"], np, ndi),
                            tr.disk(PARAMS["open_r"], np))
    lab2, _ = ndi.label(m)
    keep = set()
    for name, (sx, sy) in SEEDS.items():
        v = int(lab2[sy - REGION[1], sx - REGION[0]])
        if v == 0:
            die(f"seed {name} at {sx},{sy} did not land on water — the segmentation "
                f"moved under it; fix the seed or the parameters, do not widen the "
                f"tolerance until it sticks")
        keep.add(v)
    water = np.isin(lab2, sorted(keep))

    # Islands: a hole in the water body is land the water goes round. The sand bar
    # is one. The letters of "RIVER" drawn across the channel are not, so anything
    # under the threshold is filled back in rather than published as an island.
    filled = ndi.binary_fill_holes(water)
    holes = filled & ~water
    hl, hn = ndi.label(holes)
    hs = ndi.sum_labels(np.ones_like(hl, np.float32), hl, np.arange(1, hn + 1))
    island_ids = 1 + np.flatnonzero(hs >= PARAMS["island_min_px"])
    islands = np.isin(hl, island_ids)
    water = filled & ~islands
    print(f"water {int(water.sum()):,} px of {water.size:,}; {hn} hole(s), "
          f"{len(island_ids)} island(s) kept, {hn - len(island_ids)} filled as lettering")
    if len(island_ids) != 1:
        die(f"expected exactly one island (the sand bar), found {len(island_ids)}")

    def px_to_local(pts):
        out = []
        for px, py in pts:
            E, N = to_utm(px + REGION[0], py + REGION[1])
            out.append((round(E - o_e, 2), round(N - o_n, 2)))
        return out

    def length_m(line):
        return sum(math.dist(line[i], line[i + 1]) for i in range(len(line) - 1))

    # --- the shore ----------------------------------------------------------
    ring_px = tr.simplify_ring(tr.trace_outer(water, np), PARAMS["simplify_px"])
    runs_px = split_runs(ring_px)
    named, dropped = {}, []
    for idx in runs_px:
        pts = [ring_px[i] for i in idx]
        best, bestd = None, 1e18
        for key, (ax, ay) in ANCHORS.items():
            d = min(math.hypot(px + REGION[0] - ax, py + REGION[1] - ay) for px, py in pts)
            if d < bestd:
                best, bestd = key, d
        line = px_to_local(pts)
        if bestd > ANCHOR_MAX_PX or best in named:
            dropped.append((line, round(bestd * cell_m, 1)))
            continue
        named[best] = (line, round(bestd * cell_m, 1))
    for key in ANCHORS:
        if key not in named:
            die(f"no boundary run came within {ANCHOR_MAX_PX} px of the {key} anchor")
    for line, d in dropped:
        print(f"   dropped run: {len(line)} pts, {length_m(line):.0f} m, "
              f"E [{min(p[0] for p in line):.0f},{max(p[0] for p in line):.0f}] "
              f"N [{min(p[1] for p in line):.0f},{max(p[1] for p in line):.0f}], "
              f"nearest anchor {d} m away — no anchor claims it, so it is not written")

    bar_px = tr.simplify_ring(tr.trace_outer(islands, np), PARAMS["simplify_px"])
    bar = px_to_local(bar_px)
    print(f"shore runs: " + ", ".join(f"{k} {len(v[0])} pts / {length_m(v[0]):.0f} m"
                                      for k, v in named.items()))
    print(f"sand bar ring {len(bar)} vertices, {length_m(bar + [bar[0]]):.0f} m perimeter")

    water_px = tr.simplify_ring(tr.trace_outer(water, np), PARAMS["simplify_px"])
    water_ring = px_to_local(water_px)

    def closed(ring):
        return [[e + o_e, n + o_n] for e, n in ring] + [[ring[0][0] + o_e, ring[0][1] + o_n]]

    prov = {
        "traced_from": "wright_1834",
        "method": "grey wash segmentation of the BPL master scan measured against the whole "
                  "window rather than a local block (the lake wash band is wider than any "
                  "local background); water selected from three hand-placed seeds, boundary "
                  "traced and simplified, runs claimed by hand-placed anchors; pixels "
                  "transformed to EPSG:26916 by the least-squares affine refit from "
                  "data/traces/gcp/wright_1834_gcps.json — the same transform that fixed "
                  "the datum and traced the forks",
        "tool": "tools/trace_shoreline.py",
        "iiif_region": {"image": IIIF, "x": REGION[0], "y": REGION[1],
                        "w": REGION[2], "h": REGION[3], "sha256": sha},
        "affine_rms_m": round(rms, 1),
        "map_scale_m_per_px": round(cell_m, 4),
        "simplify_tolerance_m": round(PARAMS["simplify_px"] * cell_m, 2),
        "uncertainty_m": 20,
        "uncertainty_note": "As the forks: both 1834 sheets carry real anisotropic paper "
                            "stretch, so a global affine cannot do better than tens of metres "
                            "locally. Treat every vertex as +/-20 m. See "
                            "docs/RESEARCH/datum_derivation.md.",
        "not_traced": "The outer edge of the lake wash band is where the draughtsman stopped "
                      "washing, not a feature. It is found, reported and dropped. Nothing in "
                      "this file describes the lake east of the traced shore, and the water "
                      "polygon's eastern boundary is the window, not a shore.",
    }

    features = [
        {
            "type": "Feature",
            "id": "harbor_reach_water",
            "geometry": {"type": "Polygon",
                         "coordinates": [closed(water_ring), closed(bar)]},
            "properties": {
                "kind": "water",
                "name": "Chicago River harbour reach, the 1834 cut, the old southward "
                        "channel and the lake margin",
                "water_surface_ft_above_datum": 0.0,
                "confidence": "inferred",
                "note": "Planform traced from the Wright 1834 survey; one connected body of "
                        "water from the east edge of the forks box to the lake. The water "
                        "surface is flat at the datum because the pre-reversal river stood at "
                        "lake level through the whole downtown reach. The interior ring is "
                        "the sand bar. The EASTERN boundary of this polygon is the traced "
                        "window, not a shore — see provenance.not_traced.",
                "sources": ["wright_1834", "wikipedia_chicago_river"],
                "provenance": prov,
            },
        },
        {
            "type": "Feature",
            "id": "sand_bar_1834",
            "geometry": {"type": "Polygon", "coordinates": [closed(bar)]},
            "properties": {
                "kind": "bar",
                "name": "The sand bar across the river mouth",
                "confidence": "inferred",
                "note": "Land, not water: the bar Wright labels SAND-BAR, traced as the island "
                        "the water goes round. Its planform is drafted on a cadastral plat, so "
                        "the same +/-20 m applies and the same 'inferred' the river polygon "
                        "carries. NO ELEVATION IS CLAIMED HERE — a bar is a surface a few feet "
                        "of lake stage moves, no source gives its height, and the terrain spec "
                        "is where any such number would have to be argued for. Wright shows it "
                        "already cut through by the 1834 harbour works, with the old southward "
                        "channel behind it drawn narrowing and its arrow still running south.",
                "sources": ["wright_1834"],
                "provenance": prov,
            },
        },
    ]

    labels = {
        "south_shore_harbor_reach": (
            "South shore of the harbour reach: south bank of the main stem east of the forks "
            "box, the Fort Dearborn reservation's lake shore, and the west bank of the old "
            "southward channel behind the bar",
            "Continuous from the forks box eastward: the same waterline the forks trace ends "
            "on, picked up again at local E +314. Beyond about N -580 it leaves the traced "
            "window; the shore and the old channel continue south of there and are not traced.",
        ),
        "north_shore_harbor_reach": (
            "North shore of the harbour reach: north bank of the main stem, the inner face of "
            "the north pier, and the lake shore north of the harbour",
            "BETWEEN THE PIERS THIS IS NOT A NATURAL SHORE. Wright draws the 1834 cut as a "
            "straight channel between two pier lines, and the traced boundary there follows "
            "the pier's inner face as drafted. The piers are structures with phases (see "
            "docs/EPOCHS.md), so they are not modelled here and their alignment is not a "
            "terrain claim; this run says only where the drawn water ended.",
        ),
    }
    for key, (line, anchor_m) in named.items():
        name, note = labels[key]
        features.append({
            "type": "Feature",
            "id": key,
            "geometry": {"type": "LineString",
                         "coordinates": [[e + o_e, n + o_n] for e, n in line]},
            "properties": {
                "kind": "shore",
                "name": name,
                "crest_ft_above_datum": None,
                "confidence": "inferred",
                "note": note + " Crest heights are carried in the terrain spec, not here: they "
                                "come from narrative feet, not from the map.",
                "length_m": round(length_m(line), 1),
                "anchor_distance_m": anchor_m,
                "sources": ["wright_1834"],
            },
        })

    fc = {
        "type": "FeatureCollection",
        "name": "e1834_harbor_cut shoreline",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::26916"}},
        "_doc": "The lake shore, the harbour reach, the 1834 cut and the sand bar for terrain "
                "epoch e1834_harbor_cut — everything between the east edge of the forks box "
                "and Lake Michigan. Coordinates are EPSG:26916 metres (UTM 16N, NAD83); local "
                "ENU metres used by the scene are these minus data/datum.json origin_utm_e / "
                "origin_utm_n. Generated by tools/trace_shoreline.py — do not hand-edit. NOT "
                "YET CONSUMED by generators/terrain_gen.py: the terrain box still stops at "
                "local E +320 and extending it is the next slice of ROADMAP S2e, which needs "
                "a bake. Until then this file is the evidence, not the ground.",
        "features": features,
    }

    text = json.dumps(fc, indent=1) + "\n"
    if args.check:
        old = OUT.read_text() if OUT.exists() else ""
        same = old == text
        print(f"{'OK  ' if same else 'DIFF'} {OUT.relative_to(ROOT)}")
        if not same:
            return 1
    else:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text)
        print(f"wrote {OUT.relative_to(ROOT)} ({len(text):,} bytes)")

    if args.debug:
        over = rgb.copy()
        over[water] = (0.72 * over[water] + np.array([0, 90, 240]) * 0.28).astype(np.uint8)
        over[islands] = (0.72 * over[islands] + np.array([240, 170, 0]) * 0.28).astype(np.uint8)
        for px, py in bar_px:
            over[max(0, py - 3):py + 4, max(0, px - 3):px + 4] = (255, 140, 0)
        for key, (ax, ay) in ANCHORS.items():
            over[ay - REGION[1] - 5:ay - REGION[1] + 6,
                 ax - REGION[0] - 5:ax - REGION[0] + 6] = (0, 0, 0)
        for j, idx in enumerate(runs_px):
            col = [(200, 0, 0), (140, 0, 220), (0, 150, 0), (0, 0, 0)][j % 4]
            for i in idx:
                px, py = ring_px[i]
                over[max(0, py - 3):py + 4, max(0, px - 3):px + 4] = col
        p = Path("/tmp") / "shoreline_trace_debug.png"
        Image.fromarray(over).save(p)
        print("debug overlay", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
