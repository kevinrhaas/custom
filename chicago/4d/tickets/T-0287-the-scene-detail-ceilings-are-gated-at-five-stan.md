---
id: T-0287
title: The scene-detail ceilings are gated at five stands, and the public square is dearer than any of them
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The scene-detail ceilings are gated at five stands, and the public square is dearer
than any of them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-0224, which put the critic rig's first station on `blk_randolph_lasalle`
and read, at `full`, **165 draw calls / 1,024,051 triangles desktop** and **158 /
946,928 mobile** (`tools/critic_shots.mjs --stations public_square`, source tree,
2026-08-28, four browser processes, byte-identical). Both are inside
`DETAIL.full.triangles` (1,400,000) and `BUDGET.drawCalls` (215), so **this is not a
breach and must not be reported as one.**

What it is is a stand nothing gates. `tools/smoke_renderer.mjs`'s `STANDS` is
T-0135's fixed five, and the assertion on them is worded *"scene detail '<level>'
stays inside its own ceiling at the WORST stand"* — where "the WORST" means the worst
of those five. The comment above that check records `full` reaching **141 calls
desktop and 137 mobile** at its own worst. The public square reads 165 and 158.

The two figures are not directly comparable and the ticket must not assume they are:
the smoke's were read on the **published mirror** at dev `f7aca445`, the critic's on
the **source tree** today, and the town has grown between them. So the first job is
to take both readings on one tree.

**Acceptance:** the five gated stands and `public_square` measured at `full`,
`balanced` and `light` on ONE tree, at both viewports, in one table; and then either
`public_square` joins `STANDS` because it is genuinely dearer, or a written finding
naming the numbers that show the five already bound it. If it joins, the ceilings are
re-read against it before anything is re-tuned — the ceilings were raised on the
owner's decision (T-0229) and this ticket must not become a second raise by the back
door.

**Why it matters.** A ceiling is a promise about the worst frame a visitor can walk
into. This block is open ground with the whole South Division skyline across it and
no occluders at all, which is the shape that costs most; the gate has never stood on
it. See `T-0135`, `T-0229`, `T-0223`.
