import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { clearLocalSettings, loadSettings, normalizeFolderId, readLocalSettings, saveLocalSettings, settingsFromConfig, validateSettings, validateSettingsDocument } from '../../site/memories/js/settings.js';
import { CONFIG, DEFAULT_SETTINGS, SETTINGS_STATE } from '../../site/memories/js/config.js';

const fixture = () => ({
  title: 'Our album', honorees: [{ name: 'June', years: '1924 – 2011' }],
  dedication: 'For the family.', keeper: 'Lauren', helper: 'Kevin', people: ['June'],
  sample: true, source: 'manifest', drive: { apiKey: '', folderId: '' }, defaultSkin: 'heirloom',
});
const document = (revision = 'initial', settings = fixture()) => ({ version: 1, revision, settings });
const key = `AIza${'x'.repeat(35)}`;
const store = () => {
  const values = new Map();
  return { getItem: name => values.get(name) ?? null, setItem: (name, value) => values.set(name, value), removeItem: name => values.delete(name), values };
};

test('schema strips nonpublic settings and copies nested fields', () => {
  const input = fixture();
  input.access = { enabled: false, publicKey: 'untrusted' };
  input.publishing = { token: 'never-save-this' };
  input.honorees[0].privateKey = 'private';
  input.drive.secret = 'private';
  const clean = validateSettingsDocument({ ...document(), settings: input, token: 'private' });
  assert.deepEqual(clean, document());
  input.honorees[0].name = 'Changed';
  assert.equal(clean.settings.honorees[0].name, 'June');
  assert.deepEqual(settingsFromConfig({ ...fixture(), metadataUrl: 'evil', access: { enabled: false } }), fixture());
});

test('prototype-like fields cannot change configuration boundaries', () => {
  const input = JSON.parse(JSON.stringify(fixture()));
  Object.defineProperty(input, '__proto__', { value: { source: 'drive' }, enumerable: true });
  input.constructor = { prototype: { polluted: true } };
  assert.deepEqual(validateSettings(input), fixture());
  assert.equal({}.polluted, undefined);
});

test('names and text normalize safely; blank dedication and years are supported', () => {
  const input = fixture();
  input.title = ' Album ';
  input.honorees[0].years = '';
  input.dedication = '';
  input.people = [' Jose\u0301 ', 'JOSÉ', 'Walter'];
  const clean = validateSettings(input);
  assert.equal(clean.title, 'Album');
  assert.equal(clean.honorees[0].years, '');
  assert.equal(clean.dedication, '');
  assert.deepEqual(clean.people, ['José', 'Walter']);
});

test('Drive links normalize and reject deceptive or unsupported hosts', () => {
  const id = '1234567890_abc-XYZ';
  assert.equal(normalizeFolderId(id), id);
  assert.equal(normalizeFolderId(`https://drive.google.com/drive/u/0/folders/${id}?usp=sharing`), id);
  assert.equal(normalizeFolderId(`https://drive.google.com/open?id=${id}`), id);
  for (const value of ['abc', `http://drive.google.com/drive/folders/${id}`, `https://drive.google.com.evil.test/drive/folders/${id}`, `https://user@drive.google.com/drive/folders/${id}`, `https://example.test/${id}`, '<script>']) {
    assert.throws(() => normalizeFolderId(value));
  }
  assert.equal(normalizeFolderId(''), '');
});

test('Drive mode requires a browser key and real-photo state', () => {
  const input = fixture();
  input.source = 'drive'; input.sample = false;
  assert.throws(() => validateSettings(input), /both/);
  input.drive = { apiKey: key, folderId: '1234567890_abc' };
  assert.deepEqual(validateSettings(input).drive, input.drive);
  for (const secret of ['github_pat_not_public', 'sk-ant-not-public', 'private-admin-key']) {
    assert.throws(() => validateSettings({ ...input, drive: { ...input.drive, apiKey: secret } }), /Google Drive connection key/);
  }
  assert.throws(() => validateSettings({ ...input, sample: true }), /Choose sample photos/);
  assert.throws(() => validateSettings({ ...fixture(), sample: false }), /Choose sample photos/);
});

test('invalid settings documents fail without interpolating supplied values', () => {
  for (const value of [null, [], {}, { ...document(), version: 2 }, { ...document(), revision: '' }, { ...document(), revision: '\nsecret\nline' }, { ...document(), settings: [] }]) {
    assert.throws(() => validateSettingsDocument(value));
  }
  for (const patch of [{title:''}, {title:'x'.repeat(121)}, {title:'secret\u0000value'}, {honorees:[]}, {honorees:Array(9).fill({name:'A',years:''})}, {honorees:[{name:23,years:''}]}, {people:['']}, {people:Array(301).fill('A')}, {defaultSkin:'untrusted'}, {source:'remote'}, {keeper:null}, {drive:null}]) {
    assert.throws(() => validateSettings({ ...fixture(), ...patch }));
  }
});

test('published settings reach a fresh runtime and cache only sanitized public data', async () => {
  const storage = store();
  const saved = document('updated', { ...fixture(), title: 'Saved by Lauren' });
  saved.token = 'never-store'; saved.settings.access = { publicKey: 'never-store' };
  const calls = [];
  const loaded = await loadSettings(fixture(), { url: 'https://album.test/settings.json', storage, fetchImpl: async (url, options) => {
    calls.push({ url, cache: options.cache });
    return { ok: true, json: async () => saved };
  } });
  assert.equal(loaded.source, 'published');
  assert.equal(loaded.document.settings.title, 'Saved by Lauren');
  assert.equal(calls[0].cache, 'no-cache');
  assert.equal([...storage.values.values()][0].includes('never-store'), false);
  const otherDevice = await loadSettings(fixture(), { storage: store(), fetchImpl: async () => ({ ok: true, json: async () => saved }) });
  assert.equal(otherDevice.document.revision, 'updated');
});

test('network failures use only a validated cache for the same settings URL', async () => {
  const storage = store();
  const url = 'https://album.test/settings.json';
  storage.setItem(`memories.settings.v1:${url}`, JSON.stringify(document('cached', { ...fixture(), title: 'Saved title' })));
  const offline = async () => { throw new Error('Offline'); };
  const cached = await loadSettings(fixture(), { url, storage, fetchImpl: offline });
  assert.equal(cached.source, 'cached'); assert.equal(cached.document.settings.title, 'Saved title');
  const differentAlbum = await loadSettings(fixture(), { url: `${url}?different`, storage, fetchImpl: offline });
  assert.equal(differentAlbum.source, 'defaults');
  storage.setItem(`memories.settings.v1:${url}`, '{"version":2}');
  assert.equal((await loadSettings(fixture(), { url, storage, fetchImpl: offline })).source, 'defaults');
  const recovered = await loadSettings(fixture(), { url, storage, fetchImpl: async () => ({ok:true,json:async()=>document('recovered')}) });
  assert.equal(recovered.source, 'published'); assert.equal(recovered.document.revision, 'recovered');
});

test('bad HTTP/JSON, blocked storage, and hanging requests recover without hanging boot', async () => {
  const blocked = {getItem(){throw Error('blocked');},setItem(){throw Error('blocked');}};
  for (const fetchImpl of [async()=>({ok:false}), async()=>({ok:true,json:async()=>{throw Error('bad JSON');}}), async()=>({ok:true,json:async()=>({version:9})})]) {
    assert.equal((await loadSettings(fixture(), { storage:blocked, fetchImpl })).source,'defaults');
  }
  const valid = await loadSettings(fixture(), {storage:blocked,fetchImpl:async()=>({ok:true,json:async()=>document()})});
  assert.equal(valid.source,'published');
  let aborted = false;
  const pending = await loadSettings(fixture(), {storage:null,timeoutMs:10,fetchImpl:async(_,options)=>{
    options.signal.addEventListener('abort',()=>{aborted=true;});
    return new Promise(()=>{});
  }});
  assert.equal(pending.source,'defaults'); assert.equal(aborted,true);
});

test('published settings remain valid independently of bootstrap defaults and invite settings', async () => {
  const seed = JSON.parse(await readFile(new URL('../../site/memories/data/settings.json',import.meta.url),'utf8'));
  // Admin saves intentionally diverge from recovery defaults. Validate the
  // document, not equality to the initial family values. Never print key values.
  assert.equal(validateSettingsDocument(seed).version,1);
  assert.equal(JSON.stringify(settingsFromConfig(CONFIG))===JSON.stringify(DEFAULT_SETTINGS),true);
  assert.equal(SETTINGS_STATE.source,'defaults','Node import makes no network request');
  assert.equal(CONFIG.access.enabled,true);
  assert.equal(typeof CONFIG.access.publicKey,'string');
  assert.equal(Object.hasOwn(seed.settings,'access'),false);
});


test('device settings save and reload separately from the shared defaults cache', async () => {
  const storage = store();
  const url = 'https://album.test/memories/data/settings.json';
  const cacheKey = `memories.settings.v1:${url}`;
  const original = JSON.stringify(document('shared', fixture()));
  storage.setItem(cacheKey, original);
  const changed = { ...fixture(), title: 'On this device', access: { enabled: false }, publishingToken: 'never-store' };
  const saved = saveLocalSettings(changed, { storage, url });
  assert.match(saved.revision, /^local-/);
  assert.equal(saved.settings.title, 'On this device');
  assert.equal(storage.getItem(cacheKey), original, 'saving locally never overwrites shared cache');
  assert.equal(storage.getItem(`memories.settings.local.v1:${url}`).includes('never-store'), false);
  assert.equal(Object.hasOwn(saved.settings, 'access'), false);
  const loaded = await loadSettings(fixture(), { storage, url, fetchImpl: () => { throw Error('Local override should not fetch'); } });
  assert.equal(loaded.source, 'local');
  assert.equal(loaded.localStatus, 'saved');
  assert.equal(loaded.document.settings.title, 'On this device');
  assert.deepEqual(readLocalSettings({ storage, url }).document, saved);
});

test('new shared settings cannot replace a valid device choice; another browser uses shared settings', async () => {
  const storage = store();
  const saved = saveLocalSettings({ ...fixture(), keeper: 'Device keeper' }, {storage});
  const shared = document('new-shared', { ...fixture(), keeper: 'Shared keeper' });
  let fetches = 0;
  const fetchImpl = async () => { fetches++; return {ok:true,json:async()=>shared}; };
  const local = await loadSettings(fixture(), {storage,fetchImpl});
  assert.equal(local.document.revision,saved.revision);
  assert.equal(local.document.settings.keeper,'Device keeper');
  assert.equal(fetches,0);
  const fresh = await loadSettings(fixture(), {storage:store(),fetchImpl});
  assert.equal(fresh.source,'published');
  assert.equal(fresh.document.settings.keeper,'Shared keeper');
  assert.equal(fetches,1);
});

test('device keys are isolated by album URL and never inferred from a shared cache', async () => {
  const storage = store();
  const first='https://album.test/a/settings.json', second='https://album.test/b/settings.json';
  saveLocalSettings({ ...fixture(), title:'First album only' }, {storage,url:first});
  assert.equal(readLocalSettings({storage,url:second}).status,'none');
  const shared=document('shared',{...fixture(),title:'Second album'});
  storage.setItem(`memories.settings.v1:${second}`,JSON.stringify(shared));
  const other=await loadSettings(fixture(),{storage,url:second,fetchImpl:async()=>{throw Error('Offline');}});
  assert.equal(other.source,'cached');
  assert.equal(other.document.settings.title,'Second album');
});

test('malformed saved choices fall back without blocking boot and stay available for explicit reset', async () => {
  const storage=store();
  const url='https://album.test/settings.json';
  const key=`memories.settings.local.v1:${url}`;
  for (const malformed of ['', '{invalid', JSON.stringify({version:99}), JSON.stringify(document('bad',{...fixture(),title:''}))]) {
    storage.setItem(key,malformed);
    assert.equal(readLocalSettings({storage,url}).status,'invalid');
    const loaded=await loadSettings(fixture(),{storage,url,fetchImpl:async()=>({ok:true,json:async()=>document('shared')})});
    assert.equal(loaded.source,'published');
    assert.equal(loaded.localStatus,'invalid');
    assert.equal(storage.getItem(key),malformed,'reading never silently deletes saved data');
  }
  clearLocalSettings({storage,url});
  assert.equal(readLocalSettings({storage,url}).status,'none');
});

test('reset removes only the explicit device override and reveals shared defaults again', async () => {
  const storage=store();
  const url='https://album.test/settings.json';
  const shared=document('shared',{...fixture(),title:'Shared album'});
  storage.setItem(`memories.settings.v1:${url}`,JSON.stringify(shared));
  saveLocalSettings({...fixture(),title:'Local album'},{storage,url});
  clearLocalSettings({storage,url});
  assert.equal(readLocalSettings({storage,url}).status,'none');
  const after=await loadSettings(fixture(),{storage,url,fetchImpl:async()=>{throw Error('Offline');}});
  assert.equal(after.source,'cached');
  assert.equal(after.document.settings.title,'Shared album');
});

test('storage failures never report a successful save or reset', () => {
  const blocked={getItem(){throw Error('blocked');},setItem(){throw Error('blocked');},removeItem(){throw Error('blocked');}};
  assert.equal(readLocalSettings({storage:blocked}).status,'unavailable');
  assert.equal(readLocalSettings({storage:null}).status,'unavailable');
  for(const storage of [null,blocked,{getItem:()=>null,setItem:()=>{},removeItem:()=>{}}]) {
    assert.throws(()=>saveLocalSettings(fixture(),{storage}),/could not save/);
  }
  const retained={getItem:()=>JSON.stringify(document()),setItem:()=>{},removeItem:()=>{}};
  for(const storage of [null,blocked,retained]) {
    assert.throws(()=>clearLocalSettings({storage}),/could not reset/);
  }
  const storage=store();
  const prior=saveLocalSettings(fixture(),{storage});
  storage.setItem=()=>{throw Error('quota');};
  assert.throws(()=>saveLocalSettings({...fixture(),title:'Unsaved'},{storage}),/could not save/);
  assert.equal(readLocalSettings({storage}).document.revision,prior.revision);
});

test('invalid edits do not replace previously saved device settings', () => {
  const storage=store();
  const saved=saveLocalSettings(fixture(),{storage});
  assert.throws(()=>saveLocalSettings({...fixture(),title:''},{storage}),/required/);
  assert.equal(readLocalSettings({storage}).document.revision,saved.revision);
  const next=saveLocalSettings({...fixture(),title:'Updated locally'},{storage});
  assert.notEqual(next.revision,saved.revision);
  assert.equal(readLocalSettings({storage}).document.settings.title,'Updated locally');
});
