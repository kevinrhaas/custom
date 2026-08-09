#!/usr/bin/env python3
"""Compile per-scene provenance sidecars from the dataset.

    python3 tools/compile_scene.py --scene 1835
    python3 tools/compile_scene.py --all

The renderer reads these, never the raw dataset. That is deliberate: the sidecar
is a flattened, resolved view of one structure at one date, with its citations
already joined in — so the walkthrough and the archival record cannot drift apart,
and the renderer never has to reimplement the phase-resolution rule.

Pure Python, no Blender. See docs/GLB-CONTRACT.md § "The sidecar".
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(p: Path):
    return json.loads(p.read_text())


def resolve_phase(structure: dict, target: dt.date):
    """Exactly one phase must cover the date — the same rule the validator and
    the generator apply. Duplicated deliberately in three places is worse than
    duplicated in two, so if this grows further it moves to a shared module."""
    hits = []
    for ph in structure.get("phases", []):
        r = ph.get("documented_range", {})
        try:
            frm, to = dt.date.fromisoformat(r["from"]), dt.date.fromisoformat(r["to"])
        except (KeyError, ValueError):
            continue
        if frm <= target <= to:
            hits.append(ph)
    if len(hits) > 1:
        raise SystemExit(f"{structure['id']}: {len(hits)} phases cover {target}")
    return hits[0] if hits else None


def compile_scene(scene_id: str, sources: dict) -> int:
    scene = load(DATA / "scenes" / f"{scene_id}.json")
    target = dt.date.fromisoformat(scene["target_date"])
    outdir = DATA / "sidecars" / scene_id
    outdir.mkdir(parents=True, exist_ok=True)

    written, skipped = 0, []
    index = []

    for path in sorted((DATA / "structures").glob("*.json")):
        st = load(path)
        phase = resolve_phase(st, target)
        if phase is None:
            skipped.append(st["id"])
            continue

        # gather every source cited anywhere in this phase, so the popup can show
        # the evidence without the renderer walking the dataset
        cited: set[str] = set()

        def collect(node):
            if isinstance(node, dict):
                for s in node.get("sources", []) or []:
                    cited.add(s)
                for v in node.values():
                    collect(v)
            elif isinstance(node, list):
                for v in node:
                    collect(v)

        collect(phase)
        for key in ("function", "occupants"):
            collect(st.get(key, {}))

        attributes = {}
        for attr, a in (phase.get("form") or {}).items():
            attributes[attr] = {k: v for k, v in a.items() if k in
                                ("value", "confidence", "sources", "note")}
        for key in ("function", "occupants"):
            if key in st:
                attributes[key] = {k: v for k, v in st[key].items() if k in
                                   ("value", "confidence", "sources", "note")}

        pos = phase.get("position", {})
        provisional = pos.get("utm_e") is None
        datum = load(DATA / "datum.json")
        if provisional:
            local_e = local_n = 0.0
        else:
            local_e = round(pos["utm_e"] - datum["origin_utm_e"], 3)
            local_n = round(pos["utm_n"] - datum["origin_utm_n"], 3)

        sidecar = {
            "id": st["id"],
            "phase": phase["id"],
            "name": st["name"],
            "aka": st.get("aka", []),
            "archetype": st["archetype"],
            "asset": f"gltf/{st['id']}__{phase['id']}.glb",
            "scene": scene_id,
            "target_date": scene["target_date"],
            "placement": {
                "local_e": local_e,
                "local_n": local_n,
                "rotation_deg": pos.get("rotation_deg", 0.0),
                "position_confidence": pos.get("confidence", "conjectural"),
                "symbolic_location": pos.get("symbolic_location", ""),
                "uncertainty_m": 20,
                "placement_provisional": provisional,
            },
            "footprint": phase.get("footprint", {}).get("polygon", []),
            "attributes": attributes,
            "citations": [
                {
                    "source_id": s,
                    "citation": sources[s].get("citation", ""),
                    "url": sources[s].get("url", ""),
                    "archived_url": sources[s].get("archived_url", ""),
                    "tier": sources[s].get("tier"),
                }
                for s in sorted(cited) if s in sources
            ],
            "research_note": st.get("research_note", ""),
            "research_doc": f"docs/RESEARCH/{st['id']}.md",
            "review_required": st.get("review_required", False),
        }
        (outdir / f"{st['id']}.json").write_text(
            json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n")
        index.append({"id": st["id"], "name": st["name"],
                      "sidecar": f"sidecars/{scene_id}/{st['id']}.json",
                      "asset": sidecar["asset"]})
        written += 1

    (outdir / "index.json").write_text(json.dumps({
        "scene": scene_id,
        "target_date": scene["target_date"],
        "structures": index,
        "excluded_by_date": skipped,
    }, indent=2, ensure_ascii=False) + "\n")

    print(f"scene {scene_id}: {written} sidecar(s)"
          + (f", {len(skipped)} excluded by date ({', '.join(skipped)})" if skipped else ""))
    return written


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    sources = {}
    for p in sorted((DATA / "sources").glob("*.json")):
        s = load(p)
        sources[s["id"]] = s

    scenes = ([p.stem for p in sorted((DATA / "scenes").glob("*.json"))]
              if args.all or not args.scene else [args.scene])
    total = sum(compile_scene(s, sources) for s in scenes)
    return 0 if total else 1


if __name__ == "__main__":
    sys.exit(main())
