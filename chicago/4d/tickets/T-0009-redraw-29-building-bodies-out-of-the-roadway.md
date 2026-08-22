---
id: T-0009
title: Redraw 29 building bodies out of the roadway
state: blocked-owner
epic: TOWN
requested_by: loop
seen: true
effort: M
legacy_id: K30(c)
parent: null
opened: 2026-08-17
closed: null
pr: null
claimed_by: run 8/22/2026, 5:26:36 AM CT
blocked_on: K30(d) refutes this ticket's premise: 0 of the 17 deep records have their point on the kerb face, so the bodies are NOT drawn across their frontage and reflection would move twelve documented buildings a full depth behind the frontage their own control was offset to. The lap is the committed south_water centreline, deliberately shifted 4.3-8.8 m south of that control to keep the street on dry ground. THE DECISION: (1) move the ten buildings south with the street, (2) derive the platted corridor from the street control rather than from the drawn line, or (3) accept that 1835 South Water's north half was water and the intrusion table is measuring a corridor the town never had on that reach. Each changes a different sourced thing.
needs_bake: true
---

29 buildings on eight streets are drawn standing in the roadway — K30(b) proved the cause
is the DRAWING (bodies grow north from the frontage corner instead of onto their own lot
side). The analysis is banked; this is the repair. Deep history: § K30(c) (~5910).

**Acceptance:** the 17 deep intrusions fall to ~0 by reflection onto the correct side;
no record's frontage moves; NEEDS THE BAKE for the placeholder meshes.

---

**REFUTED 2026-08-22 — ROADMAP § K30(d), and the test is a command:
`tools/measure_corridor_intrusion.py --anchors`.**

K30(b) read one flag — is the body drawn toward the street from the anchor? — and concluded
the anchor stands on the frontage. That flag is true of two opposite drawings, and the one
this dataset actually uses is the other one: the point is set back by the footprint's own
depth so the street-facing **face** lands on the frontage. `--anchors` separates them by
measuring which face the anchor coincides with, and it finds the **back corner on all 17**
records in the deep mode and the kerb face on **none**. The three records that DO carry the
point at the kerb are `tremont_house_1`, `exchange_coffee_house` and `western_hotel` — the
three K30(b) itself named as already correct and ruined by reflection.

So the repair this ticket asks for would move twelve documented buildings a full depth
BEHIND the frontage their own committed control was offset to. The lap is not the drawing:
`data/streets/1835.json` says of `south_water` that east of Franklin the line *"is shifted
into the dry half of the platted riverfront corridor"*, and that shift measures 4.3–8.8 m
south of the intersection centres the ten placements were derived from.

Blocked on the owner because every way out changes something with a source behind it.
