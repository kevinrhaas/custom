---
id: T-0863
title: H. Van Den Bogart and Dr Henry Van der Bogart are probably one man, and the particle rule keeps them in two identities
state: open
epic: PAPERS
requested_by: steward
seen: false
effort: S
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

H. Van Den Bogart and Dr Henry Van der Bogart are probably one man, and the particle rule keeps them in two identities.

**Acceptance:** a stated ruling on whether `Van Den` and `Van der` are one surname
here, argued from the two printings rather than assumed. If they are, the rule that
says so carries a self-test case, the two identities become one, and
`id_vanderbogart_henry` recovers its G1b. If they are not, the reason is written on
both cards. **Either way the rung that moves is reported, not applied silently.**

## Salvaged from PR #954, which was closed as a duplicate

#954 was a duplicate of #931 in its data — a strict subset, 35 files against 62 —
**except for two tickets**, of which this is one. Neither finding existed anywhere on
`dev`, so closing #954 on the duplicate label would have lost both. Verbatim from
that branch:

> **Found while landing T-0724, 2026-09-06.** N1 reads a spaced surname as one
> surname, which is right — and it makes `den` and `der` two different surname keys.
> The Chicago Democrat of 4 February 1834 prints `H. Van Den Bogart`; Fergus's
> old-settler death notices print `Van der Bogart, Dr. Henry` twice. Before N1 both
> readings fell into the bucket `bogart` and the newspaper record rode along with the
> doctor. Now `id_vandenbogart_h` stands alone and the doctor's identity
> `id_vanderbogart_henry` has lost its one contemporary newspaper: its proposed rung
> drops from **G1b (attested) to G2e (inferred)**.
>
> Nothing was applied — this tool only proposes — but the town has two cards for what
> is very probably one man, and the difference between them is one letter of OCR.

**This is a consequence of T-0724's own rule, not an argument against it.** N1 is
right that a spaced surname is one surname; the cost is that it distinguishes two
spellings of a Dutch particle that a single OCR read apart. That is exactly the sort
of thing a rule should surface rather than absorb — and the honest resolution is a
reading of the two printings, not a loosening of N1.

**Blocked on nothing.** T-0724 landing (#931) is what makes the split visible; this
is the question it raises.
