/**
 * Boot-probe the PRODUCTION bundle (not the dev server).
 *
 * The dev server's optimize-deps cache goes stale whenever imports change,
 * which produces 504s that look like real failures and are not. The built
 * bundle is what actually ships, so that is what gets verified.
 */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const ROOT = '/home/user/custom/site/joliet/app';
const TYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.hdr': 'application/octet-stream',
};

const srv = createServer(async (req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/index.html';
  try {
    const buf = await readFile(path.join(ROOT, p));
    res.writeHead(200, {
      'content-type': TYPES[path.extname(p)] ?? 'application/octet-stream',
    });
    res.end(buf);
  } catch {
    res.writeHead(404);
    res.end('nope');
  }
});
await new Promise((r) => srv.listen(5310, r));

const b = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: [
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--disable-dev-shm-usage',
    '--disable-renderer-backgrounding',
    '--disable-background-timer-throttling',
  ],
});

for (const scene of ['perimeter', 'void']) {
  const pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
  const errs = [];
  pg.on('pageerror', (e) => errs.push(String(e).slice(0, 170)));
  pg.on('console', (m) => {
    if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 170));
  });
  await pg.goto(`http://localhost:5310/?scene=${scene}`, {
    waitUntil: 'load',
    timeout: 120000,
  });
  let ok = false;
  try {
    await pg.waitForFunction(() => window.__joliet?.ready === true, null, {
      timeout: 240000,
    });
    ok = true;
  } catch {
    /* fall through and report */
  }
  const id = ok ? await pg.evaluate(() => window.__joliet.scene.manifest.id) : '(never ready)';
  console.log(`${scene.padEnd(10)} ready=${ok}  id=${id}  errors=${errs.length}`);
  for (const e of errs.slice(0, 4)) console.log('   ', e);
  await pg.close();
}

await b.close();
srv.close();
