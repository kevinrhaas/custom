---
id: T-0275
title: The newspaper deposit is on main only, so dev cannot resolve 66 of the corpus's text paths
state: open
epic: PAPERS
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

`chicago/reference/newspapers/` — the ~103-file transcription deposit the PAPERS
epic reads — was pushed straight to `main` on 2026-08-27 (commits `0d97621e` and
`b9d427c7`) and `dev` has never been back-merged. So on `dev`, and on every
branch cut from it, the directory does not exist.

T-0256 shipped the corpus index against this. Its gate,
`tools/check_newspaper_corpus.py`, verifies every text path BY CONTENT — the
sha256 is recorded on every entry — and it resolves and hashes all 66 reference
paths when the deposit is in the tree, which was checked both ways on that
branch. On `dev` it reports, out loud and with the reason, that 66 paths could
not be opened. The 23 derived files this repository owns resolve on every branch
unconditionally, so nothing is silently green.

That is a safe deferral, not a fix. Until the deposit is on `dev` the extraction
tickets below T-0256 in the queue (T-0257 to T-0262) can be written but their
readings cannot be re-derived on the branch they merge to.

**WHY THIS IS THE OWNER'S CALL AND NOT AN AGENT'S.** The obvious remedy is a
`main` → `dev` back-merge, and it is not clean. `main` is 3 commits ahead of the
merge base and those commits carry, besides the deposit, **459 files of macOS
duplicate-name artefacts** — `… 2.glb`, `… 2.json` under `chicago/4d/assets/web/`
and `chicago/4d/data/sidecars/1835/`, 86,792 lines — plus a `.gitignore` change.
A back-merge takes all of it onto `dev` and then, at the next promotion, back
onto `main` as though it had been reviewed. Deleting them is a judgement about
the owner's own commits. The 4D agent lane is also scoped to `chicago/4d/` and
its published mirror and may not touch `chicago/reference/`.

So this ticket is a question with three answers, and one of them has to be
chosen by the person whose repository it is:

1. Back-merge `main` → `dev` as it stands, duplicates and all, and clean them in
   a separate commit on `dev`.
2. Delete the 459 duplicates on `main` first, then back-merge.
3. Leave `dev` without the deposit and accept that the reference half of the
   corpus is verified only on `main` and at promotion. This costs nothing today —
   the gate already reports it — and costs the extraction tickets their re-derivation.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The owner has chosen one of the three, and it is recorded here.
- If 1 or 2: `tools/check_newspaper_corpus.py` on `dev` prints "the deposit is in
  this tree; every reference path was resolved and hashed", and no `… 2.glb` or
  `… 2.json` duplicate reaches `dev`.
- If 3: this ticket is withdrawn with the reasoning, and T-0256's source records
  say that the reference half is verified at `main` only.
