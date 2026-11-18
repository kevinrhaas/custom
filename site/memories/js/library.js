// -----------------------------------------------------------------------
// library.js — loads the album from whichever source config.js names and
// hands the UI one normalized shape. Sources never touch the DOM.
//
// THE CONTRACT (every source returns this; the UI reads only this):
//
//   Library = {
//     chapters: [ { id, title, blurb?, cover? } ],   // display order
//     photos:   [ Photo ],                            // any order; normalized here
//   }
//   Photo = {
//     id:        string, unique
//     chapter:   chapter id
//     title:     short human title          "Wedding day"
//     caption?:  a sentence or two          "June made her own dress…"
//     year?:     number | null              1948
//     approx?:   boolean  (true → "about 1948")
//     place?:    string                     "St. Mary's, Joliet"
//     people?:   [string]  (optional — derived from config.people if absent)
//     kind?:     'photo' | 'keepsake' | 'letter'   (default 'photo')
//     src:       display URL, ~1600px long edge
//     thumb:     grid URL, ~480px long edge
//     download:  URL of the best original to save
//     downloadName?: suggested file name
//     w?, h?:    pixel size of src (for layout without jank)
//   }
//
// normalize() adds: decade, people (if missing), search (lowercased text).
// -----------------------------------------------------------------------

const CACHE_KEY = (prefix) => `${prefix}.library.v1`;

export async function loadLibrary(config) {
  const prefix = config.access?.prefix || 'memories';
  let raw;
  if (config.source === 'drive' && config.drive?.apiKey && config.drive?.folderId) {
    const { loadDrive } = await import('./sources/drive.js');
    try {
      raw = await loadDrive(config.drive);
      try { localStorage.setItem(CACHE_KEY(prefix), JSON.stringify({ at: Date.now(), raw })); } catch {}
    } catch (err) {
      // Offline or Drive hiccup: fall back to the last good copy on this device.
      const cached = readCache(prefix);
      if (!cached) throw err;
      raw = cached;
      raw.stale = true;
    }
  } else {
    const { loadManifest } = await import('./sources/manifest.js');
    raw = await loadManifest(config.manifestUrl || 'data/library.json');
  }
  return normalize(raw, config);
}

function readCache(prefix) {
  try { return JSON.parse(localStorage.getItem(CACHE_KEY(prefix)) || 'null')?.raw || null; } catch { return null; }
}

export function normalize(raw, config) {
  const people = (config.people || []).slice().sort((a, b) => b.length - a.length);
  const chapters = (raw.chapters || []).map((c, i) => ({ blurb: '', ...c, order: i }));
  const known = new Set(chapters.map((c) => c.id));
  const photos = (raw.photos || []).map((p) => {
    const year = Number.isFinite(+p.year) && p.year !== null && p.year !== '' ? +p.year : null;
    const text = `${p.title || ''} ${p.caption || ''}`;
    const found = p.people && p.people.length ? p.people : people.filter((n) => wordIn(text, n));
    const ph = {
      kind: 'photo', caption: '', place: '', approx: false,
      ...p,
      year,
      decade: year ? Math.floor(year / 10) * 10 : null,
      people: found,
    };
    ph.search = [ph.title, ph.caption, ph.place, ph.people.join(' '), year || '', ph.decade ? `${ph.decade}s` : '', ph.kind]
      .join(' ').toLowerCase();
    return ph;
  });
  // Any photo pointing at an unknown chapter gets a catch-all chapter.
  if (photos.some((p) => !known.has(p.chapter))) {
    chapters.push({ id: '_more', title: 'More treasures', blurb: '', order: chapters.length });
    photos.forEach((p) => { if (!known.has(p.chapter)) p.chapter = '_more'; });
  }
  const byChapter = new Map(chapters.map((c) => [c.id, []]));
  photos.forEach((p) => byChapter.get(p.chapter).push(p));
  for (const list of byChapter.values()) list.sort(byYearThenTitle);
  // Final order: chapter order, then year within a chapter.
  const ordered = chapters.flatMap((c) => byChapter.get(c.id));
  chapters.forEach((c) => {
    const list = byChapter.get(c.id);
    c.count = list.length;
    c.cover = c.cover && list.find((p) => p.id === c.cover) ? c.cover : list[0]?.id;
    const years = list.map((p) => p.year).filter(Boolean);
    c.span = years.length ? [Math.min(...years), Math.max(...years)] : null;
  });
  return { chapters: chapters.filter((c) => c.count), photos: ordered, stale: !!raw.stale };
}

function byYearThenTitle(a, b) {
  return (a.year ?? 9999) - (b.year ?? 9999) || String(a.title).localeCompare(String(b.title));
}

function wordIn(text, name) {
  const esc = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(^|[^\\p{L}])${esc}([^\\p{L}]|$)`, 'iu').test(text);
}

export function yearLabel(p) {
  if (!p.year) return '';
  return p.approx ? `about ${p.year}` : String(p.year);
}
