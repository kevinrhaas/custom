#!/usr/bin/env python3
"""Every conflict the research ledgers record is ruled on, and every ruling rules on a real one.

WHY THIS EXISTS. The passes wrote 106 conflicts against candidates and adjudicated none of
them where anything could read the decision. T-0512's audit could see the flag and not the
verdict, which means a conflict somebody HAD weighed looked exactly like a conflict nobody
found. `data/research/residents/conflict_rulings.json` is the verdicts; this is the gate that
keeps them total, so the next pass's conflict cannot silt up unruled the way those 106 did.

It is deliberately a COVERAGE gate and not a judgement. It reads no source and rules on
nothing: it asserts that the set of conflict strings in the ledgers and the set quoted in the
rulings file are the same set, that every household carrying `review_required` has a ruling
saying it is held rather than unexamined, and that the vocabulary the rulings draw on is
closed and fully used. A ruling's REASONING is a human's, and this tool never checks it.

    tools/check_conflict_rulings.py             the gate
    tools/check_conflict_rulings.py --self-test the assertions still fire when broken
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data/research/residents"
HOUSEHOLDS = ROOT / "data/residents/households"
RULINGS = RESEARCH / "conflict_rulings.json"


def ledger_conflicts() -> dict[str, Counter]:
    """person id -> the conflict strings recorded against that person, with multiplicity.

    EVERY pass is read, not just the last. `export_resident_audit.py` keeps the newest
    override per person, but a conflict written in pass 02 was still written; a ruling layer
    that only covered the surviving override would let the older ones vanish unadjudicated."""
    out: dict[str, Counter] = {}
    for path in sorted(RESEARCH.glob("pass_*_findings.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for person_id, override in (doc.get("overrides") or {}).items():
            for candidate in (override.get("candidates") or []):
                for conflict in (candidate.get("conflicts") or []):
                    out.setdefault(person_id, Counter())[conflict] += 1
    return out


def review_required() -> set[str]:
    return {json.loads(p.read_text(encoding="utf-8"))["id"]
            for p in sorted(HOUSEHOLDS.glob("*.json"))
            if json.loads(p.read_text(encoding="utf-8")).get("review_required")}


def audit(doc: dict, ledger: dict[str, Counter], flagged: set[str]) -> list[str]:
    """The problems, in the order a reader would want them. Empty list is the pass."""
    bad: list[str] = []
    verdicts = doc.get("verdicts") or {}
    grounds = doc.get("grounds") or {}
    rulings = doc.get("rulings") or []
    household_rulings = doc.get("household_rulings") or []

    seen_grounds: set[str] = set()
    ruled: dict[str, Counter] = {}
    for ruling in rulings:
        person_id = ruling.get("person_id", "?")
        if person_id in ruled:
            bad.append("%s is ruled on twice; one person, one ruling" % person_id)
        ruled[person_id] = Counter(ruling.get("conflicts") or [])
        if ruling.get("verdict") not in verdicts:
            bad.append("%s carries verdict %r, which the file's own vocabulary does not "
                       "define" % (person_id, ruling.get("verdict")))
        if not ruling.get("grounds"):
            bad.append("%s is ruled with no grounds: a verdict that names no objection says "
                       "nothing about what would settle it" % person_id)
        for ground in ruling.get("grounds") or []:
            seen_grounds.add(ground)
            if ground not in grounds:
                bad.append("%s stands on ground %r, which the vocabulary does not define"
                           % (person_id, ground))

    for person_id in sorted(set(ledger) | set(ruled)):
        recorded = ledger.get(person_id, Counter())
        covered = ruled.get(person_id, Counter())
        for conflict in sorted((recorded - covered).elements()):
            bad.append("%s: the ledgers record a conflict no ruling reaches — %r"
                       % (person_id, conflict))
        for conflict in sorted((covered - recorded).elements()):
            bad.append("%s: a ruling quotes a conflict the ledgers do not carry — %r. Quote "
                       "the ledger verbatim, or fix the ledger and rule again."
                       % (person_id, conflict))

    ruled_households: set[str] = set()
    for ruling in household_rulings:
        household_id = ruling.get("household_id", "?")
        ruled_households.add(household_id)
        if ruling.get("verdict") not in verdicts:
            bad.append("%s carries verdict %r, which the file's own vocabulary does not "
                       "define" % (household_id, ruling.get("verdict")))
        for ground in ruling.get("grounds") or []:
            seen_grounds.add(ground)
            if ground not in grounds:
                bad.append("%s stands on ground %r, which the vocabulary does not define"
                           % (household_id, ground))
    for household_id in sorted(flagged - ruled_households):
        bad.append("%s carries review_required and no ruling: the audit cannot tell a record "
                   "held for consultation from one nobody looked at" % household_id)
    for household_id in sorted(ruled_households - flagged):
        bad.append("%s is ruled held for review and no longer carries review_required"
                   % household_id)

    for ground in sorted(set(grounds) - seen_grounds):
        bad.append("ground %r is defined and used by nothing. A vocabulary nobody draws on "
                   "stops describing the rulings and starts decorating them." % ground)
    for ground, body in sorted(grounds.items()):
        for key in ("stands_because", "settled_by"):
            if not (body or {}).get(key):
                bad.append("ground %r has no %s: the exit is the point of writing it down"
                           % (ground, key))
    return bad


def cmd_check() -> bool:
    doc = json.loads(RULINGS.read_text(encoding="utf-8"))
    ledger = ledger_conflicts()
    bad = audit(doc, ledger, review_required())
    for line in bad:
        print("conflict rulings: %s" % line, file=sys.stderr)
    if bad:
        return True
    total = sum(sum(c.values()) for c in ledger.values())
    print("conflict rulings: %d conflicts across %d people are ruled, and %d households are "
          "held for consultation" % (total, len(ledger), len(doc.get("household_rulings") or [])))
    return False


def cmd_self_test() -> bool:
    """Break the file four ways in memory and require each break to be caught."""
    doc = json.loads(RULINGS.read_text(encoding="utf-8"))
    ledger = ledger_conflicts()
    flagged = review_required()
    bad = False

    def want(broken_doc, broken_ledger, broken_flagged, needle, label):
        nonlocal bad
        problems = audit(broken_doc, broken_ledger, broken_flagged)
        if not any(needle in p for p in problems):
            print("  FAIL %s: no problem mentioning %r" % (label, needle))
            bad = True

    if audit(doc, ledger, flagged):
        print("  FAIL the committed file does not pass its own gate")
        bad = True

    dropped = json.loads(json.dumps(doc))
    dropped["rulings"] = dropped["rulings"][1:]
    want(dropped, ledger, flagged, "no ruling reaches",
         "a ledger conflict with its ruling removed")

    invented = json.loads(json.dumps(doc))
    invented["rulings"][0]["conflicts"] = ["A conflict nobody ever wrote."]
    want(invented, ledger, flagged, "the ledgers do not carry",
         "a ruling quoting a conflict that is not in the ledgers")

    unknown = json.loads(json.dumps(doc))
    unknown["rulings"][0]["grounds"] = ["it_felt_wrong"]
    want(unknown, ledger, flagged, "the vocabulary does not define",
         "a ground outside the vocabulary")

    want(doc, ledger, flagged | {"hh_a_household_nobody_ruled"}, "and no ruling",
         "a newly flagged household with no ruling")

    ungrounded = json.loads(json.dumps(doc))
    ungrounded["rulings"][0]["grounds"] = []
    want(ungrounded, ledger, flagged, "no grounds", "a verdict that names no objection")

    if not bad:
        print("conflict rulings self-test: all assertions fire")
    return bad


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return 1 if cmd_self_test() else 0
    return 1 if cmd_check() else 0


if __name__ == "__main__":
    sys.exit(main())
