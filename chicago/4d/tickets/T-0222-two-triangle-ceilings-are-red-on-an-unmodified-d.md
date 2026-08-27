---
id: T-0222
title: Two triangle ceilings are red on an unmodified dev, and the third has 0.23 percent left
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

Two triangle ceilings are red on an unmodified dev, and the third has 0.23 percent left.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Measured 2026-08-27 under T-0199, twice on the same runner — once on an unmodified `origin/dev`
checkout and once on that ticket's branch — with `SMOKE_STAGE=4 node tools/smoke_renderer.mjs`. The
worst stand the sweep visits is **Lake Street at Canal, east down the axis** (`light`'s worst is the
forks, from Wolf Point).

| tier | ceiling | `origin/dev` | over by |
|---|---:|---:|---:|
| desktop `full` | 1,400,000 | 1,412,120 | **12,120** |
| desktop `balanced` | 1,210,000 | 1,252,802 | **42,802** |
| mobile `balanced` | 1,210,000 | 1,207,205 | 2,795 UNDER — 0.23 % |
| mobile `full` | 1,400,000 | 1,365,143 | 34,857 under |
| both `light` | 1,050,000 | 807,103 / 858,389 | comfortable |

**`dev` cannot pass its own smoke's stage 4 today, and no ticket said so.** T-0089 owns the `light`
ceiling, T-0147 owns re-lowering the ceilings once the trims land and T-0190 owns the street tier's
ceiling — none of them records that two of the six readings are ALREADY outside their ceilings on an
untouched tree. That matters because the next parcel to add anything visible reads its own smoke as
red and cannot tell its cost from the standing debt: T-0199 hit exactly this and is parked on it.

**Where the cost sits.** Adding 136.7 m of plank walk and two board crossings under T-0199 cost
`full` +6,496 and `balanced` +6,178 triangles at that stand, and `light` **+840** for the same
geometry — because `light` holds street furniture back at ±120 m while `full` and `balanced` both
draw to ±240 m. The overage is street-edge furniture drawn at half a kilometre.

**Acceptance:** either the two desktop readings come back inside 1,400,000 and 1,210,000 at that
stand on an unmodified tree — by the furniture reach, by T-0146's chunk merge, or by whatever the
measurement says is paying — or the ceilings are re-derived from what the tiers are FOR with the
reasoning recorded, never raised to fit a reading. Whichever it is, the mobile `balanced` margin is
restated with it, because 0.23 % is not a margin.

**Links:** T-0199 (found it, parked on it) · T-0190 · T-0147 · T-0146 · T-0089 · T-0115 (the tier
ledger) · T-0056 (the enclosure layer pays full cost at every tier)
