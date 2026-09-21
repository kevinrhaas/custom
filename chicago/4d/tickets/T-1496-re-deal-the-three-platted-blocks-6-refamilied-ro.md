---
id: T-1496
title: Re-deal the three platted blocks' 6 refamilied roofs across the principal/ancillary line: generate_block_infill gates a block's claimed schedule and refuses a second principal roof on a lot that already has one, so an ancillary yard building moved into a dwelling family is a re-deal of the block's mix, not a field edit; with the screenshot from Lake and Clark
state: withdrawn
epic: TOWN
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1452
opened: 2026-09-20
closed: 2026-09-21
pr: 1633
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: 2026-09-21T16:05:32.033Z
claimed_run: null
---

Re-deal the three platted blocks' 6 refamilied roofs across the principal/ancillary line: generate_block_infill gates a block's claimed schedule and refuses a second principal roof on a lot that already has one, so an ancillary yard building moved into a dwelling family is a re-deal of the block's mix, not a field edit; with the screenshot from Lake and Clark.

Piece 3 of 3 of **T-1452 — Migrate the 26 refamilied roofs whose id moves — the phase-one South parcel, the North Division parcel and the three platted blocks — against the measured reference list: sidecars, enclosures, liberties, signage, yard, frontage, lodgers, seating and business files all name these ids, and blk ancillary slots cross the principal/ancillary line; with the screenshot from Lake and Clark**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

## WITHDRAWN 2026-09-21 — A DUPLICATE T-1452 WAS SPLIT TWICE INTO EXISTENCE

`ticket.mjs split` had no guard on the state of the ticket it was splitting, so
T-1452 was split twice, four hours apart on 2026-09-20:

  13:48  run 35529393603 claims T-1452 and splits it into T-1480/T-1481/T-1482
  17:52  run 35542539851 reads T-1452 and splits it AGAIN into T-1494/T-1495/T-1496

Both cuts carve the SAME twenty-six roofs into the same three parcels, so the queue
carried six rows for three pieces of work, in pairs that read as unrelated rows.
This ticket is the second cut's copy of T-1482.

**The work is not dropped — T-1482 is the first cut's copy of the three platted blocks' six roofs — the two are both headed "Piece 3 of 3 of T-1452" — and it is in flight as this is written.**** The guard that stops the next one is in
`tools/ticket.mjs` (`split` refuses a parent that is already `split`, `done` or
`withdrawn`) with assertions 24-27 of `tools/test_ticket_claim_split.mjs`.

**Reopen rule.** If T-1482 ends without landing — withdrawn, or blocked and
abandoned — set this ticket's `state` back to `open` and append its row at the foot of
its band in QUEUE.md. Nothing here is lost, only deduplicated.
