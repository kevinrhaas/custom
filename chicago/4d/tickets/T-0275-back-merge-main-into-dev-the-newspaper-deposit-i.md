---
id: T-0275
title: Back-merge main into dev: the newspaper deposit is on main, and 60 Finder-duplicate files on main turn the dev gate red
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

`dev` is missing three commits that are on `main`, and one of them is the owner's
newspaper deposit: `chicago/reference/newspapers/` — 163 files, 15.4 MB, the 86
transcribed issues the whole PAPERS epic reads. A `dev` checkout has
`chicago/reference/` WITHOUT `newspapers/`, so on `dev` no agent can open a single
issue. T-0256 shipped around it (derived text for the 23 .docx-only issues is
committed inside `chicago/4d/`, and the gate knows a present deposit from an absent
one), but every remaining ticket in the epic — T-0257 through T-0264 — has to READ
the deposit, and cannot.

## Why this is not a one-line merge

Measured on 2026-08-28, on a clean branch off `origin/dev`:

    git merge origin/main     # clean, no conflicts
    ./tools/check.sh          # CHECK FAIL — 23 steps red

`./tools/check.sh` on unmodified `origin/dev` is **CHECK PASS**. The 23 reds all come
from the merge, and they come from ONE thing: commit `0d97621e` ("Add Chicago
newspaper transcriptions and reference docs") also committed **sixty Finder-duplicate
files** under `site/chicago/4d/data/` — `recon_1835_north_d4_043 2.json`,
`recon_1835_north_w5_040__recommended_1835 2.glb`, and fifty-eight more of the same
shape. They are on `main` and not on `dev`. They break the publish-mirror gates
(`sidecars derived from data/`, `published mirror matches its source`, `the shipped
derivative still describes the master's building`) and cascade from there.

So the back-merge and the cleanup are one operation, and neither is safe alone: merge
without deleting and `dev` is red; delete on `dev` alone and the next promotion
re-imports them.

## Whose call the cleanup is

Deleting sixty files from `site/` on `main` is outside a steward run's lane
(`chicago/4d/` and `site/chicago/4d/` — and this is the second of those, but they are
files no 4D process authored and no 4D record names). **The owner should confirm the
sixty are junk before anything deletes them**, which is a one-look question: they are
byte-duplicates of files that already exist without the ` 2` suffix.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The owner has confirmed the sixty ` 2.json` / ` 2.glb` files are Finder duplicates.
- They are gone, and `main` and `dev` agree.
- `chicago/reference/newspapers/` is on `dev`.
- `./tools/check.sh` is green on `dev` after the merge, and
  `python3 tools/newspaper_corpus.py --check` reports the deposit **present** with
  every one of the 66 reference text paths resolved file by file — which is the
  strict half of that gate, and it has never yet run.
