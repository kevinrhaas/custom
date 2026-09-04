---
id: T-0701
title: Clark, Filer & Co. is printed five doors east of Randolph in June 1834 and three that December: settle the numeral off the page images
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Clark, Filer & Co. is printed five doors east of Randolph in June 1834 and three that
December: settle the numeral off the page images.

Found by T-0440, which grouped the house's two anchors as one landmark and had to write
the disagreement into the grouping's `cannot_say` rather than settle it. The corpus holds
one standing advertisement under one copy date of 10 June 1834, and its two surviving
printings count a different number of doors off the same corner:

> 1834-06-11 (`chicago_democrat_1834_06_11#c005`, repeated 06-18 and 07-02) — "their ware
> house on \ South water St. five / of the corner", normalised "their ware house on South
> water St. five [doors east] of the corner [of Randolph st.]". The numeral is LEGIBLE; the
> words after it are torn away.

> 1834-12-10 (`chicago_democrat_1834_12_10#c005`) — "“bre doors east / i of Randoi",
> normalised "South wa[ter street, three] doors east [of the corner] of Randol[ph street]".
> Here the NUMERAL is the damaged part and 'three' is the reading pass's reconstruction of
> `bre` inside brackets.

So the two are not equally strong readings, and the honest guess is that the December
figure is a damaged 'five' — but a guess is what the corner-ordinal ruling may not spend.
Until this closes, `identity.json`'s `anchor_spellings` entry for the house bars any
ordinal off this corner from being turned into a position and bars a `lot_claim` on it.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The December numeral is read off the page image, not off the transcription, and the
  reading either confirms 'three', corrects it to 'five', or states that the type is
  destroyed and the count cannot be recovered.
- Whichever it is, `identity.json`'s `cannot_say` for `business_clark_filer_co` is
  rewritten to say what is now known, and the extraction file's `normalized` is corrected
  if the image contradicts it (the quote gate re-derives, so a correction has to go
  through the transcription, never around it).
- If and only if the count is settled, the bar on spending this ordinal is lifted and
  said to be lifted; if it is not settled, the bar stays and the reason is the image.

**Related:** T-0440 (which found it and wrote the bar) · T-0702 (the reader that cannot
see this phrase at all) · `docs/CORNER-ORDINAL.md` · T-0384.
