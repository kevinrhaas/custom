---
id: T-0844
title: The audit sees only the newest override, so conflicts an earlier pass recorded and a later one overwrote are invisible to it
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

The audit sees only the newest override, so conflicts an earlier pass recorded and a later one overwrote are invisible to it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found while ruling the standing conflicts under T-0733. `export_resident_audit.py`'s
`findings()` builds `person id -> override` by walking `pass_*_findings.json` in order and
assigning, so a person reviewed twice keeps only the LAST pass's row. `vann_angeline` is the
demonstration: pass 02 recorded a disqualifying conflict against Angeline Vann of Missouri
("Born 1834 and later Missouri geography"), pass 13 rewrote the override with
`no_corroboration` and no candidates, and the audit's `flag_conflicting_evidence` has read
false for her ever since. The ledgers hold conflicts against **96** people; the audit sees
**81**. The fifteen it cannot see are not resolved — they are overwritten.

`data/research/residents/conflict_rulings.json` already covers all 96, because
`check_conflict_rulings.py` reads every pass; the audit is the layer still reading one.

**Acceptance:** the audit's view of the research ledgers accounts for every pass that
reviewed a person, or states in the README why the newest override is the right one and
carries the count it therefore does not show. No conflict is silently dropped by write order.

**Links:** T-0733 (ruled them; found this) · T-0512 (the audit) · T-0517 (the re-run).
