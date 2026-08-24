---
id: T-0182
title: The Market and South Water corner needs one control point, and the node rule may not be able to make it
state: open
epic: META
requested_by: steward
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
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
