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
(known only from the post office's letter lists). Until T-0598 each pass
stamped its own prefix onto the id it minted — `hh_doc_`, `hh_placed_`,
`hh_ll_` — so a tool could recognize "a household I minted" by filename alone,
for its own stale-file cleanup and precedence-skip logic.

**`hh_placed_` was never a location.** Every household from that pass carries
`"division": "unplaced"` — "placed" names the pass's own residency EVIDENCE
test (PART ONE of its docstring: does the corpus put this person inside the
town, as opposed to outside it), not a lot or plat position. See the note in
`tools/mint_placed_residents.py` right above `PART ONE — PLACEMENT`.

**As of T-0598, no new household is minted with a legacy prefix.** A
household minted by any of the three tools from here on gets the same plain
`hh_<surname>_<given>` id the ~73 hand-authored households already use, and
records which pass minted it in `source_pass` (`"documented"` / `"placed"` /
`"letter_list"`) instead. The tools still recognize their own prior output —
`minted_by()` checks the legacy prefix OR the `source_pass` field — so a
second run stays idempotent across the migration boundary and a household
never needs two ids for the same identity.

The **747 households already minted under a legacy prefix before T-0598** were
not renamed by that change alone — filenames are load-bearing (cross-referenced
by hardcoded ids in several frozen, gated selector scripts and by the
resident-research findings ledgers) and a rename touching all of them is its
own, separately tracked migration. Until that migration lands, a legacy-prefixed
filename on disk is not a signal of anything about the person it names — check
`source_pass` (once migrated) or just the household's own `grade`/`letter_list_only`
fields, never the filename, for what a household actually is.

`hh_inf_*` (5 files) is `tools/generate_inferred_households.py`'s own, unrelated
pipeline and is not part of any of the above.
