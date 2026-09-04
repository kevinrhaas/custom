---
id: T-0677
title: The five ring townships around Chicago are unread in the Illinois land tract sales: sweep T39N R13E, T38N R14E, T38N R15E, T40N R13E and T41N R14E through 1836
state: done
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0610
opened: 2026-09-04
closed: 2026-09-04
pr: 799
claimed_by: run 9/4/2026, 11:59:25 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-04T18:23:01.549Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33897556394
---

The five ring townships around Chicago are unread in the Illinois land tract sales: sweep T39N R13E, T38N R14E, T38N R15E, T40N R13E and T41N R14E through 1836.

Piece 1 of 2 of **T-0610 — Three sections of T39N R14E were truncated at the land-sales database's 150-row ceiling, and the ring townships are unread: finish the Illinois land tract sales around Chicago**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance.** All five townships `coverage.json` names under `not_read.townships_not_read`
— T39N R13E, T38N R14E, T38N R15E, T40N R13E, T41N R14E — are swept section by section
(36 queries each, third principal meridian), the sales dated on or before 31 December
1836 are committed as deposits under `data/research/land_sales/text/`, every generated
file is re-derived from them by `tools/read_land_sales.py --build`, and `coverage.json`
declares each section that came back under the 150-row ceiling and holds a sale — or
lists it as queried-and-empty, which is read and not a hole. `townships_not_read` is
empty when this closes. Any section that returns exactly 150 rows is reported as
truncated and NOT declared, on the same rule T-0557 set. The existing `ls####` record
ids do not move: they are cited by `ground.json` and by the structures' `land_owner`
blocks, so deposits are read in an append-only order.
