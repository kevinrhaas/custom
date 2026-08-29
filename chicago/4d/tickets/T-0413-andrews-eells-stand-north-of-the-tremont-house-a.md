---
id: T-0413
title: Andrews & Eells stand north of the Tremont House, and the register can now say so
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

Andrews & Eells stand north of the Tremont House, and the register can now say so.

Both this and **T-0414** fell out of **T-0385**, which taught `tools/compile_register.py`
to see the first Tremont House through the disambiguator this project put in its name.
Three businesses were anchored on that one hotel and could not reach it; T-0385 built one
of them, the New York Clothing Store, and filed the other two rather than bundling them.

The register today reads `new_building` on `tremont_house_1` for `business_andrews_eells`,
which until 2026-08-29 was `unplaceable`. The printed anchor is thin and that is the whole
of the work here: the American sets it as `in [i]ts various branches, [nor]th of [the
Tremo]nt House` — a direction with NO COUNT OF DOORS and no side of the street, where
the clothing store's had both. So this ticket is not a copy of T-0385's: it has to decide
whether a bare `north of` is placeable at all, and saying it is not — and recording why
— is a legitimate outcome.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- Either Andrews & Eells stands in Dearborn Street with its residual stated on the record
  and a liberty naming what was chosen, or the ticket is closed with the reading written
  down: a direction with no offset places nothing, and the register's `new_building`
  action is the anchor resolving, not an address.
- Whichever way it goes, `docs/LIBERTIES.md` L214's three-part admission — the side of
  the street, the width of a door, the alley — is the shape to follow or to argue with.
- If it is built: `./tools/check.sh` green, `./tools/bake.sh --only`, `./tools/publish.sh`
  and a changelog entry in the same commit.
