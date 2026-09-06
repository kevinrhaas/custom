---
id: T-0862
title: The card rename of T-0721 broke the register's link to two townspeople: Abbot and Gabbs are proposed as new residents the town does not hold
state: open
epic: META
requested_by: loop
seen: false
effort: S
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

**Measured on `dev` at 4366ffbba, 2026-09-06, against 37b3c03a9~1 — the commit before
T-0721's PR #921 landed.**

`data/research/newspapers/register_1835.json` crosswalks every name the papers print
against the town's own cards, and says of each one whether the town already holds the
person (`enrich`, with the `action_target` naming the card) or does not (`new_resident`).
It matches on the card's stored NAME.

PR #921 settled T-0721 by rewriting the stored display name of the three digit-bearing
letter-list cards — `8. G. Abbot` became `[?] G. Abbot`, `James I1. Gabbs` became
`James [?] Gabbs` — and the crosswalk's match went with it:

| printed name | before #921 | on dev now |
|---|---|---|
| `Abbot, 8. G.` | `enrich` → `abbot_8_g` | `new_resident`, target `null` |
| `Gabbs, James I1.` | `enrich` → `gabbs_james_i1` | `new_resident`, target `null` |
| `Perry A. 8.` | `new_resident` | `new_resident` (unchanged) |

`counts.persons.by_action`: `enrich` **1373 → 1371**, `new_resident` **1233 → 1235**.

So the register now states, of two people the town holds under `hh_abbot_8_g` and
`hh_gabbs_james_i1`, that they are "a named person the town does not hold. Known only from
the post-office letter lists." That sentence is false of both, and it is the exact class of
untruth T-0692 was opened over: a derived file whose stated reason does not describe the
record it is about. `tools/compile_register.py` line 1407 is where it is written.

Nothing appears to have been minted twice as a result — `mint_letter_list_residents.py`
derives its household id from `plain_fragment()` over the PRINTED name, not the card's
display name, so it still lands on the existing card, and its `--gate` is green. The fault
is the register's ASSERTION, and the fragility underneath it: the crosswalk's link to a card
is only as stable as that card's display string, and this project renames display strings
whenever a reading is corrected (T-0638 moved 36 of them).

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

1. `Abbot, 8. G.` and `Gabbs, James I1.` read `enrich` against `abbot_8_g` and
   `gabbs_james_i1` again, with the counts back to 1373/1233 for those two rows.
2. The link survives a display rename. Whatever the fix — matching on the printed name the
   card was minted from, on the person id, or on the bracket-stripped name — a card whose
   display string changes must not silently become a stranger to the register. State which
   was chosen and why.
3. A gate says so. The register is derived and re-derives on `check.sh`; add the assertion
   that no `new_resident` row names a printed name a committed card was minted from, or
   demonstrate why that invariant cannot hold.

**Found by** the run that was building a rival fix for T-0721 (PR #963, closed unmerged
when #921 landed): it measured the two register states above while comparing the two
approaches.

**Links:** T-0721 · T-0638 (the rename pass that moves display strings) · T-0692 (a stated
reason has to be true of the record).
