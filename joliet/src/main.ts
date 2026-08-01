import { Vector3 } from '@babylonjs/core/Maths/math.vector';

import { Renderer } from './core/Renderer';
import { MaterialLibrary } from './core/Materials';
import { Player } from './core/Player';
import { input } from './core/Input';
import { settings } from './core/Settings';
import { PerimeterApproach } from './scenes/PerimeterApproach';
import { GameScene } from './scenes/SceneBase';
import { mountHud, setLoadProgress, hideLoader, showLoader } from './ui/Hud';

/**
 * Boot.
 *
 * Kept deliberately small: create the renderer, bake materials, build a scene,
 * spawn the player, run. Anything that grows here belongs in a system module.
 */

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
      stats(): { fps: number; drawCalls: number; triangles: number };
    };
  }
}

async function boot(): Promise<void> {
  const canvas = document.getElementById('stage') as HTMLCanvasElement;
  if (!canvas) throw new Error('#stage canvas missing');

  mountHud();
  showLoader('Waking the building');

  const renderer = new Renderer({ canvas, forceWebGL: hasFlag('webgl') });
  await renderer.init();

  setLoadProgress(0.05, 'Mixing paint');
  const mats = new MaterialLibrary(renderer.scene);
  await mats.prewarm((done, total) => {
    setLoadProgress(0.05 + (done / total) * 0.6, 'Weathering surfaces');
  });

  setLoadProgress(0.7, 'Raising the wall');
  const scene = new PerimeterApproach(renderer.scene, renderer, mats);
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

  input.attach(canvas);
  canvas.addEventListener('click', () => {
    if (!input.locked) input.requestLock();
  });

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
      return {
        fps: Math.round(e.getFps()),
        drawCalls: renderer.scene.getEngine()._drawCalls?.current ?? -1,
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
