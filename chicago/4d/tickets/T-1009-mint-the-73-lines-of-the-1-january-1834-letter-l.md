---
id: T-1009
title: Mint the 73 lines of the 1 January 1834 letter list that no transcription reached — the printed list is read, the names are not on cards
state: open
epic: META
requested_by: steward
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

Mint the 73 lines of the 1 January 1834 letter list that no transcription reached — the printed list is read, the names are not on cards.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

T-0424 read the Chicago post office's 1 January 1834 return at the deposit's own page
scans and found it is **170 printed lines**, 169 personal names, in two alphabetical
sub-columns of 85. The whole of it is committed, line by line, at
`data/research/newspapers/letter_list_1834_01_01_scan.json`.

The town does not hold most of it. T-0310 minted 97 residents from a .docx transcription
of the 1834-01-28 impression that had crushed the two columns into eight paragraph lines;
T-0312 minted 79 more off two crops of the 1834-03-04 impression, and T-0424 has now put
the right name on 75 of those. **Seventy-three printed lines have never reached a card**,
and under the owner's ruling 1 — a letter-list name is enough — each of them is a resident
candidate.

This is deliberately NOT part of T-0424. Minting is the pass that adds people to the town,
and it needs its own demonstration: the mint runs through
`tools/mint_letter_list_residents.py`, every new card lands `letter_list_only` with an
arrival bound dated by the RETURN and not by the impression (T-0425), and the surname
collision report has to be re-run over a list that has grown by three quarters.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Every printed line of `letter_list_1834_01_01_scan.json` is either on a card or recorded,
  by line, as a line that must not be minted — the two firms (`Axtel & Steele`,
  `Jesse B. Winn & Co.`) and any line the identity layer folds into a person the town
  already holds.
- `Lamira & Laura Carrier` is TWO people, and the page says so with an ampersand. Whatever
  the mint does with that line, it does not do it by accident.
- The trailing numerals are counts of letters waiting, never part of a name, and no card
  carries one.
- The collision report and the letter-list gate re-derive over the grown list, and the
  count of residents this project holds moves by a stated number with a stated reason.

**Links:** T-0424 (the reading, and the 170) · T-0310 (the 97) · T-0312 (the 79) ·
T-0299 (mint once, record the reprints) · T-0425 (the bound is dated by the return) ·
`tools/mint_letter_list_residents.py` · `tools/report_letter_list_collisions.py`
