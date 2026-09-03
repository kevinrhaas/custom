---
id: T-0454
title: The gate calls a GLB stale and the bake declines to rebuild it, so a stale asset cannot be cleared by baking
state: open
epic: PIPELINE
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-08-31
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Found while merging **PR #597** on 2026-08-31. Two committed tools disagree about
whether an asset needs rebuilding, and while they disagree the PR cannot be
landed by any route.

## What happened, in order

1. `tools/check.sh` on `steward/t-0429-south-water-lasalle` at `d9a04091` failed
   with exactly two errors, both staleness:

   ```
   FAIL  stale: recon_1835_blk_south_water_lasalle_d4_02__inferred_1835.glb
         its inputs now hash to 032beb895e2a, the committed mesh was built from 7a9cfe9694f3
   FAIL  stale: recon_1835_blk_south_water_lasalle_d5_01__inferred_1835.glb
   ```

2. `chicago-4d-bake.yml` was dispatched against that same branch and same commit.
   The `bake` job **succeeded in 12 m 34 s**, ran Blender, and reported
   `360x transformed — gltf-transform meshopt derivative built by bake.sh`.

3. It then reported:

   ```
   bake produced no CONTENT — only its own build stamp moved. No branch, no PR:
   the PR is the signal that a bake rebuilt something, and nothing was rebuilt.
   ```

**The gate names two assets as stale and the bake, run on the same tree, rebuilds
neither.** Both cannot be right, and there is no third tool to break the tie.

## What is known about the cause

The staleness hash is `structure_inputs_sha` from `generators/mesh_inputs.py`,
over `{scheme, structure, phase, archetype, params, code, blender_pin}`. `params`
comes from `resolve_params(...)`, and the difference in this case was real:
`siding_exposure_m` was **0.152** on `dev` and **0.127** on the branch, which is
a form parameter and therefore a mesh input.

So the gate was right that the mesh no longer matches its record. What is not
established is why `generators/build.py` did not rebuild it — whether it compares
against `assets/manifest.json` rather than recomputing, whether a merged manifest
left a hash that made the asset look current, or something else. **That is the
first thing to find out, and this ticket does not guess it.**

## Why it matters beyond one PR

Any merge that changes a mesh parameter — a form value, an archetype, a generator
module — produces exactly this state. The gate blocks the PR, and the documented
remedy the gate itself prints (*"Re-bake it (tools/bake.sh, or the
chicago-4d-bake workflow)"*) does not clear it. The remedy named in the error
message has to work.

**Acceptance:**

1. The disagreement is reproduced deliberately — change one mesh parameter on a
   branch, run the gate, run the bake — and the reason the bake skips is
   demonstrated rather than argued.
2. Whichever is wrong is fixed so that the sentence the gate prints is true: a
   stale asset is cleared by running the bake the error message names.
3. A test asserts it, so the two cannot drift apart again silently. This is the
   same class of fault as the stale-mirror and stale-board checks (T-0154,
   T-0155): two copies of one fact that can disagree.
4. ~~**PR #597 is re-read against the result.**~~ **Overtaken — see below.** #597
   merged on 2026-08-31 without this ticket. Nothing here depends on it any more.

## What has happened since, 2026-09-03

**PR #597 is no longer the reason to do this, and the ticket stands without it.**
It merged on 2026-08-31 as `bcb4d12d`, by the route its own commit message states:
*"Resolved by re-deriving each ledger the gate named, one failing step at a time:
generate_block_infill, deal_siding_stock, reconcile_665, town_census, compile_scene.
The two stale GLBs cleared themselves once the block records were re-derived from
their own recipe."* That moved the DATA until the gate agreed with the committed
mesh. It is a way round the fault, not a fix for it, and it leaves acceptance 1-3
exactly where they were: the tie between the two tools was never broken, no line of
`build.py`, `bake.sh`, `check.sh` or `mesh_inputs.py` has changed on account of it,
and no test asserts the two agree. `git grep T-0454` reaches the ticket files and
nothing else.

The staleness gate is GREEN on dev today (`tools/validate.py --stale`, 0 errors),
so nothing is blocked at this moment. That is the state the fault is invisible in.
It reappears on the next merge that moves a mesh parameter, which is what the
paragraph above this acceptance list says and is why the ticket outlives the PR
it was filed from.

**One lead, ruled out, so the next run need not spend its slice on it.** The
obvious candidate was that `build.py` never reaches the asset at all — it iterates
`data/structures/*.json` and skips on `resolve_phase` finding no phase for the
scene date, on `drawn_by_another_layer`, and on an archetype absent from
`ARCHETYPES`, and any asset behind one of those skips would be named stale by
`validate.py` (which iterates the MANIFEST instead) and never rebuilt. Audited both
trees: on dev's head, all 366 structure assets in `assets/manifest.json` are
reachable by `build.py`, and on `d9a04091` — the exact tree the bake ran on and
rebuilt nothing — all 366 were reachable there too, the two named GLBs among them.
So `build.py` would have rebuilt them and written the recomputed hash into the
manifest, and that is not what happened. The cause is somewhere between
`tools/bake.sh`, the workflow's checkout, and `bake_content_changed.py`'s verdict.
Acceptance 1 still stands: demonstrate it, do not argue it.
