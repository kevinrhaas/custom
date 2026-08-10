"""What determines the ground — the staleness hash for a terrain epoch.

The building half of this rule lives in `generators/mesh_inputs.py`, and its
docstring explains at length why a hash over "the files that were involved" is
the wrong hash. The ground was left on exactly that hash: whole file bytes of
`terrain_spec.json`, `river.geojson`, `hydrology.geojson`, `datum.json` and
`terrain_gen.py`, concatenated.

So the false positive `mesh_inputs` was written to end was still standing here,
and it was not hypothetical — it was blocking a repair. `terrain_spec.json` is
the only place a terrain claim's reasoning can be written, three `inferred`
claims carried none, and the validator had to warn rather than fail because
adding a sentence of prose to that file reported the ground as stale and could
not land without a Blender bake. A gate that makes writing a note cost a bake is
a gate that stops notes being written.

## What is hashed

1. **The spec, the traced vectors and the datum with their prose removed** — the
   graded numbers, ids, confidences and coordinates, and nothing that only a
   reader consumes. `note`, `*_note`, `_doc`, `label`, `scope`,
   `critical_caveat`, `why` and `sources` are stripped wherever they appear.
   That set is a DENYLIST on purpose: strip prose and everything else counts, so
   a zone, a reach or a watercourse added to the spec tomorrow is a mesh input
   the day it appears. An allowlist of keys the generator reads today would
   silently stop asking about the newest one, which is the failure this family
   of checks exists to prevent.
2. **The bytes of the code that turns the spec into vertices** —
   `terrain_gen.py`, `generators/common/`, and the pinned Blender.

`sources` is stripped for the same reason a `note` is: a citation is an
obligation the record answers to (`check_terrain_claims` enforces it) and it
cannot move a vertex. `name` is deliberately NOT stripped — in a GeoJSON it also
names the CRS, and dropping `crs.properties.name` would take the coordinate
reference system out of the hash to save a feature title.

This file's own bytes are not hashed. It computes the hash and makes no
geometry — the same rule `mesh_inputs` applies to itself.

## The residual, stated rather than papered over

`terrain_gen.py` goes in whole, so a docstring edit in the generator still
re-stales the ground. That is the identical residual the building hash carries on
`build.py`, it is one file rather than a data file every claim has to be written
in, and no repair is queued behind it. It is written down here so the next person
to meet it knows it is known.

And, as on the building side: this compares inputs, not output. A hand-edited GLB
behind an untouched spec passes, and nothing here can see it.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Bump when the recipe below changes. assets/manifest.json records the scheme its
# terrain entries were stamped under, so a definition change is a visible, dated
# event and the gate refuses a manifest it cannot compute rather than comparing
# two hashes that mean different things.
SCHEME = "resolved-spec-v1"

# Keys whose values are written for a reader. Nothing under `generators/` reads
# any of them — `test_terrain_prose_is_not_read_by_the_generator` holds that open.
PROSE_KEYS = frozenset({"note", "_doc", "label", "scope", "critical_caveat",
                        "why", "sources"})


class TerrainInputsError(ValueError):
    """The inputs to the ground cannot be resolved, so no hash can be taken."""


def is_prose(key: str) -> bool:
    """Is this key documentation of a claim rather than the claim itself?"""
    return key in PROSE_KEYS or key.endswith("_note")


def strip_prose(node):
    """The same document with every prose key removed, at any depth."""
    if isinstance(node, dict):
        return {k: strip_prose(v) for k, v in node.items() if not is_prose(k)}
    if isinstance(node, list):
        return [strip_prose(v) for v in node]
    return node


def _load(path: Path) -> dict:
    if not path.exists():
        raise TerrainInputsError(f"{path.relative_to(ROOT)} is missing, so what this "
                                 f"ground was built from cannot be established")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise TerrainInputsError(f"{path.relative_to(ROOT)} is not loadable: {e}") from e


def _sha_file(p: Path) -> str:
    if not p.exists():
        raise TerrainInputsError(f"{p.relative_to(ROOT)} is missing, so what this "
                                 f"ground was built from cannot be established")
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _code_shas() -> dict[str, str]:
    """The modules whose bytes turn a spec into a ground mesh.

    Not this file, which computes the hash. Not `build.py` or the archetypes,
    which build structures and share nothing with the ground.
    """
    gen = ROOT / "generators"
    wanted = [gen / "terrain_gen.py"] + sorted((gen / "common").glob("*.py"))
    return {p.relative_to(gen).as_posix(): _sha_file(p) for p in wanted}


def terrain_inputs_doc(ep_dir: Path) -> dict:
    """Everything the hash is taken over, as a readable document.

    Exposed separately from the hash for the reason `structure_inputs_doc` is: a
    hash says *that* two builds differ and never *how*, and "why has the ground
    gone stale" is the question this file exists to make answerable. Diff two of
    these.
    """
    ep_dir = Path(ep_dir)
    return {
        "scheme": SCHEME,
        "epoch": ep_dir.name,
        "spec": strip_prose(_load(ep_dir / "terrain_spec.json")),
        "vectors": {
            name: strip_prose(_load(ep_dir / name))
            for name in ("river.geojson", "hydrology.geojson")
        },
        "datum": strip_prose(_load(ROOT / "data" / "datum.json")),
        "code": _code_shas(),
        "blender_pin": (ROOT / "generators" / "blender.pin").read_text().strip(),
    }


def terrain_inputs_sha(ep_dir: Path) -> str:
    """The input hash for one epoch's ground and water GLBs.

    One definition, two callers: the bake writes it into `assets/manifest.json`
    and `tools/validate.py` recomputes it to decide whether the committed meshes
    still match the data. Two copies of this list would agree until the day one
    of them mattered.

    `shoreline.geojson` is deliberately absent: it is traced evidence that
    `build_field` does not yet read, so including it would report the ground as
    stale for a file that cannot change it. It joins the moment the heightfield
    consumes it (ROADMAP § S2e parcel b).
    """
    doc = terrain_inputs_doc(ep_dir)
    return hashlib.sha256(json.dumps(doc, sort_keys=True).encode()).hexdigest()


if __name__ == "__main__":  # pragma: no cover — the "why is it stale" helper
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--epoch", default="e1834_harbor_cut")
    ap.add_argument("--doc", action="store_true", help="print the input document, not the hash")
    a = ap.parse_args()
    d = ROOT / "data" / "terrain" / "epochs" / a.epoch
    print(json.dumps(terrain_inputs_doc(d), sort_keys=True, indent=1) if a.doc
          else terrain_inputs_sha(d))
