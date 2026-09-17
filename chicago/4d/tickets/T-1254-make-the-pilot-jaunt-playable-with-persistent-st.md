---
id: T-1254
title: Make the pilot jaunt playable with persistent stop navigation
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

Implement a reusable session reducer/controller and concise stop panel. Play the schema ticket’s New in Chicago pilot end to end through the existing destination/travel adapter.

**Depends on:** T-1253

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. States cover opening, travelling, atStop, optional detail pause, outcome and menu; use session/leg tokens so late callbacks cannot advance a replacement jaunt.
2. Previous Stop, Next Stop, End Jaunt and Jaunts Menu stay available on mobile and desktop. Previous is disabled initially; last Next completes and returns to menu with a compact outcome.
3. End immediately cancels movement, clears active state and returns to the Jaunts Menu without confirmation. Menu pauses with Resume/Restart; selecting another jaunt replaces the session.
4. Previous/forward revisits do not repeat actions; explicit skip/default continuation is available when appropriate. Record visited stop IDs independently of display index.
5. No custom code for a particular jaunt. Start a second fixture, cancel during travel, restart and rapidly press navigation without duplicate arrivals, state leakage or orphan overlays.
6. Preserve free exploration and destination framing; add focused reducer and published UI checks for this complete vertical slice.
7. Start at the first stop immediately with safe framing; duration includes opening but no unpriced ride from the previous outing. Explore Myself cancels and clears any paused jaunt.

**Touch points:** proposed js/jaunts.js, js/jaunt-panel.js, main.js/hud.js adapters; pilot content and smoke hooks.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
