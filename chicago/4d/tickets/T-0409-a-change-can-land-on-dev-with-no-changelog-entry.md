---
id: T-0409
title: A change can land on dev with no changelog entry, and one did today
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

AGENTS.md is unambiguous: *"prepend one entry to `renderers/web/js/changelog.js` … Stamp
BEFORE merging to `dev`; nothing stamps later in the pipeline."* Nothing enforces it.
`tools/check-changelog.mjs` checks the file's SHAPE — that it parses, that versions are
dense and descending, that timestamps are stamped and the two mirrors match — and it is
green on a file nobody touched. So a PR that changes the app and ships no entry is green
on every gate the pipeline has.

**It happened today.** PR #549 (T-0399) merged into `dev` at 2026-08-29, removed 21
business records from the compiled register, added a whole new identity structure, and
shipped no changelog entry. It was found only because a sibling slice had been building
the same ticket and read the file afterwards. The entry was written retroactively, by a
run that did not do the work — which is the wrong shape: whoever made the change is the
only one who knows what to say about it.

What makes this worse than a missed line of prose: `site/chicago/4d/js/changelog.js` is
the URL Manager and the polecat.live launcher parse live to build this project's release
feed. A change that ships no entry is invisible to both of them, and the What's-new tab
inside the walkthrough shows the town's last change as something older than it is.

**Options, cheapest first.**

1. **A gate that asks whether the top entry is new.** `check.sh` knows the diff against
   the merge base; if any file under `renderers/web/`, `data/` or `tools/` changed and
   `changelog.js` did not, fail with the contract quoted. Cheap and mechanical, and it
   costs a branch that genuinely changes nothing user-facing an explicit opt-out — which
   is a sentence somebody has to write, and that is the point.
2. **A CI-only check**, so a sandbox run is not blocked. Weaker: a bot-opened PR does not
   trigger the gate, which is exactly how #549 got through.
3. **Nothing, and rely on the prompt.** That is today's state, and today it failed.

The opt-out matters and should be part of whichever option is taken: a ticket that only
touches `tickets/` or `docs/` is a real case, and it is most of the queue's invisible band.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- A branch that changes the app under `renderers/web/` or `data/research/` and ships no
  new changelog entry fails a gate the steward actually runs, with the contract quoted.
- The opt-out exists, is explicit, and is recorded in the branch rather than in a habit.
- A self-test case per assertion, in the shape `check.sh` already uses.
- Reproduces the miss: the case is built from #549's own file list.
