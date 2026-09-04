# The resident grading ladder — the ratified policy, its rungs, and what each one accepts

**Status: ratified by the owner on 2026-09-03. Applied as a PROPOSAL by
`tools/consolidate_resident_evidence.py`; applied to records by T-0514 (minting) and
T-0515 (regrading), and by nothing else.** Read this before grading anybody.

## The ruling, verbatim

> "attested = 1835 poll + any second independent source, or a contemporary record naming
> the person in Chicago; inferred = 1835 poll alone, or 1833/1834 lists with another
> source, or baptism parent/godparent 1833–35, or Hubbard/Fergus naming a resident with
> trade or address; projected_resident = a single appearance with nothing else; 1839/1840
> alone is never a 1835 resident (later evidence only)."

And the tier definitions from the ask that provoked it:

> "for ones that you are confident, those will be attested, the ones corroborated, those
> who you have a source or some potential sources that you think you are reasonably sure,
> include all those unasserted as inferred. the balance of people who you have seen in at
> least one source, they are documented, but you have some names of and you dont have much
> else, you can put those in a sub category of inferred as a projected resident, under the
> inferred category so we can filter by attested or inferred."

So there are two grades a visitor can filter on — `attested` and `inferred` — and
`projected_resident` is a subtype *under* inferred, never a third grade.

## The rungs

One rung, one id. Every row of `data/research/residents/grading_proposal.json` names the
rung that fired on it, and `--self-test` refuses a row graded above what its rung allows.
The rungs are tried in the order printed here; the first that fires, wins.

| rung | grade | fires on |
|---|---|---|
| **G5** | *no proposal* | The town already carries this person and every appearance this consolidation can see describes a date after the scene year. Their card rests on sources outside these seven domains (Andreas, the newspapers' own register). **The ladder abstains** and the row is listed as a conflict. |
| **G0** | `not_1835_resident` | Every appearance describes a date after 1835 and the town does not carry the person. This is the owner's "1839/1840 alone is never a 1835 resident" — later evidence only. |
| **G1a** | `attested` | The 1835 poll list **and** at least one other independent source. |
| **G1b** | `attested` | A contemporary record naming the person in Chicago — the 1833–1835 newspapers, printing the person by name in the town. |
| **G2a** | `inferred` | The 1835 poll list alone. |
| **G2b** | `inferred` | An 1833 or 1834 list (poll, tax, the 1832 muster) **with another source**. |
| **G2c** | `inferred` | The St Cyr parish register inside 1833–1835 — a party to a marriage or a burial in the scene window. |
| **G3** | `inferred` + `projected_resident` | A single appearance and nothing else. |
| **G2e** | `inferred` | A Chicago post-office letter list of 1833–1835 **and something else**. |
| **G2d** | `inferred` | Fergus 1843 or Norris 1844 naming a person the town already carries, with a trade or an address. |
| **G4** | `inferred` + `projected_resident` | Two or more appearances, none of a class a rung above accepts. |

### Why G3 sits above G2d and G2e, and it is a ruling not an accident

The owner defined `projected_resident` as "a single appearance with nothing else". The
rungs that outrank it are the ones he named a *lone* source for — the 1835 poll (G2a), the
parish register (G2c), the contemporary press (G1b). A lone directory entry or a lone
letter-list name is not one of those, so it falls to G3. The layer already agrees: the 706
`ll_*` people it carries today are `inferred` + `projected_resident`, which is exactly what
G3 re-derives.

### The one reading the ladder needed, put back to the owner

**Is a post-office letter list "a contemporary record naming the person in Chicago"?** It
names a person whose *mail* is at Chicago. Reading it as G1b would grade roughly 1,500
letter-list names `attested` in one pass. This tool takes the cautious half — a
letter-list-only name is `inferred`, never `attested` — and says so here rather than
quietly. **If the owner rules the other way, one line of `grade()` changes and the counts
move; nothing else does.**

## What the tool proposes today

Built 2026-09-03 from seven landed domains; `--report` prints these.

| | |
|---|---|
| identities | **6,558** over 9,644 appearances |
| identities standing in two or more domains | 1,132 |
| identities the town already carries | 840 of 849 person records (7 names this tool cannot split) |
| proposed `attested` | 444 (G1a 42, G1b 402) |
| proposed `inferred` | 1,986, of which 1,717 `projected_resident` |
| proposed `not_1835_resident` | 4,095 — the 1843/1844 directories, the 1840 census and the death notices, none of which stands alone for 1835 |
| ladder abstains (G5) | 33 |
| proposed changes to existing people | 159 — 19 up, 63 down, 77 subtype only |
| conflicts listed rather than resolved | 77 — 44 proposed downgrades, 33 abstentions |

Against the #668 baseline (117 attested / 731 inferred / 706 projected / 848 persons), the
ladder as ratified moves 159 of 849 people. **It is a proposal. No household file was
changed by this pass.**

## The review half — what each source turned out to be worth

| domain | names read | identities | on a card the town already has |
|---|---|---|---|
| directories (Fergus 1843, Norris 1844) | 4,346 | 2,915 | 179 |
| newspapers (gazetteer) | 2,274 | 2,101 | 867 |
| old settlers (Fergus death notices) | 743 | 735 | 25 |
| church (St Cyr register) | 520 | 480 | 4 |
| census 1840 | 459 | 456 | 14 |
| civic (poll/tax lists, 1832 muster) | 460 | 386 | 116 |
| residents (the town layer itself) | 842 | 840 | — |
| newberry index | 0 | 0 | surname-only finding aid: R1 refuses all 4,646 cards by construction |
| census 1830, genealogytrails, books | 0 | 0 | nothing person-level read yet |

**Which domains disagree with which.** The overlap matrix in `source_coverage.json` is the
whole answer; the shape of it is that the newspapers and the town layer are nearly the same
population (782 shared identities) because the town layer was largely minted from them,
while the directories are the biggest pool of names the town has never met (2,915
identities, 100 of them already on a card). The church register is the loneliest: 480
identities, 4 of which the town carries.

**The gap that remains, and it is the finding of the pass.** 817 of the 840 identities the
town already carries have at least one source this consolidation can offer that their card
does not cite — **1,050 unspent source-links**. Philo Carpenter, the owner's worked
example, is the shape of it: ten appearances across five sources, a card citing three
(`andreas_1884_v1`, `chicago_democrat_1833_11_26`,
`chicago_tribune_1882_05_19_fourth_reception`), and 23 rulings reaching him of which **22
state no source at all** — which is T-0598, and why T-0598 stands beside this ticket in the
queue. Until a ruling can say what it rests on, spending it onto a card is a human
rereading the crosswalk.

## The merge and refusal rules

They are the newspapers' rules, already ratified in
`data/research/newspapers/identity.json`, plus two for the cross-domain case. Every merge
and every refusal in `identity_master.json` names the rule that made it.

| rule | says |
|---|---|
| **M1** | Identical normalised name — same surname, same forename tokens. |
| **M2** | An initial-only forename attaches to the ONE full forename of that surname carrying the initial. Two rivals is R3, never a choice. |
| **M3** | A middle initial on one reading and absent on the other, forename and surname agreeing, no rival middle initial. |
| **D1** | A merge already declared by a domain's crosswalk or by `identity.json`. **A landed adjudication outranks everything derived here** — 74 appearances moved on this rule in this pass, including `W. H. Adams` of the 1833 poll, whom R3 had refused while `civic/voter_crosswalk.json` had matched him a month earlier. |
| **R1** | Surname only. Never merges onto a person. 614 derived refusals, plus the whole Newberry finding aid. |
| **R2** | Same surname, different forename initial. Never merges. 956. |
| **R3** | An initial-only forename with two or more rival full forenames of that surname — refused with the rivals named. 150. |
| **R4** | Same surname and initial, two different full forenames. 80. |
| **D2** | A refusal already declared by a crosswalk or `identity.json`. 784. |

R2 and R4 are stated **once per surname**, naming everyone the bucket holds apart, not once
per pair: the cross product of forty Smiths is 780 rows that say what the bucket already
says.

## Running it

    tools/consolidate_resident_evidence.py --build       write the three data files
    tools/consolidate_resident_evidence.py --check       they re-derive; the invariants hold
    tools/consolidate_resident_evidence.py --self-test   the assertions still fire when broken
    tools/consolidate_resident_evidence.py --report      the tables above

`--check` and `--self-test` run in `tools/check.sh`. The pass is **incremental**: it
consolidates what is closed and runs again after every few sources. A pass that finds
nothing newly closed says so and costs a run nothing.

## Spending the proposal onto the people the town already carries (T-0701)

`grading_proposal.json` is a proposal and, until T-0701, nothing in it had been written
onto an existing card. Its `changes_to_existing_people` block held **158 rows** where the
ladder and a committed card disagreed. `tools/mint_civic_residents.py --regrade` applies
them — a second mode of the same tool, kept apart from `--build` because `--build` derives
WHOLE cards it owns and this mode reaches into two fields of cards it does not.

**56 applied, 102 refused.** The town moved: attested **480 → 498**, inferred **924 → 906**,
`projected_resident` **791 → 745**. Every applied person carries the rule, the ladder's
words for it, the move it made and the evidence rows behind it; every refused person
carries the refusal.

### The four refusals, and why each is a refusal rather than a grade

| | n | The rule |
|---|---|---|
| **R1** | 36 | **The ladder abstains.** Rule G5 says NO PROPOSAL: every appearance the consolidation can see is later than the scene year and the card rests on sources outside the seven domains. G5 exists to decline to demote such a person, and reading the abstention as a verdict would do the one thing it forbids. |
| **R2** | 20 | **The post office alone.** The proposal lifts the person out of `projected_resident` while every evidence class behind it is a Chicago letter list. A letter-list name leaves `projected_resident` when something OTHER than a letter list names them. |
| **R3** | 43 | **A blind demotion.** The proposal lowers a grade on a card that cites a source the seven domains do not read — `andreas_1884_v1` on 25 of them. The proposal cannot be the whole account of what the grade rests on. Refused on G5's own argument, one rung lower. |
| **R4** | 3 | **Another pass owns the card.** `mint_civic_residents.py --build` and `mint_placed_residents.py --build` re-derive their people byte for byte; a grade written on top would be reverted silently. The change belongs in the pass that owns the card. |

R3 is the finding of the pass. **43 of the 45 demotions the ladder proposes are blind** —
the consolidation reads seven domains and the cards it would demote rest on an eighth. Only
two demotions survive it, and both are the same correction: a card graded `attested` on a
Chicago paper where the paper's appearance is a list of uncalled-for letters, which the
policy above declines to read as *a contemporary record naming the person in Chicago*.

**No grade is lowered without a refusal recorded on the person.** An applied demotion
writes a `D1` refusal onto the card naming the grade refused and the ladder's reason.

### Where the ruling is kept

The pass writes `regraded_on`, `regrade_ticket`, `rule`, `regraded_from`, `regraded_to`,
`regrade_says`, `ladder_ratified` and `refusals[]` into the person's `resident_research`,
and a `REGRADED ON THE RATIFIED LADDER` prefix onto the note, above the record written
before the ruling. `tools/synthesize_resident_research.py` — the 2026-09-02 synthesis,
which forces every letter-list person to `inferred`/`projected_resident` from a research
outcome recorded a day before the ladder was ratified — now carries those keys through and
leaves a regraded person's grade alone. **The 2026-09-03 ladder outranks it.**

### Running it

    tools/mint_civic_residents.py --regrade            apply
    tools/mint_civic_residents.py --regrade --check    it re-derives byte for byte
    tools/mint_civic_residents.py --regrade --report   every regrade and every refusal
    tools/mint_civic_residents.py --regrade --scale    what it does to the town

`--regrade --check` runs in `tools/check.sh`. The run date is a constant in the tool, not
the clock: the check re-applies the whole pass and diffs it, and a `date.today()` would
turn the gate red at midnight for no change in the data.

**Not in scope, and it is T-0702:** the five 1840 heads `crosswalk_census_1840_heads.py`
matched carry a `proposed_later_census` block and no IPUMS serial, which
`census_1840_identity_bridges.csv` requires. `census_1840_linked` is unchanged at 3.

