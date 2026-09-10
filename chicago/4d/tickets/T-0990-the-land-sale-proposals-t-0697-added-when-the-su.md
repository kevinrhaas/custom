---
id: T-0990
title: The land-sale proposals T-0697 added when the surname rule widened are unruled: rule them one cohort per run, and the run that closes a cohort files the next
state: open
epic: META
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The land-sale proposals T-0697 added when the surname rule widened are unruled: rule them one cohort per run, and the run that closes a cohort files the next.

**FOUND BY T-0850**, which was written against a crosswalk of 35 matched spellings and
closed against one of 126. T-0700 ruled the ring deposit's nine; T-0850 ruled the first
deposit's twenty-six. In between, **T-0697** changed the mechanical rule — it stopped
requiring exactly one person of the surname and put every reading to every namesake on
`tools/namesake.py` — and **139 spellings met 124 people where 38 had met 35**. Neither
ticket was written against the hundred-odd proposals that arrived that way, and after
T-0850 the crosswalk's own `ruled` block reads **104 unruled**. They reached cards the same
way the ring's nine did: `spend_land_sales.py` writes what `matches[]` declares, and nobody
adjudicated them.

**The rule is written and does not need re-deciding** — `resident_rulings.json`'s
`the_ruling_rule`, applied twice now. A proposal is upheld only where the town's own record
carries something the register's row can be checked against BEYOND a bare name: a middle
initial both records print, a trade the purchase is what you would predict from, a second
document that brackets the entry date, or the register's own Residence column. A bare name
on each side is refused, however unlikely the coincidence looks, and a refusal RETRACTS the
paragraph the spend pass wrote.

**A cohort is a run.** T-0850 took twenty-six spellings and that was a full run: the reading
is per person, and the reasoning is hand-authored because a judgement is not a derivation.
So this is worked one bounded cohort at a time — the spellings T-0697's namesake rule
reached that carry a `rivals[]` list are the natural first one, since those are the
proposals where the layer holds a namesake and the forename alone decided.

**Acceptance,** per cohort: (state it before working — the definition of done, never
weakened to pass)

- the cohort is NAMED in the claim commit, and every spelling in it carries a ruling in
  `data/research/land_sales/resident_rulings.json` — `upheld` or `refused`, each with its
  `checked_against` and its reasoning;
- `python3 tools/read_land_sales.py --build` and `python3 tools/spend_land_sales.py` are
  re-run, and what moved is itemised in `data/research/land_sales/README.md` — matched,
  refused, cards retracted, entries and acres carried;
- `bash tools/check.sh` green;
- **the run that closes a cohort files the next cohort's ticket before it closes**, with
  the remaining count read off the crosswalk's `ruled` block. This closes when that block
  reads zero unruled, and says so with the count — never on "there was nothing left".
