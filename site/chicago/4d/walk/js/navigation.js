/**
 * navigation.js — compass and a truthful top-down overview of the loaded world.
 *
 * The overview is not a second map asset.  Land and water are sampled from the
 * same committed heightfield the walker stands on; streets and structure
 * outlines come from the same compiled scene index the 3D renderer places.
 * The only moving mark is the visitor: north stays at the top and the arrow
 * follows their bearing.
 */

const DEG = Math.PI / 180;
const CARDINALS = [
  'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
];

function normalBearing(value) {
  return ((Number(value) || 0) % 360 + 360) % 360;
}

function cardinal(bearing) {
  return CARDINALS[Math.round(normalBearing(bearing) / 22.5) % CARDINALS.length];
}

function structureOutlines(registry) {
  const out = [];
  for (const record of registry?.values?.() ?? []) {
    const sidecar = record.sidecar ?? {};
    const raw = sidecar.footprint;
    const polygon = Array.isArray(raw) ? raw : raw?.polygon;
    const placement = sidecar.placement ?? {};
    if (!Array.isArray(polygon) || polygon.length < 3) continue;
    const th = (placement.rotation_deg ?? 0) * DEG;
    const cos = Math.cos(th);
    const sin = Math.sin(th);
    const e0 = placement.local_e ?? 0;
    const n0 = placement.local_n ?? 0;
    out.push(polygon.map(([u, v]) => [
      e0 + u * cos + v * sin,
      n0 - u * sin + v * cos,
    ]));
  }
  return out;
}

export function createNavigation({ root, terrain, registry, streets } = {}) {
  const compass = root?.querySelector('#compass');
  const needle = root?.querySelector('#compass-needle');
  const direction = root?.querySelector('#compass-direction');
  const bearingLabel = root?.querySelector('#compass-bearing');
  const overview = root?.querySelector('#overview-map');
  const canvas = root?.querySelector('#overview-map-canvas');
  const streetReadout = root?.querySelector('#street-readout');
  const streetMode = root?.querySelector('#street-mode');
  const streetHistoric = root?.querySelector('#street-historic');
  const streetModern = root?.querySelector('#street-modern');
  const streetApproach = root?.querySelector('#street-approach');
  const ctx = canvas?.getContext('2d');
  const background = document.createElement('canvas');
  const bg = background.getContext('2d');
  const hf = terrain?.heightfield;
  const outlines = structureOutlines(registry);

  const bounds = hf?.loaded ? {
    eMin: hf.originE,
    eMax: hf.originE + hf.widthM,
    nMin: hf.originN,
    nMax: hf.originN + hf.depthM,
  } : { eMin: -320, eMax: 320, nMin: -400, nMax: 400 };

  let logicalWidth = 0;
  let logicalHeight = 0;
  let compassVisible = true;
  let mapVisible = true;
  let streetVisible = true;
  let player = { e: 0, n: 0, bearingDeg: 0 };
  let lastPaint = { e: Infinity, n: Infinity, bearingDeg: Infinity };
  let lastStreet = { e: Infinity, n: Infinity, bearingDeg: Infinity };
  let streetState = null;

  function point(e, n) {
    return {
      x: ((e - bounds.eMin) / (bounds.eMax - bounds.eMin)) * logicalWidth,
      y: ((bounds.nMax - n) / (bounds.nMax - bounds.nMin)) * logicalHeight,
    };
  }

  function paintBackground() {
    if (!bg || !logicalWidth || !logicalHeight) return;
    background.width = logicalWidth;
    background.height = logicalHeight;
    const image = bg.createImageData(logicalWidth, logicalHeight);
    const data = image.data;
    for (let y = 0; y < logicalHeight; y++) {
      const gy = hf?.loaded
        ? Math.min(hf.rows - 1, Math.round((logicalHeight - 1 - y) * (hf.rows - 1)
          / Math.max(1, logicalHeight - 1))) : 0;
      for (let x = 0; x < logicalWidth; x++) {
        const gx = hf?.loaded
          ? Math.min(hf.cols - 1, Math.round(x * (hf.cols - 1)
            / Math.max(1, logicalWidth - 1))) : 0;
        const h = hf?.loaded ? hf.data[gy * hf.cols + gx] : 1;
        const water = h < -0.02;
        const shade = Math.max(0, Math.min(18, Math.round(Math.max(0, h) * 4)));
        const i = (y * logicalWidth + x) * 4;
        data[i] = water ? 45 : 105 + shade;
        data[i + 1] = water ? 79 : 101 + shade;
        data[i + 2] = water ? 91 : 70 + Math.round(shade * 0.45);
        data[i + 3] = 255;
      }
    }
    bg.putImageData(image, 0, 0);

    // The same compiled paths the earth ribbons use.  Legal corridor width is
    // deliberately not drawn here: at this scale a centreline is the truthful
    // distinction between a street and a whole block of tan pixels.
    bg.save();
    bg.strokeStyle = 'rgba(77, 61, 36, .78)';
    bg.lineWidth = 0.9;
    for (const street of streets?.records ?? []) {
      bg.beginPath();
      street.path.forEach(([e, n], i) => {
        const screen = point(e, n);
        if (i === 0) bg.moveTo(screen.x, screen.y); else bg.lineTo(screen.x, screen.y);
      });
      bg.stroke();
    }
    bg.restore();

    // Every compiled footprint, including water-anchored bridges and piers.
    bg.save();
    bg.fillStyle = 'rgba(244, 235, 208, .82)';
    bg.strokeStyle = 'rgba(42, 34, 22, .72)';
    bg.lineWidth = 0.7;
    for (const polygon of outlines) {
      bg.beginPath();
      polygon.forEach(([e, n], i) => {
        const screen = point(e, n);
        if (i === 0) bg.moveTo(screen.x, screen.y); else bg.lineTo(screen.x, screen.y);
      });
      bg.closePath();
      bg.fill();
      bg.stroke();
    }
    bg.restore();
  }

  function resize() {
    if (!canvas || !ctx) return;
    logicalWidth = window.innerWidth <= 560 ? 188 : 248;
    logicalHeight = Math.max(76, Math.round(logicalWidth
      * (bounds.nMax - bounds.nMin) / (bounds.eMax - bounds.eMin)));
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.style.width = `${logicalWidth}px`;
    canvas.style.height = `${logicalHeight}px`;
    canvas.width = Math.round(logicalWidth * dpr);
    canvas.height = Math.round(logicalHeight * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    paintBackground();
    lastPaint = { e: Infinity, n: Infinity, bearingDeg: Infinity };
    paintMap();
  }

  function paintMap() {
    if (!ctx || !canvas || !mapVisible || overview?.hasAttribute('hidden')) return;
    const dpr = canvas.width / logicalWidth;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, logicalWidth, logicalHeight);
    ctx.drawImage(background, 0, 0, logicalWidth, logicalHeight);

    const screen = point(player.e, player.n);
    ctx.save();
    ctx.translate(screen.x, screen.y);
    ctx.rotate(normalBearing(player.bearingDeg) * DEG);
    ctx.beginPath();
    ctx.moveTo(0, -8);
    ctx.lineTo(5.2, 6);
    ctx.lineTo(0, 3.5);
    ctx.lineTo(-5.2, 6);
    ctx.closePath();
    ctx.fillStyle = '#f4b54f';
    ctx.strokeStyle = '#17140c';
    ctx.lineWidth = 1.4;
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }

  function update({ e = 0, n = 0, bearingDeg = 0 } = {}) {
    const b = normalBearing(bearingDeg);
    player = { e, n, bearingDeg: b };
    if (needle) needle.style.transform = `translate(-50%, -88%) rotate(${b}deg)`;
    if (direction) direction.textContent = cardinal(b);
    if (bearingLabel) bearingLabel.textContent = `${String(Math.round(b) % 360).padStart(3, '0')}°`;
    if (compass) compass.setAttribute('aria-label', `Heading ${cardinal(b)}, ${Math.round(b)} degrees`);
    if (overview) overview.setAttribute('aria-label',
      `Overview map. Position east ${Math.round(e)} metres, north ${Math.round(n)} metres; heading ${cardinal(b)}.`);

    if (Math.hypot(e - lastStreet.e, n - lastStreet.n) > 0.35
        || Math.abs(b - lastStreet.bearingDeg) > 2) {
      streetState = streets?.status?.(e, n, b) ?? null;
      paintStreet();
      lastStreet = { e, n, bearingDeg: b };
    }

    if (Math.hypot(e - lastPaint.e, n - lastPaint.n) > 0.08
        || Math.abs(b - lastPaint.bearingDeg) > 0.35) {
      paintMap();
      lastPaint = { e, n, bearingDeg: b };
    }
  }

  function joined(items, key) {
    return [...new Set(items.map((s) => s[key]).filter(Boolean))].join(' & ');
  }

  function paintStreet() {
    const show = streetVisible && !!streetState;
    streetReadout?.toggleAttribute('hidden', !show);
    if (!show) return;
    const records = streetState.streets ?? [];
    const historic = joined(records, 'name_1835');
    const modern = joined(records, 'name_2026');
    let mode = 'On street';
    if (streetState.mode === 'intersection') mode = 'At intersection';
    if (streetState.mode === 'ahead') mode = `Ahead · ${Math.round(streetState.distance_m)} m`;
    if (streetMode) streetMode.textContent = mode;
    if (streetHistoric) streetHistoric.textContent = historic;
    if (streetModern) streetModern.textContent = `Today: ${modern}`;

    const upcoming = streetState.upcoming;
    if (streetApproach) {
      const text = upcoming
        ? `Approaching ${upcoming.street.name_1835} · ${Math.round(upcoming.ahead_m)} m`
        : '';
      streetApproach.textContent = text;
      streetApproach.toggleAttribute('hidden', !text);
    }
    const approachLabel = upcoming
      ? `. Approaching ${upcoming.street.name_1835}, today ${upcoming.street.name_2026}, in ${Math.round(upcoming.ahead_m)} metres.`
      : '';
    streetReadout?.setAttribute('aria-label',
      `${mode}. In 1835: ${historic}. Today: ${modern}${approachLabel}`);
  }

  function setCompassVisible(on) {
    compassVisible = !!on;
    compass?.toggleAttribute('hidden', !compassVisible);
    return compassVisible;
  }

  function setMapVisible(on) {
    mapVisible = !!on;
    overview?.toggleAttribute('hidden', !mapVisible);
    if (mapVisible) {
      lastPaint = { e: Infinity, n: Infinity, bearingDeg: Infinity };
      paintMap();
    }
    return mapVisible;
  }

  function setStreetVisible(on) {
    streetVisible = !!on;
    paintStreet();
    return streetVisible;
  }

  window.addEventListener('resize', resize);
  resize();

  return {
    bounds,
    update,
    setCompassVisible,
    setMapVisible,
    setStreetVisible,
    get compassVisible() { return compassVisible; },
    get mapVisible() { return mapVisible; },
    get streetVisible() { return streetVisible; },
    get streetState() { return streetState; },
    snapshot() {
      return {
        ...player, compassVisible, mapVisible, streetVisible, streetState,
        bounds: { ...bounds },
      };
    },
  };
}
