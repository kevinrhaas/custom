---
id: T-0729
title: check.sh is red on dev: six cohort manifests read stale against their own selectors, so every branch inherits a failing gate
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

check.sh is red on dev: six cohort manifests read stale against their own selectors, so every branch inherits a failing gate.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured 2026-09-05 on a clean worktree of `origin/dev` at `06a0a9ec`, with nothing applied:
`./tools/check.sh` exits 1. The dev gate is `check.sh` and nothing else
(`docs/PIPELINE.md`), so **every branch cut from dev inherits a failing gate** and no PR can
show a green one on its own merits.

The steps that fail on unmodified `dev`:

- `data/research/residents/pilot_75_cohort.json`, `pass_02_75_cohort.json` and
  `pass_03_75_cohort.json` read **stale** against `select_resident_research_pilot.py`,
  `_pass_2.py` and `_pass_3.py` — the selectors re-derive something different from what is
  committed. Passes 4 and 5 are current, so whatever moved under them moved recently.
- `pass_13_76_cohort.json`, `pass_14_76_cohort.json`, `pass_15_76_cohort.json` — the same,
  and these three are the cohorts T-0508/T-0509/T-0510 are being researched against right
  now.
- the seven cross streets have 34 platted faces, got 0; `blk_washington_clark` stands off
  the modelled ground (SOUTHERN GROUND FAIL); the far-timber census disagrees with what is
  banked (ROADMAP R-BUG5).

**The manifests are frozen on purpose** — a cohort is fixed before it is researched — so the
answer is emphatically NOT to regenerate them until it is known what moved. A cohort that
silently re-derives to a different 75 people invalidates the research already filed against
it. Find the change that moved the population frame first; the fix may be to re-freeze the
selector's inputs rather than the manifest.

**Why it matters beyond the red:** a gate that is already failing cannot tell anyone that
their branch broke something. T-0511 could only verify itself by diffing its failure set
against dev's line by line, which is not a gate.

**Acceptance:** `check.sh` exits 0 on `dev`, or every remaining red is a named, ticketed
exception the gate itself reports as expected rather than as a failure.
