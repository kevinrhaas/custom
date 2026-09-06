---
id: T-0856
title: H. Van Den Bogart and Dr Henry Van der Bogart are one man printed two ways, and the particle rule now keeps them in two identities
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

H. Van Den Bogart and Dr Henry Van der Bogart are one man printed two ways, and the particle rule now keeps them in two identities.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found while landing T-0724, 2026-09-06.** N1 reads a spaced surname as one surname, which
is right — and it makes `den` and `der` two different surname keys. The Chicago Democrat of
4 February 1834 prints `H. Van Den Bogart`; Fergus's old-settler death notices print
`Van der Bogart, Dr. Henry` twice. Before N1 both readings fell into the bucket `bogart` and
the newspaper record rode along with the doctor. Now `id_vandenbogart_h` stands alone and the
doctor's identity `id_vanderbogart_henry` has lost its one contemporary newspaper: its
proposed rung drops from G1b (attested) to G2e (inferred).

Nothing was applied — this tool only proposes — but the town has two cards for what is very
probably one man, and the difference between them is one letter of OCR.

**Acceptance:** a stated ruling on whether `Van Den` and `Van der` are one surname here,
argued from the two printings rather than assumed; if they are, the rule that says so has a
self-test case and the two identities become one, and `id_vanderbogart_henry` recovers its
G1b; if they are not, the reason is written on both cards. Either way the rung that moves is
reported, not applied silently.
