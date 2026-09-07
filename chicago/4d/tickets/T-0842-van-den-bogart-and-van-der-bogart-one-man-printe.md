---
id: T-0842
title: Van Den Bogart and Van der Bogart: one man printed two ways, or two men? A card was minted for the second
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

Van Den Bogart and Van der Bogart: one man printed two ways, or two men? A card was minted for the second.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Surfaced by T-0724, 2026-09-05.** Until the splitter learned that a compound surname is
one surname, `Bogart, Dr. Henry Van der` and `H. Van Den Bogart` both truncated to the
surname `bogart` and were carried as one identity. That merge was never ruled on; it was an
accident of taking the last token. With the particle joined to the name they are
`vanderbogart` and `vandenbogart` — two surnames — and the consolidation does what it is
supposed to do with two surnames: it keeps them apart. `mint_civic_residents.py --build`
then minted `hh_vandenbogart_h`, and the town's person count went from 1,404 to 1,405.

**The card is honest and it is probably a duplicate.** It says only what the Democrat of
4 February 1834 prints. But `Van Den` is one letter from `Van der`, the initial matches, the
same paper's OCR of the same notice reads `r. H. Vax Den Bocart`, and Dr Henry Van der
Bogart is a man this town already carries with a death notice and a letter list behind him.

**Why it was left standing rather than merged here.** A merge across two printed surnames is
a research ruling and needs a source, not a resemblance — T-0724's own acceptance was that
no identity may span two surnames. The machinery for a ruled merge already exists (rule D1,
a merge declared in a domain crosswalk or `data/research/newspapers/identity.json`), and the
right answer is to use it or to decide the two are genuinely distinct.

**Acceptance:** the 4 February 1834 notice is read at the page, the ruling is recorded as a
declared merge or a declared refusal with its reason, `--build` is re-run, and either
`hh_vandenbogart_h` is withdrawn onto `hh_vanderbogart_henry` or it stays with a note saying
what was read and why the two stand apart.
