---
id: T-0927
title: publish.sh re-minifies four resident mirror files and check.sh's T-0838 baseline then fails: any run that publishes trips a gate it did not break
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

publish.sh re-minifies four resident mirror files and check.sh's T-0838 baseline then fails: any run that publishes trips a gate it did not break.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`tools/publish.sh` writes the site mirror with minified JSON — one line per file, which is
what every other file under `site/chicago/4d/data/residents/` carries. Four files are
committed to the mirror UNMINIFIED instead:

    site/chicago/4d/data/residents/households/hh_adams_william_h.json
    site/chicago/4d/data/residents/households/hh_miller_john.json
    site/chicago/4d/data/residents/households/hh_murphy_john.json
    site/chicago/4d/data/residents/index.json

So `publish.sh` re-minifies them on every run, and `check.sh`'s resident-synthesizer ratchet
then reports all four as "drifted from the writer and is not on the T-0838 baseline" and the
gate goes red. The content is IDENTICAL either way — parsed, dev's copies and the published
copies compare equal — so the ratchet is firing on whitespace, and the run that trips it did
not touch a resident record.

Found by T-0754, whose diff was one census page-record and a changelog entry. It published,
as every PR must, and lost a gate run to this. The workaround it used was to restore the four
files from `origin/dev` after publishing, which is exactly the kind of undocumented step that
the next run will not know to take.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Either the four mirror files are re-minified once and the T-0838 baseline re-taken so that
  `publish.sh` and `check.sh` agree, or the ratchet compares PARSED JSON rather than bytes so
  that formatting cannot trip it. One or the other, not a note telling runs to restore files.
- `./tools/publish.sh && ./tools/check.sh` is green on an otherwise untouched checkout of dev.
- Whichever is chosen, the reason is written down where the next reader of the ratchet finds it.

**Links:** T-0838 (the baseline) · T-0754 (found it) · `tools/publish.sh` · `tools/check.sh`
