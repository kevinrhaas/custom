---
id: T-0728
title: The published tree is 944 bytes under its 32 MB budget, so the next changelog entry alone is a red gate
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

The published tree is 944 bytes under its 32 MB budget, so the next changelog entry alone is a red gate.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**The measurement, 2026-09-05.** `site/chicago/4d` publishes at **33,553,488 bytes**
on `dev`. `validate.py`'s `SITE_BUDGET_MB = 32` is 33,554,432. The headroom is **944
bytes**, and `run_site_check` is a hard error, not a warning.

**Why that is a gate and not a curiosity.** The changelog is published TWICE —
`site/chicago/4d/js/changelog.js` (Manager and the launcher parse this path; it is a
contract) and `site/chicago/4d/walk/js/changelog.js` (a page under `walk/` cannot
import from its own publish mirror). So a changelog entry costs twice its own bytes,
and the fleet contract says a user-visible change SHIPS one. A 470-byte entry — four
lines of prose — is the largest that now fits, and the entry style of the last fifty
is five to ten times that. T-0511 hit this: its entry was written, stamped, published,
and reverted unwritten because the gate went red on the byte count alone.

**What the budget's own comment already says.** `tools/validate.py` lines 52-112 record
two conscious re-budgets (25 → 28 at T-0317, 28 → 32 at T-0379) and name the two largest
items in the tree. One of them is this: "the duplicated changelog at 2.07 MiB, 7.3 % of
the tree, which is T-0364 and is still unanswered." That is 7.3 % of the tree spent on a
file published twice, while the whole tree is 944 bytes from refusing the next commit.

**The three answers, and this ticket is which one.**
1. Answer T-0364 — publish the changelog once and let `walk/` reach the single copy,
   which returns ~1 MB and does not move the contract path Manager parses.
2. Raise the budget a third time. `docs/RENDERING.md` § the gate table has recorded a
   sanctioned raise to ~100 MB since the rendering plan was written, and the LFS clause
   the budget actually defends is about FORMAT, not size.
3. Trim something else in the tree by more than a changelog entry costs.

Doing nothing means the next entry-shipping PR discovers it, as T-0511 did.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- `python3 tools/validate.py --site` green with a changelog entry of ordinary length
  (≥ 2 KB) added, published, and still in the tree.
- Whichever answer is taken is written into `tools/validate.py`'s budget comment beside
  the two re-budgets already recorded there, saying what it superseded and why.
- `site/chicago/4d/js/changelog.js` still exists at that exact path, whatever else moves:
  Manager and the launcher parse it and it is a contract (T-0155).
- No record, no grade and no geometry moves.

**Links:** **T-0364** (the duplicated changelog, unanswered) · T-0317 and T-0379 (the two
re-budgets) · `tools/validate.py` §`SITE_BUDGET_MB` · T-0511 (which found it).
