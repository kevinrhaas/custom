#!/usr/bin/env node
/**
 * Traversal probe — can a player actually walk the route?
 *
 * Every automated check in this project has asked "does it render". None has
 * ever asked "can someone move through it", which is why a set of stairs that
 * ended in mid-air shipped: it photographed perfectly from all five anchors.
 *
 * This drives the real character controller — gravity, collide-and-slide,
 * step-up probe, the lot — along a route and reports where the player ends up.
 * A climb that loses height, or a walk that ends below where it started, is a
 * hole in the world.
 *
 * Usage: node tools/traverse-probe.mjs [--scene cellblocks]
 */

import { chromium } from 'playwright';
import { createServer } from 'vite';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const args = process.argv.slice(2);
const flag = (n, d) => {
  const i = args.indexOf(`--${n}`);
  return i >= 0 ? args[i + 1] : d;
};
const scene = flag('scene', 'cellblocks');

/** Routes per scene: start pose, heading, seconds to hold forward. */
const ROUTES = {
  // `from: null` means "use the scene's declared spawn" — the only start point
  // guaranteed to be standable.
  cellblocks: [
    { name: 'walk from spawn', from: null, yaw: 0, hold: 12, expectRise: -0.6 },
    // Stair centre x = WALL_X(-3.9) + 0.08 + STAIR_W/2(0.56). Flights rise
    // TIER_H (2.65 m) from z 12.4 / 28.2 / 43.6. Start a little before the
    // bottom riser and walk straight up.
    { name: 'stair flight 1 (tier 0 → 1)', from: [-3.26, 0.4, 11.4], yaw: 0, hold: 10, expectRise: 2.4 },
    { name: 'stair flight 2 (tier 1 → 2)', from: [-3.26, 3.05, 27.2], yaw: 0, hold: 10, expectRise: 2.4 },
  ],
  perimeter: [
    { name: 'approach to the wall', from: [0, 0.5, -30], yaw: 0, hold: 10, expectRise: -0.6 },
    { name: 'across the trench mouth', from: [13.5, 0.5, -12], yaw: 0, hold: 9, expectRise: -3.5 },
  ],
  void: [{ name: 'chamber length', from: [0, 0.5, -6], yaw: 0, hold: 9, expectRise: -0.6 }],
};

const route = ROUTES[scene];
if (!route) {
  console.error(`no route defined for scene "${scene}"`);
  process.exit(1);
}

const server = await createServer({
  root: ROOT,
  server: { port: 5222, strictPort: true },
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
const page = await browser.newPage({ viewport: { width: 640, height: 400 } });
page.on('pageerror', (e) => console.log('  pageerror:', String(e).slice(0, 150)));

await page.goto(`http://localhost:5222/?quality=low&scene=${scene}&webgl`, {
  waitUntil: 'load',
  timeout: 180000,
});
await page.waitForFunction(() => window.__joliet?.ready === true, null, { timeout: 300000 });

console.log(`\nTraversal probe — ${scene}`);
console.log('──────────────────────────────────────────────────────────────');

let failures = 0;
for (const leg of route) {
  const r = await page.evaluate(
    async ({ from, yaw, hold }) => {
      const g = window.__joliet;
      const p = g.player;
      const V = Object.getPrototypeOf(p.position).constructor;
      p.releaseAnchor();
      const sp = from ?? g.scene.manifest.spawn.position;
      const y = from ? from[1] : g.scene.manifest.spawn.yaw;
      p.teleport(new V(sp[0], sp[1] + 0.3, sp[2]), from ? yaw : y);

      // Let gravity settle the spawn before measuring.
      await new Promise((r) => setTimeout(r, 500));
      const start = { x: p.position.x, y: p.position.y, z: p.position.z };

      // Drive the REAL input path with synthetic key events — Input listens on
      // window, so this exercises exactly what a player's keyboard does. The
      // first version of this probe set a flag nothing read, and dutifully
      // reported that the player had not moved.
      const key = (type) =>
        window.dispatchEvent(
          new KeyboardEvent(type, { code: 'KeyW', key: 'w', bubbles: true }),
        );
      key('keydown');
      const t0 = performance.now();
      let recovered = false;
      let minY = p.position.y;
      while (performance.now() - t0 < hold * 1000) {
        await new Promise((r) => setTimeout(r, 32));
        minY = Math.min(minY, p.position.y);
        if (p.position.y < -30) recovered = true;
      }
      key('keyup');
      await new Promise((r) => setTimeout(r, 400));
      void minY;

      return {
        start,
        end: { x: p.position.x, y: p.position.y, z: p.position.z },
        grounded: p.grounded,
        recovered,
      };
    },
    { from: leg.from, yaw: leg.yaw, hold: leg.hold },
  );

  const rise = r.end.y - r.start.y;
  const dist = Math.hypot(r.end.x - r.start.x, r.end.z - r.start.z);
  const ok =
    !r.recovered && r.grounded && dist > 2 && rise >= leg.expectRise - 0.6;
  if (!ok) failures++;
  console.log(
    `  ${ok ? '✓' : '✗'} ${leg.name.padEnd(30)} moved ${dist.toFixed(1)} m, ` +
      `rise ${rise >= 0 ? '+' : ''}${rise.toFixed(2)} m ` +
      `(want ≥ ${leg.expectRise.toFixed(1)})${r.recovered ? '  FELL OUT OF WORLD' : ''}` +
      `${r.grounded ? '' : '  NOT GROUNDED'}`,
  );
}

console.log(failures ? `\n  ${failures} leg(s) failed\n` : '\n  all legs passed\n');
await browser.close();
await server.close();
process.exit(failures ? 1 : 0);
