---
id: T-0705
title: Apply the 158 grading proposals to the people who already exist: regrade, attach the evidence, and record every refusal
state: claimed
epic: TOWN
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0515
opened: 2026-09-04
closed: null
pr: null
claimed_by: run 9/4/2026, 5:41:51 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33926169512
---

Apply the 158 grading proposals to the people who already exist: regrade, attach the evidence, and record every refusal.

Piece 1 of 2 of **T-0515 — 727 projected residents rest on a letter list alone: regrade every one a second source corroborates and attach its evidence**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- `tools/mint_civic_residents.py --regrade` applies every proposal in `grading_proposal.json`'s
  `changes_to_existing_people` that the evidence rows support, and REFUSES the rest with the refusal
  written onto the person. Idempotent and re-derivable: `--regrade --check` re-applies to the committed
  tree and diffs, so `check.sh` can hold it.
- The regraded count with the rule that fired for each; projected / inferred / attested counts before
  and after.
- No grade lowered without a refusal recorded on the person.
- `--regrade --report` prints every regrade with its rule and every refusal with the reason.
- `check.sh` green; mirror published; changelog stamped.

**The parent's ask 2 (the 1840 bridges) is T-0702 and is NOT in scope here.**

