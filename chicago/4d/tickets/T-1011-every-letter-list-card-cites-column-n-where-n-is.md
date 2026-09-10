---
id: T-1011
title: Every letter-list card cites 'column N' where N is its claim NUMBER, not the printed column: c026 becomes 'column 26' on 700 cards
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Every letter-list card cites 'column N' where N is its claim NUMBER, not the printed column: c026 becomes 'column 26' on 700 cards.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-1008 while adding twenty cards that inherit the fault.

`tools/mint_letter_list_residents.py`, `issue_of()`:

    tail = f", column {int(col[1:])}" if col.startswith("c") and col[1:].isdigit() else ""

`col` is the CLAIM id — `c026`, `c033` — and the number in a claim id is its position in
the issue's claim list, not a column of the page. So `hh_conger_thomas` reads *the Democrat
of 4 March 1834, column 26* and the new `hh_harkness_j_p` reads *column 33*, while the
letter list stands in **printed column 2** of page 4 in both. Every card the pass mints
carries the same sentence, so the count is the whole cohort — 745 today.

**Why it is not a one-line fix.** The string is inside the DERIVATION: change it and all
745 cards re-derive, so the correction has to be written and the whole set rewritten in one
commit, and the pass's `--check` is currently red against the committed tree for unrelated
reasons (772 files stood drifted on dev on 2026-09-10), which a repo-wide rewrite would
silently absorb. That is the work: fix `issue_of` to read the printed column off the claim's
own `locator.column` — every claim carries one — re-derive, and land the rewrite as its own
revertible unit with the drift measured before and after.

**Acceptance:** no card cites a column the claim's locator does not state; `--check` is
green on the tree the commit lands; the count of cards whose sentence changed is stated.

**Links:** T-1008 (found it) · T-0378, T-0379 (the pass) · L214
