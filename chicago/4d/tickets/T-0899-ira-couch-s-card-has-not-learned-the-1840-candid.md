---
id: T-0899
title: Ira Couch's card has not learned the 1840 candidate ruled onto him: spend it, and drop the write-hop ceiling back to zero
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Ira Couch's card has not learned the 1840 candidate ruled onto him: spend it, and drop the write-hop ceiling back to zero.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Left by T-0714, 2026-09-06, deliberately and with the ceiling raised by exactly one.**
Re-deriving `crosswalk_census_1840_heads.py` put 290 previously unadjudicated named heads
through the ladder. One of the rulings reaches a town person whose card cites no 1840
source at all: **Ira Couch**, printed page 211 line 3 of image `33SQ-GYYJ-97P`, read
`Ira Couch` at `high` name confidence, ruled **L7 candidate** — full forename and surname
agree, the name is unique on both sides, and nothing independent of the name was found to
hold the pair together.

`measure_research_spend.py --gate`'s second hop caught it: *1 ruled onto a person whose
card has not learned it*. T-0714 raised `unwritten_ceiling.census_1840` from 0 to 1 with
that reason recorded, rather than writing the card itself, because
`crosswalk_census_1840_heads.py` mints nobody and writes no household file by design —
proposing is its job and applying is `apply_census_1840_bridges.py`'s, under T-0515.

**A candidate must stay a candidate.** Ira Couch is `attested` in 1835 and the 1840 line
carries no discriminator independent of the name, so nothing here promotes anything: what
his card should learn is that a named 1840 head of this name stands at that locator and
has not been joined to him, with the rule that says why. The other ten candidate rulings
in this crosswalk already reach cards that cite the source; this is the one that does not.

**Acceptance:** Ira Couch's card carries the 1840 candidate as a candidate, with the
reading as printed, the locator (image, printed page, line) and the rule that fired; no
grade moves; `measure_research_spend.py --gate` green with
`unwritten_ceiling.census_1840` back at **0**, dropped in the same commit; `bash tools/check.sh` green.
