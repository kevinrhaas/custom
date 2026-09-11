---
id: T-1012
title: The firm rule reads an ampersand as a partnership, so it refuses Lamira & Laura Carrier: two residents the owner's ruling 1 admits and the mint pass cannot hold
state: open
epic: PAPERS
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-1008
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The firm rule reads an ampersand as a partnership, so it refuses Lamira & Laura Carrier: two residents the owner's ruling 1 admits and the mint pass cannot hold.

Piece 3 of 3 of **T-1008 — The ninety-two lines of the 1 January 1834 letter list the crops never carried are read but unminted, and the 97 residents minted from it are a floor of a 170-name return**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

`mint_letter_list_residents.FIRM` is `&| and |\bco\b|\bcompany\b`. It refuses all three
lines of the 1 January 1834 return that are not one person — and only two of them are
firms:

    131  Axtel & Steele          firm         refused, correctly
    163  Jesse B. Winn & Co.     firm         refused, correctly
     36  Lamira & Laura Carrier  two_people   refused, and they are two residents

The roster names the distinction itself in `printed_length`
(`addressee_lines_that_are_firms` vs `addressee_lines_naming_two_people`), so the
information needed to tell them apart is committed; the pass does not read it.

**Acceptance:** (state it before working)

- Lamira Carrier and Laura Carrier either reach the town, or are refused for a stated
  reason that is not "the line contains an ampersand".
- Whatever rule admits them is general: it does not special-case this line, and it still
  refuses `Axtel & Steele` and `Jesse B. Winn & Co.`.
- Refusal 8 (one household per surname) is faced explicitly — two sisters at one surname
  is exactly what that rule exists to prevent, and this is the case that tests it.
- The T-1010 crosswalk's `mint_refuses_as_firm` for line 36 changes, and the gate sees it.

Whether two women sharing one addressee line are one household or two may be the owner's
call rather than this loop's; `block --owner` if so.

**Links:** T-1008 (parent) · T-1010 (where this was found) · T-0379 (ruling 1)
