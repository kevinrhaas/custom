---
id: T-0268
title: The west end of South Water's Franklin face lost its walk to a 10 mm ground change
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



**Acceptance:** (state it before working — the definition of done, never weakened to pass)

The plank walk on `blk_south_water_franklin`'s north face runs 91.4 m of a 96.5 m block
face. It ran the whole 96.5 m until T-0219, and the 5.1 m it lost is at the WEST end —
the corner, where a walker arrives from the crossing.

**Measured.** T-0219 re-traced the South Branch off a window 280 px taller on the same
Wright 1834 sheet. The main stem's traced south bank moved about a metre near local
E +220, which dropped the ground over the first five metres of this face by **10 mm**
(0.681 -> 0.671 m at E 219, 0.704 -> 0.694 at E 222, tapering to 0 by E 235) and
steepened it by the same amount. That face's westernmost walking deck was already the
marginal one — **69 mm of roll against the five others' 5-10 mm** — and the extra few
millimetres put it over `tools/generate_frontage_works.py`'s flatness bar. The deck count
for the face went 6 -> 5 and the walk's start moved from 0.0 m to 5.1 m.

**Why it is a ticket and not a repair inside T-0219.** Nothing here is wrong. The walk
rule refused ground that genuinely rolls more than it allows, and the ground genuinely
rolls that much — the change is inside the trace's own +/-20 m planform uncertainty and
the deck was one bad millimetre from refusal before the terrain moved at all. What the
smoke's T-0188 clause asserted was 96.5 m of continuous walk on this face, and it is now
a re-banked 91.4 (`tools/smoke_renderer.mjs`, floor moved 95 -> 90 with the reasoning at
the call site). A re-bank is honest and a repair would be better.

**Three ways it could go, none of them costed:**

1. The bar is right and the ground is right, and the corner simply has no walk. Then say
   so where a visitor can read it: the face's refusal list carries every other refusal's
   numbers and this one is invisible, folded into the run's start offset.
2. A walking deck may follow the ground instead of sitting flat on it. Every other deck
   on the street is flat because the ground under it is; this is the first place the two
   have had to disagree, and a deck that steps is a different object from one that tilts.
3. The flatness bar itself is a number nobody has re-derived since the walks landed. If
   it is a plank-carpentry limit it should be sourced; if it is a look, it should say so.

**Acceptance:** either the 5.1 m is walked again and the smoke's floor goes back to 95, or
the refusal is visible on the face's own record with its measured roll, and this ticket
closes with which of the three it was and why.
