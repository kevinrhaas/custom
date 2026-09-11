---
id: T-0867
title: The Fergus 1843 crosswalk reads 'none_recorded' as a trade, so could_carry_occupation is 0 where Norris's fixed twin reports 63
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: 2026-09-10
pr: 1098
claimed_by: run 9/10/2026, 7:43:01 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-11T01:35:27.798Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34547403898
---

The Fergus 1843 crosswalk reads 'none_recorded' as a trade, so could_carry_occupation is 0 where Norris's fixed twin reports 63.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

## Folded in from T-0868 (2026-09-10) — two normaliser fixes on the same two directories, one run

*T-0868: Norris 1844 normalizes 'Jones, B. & Co. dry goods and groceries' as a person, not a firm, so the firm filter never sees it*

Norris 1844 normalizes 'Jones, B. & Co. dry goods and groceries' as a person, not a firm, so the firm filter never sees it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Every entry of this shape filed as a firm, not the one the ticket names; the MEMBERSHIP
  entry ("Eddy, Ira B. of Eddy & Co.") and the EMPLOYMENT entry ("Anderson, Wm. blacksmith,
  at Perkins & Fenton's") held back, because both are men.
- The rule machine-checked in `read_norris_1844.py --self-test`, which the gate runs, so a
  row that stops parsing this way is a regression and not a reading moving.
- Both crosswalks regenerated and their movement accounted for.
- `bash tools/check.sh` green.

## WHAT WAS DONE (2026-09-11)

**The 1843 trade (T-0867).** `crosswalk_fergus_1843.py` tested `if not r["occupation"]`, and
the residents layer writes the string `none_recorded` where it holds no trade — the field's
most common value, and truthy. So every match read as already having a trade and
`could_carry_occupation` reported **0**. It is **72**. The predicate is now `tiebreak.is_trade`,
which this file already imported for the discriminator, and it is now the ONE copy for all
three directory crosswalks: `crosswalk_norris_1844.py` carried a private `blank_occupation`
(T-0569 fixed the same bug there a month earlier) and `crosswalk_fergus_1839.py` carried a
private tuple. Both were swapped to it and both re-derive byte-identically — that is why the
same bug could be fixed in one volume and stay live in the next, and it is now unrepeatable.

**The firm past the comma (T-0868).** `read_norris_1844.split_entry` tested `FIRM` against
`head.split(",")[0]`, because the volume alphabetises a firm under its first partner and an
ampersand deeper in the line is usually a trade's or an employer's. But the volume also
INVERTS a firm, and then the marker lands past that comma. **Forty** entries read as people.
`SEVERED_FIRM` catches the shape — the trade begins with the ampersand, immediately after the
forename run — and `NOT_A_FIRM_HEAD` holds back the two membership entries, which are men.
The firm's name is sliced from the printed head so it keeps the compositor's punctuation
("Adams, W. H. & Co.", not the split's stripped "W. H").

**What moved, and it is the point.** Those forty phantom people stood in the 1844 surname
index, so a real man whose own entry was there met TWO listings and was refused as AMBIGUOUS.
Norris matches 99 → **104**, ambiguous 24 → **19**: W. H. Adams, Stephen F. Gale, Benjamin
Jones, D. A. Jones and George Smith were each being refused their own directory entry by a
business that shares their name. `could_carry_occupation` 64 → 66, `could_carry_address`
74 → 79. All five new matches are to the line stating their PARTNERSHIP, whose parse
`spend_directories.py` rule 3 already refuses to cross, so the directories `unwritten`
ceiling moves by exactly those five and the raise says so in those words.
