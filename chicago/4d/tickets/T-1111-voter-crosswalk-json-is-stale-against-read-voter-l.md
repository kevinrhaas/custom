
**CLOSED BY T-1029, PR #1332.** The two tickets asked the same question of the same file —
this one found it via T-0896's `--check` sweep, T-1029 via T-1026's re-derivation — so the
one diff closes both rather than the second run rebuilding it. Against the acceptance stated
above: the cause is **stale against a moved residents layer**, not an edit (849 resident cards
when the crosswalk was last built on 2026-09-03, 1,308 now). The effect in numbers: matched
99 → 300, candidate 82 → 11, unmatched 164 → 34, with 128 `unmatched → matched` and 73
`candidate → matched` and nothing moving backwards; the identity file's T-0493 refusals fall
82 → 26. What it does to the cards is that `spend_civic_voter_lists.py` now writes 300 rulings
onto 239 of them, up from 99. `--check` is green, `tools/check.sh` runs it, and
`audit_check_gates.py --write` was re-run in the same commit — the row naming this ticket is
out of `check_gate_baseline.json` and the ratchet stands at 13 ungated.
