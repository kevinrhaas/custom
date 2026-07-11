#!/usr/bin/env python3
"""Generate sandstone lamp v7 with a natural inward top transition.

V7 keeps the clean v6 connector and interior, then eases the organic outer
profile inward by 1.5 mm over the 8 mm immediately below the existing 1 mm
rounded lip.  A raised-cosine curve has zero slope at both ends, producing a
gentle shoulder without a kink or a difficult overhang.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import struct
import sys
from typing import Iterable, Sequence
from zipfile import ZIP_DEFLATED, ZipFile

import generate_sandstone_v4 as v4
import generate_sandstone_v5 as v5
import generate_sandstone_v6 as v6
from generate_sandstone_v2 import (
    DEFAULT_BASE,
    DEFAULT_HEIGHT,
    DEFAULT_HOLE,
    DEFAULT_SOURCE,
    DEFAULT_TOP_LIP_SEGMENTS,
    DEFAULT_WALL,
    Mesh,
    MeshReport,
    Parameters,
    Ring,
    build_lamp_mesh,
    ensure_outward_orientation,
    format_number,
    mesh_bounds,
    normal_for_face,
    read_binary_stl,
    read_source_rings,
    scale_rings_to_height,
    source_preserving_resample,
    write_scad_polyhedron,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_CONNECTOR = v6.DEFAULT_CONNECTOR
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "files" / "lamp" / "v7" / "connected"
DEFAULT_TOP_TAPER_HEIGHT = 8.0
DEFAULT_TOP_TAPER_INSET = 1.5
PRINTABILITY_LAYER_HEIGHT = 0.16
PRINTABILITY_LINE_WIDTH = 0.40


@dataclass(frozen=True)
class TopTaperReport:
    curve: str
    crest_z_mm: float
    rounded_lip_join_z_mm: float
    organic_profile_height_mm: float
    taper_start_z_mm: float
    taper_height_mm: float
    radial_inset_mm: float
    total_transition_height_to_crest_mm: float
    affected_outer_rings: int
    top_outer_radius_before_min_mm: float
    top_outer_radius_before_max_mm: float
    top_outer_radius_after_min_mm: float
    top_outer_radius_after_max_mm: float
    minimum_inner_rim_radius_mm: float
    minimum_inner_rim_diameter_mm: float
    maximum_slope_mm_per_mm: float
    maximum_angle_from_vertical_degrees: float
    validation_layer_height_mm: float
    maximum_radial_shift_per_layer_mm: float
    validation_line_width_mm: float
    minimum_line_overlap_percent: float
    last_organic_segment_height_mm: float
    maximum_last_segment_slope_mm_per_mm: float
    maximum_last_segment_angle_from_vertical_degrees: float
    maximum_last_segment_radial_shift_per_layer_mm: float
    endpoint_tangent_start: float
    endpoint_tangent_end: float
    printable_without_support: bool


@dataclass(frozen=True)
class V7Report:
    lamp_body: MeshReport
    source_connector: MeshReport
    smoothed_connector: MeshReport
    final: MeshReport
    connector_top_clearance_mm: float
    smooth_lead_in: v6.LeadInReport
    finish_plane: v5.FinishPlaneReport
    top_taper: TopTaperReport
    single_body_boolean_union: bool
    geometry_only_3mf: bool


def raised_cosine(amount: float) -> float:
    """Monotone 0..1 easing with zero slope at both endpoints."""
    amount = min(1.0, max(0.0, amount))
    return 0.5 * (1.0 - math.cos(math.pi * amount))


def taper_inset_at_z(
    z: float,
    *,
    lip_join_z: float,
    taper_height: float,
    radial_inset: float,
) -> float:
    start_z = lip_join_z - taper_height
    if z <= start_z:
        return 0.0
    if z >= lip_join_z:
        return radial_inset
    amount = (z - start_z) / taper_height
    return radial_inset * raised_cosine(amount)


def apply_top_taper(
    outer_rings: Sequence[Ring],
    *,
    height: float,
    wall: float,
    taper_height: float,
    radial_inset: float,
) -> tuple[list[Ring], TopTaperReport]:
    """Ease only the outer control rings inward before wall construction."""
    lip_radius = wall / 2.0
    lip_join_z = height - lip_radius
    taper_start_z = lip_join_z - taper_height
    if taper_height <= 0.0 or radial_inset <= 0.0:
        raise ValueError("Top taper height and inset must be positive")
    if taper_start_z <= 0.0:
        raise ValueError("Top taper is too tall for the requested lamp")
    top_z_values = [point[2] for point in outer_rings[-1]]
    if max(abs(z - lip_join_z) for z in top_z_values) > 1e-5:
        raise ValueError(
            "The organic profile must end at the rounded-lip join height"
        )

    top_before = [math.hypot(x, y) for x, y, _ in outer_rings[-1]]
    if min(top_before) <= radial_inset + wall:
        raise ValueError("Top taper inset is too large for the lamp radius")

    tapered: list[Ring] = []
    affected_rings = 0
    for ring in outer_rings:
        changed = False
        output_ring: Ring = []
        for x, y, z in ring:
            inset = taper_inset_at_z(
                z,
                lip_join_z=lip_join_z,
                taper_height=taper_height,
                radial_inset=radial_inset,
            )
            if inset <= 0.0:
                output_ring.append((x, y, z))
                continue
            radius = math.hypot(x, y)
            scale = (radius - inset) / radius
            output_ring.append((x * scale, y * scale, z))
            changed = True
        affected_rings += int(changed)
        tapered.append(output_ring)

    top_after = [math.hypot(x, y) for x, y, _ in tapered[-1]]
    minimum_inner_radius = min(top_after) - wall
    maximum_slope = radial_inset * math.pi / (2.0 * taper_height)
    maximum_layer_shift = maximum_slope * PRINTABILITY_LAYER_HEIGHT
    last_segment_height = min(point[2] for point in tapered[-1]) - max(
        point[2] for point in tapered[-2]
    )
    if last_segment_height <= PRINTABILITY_LAYER_HEIGHT * 3.0:
        raise ValueError(
            "The last organic ring is too close to the rounded-lip join"
        )
    last_segment_slopes: list[float] = []
    for lower, upper in zip(tapered[-2], tapered[-1]):
        delta_z = upper[2] - lower[2]
        if delta_z <= 0.0:
            raise ValueError("Top organic rings overlap after height scaling")
        delta_radius = abs(
            math.hypot(upper[0], upper[1]) - math.hypot(lower[0], lower[1])
        )
        last_segment_slopes.append(delta_radius / delta_z)
    maximum_last_slope = max(last_segment_slopes)
    maximum_last_layer_shift = maximum_last_slope * PRINTABILITY_LAYER_HEIGHT
    governing_layer_shift = max(maximum_layer_shift, maximum_last_layer_shift)
    overlap = 100.0 * (1.0 - governing_layer_shift / PRINTABILITY_LINE_WIDTH)
    angle = math.degrees(math.atan(maximum_slope))
    last_segment_angle = math.degrees(math.atan(maximum_last_slope))
    printable = governing_layer_shift <= PRINTABILITY_LINE_WIDTH / 2.0

    report = TopTaperReport(
        curve="raised cosine",
        crest_z_mm=height,
        rounded_lip_join_z_mm=lip_join_z,
        organic_profile_height_mm=lip_join_z,
        taper_start_z_mm=taper_start_z,
        taper_height_mm=taper_height,
        radial_inset_mm=radial_inset,
        total_transition_height_to_crest_mm=taper_height + lip_radius,
        affected_outer_rings=affected_rings,
        top_outer_radius_before_min_mm=min(top_before),
        top_outer_radius_before_max_mm=max(top_before),
        top_outer_radius_after_min_mm=min(top_after),
        top_outer_radius_after_max_mm=max(top_after),
        minimum_inner_rim_radius_mm=minimum_inner_radius,
        minimum_inner_rim_diameter_mm=minimum_inner_radius * 2.0,
        maximum_slope_mm_per_mm=maximum_slope,
        maximum_angle_from_vertical_degrees=angle,
        validation_layer_height_mm=PRINTABILITY_LAYER_HEIGHT,
        maximum_radial_shift_per_layer_mm=maximum_layer_shift,
        validation_line_width_mm=PRINTABILITY_LINE_WIDTH,
        minimum_line_overlap_percent=overlap,
        last_organic_segment_height_mm=last_segment_height,
        maximum_last_segment_slope_mm_per_mm=maximum_last_slope,
        maximum_last_segment_angle_from_vertical_degrees=last_segment_angle,
        maximum_last_segment_radial_shift_per_layer_mm=maximum_last_layer_shift,
        endpoint_tangent_start=0.0,
        endpoint_tangent_end=0.0,
        printable_without_support=printable,
    )
    return tapered, report


def build_v7(
    *,
    height: float,
    layers: int,
    wall: float,
    base: float,
    hole: float,
    top_lip_segments: int,
    connector_top_clearance: float,
    smooth_lead_in_depth: float,
    bore_radial_clearance: float,
    top_taper_height: float,
    top_taper_inset: float,
    source: Path,
    connector: Path,
) -> tuple[Mesh, dict[str, object], V7Report]:
    source_rings = read_source_rings(source)
    preserved = source_preserving_resample(source_rings, layers)
    # Reserve the half-round lip's own height before scaling the sandstone
    # profile.  Older versions scaled the source all the way to the crest and
    # then moved its last ring down to the lip join, leaving a nearly collapsed
    # final segment on the 120 mm model.  This keeps every source XY ring while
    # giving the approach to the lip a normal, printable vertical interval.
    lip_radius = wall / 2.0
    organic_profile_height = height - lip_radius
    outer_rings = scale_rings_to_height(preserved, organic_profile_height)
    tapered_rings, taper_report = apply_top_taper(
        outer_rings,
        height=height,
        wall=wall,
        taper_height=top_taper_height,
        radial_inset=top_taper_inset,
    )
    # build_lamp_mesh derives the final crest from the last input ring and then
    # places that ring at H-wall/2. Supply a temporary height anchor; the
    # builder returns it to the already-validated organic profile height.
    body_rings = [list(ring) for ring in tapered_rings]
    body_rings[-1] = [(x, y, height) for x, y, _ in body_rings[-1]]
    body, construction = build_lamp_mesh(
        body_rings, wall, base, hole, top_lip_segments
    )
    body_report = ensure_outward_orientation(body)
    if not body_report.watertight:
        raise RuntimeError("V7 tapered lamp body is not watertight")

    source_connector = read_binary_stl(connector)
    source_connector_report = ensure_outward_orientation(source_connector)
    if not source_connector_report.watertight:
        raise ValueError("V7 requires the prepared manifold connector")
    smoothed_connector = v6.smooth_connector_lead_in(
        source_connector,
        base=base,
        hole=hole,
        depth=smooth_lead_in_depth,
        radial_clearance=bore_radial_clearance,
        top_clearance=connector_top_clearance,
    )
    smoothed_report = ensure_outward_orientation(smoothed_connector)
    expected_connector_top = base - connector_top_clearance
    actual_connector_top = mesh_bounds(smoothed_connector)[1][2]
    if abs(actual_connector_top - expected_connector_top) > 1e-5:
        raise RuntimeError("V7 connector top clearance is incorrect")

    final = v4.boolean_union(body, smoothed_connector)
    final_report = ensure_outward_orientation(final)
    v4.to_manifold(final)  # also verifies consistently oriented topology
    finish = v5.inspect_finish_plane(
        final,
        z=base,
        expected_faces=int(construction["points_per_ring"]) * 2,
    )
    lead_in = v6.inspect_lead_in(
        final,
        base=base,
        hole=hole,
        depth=smooth_lead_in_depth,
        radial_clearance=bore_radial_clearance,
    )
    minimum_required_rim_radius = hole / 2.0 + wall
    if taper_report.minimum_inner_rim_radius_mm < minimum_required_rim_radius:
        raise RuntimeError("Top taper narrows the rim too close to the base bore")
    if (
        not final_report.watertight
        or not finish.clean
        or not lead_in.clean
        or not taper_report.printable_without_support
    ):
        raise RuntimeError(
            "V7 final validation failed: "
            f"watertight={final_report.watertight}, "
            f"finish_clean={finish.clean}, lead_clean={lead_in.clean}, "
            f"taper_printable={taper_report.printable_without_support}"
        )

    construction.update(
        {
            "source_rings_retained": len(source_rings),
            "connector_boolean_union": True,
            "connector_top_clearance_mm": connector_top_clearance,
            "smooth_inner_lead_in_depth_mm": smooth_lead_in_depth,
            "smooth_inner_lead_in_bottom_z_mm": base - smooth_lead_in_depth,
            "connector_bore_cut_radius_mm": hole / 2.0 + bore_radial_clearance,
            "connector_geometry_on_finish_plane": False,
            "connector_geometry_in_smooth_lead_in": False,
            "continuous_interior_floor": True,
            "top_taper_curve": taper_report.curve,
            "top_taper_height_mm": top_taper_height,
            "top_taper_inset_mm": top_taper_inset,
            "top_taper_start_z_mm": taper_report.taper_start_z_mm,
            "organic_profile_height_mm": organic_profile_height,
            "last_organic_segment_height_mm": (
                taper_report.last_organic_segment_height_mm
            ),
            "top_transition_total_height_mm": (
                taper_report.total_transition_height_to_crest_mm
            ),
            "geometry_only_3mf": True,
        }
    )
    return final, construction, V7Report(
        lamp_body=body_report,
        source_connector=source_connector_report,
        smoothed_connector=smoothed_report,
        final=final_report,
        connector_top_clearance_mm=connector_top_clearance,
        smooth_lead_in=lead_in,
        finish_plane=finish,
        top_taper=taper_report,
        single_body_boolean_union=True,
        geometry_only_3mf=True,
    )


def write_binary_stl_v7(path: Path, mesh: Mesh) -> None:
    with path.open("wb") as handle:
        header = b"Illinois Sandstone Lamp v7 - gentle natural top transition"
        handle.write(header.ljust(80, b"\0")[:80])
        handle.write(struct.pack("<I", len(mesh.faces)))
        for face in mesh.faces:
            normal = normal_for_face(mesh, face)
            values = normal + tuple(
                coordinate
                for vertex_index in face
                for coordinate in mesh.points[vertex_index]
            )
            handle.write(struct.pack("<12fH", *values, 0))


def model_xml(mesh: Mesh) -> Iterable[str]:
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    yield '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
    yield '  <metadata name="Title">Illinois Sandstone Lamp v7</metadata>\n'
    yield '  <metadata name="Application">generate_sandstone_v7.py</metadata>\n'
    yield '  <metadata name="Description">Geometry only - no slicer settings</metadata>\n'
    yield '  <resources>\n'
    yield '    <object id="1" type="model" name="Connected lamp v7 - gentle top transition">\n'
    yield '      <mesh>\n        <vertices>\n'
    for x, y, z in mesh.points:
        yield f'          <vertex x="{x:.7f}" y="{y:.7f}" z="{z:.7f}"/>\n'
    yield '        </vertices>\n        <triangles>\n'
    for a, b, c in mesh.faces:
        yield f'          <triangle v1="{a}" v2="{b}" v3="{c}"/>\n'
    yield '        </triangles>\n      </mesh>\n    </object>\n'
    yield '  </resources>\n  <build>\n    <item objectid="1" printable="1"/>\n  </build>\n</model>\n'


def write_3mf_v7(path: Path, mesh: Mesh) -> None:
    """Write a geometry-only 3MF with no Flash Studio process metadata."""
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Override PartName="/3D/3dmodel.model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>
"""
    relationships = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
"""
    with ZipFile(path, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", relationships)
        archive.writestr("3D/3dmodel.model", "".join(model_xml(mesh)))


def write_scad_v7(
    path: Path,
    mesh: Mesh,
    parameters: Parameters,
    taper_height: float,
    taper_inset: float,
) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "// Illinois Sandstone Lamp v7\n"
            "// Generated by generate_sandstone_v7.py\n"
            "// Gentle raised-cosine transition into the rounded top lip.\n"
            f"// height={parameters.height} layers={parameters.layers} "
            f"wall={parameters.wall} base={parameters.base} hole={parameters.hole}\n"
            f"// top_taper_height={taper_height}\n"
            f"// top_taper_inset={taper_inset}\n\n"
            "/* [Height Fine-Tuning] */\n"
            "fine_tune_scale = 1.0;  // [0.90:0.001:1.10]\n\n"
            "scale([1, 1, fine_tune_scale])\n"
        )
        write_scad_polyhedron(handle, mesh)


def write_report(
    path: Path,
    parameters: Parameters,
    construction: dict[str, object],
    report: V7Report,
    outputs: Sequence[Path],
) -> None:
    payload = {
        "generator": "generate_sandstone_v7.py",
        "parameters": asdict(parameters),
        "construction": construction,
        "validation": asdict(report),
        "outputs": [output.name for output in outputs],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = v6.build_argument_parser()
    parser.description = (
        "Generate sandstone lamp v7 with a gentle natural top transition"
    )
    parser.set_defaults(output_dir=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--top-taper-height",
        type=float,
        default=DEFAULT_TOP_TAPER_HEIGHT,
        help="vertical taper span below the rounded lip in mm",
    )
    parser.add_argument(
        "--top-taper-inset",
        type=float,
        default=DEFAULT_TOP_TAPER_INSET,
        help="additional radial inset at the top in mm",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    source = args.source.resolve()
    connector = args.connector.resolve()
    source_rings = read_source_rings(source)
    layers = args.layers
    if layers is None:
        layers = max(
            len(source_rings), int(round(len(source_rings) * args.height / 120.0))
        )
    final, construction, report = build_v7(
        height=args.height,
        layers=layers,
        wall=args.wall,
        base=args.base,
        hole=args.hole,
        top_lip_segments=args.top_lip_segments,
        connector_top_clearance=args.connector_top_clearance,
        smooth_lead_in_depth=args.smooth_lead_in_depth,
        bore_radial_clearance=args.bore_radial_clearance,
        top_taper_height=args.top_taper_height,
        top_taper_inset=args.top_taper_inset,
        source=source,
        connector=connector,
    )

    def display(path: Path) -> str:
        try:
            return str(path.relative_to(PROJECT_DIR))
        except ValueError:
            return str(path)

    parameters = Parameters(
        height=args.height,
        layers=layers,
        wall=args.wall,
        base=args.base,
        hole=args.hole,
        top_lip_segments=args.top_lip_segments,
        source=display(source),
        connector=display(connector),
    )
    basename = args.name or (
        f"illinois_sandstone_v7_{format_number(args.height)}mm_"
        f"{layers}L_wall{format_number(args.wall)}_"
        f"base{format_number(args.base)}_hole{format_number(args.hole)}_connector80"
    )
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for output_format in args.formats:
        if output_format == "json":
            continue
        path = output_dir / f"{basename}.{output_format}"
        if output_format == "stl":
            write_binary_stl_v7(path, final)
        elif output_format == "3mf":
            write_3mf_v7(path, final)
        elif output_format == "scad":
            write_scad_v7(
                path,
                final,
                parameters,
                args.top_taper_height,
                args.top_taper_inset,
            )
        outputs.append(path)
    if "json" in args.formats:
        path = output_dir / f"{basename}.report.json"
        write_report(path, parameters, construction, report, outputs)
        outputs.append(path)

    mesh_report = report.final
    taper = report.top_taper
    print("Illinois Sandstone Lamp v7")
    print(f"  Source rings retained: {len(source_rings)} / {len(source_rings)}")
    print(f"  Output rings:          {layers}")
    print(f"  Vertices / faces:      {mesh_report.vertices:,} / {mesh_report.faces:,}")
    print("  Size (mm):             " + " x ".join(f"{v:.3f}" for v in mesh_report.size_mm))
    print(f"  Top taper:             {taper.taper_height_mm:.2f} mm high")
    print(f"  Top radial inset:      {taper.radial_inset_mm:.2f} mm")
    print(f"  Transition to crest:  {taper.total_transition_height_to_crest_mm:.2f} mm")
    print(f"  Taper angle:           {taper.maximum_angle_from_vertical_degrees:.2f} degrees")
    print(f"  Added shift / layer:  {taper.maximum_radial_shift_per_layer_mm:.4f} mm")
    print(f"  Final ring interval:  {taper.last_organic_segment_height_mm:.4f} mm")
    print(
        "  Worst top shift/layer:"
        f" {max(taper.maximum_radial_shift_per_layer_mm, taper.maximum_last_segment_radial_shift_per_layer_mm):.4f} mm"
    )
    print(f"  Boundary edges:        {mesh_report.boundary_edges}")
    print(f"  Non-manifold edges:    {mesh_report.nonmanifold_edges}")
    print(f"  Degenerate faces:      {mesh_report.degenerate_faces}")
    print(f"  Components:            {mesh_report.connected_components}")
    print(f"  Finish-plane clean:    {'YES' if report.finish_plane.clean else 'NO'}")
    print(f"  Smooth lead-in clean:  {'YES' if report.smooth_lead_in.clean else 'NO'}")
    print(f"  Watertight:            {'YES' if mesh_report.watertight else 'NO'}")
    print("  3MF contents:          geometry only")
    for output in outputs:
        print(f"  Wrote: {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
