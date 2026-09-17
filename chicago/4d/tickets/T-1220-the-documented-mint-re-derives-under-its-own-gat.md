---
id: T-1220
title: The documented mint re-derives under its own gate: one adjudicated person is one candidate, and refusal 6 is the reading test the place vocabulary says it is
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0662
opened: 2026-09-17
closed: null
pr: null
claimed_by: run 9/17/2026, 2:49:31 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35193523780
---

The documented mint re-derives under its own gate: one adjudicated person is one candidate, and refusal 6 is the reading test the place vocabulary says it is.

Piece 1 of 2 of **T-0662 — check.sh runs synthesize_resident_research.py for three mint steps whose labels name a different pass, so mint_documented and mint_letter_list drift ungated**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

Two faults, both found by running the pass the parent's step label names.

**F1 — one man, two printings, and they arrived as rivals.** `register_1835.json` does
not only read names, it ADJUDICATES them: two printings it has resolved onto one person
carry the same `action_target`. The mint iterated the printings, so `Grant, J., Jr.`
(militia officer, Democrat, 3 September 1834) and `James Grant` (attorney and counsellor
at law, La Salle Street, 10 June 1835) — one man by the register's own ruling — competed
for the one Grant household refusal 8 allows, and the loser was refused as a duplicate of
himself. `hh_grant_james` became `hh_grant_j` and the town's attorney became a militia
officer. Fifteen of the pool's people are read from more than one printing.

**F2 — refusal 6 read a premises as somewhere else.** The gazetteer prints L. W.
Montgomery, shoemaker, seven times, at `Chicago`, `South Water Street` and
`P. Cohen's store`. No roof is committed under that store's name, so `in_town_places()`
could not resolve the string and the refusal read it as evidence the man was elsewhere.
`data/research/newspapers/place_vocabulary.json` states the rule the refusal was meant
to be: "a reading that names only such places is not a Chicago appearance" (B2).

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- `tools/check.sh`'s step "the minted documented residents re-derive from the register"
  runs `tools/mint_documented_residents.py --check` and not another pass's tool.
- Candidates the register folds onto one `action_target` mint ONE household, carrying
  the union of every printing's mentions, variants, trades and places, filed under the
  id the register's own answer names. A name the transcription bracketed as uncertain,
  and a firm, are not folded into a clean man's evidence.
- Refusal 6 refuses a READING that resolves nothing inside the town, and a person only
  when every one of his readings does. `hh_grant_james` and `hh_montgomery_l_w` stand;
  `hh_grant_j` does not; the postmaster Levi F. Arnold, the sheriff Stephen Forbes and
  the justice Stephen M. Salisbury — each printed once beside Plainfield, Cook County
  and the Dupage — do not move.
- The drift the corrected gate then reports is committed, with every downstream
  derivation rebuilt against it, and `check.sh` is green.

**Not in this ticket.** Admitting `A. Clybourn` is not a side effect this pass may take:
the town already holds `clybourne_archibald`, and `measure_card_fuzzy_candidates.py
--self-test` refuses the one-letter duplicate that admission would make. That pair is
T-1002's open question and the refusal-7 surname proxy's blind spot, not this one's.
