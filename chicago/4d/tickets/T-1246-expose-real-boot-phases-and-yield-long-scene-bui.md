---
id: T-1246
title: Expose real boot phases and yield long scene-building tasks
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

Make loading responsive and measurable before changing its presentation. Extend main.js progress/boot with explicit phase boundaries, completed units where available, monotone real progress and an essential-ready barrier.

**Depends on:** None within this feature; consume current dev records.

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Expose start/end/error/ready events and phase timings through a small controller and the existing harness; include first usable frame and interaction readiness.
2. Time-slice the measured long CPU phase (including prairie work where indicated) at safe paint boundaries; compare geometry/scene counts to the unchanged path and show statuses repainting during that phase.
3. Keep current useful phase labels visible; optional census/history failures do not block scene entry. Essential failure cannot announce Ready.
4. Record cold and warm timings at both gate viewports and light/full detail; bounded local timing history is optional, build-keyed and safe when storage fails.
5. Test delayed/failed phases, no-progress work, tab resume and deterministic results; do not replace actual completion with a timeout.

**Touch points:** renderers/web/js/main.js, scene-loader.js, flora.js only where the measured long task requires it; focused boot harness.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
