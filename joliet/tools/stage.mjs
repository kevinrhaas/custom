#!/usr/bin/env node
/**
 * Stage the built bundle into the published site folder.
 *
 * This exists because the exclusion below kept getting forgotten. `public/`
 * holds the full CC0 texture library, which Vite copies into `dist/`
 * wholesale — but **nothing samples it**: every surface in the game is
 * generated procedurally by `src/core/Bakery.ts`. Shipping it took the
 * deployed bundle from 5.3 MB to 46 MB, spending the entire load budget for
 * zero pixels. It happened twice, both times after someone (me) rebuilt
 * without remembering the manual `rm`.
 *
 * A convention that has to be remembered is a bug waiting to happen, so it is
 * a build step now: `npm run stage`.
 *
 * When a scene genuinely starts sampling a texture set, delete its entry from
 * EXCLUDE rather than reaching for the copy command by hand.
 */

import { cp, rm, mkdir, readdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const DIST = path.join(ROOT, 'dist');
const OUT = path.resolve(ROOT, '..', 'site', 'joliet', 'app');

/** Paths under dist/ that must not ship, relative to dist/. */
const EXCLUDE = [
  // The whole CC0 PBR library. Unreferenced — all surfaces are procedural.
  'assets/textures',
  // Only the night HDRI is loaded; the dusk one is authored-but-unused.
  'assets/env/dusk-overcast-aarfontein_1k.hdr',
];

async function dirSize(dir) {
  let total = 0;
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    total += e.isDirectory() ? await dirSize(p) : (await stat(p)).size;
  }
  return total;
}

if (!existsSync(DIST)) {
  console.error('✗ no dist/ — run `npm run build` first');
  process.exit(1);
}

await rm(OUT, { recursive: true, force: true });
await mkdir(OUT, { recursive: true });
await cp(DIST, OUT, { recursive: true });

for (const rel of EXCLUDE) {
  await rm(path.join(OUT, rel), { recursive: true, force: true });
}

const mb = (await dirSize(OUT)) / 1e6;
console.log(`✓ staged → ${path.relative(path.resolve(ROOT, '..'), OUT)}  (${mb.toFixed(1)} MB)`);
for (const rel of EXCLUDE) console.log(`  excluded: ${rel}`);

// The load budget is 15 s to playable on 50 Mbps ≈ roughly 90 MB ceiling, but
// the real target is much tighter. Shout if the bundle drifts.
if (mb > 12) {
  console.error(`\n✗ bundle is ${mb.toFixed(1)} MB — expected well under 12 MB.`);
  console.error('  Something unreferenced is shipping. Check EXCLUDE in tools/stage.mjs.');
  process.exit(1);
}
