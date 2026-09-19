#!/usr/bin/env python3
"""Every pair of business records the register's PEOPLE put together and nobody has ruled.

    tools/audit_business_identity.py            the groups, read out
    tools/audit_business_identity.py --write    regenerate the ledger
    tools/audit_business_identity.py --check    it re-derives, and it has not grown
    tools/audit_business_identity.py --self-test the rules below, held over the real data

T-1388, of T-1182. THE IDENTITY QUESTION HAD ONE EYE OPEN. `compile_gazetteer.py` asks
"are these two printed notices one house or two?" and answers it three ways — a
`firm_merge`, a `refused_firm_merge`, a `premises_relation` — each declared in
identity.json with its reasoning and its printings, each gated. What it cannot do is
find the question. The grouping it runs on is `firm_surnames()`, which reads the
PARTNER SURNAMES OF THE TRADING STYLE, so a house is only ever compared with another
house whose style names the same surname.

146 of the 179 present records carry no partners at all. The register's own name for
such a record is descriptive — 'a new auction and commission room, South Water Street',
"E. Wentworth's public house on Flag Creek", '[unsigned] Boot, Shoe & Leather Store,
two doors north of Lake street' — and a descriptive name states no partner, so the
record never enters a group and its identity is never asked about. The proprietor the
register DID read off the notice is right there on the record and is not consulted.

So this pass groups on the other half: the PEOPLE. Two records are a pair when the
register read the same surname off their notices as a proprietor or a partner — a
person's name, not a style's word — and the pair is UNDECLARED when identity.json holds
no merge, no refusal and no premises relation for it. That is a question nobody has
answered, and until now nothing in the repository could name one.

WHY THE STYLE'S WORDS ARE NOT SURNAMES HERE. Keyed on the style instead, this pass reads
'Attorney', 'Store' and 'Law' as surnames and puts the town's four attorneys' cards into
one group — 182 pairs, most of them a trade word meeting itself. `firm_styled()` is the
existing reading of "is this string a firm's style rather than a person's name", and a
proprietor entry that it calls a style is skipped for exactly that reason. The pairs
below are people.

WHAT A PAIR IS NOT. It is not a claim that the two records are one house. Half of these
will be two men of one surname and the honest answer is a refusal — which is a RULING,
declared and cited, and is what this ledger asks for. The finding is that the question
stands unasked, not that the answer is a merge.

THE BASELINE MAY ONLY FALL, which is the discipline `audit_scene_window_trades.py` set.
`--check` re-derives the pairs and compares them to the committed ledger: a pair that
has disappeared is a ruling and the ledger is regenerated with it, a pair that has
appeared is a regression and fails the gate. A new business record that lands beside one
the town already holds therefore cannot arrive unadjudicated and silent.
"""
from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTER = ROOT / "data/research/newspapers/register_1835.json"
IDENTITY = ROOT / "data/research/newspapers/identity.json"
LEDGER = ROOT / "data/research/newspapers/business_identity_pairs.json"


def _gazetteer():
    """`compile_gazetteer.py`'s own readings, so this pass cannot drift from them.

    `surname_words()`, `firm_styled()` and `slug()` are the identity policy's spelling of
    three questions T-1042 settled once. Importing them is the point: a second reading
    here would be a fourth guess at the thing that ticket stopped guessing at.
    """
    spec = importlib.util.spec_from_file_location(
        "compile_gazetteer", ROOT / "tools/compile_gazetteer.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def person_surnames(business, cg):
    """The surnames the register read off this notice as PEOPLE, slugged.

    `proprietors` and `partners` both, because the register puts a sole trader in either
    depending on which claim read the printing. An entry `firm_styled()` calls a trading
    style is skipped: 'Jones, King & Co.' standing in a proprietor field names a house,
    and the house's own surnames are already `firm_surnames()`'s business.
    """
    out = set()
    for field in ("proprietors", "partners"):
        for entry in business.get(field) or []:
            name = entry if isinstance(entry, str) else (entry or {}).get("name")
            if not name or cg.firm_styled(name):
                continue
            out |= {cg.slug(w) for w in cg.surname_words(name)}
    return {s for s in out if s}


def declared_pairs(identity, cg):
    """Every pair identity.json has already answered, in any of its three ways.

    A merge, a refusal and a premises relation are three different answers to one
    question and all three end it, so all three take a pair out of this ledger.
    """
    out = set()
    for rule in identity.get("firm_merges", []):
        out.add(frozenset((cg.slug(rule.get("into") or ""), cg.slug(rule.get("from") or ""))))
    for rule in identity.get("refused_firm_merges", []):
        out.add(frozenset((cg.slug(rule.get("into") or ""), cg.slug(rule.get("from") or ""))))
    for rule in identity.get("premises_relations", []):
        out.add(frozenset((cg.slug(rule.get("part") or ""), cg.slug(rule.get("whole") or ""))))
    return out


def derive(register, identity, cg):
    """The undeclared pairs, as a sorted list of records the ledger can hold."""
    groups = collections.defaultdict(list)
    for biz in register["businesses"]:
        # SORTED, because `person_surnames` returns a set and a pair that two surnames
        # both reach — a partnership of two men who each trade alone as well — is
        # recorded under whichever surname is met first. Iterating the set directly makes
        # that depend on PYTHONHASHSEED, so the ledger differed between processes and
        # `--check` failed at random. It did, on this ticket's own run.
        for surname in sorted(person_surnames(biz, cg)):
            groups[surname].append(biz)

    already = declared_pairs(identity, cg)
    pairs = {}
    for surname, members in groups.items():
        if len(members) < 2:
            continue
        ordered = sorted(members, key=lambda b: b["name"])
        for i, a in enumerate(ordered):
            for b in ordered[i + 1:]:
                key = frozenset((cg.slug(a["name"]), cg.slug(b["name"])))
                if len(key) < 2 or key in already:
                    continue
                pairs.setdefault(key, {
                    "surname": surname,
                    "a": _side(a),
                    "b": _side(b),
                })
    return [pairs[k] for k in sorted(pairs, key=lambda k: (pairs[k]["surname"],
                                                           pairs[k]["a"]["name"],
                                                           pairs[k]["b"]["name"]))]


def _side(biz):
    """What a reader needs to rule the pair without opening the register."""
    return {
        "id": biz.get("business_record_id") or biz["id"],
        "name": biz["name"],
        "occupation": biz.get("occupation"),
        "street": biz.get("street"),
        "first_issue": (biz.get("evidence") or {}).get("first_issue"),
        "last_issue": (biz.get("evidence") or {}).get("last_issue"),
        "present_at_scene_date": biz.get("present_at_scene_date"),
    }


def build():
    cg = _gazetteer()
    register = json.loads(REGISTER.read_text())
    identity = json.loads(IDENTITY.read_text())
    pairs = derive(register, identity, cg)
    return {
        "schema": "business_identity_pairs/1",
        "generated_by": "tools/audit_business_identity.py",
        "_doc": (
            "Pairs of register businesses whose notices name the same PERSON as "
            "proprietor or partner, and which identity.json has not ruled on — no "
            "firm_merge, no refused_firm_merge, no premises_relation. Each is the "
            "question 'one house or two?' standing unanswered. The count may only "
            "fall: `--check` fails on a pair that has appeared."
        ),
        "counts": {
            "businesses": len(register["businesses"]),
            "undeclared_pairs": len(pairs),
            "surnames": len({p["surname"] for p in pairs}),
        },
        "pairs": pairs,
    }


def check():
    fresh = build()
    if not LEDGER.exists():
        print("business identity: no ledger committed — run --write", file=sys.stderr)
        return 1
    held = json.loads(LEDGER.read_text())
    fresh_keys = {(p["a"]["name"], p["b"]["name"]) for p in fresh["pairs"]}
    held_keys = {(p["a"]["name"], p["b"]["name"]) for p in held.get("pairs", [])}
    appeared = sorted(fresh_keys - held_keys)
    gone = sorted(held_keys - fresh_keys)
    if appeared:
        print("business identity: %d pair(s) APPEARED that the committed ledger does "
              "not carry. A business record that lands beside one the town already "
              "holds has to be ruled on, not left silent:" % len(appeared), file=sys.stderr)
        for a, b in appeared:
            print("  %r <-> %r" % (a, b), file=sys.stderr)
        return 1
    if gone or held != fresh:
        # SAY WHICH PART DISAGREES. A bare "stale" sent this ticket's own run looking for
        # nondeterminism that was not there, because a ruled pair and a hand-edited
        # ledger both printed the same sentence.
        differing = sorted(k for k in set(fresh) | set(held) if fresh.get(k) != held.get(k))
        print("business identity: the ledger is stale — %d pair(s) ruled since it was "
              "written, and %s differ%s. Re-run --write and commit it."
              % (len(gone), ", ".join(repr(k) for k in differing) or "nothing else",
                 "s" if len(differing) == 1 else ""), file=sys.stderr)
        for a, b in gone:
            print("  ruled: %r <-> %r" % (a, b), file=sys.stderr)
        return 1
    print("business identity: %d undeclared pair(s) across %d surname(s), as committed"
          % (fresh["counts"]["undeclared_pairs"], fresh["counts"]["surnames"]))
    return 0


def self_test():
    """The three assertions this pass rests on, held over the real corpus."""
    cg = _gazetteer()
    register = json.loads(REGISTER.read_text())
    identity = json.loads(IDENTITY.read_text())
    failures = []

    # 1. A PROPRIETOR FIELD HOLDING A TRADING STYLE NAMES NO PERSON. 'Jones, King & Co.'
    #    in a proprietor field is the house, not a man, and reading 'Jones' off it here
    #    would duplicate `firm_surnames()` rather than complement it.
    styled = {"proprietors": ["Jones, King & Co."], "partners": []}
    if person_surnames(styled, cg):
        failures.append("a firm style standing in a proprietor field was read as a person")

    # 2. A PERSON IS READ WHOLE. 'Taylor, Wm. H.' is the alphabetised setting of one man
    #    and must key the same as 'Wm. H. Taylor', or the 5 August list can never meet
    #    the card it repeats.
    a = person_surnames({"proprietors": ["Taylor, Wm. H."]}, cg)
    b = person_surnames({"proprietors": ["Wm. H. Taylor"]}, cg)
    if a != b or a != {"taylor"}:
        failures.append("the alphabetised and the printed setting of one man key "
                        "differently: %r against %r" % (sorted(a), sorted(b)))

    # 3. A RULED PAIR LEAVES THE LEDGER — in all three of its declarations, because a
    #    refusal and a relation end the question exactly as a merge does.
    for section, rule in (("firm_merges", {"into": "A & Co.", "from": "B & Co."}),
                          ("refused_firm_merges", {"into": "A & Co.", "from": "B & Co."}),
                          ("premises_relations", {"part": "A & Co.", "whole": "B & Co."})):
        spoof = dict(identity)
        spoof[section] = list(identity.get(section, [])) + [rule]
        if frozenset((cg.slug("A & Co."), cg.slug("B & Co."))) not in declared_pairs(spoof, cg):
            failures.append("a pair declared in `%s` is still read as unruled" % section)

    # 4. THE LEDGER IS DERIVED, not remembered: deriving twice over one register gives
    #    one answer — and the same answer in every process. `person_surnames` returns a
    #    SET, so a pair two surnames both reach takes whichever is iterated first, and
    #    under PYTHONHASHSEED that is not the same twice. This asserts the property the
    #    gate needs, which is that the ledger does not depend on the interpreter's seed;
    #    running it here would only re-measure one seed, so the second process is real.
    if derive(register, identity, cg) != derive(register, identity, cg):
        failures.append("the derivation is not stable over one register")
    seeds = set()
    for seed in ("0", "1", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        out = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve())],
                             capture_output=True, text=True, env=env, cwd=str(ROOT))
        seeds.add(out.stdout)
    if len(seeds) != 1:
        failures.append("the ledger differs between hash seeds — %d distinct readings, "
                        "so `--check` would fail at random" % len(seeds))

    for line in failures:
        print("  FAIL " + line, file=sys.stderr)
    print("business identity self-test: %d assertion(s), %d failure(s)"
          % (7, len(failures)))
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.check:
        return check()
    doc = build()
    if args.write:
        LEDGER.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print("wrote %s — %d undeclared pair(s)" % (LEDGER.relative_to(ROOT),
                                                    doc["counts"]["undeclared_pairs"]))
        return 0
    for pair in doc["pairs"]:
        print("[%s] %r (%s, %s..%s)\n      <-> %r (%s, %s..%s)" % (
            pair["surname"],
            pair["a"]["name"], pair["a"]["occupation"], pair["a"]["first_issue"], pair["a"]["last_issue"],
            pair["b"]["name"], pair["b"]["occupation"], pair["b"]["first_issue"], pair["b"]["last_issue"]))
    print("\n%d undeclared pair(s) across %d surname(s), of %d businesses"
          % (doc["counts"]["undeclared_pairs"], doc["counts"]["surnames"],
             doc["counts"]["businesses"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
