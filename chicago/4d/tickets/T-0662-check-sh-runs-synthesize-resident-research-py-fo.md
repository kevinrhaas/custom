---
id: T-0662
title: check.sh runs synthesize_resident_research.py for three mint steps whose labels name a different pass, so mint_documented and mint_letter_list drift ungated
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---
`tools/check.sh` has three steps whose labels name three different mint passes and
whose commands are all `python3 tools/synthesize_resident_research.py --check`:

- "the documented residents on reconstructed roofs re-derive from the register"
- "the minted documented residents re-derive from the register"  → should be
  `tools/mint_documented_residents.py --check`
- "the minted letter-list residents re-derive from the register"  → should be
  `tools/mint_letter_list_residents.py --check`

So two of the three passes that write `data/residents/households/` are not gated at
all, and both have drifted on `dev`. Measured on 2026-09-04 against a clean
`origin/dev` tree, where `check.sh` itself exits 0:

    mint_documented_residents.py --check    →   7 file(s) differ
    mint_letter_list_residents.py --check   → 743 file(s) differ

T-0418 absorbed the 6 households of the documented pass's drift because it had to run
that pass, and deliberately did NOT run the letter-list pass: 743 files is not a
by-product, it is its own unit of work that wants its own reading before it lands.

**Acceptance:** the three steps invoke the passes their labels name; whatever the
letter-list pass's 743 files turn out to be is read before it is written — the drift is
either a real re-derivation to commit (with what changed and why stated) or a fault in
the pass; `check.sh` is green afterwards with the corrected steps in place, so the two
passes cannot drift ungated again.
