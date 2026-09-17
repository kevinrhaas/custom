---
id: T-1155
title: The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-16
closed: 2026-09-17
pr: 1388
claimed_by: run 9/17/2026, 12:02:16 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-17T18:02:46.042Z
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35249185077
---

The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity.

**Found while closing T-1115, 2026-09-16.** `split_name_or_reason()` removes a
square-bracket group and everything inside it before tokenising. That is correct for a
parenthetical directory annotation and wrong for an internal supplied reading:
`E. K[in]zie` becomes `E. K zie`, `Esth[e]r M. Bailey` becomes `Esth r M. Bailey`, and
`T[e]mple, John T.` becomes surname `tmple`. T-1115 now prevents any such appearance
from minting a new card, but the bad split remains in the identity master, its gazetteer
ties and every later adjudication that consumes those identities.

**Cost measured on T-1115's tree audit:** square brackets occur throughout the research
corpus, including valid internal supplies, uncertain letters and whole later-directory
annotations. Correcting the splitter re-derives the large resident identity artefacts and
can rekey many identities; it must not be smuggled into the bounded mint-guard repair.

## A PRIOR RUN ALREADY WROTE THIS FIX, AND ITS PULL REQUEST WAS NEVER OPENED

**Recovered 2026-09-17.** Steward improve run [1/3]
([35181828835](https://github.com/kevinrhaas/polecat-platform/actions/runs/35181828835))
claimed this ticket at 04:29 UTC, committed the fix at 05:39 UTC as `70b5b5016` on
`steward/t-1155-bracket-supplies` (71 files, 2,501 insertions), merged `dev` into it at
06:40 UTC, and was **cancelled at 06:55 UTC before it opened a pull request**. No PR for that
branch exists, so `ticket.mjs landed` cannot see it and `ticket.mjs inflight` filed the branch
under *Cold*. The ticket therefore still read `open`, its claim lock went stale at three hours
and was stolen, and run [3/3] began rebuilding the same fix at 10:04 UTC.

**Do not re-decide the ruling below. It is that run's own commit message, verbatim, kept so the
next run inherits the reasoning rather than re-litigating which bracket shapes are supplies:**

> T-1155: keep the transcriber's supplied letters in a resident's name
>
> split_name_or_reason() deleted a square-bracket group and everything inside
> it before tokenising, which is right for a directory's parenthetical aside
> and wrong for an internal supply: E. K[in]zie became surname `zie`,
> Esth[e]r M. Bailey came apart into `esth` and `r`, T[e]mple, John T. became
> a `tmple`, and a leading [W]ade became an `ade`.
>
> `unmark()` now decides by where the bracket stands. Welded inside a word it
> is a supply and its letters are kept; standing free with whitespace either
> side it is the 1843/44 directories' own annotation and is still dropped. One
> free shape is kept too — a single supplied letter, [M]. B. Beaubien. `[?]`
> and `[uncertain: ...]` are still deleted wherever they stand, and so is every
> parenthesis.
>
> Re-derived: the identity master, source coverage, grading proposal, ladder
> coverage and spend, the civic mint and its regrade, the research synthesis,
> the town cards, the nine crosswalks and six research spends that key on
> resident cards, the Newberry parse, the scene sidecars, town census, register
> and the resident audit; site/chicago/4d republished.

**The branch is not worth merging and is not the recovery.** It is three commits ahead of `dev`
and six behind, and an in-memory merge conflicts on 31 files — every one of them a generated
artefact that the six merged neighbours re-derive (the identity master, the nine crosswalks, the
sidecars, `data/town_census.json`, `data/liberties.json`, the audit workbook), plus `QUEUE.md`
and `changelog.js`, which conflict by design. The substantive change is the `unmark()` rule in
`tools/consolidate_resident_evidence.py`; re-running the writers against current `dev` reproduces
the rest exactly. Take the ruling, re-derive, and delete
`steward/t-1155-bracket-supplies` when this closes.

**Both guards the owner asked for on finding this land with this ticket's note**, so it should
not recur: the steward's salvage step now opens a DRAFT pull request for any branch it rescues
that has none (kevinrhaas/polecat-platform, `.github/steward/salvage.sh`), and `ticket.mjs
inflight` now reads such a branch as **recoverable** rather than cold. Against `dev` that reading
found three, not one: this ticket, T-1154 and T-0761. A fourth was found by hand while writing
them — the commit carrying the owner's 2026-09-17 Native, Métis and Black reconstruction ruling
had been pushed to a branch whose PR had already merged, and was sitting unmerged with nothing
pointing at it. It rides in with this.

**Acceptance:** distinguish square-bracket transcription supplies from parentheses used
for directory annotations; preserve supplied letters inside a name while retaining the
original `as_read`; prove `E. K[in]zie`, `Esth[e]r M. Bailey` and `T[e]mple, John T.` split
to `kinzie`, `bailey` and `temple`; re-derive the identity master, proposal and coverage;
enumerate every changed identity id and either migrate or explicitly refuse every
downstream tie/card affected; and add mutation fixtures that fail if bracket contents are
discarded again. This is parked research under filing rule (d), not a prerequisite for
T-1115's mint refusal.
