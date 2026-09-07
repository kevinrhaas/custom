---
id: T-0927
title: Close the superseded rivals: six open PRs whose work already landed under another number, read and closed with anything they hold salvaged first
state: open
epic: PIPELINE
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Six open PRs propose work that is already on `dev` under another number. Each is closed —
**after** it is read against `dev` and anything it holds that the winner does not is
salvaged into a ticket or a follow-up commit.

**The rule this band runs on: read before you close.** In the 2026-09-06 drain, six of six
parked rivals held something real — a man's record on the wrong Hubbard, three families, a
family nearly deleted as invented when a verified source states it, two tickets existing
nowhere, a self-test no landed tool had. Closing on the duplicate label alone would have
lost every one. Assume the loser holds something until you have looked.

| PR | why it is superseded | check before closing |
|---|---|---|
| #1013 | T-0744 landed as **#1014** | #1014 read the same leaf; does #1013 disagree on any line? |
| #1015 | T-0744, second reading, `hold` | it SELF-DECLARES disagreement on line count, pairs and footing — that is a finding, not a duplicate. See T-0930; do not close it silently |
| #1011 | T-0912's footing did not close; **#1012** closes it at 198 | #1011's four closing columns — are they identical in #1012? |
| #975 | self-declared duplicate of **#974** | whether #974 actually landed, and whether the reconciliation wording differs |
| #962 | self-declared duplicate of **#959** | #962 claims to machine-check five refusals #959 left as prose — if that is still true on `dev`, it is a gate nobody has, and belongs in a ticket |
| #968 | T-0771 landed as **#966** | already read: the rule DID land (`wholer`/`unbracketed`); its placement is refuted by the plat. `hold` — see T-0930 |

**Acceptance:**

1. Every PR above is closed, or a written reason says why it is not.
2. Each close carries a comment naming what was checked, what landed instead, and what was
   salvaged — or states plainly that nothing was, having looked.
3. Anything salvaged is a filed ticket or a commit on a branch that is going to land. A
   finding recorded only in a closing comment is a finding lost.
4. No PR here is closed on its title or its label alone.
