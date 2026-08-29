---
id: T-0340
title: The bookseller's sign-name and its partners' firm-name are three gazetteer entries for one house
state: claimed
epic: PAPERS
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: run 8/29/2026, 9:42:37 AM CT
blocked_on: null
needs_bake: false
---

Three gazetteer entries are one Chicago bookshop, and **T-0304 has just landed the machinery
that could join them** — `identity.json`'s `firm_merges`, with a `merge_rule` that must name
both spellings verbatim. Nobody has applied it here.

| entry | from | what survives |
|---|---|---|
| `business_chicago_wholesale_and_retail_book_stationary_store` | `1834-08-27#c002` | the heading, signature lost |
| `business_russell_clift` | `1834-09-03#c012`, `1834-11-12#c011`, `1834-12-03#c004` | both, or the signature |
| `business_russell_clift_chicago_book_and_stationary_store` | four *Chicago American* claims, 1835 | both, run together |

The first two come from ONE advertisement: the partnership notice of Aaron Russell of Boston
and Benj. [H.] Clift of Philadelphia, copy-dated 26 August 1834, opening a store adjoining
P. Carpenter's drug establishment on South Water Street. Which entry a printing lands in
depends only on which half of the type the segmenter kept. Neither name is a misreading — one
is the shop's sign-name, one is the partners' firm-name — so neither claim can be "corrected"
into the other, and T-0327 deliberately left them standing rather than hand-merge.

**The open question is T-0304's own partner-surname guard**, which refuses a merge unless the
two styles carry the same set of partner surnames. The sign-name entry carries NO proprietors
at all, because the printing that gives it lost the signature. Whether an empty set may merge
into `{Russell, Clift}`, or whether the guard should read "no CONFLICTING surname" instead of
"the same set", is the decision this ticket has to make — and it is a decision about the rule,
not about this shop, so it will govern every headline-only firm in the corpus.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The three entries compile to one, joined by a declared `firm_merges` rule that names the
  spellings verbatim — or the ticket records why they may not be joined, with the same care.
- If the partner-surname guard is changed, the change is argued in `identity.json`'s
  `firm_note` and its negative case is in the compiler's self-test.
- No claim's `business.name` is edited to force the join.

Links: T-0304 (the rule), T-0327 (which found the pair), T-0339.
