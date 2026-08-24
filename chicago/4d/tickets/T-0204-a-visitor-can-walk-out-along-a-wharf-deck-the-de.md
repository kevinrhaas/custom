---
id: T-0204
title: A visitor can walk out along a wharf deck: the deck is a floor
state: claimed
epic: TOWN
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0058
opened: 2026-08-24
closed: null
pr: null
claimed_by: run 8/24/2026, 3:25:27 PM CT
blocked_on: null
needs_bake: false
---

A visitor can walk out along a wharf deck: the deck is a floor.

Piece 1 of 2 of **T-0058 — A visitor can walk out along a wharf deck**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**THE DESIGN QUESTION T-0058 NAMED, ANSWERED.** The parent set it out: a wharf deck needs
"either a record of its own or a second route into `walker.js`'s `surfaceAt()`". It is the second
route, and the LAYER publishes it rather than the record. A wharf has no structure record, so it
cannot carry the sidecar `placement.walk_surface_m` the bridges take their deck height from; minting
one to hold a height would put a second definition of the deck top beside the one
`renderers/web/js/wharves.js` already computes at load — which is the fault T-0001 found 1.8 m over
the North Branch planks, and the reason this record's freeboard figure is a FLOOR rather than a
height. So `createWharves` returns `decks` in `decksFrom()`'s own `{ id, y, pts }` shape, each `y`
the `_drawn.deck_top_m` the slab was drawn at, and `main.js` hands them to the walker beside the
bridges'. One number, not two that agree until they do not.

**Acceptance:** every drawn wharf publishes a walkable deck at EXACTLY the height its own mesh was
drawn at; a visitor walks the length of one of them over open water with the planks — not the 4.0 m
wading barrier — under the boot for every sample; and the boarding riser at all seven landward edges
is measured in the gate and reported rather than assumed, at both viewports. Never by widening the
step-up rule or lowering the freeboard to make a deck reachable.

**What it does not buy, measured.** The deck holds its 0.90 m freeboard floor at all seven sites,
because the traced bank under every landward edge is lower than that. Against the walker's 0.35 m
step-up rule, the riser at the best point of each heel edge is:

| wharf | bank at the heel | riser to the deck | |
|---|---:|---:|---|
| `kinzie_hunter_warehouse` | 0.58 m | **+0.32 m** | boards |
| `robert_kinzie_store` | 0.52 m | +0.38 m | refused |
| `carpenter_south_water_store` | 0.27 m | +0.63 m | refused |
| `newberry_dole_warehouse` | 0.21 m | +0.69 m | refused |
| `jh_kinzie_forwarding_store` | 0.21 m | +0.69 m | refused |
| `peck_store` | 0.20 m | +0.70 m | refused |
| `h_jones_store` | 0.19 m | +0.71 m | refused |

One of the seven can be walked onto from the ground, and it is the one dock in the town whose
existence is stated rather than reconstructed — Kinzie & Hunter's, the attested "warehouse with its
dock along the river front". The other six are **T-0205**, and they are the same edge T-0001 hit at
the bridge abutments, to be answered the same way it was: by grading the bank in `terrain_spec.json`
so the ground rises to meet the deck, which is terrain and needs a bake. No ramp is faked here and
no threshold is widened.

**Links:** T-0058 (parent) · T-0205 (piece 2) · T-0041 (the wharf layer) · T-0001 / T-0110 (the
bridges' walker half, then their terrain half — the same two-run shape) · `docs/GLB-CONTRACT.md`.
