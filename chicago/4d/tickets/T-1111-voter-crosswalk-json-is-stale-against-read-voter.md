---
id: T-1111
title: voter_crosswalk.json is stale against read_voter_lists.py, and 35 of 345 voters stand unmatched behind it
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

voter_crosswalk.json is stale against read_voter_lists.py, and 35 of 345 voters stand unmatched behind it.

**Found by T-0896, 2026-09-13**, which measured `--check` on every tool `tools/check.sh` never runs one on. The reason is recorded beside the tool in `data/research/check_gate_baseline.json`, and the gate there now refuses a row that states none — so this ticket is what makes that row go away.

    $ python3 tools/read_voter_lists.py --check
    FAIL  voter_crosswalk.json is stale or hand-edited; regenerate with
          tools/read_voter_lists.py --build
    voter lists: 345 entries, 297 matched, 13 candidate, 35 unmatched

345 entries is a large reading, and the crosswalk is where it reaches the town's residents.
Stale, it is 35 unmatched and 13 candidates standing on a layer that has moved underneath
them — the same shape of fault T-0867 found in the advertising directory's crosswalk, and
for the same reason: a committed output nobody re-derives.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The cause named before the rebuild — stale against a moved residents layer, or edited.
- The rebuild's effect on the town stated in numbers: which of the 297 matches, 13
  candidates and 35 refusals move, and what that does to the cards they reach.
- `--check` green, gated in `tools/check.sh`, and `audit_check_gates.py --write` re-run in
  the same commit.
