---
id: T-1255
title: Offer live jaunt travel modes and honest quick-play estimates
state: open
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Give every jaunt a changeable recommended mode and a duration that follows the actual selected route/pace. Prevent travel from consuming the entire outing.

**Depends on:** T-1254

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Use the existing instantly/walk/wagon/horse/fly modes and paceSpeed settings; estimate ground routes through route.js and flight ascent/cruise/descent, plus primary reading/actions.
2. Show approximate selected-mode duration before start and remaining time during play. Unknown/unroutable distances have explicit fallback instead of made-up five-minute labels.
3. Changing mode mid-leg cancels/replans from current position, keeps target and narrative state and changes real motion; a setMode label change alone does not satisfy acceptance.
4. Go straight to next stop remains available during every leg and stalled recovery. Safe arrival still frames the building and uses collision/ground contracts.
5. Manual movement pauses the jaunt travel without losing progress; ending/menu cancels it. Temporary mode choices do not silently overwrite the user’s free-exploration defaults.
6. Measure a near walk and a long cross-river horse route versus fly/instant; assert ETA changes, safe arrival, no extra inventory/reward and no stale callbacks. Viewing flight is not narrated as historical transport.

**Touch points:** js/travel.js, js/route.js, main.js arrival adapters, jaunt-menu/panel and focused route timing checks.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
