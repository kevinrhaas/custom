---
id: T-0814
title: Drain lap 1: the four PRs whose conflict is build products and nothing else
state: open
epic: META
requested_by: owner
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

**Re-cut 2026-09-05 17:10Z against the live backlog, because the first cut was overtaken
inside an hour.** The lap this ticket originally named (#892, #894, #822, #839, #868,
#858) is half merged: #892, #839, #876, #899 and #836 landed on `dev` on their own once
#836 took the published tree off the 32 MB wall. What follows is measured against `dev`
at `d6ffce99`, not against the plan.

**Three PRs whose ENTIRE conflict is build products, plus one that is nearly so.** Nothing
here needs a ruling; the whole lap is `ticket.mjs board` + `publish.sh` + a merge.

| order | PR | ticket | behind | conflicts | non-build conflicts |
|---|---|---|---|---|---|
| 1 | [#898](https://github.com/kevinrhaas/custom/pull/898) | T-0415 | **0** | **CLEAN** | — |
| 2 | [#894](https://github.com/kevinrhaas/custom/pull/894) | T-0451, owner | 6 | 7 | **none** |
| 3 | [#886](https://github.com/kevinrhaas/custom/pull/886) | T-0685, owner | 19 | 7 | **none** |
| 4 | [#901](https://github.com/kevinrhaas/custom/pull/901) | T-0509, owner | 4 | 6 | one `.xlsx` the audit tool regenerates |

**#898 merges with no lap at all** — zero commits behind, no conflict. It should go in
before anything else touches `dev`.

**#886 was parked on the planform question and the owner ruled it (T-0808 § 3): Wright
1834 stays, nothing moves.** That is what it was waiting for, and its own acceptance 5 was
*nothing moves* — it commits the Thompson GCPs and bank trace BESIDE the Wright planform,
overwriting no waterline. **One correction rides with it and is not optional:**
`thompson_plat_1830.json` declares the two sheets agree to ±20 m against **27–60 m
measured** on the North Branch. Wright being of record does not make the other sheet agree
with it; the file states the measured figure, citing
`docs/RESEARCH/thompson_forks_georeference.md`.

**#901 supersedes [#865](https://github.com/kevinrhaas/custom/pull/865)** — same ticket
T-0509, opened 17:02Z against #865's 09:58Z, and its own title says it is *"the reading the
32 MB wall held back"*. **Verify that before closing #865**, don't assume it: #865 carries
43 conflicts and ~36 non-build files against #901's 6 and one. If #901 really carries the
same reading, #865 closes with a comment naming it; if it does not, #865 is the one to land
and #901 is the duplicate. Closing the loser is part of this lap, not a follow-up.

**Acceptance:** #898, #894, #886 and #901 merged into `dev` in that order (squash);
`thompson_plat_1830.json` corrected in #886's own PR; #865 or #901 closed as the duplicate
with the comparison written into the comment. Every build product REGENERATED from its
source, never hand-reconciled. `./tools/check.sh` exit 0 with `Queue OK`,
`check-changelog.mjs` green, no conflict marker under `chicago/4d/` or `site/`. Open PRs
against `dev`: **8**.
