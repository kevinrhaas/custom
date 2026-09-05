---
id: T-0839
title: synthesize_resident_research.py carries a second, divergent derivation of the residents manifest, and T-0715's owner is the first
state: open
epic: META
requested_by: loop
seen: false
effort: XS
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

synthesize_resident_research.py carries a second, divergent derivation of the residents manifest, and T-0715's owner is the first.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found closing T-0715, 2026-09-05.** T-0715 gave `data/residents/index.json` one owner —
`tools/rebuild_resident_index.py`, gated in `check.sh` as a re-derivation — and pointed
`mint_civic_residents.apply()` and `apply_regrade()` at it. One writer was deliberately left
alone: `synthesize_resident_research.rebuild_index()`.

## Why it is still a fault

It is a SECOND implementation of the same derivation, and the two have already diverged.
The owner writes each of `letter_list_only`, `civic_mint`, `projected_resident` and
`census_1840_linked` only when the cards support it; the synthesizer starts each row from
`row = dict(old.get(hid) or {})` and re-derives three of those four — `civic_mint` is
carried across from the previous row and never checked against the persons on the card. So
the one flag it does not derive is the one that can go stale, which is T-0715's fault
wearing a different hat.

The projected_resident shape is the visible half of the same split: the mint's writer used
to emit `projected_resident: false`, the synthesizer popped it, and 450 rows carried a key
211 identical-in-meaning rows did not.

## The ask

`rebuild_index()` calls `rebuild_resident_index.rebuild(index, docs)` and keeps only what is
genuinely its own — the `_doc` sentence, the `vocabulary.resident_subtypes` entry, and
`counts.reconstructed_removed_in_2026_09_02_synthesis`, which is a frozen historical figure
and not a tally of the layer.

## Why it was not done in T-0715

T-0838 was in flight on that same file and function on 2026-09-05, and a conflict in the
synthesizer is worth more than the tidy-up. The gate T-0715 landed catches the divergence in
the meantime: if the synthesizer writes an index the owner would not, `check.sh` goes red.

**Done when** one derivation of the manifest exists in this repo, and `check.sh` still passes.
