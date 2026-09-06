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

## What "frozen" means, and what a regeneration may touch (T-0764)

Added 2026-09-06. `tools/resident_cohort_freeze.py` owns this contract; `tools/check.sh`
runs its `--self-test` beside the eight `--gate` steps, and every gated selector — the
pilot, passes 2–5 and passes 13–15 — goes through it on both the gate and the write.

A cohort manifest is **a reservation and an identity lock**: it says which people this
pass owns, in a fixed order. Each row also carries a **snapshot** of the tree at the
moment the cohort was fixed — `starting_grade`, `starting_evidence`, `starting_presence`,
`starting_occupation`, `sources`, `letter_list_returns`, `stratum`, and the document's
`population_frame` counts. That snapshot is what makes a finished pass legible: *this
person came into the cohort at `inferred`, on one source, and left it at `attested` on
three.*

**What the gate asserts** (a failure here is real staleness):

1. the committed person ids, IN ORDER, are the ones the selector's frame still yields;
2. every id still names a real, named person in `data/residents/households/` — not a
   person who has vanished, and not an unnamed placeholder;
3. every row carries exactly the fields the selector emits, so a snapshot cell cannot be
   silently dropped or invented;
4. every document key outside the snapshot matches the derivation exactly, and
   `population_frame.sample_size` still counts the people the manifest holds.

**What it does not assert, and reports instead:** how many snapshot cells have moved
since the freeze. A source landing on a member, or a member's grade rising, is the
research landing — the cohorts' whole purpose — and is printed, not failed.

**The first write is the freeze.** A regeneration reads the committed snapshot cells back
off the file for every id the manifest already holds; only an id the manifest has never
held takes today's values. Identity cells — `name`, `household_id`, `selection_reason` —
are not snapshot and are refreshed, so a corrected name still reaches the manifest.

**The loss this replaced,** measured across this repository's history on 2026-09-06: of
the 82 commits that touched the eight gated manifests, **46 rewrote the freeze**, and
**384 snapshot cells** were overwritten. The gate called a moved snapshot `stale`, the
documented remedy was to regenerate, and the regeneration rebuilt every row from today's
tree — so the freeze recorded the day of the last regeneration rather than the day the
cohort was fixed, and no diff was ever read.

| Manifest | commits | rewrote the freeze | cells overwritten |
|---|---:|---:|---:|
| `pilot_75_cohort.json` | 13 | 7 | 79 |
| `pass_02_75_cohort.json` | 16 | 10 | 92 |
| `pass_03_75_cohort.json` | 16 | 8 | 95 |
| `pass_04_75_cohort.json` | 6 | 0 | 0 |
| `pass_05_75_cohort.json` | 2 | 0 | 0 |
| `pass_13_76_cohort.json` | 9 | 7 | 50 |
| `pass_14_76_cohort.json` | 10 | 7 | 36 |
| `pass_15_76_cohort.json` | 10 | 7 | 32 |

Those 384 cells are gone; nothing here recovers them. What the contract does is stop the
next one.

**What is NOT weakened.** The selection-time refusals stay exactly where they are, inside
each selector's `derive`: the novelty rule (zero overlap with people who already carry a
research row), the strata quotas, and the per-person stratum-membership assertions. A new
manifest claiming somebody another pass has ruled on is still refused before it is ever
committed.

**The residual, not fixed here.** Those per-person membership assertions in the pilot and
passes 2–5 — "no longer marked `letter_list_only`", "established stratum became
letter-list-only", "`presence` changed" — run inside `derive` on the gate path as well as
the write path, so a member whose stratum flags move in the tree still fails the build
rather than being reported. Passes 13–15 scoped their equivalent to minting; the five
older selectors have not. Filed as its own ticket.
