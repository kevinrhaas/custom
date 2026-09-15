#!/usr/bin/env python3
"""Build and validate every STL for the parametric stand."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "stand.scad"
OUTPUT = ROOT / "files"

PARTS = {
    "stand_rail.stl": "rail",
    "stand_axle.stl": "axle",
    "stand_cap.stl": "cap",
    "stand_spacer.stl": "spacer",
    "stand_stop_pin.stl": "stop_pin",
    "stand_fit_test.stl": "fit_test",
    "stand_rails_x3.stl": "rails_plate",
    "stand_hardware_set.stl": "hardware_plate",
}


def read_binary_stl(path: Path):
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError(f"{path.name}: file is too short to be a binary STL")
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    expected = 84 + triangle_count * 50
    if len(data) != expected:
        raise ValueError(
            f"{path.name}: expected {expected} bytes for {triangle_count} "
            f"triangles, found {len(data)}"
        )

    triangles = []
    offset = 84
    for _ in range(triangle_count):
        values = struct.unpack_from("<12fH", data, offset)
        triangles.append((values[3:6], values[6:9], values[9:12]))
        offset += 50
    return triangles


def validate(path: Path) -> dict:
    triangles = read_binary_stl(path)
    vertices = [vertex for triangle in triangles for vertex in triangle]
    mins = [min(vertex[i] for vertex in vertices) for i in range(3)]
    maxs = [max(vertex[i] for vertex in vertices) for i in range(3)]

    def key(vertex):
        return tuple(round(value, 5) for value in vertex)

    edges = Counter()
    for triangle in triangles:
        points = [key(vertex) for vertex in triangle]
        for start, end in ((points[0], points[1]),
                           (points[1], points[2]),
                           (points[2], points[0])):
            edges[tuple(sorted((start, end)))] += 1

    open_edges = sum(1 for count in edges.values() if count != 2)
    if open_edges:
        raise ValueError(f"{path.name}: {open_edges} non-manifold/open edges")

    return {
        "file": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "triangles": len(triangles),
        "watertight": True,
        "bounds_mm": {
            "min": [round(value, 3) for value in mins],
            "max": [round(value, 3) for value in maxs],
            "size": [round(maxs[i] - mins[i], 3) for i in range(3)],
        },
    }


def run(command: list[str]) -> None:
    print(" ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--define",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="override an OpenSCAD parameter; may be repeated",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="also render files/stand_assembly.png",
    )
    args = parser.parse_args()

    openscad = shutil.which("openscad")
    if not openscad:
        raise SystemExit("OpenSCAD was not found on PATH")

    OUTPUT.mkdir(exist_ok=True)
    common = [item for value in args.define for item in ("-D", value)]
    manifest = []

    for filename, part in PARTS.items():
        destination = OUTPUT / filename
        run([
            openscad,
            "--export-format", "binstl",
            "-o", str(destination),
            "-D", f'part="{part}"',
            "-D", "show_object_envelope=false",
            *common,
            str(SOURCE),
        ])
        manifest.append(validate(destination))

    if args.preview:
        run([
            openscad,
            "-o", str(OUTPUT / "stand_assembly.png"),
            "--imgsize", "1400,1000",
            "--autocenter",
            "--viewall",
            "-D", 'part="assembly"',
            *common,
            str(SOURCE),
        ])

    (OUTPUT / "manifest.json").write_text(
        json.dumps({"source": SOURCE.name, "models": manifest}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(f"Built and validated {len(manifest)} STL files in {OUTPUT}")


if __name__ == "__main__":
    main()
