---
id: T-0353
title: The Chicago American dissolves Goss & Cobb in February 1835 and the firm is still standing in the town on 1 July, board and all
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

**A standing record is wrong at the scene date and the corpus already knows it.**

`data/structures/goss_cobb_saddlery.json` stands a saddler's shop at Lake and
Canal on the Chicago Democrat of 1833-11-26, and says so honestly: *"Nothing
reached follows this firm past November 1833 … THE WHOLE RANGE IS THEREFORE
CONJECTURAL … TO RESOLVE: further issues of the Chicago Democrat or the Chicago
American. One line of an 1834 or 1835 advertisement would settle the survival and
might settle the corner."*

The American settles it, and it settles it **against the firm**:

- `chicago_american_1835_06_08#c006` and `chicago_american_1835_06_13#c015` —
  *"NOTICE. The co-partnership heretofore existing under the firm of Goss & Cobb
  … is this day dissolved by mutual consent. OLIVER GOSS. S. B. COBB. Chicago,
  Feb. 18, 1835."* The extraction sets `contradicts`, and the gazetteer's
  compiler already **refuses to stand Goss & Cobb in the 1835 town** under the
  owner's ruling 3.
- `chicago_american_1835_06_13#c016` and `_07_11#c008` — *"S. B. COBB will
  continue the above business at his shop, corner of Lake and […] streets"*,
  three printings between 8 June and 11 July 1835.

So on 1835-07-01 the shop SURVIVES — which the record calls conjectural — and
the FIRM does not, which the record asserts. Its `name`, its `occupants` and its
signboard (`GOSS & COBB / Saddle & Harness Making / Lake & Canal Streets`) all
say a partnership that had been dissolved for four and a half months.

Visible: the board on Lake Street repaints. No geometry moves — signage is drawn
at load from `data/signage/town_business_signboards.json`.

Found by T-0306 while adjudicating the American's placements; not folded into it,
because a correction to a different building is a different unit.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- `goss_cobb_saddlery` carries the dissolution and the continuation, with all
  four claims cited by issue, page and column, and its `documented_range` moves
  from conjectural to documented at the scene date.
- The record's name/aka and `occupants` say S. B. Cobb continuing alone; the
  board repaints out of `SIGN_WORDING` in the register the man's own card uses.
- The corner stays unread — `[uncertain: Amor.]` / `[uncertain: Balle]` in three
  printings — and no cross street is substituted. T-0305 owns that half.
- The record's own "TO RESOLVE" paragraph is rewritten rather than left standing
  under an answer.
