---
id: T-0058
title: A visitor can walk out along a wharf deck
state: split
epic: TOWN
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-18
closed: 2026-08-24
pr: null
claimed_by: run 8/24/2026, 3:19:55 PM CT
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

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
