---
id: T-0189
title: The five South Water stores standing on a lot the roof schedule already dealt
state: open
epic: TOWN
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-0127
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The five South Water stores standing on a lot the roof schedule already dealt.

Piece 2 of 2 of **T-0127 — The rest of the town gets the street edge**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

These five documented buildings on South Water Street's south side were placed in August 2026 by
reading the MODERN West Wacker Drive centreline out of OpenStreetMap and stepping 12.2 m south of
it — each record's own `position.note` says so, and several already warn that *"modern Wacker Drive
is not exactly the 1835 South Water Street line"*. Measured against this project's committed South
Water centreline, offset by half the committed 80 ft corridor, each stands out in the platted
roadway, and `tools/generate_frontage_works.py` refuses the plank sidewalk along the stretch it
covers. T-0188 reconciled the other six of the eleven; these five it could not.

| store | out past the frontage line | would move | and would then seat |
|---|---:|---:|---|
| `h_jones_store` | 8.17 m | 9.67 m | `blk_south_water_wells` lot 0 |
| `carpenter_south_water_store` | 6.62 m | 8.12 m | `blk_south_water_wells` lot 2 |
| `chicago_american_office` | 6.91 m | 8.41 m | `blk_south_water_dearborn` lot 0 |
| `frederick_thomas_shop` | 6.25 m | 7.75 m | `blk_south_water_dearborn` lot 2 |
| `pruyne_kimball_drugstore` | 5.55 m | 7.05 m | `blk_south_water_clark` lot 2 |

**WHY EACH IS BLOCKED, MEASURED ONE AT A TIME (T-0188 ran all five separately).** Every one of those
lots is in its block's `frontage.lots` in `data/reconstruction/1835_platted_block_parcels.json` — the
665-roof schedule has already dealt that lot's roof to the anonymous South Water frontage run — and
`tools/generate_block_infill.py` refuses to deal a roof to a lot that already carries one: *"the
schedule's headroom is the block's, not the lot's"*. Nothing overlaps geometrically; the three runs
physically stand at the east end of their faces, well clear of all five stores. The conflict is
entitlement, not ground.

**Two honest routes, and the ticket is for choosing one with numbers rather than by taste.** Either
the three blocks' headroom is re-scored and the frontage runs give up the lots the documented
buildings take — which removes standing anonymous roofs from the street and has to be argued against
the owner's *"there should be more and denser buildings"* — or the runs' entitlement is re-pointed to
the lots they physically occupy, which needs `check_frontage`'s adjoining-strip rule and
`ROW_UNITS_PER_LOT` measured against the result. Either way `tools/reconcile_665.py` re-derives the
programme in the same commit.

**Acceptance:** all five are either reconciled with the committed plat or refused in writing with a
NEW reason (the roof-schedule collision having been resolved or shown unresolvable); South Water
Street's walk then runs unbroken except where its own ground refuses it, asserted by standing the
walker on it end to end; no standing roof leaves the town without that removal being argued and
counted; and all three detail tiers stay inside their ceilings. Never by weakening a gate.

**Links:** T-0127 (parent) · T-0188 (piece 1, which measured all of the above) · T-0115 (the tier
ledger) · `data/frontage/town_street_edge.json` `refused`, where all five are already named.
