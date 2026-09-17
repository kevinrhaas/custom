---
id: T-1264
title: Publish Across Wolf Point as a five-minute jaunt
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

Author the complete priority jaunt `across-wolf-point` from its brief in JAUNTS-INITIAL-LIBRARY.md. Reuse current source/structure/business/resident records and the shared engine.

**Depends on:** T-1259, T-1256, T-1257, T-1258

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Deliver opening, 4 purposeful stops (adjust only with a stated narrative reason), concise actions, supported card links, recommendation and endings in JSON; the catalog card launches it.
2. Orient from the west side; read the fork from the tavern; choose the supported crossing; arrive on the south side with a simple route note. Focus on place and everyday movement, with no forced money or drama.
3. Verify each proposed stop against the compiled scene and trace each factual claim to source ID plus locator; retain inference/reconstruction notes and append narrative liberties. Route over the current bridge graph, never straight across water. Describe disputed bridge/tavern details at their recorded tier.
4. Award Knows the Crossing in Wayfinding without forcing extra scoring. Test every authored choice/outcome and no dead ends or double rewards.
5. Time the primary path in the recommended mode walk aiming at 4-6 minutes (a justified 3-4-minute outing is fine); compare Fly/Instantly and confirm deeper cards are optional.
6. Show mobile/desktop menu-to-ending evidence, Previous/Next, mid-leg mode switch and End-to-menu. No new engine branch keyed to this jaunt.

**Touch points:** data/jaunts/across-wolf-point.json, corresponding brief/dossier and generated catalog; existing cards, not new geometry.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
