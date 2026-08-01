#!/usr/bin/env node
/**
 * The screenshot + performance harness.
 *
 * Renders every camera anchor of every scene at 1080p to
 * `artifacts/shots/<scene>/<iteration>/`, and records FPS, draw calls and
 * triangle counts alongside. The anchors never move between iterations, which
 * is the entire point: it is what makes the critic's comparisons meaningful
 * and what turns "looks better?" into a diff.
 *
 * Usage:
 *   node tools/shots.mjs                 # next iteration number, all anchors
 *   node tools/shots.mjs --iter 3        # force an iteration number
 *   node tools/shots.mjs --scene 1.1-perimeter
 *   node tools/shots.mjs --quality ultra
 */

import { chromium } from 'playwright';
import { createServer } from 'vite';
import { mkdir, writeFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const OUT_ROOT = path.join(ROOT, 'artifacts', 'shots');
const WIDTH = 1920;
const HEIGHT = 1080;

const args = process.argv.slice(2);
const flag = (n, d = null) => {
  const i = args.indexOf(`--${n}`);
  return i >= 0 ? (args[i + 1] ?? true) : d;
};

const quality = flag('quality', 'high');
const sceneFilter = flag('scene', null);

async function nextIteration(sceneId) {
  const dir = path.join(OUT_ROOT, sceneId);
  if (!existsSync(dir)) return 1;
  const entries = await readdir(dir);
  const nums = entries
    .map((e) => parseInt(e.replace(/\D/g, ''), 10))
    .filter((n) => Number.isFinite(n));
  return nums.length ? Math.max(...nums) + 1 : 1;
}

const server = await createServer({
  root: ROOT,
  server: { port: 5199, strictPort: true },
  logLevel: 'error',
});
await server.listen();
const base = `http://localhost:5199`;

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROMIUM ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: [
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--ignore-gpu-blocklist',
    '--enable-webgl',
    '--disable-dev-shm-usage',
    // Headless throttles rAF and timers for pages it treats as hidden, which
    // stalls the settle loop indefinitely.
    '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--disable-background-timer-throttling',
  ],
});

const page = await browser.newPage({
  viewport: { width: WIDTH, height: HEIGHT },
  deviceScaleFactor: 1,
});

const pageErrors = [];
page.on('pageerror', (e) => pageErrors.push(String(e)));
page.on('console', (m) => {
  if (m.type() === 'error') pageErrors.push(`console: ${m.text()}`);
});

console.log(`→ loading ${base}/?quality=${quality}&webgl`);
await page.goto(`${base}/?quality=${quality}&webgl`, { waitUntil: 'load', timeout: 120000 });

// Wait for the game to announce itself.
await page.waitForFunction(() => window.__joliet?.ready === true, null, { timeout: 180000 });

const manifest = await page.evaluate(() => ({
  id: window.__joliet.scene.manifest.id,
  title: window.__joliet.scene.manifest.title,
  anchors: window.__joliet.scene.manifest.anchors,
}));

if (sceneFilter && manifest.id !== sceneFilter) {
  console.log(`scene ${manifest.id} does not match --scene ${sceneFilter}; nothing to do`);
} else {
  const iter = flag('iter') ? Number(flag('iter')) : await nextIteration(manifest.id);
  const outDir = path.join(OUT_ROOT, manifest.id, `iter-${String(iter).padStart(2, '0')}`);
  await mkdir(outDir, { recursive: true });

  console.log(`→ ${manifest.title} (${manifest.id}) iteration ${iter}`);
  console.log(`  ${manifest.anchors.length} anchors → ${path.relative(ROOT, outDir)}`);

  const report = { scene: manifest.id, iteration: iter, quality, anchors: [], pageErrors: [] };

  for (const a of manifest.anchors) {
    await page.evaluate((n) => window.__joliet.gotoAnchor(n), a.name);
    // Sample FPS over a settled second rather than trusting the instantaneous
    // value, which is noisy right after a teleport.
    const stats = await page.evaluate(async () => {
      const samples = [];
      for (let i = 0; i < 24; i++) {
        await new Promise((r) => setTimeout(r, 60));
        samples.push(window.__joliet.stats());
      }
      const fps = samples.map((s) => s.fps).sort((x, y) => x - y);
      return {
        fpsMedian: fps[Math.floor(fps.length / 2)],
        fpsMin: fps[0],
        drawCalls: samples.at(-1).drawCalls,
        triangles: Math.round(samples.at(-1).triangles),
      };
    });

    const file = path.join(outDir, `${a.name}.png`);
    await page.screenshot({ path: file, type: 'png' });
    report.anchors.push({ name: a.name, note: a.note ?? '', ...stats });
    console.log(
      `  ✓ ${a.name.padEnd(18)} ${String(stats.fpsMedian).padStart(4)} fps · ` +
        `${String(stats.drawCalls).padStart(5)} draws · ` +
        `${String(stats.triangles).padStart(8)} tris`,
    );
  }

  report.pageErrors = pageErrors;
  await writeFile(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2));

  if (pageErrors.length) {
    console.log(`\n  ⚠ ${pageErrors.length} page error(s):`);
    for (const e of pageErrors.slice(0, 12)) console.log(`    ${e}`);
  } else {
    console.log('\n  ✓ zero page errors');
  }
}

await browser.close();
await server.close();
