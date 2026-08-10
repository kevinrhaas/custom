/**
 * pointerlock.js — the desktop backend: WASD plus mouse-look under pointer lock.
 *
 * `PointerLockControls` is used for what it is genuinely good at — the Pointer
 * Lock API plumbing, the lock/unlock events, the polar clamp — but it is NOT
 * pointed at the camera. It drives a throwaway rig, and this backend reports the
 * frame's rotation as `yawDelta` / `pitchDelta` on the shared intent object.
 *
 * That indirection buys the invariant in intent.js: the camera has exactly one
 * author (the walker), so desktop and touch cannot fight over it, and the smoke
 * harness can drive the same intent both backends write.
 *
 * Keys are read whether or not the pointer is locked. Walking before you click
 * is the friendlier behaviour, and it is what lets a headless test press W.
 */

import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

const KEYS = {
  KeyW: 'ahead', ArrowUp: 'ahead',
  KeyS: 'back', ArrowDown: 'back',
  KeyA: 'left', ArrowLeft: 'left',
  KeyD: 'right', ArrowRight: 'right',
};

export function createPointerLockBackend({ intent, domElement, onLockChange }) {
  // PointerLockControls connects its document listeners in the constructor, so
  // enabling and disabling this backend flips `controls.enabled` rather than
  // reconnecting — connect() twice would double-register every listener.
  const rig = new THREE.Object3D();
  const controls = new PointerLockControls(rig, domElement);
  controls.enabled = false;
  controls.pointerSpeed = 1.0;
  controls.minPolarAngle = Math.PI * 0.06;
  controls.maxPolarAngle = Math.PI * 0.94;

  const held = new Set();
  const euler = new THREE.Euler(0, 0, 0, 'YXZ');
  let prevYaw = 0;
  let prevPitch = 0;
  let enabled = false;

  function onKeyDown(e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') { held.add('sprint'); return; }
    // Vertical, free-fly only. Space is overloaded — it inspects on foot and
    // ascends in the air — which is why the backend has to see intent.flying.
    // The alternative was a third key nobody would find; ascend-on-Space is
    // what every flycam in existence does, and inspect has E either way.
    if (e.code === 'Space' && intent.flying) { held.add('up'); e.preventDefault(); return; }
    if (e.code === 'KeyQ') { held.add('down'); e.preventDefault(); return; }
    if (e.code === 'KeyE' || e.code === 'Space') {
      // Space also inspects: on a trackpad, E and a click are the same reach.
      // No point: a keyboard inspection is always down the crosshair.
      if (!e.repeat) { intent.interactPoint = null; intent.interact = true; }
      e.preventDefault();
      return;
    }
    const dir = KEYS[e.code];
    if (!dir) return;
    held.add(dir);
    e.preventDefault();
  }

  function onKeyUp(e) {
    if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') { held.delete('sprint'); return; }
    // Released unconditionally, NOT behind `intent.flying`: leaving fly mode
    // with Space down would otherwise strand 'up' in the held set and the
    // visitor would rise forever with nothing pressed.
    if (e.code === 'Space') { held.delete('up'); return; }
    if (e.code === 'KeyQ') { held.delete('down'); return; }
    const dir = KEYS[e.code];
    if (dir) held.delete(dir);
  }

  function onBlur() { held.clear(); }

  function onLock() { onLockChange?.(true); }
  function onUnlock() { onLockChange?.(false); }

  return {
    name: 'pointerlock',
    controls,
    get isLocked() { return controls.isLocked; },

    lock() {
      try { controls.lock(); } catch { /* a denied lock is not an error worth a page error */ }
    },
    unlock() { controls.unlock(); },

    enable() {
      if (enabled) return;
      enabled = true;
      window.addEventListener('keydown', onKeyDown);
      window.addEventListener('keyup', onKeyUp);
      window.addEventListener('blur', onBlur);
      controls.addEventListener('lock', onLock);
      controls.addEventListener('unlock', onUnlock);
      controls.enabled = true;
      rig.rotation.set(0, 0, 0);
      prevYaw = prevPitch = 0;
    },

    disable() {
      if (!enabled) return;
      enabled = false;
      held.clear();
      window.removeEventListener('keydown', onKeyDown);
      window.removeEventListener('keyup', onKeyUp);
      window.removeEventListener('blur', onBlur);
      controls.removeEventListener('lock', onLock);
      controls.removeEventListener('unlock', onUnlock);
      if (controls.isLocked) controls.unlock();
      controls.enabled = false;
    },

    /** Write this frame's intent. Called once per frame by main.js. */
    update() {
      if (!enabled) return;
      intent.forward = (held.has('ahead') ? 1 : 0) - (held.has('back') ? 1 : 0);
      intent.strafe = (held.has('right') ? 1 : 0) - (held.has('left') ? 1 : 0);
      intent.rise = (held.has('up') ? 1 : 0) - (held.has('down') ? 1 : 0);
      intent.sprint = held.has('sprint');

      euler.setFromQuaternion(rig.quaternion, 'YXZ');
      intent.yawDelta += euler.y - prevYaw;
      intent.pitchDelta += euler.x - prevPitch;
      prevYaw = euler.y;
      prevPitch = euler.x;
    },

    dispose() {
      this.disable();
      controls.dispose();
    },
  };
}
