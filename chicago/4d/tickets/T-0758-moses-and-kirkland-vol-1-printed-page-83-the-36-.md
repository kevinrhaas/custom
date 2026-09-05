---
id: T-0758
title: Moses and Kirkland vol. 1, printed page 83: the 36 purchasers at the first Chicago lot sale of 27 September 1830, read off the page images because the OCR has collapsed the table
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

Moses and Kirkland vol. 1, printed page 83: the 36 purchasers at the first Chicago lot sale of 27 September 1830, read off the page images because the OCR has collapsed the table.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0581**, which read the chapter around it and could not read the table.

Moses and Kirkland, *History of Chicago, Illinois* vol. 1 (1895), printed page 83 — scan
leaf 109 of the project's deposit, item `historyofchicago01mose_202609`. The narrative
that introduces the table IS read and is claimed at `bk_mk1_010`: 132 lots sold on 27
September 1830 at an average of $34 cash, thirty-six purchasers, only ten lots south of
Randolph, and six purchasers named with their lots and prices. **The table itself — "A
list of the purchasers of town lots at the first sale thereof in Chicago, with the prices
paid therefor" — is printed in ruled columns (LOTS, BLOCK, PRICE, NAME OF PURCHASER) and
the hOCR search text has interleaved them.** Lines 1306-1352 of
`data/research/books/text/moses_kirkland_history_of_chicago_v1_1895.txt` carry about forty
legible surnames and not one intact row: prices and lot numbers sit on lines that hold no
name at all.

**Why it is worth a run.** This is the largest untouched source of POSITION in the
project's own terms — thirty-six named men against numbered lots and blocks of the
Thompson plat, five years before the scene date. The queue's own measurement says a list
the town made of its own inhabitants is what predicts yield.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- The table read off the PAGE IMAGE, not off the search text, and graded `scan_verified`.
- Every row that reads — lot, block, price, purchaser — written into the `land_sales`
  domain in its shape, with the rows that do NOT read declared as unread rather than guessed.
- What the sale does and does not say about 1835 ownership, stated: a lot bought in 1830
  changed hands repeatedly in the 1834-36 speculation the same chapter describes.
