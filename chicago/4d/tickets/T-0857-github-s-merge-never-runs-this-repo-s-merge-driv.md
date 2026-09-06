---
id: T-0857
title: GitHub's merge never runs this repo's merge drivers, so every PR reads as conflicting and auto-merge can never fire
state: open
epic: META
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

GitHub's server-side merge never runs a custom merge driver, so every PR that touches a
`merge=generated` file reads as CONFLICTING to the platform however cleanly it merges here.

**MEASURED 2026-09-06, and this is the whole of it — same branch, same merge, two answers:**

| | result |
|---|---|
| locally, after `bash tools/setup-merge-drivers.sh` | **0 conflicts, clean** |
| GitHub *Update branch* / auto-merge on the identical merge | **merge conflict** |

Tested on PR #940, cut after T-0831. `.gitattributes` can NAME a driver; only a clone that has
run `setup-merge-drivers.sh` can EXECUTE one, and GitHub has run nothing.

**WHAT IT COSTS, and it is the cause of the 2026-09-05/06 backlog rather than a footnote.**
Sixteen PRs stood open at 02:00Z, every one of them GREEN and every one with auto-merge
ARMED by its own run. None could land. Auto-merge cannot fire on a PR GitHub calls
conflicting, *Update branch* refuses it, and the only thing that ever works is a human or
agent doing a lap in a clone that has the drivers — which is why the pile grows at exactly
the rate the lane opens PRs, and shrinks only when someone laps by hand. T-0831 IS WORKING;
it is invisible to the only merge that decides mergeability.

**A SECOND TRAP UNDERNEATH, and it is permanent for the branches it catches.** A merge driver
that lives in the repo cannot resolve a merge on a branch cut BEFORE it: `tools/merge-generated.mjs`
is absent from those trees, the driver cannot run, and the five files conflict on every lap
forever. #841, #911, #913, #914, #917, #921, #926 and the closed #850 are all in that class.

**Acceptance — one of these, argued and measured, not all three:**

1. **Take the generated artifacts off the PR surface.** Stop tracking `BOARD.md`, both
   `tickets.json`, `build.json`, `walk/index.html` and the smoke ledger; regenerate them on
   `dev` after each merge. Nothing to conflict, no driver needed, auto-merge works unaided.
   The cost is `check_published` and the staleness gate, which currently require a branch to
   carry a consistent mirror — they would gate `dev` instead. This is the version where the
   problem stops existing, and it is the one to beat.
2. **A janitor that laps in CI.** A workflow that, for each open `steward/*` PR, registers the
   drivers, merges the base, regenerates and pushes. Drivers work fine in CI. **It needs a PAT
   this repo does not have**: a push made with `GITHUB_TOKEN` does not re-trigger `gate`, so the
   PR would sit with no check on its new head and auto-merge would still not fire. Adding
   `STEWARD_PAT` here is part of the ticket if this route is taken.
3. **Make the five files merge textually** — no driver. Only worth it if a shape exists that a
   default merge resolves, and JSON and HTML mostly do not, so measure before proposing it.

Whichever is taken, **say so in `.gitattributes`**: the file currently promises a conflict-free
merge that only holds on a developer's machine, and the next person to read it will believe it.

**Links:** T-0831 (the drivers, working) · T-0813 (the six build products) · T-0809 (the
janitor) · T-0802 and T-0820 (the same family — nothing here is visible before a PR merges) ·
PR #940 (the measurement).

---

## WORKED, 2026-09-06 — acceptance 2, and the measurement that made it possible

The owner added `STEWARD_PAT` to this repo and chose the janitor route.
`.github/workflows/chicago-4d-pr-lap.yml` + `.github/steward/pr-lap.sh` bring every open
non-draft, non-`hold` PR up to date and push; they never merge a PR, they only remove the
reason GitHub calls it conflicting, and auto-merge does the rest.

**The second trap is solved, and this is the part that was not obvious.** Registering dev's
merge drivers by absolute path is NOT enough on a branch cut before T-0831: git reads `merge=`
out of the .gitattributes in the WORKING TREE, so an old branch routes nothing to a driver
however well it is registered. `$GIT_DIR/info/attributes` outranks the tree, so the lap injects
dev's rules there and merges every branch under them.

    measured on PR #841, cut before T-0831
      drivers from the branch          REAL(3) + 5 generated  = 8 conflicts
      drivers from dev, alone          8 conflicts — attributes still the branch's
      drivers AND attributes from dev  3 conflicts, and all three are real

**What it does NOT fix, measured across all sixteen open PRs on 2026-09-06.** Only #913 and
#940 came out clean; every other PR has a genuine content disagreement with dev — crosswalks,
household cards, minting tools, a research baseline — and the lap REFUSES those rather than
picking a side, leaving one comment naming the files. So the lap is worth having for what it
stops recurring, not as a drain: **it keeps tomorrow's PRs mergeable; it does not rescue
today's, which want the runs that own their tickets.**

**Still open under acceptance 1**, and still the better answer: taking the generated artifacts
off the PR surface entirely would mean no drivers, no attributes injection, no PAT and no lap.
This ticket stays open for it.

**A follow-up the lap wants**: a DERIVED tier below the generated one, for files a tool
rebuilds from sources (`identity_master.json`, `source_coverage.json`, `register_1835.json`,
`street_face_adoptions.json`, the Newberry leads) — #880 already regenerated exactly those by
hand rather than reconciling them. `*_baseline.json` must stay OUT of it: a ratchet is a
measurement, and regenerating one silently lowers a bar.
