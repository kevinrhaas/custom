# The consolidation passes — the ledger of the series

A consolidation pass takes the rulings CLOSED SINCE THE LAST PASS and writes them onto the
cards they name. It reads nothing new. The series exists because of an instruction the
owner gave on 2026-09-03 — *"dont land those tickets at the very end maybe every few you
should do that consolidation"* — and it is a numbered series (T-0634, T-0635, T-0636)
rather than one recurring ticket because a `done` ticket cannot be re-claimed.

**This file is the starting line for the next pass in the series.** Each entry says what
its window was, which crosswalks it consumed, which it skipped as already spent, and what
the two hops of `tools/measure_research_spend.py` read before and after. A pass that finds
nothing newly closed writes an entry saying so and costs a run almost nothing; that is the
design, not a failure.

The two hops, and they are different questions:

* **Hop 1 — read vs ruled.** Of the units a domain has READ, how many has anything ruled
  on? A source volume read and never adjudicated is unspent.
* **Hop 2 — ruled vs on a card.** Of the rulings that NAME A PERSON IN THIS TOWN, how many
  reached that person's card? A ruling that never leaves `data/research/` is a ruling a
  visitor cannot see.

---

## Pass 1 — T-0634, 2026-09-04

**Window:** everything closed after T-0513 (2026-09-03T22:01Z) up to dev at `80330dc7`.
Fifty tickets closed in that window.

**Consumed:** `data/research/civic/voter_crosswalk.json` — the four early Chicago lists
(the 1833 trustees' poll, the 1833 tax list, the 1834 poll, the 1835 poll), 345 entries,
99 of them matched to people this town holds and NONE of the 99 written onto a card. The
pass is `tools/spend_civic_voter_lists.py`; its ledger is
`data/research/civic/voter_spend_1835.json`.

**Skipped as already spent:** `data/research/directories/` — T-0632 spent all four
directory crosswalks the same morning and hop 2 already read 235 reached / 235 written / 0
unwritten for that domain. `data/research/census_1840/resident_crosswalk.json` — nine of
its ten rulings were already on their cards, and the tenth (John H. Kinzie) is closed by
this pass as a consequence rather than by a separate write: his record now cites
`chicago_voter_lists_1833_1835_irad`, which is one of the four sources that ruling rests
on, and the instrument's test is whether the card learned ANYTHING from the ruling.

**Skipped as not a ruling about a person:** every domain whose crosswalk holds only
refusals and pass notes — church, books, land_sales, newberry_index, and civic's own
`crosswalk.json` (90 refusals, 2 passes). A refusal names no person to write to. These are
hop-1 work and belong to the spend tickets (T-0514, T-0515, T-0609, T-0633), not here.

### Hop 2 — ruled onto a town person, and whether their card learned it

| domain | reached | before: on a card | after: on a card | before: unwritten | after: unwritten |
|---|---|---|---|---|---|
| civic | 99 | 0 | **99** | 99 | **0** |
| census_1840 | 10 | 9 | **10** | 1 | **0** |
| directories | 235 | 235 | 235 | 0 | 0 |
| **TOTAL** | **344** | **244** | **344** | **100** | **0** |

**Every ruling in this project that names a person in this town is now on that person's
card.** The `unwritten_ceiling` for civic and census_1840 is tightened to 0 in
`tools/research_spend_baseline.json`, so it cannot regrow silently.

### Hop 1 — read vs ruled

Unmoved, and unmoved on purpose: this pass reads nothing and adjudicates nothing, so it
cannot spend a unit. Measured either side of it the totals read `16,322 read · 4,553 spent
· 11,769 unspent · 502 id pairs`, unchanged. (T-0664 merged into dev while this pass was
in flight and added 765 directory claims of its own, so the totals a later reader measures
will be larger; the figure this entry holds is the pass's own delta, which is zero.) Hop 1
is what T-0514, T-0515, T-0609, T-0610 and T-0633 move.

### What the layer looks like after it

The defect T-0513 measured was *breadth of citation*: how many sources a household record
rests on. Counted across all 848 household records:

| distinct sources cited | before | after |
|---|---|---|
| 1 | 664 | **656** |
| 2 | 71 | 71 |
| 3 | 45 | 41 |
| 4 | 46 | 44 |
| 5 | 19 | 23 |
| 6 | 3 | **11** |
| 7 | 0 | **2** |

Eight households come off a single source. The movement is concentrated at the top of the
table rather than the bottom, and that is what a voter roll would predict: the men who
stood at a town election are the men the rest of the corpus already names, so the roll
mostly deepens records that were already several sources thick. The 656 that still rest on
one source are the letter-list people, and they are T-0515's.

**Grades changed by this pass: 0.** The ratified ladder is applied by T-0515 against every
source at once; a pass that wrote the evidence and graded off it in the same breath would
be marking its own work.
