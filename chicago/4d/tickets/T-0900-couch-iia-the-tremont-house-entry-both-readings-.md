---
id: T-0900
title: Couch, Iia — the Tremont House entry both readings of Norris 1844 fail on: read the printed token off the page image
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Couch, Iia — the Tremont House entry both readings of Norris 1844 fail on: read the printed token off the page image.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0695**, the pass that repaired the other eleven garbled forenames in Norris
1844 against Kim Torp's independent transcription. This one it could not touch.

    Couch, Iia, proprietor of the Tremont House, corner of Lake and Dearborn sts
      — n1844_e0415, archive.org's OCR
    Couch, (can't read), proprietor of the Tremont House, corner of Lake and Dearborn sts
      — 1844directory.txt:449, Kim Torp, typed from a different copy

Both hands fail on the same token, from two different copies, which is itself a finding:
the type is damaged or inked badly in the printing, not just in this scan. `Iia` is not
GARBLED in `name_agreement`'s sense — every character is a letter a compositor sets — so
the crosswalk refuses `Ira Couch` against it as two full forenames that differ, with no
note that the reading is in doubt.

Ira Couch of 1835 kept the Tremont House with his brother James, and `Couch, James, res
Tremont House` stands on the next line of the same page. That is exactly why the token
must be READ and not deduced: the match this project wants is sitting right beside it, and
reading `Ira` into the page because the match would be nice is the failure provenance
exists to prevent.

**Acceptance:** the printed token at printed page 30 of `generaldirectory19norr` is read off
the PAGE IMAGE, and whatever it says is what `normalized.given` carries — a repair row in
`read_norris_1844.py` cited to the image if it is legible, or a recorded refusal to guess if
it is not; `quote` keeps the damage either way; the Norris crosswalk is re-derived and what
moved is itemised; `bash tools/check.sh` green.
