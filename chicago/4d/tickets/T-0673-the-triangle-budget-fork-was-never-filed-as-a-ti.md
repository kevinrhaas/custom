---
id: T-0673
title: The triangle-budget fork was never filed as a ticket, so the owner's answer had nothing to land against: record the ruling and spend it only where a breach is measured
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-03
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

## ★ THE OWNER'S RULING, RECORDED — 2026-09-03 (evening)

**Verbatim: "i answered raise with stated headroom and a named retirement from before but it
may have been lost."**

It was lost, and this ticket is the receipt so it cannot be again.

## The failure this ticket exists for

PR #599 says, in as many words: *"**T-0441** holds the fork with the measurement and three
shapes an answer could take (raise with stated headroom and a named retirement · trim first
and name the trim · hold the buildings). One line from the owner unblocks four tickets."*

**T-0441 was never filed.** There is a clean id gap between T-0440 and T-0442. The run that
wrote that sentence named a ticket it did not create, so the owner's answer had nothing to
land against and four PRs — #432, #599, #601 and behind them the whole visible-buildings
band — sat parked for four days on a question the ledger had never been asked.

**The rule this establishes:** a fork put to the owner is not put to him until it is a
ticket. A PR comment naming a ticket id is not the same as filing it, and `ticket.mjs check`
cannot catch the difference because the id simply never exists.

## What the ruling authorises

A raise of a scene-detail ceiling, **with the headroom stated and a retirement named** — the
shape T-0229 already established (it raised `full` 1,400,000 → 1,425,000 and `balanced`
1,210,000 → 1,260,000 on the owner's decision, and existed to take them back down again).

## …and the measurement that says where NOT to spend it

Measured on `dev` the same evening, `tools/measure_detail_ceilings.mjs --only desktop`,
against the published mirror:

| tier | worst stand (the forks, from Wolf Point) | ceiling | clear |
|---|---|---|---|
| `full` | 1,385,925 | 1,400,000 | **14,075** |
| `balanced` | 1,211,986 | **1,225,000** | **13,014** |
| `light` | 769,379 | 785,000 | **15,621** |

Two things had moved under the parked PRs. `balanced` is **1,225,000** in code today, not
the 1,210,000 PR #599 measured against on 2026-08-30; and content has been trimmed since,
so `dev` sits 13,014 clear where #599 found 1,566. Against that headroom:

| PR | parcel | at the forks | verdict |
|---|---|---|---|
| **#599** (T-0432) | 4 roofs, +2,174 | 1,214,160 | **passes by 10,840** — no raise needed |
| **#601** (T-0431) | 4 roofs | same order | **passes** — no raise needed |
| **#432** (T-0219) | heightfield, +56,016 (2026-08-28 figure) | 1,268,002 | **still fails by 43,002** |

**So the raise is NOT taken for #599 and #601.** Their breach dissolved on its own, and a
ceiling raised to carry a record that already fits is exactly what the block comment at the
definition forbids: it records **five raises and one return** and says a sixth "has to argue
against" that count. Spending an authorisation where the numbers do not need it is how the
count gets to six for nothing.

## What is left to do, and the one number this ticket refuses to guess

**#432 is the only PR the ruling is needed for.** Before the raise is written:

1. **Re-measure #432 on current `dev`.** Its +56,016 is a 2026-08-28 figure taken against a
   different tree; the branch has been conflicted since. The raise is sized from a fresh
   `measure_detail_ceilings.mjs --against` run, never from that number.
2. **State the headroom** the new ceiling leaves at the worst stand, as a figure and as a
   percentage, so the next parcel knows what it is spending into.
3. **Name the retirement** — the ticket whose landing takes the ceiling back down, and file
   it if it does not exist. T-0229's own retirement was blocked on a flora ticket and would
   never have come due (T-0231 records that); the retirement named here must be one that can
   actually fall due.
4. Note that `full` and `light` carry 14,075 and 15,621 of their own. If #432 breaches only
   `balanced`, only `balanced` moves — the ladder keeps its shape, per T-0098's principle.

**Done when** the ruling is recorded here (it is), #599 and #601 are shown to need no raise
(they are, above), and #432 either lands under a raise sized from a fresh measurement with a
retirement that can fall due, or is shown to fit without one.
