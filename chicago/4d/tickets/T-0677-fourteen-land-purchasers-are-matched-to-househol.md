---
id: T-0677
title: Fourteen land purchasers are matched to households and not one is on the card: spend the land-sales resident crosswalk, tract, date and price
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

Fourteen land purchasers are matched to households and not one is on the card: spend the land-sales resident crosswalk, tract, date and price.

`data/research/land_sales/resident_crosswalk.json` matches fourteen purchasers in the
Illinois public-domain tract-sales deposit to people this town holds a card for — Hiram
Pearsons, Daniel Elston, Thomas Hartzell, Bronson, Hale, Ludby, Price, Wolcott and six
more — each row naming a `household_id` and a `resident_id`. Not one of the fourteen is on
the card it names. T-0635 (consolidation pass 2) made them visible for the first time: it
stated the file's source at the top so the rulings became judgeable, and taught the second
hop of `tools/measure_research_spend.py` to read a row filed under `matches` as a match.
The finding is recorded as that domain's write-hop ceiling of 14 in
`tools/research_spend_baseline.json`, and this ticket is how the ceiling comes back down.

WHY IT IS WORTH A RUN. A purchase is POSITION. Each row joins to an entry in
`data/research/land_sales/entries.json` carrying a record id, an aliquot part, a section,
township and range, a date of sale, an acreage and a price — and this town has 20
households with any address at all. It is the cheapest position in the project.

WHAT IT MUST NOT DO. The crosswalk's own carry rule is that a purchase "dates and places a
transaction; it proposes no residence, and under the ratified ladder it corroborates rather
than mints". So no grade moves, no `lives_at` is written off a tract, and a purchase in a
ring township is not a house. `tools/spend_civic_voter_lists.py` and
`tools/spend_fergus_1839_later_lists.py` are the two worked precedents: two fields on the
card, a ledger whose name carries no "crosswalk", and a `--check` in `tools/check.sh`.

BEWARE THE MATCHER. T-0670 carries the surname-uniqueness weakness that made nine of these
matches ambiguous when T-0514 seated 531 new residents; the fourteen are what survived it.

**Acceptance:**

1. Every one of the fourteen rulings is on the card it names, citing
   `isa_public_domain_land_tract_sales` and naming the entry record id it rests on.
2. `tools/measure_research_spend.py --gate` reads land_sales' write hop at 0, and the
   ceiling in `tools/research_spend_baseline.json` is LOWERED rather than raised.
3. No grade moves and no placement is written. The tool's `--self-test` holds it.
