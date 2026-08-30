---
id: T-0365
title: The anonymous-block programme has no unblocked ground left: every block with headroom is on the South Water reach T-0009 holds open
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: 2026-08-29
pr: 585
claimed_by: run 8/29/2026, 9:16:09 PM CT
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

---

## RESOLVED 2026-08-29 — THE OWNER ANSWERED, AND IT WAS OPTION 1

The fork this ticket posed is closed. Both blocking tickets moved on 2026-08-29, and the
answers are recorded in the tickets themselves rather than only in a PR body:

- **Option 1 — T-0009 (`done`, PR #567).** The owner was asked which of three readings the
  South Water corridor is and chose: *derive the platted corridor from the street CONTROL
  rather than from the drawn line.* The half of that ruling this programme needed is one
  sentence — **the drawn South Water line does not move** ("It does not license moving the
  drawn centreline back onto the control. The street is drawn where it is for a stated
  reason and stays there"). That discharges the refusal this ticket inherited: T-0143 and
  T-0188 each declined to tighten a party-line row *against a line that may move*, and the
  line has now been ruled not to move. The four `open` blocks are workable ground.
- **Option 2 — T-0183 (`blocked-owner`, measured in PR #573).** Its 27 roofs are not
  available and may never be. Closing South Water's west end onto Market as committed emits
  `blk_south_water_market` as a bowtie, and carried as far north as the committed waterline
  allows the block has 2.8 m of depth at Market against the 24.384 m one platted lot fronts.
  It is a wedge the South Branch pinches out, and the choice between building it and
  returning the roofs to the South balance is back with the owner. **This programme does not
  wait on it** — the 20 roofs option 1 freed are unaffected.

### The census re-derives unchanged on today's `dev`

`tools/reconcile_665.py` re-run on an unmodified `dev` at `6a88b421`, and it is the same table
this ticket derived when it was filed, so nothing has been spent or lost in between:

| block | state | headroom | free lots | what holds it |
|---|---|---|---|---|
| `blk_south_water_lasalle` | open | 8 | 3 | nothing — T-0009 answered |
| `blk_south_water_franklin` | open | 4 | 2 | nothing — T-0009 answered |
| `blk_south_water_clark` | open | 4 | 2 | nothing — T-0009 answered |
| `blk_south_water_dearborn` | open | 4 | 2 | nothing — T-0009 answered |
| `blk_south_water_market` | gated | 27 | 8 | **T-0183**, `blocked-owner` — the wedge |

`coverage.schedulable_on_committed_ground` reads **20**, which is the four `open` blocks
exactly. Every other platted block in the schedule is `at_capacity`, `blk_south_water_clinton`
is `not_a_block` (T-0163), and the four remaining `gated` rows are the un-surveyed divisions,
not lots.

### The successor, and why it had to be split before it could be run

T-0028's programme rule is *one run, one demonstration, one successor*, and this ticket's
acceptance is that the succession is handed to ground that can actually be built. T-0420 was
filed against that ground but could not be run as written: it holds **four** blocks and says
so itself — *"Take ONE block per run — four blocks is four runs."* An `M` carrying four
demonstrations is the case AGENTS.md's sizing test exists for, and the failure it invites is
the self-invented "(1/4)" the same page forbids: a run claims it, opens one block, and leaves
the ticket claimed with three blocks of work still in it.

So T-0420 is **split** here, one ticket per block, each one run with its bake, each with the
acceptance stated on its own face. The children hold T-0420's place in QUEUE — this is a
split, not a re-ranking, and the owner's order is untouched.

**The succession stands.** This ticket closes handing four buildable blocks to four runs.
