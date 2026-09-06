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
surname makes mergeable. Six households here are Kinzies.

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

An asymmetric relation may be declared only **together with its own inverse** —
the term on its own would let a one-way claim through, which is why the original
set declared none of them. T-0734 added the parent/child pair as a pair:
`father` and `mother` accept `son`/`daughter` and nothing else, `son` and
`daughter` accept `father`/`mother` and nothing else, so the reciprocity rule has
a mirror to demand at both ends and a father whose mirror row says `brother`
fails exactly as a flattened half brother does. Relations whose inverse is still
open — uncle/nephew, in-laws, step-kin — stay undeclared under the same rule: add
the pair together or not at all.

### What is actually written, and what was refused (T-0734)

`kin` says whether a tie is RECORDED; it cannot say whether a tie the corpus
states was ever written down, and a household that simply omits one is silently
valid. That is how 1,362 people came to carry 24 relationships between them.
`data/research/residents/stated_kinship.json` is the ledger of every kinship the
committed corpus states between two people — five landed as ten reciprocal rows,
eleven refused, each refusal with its reason — and `tools/read_stated_kinship.py
--check` (in `tools/check.sh`) holds it against the cards in both directions: a
row the ledger says landed must be on both records with the grade and the source
it claims, and a pair the ledger refused must carry no row at all.

The refusals are the more useful half. Only one of the eleven fails for want of
evidence about the relationship; ten fail because **the other person is not in
this layer** — a bride at Naperville, a Potawatomi chief at the Calumet, an
unnamed daughter of Payne, and above all the 54 married couples of St Mary's
baptismal register, 85 of whose Chicago adults reach no surname here at all. The
town is thin on kinship mainly because it is thin on the women and on the French,
Métis, Irish and German Catholic households the poll books never recorded.
