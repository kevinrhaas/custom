---
id: T-1252
title: Land on a warm mobile welcome with Jaunts and Explore Myself
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

On real readiness, land on the start surface: Welcome to Chicago, summer 1835, a one-sentence digital-reconstruction explanation, and Jaunts / I’ll Explore Myself — Starting At…. Wire a clearly labeled empty state until the jaunt catalog lands.

**Depends on:** T-1247, T-1250, T-1251

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Keep target_date 1835-07-01. The owner approved summer wording; do not migrate scene dates or claim an August arrival.
2. Replace Tap to walk everywhere with Tap to enter or Enter Chicago where an entry gesture remains; start/search/jaunt selection can supply that gesture.
3. No pointer lock on menu entry, typing or card navigation. Retain gesture-bound audio unlock; request movement controls only after selecting an experience and entering the world.
4. No reconstruction totals/percentages on loader or welcome; Sources & City remains one clear link away. First-run help must not cover the welcome choices.
5. One Start/Jaunts Menu route reopens this surface from the world; no duplicate Go to interface. Free-exploration selection works before any jaunt exists.
6. Check small screens, landscape, on-screen keyboard, focus restoration, saved settings and touch help. Visitor can load, choose a destination and explore without a stuck overlay.

**Touch points:** index.html, main.js openWorld/gate events, hud.js, walk.css/drawer.css, shared picker.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
