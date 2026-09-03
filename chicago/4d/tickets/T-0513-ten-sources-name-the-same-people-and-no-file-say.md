---
id: T-0513
title: Ten sources name the same people and no file says which names are one person: the cross-source identity master under the ratified grading ladder
state: open
epic: META
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-02
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

**The owner's ask, 2026-09-03, verbatim:** "And then create a final ticket that does a review and
consolidation of that research."

**The finding.** By the time the sweep above lands, the same men and women will be named in up to ten
places — the residents layer (848), the newspaper gazetteer (2,630 persons), the four voter lists (346
entries), the 1830 schedule, the 1840 heads (up to 964), the baptismal register, Fergus 26–29, Hubbard,
the 1839 directory, and fifteen cohort findings ledgers — and every one of those domains declares its
own merges and refusals against the residents layer, not against each other. Nothing says, for one
identity, everything the project knows. The newspapers solved this for themselves with `identity.json`
("the ONLY place two differently-spelled names may become one person"); this ticket does it across
domains, and it is where the grading ladder is APPLIED as a proposal — not yet to the records.

**The ratified grading ladder** — the owner's ruling of 2026-09-03, recorded verbatim, binding on every
grade this programme assigns: "attested = 1835 poll + any second independent source, or a contemporary
record naming the person in Chicago; inferred = 1835 poll alone, or 1833/1834 lists with another source,
or baptism parent/godparent 1833–35, or Hubbard/Fergus naming a resident with trade or address;
projected_resident = a single appearance with nothing else; 1839/1840 alone is never a 1835 resident
(later evidence only)." And the owner's tier definitions from the ask, verbatim: "for ones that you are
confident, those will be attested, the ones corroborated, those who you have a source or some potential
sources that you think you are reasonably sure, include all those unasserted as inferred. the balance of
people who you have seen in at least one source, they are documented, but you have some names of and
you dont have much else, you can put those in a sub category of inferred as a projected resident, under
the inferred category so we can filter by attested or inferred." 

**The ask.**

1. `tools/consolidate_resident_evidence.py --build | --check | --self-test` →
   `data/research/residents/identity_master.json`: one row per identity, listing every domain
   appearance (domain, record id, `as_read`, `normalized`, locator, describes_date), the declared
   cross-domain merges (rule id, discriminator, evidence) and refusals (rule id, why — surname-only
   is always a refusal; same surname different forename initial NEVER merges, the newspapers' rule),
   and the canonical person id where one exists. Rules carry ids so a later reader can count which
   fired.
2. `data/research/residents/source_coverage.json`: per domain — names read, matched, candidate,
   unmatched, negative searches recorded — and the overlap matrix between domains.
3. `docs/RESEARCH/resident-grading-policy.md`: the ratified ladder verbatim with its date, one rule id
   per rung (G1…), the evidence types each rung accepts, and worked examples from the master; the
   place a later run reads before grading anyone.
4. `data/research/residents/grading_proposal.json`: for every identity, the proposed `grade`,
   `resident_subtype`, the rule that fired and the evidence rows it fired on; for every existing person,
   the proposed change (or none) with the rule; conflicts (two rules disagreeing) listed for the owner
   rather than resolved silently. NOT applied — **T-0514** mints and **T-0515** regrades from this file.
5. A review section in the same doc: what each source turned out to be worth, which domains
   disagree with which, and the gaps that remain — the "review" half of the owner's ask.
6. `check.sh` steps for `--check` and `--self-test`.

**Dependencies:** this ticket consumes T-0493–T-0512. If any of them is still open, work that instead
— `blocked_on` carries one id, so CHECK THE LEDGER; a consolidation run before its inputs land is a
consolidation run twice.

**Runner notes (2026-09-03):** the improve runner's custom lane now installs `pdftotext` and
`pdftoppm` (poppler-utils), `tesseract`, `openpyxl` and `pypdf` before the run (polecat-platform
`steward-improve.yml`, on the owner's instruction the same day), and the gate installs `openpyxl` and
`pypdf` beside `jsonschema` and `pyproj`. Check with `command -v pdftotext tesseract` and
`python3 -c 'import openpyxl'` first — a failed install is a `::warning` in the step log, not a
surprise — and if one is missing, fall back to `pypdf` and page reads. Write CSV always and XLSX
when openpyxl imports. Never disable TLS or unset HTTPS_PROXY.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Every named identity in every landed domain has exactly one master row or a recorded refusal; zero
  unresolved duplicates without a refusal.
- Proposed counts by grade and subtype stated against the #668 baseline (117 attested / 731 inferred /
  706 projected / 848 persons); conflicts listed.
- The policy doc carries the ladder verbatim with rule ids; `--self-test` fires on a surname-only
  merge, a rule with no evidence, an identity in two rows, and a grade above what its rule allows.
- No household file is changed here.

**Links:** `data/research/newspapers/identity.json` (the model) · `source_hierarchy.json` · T-0487
(the first adjudication) · T-0514 · T-0515 · T-0517.
