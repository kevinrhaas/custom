---
id: T-1137
title: A change to the civic mint's derived note silently deletes every other pass's findings appended to the same card
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-14
closed: 2026-09-15
pr: 1364
claimed_by: Codex 9/15/2026, 2:49:01 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-09-15T20:25:51.900Z
claimed_run: null
---

A change to the civic mint's derived note silently deletes every other pass's findings appended to the same card.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found by T-1131, which hit it: the ticket changed one sentence of `arrival_block`'s note
and `--build` deleted about 6,000 characters of other passes' prose off
`hh_wolcott_alexander` — the Calumet Club receptions of 1879 and 1882, the federal land
tract sales, the town's own rolls. The change was reverted for that reason alone, so the
defect is still there and the next run that touches this pass's prose will hit it again.

**THE DEFECT.** `mint_civic_residents.carry_over()` preserves another pass's additions to
a person's note by prefix match:

    was = (old.get("note") or "")
    if was.startswith(person["note"]) and len(was) > len(person["note"]):
        person["note"] = person["note"] + was[len(person["note"]):]

The contract is "the derived note is a PREFIX of the committed one, and everything past it
belongs to somebody else". Change one character of the derived prefix and the match fails,
the branch does not fire, and every appended finding is dropped — silently, in a
`--build` that reports `wrote 415 file(s)` and nothing else. `--check` then passes on the
next run, because the truncated note is what re-derives.

**HOW IT SURFACED AT ALL, and it was luck.** `old_settlers.py --check` has its own gate
and went red with `wolcott_alexander ... does not say what the old-settlers roll is worth
— run --apply-citations`. The land-sales and civic-rolls appenders have no such gate, so
their prose would have gone and nothing would have said so.

- The boundary between this pass's prose and another pass's is held by something better
  than a prefix match — a marker, a structured field, or the appending passes writing
  where they cannot be truncated. Say which and why.
- A change to this pass's derived note does not delete another pass's findings, proved by
  a `--self-test` case that changes the derived prose and asserts the appended text
  survives.
- The same question is asked of the sibling mints that share `carry_over`'s contract.
- No card hand-edited; `--check` re-derives byte for byte. `bash tools/check.sh` green.
