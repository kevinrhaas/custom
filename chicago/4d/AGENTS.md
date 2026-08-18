# AGENTS.md — the contract for anyone working on 4D Chicago

Read this every session. It is one page on purpose.

## What this project is

A year-parameterized, walkable reconstruction of downtown Chicago. **It is a research
dataset with renderers attached** — not a game. The durable artifact is the georeferenced
land + structure data with per-attribute source provenance. Renderers are plural and
disposable. The first rendered scene is `1835` (target date 1835-07-01).

## Hard rules

1. **Never invent a source.** Every `source_id` must resolve in `data/sources/`. If evidence
   does not exist, mark the attribute `conjectural`. Fabricating a citation to make the
   validator pass is the worst thing you can do here.
2. **Never silently fill a gap.** Missing evidence is recorded as missing. `inferred` requires
   a `note` stating the reasoning. That is what the confidence model is for.
3. **Never drift past the scene date.** Most vivid published description of early Chicago is
   1837–1845 and describes a bigger town. `data/exclusions.json` records researched-and-excluded
   structures with citations — read it before adding anything, and add to it rather than
   deleting a finding.
4. **Every mesh is generated from `data/` by a command.** The one exception is
   `assets/authored/`, which is tagged `authored`, exempt from regeneration, and carries the
   same provenance requirements as generated geometry.
5. **Renderers consume glTF + JSON sidecars.** They never reach into `generators/` or
   reimplement the data model. Archetype parameters stay engine-neutral — the contract is
   glTF, not Blender.
6. **No asset without license provenance.** Every file under `assets/` has an entry in
   `assets/LICENSES.md`. A source whose `rights_status` is `check_required` may be cited in
   text but must not have assets derived from it.
7. **`tools/check.sh` passes before every commit.** It takes seconds and needs no Blender.

## Standing constraint — 1835 and Indigenous history

The final removal of the Potawatomi from Chicago occurred in **August 1835** — inside the
project's first target year. It is the most historically significant event of that year.

- **Do not improvise Native presence, representation, dialogue, or depiction.** This is not a
  research gap to be filled by inference; it is a subject requiring consultation.
- The Newberry's Indigenous Chicago curriculum is the starting point, and the project should
  seek review from Native scholars or community organizations before shipping any depiction.
- **Until then, v1 ships no human figures at all** — uniformly, not selectively. Build the
  built environment accurately and leave human depiction out of scope. An empty, accurate town
  is honest. A populated, invented one is not.
- `review_required: true` on any record blocks a scene from being marked `released`.

Note also that the great Potawatomi gathering and the last war dance are **August 1835**,
weeks after the 1835 scene date. Staging them in the 1835 scene would be wrong twice over.

## THE VISIBLE-PROGRESS RULE — read this before choosing a parcel

**Measured 2026-08-15, on the owner's report that the loop "just does organization and research
and not actually applying to the application": 15 of the last 30 changelog entries say nothing
you can see changed, and v124 to v137 is FOURTEEN CONSECUTIVE invisible runs.** That is not a
drift, it is a streak, and it is the loop optimising for what this project praises. The culture
here rewards measurement, refutation and honest gates — rightly — and the result is an agent that
would rather find a defect in an instrument than put a building in the town.

**So: a run must change something a visitor can SEE, and "see" means in the 3-D scene or on a
card a visitor opens.** A new gate is not visible. A corrected metric is not visible. A source
record is not visible. A refactor is not visible. All of those are real work and this project
needs them; they are not what a run is FOR.

**The three exemptions, and they are the only three.**

1. **An owner-reported bug.** Fixing what the owner reported always outranks this rule.
2. **The second half of a split whose first half was a measurement** — the R-BUG3c-a → R-BUG3c-b
   shape, where landing the measurement red before the fix is what stops the fix redefining
   success. The measurement half is exempt ONCE; the run after it must land the fix or say why.
3. **A gate that is BLOCKING a visible parcel** — not one that would be nice to have. Name the
   parcel it unblocks in the PR, or it is not this exemption.

**The cap: at most ONE invisible run in any four.** If the last three merged changelog entries
open with "Nothing you can see" — the phrase is the tell, so search for it — the next run MUST be
visible, and the exemptions above do not extend it. If everything at the top of the queue is
invisible, that is a fact about the queue and the run's job is to fix the queue: pull a visible
parcel up and say in the PR why it was buried.

**How to tell before you start.** Ask: when this merges, what will be different in a screenshot
taken from the same spot? If the honest answer is "nothing", you are on an invisible parcel and
you need one of the three exemptions, in writing, in the PR body.

**And do not make a run visible by writing the changelog as though it were.** The entry describes
what changed; if nothing in the scene changed, it says so. Gaming the phrase instead of the work
is worse than the streak.

## What's-New is for the visitor, not the reviewer — a length budget

**Measured 2026-08-15 on the owner's report that What's-New "has gotten excessively verbose". The
drift is monotonic across the whole history and nobody asked for it:**

| entries | items | words | title words |
|---|---|---|---|
| v60–79 | 5.0 | 443 | 11.9 |
| v80–99 | 7.5 | 642 | 16.2 |
| v100–119 | 7.3 | 724 | 21.4 |
| **v120–138** | **8.9** | **790** | **25.7** |

Words per entry up **78 %**, titles up **116 %**, the longest recent entry **984 words**. A
25-word title is not a title.

**It is the same pressure that produced the invisible-run streak.** This project rewards
thoroughness, so an entry that explains more of itself reads as better work. It is not. **What's-New
is read by a visitor who wants to know what changed in the town** — the reasoning, the refutations,
the measurements and the caveats belong in the PR body and `docs/STATUS.md`, which have no length
limit precisely so this one can.

**The budget, enforced by `tools/check-changelog.mjs` on entries from v139:** title **≤ 12 words**,
**≤ 6 items**, **≤ 450 words** total. Over budget warns; over 1.5× fails. The 138 entries already
written are history and are not retro-failed — the rule binds what is added next.

**Cut the entry rather than raising the number.** If a release genuinely needs more, it is usually
two entries or an entry plus a STATUS section, not one longer entry.
## RECONSTRUCTED IS A TIER, NOT A FAILURE — build, then declare

**The owner, 2026-08-15: the loop is "being hesitant and refusing to build because you are being
too cautious about being perfect. It's ok to create things that have some justification and they
can be inferred or even reconstructed based on your analysis."** He is right, and the example he
gave is the shape of it: the trees were not coloured as described because no source stated the
colour, so nothing was done at all.

**That is a misreading of this project's own vocabulary.** There are three tiers, and the third one
exists precisely for this:

- **attested** — a source states it. Cite the source.
- **inferred** — reasoned from evidence about *this particular thing*. Record the reasoning.
- **reconstructed** — **invented within bounds, because the scene needs it and nothing states it.**
  Record what bounded the invention and add a `docs/LIBERTIES.md` entry.

**`reconstructed` is a licence to build, not an admission of defeat.** Six hundred and sixty-five
roofs stand in this town on exactly that footing. A tree with no stated colour is not a reason to
leave the tree grey — it is a reconstructed colour, bounded by the species, the month and the
reference photographs already committed, recorded as a liberty, and BUILT.

**The rule.** When a parcel stalls for want of evidence, the first question is not "may I proceed?"
It is **"what is the lowest tier that honestly carries this, and what bounds it?"** Then build at
that tier and say so. Refusing to build leaves the scene wrong AND undocumented, which is strictly
worse than a declared reconstruction: an invented colour recorded as invented is honest, and a grey
tree nobody chose is not.

**"Blocked on the owner" is for four things only** — rights and licensing, the L1 constraint on
depicting people, spending real money, and a decision that changes what the project IS. **A missing
number is not one of them.** Derive a defensible figure, label it reconstructed, name what bounds
it, and write down what would replace it. There were **seven** parcels sitting on "blocked on the
owner" when this was written; most were missing numbers.

**What does NOT change, and this is the whole reason the tiers exist.** Never claim a source that
does not exist. Never promote a reconstruction to inferred or attested. Never leave an invention out
of `docs/LIBERTIES.md`. The bar was never "only build what is proven" — it is **"never misrepresent
what you built."** Those are different, and the second one is compatible with building a great deal
more than this loop has been building.

**The owner doubled down, 2026-08-18, verbatim: "in general i think you are being too cautious on
adding items to the scene. you are totally fine to be liberal with adding reconstructed items when i
ask for things, you can just label and mark them as such."** He said it while overriding, one by
one, the conservative readings the loop had settled into: only the two attested docks ("you can add
more docks!"), no boats ("you can add boats correct for the era! they would exist"), wagons only at
attested doors ("of course there would be more wagons all over the place in a frontier town"), signs
only where attested ("you need to add more signage … it is fine if they are reconstructions"). The
pattern to learn: **when the owner asks for something, the scene needing it IS the justification** —
build it at the reconstructed tier, label it, record the liberty, and do not ration it to the
attested instances. The rationing instinct is the bug this section exists to fix.

## THE QUEUE — how work is chosen (since 2026-08-17)

**`tickets/` is the single operational answer to "what next".** The owner asked for it
directly: his requests were getting lost inside an 11,000-line ROADMAP, and he could not
reorder priorities without editing prose. Read `tickets/README.md` — it is one page and it
is the contract. The short form:

- **Pick**: take the topmost ticket in `tickets/QUEUE.md` you can actually run (skip
  `needs_bake` on the improve runner, with the skip stated in the PR). `node
  tools/ticket.mjs list --workable` prints the same order.
- **Claim** in your first commit: `node tools/ticket.mjs claim T-NNNN`.
- **Close** in the merging PR: `node tools/ticket.mjs done T-NNNN --pr N`. Blocked instead?
  `block --owner "the question"` — the question goes in the ticket, where the owner will
  actually see it, not only in a PR body.
- **New work found mid-run** becomes a ticket at the QUEUE **bottom**: `ticket.mjs new
  "title" --by loop`. **Agents never reorder QUEUE.md — only the owner does.** That single
  rule is what makes his priorities durable across runs.
- **An owner ask becomes a ticket the moment it is made**, `--by owner`, before any work
  starts. This is not optional bookkeeping; an owner request going untracked for days is
  the exact failure this system exists to close.
- **Size in RUNS before you claim.** `XS` part of a run · `S` one run · `M` one run,
  tight (or one run plus a bake) · `L` **more than one run, and `claim` refuses it**.
  The test is the acceptance clause: *if it needs more than one demonstration, it is
  more than one ticket.* Split with `ticket.mjs split T-NNNN "piece" "piece"` — the
  children inherit the parent's exact place in QUEUE, so a split never re-prioritises.
  If a run discovers mid-flight that its ticket is bigger than one demonstration, it
  splits rather than shipping a self-invented "(1/2)".
- `tools/check.sh` runs `ticket.mjs check`: duplicate ids, queue drift, stale BOARD, a
  block with no stated question, an `L` in the queue — all merge-refusing.

**`docs/ROADMAP.md` is no longer the backlog.** It remains the *reasoning archive* — the
parcel boxes hold measurements, refutations and acceptance clauses that tickets link into,
and nothing there is deleted. Its NEXT UP table is tombstoned with a pointer here. STATUS.md
remains the honest narrative of what shipped; the *state* of work lives in tickets alone.

## The work-parcel contract

Work is parceled so parallel agents never collide. If you are a subagent:

- **One file per source, one file per structure, one file per zone.** Your parcel's outputs are
  disjoint from every other parcel's by construction. Do not restructure shared files.
- **Writing agents get their own git worktree.** A shared checkout across parallel agents has
  produced false alarms and lost work in this fleet before.
- Your parcel is done when `tools/check.sh` passes and your outputs carry their provenance.
- Do not run Blender unless your parcel changes geometry-affecting data. Bakes are batched.

## The two-speed build

| | `tools/check.sh` | `tools/bake.sh` |
|---|---|---|
| when | every commit, every sandbox | on demand + nightly |
| needs Blender | **no** | yes, pinned (`generators/blender.pin`) |
| runtime | seconds | minutes |
| does | schema, provenance, date gates, referential integrity, licenses, archetype params, staleness, JS parse, publish sync | generate → UV → bake AO/normals → GLB → web derivatives → sidecars → publish |

Agents consume committed GLBs. A stale committed GLB is a check failure, not a warning.

## How work ships

**Read `docs/PIPELINE.md` first.** Since 2026-08-14 this app runs a two-tier
**`dev` → `main`** pipeline on the owner's instruction: *overnight work must not ship
straight to production.* The fleet pilot is `kevinrhaas/jobtracker.polecat.live` →
`docs/PIPELINE.md`; ours is the two-tier form of it.

- **Branch `steward/<topic>` off `dev`. PR into `dev`. Merge when the dev gate is green.**
  Never push to `dev` or `main` directly. Ambiguous or unverified work stays an open PR
  with the `hold` label and a written explanation.
- **Merging into `dev` is STAGE, not ship.** It publishes only the integration preview at
  `/custom/chicago/4d/dev/walk/?year=1835` — noindex, banner-marked, `build.json` says
  `tier: dev`. Production is untouched.
- **Production moves ONLY when the owner dispatches `chicago-4d-promote-to-prod.yml`.**
  No schedule, no agent. `walk/` changes reach `main` by that dispatch and no other route.
  The hotfix exception stands: a production emergency PRs straight into `main`, and the
  next promotion's back-merge folds it into `dev`.
- **Scope is `chicago/4d/` and its published mirror `site/chicago/4d/`. Nothing else.**
  `kevinrhaas/custom` is a monorepo of unrelated personal projects — CAD, print models,
  the Joliet game, a landing site. A run that edits any of them is out of bounds, and the
  workflow files are outside scope too: changing one needs an interactive, owner-visible PR.
- **Both gates, in the foreground, before merging**: `tools/check.sh` (needs `jsonschema` +
  `pyproj`) and `node tools/smoke_renderer.mjs` (Playwright, 390×780 AND 1280×800, zero
  page errors). Mobile is a release gate. **Never weaken an assertion to pass.** The
  `--published` run is the one that matters: the source tree loads uncompressed masters and
  the site loads compressed derivatives, and bugs have shipped in the gap twice.
- **Run `tools/publish.sh` in the same commit** as any renderer, data or scene change.
  `site/chicago/4d/` is a generated mirror and `deploy.yml` only fires on `site/**`, so
  skipping it ships nothing while looking merged.
- **Changelog**: prepend one entry to `renderers/web/js/changelog.js` with all three
  authored fields blank — `v: null, ts: '', date: ''` — then run
  `node tools/stamp-changelog.mjs` and `node tools/check-changelog.mjs`. **Stamp BEFORE
  merging to `dev`; nothing stamps later in the pipeline.**
  - `date: ''` must be *present*: the stamper fills an empty `ts` but only *regenerates* a
    `date` that already exists, so an entry authored without the key fails the contract check.
  - `v: null` because the number is not yours to guess. Two branches that each compute
    "top + 1" both get it wrong, and the second to merge ships a duplicate — that cost three
    manual renumbers on 2026-08-10 alone. The stamper assigns it; `.gitattributes`
    (`merge=union`) keeps the merge itself conflict-free.
  - **Re-run `check-changelog.mjs` AFTER any merge that touches this file, not only before.**
    `merge=union` runs during the merge, so both parents can be green and the result broken —
    that is exactly how `main` shipped an unparseable changelog on 2026-08-13, killing the
    What's-new tab and this project's release feed to Manager and the launcher.
    `tools/check.sh` runs the contract check as a step, so a plain `./tools/check.sh` after
    merging covers it.
  - Nothing stamps after merge. The file is authored inside the app because the What's-new
    tab imports it; `publish.sh` mirrors it to `site/chicago/4d/js/changelog.js`, the URL
    Manager and the polecat.live launcher parse live, which must not move.
- **No Blender on the improve runner, and do not install one.** Geometry comes from the
  nightly `chicago-4d-bake.yml`, which branches off `dev` and **opens its PR into `dev`**.
  A unit that needs new geometry ships the data/archetype half and says so.
- **`docs/ROADMAP.md` is the backlog and `docs/STATUS.md` is the honest state** — update
  both in the same PR as the work. `docs/RENDERING.md` is the active rendering program;
  its phases are claimed the way ROADMAP parcels are.

## Honesty rules

- `docs/LIBERTIES.md` is append-only. Every compression and invention gets recorded. The
  standard: *a visitor should be able to tell you which parts we made up.*
- `docs/STATUS.md` states what is unverified. Do not describe a gate as passed if it was skipped.
- Where sources disagree, record the disagreement in `docs/RESEARCH/<id>.md` and pick the
  best-attested reading **with reasoning** — never silently choose.
- No model identifiers in repo artifacts.

## Orientation

`docs/PLAN.md` is the full development plan. `docs/research/` holds the source dossiers
(committed verbatim, tagged, with their own gaps stated). `docs/PROVENANCE.md` expands the
confidence model. `docs/EPOCHS.md` explains the temporal architecture.
