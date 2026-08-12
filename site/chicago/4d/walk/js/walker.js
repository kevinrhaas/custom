/**
 * walker.js — a person on foot. No physics engine.
 *
 * A capsule sliding on the heightfield sampler, and that is the whole model. It
 * is enough because there is nothing to simulate: no jumping, no vehicles, no
 * ragdolls, and — by standing instruction in `AGENTS.md` — no other people.
 * Importing a physics engine to walk across a prairie would cost a megabyte and
 * a build step to reproduce what forty lines of arithmetic already do.
 *
 * The one rule that is not arbitrary: a **0.35 m step-up limit**. That is a
 * little over a foot, which is what a plank walk stands above the mud and what a
 * person steps onto without thinking. Below it you step up; above it you are
 * looking at a wall and you stop. Downhill is free — you can always step down.
 */

import * as THREE from 'three';
import { enuToWorld, bearingToYaw, yawToBearing } from './terrain.js';

const DEG = Math.PI / 180;

export const WALK = {
  eyeHeight: 1.68,      // m — mid-19th-century adult male mean was near 1.72 m
  radius: 0.34,         // m — shoulder half-width for the push-out
  speed: 1.45,          // m/s — an unhurried walk
  sprintSpeed: 3.3,     // m/s — a jog, not a sprint
  stepUp: 0.35,         // m — the plank-walk rule
  pitchLimit: 85 * DEG,
};

/**
 * Free-fly. A separate object because these numbers are NOT the walk numbers
 * scaled up — flying answers a different question ("what is the shape of this
 * place") and wants different behaviour.
 */
export const FLY = {
  speed: 14,            // m/s — crossing a 640 m scene should take ~45 s, not 7 min
  sprintSpeed: 46,
  riseSpeed: 11,        // m/s vertical, independent of look direction
  minClearance: 1.2,    // m above the terrain; you may skim, not tunnel
  maxAltitude: 900,     // m above the datum water surface
  /**
   * Horizontal speed multiplies with height. At 300 m up, ground features
   * subtend so little angle that 14 m/s reads as not moving at all — the
   * classic flight-sim problem where altitude makes the world feel frozen.
   * Capped so it stays controllable near the top.
   */
  altitudeGain: (y) => Math.min(6, 1 + Math.max(0, y) / 90),
};

/** Point-in-polygon, ray casting. `pts` is [[e, n], ...]. */
function inside(e, n, pts) {
  let hit = false;
  for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
    const [xi, yi] = pts[i];
    const [xj, yj] = pts[j];
    if ((yi > n) !== (yj > n)
        && e < ((xj - xi) * (n - yi)) / (yj - yi) + xi) hit = !hit;
  }
  return hit;
}

/** Nearest point on a polygon's boundary. */
function nearestOnBoundary(e, n, pts) {
  let best = null;
  for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
    const [ax, ay] = pts[j];
    const [bx, by] = pts[i];
    const dx = bx - ax;
    const dy = by - ay;
    const len2 = dx * dx + dy * dy || 1e-9;
    const t = Math.max(0, Math.min(1, ((e - ax) * dx + (n - ay) * dy) / len2));
    const px = ax + dx * t;
    const py = ay + dy * t;
    const d = Math.hypot(e - px, n - py);
    if (!best || d < best.d) best = { e: px, n: py, d };
  }
  return best;
}

/**
 * Turn each sidecar's footprint into a world-space polygon in local ENU metres.
 * Tolerates both shapes seen in the wild: a bare `[[u, v], ...]` array and a
 * `{ polygon, confidence, note }` object.
 */
export function footprintsFrom(registry) {
  const out = [];
  for (const record of registry.values()) {
    const raw = record.sidecar?.footprint;
    const poly = Array.isArray(raw) ? raw : raw?.polygon;
    if (!Array.isArray(poly) || poly.length < 3) continue;

    const p = record.sidecar.placement ?? {};
    // A water-anchored structure's footprint is a DECK, not a wall, so it is not
    // an obstruction: treating a bridge as one would put an invisible barrier
    // across the river with nothing visible at head height to explain it. What
    // this does NOT yet do is let you walk the deck — the walker still follows
    // the terrain, so the bridge is scenery you pass under rather than a route.
    // Recorded as a limit in docs/STATUS.md rather than faked with a ramp.
    if (p.vertical_anchor === 'water') continue;
    const th = (p.rotation_deg ?? 0) * DEG;
    const cos = Math.cos(th);
    const sin = Math.sin(th);
    const e0 = p.local_e ?? 0;
    const n0 = p.local_n ?? 0;

    out.push({
      id: record.id,
      // Compass-bearing rotation, matching bearingToYaw(): clockwise from north.
      pts: poly.map(([u, v]) => [e0 + u * cos + v * sin, n0 - u * sin + v * cos]),
    });
  }
  return out;
}

/**
 * @param {object} o
 * @param {THREE.PerspectiveCamera} o.camera
 * @param {{height:(e:number,n:number)=>number}} o.terrain
 * @param {Array<{id:string, pts:number[][]}>} o.footprints
 * @param {{local_e:number, local_n:number, yaw_deg:number}} o.spawn
 */
export function createWalker({ camera, terrain, footprints = [], spawn = {} }) {
  const state = {
    e: spawn.local_e ?? 0,
    n: spawn.local_n ?? 0,
    yaw: bearingToYaw(spawn.yaw_deg ?? 0),
    pitch: 0,
    groundY: 0,
    eyeY: 0,
    speed: 0,
    /** Set when the last move was blocked by the step-up rule. */
    blocked: false,
    /** Free-fly mode. The walker owns the transition; the intent owns the wish. */
    flying: false,
    /** Metres above local ground, 0 on foot. What the HUD reports. */
    altitude: 0,
  };
  state.groundY = terrain.walkHeight(state.e, state.n);
  state.eyeY = state.groundY + WALK.eyeHeight;

  const euler = new THREE.Euler(0, 0, 0, 'YXZ');
  const world = new THREE.Vector3();

  /** Slide the capsule out of any footprint it has ended up inside. */
  function pushOut(e, n) {
    for (const fp of footprints) {
      const near = nearestOnBoundary(e, n, fp.pts);
      if (!near) continue;
      const within = inside(e, n, fp.pts);
      if (!within && near.d >= WALK.radius) continue;

      let dx = e - near.e;
      let dy = n - near.n;
      const len = Math.hypot(dx, dy);
      if (len < 1e-6) { dx = 1; dy = 0; }     // standing exactly on an edge
      else { dx /= len; dy /= len; }
      // Inside, that vector points into the building; outside, away from it.
      if (within) { dx = -dx; dy = -dy; }
      e = near.e + dx * WALK.radius;
      n = near.n + dy * WALK.radius;
    }
    return { e, n };
  }

  /** One axis at a time, so you slide along a slope instead of sticking to it. */
  function tryStep(e, n, de, dn) {
    let ok = true;
    const here = terrain.walkHeight(e, n);
    let next = { e, n };

    if (de !== 0) {
      const cand = { e: e + de, n };
      if (terrain.walkHeight(cand.e, cand.n) - here <= WALK.stepUp) next = cand;
      else ok = false;
    }
    if (dn !== 0) {
      const cand = { e: next.e, n: n + dn };
      if (terrain.walkHeight(cand.e, cand.n) - here <= WALK.stepUp) next = cand;
      else ok = false;
    }
    return { ...next, ok };
  }

  return {
    state,
    get position() { return world.clone(); },
    get enu() { return { e: state.e, n: state.n, y: state.eyeY }; },
    get bearingDeg() { return yawToBearing(state.yaw); },

    /**
     * Put the visitor somewhere. `altitude_m` makes it an AERIAL arrival: the
     * mode flips to free-fly and the eye goes to that height, because an
     * overhead viewpoint you are dropped into on foot is just a viewpoint of
     * some grass.
     */
    teleport({ local_e = state.e, local_n = state.n, yaw_deg = null,
               altitude_m = null, pitch_deg = null } = {}) {
      state.e = local_e;
      state.n = local_n;
      if (yaw_deg !== null) state.yaw = bearingToYaw(yaw_deg);
      if (pitch_deg !== null) {
        state.pitch = Math.max(-WALK.pitchLimit,
          Math.min(WALK.pitchLimit, pitch_deg * DEG));
      } else if (altitude_m === null) {
        // Arriving on foot levels the view. Without this you keep whatever
        // angle you had, so stepping off an aerial viewpoint down to a street
        // corner lands you staring at the cobbles — and, less visibly, aims
        // every crosshair inspection at the ground instead of the building.
        state.pitch = 0;
      }
      state.groundY = terrain.walkHeight(state.e, state.n);
      if (altitude_m !== null) {
        this.setFlying(true);
        state.eyeY = state.groundY + Math.max(FLY.minClearance, altitude_m);
        state.altitude = state.eyeY - state.groundY;
      } else {
        this.setFlying(false);
        state.eyeY = state.groundY + WALK.eyeHeight;
        state.altitude = 0;
      }
      this.apply();
    },

    /** Stand `distance` metres from a world point, looking at it. */
    lookAt(target, distance = 26, fromBearingDeg = null) {
      const te = target.x;
      const tn = -target.z;
      const bearing = fromBearingDeg ?? 200;   // stand south-west of the subject
      const rad = bearing * DEG;
      state.e = te + Math.sin(rad) * distance;
      state.n = tn + Math.cos(rad) * distance;
      state.groundY = terrain.walkHeight(state.e, state.n);
      state.eyeY = state.groundY + WALK.eyeHeight;

      const de = te - state.e;
      const dn = tn - state.n;
      state.yaw = bearingToYaw((Math.atan2(de, dn) / DEG + 360) % 360);
      const rise = (target.y || 4) - state.eyeY;
      state.pitch = Math.atan2(rise, Math.hypot(de, dn));
      this.apply();
    },

    /**
     * Enter or leave free-fly.
     *
     * Leaving SNAPS to the ground, which was not the first instinct. Letting
     * the walk path's existing ground-smoothing fly the eye down looked elegant
     * and is wrong at altitude: that term is exponential with a 14/s constant,
     * so it covers 87% of the drop in the first second — from 175 m that is a
     * 150 m/s plummet, and the remaining 13% then crawls for several seconds.
     * Both halves are bad. A rate-limited descent instead is a seven-second
     * cutscene nobody asked for. Snapping is honest and instant: you were
     * above this spot, now you are standing on it.
     */
    setFlying(on) {
      const next = !!on;
      if (next === state.flying) return next;
      state.flying = next;
      state.blocked = false;
      if (!next) {
        // Landing inside a building is possible — nothing pushed you out while
        // you were in the air — so clear the footprints before settling.
        const clear = pushOut(state.e, state.n);
        state.e = clear.e;
        state.n = clear.n;
        state.groundY = terrain.walkHeight(state.e, state.n);
        state.eyeY = state.groundY + WALK.eyeHeight;
        state.altitude = 0;
        this.apply();
      }
      return state.flying;
    },

    /**
     * Free movement. Deliberately does NOT call tryStep or pushOut: the
     * step-up rule and the footprint capsule are the two things that make
     * walking honest, and they are exactly what you are asking to leave.
     * Terrain is still a floor — you may skim the prairie, not tunnel it.
     */
    updateFly(dt, intent) {
      let f = intent.forward;
      let s = intent.strafe;
      const mag = Math.hypot(f, s);
      if (mag > 1) { f /= mag; s /= mag; }

      state.groundY = terrain.walkHeight(state.e, state.n);
      const gain = FLY.altitudeGain(state.eyeY - state.groundY);
      const base = intent.sprint ? FLY.sprintSpeed : FLY.speed;
      const speed = base * gain;

      // Forward follows the LOOK direction, pitch included — the whole point is
      // to nose up and rise away from the town, or dive back into it. Strafe
      // stays level, so sliding sideways for a better angle does not drift you
      // up or down without asking.
      const cosP = Math.cos(state.pitch);
      const sinY = Math.sin(state.yaw);
      const cosY = Math.cos(state.yaw);
      const fx = -sinY * cosP, fz = -cosY * cosP, fy = Math.sin(state.pitch);
      const rx = cosY, rz = -sinY;

      const dx = (fx * f + rx * s) * speed * dt;
      const dz = (fz * f + rz * s) * speed * dt;
      const dy = fy * f * speed * dt + intent.rise * FLY.riseSpeed * gain * dt;

      state.e += dx;
      state.n += -dz;                      // world -z is north
      state.eyeY += dy;

      const floor = terrain.walkHeight(state.e, state.n) + FLY.minClearance;
      state.eyeY = Math.max(floor, Math.min(FLY.maxAltitude, state.eyeY));
      state.groundY = terrain.walkHeight(state.e, state.n);
      state.altitude = state.eyeY - state.groundY;
      state.speed = Math.hypot(dx, dz, dy) / Math.max(dt, 1e-6);

      this.apply();
    },

    /** Write the camera. The ONLY place the camera transform is authored. */
    apply() {
      enuToWorld(state.e, state.n, state.eyeY, world);
      camera.position.copy(world);
      euler.set(state.pitch, state.yaw, 0, 'YXZ');
      camera.quaternion.setFromEuler(euler);
    },

    /**
     * @param {number} dt seconds
     * @param {object} intent  the shared intent object
     */
    update(dt, intent) {
      state.yaw += intent.yawDelta;
      state.pitch = Math.max(-WALK.pitchLimit,
        Math.min(WALK.pitchLimit, state.pitch + intent.pitchDelta));
      intent.clearLook();

      if (intent.flying !== state.flying) this.setFlying(intent.flying);
      if (state.flying) { this.updateFly(dt, intent); return; }

      let f = intent.forward;
      let s = intent.strafe;
      const mag = Math.hypot(f, s);
      if (mag > 1) { f /= mag; s /= mag; }

      const speed = intent.sprint ? WALK.sprintSpeed : WALK.speed;
      state.speed = Math.hypot(f, s) * speed;

      if (state.speed > 0) {
        // Camera-relative, flattened to the ground plane.
        const sinY = Math.sin(state.yaw);
        const cosY = Math.cos(state.yaw);
        const fx = -sinY, fz = -cosY;       // forward in world XZ
        const rx = cosY, rz = -sinY;        // right in world XZ
        const dx = (fx * f + rx * s) * speed * dt;
        const dz = (fz * f + rz * s) * speed * dt;

        const step = tryStep(state.e, state.n, dx, -dz);   // world -z is north
        state.blocked = !step.ok;
        state.e = step.e;
        state.n = step.n;
      } else {
        state.blocked = false;
      }

      // Every frame, not only while walking: a building whose placement moves
      // under a standing visitor should push them out, not swallow them.
      const clear = pushOut(state.e, state.n);
      state.e = clear.e;
      state.n = clear.n;

      // Walking is a constraint, not a camera animation: the eye stays exactly
      // WALK.eyeHeight above the SAME bilinear heightfield that built the mesh.
      // The old exponential easing lagged behind on every rise and fall, so the
      // visitor visibly entered a bank while climbing and floated while coming
      // down.  Bilinear sampling already makes ordinary terrain continuous;
      // the 0.35 m step rule above is the only place an actual step may occur.
      state.groundY = terrain.walkHeight(state.e, state.n);
      state.eyeY = state.groundY + WALK.eyeHeight;
      state.altitude = 0;

      this.apply();
    },
  };
}
