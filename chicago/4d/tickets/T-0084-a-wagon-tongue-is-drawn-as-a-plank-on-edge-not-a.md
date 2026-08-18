---
id: T-0084
title: A wagon tongue is drawn as a plank on edge, not a pole
state: open
epic: RENDERING
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-18
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Seen while shipping T-0081, standing in the Green Tree's yard where three wagons now
have their tongues down: the tongue reads as a heavy dark board lying on the grass, not
as a pole.

`renderers/web/js/yard.js` draws it as ONE horizontal box spanning the drop from the
front axle to the ground — `halfH = (rootY - tipY) / 2`, about 0.24 m — so a 2.75 m
stick 0.055 m thick is drawn 0.48 m deep. The comment says why it was done that way ("a
tongue is a stick, and a stick's exact inclination is not a claim this record makes"),
and that reasoning is sound about the ANGLE and wrong about the SECTION: the box has to
be that deep only because it is axis-aligned. An inclined box of the tongue's own
section makes the same claim about the angle and does not put a plank in the yard.

**Acceptance:** the tongue is drawn at its recorded section along its own inclination
(`pushBoxV` already exists on this layer for exactly this), on every wagon, with the
smoke's wagon bound unchanged; and one frame from the Green Tree's yard shows a pole.
