/**
 * scene-loader.js — scene JSON -> GLBs + sidecars -> a registry keyed by
 * `structure_id`.
 *
 * The renderer consumes glTF plus JSON sidecars and nothing else
 * (`AGENTS.md` rule 5). It never reaches into `generators/`, never resolves a
 * structure's phases against the scene date, never decides what is documented.
 * All of that has already happened by the time these files exist; here we only
 * fetch, index and hand on.
 *
 * Where the data lives
 * --------------------
 * Two committed layouts, told apart by the page's own path rather than by
 * probing (a probe means a 404 in the network log, and a 404 in the network log
 * means the smoke test cannot tell a healthy boot from a broken one):
 *
 *   dev        renderers/web/index.html   ->  ../../data/   ../../assets/
 *   published  chicago/4d/walk/index.html ->  ../data/      ../data/
 *
 * `?data=` and `?assets=` override either.
 */

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const GLB_MAGIC = 0x46546c67;   // 'glTF', little-endian

export function resolveBases(loc = window.location) {
  const params = new URLSearchParams(loc.search);
  const here = new URL('.', loc.href);
  const dev = /\/renderers\/web\/$/.test(here.pathname);
  return {
    dev,
    dataBase: new URL(params.get('data') ?? (dev ? '../../data/' : '../data/'), here),
    // Published layout puts the web-derivative GLBs at data/gltf/, and sidecar
    // `asset` paths are relative to the data root (see docs/GLB-CONTRACT.md
    // § Paths). In the source tree the same files sit under assets/web/.
    assetBase: new URL(params.get('assets') ?? (dev ? '../../assets/' : '../data/'), here),
  };
}

async function getJSON(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
}

/** Peek at a GLB's JSON chunk without decoding the whole asset. */
function glbHeader(buffer) {
  const dv = new DataView(buffer);
  if (buffer.byteLength < 20 || dv.getUint32(0, true) !== GLB_MAGIC) return null;
  const jsonLength = dv.getUint32(12, true);
  const text = new TextDecoder().decode(new Uint8Array(buffer, 20, jsonLength));
  try { return JSON.parse(text); } catch { return null; }
}

let meshoptPromise = null;
/**
 * `EXT_meshopt_compression` is what the published web derivatives carry
 * (docs/GLB-CONTRACT.md, "Compression"). The decoder is vendored, but importing
 * it instantiates a WebAssembly module, so it is loaded only when an asset
 * actually needs it — an uncompressed master must not pay for it.
 */
export function loadMeshoptDecoder() {
  if (!meshoptPromise) {
    meshoptPromise = import('three/addons/libs/meshopt_decoder.module.js')
      .then((m) => m.MeshoptDecoder);
  }
  return meshoptPromise;
}

/**
 * Load one scene.
 *
 * @returns {Promise<{
 *   year: string, scene: object, datum: object,
 *   registry: Map<string, object>, problems: string[], bytes: number
 * }>}
 */
export async function loadScene(year, bases = resolveBases()) {
  const { dataBase, assetBase } = bases;
  const problems = [];

  const [scene, datum] = await Promise.all([
    getJSON(new URL(`scenes/${year}.json`, dataBase)),
    getJSON(new URL('datum.json', dataBase)),
  ]);

  // Which sidecars belong to this scene. A static host cannot be globbed, so
  // the set has to be published as data. docs/GLB-CONTRACT.md does not specify
  // this file yet — see the Track B report; the shape is deliberately trivial so
  // that compile_scene.py can adopt it without argument.
  const indexUrl = new URL(`sidecars/${year}/index.json`, dataBase);
  let index;
  try {
    index = await getJSON(indexUrl);
  } catch (err) {
    problems.push(`no sidecar index for scene ${year} (${err.message}) — nothing to place`);
    return { year, scene, datum, registry: new Map(), problems, bytes: 0 };
  }

  // The index lists either bare ids or `{ id, sidecar, asset }` rows. Accept
  // both: the compiler and this renderer are being written in parallel, and a
  // loader that dies on the richer shape is a loader that dies on the version
  // that eventually ships.
  const entries = (Array.isArray(index.structures) ? index.structures : [])
    .map((row) => (typeof row === 'string' ? { id: row } : row))
    .filter((row) => row && typeof row.id === 'string');

  const loader = new GLTFLoader();
  const registry = new Map();
  let bytes = 0;

  const loads = entries.map(async ({ id, sidecar: sidecarPath }) => {
    const sidecarUrl = new URL(sidecarPath ?? `sidecars/${year}/${id}.json`, dataBase);
    let sidecar;
    try {
      sidecar = await getJSON(sidecarUrl);
    } catch (err) {
      problems.push(`sidecar ${id}: ${err.message}`);
      return;
    }
    if (sidecar.id !== id) {
      problems.push(`sidecar ${id}: declares id '${sidecar.id}' — index and file disagree`);
    }
    if (sidecar.review_required) {
      // AGENTS.md: review_required blocks a scene from being released. It does
      // not block development, but it must never pass unremarked.
      problems.push(`${id}: review_required is set — this scene cannot be released`);
    }

    const assetUrl = new URL(sidecar.asset, assetBase);
    let gltf = null;
    /**
     * Is the shape you are looking at a bake from the record, or a stand-in?
     *
     * The GLB says so about itself (`asset.extras.placeholder`) and nothing else
     * can: the sidecar is compiled from `data/` alone and never opens a mesh, so
     * a record cannot know which of its bakes is real. The fact is therefore
     * carried from the file it is a fact about to the card that shows it, rather
     * than routed through a sidecar field the compiler would have to invent.
     */
    let assetIsPlaceholder = false;
    try {
      const res = await fetch(assetUrl, { cache: 'no-cache' });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const buffer = await res.arrayBuffer();
      bytes += buffer.byteLength;

      const header = glbHeader(buffer);
      const required = header?.extensionsRequired ?? [];
      if (required.includes('EXT_meshopt_compression')) {
        loader.setMeshoptDecoder(await loadMeshoptDecoder());
      }
      gltf = await new Promise((resolve, reject) => {
        loader.parse(buffer, String(assetUrl), resolve, reject);
      });
      if (header?.asset?.extras?.placeholder) {
        assetIsPlaceholder = true;
        problems.push(`${id}: rendering a PLACEHOLDER asset (${sidecar.asset}) — `
          + 'massing only, not a bake');
      }
    } catch (err) {
      problems.push(`asset ${sidecar.asset}: ${err.message}`);
    }

    registry.set(id, {
      id,
      sidecar,
      gltf,
      assetIsPlaceholder,
      assetUrl: String(assetUrl),
      sidecarUrl: String(sidecarUrl),
      /** filled in by buildings.js once the node is in the batch */
      instanceId: null,
      node: null,
    });
  });

  await Promise.all(loads);
  return { year, scene, datum, registry, problems, bytes, index };
}
