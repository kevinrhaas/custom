---
id: T-0394
title: The firm groups an agency, a parent house or a lost signature makes ambiguous
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0338
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Piece 4 of 4 of **T-0338 — Thirty-one groups of firms share a partner surname and only one
of them has been judged**. The parent keeps the full ask; this ticket owns one slice of it.

What is left after T-0391, T-0392 and T-0393: the groups where the honest answer is not
"one house" or "two houses" but something the merge machinery cannot say at all.

    Hubbard & Co. against the Howard Fire Insurance Company, E. K. Hubbard agent
      — an AGENCY is not the house that holds it, and the gazetteer has no relation
        that says so
    the Chicago Democrat against the Chicago Democrat printing office
      — T-0391 merged each of these into itself and left them two, because the partner
        surnames are {democrat} against {office}: the guard cannot see that an office is
        its paper's. Same shape as T-0340's headline-only firm, and it should be decided
        with it rather than against it
    E. Wentworth's public house on Flag Creek against E. Wentworth's tavern on Flag Creek
      — one house under two trade WORDS, which `firm_style()` cannot cut because neither
        follows a comma
    Jones & King against Jones, King & Co.
    Abell against S. Abell, attorney and counsellor — a bare surname against a styled one

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Each group is either merged with a declared rule, refused with a written reason, or —
  where the answer needs machinery the gazetteer does not have (an agency relation, a
  paper-and-its-office relation) — a ticket is filed for that machinery and this one
  records the decision to file it.
- Nothing is merged that changes the partner surnames, unless T-0340 has already changed
  that guard and this cites the change.
- The gazetteer recompiles green and the PR states the business count before and after.

Links: T-0338 (the parent), T-0340 (the same guard question), T-0304.
