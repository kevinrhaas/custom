import { Engine } from '@babylonjs/core/Engines/engine';
import { WebGPUEngine } from '@babylonjs/core/Engines/webgpuEngine';
import type { AbstractEngine } from '@babylonjs/core/Engines/abstractEngine';
import { Scene } from '@babylonjs/core/scene';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { DefaultRenderingPipeline } from '@babylonjs/core/PostProcesses/RenderPipeline/Pipelines/defaultRenderingPipeline';
import { SSAO2RenderingPipeline } from '@babylonjs/core/PostProcesses/RenderPipeline/Pipelines/ssao2RenderingPipeline';
import { TAARenderingPipeline } from '@babylonjs/core/PostProcesses/RenderPipeline/Pipelines/taaRenderingPipeline';
import { MotionBlurPostProcess } from '@babylonjs/core/PostProcesses/motionBlurPostProcess';
import { ImageProcessingConfiguration } from '@babylonjs/core/Materials/imageProcessingConfiguration';
import { DirectionalLight } from '@babylonjs/core/Lights/directionalLight';
import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight';
import { CascadedShadowGenerator } from '@babylonjs/core/Lights/Shadows/cascadedShadowGenerator';
import { CubeTexture } from '@babylonjs/core/Materials/Textures/cubeTexture';
import { HDRCubeTexture } from '@babylonjs/core/Materials/Textures/hdrCubeTexture';
import type { Camera } from '@babylonjs/core/Cameras/camera';

// Engine extensions are SIDE-EFFECT imports that graft methods onto the engine
// prototype. Tree-shaking drops anything not explicitly imported, so without
// these the method simply does not exist at runtime — which is how iOS Chrome
// (WebKit) died on `createMultipleRenderTarget is not a function` while desktop
// Chrome happened to pull it in transitively. Every post-process that needs a
// G-buffer or a prepass depends on multiRender.
import '@babylonjs/core/Engines/Extensions/engine.multiRender';
import '@babylonjs/core/Engines/Extensions/engine.renderTarget';
import '@babylonjs/core/Engines/Extensions/engine.renderTargetTexture';
import '@babylonjs/core/Engines/Extensions/engine.rawTexture';
import '@babylonjs/core/Engines/Extensions/engine.dynamicTexture';
import '@babylonjs/core/Engines/Extensions/engine.cubeTexture';

import '@babylonjs/core/Rendering/depthRendererSceneComponent';
import '@babylonjs/core/Rendering/geometryBufferRendererSceneComponent';
import '@babylonjs/core/Rendering/prePassRendererSceneComponent';
import '@babylonjs/core/Materials/Textures/Loaders/envTextureLoader';
import '@babylonjs/core/Lights/Shadows/shadowGeneratorSceneComponent';
import '@babylonjs/core/Helpers/sceneHelpers';

import { settings, profile, type QualityProfile } from './Settings';
import { C } from './Palette';

/**
 * The renderer owns the engine, the scene, and the whole post chain.
 *
 * Art direction target (docs/ART-BIBLE.md): a moonlit, overcast midnight at a
 * decayed limestone prison. Nearly everything the player sees is lit by three
 * sources — a low cool moon key, a warm sodium spill from the two surviving
 * yard poles, and the headlamp on the player's own head. Everything else is
 * bounce and sky. The post chain is deliberately restrained: this is a real
 * place, not a music video.
 */

export interface RendererOptions {
  canvas: HTMLCanvasElement;
  /** Force WebGL2 even where WebGPU is available (the shot harness does). */
  forceWebGL?: boolean;
}

export class Renderer {
  engine!: AbstractEngine;
  scene!: Scene;
  pipeline!: DefaultRenderingPipeline;
  ssao?: SSAO2RenderingPipeline;
  taa?: TAARenderingPipeline;
  motionBlur?: MotionBlurPostProcess;

  /** The moon. Key light and the only shadow caster at full strength. */
  moon!: DirectionalLight;
  /** Sky bounce. Keeps the shadow side from going pure black. */
  sky!: HemisphericLight;
  shadows!: CascadedShadowGenerator;

  private canvas: HTMLCanvasElement;
  private camera: Camera | null = null;
  private unsubSettings: (() => void) | null = null;
  private disposed = false;

  constructor(private opts: RendererOptions) {
    this.canvas = opts.canvas;
  }

  async init(): Promise<void> {
    this.engine = await this.createEngine();
    this.scene = new Scene(this.engine);

    // Midnight overcast. Not black — an overcast city sky bounces a lot of
    // light, and pure black reads as "unfinished" rather than "dark".
    this.scene.clearColor = new Color4(0.021, 0.028, 0.042, 1);
    this.scene.ambientColor = new Color3(0.05, 0.06, 0.085);

    // Exponential height fog: the site sits in a river valley and holds mist.
    this.scene.fogMode = Scene.FOGMODE_EXP2;
    this.scene.fogDensity = 0.0125;
    this.scene.fogColor = new Color3(0.055, 0.068, 0.092);

    this.scene.imageProcessingConfiguration.toneMappingEnabled = true;
    this.scene.imageProcessingConfiguration.toneMappingType =
      ImageProcessingConfiguration.TONEMAPPING_ACES;
    this.scene.imageProcessingConfiguration.exposure = 1.45;
    this.scene.imageProcessingConfiguration.contrast = 1.12;

    this.setupLights();
    this.applyProfile(profile());

    this.unsubSettings = settings.subscribe(() => this.applyProfile(profile()));
    addEventListener('resize', this.onResize);

    return;
  }

  /** WebGPU where available, WebGL2 everywhere else. */
  private async createEngine(): Promise<AbstractEngine> {
    const wantGPU =
      !this.opts.forceWebGL &&
      typeof navigator !== 'undefined' &&
      'gpu' in navigator;

    if (wantGPU) {
      try {
        const e = new WebGPUEngine(this.canvas, {
          antialias: true,
          stencil: true,
          adaptToDeviceRatio: true,
        });
        await e.initAsync();
        return e;
      } catch {
        // Fall through to WebGL2 — never leave the player with a black page
        // because a WebGPU adapter misbehaved.
      }
    }

    return new Engine(this.canvas, true, {
      preserveDrawingBuffer: true, // the shot harness reads back the canvas
      stencil: true,
      antialias: true,
      powerPreference: 'high-performance',
      failIfMajorPerformanceCaveat: false,
    });
  }

  private setupLights(): void {
    // Moon: low in the west-north-west, raking across the limestone so the
    // rustication reads. A high moon flattens the stone and kills the frame.
    this.moon = new DirectionalLight('moon', new Vector3(0.55, -0.42, 0.72), this.scene);
    // PBR intensity, not a 0-1 dial. At 1.35 the limestone rendered nearly
    // black; a convincing "bright moon on pale stone" needs an order more.
    this.moon.intensity = 4.6;
    this.moon.diffuse = C.moonlight.scale(0.86).add(new Color3(0.16, 0.13, 0.06));
    this.moon.specular = C.moonlight.scale(0.6);
    this.moon.shadowMinZ = 1;
    this.moon.shadowMaxZ = 180;

    // Sky bounce. Ground bounce is warmer than the sky because it comes off
    // asphalt and dead grass, so the two hemispheres differ.
    this.sky = new HemisphericLight('sky', new Vector3(0, 1, 0), this.scene);
    this.sky.intensity = 0.95;
    this.sky.diffuse = new Color3(0.30, 0.38, 0.58);
    this.sky.groundColor = new Color3(0.19, 0.17, 0.14);
    this.sky.specular = Color3.Black();
  }

  /** (Re)build everything that depends on the quality tier. */
  applyProfile(p: QualityProfile): void {
    const s = settings.get();

    this.engine.setHardwareScalingLevel(
      p.hardwareScale / Math.max(0.5, Math.min(1, s.resolutionScale)),
    );

    this.rebuildShadows(p);
    if (this.camera) this.rebuildPost(this.camera, p);
  }

  private rebuildShadows(p: QualityProfile): void {
    const previous = this.shadows?.getShadowMap()?.renderList?.slice() ?? [];
    this.shadows?.dispose();

    this.shadows = new CascadedShadowGenerator(p.shadowMapSize, this.moon);
    this.shadows.numCascades = p.cascades;
    this.shadows.lambda = 0.88;
    this.shadows.cascadeBlendPercentage = 0.06;
    this.shadows.shadowMaxZ = p.shadowDistance;
    this.shadows.stabilizeCascades = true;
    this.shadows.depthClamp = true;
    this.shadows.autoCalcDepthBounds = true;
    // Contact hardening reads as real contact shadow under the cell doors and
    // where the wall meets the ground. This is the single highest-value
    // shadow setting for the look.
    this.shadows.usePercentageCloserFiltering = true;
    this.shadows.filteringQuality =
      p.shadowMapSize >= 2048
        ? CascadedShadowGenerator.QUALITY_HIGH
        : CascadedShadowGenerator.QUALITY_MEDIUM;
    this.shadows.bias = 0.006;
    this.shadows.normalBias = 0.018;
    this.shadows.darkness = 0.06;
    // Off: alpha-blended meshes casting shadows produced smeared translucent
    // panels across the wall. Nothing in this game needs a glass shadow.
    this.shadows.transparencyShadow = false;

    const list = this.shadows.getShadowMap()?.renderList;
    if (list) list.push(...previous);
  }

  /** Attach the post chain to a camera. Call once the player camera exists. */
  attachCamera(camera: Camera): void {
    this.camera = camera;
    this.scene.activeCamera = camera;
    this.rebuildPost(camera, profile());
  }

  private rebuildPost(camera: Camera, p: QualityProfile): void {
    const s = settings.get();

    this.pipeline?.dispose();
    this.ssao?.dispose();
    this.taa?.dispose();
    this.motionBlur?.dispose();
    this.ssao = undefined;
    this.taa = undefined;
    this.motionBlur = undefined;

    const pipe = new DefaultRenderingPipeline('joliet', true, this.scene, [camera]);
    this.pipeline = pipe;

    // Capability gate. Even with the extensions imported, a device can lack the
    // WebGL2 features these need. A missing effect must degrade the picture,
    // never blank the page.
    const engineAny = this.engine as unknown as {
      createMultipleRenderTarget?: unknown;
      getCaps(): { drawBuffersExtension?: boolean; textureFloatRender?: boolean };
    };
    const caps = this.engine.getCaps();
    const canMRT =
      typeof engineAny.createMultipleRenderTarget === 'function' &&
      caps.drawBuffersExtension !== false;


    // --- Anti-aliasing -----------------------------------------------------
    // TAA above medium, FXAA below. TAA is what makes the barbed wire and the
    // cell bars stop crawling, and those are in almost every frame.
    if (p.shadowMapSize >= 2048 && canMRT) {
      pipe.fxaaEnabled = false;
      try {
        this.taa = new TAARenderingPipeline('taa', this.scene, [camera]);
        this.taa.samples = 8;
        this.taa.factor = 0.06;
        // Reset the history whenever the camera moves. Without this a teleport
        // (which is exactly what the shot harness does) leaves the previous
        // view smeared across the frame permanently — the accumulation buffer
        // has no motion vectors telling it the world jumped.
        this.taa.disableOnCameraMove = true;
      } catch {
        // TAA needs a working prepass; if it fails, FXAA is a fine fallback.
        pipe.fxaaEnabled = true;
      }
    } else {
      pipe.fxaaEnabled = true;
    }
    pipe.samples = 1; // MSAA is redundant with TAA/FXAA and costs bandwidth

    // --- Bloom -------------------------------------------------------------
    // Restrained. The only genuinely bright things at midnight are the sodium
    // lamps and the headlamp hotspot; everything else must NOT glow.
    pipe.bloomEnabled = p.bloom;
    pipe.bloomThreshold = 0.86;
    pipe.bloomWeight = 0.34;
    pipe.bloomKernel = 48;
    pipe.bloomScale = 0.5;

    // --- Tone mapping / grade ---------------------------------------------
    pipe.imageProcessingEnabled = true;
    const ip = pipe.imageProcessing;
    ip.toneMappingEnabled = true;
    ip.toneMappingType = ImageProcessingConfiguration.TONEMAPPING_ACES;
    ip.exposure = 1.45;
    ip.contrast = 1.12;

    ip.vignetteEnabled = s.vignette > 0;
    ip.vignetteWeight = 2.4 * s.vignette;
    ip.vignetteStretch = 0.35;
    ip.vignetteCameraFov = 1.25;
    ip.vignetteColor = new Color4(0.008, 0.011, 0.018, 1);

    // Grain sells the low-light photography read — this is a night shot on a
    // fast sensor, and a perfectly clean night frame looks synthetic.
    pipe.grainEnabled = s.filmGrain > 0;
    pipe.grain.intensity = 9 * s.filmGrain;
    pipe.grain.animated = true;

    pipe.chromaticAberrationEnabled = s.chromaticAberration > 0;
    pipe.chromaticAberration.aberrationAmount = 6.5 * s.chromaticAberration;
    pipe.chromaticAberration.radialIntensity = 0.75;

    // Sharpen slightly to recover the softness TAA + grain introduce.
    pipe.sharpenEnabled = true;
    pipe.sharpen.edgeAmount = 0.22;
    pipe.sharpen.colorAmount = 1;

    // Depth of field stays off during traversal — it fights readability in a
    // dark corridor. Scenes enable it explicitly for scripted looks.
    pipe.depthOfFieldEnabled = false;

    // --- SSAO --------------------------------------------------------------
    // The decayed interiors are almost all soft indirect light; without AO the
    // corners go flat and everything reads as cardboard.
    if (p.ssao && canMRT) {
      try {
        this.ssao = new SSAO2RenderingPipeline('ssao', this.scene, {
          ssaoRatio: p.ssaoRatio,
          blurRatio: 1,
        });
        this.ssao.radius = 1.1;
        this.ssao.totalStrength = 1.15;
        this.ssao.base = 0.06;
        this.ssao.expensiveBlur = p.ssaoRatio >= 0.75;
        this.ssao.samples = p.ssaoRatio >= 0.75 ? 24 : 12;
        this.ssao.maxZ = 60;
        this.scene.postProcessRenderPipelineManager.attachCamerasToRenderPipeline(
          'ssao',
          camera,
        );
      } catch {
        this.ssao = undefined;
      }
    }

    // --- Motion blur -------------------------------------------------------
    // Per-object velocity blur gives movement weight. Off entirely under
    // reduced-motion; that is an accessibility requirement, not a preference.
    if (s.motionBlur > 0 && !s.reducedMotion && canMRT) {
      try {
        this.motionBlur = new MotionBlurPostProcess(
          'motionBlur',
          this.scene,
          1,
          camera,
        );
        this.motionBlur.motionStrength = 0.55 * s.motionBlur;
        this.motionBlur.motionBlurSamples = 12;
        this.motionBlur.isObjectBased = false; // camera-based is far cheaper
      } catch {
        this.motionBlur = undefined;
      }
    }
  }

  /**
   * Load the IBL environment.
   *
   * `.hdr` must go through HDRCubeTexture — `CreateFromPrefilteredData` only
   * accepts an already-prefiltered `.env`/`.dds` and fails *silently* on a raw
   * Radiance file, which costs you all your indirect light and is very hard to
   * spot because the scene still renders. Ask how I know.
   */
  async loadEnvironment(url: string, intensity = 0.35): Promise<void> {
    try {
      const isHDR = /\.hdr(\?|$)/i.test(url);
      const env = isHDR
        ? new HDRCubeTexture(url, this.scene, 128, false, true, false, true)
        : CubeTexture.CreateFromPrefilteredData(url, this.scene);
      env.name = 'env';
      env.gammaSpace = false;
      this.scene.environmentTexture = env;
      this.scene.environmentIntensity = intensity;

      await new Promise<void>((resolve) => {
        if (env.isReady()) return resolve();
        const t = setTimeout(resolve, 8000); // never block boot on the sky
        (env as HDRCubeTexture).onLoadObservable?.addOnce(() => {
          clearTimeout(t);
          resolve();
        });
      });
    } catch {
      // No IBL: the hemispheric light carries a plausible sky term on its own,
      // but the scene will read flatter. Compensate so it is still playable.
      this.scene.environmentIntensity = 0;
      this.sky.intensity = 0.62;
    }
  }

  /** Register a mesh as a shadow caster. */
  castShadows(...meshes: Parameters<CascadedShadowGenerator['addShadowCaster']>[0][]): void {
    for (const m of meshes) this.shadows.addShadowCaster(m, true);
  }

  /**
   * Discard the temporal accumulation buffer. Call after any discontinuous
   * camera move — teleport, anchor change, scene load.
   */
  resetTAA(): void {
    if (!this.taa) return;
    // Re-assigning samples re-initialises the accumulation history.
    const n = this.taa.samples;
    this.taa.samples = 1;
    this.taa.samples = n;
  }

  start(onFrame?: (dtSeconds: number) => void): void {
    this.engine.runRenderLoop(() => {
      if (this.disposed) return;
      const dt = Math.min(this.engine.getDeltaTime() / 1000, 0.1); // clamp hitches
      onFrame?.(dt);
      this.scene.render();
    });
  }

  private onResize = (): void => {
    this.engine.resize();
  };

  dispose(): void {
    this.disposed = true;
    removeEventListener('resize', this.onResize);
    this.unsubSettings?.();
    this.scene?.dispose();
    this.engine?.dispose();
  }
}
