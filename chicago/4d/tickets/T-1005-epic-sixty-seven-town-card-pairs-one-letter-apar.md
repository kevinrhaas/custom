---
id: T-1005
title: EPIC — Sixty-seven town-card pairs one letter apart, ruled a stretch at a time: the class T-1002's C9 opened and could not close
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

T-1002 folded three duplicate town cards that spelled one name two ways — Madore/Medore
Beaubien, Clybourn/Clybourne Archibald, Russel/Russell E. Heacock — and left behind the
question that made them findable: how many more are there? It is measured now rather than
supposed. `python3 tools/consolidate_town_cards.py --fuzzy` runs the same candidate test
with a one-letter key and writes
`data/research/residents/town_card_fuzzy_candidates.json`.

**SIXTY-SEVEN PAIRS**, sixty-one on the surname leg and six on the forename leg, thirteen of
them in the ONE-ANCHOR shape all three of T-1002's own pairs had: one hand-authored card
that documents the person, one thin civic mint carrying a name and `none_recorded`. That is
the shape C9 is written for, and it is where a stretch should start.

**A ROW IS A QUESTION AND NOT A DUPLICATE, and this is the whole reason it is an epic and
not a run.** Two men of a town can be one letter apart in print and two people in fact —
`hale_john` against `vale_john`, `rose_niles` against `ross_niles`, `sheldon_james` against
`wheldon_james`. A one-letter difference is a RESEMBLANCE. C9's third clause is what turns
one into a reading: the printing the thin card was minted from has to carry a SECOND DATUM
the survivor's own record documents — a trade, a civic office, an address, an arrival year.
Every row here needs that printing read. Sixty-seven readings is far more than five
tickets, which is what the queue's filing rule says makes an epic.

Some are plainly the same shape as the three already ruled and will go quickly —
`foot_john`/`foote_john`, `lloyd_alexander`/`loyd_alexander`,
`pearson_hiram`/`pearsons_hiram`, `hoit_thomas`/`hoyt_thomas`,
`vanderbogart_henry`/`vanderbogert_henry`, `scarrett_isaac`/`scarritt_isaac`. Others are
scanner damage that the town has minted a card for and should probably lose it instead of
folding it: `smow_george_w` beside `snow_george_w`, `tmple_john_t` beside the Temples,
`chark_john_a` beside the Clarks, `anight_clark` beside `knight_clark`. And a few are
almost certainly two men and want the refusal written down as carefully as a fold.

**WHAT MUST NOT HAPPEN.** A fold is a card DELETION and the town's resident count moves by
it. Nothing here may be folded to tidy a duplicate away; a pair the evidence does not decide
STANDS, which is what `D1`/`D4` are for. And the fuzzy list is a WORKLIST and not a gate —
`--check` does not read it, deliberately, because sixty-seven unruled questions would put
the merge gate red and it would then be switched off.

**How a stretch should run**, when the owner promotes this out of the epic band: take the
one-anchor rows first, in the ledger's order, as many as one run can read the printings for;
rule each in `data/residents/card_merge_rulings.json` under a named rule with `for` and
`against` written out; land them with `--apply`; and re-derive behind them — the merge
cascade is large and T-1002's own commit is the worked example of it.

**Links:** [[T-1002]] (the three, and C9) · [[T-0993]] (the first fold the derivation did
not raise) · [[T-0839]] (the exact candidate test and the ruling file) · [[T-0844]].
