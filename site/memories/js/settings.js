// Shared, public album settings. Admin publishing credentials and invite keys
// never belong in this schema; the runtime retains those bootstrap boundaries.
import { SKINS } from './skins.js';

export const SETTINGS_URL = new URL('../data/settings.json', import.meta.url).href;
export const EDITABLE_FIELDS = Object.freeze(['title', 'honorees', 'dedication', 'keeper', 'helper', 'people', 'sample', 'source', 'drive', 'defaultSkin']);
const skinIds = new Set(SKINS.map(skin => skin.id));
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);

function text(value, label, max, { optional = false, multiline = false } = {}) {
  if (typeof value !== 'string') throw new Error(`${label} must be text.`);
  const clean = value.normalize('NFC').replace(/\r\n?/g, '\n').trim();
  if ((!optional && !clean) || clean.length > max) throw new Error(`${label} ${optional ? 'must be' : 'is required and must be'} ${max} characters or fewer.`);
  const controls = multiline ? /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/ : /[\u0000-\u001f\u007f]/;
  if (controls.test(clean)) throw new Error(`${label} contains unsupported control characters.`);
  return clean;
}

export function normalizeFolderId(value) {
  const input = text(value, 'Drive folder', 1000, { optional: true });
  if (!input) return '';
  let id = input;
  if (/^https?:\/\//i.test(input)) {
    let url;
    try { url = new URL(input); } catch { throw new Error('Enter a Google Drive folder link or folder ID.'); }
    if (url.protocol !== 'https:' || url.hostname !== 'drive.google.com' || url.username || url.password) throw new Error('Use a secure drive.google.com folder link.');
    const match = url.pathname.match(/\/folders\/([A-Za-z0-9_-]+)\/?$/);
    id = match?.[1] || (url.pathname === '/open' ? url.searchParams.get('id') : '') || '';
  }
  if (!/^[A-Za-z0-9_-]{10,200}$/.test(id)) throw new Error('Enter a valid Google Drive folder link or folder ID.');
  return id;
}

/** Return only the public fields that the admin can edit. */
export function settingsFromConfig(config) {
  return validateSettings(Object.fromEntries(EDITABLE_FIELDS.map(field => [field, config[field]])));
}

/** Strictly validate known fields and discard every unknown field. */
export function validateSettings(value) {
  if (!record(value)) throw new Error('Album settings must be an object.');
  if (!Array.isArray(value.honorees) || value.honorees.length < 1 || value.honorees.length > 8) throw new Error('Add between one and eight people the album remembers.');
  const honorees = value.honorees.map(person => {
    if (!record(person)) throw new Error('Each person needs a name and years.');
    return { name: text(person.name, 'Name', 120), years: text(person.years, 'Years', 100, { optional: true }) };
  });
  if (!Array.isArray(value.people) || value.people.length > 300) throw new Error('Names to find in captions must be a list of at most 300 names.');
  const seen = new Set();
  const people = value.people.map(name => text(name, 'Searchable name', 120)).filter(name => {
    const key = name.toLocaleLowerCase();
    if (seen.has(key)) return false;
    seen.add(key); return true;
  });
  if (!['manifest', 'drive'].includes(value.source)) throw new Error('Choose sample photos or the Google Drive folder.');
  if (typeof value.sample !== 'boolean' || value.sample !== (value.source === 'manifest')) throw new Error('Sample photos must be marked as samples; a Drive album must use the real-photo setting.');
  if (!record(value.drive)) throw new Error('Drive settings must include an API key and folder.');
  const apiKey = text(value.drive.apiKey, 'Google browser API key', 120, { optional: true });
  if (apiKey && !/^AIza[A-Za-z0-9_-]{35}$/.test(apiKey)) throw new Error('Enter a Google browser API key beginning with AIza. Publishing and AI-service keys do not belong here.');
  const folderId = normalizeFolderId(value.drive.folderId);
  if (value.source === 'drive' && (!apiKey || !folderId)) throw new Error('Enter both the restricted Google API key and shared folder before choosing Drive photos.');
  if (!skinIds.has(value.defaultSkin)) throw new Error('Choose one of the available album looks.');
  return {
    title: text(value.title, 'Album title', 120),
    honorees,
    dedication: text(value.dedication, 'Dedication', 4000, { optional: true, multiline: true }),
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
  if (!record(value) || value.version !== 1) throw new Error('Use a version 1 album settings document.');
  const revision = text(value.revision, 'Settings revision', 120);
  return { version: 1, revision, settings: validateSettings(value.settings) };
}

function browserStorage() {
  try { return typeof localStorage === 'undefined' ? null : localStorage; } catch { return null; }
}

/** Network first; validated last-known settings keep a previously visited album
 * opening offline. This cache is public data, never an admin publishing secret. */
export async function loadSettings(defaultSettings, options = {}) {
  const defaults = validateSettings(defaultSettings);
  const url = options.url || SETTINGS_URL;
  const cacheKey = options.cacheKey || `memories.settings.v1:${url}`;
  const storage = Object.hasOwn(options, 'storage') ? options.storage : browserStorage();
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
    return { document, source: 'published' };
  } catch {
    try {
      const cached = storage?.getItem(cacheKey);
      if (cached) return { document: validateSettingsDocument(JSON.parse(cached)), source: 'cached' };
    } catch {}
    return { document: { version: 1, revision: 'bootstrap', settings: defaults }, source: 'defaults' };
  } finally {
    clearTimeout(timer);
  }
}
