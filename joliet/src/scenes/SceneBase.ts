import { Scene } from '@babylonjs/core/scene';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';

import type { Renderer } from '../core/Renderer';
import type { MaterialLibrary } from '../core/Materials';
import type { Player } from '../core/Player';
import { worldUV, type KitContext } from '../core/Kit';

/** A fixed camera anchor for the screenshot/critic harness. */
export interface ShotAnchor {
  name: string;
  position: [number, number, number];
  /** Yaw, pitch in radians. */
  rotation: [number, number];
  fov?: number;
  note?: string;
}

export interface SceneManifest {
  id: string;
  title: string;
  /** Where the player starts, and which way they face. */
  spawn: { position: [number, number, number]; yaw: number };
  anchors: ShotAnchor[];
}

export abstract class GameScene {
  abstract readonly manifest: SceneManifest;

  protected meshes: Mesh[] = [];

  constructor(
    protected scene: Scene,
    protected renderer: Renderer,
    protected mats: MaterialLibrary,
  ) {}

  /** Build all geometry. Called once. */
  abstract build(): Promise<void> | void;

  /** Per-frame scene logic. */
  update(_dt: number, _player: Player): void {
    /* default: static scene */
  }

  /** The KitContext scenes hand to the architectural builders. */
  protected kit(): KitContext {
    return {
      scene: this.scene,
      register: (mesh, opts = {}) => {
        const { collide = true, cast = true, surface, uvDensity, keepUV } = opts;
        // World-space UVs so texel density is constant across the whole game
        // regardless of how big the object is. See Kit.worldUV.
        if (!keepUV) worldUV(mesh, uvDensity ?? 1 / 3);
        mesh.checkCollisions = collide;
        mesh.receiveShadows = true;
        if (cast) this.renderer.castShadows(mesh);
        if (surface) mesh.metadata = { ...(mesh.metadata ?? {}), surface };
        // Static geometry: freezing the world matrix is a large draw-call win
        // and nothing in this game moves the architecture.
        mesh.freezeWorldMatrix();
        mesh.isPickable = collide;
        this.meshes.push(mesh);
      },
    };
  }

  dispose(): void {
    for (const m of this.meshes) m.dispose();
    this.meshes = [];
  }

  static v(a: [number, number, number]): Vector3 {
    return new Vector3(a[0], a[1], a[2]);
  }
}
