---
id: T-0247
title: The light tier draws 83 calls against the 80-call floor restored yesterday, on an unmodified dev
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

The light tier draws 83 calls against the 80-call floor restored yesterday, on an unmodified dev.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`tools/smoke_renderer.mjs` stage 4 at desktop fails on an **unmodified `dev`**:

```
FAILURES:
 - desktop 1280x800: the light tier draws inside its 80-call floor at the worst stand
   light  worst 746,060 tris of 785,000 at Lake Street at Canal
          worst 83 calls at Lake and Market, the corner itself
```

**Found while working T-0193** (PR #421), whose branch changes one JSON string and no geometry at
all. It reproduced identically against the untouched `dev` mirror
(`git archive origin/dev site/chicago/4d`, then `SMOKE_ROOT` pointed at it), so it is
neither that branch's nor any branch's — it is the state of `dev`.

**Why this is fresh rather than long-standing.** T-0300 restored this floor YESTERDAY,
deliberately and with the reasoning written into the changelog: *"it is eighty again —
the count this project chose before any of the summer's building, not one fitted around
today's reading of seventy-five."* It read 75 then, at the stand it was checked at. It
reads 83 now at `lake_and_market`. Something between those two readings added eight draws
to the lightest tier, and the ticket that restored the floor is the reason anybody can
tell.

**The triangle ceilings are all green** — `light` sits 38,940 under its 785,000, and
`full` and `balanced` pass too. This is the draw-call half of the budget alone, which is
exactly the half T-0300 argued was worth keeping as a separate promise: *"apart from
triangles there is a tally of how many separate times a frame is handed to the graphics
card ... which guarantees a person nothing"* if it is allowed to float.

**Where to start:** the worst stand is `lake_and_market`, not the axial view, and the
count is a per-stand worst — so the question is which layer stopped batching at that
corner specifically. T-0146 (merge far chunks back into single draws) and T-0150's
`furnitureReachM` distance cull are the two mechanisms that hold this number down at
`light`, and the hitching posts (T-0194) and Randolph's street edge (T-0240) are the two
parcels that landed between T-0300's reading and this one.

**Do not fix it by moving the floor.** T-0300's whole argument is that 80 is a chosen
number rather than a fitted one.

**Links:** T-0300 (restored the floor) · T-0135 (the five stands) · T-0146 · T-0150 ·
T-0149 · T-0193 (found it) · T-0240 · T-0194.
