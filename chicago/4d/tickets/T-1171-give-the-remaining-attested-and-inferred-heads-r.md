---
id: T-1171
title: Give the remaining attested and inferred heads reconstructed families from the household model: wives, children, servants and apprentices drawn by the head's age, trade and household type, seeded, named from the pools, every member marked reconstructed
state: claimed
epic: META
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-16
closed: null
pr: 1476
claimed_by: run 9/20/2026, 3:23:50 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35535214426
---

After T-1170, most of the 1,263 heads still stand alone — a letter-list name with a
sex and an age band and nothing else. The owner: *"make sure that family compositions included
children are complete."* Stage `families_model` of T-1167: the household model
(T-1163) is applied to every head that has no source-named family, deterministically.

**Rules:** the head's bucket (age band, trade, division, presence) → household type drawn from
the model's shares; married → a wife (age from the spacing rule, a pool forename, the head's
surname), children by marriage duration and the spacing rule (none born after 1835-07-01), a
servant/domestic where the type has one, an apprentice/journeyman where the trade's shop
household has one (agreed with T-1183); single → alone, or boarding (the type says which,
and T-1175 seats him). `presence` of members follows the head's. Every member: `grade:
reconstructed`, `name_basis`, `basis` (the model row), `seed`, `replaceable_by` ("a source naming
this head's family").

**Order-book discipline:** the tool fills the order book's person buckets (sex × age × division)
as it draws and refuses to overfill one — so the drawn town matches the population model in the
aggregate, not just per household.

**Acceptance:**

- Every head has a household type and the members it implies; the resulting person count,
  sex ratio (target ~147 men per 100 women aged 20+, from 1840, corrected by the model), age
  pyramid and household-size distribution printed against the model, all within the model's
  brackets; the order book buckets read filled to their `to_reconstruct` and not beyond.
- Deterministic: two builds are byte-identical; `--check` in `check.sh`.
- LIBERTIES entry for the whole reconstructed population, `Scope:` counted.
- Visible: the People view's reconstructed filter shows them; the household card shows the family
  with each member's tier and the rule that drew them; the "Reconstructing the town" card's
  person bars move.

**Stop condition:** the town's households look like the model's town in every printed table.

**Links:** T-1167 · T-1163 · T-1161 · T-1166 · T-1170.


---

## REOPENED 2026-09-20 by T-1463, for 227 persons — measured, not assumed

**The dates are the finding.** This ticket closed **2026-09-18** on PR #1476 having drawn
124 of 556. T-1386's presence rulings landed **2026-09-19**, the day after, and put 827
people into the town of 1 July 1835 who had been counted `uncertain`. Every quota this
stage worked to was therefore cut against a town that did not yet hold them, and the 432
it was still owed on 2026-09-20 was an unknown mixture of real work and that lag.

T-1463 summed the rulings into the order book's `known` and measured the split:

| leg | owed before the re-cut | owed after | verdict |
|---|---:|---:|---|
| households | 58 | **0** | DISCHARGED — the quota was 182 against 124 drawn; the re-cut takes it to the drawn figure |
| persons | 374 | **227** | part artifact, part real |

So 205 of the 432 was the staleness and **227 persons are genuinely owed**. That is why
this reopens rather than closing with a note: the answer was measured, and half of it is
work. T-1174 (856/856) and T-1347 (308/308) closed exact on the same counter, which is
what made 432 worth adjudicating rather than explaining away.

**What the re-taker is owed, and what they are not.** 227 persons in the `T-1171` person
buckets of `data/reconstruction/1835_reconstruction_order_book.json`; no households. And
the person buckets this stage already overdrew are REFUSED rather than re-cut — they are
named in the book's `recut_refusals` with both numbers, held at what was drawn. Nobody
this stage has already drawn is un-drawn (the owner's ruling of 2026-09-20, T-1459).
