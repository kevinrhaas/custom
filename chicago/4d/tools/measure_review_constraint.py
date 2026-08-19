#!/usr/bin/env python3
"""What `review_required` actually blocks.

ROADMAP K34. AGENTS.md puts one constraint above the work — *the final removal of
the Potawatomi from Chicago occurred in August 1835, inside this project's first
target year* — and gives it exactly one mechanism:

    `review_required: true` on any record blocks a scene from being marked `released`.

Nothing had ever measured what that sentence covers.

    tools/measure_review_constraint.py           print the census
    tools/measure_review_constraint.py --gate    exit 1 on a divergence
    tools/measure_review_constraint.py --update  rewrite the baseline (deliberate act)

FIVE ASSERTIONS, AND FOUR OF THEM ARE ABSOLUTE. There is no ratchet here on purpose:
a ratchet is the right instrument for a fault being paid down, and this is not a fault
being paid down. It is a constraint the project has committed to, so the honest bar is
zero rather than "no worse than yesterday".

1.  **A record that says it carries the flag carries it.** Two sentences are used in
    this dataset and both are declarative: *"It carries review_required so that no
    scene containing it can be marked released"*, and *"review_required is set false …
    but the call is worth a second opinion"*. Each is a claim ABOUT the field, in the
    same file as the field, and nothing read the two together.

    A REGEX OVER PROSE IS THE RIGHT INSTRUMENT HERE AND IS USUALLY THE WRONG ONE.
    R-W4a and the smoke's own `/terrain|water/i` filter were regexes guessing at a
    CATEGORY from prose — they read like a rule until a name changed under them. This
    one matches the sentence that IS the claim being tested. If the sentence is
    reworded, the claim stops being made in a form anything can check, which is a
    thing worth failing over rather than a thing to sniff harder for.

2.  **`touches_removal` implies `review_required`, at every level that carries either.**
    `tools/validate.py` holds the household half. Persons carry the same two fields in
    the schema and nothing had ever asked them.

3.  **The constraint propagates to the buildings.** A household carrying it lives and
    works somewhere, and the scene draws the building rather than the person. This
    holds today at 11 links out of 11 — and held only by coincidence before this gate,
    because nothing required it.

4.  **The release block sees every layer that carries the flag.** Behavioural, against
    the real dataset: `validate_scene` is run with `released` forced true, and the
    blocked set it names must be exactly the union of flagged ids across the layers.
    This is the assertion that fails on the pre-K34 validator, which built that set out
    of `data/structures/` alone while its own household-side message promised that "any
    record touching it blocks a scene from being marked released".

5.  **A flag may be added freely and may not be cleared silently.** `--gate` fails when
    a record in `tools/review_constraint_baseline.json` has lost its flag, and names
    what clearing one is supposed to mean: the consultation AGENTS.md commits to has
    happened. New flags pass, print, and are folded in by `--update`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BASELINE = ROOT / "tools" / "review_constraint_baseline.json"

# The two sentences the dataset uses about this field. Direction matters: the first
# asserts the flag is set, the second asserts it deliberately is not.
CLAIM_CARRIES = re.compile(r"carries\s+review_required", re.I)
CLAIM_NOT_SET = re.compile(r"review_required\s+is\s+set\s+false", re.I)

LINK_FIELDS = ("lives_at", "works_at")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def prose(obj) -> list[str]:
    """Every string value in a record, at any depth."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [s for v in obj.values() for s in prose(v)]
    if isinstance(obj, list):
        return [s for v in obj for s in prose(v)]
    return []


def value_of(field) -> str | None:
    """A household link is `{value, confidence, …}`; the manifest flattens it."""
    if isinstance(field, dict):
        return field.get("value")
    return field if isinstance(field, str) else None


def read_structures() -> dict[str, dict]:
    out = {}
    for path in sorted((DATA / "structures").glob("*.json")):
        rec = load(path)
        if isinstance(rec, dict) and rec.get("id"):
            out[rec["id"]] = rec
    return out


def read_households() -> dict[str, dict]:
    index_path = DATA / "residents" / "index.json"
    if not index_path.exists():
        return {}
    out = {}
    for entry in load(index_path).get("households", []):
        path = DATA / "residents" / entry.get("file", "")
        if path.exists():
            rec = load(path)
            if isinstance(rec, dict) and rec.get("id"):
                out[rec["id"]] = rec
    return out


def measure() -> tuple[dict, list[str]]:
    """(census, problems)."""
    problems: list[str] = []
    structures = read_structures()
    households = read_households()

    flagged_structures = sorted(i for i, r in structures.items() if r.get("review_required"))
    flagged_households = sorted(i for i, r in households.items() if r.get("review_required"))
    persons = [(hid, p) for hid, h in households.items() for p in h.get("persons", [])]
    flagged_persons = sorted(f"{hid}/{p.get('id')}" for hid, p in persons
                             if p.get("review_required"))

    # ---- assertion 1: the prose and the field agree -------------------------------
    def claims(where: str, rec: dict, flag: bool) -> None:
        text = " ".join(prose(rec))
        if CLAIM_CARRIES.search(text) and not flag:
            problems.append(
                f"{where}: its own text says it carries review_required and the field is "
                f"false. AGENTS.md's standing constraint is not carried by a sentence — "
                f"a record that argues for the flag in prose and does not set it blocks "
                f"nothing, and reads to the next agent as though it does")
        if CLAIM_NOT_SET.search(text) and flag:
            problems.append(
                f"{where}: its own text says review_required is set false and the field "
                f"is true. One of the two was changed without the other")

    for sid in sorted(structures):
        claims(f"structure {sid}", structures[sid], bool(structures[sid].get("review_required")))
    for hid in sorted(households):
        claims(f"household {hid}", households[hid], bool(households[hid].get("review_required")))

    # ---- assertion 2: touches_removal implies review_required ---------------------
    for hid in sorted(households):
        h = households[hid]
        if h.get("touches_removal") and not h.get("review_required"):
            problems.append(f"household {hid}: touches_removal is true and review_required "
                            f"is false")
        for p in h.get("persons", []):
            if p.get("touches_removal") and not p.get("review_required"):
                problems.append(f"person {hid}/{p.get('id')}: touches_removal is true and "
                                f"review_required is false. The person layer carries both "
                                f"fields and nothing had ever asked it")

    # ---- assertion 3: the constraint reaches the buildings ------------------------
    links: list[tuple[str, str, str, bool]] = []
    for hid in sorted(households):
        h = households[hid]
        if not (h.get("review_required") or h.get("touches_removal")):
            continue
        for field in LINK_FIELDS:
            target = value_of(h.get(field))
            if not target:
                continue
            ok = bool(structures.get(target, {}).get("review_required"))
            links.append((hid, field, target, ok))
            if target not in structures:
                problems.append(f"household {hid}: {field} names '{target}', which is not a "
                                f"committed structure")
            elif not ok:
                problems.append(
                    f"structure {target}: houses {hid} ({field}), which carries the standing "
                    f"constraint, and does not carry review_required itself. The scene draws "
                    f"the building and not the person, so the flag has to reach the building")

    # ---- assertion 4: the release block sees every layer -------------------------
    blocked, block_error = release_block(structures, households)
    expected = set(flagged_structures) | set(flagged_households) \
        | {ref.split("/")[0] for ref in flagged_persons}
    if block_error:
        problems.append(f"release block: {block_error}")
    else:
        missed = sorted(expected - blocked)
        spurious = sorted(blocked - expected)
        if missed:
            problems.append(
                f"release block: a scene marked released is NOT refused by {missed}, which "
                f"carry review_required. tools/validate.py's own message says any record "
                f"touching the removal blocks release; these records are the layers that "
                f"message does not reach")
        if spurious:
            problems.append(f"release block: names {spurious}, which carry no flag")

    # ---- assertion 5: nothing loses a flag quietly -------------------------------
    added: dict[str, list[str]] = {}
    if BASELINE.exists():
        base = load(BASELINE)
        current = {"structures": flagged_structures, "households": flagged_households,
                   "persons": flagged_persons}
        for layer, ids in current.items():
            was = set(base.get(layer) or [])
            cleared = sorted(was - set(ids))
            gained = sorted(set(ids) - was)
            if gained:
                added[layer] = gained
            for rid in cleared:
                problems.append(
                    f"{layer[:-1]} {rid}: carried review_required in "
                    f"{BASELINE.name} and does not now. Clearing this flag is the claim "
                    f"that the consultation AGENTS.md commits to has happened for this "
                    f"record; if it has, say so in the record and re-run this tool with "
                    f"--update in the same commit")
    else:
        problems.append(f"{BASELINE.name} is missing, so nothing can say whether a flag "
                        f"has been cleared")

    census = {
        "structures": {"total": len(structures), "flagged": flagged_structures},
        "households": {"total": len(households), "flagged": flagged_households},
        "persons": {"total": len(persons), "flagged": flagged_persons},
        "links": links,
        "added": added,
    }
    return census, problems


def release_block(structures: dict, households: dict) -> tuple[set[str], str | None]:
    """Which records a scene marked `released` is actually refused for.

    Run rather than read: the question is what `tools/validate.py` DOES, and a gate
    that restated the rule would pass while the validator disagreed with it. Every
    committed scene is put through the real `validate_scene` with `released` forced
    true, and the ids it names are collected out of the error it raises.
    """
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import validate as V  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001
        return set(), f"cannot import tools/validate.py: {e}"

    scenes = [load(p) for p in sorted((DATA / "scenes").glob("*.json"))]
    epochs_path = DATA / "terrain" / "epochs.json"
    epochs = load(epochs_path) if epochs_path.exists() else {}
    if isinstance(epochs, list):
        epochs = {e.get("id"): e for e in epochs}
    elif "epochs" in epochs:
        epochs = {e.get("id"): e for e in epochs["epochs"]}

    named: set[str] = set()
    for scene in scenes:
        rep = V.Report()
        forced = {**scene, "released": True}
        structs = {f"{i}.json": r for i, r in structures.items()}
        try:
            V.validate_scene(forced, structs, epochs, {}, rep, households=households)
        except TypeError:
            # the pre-K34 signature, which cannot be handed the household layer at all
            V.validate_scene(forced, structs, epochs, {}, rep)
        for err in rep.errors:
            if "review_required" not in err:
                continue
            for rid in list(structures) + list(households):
                if re.search(rf"\b{re.escape(rid)}\b", err):
                    named.add(rid)
    return named, None


def print_census(c: dict) -> None:
    def row(layer: str) -> str:
        d = c[layer]
        return f"{layer:<12} {len(d['flagged']):>4} flagged of {d['total']:>4}"

    print("AGENTS.md: `review_required: true` on any record blocks a scene from being "
          "marked released.\n")
    for layer in ("structures", "households", "persons"):
        print("  " + row(layer))
        for rid in c[layer]["flagged"]:
            print(f"                 {rid}")
    print(f"\n  {len(c['links'])} link(s) from a constrained household to a building:")
    for hid, field, target, ok in c["links"]:
        print(f"    {'ok  ' if ok else 'FAIL'} {hid} {field} -> {target}")
    if c["added"]:
        for layer, ids in c["added"].items():
            print(f"\n  NEW since the baseline ({layer}): {', '.join(ids)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", action="store_true", help="exit 1 on a divergence")
    ap.add_argument("--quiet", action="store_true", help="print only the verdict")
    ap.add_argument("--update", action="store_true", help="rewrite the baseline")
    args = ap.parse_args()

    census, problems = measure()

    if args.update:
        BASELINE.write_text(json.dumps({
            "_doc": "The records carrying AGENTS.md's standing constraint, as of the last "
                    "deliberate change. tools/measure_review_constraint.py fails when one "
                    "of these has lost its review_required flag: adding the flag is always "
                    "allowed, clearing it is the claim that the consultation this project "
                    "has committed to has happened, and that is not a thing to do by "
                    "accident. Rewrite with --update, in the commit that makes the change.",
            "structures": census["structures"]["flagged"],
            "households": census["households"]["flagged"],
            "persons": census["persons"]["flagged"],
        }, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {BASELINE.relative_to(ROOT)}")
        return 0

    if not args.gate and not args.quiet:
        print_census(census)

    for p in problems:
        print(f"FAIL  {p}", file=sys.stderr)
    if problems:
        return 1
    if args.gate or args.quiet:
        n_s = len(census["structures"]["flagged"])
        n_h = len(census["households"]["flagged"])
        n_p = len(census["persons"]["flagged"])
        print(f"standing constraint: {n_s} structure(s), {n_h} household(s), {n_p} person(s) "
              f"carry review_required; {len(census['links'])} link(s) reach a building that "
              f"carries it too; a scene marked released is refused for every one of them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
