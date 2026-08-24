---
id: T-0058
title: A visitor can walk out along a wharf deck
state: claimed
epic: TOWN
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-18
closed: null
pr: null
claimed_by: run 8/24/2026, 2:05:19 PM CT
blocked_on: null
needs_bake: false
---

A visitor can walk out along a wharf deck.

Filed by the run that shipped **T-0041** (the wharf layer), which deliberately did not claim it.
`terrain.walkHeight()` reports a wading barrier at +4 m over open water, and the wharf decks do not
override it, so both docks are things you see from the bank and cannot step onto. The bridges CAN
be stood on since T-0001, by a different route: `placement.walk_surface_m`, carried into a sidecar
from the archetype's resolved deck height. A wharf has no structure record and therefore no
placement, so it needs either a record of its own or a second route into `walker.js`'s
`surfaceAt()` — which is the design question, and the reason this is a ticket rather than a line in
T-0041.

Also open at the landward edge: the deck holds 0.90 m over the water and the bank at both sites is
0.2-0.6 m, so boarding it from the ground is a 0.3-0.7 m riser and the walker's 0.35 m step-up rule
refuses at least one of them — the same edge T-0001 hit at the bridge abutments.

## The design question, answered: a second route, and it already existed

The ticket offered two routes and asked which. **Neither was needed as stated** — the second route
into `surfaceAt()` had been built already, by **T-0119**, and nothing had pointed the wharves at
it. Since then a LAYER may publish `{ id, y, pts }` and `main.js` appends it to the same `decks`
registry the bridges reach through `decksFrom()`; `frontage.js` does exactly that for the river
footway over the State slough mouth and for every street-edge walk. `renderers/web/js/frontage.js`
says so in as many words: *"there is exactly one mechanism in this project for 'the visitor is
standing on something that is not the heightfield' and this is it."* So a wharf needs no structure
record, no placement and no new mechanism — it publishes its own decks and `main.js` appends them.

## The landward edge, measured before it was fixed

The ticket said the bank is "0.2-0.6 m" and that the rule "refuses at least one of them". Measured
on the committed heightfield at the three landward samples the renderer itself takes, across all
seven landings (the ticket was written when there were two):

| landing | bank at the heel | deck top | riser |
|---|---|---|---|
| `h_jones_store` | 0.19 m | 0.90 m | **0.71 m** |
| `peck_store` | 0.20 | 0.90 | **0.70** |
| `jh_kinzie_forwarding_store` | 0.21 | 0.90 | **0.69** |
| `newberry_dole_warehouse` | 0.21 | 0.90 | **0.69** |
| `carpenter_south_water_store` | 0.27 | 0.90 | **0.63** |
| `robert_kinzie_store` | 0.52 | 0.90 | 0.38 |
| `kinzie_hunter_warehouse` | 0.58 | 0.90 | 0.32 |

Against `WALK.stepUp` = 0.35 m: **five of the seven refused**, not one, and the two that cleared it
did so on the bank being higher there rather than on anything about the dock. The deck top is the
record's 0.90 m freeboard FLOOR at every landing, because the 1834 bank is under 0.60 m at all of
them — so the riser is not an accident of two sites, it is what this layer does everywhere.

Measured again after the apron went in: the step from the ground beside a deck onto its lip is
**negative at all seven** — at most 0.03 m DOWN — so nothing is stepped up onto anywhere, and the
apron's slope is 10.8° at Robert Kinzie's, 16.2° at Kinzie & Hunter and 19.2-20.1° at the other
five, none of it authored.

**Acceptance:** at every drawn landing, the layer publishes a walk surface and the step from the
bank onto it is inside the walker's own `WALK.stepUp`; and the walker, driven from the bank at
Newberry & Dole's, ends standing over open water on the drawn deck — its boot height equal to the
mesh's own height function exactly, not within a tolerance — where `terrain.walkHeight()` alone
answers the wading barrier. Asserted in `tools/smoke_renderer.mjs`, both viewports.
