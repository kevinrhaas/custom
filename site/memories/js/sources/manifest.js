// manifest.js — the simplest source: a JSON file next to the app
// (data/library.json) already in the Library shape (see ../library.js).
// Relative src/thumb/download paths resolve against the manifest's folder.

export async function loadManifest(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`Could not load the album (${res.status})`);
  const data = await res.json();
  const base = new URL(url, location.href);
  const abs = (u) => (u ? new URL(u, base).href : u);
  data.photos = (data.photos || []).map((p) => ({
    ...p,
    src: abs(p.src),
    thumb: abs(p.thumb || p.src),
    download: abs(p.download || p.src),
  }));
  return data;
}
