---
id: T-1155
title: The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity
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

The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity.

**Found while closing T-1115, 2026-09-16.** `split_name_or_reason()` removes a
square-bracket group and everything inside it before tokenising. That is correct for a
parenthetical directory annotation and wrong for an internal supplied reading:
`E. K[in]zie` becomes `E. K zie`, `Esth[e]r M. Bailey` becomes `Esth r M. Bailey`, and
`T[e]mple, John T.` becomes surname `tmple`. T-1115 now prevents any such appearance
from minting a new card, but the bad split remains in the identity master, its gazetteer
ties and every later adjudication that consumes those identities.

**Cost measured on T-1115's tree audit:** square brackets occur throughout the research
corpus, including valid internal supplies, uncertain letters and whole later-directory
annotations. Correcting the splitter re-derives the large resident identity artefacts and
can rekey many identities; it must not be smuggled into the bounded mint-guard repair.

**Acceptance:** distinguish square-bracket transcription supplies from parentheses used
for directory annotations; preserve supplied letters inside a name while retaining the
original `as_read`; prove `E. K[in]zie`, `Esth[e]r M. Bailey` and `T[e]mple, John T.` split
to `kinzie`, `bailey` and `temple`; re-derive the identity master, proposal and coverage;
enumerate every changed identity id and either migrate or explicitly refuse every
downstream tie/card affected; and add mutation fixtures that fail if bracket contents are
discarded again. This is parked research under filing rule (d), not a prerequisite for
T-1115's mint refusal.
