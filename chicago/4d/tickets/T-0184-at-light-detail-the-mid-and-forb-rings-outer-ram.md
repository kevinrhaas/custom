---
id: T-0184
title: At light detail the mid and forb rings' outer ramps dither inside the verge
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

At light detail the mid and forb rings' outer ramps dither inside the verge.

Found while shipping **T-0093** (the near/mid handover), and named there as the residue that run
holds rather than closes.

**What it is.** T-0093 converted two boundaries from coverage ramps to density handovers — the near
ring's OUTER edge and the mid ring's INNER edge — so nothing inside the near/mid crossover is
written through the 4×4 Bayer screen door any more. The mid and forb rings' own OUTER edges are
still coverage ramps. At `full` that is fine: they run 18–27 m and 18.9–27 m, where a plant is a
handful of pixels and the far band stands over the same ground (T-0086). **At `light` — the phone —
the rings are 13.0 m and 13.0 m, so the same ramps run from 5.4 m and from 7.4 m**, which is inside
the verge a walker looks at. Measured on the published mirror before T-0093 landed, at the open
prairie stand at 390×780: `flora-mid` 122 partial instances inside 9 m, `flora-forb` 14.

**Why T-0093 did not do it.** Different edge, different ticket: T-0093's acceptance is about the
handover from the near tufts to the mid cards, and its two named stands are in a roadway where the
near ring places nothing at all. And the outer edge is not free the way the inner one was — the mid
and forb rings' outer boundaries carry the world-anchored **fringe** that keeps the sward's edge off
a constant screen row (ROADMAP § S6a item 3), and `tools/smoke_renderer.mjs` holds that with
*"the boundary's variation is the fringe, not a hole in the field"* (`minReach >= nominal − fringe −
1.2`, `meanReach >= nominal − 0.5 × fringe`). A density spread thins the outermost slots, so the
drawn edge moves in by roughly `band / N` for the N slots in a bearing bin's outer metre, and that
interaction has to be measured before it is chosen — not assumed to be small.

**Acceptance:** at 390×780 at `light`, `node tools/measure_near_verge.mjs --gate` reports **0.000 %**
of the frame screen-doored inside 9 m at every stand (it is the `ditheredShare` line, not the
handover line T-0093 already holds at zero) — and both boundary checks in the smoke's part 7 stay
green at their existing bars, with the measured reach printed before and after. Before/after pairs
of the verge at eye height on a phone.

**Links:** T-0093 (which found it, and the instrument) · T-0086 (the far band, and why the outer
edges were left) · ROADMAP § S6a items 3 and 3b · `renderers/web/js/flora.js` (`TUNE.mid.band`,
`TUNE.forb.band`, `fringeOf`, `slotRing`).
