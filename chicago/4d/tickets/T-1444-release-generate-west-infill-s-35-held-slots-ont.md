---
id: T-1444
title: Release generate_west_infill's 35 held slots onto the extended ground: the terrain gate retired, the placements instantiated and baked
state: claimed
epic: GROUND
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1431
opened: 2026-09-20
closed: null
pr: null
claimed_by: run 9/20/2026, 2:15:04 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35531496699
---

Release generate_west_infill's 35 held slots onto the extended ground: the terrain gate retired, the placements instantiated and baked.

Piece 2 of 2 of **T-1431 — Carry the West Division's five tier lines off their E -320 clip and release generate_west_infill's 35 held slots on the extended ground**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

All 55 West Division placements instantiate. `generate_west_infill.py --check` re-derives
every one of the 55 records byte for byte, the 20 built under the hold are unchanged, and
`tools/validate.py --all` reports 0 errors with no stale mesh — the 35 new GLBs are baked
from the committed records by `generators/build.py` and their input hashes recorded in
`assets/manifest.json`.

**The swale reading the recipe deferred** was taken and filed as its own ticket (T-1460):
both conjectural west-prairie drains begin in open ground at the old E -320 wall, and
swale_a's corridor covers eight roofs that were reviewed while the rule was deferred. The
generator refuses a ninth rather than moving seven reviewed houses to suit an invented line.

**What this run had to undo.** The branch carried a convenience change to
`generators/build.py` (`--only` accepting a comma-separated list). `mesh_inputs._code_shas`
hashes `build.py` into every structure's input hash, so that one edit staled 382 of the 419
committed meshes — `tools/validate.py --all` is clean on `dev` and reported all 382 here.
`build.py` is restored to its committed bytes and the 35 new meshes re-baked against it; a
multi-id `--only` is a real convenience and belongs in its own ticket with the town-wide
re-bake it costs, not folded into a release.
