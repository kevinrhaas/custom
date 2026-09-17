---
id: T-1252
title: Generate the 1880s terrain spec, heightfield and extent a Prairie Avenue scene stands on, and turn the epoch active
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
needs_bake: true
closed_at: null
claimed_run: null
---

Generate the 1880s terrain spec, heightfield and extent a Prairie Avenue scene stands on, and turn the epoch active.

Piece 4 of 4 of **T-0473 — Create an 1880s South Side terrain and urban-ground epoch**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. `generators/terrain_gen.py` (or its successor) produces an `e1871_postfire` heightfield,
   ground and water GLBs from the T-1251 spec and the T-1250 lines, over an extent that covers
   the Prairie Avenue district blocks named by `wikipedia_prairie_avenue_district`.
2. The epoch's `layers` and `layer_status` are filled in the pattern `e1834_harbor_cut` sets,
   the extent is stated, and outside it the renderer says it has no data rather than inventing
   ground.
3. `status` moves from `planned` to `active` and an 1880s scene selects it — a terrain epoch
   distinct from both e1830_natural and e1834_harbor_cut, which is T-0473's own first
   acceptance clause.
4. BAKED in the same commit as the records that move (`./tools/bake.sh`), published with
   `./tools/publish.sh`, and `validate.py --stale` green. `tools/check.sh` green and the
   `--for-diff` smoke legs run.

