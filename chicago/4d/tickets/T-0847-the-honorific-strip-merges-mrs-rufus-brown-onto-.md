---
id: T-0847
title: The honorific strip merges Mrs Rufus Brown onto her husband: hold a wife-form reading apart from a man the town records, by rule and self-test
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0723
opened: 2026-09-05
closed: null
pr: null
claimed_by: run 9/5/2026, 4:23:30 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33990992662
---

**`brown_mrs_rufus` — "Mrs Rufus Brown" — is folded onto `brown_rufus`, and she is not her
husband.** `Mrs` is stripped as an honorific, which leaves `Rufus Brown` on both readings, so
the merge is M1-identical and wrong. A woman whose only printed name is her husband's is a
real and common shape in this corpus — the 1843 and 1844 directories list widows that way as
house style, and the corpus prints the form 111 times — and the splitter had no way to hold
her apart. The fix is a rule, not a one-off.

Piece 1 of 2 of **T-0723 — One identity, two town cards**, split because the parent needed
more than one run's demonstration. The Norton half is T-0840: it retires a person out of the
residents layer, and sixteen committed crosswalks and cohort manifests re-derive against that
layer, so it is its own unit of work. This piece touches no household record at all.

**Acceptance:** the honorific case is held apart by a STATED rule in `REFUSAL_RULES` with a
self-test that fires when it is broken, including negative controls that fail if the rule
widens; `Mrs Rufus Brown` gets a ladder rung of her own in `grading_proposal.json`; the rule
names the evidence it turns on rather than guessing which forenames belong to men; and the
policy doc carries the rule in prose.
