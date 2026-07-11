#!/usr/bin/env python3
"""Build the smooth-shoulder sandstone screw base v4.

The source Bambu Studio 3MF contains:

* a positive base mesh made from six disconnected components; and
* a positioned negative drill/cord object.

V4 replaces only the outer rounded component with a clean surface of
revolution.  The screw interface, central core, slots, and other functional
components are copied vertex-for-vertex.  The negative drill object and its
Bambu Studio ``negative_part`` metadata are also copied unchanged, so it is
subtracted when the 3MF is sliced.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import sys
from typing import Sequence
from xml.etree import ElementTree
from zipfile import ZIP_DEFLATED, ZipFile

from generate_sandstone_v2 import (
    Face,
    Mesh,
    Point,
    combine_meshes,
    ensure_outward_orientation,
    mesh_bounds,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_SOURCE = PROJECT_DIR / "files" / "base" / "sandstonelayers-base-v3-final.3mf"
DEFAULT_OUTPUT = PROJECT_DIR / "files" / "base" / "sandstonelayers-base-v4-smooth-drilled.3mf"
DEFAULT_REPORT = PROJECT_DIR / "files" / "base" / "sandstonelayers-base-v4-smooth-drilled.report.json"

CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
BAMBU_NS = "http://schemas.bambulab.com/package/2021"
PRODUCTION_NS = "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"
NS = {"m": CORE_NS}

DEFAULT_OUTER_RADIUS = 57.5
DEFAULT_INNER_RADIUS = 32.8
DEFAULT_FLAT_TOP_RADIUS = 47.0
DEFAULT_BODY_HEIGHT = 15.0
DEFAULT_SIDE_HEIGHT = 7.5
DEFAULT_BOTTOM_FILLET = 2.0
DEFAULT_CIRCUMFERENCE_SEGMENTS = 360
DEFAULT_SHOULDER_SEGMENTS = 24
DEFAULT_BOTTOM_FILLET_SEGMENTS = 8


def parse_mesh_object(model_root: ElementTree.Element, object_id: str) -> Mesh:
    object_element = model_root.find(f'.//m:object[@id="{object_id}"]', NS)
    if object_element is None:
        raise ValueError(f"3MF object {object_id} was not found")
    vertex_elements = object_element.findall("./m:mesh/m:vertices/m:vertex", NS)
    triangle_elements = object_element.findall("./m:mesh/m:triangles/m:triangle", NS)
    if not vertex_elements or not triangle_elements:
        raise ValueError(f"3MF object {object_id} does not contain a mesh")
    points = [
        tuple(float(vertex.get(axis)) for axis in ("x", "y", "z"))
        for vertex in vertex_elements
    ]
    faces = [
        tuple(int(triangle.get(index)) for index in ("v1", "v2", "v3"))
        for triangle in triangle_elements
    ]
    return Mesh(points, faces)


def face_components(mesh: Mesh) -> list[set[int]]:
    """Return face-index sets connected by shared indexed vertices."""
    vertex_faces: defaultdict[int, list[int]] = defaultdict(list)
    for face_index, face in enumerate(mesh.faces):
        for vertex_index in face:
            vertex_faces[vertex_index].append(face_index)

    seen: set[int] = set()
    components: list[set[int]] = []
    for start in range(len(mesh.faces)):
        if start in seen:
            continue
        pending = [start]
        seen.add(start)
        component: set[int] = set()
        while pending:
            face_index = pending.pop()
            component.add(face_index)
            for vertex_index in mesh.faces[face_index]:
                for neighbor in vertex_faces[vertex_index]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        pending.append(neighbor)
        components.append(component)
    components.sort(key=len, reverse=True)
    return components


def extract_faces(mesh: Mesh, face_indices: set[int]) -> Mesh:
    used_vertices = sorted(
        {vertex for face_index in face_indices for vertex in mesh.faces[face_index]}
    )
    index_map = {old: new for new, old in enumerate(used_vertices)}
    points = [mesh.points[index] for index in used_vertices]
    faces = [
        tuple(index_map[vertex] for vertex in mesh.faces[face_index])
        for face_index in sorted(face_indices)
    ]
    return Mesh(points, faces)


def maximum_radius(mesh: Mesh) -> float:
    return max(math.hypot(x, y) for x, y, _ in mesh.points)


def minimum_radius(mesh: Mesh) -> float:
    return min(math.hypot(x, y) for x, y, _ in mesh.points)


def identify_outer_component(mesh: Mesh, components: Sequence[set[int]]) -> int:
    """Find the disconnected body spanning the 115 mm exterior."""
    candidates: list[tuple[float, float, int]] = []
    for index, face_indices in enumerate(components):
        component = extract_faces(mesh, face_indices)
        candidates.append((maximum_radius(component), minimum_radius(component), index))
    outer_radius, inner_radius, component_index = max(candidates)
    if outer_radius < 50.0 or inner_radius < 25.0:
        raise ValueError(
            "Could not safely identify the outer body component: "
            f"radius range {inner_radius:.3f}..{outer_radius:.3f} mm"
        )
    return component_index


def smooth_profile(
    z_bottom: float,
    *,
    outer_radius: float,
    inner_radius: float,
    flat_top_radius: float,
    body_height: float,
    side_height: float,
    bottom_fillet: float,
    shoulder_segments: int,
    bottom_fillet_segments: int,
) -> list[tuple[float, float]]:
    """Closed radial/Z profile with tangent-continuous top and bottom joins."""
    z_top = z_bottom + body_height
    z_side_end = z_bottom + side_height
    if not (inner_radius < flat_top_radius < outer_radius):
        raise ValueError("Profile radii must increase: inner < flat top < outer")
    if not (0.0 < bottom_fillet < side_height < body_height):
        raise ValueError("Profile heights must satisfy fillet < side < body")
    if shoulder_segments < 4 or bottom_fillet_segments < 2:
        raise ValueError("Profile needs at least 4 shoulder and 2 fillet segments")

    profile: list[tuple[float, float]] = [
        (inner_radius, z_bottom),
        (outer_radius - bottom_fillet, z_bottom),
    ]

    # Quarter-circle bottom fillet: horizontal bottom -> vertical outer side.
    for segment in range(1, bottom_fillet_segments + 1):
        angle = (math.pi / 2.0) * segment / bottom_fillet_segments
        radius = outer_radius - bottom_fillet + bottom_fillet * math.sin(angle)
        z = z_bottom + bottom_fillet * (1.0 - math.cos(angle))
        profile.append((radius, z))

    if profile[-1][1] < z_side_end - 1e-9:
        profile.append((outer_radius, z_side_end))

    # Quarter-ellipse shoulder: vertical side -> perfectly horizontal flat top.
    shoulder_width = outer_radius - flat_top_radius
    shoulder_height = body_height - side_height
    for segment in range(1, shoulder_segments + 1):
        angle = (math.pi / 2.0) * segment / shoulder_segments
        radius = flat_top_radius + shoulder_width * math.cos(angle)
        z = z_side_end + shoulder_height * math.sin(angle)
        profile.append((radius, z))

    profile.append((inner_radius, z_top))
    return profile


def revolve_profile(profile: Sequence[tuple[float, float]], segments: int) -> Mesh:
    if segments < 24:
        raise ValueError("Circumference needs at least 24 segments")
    points: list[Point] = []
    for radius, z in profile:
        for segment in range(segments):
            angle = 2.0 * math.pi * segment / segments
            points.append((radius * math.cos(angle), radius * math.sin(angle), z))

    faces: list[Face] = []
    ring_count = len(profile)
    for profile_index in range(ring_count):
        next_profile = (profile_index + 1) % ring_count
        for segment in range(segments):
            next_segment = (segment + 1) % segments
            a = profile_index * segments + segment
            b = profile_index * segments + next_segment
            c = next_profile * segments + next_segment
            d = next_profile * segments + segment
            faces.extend(((a, b, c), (a, c, d)))
    mesh = Mesh(points, faces)
    report = ensure_outward_orientation(mesh)
    if not report.watertight:
        raise RuntimeError("Generated outer body is not watertight")
    return mesh


def replace_object_mesh(
    model_root: ElementTree.Element, object_id: str, mesh: Mesh
) -> None:
    object_element = model_root.find(f'.//m:object[@id="{object_id}"]', NS)
    if object_element is None:
        raise ValueError(f"3MF object {object_id} was not found")
    old_mesh = object_element.find("./m:mesh", NS)
    if old_mesh is None:
        raise ValueError(f"3MF object {object_id} has no mesh")
    object_element.remove(old_mesh)

    mesh_element = ElementTree.SubElement(object_element, f"{{{CORE_NS}}}mesh")
    vertices_element = ElementTree.SubElement(
        mesh_element, f"{{{CORE_NS}}}vertices"
    )
    for x, y, z in mesh.points:
        ElementTree.SubElement(
            vertices_element,
            f"{{{CORE_NS}}}vertex",
            {"x": f"{x:.7f}", "y": f"{y:.7f}", "z": f"{z:.7f}"},
        )
    triangles_element = ElementTree.SubElement(
        mesh_element, f"{{{CORE_NS}}}triangles"
    )
    for a, b, c in mesh.faces:
        ElementTree.SubElement(
            triangles_element,
            f"{{{CORE_NS}}}triangle",
            {"v1": str(a), "v2": str(b), "v3": str(c)},
        )


def update_model_settings(config_data: bytes) -> bytes:
    root = ElementTree.fromstring(config_data)
    for metadata in root.findall(".//metadata"):
        key = metadata.get("key")
        if key == "name" and metadata.get("value") == "base-simple-v3-115mmx22mm-corded":
            metadata.set("value", "sandstonelayers-base-v4-smooth-drilled")
    part = root.find('.//part[@id="1"]')
    if part is not None:
        name = part.find('./metadata[@key="name"]')
        if name is not None:
            name.set("value", "base-v4-smooth-shoulder")
    return ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)


def negative_part_is_present(config_data: bytes) -> bool:
    root = ElementTree.fromstring(config_data)
    return root.find('.//part[@subtype="negative_part"]') is not None


def build_v4(
    source: Path,
    output: Path,
    report_path: Path,
    *,
    outer_radius: float,
    inner_radius: float,
    flat_top_radius: float,
    body_height: float,
    side_height: float,
    bottom_fillet: float,
    circumference_segments: int,
    shoulder_segments: int,
    bottom_fillet_segments: int,
) -> dict[str, object]:
    with ZipFile(source) as archive:
        names = archive.namelist()
        object_models = [
            name for name in names if name.startswith("3D/Objects/") and name.endswith(".model")
        ]
        if len(object_models) != 1:
            raise ValueError("Expected exactly one 3D/Objects model in source 3MF")
        object_model_name = object_models[0]
        object_model_data = archive.read(object_model_name)
        config_data = archive.read("Metadata/model_settings.config")
        if not negative_part_is_present(config_data):
            raise ValueError("Source 3MF does not contain a negative drill part")

        ElementTree.register_namespace("", CORE_NS)
        ElementTree.register_namespace("BambuStudio", BAMBU_NS)
        ElementTree.register_namespace("p", PRODUCTION_NS)
        model_root = ElementTree.fromstring(object_model_data)
        positive_mesh = parse_mesh_object(model_root, "1")
        negative_mesh = parse_mesh_object(model_root, "2")
        components = face_components(positive_mesh)
        outer_index = identify_outer_component(positive_mesh, components)
        old_outer = extract_faces(positive_mesh, components[outer_index])
        preserved_faces = set().union(
            *(component for index, component in enumerate(components) if index != outer_index)
        )
        preserved_mesh = extract_faces(positive_mesh, preserved_faces)

        old_minimums, old_maximums = mesh_bounds(old_outer)
        z_bottom = old_minimums[2]
        profile = smooth_profile(
            z_bottom,
            outer_radius=outer_radius,
            inner_radius=inner_radius,
            flat_top_radius=flat_top_radius,
            body_height=body_height,
            side_height=side_height,
            bottom_fillet=bottom_fillet,
            shoulder_segments=shoulder_segments,
            bottom_fillet_segments=bottom_fillet_segments,
        )
        new_outer = revolve_profile(profile, circumference_segments)
        new_positive = combine_meshes([preserved_mesh, new_outer])
        replace_object_mesh(model_root, "1", new_positive)
        new_model_data = ElementTree.tostring(
            model_root, encoding="utf-8", xml_declaration=True
        )
        new_config_data = update_model_settings(config_data)

        output.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=6) as destination:
            for name in names:
                if name == object_model_name:
                    destination.writestr(name, new_model_data)
                elif name == "Metadata/model_settings.config":
                    destination.writestr(name, new_config_data)
                else:
                    destination.writestr(name, archive.read(name))

    new_outer_report = ensure_outward_orientation(new_outer)
    new_minimums, new_maximums = mesh_bounds(new_outer)
    report: dict[str, object] = {
        "generator": "generate_base_v4.py",
        "source": str(source.relative_to(PROJECT_DIR)),
        "output": output.name,
        "positive_mesh": {
            "source_faces": len(positive_mesh.faces),
            "old_outer_faces_removed": len(old_outer.faces),
            "functional_faces_preserved": len(preserved_mesh.faces),
            "new_outer_faces": len(new_outer.faces),
            "new_total_faces": len(new_positive.faces),
        },
        "outer_body": {
            "watertight": new_outer_report.watertight,
            "outer_radius_mm": outer_radius,
            "outer_diameter_mm": outer_radius * 2.0,
            "inner_overlap_radius_mm": inner_radius,
            "flat_top_radius_mm": flat_top_radius,
            "body_height_mm": body_height,
            "side_height_mm": side_height,
            "bottom_fillet_mm": bottom_fillet,
            "circumference_segments": circumference_segments,
            "shoulder_segments": shoulder_segments,
            "bottom_fillet_segments": bottom_fillet_segments,
            "bounds_min_mm": new_minimums,
            "bounds_max_mm": new_maximums,
        },
        "negative_drill": {
            "included": True,
            "bambu_subtype": "negative_part",
            "vertices": len(negative_mesh.points),
            "faces": len(negative_mesh.faces),
            "geometry_and_transform": "copied unchanged from source 3MF",
        },
        "functional_geometry": {
            "components_preserved": len(components) - 1,
            "geometry": "screw interface, core, slots, and upper features copied unchanged",
        },
        "source_outer_bounds_min_mm": old_minimums,
        "source_outer_bounds_max_mm": old_maximums,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Generate the smooth-shoulder sandstone screw base v4",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    result.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    result.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    result.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    result.add_argument("--outer-radius", type=float, default=DEFAULT_OUTER_RADIUS)
    result.add_argument("--inner-radius", type=float, default=DEFAULT_INNER_RADIUS)
    result.add_argument("--flat-top-radius", type=float, default=DEFAULT_FLAT_TOP_RADIUS)
    result.add_argument("--body-height", type=float, default=DEFAULT_BODY_HEIGHT)
    result.add_argument("--side-height", type=float, default=DEFAULT_SIDE_HEIGHT)
    result.add_argument("--bottom-fillet", type=float, default=DEFAULT_BOTTOM_FILLET)
    result.add_argument(
        "--circumference-segments", type=int, default=DEFAULT_CIRCUMFERENCE_SEGMENTS
    )
    result.add_argument("--shoulder-segments", type=int, default=DEFAULT_SHOULDER_SEGMENTS)
    result.add_argument(
        "--bottom-fillet-segments", type=int, default=DEFAULT_BOTTOM_FILLET_SEGMENTS
    )
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    report = build_v4(
        args.source.resolve(),
        args.output.resolve(),
        args.report.resolve(),
        outer_radius=args.outer_radius,
        inner_radius=args.inner_radius,
        flat_top_radius=args.flat_top_radius,
        body_height=args.body_height,
        side_height=args.side_height,
        bottom_fillet=args.bottom_fillet,
        circumference_segments=args.circumference_segments,
        shoulder_segments=args.shoulder_segments,
        bottom_fillet_segments=args.bottom_fillet_segments,
    )
    positive = report["positive_mesh"]
    outer = report["outer_body"]
    print("Sandstone screw base v4")
    print(f"  Smooth outer body:     {outer['new_outer_faces'] if 'new_outer_faces' in outer else positive['new_outer_faces']:,} faces")
    print(f"  Functional faces kept: {positive['functional_faces_preserved']:,}")
    print(f"  Negative drill:        included unchanged as negative_part")
    print(f"  Wrote:                 {args.output.resolve()}")
    print(f"  Report:                {args.report.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
