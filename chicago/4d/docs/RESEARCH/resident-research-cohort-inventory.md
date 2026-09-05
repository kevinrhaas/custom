# Resident-research cohort inventory

Updated 2026-09-02 after PR #625 (fifth cohort) landed.

## Covered or reserved

| Cohort | Ticket / PR | Count | State |
|---|---:|---:|---|
| Pilot | T-0442 / prior merged pass | 75 | covered |
| Pass 2 | T-0462 / PR #622 | 75 | covered |
| Pass 3 | T-0463 / PR #624 | 75 | covered |
| Pass 4 | T-0478 / steward/resident-research-pass-4-reconciled | 75 | reserved/in flight |
| Pass 5 | T-0479 / PR #625 | 75 | landed; research ledger remains in progress |

The reservation ledger therefore contains 375 unique person IDs. Pass 4 is retained in the collision lock even while its reconciled branch is being finalized; no later cohort may reuse it.

## Remaining queue

The eligible remainder is 461 unique named, non-reconstructed residents whose household records are marked letter-list-only. The deterministic selector sorts person IDs within the scene-date-present and earlier/uncertain strata, interleaves the strata, and chunks that sequence in order:

| Next cohort | Ticket | Draft PR | Count | Present / uncertain |
|---:|---|---:|---:|---:|
| 6 | T-0480 | #627 | 75 | 38 / 37 |
| 7 | T-0481 | #628 | 75 | 37 / 38 |
| 8 | T-0482 | #629 | 75 | 38 / 37 |
| 9 | T-0483 | #630 | 75 | 37 / 38 |
| 10 | T-0484 | #631 | 75 | 31 / 44 |
| 11 | T-0485 | #632 | 75 | 0 / 75 |
| 12 | T-0486 | #633 | 11 | 0 / 11 |

Each ticket is open in the file-backed queue and each draft PR contains a frozen manifest, a pending-outcomes ledger and a research note. Draft PRs are scaffolds, not completed research; the next worker should claim the matching queue ticket and replace pending entries with dated corroboration, candidate/duplicate or documented no-corroboration outcomes.

## Deliberate exclusions

Reconstructed and hypothesised `inf_*` entries are outside the identity-research denominator. Seven remaining technical entries are unnamed/count or inferred household placeholders (including the Beaubien, Heacock, Owen, Robinson and Temple placeholder records); they are not silently converted into named people. No named non-letter-list residents remain after pass 5.

Surname similarity is a search clue only. Heritage, lineage, immigration origin, marriage, occupation, address and household membership require resolving evidence and must retain conflicts and candidate duplicates.
