#!/usr/bin/env python3
"""What a generator half for a renderer-drawn layer would cost, measured.

    tools/measure_generator_half.py            print both readings
    tools/measure_generator_half.py --gate     exit 1 if a stated figure has moved

WHY THIS EXISTS. Ticket T-0059 asked for *"a river-wharf mode of `pier_crib`"*,
so that a town assembled from GLBs alone would carry its docks. `docs/ROADMAP.md`
K5 makes the same request of three other clauses in almost the same words — *"the
generator half, so a baked town carries its own yards"*. Before building one, two
things wanted a number rather than an opinion:

  1. **How many committed meshes does adding it re-stale?** `generators/
     mesh_inputs.py` hashes an archetype's builder, `generators/build.py` and
     `generators/common/*.py` into every asset's `inputs_sha256`, and
     `tools/validate.py` fails on any asset whose recomputed hash has moved. So
     the cost of adding a mode is not the mode: it is the rebake of everything
     the edited file's bytes reach, and `AGENTS.md` puts Blender off the improve
     runner. This measures that reach per candidate edit site.

  2. **Is a wharf the only layer that owes one?** The wharf is the fifth data
     layer drawn at load out of committed JSON rather than baked. If the debt is
     general, paying it one layer at a time — by a route that re-stales the town
     each time — is the wrong shape of work, and the ticket is a fragment of a
     decision nobody has made rather than a unit anybody can ship.

Both readings are printed. `--gate` holds them against the figures written into
this file's own `STATED` block, which is what makes them a measurement rather
than a number somebody remembers: the two are meant to be edited together, and a
reading that moves without the sentence beside it moving is the drift.

NO BLENDER, NO NETWORK. It reads `assets/manifest.json`, the generator modules'
own hashing recipes and the committed layer manifests, all of which are in the
tree — the same standing this tool's neighbours in `tools/measure_*.py` have.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "generators"
DATA = ROOT / "data"
MANIFEST = ROOT / "assets" / "manifest.json"
RENDERER = ROOT / "renderers" / "web" / "js"

# The reading this file was written against, on 2026-08-24 (T-0059). `--gate`
# holds the live measurement to it. Moving a figure here is a claim that the
# reach changed, and it belongs in the same commit as whatever changed it.
STATED = {
    "assets": 348,
    "restales": {
        "generators/common/*.py": 348,
        "generators/build.py": 346,
        "generators/terrain_gen.py": 2,
        "generators/archetypes/pier_crib.py": 2,
    },
    "layers_drawn_at_load": 9,
    "layers_with_a_generator": 0,
}

# The data layers a renderer draws at load out of committed JSON, rather than
# loading a baked GLB for. Each is a directory under `data/` carrying its own
# `index.json` manifest — a static host cannot be globbed, which is why every one
# of them has one — plus the renderer module that consumes it. NAMED, not sniffed:
# a glob over `data/*/index.json` would silently pick up the next manifest that is
# not a drawn layer, and this reading's whole value is that its denominator is
# something a reader checked.
DRAWN_AT_LOAD = {
    "boats": "boats.js",
    "enclosures": "enclosures.js",
    "fauna": "fauna.js",
    "flora": "flora.js",
    "frontage": "frontage.js",
    "residents": "residents.js",
    "signage": "signage.js",
    "wharves": "wharves.js",
    "yard": "yard.js",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def restale_reach() -> tuple[dict, int, list]:
    """Per candidate edit site, how many committed assets its bytes are hashed into.

    The reach is not read off the files — it is read off the two hashing recipes,
    which is the only reading that cannot go stale behind them:

      * `mesh_inputs._code_shas(archetype)` names what a STRUCTURE asset's hash
        covers: `build.py`, that archetype's builder, and `common/*.py`.
      * `terrain_inputs._code_shas()` names what a TERRAIN asset's covers:
        `terrain_gen.py` and `common/*.py`.

    So a site's reach is the count of assets whose recipe names it.
    """
    problems: list[str] = []
    if not MANIFEST.exists():
        return {}, 0, ["assets/manifest.json is missing, so no reach can be measured"]
    sys.path.insert(0, str(GEN))
    try:
        import mesh_inputs                      # noqa: PLC0415
        import terrain_inputs                   # noqa: PLC0415
    except Exception as e:                      # noqa: BLE001
        return {}, 0, [f"cannot import the generators' hashing recipes: {e}"]

    assets = load(MANIFEST).get("assets", {})
    reach: dict[str, int] = {}
    for entry in assets.values():
        if entry.get("structure_id"):
            arch = entry.get("archetype")
            if not arch:
                problems.append("a structure asset in the manifest names no archetype")
                continue
            try:
                names = mesh_inputs._code_shas(arch)      # noqa: SLF001
            except Exception as e:                        # noqa: BLE001
                problems.append(f"archetype {arch}: {e}")
                continue
        elif entry.get("terrain_epoch"):
            names = terrain_inputs._code_shas()           # noqa: SLF001
        else:
            continue
        for rel in names:
            key = "generators/common/*.py" if rel.startswith("common/") \
                else f"generators/{rel}"
            reach[key] = reach.get(key, 0) + 1
    # `common/*.py` is counted once per FILE above; collapse it to once per asset.
    commons = len(sorted((GEN / "common").glob("*.py"))) or 1
    if "generators/common/*.py" in reach:
        reach["generators/common/*.py"] //= commons
    return reach, len(assets), problems


def layer_debt() -> tuple[list, list]:
    """Per drawn-at-load layer: is there anything under `generators/` that builds it?

    The test is deliberately blunt, because the answer is: an archetype module
    named for the layer, or a manifest asset whose archetype is. A layer with
    neither is drawn by the renderer and by nothing else, which is what "owes a
    generator half" means.
    """
    problems: list[str] = []
    assets = load(MANIFEST).get("assets", {}) if MANIFEST.exists() else {}
    baked = {e.get("archetype") for e in assets.values() if e.get("archetype")}
    rows = []
    for layer, module in sorted(DRAWN_AT_LOAD.items()):
        index = DATA / layer / "index.json"
        js = RENDERER / module
        if not index.exists():
            problems.append(f"{layer}: data/{layer}/index.json is missing, so this "
                            f"layer is not the drawn layer this file names")
        if not js.exists():
            problems.append(f"{layer}: renderers/web/js/{module} is missing, so "
                            f"nothing draws it and this reading is out of date")
        arch = GEN / "archetypes" / f"{layer}.py"
        records = 0
        if index.exists():
            doc = load(index)
            # The manifests do not agree on a key — `wharves`, `zones`,
            # `households` — so the count is the one list in the document.
            lists = [v for v in doc.values() if isinstance(v, list)]
            records = len(lists[0]) if lists else 0
        rows.append({
            "layer": layer,
            "module": module,
            "records": records,
            "generator": arch.exists() or layer in baked,
        })
    return rows, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", action="store_true",
                    help="exit 1 if a measured figure has moved off the stated one")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    reach, total, problems = restale_reach()
    rows, more = layer_debt()
    problems += more
    drawn = len(rows)
    owed = sum(1 for r in rows if not r["generator"])

    if not args.quiet:
        print(f"COMMITTED, INPUT-TRACKED ASSETS: {total}\n")
        print(f"{'edit site':<42} {'re-stales':>9}   what a rebake would have to reach")
        for site, n in sorted(reach.items(), key=lambda kv: -kv[1]):
            share = ("every committed mesh" if n >= total
                     else "every structure in the town" if n >= total - 2
                     else "the ground" if site.endswith("terrain_gen.py")
                     else "the meshes of that archetype alone")
            print(f"{site:<42} {n:>9}   {share}")
        print(f"\nLAYERS DRAWN AT LOAD FROM COMMITTED JSON: {drawn}, "
              f"{drawn - owed} with a generator, {owed} without\n")
        print(f"{'layer':<12} {'renderer module':<18} {'records':>8}  generator")
        for r in rows:
            print(f"{r['layer']:<12} {r['module']:<18} {r['records']:>8}  "
                  f"{'yes' if r['generator'] else 'NONE'}")

    for key, want in STATED["restales"].items():
        got = reach.get(key)
        if got != want:
            problems.append(f"{key} re-stales {got} asset(s); this file states {want}")
    if total != STATED["assets"]:
        problems.append(f"{total} committed asset(s); this file states {STATED['assets']}")
    if drawn != STATED["layers_drawn_at_load"]:
        problems.append(f"{drawn} layer(s) drawn at load; this file states "
                        f"{STATED['layers_drawn_at_load']}")
    if drawn - owed != STATED["layers_with_a_generator"]:
        problems.append(f"{drawn - owed} drawn layer(s) have a generator; this file "
                        f"states {STATED['layers_with_a_generator']}")

    for p in problems:
        print(f"FAIL  {p}", file=sys.stderr)
    if problems:
        return 1
    if args.gate:
        print(f"generator half: {owed} of {drawn} drawn layers owe one; the cheapest "
              f"route into the bake re-stales "
              f"{min(reach.values()) if reach else 0} committed mesh(es), the "
              f"shared ones {max(reach.values()) if reach else 0}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
