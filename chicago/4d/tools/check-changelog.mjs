#!/usr/bin/env node
/**
 * Verify the fleet changelog contract.
 *
 * `site/chicago/4d/js/changelog.js` is parsed live by Manager and by the
 * polecat.live launcher — NOT executed, but read with a bracket-aware walker
 * that converts the JS literal to JSON. That is why the format is strict and
 * why breaking it is a fleet problem rather than a local one: two documented
 * corruptions in the fleet's history came from regexes running inside string
 * values. See polecat-platform docs/SHELL-API.md.
 */
import { readFileSync } from 'node:fs';

const FILE = new URL('../../../site/chicago/4d/js/changelog.js', import.meta.url);
const problems = [];

const src = readFileSync(FILE, 'utf8');
if (!/export const CHANGELOG\s*=\s*\[/.test(src)) problems.push('no `export const CHANGELOG = [`');
if (!/export const LATEST_VERSION\s*=/.test(src)) problems.push('no `export const LATEST_VERSION`');

const { CHANGELOG, LATEST_VERSION } = await import(FILE);

if (!Array.isArray(CHANGELOG) || !CHANGELOG.length) problems.push('CHANGELOG is empty');
if (LATEST_VERSION !== CHANGELOG[0]?.v) problems.push('LATEST_VERSION is not CHANGELOG[0].v');

let prev = Infinity;
for (const e of CHANGELOG) {
  const at = `v${e.v}`;
  for (const k of ['v', 'title', 'kind', 'ts', 'date', 'items']) {
    if (e[k] === undefined) problems.push(`${at}: missing ${k}`);
  }
  if (typeof e.v !== 'number') problems.push(`${at}: v must be a number`);
  if (e.v >= prev) problems.push(`${at}: entries must be newest-first by v`);
  prev = e.v;
  if (!e.ts) problems.push(`${at}: empty ts — run tools/stamp-changelog.mjs before merging`);
  if (e.ts && Number.isNaN(Date.parse(e.ts))) problems.push(`${at}: ts is not a date`);
  if (!Array.isArray(e.items) || !e.items.length) problems.push(`${at}: no items`);
  for (const it of e.items || []) {
    // A `//` inside item text breaks naive comment-stripping in some parsers.
    if (String(it).includes('//')) problems.push(`${at}: an item contains "//"`);
  }
}

if (problems.length) {
  console.error('changelog contract FAILED:');
  for (const p of problems) console.error('  - ' + p);
  process.exit(1);
}
console.log(`changelog contract OK — ${CHANGELOG.length} entr${CHANGELOG.length === 1 ? 'y' : 'ies'}, latest v${LATEST_VERSION}`);
