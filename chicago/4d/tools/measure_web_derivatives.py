#!/usr/bin/env python3
"""Does the file the site ships still describe the building the repository baked?

ROADMAP K36(a). The geometry a visitor downloads reaches them along four links:

    data/  ->  assets/gltf/  ->  assets/web/  ->  site/chicago/4d/assets/web/

Link 1 is gated: `validate.py --stale` recomputes every master's input hash, so a
record edited into a different building fails. Link 3 is gated: `check_published.mjs`
asserts every published file is byte-identical to its source. **Link 2 was gated by
nothing at all** — no committed number, no hash, no assertion tied a shipped
derivative to the master it was compressed from — and it is the link with the moving
parts: `tools/bake.sh` runs two `gltf-transform` passes over every master, and its own
comments record what has already gone wrong in there:

  * *"a bug that collapsed every building to a two-metre box shipped past a fully
    green gate — twice"*;
  * `--texture-compress ktx2` *"silently turned every derivative into an uncompressed
    copy of its master, in every environment, since this step was written"*;
  * `optimize` runs mesh simplification by default, which on this dataset is damage
    rather than optimisation, so the bake passes `--simplify false` — a flag, in a
    script, with nothing asserting the outcome.

Every one of those was found by a person reading the script. This reads the bytes.

    tools/measure_web_derivatives.py                 print the census
    tools/measure_web_derivatives.py --gate          exit 1 on a divergence
    tools/measure_web_derivatives.py --self-test     break each assertion, in memory
    tools/measure_web_derivatives.py --write-baseline   bank a repair (deliberate act)

NO BLENDER, NO DECODER, NO NETWORK. Only the glTF JSON chunk is read. Positions in a
shipped derivative are EXT_meshopt_compression payloads this project cannot decode
here — but every claim below is answerable from the JSON alone, because the glTF spec
requires POSITION accessors to carry `min`/`max`, and a quantised file carries its
dequantisation in the node's own TRS. Counting triangles, composing node transforms
and comparing material tables costs about a second for all 334 assets.

## The assertions

1.  **Bijection** (absolute). Every master has a derivative and every derivative has a
    master. A derivative whose master was deleted is a building on the site that the
    dataset no longer describes.

2.  **Triangle count** (absolute). Equal, per asset. This is the assertion behind
    `--simplify false`: the flag says what the bake asks for, this says what arrived.

3.  **Identity** (absolute). Node names, node `extras` — `structure_id`, `phase_id` —
    and mesh names survive. These are the join key the sidecars and the provenance
    card use; a derivative that lost them is anonymous geometry.

4.  **The contract's attributes** (absolute). `docs/GLB-CONTRACT.md` names POSITION,
    NORMAL and `_CONFIDENCE`; whichever the master carries, the shipped file carries.
    `_CONFIDENCE` is how a visitor is told which parts we made up, and it travels in
    the mesh rather than in a sidecar. TEXCOORD_0 is deliberately NOT in this list:
    the master's UVs are unused on an untextured asset and `optimize`'s prune pass is
    right to drop them. That is reported, not gated.

5.  **The building is where it was** (absolute). The world-space bounding box of the
    two files must agree to within FOUR RUNGS of the asset's own widest extent, where
    a rung is `extent / 65535` — the 16-bit lattice a normalised SHORT position is
    stored on, whatever bit depth the bake asked the quantiser for. The bound is a
    lattice, not a millimetre count, because the assets differ in size by three orders
    of magnitude: measured 2026-08-16, the worst was 2.63 rungs (0.107 mm on a 2.7 m
    shed) and the terrain's 82.8 mm is 1.08 rungs of its own 5,020 m box — the same
    quantity R-W6 committed as a 76.6 mm lattice. A building collapsed to a two-metre
    box is thousands of rungs, not four.

6.  **Material identity** (RATCHET, `tools/web_derivative_baseline.json`). The shipped
    file should resolve to the same material NAMES and base COLOURS as its master and
    should gain no texture the master does not have. **38 of 334 assets fail this
    today** and they are in the baseline: `optimize`'s palette pass folds their five or
    six named materials — `log`, `chinking`, `board`, `roof`, … — into a single
    `PaletteMaterial001` carrying two generated PNGs. It is a ratchet rather than an
    absolute for the reason K25's is: the repair is K36(b), it regenerates 334 binary
    files, and a permanently red dev gate would block every unrelated parcel behind it.
    A new offender fails. A repaired one fails too, and says to bank it.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTERS = ROOT / "assets" / "gltf"
SHIPPED = ROOT / "assets" / "web"
BASELINE = ROOT / "tools" / "web_derivative_baseline.json"

# A normalised position component is stored in a SHORT and dequantised by the node's
# own scale, so the finest step any shipped vertex can land on is the asset's widest
# extent over 65535 — regardless of the bit depth the bake asked for, which only makes
# the step coarser. Four of them is the bound; see the module docstring.
RUNGS = 65535
RUNG_TOLERANCE = 4.0

# Attributes docs/GLB-CONTRACT.md names. TEXCOORD_0 is not one of them.
CONTRACT_ATTRIBUTES = ("POSITION", "NORMAL", "_CONFIDENCE")

# glTF component types that carry a normalised integer, and their divisor.
NORMALISED = {5120: 127.0, 5121: 255.0, 5122: 32767.0, 5123: 65535.0}


# ---------------------------------------------------------------- reading the file

def glb_json(path: Path) -> dict:
    """The JSON chunk of a .glb. Never touches the binary chunk."""
    raw = path.read_bytes()
    if raw[:4] != b"glTF":
        raise ValueError(f"{path} is not a binary glTF")
    length, kind = struct.unpack_from("<I4s", raw, 12)
    if kind != b"JSON":
        raise ValueError(f"{path}: first chunk is {kind!r}, not JSON")
    return json.loads(raw[20:20 + length])


def node_matrix(node: dict) -> list[list[float]]:
    """The node's local transform as a 3x4 row-major matrix."""
    if "matrix" in node:
        m = node["matrix"]  # column-major, per the spec
        return [[m[0], m[4], m[8], m[12]],
                [m[1], m[5], m[9], m[13]],
                [m[2], m[6], m[10], m[14]]]
    tx, ty, tz = node.get("translation", [0.0, 0.0, 0.0])
    x, y, z, w = node.get("rotation", [0.0, 0.0, 0.0, 1.0])
    sx, sy, sz = node.get("scale", [1.0, 1.0, 1.0])
    rot = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
           [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
           [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    scale = (sx, sy, sz)
    trans = (tx, ty, tz)
    return [[rot[i][0] * scale[0], rot[i][1] * scale[1], rot[i][2] * scale[2], trans[i]]
            for i in range(3)]


def compose(parent, child):
    if parent is None:
        return child
    out = []
    for i in range(3):
        row = [sum(parent[i][k] * child[k][j] for k in range(3)) for j in range(3)]
        row.append(sum(parent[i][k] * child[k][3] for k in range(3)) + parent[i][3])
        out.append(row)
    return out


def transform(matrix, point):
    return [sum(matrix[i][k] * point[k] for k in range(3)) + matrix[i][3] for i in range(3)]


def world_bbox(doc: dict):
    """The scene's world-space bounding box, from accessor min/max alone.

    Dequantisation is the node's business in a meshopt file — the accessor holds
    normalised integers and the node holds the scale that puts them back in metres —
    so composing the hierarchy is what makes the two trees comparable at all.
    """
    lo = [math.inf] * 3
    hi = [-math.inf] * 3
    nodes = doc.get("nodes", [])
    meshes = doc.get("meshes", [])
    accessors = doc.get("accessors", [])

    def walk(index: int, parent):
        node = nodes[index]
        matrix = compose(parent, node_matrix(node))
        if "mesh" in node:
            for prim in meshes[node["mesh"]].get("primitives", []):
                pos = prim.get("attributes", {}).get("POSITION")
                if pos is None:
                    continue
                acc = accessors[pos]
                if "min" not in acc or "max" not in acc:
                    continue
                divisor = NORMALISED[acc["componentType"]] if acc.get("normalized") else 1.0
                lows = [v / divisor for v in acc["min"]]
                highs = [v / divisor for v in acc["max"]]
                for cx in (lows[0], highs[0]):
                    for cy in (lows[1], highs[1]):
                        for cz in (lows[2], highs[2]):
                            p = transform(matrix, [cx, cy, cz])
                            for k in range(3):
                                lo[k] = min(lo[k], p[k])
                                hi[k] = max(hi[k], p[k])
        for child in node.get("children", []):
            walk(child, matrix)

    scenes = doc.get("scenes", [])
    roots = scenes[doc.get("scene", 0)].get("nodes", []) if scenes else range(len(nodes))
    for root in roots:
        walk(root, None)
    if lo[0] is math.inf:
        return None, None
    return lo, hi


def triangles(doc: dict) -> int:
    total = 0
    accessors = doc.get("accessors", [])
    for mesh in doc.get("meshes", []):
        for prim in mesh.get("primitives", []):
            if prim.get("mode", 4) != 4:
                continue
            if "indices" in prim:
                total += accessors[prim["indices"]]["count"] // 3
            else:
                total += accessors[prim["attributes"]["POSITION"]]["count"] // 3
    return total


def identity(doc: dict) -> dict:
    return {
        "nodes": [n.get("name") for n in doc.get("nodes", [])],
        "extras": [n.get("extras") for n in doc.get("nodes", [])],
        "meshes": [m.get("name") for m in doc.get("meshes", [])],
    }


def attributes(doc: dict) -> set:
    return {key
            for mesh in doc.get("meshes", [])
            for prim in mesh.get("primitives", [])
            for key in prim.get("attributes", {})}


def materials(doc: dict) -> dict:
    names, colours = set(), set()
    for mat in doc.get("materials", []):
        if mat.get("name"):
            names.add(mat["name"])
        factor = mat.get("pbrMetallicRoughness", {}).get("baseColorFactor")
        if factor:
            colours.add(tuple(round(c, 6) for c in factor))
    return {"names": names, "colours": colours, "textures": len(doc.get("textures", []))}


# ---------------------------------------------------------------- the measurement

def measure() -> dict:
    master_files = {p.name: p for p in sorted(MASTERS.glob("*.glb"))}
    shipped_files = {p.name: p for p in sorted(SHIPPED.glob("*.glb"))}

    rows = []
    for name in sorted(set(master_files) & set(shipped_files)):
        a = glb_json(master_files[name])
        b = glb_json(shipped_files[name])
        alo, ahi = world_bbox(a)
        blo, bhi = world_bbox(b)
        if alo is None or blo is None:
            drift, extent = None, 0.0
        else:
            drift = max(max(abs(alo[i] - blo[i]), abs(ahi[i] - bhi[i])) for i in range(3))
            extent = max(ahi[i] - alo[i] for i in range(3))
        ma, mb = materials(a), materials(b)
        master_bytes = master_files[name].stat().st_size
        shipped_bytes = shipped_files[name].stat().st_size
        rows.append({
            "name": name,
            "triangles": (triangles(a), triangles(b)),
            "identity_master": identity(a),
            "identity_shipped": identity(b),
            "attributes_lost": sorted(attributes(a) - attributes(b)),
            "attributes_gained": sorted(attributes(b) - attributes(a)),
            "bbox_drift_m": drift,
            "extent_m": extent,
            "rungs": (drift / extent * RUNGS) if (drift is not None and extent) else 0.0,
            "names_lost": sorted(ma["names"] - mb["names"]),
            "colours_lost": len(ma["colours"] - mb["colours"]),
            "master_materials": len(a.get("materials", [])),
            "shipped_materials": len(b.get("materials", [])),
            "textures_master": ma["textures"],
            "textures_shipped": mb["textures"],
            "bytes": (master_bytes, shipped_bytes),
            "uncompressed_copy": master_files[name].read_bytes()
                                 == shipped_files[name].read_bytes(),
        })
    return {
        "rows": rows,
        "master_only": sorted(set(master_files) - set(shipped_files)),
        "shipped_only": sorted(set(shipped_files) - set(master_files)),
    }


def material_fault(row: dict) -> dict | None:
    """The shipped file's material table does not resolve to the master's."""
    if not row["names_lost"] and not row["colours_lost"] \
            and row["textures_shipped"] <= row["textures_master"]:
        return None
    return {
        "master_materials": row["master_materials"],
        "shipped_materials": row["shipped_materials"],
        "names_lost": row["names_lost"],
        "colours_lost": row["colours_lost"],
        "textures_gained": row["textures_shipped"] - row["textures_master"],
    }


# ---------------------------------------------------------------- the assertions

def assertions(result: dict, baseline: dict) -> list[str]:
    problems = []
    for name in result["master_only"]:
        problems.append(f"assets/gltf/{name} has no derivative in assets/web — the site "
                        f"cannot ship a building the bake did not compress")
    for name in result["shipped_only"]:
        problems.append(f"assets/web/{name} has no master in assets/gltf — the site ships "
                        f"geometry the dataset no longer describes")

    banked = baseline.get("material_identity", {})
    seen = set()
    for row in result["rows"]:
        name = row["name"]
        ta, tb = row["triangles"]
        if ta != tb:
            problems.append(f"{name}: the master has {ta} triangles and the shipped file has "
                            f"{tb} — the publish path changed the geometry, which "
                            f"tools/bake.sh's --simplify false says it must not")
        if row["identity_master"] != row["identity_shipped"]:
            problems.append(f"{name}: node names, node extras or mesh names differ between the "
                            f"master and the shipped file — the sidecars and the provenance "
                            f"card join on those")
        lost = [a for a in row["attributes_lost"] if a in CONTRACT_ATTRIBUTES]
        if lost:
            problems.append(f"{name}: the shipped file lost {', '.join(lost)}, which "
                            f"docs/GLB-CONTRACT.md names")
        if row["rungs"] > RUNG_TOLERANCE:
            problems.append(f"{name}: the shipped bounding box is {row['bbox_drift_m'] * 1000:.1f} "
                            f"mm from the master's, {row['rungs']:.2f} rungs of its own "
                            f"{row['extent_m']:.1f} m extent against a bound of "
                            f"{RUNG_TOLERANCE:.0f} — this is not quantisation")

        fault = material_fault(row)
        if fault:
            seen.add(name)
            was = banked.get(name)
            if was is None:
                problems.append(f"{name}: the shipped file's materials do not resolve to the "
                                f"master's — {fault['master_materials']} material(s) became "
                                f"{fault['shipped_materials']}, "
                                f"{len(fault['names_lost'])} name(s) and "
                                f"{fault['colours_lost']} colour(s) lost, "
                                f"{fault['textures_gained']} texture(s) gained. K36(b) owns "
                                f"the repair; this is a new one")
            elif (len(fault["names_lost"]) > len(was.get("names_lost", []))
                    or fault["colours_lost"] > was.get("colours_lost", 0)
                    or fault["textures_gained"] > was.get("textures_gained", 0)):
                problems.append(f"{name}: the material fault GREW — "
                                f"{len(fault['names_lost'])} name(s) lost against "
                                f"{len(was.get('names_lost', []))} banked. The ratchet is not "
                                f"an allowance")
    for name in sorted(set(banked) - seen):
        problems.append(f"{name}: banked in {BASELINE.name} as losing its material identity on "
                        f"the way to the site, and it no longer does. That is the repair — "
                        f"re-run tools/measure_web_derivatives.py --write-baseline in the "
                        f"commit that made it")
    return problems


# ---------------------------------------------------------------- output

def print_census(result: dict) -> None:
    rows = result["rows"]
    copies = [r for r in rows if r["uncompressed_copy"]]
    compressed = [r for r in rows if not r["uncompressed_copy"]]
    master_bytes = sum(r["bytes"][0] for r in rows)
    shipped_bytes = sum(r["bytes"][1] for r in rows)

    print(f"{len(rows)} master/derivative pair(s); "
          f"{len(result['master_only'])} master(s) with no derivative, "
          f"{len(result['shipped_only'])} derivative(s) with no master")
    print(f"  payload  masters {master_bytes / 1048576:.2f} MB  ->  shipped "
          f"{shipped_bytes / 1048576:.2f} MB")
    if compressed:
        cm = sum(r["bytes"][0] for r in compressed)
        cs = sum(r["bytes"][1] for r in compressed)
        print(f"  compressed  {len(compressed)} asset(s), {cm / cs:.2f}x")
    if copies:
        cs = sum(r["bytes"][1] for r in copies)
        print(f"  shipped UNCOMPRESSED (byte-identical to the master)  {len(copies)} asset(s), "
              f"{cs / 1024:.0f} KB, {100 * cs / shipped_bytes:.1f} % of the payload")

    worst = sorted((r for r in rows if r["bbox_drift_m"] is not None),
                   key=lambda r: -r["rungs"])[:5]
    print("  worst bounding-box disagreement (bound: "
          f"{RUNG_TOLERANCE:.0f} rungs of the asset's own extent):")
    for r in worst:
        print(f"    {r['rungs']:5.2f} rung  {r['bbox_drift_m'] * 1000:8.2f} mm  "
              f"extent {r['extent_m']:7.1f} m  {r['name']}")

    faults = [(r["name"], material_fault(r)) for r in rows if material_fault(r)]
    print(f"  material identity: {len(rows) - len(faults)} of {len(rows)} asset(s) reach the "
          f"site with the master's material names and colours")
    if faults:
        gained = sum(f["textures_gained"] for _, f in faults)
        print(f"    {len(faults)} do not: {gained} texture(s) exist on the site that exist in "
              f"no master, and the names they replace are the key R-W2b plans to wire")
        for name, fault in faults[:5]:
            print(f"      {name}: {fault['master_materials']} -> "
                  f"{fault['shipped_materials']} material(s), "
                  f"+{fault['textures_gained']} texture(s), lost "
                  f"{', '.join(fault['names_lost'][:4])}")
        if len(faults) > 5:
            print(f"      … and {len(faults) - 5} more")

    lost = {}
    for r in rows:
        for a in r["attributes_lost"]:
            lost[a] = lost.get(a, 0) + 1
    if lost:
        detail = ", ".join(f"{k} on {v}" for k, v in sorted(lost.items()))
        print(f"  attributes dropped on the way (not gated, see the docstring): {detail}")


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    """Break each absolute assertion in memory and confirm it fires.

    A gate nobody has seen fail is a gate nobody has seen. This runs against the real
    tree, mutates the parsed result rather than the repository, and asserts that each
    mutation produces at least one problem the clean tree does not.
    """
    result = measure()
    baseline = load_baseline()
    clean = assertions(result, baseline)
    if clean:
        print("SELF-TEST CANNOT RUN — the tree is not clean:", file=sys.stderr)
        for p in clean:
            print(f"  {p}", file=sys.stderr)
        return 1

    def mutate(label, fn):
        import copy
        broken = copy.deepcopy(result)
        fn(broken)
        found = assertions(broken, baseline)
        print(f"  {'caught' if found else 'MISSED'}  {label}"
              + (f" — {found[0][:96]}" if found else ""))
        return bool(found)

    ok = True
    print("self-test: each assertion, broken deliberately")
    ok &= mutate("a derivative with no master",
                 lambda r: r["shipped_only"].append("ghost__phase.glb"))
    ok &= mutate("a master with no derivative",
                 lambda r: r["master_only"].append("orphan__phase.glb"))
    ok &= mutate("the shipped file was simplified",
                 lambda r: r["rows"][0].__setitem__(
                     "triangles", (r["rows"][0]["triangles"][0],
                                   r["rows"][0]["triangles"][1] - 12)))
    ok &= mutate("the shipped file lost its structure_id",
                 lambda r: r["rows"][0]["identity_shipped"].__setitem__("extras", [None]))
    ok &= mutate("the shipped file lost _CONFIDENCE",
                 lambda r: r["rows"][0].__setitem__("attributes_lost", ["_CONFIDENCE"]))
    ok &= mutate("the building collapsed to a two-metre box",
                 lambda r: r["rows"][0].__setitem__("rungs", 8000.0))
    ok &= mutate("a new asset loses its material names",
                 lambda r: _break_materials(r))
    ok &= mutate("a banked asset was repaired and not banked",
                 lambda r: _repair_materials(r, baseline))
    print("SELF-TEST PASS" if ok else "SELF-TEST FAIL")
    return 0 if ok else 1


def _break_materials(result: dict) -> None:
    for row in result["rows"]:
        if not material_fault(row):
            row["names_lost"] = ["log", "chinking"]
            row["colours_lost"] = 2
            row["textures_shipped"] = row["textures_master"] + 2
            return


def _repair_materials(result: dict, baseline: dict) -> None:
    banked = set(baseline.get("material_identity", {}))
    for row in result["rows"]:
        if row["name"] in banked:
            row["names_lost"] = []
            row["colours_lost"] = 0
            row["textures_shipped"] = row["textures_master"]
            return


# ---------------------------------------------------------------- entry point

def load_baseline() -> dict:
    if not BASELINE.exists():
        return {}
    return json.loads(BASELINE.read_text())


def write_baseline(result: dict) -> None:
    faults = {}
    for row in result["rows"]:
        fault = material_fault(row)
        if fault:
            faults[row["name"]] = fault
    BASELINE.write_text(json.dumps({
        "$note": "ROADMAP K36(a). Assets whose shipped derivative does not resolve to the "
                 "material table of the master it was compressed from — gltf-transform's "
                 "palette pass folds their named materials into one PaletteMaterial and two "
                 "generated PNGs. DERIVED — regenerate with "
                 "tools/measure_web_derivatives.py --write-baseline, and only ever to record "
                 "a repair. This file is a RATCHET: tools/check.sh fails on an asset that is "
                 "not here, on a listed one whose loss has grown, and on a listed one that is "
                 "now clean and has not been banked. It is NOT an allowance — K36(b) owns the "
                 "fix, and these are the numbers it takes as its baseline.",
        "measured": "2026-08-16",
        "pairs": len(result["rows"]),
        "material_identity": faults,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {BASELINE.relative_to(ROOT)}: {len(faults)} asset(s)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gate", action="store_true", help="exit 1 on a divergence")
    ap.add_argument("--quiet", action="store_true", help="one summary line on success")
    ap.add_argument("--self-test", action="store_true", dest="selftest",
                    help="break each absolute assertion in memory and confirm it fires")
    ap.add_argument("--write-baseline", action="store_true", dest="write",
                    help="rewrite the material-identity ratchet (deliberate act)")
    args = ap.parse_args()

    if not MASTERS.exists() or not SHIPPED.exists():
        print("no baked assets yet — nothing to compare")
        return 0
    if args.selftest:
        return self_test()

    result = measure()
    if args.write:
        write_baseline(result)
        return 0

    problems = assertions(result, load_baseline())
    if not args.quiet:
        print_census(result)
    for p in problems:
        print(f"FAIL  {p}", file=sys.stderr)
    if problems:
        return 1
    if args.gate or args.quiet:
        rows = result["rows"]
        faults = sum(1 for r in rows if material_fault(r))
        worst = max((r["rungs"] for r in rows), default=0.0)
        print(f"shipped derivatives: {len(rows)} pair(s) carry the master's triangles, node "
              f"identity and contract attributes; worst bounding-box disagreement "
              f"{worst:.2f} of {RUNG_TOLERANCE:.0f} rungs; {faults} asset(s) lose their "
              f"material identity to the publish path (banked, K36(b))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
