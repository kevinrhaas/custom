---
id: T-0772
title: Twelve dooryard gardens went with the retired households: should a garden follow the house or the household?
state: blocked-owner
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: run 9/6/2026, 10:45:13 AM CT
blocked_on: Does a dooryard garden follow the HOUSE or the HOUSEHOLD? Clause 4 of tools/generate_dooryard_pickets.py says a garden is a household's, and T-0516's withdrawal of stale occupancy prose took the layer from thirteen gardens to one (Elijah Harmon's). Measured for you with 'generate_dooryard_pickets.py --compare-rules', over the tree as it stands: the HOUSEHOLD rule draws 1 garden; the HOUSE rule — clause 4 dropped, every other clause unchanged — draws 29, adding 28. But 25 of those 28 would stand behind a RECONSTRUCTED cottage (a garden invented behind an invented house), and of the 3 attested houses, 2 are John Wright's buildings TO LET, whose own records say the tenant cannot be named — leaving exactly one added garden behind an attested dwelling the town can name (lasalle_lake_house). Note also that the lot-line fences do NOT run off the occupancy test, contrary to this ticket's third bullet: they admit on IMPROVEMENT and fence 118 of 127 improved lots in 291 runs, so the yard fence already follows the HOUSE while the garden inside it follows the HOUSEHOLD. (a) keep the household rule, 1 garden, and accept a nearly empty layer until T-0514's address work lands real lives_at values; (b) the house rule, 29 gardens, all reconstructed-tier and hidden together; (c) the house rule EXCEPT buildings to let, 27. The full derivation is docs/RESEARCH/dooryard-garden-admission-rule.md; whichever wins, clause 4 and docs/LIBERTIES.md L129 (which still claims eighteen) are rewritten to say it.
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34043106390
---

Twelve dooryard gardens went with the retired households: should a garden follow the house or the household?.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Filed by T-0516, which caused it and refused to decide it.**

`tools/generate_dooryard_pickets.py` admits a lot to the garden layer on four clauses, and
clause 4 is *"a household recorded as living in it"* — read off the structure record's
`occupants` prose naming an `hh_` id. T-0516 withdrew that prose from the 104 anonymous
roofs the retired inferred-household layer had adopted, because the households it named
were removed on 2026-09-02 under the owner's ruling. The rule then did exactly what it
says: **thirteen dooryard gardens became one.** The survivor is Elijah Harmon's, the only
lot this record reaches where the committed household index carries a real `lives_at`.

The generator's own comment anticipated this and named the ticket: *"the stale-prose
problem is T-0516's"*. So the collapse is the rule working, not the rule breaking — twelve
gardens were resting on the prose of households that no longer exist, and a garden behind a
house nobody lives in claims a gardener who does not exist.

**But the question underneath it is the owner's, not the loop's.** A dooryard garden could
just as defensibly follow the HOUSE — one dwelling alone on a platted lot, by archetype and
by function — as follow a recorded household. That reading would keep all thirteen and
would say something weaker but still true: houses of this kind had kitchen gardens behind
them. It is a claim about what the town looked like, and the owner has ruled on exactly
this kind of trade before ("lots of nothing happened in the city which is bad").

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The owner is asked, in these terms, which rule the garden layer runs on: the household
  (today, thirteen → one) or the house (thirteen or more, on a weaker claim). Use
  `ticket.mjs block --owner --on "..."` rather than choosing for him.
- Whichever he rules, clause 4 is rewritten to say it, `docs/LIBERTIES.md` L129's entry is
  brought into line with the rule actually in force, and the count before and after is
  stated.
- If the house rule wins, the same question is asked of the lot-line fences, which run off
  the same occupancy test.

**Links:** T-0516 (the withdrawal) · T-0637 (`belongs_to` on every run) · T-0514 (the
address work the real `lives_at` count is waiting on) · `docs/LIBERTIES.md` L129.

---

**MEASURED AND PUT TO THE OWNER, 2026-09-06.** The question was asked in numbers rather
than in prose, because "thirteen or more" above was a guess and the town has grown since.
`python3 tools/generate_dooryard_pickets.py --compare-rules` (added by this pass; it
writes nothing, and no writing path can reach the clause-4-less pool) counts both readings
over the same tree:

| | lots admitted | gardens drawn |
|---|---|---|
| the HOUSEHOLD rule, in force | 1 | **1** |
| the HOUSE rule, clause 4 dropped | 34 | **29** |

Of the 28 gardens the house rule adds, **25 stand behind a `reconstructed` cottage** and
of the 3 attested houses **2 are John Wright's buildings to let** — the case clause 4's own
docstring names as the thing it excludes. One added garden stands behind an attested
dwelling the town can name.

Two things the ticket got wrong, both corrected in the evidence file:

* the lot-line fences do **not** run off the occupancy test. They admit on IMPROVEMENT and
  fence 118 of 127 improved lots in 291 runs, so the third bullet's question is already
  answered in the tree — the yard fence follows the HOUSE while the garden inside it
  follows the HOUSEHOLD, and that inconsistency is the strongest argument for ruling;
* `docs/LIBERTIES.md` L129 still claims *"Eighteen garden fences"* on eighteen house lots,
  and the record holds one. It is left uncorrected on purpose: the number to write into it
  is the ruling's.

Full derivation: `docs/RESEARCH/dooryard-garden-admission-rule.md`.
