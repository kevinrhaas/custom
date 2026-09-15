---
id: T-1141
title: The 1 April 1834 return is unread except for three lines, and the reading of those three found a name the extraction drops entirely
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-15
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The 1 April 1834 return is unread except for three lines, and the reading of those three
found a name the extraction drops entirely.

**Filed by T-1138**, which read three consecutive lines of the S run at three impressions of
the page and could not avoid seeing what stood around them. It read three lines out of about
a hundred and seventy. The rest of the return has never been compared with the page.

## What the three-line read saw on its way past

All of it on the 8 April 1834 impression, which is the clean one, and each confirmed on at
least one other. None of it is acted on anywhere: `letter_list_1834_04_01_contested_lines.json`
carries it under `seen_in_passing` as OBSERVATIONS, deliberately.

- **`Mason B. Smith` is a whole line the extraction has no entity for.** It stands between
  `Robt. Stephens 2` and `Mr. Smith`, and the 16 April transcription's own raw text carries
  it. A person the town does not hold.
- **`Robt. Strong` is carried in prose and in no record.** The 1 April claim's raw text has
  `[uncertain: Robt. Strong Detroit, ?]` and the entity list goes straight from
  `Douglass Sloan` to `Samuel Shaw`.
- **Three minted names are set otherwise on the page**: `Peter Schander` is `Peter Schauder`,
  `[uncertain: Stephen M. Satsby]` is `Stephen M. Salsby`, and `Orin N. Stevens` is
  `Orin R. Stevens`.

Five findings in the twenty-odd lines one pass happened to look at, in a return the corpus
reads through TWO extractions of THREE impressions. Whatever the rate is over the other
hundred and fifty lines, it is not zero.

## Acceptance

1. The return of 1 April 1834 is concorded line by line against its page images, in T-1010's
   shape for the 1 January 1834 return: every printed line set down in printed order, tied to
   the entity that carries it or recorded as carried by none.
2. The printed length is COUNTED off the page rather than inferred from the extraction, as
   T-0424 counted January's at 170.
3. Every line the concordance finds that the extraction drops is either minted or refused by
   a named rule, and the five findings above are among them rather than beside them.
4. Every reading the image overturns is moved in the same PR, and the card it moves is
   withdrawn rather than renamed in place — the rule T-1138 applied to its three.
5. `./tools/check.sh` green, with the concordance gated the way T-1010's is.

**Links:** T-1138 (the three lines, and the roster this starts from) · T-1010 (the shape) ·
T-0424 (the January read this is the April twin of) · T-0321 (the note that first recorded
the disagreement) · `data/research/newspapers/letter_list_1834_04_01_contested_lines.json`
