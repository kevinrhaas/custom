---
id: T-1029
title: consolidate_town_cards.py --apply overwrites a survivor's merged_from, so a card folded onto twice forgets the first fold
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-11
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

consolidate_town_cards.py --apply overwrites a survivor's merged_from, so a card folded onto twice forgets the first fold.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`tools/consolidate_town_cards.py --apply` writes a `merged_from` block onto the survivor
naming the ticket, the rule and the cards folded. It writes the LAST ruling it lands, not the
union of them, so a survivor that has been folded onto twice loses the record of the first fold
from its own card.

**FOUND BY T-1026**, landing the second fold onto `beaubien_madore`. Before that pass the card
read `ticket: T-1002, rule: C11, cards: [beaubien_medore_b]`; after it, `ticket: T-1026,
rule: C12, cards: [beaubien_medard]`. Both folds happened and both are true, and a reader of
that card now learns only the second. The block's own note says it is "THE UNION OF THE CARDS
THIS PERSON WAS SPLIT ACROSS" and the `cards` field is an array, so the shape already expects
more than one — the writer does not fill it.

**NOTHING IS LOST FROM THE DATASET.** `index.json`'s `merged` table carries both rows whole,
each with its own person, household, record file, rule, cluster and ticket, and both folded
records stand under `data/residents/merged/`. The rulings themselves are in
`card_merge_rulings.json` under the cluster. So this is a defect in what a CARD says about
itself, not a hole in the layer, and no gate catches it because every gate reads the table.

**Acceptance:**

- `--apply` writes `merged_from` as the union of every landed ruling whose survivor is this
  card: the cards list holds all of them, and the ticket and rule are carried per fold rather
  than as one pair that only the last ruling can be right about.
- `hh_beaubien_madore.json` names both T-1002/C11 and T-1026/C12 after a re-run, and no other
  survivor's block changes except the ones that are genuinely multi-fold — say how many there
  are, because a survivor folded onto twice is rare and the count is the size of the repair.
- A self-test that lands two rulings onto one survivor and refuses a block that names one.
- `bash tools/check.sh` green. No bake.
