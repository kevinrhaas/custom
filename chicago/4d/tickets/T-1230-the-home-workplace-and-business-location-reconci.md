---
id: T-1230
title: The home, workplace and business-location reconciliation table: one row per claim, with its source, date, ids, printed place, resolved street, face and anchor, and the clause that limited it
state: done
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1147
opened: 2026-09-17
closed: 2026-09-17
pr: 1389
claimed_by: run 9/17/2026, 5:14:04 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-17T11:21:29.412Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35208720422
---

The home, workplace and business-location reconciliation table: one row per claim, with its source, date, ids, printed place, resolved street, face and anchor, and the clause that limited it.

Piece 1 of 3 of **T-1147 — Spend every defensible home, workplace and business-location finding, preserve the 123 location limits, and close research with zero unclassified attested or inferred fact**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. One generated table — `data/research/location_reconciliation.json`, DERIVED and never
   authored — holds one row for every home, workplace and business-location claim the
   project already holds: the gazetteer's 316 business placement readings, the households'
   20 `lives_at` and 50 `works_at` statements, and the 218 later-directory addresses the
   two back-projection ledgers adjudicate.
2. Every row carries `subject_kind`, the household / person / business ids, `relation`,
   `source_id`, `claim_or_record_id`, `describes_date` with its precision, `printed_place`,
   `resolved_street`, `resolved_street_id`, `resolved_face`, `resolved_anchor`,
   `resolved_structure`, `confidence`, `disposition` and `limit_clause` — T-1147 ¶1 and ¶8,
   so that T-1198's address book can add a rung without re-adjudicating the evidence.
3. Every `disposition` comes from a declared vocabulary, and every row states the clause
   that stopped it going narrower. No row is silent, and a row whose confidence is null
   names the ledger that is silent about it rather than inventing a grade.
4. **The table re-argues nothing.** Every disposition is CARRIED from the committed ledger
   that made it — the scene-date register's action, the street-face adoptions and their
   refusals, the two back-projection ledgers' clauses — and each row names that ledger.
   A claim standing under one of the four owner-retained source questions carries
   `standing_question` beside its disposition rather than having the question answered here.
5. `--report` prints T-1147 ¶9's location axis: the three business location limits
   (structure / street-only / unplaceable) and the four household seating classes
   (structure / lot / face / division / none), so T-1157 can read one number per class.
6. `--check` re-derives and refuses a hand edit; `--self-test` proves the refusals fire;
   both are wired into `tools/check.sh`.

**Stop condition:** the table exists, re-derives from committed ledgers alone, and is the
single input T-1231 (writing the relationships) and T-1198 (the address book) read.

**Out of scope, and owned by the siblings:** writing plural dated `lives_at` / `works_at`
and `associated_with[]` onto the records (T-1231); the people and business views, the four
standing questions and the ledger closeout (T-1232).
