---
id: T-1011
title: Mint the 57 printed lines of the 1 January 1834 return no claim reaches, and reconcile the 14 cohort cards no printed line reaches
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

Mint the 57 printed lines of the 1 January 1834 return no claim reaches, and reconcile the 14 cohort cards no printed line reaches.

Piece 2 of 3 of **T-1008 — The ninety-two lines of the 1 January 1834 letter list the crops never carried are read but unminted, and the 97 residents minted from it are a floor of a 170-name return**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Every one of the **57** printed lines the T-1010 crosswalk reports untied is either
  matched to an existing minted resident of this cohort, or minted under owner ruling 1
  carrying `letter_list_only`, with the roster line as its source.
- The **14** cohort cards the crosswalk reports as reached by no printed line are
  reconciled — `hh_crisey_william` first, whose family name the image itself corrected to
  Crissy, so no rule comparing surnames can see the card and the line as one man.
- The count the cohort's own package states is the printed 170 and what reached a card.
- The crosswalk's counts move as a RESULT of this run, and `check.sh` re-derives them.

**The blocker to size for before claiming.** `mint_letter_list_residents.py --check`
reports 772 files drifting from what the pass derives (a pre-existing condition T-0660
measured and check.sh does not gate). Minting cannot be done by re-running the pass in
write mode without also landing that 772-file rewrite, which is a different unit. Decide
the route — targeted mint, or land the drift first — before claiming.

**Links:** T-1008 (parent) · T-1010 (the crosswalk this reads) · T-0299 · T-0310 · T-0424
