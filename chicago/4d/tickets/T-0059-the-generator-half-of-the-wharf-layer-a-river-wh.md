---
id: T-0059
title: The generator half of the wharf layer: a river-wharf mode of pier_crib
state: open
epic: TOWN
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

The generator half of the wharf layer: a river-wharf mode of `pier_crib`.

Filed by the run that shipped **T-0041**. `docs/ROADMAP.md` K5 (e) asked for the docks and said
they "need a river-wharf mode of `pier_crib`". That turned out to be a BAKE reason rather than a
blocker — the renderer-side half needs no Blender and is shipped — but the generator half is still
owed and is what a BAKED town would carry: `generators/archetypes/pier_crib.py` builds the harbour
piers, and nothing builds a river wharf, so a scene assembled from GLBs alone has no docks in it.

The outline is already derived and committed (`data/wharves/river_landings.json`), so this is the
archetype and its params, reading that record rather than inventing a second set of numbers.

**NEEDS THE BAKE** — Blender, so the improve runner cannot close it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
