---
id: T-0365
title: The anonymous-block programme has no unblocked ground left: every block with headroom is on the South Water reach T-0009 holds open
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
The anonymous-block programme has no unblocked ground left: every block with headroom is on the South Water reach T-0009 holds open.

Filed by **T-0317** as its successor, which is T-0028's programme rule — *one run, one
demonstration, one successor* — and this is the run where the succession has nothing to hand on.

**What was re-derived on 2026-08-29**, after `blk_randolph_market` took its second deal and went
`at_capacity` (`tools/reconcile_665.py`). Every platted block still carrying headroom:

| block | state | headroom | free lots | what holds it |
|---|---|---|---|---|
| `blk_south_water_franklin` | open | 4 | 2 | the South Water street line, **T-0009**, `blocked-owner` |
| `blk_south_water_lasalle` | open | 8 | 3 | the same |
| `blk_south_water_clark` | open | 4 | 2 | the same |
| `blk_south_water_dearborn` | open | 4 | 2 | the same |
| `blk_south_water_market` | gated | 27 | 8 | **T-0183**, `blocked-owner` — Market x South Water is a bend in Wacker Drive, not a crossing, and the node rule cannot derive a control point |

That is the whole of it. `blk_south_water_clinton` is `not_a_block` and no trace will ever join it
(T-0163), and every other platted block in the schedule is `at_capacity`.

**Why the four `open` ones are not simply workable.** They front the reach whose committed street
line is the open question in T-0009, and **T-0143 and T-0188 each refused to tighten a party-line
row against a line that may move**. That refusal is not a preference — a run stands ON the face,
so a face that moves moves the whole row, and the metres would be re-derived rather than corrected.
T-0317 inherited that refusal and did not reopen it.

**So this is a fork for the owner, not a missing number** (AGENTS.md § RECONSTRUCTED IS A TIER
draws that line, and it puts committed street CONTROL on the owner's side of it). The options, in
the shape the two blocking tickets already state them:

1. **Answer T-0009** — commit the South Water street line as it stands, and the four `open` blocks
   carry 20 roofs of headroom between them the next morning.
2. **Answer T-0183** — settle the Market x South Water control point, and `blk_south_water_market`
   alone carries 27 roofs on ground already measured dry (`tools/measure_block_gating.py`: South
   Water is 25 m away, 0 of 5 samples wet).
3. **Neither yet** — and then the programme's next visible ground is the CORE DENSITY standard on
   blocks that already stand (the T-0079 -> T-0105 -> T-0143 -> T-0188 line), which is a different
   programme with a different acceptance, not this one's successor.

**Acceptance:** the owner picks one of the three, or names a fourth. If it is (1) or (2), this
ticket closes by filing the next `open the block` ticket against the ground that unblocks. If it
is (3), it closes by recording that T-0028's programme is complete for the ground the project
holds, and the succession stops rather than being handed on to a block that cannot be built.

**Links:** T-0028 (the programme) - T-0317 (the run that filed this) - T-0009 - T-0183 - T-0163 -
T-0143 - T-0188 - `tools/reconcile_665.py` - `tools/measure_block_gating.py`.
