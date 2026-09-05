---
id: T-0805
title: Drain lap 1: the six PRs standing closest to dev, and the four ticket ids minted twice
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

The first drain lap under T-0804's tool. **Six PRs, each 2–33 commits behind `dev`,
6–17 conflicting files, all of them build products.** These land as ONE unit — #880
proved the shape ("landing them one at a time loses ground") and this lap is that
procedure run again, with each PR's own argument left in its own PR.

| order | PR | ticket | behind | files | note |
|---|---|---|---|---|---|
| 1 | [#892](https://github.com/kevinrhaas/custom/pull/892) | T-0412 `done` | 2 | 15 | a vendor's for-sale notice places nothing |
| 2 | [#894](https://github.com/kevinrhaas/custom/pull/894) | T-0451 `done`, owner | 5 | 30 | the North Division's six north-south streets |
| 3 | [#822](https://github.com/kevinrhaas/custom/pull/822) | T-0597 `claimed` | 2 | 27 | Hurlbut's half-brother note, both Kinzie cards |
| 4 | [#839](https://github.com/kevinrhaas/custom/pull/839) | the kin ticket | 45 | 24 | the `kin[]` block the owner ruled for |
| 5 | [#868](https://github.com/kevinrhaas/custom/pull/868) | T-0647 `done` | 21 | 17 | 33S7-9YYJ-5V's six two-stroke figures |
| 6 | [#858](https://github.com/kevinrhaas/custom/pull/858) | T-0536 `done` | 33 | 13 | the shared research gate reads `images[]` |

**#822 and #839 are one pair and must not be split across laps.** #822 writes Hurlbut's
1881 bracketed note onto `hh_kinzie_james` and `hh_kinzie_john_h`; #839 adds the `kin[]`
rows on those same two files, citing that note. #822 first, #839 immediately after.
#839 was parked on the kinship question, which **the owner ruled on 2026-09-05 —
`kin[]` on the household, per T-0808 § 2** — so it is now reviewed on its merits.

**Four ticket ids are minted twice and the lap must reconcile them**, because
`ticket.mjs check` refuses a duplicate id at the merge and whichever PR lands first makes
the other one illegal:

- **T-0783** — #892 files *"the 16 by 30 foot house at LaSalle and Lake"*, #894 files
  *"the committed Market line is fitted to N Wacker"*. Two different tickets, one number.
- **T-0787** — #822 files the kinship question, and **T-0787 is already TAKEN on `dev`**
  (the Wright 1834 sheet registration, landed in #895). #822's file must be restamped
  whatever else happens. T-0808 § 2's ruling is written into it as it moves.
- T-0784 and T-0785 on #894 are both `withdrawn` on the branch, fixed on dev by T-0780
  (#889) before they could be worked. They carry through as withdrawn records; they are
  not re-filed.

`ticket.mjs restamp <path>` is the remedy and **keeps the ticket's place in QUEUE.md** —
give it the PATH `check` prints, because with two files on one id the id alone cannot say
which one moves. Restamp the YOUNGER file each time, which is what #880 did for its seven.

**Order is least-behind first**, so each merge's regeneration is the input to the next
rather than a rerun of it — with the #822/#839 pair kept adjacent as above.

**Acceptance:** all six PRs merged into `dev` (squash, branches deleted), the id
collisions restamped with every queue place kept and nothing reordered, T-0808 § 2's
ruling written into the restamped kin ticket, `./tools/check.sh` exit 0 with `Queue OK`,
`check-changelog.mjs` green with every branch's entry present and stamped by
`stamp-changelog.mjs` (never hand-numbered), and no conflict marker anywhere under
`chicago/4d/` or `site/`. Every build product REGENERATED from its source, never
hand-reconciled — `ticket.mjs board`, `publish.sh`, `compile_scene --all`. The open-PR
count against `dev` is 10.
