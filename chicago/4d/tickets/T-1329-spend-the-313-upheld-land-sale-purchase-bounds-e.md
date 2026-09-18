---
id: T-1329
title: Spend the 313 upheld land-sale purchase bounds: each tract entered on or before 1 July 1835 by a purchaser the crosswalk joined to a card this town holds, written onto that card as a dated appearance and never as a residence
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-1319
opened: 2026-09-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Spend the 313 upheld land-sale purchase bounds: each tract entered on or before 1 July 1835 by a purchaser the crosswalk joined to a card this town holds, written onto that card as a dated appearance and never as a residence.

Piece 1 of 2 of **T-1319 — Spend the land-sale and enrichment units: the entered tracts whose purchaser join the adjudication upheld, and the corroborated_enrichment rows naming an arrival or origin no structured field carries**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**READ THIS BEFORE CLAIMING (T-1330, 2026-09-18).** A purchase bound is a DATED APPEARANCE,
and `persons[].dated_bounds[]` is the structured block a dated appearance belongs in. That
block is being introduced by **T-1326** (`tools/spend_civic_roll_bounds.py`, the town's own
rolls) and it is not on `dev` yet — check before you start:

    grep -rn 'dated_bounds' chicago/4d/tools/ | head

If it is there, write into it and do not invent a second shape for the same fact. If it is
not, T-1326 is still in flight and this ticket is not workable yet — say so and take the next
row rather than building a rival block, because two blocks carrying one fact is the
duplication this loop exists to avoid. The ticket was carried as `blocked-tech` for about an
hour on the day it was minted and then reopened, because a blocked ticket is not an open
owner and these 313 units have to defer to one (see below).

**The units.** `data/research/land_sales/spend_rulings.json`, rule
`the_purchase_bounds_a_held_residents_presence`, 313 rows — tracts entered on or before
1 July 1835 by a purchaser the crosswalk's T-0700 / T-0850 adjudication UPHELD against a card
this town holds. The rule's `ticket` was repointed from the split parent T-1319 to this
ticket by T-1330, because the parent stopped being `split_live` the moment its other child
closed and 313 units would otherwise have deferred to spent work (T-1237).

**The standing rule this whole domain was read under:** a purchase is a TRANSACTION and not a
RESIDENCE. The register's Residence column reads COOK, ILLINOIS, another county or UNKNOWN —
a county, a state, or nothing, and never a town. A row can bound a presence. It can never
assert one, and it may not move a grade or reopen an identity the crosswalk has ruled.

