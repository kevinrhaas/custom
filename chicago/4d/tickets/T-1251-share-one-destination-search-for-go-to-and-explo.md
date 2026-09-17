---
id: T-1251
title: Share one destination search for Go to and Explore Myself
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

Extract the existing Go to target/filter model so the welcome start picker and in-world navigation use one dataset and one resolver.

**Depends on:** None within this feature; consume current dev records.

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Reuse anchors, structures, historical streets/intersections, located residents and dated located businesses. Business support consumes the existing business layer; do not author a competing register.
2. Keep current diacritic/name search, keyboard selection, kind filters, reconstructed visibility preference and distance/unit behavior.
3. Unlocated residents/businesses open their information with a stated location limit; they do not acquire guessed coordinates. Ambiguous names show enough place context to choose.
4. Choosing I’ll Explore Myself — Starting At… resolves a safe initial stand-off and enters ordinary exploration with no jaunt state, rewards or overlay.
5. In-world Go to retains travel preferences and framing; initial spawn selection is immediate. Both entry points call the same resolver and avoid duplicate menu inventories.
6. Test a structure, business, resident place, anchor and intersection; unknown/excluded targets; keyboard and touch; repeated selections and dismissal without movement.

**Touch points:** js/goto.js, js/hud.js, main.js goToTarget/framing, proposed js/destinations.js.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
