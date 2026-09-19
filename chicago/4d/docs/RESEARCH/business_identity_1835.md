# The business layer's identity: which printed notices are one house

**T-1388, of T-1182.** Status: the question is now asked of every record, and 7 of the
80 pairs it turned up are ruled. 63 stand named and unruled, which is 63 more than the
repository could name before this pass.

## The gap

`compile_gazetteer.py` has carried a complete identity policy for business records since
T-0304: a pair of trading styles is one house (`firm_merges`), two houses
(`refused_firm_merges`), or one the premises of the other (`premises_relations`), and
each declaration names both spellings verbatim, names the printings it rests on, and is
refused by the gate if it ever outlives its pair. Nothing about that machinery is weak.

What it could not do is FIND the question. The grouping it runs on is `firm_surnames()`,
which reads the partner surnames **of the trading style**. A house only ever met another
house whose style named the same surname.

146 of the present records name no partner in their style at all. The register's own name
for such a record is descriptive — `a new auction and commission room, South Water Street`,
`E. Wentworth's public house on Flag Creek`, `[unsigned] Boot, Shoe & Leather Store, two
doors north of Lake street`. A descriptive name states no partner, so the record never
entered a group, and the proprietor the register *had* read off the notice and written on
the record was never consulted.

`tools/audit_business_identity.py` groups on that other half — the people — and reports
every pair identity.json has not answered in any of its three ways. On the corpus as it
stood before this pass: **80 undeclared pairs across 34 surnames, out of 196 records.**

Keyed on the style instead, the same pass reads `Attorney`, `Store` and `Law` as surnames
and returns 182 pairs, most of them a trade word meeting itself. `firm_styled()` — the
existing reading of "is this string a style or a person" — is what keeps the ledger to
people.

## What the pairs were hiding: the standing advertising block of 5 August 1835

The largest single class in the ledger was one issue. The extraction note on
`chicago_democrat_1835_08_05` says what it is:

> the attorneys' cards, the two forwarding houses, the boot stores, the auction house and
> the paper's own imprint are claimed HERE and, where they stand unchanged in the three
> later issues, are not re-claimed from them

Every card in that block sets the proprietor's name **over the trade**, as a shop sign —
`J. CURTISS, | Attorney and Cou[n]sellor at Law`, `WM. H. TAYLOR ... Boot, Shoe & Leather
Store`. That is a style the register had not met from those men before, so each card
minted a **second house** for a trader the corpus already carried, standing on the same
street, behind the same landmark, weeks after the first.

Seven are ruled here as one house each. In every one of them both records give the same
street where both give a street, and both take their anchor from the same landmark:

| merged into | from the 5 August block | the ground they share |
|---|---|---|
| `J. Curtiss` | `J. Curtiss, Attorney and Counsellor at Law` | South Water Street, at Jones, King & Co. |
| `L. G. Curtiss` | `L. G. Curtiss, Deputy Surveyor of Cook County` | orders left at the Mansion House |
| `Henry Moore` | `Henry Moore, Attorney & Counsellor at Law` | John H. Kinzie's new building |
| `S. Abell, attorney and counsellor` | `S. Abell, Attorney & Counsellor at Law` | Dearborn Street, at the Eagle Coffee House |
| `Wm. H. Kennicott, Surgeon Dentist` | `Wm. H. Kennicott` (1834) | the card states the continuous practice |
| `Wm. H. Taylor` | `Wm. H. Taylor, Boot, Shoe & Leather Store` | Dearborn Street, north of Newberry & Dole |
| `W. Montgomery` | `W. Montgomery, Auction and Commission House` | South Water Street, David Carver's old stand |

Five of the seven needed a `firm_sign_names` declaration first, because the trade on the
card is capitalised and `firm_style()` cuts only a lower-case trade tail: undeclared,
`Attorney` and `Law` read as partners and the partner guard refused the merge on a
partnership that never existed.

**The corpus had already half-seen this.** `refused_firm_merges` carried a second refusal
between `J. Curtiss, Attorney and Counsellor at Law` and `L. G. Curtiss, Deputy Surveyor
of Cook County`, restating the refusal between the two men "because a refusal cannot reach
a style it does not name". Both of those styles are now merged away, so that refusal would
have outlived its pair — the gate says so, and the ruling has been folded back into the
one refusal between `J. Curtiss` and `L. G. Curtiss` with the two August printings added
as witnesses. The judgement is unchanged: the attorney and the county surveyor are two men.

## What the town lost, and it was a flattering count

189 business records now, from 196. Against the State census of Sept–Dec 1835:

| class | census | town, before | town, after |
|---|---|---|---|
| lawyer | 22 | 18 | **15** |
| store | 44 | 59 | **58** |
| *enumerated total* | 118 | 118 | **114** |

The town's attorneys were over-counted by three, and every one of the three was a card in
the 5 August block. The `-4` the crosswalk used to print against the census's 22 lawyers
was not a measurement of the town; it was the block counted twice. `-7` is the honest
figure, and it is a gap for T-1390 to work from the research.

Nobody is removed from the town by any of this. A merge keeps both styles, both anchors,
every printing and every trade word either side set — `L. G. Curtiss` still carries `land
surveying` beside `deputy surveyor of Cook County` in `trade_variants`.

### A gate the merges caught

`trade_census_1835.py` refuses a ruling for a printed trade "the register no longer
carries". It counted only each record's PRIMARY trade, so the two strings these merges
demoted into `trade_variants` — `land surveying`, `surgeon dentistry` — read as rulings
that had outlived their readings, and the gate failed. They had not: the printings are
still in the corpus and the rulings still describe them. The orphan check now counts a
variant as a reading the register carries.

## What is left, and it is not a backlog of merges

**63 pairs across 25 surnames.** Half of these will be two men of one surname, and the
honest answer to those is a refusal — which is a ruling, declared and cited, and is what
the ledger asks for. The finding is that the question stands unasked, not that the answer
is a merge.

The heaviest groups, and what each is actually asking:

- **taylor (14 pairs)** — the Dearborn Street boot and shoe store is read under
  `Wm. H. Taylor`, `[W. H.] Taylor`, `[uncertain: W. H. Taylor]`, `[uncertain: …] Taylor`
  and `[unsigned]`. This is a *reading* question — how much of a bracketed name is a
  name — and it is not the one the 5 August merge settled.
- **wentworth (6)** — four records for one tavern keeper on Flag Creek, one of them
  reading the proprietor as `H. E. Wentworth`.
- **caton (5)** — `John Dean Caton` is printed in Dearborn Street on 22 July and in Lake
  Street on 19 August. The papers contradict each other on the street, so this is a
  removal to be documented as a claim, not a merge, and the gate will refuse it as one.
- **montgomery (5)** — an auction house on South Water Street read as `W. Montgomery`,
  `Montgomery` and unsigned, beside `L. W. Montgomery, boot and shoe maker`, who the
  corpus already holds apart.
- **brown (6), jones (4), king (2)** — namesakes and partnerships; several are likely
  refusals.

Each is one demonstration's worth of reading. None of them can now be met twice by
accident, because `--check` fails on a pair that appears.
