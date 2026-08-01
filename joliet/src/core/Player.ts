import { Scene } from '@babylonjs/core/scene';
import { UniversalCamera } from '@babylonjs/core/Cameras/universalCamera';
import { Vector3, Quaternion, Matrix } from '@babylonjs/core/Maths/math.vector';
import { Ray } from '@babylonjs/core/Culling/ray';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { MeshBuilder } from '@babylonjs/core/Meshes/meshBuilder';
import { SpotLight } from '@babylonjs/core/Lights/spotLight';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import type { AbstractMesh } from '@babylonjs/core/Meshes/abstractMesh';

import '@babylonjs/core/Collisions/collisionCoordinator';
import '@babylonjs/core/Culling/ray';

import { input } from './Input';
import { settings } from './Settings';
import { C } from './Palette';
import type { Renderer } from './Renderer';

/**
 * First-person character controller.
 *
 * Movement uses Babylon's swept-ellipsoid collide-and-slide rather than a
 * rigid body. For a walking human in a hand-authored level that is both more
 * predictable and cheaper than a physics capsule, and it never tunnels or
 * jitters against the stair geometry — which matters a lot here, because the
 * game is almost entirely stairs, ladders and doorways. Havok is reserved for
 * dynamic props (see Props.ts).
 *
 * Feel targets, tuned against reference and playtested:
 *   walk 1.9 m/s · sprint 4.4 m/s · crouch 1.15 m/s · crawl 0.62 m/s
 * Sprint is deliberately not fast — this is a careful person in the dark with
 * a headlamp, not a soldier.
 */

export type Stance = 'stand' | 'crouch' | 'prone';

export interface SurfaceAudio {
  /** Material tag the footstep system reads: 'concrete' | 'gravel' | ... */
  surface: string;
}

const EYE_STAND = 1.68;
const EYE_CROUCH = 1.06;
const EYE_PRONE = 0.42;

const RADIUS_STAND = 0.34;
const HEIGHT_STAND = 1.8;
const HEIGHT_CROUCH = 1.15;
const HEIGHT_PRONE = 0.55;

const SPEED: Record<Stance, number> = { stand: 1.9, crouch: 1.15, prone: 0.62 };
const SPRINT_SPEED = 4.4;

const GRAVITY = -18.5;
const JUMP_VELOCITY = 5.1;
/** Steps up to this height are climbed without a jump. */
const STEP_HEIGHT = 0.42;

export class Player {
  camera: UniversalCamera;
  /**
   * The collision body. Invisible, never rendered, but it must be a Mesh
   * rather than a TransformNode because collide-and-slide lives on Mesh.
   * Camera is parented to it for head motion.
   */
  root: Mesh;
  headlamp: SpotLight;

  stance: Stance = 'stand';
  grounded = false;
  velocity = new Vector3(0, 0, 0);

  /** 0..1. Drains on sprint, on cold water, on climbing. */
  stamina = 1;
  /** 0..1. Rises in the dark and near hazards; the crew's radio calms it. */
  stress = 0;
  /** 0..1. Headlamp battery. Running it on high burns it faster. */
  battery = 1;

  /** Set by scenes to tag the ground the player is standing on. */
  currentSurface = 'concrete';

  /**
   * Anchor mode. The shot harness pins the camera to a fixed pose and freezes
   * every source of frame-to-frame motion — bob, lean, land-dip, sway — so two
   * iterations of the same anchor differ only by the change under test.
   */
  private anchored = false;

  private yaw = 0;
  private pitch = 0;
  private eyeHeight = EYE_STAND;
  private targetEye = EYE_STAND;
  private bobPhase = 0;
  private bobAmount = 0;
  private leanTarget = 0;
  private lean = 0;
  private stepDistance = 0;
  private landImpulse = 0;
  private headTilt = 0;
  private moveSpeedSmoothed = 0;

  private onFootstep: ((surface: string, intensity: number) => void) | null = null;
  private onLand: ((intensity: number) => void) | null = null;

  constructor(
    private scene: Scene,
    private renderer: Renderer,
    spawn: Vector3,
    spawnYaw = 0,
  ) {
    this.root = MeshBuilder.CreateBox('playerBody', { size: 0.01 }, scene);
    this.root.isVisible = false;
    this.root.isPickable = false;
    // The body must not collide with itself or block its own ground probe.
    this.root.checkCollisions = false;
    this.root.position.copyFrom(spawn);
    this.yaw = spawnYaw;

    this.camera = new UniversalCamera('playerCam', new Vector3(0, EYE_STAND, 0), scene);
    this.camera.parent = this.root;
    this.camera.minZ = 0.06; // close enough to press your face to a cell door
    this.camera.maxZ = 340;
    this.camera.fov = (settings.get().fov * Math.PI) / 180;
    this.camera.rotationQuaternion = Quaternion.Identity();
    // We drive the camera entirely ourselves.
    this.camera.inputs.clear();

    // Collide-and-slide setup on the root.
    this.root.ellipsoid = new Vector3(RADIUS_STAND, HEIGHT_STAND / 2, RADIUS_STAND);
    this.root.ellipsoidOffset = new Vector3(0, HEIGHT_STAND / 2, 0);
    scene.collisionsEnabled = true;

    this.headlamp = this.makeHeadlamp();

    settings.subscribe((s) => {
      this.camera.fov = (s.fov * Math.PI) / 180;
    });
  }

  private makeHeadlamp(): SpotLight {
    const l = new SpotLight(
      'headlamp',
      Vector3.Zero(),
      new Vector3(0, 0, 1),
      1.15, // ~66° cone
      14,
      this.scene,
    );
    l.parent = this.camera;
    // Sit it slightly below and left of the eye so the beam and the view are
    // not perfectly coincident — coincident light kills all shadow cueing and
    // makes every surface read flat.
    l.position = new Vector3(-0.11, -0.09, 0.06);
    l.diffuse = C.headlamp;
    l.specular = C.headlamp;
    // FALLOFF_PHYSICAL is inverse-square, so this is not a 0-1 dial: at 42 the
    // beam delivered ~1.7 at five metres and was invisible against a moon key
    // of 4.6. A bright LED headlamp at arm's length needs three orders more.
    l.intensity = 900;
    l.range = 26;
    l.innerAngle = 0.42;
    l.falloffType = SpotLight.FALLOFF_PHYSICAL;
    l.shadowEnabled = true;

    // A cookie: real headlamps have a hot centre, a soft corona, and a faint
    // reflector artefact. A perfectly smooth cone is the single most obvious
    // "this is a game engine" tell.
    try {
      l.projectionTexture = makeHeadlampCookie(this.scene);
    } catch {
      /* no cookie is survivable */
    }
    return l;
  }

  setFootstepHandler(fn: (surface: string, intensity: number) => void): void {
    this.onFootstep = fn;
  }

  setLandHandler(fn: (intensity: number) => void): void {
    this.onLand = fn;
  }

  get position(): Vector3 {
    return this.root.position;
  }

  /** World-space eye position, including bob and lean. */
  get eyePosition(): Vector3 {
    return Vector3.TransformCoordinates(this.camera.position, this.root.getWorldMatrix());
  }

  get forward(): Vector3 {
    return new Vector3(Math.sin(this.yaw), 0, Math.cos(this.yaw));
  }

  toggleHeadlamp(): void {
    this.headlamp.setEnabled(!this.headlamp.isEnabled());
  }

  teleport(p: Vector3, yaw?: number): void {
    this.root.position.copyFrom(p);
    this.velocity.setAll(0);
    if (yaw !== undefined) this.yaw = yaw;
  }

  /**
   * Pin the camera to a fixed pose for the screenshot harness and stop all
   * procedural head motion. Reversible via `releaseAnchor()`.
   */
  setAnchor(p: Vector3, yaw: number, pitch: number, fovDeg?: number): void {
    this.anchored = true;
    this.root.position.copyFrom(p);
    this.root.rotation.y = yaw;
    this.yaw = yaw;
    this.pitch = pitch;
    this.velocity.setAll(0);
    this.bobAmount = 0;
    this.bobPhase = 0;
    this.lean = 0;
    this.leanTarget = 0;
    this.landImpulse = 0;
    this.headTilt = 0;
    this.eyeHeight = 0;
    this.targetEye = 0;
    // The anchor position IS the eye position, so the camera sits at the
    // root's origin rather than at standing eye height.
    this.camera.position.set(0, 0, 0);
    if (!this.camera.rotationQuaternion) {
      this.camera.rotationQuaternion = Quaternion.Identity();
    }
    this.camera.rotationQuaternion.copyFrom(Quaternion.RotationYawPitchRoll(0, pitch, 0));
    if (fovDeg) this.camera.fov = (fovDeg * Math.PI) / 180;
  }

  releaseAnchor(): void {
    this.anchored = false;
    this.eyeHeight = EYE_STAND;
    this.targetEye = EYE_STAND;
    this.camera.fov = (settings.get().fov * Math.PI) / 180;
  }

  update(dt: number): void {
    if (this.anchored) return;
    const s = settings.get();

    this.updateLook(dt);
    this.updateStance(dt);
    const speed = this.updateMovement(dt);
    this.updateHead(dt, speed, s.headBob, s.cameraLean);
    this.updateBattery(dt);
  }

  // ---------------------------------------------------------------- look ---
  private updateLook(dt: number): void {
    const look = input.consumeLook();
    // Mouse delta is already frame-independent; pad look is per-second.
    this.yaw += look.x + input.padLookX * settings.get().sensitivity * 3.2 * dt;
    this.pitch += look.y + input.padLookY * settings.get().sensitivity * 3.2 * dt;
    const limit = Math.PI / 2 - 0.02;
    this.pitch = Math.max(-limit, Math.min(limit, this.pitch));
    this.root.rotation.y = this.yaw;
  }

  // -------------------------------------------------------------- stance ---
  private updateStance(dt: number): void {
    if (input.pressed('crouch')) {
      this.stance = this.stance === 'crouch' ? 'stand' : 'crouch';
    }
    if (input.pressed('prone')) {
      this.stance = this.stance === 'prone' ? 'crouch' : 'prone';
    }
    // Refuse to stand up into a ceiling.
    if (this.stance !== 'prone' && !this.hasHeadroom(this.stance)) {
      this.stance = this.stance === 'stand' ? 'crouch' : 'prone';
    }

    const h =
      this.stance === 'stand'
        ? HEIGHT_STAND
        : this.stance === 'crouch'
          ? HEIGHT_CROUCH
          : HEIGHT_PRONE;
    this.root.ellipsoid.y = h / 2;
    this.root.ellipsoidOffset.y = h / 2;

    this.targetEye =
      this.stance === 'stand' ? EYE_STAND : this.stance === 'crouch' ? EYE_CROUCH : EYE_PRONE;
    // Asymmetric: dropping is fast, standing is slower. Reads as effort.
    const rate = this.targetEye < this.eyeHeight ? 11 : 7;
    this.eyeHeight += (this.targetEye - this.eyeHeight) * Math.min(1, rate * dt);
  }

  private hasHeadroom(from: Stance): boolean {
    const need = from === 'stand' ? HEIGHT_STAND : HEIGHT_CROUCH;
    const origin = this.root.position.add(new Vector3(0, 0.2, 0));
    const hit = this.scene.pickWithRay(
      new Ray(origin, Vector3.Up(), need),
      (m) => m.checkCollisions && m.isEnabled(),
    );
    return !hit?.hit;
  }

  // ------------------------------------------------------------ movement ---
  private updateMovement(dt: number): number {
    // Desired direction in local space.
    let ix = 0;
    let iz = 0;
    if (input.held('forward')) iz += 1;
    if (input.held('back')) iz -= 1;
    if (input.held('right')) ix += 1;
    if (input.held('left')) ix -= 1;
    ix += input.padMoveX;
    iz -= input.padMoveY;

    const mag = Math.hypot(ix, iz);
    if (mag > 1) {
      ix /= mag;
      iz /= mag;
    }

    const wantsSprint =
      input.held('sprint') && this.stance === 'stand' && iz > 0.3 && this.stamina > 0.02;

    let target = SPEED[this.stance];
    if (wantsSprint) target = SPRINT_SPEED;
    // Strafing and backpedalling are slower; it stops the strafe-run gait that
    // makes first-person movement feel weightless.
    if (iz < 0) target *= 0.72;
    target *= 1 - 0.18 * Math.abs(ix) * (iz > 0 ? 1 : 0);

    // Stamina economy. Lonnie's Adrenaline modifier hooks in via staminaRegen.
    if (wantsSprint) {
      this.stamina = Math.max(0, this.stamina - dt * 0.19);
    } else {
      const regen = this.stance === 'stand' && mag < 0.1 ? 0.34 : 0.17;
      this.stamina = Math.min(1, this.stamina + dt * regen);
    }
    // Exhaustion slows you rather than stopping you. No instant-fail states.
    if (this.stamina < 0.15) target *= 0.62 + this.stamina;

    const yawSin = Math.sin(this.yaw);
    const yawCos = Math.cos(this.yaw);
    const wishX = ix * yawCos + iz * yawSin;
    const wishZ = -ix * yawSin + iz * yawCos;

    // Ground accel is snappy; air control is deliberately poor.
    const accel = this.grounded ? 42 : 5;
    const desiredX = wishX * target;
    const desiredZ = wishZ * target;
    this.velocity.x += (desiredX - this.velocity.x) * Math.min(1, accel * dt);
    this.velocity.z += (desiredZ - this.velocity.z) * Math.min(1, accel * dt);

    if (this.grounded && input.pressed('jump') && this.stance === 'stand' && this.stamina > 0.1) {
      this.velocity.y = JUMP_VELOCITY;
      this.grounded = false;
      this.stamina -= 0.06;
    }

    this.velocity.y += GRAVITY * dt;
    if (this.velocity.y < -55) this.velocity.y = -55;

    const before = this.root.position.clone();
    const displacement = this.velocity.scale(dt);

    // Step-up: probe forward at ankle height; if blocked but clear at step
    // height, lift the move. This is what stops the player catching on the
    // 4-inch thresholds that are everywhere in this building.
    if (this.grounded && (Math.abs(displacement.x) > 1e-4 || Math.abs(displacement.z) > 1e-4)) {
      displacement.y += this.stepAssist(displacement);
    }

    this.root.moveWithCollisions(displacement);

    const moved = this.root.position.subtract(before);
    // Recover the real velocity after collision so sliding along a wall does
    // not keep accumulating speed into it.
    if (dt > 0) {
      this.velocity.x = moved.x / dt;
      this.velocity.z = moved.z / dt;
    }

    const wasGrounded = this.grounded;
    this.grounded = this.checkGround();
    if (this.grounded) {
      if (!wasGrounded) {
        const impact = Math.min(1, Math.abs(this.velocity.y) / 12);
        this.landImpulse = impact;
        if (impact > 0.12) this.onLand?.(impact);
      }
      this.velocity.y = 0;
    }

    const horizontalSpeed = Math.hypot(this.velocity.x, this.velocity.z);
    this.moveSpeedSmoothed += (horizontalSpeed - this.moveSpeedSmoothed) * Math.min(1, 12 * dt);

    // Footsteps are distance-driven, not timer-driven, so the cadence always
    // matches the actual gait.
    if (this.grounded && horizontalSpeed > 0.35) {
      this.stepDistance += horizontalSpeed * dt;
      const stride = this.stance === 'stand' ? (wantsSprint ? 1.55 : 1.18) : 0.82;
      if (this.stepDistance >= stride) {
        this.stepDistance = 0;
        const intensity =
          this.stance === 'prone' ? 0.22 : this.stance === 'crouch' ? 0.42 : wantsSprint ? 1 : 0.66;
        this.onFootstep?.(this.currentSurface, intensity);
      }
    } else if (horizontalSpeed < 0.1) {
      this.stepDistance = 0;
    }

    return horizontalSpeed;
  }

  private stepAssist(displacement: Vector3): number {
    const dir = new Vector3(displacement.x, 0, displacement.z).normalize();
    const ankle = this.root.position.add(new Vector3(0, 0.08, 0));
    const probe = 0.42;
    const lowHit = this.scene.pickWithRay(
      new Ray(ankle, dir, probe),
      (m) => m.checkCollisions && m.isEnabled(),
    );
    if (!lowHit?.hit) return 0;

    const knee = this.root.position.add(new Vector3(0, STEP_HEIGHT + 0.06, 0));
    const highHit = this.scene.pickWithRay(
      new Ray(knee, dir, probe),
      (m) => m.checkCollisions && m.isEnabled(),
    );
    if (highHit?.hit) return 0; // a real wall, not a step

    return STEP_HEIGHT * 0.55;
  }

  private checkGround(): boolean {
    const origin = this.root.position.add(new Vector3(0, 0.12, 0));
    const hit = this.scene.pickWithRay(
      new Ray(origin, Vector3.Down(), 0.28),
      (m) => m.checkCollisions && m.isEnabled(),
    );
    if (hit?.hit) {
      // Let scenes tag surfaces for footstep audio via metadata.
      const tag = (hit.pickedMesh?.metadata as SurfaceAudio | undefined)?.surface;
      if (tag) this.currentSurface = tag;
      return true;
    }
    return false;
  }

  // ------------------------------------------------------- head / camera ---
  private updateHead(dt: number, speed: number, bobScale: number, leanEnabled: boolean): void {
    // Lean. Peeking round a doorway without stepping into it is most of the
    // tension in a game with no enemies — you lean because the floor might
    // not be there.
    if (leanEnabled) {
      const l = input.held('leanLeft') && !input.held('interact');
      const r = input.held('leanRight') && !input.held('interact');
      this.leanTarget = l ? -1 : r ? 1 : 0;
    } else {
      this.leanTarget = 0;
    }
    this.lean += (this.leanTarget - this.lean) * Math.min(1, 9 * dt);

    // Head bob: a figure-eight, vertical at 2× the horizontal, which is what
    // real walking does. Amplitude scales with speed, not a fixed constant.
    const normalized = Math.min(1, speed / SPRINT_SPEED);
    this.bobAmount += (normalized - this.bobAmount) * Math.min(1, 8 * dt);
    if (this.grounded && speed > 0.3) {
      this.bobPhase += dt * (4.1 + normalized * 4.4);
    } else {
      this.bobAmount *= Math.max(0, 1 - 6 * dt);
    }

    const bob = this.bobAmount * bobScale;
    const bobX = Math.cos(this.bobPhase) * 0.038 * bob;
    const bobY = Math.abs(Math.sin(this.bobPhase * 2)) * 0.036 * bob;
    // Landing compresses the knees. Decays fast.
    this.landImpulse *= Math.max(0, 1 - 7 * dt);
    const landDip = this.landImpulse * 0.22;

    this.camera.position.set(
      bobX + this.lean * 0.36,
      this.eyeHeight + bobY - landDip,
      0,
    );

    // Roll with lean and a slight counter-roll with the bob — that tiny roll
    // is most of what makes first-person walking feel like a body.
    const bobRoll = Math.sin(this.bobPhase) * 0.008 * bob;
    const leanRoll = -this.lean * 0.16;
    this.headTilt += (leanRoll + bobRoll - this.headTilt) * Math.min(1, 12 * dt);

    if (!this.camera.rotationQuaternion) {
      this.camera.rotationQuaternion = Quaternion.Identity();
    }
    Quaternion.RotationYawPitchRollToRef(0, this.pitch, this.headTilt, this.camera.rotationQuaternion);
  }

  private updateBattery(dt: number): void {
    if (!this.headlamp.isEnabled()) return;
    this.battery = Math.max(0, this.battery - dt * 0.0038);
    // Browns out rather than cutting to black — a dead lamp that strands the
    // player in the dark is exactly the kind of instant-fail this game avoids.
    const brown = this.battery < 0.2 ? 0.45 + this.battery * 2.75 : 1;
    const flicker = this.battery < 0.12 ? 0.88 + Math.random() * 0.12 : 1;
    this.headlamp.intensity = 900 * brown * flicker;
  }

  dispose(): void {
    this.headlamp.dispose();
    this.camera.dispose();
    this.root.dispose();
  }
}

/**
 * Procedural headlamp cookie: hot centre, soft corona, faint reflector rings
 * and a slightly irregular edge. Generated rather than shipped so it costs
 * nothing in the bundle.
 */
function makeHeadlampCookie(scene: Scene): Texture {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d')!;
  const cx = size / 2;

  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, size, size);

  const g = ctx.createRadialGradient(cx, cx, 0, cx, cx, cx);
  g.addColorStop(0.0, 'rgba(255,255,255,1)');
  g.addColorStop(0.22, 'rgba(255,252,244,0.97)');
  g.addColorStop(0.46, 'rgba(255,246,226,0.72)');
  g.addColorStop(0.72, 'rgba(250,238,214,0.28)');
  g.addColorStop(0.9, 'rgba(240,230,208,0.06)');
  g.addColorStop(1.0, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, size, size);

  // Reflector rings — subtle, just enough to break the perfect gradient.
  ctx.globalCompositeOperation = 'lighter';
  for (let i = 1; i <= 3; i++) {
    ctx.beginPath();
    ctx.arc(cx, cx, cx * (0.3 + i * 0.16), 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(255,248,232,${0.05 - i * 0.012})`;
    ctx.lineWidth = 6;
    ctx.stroke();
  }

  const tex = new Texture(canvas.toDataURL('image/png'), scene, true, false);
  tex.name = 'headlampCookie';
  tex.wrapU = Texture.CLAMP_ADDRESSMODE;
  tex.wrapV = Texture.CLAMP_ADDRESSMODE;
  return tex;
}
