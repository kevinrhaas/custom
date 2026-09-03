# The 1840 federal census — later evidence, held as later evidence

**What lives here.** The 1840 deposit: seventy-five page images, the head-of-household
index by ward, and the IPUMS household extract this project already holds. Two
hundred and ten heads have been read off seven printed pages; the other sixty-eight
images are unread (T-0494, T-0495, T-0496, T-0497, T-0504, T-0507).

**Shape: `records`.** One enumerated line is one record: `as_read` for the
enumerator's hand, `normalized` for this project's spelling, and the serial, page
and row in the `locator` so a reading can be found again. Household composition
counts sit beside the row, not inside a resident record.

**THE RULE THAT MATTERS.** *1840 is later evidence, not the 1835 household.*
Children, spouses, ages and industry totals are never projected backward without a
separate, written bridge, and no 1835 resident is minted solely from an 1840
appearance. `data/research/residents/` already carries the bridge ledger and its
pending list; this domain feeds it and does not bypass it.

**Hand-authored:** `records/`, `coverage.json`, `crosswalk.json`.
**Generated:** nothing here yet; `data/research/domains.json` is, and is gated.

**Coverage.** Declare the IMAGES read, by image id. Seventy-five is the deposit's
size and it is the denominator every count in this domain is stated against — a
count with no denominator is the thing this file exists to prevent.

**Identity.** Bridging an 1840 head to an 1835 resident is a MERGE, and it is made
in `crosswalk.json` with its rule and its evidence, both names verbatim. A surname
match is a refusal. Three of the 210 named heads are bridged today; the rest are
work, not silence.

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`.
