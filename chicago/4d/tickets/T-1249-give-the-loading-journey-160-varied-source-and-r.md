---
id: T-1249
title: Give the loading journey 160 varied source and reconstruction statuses
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

Author a phase-aware loading library with source flips, entity-building messages, periodic sourced facts and very occasional humor. It must feel like assembling the reconstruction without misrepresenting live research.

**Depends on:** T-1247, T-1248

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Ship about 160 distinct entries (100-250 accepted): assess/collect/reconstruct/settle phases, including newspapers, maps, stores, fort, river and prairie; at least 50 entity-specific observations or supported facts.
2. Each fact resolves source IDs and locators, retains its confidence and reasoning, and stays paired with its source on one card. Retrospective accounts show their dates; invented operational copy is never marked DOC. Register the fact links in the shared source-use index.
3. Seedable weighted shuffle bags vary sessions without immediate repeats or phase-inappropriate endings. Normal dwell 2-4 s; a fast boot may display just one or two.
4. Humor is capped at one line in 1% of sessions, never on error/arrival; include Reticulating splines as an uncited joke. Test the session cap deterministically.
5. Provide a compact early subset; loading messages never wait on the full source library. Show correct final status at 1835 and stop all rotation on exit/error.
6. Check nonexistent sources, duplicate substantive facts, inaccessible locators, unsafe markup, and long text on a phone; preserve the existing boot payload budget.

**Touch points:** proposed data/loading/*.json, js/loading-content.js, source-use index, arrival.js, focused content validator.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
