---
id: T-0896
title: publish.sh minifies four resident mirror files that synthesize_resident_research.py writes indented, and the T-0838 drift ratchet reads the whitespace as drift
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

publish.sh minifies four resident mirror files that synthesize_resident_research.py writes indented, and the T-0838 drift ratchet reads the whitespace as drift.

Found by T-0698, which tripped it and had to work around it.

`tools/publish.sh` minifies the resident JSON it copies into `site/chicago/4d/`.
`tools/synthesize_resident_research.py` writes the cards it owns into that same mirror
INDENTED. On `dev` four files are sitting in the writer's indented form —
`site/chicago/4d/data/residents/households/hh_adams_william_h.json`, `hh_miller_john.json`,
`hh_murphy_john.json` and `site/chicago/4d/data/residents/index.json` — and the T-0838
drift ratchet passes only because they are.

Touch any of them (T-0698 ran `mint_civic_residents.py --build`, which rewrites 491 cards)
and the next `publish.sh` minifies them, the writer's scratch copy still emits indented,
and the ratchet reports four files of DRIFT that differ from the committed mirror in
whitespace and in nothing else. Their parsed JSON is identical. T-0698 restored dev's bytes
for the four rather than grow an empty baseline with a formatting artefact, which works and
is not a fix: the next pass that touches those cards meets the same wall.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- One of the two writers gives way, and the choice is stated: either `publish.sh` leaves the
  files `synthesize_resident_research.py` owns alone, or the writer emits what the publish
  path emits. Byte-identity across the two is the acceptance, not a baseline entry.
- `synthesize_resident_research.py --drift` is green on a tree where every resident card has
  been rewritten and republished — the case that fails today.
- The T-0838 baseline is still empty afterwards. A formatting artefact must not be the thing
  that first fills it.

**Links:** T-0838 (the ratchet) · T-0837 (which spent the baseline to zero) · T-0698.
