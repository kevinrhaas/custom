---
id: T-0523
title: Five real named people sit in retired inf_ records and no research cohort can reach them
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-03
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

**The finding, measured on 2026-09-03 while T-0492 froze cohorts 13-15.** 238 people in
`data/residents/households/` carry no `resident_research` block. Five of them are unnamed
placeholders and are rightly outside every cohort. Five more are REAL, NAMED people:

| person id | name | container |
|---|---|---|
| `inf_cooper_north_04` | J. Garland | `hh_inf_cooper_north_04` |
| `inf_joiner_north_02` | J. W. Reed | `hh_inf_joiner_north_02` |
| `inf_physician_south_01` | Dr. Josiah C. Goodhue | `hh_inf_physician_south_01` |
| `inf_tailor_north_02` | Thomas S. Eels | `hh_inf_tailor_north_02` |
| `inf_tavern_keeper_north_01` | J. Shrigley | `hh_inf_tavern_keeper_north_01` |

They are the register's documented residents, dealt onto reconstructed roofs by
`synthesize_resident_research.py`, then retained UNPLACED by T-0489 when the reconstructed
resident population was retired. Their ids and their household containers still carry the
`inf_` prefix of the programme that seated them, and every cohort selector since the pilot
refuses an `inf_` id outright — `select_resident_research_pass_5.py` raises on it by name,
and T-0492's `select_resident_research_pass_13.py` follows that precedent rather than
quietly widening the rule to reach five people.

So the refusal is correct and the consequence is not: a documented physician the newspapers
name has no research row and no cohort that can ever give him one. The prefix is a fact
about how the record was CREATED, and it is being read as a fact about whether the person
is real.

**The ask.** Decide which of the two it is, once, and make the tree say so. Either

1. the five are re-keyed out of the `inf_` namespace into ordinary person ids and ordinary
   household containers, with the rename recorded and every reference following it — after
   which the existing selectors reach them with no rule change at all; or
2. the selectors gain an explicit, narrow admission — an `inf_` record whose person is
   named and graded `attested`/`inferred` is eligible — declared in one place, with the
   five listed by id so the admission cannot silently widen.

(1) is the honest one if the ids are an artefact; (2) is the honest one if the containers
still mean something. Do not do both, and do not add them to a frozen cohort without
picking one — cohorts 13-15 are frozen at 228 and adding a person to one of them
retroactively is exactly the drift the frozen-manifest pattern exists to prevent.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- All five people are reachable by a research cohort, or the record says in prose why one
  of them is not and that reason is not their id prefix.
- Whichever route is taken is stated in ONE place a later selector reads, not repeated in
  three selectors.
- `python3 tools/select_resident_research_pass_13.py --gate` and `_14`/`_15` stay green:
  the frozen 228 does not move, and any admission lands in a NEW cohort.
- `bash tools/check.sh` green.

**Links:** T-0492 (froze cohorts 13-15 and found this) · T-0489 (retired the reconstructed
resident population and left these five unplaced) · T-0511 (the pilot/pass-2/pass-3
packages) · `tools/select_resident_research_pass_5.py` (the `inf_` refusal, stated first).
