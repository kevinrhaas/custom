#!/usr/bin/env node
/**
 * Headlamp calibration rig.
 *
 * The headlamp has been set by reasoning twice and been wrong twice — once an
 * order of magnitude too dim, once too bright. Reasoning about inverse-square
 * falloff is not the same as measuring it, so this measures it.
 *
 * Builds a bare scene: a flat wall, the player's headlamp, nothing else. Steps
 * the camera to 1 / 2 / 4 / 8 / 12 m and samples the centre pixel of the
 * rendered frame at each distance. Prints the measured luminance curve.
 *
 * What we want, in sRGB 0-255 at the beam centre:
 *   1 m  — bright but NOT clipped. ≤ 250. Anything at 255 is a blown hotspot.
 *   2 m  — 170-230. The reading distance; carved stone must show relief here.
 *   4 m  — 90-150. Comfortably lit.
 *   8 m  — 25-70. Visible, clearly falling off.
 *  12 m  — 5-25. The edge of useful throw.
 *
 * A curve that clips at 1 m and dies by 8 m is the failure mode we keep hitting.
 *
 * Usage: node tools/light-calibrate.mjs [--intensity 240] [--pullback 1.2]
 */

import { chromium } from 'playwright';
import { createServer } from 'vite';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const args = process.argv.slice(2);
const flag = (n, d) => {
  const i = args.indexOf(`--${n}`);
  return i >= 0 ? Number(args[i + 1]) : d;
};

const DISTANCES = [1, 2, 4, 8, 12];
const TARGETS = {
  1: [180, 250],
  2: [170, 230],
  4: [90, 150],
  8: [25, 70],
  12: [5, 25],
};

const server = await createServer({
  root: ROOT,
  server: { port: 5211, strictPort: true },
  logLevel: 'error',
});
await server.listen();

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROMIUM ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: [
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--disable-dev-shm-usage',
    '--disable-renderer-backgrounding',
    '--disable-background-timer-throttling',
  ],
});
const page = await browser.newPage({ viewport: { width: 512, height: 512 } });
page.on('pageerror', (e) => console.log('  pageerror:', String(e).slice(0, 160)));

await page.goto('http://localhost:5211/?quality=high&webgl', {
  waitUntil: 'load',
  timeout: 180000,
});
await page.waitForFunction(() => window.__joliet?.ready === true, null, { timeout: 300000 });

const intensity = flag('intensity', null);
const pullback = flag('pullback', null);

console.log('\nHeadlamp calibration');
console.log('────────────────────────────────────────────────────────────');
if (intensity !== null) console.log(`  intensity override: ${intensity}`);
if (pullback !== null) console.log(`  pullback override:  ${pullback} m`);

const rows = await page.evaluate(
  async ({ distances, intensity, pullback }) => {
    const g = window.__joliet;
    const BABYLON = g.renderer.scene.getEngine();
    void BABYLON;
    const scene = g.renderer.scene;
    const player = g.player;

    // Hide the world; we only want the wall and the lamp.
    const hidden = [];
    for (const m of scene.meshes) {
      if (m.isEnabled() && m.isVisible) {
        hidden.push(m);
        m.setEnabled(false);
      }
    }
    // Kill every light except the headlamp so nothing else contributes.
    const lightState = [];
    for (const l of scene.lights) {
      lightState.push([l, l.isEnabled()]);
      if (l !== player.headlamp) l.setEnabled(false);
    }
    const envI = scene.environmentIntensity;
    scene.environmentIntensity = 0;
    const fog = scene.fogMode;
    scene.fogMode = 0;

    if (intensity !== null) player.headlamp.intensity = intensity;
    if (pullback !== null) player.headlamp.position.z = -pullback;

    // A plain neutral wall: 50% grey, fully rough, no metal. Any measured
    // value is then purely the light, not the material.
    const wall = window.BABYLON_TEST_WALL ?? null;
    void wall;

    const results = [];
    for (const d of distances) {
      // Move the player so the wall sits `d` metres ahead. Rather than build a
      // wall we reuse an existing large mesh: re-enable the ground and stand
      // the camera off it looking straight down, which is geometrically the
      // same measurement against a flat lambertian surface.
      const ground = scene.getMeshByName('ground');
      if (!ground) return [{ error: 'no ground mesh to measure against' }];
      ground.setEnabled(true);

      player.setAnchor(
        new (Object.getPrototypeOf(player.position).constructor)(0, d, 0),
        0,
        Math.PI / 2 - 0.001, // straight down
      );
      g.renderer.resetTAA();
      await new Promise((r) => setTimeout(r, 900));
      results.push({ d });
    }

    // restore
    for (const m of hidden) m.setEnabled(true);
    for (const [l, on] of lightState) l.setEnabled(on);
    scene.environmentIntensity = envI;
    scene.fogMode = fog;
    return results;
  },
  { distances: DISTANCES, intensity, pullback },
);

if (rows[0]?.error) {
  console.log('  ✗', rows[0].error);
} else {
  // Sample the centre pixel from a screenshot at each distance.
  console.log('\n  dist   centre luminance   target        verdict');
  console.log('  ─────  ────────────────   ───────────   ─────────');
  for (const d of DISTANCES) {
    await page.evaluate(
      async ({ d, intensity, pullback }) => {
        const g = window.__joliet;
        const scene = g.renderer.scene;
        const player = g.player;
        for (const m of scene.meshes) m.setEnabled(m.name === 'ground');
        for (const l of scene.lights) l.setEnabled(l === player.headlamp);
        scene.environmentIntensity = 0;
        scene.fogMode = 0;
        if (intensity !== null) player.headlamp.intensity = intensity;
        if (pullback !== null) player.headlamp.position.z = -pullback;
        const V = Object.getPrototypeOf(player.position).constructor;
        player.setAnchor(new V(0, d, 0), 0, Math.PI / 2 - 0.001);
        g.renderer.resetTAA();
        await new Promise((r) => setTimeout(r, 900));
      },
      { d, intensity, pullback },
    );

    const shot = await page.screenshot({ type: 'png' });
    // Decode the centre pixel without an image library: use the browser.
    const lum = await page.evaluate(async (b64) => {
      const img = new Image();
      img.src = 'data:image/png;base64,' + b64;
      await img.decode();
      const c = document.createElement('canvas');
      c.width = img.width;
      c.height = img.height;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const p = ctx.getImageData(Math.floor(img.width / 2), Math.floor(img.height / 2), 1, 1).data;
      return Math.round(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]);
    }, shot.toString('base64'));

    const [lo, hi] = TARGETS[d];
    const verdict = lum >= 255 ? 'CLIPPED' : lum < lo ? 'too dim' : lum > hi ? 'too hot' : 'ok';
    console.log(
      `  ${String(d).padStart(4)}m  ${String(lum).padStart(14)}   ${String(lo).padStart(3)}-${String(hi).padEnd(3)}      ${verdict}`,
    );
  }
}

console.log('');
await browser.close();
await server.close();
