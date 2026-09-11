---
id: T-1030
title: The 619 sectionless Cook County sales are read at their detail pages and committed as their own deposit
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-1028
opened: 2026-09-11
closed: null
pr: null
claimed_by: run 9/11/2026, 5:38:19 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34589842708
---

The 619 sectionless Cook County sales are read at their detail pages and committed as their own deposit.

Piece 1 of 2 of **T-1028 — The 619 town-lot sales the by-section sweep cannot see: Cook County's register describes a lot and block with no section, so 466 sales of 1836 — the town's own ground — are outside the land_sales deposit**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- All 619 rows the committed Cook County list gives no section are read at the register's
  own DETAIL pages — by purchase number, which is the one handle such a row has — and
  committed as their own deposit carrying the sweep's seventeen columns.
- The reading is checked against the list it came from and any disagreement is REPORTED,
  never smoothed. A detail page that prints a section the list left empty is named.
- Nothing already committed renumbers. The deposit is NOT added to `DEPOSITS` here:
  record ids are positional and `data/structures/*.json` cite them, so the join is
  T-1031. `coverage.json § completeness_probe` says the file exists, how many of the
  listed rows it holds, and that it is not joined; `complete_for_1836_cook_county` stays
  false until it is.
- No resident is minted, moved or regraded. A purchase is a transaction.
- `bash tools/check.sh` green, with self-tests that fire when the new reporting is
  broken. No bake.
