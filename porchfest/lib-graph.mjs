// Pedestrian routing over the baked street graph. This exact code is inlined
// into the app — validated here against an OSRM foot matrix before shipping.

export const M_LAT = 111320, M_LON = 78700;             // metres per degree at ~45°N
export const mx = (lon) => lon * M_LON, my = (lat) => lat * M_LAT;

export function buildGraph(streets) {
  const { pts, ways } = streets;
  const adj = pts.map(() => []);                         // [{to, w}]
  const edges = [];                                      // [a, b] node pairs, for snapping
  for (const w of ways) {
    for (let i = 1; i < w.n.length; i++) {
      const a = w.n[i - 1], b = w.n[i];
      if (a === b) continue;
      const d = Math.hypot(mx(pts[a][1]) - mx(pts[b][1]), my(pts[a][0]) - my(pts[b][0]));
      adj[a].push({ to: b, w: d });
      adj[b].push({ to: a, w: d });
      edges.push([a, b, d]);
    }
  }
  return { pts, adj, edges };
}

// Nearest point on the nearest edge — lands a porch on the street out front
// rather than yanking it to the corner.
export function snap(g, lat, lon) {
  const px = mx(lon), py = my(lat);
  let best = { d2: Infinity };
  for (const [a, b] of g.edges) {
    const ax = mx(g.pts[a][1]), ay = my(g.pts[a][0]);
    const bx = mx(g.pts[b][1]), by = my(g.pts[b][0]);
    const dx = bx - ax, dy = by - ay, len2 = dx * dx + dy * dy;
    const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / len2));
    const qx = ax + t * dx, qy = ay + t * dy;
    const d2 = (px - qx) ** 2 + (py - qy) ** 2;
    if (d2 < best.d2) {
      best = { d2, a, b, t, offset: Math.sqrt(d2), da: t * Math.sqrt(len2), db: (1 - t) * Math.sqrt(len2),
               lat: (ay + t * dy) / M_LAT, lon: (ax + t * dx) / M_LON };
    }
  }
  return best;
}

// Dijkstra with a binary heap; returns {dist, prev} over all graph nodes.
export function dijkstra(g, sources) {
  const n = g.pts.length;
  const dist = new Float64Array(n).fill(Infinity);
  const prev = new Int32Array(n).fill(-1);
  const heap = [];
  const push = (d, v) => {
    heap.push([d, v]);
    let i = heap.length - 1;
    while (i > 0) { const p = (i - 1) >> 1; if (heap[p][0] <= heap[i][0]) break; [heap[p], heap[i]] = [heap[i], heap[p]]; i = p; }
  };
  const pop = () => {
    const top = heap[0], last = heap.pop();
    if (heap.length) { heap[0] = last; let i = 0;
      for (;;) { const l = 2 * i + 1, r = l + 1; let s = i;
        if (l < heap.length && heap[l][0] < heap[s][0]) s = l;
        if (r < heap.length && heap[r][0] < heap[s][0]) s = r;
        if (s === i) break; [heap[s], heap[i]] = [heap[i], heap[s]]; i = s; } }
    return top;
  };
  for (const [v, d] of sources) { if (d < dist[v]) { dist[v] = d; push(d, v); } }
  while (heap.length) {
    const [d, v] = pop();
    if (d > dist[v]) continue;
    for (const e of g.adj[v]) {
      const nd = d + e.w;
      if (nd < dist[e.to]) { dist[e.to] = nd; prev[e.to] = v; push(nd, e.to); }
    }
  }
  return { dist, prev };
}

// Walking distance (metres) + polyline between two snapped points.
export function routeBetween(g, s, t) {
  // same edge: walk straight along it
  if ((s.a === t.a && s.b === t.b) || (s.a === t.b && s.b === t.a)) {
    const sameDir = s.a === t.a;
    const d = Math.abs((sameDir ? s.da : s.da) - (sameDir ? t.da : t.db));
    return { dist: s.offset + d + t.offset, path: [[s.lat, s.lon], [t.lat, t.lon]] };
  }
  const { dist, prev } = dijkstra(g, [[s.a, s.da], [s.b, s.db]]);
  const ends = [[t.a, t.da], [t.b, t.db]];
  let best = null;
  for (const [v, tail] of ends) {
    const total = dist[v] + tail;
    if (Number.isFinite(total) && (!best || total < best.total)) best = { total, v };
  }
  if (!best) return { dist: Infinity, path: [[s.lat, s.lon], [t.lat, t.lon]] };
  const chain = [];
  for (let v = best.v; v !== -1; v = prev[v]) chain.push(v);
  chain.reverse();
  const path = [[s.lat, s.lon], ...chain.map(v => g.pts[v]), [t.lat, t.lon]];
  return { dist: s.offset + best.total + t.offset, path };
}
