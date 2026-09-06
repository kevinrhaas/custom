---
id: T-0854
title: The pilot and passes 2-5 run their stratum-membership refusals on the gate path, so a member whose letter-list flag moves fails the build instead of being reported
state: open
epic: META
requested_by: loop
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

The pilot and passes 2-5 run their stratum-membership refusals on the gate path, so a member whose letter-list flag moves fails the build instead of being reported.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0764**, which fixed the snapshot half of exactly this and left this half
standing rather than widen its diff.

T-0764 settled what a frozen cohort manifest is: a reservation and an identity lock, whose
per-person `starting_*` / `sources` / `letter_list_returns` / `stratum` cells are a
SNAPSHOT of the tree at the freeze. `tools/resident_cohort_freeze.py` now gates all eight
manifests on the reservation and REPORTS snapshot movement instead of calling it stale,
and the write path carries the freeze forward instead of overwriting it.

**What it did not reach.** Inside `derive()`, the five older selectors — the pilot and
passes 2, 3, 4 and 5 — assert each member's CURRENT tree state against the stratum it was
frozen in, and those assertions run on the `--gate` path as well as the write path:

    tools/select_resident_research_pilot.py:128   {hid}: no longer marked letter_list_only
    tools/select_resident_research_pass_2.py:72   {person_id}: no longer marked letter_list_only
    tools/select_resident_research_pass_2.py:74   {person_id}: established stratum became letter-list-only
    tools/select_resident_research_pass_4.py:61   {person_id}: established resident became letter-list-only
    tools/select_resident_research_pass_4.py:69   {person_id}: {stratum} presence changed
    tools/select_resident_research_pass_5.py:105  remaining established person became letter-list-only
    tools/select_resident_research_pass_5.py:110  pass-five present stratum changed

— plus each file's `strata != expected` quota check, which is the same assertion in
aggregate, and each file's novelty/overlap refusal (`T-0463 overlaps prior reviews`).

A member moving from `letter_list_only` to an established profile is research landing on
that person: it is precisely what the cohorts exist to cause, and the manifests' own text
says so — "a person who acquires a research row after this does NOT make the manifest
stale; a person who VANISHES, or turns into a placeholder, does". Today it is a red build,
whose documented remedy is to regenerate, which no longer changes anything, so the build
stays red until somebody edits a selector.

**Cohorts 13-15 already have the answer**, in `select_resident_research_pass_13.py`: a
`minting` flag, passed `not args.gate and not path.exists()`, that scopes the selection-time
refusals to the write that first fixes the cohort. Its docstring gives the reasoning at
length and it is the implementation to copy, not to reinvent.

**Acceptance:**

1. The five older selectors take the same `minting` scoping as pass 13: the novelty
   refusal, the strata quotas and the per-person stratum-membership assertions run when a
   cohort is SELECTED and not when it is gated. Nothing is deleted and nothing is
   softened on the write path.
2. What DOES still fail on the gate is unchanged and is `resident_cohort_freeze`'s four
   assertions — ids and their order, a person who left the layer or became a placeholder,
   a row field dropped or invented, a non-snapshot document key differing.
3. A self-test case per selector proving a moved stratum flag no longer reddens the gate
   and still refuses a mint, and `bash tools/check.sh` green.

**Links:** T-0764 (the snapshot half) · T-0492 (the `minting` scoping on cohorts 13-15)
