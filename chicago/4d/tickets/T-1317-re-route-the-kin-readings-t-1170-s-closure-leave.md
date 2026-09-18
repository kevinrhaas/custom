---
id: T-1317
title: Re-route the kin readings T-1170's closure leaves waiting: the four spend rulings that hand a named-kin enrichment to the family pass, re-pointed at the work that will actually read them
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Re-route the kin readings T-1170's closure leaves waiting: the four spend rulings that hand a named-kin enrichment to the family pass, re-pointed at the work that will actually read them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)


- Every unit the four rules below hand on carries a disposition that is true of it TODAY,
  not a pointer at an epic that has finished. Four rules, three of them authored in
  `tools/spend_remainder_rulings.py` and one hand-authored in
  `data/research/spend_rulings.json`:
  `the_enrichment_names_kin_no_field_carries`, `the_family_column_names_kin`,
  `the_register_entry_names_kin`, `handed_to_the_family_pass`.
- The seven units the ledger names today — `beaubien_josette`, `owen_thomas_jv`,
  `porter_eliza_chappel`, `porter_jeremiah`, `robinson_catherine`, `heacock_russel_e`,
  `hobson_jesse` — are each adjudicated ON THEIR OWN, and most of them already have an
  answer waiting in `data/residents/stated_family_rulings.json`: Josette LaFramboise
  Beaubien and Catherine Chevalier Robinson are `already_held`, Jesse Hobson's wife is
  `no_seat`. An `already_held` unit is not unresolved and should stop saying it is.
- `tools/measure_research_spend.py --ledger-build` green, `tools/check.sh` green, and the
  ledger report prints no unit waiting on a closed ticket.

**Why it exists.** T-1313 closed the last of T-1170's three children and the gate went red
the moment it did: `research_spend_ledger.py` holds `unresolved` to `OPEN_TICKET_STATES`, so
a fully-closed `split` parent is not somewhere a reading may wait. That is the gate working
exactly as designed — `data/research/spend_rulings.json` says in its own doc that "a ticket
closing turns this file red, which is the point." T-1313 re-pointed the four rules at this
ticket, with the reasoning written into each statement, and did NOT re-adjudicate the seven
units, because that is seven judgements about what the sources say and belongs in a run that
can show its reading.

**What it must NOT do:** close a unit by deleting its row, or re-point these rules at a
third ticket to keep the gate quiet. The next pointer must be work that is going to happen.
