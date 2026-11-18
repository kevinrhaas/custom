import { validateSettingsDocument } from '../js/settings.js';
import { validateMetadata } from '../js/metadata.js';

// These destinations cannot be changed by imported/public album settings.
export const PUBLISH_TARGET = Object.freeze({
  repository: 'kevinrhaas/custom', branch: 'main',
  path: 'site/memories/data/settings.json',
  metadataPath: 'site/memories/data/tags.json',
});
const ENDPOINT = `https://api.github.com/repos/${PUBLISH_TARGET.repository}/contents/${PUBLISH_TARGET.path}`;
const METADATA_ENDPOINT = `https://api.github.com/repos/${PUBLISH_TARGET.repository}/contents/${PUBLISH_TARGET.metadataPath}`;
const validSha = value => typeof value === 'string' && /^[a-f0-9]{40,64}$/.test(value);

function failure(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

function encodeDocument(document, maxBytes = 64 * 1024) {
  const bytes = new TextEncoder().encode(`${JSON.stringify(document, null, 2)}\n`);
  if (bytes.length > maxBytes) throw failure('invalid', 'The album data is too large to save.');
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function decodeDocument(file, validate = validateSettingsDocument, maxEncodedBytes = 100_000) {
  if (!file || file.type !== 'file' || file.encoding !== 'base64' || !validSha(file.sha) || typeof file.content !== 'string' || file.content.length > maxEncodedBytes) {
    throw failure('invalid-response', 'The saved album settings could not be read.');
  }
  try {
    const bytes = Uint8Array.from(atob(file.content.replace(/\s/g, '')), character => character.charCodeAt(0));
    return validate(JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)));
  } catch {
    throw failure('invalid-response', 'The saved album settings are not valid. Ask the site maintainer to check them.');
  }
}

/** Publishing credentials live only in this closure, never in browser storage. */
export function createPublisher({ fetchImpl = (...args) => fetch(...args), timeoutMs = 20_000 } = {}) {
  let token = '';
  let generation = 0;
  const pending = new Set();

  function disconnect() {
    token = '';
    generation++;
    for (const controller of pending) controller.abort();
    pending.clear();
  }

  async function request(credential, expectedGeneration, method = 'GET', body, endpoint = ENDPOINT) {
    const controller = new AbortController();
    pending.add(controller);
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetchImpl(method === 'GET' ? `${endpoint}?ref=${PUBLISH_TARGET.branch}` : endpoint, {
        method, signal: controller.signal, cache: 'no-store', credentials: 'omit',
        redirect: 'error', referrerPolicy: 'no-referrer',
        headers: {
          Accept: 'application/vnd.github+json',
          Authorization: `Bearer ${credential}`,
          'X-GitHub-Api-Version': '2022-11-28',
          ...(body ? { 'Content-Type': 'application/json' } : {}),
        },
        ...(body ? { body: JSON.stringify(body) } : {}),
      });
      if (generation !== expectedGeneration) throw failure('disconnected', 'Publishing was disconnected. Connect again before saving.');
      if (!response.ok) {
        if (response.status === 401) {
          disconnect();
          throw failure('unauthorized', 'The publishing credential was rejected or expired. Connect with a valid one.');
        }
        if (response.status === 409 || response.status === 422) throw failure('conflict', 'The saved settings changed, or GitHub could not accept this revision. Reload the saved settings before trying again.');
        if (response.status === 429 || response.headers?.get('x-ratelimit-remaining') === '0') throw failure('rate-limit', 'GitHub is temporarily limiting saves. Try again later.');
        if (response.status === 403) throw failure('forbidden', 'This credential cannot save here. Allow Contents: read and write for the custom repository.');
        if (response.status === 404) throw failure('not-found', 'The saved settings could not be found. Check that the credential has access to the custom repository.');
        throw failure('unavailable', 'GitHub could not complete the request. Check the saved settings before trying again.');
      }
      const result = await response.json();
      if (generation !== expectedGeneration) throw failure('disconnected', 'Publishing was disconnected. Connect again before saving.');
      return result;
    } catch (error) {
      if (error.code && ['disconnected', 'unauthorized', 'conflict', 'rate-limit', 'forbidden', 'not-found', 'unavailable'].includes(error.code)) throw error;
      if (generation !== expectedGeneration) throw failure('disconnected', 'Publishing was disconnected. Connect again before saving.');
      // A failed response does not prove a PUT failed. Never retry it automatically.
      throw failure('network', method === 'PUT'
        ? 'The save could not be confirmed. Reconnect to check the saved settings before trying again.'
        : 'Could not reach publishing. Check your connection and try again.');
    } finally {
      clearTimeout(timer);
      pending.delete(controller);
    }
  }

  function connected() {
    if (!token) throw failure('disconnected', 'Connect publishing before saving album settings.');
  }

  return {
    disconnect,
    isConnected: () => !!token,
    async connect(value) {
      disconnect();
      if (typeof value !== 'string' || !value.trim() || /\s/.test(value.trim()) || value.length > 512) {
        throw failure('credential', 'Enter a valid publishing credential.');
      }
      const candidate = value.trim();
      const expected = generation;
      const file = await request(candidate, expected);
      const document = decodeDocument(file);
      if (generation !== expected) throw failure('disconnected', 'Publishing was disconnected. Connect again before saving.');
      token = candidate;
      return { document, sha: file.sha };
    },
    async read() {
      connected();
      const file = await request(token, generation);
      return { document: decodeDocument(file), sha: file.sha };
    },
    async save(value, expectedSha) {
      connected();
      if (!validSha(expectedSha)) throw failure('conflict', 'Load the current saved settings before saving.');
      const document = validateSettingsDocument(value);
      const result = await request(token, generation, 'PUT', {
        message: 'Family album: save settings from admin',
        branch: PUBLISH_TARGET.branch,
        sha: expectedSha, content: encodeDocument(document),
      });
      if (!validSha(result?.content?.sha) || !validSha(result?.commit?.sha)) {
        throw failure('invalid-response', 'The save response was incomplete. Reconnect to check the saved settings before trying again.');
      }
      return { document, sha: result.content.sha, commitSha: result.commit.sha };
    },
    async readMetadata() {
      connected();
      const file = await request(token, generation, 'GET', undefined, METADATA_ENDPOINT);
      return { document: decodeDocument(file, validateMetadata, 1_000_000), sha: file.sha };
    },
    async saveMetadata(value, expectedSha) {
      connected();
      if (!validSha(expectedSha)) throw failure('conflict', 'Load the current approved tags before saving.');
      const document = validateMetadata(value);
      const result = await request(token, generation, 'PUT', {
        message: 'Family album: save approved photo tags from admin',
        branch: PUBLISH_TARGET.branch, sha: expectedSha,
        content: encodeDocument(document, 700_000),
      }, METADATA_ENDPOINT);
      if (!validSha(result?.content?.sha) || !validSha(result?.commit?.sha)) {
        throw failure('invalid-response', 'The save response was incomplete. Reload the approved tags before trying again.');
      }
      return { document, sha: result.content.sha, commitSha: result.commit.sha };
    },
  };
}

export const publisher = createPublisher();
