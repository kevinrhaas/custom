---
id: T-1010
title: The 1 January 1834 return, tied line by line: which of the 170 printed lines reaches a claim and a card, and the two residues named in full
state: claimed
epic: PAPERS
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-1008
opened: 2026-09-10
closed: null
pr: null
claimed_by: run 9/10/2026, 7:13:31 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34544839640
---

The 1 January 1834 return, tied line by line: which of the 170 printed lines reaches a claim and a card, and the two residues named in full.

Piece 1 of 3 of **T-1008 — The ninety-two lines of the 1 January 1834 letter list the crops never carried are read but unminted, and the 97 residents minted from it are a floor of a 170-name return**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The tie is DERIVED by a committed tool and re-derived by the gate, never hand-assembled.
- Every instrument that may tie a line is exact. A line no instrument reaches is reported
  untied and named in full; nothing is assigned to its nearest neighbour.
- The table is honest in BOTH directions: printed lines no claim reaches, and cohort cards
  no printed line reaches, are both counted and both named.
- The three lines that are not one person are classified from the roster's own declaration
  and what the mint pass does with each is recorded.
- Where a card's name and the image's reading disagree, the disagreement is recorded and
  not repaired — renaming a resident is the same decision as minting one (T-1008).

**Shipped.** `tools/letter_list_1834_01_01_crosswalk.py` and
`data/research/newspapers/letter_list_1834_01_01_crosswalk.json`, gated by `check.sh`
(`--check` + `--self-test`). What it measures, on the tree it was written against:

| | |
|---|---|
| printed lines | 170 |
| tied at the image (`read_at_image.printed_line`) | 76 |
| tied by exact text, unique | 32 |
| tied by a unique surname, both directions | 5 |
| **untied** | **57** |
| claim entities of the return's nine impressions | 177 |
| entities tying to no printed line | 64 |
| lines reaching a minted card | 33 |
| lines reaching no card | 137 |
| cohort cards reached by no printed line | 14 of 47 |
| cards whose name the image contradicts | 2 (`hh_plumer_f`, `hh_pease_h`) |

The headline correction the parent asked for: the cohort the town holds is **33** of the
printed 170, not the 97 T-0310 minted — most of those 97 have since been absorbed into
cards standing on stronger evidence, or refused by refusal 8.

A FOURTH TIE INSTRUMENT WAS MEASURED AND REFUSED: surname plus given-name initials,
unique both ways, ties exactly one further line. Everything looser is fuzzy matching over
OCR, which is T-1005's epic. The refusal is written into the tool's docstring so the next
run meets the reasoning rather than rediscovering the option.

**Links:** T-1008 (parent) · T-1011 (the mint) · T-1012 (the Carriers) · T-0424 · T-0310
