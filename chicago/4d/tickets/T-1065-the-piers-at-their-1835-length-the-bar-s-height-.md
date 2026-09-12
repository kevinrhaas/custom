---
id: T-1065
title: The piers at their 1835 length, the bar's height argued where the admission is, and the reservation's blue edge and the lighthouse checked against Wright's sheet
state: claimed
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0800
opened: 2026-09-12
closed: null
pr: null
claimed_by: run 9/12/2026, 5:44:16 AM CT
blocked_on: null
needs_bake: true
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34689035657
---

Piece 2 of 2 of **T-0800 — The mouth as built**. T-1066 took its fourth ask (the re-bake, and
the staleness hash that had been hiding the need for one). These three are what is left, in
the parent's own words:

1. **The piers as structures**, on Wright's alignment from the bend, at the 1835 length the
   dossier gives — north pier between 700 ft (1834) and 1,850 ft (Oct 1837),
   *"interpolate ~1,000–1,300 ft, flagged inferred"*
   (`docs/research/01-terrain-hydrology.md` § 3.2). **READ `data/structures/north_pier.json`
   AND `south_pier.json` FIRST — they already exist**, measured off Wright's two red lines
   through the committed affine, with a bearing check against the documented 200 ft entrance.
   What is open is the LENGTH: both records carry 900 ft, interpolated and argued on
   `form.length_m`, against the dossier's own 1,000–1,300 ft. Settle that, and say which of
   the two arguments the ticket is overturning. A length change moves geometry: re-bake the
   two structures with `tools/bake.sh --only`.
2. **The bar's height, argued.** The parent quotes the spec's admission *"THE HEIGHT OF THE
   BAR IS CHOSEN, NOT FOUND."* **The four-reason argument the parent asks for is already
   written in that same note** (the soldiers' ditches and the 1834 breach, CPL's reading of
   the 1839 Fort Dearborn Addition plat, the high-water phase, and the direction of the
   error). Either this ask is already discharged — say so and close it — or it wants the
   dossier's beach-ridge figures brought in beside them, which is a paragraph and a citation,
   not a re-argument.
3. **The reservation's blue edge** as T-0792's polygon closing on the traced old channel, and
   the lighthouse (`chicago_lighthouse_1832`) checked against Wright's *L. House* beside the
   fort. The committed position is adjacency turned into a coordinate and says so; Wright's
   glyph would be the first independent witness to it. This is a plate reading plus a
   baseline, in the idiom of `tools/measure_*.py` — and it is the piece with the most yield.

**Acceptance:** a stated pier length with the argument that chose it and the two structures
re-baked to it; the bar's height either shown already argued or argued from the dossier's
figures where the admission is; the lighthouse position measured against Wright's sheet and
either confirmed with the residual or moved with it.
