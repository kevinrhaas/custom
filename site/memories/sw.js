// sw.js — keeps the album opening even on a weak connection.
// App files: network first, cached copy if offline. Photos: cache first
// (they never change once scanned), including Google Drive images.
const VERSION = 'memories-v1';
const CORE = ['./', './index.html', './css/skins.css', './css/app.css', './css/gate.css', './js/app.js', './js/config.js',
  './js/library.js', './js/skins.js', './js/zip.js', './js/gate.js', './js/sources/manifest.js', './js/sources/drive.js',
  './vendor/polecat-shell/icons.js', './vendor/polecat-shell/access.js', './vendor/polecat-shell/fonts.css', './icon.svg'];
const PHOTOS = 'memories-photos-v1';

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => Promise.allSettled(CORE.map((u) => c.add(u)))));
  self.skipWaiting();
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION && k !== PHOTOS).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isPhoto = req.destination === 'image' && (url.pathname.includes('/photos/') || /googleusercontent\.com|drive\.google\.com/.test(url.host));
  if (isPhoto) {
    e.respondWith(caches.open(PHOTOS).then(async (c) => {
      const hit = await c.match(req);
      if (hit) return hit;
      const res = await fetch(req);
      if (res.ok || res.type === 'opaque') c.put(req, res.clone()).catch(() => {});
      return res;
    }));
    return;
  }
  if (url.origin !== self.location.origin) return;
  if (url.pathname.includes('/admin/')) return;
  e.respondWith(fetch(req).then((res) => {
    if (res.ok) { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); }
    return res;
  }).catch(() => caches.match(req).then((r) => r || caches.match('./index.html'))));
});
