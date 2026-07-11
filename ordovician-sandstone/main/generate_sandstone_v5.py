#!/usr/bin/env python3
"""Generate Illinois sandstone lamp v5 with a clean interior finish plane.

V4 made the connected lamp manifold, but the connector's top was coincident
with the 9.46 mm lamp floor. Its many tiny Boolean fragments remained visible
as dark dashed arcs in slicer previews. V5 clips only the top 0.20 mm from the
connector before unioning it below the original lamp floor. The visible floor
therefore remains the generator's 240 large, flat triangles with no connector
triangulation or micro-slivers on that plane.
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
        "Lamp v5 dependencies are missing. Run: "
        "python3 -m pip install -r requirements-v4.txt"
    ) from error

import generate_sandstone_v4 as v4
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
    cross,
    dot,
    ensure_outward_orientation,
    format_number,
    mesh_bounds,
    normal_for_face,
    parse_formats,
    read_binary_stl,
    read_source_rings,
    subtract,
    write_scad_polyhedron,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_CONNECTOR = v4.DEFAULT_CONNECTOR
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "files" / "lamp" / "v5" / "connected"
DEFAULT_CONNECTOR_TOP_CLEARANCE = 0.20
FINISH_AREA_THRESHOLD_MM2 = 0.01


@dataclass(frozen=True)
class FinishPlaneReport:
    z_mm: float
    faces: int
    expected_faces: int
    upward_faces: int
    downward_faces: int
    minimum_triangle_area_mm2: float
    micro_triangles: int
    minimum_radius_mm: float
    maximum_radius_mm: float
    clean: bool


@dataclass(frozen=True)
class V5Report:
    lamp_body: MeshReport
    source_connector: MeshReport
    trimmed_connector: MeshReport
    final: MeshReport
    connector_top_clearance_mm: float
    trimmed_connector_top_z_mm: float
    single_body_boolean_union: bool
    finish_plane: FinishPlaneReport


def trim_connector_top(connector: Mesh, base: float, clearance: float) -> Mesh:
    """Clip the connector below the visible lamp floor by ``clearance`` mm."""
    if not (0.0 < clearance < base):
        raise ValueError("Connector top clearance must be greater than 0 and below base")
    minimums, maximums = mesh_bounds(connector)
    clip_top = base - clearance
    margin = 2.0
    size_x = maximums[0] - minimums[0] + 2.0 * margin
    size_y = maximums[1] - minimums[1] + 2.0 * margin
    clip = manifold.Manifold.cube((size_x, size_y, clip_top), False).translate(
        (minimums[0] - margin, minimums[1] - margin, 0.0)
    )
    trimmed = manifold.Manifold.batch_boolean(
        [v4.to_manifold(connector), clip], manifold.OpType.Intersect
    )
    if trimmed.status() != manifold.Error.NoError or trimmed.is_empty():
        raise RuntimeError(f"Connector top clipping failed: {trimmed.status()}")
    mesh = v4.weld_exact_and_remove_degenerate(v4.from_manifold(trimmed))
    report = ensure_outward_orientation(mesh)
    if not report.watertight:
        raise RuntimeError("Clipped connector is not watertight")
    return mesh


def inspect_finish_plane(
    mesh: Mesh,
    *,
    z: float,
    expected_faces: int,
    tolerance: float = 1e-5,
) -> FinishPlaneReport:
    areas: list[float] = []
    upward = 0
    downward = 0
    radii: list[float] = []
    for face in mesh.faces:
        points = [mesh.points[index] for index in face]
        if not all(abs(point[2] - z) <= tolerance for point in points):
            continue
        normal = cross(subtract(points[1], points[0]), subtract(points[2], points[0]))
        area = 0.5 * math.sqrt(dot(normal, normal))
        areas.append(area)
        radii.extend(math.hypot(x, y) for x, y, _ in points)
        if normal[2] > 0:
            upward += 1
        else:
            downward += 1

    if not areas:
        raise RuntimeError("No triangles were found on the interior finish plane")
    micro_triangles = sum(area < FINISH_AREA_THRESHOLD_MM2 for area in areas)
    clean = (
        len(areas) == expected_faces
        and upward == expected_faces
        and downward == 0
        and micro_triangles == 0
    )
    return FinishPlaneReport(
        z_mm=z,
        faces=len(areas),
        expected_faces=expected_faces,
        upward_faces=upward,
        downward_faces=downward,
        minimum_triangle_area_mm2=min(areas),
        micro_triangles=micro_triangles,
        minimum_radius_mm=min(radii),
        maximum_radius_mm=max(radii),
        clean=clean,
    )


def build_v5(
    *,
    height: float,
    layers: int,
    wall: float,
    base: float,
    hole: float,
    top_lip_segments: int,
    connector_top_clearance: float,
    source: Path,
    connector: Path,
) -> tuple[Mesh, dict[str, float | int | bool], V5Report]:
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
        raise ValueError("V5 requires the prepared manifold v4 connector")

    trimmed_connector = trim_connector_top(
        source_connector, base, connector_top_clearance
    )
    trimmed_report = ensure_outward_orientation(trimmed_connector)
    trimmed_top = mesh_bounds(trimmed_connector)[1][2]
    expected_top = base - connector_top_clearance
    if abs(trimmed_top - expected_top) > 1e-5:
        raise RuntimeError(
            f"Trimmed connector top is {trimmed_top:.6f}; expected {expected_top:.6f}"
        )

    final = v4.boolean_union(body, trimmed_connector)
    final_report = ensure_outward_orientation(final)
    expected_finish_faces = int(construction["points_per_ring"]) * 2
    finish = inspect_finish_plane(
        final, z=base, expected_faces=expected_finish_faces
    )
    if not final_report.watertight or not finish.clean:
        raise RuntimeError(
            "V5 final validation failed: "
            f"boundary={final_report.boundary_edges}, "
            f"nonmanifold={final_report.nonmanifold_edges}, "
            f"finish_faces={finish.faces}/{finish.expected_faces}, "
            f"finish_micro_triangles={finish.micro_triangles}"
        )

    construction.update(
        {
            "connector_boolean_union": True,
            "connector_top_clearance_mm": connector_top_clearance,
            "connector_trimmed_top_z_mm": trimmed_top,
            "continuous_interior_floor": True,
            "connector_geometry_on_finish_plane": False,
        }
    )
    return final, construction, V5Report(
        lamp_body=body_validation.final,
        source_connector=source_connector_report,
        trimmed_connector=trimmed_report,
        final=final_report,
        connector_top_clearance_mm=connector_top_clearance,
        trimmed_connector_top_z_mm=trimmed_top,
        single_body_boolean_union=True,
        finish_plane=finish,
    )


def write_binary_stl_v5(path: Path, mesh: Mesh) -> None:
    with path.open("wb") as handle:
        header = b"Illinois Sandstone Lamp v5 - clean interior finish plane"
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
    yield '  <metadata name="Title">Illinois Sandstone Lamp v5</metadata>\n'
    yield '  <metadata name="Application">generate_sandstone_v5.py</metadata>\n'
    yield '  <resources>\n'
    yield '    <object id="1" type="model" name="Connected lamp v5 - smooth interior finish">\n'
    yield '      <mesh>\n        <vertices>\n'
    for x, y, z in mesh.points:
        yield f'          <vertex x="{x:.7f}" y="{y:.7f}" z="{z:.7f}"/>\n'
    yield '        </vertices>\n        <triangles>\n'
    for a, b, c in mesh.faces:
        yield f'          <triangle v1="{a}" v2="{b}" v3="{c}"/>\n'
    yield '        </triangles>\n      </mesh>\n    </object>\n'
    yield '  </resources>\n  <build>\n    <item objectid="1" printable="1"/>\n  </build>\n</model>\n'


def write_3mf_v5(path: Path, mesh: Mesh) -> None:
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


def write_scad_v5(path: Path, mesh: Mesh, parameters: Parameters, clearance: float) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "// Illinois Sandstone Lamp v5\n"
            "// Generated by generate_sandstone_v5.py\n"
            "// Single watertight solid with a clean interior finish plane.\n"
            f"// height={parameters.height} layers={parameters.layers} "
            f"wall={parameters.wall} base={parameters.base} hole={parameters.hole}\n"
            f"// connector_top_clearance={clearance}\n\n"
            "/* [Height Fine-Tuning] */\n"
            "fine_tune_scale = 1.0;  // [0.90:0.001:1.10]\n\n"
            "scale([1, 1, fine_tune_scale])\n"
        )
        write_scad_polyhedron(handle, mesh)


def write_report(
    path: Path,
    parameters: Parameters,
    construction: dict[str, float | int | bool],
    report: V5Report,
    outputs: Sequence[Path],
) -> None:
    payload = {
        "generator": "generate_sandstone_v5.py",
        "parameters": asdict(parameters),
        "construction": construction,
        "validation": asdict(report),
        "outputs": [output.name for output in outputs],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a manifold sandstone lamp v5 with a clean interior floor",
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
        help="distance the connector is recessed below the visible interior floor",
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
    final, construction, report = build_v5(
        height=args.height,
        layers=layers,
        wall=args.wall,
        base=args.base,
        hole=args.hole,
        top_lip_segments=args.top_lip_segments,
        connector_top_clearance=args.connector_top_clearance,
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
        f"illinois_sandstone_v5_{format_number(args.height)}mm_"
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
            write_binary_stl_v5(path, final)
        elif output_format == "3mf":
            write_3mf_v5(path, final)
        elif output_format == "scad":
            write_scad_v5(path, final, parameters, args.connector_top_clearance)
        outputs.append(path)
    if "json" in args.formats:
        path = output_dir / f"{basename}.report.json"
        write_report(path, parameters, construction, report, outputs)
        outputs.append(path)

    mesh_report = report.final
    finish = report.finish_plane
    print("Illinois Sandstone Lamp v5")
    print(f"  Source rings retained: {len(source_rings)} / {len(source_rings)}")
    print(f"  Output rings:          {layers}")
    print(f"  Vertices / faces:      {mesh_report.vertices:,} / {mesh_report.faces:,}")
    print("  Size (mm):             " + " x ".join(f"{v:.3f}" for v in mesh_report.size_mm))
    print(f"  Boundary edges:        {mesh_report.boundary_edges}")
    print(f"  Non-manifold edges:    {mesh_report.nonmanifold_edges}")
    print(f"  Degenerate faces:      {mesh_report.degenerate_faces}")
    print(f"  Components:            {mesh_report.connected_components}")
    print(f"  Finish-plane faces:    {finish.faces} clean large triangles")
    print(f"  Finish micro-triangles:{finish.micro_triangles}")
    print(f"  Connector clearance:  {report.connector_top_clearance_mm:.3f} mm")
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
