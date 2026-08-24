---
id: T-0190
title: The South Water placements stand out past the committed plat, and the walk breaks on them
state: claimed
epic: TOWN
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-0127
opened: 2026-08-24
closed: null
pr: null
claimed_by: run 8/24/2026, 11:26:34 AM CT
blocked_on: null
needs_bake: false
---

The South Water placements stand out past the committed plat, and the walk breaks on them.

Piece 1 of 5 of **T-0127 — The rest of the town gets the street edge**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

Ten documented buildings on the south side of South Water Street were placed against the
MODERN kerb, read off OpenStreetMap, rather than against this project's own committed plat,
and stand up to 6.9 m out past the platted lot line — inside the 80 ft corridor, nearly to
the travelled track. `tools/measure_corridor_intrusion.py` names them and measures the depth:
`h_jones_store` 8.17, `chicago_american_office` 6.91, `jh_kinzie_forwarding_store` 6.87,
`carpenter_south_water_store` 6.62, `frederick_thomas_shop` 6.25, `madore_beaubien_house`
5.98, `pruyne_kimball_drugstore` 5.55, `harmon_loomis_store` 5.31, `chicago_democrat_office`
5.11, `peck_store` 4.51.

That is why T-0069's walk on South Water comes out in pieces — 15.6 m and 20.8 m runs of a
97 m face — while Lake Street's runs whole: the march refuses every step a wall stands on,
and on this street the walls stand on the walk.

**What the sources actually fix, and what they do not.** Every one of these records cites a
street and a landmark — "on Water Street, near the draw-bridge", "at Clark", "on South Water"
— so the ALONG-STREET position is argued from a source and is not this ticket's business.
The SETBACK is not in any source: it came from `osm_streets_2026`, a 2026 kerb line, and this
project's answer to "where is the lot line" is its own committed plat
(`data/traces/vectors/thompson_lots.json`, re-derived by `tools/generate_plat_lots.py`).
Reconciling the setback with the plat is therefore not moving a building to make a number
smaller — the number it is measured against is the one the record should have used.

**Acceptance:** each of the ten either stands with its street-facing wall at or behind the
committed South Water frontage line — moved along the street's own normal only, its
along-street coordinate untouched, with the derivation and the metres recorded in its
`position.note` — or is refused in writing, per store; `measure_corridor_intrusion.py`
reports none of the ten lapping South Water's corridor and its baseline is rewritten to
record the repair; `tools/generate_frontage_works.py` re-derives and South Water's walk runs
unbroken along each face except where its own ground refuses it; `tools/check.sh` and
`tools/smoke_renderer.mjs` pass. Never by weakening a gate.

**Not in this ticket:** more streets (T-0191, T-0192, T-0193), hitching posts (T-0194), and
the shadow lever T-0115's ledger names — that is T-0192's to spend, since it is the piece
whose metres need it.
