---
id: T-0391
title: The restyled firm duplicates: one style is the other plus a trade tail or a leading article
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0338
opened: 2026-08-29
closed: null
pr: null
claimed_by: run 8/29/2026, 9:45:16 AM CT
blocked_on: null
needs_bake: false
---

Piece 1 of 4 of **T-0338 — Thirty-one groups of firms share a partner surname and only one
of them has been judged**, split because the parent needed more than one run's
demonstration. The parent keeps the full ask; this ticket owns one slice of it.

**The slice, defined mechanically so it is complete and checkable.** Take the firm styles
that are IDENTICAL once a trailing trade description and a leading article are cut away —
`slug(firm_style(name))` with a leading `the` and a possessive `'s` normalised. That is 23
clusters holding 48 of the gazetteer's 242 businesses. `Russell & Clift` is one of them and
is NOT taken: T-0340 owns it and may change the partner-surname guard itself. So 22
clusters, 46 entries.

These are the cheapest honest judgements in the parent, because the difference between the
two styles is the compositor's, not the firm's: `firm_style()` already knows that a comma
followed by a lower-case word begins a trade and not a partner. But cheap is not automatic
— three of the 22 are traps the parent names, and a sweep that merged on the style alone
would have merged them.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- All 22 clusters are judged. Every one is either declared in `firm_merges` with a rule
  that cites the printings it rests on — issues, copy dates, streets, anchors — or written
  down in `refused_firm_merges` with the reason it is two.
- No cluster is merged on the name alone.
- The gazetteer recompiles green and `check.sh` is no worse than the dev it was cut from.
- The PR states the business count before and after.
- Clusters outside this slice stay on the queue as T-0392 / T-0393 / T-0394.

Links: T-0338 (the parent), T-0304 (the firm-merge machinery), T-0340 (Russell & Clift).
