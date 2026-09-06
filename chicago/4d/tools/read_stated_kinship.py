#!/usr/bin/env python3
"""T-0734 — the kinship the sources already state, and the gate that keeps it stated.

`persons[].relationship` is a person's place inside one household.  `kin` (T-0597)
is a tie that crosses two records.  `tools/validate.py` already checks a kin row's
SHAPE — that both ends resolve, that the mirror exists, that a half brother's
mirror is not a plain brother.  What it cannot check is the thing this pass is
actually about: **whether the corpus's stated kinship reached the records at all.**
A household that simply omits a tie the sources print is silently valid, and 1,362
people carrying 24 relationships between them is what that looks like at scale.

So the ledger is the argument and this file is the gate on it:

  data/research/residents/stated_kinship.json
    `landed`    — a tie the corpus states, with the statement quoted, the identity
                  binding written out, and a confidence that says which of the two
                  was read rather than found.
    `refusals`  — a tie the corpus states that did NOT land, with the reason.  A
                  refusal is declared as explicitly as a landing; eleven of the
                  sixteen ties the corpus states are refusals, and ten of those
                  eleven fail because the other person is not in this layer.

    tools/read_stated_kinship.py --check       the gate (check.sh runs this)
    tools/read_stated_kinship.py --build       re-derive the counts block
    tools/read_stated_kinship.py --self-test   the gate's own assertions still fire

WHAT --check ENFORCES, and why each one is a fault somebody has already made
somewhere in this dataset:

  1. Every `landed` row is CARRIED, on both records, with the relation, the
     confidence and the source the ledger claims for it.  A ledger that says a tie
     landed while the card says nothing is the exact shape of the drift T-0814 is
     open about, and it is invisible to validate.py: the household without the row
     is perfectly valid.
  2. Every `refused` pair carries NO kin row.  A refusal that has quietly been
     landed by a later pass is a ruling nobody made.
  3. The counts are DERIVED here, not typed.  An unruled pair cannot hide behind a
     stale number.
  4. Every id in the ledger resolves to a committed household and person.
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = ROOT / "data/research/residents/stated_kinship.json"
HOUSEHOLDS = ROOT / "data/residents/households"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def committed():
    """Every kin row on disk, as {(hh, person, other_hh, other_person): row}."""
    rows = {}
    people = {}
    for path in sorted(HOUSEHOLDS.glob("*.json")):
        doc = load(path)
        hid = doc.get("id") or path.stem
        people[hid] = {p.get("id") for p in doc.get("persons") or []}
        for k in doc.get("kin") or []:
            rows[(hid, k.get("person"), k.get("household"), k.get("value"))] = k
    return rows, people


def audit(ledger, rows, people):
    """Every problem the ledger and the committed records have with each other."""
    problems = []
    landed = ledger.get("landed") or []
    for row in landed:
        r = row.get("relation") or {}
        hid, pid = r.get("household"), r.get("person")
        ohid, opid = r.get("other_household"), r.get("other_person")
        rid = row.get("id")
        for h, p in ((hid, pid), (ohid, opid)):
            if h not in people:
                problems.append(f"{rid}: household '{h}' does not resolve")
            elif p not in people[h]:
                problems.append(f"{rid}: '{p}' is not a person in household '{h}'")
        if problems and problems[-1].startswith(f"{rid}:"):
            continue
        # both directions, because a kinship the far record omits is half a fact
        for a, b, rel in ((( hid, pid), (ohid, opid), r.get("relation")),
                          ((ohid, opid), (hid, pid), r.get("mirror_relation"))):
            got = rows.get((a[0], a[1], b[0], b[1]))
            if got is None:
                problems.append(f"{rid}: the ledger says this tie landed, and "
                                f"'{a[0]}' carries no kin row for '{b[1]}'. A ledger "
                                f"entry is not a record")
                continue
            if got.get("relation") != rel:
                problems.append(f"{rid}: '{a[0]}' says relation "
                                f"'{got.get('relation')}' and the ledger says '{rel}'")
            if got.get("confidence") != row.get("confidence"):
                problems.append(f"{rid}: '{a[0]}' says confidence "
                                f"'{got.get('confidence')}' and the ledger says "
                                f"'{row.get('confidence')}'. The grade is the whole "
                                f"claim about how the identity was reached")
            if row.get("source") not in (got.get("sources") or []):
                problems.append(f"{rid}: '{a[0]}' does not cite "
                                f"'{row.get('source')}', which the ledger says the "
                                f"statement comes from")

    ruled = {frozenset((r["relation"]["person"], r["relation"]["other_person"]))
             for r in landed if r.get("relation")}
    for ref in ledger.get("refusals") or []:
        who = [w for w in (ref.get("who") or []) if any(w in ids for ids in people.values())]
        if len(who) == 2 and frozenset(who) in ruled:
            problems.append(f"{ref.get('id')}: refused and landed at the same time")
        for a in who:
            for b in who:
                if a == b:
                    continue
                for key, row in rows.items():
                    if key[1] == a and key[3] == b:
                        problems.append(
                            f"{ref.get('id')}: this pair is declared a REFUSAL and "
                            f"'{key[0]}' carries a kin row for it. A refusal that has "
                            f"quietly been landed is a ruling nobody made")
        if not (ref.get("reason") or "").strip():
            problems.append(f"{ref.get('id')}: a refusal without a reason is a silence")
    return problems


def derive(ledger, rows):
    landed = ledger.get("landed") or []
    refusals = ledger.get("refusals") or []
    by_conf = {}
    for row in landed:
        by_conf[row.get("confidence")] = by_conf.get(row.get("confidence"), 0) + 1
    return {
        "ties_stated_by_the_corpus": len(landed) + len(refusals),
        "landed": len(landed),
        "refused": len(refusals),
        "landed_by_confidence": dict(sorted(by_conf.items())),
        "reciprocal_rows_written": len(landed) * 2,
        "kin_rows_committed": len(rows),
    }


def check(ledger, rows, people, quiet=False):
    problems = audit(ledger, rows, people)
    derived = derive(ledger, rows)
    if ledger.get("counts") != derived:
        problems.append(f"the counts block is stale: committed {ledger.get('counts')!r}, "
                        f"derived {derived!r}. Re-run --build")
    if problems:
        if not quiet:
            print("STATED KINSHIP FAIL")
            for p in problems:
                print(" -", p)
        return 1
    if not quiet:
        print(f"OK: {derived['ties_stated_by_the_corpus']} stated ties — "
              f"{derived['landed']} landed as {derived['reciprocal_rows_written']} reciprocal "
              f"rows, {derived['refused']} refused; {derived['kin_rows_committed']} kin rows "
              f"committed in all")
    return 0


def build():
    ledger = load(LEDGER)
    rows, _ = committed()
    ledger["counts"] = derive(ledger, rows)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("counts re-derived:", json.dumps(ledger["counts"]))
    return 0


def self_test():
    """Break the ledger four ways and require the gate to notice each one."""
    import copy
    ledger = load(LEDGER)
    rows, people = committed()
    failures = []

    def expect(label, mutate, needle):
        led, rw = copy.deepcopy(ledger), dict(rows)
        mutate(led, rw)
        problems = audit(led, rw, people)
        if not any(needle in p for p in problems):
            failures.append(f"{label}: expected a problem containing {needle!r}, got {problems}")
        else:
            print(f"  pass  {label}")

    expect("a ledger entry whose record does not carry the row is caught",
           lambda led, rw: rw.pop(next(iter(
               k for k in rw if k[1] == led["landed"][0]["relation"]["person"]))),
           "is not a record")
    expect("a ledger entry whose record disagrees about the grade is caught",
           lambda led, rw: led["landed"].__setitem__(
               0, {**led["landed"][0], "confidence": "reconstructed"}),
           "The grade is the whole claim")
    expect("a ledger entry whose record does not cite the stated source is caught",
           lambda led, rw: led["landed"].__setitem__(
               0, {**led["landed"][0], "source": "no_such_source"}),
           "does not cite")
    expect("a ledger entry naming somebody who is not in the far household is caught",
           lambda led, rw: led["landed"].__setitem__(
               0, {**led["landed"][0],
                   "relation": {**led["landed"][0]["relation"], "other_person": "nobody"}}),
           "is not a person in household")
    expect("a refusal with no reason is caught",
           lambda led, rw: led["refusals"].__setitem__(
               0, {**led["refusals"][0], "reason": "  "}),
           "a silence")

    def land_a_refusal(led, rw):
        ref = next(r for r in led["refusals"]
                   if len([w for w in r["who"] if any(w in i for i in people.values())]) == 2)
        a, b = [w for w in ref["who"] if any(w in i for i in people.values())]
        rw[("hh_somewhere", a, "hh_elsewhere", b)] = {"relation": "brother"}
    expect("a refused pair that has quietly acquired a kin row is caught",
           land_a_refusal, "a ruling nobody made")

    if failures:
        print("SELF-TEST FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS — the stated-kinship gate's own assertions all fire")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.build:
        return build()
    if args.self_test:
        return self_test()
    rows, people = committed()
    return check(load(LEDGER), rows, people)


if __name__ == "__main__":
    sys.exit(main())
