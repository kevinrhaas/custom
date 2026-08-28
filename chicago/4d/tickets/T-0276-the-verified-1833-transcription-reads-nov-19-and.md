---
id: T-0276
title: The 'Verified' 1833 transcription reads NOV. 19, and the Democrat published no such issue
state: blocked-owner
epic: PAPERS
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: Does the top of the first supplied 1833 scan page read NOV. 19 or NOV. 26? The scans are yours; the answer decides whether the deposit holds an issue this project does not know about, or the transcription misread its own masthead.
needs_bake: false
---

`chicago/reference/newspapers/Transcriptions/Chicago_Democrat_1833-11_to_1835-08/Chicago_Democrat_1833_11-16-Verified_Transcription.docx`
is the one artifact in the deposit whose filename carries no issue date, and its
identification is the only judgement in `data/research/newspapers/corpus.json` that is
not a reading. T-0256 attached it to **1833-11-26** as an `alternate` witness at
`inferred`, with the reasoning on the record, and it should not stay there
unexamined.

## What the artifact says about itself

- It is headed *"Best-effort verified reading transcription of the three supplied scan
  pages"*. THREE supplied images of an 1833 Democrat is exactly the scan set
  `data/sources/chicago_democrat_1833_11_26.json` describes and was verified against
  ("THREE page images, and they are NOT in issue order"). That is the whole of the
  reasoning for attaching it to 1833-11-26.
- Its filename says `1833_11-16`. The Democrat published no November 16 issue.
- Its own first page reads **"Visible date at the top of this supplied page: NOV. 19,
  1833."** The Democrat published no November 19 issue either: Vol. I, No. 1 is
  November 26, 1833, and nothing preceded it.

Two different non-dates for one artifact, and the corpus workflow's rule 2.3 forbids
silently repairing a visibly printed date — so both are preserved and neither is
resolved.

## Why this is the owner's

It is settled by looking at the scan, and the scans are his. The question is one
sentence: **does the top of the first supplied page read NOV. 19 or NOV. 26?** If 19,
the deposit holds a Democrat issue this project does not know about and the per-issue
source record's account of the scan set is wrong. If 26, the transcription misread its
own masthead and the attachment is correct.

Note what rides on it: the 1833-11-26 record is this dataset's **first contemporary
Chicago document** and its senior tier-1 textual source.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The owner has read the date at the top of the first supplied scan page.
- `corpus.json`'s `identification` for that artifact is `documented` with the source
  record naming the scan, or the artifact is moved to its own issue entry — not left
  at `inferred`.
- If a November 19, 1833 Democrat exists, `data/sources/chicago_democrat_1833_11_26.json`
  is corrected, because everything downstream inherits its account of the scan set.
