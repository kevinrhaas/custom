---
id: T-0682
title: T39N R13E section 16 filled the 150-row first page and the ring sweep stopped there: walk it to the end with the More cursor
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

T39N R13E section 16 filled the 150-row first page and the ring sweep stopped there: walk it to the end with the More cursor.

T-0676 swept the five ring townships before T-0675 established that the results page's
More button is a keyset cursor, so it stopped at the first page of every section. Only
one ring section reached the 150-row ceiling: **T39N R13E section 16**, the school
section of the township immediately west of the town, whose first page is all this
project holds for it. `coverage.json` names it under
`not_read.truncated_at_the_150_row_ceiling` and does NOT declare it.

This is a sweep to re-run, not a source to go looking for. The machinery already exists:
`tools/harvest_land_sales.py --sweep --township 39 --range 13` now walks every section to
its end, and `held_rows` carries the 145 sales already in the deposit forward so only the
new detail pages are fetched. Budget it against the reader's pacing — about twenty
requests a minute — the way T-0675 did: section 16 of T39N R14E went from 150 rows to
337, so expect a few hundred detail pages and size the run for that.

**Acceptance:** T39N R13E section 16 is walked to the end, its sales through 31 December
1836 are in `text/isa_land_tract_sales_t39n_r13e_through_1836.tsv`, `TRUNCATED` in
`tools/read_land_sales.py` is empty, and `coverage.json` declares the section instead of
naming it as short.
