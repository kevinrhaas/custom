// Tests for the Drive source's file-name and description parsing.
// Run from anywhere:  node memories/tools/test-drive-parse.mjs
import assert from 'node:assert/strict';
import { loadDrive, parseName, parseDescription, chapterTitle, folderIdFrom } from '../../site/memories/js/sources/drive.js';

let n = 0;
const eq = (actual, expected, label) => { assert.deepEqual(actual, expected, label); n++; };
const name = (file, title, year = null, approx = false) => eq(parseName(file), { title, year, approx }, file);

// Leading years
name('1948 - Wedding day.jpg', 'Wedding day', 1948);
name('1948 Wedding day.jpg', 'Wedding day', 1948);
name('1948-Wedding day.JPG', 'Wedding day', 1948);
name('1948_wedding_day.jpg', 'Wedding day', 1948);
name('1948-06-12 Wedding day.jpg', 'Wedding day', 1948);
name('c1948 Picnic at the lake.jpg', 'Picnic at the lake', 1948, true);
name('c. 1948 Picnic.jpg', 'Picnic', 1948, true);
name('~1948 Picnic.png', 'Picnic', 1948, true);
name('about 1948 - Picnic.jpg', 'Picnic', 1948, true);
name('Circa 1952 Grandma Rose.jpeg', 'Grandma Rose', 1952, true);
name('1940s farm_house.jpg', 'Farm house', 1940, true);
name('1940s - The farm.tif', 'The farm', 1940, true);
// Trailing years
name('Wedding day 1948.jpg', 'Wedding day', 1948);
name('Wedding day (about 1948).jpg', 'Wedding day', 1948, true);
name('Wedding day - 1950s.jpg', 'Wedding day', 1950, true);
// No year
name("Uncle Frank's Buick.jpg", "Uncle Frank's Buick");
name('wedding-day-at-church.jpg', 'Wedding day at church');
name('Picnic - Lake Geneva.jpg', 'Picnic – Lake Geneva');
name('Mother-in-law visits.jpg', 'Mother-in-law visits');
name('THE OLD HOUSE ON ELM.JPG', 'The old house on elm');
name('June and Walter.HEIC', 'June and Walter');
name('Picnic (2).jpg', 'Picnic');
// Not years
name('1600 Main Street.jpg', '1600 Main Street');
// Camera / scanner names → no title (the loader falls back to the caption)
name('IMG_2231.JPG', '');
name('DSC01234.jpg', '');
name('Scan 12.png', '');
name('1948 IMG_0012.jpg', '', 1948);
// Year only
name('1965.jpg', '', 1965);

// Descriptions
eq(parseDescription("June made her own dress.\nPlace: St. Mary's, Joliet"),
  { caption: 'June made her own dress.', place: "St. Mary's, Joliet", kind: null }, 'place line');
eq(parseDescription('Dad\'s letter from the Navy #letter'),
  { caption: "Dad's letter from the Navy", place: '', kind: 'letter' }, 'letter tag');
eq(parseDescription('#Keepsake Mom\'s recipe box.\nwhere: the kitchen on Elm.'),
  { caption: "Mom's recipe box.", place: 'the kitchen on Elm', kind: 'keepsake' }, 'keepsake tag + where');
eq(parseDescription(''), { caption: '', place: '', kind: null }, 'empty');
eq(parseDescription('Line one.\n\n\n\nLine two.'), { caption: 'Line one.\n\nLine two.', place: '', kind: null }, 'blank lines');

// Chapters
eq(chapterTitle('01 Early years'), 'Early years', 'chapter number');
eq(chapterTitle('2 - The farm'), 'The farm', 'chapter dash');
eq(chapterTitle('03. Keepsakes'), 'Keepsakes', 'chapter dot');
eq(chapterTitle('1950s'), '1950s', 'decade folder kept');
eq(chapterTitle('1950s on Elm Street'), '1950s on Elm Street', 'decade folder kept 2');
eq(chapterTitle('school_days'), 'School days', 'underscores');

// Folder IDs
const ID = '1AbCdEfGhIjKlMnOpQrStUvWxYz012345';
eq(folderIdFrom(ID), ID, 'bare id');
eq(folderIdFrom(`https://drive.google.com/drive/folders/${ID}?usp=sharing`), ID, 'share url');
eq(folderIdFrom(`https://drive.google.com/drive/u/0/folders/${ID}`), ID, 'u/0 url');
eq(folderIdFrom(`https://drive.google.com/open?id=${ID}`), ID, 'open?id');
eq(folderIdFrom('not a link'), '', 'junk');

// ---- loadDrive against a fake Drive API ----------------------------------
const F = 'application/vnd.google-apps.folder';
const tree = {
  ROOTFOLDER0001: { name: 'Album', mimeType: F, kids: [
    { id: 'CH2', name: '02 Keepsakes', mimeType: F, description: 'Things June kept.' },
    { id: 'CH1', name: '01 Early years', mimeType: F },
    { id: 'EMPTY', name: '03 Nothing yet', mimeType: F },
    { id: 'L1', name: 'IMG_0001.jpg', mimeType: 'image/jpeg', description: 'Walter at the lake.\nPlace: Lake Geneva' },
    { id: 'DOC', name: 'notes.pdf', mimeType: 'application/pdf' },
  ] },
  CH1: { kids: [
    { id: 'P1', name: '1948 - Wedding day.jpg', mimeType: 'image/jpeg', imageMediaMetadata: { width: 3000, height: 2000, rotation: 1 } },
    { id: 'P2', name: 'Picnic.jpg', mimeType: 'image/jpeg', createdTime: '2026-11-01T00:00:00Z', imageMediaMetadata: { time: '2026:10:30 10:00:00' } },
    { id: 'P3', name: 'Beach.jpg', mimeType: 'image/jpeg', createdTime: '2026-11-01T00:00:00Z', imageMediaMetadata: { time: '2004:07:04 10:00:00' } },
    { id: 'SUB', name: 'More from the farm', mimeType: F },
  ] },
  SUB: { kids: [{ id: 'P4', name: '1950s Tractor.jpg', mimeType: 'image/png', description: 'Dad\'s letter #letter' }] },
  L1FILE000000: { name: 'x.jpg', mimeType: 'image/jpeg' },
  CH2: { kids: [{ id: 'K1', name: 'Recipe box.jpg', mimeType: 'image/jpeg' }] },
  EMPTY: { kids: [] },
};
const pages = [];
globalThis.fetch = async (url) => {
  const u = new URL(url);
  const json = (status, body) => ({ ok: status === 200, status, json: async () => body });
  if (u.searchParams.get('key') === 'BAD') return json(400, { error: { code: 400, message: 'API key not valid. Please pass a valid API key.', status: 'INVALID_ARGUMENT', details: [{ reason: 'API_KEY_INVALID' }] } });
  if (u.searchParams.get('key') === 'REF') return json(403, { error: { code: 403, message: 'Requests from referer http://x/ are blocked.', status: 'PERMISSION_DENIED', details: [{ reason: 'API_KEY_HTTP_REFERRER_BLOCKED' }] } });
  const m = /\/files\/([^/?]+)$/.exec(u.pathname);
  if (m) { const f = tree[m[1]]; return f ? json(200, { id: m[1], name: f.name, mimeType: f.mimeType }) : json(404, { error: { code: 404, message: 'File not found' } }); }
  const parent = /'([^']+)' in parents/.exec(u.searchParams.get('q'))[1];
  const kids = tree[parent].kids.slice().sort((a, b) => a.name.localeCompare(b.name));
  // Page the root listing in twos to exercise nextPageToken.
  if (parent === 'ROOTFOLDER0001') {
    const start = +(u.searchParams.get('pageToken') || 0);
    pages.push(start);
    return json(200, { files: kids.slice(start, start + 2), nextPageToken: start + 2 < kids.length ? String(start + 2) : undefined });
  }
  return json(200, { files: kids });
};
const lib = await loadDrive({ apiKey: 'GOOD', folderId: 'https://drive.google.com/drive/folders/ROOTFOLDER0001?usp=sharing' });
eq(pages, [0, 2, 4], 'pagination');
eq(lib.chapters.map((c) => c.title), ['Early years', 'Keepsakes', 'The album'], 'chapter order, empty skipped');
eq(lib.chapters[1].blurb, 'Things June kept.', 'blurb');
const byId = Object.fromEntries(lib.photos.map((p) => [p.id, p]));
eq([byId.P1.w, byId.P1.h, byId.P1.year], [1600, 2400, 1948], 'rotation swap + scale to w1600');
eq(byId.P2.year, null, 'scan-date camera year ignored');
eq(byId.P3.year, 2004, 'camera year used');
eq([byId.P4.chapter, byId.P4.kind, byId.P4.year, byId.P4.approx], ['CH1', 'letter', 1950, true], 'nested flattened');
eq(byId.K1.kind, 'keepsake', 'keepsake folder');
eq([byId.L1.chapter, byId.L1.title, byId.L1.place], ['_album', 'Walter at the lake', 'Lake Geneva'], 'root photo');
eq(byId.P1.src, 'https://lh3.googleusercontent.com/d/P1=w1600', 'src');
eq(byId.P1.thumbFallback, 'https://drive.google.com/thumbnail?id=P1&sz=w480', 'thumb fallback');
eq([byId.P1.download, byId.P1.downloadName], ['https://drive.google.com/uc?export=download&id=P1', '1948 - Wedding day.jpg'], 'download');
eq(byId.DOC, undefined, 'non-images skipped');
const code = async (opts) => { try { await loadDrive(opts); return 'no error'; } catch (e) { return e.code; } };
eq(await code({ apiKey: 'BAD', folderId: 'ROOTFOLDER0001' }), 'key', '400 bad key');
eq(await code({ apiKey: 'REF', folderId: 'ROOTFOLDER0001' }), 'referrer', '403 referrer');
eq(await code({ apiKey: 'GOOD', folderId: 'NOTSHARED000' }), 'not-shared', '404');
eq(await code({ apiKey: 'GOOD', folderId: 'L1FILE000000' }), 'not-folder', 'not a folder');
globalThis.fetch = async () => { throw new TypeError('Failed to fetch'); };
eq(await code({ apiKey: 'GOOD', folderId: 'ROOTFOLDER0001' }), 'network', 'network');

console.log(`ok — ${n} checks passed`);
