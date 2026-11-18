// Device settings override the published album defaults only in this browser.
// Invite verification and other bootstrap boundaries are never editable here.
import { SKINS } from './skins.js';

export const SETTINGS_URL = new URL('../data/settings.json', import.meta.url).href;
export const LOCAL_SETTINGS_KEY = `memories.settings.local.v1:${SETTINGS_URL}`;
export const EDITABLE_FIELDS = Object.freeze(['title', 'honorees', 'dedication', 'keeper', 'helper', 'people', 'sample', 'source', 'drive', 'defaultSkin']);
const skinIds = new Set(SKINS.map(skin => skin.id));
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);

function text(value, label, max, { optional = false, multiline = false } = {}) {
  if (typeof value !== 'string') throw new Error(`${label} must be text.`);
  const clean = value.normalize('NFC').replace(/\r\n?/g, '\n').trim();
  if ((!optional && !clean) || clean.length > max) throw new Error(`${label} ${optional ? 'must be' : 'is required and must be'} ${max} characters or fewer.`);
  const controls = multiline ? /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/ : /[\u0000-\u001f\u007f]/;
  if (controls.test(clean)) throw new Error(`Remove unusual characters from ${label.toLowerCase()}.`);
  return clean;
}

export function normalizeFolderId(value) {
  const input = text(value, 'Drive folder', 1000, { optional: true });
  if (!input) return '';
  let id = input;
  if (/^https?:\/\//i.test(input)) {
    let url;
    try { url = new URL(input); } catch { throw new Error('Paste the link to your Google Drive folder.'); }
    if (url.protocol !== 'https:' || url.hostname !== 'drive.google.com' || url.username || url.password) throw new Error('Paste the link to your Google Drive folder.');
    const match = url.pathname.match(/\/folders\/([A-Za-z0-9_-]+)\/?$/);
    id = match?.[1] || (url.pathname === '/open' ? url.searchParams.get('id') : '') || '';
  }
  if (!/^[A-Za-z0-9_-]{10,200}$/.test(id)) throw new Error('Check the link to your Google Drive folder.');
  return id;
}

/** Return only the public fields that the admin can edit. */
export function settingsFromConfig(config) {
  return validateSettings(Object.fromEntries(EDITABLE_FIELDS.map(field => [field, config[field]])));
}

/** Strictly validate known fields and discard every unknown field. */
export function validateSettings(value) {
  if (!record(value)) throw new Error("These album settings couldn’t be read. Please try again.");
  if (!Array.isArray(value.honorees) || value.honorees.length < 1 || value.honorees.length > 8) throw new Error('Add between one and eight names for the album.');
  const honorees = value.honorees.map(person => {
    if (!record(person)) throw new Error("Check each person's name and optional note.");
    return { name: text(person.name, 'Name', 120), years: text(person.years, 'Dates or note', 100, { optional: true }) };
  });
  if (!Array.isArray(value.people) || value.people.length > 300) throw new Error('Use up to 300 names to find in captions.');
  const seen = new Set();
  const people = value.people.map(name => text(name, 'Searchable name', 120)).filter(name => {
    const key = name.toLocaleLowerCase();
    if (seen.has(key)) return false;
    seen.add(key); return true;
  });
  if (!['manifest', 'drive'].includes(value.source)) throw new Error('Choose sample photos or the Google Drive folder.');
  if (typeof value.sample !== 'boolean' || value.sample !== (value.source === 'manifest')) throw new Error('Choose sample photos or Google Drive photos.');
  if (!record(value.drive)) throw new Error('Add your Google Drive folder and its connection key.');
  const apiKey = text(value.drive.apiKey, 'Google Drive connection key', 120, { optional: true });
  if (apiKey && !/^AIza[A-Za-z0-9_-]{35}$/.test(apiKey)) throw new Error('Check the Google Drive connection key and try again.');
  const folderId = normalizeFolderId(value.drive.folderId);
  if (value.source === 'drive' && (!apiKey || !folderId)) throw new Error('Add both your Google Drive folder and its connection key before choosing Drive photos.');
  if (!skinIds.has(value.defaultSkin)) throw new Error('Choose one of the available album looks.');
  return {
    title: text(value.title, 'Album title', 120),
    honorees,
    dedication: text(value.dedication, 'Welcome message', 4000, { optional: true, multiline: true }),
    keeper: text(value.keeper, 'Album keeper', 120),
    helper: text(value.helper, 'Site helper', 120),
    people,
    sample: value.sample,
    source: value.source,
    drive: { apiKey, folderId },
    defaultSkin: value.defaultSkin,
  };
}

export function validateSettingsDocument(value) {
  if (!record(value) || value.version !== 1) throw new Error("These saved settings couldn’t be read. Please try again.");
  const revision = text(value.revision, 'Saved settings', 120);
  return { version: 1, revision, settings: validateSettings(value.settings) };
}

function browserStorage() {
  try { return typeof localStorage === 'undefined' ? null : localStorage; } catch { return null; }
}

function localStorageOptions(options) {
  const url = options.url || SETTINGS_URL;
  return {
    storage: Object.hasOwn(options, 'storage') ? options.storage : browserStorage(),
    key: options.localKey || `memories.settings.local.v1:${url}`,
  };
}

/** A corrupt device override never blocks the album. Its status lets the admin
 * offer an explicit reset; merely visiting the album does not delete anything. */
export function readLocalSettings(options = {}) {
  const { storage, key } = localStorageOptions(options);
  if (!storage) return { document: null, status: 'unavailable' };
  let saved;
  try { saved = storage.getItem(key); }
  catch { return { document: null, status: 'unavailable' }; }
  if (saved === null || saved === undefined) return { document: null, status: 'none' };
  try { return { document: validateSettingsDocument(JSON.parse(saved)), status: 'saved' }; }
  catch { return { document: null, status: 'invalid' }; }
}

let localRevisionCounter = 0;
function localRevision() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') return `local-${crypto.randomUUID()}`;
  return `local-${Date.now()}-${++localRevisionCounter}`;
}

/** Save only this browser's editable settings; never claim a successful save
 * when storage is blocked, full, or silently drops a write. */
export function saveLocalSettings(value, options = {}) {
  const document = { version: 1, revision: localRevision(), settings: validateSettings(value) };
  const { storage, key } = localStorageOptions(options);
  try {
    if (!storage) throw new Error('Storage unavailable');
    const serialized = JSON.stringify(document);
    storage.setItem(key, serialized);
    if (storage.getItem(key) !== serialized) throw new Error('Save was not retained');
  } catch {
    throw new Error('This browser could not save your settings. Allow website storage and try again.');
  }
  return document;
}

export function clearLocalSettings(options = {}) {
  const { storage, key } = localStorageOptions(options);
  try {
    if (!storage) throw new Error('Storage unavailable');
    storage.removeItem(key);
    const remaining = storage.getItem(key);
    if (remaining !== null && remaining !== undefined) throw new Error('Reset was not retained');
  } catch {
    throw new Error('This browser could not reset your settings. Allow website storage and try again.');
  }
}

/** Explicit device choices win even offline. Without a device override, load
 * the shared defaults, then use their validated cache if the network fails. */
export async function loadSettings(defaultSettings, options = {}) {
  const defaults = validateSettings(defaultSettings);
  const url = options.url || SETTINGS_URL;
  const cacheKey = options.cacheKey || `memories.settings.v1:${url}`;
  const storage = Object.hasOwn(options, 'storage') ? options.storage : browserStorage();
  const local = readLocalSettings({ ...options, storage, url });
  if (local.document) return { document: local.document, source: 'local', localStatus: local.status };
  const fetchImpl = options.fetchImpl || fetch;
  const controller = new AbortController();
  let timer;
  try {
    const timeout = new Promise((_, reject) => {
      timer = setTimeout(() => { controller.abort(); reject(new Error('Settings request timed out.')); }, options.timeoutMs ?? 6000);
    });
    const request = (async () => {
      const response = await fetchImpl(url, { cache: 'no-cache', signal: controller.signal });
      if (!response.ok) throw new Error('Published settings are unavailable.');
      return validateSettingsDocument(await response.json());
    })();
    const document = await Promise.race([request, timeout]);
    try { storage?.setItem(cacheKey, JSON.stringify(document)); } catch {}
    return { document, source: 'published', localStatus: local.status };
  } catch {
    try {
      const cached = storage?.getItem(cacheKey);
      if (cached) return { document: validateSettingsDocument(JSON.parse(cached)), source: 'cached', localStatus: local.status };
    } catch {}
    return { document: { version: 1, revision: 'bootstrap', settings: defaults }, source: 'defaults', localStatus: local.status };
  } finally {
    clearTimeout(timer);
  }
}
