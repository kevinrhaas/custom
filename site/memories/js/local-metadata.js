import { validateMetadata } from './metadata.js';

// Only explicit saves reach the album. Work in progress uses a separate key.
export function localMetadataKey(config) {
  const prefix = config.access?.prefix || 'memories';
  const source = config.source === 'drive' ? `drive.${config.drive?.folderId || ''}` : `manifest.${config.manifestUrl || 'data/library.json'}`;
  return `${prefix}.approved.v1.${source}`;
}

function storageFor(options) {
  return Object.hasOwn(options, 'storage') ? options.storage : globalThis.localStorage;
}

export function readLocalMetadata(config, options = {}) {
  try {
    const storage = storageFor(options);
    if (!storage) return { document: null, status: 'unavailable' };
    const saved = storage.getItem(localMetadataKey(config));
    if (saved === null) return { document: null, status: 'none' };
    try {
      return { document: validateMetadata(JSON.parse(saved)), status: 'saved' };
    } catch {
      return { document: null, status: 'invalid' };
    }
  } catch {
    return { document: null, status: 'unavailable' };
  }
}

export function saveLocalMetadata(config, value, options = {}) {
  const document = validateMetadata(value);
  const serialized = JSON.stringify(document);
  try {
    const storage = storageFor(options);
    if (!storage) throw new Error();
    const key = localMetadataKey(config);
    storage.setItem(key, serialized);
    if (storage.getItem(key) !== serialized) throw new Error();
  } catch {
    throw new Error('This browser could not save the approved additions. Download a backup before leaving.');
  }
  return document;
}

export function clearLocalMetadata(config, options = {}) {
  try {
    const storage = storageFor(options);
    if (!storage) throw new Error();
    const key = localMetadataKey(config);
    storage.removeItem(key);
    if (storage.getItem(key) !== null) throw new Error();
  } catch {
    throw new Error('This browser could not clear the saved additions.');
  }
}
