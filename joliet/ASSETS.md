# Asset sourcing log — Old Joliet Prison game

## License policy

**CC0 / public domain only.** Every texture and environment map in
`public/assets/` was fetched from one of three CC0 sources: **ambientCG**
(ambientcg.com), **Poly Haven** (polyhaven.com), or **Kenney** (kenney.nl).
No assets from any commercial game, asset store, or non-CC0 source are used
anywhere in this project. Every row below records the exact source URL,
license, and fetch date for provenance. Original archives included preview
renders, sphere thumbnails, `.usdc`, `.mtlx`, `.blend`, and `.tres` files —
all of those were deleted; only the PBR map JPEGs actually used by the game
were kept.

All ambientCG materials were fetched at **2K JPG** resolution via
`https://ambientcg.com/get?file=<AssetID>_2K-JPG.zip`. All Poly Haven HDRIs
were fetched at **1K .hdr** resolution via the `api.polyhaven.com` /
`dl.polyhaven.org` file API. Every JPEG was re-encoded (quality 78 for
color/roughness/AO, quality 85 for normal maps, both with `optimize=True`)
to fit the 250MB browser-game asset budget without a visible quality loss —
still full 2048px resolution, just less redundant JPEG entropy. Only one of
AmbientOcclusion/Displacement was kept per set (never both), per the fetch
brief. The `water` set keeps only the normal map, since that's the only map
a rippling-water shader needs.

## Textures (`public/assets/textures/`)

| Asset | Local path | Source URL | License | Fetched | Notes |
|---|---|---|---|---|---|
| Limestone — ashlar/coursed | `textures/limestone-ashlar/limestone-ashlar_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Bricks008 (download: https://ambientcg.com/get?file=Bricks008_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Bricks008" — flat, coursed medieval sandstone church wall. Warm buff tone matches Joliet's dolomitic limestone; used for clean ashlar-coursed wall runs. |
| Limestone — rough rock-face | `textures/limestone-roughface/limestone-roughface_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Rock055 (download: https://ambientcg.com/get?file=Rock055_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Rock055" — beige/brown quarried cliff rock. Used for heavily quarry-tooled rustication (the rougher of the two limestone variants). |
| Concrete block (painted CMU) | `textures/concrete-block/concrete-block_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Concrete031 (download: https://ambientcg.com/get?file=Concrete031_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Concrete031" — painted grey-green bunker-style block tile pattern; used for interior painted CMU / glazed structural tile walls. |
| Concrete floor (worn/polished) | `textures/concrete-floor/concrete-floor_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Concrete048 (download: https://ambientcg.com/get?file=Concrete048_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Concrete048" — clean, smooth, pale grey-beige industrial floor slab. |
| Rusted metal — sheet rust | `textures/rusted-metal-sheet/rusted-metal-sheet_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Rust009 (download: https://ambientcg.com/get?file=Rust009_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Rust009" — heavy orange rust bloom on flat sheet steel. Variant 1 of 2. |
| Rusted metal — pitted/scaled | `textures/rusted-metal-pitted/rusted-metal-pitted_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/MetalWalkway014 (download: https://ambientcg.com/get?file=MetalWalkway014_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "MetalWalkway014" — rusted, pitted, scaled walkway steel. Variant 2 of 2. |
| Painted metal, chipped | `textures/painted-metal-chipped/painted-metal-chipped_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/PaintedMetal014 (download: https://ambientcg.com/get?file=PaintedMetal014_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "PaintedMetal014" — grey painted steel with rust showing through the chips. |
| Asphalt, cracked | `textures/asphalt/asphalt_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Road013A (download: https://ambientcg.com/get?file=Road013A_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Road013A" — cracked, worn parking-lot-grade asphalt. **Could not find a CC0 asphalt texture with weeds pre-baked into the cracks** (see "Not sourced" below) — add weeds as a separate decal/vertex-paint layer in-engine if needed. |
| Ground — dirt/gravel | `textures/ground-dirt-gravel/ground-dirt-gravel_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Ground081 (download: https://ambientcg.com/get?file=Ground081_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Ground081" — brown dirt/gravel path, rocky. For the perimeter approach. |
| Grass (mown lawn) | `textures/grass/grass_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Grass001 (download: https://ambientcg.com/get?file=Grass001_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Grass001" — dense, short, mown lawn grass. |
| Water (ripple normal map) | `textures/water/water_NormalGL.jpg` | https://ambientcg.com/a/Ice001 (download: https://ambientcg.com/get?file=Ice001_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Ice001" is tagged "lake/water" — a frozen-lake surface whose normal map is naturalistic surface ripple, a common repurposing for standing-water ripple shaders. **No literal "standing water" PBR set exists in ambientCG's or Poly Haven's public catalogs** (checked both; see "Not sourced" below) — only the NormalGL map is kept since a rippling-water shader (tinted, animated-UV) only needs the normal map, not the Color/Roughness of ice. |
| Brick (powerhouse interior) | `textures/brick/brick_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Bricks097 (download: https://ambientcg.com/get?file=Bricks097_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Bricks097" — old, dirty, industrial red factory brick. |
| Wood planks, rotten | `textures/wood-planks-rotten/wood-planks-rotten_{Color,NormalGL,Roughness,AmbientOcclusion}.jpg` | https://ambientcg.com/a/Planks039 (download: https://ambientcg.com/get?file=Planks039_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "Planks039" — dirty, large, old, rough medieval planking. For boarded windows and roof timbers. |
| Metal grate (catwalks) | `textures/metal-grate/metal-grate_{Color,NormalGL,Roughness,Displacement}.jpg` | https://ambientcg.com/a/MetalWalkway013 (download: https://ambientcg.com/get?file=MetalWalkway013_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "MetalWalkway013" — open steel floor-grid/grate pattern. No AO map was published for this set, so Displacement was kept instead. |
| Diamond plate (catwalks) | `textures/diamond-plate/diamond-plate_{Color,NormalGL,Roughness,Displacement}.jpg` | https://ambientcg.com/a/DiamondPlate001 (download: https://ambientcg.com/get?file=DiamondPlate001_2K-JPG.zip) | CC0 (ambientCG) | 2026-08-01 | ambientCG "DiamondPlate001" — clean tread-plate steel pattern. No AO map published; Displacement kept instead. |

## Environment HDRIs (`public/assets/env/`)

| Asset | Local path | Source URL | License | Fetched | Notes |
|---|---|---|---|---|---|
| Night sky w/ moon | `env/night-moonlit-golf_1k.hdr` | https://polyhaven.com/a/moonlit_golf (file: https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/moonlit_golf_1k.hdr) | CC0 (Poly Haven) | 2026-08-01 | Poly Haven "Moonlit Golf" — clear night sky, tagged `moon`, `stars`, `field`. 1K .hdr. |
| Moody overcast dusk | `env/dusk-overcast-aarfontein_1k.hdr` | https://polyhaven.com/a/aarfontein_dusk (file: https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/aarfontein_dusk_1k.hdr) | CC0 (Poly Haven) | 2026-08-01 | Poly Haven "Aarfontein Dusk" — broad overcast cloud cover at dusk, soft cool ambient light, subtle horizon glow. 1K .hdr. |

## Total size

`du -sh public/assets/` → **42 MB** (well under the 120 MB target and the
250 MB total budget). Breakdown: `textures/` ≈ 39 MB, `env/` ≈ 3.2 MB.

No sets were dropped to hit budget — after JPEG re-encoding (see License
policy above) the whole set already came in at ~42 MB, so there was room to
spare. Nothing was requantised below the requested 2K resolution; only
redundant JPEG bit-depth was trimmed.

## Could not source (documented gaps)

- **Asphalt with weeds growing in the cracks, pre-baked into one texture**:
  not present in ambientCG's or Poly Haven's public CC0 catalogs under any
  reasonable search term (asphalt+weeds, asphalt+grass, pavement+moss). Used
  plain cracked asphalt (`Road013A`) instead; weeds should be added as a
  separate grass-clump decal/instance layer in the shader/scene rather than
  baked into the ground texture.
- **A literal "standing/rippling water" PBR material** (Color + Normal +
  Roughness for a pool/pond surface): no such asset exists in ambientCG's
  Material catalog or Poly Haven's HDRI/texture catalogs (both were searched
  directly via their JSON APIs for "water", "ripple", "pool", "wave",
  "puddle", "ocean"). Substituted ambientCG's `Ice001` (a frozen-lake
  material tagged `water`) and kept only its NormalGL map, which is the only
  map a typical animated rippling-water shader needs — this is a standard,
  transparent repurposing, not a mislabeling, and is called out here and in
  the row above.
- **Kenney.nl** was checked for a suitable water/ripple normal map as a
  fallback; its asset listing page renders via client-side JS with no static
  HTML fallback reachable via `curl`, and no relevant texture pack could be
  confirmed by name, so it was not used for any asset in this pass.
