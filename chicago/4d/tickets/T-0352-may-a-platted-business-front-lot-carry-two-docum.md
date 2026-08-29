---
id: T-0352
title: May a platted business-front lot carry TWO documented storefronts, or only one — the clause was widened for South Water and Dearborn and the owner has not ruled on the plural
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

**A question for the owner, and the work is already merged under one answer to it.**

His clause of 2026-08-27, in `tools/plat_occupancy.py`'s docstring: *a platted
business-front lot is not exhausted by a researched building standing at the
street on it* — so a documented store at the frontage and the block's anonymous
dealt roof behind it may share the lot. Three conditions were stated and are
unchanged: the face is a declared business front, the building is researched
rather than invented, and it stands AT the street.

The code carried a **fourth**, unstated in the ruling and written as
`len(holders) != 1`. Its purpose is in its own comment: catch the anonymous RUN
standing on the lot, which the schedule sees (it excludes nothing) and the
generator does not (it excludes its own records). It also caught, silently, a
case nobody had produced: **two documented storefronts on one business-front
lot.**

T-0306 produced it. `blk_south_water_dearborn` lot 0 carries
`chicago_american_office` at the Dearborn corner and now `john_holbrook_store`
one door east of it, both researched, both at the street. Under the old test the
lot read as exhausted and the block's own dealt frontage roof died with `lot 0
already carries chicago_american_office`.

T-0306 widened the fourth condition to **every** holder on the lot being a
researched building at the street, on the reading that the ruling says a
business-front lot is not exhausted by a researched building standing at the
street on it and does not say *one and only one*. An anonymous holder still
takes the lot, which is condition 2 and is untouched. Nothing physical was
relaxed: the footprints still may not overlap, still clear each other by three
metres, still stand inside their own lot lines by the lot margin.

**That reading may be wrong, and it is his call, not a run's.** The alternative
is that a business front carries one documented storefront and the second one
takes the lot — in which case `blk_south_water_dearborn` gives a roof back and
the code returns to `len(holders) != 1`.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The owner is asked, in one sentence, whether a platted business-front lot may
  carry more than one documented storefront at the street and still be dealt its
  anonymous roof.
- Whichever way he answers, `tools/plat_occupancy.py`'s docstring carries the
  ruling verbatim beside the 2026-08-27 one, and the fourth condition matches it.
- If he says one only: `john_holbrook_store` stays where the evidence puts it and
  `blk_south_water_dearborn`'s frontage run loses a roof to the block's headroom,
  measured and recorded, not nudged.
