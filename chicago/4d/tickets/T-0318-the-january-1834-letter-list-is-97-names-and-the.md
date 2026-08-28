---
id: T-0318
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

## Update, 2026-08-28 (T-0311): there is a THIRD printing, and the images are no longer the only route

T-0311 read February 1834 and found the same 1 January 1834 list printed twice more —
**whole on 1834-02-04 (page 4, columns 2 and 3)** and woven through the poetry column on
1834-02-11. The February issues are in the RULED dialect, transcribed one printed line to
one file line, which is the thing the January `.docx` extraction could not do.

So the claim above that "the two printings do not repair each other and the images are the
only route" was made without two witnesses that exist, and it is half wrong:

- **A to G is repaired without a scan.** 1834-02-04 page 4 column 2 sets that run one name
  to a line. `William Cr[…]` is **William Criss**; `[?] Devoe` is **Samuel Devoe**;
  `[uncertain: Dagenet]` is **Noel Dagenet**; `[?] Gooding` is **Jos. A. Gooding**;
  `[uncertain: Childress]` is **James Childress**; `[uncertain: D. P. Cleviny]` is **D. P.
  Clevinger**; `[uncertain: Orinda Guryl]` is **Orinda Gary**; `G. W. Ewin[g]` is **G. W.
  Ewing**. About twenty names January does not carry at all are added.
- **H to W is not.** The same printing's column 3 has every initial cut away by the crop —
  seventy-three bare surnames, minted by nobody. January is the better witness there.

What is left for this ticket is therefore the H-to-W residue, the two readings where the
witnesses disagree (`I. K.`/`J. K. Blodgett`, `Jane Forster`/`Jane Forrister`), and the
`scan_verified` upgrade. The identity merges the repairs imply were deliberately NOT
declared by T-0311, because several are same-surname pairs the gazetteer refuses to merge
and the rest turn on one damaged letter; settling them off the images is this ticket's.

**Links:** T-0311 (`data/research/newspapers/coverage.json`, the 1834-02 range) ·
`extracted/chicago_democrat_1834_02_04.json` claims c013 and c014.
