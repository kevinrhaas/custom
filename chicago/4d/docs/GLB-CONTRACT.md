# The asset contract

**This is the interface between the generators and every renderer.** Track A (Blender) writes
it; Track B (three.js) and any future engine reads it. Neither side may change it unilaterally —
a change here is a change to the project's portability promise.

The rule from `AGENTS.md`: renderers consume glTF + JSON sidecars. They never reach into
`generators/` or reimplement the data model.

## Geometry

| | |
|---|---|
| container | `.glb` (binary glTF 2.0) |
| axes | **Y-up, right-handed** (glTF native) |
| units | **metres** |
| origin | each structure's mesh is authored about **its own local origin**, at ground level (y = 0 at the base of the walls) |
| placement | the renderer positions the node from the **sidecar**, not from a baked-in world transform |
| winding / normals | counter-clockwise, outward |

Authoring in metres about a local origin is what lets a structure be re-placed when its position
firms up — which will happen, because most positions currently carry `symbolic_location` and
±20 m of georeferencing uncertainty.

## Node naming and identity

One node per structure **phase**:

```
node.name    = "<structure_id>__<phase_id>"     e.g. "sauganash_hotel__frame_1831"
node.extras  = { "structure_id": "...", "phase_id": "...", "scene_ids": ["1835"] }
```

`extras` survives round-trips through Blender, glTF-Transform, Godot and glTFast, and is
diffable in git. The renderer resolves picks through `extras.structure_id`, never by parsing the
name.

**Multi-material split — verified 2026-08-09, matters for picking.** A structure with several
materials exports as ONE node with several child meshes (`…__frame_1831_1`, `…_2`, …). glTF
primitives cannot span materials, so this is unavoidable. Consequences:

- `extras` lands on the **parent node** (three.js: `object.userData`). The child meshes carry
  **empty** `userData`. A raycast hits a *child*, so **the renderer must walk up the ancestors
  to find `structure_id`** — reading it off the hit object returns nothing.
- Each child is its own draw call until batched. A four-material building is four calls; the
  ≤50–80 budget assumes the buildings get merged into a `BatchedMesh` before that matters.
- `_CONFIDENCE` is present on **every** child, verified in three.js as
  `geometry.attributes._confidence` (float, lowercased by GLTFLoader as expected).

## The confidence channel — `_CONFIDENCE`

**The single most important part of this contract.** The generator knows which geometry derives
from which attested attribute; the renderer does not and must not guess.

Every vertex carries a **custom glTF attribute `_CONFIDENCE`** (`SCALAR`, float) encoding the
confidence of the attribute that produced that geometry:

| value | meaning |
|---|---|
| `0.0` | `documented` |
| `0.5` | `inferred` |
| `1.0` | `conjectural` |

**Why not `COLOR_0`** (revised 2026-08-09 after a Blender spike): glTF defines `COLOR_0` as a
**multiplier on base colour**, so a documented value of 0.0 would render the building black in
any spec-compliant renderer, and 0.5 would half-darken every inferred surface. Blender's
exporter also silently drops `COLOR_0` unless it is wired into the material node tree — it
emits `WARNING: The active Vertex Color will not be exported, as it is not used in the node
tree of the material`, and you get a GLB with no confidence data and no error. A custom
underscore attribute avoids both problems: it is spec-sanctioned, it is never touched by
material evaluation, and it says what it means.

**Blender side:** create a `FLOAT` attribute on the `POINT` domain named `_CONFIDENCE` and
export with `export_attributes=True`. No material wiring needed.

**three.js side:** `GLTFLoader` lowercases unknown attributes, so it arrives as
`geometry.attributes._confidence`. Declare it in the shader patch yourself
(`attribute float _confidence;` / `in float _confidence;`) — three will not wire it for you,
and that is the point: it never tints anything by accident.

Worked example, the Sauganash `frame_1831` phase:

| geometry | driven by | value |
|---|---|---|
| wall massing, storey height | `stories` documented, `wall_height_m` conjectural → **worst wins** | `1.0` |
| clapboard cladding, white paint | `paint` documented | `0.0` |
| shutters | `shutters` documented | `0.0` |
| roof | `roof_type` conjectural | `1.0` |
| attached log wing | `log_wing` inferred | `0.5` |
| footprint outline | `footprint` conjectural | `1.0` |

**Rule when several attributes drive one piece of geometry: the least confident wins.** A wall
whose height is a guess is a guessed wall, even if we know it was white.

`COLOR_0` stays free for actual colour, and is currently unused.

## Materials

- One shared material per batch where possible — the buildings render as a single
  `BatchedMesh`, so per-building materials defeat the draw-call budget.
- Run `gltf-transform palette` so flat per-building colours become a shared atlas.
- **Bake ambient occlusion into the texture**, not into vertex colours.
- No emissive, no transparency in the base asset. The confidence view's translucency is a
  *renderer* effect (screen-door dither in the opaque pass), never baked geometry.

## Compression

| artifact | form | where |
|---|---|---|
| archival master | uncompressed `.glb` | `assets/gltf/` (committed, not published) |
| web derivative | `EXT_meshopt_compression` + KTX2 textures | `assets/web/` → published |

The master is the source of truth; derivatives regenerate from it. Meshopt over Draco: it
decodes far faster with no per-file WASM cold start, which matters more than bytes for ~150
small meshes.

## The sidecar

One JSON per structure per scene, compiled by `tools/compile_scene.py`, published alongside the
GLB. The renderer reads placement, provenance and footprint from here.

```jsonc
{
  "id": "sauganash_hotel",
  "phase": "frame_1831",
  "name": "Sauganash Hotel",
  "aka": ["Eagle Exchange Tavern"],
  "asset": "gltf/sauganash_hotel__frame_1831.glb",
  "placement": {
    "local_e": 0.0, "local_n": 0.0, "rotation_deg": 0.0,
    "position_confidence": "documented",
    "symbolic_location": "SE corner of Lake St and Market St",
    "uncertainty_m": 20
  },
  "attributes": {
    "stories":  { "value": 2, "confidence": "documented", "sources": ["kinzie_waubun_1856"] },
    "gallery":  { "value": false, "confidence": "inferred", "note": "..." }
  },
  "citations": [
    { "source_id": "kinzie_waubun_1856", "citation": "...", "url": "...", "archived_url": "...",
      "tier": 2 }
  ],
  "research_doc": "docs/RESEARCH/sauganash_hotel.md"
}
```

`placement.local_e` / `local_n` are **metres east and north of the scene datum origin**
(`data/datum.json`). While a structure's coordinates are still null, the compiler emits the
placement it does know and flags `"placement_provisional": true` — the renderer shows such
buildings normally but the confidence view treats position as conjectural.

`uncertainty_m` carries the georeferencing reality forward: nothing traced from the 1834 sheets
is better than about ±20 m.

## What the renderer must implement

1. **Confidence view** — a toggle reading `_CONFIDENCE` through one shared material patch:
   documented renders normally, inferred tints, conjectural renders as dithered translucent
   massing. Centralised so it cannot be forgotten per-building.
2. **Pick → provenance** — raycast to a batch id, resolve `extras.structure_id`, show the
   sidecar's attributes and citations. The visual claim and the citable claim come from the same
   record and cannot drift apart.
3. **Placement from the sidecar**, so re-georeferencing a building never requires a rebake.

## Placeholder assets during development

Track B does not wait for Track A. Until real bakes land, the renderer may load a placeholder
GLB that satisfies this contract exactly — correct node name, `extras`, and a `_CONFIDENCE`
attribute exercising all three confidence levels. `generators/placeholder.py` emits one. A placeholder
that does not satisfy the contract is worse than none, because it lets the renderer develop
against a fiction.
