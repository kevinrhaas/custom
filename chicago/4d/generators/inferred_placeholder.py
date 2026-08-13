#!/usr/bin/env python3
"""Build honest, pure-Python placeholder GLBs for all inferred anonymous infill.

These are review massings, not substitutes for the repository's Blender archetype
bakes.  The glTF asset declares ``asset.extras.placeholder = true`` so the loader and
provenance card flag that fact from the file itself.  Geometry is still generated
entirely from the committed structure record and follows the normal axis/origin,
identity and ``_CONFIDENCE`` contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRUCTURES = ROOT / "data" / "structures"
MASTER = ROOT / "assets" / "gltf"
WEB = ROOT / "assets" / "web"
MANIFEST = ROOT / "assets" / "manifest.json"
PREFIX = "recon_1835_"

WALL_COLOURS = {
    "fresh_timber": "#C3A478", "weathered_timber": "#817D72",
    "whitewash": "#D8D1BC", "ochre": "#A98B52",
    "red_oxide": "#7A4437", "mixed_patch": "#BFAE8E",
}
ROOF_COLOURS = {"fresh": "#5E4938", "darkened": "#4B4037",
                "patched": "#3C3732", "weathered": "#6C6258"}


def load(path: Path):
    return json.loads(path.read_text())


def hex_rgba(value: str) -> list[float]:
    value = value.lstrip("#")
    return [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [1.0]


def normal(a, b, c):
    ux, uy, uz = (b[i] - a[i] for i in range(3))
    vx, vy, vz = (c[i] - a[i] for i in range(3))
    x, y, z = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    length = math.sqrt(x*x + y*y + z*z) or 1.0
    return (x/length, y/length, z/length)


def tri(group: list, a, b, c):
    n = normal(a, b, c)
    group.extend((tuple(a) + n + (1.0,), tuple(b) + n + (1.0,), tuple(c) + n + (1.0,)))


def quad(group: list, a, b, c, d):
    tri(group, a, b, c)
    tri(group, a, c, d)


def box(group: list, x0, x1, y0, y1, z0, z1):
    p = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    for face in ((0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)):
        quad(group, *(p[i] for i in face))


def record_geometry(record: dict) -> tuple[dict[str, list], list[dict]]:
    phase = record["phases"][0]
    poly = phase["footprint"]["polygon"]
    w = max(p[0] for p in poly) - min(p[0] for p in poly)
    d = max(p[1] for p in poly) - min(p[1] for p in poly)
    form = {k: v["value"] for k, v in phase["form"].items()}
    stories = float(form.get("stories", 1))
    wall_h = float(form.get("wall_height_m", 2.6))
    roof_type = form.get("roof_type", "gable")
    pitch = math.radians(float(form.get("roof_pitch_deg", 34)))
    meta = record["reconstruction"]
    groups = {"wall": [], "roof": [], "opening": [], "chimney": []}

    box(groups["wall"], 0, w, 0, wall_h, -d, 0)
    if roof_type == "shed":
        rise = min(wall_h * .72, math.tan(pitch) * d)
        quad(groups["roof"], (-.12,wall_h, .12), (w+.12,wall_h,.12),
             (w+.12,wall_h+rise,-d-.12), (-.12,wall_h+rise,-d-.12))
    else:
        rise = min(wall_h * .85, math.tan(pitch) * d / 2)
        ridge = wall_h + rise
        quad(groups["roof"], (-.14,wall_h,.12), (w+.14,wall_h,.12),
             (w+.14,ridge,-d/2), (-.14,ridge,-d/2))
        quad(groups["roof"], (-.14,ridge,-d/2), (w+.14,ridge,-d/2),
             (w+.14,wall_h,-d-.12), (-.14,wall_h,-d-.12))
        tri(groups["wall"], (0,wall_h,0), (0,ridge,-d/2), (0,wall_h,-d))
        tri(groups["wall"], (w,wall_h,-d), (w,ridge,-d/2), (w,wall_h,0))

    # One readable front door and restrained dark openings. This is intentionally
    # type-level massing; the popup says no opening belongs to an observed elevation.
    door_w = min(1.25, max(.68, w * .18))
    door_h = min(2.25, wall_h * .78)
    dx = w * .5 - door_w * .5
    quad(groups["opening"], (dx,.04,-d-.018), (dx+door_w,.04,-d-.018),
         (dx+door_w,door_h,-d-.018), (dx,door_h,-d-.018))
    bays = max(1, min(5, int(form.get("bays", form.get("shopfront_bays", round(w / 2.2))))))
    for level in range(max(1, int(stories))):
        sill = .78 + level * 2.42
        if sill + 1.0 > wall_h - .16:
            continue
        for i in range(bays):
            cx = (i + .5) * w / bays
            if level == 0 and abs(cx - w*.5) < door_w:
                continue
            ww = min(.74, w / (bays * 2.1))
            quad(groups["opening"], (cx-ww/2,sill,-d-.021), (cx+ww/2,sill,-d-.021),
                 (cx+ww/2,sill+1.0,-d-.021), (cx-ww/2,sill+1.0,-d-.021))

    chimneys = int(form.get("chimneys", 0))
    if chimneys:
        top = wall_h + (math.tan(pitch) * d / 2 if roof_type == "gable" else .8) + .65
        for i in range(chimneys):
            cx = w * (.35 if i == 0 else .68)
            box(groups["chimney"], cx-.18, cx+.18, wall_h+.35, top, -d*.56, -d*.45)

    materials = [
        {"name": f"placeholder_wall_{meta['finish_key']}", "pbrMetallicRoughness": {"baseColorFactor": hex_rgba(WALL_COLOURS[meta["finish_key"]]), "metallicFactor": 0, "roughnessFactor": .86}, "doubleSided": True},
        {"name": f"placeholder_roof_{meta['roof_condition']}", "pbrMetallicRoughness": {"baseColorFactor": hex_rgba(ROOF_COLOURS[meta["roof_condition"]]), "metallicFactor": 0, "roughnessFactor": .9}, "doubleSided": True},
        {"name": "placeholder_opening_dark", "pbrMetallicRoughness": {"baseColorFactor": hex_rgba("#2D3D33"), "metallicFactor": 0, "roughnessFactor": .7}, "doubleSided": True},
        {"name": "placeholder_chimney_brick", "pbrMetallicRoughness": {"baseColorFactor": hex_rgba("#89503F"), "metallicFactor": 0, "roughnessFactor": .88}, "doubleSided": True},
    ]
    return groups, materials


def glb_for(record: dict) -> bytes:
    groups, materials = record_geometry(record)
    blob = bytearray()
    views, accessors, primitives = [], [], []
    material_index = {name: i for i, name in enumerate(("wall", "roof", "opening", "chimney"))}

    def add_accessor(values: list[float], kind: str, count: int, mins=None, maxs=None):
        offset = len(blob)
        blob.extend(struct.pack(f"<{len(values)}f", *values))
        view = len(views)
        views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(values)*4})
        acc = {"bufferView": view, "componentType": 5126, "count": count, "type": kind}
        if mins is not None: acc["min"] = mins
        if maxs is not None: acc["max"] = maxs
        accessors.append(acc)
        return len(accessors)-1

    for name, verts in groups.items():
        if not verts:
            continue
        positions = [c for v in verts for c in v[:3]]
        normals = [c for v in verts for c in v[3:6]]
        conf = [v[6] for v in verts]
        xs, ys, zs = positions[0::3], positions[1::3], positions[2::3]
        p = add_accessor(positions, "VEC3", len(verts), [min(xs),min(ys),min(zs)], [max(xs),max(ys),max(zs)])
        n = add_accessor(normals, "VEC3", len(verts))
        c = add_accessor(conf, "SCALAR", len(verts), [1.0], [1.0])
        primitives.append({"attributes": {"POSITION": p, "NORMAL": n, "_CONFIDENCE": c},
                           "material": material_index[name], "mode": 4})

    sid, phase = record["id"], record["phases"][0]["id"]
    doc = {
        "asset": {"version": "2.0", "generator": "inferred_placeholder.py",
                  "extras": {"placeholder": True, "generated_from": f"data/structures/{sid}.json",
                             "reason": "Review massing pending canonical archetype bake"}},
        "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"name": f"{sid}__{phase}", "mesh": 0,
                   "extras": {"structure_id": sid, "phase_id": phase, "scene_ids": ["1835"]}}],
        "meshes": [{"name": f"{sid}__{phase}", "primitives": primitives}],
        "materials": materials, "buffers": [{"byteLength": len(blob)}],
        "bufferViews": views, "accessors": accessors,
    }
    js = json.dumps(doc, separators=(",", ":"), ensure_ascii=False).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    blob += b"\0" * ((4 - len(blob) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(blob)
    return (struct.pack("<III", 0x46546C67, 2, total)
            + struct.pack("<II", len(js), 0x4E4F534A) + js
            + struct.pack("<II", len(blob), 0x004E4942) + blob)


def expected() -> tuple[dict[str, bytes], dict[str, dict]]:
    files, entries = {}, {}
    for path in sorted(STRUCTURES.glob(f"{PREFIX}*.json")):
        record = load(path)
        phase = record["phases"][0]["id"]
        name = f"{record['id']}__{phase}.glb"
        data = glb_for(record)
        files[name] = data
        entries[name] = {
            "archetype": record["archetype"], "bytes": len(data),
            "generator": "generators/inferred_placeholder.py",
            "inputs_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "kind": "placeholder", "phase_id": phase, "placeholder": True,
            "source_record": f"data/structures/{path.name}",
        }
    return files, entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    files, entries = expected()
    manifest = load(MANIFEST)
    drift = []
    for name, data in files.items():
        for folder in (MASTER, WEB):
            path = folder / name
            if args.check:
                if not path.exists() or path.read_bytes() != data:
                    drift.append(f"{path.relative_to(ROOT)} is missing or stale")
            else:
                path.write_bytes(data)
        if args.check:
            if manifest["assets"].get(name) != entries[name]:
                drift.append(f"assets/manifest.json entry for {name} is missing or stale")
        else:
            manifest["assets"][name] = entries[name]
    if not args.check:
        MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    if drift:
        print("RECOMMENDED PLACEHOLDER DRIFT")
        for item in drift:
            print(f"  - {item}")
        return 1
    print(f"{'verified' if args.check else 'built'} {len(files)} flagged placeholder GLBs in master and web trees")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
