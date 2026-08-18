---
id: T-0054
title: Every liberty appended since L111 lands under the Resolved heading and compiles as resolved
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Every liberty appended to `docs/LIBERTIES.md` since **L111** has landed physically BELOW the
`## Resolved` heading, because new entries are appended to the end of the file and Resolved is the
last section. `tools/compile_liberties.py` reads the section a heading falls under, so seventeen
standing liberties — L111 through L127, including **L127**, written on 2026-08-18 for a fence that
is standing in the town right now — compile with `section: "resolved"`.

**Why it matters, and it is not cosmetic.** The Resolved section is EXEMPT from the coverage gate's
over-claim check, by design: it is what lets an append-only document survive its own data being
corrected. So every one of those seventeen entries is exempt from a check it should be subject to,
and the Evidence panel groups them as settled when they are not. Found while moving L60 to Resolved
for T-0051; L128 was placed in the per-subject section by hand to avoid joining them.

**Acceptance:** the misfiled entries read as standing liberties again — `data/liberties.json` shows
`section: "per_subject"` (or `standing`) for L111–L127, with each entry's placement decided by what
it says rather than by where the file ended — and `tools/check.sh` refuses a future append that
lands in the wrong section, so this cannot silently recur. No liberty text is edited: this is a
question of where the entries sit and what the document says about appending.
