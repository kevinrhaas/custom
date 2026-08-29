---
id: T-0363
title: The South Water frontage run is dealt lots 0, 2 and 4 and all three of its roofs stand on lot 4
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

The South Water frontage run is dealt lots 0, 2 and 4 and all three of its roofs stand on lot 4.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured on `dev` on 2026-08-29 while placing John Holbrook's store (T-0358).
`data/reconstruction/1835_platted_block_parcels.json` deals `blk_south_water_dearborn`'s
South Water frontage run the lots **0, 2 and 4**, and its own `runs` note says the three
units are "packed west from their east end". On the committed geometry they are packed so
tightly that **all three stand on lot 4**:

    lot 0  chicago_american_office, recon_..._a3_06 (the alley privy)
    lot 2  frederick_thomas_shop
    lot 4  recon_..._c3_01, recon_..._c3_02, recon_..._d1_05   <- the whole run

`tools/plat_occupancy.py`'s `lot_holders` says so directly. Nothing here is physically
wrong — the units abut in a row on the frontage, which is what T-0078 and the owner's
"more and denser buildings" instruction asked for — and nothing overlaps. What is wrong is
that the recipe's `frontage.lots` and the ground disagree about which lots the run is on,
and **no gate can see it**, because `tools/generate_block_infill.py` asks
`exclusive_lots(..., exclude=mine_ids)` with its own records excluded. A rule that counts
one principal roof to a lot is enforced against everybody except the run it exists to
place.

That matters beyond bookkeeping: the same accounting refused T-0358's documented store on
lot 0, on the ground that the lot was already held, while three anonymous roofs stand
unremarked on one lot two doors east.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The disagreement is either closed (the recipe's `frontage.lots` names the lots the run
  actually stands on) or declared in the recipe's own words, with the reason.
- Whichever is chosen, a gate can see it: the run's own records are no longer invisible to
  the lot-occupancy assertion that is applied to everything else, or the assertion says in
  writing why they are exempt.
- The other four blocks of the South Water row are measured the same way and the result is
  stated, because a packing rule that did this here did it wherever it was used.
- No roof moves and no household is re-homed; this is an accounting repair, not a re-deal.
