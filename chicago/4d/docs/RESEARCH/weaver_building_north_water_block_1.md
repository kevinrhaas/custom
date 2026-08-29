# D. Weaver's building — Lot 2 or Lot 9, block 1, North Water street

*The disagreement, and the reading taken from it. AGENTS.md § Honesty rules: "Where
sources disagree, record the disagreement in `docs/RESEARCH/<id>.md` and pick the
best-attested reading **with reasoning** — never silently choose." T-0328 (PR #510) made
the choice inside the claim notes; this is the dossier that rule asks for, written after
it so it describes what the corpus actually holds.*

**Question.** Two printings of the same advertisement gave two different lot numbers. A
lot and a block are as close to a map reference as this corpus ever gets: it is the
difference between a documented building standing at one place on the north-bank river
frontage and standing at another.

**Answer. Lot 2.** Four printings to one, on four separate settings of the type.

## The witnesses

The notice is a standing advertisement, run in five consecutive numbers of the *Chicago
Democrat* from the last number of Vol. I into the fourth of Vol. II. All five stand on
issue page 3; four in column 3 and the last in column 4.

| issue | page/col | claim | the line, verbatim |
|---|---|---|---|
| 1834-11-26 | 3 / 3 | `c010` | `ling on Lot 2, in block 1, on North` |
| 1834-12-03 | 3 / 3 | `c025` | `SuE building on Lot 2, in block 1, on North` |
| 1834-12-10 | 3 / 3 | `c012` | `on Lot 2, in block 1, on North` |
| **1834-12-17** | 3 / 3 | `c006` | `building on Lot 9, in block 1, on Norh` |
| 1834-12-24 | 3 / 4 | `c012` | `THE building on Lot 2, in block 1, on Nort` |

Only the last two had been claimed before T-0328. The November read (T-0293) and the
December read (T-0294) both passed over the notice in the three earlier issues — in
1834-11-26 and 1834-12-10 it survives inside an alternating pair of physical columns,
woven line by line, which is the shape those reads found hardest. **That is a fact about
the instrument, not only about this advertisement**, and it is recorded in the November
range of `coverage.json` so the same miss can be looked for elsewhere.

## Why this is evidence and not a tidy-up

T-0294 claimed both of the printings it found, each quoting its own digit, and amended
neither to agree with the other. That was right, and the reading does not undo it:
**no transcription has been edited.** Every printing keeps its own verbatim quote,
including the one that reads 9, and the losing reading stays visible in that claim's
`normalized`. What changed is the number of witnesses.

The notice is **reset weekly** — its line breaks, its capitals, its dateline and even its
column all move between numbers — so the four agreeing printings are four compositors'
settings and four passes of the transcriber over different type, not one reading counted
four times. That is the whole warrant: a majority of independent settings, not a
manufactured agreement between two.

## The losing column, on its own record

1834-12-17 page 3 column 3 is the least reliable of the five, and demonstrably so from
inside its own three lines:

- it sets `Norh` for *North*;
- it loses the word `Water` to the alternating column entirely;
- it sets the advertisement's own dateline as `3, Nor. 13, 131`.

**And that last one also refutes the premise the ticket was opened on.** T-0328 argued
that "2 and 9 are not a confusable pair in clean type, which means one of the two
transcriptions is simply wrong rather than both being uncertain readings of a damaged
glyph". The premise is sound and the conclusion followed, but the unstated assumption —
that this type is clean — does not hold: the same advertisement's copy dateline is set
**12, 12, 13 and 19** across the five weeks. A column that sets a day four different ways
is not a column whose digits can be taken at face value, and the reading rests on the
count of independent settings rather than on any one of them being trustworthy.

## What is still open

**The dateline's day does not agree across the printings** — 1834-11-26 and 1834-12-03
read `12`, 1834-12-24 reads `19`, 1834-12-17 reads `13`, and 1834-12-10's is unreadable —
while the two claims that predate T-0328 both carry `ad_copy_date.iso: 1834-11-19`. The
three claims T-0328 added assert no `ad_copy_date` at all rather than pick a side inside a
ticket opened for the lot number. **T-0350** carries it.

## Status of the reading

`transcription_mediated`, not `scan_verified`. T-0328's acceptance asked for the lot
number to be read off a page image; **the page images are not in the repository** — the
deposit at `chicago/reference/newspapers/` holds transcriptions only. The digit is settled
on the corpus's own text, which is a weaker instrument than a scan and a stronger one than
the two-witness deadlock it replaces. A scan read would still outrank it, as
`data/sources/chicago_democrat_1833_11_26.json` outranks the transcription for the first
number.

## What it means for the model

`block 1, North Water street` is inside the modelled town, on the north bank at the east
end of the frontage. Nothing stands for this building yet; placing it is T-0263 / T-0306
territory. When it is placed, **Lot 2**.
