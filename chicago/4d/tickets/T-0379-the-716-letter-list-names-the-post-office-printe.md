---
id: T-0379
title: The letter-list names the post office printed in a single return, and the change of scale they put to the town
state: blocked-owner
epic: PAPERS
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0374
opened: 2026-08-29
closed: null
pr: null
claimed_by: run 8/29/2026, 4:26:41 PM CT
blocked_on: How many of the 705 single-return letter-list names should this town hold? A: all 705 (237 -> 942 people, 76.1% of the town a post-office name and nothing else). B: the dated head — the return of 1 July 1835 alone is 312 of them (237 -> 549, 59.0%), and the ticket carries the whole ladder by return. C: a lighter form than a household, which needs its own ticket to describe. Re-derive any of it with tools/mint_letter_list_residents.py --scale-report.
needs_bake: false
---

The letter-list names the post office printed in a single return, and the change of scale they put to the town.

Piece 2 of 2 of **T-0374 — letter_list_only reaches the visitor's card, and the 1,536 names known only from the post office**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**THE MEASUREMENT, so this is a decision and not a survey** (taken on dev at caefea5b).
1,907 register persons carry `letter_list_only` and the town does not hold them. Through
the eight refusals `tools/mint_documented_residents.py` derives — garbled 476, first
evidence after the scene date 310, surname already minted 250, the town already names that
family 101, placed outside the town 22, firms 12, a surname and nothing else 10 — **726
survive**, and T-0378 takes the twelve of them the post office printed in more than one
return. **This ticket is the other 714.**

Every one of the 714 is printed in exactly one return of uncalled-for letters, with no
trade, no place and no second sighting. Minting them would take this town from 237 people
to 951 and its households from 201 to 915 — three residents in four would be a name on a
post-office list and nothing else, and the residents panel a visitor opens would be mostly
that.

**This is a question for the owner before it is work for a run.** His ruling of 2026-08-28
is that a letter-list name is enough to make somebody a resident, and this ticket does not
dispute it; what it cannot decide on its own is whether the reconstruction should HOLD all
714 as households, hold them in a lighter form the panel can carry, or hold the ranked head
of the list. `ticket.mjs block --owner` is the honest first move on it, with these numbers.

**Acceptance:** (state it before working — never weakened to pass)

- The scale question answered by the owner, in writing, before any record is minted.
- Then whatever he rules, derived by rule and gated by `--check`, occupation absent, and
  `town_census.json` moving additively.

---

## THE QUESTION AS PUT TO THE OWNER — 2026-08-29, re-derived on dev at c658a7b6

The figures above were measured on dev at `caefea5b`. The corpus has moved since (the
identity layer, the anchor rule and the street-face policy all landed after it), so
they are restated here rather than relied on: **705 names survive, not 714**, and the
town would go from 237 people to 942 rather than from 237 to 951.

Nothing here is a survey. `tools/mint_letter_list_residents.py --scale-report` prices
the cohort through the **same eight refusals, in the same order**, that the committed
two-return pass mints by — the refusal pass was lifted into `apply_refusals()` for
exactly this reason, so the price cannot drift away from the rule that sets it. Refusal
7 additionally sees the twelve households T-0378 already minted, because they are
committed and standing. Re-run it on any tree; it will answer for that tree.

```
T-0379 — THE SINGLE-RETURN COHORT, PRICED THROUGH THIS PASS'S OWN REFUSALS

THE POOL — letter-list-only names the town does not hold: 1907
     18 printed in more than one return   — minted by this pass (T-0378)
   1889 printed in exactly ONE return      — T-0379's question

THE EIGHT REFUSALS over those 1889, in the order they are applied
    471  garbled
    310  first evidence after the scene date
    225  surname already minted
    134  the town already names that family
     22  placed where this project cannot put him in the town
     12  a firm, not a person
     10  a surname and nothing else
  -----
   1184  refused, and 705 survive

OPTION A — HOLD ALL 705
  persons       237 -> 942
  households    201 -> 906
  of the people a visitor could open, 76.1% would be a name on a post-office list and nothing else
  (today: 12 of 237, 5.1%)

OPTION B — HOLD THE DATED HEAD. Survivors by the return that printed
  them, newest first; the running column is the cost of taking every
  return down to and including that row.
           return of  survivors    persons  % of town
         1 July 1835        312   237 -> 549       59.0%
         20 May 1835        128   237 -> 677       66.8%
     22 October 1834         54   237 -> 731       69.2%
        16 July 1834          6   237 -> 737       69.5%
         9 July 1834         61   237 -> 798       71.8%
         2 July 1834         55   237 -> 853       73.6%
        8 April 1834          6   237 -> 859       73.8%
        1 April 1834         48   237 -> 907       75.2%
     28 January 1834         35   237 -> 942       76.1%

OPTION C — HOLD THEM IN A LIGHTER FORM than a household. What a record
  costs today, so the alternative can be priced against it: each of the 12
  households this pass minted is one person, one file, and no dwelling,
  division, family or party — every absence written out in its own block.
  705 more of those is 705 files and 705 households whose `lives_at` names nothing.
```

**THE THREE ANSWERS, and what each one costs.**

- **A — hold all 705.** The reconstruction becomes a post-office list with a town
  attached: 76.1 per cent of the people a visitor can open would be a name and nothing
  else, against 5.1 per cent today. The evidence is sound under the owner's ruling of
  2026-08-28; the objection is not to any one record but to what 705 of them do to the
  thing a visitor is looking at.
- **B — hold the dated head.** Every name here is in exactly one return, so `returns`
  cannot rank them and `printings` counts a reprint run rather than evidence. What does
  vary is WHEN the office held the letter, and the single return of **1 July 1835 — the
  scene date itself — carries 312 of the 705 on its own.** That cut takes the town to
  549 people, 59.0 per cent letter-list, and every name in it is one the post office was
  holding a letter for on the very day this reconstruction depicts. Adding the return of
  20 May 1835 makes it 440 names, 677 people, 66.8 per cent. The table above is the
  whole ladder.
- **C — hold them in a lighter form.** Not costed here beyond what a record costs
  today, because the shape of a lighter form is the owner's to describe: a roster the
  residents panel lists without minting a household is a different data model, not a
  smaller number of the same one, and it would need its own ticket.

**What is NOT in question**, so the ruling can be narrow: whether a letter-list name
makes a resident (the owner ruled yes, 2026-08-28), whether these people are refusable
on evidence (the eight refusals have already taken 1,184 of the 1,889), and whether
`letter_list_only` stays legible on the card (T-0378 shipped it). The only open question
is **how many of the survivors this town should hold**, and it is a question about the
reconstruction rather than about the sources.

**A boundary the owner may want to weigh with it.** A letter waiting at Chicago is
evidence that somebody believed the addressee reachable there — the office served the
country around the town as well as the town itself. Refusal 6 catches only the 22 the
corpus places elsewhere by name; it cannot catch a settler the corpus never places at
all. At 12 records that limit is a footnote on each of them. At 705 it is a property of
the town.
