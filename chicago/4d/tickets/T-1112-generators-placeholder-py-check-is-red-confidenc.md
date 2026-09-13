---
id: T-1112
title: generators/placeholder.py --check is red: _CONFIDENCE carries two levels, so the confidence view is untestable against the asset built to test it
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-13
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

generators/placeholder.py --check is red: _CONFIDENCE carries two levels, so the confidence view is untestable against the asset built to test it.

**Found by T-0896, 2026-09-13**, which measured `--check` on every tool `tools/check.sh` never runs one on. The reason is recorded beside the tool in `data/research/check_gate_baseline.json`, and the gate there now refuses a row that states none — so this ticket is what makes that row go away.

    $ python3 generators/placeholder.py --check
    FAIL  _CONFIDENCE carries [0.0, 0.5], not all three levels — the confidence view
          would not be testable against this asset

The placeholder asset exists so the confidence view has something to be tested against, and
it carries two of the three levels. So the view's rendering of `conjectural` — or whichever
level is missing — has no fixture behind it, which is the one thing this asset is for.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The placeholder carries all three confidence levels and the view is demonstrated against
  each, at both viewports.
- `--check` green, gated in `tools/check.sh`, and `audit_check_gates.py --write` re-run in
  the same commit.
