/**
 * Touch-path probe for the PRODUCTION bundle.
 *
 * Same shape as probe-build.mjs — serve site/joliet/app, boot it headless —
 * but in a phone-sized context with touch emulation on, driving real
 * multi-touch through CDP `Input.dispatchTouchEvent` (Playwright's
 * `page.touchscreen` can only tap, and the whole point of this layer is
 * drags, and two of them at once).
 *
 *   node tools/touch-probe.mjs
 */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const ROOT = '/home/user/custom/site/joliet/app';
const SHOTS = '/home/user/custom/joliet/artifacts/touch';
const PORT = 5311;
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
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] ?? 'application/octet-stream' });
    res.end(buf);
  } catch {
    res.writeHead(404);
    res.end('nope');
  }
});
await new Promise((r) => srv.listen(PORT, r));
await mkdir(SHOTS, { recursive: true });

const browser = await chromium.launch({
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

const ctx = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  hasTouch: true,
  isMobile: true,
});
const page = await ctx.newPage();
const errs = [];
// Babylon logs a console error when it probes for WebGPU and does not find it,
// then falls back to WebGL2. It happens on the desktop path too (see
// probe-build.mjs output) and is not a touch regression, so it is filtered
// here rather than counted.
const KNOWN = /fatal error occurred during WebGPU creation/i;
page.on('pageerror', (e) => errs.push(String(e).slice(0, 200)));
page.on('console', (m) => {
  if (m.type() === 'error' && !KNOWN.test(m.text())) errs.push('console: ' + m.text().slice(0, 200));
});

const results = [];
const check = (name, ok, detail = '') => {
  results.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  — ' + detail : ''}`);
};

const cdp = await ctx.newCDPSession(page);
let seq = 0;
const touch = (type, points) =>
  cdp.send('Input.dispatchTouchEvent', {
    type,
    touchPoints: points.map((p) => ({ x: p.x, y: p.y, id: p.id, radiusX: 12, radiusY: 12, force: 1 })),
    timestamp: (Date.now() + seq++) / 1000,
  });

await page.goto(`http://localhost:${PORT}/?scene=perimeter`, { waitUntil: 'load', timeout: 120000 });

let ready = false;
try {
  await page.waitForFunction(() => window.__joliet?.ready === true, null, { timeout: 300000 });
  ready = true;
} catch {
  /* reported below */
}
check('boots on a touch device', ready);
if (!ready) {
  console.log(errs.slice(0, 5).join('\n'));
  await browser.close();
  srv.close();
  process.exit(1);
}

// --- detection, notice, quality ------------------------------------------
const env = await page.evaluate(() => ({
  coarse: matchMedia('(pointer: coarse)').matches,
  noHover: matchMedia('(hover: none)').matches,
  maxTouchPoints: navigator.maxTouchPoints,
  fatal: !!document.querySelector('.fatal'),
  layer: !!document.getElementById('touch'),
  buttons: [...document.querySelectorAll('.tbtn')].map((b) => {
    const r = b.getBoundingClientRect();
    return { label: b.textContent, w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) };
  }),
  quality: JSON.parse(localStorage.getItem('joliet.settings.v1') ?? '{}').quality,
  scaleLevel: window.__joliet.renderer.engine.getHardwareScalingLevel(),
}));
check('no touch notice', !env.fatal);
check('touch layer mounted', env.layer, `coarse=${env.coarse} hover:none=${env.noHover} pts=${env.maxTouchPoints}`);
check('quality forced to low', env.quality === 'low', `quality=${env.quality}`);
check(
  'hardware scaling 1.6–2.0',
  env.scaleLevel >= 1.6 && env.scaleLevel <= 2.0,
  `level=${env.scaleLevel}`,
);
check(
  'buttons ≥ 44×44 and clear of centre',
  env.buttons.length > 0 &&
    env.buttons.every((b) => b.w >= 44 && b.h >= 44) &&
    env.buttons.every((b) => b.y > 844 * 0.6),
  JSON.stringify(env.buttons),
);

const state = () =>
  page.evaluate(() => {
    const p = window.__joliet.player;
    return {
      pos: { x: p.position.x, y: p.position.y, z: p.position.z },
      fwd: { x: p.forward.x, z: p.forward.z },
      lamp: p.headlamp.isEnabled(),
    };
  });

// --- 1. left half drags = movement ---------------------------------------
{
  const before = await state();
  await touch('touchStart', [{ x: 110, y: 620, id: 1 }]);
  for (let i = 1; i <= 6; i++) {
    await touch('touchMove', [{ x: 110, y: 620 - i * 12, id: 1 }]);
    await page.waitForTimeout(40);
  }
  await page.waitForTimeout(1600);
  await touch('touchEnd', []);
  const after = await state();
  const moved = Math.hypot(after.pos.x - before.pos.x, after.pos.z - before.pos.z);
  const turned = Math.hypot(after.fwd.x - before.fwd.x, after.fwd.z - before.fwd.z);
  check('left-half drag moves the player', moved > 0.4, `moved ${moved.toFixed(2)} m`);
  check('...without turning the view', turned < 0.02, `Δfwd ${turned.toFixed(4)}`);
}

// --- 2. right half drags = look ------------------------------------------
{
  const before = await state();
  await touch('touchStart', [{ x: 280, y: 400, id: 2 }]);
  for (let i = 1; i <= 8; i++) {
    await touch('touchMove', [{ x: 280 + i * 12, y: 400, id: 2 }]);
    await page.waitForTimeout(40);
  }
  await page.waitForTimeout(400);
  await touch('touchEnd', []);
  const after = await state();
  const moved = Math.hypot(after.pos.x - before.pos.x, after.pos.z - before.pos.z);
  const turned = Math.hypot(after.fwd.x - before.fwd.x, after.fwd.z - before.fwd.z);
  const deg = (Math.atan2(after.fwd.x, after.fwd.z) - Math.atan2(before.fwd.x, before.fwd.z)) * 57.2958;
  check('right-half drag turns the view', turned > 0.05, `${deg.toFixed(1)}° for a 96 px swipe`);
  check('...without moving the player', moved < 0.15, `moved ${moved.toFixed(3)} m`);
}

// --- 3. both at once, plus a button --------------------------------------
{
  const before = await state();
  await touch('touchStart', [{ x: 110, y: 620, id: 3 }]);
  await touch('touchStart', [
    { x: 110, y: 620, id: 3 },
    { x: 280, y: 400, id: 4 },
  ]);
  for (let i = 1; i <= 8; i++) {
    await touch('touchMove', [
      { x: 110, y: 620 - i * 10, id: 3 },
      { x: 280 - i * 10, y: 400, id: 4 },
    ]);
    await page.waitForTimeout(45);
  }
  await page.waitForTimeout(900);

  // A third finger on a button while both sticks are live.
  const lamp = await page.evaluate(() => {
    const b = document.querySelector('[data-key="lamp"]');
    const r = b.getBoundingClientRect();
    return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
  });
  const lampBefore = (await state()).lamp;
  await touch('touchStart', [
    { x: 110, y: 540, id: 3 },
    { x: 200, y: 400, id: 4 },
    { x: lamp.x, y: lamp.y, id: 5 },
  ]);
  await page.waitForTimeout(200);
  await touch('touchEnd', [
    { x: 110, y: 540, id: 3 },
    { x: 200, y: 400, id: 4 },
  ]);
  await page.waitForTimeout(150);
  const after = await state();
  await touch('touchEnd', []);

  const moved = Math.hypot(after.pos.x - before.pos.x, after.pos.z - before.pos.z);
  const turned = Math.hypot(after.fwd.x - before.fwd.x, after.fwd.z - before.fwd.z);
  check('move + look simultaneously', moved > 0.4 && turned > 0.05, `moved ${moved.toFixed(2)} m, Δfwd ${turned.toFixed(3)}`);
  check('button works while both sticks are held', after.lamp !== lampBefore, `headlamp ${lampBefore} → ${after.lamp}`);
}

// --- 4. the stick curve: partial deflection walks, full deflection sprints --
{
  // Both runs start from the spawn with full stamina and a clear approach, so
  // this measures the response curve rather than whichever wall the earlier
  // tests parked the player against.
  const reset = () =>
    page.evaluate(() => {
      const p = window.__joliet.player;
      const s = window.__joliet.scene.manifest.spawn;
      p.position.set(s.position[0], s.position[1], s.position[2]);
      p.velocity.setAll(0);
      p.stamina = 1;
    });

  const runFor = async (deflectionPx, id) => {
    await reset();
    await touch('touchStart', [{ x: 110, y: 620, id }]);
    await touch('touchMove', [{ x: 110, y: 620 - deflectionPx, id }]);
    await page.waitForTimeout(300); // let acceleration settle
    const t0 = await state();
    await page.waitForTimeout(1000);
    const t1 = await state();
    await touch('touchEnd', []);
    await page.waitForTimeout(120);
    return {
      speed: Math.hypot(t1.pos.x - t0.pos.x, t1.pos.z - t0.pos.z),
      sprintClass: await page.evaluate(() =>
        document.querySelector('.touch-stick').classList.contains('sprint'),
      ),
    };
  };

  // 48/58 = 0.83 of the radius: hard over, but under the sprint threshold.
  const walk = await runFor(48, 6);
  const run = await runFor(58, 7);
  check(
    'sprint is a stick gesture, not a button',
    !walk.sprintClass && run.sprintClass,
    `83% deflection sprinting=${walk.sprintClass}, 100%=${run.sprintClass}`,
  );
  check(
    'pushing past the rim actually runs',
    run.speed > walk.speed * 1.6 && run.speed > 2.5,
    `walk ${walk.speed.toFixed(2)} m/s → sprint ${run.speed.toFixed(2)} m/s`,
  );
}

// --- 5. the page never scrolls -------------------------------------------
{
  await touch('touchStart', [{ x: 195, y: 300, id: 7 }]);
  for (let i = 1; i <= 5; i++) await touch('touchMove', [{ x: 195, y: 300 + i * 40, id: 7 }]);
  await touch('touchEnd', []);
  const scrolled = await page.evaluate(() => window.scrollY + document.documentElement.scrollTop);
  check('page does not scroll under a drag', scrolled === 0, `scrollY=${scrolled}`);
}

// --- 6. crouch button ------------------------------------------------------
{
  const c = await page.evaluate(() => {
    const r = document.querySelector('[data-key="crouch"]').getBoundingClientRect();
    return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
  });
  await touch('touchStart', [{ x: c.x, y: c.y, id: 8 }]);
  await page.waitForTimeout(120);
  await touch('touchEnd', []);
  await page.waitForTimeout(200);
  const stance = await page.evaluate(() => window.__joliet.player.stance);
  check('crouch button toggles stance', stance === 'crouch', `stance=${stance}`);
}

await page.waitForTimeout(600);
await page.screenshot({ path: path.join(SHOTS, 'touch-390x844.png') });

// Idle shot with a finger down, so the stick is visible in the capture.
await touch('touchStart', [{ x: 120, y: 600, id: 9 }]);
await touch('touchMove', [{ x: 148, y: 566, id: 9 }]);
await page.waitForTimeout(300);
await page.screenshot({ path: path.join(SHOTS, 'touch-stick-390x844.png') });
await touch('touchEnd', []);

check('zero page errors', errs.length === 0, errs.slice(0, 3).join(' | '));

const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
console.log(`shots → ${SHOTS}`);

await browser.close();
srv.close();
process.exit(failed.length ? 1 : 0);
