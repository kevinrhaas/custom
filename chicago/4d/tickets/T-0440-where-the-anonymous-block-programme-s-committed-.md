---
id: T-0440
title: Where the anonymous-block programme's committed ground runs out, now that the four South Water blocks T-0420 held are dealt
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-30
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---
T-0028's programme rule is one run, one demonstration, one successor. T-0420 was split into
four block tickets — T-0429 `blk_south_water_lasalle`, T-0430 `blk_south_water_franklin`,
T-0431 `blk_south_water_clark`, T-0432 `blk_south_water_dearborn` — and this is the
successor T-0432 hands on: **the statement of where the programme's committed ground runs
out**, which T-0365 asked for and no run has yet written.

The question is not "what is left" but "what is left that this generator can actually
build", and the two have diverged. What is known today, and what a run of this ticket has to
re-derive rather than copy:

- `blk_south_water_market` is out. T-0183 measured it as a wedge the South Branch pinches to
  2.8 m of depth at Market, and what to do with the wedge is with the owner.
- `blk_south_water_clinton` is `not_a_block` (T-0163), 328 m away across open water.
- `blk_washington_clark` stands off the modelled terrain — `measure_southern_ground.py`'s
  own self-test names it — so every placement on it would die in the generator.
- The four South Water blocks above are dealt as of 2026-08-30, so the reach that T-0009's
  ruling opened is spent.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- One re-derived statement, from `tools/reconcile_665.py` and `tools/measure_block_gating.py`
  rather than from this list, naming every block the schedule still calls `open`, its
  headroom, and for each one the SPECIFIC thing that stands between it and a run — street
  control, terrain, an owner fork, or nothing at all.
- Where the answer is "nothing at all", the block becomes a ticket at the QUEUE bottom, so
  the programme's next run is a row rather than a search.
- Where the answer is a fork, it is put to the owner in the ticket that holds it, not
  restated here.
- If the honest answer is that the committed ground IS exhausted, the ticket says so plainly
  and names what would extend it — which is the outcome T-0365 was actually asking about.

**Links:** T-0432 (the run that hands this on) · T-0028 (the programme) · T-0365 · T-0420 ·
T-0183 · T-0163 · T-0009 · `tools/reconcile_665.py` · `tools/measure_block_gating.py` ·
`tools/measure_southern_ground.py`.
