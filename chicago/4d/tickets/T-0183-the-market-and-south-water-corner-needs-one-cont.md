---
id: T-0183
title: The Market and South Water corner needs one control point, and the node rule may not be able to make it
state: claimed
epic: META
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: run 8/29/2026, 6:37:28 PM CT
blocked_on: null
needs_bake: false
---

The Market and South Water corner needs one control point, and the node rule may not be
able to make it.

Found by **T-0163**, which split the two street-control refusals apart and measured them.
`blk_south_water_market` — north South Water, south Lake, west Market, east Franklin — is
the one that is genuinely waiting: `tools/measure_block_gating.py` carries South Water
toward it over **25 m with 0 of 5 samples wet**. Dry ground, real block, 27 roofs of
headroom behind it, and the largest single unlock left that street control can actually
deliver.

**The block is well attested.** The post office stood at the **southwest corner of Franklin
Street and South Water Street** from 2 Nov 1832 to 3 Mar 1837, which puts it there on the
scene date (`docs/research/03-structures-north.md`) — so South Water and Franklin met, and
the block between Market and Franklin fronting South Water is not in doubt.

## What is missing

One control point, at **Market × South Water**. The committed set
(`data/traces/street_control.json`) holds exactly four:

| point | streets |
|---|---|
| `lake_canal` | Lake × Canal |
| `lake_market` | Lake × Market |
| `randolph_canal` | Randolph × Canal |
| `kinzie_canal` | Kinzie × Canal |

**None of them is on South Water Street at all.** Market's committed centreline runs from
the data box at N -400 north to `lake_market` and stops there — at its only control point,
where Lake crosses it. It is not carried the further ~110 m north to South Water, because
there is nothing to carry it to.

## Why this may be harder than adding a row to a file

The project's `node_rule` makes a junction from "the set of nodes SHARED BY THE TWO NAMED
SURFACE ROADWAYS", averaged. Market's modern successor is **North Upper Wacker Drive** and
South Water's is **East Upper Wacker Drive** — and around the forks those are plausibly the
SAME carriageway changing name at a bend, not two roadways that cross. If so there is no
shared-node pair to average and the rule cannot produce this point as written.

**This is stated as the thing to check, not as a finding.** It was not verified: deriving
control needs the network (`tools/refetch_control.py --discover`), which is on-demand and
deliberately outside `tools/check.sh`. The `lake_market` note already warns that Market's
successor is "three stacked streets ... and only the top one is the plat's", so whoever
takes this should expect the same care there.

If the rule genuinely cannot make the point, that is a decision about the rule and belongs
with the owner rather than in a steward run: a bend node is not a crossing, and adopting one
would widen what counts as control for every future placement.

## Acceptance

Either a control point at Market × South Water is derived under a rule this project will
accept — recorded in `data/traces/street_control.json` with its OSM node ids and the rule it
was made under, Market's centreline carried north to it, and `blk_south_water_market`
building in `tools/generate_plat_lots.py` with its 27 roofs moving out of the West and South
balances into a real block — or the reason the rule cannot make it is recorded on the block
and on `node_rule`, and the owner is asked the one question that would settle it.

`tools/measure_block_gating.py` must keep passing either way: if the block starts building,
it leaves the refusal list and the gate stops measuring it.

---

## WHAT WAS FOUND — 2026-08-27. The rule cannot make the point, and it does not say so.

The check this ticket asked for was run, against today's OpenStreetMap, and it reproduces:

    python3 tools/refetch_control.py --discover market_south_water    # exits 1

`--discover` learned two things in this slice. It can now read a junction out of the new
`refused_control` section of `data/traces/street_control.json` — entries with the `osm_ways`
and the search centre but deliberately **no coordinate**, because a refused junction has no
committed position — and it now compares the set it discovers against the control already in
the file and refuses one it recognises.

### The reading

| | |
|---|---|
| named ways | `North Upper Wacker Drive` × `West Upper Wacker Drive` |
| shared surface-roadway nodes | **2** — `28358888`, `28358944` |
| mean | E 447161.86, N 4637285.38 — local **(89.16, −110.42)** |
| spread | 17.68 m |
| and that is | **`lake_market`**, already committed, to the id and to the centimetre |

The way geometry says why. North Upper Wacker's northernmost way (`931237154`) **ends** at
node `28358944`; West Upper Wacker's first way (`319358162`) **begins** at it and runs
north-east to E 447213.3, N 4637344.7; its other carriageway (`319358170`) comes back down to
`28358888`. The two arms are one carriageway pair changing name through a **bend at the Lake
Street junction** — not two streets crossing at South Water. The ticket guessed exactly this
("plausibly the SAME carriageway changing name at a bend") and it is now measured rather than
suspected.

### The part that was not anticipated, and is the actual finding

**The rule does not fail loudly — it returns a wrong answer that looks right.** Two nodes, a
17.68 m spread, a clean mean: the same shape `lake_market` itself has. Committed,
`market_south_water` would have stood **on Lake Street, 110 m south of the corner it names**,
and `blk_south_water_market` would have been generated with no depth at all. Nothing in the
old output said "bend". That guard is what the tool change buys, and it is why the refusal is
recorded as an entry rather than left as an absence.

### Why there is no crossing to find

Not because the modern city lost the corner — because it lost the **street**. Wacker Drive
only reaches South Water's platted line (about local N +5 to +11) at Franklin, 120 m east of
Market; west of Franklin it turns south-west onto the Lake and Market corner. That is also why
`data/streets/1835.json` already describes South Water's west approach as following *"the dry
south bank resolved by the committed heightfield"*: the modern control was never there to
follow. **The 24 m gap at Market is a question about the 1834 sheets and the bank, not about
OpenStreetMap.**

### One thing the errand did find, and did not adopt

The same extract and the same rule read **`West Upper Wacker Drive` × `North Franklin Street`**
as a clean two-node crossing: `28358941` (E 447281.12, N 4637399.57) and `28358883`
(E 447281.20, N 4637414.85), mean E 447281.16, N 4637407.21, spread 15.28 m, local
**(208.46, +11.41)** — 6.4 m north of Franklin's committed north end, and the corner the first
post office stood on from 2 Nov 1832 to 3 Mar 1837. It would be this dataset's **first control
point anywhere on South Water Street**. Measured here, recorded in `refused_control`'s
`not_the_same_as`, and deliberately **not** adopted: committing it re-derives placements, and
it does nothing for this block, whose gap is at the west end. Filed as its own ticket.

### Where it was recorded

- `data/traces/street_control.json` — `node_rule` gains the bend failure mode; new
  `refused_control.market_south_water` holds the reading, the verdict and the question; the
  `streets` table gains `south_water`, so a street a refusal names resolves.
- `tools/refetch_control.py` — `--discover` reads refusals, tolerates a missing committed
  coordinate, and exits 1 on a set already committed under another name.
- `tools/reconcile_665.py` → `data/reconstruction/1835_665_roof_programme.json` — the block's
  `waiting_on` now says what it is really waiting on.
- `docs/RESEARCH/thompson_plat_grid.md` § 6.1.

### The one question, and it is not the one this ticket opened with

The ticket expected to ask *"may a bend node be control?"*. That question is answered by
measurement and the answer is no — a bend node here is not a looser kind of control, it is a
point 110 m wrong. What is left is genuinely the owner's, because either answer sets a
precedent for every block after this one:

> **`blk_south_water_market` has 27 roofs of headroom on measured dry ground and no
> derivable control at its west corner. Should South Water Street's committed west end be
> CLOSED onto Market's corridor from the 1834 sheets and the committed bank — the same basis
> the rest of that curve already stands on, graded for what it is — or should its 27 roofs
> stop being scheduled as gated on street control and go back to the South balance, the way
> `blk_south_water_clinton`'s did when T-0163 measured them?**

`tools/measure_block_gating.py` still passes: nothing here moved a street line, so the block
is still classified `awaiting_control` and still measures dry.

---

## THE OWNER'S RULING, 2026-08-29

Asked whether to close South Water's west end on Market's corridor or to un-gate the
block's roofs to the South balance, the owner chose:

> **Close the west end on Market's corridor, from the 1834 sheets and the committed bank
> — the same basis the rest of that curve already stands on — and grade it for what it is.**

So `blk_south_water_market`'s **27 roofs of headroom on measured dry ground** become
schedulable: the single largest block of headroom left in the programme, and T-0365
measured that it and T-0009's four blocks were the whole of it.

**"Graded for what it is" is the load-bearing half of the ruling.** This end is NOT
derived control and must not be recorded as though it were. The node rule's refusal
stands — `tools/refetch_control.py --discover market_south_water` refuses it, correctly,
and that refusal is not to be softened to make this pass. What the ruling authorises is a
DIFFERENT basis, stated as such: the 1834 sheets plus the committed bank, which is what
the rest of this curve already rests on. The grade must make a reader able to tell this
corner from a corner that has a control point, and the position note must say the node
rule refused it and why.

**Acceptance for the run that takes this:**

- South Water's committed west end is closed on Market's corridor, derived from the 1834
  sheets and the committed bank, with the derivation written where the position is.
- The record grades it for its actual basis and NAMES the refusal: no derivable control
  at that corner, bend not crossing, nearest nodes 110 m away (measured 2026-08-27).
- `tools/refetch_control.py --discover market_south_water` still refuses. If a run finds
  itself editing that refusal to make this pass, it has taken the wrong path and stops.
- The block's 27 roofs are confirmed schedulable, or the reason they are not is recorded.
- A liberty entry, because a closed end on a non-control basis is a stated liberty.

---

## DONE — the closure, 2026-08-30

The owner's ruling was carried out. **South Water Street's west end is closed on Market's
corridor at local (89.51, −71.02), and `blk_south_water_market` builds.**

### The corner, and how it was derived

Market Street's platted centreline — the line through the data box at N −400 and the committed
control point `lake_market` — is carried NORTH until the committed heightfield
`e1834_harbor_cut` turns wet. The northernmost dry sample on it, bisected to 0.01 m against the
same water test `tools/generate_plat_lots.py` uses, is **(89.51, −71.02)**. That is the 1834
sheets for the line and the committed bank for the stop, which is the basis the ruling named and
the basis the rest of this street's curved west approach already stood on.

South Water's path loses its old terminal vertex **(100, −101)** — which ran 30 m down the South
Branch's east bank, past Lake Street's own latitude, and is Market Street's ground rather than
this street's — and gains the corner plus one vertex at **(101, −71)** carrying the line east
along the point of land to the committed (120, −57). Every 0.5 m sample of both new segments is
on dry, modelled ground; a single segment from the corner to (120, −57) is not, and that is why
there are two.

Market's own path gains (89.51, −71.02) as its north end. The added vertex is collinear with the
control the line already stood on, so nothing between Lake Street and the data box moved: the
seven `blk_lake_market` and `blk_randolph_market` roofs shift by at most 5 mm and 0.01°, from the
miter join, and no mesh goes stale.

### Graded for what it is

- `south_water.west_end` in `data/streets/1835.json` carries the corner, the derivation, the
  grade **`conjectural`**, and `not_control` — which names the refusal in its own words: the bend
  at the Lake Street junction, the two shared nodes, the 110 m.
- `refused_control.market_south_water` in `data/traces/street_control.json` is **unchanged**
  except for an appended `what_the_owner_ruled` recording the decision and the fact that nothing
  was softened. **`python3 tools/refetch_control.py --discover market_south_water` was re-run
  against today's OpenStreetMap in this run and still exits 1** — same two nodes, same 17.68 m
  spread, same verdict.
- Liberty **L214**, and `docs/RESEARCH/thompson_plat_grid.md` § 6.2.

### The block

8 lots, 4,957 m², 107.0 m of frontage, depth 8.8 m at the Market end to 36.9 m at Franklin — the
wedge the bank leaves between the river and Lake Street. Plat block **21**'s number is stamped on
a block instead of on an omission. The grid goes 19 blocks → 20 and 34 cross-street platted faces
→ 36; the street edge goes 36 block faces → 38.

**The 27 roofs are confirmed schedulable and are deliberately not dealt here.**
`tools/measure_block_gating.py` no longer lists the block at all — it stopped being a refusal, so
there is nothing left for that gate to classify, and `blk_south_water_clinton` stays
`never_platted` (316 m, 26 of 64 samples wet). `tools/reconcile_665.py` re-ran and the block is
available to the schedule; dealing its roofs re-derives the occupancy ledger and is its own unit
of work, filed rather than smuggled in here.

### Found along the way

**T-0428** — `tools/derive_timber_belt.py --write` left `trees.js` unparseable when the derived
belt grew from 7 points to 8. Repaired by hand in this run; the tool is not.
