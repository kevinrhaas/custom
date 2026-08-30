---
id: T-0428
title: derive_timber_belt.py --write leaves trees.js unparseable when the derived belt has more points than the committed one
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-30
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

`tools/derive_timber_belt.py --write` rewrites `FAR_TIMBER.main_stem_belt_east`'s `path:`
literal in `renderers/web/js/trees.js` by substituting the LINE the literal starts on. The
committed literal spans two lines. When the derived belt has more points than the committed
one the replacement is longer, wraps onto three lines of its own, and the literal's ORIGINAL
second line is left standing underneath it:

```js
    path: [[89.53, -83.21], [105.02, -83.19], [128.21, -66.1],
      [148.49, -43.78], [167.3, -27.8], [185.06, -16.25], [221.7, -6.18],
      [329.41, -5.2]],
      [185.06, -16.25], [221.7, -6.18], [329.41, -5.2]],   // <- orphan
```

That is a syntax error, and `trees.js` is a renderer module: the walkthrough does not boot.
Found on 2026-08-30 by T-0183, which moved South Water Street's west end and so took the
belt from 7 points to 8 — the first time the derived line has been longer than the committed
one. The tool's own `--check` still passed afterwards, because it re-reads the array by
evaluating the module's data rather than parsing the file, so nothing in the tool noticed.
`tools/check.sh` did catch it, at the `renderer modules parse` step, which is why this is a
defect in a tool and not an outage — but the repair was made by hand in that run, which is
exactly what rule 4 of AGENTS.md says a generated artefact must never need.

**Acceptance:** `--write` replaces the whole `path:` literal however many lines either the
old or the new one occupies, and a self-test drives it over a committed literal spanning one,
two and three lines with a derived belt shorter, equal and longer, asserting
`node --input-type=module --check` on the result every time.
