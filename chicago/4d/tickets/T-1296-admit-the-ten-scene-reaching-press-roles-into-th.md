---
id: T-1296
title: Admit the ten scene-reaching press roles into the 1835 occupation field by making the four generators that own it agree
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Admit the ten scene-reaching press roles into the 1835 occupation field by making the four generators that own it agree.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-1254, 2026-09-17, with the evidence already on the cards.** The newspaper
gazetteer's migration put ten roles on resident cards whose bound CONTAINS 1 July 1835 —
L. G. Curtiss printed an attorney in the Democrat of that very day, Tuthill King a
clothier, Silas Sherman the sheriff of Cook County, James Mulford a jeweller, a
silversmith and a watchmaker, and six more. Every one of them is dated, cited and
graded `inferred`, and every one of them carries `fills_scene_view: false`: it reaches
the day and does not stand in the singular `occupation` field.

That gap is deliberate and it is not a judgement about the evidence. FOUR tools derive
that one field and only one of them was taught about roles:

- `tools/derive_resident_roles.py` — the roles view (T-1229).
- `tools/qualify_later_trades.py` — T-0693's later-trade pointer, which re-derives the
  block and reverts a value it did not write.
- the ladder resident pass — `the civic, church, press and book residents re-derive from
  the ladder` re-derives the same cards.
- T-0837's write gate (`audit_scene_window_trades`) — which refuses a standing 1835 trade
  whose block cites no 1835 source of its own, and a promoted block cites nothing,
  because its citations are on the role rows.

T-1254 measured all four against a promotion and got 17 red gate steps, including
`the trade-census gap is spent from the layers that hold it` (a card the occupation count
could suddenly see and no practitioner ruling held). Making them agree is a unit of work
in its own right, not a clause of a migration.

**Acceptance:**

1. One tool owns `persons[].occupation`. The other three read it or are taught to derive
   the same value; none of them reverts what another wrote.
2. A promoted block cites the sources of the roles that fill it, so T-0837's write gate
   sees an 1835 source and passes on the evidence rather than on an exemption.
3. The ten roles above carry `fills_scene_view: true`, the ten cards read their trade,
   and `docs/RESEARCH/roles-migration-2026-09.md` re-derives with them admitted.
4. `tools/trade_census_spend_1835.py` counts the ten against its occupation lines, or
   rules each one out in writing. A card the count cannot see is a man the town loses.
5. No card LOSES a trade it holds today.

**Links:** T-1145 · T-1229 · T-1254 · T-0693 · T-0837 · T-0991.

6. **And the card shows a role's place and employer.** T-1255 shipped `rolesHtml` while
   T-1254 was in flight, so the timeline reads ten of a role's figures and not the two
   T-1254 added: `place` (where the role was worked) and `employer_or_body` (the body or
   firm it was worked for) are banked UNREAD in `tools/layer_reads_baseline.json` because
   they did not exist when the renderer was written, not because nobody should see them.
   164 roles carry a place and 56 a body. Declare both in `measure_layer_reads.py` READS
   with the expression that renders them, in the commit that renders them.
