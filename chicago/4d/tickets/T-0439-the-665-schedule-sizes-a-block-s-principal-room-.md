---
id: T-0439
title: The 665 schedule sizes a block's principal room in LOTS, so a business-front lot already carrying a documented store is dealt roofs its free frontage cannot hold
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

The 665 schedule sizes a block's principal room in LOTS, so a business-front lot already
carrying a documented store is dealt roofs its free frontage cannot hold.

**Where it was measured.** T-0431, `blk_south_water_clark`'s second deal, 2026-08-30.
`tools/reconcile_665.py` sizes a block at `principal = ROW_UNITS_PER_LOT * (free_lots - 1)`
— three party-line units per free lot, less the one the block keeps open — and dealt this
block three principal roofs and one ancillary. The block's two free lots are lot 1, wholly
empty, and lot 2, free ONLY under the owner's 2026-08-27 business-front clause, which says
Pruyne & Kimball's drug store standing at the street does not exhaust the lot. Measured on
the committed face, lot 2 projects between 24.64 m and 49.75 m; with the plat module's
1.5 m margin off each side line it offers 22.11 m of buildable frontage, and the drug store
holds 39.11 m to 46.83 m of it. **12.97 m are free to the west and 1.42 m to the east.**
The parcel could stand ONE unit — a C4 at 10.632 m — where the schedule had dealt three,
and the other two dealt roofs went back to the district balance.

**Why it is not just this block.** `ROW_UNITS_PER_LOT` is measured at the smallest lot on
the committed grid and is a claim about a WHOLE lot's frontage. A lot admitted by the
business-front clause is by construction NOT whole: something documented already stands on
part of its street line. Every future deal on that clause inherits the same arithmetic, and
the four South Water blocks of T-0420 are exactly the ground the clause reaches.

**What the fix is not.** It is not lowering `ROW_UNITS_PER_LOT`; that number is right for a
free lot, and the eleven blocks already built on it are correct. The room a business-front
lot has left is a length, not a count.

**Acceptance:**

- `tools/reconcile_665.py` sizes a lot admitted by the business-front clause on the FREE
  METRES of its face — the lot's buildable frontage less the documented building's own
  span on it — rather than on `ROW_UNITS_PER_LOT`, and the arithmetic is imported by
  `tools/generate_block_infill.py` rather than retyped, on the T-A6 rule that the two
  halves derive occupancy the same way.
- The re-derivation moves no committed record: run against the tree as it stands, the only
  schedule rows that may change are ones whose block is admitted by the clause, and
  `tools/generate_block_infill.py --check` re-derives every existing parcel unchanged.
- The width a run needs is read from the family bands the block was dealt, not assumed —
  a block whose free metres cannot seat the NARROWEST family it was dealt is dealt none,
  and says so.
- `blk_south_water_clark` is the regression case and is named in the tool's own test: it
  must size to 1 principal, not 3.

**Links:** T-0431 (where it was measured) · T-0420 · T-0079 (`ROW_UNITS_PER_LOT`) ·
T-A6/T-A7 (the two halves derive occupancy once) · the owner's 2026-08-27 business-front
clause in `tools/plat_occupancy.py` · `tools/reconcile_665.py`.
