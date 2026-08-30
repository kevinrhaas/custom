---
id: T-0431
title: Open blk_south_water_clark: 4 roofs of headroom on 2 free lots
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: T-0420
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

Open `blk_south_water_clark`: 4 roofs of headroom on 2 free lots.

Piece 3 of 4 of **T-0420 — Open the four South Water blocks T-0009 has
unblocked: 20 roofs of headroom on franklin, lasalle, clark and dearborn**, split on
2026-08-29 by T-0365 because the parent held four demonstrations and said so itself —
*"Take ONE block per run — T-0028's programme rule is one run, one demonstration, one
successor, and four blocks is four runs."* The parent keeps the full ask and its links.

## Why this ground is workable now, and was not before

T-0365 measured that the anonymous-block programme had no unblocked ground left: every
platted block still carrying headroom was gated on T-0009 or on T-0183, both `blocked-owner`.
**T-0009 closed on 2026-08-29 under the owner's ruling** (PR #567), and the load-bearing half
of it for this ticket is one sentence — *"It does not license moving the drawn centreline back
onto the control. The street is drawn where it is for a stated reason and stays there."*

That discharges the refusal T-0143 and T-0188 each made and T-0317 inherited: neither would
tighten a party-line row **against a line that may move**, because a run stands ON the face,
so a face that moves moves the whole row and the metres would be re-derived rather than
corrected. The line has now been ruled not to move.

`blk_south_water_market` is NOT in this ticket or its siblings. It stays gated on T-0183,
which PR #573 measured as a wedge the South Branch pinches out — 2.8 m of depth at Market
against the 24.384 m one platted lot fronts — and which is back with the owner.

## The measurement this piece was sized on

`tools/reconcile_665.py` on an unmodified `dev` at `6a88b421`, 2026-08-29:

| block | state | headroom | free lots |
|---|---|---|---|
| `blk_south_water_lasalle` | open | 8 | 3 |
| `blk_south_water_franklin` | open | 4 | 2 |
| `blk_south_water_clark` | open | 4 | 2 |
| `blk_south_water_dearborn` | open | 4 | 2 |

`coverage.schedulable_on_committed_ground` reads **20**, which is these four blocks exactly.
Every other platted block in the schedule is `at_capacity`, `blk_south_water_clinton` is
`not_a_block` (T-0163), and the four remaining `gated` rows are un-surveyed divisions, not
lots. **One block is one run** — 4 roofs plus the bake that deals them is a full run's
demonstration, which is why `effort: M` and `needs_bake: true`.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- `blk_south_water_clark` deals its 4 roofs against its own committed lots — no lot outside the
  block, and no roof on a lot another record already holds.
- Every row stands ON the block face, not on a re-derived line. That is the whole point of
  waiting for T-0009's ruling, and a row measured against anything else fails this clause.
- The roofs are BAKED in the same commit as the records (`./tools/bake.sh --only <id>` per
  structure). `validate.py --stale` hard-fails a record that has stopped matching its mesh,
  so a data-only PR here cannot merge and should not be attempted.
- `tools/reconcile_665.py --check` reconciles: the census moves 4 roofs from this block's
  headroom into `standing`, and `coverage.schedulable_on_committed_ground` falls from its
  value at the start of the run to that value minus 4.
- Every new record carries its confidence honestly. These are anonymous reconstructed roofs,
  not documented buildings: `reconstructed`, with the note saying what the reasoning was.
- A screenshot from the same spot shows roofs that were not there.
- `./tools/check.sh` and `node tools/smoke_renderer.mjs` are green, and the run publishes
  (`./tools/publish.sh`) in the same commit.

**Links:** T-0420 (the parent) · T-0365 (the run that split it) · T-0009 · T-0028 · T-0143 ·
T-0188 · T-0317 · T-0183 · T-0163 · `tools/reconcile_665.py` · `tools/measure_block_gating.py`.
