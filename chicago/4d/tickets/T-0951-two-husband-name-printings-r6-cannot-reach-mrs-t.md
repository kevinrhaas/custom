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

**A THIRD SHAPE, FOUND BY T-0960, 2026-09-10 — and it is not the same fault.** The two rows
above are printings R6 LOOKS AT and stands down from for want of a page. `Taylor, Mrs. C.`
(the Chicago Democrat of 19 August 1835, c007) is one R6 never looks at at all: the printed
forename is an INITIAL, so the honorific strip leaves `Taylor, C.`, which is not the bare
reading `Taylor, Charles` letter for letter, and R6's exact-match test — the test that is
correct for `Mrs. Rufus B. Brown` — simply does not fire. M2 takes her instead, because an
initial-only forename attaches to the one full forename of that surname carrying it, and
Charles is the only C-Taylor in the corpus. So a woman printed under a female honorific was
folded onto a man by the ordinary initial rule, with no refusal recorded anywhere.

T-0960 gave her her own card by hand (`hh_taylor_c`, G1b off the Democrat) and left the
consolidation untouched, so `identity_master.json` still spends `person_taylor_mrs_c` on
`id_taylor_charles`. That is the third shape this ticket's last paragraph asks about, held
here with the evidence in hand rather than widened on the strength of one row: any widening
has to say what stops `Mrs. C. Taylor` splitting off a `Charles Taylor` the corpus prints
without an honorific WHEN THEY REALLY ARE ONE HOUSEHOLD'S TWO READINGS — the same question
the Haight case asks of the exact-match rule, one initial further down.
