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
 *  3. **One material per batch.** `BatchedMesh` renders one material, so the
 *     buildings become one batch per distinct material. Materials that are
 *     identical in every rendered respect are collapsed first, so the five
 *     materials of one tavern become five draw calls and the five materials of
 *     a hundred taverns still become five draw calls.
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
 * Reduce a geometry to exactly the attribute set a batch can hold, in a fixed
 * order, indexed. Anything else (tangents, a stray COLOR_0) is dropped: the
 * first geometry added to a BatchedMesh defines the batch's attributes for
 * good, and a later geometry carrying an extra one has it silently ignored.
 * Normalising up front means the batch never depends on load order.
 */
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

function normalizeGeometry(src, matrix, confidence, label) {
  const geo = new THREE.BufferGeometry();
  const position = src.getAttribute('position');
  if (!position) throw new Error(`${label}: geometry has no POSITION`);

  geo.setAttribute('position', toFloatAttribute(position, 3));
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

/** Two materials that render identically should not cost two draw calls. */
function materialKey(m) {
  return [
    m.type,
    m.color?.getHexString() ?? '-',
    m.emissive?.getHexString() ?? '-',
    m.roughness ?? '-', m.metalness ?? '-',
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
      let prepared;
      try {
        prepared = normalizeGeometry(mesh.geometry, matrix, confidence, label);
        // After the channel exists and is float — see existenceFloor for why the
        // building's own existence grade governs what its parts may claim.
        applyExistence(prepared.geo, existenceFloor(record));
      } catch (err) {
        problems.push(`${label}: ${err.message}`);
        continue;
      }
      if (prepared.warning) problems.push(prepared.warning);

      const material = Array.isArray(mesh.material) ? mesh.material[0] : mesh.material;
      const key = materialKey(material);
      let bucket = groups.get(key);
      if (!bucket) {
        material.side = material.side ?? THREE.FrontSide;
        confidence.patch(material);
        bucket = { material, entries: [] };
        groups.set(key, bucket);
      }
      bucket.entries.push({ record, geo: prepared.geo });
      totalTris += prepared.geo.getIndex().count / 3;
    }
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
    const y = onWater ? 0 : (terrain ? terrain.surfaceHeight(e, n) : 0);
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
        out[id] = {
          size: [size.x, size.y, size.z],
          min: box.min.toArray(),
          max: box.max.toArray(),
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
      const hits = raycaster.intersectObjects(batches, false);
      if (!hits.length) return null;
      const hit = hits[0];
      const id = hit.object.userData.batchIndex?.[hit.batchId]
        ?? structureIdOf(hit.object);
      if (!id) return null;
      return { id, record: registry.get(id), point: hit.point.clone(), distance: hit.distance };
    },

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
