---
id: T-1247
title: Roll the year back into a restrained time-machine arrival
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

Replace the static loading treatment with a modern 1960s instrument-panel feel: warm ivory, ink, muted brass and restrained split-flap year/source motion. Welcome visitors into a digital reconstruction.

**Depends on:** T-1246

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Use real phase events plus bounded phase interpolation: current calendar year (2026 now) descends monotonically and never shows 1835 before essential readiness.
2. Readiness settles to exactly 1835 and Welcome to Chicago, summer 1835; the final arrival text, number and welcome transition agree. No minimum animation duration; at most 300 ms cosmetic settle, immediate for reduced motion.
3. Slow phases ease toward a bound; actual phase text stays legible. An error stops the ticker and offers retry without reporting arrival.
4. Provide the source/fact flip-card slot consumed by the catalog ticket; initial operational copy does not pretend that archival research happens live.
5. Check 390x780, 1280x800, reduced motion, 320 px width, long source titles, failed load and a sub-second warm boot; screen readers announce phases rather than every year.

**Touch points:** renderers/web/index.html, css/walk.css, proposed js/arrival.js; boot adapter.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
