---
id: T-1272
title: Verify arrival, jaunts and source browsing on the published mobile app
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

Run the integrated published experience from a cold boot through another jaunt or free exploration. Fix concrete integration failures within this slice and finish the section.

**Depends on:** T-1271, T-1249, T-1250, T-1252, T-1259

**Execution contract:** [architecture](../docs/ARRIVAL-JAUNTS-ARCHITECTURE.md), [ordered plan](../docs/ARRIVAL-JAUNTS-EXECUTION.md), [content briefs](../docs/JAUNTS-INITIAL-LIBRARY.md). Read these before claiming.

**Acceptance:**

1. Published 390x780 and 1280x800 paths: ticker/source cards -> summer 1835 welcome -> jaunt -> detail/source -> change travel -> finish/End -> second jaunt -> Explore Myself, zero page errors.
2. Verify warm/slow/failed boot, no premature 1835, reduced motion, no artificial wait, stale timing history, background/resume and optional source/jaunt request failure.
3. Check 320 px width, short landscape, keyboard/safe areas, focus order/restoration, >=44 px touch targets and persistent navigation without overlay collision. Menu entry does not take pointer lock.
4. Source search/backlinks and City Summary retain accurate counts after the 25 jaunts add their citations; all legacy Evidence cards, Go to, travel settings and framing remain usable.
5. Measure boot payload/frame impact against existing budgets; catalog/history detail stays lazy. T-1156 still owns CI wiring; do not duplicate that ticket or silently raise budgets.
6. Run check.sh, preflight and the appropriate published renderer smoke, record evidence and merge green to dev. Do not promote main. No unfinished requirement may be relabeled completed; unavoidable successors stay inside this band.

**Touch points:** published runtime, smoke_renderer.mjs focused coverage, acceptance report; only fixes justified by observed failures.

**Finish:** one gated PR into `dev`, focused checks plus affected published desktop/mobile smoke; no production promotion. Claim through `ticket.mjs`. Meet this acceptance before closing. If an unforeseen piece truly needs a successor, place it beside this dependency inside the same subsection, update the plan, and keep the subsection below 15 tickets. Do not append unfinished work to the queue tail.
