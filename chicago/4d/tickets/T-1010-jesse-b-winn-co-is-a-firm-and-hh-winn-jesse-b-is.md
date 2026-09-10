---
id: T-1010
title: Jesse B. Winn & Co. is a firm, and hh_winn_jesse_b is a resident card minted from a crop that had lost the '& Co.'
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

Jesse B. Winn & Co. is a firm, and hh_winn_jesse_b is a resident card minted from a crop that had lost the '& Co.'.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-1008, which read the printed line and could not act on it inside its own run.

Line 163 of the 1 January 1834 return prints **`Jesse B. Winn & Co.`**. Both crops of that
return lost the `& Co.` — the 1834-01-28 crop reads `Jesse B. Winn` — so refusal 2 of
`tools/mint_letter_list_residents.py`, `a firm, not a person`, never saw a firm, and
`hh_winn_jesse_b` was minted as a man. Claim c033 of `chicago_democrat_1834_03_04` now
carries the printed line as a firm and the mint refuses IT correctly; the card minted from
the truncated reading stands beside it, unaffected, because the two are different gazetteer
entries.

**Why T-1008 did not just retire it.** Unminting a resident is the same decision as minting
one, and this one is not obvious: a firm styled `& Co.` has a principal, and `Jesse B. Winn`
may well be him. The three candidate answers are (a) retire the card and let the firm stand
in the business register, (b) keep the card and record that its only evidence is a firm
line, (c) keep the card and cite the firm line as evidence of the man behind the firm. The
first is a withdrawal, the third is an inference nobody has argued. **Acceptance:** one of
the three is chosen with the reasoning written down, the card and the claim agree, and if a
card is retired it goes to `data/residents/merged/` whole, the way T-0723 retired
`N. R. Norton`.

**Links:** T-1008 (the read) · L214 (the scale of the letter-list cohort) ·
`data/research/newspapers/letter_list_1834_01_01_printed.json` (`printed_length.addressee_lines_that_are_firms`)
