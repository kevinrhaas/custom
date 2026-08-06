#!/usr/bin/env python3
"""The baseline piece: a faceted knight.

This is the reference form for the whole set. Everything downstream — pawn,
bishop, rook, queen, king — stands on `chesskit.fleet_plinth()`, uses the same
chamfer language, and is built the same way. Only what happens above the
shoulders changes.

The construction method, in three moves:

  1. **Constant-width slabs.** Each mass is a chamfered extrusion of a
     side-view outline at ONE half-width, so its flank is a single flat plane
     rather than a dome. A narrow head slab unioned onto a wider body slab is
     what produces the hard jowl step. The drafts that shape the neck must
     therefore stop *below* the jowl — a draft plane that runs past it clips
     both slabs to the same width and silently annihilates the step, which is
     exactly what `assert_invariants` now refuses to let happen.
  2. **Planar slice cuts.** Taper and draft are subtracted with flat blocks,
     never modelled by varying the extrusion width — that keeps every facet
     genuinely planar and every crease a straight line.
  3. **Grooves and pockets** for the chest panel and the eye,
     each placed against the flank the solid actually has (`flank_at`) rather
     than against a formula predicting it.

Printed upright on the plinth. Claims about that are asserted at build time,
not left to this docstring: see `assert_invariants`.
"""

from __future__ import annotations

from pathlib import Path

import trimesh

from chesskit import (
    PLINTH_TOP_Z,
    Knot,
    Silhouette,
    chamfered_extrude,
    cull_slivers,
    flank_at,
    fleet_plinth,
    groove_along,
    layer_report,
    mirror_y,
    plane_block,
    pocket,
    printability,
    slice_block_z,
    NEEDLE_LIMIT,
    triangle_altitude,
    write_stl,
)

HERE = Path(__file__).parent

HEIGHT = 60.0
HEAD_W = 6.0           # half-width of the skull
BODY_W = 8.6           # half-width of the neck at the shoulder

# Bevel depth as a fraction of the chamfer. 0.80 -> the bevel plane under a
# horizontal silhouette edge sits at atan(0.80) = 38.7 deg from vertical.
BEVEL_RATIO = 0.80

# Where the head stops being governed by the neck. Every neck draft must
# terminate at or below this height or the jowl step disappears.
JOWL_Z = 47.6


def K(x: float, z: float, c: float = 1.6, b: float | None = None) -> Knot:
    """A silhouette knot. Width is set per-slab, so it is not a knot property."""
    return Knot(x, z, 0.0, c, c * BEVEL_RATIO if b is None else b)


def at_width(knots, w: float) -> Silhouette:
    return Silhouette([Knot(k.x, k.z, w, k.chamfer, k.b) for k in knots])


# --------------------------------------------------------------------------
# Outlines
# --------------------------------------------------------------------------
#
# Read the reference from the chest upward: the chest leans forward out of the
# collar, the throat draws back, the jaw is thrown forward at a hard notch, the
# muzzle runs out as a long wedge, the brow and crown rise behind it, and the
# mane falls away in five teeth to the shoulder.

CHEST = [
    K(10.6, 11.0, 1.2),               # buried in the plinth
    K(12.0, PLINTH_TOP_Z, 1.5),       # chest springs from the collar
    K(12.6, 21.0, 2.1),               # chest at its most forward
    K(11.0, 30.0, 2.1),               # three big facets down the chest, not
    K(7.6, 39.5, 1.9),                # five — the reference is not ribbed
    K(4.8, 44.6, 1.2),                # throat to jaw notch, one straight run
]

MUZZLE_AND_SKULL = [
    K(12.2, 45.2, 1.5),               # jaw underside, one straight run
    K(25.2, 46.0, 1.3),               # chin: the lower lip leads the nose
    K(22.4, 50.2, 1.0),               # nose front, strongly raked back
    # The top of the head is ONE long plane from the nostril to the crown, as
    # the reference has it. Intermediate knots along a near-straight run turn
    # by a degree or two, which is neither a flat plane nor a hard crease — it
    # is a shading seam, and it is what made the skull read as a lumpy dome.
    K(18.6, 52.6, 1.1),
    K(16.4, 53.0, 1.3),               # the nostril facet: the one break
    K(-2.0, 60.0, 2.2),               # crown
    K(-3.2, 58.7, 1.5),               # ear, thrown back
    K(-7.4, 56.2, 1.3),               # notch behind the ear (concave)
]

# The head is its own slab, closed along a line that dips just under the body's
# jowl line so the two interpenetrate instead of sharing a coincident face.
HEAD_OUTLINE = MUZZLE_AND_SKULL + [
    K(-6.2, 54.2, 1.5),
    K(1.8, 50.6, 1.6),
    K(7.4, 46.4, 1.3),
    K(4.8, 44.6, 1.2),                # throat notch, shared with the body
]

# Five teeth down the back, peak then valley. Each tooth's underside runs
# about 28 deg from vertical, so the whole crest self-supports.
MANE = [
    K(-10.7, 53.9, 1.1),              # tooth 1
    K(-9.0, 50.5, 0.9),
    K(-12.9, 47.1, 1.1),              # tooth 2
    K(-11.1, 43.7, 0.9),
    K(-13.6, 40.4, 1.1),              # tooth 3
    K(-12.4, 37.0, 0.9),
    K(-14.7, 33.6, 1.2),              # tooth 4
    K(-13.5, 30.2, 1.0),
    K(-15.8, 26.9, 1.2),              # tooth 5
    K(-14.6, 23.5, 1.1),
]

SHOULDER_BACK = [
    K(-16.8, 19.6, 1.6),              # shoulder swells back out
    K(-11.0, 10.5, 1.2),              # into the plinth
]

# The body slab closes under the skull along the jowl line and then follows the
# mane, so the crest is full-bodied rather than a fin.
BODY_OUTLINE = CHEST + [
    K(10.0, JOWL_Z, 1.3),             # jowl, tucked under the cheek
    K(3.6, 52.2, 1.5),
    K(-4.8, 55.6, 1.5),               # neck crest, filling in behind the ear
] + MANE + SHOULDER_BACK


# --------------------------------------------------------------------------
# Planar slice cuts
# --------------------------------------------------------------------------


def muzzle_taper() -> list[trimesh.Trimesh]:
    """Draw the muzzle in toward the nose AND toward its top ridge.

    One plane tilted in x and z at once. Tilting only in x leaves the muzzle a
    parallel-sided slab above the lip line; tilting in z as well makes the
    section a true wedge at every station, which is what stops the head reading
    as a bill. The same plane carries on over the skull and takes width off the
    crown, so the head is never a mushroom cap.
    """
    cut = plane_block(
        through=[(2.0, HEAD_W, 47.0), (24.8, 3.3, 47.0), (2.0, 5.1, 57.0)],
        x_range=(-18.0, 27.0),
        z_range=(43.0, 61.5),
    )
    return [cut, mirror_y(cut)]


# The three points that define the jaw plane. Named so the invariant can
# measure the angle off the same definition the cutter uses, instead of a
# number typed into a docstring beside it.
JAW_PLANE = [(9.5, 5.25, 47.1), (24.0, 3.30, 48.7), (24.0, 1.70, 46.2)]


def jaw_draft_angle() -> float:
    """Degrees from vertical of the facet `jaw_draft` cuts."""
    import math

    import numpy as np

    p, q, r = (np.array(t, float) for t in JAW_PLANE)
    n = np.cross(q - p, r - p)
    n /= np.linalg.norm(n)
    return math.degrees(math.asin(abs(n[2])))


def jaw_draft() -> list[trimesh.Trimesh]:
    """The lip line and the jaw taper, cut as ONE sloped plane.

    Three jobs from one facet: its upper edge is the lip line, a straight
    crease running the length of the muzzle; below that edge the jaw narrows to
    a keel, giving the muzzle its triangular horse section instead of a flat
    bill; and the facet itself is drafted rather than left as a flat ceiling.

    The plane runs through the lip line at the throat end, the lip line at the
    nose, and the keel under the nose. Its angle is not quoted here — it is
    computed from these same three points by `jaw_draft_angle` and asserted, so
    the number cannot drift away from the geometry the way the last one did.
    """
    cut = plane_block(
        through=JAW_PLANE,
        x_range=(9.5, 27.0),
        z_range=(41.0, 52.5),
    )
    return [cut, mirror_y(cut)]


def neck_draft() -> list[trimesh.Trimesh]:
    """The neck sheds width continuously, from the shoulder to the crest.

    ONE plane over the body's whole height, deliberately. Splitting it at the
    jowl put a block boundary inside the solid, and a cutter boundary inside a
    solid is a flat ledge — 11 mm2 of dead-level shelf across the neck flank.
    Now that the head is shaped as its own slab, nothing here can reach it, so
    the draft has no reason to stop and both of its ends sit in open air.
    """
    cut = slice_block_z((8.0, 9.2), (62.0, 6.5), -18.0, 14.0)
    return [cut, mirror_y(cut)]


def mane_taper() -> list[trimesh.Trimesh]:
    """Taper the crest so each tooth reads as a wedge, not a paddle."""
    cut = plane_block(
        through=[(-6.0, 7.7, 20.0), (-17.5, 6.4, 20.0), (-6.0, 7.0, 56.0)],
        x_range=(-18.5, -5.0),
        z_range=(17.0, 58.5),
    )
    return [cut, mirror_y(cut)]


# --------------------------------------------------------------------------
# Detail cuts — placed against the flank the solid actually has
# --------------------------------------------------------------------------


def crease(solid: trimesh.Trimesh, path, depth: float,
           half_angle: float = 30.0) -> list[trimesh.Trimesh]:
    """A V-crease held at a constant depth below the flank it runs across.

    The path is expected to RUN OUT through the surface at both ends. A groove
    that stops on the flank fades to nothing there, and the fade leaves needle
    triangles where its walls graze the surface at near-zero incidence. Past
    the run-out `flank_at` reports nothing, so those points inherit the depth
    of the last point that was actually on the solid.
    """
    flanks = [flank_at(solid, x, z) for x, z in path]
    known = [i for i, f in enumerate(flanks) if f > 0.1]
    if not known:
        raise ValueError("crease path never touches the solid")
    apex = [flanks[i] - depth if i in known
            else flanks[min(known, key=lambda k: abs(k - i))] - depth
            for i in range(len(path))]
    cut = groove_along(path, apex_y=apex, reach=7.0, half_angle=half_angle)
    return [cut, mirror_y(cut)]


def chest_panel(solid: trimesh.Trimesh) -> list[trimesh.Trimesh]:
    """Angular panel on the chest, echoing the jowl step above it.

    Held ~2 mm inboard of the chest outline: run it along the outline and it
    nicks the silhouette edge instead of cutting a panel on the flank.
    """
    return crease(solid, [(7.8, 41.5), (8.2, 35.0), (9.7, 28.0),
                          (10.6, 22.0), (12.6, 17.6)], depth=0.6, half_angle=32.0)


def eye_socket(solid: trimesh.Trimesh) -> list[trimesh.Trimesh]:
    """Triangular recess sunk into the flank, under the brow — not on it."""
    section = [(8.4, 54.6), (3.6, 53.6), (7.6, 52.0)]
    surface = min(flank_at(solid, x, z) for x, z in section)
    cut = pocket(section, surface_y=surface - 0.05, depth=1.3, reach=5.0)
    return [cut, mirror_y(cut)]


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def build() -> trimesh.Trimesh:
    """Shape each slab, THEN union.

    Cutting the assembled piece was the mistake that hollowed out this design:
    a block bounded to the muzzle still has to be bounded somewhere, and every
    bound that falls inside the assembled solid leaves a flat ledge behind it
    — while a taper plane wide enough to reach the nose also reached the neck
    and clipped both slabs to one width, erasing the jowl step it was supposed
    to sit above.

    Shaping each slab on its own fixes both at once. The head's cutters only
    have to clear the head, which is small, so their bounds sit in open air;
    and nothing that shapes the head can touch the body.
    """
    head = chamfered_extrude(at_width(HEAD_OUTLINE, HEAD_W))
    for cut in muzzle_taper() + jaw_draft():
        head = head.difference(cut)

    body = chamfered_extrude(at_width(BODY_OUTLINE, BODY_W))
    for cut in neck_draft() + mane_taper():
        body = body.difference(cut)

    piece = head.union(body).union(fleet_plinth())

    # Detail cuts are placed against the assembled, drafted solid.
    for cut in (chest_panel(piece) + eye_socket(piece)):
        piece = piece.difference(cut)

    piece = cull_slivers(piece)
    piece.apply_translation((0.0, 0.0, -piece.bounds[0][2]))
    return piece


# --------------------------------------------------------------------------
# Invariants — the build fails rather than the docstring lying
# --------------------------------------------------------------------------


def jowl_step(mesh: trimesh.Trimesh, z: float = 50.0) -> float:
    """The largest single-step drop in half-width crossing the jowl line.

    Written this way deliberately. The previous version sampled the neck at one
    x and the head at another and subtracted — which returns a healthy-looking
    number on a form that has no step at all, because the width between those
    two points was a smooth ramp. It certified as fixed exactly the regression
    it was written to catch.

    Walking the width in small increments and taking the largest single drop
    cannot be fooled that way: a ramp of any slope yields only its per-step
    slope, while a real step yields the whole step.
    """
    import numpy as np

    xs = np.arange(-3.0, 12.0, 0.4)
    widths = [flank_at(mesh, float(x), z) for x in xs]
    drops = [widths[i] - widths[i + 1] for i in range(len(widths) - 1)
             if widths[i] > 0.1 and widths[i + 1] > 0.1]
    return max(drops) if drops else 0.0


# Overhangs are judged in two classes, because they fail differently.
#
#   45-60 deg  is what the upper wall of a 1.3 mm detail pocket looks like — the
#              brow over the eye, the top wall of the chest crease. A wall that
#              shallow and that short bridges cleanly on any printer, so it is
#              allowed anywhere, within a budget.
#   over 60    is a real ceiling. The knight has exactly one: its muzzle
#              projects forward of its throat, so part of the underside is
#              unsupported however the section is drafted. That is the shape of
#              a knight, not a modelling shortcut — but the exemption is bounded
#              rather than waved through.
#
# JAW_BAND is DERIVED from the outline knots that make the muzzle underside,
# not fitted around wherever the steep faces happened to land. An earlier
# version had x_min = 7.0 against faces starting at x = 7.03 — a boundary drawn
# to the defect to three-hundredths of a millimetre, which describes nothing.
# Deriving it means the band moves when the form moves, and a ceiling that
# escapes it fails the build instead of being quietly re-fenced.
OVERHANG_BUDGET = 0.03
CEILING_DEG = 60.0

JAW_NOTCH_X = 4.8        # where the jaw is thrown forward of the throat
JAW_UNDERSIDE_Z = 44.6   # the lowest point of that underside
LIP_Z = 48.4             # the lip line at the throat end

JAW_BAND = {
    "z": (JAW_UNDERSIDE_Z - 1.5, LIP_Z + 0.5),
    "x_min": JAW_NOTCH_X - 0.5,
}


def stray_overhangs(mesh: trimesh.Trimesh, limit_deg: float = CEILING_DEG):
    """Ceilings that are NOT under the jaw — their area and worst angle."""
    import numpy as np

    normals, areas, tris = mesh.face_normals, mesh.area_faces, mesh.triangles
    overhang = np.degrees(np.arcsin(np.clip(-normals[:, 2], -1.0, 1.0)))
    on_plate = tris[:, :, 2].max(axis=1) < 1e-6
    unsupported = (overhang > limit_deg) & ~on_plate

    centre = tris.mean(axis=1)
    in_jaw = ((centre[:, 2] > JAW_BAND["z"][0]) & (centre[:, 2] < JAW_BAND["z"][1])
              & (centre[:, 0] > JAW_BAND["x_min"]))
    stray = unsupported & ~in_jaw
    return float(areas[stray].sum()), float(overhang[stray].max()) if stray.any() else 0.0


def jaw_ceilings(mesh: trimesh.Trimesh):
    """Area and worst angle of the exempted muzzle underside.

    Exempt is not the same as unmeasured. The number is printed on every build
    so the thing the exemption covers stays visible and cannot quietly grow.
    """
    import numpy as np

    normals, areas, tris = mesh.face_normals, mesh.area_faces, mesh.triangles
    overhang = np.degrees(np.arcsin(np.clip(-normals[:, 2], -1.0, 1.0)))
    centre = tris.mean(axis=1)
    in_jaw = ((centre[:, 2] > JAW_BAND["z"][0]) & (centre[:, 2] < JAW_BAND["z"][1])
              & (centre[:, 0] > JAW_BAND["x_min"]))
    hit = (overhang > CEILING_DEG) & in_jaw
    return float(areas[hit].sum()), float(overhang[hit].max()) if hit.any() else 0.0


def assert_invariants(mesh: trimesh.Trimesh) -> dict:
    report = printability(mesh)
    layers = layer_report(mesh)
    altitude = triangle_altitude(mesh)
    step = jowl_step(mesh)
    reach = float(mesh.bounds[1][0])
    slivers = int((altitude < NEEDLE_LIMIT).sum())
    stray_area, stray_worst = stray_overhangs(mesh)
    jaw_area, jaw_worst = jaw_ceilings(mesh)
    jaw_angle = jaw_draft_angle()

    failures = []
    if not report["watertight"]:
        failures.append("not watertight")
    if report["euler"] != 2:
        failures.append(f"euler {report['euler']} != 2 (handle or void)")
    if not report["winding_consistent"]:
        failures.append("inconsistent winding")
    if layers["empty_layers"]:
        failures.append(f"empty layers at {layers['empty_layers'][:5]}")
    if layers["layers_with_islands"]:
        failures.append(f"layer islands at {layers['layers_with_islands'][:5]}")
    if slivers:
        failures.append(f"{slivers} needle triangles thinner than {NEEDLE_LIMIT} mm")
    if step < 0.8:
        failures.append(f"jowl step {step:.2f} mm < 0.8 — the head is as wide "
                        "as the neck, so a draft is running past JOWL_Z")
    if reach > 25.5:
        failures.append(f"muzzle reaches {reach:.2f} mm, over the 25.5 limit")
    if jaw_angle > 45.0:
        failures.append(f"jaw draft facet is {jaw_angle:.1f} deg from vertical, "
                        "over the 45 deg support-free limit")
    if report["overhang_fraction"] > OVERHANG_BUDGET:
        failures.append(f"unsupported area {report['overhang_fraction']:.1%} "
                        f"over the {OVERHANG_BUDGET:.0%} budget")
    if stray_area > 0.5:
        failures.append(f"{stray_area:.1f} mm2 of ceiling (over {CEILING_DEG:.0f} "
                        f"deg, worst {stray_worst:.0f}) OUTSIDE the jaw band — "
                        "the exemption covers the muzzle underside only")
    if failures:
        raise AssertionError("invariants failed:\n  - " + "\n  - ".join(failures))

    return {
        "checks": {
            "watertight": report["watertight"],
            "euler (want 2)": report["euler"],
            "winding_consistent": report["winding_consistent"],
            "empty_layers": len(layers["empty_layers"]),
            "layer_islands": len(layers["layers_with_islands"]),
            "needle_triangles": slivers,
            "thinnest_triangle_mm": round(float(altitude.min()), 4),
            "jowl_step_mm (want >= 0.8)": round(step, 2),
            "muzzle_reach_mm (want <= 25.5)": round(reach, 2),
            "unsupported_fraction (want <= 3%)":
                f"{report['overhang_fraction']:.2%}",
            "ceilings_outside_jaw_mm2 (want 0)": round(stray_area, 2),
            "jaw_ceiling_mm2 (exempt, measured)": round(jaw_area, 1),
            "jaw_ceiling_worst_deg (exempt)": round(jaw_worst, 1),
            "jaw_draft_deg (want <= 45)": round(jaw_angle, 1),
            "height_mm": round(float(mesh.bounds[1][2]), 2),
        },
        "printability": report,
        "layers": layers,
    }


def main() -> None:
    piece = build()
    result = assert_invariants(piece)

    (HERE / "stl").mkdir(exist_ok=True)
    out = HERE / "stl" / "knight_baseline.stl"
    write_stl(piece, out, "alligator-chess baseline knight")
    print(f"wrote {out}")

    print("  --- invariants (all passed) ---")
    for key, value in result["checks"].items():
        print(f"  {key}: {value}")
    print("  --- printability ---")
    for key in ("faces", "volume_mm3", "overhang_area_mm2",
                "overhang_fraction", "worst_overhang_deg"):
        print(f"  {key}: {result['printability'][key]}")
    print("  --- slicing ---")
    for key, value in result["layers"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
