---
id: T-0916
title: The 1840 census images 51-74: printed 212 (33SQ-GYYJ-RY) and 213 (33SQ-GYYJ-RK) read line by line to the name
state: done
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0746
opened: 2026-09-06
closed: 2026-09-06
pr: 1009
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: 2026-09-06T23:33:49.495Z
claimed_run: null
---

The 1840 census images 51-74: printed 212 (33SQ-GYYJ-RY) and 213 (33SQ-GYYJ-RK) read line by line to the name.

Piece 1 of 4 of **T-0746 — The 1840 census images 51-74: the names and cells of the sheets the inventory finds, read line by line**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- Both leaves get a page file under `data/research/census_1840/pages/`, in the shape the
  group's two prior name readings use (33SQ-GYYJ-RJ, 33SQ-GYYJ-ZQ): every ruled line with an
  entry carries `as_read`, `normalized`, `name_confidence` and `reading: scan_verified`, in
  enumeration order, and a line that cannot be carried is recorded rather than skipped.
- Each sheet's `lines_ruled_with_an_entry` is TESTED against the inventory by reading to the
  last written line and saying where the table closes — the group-1 and group-2 inventories
  read long by one to four lines, and that finding is either repeated here or refuted.
- Neither leaf is in PR #670's calibration set (printed 229-235), so the cross-check clause
  of the parent has nothing to bite on here; the PR says so rather than passing silently.
- The cells are NOT read by this piece and every page file says so; nothing may be taken as
  a zero. T-0919 owns them.
- `coverage.json` group 3 has its counts RECOMPUTED from the images array, not incremented.
