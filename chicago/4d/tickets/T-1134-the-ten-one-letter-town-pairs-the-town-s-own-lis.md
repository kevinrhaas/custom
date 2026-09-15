---
id: T-1134
title: The ten one-letter town pairs the town's own lists print with no anchor on either card
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-1130
opened: 2026-09-14
closed: null
pr: null
claimed_by: run 9/15/2026, 1:42:28 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34937778308
---

The ten one-letter town pairs the town's own lists print with no anchor on either card.

Piece 3 of 3 of **T-1130 — Nineteen town cards stand one letter apart in the surname and identical in the forename, and the merge machinery has never been shown one of them**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

## The ten, named before the work, on the repository's own test

`tools/surname_one_letter_away.py` § `town_pairs` joins the cards one letter apart in the
surname and identical in the forename. T-1132 drew the split's line with
`consolidate_town_cards.anchored()` — the three pairs a card DOCUMENTS went first — and the
seventeen left divide on the mint that put them there, which is the card's own
`source_pass`. Where BOTH cards are `letter_list`, the post office alone prints the pair:
those are T-1133's. Where the town's own rolls print one of them — a `civic` card, minted
off the IRAD poll and tax lists — the pair is this ticket's. Intersected with the nineteen
T-1130 counted, that is exactly ten:

```
  Clark Anight / Clark Knight            A O T Bread / A O T Breed
  John W Eldredge / John W Eldridge      William Forsyth / William Forsythe
  Paul Kingston / Paul Kingstone         William Paine / William Payne
  Stephen M Salsbury / Stephen M. Salisbury
  Isaac Scarrett / Isaac Scarritt        E L Trall / E. L. Thrall
  Charles Wesencraft / Charles Wessencraft
```

(The same test also joins `John L Wilton / John Wilson`, a pair T-1130 did not count
because the surnames are two letters apart at the stem it folds. It is not taken here.)

## Acceptance

1. Every one of the ten carries a written ruling in `data/residents/card_merge_rulings.json`
   — `merge` under a named C-rule, or a refusal that says what keeps the two apart. None is
   left silent, and **none is ruled on the one-letter distance alone**: C9's load-bearing
   clause is a page that demonstrates the variation, and a pair with no such page is refused
   and says so.
2. The page question is ASKED OF THE CORPUS AND NOT OF THE READER'S MEMORY: every deposited
   text this project holds — the IRAD poll and tax rolls, the 1833-1835 newspaper run, the
   land register, Fergus 1839 and 1843, Norris 1844, the books, the church and old-settler
   lists — is searched for both spellings of each stem, and the ruling quotes what that
   search returned, including when it returned nothing.
3. A merge takes the survivor the existing rules pick and states what each card knew. The
   town's person count moves by exactly the number merged and the PR says the number.
4. `./tools/check.sh` green, the chain iterated to a fixed point behind any merge.
