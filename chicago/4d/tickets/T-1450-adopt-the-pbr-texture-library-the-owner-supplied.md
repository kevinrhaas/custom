---
id: T-1450
title: Adopt the PBR texture library the owner supplied: it is dimensionally interlocked with the material sheet, and ten of its twenty-five maps declare a module their pixels do not contain
state: open
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-09-20
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Adopt the PBR texture library the owner supplied: it is dimensionally interlocked with the material sheet, and ten of its twenty-five maps declare a module their pixels do not contain.

The owner supplied a 25-material PBR library (`Chicago_1835_PBR_Texture_Library`, four
parts, ~80 MB, CC0 per its LICENSE.txt, deterministic procedural synthesis with a seed per
material). Each material ships basecolor, roughness, AO, metallic, ORM, 16-bit height and
BOTH normal conventions, plus a `material.json`, a manifest, a contact sheet and research
notes.

**IT WAS GENERATED AGAINST THIS REPO'S MATERIAL SHEET, and that is the valuable part.**
`generators/common/materials.py` SUBSTRATES and the library agree to two decimals on the
tiling rate, the texel density and the mean roughness — seven substrates, not one of them
a coincidence:

| substrate | sheet `tile_m` / `texel_px_per_m` / roughness | library `span_m` / `px_per_m` / `mean_roughness` |
|---|---|---|
| clapboard | 4.48 / 228.6 / 0.86 | 4.48 / 228.57 / 0.86 |
| board_and_batten | 4.272 / 239.7 / 0.88 | 4.272 / 239.7 / 0.88 |
| vertical_board | 4.58 / 223.6 / 0.90 | 4.58 / 223.58 / 0.90 |
| hewn_log | 4.08 / 251.0 / 0.92 | 4.08 / 250.98 / 0.92 |
| sawn_board | 4.00 / 256.0 / 0.94 | 4.00 / 256.0 / 0.94 |
| heavy_timber | 4.00 / 256.0 / 0.90 | 4.00 / 256.0 / 0.90 |
| chinking / cat_and_clay | 2.04 / 251.0 / 0.95 | 2.04 / **501.96** / 0.95 |

The dimensional contract §3.2 argues for — *every tile a whole multiple of the surface's
own rhythm* — is already honoured in the metadata. The `material.json` schema also carries
a `confidence` tier per material with attested/reconstructed split out in prose, which is
this project's epistemics arriving in an asset pipeline unprompted.

**AND TEN OF THE TWENTY-FIVE DECLARE A MODULE THEIR PIXELS DO NOT CONTAIN.** Measured, not
eyeballed: take the row-mean and column-mean of each basecolor, remove the DC term, and
read the dominant spatial frequency. A clapboard tile of 4.48 m at 0.14 m exposure must
show **32 cycles** across the tile. It shows one.

| material | declared module | dominant row frequency | verdict |
|---|---:|---:|---|
| `hewn_log_oak_chinked` | 12 courses | **12** | carries it |
| `chicago_clay_brick_lime_mortar` | — | 48 rows × 40 cols | real coursing |
| `clapboard_red_oxide` | 32 courses | 35 (weak, 0.09) | partial |
| `clapboard_weathered_oak` | 32 courses | **1** | does not carry it |
| `clapboard_whitewash` | 32 courses | **2** | does not carry it |
| `clapboard_white_lead_paint` | 32 courses | **1** | does not carry it |
| `board_and_batten_weathered` | 12 battens | **1** | no battens |
| `vertical_sawn_board` | 20 boards | **1** | no boards |
| `wood_shingles_weathered` | — | **1** | no shingle units |

What those ten actually are is one wavy band-noise pattern re-tinted: no lap shadow, no
butt line, no batten, no stagger. **A file that declares a rhythm it does not have is the
one failure this project refuses everywhere else** — it is the atlas equivalent of a count
nobody measured (T-1447, yesterday).

**THREE MATERIALS ASSERT WHAT THE SHEET REFUSES IN WRITING.** `materials.py` says, in
terms: *"No source in this repository states what any Chicago roof of 1835 was covered
with... inventing one here to make the sheet look finished is the exact move
docs/LIBERTIES.md exists to catch."* The library ships `wood_shingles_weathered` and
`roof_boards_weathered`. The same module leaves `brick` and `stone` at `tile_m = None`
because the rate is UNRESOLVABLE *"rather than filled with a modern brick"*; the library
ships brick at 4.20 m and limestone at 4.00 m. The library's own notes are honest about it
(*"brick dimensions are reconstructed, not Chicago-attested"*) — which is what makes them
adoptable **under a written liberty**, and not adoptable silently.

**THE GROUND MAPS ARE THE BEST PIXELS AND THE WRONG TARGET.** `muddy_rutted_street` is the
strongest asset here — broadband, no dominant periodicity (peak share 0.02), real aggregate
and rut structure. But materials.md §1.2: *"The ground, the roads and the water are the only
textured surfaces in the scene and they are **runtime canvases**, not assets... W2's atlas
must not absorb them — three parcels have already been burned by treating the ground as a
building surface."* Taking them is a separate decision from this one.

**Acceptance:**

- The library is vendored under a stated path with its LICENSE, manifest and RESEARCH_NOTES
  intact, and a `docs/RESEARCH/` note recording where it came from, that it is CC0, and that
  it was generated against this sheet.
- A **conformance tool** (`tools/check_texture_module.py --check|--self-test`) measures each
  adopted map's dominant spatial frequency against the module its `material.json` declares,
  and is RED when they disagree. This is the gate that makes the table above reproducible
  rather than a paragraph in a ticket, and it is what stops the next library landing on
  vibes. Self-test drives it against a synthesised tile of known period.
- **Only maps that pass it are adopted.** The ten that fail are either regenerated against
  the module the sheet already commits — 32 courses, 12 battens, 20 boards — or left out.
  No map is adopted by relaxing the tolerance.
- `wood_shingles_weathered`, `roof_boards_weathered`, and the brick and stone tiling rates
  are each **refused, or taken with an L-number in `docs/LIBERTIES.md`** naming what is being
  claimed and on whose authority. The covering question is R-W2a finding 2 and is not closed
  by an asset arriving.
- `cat_and_clay_chimney` is resolved to 251 px/m (a 512 px tile at 2.04 m) or its divergence
  is argued, per the chinking row's own rule that *"a wall whose two materials render at two
  densities reads as two walls."*
- The ground and waterfront maps are NOT wired into the terrain program in this ticket;
  §1.2's warning is recorded and they are held for their own parcel.
- Nothing in `materials.py` changes its committed constants to match an asset. The sheet is
  the source; the atlas is authored against it (materials.md §3.1).

**Stop condition:** every texture the town ships carries the rhythm its metadata claims, and
a map that does not cannot be adopted without the gate going red.

**Links:** T-1210 (the fabric-by-household rule these maps would clothe) · T-0007 (the sheet
as code) · T-0126 (the openings half) · T-1447 (a figure nobody measured) ·
`docs/RESEARCH/materials.md` §1.2, §2.2, §3.1, §3.2, §3.4, §5 · R-W2a finding 2.
