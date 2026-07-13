#!/usr/bin/env python3
"""Generate the AC screen support insert and fit gauges as manifold STL meshes.

All dimensions are millimeters. The production part is designed for nominal
20 x 20 x 1 mm square aluminum tube (18 mm nominal inside width), ASA-CF,
and an M5 x 7.1 x 9.5 mm heat-set insert.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


OUT_DIR = Path(__file__).resolve().parent
SEGMENTS = 64


def rounded_square(width: float, radius: float, z: float) -> np.ndarray:
    """Return a counter-clockwise rounded-square ring with SEGMENTS points."""
    points: list[tuple[float, float, float]] = []
    half = width / 2.0
    per_corner = SEGMENTS // 4
    corners = [
        (half - radius, -half + radius, -90.0),
        (half - radius, half - radius, 0.0),
        (-half + radius, half - radius, 90.0),
        (-half + radius, -half + radius, 180.0),
    ]
    for cx, cy, start_angle in corners:
        for i in range(per_corner):
            # Exclude each arc's endpoint because it is the next arc's start.
            # This avoids coincident vertices and zero-area STL triangles.
            angle = math.radians(start_angle + 90.0 * i / per_corner)
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle), z))
    return np.asarray(points, dtype=float)


def circle(diameter: float, z: float, start_degrees: float = -50.0) -> np.ndarray:
    # Align the circular ring with the rounded-square ring's first point so the
    # planar annulus triangulation stays local and does not spiral around the hole.
    angles = np.linspace(0.0, 2.0 * math.pi, SEGMENTS, endpoint=False) + math.radians(start_degrees)
    radius = diameter / 2.0
    return np.column_stack((radius * np.cos(angles), radius * np.sin(angles), np.full(SEGMENTS, z)))


class MeshBuilder:
    def __init__(self) -> None:
        self.vertices: list[tuple[float, float, float]] = []
        self.faces: list[tuple[int, int, int]] = []

    def add_ring(self, ring: np.ndarray) -> list[int]:
        start = len(self.vertices)
        self.vertices.extend(map(tuple, ring.tolist()))
        return list(range(start, start + len(ring)))

    def connect(self, lower: list[int], upper: list[int], *, reverse: bool = False) -> None:
        """Connect equal-length rings; normal points outward unless reverse=True."""
        count = len(lower)
        for i in range(count):
            j = (i + 1) % count
            tris = [
                (lower[i], lower[j], upper[j]),
                (lower[i], upper[j], upper[i]),
            ]
            if reverse:
                tris = [(a, c, b) for a, b, c in tris]
            self.faces.extend(tris)

    def annulus(self, outer: list[int], inner: list[int], *, upward: bool) -> None:
        count = len(outer)
        for i in range(count):
            j = (i + 1) % count
            tris = [
                (outer[i], outer[j], inner[j]),
                (outer[i], inner[j], inner[i]),
            ]
            if not upward:
                tris = [(a, c, b) for a, b, c in tris]
            self.faces.extend(tris)

    def cap(self, ring: list[int], center: tuple[float, float, float], *, upward: bool) -> None:
        center_index = len(self.vertices)
        self.vertices.append(center)
        for i in range(len(ring)):
            j = (i + 1) % len(ring)
            tri = (center_index, ring[i], ring[j])
            self.faces.append(tri if upward else (tri[0], tri[2], tri[1]))

    def arrays(self) -> tuple[np.ndarray, np.ndarray]:
        return np.asarray(self.vertices, dtype=float), np.asarray(self.faces, dtype=np.int64)


def make_insert(stem_width: float = 17.7) -> tuple[np.ndarray, np.ndarray]:
    flange_width = 23.0
    flange_radius = 1.8
    flange_thickness = 3.0
    stem_radius = 1.5
    insertion_depth = 40.0
    tip_chamfer = 1.0
    pilot_diameter = 6.4
    pocket_depth = 10.5
    entrance_chamfer = 0.5

    mesh = MeshBuilder()
    flange_bottom = mesh.add_ring(rounded_square(flange_width, flange_radius, 0.0))
    hole_opening = mesh.add_ring(circle(pilot_diameter + 2.0 * entrance_chamfer, 0.0))
    flange_at_chamfer = mesh.add_ring(rounded_square(flange_width, flange_radius, entrance_chamfer))
    hole_pilot = mesh.add_ring(circle(pilot_diameter, entrance_chamfer))
    flange_top = mesh.add_ring(rounded_square(flange_width, flange_radius, flange_thickness))
    hole_at_flange_top = mesh.add_ring(circle(pilot_diameter, flange_thickness))
    stem_base = mesh.add_ring(rounded_square(stem_width, stem_radius, flange_thickness))
    hole_end = mesh.add_ring(circle(pilot_diameter, pocket_depth))
    stem_before_tip = mesh.add_ring(
        rounded_square(stem_width, stem_radius, flange_thickness + insertion_depth - tip_chamfer)
    )
    tip_width = stem_width - 2.0 * tip_chamfer
    tip = mesh.add_ring(
        rounded_square(tip_width, max(0.5, stem_radius - 0.35), flange_thickness + insertion_depth)
    )

    mesh.annulus(flange_bottom, hole_opening, upward=False)
    mesh.connect(flange_bottom, flange_at_chamfer)
    mesh.connect(hole_opening, hole_pilot, reverse=True)
    mesh.connect(flange_at_chamfer, flange_top)
    mesh.connect(hole_pilot, hole_at_flange_top, reverse=True)
    mesh.annulus(flange_top, stem_base, upward=True)
    mesh.connect(stem_base, stem_before_tip)
    mesh.connect(hole_at_flange_top, hole_end, reverse=True)
    mesh.cap(hole_end, (0.0, 0.0, pocket_depth), upward=False)
    mesh.connect(stem_before_tip, tip)
    mesh.cap(tip, (0.0, 0.0, flange_thickness + insertion_depth), upward=True)
    return mesh.arrays()


def make_fit_gauge(stem_width: float) -> tuple[np.ndarray, np.ndarray]:
    """Create a quick 10 mm insertion gauge without the hardware pocket."""
    flange_width = 22.0
    flange_thickness = 2.0
    stem_depth = 10.0
    tip_chamfer = 1.0
    mesh = MeshBuilder()
    bottom = mesh.add_ring(rounded_square(flange_width, 1.5, 0.0))
    flange_top = mesh.add_ring(rounded_square(flange_width, 1.5, flange_thickness))
    stem_base = mesh.add_ring(rounded_square(stem_width, 1.2, flange_thickness))
    before_tip = mesh.add_ring(rounded_square(stem_width, 1.2, flange_thickness + stem_depth - tip_chamfer))
    tip = mesh.add_ring(
        rounded_square(stem_width - 2.0 * tip_chamfer, 0.85, flange_thickness + stem_depth)
    )
    mesh.cap(bottom, (0.0, 0.0, 0.0), upward=False)
    mesh.connect(bottom, flange_top)
    mesh.annulus(flange_top, stem_base, upward=True)
    mesh.connect(stem_base, before_tip)
    mesh.connect(before_tip, tip)
    mesh.cap(tip, (0.0, 0.0, flange_thickness + stem_depth), upward=True)
    return mesh.arrays()


def signed_volume(vertices: np.ndarray, faces: np.ndarray) -> float:
    triangles = vertices[faces]
    return float(np.einsum("ij,ij->i", triangles[:, 0], np.cross(triangles[:, 1], triangles[:, 2])).sum() / 6.0)


def verify(vertices: np.ndarray, faces: np.ndarray, expected_bounds: tuple[float, float, float]) -> dict[str, object]:
    edges: dict[tuple[int, int], int] = {}
    for face in faces:
        for a, b in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
            edge = tuple(sorted((int(a), int(b))))
            edges[edge] = edges.get(edge, 0) + 1
    bad_edges = [edge for edge, count in edges.items() if count != 2]
    triangles = vertices[faces]
    double_areas = np.linalg.norm(
        np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]),
        axis=1,
    )
    bounds = np.ptp(vertices, axis=0)
    if bad_edges:
        raise ValueError(f"Mesh is not manifold: {len(bad_edges)} edges do not have two faces")
    if np.any(double_areas < 1e-9):
        raise ValueError(f"Mesh contains {int(np.count_nonzero(double_areas < 1e-9))} degenerate triangles")
    if not np.allclose(bounds, expected_bounds, atol=0.01):
        raise ValueError(f"Unexpected bounds {bounds}; expected {expected_bounds}")
    volume = signed_volume(vertices, faces)
    if volume <= 0:
        raise ValueError(f"Mesh winding is inverted or volume is invalid: {volume}")
    return {
        "vertices": len(vertices),
        "triangles": len(faces),
        "bounds_mm": [round(float(value), 3) for value in bounds],
        "volume_mm3": round(volume, 3),
        "manifold": True,
    }


def write_ascii_stl(path: Path, vertices: np.ndarray, faces: np.ndarray, name: str) -> None:
    with path.open("w", encoding="ascii", newline="\n") as output:
        output.write(f"solid {name}\n")
        for face in faces:
            triangle = vertices[face]
            normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
            length = np.linalg.norm(normal)
            normal = normal / length if length else np.zeros(3)
            output.write(
                f"  facet normal {normal[0]:.8g} {normal[1]:.8g} {normal[2]:.8g}\n"
                "    outer loop\n"
            )
            for vertex in triangle:
                output.write(f"      vertex {vertex[0]:.8g} {vertex[1]:.8g} {vertex[2]:.8g}\n")
            output.write("    endloop\n  endfacet\n")
        output.write(f"endsolid {name}\n")


def main() -> None:
    jobs = [
        ("ac_support_insert_17.7mm_ASA-CF.stl", make_insert(17.7), (23.0, 23.0, 43.0)),
        ("ac_support_insert_17.9mm_ASA-CF.stl", make_insert(17.9), (23.0, 23.0, 43.0)),
        ("ac_support_insert_18.0mm_ASA-CF.stl", make_insert(18.0), (23.0, 23.0, 43.0)),
    ]
    for width in (17.5, 17.7, 17.9):
        jobs.append(
            (
                f"fit_gauge_{width:.1f}mm.stl",
                make_fit_gauge(width),
                (22.0, 22.0, 12.0),
            )
        )

    for filename, (vertices, faces), expected_bounds in jobs:
        report = verify(vertices, faces, expected_bounds)
        write_ascii_stl(OUT_DIR / filename, vertices, faces, filename)
        print(f"{filename}: {report}")


if __name__ == "__main__":
    main()
