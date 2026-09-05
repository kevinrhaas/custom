---
id: T-0753
title: The 1840 census images 51-74: the group declared image by image, and printed 233 and 235 - PR #670's last two calibration pages - read to the name
state: done
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0496
opened: 2026-09-05
closed: 2026-09-05
pr: 860
claimed_by: run 9/5/2026, 1:50:12 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-05T07:24:42.040Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33950196510
---

The 1840 census images 51-74: the group declared image by image, and printed 233 and 235 - PR #670's last two calibration pages - read to the name.

Piece 1 of 11 of **T-0496 — The 1840 census deposit is 75 page images and 210 heads on seven printed pages are the only names read from it: images 51-75**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- All 24 images of the group are declared in `coverage.json` with what each leaf is, its sheet
  side and its printed page number where the heading band carries one; a hole fails rather
  than passes quietly.
- Printed 233 and 235 are read to the NAME, line by line, with `[?]` as a POSITION and a
  stated `name_confidence`; blank lines are looked at rather than assumed.
- `crosswalk_670.json` gains both pages: the agreement count against #670's rows and the
  row-offset test that tells a drifted row from a bad reading.
- A line count is stated where the leaf was read, and where it is NOT stated the reason is
  measured rather than asserted.

**Done by this ticket** — see the PR. The other ten pieces carry the reading of the
remaining 22 leaves; `T-0754` is the one to do first.
