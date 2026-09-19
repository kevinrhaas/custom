---
id: T-1383
title: The two women the St Mary's priest wrote down as Indigenous are the only adults on their own entries the borderline roster ruled ineligible, so the town carries their husbands and children and not them
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-19
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The two women the St Mary's priest wrote down as Indigenous are the only adults on their own entries the borderline roster ruled ineligible, so the town carries their husbands and children and not them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-1376, 2026-09-19, while reading the corpus for Native and Métis people the
sources NAME.**

`data/research/church/records/st_marys_baptisms_1833_1835.json` is the only source this
project holds in which a contemporary STATES an Indigenous identity for a named person at
Chicago — not a term in a later biography, the priest's own parenthesis on the page. Four
entries of 1833 carry one:

| entry | the words | people |
|---|---|---|
| 7 (at Ottawa, not Chicago) | *"of Ottaway"* | Francise Nowbonnois, Josette Ashkam |
| 14 | *"Marianne (sauvage)"* | wife of Antoine Aspam |
| 17 | *"Marianne (sauvage)"* | the same woman, second child |
| 18 | *"Jaespquaa (sauvage de Green Bay)"* | wife of Paul Vieaux |

The reading's own note on entry 14: *"'Sauvage' is his word for an Indigenous woman and it
is kept in as_read because it is the register's own vocabulary; it is not this project's."*
Entry 18 carries the only origin the book ever gives for a mother.

**The defect.** The borderline roster carries every other adult on those entries — Antoine
Aspam (twice), Josette Aspam (twice), Paul Vieaux, Jacob Vieau, and the children Jean
Baptiste, Magdelene, Susanne and Marie Josette — and T-1172 minted four of them into
`data/residents/readmitted/`. It does NOT carry **Marianne** or **Jaespquaa**: both sit in
the roster's `ineligible` list, normalised to `marianne` and `jaespquaa`. So the town holds
these two families' husbands and their children and not the two women the priest wrote down
as Indigenous — and the four cards that ARE in the town carry `community: null`,
`touches_removal: false` and no kinship to each other, though the register puts the whole
family on one dated line.

**Why T-1376 filed it rather than spending it.** A baptism is not a residence, and the
ineligibility ruling is the RESEARCH layer's, not a reconstruction stage's to overturn from
outside with a one-line patch — the roster is generated, and a stage that hand-edited its
output would be un-derivable by the next run. The honest fix is in the roster's own
eligibility rule, and it wants its own demonstration.

**What it should answer.** Why the two readings are ineligible (a forename-only name? the
parenthesis? something else — the `ineligible` rows carry a `rule` key and the reason should
be read, not guessed); whether the rule is right in general and wrong here; whether the
Aspam and Vieaux cards should be one household each rather than one person each, since the
register states the kinship on one line; and whether those cards should carry
`review_required` + `touches_removal` and a community, which they do not today. Stage
`underdocumented` (T-1177) is the only stage licensed to write the last of those.

