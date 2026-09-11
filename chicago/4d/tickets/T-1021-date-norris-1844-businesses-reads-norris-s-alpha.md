---
id: T-1021
title: date_norris_1844_businesses reads Norris's alphabetising comma as a partner separator, so 'Jones, B. & Co' loses its initial and the continuity test refuses B. Jones on a surname alone
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-10
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

date_norris_1844_businesses reads Norris's alphabetising comma as a partner separator, so 'Jones, B. & Co' loses its initial and the continuity test refuses B. Jones on a surname alone.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

MEASURED ON THIS BRANCH BY T-1013'S RUN, so this ticket is the fix and not the survey.

`firm_names()` splits a printed firm style on `&`, on `and`, and on the comma Norris uses
between partners — `Jones, King & Co.` So it reads the ALPHABETISING comma the same way.
For the style `Jones, B. & Co` the parts are `Jones` / `B.` / `Co`; the part that is only an
initial has no surname in it, `if not longs: continue` drops it, and the initial `B` never
reaches `initials['jones']`.

T-1013 put 30 of these inverted styles into the dating pass for the first time, and the
cost is visible in `norris_1844_businesses_1835.json`:

    Jones, B. & Co   meets business_b_jones_grocery_and_provision_store
                     and business_b_jones_storage_and_forwarding
                     "One surname, and no initial printed on both sides agrees.
                      Refused — the eleven-Smiths rule."

The 1844 style prints B. and the 1835 businesses are B. Jones's. The refusal is the tool
saying it cannot see an initial it is holding.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- An initial-only part that FOLLOWS a surname part attaches to that surname, and one that
  follows nothing is still dropped — `Jones, B. & Co` is `{jones: {B}} + {co}`.
- `Jones, B. & Co` and `Johnson, J. & Co` are re-adjudicated against the 1835 businesses
  they meet, and the outcome is stated whichever way it goes: a one-surname firm still
  REQUIRES an initial agreement, so this makes the rule able to run, not certain to pass.
- No firm that matches today stops matching, and the continuity counts are stated
  before and after. `bash tools/check.sh` green. No bake.
