---
id: T-0379
title: The 716 letter-list names the post office printed in a single return, and the change of scale they put to the town
state: open
epic: PAPERS
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0374
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The 716 letter-list names the post office printed in a single return, and the change of scale they put to the town.

Piece 2 of 2 of **T-0374 — letter_list_only reaches the visitor's card, and the 1,536 names known only from the post office**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**THE MEASUREMENT, so this is a decision and not a survey** (taken on dev at 4e21389).
1,530 register persons carry `letter_list_only` with action `new_resident`. Through the
eight refusals `tools/mint_documented_residents.py` derives — garbled 415, surname already
minted 250, the town already names that family 101, placed outside the town 22, a surname
and nothing else 10, a firm 6 — **726 survive**, and T-0378 takes the ten of them the post
office printed in more than one return. **This ticket is the other 716.**

563 of them are printed exactly once, in one return of uncalled-for letters, with no
trade, no place and no second sighting. Minting them would take this town from 225 people
to 941 and its households from 189 to 905 — four residents in five would be a name on a
post-office list and nothing else, and the residents panel a visitor opens would be mostly
that.

**This is a question for the owner before it is work for a run.** His ruling of 2026-08-28
is that a letter-list name is enough to make somebody a resident, and this ticket does not
dispute it; what it cannot decide on its own is whether the reconstruction should HOLD all
716 as households, hold them in a lighter form the panel can carry, or hold the ranked head
of the list. `ticket.mjs block --owner` is the honest first move on it, with these numbers.

**Acceptance:** (state it before working — never weakened to pass)

- The scale question answered by the owner, in writing, before any record is minted.
- Then whatever he rules, derived by rule and gated by `--check`, occupation absent, and
  `town_census.json` moving additively.
