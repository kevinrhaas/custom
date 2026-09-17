---
id: T-1276
title: Move city statistics into a browsable Sources and City summary
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

Expand the existing Evidence surface into shallow Sources and City Summary views. Remove building/household completeness numbers and percentages from loading and welcome.

**Depends on:** T-1248

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Reuse census.js and existing census/coverage inputs, keeping definitions, denominators, confidence vocabulary and build date; no new hand-maintained counts.
2. Search source title/author, filter by type/date/tier/use, group newspaper publication and issues, and paginate or window long lists. Default to used-in-scene; expose all registered sources separately.
3. Source details show supplies/limits, original/archive availability and used-for links to specific cards or decision summaries, including claim confidence/locator.
4. Show per-source unique entities versus claims, and clearly explain overlapping confidence buckets; distinguish source tier from claim confidence.
5. Preserve [DOC]/[INF]/[CONJ] display compatibility while using attested/inferred/reconstructed storage. Keep all existing Evidence content reachable.
6. At mobile/desktop, opening a used-for card and returning restores search/filter/scroll; missing optional data leaves exploration usable and no false zero counts. Adapt old gate-census assertions to the new location.

**Touch points:** js/census.js, js/citations.js, js/hud.js, js/sources.js, index.html, css/evidence.css, smoke parts for gate/drawer.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
