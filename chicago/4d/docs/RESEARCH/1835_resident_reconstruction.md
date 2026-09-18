# The 1835 resident reconstruction

**Opened by T-1167, 2026-09-18.** This is the dossier for the reconstructed half of the
resident layer: what the owner asked for, the three standing readings his direction
reverses, and the machinery that makes a reconstructed person auditable and withdrawable.

It writes nobody. The programme file is
[`data/reconstruction/1835_resident_reconstruction_programme.json`](../../data/reconstruction/1835_resident_reconstruction_programme.json)
and the one writer is [`tools/reconstruct_residents_1835.py`](../../tools/reconstruct_residents_1835.py);
bands 3A–3C are each a *stage* of that writer.

---

## What the owner asked for

**2026-09-17, verbatim:**

> create reconstructed residents households businesses structures and any other items …
> including what I think are a fair number of missing women and children and perhaps
> former slaves or other less documented individuals, certainly mark these family members
> and people as reconstructed.

and:

> we should make the expected number of residents and data of the town complete with these
> reconstructed residents.

**2026-09-18, on what the band may and may not spend:**

> i dont want new research tickets spun up off of that they should use the existing
> research … i do not want a ton of tickets sprung up from them starting a whole new stream
> of research on everything

So: the bands below **read** the layer bands 1 and 2 signed off, and the model folded into
`1835_town_model.json`, and **write** reconstructed people from them. A gap is an expected
output here — it goes to the order book as a quantity and to the record's own `basis` and
`replaceable_by` as a statement of what would retire it. It does not become a new reading.

---

## The three supersessions

The reversal is written down here because a reversal nobody writes down is one the next run
re-applies. Each of these is superseded **for the `reconstructed` tier only**; nothing about
the attested and inferred grades moves.

**1. `residents-households-summary-2026-09.md` § "What this layer must not be asked to do is
estimate".** A recommendation, and a good one for the layer it was written about. The owner
has now asked for exactly the estimate it declined, at a tier that labels itself. Attested
and inferred stay precisely what the evidence ladder says they are; the estimate lives in a
third grade that says on its face that it is one.

**2. T-1146 acceptance ¶4 — "aggregate age/sex buckets … mint no spouse, child, boarder or
servant".** That clause binds the *attested and inferred* spend, and it still does: a
research pass may not turn a bucket into a named person. It does not bind a programme that
grades every such person `reconstructed`, gives each a basis and a seed, and publishes the
rule that would retire them. A one-line note stating this is on T-1146 itself, so a reader
who reaches the clause first is not left to reconcile the two.

**3. `data/research/census_1840/composition_1840.json` § `what_this_may_not_do[]` — "never
names anybody".** **Unchanged and still true.** The 1840 composition is a *distribution* the
models draw from. It supplies no name and no row, here or anywhere; the names come from
`1835_invented_name_pools.json` and the rows come from the stages.

---

## What makes a reconstruction accountable

The 2026-09-02 retirement is the thing this design is built against. The owner removed the
previous reconstructed population wholesale, and the reason he could not do anything *less*
than wholesale is that no record said what had been invented, from what, or what would
replace it. Four fields fix that, and `tools/validate.py` refuses a reconstructed person
that lacks any of them:

| field | says |
| --- | --- |
| `name_basis` | the name is invented, and which pool it came from (graded `reconstructed`, always) |
| `basis` | the model row or the rule the *person* was drawn from, and why they follow from it |
| `seed` | the retypable string that redraws them — `<household_id>:<bucket>` |
| `replaceable_by` | what evidence would retire them, as a search somebody could actually run |
| `reconstruction.stage` | which stage of the programme wrote them |

A person no stage claims is a person the programme cannot re-derive, so the validator names
that case on its own. The per-*attribute* half of the contract is T-1158's `check_tier_block`
and is unchanged; this is the per-*record* half, and it is imported from the writer rather
than restated, so the tool that mints a person and the gate that reads one back cannot drift.

---

## The boundary, in one line

Every research writer of `data/residents/` calls
`tools/refuse_reconstructed_grade.refuse()` and may emit only `attested` or `inferred`.
`tools/reconstruct_residents_1835.py` does not call it, and its own `--self-test` reads its
syntax tree to prove it still does not. That asymmetry is the whole boundary: the research
passes cannot mint an invention by falling through a default, and the one tool that may mint
one is held to the record contract instead.

---

## What is not decided here

- **The quota.** How many of each kind of person the town wants is the order book's (T-1166),
  and no stage may `--build` until it lands. A reconstruction with no quota has nothing to
  stop at, and `--build` says so rather than choosing a number.
- **The retired programme.** `1835_inferred_household_programme.json` stays retired;
  `resident_population_active` stays `false`, and its 31 `inferred_anonymous` roofs stay
  anonymous stock for T-1197. This programme writes its own people rather than restoring
  anybody's.
- **Depiction.** `docs/LIBERTIES.md` L1 stands: no human figure is drawn, anywhere. These are
  records. Native, Métis, free Black, Irish and German residents *are* reconstructed — the
  owner re-ruled that on 2026-09-17 — through stage `underdocumented` alone, every record
  carrying `review_required` and `touches_removal`, under AGENTS.md's Indigenous-history
  review.

---

## Stage `attribute_fill_arrival` — arrival year, origin and reason (T-1169, 2026-09-18)

The first stage of the programme to write anything, and it writes **no person**: it fills three
attribute blocks on the 1,258 households that already exist. The recipe is
`1835_resident_reconstruction_programme.json` § `arrival_fill`; the build is
`--stage attribute_fill_arrival --build` and the re-derivation is the `--check` `tools/check.sh`
already runs.

**Where the layer stood.** `arrival` was filled on every household — but 1,196 of those are a
`not_later_than` BOUND, which is a statement that somebody was here BY a date and none at all
about when they came. `origin` was asserted on 23 cards and `reason_for_coming` on 25. The other
1,235 and 1,233 read *Not attested*.

**Three legs, strongest first.**

| leg | tier | what it is | count |
| --- | --- | --- | --- |
| the Old Settlers roll, spent onto the cards it names | `inferred` | the registry's own arrival year and birthplace, for the 35 rows the crosswalk MERGED into this layer | 16 arrival years, 21 origins |
| a draw from a model row | `reconstructed`, `basis.kind: model` + seed | the known layer's arrival-year distribution truncated at each household's own bound; the roll's birthplace distribution | 1,182 arrival years, 1,204 origins |
| an argument from a rule | `reconstructed`, `basis.kind: rule`, no seed | origin from a surname only one community pool carries; reason from the head's recorded trade, or from the arrival season | 10 origins, 1,233 reasons |

**Never `attested`.** The roll is a recollection registered at the Calumet Club in 1879, forty to
sixty years after the fact, and its own `arrival_year_basis` says it dates the claim and does not
prove it. A birthplace is not an origin either — this field asks where a household came FROM — and
each of the 21 blocks says so on the card.

**Four refusals are recorded rather than smoothed.** Adams, Campbell and Couch registered arrivals
LATER than the scene date; Stephen F. Gale registered 1835 against a layer that reads 1833. The
contemporary record wins in each case, the roll's rows are kept as they were read, and the block
that overrides them names the year it refused. Where the roll AGREES with a read arrival — seven
households — no block is written at all: a weaker duplicate of an attested value is noise, and
seven of them would have buried the one disagreement worth seeing.

**Why there is no cohort × trade table.** T-1169 asked for a reason drawn from one. The town model
refuses to build one, in as many words: *the land sales, the canal commission and the harbour works
are each a documented draw, but no committed source apportions the town between them and this model
will not invent the split.* Building it here would be inventing that split in the place the model
declined to, and the seed would have made the result reproducible without making it true. So every
reason is ARGUED from something the household itself carries — its trade, or its season — names the
draws that were operating, and ends with the sentence that it does not know which of them applied.
`docs/LIBERTIES.md` **L242** is the admission; the programme file's
`arrival_fill.the_argued_leg.WHY_IS_NOT_APPORTIONED` is the argument.

**`written_by_stage` is what makes it re-derivable.** Every block the stage writes carries that
marker, and it is the whole of how `--check` works: a marked block is recomputed from the programme
and compared, an unmarked one is some earlier reading's and is never touched, and a marked block the
recipe no longer produces is WITHDRAWN rather than left behind. Without it `--build` would be a
one-way write and the committed layer could drift from the rules that claim to explain it — which
is the failure the 2026-09-02 retirement was about, one attribute down instead of one person.
