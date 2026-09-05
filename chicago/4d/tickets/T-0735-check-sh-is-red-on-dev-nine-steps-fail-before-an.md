---
id: T-0735
title: check.sh is red on dev: nine steps fail before any branch touches them, five because finishing a research cohort is what makes its own gate fire
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

check.sh is red on dev: nine steps fail before any branch touches them, five because finishing a research cohort is what makes its own gate fire.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured 2026-09-05** on a clean `origin/dev` worktree, before any branch touched it —
`./tools/check.sh` exits 1 with nine failing steps:

```
sidecars derived from data/
the 75-person real-resident research cohort is fixed
the second non-overlapping 75-person research cohort is fixed
the third non-overlapping 75-person research cohort is fixed
the thirteenth research cohort is fixed
the fourteenth research cohort is fixed
the fifteenth research cohort is fixed
the civic, church, press and book residents re-derive from the ladder
the regraded residents re-derive from the ladder too
```

The dev gate IS `check.sh` and nothing else (`docs/PIPELINE.md`), so every steward branch
now merges at parity with a red gate instead of on a green one, and the question "is this
red mine?" costs a worktree and ten minutes on every run. T-0510 paid it.

**Five of the nine are one bug.** `select_resident_research_*.py --gate` refuses a cohort
whose members "already carry a research row" — and researching the cohort is precisely what
gives every member one. The check is meaningful at SELECTION time and self-refuting after
the pass runs. The fix is narrow: `researched_ids()` should ignore a row whose
`resident_research.ticket` is the cohort's own ticket, so a row from ANOTHER pass still
fails and completion does not. Four files carry the same shape: `select_resident_research_
pilot.py`, `_pass_2.py`, `_pass_3.py` and `_pass_13.py` (which pass 14 and 15 share).

The other four want a `--build` and a look at what moved: `tools/build_sidecars*`, and the
two ladder re-derivations under `tools/`.

**Acceptance:** `./tools/check.sh` exits 0 on `origin/dev`, and the cohort gate still fails
when a manifest claims somebody another pass has already ruled on.
