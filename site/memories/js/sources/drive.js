// -----------------------------------------------------------------------
// drive.js — the Google Drive source.
//
// Reads a Drive folder shared "Anyone with the link can view" using a
// browser API key (Drive API v3, no sign-in) and returns the raw Library
// shape described in ../library.js:  { chapters, photos }.
//
//   Root folder
//   ├─ 01 Early years/        → chapter "Early years" (folder description = blurb)
//   │   ├─ 1948 - Wedding day.jpg   → title "Wedding day", year 1948
//   │   └─ More from the farm/      → nested one level: flattened into "Early years"
//   ├─ 02 Keepsakes/          → chapter; photos default to kind 'keepsake'
//   └─ loose.jpg              → chapter "The album"
//
// A file's Drive "Description" becomes its caption. Inside it:
//   #keepsake / #letter   → kind (the tag is removed from the caption)
//   Place: Joliet         → place (the line is removed from the caption)
//
// Image URLs: lh3.googleusercontent.com/d/<id> serves resized copies of
// publicly shared files; drive.google.com/thumbnail is the fallback the UI
// swaps to if lh3 fails (img onerror → photo.fallback / photo.thumbFallback).
// -----------------------------------------------------------------------

const API = 'https://www.googleapis.com/drive/v3/files';
const FOLDER = 'application/vnd.google-apps.folder';
const FILE_FIELDS =
  'id,name,mimeType,description,imageMediaMetadata(width,height,rotation,time),createdTime';
const SRC_W = 1600;
const THUMB_W = 480;
const ROOT_CHAPTER = { id: '_album', title: 'The album', blurb: '' };

// ---- public entry ------------------------------------------------------

export async function loadDrive({ apiKey, folderId } = {}) {
  apiKey = String(apiKey || '').trim();
  folderId = folderIdFrom(folderId);
  if (!apiKey) throw friendly('no-key', 'The album needs a Google API key before it can read the Drive folder.');
  if (!folderId) throw friendly('no-folder', 'The album needs the Google Drive folder ID before it can show photos.');

  // 1. Check the folder itself. (Listing an unshared folder just returns
  //    nothing, so this is the only way to tell "not shared" from "empty".)
  const root = await driveGet(`${API}/${encodeURIComponent(folderId)}`, {
    key: apiKey,
    fields: 'id,name,mimeType',
    supportsAllDrives: 'true',
  });
  if (root.mimeType !== FOLDER) {
    throw friendly('not-folder', 'That link points to a single file, not a folder. Use the link to the whole photo folder.');
  }

  // 2. Root: subfolders become chapters, loose images go to "The album".
  const top = await listFolder(apiKey, folderId);
  const folders = top.filter((f) => f.mimeType === FOLDER);
  const chapters = [];
  const photos = [];

  const chapterLists = await mapLimit(folders, 6, async (folder) => {
    const items = await listFolder(apiKey, folder.id);
    const nested = items.filter((f) => f.mimeType === FOLDER);
    const nestedItems = await mapLimit(nested, 4, async (sub) =>
      (await listFolder(apiKey, sub.id)).filter(isImage).map((f) => ({ f, folderName: sub.name })));
    return [
      ...items.filter(isImage).map((f) => ({ f, folderName: folder.name })),
      ...nestedItems.flat(),
    ];
  });

  folders.forEach((folder, i) => {
    const list = chapterLists[i];
    if (!list.length) return;
    chapters.push({
      id: folder.id,
      title: chapterTitle(folder.name),
      blurb: tidySpace(folder.description || ''),
    });
    for (const { f, folderName } of list) photos.push(toPhoto(f, folder.id, kindFromFolder(folderName) || kindFromFolder(folder.name)));
  });

  const loose = top.filter(isImage);
  if (loose.length) {
    // Stragglers sit after the real chapters; on their own they are the album.
    chapters.push({ ...ROOT_CHAPTER });
    for (const f of loose) photos.push(toPhoto(f, ROOT_CHAPTER.id, null));
  }

  if (!photos.length) {
    throw friendly('empty', 'The Google Drive folder is shared, but there are no photos in it yet.');
  }
  return { chapters, photos };
}

// ---- Drive calls -------------------------------------------------------

async function listFolder(key, parentId) {
  const out = [];
  let pageToken = '';
  do {
    const page = await driveGet(API, {
      q: `'${parentId.replace(/'/g, "\\'")}' in parents and trashed=false`,
      key,
      fields: `nextPageToken,files(${FILE_FIELDS})`,
      pageSize: '1000',
      orderBy: 'name',
      supportsAllDrives: 'true',
      includeItemsFromAllDrives: 'true',
      ...(pageToken ? { pageToken } : {}),
    });
    out.push(...(page.files || []));
    pageToken = page.nextPageToken || '';
  } while (pageToken);
  return out;
}

async function driveGet(base, params) {
  const url = `${base}?${new URLSearchParams(params)}`;
  let res;
  try {
    res = await fetch(url, { cache: 'no-cache' });
  } catch {
    throw friendly('network', "We couldn't reach Google Drive. Check the internet connection and try again.");
  }
  if (res.ok) return res.json();

  let body = null;
  try { body = await res.json(); } catch {}
  const err = body?.error || {};
  const msg = String(err.message || '');
  const reasons = [err.status, ...(err.errors || []).map((e) => e.reason), ...(err.details || []).map((d) => d.reason)]
    .filter(Boolean).join(' ');

  if (res.status === 404) {
    throw friendly('not-shared',
      "We couldn't open the Google Drive folder. Make sure it's shared as \"Anyone with the link\" and the folder ID is right.");
  }
  if (res.status === 400 && /API_KEY_INVALID|keyInvalid|API key not valid/i.test(reasons + msg)) {
    throw friendly('key', 'The Google API key in the album settings is not valid. Check that it was copied in full.');
  }
  if (res.status === 429 || /RateLimit|dailyLimit|quota|RATE_LIMIT/i.test(reasons + msg)) {
    throw friendly('quota', 'Google Drive is busy right now. Please wait a minute and try again.');
  }
  if (res.status === 403) {
    if (/accessNotConfigured|SERVICE_DISABLED|has not been used|is disabled/i.test(reasons + msg)) {
      throw friendly('api-disabled', 'The Google Drive API is not turned on for this API key. Turn it on in the Google Cloud console.');
    }
    if (/referer|referrer|API_KEY_HTTP_REFERRER_BLOCKED|API_KEY_SERVICE_BLOCKED|blocked/i.test(reasons + msg)) {
      throw friendly('referrer',
        `The Google API key isn't allowed on this web address (${safeOrigin()}). Add it to the key's website restrictions.`);
    }
    throw friendly('forbidden',
      "Google Drive said no. Check the API key and that the folder is shared as \"Anyone with the link\".");
  }
  throw friendly('drive', `Google Drive had a problem (${res.status}). Please try again in a little while.`);
}

function friendly(code, message) {
  const e = new Error(message);
  e.code = code;
  e.friendly = true;
  return e;
}

function safeOrigin() {
  try { return location.host || 'this page'; } catch { return 'this page'; }
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let next = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (next < items.length) {
      const i = next++;
      out[i] = await fn(items[i], i);
    }
  });
  await Promise.all(workers);
  return out;
}

// ---- shaping -----------------------------------------------------------

function isImage(f) {
  return /^image\//i.test(f.mimeType || '');
}

function toPhoto(f, chapterId, folderKind) {
  const named = parseName(f.name);
  const desc = parseDescription(f.description);
  const meta = f.imageMediaMetadata || {};

  let { year, approx } = named;
  if (year == null) {
    const camYear = metaYear(meta.time);
    const addedYear = f.createdTime ? new Date(f.createdTime).getUTCFullYear() : null;
    // A scanner stamps the scan date, not the day the photo was taken. Only
    // trust the camera date when it's older than the upload year.
    if (camYear && (!addedYear || camYear < addedYear)) { year = camYear; approx = false; }
  }

  let w = +meta.width || undefined;
  let h = +meta.height || undefined;
  if (w && h && (meta.rotation === 1 || meta.rotation === 3)) [w, h] = [h, w];
  if (w && h && w > SRC_W) { h = Math.round((h * SRC_W) / w); w = SRC_W; }

  const title = named.title || firstWords(desc.caption) || 'A family photo';
  const id = encodeURIComponent(f.id);
  const photo = {
    id: f.id,
    chapter: chapterId,
    title,
    caption: desc.caption,
    year: year ?? null,
    approx: !!approx,
    kind: desc.kind || folderKind || 'photo',
    src: `https://lh3.googleusercontent.com/d/${id}=w${SRC_W}`,
    thumb: `https://lh3.googleusercontent.com/d/${id}=w${THUMB_W}`,
    fallback: `https://drive.google.com/thumbnail?id=${id}&sz=w${SRC_W}`,
    thumbFallback: `https://drive.google.com/thumbnail?id=${id}&sz=w${THUMB_W}`,
    download: `https://drive.google.com/uc?export=download&id=${id}`,
    downloadName: f.name,
  };
  if (desc.place) photo.place = desc.place;
  if (w && h) { photo.w = w; photo.h = h; }
  return photo;
}

function metaYear(time) {
  // EXIF style "2019:06:12 14:22:01" (sometimes ISO).
  const m = /^(\d{4})/.exec(String(time || ''));
  const y = m ? +m[1] : null;
  return y && plausibleYear(y) ? y : null;
}

function plausibleYear(y) {
  return y >= 1800 && y <= new Date().getFullYear() + 1;
}

function firstWords(text) {
  const s = String(text || '').split(/(?<=[.!?])\s|\n/)[0].trim();
  if (!s) return '';
  return s.length > 60 ? `${s.slice(0, 57).replace(/\s+\S*$/, '')}…` : s.replace(/[.]$/, '');
}

// ---- names & descriptions (exported for tests and the admin check) -----

/** "01 Early years" → "Early years"; "1950s" stays "1950s". */
export function chapterTitle(name) {
  let s = String(name || '').replace(/_/g, ' ');
  s = s.replace(/^\s*\d{1,3}(?:[.)]\s*|\s*[-–—]\s*|\s+)(?=\S)/, '');
  return tidyCase(tidySpace(s)) || 'Photos';
}

function kindFromFolder(name) {
  const s = String(name || '').toLowerCase();
  if (/keepsake/.test(s)) return 'keepsake';
  if (/\bletters?\b/.test(s)) return 'letter';
  return null;
}

const APPROX = String.raw`(?:c\.?|ca\.?|circa|~|about|abt\.?|around)`;
const LEAD_YEAR = new RegExp(String.raw`^(${APPROX}\s*)?(\d{4})(s)?(?:[-._]\d{1,2}(?:[-._]\d{1,2})?)?(?=$|[\s\-–—_.,:)])`, 'i');
const TRAIL_YEAR = new RegExp(String.raw`[\s\-–—_,(]+(${APPROX}\s*)?(\d{4})(s)?\)?$`, 'i');
const CAMERA_NAME = /^(?:img|dsc|dscn|dscf|pxl|mvimg|photo|image|scan|scanned|scan_?\d*|p)[\s_-]*\d*(?:[\s_-]+\d+)*(?:\s*\(\d+\))?$/i;

/**
 * parseName("1948 - Wedding day.jpg") → { title: "Wedding day", year: 1948, approx: false }
 * parseName("c1948 Picnic.jpg")       → { title: "Picnic",      year: 1948, approx: true }
 * parseName("1940s farm_house.jpg")   → { title: "Farm house",  year: 1940, approx: true }
 * parseName("IMG_2231.JPG")           → { title: "",            year: null, approx: false }
 */
export function parseName(fileName) {
  let s = String(fileName || '').trim().replace(/\.[a-z0-9]{2,5}$/i, '');
  let year = null;
  let approx = false;

  const take = (m) => {
    const y = +m[2];
    if (!plausibleYear(y)) return false;
    year = y;
    approx = !!m[1] || !!m[3];
    return true;
  };

  const lead = LEAD_YEAR.exec(s);
  if (lead && take(lead)) {
    s = s.slice(lead[0].length);
  } else {
    const trail = TRAIL_YEAR.exec(s);
    if (trail && take(trail)) s = s.slice(0, trail.index);
  }

  // Separators left behind by the year ("1948 - ", "1948_").
  s = s.replace(/^[\s\-–—_.,:]+/, '').replace(/[\s\-–—_.,:(]+$/, '');
  if (!s || CAMERA_NAME.test(s)) return { title: '', year, approx };

  s = s.replace(/_+/g, ' ');
  if (!/\s/.test(s)) s = s.replace(/-+/g, ' ');       // wedding-day-at-church
  s = s.replace(/\s+[-–—]+\s+/g, ' – ');               // "Picnic - Lake Geneva"
  s = s.replace(/\s*\(\d+\)$/, '');                    // "Picnic (2)" duplicates
  return { title: tidyCase(tidySpace(s)), year, approx };
}

/**
 * parseDescription("June made her own dress.\nPlace: St. Mary's, Joliet #keepsake")
 *   → { caption: "June made her own dress.", place: "St. Mary's, Joliet", kind: "keepsake" }
 */
export function parseDescription(text) {
  let s = String(text || '').replace(/\r\n?/g, '\n');
  let kind = null;
  s = s.replace(/(^|\s)#(keepsake|letter|photo)\b/gi, (_, pre, tag) => {
    kind = tag.toLowerCase();
    return pre;
  });
  let place = '';
  s = s.replace(/^[ \t]*(?:place|where)\s*:\s*(.+)$/gim, (_, p) => {
    if (!place) place = p.trim().replace(/[.]$/, '');
    return '';
  });
  const caption = s.split('\n').map((l) => l.trim()).join('\n').replace(/\n{3,}/g, '\n\n').trim();
  return { caption: tidySpace(caption, true), place, kind };
}

function tidySpace(s, keepLines = false) {
  return keepLines
    ? String(s).replace(/[ \t]+/g, ' ').replace(/ *\n */g, '\n').trim()
    : String(s).replace(/\s+/g, ' ').trim();
}

/** Lightly tidy capitals: no shouting, first letter up, otherwise leave it. */
function tidyCase(s) {
  if (!s) return s;
  const letters = s.replace(/[^\p{L}]/gu, '');
  if (letters.length > 3 && letters === letters.toUpperCase()) s = s.toLowerCase();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Accepts a bare ID or any Drive folder link; returns the ID or ''. */
export function folderIdFrom(input) {
  const s = String(input || '').trim();
  if (!s) return '';
  const m = /\/folders\/([A-Za-z0-9_-]{10,})/.exec(s) || /[?&]id=([A-Za-z0-9_-]{10,})/.exec(s);
  if (m) return m[1];
  return /^[A-Za-z0-9_-]{10,}$/.test(s) ? s : '';
}
