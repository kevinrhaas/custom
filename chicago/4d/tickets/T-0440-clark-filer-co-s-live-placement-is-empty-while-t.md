---
id: T-0440
title: Clark, Filer & Co.'s live placement is empty while three printings put its warehouse five doors east of Randolph
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-30
closed: null
pr: null
claimed_by: run 9/4/2026, 5:43:52 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33926203781
---

Clark, Filer & Co.'s live placement is empty while three printings put its warehouse five
doors east of Randolph.

Found by T-0384's corpus sweep (`tools/measure_corner_ordinals.py`, which reports it every
time it runs). The gazetteer holds three placement readings for `business_clark_filer_co`,
and the middle one — printed 1834-06-11, 1834-06-18 and 1834-07-02 — reads

> "their ware house on South water St. five [doors east] of the corner [of Randolph st.]"

with `class: relative`, an anchor of *the corner of Randolph st.* and `street: South Water
Street`. That is an ordinal off a corner in the exact shape `docs/CORNER-ORDINAL.md` was
written for, and under the owner's ruling of 2026-08-30 it places.

**It never reaches the register.** `business_clark_filer_co`'s LIVE placement is
`{"class": "none"}` with `street: null`, so `compile_register.resolve_anchor` is handed no
anchor at all and the row reads `action: unplaceable`, *"The paper gives no anchor."* The
house is present at the scene date and is not excluded — it is unplaceable only because the
live placement is empty while three of its own printings are not.

So the fault is in how the gazetteer chooses a business's live placement, not in the
register's reading and not in this corpus. `tools/compile_gazetteer.py` ranks placement
classes `none < street_only < relative < corner` and a `relative` reading should beat a
`none` one; something else is choosing here, and whatever it is may be choosing for other
houses too — the first thing this ticket owes is a count of how many.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Why the live placement is `none` when a `relative` reading exists is stated, with the
  code path named, and the count of OTHER businesses in the same position is measured
  rather than assumed.
- Either the live placement resolves to the printings' own anchor and Clark, Filer & Co.
  stops reading `unplaceable`, or the reason it may not is written down and the ticket is
  blocked on it — never a silent narrowing.
- Whatever changes, `tools/measure_corner_ordinals.py`'s sweep and the register both
  re-derive green, and the gazetteer's own self-test carries the case.

**Related:** T-0384 (the ruling and the sweep that found this) · `docs/CORNER-ORDINAL.md` ·
T-0306 (the storefronts programme).
