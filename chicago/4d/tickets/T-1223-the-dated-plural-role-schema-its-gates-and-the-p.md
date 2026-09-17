---
id: T-1223
title: The dated plural role schema, its gates and the person card's role timeline, with Daniel Elston's four dated roles as the fixture
state: claimed
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1145
opened: 2026-09-17
closed: null
pr: null
claimed_by: run 9/17/2026, 3:59:21 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35202200830
---

The dated plural role schema, its gates and the person card's role timeline, with Daniel Elston's four dated roles as the fixture.

Piece 1 of 4 of **T-1145 — Replace the one-occupation resident field with dated plural roles and migrate every matched trade, profession and civic office without back-projecting later evidence**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

Carries acceptance clauses 1, 2, 5 (the card half), 7 and 8 of the parent, and the half of
clause 6 that is the schema and the validator. Clause 3 (the bulk migration) and its table are
T-1224; clause 4 (T-0991's six 1833 trades) and the audit/census half of clause 6 are T-1225;
the People-view search half of clause 5 is T-1226.

1. A person carries `roles[]`. Each assertion states a controlled `role` from the manifest
   vocabulary, the source's own wording in `as_read`, a `kind` of `trade`, `profession`,
   `office`, `employment` or `business_interest`, a date — `from`/`to`, or `on` for a point —
   with its own `precision`, a `confidence`, a `source` that resolves in `data/sources/`, and
   the `claim_id` or `entry_id` of the row it was read from. An unknown date stays unknown and
   is never widened to the scene date.
2. A role states `place` — a structure id, or `not_stated` — and, for `office` and `employment`,
   `employer_or_body`, so a later band can attach a role to the establishment it served.
3. The singular `occupation` block becomes a GENERATED compatibility view of the roles that
   actually cover 1835-07-01. Two simultaneous roles remain two roles; the singular field can no
   longer be the only place a trade is written.
4. Gates, in `tools/validate.py` and run by `tools/check.sh`: a role that loses its source or its
   claim/entry id fails; a role whose dates do not cover the scene date may not be the singular
   compatibility value; a role outside the manifest vocabulary fails; an `office` or `employment`
   with no `employer_or_body` fails.
5. Daniel Elston is the fixture and his card SHOWS it: candle and soap manufacturer from 1833 at
   the North Side manufactory, provision dealer and pork curer, brickmaker from 1839, and school
   inspector in the 1839 civic register — each with its date, its source and its place, and the
   card marks which reach 1 July 1835.
6. The person card renders `roles[]` as a dated timeline for every person that has one, and the
   compiled `people.json` row carries the roles so the timeline needs no second fetch.

**Stop condition:** the schema, its gates and the card exist and are demonstrated on the fixture;
the remaining 1,126 structured role rows are T-1224's to migrate into them.
