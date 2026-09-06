---
id: T-0860
title: A printing that named a street and no anchor, superseded by one of the same house that names one: T-0440 one rank up
state: open
epic: META
requested_by: loop
seen: false
effort: M
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

A printing that named a street and no anchor, superseded by one of the same house that names one: T-0440 one rank up.

FOUND WHILE RULING T-0773. Two of the six houses a later printed address outranks —
`business_j_s_c_hogan` and `business_newberry_dole` — are outranked from a live placement
that names NO ANCHOR. Hogan's 1834-03-25 card gives South Water Street and stops, and
'the Post Office' is first printed on 1834-08-13; Newberry & Dole's live reading names
neither anchor nor a street the model holds, and 1834-05-14 reads 'opposite to Fort
Dearborn'. Both are refused an `anchor_changes` rule and the refusal is right: one anchor
is not a change, and calling a silent printing the earlier of two anchors would assert a
move nothing printed says. See `identity.json` § `refused_anchor_changes` and
`docs/RESEARCH/printed_address_outranked.md` § 3.

But the refusal answers a question nobody asked. **T-0440 ruled that silence about an
address does not outrank speech about one, and stopped at `placement_rank == 0`.** These
two are the same argument one rung up: a printing that named a STREET and no anchor,
against a printing of the same house that names one. A card that gives 'South Water
Street' one week and 'in South Water Street, one door from the Post Office' the next has
not contradicted itself; it has said more. If that is right, the rule is a bounded
extension of the T-0440 pass and not a judgement between two addresses — and Hogan gains a
placement the town can use.

It is NOT obviously right, which is why it is its own ticket. The counter-case is that a
street named without an anchor is a positive statement about the frontage and a later
anchor may sit on another street entirely; the street-face adoption policy (T-0354) has
already dealt a roof on the strength of the coarser reading, and moving the house off it
is a real change to the town, not a refinement of a field.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

1. The question is answered in writing, either way, where the other placement rules are
   stated — `compile_gazetteer.py` beside the T-0440 pass — and not only in code.
2. If the answer is yes: the extension fires ONLY where the outranked reading names no
   anchor, is bounded by the scene date exactly as T-0440's is, records where the
   placement came from, and never prefers one printed ANCHOR to another. Its own
   self-test cases fire when broken.
3. Whatever the answer, `business_j_s_c_hogan` and `business_newberry_dole` stop being
   refused for a reason that has been superseded: either the refusals go, or their
   `refused_because` says the question was asked and settled the other way.
4. Newberry & Dole is NOT moved to the north bank as a side effect — that is a structure
   to argue for and `docs/RESEARCH/dole_warehouse_south.md` carries the guard.
5. `bash tools/check.sh` green, and `tools/measure_placement_silence.py` re-derives with
   its three counts stated.

**Links:** T-0773 (which refused them and filed this) · T-0440 (the ruling one rank
lower) · T-0354 (street-face adoption) · T-0396 · `docs/RESEARCH/printed_address_outranked.md`.
