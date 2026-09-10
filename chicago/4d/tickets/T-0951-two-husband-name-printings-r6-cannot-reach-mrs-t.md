---
id: T-0951
title: Two husband-name printings R6 cannot reach: Mrs. T. G. Hadley and Mrs. Wm. B. Egan are merged onto their husbands because no single source prints both readings
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

Two husband-name printings R6 cannot reach: Mrs. T. G. Hadley and Mrs. Wm. B. Egan are merged onto their husbands because no single source prints both readings.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0723, 2026-09-06.** R6 holds a female honorific apart from the man whose name
it stands on, and it fires only where ONE SOURCE prints both readings as separate entries —
Fergus 1843 setting `Brown, Rufus B.` at 458 and `Brown, Mrs. Rufus B.` at 459. That proof
is what keeps the rule from splitting `Mrs. Eliza Haight` off the census's `Eliza Haight`,
who is one woman: nothing in the letters of a name says Rufus is a man and Eliza is not.

Two printings have the husband-name shape and no such page:

| the honorific reading | the bare reading | why R6 stands down |
|---|---|---|
| `Hadley, Mrs. T. G.` — Fergus 1843, e1164 | `Hadley, T. G.` — Norris 1844, e0769 | two directories, two years |
| `Mrs. Wm. B. Egan` — the 1833-1835 papers | `Egan, Wm. B.` — Norris 1844, e0562 | the press and a directory |

Both are almost certainly a wife under her husband's name — Fergus 1843 also prints
`Hadley, Timothy Gibson` and `Hadley, Elijah W.`, and the Egan household card is Dr William
Bradshaw Egan's. Neither has the page that would prove it, so both stay merged onto the
husband and neither woman has a card or a rung of her own.

**Acceptance:** each of the two is read on its own page — the Fergus and Norris entries in
full, and the newspaper printing of Mrs Wm. B. Egan — and either a source is found that
names the woman apart from her husband (which lands her as her own identity, with the
citation), or the pair is ruled one person with the reasoning written down. Nothing is
split on the shape of the name alone. If the reading turns up a THIRD shape R6 should
reach, the rule is widened with the evidence in hand, not on the strength of these two.

**Links:** T-0723 · `tools/consolidate_resident_evidence.py` rule R6 ·
`data/residents/card_merge_rulings.json` rule D3

---

**HALF OF THIS TICKET IS ANSWERED — by T-0960 / #1051, and not by a page.** The last
paragraph above says that if a reading turns up a THIRD shape R6 should reach, the rule
is widened with the evidence in hand. That shape turned up: a courtesy title standing on
an INITIAL, `Mrs. C. Taylor` against Charles Taylor, where M2 rather than M1 does the
folding. R6's second shape does not ask for the two-entry page proof, because for an
initial that proof can never exist — a directory sets `Taylor, Charles` and never
`Taylor, C.`. It rests instead on the failure of M2's own warrant: the rule reads an
initial as the abbreviation of the one full forename carrying it, and a title says the
initial may be the husband's and abbreviate nothing of hers.

**`Hadley, Mrs. T. G.` is initial-only, so the new shape reaches her.** She now stands as
`id_hadley_mrs_t_g` on `dev`, held apart from `id_hadley_timothy_gibson`. The ladder grades
her G0 — Fergus 1843 alone is never an 1835 resident — so she has no card and no rung, which
is the correct outcome and not a gap. The first row of the table above is spent.

**`Mrs. Wm. B. Egan` is NOT reached, and the reason is exact.** `Wm. B.` is an abbreviated
forename, not an initial: `is_initial` tests for a single character and `wm` is two. So M1's
strip is what folds her onto Dr William Bradshaw Egan, not M2, and only the two-entry page
proof would separate her. The press printing and Norris 1844 are two bodies, so R6 still
stands down. **The second row of the table is the whole of this ticket now** — one reading,
not two, and the acceptance above is unchanged for it.

Filed under the FILING RULE, 2026-09-10: the open ticket that owns the question gets the
finding, and nothing new is filed.
