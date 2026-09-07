---
id: T-0841
title: The keeper of the St Cyr register is graded G5, not G2c: may the officiant of a parish register be graded on it?
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

The keeper of the St Cyr register is graded G5, not G2c: may the officiant of a parish register be graded on it?.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0724, 2026-09-05.** That ticket fixed the splitter — a compound surname is now
one surname — and `st_cyr_john_mary` finally carries a ladder rung. The rung is **G5**, and
T-0724 expected **G2c**.

G5 is honest. G2c reads *"the St Cyr register 1833-1835 — a party to a marriage or burial in
the parish inside the scene window"*, and the priest is a party to neither: he is the
officiant. `read_church()` reads `st_cyr_marriages_1834_1839.json` and
`st_cyr_deaths_1834_1837.json` and yields one appearance per record — the person the record
is *about*. So the consolidation sees exactly one appearance of Fr St Cyr, his own town
card citing `andreas_1884_v1`, and G5 is the ladder declining to grade a man on a source it
has not read, and filing him as a conflict.

**The question, and it is the owner's.** The register is his handwriting. `J. M. I. St Cyr`
is printed in `st_marys_baptisms_1833_1835.json`, and the register places him in the parish
across the whole scene window as plainly as it places anybody it names. But grading the
keeper of a register on it is a change to a rung the owner ratified, and this project does
not move a rung to make a man look better.

Three ways it could go, and none of them should be taken without a ruling:
1. **Leave it.** G5 is correct under the rung as written; the priest stays a conflict for
   the owner to read, and his card keeps its Andreas grade.
2. **A new rung** — the keeper of a contemporary register, distinct from a party to it,
   graded on the register's own dates. Needs a name, a grade and a place on the ladder.
3. **Read the baptisms.** `st_marys_baptisms_1833_1835.json` is not in `read_church()` at
   all, so the whole baptismal register is invisible to the ladder — parties included. That
   is worth doing whichever way the officiant question goes, and it may be the larger find.

**Acceptance:** the owner rules, the ruling is written into
`docs/RESEARCH/resident-grading-policy.md`, and `grading_proposal.json` is re-derived if it
moves.
