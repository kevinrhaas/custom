---
id: T-0854
title: Andreas makes John Miller the brother of 'Samuel, the landlord' and the town holds a Samuel Miller card nobody has ruled identical to him
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Andreas makes John Miller the brother of 'Samuel, the landlord' and the town holds a Samuel Miller card nobody has ruled identical to him.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0734**, the pass that wrote the kinship the sources already state.

Andreas prints the tie outright, in `hh_miller_john/persons[0]/occupation/note`:

> John Miller, brother of Samuel, the landlord, came in 1831, and run a tannery just
> north of Miller's tavern.

The town also holds `miller_samuel` in `hh_miller_samuel` — but that card was minted from
the 1832 muster, the 1833-1835 newspapers and the 1833 tax list, and it claims no trade,
no tavern and no family. John Miller's own record still says his brother "is not written
as a household here", which was true when it was written and is not true now.

So the RELATIONSHIP is documented and the far END is a card nobody has ruled identical to
Andreas's man. T-0734 declined to land the kin row for exactly that reason: five Millers
stand in this dataset, and a family tie is not the place to settle an identity by
assumption.

**Acceptance:** the identity of Andreas's "Samuel, the landlord" against the card
`miller_samuel` is RULED — upheld with its reasoning and its sources, or refused with
them — under the crosswalk's own rules and not this pass's; if it is upheld, the
reciprocal `brother` kin rows are written onto both records and
`tools/harvest_stated_kinship.py` carries the ruling so its worklist stops saying
`not_supported`; if it is refused, the reason is written where the next reader of that
sentence will find it. `hh_miller_john`'s stale "is not written as a household here"
is corrected either way.

**Links:** T-0734 (found it, and holds the reasoning) · T-0597 (the kin row).
