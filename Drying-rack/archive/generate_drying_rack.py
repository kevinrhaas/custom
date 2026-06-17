"""
Moorish Mesh Drying Rack Generator
Produces separate base.stl + panel STLs for designs 3, 4, 5, 6.
Print panels flat (200x160mm footprint, 4mm Z), base flat.
Assembly: panel tab slides into base slot (full 200mm width).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.venv/lib/python3.14/site-packages'))

import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import shapely.affinity as aff

# ── Shared parameters ─────────────────────────────────────────────────────────
PANEL_W      = 200.0   # mm, X
PANEL_H      = 160.0   # mm, Y (visible height)
PANEL_T      =   4.0   # mm, Z (thickness, printed flat)
FRAME        =   6.0   # mm, solid frame width on sides + bottom
CORNER_R     =   4.0   # mm, corner softening radius

TAB_H        =  12.0   # mm, assembly tab below panel (hidden in base slot)
TAB_CLEARANCE=   0.4   # mm, total clearance panel-in-slot

# Base
BASE_W       = 200.0
N_PANELS     =   4
BAY_W        =  10.0   # mm, sponge slot width
WALL         =   5.0   # mm, outer wall on each side (depth direction)
BASE_H       =  20.0   # mm, height of base (tab slot depth = TAB_H - 2mm)
SLOT_DEPTH   =  12.0   # mm, how deep panel tab goes into base
SLOT_W       = PANEL_T + TAB_CLEARANCE  # 4.4mm

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Helpers ───────────────────────────────────────────────────────────────────

def extrude_polygon(poly, thickness):
    """Extrude a Shapely polygon to a trimesh solid."""
    return trimesh.creation.extrude_polygon(poly, thickness)


def rounded_rect(x0, y0, x1, y1, r):
    """Shapely polygon of a rectangle with rounded corners."""
    from shapely.geometry import box
    from shapely import buffer
    # shrink rect by r, then buffer by r to get rounded corners
    inner = box(x0 + r, y0 + r, x1 - r, y1 - r)
    return inner.buffer(r, resolution=8)


def panel_outline(w=PANEL_W, h=PANEL_H, r=CORNER_R):
    """Outer boundary of a panel (with tab appended below)."""
    # Visible panel: rounded rect
    visible = rounded_rect(0, 0, w, h, r)
    # Tab: solid rect extending below (no rounding needed, hidden in slot)
    from shapely.geometry import box
    tab = box(0, -TAB_H, w, 0)
    return unary_union([visible, tab])


def make_panel_solid():
    """Full solid panel shape (for subtracting openings from)."""
    return panel_outline()


def save_stl(mesh, name):
    path = os.path.join(OUT_DIR, name)
    mesh.export(path)
    bb = mesh.bounding_box.extents
    wt = mesh.is_watertight
    print(f"  {name}: {bb[0]:.1f}x{bb[1]:.1f}x{bb[2]:.1f}mm  watertight={wt}  tris={len(mesh.faces)}")
    return path


def build_mesh_from_2d(solid_2d, thickness=PANEL_T):
    """Extrude 2D solid region to 3D panel."""
    if isinstance(solid_2d, MultiPolygon):
        parts = [extrude_polygon(g, thickness) for g in solid_2d.geoms if g.area > 0.1]
        m = trimesh.util.concatenate(parts)
    else:
        m = extrude_polygon(solid_2d, thickness)
    m = trimesh.Trimesh(vertices=m.vertices, faces=m.faces, process=True)
    m.merge_vertices()
    m.remove_unreferenced_vertices()
    if not m.is_watertight:
        trimesh.repair.fill_holes(m)
        trimesh.repair.fix_winding(m)
        m.merge_vertices()
    return m


# ── Base ──────────────────────────────────────────────────────────────────────

def build_base():
    """
    Base: 200mm wide, depth = WALL + N_PANELS*PANEL_T + (N_PANELS-1)*BAY_W + WALL
    Has 4 panel slots (full 200mm long, SLOT_W wide, SLOT_DEPTH deep) and
    drainage cutouts in each bay.
    """
    from shapely.geometry import box
    depth = WALL + N_PANELS * PANEL_T + (N_PANELS - 1) * BAY_W + WALL

    # Base footprint (viewed from top: X=width, Y=depth)
    base_2d = box(0, 0, BASE_W, depth)

    # Panel slot positions (Y center of each slot)
    slot_centers = []
    y = WALL + PANEL_T / 2
    for i in range(N_PANELS):
        slot_centers.append(y)
        if i < N_PANELS - 1:
            y += PANEL_T + BAY_W

    # Bay centers (between slots)
    bay_centers = [(slot_centers[i] + slot_centers[i+1]) / 2 for i in range(N_PANELS - 1)]

    # Cut panel slots: full width, SLOT_W wide, going down from top
    # We model the base as a solid and subtract slots from the top
    # Build as 2D top-view then extrude, subtract slots separately in 3D

    base_solid = extrude_polygon(base_2d, BASE_H)

    # Cut slots: boxes running full X width, SLOT_W in Y, SLOT_DEPTH in Z from top
    slot_cuts = []
    for yc in slot_centers:
        cut = trimesh.creation.box(
            extents=[BASE_W + 2, SLOT_W, SLOT_DEPTH + 1],
            transform=trimesh.transformations.translation_matrix([
                BASE_W / 2,
                yc,
                BASE_H - SLOT_DEPTH / 2 + 0.5
            ])
        )
        slot_cuts.append(cut)

    # Drainage holes: 2 slots per bay, each 60mm long x 4mm wide, through full Z
    drain_cuts = []
    dx_offsets = [BASE_W * 0.28, BASE_W * 0.72]  # two columns
    for yc in bay_centers:
        for dx in dx_offsets:
            cut = trimesh.creation.box(
                extents=[4.0, BAY_W - 2, BASE_H + 2],
                transform=trimesh.transformations.translation_matrix([dx, yc, BASE_H / 2])
            )
            drain_cuts.append(cut)

    # Boolean subtract using manifold3d via trimesh
    result = base_solid
    all_cuts = slot_cuts + drain_cuts
    for cut in all_cuts:
        result = trimesh.boolean.difference([result, cut], engine='manifold')

    result.merge_vertices()
    result.remove_unreferenced_vertices()
    return result, depth


# ── Design 6: Granada Arcade ──────────────────────────────────────────────────

def design6_panel():
    """
    Granada Arcade: vertical columns with pointed Moorish arches between them.
    Columns are solid, arch openings are tall pointed shapes.
    Printed flat. Frame on all 4 sides + rounded corners.
    """
    from shapely.geometry import box
    import math

    outline = panel_outline()
    # Interior area (inside frame, inside visible panel only — not tab)
    interior_box = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)

    # Arcade parameters
    n_arches = 5           # number of arch openings across width
    inner_w = PANEL_W - 2 * FRAME
    inner_h = PANEL_H - 2 * FRAME
    col_w = 7.0            # column width
    arch_gap = (inner_w - (n_arches + 1) * col_w) / n_arches  # opening width per arch

    # Each arch: rectangle + pointed top
    # Arch opening: arch_gap wide, rises from bottom of interior to near top
    # Pointed top: isoceles triangle / two lines meeting at apex
    arch_openings = []
    for i in range(n_arches):
        x0 = FRAME + (i + 1) * col_w + i * arch_gap
        x1 = x0 + arch_gap
        xc = (x0 + x1) / 2
        y0 = FRAME                       # bottom of opening
        y_arch_start = PANEL_H - FRAME - arch_gap * 0.6  # where arch begins

        # Rectangular body of arch
        body = box(x0, y0, x1, y_arch_start)

        # Pointed arch top: polygon with two 45° sides meeting at apex
        apex_h = arch_gap * 0.5          # height of pointed section
        apex_y = y_arch_start + apex_h
        apex_pts = [
            (x0, y_arch_start),
            (x1, y_arch_start),
            (xc, apex_y),
        ]
        arch_top = Polygon(apex_pts)

        arch_openings.append(unary_union([body, arch_top]))

    # Subtract openings from the outline (only within interior_box)
    openings_union = unary_union(arch_openings).intersection(interior_box)
    panel_2d = outline.difference(openings_union)

    return build_mesh_from_2d(panel_2d)


# ── Design 4: Diamond Trellis ─────────────────────────────────────────────────

def design4_panel():
    """
    Diamond trellis: 45° diagonal struts crossing in both directions.
    Printed flat.
    """
    from shapely.geometry import box, LineString
    import math

    outline = panel_outline()
    interior_box = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)

    strut_w = 4.5   # half-width buffer for each diagonal line
    spacing = 22.0  # distance between parallel diagonals

    inner_w = PANEL_W - 2 * FRAME
    inner_h = PANEL_H - 2 * FRAME

    # Generate diagonal lines in both directions over the interior
    diag_struts = []
    diag_range = int((inner_w + inner_h) / spacing) + 4

    for k in range(-diag_range, diag_range + 1):
        offset = k * spacing
        # NE direction (bottom-left to top-right)
        x0 = FRAME + offset - inner_h
        x1 = FRAME + offset + inner_w
        line_ne = LineString([(x0, FRAME), (x1, FRAME + inner_h)])
        strut = line_ne.buffer(strut_w / 2, cap_style=2)
        diag_struts.append(strut)

        # NW direction (bottom-right to top-left)
        x0 = FRAME + offset
        x1 = FRAME + offset - inner_h
        line_nw = LineString([(FRAME + inner_w - offset + FRAME, FRAME),
                               (FRAME + inner_w - offset + FRAME - inner_h, FRAME + inner_h)])
        strut2 = line_nw.buffer(strut_w / 2, cap_style=2)
        diag_struts.append(strut2)

    # Also add frame
    frame_poly = outline.difference(interior_box)

    lattice = unary_union(diag_struts).intersection(interior_box)
    panel_2d = unary_union([frame_poly, lattice])
    panel_2d = panel_2d.intersection(outline)  # clip to outline

    return build_mesh_from_2d(panel_2d)


# ── Design 5: Seville Clover ──────────────────────────────────────────────────

def design5_panel():
    """
    Seville Clover: chamfered quatrefoil openings (4-lobed, 45° geometry) with
    star/cross connectors. Printed flat.
    """
    from shapely.geometry import box
    import math

    outline = panel_outline()
    interior_box = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)

    # Quatrefoil parameters
    cell_size = 32.0    # cell repeat
    lobe_r    = 9.0     # lobe "radius" (half-width of each lobe)
    connector = 4.5     # width of star connector at cell corners

    inner_w = PANEL_W - 2 * FRAME
    inner_h = PANEL_H - 2 * FRAME

    nx = int(inner_w / cell_size) + 1
    ny = int(inner_h / cell_size) + 1

    openings = []
    for ix in range(nx):
        for iy in range(ny):
            cx = FRAME + (ix + 0.5) * cell_size
            cy = FRAME + (iy + 0.5) * cell_size

            # Chamfered quatrefoil: 4 lobes as octagons (45° chamfer)
            # Each lobe is a small octagon offset in one of the 4 cardinal directions
            lobe_pts_list = []
            for angle_deg in [0, 90, 180, 270]:
                a = math.radians(angle_deg)
                lx = cx + math.cos(a) * (cell_size * 0.22)
                ly = cy + math.sin(a) * (cell_size * 0.22)
                # octagon approximation of circle with 45° chamfer
                from shapely.geometry import Point
                lobe = Point(lx, ly).buffer(lobe_r, resolution=4)
                lobe_pts_list.append(lobe)

            quatrefoil = unary_union(lobe_pts_list)
            openings.append(quatrefoil)

    openings_union = unary_union(openings).intersection(interior_box)
    panel_2d = outline.difference(openings_union)

    return build_mesh_from_2d(panel_2d)


# ── Design 3: Teardrop Moorish Arch ───────────────────────────────────────────

def design3_panel():
    """
    Teardrop Moorish Arch: columns of teardrop-shaped openings (rounded base,
    pointed apex), offset by half a row in alternating columns.
    Printed flat.
    """
    from shapely.geometry import box
    import math

    outline = panel_outline()
    interior_box = box(FRAME, FRAME, PANEL_W - FRAME, PANEL_H - FRAME)

    # Teardrop cell params
    col_w    = 34.0   # column repeat width
    row_h    = 38.0   # row repeat height
    td_w     = 22.0   # teardrop width
    td_h     = 30.0   # teardrop height
    strut_w  =  5.0   # wall between teardrops

    inner_w = PANEL_W - 2 * FRAME
    inner_h = PANEL_H - 2 * FRAME
    n_cols = int(inner_w / col_w) + 1
    n_rows = int(inner_h / row_h) + 2

    def teardrop(cx, cy, w, h):
        """Teardrop shape: rounded base blending to pointed apex."""
        r = w / 2
        pts = []
        # Bottom arc: full circle bottom half (180..360 = lower semicircle)
        for deg in range(180, 361, 8):
            a = math.radians(deg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        # Right side: curve from (cx+r, cy) up to apex
        # Use a few interpolated points for a gentle taper
        steps = 6
        for i in range(1, steps):
            t = i / steps
            x = cx + r * (1 - t)
            y = cy + t * h
            pts.append((x, y))
        # Apex
        pts.append((cx, cy + h))
        # Left side: mirror
        for i in range(steps - 1, 0, -1):
            t = i / steps
            x = cx - r * (1 - t)
            y = cy + t * h
            pts.append((x, y))
        return Polygon(pts)

    openings = []
    for ic in range(n_cols):
        cx = FRAME + (ic + 0.5) * col_w
        offset_y = (row_h / 2) if (ic % 2 == 1) else 0
        for ir in range(n_rows):
            cy = FRAME + offset_y + ir * row_h
            td = teardrop(cx, cy, td_w, td_h)
            openings.append(td)

    # Use boolean subtraction (more robust for many holes than extrude_polygon)
    solid_mesh = extrude_polygon(outline, PANEL_T)
    solid_mesh = trimesh.Trimesh(vertices=solid_mesh.vertices, faces=solid_mesh.faces, process=True)

    for td in openings:
        td_clipped = td.intersection(interior_box)
        if td_clipped.is_empty or td_clipped.area < 1.0:
            continue
        try:
            cut = extrude_polygon(td_clipped, PANEL_T + 2)
            cut_mesh = trimesh.Trimesh(vertices=cut.vertices, faces=cut.faces, process=True)
            cut_mesh.apply_translation([0, 0, -1])
            solid_mesh = trimesh.boolean.difference([solid_mesh, cut_mesh], engine='manifold')
        except Exception:
            pass

    solid_mesh.merge_vertices()
    solid_mesh.remove_unreferenced_vertices()
    return solid_mesh


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--design', choices=['all', 'base', '3', '4', '5', '6'], default='all')
    args = p.parse_args()

    do_all = args.design == 'all'

    if do_all or args.design == 'base':
        print("Building base...")
        base, base_depth = build_base()
        save_stl(base, 'base.stl')
        print(f"  Base depth: {base_depth:.1f}mm")

    if do_all or args.design == '6':
        print("Building Design 6 (Granada Arcade)...")
        m = design6_panel()
        save_stl(m, 'panel_design6_granada_arcade.stl')

    if do_all or args.design == '4':
        print("Building Design 4 (Diamond Trellis)...")
        m = design4_panel()
        save_stl(m, 'panel_design4_diamond.stl')

    if do_all or args.design == '5':
        print("Building Design 5 (Seville Clover)...")
        m = design5_panel()
        save_stl(m, 'panel_design5_seville_clover.stl')

    if do_all or args.design == '3':
        print("Building Design 3 (Teardrop Arch)...")
        m = design3_panel()
        save_stl(m, 'panel_design3_teardrop_arch.stl')

    print("Done.")
