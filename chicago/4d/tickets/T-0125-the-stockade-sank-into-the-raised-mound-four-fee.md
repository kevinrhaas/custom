---
id: T-0125
title: The stockade sank into the raised mound: four feet of picket show from the parade
state: blocked-owner
epic: TOWN
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-20
closed: null
pr: null
claimed_by: null
blocked_on: Which gives — the bake (stepped pickets), the mound, or the placement? Three options in the ticket; each changes a different researched claim. No dimension moves without your say-so.
needs_bake: false
---

The stockade sank into the raised mound: four feet of picket show from the parade.

Found while gating T-0123 ("prove the fort stockade stands its full twelve feet").
The bake is right and the record is right — `fort_dearborn_palisade` states
`picket_height_m` 3.7 m and the committed GLB measures **3.80 m** of picket. What
a walker MEETS is not: the wall shows about **1.15 m** above the ground along its
whole south, west and east faces, and a level gaze at the south wall from the
fort road sails clean over the pickets into the compound.

## Measured, 2026-08-20, on the published mirror

- The placement contract anchors a rigid mesh at the LOWEST ground under it
  (`buildings.groundUnder`; the "shares the terrain surface" gate allows bedding
  up to 3 m and forbids floating). For the stockade that lowest point is the
  river bank under the north-west bastion: ground **1.02 m**, so the wall top
  stands at **4.82 m** world.
- The mound raise of changelog **v202** ("Fort Dearborn stands higher on its
  mound", 2026-08-20) lifted the parade-side ground under the fort to
  **3.62–3.68 m**. Wall top 4.82 − ground 3.65 ≈ **1.17 m of visible picket** —
  four feet, on a twelve-foot wall. Before v202 the mound rose "only a foot or
  so" and the wall stood essentially full height.
- Sampled every ~6.6 m around the authored 53 m square: visible height is
  1.14–1.21 m along the south, east and west walls, rising to 2.7 m only at the
  north-west corner where the bank falls away. The walker's eye is 1.68 m.
- So the owner's 2026-08-19 report on T-0123 ("way too short … below my
  height") is now literally true of the fort's own wall from every landward
  approach — whatever he was looking at that day, this is what a visitor meets
  today.

## The remedy is a judgement about the reconstruction — the owner's

A rigid 53 m mesh on 2.6 m of relief cannot both hug the ground and hold its
height; something has to give, and each option changes a different claim:

1. **Bake the stockade stepped or draped** (pickets follow the grade, tops
   stepping down the bank the way a real set-picket wall does). Truest to the
   type; needs the bake pipeline and terrain knowledge at bake time.
2. **Regrade the mound under the wall line** (flatten the fort's pad so the
   relief under the palisade box is small). Touches v202's researched mound.
3. **Move the placement a few metres south-east** off the bank slope
   (uncertainty is ±20 m). Shrinks the relief under the box; does not zero it.

None of these is a dimension change to `picket_height_m`, and none should be
taken without the owner's say-so (T-0123 rule 3). The smoke now pins the two
truths that must survive any remedy: the baked picket carries the record's
3.7 m, and the wall tops a walker's eye where wall and anchor meet (the bank
foot). The parade-side clearance is deliberately NOT gated — that number is
exactly what this ticket exists to settle.

**Acceptance:** standing on the parade side (the fort road approach, local ENU
about (1148, 189) facing north), the rendered wall top clears the walker's eye
— then gate that stand in `tools/smoke_renderer.mjs` beside the T-0123 block,
and record in the changelog what gave (bake, ground or placement) and on whose
word. No change to `picket_height_m` without the owner's written say-so.

**Links:** `data/structures/fort_dearborn_palisade.json` (`picket_height_m` 3.7)
· `renderers/web/js/buildings.js` (`groundUnder`, the lowest-ground anchor) ·
changelog v202 (the mound raise) · T-0123 (the gate that found this, and the PR
carrying the frames).
