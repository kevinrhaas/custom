---
id: T-1261
title: Publish Taverns of Chicago as a five-minute jaunt
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

Author the complete priority jaunt `taverns-of-chicago` from its brief in JAUNTS-INITIAL-LIBRARY.md. Reuse current source/structure/business/resident records and the shared engine.

**Depends on:** T-1259, T-1256, T-1257, T-1258

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Deliver opening, 4 purposeful stops (adjust only with a stated narrative reason), concise actions, supported card links, recommendation and endings in JSON; the catalog card launches it.
2. Choose a modest purse; hear a short piece of clearly fictional gossip bounded by the papers; compare welcome and lodging; pick a final house. Money and optional sobriety alter a restrained ending; abstaining is equally playable.
3. Verify each proposed stop against the compiled scene and trace each factual claim to source ID plus locator; retain inference/reconstruction notes and append narrative liberties. Do not put reconstructed dialogue in a named historical person’s mouth as quotation; site presence and business tenure retain their own grades.
4. Award A Sensible Evening in Neighbors without forcing extra scoring. Test every authored choice/outcome and no dead ends or double rewards.
5. Time the primary path in the recommended mode horse aiming at 4-6 minutes (a justified 3-4-minute outing is fine); compare Fly/Instantly and confirm deeper cards are optional.
6. Show mobile/desktop menu-to-ending evidence, Previous/Next, mid-leg mode switch and End-to-menu. No new engine branch keyed to this jaunt.

**Touch points:** data/jaunts/taverns-of-chicago.json, corresponding brief/dossier and generated catalog; existing cards, not new geometry.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
