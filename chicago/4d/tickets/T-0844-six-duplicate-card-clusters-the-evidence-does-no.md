---
id: T-0844
title: Six duplicate-card clusters the evidence does not decide: Hunt, Kennicott, Saunders, Walker, T. Temple and John S. Kinzie
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

Six duplicate-card clusters the evidence does not decide: Hunt, Kennicott, Saunders, Walker, T. Temple and John S. Kinzie.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Raised by T-0839**, which folded 42 duplicate town cards onto the people they name and
ruled every candidate cluster in writing. Six pairs it declined to rule, because the
evidence genuinely does not decide and a merge is not reversible by the next reader's
opinion. Each is written onto both cards as a `merge_ruling` block with
`verdict: undecided` and `referred_to: owner`, and the reasoning is in
`data/residents/card_merge_rulings.json`. Ruling one is a sentence; ruling all six is one
run, and the merges then land through `tools/consolidate_town_cards.py --apply`.

| cluster | the two cards | for the merge | against it |
|---|---|---|---|
| `hunt-c` | `hunt_c_s` (C S Hunt) · `hunt_charles_cotesworth_pinckney` | both printed in Chicago papers seventeen days apart in August 1835; the only Hunt forename beginning C | middle initial S against C, and neither card documents the man beyond a list and a death notice |
| `kennicott` | `kennicott_w_l` · `kennicott_william_h` | uncommon surname, no third bearer in the town | middle initials L and H disagree; no anchor on either side |
| `saunders` | `saunders_william_s` · `saunders_william_w` | both in the Democrat; Saunders is not common here | middle initials S and W disagree; one is letter-list only, the other a press mention |
| `walker-george` | `walker_george_e` · `walker_george_h` | both Georges in the Democrat; no third Walker | middle initials E and H disagree; no anchor |
| `temple` | `temple_t` (T Temple) · `temple_john_t` | 'T. Temple' in the Democrat of 3 Dec 1834 is most probably Dr John Taylor Temple with the first initial dropped | T matches neither Temple forename — the town's two are John and Peter — and no rule in this project attaches a card whose only forename token is a MIDDLE initial |
| `kinzie-john` | `kinzie_john_s` · `kinzie_john_h` | John Harris Kinzie is the town's only John Kinzie in 1835 | middle initial S against H, on the one surname T-0839 warns about: four Kinzie men stand on the cards and this project has mis-folded a Kinzie once already (T-0732) |

Rule C4 in the rulings file — *a contradicted middle initial, over an anchor* — would fire
on Temple and Kinzie and is withheld on both for a stated reason. Hunt, Kennicott, Saunders
and Walker fail C4 outright: there is no anchor, so nothing says which printing is the
mis-set one.

**Done when** each of the six carries a MERGE or a DISTINCT ruling in
`data/residents/card_merge_rulings.json`, the merges are landed, and the gate
`tools/consolidate_town_cards.py --check` is green with no card left undecided-to-owner.
