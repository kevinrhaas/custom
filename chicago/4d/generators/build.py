"""Generate meshes from data/. Run inside Blender:

    blender -b -noaudio --factory-startup --python generators/build.py -- [args]

    --all           build every structure phase resolvable for the scene
    --only <id>     build one structure id
    --scene <id>    scene to resolve phases against (default 1835)
    --no-bake       skip UV + AO baking (fast iteration)
    --out <dir>     output directory (default assets/gltf)

Refuses to run while data/datum.json is unverified — fixing the origin after
geometry exists means regenerating everything, so the build makes that impossible
rather than merely discouraged.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generators"))

import bpy  # noqa: E402

from common.mesh import reset_scene  # noqa: E402
from archetypes import frame_tavern  # noqa: E402
from archetypes.frame_tavern_params import from_phase as frame_tavern_params  # noqa: E402

ARCHETYPES = {
    "frame_tavern": (frame_tavern_params, frame_tavern.build),
}


def argv_after_ddash() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def load(p: Path):
    return json.loads(p.read_text())


def resolve_phase(structure: dict, target: dt.date):
    """The scene rule, identical to tools/validate.py: exactly one phase must
    cover the date, or the structure is not in the scene."""
    hits = []
    for ph in structure.get("phases", []):
        r = ph.get("documented_range", {})
        try:
            frm = dt.date.fromisoformat(r["from"])
            to = dt.date.fromisoformat(r["to"])
        except (KeyError, ValueError):
            continue
        if frm <= target <= to:
            hits.append(ph)
    if len(hits) > 1:
        raise SystemExit(f"{structure['id']}: {len(hits)} phases cover {target}; exactly one must")
    return hits[0] if hits else None


def inputs_hash(structure: dict, phase: dict, archetype: str) -> str:
    """Hash of everything that determines this mesh: the resolved phase, the
    archetype modules, and the pinned Blender. assets/manifest.json stores it so
    check.sh can tell a stale committed GLB from a fresh one — determinism is
    defined on inputs, because Cycles AO is not bit-reproducible across hardware."""
    h = hashlib.sha256()
    h.update(json.dumps({"id": structure["id"], "phase": phase}, sort_keys=True).encode())
    for f in sorted((ROOT / "generators").rglob("*.py")):
        h.update(f.read_bytes())
    h.update((ROOT / "generators" / "blender.pin").read_bytes())
    return h.hexdigest()


def bake_ao(ob, size: int = 512, samples: int = 48) -> None:
    """Smart-UV unwrap and bake ambient occlusion to an image texture.

    AO is the largest visible quality gain available on plain frame buildings and
    it is the reason this pipeline uses Blender at all.
    """
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")

    img = bpy.data.images.new(f"{ob.name}_ao", size, size)
    for mat in ob.data.materials:
        nt = mat.node_tree
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        nt.nodes.active = tex

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.render.bake.use_selected_to_active = False
    sc.render.bake.margin = 4
    bpy.ops.object.bake(type="AO")


def export_glb(ob, structure_id: str, phase_id: str, out: Path) -> Path:
    ob["structure_id"] = structure_id
    ob["phase_id"] = phase_id
    ob.name = f"{structure_id}__{phase_id}"
    ob.data.name = ob.name

    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.export_scene.gltf(
        filepath=str(out),
        export_format="GLB",
        use_selection=True,
        export_yup=True,
        export_apply=True,
        export_attributes=True,      # carries _CONFIDENCE — see docs/GLB-CONTRACT.md
        export_extras=True,          # carries structure_id / phase_id into node.extras
        export_cameras=False,
        export_lights=False,
    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--scene", default="1835")
    ap.add_argument("--no-bake", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "assets" / "gltf"))
    args = ap.parse_args(argv_after_ddash())

    datum = load(ROOT / "data" / "datum.json")
    if not datum.get("verified"):
        print("REFUSING TO BUILD: data/datum.json is not verified.\n"
              "Fixing the origin after geometry exists means regenerating everything.\n"
              "See docs/EPOCHS.md and docs/RESEARCH/datum_derivation.md.")
        return 2

    scene = load(ROOT / "data" / "scenes" / f"{args.scene}.json")
    target = dt.date.fromisoformat(scene["target_date"])
    outdir = Path(args.out)

    manifest_path = ROOT / "assets" / "manifest.json"
    manifest = load(manifest_path) if manifest_path.exists() else {}
    manifest.setdefault("assets", {})
    manifest["blender"] = bpy.app.version_string.split()[0]

    built = 0
    for path in sorted((ROOT / "data" / "structures").glob("*.json")):
        st = load(path)
        if args.only and st["id"] != args.only:
            continue
        phase = resolve_phase(st, target)
        if phase is None:
            print(f"skip {st['id']}: no phase covers {target}")
            continue
        arch = st["archetype"]
        if arch not in ARCHETYPES:
            print(f"skip {st['id']}: archetype '{arch}' has no generator yet")
            continue

        to_params, build_fn = ARCHETYPES[arch]
        params = to_params(phase)
        name = f"{st['id']}__{phase['id']}"

        reset_scene()
        ob = build_fn(params, name)
        if not args.no_bake:
            bake_ao(ob)
        out = export_glb(ob, st["id"], phase["id"], outdir / f"{name}.glb")

        manifest["assets"][out.name] = {
            "kind": "generated",
            "structure_id": st["id"],
            "phase_id": phase["id"],
            "archetype": arch,
            "inputs_sha256": inputs_hash(st, phase, arch),
            "bytes": out.stat().st_size,
            "baked_ao": not args.no_bake,
        }
        tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
        print(f"built {out.name}  {out.stat().st_size:,} bytes  ~{tris} tris")
        built += 1

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"\n{built} asset(s) built; manifest updated")
    return 0 if built else 1


if __name__ == "__main__":
    sys.exit(main())
