#!/usr/bin/env python3
"""Generate a detail-preserving, watertight Illinois sandstone lamp shell.

V2 fixes the base-transition seam in the original parametric generator by
building the complete lamp (outer wall, inner wall, base floor, center hole,
and top rim) as one indexed manifold mesh.  It also retains every ring from
the 120 mm source model.  Requested extra layers are inserted between source
rings, so increasing the height or layer count never discards a source ring.

The default preset reproduces the requested tall lamp:

    python3 generate_sandstone_v2.py

Equivalent explicit command:

    python3 generate_sandstone_v2.py \
        --height 180 --layers 166 --wall 2 --base 9.46 --hole 66

The program uses only the Python standard library and writes STL, 3MF, SCAD,
and a JSON validation report by default.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import re
import struct
import sys
from typing import Iterable, Sequence
from zipfile import ZIP_DEFLATED, ZipFile


Point = tuple[float, float, float]
Face = tuple[int, int, int]
Ring = list[Point]

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = SCRIPT_DIR.parent / "raw" / "1-illinois_sandstone_cylinder_v3.scad"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR.parent / "files" / "lamp" / "v2"

DEFAULT_HEIGHT = 180.0
DEFAULT_LAYERS = 166
DEFAULT_WALL = 2.0
DEFAULT_BASE = 9.46
DEFAULT_HOLE = 66.0
DEFAULT_TOP_LIP_SEGMENTS = 8

POINT_RE = re.compile(r"\[\s*([^,]+),\s*([^,]+),\s*([^\]]+)\]")


@dataclass(frozen=True)
class Parameters:
    height: float
    layers: int
    wall: float
    base: float
    hole: float
    top_lip_segments: int
    source: str


@dataclass(frozen=True)
class MeshReport:
    vertices: int
    faces: int
    unique_edges: int
    boundary_edges: int
    nonmanifold_edges: int
    connected_components: int
    unused_vertices: int
    degenerate_faces: int
    duplicate_faces: int
    signed_volume_mm3: float
    minimum_triangle_area_mm2: float
    bounds_min_mm: list[float]
    bounds_max_mm: list[float]
    size_mm: list[float]
    watertight: bool


@dataclass
class Mesh:
    points: list[Point]
    faces: list[Face]


def format_number(value: float) -> str:
    """Compact decimal for filenames and status output."""
    return f"{value:.4f}".rstrip("0").rstrip(".")


def read_source_rings(path: Path, points_per_ring: int = 120) -> list[Ring]:
    """Read the original polyhedron points and return its ordered rings.

    The source ends with two center-cap vertices.  Unlike the old generator,
    v2 recognizes that the first and last source rings are already flat caps
    and does not add coincident duplicates.
    """
    points: list[Point] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if "faces" in line and "=" in line:
                break
            match = POINT_RE.search(line)
            if match:
                points.append(tuple(float(value) for value in match.groups()))

    if len(points) < points_per_ring + 2:
        raise ValueError(f"Source does not contain enough polyhedron points: {path}")

    ring_point_count = len(points) - 2
    if ring_point_count % points_per_ring:
        raise ValueError(
            f"Expected ring points plus two cap centers; found {len(points)} points"
        )

    ring_count = ring_point_count // points_per_ring
    rings = [
        points[index * points_per_ring : (index + 1) * points_per_ring]
        for index in range(ring_count)
    ]

    if ring_count < 2:
        raise ValueError("Source must contain at least two rings")
    if max(abs(point[2] - rings[0][0][2]) for point in rings[0]) > 1e-7:
        raise ValueError("Source first ring is not flat")
    if max(abs(point[2] - rings[-1][0][2]) for point in rings[-1]) > 1e-7:
        raise ValueError("Source last ring is not flat")

    return rings


def lerp_point(a: Point, b: Point, amount: float) -> Point:
    inverse = 1.0 - amount
    return (
        inverse * a[0] + amount * b[0],
        inverse * a[1] + amount * b[1],
        inverse * a[2] + amount * b[2],
    )


def source_preserving_resample(source_rings: Sequence[Ring], layers: int) -> list[Ring]:
    """Add rings without removing any original source profile.

    Segment counts are distributed evenly across source intervals.  Every
    source ring is emitted exactly, while extra rings are linear subdivisions
    between adjacent originals.  This avoids the detail loss caused by
    uniformly resampling 111 control rings onto a 166-ring grid.
    """
    source_count = len(source_rings)
    if layers < source_count:
        raise ValueError(
            f"--layers must be at least {source_count} to preserve all source detail"
        )

    source_intervals = source_count - 1
    requested_segments = layers - 1
    result: list[Ring] = []

    for interval in range(source_intervals):
        # Keep the final source interval unsubdivided.  That leaves a clean
        # approach to the rounded lip while distributing all requested extra
        # detail through the sandstone body below it.
        if source_intervals == 1 or interval == source_intervals - 1:
            subdivisions = 1
        else:
            distributable_intervals = source_intervals - 1
            distributable_segments = requested_segments - 1
            segment_start = (interval * distributable_segments) // distributable_intervals
            segment_end = ((interval + 1) * distributable_segments) // distributable_intervals
            subdivisions = segment_end - segment_start
        if subdivisions < 1:
            raise AssertionError("Every source interval must receive a segment")

        lower = source_rings[interval]
        upper = source_rings[interval + 1]
        for subdivision in range(subdivisions):
            amount = subdivision / subdivisions
            if subdivision == 0:
                result.append(list(lower))
            else:
                result.append(
                    [lerp_point(a, b, amount) for a, b in zip(lower, upper)]
                )

    result.append(list(source_rings[-1]))
    if len(result) != layers:
        raise AssertionError(f"Generated {len(result)} rings; expected {layers}")
    return result


def scale_rings_to_height(rings: Sequence[Ring], height: float) -> list[Ring]:
    source_bottom = rings[0][0][2]
    source_top = rings[-1][0][2]
    source_height = source_top - source_bottom
    if source_height <= 0:
        raise ValueError("Source height must be positive")
    scale = height / source_height
    return [
        [(x, y, (z - source_bottom) * scale) for x, y, z in ring]
        for ring in rings
    ]


def ring_average_z(ring: Sequence[Point]) -> float:
    return sum(point[2] for point in ring) / len(ring)


def interpolate_profile_at_z(rings: Sequence[Ring], z: float) -> Ring:
    """Interpolate XY at a nominal ring-average height and return a flat ring."""
    averages = [ring_average_z(ring) for ring in rings]
    if z <= averages[0]:
        return [(x, y, z) for x, y, _ in rings[0]]
    if z >= averages[-1]:
        return [(x, y, z) for x, y, _ in rings[-1]]

    for index in range(len(rings) - 1):
        lower_z = averages[index]
        upper_z = averages[index + 1]
        if lower_z <= z <= upper_z:
            amount = (z - lower_z) / (upper_z - lower_z)
            return [
                (
                    (1.0 - amount) * a[0] + amount * b[0],
                    (1.0 - amount) * a[1] + amount * b[1],
                    z,
                )
                for a, b in zip(rings[index], rings[index + 1])
            ]
    raise AssertionError("Unable to bracket requested Z profile")


def radial_offset_inward(ring: Sequence[Point], distance: float) -> Ring:
    """Offset an origin-centered organic ring inward by an exact radial distance."""
    result: Ring = []
    for x, y, z in ring:
        radius = math.hypot(x, y)
        if radius <= distance:
            raise ValueError(
                f"Wall {distance} mm is too thick for local radius {radius:.4f} mm"
            )
        scale = (radius - distance) / radius
        result.append((x * scale, y * scale, z))
    return result


def circular_ring_from_angles(reference: Sequence[Point], radius: float, z: float) -> Ring:
    return [
        (radius * math.cos(math.atan2(y, x)), radius * math.sin(math.atan2(y, x)), z)
        for x, y, _ in reference
    ]


def add_ring(points: list[Point], ring: Sequence[Point]) -> int:
    start = len(points)
    points.extend(ring)
    return start


def stitch_rings(
    faces: list[Face],
    lower_start: int,
    upper_start: int,
    count: int,
    *,
    reverse: bool = False,
) -> None:
    for point_index in range(count):
        next_index = (point_index + 1) % count
        a = lower_start + point_index
        b = lower_start + next_index
        c = upper_start + next_index
        d = upper_start + point_index
        if reverse:
            faces.extend(((a, c, b), (a, d, c)))
        else:
            faces.extend(((a, b, c), (a, c, d)))


def build_lamp_mesh(
    outer_rings: Sequence[Ring],
    wall: float,
    base: float,
    hole_diameter: float,
    top_lip_segments: int,
) -> tuple[Mesh, dict[str, float | int]]:
    """Build the entire lamp as one connected, watertight indexed mesh."""
    outer_rings = [list(ring) for ring in outer_rings]
    point_count = len(outer_rings[0])
    if any(len(ring) != point_count for ring in outer_rings):
        raise ValueError("All rings must contain the same number of points")

    height = ring_average_z(outer_rings[-1])
    if not (0.0 < base < height):
        raise ValueError("Base height must be greater than zero and below total height")
    if hole_diameter <= 0:
        raise ValueError("Hole diameter must be positive")
    if top_lip_segments < 4 or top_lip_segments % 2:
        raise ValueError("Top-lip segments must be an even integer of at least 4")

    # Rounded inward return at the top.  Its half-round cross-section uses the
    # wall thickness as its diameter: the exterior joins at H-wall/2, rises to
    # a soft crest at H, then curls inward to the inner wall at H-wall/2.
    lip_radius = wall / 2.0
    lip_join_z = height - lip_radius
    previous_ring_max_z = max(point[2] for point in outer_rings[-2])
    if previous_ring_max_z >= lip_join_z - 1e-6:
        raise ValueError(
            "Top lip overlaps the preceding source ring; reduce --wall or increase --height"
        )
    outer_rings[-1] = [(x, y, lip_join_z) for x, y, _ in outer_rings[-1]]

    points: list[Point] = []
    faces: list[Face] = []

    # Outer source surface, including its original flat bottom and top rings.
    outer_starts = [add_ring(points, ring) for ring in outer_rings]
    for lower, upper in zip(outer_starts, outer_starts[1:]):
        stitch_rings(faces, lower, upper, point_count)

    # A single flat inner-floor boundary replaces the old overlapping base and
    # open shell.  Start the organic inner wall at the first ring wholly above
    # this floor, preventing clipped/inverted triangles at the transition.
    floor_outer_profile = interpolate_profile_at_z(outer_rings, base)
    inner_floor = radial_offset_inward(floor_outer_profile, wall)
    inner_rings: list[Ring] = [inner_floor]
    first_organic_inner_index = -1
    for index, ring in enumerate(outer_rings):
        if min(point[2] for point in ring) > base + 1e-6:
            first_organic_inner_index = index
            inner_rings.extend(
                radial_offset_inward(candidate, wall)
                for candidate in outer_rings[index:]
            )
            break
    if first_organic_inner_index < 0:
        raise ValueError("No source ring lies wholly above the requested base")

    inner_starts = [add_ring(points, ring) for ring in inner_rings]
    for lower, upper in zip(inner_starts, inner_starts[1:]):
        stitch_rings(faces, lower, upper, point_count, reverse=True)

    # Rounded top lip: explicit intermediate rings form a gentle half-round
    # inward return instead of the old abrupt horizontal annulus.
    outer_top = outer_starts[-1]
    inner_top = inner_starts[-1]
    rim_starts = [outer_top]
    outer_top_ring = outer_rings[-1]
    for segment in range(1, top_lip_segments):
        angle = math.pi * segment / top_lip_segments
        radial_inset = lip_radius * (1.0 - math.cos(angle))
        rim_z = lip_join_z + lip_radius * math.sin(angle)
        rim_ring: Ring = []
        for x, y, _ in outer_top_ring:
            radius = math.hypot(x, y)
            scale = (radius - radial_inset) / radius
            rim_ring.append((x * scale, y * scale, rim_z))
        rim_starts.append(add_ring(points, rim_ring))
    rim_starts.append(inner_top)
    for outer_edge, inner_edge in zip(rim_starts, rim_starts[1:]):
        stitch_rings(faces, outer_edge, inner_edge, point_count)

    # Bottom annulus, hole tube, and inner floor are all stitched through the
    # same point loops; there are no coincident or merely-overlapping surfaces.
    hole_radius = hole_diameter / 2.0
    if min(math.hypot(x, y) for x, y, _ in inner_floor) <= hole_radius:
        raise ValueError("Hole is too large for the inner floor profile")

    hole_bottom = circular_ring_from_angles(outer_rings[0], hole_radius, 0.0)
    hole_top = circular_ring_from_angles(inner_floor, hole_radius, base)
    hole_bottom_start = add_ring(points, hole_bottom)
    hole_top_start = add_ring(points, hole_top)

    outer_bottom = outer_starts[0]
    inner_floor_start = inner_starts[0]
    for index in range(point_count):
        next_index = (index + 1) % point_count

        # Downward-facing bottom annulus.
        faces.extend(
            (
                (outer_bottom + index, hole_bottom_start + index, hole_bottom_start + next_index),
                (outer_bottom + index, hole_bottom_start + next_index, outer_bottom + next_index),
            )
        )

        # Inward-facing cylindrical hole wall.
        faces.extend(
            (
                (hole_bottom_start + index, hole_top_start + index, hole_top_start + next_index),
                (hole_bottom_start + index, hole_top_start + next_index, hole_bottom_start + next_index),
            )
        )

        # Upward-facing inner floor annulus.
        faces.extend(
            (
                (inner_floor_start + index, inner_floor_start + next_index, hole_top_start + next_index),
                (inner_floor_start + index, hole_top_start + next_index, hole_top_start + index),
            )
        )

    metadata: dict[str, float | int] = {
        "outer_rings": len(outer_rings),
        "inner_rings": len(inner_rings),
        "points_per_ring": point_count,
        "first_organic_inner_outer_ring": first_organic_inner_index,
        "first_organic_inner_min_z_mm": min(
            point[2] for point in outer_rings[first_organic_inner_index]
        ),
        "floor_z_mm": base,
        "radial_wall_mm": wall,
        "hole_diameter_mm": hole_diameter,
        "top_lip_radius_mm": lip_radius,
        "top_lip_segments": top_lip_segments,
        "top_lip_join_z_mm": lip_join_z,
        "top_lip_crest_z_mm": height,
    }
    return Mesh(points, faces), metadata


def subtract(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Point, b: Point) -> Point:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a: Point, b: Point) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1


def inspect_mesh(mesh: Mesh) -> MeshReport:
    edge_counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    used_vertices: set[int] = set()
    canonical_faces: set[tuple[int, int, int]] = set()
    duplicate_faces = 0
    degenerate_faces = 0
    minimum_area = math.inf
    signed_volume = 0.0
    union_find = UnionFind(len(mesh.points))

    for face in mesh.faces:
        if len(set(face)) != 3:
            degenerate_faces += 1
        canonical = tuple(sorted(face))
        if canonical in canonical_faces:
            duplicate_faces += 1
        canonical_faces.add(canonical)

        a, b, c = (mesh.points[index] for index in face)
        normal = cross(subtract(b, a), subtract(c, a))
        area = 0.5 * math.sqrt(dot(normal, normal))
        minimum_area = min(minimum_area, area)
        if area <= 1e-10:
            degenerate_faces += 1
        signed_volume += dot(a, cross(b, c)) / 6.0

        for left, right in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
            edge = (left, right) if left < right else (right, left)
            edge_counts[edge] += 1
            used_vertices.update((left, right))
            union_find.union(left, right)

    components = len({union_find.find(index) for index in used_vertices})
    minimums = [min(point[axis] for point in mesh.points) for axis in range(3)]
    maximums = [max(point[axis] for point in mesh.points) for axis in range(3)]
    boundary_edges = sum(count == 1 for count in edge_counts.values())
    nonmanifold_edges = sum(count > 2 for count in edge_counts.values())
    unused_vertices = len(mesh.points) - len(used_vertices)
    watertight = (
        boundary_edges == 0
        and nonmanifold_edges == 0
        and components == 1
        and unused_vertices == 0
        and degenerate_faces == 0
        and duplicate_faces == 0
    )

    return MeshReport(
        vertices=len(mesh.points),
        faces=len(mesh.faces),
        unique_edges=len(edge_counts),
        boundary_edges=boundary_edges,
        nonmanifold_edges=nonmanifold_edges,
        connected_components=components,
        unused_vertices=unused_vertices,
        degenerate_faces=degenerate_faces,
        duplicate_faces=duplicate_faces,
        signed_volume_mm3=signed_volume,
        minimum_triangle_area_mm2=minimum_area,
        bounds_min_mm=minimums,
        bounds_max_mm=maximums,
        size_mm=[maximum - minimum for minimum, maximum in zip(minimums, maximums)],
        watertight=watertight,
    )


def ensure_outward_orientation(mesh: Mesh) -> MeshReport:
    report = inspect_mesh(mesh)
    if report.signed_volume_mm3 < 0:
        mesh.faces = [(a, c, b) for a, b, c in mesh.faces]
        report = inspect_mesh(mesh)
    return report


def normal_for_face(mesh: Mesh, face: Face) -> Point:
    a, b, c = (mesh.points[index] for index in face)
    value = cross(subtract(b, a), subtract(c, a))
    length = math.sqrt(dot(value, value))
    if length <= 1e-15:
        return (0.0, 0.0, 0.0)
    return (value[0] / length, value[1] / length, value[2] / length)


def write_binary_stl(path: Path, mesh: Mesh) -> None:
    with path.open("wb") as handle:
        header = b"Illinois Sandstone Lamp v2 - detail preserving manifold mesh"
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


def write_scad(path: Path, mesh: Mesh, parameters: Parameters) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "// Illinois Sandstone Lamp v2\n"
            "// Generated by generate_sandstone_v2.py\n"
            "// One watertight mesh; source rings preserved; seamless base transition.\n"
            f"// height={parameters.height} layers={parameters.layers} wall={parameters.wall} "
            f"base={parameters.base} hole={parameters.hole}\n\n"
            "/* [Height Fine-Tuning] */\n"
            "fine_tune_scale = 1.0;  // [0.90:0.001:1.10]\n\n"
            "scale([1, 1, fine_tune_scale])\n"
            "polyhedron(\n  points = [\n"
        )
        for index, (x, y, z) in enumerate(mesh.points):
            comma = "," if index + 1 < len(mesh.points) else ""
            handle.write(f"    [{x:.6f}, {y:.6f}, {z:.6f}]{comma}\n")
        handle.write("  ],\n  faces = [\n")
        for index, (a, b, c) in enumerate(mesh.faces):
            comma = "," if index + 1 < len(mesh.faces) else ""
            handle.write(f"    [{a}, {b}, {c}]{comma}\n")
        handle.write("  ],\n  convexity = 12\n);\n")


def model_xml(mesh: Mesh) -> Iterable[str]:
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    yield '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
    yield '  <metadata name="Title">Illinois Sandstone Lamp v2</metadata>\n'
    yield '  <metadata name="Application">generate_sandstone_v2.py</metadata>\n'
    yield '  <resources>\n    <object id="1" type="model">\n      <mesh>\n        <vertices>\n'
    for x, y, z in mesh.points:
        yield f'          <vertex x="{x:.7f}" y="{y:.7f}" z="{z:.7f}"/>\n'
    yield '        </vertices>\n        <triangles>\n'
    for a, b, c in mesh.faces:
        yield f'          <triangle v1="{a}" v2="{b}" v3="{c}"/>\n'
    yield '        </triangles>\n      </mesh>\n    </object>\n  </resources>\n'
    yield '  <build>\n    <item objectid="1" printable="1"/>\n  </build>\n</model>\n'


def write_3mf(path: Path, mesh: Mesh) -> None:
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


def write_report(
    path: Path,
    parameters: Parameters,
    report: MeshReport,
    build_metadata: dict[str, float | int],
    outputs: Sequence[Path],
) -> None:
    payload = {
        "generator": "generate_sandstone_v2.py",
        "parameters": asdict(parameters),
        "construction": build_metadata,
        "mesh": asdict(report),
        "outputs": [str(output) for output in outputs],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_formats(value: str) -> list[str]:
    formats = [item.strip().lower() for item in value.split(",") if item.strip()]
    allowed = {"stl", "3mf", "scad", "json"}
    invalid = sorted(set(formats) - allowed)
    if invalid:
        raise argparse.ArgumentTypeError(f"Unsupported formats: {', '.join(invalid)}")
    if not formats:
        raise argparse.ArgumentTypeError("At least one output format is required")
    return formats


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a source-detail-preserving watertight sandstone lamp mesh",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--height", type=float, default=DEFAULT_HEIGHT, help="total height in mm")
    parser.add_argument("--layers", type=int, default=DEFAULT_LAYERS, help="outer source/resampling rings")
    parser.add_argument("--wall", type=float, default=DEFAULT_WALL, help="radial wall thickness in mm")
    parser.add_argument("--base", type=float, default=DEFAULT_BASE, help="flat inner-floor height in mm")
    parser.add_argument("--hole", type=float, default=DEFAULT_HOLE, help="center-hole diameter in mm")
    parser.add_argument(
        "--top-lip-segments",
        type=int,
        default=DEFAULT_TOP_LIP_SEGMENTS,
        help="even segment count for the rounded inward top return",
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="original 120 mm SCAD source")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="output directory")
    parser.add_argument("--name", default=None, help="output basename without extension")
    parser.add_argument(
        "--formats",
        type=parse_formats,
        default=parse_formats("stl,3mf,scad,json"),
        help="comma-separated output formats: stl,3mf,scad,json",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    if args.height <= 0 or args.wall <= 0 or args.base <= 0 or args.hole <= 0:
        raise ValueError("Height, wall, base, and hole must all be positive")

    source_path = args.source.resolve()
    source_rings = read_source_rings(source_path)
    preserved = source_preserving_resample(source_rings, args.layers)
    outer_rings = scale_rings_to_height(preserved, args.height)

    parameters = Parameters(
        height=args.height,
        layers=args.layers,
        wall=args.wall,
        base=args.base,
        hole=args.hole,
        top_lip_segments=args.top_lip_segments,
        source=str(source_path),
    )
    mesh, build_metadata = build_lamp_mesh(
        outer_rings,
        args.wall,
        args.base,
        args.hole,
        args.top_lip_segments,
    )
    report = ensure_outward_orientation(mesh)
    if not report.watertight:
        raise RuntimeError(
            "Generated mesh failed validation: "
            f"boundary={report.boundary_edges}, nonmanifold={report.nonmanifold_edges}, "
            f"components={report.connected_components}, degenerate={report.degenerate_faces}"
        )

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.name or (
        f"illinois_sandstone_v2_{format_number(args.height)}mm_"
        f"{args.layers}L_wall{format_number(args.wall)}_"
        f"base{format_number(args.base)}_hole{format_number(args.hole)}"
    )

    outputs: list[Path] = []
    for output_format in args.formats:
        if output_format == "json":
            continue
        path = output_dir / f"{basename}.{output_format}"
        if output_format == "stl":
            write_binary_stl(path, mesh)
        elif output_format == "3mf":
            write_3mf(path, mesh)
        elif output_format == "scad":
            write_scad(path, mesh, parameters)
        outputs.append(path)

    if "json" in args.formats:
        report_path = output_dir / f"{basename}.report.json"
        write_report(report_path, parameters, report, build_metadata, outputs)
        outputs.append(report_path)

    print("Illinois Sandstone Lamp v2")
    print(f"  Source rings retained: {len(source_rings)} / {len(source_rings)}")
    print(f"  Output rings:          {args.layers}")
    print(f"  Vertices / faces:      {report.vertices:,} / {report.faces:,}")
    print(f"  Size (mm):             " + " x ".join(f"{value:.3f}" for value in report.size_mm))
    print(f"  Boundary edges:        {report.boundary_edges}")
    print(f"  Non-manifold edges:    {report.nonmanifold_edges}")
    print(f"  Components:            {report.connected_components}")
    print(f"  Watertight:            {'YES' if report.watertight else 'NO'}")
    for output in outputs:
        print(f"  Wrote: {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
