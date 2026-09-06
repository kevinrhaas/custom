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

PRS=$(gh pr list --repo "$REPO" --base "$BASE" --state open --limit 100 \
        --json number,headRefName,isDraft,labels \
        --jq '.[] | select(.isDraft==false)
                  | select([.labels[].name] | index("hold") | not)
                  | "\(.number)\t\(.headRefName)"')
[ -n "$ONLY" ] && PRS=$(echo "$PRS" | awk -v n="$ONLY" -F'\t' '$1==n')

PUSHED=0; SKIPPED=0; RED=0; NOOP=0
while IFS=$'\t' read -r N BR; do
  [ -n "${N:-}" ] || continue
  say "=== PR #$N  ($BR)"
  git fetch origin "$BR" -q 2>/dev/null || { say "  fetch failed"; SKIPPED=$((SKIPPED+1)); continue; }
  git checkout -B "lap/$N" "origin/$BR" -q 2>/dev/null || { say "  checkout failed"; SKIPPED=$((SKIPPED+1)); continue; }

  if [ "$(git rev-list --count "HEAD..origin/$BASE")" -eq 0 ]; then
    say "  already current — nothing to lap"; NOOP=$((NOOP+1)); continue
  fi

  git merge "origin/$BASE" --no-edit >/dev/null 2>&1
  U=$(git diff --name-only --diff-filter=U)
  if [ -n "$U" ]; then
    REAL=$(comm -23 <(echo "$U" | sort -u) <(echo "$GENERATED" | sed '/^$/d' | sort -u))
    if [ -n "$REAL" ]; then
      say "  REAL CONFLICT — left alone:"; echo "$REAL" | sed 's/^/    /'
      git merge --abort 2>/dev/null
      MARK="PR lap: this branch disagrees with \`$BASE\` about content"
      if ! gh pr view "$N" --repo "$REPO" --json comments --jq '.comments[].body' | grep -qF "$MARK"; then
        { printf '%s, not about bookkeeping, so the lap left it alone rather than pick a side.\n\n' "$MARK"
          printf 'Conflicting outside the generated set:\n\n```\n%s\n```\n\n' "$REAL"
          printf 'The generated files (BOARD.md, tickets.json, build.json, the mirrors, the smoke ledger)\n'
          printf 'are regenerated by the lap and never hand-merged. These are not those. This wants the\n'
          printf 'run that owns the ticket — or closing and re-cutting on a current `%s`.\n\n' "$BASE"
          printf -- '---\n_Generated by [Claude Code](https://claude.ai/code)_\n'
        } > /tmp/lap-comment.md
        gh pr comment "$N" --repo "$REPO" --body-file /tmp/lap-comment.md >/dev/null 2>&1 || true
      fi
      SKIPPED=$((SKIPPED+1)); continue
    fi
    say "  $(echo "$U" | grep -c .) generated conflict(s) — regenerating"
    git checkout --ours $U >/dev/null 2>&1; git add $U
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

  if git push origin "HEAD:$BR" >/dev/null 2>&1; then
    say "  pushed — gate will re-run and auto-merge can fire"; PUSHED=$((PUSHED+1))
  else
    say "  push rejected (branch moved under the lap?)"; SKIPPED=$((SKIPPED+1))
  fi
done <<< "$PRS"

say ""
say "PR lap: pushed=$PUSHED already-current=$NOOP left-alone=$SKIPPED red=$RED"
