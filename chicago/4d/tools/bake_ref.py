#!/usr/bin/env python3
"""Which tree does the content bake actually build? (T-0454)

`chicago-4d-bake.yml` opened with a checkout and then, unconditionally, this:

    if git ls-remote --exit-code --heads origin dev >/dev/null 2>&1; then
      git checkout -B dev origin/dev
    fi

For the nightly that is right — the schedule always fires on the default branch,
and the bake's PR goes to `dev`, so branching off `main` would put every commit
already promoted past into the diff. For a **dispatch against a branch it is a
silent discard**: the run is handed a ref, throws it away, and bakes `dev`.

That is the whole of T-0454, and it is why the gate and the bake could both be
right while disagreeing. Reproduced on 2026-09-03 on `steward/t-0429-...`'s
fault pattern, one mesh parameter moved on a branch:

    tools/validate.py --stale   FAIL  bates_auction_room__frame_1834.glb is STALE
                                      inputs now hash e2c58b0e5ee8, mesh built from 010608142cf0
    the step above                    HEAD t0454-repro fbebc203 -> dev 8ecfcb57
                                      the changed parameter: 0 occurrences
    build.py --only <id>              rebuilds it in 0.7 s and clears the gate
                                      — WHEN IT IS SHOWN THE TREE THAT CARRIES THE CHANGE

So `build.py` never skips; it was never asked. It rebuilt a fresh `dev`, produced
byte-identical output, and `bake_content_changed.py` reported "no CONTENT" —
correctly, about a tree nobody had asked about. Two right answers to two
different questions, and the branch's stale asset untouched. The remedy the gate
prints ("Re-bake it — tools/bake.sh, or the chicago-4d-bake workflow") was true
of the first and false of the second.

## The rule

Bake `dev` when the run has no tree of its own to speak for:

  * the **schedule**, which always fires on the default branch; and
  * a run whose ref IS the production tier, because nothing may PR into `main`
    (docs/PIPELINE.md) — a bake there would have nowhere to land.

Otherwise bake **the ref the run was started on**, and open the PR against that
same ref. A dispatch names a tree because it means that tree.

The tiers are read from `.github/pipeline.json` rather than spelled `dev`/`main`
here, so the day the pipeline grows a stage tier this does not quietly disagree
with the manifest that every other reader uses.

    tools/bake_ref.py --event <name> --ref <ref> [--github]
    tools/bake_ref.py --self-test
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent          # chicago/4d
REPO = ROOT.parent.parent                                      # the repo root
PIPELINE = REPO / ".github" / "pipeline.json"
WORKFLOW = REPO / ".github" / "workflows" / "chicago-4d-bake.yml"

# The events that arrive without a tree of their own. `schedule` fires on the
# default branch by GitHub's definition, never on the branch anyone cares about.
REFLESS_EVENTS = {"schedule"}


def tiers(pipeline_path=None):
    """(integration, production) from the pipeline manifest."""
    data = json.loads((pipeline_path or PIPELINE).read_text(encoding="utf-8"))
    t = data["tiers"]
    return t[0], t[-1]


def short(ref):
    """`refs/heads/x` and `x` both name the branch x."""
    for prefix in ("refs/heads/", "refs/tags/"):
        if ref.startswith(prefix):
            return ref[len(prefix):]
    return ref


def resolve(event, ref, dev_exists, integration="dev", production="main"):
    """The branch to bake, and why. Pure — the self-test is the point.

    Returns (branch, reason).
    """
    name = short(ref or "")
    if not dev_exists:
        # The pipeline is not activated. Everything bakes what it was given, and
        # the PR goes there; this is the pre-2026-08-14 shape.
        return name or production, "no dev ref — baking the ref this run was started on"
    if event in REFLESS_EVENTS:
        return integration, f"{event} carries no ref of its own — baking {integration}"
    if name == production:
        return integration, (f"{production} is the production tier and nothing may PR into it "
                             f"(docs/PIPELINE.md) — baking {integration}")
    return name, f"baking {name}, the ref this run was started on"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--event", default=os.environ.get("GITHUB_EVENT_NAME", ""))
    ap.add_argument("--ref", default=os.environ.get("GITHUB_REF", ""))
    ap.add_argument("--dev-exists", choices=["0", "1"])
    ap.add_argument("--github", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    integration, production = tiers()
    if args.dev_exists is not None:
        dev_exists = args.dev_exists == "1"
    else:
        import subprocess
        dev_exists = subprocess.run(
            ["git", "ls-remote", "--exit-code", "--heads", "origin", integration],
            cwd=REPO, capture_output=True).returncode == 0

    branch, reason = resolve(args.event, args.ref, dev_exists, integration, production)
    # The REASON goes to stderr and the ANSWER to stdout, always — so the caller
    # can read the branch with `$(...)` whether or not it also wants the step
    # output, and the log still says why. A caller that had to grep
    # $GITHUB_OUTPUT back out would break the day another step appended to it.
    print(reason, file=sys.stderr)
    print(branch)
    if args.github and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"branch={branch}\n")
            fh.write(f"dev_exists={'1' if dev_exists else '0'}\n")
    return 0


# --- the self-test ---------------------------------------------------------
# Pure inputs, so this needs no runner, no remote and no Blender. The drift
# guards at the end are the other half: a correct decision the workflow has
# stopped asking for is the same bug wearing a different hat.

def self_test():
    cases, failed = [], 0

    def case(name, got, want):
        nonlocal failed
        ok = got == want
        cases.append((ok, name, got, want))
        if not ok:
            failed += 1

    # THE FAULT. This is the one that cost PR #597 and produced T-0454.
    case("a dispatch against a branch bakes THAT BRANCH",
         resolve("workflow_dispatch", "refs/heads/steward/t-0429-south-water-lasalle", True)[0],
         "steward/t-0429-south-water-lasalle")
    case("a push to a branch bakes that branch, not dev",
         resolve("push", "refs/heads/steward/t-0121-stage-recut", True)[0],
         "steward/t-0121-stage-recut")

    # …and the nightly's behaviour is UNCHANGED, which is the other half of the
    # fix: it is the reason the old line was written and it still holds.
    case("the nightly bakes dev", resolve("schedule", "refs/heads/main", True)[0], "dev")
    case("a run whose ref is main bakes dev — nothing may PR into main",
         resolve("workflow_dispatch", "refs/heads/main", True)[0], "dev")
    case("a push to dev bakes dev", resolve("push", "refs/heads/dev", True)[0], "dev")

    # Before the pipeline was activated there was no dev, and the old line said so.
    case("with no dev ref, the nightly bakes what it was given",
         resolve("schedule", "refs/heads/main", False)[0], "main")
    case("with no dev ref, a dispatch bakes its own branch",
         resolve("workflow_dispatch", "refs/heads/topic", False)[0], "topic")

    case("a bare branch name is a branch name", short("dev"), "dev")
    case("refs/heads/ is stripped", short("refs/heads/a/b"), "a/b")

    # The tiers come from the manifest every other reader uses.
    case("the tiers are read from .github/pipeline.json", tiers(), ("dev", "main"))

    # --- the drift guards --------------------------------------------------
    # Comments stripped first: the workflow step quotes the line it replaced, and
    # a guard that reads prose cannot tell a fix from a description of one.
    wf = WORKFLOW.read_text(encoding="utf-8")
    live = "\n".join(l for l in wf.splitlines() if not l.lstrip().startswith("#"))
    case("the workflow no longer hard-checks-out dev",
         "git checkout -B dev origin/dev" in live, False)
    case("the workflow asks this script which ref to bake",
         "tools/bake_ref.py" in live, True)
    case("the PR base follows the ref that was baked, not a literal dev",
         "--base dev" in live, False)
    case("…and the base comes from the bake job's own output",
         "needs.bake.outputs.base" in live, True)

    for ok, name, got, want in cases:
        if ok:
            print(f"  ok    {name}")
        else:
            print(f"  FAIL  {name}\n        got  {got}\n        want {want}")
    if failed:
        print(f"SELF-TEST FAIL — {failed} of {len(cases)} case(s)")
        return 1
    print(f"SELF-TEST PASS — the bake builds the ref it was given, the nightly "
          f"still builds dev, and the workflow still asks ({len(cases)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
