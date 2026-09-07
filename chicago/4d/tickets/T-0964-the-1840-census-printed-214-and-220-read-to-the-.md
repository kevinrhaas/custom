---
id: T-0964
title: The 1840 census printed 214 and 220 read to the name and the cell: 33SQ-GYYJ-BP and 33SQ-GYYJ-P5
state: claimed
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0746
opened: 2026-09-07
closed: null
pr: null
claimed_by: run 9/7/2026, 9:50:06 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34133061399
---

The 1840 census printed 214 and 220 read to the name and the cell: 33SQ-GYYJ-BP and 33SQ-GYYJ-P5.

Piece 2 of 5 of **T-0746 — The 1840 census images 51-74: the names and cells of the sheets the inventory finds, read line by line**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

Printed **214** (`33SQ-GYYJ-BP`) and printed **220** (`33SQ-GYYJ-P5`) each carry a page file
under `data/research/census_1840/pages/` holding, for every ruled line with an entry, the head's
name as read off the deposited image AND all thirty-eight free-white and free-coloured age-band
cells of the left sheet. Each page states, per column, what its marks come to and what the
enumerator's own printed footing at the foot of the leaf says, with every residual named rather
than smoothed and any footing glyph that cannot be settled recorded as `null` rather than
presented as closed. `coverage.json` moves both images off `inventoried_only` and states what was
read and what was not. Nothing here mints an 1835 resident.
