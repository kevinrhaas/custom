---
id: T-0341
title: A bare surname can never be joined to its forename: the family rule reads 'no initials' as 'different initials'
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

A bare surname can never be joined to its forename: the family rule reads 'no initials' as
'different initials'.

`tools/compile_gazetteer.py` refuses a merge when `surname(into) == surname(frm)` and
`initials(into) != initials(frm)`, "with or without a rule (the letter lists are full of
families)". That rule is right and it should stay. But `initials()` returns an empty tuple
for a name with no forename at all, and an empty tuple is not equal to `('a','o','t')`, so
the guard fires on the one case it was never aimed at: joining a bare surname to the SAME
surname with a forename supplied.

**Measured on 2026-08-29 while working T-0323**, by compiling the real corpus with one probe
merge at a time:

| merge probed | verdict |
|---|---|
| `[?] Blodget` → `[uncertain: Avice] Blodget` | refused, "same surname, different initials" |
| `[?] Breed` → `A. O. T. Breed` | refused, same |
| `[?] Devoe` → `[…]nel Devoe` | refused, same |
| `[?] Temple` → `[Lew]is Temple` | refused, same |
| `Lewis Tem[…]` → `[Lew]is Temple` | accepted — because the CUT surname is a different string |

The last row is the tell. A name cut in its SURNAME can be repaired, because the truncation
changes the surname slug; a name cut in its FORENAME cannot, because the truncation changes
nothing the guard looks at. That is backwards: a surname repair is the riskier of the two,
and it is the one the policy lets through.

**What it costs, today.** T-0323 read the third printing of the 1 January 1834 letter list
and closed the readings of four January bare surnames — `[?] Blodget` is A[l]vice Blodget,
`[?] Breed` is [A]. O. T. Breed, `[?] Devoe` is Samuel Devoe, `[uncertain: Dagenet]` is Noel
Dagenet. Two of those four have the completed person already standing in the gazetteer from
another issue, and neither could be declared. The evidence exists, the judgement is written
out, and there is no admissible way to record it — so the gazetteer keeps counting one man
twice, which is exactly T-0299's complaint.

**This is a policy question and not only a code one.** `identity.json`'s own note says the
family rule binds "rule or no rule", so widening it is the owner's call, not a refactor. The
narrowest change that would do the work: allow a merge when one side has NO forename at all
and the other's initials are not contradicted by it — refuse `[?] Cohen` → `P. Cohen` while
`J. Cohen` also stands, and refuse it whenever more than one forenamed bearer of that surname
is in the corpus, which is the family case the rule was written for.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The owner rules on whether a bare surname may be joined to a forenamed bearer of the same
  surname, and on what test guards it. `block --owner` until he has.
- If allowed: `compile_gazetteer.py` implements exactly that test, the self-test carries a
  case per branch — allowed, refused for a second bearer, refused for contradicted initials —
  and `identity.json`'s note states the widened rule in the same words the code enforces.
- The four T-0323 readings above are then declared or explicitly left undeclarable, with the
  reason on T-0318.

**Links:** T-0323 (the reading that hit this) · T-0318 (the names waiting on it) · T-0337 and
T-0338 (the same question asked of FIRMS, where the initial rule was deliberately dropped) · T-0299
(the same-list-different-OCR duplicates) · `data/research/newspapers/identity.json`
