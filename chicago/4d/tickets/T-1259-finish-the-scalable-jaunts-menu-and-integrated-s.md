---
id: T-1259
title: Finish the scalable Jaunts Menu and integrated start experience
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

Complete the welcome’s Jaunts Menu as a content-driven library that stays quick to browse at 25 and 50+ jaunts, alongside the shared Explore Myself option.

**Depends on:** T-1279, T-1280, T-1258, T-1278

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Each card shows title, one-sentence premise, stop count, category, selected-mode approximate quick-play duration and editable recommended travel mode.
2. Offer category/search and a small priority selection; all six priority titles retain prominence as they land. Only available content can start; preview/unavailable cards explain why.
3. Keep I’ll Explore Myself — Starting At… prominent and reuse the shared picker; no competing Go to search or jaunt session after free-start selection.
4. End/completion return immediately to this menu with focus/filter retained; Resume/Restart semantics are clear for a paused jaunt, and a different selection cancels it cleanly.
5. Lazy-load selected content and paginate/window as necessary; a 55-item test manifest requires no UI code change, excessive boot downloads or clipped controls.
6. Verify keyboard, touch, short screens, source links and non-jaunt entry; warm welcome contains no coverage dashboard.

**Touch points:** js/jaunt-menu.js, index.html/welcome, hud.js, responsive jaunt CSS and lightweight catalog.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
