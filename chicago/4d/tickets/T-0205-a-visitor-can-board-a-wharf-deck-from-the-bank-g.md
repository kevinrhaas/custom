---
id: T-0205
title: A visitor can board a wharf deck from the bank: grade the six landward edges
state: open
epic: TOWN
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0058
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
---

A visitor can board a wharf deck from the bank: grade the six landward edges.

Piece 2 of 2 of **T-0058 — A visitor can walk out along a wharf deck**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** a visitor walks off the bank and onto every drawn wharf deck without a teleport
onto it and without the step-up rule being widened — the ground itself rising to meet the planks —
or each site that still refuses is refused in writing with its own measured riser. Both gates green,
the ground re-baked in the same commit, and the invention recorded in `docs/LIBERTIES.md`.

**The measurement, taken by T-0204 on 2026-08-24.** Every deck holds the record's 0.90 m freeboard
floor, because the traced 1834 bank under all seven landward edges is lower than it. The riser at
the best point of each heel edge, against the walker's 0.35 m step-up rule:

| wharf | bank at the heel | riser to the deck | |
|---|---:|---:|---|
| `kinzie_hunter_warehouse` | 0.58 m | +0.32 m | boards already |
| `robert_kinzie_store` | 0.52 m | +0.38 m | refused |
| `carpenter_south_water_store` | 0.27 m | +0.63 m | refused |
| `newberry_dole_warehouse` | 0.21 m | +0.69 m | refused |
| `jh_kinzie_forwarding_store` | 0.21 m | +0.69 m | refused |
| `peck_store` | 0.20 m | +0.70 m | refused |
| `h_jones_store` | 0.19 m | +0.71 m | refused |

**The shape of the answer is already in this repo.** T-0001 left the bridge decks walkable and
unreachable for the same reason — a 2.2 m riser at a deck end the terrain put at zero — and T-0110
answered it by adding an `approaches` block to `terrain_spec.json`: graded corridors applied by
`generators/terrain_gen.py` as max()/min() against the assembled surface, each dying out where
natural ground takes over, with the invention claimed as **L147**. Six wharf heels want the same
treatment at a far smaller scale: 0.03–0.36 m of fill over the 2.0 m `heel_in_m` the deck already
ties back into the bank, which is a 1-in-6 tie at worst and gentler than any of L147's 1-in-12 road
fills — but it is a claim about the shore in front of the town's own warehouses, so it wants its own
liberty and its own reasoning rather than L147's.

**Two things to settle before building it**, because neither is obvious and both are cheap to get
wrong:
* **A fill at the water's edge is not a road fill.** L147's crests run into the shallows behind a
  bridge's log abutment cribs, which are attested. Nothing attests made ground at these landings,
  and raising the bank raises it in front of `isWater`, the flora reach and the corridor gates — so
  the reach of each fill has to be bounded by the wharf's own heel rather than swept along the bank.
* **`freeboard_m` is invented and is the other half of the riser.** Lowering it would close the gap
  without touching the terrain, and that is exactly the move to refuse: it would be tuning a figure
  about 1835 to fit a navigation rule about a walker. If it is ever revisited it is on evidence
  about working decks, in its own ticket, and not here.

**And it costs a bake.** `terrain_gen.py` writes the ground GLB, so this is a `needs_bake` ticket —
the master, the 16-bit web derivative, and the planting-reach baseline all move with it, which is
what T-0110 measured last time.

**Links:** T-0058 (parent) · T-0204 (piece 1, which made the decks floors and took the table above)
· T-0110 / L147 (the bridge approaches, the worked precedent) · T-0041 · `data/wharves/river_landings.json`
`form.freeboard_m`.
