#!/usr/bin/env python3
"""Compile per-scene provenance sidecars from the dataset.

    python3 tools/compile_scene.py --scene 1835
    python3 tools/compile_scene.py --all
    python3 tools/compile_scene.py --all --check     # re-derive, change nothing

The renderer reads these, never the raw dataset. That is deliberate: the sidecar
is a flattened, resolved view of one structure at one date, with its citations
already joined in — so the walkthrough and the archival record cannot drift apart,
and the renderer never has to reimplement the phase-resolution rule.

"Cannot drift apart" was a statement about the design and not a check on it until
`--check` existed: the derived files are committed so the site needs no build step,
and a record edited without a recompile shipped a walkthrough quoting the previous
dataset. `tools/check.sh` re-derives them on every commit for the same reason it
re-derives the liberties — drift is a gate failure, not a discovery.

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


CHECK = False
DRIFT: list[str] = []


def load(p: Path):
    return json.loads(p.read_text())


def emit(path: Path, doc) -> None:
    """Write a derived file — or, under `--check`, prove the committed one is
    exactly what this compiler would write."""
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if not CHECK:
        path.write_text(text)
        return
    rel = path.relative_to(ROOT)
    if not path.exists():
        DRIFT.append(f"{rel} is missing")
    elif path.read_text() != text:
        DRIFT.append(f"{rel} is not what the dataset compiles to")


def vertical_anchor(archetype: str) -> str:
    """What this archetype's `y = 0` sits on — `terrain` or `water`.

    docs/GLB-CONTRACT.md pins the convention and says it is "declared per archetype";
    this reads that declaration off the parameter module rather than keeping a second
    list here, for the same reason `terrain_inputs_sha` has one definition: two copies
    agree until the day one of them matters. An archetype that declares nothing is
    placed against the terrain, which is what every building wants.

    Import failures are deliberately NOT fatal. A missing parameter module is already
    an error the staleness gate raises with a better message, and a sidecar compile is
    not the place to discover it.
    """
    gen = str(ROOT / "generators")
    if gen not in sys.path:
        sys.path.insert(0, gen)
    try:
        mod = __import__(f"archetypes.{archetype}_params", fromlist=["VERTICAL_ANCHOR"])
    except Exception:  # noqa: BLE001
        return "terrain"
    return getattr(mod, "VERTICAL_ANCHOR", "terrain")


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


def cite(source_ids, sources: dict) -> list[dict]:
    """Join source ids to the citation the visitor reads. One shape, one place:
    the popup and the exclusions list quote the same record the same way."""
    return [
        {
            "source_id": s,
            "citation": sources[s].get("citation", ""),
            "url": sources[s].get("url", ""),
            "archived_url": sources[s].get("archived_url", ""),
            "tier": sources[s].get("tier"),
        }
        for s in sorted(source_ids) if s in sources
    ]


def compile_exclusions(scene_id: str, scene: dict, target: dt.date,
                       sources: dict, exclusions: dict, outdir: Path) -> int:
    """The structures researched and deliberately LEFT OUT of this scene.

    `data/exclusions.json` is the authored research record and has lived only in
    the repository, where a visitor cannot read it. A town of eight buildings
    looks the same whether a structure is missing because nobody looked, because
    the evidence dates it after the scene, or because it had already come down —
    and those are three completely different statements about the research. This
    derives the second and third kinds, with their citations joined, so the
    walkthrough can say which it is.

    Filtered by the scene's own year rather than shipped wholesale: an entry
    whose `earliest_scene` this scene has reached is not an exclusion here, and
    the validator reports that contradiction rather than this compiler hiding it.
    """
    year = target.year
    entries = []
    for ex in exclusions.get("excluded", []):
        earliest = str(ex.get("earliest_scene") or "")
        if earliest.isdigit() and int(earliest) <= year:
            continue
        entries.append({
            "id": ex.get("id"),
            "name": ex.get("name", ex.get("id")),
            "reason": ex.get("reason", ""),
            "detail": ex.get("detail", ""),
            "earliest_scene": ex.get("earliest_scene"),
            "citations": cite(ex.get("sources", []) or [], sources),
        })

    emit(outdir / "exclusions.json", {
        "scene": scene_id,
        "target_date": scene["target_date"],
        # What the list covers, stated in the derived file so the renderer quotes
        # it rather than composing its own claim about the dataset's completeness.
        "standard": "Structures this project researched and deliberately left out of "
                    "this scene, with the evidence that dates them. It is not a list of "
                    "everything missing: most of the town is simply not built yet.",
        "excluded": entries,
    })
    return len(entries)


def compile_scene(scene_id: str, sources: dict, exclusions: dict) -> int:
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

        # `geometry` travels with the attribute because it qualifies the chip next
        # to it: a documented value the mesh does not contain is a true statement
        # about the evidence and a false one about the view, and the popup has to
        # be able to say which it is showing.
        attributes = {}
        for attr, a in (phase.get("form") or {}).items():
            attributes[attr] = {k: v for k, v in a.items() if k in
                                ("value", "confidence", "sources", "note", "geometry")}
        for key in ("function", "occupants"):
            if key in st:
                attributes[key] = {k: v for k, v in st[key].items() if k in
                                   ("value", "confidence", "sources", "note", "geometry")}

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
                # `terrain` for a building, `water` for a bridge. The renderer must
                # not sample the heightfield for the second kind: mid-channel the
                # ground surface is the river bed, and a bridge placed on it sinks.
                "vertical_anchor": vertical_anchor(st["archetype"]),
            },
            # Carry the footprint's own confidence, not just its geometry — a bare
            # polygon loses precisely the thing the confidence view exists to show.
            "footprint": {
                "polygon": phase.get("footprint", {}).get("polygon", []),
                "confidence": phase.get("footprint", {}).get("confidence", "conjectural"),
            },
            "attributes": attributes,
            "citations": cite(cited, sources),
            "research_note": st.get("research_note", ""),
            "research_doc": f"docs/RESEARCH/{st['id']}.md",
            "review_required": st.get("review_required", False),
        }
        emit(outdir / f"{st['id']}.json", sidecar)
        index.append({"id": st["id"], "name": st["name"],
                      "sidecar": f"sidecars/{scene_id}/{st['id']}.json",
                      "asset": sidecar["asset"]})
        written += 1

    emit(outdir / "index.json", {
        "scene": scene_id,
        "target_date": scene["target_date"],
        "structures": index,
        "excluded_by_date": skipped,
    })

    left_out = compile_exclusions(scene_id, scene, target, sources, exclusions, outdir)

    print(f"scene {scene_id}: {written} sidecar(s), {left_out} researched exclusion(s)"
          + (f", {len(skipped)} excluded by date ({', '.join(skipped)})" if skipped else ""))
    return written


def main() -> int:
    global CHECK
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="re-derive and fail on drift; write nothing")
    args = ap.parse_args()
    CHECK = args.check

    sources = {}
    for p in sorted((DATA / "sources").glob("*.json")):
        s = load(p)
        sources[s["id"]] = s
    exclusions = load(DATA / "exclusions.json")

    scenes = ([p.stem for p in sorted((DATA / "scenes").glob("*.json"))]
              if args.all or not args.scene else [args.scene])
    total = sum(compile_scene(s, sources, exclusions) for s in scenes)
    if CHECK:
        for d in DRIFT:
            print(f"   DRIFT: {d}")
        if DRIFT:
            print(f"{len(DRIFT)} derived file(s) disagree with the dataset — "
                  f"run: python3 tools/compile_scene.py --all")
            return 1
        print("OK: every committed sidecar is what the dataset compiles to")
    return 0 if total else 1


if __name__ == "__main__":
    sys.exit(main())
