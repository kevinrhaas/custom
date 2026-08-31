---
id: T-0419
title: The re-centred South Water corridor stands 8.58 m off its own block faces, and the strip between belongs to neither
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The re-centred South Water corridor stands 8.58 m off its own block faces, and the strip between belongs to neither.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by **T-0009** while carrying out the owner's ruling of 2026-08-29 — the platted corridor
is derived from the street CONTROL rather than from the drawn line. On `south_water` that
translates the corridor **+8.58 m** in northing. Its block faces do not move: they come from
`generate_plat_lots.block_edges`, which offsets the DRAWN line by the same 12.192 m half-module.

So on that reach the corridor's south edge now stands 8.58 m north of the block's north face,
and **a strip 8.58 m wide belongs to neither**. Under the drawn corridor the two abutted by
construction, which is what several gates assume.

**This is why T-0009 did not swap the module default.** Making `plat_corridors.corridors()`
answer the control-derived ring town-wide was tried and measured on 2026-08-29: five gates that
read a corridor edge AGAINST a block face or a frontage line went red on an otherwise clean tree
— the cross-street platted-face census in `reconcile_665.py` (34 faces → 0), the southern-ground
stations (`measure_south_bank_ground.py`), the block-parcel street-line assertions and their
self-tests, and the far-timber census. None of them is wrong; they are all reading a plat whose
two halves are now derived from different lines.

**The question, which is the owner's kind of question and not an agent's:** is the platted BLOCK
grid on that reach also offset from the control, in which case the lots move and every roof
standing on them moves with them — or is the drawn line the block grid's own control, in which
case the corridor and the blocks are answers to two different questions and the gates should say
which one they are asking?

**Acceptance:** the strip is measured on the ground rather than in the abstract (how many lots,
how many committed roofs, how much of it is dry); the fork above is put to the owner with what
each branch costs; nothing moves until he answers. **Do not "fix" this by moving the lot grid.**

**Links:** T-0009 · K30(e) in `docs/ROADMAP.md` · `tools/plat_corridors.py` ·
`tools/generate_plat_lots.py` · T-0421.
