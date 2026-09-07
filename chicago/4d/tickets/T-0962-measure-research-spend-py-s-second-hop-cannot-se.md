---
id: T-0962
title: measure_research_spend.py's second hop cannot see a resident_crosswalk: census_1840 read 27 head rulings as fully spent while 15 of the 27 cards had never been told
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-07
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

measure_research_spend.py's second hop cannot see a resident_crosswalk: census_1840 read 27 head rulings as fully spent while 15 of the 27 cards had never been told.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**Measured on `dev` at `577c2f6f5`, 2026-09-07, while landing T-0698.** The meter's second
hop is the instrument that catches a ruling naming a person whose CARD has not learned it —
it is what stopped T-0670. It reported `census_1840` as **27 reached, 27 judgeable, 27 on a
card, 0 unwritten** at the same moment that **15 of those 27 cards carried no mention of the
1840 census at all**, seven of them MATCHES (Philo Carpenter, John Calhoun, Ira Couch,
George W. Dole, William H. Stow, John Davis, Edward A. Rogers).

**Why.** The hop reads the domain's `crosswalk.json` — the spelling-pair rulings — and never
reads `resident_crosswalk.json`, which is where the head-to-person adjudications live. The 27
it counted were a different 27. So the domain's per-person rulings were invisible to the one
gate whose job is to see them, and stayed invisible under a `--check` that was green.

**This is a class, not an instance.** T-0698 spent census_1840's heads by hand
(`tools/spend_census_1840_heads.py`, gated in its own commit), which fixes this domain and
nothing else. Every other domain holding a `resident_crosswalk.json` — land_sales,
directories, civic, church, books, old_settlers — is measured by the same blind hop.

**The ask.** Make the second hop read `resident_crosswalk.json`'s `matched` and `candidate`
rulings alongside `crosswalk.json`'s, for every registered domain; then re-measure and report
what it finds. Expect it to go red somewhere, and expect that red to be true — the ceilings
were set against a count that was missing this whole class of ruling, so raising or spending
is a ruling in itself and belongs to whoever takes it.

**Links:** T-0698 (found it; spent census_1840) · T-0670 (stopped by the hop when it could
still see one ruling) · T-0714 (gated the crosswalk's `--check`) ·
`tools/measure_research_spend.py` · `tools/spend_census_1840_heads.py`.
