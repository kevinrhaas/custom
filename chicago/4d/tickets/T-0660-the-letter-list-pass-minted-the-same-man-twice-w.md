---
id: T-0660
title: The letter-list pass minted the same man twice when the paper printed his name in both orders, and the corrected reading now shows it
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The letter-list pass minted the same man twice when the paper printed his name in both orders, and the corrected reading now shows it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

The papers print a name in either order, and until T-0638 this pass read the LAST token
as the family name in both. So `Palmer N. H.` was minted under the surname `h` and
`N. H. Palmer` under `palmer`, and refusal 8 — one household per surname per pass —
never saw them as the same man. Both are in the town.

FOUND WHILE LANDING T-0638, by running the pass's own derivation with the corrected
reading and the old one side by side. With the fix in, 11 candidates the pass used to
accept are refused and 16 it used to refuse are accepted; the refusals are the
collisions the fault had been hiding. Named in that diff, among others:

| the pair | how the paper set it |
|---|---|
| `person_n_h_palmer` / `person_palmer_n_h` | given-first and surname-first, same initials |
| `person_wm_osborn` / `person_osborn_b` | ditto |
| `person_philo_c_mills` / `Mills Joel C.` | different men, but only one may hold `mills` |

**This is not a bug T-0638 introduced — it is one it revealed**, and the reason it was
left alone there is that closing it RETIRES RECORDS. A duplicate household removed is a
person removed from the town: the population counts move, the manifest moves, the
published mirror moves, and every ledger that ever ruled on the retired id has to be
told where the ruling went. That is a different unit of work from a rename, and it
needs the owner's ruling on one question first (below).

## What has to be settled before any of it

Which of a pair survives? The two records are not equal — one may carry a research row,
a crosswalk match or an 1840 bridge that the other does not — so `ticket.mjs` cannot
answer it and neither can a rule that just prefers the earlier id.

**Acceptance:** (state it before working)

1. The full list of pairs, derived (not hand-assembled) by running the letter-list
   pass's `mint()` against the committed tree and reporting every candidate refusal 8
   now catches that it did not before, with the two printings side by side.
2. A stated survivorship rule, applied by a tool, with the losing record RETIRED rather
   than deleted — the id kept resolvable, pointing at the survivor, because ledgers,
   crosswalks and the published mirror cite it.
3. The town's population counts move by exactly the number of pairs closed, and
   `index.json`'s counts, the manifest and the published mirror all move with them.
4. `bash tools/check.sh` green, and no record's grade moves in either direction.
