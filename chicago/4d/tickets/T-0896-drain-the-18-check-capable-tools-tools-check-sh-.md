---
id: T-0896
title: Drain the 18 --check-capable tools tools/check.sh never runs: gate each or record why it cannot be gated
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Drain the 18 --check-capable tools tools/check.sh never runs: gate each or record why it cannot be gated.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0714, 2026-09-06.** `tools/audit_check_gates.py` reports 18 of this repo's 100
`--check`-capable tools that `tools/check.sh` never runs a `--check` on; 17 of them it does not
invoke under any mode at all. The list is committed at `data/research/check_gate_baseline.json`
and the gate T-0714 added is a RATCHET only — the set may not grow, and nothing shrinks it.

Each of the 18 needs one of two answers, and they are not the same answer:

- **gate it** — the tool re-derives a committed file from committed inputs, so `check.sh` runs
  its `--check` beside its siblings, in the same commit that makes it green; or
- **record why it cannot be** — a one-shot pass whose inputs are gone, a tool that reaches the
  network, a derivation that is red for a ruling somebody else owns. That reason belongs in the
  baseline file, next to the tool, where the next reader finds it.

Known before starting: `mint_letter_list_residents.py --check` is red today and is **T-0691's**,
which is itself blocked on T-0660's ruling — do not fold it in here. `verify_fergus_1839_first_ward.py`
runs `--offline` in the gate, which proves something different from `--check`.

**Acceptance:** every one of the 18 is either gated in `check.sh` with a green `--check`, or
carries a stated reason in `check_gate_baseline.json` that a reader can act on; `bash tools/check.sh`
green; and `audit_check_gates.py --gate` still passes. Splittable by group if 18 is more than one
run — it very likely is.
