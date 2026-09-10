---
id: T-0998
title: The land-sale crosswalk keys the purchaser on an exact surname, so T-0842's ruled merge made VANDERBOGERT invisible to it and orphaned a written ruling
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

The land-sale crosswalk keys the purchaser on an exact surname, so T-0842's ruled merge made VANDERBOGERT invisible to it and orphaned a written ruling.

**Found by T-0842, 2026-09-10.** `build_resident_crosswalk()` in `tools/read_land_sales.py`
proposes a purchaser onto a resident by ONE mechanical rule, and the first clause of it is
that the surname agrees exactly. T-0842 ruled that the town's `Vanderbogert, Henry` (the 1833
tax list) is Dr Henry Van der Bogart and folded the card onto `vanderbogart_henry`. The
register's two rows — `VANDERBOGERT HENRY` and `VANDERBOGERT JOHN AS` — now match nothing at
all: the crosswalk refuses both with "the residents layer holds nobody of the surname", which
is true of the string and false of the town. A written adjudication went with them: T-0850's
refusal of `VANDERBOGERT HENRY` became a ruling on a proposal nobody makes, and `--check`
calls that "a ruling on nothing", so it is parked in `resident_rulings.json`'s new
`withdrawn` list with the reason.

**The shape of the defect.** A ruled merge is supposed to make the town's knowledge of a
person BETTER, and here it made one source's view of him worse. The residents layer now
carries the spellings a card was folded FROM — `index.json`'s `merged` table names each one —
so the crosswalk has everything it needs to keep proposing; it just does not look. The same
blindness will fire on every future merge across a spelling.

**Acceptance:** the land-sale crosswalk resolves a purchaser surname through the folded
spellings as well as the standing ones (`index.json` `merged`, or `tools/folded_residents.py`
which T-0842 added for the frozen cohorts), the two `VANDERBOGERT` rows are proposed again
against the one Van der Bogart the town holds, T-0850's parked refusal is restored to `ruled`
and RE-READ rather than reinstated unchanged — one of its two grounds is gone and the other
stands — and no proposal that the exact-surname rule made before this change is lost or
altered.
