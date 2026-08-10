#!/usr/bin/env python3
"""Validate the 4D Chicago dataset.

Runs in seconds and needs no Blender. This is the per-commit gate.

    validate.py              schema + referential + semantic + scene date gates
    validate.py --params     also resolve every phase's form to archetype params
    validate.py --licenses   also check asset license coverage and rights gating
    validate.py --stale      also recompute every committed GLB's input hash
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
import math
import re
import sys
from pathlib import Path

from heightfield import Heightfield

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

# The record's fixed attested blocks, in the order a claim reads best. Everything
# else a liberty can be held to is under `form`, whose vocabulary is open and is
# enumerated from the data rather than listed here. Kept in step with
# tools/compile_liberties.py's COVER_ASPECTS.
PHASE_ASPECTS = ("footprint", "position", "documented_range")
STRUCTURE_ASPECTS = ("function", "occupants")


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
    # The confidence contract applied to the claim the whole scene rests on. Every
    # other `documented` value in this dataset owes a resolving source (see
    # check_attested); the date span was outside that rule for no reason but the
    # order the checks were written in, and it is the claim that decides whether a
    # building is in the town at all. It reaches the provenance card now, which is
    # the argument for holding it to the same standard as a roof pitch.
    if rng.get("confidence") == "documented" and not (rng.get("sources") or []):
        rep.error(where, "documented_range: documented requires at least one source_id")
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
        # The same disagreement in its second form, which no record can report
        # because the excluded structure has no record: an entry that dates a
        # building to 1837 is not an exclusion from an 1837 scene. Nothing here
        # is wrong at one year and becomes wrong later without saying so — this
        # project is year-parameterized, so the year has to be asked.
        earliest = str(ex.get("earliest_scene") or "")
        if earliest.isdigit() and int(earliest) <= target.year:
            rep.error(where, f"'{ex.get('id')}' is excluded, but its own earliest_scene "
                             f"({earliest}) is on or before this scene ({target.year}) — "
                             f"it belongs in the dataset here, or the entry is wrong")


def check_exclusions(exclusions: dict, source_ids: set, rep: Report) -> None:
    """The research record of what was left out is held to the citation rule.

    Every `source_id` in this project must resolve in `data/sources/` — rule one
    in AGENTS.md — and until this check, exclusions.json was the one file where
    it did not: nothing read its `sources` arrays, so a citation there could name
    a source that has never existed. That mattered least while the file was read
    only by agents and matters most now that the walkthrough quotes it: a visitor
    reading why the Saloon Building is not here is reading these ids joined to
    their citations.

    A reason is required for the same reason a `note` is required on an inferred
    value. "Left out" without a stated ground is not a finding, it is a deletion
    with a filename.
    """
    seen: set[str] = set()
    for ex in exclusions.get("excluded", []):
        eid = ex.get("id") or "?"
        where = f"exclusion {eid}"
        if not SLUG.match(eid):
            rep.error(where, f"id '{eid}' is not a lowercase slug")
        if eid in seen:
            rep.error(where, "duplicate id in exclusions.json")
        seen.add(eid)
        if not (ex.get("name") or "").strip():
            rep.error(where, "no name — the list is read by people, not only by ids")
        if not (ex.get("reason") or "").strip():
            rep.error(where, "no reason — an exclusion without a stated ground is a "
                             "deletion, and this file exists so that it is a finding")
        srcs = ex.get("sources") or []
        if not srcs:
            rep.error(where, "no sources — excluding a structure is a claim about the "
                             "evidence and carries a citation like any other")
        for s in srcs:
            if s not in source_ids:
                rep.error(where, f"source '{s}' does not resolve in data/sources/")


# Land vertices. The terrain spec's own caveat says no land elevation in it is
# better than `inferred` and that the generator refuses to emit `documented` for
# any land vertex — a statement that was true because whoever wrote the spec kept
# it true, and nothing was checking. These are the blocks that set the height of
# ground a visitor walks on; the reaches and the channel are under water.
LAND_ELEVATION_GROUPS = ("bank", "divisions", "marsh_strips", "swales", "micro_relief")


def load_terrain_specs(rep: Report) -> dict[str, dict]:
    """epoch -> its committed `terrain_spec.json`."""
    specs: dict[str, dict] = {}
    for spec_path in sorted((DATA / "terrain" / "epochs").glob("*/terrain_spec.json")):
        specs[spec_path.parent.name] = load_json(spec_path, rep) or {}
    return specs


def terrain_claim_index(specs: dict[str, dict], rep: Report) -> dict[str, dict[str, dict]]:
    """epoch -> claim id -> the graded statement the ground makes.

    Off `compile_scene.ground_claims`, which is also what puts these on the
    Evidence panel — so the set a gate checks, the set a liberty may admit to and
    the set a visitor reads are one set. A second enumeration would agree with
    the panel until the day somebody added a zone to the spec, which is the drift
    this project keeps closing everywhere else.
    """
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import compile_scene as ground  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001
        rep.error("terrain", f"cannot import the ground compiler, so the claims the "
                             f"Evidence panel shows cannot be checked: {e}")
        return {}
    return {epoch: {c["id"]: c for c in ground.ground_claims(spec, {})}
            for epoch, spec in sorted(specs.items())}


def terrain_conjectural_values(index: dict[str, dict[str, dict]]) -> list[tuple]:
    """Every value the ground states without evidence.

    Returns `(epoch, claim_id, label, where)`. The ground invents as freely as a
    record does — a bank face nobody drew, two swale alignments attested nowhere,
    a channel section whose own note says it carries no evidence at all — and a
    visitor walks on all of it. The confidence view even dithers it. So it owes
    `docs/LIBERTIES.md` an admission on exactly the argument a conjectural
    footprint does.
    """
    return [(epoch, cid, claim.get("label") or cid, f"terrain {epoch}/{cid}")
            for epoch, claims in sorted(index.items())
            for cid, claim in claims.items()
            if claim.get("confidence") == "conjectural"]


def check_terrain_claims(source_ids: set, rep: Report,
                         specs: dict[str, dict] | None = None,
                         index: dict[str, dict[str, dict]] | None = None) -> None:
    """The ground is held to the rules a structure record is held to.

    `terrain_spec.json` is as fully graded as any record — a documented water
    plane, three inferred division levels argued from period narrative feet, a
    conjectural bank face — and until the ground claims reached the Evidence
    panel it was read only by the generator, so none of it was ever checked.
    Both halves of that mattered: rule one of AGENTS.md is that every
    `source_id` resolves in `data/sources/`, and this was the second file after
    `exclusions.json` where nothing enforced it. A citation here could have named
    a source that never existed, and now a visitor reads these ids joined to
    their citations.

    The claims are enumerated by the same function that puts them on the panel
    (`compile_scene.ground_claims`), so the checked set and the displayed set are
    one set. A gate walking its own copy would agree with the panel until a zone
    was added to the spec.

    Three rules are enforced, all of them the record's rules:
      * every cited `source_id` resolves;
      * a `documented` claim owes at least one resolving source;
      * no land elevation may be `documented` — the spec says so itself, in the
        caveat the walkthrough now quotes to visitors.

    The fourth — `inferred` owes stated reasoning, which `check_attested` makes an
    error on a record — is a WARNING here, and the reason is worth stating rather
    than hiding in a severity constant. Three surface-material claims carry no
    note, so the rule is right and the data is short; but the only place to write
    those notes is `terrain_spec.json`, whose BYTES are hashed into the terrain's
    staleness, so adding a sentence of reasoning re-stales the ground and cannot
    land without a Blender bake. A warning that is correct and stands until
    someone fixes the data is this project's existing shape for that (the
    un-archived sources have carried one for weeks). The rule becomes an error in
    the slice that writes the notes and lands the bake with them.
    """
    if index is None:
        index = terrain_claim_index(specs if specs is not None else load_terrain_specs(rep), rep)

    total = unreasoned = 0
    for epoch, claims in sorted(index.items()):
        for claim in claims.values():
            total += 1
            where = f"terrain {epoch}/{claim['id']}"
            conf = claim["confidence"]
            if conf not in CONFIDENCE:
                rep.error(where, f"confidence '{conf}' is not one of {sorted(CONFIDENCE)}")
            srcs = claim["sources"]
            for s in srcs:
                if s not in source_ids:
                    rep.error(where, f"source '{s}' does not resolve in data/sources/ — "
                                     f"the ground quotes these ids to a visitor")
            if conf == "documented" and not srcs:
                rep.error(where, "documented with no source — the ground is held to the "
                                 "same rule as a structure record, and the strongest "
                                 "grade this project has is the one that needs evidence")
            if conf == "inferred" and not any(n.strip() for n in claim["notes"]):
                unreasoned += 1
                rep.warn(where, "inferred with no reasoning recorded — a record would "
                                "fail for this. The note has to go in terrain_spec.json, "
                                "whose bytes are the terrain's staleness hash, so writing "
                                "it re-stales the ground and lands with a bake; the "
                                "walkthrough says 'no reasoning is recorded' meanwhile")
            if conf == "documented" and claim["id"].split(".")[0] in LAND_ELEVATION_GROUPS:
                rep.error(where, "a land elevation marked documented — the spec's own "
                                 "caveat says no land elevation in it is better than "
                                 "inferred, and that sentence is now shown to visitors")

    rep.note(f"ground claims: {total} graded statement(s) in the terrain specs, held to "
             f"the citation rule and shown in the Evidence panel; {unreasoned} inferred "
             f"without recorded reasoning")


# --------------------------------------------------------------------------
# semantic: the liberties document is complete about what was invented
# --------------------------------------------------------------------------

def conjectural_values(structures: dict) -> list[tuple]:
    """Every value a structure record states without evidence.

    Returns `(structure_id, phase_id|None, aspect, where)`, with `aspect` in the
    same vocabulary a `Covers:` token is written in — `footprint`, `position`,
    `documented_range`, the structure-level `function` and `occupants`, and
    `form.<attribute>` for anything under a phase's form, however deeply nested.

    The form half is enumerated from the data rather than from a list, because
    the archetypes keep adding attributes and a hard-coded vocabulary would
    quietly stop asking about the newest ones — which is the exact failure this
    check exists to prevent, one level up.
    """
    found: list[tuple] = []

    def walk_form(node, sid: str, pid: str, where: str, path: str) -> None:
        if not isinstance(node, dict):
            return
        if "confidence" in node and "value" in node:
            if node.get("confidence") == "conjectural":
                found.append((sid, pid, path, where))
            return
        for k, v in node.items():
            walk_form(v, sid, pid, where, f"{path}.{k}")

    for name, st in sorted(structures.items()):
        sid = st.get("id", name)
        for aspect in STRUCTURE_ASPECTS:
            block = st.get(aspect)
            if isinstance(block, dict) and block.get("confidence") == "conjectural":
                found.append((sid, None, aspect, f"structure {sid}"))
        for ph in st.get("phases", []):
            pid = ph.get("id", "?")
            where = f"structure {sid}/{pid}"
            for aspect in PHASE_ASPECTS:
                block = ph.get(aspect)
                if isinstance(block, dict) and block.get("confidence") == "conjectural":
                    found.append((sid, pid, aspect, where))
            walk_form(ph.get("form") or {}, sid, pid, where, "form")
    return found


def archetype_consumed(rep: Report | None = None) -> dict[str, frozenset]:
    """archetype name -> the form attributes whose value its generator reads.

    Declared by each `generators/archetypes/*_params.py` as `CONSUMED`, next to
    the `from_phase` that does the reading, because the two drift apart the
    moment they live in different files. Imports only the pure-Python halves, so
    this costs milliseconds and needs no Blender.

    An archetype with no params module yet returns nothing and is skipped rather
    than assumed empty: "we have not written the generator" and "the generator
    ignores everything" are different states and only one of them is a finding.
    """
    out: dict[str, frozenset] = {}
    arch_dir = ROOT / "generators" / "archetypes"
    if not arch_dir.exists():
        return out
    sys.path.insert(0, str(ROOT / "generators"))
    for mod_path in sorted(arch_dir.glob("*_params.py")):
        name = mod_path.stem.removesuffix("_params")
        try:
            mod = __import__(f"archetypes.{mod_path.stem}", fromlist=["CONSUMED"])
        except Exception as e:  # noqa: BLE001
            if rep:
                rep.error("geometry", f"cannot import {mod_path.name}: {e}")
            continue
        consumed = getattr(mod, "CONSUMED", None)
        if consumed is None:
            if rep:
                rep.error("geometry", f"{mod_path.name} declares no CONSUMED set, so nothing "
                                      f"can tell which of a {name} record's attributes reach "
                                      f"the mesh and which are stated and never built")
            continue
        out[name] = frozenset(consumed)
    return out


# What a `geometry:` declaration may say, and whether saying it is an admission
# that owes the liberties document an entry. `record_only` does not: an attribute
# that is a research note rather than a build instruction — a rejected reading, a
# negative finding — has nothing missing from the model to admit to.
GEOMETRY_STATES = ("absent", "simplified", "record_only")
GEOMETRY_OWES_LIBERTY = ("absent", "simplified")


def unbuilt_values(structures: dict, consumed: dict[str, frozenset]) -> list[tuple]:
    """Every form attribute whose archetype does not read it.

    Returns `(structure_id, phase_id, aspect, where, attr_dict)` with `aspect` in
    the `Covers:` vocabulary — `form.<attribute>` — so an omission is claimed by
    the same grammar an invention is.

    Attributes whose value is falsy are excluded, and the exclusion is the whole
    difference between a gap and a nothing: `log_core: false` records a reading
    the project rejected, and there is no missing stable, sign or wing behind it
    to admit to. What is left is the set of things a record says the building had
    and the mesh cannot show.
    """
    found: list[tuple] = []
    for name, st in sorted(structures.items()):
        sid = st.get("id", name)
        known = consumed.get(st.get("archetype"))
        if known is None:
            continue
        for ph in st.get("phases", []):
            pid = ph.get("id", "?")
            for attr, a in sorted((ph.get("form") or {}).items()):
                if attr in known or not isinstance(a, dict):
                    continue
                found.append((sid, pid, f"form.{attr}", f"structure {sid}/{pid}", a))
    return found


def check_geometry_declarations(structures: dict, consumed: dict[str, frozenset],
                                rep: Report) -> None:
    """A record may not state something the mesh does not contain without saying so.

    The confidence model answers "how sure are we of this value". It has nothing
    to say about a value nobody builds — and the two are not the same claim at
    all. The Wolf Point Tavern's painted wolf sign is `documented`: the popup
    shows the strongest chip the project has, over a building that has no sign on
    it. That reads as a well-evidenced feature you are looking at, and it is a
    well-evidenced feature you are not.

    So the rule is mechanical and comes from the generator rather than from a
    reviewer's attention: every form attribute outside its archetype's `CONSUMED`
    set carries a `geometry:` declaration saying what the mesh does instead —
    `absent`, `simplified`, or `record_only` for something that was never a build
    instruction. The first two are omissions and simplifications, so they owe
    docs/LIBERTIES.md an entry, which `check_liberties_coverage` collects.

    The declaration is checked the other way too. Putting `geometry:` on an
    attribute the archetype *does* read is a false admission — the value drives
    the mesh by construction — and it would quietly excuse a real omission if the
    parameter were ever removed.
    """
    if not consumed:
        rep.note("geometry check: no archetype params modules to compare against")
        return
    declared = 0
    for name, st in sorted(structures.items()):
        sid = st.get("id", name)
        known = consumed.get(st.get("archetype"))
        if known is None:
            continue
        for ph in st.get("phases", []):
            pid = ph.get("id", "?")
            where = f"structure {sid}/{pid}"
            for attr, a in sorted((ph.get("form") or {}).items()):
                if not isinstance(a, dict):
                    continue
                state = a.get("geometry")
                if attr in known:
                    if state is not None:
                        rep.error(where, f"form.{attr} carries geometry: '{state}', but the "
                                         f"{st.get('archetype')} archetype reads this attribute "
                                         f"— it is built from the value, so there is nothing to "
                                         f"declare. Drop the field, or remove the attribute from "
                                         f"CONSUMED if the generator stopped using it")
                    continue
                if state is None:
                    rep.error(where, f"form.{attr} is stated by the record and the "
                                     f"{st.get('archetype')} archetype never reads it, so "
                                     f"nothing in the mesh comes from it — and the popup still "
                                     f"shows the value with a confidence chip. Declare what the "
                                     f"geometry does: geometry: 'absent' (nothing of it is "
                                     f"built), 'simplified' (a fixed default stands in its "
                                     f"place), or 'record_only' (a reading recorded, not a "
                                     f"build instruction)")
                    continue
                if state not in GEOMETRY_STATES:
                    rep.error(where, f"form.{attr} declares geometry: '{state}', which is not "
                                     f"one of {', '.join(GEOMETRY_STATES)}")
                    continue
                if state in GEOMETRY_OWES_LIBERTY and not a.get("value"):
                    rep.error(where, f"form.{attr} declares geometry: '{state}' over the value "
                                     f"{a.get('value')!r} — admitting to leaving out something "
                                     f"the record says was not there. Use 'record_only' for a "
                                     f"reading recorded rather than a thing omitted")
                    continue
                declared += 1
    rep.note(f"geometry check: {declared} attribute(s) the archetypes do not read, each "
             f"declaring what the mesh does instead")


# How far a structure's ground contact may sit off the terrain under it before
# the record has to say so. The number is not a fresh tolerance: it is the
# walker's step-up rule from renderers/web/js/walker.js — "a little over a foot,
# which is what a plank walk stands above the mud and what a person steps onto
# without thinking". The question this gate asks IS that question. Anything a
# visitor could step onto has met the ground; anything they could not has not.
GROUND_CONTACT_TOL_M = 0.35

# What a phase may say when its structure does not reach the ground. One state
# so far, and it is deliberately narrow: the model stops at the structure and
# the ground it needed to arrive at is not built. A second state would need its
# own argument.
GROUND_CONTACT_STATES = ("approach_not_modelled",)


def archetype_ground_contact(rep: Report | None = None) -> dict[str, dict]:
    """archetype -> {mode, anchor}, declared beside the generator that builds it.

    `GROUND_CONTACT` is `perimeter` (the footprint outline meets the terrain at
    the base of the walls) or `ends` (only the end edges of the footprint meet
    it, at the params object's `ground_contact_z`). An archetype that declares
    nothing is skipped, not assumed — the same rule `archetype_consumed` uses,
    for the same reason.
    """
    out: dict[str, dict] = {}
    arch_dir = ROOT / "generators" / "archetypes"
    if not arch_dir.exists():
        return out
    sys.path.insert(0, str(ROOT / "generators"))
    for mod_path in sorted(arch_dir.glob("*_params.py")):
        name = mod_path.stem.removesuffix("_params")
        try:
            mod = __import__(f"archetypes.{mod_path.stem}", fromlist=["GROUND_CONTACT"])
        except Exception:  # noqa: BLE001 — archetype_consumed already reported it
            continue
        mode = getattr(mod, "GROUND_CONTACT", None)
        if mode is None:
            continue
        if mode not in ("perimeter", "ends"):
            if rep:
                rep.error("ground contact", f"{mod_path.name} declares GROUND_CONTACT "
                                            f"'{mode}', which is not perimeter or ends")
            continue
        if mode == "ends" and not callable(getattr(mod, "ground_contact_z", None)):
            if rep:
                rep.error("ground contact", f"{mod_path.name} declares GROUND_CONTACT 'ends' "
                                            f"but no ground_contact_z(params) to say at what "
                                            f"height those ends arrive")
            continue
        out[name] = {"mode": mode,
                     "anchor": getattr(mod, "VERTICAL_ANCHOR", None),
                     "contact_z": getattr(mod, "ground_contact_z", None)}
    return out


def _resample(a: tuple, b: tuple, step: float = 1.0) -> list[tuple]:
    """Points along a segment, no farther apart than `step`, ends included."""
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    n = max(1, int(math.ceil(d / step)))
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]


def _contact_outline(poly: list, mode: str) -> list[tuple]:
    """The footprint edges, in local (u, v), where this archetype meets the ground.

    `perimeter` is the whole outline. `ends` is the two edges at the extremes of
    u — the span axis — which for a crossing is where the deck arrives at land
    and everything between is over water by construction.
    """
    edges = [(tuple(poly[i]), tuple(poly[(i + 1) % len(poly)])) for i in range(len(poly))]
    if mode == "perimeter":
        return edges
    us = [p[0] for p in poly]
    lo, hi = min(us), max(us)
    return [(a, b) for a, b in edges
            if (abs(a[0] - lo) < 1e-6 and abs(b[0] - lo) < 1e-6)
            or (abs(a[0] - hi) < 1e-6 and abs(b[0] - hi) < 1e-6)]


def unlanded_values(structures: dict, scenes: dict, rep: Report,
                    field=None, origin: tuple | None = None,
                    contacts: dict | None = None,
                    resolvers: dict | None = None) -> list[tuple]:
    """Every structure whose ground contact does not reach the ground.

    Returns `(structure_id, phase_id, "ground_contact", where, gap_m)`.

    The confidence model grades what a value claims; the geometry declarations
    grade whether a value was built. Neither can see a structure that WAS built,
    faithfully, onto ground that is not underneath it — because nothing in the
    record is wrong. The Wolf Point Tavern's `frame_extension` was a name the
    archetype could not find; this is the class where every name resolves and the
    result still stands in the air.

    Measured against the raw heightfield, not the renderer's walkable surface:
    `terrain.js` reports a wading barrier at +4 m over water so a walker cannot
    stroll into the river, and measuring a bridge against that barrier would be
    measuring it against a navigation rule.
    """
    found: list[tuple] = []
    if field is None or origin is None or not contacts:
        return found
    o_e, o_n = origin
    if resolvers is None:
        resolvers = {}
        sys.path.insert(0, str(ROOT / "generators"))
        for mod_path in sorted((ROOT / "generators" / "archetypes").glob("*_params.py")):
            try:
                mod = __import__(f"archetypes.{mod_path.stem}", fromlist=["from_phase"])
                resolvers[mod_path.stem.removesuffix("_params")] = mod.from_phase
            except Exception:  # noqa: BLE001 — reported by the param check
                continue

    targets = [d for d in (parse_date(sc.get("target_date", "")) for sc in scenes.values()) if d]
    for name, st in sorted(structures.items()):
        sid = st.get("id", name)
        arch = st.get("archetype")
        decl = contacts.get(arch)
        if decl is None or arch not in resolvers:
            continue
        for ph in st.get("phases", []):
            pid = ph.get("id", "?")
            r = ph.get("documented_range", {})
            frm, to = parse_date(r.get("from", "")), parse_date(r.get("to", ""))
            if not (frm and to and any(frm <= t <= to for t in targets)):
                continue
            pos = ph.get("position") or {}
            poly = (ph.get("footprint") or {}).get("polygon")
            if not isinstance(poly, list) or len(poly) < 3:
                continue
            if pos.get("utm_e") is None or pos.get("utm_n") is None:
                continue
            try:
                params = resolvers[arch](ph)
            except Exception:  # noqa: BLE001 — reported by the param check
                continue

            e0 = float(pos["utm_e"]) - o_e
            n0 = float(pos["utm_n"]) - o_n
            th = math.radians(float(pos.get("rotation_deg") or 0.0))
            cos, sin = math.cos(th), math.sin(th)

            def to_world(p, e0=e0, n0=n0, cos=cos, sin=sin):
                u, v = float(p[0]), float(p[1])
                return (e0 + u * cos + v * sin, n0 - u * sin + v * cos)

            base_y = 0.0 if decl["anchor"] == "water" else field.height(e0, n0)
            contact_z = 0.0 if decl["mode"] == "perimeter" else float(decl["contact_z"](params))
            contact_y = base_y + contact_z

            worst = 0.0
            for a, b in _contact_outline(poly, decl["mode"]):
                for e, n in _resample(to_world(a), to_world(b)):
                    gap = contact_y - field.height(e, n)
                    if abs(gap) > abs(worst):
                        worst = gap
            if abs(worst) > GROUND_CONTACT_TOL_M:
                found.append((sid, pid, "ground_contact", f"structure {sid}/{pid}", worst))
    return found


def check_ground_contact(structures: dict, unlanded: list[tuple], rep: Report) -> None:
    """A structure that does not reach the ground has to say so on the record.

    Checked in both directions, like the geometry declarations: a structure that
    stands clear of the terrain and admits nothing is an unrecorded liberty, and
    a structure that admits to one while sitting flat on the ground is an
    admission to something we did not do.
    """
    gapped = {(sid, pid): gap for sid, pid, _, _, gap in unlanded}
    declared = 0
    for name, st in sorted(structures.items()):
        sid = st.get("id", name)
        for ph in st.get("phases", []):
            pid = ph.get("id", "?")
            where = f"structure {sid}/{pid}"
            block = ph.get("ground_contact")
            gap = gapped.get((sid, pid))
            if block is not None and not isinstance(block, dict):
                rep.error(where, "ground_contact must be an object with a state and a note")
                continue
            state = (block or {}).get("state")
            if gap is None:
                if block is not None:
                    rep.error(where, f"declares ground_contact: '{state}', but its contact "
                                     f"outline sits within {GROUND_CONTACT_TOL_M} m of the "
                                     f"terrain under it — it lands. Drop the declaration, or "
                                     f"move the entry claiming it to the Resolved section of "
                                     f"docs/LIBERTIES.md if the ground caught up")
                continue
            if block is None:
                rep.error(where, f"its ground contact stands {gap:+.2f} m off the terrain "
                                 f"beneath it — more than the walker's {GROUND_CONTACT_TOL_M} m "
                                 f"step-up rule, so a visitor could not step between the two. "
                                 f"Nothing in the record is wrong and nothing shows it: declare "
                                 f"ground_contact: {{state: 'approach_not_modelled', note: ...}} "
                                 f"on the phase and admit it in docs/LIBERTIES.md")
                continue
            if state not in GROUND_CONTACT_STATES:
                rep.error(where, f"ground_contact state '{state}' is not one of "
                                 f"{', '.join(GROUND_CONTACT_STATES)}")
                continue
            if not (block.get("note") or "").strip():
                rep.error(where, "ground_contact declares a state with no note — the note is "
                                 "where the reasoning lives, exactly as it is for an inferred "
                                 "value")
                continue
            declared += 1
    rep.note(f"ground contact: {len(gapped)} structure(s) do not reach the terrain under them, "
             f"{declared} declaring it")


def check_liberties_coverage(structures: dict, liberties: dict, rep: Report,
                             consumed: dict[str, frozenset] | None = None,
                             unlanded: list[tuple] | None = None,
                             ground: dict[str, dict[str, dict]] | None = None) -> None:
    """Every conjectural value in a record must be CLAIMED in LIBERTIES.md.

    This is the inverse of the check the walkthrough already makes. The panel and
    the provenance card report the liberties that were *recorded* — which is not
    the claim that everything taken was written down, and the project's standard
    is that a visitor can tell you which parts we made up. A conjectural footprint
    is not merely an unknown: the polygon gets drawn, the building stands on it,
    and the visitor sees one specific shape. That is an invention, and an
    invention nobody wrote down is exactly the gap the standard is about.

    The same argument runs past the drawn geometry, which is why the requirement
    now covers every attested value in the record. A conjectural `roof_type` is
    not an absence in the model: a gable gets built, and the visitor sees a gable.
    A conjectural `gallery: false` is the same claim in the negative — the front
    of the building is rendered plain because nobody found evidence either way,
    and *that* is a decision a visitor cannot recover from a dithered tint. The
    confidence chip says "we do not know"; only the liberty says what we did about
    not knowing.

    So the confidence value drives the requirement, mechanically: mark anything
    conjectural and the gate demands an entry whose `Covers:` field names that
    structure and that aspect. The claim is DECLARED, not inferred from the
    entry's wording. Reading the prose — the earlier rule — meant a liberty could
    discharge a footprint by mentioning the word while discussing a gallery, which
    is a coverage check that can be satisfied by an accident of phrasing.

    The claims are checked the other way too. A `Covers:` token that names no such
    structure, no such phase, or an attribute that is not conjectural is an
    over-claim: the document says it admitted to something it did not, and that
    reads as diligence while providing none. Entries under **Resolved** are exempt
    from the last of those, because an append-only document has to be able to say
    "evidence settled this" without the settlement itself becoming a gate failure.

    **And the ground answers to all of it too.** Every paragraph above is about a
    building, because the check read `data/structures/` and nothing else. The
    terrain invents on the same terms and at a larger scale — a 6 m bank face
    nobody recorded, on every bank in the box, which is the piece of ground every
    visitor walks down to the water on — and none of that was demanded by a
    check: L32 and L33 were written by a person who noticed. A liberty owed by
    somebody's attention is precisely the arrangement this gate exists to
    replace. Ground claims are enumerated by the same function that puts them on
    the Evidence panel and claimed in a namespace of their own,
    `terrain.<epoch>.<claim>`, because the terrain is not a structure and the one
    document whose subject is honesty should not have to call it one.
    """
    entries = liberties.get("liberties") if isinstance(liberties, dict) else None
    if not entries:
        rep.error("liberties", "data/liberties.json holds no entries, so the values "
                               "invented in data/structures/ cannot be checked against "
                               "docs/LIBERTIES.md — run tools/compile_liberties.py")
        return

    # (structure, phase|None, aspect) -> the entries claiming it, and the ground's
    # (epoch, claim) beside it. Two dicts rather than one keyspace with a marker
    # in it: the two domains are checked against different documents and fail for
    # different reasons, and a shared key would only make that harder to read.
    claims: dict[tuple, list[dict]] = {}
    ground_claims_made: dict[tuple, list[dict]] = {}
    for e in entries:
        for c in e.get("covers") or []:
            if c.get("domain") == "terrain":
                ground_claims_made.setdefault((c.get("epoch"), c.get("claim")), []).append(e)
                continue
            key = (c.get("structure"), c.get("phase"), c.get("aspect"))
            claims.setdefault(key, []).append(e)

    by_subject: dict[str, list[dict]] = {}
    for e in entries:
        for sid in e.get("subjects") or []:
            by_subject.setdefault(sid, []).append(e)

    # Two kinds of thing owe the document an entry, and they are opposites: a
    # value invented to fill a gap, and a value we have but did not build.
    owed: list[tuple] = [(sid, pid, aspect, where, "invented")
                         for sid, pid, aspect, where in conjectural_values(structures)]
    for sid, pid, aspect, where, attr in unbuilt_values(structures, consumed or {}):
        state = attr.get("geometry")
        if state in GEOMETRY_OWES_LIBERTY and attr.get("value"):
            owed.append((sid, pid, aspect, where, state))
    # And a third: a structure built faithfully onto ground that is not under it.
    for sid, pid, aspect, where, _gap in (unlanded or []):
        owed.append((sid, pid, aspect, where, "unlanded"))

    covered = 0
    invented = omitted = unlanded_n = ground_n = 0
    honoured: set[tuple] = set()
    for sid, pid, aspect, where, kind in owed:
        keys = [(sid, pid, aspect), (sid, None, aspect)]
        hit = [k for k in keys if k in claims]
        if hit:
            covered += 1
            invented += kind == "invented"
            unlanded_n += kind == "unlanded"
            omitted += kind not in ("invented", "unlanded")
            honoured.update(hit)
            continue
        named = ", ".join(e.get("id", "?") for e in by_subject.get(sid, [])) or "none"
        token = ".".join(t for t in (sid, pid, aspect) if t)
        if kind == "invented":
            # A drawn shape and a stated attribute are invented in different ways, and
            # the message says which one the reader is looking at.
            what = (f"a drawn {aspect}" if aspect in ("footprint", "position")
                    else "a stated " + re.sub(r"\bm\b", "(m)",
                                              aspect.split(".")[-1].replace("_", " ")))
            why = (f"{aspect} is conjectural but no liberty in docs/LIBERTIES.md "
                   f"claims it — {what} nobody can defend is something we made up")
        elif kind == "unlanded":
            why = ("this structure does not reach the ground it stands over and no "
                   "liberty in docs/LIBERTIES.md claims it — the record is right, the "
                   "mesh is right, and the model still shows a thing arriving nowhere")
        else:
            why = (f"{aspect} declares geometry: '{kind}' but no liberty in "
                   f"docs/LIBERTIES.md claims it — the record states something the "
                   f"model does not show, which a confidence chip cannot say and a "
                   f"visitor cannot see")
        rep.error(where,
                  f"{why}, and the standard is that a visitor can tell you which parts. "
                  f"Append the liberty with '**Covers:** `{token}`' and re-run "
                  f"tools/compile_liberties.py (liberties naming {sid}: {named})")

    # The ground, on the same terms. Its claims are blocks of a spec rather than
    # attributes of a record, so they are matched by id and not by aspect — but
    # the requirement is the identical one, and so is the argument for it.
    ground = ground or {}
    ground_honoured: set[tuple] = set()
    ground_owed = terrain_conjectural_values(ground)
    for epoch, cid, label, where in ground_owed:
        key = (epoch, cid)
        if key in ground_claims_made:
            covered += 1
            ground_n += 1
            ground_honoured.add(key)
            continue
        rep.error(where,
                  f"'{label}' is conjectural and no liberty in docs/LIBERTIES.md claims "
                  f"it — the ground invents as freely as a record does, a visitor walks "
                  f"on the result, and the standard is that they can tell you which parts. "
                  f"Append the liberty with '**Covers:** `terrain.{epoch}.{cid}`' and "
                  f"re-run tools/compile_liberties.py")

    for (epoch, cid), owners in sorted(ground_claims_made.items(), key=lambda kv: str(kv[0])):
        who = ", ".join(e.get("id", "?") for e in owners)
        if epoch not in ground:
            rep.error("liberties", f"{who} claims to cover 'terrain.{epoch}.{cid}' but no "
                                   f"terrain epoch '{epoch}' is committed — an admission "
                                   f"about ground that does not exist")
            continue
        if cid not in ground[epoch]:
            rep.error("liberties", f"{who} claims to cover 'terrain.{epoch}.{cid}' but that "
                                   f"epoch's spec makes no graded claim '{cid}' — the claims "
                                   f"are the ones the Evidence panel shows, so a token "
                                   f"naming none of them admits to nothing a visitor reads")
            continue
        if (epoch, cid) in ground_honoured:
            continue
        if all((e.get("section") or "") == "resolved" for e in owners):
            continue
        rep.error("liberties", f"{who} claims to cover 'terrain.{epoch}.{cid}', but that "
                               f"ground claim is not conjectural — either evidence arrived "
                               f"and the spec caught up, in which case move the entry to the "
                               f"Resolved section of docs/LIBERTIES.md, or the claim was "
                               f"never true. An admission to something we did not do reads "
                               f"as diligence and provides none")

    # The claims answer for themselves.
    for (csid, cpid, aspect), owners in sorted(claims.items(), key=lambda kv: str(kv[0])):
        who = ", ".join(e.get("id", "?") for e in owners)
        st = next((s for s in structures.values() if s.get("id") == csid), None)
        if st is None:
            rep.error("liberties", f"{who} claims to cover '{csid}.{aspect}' but no structure "
                                   f"record has id '{csid}' — a liberty admitting to an "
                                   f"invention in a building that does not exist")
            continue
        if cpid is not None and cpid not in [p.get("id") for p in st.get("phases", [])]:
            rep.error("liberties", f"{who} claims to cover '{csid}.{cpid}.{aspect}' but "
                                   f"'{csid}' has no phase '{cpid}'")
            continue
        if (csid, cpid, aspect) in honoured:
            continue
        if all((e.get("section") or "") == "resolved" for e in owners):
            continue
        rep.error("liberties", f"{who} claims to cover '{csid}"
                               f"{'.' + cpid if cpid else ''}.{aspect}', but that value is "
                               f"neither conjectural, nor declared absent or simplified, nor "
                               f"standing off the ground — either "
                               f"the evidence arrived and the model caught up, in which case "
                               f"move the entry to the Resolved section of docs/LIBERTIES.md, or "
                               f"the claim was never true. An admission to something we did not "
                               f"do reads as diligence and provides none")

    rep.note(f"liberties coverage: {covered} value(s) owed an admission — {invented} invented, "
             f"{omitted} stated and not built, {unlanded_n} standing off the ground, "
             f"{ground_n} invented in the ground itself — claimed by "
             f"{len(honoured) + len(ground_honoured)} declaration(s) in docs/LIBERTIES.md")


# --------------------------------------------------------------------------
# the sidecar interface
# --------------------------------------------------------------------------
#
# `tools/compile_scene.py` writes the sidecars and the renderer reads them, and
# until now nothing stated what passes between them. That is not a hypothetical
# gap: `popup.js` read `sidecar.documented_range` from the day the card was
# written and the compiler never emitted it, so the one line answering *was this
# building here on 1 July 1835* rendered as nothing for the life of the project
# (STATUS § 28). Every existing gate was silent, and correctly so — each half was
# consistent with itself, `--check` proves only that the compiler agrees with its
# own output, and the record validated clean.
#
# So the interface is derived from both sides and compared. What the compiler
# emits is read off the committed sidecars, which `compile_scene.py --check`
# proves are exactly what the dataset compiles to; what the renderer reads is
# scanned out of the renderer's own source. A field read on one side and absent
# on the other is an error.

# `record.sidecar`, or the bare `sidecar` the loader binds when it fetches one.
SIDECAR_ROOT = r"(?:\brecord\b\s*\??\.\s*)?\bsidecar\b"
JS_IDENT = r"[A-Za-z_$][\w$]*"
JS_CHAIN = r"((?:\s*\??\.\s*[A-Za-z_$][\w$]*)*)"


def sidecar_shape() -> dict:
    """The shape of a per-structure sidecar, unioned over every committed one.

    A union rather than one file because a field is part of the interface even
    when only one structure carries it — `aka` is empty on most records and the
    card still reads it. The set is taken from each scene's `index.json` rather
    than from every file in the directory, because the other derived documents —
    `exclusions.json`, `terrain.json` — have their own readers and their own
    shapes, and a name-exclusion list stops being right the moment somebody
    compiles a third one. This gate covers the record the popup, the walker and
    the placement code all read.

    Dict values recurse; anything else becomes a leaf. Resolution stops at a
    leaf, which is what keeps `aka.length` and `polygon.map` from being read as
    missing fields of a list.
    """
    def merge(shape: dict, doc: dict) -> dict:
        for k, v in doc.items():
            if isinstance(v, dict):
                prev = shape.get(k)
                shape[k] = merge(prev if isinstance(prev, dict) else {}, v)
            else:
                shape.setdefault(k, None)
        return shape

    shape: dict = {}
    for index in sorted((DATA / "sidecars").glob("*/index.json")):
        listed = json.loads(index.read_text()).get("structures", [])
        for entry in listed:
            p = DATA / entry.get("sidecar", "")
            if not p.is_file():
                continue
            doc = json.loads(p.read_text())
            if isinstance(doc, dict):
                merge(shape, doc)
    return shape


def strip_js_comments(text: str) -> str:
    """Comments out, line numbers intact.

    Not cosmetic: this file's modules explain their own history in prose, and the
    first thing the gate reported was a field named in the comment that documents
    why it is no longer read. A sentence about a field is not a read of it.

    Block comments collapse to their own newlines so a reported line still points
    at the right line. The line-comment rule refuses a `//` preceded by a colon or
    a quote, which is what keeps a URL inside a string from truncating the code
    after it; the cost of the heuristic is a missed read on such a line, never a
    false one.
    """
    text = re.sub(r"/\*[\s\S]*?\*/", lambda m: "\n" * m.group(0).count("\n"), text)
    return re.sub(r"""(?<![:'"\\\w])//[^\n]*""", "", text)


def sidecar_field_reads(text: str, shape: dict | None = None) -> list[tuple[int, str]]:
    """Every sidecar field one renderer module reads, as (line, dotted path).

    A regex over JavaScript is a blunt instrument and this one is deliberately
    narrow: it follows `record.sidecar` and the local names bound directly to it
    (`const s = record.sidecar`, `const p = s.placement ?? {}`), and nothing
    else. A name is only followed when its path lands on a dict, so `const e =
    p.local_e` binds nothing further and a later unrelated `e` in the same file
    cannot be mistaken for it.

    What it cannot see is stated rather than implied: a sidecar value handed to a
    function is read through that function's parameter, so `claimRow(label, span,
    range)` puts `range.confidence` out of reach. This finds the reads that name
    the field where the sidecar is in hand, which is where the field name is
    chosen and therefore where it can be wrong.

    Where it errs it errs loudly. Bind a name to a sidecar block and then reuse
    that name for an unrelated object in the same module, and this attributes the
    second object's fields to the sidecar and reports them missing. That is a
    false alarm a reader resolves in a minute by renaming the variable, and it is
    the direction to fail in: the alternative is the silence that let a card read
    a field nobody wrote for the life of the project.
    """
    shape = sidecar_shape() if shape is None else shape
    text = strip_js_comments(text)

    def resolve(path: list[str]):
        """(node, ok, missing_segment) — resolution stops at the first leaf."""
        node = shape
        for i, seg in enumerate(path):
            if not isinstance(node, dict):
                return node, True, None, path[:i]
            if seg not in node:
                return None, False, seg, path[:i + 1]
            node = node[seg]
        return node, True, None, path

    def segments(chain: str) -> list[str]:
        return re.findall(JS_IDENT, chain or "")

    bound: dict[str, list[str]] = {}
    for _ in range(3):          # `s` binds before `p = s.placement` resolves
        anchors = [(SIDECAR_ROOT, [])] + [(r"\b%s\b" % re.escape(n), p)
                                          for n, p in bound.items()]
        for anchor, prefix in anchors:
            pat = r"\b(?:const|let|var)\s+(%s)\s*=\s*%s%s" % (JS_IDENT, anchor, JS_CHAIN)
            for m in re.finditer(pat, text):
                name, path = m.group(1), prefix + segments(m.group(2))
                node, ok, _, _ = resolve(path)
                if name not in bound and ok and isinstance(node, dict):
                    bound[name] = path

    reads: dict[str, int] = {}
    anchors = [(SIDECAR_ROOT, [])] + [(r"\b%s\b" % re.escape(n), p)
                                      for n, p in bound.items()]
    for anchor, prefix in anchors:
        for m in re.finditer(anchor + JS_CHAIN, text):
            path = prefix + segments(m.group(1))
            if not path:
                continue
            _, _, _, reached = resolve(path)
            key = ".".join(reached)
            line = text[:m.start()].count("\n") + 1
            if key and reads.get(key, 1 << 30) > line:
                reads[key] = line
    return sorted((line, path) for path, line in reads.items())


def check_sidecar_contract(rep: Report) -> None:
    """Every sidecar field the renderer reads must be one the compiler writes."""
    shape = sidecar_shape()
    if not shape:
        rep.note("sidecar contract: skipped — no committed sidecars to read the shape from")
        return

    js = sorted(p for p in (ROOT / "renderers").rglob("*.js") if "vendor" not in p.parts)
    read_paths: set[str] = set()
    files_reading = 0
    for path in js:
        reads = sidecar_field_reads(path.read_text(), shape)
        if reads:
            files_reading += 1
        for line, dotted in reads:
            read_paths.add(dotted)
            node = shape
            for seg in dotted.split("."):
                if not isinstance(node, dict):
                    break
                if seg not in node:
                    rep.error("sidecar contract",
                              f"{path.relative_to(ROOT)}:{line} reads `{dotted}` and no "
                              f"committed sidecar carries it — the renderer would read "
                              f"undefined on every building, silently, forever. Either "
                              f"tools/compile_scene.py emits the field or the renderer "
                              f"stops asking for it")
                    break
                node = node[seg]

    # A scanner that matched nothing would pass every renderer ever written, so
    # it reports what it found and the floor it is holding itself to.
    if read_paths and files_reading < 2:
        rep.error("sidecar contract",
                  f"only {files_reading} renderer module reads a sidecar — the scan has "
                  f"probably stopped matching; check sidecar_field_reads")
    rep.note(f"sidecar contract: {len(read_paths)} field(s) read across {files_reading} "
             f"renderer module(s), all present in the compiled sidecars")

    # The other direction is reported and not enforced, because the scan cannot
    # follow a value into a function: `documented_range` is read field by field
    # inside the row renderer it is passed to. At the top level that limit does
    # not bite, so an unread root key is a real finding — something the compiler
    # writes for a visitor who never sees it.
    unread = sorted(k for k in shape if k not in {p.split(".")[0] for p in read_paths})
    if unread:
        rep.note(f"sidecar contract: {len(unread)} top-level field(s) compiled and never "
                 f"read by the renderer ({', '.join(unread)}) — dead weight or an "
                 f"unshipped claim, not an error either way")


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
    liberties = load_json(DATA / "liberties.json", rep) or {}

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

    # what was researched and left out — a record with the same citation rule as
    # anything else here, and now one the walkthrough quotes to a visitor
    check_exclusions(exclusions, source_ids, rep)

    # and the ground itself, which makes graded claims like everything else here
    # and was checked by nothing until it started making them to a visitor. One
    # enumeration serves this check and the coverage gate below, so the ground
    # cannot be graded against one list and admitted to against another.
    ground_index = terrain_claim_index(load_terrain_specs(rep), rep)
    check_terrain_claims(source_ids, rep, index=ground_index)

    # scenes
    for name, sc in scenes.items():
        validate_scene(sc, structures, epochs, exclusions, rep)

    # what we invented has to be written down, not merely tagged — and so does
    # what we recorded and never built, which is the same standard read backwards
    consumed = archetype_consumed(rep)
    check_geometry_declarations(structures, consumed, rep)

    # Does each structure reach the ground it stands over? Needs the committed
    # heightfield and the datum origin; without either the question cannot be
    # asked, and a gate that silently answers "yes" when it cannot see is worse
    # than one that says it did not run.
    contacts = archetype_ground_contact(rep)
    epoch_ids = {sc.get("terrain_epoch") for sc in scenes.values() if sc.get("terrain_epoch")}
    field = None
    for ep in sorted(i for i in epoch_ids if i):
        try:
            field = Heightfield.load(DATA / "terrain" / "epochs" / ep)
        except Exception as e:  # noqa: BLE001
            rep.error("ground contact", f"cannot read the {ep} heightfield: {e}")
        if field is not None:
            break
    datum_origin = None
    if datum.get("origin_utm_e") is not None and datum.get("origin_utm_n") is not None:
        datum_origin = (float(datum["origin_utm_e"]), float(datum["origin_utm_n"]))
    unlanded: list[tuple] = []
    if field is None or datum_origin is None or not contacts:
        rep.note("ground contact: skipped — needs a committed heightfield, a datum origin "
                 "and at least one archetype declaring GROUND_CONTACT")
    else:
        unlanded = unlanded_values(structures, scenes, rep, field, datum_origin, contacts)
        check_ground_contact(structures, unlanded, rep)

    check_liberties_coverage(structures, liberties, rep, consumed, unlanded, ground_index)

    # what passes between the compiler and the renderer, checked from both sides
    check_sidecar_contract(rep)

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
        run_stale_check(structures, rep)
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


def run_stale_check(structures: dict, rep: Report) -> None:
    """Does every committed GLB still match the inputs that made it?

    Until 2026-08-10 this function only asked whether each GLB appeared in
    `assets/manifest.json`. The manifest has recorded an `inputs_sha256` per asset
    since the first bake and nothing ever recomputed it, so "a stale committed GLB
    is a check failure, not a warning" (AGENTS.md) was a sentence, not a gate: a
    record could be edited into a different building and the town would keep
    rendering the old one, green.

    The recipe lives with the generators — `generators/mesh_inputs.py` for
    structures, `terrain_gen.terrain_inputs_sha` for the ground — so the bake that
    writes the hash and the gate that checks it cannot drift apart.
    """
    manifest_path = ROOT / "assets" / "manifest.json"
    gltf_dir = ROOT / "assets" / "gltf"
    glbs = sorted(gltf_dir.glob("*.glb"))
    if not manifest_path.exists():
        if glbs:
            rep.error("stale", "assets/gltf contains GLBs but assets/manifest.json is missing")
        else:
            rep.note("stale check: no baked assets yet")
        return

    manifest = json.loads(manifest_path.read_text())
    assets = manifest.get("assets", {})
    for g in glbs:
        if g.name not in assets:
            rep.error("stale", f"assets/gltf/{g.name} is not in manifest.json — "
                               f"it was not produced by a tracked bake")

    sys.path.insert(0, str(ROOT / "generators"))
    try:
        import mesh_inputs  # noqa: PLC0415
        import terrain_gen  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001
        rep.error("stale", f"cannot import the generators' input-hash recipe, so no committed "
                           f"asset can be checked against its inputs: {e}")
        return

    scheme = manifest.get("inputs_scheme")
    if scheme != mesh_inputs.SCHEME:
        rep.error("stale", f"manifest inputs_scheme is {scheme!r} but the generators compute "
                           f"{mesh_inputs.SCHEME!r} — the two sides are hashing different things, "
                           f"so every comparison below would be meaningless. Re-stamp the manifest "
                           f"(and say in the commit why the definition changed)")
        return

    by_id = {st.get("id"): st for st in structures.values() if isinstance(st, dict)}
    fresh, stale, unchecked = 0, 0, 0

    for name, entry in sorted(assets.items()):
        if not (gltf_dir / name).exists():
            rep.error("stale", f"manifest.json lists {name} but assets/gltf/{name} does not "
                               f"exist — the record of a bake outlived its output")
            continue
        recorded = entry.get("inputs_sha256")
        if not recorded:
            rep.error("stale", f"{name} has no inputs_sha256, so nothing can say whether it "
                               f"still matches the data it was built from")
            continue
        try:
            if entry.get("structure_id"):
                st = by_id.get(entry["structure_id"])
                if st is None:
                    rep.error("stale", f"{name} was built from structure "
                                       f"'{entry['structure_id']}', which no longer exists in "
                                       f"data/structures — a mesh with no record behind it")
                    continue
                phase = next((p for p in st.get("phases", [])
                              if p.get("id") == entry.get("phase_id")), None)
                if phase is None:
                    rep.error("stale", f"{name} was built from phase '{entry.get('phase_id')}' "
                                       f"of {entry['structure_id']}, which the record no longer "
                                       f"has")
                    continue
                got = mesh_inputs.structure_inputs_sha(st, phase, entry.get("archetype"))
            elif entry.get("terrain_epoch"):
                ep_dir = DATA / "terrain" / "epochs" / entry["terrain_epoch"]
                got = terrain_gen.terrain_inputs_sha(ep_dir)
            else:
                unchecked += 1
                continue
        except Exception as e:  # noqa: BLE001 — an unresolvable input is a failure, not a skip
            rep.error("stale", f"{name}: cannot recompute its input hash: {e}")
            continue

        if got == recorded:
            fresh += 1
        else:
            stale += 1
            rep.error("stale", f"{name} is STALE — its inputs now hash to {got[:12]}, the "
                               f"committed mesh was built from {recorded[:12]}. The data and the "
                               f"geometry disagree, so the renderer is showing the old building. "
                               f"Re-bake it (tools/bake.sh, or the chicago-4d-bake workflow) and "
                               f"land the GLB with the change that caused this")

    rep.note(f"stale check: {fresh} asset(s) match their inputs, {stale} stale"
             + (f", {unchecked} not input-tracked" if unchecked else "")
             + f"; scheme {scheme}, manifest blender {manifest.get('blender', '?')}")


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
