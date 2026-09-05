---
id: T-0807
title: Drain lap 3: the site-budget cluster, and the one PR whose conflict is a research claim
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

The third and hardest drain lap. Four PRs, and unlike laps 1 and 2 they are ordered by a
DEPENDENCY rather than by distance from dev.

**#836 goes first, and it is the one that unwedges the lane.** The published tree is at
the 32 MB Pages ceiling, and T-0730 records what that costs: *"every run in the lane now
fails check.sh on bookkeeping bytes."* #836 is T-0722's fix — it stops the mirror shipping
`changelog.js` **twice**, recovering ~1.35 MB of verbatim duplicate, and it prints where
the rest of the 32 MB goes. That headroom is what every later merge in this lap spends.

| order | PR | ticket | behind | files | note |
|---|---|---|---|---|---|
| 1 | [#836](https://github.com/kevinrhaas/custom/pull/836) | T-0722 `claimed` | 45 | 22 | publish the changelog once; say where the 32 MB is |
| 2 | [#841](https://github.com/kevinrhaas/custom/pull/841) | T-0581 `claimed` | 45 | 24 | Moses and Kirkland vol. 1, forty-nine surnames |
| 3 | [#834](https://github.com/kevinrhaas/custom/pull/834) | T-0693 `done`, owner | 49 | 254 | date the trade-absence on 97 cards |
| 4 | [#876](https://github.com/kevinrhaas/custom/pull/876) | T-0601 `done` | 17 | 25 | the column sliver measured at nine |

**Two more id collisions, both inside this lap** — restamp the younger file with
`ticket.mjs restamp <path>`, queue place kept:

- **T-0722** is filed by both #834 and #836, same filename, same subject. #836 is the one
  that WORKS it; #834 merely filed it. Reconcile to one file in the state #836 leaves it.
- **T-0729** is two different tickets on one number: #836's *"dev's gate is red on an
  untouched dev again"* and #841's *"Moses and Kirkland's History of Chicago volume 2"*.

**#836's T-0729 needs checking before it is carried in.** It records dev red on five
checks at `06a0a9ec`. **Dev is green now** — #863 and #889 (T-0780) cleared it, and the
`chicago-4d-check.yml` runs on `dev` have been `success` since `29cca6ff`. If the five
failures are gone, the ticket is `withdrawn` with the runs named, not carried as open work.

**#876 is the one PR in the whole backlog whose conflict is NOT a build product**, and it
must not be forced. #891 named it and stood down for the right reason: it collides with
#888 in `data/research/newberry_index/coverage.json`, where #876 rewrites the coverage
note to account for T-0601's column slivers and #888 rewrites the same declarations for
volume 4's twelve-shard stitch. **Both are readings of what was read.** Choosing between
them is a research claim, so this lap must be run by an agent that reads T-0601 and both
declarations and RULES, with the ruling written into the coverage note's own `why`. If it
cannot be ruled on the evidence, #876 is blocked with the question stated — never
merged by picking a side.

**Acceptance:** #836, #841, #834 and #876 merged into `dev` in that order (squash,
branches deleted), or #876 blocked with the coverage-note question stated in its ticket.
The published tree is measured under the 32 MB budget with the headroom recovered stated
as a number. T-0722 exists once; T-0729's two tickets are separated and #836's is
withdrawn-or-fixed against today's green dev. `./tools/check.sh` exit 0 with `Queue OK`,
`check-changelog.mjs` green, no conflict marker under `chicago/4d/` or `site/`. The
open-PR count against `dev` is 2 — #886 and #839, both waiting on T-0808.
