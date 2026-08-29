---
id: T-0385
title: The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: T-0306
opened: 2026-08-29
closed: null
pr: null
claimed_by: run 8/29/2026, 2:27:59 PM CT
blocked_on: null
needs_bake: true
---

The New York Clothing Store stands three doors north of the Tremont House in Dearborn Street.

Piece 3 of 5 of **T-0306 — The American names six Chicago storefronts with usable placements and none of them is standing in the model yet**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**What it needs first.** The anchor is *"three doors north of the Tremont House, in
Dearborn Street"*, and `tools/compile_register.py`'s `match_landmark` cannot see the
Tremont: it compares whole word-sets, and every one of `tremont_house_1`'s three names
carries a disambiguator this project added — *(the first)*, *I*, *old* — so
`{tremont, house}` matches none of them. Four businesses fail on that one anchor. The
register calls this one `street_only` on `dearborn` today.
