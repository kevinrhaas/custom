---
id: T-1262
title: Publish New in Chicago as a five-minute jaunt
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

Author the complete priority jaunt `new-in-chicago` from its brief in JAUNTS-INITIAL-LIBRARY.md. Reuse current source/structure/business/resident records and the shared engine.

**Depends on:** T-1259, T-1256, T-1257, T-1258

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Deliver opening, 5 purposeful stops (adjust only with a stated narrative reason), concise actions, supported card links, recommendation and endings in JSON; the catalog card launches it.
2. Arrive at the Sauganash; learn how the old mail corner oriented the settlement; note a supply shop; inspect a useful notice; choose a boarding arrangement. A low-pressure outing with one optional preference and a route-note keepsake.
3. Verify each proposed stop against the compiled scene and trace each factual claim to source ID plus locator; retain inference/reconstruction notes and append narrative liberties. Hogan’s held the post office earlier; the record says it moved about July 1834. This is not the current 1835 mail counter. Engine pilot becomes this final authored jaunt, not a duplicate.
4. Award Finding Your Feet in Wayfinding without forcing extra scoring. Test every authored choice/outcome and no dead ends or double rewards.
5. Time the primary path in the recommended mode walk aiming at 4-6 minutes (a justified 3-4-minute outing is fine); compare Fly/Instantly and confirm deeper cards are optional.
6. Show mobile/desktop menu-to-ending evidence, Previous/Next, mid-leg mode switch and End-to-menu. No new engine branch keyed to this jaunt.

**Touch points:** data/jaunts/new-in-chicago.json, corresponding brief/dossier and generated catalog; existing cards, not new geometry.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
