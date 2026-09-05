---
id: T-0725
title: The published tree is 900 bytes under the 32 MB ceiling on dev, so the next PR that adds anything at all fails the gate
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
**Measured 2026-09-04 while gating PR #827 (T-0692).** `validate.py`'s `run_site_check`
sums every file under `site/chicago/4d/` against a hard 32 MB ceiling, and reports over-budget
as an **error**, so `check.sh` fails and the dev gate stops the PR.

| tree | bytes | of 32 MB |
|---|---|---|
| `origin/dev` | 33,553,488 | **31.9991 MB** — 900 bytes of headroom |
| dev + PR #827 | 33,561,196 | 32.0065 MB — 6,808 bytes over |

**The whole of PR #827's published footprint is 7,708 bytes**: one changelog entry and the
four rows its follow-up tickets add to the mirrored `tickets.json`. There is nothing in it
to trim, and trimming it would not help — **the next PR on this lane hits the same wall**,
whatever it contains. Any PR that ships a changelog entry (which the contract requires of
every user-visible change) adds a few kilobytes to the mirror by construction.

**Why it is not a one-off.** `tickets.json` is mirrored in full and grows with every ticket
filed; the changelog grows with every entry. Both are append-only by design and both are
published. The ceiling exists because GitHub Pages cannot serve Git LFS objects, so it
cannot simply be raised without knowing what Pages will actually take.

**The shape of an answer** (for the owner to rule on, not for a run to pick):
- the 30 MB of assets is where the room is, not the 60 KB of text — one asset re-encode
  buys back more than a year of changelog;
- or the mirror stops carrying what the renderer never loads. `tickets.json` is read by
  Manager, not by the walkthrough, and `smoke_budget.mjs --for-diff` already says so in as
  many words: *"the backlog mirror — the renderer never loads it"*;
- or the ceiling moves, with a measurement of what Pages serves, rather than by guess.

**Acceptance:** the published tree is back under the ceiling with stated headroom, and the
gate says how much; whatever is removed from the mirror is shown not to be loaded by the
renderer (or by Manager, for `tickets.json`); and the check reports the margin on every run
so the next approach to the wall is visible before it is a blocked PR rather than after.
