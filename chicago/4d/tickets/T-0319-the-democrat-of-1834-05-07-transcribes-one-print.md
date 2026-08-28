---
id: T-0319
title: The Democrat of 1834-05-07 transcribes one printed page twice and the other not at all
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---
`corpus.json` says the Democrat of 1834-05-07 (Vol. I No. 23) is four printed pages from
PDF pages 21-24, and the transcription carries four `ISSUE PAGE n` blocks. **The block
marked ISSUE PAGE 4 / SOURCE PDF PAGE 24 is a second reading of the same printed columns
its ISSUE PAGE 2 block carries** — so this issue's printed page 4, which on every other
issue in the run is an advertising page, is not in the transcription at all.

Found while reading the month for T-0314. Verified column for column at four independent
points, which is why it is filed as a fact rather than a suspicion:

| the same printed lines | as ISSUE PAGE 2 | as ISSUE PAGE 4 |
|---|---|---|
| the steamboat explosion, `Mrs. Moore and …` | lines 1442-1443 | lines 3549-3550 |
| the 'CLINTON' canal letter, `…ny other mode; for where the pros-` | lines 2380-2381 | lines 4478-4479 |
| the infant-school letter, `…Sir,—On the evening of` | lines 2394-2396 | lines 4490-4492 |
| the New York election squib, `In the late New York elections` | lines 2412-2431 | lines 4650-4654 |

The two readings are cut at DIFFERENT offsets, so they are complementary and the pass used
them that way (T-0314's claim c001 reads its salutation off both). That is the one benefit;
everything else about it is loss.

**Why it matters beyond one issue.** The other three issues of May 1834 were swept the same
way and are clean, so this is not a systematic defect — but nothing in the repo would have
caught it. `newspaper_corpus.py` counts column markers and `compile_gazetteer.py` resolves a
locator against them; neither asks whether two blocks of one transcription are the same text.
A duplicated page inflates the corpus's own `text_chars` and column counts, and a missing
advertising page is silently absent from a reading pass that believes it read the issue.

**Options, and the second is probably right:**

1. Treat it as a deposit defect and record it on the issue's `corpus.json` entry only.
2. Add a **duplicate-block check** to `newspaper_corpus.py --check` that compares the
   normalised word bags of an issue's page blocks and reports any pair over a threshold,
   then sweep all 66 deposit `.txt` and all 23 derived ones with it. A word-bag
   `quick_ratio` of 0.63 separates this pair from every other pair in the month; the sweep
   is what would say whether the threshold generalises.
3. Ask the owner whether the missing page can be re-transcribed from the scan. That is a
   deposit question and not the loop's to answer.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Every issue in `corpus.json` is swept for duplicated page blocks by a committed check, and
  the sweep's result is recorded — the count of duplicates found, or none.
- The 1834-05-07 entry in `corpus.json` carries the finding in its `notes`, naming the four
  verified line pairs above.
- If the check is added it fails on this issue before it is quieted, and the way it is
  quieted is a recorded exception on that issue and not a raised threshold.
