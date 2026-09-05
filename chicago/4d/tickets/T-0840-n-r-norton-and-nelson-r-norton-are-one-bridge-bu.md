---
id: T-0840
title: N. R. Norton and Nelson R. Norton are one bridge-builder carried twice: retire the duplicate card and rebuild the sixteen crosswalks that re-derive against the layer
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0723
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

**`norton_n_r` and `norton_nelson_r` are two cards for one man.** The merge the consolidation
makes is RIGHT — M2 attaches the initial-only reading to the one full forename of that
surname — and the defect is upstream: the town carries Nelson R. Norton twice. That is a
reconciliation of two household records, not a splitter change.

**The evidence, already gathered (T-0723, 2026-09-05).** Fergus's Chicago directory of 1839
prints exactly one Norton of that initial, on page 26 — *"Norton, N.R., bridge-builder,
n.-w. cor. N. State and Indiana sts"* (`f1839_e1107`) — and BRIDGE-BUILDER is the deed
Andreas gives Nelson R. Norton in terms: the first draw-bridge over the main river, at
Dearborn Street, in March 1834. His arrival of 16 November 1833 and the sloop Clarissa of
May 1836 bracket 1 July 1835, so he is the man whose letter was waiting. `norton_n_r` was
minted from the Democrat's letter list of 1 July 1835, column 5, by
`tools/mint_letter_list_residents.py`, which mints one record per printed name and by its own
ruling matches none of them against residents the town already holds. The directories
crosswalk already records that 1839 line as `contested` on the ground that two 1835 residents
meet it.

**WHY THIS IS ITS OWN RUN, and what a run that takes it is walking into.** Retiring one
person out of `data/residents/` makes `check.sh` red in sixteen places at once. A run in
T-0723 did the whole retirement, went green on `validate.py`, and then found: the resident
audit, the sidecars, the st-cyr and newspaper registers, the liberties scope count for L214
(727 → 726) and the research-package index all need regenerating; the layer-reads census
fails on every new field of the retirement ledger until it is wired or banked; and the
FROZEN cohort manifests — *"the 75-person research cohort is fixed"*, four of them — fail
because a frozen snapshot is exactly what must NOT be regenerated to make a gate pass. That
last one is the real question this ticket has to answer, and it is adjacent to T-0764.

**Acceptance:** the two cards are reconciled into one, or shown to be two men with the
evidence that says so; `--coverage` reports no person in state `absorbed_by_another_card`;
no person is deleted without the merge being recorded where a reader of either card can see
it, and where a reader who follows the RETIRED id can find it; `check.sh` is green, with the
frozen cohort manifests handled by a stated decision rather than a regeneration that quietly
rewrites a freeze.
