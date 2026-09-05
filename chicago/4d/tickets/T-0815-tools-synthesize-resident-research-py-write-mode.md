---
id: T-0815
title: tools/synthesize_resident_research.py write-mode reverts the 2026-09-04 regrades and --check cannot see it
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

tools/synthesize_resident_research.py write-mode reverts the 2026-09-04 regrades and --check cannot see it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0508 (cohort 13), 2026-09-05, while trying to carry a research pass into the
derived layer.**

`tools/check.sh` runs `synthesize_resident_research.py --check` and it is GREEN on `dev`.
Running the SAME tool in write mode, on the same clean `dev` tree, rewrites 109 household
files and one index — and what it writes is a REVERSION:

    regraded_on stamps removed:  109      re-added: 0
    "grade": "attested" removed:  17      "grade": "inferred" added: 17

Those `regraded_on: "2026-09-04"` / `rule: "G1c"` stamps are the grading pass the owner
asked for on 2026-09-04 ("we have people now who have been identified in multiple sources,
but they are still being marked as inferred"). The synthesis tool does not know about them,
so it recomputes the grade from its own inputs and throws the stamp away.

**Why this matters more than the 109 files.** `--check` is the per-commit gate and it passes
either way, so the drift is INVISIBLE: the tool and the committed tree disagree and nothing
says so. Any run that legitimately runs the writer — a research cohort, a mint, a
consolidation — silently reverts seventeen grades as a side effect of unrelated work. T-0508
found it only because it diffed before committing, and shipped its ledger WITHOUT running the
writer for exactly this reason.

## The ask

1. Make `--check` see it: the check must fail when write-mode would change a committed byte,
   or state in the ledger which fields it does not own.
2. Decide who owns `grade` on a person with a `regraded_on` stamp — the regrade pass or the
   synthesis — and make the loser leave it alone. Both writing it is the defect.
3. Once (2) is settled, run the writer once and land the derived layer, which is where
   T-0508's 76 rows (and T-0509's, and T-0510's) are waiting.

**Done when** running `tools/synthesize_resident_research.py` on a clean tree changes no file,
and `--check` fails if it would.
