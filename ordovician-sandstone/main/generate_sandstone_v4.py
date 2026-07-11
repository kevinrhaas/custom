#!/usr/bin/env python3
"""Generate single-body, manifold Illinois sandstone lamp v4 models.

V4 preserves the original 120 mm sandstone control rings and v2's gentle
rounded top lip, but replaces the old overlapping lamp/connector assembly with
an actual Boolean union.  The resulting 120, 150, and 180 mm releases contain
one indexed watertight mesh with a continuous interior floor.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from importlib.metadata import version
import json
import math
from pathlib import Path
import struct
import sys
from typing import Iterable, Sequence
from zipfile import ZIP_DEFLATED, ZipFile

try:
    import manifold3d as manifold
    import numpy as np
except ImportError as error:  # pragma: no cover - exercised by end users
    raise SystemExit(
        "Lamp v4 dependencies are missing. Run: "
        "python3 -m pip install -r requirements-v4.txt"
    ) from error

from generate_sandstone_v2 import (
    DEFAULT_BASE,
    DEFAULT_HEIGHT,
    DEFAULT_HOLE,
    DEFAULT_LAYERS,
    DEFAULT_SOURCE,
    DEFAULT_TOP_LIP_SEGMENTS,
    DEFAULT_WALL,
    Mesh,
    MeshReport,
    Parameters,
    build_lamp_mesh,
    ensure_outward_orientation,
    format_number,
    inspect_mesh,
    mesh_bounds,
    normal_for_face,
    parse_formats,
    read_binary_stl,
    read_source_rings,
    scale_rings_to_height,
    source_preserving_resample,
    write_scad_polyhedron,
)
from repair_connector_v4 import weld_exact_and_remove_degenerate


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_CONNECTOR = (
    PROJECT_DIR / "files" / "connect" / "80mm-lamp-attach-base-manifold-v4.stl"
)
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "files" / "lamp" / "v4" / "connected"


@dataclass(frozen=True)
class V4Report:
    lamp_body: MeshReport
    connector: MeshReport | None
    final: MeshReport
    boolean_engine: str | None
    single_body_boolean_union: bool
    internal_floor_coplanar_duplicate_faces: int


def to_manifold(mesh: Mesh) -> manifold.Manifold:
    value = manifold.Manifold(
        manifold.Mesh(
            np.asarray(mesh.points, dtype=np.float32),
            np.asarray(mesh.faces, dtype=np.uint32),
        )
    )
    if value.status() != manifold.Error.NoError:
        raise RuntimeError(f"Manifold rejected input mesh: {value.status()}")
    return value


def from_manifold(value: manifold.Manifold) -> Mesh:
    result = value.to_mesh()
    return Mesh(
        [tuple(map(float, point[:3])) for point in result.vert_properties],
        [tuple(map(int, face)) for face in result.tri_verts],
    )


def count_coplanar_duplicate_faces(mesh: Mesh, z: float, tolerance: float = 1e-5) -> int:
    """Count duplicate triangles lying on the horizontal interior floor."""
    seen: set[tuple[tuple[float, float, float], ...]] = set()
    duplicates = 0
    for face in mesh.faces:
        points = [mesh.points[index] for index in face]
        if not all(abs(point[2] - z) <= tolerance for point in points):
            continue
        canonical = tuple(
            sorted(tuple(round(value, 6) for value in point) for point in points)
        )
        if canonical in seen:
            duplicates += 1
        seen.add(canonical)
    return duplicates


def boolean_union(lamp_body: Mesh, connector: Mesh) -> Mesh:
    unified = to_manifold(lamp_body) + to_manifold(connector)
    if unified.status() != manifold.Error.NoError:
        raise RuntimeError(f"Lamp/connector Boolean union failed: {unified.status()}")
    if len(unified.decompose()) != 1:
        raise RuntimeError("Lamp/connector Boolean did not produce one connected solid")
    return weld_exact_and_remove_degenerate(from_manifold(unified))


def build_v4(
    *,
    height: float,
    layers: int,
    wall: float,
    base: float,
    hole: float,
    top_lip_segments: int,
    source: Path,
    connector: Path | None,
) -> tuple[Mesh, dict[str, float | int], V4Report]:
    source_rings = read_source_rings(source)
    preserved = source_preserving_resample(source_rings, layers)
    outer_rings = scale_rings_to_height(preserved, height)
    body, construction = build_lamp_mesh(
        outer_rings, wall, base, hole, top_lip_segments
    )
    body_report = ensure_outward_orientation(body)
    if not body_report.watertight:
        raise RuntimeError("The generated lamp body is not watertight")

    connector_report: MeshReport | None = None
    final = body
    engine: str | None = None
    single_body = False
    if connector is not None:
        connector_mesh = read_binary_stl(connector)
        connector_report = ensure_outward_orientation(connector_mesh)
        if not connector_report.watertight:
            raise ValueError(
                "V4 requires the prepared manifold connector; run "
                "repair_connector_v4.py first"
            )
        connector_min, connector_max = mesh_bounds(connector_mesh)
        if abs(connector_min[2]) > 0.02 or abs(connector_max[2] - base) > 0.02:
            raise ValueError(
                f"Connector z bounds {connector_min[2]:.3f}..{connector_max[2]:.3f} "
                f"do not match the {base:.3f} mm lamp floor"
            )
        final = boolean_union(body, connector_mesh)
        engine = f"manifold3d {version('manifold3d')}"
        single_body = True

    final_report = ensure_outward_orientation(final)
    floor_duplicates = count_coplanar_duplicate_faces(final, base)
    if not final_report.watertight or floor_duplicates:
        raise RuntimeError(
            "V4 final mesh failed validation: "
            f"boundary={final_report.boundary_edges}, "
            f"nonmanifold={final_report.nonmanifold_edges}, "
            f"degenerate={final_report.degenerate_faces}, "
            f"floor_duplicates={floor_duplicates}"
        )
    construction.update(
        {
            "source_rings_retained": len(source_rings),
            "connector_boolean_union": single_body,
            "continuous_interior_floor": True,
        }
    )
    return final, construction, V4Report(
        lamp_body=body_report,
        connector=connector_report,
        final=final_report,
        boolean_engine=engine,
        single_body_boolean_union=single_body,
        internal_floor_coplanar_duplicate_faces=floor_duplicates,
    )


def write_binary_stl_v4(path: Path, mesh: Mesh) -> None:
    with path.open("wb") as handle:
        header = b"Illinois Sandstone Lamp v4 - single-body manifold Boolean"
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
    yield '  <metadata name="Title">Illinois Sandstone Lamp v4</metadata>\n'
    yield '  <metadata name="Application">generate_sandstone_v4.py</metadata>\n'
    yield '  <resources>\n'
    yield '    <object id="1" type="model" name="Connected lamp - single Boolean solid">\n'
    yield '      <mesh>\n        <vertices>\n'
    for x, y, z in mesh.points:
        yield f'          <vertex x="{x:.7f}" y="{y:.7f}" z="{z:.7f}"/>\n'
    yield '        </vertices>\n        <triangles>\n'
    for a, b, c in mesh.faces:
        yield f'          <triangle v1="{a}" v2="{b}" v3="{c}"/>\n'
    yield '        </triangles>\n      </mesh>\n    </object>\n'
    yield '  </resources>\n  <build>\n    <item objectid="1" printable="1"/>\n  </build>\n</model>\n'


def write_3mf_v4(path: Path, mesh: Mesh) -> None:
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


def write_scad_v4(path: Path, mesh: Mesh, parameters: Parameters) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "// Illinois Sandstone Lamp v4\n"
            "// Generated by generate_sandstone_v4.py\n"
            "// Single watertight Boolean solid; continuous interior floor.\n"
            f"// height={parameters.height} layers={parameters.layers} "
            f"wall={parameters.wall} base={parameters.base} hole={parameters.hole}\n\n"
            "/* [Height Fine-Tuning] */\n"
            "fine_tune_scale = 1.0;  // [0.90:0.001:1.10]\n\n"
            "scale([1, 1, fine_tune_scale])\n"
        )
        write_scad_polyhedron(handle, mesh)


def write_report(
    path: Path,
    parameters: Parameters,
    construction: dict[str, float | int],
    report: V4Report,
    outputs: Sequence[Path],
) -> None:
    payload = {
        "generator": "generate_sandstone_v4.py",
        "parameters": asdict(parameters),
        "construction": construction,
        "validation": asdict(report),
        "outputs": [output.name for output in outputs],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a single-body manifold sandstone lamp v4",
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
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--connector", type=Path, default=DEFAULT_CONNECTOR)
    parser.add_argument("--no-connector", action="store_true")
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
    source_rings = read_source_rings(source)
    layers = args.layers
    if layers is None:
        layers = max(
            len(source_rings), int(round(len(source_rings) * args.height / 120.0))
        )
    connector = None if args.no_connector else args.connector.resolve()
    final, construction, report = build_v4(
        height=args.height,
        layers=layers,
        wall=args.wall,
        base=args.base,
        hole=args.hole,
        top_lip_segments=args.top_lip_segments,
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
        connector=display(connector) if connector else None,
    )
    basename = args.name or (
        f"illinois_sandstone_v4_{format_number(args.height)}mm_"
        f"{layers}L_wall{format_number(args.wall)}_"
        f"base{format_number(args.base)}_hole{format_number(args.hole)}"
        f"{'_connector80' if connector else ''}"
    )
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for output_format in args.formats:
        if output_format == "json":
            continue
        path = output_dir / f"{basename}.{output_format}"
        if output_format == "stl":
            write_binary_stl_v4(path, final)
        elif output_format == "3mf":
            write_3mf_v4(path, final)
        elif output_format == "scad":
            write_scad_v4(path, final, parameters)
        outputs.append(path)
    if "json" in args.formats:
        path = output_dir / f"{basename}.report.json"
        write_report(path, parameters, construction, report, outputs)
        outputs.append(path)

    mesh_report = report.final
    print("Illinois Sandstone Lamp v4")
    print(f"  Source rings retained: {len(source_rings)} / {len(source_rings)}")
    print(f"  Output rings:          {layers}")
    print(f"  Vertices / faces:      {mesh_report.vertices:,} / {mesh_report.faces:,}")
    print("  Size (mm):             " + " x ".join(f"{v:.3f}" for v in mesh_report.size_mm))
    print(f"  Boundary edges:        {mesh_report.boundary_edges}")
    print(f"  Non-manifold edges:    {mesh_report.nonmanifold_edges}")
    print(f"  Degenerate faces:      {mesh_report.degenerate_faces}")
    print(f"  Components:            {mesh_report.connected_components}")
    print(f"  Interior duplicates:  {report.internal_floor_coplanar_duplicate_faces}")
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
