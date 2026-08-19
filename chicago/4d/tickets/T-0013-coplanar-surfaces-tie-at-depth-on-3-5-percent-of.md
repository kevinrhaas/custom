---
id: T-0013
title: Coplanar surfaces tie at depth on 3.5 percent of the aerial frame
state: open
epic: RENDERING
requested_by: loop
seen: false
effort: M
legacy_id: R-BUG6(c)
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

After R-BUG6(a)/(b), 3.5 % of the aerial frame is still two surfaces at one depth —
genuine coplanar ties, mostly roof/wall junctions. Deep history: § R-BUG6(c) (~8988).
Needs one bake (geometry separation).

**Acceptance:** the 2 mm-nudge instrument reads ≤ 1 % changed pixels aerial; no visual
regression at eye height.
