#!/usr/bin/env python3
"""T-1124 — a judgement that is simply GONE, which no derivation can see.

On 10 September 2026 the merge lap pushed onto #1055 and
`data/research/land_sales/resident_rulings.json` conflicted. The file is
`hand_authored`; the lap's regex resolution took the branch's whole block for the
second conflict, and that branch had been cut before T-0850 and T-0990 cohort A
ruled. Forty entries left the file on one line, and twelve resident cards silently
got back a federal land purchase each had been ruled it could not have. #1073
restored them. This is the reason nobody was told.

`check.sh` was green on #1055 and on every commit after it, and it was RIGHT to be.
`read_land_sales.py --check` asks whether a ruling is WELL FORMED — that it names a
spelling the register holds, and a person the proposal named — and every surviving
ruling was. The eight that were left re-derived perfectly into a crosswalk perfectly
consistent with them. **A smaller rulings file is a legal rulings file**, and that is
the general shape: every gate this repository has re-derives DOWNSTREAM of its
hand-authored evidence, and a derivation cannot see a shrinking input. It just
derives less.

So this asks the one question a derivation cannot: is every judgement that was here
before still here? Two readings of "still here", both required:

  * BY IDENTITY — every (purchaser_as_read, resident_id) pair adjudicated at the
    merge base is adjudicated at HEAD. This is the strong one: it catches a swap,
    where one judgement leaves and another arrives and the total never moves.
  * BY COUNT — the adjudicated total may not fall. Redundant while the keys are
    unique, and kept because it is the number a person reads, and because it is what
    the incident is remembered by: 49 -> 9.

`ruled[]` and `retired[]` are counted TOGETHER, so retiring a ruling is a MOVE and
not a loss.

THE COMPARISON IS AGAINST THE MERGE BASE, never against a number committed beside the
file. A branch that dropped forty entries and also edited a total downwards would
satisfy any self-consistent check; it cannot satisfy this one, because the figure it
is held to lives in git and not in the tree it is editing.

**A DELIBERATE REMOVAL IS STILL POSSIBLE AND MUST STATE ITSELF.** A judgement that
should never have been made does not get deleted — it moves to `withdrawn[]`, which
this counts alongside `ruled[]` and `retired[]` and which requires a `reason` and the
`ticket` that decided it, exactly the way `retired[]` already carries its reason. The
total therefore never falls, and the record of what left says why. That is the same
trade the liberty ledger and the refusal lists make everywhere else in this project.

    tools/check_rulings_not_lost.py              the gate (base defaults to origin/dev)
    tools/check_rulings_not_lost.py --base REF   hold it to a different base
    tools/check_rulings_not_lost.py --self-test  prove the refusal fires

TWO STATES, deliberately different — T-1083's lesson, that a gate may not count a
skip as a pass:

  * `C4D_GATE_REQUIRE_BASE=1` (the workflow sets it) — a base ref that will not
    resolve is RED. In CI it always resolves; `actions/checkout` is pinned to
    `fetch-depth: 0`, which fetches every branch.
  * unset (an agent sandbox, a laptop, a shallow clone) — the same absence is a
    WARNING that names what went unasked, and the gate goes on.

REGISTRY, below: one entry per guarded file. The mechanism is already general; what
each new file needs is a READING of which of its arrays hold a judgement and which
hold a transcription. That reading is T-1125 and is deliberately not done here.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent  # chicago/4d -> the monorepo root, which git speaks in

# path (repo-relative) -> what a judgement is in that file.
#   arrays  : the lists that hold one. Counted together; a move between them is not a loss.
#   identity: the fields that name one, in order. Their tuple is the key.
#   stated  : the array a deliberate withdrawal moves INTO, counted with the rest.
#   requires: the fields a `stated` entry must carry for the removal to have stated itself.
REGISTRY = {
    "chicago/4d/data/research/land_sales/resident_rulings.json": {
        "arrays": ["ruled", "retired", "withdrawn"],
        "identity": ["purchaser_as_read", "resident_id"],
        "stated": "withdrawn",
        "requires": ["reason", "ticket"],
    },
}


class Absent(Exception):
    """the file did not exist at that ref — a first commit, not a loss."""


def git(*args, ok=(0,)):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if r.returncode not in ok:
        return None
    return r.stdout


def resolve_base(explicit=None):
    """the first ref that exists, in the order a run actually has one."""
    candidates = []
    if explicit:
        candidates.append(explicit)
    elif os.environ.get("C4D_RULINGS_BASE"):
        candidates.append(os.environ["C4D_RULINGS_BASE"])
    else:
        if os.environ.get("GITHUB_BASE_REF"):
            candidates.append("origin/" + os.environ["GITHUB_BASE_REF"])
        candidates += ["origin/dev", "dev", "origin/main"]
    for ref in candidates:
        if git("rev-parse", "--verify", "--quiet", ref + "^{commit}") is not None:
            return ref, candidates
    return None, candidates


def at_ref(path, ref):
    """the file's JSON at `ref`, or Absent if the ref did not carry it."""
    out = git("show", f"{ref}:{path}")
    if out is None:
        raise Absent(path)
    return json.loads(out)


def in_tree(path):
    p = REPO / path
    if not p.exists():
        raise Absent(path)
    return json.loads(p.read_text(encoding="utf-8"))


def adjudications(doc, spec):
    """every judgement in `doc`, as key -> the array it sits in."""
    found = {}
    for name in spec["arrays"]:
        for entry in doc.get(name) or []:
            key = tuple(str(entry.get(f, "")) for f in spec["identity"])
            found.setdefault(key, name)
    return found


def malformed_withdrawals(doc, spec):
    """a withdrawal that does not say why is not a stated removal."""
    out = []
    for entry in doc.get(spec["stated"]) or []:
        key = " / ".join(str(entry.get(f, "?")) for f in spec["identity"])
        missing = [f for f in spec["requires"] if not str(entry.get(f, "")).strip()]
        if missing:
            out.append(f"{key} — no {', '.join(missing)}")
    return out


def compare(path, spec, base_doc, head_doc):
    """the whole judgement, as (failures, note). base_doc None = nothing to compare."""
    fails = []
    for bad in malformed_withdrawals(head_doc, spec):
        fails.append(f"{path}: a withdrawal that states no reason is a deletion: {bad}")

    head = adjudications(head_doc, spec)
    if base_doc is None:
        return fails, f"{path}: {len(head)} adjudication(s); no base copy to compare"

    base = adjudications(base_doc, spec)
    gone = sorted(k for k in base if k not in head)
    if gone:
        fails.append(
            f"{path}: {len(gone)} judgement(s) adjudicated at the base are GONE — "
            "a ruling leaves by moving into "
            f"{spec['stated']}[] with a reason, never by being deleted:")
        for k in gone[:12]:
            fails.append(f"        · {' / '.join(k)}  (was in {base[k]}[])")
        if len(gone) > 12:
            fails.append(f"        · …and {len(gone) - 12} more")
    if len(head) < len(base):
        fails.append(
            f"{path}: the adjudicated total FELL, {len(base)} -> {len(head)}, "
            f"counting {' + '.join(spec['arrays'])} together")
    return fails, f"{path}: {len(base)} -> {len(head)} adjudication(s), none lost"


def run(base_ref, registry=REGISTRY, quiet=False):
    """0 green, 1 red. base_ref None means there was nothing to compare against."""
    fails = []
    for path, spec in registry.items():
        try:
            head_doc = in_tree(path)
        except Absent:
            fails.append(f"{path}: the registry names a file this tree does not carry")
            continue
        base_doc = None
        if base_ref:
            try:
                base_doc = at_ref(path, base_ref)
            except Absent:
                pass
        f, note = compare(path, spec, base_doc, head_doc)
        fails += f
        if quiet:
            continue
        # A file says ONE thing — its clean note, or its failures. Never both: a
        # transcript that opens "none lost" and then lists what was lost is the kind
        # of line three tickets have been filed against (T-0763).
        if f:
            for line in f:
                print(line if line.startswith("      ") else f"   FAIL  {line}")
        else:
            print(f"   ok    {note}")
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", help="the ref to hold this tree to (default: origin/dev)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()

    ref, tried = resolve_base(args.base)
    if ref is None:
        required = bool(os.environ.get("C4D_GATE_REQUIRE_BASE"))
        print(f"   {'FAIL ' if required else 'WARN '} no base ref resolved "
              f"(tried {', '.join(tried)}), so nothing can say whether a judgement left")
        for path in REGISTRY:
            print(f"            · {path} went unasked")
        print("   " + ("FAIL  a GATE may not count a skip as a pass — fetch the base ref"
                       if required else
                       "WARN  this is a sandbox or a shallow clone, so the gate goes on. "
                       "CI sets C4D_GATE_REQUIRE_BASE=1 and would be red here."))
        return 1 if required else 0

    merge_base = (git("merge-base", ref, "HEAD") or "").strip()
    if not merge_base:
        # A detached or unrelated HEAD: the ref resolves but shares no history. Hold to
        # the ref itself rather than to nothing — stricter, and never wrong.
        merge_base = ref
    print(f"   ok    base {ref} at {merge_base[:9]}")
    return run(merge_base)


# ---------------------------------------------------------------------------
# the self-test — the check.sh convention (T-0763): prove the refusal FIRES.

INCIDENT = {
    "before": "07a6a1b04",   # 49 ruled, 0 retired
    "after": "02ce7d97a",    # 8 ruled, 1 retired — forty judgements gone
    "restored": "2e5aa8a02",  # 47 ruled, 2 retired — the same 49, two of them moved
}
LAND_SALES = "chicago/4d/data/research/land_sales/resident_rulings.json"


def _pair(base_ref, head_ref):
    spec = REGISTRY[LAND_SALES]
    return compare(LAND_SALES, spec, at_ref(LAND_SALES, base_ref), at_ref(LAND_SALES, head_ref))[0]


def self_test():
    ok = True
    spec = REGISTRY[LAND_SALES]

    def check(cond, bad):
        nonlocal ok
        if not cond:
            print(f"   FAIL self-test {bad}")
            ok = False

    have_history = all(git("rev-parse", "--verify", "--quiet", c + "^{commit}")
                       for c in INCIDENT.values())
    if have_history:
        print("   fires: the #1055 incident itself — 49 adjudications down to 9")
        broke = _pair(INCIDENT["before"], INCIDENT["after"])
        check(broke, "the commits that lost forty rulings passed the check")
        check(any("GONE" in f for f in broke), "the incident failed for some other reason")
        print("   passes: #1073's restoration against the same base — 47 + 2 is the same 49")
        check(not _pair(INCIDENT["before"], INCIDENT["restored"]),
              "the restored tree was called a loss")
        print("   passes: a tree against itself")
        check(not _pair(INCIDENT["restored"], INCIDENT["restored"]),
              "a tree was called a loss against itself")
    else:
        print("   WARN  the #1055 commits are not in this clone (shallow?) — "
              "the fixture pair went unasked")

    # The synthetic half, which needs no history and so always runs.
    base = in_tree(LAND_SALES)
    print("   fires: one entry removed from the tree under test")
    cut = json.loads(json.dumps(base))
    cut["ruled"] = cut["ruled"][1:]
    check(compare(LAND_SALES, spec, base, cut)[0], "a removed ruling was not a failure")

    print("   fires: a swap — one judgement out, one in, and the total never moves")
    swap = json.loads(json.dumps(base))
    swap["ruled"] = swap["ruled"][1:] + [dict(swap["ruled"][0], purchaser_as_read="A STRANGER")]
    check(len(adjudications(swap, spec)) == len(adjudications(base, spec)),
          "the swap fixture moved the total, so it is not testing identity")
    check(compare(LAND_SALES, spec, base, swap)[0], "a swapped judgement passed on count alone")

    print("   passes: the same ruling RETIRED — a move between the counted arrays")
    moved = json.loads(json.dumps(base))
    moved["retired"] = moved["retired"] + [moved["ruled"][0]]
    moved["ruled"] = moved["ruled"][1:]
    check(not compare(LAND_SALES, spec, base, moved)[0], "retiring a ruling was called a loss")

    print("   passes: a ruling WITHDRAWN with a reason and the ticket that decided it")
    withdrawn = json.loads(json.dumps(base))
    withdrawn["withdrawn"] = [dict(withdrawn["ruled"][0],
                                   reason="the register row was a second hand's marginal",
                                   ticket="T-1124")]
    withdrawn["ruled"] = withdrawn["ruled"][1:]
    check(not compare(LAND_SALES, spec, base, withdrawn)[0],
          "a stated withdrawal was refused")

    print("   fires: the same withdrawal with no reason written")
    silent = json.loads(json.dumps(withdrawn))
    silent["withdrawn"] = [{k: v for k, v in silent["withdrawn"][0].items() if k != "reason"}]
    check(compare(LAND_SALES, spec, base, silent)[0],
          "a withdrawal that states nothing was accepted as a stated removal")

    print("   ok: the identity fields still name a unique judgement on dev")
    check(len(adjudications(base, spec))
          == sum(len(base.get(a) or []) for a in spec["arrays"]),
          "two judgements share an identity key, so a loss could hide behind a duplicate")

    print("   ok: every registered file's arrays and identity fields exist in it")
    for path, s in REGISTRY.items():
        doc = in_tree(path)
        check(any(isinstance(doc.get(a), list) for a in s["arrays"]),
              f"{path} carries none of the arrays the registry names")
        check(s["stated"] in s["arrays"],
              f"{path}: the stated-withdrawal array is not one of the counted ones")

    # THE WORKFLOW IS HALF OF THIS CHECK, so it is asserted rather than assumed —
    # check_gate_readers.py's rule, for the same reason. The comparison needs a base
    # ref in the clone, which is `fetch-depth: 0`, and it needs the absence of one to
    # be RED in CI, which is C4D_GATE_REQUIRE_BASE. Either one quietly removed turns
    # this step into a skip that counts as a pass.
    wf = REPO / ".github/workflows/chicago-4d-check.yml"
    if wf.exists():
        src = wf.read_text(encoding="utf-8")
        print("   ok: the gate workflow still fetches a base ref and requires one")
        check("fetch-depth: 0" in src,
              "the gate workflow no longer fetches history, so no base ref will resolve")
        check("C4D_GATE_REQUIRE_BASE" in src,
              "the gate workflow no longer requires a base ref, so CI counts the skip as a pass")
    else:
        print("   WARN  the gate workflow is not in this checkout — its half went unasked")

    print("   self-test: a lost judgement fails, a moved or stated one does not"
          if ok else "   self-test: FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
