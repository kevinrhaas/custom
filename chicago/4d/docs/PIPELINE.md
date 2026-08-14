# PIPELINE — how 4D Chicago ships

**Two tiers: `dev` → `main`. Production moves only when the owner dispatches it.**

Adapted from the fleet pilot, `kevinrhaas/jobtracker.polecat.live` → `docs/PIPELINE.md`,
which is the canonical runbook and worth reading for the reasoning behind the shape. This
document records what is different here and why, so nobody has to diff two repos to find out.

Activated 2026-08-14 on the owner's instruction: *overnight work must not ship straight to
production.*

---

## The two tiers

| tier | branch | URL | who moves it |
|---|---|---|---|
| production | `main` | `/custom/chicago/4d/walk/?year=1835` | the owner, by dispatch |
| integration | `dev` | `/custom/chicago/4d/dev/walk/?year=1835` | any green PR into `dev` |

There is **no stage tier and no scheduled promotion**. The pilot has three tiers because it
promotes on a nightly cron; this app promotes on a human asking, so the middle tier would be
a queue with nobody in it.

**Merging into `dev` is stage, not ship.** It publishes the preview and nothing else.

---

## What each piece does

| file | job |
|---|---|
| `.github/workflows/chicago-4d-pipeline-setup.yml` | one-button: creates `dev` from `main` if absent, then dispatches a deploy. Idempotent. |
| `.github/workflows/deploy.yml` | the single deploy authority. Assembles ONE Pages artifact: `main` at the root, plus the `dev` branch's `site/chicago/4d/` folded in at `site/chicago/4d/dev/`. |
| `.github/chicago-4d-dev-preview.mjs` | assembles that preview — copy, `noindex`, banner, dev build stamp, `build.json`, robots disallow. |
| `.github/workflows/chicago-4d-check.yml` | **the dev gate.** Runs on PRs into `dev` and pushes to `dev` (no branch filter, deliberately). |
| `.github/workflows/chicago-4d-promote-to-prod.yml` | **dispatch-only.** Back-merges `main`→`dev`, then merges `dev`→`main` `--no-ff`, then dispatches the deploy. |
| `.github/workflows/chicago-4d-bake.yml` | the nightly content bake. Branches off `dev` and PRs **into `dev`**. |

---

## Five things that are easy to get wrong

**1. A Pages deploy job on a dev ref is REJECTED, silently.** The `github-pages` environment
carries a deployment-branch policy, so a `deploy` job running on `dev` fails in about a second
with no steps and no logs. It reads as "nothing ran" while the preview stays frozen at the last
main deploy. The fix, inherited verbatim from the pilot: a push to `dev` does not deploy
itself — the `refresh-previews` job re-dispatches `deploy.yml` **on main**, which rebuilds the
whole artifact from both refs.

**2. The preview needs no path rewriting, and that is a measured fact.** The pilot rewrites
every root-absolute `/x` URL because its app is served from the domain root. This app has
**zero** root-absolute URLs: `walk/index.html` uses `./css/…` and `./js/…`, and `scene-loader.js`
resolves data by page path (`walk/` → `../data/`). Mirroring the whole published
`site/chicago/4d/` tree under `dev/` therefore preserves every path by construction — which is
exactly why the whole tree is mirrored and not just `walk/`. If a root-absolute URL is ever
introduced, this stops being true and the preview script needs the pilot's rewriting.

**3. There is no service worker to neutralise.** The pilot replaces `sw.js` with a
self-unregistering stub so a preview never installs offline caching. This app has no service
worker, so there is nothing to stub and no cache to bump.

**4. Scope is `chicago/4d` alone.** `kevinrhaas/custom` is a monorepo of unrelated tenants —
CAD, print models, the Joliet game, a landing site. The dev tier covers the 4D app and nothing
else; every other tenant stays main-only. The artifact path stays `site`, so the ~2 GB of CAD
source can never enter it.

**5. Promotion is gated; deploy is not.** `deploy.yml` has no `needs: test` and must never get
one — a hard test gate on deploy once froze a fleet site for about 21 hours. The gate lives on
the *promotion*. The **hotfix exception** stands: a production emergency PRs straight into
`main`, and the next promotion's back-merge folds it into `dev` (which is why the promotion
back-merges main into dev *first* — otherwise it would silently revert the hotfix).

---

## The changelog, which the pipeline does not stamp for you

**Stamp before merging to `dev`. Nothing stamps later.** Prepend one entry to
`renderers/web/js/changelog.js` with all three authored fields blank — `v: null, ts: '',
date: ''` — then run `node tools/stamp-changelog.mjs`.

`date: ''` must be *present*: the stamper fills an empty `ts` but only *regenerates* a `date`
that already exists. `v: null` because the number is not yours to guess — two branches that
each compute "top + 1" both ship the same number.

**Re-run `node tools/check-changelog.mjs` AFTER any merge that touches this file, not only
before.** `.gitattributes` sets `merge=union`, which runs during the merge, so both parents can
be green and the result broken. That is exactly how `main` once shipped an unparseable
changelog and killed the What's-new tab and this project's release feed to Manager and the
launcher. The promotion workflow runs the contract check after both of its merges for this
reason.

---

## Running it

```bash
# once, to create the branch and light up the preview
gh workflow run chicago-4d-pipeline-setup.yml

# ordinary work
git switch dev && git pull
git switch -c steward/<topic>
#   … one coherent unit of work …
./tools/check.sh && node tools/smoke_renderer.mjs      # both, foreground
gh pr create --base dev
#   merge when the dev gate is green → /chicago/4d/dev/ updates

# production, owner only
gh workflow run chicago-4d-promote-to-prod.yml -f dry_run=true   # what would move
gh workflow run chicago-4d-promote-to-prod.yml                   # move it
```

---

## Proof of life

**2026-08-14** — this line was added on `dev` and nowhere else, as the pipeline's first
end-to-end proof: it must appear at `/custom/chicago/4d/dev/` while production at
`/custom/chicago/4d/walk/` is byte-for-byte unchanged. If you are reading it in a file that
also exists on `main`, the first promotion has since carried it across, which is the other
half of the proof.
