---
id: T-1253
title: Define validated jaunt JSON and render a real pilot preview
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

Establish a compact declarative jaunt schema and lazy catalog, with a New in Chicago pilot preview in the welcome. The engine ticket turns the same pilot into a playable path; the priority content ticket finishes its authored narrative.

**Depends on:** T-1248, T-1277, T-1278

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Define identity/version/scene, premise/category, opening, typed stop destinations, 25-60-word primary text, choices, conditions/effects, resources, endings, card links, mode defaults and timing inputs as in the architecture.
2. Canonical confidence values preserve DOC/INF/CONJ aliases. Source claims carry locators, inference reasoning and reconstruction liberties separately from invented connective text. Register these claims with T-1248’s source-use index so Sources can link back to jaunt facts.
3. Semantic validator refuses duplicate/dangling IDs, excluded dates, missing citations, unbounded effects, unreachable endings and unsupported operators; no eval or raw HTML.
4. Compile only summary fields for the menu and load stop content on selection. Show a source-linked pilot preview with real resolved destinations and clearly labeled availability.
5. Add an authoring example and an additional fixture jaunt solely by JSON plus catalog regeneration, with no application switch/case keyed to its ID.
6. Reject reviewed/held content from release while retaining an explanatory unavailable card; one malformed file cannot crash the whole menu.

**Touch points:** proposed data/jaunts/schema.json, pilot JSON, tools/compile_jaunts.py/check_jaunts.py, js/jaunt-menu.js, publish rules.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
