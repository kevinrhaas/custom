---
id: T-1248
title: Compile the sources used and their reconstruction backlinks
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

Build a compact public source catalog and typed source-to-claim-to-entity index from existing compiler inputs. Give the existing Evidence surface a basic source/used-for view in this slice.

**Depends on:** None within this feature; consume current dev records.

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Reuse compile_scene.py cite() and its public/internal-field partition; include registered sources with explicit used-in-scene, other-scene, exclusion/research-only or unused status.
2. Edges name entity type/ID, field or claim, confidence and locator. Cover structures, people, businesses when available, terrain, flora/fauna, exclusions and decision summaries; preserve a coverage report for any unsupported input family.
3. Show a basic searchable source list and a real used-for backlink on the existing Evidence surface, so the output is inspectable before the later browser refinement.
4. Deduplicate entity counts separately from attribute claims; validate dangling IDs, alias/citation joins and mixed-tier entities. A registered source alone is not a used-in-scene edge.
5. Publish compact manifest and lazy per-source detail through resolveBases; no raw research corpus, PDFs, private/internal fields or unlicensed derived imagery enters boot. Use fixture and deterministic generation checks.

**Touch points:** tools/compile_scene.py, tools/publish.sh, data/sources/, data/sidecars/1835/, proposed source-use compiler and js/sources.js.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
