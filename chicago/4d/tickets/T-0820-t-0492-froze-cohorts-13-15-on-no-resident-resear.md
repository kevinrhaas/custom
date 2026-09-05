---
id: T-0820
title: T-0492 froze cohorts 13-15 on 'no resident_research block', but all 76 of cohort 13 already carried a package row — cohorts 14 and 15 are framed the same way
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

T-0492 froze cohorts 13-15 on 'no resident_research block', but all 76 of cohort 13 already carried a package row — cohorts 14 and 15 are framed the same way.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Measured by T-0508 (cohort 13), 2026-09-05, before the pass was written.**

T-0492's freeze selected "every named person carrying no `resident_research` block" by reading
`data/residents/households/*.json`. But a research row does not live only there:
`synthesize_resident_research.py`'s `research_rows()` ALSO reads every durable package under
`chicago/reference/resident-research/T-*/`. Measured against cohort 13:

    cohort members carrying a row in an EARLIER package:  76 of 76
    earlier packages involved:  T-0463 (43) · T-0493 (27) · T-0462 (23) · T-0442 (9)
    outcomes RAISED by re-reviewing all 76:               10

So the headline "237 named residents have no research row" is measuring the DERIVED layer
being unwritten (see T-0812), not the research being undone. That is not nothing — the ten
raised outcomes include `beckford_printer`, who went from a documented negative to a trade and
an employer — but it is a different, smaller claim than the ticket titles make, and cohorts 14
(T-0509) and 15 (T-0510) are framed on exactly the same test.

## The ask

1. Re-measure the 237 against BOTH sources of a research row — the household block and the
   package CSVs — and say how many are genuinely unreviewed.
2. Re-title or re-scope T-0509 and T-0510 to what the re-measurement finds. If most of their
   members already carry rows, the useful unit is "re-review the ones whose outcome is a
   documented negative and whose name is distinctive", not "review 76 people who have nothing".
3. Keep the re-review value visible either way: T-0508 raised 10 of 76 outcomes on a corpus
   sweep plus ONE external fetch, so re-review pays — it just does not pay what the title says.

**Done when** the 237 figure is re-derived against both sources and T-0509/T-0510 carry the
scope the new number supports.
