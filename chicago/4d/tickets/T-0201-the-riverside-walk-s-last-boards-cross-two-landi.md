---
id: T-0201
title: The riverside walk's last boards cross two landings' boarding aprons
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

The riverside walk's last boards cross two landings' boarding aprons.

Found by **T-0058**, which made the wharf decks walk surfaces and gave their landward band an
inclined boarding apron (L182). The junction was measured and left standing rather than fixed,
because fixing it means deciding which layer gives way and that is a parcel of its own.

## What was measured

`river_plank_walk_wharf_reach` is bounded by Jones's landing ON PURPOSE — its own note says *"that
wharf is where the town's own riverfront walking surface begins"* — so its outer boards run into
the landward strip of two decks. Sampled at 0.25 m along the walk's centreline and both edges,
against the committed heightfield:

- it reaches at most **1.30 m** into the 2.0 m apron band, at `h_jones_store` and
  `carpenter_south_water_store`, and touches no other landing;
- across that overlap the apron's top runs from **0.18 m BELOW the boards to 0.37 m above them**,
  so the two surfaces cross rather than one clearing the other.

The plank deck is 0.05 m and the apron slab 0.14 m, so over roughly half a metre of the band the
two solids interpenetrate. Before T-0058 the wharf's landward band was a level slab at 0.90 m and
flew clear over the boards with 0.45 m to spare — that was not better, it was a deck hanging over
a walk with daylight under it, which is the fault the apron exists to end.

## Why it is not obviously the wharf's fault

Both records are right about their own ground. The walk is *supposed* to end at the landing; the
apron is *supposed* to reach the bank. What is missing is that neither layer knows the other
exists: `wharves.js` publishes a planting keep-out that `flora.js` and `trees.js` honour, and
`frontage.js` does not read it — so a plank walk may be laid across a wharf deck's outline while
nothing may grow there.

## The three candidate fixes

1. **The walk gives way**: `frontage.js` (or the walk's generator) refuses board stations inside a
   wharf's `keepOut`, so the run stops at the landing's own outline instead of under it. Truest to
   the record's stated intent, and it shortens a committed walk.
2. **The wharf gives way**: the apron holds the ground where a walk covers it. Cross-layer coupling
   in the other direction, and it would leave that landing unboardable from that side.
3. **They are made one junction**: the walk's last boards run onto the apron at its lip, drawn as
   one surface. The best-looking answer and the most work.

## Acceptance

At every point where a plank walk and a wharf deck share ground, the drawn timber of one does not
pass through the drawn timber of the other, asserted in `tools/smoke_renderer.mjs` against the
figures above; and the choice of which layer gave way is written down with its reason. The
frontage layer's own `deckAt` exclusion of `__wharf` decks (added by T-0058, with the reason) stays
either way — a board is never LAID on a wharf, whatever is done about the junction.
