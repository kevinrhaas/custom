/**
 * buildings.js — GLBs in, one batch per material out, picks resolved to a
 * structure_id.
 *
 * Three things here are contract, not preference:
 *
 *  1. **Placement comes from the sidecar, never from a baked transform**
 *     (docs/GLB-CONTRACT.md). Whatever transform a node carries inside the GLB
 *     is baked *into the geometry* relative to the structure node, and the
 *     instance matrix is then composed purely from `placement.local_e`,
 *     `local_n` and `rotation_deg`. Re-georeferencing a building is a two-number
 *     edit in a JSON file and never a rebake — which matters, because almost
 *     every position in this dataset is still symbolic.
 *
 *  2. **Identity comes from `extras.structure_id`, never from the node name.**
 *     A structure with several materials exports as ONE node with SEVERAL child
 *     meshes, because a glTF primitive cannot span materials. `extras` lands on
 *     the parent; the children carry empty `userData`. So identity is resolved
 *     by walking *up* the ancestors, and a raycast is resolved through a batch
 *     id we recorded when we built the batch.
 *
 *  3. **One material per batch, and the batch does not care what colour the
 *     building is.** `BatchedMesh` renders one material, so the buildings become
 *     one batch per distinct material. Materials identical in every rendered
 *     respect are collapsed, and BASE COLOUR IS CARRIED PER VERTEX rather than
 *     per material (see `materialKey`), so two walls that differ only in paint
 *     share a draw call. The five materials of one tavern become a handful of
 *     draw calls and the five materials of a hundred taverns still do.
 */

import * as THREE from 'three';
import { enuToWorld, bearingToYaw, toFloatAttribute } from './terrain.js';

/** Walk up until something claims a structure_id. Returns null if nothing does. */
export function structureIdOf(object) {
  for (let o = object; o; o = o.parent) {
    const id = o.userData?.structure_id;
    if (id) return id;
  }
  return null;
}

/** The node inside a loaded glTF that carries this structure's identity. */
function findStructureNode(root, id) {
  let found = null;
  root.traverse((o) => {
    if (!found && o.userData?.structure_id === id) found = o;
  });
  // Fall back to the whole scene: a generator that forgot extras still gets
  // rendered, and the caller reports it rather than dropping the building.
  return found ?? root;
}

/**
 * Everything that renders, in one flat list, with geometry in the frame the
 * structure node SITS IN rather than the frame it defines.
 *
 * The difference is not academic and it broke the whole scene once. Under
 * `KHR_mesh_quantization` — which `tools/bake.sh` asks gltf-transform for, and
 * which is what makes the web derivatives small — positions are stored as
 * integers and the DEQUANTISATION is carried on the node as a translation and a
 * scale (6.25 on the Sauganash, for instance). That transform is part of the
 * encoding, not an authored placement. Taking geometry relative to the node
 * itself inverts it and cancels it out, so every building rendered at about a
 * sixth of its size and the ground sank under the water plane while the walker,
 * which reads the heightfield and not the mesh, went on standing at the right
 * height — a scene that looked flooded and left you floating over it.
 *
 * So: the parent's frame. For an uncompressed file the node is identity and this
 * is exactly what it always was; for a quantised one the node's own transform
 * survives, which is the whole point.
 */
function collectMeshes(structureNode) {
  structureNode.updateWorldMatrix(true, true);
  const frame = structureNode.parent ?? structureNode;
  const toLocal = new THREE.Matrix4().copy(frame.matrixWorld).invert();
  const out = [];
  structureNode.traverse((o) => {
    if (!o.isMesh || !o.geometry) return;
    const rel = new THREE.Matrix4().multiplyMatrices(toLocal, o.matrixWorld);
    out.push({ mesh: o, matrix: rel });
  });
  return out;
}

/**
 * Rewrite a structure's confidence channel so the MASSING answers "was this
 * building here", not "do we know its exact wall height".
 *
 * Those are different questions and the view was answering the wrong one. The
 * Exchange Coffee House is a tavern Andreas names, whose keeper is known and
 * whose corner is described — but nobody wrote down how tall it was, so its
 * wall height is honestly reconstructed, and the shader dithered its walls into
 * translucent massing. Dithering is this project's mark for "we made this up".
 * Applied to a building that demonstrably stood there, it is simply false, and
 * a visitor reads it as doubt about the building rather than about a number.
 *
 * So the structure's OWN existence grade sets the range its parts may occupy:
 *
 *   existence reconstructed  every vertex goes to 1.0 — the whole building
 *                            dithers, walls, roof, trim and chimney together.
 *                            A half-dithered invention with a solid chimney
 *                            reads as a real building with an odd texture.
 *   existence attested       nothing dithers. Attribute uncertainty still shows,
 *   or inferred              tinted, because the card behind the click carries
 *                            the exact per-attribute grade and this is the
 *                            summary, not a replacement for it.
 *
 * Nothing is lost by this: the popup still reports every attribute at its own
 * grade, unclamped. What changes is only what the SHAPE in front of you claims.
 */
function existenceFloor(record) {
  const grade = record?.sidecar?.documented_range?.confidence;
  if (grade === 'reconstructed') return { force: 1.0 };
  if (grade === 'attested' || grade === 'inferred') return { ceiling: 0.5 };
  // No stated existence grade: leave the channel exactly as authored rather
  // than inventing a policy for a case the dataset does not produce.
  return {};
}

function applyExistence(geo, rule) {
  const attr = geo.getAttribute('_confidence');
  if (!attr || (rule.force === undefined && rule.ceiling === undefined)) return;
  const a = attr.array;
  for (let i = 0; i < a.length; i += 1) {
    a[i] = rule.force !== undefined ? rule.force : Math.min(a[i], rule.ceiling);
  }
  attr.needsUpdate = true;
}

/**
 * Reduce a geometry to exactly the attribute set a batch can hold, in a fixed
 * order, indexed. Anything else (tangents, a stray COLOR_0) is dropped: the
 * first geometry added to a BatchedMesh defines the batch's attributes for
 * good, and a later geometry carrying an extra one has it silently ignored.
 * Normalising up front means the batch never depends on load order.
 */
function normalizeGeometry(src, matrix, material, confidence, label) {
  const geo = new THREE.BufferGeometry();
  const position = src.getAttribute('position');
  if (!position) throw new Error(`${label}: geometry has no POSITION`);

  geo.setAttribute('position', toFloatAttribute(position, 3));
  geo.setAttribute('color', albedoAttribute(material, position.count));
  geo.setAttribute('normal', src.getAttribute('normal')
    ? toFloatAttribute(src.getAttribute('normal'), 3)
    : new THREE.BufferAttribute(new Float32Array(position.count * 3), 3));
  geo.setAttribute('uv', src.getAttribute('uv')
    ? toFloatAttribute(src.getAttribute('uv'), 2)
    : new THREE.BufferAttribute(new Float32Array(position.count * 2), 2));

  const conf = src.getAttribute('_confidence');
  if (conf) geo.setAttribute('_confidence', toFloatAttribute(conf, conf.itemSize));

  geo.setIndex(src.getIndex()
    ? src.getIndex().clone()
    : new THREE.BufferAttribute(
        new Uint32Array(position.count).map((_, i) => i), 1));

  geo.applyMatrix4(matrix);
  if (!src.getAttribute('normal')) geo.computeVertexNormals();

  const warning = confidence.ensureAttribute(geo, label);
  return { geo, warning };
}

/**
 * The material's base colour, written once per vertex.
 *
 * `material.color` is already in the renderer's linear working space (three
 * converts on assignment, and glTF's `baseColorFactor` is linear to begin
 * with), and three's `<color_fragment>` chunk multiplies `diffuseColor.rgb` by
 * the `color` attribute with no colour-space conversion of its own. So copying
 * `.r/.g/.b` straight in and leaving the shared material white is EXACTLY the
 * arithmetic that was happening before — the same product, in a different
 * order. That exactness is the whole licence for this: a documented white wall
 * still renders at the value its record claims, to the bit.
 */
function albedoAttribute(material, count) {
  const c = material?.color;
  const r = c ? c.r : 1, g = c ? c.g : 1, b = c ? c.b : 1;
  const out = new Float32Array(count * 3);
  for (let i = 0; i < count; i += 1) {
    out[i * 3] = r; out[i * 3 + 1] = g; out[i * 3 + 2] = b;
  }
  return new THREE.BufferAttribute(out, 3);
}

/**
 * Two materials that render identically should not cost two draw calls — and
 * COLOUR IS NOT PART OF THE ANSWER, because colour is carried per vertex.
 *
 * This is R-W5a, and the measurement is what makes the case. Every one of the
 * 47 building batches in the 2026-08-15 scene was the same
 * `MeshStandardMaterial`: metalness 0, no map of any kind, `DoubleSide`,
 * opaque, no alpha test, smooth-shaded. The ONLY fields that differed were
 * `color` — 39 distinct values across 47 batches — and `roughness`, which takes
 * 16 values. So the town was paying 47 draw calls to render two numbers, and it
 * paid ANOTHER one every time a block landed carrying a paint colour nothing
 * else in the town used: R-G1 measured exactly +11 draw calls for 19 new roofs,
 * and the straight line over the 399 roofs still to come was about +240 against
 * a budget of 80.
 *
 * Taking `color` out of the key collapses those 47 to 16 and, far more
 * importantly, makes a new roof's paint FREE: a block can land any colour it
 * likes without adding a batch. Roughness is left in the key deliberately — it
 * would need a shader patch to carry per-vertex, and 16 batches is already
 * inside the budget with room. The remaining 16 → 1 is written up under R-W5a
 * in docs/ROADMAP.md with its own numbers.
 *
 * `emissive` stays in the key: nothing in this dataset uses it, and if
 * something ever does, a glowing material is not something to merge silently
 * into a batch of dark ones.
 *
 * Roughness and metalness are compared at THREE DECIMALS, which costs two more
 * batches than it sounds and is not a tolerance dialled by eye. The town is
 * baked by two pipelines: the bespoke masters carry roughness as a float32
 * (`0.8999999761581421`) and the generated infill writes the decimal it
 * authored (`0.9`). Those are the same number to any renderer, and comparing
 * them exactly split the 0.90 and 0.88 buckets in two for no reason a visitor
 * could ever see. Nothing in the dataset uses two roughness values closer than
 * 0.01 on purpose.
 */
function materialKey(m) {
  const near = (v) => (typeof v === 'number' ? v.toFixed(3) : '-');
  return [
    m.type,
    m.emissive?.getHexString() ?? '-',
    near(m.roughness), near(m.metalness),
    m.map?.uuid ?? '-', m.normalMap?.uuid ?? '-', m.aoMap?.uuid ?? '-',
    m.side, m.transparent ? 't' : 'o', m.alphaTest ?? 0, m.flatShading ? 'f' : 's',
  ].join('|');
}

/**
 * @param {object} o
 * @param {Map<string,object>} o.registry   from scene-loader
 * @param {object} o.confidence             from createConfidenceView
 * @param {object} o.terrain                from createTerrain (for ground height)
 */
export function createBuildings({ registry, confidence, terrain }) {
  const group = new THREE.Group();
  group.name = 'structures';
  const problems = [];

  // material key -> { material, entries: [{ record, geo }] }
  const groups = new Map();
  /** structure id -> its footprint extent in its own local frame, so a building
   *  can be stood on the lowest ground UNDER it rather than under its origin.
   *  Filled in the load loop because placement needs it. */
  const localXZ = new Map();
  let totalTris = 0;

  for (const record of registry.values()) {
    if (!record.gltf) continue;
    const node = findStructureNode(record.gltf.scene, record.id);
    record.node = node;
    if (!node.userData?.structure_id) {
      problems.push(`${record.id}: no extras.structure_id anywhere in the GLB — `
        + 'identity fell back to the file it came from');
    }
    if (node.userData?.phase_id && record.sidecar.phase
        && node.userData.phase_id !== record.sidecar.phase) {
      problems.push(`${record.id}: GLB is phase '${node.userData.phase_id}' but the sidecar `
        + `says '${record.sidecar.phase}' — the asset and the record disagree`);
    }

    const meshes = collectMeshes(node);
    if (!meshes.length) {
      problems.push(`${record.id}: the GLB contains no meshes`);
      continue;
    }

    for (const { mesh, matrix } of meshes) {
      const label = `${record.id}/${mesh.name || 'mesh'}`;
      const material = Array.isArray(mesh.material) ? mesh.material[0] : mesh.material;
      let prepared;
      try {
        prepared = normalizeGeometry(mesh.geometry, matrix, material, confidence, label);
        // After the channel exists and is float — see existenceFloor for why the
        // building's own existence grade governs what its parts may claim.
        applyExistence(prepared.geo, existenceFloor(record));
      } catch (err) {
        problems.push(`${label}: ${err.message}`);
        continue;
      }
      if (prepared.warning) problems.push(prepared.warning);

      const key = materialKey(material);
      let bucket = groups.get(key);
      if (!bucket) {
        material.side = material.side ?? THREE.FrontSide;
        // The batch's own colour is now the identity, and every vertex carries
        // its building's paint. Whitening the shared material is what makes the
        // multiply come out unchanged — see albedoAttribute.
        material.vertexColors = true;
        material.color = new THREE.Color(1, 1, 1);
        material.name = `merged-r${(material.roughness ?? 1).toFixed(2)}`;
        confidence.patch(material);
        bucket = { material, entries: [] };
        groups.set(key, bucket);
      }
      bucket.entries.push({ record, geo: prepared.geo });
      totalTris += prepared.geo.getIndex().count / 3;

      // Grow this structure's local footprint as its parts arrive — see
      // groundUnder(), which samples the terrain across it.
      prepared.geo.computeBoundingBox();
      const gb = prepared.geo.boundingBox;
      const seen = localXZ.get(record.id);
      localXZ.set(record.id, seen ? {
        minX: Math.min(seen.minX, gb.min.x), maxX: Math.max(seen.maxX, gb.max.x),
        minZ: Math.min(seen.minZ, gb.min.z), maxZ: Math.max(seen.maxZ, gb.max.z),
      } : { minX: gb.min.x, maxX: gb.max.x, minZ: gb.min.z, maxZ: gb.max.z });
    }
  }

  /**
   * The height to stand a building at: the LOWEST ground under its footprint,
   * not the ground under its origin.
   *
   * A single sample is only right on flat ground. This town is nearly flat, so
   * it was right for 221 of 236 structures and wrong for the fifteen that
   * matter most — the ones on the riverbank and the fort mound, where the whole
   * point is that the land falls away. The Wolf Point Tavern hung 1.84 m in the
   * air on its river side and the fort palisade 2.82 m, and in both cases the
   * gap was almost exactly the relief under the footprint, which is the
   * signature of anchoring at one point on a slope.
   *
   * The minimum is the right choice rather than the mean or the origin. Bedding
   * to the lowest corner buries a little of the uphill side, which is what a
   * sill on a slope actually does and what any builder would have done; the
   * alternative leaves daylight under the downhill wall, which nothing does.
   *
   * The footprint is sampled in the building's own rotated frame, because a
   * long building across a slope and the same building along it meet quite
   * different ground.
   */
  function groundUnder(record, e, n, rotationDeg) {
    if (!terrain) return 0;
    const box = localXZ.get(record.id);
    if (!box) return terrain.surfaceHeight(e, n);
    // Local +x is east and local +z is SOUTH (world -z is north), before the
    // building's own rotation is applied.
    const th = bearingToYaw(rotationDeg);
    const cos = Math.cos(th);
    const sin = Math.sin(th);
    let lowest = Infinity;
    const STEPS = 4;
    for (let i = 0; i <= STEPS; i += 1) {
      const lx = box.minX + ((box.maxX - box.minX) * i) / STEPS;
      for (let j = 0; j <= STEPS; j += 1) {
        const lz = box.minZ + ((box.maxZ - box.minZ) * j) / STEPS;
        const ee = e + lx * cos + lz * sin;
        const nn = n + lx * sin - lz * cos;
        lowest = Math.min(lowest, terrain.surfaceHeight(ee, nn));
      }
    }
    return Number.isFinite(lowest) ? lowest : terrain.surfaceHeight(e, n);
  }

  // Placement matrix per structure, from the sidecar and nothing else.
  const placements = new Map();
  for (const record of registry.values()) {
    const p = record.sidecar?.placement ?? {};
    const e = p.local_e ?? 0;
    const n = p.local_n ?? 0;
    // docs/GLB-CONTRACT.md: a structure sits at the base of its walls on the
    // ground, EXCEPT one declared `water`, whose local y = 0 is the design water
    // surface — that plane is z = 0 by the definition of the vertical datum, so
    // the anchor is a literal zero and not a lookup. Note what the alternative
    // actually does: `terrain.walkHeight()` reports a wading BARRIER over water, not
    // the bed, so a bridge left on the terrain anchor does not sink — it hangs
    // four metres above the river, which is the harder failure to read.
    const onWater = p.vertical_anchor === 'water';
    const y = onWater ? 0 : groundUnder(record, e, n, p.rotation_deg ?? 0);
    placements.set(record.id, new THREE.Matrix4().compose(
      enuToWorld(e, n, y),
      new THREE.Quaternion().setFromEuler(
        new THREE.Euler(0, bearingToYaw(p.rotation_deg ?? 0), 0)),
      new THREE.Vector3(1, 1, 1),
    ));
    if (p.placement_provisional) {
      problems.push(`${record.id}: placement is provisional — `
        + `${p.symbolic_location ?? 'no coordinates yet'}`);
    }
  }

  // Shadows have to agree with the view: a wall you can see through should not
  // cast a solid shadow. The same patch on a depth material dithers the shadow
  // exactly as it dithers the surface, and the depth shader has the same
  // `<clipping_planes_fragment>` anchor to hang the discard on.
  const depthMaterial = confidence.patch(new THREE.MeshDepthMaterial({
    depthPacking: THREE.RGBADepthPacking,
  }));

  const batches = [];
  /** structure id -> its union bounding box, in the structure's own frame. */
  const localBoxes = new Map();
  /** structure id -> the confidence channel the shader will actually read. */
  const channels = new Map();
  for (const [, bucket] of groups) {
    const verts = bucket.entries.reduce((a, e) => a + e.geo.getAttribute('position').count, 0);
    const idx = bucket.entries.reduce((a, e) => a + e.geo.getIndex().count, 0);
    const batch = new THREE.BatchedMesh(bucket.entries.length, verts, idx, bucket.material);
    batch.name = `structures:${bucket.material.name || bucket.material.type}`;
    batch.castShadow = true;
    batch.receiveShadow = true;
    batch.customDepthMaterial = depthMaterial;
    batch.userData.batchIndex = [];

    for (const { record, geo } of bucket.entries) {
      const geometryId = batch.addGeometry(geo);
      const instanceId = batch.addInstance(geometryId);
      batch.setMatrixAt(instanceId, placements.get(record.id));
      batch.userData.batchIndex[instanceId] = record.id;
      record.instanceId = instanceId;
      // Measure BEFORE dispose, and union across every material a structure
      // uses: a building is walls plus roof plus trim, and any one of those
      // alone is not the building. This is what `instanceBounds()` reports and
      // what the size gate reads — see the note on that method.
      geo.computeBoundingBox();
      let box = localBoxes.get(record.id);
      if (!box) { box = new THREE.Box3(); localBoxes.set(record.id, box); }
      box.union(geo.boundingBox);
      // The confidence the SHADER will see, after the existence floor, recorded
      // per structure so a gate can ask the question a visitor asked: does this
      // building dither, and does it dither all over?
      const conf = geo.getAttribute('_confidence');
      if (conf) {
        let seen = channels.get(record.id);
        if (!seen) { seen = { min: Infinity, max: -Infinity, dithered: 0, total: 0 }; channels.set(record.id, seen); }
        for (let i = 0; i < conf.array.length; i += 1) {
          const v = conf.array[i];
          seen.min = Math.min(seen.min, v);
          seen.max = Math.max(seen.max, v);
          seen.total += 1;
          if (v > 0.75) seen.dithered += 1;
        }
      }
      geo.dispose();
    }
    batch.computeBoundingBox();
    batch.computeBoundingSphere();
    group.add(batch);
    batches.push(batch);
  }

  const raycaster = new THREE.Raycaster();
  raycaster.far = 400;

  return {
    group,
    batches,
    problems,
    triangles: totalTris,
    /** Draw calls these buildings cost in the colour pass. */
    get drawCalls() { return batches.length; },

    /**
     * Every structure's rendered size, in metres, keyed by structure id.
     *
     * This exists because the gate that was supposed to catch a broken town
     * measured the TALLEST building in the scene and stopped. That assertion
     * passes with one correct building and two hundred and forty-one collapsed
     * ones, which is exactly the scene that shipped: every wall clamped into a
     * two-metre box by a quantised attribute (see `toFloatAttribute`), while the
     * one uncompressed asset kept the check green.
     *
     * A size is only meaningful against a claim, so this reports the rendered
     * box and leaves the comparison to the caller, which holds the records.
     */
    instanceBounds() {
      const out = {};
      for (const [id, box] of localBoxes) {
        const size = box.getSize(new THREE.Vector3());
        const c = channels.get(id);
        out[id] = {
          size: [size.x, size.y, size.z],
          min: box.min.toArray(),
          max: box.max.toArray(),
          // What the confidence view will show for this building.
          confidence: c ? { min: c.min, max: c.max, ditheredShare: c.dithered / c.total } : null,
        };
      }
      return out;
    },

    /**
     * Raycast into the batches.
     * @param {THREE.Vector2} ndc  normalised device coords, or null for centre
     * @param {THREE.Camera} camera
     */
    pickAt(ndc, camera) {
      raycaster.setFromCamera(ndc ?? new THREE.Vector2(0, 0), camera);
      // The ray reaches as far as you can see, and how far that is depends on
      // how high you are.
      //
      // A fixed 400 m is generous at eye level and short from the air along any
      // shallow sightline: from the aerial anchor at 175 m looking out at -30°,
      // a roof on the far side of the town is past 400 m and simply cannot be
      // picked. Straight down it was never the limit — measured, not assumed:
      // 200 m of altitude at -80° is only ~203 m of ray — so this is not the
      // reason inspecting from the air felt broken. It is a real ceiling on a
      // real sightline, and lifting it costs nothing at eye level, where
      // camera.position.y * 4 stays well under the old constant.
      raycaster.far = Math.max(400, camera.position.y * 4);
      const hits = raycaster.intersectObjects(batches, false);
      if (!hits.length) return null;
      const hit = hits[0];
      const id = hit.object.userData.batchIndex?.[hit.batchId]
        ?? structureIdOf(hit.object);
      if (!id) return null;
      return { id, record: registry.get(id), point: hit.point.clone(), distance: hit.distance };
    },

    /** The instance matrix a structure was placed with — for gates that need to
     *  measure the RENDERED result rather than re-derive it. */
    matrixOf(id) { return placements.get(id) ?? null; },

    /** Where a structure stands, in world space — for framing and popups. */
    positionOf(id) {
      const m = placements.get(id);
      return m ? new THREE.Vector3().setFromMatrixPosition(m) : null;
    },

    dispose() {
      for (const b of batches) {
        b.dispose?.();
        b.geometry.dispose();
      }
      for (const [, bucket] of groups) bucket.material.dispose();
      depthMaterial.dispose();
    },
  };
}
