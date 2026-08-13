#!/usr/bin/env node
/**
 * Verify the fleet changelog contract.
 *
 * The file is authored at `renderers/web/js/changelog.js` — inside the app,
 * because the app displays it in its What's-new tab and a walkthrough cannot
 * import from the publish mirror. `tools/publish.sh` copies it to
 * `site/chicago/4d/js/changelog.js`, which is the URL Manager and the
 * polecat.live launcher fetch.
 *
 * They do not EXECUTE it — they read it with a bracket-aware walker that
 * converts the JS literal to JSON. That is why the format is strict and why
 * breaking it is a fleet problem rather than a local one: two documented
 * corruptions in the fleet's history came from regexes running inside string
 * values. See polecat-platform docs/SHELL-API.md.
 */
import { readFileSync } from 'node:fs';

const FILE = new URL('../renderers/web/js/changelog.js', import.meta.url);
const problems = [];

const src = readFileSync(FILE, 'utf8');
if (!/export const CHANGELOG\s*=\s*\[/.test(src)) problems.push('no `export const CHANGELOG = [`');
if (!/export const LATEST_VERSION\s*=/.test(src)) problems.push('no `export const LATEST_VERSION`');

/**
 * The literal's SHAPE, read as text, before anything tries to execute it.
 *
 * This exists because of a real corruption on 2026-08-13. `.gitattributes`
 * merges this file with `merge=union` — two branches each prepend an entry and
 * union keeps both instead of conflicting — and merging two such branches
 * dropped exactly one `] },`. Every entry below that point was then nested
 * INSIDE the entry above it: 64 entries, back to the first building, sitting
 * in the file and reaching nobody. The union driver runs during the merge, so
 * both parents can be green and the merge result still broken.
 *
 * Executing the module is a weaker test than this walk, for two reasons.
 * A missing terminator does not always produce a syntax error at all — a
 * swallowed entry is still a valid object literal inside an array — and when
 * it does, node reports it at the LAST line of the file, hundreds of lines
 * from the entry that actually lost its closing line. And Manager and the
 * launcher never execute this file: they read it with a bracket-aware walker,
 * so the shape is the contract, not the semantics.
 *
 * Every entry must open at bracket depth 1 — directly inside `CHANGELOG = [`.
 * An entry that opens deeper is one that got swallowed, and the entry before
 * it is the one that lost its terminator.
 */
function scanShape(text) {
  const found = [];
  let depth = 0;
  let line = 1;
  let quote = null;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '\n') { line++; continue; }
    if (quote) {
      if (c === '\\') i++;                       // an escaped quote is content
      else if (c === quote) quote = null;
      continue;
    }
    if (c === "'" || c === '"' || c === '`') { quote = c; continue; }
    if (c === '{' || c === '[') {
      // The entry header is written on one line by every tool that writes it.
      if (c === '{' && /^\{ v: (null|\d+),/.test(text.slice(i, i + 24))) {
        found.push({ line, depth, v: /^\{ v: (null|\d+),/.exec(text.slice(i, i + 24))[1] });
      }
      depth++;
    } else if (c === '}' || c === ']') {
      depth--;
      if (depth < 0) return { entries: found, problem: `unbalanced bracket at line ${line}` };
    }
  }
  if (quote) return { entries: found, problem: `unterminated ${quote} string` };
  if (depth !== 0) {
    return { entries: found, problem: `the literal never closes — ${depth} unclosed bracket(s). `
      + 'An entry is missing its `] },`' };
  }
  return { entries: found, problem: null };
}

const shape = scanShape(src);
if (shape.problem) problems.push(shape.problem);
if (!shape.entries.length) problems.push('no entries found — the `{ v: N,` header shape changed');
for (let i = 0; i < shape.entries.length; i++) {
  const e = shape.entries[i];
  if (e.depth === 1) continue;
  const above = shape.entries[i - 1];
  problems.push(`line ${e.line}: entry v${e.v} opens at bracket depth ${e.depth}, not 1 — it is `
    + `nested inside ${above ? `entry v${above.v} (line ${above.line}), which is missing its `
      + '`] },`' : 'something above it'}`);
  break;                                          // one report; the rest cascade
}

// Only worth executing once the shape holds — otherwise node reports a syntax
// error at the end of the file and buries the diagnosis above.
if (problems.length) report();

let CHANGELOG;
let LATEST_VERSION;
try {
  ({ CHANGELOG, LATEST_VERSION } = await import(FILE));
} catch (err) {
  problems.push(`the module does not load: ${err.message}`);
  report();
}

if (!Array.isArray(CHANGELOG) || !CHANGELOG.length) problems.push('CHANGELOG is empty');
if (LATEST_VERSION !== CHANGELOG[0]?.v) problems.push('LATEST_VERSION is not CHANGELOG[0].v');
// The text walk and the loaded array must agree on how many entries there are.
// A swallowed entry is still a valid object literal, so it can survive the
// parser and simply not be in the array — which is the silent half of the 2026-08-13
// corruption, and the half a syntax check can never see.
if (Array.isArray(CHANGELOG) && CHANGELOG.length !== shape.entries.length) {
  problems.push(`the file contains ${shape.entries.length} entry header(s) but CHANGELOG holds `
    + `${CHANGELOG.length} — ${shape.entries.length - CHANGELOG.length} entr`
    + `${shape.entries.length - CHANGELOG.length === 1 ? 'y is' : 'ies are'} nested inside another `
    + 'entry instead of standing in the array');
}

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

report();
console.log(`changelog contract OK — ${CHANGELOG.length} entr${CHANGELOG.length === 1 ? 'y' : 'ies'}`
  + ` (${shape.entries.length} in the literal), latest v${LATEST_VERSION}`);

function report() {
  if (!problems.length) return;
  console.error('changelog contract FAILED:');
  for (const p of problems) console.error('  - ' + p);
  process.exit(1);
}
