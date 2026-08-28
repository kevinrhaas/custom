---
id: T-0316
title: The January 1834 letter list is 97 names and the printed list was longer; the page images can close the gap
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

The January 1834 letter list is 97 names and the printed list was longer; the page images can close the gap.



T-0310 read the list of letters remaining in the Post Office at Chicago on 1 January 1834
(`chicago_democrat_1834_01_28`, page 4 column 2, lines 1105-1127) and minted **97 residents**
from it under ruling 1. Ninety-seven is a floor, not the printed length.

The `.docx` extraction crushed the printed list's two alphabetical columns into eight
paragraph lines, interleaving them, and it left orphan debris exactly where names stood:

| line | debris |
|---|---|
| 1111 | `Me print ofl Coram amor Hei otinan Wor in vard` |
| 1117 | `pe see` |
| 1119 | `onger areita`, `Thomas OF ae 3` |
| 1121 | `if 1 LabiteLase Cemier Go Bene`, `ps` |
| 1123 | `ef` |

Four names in the extracted set are cut surnames — `William Cr[…]`, `Gustavus C[…]`,
`Benj. Cl[…]`, `Lewis Tem[…]` — and seven more are bare surnames with no initial. Each of
those is a person in the gazetteer under a name nobody can match against another record,
which is the concrete cost.

The same list is printed a second time, a fortnight earlier, at
`chicago_democrat_1834_01_14` page 4 column 2 (lines 1063-1075), where it is cut even
harder by W. Kimball's store advertisement — so the two printings do not repair each other
and the images are the only route.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

The list is read off the page images, the extracted count is stated against a hand count of
the printed list, the four cut surnames and the seven bare ones are either completed or
reported unreadable at the image too, and the claim's `reading` becomes `scan_verified`.
`coverage.json`'s T-0310 note then states a count instead of a floor.

**Links:** T-0310 (the month, and the claim) · `data/research/newspapers/identity.json`
(the rule that keeps same-surname-different-initial apart, which is what makes the bare
surnames unmatchable) · `data/research/newspapers/README.md` § Quality is not uniform.
