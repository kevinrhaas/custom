---
id: T-0720
title: 459 household cards are stale against tools/synthesize_resident_research.py and --check does not notice: the T-0493 voter evidence never reached the cards
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

459 household cards are stale against tools/synthesize_resident_research.py and --check does not notice: the T-0493 voter evidence never reached the cards.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**The finding, measured 2026-09-05 on dev at 82abe294.** From a clean checkout of `dev`,
with nothing else changed, `python3 tools/synthesize_resident_research.py` rewrites **459
household cards**. The tool is the writer of the `resident_research` block on every
person, and the block it wants to write is not the block that is committed: 380-odd cards
gain a `resident_research` object citing **T-0493** with `outcome: no_corroboration_yet`
and `reviewed_on: ""` — the voter-crosswalk evidence read by T-0493, which the synthesis
has been able to write since that ticket landed and which never reached a card.

**Why nothing caught it.** `--check` is green on that same clean checkout. It re-derives
the population in memory and validates the invariants; it does NOT compare its derivation
against the committed household files. So a tool whose output has drifted 459 files away
from the repository reports `OK: 1404 people` and `check.sh` is satisfied. Every other
generated artefact in this project is gated by re-derivation (`datum.json`,
`validate.py --stale`); this one is not.

**Why T-0509 did not fix it in passing.** Running the write is not a bookkeeping tidy: it
also moves grades. Re-deriving against T-0509's completed ledger takes the town from 523
attested / 722 projected to 511 / 782, because a letter-list-only person carrying a
*documented* no-corroboration reads differently to the tool than one never reviewed. That
is a grade movement, the cohort tickets forbid grade movement (T-0513 consolidates,
T-0514/T-0515 apply), and 459 unrelated files do not belong in a cohort's PR.

**The ask.** Two pieces, and the second is the one that matters:

1. Run the write, as its own reviewed unit, and say in the PR which cards moved and why —
   including the grade deltas above, which are T-0515's to rule on, not this ticket's.
2. Give `--check` a re-derivation gate: write to a temporary tree, diff against
   `data/residents/`, and fail on any difference, the way `validate.py --stale` fails on a
   record that no longer matches its mesh. Without that, the next drift is silent too.

**Links:** T-0493 (the voter read whose evidence is stranded) · T-0509 (which measured
this) · T-0513 / T-0514 / T-0515 (the passes entitled to move a grade).
