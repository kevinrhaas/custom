---
id: T-0247
title: The flora census reads BUDGET.triangles, so 10,400 triangles of new walk swing a frame by 40,000 in either direction
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-27
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The flora census reads `BUDGET.triangles`, so 10,400 triangles of new walk swing a frame
by 40,000 in either direction.

**Found by T-0192**, which added Market Street's plank walk — 208.8 m of it and one
crossing, about **10,400 triangles** at this layer's own measured 42.8 a metre — and
then read all five of T-0135's stands on the published mirror, desktop 1280x800, against
a `dev` baseline read twice and identical to the triangle:

| stand | tier | dev | with Market | delta |
|---|---|---:|---:|---:|
| the forks | `full` | 1,369,931 | 1,338,875 | **−31,056** |
| the forks | `balanced` | 1,201,344 | 1,226,196 | **+24,852** |
| the forks | `light` | 739,040 | 739,488 | +448 |
| Lake at Canal | `full` | 1,333,883 | 1,316,633 | −17,250 |
| Lake at Canal | `balanced` | 1,200,178 | 1,217,380 | +17,202 |
| the Sauganash | `full` | 899,921 | 871,970 | −27,951 |
| the Sauganash | `balanced` | 780,181 | 792,814 | +12,633 |

**Adding geometry made `full` cheaper at every one of the five stands.** That is not a
measurement error — the instrument reproduces itself to the triangle, and `check.sh`
confirms the only thing that changed in the published tree is the frontage record.

**Where it comes from.** `DETAIL.full` and `DETAIL.balanced` in
`renderers/web/js/main.js` are IDENTICAL apart from the ceiling number itself —
`shadowReachM: 240`, `furnitureCastsShadow: true`, `furnitureReachM: null` on both. So
the only thing that can make them different scenes is something downstream reading
`BUDGET.triangles`, which `applyDetail` sets from the tier and which the flora planting
is handed. The flora census is therefore a function of the tier's own CEILING, and a
tenth of a per cent of new geometry moves it by three per cent of a frame.

**Why it matters more than its size.** Every ceiling reading this project takes — every
"OVER by N", every re-basing argument in `main.js`, T-0223, T-0229, T-0147, T-0240's
174 triangles — is taken on an instrument whose answer moves ±40,000 when the scene
moves 10,400, and moves it in OPPOSITE directions at two tiers. A parcel can be refused
for triangles it did not add, and one can be accepted for the same reason.

**Acceptance:** the mechanism is named in code (which call reads `BUDGET.triangles`, and
what it does with it), and one measurement demonstrates it: the same geometry change
read at two tiers whose only difference is the ceiling number, with the flora census
printed beside the triangle count at each. Then either the coupling is defended in
writing where the number is set, or the census is pinned so a tier's ceiling no longer
changes what the tier draws. No ceiling moves in this ticket.

**Links:** T-0192 (found it) · T-0223 · T-0229 · T-0147 · T-0225 · T-0135 (the stands) ·
`tools/measure_detail_ceilings.mjs`.
