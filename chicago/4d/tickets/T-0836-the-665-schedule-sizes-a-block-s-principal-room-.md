---
id: T-0836
title: The 665 schedule sizes a block's principal room in free LOTS, and on a business-front lot the free frontage METRES bind first
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The 665 schedule sizes a block's principal room in free LOTS, and on a business-front lot the free frontage METRES bind first.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-0431 while dealing the second parcel on `blk_south_water_clark`, and it is the
reason that block was dealt 4 roofs and built 2.

`tools/reconcile_665.py` sizes a block's principal room as `ROW_UNITS_PER_LOT * (free_lots - 1)`.
That counts LOTS. Under the owner's business-front clause of 2026-08-27 a lot already carrying a
documented store standing at the street is still counted FREE — correctly, because the store does
not exhaust it — but it is by construction not a whole lot, and what binds a second roof there is
the free FRONTAGE METRES, not the lot.

Measured on `blk_south_water_clark` lot 2, on the committed north face:

| quantity | metres |
|---|---|
| lot 2's projection on the face | 24.64 → 49.75 |
| less the plat module's 1.5 m margin each side | 22.11 buildable |
| Pruyne & Kimball's drug store holds | 39.11 → 46.83 |
| clear to the west | **12.97** |
| clear to the east | **1.42** |

The schedule dealt this block three principal roofs. One fitted — the C4 store, 10.63 m wide, in
the west gap. The other two are a larger one-and-a-half-storey house and a merchant two-storey
house, both over eight metres wide, and neither can stand: 1.42 m is the only frontage left, a
principal roof may not stand on a lot the run was not dealt, and a house set back at the recipe's
own typology range cannot clear the drug store's back wall by the three metres the separation gate
requires. They returned to the south district's balance, where every marginal still sums to the
programme's total, so nothing is lost — but the schedule PROMISED room that the ground never had,
and the next business-front lot will promise it again.

**Acceptance:** `reconcile_665.py`'s principal-room sizing accounts for the frontage a documented
building already occupies on a business-front lot, so a block's stated headroom is room a parcel
can actually be dealt; the re-derivation is committed; and no roof already standing moves. State
the before/after headroom for every block the change touches, and say which ones stop over-promising.

**Links:** T-0431 (where it was measured) · T-0420 · T-0028 (the programme) · T-0213 ·
`tools/reconcile_665.py` · `tools/generate_block_infill.py`.
