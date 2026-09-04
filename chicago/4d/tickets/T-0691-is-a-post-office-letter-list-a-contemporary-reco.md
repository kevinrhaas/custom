---
id: T-0691
title: The ladder is a max over single classes and cannot see corroboration, so six men on the 1835 poll AND other lists are graded "the 1835 poll alone": add the convergence rung
state: open
epic: META
requested_by: owner
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
---

**The owner, 2026-09-04:** *"if the letter list places someone as likely there, and then there are
voter records, and then other records later, then that is fairly strong attestation route that they
are a real person… can we change or improve the grading system for these people like this with
multiple sources that are identifying them there in and around 1835?"* And, naming the pair:
*"like to me alone these two sources together would be attestation —
`chicago_democrat_1833_1835`, `chicago_voter_lists_1833_1835_irad`."*

**He is right, and this ticket exists because the first review of his question pushed back on it and
was wrong.** The objection raised was that the ladder grades by CLASS and not COUNT, and that a
count rule would make a man attested on two 1843 directory entries. That conflated two different
things: the *number of appearances* and the *convergence of independent classes*. Two 1843 directory
entries are one class, one era, possibly one lineage. The town's own poll list and the town's
newspaper are two different bodies recording the same man in the same window, and that is not the
same claim at all. The measurement below is what settled it.

## FINDING 1 — six men are graded on a false description of their own evidence

`grade()` reaches `G1a` (**attested** — *"The 1835 poll list and at least one other independent
source"*) only when:

```python
if POLL_1835 in classes and len(sources) > 1:
```

`sources` is the set of **`source_id`s** — archival provenance. Every Chicago poll, tax and muster
list in this project was digitised by IRAD and carries the single id
`chicago_voter_lists_1833_1835_irad`. So a man on the 1833 tax list, the 1834 poll AND the 1835 poll
has `len(sources) == 1`, misses `G1a`, and falls to **`G2a` — *"The 1835 poll list alone."***

That description is **factually untrue of the record it is applied to**. Willard Jones:

```
civic: tax_1833  | Jones, Willard | source: chicago_voter_lists_1833_1835_irad
civic: poll_1834 | Jones, Willard | source: chicago_voter_lists_1833_1835_irad
civic: poll_1835 | Jones, Willard | source: chicago_voter_lists_1833_1835_irad
   grade: inferred | rule: G2a  ("The 1835 poll list alone")
```

Three lists, taken in three different years, by the town, of who could vote and who paid tax. **They
are three independent records.** That one archive published them together is a fact about the
archive, not about the evidence. Under the ladder **exactly as the owner ratified it** these six are
already `G1a`, attested — no rung needs inventing:

| | in-window records | graded |
|---|---|---|
| Willard Jones | tax 1833 · poll 1834 · poll 1835 | G2a |
| Peter Pryne | tax 1833 · poll 1834 · poll 1835 | G2a |
| Ira Kimberly | tax 1833 · poll 1835 | G2a |
| John Foot | tax 1833 · poll 1835 | G2a |
| Dexter Hapgood | poll 1833 · poll 1835 | G2a |
| Edmund L Kimberly | poll 1834 · poll 1835 | G2a |

**This half is a defect fix, not a policy change**, and it should land first and separately.

## FINDING 2 — the ladder cannot express convergence at all

`grade()` is a **first-match cascade**: it asks "does any ONE class reach this rung?" and stops. It
never asks "do several independent classes agree?" So Edward Richards Allen —

| record | date | body that made it |
|---|---|---|
| `poll_1834` | 1834 | the town's electors |
| Chicago Democrat letter list | **1835-05-20** | the town's newspaper |
| Fergus directory | 1839, 1843 | a commercial directory |
| Tribune, Old Settlers' reception | 1882 | the Calumet Club, criterion = Chicago before 1840 |

— reaches `G2b` and stops, and would reach `G2b` on two of those four just as well. **Four
independent bodies naming one man across 1834 → 1835 → 1843 → 1882 grade identically to two.** That
is the gap the owner is pointing at, and no ruling on the letter list alone closes it.

## What is measured

Over `data/residents/households/` on dev, 2026-09-04:

| | |
|---|---|
| people graded `inferred` | 922 |
| …on the 1835 poll **plus** another in-window record (Finding 1) | **6** |
| …with 2+ distinct in-window classes but no 1835 poll (the Allen shape) | **14** |
| …carrying **both** the Democrat and the IRAD voter lists — the owner's named pair | **17** |
| of those 17, carrying no `ladder_rule` at all | 6 (T-0692's population) |

**Roughly twenty people.** Not the ~1,500 the letter-list-as-G1b reading would have moved — because
this rung asks for CONVERGENCE, not for a letter list to be promoted on its own. That distinction is
what makes it safe.

## The ask

1. **Fix `G1a`'s independence test.** Independence is a property of the RECORD — a distinct list,
   taken on a distinct occasion, by a distinct body — not of the `source_id` that digitised it.
   Count distinct `(list, describes_date)` records, not `source_id`s. The six above become `G1a`
   under the existing rung and no new policy is needed.
2. **Add a convergence rung — `G1c`, attested.** Two or more independent in-window records **of
   different class families**, naming the same identity. The families are: the town's civic lists
   (poll/tax/muster), the contemporary press (the 1833-35 papers, letter lists included), and the
   parish register. Allen qualifies on civic + press. **A letter list is not promoted on its own** —
   `G2e`/`G3` still hold it down alone — it only counts toward convergence, which is precisely the
   owner's reading: *"the letter list places someone as likely there, AND there are voter records."*
3. **`G0` SURVIVES UNTOUCHED.** Later evidence never constitutes attestation by itself. Allen's 1843
   directory and 1882 reception corroborate and date; the two in-window records are what earn the
   rung. A man with four later sources and nothing in-window stays `not_1835_resident`.
4. **Independence must be defined before it is counted**, or convergence becomes an artefact:
   - nine printings of one letter list are ONE record, not nine — T-0318, T-0424, T-0428 are the
     tickets that establish which printings are the same list;
   - the same man minted twice from two printings is one identity, not two — that is T-0660;
   - the identity merge must be sound first, or two men wrongly merged manufacture their own
     corroboration. `crosswalk.json`'s refusal rules already govern this and are the gate.
5. **Land it as a proposal.** `consolidate_resident_evidence.py --build` prints proposed changes
   without writing household files; the regrade is a separate PR with before/after counts and the
   twenty names listed, each checkable by hand. At this size they should be checked by hand.

**Done when** no person record is described by a rung that contradicts its own evidence blocks,
`G1c` exists with its independence rule written down, the twenty are regraded or individually
explained, and `docs/RESEARCH/resident-grading-policy.md` carries the owner's words and the date.
