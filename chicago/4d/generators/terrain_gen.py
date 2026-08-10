"""Terrain for one epoch: spec + traced vectors -> heightfield + GLB.

    # heightfield only (no Blender needed — numpy is the one dependency)
    python3 generators/terrain_gen.py --epoch e1834_harbor_cut

    # heightfield AND the terrain / water GLBs
    blender -b -noaudio --factory-startup --python generators/terrain_gen.py -- --glb

Inputs, all committed:

    data/datum.json                                   origin and vertical datum
    data/terrain/epochs/<e>/terrain_spec.json         the authored zone table
    data/terrain/epochs/<e>/river.geojson             traced water polygon + bank runs
    data/terrain/epochs/<e>/hydrology.geojson         traced secondary watercourses

Outputs:

    data/terrain/epochs/<e>/heightfield.json          runtime meta (what the renderer reads)
    data/terrain/epochs/<e>/heightfield.bin           int16 samples, row 0 = SOUTH
    assets/gltf/terrain__<e>.glb                      the ground
    assets/gltf/water__<e>.glb                        the water surface
    assets/manifest.json                              input hashes for the staleness gate

How the surface is built, and why it is built this way
------------------------------------------------------
Everything hangs off ONE geometric quantity: the signed distance from the traced
waterline. Land elevation is a function of distance inland; channel depth is a
function of distance offshore; both are zero at the waterline, so the ground
surface crosses Z = 0 exactly along the line traced off the Wright 1834 survey
and the water plane needs no separate shoreline geometry — it is simply the
plane Z = 0, and the terrain occludes it wherever the terrain is above it.

Land is assigned to a DIVISION by which of the three traced bank runs it is
nearest to. That is not a convenience: the North, South and West Divisions were
*defined* by the river, so deriving them from the river rather than drawing
three polygons by hand keeps the zone boundaries honest and keeps them correct
if the trace is ever refit.

Refuses to run while data/datum.json is unverified, for the same reason
generators/build.py does.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FT = 0.3048

try:
    import numpy as np
except ImportError:                                   # pragma: no cover
    np = None

try:
    import bpy                                        # noqa: F401
    HAVE_BPY = True
except ImportError:
    HAVE_BPY = False

# Confidence channel, docs/GLB-CONTRACT.md. Least confident wins.
CONF_DOCUMENTED, CONF_INFERRED, CONF_CONJECTURAL = 0.0, 0.5, 1.0

# The skirt carries the terrain's own edge heights outward so the river does not
# end in mid-air at the box boundary and the horizon is ground rather than void.
SKIRT_HALF_M = 1400.0
WATER_HALF_M = 1200.0

# How far the decimated ground mesh may depart from the heightfield the walker
# samples. 30 mm is well under the resolution of anything a person notices on
# foot and two orders under the relief being modelled.
MESH_FIT_TOLERANCE_M = 0.03


def _unbuffer():
    """Blender block-buffers the script's stdout, so a crash loses every print
    that would have told you where it crashed. Line-buffer it."""
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:  # noqa: BLE001
        pass


def argv_after_ddash() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def load(p: Path):
    return json.loads(p.read_text())


# ---------------------------------------------------------------------------
# vector helpers — exact distances, no rasterised approximations
# ---------------------------------------------------------------------------

def seg_distance(E, N, pts):
    """Distance from every grid point to a polyline, exactly. `pts` is a list of
    (e, n). Vectorised over the grid, looped over the (few dozen) segments."""
    best = np.full(E.shape, np.inf, np.float64)
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        if L2 < 1e-12:
            d = np.hypot(E - ax, N - ay)
        else:
            t = np.clip(((E - ax) * dx + (N - ay) * dy) / L2, 0.0, 1.0)
            d = np.hypot(E - (ax + t * dx), N - (ay + t * dy))
        np.minimum(best, d, out=best)
    return best


def point_in_ring(E, N, ring):
    """Crossing-number point-in-polygon, vectorised over the grid."""
    inside = np.zeros(E.shape, bool)
    n = len(ring)
    for i in range(n):
        ax, ay = ring[i - 1]
        bx, by = ring[i]
        if ay == by:
            continue
        cond = (ay > N) != (by > N)
        with np.errstate(divide="ignore", invalid="ignore"):
            xint = (bx - ax) * (N - ay) / (by - ay) + ax
        inside ^= cond & (E < xint)
    return inside


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def value_noise(E, N, wavelength, seed):
    """Two-dimensional value noise with smoothstep interpolation. Deterministic
    from `seed`; no dependency on any RNG's stream order."""
    gx = E / wavelength
    gy = N / wavelength
    x0 = np.floor(gx).astype(np.int64)
    y0 = np.floor(gy).astype(np.int64)
    fx, fy = gx - x0, gy - y0

    def h(ix, iy):
        k = (ix * np.int64(374761393) + iy * np.int64(668265263)
             + np.int64(seed) * np.int64(2246822519))
        k = (k ^ (k >> np.int64(13))) * np.int64(1274126177)
        k = k ^ (k >> np.int64(16))
        return (k & np.int64(0xFFFFFF)) / float(0xFFFFFF)

    sx, sy = smoothstep(fx), smoothstep(fy)
    a = h(x0, y0) * (1 - sx) + h(x0 + 1, y0) * sx
    b = h(x0, y0 + 1) * (1 - sx) + h(x0 + 1, y0 + 1) * sx
    return (a * (1 - sy) + b * sy) * 2.0 - 1.0


# ---------------------------------------------------------------------------
# the field
# ---------------------------------------------------------------------------

def build_field(spec, river, hydro, origin):
    """Returns (h_m, conf, water_mask, meta) on the spec's grid.

    h_m[row][col], row 0 = SOUTH edge, col 0 = WEST edge — the layout
    renderers/web/js/terrain.js's Heightfield sampler requires.
    """
    o_e, o_n = origin
    g = spec["grid"]
    half, cell = float(g["half_extent_m"]), float(g["cell_m"])
    n = int(round(2 * half / cell)) + 1
    axis = -half + cell * np.arange(n)
    E, N = np.meshgrid(axis, axis)                    # E varies along columns

    def to_local(coords):
        return [(c[0] - o_e, c[1] - o_n) for c in coords]

    feats = {f["id"]: f for f in river["features"]}
    ring = to_local(feats["chicago_river_forks"]["geometry"]["coordinates"][0])[:-1]
    runs = {d["bank_run"]: to_local(feats[d["bank_run"]]["geometry"]["coordinates"])
            for d in spec["divisions"]}

    # ---- distance to the waterline, signed -------------------------------
    d_ring = seg_distance(E, N, ring + [ring[0]])
    in_ring = point_in_ring(E, N, ring)

    # ---- the north-side slough, buffered off its traced centreline -------
    slough_feat = next((f for f in hydro["features"] if f["id"] == "north_side_slough"), None)
    wc = {w["id"]: w for w in spec.get("watercourses", [])}
    if slough_feat is not None:
        line = to_local(slough_feat["geometry"]["coordinates"])
        s_half = 0.5 * float(slough_feat["properties"]["drafted_width_m"])
        d_slough = seg_distance(E, N, line)
        in_slough = d_slough < s_half
        slough_bed = float(wc["north_side_slough"]["bed_ft"])
        slough_efold = float(wc["north_side_slough"].get("e_fold_m", 9.0))
    else:
        d_slough = np.full(E.shape, 1e9)
        in_slough = np.zeros(E.shape, bool)
        s_half, slough_bed, slough_efold = 0.0, 0.0, 9.0

    water = in_ring | in_slough
    # distance INTO the water from the nearest waterline, and distance INLAND
    d_in = np.where(in_ring, d_ring, 0.0)
    d_in = np.maximum(d_in, np.where(in_slough, s_half - d_slough, 0.0))
    d_land = np.minimum(np.where(in_ring, 1e9, d_ring),
                        np.where(in_slough, 1e9, d_slough - s_half))
    d_land = np.maximum(d_land, 0.0)

    # ---- channel bed: inverse-distance blend of the reach beds -----------
    wsum = np.zeros(E.shape)
    bsum = np.zeros(E.shape)
    for r in spec["reaches"]:
        dd = np.maximum(np.hypot(E - r["anchor_e"], N - r["anchor_n"]), 1.0)
        w = 1.0 / (dd * dd)
        wsum += w
        bsum += w * float(r["bed_ft"])
    bed_ft = bsum / wsum
    bed_ft = np.where(in_slough & ~in_ring, slough_bed, bed_ft)
    efold = np.where(in_slough & ~in_ring, slough_efold,
                     float(spec["channel_profile"]["e_fold_m"]))
    depth_ft = bed_ft * (1.0 - np.exp(-d_in / efold))

    # ---- which division is this land in ----------------------------------
    run_ids = list(runs)
    dists = np.stack([seg_distance(E, N, runs[k]) for k in run_ids])
    nearest = np.argmin(dists, axis=0)

    level_ft = np.zeros(E.shape)
    for i, run_id in enumerate(run_ids):
        div = next(d for d in spec["divisions"] if d["bank_run"] == run_id)
        near, far = float(div["near_ft"]), float(div["far_ft"])
        lv = near + (far - near) * np.clip(d_land / float(div["far_m"]), 0.0, 1.0)
        for m in spec.get("marsh_strips", []):
            if m["applies_to"] != div["id"]:
                continue
            w_m, b_m = float(m["width_m"]), float(m["blend_m"])
            wgt = 1.0 - smoothstep((d_land - (w_m - b_m)) / b_m)
            lv = lv * (1.0 - wgt) + float(m["level_ft"]) * wgt
        level_ft = np.where(nearest == i, lv, level_ft)

    # ---- swales in the west prairie --------------------------------------
    conj_land = np.zeros(E.shape, bool)
    for s in spec.get("swales", []):
        dd = seg_distance(E, N, [tuple(p) for p in s["line"]])
        hw = float(s["half_width_m"])
        prof = np.clip(1.0 - (dd / hw) ** 2, 0.0, 1.0)
        level_ft = level_ft - float(s["depth_ft"]) * prof
        conj_land |= prof > 0.01

    # ---- micro-relief -----------------------------------------------------
    mr = spec.get("micro_relief", {})
    amp = float(mr.get("amplitude_ft", 0.0))
    micro = np.zeros(E.shape)
    if amp > 0:
        waves = mr.get("wavelengths_m", [50.0])
        seed = int(mr.get("seed", 1))
        for k, wl in enumerate(waves):
            micro += value_noise(E, N, float(wl), seed + 977 * k) / (k + 1)
        micro *= amp / max(1e-9, sum(1.0 / (k + 1) for k in range(len(waves))))

    # ---- assemble ---------------------------------------------------------
    # The bank ramp is an ease-OUT (steepest at the waterline, flattening into
    # the plain), not a smoothstep. Two reasons, and the second is the one that
    # matters. Physically, a natural bank in alluvium is undercut by the flow and
    # is steepest right at the water. Numerically, a smoothstep leaves the ground
    # almost exactly flat for the first metre inland, so the surface's Z = 0
    # contour — which IS the drawn waterline, since the water is the plane Z = 0 —
    # is badly conditioned and snaps to cell boundaries. An ease-out crosses zero
    # with a definite slope and the shoreline comes out crisp.
    face = float(spec["bank"]["face_m"])
    t_bank = np.clip(d_land / face, 0.0, 1.0)
    ramp = 1.0 - (1.0 - t_bank) ** 2
    h_ft = np.where(water, depth_ft, (level_ft + micro) * ramp)

    conf = np.where(water, CONF_CONJECTURAL, CONF_INFERRED)
    conf = np.where(conj_land & ~water, CONF_CONJECTURAL, conf)

    meta = {
        "cols": n, "rows": n, "cell_m": cell,
        "origin_e": -half, "origin_n": -half,
        "min_m": float((h_ft * FT).min()), "max_m": float((h_ft * FT).max()),
        "water_fraction": float(water.mean()),
        "land_min_ft": float(h_ft[~water].min()), "land_max_ft": float(h_ft[~water].max()),
    }
    return h_ft * FT, conf, water, meta, {"E": E, "N": N, "d_land": d_land,
                                          "swale": conj_land, "cell": cell}


# ---------------------------------------------------------------------------
# gradient audit — the dossier's own flatness rule, checked rather than claimed
# ---------------------------------------------------------------------------

def gradient_audit(h_m, water, geom, spec):
    """Check, rather than claim, the dossier's own flatness rule: outside the
    zones that earn relief, hold local gradients under 0.5 ft per 300 ft.

    The zones that DO earn relief here — and are therefore reported separately
    rather than excused — are the bank faces, the marshy shore strip and its
    blend into the plain, and the west-prairie swales.
    """
    cell = geom["cell"]
    # The rule is about the FALL ACROSS A 300-FT BLOCK — the drainage grade of
    # the plain — not about the cell-to-cell derivative, which on any real
    # ground is dominated by surface texture. So the baseline is a 300 ft
    # (91.44 m) chord, and the sub-block roughness is reported separately
    # instead of being smuggled into the same number.
    k = max(1, int(round(300.0 * FT / cell)))
    shore_m = max(2.5 * float(spec["bank"]["face_m"]),
                  max((float(m["width_m"]) + float(m["blend_m"])
                       for m in spec.get("marsh_strips", [])), default=0.0))
    ok = (~water) & (geom["d_land"] >= shore_m) & (~geom["swale"])

    de = (h_m[:, k:] - h_m[:, :-k]) / FT
    dn = (h_m[k:, :] - h_m[:-k, :]) / FT
    ve = ok[:, k:] & ok[:, :-k]
    vn = ok[k:, :] & ok[:-k, :]
    block = np.concatenate([np.abs(de[ve]), np.abs(dn[vn])]) if (ve.any() or vn.any()) \
        else np.zeros(1)

    gy, gx = np.gradient(h_m, cell)
    rough = (np.hypot(gx, gy) * 300.0)[ok] if ok.any() else np.zeros(1)
    relief = (~water) & ~ok
    rel = (np.hypot(gx, gy) * 300.0)[relief] if relief.any() else np.zeros(1)

    return {
        "baseline_ft": 300.0,
        "shore_and_swale_exclusion_m": round(shore_m, 1),
        "plain_block_max": round(float(block.max()), 3),
        "plain_block_mean": round(float(block.mean()), 4),
        "passes": bool(block.max() <= 0.5),
        "plain_cell_roughness_max": round(float(rough.max()), 3),
        "shore_and_swale_cell_max": round(float(rel.max()), 3),
    }


# ---------------------------------------------------------------------------
# writing
# ---------------------------------------------------------------------------

def write_heightfield(out_dir: Path, h_m, meta, spec, inputs_sha: str):
    scale = float(spec["grid"]["scale_m"])
    q = np.rint(h_m / scale).astype(np.int16)
    err = float(np.abs(q.astype(np.float64) * scale - h_m).max())
    (out_dir / "heightfield.bin").write_bytes(q.tobytes(order="C"))

    doc = {
        "_doc": "Runtime heightfield meta for terrain epoch e1834_harbor_cut. Row 0 is the "
                "SOUTH edge and column 0 the WEST edge; the sample at [0][0] sits exactly on "
                "(origin_e, origin_n) in local ENU metres from data/datum.json. Elevation in "
                "metres above the summer-1835 water surface: y = raw * scale + offset. "
                "GENERATED by generators/terrain_gen.py — do not hand-edit.",
        "epoch": spec["epoch"],
        "spec": "terrain_spec.json",
        "bin": "heightfield.bin",
        "encoding": "int16",
        "scale": scale,
        "offset": 0.0,
        "cols": meta["cols"], "rows": meta["rows"],
        "cell_m": meta["cell_m"],
        "origin_e": meta["origin_e"], "origin_n": meta["origin_n"],
        "min_m": round(meta["min_m"], 4), "max_m": round(meta["max_m"], 4),
        "quantisation_error_m": round(err, 5),
        "water_surface_m": 0.0,
        "water_fraction": round(meta["water_fraction"], 4),
        "relief_ft": {
            "land_min": round(meta["land_min_ft"], 3),
            "land_max": round(meta["land_max_ft"], 3),
            "channel_min": round(meta["min_m"] / FT, 3),
        },
        "gradient_audit_ft_per_300ft": meta.get("gradient_audit"),
        "glb": {
            "ground": f"gltf/terrain__{spec['epoch']}.glb",
            "water": f"gltf/water__{spec['epoch']}.glb",
        },
        "inputs_sha256": inputs_sha,
    }
    (out_dir / "heightfield.json").write_text(json.dumps(doc, indent=1) + "\n")
    return doc


def inputs_hash(paths) -> str:
    h = hashlib.sha256()
    for p in paths:
        h.update(Path(p).read_bytes())
    return h.hexdigest()


def terrain_inputs_sha(ep_dir: Path) -> str:
    """Everything that determines this epoch's ground and water meshes.

    One definition, called both by the bake that writes `inputs_sha256` into
    `assets/manifest.json` and by `tools/validate.py`, which recomputes it to
    decide whether the committed GLB still matches its inputs. Two copies of this
    list would agree until the day one of them mattered.

    `shoreline.geojson` is deliberately absent: it is traced evidence that
    `build_field` does not yet read, so including it would report the ground as
    stale for a file that cannot change it. It joins the list the moment the
    heightfield consumes it (ROADMAP § S2e parcel b).

    Nothing here imports bpy — the meshing does, this does not.
    """
    return inputs_hash([ep_dir / "terrain_spec.json", ep_dir / "river.geojson",
                        ep_dir / "hydrology.geojson", ROOT / "data" / "datum.json",
                        Path(__file__)])


# ---------------------------------------------------------------------------
# meshing (bpy)
# ---------------------------------------------------------------------------

def build_meshes(h_m, conf, spec, epoch, outdir: Path, decimate_deg: float):
    from math import radians

    from common.mesh import reset_scene, simple_material  # noqa: PLC0415

    g = spec["grid"]
    half, cell = float(g["half_extent_m"]), float(g["cell_m"])
    rows, cols = h_m.shape

    def enu_to_blender(e, n, y):
        # glTF export runs with export_yup=True, which maps Blender +Z to glTF
        # +Y and Blender +Y to glTF -Z. So authoring (E, N, up) as Blender
        # (x=E, y=N, z=up) lands as glTF (x=E, y=up, z=-N) — exactly the ENU
        # convention docs/GLB-CONTRACT.md pins.
        return (e, n, y)

    results = []

    # ---- ground -----------------------------------------------------------
    reset_scene()
    verts, confs = [], []
    for r in range(rows):
        n = -half + r * cell
        for c in range(cols):
            verts.append(enu_to_blender(-half + c * cell, n, float(h_m[r, c])))
            confs.append(float(conf[r, c]))
    faces = []
    for r in range(rows - 1):
        base = r * cols
        for c in range(cols - 1):
            i = base + c
            faces.append((i, i + 1, i + 1 + cols, i + cols))

    # skirt: carry each boundary vertex outward to a larger square, keeping its
    # own height, so the channel continues past the box instead of stopping
    k = SKIRT_HALF_M / half
    # Clockwise seen from above, each corner listed exactly once — a repeated
    # index here produces a degenerate quad, which from_pydata accepts and the
    # decimate modifier then segfaults on.
    ring_idx = ([r * cols for r in range(rows)]                              # west, S->N
                + [(rows - 1) * cols + c for c in range(1, cols)]            # north, W->E
                + [r * cols + cols - 1 for r in range(rows - 2, -1, -1)]     # east, N->S
                + [c for c in range(cols - 2, 0, -1)])                       # south, E->W
    assert len(set(ring_idx)) == len(ring_idx), "skirt ring visits a vertex twice"
    outer = {}
    for i in ring_idx:
        e, n, y = verts[i]
        outer[i] = len(verts)
        verts.append((e * k, n * k, y))
        confs.append(confs[i])
    # Wound so the skirt's normal points up, matching the grid above it: the
    # boundary runs clockwise from above, so the quad is a -> b -> outer_b ->
    # outer_a, not the other way round.
    for a, b in zip(ring_idx, ring_idx[1:] + ring_idx[:1]):
        faces.append((a, b, outer[b], outer[a]))

    ground = _emit(f"terrain__{epoch}", verts, faces, confs,
                   simple_material("terrain_ground", (0.36, 0.35, 0.22, 1.0), 1.0),
                   {"terrain_epoch": epoch, "layer": "ground"}, decimate_deg)
    fit = mesh_vs_field(ground, h_m, spec)
    print(f"ground mesh vs heightfield: max {fit['max_m'] * 1000:.0f} mm, "
          f"rms {fit['rms_m'] * 1000:.1f} mm over {fit['samples']:,} rays "
          f"({fit['misses']} misses)")
    if fit["max_m"] > MESH_FIT_TOLERANCE_M:
        raise SystemExit(
            f"REFUSING: the decimated ground mesh departs from the heightfield by "
            f"{fit['max_m'] * 1000:.0f} mm, over the {MESH_FIT_TOLERANCE_M * 1000:.0f} mm "
            f"tolerance. The walker's eye is pinned to the heightfield, so it would visibly "
            f"float or sink. Lower --decimate-deg.")
    ground_res = _export(ground, outdir / f"terrain__{epoch}.glb")
    ground_res["fit"] = fit
    results.append(ground_res)

    # ---- water ------------------------------------------------------------
    reset_scene()
    w = WATER_HALF_M
    wv = [(-w, -w, 0.0), (w, -w, 0.0), (w, w, 0.0), (-w, w, 0.0)]
    water = _emit(f"water__{epoch}", wv, [(0, 1, 2, 3)], [CONF_DOCUMENTED] * 4,
                  simple_material("terrain_water", (0.18, 0.24, 0.24, 1.0), 0.15),
                  {"terrain_epoch": epoch, "layer": "water"}, 0.0)
    results.append(_export(water, outdir / f"water__{epoch}.glb"))
    return results


def _emit(name, verts, faces, confs, material, extras, decimate_deg):
    import bpy  # noqa: PLC0415

    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if me.validate(verbose=False):
        raise SystemExit(f"{name}: mesh failed validation — degenerate or duplicate faces")
    attr = me.attributes.new(name="_CONFIDENCE", type="FLOAT", domain="POINT")
    attr.data.foreach_set("value", confs)
    me.materials.append(material)
    for poly in me.polygons:
        poly.use_smooth = True

    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    for k, v in extras.items():
        ob[k] = v

    bpy.context.view_layer.objects.active = ob
    if decimate_deg > 0:
        mod = ob.modifiers.new("planar", "DECIMATE")
        mod.decimate_type = "DISSOLVE"
        mod.angle_limit = math.radians(decimate_deg)
        mod.delimit = {"NORMAL"}
        bpy.ops.object.modifier_apply(modifier=mod.name)
    tri = ob.modifiers.new("tri", "TRIANGULATE")
    tri.min_vertices = 4
    bpy.ops.object.modifier_apply(modifier=tri.name)
    return ob


def mesh_vs_field(ob, h_m, spec, stride=3):
    """Measure the ground mesh against the heightfield the WALKER samples.

    They are generated from the same grid, but the planar-dissolve pass that
    keeps the triangle count down is free to flatten anything whose face-pair
    angle is under the limit, and nothing about that bounds the accumulated
    error across a merged region. So it gets measured rather than argued about:
    a visitor whose eye is pinned to a heightfield the mesh does not match will
    see themselves float or sink, and that is exactly the failure this project
    should not ship.
    """
    from mathutils import Vector  # noqa: PLC0415
    from mathutils.bvhtree import BVHTree  # noqa: PLC0415

    bvh = BVHTree.FromObject(ob, bpy.context.evaluated_depsgraph_get())
    g = spec["grid"]
    half, cell = float(g["half_extent_m"]), float(g["cell_m"])
    rows, cols = h_m.shape
    down = Vector((0, 0, -1))
    worst, sq, n_hit, n_miss = 0.0, 0.0, 0, 0
    for r in range(0, rows, stride):
        n = -half + r * cell
        for c in range(0, cols, stride):
            e = -half + c * cell
            hit = bvh.ray_cast(Vector((e, n, 60.0)), down)
            if hit[0] is None:
                n_miss += 1
                continue
            d = abs(hit[0].z - float(h_m[r, c]))
            worst = max(worst, d)
            sq += d * d
            n_hit += 1
    rms = math.sqrt(sq / n_hit) if n_hit else 0.0
    return {"samples": n_hit, "misses": n_miss,
            "max_m": round(worst, 4), "rms_m": round(rms, 5)}


def _export(ob, out: Path):
    import bpy  # noqa: PLC0415

    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.export_scene.gltf(
        filepath=str(out), export_format="GLB", use_selection=True,
        export_yup=True, export_apply=True,
        export_attributes=True, export_extras=True,
        export_cameras=False, export_lights=False, export_normals=True,
    )
    tris = len(ob.data.polygons)
    print(f"built {out.name}  {out.stat().st_size:,} bytes  {tris:,} tris  "
          f"{len(ob.data.vertices):,} verts")
    return {"path": out, "tris": tris, "verts": len(ob.data.vertices)}


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--epoch", default="e1834_harbor_cut")
    ap.add_argument("--glb", action="store_true", help="also build the GLBs (needs Blender)")
    ap.add_argument("--decimate-deg", type=float, default=0.04,
                    help="planar-dissolve angle limit for the ground mesh; 0 disables. "
                         "0.04 deg was picked by measurement, not taste: it is the loosest "
                         "limit whose mesh still tracks the heightfield inside "
                         "MESH_FIT_TOLERANCE_M (16 mm max, 3 mm rms), and it throws away "
                         "two thirds of the triangles a plain grid would carry.")
    ap.add_argument("--out", default=str(ROOT / "assets" / "gltf"))
    args = ap.parse_args(argv_after_ddash())
    _unbuffer()

    if np is None:
        print("REFUSING: numpy is required (pip install numpy). Blender ships it.")
        return 2

    datum = load(ROOT / "data" / "datum.json")
    if not datum.get("verified"):
        print("REFUSING TO BUILD: data/datum.json is not verified.\n"
              "Fixing the origin after geometry exists means regenerating everything.\n"
              "See docs/EPOCHS.md and docs/RESEARCH/datum_derivation.md.")
        return 2

    ep_dir = ROOT / "data" / "terrain" / "epochs" / args.epoch
    spec = load(ep_dir / "terrain_spec.json")
    river = load(ep_dir / "river.geojson")
    hydro = load(ep_dir / "hydrology.geojson")
    origin = (datum["origin_utm_e"], datum["origin_utm_n"])

    h_m, conf, water, meta, geom = build_field(spec, river, hydro, origin)
    audit = gradient_audit(h_m, water, geom, spec)
    audit["rule"] = ("docs/research/01-terrain-hydrology.md modelling rule 1: outside the zones "
                     "that earn relief, hold local gradients under 0.5 ft per 300 ft")
    meta["gradient_audit"] = audit

    sha = terrain_inputs_sha(ep_dir)
    doc = write_heightfield(ep_dir, h_m, meta, spec, sha)

    print(f"grid {doc['cols']}x{doc['rows']} @ {doc['cell_m']} m  "
          f"({2 * float(spec['grid']['half_extent_m']):.0f} m square)")
    print(f"relief: land {meta['land_min_ft']:+.2f} .. {meta['land_max_ft']:+.2f} ft, "
          f"channel floor {meta['min_m'] / FT:+.2f} ft; water covers "
          f"{100 * meta['water_fraction']:.1f}% of the box")
    print(f"quantisation error {doc['quantisation_error_m'] * 1000:.2f} mm "
          f"(dossier asks for <= 0.25 ft = 76 mm)")
    ga = meta["gradient_audit"]
    print(f"gradient audit (fall across a 300 ft chord): plain max {ga['plain_block_max']} ft "
          f"(mean {ga['plain_block_mean']}) — {'PASS' if ga['passes'] else 'OVER THE 0.5 RULE'}; "
          f"plain cell roughness {ga['plain_cell_roughness_max']}, "
          f"shore and swales {ga['shore_and_swale_cell_max']}")
    print(f"wrote {(ep_dir / 'heightfield.bin').relative_to(ROOT)} "
          f"({(ep_dir / 'heightfield.bin').stat().st_size:,} bytes)")

    if not args.glb:
        print("\nheightfield only; re-run under Blender with --glb for the meshes")
        return 0
    if not HAVE_BPY:
        print("\n--glb asked for but bpy is not importable. Run:\n"
              "  blender -b -noaudio --factory-startup --python generators/terrain_gen.py "
              "-- --glb")
        return 2

    sys.path.insert(0, str(ROOT / "generators"))
    built = build_meshes(h_m, conf, spec, args.epoch, Path(args.out), args.decimate_deg)

    manifest_path = ROOT / "assets" / "manifest.json"
    manifest = load(manifest_path) if manifest_path.exists() else {}
    manifest.setdefault("assets", {})
    manifest["blender"] = bpy.app.version_string.split()[0]
    # Terrain and structures share one manifest and therefore one declaration of
    # what its hashes mean; see generators/mesh_inputs.py.
    sys.path.insert(0, str(ROOT / "generators"))
    from mesh_inputs import SCHEME  # noqa: PLC0415

    manifest["inputs_scheme"] = SCHEME
    for b in built:
        p: Path = b["path"]
        manifest["assets"][p.name] = {
            "kind": "generated",
            "generator": "generators/terrain_gen.py",
            "terrain_epoch": args.epoch,
            "layer": "water" if p.name.startswith("water__") else "ground",
            "inputs_sha256": sha,
            "bytes": p.stat().st_size,
            "triangles": b["tris"],
            **({"mesh_vs_heightfield": b["fit"]} if "fit" in b else {}),
            "baked_ao": False,
        }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"\nmanifest updated: {len(built)} terrain asset(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
