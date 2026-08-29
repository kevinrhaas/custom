---
id: T-0400
title: The firm styles that differ in the forename's form: whole against abbreviated against initial
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

Piece 2 of 4 of **T-0338 — Thirty-one groups of firms share a partner surname and only one
of them has been judged**. The parent keeps the full ask; this ticket owns one slice of it.

The groups where the two styles carry the SAME partner surnames and differ in the form of a
forename — whole against abbreviated against bare initial. T-0304 already ruled that a
forename initial is not decisive for a firm the way it is for a person, so these are
judgeable; what they need is the printing that ties the two forms to one house.

The candidates, after T-0399 collapses the restyles:

    Collins & Caton against J. H. Collins & J. D. Caton
    Matthias Mason & Co. against Mathias Mason & Co. (one t) and bare Matthias Mason
    G. Spring against Giles Spring · J. S. C. Hogan against John S. C. Hogan
    J. Bates, Jr. against John Bates, Jr. · J. Wellmaker & Co. against John Wellmaker & Co.
    J. Wright, merchant against John Wright · D. Elston & Co. against Daniel Elston & [Co.]
    J. D. Caton, attorney… against John Dean Caton · Doty & Co. against H. Doty & Co.
    P. Pruyne against P. Pruyne & Co.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Every group above is declared in `firm_merges` with a rule citing the printings, or
  written into `refused_firm_merges` with the reason it is two houses.
- No group is merged on the forename alone: the rule cites an issue, a copy date, a street
  or an anchor that ties the two forms together.
- The gazetteer recompiles green and the PR states the business count before and after.

Links: T-0338 (the parent), T-0399 (which ran first), T-0304.
