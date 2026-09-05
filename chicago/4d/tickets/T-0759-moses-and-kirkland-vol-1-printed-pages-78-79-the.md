---
id: T-0759
title: Moses and Kirkland vol. 1, printed pages 78-79: the list of actual settlers prior to 1830 with its NAME / NATIVITY / date / REMARKS columns, read off the page images
state: open
epic: META
requested_by: loop
seen: false
effort: M
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

Moses and Kirkland vol. 1, printed pages 78-79: the list of actual settlers prior to 1830 with its NAME / NATIVITY / date / REMARKS columns, read off the page images.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0581**, which read the footnote that introduces the table and could not read
the table.

Moses and Kirkland, *History of Chicago, Illinois* vol. 1 (1895), printed pages 78-79 —
scan leaves 102-103 of the project's deposit, item `historyofchicago01mose_202609`. The
footnote IS read and is claimed at `bk_mk1_033`: the list "contains the names of all those
who are known to have had a residence at the settlement, nearly all of whom paid taxes in
1825, and voted in 1826", and it explains that Gurdon S. Hubbard is left out because he was
not permanently resident until 1832. **The table itself — "LIST OF ACTUAL SETTLERS AT
CHICAGO, PRIOR TO 1830", set in four ruled columns (NAME, NATIVITY, a date, REMARKS) — is
rubble in the hOCR search text.** Lines 1218-1232 of
`data/research/books/text/moses_kirkland_history_of_chicago_v1_1895.txt` carry about forty
surnames and stray fragments of remarks ("Voted in 1830, died at Summit, 1849", "1824") with
no way to tell which remark belongs to which name.

**Why it is worth a run.** NATIVITY is the column this project has almost nowhere else: a
birthplace against a name, for the whole pre-1830 settlement. The REMARKS column carries
arrival years and deaths. Both feed the residents and households layers directly.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- The table read off the PAGE IMAGES, not off the search text, and graded `scan_verified`.
- Every row that reads — name, nativity, date, remark — written into the `books` domain in
  the T-0492 claims shape, with unreadable cells declared unread and never inferred from a
  neighbour.
- The list crosswalked against the 1825 tax list (`bk_mk1_031`) and the 1826 voter list,
  which the footnote says it mostly reproduces — including the disagreements.
