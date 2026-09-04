#!/usr/bin/env bash
# Register this repo's custom git merge drivers in the LOCAL clone.
#
# `.gitattributes` can say `merge=queue`, but it cannot say what `queue` runs —
# git deliberately keeps the command out of tracked content, because a merge
# driver is an executable a repository would otherwise be able to hand you. So
# every clone registers it once, and this is that step.
#
# Safe either way: with the driver unregistered git falls back to the ordinary
# text merge, which is the behaviour this repo had before the driver existed.
# `tools/check.sh` notices and advises; it does not fail, because a fresh clone
# that has not run this is not broken.
#
# Idempotent. Run it as often as you like.
set -euo pipefail
cd "$(dirname "$0")/../../.."          # repo root

git config merge.queue.name \
  'tickets/QUEUE.md — keep our order, take their closes and their new tickets'
git config merge.queue.driver \
  'node chicago/4d/tools/merge-queue.mjs %O %A %B %P'

git config merge.changelog.name \
  'changelog.js — our new entries, unstamped, on top of theirs'
git config merge.changelog.driver \
  'node chicago/4d/tools/merge-changelog.mjs %O %A %B %P'

echo "registered: merge.queue.driver     -> $(git config merge.queue.driver)"
echo "registered: merge.changelog.driver -> $(git config merge.changelog.driver)"
echo "  QUEUE.md:     $(git check-attr merge -- chicago/4d/tickets/QUEUE.md)"
echo "  changelog.js: $(git check-attr merge -- chicago/4d/renderers/web/js/changelog.js)"
echo
echo "NOTE: a changelog merge leaves our entries UNSTAMPED on purpose. After one, run:"
echo "  node chicago/4d/tools/stamp-changelog.mjs && node chicago/4d/tools/check-changelog.mjs"
