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

---

**POSTSCRIPT, 2026-08-28, from T-0311 (February 1834 read) — most of this gap is closed, and
NOT by the page images.**

The premise above is that "the two printings do not repair each other and the images are the
only route." There are not two printings. There are **seven**: the same 1 January 1834 list is
reprinted in ALL FOUR issues of February 1834 as well as the two January ones, and the February
ones are `.txt` transcriptions in the ruled dialect, which put **one name per line with its
initial** where the January `.docx` crushed two alphabetical columns into eight paragraph lines.

T-0311 minted the list from the two best of them — the first half (A-H, 71 names) from
`chicago_democrat_1834_02_04` page 4 column 2, the second (H-W, 74 names and the postmaster's
signature) from `chicago_democrat_1834_02_11` page 4 column 3 — under a stated one-list-one-cohort
rule, per half because no single printing carries the list whole. **87 of those 146 entities are
people the corpus did not hold**, and among them are readings for names this ticket lists as its
concrete cost: `Lewis Tem[…]` is **Lewis Temple**, and the bare surnames `Killigoss`, `Kercheval`,
`Parsons` and `Sprague` now stand beside initialled neighbours that make the column order legible.

**WHAT IS LEFT, and it is a real remainder.** The printed list ran in TWO alphabetical
sub-columns and the segmenter kept only the left one in every printing; the right survives as
line-end debris (`Edwar`, `Isanc K`, `Lewis |`) in all seven. So the floor is much higher and it
is still a floor, and the page images remain the only route to the right sub-column. Four names
that stand only in `chicago_democrat_1834_02_18` page 4 column 2 — Constant Abbott, Wm. G. Austin,
Myron K. Brownson, Timothy Burnett — are quoted in that issue's reprint claim and deliberately
left UNMINTED, because minting them would break the per-half rule for four names and then for
forty, which is the defect T-0299 records. Whether the rule should be per-name rather than per-half
is a decision about the corpus, not a reading of an issue, and it is left to the owner.

The ticket is therefore **not closed by T-0311**: its acceptance asks for `scan_verified` and a
count rather than a floor, and neither is delivered here. What has changed is its size and its
route — it is now a narrow image read of one sub-column against a nearly complete left one,
rather than a read of the whole list from scratch.
