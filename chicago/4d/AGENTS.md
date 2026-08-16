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
