---
id: T-0688
title: The wagon-variety gate counts street bearings, so re-deriving a street took it from 9 buckets to 7 and it is at its floor of 8
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The wagon-variety gate counts street bearings, so re-deriving a street took it from 9 buckets to 7 and it is at its floor of 8.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-0447 (PR on `steward/t-0447-north-water-east-end`), which is parked on this
and on nothing else.

## The assertion

`tools/smoke_renderer.mjs:3762`, part 2, both viewports:

```js
check(`${label}: the town's wagons vary in type and in the way they stand`,
  kinds.size >= 3 && kinds.has('covered') && kinds.has('cart')
    && kinds.has('farm_box')
    && commonest <= townWagons.length * 0.75 && bearings.size >= 8, …
```

where `bearings = new Set(townWagons.map((w) => Math.round(w.bearing / 5)))`.

## What it actually measures

A town wagon drawn up "along the road" takes the bearing of the street segment it stands
on, so this clause counts **distinct street bearings that happen to have a wagon on
them**. It is a property of the street network, not of the wagon rule, and the comment
above it justifies only the three `kinds` clauses — the floor of 8 is unexplained.

## Measured, on `dev` and on the T-0447 branch

| bucket | dev | branch |
|---|---|---|
| 0° | 5 | 5 |
| **90°** | 14 | **15** |
| **95°** | **1** (`town_wagon_north_water_7`) | — |
| 175° | 1 | 1 |
| 180° | 9 | 9 |
| **225°** | **1** (`town_wagon_north_water_8`) | — |
| 270° | 33 | 33 |
| 355° | 1 | 1 |
| 360° | 1 | 1 |
| **buckets** | **9** | **7** |

Both lost buckets were single wagons on North Water Street's **hand-drawn** east tail —
the two vertices T-0447 removed as unsourced. `north_water_7` moved 0.9 m and its street
segment's bearing went 96.2° → 90.2°, merging it into the 90° group; `north_water_8` was
refused outright, with the rule's own reason: *"on the left verge, it reaches into the
North Water Street travelled track, which is where a visitor walks."*

So **the gate was passing with one bucket of margin, and both of the buckets carrying that
margin were artifacts of a line nobody derived.** It is also weaker than 9 makes it look:
0° and 360° are the same heading, and 175° and 180° differ by five degrees, so the town's
66 wagons stand in about four real directions.

## The question, and it is a judgement, not arithmetic

Two answers are defensible and T-0447 declined to pick one inside its own PR, because
either is a change to a gate made by the change the gate refused:

1. **The proxy is wrong.** Re-cut the clause to measure what the comment says it measures
   — the wagon rule's own variety, `drawn_up` mix and kind mix — and stop counting street
   bearings, which no wagon rule controls.
2. **The town is genuinely thin.** 65 wagons in four real directions is what this town
   has; keep a bearing measure, but set its floor from something derived rather than from
   whatever the last measurement happened to read.

**Acceptance:**

1. The clause either measures the wagon rule or measures the street network, and says
   which in its own comment.
2. Its floor is derived from something, not from the last green reading.
3. The T-0447 branch's diff is green under the re-cut gate, or T-0447 is told why not.
