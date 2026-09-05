---
id: T-0771
title: dev's gate is red: 160 Newberry leads went unruled when T-0600 struck 443 cards, and neither derived file was re-derived
state: claimed
epic: META
requested_by: loop
seen: false
effort: XS
legacy_id: null
parent: null
opened: 2026-09-05
closed: null
pr: null
claimed_by: run 9/5/2026, 6:50:28 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/33963513683
---

**dev's gate is red, and no branch is cut yet.** `./tools/check.sh` on a clean worktree of
`origin/dev` at `326d2f6`/`077b34711` exits 1 on one step —
*every Newberry lead is ruled on, anchored, and re-derives from the cards* — with 57 problems:

```
lead_crosswalk.json does not re-derive from leads.json and the committed cards
160 lead(s) offered and not ruled on: lead_v01_abbott_census_1840, …
lead_crosswalk.json refusals nbi_v01_2461: anchored to a card that is not in the records   (× 54)
acquisition_list.json does not re-derive from the committed cards
```

**The cause is #873 (T-0600),** which struck 443 stanzas that named a place and no work.
Those stanzas were cards, and two generated files stand on the card set: `lead_crosswalk.json`
anchors each ruling to a card, and `acquisition_list.json` is the list of works to fetch. Neither
was re-derived in that commit, so 54 refusals now point at cards that no longer exist and the 160
leads the surviving cards newly offer are unruled.

**Both files are `generated_by: tools/rule_newberry_leads.py --write`** and the gate's whole
assertion is that they re-derive. So the repair is to re-derive them, and nothing else.

**Measured, `origin/dev` → this branch:**

| | dev | here |
|---|---:|---:|
| leads ruled | 788 | **907** (+160 newly offered, −41 whose card was struck) |
| cards ruled | 1,294 | 1,327 |
| candidate / refused | 190 / 598 | 229 / 678 |
| acquisition list | 375 cards | **324** (the 51 struck; the 81 carrying a year unchanged) |
| **merges** | **0** | **0** |

Ten leads present on both sides change class and three of those change outcome
(`colman_residents` and `mann_census_1840` refused → candidate, `lang_census_1840` the other
way). That is the ladder working as written rather than drift: the first rung a lead fails
decides it, T-0600 removed the wrecked place-only cards that were failing rung 1
(`ocr_variant_only`), and the leads that stood on them now fall through to the rung that
actually describes them. **`matched` stays 0 and `discriminators_found` stays 0** — a card
heads a surname over a citation and can never reach a merge, and this change does not touch
that.

**Scope, deliberately narrow.** This re-derives the two files the gate names and nothing more.
It is NOT **T-0740**, which is the larger, still-open drift: `read_newberry_index.py --parse`
rewrites `leads.json` by 6,039 lines because the layers underneath it grew, and it asks for a
gate that catches the next drift before a run trips over it. T-0740 stays open and unchanged;
this ticket only gets `dev` back to green so the twenty PRs held behind it can be judged on
their own work.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- `python3 tools/rule_newberry_leads.py --check` exits 0, and `./tools/check.sh` exits 0 with
  zero failing steps on this branch — measured against the same command on clean `origin/dev`,
  which fails this one step.
- `merges` and `discriminators_found` are still 0; the count change is stated in the PR with
  the leads added, removed and re-ruled.
- No file outside `data/research/newberry_index/` changes except the changelog, the ticket
  bookkeeping and the publish mirror.

**Links:** T-0590 (the rulings) · T-0600 (the card removal that caused this) · T-0740 (the
wider parse drift, untouched) · T-0763 (why a `FAIL` line in `check.sh` is not always a failure)
