---
id: T-0907
title: publish.sh minifies four resident files the committed mirror carries pretty-printed, and the T-0838 drift ratchet reads the mirror, so any run that publishes fails a gate it did not break
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

publish.sh minifies four resident files the committed mirror carries pretty-printed, and the T-0838 drift ratchet reads the mirror, so any run that publishes fails a gate it did not break.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0769's run**, which published a Newberry-index change and failed
`tools/synthesize_resident_research.py --drift` on four files it never touched:
`site/chicago/4d/data/residents/households/hh_adams_william_h.json`, `hh_miller_john.json`,
`hh_murphy_john.json` and `site/chicago/4d/data/residents/index.json`. `./tools/publish.sh`
rewrites them minified (194 lines to 1); the committed mirror carries them pretty-printed.
The drift ratchet reads the MIRROR, so publishing anything at all reports drift in the
residents layer.

T-0769 restored those four from `origin/dev` rather than carry another ticket's drift, so
the mirror is one publish behind on them and the next publish will re-open it.

**Acceptance:** one of — publish.sh stops reformatting these four, or the ratchet reads the
tree rather than the mirror, or the mirror is landed minified with the baseline moved to
match. Whichever it is, `./tools/publish.sh && bash tools/check.sh` is green twice in a row.
