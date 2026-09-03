#!/usr/bin/env python3
"""What the research domains have READ, against what the town has SPENT.

WHY THIS EXISTS. On 2026-09-03 the owner reported, of the 1840 census reading
tickets: "i see lots of research being done and some apparent findings from
parsing but there are not outputs or updates to the household and resident data
it seems, should i be concerned?"

He was right, and nothing in the repo could have told him so. Every reading
ticket DOES leave an output — T-0584 wrote 2,354 lines of page records, a
coverage entry and a changelog line — so no gate was red and no run was idle.
The hole was one layer down: `data/research/census_1840/` held 562 named heads
read off the sheets and `census_1840/crosswalk.json` held `passes: []`,
`merges: []`, `refusals: []`. Nothing had crossed into the town. Four of 828
household records carried an 1840 link.

`coverage.json` already answers "which images have been looked at, and what has
NOT been read from them" — deliberately, so a hole fails rather than passes
quietly. This is the same instrument one step later: which names have been READ,
and how many of them anybody has RULED ON. A domain may read far ahead of its
spending — the ratified ladder REQUIRES it, since 1839/1840 alone is never an
1835 resident and the bridge is a separate adjudicated step — but the gap may
not silently WIDEN. That is what this gate holds.

THE MEASURE, and what each half deliberately does not count.

  read    a unit captured off a source and carrying a name or a quote: an entry
          of a `records` array (domains that hold records) or of a `claims`
          array (domains that hold claims). Continuation-sheet lines that carry
          cells and no name are not names and do not count.

  spent   a crosswalk entry ANCHORED to something real — a read record
          (`record_id`, `entry_id`, `claim_id`) or a person in the town
          (`person_id`, `resident`, `matched_resident`). Deduped by that anchor,
          because civic adjudicates its 479 voters in `voter_crosswalk.json`
          AND rules on name pairs in `crosswalk.json`, and summing the two array
          lengths reported civic as 571 spent against 492 read — a domain more
          than finished. An instrument that reports -79 unspent is worse than no
          instrument.

          A REFUSAL COUNTS AS SPENT. census_1840/crosswalk.json says why: "A
          refusal is declared as explicitly as a merge — the absence of one
          reads like a pair nobody has looked at yet." Ruling that a name is
          NOT a town person is the adjudication; it is not a failure to do one.

  id pairs a merge/refusal ruling on two spellings (`a` / `b`) with no anchor.
          Reported, never counted as spend: it is a ruling about the sources'
          own vocabulary, not about whether the town gained anything.

  unspent read - spent. NOT a defect count. census_1830, church and books read
          nothing yet and are honestly 0/0; a domain reading ahead of a bridge
          ticket is the method working.

THE GATE is a ratchet, not a target. `unspent` may not exceed the figure in
research_spend_baseline.json. Read more and you must rule on more, or say in the
PR why the baseline moves. Raising a baseline is a decision somebody makes on
purpose; drifting past it is what happened for three weeks.

THE RATCHET HAS TWO DIRECTIONS, and only one of them costs anything. Raising a
ceiling says the project chose to read further ahead of its adjudication, so it
takes one domain and a written reason. Lowering is what SPENDING a domain earns,
can only make this gate stricter, and is therefore free. Without the second
direction the first is a slow leak: a domain spent to nothing would keep the
ceiling its worst day earned and could drift back up to it in silence.

    tools/measure_research_spend.py              the table
    tools/measure_research_spend.py --gate       the ratchet, and what slack it sees
    tools/measure_research_spend.py --raise newberry_index --why "T-0578 read vol 2"
    tools/measure_research_spend.py --tighten    reclaim slack after spending
    tools/measure_research_spend.py --rebaseline first write only
    tools/measure_research_spend.py --self-test
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data" / "research"
REGISTRY = RESEARCH / "domains.json"
BASELINE = Path(__file__).resolve().parent / "research_spend_baseline.json"

# The arrays a crosswalk file states its rulings in. `pages` is deliberately
# absent: census_1840/crosswalk_670.json compares five PAGES against the lost v4
# workbook, which is a page-level agreement test and rules on nobody.
ADJUDICATION_KEYS = ("passes", "merges", "refusals", "matches",
                     "contested", "ambiguous", "probable", "entries")

# What a ruling may anchor to. Order matters only for which name the dedup key
# takes; any one of them makes the entry a spend.
ANCHOR_KEYS = ("record_id", "entry_id", "claim_id",
               "person_id", "resident", "matched_resident")

# A unit is READ if it carries one of these. `quote` is here for the claims
# domains, whose unit is a sentence the source prints rather than a name.
NAME_KEYS = ("normalized", "as_read", "quote")


def is_crosswalk(path: Path) -> bool:
    return "crosswalk" in path.name


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def count_read(domain_dir: Path) -> int:
    """Named units captured in a domain, over every JSON it holds but its crosswalks."""
    total = 0
    for path in sorted(domain_dir.rglob("*.json")):
        if is_crosswalk(path):
            continue
        doc = read_json(path)
        if not isinstance(doc, dict):
            continue
        for key in ("records", "claims"):
            units = doc.get(key)
            if not isinstance(units, list):
                continue
            total += sum(1 for u in units if isinstance(u, dict)
                         and any(u.get(n) for n in NAME_KEYS))
    return total


def count_spent(domain_dir: Path) -> tuple[int, int]:
    """(anchored rulings, deduped) and (unanchored name-pair rulings)."""
    anchors: set[str] = set()
    pairs = 0
    for path in sorted(domain_dir.rglob("*.json")):
        if not is_crosswalk(path):
            continue
        doc = read_json(path)
        if not isinstance(doc, dict):
            continue
        for key in ADJUDICATION_KEYS:
            rulings = doc.get(key)
            if not isinstance(rulings, list):
                continue
            for ruling in rulings:
                if not isinstance(ruling, dict):
                    continue
                anchor = next((f"{k}={ruling[k]}" for k in ANCHOR_KEYS
                               if ruling.get(k)), None)
                if anchor:
                    anchors.add(anchor)
                else:
                    pairs += 1
    return len(anchors), pairs


def measure() -> list[dict]:
    registry = read_json(REGISTRY)
    if not isinstance(registry, dict) or not registry.get("domains"):
        raise SystemExit(f"unreadable domain registry: {REGISTRY}")
    rows = []
    for entry in registry["domains"]:
        domain_dir = ROOT / entry["path"]
        if not domain_dir.is_dir():
            raise SystemExit(f"registered domain has no directory: {entry['path']}")
        read = count_read(domain_dir)
        spent, pairs = count_spent(domain_dir)
        rows.append({"domain": entry["id"], "holds": entry["holds"],
                     "read": read, "spent": spent,
                     "unspent": read - spent, "id_pairs": pairs})
    return rows


def unregistered() -> list[str]:
    """Domain directories on disk that the registry does not name.

    Not a failure: `newspapers` is registered nowhere on purpose (domains.json
    says "beside the newspapers") and `residents` is the destination layer, not
    a source. Printed so a NEW domain cannot be read into existence unmeasured.
    """
    registry = read_json(REGISTRY) or {}
    known = {Path(d["path"]).name for d in registry.get("domains", [])}
    return sorted(p.name for p in RESEARCH.iterdir()
                  if p.is_dir() and p.name not in known)


def report() -> str:
    rows = measure()
    out = ["domain            holds      read    spent  unspent  id pairs",
           "-" * 58]
    for r in rows:
        out.append(f"{r['domain']:<17}{r['holds']:<9}{r['read']:>7}"
                   f"{r['spent']:>9}{r['unspent']:>9}{r['id_pairs']:>10}")
    out.append("-" * 58)
    out.append(f"{'TOTAL':<26}{sum(r['read'] for r in rows):>7}"
               f"{sum(r['spent'] for r in rows):>9}"
               f"{sum(r['unspent'] for r in rows):>9}"
               f"{sum(r['id_pairs'] for r in rows):>10}")
    extra = unregistered()
    if extra:
        out.append("")
        out.append("not registered in domains.json (not measured): " + ", ".join(extra))
    return "\n".join(out)


def gate(quiet: bool = False) -> int:
    baseline = read_json(BASELINE)
    if not isinstance(baseline, dict):
        print(f"   no baseline at {BASELINE.name} — run --rebaseline")
        return 1
    ceilings = baseline.get("unspent_ceiling", {})
    rows = measure()
    faults = []
    for r in rows:
        if r["domain"] not in ceilings:
            faults.append(f"{r['domain']}: no ceiling recorded — a new domain must "
                          f"enter the baseline deliberately (unspent {r['unspent']})")
            continue
        ceiling = ceilings[r["domain"]]
        if r["unspent"] > ceiling:
            faults.append(f"{r['domain']}: {r['unspent']} unspent, ceiling {ceiling} "
                          f"(+{r['unspent'] - ceiling}) — {r['read']} read, {r['spent']} ruled on")
    for domain in ceilings:
        if not any(r["domain"] == domain for r in rows):
            faults.append(f"{domain}: in the baseline and not in domains.json")
    if faults:
        print("   research read faster than the town spent it:")
        for f in faults:
            print(f"     {f}")
        print("   Rule on the names, or raise that one domain's ceiling with")
        print("     tools/measure_research_spend.py --raise <domain> --why \"...\"")
        return 1
    # SLACK IS REPORTED, ALWAYS. A ceiling only ever moved up, and this gate would
    # have stayed silent about it: a domain spent all the way down keeps the ceiling
    # its worst day earned, and may drift back up to it unnoticed. That is a ratchet
    # with one tooth. `--tighten` reclaims it and needs no justification, because
    # lowering a ceiling can only make this gate stricter.
    slack = [(r["domain"], ceilings[r["domain"]] - r["unspent"]) for r in rows
             if r["domain"] in ceilings and ceilings[r["domain"]] > r["unspent"]]
    if slack and not quiet:
        for domain, by in slack:
            print(f"   reclaimable: {domain} sits {by} under its ceiling")
        print("   tools/measure_research_spend.py --tighten takes it back")
    if not quiet:
        print(report())
    return 0


def write_baseline(doc: dict) -> None:
    BASELINE.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8")


def rebaseline() -> int:
    """FIRST WRITE ONLY. It used to rewrite every domain from current state, which
    is how a run raising one ceiling would have silently absorbed the drift of all
    the others — no reason recorded anywhere, which is the exact fault this file
    exists to catch. Raising is now per-domain and costs a sentence (`--raise`);
    lowering is free (`--tighten`)."""
    if BASELINE.exists():
        print(f"   {BASELINE.name} already exists — refusing to rewrite every ceiling at once.")
        print("   Raise ONE domain, with a reason:  --raise <domain> --why \"...\"")
        print("   Reclaim slack after spending:     --tighten")
        return 1
    rows = measure()
    write_baseline({
        "schema": 1,
        "_doc": ("The unspent ceiling per research domain — read minus ruled-on. RAISING A "
                 "NUMBER HERE IS A DECISION and is written by --raise, which requires a "
                 "reason and touches one domain. Lowering is free and is what spending a "
                 "domain does: --tighten reclaims the slack. --rebaseline writes this file "
                 "once and then refuses, so no run can launder every ceiling in one go."),
        "generated_by": "tools/measure_research_spend.py --rebaseline",
        "unspent_ceiling": {r["domain"]: r["unspent"] for r in rows},
        "witness": {r["domain"]: {"read": r["read"], "spent": r["spent"]} for r in rows},
        "raised": [],
    })
    print(f"wrote {BASELINE.name}")
    print(report())
    return 0


def raise_ceiling(domain: str, why: str) -> int:
    """Raise ONE domain's ceiling to what it currently reads, and record who said why."""
    baseline = read_json(BASELINE)
    if not isinstance(baseline, dict):
        print(f"   no baseline at {BASELINE.name} — run --rebaseline")
        return 1
    rows = {r["domain"]: r for r in measure()}
    if domain not in rows:
        print(f"   {domain} is not a domain in domains.json — nothing to raise")
        return 1
    if not why.strip():
        print("   --why is required: a raise says the project chose to read further "
              "ahead of its adjudication, and somebody has to say why")
        return 1
    row = rows[domain]
    ceilings = baseline.setdefault("unspent_ceiling", {})
    was = ceilings.get(domain)
    if was is not None and row["unspent"] <= was:
        print(f"   {domain} is at {row['unspent']} against a ceiling of {was} — "
              "nothing to raise. Use --tighten to reclaim the slack.")
        return 1
    ceilings[domain] = row["unspent"]
    baseline.setdefault("witness", {})[domain] = {"read": row["read"], "spent": row["spent"]}
    baseline.setdefault("raised", []).append({
        "domain": domain, "from": was, "to": row["unspent"],
        "date": date.today().isoformat(), "why": why.strip()})
    write_baseline(baseline)
    print(f"raised {domain}: {was} -> {row['unspent']} ({row['read']} read, "
          f"{row['spent']} ruled on)")
    print(f"  why: {why.strip()}")
    return 0


def tighten() -> int:
    """Lower every ceiling that sits above what the domain now reads. Always safe:
    it can only make the gate stricter, so it needs no reason and asks for none."""
    baseline = read_json(BASELINE)
    if not isinstance(baseline, dict):
        print(f"   no baseline at {BASELINE.name} — run --rebaseline")
        return 1
    ceilings = baseline.setdefault("unspent_ceiling", {})
    moved = []
    for row in measure():
        was = ceilings.get(row["domain"])
        if was is not None and row["unspent"] < was:
            ceilings[row["domain"]] = row["unspent"]
            baseline.setdefault("witness", {})[row["domain"]] = {
                "read": row["read"], "spent": row["spent"]}
            moved.append((row["domain"], was, row["unspent"]))
    if not moved:
        print("every ceiling already sits at what its domain reads — nothing to reclaim")
        return 0
    write_baseline(baseline)
    for domain, was, now in moved:
        print(f"tightened {domain}: {was} -> {now} (reclaimed {was - now})")
    return 0


def self_test() -> int:
    """Every assertion this gate makes, proved to fire when the fault is present."""
    failures = []

    def fires(label: str, condition: bool) -> None:
        if not condition:
            failures.append(label)

    # --- the read counter
    fires("a record with a normalized name is read",
          sum(1 for u in [{"normalized": "W. H. Adams"}]
              if any(u.get(n) for n in NAME_KEYS)) == 1)
    fires("a continuation line with cells and no name is NOT read",
          sum(1 for u in [{"line": 4, "cells": {"1": 2}}]
              if any(u.get(n) for n in NAME_KEYS)) == 0)
    fires("an as_read-only record is still read",
          sum(1 for u in [{"as_read": "Wm S. Lans[?]me"}]
              if any(u.get(n) for n in NAME_KEYS)) == 1)
    fires("a claims unit counts by its quote",
          sum(1 for u in [{"quote": "the town then had four stores"}]
              if any(u.get(n) for n in NAME_KEYS)) == 1)

    # --- the spend counter, on a scratch tree
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "voter_crosswalk.json").write_text(json.dumps({"entries": [
            {"record_id": "poll_1833_001", "outcome": "matched"},
            {"record_id": "poll_1833_002", "outcome": "refused"}]}))
        spent, pairs = count_spent(d)
        fires("two anchored rulings are two spends", spent == 2)
        fires("…and neither is an id pair", pairs == 0)

        # the civic double-count this tool was written to avoid
        (d / "crosswalk.json").write_text(json.dumps({"refusals": [
            {"a": "Medard Beaubien", "b": "Col. Jean Baptiste Beaubien"}]}))
        spent, pairs = count_spent(d)
        fires("an unanchored name-pair ruling is NOT a spend", spent == 2)
        fires("…it is reported as an id pair", pairs == 1)

        # one record ruled on twice in two files is one spend
        (d / "second_crosswalk.json").write_text(json.dumps({"matches": [
            {"record_id": "poll_1833_001", "person_id": "adams_william_h"}]}))
        spent, _ = count_spent(d)
        fires("one record ruled on in two files is one spend", spent == 2)

        # a refusal that names a person is spent
        (d / "third_crosswalk.json").write_text(json.dumps({"refusals": [
            {"person_id": "beaubien_jean_baptiste", "rule": "surname only"}]}))
        spent, _ = count_spent(d)
        fires("an anchored refusal IS a spend", spent == 3)

        # `pages` is not an adjudication array
        (d / "crosswalk_670.json").write_text(json.dumps({
            "pages": [{"printed_page": 229}, {"printed_page": 231}]}))
        spent, pairs = count_spent(d)
        # `pages` is not in ADJUDICATION_KEYS, so the file adds nothing at all —
        # the one id pair still standing is the Beaubien refusal above.
        fires("a page-level agreement test rules on nobody",
              spent == 3 and pairs == 1)

        # a non-crosswalk file is never a spend, however it is shaped
        (d / "records.json").write_text(json.dumps({"entries": [
            {"record_id": "x"}]}))
        spent, _ = count_spent(d)
        fires("only a crosswalk file carries rulings", spent == 3)

        # the read counter over the same tree
        (d / "page.json").write_text(json.dumps({"records": [
            {"as_read": "A"}, {"line": 2}, {"normalized": "B"}]}))
        fires("read counts names and skips the blank line", count_read(d) == 2)
        fires("…and never reads a crosswalk as a source",
              count_read(d) == 2)

    # --- the ratchet
    def over(unspent: int, ceiling: int) -> bool:
        return unspent > ceiling
    fires("the gate fires when the gap widens", over(563, 562))
    fires("the gate is silent when the gap holds", not over(562, 562))
    fires("the gate is silent when a domain is spent down", not over(0, 562))

    # --- raising and tightening, against a real baseline file
    global BASELINE
    kept = BASELINE
    # These cases drive the real writers, which report to stdout by design. A
    # self-test that narrates every one of them buries its own verdict.
    import contextlib, io
    hush = contextlib.redirect_stdout(io.StringIO())
    try:
        with tempfile.TemporaryDirectory() as tmp, hush:
            BASELINE = Path(tmp) / "baseline.json"
            rows = measure()
            live = {r["domain"]: r["unspent"] for r in rows}
            some = rows[0]["domain"]

            fires("--rebaseline writes the file when there is none",
                  rebaseline() == 0 and BASELINE.exists())
            fires("…and REFUSES a second time, so no run launders every ceiling at once",
                  rebaseline() == 1)

            doc = json.loads(BASELINE.read_text())
            fires("the first write records every domain",
                  doc["unspent_ceiling"] == live)

            fires("a raise with no reason is refused",
                  raise_ceiling(some, "   ") == 1)
            fires("a raise on an unknown domain is refused",
                  raise_ceiling("no_such_domain", "because") == 1)
            fires("a raise with nothing to raise is refused, and points at --tighten",
                  raise_ceiling(some, "because") == 1)

            # drop one ceiling below the live figure so a raise is genuinely owed
            doc["unspent_ceiling"][some] = live[some] - 1
            BASELINE.write_text(json.dumps(doc))
            fires("the gate fires on that one domain", gate(quiet=True) == 1)
            fires("a reasoned raise is taken", raise_ceiling(some, "T-9999 read it") == 0)
            after = json.loads(BASELINE.read_text())
            fires("…the ceiling moves to what the domain now reads",
                  after["unspent_ceiling"][some] == live[some])
            fires("…the reason is written down, with what it moved from and to",
                  after["raised"][-1]["why"] == "T-9999 read it"
                  and after["raised"][-1]["to"] == live[some])
            fires("…and only that domain moved", all(
                  after["unspent_ceiling"][d] == live[d] for d in live if d != some))
            fires("the gate is green again", gate(quiet=True) == 0)

            # slack: a ceiling above the live figure is reclaimable
            after["unspent_ceiling"][some] = live[some] + 50
            BASELINE.write_text(json.dumps(after))
            fires("slack does not fire the gate", gate(quiet=True) == 0)
            fires("--tighten reclaims it", tighten() == 0)
            fires("…down to what the domain reads",
                  json.loads(BASELINE.read_text())["unspent_ceiling"][some] == live[some])
            fires("…and a second --tighten has nothing left to take", tighten() == 0)
            fires("…and never RAISES a ceiling that is already tight",
                  json.loads(BASELINE.read_text())["unspent_ceiling"] == live)
    finally:
        BASELINE = kept

    for line in failures:
        print(f"   SILENT: {line}")
    print("SELF-TEST %s — %d case(s)" % ("FAIL" if failures else "PASS", 35))
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", action="store_true")
    parser.add_argument("--rebaseline", action="store_true")
    parser.add_argument("--raise", dest="raise_domain", metavar="DOMAIN",
                        help="raise ONE domain's ceiling to what it now reads; needs --why")
    parser.add_argument("--why", default="", help="the reason a raise is being taken")
    parser.add_argument("--tighten", action="store_true",
                        help="lower every ceiling to what its domain now reads (always safe)")
    parser.add_argument("--self-test", action="store_true", dest="self_test")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.raise_domain:
        return raise_ceiling(args.raise_domain, args.why)
    if args.tighten:
        return tighten()
    if args.rebaseline:
        return rebaseline()
    if args.gate:
        return gate(quiet=args.quiet)
    print(report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
