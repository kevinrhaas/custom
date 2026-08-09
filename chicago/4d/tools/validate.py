#!/usr/bin/env python3
"""Validate the 4D Chicago dataset.

Runs in seconds and needs no Blender. This is the per-commit gate.

    validate.py              schema + referential + semantic + scene date gates
    validate.py --params     also resolve every phase's form to archetype params
    validate.py --licenses   also check asset license coverage and rights gating
    validate.py --stale      also check committed GLBs against assets/manifest.json
    validate.py --site       also check publish sync and the published size budget
    validate.py --all        everything
    validate.py --strict     warnings become errors

The rules enforced here are the project's contract, not style preferences:
documented requires a resolving source, inferred requires stated reasoning, a
structure must have exactly one phase covering a scene's date, and geometry
cannot be generated while the datum origin is unverified.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# A documented_range spanning more than this earns a warning. Chicago between
# 1833 and 1837 changed faster than almost any settlement in American history;
# a wide range is usually a research gap wearing a disguise.
WIDE_RANGE_YEARS = 12

# Published payload budget. GitHub Pages does not serve Git LFS objects, so the
# published tree holds plain binaries and has to stay reasonable.
SITE_BUDGET_MB = 25

CONFIDENCE = ("documented", "inferred", "conjectural")
SLUG = re.compile(r"^[a-z0-9_]+$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def ok(self, strict: bool) -> bool:
        return not self.errors and not (strict and self.warnings)

    def print(self, strict: bool) -> None:
        for n in self.notes:
            print(f"  {n}")
        for w in self.warnings:
            print(f"  WARN  {w}")
        for e in self.errors:
            print(f"  FAIL  {e}")
        n_e, n_w = len(self.errors), len(self.warnings)
        verdict = "PASS" if self.ok(strict) else "FAIL"
        print(f"\n{verdict}  {n_e} error(s), {n_w} warning(s)"
              + ("  [strict: warnings are errors]" if strict else ""))


def load_json(path: Path, rep: Report, required: bool = True):
    if not path.exists():
        if required:
            rep.error(str(path.relative_to(ROOT)), "missing")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        rep.error(str(path.relative_to(ROOT)), f"invalid JSON: {e}")
        return None


def parse_date(s: str):
    try:
        return dt.date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


# --------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------

def validate_schemas(sources, structures, scenes, rep: Report) -> None:
    """JSON Schema pass, when jsonschema is installed.

    The semantic checks below are the ones that actually protect the dataset,
    so a missing jsonschema degrades to a warning rather than blocking work.
    """
    try:
        import jsonschema
    except ImportError:
        rep.warn("schema", "jsonschema not installed; skipping schema pass "
                           "(pip install jsonschema). Semantic checks still ran.")
        return

    pairs = [
        (DATA / "source.schema.json", sources, "source"),
        (DATA / "structures.schema.json", structures, "structure"),
        (DATA / "scene.schema.json", scenes, "scene"),
    ]
    for schema_path, docs, label in pairs:
        if not schema_path.exists():
            rep.error("schema", f"missing schema {schema_path.name}")
            continue
        schema = load_json(schema_path, rep)
        if schema is None:
            continue
        validator = jsonschema.Draft202012Validator(schema)
        for path, doc in docs.items():
            for err in sorted(validator.iter_errors(doc), key=lambda e: e.path):
                loc = "/".join(str(p) for p in err.path) or "(root)"
                rep.error(f"{label} {path}", f"{loc}: {err.message}")


# --------------------------------------------------------------------------
# semantic: the confidence contract
# --------------------------------------------------------------------------

def check_attested(where: str, key: str, att: dict, source_ids: set, rep: Report) -> str | None:
    """documented needs a resolving source; inferred needs stated reasoning."""
    if not isinstance(att, dict) or "confidence" not in att:
        return None
    conf = att.get("confidence")
    if conf not in CONFIDENCE:
        rep.error(where, f"{key}: unknown confidence '{conf}'")
        return None

    srcs = att.get("sources") or []
    note = (att.get("note") or "").strip()

    if conf == "documented":
        if not srcs:
            rep.error(where, f"{key}: documented requires at least one source_id")
        for sid in srcs:
            if sid not in source_ids:
                rep.error(where, f"{key}: source '{sid}' does not resolve in data/sources/")
    elif conf == "inferred":
        if not note:
            rep.error(where, f"{key}: inferred requires a note stating the reasoning")
        for sid in srcs:
            if sid not in source_ids:
                rep.error(where, f"{key}: source '{sid}' does not resolve in data/sources/")
    else:  # conjectural
        if srcs:
            rep.warn(where, f"{key}: conjectural but cites sources — either the source "
                            f"supports it (make it documented/inferred) or the citation is decorative")
    return conf


def walk_attested(where: str, node, source_ids: set, rep: Report, tally: dict, prefix: str = "") -> None:
    """Find every attested block in a record and check it."""
    if isinstance(node, dict):
        if "confidence" in node and "value" in node:
            conf = check_attested(where, prefix or "(attr)", node, source_ids, rep)
            if conf:
                tally[conf] = tally.get(conf, 0) + 1
            return
        for k, v in node.items():
            walk_attested(where, v, source_ids, rep, tally, f"{prefix}.{k}" if prefix else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_attested(where, v, source_ids, rep, tally, f"{prefix}[{i}]")


def check_range(where: str, rng: dict, source_ids: set, rep: Report) -> tuple:
    frm, to = parse_date(rng.get("from", "")), parse_date(rng.get("to", ""))
    if frm is None or to is None:
        rep.error(where, "documented_range: from/to must be ISO dates")
        return None, None
    if to < frm:
        rep.error(where, f"documented_range: to ({to}) precedes from ({frm})")
    # A wide range is only suspicious when it is a guess. A building that demonstrably
    # stood for twenty years and burned on a recorded date is not the failure mode this
    # rule exists to catch — a vague range widened until the date gate stopped complaining is.
    if (to - frm).days > WIDE_RANGE_YEARS * 365.25 and rng.get("confidence") != "documented":
        rep.warn(where, f"documented_range spans {(to - frm).days // 365} years and is not "
                        f"documented — Chicago changed fast in this period; narrow it to what "
                        f"is attested rather than widening it to pass")
    for sid in rng.get("sources") or []:
        if sid not in source_ids:
            rep.error(where, f"documented_range: source '{sid}' does not resolve")
    if rng.get("confidence") == "inferred" and not (rng.get("note") or "").strip():
        rep.error(where, "documented_range: inferred requires a note")
    return frm, to


# --------------------------------------------------------------------------
# semantic: scenes resolve against phases
# --------------------------------------------------------------------------

def validate_scene(scene: dict, structures: dict, epochs: dict, exclusions: dict, rep: Report) -> None:
    sid = scene.get("id", "?")
    where = f"scene {sid}"
    target = parse_date(scene.get("target_date", ""))
    if target is None:
        rep.error(where, "target_date must be an ISO date")
        return

    # the epoch must exist and cover the date
    ep_id = scene.get("terrain_epoch")
    ep = epochs.get(ep_id)
    if ep is None:
        rep.error(where, f"terrain_epoch '{ep_id}' does not resolve in data/terrain/epochs.json")
    else:
        frm, to = parse_date(ep.get("from", "")), parse_date(ep.get("to", ""))
        if frm and to and not (frm <= target <= to):
            rep.error(where, f"terrain_epoch '{ep_id}' covers {frm}..{to}, "
                             f"which does not include target_date {target}")

    included, excluded, blocked = [], [], []
    for path, st in structures.items():
        covering = []
        for ph in st.get("phases", []):
            rng = ph.get("documented_range", {})
            frm, to = parse_date(rng.get("from", "")), parse_date(rng.get("to", ""))
            if frm and to and frm <= target <= to:
                covering.append(ph.get("id", "?"))
        if len(covering) > 1:
            rep.error(f"structure {st.get('id', path)}",
                      f"{len(covering)} phases cover scene {sid} ({target}): {covering} — "
                      f"exactly one must")
        elif len(covering) == 1:
            included.append(f"{st.get('id')}:{covering[0]}")
            if st.get("review_required"):
                blocked.append(st.get("id"))
        else:
            excluded.append(st.get("id"))

    if scene.get("released") and blocked:
        rep.error(where, f"released is true but these records carry review_required: {blocked}")

    rep.note(f"scene {sid} ({target}): {len(included)} structure(s) included, "
             f"{len(excluded)} excluded by date"
             + (f" [{', '.join(excluded)}]" if excluded else ""))

    # exclusions.json is a research record, not a filter — but it should not
    # contradict the dataset by naming something that is actually in the scene.
    for ex in exclusions.get("excluded", []):
        if ex.get("id") in [i.split(":")[0] for i in included]:
            rep.error(where, f"'{ex.get('id')}' is listed in exclusions.json but resolves "
                             f"into this scene — the data and the research record disagree")


# --------------------------------------------------------------------------
# loaders
# --------------------------------------------------------------------------

def load_dir(d: Path, rep: Report) -> dict:
    out = {}
    if not d.exists():
        return out
    for p in sorted(d.glob("*.json")):
        doc = load_json(p, rep)
        if doc is not None:
            out[p.name] = doc
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--params", action="store_true")
    ap.add_argument("--licenses", action="store_true")
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--site", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    if args.all:
        args.params = args.licenses = args.stale = args.site = True

    rep = Report()

    sources = load_dir(DATA / "sources", rep)
    structures = load_dir(DATA / "structures", rep)
    scenes = load_dir(DATA / "scenes", rep)

    source_ids = {s.get("id") for s in sources.values() if isinstance(s, dict)}
    for name, s in sources.items():
        if isinstance(s, dict) and s.get("id") != Path(name).stem:
            rep.error(f"source {name}", f"id '{s.get('id')}' does not match filename stem")
        if isinstance(s, dict) and s.get("type") == "website" and not s.get("archived_url"):
            rep.warn(f"source {name}", "website source without archived_url — several key hosts "
                                       "for this project return 503/403 intermittently; a citation "
                                       "that cannot be re-read is not a citation")

    datum = load_json(DATA / "datum.json", rep) or {}
    epochs_doc = load_json(DATA / "terrain" / "epochs.json", rep) or {}
    epochs = {e["id"]: e for e in epochs_doc.get("epochs", []) if isinstance(e, dict)}
    exclusions = load_json(DATA / "exclusions.json", rep) or {}

    validate_schemas(sources, structures, scenes, rep)

    # epoch intervals must not overlap
    spans = []
    for e in epochs.values():
        frm, to = parse_date(e.get("from", "")), parse_date(e.get("to", ""))
        if frm and to:
            spans.append((frm, to, e["id"]))
    for i, (f1, t1, id1) in enumerate(sorted(spans)):
        for f2, t2, id2 in sorted(spans)[i + 1:]:
            if f2 <= t1 and f1 <= t2:
                rep.error("epochs", f"'{id1}' ({f1}..{t1}) overlaps '{id2}' ({f2}..{t2})")

    active = [e["id"] for e in epochs.values() if e.get("status") == "active"]
    if len(active) > 1:
        rep.warn("epochs", f"{len(active)} epochs marked active ({active}); only one should be "
                           f"active until the first milestone ships")

    # structures
    tally: dict = {}
    for name, st in structures.items():
        sid = st.get("id", name)
        where = f"structure {sid}"
        if sid != Path(name).stem:
            rep.error(where, f"id does not match filename stem '{Path(name).stem}'")
        if not SLUG.match(sid or ""):
            rep.error(where, f"id '{sid}' is not a lowercase slug")

        phase_ids = set()
        for ph in st.get("phases", []):
            pid = ph.get("id", "?")
            pwhere = f"{where}/{pid}"
            if pid in phase_ids:
                rep.error(where, f"duplicate phase id '{pid}'")
            phase_ids.add(pid)
            check_range(pwhere, ph.get("documented_range", {}), source_ids, rep)

            pos = ph.get("position", {})
            if pos.get("utm_e") is None and not (pos.get("symbolic_location") or "").strip():
                rep.error(pwhere, "position has no coordinates and no symbolic_location — "
                                  "a structure must be locatable in words even before the datum "
                                  "is verified")
            walk_attested(pwhere, ph.get("form", {}), source_ids, rep, tally, "form")
            check_attested(pwhere, "position", pos, source_ids, rep)
            check_attested(pwhere, "footprint", ph.get("footprint", {}), source_ids, rep)
            tally[pos.get("confidence")] = tally.get(pos.get("confidence"), 0) + 1
            fp_conf = ph.get("footprint", {}).get("confidence")
            tally[fp_conf] = tally.get(fp_conf, 0) + 1

        for key in ("function", "occupants"):
            if key in st:
                check_attested(where, key, st[key], source_ids, rep)
                c = st[key].get("confidence")
                tally[c] = tally.get(c, 0) + 1

    # scenes
    for name, sc in scenes.items():
        validate_scene(sc, structures, epochs, exclusions, rep)

    # the datum gate — the single most consequential check in the suite
    if not datum.get("verified"):
        rep.note("datum is UNVERIFIED — generators and bake will refuse to run. "
                 "This is by design: fixing the origin after geometry exists means "
                 "regenerating everything. See docs/EPOCHS.md.")

    # optional passes
    if args.params:
        run_param_check(structures, scenes, rep)
    if args.licenses:
        run_license_check(sources, rep)
    if args.stale:
        run_stale_check(rep)
    if args.site:
        run_site_check(rep)

    # confidence summary — the honest picture of the dataset
    total = sum(v for k, v in tally.items() if k)
    if total:
        print(f"\nConfidence across {total} attributes in {len(structures)} structure(s):")
        for level in CONFIDENCE:
            n = tally.get(level, 0)
            bar = "#" * round(40 * n / total) if total else ""
            print(f"  {level:<12} {n:>4}  {100 * n / total:5.1f}%  {bar}")

    print()
    rep.print(args.strict)
    return 0 if rep.ok(args.strict) else 1


def run_param_check(structures: dict, scenes: dict, rep: Report) -> None:
    """Resolve every scene-included phase into archetype parameters.

    Imports only the pure-Python `*_params.py` halves — no bpy, so this runs in
    any agent sandbox in milliseconds. It catches the failure mode where a record
    is schema-valid but produces a building 400 metres tall, long before anyone
    spends minutes on a bake.
    """
    sys.path.insert(0, str(ROOT / "generators"))
    resolvers = {}
    arch_dir = ROOT / "generators" / "archetypes"
    if not arch_dir.exists():
        rep.note("--params: no archetype modules yet")
        return
    for mod_path in sorted(arch_dir.glob("*_params.py")):
        name = mod_path.stem.removesuffix("_params")
        try:
            mod = __import__(f"archetypes.{mod_path.stem}", fromlist=["from_phase"])
            resolvers[name] = mod.from_phase
        except Exception as e:  # noqa: BLE001 — a broken generator must fail the gate
            rep.error("params", f"cannot import {mod_path.name}: {e}")

    checked, no_gen = 0, set()
    for sc in scenes.values():
        target = parse_date(sc.get("target_date", ""))
        if target is None:
            continue
        for st in structures.values():
            arch = st.get("archetype")
            for ph in st.get("phases", []):
                r = ph.get("documented_range", {})
                frm, to = parse_date(r.get("from", "")), parse_date(r.get("to", ""))
                if not (frm and to and frm <= target <= to):
                    continue
                if arch not in resolvers:
                    no_gen.add(arch)
                    continue
                try:
                    resolvers[arch](ph)
                    checked += 1
                except Exception as e:  # noqa: BLE001
                    rep.error(f"structure {st.get('id')}/{ph.get('id')}",
                              f"does not resolve into {arch} parameters: {e}")
    rep.note(f"param check: {checked} phase(s) resolved"
             + (f"; no generator yet for {sorted(no_gen)}" if no_gen else ""))


def run_license_check(sources: dict, rep: Report) -> None:
    licenses = ROOT / "assets" / "LICENSES.md"
    if not licenses.exists():
        rep.error("licenses", "assets/LICENSES.md is missing")
        return
    text = licenses.read_text()
    manifest_path = ROOT / "assets" / "manifest.json"
    manifest = json.loads(manifest_path.read_text()).get("assets", {}) \
        if manifest_path.exists() else {}

    generated, third_party = 0, 0
    for p in sorted((ROOT / "assets").rglob("*")):
        if p.is_dir() or p.name in ("LICENSES.md", "manifest.json") or p.name.startswith("."):
            continue
        rel = p.relative_to(ROOT / "assets").as_posix()

        # Build output under gltf/ and web/ is provenance-tracked by the manifest
        # (which records its input hash and the Blender that made it), not by a
        # hand-written licence row. Untracked build output IS an error — it means
        # a file appeared that no recorded bake produced.
        if rel.startswith(("gltf/", "web/")):
            if p.name in manifest:
                generated += 1
            else:
                rep.error("licenses", f"assets/{rel} is not in assets/manifest.json — "
                                      f"no recorded bake produced it")
            continue

        if rel not in text:
            rep.error("licenses", f"assets/{rel} has no entry in assets/LICENSES.md")
        third_party += 1
    rep.note(f"license check: {generated} generated (manifest-tracked), "
             f"{third_party} authored/third-party asset(s)")

    # rights gating: nothing may be derived from a source still awaiting a check
    for name, s in sources.items():
        if s.get("rights_status") in ("check_required", "restricted") \
                and s.get("asset_use") == "geometry":
            rep.error(f"source {name}",
                      f"rights_status is '{s['rights_status']}' but asset_use is 'geometry' — "
                      f"resolve the rights check before deriving geometry from this source")


def run_stale_check(rep: Report) -> None:
    manifest_path = ROOT / "assets" / "manifest.json"
    glbs = sorted((ROOT / "assets" / "gltf").glob("*.glb"))
    if not manifest_path.exists():
        if glbs:
            rep.error("stale", "assets/gltf contains GLBs but assets/manifest.json is missing")
        else:
            rep.note("stale check: no baked assets yet")
        return
    manifest = json.loads(manifest_path.read_text())
    known = set(manifest.get("assets", {}))
    for g in glbs:
        if g.name not in known:
            rep.error("stale", f"assets/gltf/{g.name} is not in manifest.json — "
                               f"it was not produced by a tracked bake")
    rep.note(f"stale check: {len(glbs)} baked asset(s), manifest blender "
             f"{manifest.get('blender', '?')}")


def run_site_check(rep: Report) -> None:
    site = ROOT.parent.parent / "site" / "chicago" / "4d"
    if not site.exists():
        rep.note("site check: nothing published yet")
        return
    total = sum(p.stat().st_size for p in site.rglob("*") if p.is_file())
    mb = total / (1024 * 1024)
    if mb > SITE_BUDGET_MB:
        rep.error("site", f"published tree is {mb:.1f} MB, over the {SITE_BUDGET_MB} MB budget — "
                          f"GitHub Pages cannot serve Git LFS objects, so this has to stay lean")
    rep.note(f"site check: published tree {mb:.2f} MB of {SITE_BUDGET_MB} MB budget")
    # Only page directories need an index.html; asset and data directories are
    # fetched by explicit path and are never a bare URL a visitor lands on.
    def is_page_dir(d: Path) -> bool:
        rel = d.relative_to(site).as_posix()
        if rel.startswith(("data", "walk/vendor", "walk/js", "walk/css")):
            return False
        return any(p.suffix == ".html" for p in d.iterdir() if p.is_file()) or d == site

    for d in [site] + [p for p in site.rglob("*") if p.is_dir()]:
        if is_page_dir(d) and not (d / "index.html").exists():
            rep.warn("site", f"{d.relative_to(site.parent.parent)} is a page directory with "
                             f"no index.html — the bare URL will 404 on Pages")


if __name__ == "__main__":
    sys.exit(main())
