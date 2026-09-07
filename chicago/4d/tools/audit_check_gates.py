#!/usr/bin/env python3
"""T-0714 — every tool that can re-derive itself, and whether the gate ever asks it to.

    tools/audit_check_gates.py            the report: which --check modes check.sh runs
    tools/audit_check_gates.py --gate     fail if the ungated set has GROWN
    tools/audit_check_gates.py --write    re-record the baseline after a deliberate change
    tools/audit_check_gates.py --self-test

WHY THIS EXISTS. `crosswalk_census_1840_heads.py --check` had been red on `dev` for an
unknown number of days when T-0714 measured it: 498 heads adjudicated on disk against
788 read off the pages. Every sibling crosswalk IS gated and fails the moment its
committed file stops re-deriving; this one alone was not, so 290 heads of reading sat
un-adjudicated without one red build. The fault is not the crosswalk. The fault is that
NOTHING ASKED whether a tool with a `--check` mode is wired into `tools/check.sh`, so the
answer could only ever be found by hand, one tool at a time, by someone who suspected it.

WHAT THIS ASSERTS, AND WHAT IT DOES NOT. It does not assert that every `--check` runs in
the gate: some of these are one-shot passes whose inputs are gone, some are slow, and a
few are red today for reasons that are their own tickets (T-0691 holds
`mint_letter_list_residents.py --check`, which is red because a cohort drifted, not
because this file is wrong). Gating them is work with rulings in it and it is not free.
What this asserts is a RATCHET: the set of `--check`-capable tools the gate never runs
may SHRINK freely and may not GROW. A new derivation arrives gated, or it arrives with a
deliberate line in `data/research/check_gate_baseline.json` saying why not.

HOW IT READS check.sh. A tool counts as gated when `tools/check.sh` invokes it with
`--check` anywhere — the same string a reader would grep for. A tool check.sh runs under
some OTHER mode (`--gate`, `--self-test`, `--offline`) is still counted UNGATED here, and
the report says which modes it does run, because those modes prove different things: a
self-test proves the assertions fire, and only `--check` proves the committed file still
follows from its inputs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK_SH = ROOT / "tools" / "check.sh"
BASELINE = ROOT / "data" / "research" / "check_gate_baseline.json"
SEARCH = ("tools/*.py", "generators/*.py", "tools/*.mjs")


def scripts() -> list[Path]:
    out: list[Path] = []
    for pattern in SEARCH:
        out.extend(sorted(ROOT.glob(pattern)))
    return out


def survey() -> dict:
    """Every script advertising a --check flag, and how check.sh invokes it."""
    text = CHECK_SH.read_text()
    capable, ungated = [], []
    for path in scripts():
        body = path.read_text(errors="replace")
        if not re.search(r"""["']--check["']""", body):
            continue
        rel = path.relative_to(ROOT).as_posix()
        capable.append(rel)
        if re.search(re.escape(rel) + r"[^\n]*--check", text):
            continue
        modes = sorted(set(re.findall(re.escape(rel) + r"\s+(--[a-z-]+)", text)))
        ungated.append({"tool": rel, "other_modes_in_check_sh": modes})
    return {"check_capable": capable, "ungated": ungated}


def load_baseline() -> dict:
    if not BASELINE.exists():
        return {"ungated": []}
    return json.loads(BASELINE.read_text())


def report() -> int:
    found = survey()
    print("TOOLS WITH A --check MODE: %d" % len(found["check_capable"]))
    print("RUN WITH --check BY tools/check.sh: %d"
          % (len(found["check_capable"]) - len(found["ungated"])))
    print("NOT RUN WITH --check BY tools/check.sh: %d" % len(found["ungated"]))
    for row in found["ungated"]:
        other = (" ".join(row["other_modes_in_check_sh"])
                 if row["other_modes_in_check_sh"] else "not run in check.sh at all")
        print("  %-52s %s" % (row["tool"], other))
    return 0


def gate(quiet: bool = False) -> int:
    found = {row["tool"] for row in survey()["ungated"]}
    known = {row["tool"] for row in load_baseline().get("ungated", [])}
    new = sorted(found - known)
    gone = sorted(known - found)
    for tool in new:
        print("BAD: %s has a --check mode that tools/check.sh never runs, and it is not "
              "in %s. Gate it, or record why not."
              % (tool, BASELINE.relative_to(ROOT)))
    if new:
        return 1
    if not quiet:
        print("OK: %d ungated --check mode(s), none new%s"
              % (len(found),
                 "; %d newly gated since the baseline" % len(gone) if gone else ""))
    return 0


def write() -> int:
    found = survey()
    doc = {
        "schema": 1,
        "ticket": "T-0714",
        "what": "The tools carrying a --check mode that tools/check.sh does not run with "
                "--check. A ratchet, not a target: this list may shrink, and "
                "audit_check_gates.py --gate fails when it grows.",
        "how_to_change_it": "Gate the tool in tools/check.sh and re-run --write, or, if "
                            "it genuinely cannot be gated, re-run --write in the same "
                            "commit that says why in the PR.",
        "counts": {"check_capable": len(found["check_capable"]),
                   "ungated": len(found["ungated"])},
        "ungated": found["ungated"],
    }
    BASELINE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print("wrote %s — %d of %d --check-capable tool(s) ungated"
          % (BASELINE.relative_to(ROOT), len(found["ungated"]),
             len(found["check_capable"])))
    return 0


def self_test() -> int:
    failures = []

    def expect(label, got, want):
        if got != want:
            failures.append("%s: got %r, wanted %r" % (label, got, want))

    found = survey()
    expect("the survey finds the gate's own siblings",
           "tools/apply_census_1840_bridges.py" in found["check_capable"], True)
    expect("a tool check.sh runs with --check is not reported ungated",
           "tools/apply_census_1840_bridges.py" in {r["tool"] for r in found["ungated"]},
           False)
    expect("the crosswalk this ticket gated is no longer ungated",
           "tools/crosswalk_census_1840_heads.py" in {r["tool"] for r in found["ungated"]},
           False)
    expect("a tool run only under another mode still counts as ungated",
           next((r["other_modes_in_check_sh"]
                 for r in found["ungated"]
                 if r["tool"] == "tools/mint_letter_list_residents.py"), None),
           ["--gate", "--self-test"])
    expect("the baseline covers every ungated tool found today",
           sorted({r["tool"] for r in found["ungated"]}
                  - {r["tool"] for r in load_baseline().get("ungated", [])}), [])
    for line in failures:
        print("FAIL: %s" % line)
    print("self-test: %d assertion(s) failed" % len(failures))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.write:
        return write()
    if args.gate:
        return gate(args.quiet)
    return report()


if __name__ == "__main__":
    sys.exit(main())
