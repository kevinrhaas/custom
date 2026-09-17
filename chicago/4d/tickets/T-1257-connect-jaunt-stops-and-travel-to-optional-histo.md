---
id: T-1257
title: Connect jaunt stops and travel to optional historical context
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

Keep the primary story concise while linking every stop to existing building, resident, business and source information. Add light optional context between stops.

**Depends on:** T-1254, T-1255, T-1250

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Typed links open existing cards without copying biographies or source records; return restores the exact stop, choice state and scroll/focus.
2. Opening a detail pauses auto travel and any primary-path timer; closing offers continue from the same position. Reading never changes resources or earns mandatory completion credit.
3. Route-aware inter-stop snippets are one or two sentences, nonblocking and available later; a quick flight/instant hop never waits for narration to finish.
4. Historical statements retain claim-level DOC/INF/CONJ equivalents and citations; invented gossip/bridging dialogue is expressly narrative and not attributed as a real quotation.
5. A missing optional card has a useful unavailable state; source errors cannot end the jaunt. Avoid overlapping drawer, popup, stop panel and controls at both viewports.
6. Test detours to person/source/building cards, repeated back navigation, dismissing transit text and exiting during a detail request.

**Touch points:** js/popup.js, people.js, citations.js, hud.js and jaunt panel/adapter; route context content hooks.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
