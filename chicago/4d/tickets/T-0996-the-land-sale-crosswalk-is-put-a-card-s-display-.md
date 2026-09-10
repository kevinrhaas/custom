---
id: T-0996
title: The land-sale crosswalk is put a card's display NAME and never the spellings its own evidence carries, so BLANCHARD GURTREY refuses the man Fergus 1843 prints as Francis Gurtrey
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The land-sale crosswalk is put a card's display NAME and never the spellings its own evidence carries, so BLANCHARD GURTREY refuses the man Fergus 1843 prints as Francis Gurtrey.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**FOUND BY T-0993**, which ruled the Blanchard pair and then could not file the
land-sale half of its own acceptance.

`build_resident_crosswalk` hands `namesake.choose` one string per candidate — the
person's display name, `" ".join(name.split()[:-1])` — and nothing else. So the reading
is put to ONE spelling of a man who may be printed five ways in the sources his own card
cites. The register's six `BLANCHARD GURTREY` rows (ls0076–ls0081, school-section lots,
22–24 October 1833, $547.00) refuse against `F Gantry Blanchard` on two counts that are
both artefacts of that: the first given word is `F` and the register prints only the
second, and the card spells the second `Gantry` where the register spells it `GURTREY`.
The man's own card quotes Fergus 1843 printing him whole — *"Blanchard, Francis Gurtrey,
capitalist, res 45 Wells"* — in `book_evidence`, where the crosswalk never looks.

The ruling on those six rows is already written, in full, under
`data/research/land_sales/resident_rulings.json` → `referred_the_gate_cannot_hold`,
because `check_rulings()` admits a ruling only on a spelling the mechanical rule
proposed. It is right to admit only those; the fix is to make the proposal see what the
card knows, not to widen what the gate accepts.

**Acceptance.** `namesake.choose` is put every spelling a candidate's card carries —
the display name plus the `as_read` of its own `civic_evidence` / `book_evidence` /
`press_evidence` / `census_evidence` blocks, surname stripped — with the RULE unchanged:
the same M1/M2/M3, R3/R4, rules 2, 3, 4 and 7, and two survivors or none still a refusal.
A reading named on a source spelling rather than the display name says so, in the
proposal's own `rule` text and with the record id of the printing that carried it, so a
reader can go back to the page. Measured before and after over all 431 purchaser
spellings, with every reading that MOVES listed in the PR and each one ruled; the six
`BLANCHARD GURTREY` rows move into `ruled[]` under this ticket's number, and the block
they came out of records that they did. `read_land_sales.py --check` and
`namesake.py --self-test` green, and no reading that was named before becomes ambiguous
without its rivals being named in the refusal.
