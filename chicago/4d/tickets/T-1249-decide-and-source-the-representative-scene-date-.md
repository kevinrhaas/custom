---
id: T-1249
title: Decide and source the representative scene date of the 1880s South Side epoch, and make the checker read every dated shoreline state's date from the record that argues for it
state: done
epic: SOUTH_TIME
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0473
opened: 2026-09-17
closed: 2026-09-17
pr: 1401
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: 2026-09-17T16:08:20.678Z
claimed_run: null
---

Decide and source the representative scene date of the 1880s South Side epoch, and make the checker read every dated shoreline state's date from the record that argues for it.

Piece 1 of 4 of **T-0473 — Create an 1880s South Side terrain and urban-ground epoch**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. A specific representative scene date in the 1880s is chosen and ARGUED — the candidates
   considered, the evidence for each, and the reason the chosen one beats them — in a research
   doc, and carried in `data/terrain/shoreline_states.json` on `shore_1880s_ic_edge` where a
   reader meets it beside the state it dates.
2. Every source the argument leans on is a source RECORD, read at its URL, graded at the rung
   the page actually sits on, and honest about what it cannot supply. No confidence is upgraded
   and no citation is invented.
3. `tools/check_shoreline_states.py` stops carrying a probe date of its own: it resolves each
   epoch through the date its state declares, requires `address_date` of every dated state, and
   refuses a date outside that state's declared range — each assertion proved by a self-test
   that breaks it.
4. No geometry is written and none is implied: `shore_1880s_ic_edge.geometry` stays `null` and
   `e1871_postfire` stays `planned`. The successor tickets own the ground.
5. `tools/check.sh` green.

