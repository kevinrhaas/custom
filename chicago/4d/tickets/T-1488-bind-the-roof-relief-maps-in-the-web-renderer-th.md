---
id: T-1488
title: Bind the roof relief maps in the web renderer: the metric roof UVs a 4.48 m tile needs — the smart-project atlas is a per-object island pack and cannot tile one — one shared material per roof substrate, the two maps published, and the draw count measured at the critic stations at both viewports
state: open
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-1465
opened: 2026-09-20
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: null
---

Bind the roof relief maps in the web renderer: the metric roof UVs a 4.48 m tile needs — the smart-project atlas is a per-object island pack and cannot tile one — one shared material per roof substrate, the two maps published, and the draw count measured at the critic stations at both viewports.

Piece 2 of 2 of **T-1465 — Give every roof its covering and its texture before the 297 are built: shingle and roof_board substrates on the sheet, dealt by archetype, bound to the vendored relief maps on L263's exposure — a roof nobody can see the material of is not a reconstruction, it is a gap**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**What T-1487 leaves you.** The sheet carries `shingle` (4.48 m, 0.14 m exposure, 32
courses, 228.6 px/m) and `roof_board` (4.00 m), the dealing rule is written and its liberty
recorded, and every roof primitive in the town is drawn on a material named for its
covering. The vendored library (T-1450) already ships both maps with their modules intact
and measured: `wood_shingles_weathered` carries 32 course cycles in `height16` and 32 in
`ao`, `roof_boards_weathered` matches `sawn_board` at 4.00 m.

**And the question it could not answer in one run.** `generators/build.py` `unwrap()` runs
`bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.02)` per object. That is a
per-object island pack in 0..1 laid out for an AO atlas, so a tile rate expressed in METRES
cannot be read off it: the same map would land at a different scale on every roof and on
every island of one roof. Something has to give UV0 a metric meaning for roof faces, or add
UV1, or go triplanar in a shader — and each of those is a different bargain with the AO
path (`bake_ao`, off by default today) and with `docs/GLB-CONTRACT.md`.

**Acceptance:**

- A **decision, argued in the ticket before it is built**, on how a 4.48 m tile reaches a
  roof face: metric UV0 on roof primitives, a second UV set, or world-space triplanar —
  and what each costs the AO path and the GLB contract.
- **The relief maps are bound, not the basecolors.** `normalMap`, `roughnessMap` and
  `aoMap` per substrate; colour stays on the per-vertex stream, so the condition grading
  and T-0048's per-building jitter both survive and `materialKey()` is unchanged.
- **How the renderer knows a roof is shingled.** Material names are NOT pinned by
  `docs/GLB-CONTRACT.md` and it says in terms that a renderer keyed on one is reading a
  convention nobody promised to keep. So either the contract PROPOSES pinning the substrate
  name — bilaterally, per that document — or the substrate travels in the material's
  `extras`. Pick one and say why.
- The two roof maps are **published** into `site/chicago/4d/` by `publish.sh`, or the
  reason they are not is written down.
- **The draw count is measured at the critic stations, both viewports, before and after**,
  and lands in the ticket. One shared shingle material across every shingled roof should
  cost one draw call, not one per building — T-0285's open question answered for the case
  that actually batches.
- **Bake** if the chosen route moves a vertex or a UV, which two of the three do.
- The `lake_market` and `south_water` critic frames show roofs reading as roofs — a shingle
  field legible as courses, a board roof as boards — at both viewports.

**Stop condition:** a visitor looking at a roof can tell what it is made of.

**Links:** T-1465 (the parent) · T-1487 (the sheet, which lands first) · T-1450 · T-0285 ·
L263 · `docs/GLB-CONTRACT.md` · `docs/RESEARCH/texture_library.md`.
