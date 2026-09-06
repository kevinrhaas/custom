---
id: T-0681
title: T-0666's Fort Dearborn lot crosswalk matches 11 bidders to residents and 3 of them are on no card: spend the lot sale onto the people it names
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: 2026-09-05
pr: 939
claimed_by: run 9/5/2026, 6:20:39 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-06T00:01:59.866Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33998306732
---

T-0666's Fort Dearborn lot crosswalk matches 11 bidders to residents and 3 of them are on no card: spend the lot sale onto the people it names.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Every one of the resident matches in `fergus_1839_lots_crosswalk_1835.json` carries, on
the person's OWN card, a paragraph naming the Fort Dearborn Addition sale of 10-24 June
1839: the bidder as printed, each bid's block and lot, its price, the printed page and the
claim id it was read into, the crosswalk's own identity rule, and the crosswalk's own
carry rule quoted rather than paraphrased. The volume's source id is in that person's
`sources`. TWO FIELDS MOVE AND NO OTHERS — no grade, no arrival, no placement, no
`present_on_scene_date` — held by a self-test that diffs a record through the applier and
asserts the changed key set. A ledger re-derives from the crosswalk, carries no
"crosswalk" in its name, and `check.sh` gates both directions: a ruling that stops
reaching its card, and a card that carries the paragraph with no ruling behind it.

The measure's second hop is the visible number: `directories` unwritten falls from 3 to 0.
It is deliberately NOT the whole of the acceptance, because the instrument reads a card's
citations at the HOUSEHOLD level, so 8 of these 11 already read "written" on the strength
of a different Fergus 1839 pass while the lot sale had reached nobody. The deliverable is
the paragraphs, not the counter.

The title says 11 because that is what the crosswalk held when the ticket was written. While
this was in flight T-0839's card merges landed on `dev` and folded 42 duplicate residents,
which settled four of the contested names; the crosswalk now declares 15 matches over 44
lots, and the pass writes whatever it declares rather than a number fixed in advance.
