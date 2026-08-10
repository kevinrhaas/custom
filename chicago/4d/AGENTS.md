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

This project runs on the Polecat fleet's continuous improvement loop —
`kevinrhaas/polecat-platform`, focus lane `custom`, hourly, one unit of work per run. The
steward's prompt is that repo's `.github/steward/improve.md`; its CUSTOM / CHICAGO 4D rule
is the authority and this section is the local restatement.

- **Scope is `chicago/4d/` and its published mirror `site/chicago/4d/`. Nothing else.**
  `kevinrhaas/custom` is a monorepo of unrelated personal projects — CAD, print models, the
  Joliet game, a landing site. A run that edits any of them is out of bounds.
- **Branch `steward/<topic>` off `main`, PR into `main`, merge your own PR when green.**
  Never push to main. Ambiguous or unverified work stays an open PR with the `hold` label
  and a written explanation.
- **Both gates, in the foreground, before merging**: `tools/check.sh` (needs
  `jsonschema` + `pyproj`) and `node tools/smoke_renderer.mjs` (Playwright, 390×780 AND
  1280×800, zero page errors). Mobile is a release gate. Never weaken an assertion to pass.
- **Run `tools/publish.sh` in the same commit** as any renderer, data or scene change.
  `site/chicago/4d/` is a generated mirror and the repo's `deploy.yml` only fires on
  `site/**`, so skipping it ships nothing while looking merged.
- **Changelog**: prepend one entry to `renderers/web/js/changelog.js` with all three
  authored fields blank — `v: null, ts: '', date: ''` — then run
  `node tools/stamp-changelog.mjs` and `node tools/check-changelog.mjs`.
  - `date: ''` must be *present*: the stamper fills an empty `ts` but only
    *regenerates* a `date` that already exists, so an entry authored without the key
    fails the contract check.
  - `v: null` because the number is not yours to guess. Two branches that each compute
    "top + 1" both get it wrong, and the second to merge ships a duplicate — that cost
    three manual renumbers on 2026-08-10 alone. The stamper assigns it after the merge;
    `.gitattributes` (`merge=union`) keeps the merge itself conflict-free.
  - Nothing stamps after merge. The file is authored inside the app because the
    What's-new tab imports it; `publish.sh` mirrors it to
    `site/chicago/4d/js/changelog.js`, the URL Manager and the polecat.live launcher
    parse live, which must not move.
- **No Blender on the improve runner, and do not install one.** Geometry comes from the
  nightly `chicago-4d-bake.yml`, which opens its own PR. A unit that needs new geometry
  ships the data/archetype half and says so.
- **`docs/ROADMAP.md` is the backlog and `docs/STATUS.md` is the honest state** — update
  both in the same PR as the work.

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
