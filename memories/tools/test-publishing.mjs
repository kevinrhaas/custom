import test from 'node:test';
import assert from 'node:assert/strict';
import { createPublisher, PUBLISH_TARGET } from '../../site/memories/admin/publishing.js';

const SECRET = 'github_pat_UNIT_TEST_ONLY_NEVER_REAL';
const SHA = 'a'.repeat(40);
const NEW_SHA = 'b'.repeat(40);
const COMMIT = 'c'.repeat(40);
const ENDPOINT = 'https://api.github.com/repos/kevinrhaas/custom/contents/site/memories/data/settings.json';
const document = () => ({
  version: 1,
  revision: 'test-revision',
  settings: {
    title: 'The García family — 家族',
    honorees: [{ name: 'José García', years: '1921–2019' }],
    dedication: 'Remembering our family.\n思い出を大切に。',
    keeper: 'Lauren', helper: 'Kevin', people: ['José', 'Zoë'],
    sample: true, source: 'manifest', drive: { apiKey: '', folderId: '' }, defaultSkin: 'heirloom',
  },
});
const contents = (value = document(), sha = SHA) => ({
  type: 'file', encoding: 'base64', sha,
  content: Buffer.from(JSON.stringify(value), 'utf8').toString('base64'),
});
const response = (body, status = 200, headers = {}) => ({
  ok: status >= 200 && status < 300, status,
  headers: new Headers(headers), json: async () => body,
});
const success = () => response({ content: { sha: NEW_SHA }, commit: { sha: COMMIT } });
function deferred() {
  let resolve;
  const promise = new Promise(done => { resolve = done; });
  return { promise, resolve };
}
function noSecret(error, code) {
  assert.equal(error.code, code);
  assert.equal(error.message.includes(SECRET), false);
  assert.equal(error.stack.includes(SECRET), false);
  return true;
}

test('connect/read/save use only the fixed repository, branch and path with UTF-8 roundtrip', async () => {
  const calls = [];
  const publisher = createPublisher({ fetchImpl: async (url, options) => {
    calls.push({ url, options });
    return options.method === 'PUT' ? success() : response(contents());
  } });
  assert.deepEqual(PUBLISH_TARGET, { repository: 'kevinrhaas/custom', branch: 'main', path: 'site/memories/data/settings.json', metadataPath: 'site/memories/data/tags.json' });
  assert.throws(() => { PUBLISH_TARGET.repository = 'someone/else'; }, TypeError);
  assert.deepEqual(await publisher.connect(SECRET), { document: document(), sha: SHA });
  assert.equal(publisher.isConnected(), true);
  assert.deepEqual(await publisher.read(), { document: document(), sha: SHA });
  assert.deepEqual(await publisher.save(document(), SHA), { document: document(), sha: NEW_SHA, commitSha: COMMIT });
  assert.deepEqual(calls.map(call => call.url), [`${ENDPOINT}?ref=main`, `${ENDPOINT}?ref=main`, ENDPOINT]);
  for (const { options } of calls) {
    assert.equal(options.headers.Authorization, `Bearer ${SECRET}`);
    assert.equal(options.cache, 'no-store');
    assert.equal(options.credentials, 'omit');
    assert.equal(options.redirect, 'error');
    assert.equal(options.referrerPolicy, 'no-referrer');
  }
  const put = JSON.parse(calls[2].options.body);
  assert.equal(put.branch, 'main'); assert.equal(put.sha, SHA);
  assert.deepEqual(JSON.parse(Buffer.from(put.content, 'base64').toString('utf8')), document());
  assert.equal(calls[2].options.body.includes(SECRET), false);
  publisher.disconnect();
});

test('published documents discard bootstrap fields and credentials from every editable record', async () => {
  const input = document();
  Object.assign(input, { githubToken: SECRET, access: { publicKey: 'attacker' }, repository: 'attacker/repo' });
  Object.assign(input.settings, { githubToken: SECRET, anthropicKey: SECRET, access: { enabled: false, publicKey: 'attacker' }, metadataUrl: 'https://attacker.invalid/', manifestUrl: 'https://attacker.invalid/', publishing: { repository: 'attacker/repo' } });
  input.settings.drive.privateKey = SECRET;
  input.settings.honorees[0].privateKey = SECRET;
  let written;
  const publisher = createPublisher({ fetchImpl: async (_, options) => {
    if (options.method === 'GET') return response(contents(input));
    written = JSON.parse(Buffer.from(JSON.parse(options.body).content, 'base64').toString('utf8'));
    return success();
  } });
  assert.deepEqual((await publisher.connect(SECRET)).document, document());
  await publisher.save(input, SHA);
  assert.deepEqual(written, document());
  assert.equal(JSON.stringify(written).includes(SECRET), false);
  publisher.disconnect();
});

test('SHA conflicts are surfaced without retrying or overwriting the other revision', async () => {
  let writes = 0;
  const publisher = createPublisher({ fetchImpl: async (_, options) => {
    if (options.method === 'GET') return response(contents());
    writes++;
    assert.equal(JSON.parse(options.body).sha, SHA);
    return response({ message: `${SECRET} provider detail` }, 409);
  } });
  await publisher.connect(SECRET);
  await assert.rejects(publisher.save(document(), SHA), error => noSecret(error, 'conflict'));
  assert.equal(writes, 1);
  await assert.rejects(publisher.save(document(), 'stale-not-a-sha'), error => noSecret(error, 'conflict'));
  assert.equal(writes, 1, 'invalid revisions must not send requests');
  publisher.disconnect();
});

test('denied credentials fail safely and never connect', async () => {
  for (const [status, code] of [[401, 'unauthorized'], [403, 'forbidden'], [404, 'not-found'], [422, 'conflict'], [429, 'rate-limit'], [500, 'unavailable']]) {
    let calls = 0;
    const publisher = createPublisher({ fetchImpl: async () => { calls++; return response({ message: SECRET }, status); } });
    await assert.rejects(publisher.connect(SECRET), error => noSecret(error, code));
    assert.equal(publisher.isConnected(), false);
    assert.equal(calls, 1);
  }
});

test('GitHub rate-limit 403 is distinguishable from a permission denial', async () => {
  const publisher = createPublisher({ fetchImpl: async () => response({ message: SECRET }, 403, { 'x-ratelimit-remaining': '0' }) });
  await assert.rejects(publisher.connect(SECRET), error => noSecret(error, 'rate-limit'));
});

test('an ambiguous network failure after PUT never retries and asks to check the saved revision', async () => {
  let writes = 0;
  const publisher = createPublisher({ fetchImpl: async (_, options) => {
    if (options.method === 'GET') return response(contents());
    writes++;
    throw new Error(`The response was lost after committing ${SECRET}`);
  } });
  await publisher.connect(SECRET);
  await assert.rejects(publisher.save(document(), SHA), error => {
    noSecret(error, 'network');
    assert.match(error.message, /could not be confirmed/);
    assert.match(error.message, /Reconnect/);
    return true;
  });
  assert.equal(writes, 1);
  publisher.disconnect();
});

test('disconnect invalidates a pending connect even when fetch ignores cancellation', async () => {
  const waiting = deferred();
  let signal;
  const publisher = createPublisher({ fetchImpl: async (_, options) => { signal = options.signal; return waiting.promise; } });
  const pending = publisher.connect(SECRET);
  const rejected = assert.rejects(pending, error => noSecret(error, 'disconnected'));
  publisher.disconnect();
  assert.equal(signal.aborted, true);
  waiting.resolve(response(contents()));
  await rejected;
  assert.equal(publisher.isConnected(), false);
  await assert.rejects(publisher.read(), error => noSecret(error, 'disconnected'));
});

test('disconnect while the response body is pending cannot restore the old credential', async () => {
  const body = deferred();
  const entered = deferred();
  const publisher = createPublisher({ fetchImpl: async () => ({ ...response(null), json: () => { entered.resolve(); return body.promise; } }) });
  const pending = publisher.connect(SECRET);
  const rejected = assert.rejects(pending, error => noSecret(error, 'disconnected'));
  await entered.promise;
  publisher.disconnect();
  body.resolve(contents());
  await rejected;
  assert.equal(publisher.isConnected(), false);
});

test('a later connection wins over an earlier pending connection', async () => {
  const old = deferred();
  const authorizations = [];
  const publisher = createPublisher({ fetchImpl: async (_, options) => {
    authorizations.push(options.headers.Authorization);
    return options.headers.Authorization === `Bearer ${SECRET}` ? old.promise : response(contents());
  } });
  const first = publisher.connect(SECRET);
  const rejected = assert.rejects(first, error => noSecret(error, 'disconnected'));
  await publisher.connect('replacement-test-credential');
  old.resolve(response(contents()));
  await rejected;
  assert.equal(publisher.isConnected(), true);
  await publisher.read();
  assert.equal(authorizations.at(-1), 'Bearer replacement-test-credential');
  publisher.disconnect();
});

test('malformed files and invalid settings never produce a connected publisher', async () => {
  const invalidSettings = document(); invalidSettings.settings.source = 'arbitrary-server';
  const malformed = [null, {}, { ...contents(), type: 'dir' }, { ...contents(), encoding: 'utf-8' }, { ...contents(), sha: 'bad' }, { ...contents(), content: '%%%' }, { ...contents(), content: Buffer.from('not json').toString('base64') }, { ...contents(), content: Buffer.from([0xff]).toString('base64') }, contents(invalidSettings)];
  for (const body of malformed) {
    const publisher = createPublisher({ fetchImpl: async () => response(body) });
    await assert.rejects(publisher.connect(SECRET), error => noSecret(error, 'invalid-response'));
    assert.equal(publisher.isConnected(), false);
  }
});

test('an incomplete successful PUT response is not reported as a confirmed save', async () => {
  for (const body of [null, {}, { content: { sha: NEW_SHA } }, { content: { sha: 'bad' }, commit: { sha: COMMIT } }]) {
    let writes = 0;
    const publisher = createPublisher({ fetchImpl: async (_, options) => {
      if (options.method === 'GET') return response(contents());
      writes++; return response(body);
    } });
    await publisher.connect(SECRET);
    await assert.rejects(publisher.save(document(), SHA), error => noSecret(error, 'invalid-response'));
    assert.equal(writes, 1);
    publisher.disconnect();
  }
});

test('invalid credentials, disconnected saves and invalid public settings never make requests', async () => {
  let calls = 0;
  const publisher = createPublisher({ fetchImpl: async () => { calls++; return response(contents()); } });
  for (const token of ['', null, 'has spaces', 'x'.repeat(513)]) {
    await assert.rejects(publisher.connect(token), error => noSecret(error, 'credential'));
  }
  await assert.rejects(publisher.save(document(), SHA), error => noSecret(error, 'disconnected'));
  assert.equal(calls, 0);
  await publisher.connect(SECRET);
  const invalid = document(); invalid.settings.drive.apiKey = SECRET;
  await assert.rejects(publisher.save(invalid, SHA), error => {
    assert.equal(error.message.includes(SECRET), false);
    return true;
  });
  assert.equal(calls, 1, 'invalid public settings must not reach GitHub');
  publisher.disconnect();
});

test('approved metadata has its own fixed destination and exports only public text', async () => {
  const metadata = { version: 1, photos: { 'photo-1': { tags: ['horse'], people: ['José'], caption: '家族と馬。' } } };
  const raw = structuredClone(metadata);
  raw.photos['photo-1'].descriptor = [0.1, 0.2];
  raw.photos['photo-1'].apiKey = SECRET;
  raw.provenance = { secret: SECRET };
  const calls = [];
  const metadataEndpoint = 'https://api.github.com/repos/kevinrhaas/custom/contents/site/memories/data/tags.json';
  const publisher = createPublisher({ fetchImpl: async (url, options) => {
    calls.push({ url, options });
    if (options.method === 'PUT') return success();
    return response(contents(url.startsWith(metadataEndpoint) ? raw : document()));
  } });
  await publisher.connect(SECRET);
  assert.deepEqual(await publisher.readMetadata(), { document: metadata, sha: SHA });
  assert.deepEqual(await publisher.saveMetadata(raw, SHA), { document: metadata, sha: NEW_SHA, commitSha: COMMIT });
  assert.equal(calls[1].url, `${metadataEndpoint}?ref=main`);
  assert.equal(calls[2].url, metadataEndpoint);
  const body = JSON.parse(calls[2].options.body);
  assert.equal(body.branch, 'main'); assert.equal(body.sha, SHA);
  const published = Buffer.from(body.content, 'base64').toString('utf8');
  assert.deepEqual(JSON.parse(published), metadata);
  assert.equal(published.includes(SECRET), false);
  assert.equal(published.includes('descriptor'), false);
  publisher.disconnect();
});

test('metadata conflicts and invalid revisions never get a second write attempt', async () => {
  let writes = 0;
  const metadata = { version: 1, photos: {} };
  const publisher = createPublisher({ fetchImpl: async (_, options) => {
    if (options.method === 'GET') return response(contents());
    writes++; return response({ message: SECRET }, 409);
  } });
  await publisher.connect(SECRET);
  await assert.rejects(publisher.saveMetadata(metadata, SHA), error => noSecret(error, 'conflict'));
  assert.equal(writes, 1);
  await assert.rejects(publisher.saveMetadata(metadata, ''), error => noSecret(error, 'conflict'));
  assert.equal(writes, 1);
  publisher.disconnect();
});
