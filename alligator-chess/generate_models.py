#!/usr/bin/env python3
"""Generate the faceted Tomorrowland Alligators chess family.

The visual language is an upright low-poly alligator bust: long wedge muzzle,
heavy brow, tapered chest, angular forelimbs, dorsal plates, and a stepped base.
Each chess piece keeps that complete figure and varies the silhouette at the
head/back. Units are millimetres and every model is upright on Z=0.
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


def mul(v: Vec, k: float) -> Vec:
    return (v[0] * k, v[1] * k, v[2] * k)


def cross(a: Vec, b: Vec) -> Vec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def normalize(v: Vec) -> Vec:
    length = math.sqrt(sum(q * q for q in v))
    return (0.0, 0.0, 0.0) if length == 0 else tuple(q / length for q in v)  # type: ignore[return-value]


def rotate_xyz(v: Vec, angles_deg: Vec) -> Vec:
    x, y, z = v
    ax, ay, az = (math.radians(a) for a in angles_deg)
    ca, sa = math.cos(ax), math.sin(ax)
    y, z = y * ca - z * sa, y * sa + z * ca
    ca, sa = math.cos(ay), math.sin(ay)
    x, z = x * ca + z * sa, -x * sa + z * ca
    ca, sa = math.cos(az), math.sin(az)
    return (x * ca - y * sa, x * sa + y * ca, z)


@dataclass
class Mesh:
    name: str
    vertices: list[Vec] = field(default_factory=list)
    faces: list[Face] = field(default_factory=list)
    solids: int = 0

    def append(self, vertices: Iterable[Vec], faces: Iterable[Face]) -> None:
        offset = len(self.vertices)
        self.vertices.extend(vertices)
        self.faces.extend((a + offset, b + offset, c + offset) for a, b, c in faces)
        self.solids += 1

    def bounds(self) -> tuple[Vec, Vec]:
        lo = tuple(min(v[i] for v in self.vertices) for i in range(3))
        hi = tuple(max(v[i] for v in self.vertices) for i in range(3))
        return lo, hi  # type: ignore[return-value]


def frustum(radius0: float, radius1: float, z0: float, z1: float, sides: int = 12,
            center: tuple[float, float] = (0.0, 0.0), phase: float = math.pi / 12) -> tuple[list[Vec], list[Face]]:
    cx, cy = center
    vertices: list[Vec] = []
    for z, radius in ((z0, radius0), (z1, radius1)):
        for i in range(sides):
            a = phase + 2 * math.pi * i / sides
            vertices.append((cx + radius * math.cos(a), cy + radius * math.sin(a), z))
    vertices.extend([(cx, cy, z0), (cx, cy, z1)])
    faces: list[Face] = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.extend([(i, j, sides + j), (i, sides + j, sides + i)])
        faces.append((2 * sides, j, i))
        faces.append((2 * sides + 1, sides + i, sides + j))
    return vertices, faces


def loft(rings: list[tuple[float, float, float, float, float]], sides: int = 10,
         phase: float = math.pi / 2) -> tuple[list[Vec], list[Face]]:
    """Closed faceted loft. Rings are (cx, cy, z, radius_x, radius_y)."""
    vertices: list[Vec] = []
    for cx, cy, z, rx, ry in rings:
        for i in range(sides):
            a = phase + 2 * math.pi * i / sides
            vertices.append((cx + rx * math.cos(a), cy + ry * math.sin(a), z))
    vertices.extend([(rings[0][0], rings[0][1], rings[0][2]),
                     (rings[-1][0], rings[-1][1], rings[-1][2])])
    faces: list[Face] = []
    for ring in range(len(rings) - 1):
        a0, b0 = ring * sides, (ring + 1) * sides
        for i in range(sides):
            j = (i + 1) % sides
            faces.extend([(a0 + i, a0 + j, b0 + j), (a0 + i, b0 + j, b0 + i)])
    bottom_center, top_center = len(vertices) - 2, len(vertices) - 1
    last = (len(rings) - 1) * sides
    for i in range(sides):
        j = (i + 1) % sides
        faces.extend([(bottom_center, j, i), (top_center, last + i, last + j)])
    return vertices, faces


def ellipsoid(center: Vec, radii: Vec, rings: int = 5, sides: int = 10,
              rotation: Vec = (0.0, 0.0, 0.0)) -> tuple[list[Vec], list[Face]]:
    vertices: list[Vec] = [
        add(center, rotate_xyz((0.0, 0.0, -radii[2]), rotation)),
        add(center, rotate_xyz((0.0, 0.0, radii[2]), rotation)),
    ]
    for ring in range(1, rings):
        phi = -math.pi / 2 + math.pi * ring / rings
        for i in range(sides):
            theta = 2 * math.pi * i / sides
            local = (radii[0] * math.cos(phi) * math.cos(theta),
                     radii[1] * math.cos(phi) * math.sin(theta),
                     radii[2] * math.sin(phi))
            vertices.append(add(center, rotate_xyz(local, rotation)))
    faces: list[Face] = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((0, 2 + j, 2 + i))
    for ring in range(rings - 2):
        a0, b0 = 2 + ring * sides, 2 + (ring + 1) * sides
        for i in range(sides):
            j = (i + 1) % sides
            faces.extend([(a0 + i, a0 + j, b0 + j), (a0 + i, b0 + j, b0 + i)])
    last = 2 + (rings - 2) * sides
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((1, last + i, last + j))
    return vertices, faces


def axis_profile_prism(start: Vec, end: Vec, start_profile: list[tuple[float, float]],
                       end_profile: list[tuple[float, float]] | None = None) -> tuple[list[Vec], list[Face]]:
    """Closed prism along an axis with matching arbitrary radial profiles."""
    end_profile = end_profile or start_profile
    if len(start_profile) != len(end_profile):
        raise ValueError("Profiles must have matching point counts")
    direction = normalize(sub(end, start))
    helper = (0.0, 0.0, 1.0) if abs(direction[2]) < 0.9 else (0.0, 1.0, 0.0)
    u = normalize(cross(direction, helper))
    v = normalize(cross(direction, u))
    vertices: list[Vec] = []
    for center, profile in ((start, start_profile), (end, end_profile)):
        for pu, pv in profile:
            vertices.append(add(center, add(mul(u, pu), mul(v, pv))))
    n = len(start_profile)
    vertices.extend([start, end])
    faces: list[Face] = []
    for i in range(n):
        j = (i + 1) % n
        faces.extend([(i, j, n + j), (i, n + j, n + i)])
        faces.extend([(2 * n, j, i), (2 * n + 1, n + i, n + j)])
    return vertices, faces


def axis_frustum(start: Vec, end: Vec, radius0: float, radius1: float,
                 sides: int = 6, flatten: float = 1.0) -> tuple[list[Vec], list[Face]]:
    a = [(math.cos(2 * math.pi * i / sides) * radius0 * flatten,
          math.sin(2 * math.pi * i / sides) * radius0) for i in range(sides)]
    b = [(math.cos(2 * math.pi * i / sides) * radius1 * flatten,
          math.sin(2 * math.pi * i / sides) * radius1) for i in range(sides)]
    return axis_profile_prism(start, end, a, b)


def muzzle_profile(width: float, height: float) -> list[tuple[float, float]]:
    """Chamfered muzzle with a narrow keel instead of a broad unsupported floor."""
    return [(x * width, z * height) for x, z in (
        (-0.07, -0.50), (0.07, -0.50), (0.50, -0.12), (0.50, 0.24),
        (0.31, 0.50), (-0.31, 0.50), (-0.50, 0.24), (-0.50, -0.12),
    )]


def wedge_box(center: Vec, bottom: tuple[float, float], top: tuple[float, float], height: float,
              rotation: Vec = (0.0, 0.0, 0.0)) -> tuple[list[Vec], list[Face]]:
    vertices: list[Vec] = []
    for z, size in ((-height / 2, bottom), (height / 2, top)):
        sx, sy = size
        for x, y in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2),
                     (sx / 2, sy / 2), (-sx / 2, sy / 2)):
            vertices.append(add(center, rotate_xyz((x, y, z), rotation)))
    faces: list[Face] = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7)]
    for i in range(4):
        j = (i + 1) % 4
        faces.extend([(i, j, 4 + j), (i, 4 + j, 4 + i)])
    return vertices, faces


def triangular_plate(width: float, y_base: float, z: float, height: float, depth: float) -> tuple[list[Vec], list[Face]]:
    profile = [(y_base, z - height / 2), (y_base + depth, z), (y_base, z + height / 2)]
    vertices = [(-width / 2, y, qz) for y, qz in profile] + [(width / 2, y, qz) for y, qz in profile]
    faces: list[Face] = [(0, 2, 1), (3, 4, 5)]
    for i in range(3):
        j = (i + 1) % 3
        faces.extend([(i, j, 3 + j), (i, 3 + j, 3 + i)])
    return vertices, faces


def add_base(mesh: Mesh, radius: float) -> None:
    mesh.append(*frustum(radius - 0.8, radius, 0.0, 1.6))
    mesh.append(*frustum(radius, radius, 1.6, 3.4))
    mesh.append(*frustum(radius, radius - 1.5, 3.4, 5.0))
    mesh.append(*frustum(radius - 1.8, radius - 1.2, 5.0, 6.5))
    mesh.append(*frustum(radius - 1.2, radius - 2.3, 6.5, 8.0))


def add_dorsal_row(mesh: Mesh, head_z: float, count: int, body_width: float,
                   blocky: bool = False, crown_scale: float = 1.0) -> None:
    low, high = 16.0, head_z + 1.0
    for i in range(count):
        t = i / max(1, count - 1)
        z = low + (high - low) * t
        width = (6.3 - 1.4 * t) * crown_scale
        depth = (4.1 + 1.0 * t) * crown_scale
        height = (7.0 - 0.8 * t) * crown_scale
        y_base = 6.7 - 0.8 * t
        if blocky:
            mesh.append(*wedge_box((0.0, y_base + depth * 0.35, z),
                                   (width, depth), (width * 0.9, depth * 0.82), height))
        else:
            mesh.append(*triangular_plate(width, y_base, z, height, depth))


def add_forelimbs(mesh: Mesh, head_z: float, body_width: float, compact: float = 1.0) -> None:
    for side in (-1.0, 1.0):
        shoulder = (side * body_width * 0.76, -1.7, head_z - 13.0)
        elbow = (side * body_width * 1.04, -4.0, head_z - 21.5 * compact)
        wrist = (side * body_width * 0.91, -6.0, head_z - 29.0 * compact)
        mesh.append(*wedge_box((side * body_width * 0.73, -1.4, head_z - 13.5),
                               (6.6, 7.2), (4.0, 4.4), 9.5, rotation=(0, side * 13, side * 2)))
        mesh.append(*axis_frustum(shoulder, elbow, 3.8, 3.0, sides=5, flatten=0.86))
        mesh.append(*axis_frustum(elbow, wrist, 3.1, 2.25, sides=5, flatten=0.84))
        mesh.append(*wedge_box((wrist[0], wrist[1] - 0.3, wrist[2] - 1.0),
                               (5.2, 5.4), (3.4, 3.5), 6.5, rotation=(0, side * 7, 0)))


def add_alligator_bust(mesh: Mesh, *, base_radius: float, head_z: float, body_width: float,
                       snout_length: float, dorsal_count: int, blocky_dorsal: bool = False,
                       arms_compact: float = 1.0, eye_scale: float = 1.0) -> None:
    add_base(mesh, base_radius)
    # One continuous decagonal torso/neck gives the reference's broad planar facets.
    mesh.append(*loft([
        (0.0, 1.0, 7.4, base_radius - 2.7, base_radius * 0.66),
        (0.0, 1.2, 12.0, body_width * 1.08, base_radius - 3.0),
        (0.0, 1.5, head_z - 24.0, body_width, base_radius - 3.7),
        (0.0, 1.0, head_z - 14.0, body_width * 0.82, base_radius - 5.3),
        (0.0, 0.0, head_z - 6.0, body_width * 0.64, base_radius - 8.0),
        (0.0, -1.2, head_z - 2.0, body_width * 0.68, base_radius - 8.5),
    ], sides=10))
    # Raised breast plane and throat make the creature feel sculpted rather than lathed.
    chest_height = max(12.0, head_z - 27.0)
    mesh.append(*wedge_box((0.0, -4.8, 10.0 + chest_height / 2),
                           (body_width * 1.38, 6.0), (body_width * 0.76, 4.1), chest_height))
    mesh.append(*wedge_box((0.0, -3.8, head_z - 9.0),
                           (body_width * 1.03, 6.3), (body_width * 0.78, 4.7), 15.0))
    # Low-poly cranium, long upper muzzle, and a thinner jaw create the signature profile.
    mesh.append(*ellipsoid((0.0, -1.8, head_z), (body_width * 0.73, 5.3, 5.2), rings=4, sides=10,
                           rotation=(-4.0, 0.0, 0.0)))
    upper_start = (0.0, -4.0, head_z + 0.3)
    upper_end = (0.0, -snout_length, head_z + 0.9)
    mesh.append(*axis_profile_prism(upper_start, upper_end,
                                    muzzle_profile(body_width * 1.12, 6.2),
                                    muzzle_profile(body_width * 0.72, 4.2)))
    jaw_start = (0.0, -4.1, head_z - 2.2)
    jaw_end = (0.0, -snout_length - 0.15, head_z - 1.3)
    mesh.append(*axis_profile_prism(jaw_start, jaw_end,
                                    muzzle_profile(body_width * 1.02, 3.2),
                                    muzzle_profile(body_width * 0.68, 2.25)))
    # Heavy angular eyebrow wedges cast a natural slit-like shadow over the eyes.
    for side in (-1.0, 1.0):
        x = side * body_width * 0.42
        mesh.append(*wedge_box((x, -5.0, head_z + 2.7), (body_width * 0.55, 3.1),
                               (body_width * 0.42, 2.1), 2.7, rotation=(-6, side * 9, side * 3)))
        mesh.append(*ellipsoid((side * body_width * 0.45, -5.35, head_z + 1.55),
                               (0.85 * eye_scale, 0.70, 0.72), rings=3, sides=8))
    add_forelimbs(mesh, head_z, body_width, compact=arms_compact)
    add_dorsal_row(mesh, head_z, dorsal_count, body_width, blocky=blocky_dorsal)


def add_rook_crest(mesh: Mesh, head_z: float, width: float) -> None:
    # Four squared cranial plates read as battlements while remaining part of the animal.
    for x in (-5.1, -1.7, 1.7, 5.1):
        mesh.append(*wedge_box((x, 1.8, head_z + 6.2), (3.2, 5.0), (2.8, 4.3), 9.0))
    mesh.append(*axis_frustum((-width * 0.72, 1.8, head_z + 2.6),
                              (width * 0.72, 1.8, head_z + 2.6), 2.2, 2.2, sides=6))


def add_bishop_crest(mesh: Mesh, head_z: float) -> None:
    # Two separated tapered planes form a clear mitre without a fragile cut slot.
    mesh.append(*wedge_box((-2.15, 1.2, head_z + 10.0), (4.0, 5.4), (1.0, 2.1), 18.0,
                           rotation=(0, -10, -3)))
    mesh.append(*wedge_box((2.15, 1.2, head_z + 10.0), (4.0, 5.4), (1.0, 2.1), 18.0,
                           rotation=(0, 10, 3)))


def add_queen_crest(mesh: Mesh, head_z: float) -> None:
    for x, extra in ((-6.0, 1.0), (-3.1, 4.0), (0.0, 7.0), (3.1, 4.0), (6.0, 1.0)):
        mesh.append(*wedge_box((x, 1.3, head_z + 7.0 + extra / 2),
                               (3.1, 4.2), (0.65, 1.1), 11.0 + extra,
                               rotation=(0, x * 1.1, 0)))
    mesh.append(*frustum(8.0, 7.1, head_z + 2.2, head_z + 5.0, sides=10, center=(0.0, 1.1)))


def add_king_crest(mesh: Mesh, head_z: float) -> None:
    mesh.append(*wedge_box((0.0, 1.4, head_z + 10.0), (5.4, 5.2), (3.3, 3.2), 18.0))
    # Diamond-section crossbar: its underside consists of self-supporting sloped faces.
    diamond = [(0.0, -2.5), (2.5, 0.0), (0.0, 2.5), (-2.5, 0.0)]
    mesh.append(*axis_profile_prism((-9.2, 1.4, head_z + 13.5),
                                    (9.2, 1.4, head_z + 13.5), diamond))


def pawn() -> Mesh:
    m = Mesh("alligator_pawn")
    add_alligator_bust(m, base_radius=13.5, head_z=36.5, body_width=7.1,
                       snout_length=10.8, dorsal_count=4, arms_compact=0.73, eye_scale=0.82)
    # A single low crown nub keeps the pawn simple and hatchling-like.
    m.append(*triangular_plate(4.6, 3.4, 40.0, 6.0, 3.3))
    return m


def rook() -> Mesh:
    m = Mesh("alligator_rook")
    add_alligator_bust(m, base_radius=15.4, head_z=47.5, body_width=8.3,
                       snout_length=12.0, dorsal_count=5, blocky_dorsal=True, arms_compact=0.90)
    add_rook_crest(m, 47.5, 8.3)
    return m


def knight() -> Mesh:
    m = Mesh("alligator_knight")
    add_alligator_bust(m, base_radius=15.5, head_z=55.0, body_width=8.5,
                       snout_length=14.8, dorsal_count=7, arms_compact=1.0)
    # The unadorned long-snouted rearing silhouette is the reference concept itself.
    return m


def bishop() -> Mesh:
    m = Mesh("alligator_bishop")
    add_alligator_bust(m, base_radius=15.2, head_z=52.0, body_width=7.7,
                       snout_length=13.0, dorsal_count=6, arms_compact=0.94)
    add_bishop_crest(m, 52.0)
    return m


def queen() -> Mesh:
    m = Mesh("alligator_queen")
    add_alligator_bust(m, base_radius=16.2, head_z=55.0, body_width=8.2,
                       snout_length=13.6, dorsal_count=7, arms_compact=0.96)
    add_queen_crest(m, 55.0)
    return m


def king() -> Mesh:
    m = Mesh("alligator_king")
    add_alligator_bust(m, base_radius=16.8, head_z=57.0, body_width=8.5,
                       snout_length=14.0, dorsal_count=7, arms_compact=0.98)
    add_king_crest(m, 57.0)
    return m


def face_normal(a: Vec, b: Vec, c: Vec) -> Vec:
    return normalize(cross(sub(b, a), sub(c, a)))


def write_binary_stl(mesh: Mesh, path: Path) -> None:
    header = f"Faceted Tomorrowland Alligators | {mesh.name} | millimetres".encode("ascii")[:80].ljust(80, b"\0")
    with path.open("wb") as stream:
        stream.write(header)
        stream.write(struct.pack("<I", len(mesh.faces)))
        for ia, ib, ic in mesh.faces:
            a, b, c = mesh.vertices[ia], mesh.vertices[ib], mesh.vertices[ic]
            stream.write(struct.pack("<12fH", *(face_normal(a, b, c) + a + b + c), 0))


def validate(mesh: Mesh) -> dict[str, object]:
    edges: dict[tuple[int, int], int] = {}
    degenerate = 0
    for ia, ib, ic in mesh.faces:
        a, b, c = mesh.vertices[ia], mesh.vertices[ib], mesh.vertices[ic]
        twice_area = math.sqrt(sum(q * q for q in cross(sub(b, a), sub(c, a))))
        degenerate += twice_area < 1e-7
        for u, v in ((ia, ib), (ib, ic), (ic, ia)):
            edge = (min(u, v), max(u, v))
            edges[edge] = edges.get(edge, 0) + 1
    bad_edges = sum(count != 2 for count in edges.values())
    lo, hi = mesh.bounds()
    return {
        "triangles": len(mesh.faces),
        "closed_solids": mesh.solids,
        "degenerate_triangles": degenerate,
        "nonmanifold_or_boundary_edges": bad_edges,
        "size_mm": tuple(round(hi[i] - lo[i], 2) for i in range(3)),
        "z_min": round(lo[2], 5),
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    output = root / "stl"
    output.mkdir(exist_ok=True)
    rows = ["piece,triangles,closed_solids,nonmanifold_or_boundary_edges,degenerate_triangles,size_x_mm,size_y_mm,size_z_mm,z_min_mm"]
    for model in (pawn(), rook(), knight(), bishop(), queen(), king()):
        report = validate(model)
        if report["nonmanifold_or_boundary_edges"] or report["degenerate_triangles"] or report["z_min"] < 0:
            raise RuntimeError(f"Validation failed for {model.name}: {report}")
        write_binary_stl(model, output / f"{model.name}.stl")
        sx, sy, sz = report["size_mm"]  # type: ignore[misc]
        rows.append(f"{model.name},{report['triangles']},{report['closed_solids']},0,0,{sx},{sy},{sz},{report['z_min']}")
        print(f"{model.name:22s} {report}")
    (root / "mesh_report.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
