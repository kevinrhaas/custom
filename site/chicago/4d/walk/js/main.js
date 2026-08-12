/**
 * main.js — boot, loop, and the test harness handle.
 *
 *   ?year=1835     which scene (default 1835)
 *   ?anchor=fort   start at a named camera anchor from the scene file
 *   ?data= ?assets=  override where the dataset lives
 *   ?debug=1       print budgets to the console after boot
 *
 * `window.__chicago4d` is the harness handle. `tools/smoke_renderer.mjs` drives
 * the real page through it: it is a view onto the running scene, not a parallel
 * code path, so a test that passes means the thing a visitor loads works.
 */

import * as THREE from 'three';

import { loadScene, resolveBases } from './scene-loader.js';
import { createWorld } from './world.js';
import { createTerrain, enuToWorld } from './terrain.js';
import { createBuildings } from './buildings.js';
import { createConfidenceView } from './confidence.js';
import { createIntent, createBackendSwitch } from './controls/intent.js';
import { createPointerLockBackend } from './controls/pointerlock.js';
import { createTouchBackend, prefersTouch } from './controls/touch.js';
import { createWalker, footprintsFrom, WALK } from './walker.js';
import { createFlora } from './flora.js';
import { createTrees } from './trees.js';
import { createPopup } from './popup.js';
import { createHud } from './hud.js';
import { createNavigation } from './navigation.js';
import { createStreets } from './streets.js';
import { mountExclusions } from './exclusions.js';
import { mountGround } from './ground.js';
import { mountLiberties } from './liberties.js';

const VERSION = '0.1.0';
const BUDGET = { drawCalls: 80, triangles: 600000 };

const params = new URLSearchParams(location.search);
const YEAR = (params.get('year') || '1835').replace(/[^0-9a-z_-]/gi, '');
const DEBUG = params.get('debug') === '1';

const canvas = document.getElementById('view');
const gate = document.getElementById('gate');
const gateBtn = document.getElementById('gate-btn');
const gateSub = document.getElementById('gate-sub');
const hudRoot = document.getElementById('hud');
const popupRoot = document.getElementById('popup');

const problems = [];

/** The harness handle. Populated as boot proceeds so a failure is still legible. */
const api = {
  version: VERSION,
  three: THREE.REVISION,
  year: YEAR,
  ready: false,
  error: null,
  scene: null,
  datum: null,
  registry: new Map(),
  player: { e: 0, n: 0, y: 0, bearingDeg: 0, pitchDeg: 0, speed: 0, moving: false,
            altitude: 0, flying: false },
  problems,
  budget: BUDGET,
};
window.__chicago4d = api;

boot().catch((err) => {
  api.error = String(err?.message || err);
  problems.push(`boot: ${api.error}`);
  if (gateSub) gateSub.textContent = `Could not load the scene — ${api.error}`;
  if (gateBtn) gateBtn.textContent = 'Failed to load';
  console.error('[4D Chicago] boot failed', err);
});

async function boot() {
  const bases = resolveBases();
  const coarse = prefersTouch();

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: !coarse,
    powerPreference: 'high-performance',
    stencil: false,
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, coarse ? 1.5 : 2));

  const scene3d = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 3000);

  const loaded = await loadScene(YEAR, bases);
  problems.push(...loaded.problems);
  api.scene = loaded.scene;
  api.datum = loaded.datum;
  api.registry = loaded.registry;

  const world = createWorld({
    renderer, scene: scene3d, sceneJson: loaded.scene, datum: loaded.datum, lowSpec: coarse,
  });

  const confidence = createConfidenceView();

  // The ground, the river, and the heightfield the walker stands on, all from
  // the scene's terrain epoch. Awaited: everything after this asks it how high
  // the ground is, and a flat answer would place every building at the datum.
  const terrain = await createTerrain({
    dataBase: bases.dataBase,
    assetBase: bases.assetBase,
    epochId: loaded.scene.terrain_epoch,
    confidence,
    problems,
  });
  scene3d.add(terrain.group);

  const buildings = createBuildings({ registry: loaded.registry, confidence, terrain });
  problems.push(...buildings.problems);
  scene3d.add(buildings.group);

  const footprints = footprintsFrom(loaded.registry);
  const spawn = anchorFor(loaded.scene, params.get('anchor')) ?? loaded.scene.spawn ?? {};
  const walker = createWalker({ camera, terrain, footprints, spawn });
  walker.apply();

  // The dated street layer is a skin on the heightfield, never a replacement
  // for it.  Mount it before vegetation so the travelled strips can clear only
  // the plants that would otherwise grow through the visible wagon tracks.
  const streets = createStreets({
    terrain,
    records: loaded.index?.streets ?? [],
    confidence,
  });
  scene3d.add(streets.group);

  // ---- vegetation ------------------------------------------------------- //
  // Awaited, like the terrain and for the same reason: the sward is what the
  // ground looks like from standing height, and a walkthrough that opened its
  // gate onto a bare plane and grew a prairie a second later would be showing
  // the visitor a loading state and calling it 1835. Missing records degrade to
  // NOTHING planted plus a recorded problem — never to an invented community.
  const flora = await createFlora({
    dataBase: bases.dataBase, terrain, footprints,
    growthBlocked: streets.blocksGrowth,
    confidence, problems, lowSpec: coarse,
  });
  scene3d.add(flora.group);
  const trees = await createTrees({
    dataBase: bases.dataBase, terrain, footprints,
    growthBlocked: streets.blocksGrowth,
    confidence, problems, lowSpec: coarse,
  });
  scene3d.add(trees.group);

  const popup = createPopup(popupRoot, { docBase: bases.dev ? '../../' : '../' });
  const navigation = createNavigation({
    root: hudRoot, terrain, registry: loaded.registry, streets,
  });
  const hud = createHud({
    root: hudRoot,
    scene: loaded.scene,
    registry: loaded.registry,
    intersections: loaded.index?.intersections ?? [],
    isTouch: prefersTouch(),
    onConfidence: (on) => confidence.set(on),
    onFly: (on) => { intent.flying = !!on; },
    onGoTo: (target) => goToTarget(target),
    onSetting: (key, value) => {
      if (key === 'speed') {
        // Keep the run multiplier the walker was tuned with rather than pinning
        // a fixed run speed, so the two stay in proportion at any setting.
        WALK.speed = value;
        WALK.sprintSpeed = value * 2.28;
      } else if (key === 'fov') {
        camera.fov = value;
        camera.updateProjectionMatrix();
      } else if (key === 'quality') {
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, value));
      } else if (key === 'compass') {
        navigation.setCompassVisible(value);
      } else if (key === 'overviewMap') {
        navigation.setMapVisible(value);
      } else if (key === 'streetNames') {
        navigation.setStreetVisible(value);
      }
    },
  });

  // The liberties the scene takes, in the Evidence panel. Awaited rather than
  // fired and forgotten: it is one small JSON, and a visitor who opens the panel
  // in the first second should not find it empty. A failure here degrades the
  // panel and records a problem; it does not stop the walkthrough.
  api.liberties = await mountLiberties({
    mount: document.getElementById('liberties'),
    noteMount: document.getElementById('liberties-note'),
    dataBase: bases.dataBase,
    registry: loaded.registry,
    problems,
  });
  // The same list, filtered to the building being inspected, in the provenance
  // popup. One fetch feeds both views: the panel says what the scene made up,
  // the card says what THIS building made up, and neither can drift from the
  // markdown they are both quoting.
  popup.setLiberties(api.liberties.liberties);

  // And what the GROUND claims, which no building can carry either: the surface
  // every one of them stands on is graded as carefully as they are, and said so
  // nowhere a visitor could read it.
  api.ground = await mountGround({
    mount: document.getElementById('ground'),
    dataBase: bases.dataBase,
    sceneId: loaded.scene.id ?? YEAR,
    problems,
  });

  // And what was researched and left out, which no building can carry because
  // the buildings that would carry it are the ones not standing here.
  // …and the third category, which neither of those can hold: researched, and
  // still open. One of the four is standing in the scene, so it cannot go on the
  // not-here list without that list becoming false.
  api.exclusions = await mountExclusions({
    mount: document.getElementById('exclusions'),
    uncertainMount: document.getElementById('uncertain'),
    // …and what each of the two lists says it is, in the compiled document's own
    // words rather than a paraphrase typed into the markup beside it.
    standardMount: document.getElementById('exclusions-note'),
    uncertainStandardMount: document.getElementById('uncertain-note'),
    dataBase: bases.dataBase,
    sceneId: loaded.scene.id ?? YEAR,
    problems,
  });
  // And the open questions again, filtered to the building being inspected —
  // exactly as the liberties are, and for the same reason. One of the four is
  // standing in the scene, and the panel's entry for it promises that the
  // provenance card shows the claim carrying the doubt; the card is where a
  // visitor who walked up to that building would think to ask.
  popup.setOpenQuestions(api.exclusions.uncertain);

  // Apply the visitor's stored settings before the first frame, so nothing
  // visibly snaps a moment after load.
  WALK.speed = hud.settings.speed;
  WALK.sprintSpeed = hud.settings.speed * 2.28;
  camera.fov = hud.settings.fov;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, hud.settings.quality));
  navigation.setCompassVisible(hud.settings.compass);
  navigation.setMapVisible(hud.settings.overviewMap);
  navigation.setStreetVisible(hud.settings.streetNames);

  // ---- input ------------------------------------------------------------ //

  const intent = createIntent();
  const backends = createBackendSwitch(intent);

  const pointerlock = createPointerLockBackend({
    intent,
    domElement: canvas,
    onLockChange: (locked) => {
      hud.setLocked(locked);
      if (!locked) hud.say('Pointer released — click the view to look around again');
    },
  });

  const touch = createTouchBackend({
    intent,
    domElement: canvas,
    ui: {
      layer: document.getElementById('touch-layer'),
      stick: document.getElementById('stick'),
      knob: document.getElementById('stick-knob'),
      risePad: document.getElementById('rise-pad'),
      riseUp: document.getElementById('rise-up'),
      riseDown: document.getElementById('rise-down'),
    },
    onViewport: () => resize(),
  });

  let gateOpen = true;

  // Exactly one backend is live. Whichever device the visitor actually uses
  // wins, switched by the first real event of that kind — a laptop with a
  // touchscreen must not end up driving both.
  backends.activate(coarse ? touch : pointerlock);
  window.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'touch') backends.activate(touch);
    else if (e.pointerType === 'mouse') backends.activate(pointerlock);
  }, { capture: true });
  window.addEventListener('keydown', (e) => {
    if (!e.metaKey && !e.ctrlKey) backends.activate(pointerlock);
  }, { capture: true });

  canvas.addEventListener('click', () => {
    if (backends.active === pointerlock && !pointerlock.isLocked && !gateOpen) pointerlock.lock();
  });

  // ---- picking ---------------------------------------------------------- //

  function inspect(ndc = null) {
    const hit = buildings.pickAt(ndc, camera);
    if (!hit) {
      popup.close();
      hud.say('Nothing there — aim at a building');
      return null;
    }
    popup.show(hit.record);
    return hit;
  }

  /** Programmatic pick: by structure_id, by NDC point, or down the crosshair. */
  function pick(target) {
    if (typeof target === 'string') {
      const record = loaded.registry.get(target);
      if (!record) return null;
      return popup.show(record) ? { id: target, record } : null;
    }
    if (target && typeof target.x === 'number' && typeof target.y === 'number') {
      return inspect(new THREE.Vector2(target.x, target.y));
    }
    return inspect(null);
  }

  /** Stand back and look at a structure — used by anchors and by the harness. */
  function frame(id, distance = 26) {
    const point = focusPoint(id);
    if (!point) return false;
    walker.lookAt(point, distance);
    return true;
  }

  function focusPoint(id) {
    const fp = footprints.find((f) => f.id === id);
    const record = loaded.registry.get(id);
    let e; let n;
    if (fp) {
      e = fp.pts.reduce((a, p) => a + p[0], 0) / fp.pts.length;
      n = fp.pts.reduce((a, p) => a + p[1], 0) / fp.pts.length;
    } else {
      const p = record?.sidecar?.placement;
      if (!p) return null;
      e = p.local_e ?? 0;
      n = p.local_n ?? 0;
    }
    const wallH = record?.sidecar?.attributes?.wall_height_m?.value ?? 5;
    return enuToWorld(e, n, terrain.height(e, n) + wallH * 0.55);
  }

  /** One route for the complete search: frame a structure, stand at a verified
   * intersection, or use one of the authored scene viewpoints. */
  function goToTarget(target) {
    if (!target?.kind) return false;
    if (target.kind === 'anchor') return api.goTo?.(target.id) ?? false;
    hud.setFly(false, { announce: false });
    walker.setFlying(false);
    if (target.kind === 'structure') return frame(target.id);
    if (target.kind === 'intersection'
        && Number.isFinite(target.local_e) && Number.isFinite(target.local_n)) {
      walker.teleport({
        local_e: target.local_e, local_n: target.local_n, yaw_deg: 0,
      });
      return true;
    }
    return false;
  }

  // ---- gate ------------------------------------------------------------- //

  function openWorld() {
    if (!gateOpen) return;
    gateOpen = false;
    gate?.setAttribute('hidden', '');
    hud.show();
    hud.restore();
    // The gate doubles as the audio-unlock gesture: browsers only allow an
    // AudioContext to start from one, and ambience lands in a later slice.
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (Ctx && !api.audio) { api.audio = new Ctx(); api.audio.resume?.(); }
    } catch { /* no audio is fine; a thrown error is not */ }
    if (backends.active === pointerlock) pointerlock.lock();
    hud.say(backends.name === 'touch'
      ? 'Left thumb walks · drag the right side to look · tap a building'
      : 'W A S D to walk · E to inspect what you are looking at');
  }
  gateBtn?.addEventListener('click', openWorld);

  // ---- resize ----------------------------------------------------------- //

  function resize() {
    const vv = window.visualViewport;
    const w = Math.max(1, Math.round(vv?.width ?? window.innerWidth));
    const h = Math.max(1, Math.round(vv?.height ?? window.innerHeight));
    renderer.setSize(w, h, true);
    camera.aspect = w / h;
    // Hor+ : hold the horizontal field of view and let the vertical follow, so a
    // portrait phone does not end up looking down a drinking straw.
    const hFov = 76 * Math.PI / 180;
    const vFov = 2 * Math.atan(Math.tan(hFov / 2) / camera.aspect);
    camera.fov = THREE.MathUtils.clamp(vFov * 180 / Math.PI, 55, 94);
    camera.updateProjectionMatrix();
    document.documentElement.style.setProperty('--vh', `${h}px`);
  }
  window.addEventListener('resize', resize);
  window.addEventListener('orientationchange', resize);
  window.visualViewport?.addEventListener('resize', resize);
  resize();

  // ---- loop ------------------------------------------------------------- //

  const clock = new THREE.Clock();
  let frames = 0;
  let fpsMark = performance.now();
  let fps = 0;
  /** Set by capture(); read back at the end of the frame it asked for. */
  let pendingCapture = null;

  function tick() {
    // Keep visual simulation stable, but do not make a visitor crawl in direct
    // proportion to a slow renderer. At 2 fps the former 0.05 s clamp advanced
    // walking by only 0.10 s per real second. Movement now consumes up to a
    // quarter-second of real frame time in <= 0.05 s collision/terrain steps.
    const frameDt = Math.min(clock.getDelta(), 0.25);
    const dt = Math.min(frameDt, 0.05);

    backends.active?.update?.(dt);
    terrain.update(dt);
    const asked = intent.takeInteract();
    if (asked) inspect(asked.point ? new THREE.Vector2(asked.point.x, asked.point.y) : null);
    const walkSteps = Math.max(1, Math.ceil(frameDt / 0.05));
    const walkDt = frameDt / walkSteps;
    for (let i = 0; i < walkSteps; i++) walker.update(walkDt, intent);
    world.follow(camera.position);
    flora.update(dt, camera);
    trees.update(dt, camera);

    renderer.render(scene3d, camera);

    // Read back inside the frame that drew it. Outside the loop the drawing
    // buffer has already been composited and cleared, and readPixels quietly
    // returns the PREVIOUS frame — which makes a toggle look like it changed
    // nothing at all.
    if (pendingCapture) {
      const { grid, resolve } = pendingCapture;
      pendingCapture = null;
      resolve(readbackSignature(renderer, grid));
    }

    const st = walker.state;
    api.player.e = st.e;
    api.player.n = st.n;
    api.player.y = st.eyeY;
    api.player.bearingDeg = walker.bearingDeg;
    api.player.pitchDeg = st.pitch * 180 / Math.PI;
    api.player.speed = st.speed;
    api.player.moving = st.speed > 0.001;
    api.player.altitude = st.altitude;
    api.player.flying = st.flying;
    hud.setAltitude(st.altitude);
    navigation.update({ e: st.e, n: st.n, bearingDeg: walker.bearingDeg });

    // Wall-clock, not the clamped dt: a clamped dt reports a healthy 20 fps on
    // a machine that is actually drawing three frames a second.
    frames++;
    const now = performance.now();
    if (now - fpsMark >= 500) {
      fps = (frames * 1000) / (now - fpsMark);
      frames = 0;
      fpsMark = now;
    }
  }
  renderer.setAnimationLoop(tick);

  // ---- harness ---------------------------------------------------------- //

  Object.assign(api, {
    renderer, camera, scene3d, world, terrain, buildings, walker, intent, popup, hud,
    backends, streets, flora, trees, navigation,
    setConfidenceView(on) { return hud.setConfidence(!!on, { announce: false }); },
    setFly(on) { return hud.setFly(!!on, { announce: false }); },
    get flying() { return walker.state.flying; },
    get altitude() { return walker.state.altitude; },
    pick,
    frame,
    goToTarget,
    goTo(anchorId) {
      const a = anchorFor(loaded.scene, anchorId);
      if (!a) return false;
      // Set the MODE through the HUD, not on the walker: intent.flying is the
      // one master, and a walker flipped directly would be reverted on the very
      // next frame when update() reconciled it against an intent still reading
      // false. The HUD's setter is what writes the intent.
      const aerial = typeof a.altitude_m === 'number';
      hud.setFly(aerial, { announce: false });
      walker.teleport({
        local_e: a.local_e,
        local_n: a.local_n,
        yaw_deg: a.yaw_deg,
        altitude_m: aerial ? a.altitude_m : null,
        pitch_deg: typeof a.pitch_deg === 'number' ? a.pitch_deg : null,
      });
      return true;
    },
    stats() {
      const info = renderer.info;
      return {
        drawCalls: info.render.calls,
        triangles: info.render.triangles,
        programs: info.programs?.length ?? 0,
        geometries: info.memory.geometries,
        textures: info.memory.textures,
        batches: buildings.batches.length,
        structures: loaded.registry.size,
        bytes: loaded.bytes,
        fps: Math.round(fps),
        budget: BUDGET,
        withinBudget: info.render.calls <= BUDGET.drawCalls
          && info.render.triangles <= BUDGET.triangles,
      };
    },
    /**
     * A pixel signature of the next rendered frame. Resolves from inside the
     * render loop, so it always measures a frame that includes whatever you
     * just changed — and it needs no `preserveDrawingBuffer`, which means the
     * test measures the same renderer configuration a visitor gets.
     */
    capture(grid = 12) {
      return new Promise((resolve, reject) => {
        pendingCapture = { grid, resolve };
        setTimeout(() => {
          if (pendingCapture?.resolve === resolve) {
            pendingCapture = null;
            reject(new Error('capture: no frame rendered within 10 s'));
          }
        }, 10000);
      });
    },
    /** Force one frame — for tests that must not race the animation loop. */
    step() { tick(); },
    walkBudget: WALK,
  });

  // Live getters, defined rather than assigned: Object.assign COPIES the value
  // a getter returns at assignment time, which would have frozen these at their
  // boot-time answer and made every later reading wrong.
  Object.defineProperties(api, {
    confidenceView: { get: () => confidence.enabled, enumerable: true },
    controlBackend: { get: () => backends.name, enumerable: true },
    footprints: { get: () => footprints, enumerable: false },
  });

  api.ready = true;
  if (gateBtn) { gateBtn.disabled = false; gateBtn.textContent = 'Tap to walk'; }
  if (gateSub) {
    const n = loaded.registry.size;
    gateSub.textContent = `${n} structure${n === 1 ? '' : 's'} · ${world.describe()}`;
  }

  if (DEBUG) {
    console.info('[4D Chicago]', api.stats(), world.describe());
    if (problems.length) console.warn('[4D Chicago] problems:\n - ' + problems.join('\n - '));
  }
}

/**
 * Reduce the current drawing buffer to a small comparable signature: a mean, a
 * lit fraction, and a coarse grid of cell luminances. Small enough to hand back
 * over a debug protocol, specific enough that a shader change moves it.
 */
function readbackSignature(renderer, grid) {
  const gl = renderer.getContext();
  const w = renderer.domElement.width;
  const h = renderer.domElement.height;
  const px = new Uint8Array(w * h * 4);
  gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);

  const cells = new Array(grid * grid).fill(0);
  const counts = new Array(grid * grid).fill(0);
  let sum = 0;
  let lit = 0;
  let n = 0;
  for (let y = 0; y < h; y += 2) {
    const row = Math.min(grid - 1, ((h - 1 - y) * grid / h) | 0);   // readPixels is bottom-up
    for (let x = 0; x < w; x += 2) {
      const i = (y * w + x) * 4;
      const lum = 0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2];
      sum += lum;
      n++;
      if (lum > 8) lit++;
      const c = row * grid + Math.min(grid - 1, (x * grid / w) | 0);
      cells[c] += lum;
      counts[c]++;
    }
  }
  return {
    width: w,
    height: h,
    mean: sum / (n || 1),
    litFraction: lit / (n || 1),
    cells: cells.map((v, i) => Math.round(v / (counts[i] || 1))),
  };
}

/** Look up a named camera anchor in the scene file. */
function anchorFor(scene, id) {
  if (!id || !Array.isArray(scene?.anchors)) return null;
  return scene.anchors.find((a) => a.id === id) ?? null;
}
