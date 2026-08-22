---
id: T-0139
title: The bake cannot reach cook_county_courthouse_1835, so any common/ edit leaves it stale
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-22
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The bake cannot reach `cook_county_courthouse_1835`, so any `common/` edit leaves it stale.

`generators/build.py` resolves a structure's phase against the SCENE's target date and skips the
record when no phase covers it. The courthouse's only phase (`wood_1835`) runs 1835-10-01 to
1835-12-31; the only scene in `data/scenes/` targets 1835-07-01. So `build.py --only
cook_county_courthouse_1835` prints *"skip: no phase covers 1835-07-01"* and builds nothing — while
`cook_county_courthouse_1835__wood_1835.glb` is committed, is in `assets/manifest.json`, and IS
hashed by the staleness gate like every other asset.

The consequence is a trap rather than a defect anybody has hit twice: every edit to
`generators/common/` restales that asset along with the rest of the town, and the bake that heals
the rest cannot heal it. T-0008 got past it with a throwaway script that monkey-patched
`resolve_phase` — which is exactly the shape of thing that should not be needed twice.

**Acceptance:** the bake can rebuild every asset the staleness gate holds it responsible for, by a
committed route — either the scene grows an out-of-date-range build list, or `build.py` takes an
explicit phase, or the asset stops being committed because nothing loads it (`compile_scene`
already reports it as *"1 excluded by date"*). Whichever is chosen, `tools/check.sh` stays green on
a clean tree after a `common/` edit.

**Links:** T-0008 (the run that hit it) · `generators/build.py::main` · `generators/mesh_inputs.py`
· `tools/validate.py::run_stale_check`.
