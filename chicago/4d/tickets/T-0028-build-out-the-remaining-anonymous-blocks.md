---
id: T-0028
title: Build out the NEXT anonymous block (one per run)
state: open
epic: TOWN
requested_by: loop
seen: true
effort: M
legacy_id: T-A13+
parent: null
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

The remaining anonymous blocks (T-A13…T-An pattern): continue block-by-block with the
adoption rules as they now stand (K28's projections clause, K31/K32 pending). Deep history:
§ T-A13…T-An (~7125).

**Acceptance:** one block per run, its gates green, STATUS row per block.

---
**SIZED 2026-08-17 as a PROGRAMME TICKET, not a batch.** "The remaining blocks" is many runs
and cannot be one ticket; naming every future block now would invent a plan the adoption
rules will change. So this ticket is **one block**, and the rule that keeps the programme
alive is in its acceptance: **the run that closes this ticket files the next block's ticket
before it closes**, `--by loop`, which lands at the QUEUE bottom for the owner to rank.

That is the general pattern for any open-ended programme here: one run, one demonstration,
one successor — never a ticket whose scope is "keep going".

**Acceptance:** one named block built to the adoption rules as they stand, its gates green,
its STATUS row written, AND the successor ticket filed.

---

## 2026-08-23 — THERE IS NO NEXT BLOCK, and that is the answer rather than a blocked run

Claimed to build one, and the schedule says there is none to open. `tools/reconcile_665.py`
re-derived `data/reconstruction/1835_665_roof_programme.json` with **no diff**, so the committed
schedule is current, and every platted block under committed street control is now one of:

- **`at_capacity`** — eleven of them, nothing left to deal;
- **`open`** — six, but their headroom is on lots that ALREADY STAND. Densifying those is the core
  density standard, **T-0143**, explicitly a different ticket in the same programme;
- **`reserved`** — `blk_randolph_lasalle`, the public square, refused at T-A16.

**The two platted blocks left are both `gated` on one thing.** `blk_south_water_clinton` and
`blk_south_water_market` — the West Side pair bounded by South Water, Lake, Clinton and Canal —
carry 8 lots, 31 capacity roofs and **27 headroom each**, and both read
`waiting_on: "South Water Street's committed centreline stops 878 m short of this block"`. Their
`lots_note` is explicit that the eight lots are *assumed from the emitted blocks' own subdivision;
the block itself is not generated, so it has no measured geometry.* **No adoption rule is waiting
on a decision here — the block generator has nothing to stand on.**

The programme states the same constraint itself: *"32 of the 331 remaining roofs stand on ground
this project has already surveyed, platted and modelled. The other 299 have nowhere to go until
street control, terrain and hydrology reach them. The binding constraint on the 665-roof programme
is coverage, not recipes."* Those 32 are precisely the `open` blocks' headroom — T-0143's.

**Successor filed: T-0163**, the street control, which would open **54 roofs** of platted
schedulable ground at once — the largest single unlock left in the programme. ROADMAP S9 already
records the control as owed; T-0163 names what it is now costing.

**Left open rather than closed**, deliberately. Closing this on "there was nothing to build" would
bury the programme's terminal state inside a done ticket, and the ticket resumes the moment T-0163
lands. Whether it closes against T-0163 or waits is the owner's call.
