---
id: T-1033
title: Read the town-lot deposit into records: append the ids, declare its firms, and make tract() resolve or refuse a lot-and-block-in-a-named-town without inventing a section
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
claimed_by: run 9/11/2026, 6:54:57 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34596064091
---

Read the town-lot deposit into records: append the ids, declare its firms, and make tract() resolve or refuse a lot-and-block-in-a-named-town without inventing a section.

Piece 2 of 2 of **T-1028 — The 619 town-lot sales the by-section sweep cannot see: Cook County's register describes a lot and block with no section, so 466 sales of 1836 — the town's own ground — are outside the land_sales deposit**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- `isa_land_tract_sales_cook_town_lots_through_1836.tsv` joins `DEPOSITS`, its record
  ids APPENDED so nothing already cited by `data/structures/*.json` renumbers.
- `tract()` either resolves a lot-and-block-in-a-named-town or REFUSES it with a stated
  reason; it never guesses which plat a town code names and never invents a section.
- Every firm the reading finds is declared in `KNOWN_FIRMS` after its rows are read.
- `coverage.json § completeness_probe` re-derives to
  `complete_for_1836_cook_county: true`, or says precisely what is still outside it.
- No resident is minted or regraded. A purchase is a transaction.

**What T-1032 already measured for it** — the four tract forms, the three refusals, the
57 blocks, the `CHIOTVO`/`VO` trap and the 255 purchaser spellings — is in that ticket
and in `data/research/land_sales/README.md` § *The 619 read*.
