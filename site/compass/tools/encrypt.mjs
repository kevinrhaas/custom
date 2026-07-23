#!/usr/bin/env node
/* Compass payload builder.
   Usage: node tools/encrypt.mjs <plaintext.json> <passcode>
   Writes js/payload.js (AES-256-GCM, PBKDF2-SHA256 x310k — mirrors js/app.js).
   The plaintext JSON must NEVER be committed; keep it outside the repo. */
import { webcrypto as wc } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const [, , plainPath, passcodeRaw] = process.argv;
if (!plainPath || !passcodeRaw) {
  console.error('Usage: node tools/encrypt.mjs <plaintext.json> <passcode>');
  process.exit(1);
}
// Mirror js/app.js normalizePass: only letters and digits count.
const passcode = passcodeRaw.toLowerCase().replace(/[^a-z0-9]/g, '');
const data = readFileSync(plainPath, 'utf8');
JSON.parse(data); // validate before encrypting

const enc = new TextEncoder();
const salt = wc.getRandomValues(new Uint8Array(16));
const iv = wc.getRandomValues(new Uint8Array(12));
const keyMaterial = await wc.subtle.importKey('raw', enc.encode(passcode), { name: 'PBKDF2' }, false, ['deriveKey']);
const key = await wc.subtle.deriveKey(
  { name: 'PBKDF2', salt, iterations: 310000, hash: 'SHA-256' },
  keyMaterial, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
const ct = new Uint8Array(await wc.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(data)));

const b64 = (u8) => Buffer.from(u8).toString('base64');
const out = '/* Encrypted Compass payload — built by tools/encrypt.mjs. ' +
  'Ciphertext only; the passcode is not in this repo. */\n' +
  'window.COMPASS_PAYLOAD = ' + JSON.stringify({ v: 1, salt: b64(salt), iv: b64(iv), ct: b64(ct) }) + ';\n';

const dest = join(dirname(fileURLToPath(import.meta.url)), '..', 'js', 'payload.js');
writeFileSync(dest, out);
console.log('Wrote', dest, '(' + ct.length + ' bytes ciphertext)');
