---
id: T-1158
title: Per-attribute tiers on every person, household and business field — attested, inferred or reconstructed, each with its reason — so a profile can be filled at the lowest honest tier and replaced later
state: open
epic: META
requested_by: owner
seen: true
effort: M
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

The owner, 2026-09-17: *"note for each attribute of each person what is attested, inferred or
reconstructed and reasons why."* Today the grade is carried per PERSON (`grade`, ladder rung) and
per structure attribute (`confidence` blocks on structures), but a person's sex, birth year,
arrival, origin, relationship and roles do not each say which tier THEY stand on. T-1146 adds
per-value provenance for asserted facts; this ticket makes the third tier — `reconstructed` —
a first-class per-attribute value with a required `basis`, so the analysis and reconstruction
bands can fill every attribute honestly and a later source can replace one value without
touching the rest.

**One collision to resolve first.** Household claim blocks (`arrival`, `origin`,
`reason_for_coming`, `lives_at`, `works_at`, `party_size_on_arrival`, `occupation`) already use
`confidence: "reconstructed"` — 7,383 times — to mean *not attested*, almost always with `value:
null` ("Not attested."). That is the opposite of what the tier will mean once a value is actually
invented. The migration below reads a null-valued `reconstructed` block as `tier: unknown` (a new
value that means "nothing is asserted yet") and reserves `reconstructed` for a non-null value
carrying `basis` and `seed`; `audit_confidence.py --strict` and `validate.py` refuse the old
ambiguity after the migration, and the renderer prints "not recorded" for `unknown`.

**The model (additive — no existing field moves; validators accept the old shape until the
migration below runs):**

- Every scalar person attribute that reconstruction will touch — `sex`, `birth_year` (with
  `precision`), `arrival` (date + precision + `reason`), `origin`, `relationship`,
  `presence`, `division`, each `roles[]` entry, `lives_at[]`/`works_at[]` entries, `name` (for
  a reconstructed name) — becomes `{ value, tier: attested|inferred|reconstructed, basis,
  source_id?, claim_id?, model_id?, seed? }`. `attested` requires `source_id`; `inferred`
  requires a `basis` naming the evidence about THIS person; `reconstructed` requires `basis`
  naming the MODEL row it was drawn from (`data/reconstruction/1835_population_model.json` etc.
  once T-1161 lands — until then a stated rule) and the deterministic `seed`.
- Household and business records take the same shape on `composition`, `type`, `capacity`,
  `staff[]`, `proprietors[]`, `location`.
- A record-level `grade` stays, derived: the HIGHEST tier of its identity (name + presence)
  assertions, never above `reconstructed` when the name is invented (`tools/validate.py` already
  refuses an invented name above the bottom tier — keep that rule and extend it).
- `replaceable_by: { kind: person|household|business, match: <rule> }` on every reconstructed
  record and attribute: what evidence would retire it (the owner: *"so if we get new research …
  we can replace the reconstructed person or business with an inferred or attested one later"*).

**Acceptance:**

- Schema (`data/residents/`, the business schema, `data/structures.schema.json` occupant links)
  extended; `tools/validate.py` refuses a tier without its required fields and a `reconstructed`
  value with no `basis`/`seed`; a mutation self-test in `check.sh` breaks each rule.
- Migration tool `tools/migrate_attribute_tiers.py --build|--check` lifts every existing value
  into the shape at the tier its current provenance supports (attested source → attested;
  `inferred` note → inferred), with a report of counts per attribute per tier. Zero value changes
  tier upward; the check is wired.
- The evidence panel (`renderers/web/js/` people card) prints the tier beside each attribute and
  the basis on hover/expand, and the People view gains a filter `attested / inferred /
  reconstructed` that reads the derived record grade. This is the visible half of the ticket.
- `summarize_residents.py` (and the town census) gain a per-attribute tier section.
- `docs/PROVENANCE.md` documents the per-attribute shape and the replaceability rule.

**Stop condition:** every person/household/business attribute the reconstruction bands will
write has a place to say its tier and why, and a reconstructed value cannot be written without
a basis and a seed.

**Links:** T-1145 · T-1146 · T-1147 · AGENTS.md § RECONSTRUCTED IS A TIER · `docs/PROVENANCE.md`.
