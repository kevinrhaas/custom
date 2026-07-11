#!/usr/bin/env python3
"""Generate sandstone lamp v6 with a smooth inner-rim lead-in.

V5 left the functional screw profile immediately below the otherwise-clean
9.46 mm finish plane. In a top view, the upper thread fragments projected onto
the hole edge as repeated dashed divots. V6 clears the connector away from the
66 mm bore for the upper 1.50 mm, creating a continuous cylindrical lead-in
before the screw profile begins. The lower 7.96 mm of engagement is preserved.
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

try:
    import manifold3d as manifold
except ImportError as error:  # pragma: no cover - exercised by end users
    raise SystemExit(
        "Lamp v6 dependencies are missing. Run: "
        "python3 -m pip install -r requirements-v4.txt"
    ) from error

import generate_sandstone_v4 as v4
import generate_sandstone_v5 as v5
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
    ensure_outward_orientation,
    format_number,
    mesh_bounds,
    normal_for_face,
    parse_formats,
    read_binary_stl,
    read_source_rings,
    write_scad_polyhedron,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_CONNECTOR = v4.DEFAULT_CONNECTOR
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "files" / "lamp" / "v6" / "connected"
DEFAULT_CONNECTOR_TOP_CLEARANCE = v5.DEFAULT_CONNECTOR_TOP_CLEARANCE
DEFAULT_SMOOTH_LEAD_IN_DEPTH = 1.50
DEFAULT_BORE_RADIAL_CLEARANCE = 0.05
DEFAULT_BORE_SEGMENTS = 120


@dataclass(frozen=True)
class LeadInReport:
    top_z_mm: float
    bottom_z_mm: float
    depth_mm: float
    nominal_bore_radius_mm: float
    connector_cut_radius_mm: float
    connector_intruding_vertices: int
    exact_dash_cap_vertices: int
    exact_dash_cap_faces: int
    dashed_zone_faces: int
    clean: bool


@dataclass(frozen=True)
class V6Report:
    lamp_body: MeshReport
    source_connector: MeshReport
    smoothed_connector: MeshReport
    final: MeshReport
    connector_top_clearance_mm: float
    smooth_lead_in: LeadInReport
    single_body_boolean_union: bool
    finish_plane: v5.FinishPlaneReport


def smooth_connector_lead_in(
    connector: Mesh,
    *,
    base: float,
    hole: float,
    depth: float,
    radial_clearance: float,
    top_clearance: float,
    bore_segments: int = DEFAULT_BORE_SEGMENTS,
) -> Mesh:
    """Remove upper thread projections from the visible 66 mm bore band."""
    if not (top_clearance > 0.0 and depth > top_clearance and depth < base):
        raise ValueError(
            "Lead-in depth must be below base and greater than top clearance"
        )
    if radial_clearance <= 0.0 or bore_segments < 24:
        raise ValueError("Bore clearance must be positive and needs at least 24 segments")

    bore_radius = hole / 2.0 + radial_clearance
    # Extend above the floor slightly so the subtraction cannot leave a
    # coincident cap at z=base.
    cutter = manifold.Manifold.cylinder(
        depth + 0.02,
        bore_radius,
        bore_radius,
        bore_segments,
        False,
    ).translate((0.0, 0.0, base - depth))
    cleared = manifold.Manifold.batch_boolean(
        [v4.to_manifold(connector), cutter], manifold.OpType.Subtract
    )
    if cleared.status() != manifold.Error.NoError or cleared.is_empty():
        raise RuntimeError(f"Smooth-bore subtraction failed: {cleared.status()}")
    cleared_mesh = v4.weld_exact_and_remove_degenerate(v4.from_manifold(cleared))
    cleared_report = ensure_outward_orientation(cleared_mesh)
    if not cleared_report.watertight:
        raise RuntimeError("Lead-in-cleared connector is not watertight")

    # Retain v5's separation between the connector cap and visible finish
    # plane, eliminating coplanar Boolean fragments on the horizontal floor.
    return v5.trim_connector_top(cleared_mesh, base, top_clearance)


def inspect_lead_in(
    mesh: Mesh,
    *,
    base: float,
    hole: float,
    depth: float,
    radial_clearance: float,
    tolerance: float = 1e-4,
) -> LeadInReport:
    bottom = base - depth
    nominal_radius = hole / 2.0
    # The 120-sided generated bore has vertices at nominal radius and chords
    # just inside it. A 0.05 mm threshold distinguishes actual thread/divot
    # vertices from that intentional polygonal approximation.
    intrusion_radius = nominal_radius - 0.05
    intruding_vertices = sum(
        1
        for x, y, z in mesh.points
        if bottom + tolerance < z < base - tolerance
        and math.hypot(x, y) < intrusion_radius
    )

    dash_cap_z = 9.066002
    dash_radius_min = nominal_radius - 0.75
    dash_radius_max = nominal_radius - 0.30
    exact_dash_vertices = sum(
        1
        for x, y, z in mesh.points
        if abs(z - dash_cap_z) <= tolerance
        and dash_radius_min < math.hypot(x, y) < dash_radius_max
    )
    exact_dash_faces = 0
    for face in mesh.faces:
        points = [mesh.points[index] for index in face]
        if (
            all(abs(point[2] - dash_cap_z) <= tolerance for point in points)
            and min(math.hypot(point[0], point[1]) for point in points)
            > dash_radius_min
            and max(math.hypot(point[0], point[1]) for point in points)
            < dash_radius_max
        ):
            exact_dash_faces += 1

    # This is the exact zone occupied by the repeated v5 dashes. Assert that
    # no surface triangles remain there in v6.
    dashed_zone_faces = 0
    dashed_radius = nominal_radius - 0.30
    dashed_z_min = max(bottom + tolerance, 8.48)
    dashed_z_max = min(base - tolerance, 9.08)
    if dashed_z_min < dashed_z_max:
        for face in mesh.faces:
            points = [mesh.points[index] for index in face]
            if (
                min(point[2] for point in points) >= dashed_z_min
                and max(point[2] for point in points) <= dashed_z_max
                and max(math.hypot(point[0], point[1]) for point in points)
                < dashed_radius
            ):
                dashed_zone_faces += 1

    clean = (
        intruding_vertices == 0
        and exact_dash_vertices == 0
        and exact_dash_faces == 0
        and dashed_zone_faces == 0
    )
    return LeadInReport(
        top_z_mm=base,
        bottom_z_mm=bottom,
        depth_mm=depth,
        nominal_bore_radius_mm=nominal_radius,
        connector_cut_radius_mm=nominal_radius + radial_clearance,
        connector_intruding_vertices=intruding_vertices,
        exact_dash_cap_vertices=exact_dash_vertices,
        exact_dash_cap_faces=exact_dash_faces,
        dashed_zone_faces=dashed_zone_faces,
        clean=clean,
    )


def build_v6(
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
    source: Path,
    connector: Path,
) -> tuple[Mesh, dict[str, float | int | bool], V6Report]:
    body, construction, body_validation = v4.build_v4(
        height=height,
        layers=layers,
        wall=wall,
        base=base,
        hole=hole,
        top_lip_segments=top_lip_segments,
        source=source,
        connector=None,
    )
    source_connector = read_binary_stl(connector)
    source_connector_report = ensure_outward_orientation(source_connector)
    if not source_connector_report.watertight:
        raise ValueError("V6 requires the prepared manifold connector")

    smoothed_connector = smooth_connector_lead_in(
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
        raise RuntimeError("Smoothed connector top clearance is incorrect")

    final = v4.boolean_union(body, smoothed_connector)
    final_report = ensure_outward_orientation(final)
    expected_finish_faces = int(construction["points_per_ring"]) * 2
    finish = v5.inspect_finish_plane(
        final, z=base, expected_faces=expected_finish_faces
    )
    lead_in = inspect_lead_in(
        final,
        base=base,
        hole=hole,
        depth=smooth_lead_in_depth,
        radial_clearance=bore_radial_clearance,
    )
    if not final_report.watertight or not finish.clean or not lead_in.clean:
        raise RuntimeError(
            "V6 final validation failed: "
            f"boundary={final_report.boundary_edges}, "
            f"nonmanifold={final_report.nonmanifold_edges}, "
            f"finish_clean={finish.clean}, "
            f"lead_intrusions={lead_in.connector_intruding_vertices}, "
            f"dash_cap_faces={lead_in.exact_dash_cap_faces}, "
            f"dashed_zone_faces={lead_in.dashed_zone_faces}"
        )

    construction.update(
        {
            "connector_boolean_union": True,
            "connector_top_clearance_mm": connector_top_clearance,
            "smooth_inner_lead_in_depth_mm": smooth_lead_in_depth,
            "smooth_inner_lead_in_bottom_z_mm": base - smooth_lead_in_depth,
            "connector_bore_cut_radius_mm": hole / 2.0 + bore_radial_clearance,
            "connector_geometry_on_finish_plane": False,
            "connector_geometry_in_smooth_lead_in": False,
            "continuous_interior_floor": True,
        }
    )
    return final, construction, V6Report(
        lamp_body=body_validation.final,
        source_connector=source_connector_report,
        smoothed_connector=smoothed_report,
        final=final_report,
        connector_top_clearance_mm=connector_top_clearance,
        smooth_lead_in=lead_in,
        single_body_boolean_union=True,
        finish_plane=finish,
    )


def write_binary_stl_v6(path: Path, mesh: Mesh) -> None:
    with path.open("wb") as handle:
        header = b"Illinois Sandstone Lamp v6 - smooth inner-rim lead-in"
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
    yield '  <metadata name="Title">Illinois Sandstone Lamp v6</metadata>\n'
    yield '  <metadata name="Application">generate_sandstone_v6.py</metadata>\n'
    yield '  <resources>\n'
    yield '    <object id="1" type="model" name="Connected lamp v6 - smooth inner rim">\n'
    yield '      <mesh>\n        <vertices>\n'
    for x, y, z in mesh.points:
        yield f'          <vertex x="{x:.7f}" y="{y:.7f}" z="{z:.7f}"/>\n'
    yield '        </vertices>\n        <triangles>\n'
    for a, b, c in mesh.faces:
        yield f'          <triangle v1="{a}" v2="{b}" v3="{c}"/>\n'
    yield '        </triangles>\n      </mesh>\n    </object>\n'
    yield '  </resources>\n  <build>\n    <item objectid="1" printable="1"/>\n  </build>\n</model>\n'


def write_3mf_v6(path: Path, mesh: Mesh) -> None:
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


def write_scad_v6(
    path: Path,
    mesh: Mesh,
    parameters: Parameters,
    top_clearance: float,
    lead_in_depth: float,
) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "// Illinois Sandstone Lamp v6\n"
            "// Generated by generate_sandstone_v6.py\n"
            "// Smooth 66 mm inner-rim lead-in above the connector thread.\n"
            f"// height={parameters.height} layers={parameters.layers} "
            f"wall={parameters.wall} base={parameters.base} hole={parameters.hole}\n"
            f"// connector_top_clearance={top_clearance}\n"
            f"// smooth_lead_in_depth={lead_in_depth}\n\n"
            "/* [Height Fine-Tuning] */\n"
            "fine_tune_scale = 1.0;  // [0.90:0.001:1.10]\n\n"
            "scale([1, 1, fine_tune_scale])\n"
        )
        write_scad_polyhedron(handle, mesh)


def write_report(
    path: Path,
    parameters: Parameters,
    construction: dict[str, float | int | bool],
    report: V6Report,
    outputs: Sequence[Path],
) -> None:
    payload = {
        "generator": "generate_sandstone_v6.py",
        "parameters": asdict(parameters),
        "construction": construction,
        "validation": asdict(report),
        "outputs": [output.name for output in outputs],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate sandstone lamp v6 with a smooth inner-rim lead-in",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--height", type=float, default=DEFAULT_HEIGHT)
    parser.add_argument("--layers", type=int, default=None)
    parser.add_argument("--wall", type=float, default=DEFAULT_WALL)
    parser.add_argument("--base", type=float, default=DEFAULT_BASE)
    parser.add_argument("--hole", type=float, default=DEFAULT_HOLE)
    parser.add_argument(
        "--top-lip-segments", type=int, default=DEFAULT_TOP_LIP_SEGMENTS
    )
    parser.add_argument(
        "--connector-top-clearance",
        type=float,
        default=DEFAULT_CONNECTOR_TOP_CLEARANCE,
    )
    parser.add_argument(
        "--smooth-lead-in-depth",
        type=float,
        default=DEFAULT_SMOOTH_LEAD_IN_DEPTH,
    )
    parser.add_argument(
        "--bore-radial-clearance",
        type=float,
        default=DEFAULT_BORE_RADIAL_CLEARANCE,
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--connector", type=Path, default=DEFAULT_CONNECTOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--name", default=None)
    parser.add_argument(
        "--formats",
        type=parse_formats,
        default=parse_formats("stl,3mf,scad,json"),
        help="comma-separated output formats: stl,3mf,scad,json",
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
    final, construction, report = build_v6(
        height=args.height,
        layers=layers,
        wall=args.wall,
        base=args.base,
        hole=args.hole,
        top_lip_segments=args.top_lip_segments,
        connector_top_clearance=args.connector_top_clearance,
        smooth_lead_in_depth=args.smooth_lead_in_depth,
        bore_radial_clearance=args.bore_radial_clearance,
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
        f"illinois_sandstone_v6_{format_number(args.height)}mm_"
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
            write_binary_stl_v6(path, final)
        elif output_format == "3mf":
            write_3mf_v6(path, final)
        elif output_format == "scad":
            write_scad_v6(
                path,
                final,
                parameters,
                args.connector_top_clearance,
                args.smooth_lead_in_depth,
            )
        outputs.append(path)
    if "json" in args.formats:
        path = output_dir / f"{basename}.report.json"
        write_report(path, parameters, construction, report, outputs)
        outputs.append(path)

    mesh_report = report.final
    finish = report.finish_plane
    lead_in = report.smooth_lead_in
    print("Illinois Sandstone Lamp v6")
    print(f"  Source rings retained: {len(source_rings)} / {len(source_rings)}")
    print(f"  Output rings:          {layers}")
    print(f"  Vertices / faces:      {mesh_report.vertices:,} / {mesh_report.faces:,}")
    print("  Size (mm):             " + " x ".join(f"{v:.3f}" for v in mesh_report.size_mm))
    print(f"  Boundary edges:        {mesh_report.boundary_edges}")
    print(f"  Non-manifold edges:    {mesh_report.nonmanifold_edges}")
    print(f"  Degenerate faces:      {mesh_report.degenerate_faces}")
    print(f"  Components:            {mesh_report.connected_components}")
    print(f"  Finish-plane faces:    {finish.faces} clean large triangles")
    print(f"  Smooth lead-in depth:  {lead_in.depth_mm:.3f} mm")
    print(f"  Lead-in intrusions:    {lead_in.connector_intruding_vertices}")
    print(f"  Exact dash-cap faces:  {lead_in.exact_dash_cap_faces}")
    print(f"  Dashed-zone faces:     {lead_in.dashed_zone_faces}")
    print(f"  Watertight:            {'YES' if mesh_report.watertight else 'NO'}")
    for output in outputs:
        print(f"  Wrote: {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
