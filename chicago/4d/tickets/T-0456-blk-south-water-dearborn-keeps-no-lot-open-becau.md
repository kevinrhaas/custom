---
id: T-0456
title: blk_south_water_dearborn keeps no lot open, because the owner's business-front clause and the density standard's closing clause cannot both hold on a built-out block
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-30
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---
The core density standard (T-0079) closes with `a block still keeps a lot open`, and the
owner's 2026-08-27 business-front clause says a documented store standing at the street
does not exhaust its lot. On `blk_south_water_dearborn` the two cannot both hold, and
T-0432 is the parcel that reached it first.

**The arithmetic, and it is only arithmetic.** The block has eight lots. Lots 1 and 6 carry
the Mansion House and the Chappel infant school. The first deal (2026-08-15) was dealt the
frontage lots 0, 2 and 4 and built on 3 and 5 as well. T-0432's second deal takes lot 7,
the block's one free corner lot. That accounts for all eight, and the lot-accounting gate
in `tools/generate_block_infill.py` therefore has no lot left it may call open — so the
recipe's `open_lots` is empty for the first time in the programme.

**The unbuilt ground is real; what it is not is a LOT.** Lot 2 carries Frederick Thomas's
shop at the street and nothing behind it. Under the business-front clause the schedule
reads that lot as FREE — it is one of the two free lots the 665-roof programme counts for
this block — while the first deal's frontage run already accounts for it, so the gate can
call it neither open nor available. The yard behind that shop is exactly the vacancy the
standard's closing clause is about, and the recipe has no vocabulary for it.

**Which is the question.** Three shapes it could take, and the choice is the owner's because
it decides what a business-front lot IS rather than where a building stands:

  (a) **The closing clause yields**: a block whose vacancy lives behind a documented store
      has kept its open ground, and `open_lots` may be empty when the recipe can say where
      the vacancy is. Cheapest, and it needs a class the gate can check.
  (b) **The business-front clause yields on this block**: lot 2 is named open and the first
      deal's frontage entry gives it up. Costs the first deal a dealt lot and reopens
      arithmetic settled in August.
  (c) **A fourth class**, `vacant behind a documented storefront`, joins the three the gate
      already keeps disjoint. Most honest, most work, and it would reach every business-front
      block rather than this one.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The owner's answer is recorded where BOTH clauses are authored — the recipe's
  `placement_rule.density_standard` and `tools/plat_occupancy.py`'s module docstring — so
  the next parcel reads one rule and not two.
- `tools/generate_block_infill.py`'s lot-accounting gate implements it, with its four (or
  five) classes still provably disjoint and still covering every lot.
- `blk_south_water_dearborn` re-derives under it unchanged, or its change is stated. No
  roof moves to satisfy a bookkeeping rule.

**Links:** T-0432 (which reached it) · T-0079 (the density standard) · T-0105 (the sibling
class this one sits beside) · the owner's ruling of 2026-08-27 ·
`tools/plat_occupancy.py` § `shared_business_fronts`.
