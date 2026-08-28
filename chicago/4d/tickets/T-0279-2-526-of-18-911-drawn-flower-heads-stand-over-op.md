---
id: T-0279
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

**Acceptance:** the R-BUG7 head-support gate is green at desktop 1280x800 on an unmodified
`dev`, or the 13.4 % of heads it names are shown to be correctly placed and the gate is
corrected to say so — with the reason the figure moved recorded either way. Never the bar
lowered to fit.

**What was seen.** `tools/smoke_renderer.mjs` stage 7, desktop 1280x800, twice on the same
tree, on `dev` at `5b69f17c` with no renderer or data change:

```
FAIL  [5:54] desktop 1280x800: every drawn flower head has a plant under its own stalk
      — 2526 of 18911 drawn heads over 40 poses had nothing under the foot of
      their own stalk; worst flora-head-corymb at from_above 270deg, foot 1.61 m,
      0.61 m over its base over open ground
```

**13.4 % of drawn heads**, and the worst case is `over open ground` rather than over a gap —
an ORPHAN, a flower head with no plant beneath it at all. The mobile half of the same stage
does not reach this check's failing case, so it is a desktop-only reading today.

**It is new, and it is not a branch's.** `tools/dev-smoke-state.json` records `dev`'s standing
desktop part 7 as of 2026-08-28T00:55 with two failures — the tree-station gate (T-0243) and
the suite body killed at the per-command ceiling — and this is not among them. It was found
while measuring stage 7 for T-0225, whose diff is confined to the seam block BELOW this check
and reads no flora module, so it cannot be that either.

**Where to start.** The two flora changes that landed on `dev` immediately before, both of
which move which heads are drawn: T-0209 (the prairie's flowers carried out past the near
ring to 119.9 m, on the far band's aggregate clumps) and T-0214 (the nine flower-head ceilings
split by measured demand, `HEAD_SHARE`). The far band's `minPx` reach rule and `headRingAt`
are the two places a head can be drawn where its plant is not.

**Why it matters, and why the two readings are different findings.** R-BUG7's invariant is
that a head can only be drawn where its own plant is, because its ring is DERIVED from that
plant's (`headRingAt`). A red here says either

  * the invariant is broken in the drawing — a visitor sees flowers hanging in the air, which
    is the T-0035 defect in a new place and is visible; or
  * the gate has stopped being able to find the plant it should match, which is exactly the
    shape T-0243 and T-0244 describe for the timber gates since T-0223's lattice landed, and
    is a gate defect rather than a scene one.

Both are worth knowing and they are not the same thing. Whichever it is, say which.

**Links:** `tools/smoke_renderer.mjs` (stage 7, `headSupport`) ·
`renderers/web/js/flora.js` (`headRingAt`, `HEAD_FADE_AT`, `HEAD_SHARE`, `far.minPx`) ·
`tools/measure_head_support.mjs` · `tools/dev-smoke-state.json` ·
T-0209 · T-0214 · T-0035 · T-0243 · T-0244 · T-0225.
