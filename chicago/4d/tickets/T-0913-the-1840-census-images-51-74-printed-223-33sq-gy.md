---
id: T-0913
title: The 1840 census images 51-74: printed 223 (33SQ-GYYJ-LV) and 240 (33SQ-GYYJ-CK) read line by line to the name
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0746
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The 1840 census images 51-74: printed 223 (33SQ-GYYJ-LV) and 240 (33SQ-GYYJ-CK) read line by line to the name.

Piece 3 of 4 of **T-0746 — The 1840 census images 51-74: the names and cells of the sheets the inventory finds, read line by line**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- Same shape as T-0911, which is the demonstration this piece repeats: a page file per leaf,
  every ruled line with an entry recorded in enumeration order with `as_read`, `normalized`,
  `name_confidence` and `reading: scan_verified`, and the inventory's line count tested by
  reading to the last written line rather than assumed.
- The cells stay unread and each page file says so; T-0914 owns them.
- `coverage.json` group 3 has its counts RECOMPUTED from the images array, not incremented.
