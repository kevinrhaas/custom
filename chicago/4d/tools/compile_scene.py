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
                       sources: dict, exclusions: dict, outdir: Path,
                       in_scene: dict | None = None) -> int:
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
    in_scene = in_scene or {}
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

    uncertain = compile_watch_list(scene_id, sources, exclusions, in_scene)

    emit(outdir / "exclusions.json", {
        "scene": scene_id,
        "target_date": scene["target_date"],
        # What the list covers, stated in the derived file so the renderer quotes
        # it rather than composing its own claim about the dataset's completeness.
        "standard": "Structures this project researched and deliberately left out of "
                    "this scene, with the evidence that dates them. It is not a list of "
                    "everything missing: most of the town is simply not built yet.",
        "excluded": entries,
        "uncertain_standard": "Structures whose status on this date is genuinely OPEN — "
                              "neither built with confidence nor ruled out. They are the "
                              "third category, and one of them is standing in front of you.",
        "uncertain": uncertain,
    })
    return len(entries)


def compile_watch_list(scene_id: str, sources: dict, exclusions: dict,
                       in_scene: dict) -> list[dict]:
    """The open questions, which are neither a building nor an exclusion.

    A visitor can be told what stands and, since the exclusions shipped, what was
    researched and left out. Between those sits a third statement the walkthrough
    could not make: researched, and still open. Three of the four are empty
    ground for the same reason a gap is empty — nobody could establish whether
    the building was there — and the fourth is standing in the scene with an
    `inferred` claim about its own date. Putting all four under "what is not
    here" would be false about that one, which is why they get their own section
    rather than a footnote on somebody else's.

    `standing` is derived from the scene rather than read off the entry: whether
    a structure resolves into 1 July 1835 is a fact about the dataset and the
    date, and an entry that asserted it would be one more thing to drift.
    """
    out = []
    for item in exclusions.get("watch_list", []):
        wid = item.get("id")
        phase = in_scene.get(wid)
        entry = {
            "id": wid,
            "name": item.get("name", wid),
            "question": item.get("question", ""),
            "consequence": item.get("consequence", ""),
            "standing": phase is not None,
            "no_source_record": item.get("no_source_record", ""),
            "dossier": item.get("dossier", {}),
            "citations": cite(item.get("sources", []) or [], sources),
        }
        # For the one that IS standing, name the claim on its own record that
        # carries the doubt and repeat that claim's grade — so the section and
        # the provenance card cannot describe the same uncertainty differently.
        ref = (item.get("carried_by") or "").strip()
        if phase is not None and ref.count(".") == 1:
            _, field = ref.split(".")
            claim = phase.get(field) or {}
            entry["carried_by"] = ref
            entry["carried_confidence"] = claim.get("confidence", "")
        out.append(entry)
    return out


# Keys that are the claim's machinery rather than part of what it states: the
# grade itself, the evidence behind it, the reasoning, the names already shown in
# the heading, and the `mesh` map, which is a statement ABOUT the figures
# rather than one of them (it is attached to the rows below instead). Everything
# else in a block is a figure the spec authored and a visitor is entitled to read.
#
# `zone` is in the heading exactly as `id` and `label` are — a surface-material
# block is titled by it — so it is machinery here for the same reason.
GROUND_META_KEYS = {"confidence", "bed_confidence", "sources", "note", "label",
                    "id", "zone", "mesh"}

# The blocks of `terrain_spec.json`, in the order a visitor should meet them:
# what the water is, what it does under the surface, how the land leaves it, what
# each division stands at, and what was laid on top. Order is authored because
# reading order is a piece of writing; membership is not — anything inside these
# blocks that grades itself is surfaced, so a zone added to the spec appears here
# the day it is added.
GROUND_GROUPS = [
    ("water", "the water surface"),
    ("reaches", "the channel beds"),
    ("channel_profile", "the channel cross-section"),
    ("bank", "the bank"),
    ("divisions", "the three divisions"),
    ("marsh_strips", "the marshy shore"),
    ("swales", "the prairie swales"),
    ("watercourses", "the watercourses"),
    ("micro_relief", "the surface texture"),
    ("surface_materials", "what the ground is made of"),
]


def ground_fields(block: dict) -> list[dict]:
    """The figures a spec block states, as the block states them.

    No prose is composed here. A division says `near_ft: 2.4` and the card says
    `near_ft 2.4`, because the moment this function starts writing "rising gently
    from the bank" it is making a claim the record does not.

    Nested structure is skipped rather than flattened: a swale's `line` is a
    polyline of eleven numbers that tells a reader nothing, and the alignment it
    describes is exactly the thing that entry admits is invented.

    A field the terrain generator does not read carries its `mesh:` declaration
    here, on the row, for the reason the provenance card puts the
    same mark beside a building's attribute: a figure a visitor is shown with a
    confidence chip over it, and no vertex behind it, reads as something they are
    looking at. The declaration is authored on the block, in a map keyed by field
    name, and travels to the row so the panel cannot show one without the other.
    """
    declared = block.get("mesh") or {}
    out = []
    for key, value in block.items():
        if key in GROUND_META_KEYS or key.endswith("_note"):
            continue
        if isinstance(value, (dict, type(None))):
            continue
        if isinstance(value, list):
            if len(value) > 4 or any(isinstance(v, (list, dict)) for v in value):
                continue
        field = {"key": key, "value": value}
        if isinstance(declared, dict) and declared.get(key):
            field["mesh"] = declared[key]
        out.append(field)
    return out


def ground_claim(group: str, path: str, block: dict, sources: dict) -> dict | None:
    """One graded statement the ground makes about itself, joined to its evidence.

    A block earns a card by carrying a confidence, which is the same rule the
    provenance popup applies to a building's attributes: a value with a grade on
    it is a claim, and a claim a visitor cannot read is one this project has not
    really made. `channel_profile` grades itself under `bed_confidence`, so the
    key travels with the claim rather than being normalised away — the spec is a
    generator input whose bytes are hashed into the terrain's staleness, and
    tidying its vocabulary would re-stale the ground for a rename.
    """
    key = "confidence" if "confidence" in block else (
        "bed_confidence" if "bed_confidence" in block else None)
    if key is None:
        return None
    notes = [str(block[k]) for k in block if k == "note" or k.endswith("_note")]
    return {
        "id": path,
        "group": group,
        "label": (block.get("label") or block.get("id") or block.get("zone")
                  or path.split(".")[-1]),
        "confidence": block[key],
        "confidence_key": key,
        "fields": ground_fields(block),
        "sources": block.get("sources", []) or [],
        "citations": cite(block.get("sources", []) or [], sources),
        "notes": notes,
    }


def ground_claims(spec: dict, sources: dict) -> list[dict]:
    """Every graded statement in one epoch's terrain spec, in reading order.

    One enumeration, two callers — this compiler, which puts the claims on the
    Evidence panel, and `tools/validate.py`, which holds them to the citation
    rule. A gate walking its own copy of the spec would check a set of claims
    that could quietly stop being the set a visitor reads, which is the drift
    this project keeps closing in other places.
    """
    claims = []
    for group, group_label in GROUND_GROUPS:
        block = spec.get(group)
        if isinstance(block, dict):
            claim = ground_claim(group_label, group, block, sources)
            if claim:
                claims.append(claim)
        elif isinstance(block, list):
            for i, item in enumerate(block):
                if not isinstance(item, dict):
                    continue
                key = item.get("id") or item.get("zone") or i
                claim = ground_claim(group_label, f"{group}.{key}", item, sources)
                if claim:
                    claims.append(claim)
    return claims


def compile_ground(scene_id: str, scene: dict, sources: dict, outdir: Path) -> int:
    """What the ground claims, for the visitor standing on it.

    Every building in this scene can tell you what it asserts, how sure of it we
    are, which sources say so and where the record is weakest. The surface all of
    them stand on could tell you none of that. `terrain_spec.json` is as fully
    graded as any structure record — a documented water plane, three inferred
    division levels arguing from period narrative feet, a conjectural bank face
    and a channel cross-section that says on its own face that it carries no
    evidence at all — and none of it reached any surface a visitor could read.
    The ground even dithers under the confidence view, which shows that a grade
    exists while saying nothing about what it grades.

    Derived, never authored: the spec is a generator input, hashed into the
    terrain's staleness, and this compiler only ever reads it. The measured
    figures come off `heightfield.json`, which the generator wrote — so the
    relief a visitor is told about is the relief the mesh actually has, not a
    number copied into prose and left to rot.
    """
    epoch = scene.get("terrain_epoch", "")
    ep_dir = DATA / "terrain" / "epochs" / epoch
    spec_path = ep_dir / "terrain_spec.json"
    if not spec_path.exists():
        emit(outdir / "terrain.json", {
            "scene": scene_id, "epoch": epoch, "claims": [], "not_modelled": [],
            "standard": f"No terrain spec is committed for epoch '{epoch}', so the "
                        f"ground in this scene makes no recorded claims.",
        })
        return 0

    spec = load(spec_path)
    datum = load(DATA / "datum.json")
    hf = load(ep_dir / "heightfield.json") if (ep_dir / "heightfield.json").exists() else {}

    claims = ground_claims(spec, sources)

    vert = datum.get("vertical", {})
    # The one claim the ground makes that is not in its own spec. Z = 0 is the
    # 1835 water surface by definition, and what that surface stood at above the
    # sea is a working assumption the whole vertical datum hangs off — recorded
    # in datum.json, graded conjectural there, and read by nobody.
    if vert.get("lake_stage_confidence"):
        claims.append({
            "id": "datum.lake_stage",
            "group": "the vertical datum",
            "label": "How high the 1835 water surface stood",
            "confidence": vert["lake_stage_confidence"],
            "confidence_key": "lake_stage_confidence",
            "fields": [{"key": "export_offset_ft_asl", "value": vert.get("export_offset_ft_asl")}],
            "sources": [],
            "citations": [],
            "notes": [t for t in (vert.get("lake_stage_note"), vert.get("internal")) if t],
        })

    relief = (hf.get("relief_ft") or {})
    grid = spec.get("grid", {})
    context = [
        {"label": "Zero", "text": spec.get("vertical", {}).get("datum", "")},
        {"label": "Vertical exaggeration",
         "text": spec.get("vertical", {}).get("exaggeration_note", "")},
        {"label": "The modelled box", "text": grid.get("note", "")},
    ]
    if relief:
        # Measured off the committed heightfield rather than asserted: the whole
        # argument for refusing the dossier's 4-8x exaggeration is that the site
        # really is this flat, and a visitor should get that figure from the mesh
        # they are standing on.
        context.append({
            "label": "Measured relief",
            "text": f"Land in the modelled box runs {relief.get('land_min')} to "
                    f"{relief.get('land_max')} ft above the water surface, and the "
                    f"channel floor reaches {relief.get('channel_min')} ft below it. "
                    f"Measured from the committed heightfield, not asserted.",
        })

    emit(outdir / "terrain.json", {
        "scene": scene_id,
        "target_date": scene["target_date"],
        "epoch": epoch,
        "scope": spec.get("scope", ""),
        # The spec's own caveat, verbatim, for the same reason the exclusions list
        # quotes its own standard: the section's honesty claim belongs to the
        # dataset, not to whichever renderer happens to be displaying it.
        "standard": spec.get("critical_caveat", ""),
        "context": [c for c in context if c["text"]],
        "claims": claims,
        # Researched, sited, and outside this box — the terrain's own version of
        # "what is not here", which the same spec has recorded since it was written.
        "not_modelled": [
            {"dossier_zone": z.get("dossier_zone"), "why": z.get("why", "")}
            for z in spec.get("not_modelled_in_this_box", [])
        ],
    })
    return len(claims)


def compile_scene(scene_id: str, sources: dict, exclusions: dict) -> int:
    scene = load(DATA / "scenes" / f"{scene_id}.json")
    target = dt.date.fromisoformat(scene["target_date"])
    outdir = DATA / "sidecars" / scene_id
    outdir.mkdir(parents=True, exist_ok=True)

    written, skipped = 0, []
    index = []
    # id -> the phase that resolves into this scene, for the watch list below
    resolved: dict[str, dict] = {}

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

        # THE PHASE'S CLAIM ABOUT ITSELF. Every `form` attribute has carried its
        # note to the card since the card was written; the two phase-level blocks
        # a visitor is most likely to ask about — was it here, and how do you know
        # where — carried only a confidence chip, and `documented_range` did not
        # reach the sidecar at all. The popup has read `documented_range` since it
        # was written and this compiler never wrote it, so the line has never once
        # rendered: the question the whole scene rests on was answered nowhere in
        # the walkthrough while being argued at length in the record.
        #
        # Note the shape is the SAME as an attribute's — value/confidence/sources/
        # note — because the card renders these rows with the attribute renderer.
        # Two renderers describing the same kind of claim differently is the drift
        # this project keeps closing.
        rng = phase.get("documented_range", {})
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
            # Was it here at all? The scene date falls inside this span by
            # construction — resolve_phase would not have returned the phase
            # otherwise — so what the card has to show is not the fact but the
            # STRENGTH of it, and the reasoning behind the end of the range, which
            # for a building nobody followed past 1834 is the weakest claim on it.
            "documented_range": {
                "from": rng.get("from", ""),
                "to": rng.get("to", ""),
                "confidence": rng.get("confidence", "conjectural"),
                "sources": rng.get("sources", []),
                "note": rng.get("note", ""),
            },
            # What this phase IS, in the record's own words. Written for a reader
            # and read by nobody: it is where a record says that a building holding
            # the post office for three years is not the post office on the scene
            # date, which no chip can express.
            "change_note": phase.get("change_note", ""),
            "placement": {
                "local_e": local_e,
                "local_n": local_n,
                "rotation_deg": pos.get("rotation_deg", 0.0),
                "position_confidence": pos.get("confidence", "conjectural"),
                "position_sources": pos.get("sources", []),
                "position_note": pos.get("note", ""),
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
        resolved[st["id"]] = phase
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

    left_out = compile_exclusions(scene_id, scene, target, sources, exclusions, outdir,
                                  in_scene=resolved)
    ground = compile_ground(scene_id, scene, sources, outdir)

    print(f"scene {scene_id}: {written} sidecar(s), {left_out} researched exclusion(s), "
          f"{ground} ground claim(s)"
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
