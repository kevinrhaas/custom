---
id: T-0735
title: check.sh is red on dev: nine steps fail before any branch touches them, five because finishing a research cohort is what makes its own gate fire
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: 2026-09-05
pr: 867
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: 2026-09-05T10:17:56.493Z
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

---

**CLOSED 2026-09-05, and the diagnosis was right about the shape and wrong about the
fix.** "Five of the nine are one bug" is exactly correct. But the proposed repair —
`researched_ids()` should ignore a row whose `resident_research.ticket` is the cohort's
own ticket — fixes cohort 15 only. Measured: cohort 15's 76 colliding rows all carry
`ticket: T-0510`, its own; cohorts 13 and 14's 152 carry T-0442, T-0462, T-0463 and
T-0493, written by PR #844 when the pilot, pass 2 and pass 3 sweeps' findings were
finally spent onto the people those passes had reserved in June. Under the narrow fix
both cohorts stay red for ever, on other passes' honest work.

The repair made instead is the one the manifests' own text already asserts and the gate
contradicted: a frozen cohort is gated on what is frozen. `tools/resident_cohort_freeze.py`
gates the reservation — the ids, in order, still naming real, non-placeholder people, with
the field set the selector emits — and not the snapshot of grades, sources and counts
beside it, which records the tree as it stood at the freeze and which the research is
supposed to move. It reports how many snapshot cells have moved rather than failing on
them. **The novelty refusal is unchanged and still fatal on the write path**, which is
this ticket's second acceptance clause: a NEW manifest claiming somebody another pass has
ruled on is refused before it can be committed, and `--self-test` fires that case.

The other four wanted `--build` and a look at what moved: four cards whose `sources` had
been left unsorted by a merge, 450 index rows missing `projected_resident`, and a regrade
that lifts 17 people from inferred to attested on evidence that landed after the last run.
Re-deriving them cascaded into fourteen further passes, all re-run in the same commit.
