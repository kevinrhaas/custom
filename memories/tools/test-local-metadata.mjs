import test from 'node:test';
import assert from 'node:assert/strict';
import { localMetadataKey, readLocalMetadata, saveLocalMetadata, clearLocalMetadata } from '../../site/memories/js/local-metadata.js';
import { loadLibrary } from '../../site/memories/js/library.js';

const config = { source: 'manifest', people: [], access: { prefix: 'memories' } };
const file = (photos = {}) => ({ version: 1, photos });
const store = () => {
  const values = new Map();
  return { values, getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value), removeItem: key => values.delete(key) };
};

test('saved approved additions are validated separately from drafts and private face data', () => {
  const storage = store();
  storage.setItem('memories.tagging.v1.manifest', JSON.stringify({ drafts: file({ p1: { tags: ['unreviewed'] } }) }));
  assert.deepEqual(readLocalMetadata(config, { storage }), { document: null, status: 'none' });
  const saved = saveLocalMetadata(config, { ...file({ p1: { tags: ['horse', 'HORSE'], people: ['Lee'], descriptor: [0.3], image: 'private' } }), drafts: { secret: 'unreviewed' } }, { storage });
  assert.deepEqual(saved, file({ p1: { tags: ['horse'], people: ['Lee'] } }));
  assert.deepEqual(readLocalMetadata(config, { storage }), { document: saved, status: 'saved' });
  assert.equal(storage.getItem(localMetadataKey(config)).includes('unreviewed'), false);
  assert.equal(storage.getItem(localMetadataKey(config)).includes('descriptor'), false);
  assert.equal(storage.getItem(localMetadataKey(config)).includes('private'), false);
});

test('saved additions stay within their browser, album prefix and photo source', () => {
  const storage = store();
  const folderA = { ...config, source: 'drive', drive: { folderId: 'folder-AAAAA' } };
  const folderB = { ...folderA, drive: { folderId: 'folder-BBBBB' } };
  saveLocalMetadata(folderA, file({ p1: { tags: ['horse'] } }), { storage });
  for (const isolated of [config, folderB, { ...folderA, access: { prefix: 'other-album' } }]) {
    assert.equal(readLocalMetadata(isolated, { storage }).status, 'none');
  }
  assert.equal(readLocalMetadata(folderA, { storage: store() }).status, 'none');
  saveLocalMetadata(config, file({ p2: { people: ['Kevin'] } }), { storage });
  assert.equal(readLocalMetadata({ ...config, manifestUrl: 'data/another-library.json' }, { storage }).status, 'none');
});

test('unavailable, malformed and silently discarded storage cannot report a successful save', () => {
  const storage = store();
  storage.setItem(localMetadataKey(config), '{broken');
  assert.equal(readLocalMetadata(config, { storage }).status, 'invalid');
  storage.setItem(localMetadataKey(config), JSON.stringify({ version: 2, photos: {} }));
  assert.equal(readLocalMetadata(config, { storage }).status, 'invalid');
  const blocked = { getItem() { throw Error('blocked'); }, setItem() { throw Error('quota'); }, removeItem() { throw Error('blocked'); } };
  const silent = { getItem() { return null; }, setItem() {} };
  for (const unavailable of [null, blocked, silent]) {
    assert.throws(() => saveLocalMetadata(config, file(), { storage: unavailable }), /could not save/);
  }
  assert.equal(readLocalMetadata(config, { storage: blocked }).status, 'unavailable');
  assert.throws(() => saveLocalMetadata(config, { version: 2 }, { storage }));
  assert.throws(() => clearLocalMetadata(config, { storage: blocked }), /could not clear/);
  clearLocalMetadata(config, { storage });
  assert.equal(readLocalMetadata(config, { storage }).status, 'none');
});

async function withBrowser(storage, fetchImpl, run) {
  const before = { storage: globalThis.localStorage, fetch: globalThis.fetch, location: globalThis.location };
  globalThis.localStorage = storage;
  globalThis.fetch = fetchImpl;
  globalThis.location = { href: 'https://album.test/memories/' };
  try { await run(); }
  finally {
    globalThis.fetch = before.fetch;
    for (const [key, value] of [['localStorage', before.storage], ['location', before.location]]) {
      if (value === undefined) delete globalThis[key]; else globalThis[key] = value;
    }
  }
}

const source = () => ({ chapters: [{ id: 'chapter', title: 'The album' }], photos: [{ id: 'p1', chapter: 'chapter', title: 'A photo', caption: 'Original caption', tags: ['source-label'], src: 'photo.jpg' }] });

test('album search reads explicit saved approvals, while staged drafts stay invisible', async () => {
  const storage = store();
  const shared = file({ p1: { tags: ['shared-label'] } });
  const requested = [];
  await withBrowser(storage, async url => {
    requested.push(String(url));
    return { ok: true, json: async () => String(url).endsWith('tags.json') ? shared : source() };
  }, async () => {
    storage.setItem('memories.tagging.v1.manifest', JSON.stringify({ approved: file({ p1: { tags: ['not-saved'] } }), drafts: file({ p1: { tags: ['unreviewed'] } }) }));
    let loaded = await loadLibrary(config);
    assert.match(loaded.photos[0].search, /shared-label/);
    assert.doesNotMatch(loaded.photos[0].search, /not-saved|unreviewed/);
    saveLocalMetadata(config, file({ p1: { tags: ['local-label'], people: ['Lee'], caption: 'Approved caption' } }));
    requested.length = 0;
    loaded = await loadLibrary(config);
    assert.match(loaded.photos[0].search, /local-label/);
    assert.match(loaded.photos[0].search, /lee/);
    assert.match(loaded.photos[0].search, /source-label/);
    assert.equal(loaded.photos[0].caption, 'Approved caption');
    assert.doesNotMatch(loaded.photos[0].search, /shared-label|not-saved|unreviewed/);
    assert.equal(requested.some(url => url.endsWith('tags.json')), false, 'local snapshot can load without sidecar request');
    const original = await loadLibrary({ ...config, metadataUrl: false, localMetadata: false });
    assert.deepEqual(original.photos[0].tags, ['source-label']);
    assert.equal(original.photos[0].caption, 'Original caption');
  });
});

test('saving an empty snapshot removes additions; malformed storage falls back to shared defaults', async () => {
  const storage = store();
  await withBrowser(storage, async url => ({ ok: true, json: async () => String(url).endsWith('tags.json') ? file({ p1: { tags: ['shared-label'] } }) : source() }), async () => {
    saveLocalMetadata(config, file());
    assert.deepEqual((await loadLibrary(config)).photos[0].tags, ['source-label']);
    storage.setItem(localMetadataKey(config), 'invalid');
    assert.deepEqual((await loadLibrary(config)).photos[0].tags, ['source-label', 'shared-label']);
    clearLocalMetadata(config);
    assert.deepEqual((await loadLibrary(config)).photos[0].tags, ['source-label', 'shared-label']);
  });
});

test('Drive offline cache never crosses folders or trusts the old unscoped cache', async () => {
  const storage = store();
  const folderA = { ...config, source: 'drive', metadataUrl: false, localMetadata: false, drive: { folderId: 'folder-AAAAA', apiKey: 'test-key' } };
  const folderB = { ...folderA, drive: { ...folderA.drive, folderId: 'folder-BBBBB' } };
  let offline = false;
  await withBrowser(storage, async url => {
    if (offline) throw new TypeError('offline');
    const parsed = new URL(url);
    if (parsed.pathname.endsWith('/folder-AAAAA')) return { ok: true, json: async () => ({ id: 'folder-AAAAA', mimeType: 'application/vnd.google-apps.folder' }) };
    return { ok: true, json: async () => ({ files: [{ id: 'photo-A', name: '1948 - Folder A photo.jpg', mimeType: 'image/jpeg' }] }) };
  }, async () => {
    assert.equal((await loadLibrary(folderA)).photos[0].id, 'photo-A');
    assert.ok(storage.getItem('memories.library.v2.drive.folder-AAAAA'));
    offline = true;
    const cached = await loadLibrary(folderA);
    assert.equal(cached.photos[0].id, 'photo-A');
    assert.equal(cached.stale, true);
    storage.setItem('memories.library.v1', JSON.stringify({ raw: source() }));
    await assert.rejects(loadLibrary(folderB), /couldn't reach Google Drive/);
    assert.equal(storage.getItem('memories.library.v2.drive.folder-BBBBB'), null);
  });
});
