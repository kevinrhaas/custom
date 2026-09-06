# data/residents/ — the id, filename and manifest contract

`households/*.json` is one file per household; `index.json` is the manifest
(`households[]` rows of `{id, file, head, division, persons, grades, ...}`,
plus the `vocabulary` block that declares every closed enum a renderer must
implement). This note exists because a household's **filename has looked, at
different times, like it was encoding something it wasn't** — see "On the
`hh_doc_`/`hh_placed_`/`hh_ll_` prefixes" below, which is the direct answer to
that question.

## The rule

A household's id is always `hh_<surname>_<given...>`, lowercase-slugged, surname
first (`hh_morris_b_s`, not `hh_b_s_morris`) — built by `plain_fragment()` in
`tools/mint_documented_residents.py` from the head person's name (`surname()`
finds the surname; `plain_fragment` drops it from the token list and puts it
back in front). `id == the filename stem == the manifest's `id` field for that
row` is enforced by `tools/validate.py check_residents()` — never hand-diverge
one from another.

**Nothing about a person's evidence grade, residency status, or which pass
minted them belongs in this name.** Those are fields:

- `grade` (`attested` / `inferred` / `reconstructed`, on each person) is the
  accuracy ladder. A household is free to be promoted — a `letter_list_only`
  person corroborated by a second source becomes `attested` — **without a
  rename**. 21 households did exactly this under T-0489 while keeping
  whatever id they already had.
- `letter_list_only` (bool, per person) and `resident_subtype:
  "projected_resident"` mark how a person entered the dataset.
- `source_pass` (household-level, optional — see below) records which of the
  three mint tools produced the record, for the tools' own bookkeeping. It is
  provenance about the *tooling*, not a finding about the *person*, so it is
  not part of the public `vocabulary` block in `index.json`.

## On the `hh_doc_` / `hh_placed_` / `hh_ll_` prefixes

Three tools independently derive households from the 1835 register
(`data/research/newspapers/register_1835.json`) and the gazetteer, in a fixed
precedence order (best-evidenced first): `mint_documented_residents.py`
(a person with a printed trade), `mint_placed_residents.py` (no trade, but the
corpus places them inside the town and nowhere else), `mint_letter_list_residents.py`
(known only from the post office's letter lists). Until T-0599 each pass
stamped its own prefix onto the id it minted — `hh_doc_`, `hh_placed_`,
`hh_ll_` — so a tool could recognize "a household I minted" by filename alone,
for its own stale-file cleanup and precedence-skip logic.

**`hh_placed_` was never a location.** Every household from that pass carries
`"division": "unplaced"` — "placed" names the pass's own residency EVIDENCE
test (PART ONE of its docstring: does the corpus put this person inside the
town, as opposed to outside it), not a lot or plat position. See the note in
`tools/mint_placed_residents.py` right above `PART ONE — PLACEMENT`.

**As of T-0599, no new household is minted with a legacy prefix.** A
household minted by any of the three tools from here on gets the same plain
`hh_<surname>_<given>` id the ~73 hand-authored households already use, and
records which pass minted it in `source_pass` (`"documented"` / `"placed"` /
`"letter_list"`) instead. The tools still recognize their own prior output —
`minted_by()` checks the legacy prefix OR the `source_pass` field — so a
second run stays idempotent across the migration boundary and a household
never needs two ids for the same identity.

The **747 households already minted under a legacy prefix before T-0599** were
not renamed by that change alone — filenames are load-bearing (cross-referenced
by hardcoded ids in several frozen, gated selector scripts and by the
resident-research findings ledgers) and a rename touching all of them is its
own, separately tracked migration. Until that migration lands, a legacy-prefixed
filename on disk is not a signal of anything about the person it names — check
`source_pass` (once migrated) or just the household's own `grade`/`letter_list_only`
fields, never the filename, for what a household actually is.

`hh_inf_*` (5 files) is `tools/generate_inferred_households.py`'s own, unrelated
pipeline and is not part of any of the above.

## `kin` — a relationship that crosses two records (T-0597)

`persons[].relationship` is a person's place **inside** one household and stops
at that household's edge. A family tie between two households had nowhere to go
but a free-text note, which is to say nowhere a query can reach it — and the
households this dataset most needs to keep apart are exactly the ones a shared
surname makes mergeable. Four household cards here are Kinzies — six until
T-0839 folded two duplicate initials cards on 2026-09-05, and T-0732 ruled on
what the family's remaining prose claims are worth
(`data/research/residents/kinzie_kinship_ruling.json`).

`kin` is an optional household-level list. Each row is an ordinary graded claim
block — `value` names the **other person**, so `walk_attested()` checks its
`confidence`, `sources` and `note` exactly as it checks an `arrival` — plus
three fields that make it a link:

| field | means |
|---|---|
| `person` | whose relative this is; must be a person in **this** household |
| `relation` | the term, from `index.json`'s `vocabulary.kin_relations` |
| `household` | the other household's id; must resolve, and must not be this one |
| `value` | the other person's id; must be a person in that household |

Two rules, and both exist because **half** is the point. Hurlbut says James
Kinzie was the *half* brother of John H. Kinzie — same father, different
mothers — and that is the first thing a summary flattens:

- **A relation is legal only against its declared inverses.** For a sibling tie
  the mirror must be a sibling tie *of the same degree*; a `half_brother` whose
  mirror row says `brother` fails. The vocabulary is therefore exactly the set
  whose inverse `tools/validate.py` knows (`RESIDENT_KIN_INVERSES`).
- **Every row is reciprocal.** Write it on both records or on neither: the
  record that omits it still reads as no relationship at all, which is the
  defect the ticket was opened about.

A relation is refused outright unless its inverse is declared, and the rule is
satisfied rather than relaxed when the set grows: **T-0734 added the asymmetric
pairs together** — `husband`/`wife`, and the parent terms against the child
terms — so `father` is legal only against `son` or `daughter`, and a `father`
whose mirror row also says `father` is the one-way claim the rule exists to
catch. `uncle`/`nephew` and `cousin` are still undeclared, because nothing in
the corpus has needed them.

## The kinship the corpus states, surveyed and ruled on (T-0734)

The audit that opened T-0734 found **14 of 1,404** people related to anybody at
all, and the cause was never that the sources are silent: the St Cyr register
marries six couples this town holds both halves of, and nothing had read it.

Two files, and they are two on purpose:

| file | |
|---|---|
| `kin_survey.json` | **DERIVED** by `tools/survey_stated_kin.py`. Every stated kinship in the committed corpus, with both ends resolved against this layer. Re-derived by `--check`; hand-edits lose. |
| `kin_rulings.json` | **AUTHORED**. One verdict per landable proposal — `landed`, `refused` or `deferred` — each with its reason. No pass may rewrite it. |

`tools/check.sh` runs `survey_stated_kin.py --check`, which fails while a
proposal whose two people this dataset holds is unanswered, while a `landed`
ruling has no reciprocal `kin` rows on the two records, or while a `refused` one
has them anyway. A newly stated kinship is therefore a red build rather than
something to notice one day.

How a name becomes a person differs by source, and the line is drawn at
identity, never at the tie:

- **A register entry** resolves through the `..._evidence[].record_id`
  back-links the cards already carry. Most of these people exist *because of*
  the entry that names them, so nothing is matched by name at all. Where a
  back-link is missing but a townsperson shares the name, the row is
  `identity_not_asserted` and is **not** proposed — the town's John Murphy is
  attested from three sources that are not the register and no one has ever
  established that he is the register's groom.
- **Prose already quoted onto a card** takes that card's head as the subject and
  resolves the other party by the st_cyr crosswalk's own rule: surname folds
  equal, forenames agree initial for initial, and **exactly one** townsperson
  may match. Two is `ambiguous` and is reported rather than guessed. A bare
  forename inside a card (`brother of Samuel`) is read with the subject's
  surname and then has to resolve like any other name.

The 1840 census households are the densest kinship the corpus holds and are
deliberately **not** read: the crosswalk is stale against both the pages
(T-0714) and the town (T-0698), and kin read off it would land on the wrong
people.
