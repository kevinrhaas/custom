from __future__ import annotations

import argparse
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import trimesh

CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
PROD_NS = "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"
NS = {"m": CORE_NS, "p": PROD_NS}

VERTEX_RE = re.compile(
    rb'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/>'
)
TRIANGLE_RE = re.compile(
    rb'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"[^/]*/>'
)


def parse_transform(transform: str) -> np.ndarray:
    v = [float(x) for x in transform.split()]
    return np.array([
        [v[0], v[1], v[2], v[9]],
        [v[3], v[4], v[5], v[10]],
        [v[6], v[7], v[8], v[11]],
        [0, 0, 0, 1],
    ], dtype=float)


def smoothstep(t: np.ndarray) -> np.ndarray:
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def world_verts(local: np.ndarray, M: np.ndarray) -> np.ndarray:
    hom = np.c_[local, np.ones(len(local))]
    return (M @ hom.T).T[:, :3]


def parse_verts_from_xml(raw: bytes) -> np.ndarray:
    matches = VERTEX_RE.findall(raw)
    return np.array([[float(x), float(y), float(z)] for x, y, z in matches], dtype=float)


def parse_triangles_from_xml(raw: bytes) -> np.ndarray:
    matches = TRIANGLE_RE.findall(raw)
    return np.array([[int(a), int(b), int(c)] for a, b, c in matches], dtype=np.int64)


def replace_verts_in_xml(raw: bytes, new_verts: np.ndarray) -> bytes:
    idx = [0]

    def _sub(m: re.Match) -> bytes:
        i = idx[0]
        idx[0] += 1
        x, y, z = new_verts[i]
        return f'<vertex x="{x}" y="{y}" z="{z}"/>'.encode()

    result = VERTEX_RE.sub(_sub, raw)
    if idx[0] != len(new_verts):
        raise ValueError(f"Vertex count mismatch: expected {len(new_verts)}, replaced {idx[0]}")
    return result


def taper_shell(
    world: np.ndarray,
    target_radius: float,
    taper_height: float,
    lip: float,
    flat_top_height: float,
) -> np.ndarray:
    out = world.copy()
    z_max = out[:, 2].max()
    start_z = z_max - taper_height
    flat_start_z = z_max - max(flat_top_height, 0.0)
    effective_target = target_radius + lip

    radii = np.hypot(out[:, 0], out[:, 1])

    # Force a clean annular land at the top by snapping near-rim points
    # in the flat-top band to the exact target radius.
    snap_mask = (out[:, 2] >= flat_start_z) & (radii >= (effective_target - 0.5))
    if np.any(snap_mask):
        snap_r = radii[snap_mask]
        snap_scale = effective_target / np.maximum(snap_r, 1e-9)
        out[snap_mask, 0] *= snap_scale
        out[snap_mask, 1] *= snap_scale
        radii = np.hypot(out[:, 0], out[:, 1])

    movable = (out[:, 2] > start_z) & (radii > effective_target)
    if not np.any(movable):
        return out

    cur = radii[movable]
    z_movable = out[movable, 2]
    transition_height = max(taper_height - max(flat_top_height, 0.0), 1e-6)
    blend = smoothstep((z_movable - start_z) / transition_height)
    new_r = effective_target + (cur - effective_target) * (1.0 - blend)
    in_flat_top = z_movable >= flat_start_z
    new_r[in_flat_top] = effective_target
    scale = new_r / cur
    out[movable, 0] *= scale
    out[movable, 1] *= scale
    return out


def find_component_transform(top_xml: bytes, obj_id: int) -> np.ndarray:
    top = ET.fromstring(top_xml)
    for c in top.findall(".//m:component", NS):
        if int(c.attrib["objectid"]) == obj_id:
            return parse_transform(c.attrib["transform"])
    raise ValueError(f"No component for object id {obj_id}")


def extract_object_xml(raw: bytes, obj_id: int) -> tuple[int, int]:
    pattern = re.compile(
        rb'(<object\s[^>]*id="' + str(obj_id).encode() + rb'".*?</object>)',
        re.DOTALL,
    )
    m = pattern.search(raw)
    if not m:
        raise ValueError(f"Object id={obj_id} not found in XML")
    return m.start(), m.end()


def generate_3mf(
    input_path: Path,
    output_path: Path,
    taper_height: float,
    lip: float,
    flat_top_height: float,
) -> np.ndarray:
    with zipfile.ZipFile(input_path) as zf:
        top_raw = zf.read("3D/3dmodel.model")
        obj_raw = zf.read("3D/Objects/TissueShell_3.model")

        pos_M = find_component_transform(top_raw, 1)
        neg_M = find_component_transform(top_raw, 2)
        pos_inv = np.linalg.inv(pos_M)

        # Isolate object id=1 block to only replace its vertices
        start1, end1 = extract_object_xml(obj_raw, 1)
        obj1_block = obj_raw[start1:end1]
        start2, end2 = extract_object_xml(obj_raw, 2)
        obj2_block = obj_raw[start2:end2]

        pos_local = parse_verts_from_xml(obj1_block)
        neg_local = parse_verts_from_xml(obj2_block)
        neg_world = world_verts(neg_local, neg_M)
        cavity_r = np.hypot(neg_world[:, 0], neg_world[:, 1]).max()

        pos_world = world_verts(pos_local, pos_M)
        tapered_world = taper_shell(pos_world, cavity_r, taper_height, lip, flat_top_height)
        tapered_local = world_verts(tapered_world, pos_inv)

        new_obj1_block = replace_verts_in_xml(obj1_block, tapered_local)
        new_obj_raw = obj_raw[:start1] + new_obj1_block + obj_raw[end1:]

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, "w") as out_zip:
            for info in zf.infolist():
                data = zf.read(info.filename)
                if info.filename == "3D/Objects/TissueShell_3.model":
                    data = new_obj_raw
                out_zip.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)

    radii_before = np.hypot(pos_world[:, 0], pos_world[:, 1])
    radii_after = np.hypot(tapered_world[:, 0], tapered_world[:, 1])
    top_mask = pos_world[:, 2] >= pos_world[:, 2].max() - 0.05
    print(f"wrote {output_path}")
    print(f"  taper: {taper_height} mm, lip: {lip} mm, flat top: {flat_top_height} mm")
    print(f"  cavity radius: {cavity_r:.2f} mm")
    print(f"  top radius before: {radii_before[top_mask].max():.2f} → after: {radii_after[top_mask].max():.2f} mm")

    return tapered_world


def generate_stl(
    input_path: Path,
    output_path: Path,
    taper_height: float,
    lip: float,
    flat_top_height: float,
) -> None:
    with zipfile.ZipFile(input_path) as zf:
        top_raw = zf.read("3D/3dmodel.model")
        obj_raw = zf.read("3D/Objects/TissueShell_3.model")

        pos_M = find_component_transform(top_raw, 1)
        neg_M = find_component_transform(top_raw, 2)

        start1, end1 = extract_object_xml(obj_raw, 1)
        obj1_block = obj_raw[start1:end1]
        start2, end2 = extract_object_xml(obj_raw, 2)
        obj2_block = obj_raw[start2:end2]

        pos_local = parse_verts_from_xml(obj1_block)
        pos_faces = parse_triangles_from_xml(obj1_block)
        neg_local = parse_verts_from_xml(obj2_block)
        neg_faces = parse_triangles_from_xml(obj2_block)

        neg_world = world_verts(neg_local, neg_M)
        cavity_r = np.hypot(neg_world[:, 0], neg_world[:, 1]).max()

        pos_world = world_verts(pos_local, pos_M)
        tapered_world = taper_shell(pos_world, cavity_r, taper_height, lip, flat_top_height)

        # Also apply the build-item transform (z offset of 89.5)
        top = ET.fromstring(top_raw)
        item = top.find(".//m:item", NS)
        if item is not None and "transform" in item.attrib:
            build_M = parse_transform(item.attrib["transform"])
        else:
            build_M = np.eye(4)

        pos_final = world_verts(tapered_world, build_M)
        neg_final = world_verts(neg_world, build_M)

        pos_mesh = trimesh.Trimesh(vertices=pos_final, faces=pos_faces, process=False)
        neg_mesh = trimesh.Trimesh(vertices=neg_final, faces=neg_faces, process=False)

        try:
            result = trimesh.boolean.difference([pos_mesh, neg_mesh], engine="manifold")
        except Exception:
            print("  boolean difference failed, exporting shell without cavity subtraction")
            result = pos_mesh

        result.export(str(output_path))
        print(f"wrote {output_path}  ({len(result.vertices)} verts, {len(result.faces)} faces)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a tapered TissueShell.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, help="Base output name (without extension)")
    parser.add_argument("--taper-height", type=float, default=10.0)
    parser.add_argument("--lip", type=float, default=1.0, help="Wall thickness to keep at top rim (mm)")
    parser.add_argument(
        "--flat-top-height",
        type=float,
        default=0.6,
        help="Height of constant-width rim at very top to improve top-surface continuity (mm)",
    )
    args = parser.parse_args()

    stem = args.output
    threemf_path = stem.with_suffix(".3mf")
    stl_path = stem.with_suffix(".stl")

    generate_3mf(args.input, threemf_path, args.taper_height, args.lip, args.flat_top_height)
    generate_stl(args.input, stl_path, args.taper_height, args.lip, args.flat_top_height)
    print("\ndone")


if __name__ == "__main__":
    main()