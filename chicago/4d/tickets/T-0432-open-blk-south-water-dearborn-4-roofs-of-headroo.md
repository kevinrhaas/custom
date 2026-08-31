---
id: T-0432
title: Open blk_south_water_dearborn: 4 roofs of headroom on two free lots
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0420
opened: 2026-08-29
closed: null
pr: null
claimed_by: run 8/30/2026, 1:51:44 AM CT
blocked_on: null
needs_bake: true
---

Open `blk_south_water_dearborn` — 4 roof(s) of headroom, 2 free lot(s) — under the anonymous-block
programme (T-0028). Piece 4 of 4 of **T-0420**, which held all four South Water blocks in one
ticket: four blocks is four demonstrations, and T-0028's programme rule is one run, one
demonstration, one successor. This ticket owns ONE block, which is one run.

**Why this ground is workable now, and it is the whole reason the parent exists.** T-0143 and
T-0188 each refused to tighten a party-line row against a street line that might move, and T-0317
inherited the refusal. T-0009 closed it on 2026-08-29 under the owner's ruling: the drawn South
Water line does NOT move — the corridor was re-derived from committed control (`recentred`, +8.58 m)
and `data/streets/1835.json` was not touched. The refusal is discharged for the four blocks that
front this reach. `blk_south_water_market` is NOT one of them and is not in this family of
tickets: T-0183 measured it out as a wedge the South Branch pinches to 2.8 m of depth at Market,
and what to do with that wedge is with the owner.

**The block, re-derived on 2026-08-30 by `tools/reconcile_665.py`** (not typed — every figure here
is read back out of `data/reconstruction/1835_665_roof_programme.json`, and a run that finds them
changed should trust the tool and correct this table):

| field | value |
|---|---|
| bounded by | south_water (N), lake (S), dearborn (W), state (E) |
| lots | 8 |
| standing roofs | 10 |
| free lots | 2 |
| headroom | **4** — 3 principal, 1 ancillary |
| families dealt | A5, D4, D5, H3 — one roof each |
| frontage weight | 0.4886 |
| trade roofs in the deal (T-0213) | 0 |

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The 4 roof(s) stand on `blk_south_water_dearborn`'s own committed lots, and the row stands ON THE BLOCK FACE
  rather than on a re-derived line — that is the distinction T-0143 and T-0188 were protecting and
  it survives the ruling unchanged.
- `tools/reconcile_665.py` re-derives and the census reconciles: this block moves to
  `at_capacity`, or its remaining headroom is stated and why.
- The roofs are BAKED in the same commit (`./tools/bake.sh --only <structure-id>` per structure —
  `validate.py --stale` hard-fails a record that no longer matches its committed mesh), and
  `tools/publish.sh` mirrors the result.
- A screenshot from the same spot shows roofs that were not there. This is a VISIBLE ticket and it
  is the payoff the whole programme was for; it does not need the invisible-run exemption.
- One successor is handed on, per T-0028: the next block in this family, or — for whichever of the
  four runs last — the statement of where the programme's committed ground runs out.

**Links:** T-0420 (the parent) · T-0365 (the succession this discharges) · T-0009 (the ruling) ·
T-0028 (the programme) · T-0143 · T-0188 · T-0317 · T-0183 (the market wedge, not this ground) ·
`tools/reconcile_665.py` · `tools/measure_block_gating.py`.

---

## 2026-08-30 — BUILT, GATED, AND PARKED ON ONE MEASUREMENT (PR pending)

The four roofs are built, baked, published and green on `./tools/check.sh` (0 errors,
28 warnings — the same 28 `dev` carries) and on the FULL mobile smoke at 390x780. They
stand on lot 7, the block's one free corner lot, packed east to the Lake-and-State corner:
`h3_07` (boarding house) on the corner, `d5_08`, `d4_09` closing the run at the west end
nearest the bridge, and `a5_10` in the yard behind them. The block moves to `at_capacity`.

**What stops the merge is not this parcel.** `SMOKE_VIEWPORT=desktop SMOKE_STAGE=5` fails
one assertion — the `balanced` scene-detail tier's triangle ceiling at the worst stand:

| tree | balanced, worst stand (the forks, from Wolf Point) | verdict |
|---|---|---|
| `dev` at 590e64c1 | 1,208,434 of 1,210,000 | PASS by 1,566 |
| this branch | 1,210,608 of 1,210,000 | FAIL by 608 |

Four roofs cost 2,174 triangles and `dev` has 1,566 to give. **T-0458** holds the fork and
the reasoning; the short of it is that the ceiling's own block comment records five raises
and one return and twice declined a sixth, so raising it to land this parcel is exactly
what it forbids and is not a call this run may make. Every other ticket in the queue's top
band adds roofs and will meet the same wall.

**The ticket is left `open` and claimed rather than `blocked` ON PURPOSE.** `ticket.mjs
block` removes a ticket from QUEUE.md and `unblock` appends it to the BOTTOM, which would
silently re-rank a ticket the owner put in the top band on 2026-08-30 — and the queue is
his. The collision lock still holds: `claim` refuses a ticket with a rival branch, and
`steward/t-0432-south-water-dearborn` carries this work. Merge that PR once T-0458 is
answered; nothing about the parcel needs redoing.
