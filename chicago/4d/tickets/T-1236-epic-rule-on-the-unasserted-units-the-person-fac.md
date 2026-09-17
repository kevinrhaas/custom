---
id: T-1236
title: EPIC: rule on the unasserted units the person-fact passes do not own — the land-sale, civic, 1830-census, church, newspaper and directory names, the resident-pass reserved people, and the book readings of ground, harbour, weather, price and institution
state: open
epic: META
requested_by: loop
seen: false
effort: L
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

EPIC: rule on the unasserted units the person-fact passes do not own — the land-sale, civic, 1830-census, church, newspaper and directory names, the resident-pass reserved people, and the book readings of ground, harbour, weather, price and institution.

Filed by T-1234, which spent the corpus its own title named — the book-domain PERSON
units and the letter-list name suspicions — and left behind the units the ledger's
default owner rule had been routing to it without its title ever covering them. This is
that remainder, and it is an EPIC: it is more than five tickets' worth and the loop does
not work it until the owner promotes pieces out of it.

**What is in it** (counts as of the ledger rebuilt on T-1234's PR):

| corpus | units | what a ruling would have to say |
| --- | ---: | --- |
| land_sales | 1,572 | a purchaser's name against the standing rule that a sale is never a residence |
| civic | 496 | the poll and voter names the civic crosswalk has not adjudicated |
| residents, cohort passes | 382 | the reserved people of the pilot and passes 02-15 whose findings name no exact structured field |
| newspapers | 378 | the person units of the thirteen held issues that no card names |
| church | 272 | the register entries outside the later-only and outside-Chicago rulings |
| census_1830 | 204 | the 1830 heads, five years before the scene and on the same ladder as 1840 |
| books, non-person readings | 61 | the ground, harbour, weather, price, shipping, institution and household readings |
| directories | 18 | the entries the directory pass left unruled |
| genealogytrails | 1 | one unit |

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

1. Each corpus above is taken as its own ticket, split out of this one when the owner
   promotes it, and closed by rulings that are WRITTEN — a rule with a statement and a
   note per unit, in the shape `data/research/spend_rulings.json` established, or by an
   assertion onto a structured resident field. A silent reclassification is a fail.
2. No ruling upgrades a confidence, mints a person or invents a citation, and a hand-off
   names an OPEN ticket whose field genuinely owns the finding.
3. `tools/measure_research_spend.py --check` stays green, and when the last corpus is
   ruled the ledger carries no unresolved unit owned by this ticket.

**Links:** T-1234 (the pass that filed this) · T-1232 · T-1143 · T-1147 · T-1157.
