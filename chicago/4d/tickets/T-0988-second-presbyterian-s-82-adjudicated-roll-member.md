---
id: T-0988
title: Second Presbyterian's 82 adjudicated roll members reach 82 cards and not one card cites the roll: spend them, and drop church's write ceiling back to zero
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Second Presbyterian's 82 adjudicated roll members reach 82 cards and not one card cites the roll: spend them, and drop church's write ceiling back to zero.

**Acceptance:** every card named by a `matched` row of the Second Presbyterian crosswalk cites the roll, and the gate reports church at 0 unwritten with the ceiling tightened to 0.

**Measured on this branch, 2026-09-10, landing T-0962.** With the second hop widened to read
the `matched` container, church entered the report for the first time: **82 reached, 82
judgeable, 0 on a card, 82 unwritten**. Independently confirmed — `grep -r
second_presbyterian_chicago_1892 data/residents/` returns **nothing**. Not one resident record
in the town cites the roll, so this is the whole debt, not a sample of it.

**What the rulings are.** The crosswalk adjudicates the 1892 printed roll of the Second
Presbyterian Church against the residents layer, filing 82 as `matched`, 37 as `ambiguous` and
330 as `refused`. Only the 82 are a spend — a rival still standing is not a ruling to spend,
which is the line MATCH_CONTAINERS draws and this ticket must not cross. Each matched row
carries `person_id`, `household_id`, `grade`, its `rule` (the reasoning that got it there) and
`roll_lines[]` with the printed line as read, the admission date, how admitted and the printed
page.

**The caution this one needs, and it is the whole difficulty.** The roll is an **1892**
printing and its admission dates run decades past the scene — `second_presb_0371` is admitted
27 April **1859**. An 1859 admission is not 1835 evidence and may not move a grade or mint
anybody; the ladder T-0505 ratified binds here exactly as it binds an 1840 head.
`tools/spend_census_1840_heads.py` is the shape to copy: two fields, no grade moved, the limit
quoted in the card's own words rather than paraphrased, `--check` and `--self-test` gated in
the same commit so the pass re-derives and cannot drift.

**Links:** T-0962 (widened the hop and found this) · T-0698 / `tools/spend_census_1840_heads.py`
(the same debt paid on census_1840, and the pattern) · T-0700 (a paragraph present and no
longer true is the failure that looks like success) ·
`tools/research_spend_baseline.json` § `raised` (the entry recording the 82).
