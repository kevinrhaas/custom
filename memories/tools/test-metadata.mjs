// Regression checks for manual labels, approved metadata and searchable names.
// Run: node memories/tools/test-metadata.mjs
import assert from 'node:assert/strict';
import { uniqueLabels, validateMetadata, applyMetadata, loadMetadata } from '../../site/memories/js/metadata.js';
import { normalize, loadLibrary } from '../../site/memories/js/library.js';
import { parseDescription } from '../../site/memories/js/sources/drive.js';

let checks = 0;
const eq = (actual, expected, label) => { assert.deepEqual(actual, expected, label); checks++; };
const ok = (actual, label) => { assert.ok(actual, label); checks++; };

eq(uniqueLabels('horse, HORSE; county fair ;; June Hale'), ['horse', 'county fair', 'June Hale'], 'labels split, trim and deduplicate');
eq(uniqueLabels([' Jose\u0301  Hale ', 'José Hale', null, 42, '']), ['José Hale'], 'Unicode and invalid labels');
eq(parseDescription('June and Walter on the farm.\r\nTags: horse, carriage\r\nPeople: June Hale; Walter Hale\r\ntags: HORSE; county fair\r\nPlace: Joliet'), {
  caption: 'June and Walter on the farm.', place: 'Joliet', kind: null,
  tags: ['horse', 'carriage', 'county fair'], people: ['June Hale', 'Walter Hale'],
}, 'manual lines are metadata, not caption');
eq(parseDescription('The sign said Tags: nothing here.\nTags: \nPeople:\nA second sentence.'), {
  caption: 'The sign said Tags: nothing here.\n\nA second sentence.', place: '', kind: null, tags: [], people: [],
}, 'only whole lines are removed, including empty lines');

const source = {
  chapters: [{ id: 'farm', title: 'County fair', blurb: 'Growing up' }],
  photos: [{ id: 'p1', chapter: 'farm', title: 'June driving', caption: 'Walter was there.', tags: ['family'], people: ['June Hale'], year: 1948 }],
};
const sidecar = { version: 1, photos: { p1: { tags: ['horse', 'FAMILY'], people: ['Walter Hale'] }, missing: { tags: ['ignore'] } } };
const merged = applyMetadata(source, sidecar);
eq(merged.photos[0].tags, ['family', 'horse'], 'sidecar adds tags');
eq(merged.photos[0].people, ['June Hale', 'Walter Hale'], 'sidecar adds people');
eq(merged.photos[0].caption, 'Walter was there.', 'omitted caption preserves original');
eq(source.photos[0].tags, ['family'], 'source is not mutated');
eq(merged.photos.length, 1, 'unknown IDs cannot add photos');
eq(applyMetadata(source, { version: 1, photos: { p1: { caption: 'Approved caption.' } } }).photos[0].caption, 'Approved caption.', 'explicit approved caption replaces source');
eq(applyMetadata(source, { version: 1, photos: { p1: { caption: '' } } }).photos[0].caption, '', 'explicit blank caption clears source');
eq(validateMetadata({ version: 1, photos: { p1: { tags: ['horse'], descriptor: [0.1], box: {}, secret: 'ignored' } } }), { version: 1, photos: { p1: { tags: ['horse'] } } }, 'public schema excludes face descriptors and unknown fields');
for (const bad of [null, [], { version: 2, photos: {} }, { version: 1, photos: [] }, { version: 1, photos: { p1: { tags: 'horse' } } }, { version: 1, photos: { p1: { people: [42] } } }, { version: 1, photos: { p1: { caption: null } } }]) {
  assert.throws(() => validateMetadata(bad)); checks++;
}
const unusualId = JSON.parse('{"version":1,"photos":{"__proto__":{"tags":["safe"]}}}');
eq(applyMetadata({ photos: [{ id: '__proto__' }, { id: 'toString' }] }, unusualId).photos, [{ id: '__proto__', tags: ['safe'], people: [] }, { id: 'toString' }], 'IDs are own keys, never prototype properties');

const library = normalize(merged, { people: ['June', 'Walter'] });
eq(library.photos[0].people, ['June Hale', 'Walter Hale', 'Walter', 'June'], 'manual and automatically found names coexist');
for (const term of ['horse', 'county fair', 'june hale', 'walter hale', '1948', '1940s']) ok(library.photos[0].search.includes(term), `search includes ${term}`);
const catchall = normalize({ photos: [{ id: 'orphan', title: 'Lost photo', chapter: 'missing' }] }, {});
ok(catchall.photos[0].search.includes('more treasures'), 'catch-all chapter is searchable');

const savedFetch = globalThis.fetch;
const savedLocation = globalThis.location;
try {
  globalThis.fetch = async () => ({ ok: true, json: async () => sidecar });
  eq(await loadMetadata('/tags.json'), sidecar, 'load approved sidecar');
  globalThis.fetch = async () => ({ ok: false, status: 404 });
  eq(await loadMetadata('/missing.json'), null, 'missing sidecar is optional');
  globalThis.fetch = async () => { throw new TypeError('Offline'); };
  eq(await loadMetadata('/tags.json'), null, 'network failure is optional');
  globalThis.fetch = async () => ({ ok: true, json: async () => ({ version: 9 }) });
  eq(await loadMetadata('/tags.json'), null, 'invalid sidecar is optional');
  eq(await loadMetadata(null), null, 'disabled sidecar skips fetch');

  globalThis.location = { href: 'https://example.test/memories/admin/' };
  const requested = [];
  globalThis.fetch = async (url) => {
    requested.push(String(url));
    return { ok: true, json: async () => String(url).endsWith('/data/tags.json') ? structuredClone(sidecar) : structuredClone(source) };
  };
  const loaded = await loadLibrary({ people: [], source: 'manifest' });
  ok(requested.some((url) => url.endsWith('/site/memories/data/library.json')), 'manifest resolves from album root even on admin page');
  ok(requested.some((url) => url.endsWith('/site/memories/data/tags.json')), 'sidecar resolves from album root');
  ok(loaded.photos[0].search.includes('horse'), 'loadLibrary overlays approved metadata before indexing');
  for (const disabled of [null, false]) {
    requested.length = 0;
    const plain = await loadLibrary({ source: 'manifest', metadataUrl: disabled });
    eq(requested.length, 1, 'explicit opt-out makes only source request');
    ok(!plain.photos[0].search.includes('horse'), 'explicit opt-out returns source metadata only');
  }
} finally {
  globalThis.fetch = savedFetch;
  if (savedLocation === undefined) delete globalThis.location;
  else globalThis.location = savedLocation;
}
console.log(`ok — ${checks} metadata checks passed`);
