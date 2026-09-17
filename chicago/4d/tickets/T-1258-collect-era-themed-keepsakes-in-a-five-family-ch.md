---
id: T-1258
title: Collect era-themed keepsakes in a five-family Chicago daybook
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

Provide optional collection progress across different kinds of jaunts. Draw on low-pressure everyday collection and waypoint-story patterns in the architecture, with era-themed rewards rather than generic XP.

**Depends on:** T-1256, T-1257

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Implement Provisions, Livelihood, Wayfinding, News & Knowledge, and Neighbors; one primary and at most one secondary family per jaunt. Plain outings can leave a simple memento.
2. Data-defined ranks New Arrival / Finding Your Feet / Knows the Town / Seasoned Chicagoan reward distinct completions across all families; initial thresholds are 1/2/3 unique keepsakes per family.
3. Receipts, work chits, clippings and calling cards are labeled fictional narrative keepsakes, not newly discovered evidence. No source attribution invented for a reward.
4. Revisits, duplicate completion events and replay farming cannot inflate ranks. Separate local per-jaunt variables from persistent collection state.
5. Save schema/content versions, recover corrupt/incompatible saves, work without storage, and expose reset. Returning/new visitors can play all jaunts regardless of rank.
6. Render a compact daybook and outcome receipt on mobile; no streaks, timed pressure or leaderboard. Verify balanced progression with fixtures covering all five families.

**Touch points:** proposed js/jaunt-journal.js, journal/rank content JSON, jaunt menu/outcome, local persistence helpers.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
