---
id: T-1267
title: Publish land, freight, household supplies and clothing jaunts
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

Author only this bounded content batch: `inspect-a-lot`, `freight-for-the-store`, `household-provisions`, `a-decent-coat`. Each is a separate short jaunt, not stops in one long tour. The full briefs define their distinct premises.

**Depends on:** T-1259, T-1256, T-1257, T-1258

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Complete 4 JSON jaunts with openings, 4-8 purposeful stops normally, concise actions, optional appropriate mechanics, outcomes/keepsakes, categories, travel defaults and live duration inputs.
2. Use the corresponding routes/evidence cautions in JAUNTS-INITIAL-LIBRARY.md; resolve every factual claim and entity/date against current dev. Substitute supported destinations with reasons rather than inventing missing venues.
3. At least one outing in the batch remains low-pressure with no forced branching. Keep goods, dialogue, prices, rewards and errands at their honest narrative tier.
4. Run the content validator and all authored paths; verify a sample of each distinct mechanic visually, with no custom engine code or shared compiler refactor.
5. Record a recommended-mode primary duration for each (normally 4-6 minutes), compare a faster mode, and confirm optional deep links return to the same stop.
6. All 4 menu cards start, finish/End returns to menu, and mobile content fits. Completion requires the whole batch; split inside this band only if a real unforeseen blocker remains.

**Touch points:** data/jaunts/inspect-a-lot.json, data/jaunts/freight-for-the-store.json, data/jaunts/household-provisions.json, data/jaunts/a-decent-coat.json; associated content evidence/locators and generated outputs.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
