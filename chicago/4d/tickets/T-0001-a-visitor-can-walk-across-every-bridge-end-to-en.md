---
id: T-0001
title: A visitor can walk across every bridge, end to end
state: open
epic: TOWN
requested_by: owner
seen: true
effort: M
legacy_id: K10
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

**The owner's ask, verbatim (K10):** "How would a wagon cross that?" Every bridge floats
over its banks (`approach_not_modelled`), and the walker cannot cross one — it follows the
terrain heightfield, so a deck is not ground.

Two halves. (1) **Walker deck support** — the walker stands on a bridge deck instead of the
water under it; renderer-only, no bake. Ship this first. (2) **Approach earthworks** — log
abutments in the shallows (the 1883 settlers' statement), wagon-plausible gradients meeting
the deck at grade; geometry, needs the bake. Regrade `ground_contact` per bridge as it lands.

**Acceptance:** spawn on foot, walk across both branch bridges and the Dearborn drawbridge
end to end without falling into the river; a smoke gate walks one and asserts deck height
under the walker the whole way. Deep history: docs/ROADMAP.md § K10 (line ~9671).
