---
id: T-0180
title: The bake opens a content PR on every run, because the build stamp it writes is always dirty
state: open
epic: META
requested_by: steward
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The bake opens a content PR on every run, because the build stamp it writes is always dirty.

## What was seen

Four bake PRs open at once on 2026-08-24 — #349 (run 32688616908), #351 (32690517288),
#353 (32696112597), #354 (32696836806) — spanning 04:41 to 06:56 UTC. Every one of them
changes exactly TWO files and no geometry, no assets, no data:

    site/chicago/4d/build.json      | 6 +++---
    site/chicago/4d/walk/index.html | 2 +-

and the whole of that diff is the stamp:

    -  "version": "762fa99c",
    -  "built_utc": "2026-08-24T06:04:28Z",
    +  "version": "55fca619",
    +  "built_utc": "2026-08-24T06:32:39Z",

## Why it happens

`chicago-4d-bake.yml`'s "Push a bake branch" step decides whether the bake produced
anything with

    if [ -z "$(git status --porcelain)" ]; then ... changed=0

`build.json` carries `built_utc`, a wall-clock timestamp, and `version`, the head sha.
Both move on every run by construction, so the tree is ALWAYS dirty and `changed` is
always 1. The `changed=0` branch is unreachable in practice.

## Why it matters

The PR is the signal that a bake produced new content. That signal is dead — it fires
identically whether 300 structures were rebuilt or nothing at all was. A reviewer cannot
tell the two apart without diffing each branch by hand, which is what this ticket did.

It also queues: one PR per run, none self-closing, four in six hours once the nightly
started succeeding (T-0114/T-0165/T-0171). The pileup is a symptom; the dead signal is
the defect.

Note the determinism story is INTACT and this is evidence for it, not against it — the
geometry re-baked byte for byte across all four runs, which is exactly what
`assets/manifest.json`'s inputs-based determinism promises. Only the stamp moved.

## The fix, roughly

Decide `changed` on the content rather than on the whole tree: exclude the stamp files
from the dirtiness test, and if nothing else moved, skip the branch and the PR (and say
so in the log). The stamp still gets written and still ships with the next PR that
carries real content — it just stops being the thing that manufactures one.

Two traps worth stating before someone implements it:

- Do NOT stop writing the stamp. The gate screen reads it ("build 55fca619 · Aug 24,
  2026, 1:32 AM CT") and it is how a visitor and a bake report agree on what is live.
- The stamp can never be self-consistent with the commit that carries it: merging it
  changes the head sha it names. That is inherent, not a bug to chase.

## Acceptance

- A bake run over unchanged inputs pushes no branch, opens no PR, and logs why.
- A bake run that changes any geometry, sidecar, derivative or data file still opens one.
- Demonstrated by two consecutive runs on `dev` with no content change between them:
  the first may carry a stamp, the second opens nothing.
