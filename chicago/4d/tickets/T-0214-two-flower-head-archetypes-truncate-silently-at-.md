---
id: T-0214
title: Two flower-head archetypes truncate silently at their instance cap
state: claimed
epic: FLORA
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-26
closed: null
pr: null
claimed_by: run 8/28/2026, 2:55:45 AM CT
blocked_on: null
needs_bake: false
---

Found by T-0034 while measuring what bounds the bloom, and **not caused by it** — the same two
sets stand at their cap on the build before that ticket's raise as well as after.

`node tools/measure_bloom_headroom.mjs`, standing in every community at four bearings:

| set | worst stand | drawn / cap |
|---|---|---|
| `flora-head-spike` | `z10_settled_town`, facing 90° | **820 / 820** |
| `flora-head-dome` | `z06_dense_forest`, facing 0° | **820 / 820** |
| `flora-head-pompom` | `z06_dense_forest`, facing 90° | 804 / 820 |

`maybeHead` (`renderers/web/js/flora.js`) stops pushing the moment a set is full — `if
(!set.push(...)) return;` — so it truncates **mid-plant and without a word**: the placer deals
the head, the record asked for it, and the frame never draws it. Nothing reports it. The nine
head sets share nine separate `TUNE.cap.head` ceilings of 820 each and the aggregate is barely a
fifth spent at the worst stand measured, so the shortfall is an ALLOCATION, not a budget: two
sets are full while seven are nearly empty.

**Do not simply raise `TUNE.cap.head`.** The three routes worth measuring between are (1)
allocate the nine ceilings against measured per-set demand at a constant or lower TOTAL, which
buys the room out of a budget that already exists; (2) one head archetype set with a per-instance
shape, which removes the nine-way split entirely; (3) accept the ceiling and REPORT the
truncation, which is at least honest and is nearly free. Route 1 needs demand measured across
every community and every bearing before any number moves, because a cap tuned at three stands
and blown at a fourth is the defect this ticket is about.

**Acceptance:** a measurement across every community and four bearings shows **no head set at
its cap anywhere**, or the shortfall is reported by name and count where a reader can see it —
and the total head instance ceiling is not larger than it is today. `tools/measure_bloom_headroom.mjs`
already prints the table; its `--assert` run is the gate.

Related: T-0034 (the measurement that found it) · ROADMAP K58 (the same shape one stratum down:
a ceiling deciding how much of the evidence a visitor sees).
