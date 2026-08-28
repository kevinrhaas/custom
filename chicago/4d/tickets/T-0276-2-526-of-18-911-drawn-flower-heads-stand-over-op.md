---
id: T-0276
title: 2,526 of 18,911 drawn flower heads stand over open ground with no plant under their own stalk, on an unmodified dev
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

2,526 of 18,911 drawn flower heads stand over open ground with no plant under their own stalk, on an unmodified dev.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Acceptance:** the R-BUG7 head-support gate is green at desktop 1280x800 on `dev`, or
the 13.4 % of heads it names are shown to be correctly placed and the gate is corrected
to say so — with the reason the figure moved recorded either way.

**What was seen.** `tools/smoke_renderer.mjs` stage 7, desktop 1280x800, on `dev` at
`5b69f17c` with no renderer or data change in the tree:

```
FAIL  desktop 1280x800: every drawn flower head has a plant under its own stalk
      — 2526 of 18911 drawn heads over 40 poses had nothing under the foot of
      their own stalk; worst flora-head-corymb at from_above 270deg, foot 1.61 m,
      0.61 m over its base over open ground
```

13.4 % of drawn heads, and the worst is `over open ground` rather than over a gap — an
ORPHAN, a flower head floating with no plant beneath it at all. The mobile half of the
same stage does not reach this check's failing case.

**Where it came from.** Not investigated here; found while measuring stage 7 for T-0225,
which touches only the seam block below it and cannot affect this reading. The obvious
suspects are the two flora changes that landed on `dev` immediately before: T-0209 (the
prairie's flowers out to 119.9 m) and T-0214 (the nine flower-head ceilings split by
measured demand). Both move which heads are drawn; `HEAD_SHARE` and the far band's
`minPx` are where to start.

**Why it matters.** R-BUG7's invariant is that a head can only be drawn where its own
plant is, because its ring is derived from that plant's (`headRingAt`). A red here says
either that invariant is broken in the drawing — a visitor sees flowers hanging in the
air — or the gate has stopped being able to find the plant it should be matching, which
is the shape T-0243 and T-0244 already describe for the timber gates since the lattice
landed. Both are worth knowing and they are not the same defect.

**Links:** `tools/smoke_renderer.mjs` (stage 7, `headSupport`) ·
`renderers/web/js/flora.js` (`headRingAt`, `HEAD_FADE_AT`, `HEAD_SHARE`, `far.minPx`) ·
T-0209 · T-0214 · T-0035 · T-0243 · T-0244.
