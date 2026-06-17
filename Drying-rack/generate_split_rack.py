"""
Split "design4 diamond" rack into two flat-printable parts:
  1. panel_diamond_flat.stl  - 6mm flat panel carrying the exact diamond-trellis
                               pattern extracted from the original STL, plus
                               finger tabs along the bottom edge.
  2. base_diamond_stand.stl  - low decorative drain-stand the panel plugs into,
                               with matching mortises and drainage slots.

Both print flat with no overhangs: every finger tab is the full panel thickness
and is only shaped in the panel's own plane, so the bottom-edge joint has no
overhanging geometry in either part's flat print orientation.

Assembly: stand the panel up, drop the fingers straight down into the base
mortises (clearance fit), optionally add super glue.

Run:  python generate_split_rack.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.venv/lib/python3.14/site-packages'))

import numpy as np
import trimesh
from shapely.geometry import Polygon, box, LineString
from shapely.ops import unary_union
import shapely.affinity as aff

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_STL = os.path.join(OUT_DIR, 'cutting board rack design4 diamond.stl')

# ── Parameters (tune here) ─────────────────────────────────────────────────────
PANEL_W   = 200.0   # mm, X  (matches original)
PANEL_H   = 160.0   # mm, Y in panel coords (visible lattice height)
PANEL_T   =   6.0   # mm, Z (printed flat -> this is the print height)
FRAME     =   6.0   # mm, solid border re-applied around the lattice
CORNER_R  =   4.0   # mm, outer corner rounding

TAB_H     =  12.0   # mm, finger length below the panel (into the base)
N_FINGERS =   5
FINGER_W  =  26.0   # mm, width of each finger
CHAMFER   =   1.5   # mm, 45 lead-in chamfer on finger bottom corners
CLEAR     =   0.35  # mm, clearance per joint (mortise larger than finger)

# Base (4-panel drying rack with sponge bays + drainage)
BASE_W     = 200.0   # mm, X (matches panel width)
N_PANELS   =   4     # number of panels the base accepts
BAY_W      =  14.0   # mm, clear sponge bay between panels (12-15mm)
END_WALL   =   0.0   # mm, border front/back (0 = outer panels flush to edges)
BASE_H     =  18.0   # mm, Z height
SLOT_DEPTH =  12.0   # mm, how deep the mortises go (== TAB_H)
MOUTH_CHAMF=   0.5   # mm, 45 lead-in chamfer around each mortise mouth

# Drainage slots: as wide as possible, leaving only thin support bridges
DRAIN_N      =  4    # slots per bay
DRAIN_BRIDGE = 10.0  # mm, support between adjacent drain slots (v1-v3)
DRAIN_RIM    = 10.0  # mm, solid side rail at each X end
DRAIN_W      =  6.0  # mm, slot width in Y (along bay)

# v4 soft-drain variant
V4_DRAIN_BRIDGE  = 5.0   # mm, narrower bridges -> wider holes
V4_FUNNEL_DEPTH  = 2.0   # mm, depth of the soft draining lip
V4_FUNNEL_FLARE  = 1.5   # mm, how far the lip flares per side at the top

OUT_PANEL   = os.path.join(OUT_DIR, 'panel_diamond_flat.stl')
OUT_PANEL_C    = os.path.join(OUT_DIR, 'panel_laceria.stl')          # C: interlace lacto
OUT_PANEL_C2   = os.path.join(OUT_DIR, 'panel_laceria_v3_clean.stl')  # C v3: mitred joins, no close
OUT_PANEL_C4   = os.path.join(OUT_DIR, 'panel_laceria_v4.stl')        # C v4: v3 + corner notch fill
OUT_PANEL_HERO3 = os.path.join(OUT_DIR, 'panel_hero_8star_v3.stl')      # Hero v3: open 4mm-strut tessellation
OUT_PANEL_MOORISH = os.path.join(OUT_DIR, 'panel_moorish.stl')          # Moorish stepped-diamond lattice
OUT_JIG = os.path.join(OUT_DIR, 'glue_jig_top.stl')                      # temporary top spacing/gluing jig

# Glue jig (temporary): comb that caps the panel tops to hold spacing while gluing
JIG_X        = 200.0   # mm, spans full panel width
JIG_FIN_H    =  12.0   # mm, how far the spacer bars drop into the gaps
JIG_PLATE_T  =   3.0   # mm, flat top plate (weighting surface)
JIG_SLOT_CLR =   1.0   # mm, total clearance on each panel slot
JIG_OUTER_W  =   3.5   # mm, width of the two outer retaining bars

# Zellij panel design parameters
C_PITCH, C_STRUT, C_FRAME       = 44.0, 2.0, 8.0   # medium scale, ~4mm struts, wider border
HERO_PITCH, HERO_STRUT, HERO_FRAME = 40.0, 2.0, 8.0   # open star tessellation, ~4mm struts
MOORISH_STRUT, MOORISH_FRAME = 2.0, 8.0               # stepped-diamond lattice, ~4mm struts
OUT_BASE    = os.path.join(OUT_DIR, 'base_diamond_stand.stl')               # v1: flush ends
OUT_BASE_V2 = os.path.join(OUT_DIR, 'base_diamond_stand_v2_2mmwall.stl')    # v2: 2mm end wall
OUT_BASE_V3 = os.path.join(OUT_DIR, 'base_diamond_stand_v3_chamfered.stl')  # v3: v2 + mouth chamfer
OUT_BASE_V4 = os.path.join(OUT_DIR, 'base_diamond_stand_v4_softdrain.stl')  # v4: v3 + 5mm bridges + soft drains


# ── Helpers (mirrors generate_drying_rack.py) ──────────────────────────────────

def rounded_rect(x0, y0, x1, y1, r):
    inner = box(x0 + r, y0 + r, x1 - r, y1 - r)
    return inner.buffer(r, resolution=8)


def extrude(poly, thickness):
    return trimesh.creation.extrude_polygon(poly, thickness)


def clean(m):
    m = trimesh.Trimesh(vertices=m.vertices, faces=m.faces, process=True)
    m.merge_vertices()
    m.remove_unreferenced_vertices()
    if not m.is_watertight:
        trimesh.repair.fill_holes(m)
        trimesh.repair.fix_winding(m)
        m.merge_vertices()
    return m


def report(m, name):
    bb = m.bounding_box.extents
    print(f"  {name}: {bb[0]:.1f} x {bb[1]:.1f} x {bb[2]:.1f} mm   "
          f"watertight={m.is_watertight}  tris={len(m.faces)}")


# ── Extract the diamond-trellis pattern from the original STL ───────────────────

def extract_pattern():
    """
    Project every triangle of the source mesh onto the X-Z plane and union them.
    The result is the exact 'see-through' silhouette: solid where the lattice has
    material, open where you can see through. Returns a Shapely polygon placed in
    panel coords (X 0..PANEL_W, Y 0..PANEL_H), trimmed to the lattice window.
    """
    m = trimesh.load(SRC_STL)
    tris = m.triangles
    polys = []
    for t in tris:
        p = Polygon([(t[0, 0], t[0, 2]), (t[1, 0], t[1, 2]), (t[2, 0], t[2, 2])])
        if p.area > 0.05:
            polys.append(p)
    occ = unary_union(polys)

    # Source lattice: X in [-100, 100], visible pattern Z in ~[6, 166.5].
    # Crop to the patterned window, then re-origin to (0,0) and scale to PANEL_H.
    z_lo, z_hi = 6.0, 166.5
    occ = occ.intersection(box(-100, z_lo, 100, z_hi))
    # move to positive coords: X+100 -> 0..200 ; Z-z_lo -> 0..(z_hi-z_lo)
    occ = aff.translate(occ, xoff=100.0, yoff=-z_lo)
    src_h = z_hi - z_lo
    occ = aff.scale(occ, xfact=1.0, yfact=PANEL_H / src_h, origin=(0, 0))
    return occ


# ── Panel ──────────────────────────────────────────────────────────────────────

def finger_polygon(cx):
    """One finger tab below the panel (y<0), full thickness, chamfered bottom."""
    x0, x1 = cx - FINGER_W / 2, cx + FINGER_W / 2
    c = CHAMFER
    pts = [
        (x0, 0.5), (x0, -TAB_H + c), (x0 + c, -TAB_H),
        (x1 - c, -TAB_H), (x1, -TAB_H + c), (x1, 0.5),
    ]
    return Polygon(pts)


MIN_PIECE = 25.0   # mm^2, drop solid fragments smaller than this (loose bits)
MIN_HOLE  =  4.0   # mm^2, fill openings smaller than this (won't print cleanly)


def cleanup_lattice(geom):
    """Make a strut field printable: drop tiny disconnected solids and fill
    sub-printable holes. Keeps only pieces that survive the area thresholds."""
    geoms = list(geom.geoms) if geom.geom_type == 'MultiPolygon' else [geom]
    out = []
    for g in geoms:
        if g.area < MIN_PIECE:
            continue
        keep_holes = [r for r in g.interiors if Polygon(r).area >= MIN_HOLE]
        out.append(Polygon(g.exterior.coords, [r.coords for r in keep_holes]))
    return unary_union(out)


def assemble_panel(lattice, frame=FRAME):
    """Wrap a 2D strut field in the frame + finger tabs and extrude to a panel.
    Reused by every pattern so they all fit the same base. `frame` can be widened
    a touch for busy patterns so edge strap-ends don't leave tiny slivers."""
    # Outline: top two corners rounded, bottom two corners SQUARE so panels butt
    # in neatly against the base. (union of fully-rounded rect + square lower band)
    outer = unary_union([
        rounded_rect(0, 0, PANEL_W, PANEL_H, CORNER_R),
        box(0, 0, PANEL_W, PANEL_H - CORNER_R),
    ])
    inner = box(frame, frame, PANEL_W - frame, PANEL_H - frame)
    ring = outer.difference(inner)

    # Frame ring + lattice (clipped + cleaned) + finger tabs, all connected
    body = cleanup_lattice(unary_union([ring, lattice.intersection(outer)]))
    fingers = unary_union([finger_polygon(cx) for cx in finger_centers()])
    return clean(extrude(unary_union([body, fingers]), PANEL_T))


def build_panel():
    return assemble_panel(extract_pattern())


# ── Zellij pattern generators (Andalusian / Alhambra openwork) ──────────────────

def star_poly(cx, cy, Ro, Ri, phase=0.0, n=8):
    """2n-vertex star polygon (n points), outer radius Ro, inner radius Ri."""
    return Polygon([(cx + (Ro if k % 2 == 0 else Ri) * np.cos(phase + k * np.pi / n),
                     cy + (Ro if k % 2 == 0 else Ri) * np.sin(phase + k * np.pi / n))
                    for k in range(2 * n)])


def _grid(P):
    """Grid that overfills the inner area by one cell each side (pad=2)."""
    iw, ih = PANEL_W - 2 * FRAME, PANEL_H - 2 * FRAME
    nx, ny = int(iw // P) + 3, int(ih // P) + 3
    return nx, ny, (PANEL_W - (nx - 1) * P) / 2, (PANEL_H - (ny - 1) * P) / 2


def pattern_laceria(P, w):
    """C — interlacing strap lacto: 8-point star rings at each node, linked to
    their axis and diagonal neighbours by straps (the X-in-box starburst look)."""
    nx, ny, ox, oy = _grid(P)
    ribs = []
    for i in range(nx):
        for j in range(ny):
            cx, cy = ox + i * P, oy + j * P
            ribs.append(star_poly(cx, cy, P * 0.62, P * 0.30, np.pi / 8).boundary.buffer(w))
            for dx, dy in [(P, 0), (0, P), (P, P), (P, -P)]:
                ribs.append(LineString([(cx, cy), (cx + dx, cy + dy)]).buffer(w * 0.78))
    inner = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)
    return unary_union(ribs).intersection(inner)


def pattern_laceria_smooth(P, w, close=0.0):
    """C (clean) — identical layout to pattern_laceria (uniform, robust separate
    buffers) but every buffer uses MITRED joins + FLAT caps, so the round bumps
    where straps meet the squares become clean straight angles.

    `close` > 0 applies a small mitred morphological close (fill then shave) that
    fills the tiny corner notches where edge struts meet the diagonal X, carrying
    the wall straight into the cross strut. Mitred so sharp points stay sharp."""
    MITRE = dict(join_style=2, cap_style=2, mitre_limit=2.0)
    nx, ny, ox, oy = _grid(P)
    ribs = []
    for i in range(nx):
        for j in range(ny):
            cx, cy = ox + i * P, oy + j * P
            ribs.append(star_poly(cx, cy, P * 0.62, P * 0.30, np.pi / 8).boundary.buffer(w, **MITRE))
            for dx, dy in [(P, 0), (0, P), (P, P), (P, -P)]:
                ribs.append(LineString([(cx, cy), (cx + dx, cy + dy)]).buffer(w * 0.78, **MITRE))
    struts = unary_union(ribs)
    if close > 0:
        struts = (struts.buffer(close, join_style=2, mitre_limit=2.0)
                        .buffer(-close, join_style=2, mitre_limit=2.0)
                        .buffer(0))
    inner = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)
    return struts.intersection(inner)


def _diamond(cx, cy, d):
    """Axis-aligned square rotated 45 -> diamond, half-diagonal d*sqrt(2)."""
    return aff.rotate(box(cx - d, cy - d, cx + d, cy + d), 45, origin=(cx, cy))


def _stepped_square(cx, cy, a, s):
    """Square (half-width a) with a stair-step notch at each corner -> the
    Moorish stepped-square node motif."""
    p = [(-(a - 2 * s), a), (a - 2 * s, a), (a - 2 * s, a - s), (a - s, a - s),
         (a - s, a - 2 * s), (a, a - 2 * s), (a, -(a - 2 * s)), (a - s, -(a - 2 * s)),
         (a - s, -(a - s)), (a - 2 * s, -(a - s)), (a - 2 * s, -a), (-(a - 2 * s), -a),
         (-(a - 2 * s), -(a - s)), (-(a - s), -(a - s)), (-(a - s), -(a - 2 * s)),
         (-a, -(a - 2 * s)), (-a, a - 2 * s), (-(a - s), a - 2 * s),
         (-(a - s), a - s), (-(a - 2 * s), a - s)]
    return aff.translate(Polygon(p), cx, cy)


def _clover(cx, cy, R, w):
    """Small diamond ring with a 4-petal plus centre (the medallion motif)."""
    MIT = dict(join_style=2, cap_style=2, mitre_limit=6)
    dia = aff.rotate(box(cx - R, cy - R, cx + R, cy + R), 45, origin=(cx, cy)).boundary.buffer(w, **MIT)
    plus = unary_union([LineString([(cx - R * 0.8, cy), (cx + R * 0.8, cy)]).buffer(w, **MIT),
                        LineString([(cx, cy - R * 0.8), (cx, cy + R * 0.8)]).buffer(w, **MIT)])
    return unary_union([dia, plus])


def pattern_moorish(w):
    """Stepped-diamond Moorish lattice (from the reference diagram): a 4x4 grid of
    large diamonds with stepped-square node motifs and four clover medallions, all
    at uniform ~2w struts. Mitred for crisp stair-steps."""
    MIT = dict(join_style=2, cap_style=2, mitre_limit=6)
    fr = MOORISH_FRAME
    nx, ny = 5, 5
    ox, oy = fr, fr
    Px = (PANEL_W - 2 * fr) / (nx - 1)
    Py = (PANEL_H - 2 * fr) / (ny - 1)
    parts = []
    for i in range(nx):
        for j in range(ny):
            cx, cy = ox + i * Px, oy + j * Py
            for di, dj in [(1, 1), (1, -1)]:          # diagonal diamond lattice
                ii, jj = i + di, j + dj
                if 0 <= ii < nx and 0 <= jj < ny:
                    parts.append(LineString([(cx, cy), (ox + ii * Px, oy + jj * Py)]).buffer(w, **MIT))
    clov = {(2, 1), (2, 3), (1, 2), (3, 2)}            # clover medallions
    for i in range(nx):
        for j in range(ny):
            cx, cy = ox + i * Px, oy + j * Py
            if (i, j) in clov:
                parts.append(_clover(cx, cy, 9.0, w))
            else:
                parts.append(_stepped_square(cx, cy, 11.0, 3.0).boundary.buffer(w, **MIT))
    inner = box(fr, fr, PANEL_W - fr, PANEL_H - fr)
    return unary_union(parts).intersection(inner)


def pattern_hero_8star(P, w):
    """Hero — open 8-point star + diamond tessellation: chubby 8-point star holes
    on the grid + diamond holes at the cell centres, sized to tile (touch), then
    each shrunk by `w` so a uniform ~2w strut is left between every hole. Airy,
    with the same straight mitred-edge finish as the lacto panel."""
    nx, ny, ox, oy = _grid(P)
    tiles = []
    for i in range(nx):
        for j in range(ny):                         # chubby 8-point star holes
            cx, cy = ox + i * P, oy + j * P
            tiles.append(star_poly(cx, cy, P * 0.50, P * 0.40, phase=0.0))
    for i in range(nx - 1):
        for j in range(ny - 1):                     # diamonds fill the centres
            cx, cy = ox + (i + 0.5) * P, oy + (j + 0.5) * P
            tiles.append(_diamond(cx, cy, P * 0.21))
    holes = unary_union([t.buffer(-w, join_style=2, mitre_limit=2.0) for t in tiles])
    inner = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)
    return inner.difference(holes)


def finger_centers():
    pitch = PANEL_W / N_FINGERS
    return [pitch * (i + 0.5) for i in range(N_FINGERS)]


# ── Base ────────────────────────────────────────────────────────────────────────

def panel_centers_y(end_wall=END_WALL):
    """Y centreline of each of the N_PANELS panel slots in the base."""
    pitch = PANEL_T + BAY_W
    y0 = end_wall + PANEL_T / 2
    return [y0 + i * pitch for i in range(N_PANELS)]


def base_depth(end_wall=END_WALL):
    return 2 * end_wall + N_PANELS * PANEL_T + (N_PANELS - 1) * BAY_W


def top_funnel(cx, yc, w, t, depth, flare):
    """Truncated-pyramid solid that, when subtracted, leaves a sloped lip around
    an opening at the top surface: the hole widens from (w x t) at depth below
    the top out to (+flare per side) at the top, funnelling water down into it.
    Used for both the mortise lead-in and the soft-draining drain holes."""
    z0 = BASE_H - depth          # where the slope starts (nominal hole size)
    z1 = BASE_H + 1.0            # above the top surface (gets clipped)
    slope = flare / depth        # half-extent growth per unit Z
    grow_top = slope * (z1 - z0)
    hw, ht = w / 2, t / 2
    pts = []
    for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        pts.append([cx + sx * hw, yc + sy * ht, z0])
        pts.append([cx + sx * (hw + grow_top), yc + sy * (ht + grow_top), z1])
    return trimesh.Trimesh(vertices=np.array(pts)).convex_hull


def build_base(end_wall=END_WALL, mouth_chamf=0.0, drain_bridge=DRAIN_BRIDGE,
               drain_funnel_depth=0.0, drain_funnel_flare=0.0):
    """
    Drying-rack tray (X=width, Y=depth, Z=height) that accepts N_PANELS panels:
      - each panel locks in via a row of N_FINGERS mortises (clearance fit)
      - clear sponge bays (BAY_W) between panels
      - drainage slots through the floor of every bay
    """
    depth = base_depth(end_wall)
    base = extrude(box(0, 0, BASE_W, depth), BASE_H)

    mort_w = FINGER_W + CLEAR          # X
    mort_t = PANEL_T + CLEAR           # Y (panel thickness direction)

    cuts = []
    # mortises: one row per panel (+ optional lead-in chamfer at the mouth)
    for yc in panel_centers_y(end_wall):
        for cx in finger_centers():
            cuts.append(trimesh.creation.box(
                extents=[mort_w, mort_t, SLOT_DEPTH + 1],
                transform=trimesh.transformations.translation_matrix(
                    [cx, yc, BASE_H - SLOT_DEPTH / 2 + 0.5])))
            if mouth_chamf > 0:
                cuts.append(top_funnel(cx, yc, mort_w, mort_t, mouth_chamf, mouth_chamf))

    # drainage: wide through-slots in each sponge bay, drain_bridge mm bridges,
    # optionally with a soft funnel lip at the top so water sheds down into them
    centers = panel_centers_y(end_wall)
    bay_centers = [(centers[i] + centers[i + 1]) / 2 for i in range(N_PANELS - 1)]
    usable = BASE_W - 2 * DRAIN_RIM - (DRAIN_N - 1) * drain_bridge
    slot_len = usable / DRAIN_N
    for yc in bay_centers:
        for i in range(DRAIN_N):
            cx = DRAIN_RIM + slot_len / 2 + i * (slot_len + drain_bridge)
            cuts.append(trimesh.creation.box(
                extents=[slot_len, DRAIN_W, BASE_H + 2],
                transform=trimesh.transformations.translation_matrix(
                    [cx, yc, BASE_H / 2])))
            if drain_funnel_depth > 0:
                cuts.append(top_funnel(cx, yc, slot_len, DRAIN_W,
                                       drain_funnel_depth, drain_funnel_flare))

    result = base
    for c in cuts:
        result = trimesh.boolean.difference([result, c], engine='manifold')

    return clean(result)


def build_glue_jig(end_wall=2.0):
    """Temporary top jig: a comb of continuous bars that drops over the assembled
    panel tops. 3 internal bars fill the gaps + 2 outer bars hug the end panels,
    with slots between them for the panel tops; a flat plate on top takes weight
    so the panel-to-base glue joints press home while curing.
    Sized off the v4 base spacing so it registers exactly."""
    centers = panel_centers_y(end_wall)            # [5, 25, 45, 65]
    sh = PANEL_T / 2 + JIG_SLOT_CLR / 2            # half slot width
    slots = [(c - sh, c + sh) for c in centers]
    y_lo = slots[0][0] - JIG_OUTER_W
    y_hi = slots[-1][1] + JIG_OUTER_W

    # bars = the complement of the panel slots over [y_lo, y_hi]
    bars, prev = [], y_lo
    for a, b in slots:
        bars.append((prev, a))
        prev = b
    bars.append((prev, y_hi))

    parts = []
    for a, b in bars:
        parts.append(trimesh.creation.box(
            extents=[JIG_X, b - a, JIG_FIN_H],
            transform=trimesh.transformations.translation_matrix(
                [JIG_X / 2, (a + b) / 2, JIG_FIN_H / 2])))
    parts.append(trimesh.creation.box(                 # flat top plate
        extents=[JIG_X, y_hi - y_lo, JIG_PLATE_T],
        transform=trimesh.transformations.translation_matrix(
            [JIG_X / 2, (y_lo + y_hi) / 2, JIG_FIN_H + JIG_PLATE_T / 2])))

    jig = parts[0]
    for p in parts[1:]:
        jig = trimesh.boolean.union([jig, p], engine='manifold')
    return clean(jig)


# ── Main ─────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Building flat diamond panel...")
    panel = build_panel()
    panel.export(OUT_PANEL)
    report(panel, os.path.basename(OUT_PANEL))

    print("Building C lacto panel (medium scale, 4mm struts)...")
    pc = assemble_panel(pattern_laceria(C_PITCH, C_STRUT), frame=C_FRAME)
    pc.export(OUT_PANEL_C)
    report(pc, os.path.basename(OUT_PANEL_C))

    print("Building C v3 clean lacto panel (mitred joins, uniform)...")
    pc2 = assemble_panel(pattern_laceria_smooth(C_PITCH, C_STRUT), frame=C_FRAME)
    pc2.export(OUT_PANEL_C2)
    report(pc2, os.path.basename(OUT_PANEL_C2))

    print("Building C v4 lacto panel (corner notches filled)...")
    pc4 = assemble_panel(pattern_laceria_smooth(C_PITCH, C_STRUT, close=0.6), frame=C_FRAME)
    pc4.export(OUT_PANEL_C4)
    report(pc4, os.path.basename(OUT_PANEL_C4))

    print("Building Hero v3 (open 8-star tessellation, 4mm struts)...")
    ph3 = assemble_panel(pattern_hero_8star(HERO_PITCH, HERO_STRUT), frame=HERO_FRAME)
    ph3.export(OUT_PANEL_HERO3)
    report(ph3, os.path.basename(OUT_PANEL_HERO3))

    print("Building Moorish stepped-diamond panel...")
    pm = assemble_panel(pattern_moorish(MOORISH_STRUT), frame=MOORISH_FRAME)
    pm.export(OUT_PANEL_MOORISH)
    report(pm, os.path.basename(OUT_PANEL_MOORISH))

    print("Building temporary glue jig (top spacer)...")
    jig = build_glue_jig(end_wall=2.0)
    jig.export(OUT_JIG)
    report(jig, os.path.basename(OUT_JIG))

    print("Building drain-stand base (v1: outer panels flush, END_WALL=0)...")
    base = build_base(end_wall=0.0)
    base.export(OUT_BASE)
    report(base, os.path.basename(OUT_BASE))

    print("Building drain-stand base (v2: 2mm end wall, clean outer face)...")
    base2 = build_base(end_wall=2.0)
    base2.export(OUT_BASE_V2)
    report(base2, os.path.basename(OUT_BASE_V2))

    print(f"Building drain-stand base (v3: 2mm wall + {MOUTH_CHAMF}mm mortise lead-in chamfer)...")
    base3 = build_base(end_wall=2.0, mouth_chamf=MOUTH_CHAMF)
    base3.export(OUT_BASE_V3)
    report(base3, os.path.basename(OUT_BASE_V3))

    print(f"Building drain-stand base (v4: v3 + {V4_DRAIN_BRIDGE}mm drain bridges + soft draining lip)...")
    base4 = build_base(end_wall=2.0, mouth_chamf=MOUTH_CHAMF,
                       drain_bridge=V4_DRAIN_BRIDGE,
                       drain_funnel_depth=V4_FUNNEL_DEPTH,
                       drain_funnel_flare=V4_FUNNEL_FLARE)
    base4.export(OUT_BASE_V4)
    report(base4, os.path.basename(OUT_BASE_V4))

    print("Done.")
