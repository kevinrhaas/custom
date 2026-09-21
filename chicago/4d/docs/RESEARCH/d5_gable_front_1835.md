# Did the deep-plan gable-front cottage stand in Chicago on 1 July 1835?

**Ticket:** T-1497. **Answer: no — not as a dwelling, and not as the defining silhouette of a
58-roof family.** The reading below is the first half of that ticket, and it was taken before
any archetype was written, because the cheaper outcome had to stay available: if the form is
not 1835, the repair is to the D5 crosswalk row and no generator is built at all. It is not
1835, and that is what this document establishes.

## The question, stated so it can be answered

`data/reconstruction/1835_family_archetype_crosswalk.json` authors family **D5 — Deep-plan
frame cottage**, 58 roofs town-wide, as `roof: "front gable, 7:12-10:12"`, `variants: "narrow
urban plan; side entry"`, and names a canonical archetype it does not have —
`dwelling_frame` with a `deep_plan_gable_front` variant. Its `evidence_note` says the current
generator "is eaves-front and therefore compresses the defining front-gable silhouette".

`generators/archetypes/frame_dwelling_params.py` refuses that shape in as many words, and
gives a date for the refusal:

> The eaves-front house is the 1835 form; the gable-front house, turned end-on to the street,
> is the Greek Revival habit that arrives with the Clarke House in 1836 and dominates the
> 1840s.

Two committed documents, both cited, in flat contradiction. Either D5 should not be a
front-gable family for this scene, or the archetype's 1836 line is too hard for a *deep-plan*
cottage whose gable faces the street for want of frontage rather than for fashion. That is a
question about the town, not about the renderer, and it is what follows.

## What the sources actually attest

**Gable-front building IS attested here — on the store row, and only there.**
`gifford_tremont_house_no_1` (tier 5, `describes_date` 1833-1839) is read in its own source
record as showing "gable-front and eaves-front stores alternating along one street rather than
one repeated form", in a continuous row of one-and-a-half and two-storey stores "standing
shoulder to shoulder with shared party lines". That is the only attestation of a gable end
addressing a street anywhere in `data/sources/`. It is commercial, it is party-walled, and the
crosswalk already serves it: C1, C2 and C3 are front-gable store families built by
`frame_storefront`, which carries no eaves-front refusal. A store row's narrow front is a
party-line fact. It does not transfer to a detached cottage standing alone on a platted lot.

**No dwelling in this dataset is attested with its gable to the street.** `gable` appears in
five source records in all — the Gifford view above, and four that describe a gable as a roof
end rather than as a front: the Green Tree plate and its two textual witnesses, and the Chappel
school shore view's log building. None of the four turns a house end-on. The one record that
states a dwelling's orientation states the opposite: the Green Tree's entrance is "on the Lake
street front about the middle of the long side" (`chicagology_prefire127`) — the long side is
the street side, which is what eaves-front means. Nothing reached in `data/sources/` describes,
depicts or implies a Chicago *house* turned end-on before the scene date.

**The stylistic driver post-dates the scene, and this project already dated it.**
`data/exclusions.json` carries `clarke_house`: "Built 1836, and well outside the platted town
in any case. Greek Revival on 20 acres... Frequently and wrongly pulled into early-Chicago
scenes because it survives today as the city's oldest house." The gable-front dwelling is the
Greek Revival temple front's vernacular descendant. Its Chicago arrival is a year after
1 July 1835 and the exclusion list already refuses it by date.

**The non-stylistic driver does not exist on this plat.** A deep plan is turned end-on to save
frontage. There was no frontage to save. The committed lot grid,
`data/traces/vectors/thompson_lots.json`, holds **226 lots** across five grids; its own
`module` authors a **80 ft** lot frontage and its own `summary` records a range of **24.3 to
169.2 ft**. Measured over the committed polygons the median frontage is **80.1 ft** and only
**two lots of 226** fall below 34 ft:

```
python3 - <<'PY'
import json, statistics
d = json.load(open('data/traces/vectors/thompson_lots.json'))
f = [l['frontage_m']/0.3048 for b in d['blocks'] for l in b.get('lots', [])]
print(len(f), round(min(f),1), round(statistics.median(f),1), sum(1 for x in f if x < 34))
PY
# 226 24.3 80.1 2
```

D5's widest authored form is 24 ft. On the median lot that house has 56 ft of slack beside it.
Turning it end-on saves a frontage nobody in 1835 Chicago was short of, and buys a silhouette
the town would not see for another decade.

## What the town already built, which settles it in practice

D5 has 32 instantiated roofs. **Thirty-one of them are eaves-front**, standing 1.27 to 1.50
times deeper than wide — the ceiling `frame_dwelling_params` sets and `tools/family_bands.py`
clamps to. The front gable the row asks for has never been built, not once, in 32 roofs. The
single exception is `recon_1835_west_033`, which is not the family's form but the one record
where the recipe authored a rectangle past the ceiling (20 × 32 ft, ratio 1.6) and
`tools/generate_west_infill.py` turned it a quarter circle to get it through the placeholder —
so it stands as `32.00 × 20.00 ft` and reads out of the very band it cites. It is banked in
`tools/band_claims_baseline.json` with `waiting_on` naming this ticket.

So the reconstruction has been eaves-front all along. What the row asked for was never a
description of the town; it was a description of a generator nobody wrote.

## The ruling

1. **D5 is an eaves-front family.** Its row is repaired to say so: `side gable`, and a variants
   line that no longer claims a narrow urban plan. The deep plan itself is kept — D5 remains
   the deepest cottage on the sheet, 1.4 to 1.5 times deeper than its front — because nothing
   above argues against depth. What is withdrawn is the claim that the depth was presented
   end-on.
2. **No archetype is built.** `dwelling_frame` / `deep_plan_gable_front` is not needed, and
   building it would have put a form in the scene that no source in this dataset supports.
   `frame_dwelling` is D5's archetype, not its placeholder.
3. **`frame_dwelling_params`'s 1.5 refusal is untouched**, and the bands are untouched, so no
   other family's dealt dimensions move.
4. **`recon_1835_west_033` is repaired the way this project has already repaired this exact
   fault.** T-1445's roof redeal met the same 20 × 32 ft rectangle at `recon_1835_west_009` and
   took two feet off its depth — "each the smaller of the two moves its own band permits"
   (`docs/LIBERTIES.md`). The recipe row becomes `[20, 30]`, which is the figure the recipe
   already authors for `west_rec_004` and `west_rec_009`, sits inside D5's band, and stands at
   exactly the 1.5 the archetype allows. The facing correction is deleted; the house is built
   from the recipe with no swap, facing the street on its own long side.

**Which way this is wrong if it is wrong.** Toward a town whose smaller houses read a little
more alike than they were — 58 roofs that the crosswalk wanted to vary by turning some of them
end-on now all present a long side to their street. That is the price of refusing a form no
source reached, and it is the direction this project has said it prefers to be wrong in. The
door is not closed: a source that shows a Chicago dwelling gable-end to a street before July
1835 re-opens the row, and this document is the thing it would have to argue with.

## Sources

- `gifford_tremont_house_no_1` — tier 5 illustration, 1833-1839; the store row's alternating
  gable-front and eaves-front fronts. Commercial only.
- `chicagology_prefire127` — tier 2; the Green Tree's entrance on the long side to Lake Street.
- `andreas_1884_v1` — via `data/exclusions.json` `clarke_house`; Greek Revival arrives 1836.
- `owner_chicago_1835_reconstruction_spec_2026` — the crosswalk's own source, which authors
  D5's counts and bands and documents no individual building.
- `data/traces/vectors/thompson_lots.json` — the committed lot grid; the frontage measurement.
