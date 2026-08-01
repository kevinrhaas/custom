import { Vector3 } from '@babylonjs/core/Maths/math.vector';

import { Renderer } from './core/Renderer';
import { MaterialLibrary } from './core/Materials';
import { Player } from './core/Player';
import { input } from './core/Input';
import { settings } from './core/Settings';
import { audio } from './core/Audio';
import { PerimeterApproach } from './scenes/PerimeterApproach';
import { TheVoid } from './scenes/TheVoid';
import { GameScene } from './scenes/SceneBase';
import { mountHud, setLoadProgress, hideLoader, showLoader, showTouchNotice } from './ui/Hud';

/**
 * Boot.
 *
 * Kept deliberately small: create the renderer, bake materials, build a scene,
 * spawn the player, run. Anything that grows here belongs in a system module.
 */

/**
 * The scene registry.
 *
 * There is no transition system yet — no doors between scenes, no run state,
 * no save. Until there is, `?scene=<id>` is how the built scenes are reachable
 * at all, and it is what the shot harness and the landing page's deep links
 * use. Adding a scene here is the whole integration step.
 */
const SCENES: Record<
  string,
  {
    title: string;
    ambience: 'exterior' | 'corridor' | 'cellblock' | 'tunnel' | 'chamber';
    loadingLine: string;
    make: (
      s: import('@babylonjs/core/scene').Scene,
      r: Renderer,
      m: MaterialLibrary,
    ) => GameScene;
  }
> = {
  perimeter: {
    title: 'Perimeter Approach',
    ambience: 'exterior',
    loadingLine: 'Raising the wall',
    make: (s, r, m) => new PerimeterApproach(s, r, m),
  },
  void: {
    title: 'The Void',
    ambience: 'chamber',
    loadingLine: 'Opening the floor',
    make: (s, r, m) => new TheVoid(s, r, m),
  },
};

declare global {
  interface Window {
    /** The shot harness drives the game through this. */
    __joliet?: {
      ready: boolean;
      scene: GameScene;
      player: Player;
      renderer: Renderer;
      /** Move the camera to a named anchor and settle the frame. */
      gotoAnchor(name: string): Promise<void>;
      stats(): { fps: number; activeMeshes: number; triangles: number };
    };
  }
}

async function boot(): Promise<void> {
  const canvas = document.getElementById('stage') as HTMLCanvasElement;
  if (!canvas) throw new Error('#stage canvas missing');

  mountHud();

  // Bail before downloading and baking anything on a device that cannot play
  // it. `pointer: coarse` with no `hover` is the reliable touch-only signal;
  // a laptop with a touchscreen still reports fine pointer + hover.
  const touchOnly =
    typeof matchMedia === 'function' &&
    matchMedia('(pointer: coarse)').matches &&
    !matchMedia('(hover: hover)').matches;
  if (touchOnly && !new URLSearchParams(location.search).has('force')) {
    showTouchNotice();
    return;
  }

  showLoader('Waking the building');

  const renderer = new Renderer({ canvas, forceWebGL: hasFlag('webgl') });
  await renderer.init();

  setLoadProgress(0.05, 'Mixing paint');
  const mats = new MaterialLibrary(renderer.scene);
  await mats.prewarm((done, total) => {
    setLoadProgress(0.05 + (done / total) * 0.6, 'Weathering surfaces');
  });

  const requested = new URLSearchParams(location.search).get('scene') ?? 'perimeter';
  const entry = SCENES[requested] ?? SCENES.perimeter;

  setLoadProgress(0.7, entry.loadingLine);
  const scene = entry.make(renderer.scene, renderer, mats);
  await scene.build();

  setLoadProgress(0.9, 'Loading the sky');
  await renderer.loadEnvironment('assets/env/night-moonlit-golf_1k.hdr', 0.75);

  const spawn = scene.manifest.spawn;
  const player = new Player(
    renderer.scene,
    renderer,
    new Vector3(...spawn.position),
    spawn.yaw,
  );
  renderer.attachCamera(player.camera);
  // The material library was baked and frozen during the loading screen, before
  // the player's headlamp existed. Frozen materials never recompile, so without
  // this the headlamp lights nothing at all.
  mats.rebindLights();

  input.attach(canvas);
  canvas.addEventListener('click', () => {
    if (!input.locked) input.requestLock();
    // Browsers refuse to start an AudioContext without a gesture, so the
    // first click both locks the pointer and wakes the audio engine.
    void audio.start().then(() => {
      audio.setSpace(entry.ambience);
      audio.startAmbience(entry.ambience);
    });
  });

  // Sound is the whole tension model in a game with no enemies — wire it to
  // the controller's existing hooks rather than polling.
  player.setFootstepHandler((surface, intensity) => audio.footstep(surface, intensity));
  player.setLandHandler((intensity) => audio.land(intensity, player.currentSurface));

  setLoadProgress(1, 'Ready');
  await renderer.scene.whenReadyAsync();
  hideLoader();

  let paused = false;
  renderer.start((dt) => {
    input.update();
    if (input.pressed('pause')) {
      paused = !paused;
      if (paused) input.releaseLock();
    }
    if (paused) return;
    if (input.pressed('flashlight')) player.toggleHeadlamp();
    player.update(dt);
    scene.update(dt, player);
  });

  window.__joliet = {
    ready: true,
    scene,
    player,
    renderer,
    async gotoAnchor(name: string) {
      const a = scene.manifest.anchors.find((x) => x.name === name);
      if (!a) throw new Error(`No anchor "${name}" in ${scene.manifest.id}`);
      // Anchor mode freezes bob/lean/sway so successive iterations differ only
      // by the change under test.
      player.setAnchor(
        new Vector3(...a.position),
        a.rotation[0],
        a.rotation[1],
        a.fov,
      );
      // A teleport is a discontinuity the temporal filter cannot resolve on
      // its own; without this reset the previous anchor stays smeared across
      // the whole frame.
      renderer.resetTAA();
      // Let TAA converge and the shadow cascades settle before the capture.
      // Deliberately NOT driven by requestAnimationFrame: headless browsers
      // throttle rAF for pages they consider hidden, and calling scene.render()
      // by hand here would double-render against the engine's own loop. A plain
      // timer lets the existing render loop settle on its own.
      await new Promise((r) => setTimeout(r, 1500));
    },
    stats() {
      const e = renderer.engine;
      // NOTE: engine._drawCalls.current accumulates across frames rather than
      // resetting per frame, so it reports a monotonically rising number that
      // means nothing. Active mesh count is the honest per-frame proxy — it is
      // the number of meshes that survived culling, which is what actually
      // drives the draw-call count.
      return {
        fps: Math.round(e.getFps()),
        activeMeshes: renderer.scene.getActiveMeshes().length,
        triangles: renderer.scene.getActiveIndices() / 3,
      };
    },
  };
}

function hasFlag(name: string): boolean {
  return new URLSearchParams(location.search).has(name);
}

/** Apply a quality override from the URL, used by the perf harness. */
const q = new URLSearchParams(location.search).get('quality');
if (q === 'low' || q === 'medium' || q === 'high' || q === 'ultra') {
  settings.set('quality', q);
}

boot().catch((err) => {
  console.error(err);
  const ui = document.getElementById('ui');
  if (ui) {
    ui.innerHTML = `<div class="fatal"><h1>The lights did not come on.</h1>
      <p>${String(err instanceof Error ? err.message : err)}</p>
      <p class="hint">This build needs WebGL2. Try a current Chrome, Edge, Firefox or Safari 17+.</p></div>`;
  }
});
