---
id: T-0807
title: Drain lap 3: the site-budget cluster, the Thompson georeference, and the one PR whose conflict is a research claim
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

The third and last drain lap. Five PRs, and unlike laps 1 and 2 they are ordered by a
DEPENDENCY rather than by distance from dev.

**#836 goes first, and it is the one that unwedges the lane.** The published tree stood
at **31.999 MB of a 32 MB budget on dev alone**, so every open PR had stopped being
mergeable — `validate.py` refuses over budget and a changelog entry is a few KB. #836
found that `js/changelog.js` and `walk/js/changelog.js` were the **same 1.31 MB** under
two published URLs, made one a re-export, and took the tree to **30.69 MB**. That
headroom is what every later merge in this lap spends.

**The owner ruled on the budget, 2026-09-05 (T-0808 § 1): keep 32, land #836, rank T-0727
next.** The budget is NOT raised — 32 is this project's own number (GitHub's documented
Pages limit is 1 GB), and it stays because it is what found the duplicate. The run
landing #836 places **T-0727** — *budget the walkthrough's boot payload, which is what a
visitor actually downloads* — in QUEUE.md immediately after this drain band, under that
instruction. T-0728 (minify the mirror's JSON, a measured further 1.99 MB) is not ranked
here; it carries a question about what the mirror is for and waits behind T-0727.

| order | PR | ticket | behind | files | note |
|---|---|---|---|---|---|
| 1 | [#836](https://github.com/kevinrhaas/custom/pull/836) | T-0722 `claimed` | 45 | 22 | publish the changelog once; say where the 32 MB is |
| 2 | [#841](https://github.com/kevinrhaas/custom/pull/841) | T-0581 `claimed` | 45 | 24 | Moses and Kirkland vol. 1, forty-nine surnames |
| 3 | [#834](https://github.com/kevinrhaas/custom/pull/834) | T-0693 `done`, owner | 49 | 254 | date the trade-absence on 97 cards |
| 4 | [#886](https://github.com/kevinrhaas/custom/pull/886) | T-0685, owner | 12 | 15 | the Thompson plat georeferenced at the forks |
| 5 | [#876](https://github.com/kevinrhaas/custom/pull/876) | T-0601 `done` | 17 | 25 | the column sliver measured at nine |

**#886 was parked on the planform question and the owner ruled it: Wright 1834 stays the
planform of record, nothing moves (T-0808 § 3).** That is what the PR was waiting for and
it is mergeable as it stands — its own acceptance 5 was *nothing moves*, and nothing did:
it commits the GCPs and the Thompson bank trace **beside** the Wright planform, each with
its source, overwriting no waterline. **One correction rides with it**, and it is not
optional: `thompson_plat_1830.json` declares the two sheets agree to ±20 m, and this run
measured 27–60 m of disagreement on the North Branch. Wright being of record does not
make the other sheet agree with it. The file states the measured figure instead, citing
`docs/RESEARCH/thompson_forks_georeference.md`, in this same PR.

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
must not be forced — which is why it is last. #891 named it and stood down for the right
reason: it collides with #888 in `data/research/newberry_index/coverage.json`, where #876
rewrites the coverage note to account for T-0601's column slivers and #888 rewrites the
same declarations for volume 4's twelve-shard stitch. **Both are readings of what was
read.** Choosing between them is a research claim, so this lap must be run by an agent
that reads T-0601 and both declarations and RULES, with the ruling written into the
coverage note's own `why`. If it cannot be ruled on the evidence, #876 is blocked with the
question stated — never merged by picking a side.

**Acceptance:** #836, #841, #834, #886 and #876 merged into `dev` in that order (squash,
branches deleted), or #876 blocked with the coverage-note question stated in its ticket.
The published tree is measured under the 32 MB budget with the headroom recovered stated
as a number, and T-0727 carries a queue line. T-0722 exists once; T-0729's two tickets are
separated and #836's is withdrawn-or-fixed against today's green dev.
`thompson_plat_1830.json` carries the measured disagreement in place of its ±20 m claim.
`./tools/check.sh` exit 0 with `Queue OK`, `check-changelog.mjs` green, no conflict marker
under `chicago/4d/` or `site/`. **The open-PR count against `dev` is 0.**
