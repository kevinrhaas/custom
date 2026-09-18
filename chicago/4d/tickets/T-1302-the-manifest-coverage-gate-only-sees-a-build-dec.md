---
id: T-1302
title: The manifest coverage gate only sees a --build declared one way, so 55 gated writers still slip past it
state: open
epic: META
requested_by: owner
seen: false
effort: M
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

`tools/audit_manifest_coverage.mjs` refuses a gated writer the derived manifest has never
heard of. It works, and it found four on the day it shipped. **It also has a false negative,
and a gate with one is worse than no gate, because it is believed.**

Its write-mode pattern was anchored to the start of a line:

    /(?:^|\n)\s*(?:if\s+)?["']--(?:build|write)["']/

That matches a tool which reads argv directly — `if "--build" in argv:` — and MISSES one
that declares the same mode through argparse — `parser.add_argument("--build", ...)`. Both
styles are used in this repository.

**It cost two red runs on #1422.** `export_borderline_roster.py` declares `--build` through
argparse, landed on dev after the audit was written, and the audit reported OK while the lap
could not rebuild the roster. That one is now listed (measured first: a rebuild on clean dev
changed no committed byte). This ticket is the rest.

**Widening the pattern to `/["'`]--(?:build|write)["'`]/` reports 55 tools.** That number is
the finding, and it is why this is a ticket rather than a same-night fix: fifty-five is far
too many to list unmeasured, and `_must_reproduce` is not a formality — a tool can pass
`--check` and still not rebuild to itself, which is what `crosswalk_census_1840_heads.py`
already demonstrates at 137 rewritten lines.

**Acceptance:** widen the pattern, then triage all 55 BY MEASUREMENT, in batches, and state
the split. For each: run its build on a clean `dev` and record whether it changed a committed
byte. It reproduces, so it goes in the manifest with what it writes. It does not, so it goes
in `NOT_DERIVABLE` with the measurement that says why. **No tool is listed on the strength of
its `--check` passing**, and none is exempted without a number beside it. The gate must be
green at the end with the widened pattern in place, and the count of listed versus exempted
is the deliverable.

**Do not weaken the gate to make this pass.** If the triage cannot be finished in one run,
split it by batch and leave the pattern widened behind a smaller exemption list — a gate that
fails honestly beats one that reports OK while a writer it cannot see goes stale.
