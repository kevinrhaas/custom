---
id: T-1167
title: The 1835 resident reconstruction programme: one recipe file, one generator, the `reconstructed` grade turned on — superseding the retired programme without restoring it, and stating the owner's 2026-09-17 override of the no-estimation rule
state: open
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: null
opened: 2026-09-16
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

**The owner, 2026-09-17:** *"create reconstructed residents households businesses structures and
any other items … including what I think are a fair number of missing women and children and
perhaps former slaves or other less documented individuals, certainly mark these family members
and people as reconstructed."* And: *"we should make the expected number of residents and data of
the town complete with these reconstructed residents."*

This reverses, deliberately and on the owner's instruction, three standing readings — and the
reversal has to be written down before any person is written, or the next run will re-apply them:

1. `docs/RESEARCH/residents-households-summary-2026-09.md` § "What this layer must not be asked
   to do is estimate" — the recommendation, not a rule; superseded by the owner's direction for
   the `reconstructed` tier ONLY. Attested and inferred grades stay exactly what the ladder says.
2. T-1146 acceptance ¶4 — "aggregate age/sex buckets … mint no spouse, child, boarder or
   servant" — binds the attested/inferred spend and does not bind a reconstruction that labels
   every such person `reconstructed` with a basis and a seed. State this on T-1146 (a one-line
   note, not a re-decision) and here.
3. `composition_1840.json.what_this_may_not_do[]` — "never names anybody"; still true. The
   1840 shape is a distribution the models draw from; it never supplies a name or a row.

**What this ticket builds** (no person is written here):

- `data/reconstruction/1835_resident_reconstruction_programme.json` — the recipe: which model
  files (T-1161, T-1162, T-1163, T-1164, T-1165), which
  order book (T-1166), the id scheme (`hh_rc_<surname>_<given>` / `rc_<surname>_<given>`
  for invented people; roster re-admissions keep `hh_<read name>` with `source_pass:
  reconstructed_readmission`), the seed rule (household id + bucket), the naming rule (pools by
  community, collision check against the identity master), `replaceable_by` template text, the
  LIBERTIES entry ids it will fill, and the standing constraint restated: no reconstructed
  Native or Métis person, no reconstructed kin for a `touches_removal` household.
- `tools/reconstruct_residents_1835.py` — the ONE writer for `grade: reconstructed` persons and
  households and for reconstructed attribute values on existing persons, with `--stage <ticket
  key> --build|--check|--self-test` so each ticket below is a stage of one deterministic build,
  and `--check` re-derives every stage in `check.sh`. Mutation self-test: a reconstructed person
  without basis/seed, a reconstructed attribute above its tier, a Native reconstruction, an
  attested name reused — each refused.
- The retired programme stays retired: `1835_inferred_household_programme.json
  .resident_population_active` remains `false`; its 31 `inferred_anonymous` roofs are stock for
  T-1197; its 29-row occupation census is superseded by T-1162 and the file's `_doc`
  says so.
- `validate.py`: `grade: reconstructed` allowed on persons, requires `name_basis`, `basis`,
  `seed`, `replaceable_by`; the existing invented-name floor rule kept.
- `people.js` filter pills gain `reconstructed`; `census.js`/town census count the grade.

**Acceptance:** the programme file, the writer skeleton with self-tests, the validator rules,
the People-view pill, and the note on T-1146 land; `check.sh` green; `docs/RESEARCH/
1835_resident_reconstruction.md` opened with the owner's direction quoted and the three
supersessions stated.

**Stop condition:** every ticket below can run as a stage of this tool and nothing else can write
a reconstructed person.

**Links:** T-1158 · T-1166 · T-0489 · T-0516 · T-1146 · AGENTS.md § RECONSTRUCTED IS
A TIER · `1835_invented_name_pools.json`.
