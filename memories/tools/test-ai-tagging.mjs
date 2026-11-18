import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile, rm, stat } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { imageInfo, normalizeDraft, parseDraftResponse, requestDraft, tagPhotos, DEFAULT_MODEL } from './tag-photos.mjs';

const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=', 'base64');
const result = (tags = ['horse', 'farm'], caption = 'A horse stands beside a fence.') => ({ content: [{ type: 'text', text: JSON.stringify({ tags, caption }) }], stop_reason: 'end_turn' });
const ok = body => ({ ok: true, status: 200, json: async () => body });
const rejected = (status, retryAfter = null) => ({ ok: false, status, headers: { get: () => retryAfter } });
async function fixture(t, photos = [{ id: 'one', path: 'one.png' }]) {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'memories-ai-test-'));
  t.after(() => rm(directory, { recursive: true, force: true }));
  const inputPath = path.join(directory, 'photo-list.json');
  const outputPath = path.join(directory, 'album.drafts.json');
  await writeFile(inputPath, JSON.stringify({ photos }));
  for (const photo of photos) if (photo.path && !photo.path.includes(':')) await writeFile(path.join(directory, photo.path), PNG);
  return { directory, inputPath, outputPath };
}

test('recognizes PNG/JPEG dimensions and rejects unsupported or oversized images', () => {
  assert.deepEqual(imageInfo(PNG), { mime: 'image/png', width: 1, height: 1 });
  const jpeg = Buffer.from([255,216,255,192,0,11,8,0,20,0,30,1,1,17,0,255,217]);
  assert.deepEqual(imageInfo(jpeg), { mime: 'image/jpeg', width: 30, height: 20 });
  assert.throws(() => imageInfo(Buffer.from('not an image')), /JPG or PNG/);
  const tooWide = Buffer.from(PNG); tooWide.writeUInt32BE(9000, 16);
  assert.throws(() => imageInfo(tooWide), /8,000 pixels/);
  assert.throws(() => imageInfo(Buffer.concat([PNG, Buffer.alloc(5 * 1024 * 1024)])), /5 MiB/);
});

test('normalizes only the draft contract and validates provider JSON', () => {
  assert.deepEqual(normalizeDraft({ tags: [' Horse ', 'horse', ''], caption: ' A horse. ', people: ['June'] }), { tags: ['horse'], caption: 'A horse.' });
  assert.throws(() => normalizeDraft({ tags: [1], caption: 'Photo' }), /too long/);
  assert.throws(() => normalizeDraft({ tags: [], caption: 3 }), /invalid draft/);
  assert.throws(() => parseDraftResponse({ content: [], stop_reason: 'max_tokens' }), /incomplete/);
  assert.throws(() => parseDraftResponse({ content: [{ type: 'text', text: 'not JSON' }] }), /unreadable/);
  assert.deepEqual(parseDraftResponse({ content: [{ type: 'text', text: '```json\n{"tags":["lake"],"caption":"A lake."}\n```' }] }), { tags: ['lake'], caption: 'A lake.' });
});

test('calls only Anthropic with base64 image and no local path or caption context', async () => {
  let call;
  const draft = await requestDraft({ bytes: PNG, mime: 'image/png', apiKey: 'test-secret', fetchImpl: async (url, options) => { call = { url, options }; return ok(result()); } });
  assert.equal(call.url, 'https://api.anthropic.com/v1/messages');
  assert.equal(call.options.headers['x-api-key'], 'test-secret');
  const body = JSON.parse(call.options.body);
  assert.equal(body.model, DEFAULT_MODEL);
  assert.equal(body.messages[0].content[0].source.data, PNG.toString('base64'));
  assert.match(body.system, /Do not identify or name people/);
  assert.deepEqual(draft.tags, ['horse', 'farm']);
});

test('retries rate limits and server failures with a bounded retry-after', async () => {
  let calls = 0; const waits = [];
  await requestDraft({ bytes: PNG, mime: 'image/png', apiKey: 'test-secret', fetchImpl: async () => [rejected(429, '600'), rejected(503), ok(result())][calls++], sleep: async ms => waits.push(ms) });
  assert.equal(calls, 3); assert.deepEqual(waits, [30000, 2000]);
  calls = 0;
  await assert.rejects(requestDraft({ bytes: PNG, mime: 'image/png', apiKey: 'test-secret', fetchImpl: async () => { calls++; return rejected(429); }, sleep: async () => {} }), /HTTP 429/);
  assert.equal(calls, 4);
});

test('fails without a key and avoids secret or response leakage on errors', async () => {
  let calls = 0;
  const fetchImpl = async () => { calls++; return { ...rejected(401), json: async () => ({ error: 'test-secret' }) }; };
  await assert.rejects(requestDraft({ bytes: PNG, mime: 'image/png', fetchImpl }), /ANTHROPIC_API_KEY/);
  assert.equal(calls, 0);
  await assert.rejects(requestDraft({ bytes: PNG, mime: 'image/png', apiKey: 'test-secret', fetchImpl }), error => /HTTP 401/.test(error.message) && !error.message.includes('test-secret'));
  assert.equal(calls, 1);
  await assert.rejects(requestDraft({ bytes: PNG, mime: 'image/png', apiKey: 'test-secret', fetchImpl: async () => { throw new Error('test-secret'); } }), error => /timed out/.test(error.message) && !error.message.includes('test-secret'));
});

test('saves drafts privately, skips unchanged photos, and refreshes changed image or model', async t => {
  const files = await fixture(t, [{ id: 'one', path: 'one.png' }, { id: 'two', path: 'two.png' }]);
  let calls = 0;
  const settings = { ...files, apiKey: 'test-secret', fetchImpl: async () => { calls++; return ok(result()); } };
  assert.deepEqual(await tagPhotos(settings), { processed: 2, skipped: 0, outputPath: files.outputPath });
  assert.equal(calls, 2);
  const output = JSON.parse(await readFile(files.outputPath, 'utf8'));
  assert.equal(output.version, 1);
  assert.equal(output.provenance.one.sha256.length, 64);
  assert.equal((await stat(files.outputPath)).mode & 0o777, 0o600);
  assert.deepEqual(Object.keys(output.photos.one).sort(), ['caption', 'tags']);
  assert.equal((await tagPhotos({ ...settings, apiKey: undefined })).skipped, 2);
  assert.equal(calls, 2);
  await writeFile(path.join(files.directory, 'two.png'), Buffer.concat([PNG, Buffer.from('changed')]));
  assert.equal((await tagPhotos(settings)).processed, 1);
  assert.equal(calls, 3);
  assert.equal((await tagPhotos({ ...settings, model: 'different-model' })).processed, 2);
  assert.equal(calls, 5);
});

test('keeps completed drafts after a failed photo and resumes without repeating them', async t => {
  const files = await fixture(t, [{ id: 'one', path: 'one.png' }, { id: 'two', path: 'two.png' }]);
  let calls = 0;
  await assert.rejects(tagPhotos({ ...files, apiKey: 'test-secret', fetchImpl: async () => ++calls === 1 ? ok(result()) : rejected(401) }), /HTTP 401/);
  assert.deepEqual(Object.keys(JSON.parse(await readFile(files.outputPath, 'utf8')).photos), ['one']);
  const resumed = await tagPhotos({ ...files, apiKey: 'test-secret', fetchImpl: async () => { calls++; return ok(result()); } });
  assert.equal(resumed.processed, 1); assert.equal(resumed.skipped, 1); assert.equal(calls, 3);
});

test('validates all input files and duplicate IDs before any paid request', async t => {
  const files = await fixture(t, [{ id: 'one', path: 'one.png' }, { id: 'two', path: 'two.png' }]);
  let calls = 0;
  const settings = { ...files, apiKey: 'test-secret', fetchImpl: async () => { calls++; return ok(result()); } };
  await writeFile(path.join(files.directory, 'two.png'), 'broken');
  await assert.rejects(tagPhotos(settings), /JPG or PNG/);
  assert.equal(calls, 0);
  for (const photos of [[{ id: 'one', path: 'https://example.test/one.png' }], [{ id: 'one', path: 'one.png' }, { id: 'one', path: 'one.png' }], [{ id: '__proto__', path: 'one.png' }]]) {
    await writeFile(files.inputPath, JSON.stringify({ photos }));
    await assert.rejects(tagPhotos(settings), /local JPG|unique/);
    assert.equal(calls, 0);
  }
  await writeFile(files.inputPath, JSON.stringify({ photos: [{ id: 'one', path: 'one.png' }, { id: 'two', path: './one.png' }] }));
  await assert.rejects(tagPhotos(settings), /same local path/);
  assert.equal(calls, 0);
});

test('supports local src manifests and root override without overwriting input', async t => {
  const files = await fixture(t);
  await writeFile(files.inputPath, JSON.stringify({ photos: [{ id: 'one', src: 'one.png' }] }));
  await tagPhotos({ ...files, imageRoot: files.directory, apiKey: 'test-secret', fetchImpl: async () => ok(result()) });
  await assert.rejects(tagPhotos({ ...files, outputPath: files.inputPath }), /separate draft/);
  await writeFile(files.outputPath, 'not JSON');
  await assert.rejects(tagPhotos(files), /existing output file/);
});
