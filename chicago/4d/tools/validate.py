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

# What a phase may say when its structure does not reach the ground. Two states,
# and the second one earned its own argument on 2026-08-11 when Fort Dearborn
# became the first structure in the dataset placed OUTSIDE the modelled terrain
# box rather than merely above it.
#
#   approach_not_modelled   — the ground exists under the structure and the
#                             structure does not reach it. The bridge's case.
#   outside_modelled_ground — there is no ground under the structure at all. The
#                             terrain epoch has not been extended that far yet,
#                             so the question "does it land" has no answer, and
#                             pretending it has one is the failure this state
#                             exists to make visible.
GROUND_CONTACT_STATES = ("approach_not_modelled", "outside_modelled_ground")


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

            # Is there any ground here at all? `Heightfield.height` clamps outside
            # the box, so a structure placed beyond the modelled terrain samples
            # the edge for its base AND for every contact point, the two agree
            # exactly, and the measurement below reports a perfect landing on
            # ground that does not exist. Ask the prior question first.
            outline = _contact_outline(poly, decl["mode"])
            points = [pt for a, b in outline
                      for pt in _resample(to_world(a), to_world(b))]
            if not all(field.covers(e, n) for e, n in points) or not field.covers(e0, n0):
                found.append((sid, pid, "ground_contact", f"structure {sid}/{pid}", None))
                continue

            worst = 0.0
            for e, n in points:
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
            found = (sid, pid) in gapped
            want = "approach_not_modelled" if (found and gap is not None) \
                else "outside_modelled_ground"
            if not found:
                if block is not None:
                    rep.error(where, f"declares ground_contact: '{state}', but its contact "
                                     f"outline sits within {GROUND_CONTACT_TOL_M} m of the "
                                     f"terrain under it — it lands. Drop the declaration, or "
                                     f"move the entry claiming it to the Resolved section of "
                                     f"docs/LIBERTIES.md if the ground caught up")
                continue
            if block is None and gap is None:
                rep.error(where, "stands outside the modelled terrain box altogether — there "
                                 "is no ground under any part of its contact outline, so "
                                 "whether it lands has no answer. Declare ground_contact: "
                                 "{state: 'outside_modelled_ground', note: ...} on the phase "
                                 "and admit it in docs/LIBERTIES.md, or extend the terrain "
                                 "epoch to reach it")
                continue
            if block is None:
                rep.error(where, f"its ground contact stands {gap:+.2f} m off the terrain "
                                 f"beneath it — more than the walker's {GROUND_CONTACT_TOL_M} m "
                                 f"step-up rule, so a visitor could not step between the two. "
                                 f"Nothing in the record is wrong and nothing shows it: declare "
                                 f"ground_contact: {{state: 'approach_not_modelled', note: ...}} "
                                 f"on the phase and admit it in docs/LIBERTIES.md")
                continue
            if state in GROUND_CONTACT_STATES and state != want:
                rep.error(where, f"declares ground_contact: '{state}', but the measurement says "
                                 f"'{want}' — the two are different findings and a visitor "
                                 f"reading the first would be told the ground is there")
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
                             unlanded: list[tuple] | None = None) -> None:
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
    """
    entries = liberties.get("liberties") if isinstance(liberties, dict) else None
    if not entries:
        rep.error("liberties", "data/liberties.json holds no entries, so the values "
                               "invented in data/structures/ cannot be checked against "
                               "docs/LIBERTIES.md — run tools/compile_liberties.py")
        return

    # (structure, phase|None, aspect) -> the entries claiming it.
    claims: dict[tuple, list[dict]] = {}
    for e in entries:
        for c in e.get("covers") or []:
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
    invented = omitted = unlanded_n = 0
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
             f"{omitted} stated and not built, {unlanded_n} standing off the ground — claimed by "
             f"{len(honoured)} declaration(s) in docs/LIBERTIES.md")


# --------------------------------------------------------------------------
# flora: zone records, palettes, and the July phenology traps
# --------------------------------------------------------------------------
#
# docs/research/02-flora.md carries a block of "Global phenology rules" whose
# whole point is that a mid-July prairie is easy to render as a September one.
# Those rules are enforced HERE, as schema, rather than left as prose: the
# dossier calls 2 m turkey-foot seed heads on big bluestem in July "the single
# most common historical-reconstruction error", and an error you can only catch
# by eye is one you will ship. Everything below makes a wrong record
# unrepresentable rather than merely discouraged.

FLORA = DATA / "flora"

FLORA_ROLES = ("matrix", "forb", "emergent", "shrub_low", "ground", "tree", "thicket")
FLORA_PHENOLOGY = ("flowering", "vegetative", "budding", "past_bloom", "fruiting",
                   "leafless", "senescent")
EXTENT_KINDS = ("elevation_band", "polygon", "buffer", "everywhere")
ABUNDANCE_LIMITS = {"cover_fraction": 1.0, "density_per_ha": 5000.0, "stems_per_m2": 200.0}

# The three warm-season grasses that are LEAFY AND VEGETATIVE in mid-July, at
# roughly half their September height. Naming them here is the point: this is the
# error the dossier singles out.
JULY_VEGETATIVE_GRASSES = {
    "Andropogon gerardii": 1.5,
    "Sorghastrum nutans": 1.5,
    "Panicum virgatum": 1.6,
}
# ...and the two that DO flower now. Cordgrass is the tall element in July.
JULY_FLOWERING_GRASSES = ("Sporobolus michauxianus", "Calamagrostis canadensis")
# Later arrivals: a cattail that did not reach Illinois until long after 1835.
BANNED_TAXA = ("Typha angustifolia", "Typha x glauca", "Typha × glauca",
               "Lythrum salicaria", "Phalaris arundinacea", "Rhamnus cathartica",
               "Phragmites australis subsp. australis")


def _rgb_ok(v) -> bool:
    return (isinstance(v, list) and len(v) == 3
            and all(isinstance(c, int) and 0 <= c <= 255 for c in v))


def _is_july_green(rgb) -> bool:
    """A July foliage colour: green-dominant and not straw.

    A tawny sward is the October negative control the reference set carries on
    purpose; the check is deliberately crude and deliberately absolute.
    """
    r, g, b = rgb
    return g >= r and g > b


def _carries_flower_colour(rgb) -> bool:
    """True for a saturated bloom colour — what a past-bloom fruit must not be."""
    r, g, b = rgb
    return b >= max(r, g) or (min(r, g) - b) > 100 or (r - max(g, b)) > 90


def _num_range(v, lo=0.0, hi=1e9) -> bool:
    return (isinstance(v, list) and len(v) == 2
            and all(isinstance(x, (int, float)) for x in v)
            and lo <= v[0] <= v[1] <= hi)


def _point_in_polygon(e: float, n: float, poly: list) -> bool:
    inside = False
    j = len(poly) - 1
    for i, (xi, yi) in enumerate(poly):
        xj, yj = poly[j]
        if (yi > n) != (yj > n):
            x = xi + (n - yi) * (xj - xi) / ((yj - yi) or 1e-12)
            if e < x:
                inside = not inside
        j = i
    return inside


def _water_distance(field) -> list:
    """Chamfer distance in metres from every cell to the nearest water cell.

    Two passes over the grid with a (1, sqrt2) kernel. Approximate by about two
    per cent, which is far inside the tolerance of a question like "is this cell
    within eight metres of the river".
    """
    cols, rows, cell = field.cols, field.rows, field.cell_m
    big = 1e9
    d = [0.0 if field._at(i, j) <= 0.0 else big
         for j in range(rows) for i in range(cols)]
    diag = 2 ** 0.5
    for j in range(rows):
        base = j * cols
        prev = base - cols
        for i in range(cols):
            k = base + i
            if d[k] == 0.0:
                continue
            best = d[k]
            if i > 0:
                best = min(best, d[k - 1] + 1.0)
            if j > 0:
                best = min(best, d[prev + i] + 1.0)
                if i > 0:
                    best = min(best, d[prev + i - 1] + diag)
                if i < cols - 1:
                    best = min(best, d[prev + i + 1] + diag)
            d[k] = best
    for j in range(rows - 1, -1, -1):
        base = j * cols
        nxt = base + cols
        for i in range(cols - 1, -1, -1):
            k = base + i
            if d[k] == 0.0:
                continue
            best = d[k]
            if i < cols - 1:
                best = min(best, d[k + 1] + 1.0)
            if j < rows - 1:
                best = min(best, d[nxt + i] + 1.0)
                if i < cols - 1:
                    best = min(best, d[nxt + i + 1] + diag)
                if i > 0:
                    best = min(best, d[nxt + i - 1] + diag)
            d[k] = best
    return [x * cell for x in d]


def _extent_matches(ext: dict, e: float, n: float, h: float, dwater: float) -> bool:
    box = ext.get("box")
    if box:
        be, bn = box.get("e"), box.get("n")
        if be and not (be[0] <= e <= be[1]):
            return False
        if bn and not (bn[0] <= n <= bn[1]):
            return False
    kind = ext.get("kind")
    if kind == "elevation_band":
        lo, hi = ext.get("elev_m", [0, 0])
        if not (lo <= h <= hi):
            return False
    elif kind == "polygon":
        if not _point_in_polygon(e, n, ext.get("polygon") or []):
            return False
    elif kind == "buffer":
        lo, hi = ext.get("distance_m", [0, 0])
        if not (lo <= dwater <= hi):
            return False
    elif kind != "everywhere":
        return False
    for hole in ext.get("exclude_polygons") or []:
        if _point_in_polygon(e, n, hole):
            return False
    return True


def check_flora_extents(zones: dict, field, rep: Report) -> None:
    """Evaluate every zone's extent against the committed heightfield.

    Answers three questions no eye can answer reliably: does a zone that claims
    to be plantable actually match any ground; do two zones tie on priority
    anywhere (the contract calls a tie a data error); and how much land ends up
    unzoned, which the renderer must leave EMPTY rather than fill with a default
    community.
    """
    if field is None:
        rep.note("flora extents: skipped — needs the committed heightfield")
        return
    dwater = _water_distance(field)
    cols, rows, cell = field.cols, field.rows, field.cell_m
    step = 2  # every second cell: 5 m spacing over a 640 m box
    matched = {zid: 0 for zid in zones}
    land = water = unzoned = 0
    ties: set = set()
    for j in range(0, rows, step):
        n = field.origin_n + j * cell
        for i in range(0, cols, step):
            e = field.origin_e + i * cell
            h = field._at(i, j)
            d = dwater[j * cols + i]
            hits = [(z.get("extent", {}).get("priority", 0), zid)
                    for zid, z in zones.items()
                    if _extent_matches(z.get("extent", {}), e, n, h, d)]
            for _, zid in hits:
                matched[zid] += 1
            if h <= 0.0:
                water += 1
                continue
            land += 1
            if not hits:
                unzoned += 1
                continue
            top = max(p for p, _ in hits)
            winners = sorted(zid for p, zid in hits if p == top)
            if len(winners) > 1:
                ties.add(tuple(winners))
    for w in sorted(ties):
        rep.error("flora extents", f"zones {' and '.join(w)} share priority where their "
                                   f"extents overlap — the contract makes a tie a data error, "
                                   f"because it leaves the community at that point undecided")
    for zid, z in zones.items():
        declared = z.get("plantable_in_scene")
        actual = matched[zid] > 0
        if declared is None:
            rep.error(f"flora zone {zid}", "plantable_in_scene is missing — a zone must say "
                                           "whether it has modelled ground in this scene "
                                           "rather than leave the renderer to discover it")
        elif bool(declared) != actual:
            rep.error(f"flora zone {zid}",
                      f"plantable_in_scene is {declared} but its extent matches "
                      f"{matched[zid]} sample(s) of the committed heightfield. A zone off the "
                      f"modelled ground must say so; one on it must not claim otherwise")
    pct = 100.0 * unzoned / land if land else 0.0
    rep.note(f"flora extents: {land} land sample(s), {water} water, {unzoned} unzoned "
             f"({pct:.1f}%) — unzoned ground is planted with NOTHING, never a default "
             f"community")
    if pct > 10.0:
        rep.warn("flora extents", f"{pct:.1f}% of the modelled land matches no zone; that is "
                                  f"bare ground in the walkthrough, so either a zone's extent "
                                  f"is wrong or the gap needs stating")


def check_flora_species(zid: str, sp: dict, source_ids: set, vocab: dict,
                        rep: Report, tally: dict) -> None:
    where = f"flora zone {zid}/{sp.get('id', '?')}"
    binomial = (sp.get("binomial") or "").strip()
    for key in ("id", "binomial", "common", "role", "form", "abundance", "height_m",
                "july", "confidence"):
        if key not in sp:
            rep.error(where, f"missing required key '{key}'")
            return
    if not SLUG.match(sp["id"] or ""):
        rep.error(where, f"id '{sp['id']}' is not a lowercase slug")
    if sp["role"] not in FLORA_ROLES:
        rep.error(where, f"role '{sp['role']}' is not one of {FLORA_ROLES}")
    forms = set(vocab.get("forms_flora", [])) | set(vocab.get("forms_trees", [])) \
        | set(vocab.get("forms_unimplemented", []))
    if sp["form"] not in forms:
        rep.error(where, f"form '{sp['form']}' is not declared in index.json's vocabulary — "
                         f"a renderer reads that block to know what it may be asked to draw")
    for banned in BANNED_TAXA:
        if binomial.lower() == banned.lower():
            rep.error(where, f"{banned} is a post-settlement arrival and must not appear in "
                             f"an 1835 record")

    ab = sp["abundance"]
    keys = [k for k in ABUNDANCE_LIMITS if k in ab]
    if len(keys) != 1 or len(ab) != 1:
        rep.error(where, f"abundance must carry EXACTLY ONE of {tuple(ABUNDANCE_LIMITS)}, "
                         f"got {sorted(ab)}")
    elif not _num_range(ab[keys[0]], 0.0, ABUNDANCE_LIMITS[keys[0]]):
        rep.error(where, f"abundance.{keys[0]} must be [min,max] ascending within "
                         f"0..{ABUNDANCE_LIMITS[keys[0]]}, got {ab[keys[0]]}")
    if not _num_range(sp["height_m"], 0.01, 45.0):
        rep.error(where, f"height_m must be [min,max] ascending in metres, got {sp['height_m']}")
    if "width_m" in sp and not _num_range(sp["width_m"], 0.01, 45.0):
        rep.error(where, f"width_m must be [min,max] ascending, got {sp['width_m']}")

    j = sp.get("july")
    if not isinstance(j, dict):
        rep.error(where, "july must be the phenology block for the scene date")
        return
    ph = j.get("phenology")
    if ph not in FLORA_PHENOLOGY:
        rep.error(where, f"july.phenology '{ph}' is not one of {FLORA_PHENOLOGY}")
    infl = j.get("inflorescence")
    if "inflorescence" not in j:
        rep.error(where, "july.inflorescence must be present, null when there is nothing "
                         "in flower or fruit — an absent key hides the claim")
    if not (j.get("appearance") or "").strip():
        rep.error(where, "july.appearance is what a critic reads to decide whether the render "
                         "matches the record; it may not be empty")

    fol = j.get("foliage_rgb")
    if ph == "leafless":
        if fol is not None:
            rep.error(where, "phenology 'leafless' requires foliage_rgb null — leafless means "
                             "no leaves, and a green in this field puts them back")
    elif not _rgb_ok(fol):
        rep.error(where, f"july.foliage_rgb must be [r,g,b] 0-255, got {fol}")
    elif not _is_july_green(fol):
        rep.error(where, f"july.foliage_rgb {fol} is not a July green (green must be the "
                         f"dominant channel). A tawny or straw sward is the October scene, "
                         f"which fails the reference bar")
    alt = j.get("foliage_rgb_alt")
    if alt is not None and (not _rgb_ok(alt) or not _is_july_green(alt)):
        rep.error(where, f"july.foliage_rgb_alt {alt} must be a second July green")

    if infl is not None:
        if not isinstance(infl, dict) or not _rgb_ok(infl.get("rgb")):
            rep.error(where, "july.inflorescence needs a shape and an [r,g,b]")
        else:
            if not (0.0 <= (infl.get("height_frac") or -1) <= 1.0):
                rep.error(where, "july.inflorescence.height_frac must be 0..1 (0 base, 1 tip)")
            if not _num_range(infl.get("size_m"), 0.001, 3.0):
                rep.error(where, "july.inflorescence.size_m must be [min,max] in metres")

    # --- the traps ---------------------------------------------------------
    if ph in ("vegetative", "budding") and infl is not None:
        rep.error(where, f"phenology '{ph}' requires inflorescence null — a plant that is "
                         f"vegetative or in bud has nothing open to draw")
    if binomial in JULY_VEGETATIVE_GRASSES:
        limit = JULY_VEGETATIVE_GRASSES[binomial]
        if ph != "vegetative" or infl is not None:
            rep.error(where, f"{binomial} is VEGETATIVE in mid-July with no inflorescence. "
                             f"The dossier names July seed heads on this grass the single "
                             f"most common historical-reconstruction error")
        if isinstance(sp.get("height_m"), list) and len(sp["height_m"]) == 2 \
                and sp["height_m"][1] > limit:
            rep.error(where, f"{binomial} at {sp['height_m'][1]} m is its September height; in "
                             f"mid-July it stands at 50-60 per cent of that, under {limit} m")
    if binomial in JULY_FLOWERING_GRASSES and (ph != "flowering" or infl is None):
        rep.error(where, f"{binomial} IS in flower in mid-July and must carry an "
                         f"inflorescence — cordgrass is the tall flowering element of the "
                         f"July prairie")
    if binomial == "Typha latifolia":
        if ph != "fruiting":
            rep.error(where, "Typha latifolia is FRUITING in July — the spike is mature")
        if isinstance(infl, dict) and _rgb_ok(infl.get("rgb")):
            r, g, b = infl["rgb"]
            if not (r > g > b):
                rep.error(where, f"the July cattail spike is BROWN; {infl['rgb']} is not "
                                 f"(needs red > green > blue). Green or yellow spikes date "
                                 f"the scene to spring")
    if binomial == "Allium tricoccum":
        if ph != "leafless" or sp.get("form") != "scape_leafless" or fol is not None:
            rep.error(where, "Allium tricoccum in July is LEAFLESS: phenology 'leafless', "
                             "form 'scape_leafless', foliage_rgb null. Its leaves wither "
                             "before the scape rises, so green onion foliage in a July scene "
                             "is wrong")
    if ph == "past_bloom" and isinstance(infl, dict) and _rgb_ok(infl.get("rgb")) \
            and _carries_flower_colour(infl["rgb"]):
        rep.error(where, f"phenology 'past_bloom' with inflorescence {infl['rgb']} — a plant "
                         f"past bloom shows a fruit, not its flower colour")
    if ph == "fruiting" and isinstance(infl, dict) and not infl.get("fruit"):
        rep.error(where, "phenology 'fruiting' requires inflorescence.fruit true, so a reader "
                         "cannot mistake the colour for a flower")

    conf = check_attested(where, "species", sp, source_ids, rep)
    if conf:
        tally[conf] = tally.get(conf, 0) + 1


def check_flora(source_ids: set, field, rep: Report, tally: dict) -> dict:
    """Schema, provenance and phenology gate for data/flora/**."""
    index_path = FLORA / "index.json"
    if not index_path.exists():
        rep.note("flora: no data/flora/index.json — the walkthrough plants nothing")
        return {}
    index = load_json(index_path, rep)
    if not isinstance(index, dict):
        return {}

    scene_date = index.get("scene_date") or ""
    d = parse_date(scene_date)
    if d is None:
        rep.error("flora index", "scene_date must be an ISO date")
    elif d.month != 7:
        rep.error("flora index", f"scene_date {scene_date} is not in July, but every zone "
                                 f"record carries a 'july' phenology block. Move the "
                                 f"phenology, do not move the month")

    vocab = index.get("vocabulary") or {}
    for key in ("roles", "forms_flora", "forms_trees", "phenology"):
        if not vocab.get(key):
            rep.error("flora index", f"vocabulary.{key} is missing — the renderer reads this "
                                     f"block to know the closed sets it must implement")

    palettes = {}
    for entry in index.get("palettes", []):
        pid, pfile = entry.get("id"), entry.get("file")
        path = FLORA / (pfile or "")
        if not pfile or not path.exists():
            rep.error("flora index", f"palette '{pid}' names {pfile}, which does not exist")
            continue
        pal = load_json(path, rep)
        if not isinstance(pal, dict):
            continue
        if pal.get("id") != pid or path.stem != pid:
            rep.error(f"flora palette {pid}", "id must match both the manifest and the filename")
        if pal.get("sources"):
            rep.error(f"flora palette {pid}", "a palette is render tuning, not evidence, and "
                                              "must not carry a source_id")
        greens = pal.get("greens") or []
        if len(greens) < 3 or not all(_rgb_ok(g) for g in greens):
            rep.error(f"flora palette {pid}", "greens must be a ramp of at least three "
                                              "[r,g,b] values")
        elif not all(_is_july_green(g) for g in greens):
            rep.error(f"flora palette {pid}", f"the foliage ramp {greens} is not all July "
                                              f"greens — a straw ramp is the October scene")
        palettes[pid] = pal

    zones = {}
    for entry in index.get("zones", []):
        zid, zfile = entry.get("id"), entry.get("file")
        path = FLORA / (zfile or "")
        if not zfile or not path.exists():
            rep.error("flora index", f"zone '{zid}' names {zfile}, which does not exist — a "
                                     f"static host cannot be globbed, so a manifest entry "
                                     f"without a file is a 404 on the deployed site")
            continue
        z = load_json(path, rep)
        if not isinstance(z, dict):
            continue
        where = f"flora zone {zid}"
        if z.get("id") != zid or path.stem != zid:
            rep.error(where, "id must match both the manifest entry and the filename stem")
        for key in ("zone", "name", "dossier", "scene_date", "palette", "cover", "ground",
                    "extent", "species", "confidence", "plantable_in_scene"):
            if key not in z:
                rep.error(where, f"missing required key '{key}'")
        if z.get("scene_date") != scene_date:
            rep.error(where, f"scene_date {z.get('scene_date')} disagrees with the manifest's "
                             f"{scene_date}; the phenology is stated FOR a date")
        if z.get("palette") not in palettes:
            rep.error(where, f"palette '{z.get('palette')}' does not resolve in the manifest")

        # the manifest carries denormalised copies so terrain.js needs one fetch;
        # a copy that has drifted is worse than no copy at all
        for key, actual in (("extent", z.get("extent")),
                            ("plantable_in_scene", z.get("plantable_in_scene")),
                            ("ground_rgb", (z.get("ground") or {}).get("rgb")),
                            ("ground_wet_rgb", (z.get("ground") or {}).get("wet_rgb")),
                            ("bare_soil_fraction",
                             (z.get("cover") or {}).get("bare_soil_fraction"))):
            if entry.get(key) != actual:
                rep.error("flora index", f"zone '{zid}' {key} in the manifest "
                                         f"({entry.get(key)!r}) disagrees with the zone record "
                                         f"({actual!r}); the zone record is authoritative")
        if entry.get("priority") != (z.get("extent") or {}).get("priority"):
            rep.error("flora index", f"zone '{zid}' priority in the manifest disagrees with "
                                     f"its extent")

        cover = z.get("cover") or {}
        for key in ("matrix_fraction", "bare_soil_fraction", "standing_water_fraction"):
            v = cover.get(key)
            if not isinstance(v, (int, float)) or not 0.0 <= v <= 1.0:
                rep.error(where, f"cover.{key} must be a fraction 0..1, got {v!r}")
        for key in ("rgb", "wet_rgb"):
            if not _rgb_ok((z.get("ground") or {}).get(key)):
                rep.error(where, f"ground.{key} must be [r,g,b] 0-255")

        ext = z.get("extent") or {}
        kind = ext.get("kind")
        if kind not in EXTENT_KINDS:
            rep.error(where, f"extent.kind '{kind}' is not one of {EXTENT_KINDS}")
        if kind == "elevation_band" and not _num_range(ext.get("elev_m"), -50.0, 400.0):
            rep.error(where, "extent.elev_m must be [low,high] metres above the datum water")
        if kind == "polygon" and len(ext.get("polygon") or []) < 3:
            rep.error(where, "extent.polygon needs at least three vertices")
        if kind == "buffer":
            if ext.get("of") != "water":
                rep.error(where, "extent.of only takes 'water' — the renderer implements one "
                                 "buffer, and an unimplemented one silently plants nothing")
            if not _num_range(ext.get("distance_m"), 0.0, 2000.0):
                rep.error(where, "extent.distance_m must be [min,max] metres from the water")
        if not isinstance(ext.get("priority"), int):
            rep.error(where, "extent.priority must be an integer; higher wins on overlap")
        check_attested(where, "extent", ext, source_ids, rep)

        seen: set = set()
        matrix_max = 0.0
        for sp in z.get("species") or []:
            if sp.get("id") in seen:
                rep.error(where, f"duplicate species id '{sp.get('id')}' in this zone")
            seen.add(sp.get("id"))
            check_flora_species(zid, sp, source_ids, vocab, rep, tally)
            if sp.get("role") in ("matrix", "ground"):
                cf = (sp.get("abundance") or {}).get("cover_fraction")
                if isinstance(cf, list) and len(cf) == 2:
                    matrix_max += cf[1]
        if not seen:
            rep.error(where, "a zone with no species is not a community record")
        if matrix_max > 1.8:
            rep.warn(where, f"matrix and ground cover fractions sum to {matrix_max:.2f} at "
                            f"their maxima; some overlap is real, this much is a bookkeeping "
                            f"error")
        if cover.get("matrix_fraction", 0) >= 0.5 and not any(
                sp.get("role") in ("matrix", "emergent") for sp in z.get("species") or []):
            rep.error(where, "the zone claims a graminoid matrix but lists no matrix or "
                             "emergent species to build it from")
        check_attested(where, "zone", z, source_ids, rep)
        zones[zid] = z

    check_flora_extents(zones, field, rep)

    # Honesty ledger: how much of the species record rests on a source nobody in
    # this project has actually opened. Not an error — a bibliographic record for
    # a work the dossier cites is legitimate — but it is the number a reader
    # should see rather than have to compute.
    unverified = {sid for sid, s in ((Path(p).stem, json.loads(Path(p).read_text()))
                                     for p in sorted((DATA / "sources").glob("*.json")))
                  if not s.get("verified")}
    resting = 0
    for z in zones.values():
        for sp in z.get("species") or []:
            srcs = sp.get("sources") or []
            if sp.get("confidence") == "documented" and srcs and set(srcs) <= unverified:
                resting += 1
    total_sp = sum(len(z.get("species") or []) for z in zones.values())
    if total_sp:
        rep.note(f"flora: {len(zones)} zone(s), {total_sp} species record(s); {resting} "
                 f"documented claim(s) rest only on sources no agent has retrieved "
                 f"(verified false) — real citations, unread")
    return zones


# --------------------------------------------------------------------------
# fauna: zone records, presence modes, and the July gate
# --------------------------------------------------------------------------
#
# The flora section above exists because a mid-July prairie is easy to render as
# a September one. This one exists for the mirror-image reason: a mid-July
# Chicago is easy to render as a May one. Every headline wildlife event in the
# record — passenger-pigeon flights, prairie-chicken booming, waterfowl clouds,
# the spring dawn chorus — is a spring, autumn or winter phenomenon, and 1 July
# is the QUIETEST wildlife date in the Chicago year. docs/research/08-fauna.md
# § 0.3 states that as guidance; the rules below make the wrong record
# unrepresentable rather than merely discouraged, exactly as the phenology gate
# does for the flora.
#
# The second thing this section enforces is that "present" and "visible" are
# different claims. Liberty L2 licenses fauna at low density and often as sound
# only, and that liberty is worth nothing unless the data can SAY "here, and not
# seen" — which is what `presence.mode` is for.

FAUNA = DATA / "fauna"

FAUNA_CLASSES = ("mammal", "bird", "fish", "amphibian", "reptile", "insect", "mollusc")
FAUNA_ACTIVITY = ("diurnal", "crepuscular", "nocturnal", "cathemeral")
FAUNA_PERIODS = ("dawn", "day", "dusk", "night")
FAUNA_STATUS = ("breeding_resident", "year_round_resident", "post_breeding_dispersal",
                "flightless_moult", "domestic", "feral_or_commensal", "doubtful",
                "absent_seasonal", "absent_extirpated", "absent_anachronism",
                "excluded_by_scope")
FAUNA_PRESENCE = ("visible", "audible", "visible_and_audible", "trace_only",
                  "not_perceptible", "absent", "not_depicted")
FAUNA_ABUNDANCE = ("abundant", "common", "frequent", "uncommon", "sparse", "rare", "absent")
FAUNA_VOICE = ("song_full", "song_reduced", "call_only", "chorus", "display_over",
               "silent", "non_vocal")
FAUNA_DAWN_CHORUS = ("none", "reduced")

# A status that says the animal is not in the scene, and the presence mode each
# of those two families must carry. Kept as two sets because they are different
# findings: `absent` is "not here", `not_depicted` is "here and we chose not to
# show it", and collapsing them would lose the distinction liberty L1 rests on.
FAUNA_ABSENT_STATUS = ("absent_seasonal", "absent_extirpated", "absent_anachronism")
FAUNA_ABSENT_MODES = ("absent",)
FAUNA_WITHHELD_STATUS = ("excluded_by_scope",)
FAUNA_WITHHELD_MODES = ("not_depicted",)

# A voice that does not reach a listener. A species recorded as audible must not
# have one of these, or the record claims a sound nobody could hear.
FAUNA_INAUDIBLE = ("silent", "display_over", "non_vocal")

# THE BIRD-SONG GATE. Named species whose song or display is over, or sharply
# reduced, by 1 July — the direct analogue of JULY_VEGETATIVE_GRASSES. Value is
# the set of voices the record is allowed to claim. Getting this wrong does not
# look wrong: a scene full of birdsong reads as "summer" to every viewer and is
# a May scene.
JULY_QUIET_BIRDS = {
    # The lek is silent from June. This is the fauna dossier's headline trap.
    "Tympanuchus cupido": {"display_over", "silent"},
    # Song stops as the young fledge in early July; the chatter carries on.
    "Icterus galbula": {"call_only", "silent"},
    # An April-to-June performance, finished before this date.
    "Toxostoma rufum": {"call_only", "song_reduced", "silent"},
    # Collapses through July as the birds move to moult.
    "Dolichonyx oryzivorus": {"song_reduced", "call_only", "silent"},
    # No song to lose in any month — calls are the whole vocabulary.
    "Cyanocitta cristata": {"call_only", "silent"},
    "Poecile atricapillus": {"call_only", "silent"},
    "Tyrannus tyrannus": {"call_only", "silent"},
    # Drumming and the long territorial call are spring signals.
    "Melanerpes erythrocephalus": {"call_only", "silent"},
    "Colaptes auratus": {"call_only", "silent"},
    # Vultures are effectively voiceless.
    "Cathartes aura": {"silent", "non_vocal"},
    # Not a songbird at all, whatever the flights looked like.
    "Ectopistes migratorius": {"call_only", "silent"},
}

# ...and the positive half, which is what stops a gate like this being satisfied
# by rendering July silent. These species ARE in full song on 1 July — later
# than almost anything else — and recording them mute is the opposite error.
JULY_STILL_SINGING = ("Contopus virens", "Passerina cyanea", "Hylocichla mustelina",
                      "Geothlypis trichas", "Spizella pusilla", "Colinus virginianus")

# The same gate one class down. These frogs call from March to May and are done
# by 1 July — the species is still in the landscape and its VOICE is not, which
# for a frog is the whole of what a scene would carry. A peeper chorus is the
# easiest wrong sound to lay over any Illinois marsh at any date.
FAUNA_SPRING_CHORUS_OVER = ("Pseudacris crucifer", "Pseudacris maculata",
                            "Pseudacris triseriata", "Lithobates sylvaticus")

# Wing moult. Adult ducks enter simultaneous flight-feather moult in late June
# and July and are flightless or nearly so: dull, skulking, and NOT flying.
FAUNA_MOULTING_WATERFOWL = ("Anas platyrhynchos", "Spatula discors", "Aix sponsa",
                            "Mareca strepera", "Anas acuta", "Aythya americana")
FAUNA_MOULT_MAX_GROUP = 12

# The species whose real abundance sounds like an exaggeration, which is exactly
# why the July number has to be held down by the schema rather than by taste.
PASSENGER_PIGEON = "Ectopistes migratorius"
PASSENGER_PIGEON_JULY_MAX = 60

# Present in the period but nothing like its modern numbers. The default modern
# Chicago gull is a post-1916 phenomenon and a flock of them is the single most
# visible anachronism available at the river mouth.
FAUNA_RARE_ONLY = {"Larus delawarensis": ("rare", "absent")}

# NOT AT THIS PLACE ON THIS DATE, and the dataset may not say otherwise. These
# are the dossier's § 6 negative findings turned into schema: a record may state
# any of them as an ABSENCE — that is what the negative findings are for, and
# recording why something is missing is the whole standard — but it may not put
# the animal in the scene. Without this, a beaver lodge could be added at the
# forks by editing one field, which is exactly the difference between a rule a
# modeller should follow and a record that cannot be written.
FAUNA_ABSENT_TAXA = {
    "Bison bison": "no wild bison remained in Illinois by about 1830",
    "Bos bison": "the period name for the bison; extirpated from Illinois by about 1830",
    "Cervus canadensis": "elk were gone from Illinois by the early 1800s",
    "Castor canadensis": "no Chicago-proper 1830s beaver record exists; the nearest attested "
                         "population was the Calumet region, twelve or more miles south. No "
                         "beaver, no lodges, and no beaver-cut stumps at the forks",
    "Puma concolor": "probably exterminated in Illinois before 1870 and locally far earlier",
    "Ursus americanus": "Chicago-area bear records end in the 1830s and are anecdotal; none is "
                        "datable to 1835",
    "Passer domesticus": "introduced to North America in 1851, sixteen years after this scene",
    "Sturnus vulgaris": "introduced to North America in 1890",
    "Cyprinus carpio": "the common carp was not stocked in North America in numbers until the "
                       "1870s; Andreas's 'twelve carps' are native minnows in period usage",
    "Magicicada septendecim": "northern Illinois is 17-year Brood XIII and its years are 1820, "
                              "1837 and 1854 — not 1835 — and it emerges in late May and June "
                              "in any case",
    "Magicicada cassinii": "as Magicicada septendecim: Brood XIII, and 1835 is not a brood year",
    "Magicicada septendecula": "as Magicicada septendecim: Brood XIII, and 1835 is not a brood "
                               "year",
}

# Words that name a spring, autumn or winter spectacle. Forbidden in `behaviour`
# — the render instruction — for any species the record says is present. A
# negative record may say them freely, because saying what is NOT here is the
# whole job of a negative record.
FAUNA_WRONG_SEASON_WORDS = ("migrat", "skein", "v-formation", "sky-darken",
                            "booming", "lek", "raft of", "dawn chorus", "rut")


def _fauna_val(node, key: str):
    """The value of an attested block, or of a bare value."""
    v = node.get(key)
    if isinstance(v, dict) and "value" in v:
        return v["value"]
    return v


def check_fauna_species(zid: str, sp: dict, source_ids: set, vocab: dict,
                        rep: Report, tally: dict) -> None:
    where = f"fauna zone {zid}/{sp.get('id', '?')}"
    binomial = (sp.get("binomial") or "").strip()
    for key in ("id", "binomial", "common", "class", "activity", "active_periods",
                "july", "confidence"):
        if key not in sp:
            rep.error(where, f"missing required key '{key}'")
            return
    if not SLUG.match(sp["id"] or ""):
        rep.error(where, f"id '{sp['id']}' is not a lowercase slug")
    if sp["class"] not in (vocab.get("classes") or FAUNA_CLASSES):
        rep.error(where, f"class '{sp['class']}' is not declared in index.json's vocabulary")
    if sp["activity"] not in (vocab.get("activity") or FAUNA_ACTIVITY):
        rep.error(where, f"activity '{sp['activity']}' is not one of {FAUNA_ACTIVITY}")

    periods = sp.get("active_periods")
    if not isinstance(periods, list) or not periods \
            or any(p not in FAUNA_PERIODS for p in periods):
        rep.error(where, f"active_periods must be a non-empty subset of {FAUNA_PERIODS}, "
                         f"got {periods!r}")
        periods = []
    # An animal on screen at an hour its own activity pattern excludes is the
    # commonest way a reconstruction quietly invents behaviour. Say cathemeral
    # and mean it — the Chicago coyotes are documented abroad in daylight, and
    # that is a finding, not a default.
    act = sp["activity"]
    if act == "diurnal" and "night" in periods:
        rep.error(where, "activity 'diurnal' with 'night' in active_periods — use 'cathemeral' "
                         "and say on the record why this animal is abroad after dark")
    if act == "nocturnal" and "day" in periods:
        rep.error(where, "activity 'nocturnal' with 'day' in active_periods — use 'cathemeral'. "
                         "A nocturnal animal on screen at noon is a claim, and it needs to be "
                         "made explicitly (the Chicago coyote is exactly that case: Andreas has "
                         "one entering a meat-house IN THE DAY TIME)")
    if act == "crepuscular":
        if "day" in periods:
            rep.error(where, "activity 'crepuscular' with 'day' in active_periods — use "
                             "'cathemeral'; crepuscular means the light margins, not midday")
        if not ({"dawn", "dusk"} & set(periods)):
            rep.error(where, "activity 'crepuscular' but neither dawn nor dusk is in "
                             "active_periods")
    if act == "diurnal" and "day" not in periods:
        rep.error(where, "activity 'diurnal' without 'day' in active_periods")

    j = sp.get("july")
    if not isinstance(j, dict):
        rep.error(where, "july must be the block stating this animal's state on the scene date")
        return
    for key in ("status", "presence", "abundance", "max_group", "vocalization",
                "behaviour", "appearance"):
        if key not in j:
            rep.error(where, f"july.{key} is required — the whole point of this dataset is "
                             f"that the July state is stated rather than assumed")
            return
    if "trace" not in j:
        rep.error(where, "july.trace must be present, null when the animal leaves no rendered "
                         "sign — an absent key hides the claim, exactly as it does for flora "
                         "inflorescence")

    status = _fauna_val(j, "status")
    mode = _fauna_val(j, "presence")
    abundance = _fauna_val(j, "abundance")
    voice = j.get("vocalization")
    group = j.get("max_group")
    behaviour = (j.get("behaviour") or "").strip()
    appearance = (j.get("appearance") or "").strip()

    if status not in FAUNA_STATUS:
        rep.error(where, f"july.status '{status}' is not one of {FAUNA_STATUS}")
    if mode not in FAUNA_PRESENCE:
        rep.error(where, f"july.presence '{mode}' is not one of {FAUNA_PRESENCE}")
    if abundance not in FAUNA_ABUNDANCE:
        rep.error(where, f"july.abundance '{abundance}' is not one of {FAUNA_ABUNDANCE}")
    if voice not in FAUNA_VOICE:
        rep.error(where, f"july.vocalization '{voice}' is not one of {FAUNA_VOICE}")
    if not isinstance(group, int) or isinstance(group, bool) or not 0 <= group <= 500:
        rep.error(where, f"july.max_group must be an integer 0..500 (0 = nothing is placed), "
                         f"got {group!r}")
        group = 0
    if not behaviour:
        rep.error(where, "july.behaviour is the render instruction and may not be empty; write "
                         "'Nothing is drawn.' when that is the answer")
    if not appearance:
        rep.error(where, "july.appearance is what a critic reads to decide whether the render "
                         "matches the record; it may not be empty")

    # --- present, absent, and withheld are three different claims -----------
    #
    # ...and `doubtful` is the fourth, which is why it is exempt from the
    # coupling below. A species whose July presence is genuinely uncertain may
    # be recorded with NOTHING placed for it without that being a finding of
    # absence — the ring-billed gull is the case: rare and persecuted in the
    # 19th century, tempting to a renderer, and neither attested nor refuted
    # here. Forcing that record to choose between "present" and "absent" would
    # make the dataset resolve a question the evidence does not.
    if status == "doubtful":
        pres = j.get("presence")
        if not (isinstance(pres, dict) and (pres.get("note") or "").strip()):
            rep.error(where, "july.status 'doubtful' requires a note on the presence block "
                             "saying what the doubt is and what the scene does about it. "
                             "Recording doubt is the point; recording it silently is not")
    elif status in FAUNA_ABSENT_STATUS:
        if mode not in FAUNA_ABSENT_MODES:
            rep.error(where, f"july.status '{status}' says this animal is not in the scene, but "
                             f"july.presence is '{mode}'. A negative finding that leaves a "
                             f"visible animal on the record is worse than no finding")
        if abundance != "absent":
            rep.error(where, f"july.status '{status}' with abundance '{abundance}' — an animal "
                             f"that is not here has no abundance")
        if group:
            rep.error(where, f"july.status '{status}' with max_group {group} — nothing may be "
                             f"placed for a species recorded as absent")
    elif status in FAUNA_WITHHELD_STATUS:
        if mode not in FAUNA_WITHHELD_MODES:
            rep.error(where, f"july.status 'excluded_by_scope' requires presence 'not_depicted' "
                             f"— the animal IS here and is deliberately not shown, which is a "
                             f"different claim from absence and must not be recorded as one")
        if group:
            rep.error(where, "an excluded_by_scope record may not place anything (max_group 0)")
    else:
        if mode in ("absent", "not_depicted"):
            rep.error(where, f"july.presence '{mode}' with a present status '{status}' — say "
                             f"which absence this is: absent_seasonal, absent_extirpated, "
                             f"absent_anachronism, or excluded_by_scope")
        if abundance == "absent":
            rep.error(where, f"abundance 'absent' with a present status '{status}'")

    # --- present, and not seen ---------------------------------------------
    if mode in ("audible", "visible_and_audible") and voice in FAUNA_INAUDIBLE:
        rep.error(where, f"july.presence '{mode}' claims this animal is HEARD, but its "
                         f"vocalization is '{voice}'. A silent bird cannot be audible, and a "
                         f"lek whose season is over is silent by definition")
    if mode == "trace_only" and not (j.get("trace") or "").strip():
        rep.error(where, "july.presence 'trace_only' requires july.trace to describe the sign "
                         "that IS rendered — runways, burrows, shell scatter, a landed fish. "
                         "Trace-only with no trace renders nothing and claims something")
    if mode == "not_perceptible" and not (
            (j.get("presence") or {}).get("note") if isinstance(j.get("presence"), dict) else None):
        rep.error(where, "july.presence 'not_perceptible' says the animal is here and neither "
                         "seen nor heard, which is the strongest claim in this vocabulary and "
                         "needs a note on the presence block saying why")

    # --- the July gate ------------------------------------------------------
    if sp["class"] == "bird" and voice == "song_full":
        note = (sp.get("note") or "")
        if "July" not in note:
            rep.error(where, "vocalization 'song_full' on a bird is the EXCEPTIONAL claim for "
                             "1 July — the dawn chorus is a spring phenomenon and most "
                             "passerines have stopped or sharply reduced singing by now. The "
                             "record must argue it: put the reason, mentioning July, in the "
                             "species note")
    if binomial in JULY_QUIET_BIRDS and voice not in JULY_QUIET_BIRDS[binomial]:
        rep.error(where, f"{binomial} is not in song on 1 July; this record claims '{voice}'. "
                         f"Allowed: {sorted(JULY_QUIET_BIRDS[binomial])}. A July scene full of "
                         f"birdsong is the fauna equivalent of seed heads on July big bluestem")
    if binomial in JULY_STILL_SINGING and voice in ("silent", "display_over"):
        rep.error(where, f"{binomial} IS still in song on 1 July — later than almost anything "
                         f"else — and recording it silent over-corrects the July gate into a "
                         f"different error")
    if binomial in FAUNA_SPRING_CHORUS_OVER and voice not in ("silent", "non_vocal"):
        rep.error(where, f"{binomial} calls from March to May and is finished by 1 July; this "
                         f"record claims '{voice}'. The animal may still be recorded as "
                         f"present — it is in the landscape — but its chorus is a spring "
                         f"sound and putting it over a July marsh dates the scene by two "
                         f"months")
    if binomial in FAUNA_MOULTING_WATERFOWL and status not in FAUNA_ABSENT_STATUS:
        if status != "flightless_moult":
            rep.error(where, f"{binomial} is in simultaneous wing moult in late June and July "
                             f"and is flightless or nearly so; july.status must be "
                             f"'flightless_moult', not '{status}'. There are no migrating "
                             f"flocks on 1 July and the adults are dull, skulking and not "
                             f"flying")
        if group > FAUNA_MOULT_MAX_GROUP:
            rep.error(where, f"{binomial} with max_group {group} — a moulting July duck is a "
                             f"hen with a brood, not a raft. Ceiling is "
                             f"{FAUNA_MOULT_MAX_GROUP}")
    if binomial == PASSENGER_PIGEON and status not in FAUNA_ABSENT_STATUS:
        if status != "post_breeding_dispersal":
            rep.error(where, "the passenger pigeon on 1 July is in small wandering "
                             "post-breeding flocks, not nesting and not on passage; "
                             "july.status must be 'post_breeding_dispersal'")
        if group > PASSENGER_PIGEON_JULY_MAX:
            rep.error(where, f"max_group {group} for the passenger pigeon. The Chicago record "
                             f"of a sky full of them — 'the horizon in almost every direction "
                             f"was black with them' — is dated 17 SEPTEMBER 1836, a fall "
                             f"movement. On 1 July the number is tens, not millions; the "
                             f"ceiling here is {PASSENGER_PIGEON_JULY_MAX}")
        if not (sp.get("note") or "").strip():
            rep.error(where, "the passenger pigeon needs its numbers argued on the record more "
                             "than any other species in this dataset, because its real "
                             "abundance sounds like exaggeration. State what the source "
                             "actually says, and when it says it")
    if binomial in FAUNA_ABSENT_TAXA and status not in FAUNA_ABSENT_STATUS:
        rep.error(where, f"{binomial} is not at the Chicago town site on 1 July 1835: "
                         f"{FAUNA_ABSENT_TAXA[binomial]}. The record may state this species as "
                         f"an absence — a negative finding is worth keeping — but it may not "
                         f"put the animal in the scene")
    if binomial in FAUNA_RARE_ONLY and abundance not in FAUNA_RARE_ONLY[binomial]:
        rep.error(where, f"{binomial} may only be recorded as "
                         f"{' or '.join(FAUNA_RARE_ONLY[binomial])} in an 1835 scene — it was "
                         f"rare and persecuted in the 19th century and became the abundant "
                         f"Great Lakes gull only after protection in 1916")
    if status not in FAUNA_ABSENT_STATUS and status not in FAUNA_WITHHELD_STATUS:
        low = behaviour.lower()
        for word in FAUNA_WRONG_SEASON_WORDS:
            if word in low:
                rep.error(where, f"july.behaviour names '{word}', which is a spring, autumn or "
                                 f"winter phenomenon. 1 July is the annual minimum for all of "
                                 f"them: no migration, silent leks, moulting waterfowl. Say it "
                                 f"in the note if it needs saying; it may not be a render "
                                 f"instruction")
    if status == "doubtful" and sp.get("confidence") == "documented":
        rep.error(where, "july.status 'doubtful' with confidence 'documented' — if the July "
                         "presence is in doubt the record cannot also be documented. Record the "
                         "doubt rather than resolving it by preference")

    # --- provenance ---------------------------------------------------------
    walk_attested(where, j, source_ids, rep, tally, "july")
    conf = check_attested(where, "species", sp, source_ids, rep)
    if conf:
        tally[conf] = tally.get(conf, 0) + 1
    if conf == "conjectural" and not (sp.get("note") or "").strip():
        rep.error(where, "conjectural requires a note saying what the belief rests on and that "
                         "it is not evidence. Unknown is recorded as unknown, never left blank")


def check_fauna(source_ids: set, rep: Report, tally: dict) -> dict:
    """Schema, provenance and the July gate for data/fauna/**."""
    index_path = FAUNA / "index.json"
    if not index_path.exists():
        rep.note("fauna: no data/fauna/index.json — the scene carries no animals")
        return {}
    index = load_json(index_path, rep)
    if not isinstance(index, dict):
        return {}

    scene_date = index.get("scene_date") or ""
    d = parse_date(scene_date)
    if d is None:
        rep.error("fauna index", "scene_date must be an ISO date")
    elif d.month != 7:
        rep.error("fauna index", f"scene_date {scene_date} is not in July, but every zone "
                                 f"record carries a 'july' block stating what each animal is "
                                 f"doing on the scene date. Move the seasonal states, do not "
                                 f"move the month")

    vocab = index.get("vocabulary") or {}
    for key in ("classes", "activity", "active_periods", "july_status", "presence_modes",
                "abundance", "vocalization", "habitats"):
        if not vocab.get(key):
            rep.error("fauna index", f"vocabulary.{key} is missing — a renderer reads this "
                                     f"block to know the closed sets it must implement")

    # The fauna zones borrow their geometry from the flora zones rather than
    # restating it, so the two datasets cannot drift into describing different
    # ground. That only holds if the reference is checked.
    flora_index = load_json(FLORA / "index.json", rep, required=False)
    flora_zones = {z.get("id"): z for z in (flora_index or {}).get("zones", [])} \
        if isinstance(flora_index, dict) else {}

    zones = {}
    for entry in index.get("zones", []):
        zid, zfile = entry.get("id"), entry.get("file")
        path = FAUNA / (zfile or "")
        if not zfile or not path.exists():
            rep.error("fauna index", f"zone '{zid}' names {zfile}, which does not exist — a "
                                     f"static host cannot be globbed, so a manifest entry "
                                     f"without a file is a 404 on the deployed site")
            continue
        z = load_json(path, rep)
        if not isinstance(z, dict):
            continue
        where = f"fauna zone {zid}"
        if z.get("id") != zid or path.stem != zid:
            rep.error(where, "id must match both the manifest entry and the filename stem")
        for key in ("zone", "name", "habitat", "dossier", "scene_date", "reads_as",
                    "in_modelled_extent", "extent_from", "soundscape", "species",
                    "confidence", "note"):
            if key not in z:
                rep.error(where, f"missing required key '{key}'")
        if z.get("scene_date") != scene_date:
            rep.error(where, f"scene_date {z.get('scene_date')} disagrees with the manifest's "
                             f"{scene_date}; every july block is stated FOR a date")
        if z.get("habitat") not in (vocab.get("habitats") or []):
            rep.error(where, f"habitat '{z.get('habitat')}' is not declared in the manifest "
                             f"vocabulary")

        # denormalised copies, checked the way the flora manifest's are
        for key, actual in (("habitat", z.get("habitat")),
                            ("in_modelled_extent", z.get("in_modelled_extent")),
                            ("extent_from", z.get("extent_from"))):
            if entry.get(key) != actual:
                rep.error("fauna index", f"zone '{zid}' {key} in the manifest "
                                         f"({entry.get(key)!r}) disagrees with the zone record "
                                         f"({actual!r}); the zone record is authoritative")
        if entry.get("species_count") != len(z.get("species") or []):
            rep.error("fauna index", f"zone '{zid}' species_count {entry.get('species_count')!r} "
                                     f"disagrees with the {len(z.get('species') or [])} species "
                                     f"in the record")

        ext = z.get("extent_from") or {}
        fz = ext.get("flora_zone")
        if fz is None:
            if ext.get("kind") != "water":
                rep.error(where, "extent_from must name a flora_zone whose extent this zone "
                                 "shares, or declare kind 'water'. A fauna zone does not "
                                 "restate a polygon: two datasets describing the same ground in "
                                 "two places drift, and then nobody knows which is the town")
        elif flora_zones and fz not in flora_zones:
            rep.error(where, f"extent_from.flora_zone '{fz}' does not resolve in "
                             f"data/flora/index.json")
        elif fz in flora_zones:
            plantable = flora_zones[fz].get("plantable_in_scene")
            if z.get("in_modelled_extent") != plantable:
                rep.error(where, f"in_modelled_extent is {z.get('in_modelled_extent')!r} but "
                                 f"flora zone '{fz}', whose extent this zone shares, is "
                                 f"plantable_in_scene {plantable!r}. The same ground cannot be "
                                 f"inside the modelled box for one dataset and outside it for "
                                 f"the other")

        # --- the soundscape gate -------------------------------------------
        snd = z.get("soundscape")
        if not isinstance(snd, dict):
            rep.error(where, "soundscape is required: a July zone has to state what it SOUNDS "
                             "like, because most of its animals are audible and not visible")
        else:
            dc = snd.get("dawn_chorus")
            if dc not in FAUNA_DAWN_CHORUS:
                rep.error(where, f"soundscape.dawn_chorus '{dc}' is not one of "
                                 f"{FAUNA_DAWN_CHORUS}. There is no third option: the full dawn "
                                 f"chorus is a spring phenomenon and by 1 July most breeding "
                                 f"passerines have stopped or sharply reduced singing. A zone "
                                 f"cannot declare one")
            if not (snd.get("note") or "").strip():
                rep.error(where, "soundscape needs a note saying what July does to this zone's "
                                 "sound — the reduction is the finding")
            heroes = snd.get("hero") or []
            ids = {s.get("id") for s in z.get("species") or []}
            for h in heroes:
                if h not in ids:
                    rep.error(where, f"soundscape.hero names '{h}', which is not a species in "
                                     f"this zone")

        seen: set = set()
        n_birds = n_full = 0
        for sp in z.get("species") or []:
            if sp.get("id") in seen:
                rep.error(where, f"duplicate species id '{sp.get('id')}' in this zone")
            seen.add(sp.get("id"))
            check_fauna_species(zid, sp, source_ids, vocab, rep, tally)
            if sp.get("class") == "bird":
                n_birds += 1
                if (sp.get("july") or {}).get("vocalization") == "song_full":
                    n_full += 1
        if not seen:
            rep.error(where, "a zone with no species is not a fauna record")
        if n_birds and n_full * 2 > n_birds:
            rep.warn(where, f"{n_full} of {n_birds} birds in this zone are in full song on "
                            f"1 July. That is most of them, and by July most breeding birds "
                            f"have stopped — check each one against its own July biology "
                            f"rather than against the habitat")
        check_attested(where, "zone", z, source_ids, rep)
        zones[zid] = z

    # A species is one animal wherever it appears; a binomial that changes
    # between zones means two records that look like one to any renderer that
    # keys on the id.
    binomials: dict = {}
    for zid, z in zones.items():
        for sp in z.get("species") or []:
            sid, b = sp.get("id"), sp.get("binomial")
            if sid in binomials and binomials[sid][0] != b:
                rep.error(f"fauna zone {zid}/{sid}",
                          f"binomial '{b}' disagrees with '{binomials[sid][0]}' for the same "
                          f"species id in {binomials[sid][1]}")
            binomials.setdefault(sid, (b, zid))

    total = sum(len(z.get("species") or []) for z in zones.values())
    if total:
        heard = sum(1 for z in zones.values() for s in z.get("species") or []
                    if (s.get("july") or {}).get("presence", {}).get("value")
                    if isinstance((s.get("july") or {}).get("presence"), dict))
        unseen = sum(1 for z in zones.values() for s in z.get("species") or []
                     if _fauna_val(s.get("july") or {}, "presence")
                     in ("audible", "trace_only", "not_perceptible"))
        gone = sum(1 for z in zones.values() for s in z.get("species") or []
                   if str(_fauna_val(s.get("july") or {}, "status")).startswith("absent")
                   or _fauna_val(s.get("july") or {}, "status") == "excluded_by_scope")
        rep.note(f"fauna: {len(zones)} zone(s), {total} species record(s); {unseen} present and "
                 f"NOT SEEN (audible, trace or imperceptible), {gone} recorded as absent or "
                 f"withheld — liberty L2 in the data (of {heard} with an attested presence)")
    return zones


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

    check_liberties_coverage(structures, liberties, rep, consumed, unlanded)

    # the vegetation records, and the July phenology rules they have to obey
    check_flora(source_ids, field, rep, tally)

    # the animal records, and the July gate they have to obey — the same
    # argument as the flora phenology, one trophic level up
    check_fauna(source_ids, rep, tally)

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

    # The flora manifest names its own files, and the renderer fetches exactly
    # what it names — no probing — so a zone file that never reached site/ is a
    # 404 on the deployed walkthrough while the dev tree renders perfectly. This
    # is the failure mode publish.sh exists to prevent, checked rather than hoped.
    index_path = FLORA / "index.json"
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text())
        except json.JSONDecodeError:
            return
        wanted = ["index.json"] + [e.get("file") for e in index.get("zones", [])] \
            + [e.get("file") for e in index.get("palettes", [])]
        missing = [w for w in wanted if w and not (site / "data" / "flora" / w).exists()]
        if missing:
            rep.error("site", f"data/flora/ is not fully published: {len(missing)} file(s) "
                              f"the manifest names are absent from site/, starting with "
                              f"{missing[0]} — run tools/publish.sh")
        else:
            rep.note(f"site check: {len(wanted)} flora file(s) published")


if __name__ == "__main__":
    sys.exit(main())
