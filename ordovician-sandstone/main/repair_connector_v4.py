#!/usr/bin/env python3
"""Repair and Boolean-unify the legacy 80 mm lamp connector for lamp v4.

The source STL contains several overlapping closed pieces and one inner puck
with a very small number of malformed edges.  This preparation step repairs
only that malformed component, preserves every already-valid component, and
uses Manifold to combine the pieces into one printable solid.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from importlib.metadata import version
import json
from pathlib import Path
import sys
from typing import Sequence

try:
    import manifold3d as manifold
    import numpy as np
    import pymeshfix
except ImportError as error:  # pragma: no cover - exercised by end users
    raise SystemExit(
        "Lamp v4 dependencies are missing. Run: "
        "python3 -m pip install -r requirements-v4.txt"
    ) from error

from generate_base_v4 import extract_faces, face_components
from generate_sandstone_v2 import (
    Mesh,
    ensure_outward_orientation,
    inspect_mesh,
    read_binary_stl,
    write_binary_stl,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_SOURCE = PROJECT_DIR / "files" / "connect" / "80mm-lamp-attach-base.stl"
DEFAULT_OUTPUT = (
    PROJECT_DIR / "files" / "connect" / "80mm-lamp-attach-base-manifold-v4.stl"
)
DEFAULT_REPORT = (
    PROJECT_DIR
    / "files"
    / "connect"
    / "80mm-lamp-attach-base-manifold-v4.report.json"
)


def to_manifold(mesh: Mesh) -> manifold.Manifold:
    value = manifold.Manifold(
        manifold.Mesh(
            np.asarray(mesh.points, dtype=np.float32),
            np.asarray(mesh.faces, dtype=np.uint32),
        )
    )
    if value.status() != manifold.Error.NoError:
        raise RuntimeError(f"Manifold rejected connector component: {value.status()}")
    return value


def from_manifold(value: manifold.Manifold) -> Mesh:
    result = value.to_mesh()
    return Mesh(
        [tuple(map(float, point[:3])) for point in result.vert_properties],
        [tuple(map(int, face)) for face in result.tri_verts],
    )


def weld_exact_and_remove_degenerate(mesh: Mesh) -> Mesh:
    """Collapse identical output coordinates and discard zero-index faces.

    Manifold may retain separate indexed vertices at Boolean property seams.
    STL and basic 3MF do not carry its merge-vector metadata, so v4 performs
    the equivalent exact weld before export.
    """
    points: list[tuple[float, float, float]] = []
    point_indices: dict[tuple[float, float, float], int] = {}
    old_to_new: list[int] = []
    for point in mesh.points:
        if point not in point_indices:
            point_indices[point] = len(points)
            points.append(point)
        old_to_new.append(point_indices[point])

    faces: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int, int]] = set()
    for face in mesh.faces:
        remapped = tuple(old_to_new[index] for index in face)
        if len(set(remapped)) != 3:
            continue
        canonical = tuple(sorted(remapped))
        if canonical in seen:
            continue
        seen.add(canonical)
        faces.append(remapped)
    return Mesh(points, faces)


def repair_connector(source: Path) -> tuple[Mesh, dict[str, object]]:
    original = read_binary_stl(source)
    component_faces = face_components(original)
    if len(component_faces) < 2:
        raise ValueError("Expected the legacy connector to contain multiple components")

    manifolds: list[manifold.Manifold] = []
    repaired_components = 0
    component_summary: list[dict[str, object]] = []
    for index, face_indices in enumerate(component_faces):
        component = extract_faces(original, face_indices)
        before = ensure_outward_orientation(component)
        was_repaired = False
        if not before.watertight:
            fixer = pymeshfix.MeshFix(
                np.asarray(component.points), np.asarray(component.faces)
            )
            fixer.repair(joincomp=False, remove_smallest_components=False)
            component = Mesh(
                [tuple(map(float, point)) for point in fixer.points],
                [tuple(map(int, face)) for face in fixer.faces],
            )
            repaired_components += 1
            was_repaired = True

        after = ensure_outward_orientation(component)
        if not after.watertight:
            raise RuntimeError(
                f"Connector component {index} is still invalid after repair: "
                f"boundary={after.boundary_edges}, nonmanifold={after.nonmanifold_edges}"
            )
        manifolds.append(to_manifold(component))
        component_summary.append(
            {
                "index": index,
                "source_faces": len(face_indices),
                "output_faces": after.faces,
                "repaired": was_repaired,
            }
        )

    unified = manifold.Manifold.batch_boolean(manifolds, manifold.OpType.Add)
    if unified.status() != manifold.Error.NoError:
        raise RuntimeError(f"Connector Boolean union failed: {unified.status()}")
    mesh = weld_exact_and_remove_degenerate(from_manifold(unified))
    report = ensure_outward_orientation(mesh)
    if not report.watertight:
        raise RuntimeError(
            "Prepared connector failed validation: "
            f"boundary={report.boundary_edges}, nonmanifold={report.nonmanifold_edges}, "
            f"degenerate={report.degenerate_faces}"
        )
    metadata: dict[str, object] = {
        "source": str(source),
        "source_components": len(component_faces),
        "repaired_components": repaired_components,
        "components": component_summary,
        "boolean_engine": f"manifold3d {version('manifold3d')}",
        "mesh": asdict(report),
    }
    return mesh, metadata


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Repair and unify the legacy 80 mm lamp connector"
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    mesh, metadata = repair_connector(args.source.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_binary_stl(args.output.resolve(), mesh)
    args.report.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    report = inspect_mesh(mesh)
    print("Illinois Sandstone connector v4 preparation")
    print(f"  Vertices / faces:      {report.vertices:,} / {report.faces:,}")
    print(f"  Boundary edges:        {report.boundary_edges}")
    print(f"  Non-manifold edges:    {report.nonmanifold_edges}")
    print(f"  Components:            {report.connected_components}")
    print(f"  Watertight:            {'YES' if report.watertight else 'NO'}")
    print(f"  Wrote: {args.output.resolve()}")
    print(f"  Wrote: {args.report.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
