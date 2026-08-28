---
id: T-0320
title: The April 1834 letter list mints 159 of at least 174 printed names, and only the page images can close the gap
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

The Chicago post office's list of letters for 1 April 1834 is minted at
`extracted/chicago_democrat_1834_04_01.json` c001 and c002 (T-0313): **159 names**, over
John S. C. Hogan's signature. That is a floor, not the printed length.

The list is cited across 194 transcription lines and 15 of them carry list debris rather
than a readable name — `is Bet i`, `Bate es`, `Rowercee ee, i`, `shal astio`,
`eeripeeancottric`, `inn Renny`, `pile. wr Bradley 2`, `é losept Habeax`, `Robt. V.’ Ale:`,
`Mons: Kinbert`, `Win Lou!`, `iregory. 1`, `ee gear :`, `« . Walker`, and the line the
16 April reprint reads `Dr. Trimball`. So the printed list is **at least 174 names** and
this pass mints 159 of them.

The 16 April reprint (c004 of `chicago_democrat_1834_04_16.json`) reads nine of those
fifteen — `Josept Habeas`, `Robt. V. n`, `Robert W. Chapma[n]`, `Mons. Lath`, `Ivin Lou`,
`Gregory E. Legg`, `Dr. Trimball`, `Geo. E. Walker` — and it is deliberately **not** minted,
because one list makes one cohort of people (T-0299). It also **disagrees** with the first
printing about two names: `Benjamin Reed` / `Benjarnin Smith`, and `Ira Raymore` /
`Ira Saymore`. Both sit in an alphabetical S-run, which is an argument from position rather
than a witness, so the first printing's reading stands and the alternative is written down.

This is the same shape of gap T-0310 recorded for the 1 January 1834 list, and it has the
same answer: **only the page images can close it.** Both April printings are
Tesseract-fallback reads of the same damaged columns; a third transcription of the same OCR
will not recover a name neither impression carries.

## Acceptance (one demonstration)

- The two printings' page images are read at name level and the fifteen unreadable lines
  are resolved or declared unresolvable one by one.
- The nine names the reprint carries are minted **into the existing cohort** — same claim,
  same list, `reading: scan_verified` where the scan supplied them — and NOT as a second
  cohort. `identity.json` carries a `merge_rule` for anything the two spellings join.
- The two disagreements are settled from the page rather than from alphabetical position,
  or recorded as permanently open with the reasoning.
- `coverage.json`'s T-0313 note is updated with the true printed length, and the count in
  it stops being a floor.
