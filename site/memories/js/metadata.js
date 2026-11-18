// Approved, portable search metadata. Drafts and face descriptors never belong
// in this file format: only names, tags and explicitly approved captions.

/** Tidy comma/semicolon-separated labels, preserving the first spelling. */
export function uniqueLabels(values) {
  const list = typeof values === 'string' ? values.split(/[,;]+/) : Array.isArray(values) ? values : [];
  const seen = new Set();
  return list.filter((value) => typeof value === 'string').map((value) => value.normalize('NFC').replace(/\s+/g, ' ').trim()).filter((value) => {
    const key = value.toLowerCase();
    if (!value || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function record(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/** Validate an approved sidecar and strip anything outside its public schema. */
export function validateMetadata(value) {
  if (!record(value) || value.version !== 1 || !record(value.photos)) {
    throw new Error('Use a tags file with version: 1 and a photos object.');
  }
  const entries = Object.entries(value.photos).map(([id, entry]) => {
    if (!id.trim() || !record(entry)) throw new Error('Each photo needs an ID and a metadata object.');
    const clean = {};
    for (const field of ['tags', 'people']) {
      if (!Object.hasOwn(entry, field)) continue;
      if (!Array.isArray(entry[field]) || entry[field].some((label) => typeof label !== 'string')) {
        throw new Error(`The ${field} for photo ${id} must be a list of text labels.`);
      }
      clean[field] = uniqueLabels(entry[field]);
    }
    if (Object.hasOwn(entry, 'caption')) {
      if (typeof entry.caption !== 'string') throw new Error(`The caption for photo ${id} must be text.`);
      clean.caption = entry.caption.trim();
    }
    return [id, clean];
  });
  return { version: 1, photos: Object.fromEntries(entries) };
}

/** Merge approved labels into their exact IDs; never change the source object. */
export function applyMetadata(raw, value) {
  const metadata = validateMetadata(value);
  return {
    ...raw,
    photos: (raw.photos || []).map((photo) => {
      if (!Object.hasOwn(metadata.photos, photo.id)) return photo;
      const entry = metadata.photos[photo.id];
      return {
        ...photo,
        tags: uniqueLabels([...uniqueLabels(photo.tags), ...(entry.tags || [])]),
        people: uniqueLabels([...uniqueLabels(photo.people), ...(entry.people || [])]),
        ...(Object.hasOwn(entry, 'caption') ? { caption: entry.caption } : {}),
      };
    }),
  };
}

/** An optional tags file must never prevent the family from opening the album. */
export async function loadMetadata(url) {
  if (!url) return null;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 6000);
  try {
    const response = await fetch(url, { cache: 'no-cache', signal: controller.signal });
    if (!response.ok) return null;
    return validateMetadata(await response.json());
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}
