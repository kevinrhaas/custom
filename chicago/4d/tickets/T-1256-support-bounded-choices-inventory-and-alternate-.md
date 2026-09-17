---
id: T-1256
title: Support bounded choices, inventory and alternate jaunt endings
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

Add optional data-driven mechanics without forcing them onto a simple walk: money, inventory, story time, reputation, information, health, sobriety, cargo and readiness only when the content declares them.

**Depends on:** T-1279

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Whitelist typed conditions/effects, variable bounds and inventory IDs; no executable code in JSON. Integers represent cents; fictional prices carry reconstructed bounds/notes.
2. Commit actions exactly once. Previous then Next cannot duplicate a purchase or reward. Revise choice truncates downstream events and deterministically rebuilds state/branch.
3. Every reachable decision has a viable choice/default/skip and an ending. Test insufficient money, full cargo, missing inventory, alternate endings and repeated rapid taps.
4. Optional resources are hidden when unused. Deeper reading and real-world delays do not drain resources or advance story time.
5. Demonstrate one shopping fixture, one branching tavern fixture and a plain outing using the same engine; explain consequences in short visitor language.
6. Persist only version-compatible state with safe fallback for blocked/corrupt storage; no account or shared competitive score.

**Touch points:** jaunt schema/validator, js/jaunts.js reducer, jaunt-panel.js; small mechanics fixtures.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
