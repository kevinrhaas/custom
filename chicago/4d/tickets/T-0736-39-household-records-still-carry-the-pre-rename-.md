---
id: T-0736
title: 39 household records still carry the pre-rename word for attested in their source_pass, the last place the old vocabulary survives in the data
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

39 household records still carry the pre-rename word for attested in their source_pass, the last place the old vocabulary survives in the data.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0517** while rewriting `docs/RESEARCH/residents_1835.md` for the current model.

**The finding.** The person-grade vocabulary was renamed to `attested` / `inferred` /
`reconstructed`. `tools/validate.py` rejects the older `recommended` *by name*, and the dossier
no longer contains the pre-rename word at all. But 39 household records still carry it as the
value of `source_pass`:

```
python3 - <<'PY'
import json, glob
from collections import Counter
c = Counter(json.load(open(f)).get('source_pass')
            for f in glob.glob('data/residents/households/*.json'))
print(c)   # {'letter_list': 727, 'civic': 531, 'documented': 39, None: 78, 'placed': 5}
PY
```

**What it is and is not.** `source_pass` is a provenance label naming the mint that made the
record, not a grade, and nothing reads it as one — no gate, no renderer, no ladder rung. So this
is not a correctness bug. It is the last place in the data where the retired vocabulary survives,
and the reason that matters here is the rule the rename was made under: *a vocabulary that merely
omits a word gets it back the first time somebody copies an older file.*

**The ask.** Rename the value on those 39 records to something that names the mint rather than a
grade — `register` is the honest word, since those are the records minted from the register pass
— and add `source_pass` to `index.json`'s `vocabulary` so it is a closed set the validator holds,
which is what would have caught this. Regenerate anything derived. Do NOT silently rewrite it as
`attested`: that would put a grade word back into a provenance field, which is the conflation the
two-axis table in the dossier exists to prevent.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- No `source_pass` value in `data/residents/households/*.json` is a grade word; `index.json`
  declares the closed set and `tools/validate.py` fails a record outside it, tested in
  `tools/test_validate.py`.
- `check.sh` green, including the mint re-derivation steps that read these records.

**Links:** T-0517 (found it) · T-0638 (the id rename, the other half of the same tidy-up) ·
`docs/RESEARCH/residents_1835.md` § 2
