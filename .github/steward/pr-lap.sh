#!/usr/bin/env bash
#
# THE PR LAP. For every open PR into `dev` that is not a draft and not `hold`:
# merge `dev` in, regenerate what a tool owns, gate it, and push. It does NOT
# merge the PR — auto-merge does that once `gate` goes green on the new head.
#
# WHY THIS EXISTS (T-0857). GitHub's server-side merge NEVER runs a custom merge
# driver. `.gitattributes` can name `merge=generated`; only a clone that has run
# tools/setup-merge-drivers.sh can execute it, and GitHub has run nothing. So a
# branch that merges `dev` with ZERO conflicts here is reported as CONFLICTING by
# GitHub, auto-merge cannot fire, "Update branch" refuses, and the pile grows at
# exactly the rate the lane opens PRs. Measured 2026-09-06 on PR #940: clean
# locally, conflicted on GitHub, same commit.
#
# THE DRIVERS ARE REGISTERED FROM `dev`, NOT FROM THE BRANCH, and that is the
# other half. A merge driver that lives in the repo cannot resolve a merge on a
# branch cut BEFORE it: tools/merge-generated.mjs is simply absent from those
# trees. Copying dev's drivers aside and pointing git at the copies means a
# branch from before T-0831 gets the same clean merge as one from after it.
#
# It REFUSES rather than guesses. A conflict outside the generated set is a real
# disagreement about content — research claims, prose, tools — and picking a side
# is not a merge. Those PRs are left alone with one comment saying which files.
set -uo pipefail

REPO="${GITHUB_REPOSITORY:-kevinrhaas/custom}"
BASE="${LAP_BASE:-dev}"
ONLY="${LAP_ONLY:-}"
DRIVERS="$(mktemp -d)"
WORK="$(git rev-parse --show-toplevel)"

# THE IDENTITY THIS SCRIPT COMMITS UNDER, SET ONCE — and this one line is why the
# lap has never lapped anything. `git merge` writes a COMMIT, so it needs an
# author, and actions/checkout sets none: the runner has no user.name and its
# user.email is a machine hostname git will not accept. The identity was passed
# with `-c` on the `git commit` below and nowhere else, so every merge in every
# lap died with
#
#   fatal: empty ident name (for <runner@runnervm….internal.cloudapp.net>)
#       not allowed
#
# leaving no conflict, no commit and — until the exit status above started being
# read — no complaint. Measured on run 82, 2026-09-10 08:15: FOUR open PRs, four
# identical failures, and the old code would have reported `pushed=4`. It reported
# `left-alone=4` instead, which is how this was finally visible.
git config user.name  "polecat-steward"
git config user.email "steward@polecat.live"

# Files a TOOL owns. A conflict here is never resolved by hand: the merge takes
# either side to clear the marker and the tool then rewrites the file from source.
GENERATED='
chicago/4d/tickets/BOARD.md
chicago/4d/tickets/tickets.json
chicago/4d/tickets/QUEUE.md
chicago/4d/tools/dev-smoke-state.json
chicago/4d/renderers/web/js/changelog.js
site/chicago/4d/build.json
site/chicago/4d/tickets.json
site/chicago/4d/js/changelog.js
site/chicago/4d/walk/index.html
site/chicago/4d/walk/js/changelog.js
'

# ...AND THE THREE OF THOSE THAT ARE NO LONGER TRACKED AT ALL (T-0937).
#
# BOARD.md and both tickets.json came off the PR surface entirely: they are
# .gitignored now, because a run's first act is `ticket.mjs claim`, which rewrites
# all three before any work is done, and GitHub's merge runs no driver to reconcile
# them (T-0857). An untracked file cannot conflict, which is the point.
#
# But every branch cut BEFORE that landed still tracks them AND still modifies them,
# so merging the base into one is a modify/delete conflict on all three — for as long
# as those branches stay open. They must be resolved by REMOVING, not by
# `checkout --ours`: taking ours would put the file back in the index, and the lap's
# own `git add -A` would then carry it into the PR, re-tracking on the merge exactly
# the file the base just untracked. The regeneration below rebuilds all three as
# ignored files a moment later, so nothing is lost by deleting them here.
UNTRACKED_GENERATED='
chicago/4d/tickets/BOARD.md
chicago/4d/tickets/tickets.json
site/chicago/4d/tickets.json
'

say() { printf '%s\n' "$*"; }

# --- dev's drivers, registered by absolute path so any branch can use them
git fetch origin "$BASE" -q
for f in merge-queue.mjs merge-changelog.mjs merge-generated.mjs merge-smoke-state.mjs; do
  git show "origin/$BASE:chicago/4d/tools/$f" > "$DRIVERS/$f" 2>/dev/null || true
done
reg() { [ -s "$DRIVERS/$2" ] && git config "merge.$1.driver" "node $DRIVERS/$2 %O %A %B %P" && say "  driver $1 <- $BASE"; }
reg queue      merge-queue.mjs
reg changelog  merge-changelog.mjs
reg generated  merge-generated.mjs
reg smokestate merge-smoke-state.mjs

# ...AND THE ATTRIBUTES FROM `dev` TOO, WHICH IS THE HALF THAT IS EASY TO MISS.
# Registering a driver is not enough: git reads `merge=` out of the .gitattributes
# in the WORKING TREE, so a branch cut before T-0831 routes nothing to the driver
# however well it is registered. $GIT_DIR/info/attributes outranks the tree, so
# dev's rules are injected there and every branch is merged under them.
# MEASURED on PR #841 (cut before T-0831): drivers alone left 8 conflicts, five of
# them generated; drivers PLUS these attributes left 3, and all three are real.
git show "origin/$BASE:.gitattributes" \
  | grep -E 'merge=(queue|changelog|generated|smokestate)' \
  > "$(git rev-parse --git-dir)/info/attributes"
say "  attributes <- $BASE ($(wc -l < "$(git rev-parse --git-dir)/info/attributes") rules)"

# EVERY DRIVER THE ATTRIBUTES ROUTE TO HAS TO BE REGISTERED, and nothing checked.
# `reg` skips SILENTLY when dev's copy of a driver cannot be read — a renamed or
# moved tool, a path that drifted — while the attributes above still route files
# to it. The first merge then dies with `fatal: custom merge driver <name> lacks
# command line`: no conflict to find, no commit made, and before this script
# learned to read `git merge`'s exit status, no complaint either. Reproduced
# 2026-09-10 against PR #1049's branch. It is armed by absence, so absence is
# what this looks for, and it stops the whole lap rather than lapping nothing.
MISSING=
for D in $(grep -v '^[[:space:]]*#' "$(git rev-parse --git-dir)/info/attributes" \
             | grep -oE 'merge=[a-z]+' | sed 's/merge=//' | grep -v '^union$' | sort -u); do
  git config --get "merge.$D.driver" >/dev/null 2>&1 || MISSING="$MISSING $D"
done
if [ -n "$MISSING" ]; then
  echo "::error::.gitattributes routes files to unregistered merge driver(s):$MISSING"
  echo "::error::Every merge would die with 'lacks command line' and lap nothing."
  echo "::error::Check that $BASE still carries chicago/4d/tools/merge-*.mjs under those names."
  exit 1
fi

# REST, NOT `gh pr list`, AND THE REASON IS A RATE LIMIT THAT ONLY BITES HERE.
# `gh pr list` is a GRAPHQL call. GitHub budgets GraphQL separately from REST and
# far more tightly, and on 2026-09-14 the steward's own PAT spent its GraphQL
# allowance — the loop, the janitor and Manager all draw on it — while REST sat
# untouched:
#
#   gh pr list (GraphQL, STEWARD_PAT)  GraphQL: API rate limit already exceeded
#                                      for user ID 4193586
#   every REST call in the same minute  answered normally
#
# Two full laps were dispatched against a queue of nine lappable PRs, seven of
# them green and five with auto-merge armed and unable to fire, and both laps
# reported `pushed=0 ... red=0` and exited green having listed nothing.
#
# The same question over REST costs one request against a 15,000/hour budget and
# needs no GraphQL at all. The field names differ — REST spells them `draft` and
# `head.ref` where gh's GraphQL layer spells them `isDraft` and `headRefName` —
# and that is the whole of the change; the filter is the one it always was.
PRS=$(gh api --paginate \
        "repos/$REPO/pulls?state=open&base=$BASE&per_page=100" \
        --jq '.[] | select(.draft==false)
                  | select([.labels[].name] | index("hold") | not)
                  | "\(.number)\t\(.head.ref)"')
# THE STATUS OF THAT CALL, BECAUSE AN EMPTY ANSWER AND A FAILED ONE LOOK
# IDENTICAL FROM HERE. `PRS=$(cmd)` carries cmd's exit status, and this script
# runs `set -uo pipefail` WITHOUT `-e`, so a failure does not stop it: PRS is
# simply empty, the loop below runs zero times, and the lap prints
#
#   PR lap: pushed=0 already-current=0 left-alone=0 red=0
#
# which is EXACTLY what a healthy lap with nothing to do prints. It then exits 0
# and the workflow goes green.
#
# Measured 2026-09-14 on run 301, dispatched with LAP_ONLY=1257 to lap a PR that
# was 39 commits behind dev:
#
#   GraphQL: API rate limit already exceeded for user ID 4193586.
#   PR lap: pushed=0 already-current=0 left-alone=0 red=0
#
# The run was GREEN. Nothing was lapped, nothing said so, and the only trace was
# one line of gh's stderr in the middle of a successful log. Every lap inside
# that rate-limit window reported clean while sweeping nothing — which is what a
# stuck PR queue looks like from the outside when the workflow list looks
# healthy.
#
# This is the same shape as the steward janitor's `set -e` abort (polecat-platform
# #165): a failure wearing the costume of a clean run. The janitor at least went
# RED. This went green, which is worse.
#
# So the lap now refuses to be quietly useless. If it cannot ASK, it fails, loudly
# — the lap's whole job is the list, and a lap that cannot see its PRs has not
# done that job. (If `set -e` is ever added to this script, this capture needs a
# `set +e` around it or it becomes unreachable — which is precisely the bug #165
# was.)
LIST_RC=$?
if [ "$LIST_RC" -ne 0 ]; then
  echo "::error::the PR-list call failed (exit $LIST_RC) — the lap cannot see the pull requests it exists to lap."
  echo "::error::A rate limit or an auth failure here is indistinguishable from an empty queue:"
  echo "::error::both leave the list empty, and the lap would print 'pushed=0 ... red=0' and exit 0."
  echo "::error::Failing instead, so a lap that swept nothing is never reported as a lap that found nothing."
  exit 1
fi

if [ -n "$ONLY" ]; then
  # A DISPATCH THAT NAMES A PR AND MATCHES NOTHING IS ALSO NOT "no work". The
  # operator asked for something specific; silence is the wrong answer whether the
  # number is wrong, the PR is closed, or — the case that cost an hour on
  # 2026-09-14 — it carries `hold`, which the filter above removes BEFORE this
  # line ever sees it.
  MATCHED=$(echo "$PRS" | awk -v n="$ONLY" -F'\t' '$1==n')
  if [ -z "$MATCHED" ]; then
    echo "::error::LAP_ONLY=$ONLY matched no lappable pull request into $BASE."
    echo "::error::The list above holds $(echo "$PRS" | grep -c . || true) PR(s). A PR is absent from it when it is"
    echo "::error::closed, a draft, labelled 'hold', or targets another base — the 'hold' filter runs"
    echo "::error::BEFORE this one, so a held PR can never be reached by naming it here. Remove the"
    echo "::error::label first if that is what you meant."
    exit 1
  fi
  PRS="$MATCHED"
fi

PUSHED=0; SKIPPED=0; RED=0; NOOP=0
while IFS=$'\t' read -r N BR; do
  [ -n "${N:-}" ] || continue
  say "=== PR #$N  ($BR)"
  git fetch origin "$BR" -q 2>/dev/null || { say "  fetch failed"; SKIPPED=$((SKIPPED+1)); continue; }
  git checkout -B "lap/$N" "origin/$BR" -q 2>/dev/null || { say "  checkout failed"; SKIPPED=$((SKIPPED+1)); continue; }

  if [ "$(git rev-list --count "HEAD..origin/$BASE")" -eq 0 ]; then
    say "  already current — nothing to lap"; NOOP=$((NOOP+1)); continue
  fi

  BEFORE=$(git rev-parse HEAD)
  git merge "origin/$BASE" --no-edit >/tmp/lap-merge.log 2>&1
  MERGED=$?
  U=$(git diff --name-only --diff-filter=U)

  # A MERGE CAN FAIL WITHOUT LEAVING A CONFLICT, and this used to read as success.
  # The exit status was discarded and only `--diff-filter=U` was consulted, so a
  # merge that died before it began — `fatal: custom merge driver queue lacks
  # command line` is the one that bit, when .gitattributes routes a file to a
  # driver this shell did not register — left no conflicts, and the lap sailed on
  # to gate an UNMERGED tree (green, of course: it is the branch as it already
  # was), push nothing, and report "pushed — auto-merge can fire". Measured
  # 2026-09-10: PRs #1049 and #1051 were both reported pushed by run 79 and
  # neither branch moved; #1049 sat at the same head for over two hours while the
  # lane looked healthy. A lap that cannot tell you it did nothing is worse than
  # no lap, because the pile it leaves looks like somebody else's problem.
  if [ "$MERGED" -ne 0 ] && [ -z "$U" ]; then
    say "  MERGE FAILED with no conflict to resolve — this is a broken merge, not a disagreement:"
    tail -5 /tmp/lap-merge.log | sed 's/^/    /'
    git merge --abort 2>/dev/null
    SKIPPED=$((SKIPPED+1)); continue
  fi
  if [ -n "$U" ]; then
    REAL=$(comm -23 <(echo "$U" | sort -u) <(echo "$GENERATED" | sed '/^$/d' | sort -u))

    # ...AND THE DERIVED RESEARCH LAYER, WHICH IS THE SAME KIND OF THING AS THE
    # GENERATED FIVE and was left out only because nobody had enumerated it.
    # Measured 2026-09-10, on the first laps that could merge at all (#1058):
    # every one of the three surviving PRs was left alone for a REAL CONFLICT,
    # and every conflicting file was a tool output two runs had each re-derived —
    # seven directory crosswalks on #1051, the land-sale crosswalk and spend and
    # identity_master on #1055, the scene sidecar and the audit workbook on
    # #1053. Not one was a disagreement about the town.
    #
    # `rederive.mjs --resolvable` answers from tools/derived_manifest.json, which
    # ENUMERATES rather than pattern-matches, so what is in scope can be read.
    # It refuses the set as a whole if any member is unlisted or declares
    # hand_authored — half a merge is not a merge. check.sh still runs after
    # this and is what PROVES the rebuild; a wrong manifest entry makes the gate
    # red and the branch is not pushed, so the worst case is the PR staying open.
    if [ -n "$REAL" ] && [ -f chicago/4d/tools/rederive.mjs ] \
       && node chicago/4d/tools/rederive.mjs --resolvable $REAL >/tmp/lap-rederive.log 2>&1; then
      say "  $(echo "$REAL" | grep -c .) conflict(s) in the derived research layer — rebuilding from source"
      git checkout --ours $REAL >/dev/null 2>&1; git add $REAL
      if ! ( cd chicago/4d && node tools/rederive.mjs --run ) >>/tmp/lap-rederive.log 2>&1; then
        say "  the rebuild itself failed — left alone:"; tail -6 /tmp/lap-rederive.log | sed 's/^/    /'
        git merge --abort 2>/dev/null; SKIPPED=$((SKIPPED+1)); continue
      fi
      REAL=
    fi

    if [ -n "$REAL" ]; then
      say "  REAL CONFLICT — left alone:"; echo "$REAL" | sed 's/^/    /'
      [ -s /tmp/lap-rederive.log ] && sed 's/^/      /' /tmp/lap-rederive.log | head -8
      git merge --abort 2>/dev/null
      MARK="PR lap: this branch disagrees with \`$BASE\` about content"
      # REST for both halves of this, for the reason the list above moved: `gh pr
      # view` and `gh pr comment` are GRAPHQL, and the steward PAT's GraphQL
      # budget is the one that runs out. Measured on lap 307, the first lap able
      # to list anything all day — every REAL CONFLICT it found was followed by
      #
      #     GraphQL: API rate limit already exceeded for user ID 4193586.
      #
      # so five PRs were correctly refused and NOT ONE of them was told why. From
      # GitHub they read as stuck pull requests with no explanation, which is the
      # exact failure this whole comment exists to prevent.
      if ! gh api --paginate "repos/$REPO/issues/$N/comments" --jq '.[].body' 2>/dev/null | grep -qF "$MARK"; then
        { printf '%s, not about bookkeeping, so the lap left it alone rather than pick a side.\n\n' "$MARK"
          printf 'Conflicting outside the generated set:\n\n```\n%s\n```\n\n' "$REAL"
          printf 'The generated files (build.json, the mirrors, the smoke ledger — and BOARD.md and\n'
          printf 'tickets.json, which are not even tracked any more) are regenerated by the lap and\n'
          printf 'never hand-merged. These are not those. This wants the\n'
          printf 'run that owns the ticket — or closing and re-cutting on a current `%s`.\n\n' "$BASE"
          printf -- '---\n_Generated by [Claude Code](https://claude.ai/code)_\n'
        } > /tmp/lap-comment.md
        # `jq -Rs` wraps the file as a JSON string so the body reaches the API
        # intact — it carries backticks, a fenced block and the conflicting paths,
        # and none of that survives being interpolated into a shell argument.
        if jq -Rs '{body: .}' < /tmp/lap-comment.md \
             | gh api -X POST "repos/$REPO/issues/$N/comments" --input - >/dev/null 2>/tmp/lap-comment.err; then
          say "  said so on the PR"
        else
          # NOT silent, even though it is best-effort. A conflict the lap refused
          # and could not explain is the worst of both: the PR does not move and
          # nobody is told why.
          say "  could not comment on #$N — $(tail -1 /tmp/lap-comment.err 2>/dev/null | cut -c1-120)"
          say "  the conflict above stands; it is in this log and not on the PR"
        fi
      fi
      SKIPPED=$((SKIPPED+1)); continue
    fi
    say "  $(echo "$U" | grep -c .) generated conflict(s) — regenerating"
    # Split the generated conflicts: the ones the base still tracks are resolved by
    # taking ours and letting the tools rewrite them; the ones the base has
    # UNTRACKED are resolved by removing them (see UNTRACKED_GENERATED above).
    DROP=$(comm -12 <(echo "$U" | sort -u) <(echo "$UNTRACKED_GENERATED" | sed '/^$/d' | sort -u))
    KEEP=$(comm -23 <(echo "$U" | sort -u) <(echo "$UNTRACKED_GENERATED" | sed '/^$/d' | sort -u))
    if [ -n "$DROP" ]; then
      say "  $(echo "$DROP" | grep -c .) of them are untracked on $BASE — removing, not keeping (T-0937)"
      git rm -q -f --ignore-unmatch $DROP >/dev/null 2>&1
    fi
    if [ -n "$KEEP" ]; then
      git checkout --ours $KEEP >/dev/null 2>&1; git add $KEEP
    fi
  fi

  # TWO BRANCHES MINTED THE SAME TICKET ID — bookkeeping, so the lap heals it.
  # `ticket.mjs nextIdNum` scans every origin ref before it mints, so this is not
  # a missing guard but the window between minting an id and pushing the branch
  # that carries it; no scan can close it. Measured 2026-09-10: PRs #1048 and
  # #1049 each filed T-0988 ten minutes apart. The merge is CLEAN — git has no
  # opinion about two files with the same front-matter id — and then check.sh
  # fails on the duplicate AND on the survivor's queue line, which merge-queue.mjs
  # ate because it reconciles QUEUE.md by id. Neither branch is wrong about
  # anything. Same line this script already draws for the files a tool owns: a
  # number nobody chose on purpose is not a disagreement about the town.
  # It REFUSES rather than guess when it cannot tell which side is the branch's,
  # and a refusal is a non-zero exit that stops this PR here.
  if [ -f chicago/4d/tools/resolve_id_collisions.mjs ]; then
    if ! ( cd chicago/4d && node tools/resolve_id_collisions.mjs --base "origin/$BASE" ) \
         >/tmp/lap-ids.log 2>&1; then
      say "  TICKET ID COLLISION it would not resolve — left alone:"
      tail -6 /tmp/lap-ids.log | sed 's/^/    /'
      git merge --abort 2>/dev/null; SKIPPED=$((SKIPPED+1)); continue
    fi
    grep -E '^ticket ids: T-' /tmp/lap-ids.log | sed 's/^/  /' || true
  fi

  ( cd chicago/4d \
    && node tools/stamp-changelog.mjs \
    && node tools/ticket.mjs board \
    && python3 tools/compile_scene.py --all \
    && ./tools/publish.sh ) >/tmp/lap-regen.log 2>&1 || {
      say "  regeneration failed — see log"; tail -5 /tmp/lap-regen.log | sed 's/^/    /'
      git merge --abort 2>/dev/null; SKIPPED=$((SKIPPED+1)); continue; }

  git add -A
  git -c user.name="polecat-steward" -c user.email="steward@polecat.live" \
      commit -q --no-edit -m "Lap onto $BASE: generated files regenerated, not merged

The five files a tool owns conflict on every merge and are never hand-merged —
ticket.mjs board, publish.sh and compile_scene rewrite them from source. Nothing
in this branch's own diff was touched.

Merge drivers registered from $BASE rather than from this branch, so a branch cut
before T-0831 resolves the same way one cut after it does (T-0857)." 2>/dev/null

  if ! ( cd chicago/4d && ./tools/check.sh ) >/tmp/lap-gate.log 2>&1; then
    say "  GATE RED after the lap — not pushed"; tail -6 /tmp/lap-gate.log | sed 's/^/    /'
    RED=$((RED+1)); continue
  fi

  # SAY WHAT ACTUALLY HAPPENED. `git push` to a ref that is already at HEAD is
  # "Everything up-to-date" and exits 0, so the old form printed "pushed — gate
  # will re-run and auto-merge can fire" for a push that moved nothing and a gate
  # that will not re-run. That sentence is the one a person reads to decide the
  # lane is healthy, so it has to be earned: compare HEAD against the head this
  # PR started the lap on, and only claim a push when the branch really moved.
  if [ "$(git rev-parse HEAD)" = "$BEFORE" ]; then
    say "  the lap produced no new commit — nothing to push, and this PR is unchanged"
    NOOP=$((NOOP+1))
  elif git push origin "HEAD:$BR" >/dev/null 2>&1; then
    say "  pushed $(git rev-parse --short "$BEFORE") → $(git rev-parse --short HEAD)"
    say "  — gate will re-run and auto-merge can fire"; PUSHED=$((PUSHED+1))
  else
    say "  push rejected (branch moved under the lap?)"; SKIPPED=$((SKIPPED+1))
  fi
done <<< "$PRS"

say ""

# --- claim markers nobody released ------------------------------------------
# A claim is a branch, `claim/t-NNNN`, and NOTHING ELSE COLLECTS THEM. The
# steward janitor sweeps open PULL REQUESTS and a marker has none; the 3h
# staleness rule only lets the NEXT claim on that same ticket steal it, which
# never comes once the ticket is closed and out of the queue.
#
# So they accumulated. Measured 2026-09-14: nineteen markers on the remote, the
# oldest three days old, and seventeen of the nineteen belonging to tickets that
# were no longer open. The largest single cause was `ticket.mjs split` never
# releasing — fixed in the tool — but a run that DIES mid-work leaves one too,
# and no fix in the tool can help there because the run is gone.
#
# The lap is the right broom: it already runs on every push to dev, it already
# holds the credentials, and `claims --sweep` deletes only markers older than
# RUN_HOURS — which the claim path itself already treats as dead and steals.
# Best-effort, and never the lap's exit status: a marker is litter, not a block.
# $WORK, not a relative path: the loop above walks in and out of checkouts, so
# the only directory this script can name with confidence is the one it resolved
# at the top.
if [ -f "$WORK/chicago/4d/tools/ticket.mjs" ]; then
  say "claim markers:"
  ( cd "$WORK/chicago/4d" && node tools/ticket.mjs claims --sweep 2>&1 ) \
    | tail -n 60 | while IFS= read -r line; do say "  $line"; done
else
  say "claim markers: tools/ticket.mjs is not in this checkout — not swept"
fi

say ""
say "PR lap: pushed=$PUSHED already-current=$NOOP left-alone=$SKIPPED red=$RED"
