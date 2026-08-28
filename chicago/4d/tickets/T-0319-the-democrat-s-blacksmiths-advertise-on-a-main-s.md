---
id: T-0319
title: The Democrat's blacksmiths advertise on a Main-street the plat does not carry, twice, five months apart
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Two blacksmith advertisements in the *Chicago Democrat*, five months and two proprietors
apart, place their shops on a street the 1830 plat of Chicago does not have.

- **1834-04-01**, page 3 column 6 — "M[AT]THIAS MASON & [Co.] … various branches, on
  Main-stre[et,] opposite Graves' Tavern", on copy dated 26 November 1833
  (T-0313, `extracted/chicago_democrat_1834_04_01.json` c004).
- **September 1834** — a blacksmith "on Main-street, opposite the Tremont House"
  (T-0291, recorded in that pass and in changelog v347).

One instance is OCR damage. Two, in the same paper, in the same trade, with different
anchors and different proprietors, is a usage. `data/streets.json` has no Main Street and
neither does the plat this reconstruction is built on, so one of three things is true and
the project does not currently know which:

1. the Democrat's compositors called some platted street Main in ordinary speech, and the
   claims should carry a `merge_rule`-shaped note saying which one;
2. both shops stood outside the platted town, where a local name could stand unopposed;
3. both readings are the same OCR confusion twice — in which case say what the underlying
   word is, because "Main" is not close to "Lake", "Water", "Kinzie" or "Canal".

## Acceptance (one demonstration)

- Every "Main-street" occurrence in the corpus is enumerated with issue, page, column and
  line — a sweep, not two examples.
- ONE of the three readings above is settled against evidence, or the ticket is closed
  `blocked --owner` with the question stated. A guess recorded as a finding is a fail.
- Whatever is concluded lands in the affected claims' notes and, if it is a liberty,
  in `docs/LIBERTIES.md`. No confidence is upgraded to make the street exist.
