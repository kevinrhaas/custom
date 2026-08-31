---
id: T-0424
title: The 1 January 1834 letter list's printed length, and the names all nine printings lost, need the page images
state: open
epic: PAPERS
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

T-0331 settled which return the 1834-03-04 crop carries — the Chicago post office's
**1 January 1834** return, printed for the ninth time — and repaired twenty-five of its
fifty-seven cut forenames from the eight concordant printings, without a page image.
Two questions it could not answer that way survive, and both need the images.

**1. THE PRINTED LENGTH IS STILL A FLOOR.** Seventy-eight personal names are extracted
from the 1834-03-04 crops and seventy-eight are hand-counted in them, but the crops are
not the printed list: `Anderson`, `Abbott`, `Austin`, `Axtell`, `Bertrand`, `Barrows`,
`Bowen`, `Bradford` and `Britton` all stand in No. 7's printing at line 645 and in none
of the March crops. The concordance cannot measure the shortfall, because the regions it
reads carry the interleaved advertisement as well as the list, so a surname census over
them counts `Athenian` and `Blankets` too. A count off the page images would settle the
printed length of a list this project is treating as a census proxy.

**2. THIRTY-TWO CUT READINGS ARE STILL CUT**, and `tools/letter_list_printings.py`
states the reason for each: twelve where no two printings set the same forename, four
where the surname stands TWICE in the list (Bennett, Miner, Temple — a crop that lost
both forenames cannot say which line is which), fifteen with no witness at all, and one,
Tuller, reported as a disagreement because Alden Tuller and Elam Tuller both stand in
the list, at No. 13 lines 3137-3138.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The printed length of the 1 January 1834 Chicago return is COUNTED off the page
  images, and the extracted 78 is stated against it as a shortfall rather than a floor.
- Each of the thirty-two still-cut readings is completed at the image or reported
  unreadable at the image, by name.
- Claims c026 and c027 of `chicago_democrat_1834_03_04` take `reading: scan_verified`
  for whatever the images settle, and keep `transcription_mediated` for the rest.
- The two Bennetts, two Miners and two Temples are resolved to their own lines, or the
  ambiguity is recorded as permanent.

**Links:** T-0331 (which return it is, and the twenty-five repairs) · T-0312 (the month,
and the two claims) · T-0299 (mint one list once — and these names are January's, so
they mint WITH January's) · `tools/letter_list_printings.py` · `data/research/newspapers/README.md`
§ the letter-list sweep.
