---
id: T-1250
title: Trace the 1880s lake edge and Illinois Central corridor from period cartography, south past Twelfth Street to the Prairie Avenue blocks, with its sources, confidence and bounds
state: open
epic: SOUTH_TIME
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: T-0473
opened: 2026-09-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Trace the 1880s lake edge and Illinois Central corridor from period cartography, south past Twelfth Street to the Prairie Avenue blocks, with its sources, confidence and bounds.

Piece 2 of 4 of **T-0473 — Create an 1880s South Side terrain and urban-ground epoch**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. A traced 1880s lake edge and Illinois Central corridor for the scene date T-1249 fixed,
   from period cartography — fire-insurance and lakefront survey mapping — reaching south past
   Twelfth Street to the Prairie Avenue blocks, committed as geojson under
   `data/terrain/epochs/e1871_postfire/` and named by `shore_1880s_ic_edge.geometry`.
2. Every line carries its source record, its observed date, its role (primary where drawn, or a
   bound) and its confidence. Where independent readings differ, the full spread is a named
   disagreement band, not an adopted midpoint — the 1835 state is the pattern.
3. The reading that this project currently holds is DOWNTOWN ONLY (Lake Park, between Randolph
   and present Roosevelt Road) and says nothing about the water off 18th Street. This ticket may
   not stretch it; it must fetch cartography that reaches Prairie Avenue or state plainly that it
   could not and what it did instead.
4. `tools/check_shoreline_states.py` accepts the state as active geometry and its self-tests
   still fire. `tools/check.sh` green.

