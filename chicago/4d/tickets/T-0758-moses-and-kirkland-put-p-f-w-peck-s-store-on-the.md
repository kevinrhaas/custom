---
id: T-0758
title: Moses and Kirkland put P. F. W. Peck's store on the south-EAST corner of South Water and La Salle, and hh_peck_philip puts it south-west - and the project holds two Peck households
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

Moses and Kirkland put P. F. W. Peck's store on the south-EAST corner of South Water and La Salle, and hh_peck_philip puts it south-west - and the project holds two Peck households

**Found by T-0581**, reading Moses and Kirkland's *History of Chicago* vol. 1 (1895).

**Two findings, one ticket, because they are the same record.**

1. **The corner disagrees.** `data/residents/households/hh_peck_philip.json` puts Philip F. W.
   Peck's two-storey frame store at the **south-west** corner of South Water and LaSalle, and
   calls it "the anchor of the town's business street in this dataset". Moses and Kirkland put
   it on the **south-east** corner of South Water and La Salle
   (`bk_mk1_001`), in the same sentence that puts George W. Dole's on the south-east corner of
   South Water and Dearborn. The 1895 volume is tier 4 and is the weaker witness; Andreas, which
   `hh_peck_philip` already rests on, is the one to re-read. THE POINT IS THAT AN ANCHOR OF THE
   BUSINESS STREET HAS TWO CORNERS IN THE CORPUS AND NOTHING SAYS SO.

2. **There are two Peck households.** `hh_peck_philip.json` carries `peck_philip`, "Philip F. W.
   Peck", occupation merchant, attested off `andreas_1884_v1`. `hh_peck_p_f_w.json` carries
   `peck_p_f_w`, "P F W Peck", occupation `none_recorded`. Moses and Kirkland's contents list
   prints "Peck, Philip F. W." for the sketch its running text calls "Mr. P. F. W. Peck"
   throughout, which is one book equating the two spellings on its own pages
   (`bk_mk1_034`, `bk_mk1_028`). T-0581 merged the volume's reading into `peck_philip` and
   refused to touch the pair, because whether the two households are one man is a question about
   the residents layer.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)
- Andreas re-read at the page `hh_peck_philip` cites, and the corner it actually prints written
  down verbatim — then the record corrected or confirmed, with the disagreement noted either way.
- A ruling on `peck_philip` / `peck_p_f_w`: one household or two, with the rule naming both
  spellings verbatim in `data/research/residents/identity_master.json`'s shape.
- If they are one, the merge carried through the households and the counts; if two, the reason.

**Links:** T-0581 · `data/research/books/crosswalk.json` (the T-0581 pass) ·
`data/research/books/claims/moses_kirkland_history_of_chicago_v1_1895.json`
