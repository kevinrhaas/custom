---
id: T-0114
title: The road-legibility gate is red from mid-distance, and no run had reached it since it turned
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-20
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The road-legibility gate is red from mid-distance, and no run had reached it since it turned.

Found by T-0060's staged smoke, 2026-08-20, on the published mirror at 390x780 — and
corroborated three ways: the same two checks fail with the T-0060 machinery, without it
(a pre-split filtered run), and the 2026-08-18 full-run kill already reported "208
passed / 2 failed" without ever printing which two. The suite simply died before the
road bands for long enough that nobody saw them turn.

The failing pair, with R-BUG2's own numbers:

- **from the walker's eye, down an open street** — the 100-250 m band reads ΔL* 1.8 of
  the 3.2 its opacity earns, 33 % perceptible of 42 bare probes, weber 0.0795 over
  ground L* 49.8. The near bands pass (2-40 m: 90 % perceptible; 40-100 m: 80 %).
- **from the air, at the aerial anchor** — the 250-600 m band reads ΔL* 2.1 of 4.6,
  49-51 % perceptible of 182 bare, weber 0.093 over ground L* 49.5.

Desktop confirms both (unfiltered reference run 32346862982, 2026-08-20): the walker's-eye
check reads ΔL* 3.4 of 4.5 opaque, 70 % perceptible in its near band, and the aerial
check fails its gated bands the same way. This is the town, on both widths.

The recent ground work is the suspect pool (the bands that fail are exactly the
mid-distance reaches the bank regrades and road-panel splitting touched: T-0110's
curved-bank panel subdivision, T-0046/T-0004's approach earthworks and fort-mound
regrade) — but R-BUG2's own history warns that "measure before choosing" refuted its
prime suspect once already. Read its box in docs/ROADMAP.md before deciding anything.

**Acceptance:** the failing bands are diagnosed with the R-BUG2 measurement (which
build turned them, and why), the repair restores every gated band over its bar without
touching the bars themselves, and both road checks pass in the affected stages
(`SMOKE_STAGE=3`, both viewports) and in the unfiltered workflow run.

**Re-measured by T-0074, 2026-08-20:** both checks fail with the same numbers on the
dooryard-plantings branch — walker 100-250 m band ΔL* 1.8 of 3.2, 33 % of 42 bare,
weber 0.0795; aerial 250-600 m ΔL* 2.1 of 4.6, 53 % of 182, weber 0.0922. The dooryard
stems change neither count nor contrast (probes under flora are excluded by the gate
itself), so this stands exactly as found.
