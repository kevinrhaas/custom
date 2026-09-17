---
id: T-1255
title: The people view shows every role as a dated timeline, marks which reach the scene date, and searches controlled and printed wording
state: open
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1145
opened: 2026-09-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The people view shows every role as a dated timeline, marks which reach the scene date, and searches controlled and printed wording.

Piece 3 of 3 of **T-1145 — Replace the one-occupation resident field with dated plural roles and migrate every matched trade, profession and civic office without back-projecting later evidence**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)


## T-1283 IS FOLDED IN HERE (owner's tightening, 2026-09-17)

T-1283 asked for the dated roles to be wired onto the person card, and named the ready
renderer on the closed duplicate branch `steward/t-1145-plural-roles` — 99 lines in
`residents.js` and a 164-line `tools/roles.py`:

    git fetch origin steward/t-1145-plural-roles
    git show 27c30072b -- chicago/4d/renderers/web/js/residents.js

That is the same feature as this ticket's timeline, not a separate one, and two tickets for
one view is exactly the split the owner asked to stop. **Read that branch against `dev`'s
schema before using a line of it** — the two runs wrote the role shape independently, so the
field names may not agree and `roles.py` may need rewriting. The card layout is the part that
carries over.

**Good, not great:** a dated list on the card that shows which roles reach 1 July 1835 and
which do not, each with its dates and source. Search and filter are worth having and are NOT
a reason to hold the card; ship the card, and say in the PR if filtering did not fit.
