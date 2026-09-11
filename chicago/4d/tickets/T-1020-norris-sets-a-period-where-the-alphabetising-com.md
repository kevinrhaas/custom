---
id: T-1020
title: Norris sets a period where the alphabetising comma belongs after 56 surnames, so the splitter reads the whole clause to the next comma as the surname
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Norris sets a period where the alphabetising comma belongs after 56 surnames, so the splitter reads the whole clause to the next comma as the surname.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

MEASURED ON THIS BRANCH BY T-1013'S RUN, so this ticket is the fix and not the survey.

`split_entry` takes the surname as everything before the FIRST comma. Norris's compositor
— or the scanner — sets a period there instead in 56 entries:

    Norton. C. C. of N. & Case, house State st. b Madison and Mon
    Wicker. J. H. at C. G. Wicker & Go's, h Dearborn, b Washington and Madison sts
    AVorcester. D. L. at H. Norton & Co.'s, h Wabash st

so the first comma is the one that ends the PARTNERSHIP, and the surname reads
`Norton. C. C. of N. & Case`. Six of the 56 are worse than that: the whole clause carries
`& Co.`, so T-1013's second reading of the firm test still calls them businesses, and every
one of the six is a man — a partner or a clerk giving his residence. They are the reason
T-1013 kept the before-the-first-comma test beside the name-prefix one.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The name of each of the 56 comes off the NAME PREFIX (`read_norris_1844.name_prefix`,
  T-1013) rather than the first comma, so `Norton. C. C.` is surname `Norton`, given `C. C.`
- The six above read as people, and no entry that is a firm today stops being one.
- `PLACE` must not then take `at H. Norton & Co.'s` as an address because `H. ` looks like
  `h `: the place marker is only a place marker at a clause boundary. That is the part of
  this that is not a one-line change, and it is why T-1013 did not do it.
- `read_norris_1844.py --check` re-derives, the person crosswalk's before/after is counted
  and stated, and `bash tools/check.sh` is green. No bake.
