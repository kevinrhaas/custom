---
id: T-0991
title: Eight cards assert an 1835 trade out of a PRE-scene printing, and T-0693's later_occupation pointer cannot hold one: blank the field, or regrade it reconstructed?
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0872
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

T-0872's title reads "a later trade", and the population it names no longer is one. Five of
its eight — the Fergus 1839 cards — were repaired by other work between 2026-09-06 and
2026-09-10, and the audit T-0994 landed
(`python3 tools/audit_scene_window_trades.py --report`) shows what is actually left. Every
remaining row fails T-0837's rule from the OTHER side: the cited volume is about a year
BEFORE the scene, not after it.

| person | 1835 trade, at `attested` | cited | that source's `describes_date` | verdict |
|---|---|---|---|---|
| `elston_daniel` | soap_and_candle_maker | Democrat, 26 Nov 1833 | 1833-11 | pre_scene_printing |
| `goss_o` | saddler | Democrat, 26 Nov 1833 | 1833-11 | dissolved_before_the_scene |
| `harmon_charles_l` | dry_goods_merchant | Democrat, 26 Nov 1833 | 1833-11 | firm_in_window_trade_not_printed |
| `harmon_isaac_d` | dry_goods_merchant | Democrat, 26 Nov 1833 | 1833-11 | firm_in_window_trade_not_printed |
| `hathaway_joshua` | forwarding_and_commission | `hathaway_1834` (a MAP) | 1834 | trade_read_from_a_map |
| `jones_benjamin` | grocer | Democrat, 26 Nov 1833 | 1833-11 | pre_scene_printing |
| `kimball_walter` | dry_goods_merchant | Democrat, 26 Nov 1833 | 1833-11 | pre_scene_printing |
| `mason_matthias` | blacksmith | Democrat, 26 Nov 1833 | 1833-11 | pre_scene_printing |

The reasoning behind each verdict is written per row in
`data/research/residents/scene_window_trade_audit.json`, out of the newspaper register's own
compilation of the corpus — for each firm, the last issue that prints it.

**WHY THE PARENT'S REMEDY CANNOT BE EXECUTED HERE.** T-0872 says an unrepairable row is
"moved to the `occupation.later_occupation` pointer T-0693 mints, leaving the 1835 field as
`none_recorded`". That pointer is derived, wholly and only, from the record's own
`directories` block — a directory of 1839, 1843 or 1844 — and it says in its own note "a
trade is recorded for {year}". There is nowhere in it to put a trade printed in November
1833, and writing one there would assert the exact back-projection T-0693 exists to refuse,
in reverse. The parent's second arm has no mechanism behind it for this population.

**THE QUESTION, and it is the owner's because either answer changes what a visitor sees.**

  a. **Blank and point.** 1835 field to `none_recorded`, and mint the symmetric
     `occupation.earlier_occupation` pointer carrying the pre-scene trade and its year.
     Faithful to the parent's letter and to T-0837's rule. It takes eight trades out of the
     town's 1835 layer — a blacksmith, a saddler, two dry-goods houses, a grocer, a soap
     and candle manufactory — and out of everything downstream that reads
     `occupation.value`. It also needs a new key declared to
     `tools/measure_layer_reads.py`, which refuses an unread figure.

  b. **Regrade and say so.** Keep the value, move `attested` to `reconstructed`, keep the
     pre-scene issue cited, and write the carry-forward and its last-printed date into the
     note. `reconstructed` is this dataset's word for a figure the reconstruction supplies
     rather than a source, and `synthesize_resident_research.py`'s own overwrite guard
     already treats a `reconstructed` trade as an empty field — so the machinery for this
     answer exists and needs nothing new. The town keeps its blacksmith and the card stops
     claiming a printing it does not have. It diverges from the parent's written acceptance,
     which is why a run should not simply choose it.

`goss_o` may not want either: the Chicago American of 8 June 1835 prints the DISSOLUTION of
Goss & Cobb over copy dated 18 February 1835, four months before the scene date, and the
newspaper register already reads `business_goss_cobb` as `present_at_scene_date: false`. A
card asserting that trade at `attested` for July 1835 is contradicted by the corpus rather
than merely unsupported by it, and that is a repair rather than a grading question.

**Acceptance:** the owner's rule is recorded, and all eight rows leave
`tools/audit_scene_window_trades.py --report` under it. The gate T-0994 wired into
`check.sh` is what proves it: the ledger may only fall.

**Links:** [[T-0872]] (the parent) · [[T-0994]] (the audit and the one row the corpus
decided) · [[T-0837]] (the write gate) · [[T-0693]] (the later-trade pointer).
