---
id: T-1127
title: The stem budget binds now the ground reaches Kinzie's Addition, so the wood is cut off in a straight line at the north edge
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-14
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The stem budget binds now the ground reaches Kinzie's Addition, so the wood is cut off in a straight line at the north edge.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-1122, 2026-09-14**, as an inherited red on three smoke legs — not that ticket's
diff, which is prose in two python passes.

`renderers/web/js/trees.js` plants until a stem budget is spent and then stops, and the
smoke's loader check fails the moment it stops partway:

    trees: the full stem budget bound at 3030 trees, so the planting loop stopped partway
    north and the wood is cut off in a straight line rather than thinned — lower full's
    keep fraction, do not lower the budget

Measured on this tree, 2026-09-14: `desktop 3,12`, `desktop 13` and `mobile 3,12-13` all
fail on it and on nothing else (the light level binds at 1,110 stems, the full level at
3,030). The same failure is already on the record against
`steward/t-1123-north-ground-kinzie` at 11:48 — the branch that IS dev's tip — so it
arrived with T-1123 and dev has carried it since. T-1123 grew the modelled field by
seventy-seven per cent northward; the budget did not grow with it, and the planting loop
reaches the new ground last.

The message says what the repair is not: **do not lower the budget.** The wood is cut off
because the loop ran out of stems before it ran out of ground, so the fix is the keep
fraction — plant the whole field more thinly rather than part of it at the old density —
and a check that the north edge is thinned and not truncated.

**Acceptance:** the loader check passes at both viewports; the wood reaches the north edge
of the enlarged field; the stem budget is unchanged; and the smoke says which level bound,
as it does now.
