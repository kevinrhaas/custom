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
from archetypes import bridge_timber, frame_tavern, log_dwelling  # noqa: E402
from archetypes.bridge_timber_params import from_phase as bridge_timber_params  # noqa: E402
from archetypes.frame_tavern_params import from_phase as frame_tavern_params  # noqa: E402
from archetypes.log_dwelling_params import from_phase as log_dwelling_params  # noqa: E402

ARCHETYPES = {
    "frame_tavern": (frame_tavern_params, frame_tavern.build),
    "log_dwelling": (log_dwelling_params, log_dwelling.build),
    "bridge_timber": (bridge_timber_params, bridge_timber.build),
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


def unwrap(ob) -> None:
    """Smart-UV unwrap. Always run — textures need UVs even when AO does not."""
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


def bake_ao(ob, size: int = 512, samples: int = 48) -> None:
    """Bake ambient occlusion and wire it in as the glTF occlusion texture.

    OFF BY DEFAULT, and that is a considered choice rather than an oversight.
    AO is the largest visible quality gain available on plain frame buildings,
    which is why this pipeline uses Blender at all — but it only works on
    geometry built for it. These archetypes model clapboard courses, window
    reveals and shutters as thin surfaces sitting a centimetre off the wall, and
    every one of them occludes its neighbours: a measured bake comes out at mean
    0.265 with 69% of texels below half, and the Sauganash renders brown when its
    white paint is DOCUMENTED. Shortening the AO distance to 0.25 m only reaches
    0.38. That is not a tuning problem, it is a geometry problem.

    The fix, when someone picks this up, is a low-poly AO cage — bake the massing
    only, and let the decorative surfaces inherit it — not a stronger denoiser.
    Until then `--ao` exists so the path stays exercised, and the manifest records
    honestly whether any given asset actually carries AO.
    """
    img = bpy.data.images.new(f"{ob.name}_ao", size, size)
    for mat in ob.data.materials:
        nt = mat.node_tree
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.name = "ao_tex"
        nt.nodes.active = tex          # bake target

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.render.bake.use_selected_to_active = False
    sc.render.bake.margin = 4
    bpy.ops.object.bake(type="AO")

    # Wire the baked image in as the glTF OCCLUSION texture. Without this the
    # exporter drops it and the GLB carries no AO at all — the bake silently
    # produces nothing, which is exactly what happened before this was added.
    # The exporter recognises a node group literally named "glTF Material Output"
    # with an "Occlusion" input; that is the only supported path.
    for mat in ob.data.materials:
        nt = mat.node_tree
        tex = next((n for n in nt.nodes if n.name == "ao_tex"), None)
        if tex is None:
            continue
        tex.image.colorspace_settings.name = "Non-Color"
        grp = bpy.data.node_groups.get("glTF Material Output")
        if grp is None:
            grp = bpy.data.node_groups.new("glTF Material Output", "ShaderNodeTree")
            grp.interface.new_socket("Occlusion", in_out="INPUT",
                                     socket_type="NodeSocketFloat")
            grp.nodes.new("NodeGroupInput")
        node = nt.nodes.new("ShaderNodeGroup")
        node.node_tree = grp
        node.name = "glTF Material Output"
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tex.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Red"], node.inputs["Occlusion"])


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
    ap.add_argument("--no-bake", action="store_true",
                    help="skip UV unwrap as well as AO")
    ap.add_argument("--ao", action="store_true",
                    help="bake ambient occlusion. OFF by default: see bake_ao().")
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
            unwrap(ob)
            if args.ao:
                bake_ao(ob)
        out = export_glb(ob, st["id"], phase["id"], outdir / f"{name}.glb")

        manifest["assets"][out.name] = {
            "kind": "generated",
            "structure_id": st["id"],
            "phase_id": phase["id"],
            "archetype": arch,
            "inputs_sha256": inputs_hash(st, phase, arch),
            "bytes": out.stat().st_size,
            "baked_ao": bool(args.ao and not args.no_bake),
        }
        tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
        print(f"built {out.name}  {out.stat().st_size:,} bytes  ~{tris} tris")
        built += 1

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"\n{built} asset(s) built; manifest updated")
    return 0 if built else 1


if __name__ == "__main__":
    sys.exit(main())
