/**
 * intent.js — the single input-intent object.
 *
 * Every input backend writes THIS and nothing else. The walker reads THIS and
 * nothing else. No backend touches the camera, and exactly one backend is active
 * at a time, so "why is the camera moving" always has one answer.
 *
 * The alternative — pointer-lock moving the camera directly while a touch layer
 * moves it too — is how you get a scene that walks twice as fast on a laptop
 * with a touchscreen, and it is the bug you find last.
 *
 * Fields, all in the walker's units:
 *
 *   forward    -1 back .. +1 ahead        (analogue: a thumbstick gives 0.4)
 *   strafe     -1 left .. +1 right
 *   yawDelta   radians to turn this frame, + is left (counter-clockwise)
 *   pitchDelta radians to look up this frame, + is up
 *   sprint     boolean
 *   interact   edge-triggered; consume it with `takeInteract()`
 *
 * `interactPoint` rides along with `interact`: a crosshair inspection has no
 * point (null) and a tap has the one you tapped, in normalised device coords.
 * It lives on the intent rather than in a backend callback so that "what did the
 * visitor ask for" is still answered by exactly one object.
 */

export function createIntent() {
  const intent = {
    forward: 0,
    strafe: 0,
    yawDelta: 0,
    pitchDelta: 0,
    sprint: false,
    interact: false,
    interactPoint: null,

    /** Movement written this frame, for the HUD and the smoke harness. */
    get moving() { return Math.abs(this.forward) > 0.001 || Math.abs(this.strafe) > 0.001; },

    /**
     * Read-and-clear, so one tap is one interaction.
     * @returns {false | {point: {x:number,y:number}|null}}
     */
    takeInteract() {
      if (!this.interact) return false;
      const point = this.interactPoint;
      this.interact = false;
      this.interactPoint = null;
      return { point };
    },

    /** Look deltas are per-frame; the walker clears them once consumed. */
    clearLook() {
      this.yawDelta = 0;
      this.pitchDelta = 0;
    },

    clear() {
      this.forward = 0;
      this.strafe = 0;
      this.sprint = false;
      this.interact = false;
      this.interactPoint = null;
      this.clearLook();
    },
  };
  return intent;
}

/**
 * Holds exactly one active backend. Switching deactivates the outgoing one and
 * zeroes the intent, so a half-pressed key or a lifted thumb cannot leak across.
 */
export function createBackendSwitch(intent) {
  let active = null;
  const listeners = new Set();

  return {
    get active() { return active; },
    get name() { return active?.name ?? 'none'; },

    /** @param {{name:string, enable:Function, disable:Function}} backend */
    activate(backend) {
      if (active === backend) return backend;
      active?.disable?.();
      intent.clear();
      active = backend ?? null;
      active?.enable?.();
      for (const fn of listeners) fn(active?.name ?? 'none');
      return active;
    },

    onChange(fn) {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
  };
}
