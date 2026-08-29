---
id: T-0370
title: The register counts seven documented households as invented, because it reads any reconstructed person in them
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The register counts seven documented households as invented, because it reads any reconstructed person in them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0264.** `tools/compile_register.py` builds its invented-household census
by walking every person in `data/residents/` and counting the household of anybody
graded `reconstructed` or `inferred` who carries an occupation:

```python
for r in town["residents"]:
    if r["grade"] in ("reconstructed", "inferred") and r["occupation"]:
        town["invented"].setdefault(r["occupation"], set()).add(r["household"])
```

A DOCUMENTED household with one reconstructed member in it is therefore counted as an
invented household of that member's trade. Seven are: `hh_mason_matthias`,
`hh_temple_john_t`, `hh_couch_ira`, `hh_church_thomas`, `hh_haddock_edward`,
`hh_murphy_john`, `hh_walters_william` — Matthias Mason, John T. Temple, Ira Couch,
Thomas Church, Edward Haddock, John Murphy and William Walters, all of them real men
this project already names from cited sources.

**What it costs.** The register reported `retirable_total: 28` where the town holds 24
invented households in matched trades, and three of its per-trade rows were wholly
spurious — dentist 1, hotel_keeper 1, merchant 1 named no invented household at all,
and tavern_keeper claimed 4 where 1 stands. A run reading that table at face value
would have proposed retiring John T. Temple's household in favour of a documented
dentist, which is to say replacing a documented man with another documented man.

`tools/retire_invented_residents.py` does not use this census — it takes the invented
set from the authored occupation census in
`data/reconstruction/1835_inferred_household_programme.json` instead, and the
household files agree with it exactly (101 of 101, `name_basis` on the head being the
exact marker). So nothing is standing wrong in the town today. What is wrong is the
register's own COUNTS block, which is what a reader consults.

**Acceptance:** the invented-household census counts a household as invented on a test
about the HOUSEHOLD rather than about any one member — the programme's own list, or a
head whose name is invented — the seven documented households above leave the tally,
`counts.invented_residents` is restated with the correct per-trade rows, and
`compile_register.py --self-test` grows a case that fires when a documented household
with a reconstructed member is counted again.
