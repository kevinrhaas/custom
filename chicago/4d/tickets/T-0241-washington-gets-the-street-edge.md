---
id: T-0241
title: Washington gets the street edge
state: claimed
epic: TOWN
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-0191
opened: 2026-08-27
closed: null
pr: null
claimed_by: run 8/27/2026, 6:18:01 PM CT
blocked_on: null
needs_bake: false
---

Washington gets the street edge.

Piece 2 of 2 of **T-0191 — Randolph and Washington get the street edge**, split because
the parent needed more than one run's demonstration. This half is the one that does not
fit today, and the number is why the split exists rather than a preference.

## It was built and measured, not deferred on a guess

Both streets were added to `EDGE_STREETS` together and generated together — 36 block
faces, 3,129.1 m of walk, 30 crossings, 35 fence runs, 239 walking decks. Read on the
published mirror with `tools/measure_detail_ceilings.mjs`, desktop 1280x800, worst of
T-0135's five stands:

| tier | ceiling | both streets | Randolph alone (shipped, T-0240) | Washington's share |
|---|---:|---:|---:|---:|
| `full` | 1,425,000 | 1,385,207 | 1,369,835 | +15,372 |
| `balanced` | 1,260,000 | **1,260,174 — OVER by 174** | 1,201,248 | **+58,926** |
| `light` | 1,050,000 | 761,404 | 745,904 | +15,500 |

Washington's seven block faces cost **58,926 triangles at `balanced`** at the worst stand
and only about 15,400 at the tiers either side of it — so this is not "the town is full",
it is `balanced` specifically, which is the rung T-0098 already recorded as the one
"squeezed to nothing" while `full` carried headroom.

## What unblocks it, and what does not

**Not a ceiling raise.** T-0237's acceptance names that route and refuses it, and the
count of re-basings written into `renderers/web/js/main.js` beside `DETAIL` is the
argument. This ticket is not a request for the sixth.

Any ONE of these makes Washington affordable, and each is somebody else's ticket:

- **T-0056** — the enclosure layer pays its full triangle cost at every scene-detail
  level. The street edge's fences are enclosures; a `balanced` tier that thinned them
  would pay for this street outright.
- **T-0223's remaining steps** — the timber cull's first step recovered ~160,000 at this
  stand. What is left of that ticket is the same shape of finding.
- **A `balanced` trim on the street edge layer itself** — the walk is already down to
  42.8 triangles a metre from 61.6 (see `EDGE_PLANK_UNDERSIDE` and the stringer-bay note
  in `tools/generate_frontage_works.py`); whether a further tier-conditional trim is
  honest is a real question and not a foregone one.

**Acceptance:** Washington Street's seven platted block faces carry the street edge by the
same rule, and all three tiers are inside their ceilings at all five stands at both
viewports — **without** raising a ceiling. If the run that takes this finds the 58,926
still unaffordable, that is a finding to write down, not a licence to re-base.

**Links:** T-0191 (parent) · T-0240 (Randolph, shipped) · T-0056 · T-0223 · T-0237 ·
T-0127 · `tools/generate_frontage_works.py` `EDGE_STREETS`.
