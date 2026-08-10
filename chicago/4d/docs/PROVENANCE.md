# The provenance model

This is the part that makes the project worth doing. It is fixed before there are thirty
buildings in the dataset, not after.

## Confidence is per attribute, not per building

You will routinely know a building's footprint and location precisely while knowing nothing
about its roof pitch. A single confidence score per building would either lie about the
footprint or lie about the roof. So every attribute carries its own.

```jsonc
"form": {
  "stories":  { "value": 2, "confidence": "documented",
                "sources": ["kinzie_waubun_1856"] },
  "gallery":  { "value": true, "confidence": "conjectural",
                "note": "All surviving images are retrospective and disagree. Unresolved." }
}
```

| level | meaning | validator requires |
|---|---|---|
| `documented` | a primary or near-primary source directly attests this attribute at the scene date | ≥1 `source_id` resolving in `data/sources/` |
| `inferred` | derived from typology, adjacent evidence, or construction practice of the period and region | a non-empty `note` stating the reasoning |
| `conjectural` | no evidence; filled for visual completeness only | nothing — but it is surfaced in the build report and rendered distinctly |

A `conjectural` attribute carrying `sources` is a warning: either the source supports it (so
it is `documented` or `inferred`) or the citation is decorative.

## Evidence tiers

Not all sources are equal, and the dataset should not pretend otherwise.

| tier | kind | examples |
|---|---|---|
| 1 | period document, eyewitness at or near the date | period surveys, the 1834 Wright and Hathaway maps, newspaper advertisements |
| 2 | near-primary recollection | *Wau-Bun* (1856, describing 1831) — the load-bearing text for the Sauganash |
| 3 | compiled secondary from pioneer testimony | Andreas, *History of Chicago* (1884) — cite the page for every claim |
| 4 | later scholarly synthesis | Encyclopedia of Chicago, academic ecology and geology |
| 5 | modern retrospective illustration or reconstruction | the Conley/Stelzer 1933 pictorial map, Kurz & Allison chromolithographs |
| 6 | decorative or popular cartography | the 1940 Nelson/Winters pictorial map — **orientation and toponyms only; no geometry** |

Tier 5 and 6 sources may inform *inventory* (what existed, roughly where) and *cross-checks*.
They must never be the sole evidence for a `documented` attribute, and no geometry is traced
from them.

## Rights are part of provenance

Each source carries `rights_status`:

- `public_domain` / `no_known_restrictions` — usable, cite the holding institution.
- `check_required` — **may be cited in text, but no asset may be derived from it** until the
  check is done and recorded. The validator enforces this.
- `cleared` — a `check_required` source that has been resolved; record what was checked and when.

Web sources require an `archived_url`. Several of the best online references for this project
return 503s and 403s intermittently; a citation that cannot be re-read is not a citation.

## Date enforcement

Chicago between 1833 and 1837 changed faster than almost any settlement in American history.
A building correct for 1837 is wrong for 1835.

Every structure phase carries `documented_range`. For a given scene, a structure appears iff
**exactly one** phase's range covers the scene date. Overlapping phases are a hard error. No
covering phase means the structure is excluded from that scene, and the exclusion is reported.

**Do not widen a range to make the build pass.** Narrow it to what is attested and mark the
phase `conjectural` if that is what it is. A `documented_range` spanning more than about a
dozen years in this period earns a warning on principle.

`data/exclusions.json` records structures that were researched and deliberately left out, with
the date evidence and citation. It exists so that the next agent — or the next you — does not
helpfully re-add the Saloon Building.

## The confidence view is a deliverable

Every renderer implements a toggle that recolors the scene by evidence quality:

- `documented` — renders normally
- `inferred` — renders tinted
- `conjectural` — renders as translucent massing

Implementation is centralized (the generator paints a per-vertex confidence channel; the
renderer reads it through one shared material patch) so it cannot be forgotten per-building.
The visual claim and the citable claim come from the same record and cannot drift apart.

For a museum, a classroom, or a civic audience this is the single most valuable thing the
project offers.

## Confidence grades the evidence, not the view

A confidence chip answers *how sure are we of this value*. It cannot answer *are you looking at
it*, and the two come apart in the direction that does the most damage: a `documented` attribute
the generator never reads renders nothing and still shows the strongest claim the project makes.
Wolf Point Tavern's painted wolf sign was exactly that for as long as nobody checked.

So the two questions are recorded separately. Each archetype's `*_params.py` declares `CONSUMED`
— the form attributes its `from_phase` actually reads — and any attribute outside that set
carries a `geometry:` field saying what the mesh does instead:

- `absent` — the record attests it and nothing of it is built
- `simplified` — something stands in its place, but this value does not drive it
- `record_only` — never a build instruction: a rejected reading, a negative finding

`absent` and `simplified` are admissions, so `tools/validate.py` requires a matching `Covers:`
token in `docs/LIBERTIES.md` and the provenance popup marks the row. A missing declaration is a
gate failure, which means adding a generator parameter without adding it to `CONSUMED` fails
loudly rather than quietly excusing an omission.

The absence of the field asserts nothing on its own. An attribute inside `CONSUMED` is built
from its value by construction, which is the only reason it needs no declaration.

## When sources disagree

Record the disagreement in `docs/RESEARCH/<structure_id>.md`, state both readings and their
sources, pick the best-attested one, and **write down why**. Then reflect the uncertainty in
the data: a disputed attribute is `conjectural` or `inferred`, never `documented`.

A dispute that cannot be resolved is not a failure. It is the honest state of the evidence, and
the confidence view is built to show it.
