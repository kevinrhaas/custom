---
id: T-0455
title: The run grading criterion is read two ways — the crosswalk's scheduling rank and the building's own size — and the two disagree the first time an H roof stands beside D roofs
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-30
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---
A party-line run is graded along its face by the end rule — the better roof stands nearer
the Dearborn Street drawbridge — and *which roof is better* has been answered two different
ways by two parcels, without either noticing the other.

- **T-0317** (`blk_randolph_market`, second deal) graded by the crosswalk's
  `priority_rank`: D5 at 3, D1 at 4, D2 at 7, best to meanest, "not by taste".
- **`blk_randolph_dearborn`, third deal** graded by SIZE: its H1 "is the largest of the
  three in this run, which is what puts it on the corner under the end rule."

On D-family dwellings the two run together, so nothing separated them. **T-0432 separated
them**: dealt D4 (rank 1), D5 (rank 3) and H3 (rank 18, a two-storey boarding house of
26x38-34x50 ft), the two readings order the run in opposite directions. It applied the
rank, said so, and recorded that the crosswalk's own `priority_rule` defines the rank as
`descending remaining_roofs, then family id` — a SCHEDULING order, how many roofs of that
family the programme still owes, which is not a claim about the building at all.

**Why this is worth a run.** A grading criterion is an invention ordering an invention, and
this project's standard is not that the invention be right but that it be *stated and
re-derivable*. Two criteria in three parcel notes is neither. And the rank reading has a
demonstrable defect the size reading does not: it calls a two-storey boarding house the
meanest building in a run of cottages, because the programme happens to owe few of them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- One criterion is named, in one place a recipe entry can point at rather than restate —
  the crosswalk, `tools/measure_end_rule.py`, or the recipe's `placement_rule` — with the
  reasoning for choosing it and the reading it rejects.
- Every parcel note that grades a run is reconciled to it, or says why its own run keeps
  the order it has. **No roof moves for tidiness**: a re-grade that reorders a committed
  run has to be argued as a repair, and if the answer is "the committed rows stand", that
  is a finding and the entries say so.
- The `blk_south_water_dearborn` second deal is checked against it by name, because it is
  the one run in the town whose two readings are known to disagree.

**Links:** T-0432 (which found it) · T-0317 · T-0105 · T-0028 · T-A11 (the end rule) ·
`data/reconstruction/1835_family_archetype_crosswalk.json` § `priority_rule` ·
`tools/measure_end_rule.py`.
