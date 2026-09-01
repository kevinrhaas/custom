---
id: T-0460
title: The plank walk meets the dirt road in a jagged sawtooth, and it is the first thing a visitor sees
state: open
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-08-31
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Reported by the owner on 2026-08-31, with a screenshot, and flagged as wanting
fixing **sooner than most**: *"this one still really bugs me… it's like the first
thing we see."*

The plank walk meets the dirt road in a **jagged sawtooth**. Close up it reads as
a row of loose boards with ragged ends rather than as a made footway. The owner's
statement of what would be acceptable is either of:

- the plank walk sits **consistently over** the dirt road, or
- the walk is **dirty** — the boards meet the mud the way boards in mud do

What is not acceptable is the current in-between: a clean hard sawtooth edge.

## Measured

`data/frontage/town_street_edge.json` — 77 runs, 41 `plank_walk` and 36
`board_crossing`, **254 footway decks** in total:

| | |
|---|---|
| walk width | 1.83 m (6 ft) |
| deck rise over the ground | **0.06 m and 0.11 m** |
| plank thickness | 0.055 m |
| plank pitch | 0.26 m on a walk, 0.32 m on a street edge (`EDGE_PLANK_PITCH_M`) |
| clear between wall face and deck | 0.20 m (`WALK_CLEAR_M`) |

The deck stands **6 to 11 cm proud of the ground** and is built of individual
boards at a 26–32 cm pitch. The sawtooth is what those two facts produce at the
outer edge when nothing resolves the boundary: each board ends where it ends, the
deck is high enough to cast a hard line, and the road surface simply stops.

## Where this sits against the rest of the queue

This is a **visible-quality** ticket in a queue whose top band exists because 41
merges added nothing a visitor could see. It is at the front door of the
experience — the owner's point is that it is among the first things in view — and
it is cheap next to the ground work in T-0444 and T-0453.

**Acceptance:**

1. The chosen treatment is stated before it is built, and it is one of the
   owner's two: the walk sits over the road consistently, or the boards meet dirt
   as dirty boards do. **Not a compromise that keeps the hard sawtooth.**
2. Whatever is chosen is applied to all **254 decks**, not to the one in the
   screenshot. A fix visible from one stand and wrong from the next is not a fix.
3. It holds at walking distance. The fault is reported from close up, so the
   demonstration is a close stand, not an overhead.
4. The 6 cm and 11 cm rises are re-read: if the rise is what makes the edge hard,
   say so and say what it becomes. `WALK_RISE_M` is a chosen number, not a source.
5. `tools/check.sh` green, and the renderer smoke carries an assertion for
   whatever the new edge rule is.
