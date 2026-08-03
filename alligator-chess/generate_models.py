#!/usr/bin/env python3
"""Generate the Tomorrowland Alligators chess family as binary STL files.

The models deliberately use overlapping, individually watertight solids. Modern
slicers merge those volumes while slicing, and this keeps the source dependency-
free and easy to modify. Units are millimetres; every piece is oriented upright
on Z=0 and designed for support-free FDM printing.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


Vec = tuple[float, float, float]
Face = tuple[int, int, int]


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Vec, b: Vec) -> Vec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def normalize(v: Vec) -> Vec:
    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    return (0.0, 0.0, 0.0) if length == 0 else (v[0] / length, v[1] / length, v[2] / length)


def rotate_xyz(v: Vec, angles_deg: Vec) -> Vec:
    x, y, z = v
    ax, ay, az = (math.radians(a) for a in angles_deg)
    cy, sy = math.cos(ax), math.sin(ax)
    y, z = y * cy - z * sy, y * sy + z * cy
    cx, sx = math.cos(ay), math.sin(ay)
    x, z = x * cx + z * sx, -x * sx + z * cx
    cz, sz = math.cos(az), math.sin(az)
    return (x * cz - y * sz, x * sz + y * cz, z)


@dataclass
class Mesh:
    name: str
    vertices: list[Vec] = field(default_factory=list)
    faces: list[Face] = field(default_factory=list)
    solids: int = 0

    def append(self, vertices: Iterable[Vec], faces: Iterable[Face]) -> None:
        offset = len(self.vertices)
        vertices = list(vertices)
        self.vertices.extend(vertices)
        self.faces.extend((a + offset, b + offset, c + offset) for a, b, c in faces)
        self.solids += 1

    def bounds(self) -> tuple[Vec, Vec]:
        mins = tuple(min(v[i] for v in self.vertices) for i in range(3))
        maxs = tuple(max(v[i] for v in self.vertices) for i in range(3))
        return mins, maxs  # type: ignore[return-value]


def frustum(radius0: float, radius1: float, z0: float, z1: float, sides: int = 48,
            center: tuple[float, float] = (0.0, 0.0)) -> tuple[list[Vec], list[Face]]:
    """Closed vertical frustum with caps."""
    cx, cy = center
    vertices: list[Vec] = []
    for z, r in ((z0, radius0), (z1, radius1)):
        for i in range(sides):
            a = 2 * math.pi * i / sides
            vertices.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
    vertices.extend([(cx, cy, z0), (cx, cy, z1)])
    faces: list[Face] = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.extend([(i, j, sides + j), (i, sides + j, sides + i)])
        faces.append((2 * sides, j, i))
        faces.append((2 * sides + 1, sides + i, sides + j))
    return vertices, faces


def ellipsoid(center: Vec, radii: Vec, rings: int = 10, sides: int = 24,
              rotation: Vec = (0.0, 0.0, 0.0)) -> tuple[list[Vec], list[Face]]:
    """Closed low-poly ellipsoid with clean single-vertex poles."""
    vertices: list[Vec] = []
    top = add(center, rotate_xyz((0.0, 0.0, radii[2]), rotation))
    bottom = add(center, rotate_xyz((0.0, 0.0, -radii[2]), rotation))
    vertices.extend([bottom, top])
    for r in range(1, rings):
        phi = -math.pi / 2 + math.pi * r / rings
        for i in range(sides):
            theta = 2 * math.pi * i / sides
            p = (
                radii[0] * math.cos(phi) * math.cos(theta),
                radii[1] * math.cos(phi) * math.sin(theta),
                radii[2] * math.sin(phi),
            )
            vertices.append(add(center, rotate_xyz(p, rotation)))
    faces: list[Face] = []
    first = 2
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((0, first + j, first + i))
    for r in range(rings - 2):
        a0 = 2 + r * sides
        b0 = a0 + sides
        for i in range(sides):
            j = (i + 1) % sides
            faces.extend([(a0 + i, a0 + j, b0 + j), (a0 + i, b0 + j, b0 + i)])
    last = 2 + (rings - 2) * sides
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((1, last + i, last + j))
    return vertices, faces


def axis_frustum(start: Vec, end: Vec, radius0: float, radius1: float,
                 sides: int = 12, scale_x: float = 1.0) -> tuple[list[Vec], list[Face]]:
    """Closed tapered prism following an arbitrary axis.

    `scale_x` flattens or widens one local radial direction, useful for snouts
    and the king's diamond-section crossbar.
    """
    direction = normalize(sub(end, start))
    helper = (0.0, 0.0, 1.0) if abs(direction[2]) < 0.9 else (0.0, 1.0, 0.0)
    u = normalize(cross(direction, helper))
    v = normalize(cross(direction, u))
    vertices: list[Vec] = []
    for center, radius in ((start, radius0), (end, radius1)):
        for i in range(sides):
            a = 2 * math.pi * i / sides
            radial = (
                u[0] * math.cos(a) * radius * scale_x + v[0] * math.sin(a) * radius,
                u[1] * math.cos(a) * radius * scale_x + v[1] * math.sin(a) * radius,
                u[2] * math.cos(a) * radius * scale_x + v[2] * math.sin(a) * radius,
            )
            vertices.append(add(center, radial))
    vertices.extend([start, end])
    faces: list[Face] = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.extend([(i, j, sides + j), (i, sides + j, sides + i)])
        faces.append((2 * sides, j, i))
        faces.append((2 * sides + 1, sides + i, sides + j))
    return vertices, faces


def wedge_box(center: Vec, size_bottom: tuple[float, float], size_top: tuple[float, float],
              height: float, rotation: Vec = (0.0, 0.0, 0.0)) -> tuple[list[Vec], list[Face]]:
    """Closed tapered rectangular solid, with rotation about its center."""
    verts: list[Vec] = []
    for z, size in ((-height / 2, size_bottom), (height / 2, size_top)):
        sx, sy = size
        for x, y in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
            verts.append(add(center, rotate_xyz((x, y, z), rotation)))
    faces: list[Face] = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7)]
    for i in range(4):
        j = (i + 1) % 4
        faces.extend([(i, j, 4 + j), (i, 4 + j, 4 + i)])
    return verts, faces


def cone(center_xy: tuple[float, float], z0: float, height: float, radius: float,
         sides: int = 16) -> tuple[list[Vec], list[Face]]:
    return frustum(radius, 0.35, z0, z0 + height, sides, center_xy)


def add_base(mesh: Mesh, radius: float) -> None:
    mesh.append(*frustum(radius - 1.0, radius, 0.0, 2.2))
    mesh.append(*frustum(radius, radius, 2.2, 4.2))
    mesh.append(*frustum(radius, radius - 2.2, 4.2, 7.0))
    mesh.append(*frustum(radius - 2.2, radius - 3.0, 7.0, 8.2))


def add_streamlined_body(mesh: Mesh, base_radius: float, z_top: float, waist: float = 0.62) -> None:
    add_base(mesh, base_radius)
    mesh.append(*frustum(base_radius - 3.1, base_radius * waist, 7.6, z_top * 0.55))
    mesh.append(*frustum(base_radius * waist, base_radius * 0.72, z_top * 0.55, z_top - 3.5))
    mesh.append(*frustum(base_radius * 0.72, base_radius * 0.60, z_top - 3.5, z_top))


def add_gator_head(mesh: Mesh, z: float, scale: float = 1.0, snout_length: float = 9.0,
                   angle: float = 0.0, eyes: bool = True) -> None:
    """Add the family's recognizable broad brow and supported tapered muzzle."""
    mesh.append(*ellipsoid((0.0, 0.1, z), (5.4 * scale, 4.7 * scale, 3.8 * scale), rings=8, sides=24,
                           rotation=(angle, 0.0, 0.0)))
    # The muzzle uses an octagonal/decagonal section: faceted, printable, and intentionally retro.
    back = add((0.0, -1.8 * scale, z - 0.3 * scale), rotate_xyz((0.0, 0.0, 0.0), (angle, 0.0, 0.0)))
    front = add((0.0, -snout_length * scale, z + 0.4 * scale), rotate_xyz((0.0, 0.0, 0.0), (angle, 0.0, 0.0)))
    mesh.append(*axis_frustum(back, front, 3.0 * scale, 2.15 * scale, sides=8, scale_x=1.65))
    # A keel under the muzzle turns the underside into slicer-friendly 45-degree facets.
    mesh.append(*axis_frustum((0.0, -2.4 * scale, z - 1.1 * scale),
                              (0.0, -snout_length * 0.88 * scale, z - 0.2 * scale),
                              1.75 * scale, 0.75 * scale, sides=6, scale_x=1.35))
    if eyes:
        for x in (-3.35 * scale, 3.35 * scale):
            mesh.append(*ellipsoid((x, -1.8 * scale, z + 2.55 * scale),
                                   (1.25 * scale, 1.35 * scale, 1.25 * scale), rings=6, sides=16))


def pawn() -> Mesh:
    m = Mesh("alligator_pawn")
    add_base(m, 13.0)
    m.append(*ellipsoid((0, 0.5, 17.0), (7.3, 6.6, 10.0), rings=10, sides=28))
    add_gator_head(m, 28.0, scale=0.78, snout_length=7.3)
    # Single hatchling scute: the pawn's simple identifying top note.
    m.append(*cone((0.0, 1.7), 30.0, 5.7, 2.1, 14))
    return m


def rook() -> Mesh:
    m = Mesh("alligator_rook")
    add_streamlined_body(m, 15.0, 37.0, waist=0.72)
    add_gator_head(m, 39.5, scale=0.93, snout_length=8.0)
    # Four dorsal scutes form a crenellated fortress crown.
    for x in (-5.5, -1.8, 1.8, 5.5):
        m.append(*wedge_box((x, 1.0, 46.0), (3.1, 5.2), (2.4, 4.2), 8.0))
    m.append(*axis_frustum((-7.6, 1.0, 43.0), (7.6, 1.0, 43.0), 2.3, 2.3, sides=8, scale_x=1.0))
    return m


def knight() -> Mesh:
    m = Mesh("alligator_knight")
    add_base(m, 15.0)
    m.append(*frustum(11.8, 8.4, 7.6, 20.0))
    # A rearing S-curve made from overlapping streamlined neck volumes.
    m.append(*ellipsoid((0.0, 2.0, 29.0), (7.0, 6.0, 13.0), rings=10, sides=24, rotation=(-13, 0, 0)))
    m.append(*ellipsoid((0.0, -0.8, 43.0), (6.0, 5.2, 11.5), rings=10, sides=24, rotation=(13, 0, 0)))
    add_gator_head(m, 54.0, scale=0.94, snout_length=10.8, angle=4)
    # Swept-back scutes echo a knight's mane without thin unsupported fins.
    for y, z, tilt in ((3.4, 36.0, -18), (3.0, 43.0, -12), (2.4, 49.0, -7)):
        m.append(*wedge_box((0.0, y, z), (4.2, 4.5), (2.0, 2.4), 7.0, rotation=(tilt, 0, 45)))
    return m


def bishop() -> Mesh:
    m = Mesh("alligator_bishop")
    add_streamlined_body(m, 14.5, 48.0, waist=0.48)
    m.append(*ellipsoid((0.0, 0.0, 51.0), (6.1, 5.6, 6.8), rings=10, sides=24))
    add_gator_head(m, 54.0, scale=0.82, snout_length=8.4)
    # Split, leaning crest reads as a bishop's mitre; the open center avoids a fragile engraved slot.
    m.append(*wedge_box((-2.2, 1.1, 63.0), (3.6, 5.0), (1.1, 2.0), 13.0, rotation=(0, -12, -5)))
    m.append(*wedge_box((2.2, 1.1, 63.0), (3.6, 5.0), (1.1, 2.0), 13.0, rotation=(0, 12, 5)))
    return m


def queen() -> Mesh:
    m = Mesh("alligator_queen")
    add_streamlined_body(m, 16.0, 50.0, waist=0.56)
    m.append(*frustum(9.5, 7.0, 47.0, 57.0))
    add_gator_head(m, 58.0, scale=0.92, snout_length=9.0)
    # Five alternating scutes create a flowing crown silhouette.
    crown = [(-6.0, 0.8, 61.0, 9.0), (-3.1, 1.6, 62.0, 12.0),
             (0.0, 2.0, 62.0, 15.0), (3.1, 1.6, 62.0, 12.0), (6.0, 0.8, 61.0, 9.0)]
    for x, y, z0, h in crown:
        m.append(*cone((x, y), z0, h, 2.35, 14))
    m.append(*frustum(8.2, 7.2, 61.0, 64.0, sides=32, center=(0.0, 1.0)))
    return m


def king() -> Mesh:
    m = Mesh("alligator_king")
    add_streamlined_body(m, 16.5, 54.0, waist=0.60)
    m.append(*frustum(10.0, 7.4, 50.0, 62.0))
    add_gator_head(m, 63.0, scale=0.96, snout_length=9.3)
    # Tall central dorsal fin supports the iconic cross from below.
    m.append(*wedge_box((0.0, 1.5, 71.0), (6.2, 5.8), (3.2, 3.2), 15.0))
    # Diamond-section bar has self-supporting 45-degree lower facets.
    m.append(*axis_frustum((-8.5, 1.5, 74.8), (8.5, 1.5, 74.8), 2.4, 2.4, sides=4, scale_x=1.0))
    m.append(*cone((-5.8, 1.0), 65.0, 7.5, 2.2, 14))
    m.append(*cone((5.8, 1.0), 65.0, 7.5, 2.2, 14))
    return m


def normal(a: Vec, b: Vec, c: Vec) -> Vec:
    return normalize(cross(sub(b, a), sub(c, a)))


def write_binary_stl(mesh: Mesh, path: Path) -> None:
    header = f"Tomorrowland Alligators | {mesh.name} | mm | support-free".encode("ascii")[:80]
    header = header.ljust(80, b"\0")
    with path.open("wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(mesh.faces)))
        for ia, ib, ic in mesh.faces:
            a, b, c = mesh.vertices[ia], mesh.vertices[ib], mesh.vertices[ic]
            n = normal(a, b, c)
            f.write(struct.pack("<12fH", *(n + a + b + c), 0))


def validate(mesh: Mesh) -> dict[str, object]:
    """Run topology and dimensional checks before export."""
    edges: dict[tuple[int, int], int] = {}
    degenerate = 0
    for ia, ib, ic in mesh.faces:
        a, b, c = mesh.vertices[ia], mesh.vertices[ib], mesh.vertices[ic]
        area2 = math.sqrt(sum(q * q for q in cross(sub(b, a), sub(c, a))))
        if area2 < 1e-7:
            degenerate += 1
        for u, v in ((ia, ib), (ib, ic), (ic, ia)):
            edge = (min(u, v), max(u, v))
            edges[edge] = edges.get(edge, 0) + 1
    boundary_edges = sum(count != 2 for count in edges.values())
    mins, maxs = mesh.bounds()
    return {
        "triangles": len(mesh.faces),
        "solids": mesh.solids,
        "degenerate_triangles": degenerate,
        "nonmanifold_or_boundary_edges": boundary_edges,
        "size_mm": tuple(round(maxs[i] - mins[i], 2) for i in range(3)),
        "z_min": round(mins[2], 4),
    }


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "stl"
    output_dir.mkdir(exist_ok=True)
    models = [pawn(), rook(), knight(), bishop(), queen(), king()]
    report_lines = ["piece,triangles,closed_solids,nonmanifold_or_boundary_edges,degenerate_triangles,size_x_mm,size_y_mm,size_z_mm,z_min_mm"]
    for model in models:
        result = validate(model)
        if result["nonmanifold_or_boundary_edges"] or result["degenerate_triangles"] or result["z_min"] < -1e-6:
            raise RuntimeError(f"Validation failed for {model.name}: {result}")
        path = output_dir / f"{model.name}.stl"
        write_binary_stl(model, path)
        sx, sy, sz = result["size_mm"]  # type: ignore[misc]
        report_lines.append(
            f"{model.name},{result['triangles']},{result['solids']},0,0,{sx},{sy},{sz},{result['z_min']}"
        )
        print(f"{path.name:24s} {result}")
    (Path(__file__).resolve().parent / "mesh_report.csv").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
