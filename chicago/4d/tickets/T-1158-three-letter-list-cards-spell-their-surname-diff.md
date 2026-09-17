---
id: T-1158
title: Three letter-list cards spell their surname differently from the id minted off the same printing: fraser_wm_h reads Frazer, provis_joshua reads Pruvis, vandino_john reads Vandine
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-16
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Three letter-list cards spell their surname differently from the id minted off the same printing: fraser_wm_h reads Frazer, provis_joshua reads Pruvis, vandino_john reads Vandine.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-1121**, which tried the assertion and then narrowed it. Asserting that a
card's own name gives the family name its id starts with names three cards beyond the
comma fault T-1121 closed:

| card | id says | card says |
|---|---|---|
| `fraser_wm_h` | fraser | `Wm. H. Frazer` |
| `provis_joshua` | provis | `Joshua Pruvis` |
| `vandino_john` | vandino | `John Vandine` |

These are not the same fault: the card and the id disagree on the SPELLING of the
surname, not on which token is the surname, so the reordering rule is not involved and
neither is a comma. Each is one OCR reading minted into an id and a different reading
written onto the card, and the remedy is a ruling on which reading stands — not a code
fix. The register of readings that look misread is
`tools/register_letter_list_suspicions.py`.

**Acceptance:** each of the three is ruled — one spelling stands, the other is recorded
as the reading it is — and the assertion T-1121 could not make becomes a gate: a
letter-list card's name gives the family name the id minted off the same printing.
