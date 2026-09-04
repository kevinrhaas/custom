---
id: T-0691
title: Is a post-office letter list a contemporary record naming the person in Chicago? The ladder parked this for the owner and 11 multi-source residents sit on the answer
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

**The owner, 2026-09-04, looking at `hh_allen_edward_richards.json`:** *"we have people now who have
been identified in multiple sources, but they are still being marked as inferred? they should be
attested if you have seen them like this in multiple sources."*

## The question is already asked, and it is his to answer

`tools/consolidate_resident_evidence.py` states it against rung **G2e**, in the code:

> *"A Chicago post-office letter list of 1833-1835 and nothing stronger. The list names a person
> whose mail is at Chicago; **this tool declines to read that as the ladder's `contemporary record
> naming the person in Chicago` and grades it down. See the policy doc — it is the one reading put
> back to the owner.**"*

And `docs/RESEARCH/resident-grading-policy.md` § *The one reading the ladder needed, put back to the
owner* puts the stakes on it:

> *"**Is a post-office letter list 'a contemporary record naming the person in Chicago'?** It names
> a person whose *mail* is at Chicago. Reading it as G1b would grade roughly **1,500 letter-list
> names `attested`** in one pass. This tool takes the cautious half … **If the owner rules the other
> way, one line of `grade()` changes and the counts move; nothing else does.**"*

It has never been answered. That is why the card he opened reads as it does.

## Edward Richards Allen, the case that raised it

| appearance | date | class |
|---|---|---|
| `poll_1834` — "Allen, Edward" | 1834 | an 1834 civic list |
| **Chicago Democrat letter list — "Edward Allen"** | **1835-05-20** | **an 1833-35 newspaper, printing him by name** |
| Fergus 1839 / 1843 — "druggist, Leroy M. Boyce" | 1839, 1843 | later evidence |
| Chicago Tribune, Old Settlers' fourth reception | 1882 | later recollection, corroborates pre-1840 residence |

He is graded **G2b — inferred** ("an 1833 or 1834 list with another source"). The letter list of
20 May 1835 is the only appearance that could reach **G1b — attested** ("a contemporary record
naming the person in Chicago — the 1833-1835 newspapers, which print the person by name in the
town"), and G2e is exactly the rule that declines to let it.

So: a man named on an 1834 Chicago poll list, named again in a Chicago paper in May 1835, printed
as a Chicago druggist in 1839 and 1843, and received in 1882 as a settler of Chicago before 1840,
is `inferred`. The owner's instinct that this reads wrong is a fair reading of that card.

## What is measured, so the ruling is made on figures

Counted over `data/residents/households/` on dev, 2026-09-04:

| | |
|---|---|
| people graded `inferred` citing **2 or more** sources | **54** |
| …of those, carrying an 1833-35 newspaper **letter-list** appearance | **11** |
| by rule: G2b 33 · G2c 3 · **no ladder_rule at all 18** (that is T-0692, not this ticket) | |
| letter-list names fleet-wide the policy doc says a G1b reading would lift | **~1,500** |

**11 people move on this ruling here; ~1,500 move when the ladder is applied to the whole corpus.**
That gap is the reason to rule deliberately rather than case by case.

## THE COUNTER-ARGUMENT, WRITTEN OUT, because the cautious half has a real basis

A letter list is the post office advertising **uncollected mail**. It is evidence that somebody
*sent* to that person at Chicago — not that the person was standing in Chicago. It is the one class
of source in this project where the name's presence is an act by a third party rather than by the
person. That is a genuine distinction, and it is why the tool graded it down rather than up.

**It is also why the count alone must not decide it.** The ratified ladder grades by the CLASS of
evidence, never by how many appearances there are — G4 says so explicitly: *"Two or more
appearances, none of them of a class a rung above accepts"* stays `inferred`. A rule of the shape
"two sources means attested" would make a man attested on two 1843 directory entries, which the
ladder's own G0 forbids in the same breath. **This ticket does not propose that rule and should not
be closed by implementing it.**

## The ask

1. **Put the question to the owner in one sentence and record the answer in the ledger** — not only
   in a PR comment. The last two rulings this project needed were both lost that way (T-0673 records
   the triangle fork that was never filed; T-0426's fence ruling was made on 2026-08-31, implemented,
   and stranded for four days).
2. If he rules a letter list **IS** G1b: change the one line of `grade()`, re-run
   `consolidate_resident_evidence.py --build`, and land the regrade as its own PR with the before/
   after counts — expect roughly 1,500 names to move, so it is a slice of its own, not a rider.
3. If he rules it is **NOT**: G2e stands, and the policy doc gains the ruling with its date so the
   next reader meets the answer instead of the argument. **Allen's card then also gains a sentence
   saying why a man in four sources is `inferred`** — the grade is defensible but the card does not
   currently defend it.
4. Either way, **`hh_allen_edward_richards.json` is the worked example** and should be named in the
   policy doc, because it is the clearest case of the tension the ruling resolves.

**Done when** the ruling is written in `docs/RESEARCH/resident-grading-policy.md` with its date and
the owner's words, `GRADE_RULES` agrees with it, and the count of `inferred` people carrying 2+
sources is either explained on their cards or moved.
