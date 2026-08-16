#!/usr/bin/env python3
"""Whether a routed woody record can be PLACED — the step after K44's cohort.

ROADMAP K45(a). K44 measured routing: which reader is handed the record. It said
in its own docstring that it does not ask whether a routed record then reaches
the ground, and it named the repair its finding 2 implies —

    "Add `z08_lakeshore` to `TIMBER_ZONES` and the four dune records are drawn
     by the archetypes that already exist."   (docs/LIBERTIES.md L113)

That sentence has two assumptions in it and this file measures both, because
neither is true.

**`TIMBER_ZONES` is a species table, not a placement list.** `trees.js` opens
those four zone files to build one render spec per species — height, crown width,
July foliage, density, confidence — and then throws the zone away. Placement is
`COMMUNITIES`: four hand-written mixes selected by heightfield rules (distance to
water, which land division, a generated relief field), and a stem's species comes
from `pick(mix, rnd())`. A zone's `extent` is never consulted here at all. The
proof is already committed: `z07_bur_oak_savanna`'s declared extent box is
E -2600..-600, N -6400..-4400 — 4.4 km outside the modelled field in the nearest
direction — and its two oaks are drawn anyway, out of the `ridge_oak` mix.

So a woody record reaches a stem only if its species id is in one of those mixes
or is named at an `addTree` call site. **A record whose species is in neither is
routed, archetyped, and selected by nothing** — the same shape of loss K44
measured one level out, and invisible from there for the same reason: K44's
question is answered by the file that receives the record, and this one is
answered by a literal inside it.

**And the woody planter is a fixed box inside a field four times its size.** It
sweeps `-half..+half` in both axes, `half = 320 - step`, while the heightfield
S2e carried east runs E -320..+1700. `flora.js`'s lattice is centred on the
CAMERA and follows the visitor everywhere; the timber does not move. Both
declarations are scanned below rather than restated, because the asymmetry is the
finding and an asymmetry quoted from memory is an anecdote.

**And the weight beside the species id is a FALLBACK.** ROADMAP K45(b1). The
literal in `COMMUNITIES` is documented as *"the dossier's per-species
densities"*, and it is — but `mixes` is rebuilt at load as
`records.density[id] ?? fallback`, and `records.density` is the midpoint of the
first `TIMBER_ZONES` entry that names the species. So the number that places a
stem is ONE GLOBAL FIGURE PER SPECIES, taken from whichever zone comes first in
that list, and the per-community weighting the file writes by hand is overridden
wherever a record carries a band. Both numbers are scanned below and banked side
by side, because a literal that disagrees with what runs is a number a reader
will quote.

    tools/measure_planting_reach.py             print the census
    tools/measure_planting_reach.py --gate      exit 1 on a divergence
    tools/measure_planting_reach.py --self-test break each assertion, in memory
    tools/measure_planting_reach.py --update    rewrite the baseline

FIVE ASSERTIONS.

1.  **(absolute) Every declaration this gate reads is still in the renderer**,
    and `trees.js` still has exactly the banked number of `addTree` call sites.
    A scanner that cannot find its declaration RAISES rather than returning an
    empty set: an empty mix would call every species unselectable and bank it,
    and an unseen third call site would call an unselectable species drawn.

2.  **(absolute, banked, may grow and may not shrink) The woody planter's
    domain.** The half-extent scanned out of the planting loop, the field it
    sits inside, and how many of the heightfield's nodes stand above the
    planter's OWN dry floor inside it and outside it. This is the number a
    lakeshore repair has to move, and banking it means the repair cannot be
    reported as done while the box stands still.

3.  **(absolute, banked both ways) Every woody species a `TIMBER_ZONE`
    contributes, whose form has an archetype, that no community mix and no
    direct call site can select.** New one fails; a banked one that has become
    selectable fails until it is un-banked in the commit that placed it. This is
    the assertion that refuses L113's repair: adding `z08_lakeshore` puts two
    poplars into this bank and draws nothing.

4.  **(absolute, banked both ways) Every zone in `TIMBER_ZONES` that declares an
    extent box, with whether that box meets the woody planter's domain.** `z07`
    is banked as `outside-the-planter` and is drawn regardless, which is the
    routing-is-not-placement fact held in a file instead of in a paragraph.

5.  **(absolute, banked both ways) Every mix entry's literal weight beside the
    weight that actually runs**, and which zone the running one came from. A new
    entry, a departed one or a moved number fails until it is re-banked, so the
    fallback and the record can never drift apart unnoticed. The derivation
    itself is scanned: if `trees.js` stops overriding the literal, or stops
    taking the band's midpoint, this assertion RAISES rather than quietly
    comparing a literal against itself.

THE LIMIT, stated rather than discovered later. `standsDry` is one of several
tests a stem must pass — `terrain.isWater()` is a traced mask, buildings block,
the community classifier returns null over most of the box, and the per-hectare
roll refuses most of what is left. So the land census here is an UPPER bound on
plantable ground, not a count of stems: it answers "could the loop ever visit
this point", which is the question a reach measurement is for. The stems actually
built are `trees.stats`, and they are the smoke's business, not this file's.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import measure_layer_reads as k42      # noqa: E402  (strip_js_comments)
import measure_flora_reach as k44      # noqa: E402  (the cohort this file follows)

DATA = ROOT / "data" / "flora"
TERRAIN = ROOT / "data" / "terrain" / "epochs"
RENDERER = ROOT / "renderers" / "web" / "js"
BASELINE = ROOT / "tools" / "planting_reach_baseline.json"

FLORA_JS = "flora.js"
TREES_JS = "trees.js"

EPOCH = "e1834_harbor_cut"

# Why a routed woody record can never be selected. Named rather than free text,
# for the reason K44 names its own: a bank of reasons is only worth having if two
# runs spell them the same way.
UNSELECTABLE_REASONS = {
    "in-no-community-mix": "its species is in no COMMUNITIES mix and at no addTree call site",
}

# Whether a mix entry's literal weight is the weight that places a stem.
WEIGHT_VERDICTS = {
    "the-literal-runs": "no record in TIMBER_ZONES carries a band for the species, so the "
                        "literal is the weight",
    "the-record-agrees": "a record's band midpoint replaces the literal, and they are the "
                         "same number",
    "the-record-overrides": "a record's band midpoint replaces the literal, and they are "
                            "different numbers",
}

# Whether a zone's declared extent box meets the ground the woody planter sweeps.
BOX_VERDICTS = {
    "meets-the-planter": "the declared box overlaps the swept square",
    "outside-the-planter": "the declared box is wholly outside the swept square",
    "no-box": "the extent declares no box, so it is bounded by its kind alone",
}


# ---------------------------------------------------------------------------
# the renderer, read for its placement declarations
# ---------------------------------------------------------------------------

def renderer_source(name: str) -> str:
    """One renderer file with its comments stripped.

    Stripped for K42's reason and then for one of this file's own: `trees.js`
    discusses `TIMBER_ZONES` and the community mixes in prose at length, and a
    scan that matches its own commentary would find a sycamore in a mix that has
    never held one.
    """
    path = RENDERER / name
    if not path.exists():
        raise LookupError(f"{path.relative_to(ROOT)} is not there — this gate is "
                          f"describing a renderer that no longer exists")
    return k42.strip_js_comments(path.read_text(encoding="utf-8"))


def js_number(src: str, pattern: str, what: str, where: str) -> float:
    m = re.search(pattern, src)
    if not m:
        raise LookupError(f"{where} no longer declares {what} — this gate measures the "
                          f"planter's reach from it, and a missing bound would read as "
                          f"a planter that sweeps everything")
    return float(m.group(1))


def bracketed(src: str, start: int) -> str:
    """The text inside the `[...]` that opens at `start`, brackets balanced.

    A regex cannot do this and a non-greedy one is worse than useless here: the
    mixes are written several lines long with a `],` closing each species pair,
    so `\\[(.*?)\\],` stops two entries in and reports a community that holds a
    quarter of its own species. It did exactly that on the first run of this
    file, and called six placed trees unselectable.
    """
    depth = 0
    for i in range(start, len(src)):
        if src[i] == "[":
            depth += 1
        elif src[i] == "]":
            depth -= 1
            if depth == 0:
                return src[start + 1:i]
    raise LookupError(f"{TREES_JS} has an unclosed `[` at offset {start} — this gate "
                      f"reads a community's species list out of it")


def community_blocks(src: str) -> list[tuple[str, str]]:
    """Each community's key and its block of source, in declaration order."""
    m = re.search(r"const COMMUNITIES\s*=\s*\{(.*?)\n\};", src, re.S)
    if not m:
        raise LookupError(f"{TREES_JS} no longer declares `COMMUNITIES` as an object — "
                          f"every stem's species comes out of it, so an empty one would "
                          f"call the whole town unselectable")
    body = m.group(1)
    keys = [(mm.group(1), mm.start()) for mm in re.finditer(r"^  (\w+):\s*\{", body, re.M)]
    out = []
    for i, (key, start) in enumerate(keys):
        end = keys[i + 1][1] if i + 1 < len(keys) else len(body)
        out.append((key, body[start:end]))
    if not out:
        raise LookupError(f"{TREES_JS} declares no communities this gate can read")
    return out


def mix_entries(block: str, key: str) -> dict[str, list[tuple[str, float]]]:
    """`{ 'mix': [(species, weight), ...], 'edgeMix': [...] }` for one community."""
    lists: dict[str, list[tuple[str, float]]] = {}
    for name in ("mix", "edgeMix"):
        lm = re.search(rf"\b{name}:\s*\[", block)
        if lm:
            inner = bracketed(block, lm.end() - 1)
            lists[name] = [(sp, float(w))
                           for sp, w in re.findall(r"\['(\w+)',\s*([\d.]+)\]", inner)]
    if not lists:
        raise LookupError(f"{TREES_JS} community `{key}` declares no `mix` this gate "
                          f"can read — a community with no readable mix would hide "
                          f"every species it holds")
    return lists


def community_mixes(src: str) -> dict[str, dict[str, list[str]]]:
    """`const COMMUNITIES = { key: { mix: [['id', w], ...], edgeMix: [...] } }`.

    Returns the species ids per community per list. The weights are read by
    `mix_weights` below rather than here: this function's question is whether
    `pick()` can ever return the id at all, which the weight cannot answer —
    the literal beside the id is a fallback, and `records.density` usually
    replaces it (ROADMAP K45(b1)).
    """
    return {key: {name: [sp for sp, _ in entries]
                  for name, entries in mix_entries(block, key).items()}
            for key, block in community_blocks(src)}


def mix_weights(src: str) -> dict[str, dict]:
    """Every mix entry's literal weight, and the zones its community cites.

    The dossier line is read for its `ZONE n` numbers because the literal is a
    PER-COMMUNITY figure — `ulmus_americana` is written 60 in the swamp thicket
    and 12 in the mesic pocket — while the number that runs is one figure per
    species for the whole town. Holding both is what lets the divergence be read
    rather than argued.
    """
    out: dict[str, dict] = {}
    for key, block in community_blocks(src):
        dm = re.search(r"dossier:\s*'([^']*)'", block)
        if not dm:
            raise LookupError(f"{TREES_JS} community `{key}` no longer carries a `dossier` "
                              f"line — it is where the literal weights say they come from, "
                              f"and this gate reports the divergence against it")
        out[key] = {
            "dossier_zones": sorted(set(re.findall(r"ZONE (\d+)", dm.group(1)))),
            "lists": mix_entries(block, key),
        }
    return out


def archetype_fallback(src: str) -> tuple[set[str], str]:
    """`SPECIES`' own keys, and the id every other species is drawn as.

    `loadTimberZones` builds a spec as `SPECIES[sp.id] ?? SPECIES.<fallback>`,
    so a placed species with no entry of its own is drawn with another species'
    bole fraction, taper, puff count and BARK COLOUR — silently, and with its
    `fromRecord` flag still true. The fallback id is scanned rather than named
    here for the usual reason: a gate that hard-codes it would keep reporting
    the elm after somebody changed it.
    """
    m = re.search(r"const SPECIES\s*=\s*\{(.*?)\n\};", src, re.S)
    if not m:
        raise LookupError(f"{TREES_JS} no longer declares `SPECIES` as an object — it is "
                          f"the draw archetype every stem is built from, and a missing one "
                          f"would report the whole town as drawn from a fallback")
    keys = set(re.findall(r"^  (\w+):\s*\{", m.group(1), re.M))
    fm = re.search(r"SPECIES\[sp\.id\]\s*\?\?\s*SPECIES\.(\w+)", src)
    if not fm:
        raise LookupError(f"{TREES_JS} no longer falls back to a default archetype as "
                          f"`SPECIES[sp.id] ?? SPECIES.<id>` — this gate reports which "
                          f"placed species are drawn as something else, and cannot say "
                          f"which one they are drawn as without that line")
    if fm.group(1) not in keys:
        raise LookupError(f"{TREES_JS} falls back to `SPECIES.{fm.group(1)}`, which is not "
                          f"a key of SPECIES — every species without its own entry would "
                          f"be drawn from `undefined`")
    return keys, fm.group(1)


def timber_zone_order(src: str) -> list[str]:
    """`TIMBER_ZONES` in DECLARATION order, which `k44.js_array` discards.

    The order is load-bearing for assertion 5 and for nothing else in this file:
    `loadTimberZones` writes `density[sp.id]` only `if (!(sp.id in density))`, so
    a species named by two zones takes its weight from whichever is listed first
    — z05's band for five of the species the swamp thicket and the mesic pocket
    weight by hand.
    """
    m = re.search(r"const TIMBER_ZONES\s*=\s*\[(.*?)\];", src, re.S)
    if not m:
        raise LookupError(f"{TREES_JS} no longer declares `TIMBER_ZONES` as an array — "
                          f"assertion 5 resolves a species' running weight by walking it "
                          f"in order")
    return re.findall(r"'([^']*)'", m.group(1))


def record_density_rule(src: str) -> None:
    """Raise unless `trees.js` still overrides the literal with the record's midpoint.

    Assertion 5 compares a fallback against the weight that replaces it. If the
    replacement goes away the comparison becomes a literal against itself, which
    is the shape of gate that passes for years while measuring nothing — so the
    two lines that make the claim true are scanned, not assumed.
    """
    if not re.search(r"density\[sp\.id\]\s*=\s*\(perHa\[0\]\s*\+\s*perHa\[1\]\)\s*/\s*2;", src):
        raise LookupError(f"{TREES_JS} no longer takes a species' running weight as the "
                          f"MIDPOINT of its recorded band — assertion 5 compares the "
                          f"literal in COMMUNITIES against that number and cannot derive "
                          f"it any other way")
    if not re.search(r"records\.density\[id\]\s*\?\?\s*fallback", src):
        raise LookupError(f"{TREES_JS} no longer rebuilds the community mixes as "
                          f"`records.density[id] ?? fallback` — the literal weights would "
                          f"then be the weights, and assertion 5 would be comparing a "
                          f"number with itself")


def direct_call_sites(src: str) -> tuple[int, set[str]]:
    """How many `addTree` call sites the module has, and the ids named at them.

    Two paths select a spec today: `specs.salix_interior` at the point-bar
    thicket, and `specs[id]` where `id` came from `pick()`. The COUNT is banked
    because a third path is exactly how this gate would go quietly wrong — an
    unselectable species drawn by a call site nobody told this file about.
    """
    sites = len(re.findall(r"\baddTree\(", src)) - len(re.findall(r"function addTree\(", src))
    named = set(re.findall(r"\bspecs\.(\w+)\b", src))
    return sites, named


def planter_bounds(src: str) -> dict:
    """The woody planting loop's fixed square, and the steps that size it."""
    half_const = js_number(src, r"const half\s*=\s*([\d.]+)\s*-\s*step;",
                           "the planting loop's half-extent", TREES_JS)
    steps = [float(v) for v in re.findall(r"step:\s*([\d.]+),", src)]
    if not steps:
        raise LookupError(f"{TREES_JS} no longer declares the STEMS planting steps — the "
                          f"swept square is `half_const - step` and cannot be sized "
                          f"without them")
    if not re.search(r"for \(let n = -half; n <= half; n \+= step\)", src):
        raise LookupError(f"{TREES_JS}'s planting loop no longer sweeps -half..+half — "
                          f"this gate's whole domain claim is read off that loop")
    dry_margin = js_number(src, r"const TREE_DRY_MARGIN_M\s*=\s*([\d.]+);",
                           "TREE_DRY_MARGIN_M", TREES_JS)
    return {
        "half_const_m": half_const,
        "steps_m": sorted(steps),
        # The widest sweep is the smallest step, which is the `full` detail
        # level. Banking the widest is banking the most generous case: a repair
        # that has to move this number cannot be reported done at `light`.
        "half_m": round(half_const - min(steps), 3),
        "dry_margin_m": dry_margin,
    }


def herbaceous_is_camera_centred(src: str) -> bool:
    """`flora.js` builds its lattice around the camera, not around the origin.

    Scanned, because this is the other half of the asymmetry and an asymmetry one
    side of which is assumed is half a measurement.
    """
    return bool(re.search(r"Math\.floor\(\(camE - radius\) / cell\)", src)
                and re.search(r"Math\.ceil\(\(camE \+ radius\) / cell\)", src))


def declarations() -> dict:
    trees = renderer_source(TREES_JS)
    flora = renderer_source(FLORA_JS)
    sites, named = direct_call_sites(trees)
    if not herbaceous_is_camera_centred(flora):
        raise LookupError(f"{FLORA_JS} no longer builds its lattice around the camera — "
                          f"this gate's claim that the sward follows the visitor and the "
                          f"timber does not is read off that lattice")
    mixes = community_mixes(trees)
    record_density_rule(trees)
    archetypes, fallback_id = archetype_fallback(trees)
    selectable = {sp for c in mixes.values() for lst in c.values() for sp in lst}
    return {
        "source": trees,
        "weights": mix_weights(trees),
        "archetypes": archetypes,
        "archetype_fallback": fallback_id,
        "zones": k44.js_array(trees, "TIMBER_ZONES", TREES_JS),
        "forms": k44.js_object_keys(trees, "FORM_OF", TREES_JS),
        "roles": k44.js_role_guard(trees, TREES_JS),
        "communities": mixes,
        "zone_order": timber_zone_order(trees),
        "call_sites": sites,
        "named_at_call_sites": named,
        "selectable": selectable | named,
        "planter": planter_bounds(trees),
    }


# ---------------------------------------------------------------------------
# the ground, read for what the planter can visit
# ---------------------------------------------------------------------------

def heightfield() -> dict:
    meta = json.loads((TERRAIN / EPOCH / "heightfield.json").read_text(encoding="utf-8"))
    raw = (TERRAIN / EPOCH / "heightfield.bin").read_bytes()
    n = meta["cols"] * meta["rows"]
    if meta.get("encoding") != "int16" or len(raw) != n * 2:
        raise LookupError("the heightfield is no longer the int16 grid this gate reads")
    meta["_samples"] = struct.unpack(f"<{n}h", raw)
    return meta


def land_census(hf: dict, half: float, dry_margin: float) -> dict:
    """How many heightfield nodes stand above the planter's own dry floor, and
    how they split across the boundary of the square it sweeps."""
    cols, rows, cell = hf["cols"], hf["rows"], hf["cell_m"]
    e0, n0 = hf["origin_e"], hf["origin_n"]
    scale, off = hf["scale"], hf["offset"]
    floor = hf.get("water_surface_m", 0.0) + dry_margin
    s = hf["_samples"]
    inside = outside = 0
    for r in range(rows):
        n = n0 + r * cell
        in_n = -half <= n <= half
        for c in range(cols):
            if s[r * cols + c] * scale + off < floor:
                continue
            e = e0 + c * cell
            if in_n and -half <= e <= half:
                inside += 1
            else:
                outside += 1
    total = inside + outside
    ha = cell * cell / 10000.0
    return {
        "dry_floor_m": round(floor, 3),
        "nodes_above_floor": total,
        "inside_planter": inside,
        "outside_planter": outside,
        "inside_pct": round(100.0 * inside / total, 2) if total else 0.0,
        "outside_ha": round(outside * ha, 1),
        "field_e_m": [e0, e0 + (cols - 1) * cell],
        "field_n_m": [n0, n0 + (rows - 1) * cell],
    }


# ---------------------------------------------------------------------------
# the data, asked whether it can be selected
# ---------------------------------------------------------------------------

def boxes_overlap(box: dict, half: float) -> bool:
    be = box.get("e")
    bn = box.get("n")
    if be and (be[1] < -half or be[0] > half):
        return False
    if bn and (bn[1] < -half or bn[0] > half):
        return False
    return True


def running_density(dec: dict, zones_read, records: dict[str, dict]) -> dict[str, tuple[float, str]]:
    """`loadTimberZones`'s `density` table, re-derived here rather than assumed.

    Same three guards, in the same order and for the same reason the renderer
    has them: a role it does not take is skipped, a form it cannot draw is
    skipped BEFORE the density is written, and the first zone to name a species
    keeps it. A re-derivation that got any of those wrong would report a
    divergence the renderer does not have.
    """
    order = ([z for z in dec["zone_order"] if z in zones_read]
             + sorted(set(zones_read) - set(dec["zone_order"])))
    density: dict[str, tuple[float, str]] = {}
    for zid in order:
        for sp in records[zid].get("species", []):
            if sp.get("role") not in dec["roles"]:
                continue
            if sp.get("form") not in dec["forms"]:
                continue
            band = (sp.get("abundance") or {}).get("density_per_ha")
            if isinstance(band, list) and len(band) == 2 and sp["id"] not in density:
                density[sp["id"]] = ((band[0] + band[1]) / 2, zid)
    return density


def weight_census(dec: dict, density: dict[str, tuple[float, str]]) -> dict[str, dict]:
    """Every mix entry, with the literal beside the weight that replaces it."""
    out: dict[str, dict] = {}
    for key, comm in sorted(dec["weights"].items()):
        for name, entries in sorted(comm["lists"].items()):
            for sp, literal in entries:
                run = density.get(sp)
                if run is None:
                    verdict, running, source = "the-literal-runs", literal, None
                else:
                    running, source = run
                    verdict = ("the-record-agrees" if running == literal
                               else "the-record-overrides")
                out[f"{key}.{name}.{sp}"] = {
                    "literal": literal,
                    "running": running,
                    "from_zone": source,
                    "verdict": verdict,
                    "dossier_zones": comm["dossier_zones"],
                }
    return out


def measure(dec: dict | None = None, timber_zones: set[str] | None = None) -> tuple[dict, list[str]]:
    dec = dec or declarations()
    zones_read = timber_zones if timber_zones is not None else dec["zones"]
    manifest = json.loads((DATA / "index.json").read_text(encoding="utf-8"))
    hf = heightfield()
    half = dec["planter"]["half_m"]

    contributed: dict[str, list[str]] = {}
    unimplemented: dict[str, list[str]] = {}
    zone_boxes: dict[str, dict] = {}
    zone_records: dict[str, dict] = {}
    for entry in manifest.get("zones", []):
        zid = entry["id"]
        rec = json.loads((DATA / entry["file"]).read_text(encoding="utf-8"))
        zone_records[zid] = rec
        if zid in zones_read:
            box = (rec.get("extent") or {}).get("box")
            if box:
                verdict = ("meets-the-planter" if boxes_overlap(box, half)
                           else "outside-the-planter")
            else:
                verdict = "no-box"
            zone_boxes[zid] = {"verdict": verdict,
                               "box": {"e": box.get("e"), "n": box.get("n")} if box else None}
        for sp in rec.get("species", []):
            if sp.get("role") not in dec["roles"]:
                continue
            if zid not in zones_read:
                continue
            target = contributed if sp.get("form") in dec["forms"] else unimplemented
            target.setdefault(sp["id"], []).append(zid)

    unselectable = {
        sp: {"zones": sorted(set(zs)), "reason": "in-no-community-mix"}
        for sp, zs in sorted(contributed.items())
        if sp not in dec["selectable"]
    }
    weights = weight_census(dec, running_density(dec, zones_read, zone_records))
    # A species that can be selected but has no archetype of its own is drawn as
    # another species. It is the sycamore today, and it is the shape of thing
    # this file exists to refuse to leave implicit: assertion 3 counts a placed
    # record as reached, and "reached" here means drawn with the American elm's
    # bole, taper, puff count and bark (docs/LIBERTIES.md L116).
    drawn_as = {
        sp: dec["archetype_fallback"]
        for sp in sorted(dec["selectable"])
        if sp not in dec["archetypes"] and sp in contributed
    }

    state = {
        "planter": {
            **{k: v for k, v in dec["planter"].items() if k != "steps_m"},
            "steps_m": dec["planter"]["steps_m"],
            "call_sites": dec["call_sites"],
        },
        "ground": land_census(hf, half, dec["planter"]["dry_margin_m"]),
        "zones_read": sorted(zones_read),
        "zone_boxes": zone_boxes,
        "communities": {k: sorted({sp for lst in v.values() for sp in lst})
                        for k, v in sorted(dec["communities"].items())},
        "contributed": {k: sorted(set(v)) for k, v in sorted(contributed.items())},
        "unimplemented_form": {k: sorted(set(v)) for k, v in sorted(unimplemented.items())},
        "unselectable": unselectable,
        "drawn_as_another_species": drawn_as,
        "weights": weights,
    }
    problems: list[str] = []
    for entry, w in weights.items():
        if w["literal"] <= 0:
            problems.append(f"the mix entry {entry} is weighted {w['literal']} — `pick()` "
                            f"walks a cumulative sum and can never return a zero-weighted "
                            f"id, so it is in a mix and selectable by nothing, which is "
                            f"the fault assertion 3 exists to catch wearing a disguise")
    if not state["contributed"]:
        problems.append("no woody record is routed to the timber reader at all — the "
                        "scan found nothing, which is a broken gate rather than a town "
                        "without trees")
    return state, problems


# ---------------------------------------------------------------------------
# the assertions
# ---------------------------------------------------------------------------

def evaluate(state: dict, bank: dict) -> list[str]:
    out: list[str] = []

    # 1 — the declarations are still there. The scanners raise on absence, so
    # what is left to assert here is the call-site count: a path this file cannot
    # see would call a drawn species unselectable.
    if state["planter"]["call_sites"] != bank["planter"]["call_sites"]:
        out.append(f"trees.js has {state['planter']['call_sites']} addTree call site(s), "
                   f"and this gate accounts for {bank['planter']['call_sites']}. A new "
                   f"selection path has to be read into `direct_call_sites` before the "
                   f"unselectable bank below means anything")

    # 2 — the planter's domain. It may GROW: that is what a repair looks like.
    b, s = bank["planter"], state["planter"]
    for key in ("half_const_m", "half_m", "dry_margin_m"):
        if s[key] != b[key]:
            direction = "widened" if s[key] > b[key] else "narrowed"
            note = (" — re-bank it with --update in the commit that widened it"
                    if s[key] > b[key] else "")
            out.append(f"the woody planter's {key} {direction}: {b[key]} -> {s[key]}{note}")
    bg, sg = bank["ground"], state["ground"]
    if sg["field_e_m"] != bg["field_e_m"] or sg["field_n_m"] != bg["field_n_m"]:
        out.append(f"the modelled field moved: E {bg['field_e_m']} N {bg['field_n_m']} -> "
                   f"E {sg['field_e_m']} N {sg['field_n_m']} — the reach fraction below is "
                   f"a fraction OF this field and has to be re-banked with it")
    if sg["inside_planter"] < bg["inside_planter"]:
        out.append(f"the woody planter reaches less ground than it did: "
                   f"{bg['inside_planter']} -> {sg['inside_planter']} node(s) above its "
                   f"own dry floor. The reach may grow and may not shrink")
    elif sg["inside_planter"] > bg["inside_planter"]:
        out.append(f"the woody planter reaches MORE ground than it did: "
                   f"{bg['inside_planter']} -> {sg['inside_planter']} node(s). That is a "
                   f"repair — re-bank it with --update in the same commit, so the "
                   f"lakeshore question is answered by a number rather than by a claim")

    # 3 — the species no mix can select, exact in both directions.
    sb, bb = state["unselectable"], bank["unselectable"]
    for sp in sorted(set(sb) - set(bb)):
        out.append(f"{sp} is routed to the timber reader by "
                   f"{', '.join(sb[sp]['zones'])}, its form has an archetype, and no "
                   f"community mix or addTree call site can select it — so it is "
                   f"committed, cited and drawn nowhere. Give it a mix entry, or bank "
                   f"it here with --update and say why in docs/LIBERTIES.md")
    for sp in sorted(set(bb) - set(sb)):
        out.append(f"{sp} is banked as selectable by nothing and no longer is — un-bank "
                   f"it with --update in the commit that placed it, so a repair is "
                   f"recorded rather than absorbed")
    for sp in sorted(set(sb) & set(bb)):
        if sb[sp]["zones"] != bb[sp]["zones"] or sb[sp]["reason"] != bb[sp]["reason"]:
            out.append(f"{sp}'s unselectable entry moved: {bb[sp]} -> {sb[sp]}")

    # 4 — the zones routed to the timber reader, and where their ground is.
    sz, bz = state["zone_boxes"], bank["zone_boxes"]
    for zid in sorted(set(sz) - set(bz)):
        out.append(f"{zid} is newly routed to the timber reader and its extent "
                   f"{BOX_VERDICTS[sz[zid]['verdict']]}. Routing is not placement: bank "
                   f"it with --update and read ROADMAP K45(a) before calling it drawn")
    for zid in sorted(set(bz) - set(sz)):
        out.append(f"{zid} is banked as a timber zone and is no longer routed to "
                   f"trees.js — re-bank with --update")
    for zid in sorted(set(sz) & set(bz)):
        if sz[zid]["verdict"] != bz[zid]["verdict"]:
            out.append(f"{zid}'s extent moved relative to the planter: "
                       f"{bz[zid]['verdict']} -> {sz[zid]['verdict']}")

    # 3b — placed, and drawn as something else. Exact both ways, for assertion
    # 3's own reason: a species with no archetype is not "drawn nowhere", it is
    # drawn wearing another species' bark, which is a claim about the town.
    sd, bd = state["drawn_as_another_species"], bank.get("drawn_as_another_species", {})
    for sp in sorted(set(sd) - set(bd)):
        out.append(f"{sp} can be selected and has no `SPECIES` archetype of its own, so it "
                   f"is drawn with {sd[sp]}'s bole, taper, puff count and bark. Give it an "
                   f"entry, or bank it with --update and record the substitution in "
                   f"docs/LIBERTIES.md")
    for sp in sorted(set(bd) - set(sd)):
        out.append(f"{sp} is banked as drawn with another species' archetype and no longer "
                   f"is — un-bank it with --update in the commit that gave it its own")
    for sp in sorted(set(sd) & set(bd)):
        if sd[sp] != bd[sp]:
            out.append(f"{sp} is now drawn as {sd[sp]} where it was drawn as {bd[sp]}")

    # 5 — the literal weight beside the weight that runs, exact both ways. The
    # bank is what stops a mix entry being written to one number and read as
    # another: seventeen of the twenty-six already are, and a reader who quotes
    # the file gets the wrong figure for every one of them (ROADMAP K45(b1)).
    if "weights" not in bank:
        out.append("the baseline predates assertion 5 and holds no mix weights at all — "
                   "run --update once to bank the literal and the running weight for "
                   "every entry")
        return out
    sw, bw = state["weights"], bank["weights"]
    for e in sorted(set(sw) - set(bw)):
        w = sw[e]
        out.append(f"{e} is a mix entry this gate has never banked: literal {w['literal']}, "
                   f"and what places a stem is {w['running']}"
                   + (f" (the midpoint of the band {w['from_zone']} records)"
                      if w["from_zone"] else " (no record carries a band for it)")
                   + ". Re-bank with --update in the commit that added it")
    for e in sorted(set(bw) - set(sw)):
        out.append(f"{e} is banked as a mix entry and is no longer one — un-bank it with "
                   f"--update in the commit that removed it, so a species leaving the "
                   f"scene is recorded rather than absorbed")
    for e in sorted(set(sw) & set(bw)):
        s, b = sw[e], bw[e]
        for field in ("literal", "running", "from_zone", "verdict", "dossier_zones"):
            if s[field] != b[field]:
                out.append(f"{e}'s {field} moved: {b[field]} -> {s[field]}. The literal is a "
                           f"fallback and `records.density` is what runs — re-bank with "
                           f"--update and say in the commit which of the two you meant to "
                           f"move")
                break
    return out


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------

def print_census(state: dict) -> None:
    p, g = state["planter"], state["ground"]
    print("WHERE THE WOODY PLANTER CAN PUT A STEM")
    print(f"  the swept square   E/N -{p['half_m']:.1f}..+{p['half_m']:.1f} m "
          f"(`half = {p['half_const_m']:.0f} - step`, steps "
          f"{'/'.join(f'{s:g}' for s in p['steps_m'])})")
    print(f"  the modelled field E {g['field_e_m'][0]:.0f}..{g['field_e_m'][1]:.0f}  "
          f"N {g['field_n_m'][0]:.0f}..{g['field_n_m'][1]:.0f} m")
    print(f"  ground above the planter's own dry floor ({g['dry_floor_m']:.2f} m): "
          f"{g['nodes_above_floor']} node(s)")
    print(f"    inside the square   {g['inside_planter']:>7} ({g['inside_pct']:.2f} %)")
    print(f"    outside it          {g['outside_planter']:>7} "
          f"({100 - g['inside_pct']:.2f} %, {g['outside_ha']:.1f} ha the timber layer "
          f"never visits)")
    print(f"  flora.js's lattice is centred on the camera and has no such bound.")

    print("\nTHE TIMBER READER'S ZONES, AND WHERE THEIR GROUND IS")
    for zid, z in sorted(state["zone_boxes"].items()):
        box = z["box"]
        where = (f"box E {box['e']} N {box['n']}" if box else "no box")
        print(f"  {zid:<24} {z['verdict']:<20} {where}")
    print("  (a zone's extent is read by flora.js and never by trees.js: the timber "
          "reader\n   takes species parameters out of these files and places from "
          "COMMUNITIES)")

    print("\nWHAT EACH COMMUNITY CAN SELECT")
    for key, ids in state["communities"].items():
        print(f"  {key:<14} {len(ids):>2}  {', '.join(ids)}")

    w = state["weights"]
    overridden = [e for e, v in w.items() if v["verdict"] == "the-record-overrides"]
    print(f"\nTHE WEIGHT BESIDE EACH SPECIES, AND THE WEIGHT THAT PLACES IT — "
          f"{len(overridden)} of {len(w)} differ")
    print(f"  {'entry':<48}{'literal':>8}{'runs':>8}  from")
    for e, v in w.items():
        mark = "  <-" if v["verdict"] == "the-record-overrides" else ""
        print(f"  {e:<48}{v['literal']:>8.1f}{v['running']:>8.1f}  "
              f"{v['from_zone'] or 'the literal':<24}{mark}")
    print("  (the literal is a FALLBACK: `mixes` is rebuilt at load as "
          "`records.density[id] ?? fallback`,\n   and `records.density` is the midpoint of "
          "the band in the FIRST TIMBER_ZONE naming the\n   species — one figure per "
          "species for the whole town, whatever a community writes)")

    print(f"\nROUTED, ARCHETYPED, AND SELECTED BY NOTHING — "
          f"{len(state['unselectable'])} of {len(state['contributed'])}")
    for sp, e in state["unselectable"].items():
        print(f"  {sp:<28} {UNSELECTABLE_REASONS[e['reason']]}")
        print(f"  {'':<28} routed by {', '.join(e['zones'])}")
    if state["drawn_as_another_species"]:
        print("\nPLACED, AND DRAWN AS ANOTHER SPECIES")
        for sp, as_id in state["drawn_as_another_species"].items():
            print(f"  {sp:<28} no `SPECIES` archetype: drawn with {as_id}'s bole, taper, "
                  f"puffs and bark")

    if state["unimplemented_form"]:
        print(f"\n  (and {len(state['unimplemented_form'])} woody record(s) whose form has "
              f"no archetype at all,\n   which is K44's bank rather than this one: "
              f"{', '.join(state['unimplemented_form'])})")


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

def self_test() -> int:
    state, _ = measure()
    bank = json.loads(BASELINE.read_text(encoding="utf-8"))
    clean = evaluate(state, bank)
    print("SELF-TEST — each case must FIRE")
    if clean:
        print("  note: the clean tree already reports:")
        for c in clean:
            print(f"    {c}")

    cases: list[tuple[str, dict, dict]] = []

    s1 = copy.deepcopy(state)
    s1["planter"]["call_sites"] += 1
    cases.append(("1 a third addTree call site this gate cannot read", s1, bank))

    s2 = copy.deepcopy(state)
    s2["planter"]["half_m"] = 900.0
    cases.append(("2 the swept square widened and not re-banked", s2, bank))

    s2b = copy.deepcopy(state)
    s2b["ground"]["inside_planter"] -= 1
    cases.append(("2 the planter reaching less ground than it did", s2b, bank))

    s2c = copy.deepcopy(state)
    s2c["ground"]["field_e_m"] = [-320.0, 2400.0]
    cases.append(("2 the field extended east under a fixed planter", s2c, bank))

    s3 = copy.deepcopy(state)
    s3["unselectable"]["quercus_alba"] = {"zones": ["z07_bur_oak_savanna"],
                                          "reason": "in-no-community-mix"}
    cases.append(("3 a species newly selectable by nothing", s3, bank))

    b3 = copy.deepcopy(bank)
    b3["unselectable"]["a_species_that_left"] = {"zones": ["z05_riverbank_timber"],
                                                 "reason": "in-no-community-mix"}
    cases.append(("3 a banked unselectable species that has been placed", state, b3))

    if state["unselectable"]:
        b3z = copy.deepcopy(bank)
        first = sorted(state["unselectable"])[0]
        b3z["unselectable"][first] = {**b3z["unselectable"][first],
                                      "zones": ["z10_settled_town"]}
        cases.append(("3 a banked species whose routing moved", state, b3z))

    s3d = copy.deepcopy(state)
    s3d["drawn_as_another_species"]["quercus_alba"] = "ulmus_americana"
    cases.append(("3b a placed species newly drawn with another's archetype", s3d, bank))

    b3d = copy.deepcopy(bank)
    b3d["drawn_as_another_species"] = {}
    cases.append(("3b a banked substitution that has been given its own archetype",
                  state, b3d))

    s4 = copy.deepcopy(state)
    s4["zone_boxes"]["z09_sand_prairie"] = {"verdict": "outside-the-planter",
                                            "box": {"e": [840, 1400], "n": [-400, 400]}}
    cases.append(("4 a zone newly routed to the timber reader", s4, bank))

    s4b = copy.deepcopy(state)
    s4b["zone_boxes"]["z07_bur_oak_savanna"]["verdict"] = "meets-the-planter"
    cases.append(("4 a banked zone whose extent moved onto the planter", s4b, bank))

    s5 = copy.deepcopy(state)
    first_entry = sorted(state["weights"])[0]
    s5["weights"][first_entry]["literal"] += 3
    cases.append(("5 a mix entry's literal weight edited and not re-banked", s5, bank))

    s5b = copy.deepcopy(state)
    s5b["weights"]["gallery.mix.a_species_added_to_the_mix"] = {
        "literal": 1.0, "running": 1.0, "from_zone": None,
        "verdict": "the-literal-runs", "dossier_zones": ["5"]}
    cases.append(("5 a species added to a mix and not banked", s5b, bank))

    b5 = copy.deepcopy(bank)
    b5["weights"]["gallery.mix.a_species_that_left"] = {
        "literal": 4.0, "running": 4.0, "from_zone": None,
        "verdict": "the-literal-runs", "dossier_zones": ["5"]}
    cases.append(("5 a banked mix entry that has been removed", state, b5))

    b5r = copy.deepcopy(bank)
    b5r["weights"][first_entry] = {**b5r["weights"][first_entry], "running": 99.0,
                                   "verdict": "the-record-overrides"}
    cases.append(("5 a record's band edited under a fixed literal", state, b5r))

    # THE CASE THIS HALF OF THE PARCEL EXISTS FOR, and it is K45(a)'s move
    # applied to K45(b)'s own prescription. ROADMAP K45(b) and docs/LIBERTIES.md
    # L114 both say the sycamore is "a one-line mix entry weighted at the density
    # its own record carries", and K45(b) writes that line out as
    # `['platanus_occidentalis', 1]`. Weighted at 1 the literal disagrees with
    # the 2 that would place it, so the entry ships as a third dead number.
    s5c = copy.deepcopy(state)
    syc = s5c["weights"].get("gallery.mix.platanus_occidentalis")
    if syc:
        s5c["weights"]["gallery.mix.platanus_occidentalis"] = {
            **syc, "literal": 1.0, "verdict": "the-record-overrides"}
        cases.append(("5 K45(b)'s prescribed ['platanus_occidentalis', 1] — the literal "
                      "disagreeing with the 2 that runs", s5c, bank))

    # THE CASE THIS PARCEL EXISTS FOR. docs/LIBERTIES.md L113 and ROADMAP K45
    # both say the lakeshore's four dune records are repaired by adding the zone
    # to `TIMBER_ZONES`. Applied here in memory, against the real tree: two of
    # the four already take their spec from `z05_riverbank_timber` and first
    # zone wins, and the other two land in the unselectable bank because no
    # community mix holds a poplar. The repair draws nothing, and this is where
    # that is measured rather than argued.
    dec = declarations()
    l113, _ = measure(dec, timber_zones=dec["zones"] | {"z08_lakeshore"})
    cases.append(("K45(a) L113's repair — z08_lakeshore added to TIMBER_ZONES",
                  l113, bank))

    ok = True
    for label, s, b in cases:
        fired = len(evaluate(s, b)) > len(clean)
        print(f"  {'fires' if fired else 'SILENT'}  {label}")
        ok = ok and fired

    added = sorted(set(l113["unselectable"]) - set(state["unselectable"]))
    print(f"  …and it adds {len(added)} species to the unselectable bank: "
          f"{', '.join(added) or 'none'}")
    print(f"  …while the planter's reach is unchanged at "
          f"{l113['ground']['inside_planter']} node(s), and z08_lakeshore's own extent "
          f"box is {BOX_VERDICTS[l113['zone_boxes']['z08_lakeshore']['verdict']]}")

    # The scanners are the load-bearing half of assertion 1: each must be able to
    # say yes AND no. A scanner that silently returns nothing would call every
    # species unselectable and bank the lot.
    src = dec["source"]
    checks = [
        ("the community scanner finds the four mixes",
         set(dec["communities"]) == {"gallery", "wet_woods", "mesic_pocket", "ridge_oak"}),
        ("…and reads the gallery's edge mix as well as its mix",
         "salix_nigra" in dec["communities"]["gallery"]["edgeMix"]),
        ("…and reads a multi-line mix to its END, not to its second entry",
         {"juglans_nigra", "salix_amygdaloides"}
         <= set(dec["communities"]["gallery"]["mix"])),
        ("the community scanner refuses a renderer with no COMMUNITIES",
         raises(lambda: community_mixes("const NOTHING = 1;"))),
        ("the direct call site scan finds the point-bar thicket",
         "salix_interior" in dec["named_at_call_sites"]),
        ("the call sites are counted, not assumed", dec["call_sites"] >= 2),
        ("the planter's half-extent is read off the loop",
         dec["planter"]["half_const_m"] == 320.0),
        ("the bound scanner refuses a loop that no longer sweeps a square",
         raises(lambda: planter_bounds(src.replace(
             "for (let n = -half; n <= half; n += step)", "for (const n of everywhere)")))),
        ("the bound scanner refuses a renderer with no half-extent",
         raises(lambda: planter_bounds("const STEMS = { full: { step: 4.0 } };"))),
        ("flora.js's lattice is read as camera-centred",
         herbaceous_is_camera_centred(renderer_source(FLORA_JS))),
        ("…and a lattice that stopped following the camera is refused",
         not herbaceous_is_camera_centred("const c0 = Math.floor((0 - radius) / cell);")),
        ("a species in a mix is selectable",
         "quercus_macrocarpa" in dec["selectable"]),
        # The mix scanner's negative used to be the sycamore, which K45(b1)
        # placed. A gate whose only proof that a scanner can say no is a species
        # somebody is about to plant stops proving it the day the repair lands,
        # so the negative is synthetic now and cannot be repaired out from under
        # this file.
        ("a species in no mix is not",
         "platanus_occidentalis" not in {
             sp for c in community_mixes(
                 "const COMMUNITIES = {\n  gallery: {\n"
                 "    mix: [['ulmus_americana', 1]],\n  },\n};").values()
             for lst in c.values() for sp in lst}),
        ("the weight scanner reads every mix entry in the file",
         len(weight_census(dec, {})) == sum(
             len(v) for c in dec["weights"].values() for v in c["lists"].values())),
        # Synthetic, so that it cannot be satisfied by whichever species happens
        # to sit last in the real gallery today: the bug this guards against is
        # a non-greedy `\[(.*?)\],` stopping at the first line break, and the
        # only honest control for it is a list that HAS a line break in it.
        ("…and reads a multi-line mix to its last weight, not to its second",
         mix_entries("  x: {\n    mix: [\n      ['a', 1], ['b', 2],\n"
                     "      ['c', 3],\n    ],\n  },\n", "x")["mix"]
         == [("a", 1.0), ("b", 2.0), ("c", 3.0)]),
        ("…and each community's dossier still says which ZONE its literals came from",
         all(c["dossier_zones"] for c in dec["weights"].values())),
        ("…and refuses a community that no longer says",
         raises(lambda: mix_weights(re.sub(r"dossier: '", "dossierWas: '", src)))),
        ("the running weight is re-derived in TIMBER_ZONES order",
         dec["zone_order"][0] == "z05_riverbank_timber"
         and set(dec["zone_order"]) == dec["zones"]),
        ("the archetype table and its fallback are read off the renderer",
         archetype_fallback(src)[1] in archetype_fallback(src)[0]),
        ("…and a fallback to an archetype that is not in the table is refused",
         raises(lambda: archetype_fallback(
             src.replace("SPECIES[sp.id] ?? SPECIES.ulmus_americana",
                         "SPECIES[sp.id] ?? SPECIES.no_such_tree")))),
        ("the override rule is scanned out of the renderer, not assumed",
         record_density_rule(src) is None),
        ("…and a renderer that stopped overriding the literal is refused",
         raises(lambda: record_density_rule(
             src.replace("records.density[id] ?? fallback", "fallback")))),
        ("…and one that stopped taking the band's midpoint is refused",
         raises(lambda: record_density_rule(
             src.replace("density[sp.id] = (perHa[0] + perHa[1]) / 2;",
                         "density[sp.id] = perHa[0];")))),
        ("the heightfield is the int16 grid this gate reads",
         heightfield()["cols"] > 0),
    ]
    for label, passed in checks:
        print(f"  {'ok   ' if passed else 'FAIL '}  {label}")
        ok = ok and passed

    print("SELF-TEST PASS" if ok else "SELF-TEST FAIL")
    return 0 if ok else 1


def raises(fn) -> bool:
    try:
        fn()
    except LookupError:
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", action="store_true", help="exit 1 on a divergence")
    ap.add_argument("--quiet", action="store_true", help="print only the verdict")
    ap.add_argument("--self-test", action="store_true",
                    help="break each assertion in memory and check that it fires")
    ap.add_argument("--update", action="store_true", help="rewrite the baseline")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    state, problems = measure()

    if args.update:
        BASELINE.write_text(json.dumps({
            "_doc": "Whether a routed woody record can be PLACED. K44 measured which "
                    "reader receives a record; trees.js receives one and then selects a "
                    "species out of a hand-written COMMUNITIES mix, so a record it "
                    "receives whose species is in no mix is drawn nowhere. `planter` and "
                    "`ground` are the fixed square the timber loop sweeps and how much "
                    "of the modelled field it reaches — it may grow and may not shrink. "
                    "`unselectable` is the population, exact in both directions, and "
                    "`drawn_as_another_species` is the placed species that have no archetype of "
                    "their own. "
                    "`zone_boxes` records that a TIMBER_ZONE's extent is never consulted "
                    "by the reader it is routed to. `weights` is every mix entry's "
                    "literal beside the weight that replaces it at load — the literal is "
                    "a fallback, and `records.density` (the midpoint of the band in the "
                    "first TIMBER_ZONE naming the species) is what places a stem. Held by "
                    "tools/measure_planting_reach.py. Read ROADMAP K45(a) and K45(b1) "
                    "before adding a line.",
            "planter": state["planter"],
            "ground": state["ground"],
            "zone_boxes": {k: state["zone_boxes"][k] for k in sorted(state["zone_boxes"])},
            "unselectable": state["unselectable"],
            "drawn_as_another_species": state["drawn_as_another_species"],
            "weights": state["weights"],
        }, indent=2) + "\n", encoding="utf-8")
        overridden = sum(1 for v in state["weights"].values()
                         if v["verdict"] == "the-record-overrides")
        print(f"wrote {BASELINE.relative_to(ROOT)} "
              f"({len(state['unselectable'])} unselectable species, "
              f"{len(state['zone_boxes'])} timber zone(s), "
              f"{len(state['weights'])} mix entries, {overridden} of them overridden)")
        return 0

    if not args.gate and not args.quiet:
        print_census(state)

    bank = json.loads(BASELINE.read_text(encoding="utf-8"))
    problems += evaluate(state, bank)

    for p in problems:
        print(f"FAIL  {p}", file=sys.stderr)
    if problems:
        return 1

    if args.gate or args.quiet:
        g = state["ground"]
        overridden = sum(1 for v in state["weights"].values()
                         if v["verdict"] == "the-record-overrides")
        print(f"planting reach: the woody planter sweeps a "
              f"{2 * state['planter']['half_m']:.0f} m square and reaches "
              f"{g['inside_pct']:.1f} % of the ground above its own dry floor "
              f"({g['outside_ha']:.1f} ha outside it); "
              f"{len(state['unselectable'])} routed woody species can be selected by no "
              f"community mix; {overridden} of {len(state['weights'])} mix weights are "
              f"written to one number and run at another. All three are banked and none "
              f"may worsen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
