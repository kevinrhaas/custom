---
id: T-0319
title: The 1 March 1834 letter list survives only as surnames, and the page images would finish it
state: open
epic: PAPERS
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

The Chicago post-office letter list printed in the *Chicago Democrat* of 1834-03-04, page 4
columns 2-3, is the densest record of who was living in the town in the spring of 1835's
year-before — and T-0312 could mint only EIGHT names out of it.

**What is wrong, and it is mechanical rather than a judgement.** The deposit's segmenter cut
that printed column at its LEFT EDGE, so the list reaches the transcription with the forenames
sheared off: `ell Baldwin`, `nel Devoe`, `il. Frazer`, `3, Haight`, `». Johnson`, `c Killigoss`.
Seventy-eight lines of the list survive — nineteen in the first half and fifty-nine in the second,
hand-counted — and the gazetteer keys on the WHOLE normalized name, so a bare surname cannot be
minted without inventing the half that is missing. T-0312 quoted all seventy-eight verbatim as
claims c024 and c025 of `extracted/chicago_democrat_1834_03_04.json` and minted the eight entries
that carry a legible forename or initials. Seventy-eight is a floor on LINES, not a count of
entries: at least one name is broken across two lines and at least one line carries two.

This is the same damage T-0310 recorded for the 1 January 1834 list, where ninety-seven names were
minted and the ticket said the number was a floor. The two lists together are the town's census
proxy for the winter and spring of 1834, and both are short by the same mechanism.

**Two things this ticket should also fix while it is in there**, both found by T-0312:

- The heading is CUT ACROSS A COLUMN BOUNDARY — `List of L` ends page 4 column 2's first line and
  `ost-Offiee at Chica-` opens column 3 — which is why no keyword sweep had ever found this list.
  `data/research/newspapers/README.md` now says so. The cheap generalisation is a sweep for the
  FRAGMENTS across the whole deposit (a line ending `List of L`, a line beginning `ost-Off`, a bare
  `P.M.` at a column foot) rather than for the phrases, which would say whether any other issue in
  the corpus is hiding a list the same way. Do that before reading images: it may be more than one.
- The Democrat of 1834-03-04 is available as a `.docx` as well as a `.txt` in the deposit. Whether
  the `.docx` extraction preserves the left edge this `.txt` lost has not been checked, and if it
  does the list can be finished without page images at all.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The fragment sweep is run over the whole deposit and its result is written down — either "no
  other issue hides a list this way" or the list of issues that do, as tickets.
- Every entry of the 1834-03-04 list that a fuller witness can read is minted, with the witness
  named in the claim's note; entries that no witness can complete stay unminted and are counted.
- The count minted is stated against the seventy-eight surviving lines, and against a hand count
  of the printed list if a page image is read.
- `tools/compile_gazetteer.py --check` green, and the claims edited in place rather than added
  beside the existing c024/c025 — one list, one pair of claims.
