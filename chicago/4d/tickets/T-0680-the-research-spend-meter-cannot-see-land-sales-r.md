---
id: T-0680
title: The research spend meter cannot see land_sales' refusals: 354 adjudicated names read as unspent because a refusal is keyed on the purchaser's name and carries no record_id
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The research spend meter cannot see land_sales' refusals: 354 adjudicated names read as unspent because a refusal is keyed on the purchaser's name and carries no record_id.

`tools/measure_research_spend.py` counts a crosswalk entry as SPENT when it is anchored
to something real — a `record_id`, `entry_id`, `claim_id`, `person_id`, `resident` — and
its own docstring says a refusal counts as spend, because ruling that a name is NOT a
town person IS the adjudication. `land_sales/resident_crosswalk.json` rules on EVERY
purchaser it reads: 27 matches carry a `resident_id` and are counted, and 354 refusals
carry `{a, b, rule, evidence}` keyed on the purchaser's name as read and are counted as
nothing. So the meter reports the domain as 736 unspent when the truth is closer to
fully adjudicated, and T-0677 had to raise the read ceiling to 736 to merge a finished
sweep.

This is a MEASUREMENT bug and the fix must not become a way of buying spend cheaply.
The honest change is to give each refusal the `record_ids` it refuses — every sale of
that purchaser name — so the anchor is a read record and the meter can dedupe it the way
it dedupes everything else. Then re-baseline and see what the number actually is. If the
domain really is adjudicated end to end, the ceiling should come back down to near zero
and the raise T-0677 took should be undone in the same PR.

Check the other domains for the same shape before changing the tool: a refusal keyed on a
name rather than a record is the natural thing to write, so land_sales is unlikely to be
the only one.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)
