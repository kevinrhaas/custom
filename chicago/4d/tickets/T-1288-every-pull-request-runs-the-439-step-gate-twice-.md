---
id: T-1288
title: Every pull request runs the 439-step gate TWICE, because the check fires on push and on pull_request for the same commit
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-09-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

`.github/workflows/chicago-4d-check.yml` fires on **both** `push` and `pull_request`:

```yaml
on:
  push:
    paths: ['chicago/4d/**', '.github/workflows/chicago-4d-check.yml']
  pull_request:
    paths: ['chicago/4d/**']
```

A steward branch with an open pull request satisfies both. So every push to such a branch
starts the 439-step suite TWICE on the same commit, and the two runs are identical.

Observed on 2026-09-17 on every open pull request in the queue at once — #1411, #1410, #1409,
#1407, #1405 and #1392 each showed two `gate` check runs on the same head sha. One gate is
roughly ten minutes. The lap pushes to every open PR on every merge into `dev`, so the waste
is not once per PR: it is once per PR **per lap**, and there were four laps in the hour this
was found.

**This matters because CI time is what makes the queue slow to converge.** Every merge into
`dev` dirties every other pull request, each needs a lap, and each lapped head needs a gate
before it can be called clean. Paying twice for that doubles the wall-clock of the whole
drain.

**The fix is one line**, and it is the standard shape:

```yaml
on:
  push:
    branches: [dev, main]
    paths: [...]
  pull_request:
    paths: [...]
```

A branch push is then gated through the pull-request event only, and `dev` and `main` keep
their own push gate. **Check the other workflows for the same shape before assuming this one
is alone** — and check that nothing downstream keys off the push-event check run by name,
because `merge-ready` merges on GitHub's `clean`, which is computed from the REQUIRED checks
and would change if a required check stops being produced on push.

**Acceptance:** one pushed commit on a branch with an open pull request produces exactly ONE
`gate` check run; `dev` still gates on its own pushes; `merge-ready` still reports `clean` for
a green PR afterwards, verified on a real PR rather than reasoned about.
