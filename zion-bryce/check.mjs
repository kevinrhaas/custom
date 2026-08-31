import { createHash } from 'node:crypto';
import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const projectRoot = dirname(fileURLToPath(import.meta.url));
const repoRoot = dirname(projectRoot);
const sourceRoot = join(projectRoot, 'src');
const publicRoot = join(repoRoot, 'site', 'zion-bryce');
const errors = [];

const expect = (condition, message) => { if (!condition) errors.push(message); };
const digest = (value) => createHash('sha256').update(value).digest('hex');
const read = (path) => readFile(path, 'utf8');

const sourceFiles = (await readdir(sourceRoot)).sort();
const publicFiles = (await readdir(publicRoot)).sort();
expect(JSON.stringify(sourceFiles) === JSON.stringify(publicFiles), 'source and deployed file lists differ');

for (const file of sourceFiles) {
  const source = await read(join(sourceRoot, file));
  const published = await read(join(publicRoot, file));
  expect(digest(source) === digest(published), `${file} differs between source and site mirror`);
}

for (const file of ['app.js', 'data.js', 'sw.js']) {
  const contents = await read(join(sourceRoot, file));
  const parsed = spawnSync(process.execPath, ['--input-type=module', '--check'], { input: contents, encoding: 'utf8' });
  expect(parsed.status === 0, `${file} has invalid JavaScript: ${parsed.stderr.trim()}`);
}

const html = await read(join(sourceRoot, 'index.html'));
const css = await read(join(sourceRoot, 'styles.css'));
const app = await read(join(sourceRoot, 'app.js'));
const data = await read(join(sourceRoot, 'data.js'));
const allPublicText = `${html}\n${css}\n${app}\n${data}`;

expect(html.includes('name="viewport"'), 'viewport meta tag is missing');
expect(html.includes('Skip to trip plan'), 'skip link is missing');
expect(html.includes('aria-live="polite"'), 'live-region status is missing');
expect(html.includes('manifest.webmanifest'), 'PWA manifest is not linked');
expect(html.includes('data-theme-mode'), 'pre-paint theme state is missing');
expect(css.includes('@media (max-width: 430px)'), 'small-mobile layout gate is missing');
expect(css.includes('@media (prefers-reduced-motion: reduce)'), 'reduced-motion support is missing');
expect(css.includes('@media print'), 'print layout is missing');
expect(app.includes('serviceWorker.register'), 'service worker registration is missing');
expect((await read(join(sourceRoot, 'sw.js'))).includes('fetch(request)'), 'offline shell is not network-first for version consistency');
expect(app.includes('forecastSuggestion'), 'forecast-assisted day swap is missing');
expect(app.includes('zionBryce.dayPack.v1'), 'saved day-specific packing state is missing');
expect(app.includes('dayExtrasTemplate'), 'day packing and tips renderer is missing');
expect(app.includes('zionBryce.brycePlan.v1'), 'saved Bryce planner state is missing');
expect(app.includes('renderBrycePlanner'), 'Bryce planning renderer is missing');
expect(html.includes('data-park-tab="zion"') && html.includes('data-park-tab="bryce"'), 'Zion/Bryce planning tabs are missing');
expect(html.includes('Shape the Bryce 24 hours'), 'Bryce planning panel is missing');
expect(data.includes('Bryce shuttle starts at 8:00 AM'), 'Bryce sunrise shuttle correction is missing');
expect(data.includes('Scout Cave does not fit'), 'Day 8 feasibility correction is missing');
expect(data.includes('Red Canyon arches'), 'Red Canyon route correction is missing');
expect(data.includes("chips: ['AA1497', 'LAS 12:56 PM PDT', 'ORD 7:19 PM CDT']"), 'confirmed return flight is missing');
expect(data.includes("chips: ['AA1497', 'ORD 10:30 AM CDT', 'LAS 12:25 PM PDT']"), 'confirmed outbound flight is missing');
expect(app.includes('20260913T195600Z'), 'timed return flight calendar event is missing');
expect((data.match(/\n    carry: \[/g) || []).length === 9, 'every fixed/activity day needs a carry checklist');
expect((data.match(/\n    tips: \[/g) || []).length === 9, 'every fixed/activity day needs field tips');
expect((data.match(/category: '/g) || []).length >= 45, 'master packing checklist is unexpectedly thin');
expect(css.includes('.day-extras'), 'responsive day packing/tips styling is missing');
expect(!/confirmation\s+(?:code|number)\s*[:#]\s*[A-Z0-9]{6}/i.test(allPublicText), 'a private confirmation code leaked into the public app');
expect(!allPublicText.includes('AA14970'), 'unverified return flight number leaked into the public app');
expect((data.match(/https:\/\//g) || []).length >= 25, 'research/source coverage is unexpectedly thin');

const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
expect(duplicateIds.length === 0, `duplicate HTML ids: ${[...new Set(duplicateIds)].join(', ')}`);

const localAssets = [...html.matchAll(/(?:href|src)="([^"#]+)"/g)]
  .map((match) => match[1])
  .filter((value) => !value.startsWith('http') && !value.startsWith('../') && !value.startsWith('data:'));
for (const asset of localAssets) {
  try { await stat(join(sourceRoot, asset)); }
  catch (error) { errors.push(`missing local asset referenced by HTML: ${asset}`); }
}

try { JSON.parse(await read(join(sourceRoot, 'manifest.webmanifest'))); }
catch (error) { errors.push(`manifest is invalid JSON: ${error.message}`); }

const landing = await read(join(repoRoot, 'site', 'index.html'));
const sitemap = await read(join(repoRoot, 'site', 'sitemap.xml'));
const readme = await read(join(repoRoot, 'README.md'));
expect(landing.includes('href="zion-bryce/"'), 'Custom landing page does not link the app');
expect(sitemap.includes('/custom/zion-bryce/'), 'sitemap does not include the app');
expect(readme.includes('Zion + Bryce Field Guide'), 'root README does not list the app');

if (errors.length) {
  console.error(`Zion + Bryce checks failed (${errors.length}):`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`Zion + Bryce checks passed: ${sourceFiles.length} mirrored files, ${ids.length} unique ids, privacy guard clean.`);
